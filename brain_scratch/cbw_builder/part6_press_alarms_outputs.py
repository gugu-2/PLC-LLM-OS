# part6_press_alarms_outputs.py
# Generates Phase 7 (Press & Shuttle Safety Interlocks), Phase 8 (ISA-18.2 Alarms & Status Words),
# Phase 9 (Actuator Slew Rate Limiting & Safe Clamping), and END_FUNCTION_BLOCK

def get_part6():
    return '''(* ==========================================================================================
 * PHASE 7: 50-BAR HYDRAULIC MEMBRANE PRESS & SHUTTLE CONVEYOR SAFETY INTERLOCKS
 * Real-time monitoring of rubber membrane bladder differential pressure, enclosure guards,
 * optical safety light curtains, ram displacement velocity, and multi-bay dryer transfer.
 * ========================================================================================== *)

(* 1. Membrane Bladder Rupture Differential Pressure Interlock *)
(* Differential between water cushion bladder pressure and main hydraulic cylinder ram *)
IF (ABS(rPress_Bladder_bar - rTMR4_VotedVal) > 8.0) AND (rTMR4_VotedVal > 15.0) THEN
    tAlarmTimer_BladderDiff := tAlarmTimer_BladderDiff + rDeltaTime_s;
    IF tAlarmTimer_BladderDiff >= 0.5 THEN
        (* Tripped: Membrane bladder rupture detected, abort pressing immediately *)
        bValve_EmergencyDump_Open := TRUE;
        IF iState <> 12 THEN
            iPrevState := iState;
            iState := 12; (* Jump to EMERGENCY_PRESS_DUMP_SAFE *)
            tStateTimer_s := 0.0;
            bStateFirstScan := TRUE;
        END_IF;
    END_IF;
ELSE
    tAlarmTimer_BladderDiff := MAX(0.0, tAlarmTimer_BladderDiff - (2.0 * rDeltaTime_s));
END_IF;

(* 2. Hardware Membrane Rupture Physical Sensor Switch *)
IF NOT bMembraneBladder_RuptureSwitch THEN
    bValve_EmergencyDump_Open := TRUE;
    IF iState <> 12 THEN
        iPrevState := iState;
        iState := 12;
        tStateTimer_s := 0.0;
        bStateFirstScan := TRUE;
    END_IF;
END_IF;

(* 3. Enclosure Safety Guard Solenoid Interlock *)
(* If guard unlocked during active pressing (States 8 or 9), execute immediate safety dump *)
IF NOT bPressGuard_Locked AND ((iState = 8) OR (iState = 9)) THEN
    bValve_EmergencyDump_Open := TRUE;
    IF iState <> 12 THEN
        iPrevState := iState;
        iState := 12;
        tStateTimer_s := 0.0;
        bStateFirstScan := TRUE;
    END_IF;
END_IF;

(* 4. Category 4 Safety Light Curtain Intrusion Interlock *)
(* Halts shuttle car traversing if light curtain interrupted *)
IF NOT bLightCurtain_Clear THEN
    bShuttle_TraverseForward := FALSE;
    bShuttle_TraverseReverse := FALSE;
    rShuttle_Speed_mms := 0.0;
END_IF;

(* 5. Shuttle Conveyor Absolute Position Limiting [0.0 mm to 12,000.0 mm] *)
IF rShuttle_Position_mm > 12000.0 THEN
    bShuttle_TraverseForward := FALSE;
    rShuttle_Speed_mms := 0.0;
ELSIF rShuttle_Position_mm < 0.0 THEN
    bShuttle_TraverseReverse := FALSE;
    rShuttle_Speed_mms := 0.0;
END_IF;


(* ==========================================================================================
 * PHASE 8: ISA-18.2 MULTI-TIERED ALARM ENGINE & DIAGNOSTIC WORD PACKING
 * Hierarchy:
 *   Priority 1: Critical Safety Alarms (Emergency Abort, Slam Dump, E-Stop)
 *   Priority 2: Warning & Disinfection Quality Alarms (H/L Trip, Degradation)
 *   Priority 3: Advisory & Maintenance Alarms (Filter Backwash, Tube Fatigue)
 * ========================================================================================== *)

(* ------------------------------------------------------------------------------------------
 * 8.1: PRIORITY 1 - CRITICAL SAFETY ALARMS (Slam Dump & Immediate Abort)
 * ------------------------------------------------------------------------------------------ *)
(* Bit 0: Hydraulic Ram Overpressure HH (> 53.0 bar) *)
IF rTMR4_VotedVal >= rHydraulicPress_HH_Trip THEN
    tAlarmTimer_PressHH := tAlarmTimer_PressHH + rDeltaTime_s;
    IF tAlarmTimer_PressHH >= 0.20 THEN
        dwISAAlarmWord_Critical := dwISAAlarmWord_Critical OR 16#00000001;
        bAlarm_AnyCritical := TRUE;
        bValve_EmergencyDump_Open := TRUE;
        IF iState <> 12 THEN
            iPrevState := iState;
            iState := 12;
            tStateTimer_s := 0.0;
            bStateFirstScan := TRUE;
        END_IF;
    END_IF;
ELSIF rTMR4_VotedVal <= (rHydraulicPress_HH_Trip - rHydraulicPress_Deadband) THEN
    tAlarmTimer_PressHH := 0.0;
END_IF;

(* Bit 1: Wash Zone Temperature Overheat HH (> 93.0 deg C, Boiling/Cavitation Risk) *)
IF rTMR1_VotedVal >= rWashTemp_HH_Trip THEN
    tAlarmTimer_TempHH := tAlarmTimer_TempHH + rDeltaTime_s;
    IF tAlarmTimer_TempHH >= 1.0 THEN
        dwISAAlarmWord_Critical := dwISAAlarmWord_Critical OR 16#00000002;
        bAlarm_AnyCritical := TRUE;
        bValve_SteamIsolation_Open := FALSE; (* Isolate steam immediately *)
    END_IF;
ELSIF rTMR1_VotedVal <= (rWashTemp_HH_Trip - rWashTemp_Deadband) THEN
    tAlarmTimer_TempHH := 0.0;
END_IF;

(* Bit 2: Reclaim Tank Overflow HH (> 95.0 %) *)
IF rTMR2_VotedVal >= rReclaimLvl_HH_Trip THEN
    tAlarmTimer_LvlHH := tAlarmTimer_LvlHH + rDeltaTime_s;
    IF tAlarmTimer_LvlHH >= 1.5 THEN
        dwISAAlarmWord_Critical := dwISAAlarmWord_Critical OR 16#00000004;
        bAlarm_AnyCritical := TRUE;
        rValve_FreshWater_pct := 0.0; (* Cut off makeup water *)
    END_IF;
ELSIF rTMR2_VotedVal <= (rReclaimLvl_HH_Trip - rReclaimLvl_Deadband) THEN
    tAlarmTimer_LvlHH := 0.0;
END_IF;

(* Bit 3: Membrane Bladder Rupture Discrepancy HH *)
IF tAlarmTimer_BladderDiff >= 0.5 THEN
    dwISAAlarmWord_Critical := dwISAAlarmWord_Critical OR 16#00000008;
    bAlarm_AnyCritical := TRUE;
END_IF;

(* Bit 4: Hardware Emergency Stop Active *)
IF NOT bEmergencyStop THEN
    dwISAAlarmWord_Critical := dwISAAlarmWord_Critical OR 16#00000010;
    bAlarm_AnyCritical := TRUE;
END_IF;

(* Bit 5: Press Safety Enclosure Violation *)
IF NOT bPressGuard_Locked AND ((iState = 8) OR (iState = 9)) THEN
    dwISAAlarmWord_Critical := dwISAAlarmWord_Critical OR 16#00000020;
    bAlarm_AnyCritical := TRUE;
END_IF;

(* Bit 6: Optical Light Curtain Safety Intrusion *)
IF NOT bLightCurtain_Clear THEN
    dwISAAlarmWord_Critical := dwISAAlarmWord_Critical OR 16#00000040;
END_IF;

(* Bit 7: Complete TMR Sensor Loss (Health Grade = 0) *)
IF (iTMR1_HealthGrade = 0) OR (iTMR4_HealthGrade = 0) THEN
    dwISAAlarmWord_Critical := dwISAAlarmWord_Critical OR 16#00000080;
    bAlarm_AnyCritical := TRUE;
END_IF;


(* ------------------------------------------------------------------------------------------
 * 8.2: PRIORITY 2 - WARNING & DISINFECTION QUALITY ALARMS
 * ------------------------------------------------------------------------------------------ *)
(* Bit 0: Hydraulic Ram Pressure High Warning H (> 48.0 bar) *)
IF (rTMR4_VotedVal >= rHydraulicPress_H_Trip) AND (rTMR4_VotedVal < rHydraulicPress_HH_Trip) THEN
    dwISAAlarmWord_Warning := dwISAAlarmWord_Warning OR 16#00000001;
    bAlarm_AnyWarning := TRUE;
ELSIF rTMR4_VotedVal <= (rHydraulicPress_H_Trip - rHydraulicPress_Deadband) THEN
    dwISAAlarmWord_Warning := dwISAAlarmWord_Warning AND 16#FFFFFFFE;
END_IF;

(* Bit 1: Wash Temperature High Warning H (> 88.0 deg C) *)
IF (rTMR1_VotedVal >= rWashTemp_H_Trip) AND (rTMR1_VotedVal < rWashTemp_HH_Trip) THEN
    dwISAAlarmWord_Warning := dwISAAlarmWord_Warning OR 16#00000002;
    bAlarm_AnyWarning := TRUE;
ELSIF rTMR1_VotedVal <= (rWashTemp_H_Trip - rWashTemp_Deadband) THEN
    dwISAAlarmWord_Warning := dwISAAlarmWord_Warning AND 16#FFFFFFFD;
END_IF;

(* Bit 2: Main Wash Low Disinfection Temperature Warning L (< 72.0 deg C during wash) *)
IF (iState = 5) AND (tStateTimer_s >= 40.0) AND (rTMR1_VotedVal < rWashTemp_L_Trip) THEN
    dwISAAlarmWord_Warning := dwISAAlarmWord_Warning OR 16#00000004;
    bAlarm_AnyWarning := TRUE;
ELSIF rTMR1_VotedVal >= (rWashTemp_L_Trip + rWashTemp_Deadband) THEN
    dwISAAlarmWord_Warning := dwISAAlarmWord_Warning AND 16#FFFFFFFB;
END_IF;

(* Bit 3: Critical Disinfection Failure LL (< 45.0 deg C during wash) *)
IF (iState = 5) AND (tStateTimer_s >= 60.0) AND (rTMR1_VotedVal < rWashTemp_LL_Trip) THEN
    tAlarmTimer_TempLL := tAlarmTimer_TempLL + rDeltaTime_s;
    IF tAlarmTimer_TempLL >= 5.0 THEN
        dwISAAlarmWord_Warning := dwISAAlarmWord_Warning OR 16#00000008;
        bAlarm_AnyWarning := TRUE;
    END_IF;
ELSE
    tAlarmTimer_TempLL := 0.0;
END_IF;

(* Bit 4: Reclaim Tank High Warning H (> 88.0 %) *)
IF (rTMR2_VotedVal >= rReclaimLvl_H_Trip) AND (rTMR2_VotedVal < rReclaimLvl_HH_Trip) THEN
    dwISAAlarmWord_Warning := dwISAAlarmWord_Warning OR 16#00000010;
ELSIF rTMR2_VotedVal <= (rReclaimLvl_H_Trip - rReclaimLvl_Deadband) THEN
    dwISAAlarmWord_Warning := dwISAAlarmWord_Warning AND 16#FFFFFFEF;
END_IF;

(* Bit 5: Reclaim Tank Low Warning L (< 25.0 %) *)
IF rTMR2_VotedVal <= rReclaimLvl_L_Trip THEN
    dwISAAlarmWord_Warning := dwISAAlarmWord_Warning OR 16#00000020;
    bAlarm_AnyWarning := TRUE;
ELSIF rTMR2_VotedVal >= (rReclaimLvl_L_Trip + rReclaimLvl_Deadband) THEN
    dwISAAlarmWord_Warning := dwISAAlarmWord_Warning AND 16#FFFFFFDF;
END_IF;

(* Bit 6: Reclaim Water Severe Turbidity (> 150.0 NTU Auto Drain Divert) *)
IF rTMR6_VotedVal >= rTurbidity_Severe_Trip THEN
    dwISAAlarmWord_Warning := dwISAAlarmWord_Warning OR 16#00000040;
    bAlarm_AnyWarning := TRUE;
ELSIF rTMR6_VotedVal <= (rTurbidity_Severe_Trip - rTurbidity_Deadband) THEN
    dwISAAlarmWord_Warning := dwISAAlarmWord_Warning AND 16#FFFFFFBF;
END_IF;

(* Bit 7: Wash Bath Conductivity High Warning (> 18,000 uS/cm) *)
IF rCond_Normalized_uS >= 18000.0 THEN
    dwISAAlarmWord_Warning := dwISAAlarmWord_Warning OR 16#00000080;
ELSIF rCond_Normalized_uS <= 16500.0 THEN
    dwISAAlarmWord_Warning := dwISAAlarmWord_Warning AND 16#FFFFFF7F;
END_IF;

(* Bit 8: Wash Bath Conductivity Low Warning (< 7,000 uS/cm during wash) *)
IF (iState = 5) AND (tStateTimer_s >= 30.0) AND (rCond_Normalized_uS <= 7000.0) THEN
    dwISAAlarmWord_Warning := dwISAAlarmWord_Warning OR 16#00000100;
ELSIF rCond_Normalized_uS >= 8500.0 THEN
    dwISAAlarmWord_Warning := dwISAAlarmWord_Warning AND 16#FFFFFEFF;
END_IF;

(* Bit 9: Rinse Bath Neutralization pH Out of Range (pH < 5.0 OR pH > 8.0) *)
IF (iState = 7) AND (tStateTimer_s >= 40.0) AND ((rPH_RinseBath < 5.0) OR (rPH_RinseBath > 8.0)) THEN
    dwISAAlarmWord_Warning := dwISAAlarmWord_Warning OR 16#00000200;
    bAlarm_AnyWarning := TRUE;
ELSE
    dwISAAlarmWord_Warning := dwISAAlarmWord_Warning AND 16#FFFFFDFF;
END_IF;

(* Bit 10: Plate Heat Exchanger Severe Fouling High DP Switch *)
IF NOT bHEX_HighDP_Switch THEN
    dwISAAlarmWord_Warning := dwISAAlarmWord_Warning OR 16#00000400;
ELSE
    dwISAAlarmWord_Warning := dwISAAlarmWord_Warning AND 16#FFFFFBFF;
END_IF;

(* Bit 11: Single TMR Sensor Fault Active (Channel Degradation) *)
IF bTMR1_FaultA OR bTMR1_FaultB OR bTMR1_FaultC OR
   bTMR2_FaultA OR bTMR2_FaultB OR bTMR2_FaultC OR
   bTMR3_FaultA OR bTMR3_FaultB OR bTMR3_FaultC OR
   bTMR4_FaultA OR bTMR4_FaultB OR bTMR4_FaultC OR
   bTMR5_FaultA OR bTMR5_FaultB OR bTMR5_FaultC OR
   bTMR6_FaultA OR bTMR6_FaultB OR bTMR6_FaultC THEN
    dwISAAlarmWord_Warning := dwISAAlarmWord_Warning OR 16#00000800;
ELSE
    dwISAAlarmWord_Warning := dwISAAlarmWord_Warning AND 16#FFFFF7FF;
END_IF;


(* ------------------------------------------------------------------------------------------
 * 8.3: PRIORITY 3 - ADVISORY & PREVENTIVE MAINTENANCE ALARMS
 * ------------------------------------------------------------------------------------------ *)
(* Bit 0: Greywater Drum Screen Filter Backwash Required (DP > 450 mbar) *)
IF rDP_GreywaterFilter_mbar >= 450.0 THEN
    dwISAAlarmWord_Advisory := dwISAAlarmWord_Advisory OR 16#00000001;
ELSE
    dwISAAlarmWord_Advisory := dwISAAlarmWord_Advisory AND 16#FFFFFFFE;
END_IF;

(* Bit 1: Peristaltic Dosing Tubing Wear Exceeded 85% Life *)
IF (rPeristaltic_WearRatio[1] >= 0.85) OR (rPeristaltic_WearRatio[2] >= 0.85) OR
   (rPeristaltic_WearRatio[3] >= 0.85) OR (rPeristaltic_WearRatio[4] >= 0.85) OR
   (rPeristaltic_WearRatio[5] >= 0.85) OR (rPeristaltic_WearRatio[7] >= 0.85) OR
   (rPeristaltic_WearRatio[9] >= 0.85) THEN
    dwISAAlarmWord_Advisory := dwISAAlarmWord_Advisory OR 16#00000002;
ELSE
    dwISAAlarmWord_Advisory := dwISAAlarmWord_Advisory AND 16#FFFFFFFD;
END_IF;

(* Bit 2: Plate Heat Exchanger Thermal Degradation (U < 2500 W/(m2*K)) *)
IF (rPHE_HeatTransferCoeff_U < 2500.0) AND (rPHE_HeatTransfer_kW > 20.0) THEN
    dwISAAlarmWord_Advisory := dwISAAlarmWord_Advisory OR 16#00000004;
ELSE
    dwISAAlarmWord_Advisory := dwISAAlarmWord_Advisory AND 16#FFFFFFFB;
END_IF;

(* Bit 3: Slow Cake Dewatering Consolidation Advisory *)
IF (iState = 9) AND (tStateTimer_s >= 85.0) AND (rConsolidationRate_pct_s > -0.05) AND
   (rEstimatedCakeMoisture_pct > (rTargetMoisture_pct + 8.0)) THEN
    dwISAAlarmWord_Advisory := dwISAAlarmWord_Advisory OR 16#00000008;
ELSE
    dwISAAlarmWord_Advisory := dwISAAlarmWord_Advisory AND 16#FFFFFFF7;
END_IF;

(* Acknowledge Alarms Handling *)
IF bAckAlarms THEN
    dwISAAlarmWord_Warning  := dwISAAlarmWord_Warning AND 16#00000000;
    dwISAAlarmWord_Advisory := dwISAAlarmWord_Advisory AND 16#00000000;
    bAlarm_AnyWarning := FALSE;
END_IF;


(* ------------------------------------------------------------------------------------------
 * 8.4: DIAGNOSTIC STATUS WORD PACKING
 * ------------------------------------------------------------------------------------------ *)
(* dwSystemStatusWord Serialization:
 * Bits 0..3 : Current FSM State Code [1..12]
 * Bit 4     : bAutoMode Active
 * Bit 5     : bReadyForNextBatch
 * Bit 6     : bCycleComplete Pulse
 * Bit 7     : bEmergencyStop Healthy
 * Bit 8     : bPressGuard_Locked
 * Bit 9     : bLightCurtain_Clear
 * Bit 10    : bDrumHome_Position
 * Bit 11    : bCakeDischarged_Detect
 * Bit 12    : bValve_ReclaimDivertToDrain (Sewer Active)
 * Bit 13    : bValve_SteamIsolation_Open
 * Bit 14    : bValve_EmergencyDump_Open
 * Bit 15    : bMembraneBladder_RuptureSwitch Healthy *)
dwSystemStatusWord := INT_TO_DWORD(iState) AND 16#0000000F;
IF bAutoMode THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00000010; END_IF;
IF bReadyForNextBatch THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00000020; END_IF;
IF bCycleComplete THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00000040; END_IF;
IF bEmergencyStop THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00000080; END_IF;
IF bPressGuard_Locked THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00000100; END_IF;
IF bLightCurtain_Clear THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00000200; END_IF;
IF bDrumHome_Position THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00000400; END_IF;
IF bCakeDischarged_Detect THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00000800; END_IF;
IF bValve_ReclaimDivertToDrain THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00001000; END_IF;
IF bValve_SteamIsolation_Open THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00002000; END_IF;
IF bValve_EmergencyDump_Open THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00004000; END_IF;
IF bMembraneBladder_RuptureSwitch THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00008000; END_IF;

(* dwTMRStatusWord Serialization: Health Grades & Faults for 6 Groups *)
dwTMRStatusWord := SHL(INT_TO_DWORD(iTMR1_HealthGrade), 0)  OR
                   SHL(INT_TO_DWORD(iTMR2_HealthGrade), 3)  OR
                   SHL(INT_TO_DWORD(iTMR3_HealthGrade), 6)  OR
                   SHL(INT_TO_DWORD(iTMR4_HealthGrade), 9)  OR
                   SHL(INT_TO_DWORD(iTMR5_HealthGrade), 12) OR
                   SHL(INT_TO_DWORD(iTMR6_HealthGrade), 15);

(* dwActuatorStatusWord Serialization: Echo Feedback of Actuator Commands *)
dwActuatorStatusWord := 16#00000000;
IF rValve_SteamDirect_pct > 0.5 THEN dwActuatorStatusWord := dwActuatorStatusWord OR 16#00000001; END_IF;
IF rValve_FreshWater_pct > 0.5 THEN dwActuatorStatusWord := dwActuatorStatusWord OR 16#00000002; END_IF;
IF rPump_ReclaimRecirc_pct > 0.5 THEN dwActuatorStatusWord := dwActuatorStatusWord OR 16#00000004; END_IF;
IF rDosing_Alkali_Lmin > 0.1 THEN dwActuatorStatusWord := dwActuatorStatusWord OR 16#00000008; END_IF;
IF rDosing_Detergent_Lmin > 0.1 THEN dwActuatorStatusWord := dwActuatorStatusWord OR 16#00000010; END_IF;
IF rDosing_Bleach_Lmin > 0.1 THEN dwActuatorStatusWord := dwActuatorStatusWord OR 16#00000020; END_IF;
IF rDosing_AcidSour_Lmin > 0.1 THEN dwActuatorStatusWord := dwActuatorStatusWord OR 16#00000040; END_IF;
IF rDosing_Softener_Lmin > 0.1 THEN dwActuatorStatusWord := dwActuatorStatusWord OR 16#00000080; END_IF;
IF rPress_ProportionalPressure_bar > 1.0 THEN dwActuatorStatusWord := dwActuatorStatusWord OR 16#00000100; END_IF;
IF rDrum_DriveSpeed_RPM > 0.1 THEN dwActuatorStatusWord := dwActuatorStatusWord OR 16#00000200; END_IF;
IF bPump_GreywaterBackwash_Start THEN dwActuatorStatusWord := dwActuatorStatusWord OR 16#00000400; END_IF;
IF bPress_BottomPlateLift_Up THEN dwActuatorStatusWord := dwActuatorStatusWord OR 16#00000800; END_IF;
IF bPress_PneumaticEjector_Active THEN dwActuatorStatusWord := dwActuatorStatusWord OR 16#00001000; END_IF;
IF bShuttle_TraverseForward OR bShuttle_TraverseReverse THEN dwActuatorStatusWord := dwActuatorStatusWord OR 16#00002000; END_IF;
IF bShuttle_DischargeRollers_Run THEN dwActuatorStatusWord := dwActuatorStatusWord OR 16#00004000; END_IF;


(* ==========================================================================================
 * PHASE 9: ACTUATOR OUTPUT SATURATION, FIRST-ORDER SLEW-RATE LIMITING & SAFE CLAMPING
 * ========================================================================================== *)
(* 1. Direct Saturated Steam Valve Slew Rate Limiter (Max 10% / second) *)
rTempSum := rValve_SteamDirect_pct - rValve_Steam_Filtered;
IF rTempSum > (rValve_Steam_SlewLimit * rDeltaTime_s) THEN
    rValve_Steam_Filtered := rValve_Steam_Filtered + (rValve_Steam_SlewLimit * rDeltaTime_s);
ELSIF rTempSum < -(rValve_Steam_SlewLimit * rDeltaTime_s) THEN
    rValve_Steam_Filtered := rValve_Steam_Filtered - (rValve_Steam_SlewLimit * rDeltaTime_s);
ELSE
    rValve_Steam_Filtered := rValve_SteamDirect_pct;
END_IF;
rValve_SteamDirect_pct := LIMIT(0.0, rValve_Steam_Filtered, 100.0);

(* 2. 50-Bar Hydraulic Press Ram Proportional Pressure Relief Slew Rate Limiter (Max 15 bar/s) *)
rTempSum := rPress_ProportionalPressure_bar - rPress_Hyd_Filtered;
IF rTempSum > (rPress_Hyd_SlewLimit * rDeltaTime_s) THEN
    rPress_Hyd_Filtered := rPress_Hyd_Filtered + (rPress_Hyd_SlewLimit * rDeltaTime_s);
ELSIF rTempSum < -(rPress_Hyd_SlewLimit * rDeltaTime_s) THEN
    rPress_Hyd_Filtered := rPress_Hyd_Filtered - (rPress_Hyd_SlewLimit * rDeltaTime_s);
ELSE
    rPress_Hyd_Filtered := rPress_ProportionalPressure_bar;
END_IF;
rPress_ProportionalPressure_bar := LIMIT(0.0, rPress_Hyd_Filtered, 55.0);

(* 3. Chemical Dosing Pump Command Clamping *)
rDosing_Alkali_Lmin    := LIMIT(0.0, rDosing_Alkali_Lmin, 25.0);
rDosing_Detergent_Lmin := LIMIT(0.0, rDosing_Detergent_Lmin, 15.0);
rDosing_Bleach_Lmin    := LIMIT(0.0, rDosing_Bleach_Lmin, 10.0);
rDosing_AcidSour_Lmin  := LIMIT(0.0, rDosing_AcidSour_Lmin, 10.0);
rDosing_Softener_Lmin  := LIMIT(0.0, rDosing_Softener_Lmin, 8.0);
rDosing_Alkali_Filtered := rDosing_Alkali_Lmin;
rDosing_Acid_Filtered   := rDosing_AcidSour_Lmin;

(* 4. Water Valves & Drum Speeds Clamping *)
rValve_FreshWater_pct   := LIMIT(0.0, rValve_FreshWater_pct, 100.0);
rPump_ReclaimRecirc_pct := LIMIT(0.0, rPump_ReclaimRecirc_pct, 100.0);
rDrum_DriveSpeed_RPM    := LIMIT(0.0, rDrum_DriveSpeed_RPM, 12.0);
rShuttle_Speed_mms      := LIMIT(0.0, rShuttle_Speed_mms, 500.0);

(* 5. Master Safety Override Enforcement *)
IF (iState = 12) OR NOT bEnable OR NOT bEmergencyStop THEN
    rValve_SteamDirect_pct          := 0.0;
    rPress_ProportionalPressure_bar := 0.0;
    rPress_RamSpeed_mms             := 0.0;
    rDrum_DriveSpeed_RPM            := 0.0;
    rShuttle_Speed_mms              := 0.0;
    rValve_FreshWater_pct           := 0.0;
    rPump_ReclaimRecirc_pct         := 0.0;
    rDosing_Alkali_Lmin             := 0.0;
    rDosing_Detergent_Lmin          := 0.0;
    rDosing_Bleach_Lmin             := 0.0;
    rDosing_AcidSour_Lmin           := 0.0;
    rDosing_Softener_Lmin           := 0.0;
    bValve_EmergencyDump_Open       := TRUE;
    bValve_SteamIsolation_Open      := FALSE;
    bPress_BottomPlateLift_Up       := FALSE;
    bPress_PneumaticEjector_Active  := FALSE;
    bShuttle_TraverseForward        := FALSE;
    bShuttle_TraverseReverse        := FALSE;
    bShuttle_DischargeRollers_Run   := FALSE;
END_IF;

END_FUNCTION_BLOCK
'''

if __name__ == "__main__":
    p6 = get_part6()
    print(f"Part 6 length: {len(p6)} characters")
