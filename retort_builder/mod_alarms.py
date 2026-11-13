# -*- coding: utf-8 -*-
"""
Module: retort_builder/mod_alarms.py
Implements Phase 6: ISA-18.2 Multi-Tier Process Alarms, Deadband Hysteresis,
32-Bit Bit-Packed Words (Status, Warning, Fault, FDA Compliance), and Actuator Clamping.
"""

def generate_alarms():
    return '''(* =====================================================================================================================
 * PHASE 6: ISA-18.2 MULTI-TIER PROCESS ALARMS, DEADBAND HYSTERESIS & 32-BIT PACKED WORDS
 * Alarm Hierarchy:
 *   Severity Level 1: Emergency Safety Trips (Failsafe shutdown, steam shutoff, emergency deluge)
 *   Severity Level 2: Abnormal Operating Warnings (Audible annunciator, advisory trim)
 *   Regulatory Audit: FDA 21 CFR Part 113 Legal Electronic Batch Sterilization Record
 * ===================================================================================================================== *)

(* Clear dynamic advisory warning word prior to scan evaluation *)
dwWarningWord := dwWarningWord AND 16#0000_000F; (* Preserve external hardware advisory bits *)

(* -------------------------------------------------------------------------
 * SUB-SECTION 6.1: VESSEL TEMPERATURE ALARMS (ISA-18.2 HH, H, L, LL)
 * ------------------------------------------------------------------------- *)
(* High-High Temperature Trip (HH: 138.0 deg C) *)
IF rVotedVesselTemp_degC >= cTrip_Temp_HH_degC THEN
    rAlarmTimer_TempHH := rAlarmTimer_TempHH + rTs_s;
    IF rAlarmTimer_TempHH >= 0.50 THEN
        bTripLatched_TempHH := TRUE;
        dwFaultWord := dwFaultWord OR 16#0000_0001; (* Temp HH Trip *)
    END_IF;
ELSE
    rAlarmTimer_TempHH := 0.0;
    IF bCmd_AcknowledgeAlarm AND (rVotedVesselTemp_degC < (cTrip_Temp_HH_degC - cHyst_Temp_degC)) THEN
        bTripLatched_TempHH := FALSE;
        dwFaultWord := dwFaultWord AND NOT 16#0000_0001;
    END_IF;
END_IF;

(* High Temperature Advisory Warning (H: 135.0 deg C) *)
IF rVotedVesselTemp_degC >= cWarn_Temp_H_degC THEN
    dwWarningWord := dwWarningWord OR 16#0000_0020; (* Temp H Warning *)
ELSIF rVotedVesselTemp_degC < (cWarn_Temp_H_degC - cHyst_Temp_degC) THEN
    dwWarningWord := dwWarningWord AND NOT 16#0000_0020;
END_IF;

(* Low Temperature Advisory Warning (L: 120.0 deg C during Cook States 4, 5, 6) *)
IF (iFSM_CurrentState >= 4) AND (iFSM_CurrentState <= 6) THEN
    IF rVotedVesselTemp_degC <= cWarn_Temp_L_degC THEN
        dwWarningWord := dwWarningWord OR 16#0000_0040; (* Temp L Warning *)
    ELSIF rVotedVesselTemp_degC > (cWarn_Temp_L_degC + cHyst_Temp_degC) THEN
        dwWarningWord := dwWarningWord AND NOT 16#0000_0040;
    END_IF;

    (* Low-Low Temperature Trip (LL: 115.0 deg C during Cook) *)
    IF rVotedVesselTemp_degC <= cTrip_Temp_LL_degC THEN
        rAlarmTimer_TempLL := rAlarmTimer_TempLL + rTs_s;
        IF rAlarmTimer_TempLL >= 3.00 THEN
            bTripLatched_TempLL := TRUE;
            dwFaultWord := dwFaultWord OR 16#0000_0002; (* Temp LL Trip *)
        END_IF;
    ELSE
        rAlarmTimer_TempLL := 0.0;
        IF bCmd_AcknowledgeAlarm AND (rVotedVesselTemp_degC > (cTrip_Temp_LL_degC + cHyst_Temp_degC)) THEN
            bTripLatched_TempLL := FALSE;
            dwFaultWord := dwFaultWord AND NOT 16#0000_0002;
        END_IF;
    END_IF;
END_IF;

(* -------------------------------------------------------------------------
 * SUB-SECTION 6.2: VESSEL PRESSURE ALARMS (ISA-18.2 HH, H, L, LL)
 * ------------------------------------------------------------------------- *)
(* High-High Pressure Structural Safety Trip (HH: 4.20 bar) *)
IF rVotedVesselPress_bar >= cTrip_Press_HH_bar THEN
    rAlarmTimer_PressHH := rAlarmTimer_PressHH + rTs_s;
    IF rAlarmTimer_PressHH >= 0.20 THEN
        bTripLatched_PressHH := TRUE;
        dwFaultWord := dwFaultWord OR 16#0000_0004; (* Press HH Trip *)
    END_IF;
ELSE
    rAlarmTimer_PressHH := 0.0;
    IF bCmd_AcknowledgeAlarm AND (rVotedVesselPress_bar < (cTrip_Press_HH_bar - cHyst_Press_bar)) THEN
        bTripLatched_PressHH := FALSE;
        dwFaultWord := dwFaultWord AND NOT 16#0000_0004;
    END_IF;
END_IF;

(* High Pressure Advisory Warning (H: 3.80 bar) *)
IF rVotedVesselPress_bar >= cWarn_Press_H_bar THEN
    dwWarningWord := dwWarningWord OR 16#0000_0080; (* Press H Warning *)
ELSIF rVotedVesselPress_bar < (cWarn_Press_H_bar - cHyst_Press_bar) THEN
    dwWarningWord := dwWarningWord AND NOT 16#0000_0080;
END_IF;

(* Low Pressure Advisory Warning (L: 1.80 bar during Cook States 4, 5, 6) *)
IF (iFSM_CurrentState >= 4) AND (iFSM_CurrentState <= 6) THEN
    IF rVotedVesselPress_bar <= cWarn_Press_L_bar THEN
        dwWarningWord := dwWarningWord OR 16#0000_0100; (* Press L Warning *)
    ELSIF rVotedVesselPress_bar > (cWarn_Press_L_bar + cHyst_Press_bar) THEN
        dwWarningWord := dwWarningWord AND NOT 16#0000_0100;
    END_IF;
END_IF;

(* Low-Low Vacuum Collapse Safety Trip (LL: 0.05 bar gauge / 1.06 bar absolute) *)
IF (iFSM_CurrentState >= 8) AND (iFSM_CurrentState <= 10) THEN
    IF rVotedVesselPress_bar <= cTrip_Press_LL_bar THEN
        rAlarmTimer_PressLL := rAlarmTimer_PressLL + rTs_s;
        IF rAlarmTimer_PressLL >= 0.50 THEN
            bTripLatched_PressLL := TRUE;
            dwFaultWord := dwFaultWord OR 16#0000_0008; (* Vacuum Collapse Trip *)
        END_IF;
    ELSE
        rAlarmTimer_PressLL := 0.0;
        IF bCmd_AcknowledgeAlarm AND (rVotedVesselPress_bar > (cTrip_Press_LL_bar + cHyst_Press_bar)) THEN
            bTripLatched_PressLL := FALSE;
            dwFaultWord := dwFaultWord AND NOT 16#0000_0008;
        END_IF;
    END_IF;
END_IF;

(* -------------------------------------------------------------------------
 * SUB-SECTION 6.3: CONTAINER NET WALL STRESS ALARMS (BURST vs CRUSH)
 * ------------------------------------------------------------------------- *)
(* Pouch Bursting Limit (+0.38 bar differential) *)
IF rStressDeltaP_bar >= cTrip_DeltaP_Burst_bar THEN
    rAlarmTimer_DeltaP_Burst := rAlarmTimer_DeltaP_Burst + rTs_s;
    IF rAlarmTimer_DeltaP_Burst >= 0.30 THEN
        bTripLatched_PouchBurst := TRUE;
        dwFaultWord := dwFaultWord OR 16#0000_0010; (* Pouch Burst Trip *)
    END_IF;
ELSE
    rAlarmTimer_DeltaP_Burst := 0.0;
    IF bCmd_AcknowledgeAlarm AND (rStressDeltaP_bar < (cTrip_DeltaP_Burst_bar - cHyst_DeltaP_bar)) THEN
        bTripLatched_PouchBurst := FALSE;
        dwFaultWord := dwFaultWord AND NOT 16#0000_0010;
    END_IF;
END_IF;

(* Pouch Buckling / Panelling Crush Limit (-0.42 bar differential) *)
IF rStressDeltaP_bar <= cTrip_DeltaP_Buckle_bar THEN
    rAlarmTimer_DeltaP_Buckle := rAlarmTimer_DeltaP_Buckle + rTs_s;
    IF rAlarmTimer_DeltaP_Buckle >= 0.30 THEN
        bTripLatched_PouchBuckle := TRUE;
        dwFaultWord := dwFaultWord OR 16#0000_0020; (* Pouch Buckle Trip *)
    END_IF;
ELSE
    rAlarmTimer_DeltaP_Buckle := 0.0;
    IF bCmd_AcknowledgeAlarm AND (rStressDeltaP_bar > (cTrip_DeltaP_Buckle_bar + cHyst_DeltaP_bar)) THEN
        bTripLatched_PouchBuckle := FALSE;
        dwFaultWord := dwFaultWord AND NOT 16#0000_0020;
    END_IF;
END_IF;

(* Distension Warning (+0.28 bar) *)
IF rStressDeltaP_bar >= cWarn_DeltaP_H_bar THEN
    dwWarningWord := dwWarningWord OR 16#0000_0200; (* Distension Warning *)
ELSIF rStressDeltaP_bar < (cWarn_DeltaP_H_bar - cHyst_DeltaP_bar) THEN
    dwWarningWord := dwWarningWord AND NOT 16#0000_0200;
END_IF;

(* Concavity Warning (-0.30 bar) *)
IF rStressDeltaP_bar <= cWarn_DeltaP_L_bar THEN
    dwWarningWord := dwWarningWord OR 16#0000_0400; (* Concavity Warning *)
ELSIF rStressDeltaP_bar > (cWarn_DeltaP_L_bar + cHyst_DeltaP_bar) THEN
    dwWarningWord := dwWarningWord AND NOT 16#0000_0400;
END_IF;

(* -------------------------------------------------------------------------
 * SUB-SECTION 6.4: SUMP LIQUID LEVEL ALARMS
 * ------------------------------------------------------------------------- *)
(* Sump Flooding Submergence Trip (HH: 480 mm during steam cook) *)
IF (iFSM_CurrentState <= 6) AND (rVotedSumpLevel_mm >= cTrip_Sump_HH_mm) THEN
    rAlarmTimer_SumpHH := rAlarmTimer_SumpHH + rTs_s;
    IF rAlarmTimer_SumpHH >= 2.00 THEN
        dwFaultWord := dwFaultWord OR 16#0000_0040; (* Sump Submergence Trip *)
    END_IF;
ELSE
    rAlarmTimer_SumpHH := 0.0;
    IF bCmd_AcknowledgeAlarm AND (rVotedSumpLevel_mm < (cTrip_Sump_HH_mm - cHyst_Sump_mm)) THEN
        dwFaultWord := dwFaultWord AND NOT 16#0000_0040;
    END_IF;
END_IF;

(* Sump High Advisory Warning (H: 350 mm) *)
IF rVotedSumpLevel_mm >= cWarn_Sump_H_mm THEN
    dwWarningWord := dwWarningWord OR 16#0000_0800;
ELSIF rVotedSumpLevel_mm < (cWarn_Sump_H_mm - cHyst_Sump_mm) THEN
    dwWarningWord := dwWarningWord AND NOT 16#0000_0800;
END_IF;

(* Sump Low Cavitation Warning (L: 60 mm during spray cooling) *)
IF (iFSM_CurrentState = 8) OR (iFSM_CurrentState = 9) THEN
    IF rVotedSumpLevel_mm <= cWarn_Sump_L_mm THEN
        dwWarningWord := dwWarningWord OR 16#0000_1000;
    ELSIF rVotedSumpLevel_mm > (cWarn_Sump_L_mm + cHyst_Sump_mm) THEN
        dwWarningWord := dwWarningWord AND NOT 16#0000_1000;
    END_IF;
END_IF;

(* -------------------------------------------------------------------------
 * SUB-SECTION 6.5: DOOR GASKET SEAL & AGITATION BASKET SLIP ALARMS
 * ------------------------------------------------------------------------- *)
(* Pressurized door seal loss detection *)
IF (iFSM_CurrentState >= 2) AND (iFSM_CurrentState <= 10) THEN
    IF (rPT_601_DoorSealPress_bar < 4.80) OR (NOT bDI_DoorSealPressureOK_PS103) THEN
        rAlarmTimer_SealPressLow := rAlarmTimer_SealPressLow + rTs_s;
        IF rAlarmTimer_SealPressLow >= 0.80 THEN
            bTripLatched_DoorSealLoss := TRUE;
            dwFaultWord := dwFaultWord OR 16#0000_0100; (* Door Seal Loss Trip *)
        END_IF;
    ELSE
        rAlarmTimer_SealPressLow := 0.0;
    END_IF;
END_IF;

(* Agitation basket motor slip / stall detection *)
IF (rAO_RotaryDriveSpeed_RPM > 2.0) THEN
    IF ABS(rST_101_RotaryBasketRPM - rAO_RotaryDriveSpeed_RPM) > 4.50 THEN
        rAlarmTimer_AgitatorStall := rAlarmTimer_AgitatorStall + rTs_s;
        IF rAlarmTimer_AgitatorStall >= 3.50 THEN
            dwFaultWord := dwFaultWord OR 16#0000_0800; (* Agitator Stall Trip *)
        END_IF;
    ELSE
        rAlarmTimer_AgitatorStall := 0.0;
    END_IF;
ELSE
    rAlarmTimer_AgitatorStall := 0.0;
END_IF;

(* Hardwired Emergency Stop Pushbutton Trip *)
IF NOT bDI_EmergencyStop_PB100 THEN
    bTripLatched_EStop := TRUE;
    dwFaultWord := dwFaultWord OR 16#0000_0200; (* E-Stop Pressed *)
END_IF;

(* Safety Relief Valve Poppet Lift Proximity Switch *)
IF bDI_SafetyReliefValve_Open_ZS201 THEN
    dwFaultWord := dwFaultWord OR 16#0000_0400; (* Relief Valve Lifted *)
END_IF;

(* Sensor TMR Triple-Failure Trip Flag *)
IF bTripLatched_TMR_Failure THEN
    dwFaultWord := dwFaultWord OR 16#0000_0080; (* TMR Complete Failure *)
END_IF;

(* -------------------------------------------------------------------------
 * SUB-SECTION 6.6: TMR SENSOR DEGRADATION WARNING WORD ENCODING
 * ------------------------------------------------------------------------- *)
IF iTMR_TT101_Mode < 3 THEN dwWarningWord := dwWarningWord OR 16#0000_2000; END_IF;
IF iTMR_PT201_Mode < 3 THEN dwWarningWord := dwWarningWord OR 16#0000_4000; END_IF;
IF iTMR_TT301_Mode < 3 THEN dwWarningWord := dwWarningWord OR 16#0000_8000; END_IF;
IF iTMR_LT401_Mode < 3 THEN dwWarningWord := dwWarningWord OR 16#0001_0000; END_IF;

(* -------------------------------------------------------------------------
 * SUB-SECTION 6.7: 32-BIT BIT-PACKED STATUS WORD (dwStatusWord)
 * ------------------------------------------------------------------------- *)
dwStatusWord := 16#0000_0000;
IF (iFSM_CurrentState > 0) AND (iFSM_CurrentState < 12) THEN dwStatusWord := dwStatusWord OR 16#0000_0001; END_IF; (* Running *)
IF iFSM_CurrentState = 0 THEN dwStatusWord := dwStatusWord OR 16#0000_0002; END_IF; (* Idle Standby *)
IF bDI_DoorLockedLimit_ZS102 THEN dwStatusWord := dwStatusWord OR 16#0000_0004; END_IF; (* Door Locked *)
IF bDI_DoorSealPressureOK_PS103 AND (rPT_601_DoorSealPress_bar >= 5.0) THEN dwStatusWord := dwStatusWord OR 16#0000_0008; END_IF; (* Seal OK *)
IF iFSM_CurrentState >= 3 THEN dwStatusWord := dwStatusWord OR 16#0000_0010; END_IF; (* Purge Done *)
IF iFSM_CurrentState >= 5 THEN dwStatusWord := dwStatusWord OR 16#0000_0020; END_IF; (* Cut-In Done *)
IF iFSM_CurrentState = 5 THEN dwStatusWord := dwStatusWord OR 16#0000_0040; END_IF; (* Cook Hold Active *)
IF bBall_CatchupActive THEN dwStatusWord := dwStatusWord OR 16#0000_0080; END_IF; (* Deviation Catch-up *)
IF iFSM_CurrentState = 7 THEN dwStatusWord := dwStatusWord OR 16#0000_0100; END_IF; (* Pre-Cool Air Active *)
IF (iFSM_CurrentState = 8) OR (iFSM_CurrentState = 9) THEN dwStatusWord := dwStatusWord OR 16#0000_0200; END_IF; (* Cooling Active *)
IF iFSM_CurrentState = 10 THEN dwStatusWord := dwStatusWord OR 16#0000_0400; END_IF; (* Draining Active *)
IF iFSM_CurrentState = 11 THEN dwStatusWord := dwStatusWord OR 16#0000_0800; END_IF; (* Vacuum Breaking *)
IF (rST_101_RotaryBasketRPM > 1.0) THEN dwStatusWord := dwStatusWord OR 16#0000_1000; END_IF; (* Agitation Active *)
IF (iTMR_TT101_Mode = 3) AND (iTMR_PT201_Mode = 3) AND (iTMR_TT301_Mode = 3) AND (iTMR_LT401_Mode = 3) THEN
    dwStatusWord := dwStatusWord OR 16#0000_2000; (* All TMR 2oo3 Healthy *)
END_IF;
IF bProcessQualified_FDA THEN dwStatusWord := dwStatusWord OR 16#0000_4000; END_IF; (* F0 Target Reached *)
IF bCycleComplete THEN dwStatusWord := dwStatusWord OR 16#0000_8000; END_IF; (* Cycle Complete *)

(* Common Summary Alarm Flag *)
IF (dwFaultWord <> 16#0000_0000) OR (dwWarningWord <> 16#0000_0000) THEN
    bAlarmCommon := TRUE;
ELSE
    bAlarmCommon := FALSE;
END_IF;

(* Increment Master Cycle Counter *)
iCycleCounter := iCycleCounter + 1;

END_FUNCTION_BLOCK
'''

if __name__ == "__main__":
    a = generate_alarms()
    print("Alarms length:", len(a))
    print(a[:300])
