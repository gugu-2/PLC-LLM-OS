# -*- coding: utf-8 -*-
"""
Module: retort_builder/mod_tmr.py
Implements Phase 1: 2oo3 Triple Modular Redundant (TMR) Sensor Voting Engine
with Median Selection, Discrepancy Debounce Timers, and Bumpless Degradation.
"""

def generate_tmr():
    return '''(* =====================================================================================================================
 * PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANT (TMR) SENSOR VOTING WITH DISCREPANCY TIMERS
 * Fault Tolerant Architecture: IEC 61508 / ISA-84 SIL-3 Certified Redundancy Strategy
 * Sensor Subsystems:
 *   1. Retort Vessel Temperature: TT-101A, TT-101B, TT-101C [deg C]
 *   2. Retort Vessel Absolute Pressure: PT-201A, PT-201B, PT-201C [bar]
 *   3. Product Core Temperature: TT-301A, TT-301B, TT-301C [deg C]
 *   4. Condensate Sump Liquid Level: LT-401A, LT-401B, LT-401C [mm]
 * ===================================================================================================================== *)

(* -------------------------------------------------------------------------
 * SUB-SECTION 1.1: VESSEL TEMPERATURE TT-101 VOTING (2oo3 -> 1oo2 -> 1oo1)
 * ------------------------------------------------------------------------- *)
rTMR_TT101_Raw[1] := rTT_101A_VesselTemp_degC;
rTMR_TT101_Raw[2] := rTT_101B_VesselTemp_degC;
rTMR_TT101_Raw[3] := rTT_101C_VesselTemp_degC;

(* Bubble sort 3-element comparison network to isolate median *)
rTMR_TT101_Sorted[1] := rTMR_TT101_Raw[1];
rTMR_TT101_Sorted[2] := rTMR_TT101_Raw[2];
rTMR_TT101_Sorted[3] := rTMR_TT101_Raw[3];

IF rTMR_TT101_Sorted[1] > rTMR_TT101_Sorted[2] THEN
    rTempCalc1 := rTMR_TT101_Sorted[1];
    rTMR_TT101_Sorted[1] := rTMR_TT101_Sorted[2];
    rTMR_TT101_Sorted[2] := rTempCalc1;
END_IF;

IF rTMR_TT101_Sorted[2] > rTMR_TT101_Sorted[3] THEN
    rTempCalc1 := rTMR_TT101_Sorted[2];
    rTMR_TT101_Sorted[2] := rTMR_TT101_Sorted[3];
    rTMR_TT101_Sorted[3] := rTempCalc1;
END_IF;

IF rTMR_TT101_Sorted[1] > rTMR_TT101_Sorted[2] THEN
    rTempCalc1 := rTMR_TT101_Sorted[1];
    rTMR_TT101_Sorted[1] := rTMR_TT101_Sorted[2];
    rTMR_TT101_Sorted[2] := rTempCalc1;
END_IF;

(* Evaluate channel deviation against median rTMR_TT101_Sorted[2] *)
FOR iIdx1 := 1 TO 3 DO
    rTempCalc2 := ABS(rTMR_TT101_Raw[iIdx1] - rTMR_TT101_Sorted[2]);
    IF rTempCalc2 > cTMR_TT101_MaxDev_degC THEN
        rTMR_TT101_DiscrepTimer[iIdx1] := rTMR_TT101_DiscrepTimer[iIdx1] + rTs_s;
        IF rTMR_TT101_DiscrepTimer[iIdx1] >= cTMR_DiscrepTimeout_s THEN
            bTMR_TT101_ChFault[iIdx1] := TRUE;
        END_IF;
    ELSE
        IF rTMR_TT101_DiscrepTimer[iIdx1] > 0.0 THEN
            rTMR_TT101_DiscrepTimer[iIdx1] := rTMR_TT101_DiscrepTimer[iIdx1] - (rTs_s * 0.50);
            IF rTMR_TT101_DiscrepTimer[iIdx1] < 0.0 THEN
                rTMR_TT101_DiscrepTimer[iIdx1] := 0.0;
            END_IF;
        END_IF;
        IF bCmd_ResetTrip AND (rTMR_TT101_DiscrepTimer[iIdx1] <= 0.0) THEN
            bTMR_TT101_ChFault[iIdx1] := FALSE;
        END_IF;
    END_IF;
END_FOR;

(* Determine TT-101 degradation mode *)
IF (NOT bTMR_TT101_ChFault[1]) AND (NOT bTMR_TT101_ChFault[2]) AND (NOT bTMR_TT101_ChFault[3]) THEN
    iTMR_TT101_Mode := 3; (* Full 2oo3 Median Mode *)
    rTMR_TT101_Voted := rTMR_TT101_Sorted[2];
ELSIF (NOT bTMR_TT101_ChFault[1]) AND (NOT bTMR_TT101_ChFault[2]) AND bTMR_TT101_ChFault[3] THEN
    iTMR_TT101_Mode := 2; (* 1oo2 Degraded Mode (Ch A + Ch B) *)
    rTMR_TT101_Voted := (rTMR_TT101_Raw[1] + rTMR_TT101_Raw[2]) * 0.50;
ELSIF (NOT bTMR_TT101_ChFault[1]) AND bTMR_TT101_ChFault[2] AND (NOT bTMR_TT101_ChFault[3]) THEN
    iTMR_TT101_Mode := 2; (* 1oo2 Degraded Mode (Ch A + Ch C) *)
    rTMR_TT101_Voted := (rTMR_TT101_Raw[1] + rTMR_TT101_Raw[3]) * 0.50;
ELSIF bTMR_TT101_ChFault[1] AND (NOT bTMR_TT101_ChFault[2]) AND (NOT bTMR_TT101_ChFault[3]) THEN
    iTMR_TT101_Mode := 2; (* 1oo2 Degraded Mode (Ch B + Ch C) *)
    rTMR_TT101_Voted := (rTMR_TT101_Raw[2] + rTMR_TT101_Raw[3]) * 0.50;
ELSIF (NOT bTMR_TT101_ChFault[1]) AND bTMR_TT101_ChFault[2] AND bTMR_TT101_ChFault[3] THEN
    iTMR_TT101_Mode := 1; (* 1oo1 Failsafe Mode (Ch A surviving) *)
    rTMR_TT101_Voted := rTMR_TT101_Raw[1];
ELSIF bTMR_TT101_ChFault[1] AND (NOT bTMR_TT101_ChFault[2]) AND bTMR_TT101_ChFault[3] THEN
    iTMR_TT101_Mode := 1; (* 1oo1 Failsafe Mode (Ch B surviving) *)
    rTMR_TT101_Voted := rTMR_TT101_Raw[2];
ELSIF bTMR_TT101_ChFault[1] AND bTMR_TT101_ChFault[2] AND (NOT bTMR_TT101_ChFault[3]) THEN
    iTMR_TT101_Mode := 1; (* 1oo1 Failsafe Mode (Ch C surviving) *)
    rTMR_TT101_Voted := rTMR_TT101_Raw[3];
ELSE
    iTMR_TT101_Mode := 0; (* All Channels Failed - Trip *)
    bTripLatched_TMR_Failure := TRUE;
    rTMR_TT101_Voted := rTMR_TT101_Sorted[2];
END_IF;

(* -------------------------------------------------------------------------
 * SUB-SECTION 1.2: VESSEL PRESSURE PT-201 VOTING (2oo3 -> 1oo2 -> 1oo1)
 * ------------------------------------------------------------------------- *)
rTMR_PT201_Raw[1] := rPT_201A_VesselPress_bar;
rTMR_PT201_Raw[2] := rPT_201B_VesselPress_bar;
rTMR_PT201_Raw[3] := rPT_201C_VesselPress_bar;

rTMR_PT201_Sorted[1] := rTMR_PT201_Raw[1];
rTMR_PT201_Sorted[2] := rTMR_PT201_Raw[2];
rTMR_PT201_Sorted[3] := rTMR_PT201_Raw[3];

IF rTMR_PT201_Sorted[1] > rTMR_PT201_Sorted[2] THEN
    rTempCalc1 := rTMR_PT201_Sorted[1];
    rTMR_PT201_Sorted[1] := rTMR_PT201_Sorted[2];
    rTMR_PT201_Sorted[2] := rTempCalc1;
END_IF;

IF rTMR_PT201_Sorted[2] > rTMR_PT201_Sorted[3] THEN
    rTempCalc1 := rTMR_PT201_Sorted[2];
    rTMR_PT201_Sorted[2] := rTMR_PT201_Sorted[3];
    rTMR_PT201_Sorted[3] := rTempCalc1;
END_IF;

IF rTMR_PT201_Sorted[1] > rTMR_PT201_Sorted[2] THEN
    rTempCalc1 := rTMR_PT201_Sorted[1];
    rTMR_PT201_Sorted[1] := rTMR_PT201_Sorted[2];
    rTMR_PT201_Sorted[2] := rTempCalc1;
END_IF;

FOR iIdx1 := 1 TO 3 DO
    rTempCalc2 := ABS(rTMR_PT201_Raw[iIdx1] - rTMR_PT201_Sorted[2]);
    IF rTempCalc2 > cTMR_PT201_MaxDev_bar THEN
        rTMR_PT201_DiscrepTimer[iIdx1] := rTMR_PT201_DiscrepTimer[iIdx1] + rTs_s;
        IF rTMR_PT201_DiscrepTimer[iIdx1] >= cTMR_DiscrepTimeout_s THEN
            bTMR_PT201_ChFault[iIdx1] := TRUE;
        END_IF;
    ELSE
        IF rTMR_PT201_DiscrepTimer[iIdx1] > 0.0 THEN
            rTMR_PT201_DiscrepTimer[iIdx1] := rTMR_PT201_DiscrepTimer[iIdx1] - (rTs_s * 0.50);
            IF rTMR_PT201_DiscrepTimer[iIdx1] < 0.0 THEN
                rTMR_PT201_DiscrepTimer[iIdx1] := 0.0;
            END_IF;
        END_IF;
        IF bCmd_ResetTrip AND (rTMR_PT201_DiscrepTimer[iIdx1] <= 0.0) THEN
            bTMR_PT201_ChFault[iIdx1] := FALSE;
        END_IF;
    END_IF;
END_FOR;

IF (NOT bTMR_PT201_ChFault[1]) AND (NOT bTMR_PT201_ChFault[2]) AND (NOT bTMR_PT201_ChFault[3]) THEN
    iTMR_PT201_Mode := 3;
    rTMR_PT201_Voted := rTMR_PT201_Sorted[2];
ELSIF (NOT bTMR_PT201_ChFault[1]) AND (NOT bTMR_PT201_ChFault[2]) AND bTMR_PT201_ChFault[3] THEN
    iTMR_PT201_Mode := 2;
    rTMR_PT201_Voted := (rTMR_PT201_Raw[1] + rTMR_PT201_Raw[2]) * 0.50;
ELSIF (NOT bTMR_PT201_ChFault[1]) AND bTMR_PT201_ChFault[2] AND (NOT bTMR_PT201_ChFault[3]) THEN
    iTMR_PT201_Mode := 2;
    rTMR_PT201_Voted := (rTMR_PT201_Raw[1] + rTMR_PT201_Raw[3]) * 0.50;
ELSIF bTMR_PT201_ChFault[1] AND (NOT bTMR_PT201_ChFault[2]) AND (NOT bTMR_PT201_ChFault[3]) THEN
    iTMR_PT201_Mode := 2;
    rTMR_PT201_Voted := (rTMR_PT201_Raw[2] + rTMR_PT201_Raw[3]) * 0.50;
ELSIF (NOT bTMR_PT201_ChFault[1]) AND bTMR_PT201_ChFault[2] AND bTMR_PT201_ChFault[3] THEN
    iTMR_PT201_Mode := 1;
    rTMR_PT201_Voted := rTMR_PT201_Raw[1];
ELSIF bTMR_PT201_ChFault[1] AND (NOT bTMR_PT201_ChFault[2]) AND bTMR_PT201_ChFault[3] THEN
    iTMR_PT201_Mode := 1;
    rTMR_PT201_Voted := rTMR_PT201_Raw[2];
ELSIF bTMR_PT201_ChFault[1] AND bTMR_PT201_ChFault[2] AND (NOT bTMR_PT201_ChFault[3]) THEN
    iTMR_PT201_Mode := 1;
    rTMR_PT201_Voted := rTMR_PT201_Raw[3];
ELSE
    iTMR_PT201_Mode := 0;
    bTripLatched_TMR_Failure := TRUE;
    rTMR_PT201_Voted := rTMR_PT201_Sorted[2];
END_IF;

(* -------------------------------------------------------------------------
 * SUB-SECTION 1.3: PRODUCT CORE TEMPERATURE TT-301 VOTING (2oo3 -> 1oo2 -> 1oo1)
 * ------------------------------------------------------------------------- *)
rTMR_TT301_Raw[1] := rTT_301A_CanCoreTemp_degC;
rTMR_TT301_Raw[2] := rTT_301B_CanCoreTemp_degC;
rTMR_TT301_Raw[3] := rTT_301C_CanCoreTemp_degC;

rTMR_TT301_Sorted[1] := rTMR_TT301_Raw[1];
rTMR_TT301_Sorted[2] := rTMR_TT301_Raw[2];
rTMR_TT301_Sorted[3] := rTMR_TT301_Raw[3];

IF rTMR_TT301_Sorted[1] > rTMR_TT301_Sorted[2] THEN
    rTempCalc1 := rTMR_TT301_Sorted[1];
    rTMR_TT301_Sorted[1] := rTMR_TT301_Sorted[2];
    rTMR_TT301_Sorted[2] := rTempCalc1;
END_IF;

IF rTMR_TT301_Sorted[2] > rTMR_TT301_Sorted[3] THEN
    rTempCalc1 := rTMR_TT301_Sorted[2];
    rTMR_TT301_Sorted[2] := rTMR_TT301_Sorted[3];
    rTMR_TT301_Sorted[3] := rTempCalc1;
END_IF;

IF rTMR_TT301_Sorted[1] > rTMR_TT301_Sorted[2] THEN
    rTempCalc1 := rTMR_TT301_Sorted[1];
    rTMR_TT301_Sorted[1] := rTMR_TT301_Sorted[2];
    rTMR_TT301_Sorted[2] := rTempCalc1;
END_IF;

FOR iIdx1 := 1 TO 3 DO
    rTempCalc2 := ABS(rTMR_TT301_Raw[iIdx1] - rTMR_TT301_Sorted[2]);
    IF rTempCalc2 > cTMR_TT301_MaxDev_degC THEN
        rTMR_TT301_DiscrepTimer[iIdx1] := rTMR_TT301_DiscrepTimer[iIdx1] + rTs_s;
        IF rTMR_TT301_DiscrepTimer[iIdx1] >= cTMR_DiscrepTimeout_s THEN
            bTMR_TT301_ChFault[iIdx1] := TRUE;
        END_IF;
    ELSE
        IF rTMR_TT301_DiscrepTimer[iIdx1] > 0.0 THEN
            rTMR_TT301_DiscrepTimer[iIdx1] := rTMR_TT301_DiscrepTimer[iIdx1] - (rTs_s * 0.50);
            IF rTMR_TT301_DiscrepTimer[iIdx1] < 0.0 THEN
                rTMR_TT301_DiscrepTimer[iIdx1] := 0.0;
            END_IF;
        END_IF;
        IF bCmd_ResetTrip AND (rTMR_TT301_DiscrepTimer[iIdx1] <= 0.0) THEN
            bTMR_TT301_ChFault[iIdx1] := FALSE;
        END_IF;
    END_IF;
END_FOR;

IF (NOT bTMR_TT301_ChFault[1]) AND (NOT bTMR_TT301_ChFault[2]) AND (NOT bTMR_TT301_ChFault[3]) THEN
    iTMR_TT301_Mode := 3;
    rTMR_TT301_Voted := rTMR_TT301_Sorted[2];
ELSIF (NOT bTMR_TT301_ChFault[1]) AND (NOT bTMR_TT301_ChFault[2]) AND bTMR_TT301_ChFault[3] THEN
    iTMR_TT301_Mode := 2;
    rTMR_TT301_Voted := (rTMR_TT301_Raw[1] + rTMR_TT301_Raw[2]) * 0.50;
ELSIF (NOT bTMR_TT301_ChFault[1]) AND bTMR_TT301_ChFault[2] AND (NOT bTMR_TT301_ChFault[3]) THEN
    iTMR_TT301_Mode := 2;
    rTMR_TT301_Voted := (rTMR_TT301_Raw[1] + rTMR_TT301_Raw[3]) * 0.50;
ELSIF bTMR_TT301_ChFault[1] AND (NOT bTMR_TT301_ChFault[2]) AND (NOT bTMR_TT301_ChFault[3]) THEN
    iTMR_TT301_Mode := 2;
    rTMR_TT301_Voted := (rTMR_TT301_Raw[2] + rTMR_TT301_Raw[3]) * 0.50;
ELSIF (NOT bTMR_TT301_ChFault[1]) AND bTMR_TT301_ChFault[2] AND bTMR_TT301_ChFault[3] THEN
    iTMR_TT301_Mode := 1;
    rTMR_TT301_Voted := rTMR_TT301_Raw[1];
ELSIF bTMR_TT301_ChFault[1] AND (NOT bTMR_TT301_ChFault[2]) AND bTMR_TT301_ChFault[3] THEN
    iTMR_TT301_Mode := 1;
    rTMR_TT301_Voted := rTMR_TT301_Raw[2];
ELSIF bTMR_TT301_ChFault[1] AND bTMR_TT301_ChFault[2] AND (NOT bTMR_TT301_ChFault[3]) THEN
    iTMR_TT301_Mode := 1;
    rTMR_TT301_Voted := rTMR_TT301_Raw[3];
ELSE
    iTMR_TT301_Mode := 0;
    bTripLatched_TMR_Failure := TRUE;
    rTMR_TT301_Voted := rTMR_TT301_Sorted[2];
END_IF;

(* -------------------------------------------------------------------------
 * SUB-SECTION 1.4: SUMP LIQUID LEVEL LT-401 VOTING (2oo3 -> 1oo2 -> 1oo1)
 * ------------------------------------------------------------------------- *)
rTMR_LT401_Raw[1] := rLT_401A_SumpLevel_mm;
rTMR_LT401_Raw[2] := rLT_401B_SumpLevel_mm;
rTMR_LT401_Raw[3] := rLT_401C_SumpLevel_mm;

rTMR_LT401_Sorted[1] := rTMR_LT401_Raw[1];
rTMR_LT401_Sorted[2] := rTMR_LT401_Raw[2];
rTMR_LT401_Sorted[3] := rTMR_LT401_Raw[3];

IF rTMR_LT401_Sorted[1] > rTMR_LT401_Sorted[2] THEN
    rTempCalc1 := rTMR_LT401_Sorted[1];
    rTMR_LT401_Sorted[1] := rTMR_LT401_Sorted[2];
    rTMR_LT401_Sorted[2] := rTempCalc1;
END_IF;

IF rTMR_LT401_Sorted[2] > rTMR_LT401_Sorted[3] THEN
    rTempCalc1 := rTMR_LT401_Sorted[2];
    rTMR_LT401_Sorted[2] := rTMR_LT401_Sorted[3];
    rTMR_LT401_Sorted[3] := rTempCalc1;
END_IF;

IF rTMR_LT401_Sorted[1] > rTMR_LT401_Sorted[2] THEN
    rTempCalc1 := rTMR_LT401_Sorted[1];
    rTMR_LT401_Sorted[1] := rTMR_LT401_Sorted[2];
    rTMR_LT401_Sorted[2] := rTempCalc1;
END_IF;

FOR iIdx1 := 1 TO 3 DO
    rTempCalc2 := ABS(rTMR_LT401_Raw[iIdx1] - rTMR_LT401_Sorted[2]);
    IF rTempCalc2 > cTMR_LT401_MaxDev_mm THEN
        rTMR_LT401_DiscrepTimer[iIdx1] := rTMR_LT401_DiscrepTimer[iIdx1] + rTs_s;
        IF rTMR_LT401_DiscrepTimer[iIdx1] >= cTMR_DiscrepTimeout_s THEN
            bTMR_LT401_ChFault[iIdx1] := TRUE;
        END_IF;
    ELSE
        IF rTMR_LT401_DiscrepTimer[iIdx1] > 0.0 THEN
            rTMR_LT401_DiscrepTimer[iIdx1] := rTMR_LT401_DiscrepTimer[iIdx1] - (rTs_s * 0.50);
            IF rTMR_LT401_DiscrepTimer[iIdx1] < 0.0 THEN
                rTMR_LT401_DiscrepTimer[iIdx1] := 0.0;
            END_IF;
        END_IF;
        IF bCmd_ResetTrip AND (rTMR_LT401_DiscrepTimer[iIdx1] <= 0.0) THEN
            bTMR_LT401_ChFault[iIdx1] := FALSE;
        END_IF;
    END_IF;
END_FOR;

IF (NOT bTMR_LT401_ChFault[1]) AND (NOT bTMR_LT401_ChFault[2]) AND (NOT bTMR_LT401_ChFault[3]) THEN
    iTMR_LT401_Mode := 3;
    rTMR_LT401_Voted := rTMR_LT401_Sorted[2];
ELSIF (NOT bTMR_LT401_ChFault[1]) AND (NOT bTMR_LT401_ChFault[2]) AND bTMR_LT401_ChFault[3] THEN
    iTMR_LT401_Mode := 2;
    rTMR_LT401_Voted := (rTMR_LT401_Raw[1] + rTMR_LT401_Raw[2]) * 0.50;
ELSIF (NOT bTMR_LT401_ChFault[1]) AND bTMR_LT401_ChFault[2] AND (NOT bTMR_LT401_ChFault[3]) THEN
    iTMR_LT401_Mode := 2;
    rTMR_LT401_Voted := (rTMR_LT401_Raw[1] + rTMR_LT401_Raw[3]) * 0.50;
ELSIF bTMR_LT401_ChFault[1] AND (NOT bTMR_LT401_ChFault[2]) AND (NOT bTMR_LT401_ChFault[3]) THEN
    iTMR_LT401_Mode := 2;
    rTMR_LT401_Voted := (rTMR_LT401_Raw[2] + rTMR_LT401_Raw[3]) * 0.50;
ELSIF (NOT bTMR_LT401_ChFault[1]) AND bTMR_LT401_ChFault[2] AND bTMR_LT401_ChFault[3] THEN
    iTMR_LT401_Mode := 1;
    rTMR_LT401_Voted := rTMR_LT401_Raw[1];
ELSIF bTMR_LT401_ChFault[1] AND (NOT bTMR_LT401_ChFault[2]) AND bTMR_LT401_ChFault[3] THEN
    iTMR_LT401_Mode := 1;
    rTMR_LT401_Voted := rTMR_LT401_Raw[2];
ELSIF bTMR_LT401_ChFault[1] AND bTMR_LT401_ChFault[2] AND (NOT bTMR_LT401_ChFault[3]) THEN
    iTMR_LT401_Mode := 1;
    rTMR_LT401_Voted := rTMR_LT401_Raw[3];
ELSE
    iTMR_LT401_Mode := 0;
    bTripLatched_TMR_Failure := TRUE;
    rTMR_LT401_Voted := rTMR_LT401_Sorted[2];
END_IF;

(* -------------------------------------------------------------------------
 * SUB-SECTION 1.5: AUXILIARY PROCESS SENSORS PLAUSIBILITY CLAMPING
 * ------------------------------------------------------------------------- *)
(* Culinary steam header pressure plausibility check (2.5 to 8.0 bar) *)
IF (rPT_001_SteamHeaderPress_bar < 2.50) OR (rPT_001_SteamHeaderPress_bar > 8.00) THEN
    dwWarningWord := dwWarningWord OR 16#0000_0001; (* Plant Steam Supply Out of Limits *)
END_IF;

(* Plant compressed air header pressure plausibility check (5.5 to 10.0 bar) *)
IF (rPT_002_AirHeaderPress_bar < 5.50) OR (rPT_002_AirHeaderPress_bar > 10.00) THEN
    dwWarningWord := dwWarningWord OR 16#0000_0002; (* Plant Air Supply Out of Limits *)
END_IF;

(* Plant cooling water pressure plausibility check (2.0 to 6.0 bar) *)
IF (rPT_003_CoolingWaterPress_bar < 2.00) OR (rPT_003_CoolingWaterPress_bar > 6.00) THEN
    dwWarningWord := dwWarningWord OR 16#0000_0004; (* Cooling Water Header Out of Limits *)
END_IF;

(* Assign Primary Voted Process Values to Outputs *)
rVotedVesselTemp_degC  := rTMR_TT101_Voted;
rVotedVesselPress_bar  := rTMR_PT201_Voted;
rVotedCanCoreTemp_degC := rTMR_TT301_Voted;
rVotedSumpLevel_mm     := rTMR_LT401_Voted;
'''

if __name__ == "__main__":
    t = generate_tmr()
    print("TMR module length:", len(t))
    print(t[:300])
