# -*- coding: utf-8 -*-
"""
cement_kiln_builder/part3_tmr_voting.py
Part 3: Phase 1 - 2oo3 Triple Modular Redundancy (TMR) Sensor Voting Suite
Pairwise discrepancy detection, 300 ms persistence timers, median selection,
bumpless degradation to 1oo2, and fallback handling across 4 critical sensor triplets.
"""

def get_part3_tmr_voting():
    return """
(* ========================================================================================================= *)
(* === PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING WITH DISCREPANCY TIMERS              === *)
(* ========================================================================================================= *)

(* --------------------------------------------------------------------------------------------------------- *)
(* SUBSECTION 1.1: BURNING ZONE TWO-COLOR OPTICAL PYROMETER TRIPLET (S1, S2, S3) [deg C]                    *)
(* Evaluates pair deviations, accumulates discrepancy timers, identifies outlier, and computes median       *)
(* --------------------------------------------------------------------------------------------------------- *)
(* Pairwise absolute discrepancy evaluation *)
IF ABS(rPyrometer_BurnZone_Temp_S1_degC - rPyrometer_BurnZone_Temp_S2_degC) > rTMR_Pyrometer_Tolerance_degC THEN
    tTMR_Pyrometer_T12_s := tTMR_Pyrometer_T12_s + rScanCycleTime_s;
ELSE
    tTMR_Pyrometer_T12_s := MAX(0.0, tTMR_Pyrometer_T12_s - (rScanCycleTime_s * 2.0));
END_IF;

IF ABS(rPyrometer_BurnZone_Temp_S2_degC - rPyrometer_BurnZone_Temp_S3_degC) > rTMR_Pyrometer_Tolerance_degC THEN
    tTMR_Pyrometer_T23_s := tTMR_Pyrometer_T23_s + rScanCycleTime_s;
ELSE
    tTMR_Pyrometer_T23_s := MAX(0.0, tTMR_Pyrometer_T23_s - (rScanCycleTime_s * 2.0));
END_IF;

IF ABS(rPyrometer_BurnZone_Temp_S3_degC - rPyrometer_BurnZone_Temp_S1_degC) > rTMR_Pyrometer_Tolerance_degC THEN
    tTMR_Pyrometer_T31_s := tTMR_Pyrometer_T31_s + rScanCycleTime_s;
ELSE
    tTMR_Pyrometer_T31_s := MAX(0.0, tTMR_Pyrometer_T31_s - (rScanCycleTime_s * 2.0));
END_IF;

(* Identify Faulty Sensor with Persistence Confirmation (300 ms) *)
IF (tTMR_Pyrometer_T12_s >= rTMR_Persistence_s) AND (tTMR_Pyrometer_T31_s >= rTMR_Persistence_s) THEN
    bTMR_Pyrometer_S1_Valid := FALSE; (* Sensor 1 deviates from both S2 and S3 *)
ELSE
    bTMR_Pyrometer_S1_Valid := TRUE;
END_IF;

IF (tTMR_Pyrometer_T12_s >= rTMR_Persistence_s) AND (tTMR_Pyrometer_T23_s >= rTMR_Persistence_s) THEN
    bTMR_Pyrometer_S2_Valid := FALSE; (* Sensor 2 deviates from both S1 and S3 *)
ELSE
    bTMR_Pyrometer_S2_Valid := TRUE;
END_IF;

IF (tTMR_Pyrometer_T23_s >= rTMR_Persistence_s) AND (tTMR_Pyrometer_T31_s >= rTMR_Persistence_s) THEN
    bTMR_Pyrometer_S3_Valid := FALSE; (* Sensor 3 deviates from both S1 and S2 *)
ELSE
    bTMR_Pyrometer_S3_Valid := TRUE;
END_IF;

(* Median Selection and Bumpless Degradation Logic *)
IF bTMR_Pyrometer_S1_Valid AND bTMR_Pyrometer_S2_Valid AND bTMR_Pyrometer_S3_Valid THEN
    (* All 3 sensors valid: Exact Mathematical Median *)
    IF ((rPyrometer_BurnZone_Temp_S1_degC >= rPyrometer_BurnZone_Temp_S2_degC) AND (rPyrometer_BurnZone_Temp_S1_degC <= rPyrometer_BurnZone_Temp_S3_degC)) OR
       ((rPyrometer_BurnZone_Temp_S1_degC <= rPyrometer_BurnZone_Temp_S2_degC) AND (rPyrometer_BurnZone_Temp_S1_degC >= rPyrometer_BurnZone_Temp_S3_degC)) THEN
        rVoted_BurnZone_Temp := rPyrometer_BurnZone_Temp_S1_degC;
    ELSIF ((rPyrometer_BurnZone_Temp_S2_degC >= rPyrometer_BurnZone_Temp_S1_degC) AND (rPyrometer_BurnZone_Temp_S2_degC <= rPyrometer_BurnZone_Temp_S3_degC)) OR
          ((rPyrometer_BurnZone_Temp_S2_degC <= rPyrometer_BurnZone_Temp_S1_degC) AND (rPyrometer_BurnZone_Temp_S2_degC >= rPyrometer_BurnZone_Temp_S3_degC)) THEN
        rVoted_BurnZone_Temp := rPyrometer_BurnZone_Temp_S2_degC;
    ELSE
        rVoted_BurnZone_Temp := rPyrometer_BurnZone_Temp_S3_degC;
    END_IF;
    bTMR_Pyrometer_Degraded := FALSE;
ELSIF bTMR_Pyrometer_S1_Valid AND bTMR_Pyrometer_S2_Valid THEN
    (* Sensor 3 failed: Degrade to 1oo2 Average of S1 and S2 *)
    rVoted_BurnZone_Temp := (rPyrometer_BurnZone_Temp_S1_degC + rPyrometer_BurnZone_Temp_S2_degC) * 0.5;
    bTMR_Pyrometer_Degraded := TRUE;
ELSIF bTMR_Pyrometer_S2_Valid AND bTMR_Pyrometer_S3_Valid THEN
    (* Sensor 1 failed: Degrade to 1oo2 Average of S2 and S3 *)
    rVoted_BurnZone_Temp := (rPyrometer_BurnZone_Temp_S2_degC + rPyrometer_BurnZone_Temp_S3_degC) * 0.5;
    bTMR_Pyrometer_Degraded := TRUE;
ELSIF bTMR_Pyrometer_S1_Valid AND bTMR_Pyrometer_S3_Valid THEN
    (* Sensor 2 failed: Degrade to 1oo2 Average of S1 and S3 *)
    rVoted_BurnZone_Temp := (rPyrometer_BurnZone_Temp_S1_degC + rPyrometer_BurnZone_Temp_S3_degC) * 0.5;
    bTMR_Pyrometer_Degraded := TRUE;
ELSIF bTMR_Pyrometer_S1_Valid THEN
    (* Dual failure: Fallback to remaining single healthy sensor S1 *)
    rVoted_BurnZone_Temp := rPyrometer_BurnZone_Temp_S1_degC;
    bTMR_Pyrometer_Degraded := TRUE;
ELSIF bTMR_Pyrometer_S2_Valid THEN
    rVoted_BurnZone_Temp := rPyrometer_BurnZone_Temp_S2_degC;
    bTMR_Pyrometer_Degraded := TRUE;
ELSIF bTMR_Pyrometer_S3_Valid THEN
    rVoted_BurnZone_Temp := rPyrometer_BurnZone_Temp_S3_degC;
    bTMR_Pyrometer_Degraded := TRUE;
ELSE
    (* Triple failure: Critical Sensor Loss - Hold Observer Estimate or Safe Default *)
    rVoted_BurnZone_Temp := rState_x_hat[1];
    bTMR_Pyrometer_Degraded := TRUE;
END_IF;

(* --------------------------------------------------------------------------------------------------------- *)
(* SUBSECTION 1.2: PRECALCINER BOTTOM THERMOCOUPLE TRIPLET (TC_S1, TC_S2, TC_S3) [deg C]                   *)
(* --------------------------------------------------------------------------------------------------------- *)
(* Pairwise absolute discrepancy evaluation *)
IF ABS(rCalciner_Temp_TC_S1_degC - rCalciner_Temp_TC_S2_degC) > rTMR_Calciner_Tolerance_degC THEN
    tTMR_Calciner_T12_s := tTMR_Calciner_T12_s + rScanCycleTime_s;
ELSE
    tTMR_Calciner_T12_s := MAX(0.0, tTMR_Calciner_T12_s - (rScanCycleTime_s * 2.0));
END_IF;

IF ABS(rCalciner_Temp_TC_S2_degC - rCalciner_Temp_TC_S3_degC) > rTMR_Calciner_Tolerance_degC THEN
    tTMR_Calciner_T23_s := tTMR_Calciner_T23_s + rScanCycleTime_s;
ELSE
    tTMR_Calciner_T23_s := MAX(0.0, tTMR_Calciner_T23_s - (rScanCycleTime_s * 2.0));
END_IF;

IF ABS(rCalciner_Temp_TC_S3_degC - rCalciner_Temp_TC_S1_degC) > rTMR_Calciner_Tolerance_degC THEN
    tTMR_Calciner_T31_s := tTMR_Calciner_T31_s + rScanCycleTime_s;
ELSE
    tTMR_Calciner_T31_s := MAX(0.0, tTMR_Calciner_T31_s - (rScanCycleTime_s * 2.0));
END_IF;

(* Identify Faulty Sensor with Persistence Confirmation (300 ms) *)
IF (tTMR_Calciner_T12_s >= rTMR_Persistence_s) AND (tTMR_Calciner_T31_s >= rTMR_Persistence_s) THEN
    bTMR_Calciner_S1_Valid := FALSE;
ELSE
    bTMR_Calciner_S1_Valid := TRUE;
END_IF;

IF (tTMR_Calciner_T12_s >= rTMR_Persistence_s) AND (tTMR_Calciner_T23_s >= rTMR_Persistence_s) THEN
    bTMR_Calciner_S2_Valid := FALSE;
ELSE
    bTMR_Calciner_S2_Valid := TRUE;
END_IF;

IF (tTMR_Calciner_T23_s >= rTMR_Persistence_s) AND (tTMR_Calciner_T31_s >= rTMR_Persistence_s) THEN
    bTMR_Calciner_S3_Valid := FALSE;
ELSE
    bTMR_Calciner_S3_Valid := TRUE;
END_IF;

(* Median Selection and Bumpless Degradation Logic *)
IF bTMR_Calciner_S1_Valid AND bTMR_Calciner_S2_Valid AND bTMR_Calciner_S3_Valid THEN
    IF ((rCalciner_Temp_TC_S1_degC >= rCalciner_Temp_TC_S2_degC) AND (rCalciner_Temp_TC_S1_degC <= rCalciner_Temp_TC_S3_degC)) OR
       ((rCalciner_Temp_TC_S1_degC <= rCalciner_Temp_TC_S2_degC) AND (rCalciner_Temp_TC_S1_degC >= rCalciner_Temp_TC_S3_degC)) THEN
        rVoted_Calciner_Temp := rCalciner_Temp_TC_S1_degC;
    ELSIF ((rCalciner_Temp_TC_S2_degC >= rCalciner_Temp_TC_S1_degC) AND (rCalciner_Temp_TC_S2_degC <= rCalciner_Temp_TC_S3_degC)) OR
          ((rCalciner_Temp_TC_S2_degC <= rCalciner_Temp_TC_S1_degC) AND (rCalciner_Temp_TC_S2_degC >= rCalciner_Temp_TC_S3_degC)) THEN
        rVoted_Calciner_Temp := rCalciner_Temp_TC_S2_degC;
    ELSE
        rVoted_Calciner_Temp := rCalciner_Temp_TC_S3_degC;
    END_IF;
    bTMR_Calciner_Degraded := FALSE;
ELSIF bTMR_Calciner_S1_Valid AND bTMR_Calciner_S2_Valid THEN
    rVoted_Calciner_Temp := (rCalciner_Temp_TC_S1_degC + rCalciner_Temp_TC_S2_degC) * 0.5;
    bTMR_Calciner_Degraded := TRUE;
ELSIF bTMR_Calciner_S2_Valid AND bTMR_Calciner_S3_Valid THEN
    rVoted_Calciner_Temp := (rCalciner_Temp_TC_S2_degC + rCalciner_Temp_TC_S3_degC) * 0.5;
    bTMR_Calciner_Degraded := TRUE;
ELSIF bTMR_Calciner_S1_Valid AND bTMR_Calciner_S3_Valid THEN
    rVoted_Calciner_Temp := (rCalciner_Temp_TC_S1_degC + rCalciner_Temp_TC_S3_degC) * 0.5;
    bTMR_Calciner_Degraded := TRUE;
ELSIF bTMR_Calciner_S1_Valid THEN
    rVoted_Calciner_Temp := rCalciner_Temp_TC_S1_degC;
    bTMR_Calciner_Degraded := TRUE;
ELSIF bTMR_Calciner_S2_Valid THEN
    rVoted_Calciner_Temp := rCalciner_Temp_TC_S2_degC;
    bTMR_Calciner_Degraded := TRUE;
ELSIF bTMR_Calciner_S3_Valid THEN
    rVoted_Calciner_Temp := rCalciner_Temp_TC_S3_degC;
    bTMR_Calciner_Degraded := TRUE;
ELSE
    rVoted_Calciner_Temp := rState_x_hat[2];
    bTMR_Calciner_Degraded := TRUE;
END_IF;

(* --------------------------------------------------------------------------------------------------------- *)
(* SUBSECTION 1.3: KILN INLET CARBON MONOXIDE (CO) ANALYZER TRIPLET (CO_1, CO_2, CO_3) [%]                   *)
(* High-integrity optical / paramagnetic detection to prevent preheater explosive deflagration               *)
(* --------------------------------------------------------------------------------------------------------- *)
IF ABS(rKilnInlet_CO_Sens1_pct - rKilnInlet_CO_Sens2_pct) > rTMR_CO_Tolerance_pct THEN
    tTMR_CO_T12_s := tTMR_CO_T12_s + rScanCycleTime_s;
ELSE
    tTMR_CO_T12_s := MAX(0.0, tTMR_CO_T12_s - (rScanCycleTime_s * 2.0));
END_IF;

IF ABS(rKilnInlet_CO_Sens2_pct - rKilnInlet_CO_Sens3_pct) > rTMR_CO_Tolerance_pct THEN
    tTMR_CO_T23_s := tTMR_CO_T23_s + rScanCycleTime_s;
ELSE
    tTMR_CO_T23_s := MAX(0.0, tTMR_CO_T23_s - (rScanCycleTime_s * 2.0));
END_IF;

IF ABS(rKilnInlet_CO_Sens3_pct - rKilnInlet_CO_Sens1_pct) > rTMR_CO_Tolerance_pct THEN
    tTMR_CO_T31_s := tTMR_CO_T31_s + rScanCycleTime_s;
ELSE
    tTMR_CO_T31_s := MAX(0.0, tTMR_CO_T31_s - (rScanCycleTime_s * 2.0));
END_IF;

IF (tTMR_CO_T12_s >= rTMR_Persistence_s) AND (tTMR_CO_T31_s >= rTMR_Persistence_s) THEN
    bTMR_CO_S1_Valid := FALSE;
ELSE
    bTMR_CO_S1_Valid := TRUE;
END_IF;

IF (tTMR_CO_T12_s >= rTMR_Persistence_s) AND (tTMR_CO_T23_s >= rTMR_Persistence_s) THEN
    bTMR_CO_S2_Valid := FALSE;
ELSE
    bTMR_CO_S2_Valid := TRUE;
END_IF;

IF (tTMR_CO_T23_s >= rTMR_Persistence_s) AND (tTMR_CO_T31_s >= rTMR_Persistence_s) THEN
    bTMR_CO_S3_Valid := FALSE;
ELSE
    bTMR_CO_S3_Valid := TRUE;
END_IF;

IF bTMR_CO_S1_Valid AND bTMR_CO_S2_Valid AND bTMR_CO_S3_Valid THEN
    IF ((rKilnInlet_CO_Sens1_pct >= rKilnInlet_CO_Sens2_pct) AND (rKilnInlet_CO_Sens1_pct <= rKilnInlet_CO_Sens3_pct)) OR
       ((rKilnInlet_CO_Sens1_pct <= rKilnInlet_CO_Sens2_pct) AND (rKilnInlet_CO_Sens1_pct >= rKilnInlet_CO_Sens3_pct)) THEN
        rVoted_KilnInlet_CO := rKilnInlet_CO_Sens1_pct;
    ELSIF ((rKilnInlet_CO_Sens2_pct >= rKilnInlet_CO_Sens1_pct) AND (rKilnInlet_CO_Sens2_pct <= rKilnInlet_CO_Sens3_pct)) OR
          ((rKilnInlet_CO_Sens2_pct <= rKilnInlet_CO_Sens1_pct) AND (rKilnInlet_CO_Sens2_pct >= rKilnInlet_CO_Sens3_pct)) THEN
        rVoted_KilnInlet_CO := rKilnInlet_CO_Sens2_pct;
    ELSE
        rVoted_KilnInlet_CO := rKilnInlet_CO_Sens3_pct;
    END_IF;
    bTMR_CO_Degraded := FALSE;
ELSIF bTMR_CO_S1_Valid AND bTMR_CO_S2_Valid THEN
    (* Fail-safe high selection when degraded to protect electrostatic precipitator *)
    rVoted_KilnInlet_CO := MAX(rKilnInlet_CO_Sens1_pct, rKilnInlet_CO_Sens2_pct);
    bTMR_CO_Degraded := TRUE;
ELSIF bTMR_CO_S2_Valid AND bTMR_CO_S3_Valid THEN
    rVoted_KilnInlet_CO := MAX(rKilnInlet_CO_Sens2_pct, rKilnInlet_CO_Sens3_pct);
    bTMR_CO_Degraded := TRUE;
ELSIF bTMR_CO_S1_Valid AND bTMR_CO_S3_Valid THEN
    rVoted_KilnInlet_CO := MAX(rKilnInlet_CO_Sens1_pct, rKilnInlet_CO_Sens3_pct);
    bTMR_CO_Degraded := TRUE;
ELSIF bTMR_CO_S1_Valid THEN
    rVoted_KilnInlet_CO := rKilnInlet_CO_Sens1_pct;
    bTMR_CO_Degraded := TRUE;
ELSIF bTMR_CO_S2_Valid THEN
    rVoted_KilnInlet_CO := rKilnInlet_CO_Sens2_pct;
    bTMR_CO_Degraded := TRUE;
ELSIF bTMR_CO_S3_Valid THEN
    rVoted_KilnInlet_CO := rKilnInlet_CO_Sens3_pct;
    bTMR_CO_Degraded := TRUE;
ELSE
    rVoted_KilnInlet_CO := MAX(0.25, rState_x_hat[6]); (* Conservative safe default *)
    bTMR_CO_Degraded := TRUE;
END_IF;

(* --------------------------------------------------------------------------------------------------------- *)
(* SUBSECTION 1.4: PREHEATER STAGE C1 DRAFT PRESSURE TRIPLET (P1, P2, P3) [mbar]                             *)
(* Critical for induced draft fan control and preventing positive flue gas blowouts                           *)
(* --------------------------------------------------------------------------------------------------------- *)
IF ABS(rPreheater_TopDraft_P1_mbar - rPreheater_TopDraft_P2_mbar) > rTMR_Draft_Tolerance_mbar THEN
    tTMR_Draft_T12_s := tTMR_Draft_T12_s + rScanCycleTime_s;
ELSE
    tTMR_Draft_T12_s := MAX(0.0, tTMR_Draft_T12_s - (rScanCycleTime_s * 2.0));
END_IF;

IF ABS(rPreheater_TopDraft_P2_mbar - rPreheater_TopDraft_P3_mbar) > rTMR_Draft_Tolerance_mbar THEN
    tTMR_Draft_T23_s := tTMR_Draft_T23_s + rScanCycleTime_s;
ELSE
    tTMR_Draft_T23_s := MAX(0.0, tTMR_Draft_T23_s - (rScanCycleTime_s * 2.0));
END_IF;

IF ABS(rPreheater_TopDraft_P3_mbar - rPreheater_TopDraft_P1_mbar) > rTMR_Draft_Tolerance_mbar THEN
    tTMR_Draft_T31_s := tTMR_Draft_T31_s + rScanCycleTime_s;
ELSE
    tTMR_Draft_T31_s := MAX(0.0, tTMR_Draft_T31_s - (rScanCycleTime_s * 2.0));
END_IF;

IF (tTMR_Draft_T12_s >= rTMR_Persistence_s) AND (tTMR_Draft_T31_s >= rTMR_Persistence_s) THEN
    bTMR_Draft_P1_Valid := FALSE;
ELSE
    bTMR_Draft_P1_Valid := TRUE;
END_IF;

IF (tTMR_Draft_T12_s >= rTMR_Persistence_s) AND (tTMR_Draft_T23_s >= rTMR_Persistence_s) THEN
    bTMR_Draft_P2_Valid := FALSE;
ELSE
    bTMR_Draft_P2_Valid := TRUE;
END_IF;

IF (tTMR_Draft_T23_s >= rTMR_Persistence_s) AND (tTMR_Draft_T31_s >= rTMR_Persistence_s) THEN
    bTMR_Draft_P3_Valid := FALSE;
ELSE
    bTMR_Draft_P3_Valid := TRUE;
END_IF;

IF bTMR_Draft_P1_Valid AND bTMR_Draft_P2_Valid AND bTMR_Draft_P3_Valid THEN
    IF ((rPreheater_TopDraft_P1_mbar >= rPreheater_TopDraft_P2_mbar) AND (rPreheater_TopDraft_P1_mbar <= rPreheater_TopDraft_P3_mbar)) OR
       ((rPreheater_TopDraft_P1_mbar <= rPreheater_TopDraft_P2_mbar) AND (rPreheater_TopDraft_P1_mbar >= rPreheater_TopDraft_P3_mbar)) THEN
        rVoted_Preheater_Draft := rPreheater_TopDraft_P1_mbar;
    ELSIF ((rPreheater_TopDraft_P2_mbar >= rPreheater_TopDraft_P1_mbar) AND (rPreheater_TopDraft_P2_mbar <= rPreheater_TopDraft_P3_mbar)) OR
          ((rPreheater_TopDraft_P2_mbar <= rPreheater_TopDraft_P1_mbar) AND (rPreheater_TopDraft_P2_mbar >= rPreheater_TopDraft_P3_mbar)) THEN
        rVoted_Preheater_Draft := rPreheater_TopDraft_P2_mbar;
    ELSE
        rVoted_Preheater_Draft := rPreheater_TopDraft_P3_mbar;
    END_IF;
    bTMR_Draft_Degraded := FALSE;
ELSIF bTMR_Draft_P1_Valid AND bTMR_Draft_P2_Valid THEN
    rVoted_Preheater_Draft := (rPreheater_TopDraft_P1_mbar + rPreheater_TopDraft_P2_mbar) * 0.5;
    bTMR_Draft_Degraded := TRUE;
ELSIF bTMR_Draft_P2_Valid AND bTMR_Draft_P3_Valid THEN
    rVoted_Preheater_Draft := (rPreheater_TopDraft_P2_mbar + rPreheater_TopDraft_P3_mbar) * 0.5;
    bTMR_Draft_Degraded := TRUE;
ELSIF bTMR_Draft_P1_Valid AND bTMR_Draft_P3_Valid THEN
    rVoted_Preheater_Draft := (rPreheater_TopDraft_P1_mbar + rPreheater_TopDraft_P3_mbar) * 0.5;
    bTMR_Draft_Degraded := TRUE;
ELSIF bTMR_Draft_P1_Valid THEN
    rVoted_Preheater_Draft := rPreheater_TopDraft_P1_mbar;
    bTMR_Draft_Degraded := TRUE;
ELSIF bTMR_Draft_P2_Valid THEN
    rVoted_Preheater_Draft := rPreheater_TopDraft_P2_mbar;
    bTMR_Draft_Degraded := TRUE;
ELSIF bTMR_Draft_P3_Valid THEN
    rVoted_Preheater_Draft := rPreheater_TopDraft_P3_mbar;
    bTMR_Draft_Degraded := TRUE;
ELSE
    rVoted_Preheater_Draft := -45.0; (* Standard nominal design draft default *)
    bTMR_Draft_Degraded := TRUE;
END_IF;
"""
