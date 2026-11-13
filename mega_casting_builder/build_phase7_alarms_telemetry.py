# mega_casting_builder/build_phase7_alarms_telemetry.py

def get_phase7_alarms_telemetry():
    return """(* =====================================================================================================================
 * PHASE 7: ISA-18.2 MULTI-TIER PROCESS ALARM MATRIX, FIRST-OUT FORENSICS & 32-BIT DWORD BIT-PACKING
 * HH/H/L/LL trips with hysteresis deadbands + complete bit-level packing for SCADA/MES telemetry
 * ===================================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------------------------
 * 1. ISA-18.2 PROCESS ALARM EVALUATION ENGINE WITH DEADBAND HYSTERESIS
 * --------------------------------------------------------------------------------------------------------------------- *)

(* 1.1 Hydraulic Shot Cylinder Head Pressure Alarms *)
IF rHeadPress_Voted >= rTrip_HeadPress_HH THEN
    bAlarm_HeadPress_HH := TRUE;
    IF NOT bFirstOut_Latched THEN
        bFirstOut_Latched := TRUE;
        dwFirstOut_Code := 16#00000001; (* Code 1: Head Pressure HH Overpressure *)
    END_IF;
ELSIF rHeadPress_Voted <= (rTrip_HeadPress_HH - rDeadband_HeadPress) THEN
    bAlarm_HeadPress_HH := FALSE;
END_IF;

IF rHeadPress_Voted >= rTrip_HeadPress_H THEN
    bAlarm_HeadPress_H := TRUE;
ELSIF rHeadPress_Voted <= (rTrip_HeadPress_H - rDeadband_HeadPress) THEN
    bAlarm_HeadPress_H := FALSE;
END_IF;

(* 1.2 In-Cavity Dynamic Piezoelectric Pressure Alarms *)
IF rCavityPress_Voted >= rTrip_CavityPress_HH THEN
    bAlarm_CavityPress_HH := TRUE;
    IF NOT bFirstOut_Latched THEN
        bFirstOut_Latched := TRUE;
        dwFirstOut_Code := 16#00000002; (* Code 2: Cavity Pressure HH *)
    END_IF;
ELSIF rCavityPress_Voted <= (rTrip_CavityPress_HH - rDeadband_CavityPress) THEN
    bAlarm_CavityPress_HH := FALSE;
END_IF;

IF rCavityPress_Voted >= rTrip_CavityPress_H THEN
    bAlarm_CavityPress_H := TRUE;
ELSIF rCavityPress_Voted <= (rTrip_CavityPress_H - rDeadband_CavityPress) THEN
    bAlarm_CavityPress_H := FALSE;
END_IF;

(* 1.3 Plunger Axial Velocity Overspeed Alarms *)
IF rPlungerVel_Filtered >= rTrip_PlungerVel_HH THEN
    bAlarm_PlungerVel_HH := TRUE;
    IF NOT bFirstOut_Latched THEN
        bFirstOut_Latched := TRUE;
        dwFirstOut_Code := 16#00000003; (* Code 3: Plunger Runaway Overspeed HH *)
    END_IF;
ELSIF rPlungerVel_Filtered <= (rTrip_PlungerVel_HH - rDeadband_PlungerVel) THEN
    bAlarm_PlungerVel_HH := FALSE;
END_IF;

IF rPlungerVel_Filtered >= rTrip_PlungerVel_H THEN
    bAlarm_PlungerVel_H := TRUE;
ELSIF rPlungerVel_Filtered <= (rTrip_PlungerVel_H - rDeadband_PlungerVel) THEN
    bAlarm_PlungerVel_H := FALSE;
END_IF;

(* 1.4 Parting Plane Evacuation Absolute Vacuum Alarms *)
IF (iFSM_State >= 4 AND iFSM_State <= 7) THEN
    IF rVacPressure_Voted >= rTrip_Vac_LL THEN
        bAlarm_Vac_LL := TRUE;
        IF NOT bFirstOut_Latched THEN
            bFirstOut_Latched := TRUE;
            dwFirstOut_Code := 16#00000004; (* Code 4: Vacuum Drawdown Failure LL *)
        END_IF;
    ELSIF rVacPressure_Voted <= (rTrip_Vac_LL - rDeadband_Vac) THEN
        bAlarm_Vac_LL := FALSE;
    END_IF;

    IF rVacPressure_Voted >= rTrip_Vac_L THEN
        bAlarm_Vac_L := TRUE;
    ELSIF rVacPressure_Voted <= (rTrip_Vac_L - rDeadband_Vac) THEN
        bAlarm_Vac_L := FALSE;
    END_IF;
ELSE
    bAlarm_Vac_LL := FALSE;
    bAlarm_Vac_L  := FALSE;
END_IF;

(* 1.5 Toggle Clamping Force Tonnage Underload & Overload Alarms *)
IF rTotalClampingForce_kN >= rTrip_Clamp_HH THEN
    bAlarm_Clamp_HH := TRUE;
    IF NOT bFirstOut_Latched THEN
        bFirstOut_Latched := TRUE;
        dwFirstOut_Code := 16#00000005; (* Code 5: Clamping Force Overload HH *)
    END_IF;
ELSIF rTotalClampingForce_kN <= (rTrip_Clamp_HH - rDeadband_Clamp) THEN
    bAlarm_Clamp_HH := FALSE;
END_IF;

IF (iFSM_State >= 5 AND iFSM_State <= 8) THEN
    IF rTotalClampingForce_kN <= rTrip_Clamp_LL THEN
        bAlarm_Clamp_LL := TRUE;
        IF NOT bFirstOut_Latched THEN
            bFirstOut_Latched := TRUE;
            dwFirstOut_Code := 16#00000006; (* Code 6: Clamping Force Loss / Flash Risk LL *)
        END_IF;
    ELSIF rTotalClampingForce_kN >= (rTrip_Clamp_LL + rDeadband_Clamp) THEN
        bAlarm_Clamp_LL := FALSE;
    END_IF;
ELSE
    bAlarm_Clamp_LL := FALSE;
END_IF;

(* 1.6 Platen Tilt Parallelism Deflection Alarms *)
IF rPlatenTilt_Parallelism_um >= rTrip_PlatenTilt_HH THEN
    bAlarm_PlatenTilt_HH := TRUE;
    IF NOT bFirstOut_Latched THEN
        bFirstOut_Latched := TRUE;
        dwFirstOut_Code := 16#00000007; (* Code 7: Platen Destructive Angular Tilt HH *)
    END_IF;
ELSIF rPlatenTilt_Parallelism_um <= (rTrip_PlatenTilt_HH - rDeadband_PlatenTilt) THEN
    bAlarm_PlatenTilt_HH := FALSE;
END_IF;

IF rPlatenTilt_Parallelism_um >= rTrip_PlatenTilt_H THEN
    bAlarm_PlatenTilt_H := TRUE;
ELSIF rPlatenTilt_Parallelism_um <= (rTrip_PlatenTilt_H - rDeadband_PlatenTilt) THEN
    bAlarm_PlatenTilt_H := FALSE;
END_IF;

(* 1.7 Casting Biscuit Thickness Integrity Alarms *)
IF (iFSM_State = 8) THEN
    IF rBiscuitThickness_Actual_mm >= rTrip_Biscuit_HH THEN
        bAlarm_Biscuit_HH := TRUE;
        IF NOT bFirstOut_Latched THEN
            bFirstOut_Latched := TRUE;
            dwFirstOut_Code := 16#00000008; (* Code 8: Biscuit Thickness HH *)
        END_IF;
    ELSIF rBiscuitThickness_Actual_mm <= (rTrip_Biscuit_HH - rDeadband_Biscuit) THEN
        bAlarm_Biscuit_HH := FALSE;
    END_IF;

    IF rBiscuitThickness_Actual_mm <= rTrip_Biscuit_LL THEN
        bAlarm_Biscuit_LL := TRUE;
        IF NOT bFirstOut_Latched THEN
            bFirstOut_Latched := TRUE;
            dwFirstOut_Code := 16#00000009; (* Code 9: Biscuit Thickness LL Starvation *)
        END_IF;
    ELSIF rBiscuitThickness_Actual_mm >= (rTrip_Biscuit_LL + rDeadband_Biscuit) THEN
        bAlarm_Biscuit_LL := FALSE;
    END_IF;
END_IF;

(* 1.8 Metal Flash Liquid Alloy Blowout Breach Detector *)
IF (iFSM_State >= 6 AND iFSM_State <= 8) THEN
    IF (rPlatenTilt_Parallelism_um >= 135.0) AND (rCavityPress_Voted >= 180.0) AND (rVac_LeakRate_Actual_mbar_s >= 40.0) THEN
        bAlarm_FlashBlowout_Detected := TRUE;
        IF NOT bFirstOut_Latched THEN
            bFirstOut_Latched := TRUE;
            dwFirstOut_Code := 16#0000000A; (* Code 10: Molten Flash Blowout Breach *)
        END_IF;
    END_IF;
END_IF;

(* 1.9 Emergency Stop & Safety Gate Alarms *)
IF NOT bEmergencyStop THEN
    bAlarm_EmergencyStop_Active := TRUE;
    IF NOT bFirstOut_Latched THEN
        bFirstOut_Latched := TRUE;
        dwFirstOut_Code := 16#0000000B; (* Code 11: Emergency Stop Trip *)
    END_IF;
ELSE
    bAlarm_EmergencyStop_Active := FALSE;
END_IF;

IF NOT bSafetyGate_Closed THEN
    bAlarm_SafetyGate_Breach := TRUE;
    IF NOT bFirstOut_Latched THEN
        bFirstOut_Latched := TRUE;
        dwFirstOut_Code := 16#0000000C; (* Code 12: Safety Gate Interlock Open *)
    END_IF;
ELSE
    bAlarm_SafetyGate_Breach := FALSE;
END_IF;

(* Master Warning & Fault Aggregation *)
bGeneralFault := bAlarm_HeadPress_HH OR bAlarm_CavityPress_HH OR bAlarm_PlungerVel_HH OR
                 bAlarm_Vac_LL OR bAlarm_Clamp_LL OR bAlarm_Clamp_HH OR bAlarm_PlatenTilt_HH OR
                 bAlarm_FlashBlowout_Detected OR bAlarm_EmergencyStop_Active OR
                 bAlarm_Plunger_TMR_Fault OR bAlarm_HeadPress_TMR_Fault OR
                 bAlarm_CavityPress_TMR_Fault OR bAlarm_Vac_TMR_Fault;

bGeneralWarning := bAlarm_HeadPress_H OR bAlarm_CavityPress_H OR bAlarm_PlungerVel_H OR
                   bAlarm_Vac_L OR bAlarm_PlatenTilt_H OR bAlarm_Biscuit_HH OR
                   bAlarm_Biscuit_LL OR bAlarm_IntensificationDelay_HH OR
                   (iPlunger_TMR_HealthMode < 3) OR (iHeadPress_TMR_HealthMode < 3) OR
                   (iCavityPress_TMR_HealthMode < 3) OR (iVac_TMR_HealthMode < 3);

(* ---------------------------------------------------------------------------------------------------------------------
 * 2. 32-BIT BIT-PACKED TELEMETRY WORDS
 * --------------------------------------------------------------------------------------------------------------------- *)

(* 2.1 dwStatusWord1: Machine Operational Telemetry & State Machine Mapping *)
dwStatusWord1 := 16#00000000;
IF bEnable                          THEN dwStatusWord1 := dwStatusWord1 OR 16#00000001; END_IF;
IF bEmergencyStop                   THEN dwStatusWord1 := dwStatusWord1 OR 16#00000002; END_IF;
IF bSafetyGate_Closed               THEN dwStatusWord1 := dwStatusWord1 OR 16#00000004; END_IF;
IF bRobot_Extractor_Home            THEN dwStatusWord1 := dwStatusWord1 OR 16#00000008; END_IF;
IF bRobot_Spray_Home                THEN dwStatusWord1 := dwStatusWord1 OR 16#00000010; END_IF;
IF bCorePins_Advanced_Permissive    THEN dwStatusWord1 := dwStatusWord1 OR 16#00000020; END_IF;
IF bCorePins_Retracted_Permissive   THEN dwStatusWord1 := dwStatusWord1 OR 16#00000040; END_IF;
IF bEjector_Retracted_Permissive    THEN dwStatusWord1 := dwStatusWord1 OR 16#00000080; END_IF;
IF bAccumulator_Charged_Permissive  THEN dwStatusWord1 := dwStatusWord1 OR 16#00000100; END_IF;
IF bPreheat_Balanced                THEN dwStatusWord1 := dwStatusWord1 OR 16#00000200; END_IF;
IF bLadle_Pour_Ready                THEN dwStatusWord1 := dwStatusWord1 OR 16#00000400; END_IF;
IF bClamp_Locked_Permissive         THEN dwStatusWord1 := dwStatusWord1 OR 16#00000800; END_IF;
IF bVacuum_Evacuated_Permissive     THEN dwStatusWord1 := dwStatusWord1 OR 16#00001000; END_IF;
IF bPhase1_Complete                 THEN dwStatusWord1 := dwStatusWord1 OR 16#00002000; END_IF;
IF bPhase2_Complete                 THEN dwStatusWord1 := dwStatusWord1 OR 16#00004000; END_IF;
IF bPhase3_Complete                 THEN dwStatusWord1 := dwStatusWord1 OR 16#00008000; END_IF;
IF bPhase4_Complete                 THEN dwStatusWord1 := dwStatusWord1 OR 16#00010000; END_IF;
IF bVacuum_Vented_Permissive        THEN dwStatusWord1 := dwStatusWord1 OR 16#00020000; END_IF;
IF bClamp_Open_Permissive           THEN dwStatusWord1 := dwStatusWord1 OR 16#00040000; END_IF;
IF bDemold_Ejection_Permissive      THEN dwStatusWord1 := dwStatusWord1 OR 16#00080000; END_IF;
IF bPart_Extracted_Permissive       THEN dwStatusWord1 := dwStatusWord1 OR 16#00100000; END_IF;
IF bDie_Sprayed_Permissive          THEN dwStatusWord1 := dwStatusWord1 OR 16#00200000; END_IF;
IF bCycleActive                     THEN dwStatusWord1 := dwStatusWord1 OR 16#00400000; END_IF;
IF bCycleComplete_Pulse             THEN dwStatusWord1 := dwStatusWord1 OR 16#00800000; END_IF;
(* Encode Current State Index (0..13) into Bits 24-27 *)
dwStatusWord1 := dwStatusWord1 OR SHL(INT_TO_DWORD(iFSM_State AND 16#0F), 24);
(* Encode Quality Grade into Bits 28-29 *)
dwStatusWord1 := dwStatusWord1 OR SHL(INT_TO_DWORD(iCasting_Quality_Grade AND 16#03), 28);
IF bGeneralWarning                  THEN dwStatusWord1 := dwStatusWord1 OR 16#40000000; END_IF;
IF bGeneralFault                    THEN dwStatusWord1 := dwStatusWord1 OR 16#80000000; END_IF;

(* 2.2 dwStatusWord2: Sensor TMR Health & Subsystem Telemetry *)
dwStatusWord2 := 16#00000000;
dwStatusWord2 := dwStatusWord2 OR SHL(INT_TO_DWORD(iPlunger_TMR_HealthMode AND 16#03), 0);
dwStatusWord2 := dwStatusWord2 OR SHL(INT_TO_DWORD(iHeadPress_TMR_HealthMode AND 16#03), 2);
dwStatusWord2 := dwStatusWord2 OR SHL(INT_TO_DWORD(iCavityPress_TMR_HealthMode AND 16#03), 4);
dwStatusWord2 := dwStatusWord2 OR SHL(INT_TO_DWORD(iVac_TMR_HealthMode AND 16#03), 6);
IF bPlunger_Sensor1_Healthy         THEN dwStatusWord2 := dwStatusWord2 OR 16#00000100; END_IF;
IF bPlunger_Sensor2_Healthy         THEN dwStatusWord2 := dwStatusWord2 OR 16#00000200; END_IF;
IF bPlunger_Sensor3_Healthy         THEN dwStatusWord2 := dwStatusWord2 OR 16#00000400; END_IF;
IF bHeadPress_Sensor1_Healthy       THEN dwStatusWord2 := dwStatusWord2 OR 16#00000800; END_IF;
IF bHeadPress_Sensor2_Healthy       THEN dwStatusWord2 := dwStatusWord2 OR 16#00001000; END_IF;
IF bHeadPress_Sensor3_Healthy       THEN dwStatusWord2 := dwStatusWord2 OR 16#00002000; END_IF;
IF bCavityPress_Sensor1_Healthy     THEN dwStatusWord2 := dwStatusWord2 OR 16#00004000; END_IF;
IF bCavityPress_Sensor2_Healthy     THEN dwStatusWord2 := dwStatusWord2 OR 16#00008000; END_IF;
IF bCavityPress_Sensor3_Healthy     THEN dwStatusWord2 := dwStatusWord2 OR 16#00010000; END_IF;
IF bVac_Sensor1_Healthy             THEN dwStatusWord2 := dwStatusWord2 OR 16#00020000; END_IF;
IF bVac_Sensor2_Healthy             THEN dwStatusWord2 := dwStatusWord2 OR 16#00040000; END_IF;
IF bVac_Sensor3_Healthy             THEN dwStatusWord2 := dwStatusWord2 OR 16#00080000; END_IF;
IF bStateSpace_Initialized          THEN dwStatusWord2 := dwStatusWord2 OR 16#00100000; END_IF;
IF bIntensification_Triggered       THEN dwStatusWord2 := dwStatusWord2 OR 16#00200000; END_IF;
IF bVacuumValve_Open_Cmd            THEN dwStatusWord2 := dwStatusWord2 OR 16#00400000; END_IF;
IF bVacuumPurge_N2_Cmd              THEN dwStatusWord2 := dwStatusWord2 OR 16#00800000; END_IF;
IF rPorosity_Risk_Index <= 0.20     THEN dwStatusWord2 := dwStatusWord2 OR 16#01000000; END_IF;
IF rPlatenTilt_Parallelism_um <= 95.0 THEN dwStatusWord2 := dwStatusWord2 OR 16#02000000; END_IF;

(* 2.3 dwAlarmWord1: ISA-18.2 Process Trip Alarms *)
dwAlarmWord1 := 16#00000000;
IF bAlarm_HeadPress_HH              THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000001; END_IF;
IF bAlarm_HeadPress_H               THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000002; END_IF;
IF bAlarm_CavityPress_HH            THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000004; END_IF;
IF bAlarm_CavityPress_H             THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000008; END_IF;
IF bAlarm_PlungerVel_HH             THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000010; END_IF;
IF bAlarm_PlungerVel_H              THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000020; END_IF;
IF bAlarm_Vac_LL                    THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000040; END_IF;
IF bAlarm_Vac_L                     THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000080; END_IF;
IF bAlarm_Clamp_HH                  THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000100; END_IF;
IF bAlarm_Clamp_LL                  THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000200; END_IF;
IF bAlarm_PlatenTilt_HH             THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000400; END_IF;
IF bAlarm_PlatenTilt_H              THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000800; END_IF;
IF bAlarm_Biscuit_HH                THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00001000; END_IF;
IF bAlarm_Biscuit_LL                THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00002000; END_IF;
IF bAlarm_IntensificationDelay_HH   THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00004000; END_IF;
IF bAlarm_FlashBlowout_Detected     THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00008000; END_IF;
IF bAlarm_EmergencyStop_Active      THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00010000; END_IF;
IF bAlarm_SafetyGate_Breach         THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00020000; END_IF;

(* 2.4 dwAlarmWord2: Sensor Discrepancy & Hardware Trips *)
dwAlarmWord2 := 16#00000000;
IF NOT bPlunger_Sensor1_Healthy     THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000001; END_IF;
IF NOT bPlunger_Sensor2_Healthy     THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000002; END_IF;
IF NOT bPlunger_Sensor3_Healthy     THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000004; END_IF;
IF bAlarm_Plunger_TMR_Fault         THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000008; END_IF;
IF NOT bHeadPress_Sensor1_Healthy   THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000010; END_IF;
IF NOT bHeadPress_Sensor2_Healthy   THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000020; END_IF;
IF NOT bHeadPress_Sensor3_Healthy   THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000040; END_IF;
IF bAlarm_HeadPress_TMR_Fault       THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000080; END_IF;
IF NOT bCavityPress_Sensor1_Healthy THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000100; END_IF;
IF NOT bCavityPress_Sensor2_Healthy THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000200; END_IF;
IF NOT bCavityPress_Sensor3_Healthy THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000400; END_IF;
IF bAlarm_CavityPress_TMR_Fault     THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000800; END_IF;
IF NOT bVac_Sensor1_Healthy         THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00001000; END_IF;
IF NOT bVac_Sensor2_Healthy         THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00002000; END_IF;
IF NOT bVac_Sensor3_Healthy         THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00004000; END_IF;
IF bAlarm_Vac_TMR_Fault             THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00008000; END_IF;

(* 2.5 dwFirstOutWord: Forensic Trip Latch *)
dwFirstOutWord := dwFirstOut_Code;
"""
