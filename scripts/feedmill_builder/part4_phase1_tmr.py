# scripts/feedmill_builder/part4_phase1_tmr.py
# -*- coding: utf-8 -*-

def get_phase1_block():
    return """(* ====================================================================================================
   PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) VOTING & SENSOR HEALTH DIAGNOSTICS
   ==================================================================================================== *)

(* ----------------------------------------------------------------------------------------------------
   TRIPLET 1: CONDITIONER DISCHARGE MASH TEMPERATURE (TE101A, TE101B, TE101C) [deg C]
   Range: 0.0 deg C to 140.0 deg C, Discrepancy Limit: 4.5 deg C, Timeout: 2.50 s
   ---------------------------------------------------------------------------------------------------- *)
(* 1.1 Out-of-Range Sensor Hardware Validation *)
bTmr_CondTemp_Fault_A := (rCondTemp_TE101A_degC < 0.0) OR (rCondTemp_TE101A_degC > 140.0);
bTmr_CondTemp_Fault_B := (rCondTemp_TE101B_degC < 0.0) OR (rCondTemp_TE101B_degC > 140.0);
bTmr_CondTemp_Fault_C := (rCondTemp_TE101C_degC < 0.0) OR (rCondTemp_TE101C_degC > 140.0);

(* 1.2 Pairwise Discrepancy Evaluation *)
bTmr_CondTemp_Discrep_AB := ABS(rCondTemp_TE101A_degC - rCondTemp_TE101B_degC) > rDiscrepLimit_CondTemp_degC;
bTmr_CondTemp_Discrep_BC := ABS(rCondTemp_TE101B_degC - rCondTemp_TE101C_degC) > rDiscrepLimit_CondTemp_degC;
bTmr_CondTemp_Discrep_CA := ABS(rCondTemp_TE101C_degC - rCondTemp_TE101A_degC) > rDiscrepLimit_CondTemp_degC;

(* 1.3 Discrepancy Debounce Integration Timers *)
IF bTmr_CondTemp_Discrep_AB AND NOT bTmr_CondTemp_Fault_A AND NOT bTmr_CondTemp_Fault_B THEN
    tTmr_CondTemp_Timer_AB := tTmr_CondTemp_Timer_AB + 0.050;
ELSE
    tTmr_CondTemp_Timer_AB := MAX(0.0, tTmr_CondTemp_Timer_AB - 0.100);
END_IF;

IF bTmr_CondTemp_Discrep_BC AND NOT bTmr_CondTemp_Fault_B AND NOT bTmr_CondTemp_Fault_C THEN
    tTmr_CondTemp_Timer_BC := tTmr_CondTemp_Timer_BC + 0.050;
ELSE
    tTmr_CondTemp_Timer_BC := MAX(0.0, tTmr_CondTemp_Timer_BC - 0.100);
END_IF;

IF bTmr_CondTemp_Discrep_CA AND NOT bTmr_CondTemp_Fault_C AND NOT bTmr_CondTemp_Fault_A THEN
    tTmr_CondTemp_Timer_CA := tTmr_CondTemp_Timer_CA + 0.050;
ELSE
    tTmr_CondTemp_Timer_CA := MAX(0.0, tTmr_CondTemp_Timer_CA - 0.100);
END_IF;

(* 1.4 Persistent Divergence Fault Isolation *)
IF tTmr_CondTemp_Timer_AB > tDiscrepTimeout_s AND tTmr_CondTemp_Timer_CA > tDiscrepTimeout_s THEN
    bTmr_CondTemp_Fault_A := TRUE;  (* Sensor A is divergent from both B and C *)
END_IF;
IF tTmr_CondTemp_Timer_AB > tDiscrepTimeout_s AND tTmr_CondTemp_Timer_BC > tDiscrepTimeout_s THEN
    bTmr_CondTemp_Fault_B := TRUE;  (* Sensor B is divergent from both A and C *)
END_IF;
IF tTmr_CondTemp_Timer_BC > tDiscrepTimeout_s AND tTmr_CondTemp_Timer_CA > tDiscrepTimeout_s THEN
    bTmr_CondTemp_Fault_C := TRUE;  (* Sensor C is divergent from both A and B *)
END_IF;

(* 1.5 2oo3 Median Voting & Graceful Degradation *)
IF NOT bTmr_CondTemp_Fault_A AND NOT bTmr_CondTemp_Fault_B AND NOT bTmr_CondTemp_Fault_C THEN
    (* All 3 Channels Healthy: Exact Mid-Value Selection *)
    IF ((rCondTemp_TE101A_degC >= rCondTemp_TE101B_degC AND rCondTemp_TE101A_degC <= rCondTemp_TE101C_degC) OR
        (rCondTemp_TE101A_degC <= rCondTemp_TE101B_degC AND rCondTemp_TE101A_degC >= rCondTemp_TE101C_degC)) THEN
        rTmr_CondTemp_Val := rCondTemp_TE101A_degC;
    ELSIF ((rCondTemp_TE101B_degC >= rCondTemp_TE101A_degC AND rCondTemp_TE101B_degC <= rCondTemp_TE101C_degC) OR
           (rCondTemp_TE101B_degC <= rCondTemp_TE101A_degC AND rCondTemp_TE101B_degC >= rCondTemp_TE101C_degC)) THEN
        rTmr_CondTemp_Val := rCondTemp_TE101B_degC;
    ELSE
        rTmr_CondTemp_Val := rCondTemp_TE101C_degC;
    END_IF;
    bTmr_CondTemp_Degraded_1oo2 := FALSE;
    bTmr_CondTemp_Trip_0oo3     := FALSE;
ELSIF NOT bTmr_CondTemp_Fault_A AND NOT bTmr_CondTemp_Fault_B THEN
    (* Sensor C Faulty: Degraded 1oo2 Mean of A and B *)
    rTmr_CondTemp_Val           := (rCondTemp_TE101A_degC + rCondTemp_TE101B_degC) * 0.5;
    bTmr_CondTemp_Degraded_1oo2 := TRUE;
    bTmr_CondTemp_Trip_0oo3     := FALSE;
ELSIF NOT bTmr_CondTemp_Fault_B AND NOT bTmr_CondTemp_Fault_C THEN
    (* Sensor A Faulty: Degraded 1oo2 Mean of B and C *)
    rTmr_CondTemp_Val           := (rCondTemp_TE101B_degC + rCondTemp_TE101C_degC) * 0.5;
    bTmr_CondTemp_Degraded_1oo2 := TRUE;
    bTmr_CondTemp_Trip_0oo3     := FALSE;
ELSIF NOT bTmr_CondTemp_Fault_C AND NOT bTmr_CondTemp_Fault_A THEN
    (* Sensor B Faulty: Degraded 1oo2 Mean of C and A *)
    rTmr_CondTemp_Val           := (rCondTemp_TE101C_degC + rCondTemp_TE101A_degC) * 0.5;
    bTmr_CondTemp_Degraded_1oo2 := TRUE;
    bTmr_CondTemp_Trip_0oo3     := FALSE;
ELSIF NOT bTmr_CondTemp_Fault_A THEN
    (* 2 Sensors Faulty: Degraded 1oo1 Single Survivor A *)
    rTmr_CondTemp_Val           := rCondTemp_TE101A_degC;
    bTmr_CondTemp_Degraded_1oo2 := TRUE;
    bTmr_CondTemp_Trip_0oo3     := FALSE;
ELSIF NOT bTmr_CondTemp_Fault_B THEN
    (* 2 Sensors Faulty: Degraded 1oo1 Single Survivor B *)
    rTmr_CondTemp_Val           := rCondTemp_TE101B_degC;
    bTmr_CondTemp_Degraded_1oo2 := TRUE;
    bTmr_CondTemp_Trip_0oo3     := FALSE;
ELSIF NOT bTmr_CondTemp_Fault_C THEN
    (* 2 Sensors Faulty: Degraded 1oo1 Single Survivor C *)
    rTmr_CondTemp_Val           := rCondTemp_TE101C_degC;
    bTmr_CondTemp_Degraded_1oo2 := TRUE;
    bTmr_CondTemp_Trip_0oo3     := FALSE;
ELSE
    (* All 3 Sensors Tripped: Fail-Safe State *)
    rTmr_CondTemp_Val           := 20.0; (* Fail-safe ambient fallback *)
    bTmr_CondTemp_Degraded_1oo2 := TRUE;
    bTmr_CondTemp_Trip_0oo3     := TRUE;
END_IF;
rVoted_CondMashTemp_degC := rTmr_CondTemp_Val;

(* ----------------------------------------------------------------------------------------------------
   TRIPLET 2: PELLET PRESS 400 kW MOTOR CURRENT (JT201A, JT201B, JT201C) [A]
   Range: 0.0 A to 1200.0 A, Discrepancy Limit: 35.0 A, Timeout: 2.50 s
   ---------------------------------------------------------------------------------------------------- *)
(* 2.1 Out-of-Range Sensor Hardware Validation *)
bTmr_PressCurr_Fault_A := (rPressMotorCurrent_JT201A_A < 0.0) OR (rPressMotorCurrent_JT201A_A > 1200.0);
bTmr_PressCurr_Fault_B := (rPressMotorCurrent_JT201B_A < 0.0) OR (rPressMotorCurrent_JT201B_A > 1200.0);
bTmr_PressCurr_Fault_C := (rPressMotorCurrent_JT201C_A < 0.0) OR (rPressMotorCurrent_JT201C_A > 1200.0);

(* 2.2 Pairwise Discrepancy Evaluation *)
bTmr_PressCurr_Discrep_AB := ABS(rPressMotorCurrent_JT201A_A - rPressMotorCurrent_JT201B_A) > rDiscrepLimit_PressCurr_A;
bTmr_PressCurr_Discrep_BC := ABS(rPressMotorCurrent_JT201B_A - rPressMotorCurrent_JT201C_A) > rDiscrepLimit_PressCurr_A;
bTmr_PressCurr_Discrep_CA := ABS(rPressMotorCurrent_JT201C_A - rPressMotorCurrent_JT201A_A) > rDiscrepLimit_PressCurr_A;

(* 2.3 Discrepancy Debounce Integration Timers *)
IF bTmr_PressCurr_Discrep_AB AND NOT bTmr_PressCurr_Fault_A AND NOT bTmr_PressCurr_Fault_B THEN
    tTmr_PressCurr_Timer_AB := tTmr_PressCurr_Timer_AB + 0.050;
ELSE
    tTmr_PressCurr_Timer_AB := MAX(0.0, tTmr_PressCurr_Timer_AB - 0.100);
END_IF;

IF bTmr_PressCurr_Discrep_BC AND NOT bTmr_PressCurr_Fault_B AND NOT bTmr_PressCurr_Fault_C THEN
    tTmr_PressCurr_Timer_BC := tTmr_PressCurr_Timer_BC + 0.050;
ELSE
    tTmr_PressCurr_Timer_BC := MAX(0.0, tTmr_PressCurr_Timer_BC - 0.100);
END_IF;

IF bTmr_PressCurr_Discrep_CA AND NOT bTmr_PressCurr_Fault_C AND NOT bTmr_PressCurr_Fault_A THEN
    tTmr_PressCurr_Timer_CA := tTmr_PressCurr_Timer_CA + 0.050;
ELSE
    tTmr_PressCurr_Timer_CA := MAX(0.0, tTmr_PressCurr_Timer_CA - 0.100);
END_IF;

(* 2.4 Persistent Divergence Fault Isolation *)
IF tTmr_PressCurr_Timer_AB > tDiscrepTimeout_s AND tTmr_PressCurr_Timer_CA > tDiscrepTimeout_s THEN
    bTmr_PressCurr_Fault_A := TRUE;
END_IF;
IF tTmr_PressCurr_Timer_AB > tDiscrepTimeout_s AND tTmr_PressCurr_Timer_BC > tDiscrepTimeout_s THEN
    bTmr_PressCurr_Fault_B := TRUE;
END_IF;
IF tTmr_PressCurr_Timer_BC > tDiscrepTimeout_s AND tTmr_PressCurr_Timer_CA > tDiscrepTimeout_s THEN
    bTmr_PressCurr_Fault_C := TRUE;
END_IF;

(* 2.5 2oo3 Median Voting & Graceful Degradation *)
IF NOT bTmr_PressCurr_Fault_A AND NOT bTmr_PressCurr_Fault_B AND NOT bTmr_PressCurr_Fault_C THEN
    IF ((rPressMotorCurrent_JT201A_A >= rPressMotorCurrent_JT201B_A AND rPressMotorCurrent_JT201A_A <= rPressMotorCurrent_JT201C_A) OR
        (rPressMotorCurrent_JT201A_A <= rPressMotorCurrent_JT201B_A AND rPressMotorCurrent_JT201A_A >= rPressMotorCurrent_JT201C_A)) THEN
        rTmr_PressCurr_Val := rPressMotorCurrent_JT201A_A;
    ELSIF ((rPressMotorCurrent_JT201B_A >= rPressMotorCurrent_JT201A_A AND rPressMotorCurrent_JT201B_A <= rPressMotorCurrent_JT201C_A) OR
           (rPressMotorCurrent_JT201B_A <= rPressMotorCurrent_JT201A_A AND rPressMotorCurrent_JT201B_A >= rPressMotorCurrent_JT201C_A)) THEN
        rTmr_PressCurr_Val := rPressMotorCurrent_JT201B_A;
    ELSE
        rTmr_PressCurr_Val := rPressMotorCurrent_JT201C_A;
    END_IF;
    bTmr_PressCurr_Degraded_1oo2 := FALSE;
    bTmr_PressCurr_Trip_0oo3     := FALSE;
ELSIF NOT bTmr_PressCurr_Fault_A AND NOT bTmr_PressCurr_Fault_B THEN
    (* Degraded 1oo2: Maximum selection for safety (prevents under-estimating overload) *)
    rTmr_PressCurr_Val           := MAX(rPressMotorCurrent_JT201A_A, rPressMotorCurrent_JT201B_A);
    bTmr_PressCurr_Degraded_1oo2 := TRUE;
    bTmr_PressCurr_Trip_0oo3     := FALSE;
ELSIF NOT bTmr_PressCurr_Fault_B AND NOT bTmr_PressCurr_Fault_C THEN
    rTmr_PressCurr_Val           := MAX(rPressMotorCurrent_JT201B_A, rPressMotorCurrent_JT201C_A);
    bTmr_PressCurr_Degraded_1oo2 := TRUE;
    bTmr_PressCurr_Trip_0oo3     := FALSE;
ELSIF NOT bTmr_PressCurr_Fault_C AND NOT bTmr_PressCurr_Fault_A THEN
    rTmr_PressCurr_Val           := MAX(rPressMotorCurrent_JT201C_A, rPressMotorCurrent_JT201A_A);
    bTmr_PressCurr_Degraded_1oo2 := TRUE;
    bTmr_PressCurr_Trip_0oo3     := FALSE;
ELSIF NOT bTmr_PressCurr_Fault_A THEN
    rTmr_PressCurr_Val           := rPressMotorCurrent_JT201A_A;
    bTmr_PressCurr_Degraded_1oo2 := TRUE;
    bTmr_PressCurr_Trip_0oo3     := FALSE;
ELSIF NOT bTmr_PressCurr_Fault_B THEN
    rTmr_PressCurr_Val           := rPressMotorCurrent_JT201B_A;
    bTmr_PressCurr_Degraded_1oo2 := TRUE;
    bTmr_PressCurr_Trip_0oo3     := FALSE;
ELSIF NOT bTmr_PressCurr_Fault_C THEN
    rTmr_PressCurr_Val           := rPressMotorCurrent_JT201C_A;
    bTmr_PressCurr_Degraded_1oo2 := TRUE;
    bTmr_PressCurr_Trip_0oo3     := FALSE;
ELSE
    rTmr_PressCurr_Val           := 750.0; (* Over-estimate fail-safe to force interlock shutdown *)
    bTmr_PressCurr_Degraded_1oo2 := TRUE;
    bTmr_PressCurr_Trip_0oo3     := TRUE;
END_IF;
rVoted_PressMotorCurrent_A := rTmr_PressCurr_Val;

(* ----------------------------------------------------------------------------------------------------
   TRIPLET 3: ROLLER DYNAMIC HYDRAULIC GAP PRESSURE (PT202A, PT202B, PT202C) [bar]
   Range: 0.0 bar to 350.0 bar, Discrepancy Limit: 18.0 bar, Timeout: 2.50 s
   ---------------------------------------------------------------------------------------------------- *)
(* 3.1 Out-of-Range Sensor Hardware Validation *)
bTmr_HydGapPress_Fault_A := (rHydGapPress_PT202A_bar < 0.0) OR (rHydGapPress_PT202A_bar > 350.0);
bTmr_HydGapPress_Fault_B := (rHydGapPress_PT202B_bar < 0.0) OR (rHydGapPress_PT202B_bar > 350.0);
bTmr_HydGapPress_Fault_C := (rHydGapPress_PT202C_bar < 0.0) OR (rHydGapPress_PT202C_bar > 350.0);

(* 3.2 Pairwise Discrepancy Evaluation *)
bTmr_HydGapPress_Discrep_AB := ABS(rHydGapPress_PT202A_bar - rHydGapPress_PT202B_bar) > rDiscrepLimit_HydGapPress_bar;
bTmr_HydGapPress_Discrep_BC := ABS(rHydGapPress_PT202B_bar - rHydGapPress_PT202C_bar) > rDiscrepLimit_HydGapPress_bar;
bTmr_HydGapPress_Discrep_CA := ABS(rHydGapPress_PT202C_bar - rHydGapPress_PT202A_bar) > rDiscrepLimit_HydGapPress_bar;

(* 3.3 Discrepancy Debounce Integration Timers *)
IF bTmr_HydGapPress_Discrep_AB AND NOT bTmr_HydGapPress_Fault_A AND NOT bTmr_HydGapPress_Fault_B THEN
    tTmr_HydGapPress_Timer_AB := tTmr_HydGapPress_Timer_AB + 0.050;
ELSE
    tTmr_HydGapPress_Timer_AB := MAX(0.0, tTmr_HydGapPress_Timer_AB - 0.100);
END_IF;

IF bTmr_HydGapPress_Discrep_BC AND NOT bTmr_HydGapPress_Fault_B AND NOT bTmr_HydGapPress_Fault_C THEN
    tTmr_HydGapPress_Timer_BC := tTmr_HydGapPress_Timer_BC + 0.050;
ELSE
    tTmr_HydGapPress_Timer_BC := MAX(0.0, tTmr_HydGapPress_Timer_BC - 0.100);
END_IF;

IF bTmr_HydGapPress_Discrep_CA AND NOT bTmr_HydGapPress_Fault_C AND NOT bTmr_HydGapPress_Fault_A THEN
    tTmr_HydGapPress_Timer_CA := tTmr_HydGapPress_Timer_CA + 0.050;
ELSE
    tTmr_HydGapPress_Timer_CA := MAX(0.0, tTmr_HydGapPress_Timer_CA - 0.100);
END_IF;

(* 3.4 Persistent Divergence Fault Isolation *)
IF tTmr_HydGapPress_Timer_AB > tDiscrepTimeout_s AND tTmr_HydGapPress_Timer_CA > tDiscrepTimeout_s THEN
    bTmr_HydGapPress_Fault_A := TRUE;
END_IF;
IF tTmr_HydGapPress_Timer_AB > tDiscrepTimeout_s AND tTmr_HydGapPress_Timer_BC > tDiscrepTimeout_s THEN
    bTmr_HydGapPress_Fault_B := TRUE;
END_IF;
IF tTmr_HydGapPress_Timer_BC > tDiscrepTimeout_s AND tTmr_HydGapPress_Timer_CA > tDiscrepTimeout_s THEN
    bTmr_HydGapPress_Fault_C := TRUE;
END_IF;

(* 3.5 2oo3 Median Voting & Graceful Degradation *)
IF NOT bTmr_HydGapPress_Fault_A AND NOT bTmr_HydGapPress_Fault_B AND NOT bTmr_HydGapPress_Fault_C THEN
    IF ((rHydGapPress_PT202A_bar >= rHydGapPress_PT202B_bar AND rHydGapPress_PT202A_bar <= rHydGapPress_PT202C_bar) OR
        (rHydGapPress_PT202A_bar <= rHydGapPress_PT202B_bar AND rHydGapPress_PT202A_bar >= rHydGapPress_PT202C_bar)) THEN
        rTmr_HydGapPress_Val := rHydGapPress_PT202A_bar;
    ELSIF ((rHydGapPress_PT202B_bar >= rHydGapPress_PT202A_bar AND rHydGapPress_PT202B_bar <= rHydGapPress_PT202C_bar) OR
           (rHydGapPress_PT202B_bar <= rHydGapPress_PT202A_bar AND rHydGapPress_PT202B_bar >= rHydGapPress_PT202C_bar)) THEN
        rTmr_HydGapPress_Val := rHydGapPress_PT202B_bar;
    ELSE
        rTmr_HydGapPress_Val := rHydGapPress_PT202C_bar;
    END_IF;
    bTmr_HydGapPress_Degraded_1oo2 := FALSE;
    bTmr_HydGapPress_Trip_0oo3     := FALSE;
ELSIF NOT bTmr_HydGapPress_Fault_A AND NOT bTmr_HydGapPress_Fault_B THEN
    rTmr_HydGapPress_Val           := (rHydGapPress_PT202A_bar + rHydGapPress_PT202B_bar) * 0.5;
    bTmr_HydGapPress_Degraded_1oo2 := TRUE;
    bTmr_HydGapPress_Trip_0oo3     := FALSE;
ELSIF NOT bTmr_HydGapPress_Fault_B AND NOT bTmr_HydGapPress_Fault_C THEN
    rTmr_HydGapPress_Val           := (rHydGapPress_PT202B_bar + rHydGapPress_PT202C_bar) * 0.5;
    bTmr_HydGapPress_Degraded_1oo2 := TRUE;
    bTmr_HydGapPress_Trip_0oo3     := FALSE;
ELSIF NOT bTmr_HydGapPress_Fault_C AND NOT bTmr_HydGapPress_Fault_A THEN
    rTmr_HydGapPress_Val           := (rHydGapPress_PT202C_bar + rHydGapPress_PT202A_bar) * 0.5;
    bTmr_HydGapPress_Degraded_1oo2 := TRUE;
    bTmr_HydGapPress_Trip_0oo3     := FALSE;
ELSIF NOT bTmr_HydGapPress_Fault_A THEN
    rTmr_HydGapPress_Val           := rHydGapPress_PT202A_bar;
    bTmr_HydGapPress_Degraded_1oo2 := TRUE;
    bTmr_HydGapPress_Trip_0oo3     := FALSE;
ELSIF NOT bTmr_HydGapPress_Fault_B THEN
    rTmr_HydGapPress_Val           := rHydGapPress_PT202B_bar;
    bTmr_HydGapPress_Degraded_1oo2 := TRUE;
    bTmr_HydGapPress_Trip_0oo3     := FALSE;
ELSIF NOT bTmr_HydGapPress_Fault_C THEN
    rTmr_HydGapPress_Val           := rHydGapPress_PT202C_bar;
    bTmr_HydGapPress_Degraded_1oo2 := TRUE;
    bTmr_HydGapPress_Trip_0oo3     := FALSE;
ELSE
    rTmr_HydGapPress_Val           := 0.0;
    bTmr_HydGapPress_Degraded_1oo2 := TRUE;
    bTmr_HydGapPress_Trip_0oo3     := TRUE;
END_IF;
rVoted_HydGapPress_bar := rTmr_HydGapPress_Val;

(* ----------------------------------------------------------------------------------------------------
   TRIPLET 4: COUNTERFLOW COOLER BED LEVEL (LT301A, LT301B, LT301C) [mm]
   Range: 0.0 mm to 2000.0 mm, Discrepancy Limit: 85.0 mm, Timeout: 2.50 s
   ---------------------------------------------------------------------------------------------------- *)
(* 4.1 Out-of-Range Sensor Hardware Validation *)
bTmr_CoolerLevel_Fault_A := (rCoolerBedLevel_LT301A_mm < 0.0) OR (rCoolerBedLevel_LT301A_mm > 2000.0);
bTmr_CoolerLevel_Fault_B := (rCoolerBedLevel_LT301B_mm < 0.0) OR (rCoolerBedLevel_LT301B_mm > 2000.0);
bTmr_CoolerLevel_Fault_C := (rCoolerBedLevel_LT301C_mm < 0.0) OR (rCoolerBedLevel_LT301C_mm > 2000.0);

(* 4.2 Pairwise Discrepancy Evaluation *)
bTmr_CoolerLevel_Discrep_AB := ABS(rCoolerBedLevel_LT301A_mm - rCoolerBedLevel_LT301B_mm) > rDiscrepLimit_CoolerLevel_mm;
bTmr_CoolerLevel_Discrep_BC := ABS(rCoolerBedLevel_LT301B_mm - rCoolerBedLevel_LT301C_mm) > rDiscrepLimit_CoolerLevel_mm;
bTmr_CoolerLevel_Discrep_CA := ABS(rCoolerBedLevel_LT301C_mm - rCoolerBedLevel_LT301A_mm) > rDiscrepLimit_CoolerLevel_mm;

(* 4.3 Discrepancy Debounce Integration Timers *)
IF bTmr_CoolerLevel_Discrep_AB AND NOT bTmr_CoolerLevel_Fault_A AND NOT bTmr_CoolerLevel_Fault_B THEN
    tTmr_CoolerLevel_Timer_AB := tTmr_CoolerLevel_Timer_AB + 0.050;
ELSE
    tTmr_CoolerLevel_Timer_AB := MAX(0.0, tTmr_CoolerLevel_Timer_AB - 0.100);
END_IF;

IF bTmr_CoolerLevel_Discrep_BC AND NOT bTmr_CoolerLevel_Fault_B AND NOT bTmr_CoolerLevel_Fault_C THEN
    tTmr_CoolerLevel_Timer_BC := tTmr_CoolerLevel_Timer_BC + 0.050;
ELSE
    tTmr_CoolerLevel_Timer_BC := MAX(0.0, tTmr_CoolerLevel_Timer_BC - 0.100);
END_IF;

IF bTmr_CoolerLevel_Discrep_CA AND NOT bTmr_CoolerLevel_Fault_C AND NOT bTmr_CoolerLevel_Fault_A THEN
    tTmr_CoolerLevel_Timer_CA := tTmr_CoolerLevel_Timer_CA + 0.050;
ELSE
    tTmr_CoolerLevel_Timer_CA := MAX(0.0, tTmr_CoolerLevel_Timer_CA - 0.100);
END_IF;

(* 4.4 Persistent Divergence Fault Isolation *)
IF tTmr_CoolerLevel_Timer_AB > tDiscrepTimeout_s AND tTmr_CoolerLevel_Timer_CA > tDiscrepTimeout_s THEN
    bTmr_CoolerLevel_Fault_A := TRUE;
END_IF;
IF tTmr_CoolerLevel_Timer_AB > tDiscrepTimeout_s AND tTmr_CoolerLevel_Timer_BC > tDiscrepTimeout_s THEN
    bTmr_CoolerLevel_Fault_B := TRUE;
END_IF;
IF tTmr_CoolerLevel_Timer_BC > tDiscrepTimeout_s AND tTmr_CoolerLevel_Timer_CA > tDiscrepTimeout_s THEN
    bTmr_CoolerLevel_Fault_C := TRUE;
END_IF;

(* 4.5 2oo3 Median Voting & Graceful Degradation *)
IF NOT bTmr_CoolerLevel_Fault_A AND NOT bTmr_CoolerLevel_Fault_B AND NOT bTmr_CoolerLevel_Fault_C THEN
    IF ((rCoolerBedLevel_LT301A_mm >= rCoolerBedLevel_LT301B_mm AND rCoolerBedLevel_LT301A_mm <= rCoolerBedLevel_LT301C_mm) OR
        (rCoolerBedLevel_LT301A_mm <= rCoolerBedLevel_LT301B_mm AND rCoolerBedLevel_LT301A_mm >= rCoolerBedLevel_LT301C_mm)) THEN
        rTmr_CoolerLevel_Val := rCoolerBedLevel_LT301A_mm;
    ELSIF ((rCoolerBedLevel_LT301B_mm >= rCoolerBedLevel_LT301A_mm AND rCoolerBedLevel_LT301B_mm <= rCoolerBedLevel_LT301C_mm) OR
           (rCoolerBedLevel_LT301B_mm <= rCoolerBedLevel_LT301A_mm AND rCoolerBedLevel_LT301B_mm >= rCoolerBedLevel_LT301C_mm)) THEN
        rTmr_CoolerLevel_Val := rCoolerBedLevel_LT301B_mm;
    ELSE
        rTmr_CoolerLevel_Val := rCoolerBedLevel_LT301C_mm;
    END_IF;
    bTmr_CoolerLevel_Degraded_1oo2 := FALSE;
    bTmr_CoolerLevel_Trip_0oo3     := FALSE;
ELSIF NOT bTmr_CoolerLevel_Fault_A AND NOT bTmr_CoolerLevel_Fault_B THEN
    rTmr_CoolerLevel_Val           := (rCoolerBedLevel_LT301A_mm + rCoolerBedLevel_LT301B_mm) * 0.5;
    bTmr_CoolerLevel_Degraded_1oo2 := TRUE;
    bTmr_CoolerLevel_Trip_0oo3     := FALSE;
ELSIF NOT bTmr_CoolerLevel_Fault_B AND NOT bTmr_CoolerLevel_Fault_C THEN
    rTmr_CoolerLevel_Val           := (rCoolerBedLevel_LT301B_mm + rCoolerBedLevel_LT301C_mm) * 0.5;
    bTmr_CoolerLevel_Degraded_1oo2 := TRUE;
    bTmr_CoolerLevel_Trip_0oo3     := FALSE;
ELSIF NOT bTmr_CoolerLevel_Fault_C AND NOT bTmr_CoolerLevel_Fault_A THEN
    rTmr_CoolerLevel_Val           := (rCoolerBedLevel_LT301C_mm + rCoolerBedLevel_LT301A_mm) * 0.5;
    bTmr_CoolerLevel_Degraded_1oo2 := TRUE;
    bTmr_CoolerLevel_Trip_0oo3     := FALSE;
ELSIF NOT bTmr_CoolerLevel_Fault_A THEN
    rTmr_CoolerLevel_Val           := rCoolerBedLevel_LT301A_mm;
    bTmr_CoolerLevel_Degraded_1oo2 := TRUE;
    bTmr_CoolerLevel_Trip_0oo3     := FALSE;
ELSIF NOT bTmr_CoolerLevel_Fault_B THEN
    rTmr_CoolerLevel_Val           := rCoolerBedLevel_LT301B_mm;
    bTmr_CoolerLevel_Degraded_1oo2 := TRUE;
    bTmr_CoolerLevel_Trip_0oo3     := FALSE;
ELSIF NOT bTmr_CoolerLevel_Fault_C THEN
    rTmr_CoolerLevel_Val           := rCoolerBedLevel_LT301C_mm;
    bTmr_CoolerLevel_Degraded_1oo2 := TRUE;
    bTmr_CoolerLevel_Trip_0oo3     := FALSE;
ELSE
    rTmr_CoolerLevel_Val           := 950.0; (* Default nominal bed depth fallback *)
    bTmr_CoolerLevel_Degraded_1oo2 := TRUE;
    bTmr_CoolerLevel_Trip_0oo3     := TRUE;
END_IF;
rVoted_CoolerBedLevel_mm := rTmr_CoolerLevel_Val;

(* ----------------------------------------------------------------------------------------------------
   SENSOR HEALTH DIAGNOSTIC BIT-PACKING (DWORD dwSensorHealth_Status)
   ---------------------------------------------------------------------------------------------------- *)
dwSensorHealth_Status := 16#00000000;
IF bTmr_CondTemp_Fault_A          THEN dwSensorHealth_Status := dwSensorHealth_Status OR 16#00000001; END_IF;
IF bTmr_CondTemp_Fault_B          THEN dwSensorHealth_Status := dwSensorHealth_Status OR 16#00000002; END_IF;
IF bTmr_CondTemp_Fault_C          THEN dwSensorHealth_Status := dwSensorHealth_Status OR 16#00000004; END_IF;
IF bTmr_CondTemp_Degraded_1oo2    THEN dwSensorHealth_Status := dwSensorHealth_Status OR 16#00000008; END_IF;
IF bTmr_CondTemp_Trip_0oo3        THEN dwSensorHealth_Status := dwSensorHealth_Status OR 16#00000010; END_IF;

IF bTmr_PressCurr_Fault_A         THEN dwSensorHealth_Status := dwSensorHealth_Status OR 16#00000020; END_IF;
IF bTmr_PressCurr_Fault_B         THEN dwSensorHealth_Status := dwSensorHealth_Status OR 16#00000040; END_IF;
IF bTmr_PressCurr_Fault_C         THEN dwSensorHealth_Status := dwSensorHealth_Status OR 16#00000080; END_IF;
IF bTmr_PressCurr_Degraded_1oo2   THEN dwSensorHealth_Status := dwSensorHealth_Status OR 16#00000100; END_IF;
IF bTmr_PressCurr_Trip_0oo3       THEN dwSensorHealth_Status := dwSensorHealth_Status OR 16#00000200; END_IF;

IF bTmr_HydGapPress_Fault_A       THEN dwSensorHealth_Status := dwSensorHealth_Status OR 16#00000400; END_IF;
IF bTmr_HydGapPress_Fault_B       THEN dwSensorHealth_Status := dwSensorHealth_Status OR 16#00000800; END_IF;
IF bTmr_HydGapPress_Fault_C       THEN dwSensorHealth_Status := dwSensorHealth_Status OR 16#00001000; END_IF;
IF bTmr_HydGapPress_Degraded_1oo2 THEN dwSensorHealth_Status := dwSensorHealth_Status OR 16#00002000; END_IF;
IF bTmr_HydGapPress_Trip_0oo3     THEN dwSensorHealth_Status := dwSensorHealth_Status OR 16#00004000; END_IF;

IF bTmr_CoolerLevel_Fault_A       THEN dwSensorHealth_Status := dwSensorHealth_Status OR 16#00008000; END_IF;
IF bTmr_CoolerLevel_Fault_B       THEN dwSensorHealth_Status := dwSensorHealth_Status OR 16#00010000; END_IF;
IF bTmr_CoolerLevel_Fault_C       THEN dwSensorHealth_Status := dwSensorHealth_Status OR 16#00020000; END_IF;
IF bTmr_CoolerLevel_Degraded_1oo2 THEN dwSensorHealth_Status := dwSensorHealth_Status OR 16#00040000; END_IF;
IF bTmr_CoolerLevel_Trip_0oo3     THEN dwSensorHealth_Status := dwSensorHealth_Status OR 16#00080000; END_IF;
"""
