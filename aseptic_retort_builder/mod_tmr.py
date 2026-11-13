# -*- coding: utf-8 -*-
"""
Module: aseptic_retort_builder/mod_tmr.py
Implements Phase 1: 2oo3 Triple Modular Redundancy (TMR) Sensor Voting Engine
across 4 process instrumentation channels with discrepancy debounce timers and bumpless degradation.
"""

def generate_tmr():
    return '''(* =====================================================================================================================
 * PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANT (TMR) SENSOR VOTING WITH DISCREPANCY TIMERS
 * Safety Architecture: IEC 61508 / ISA-84 SIL-3 Certified Triple Modular Redundancy Strategy
 * Voting Channels:
 *   1. Retort Chamber Dual-Element Class A Pt100 RTDs: rTemp_Sensor1, rTemp_Sensor2, rTemp_Sensor3 [deg C]
 *   2. Retort Shell Piezoresistive Pressure Transmitters: rPress_Sensor1, rPress_Sensor2, rPress_Sensor3 [bar]
 *   3. Vessel Condensate Level Differential Pressure Transmitters: rLevel_Sensor1, rLevel_Sensor2, rLevel_Sensor3 [mm]
 *   4. Container Internal Pressure Wireless Telemetry Transponders: rPouch_Press1, rPouch_Press2, rPouch_Press3 [bar]
 * Degradation Path: 2oo3 (Triplicated Median) -> 1oo2 (Dual Mean) -> 1oo1 (Single Channel) -> 0oo0 (Failsafe Trip)
 * ===================================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------------------------
 * CHANNEL 1: RETORT CHAMBER TEMPERATURE RTDs (rTemp_Sensor1, rTemp_Sensor2, rTemp_Sensor3) [deg C]
 * --------------------------------------------------------------------------------------------------------------------- *)
rTMR_TempRaw[1] := rTemp_Sensor1_degC;
rTMR_TempRaw[2] := rTemp_Sensor2_degC;
rTMR_TempRaw[3] := rTemp_Sensor3_degC;

(* 3-Element Bubble Sort Sorting Network to determine median value *)
rTMR_TempSorted[1] := rTMR_TempRaw[1];
rTMR_TempSorted[2] := rTMR_TempRaw[2];
rTMR_TempSorted[3] := rTMR_TempRaw[3];

IF rTMR_TempSorted[1] > rTMR_TempSorted[2] THEN
    rTempCalc1 := rTMR_TempSorted[1];
    rTMR_TempSorted[1] := rTMR_TempSorted[2];
    rTMR_TempSorted[2] := rTempCalc1;
END_IF;

IF rTMR_TempSorted[2] > rTMR_TempSorted[3] THEN
    rTempCalc1 := rTMR_TempSorted[2];
    rTMR_TempSorted[2] := rTMR_TempSorted[3];
    rTMR_TempSorted[3] := rTempCalc1;
END_IF;

IF rTMR_TempSorted[1] > rTMR_TempSorted[2] THEN
    rTempCalc1 := rTMR_TempSorted[1];
    rTMR_TempSorted[1] := rTMR_TempSorted[2];
    rTMR_TempSorted[2] := rTempCalc1;
END_IF;

(* Individual Channel Deviation Evaluation against Sorted Median *)
FOR iIdx1 := 1 TO 3 DO
    rTempCalc2 := ABS(rTMR_TempRaw[iIdx1] - rTMR_TempSorted[2]);
    IF rTempCalc2 > cTMR_TempMaxDev_degC THEN
        rTMR_TempDiscrepTimer[iIdx1] := rTMR_TempDiscrepTimer[iIdx1] + rTs_s;
        IF rTMR_TempDiscrepTimer[iIdx1] >= cTMR_DiscrepTimeout_s THEN
            bTMR_TempChFault[iIdx1] := TRUE;
        END_IF;
    ELSE
        IF rTMR_TempDiscrepTimer[iIdx1] > 0.0 THEN
            rTMR_TempDiscrepTimer[iIdx1] := rTMR_TempDiscrepTimer[iIdx1] - (rTs_s * 0.50);
            IF rTMR_TempDiscrepTimer[iIdx1] < 0.0 THEN
                rTMR_TempDiscrepTimer[iIdx1] := 0.0;
            END_IF;
        END_IF;
        IF bCmd_EmergencyTripReset AND (rTMR_TempDiscrepTimer[iIdx1] <= 0.0) THEN
            bTMR_TempChFault[iIdx1] := FALSE;
        END_IF;
    END_IF;
END_FOR;

(* Determine Temperature Voting Architecture Degradation Mode *)
IF NOT bTMR_TempChFault[1] AND NOT bTMR_TempChFault[2] AND NOT bTMR_TempChFault[3] THEN
    (* Full 2oo3 Redundancy: Select Perfect Median Element *)
    rVoted_Temp_degC := rTMR_TempSorted[2];
    iTMR_TempMode    := 3;
ELSIF NOT bTMR_TempChFault[1] AND NOT bTMR_TempChFault[2] THEN
    (* 1oo2 Dual Redundancy: Ch1 & Ch2 healthy *)
    rVoted_Temp_degC := (rTMR_TempRaw[1] + rTMR_TempRaw[2]) * 0.50;
    iTMR_TempMode    := 2;
ELSIF NOT bTMR_TempChFault[1] AND NOT bTMR_TempChFault[3] THEN
    (* 1oo2 Dual Redundancy: Ch1 & Ch3 healthy *)
    rVoted_Temp_degC := (rTMR_TempRaw[1] + rTMR_TempRaw[3]) * 0.50;
    iTMR_TempMode    := 2;
ELSIF NOT bTMR_TempChFault[2] AND NOT bTMR_TempChFault[3] THEN
    (* 1oo2 Dual Redundancy: Ch2 & Ch3 healthy *)
    rVoted_Temp_degC := (rTMR_TempRaw[2] + rTMR_TempRaw[3]) * 0.50;
    iTMR_TempMode    := 2;
ELSIF NOT bTMR_TempChFault[1] THEN
    (* 1oo1 Single Channel Degraded: Ch1 only *)
    rVoted_Temp_degC := rTMR_TempRaw[1];
    iTMR_TempMode    := 1;
ELSIF NOT bTMR_TempChFault[2] THEN
    (* 1oo1 Single Channel Degraded: Ch2 only *)
    rVoted_Temp_degC := rTMR_TempRaw[2];
    iTMR_TempMode    := 1;
ELSIF NOT bTMR_TempChFault[3] THEN
    (* 1oo1 Single Channel Degraded: Ch3 only *)
    rVoted_Temp_degC := rTMR_TempRaw[3];
    iTMR_TempMode    := 1;
ELSE
    (* Total Sensor Breakdown: Zero healthy channels -> Failsafe Clamp *)
    rVoted_Temp_degC := 145.0; (* Conservative high clamp triggers overtemp shutdown *)
    iTMR_TempMode    := 0;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * CHANNEL 2: RETORT SHELL PRESSURE TRANSMITTERS (rPress_Sensor1, rPress_Sensor2, rPress_Sensor3) [bar]
 * --------------------------------------------------------------------------------------------------------------------- *)
rTMR_PressRaw[1] := rPress_Sensor1_bar;
rTMR_PressRaw[2] := rPress_Sensor2_bar;
rTMR_PressRaw[3] := rPress_Sensor3_bar;

rTMR_PressSorted[1] := rTMR_PressRaw[1];
rTMR_PressSorted[2] := rTMR_PressRaw[2];
rTMR_PressSorted[3] := rTMR_PressRaw[3];

IF rTMR_PressSorted[1] > rTMR_PressSorted[2] THEN
    rTempCalc1 := rTMR_PressSorted[1];
    rTMR_PressSorted[1] := rTMR_PressSorted[2];
    rTMR_PressSorted[2] := rTempCalc1;
END_IF;

IF rTMR_PressSorted[2] > rTMR_PressSorted[3] THEN
    rTempCalc1 := rTMR_PressSorted[2];
    rTMR_PressSorted[2] := rTMR_PressSorted[3];
    rTMR_PressSorted[3] := rTempCalc1;
END_IF;

IF rTMR_PressSorted[1] > rTMR_PressSorted[2] THEN
    rTempCalc1 := rTMR_PressSorted[1];
    rTMR_PressSorted[1] := rTMR_PressSorted[2];
    rTMR_PressSorted[2] := rTempCalc1;
END_IF;

FOR iIdx1 := 1 TO 3 DO
    rTempCalc2 := ABS(rTMR_PressRaw[iIdx1] - rTMR_PressSorted[2]);
    IF rTempCalc2 > cTMR_PressMaxDev_bar THEN
        rTMR_PressDiscrepTimer[iIdx1] := rTMR_PressDiscrepTimer[iIdx1] + rTs_s;
        IF rTMR_PressDiscrepTimer[iIdx1] >= cTMR_DiscrepTimeout_s THEN
            bTMR_PressChFault[iIdx1] := TRUE;
        END_IF;
    ELSE
        IF rTMR_PressDiscrepTimer[iIdx1] > 0.0 THEN
            rTMR_PressDiscrepTimer[iIdx1] := rTMR_PressDiscrepTimer[iIdx1] - (rTs_s * 0.50);
            IF rTMR_PressDiscrepTimer[iIdx1] < 0.0 THEN
                rTMR_PressDiscrepTimer[iIdx1] := 0.0;
            END_IF;
        END_IF;
        IF bCmd_EmergencyTripReset AND (rTMR_PressDiscrepTimer[iIdx1] <= 0.0) THEN
            bTMR_PressChFault[iIdx1] := FALSE;
        END_IF;
    END_IF;
END_FOR;

IF NOT bTMR_PressChFault[1] AND NOT bTMR_PressChFault[2] AND NOT bTMR_PressChFault[3] THEN
    rVoted_Press_bar := rTMR_PressSorted[2];
    iTMR_PressMode   := 3;
ELSIF NOT bTMR_PressChFault[1] AND NOT bTMR_PressChFault[2] THEN
    rVoted_Press_bar := (rTMR_PressRaw[1] + rTMR_PressRaw[2]) * 0.50;
    iTMR_PressMode   := 2;
ELSIF NOT bTMR_PressChFault[1] AND NOT bTMR_PressChFault[3] THEN
    rVoted_Press_bar := (rTMR_PressRaw[1] + rTMR_PressRaw[3]) * 0.50;
    iTMR_PressMode   := 2;
ELSIF NOT bTMR_PressChFault[2] AND NOT bTMR_PressChFault[3] THEN
    rVoted_Press_bar := (rTMR_PressRaw[2] + rTMR_PressRaw[3]) * 0.50;
    iTMR_PressMode   := 2;
ELSIF NOT bTMR_PressChFault[1] THEN
    rVoted_Press_bar := rTMR_PressRaw[1];
    iTMR_PressMode   := 1;
ELSIF NOT bTMR_PressChFault[2] THEN
    rVoted_Press_bar := rTMR_PressRaw[2];
    iTMR_PressMode   := 1;
ELSIF NOT bTMR_PressChFault[3] THEN
    rVoted_Press_bar := rTMR_PressRaw[3];
    iTMR_PressMode   := 1;
ELSE
    rVoted_Press_bar := 4.50; (* Conservative high pressure clamp *)
    iTMR_PressMode   := 0;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * CHANNEL 3: SUMP CONDENSATE LEVEL TRANSMITTERS (rLevel_Sensor1, rLevel_Sensor2, rLevel_Sensor3) [mm]
 * --------------------------------------------------------------------------------------------------------------------- *)
rTMR_LevelRaw[1] := rLevel_Sensor1_mm;
rTMR_LevelRaw[2] := rLevel_Sensor2_mm;
rTMR_LevelRaw[3] := rLevel_Sensor3_mm;

rTMR_LevelSorted[1] := rTMR_LevelRaw[1];
rTMR_LevelSorted[2] := rTMR_LevelRaw[2];
rTMR_LevelSorted[3] := rTMR_LevelRaw[3];

IF rTMR_LevelSorted[1] > rTMR_LevelSorted[2] THEN
    rTempCalc1 := rTMR_LevelSorted[1];
    rTMR_LevelSorted[1] := rTMR_LevelSorted[2];
    rTMR_LevelSorted[2] := rTempCalc1;
END_IF;

IF rTMR_LevelSorted[2] > rTMR_LevelSorted[3] THEN
    rTempCalc1 := rTMR_LevelSorted[2];
    rTMR_LevelSorted[2] := rTMR_LevelSorted[3];
    rTMR_LevelSorted[3] := rTempCalc1;
END_IF;

IF rTMR_LevelSorted[1] > rTMR_LevelSorted[2] THEN
    rTempCalc1 := rTMR_LevelSorted[1];
    rTMR_LevelSorted[1] := rTMR_LevelSorted[2];
    rTMR_LevelSorted[2] := rTempCalc1;
END_IF;

FOR iIdx1 := 1 TO 3 DO
    rTempCalc2 := ABS(rTMR_LevelRaw[iIdx1] - rTMR_LevelSorted[2]);
    IF rTempCalc2 > cTMR_LevelMaxDev_mm THEN
        rTMR_LevelDiscrepTimer[iIdx1] := rTMR_LevelDiscrepTimer[iIdx1] + rTs_s;
        IF rTMR_LevelDiscrepTimer[iIdx1] >= cTMR_DiscrepTimeout_s THEN
            bTMR_LevelChFault[iIdx1] := TRUE;
        END_IF;
    ELSE
        IF rTMR_LevelDiscrepTimer[iIdx1] > 0.0 THEN
            rTMR_LevelDiscrepTimer[iIdx1] := rTMR_LevelDiscrepTimer[iIdx1] - (rTs_s * 0.50);
            IF rTMR_LevelDiscrepTimer[iIdx1] < 0.0 THEN
                rTMR_LevelDiscrepTimer[iIdx1] := 0.0;
            END_IF;
        END_IF;
        IF bCmd_EmergencyTripReset AND (rTMR_LevelDiscrepTimer[iIdx1] <= 0.0) THEN
            bTMR_LevelChFault[iIdx1] := FALSE;
        END_IF;
    END_IF;
END_FOR;

IF NOT bTMR_LevelChFault[1] AND NOT bTMR_LevelChFault[2] AND NOT bTMR_LevelChFault[3] THEN
    rVoted_Level_mm := rTMR_LevelSorted[2];
    iTMR_LevelMode  := 3;
ELSIF NOT bTMR_LevelChFault[1] AND NOT bTMR_LevelChFault[2] THEN
    rVoted_Level_mm := (rTMR_LevelRaw[1] + rTMR_LevelRaw[2]) * 0.50;
    iTMR_LevelMode  := 2;
ELSIF NOT bTMR_LevelChFault[1] AND NOT bTMR_LevelChFault[3] THEN
    rVoted_Level_mm := (rTMR_LevelRaw[1] + rTMR_LevelRaw[3]) * 0.50;
    iTMR_LevelMode  := 2;
ELSIF NOT bTMR_LevelChFault[2] AND NOT bTMR_LevelChFault[3] THEN
    rVoted_Level_mm := (rTMR_LevelRaw[2] + rTMR_LevelRaw[3]) * 0.50;
    iTMR_LevelMode  := 2;
ELSIF NOT bTMR_LevelChFault[1] THEN
    rVoted_Level_mm := rTMR_LevelRaw[1];
    iTMR_LevelMode  := 1;
ELSIF NOT bTMR_LevelChFault[2] THEN
    rVoted_Level_mm := rTMR_LevelRaw[2];
    iTMR_LevelMode  := 1;
ELSIF NOT bTMR_LevelChFault[3] THEN
    rVoted_Level_mm := rTMR_LevelRaw[3];
    iTMR_LevelMode  := 1;
ELSE
    rVoted_Level_mm := 400.0; (* Conservative flooding clamp *)
    iTMR_LevelMode  := 0;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * CHANNEL 4: CONTAINER INTERNAL PRESSURE WIRELESS TELEMETRY (rPouch_Press1, rPouch_Press2, rPouch_Press3) [bar]
 * --------------------------------------------------------------------------------------------------------------------- *)
rTMR_PouchRaw[1] := rPouch_Press1_bar;
rTMR_PouchRaw[2] := rPouch_Press2_bar;
rTMR_PouchRaw[3] := rPouch_Press3_bar;

rTMR_PouchSorted[1] := rTMR_PouchRaw[1];
rTMR_PouchSorted[2] := rTMR_PouchRaw[2];
rTMR_PouchSorted[3] := rTMR_PouchRaw[3];

IF rTMR_PouchSorted[1] > rTMR_PouchSorted[2] THEN
    rTempCalc1 := rTMR_PouchSorted[1];
    rTMR_PouchSorted[1] := rTMR_PouchSorted[2];
    rTMR_PouchSorted[2] := rTempCalc1;
END_IF;

IF rTMR_PouchSorted[2] > rTMR_PouchSorted[3] THEN
    rTempCalc1 := rTMR_PouchSorted[2];
    rTMR_PouchSorted[2] := rTMR_PouchSorted[3];
    rTMR_PouchSorted[3] := rTempCalc1;
END_IF;

IF rTMR_PouchSorted[1] > rTMR_PouchSorted[2] THEN
    rTempCalc1 := rTMR_PouchSorted[1];
    rTMR_PouchSorted[1] := rTMR_PouchSorted[2];
    rTMR_PouchSorted[2] := rTempCalc1;
END_IF;

FOR iIdx1 := 1 TO 3 DO
    rTempCalc2 := ABS(rTMR_PouchRaw[iIdx1] - rTMR_PouchSorted[2]);
    IF rTempCalc2 > cTMR_PouchMaxDev_bar THEN
        rTMR_PouchDiscrepTimer[iIdx1] := rTMR_PouchDiscrepTimer[iIdx1] + rTs_s;
        IF rTMR_PouchDiscrepTimer[iIdx1] >= cTMR_DiscrepTimeout_s THEN
            bTMR_PouchChFault[iIdx1] := TRUE;
        END_IF;
    ELSE
        IF rTMR_PouchDiscrepTimer[iIdx1] > 0.0 THEN
            rTMR_PouchDiscrepTimer[iIdx1] := rTMR_PouchDiscrepTimer[iIdx1] - (rTs_s * 0.50);
            IF rTMR_PouchDiscrepTimer[iIdx1] < 0.0 THEN
                rTMR_PouchDiscrepTimer[iIdx1] := 0.0;
            END_IF;
        END_IF;
        IF bCmd_EmergencyTripReset AND (rTMR_PouchDiscrepTimer[iIdx1] <= 0.0) THEN
            bTMR_PouchChFault[iIdx1] := FALSE;
        END_IF;
    END_IF;
END_FOR;

IF NOT bTMR_PouchChFault[1] AND NOT bTMR_PouchChFault[2] AND NOT bTMR_PouchChFault[3] THEN
    rVoted_PouchPress_bar := rTMR_PouchSorted[2];
    iTMR_PouchMode        := 3;
ELSIF NOT bTMR_PouchChFault[1] AND NOT bTMR_PouchChFault[2] THEN
    rVoted_PouchPress_bar := (rTMR_PouchRaw[1] + rTMR_PouchRaw[2]) * 0.50;
    iTMR_PouchMode        := 2;
ELSIF NOT bTMR_PouchChFault[1] AND NOT bTMR_PouchChFault[3] THEN
    rVoted_PouchPress_bar := (rTMR_PouchRaw[1] + rTMR_PouchRaw[3]) * 0.50;
    iTMR_PouchMode        := 2;
ELSIF NOT bTMR_PouchChFault[2] AND NOT bTMR_PouchChFault[3] THEN
    rVoted_PouchPress_bar := (rTMR_PouchRaw[2] + rTMR_PouchRaw[3]) * 0.50;
    iTMR_PouchMode        := 2;
ELSIF NOT bTMR_PouchChFault[1] THEN
    rVoted_PouchPress_bar := rTMR_PouchRaw[1];
    iTMR_PouchMode        := 1;
ELSIF NOT bTMR_PouchChFault[2] THEN
    rVoted_PouchPress_bar := rTMR_PouchRaw[2];
    iTMR_PouchMode        := 1;
ELSIF NOT bTMR_PouchChFault[3] THEN
    rVoted_PouchPress_bar := rTMR_PouchRaw[3];
    iTMR_PouchMode        := 1;
ELSE
    (* Fallback to First-Principles Thermodynamic Analytical Model if all telemetry tags lost *)
    rVoted_PouchPress_bar := rTotalEstimatedPcan_bar;
    iTMR_PouchMode        := 0;
END_IF;'''
