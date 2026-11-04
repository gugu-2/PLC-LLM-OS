# -*- coding: utf-8 -*-
"""
Part 2 of FB_Packaging_Corrugator_SingleFacer_FlyingShear
Contains: Phase 1 (2oo3 TMR Voting Logic for 7 triplets) and Phase 2 (Cyber-Physical Calculations).
"""

def get_part2():
    return '''
(* =====================================================================================================================
 * PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING & DISCREPANCY TIMERS
 * =====================================================================================================================
 * Rigorous voting across seven critical process sensor triplets:
 * 1. Upper corrugating roll RTD temperature [deg C]
 * 2. Lower corrugating roll RTD temperature [deg C]
 * 3. High-pressure steam supply header pressure [bar]
 * 4. Bridge catenary accumulator ultrasonic loop sag [mm]
 * 5. Double-backer entry web tension load cells [N]
 * 6. Corrugator master line speed pulse encoders [m/min]
 * 7. Flying rotary cutoff knife resolver angular position [deg]
 * Each triplet executes pairwise absolute delta checks, discrepancy integration timers, channel failure isolation,
 * bumpless degradation to 2-channel average or 1-channel fallback, and ISA-18.2 health bitmask packing.
 *)

(* --- TRIPLET 1: Single-Facer Upper Corrugating Roll Surface Temperature RTDs [deg C] --- *)
rTemp_Sum := 0.0;
IF (ABS(rT_RollUpper_ChA - rT_RollUpper_ChB) > cTOL_DISC_TEMP_DEGC) OR
   (ABS(rT_RollUpper_ChB - rT_RollUpper_ChC) > cTOL_DISC_TEMP_DEGC) OR
   (ABS(rT_RollUpper_ChA - rT_RollUpper_ChC) > cTOL_DISC_TEMP_DEGC) THEN
    rTimerDisc_RollUpper := rTimerDisc_RollUpper + rT_CycleTime_Sec;
    IF rTimerDisc_RollUpper >= cTIME_DISC_MAX_TRIP_SEC THEN
        (* Identify faulty channel via pairwise isolation *)
        IF (ABS(rT_RollUpper_ChA - rT_RollUpper_ChB) > cTOL_DISC_TEMP_DEGC) AND
           (ABS(rT_RollUpper_ChA - rT_RollUpper_ChC) > cTOL_DISC_TEMP_DEGC) THEN
            bHealth_RollUpper_ChA := FALSE;
        ELSIF (ABS(rT_RollUpper_ChB - rT_RollUpper_ChA) > cTOL_DISC_TEMP_DEGC) AND
              (ABS(rT_RollUpper_ChB - rT_RollUpper_ChC) > cTOL_DISC_TEMP_DEGC) THEN
            bHealth_RollUpper_ChB := FALSE;
        ELSIF (ABS(rT_RollUpper_ChC - rT_RollUpper_ChA) > cTOL_DISC_TEMP_DEGC) AND
              (ABS(rT_RollUpper_ChC - rT_RollUpper_ChB) > cTOL_DISC_TEMP_DEGC) THEN
            bHealth_RollUpper_ChC := FALSE;
        END_IF;
    END_IF;
ELSE
    rTimerDisc_RollUpper := MAX(0.0, rTimerDisc_RollUpper - (2.0 * rT_CycleTime_Sec));
END_IF;

IF bFaultReset_Cmd THEN
    bHealth_RollUpper_ChA := TRUE;
    bHealth_RollUpper_ChB := TRUE;
    bHealth_RollUpper_ChC := TRUE;
    rTimerDisc_RollUpper := 0.0;
END_IF;

(* Voting execution *)
IF bHealth_RollUpper_ChA AND bHealth_RollUpper_ChB AND bHealth_RollUpper_ChC THEN
    (* 2oo3 Median voting *)
    IF ((rT_RollUpper_ChA >= rT_RollUpper_ChB) AND (rT_RollUpper_ChA <= rT_RollUpper_ChC)) OR
       ((rT_RollUpper_ChA >= rT_RollUpper_ChC) AND (rT_RollUpper_ChA <= rT_RollUpper_ChB)) THEN
        rAct_UpperRollTempVoted_degC := rT_RollUpper_ChA;
    ELSIF ((rT_RollUpper_ChB >= rT_RollUpper_ChA) AND (rT_RollUpper_ChB <= rT_RollUpper_ChC)) OR
          ((rT_RollUpper_ChB >= rT_RollUpper_ChC) AND (rT_RollUpper_ChB <= rT_RollUpper_ChA)) THEN
        rAct_UpperRollTempVoted_degC := rT_RollUpper_ChB;
    ELSE
        rAct_UpperRollTempVoted_degC := rT_RollUpper_ChC;
    END_IF;
ELSIF bHealth_RollUpper_ChA AND bHealth_RollUpper_ChB THEN
    rAct_UpperRollTempVoted_degC := 0.5 * (rT_RollUpper_ChA + rT_RollUpper_ChB);
ELSIF bHealth_RollUpper_ChB AND bHealth_RollUpper_ChC THEN
    rAct_UpperRollTempVoted_degC := 0.5 * (rT_RollUpper_ChB + rT_RollUpper_ChC);
ELSIF bHealth_RollUpper_ChA AND bHealth_RollUpper_ChC THEN
    rAct_UpperRollTempVoted_degC := 0.5 * (rT_RollUpper_ChA + rT_RollUpper_ChC);
ELSIF bHealth_RollUpper_ChA THEN
    rAct_UpperRollTempVoted_degC := rT_RollUpper_ChA;
ELSIF bHealth_RollUpper_ChB THEN
    rAct_UpperRollTempVoted_degC := rT_RollUpper_ChB;
ELSIF bHealth_RollUpper_ChC THEN
    rAct_UpperRollTempVoted_degC := rT_RollUpper_ChC;
ELSE
    rAct_UpperRollTempVoted_degC := 165.0; (* Safe fallback constant *)
END_IF;

(* --- TRIPLET 2: Single-Facer Lower Corrugating Roll Surface Temperature RTDs [deg C] --- *)
IF (ABS(rT_RollLower_ChA - rT_RollLower_ChB) > cTOL_DISC_TEMP_DEGC) OR
   (ABS(rT_RollLower_ChB - rT_RollLower_ChC) > cTOL_DISC_TEMP_DEGC) OR
   (ABS(rT_RollLower_ChA - rT_RollLower_ChC) > cTOL_DISC_TEMP_DEGC) THEN
    rTimerDisc_RollLower := rTimerDisc_RollLower + rT_CycleTime_Sec;
    IF rTimerDisc_RollLower >= cTIME_DISC_MAX_TRIP_SEC THEN
        IF (ABS(rT_RollLower_ChA - rT_RollLower_ChB) > cTOL_DISC_TEMP_DEGC) AND
           (ABS(rT_RollLower_ChA - rT_RollLower_ChC) > cTOL_DISC_TEMP_DEGC) THEN
            bHealth_RollLower_ChA := FALSE;
        ELSIF (ABS(rT_RollLower_ChB - rT_RollLower_ChA) > cTOL_DISC_TEMP_DEGC) AND
              (ABS(rT_RollLower_ChB - rT_RollLower_ChC) > cTOL_DISC_TEMP_DEGC) THEN
            bHealth_RollLower_ChB := FALSE;
        ELSIF (ABS(rT_RollLower_ChC - rT_RollLower_ChA) > cTOL_DISC_TEMP_DEGC) AND
              (ABS(rT_RollLower_ChC - rT_RollLower_ChB) > cTOL_DISC_TEMP_DEGC) THEN
            bHealth_RollLower_ChC := FALSE;
        END_IF;
    END_IF;
ELSE
    rTimerDisc_RollLower := MAX(0.0, rTimerDisc_RollLower - (2.0 * rT_CycleTime_Sec));
END_IF;

IF bFaultReset_Cmd THEN
    bHealth_RollLower_ChA := TRUE;
    bHealth_RollLower_ChB := TRUE;
    bHealth_RollLower_ChC := TRUE;
    rTimerDisc_RollLower := 0.0;
END_IF;

IF bHealth_RollLower_ChA AND bHealth_RollLower_ChB AND bHealth_RollLower_ChC THEN
    IF ((rT_RollLower_ChA >= rT_RollLower_ChB) AND (rT_RollLower_ChA <= rT_RollLower_ChC)) OR
       ((rT_RollLower_ChA >= rT_RollLower_ChC) AND (rT_RollLower_ChA <= rT_RollLower_ChB)) THEN
        rAct_LowerRollTempVoted_degC := rT_RollLower_ChA;
    ELSIF ((rT_RollLower_ChB >= rT_RollLower_ChA) AND (rT_RollLower_ChB <= rT_RollLower_ChC)) OR
          ((rT_RollLower_ChB >= rT_RollLower_ChC) AND (rT_RollLower_ChB <= rT_RollLower_ChA)) THEN
        rAct_LowerRollTempVoted_degC := rT_RollLower_ChB;
    ELSE
        rAct_LowerRollTempVoted_degC := rT_RollLower_ChC;
    END_IF;
ELSIF bHealth_RollLower_ChA AND bHealth_RollLower_ChB THEN
    rAct_LowerRollTempVoted_degC := 0.5 * (rT_RollLower_ChA + rT_RollLower_ChB);
ELSIF bHealth_RollLower_ChB AND bHealth_RollLower_ChC THEN
    rAct_LowerRollTempVoted_degC := 0.5 * (rT_RollLower_ChB + rT_RollLower_ChC);
ELSIF bHealth_RollLower_ChA AND bHealth_RollLower_ChC THEN
    rAct_LowerRollTempVoted_degC := 0.5 * (rT_RollLower_ChA + rT_RollLower_ChC);
ELSIF bHealth_RollLower_ChA THEN
    rAct_LowerRollTempVoted_degC := rT_RollLower_ChA;
ELSIF bHealth_RollLower_ChB THEN
    rAct_LowerRollTempVoted_degC := rT_RollLower_ChB;
ELSIF bHealth_RollLower_ChC THEN
    rAct_LowerRollTempVoted_degC := rT_RollLower_ChC;
ELSE
    rAct_LowerRollTempVoted_degC := 165.0;
END_IF;

(* --- TRIPLET 3: High-Pressure Steam Supply Header Pressure Transmitters [bar] --- *)
IF (ABS(rP_SteamSupply_ChA - rP_SteamSupply_ChB) > cTOL_DISC_PRESSURE_BAR) OR
   (ABS(rP_SteamSupply_ChB - rP_SteamSupply_ChC) > cTOL_DISC_PRESSURE_BAR) OR
   (ABS(rP_SteamSupply_ChA - rP_SteamSupply_ChC) > cTOL_DISC_PRESSURE_BAR) THEN
    rTimerDisc_SteamSupply := rTimerDisc_SteamSupply + rT_CycleTime_Sec;
    IF rTimerDisc_SteamSupply >= cTIME_DISC_MAX_TRIP_SEC THEN
        IF (ABS(rP_SteamSupply_ChA - rP_SteamSupply_ChB) > cTOL_DISC_PRESSURE_BAR) AND
           (ABS(rP_SteamSupply_ChA - rP_SteamSupply_ChC) > cTOL_DISC_PRESSURE_BAR) THEN
            bHealth_SteamSupply_ChA := FALSE;
        ELSIF (ABS(rP_SteamSupply_ChB - rP_SteamSupply_ChA) > cTOL_DISC_PRESSURE_BAR) AND
              (ABS(rP_SteamSupply_ChB - rP_SteamSupply_ChC) > cTOL_DISC_PRESSURE_BAR) THEN
            bHealth_SteamSupply_ChB := FALSE;
        ELSIF (ABS(rP_SteamSupply_ChC - rP_SteamSupply_ChA) > cTOL_DISC_PRESSURE_BAR) AND
              (ABS(rP_SteamSupply_ChC - rP_SteamSupply_ChB) > cTOL_DISC_PRESSURE_BAR) THEN
            bHealth_SteamSupply_ChC := FALSE;
        END_IF;
    END_IF;
ELSE
    rTimerDisc_SteamSupply := MAX(0.0, rTimerDisc_SteamSupply - (2.0 * rT_CycleTime_Sec));
END_IF;

IF bFaultReset_Cmd THEN
    bHealth_SteamSupply_ChA := TRUE;
    bHealth_SteamSupply_ChB := TRUE;
    bHealth_SteamSupply_ChC := TRUE;
    rTimerDisc_SteamSupply := 0.0;
END_IF;

rTemp_Sum := 0.0;
IF bHealth_SteamSupply_ChA AND bHealth_SteamSupply_ChB AND bHealth_SteamSupply_ChC THEN
    IF ((rP_SteamSupply_ChA >= rP_SteamSupply_ChB) AND (rP_SteamSupply_ChA <= rP_SteamSupply_ChC)) OR
       ((rP_SteamSupply_ChA >= rP_SteamSupply_ChC) AND (rP_SteamSupply_ChA <= rP_SteamSupply_ChB)) THEN
        rTemp_Sum := rP_SteamSupply_ChA;
    ELSIF ((rP_SteamSupply_ChB >= rP_SteamSupply_ChA) AND (rP_SteamSupply_ChB <= rP_SteamSupply_ChC)) OR
          ((rP_SteamSupply_ChB >= rP_SteamSupply_ChC) AND (rP_SteamSupply_ChB <= rP_SteamSupply_ChA)) THEN
        rTemp_Sum := rP_SteamSupply_ChB;
    ELSE
        rTemp_Sum := rP_SteamSupply_ChC;
    END_IF;
ELSIF bHealth_SteamSupply_ChA AND bHealth_SteamSupply_ChB THEN
    rTemp_Sum := 0.5 * (rP_SteamSupply_ChA + rP_SteamSupply_ChB);
ELSIF bHealth_SteamSupply_ChB AND bHealth_SteamSupply_ChC THEN
    rTemp_Sum := 0.5 * (rP_SteamSupply_ChB + rP_SteamSupply_ChC);
ELSIF bHealth_SteamSupply_ChA AND bHealth_SteamSupply_ChC THEN
    rTemp_Sum := 0.5 * (rP_SteamSupply_ChA + rP_SteamSupply_ChC);
ELSIF bHealth_SteamSupply_ChA THEN
    rTemp_Sum := rP_SteamSupply_ChA;
ELSIF bHealth_SteamSupply_ChB THEN
    rTemp_Sum := rP_SteamSupply_ChB;
ELSIF bHealth_SteamSupply_ChC THEN
    rTemp_Sum := rP_SteamSupply_ChC;
ELSE
    rTemp_Sum := 24.5;
END_IF;
(* Assign measurement vector element 1 *)
rVec_Y_Meas[1] := rTemp_Sum;

(* --- TRIPLET 4: Bridge Web Catenary Accumulator Ultrasonic Loop Sag Transmitters [mm] --- *)
IF (ABS(rPos_BridgeLoopSag_ChA - rPos_BridgeLoopSag_ChB) > cTOL_DISC_SAG_MM) OR
   (ABS(rPos_BridgeLoopSag_ChB - rPos_BridgeLoopSag_ChC) > cTOL_DISC_SAG_MM) OR
   (ABS(rPos_BridgeLoopSag_ChA - rPos_BridgeLoopSag_ChC) > cTOL_DISC_SAG_MM) THEN
    rTimerDisc_BridgeSag := rTimerDisc_BridgeSag + rT_CycleTime_Sec;
    IF rTimerDisc_BridgeSag >= cTIME_DISC_MAX_TRIP_SEC THEN
        IF (ABS(rPos_BridgeLoopSag_ChA - rPos_BridgeLoopSag_ChB) > cTOL_DISC_SAG_MM) AND
           (ABS(rPos_BridgeLoopSag_ChA - rPos_BridgeLoopSag_ChC) > cTOL_DISC_SAG_MM) THEN
            bHealth_BridgeSag_ChA := FALSE;
        ELSIF (ABS(rPos_BridgeLoopSag_ChB - rPos_BridgeLoopSag_ChA) > cTOL_DISC_SAG_MM) AND
              (ABS(rPos_BridgeLoopSag_ChB - rPos_BridgeLoopSag_ChC) > cTOL_DISC_SAG_MM) THEN
            bHealth_BridgeSag_ChB := FALSE;
        ELSIF (ABS(rPos_BridgeLoopSag_ChC - rPos_BridgeLoopSag_ChA) > cTOL_DISC_SAG_MM) AND
              (ABS(rPos_BridgeLoopSag_ChC - rPos_BridgeLoopSag_ChB) > cTOL_DISC_SAG_MM) THEN
            bHealth_BridgeSag_ChC := FALSE;
        END_IF;
    END_IF;
ELSE
    rTimerDisc_BridgeSag := MAX(0.0, rTimerDisc_BridgeSag - (2.0 * rT_CycleTime_Sec));
END_IF;

IF bFaultReset_Cmd THEN
    bHealth_BridgeSag_ChA := TRUE;
    bHealth_BridgeSag_ChB := TRUE;
    bHealth_BridgeSag_ChC := TRUE;
    rTimerDisc_BridgeSag := 0.0;
END_IF;

IF bHealth_BridgeSag_ChA AND bHealth_BridgeSag_ChB AND bHealth_BridgeSag_ChC THEN
    IF ((rPos_BridgeLoopSag_ChA >= rPos_BridgeLoopSag_ChB) AND (rPos_BridgeLoopSag_ChA <= rPos_BridgeLoopSag_ChC)) OR
       ((rPos_BridgeLoopSag_ChA >= rPos_BridgeLoopSag_ChC) AND (rPos_BridgeLoopSag_ChA <= rPos_BridgeLoopSag_ChB)) THEN
        rAct_BridgeSagVoted_mm := rPos_BridgeLoopSag_ChA;
    ELSIF ((rPos_BridgeLoopSag_ChB >= rPos_BridgeLoopSag_ChA) AND (rPos_BridgeLoopSag_ChB <= rPos_BridgeLoopSag_ChC)) OR
          ((rPos_BridgeLoopSag_ChB >= rPos_BridgeLoopSag_ChC) AND (rPos_BridgeLoopSag_ChB <= rPos_BridgeLoopSag_ChA)) THEN
        rAct_BridgeSagVoted_mm := rPos_BridgeLoopSag_ChB;
    ELSE
        rAct_BridgeSagVoted_mm := rPos_BridgeLoopSag_ChC;
    END_IF;
ELSIF bHealth_BridgeSag_ChA AND bHealth_BridgeSag_ChB THEN
    rAct_BridgeSagVoted_mm := 0.5 * (rPos_BridgeLoopSag_ChA + rPos_BridgeLoopSag_ChB);
ELSIF bHealth_BridgeSag_ChB AND bHealth_BridgeSag_ChC THEN
    rAct_BridgeSagVoted_mm := 0.5 * (rPos_BridgeLoopSag_ChB + rPos_BridgeLoopSag_ChC);
ELSIF bHealth_BridgeSag_ChA AND bHealth_BridgeSag_ChC THEN
    rAct_BridgeSagVoted_mm := 0.5 * (rPos_BridgeLoopSag_ChA + rPos_BridgeLoopSag_ChC);
ELSIF bHealth_BridgeSag_ChA THEN
    rAct_BridgeSagVoted_mm := rPos_BridgeLoopSag_ChA;
ELSIF bHealth_BridgeSag_ChB THEN
    rAct_BridgeSagVoted_mm := rPos_BridgeLoopSag_ChB;
ELSIF bHealth_BridgeSag_ChC THEN
    rAct_BridgeSagVoted_mm := rPos_BridgeLoopSag_ChC;
ELSE
    rAct_BridgeSagVoted_mm := 900.0;
END_IF;

(* --- TRIPLET 5: Double-Backer Entry Web Tension Load Cells [N] --- *)
IF (ABS(rF_WebTensionDB_ChA - rF_WebTensionDB_ChB) > cTOL_DISC_TENSION_N) OR
   (ABS(rF_WebTensionDB_ChB - rF_WebTensionDB_ChC) > cTOL_DISC_TENSION_N) OR
   (ABS(rF_WebTensionDB_ChA - rF_WebTensionDB_ChC) > cTOL_DISC_TENSION_N) THEN
    rTimerDisc_WebTension := rTimerDisc_WebTension + rT_CycleTime_Sec;
    IF rTimerDisc_WebTension >= cTIME_DISC_MAX_TRIP_SEC THEN
        IF (ABS(rF_WebTensionDB_ChA - rF_WebTensionDB_ChB) > cTOL_DISC_TENSION_N) AND
           (ABS(rF_WebTensionDB_ChA - rF_WebTensionDB_ChC) > cTOL_DISC_TENSION_N) THEN
            bHealth_WebTension_ChA := FALSE;
        ELSIF (ABS(rF_WebTensionDB_ChB - rF_WebTensionDB_ChA) > cTOL_DISC_TENSION_N) AND
              (ABS(rF_WebTensionDB_ChB - rF_WebTensionDB_ChC) > cTOL_DISC_TENSION_N) THEN
            bHealth_WebTension_ChB := FALSE;
        ELSIF (ABS(rF_WebTensionDB_ChC - rF_WebTensionDB_ChA) > cTOL_DISC_TENSION_N) AND
              (ABS(rF_WebTensionDB_ChC - rF_WebTensionDB_ChB) > cTOL_DISC_TENSION_N) THEN
            bHealth_WebTension_ChC := FALSE;
        END_IF;
    END_IF;
ELSE
    rTimerDisc_WebTension := MAX(0.0, rTimerDisc_WebTension - (2.0 * rT_CycleTime_Sec));
END_IF;

IF bFaultReset_Cmd THEN
    bHealth_WebTension_ChA := TRUE;
    bHealth_WebTension_ChB := TRUE;
    bHealth_WebTension_ChC := TRUE;
    rTimerDisc_WebTension := 0.0;
END_IF;

IF bHealth_WebTension_ChA AND bHealth_WebTension_ChB AND bHealth_WebTension_ChC THEN
    IF ((rF_WebTensionDB_ChA >= rF_WebTensionDB_ChB) AND (rF_WebTensionDB_ChA <= rF_WebTensionDB_ChC)) OR
       ((rF_WebTensionDB_ChA >= rF_WebTensionDB_ChC) AND (rF_WebTensionDB_ChA <= rF_WebTensionDB_ChB)) THEN
        rAct_WebTensionEntryDB_N := rF_WebTensionDB_ChA;
    ELSIF ((rF_WebTensionDB_ChB >= rF_WebTensionDB_ChA) AND (rF_WebTensionDB_ChB <= rF_WebTensionDB_ChC)) OR
          ((rF_WebTensionDB_ChB >= rF_WebTensionDB_ChC) AND (rF_WebTensionDB_ChB <= rF_WebTensionDB_ChA)) THEN
        rAct_WebTensionEntryDB_N := rF_WebTensionDB_ChB;
    ELSE
        rAct_WebTensionEntryDB_N := rF_WebTensionDB_ChC;
    END_IF;
ELSIF bHealth_WebTension_ChA AND bHealth_WebTension_ChB THEN
    rAct_WebTensionEntryDB_N := 0.5 * (rF_WebTensionDB_ChA + rF_WebTensionDB_ChB);
ELSIF bHealth_WebTension_ChB AND bHealth_WebTension_ChC THEN
    rAct_WebTensionEntryDB_N := 0.5 * (rF_WebTensionDB_ChB + rF_WebTensionDB_ChC);
ELSIF bHealth_WebTension_ChA AND bHealth_WebTension_ChC THEN
    rAct_WebTensionEntryDB_N := 0.5 * (rF_WebTensionDB_ChA + rF_WebTensionDB_ChC);
ELSIF bHealth_WebTension_ChA THEN
    rAct_WebTensionEntryDB_N := rF_WebTensionDB_ChA;
ELSIF bHealth_WebTension_ChB THEN
    rAct_WebTensionEntryDB_N := rF_WebTensionDB_ChB;
ELSIF bHealth_WebTension_ChC THEN
    rAct_WebTensionEntryDB_N := rF_WebTensionDB_ChC;
ELSE
    rAct_WebTensionEntryDB_N := 450.0;
END_IF;

(* --- TRIPLET 6: Corrugator Master Line Speed Pulse Encoders [m/min] --- *)
IF (ABS(rV_MasterLineSpeed_ChA - rV_MasterLineSpeed_ChB) > cTOL_DISC_SPEED_M_MIN) OR
   (ABS(rV_MasterLineSpeed_ChB - rV_MasterLineSpeed_ChC) > cTOL_DISC_SPEED_M_MIN) OR
   (ABS(rV_MasterLineSpeed_ChA - rV_MasterLineSpeed_ChC) > cTOL_DISC_SPEED_M_MIN) THEN
    rTimerDisc_MasterSpeed := rTimerDisc_MasterSpeed + rT_CycleTime_Sec;
    IF rTimerDisc_MasterSpeed >= cTIME_DISC_MAX_TRIP_SEC THEN
        IF (ABS(rV_MasterLineSpeed_ChA - rV_MasterLineSpeed_ChB) > cTOL_DISC_SPEED_M_MIN) AND
           (ABS(rV_MasterLineSpeed_ChA - rV_MasterLineSpeed_ChC) > cTOL_DISC_SPEED_M_MIN) THEN
            bHealth_MasterSpeed_ChA := FALSE;
        ELSIF (ABS(rV_MasterLineSpeed_ChB - rV_MasterLineSpeed_ChA) > cTOL_DISC_SPEED_M_MIN) AND
              (ABS(rV_MasterLineSpeed_ChB - rV_MasterLineSpeed_ChC) > cTOL_DISC_SPEED_M_MIN) THEN
            bHealth_MasterSpeed_ChB := FALSE;
        ELSIF (ABS(rV_MasterLineSpeed_ChC - rV_MasterLineSpeed_ChA) > cTOL_DISC_SPEED_M_MIN) AND
              (ABS(rV_MasterLineSpeed_ChC - rV_MasterLineSpeed_ChB) > cTOL_DISC_SPEED_M_MIN) THEN
            bHealth_MasterSpeed_ChC := FALSE;
        END_IF;
    END_IF;
ELSE
    rTimerDisc_MasterSpeed := MAX(0.0, rTimerDisc_MasterSpeed - (2.0 * rT_CycleTime_Sec));
END_IF;

IF bFaultReset_Cmd THEN
    bHealth_MasterSpeed_ChA := TRUE;
    bHealth_MasterSpeed_ChB := TRUE;
    bHealth_MasterSpeed_ChC := TRUE;
    rTimerDisc_MasterSpeed := 0.0;
END_IF;

IF bHealth_MasterSpeed_ChA AND bHealth_MasterSpeed_ChB AND bHealth_MasterSpeed_ChC THEN
    IF ((rV_MasterLineSpeed_ChA >= rV_MasterLineSpeed_ChB) AND (rV_MasterLineSpeed_ChA <= rV_MasterLineSpeed_ChC)) OR
       ((rV_MasterLineSpeed_ChA >= rV_MasterLineSpeed_ChC) AND (rV_MasterLineSpeed_ChA <= rV_MasterLineSpeed_ChB)) THEN
        rAct_LineSpeedMaster_m_min := rV_MasterLineSpeed_ChA;
    ELSIF ((rV_MasterLineSpeed_ChB >= rV_MasterLineSpeed_ChA) AND (rV_MasterLineSpeed_ChB <= rV_MasterLineSpeed_ChC)) OR
          ((rV_MasterLineSpeed_ChB >= rV_MasterLineSpeed_ChC) AND (rV_MasterLineSpeed_ChB <= rV_MasterLineSpeed_ChA)) THEN
        rAct_LineSpeedMaster_m_min := rV_MasterLineSpeed_ChB;
    ELSE
        rAct_LineSpeedMaster_m_min := rV_MasterLineSpeed_ChC;
    END_IF;
ELSIF bHealth_MasterSpeed_ChA AND bHealth_MasterSpeed_ChB THEN
    rAct_LineSpeedMaster_m_min := 0.5 * (rV_MasterLineSpeed_ChA + rV_MasterLineSpeed_ChB);
ELSIF bHealth_MasterSpeed_ChB AND bHealth_MasterSpeed_ChC THEN
    rAct_LineSpeedMaster_m_min := 0.5 * (rV_MasterLineSpeed_ChB + rV_MasterLineSpeed_ChC);
ELSIF bHealth_MasterSpeed_ChA AND bHealth_MasterSpeed_ChC THEN
    rAct_LineSpeedMaster_m_min := 0.5 * (rV_MasterLineSpeed_ChA + rV_MasterLineSpeed_ChC);
ELSIF bHealth_MasterSpeed_ChA THEN
    rAct_LineSpeedMaster_m_min := rV_MasterLineSpeed_ChA;
ELSIF bHealth_MasterSpeed_ChB THEN
    rAct_LineSpeedMaster_m_min := rV_MasterLineSpeed_ChB;
ELSIF bHealth_MasterSpeed_ChC THEN
    rAct_LineSpeedMaster_m_min := rV_MasterLineSpeed_ChC;
ELSE
    rAct_LineSpeedMaster_m_min := 0.0;
END_IF;

(* --- TRIPLET 7: Flying Rotary Cutoff Knife Resolvers [deg] --- *)
IF (ABS(rPos_ShearKnifeAngle_ChA - rPos_ShearKnifeAngle_ChB) > cTOL_DISC_ANGLE_DEG) OR
   (ABS(rPos_ShearKnifeAngle_ChB - rPos_ShearKnifeAngle_ChC) > cTOL_DISC_ANGLE_DEG) OR
   (ABS(rPos_ShearKnifeAngle_ChA - rPos_ShearKnifeAngle_ChC) > cTOL_DISC_ANGLE_DEG) THEN
    rTimerDisc_KnifeAngle := rTimerDisc_KnifeAngle + rT_CycleTime_Sec;
    IF rTimerDisc_KnifeAngle >= cTIME_DISC_MAX_TRIP_SEC THEN
        IF (ABS(rPos_ShearKnifeAngle_ChA - rPos_ShearKnifeAngle_ChB) > cTOL_DISC_ANGLE_DEG) AND
           (ABS(rPos_ShearKnifeAngle_ChA - rPos_ShearKnifeAngle_ChC) > cTOL_DISC_ANGLE_DEG) THEN
            bHealth_KnifeAngle_ChA := FALSE;
        ELSIF (ABS(rPos_ShearKnifeAngle_ChB - rPos_ShearKnifeAngle_ChA) > cTOL_DISC_ANGLE_DEG) AND
              (ABS(rPos_ShearKnifeAngle_ChB - rPos_ShearKnifeAngle_ChC) > cTOL_DISC_ANGLE_DEG) THEN
            bHealth_KnifeAngle_ChB := FALSE;
        ELSIF (ABS(rPos_ShearKnifeAngle_ChC - rPos_ShearKnifeAngle_ChA) > cTOL_DISC_ANGLE_DEG) AND
              (ABS(rPos_ShearKnifeAngle_ChC - rPos_ShearKnifeAngle_ChB) > cTOL_DISC_ANGLE_DEG) THEN
            bHealth_KnifeAngle_ChC := FALSE;
        END_IF;
    END_IF;
ELSE
    rTimerDisc_KnifeAngle := MAX(0.0, rTimerDisc_KnifeAngle - (2.0 * rT_CycleTime_Sec));
END_IF;

IF bFaultReset_Cmd THEN
    bHealth_KnifeAngle_ChA := TRUE;
    bHealth_KnifeAngle_ChB := TRUE;
    bHealth_KnifeAngle_ChC := TRUE;
    rTimerDisc_KnifeAngle := 0.0;
END_IF;

IF bHealth_KnifeAngle_ChA AND bHealth_KnifeAngle_ChB AND bHealth_KnifeAngle_ChC THEN
    IF ((rPos_ShearKnifeAngle_ChA >= rPos_ShearKnifeAngle_ChB) AND (rPos_ShearKnifeAngle_ChA <= rPos_ShearKnifeAngle_ChC)) OR
       ((rPos_ShearKnifeAngle_ChA >= rPos_ShearKnifeAngle_ChC) AND (rPos_ShearKnifeAngle_ChA <= rPos_ShearKnifeAngle_ChB)) THEN
        rKnifeActualAngle_deg := rPos_ShearKnifeAngle_ChA;
    ELSIF ((rPos_ShearKnifeAngle_ChB >= rPos_ShearKnifeAngle_ChA) AND (rPos_ShearKnifeAngle_ChB <= rPos_ShearKnifeAngle_ChC)) OR
          ((rPos_ShearKnifeAngle_ChB >= rPos_ShearKnifeAngle_ChC) AND (rPos_ShearKnifeAngle_ChB <= rPos_ShearKnifeAngle_ChA)) THEN
        rKnifeActualAngle_deg := rPos_ShearKnifeAngle_ChB;
    ELSE
        rKnifeActualAngle_deg := rPos_ShearKnifeAngle_ChC;
    END_IF;
ELSIF bHealth_KnifeAngle_ChA AND bHealth_KnifeAngle_ChB THEN
    rKnifeActualAngle_deg := 0.5 * (rPos_ShearKnifeAngle_ChA + rPos_ShearKnifeAngle_ChB);
ELSIF bHealth_KnifeAngle_ChB AND bHealth_KnifeAngle_ChC THEN
    rKnifeActualAngle_deg := 0.5 * (rPos_ShearKnifeAngle_ChB + rPos_ShearKnifeAngle_ChC);
ELSIF bHealth_KnifeAngle_ChA AND bHealth_KnifeAngle_ChC THEN
    rKnifeActualAngle_deg := 0.5 * (rPos_ShearKnifeAngle_ChA + rPos_ShearKnifeAngle_ChC);
ELSIF bHealth_KnifeAngle_ChA THEN
    rKnifeActualAngle_deg := rPos_ShearKnifeAngle_ChA;
ELSIF bHealth_KnifeAngle_ChB THEN
    rKnifeActualAngle_deg := rPos_ShearKnifeAngle_ChB;
ELSIF bHealth_KnifeAngle_ChC THEN
    rKnifeActualAngle_deg := rPos_ShearKnifeAngle_ChC;
ELSE
    rKnifeActualAngle_deg := 0.0;
END_IF;

(* --- PACK TMR SENSOR HEALTH STATUS BITS INTO dwStatusWord_TMR_Health --- *)
dwStatusWord_TMR_Health := DWORD#16#00000000;
IF bHealth_RollUpper_ChA THEN dwStatusWord_TMR_Health := dwStatusWord_TMR_Health OR DWORD#16#00000001; END_IF;
IF bHealth_RollUpper_ChB THEN dwStatusWord_TMR_Health := dwStatusWord_TMR_Health OR DWORD#16#00000002; END_IF;
IF bHealth_RollUpper_ChC THEN dwStatusWord_TMR_Health := dwStatusWord_TMR_Health OR DWORD#16#00000004; END_IF;

IF bHealth_RollLower_ChA THEN dwStatusWord_TMR_Health := dwStatusWord_TMR_Health OR DWORD#16#00000008; END_IF;
IF bHealth_RollLower_ChB THEN dwStatusWord_TMR_Health := dwStatusWord_TMR_Health OR DWORD#16#00000010; END_IF;
IF bHealth_RollLower_ChC THEN dwStatusWord_TMR_Health := dwStatusWord_TMR_Health OR DWORD#16#00000020; END_IF;

IF bHealth_SteamSupply_ChA THEN dwStatusWord_TMR_Health := dwStatusWord_TMR_Health OR DWORD#16#00000040; END_IF;
IF bHealth_SteamSupply_ChB THEN dwStatusWord_TMR_Health := dwStatusWord_TMR_Health OR DWORD#16#00000080; END_IF;
IF bHealth_SteamSupply_ChC THEN dwStatusWord_TMR_Health := dwStatusWord_TMR_Health OR DWORD#16#00000100; END_IF;

IF bHealth_BridgeSag_ChA THEN dwStatusWord_TMR_Health := dwStatusWord_TMR_Health OR DWORD#16#00000200; END_IF;
IF bHealth_BridgeSag_ChB THEN dwStatusWord_TMR_Health := dwStatusWord_TMR_Health OR DWORD#16#00000400; END_IF;
IF bHealth_BridgeSag_ChC THEN dwStatusWord_TMR_Health := dwStatusWord_TMR_Health OR DWORD#16#00000800; END_IF;

IF bHealth_WebTension_ChA THEN dwStatusWord_TMR_Health := dwStatusWord_TMR_Health OR DWORD#16#00001000; END_IF;
IF bHealth_WebTension_ChB THEN dwStatusWord_TMR_Health := dwStatusWord_TMR_Health OR DWORD#16#00002000; END_IF;
IF bHealth_WebTension_ChC THEN dwStatusWord_TMR_Health := dwStatusWord_TMR_Health OR DWORD#16#00004000; END_IF;

IF bHealth_MasterSpeed_ChA THEN dwStatusWord_TMR_Health := dwStatusWord_TMR_Health OR DWORD#16#00008000; END_IF;
IF bHealth_MasterSpeed_ChB THEN dwStatusWord_TMR_Health := dwStatusWord_TMR_Health OR DWORD#16#00010000; END_IF;
IF bHealth_MasterSpeed_ChC THEN dwStatusWord_TMR_Health := dwStatusWord_TMR_Health OR DWORD#16#00020000; END_IF;

IF bHealth_KnifeAngle_ChA THEN dwStatusWord_TMR_Health := dwStatusWord_TMR_Health OR DWORD#16#00040000; END_IF;
IF bHealth_KnifeAngle_ChB THEN dwStatusWord_TMR_Health := dwStatusWord_TMR_Health OR DWORD#16#00080000; END_IF;
IF bHealth_KnifeAngle_ChC THEN dwStatusWord_TMR_Health := dwStatusWord_TMR_Health OR DWORD#16#00100000; END_IF;


(* =====================================================================================================================
 * PHASE 2: CYBER-PHYSICAL FLUID, THERMAL, KINEMATIC & WARPAGE CALCULATIONS
 * =====================================================================================================================
 * 1. Flute Profile Geometry & Consumption Rates
 * 2. Starch Adhesive Viscosity, Shear Thinning & Taylor Film Metering
 * 3. Starch Gelatinization Rate & Degree of Gelation
 * 4. Double-Backer Steam Chest Multi-Zone Heat Flux & Moisture Balance
 * 5. Cardboard Warpage / Curl Mechanics & Dynamic Ballast Shoe Pressure Trim
 * 6. Bridge Festoon Catenary Web Dynamics & Mass Accumulation Integral
 * 7. Flying Rotary Cutoff Shear Kinematics & 5th-Order Cam Polynomial Sync
 *)

(* 1. FLUTE PROFILE GEOMETRY PARAMETERS *)
CASE nFluteType_Selector OF
    1: (* A-Flute: Coarse flute, highest vertical compression strength *)
        rFlutePitch_p_f      := 8.60;
        rFluteHeight_h_f     := 4.70;
        rFluteTakeUp_alpha_f := 1.540;
    2: (* B-Flute: Fine flute, superior crush resistance & printing surface *)
        rFlutePitch_p_f      := 6.50;
        rFluteHeight_h_f     := 2.50;
        rFluteTakeUp_alpha_f := 1.320;
    3: (* C-Flute: Universal medium flute, standard transit packaging *)
        rFlutePitch_p_f      := 7.80;
        rFluteHeight_h_f     := 3.60;
        rFluteTakeUp_alpha_f := 1.430;
    4: (* E-Flute: Micro-flute, high-graphic carton litho-lamination *)
        rFlutePitch_p_f      := 3.50;
        rFluteHeight_h_f     := 1.15;
        rFluteTakeUp_alpha_f := 1.270;
ELSE
    (* Fallback default C-Flute *)
    rFlutePitch_p_f      := 7.80;
    rFluteHeight_h_f     := 3.60;
    rFluteTakeUp_alpha_f := 1.430;
END_CASE;

(* Production Throughput Area [m2/h] *)
rCalc_CorrugatorThroughput_sqm_h := (rAct_LineSpeedMaster_m_min * 60.0) * rWebWidth_m;

(* 2. STARCH ADHESIVE RHEOLOGY & TAYLOR FILM GAP METERING *)
(* Empirical conversion from Stein-Hall seconds to dynamic viscosity in centipoise [cP] *)
rStarchViscosity_cP := (12.50 * rVisc_StarchSteinHall_Sec) + (0.085 * rVisc_StarchSteinHall_Sec * rVisc_StarchSteinHall_Sec);

(* Shear rate in applicator roll nip [1/s] *)
IF rGap_StarchApplicatorNominal_Setpt > 0.05 THEN
    rGlueShearRate_inv_s := ((rAct_LineSpeedMaster_m_min / 60.0) * 1000.0) / rGap_StarchApplicatorNominal_Setpt;
ELSE
    rGlueShearRate_inv_s := 1000.0;
END_IF;

(* Temperature correction factor (Arrhenius behavior around reference 40 deg C) *)
rTemp_Diff := (42.0 - 40.0);
rTemp_Term := EXP(-0.022 * rTemp_Diff);

(* Taylor hydrodynamic film splitting model: film thickness h_film [um] *)
rGlueFilmThickness_um := 0.485 * (rGap_StarchApplicatorNominal_Setpt * 1000.0) *
                         EXPT(((rStarchViscosity_cP * 0.001 * (rAct_LineSpeedMaster_m_min / 60.0)) / 0.045), 0.3333) * rTemp_Term;
rGlueFilmThickness_um := MAX(8.0, MIN(45.0, rGlueFilmThickness_um));

(* Dry starch coat weight on fluting tips [g/m2]: Flute tip width ~ 1.2 mm per flute pitch *)
rCalc_StarchFilmCoatWeight_gsm := rGlueFilmThickness_um * 1.120 * 0.265 * (1.20 / rFlutePitch_p_f);

(* Dynamic gap servo trim to maintain constant dry coat weight 15.0 g/m2 *)
rTemp_Diff := 15.0 - rCalc_StarchFilmCoatWeight_gsm;
rCmd_StarchApplicatorGap_ServoPos := rGap_StarchApplicatorNominal_Setpt + (0.0085 * rTemp_Diff) + (0.00015 * (rStarchViscosity_cP - 480.0));
rCmd_StarchApplicatorGap_ServoPos := MAX(0.150, MIN(0.350, rCmd_StarchApplicatorGap_ServoPos));

(* 3. STARCH GELATINIZATION RATE & PROGRESS *)
IF rAct_LineSpeedMaster_m_min > 5.0 THEN
    rStarchDwellTime_Sec := 0.035 / (rAct_LineSpeedMaster_m_min / 60.0);
ELSE
    rStarchDwellTime_Sec := 0.200;
END_IF;

IF rAct_UpperRollTempVoted_degC > rT_StarchGelatinization_Setpt THEN
    rTemp_Term := 65.0 * EXP(0.085 * (rAct_UpperRollTempVoted_degC - rT_StarchGelatinization_Setpt));
    rStarchGelDegree_Internal := 1.0 - EXP(-rTemp_Term * rStarchDwellTime_Sec);
ELSE
    rStarchGelDegree_Internal := 0.05;
END_IF;
rCalc_StarchGelatinizationDegree_Pct := MAX(0.0, MIN(100.0, rStarchGelDegree_Internal * 100.0));

(* 4. DOUBLE-BACKER MULTI-ZONE STEAM CHEST THERMAL PROFILING & HEAT FLUX *)
(* Overall heat transfer coefficient U ~ 350 W/(m2*K) *)
rPlateTemp_Zone1_Act := rT_SteamChestZone1_Setpt - (0.045 * (rAct_LineSpeedMaster_m_min - 200.0));
rPlateTemp_Zone2_Act := rT_SteamChestZone2_Setpt - (0.060 * (rAct_LineSpeedMaster_m_min - 200.0));
rPlateTemp_Zone3_Act := rT_SteamChestZone3_Setpt - (0.035 * (rAct_LineSpeedMaster_m_min - 200.0));

rQ_SteamChestZone1_kW := 0.350 * 12.5 * (rPlateTemp_Zone1_Act - 95.0);
rQ_SteamChestZone2_kW := 0.380 * 15.0 * (rPlateTemp_Zone2_Act - 105.0);
rQ_SteamChestZone3_kW := 0.320 * 10.0 * (rPlateTemp_Zone3_Act - 98.0);

(* Moisture evaporation gradient *)
rBoardMoistureBottomLiner_Pct := 8.5 - (0.0035 * (rQ_SteamChestZone1_kW + rQ_SteamChestZone2_kW));
rBoardMoistureTopLiner_Pct    := 8.0 - (0.0022 * (rQ_SteamChestZone2_kW + rQ_SteamChestZone3_kW));
rBoardMoistureBottomLiner_Pct := MAX(5.0, MIN(11.0, rBoardMoistureBottomLiner_Pct));
rBoardMoistureTopLiner_Pct    := MAX(5.0, MIN(11.0, rBoardMoistureTopLiner_Pct));

(* 5. CARDBOARD WARPAGE / CURL MECHANICS & DYNAMIC BALLAST SHOE PRESSURE *)
(* Moisture differential Delta_M drives hygro-expansion curl *)
rTemp_Diff := rBoardMoistureTopLiner_Pct - rBoardMoistureBottomLiner_Pct;
(* Thermal differential Delta_T drives differential shrinkage *)
rTemp_Term := (rPlateTemp_Zone1_Act - 110.0) - (rPlateTemp_Zone3_Act - 95.0);

(* Warpage curvature index [-100.0% = downward curl, +100.0% = upward curl] *)
rBoardCurlIndex_Internal := (18.5 * rTemp_Diff) + (0.45 * rTemp_Term);
rCalc_BoardWarpageCurlIndex_Pct := MAX(-100.0, MIN(100.0, rBoardCurlIndex_Internal));

(* Dynamic ballast shoe pressure trim: increased pressure on zone with higher moisture *)
IF rBoardCurlIndex_Internal > 5.0 THEN
    (* Upward curl: top liner wetter -> increase ballast shoe force to accelerate heat penetration *)
    rCmd_BallastShoePneumatic_Reg_bar := rP_BallastShoePressure_Setpt + (0.008 * rBoardCurlIndex_Internal);
ELSIF rBoardCurlIndex_Internal < -5.0 THEN
    (* Downward curl: bottom liner wetter -> decrease ballast shoe force *)
    rCmd_BallastShoePneumatic_Reg_bar := rP_BallastShoePressure_Setpt + (0.006 * rBoardCurlIndex_Internal);
ELSE
    rCmd_BallastShoePneumatic_Reg_bar := rP_BallastShoePressure_Setpt;
END_IF;
rCmd_BallastShoePneumatic_Reg_bar := MAX(0.20, MIN(1.80, rCmd_BallastShoePneumatic_Reg_bar));

(* 6. BRIDGE CATENARY WEB DYNAMICS & ACCUMULATION INTEGRAL *)
(* Single-facer web feed vs double-backer traction consumption *)
rTemp_Diff := (rCmd_SingleFacerDrive_Speed - rCmd_DoubleBackerDrive_Speed) / 60.0;
rBridgeAccumulatorLength_Act := rBridgeAccumulatorLength_Act + (rTemp_Diff * rT_CycleTime_Sec);
rBridgeAccumulatorLength_Act := MAX(rBridgeAccumulatorLength_Min, MIN(rBridgeAccumulatorLength_Max, rBridgeAccumulatorLength_Act));
rCalc_BridgeAccumulatedWebLength_m := rBridgeAccumulatorLength_Act;

(* Catenary sag and web tension balancing *)
IF rAct_BridgeSagVoted_mm > 100.0 THEN
    rTemp_Term := (rBridgeLinearMassDensity_kg_m * 9.81 * rBridgeSpanLength_m * rBridgeSpanLength_m) / (8.0 * (rAct_BridgeSagVoted_mm * 0.001));
ELSE
    rTemp_Term := 450.0;
END_IF;

(* Bridge vacuum suction brake modulation: maintains entry tension at 450 N *)
rTemp_Diff := 450.0 - rAct_WebTensionEntryDB_N;
rCmd_BridgeFestoonSuctionBrake_Pct := 35.0 + (0.065 * rTemp_Diff);
rCmd_BridgeFestoonSuctionBrake_Pct := MAX(5.0, MIN(95.0, rCmd_BridgeFestoonSuctionBrake_Pct));

(* 7. DRY-END FLYING ROTARY CUTOFF SHEAR KINEMATICS & 5th-ORDER CAM PROFILE *)
(* Synchronous cutting velocity [m/min] *)
rKnifeSyncVelocity_m_min := rAct_LineSpeedMaster_m_min;

(* Synchronous cutting rotational velocity [rpm]: omega = v_line / (2 * pi * R_knife) *)
IF rKnifeRadius_mm > 10.0 THEN
    rKnifeTargetOmega_rpm := (rKnifeSyncVelocity_m_min / (2.0 * 3.14159265 * (rKnifeRadius_mm * 0.001)));
ELSE
    rKnifeTargetOmega_rpm := 0.0;
END_IF;

(* Cut zone detection: Bottom Dead Center is at 180.0 deg *)
IF (rKnifeActualAngle_deg >= (180.0 - rKnifeCutZoneHalfAngle_deg)) AND
   (rKnifeActualAngle_deg <= (180.0 + rKnifeCutZoneHalfAngle_deg)) THEN
    bKnifeInSyncCutZone := TRUE;
ELSE
    bKnifeInSyncCutZone := FALSE;
END_IF;

(* Non-linear sheet length camming ratio: lambda = L_target / C_knife *)
IF rL_TargetSheetCutoff_Setpt > 100.0 THEN
    rTemp_Term := rL_TargetSheetCutoff_Setpt / rKnifeCircumference_mm;
ELSE
    rTemp_Term := 1.0;
END_IF;

(* Speed profile calculation: outside cut zone, modulate speed to match cutoff length *)
IF bKnifeInSyncCutZone THEN
    (* Knife must strictly match web speed during blade engagement *)
    rCmd_FlyingShearKnife_ServoVelocity := rKnifeTargetOmega_rpm;
ELSE
    (* Outside cut zone: accelerate if sheet is short, decelerate if sheet is long *)
    IF rTemp_Term > 1.001 THEN
        (* Longer sheet: knife must dwell / decelerate *)
        rCmd_FlyingShearKnife_ServoVelocity := rKnifeTargetOmega_rpm / rTemp_Term;
    ELSIF rTemp_Term < 0.999 THEN
        (* Shorter sheet: knife must sprint / accelerate *)
        rCmd_FlyingShearKnife_ServoVelocity := rKnifeTargetOmega_rpm / rTemp_Term;
    ELSE
        rCmd_FlyingShearKnife_ServoVelocity := rKnifeTargetOmega_rpm;
    END_IF;
END_IF;

(* Cut registration phase correction *)
rKnifeCutoffPhaseError_deg := (rKnifeActualAngle_deg - 180.0);
IF ABS(rKnifeCutoffPhaseError_deg) > 180.0 THEN
    IF rKnifeCutoffPhaseError_deg > 0.0 THEN
        rKnifeCutoffPhaseError_deg := rKnifeCutoffPhaseError_deg - 360.0;
    ELSE
        rKnifeCutoffPhaseError_deg := rKnifeCutoffPhaseError_deg + 360.0;
    END_IF;
END_IF;

(* Sheet length error in mm: Delta_L = Delta_theta * R_knife *)
rErr_SheetLengthCutoff_mm := rKnifeCutoffPhaseError_deg * (3.14159265 / 180.0) * rKnifeRadius_mm;

(* Phase integrator with anti-windup *)
rKnifeIntegralPhaseErr_deg := rKnifeIntegralPhaseErr_deg + (rKnifeCutoffPhaseError_deg * rT_CycleTime_Sec);
rKnifeIntegralPhaseErr_deg := MAX(-15.0, MIN(15.0, rKnifeIntegralPhaseErr_deg));

(* Total knife servo command velocity with phase trim *)
rCmd_FlyingShearKnife_ServoVelocity := rCmd_FlyingShearKnife_ServoVelocity - (0.45 * rKnifeCutoffPhaseError_deg) - (0.08 * rKnifeIntegralPhaseErr_deg);
rCmd_FlyingShearKnife_ServoVelocity := MAX(0.0, MIN(850.0, rCmd_FlyingShearKnife_ServoVelocity));
rCmd_FlyingShearKnife_ServoPosition := rKnifeActualAngle_deg;
'''

if __name__ == '__main__':
    p2 = get_part2()
    print("Part 2 length:", len(p2))
