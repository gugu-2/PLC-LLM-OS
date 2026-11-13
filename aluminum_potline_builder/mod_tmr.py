# -*- coding: utf-8 -*-
"""
Module: aluminum_potline_builder/mod_tmr.py
Implements Phase 1: Quadruple 2oo3 Triple Modular Redundancy (TMR) Sensor Voting Logic
for Cell Voltage, Line Current, Bath Temperature, and Beam Position.
"""

def generate_tmr():
    return '''(* =====================================================================================================================
 * PHASE 1: QUADRUPLE 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING SUITE
 * Incorporates pairwise deviation cross-checks, 300 ms persistence timers, bumpless degradation, and fault isolation.
 * ===================================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------------------------
 * 1. POT CELL VOLTAGE TRANSMITTERS (CH1, CH2, CH3) [V]
 * Nominal: 4.15 V, Discrepancy Tolerance: 0.150 V, Trip Persistence: 300.0 ms
 * --------------------------------------------------------------------------------------------------------------------- *)
rDev_Volt_12 := ABS(rCellVoltage_CH1_V - rCellVoltage_CH2_V);
rDev_Volt_23 := ABS(rCellVoltage_CH2_V - rCellVoltage_CH3_V);
rDev_Volt_31 := ABS(rCellVoltage_CH3_V - rCellVoltage_CH1_V);

bDiscr_Volt_12 := (rDev_Volt_12 > 0.150);
bDiscr_Volt_23 := (rDev_Volt_23 > 0.150);
bDiscr_Volt_31 := (rDev_Volt_31 > 0.150);

(* Channel 1-2 Discrepancy Timer *)
IF bDiscr_Volt_12 THEN
    rTimer_Volt_12_ms := rTimer_Volt_12_ms + (rLocalDeltaT_s * 1000.0);
ELSE
    IF rTimer_Volt_12_ms > (rLocalDeltaT_s * 500.0) THEN
        rTimer_Volt_12_ms := rTimer_Volt_12_ms - (rLocalDeltaT_s * 500.0);
    ELSE
        rTimer_Volt_12_ms := 0.0;
    END_IF;
END_IF;

(* Channel 2-3 Discrepancy Timer *)
IF bDiscr_Volt_23 THEN
    rTimer_Volt_23_ms := rTimer_Volt_23_ms + (rLocalDeltaT_s * 1000.0);
ELSE
    IF rTimer_Volt_23_ms > (rLocalDeltaT_s * 500.0) THEN
        rTimer_Volt_23_ms := rTimer_Volt_23_ms - (rLocalDeltaT_s * 500.0);
    ELSE
        rTimer_Volt_23_ms := 0.0;
    END_IF;
END_IF;

(* Channel 3-1 Discrepancy Timer *)
IF bDiscr_Volt_31 THEN
    rTimer_Volt_31_ms := rTimer_Volt_31_ms + (rLocalDeltaT_s * 1000.0);
ELSE
    IF rTimer_Volt_31_ms > (rLocalDeltaT_s * 500.0) THEN
        rTimer_Volt_31_ms := rTimer_Volt_31_ms - (rLocalDeltaT_s * 500.0);
    ELSE
        rTimer_Volt_31_ms := 0.0;
    END_IF;
END_IF;

(* Channel Integrity and Fault Isolation *)
IF rTimer_Volt_12_ms >= 300.0 AND rTimer_Volt_31_ms >= 300.0 THEN
    bHealth_Volt_CH1 := FALSE; (* Channel 1 deviates from both Channel 2 and 3 *)
END_IF;

IF rTimer_Volt_12_ms >= 300.0 AND rTimer_Volt_23_ms >= 300.0 THEN
    bHealth_Volt_CH2 := FALSE; (* Channel 2 deviates from both Channel 1 and 3 *)
END_IF;

IF rTimer_Volt_23_ms >= 300.0 AND rTimer_Volt_31_ms >= 300.0 THEN
    bHealth_Volt_CH3 := FALSE; (* Channel 3 deviates from both Channel 1 and 2 *)
END_IF;

(* Plausibility clamp check [0.5 V to 65.0 V] *)
IF rCellVoltage_CH1_V < 0.50 OR rCellVoltage_CH1_V > 65.00 THEN bHealth_Volt_CH1 := FALSE; END_IF;
IF rCellVoltage_CH2_V < 0.50 OR rCellVoltage_CH2_V > 65.00 THEN bHealth_Volt_CH2 := FALSE; END_IF;
IF rCellVoltage_CH3_V < 0.50 OR rCellVoltage_CH3_V > 65.00 THEN bHealth_Volt_CH3 := FALSE; END_IF;

(* 2oo3 Voting / Degraded Selection *)
IF bHealth_Volt_CH1 AND bHealth_Volt_CH2 AND bHealth_Volt_CH3 THEN
    (* All 3 Channels Healthy: Median Selection *)
    nDegradedMode_Volt := 0;
    IF (rCellVoltage_CH1_V >= rCellVoltage_CH2_V AND rCellVoltage_CH1_V <= rCellVoltage_CH3_V) OR
       (rCellVoltage_CH1_V <= rCellVoltage_CH2_V AND rCellVoltage_CH1_V >= rCellVoltage_CH3_V) THEN
        rPot_VotedCellVoltage_V := rCellVoltage_CH1_V;
    ELSIF (rCellVoltage_CH2_V >= rCellVoltage_CH1_V AND rCellVoltage_CH2_V <= rCellVoltage_CH3_V) OR
          (rCellVoltage_CH2_V <= rCellVoltage_CH1_V AND rCellVoltage_CH2_V >= rCellVoltage_CH3_V) THEN
        rPot_VotedCellVoltage_V := rCellVoltage_CH2_V;
    ELSE
        rPot_VotedCellVoltage_V := rCellVoltage_CH3_V;
    END_IF;
ELSIF bHealth_Volt_CH1 AND bHealth_Volt_CH2 AND NOT bHealth_Volt_CH3 THEN
    nDegradedMode_Volt := 1;
    rPot_VotedCellVoltage_V := (rCellVoltage_CH1_V + rCellVoltage_CH2_V) * 0.50;
ELSIF bHealth_Volt_CH1 AND NOT bHealth_Volt_CH2 AND bHealth_Volt_CH3 THEN
    nDegradedMode_Volt := 1;
    rPot_VotedCellVoltage_V := (rCellVoltage_CH1_V + rCellVoltage_CH3_V) * 0.50;
ELSIF NOT bHealth_Volt_CH1 AND bHealth_Volt_CH2 AND bHealth_Volt_CH3 THEN
    nDegradedMode_Volt := 1;
    rPot_VotedCellVoltage_V := (rCellVoltage_CH2_V + rCellVoltage_CH3_V) * 0.50;
ELSIF bHealth_Volt_CH1 THEN
    nDegradedMode_Volt := 2;
    rPot_VotedCellVoltage_V := rCellVoltage_CH1_V;
ELSIF bHealth_Volt_CH2 THEN
    nDegradedMode_Volt := 2;
    rPot_VotedCellVoltage_V := rCellVoltage_CH2_V;
ELSIF bHealth_Volt_CH3 THEN
    nDegradedMode_Volt := 2;
    rPot_VotedCellVoltage_V := rCellVoltage_CH3_V;
ELSE
    nDegradedMode_Volt := 3;
    (* All channels unhealthy - latch last valid or fallback to 4.150 V *)
    IF rPot_VotedCellVoltage_V < 1.00 OR rPot_VotedCellVoltage_V > 60.00 THEN
        rPot_VotedCellVoltage_V := 4.150;
    END_IF;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * 2. POTLINE DC TOTAL CURRENT TRANSDUCTORS (CH1, CH2, CH3) [kA]
 * Nominal: 500.0 kA, Discrepancy Tolerance: 15.0 kA, Trip Persistence: 300.0 ms
 * --------------------------------------------------------------------------------------------------------------------- *)
rDev_Curr_12 := ABS(rLineCurrent_CH1_kA - rLineCurrent_CH2_kA);
rDev_Curr_23 := ABS(rLineCurrent_CH2_kA - rLineCurrent_CH3_kA);
rDev_Curr_31 := ABS(rLineCurrent_CH3_kA - rLineCurrent_CH1_kA);

bDiscr_Curr_12 := (rDev_Curr_12 > 15.0);
bDiscr_Curr_23 := (rDev_Curr_23 > 15.0);
bDiscr_Curr_31 := (rDev_Curr_31 > 15.0);

IF bDiscr_Curr_12 THEN
    rTimer_Curr_12_ms := rTimer_Curr_12_ms + (rLocalDeltaT_s * 1000.0);
ELSE
    IF rTimer_Curr_12_ms > (rLocalDeltaT_s * 500.0) THEN
        rTimer_Curr_12_ms := rTimer_Curr_12_ms - (rLocalDeltaT_s * 500.0);
    ELSE
        rTimer_Curr_12_ms := 0.0;
    END_IF;
END_IF;

IF bDiscr_Curr_23 THEN
    rTimer_Curr_23_ms := rTimer_Curr_23_ms + (rLocalDeltaT_s * 1000.0);
ELSE
    IF rTimer_Curr_23_ms > (rLocalDeltaT_s * 500.0) THEN
        rTimer_Curr_23_ms := rTimer_Curr_23_ms - (rLocalDeltaT_s * 500.0);
    ELSE
        rTimer_Curr_23_ms := 0.0;
    END_IF;
END_IF;

IF bDiscr_Curr_31 THEN
    rTimer_Curr_31_ms := rTimer_Curr_31_ms + (rLocalDeltaT_s * 1000.0);
ELSE
    IF rTimer_Curr_31_ms > (rLocalDeltaT_s * 500.0) THEN
        rTimer_Curr_31_ms := rTimer_Curr_31_ms - (rLocalDeltaT_s * 500.0);
    ELSE
        rTimer_Curr_31_ms := 0.0;
    END_IF;
END_IF;

IF rTimer_Curr_12_ms >= 300.0 AND rTimer_Curr_31_ms >= 300.0 THEN
    bHealth_Curr_CH1 := FALSE;
END_IF;

IF rTimer_Curr_12_ms >= 300.0 AND rTimer_Curr_23_ms >= 300.0 THEN
    bHealth_Curr_CH2 := FALSE;
END_IF;

IF rTimer_Curr_23_ms >= 300.0 AND rTimer_Curr_31_ms >= 300.0 THEN
    bHealth_Curr_CH3 := FALSE;
END_IF;

IF rLineCurrent_CH1_kA < 10.0 OR rLineCurrent_CH1_kA > 650.0 THEN bHealth_Curr_CH1 := FALSE; END_IF;
IF rLineCurrent_CH2_kA < 10.0 OR rLineCurrent_CH2_kA > 650.0 THEN bHealth_Curr_CH2 := FALSE; END_IF;
IF rLineCurrent_CH3_kA < 10.0 OR rLineCurrent_CH3_kA > 650.0 THEN bHealth_Curr_CH3 := FALSE; END_IF;

IF bHealth_Curr_CH1 AND bHealth_Curr_CH2 AND bHealth_Curr_CH3 THEN
    nDegradedMode_Curr := 0;
    IF (rLineCurrent_CH1_kA >= rLineCurrent_CH2_kA AND rLineCurrent_CH1_kA <= rLineCurrent_CH3_kA) OR
       (rLineCurrent_CH1_kA <= rLineCurrent_CH2_kA AND rLineCurrent_CH1_kA >= rLineCurrent_CH3_kA) THEN
        rPot_VotedLineCurrent_kA := rLineCurrent_CH1_kA;
    ELSIF (rLineCurrent_CH2_kA >= rLineCurrent_CH1_kA AND rLineCurrent_CH2_kA <= rLineCurrent_CH3_kA) OR
          (rLineCurrent_CH2_kA <= rLineCurrent_CH1_kA AND rLineCurrent_CH2_kA >= rLineCurrent_CH3_kA) THEN
        rPot_VotedLineCurrent_kA := rLineCurrent_CH2_kA;
    ELSE
        rPot_VotedLineCurrent_kA := rLineCurrent_CH3_kA;
    END_IF;
ELSIF bHealth_Curr_CH1 AND bHealth_Curr_CH2 AND NOT bHealth_Curr_CH3 THEN
    nDegradedMode_Curr := 1;
    rPot_VotedLineCurrent_kA := (rLineCurrent_CH1_kA + rLineCurrent_CH2_kA) * 0.50;
ELSIF bHealth_Curr_CH1 AND NOT bHealth_Curr_CH2 AND bHealth_Curr_CH3 THEN
    nDegradedMode_Curr := 1;
    rPot_VotedLineCurrent_kA := (rLineCurrent_CH1_kA + rLineCurrent_CH3_kA) * 0.50;
ELSIF NOT bHealth_Curr_CH1 AND bHealth_Curr_CH2 AND bHealth_Curr_CH3 THEN
    nDegradedMode_Curr := 1;
    rPot_VotedLineCurrent_kA := (rLineCurrent_CH2_kA + rLineCurrent_CH3_kA) * 0.50;
ELSIF bHealth_Curr_CH1 THEN
    nDegradedMode_Curr := 2;
    rPot_VotedLineCurrent_kA := rLineCurrent_CH1_kA;
ELSIF bHealth_Curr_CH2 THEN
    nDegradedMode_Curr := 2;
    rPot_VotedLineCurrent_kA := rLineCurrent_CH2_kA;
ELSIF bHealth_Curr_CH3 THEN
    nDegradedMode_Curr := 2;
    rPot_VotedLineCurrent_kA := rLineCurrent_CH3_kA;
ELSE
    nDegradedMode_Curr := 3;
    IF rPot_VotedLineCurrent_kA < 50.0 OR rPot_VotedLineCurrent_kA > 600.0 THEN
        rPot_VotedLineCurrent_kA := 500.0; (* Fallback nominal potline rating *)
    END_IF;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * 3. MOLTEN BATH ELECTROLYTE TEMPERATURE SENSORS (CH1, CH2, CH3) [deg C]
 * Nominal: 955.0 deg C, Discrepancy Tolerance: 12.0 deg C, Trip Persistence: 300.0 ms
 * --------------------------------------------------------------------------------------------------------------------- *)
rDev_Temp_12 := ABS(rBathTemp_CH1_degC - rBathTemp_CH2_degC);
rDev_Temp_23 := ABS(rBathTemp_CH2_degC - rBathTemp_CH3_degC);
rDev_Temp_31 := ABS(rBathTemp_CH3_degC - rBathTemp_CH1_degC);

bDiscr_Temp_12 := (rDev_Temp_12 > 12.0);
bDiscr_Temp_23 := (rDev_Temp_23 > 12.0);
bDiscr_Temp_31 := (rDev_Temp_31 > 12.0);

IF bDiscr_Temp_12 THEN
    rTimer_Temp_12_ms := rTimer_Temp_12_ms + (rLocalDeltaT_s * 1000.0);
ELSE
    IF rTimer_Temp_12_ms > (rLocalDeltaT_s * 500.0) THEN
        rTimer_Temp_12_ms := rTimer_Temp_12_ms - (rLocalDeltaT_s * 500.0);
    ELSE
        rTimer_Temp_12_ms := 0.0;
    END_IF;
END_IF;

IF bDiscr_Temp_23 THEN
    rTimer_Temp_23_ms := rTimer_Temp_23_ms + (rLocalDeltaT_s * 1000.0);
ELSE
    IF rTimer_Temp_23_ms > (rLocalDeltaT_s * 500.0) THEN
        rTimer_Temp_23_ms := rTimer_Temp_23_ms - (rLocalDeltaT_s * 500.0);
    ELSE
        rTimer_Temp_23_ms := 0.0;
    END_IF;
END_IF;

IF bDiscr_Temp_31 THEN
    rTimer_Temp_31_ms := rTimer_Temp_31_ms + (rLocalDeltaT_s * 1000.0);
ELSE
    IF rTimer_Temp_31_ms > (rLocalDeltaT_s * 500.0) THEN
        rTimer_Temp_31_ms := rTimer_Temp_31_ms - (rLocalDeltaT_s * 500.0);
    ELSE
        rTimer_Temp_31_ms := 0.0;
    END_IF;
END_IF;

IF rTimer_Temp_12_ms >= 300.0 AND rTimer_Temp_31_ms >= 300.0 THEN
    bHealth_Temp_CH1 := FALSE;
END_IF;

IF rTimer_Temp_12_ms >= 300.0 AND rTimer_Temp_23_ms >= 300.0 THEN
    bHealth_Temp_CH2 := FALSE;
END_IF;

IF rTimer_Temp_23_ms >= 300.0 AND rTimer_Temp_31_ms >= 300.0 THEN
    bHealth_Temp_CH3 := FALSE;
END_IF;

IF rBathTemp_CH1_degC < 850.0 OR rBathTemp_CH1_degC > 1150.0 THEN bHealth_Temp_CH1 := FALSE; END_IF;
IF rBathTemp_CH2_degC < 850.0 OR rBathTemp_CH2_degC > 1150.0 THEN bHealth_Temp_CH2 := FALSE; END_IF;
IF rBathTemp_CH3_degC < 850.0 OR rBathTemp_CH3_degC > 1150.0 THEN bHealth_Temp_CH3 := FALSE; END_IF;

IF bHealth_Temp_CH1 AND bHealth_Temp_CH2 AND bHealth_Temp_CH3 THEN
    nDegradedMode_Temp := 0;
    IF (rBathTemp_CH1_degC >= rBathTemp_CH2_degC AND rBathTemp_CH1_degC <= rBathTemp_CH3_degC) OR
       (rBathTemp_CH1_degC <= rBathTemp_CH2_degC AND rBathTemp_CH1_degC >= rBathTemp_CH3_degC) THEN
        rPot_VotedBathTemp_degC := rBathTemp_CH1_degC;
    ELSIF (rBathTemp_CH2_degC >= rBathTemp_CH1_degC AND rBathTemp_CH2_degC <= rBathTemp_CH3_degC) OR
          (rBathTemp_CH2_degC <= rBathTemp_CH1_degC AND rBathTemp_CH2_degC >= rBathTemp_CH3_degC) THEN
        rPot_VotedBathTemp_degC := rBathTemp_CH2_degC;
    ELSE
        rPot_VotedBathTemp_degC := rBathTemp_CH3_degC;
    END_IF;
ELSIF bHealth_Temp_CH1 AND bHealth_Temp_CH2 AND NOT bHealth_Temp_CH3 THEN
    nDegradedMode_Temp := 1;
    rPot_VotedBathTemp_degC := (rBathTemp_CH1_degC + rBathTemp_CH2_degC) * 0.50;
ELSIF bHealth_Temp_CH1 AND NOT bHealth_Temp_CH2 AND bHealth_Temp_CH3 THEN
    nDegradedMode_Temp := 1;
    rPot_VotedBathTemp_degC := (rBathTemp_CH1_degC + rBathTemp_CH3_degC) * 0.50;
ELSIF NOT bHealth_Temp_CH1 AND bHealth_Temp_CH2 AND bHealth_Temp_CH3 THEN
    nDegradedMode_Temp := 1;
    rPot_VotedBathTemp_degC := (rBathTemp_CH2_degC + rBathTemp_CH3_degC) * 0.50;
ELSIF bHealth_Temp_CH1 THEN
    nDegradedMode_Temp := 2;
    rPot_VotedBathTemp_degC := rBathTemp_CH1_degC;
ELSIF bHealth_Temp_CH2 THEN
    nDegradedMode_Temp := 2;
    rPot_VotedBathTemp_degC := rBathTemp_CH2_degC;
ELSIF bHealth_Temp_CH3 THEN
    nDegradedMode_Temp := 2;
    rPot_VotedBathTemp_degC := rBathTemp_CH3_degC;
ELSE
    nDegradedMode_Temp := 3;
    IF rPot_VotedBathTemp_degC < 880.0 OR rPot_VotedBathTemp_degC > 1050.0 THEN
        rPot_VotedBathTemp_degC := 955.0; (* Fallback nominal bath operating temperature *)
    END_IF;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * 4. ANODE BEAM ABSOLUTE LINEAR ENCODERS (CH1, CH2, CH3) [mm]
 * Nominal: 0.0 - 500.0 mm, Discrepancy Tolerance: 2.5 mm, Trip Persistence: 300.0 ms
 * --------------------------------------------------------------------------------------------------------------------- *)
rDev_Pos_12 := ABS(rBeamPos_CH1_mm - rBeamPos_CH2_mm);
rDev_Pos_23 := ABS(rBeamPos_CH2_mm - rBeamPos_CH3_mm);
rDev_Pos_31 := ABS(rBeamPos_CH3_mm - rBeamPos_CH1_mm);

bDiscr_Pos_12 := (rDev_Pos_12 > 2.50);
bDiscr_Pos_23 := (rDev_Pos_23 > 2.50);
bDiscr_Pos_31 := (rDev_Pos_31 > 2.50);

IF bDiscr_Pos_12 THEN
    rTimer_Pos_12_ms := rTimer_Pos_12_ms + (rLocalDeltaT_s * 1000.0);
ELSE
    IF rTimer_Pos_12_ms > (rLocalDeltaT_s * 500.0) THEN
        rTimer_Pos_12_ms := rTimer_Pos_12_ms - (rLocalDeltaT_s * 500.0);
    ELSE
        rTimer_Pos_12_ms := 0.0;
    END_IF;
END_IF;

IF bDiscr_Pos_23 THEN
    rTimer_Pos_23_ms := rTimer_Pos_23_ms + (rLocalDeltaT_s * 1000.0);
ELSE
    IF rTimer_Pos_23_ms > (rLocalDeltaT_s * 500.0) THEN
        rTimer_Pos_23_ms := rTimer_Pos_23_ms - (rLocalDeltaT_s * 500.0);
    ELSE
        rTimer_Pos_23_ms := 0.0;
    END_IF;
END_IF;

IF bDiscr_Pos_31 THEN
    rTimer_Pos_31_ms := rTimer_Pos_31_ms + (rLocalDeltaT_s * 1000.0);
ELSE
    IF rTimer_Pos_31_ms > (rLocalDeltaT_s * 500.0) THEN
        rTimer_Pos_31_ms := rTimer_Pos_31_ms - (rLocalDeltaT_s * 500.0);
    ELSE
        rTimer_Pos_31_ms := 0.0;
    END_IF;
END_IF;

IF rTimer_Pos_12_ms >= 300.0 AND rTimer_Pos_31_ms >= 300.0 THEN
    bHealth_Pos_CH1 := FALSE;
END_IF;

IF rTimer_Pos_12_ms >= 300.0 AND rTimer_Pos_23_ms >= 300.0 THEN
    bHealth_Pos_CH2 := FALSE;
END_IF;

IF rTimer_Pos_23_ms >= 300.0 AND rTimer_Pos_31_ms >= 300.0 THEN
    bHealth_Pos_CH3 := FALSE;
END_IF;

IF rBeamPos_CH1_mm < -50.0 OR rBeamPos_CH1_mm > 600.0 THEN bHealth_Pos_CH1 := FALSE; END_IF;
IF rBeamPos_CH2_mm < -50.0 OR rBeamPos_CH2_mm > 600.0 THEN bHealth_Pos_CH2 := FALSE; END_IF;
IF rBeamPos_CH3_mm < -50.0 OR rBeamPos_CH3_mm > 600.0 THEN bHealth_Pos_CH3 := FALSE; END_IF;

IF bHealth_Pos_CH1 AND bHealth_Pos_CH2 AND bHealth_Pos_CH3 THEN
    nDegradedMode_Pos := 0;
    IF (rBeamPos_CH1_mm >= rBeamPos_CH2_mm AND rBeamPos_CH1_mm <= rBeamPos_CH3_mm) OR
       (rBeamPos_CH1_mm <= rBeamPos_CH2_mm AND rBeamPos_CH1_mm >= rBeamPos_CH3_mm) THEN
        rPot_VotedBeamPos_mm := rBeamPos_CH1_mm;
    ELSIF (rBeamPos_CH2_mm >= rBeamPos_CH1_mm AND rBeamPos_CH2_mm <= rBeamPos_CH3_mm) OR
          (rBeamPos_CH2_mm <= rBeamPos_CH1_mm AND rBeamPos_CH2_mm >= rBeamPos_CH3_mm) THEN
        rPot_VotedBeamPos_mm := rBeamPos_CH2_mm;
    ELSE
        rPot_VotedBeamPos_mm := rBeamPos_CH3_mm;
    END_IF;
ELSIF bHealth_Pos_CH1 AND bHealth_Pos_CH2 AND NOT bHealth_Pos_CH3 THEN
    nDegradedMode_Pos := 1;
    rPot_VotedBeamPos_mm := (rBeamPos_CH1_mm + rBeamPos_CH2_mm) * 0.50;
ELSIF bHealth_Pos_CH1 AND NOT bHealth_Pos_CH2 AND bHealth_Pos_CH3 THEN
    nDegradedMode_Pos := 1;
    rPot_VotedBeamPos_mm := (rBeamPos_CH1_mm + rBeamPos_CH3_mm) * 0.50;
ELSIF NOT bHealth_Pos_CH1 AND bHealth_Pos_CH2 AND bHealth_Pos_CH3 THEN
    nDegradedMode_Pos := 1;
    rPot_VotedBeamPos_mm := (rBeamPos_CH2_mm + rBeamPos_CH3_mm) * 0.50;
ELSIF bHealth_Pos_CH1 THEN
    nDegradedMode_Pos := 2;
    rPot_VotedBeamPos_mm := rBeamPos_CH1_mm;
ELSIF bHealth_Pos_CH2 THEN
    nDegradedMode_Pos := 2;
    rPot_VotedBeamPos_mm := rBeamPos_CH2_mm;
ELSIF bHealth_Pos_CH3 THEN
    nDegradedMode_Pos := 2;
    rPot_VotedBeamPos_mm := rBeamPos_CH3_mm;
ELSE
    nDegradedMode_Pos := 3;
    IF rPot_VotedBeamPos_mm < 0.0 OR rPot_VotedBeamPos_mm > 500.0 THEN
        rPot_VotedBeamPos_mm := 150.0; (* Fallback nominal mid-stroke elevation *)
    END_IF;
END_IF;
'''
