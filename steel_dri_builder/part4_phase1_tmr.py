# steel_dri_builder/part4_phase1_tmr.py
"""
Part 4: Phase 1 - 2oo3 Triple Modular Redundancy (TMR) Sensor Voting Suite with Discrepancy Timers
"""

def get_phase1_tmr():
    return """(* ==================================================================================================== *)
(* PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING SUITE WITH DISCREPANCY TIMERS           *)
(* ==================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------- *)
(* 1.1 TMR CHANNEL 1: BUSTLE PIPE REDUCTION GAS TEMPERATURE (TT_BUSTLE_101A/B/C) [deg C]                *)
(* ---------------------------------------------------------------------------------------------------- *)
(* Plausibility & Raw Health Pre-Screening (Range: 400.0 to 1250.0 deg C) *)
bTMR_Bustle_FaultA := (NOT bTT_Bustle_101A_Valid) OR (rTT_Bustle_101A < 400.0) OR (rTT_Bustle_101A > 1250.0);
bTMR_Bustle_FaultB := (NOT bTT_Bustle_101B_Valid) OR (rTT_Bustle_101B < 400.0) OR (rTT_Bustle_101B > 1250.0);
bTMR_Bustle_FaultC := (NOT bTT_Bustle_101C_Valid) OR (rTT_Bustle_101C < 400.0) OR (rTT_Bustle_101C > 1250.0);

(* Pairwise Deviation Evaluation *)
rTMR_Bustle_DevAB := ABS(rTT_Bustle_101A - rTT_Bustle_101B);
rTMR_Bustle_DevBC := ABS(rTT_Bustle_101B - rTT_Bustle_101C);
rTMR_Bustle_DevAC := ABS(rTT_Bustle_101A - rTT_Bustle_101C);

(* Discrepancy Integration Timers (Threshold: tTmrDiscrepancyLimit = 250 ms) *)
IF (NOT bTMR_Bustle_FaultA) AND (NOT bTMR_Bustle_FaultB) AND (rTMR_Bustle_DevAB > rTMR_Tol_BustleTemp) THEN
    tTMR_Bustle_TimerAB := tTMR_Bustle_TimerAB + tSampleTime;
    IF tTMR_Bustle_TimerAB >= tTmrDiscrepancyLimit THEN
        bTMR_Bustle_DiscAB := TRUE;
    END_IF;
ELSE
    tTMR_Bustle_TimerAB := T#0ms;
    bTMR_Bustle_DiscAB := FALSE;
END_IF;

IF (NOT bTMR_Bustle_FaultB) AND (NOT bTMR_Bustle_FaultC) AND (rTMR_Bustle_DevBC > rTMR_Tol_BustleTemp) THEN
    tTMR_Bustle_TimerBC := tTMR_Bustle_TimerBC + tSampleTime;
    IF tTMR_Bustle_TimerBC >= tTmrDiscrepancyLimit THEN
        bTMR_Bustle_DiscBC := TRUE;
    END_IF;
ELSE
    tTMR_Bustle_TimerBC := T#0ms;
    bTMR_Bustle_DiscBC := FALSE;
END_IF;

IF (NOT bTMR_Bustle_FaultA) AND (NOT bTMR_Bustle_FaultC) AND (rTMR_Bustle_DevAC > rTMR_Tol_BustleTemp) THEN
    tTMR_Bustle_TimerAC := tTMR_Bustle_TimerAC + tSampleTime;
    IF tTMR_Bustle_TimerAC >= tTmrDiscrepancyLimit THEN
        bTMR_Bustle_DiscAC := TRUE;
    END_IF;
ELSE
    tTMR_Bustle_TimerAC := T#0ms;
    bTMR_Bustle_DiscAC := FALSE;
END_IF;

(* Identify and Isolate Outlier Sensor Under 3 Healthy Channel Conditions *)
IF (NOT bTMR_Bustle_FaultA) AND (NOT bTMR_Bustle_FaultB) AND (NOT bTMR_Bustle_FaultC) THEN
    IF bTMR_Bustle_DiscAB AND bTMR_Bustle_DiscAC AND (NOT bTMR_Bustle_DiscBC) THEN
        bTMR_Bustle_FaultA := TRUE; (* Sensor A is diverging from B and C *)
    ELSIF bTMR_Bustle_DiscAB AND bTMR_Bustle_DiscBC AND (NOT bTMR_Bustle_DiscAC) THEN
        bTMR_Bustle_FaultB := TRUE; (* Sensor B is diverging from A and C *)
    ELSIF bTMR_Bustle_DiscAC AND bTMR_Bustle_DiscBC AND (NOT bTMR_Bustle_DiscAB) THEN
        bTMR_Bustle_FaultC := TRUE; (* Sensor C is diverging from A and B *)
    END_IF;
END_IF;

(* 2oo3 Voting & Fault-Tolerant Synthesis *)
IF (NOT bTMR_Bustle_FaultA) AND (NOT bTMR_Bustle_FaultB) AND (NOT bTMR_Bustle_FaultC) THEN
    (* 3-Way Median Select *)
    IF (rTT_Bustle_101A >= rTT_Bustle_101B AND rTT_Bustle_101A <= rTT_Bustle_101C) OR (rTT_Bustle_101A >= rTT_Bustle_101C AND rTT_Bustle_101A <= rTT_Bustle_101B) THEN
        rPV_BustleTemp_Voted := rTT_Bustle_101A;
    ELSIF (rTT_Bustle_101B >= rTT_Bustle_101A AND rTT_Bustle_101B <= rTT_Bustle_101C) OR (rTT_Bustle_101B >= rTT_Bustle_101C AND rTT_Bustle_101B <= rTT_Bustle_101A) THEN
        rPV_BustleTemp_Voted := rTT_Bustle_101B;
    ELSE
        rPV_BustleTemp_Voted := rTT_Bustle_101C;
    END_IF;
    bTMR_Bustle_Degraded := FALSE;
    bTMR_Bustle_Critical := FALSE;
ELSIF (NOT bTMR_Bustle_FaultA) AND (NOT bTMR_Bustle_FaultB) THEN
    (* Degraded 1oo2: A & B Average *)
    rPV_BustleTemp_Voted := (rTT_Bustle_101A + rTT_Bustle_101B) * 0.5;
    bTMR_Bustle_Degraded := TRUE;
    bTMR_Bustle_Critical := FALSE;
ELSIF (NOT bTMR_Bustle_FaultB) AND (NOT bTMR_Bustle_FaultC) THEN
    (* Degraded 1oo2: B & C Average *)
    rPV_BustleTemp_Voted := (rTT_Bustle_101B + rTT_Bustle_101C) * 0.5;
    bTMR_Bustle_Degraded := TRUE;
    bTMR_Bustle_Critical := FALSE;
ELSIF (NOT bTMR_Bustle_FaultA) AND (NOT bTMR_Bustle_FaultC) THEN
    (* Degraded 1oo2: A & C Average *)
    rPV_BustleTemp_Voted := (rTT_Bustle_101A + rTT_Bustle_101C) * 0.5;
    bTMR_Bustle_Degraded := TRUE;
    bTMR_Bustle_Critical := FALSE;
ELSIF (NOT bTMR_Bustle_FaultA) THEN
    rPV_BustleTemp_Voted := rTT_Bustle_101A;
    bTMR_Bustle_Degraded := TRUE;
    bTMR_Bustle_Critical := FALSE;
ELSIF (NOT bTMR_Bustle_FaultB) THEN
    rPV_BustleTemp_Voted := rTT_Bustle_101B;
    bTMR_Bustle_Degraded := TRUE;
    bTMR_Bustle_Critical := FALSE;
ELSIF (NOT bTMR_Bustle_FaultC) THEN
    rPV_BustleTemp_Voted := rTT_Bustle_101C;
    bTMR_Bustle_Degraded := TRUE;
    bTMR_Bustle_Critical := FALSE;
ELSE
    (* Total Sensor Array Loss: Bumpless Hold *)
    rPV_BustleTemp_Voted := rTMR_Bustle_LastGood;
    bTMR_Bustle_Degraded := TRUE;
    bTMR_Bustle_Critical := TRUE;
END_IF;
rTMR_Bustle_LastGood := rPV_BustleTemp_Voted;


(* ---------------------------------------------------------------------------------------------------- *)
(* 1.2 TMR CHANNEL 2: SHAFT DIFFERENTIAL PRESSURE TRANSMITTERS (PDT_SHAFT_201A/B/C) [kPa]              *)
(* ---------------------------------------------------------------------------------------------------- *)
(* Plausibility & Raw Health Pre-Screening (Range: 5.0 to 120.0 kPa) *)
bTMR_ShaftDP_FaultA := (NOT bPDT_Shaft_201A_Valid) OR (rPDT_Shaft_201A < 5.0) OR (rPDT_Shaft_201A > 120.0);
bTMR_ShaftDP_FaultB := (NOT bPDT_Shaft_201B_Valid) OR (rPDT_Shaft_201B < 5.0) OR (rPDT_Shaft_201B > 120.0);
bTMR_ShaftDP_FaultC := (NOT bPDT_Shaft_201C_Valid) OR (rPDT_Shaft_201C < 5.0) OR (rPDT_Shaft_201C > 120.0);

(* Pairwise Deviation Evaluation *)
rTMR_ShaftDP_DevAB := ABS(rPDT_Shaft_201A - rPDT_Shaft_201B);
rTMR_ShaftDP_DevBC := ABS(rPDT_Shaft_201B - rPDT_Shaft_201C);
rTMR_ShaftDP_DevAC := ABS(rPDT_Shaft_201A - rPDT_Shaft_201C);

(* Discrepancy Integration Timers *)
IF (NOT bTMR_ShaftDP_FaultA) AND (NOT bTMR_ShaftDP_FaultB) AND (rTMR_ShaftDP_DevAB > rTMR_Tol_ShaftDP) THEN
    tTMR_ShaftDP_TimerAB := tTMR_ShaftDP_TimerAB + tSampleTime;
    IF tTMR_ShaftDP_TimerAB >= tTmrDiscrepancyLimit THEN
        bTMR_ShaftDP_DiscAB := TRUE;
    END_IF;
ELSE
    tTMR_ShaftDP_TimerAB := T#0ms;
    bTMR_ShaftDP_DiscAB := FALSE;
END_IF;

IF (NOT bTMR_ShaftDP_FaultB) AND (NOT bTMR_ShaftDP_FaultC) AND (rTMR_ShaftDP_DevBC > rTMR_Tol_ShaftDP) THEN
    tTMR_ShaftDP_TimerBC := tTMR_ShaftDP_TimerBC + tSampleTime;
    IF tTMR_ShaftDP_TimerBC >= tTmrDiscrepancyLimit THEN
        bTMR_ShaftDP_DiscBC := TRUE;
    END_IF;
ELSE
    tTMR_ShaftDP_TimerBC := T#0ms;
    bTMR_ShaftDP_DiscBC := FALSE;
END_IF;

IF (NOT bTMR_ShaftDP_FaultA) AND (NOT bTMR_ShaftDP_FaultC) AND (rTMR_ShaftDP_DevAC > rTMR_Tol_ShaftDP) THEN
    tTMR_ShaftDP_TimerAC := tTMR_ShaftDP_TimerAC + tSampleTime;
    IF tTMR_ShaftDP_TimerAC >= tTmrDiscrepancyLimit THEN
        bTMR_ShaftDP_DiscAC := TRUE;
    END_IF;
ELSE
    tTMR_ShaftDP_TimerAC := T#0ms;
    bTMR_ShaftDP_DiscAC := FALSE;
END_IF;

(* Identify and Isolate Outlier Sensor *)
IF (NOT bTMR_ShaftDP_FaultA) AND (NOT bTMR_ShaftDP_FaultB) AND (NOT bTMR_ShaftDP_FaultC) THEN
    IF bTMR_ShaftDP_DiscAB AND bTMR_ShaftDP_DiscAC AND (NOT bTMR_ShaftDP_DiscBC) THEN
        bTMR_ShaftDP_FaultA := TRUE;
    ELSIF bTMR_ShaftDP_DiscAB AND bTMR_ShaftDP_DiscBC AND (NOT bTMR_ShaftDP_DiscAC) THEN
        bTMR_ShaftDP_FaultB := TRUE;
    ELSIF bTMR_ShaftDP_DiscAC AND bTMR_ShaftDP_DiscBC AND (NOT bTMR_ShaftDP_DiscAB) THEN
        bTMR_ShaftDP_FaultC := TRUE;
    END_IF;
END_IF;

(* 2oo3 Voting & Fault-Tolerant Synthesis *)
IF (NOT bTMR_ShaftDP_FaultA) AND (NOT bTMR_ShaftDP_FaultB) AND (NOT bTMR_ShaftDP_FaultC) THEN
    IF (rPDT_Shaft_201A >= rPDT_Shaft_201B AND rPDT_Shaft_201A <= rPDT_Shaft_201C) OR (rPDT_Shaft_201A >= rPDT_Shaft_201C AND rPDT_Shaft_201A <= rPDT_Shaft_201B) THEN
        rPV_ShaftDP_Voted := rPDT_Shaft_201A;
    ELSIF (rPDT_Shaft_201B >= rPDT_Shaft_201A AND rPDT_Shaft_201B <= rPDT_Shaft_201C) OR (rPDT_Shaft_201B >= rPDT_Shaft_201C AND rPDT_Shaft_201B <= rPDT_Shaft_201A) THEN
        rPV_ShaftDP_Voted := rPDT_Shaft_201B;
    ELSE
        rPV_ShaftDP_Voted := rPDT_Shaft_201C;
    END_IF;
    bTMR_ShaftDP_Degraded := FALSE;
    bTMR_ShaftDP_Critical := FALSE;
ELSIF (NOT bTMR_ShaftDP_FaultA) AND (NOT bTMR_ShaftDP_FaultB) THEN
    rPV_ShaftDP_Voted := (rPDT_Shaft_201A + rPDT_Shaft_201B) * 0.5;
    bTMR_ShaftDP_Degraded := TRUE;
    bTMR_ShaftDP_Critical := FALSE;
ELSIF (NOT bTMR_ShaftDP_FaultB) AND (NOT bTMR_ShaftDP_FaultC) THEN
    rPV_ShaftDP_Voted := (rPDT_Shaft_201B + rPDT_Shaft_201C) * 0.5;
    bTMR_ShaftDP_Degraded := TRUE;
    bTMR_ShaftDP_Critical := FALSE;
ELSIF (NOT bTMR_ShaftDP_FaultA) AND (NOT bTMR_ShaftDP_FaultC) THEN
    rPV_ShaftDP_Voted := (rPDT_Shaft_201A + rPDT_Shaft_201C) * 0.5;
    bTMR_ShaftDP_Degraded := TRUE;
    bTMR_ShaftDP_Critical := FALSE;
ELSIF (NOT bTMR_ShaftDP_FaultA) THEN
    rPV_ShaftDP_Voted := rPDT_Shaft_201A;
    bTMR_ShaftDP_Degraded := TRUE;
    bTMR_ShaftDP_Critical := FALSE;
ELSIF (NOT bTMR_ShaftDP_FaultB) THEN
    rPV_ShaftDP_Voted := rPDT_Shaft_201B;
    bTMR_ShaftDP_Degraded := TRUE;
    bTMR_ShaftDP_Critical := FALSE;
ELSIF (NOT bTMR_ShaftDP_FaultC) THEN
    rPV_ShaftDP_Voted := rPDT_Shaft_201C;
    bTMR_ShaftDP_Degraded := TRUE;
    bTMR_ShaftDP_Critical := FALSE;
ELSE
    rPV_ShaftDP_Voted := rTMR_ShaftDP_LastGood;
    bTMR_ShaftDP_Degraded := TRUE;
    bTMR_ShaftDP_Critical := TRUE;
END_IF;
rTMR_ShaftDP_LastGood := rPV_ShaftDP_Voted;


(* ---------------------------------------------------------------------------------------------------- *)
(* 1.3 TMR CHANNEL 3: IN-LINE SPECTROMETRIC H2/CO RATIO ANALYZERS (AT_GAS_301A/B/C) [ratio]             *)
(* ---------------------------------------------------------------------------------------------------- *)
(* Plausibility & Raw Health Pre-Screening (Range: 0.5 to 8.0 ratio) *)
bTMR_GasH2CO_FaultA := (NOT bAT_Gas_301A_Valid) OR (rAT_Gas_301A_H2CO < 0.50) OR (rAT_Gas_301A_H2CO > 8.00);
bTMR_GasH2CO_FaultB := (NOT bAT_Gas_301B_Valid) OR (rAT_Gas_301B_H2CO < 0.50) OR (rAT_Gas_301B_H2CO > 8.00);
bTMR_GasH2CO_FaultC := (NOT bAT_Gas_301C_Valid) OR (rAT_Gas_301C_H2CO < 0.50) OR (rAT_Gas_301C_H2CO > 8.00);

(* Pairwise Deviation Evaluation *)
rTMR_GasH2CO_DevAB := ABS(rAT_Gas_301A_H2CO - rAT_Gas_301B_H2CO);
rTMR_GasH2CO_DevBC := ABS(rAT_Gas_301B_H2CO - rAT_Gas_301C_H2CO);
rTMR_GasH2CO_DevAC := ABS(rAT_Gas_301A_H2CO - rAT_Gas_301C_H2CO);

(* Discrepancy Integration Timers *)
IF (NOT bTMR_GasH2CO_FaultA) AND (NOT bTMR_GasH2CO_FaultB) AND (rTMR_GasH2CO_DevAB > rTMR_Tol_GasH2CO) THEN
    tTMR_GasH2CO_TimerAB := tTMR_GasH2CO_TimerAB + tSampleTime;
    IF tTMR_GasH2CO_TimerAB >= tTmrDiscrepancyLimit THEN
        bTMR_GasH2CO_DiscAB := TRUE;
    END_IF;
ELSE
    tTMR_GasH2CO_TimerAB := T#0ms;
    bTMR_GasH2CO_DiscAB := FALSE;
END_IF;

IF (NOT bTMR_GasH2CO_FaultB) AND (NOT bTMR_GasH2CO_FaultC) AND (rTMR_GasH2CO_DevBC > rTMR_Tol_GasH2CO) THEN
    tTMR_GasH2CO_TimerBC := tTMR_GasH2CO_TimerBC + tSampleTime;
    IF tTMR_GasH2CO_TimerBC >= tTmrDiscrepancyLimit THEN
        bTMR_GasH2CO_DiscBC := TRUE;
    END_IF;
ELSE
    tTMR_GasH2CO_TimerBC := T#0ms;
    bTMR_GasH2CO_DiscBC := FALSE;
END_IF;

IF (NOT bTMR_GasH2CO_FaultA) AND (NOT bTMR_GasH2CO_FaultC) AND (rTMR_GasH2CO_DevAC > rTMR_Tol_GasH2CO) THEN
    tTMR_GasH2CO_TimerAC := tTMR_GasH2CO_TimerAC + tSampleTime;
    IF tTMR_GasH2CO_TimerAC >= tTmrDiscrepancyLimit THEN
        bTMR_GasH2CO_DiscAC := TRUE;
    END_IF;
ELSE
    tTMR_GasH2CO_TimerAC := T#0ms;
    bTMR_GasH2CO_DiscAC := FALSE;
END_IF;

(* Identify and Isolate Outlier Sensor *)
IF (NOT bTMR_GasH2CO_FaultA) AND (NOT bTMR_GasH2CO_FaultB) AND (NOT bTMR_GasH2CO_FaultC) THEN
    IF bTMR_GasH2CO_DiscAB AND bTMR_GasH2CO_DiscAC AND (NOT bTMR_GasH2CO_DiscBC) THEN
        bTMR_GasH2CO_FaultA := TRUE;
    ELSIF bTMR_GasH2CO_DiscAB AND bTMR_GasH2CO_DiscBC AND (NOT bTMR_GasH2CO_DiscAC) THEN
        bTMR_GasH2CO_FaultB := TRUE;
    ELSIF bTMR_GasH2CO_DiscAC AND bTMR_GasH2CO_DiscBC AND (NOT bTMR_GasH2CO_DiscAB) THEN
        bTMR_GasH2CO_FaultC := TRUE;
    END_IF;
END_IF;

(* 2oo3 Voting & Fault-Tolerant Synthesis *)
IF (NOT bTMR_GasH2CO_FaultA) AND (NOT bTMR_GasH2CO_FaultB) AND (NOT bTMR_GasH2CO_FaultC) THEN
    IF (rAT_Gas_301A_H2CO >= rAT_Gas_301B_H2CO AND rAT_Gas_301A_H2CO <= rAT_Gas_301C_H2CO) OR (rAT_Gas_301A_H2CO >= rAT_Gas_301C_H2CO AND rAT_Gas_301A_H2CO <= rAT_Gas_301B_H2CO) THEN
        rPV_TopGasH2CO_Voted := rAT_Gas_301A_H2CO;
    ELSIF (rAT_Gas_301B_H2CO >= rAT_Gas_301A_H2CO AND rAT_Gas_301B_H2CO <= rAT_Gas_301C_H2CO) OR (rAT_Gas_301B_H2CO >= rAT_Gas_301C_H2CO AND rAT_Gas_301B_H2CO <= rAT_Gas_301A_H2CO) THEN
        rPV_TopGasH2CO_Voted := rAT_Gas_301B_H2CO;
    ELSE
        rPV_TopGasH2CO_Voted := rAT_Gas_301C_H2CO;
    END_IF;
    bTMR_GasH2CO_Degraded := FALSE;
    bTMR_GasH2CO_Critical := FALSE;
ELSIF (NOT bTMR_GasH2CO_FaultA) AND (NOT bTMR_GasH2CO_FaultB) THEN
    rPV_TopGasH2CO_Voted := (rAT_Gas_301A_H2CO + rAT_Gas_301B_H2CO) * 0.5;
    bTMR_GasH2CO_Degraded := TRUE;
    bTMR_GasH2CO_Critical := FALSE;
ELSIF (NOT bTMR_GasH2CO_FaultB) AND (NOT bTMR_GasH2CO_FaultC) THEN
    rPV_TopGasH2CO_Voted := (rAT_Gas_301B_H2CO + rAT_Gas_301C_H2CO) * 0.5;
    bTMR_GasH2CO_Degraded := TRUE;
    bTMR_GasH2CO_Critical := FALSE;
ELSIF (NOT bTMR_GasH2CO_FaultA) AND (NOT bTMR_GasH2CO_FaultC) THEN
    rPV_TopGasH2CO_Voted := (rAT_Gas_301A_H2CO + rAT_Gas_301C_H2CO) * 0.5;
    bTMR_GasH2CO_Degraded := TRUE;
    bTMR_GasH2CO_Critical := FALSE;
ELSIF (NOT bTMR_GasH2CO_FaultA) THEN
    rPV_TopGasH2CO_Voted := rAT_Gas_301A_H2CO;
    bTMR_GasH2CO_Degraded := TRUE;
    bTMR_GasH2CO_Critical := FALSE;
ELSIF (NOT bTMR_GasH2CO_FaultB) THEN
    rPV_TopGasH2CO_Voted := rAT_Gas_301B_H2CO;
    bTMR_GasH2CO_Degraded := TRUE;
    bTMR_GasH2CO_Critical := FALSE;
ELSIF (NOT bTMR_GasH2CO_FaultC) THEN
    rPV_TopGasH2CO_Voted := rAT_Gas_301C_H2CO;
    bTMR_GasH2CO_Degraded := TRUE;
    bTMR_GasH2CO_Critical := FALSE;
ELSE
    rPV_TopGasH2CO_Voted := rTMR_GasH2CO_LastGood;
    bTMR_GasH2CO_Degraded := TRUE;
    bTMR_GasH2CO_Critical := TRUE;
END_IF;
rTMR_GasH2CO_LastGood := rPV_TopGasH2CO_Voted;


(* ---------------------------------------------------------------------------------------------------- *)
(* 1.4 TMR CHANNEL 4: TOP GAS CO2 ABSORPTION CONCENTRATION (AT_GAS_302A/B/C) [% vol]                    *)
(* ---------------------------------------------------------------------------------------------------- *)
(* Plausibility & Raw Health Pre-Screening (Range: 1.0 to 35.0 % vol) *)
bTMR_GasCO2_FaultA := (NOT bAT_Gas_302A_Valid) OR (rAT_Gas_302A_CO2 < 1.0) OR (rAT_Gas_302A_CO2 > 35.0);
bTMR_GasCO2_FaultB := (NOT bAT_Gas_302B_Valid) OR (rAT_Gas_302B_CO2 < 1.0) OR (rAT_Gas_302B_CO2 > 35.0);
bTMR_GasCO2_FaultC := (NOT bAT_Gas_302C_Valid) OR (rAT_Gas_302C_CO2 < 1.0) OR (rAT_Gas_302C_CO2 > 35.0);

(* Pairwise Deviation Evaluation *)
rTMR_GasCO2_DevAB := ABS(rAT_Gas_302A_CO2 - rAT_Gas_302B_CO2);
rTMR_GasCO2_DevBC := ABS(rAT_Gas_302B_CO2 - rAT_Gas_302C_CO2);
rTMR_GasCO2_DevAC := ABS(rAT_Gas_302A_CO2 - rAT_Gas_302C_CO2);

(* Discrepancy Integration Timers *)
IF (NOT bTMR_GasCO2_FaultA) AND (NOT bTMR_GasCO2_FaultB) AND (rTMR_GasCO2_DevAB > rTMR_Tol_GasCO2) THEN
    tTMR_GasCO2_TimerAB := tTMR_GasCO2_TimerAB + tSampleTime;
    IF tTMR_GasCO2_TimerAB >= tTmrDiscrepancyLimit THEN
        bTMR_GasCO2_DiscAB := TRUE;
    END_IF;
ELSE
    tTMR_GasCO2_TimerAB := T#0ms;
    bTMR_GasCO2_DiscAB := FALSE;
END_IF;

IF (NOT bTMR_GasCO2_FaultB) AND (NOT bTMR_GasCO2_FaultC) AND (rTMR_GasCO2_DevBC > rTMR_Tol_GasCO2) THEN
    tTMR_GasCO2_TimerBC := tTMR_GasCO2_TimerBC + tSampleTime;
    IF tTMR_GasCO2_TimerBC >= tTmrDiscrepancyLimit THEN
        bTMR_GasCO2_DiscBC := TRUE;
    END_IF;
ELSE
    tTMR_GasCO2_TimerBC := T#0ms;
    bTMR_GasCO2_DiscBC := FALSE;
END_IF;

IF (NOT bTMR_GasCO2_FaultA) AND (NOT bTMR_GasCO2_FaultC) AND (rTMR_GasCO2_DevAC > rTMR_Tol_GasCO2) THEN
    tTMR_GasCO2_TimerAC := tTMR_GasCO2_TimerAC + tSampleTime;
    IF tTMR_GasCO2_TimerAC >= tTmrDiscrepancyLimit THEN
        bTMR_GasCO2_DiscAC := TRUE;
    END_IF;
ELSE
    tTMR_GasCO2_TimerAC := T#0ms;
    bTMR_GasCO2_DiscAC := FALSE;
END_IF;

(* Identify and Isolate Outlier Sensor *)
IF (NOT bTMR_GasCO2_FaultA) AND (NOT bTMR_GasCO2_FaultB) AND (NOT bTMR_GasCO2_FaultC) THEN
    IF bTMR_GasCO2_DiscAB AND bTMR_GasCO2_DiscAC AND (NOT bTMR_GasCO2_DiscBC) THEN
        bTMR_GasCO2_FaultA := TRUE;
    ELSIF bTMR_GasCO2_DiscAB AND bTMR_GasCO2_DiscBC AND (NOT bTMR_GasCO2_DiscAC) THEN
        bTMR_GasCO2_FaultB := TRUE;
    ELSIF bTMR_GasCO2_DiscAC AND bTMR_GasCO2_DiscBC AND (NOT bTMR_GasCO2_DiscAB) THEN
        bTMR_GasCO2_FaultC := TRUE;
    END_IF;
END_IF;

(* 2oo3 Voting & Fault-Tolerant Synthesis *)
IF (NOT bTMR_GasCO2_FaultA) AND (NOT bTMR_GasCO2_FaultB) AND (NOT bTMR_GasCO2_FaultC) THEN
    IF (rAT_Gas_302A_CO2 >= rAT_Gas_302B_CO2 AND rAT_Gas_302A_CO2 <= rAT_Gas_302C_CO2) OR (rAT_Gas_302A_CO2 >= rAT_Gas_302C_CO2 AND rAT_Gas_302A_CO2 <= rAT_Gas_302B_CO2) THEN
        rPV_TopGasCO2_Voted := rAT_Gas_302A_CO2;
    ELSIF (rAT_Gas_302B_CO2 >= rAT_Gas_302A_CO2 AND rAT_Gas_302B_CO2 <= rAT_Gas_302C_CO2) OR (rAT_Gas_302B_CO2 >= rAT_Gas_302C_CO2 AND rAT_Gas_302B_CO2 <= rAT_Gas_302A_CO2) THEN
        rPV_TopGasCO2_Voted := rAT_Gas_302B_CO2;
    ELSE
        rPV_TopGasCO2_Voted := rAT_Gas_302C_CO2;
    END_IF;
    bTMR_GasCO2_Degraded := FALSE;
    bTMR_GasCO2_Critical := FALSE;
ELSIF (NOT bTMR_GasCO2_FaultA) AND (NOT bTMR_GasCO2_FaultB) THEN
    rPV_TopGasCO2_Voted := (rAT_Gas_302A_CO2 + rAT_Gas_302B_CO2) * 0.5;
    bTMR_GasCO2_Degraded := TRUE;
    bTMR_GasCO2_Critical := FALSE;
ELSIF (NOT bTMR_GasCO2_FaultB) AND (NOT bTMR_GasCO2_FaultC) THEN
    rPV_TopGasCO2_Voted := (rAT_Gas_302B_CO2 + rAT_Gas_302C_CO2) * 0.5;
    bTMR_GasCO2_Degraded := TRUE;
    bTMR_GasCO2_Critical := FALSE;
ELSIF (NOT bTMR_GasCO2_FaultA) AND (NOT bTMR_GasCO2_FaultC) THEN
    rPV_TopGasCO2_Voted := (rAT_Gas_302A_CO2 + rAT_Gas_302C_CO2) * 0.5;
    bTMR_GasCO2_Degraded := TRUE;
    bTMR_GasCO2_Critical := FALSE;
ELSIF (NOT bTMR_GasCO2_FaultA) THEN
    rPV_TopGasCO2_Voted := rAT_Gas_302A_CO2;
    bTMR_GasCO2_Degraded := TRUE;
    bTMR_GasCO2_Critical := FALSE;
ELSIF (NOT bTMR_GasCO2_FaultB) THEN
    rPV_TopGasCO2_Voted := rAT_Gas_302B_CO2;
    bTMR_GasCO2_Degraded := TRUE;
    bTMR_GasCO2_Critical := FALSE;
ELSIF (NOT bTMR_GasCO2_FaultC) THEN
    rPV_TopGasCO2_Voted := rAT_Gas_302C_CO2;
    bTMR_GasCO2_Degraded := TRUE;
    bTMR_GasCO2_Critical := FALSE;
ELSE
    rPV_TopGasCO2_Voted := rTMR_GasCO2_LastGood;
    bTMR_GasCO2_Degraded := TRUE;
    bTMR_GasCO2_Critical := TRUE;
END_IF;
rTMR_GasCO2_LastGood := rPV_TopGasCO2_Voted;


(* ---------------------------------------------------------------------------------------------------- *)
(* 1.5 TMR CHANNEL 5: SHAFT TOP BURDEN SURFACE LEVEL RADAR PROFILERS (LT_BURDEN_401A/B/C) [m]          *)
(* ---------------------------------------------------------------------------------------------------- *)
(* Plausibility & Raw Health Pre-Screening (Range: 5.0 to 25.0 m) *)
bTMR_Burden_FaultA := (NOT bLT_Burden_401A_Valid) OR (rLT_Burden_401A < 5.0) OR (rLT_Burden_401A > 25.0);
bTMR_Burden_FaultB := (NOT bLT_Burden_401B_Valid) OR (rLT_Burden_401B < 5.0) OR (rLT_Burden_401B > 25.0);
bTMR_Burden_FaultC := (NOT bLT_Burden_401C_Valid) OR (rLT_Burden_401C < 5.0) OR (rLT_Burden_401C > 25.0);

(* Pairwise Deviation Evaluation *)
rTMR_Burden_DevAB := ABS(rLT_Burden_401A - rLT_Burden_401B);
rTMR_Burden_DevBC := ABS(rLT_Burden_401B - rLT_Burden_401C);
rTMR_Burden_DevAC := ABS(rLT_Burden_401A - rLT_Burden_401C);

(* Discrepancy Integration Timers *)
IF (NOT bTMR_Burden_FaultA) AND (NOT bTMR_Burden_FaultB) AND (rTMR_Burden_DevAB > rTMR_Tol_BurdenLevel) THEN
    tTMR_Burden_TimerAB := tTMR_Burden_TimerAB + tSampleTime;
    IF tTMR_Burden_TimerAB >= tTmrDiscrepancyLimit THEN
        bTMR_Burden_DiscAB := TRUE;
    END_IF;
ELSE
    tTMR_Burden_TimerAB := T#0ms;
    bTMR_Burden_DiscAB := FALSE;
END_IF;

IF (NOT bTMR_Burden_FaultB) AND (NOT bTMR_Burden_FaultC) AND (rTMR_Burden_DevBC > rTMR_Tol_BurdenLevel) THEN
    tTMR_Burden_TimerBC := tTMR_Burden_TimerBC + tSampleTime;
    IF tTMR_Burden_TimerBC >= tTmrDiscrepancyLimit THEN
        bTMR_Burden_DiscBC := TRUE;
    END_IF;
ELSE
    tTMR_Burden_TimerBC := T#0ms;
    bTMR_Burden_DiscBC := FALSE;
END_IF;

IF (NOT bTMR_Burden_FaultA) AND (NOT bTMR_Burden_FaultC) AND (rTMR_Burden_DevAC > rTMR_Tol_BurdenLevel) THEN
    tTMR_Burden_TimerAC := tTMR_Burden_TimerAC + tSampleTime;
    IF tTMR_Burden_TimerAC >= tTmrDiscrepancyLimit THEN
        bTMR_Burden_DiscAC := TRUE;
    END_IF;
ELSE
    tTMR_Burden_TimerAC := T#0ms;
    bTMR_Burden_DiscAC := FALSE;
END_IF;

(* Identify and Isolate Outlier Sensor *)
IF (NOT bTMR_Burden_FaultA) AND (NOT bTMR_Burden_FaultB) AND (NOT bTMR_Burden_FaultC) THEN
    IF bTMR_Burden_DiscAB AND bTMR_Burden_DiscAC AND (NOT bTMR_Burden_DiscBC) THEN
        bTMR_Burden_FaultA := TRUE;
    ELSIF bTMR_Burden_DiscAB AND bTMR_Burden_DiscBC AND (NOT bTMR_Burden_DiscAC) THEN
        bTMR_Burden_FaultB := TRUE;
    ELSIF bTMR_Burden_DiscAC AND bTMR_Burden_DiscBC AND (NOT bTMR_Burden_DiscAB) THEN
        bTMR_Burden_FaultC := TRUE;
    END_IF;
END_IF;

(* 2oo3 Voting & Fault-Tolerant Synthesis *)
IF (NOT bTMR_Burden_FaultA) AND (NOT bTMR_Burden_FaultB) AND (NOT bTMR_Burden_FaultC) THEN
    IF (rLT_Burden_401A >= rLT_Burden_401B AND rLT_Burden_401A <= rLT_Burden_401C) OR (rLT_Burden_401A >= rLT_Burden_401C AND rLT_Burden_401A <= rLT_Burden_401B) THEN
        rPV_BurdenLevel_Voted := rLT_Burden_401A;
    ELSIF (rLT_Burden_401B >= rLT_Burden_401A AND rLT_Burden_401B <= rLT_Burden_401C) OR (rLT_Burden_401B >= rLT_Burden_401C AND rLT_Burden_401B <= rLT_Burden_401A) THEN
        rPV_BurdenLevel_Voted := rLT_Burden_401B;
    ELSE
        rPV_BurdenLevel_Voted := rLT_Burden_401C;
    END_IF;
    bTMR_Burden_Degraded := FALSE;
    bTMR_Burden_Critical := FALSE;
ELSIF (NOT bTMR_Burden_FaultA) AND (NOT bTMR_Burden_FaultB) THEN
    rPV_BurdenLevel_Voted := (rLT_Burden_401A + rLT_Burden_401B) * 0.5;
    bTMR_Burden_Degraded := TRUE;
    bTMR_Burden_Critical := FALSE;
ELSIF (NOT bTMR_Burden_FaultB) AND (NOT bTMR_Burden_FaultC) THEN
    rPV_BurdenLevel_Voted := (rLT_Burden_401B + rLT_Burden_401C) * 0.5;
    bTMR_Burden_Degraded := TRUE;
    bTMR_Burden_Critical := FALSE;
ELSIF (NOT bTMR_Burden_FaultA) AND (NOT bTMR_Burden_FaultC) THEN
    rPV_BurdenLevel_Voted := (rLT_Burden_401A + rLT_Burden_401C) * 0.5;
    bTMR_Burden_Degraded := TRUE;
    bTMR_Burden_Critical := FALSE;
ELSIF (NOT bTMR_Burden_FaultA) THEN
    rPV_BurdenLevel_Voted := rLT_Burden_401A;
    bTMR_Burden_Degraded := TRUE;
    bTMR_Burden_Critical := FALSE;
ELSIF (NOT bTMR_Burden_FaultB) THEN
    rPV_BurdenLevel_Voted := rLT_Burden_401B;
    bTMR_Burden_Degraded := TRUE;
    bTMR_Burden_Critical := FALSE;
ELSIF (NOT bTMR_Burden_FaultC) THEN
    rPV_BurdenLevel_Voted := rLT_Burden_401C;
    bTMR_Burden_Degraded := TRUE;
    bTMR_Burden_Critical := FALSE;
ELSE
    rPV_BurdenLevel_Voted := rTMR_Burden_LastGood;
    bTMR_Burden_Degraded := TRUE;
    bTMR_Burden_Critical := TRUE;
END_IF;
rTMR_Burden_LastGood := rPV_BurdenLevel_Voted;


(* ---------------------------------------------------------------------------------------------------- *)
(* 1.6 TMR CHANNEL 6: DISCHARGED HOT DRI OPTICAL PYROMETERS (TT_DRI_501A/B/C) [deg C]                   *)
(* ---------------------------------------------------------------------------------------------------- *)
(* Plausibility & Raw Health Pre-Screening (Range: 200.0 to 1100.0 deg C) *)
bTMR_DRITemp_FaultA := (NOT bTT_DRI_501A_Valid) OR (rTT_DRI_501A < 200.0) OR (rTT_DRI_501A > 1100.0);
bTMR_DRITemp_FaultB := (NOT bTT_DRI_501B_Valid) OR (rTT_DRI_501B < 200.0) OR (rTT_DRI_501B > 1100.0);
bTMR_DRITemp_FaultC := (NOT bTT_DRI_501C_Valid) OR (rTT_DRI_501C < 200.0) OR (rTT_DRI_501C > 1100.0);

(* Pairwise Deviation Evaluation *)
rTMR_DRITemp_DevAB := ABS(rTT_DRI_501A - rTT_DRI_501B);
rTMR_DRITemp_DevBC := ABS(rTT_DRI_501B - rTT_DRI_501C);
rTMR_DRITemp_DevAC := ABS(rTT_DRI_501A - rTT_DRI_501C);

(* Discrepancy Integration Timers *)
IF (NOT bTMR_DRITemp_FaultA) AND (NOT bTMR_DRITemp_FaultB) AND (rTMR_DRITemp_DevAB > rTMR_Tol_DRITemp) THEN
    tTMR_DRITemp_TimerAB := tTMR_DRITemp_TimerAB + tSampleTime;
    IF tTMR_DRITemp_TimerAB >= tTmrDiscrepancyLimit THEN
        bTMR_DRITemp_DiscAB := TRUE;
    END_IF;
ELSE
    tTMR_DRITemp_TimerAB := T#0ms;
    bTMR_DRITemp_DiscAB := FALSE;
END_IF;

IF (NOT bTMR_DRITemp_FaultB) AND (NOT bTMR_DRITemp_FaultC) AND (rTMR_DRITemp_DevBC > rTMR_Tol_DRITemp) THEN
    tTMR_DRITemp_TimerBC := tTMR_DRITemp_TimerBC + tSampleTime;
    IF tTMR_DRITemp_TimerBC >= tTmrDiscrepancyLimit THEN
        bTMR_DRITemp_DiscBC := TRUE;
    END_IF;
ELSE
    tTMR_DRITemp_TimerBC := T#0ms;
    bTMR_DRITemp_DiscBC := FALSE;
END_IF;

IF (NOT bTMR_DRITemp_FaultA) AND (NOT bTMR_DRITemp_FaultC) AND (rTMR_DRITemp_DevAC > rTMR_Tol_DRITemp) THEN
    tTMR_DRITemp_TimerAC := tTMR_DRITemp_TimerAC + tSampleTime;
    IF tTMR_DRITemp_TimerAC >= tTmrDiscrepancyLimit THEN
        bTMR_DRITemp_DiscAC := TRUE;
    END_IF;
ELSE
    tTMR_DRITemp_TimerAC := T#0ms;
    bTMR_DRITemp_DiscAC := FALSE;
END_IF;

(* Identify and Isolate Outlier Sensor *)
IF (NOT bTMR_DRITemp_FaultA) AND (NOT bTMR_DRITemp_FaultB) AND (NOT bTMR_DRITemp_FaultC) THEN
    IF bTMR_DRITemp_DiscAB AND bTMR_DRITemp_DiscAC AND (NOT bTMR_DRITemp_DiscBC) THEN
        bTMR_DRITemp_FaultA := TRUE;
    ELSIF bTMR_DRITemp_DiscAB AND bTMR_DRITemp_DiscBC AND (NOT bTMR_DRITemp_DiscAC) THEN
        bTMR_DRITemp_FaultB := TRUE;
    ELSIF bTMR_DRITemp_DiscAC AND bTMR_DRITemp_DiscBC AND (NOT bTMR_DRITemp_DiscAB) THEN
        bTMR_DRITemp_FaultC := TRUE;
    END_IF;
END_IF;

(* 2oo3 Voting & Fault-Tolerant Synthesis *)
IF (NOT bTMR_DRITemp_FaultA) AND (NOT bTMR_DRITemp_FaultB) AND (NOT bTMR_DRITemp_FaultC) THEN
    IF (rTT_DRI_501A >= rTT_DRI_501B AND rTT_DRI_501A <= rTT_DRI_501C) OR (rTT_DRI_501A >= rTT_DRI_501C AND rTT_DRI_501A <= rTT_DRI_501B) THEN
        rPV_DRITemp_Voted := rTT_DRI_501A;
    ELSIF (rTT_DRI_501B >= rTT_DRI_501A AND rTT_DRI_501B <= rTT_DRI_501C) OR (rTT_DRI_501B >= rTT_DRI_501C AND rTT_DRI_501B <= rTT_DRI_501A) THEN
        rPV_DRITemp_Voted := rTT_DRI_501B;
    ELSE
        rPV_DRITemp_Voted := rTT_DRI_501C;
    END_IF;
    bTMR_DRITemp_Degraded := FALSE;
    bTMR_DRITemp_Critical := FALSE;
ELSIF (NOT bTMR_DRITemp_FaultA) AND (NOT bTMR_DRITemp_FaultB) THEN
    rPV_DRITemp_Voted := (rTT_DRI_501A + rTT_DRI_501B) * 0.5;
    bTMR_DRITemp_Degraded := TRUE;
    bTMR_DRITemp_Critical := FALSE;
ELSIF (NOT bTMR_DRITemp_FaultB) AND (NOT bTMR_DRITemp_FaultC) THEN
    rPV_DRITemp_Voted := (rTT_DRI_501B + rTT_DRI_501C) * 0.5;
    bTMR_DRITemp_Degraded := TRUE;
    bTMR_DRITemp_Critical := FALSE;
ELSIF (NOT bTMR_DRITemp_FaultA) AND (NOT bTMR_DRITemp_FaultC) THEN
    rPV_DRITemp_Voted := (rTT_DRI_501A + rTT_DRI_501C) * 0.5;
    bTMR_DRITemp_Degraded := TRUE;
    bTMR_DRITemp_Critical := FALSE;
ELSIF (NOT bTMR_DRITemp_FaultA) THEN
    rPV_DRITemp_Voted := rTT_DRI_501A;
    bTMR_DRITemp_Degraded := TRUE;
    bTMR_DRITemp_Critical := FALSE;
ELSIF (NOT bTMR_DRITemp_FaultB) THEN
    rPV_DRITemp_Voted := rTT_DRI_501B;
    bTMR_DRITemp_Degraded := TRUE;
    bTMR_DRITemp_Critical := FALSE;
ELSIF (NOT bTMR_DRITemp_FaultC) THEN
    rPV_DRITemp_Voted := rTT_DRI_501C;
    bTMR_DRITemp_Degraded := TRUE;
    bTMR_DRITemp_Critical := FALSE;
ELSE
    rPV_DRITemp_Voted := rTMR_DRITemp_LastGood;
    bTMR_DRITemp_Degraded := TRUE;
    bTMR_DRITemp_Critical := TRUE;
END_IF;
rTMR_DRITemp_LastGood := rPV_DRITemp_Voted;

(* Aggregate TMR Status Across All 6 Arrays *)
bTMR_DegradedAlarm := bTMR_Bustle_Degraded OR bTMR_ShaftDP_Degraded OR bTMR_GasH2CO_Degraded OR
                      bTMR_GasCO2_Degraded OR bTMR_Burden_Degraded OR bTMR_DRITemp_Degraded;

bTMR_CriticalFailureAlarm := bTMR_Bustle_Critical OR bTMR_ShaftDP_Critical OR bTMR_GasH2CO_Critical OR
                             bTMR_GasCO2_Critical OR bTMR_Burden_Critical OR bTMR_DRITemp_Critical;
"""
