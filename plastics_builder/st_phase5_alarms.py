(* =====================================================================================================================
 * PHASE 5: ISA-18.2 MULTI-TIERED ALARM HIERARCHY & 32-BIT BIT-PACKED STATUS WORDS
 * Subsystems:
 *   5.1: Dynamic Rate-of-Change (ROC) Numerical Derivatives
 *   5.2: Multi-Tiered Alarm Trips & Warnings with Deadband Clearance Hysteresis
 *   5.3: 32-Bit Packed Diagnostic Status and Alarm Words
 *   5.4: Failsafe Emergency Interlocks & Actuator Safe Output Mapping
 * ===================================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------------------------
 * SUBSECTION 5.1: DYNAMIC RATE-OF-CHANGE (ROC) DERIVATIVES
 * --------------------------------------------------------------------------------------------------------------------- *)
(* Nozzle Melt Pressure ROC Filter *)
rTemp_A := (rMeltPres_Voted_Val - rMeltPres_Prev_Voted) / rScanTime_Ts;
rMeltPres_ROC := rMeltPres_ROC + (0.25 * (rTemp_A - rMeltPres_ROC));

(* Clamp Force ROC Filter *)
rTemp_B := (rTB_TotalClampForce - (x_State[6])) / rScanTime_Ts;
rClampForce_ROC := rClampForce_ROC + (0.20 * (rTemp_B - rClampForce_ROC));

(* ---------------------------------------------------------------------------------------------------------------------
 * SUBSECTION 5.2: ISA-18.2 MULTI-TIERED TRIP & WARNING EVALUATION WITH HYSTERESIS
 * --------------------------------------------------------------------------------------------------------------------- *)
(* Cavity Pressure Alarm Thresholds *)
IF rCavPres_Voted_Val >= rAlarm_CavPres_HH_Trip THEN
    bTrip_CavPres_HH := TRUE;
ELSIF rCavPres_Voted_Val < (rAlarm_CavPres_HH_Trip - rAlarm_CavPres_Hyst) THEN
    bTrip_CavPres_HH := FALSE;
END_IF;

IF rCavPres_Voted_Val >= rAlarm_CavPres_H_Warn THEN
    bWarn_CavPres_H := TRUE;
ELSIF rCavPres_Voted_Val < (rAlarm_CavPres_H_Warn - rAlarm_CavPres_Hyst) THEN
    bWarn_CavPres_H := FALSE;
END_IF;

IF (iFSM_State = 7) AND (rFSM_StateTimer > 1.0) AND (rCavPres_Voted_Val <= rAlarm_CavPres_L_Warn) THEN
    bWarn_CavPres_L := TRUE;
ELSIF rCavPres_Voted_Val > (rAlarm_CavPres_L_Warn + rAlarm_CavPres_Hyst) THEN
    bWarn_CavPres_L := FALSE;
END_IF;

IF (iFSM_State = 5) AND (rFSM_StateTimer > 2.0) AND (rCavPres_Voted_Val <= rAlarm_CavPres_LL_Trip) THEN
    bTrip_CavPres_LL := TRUE;
ELSIF rCavPres_Voted_Val > (rAlarm_CavPres_LL_Trip + rAlarm_CavPres_Hyst) THEN
    bTrip_CavPres_LL := FALSE;
END_IF;

IF rCavPres_Derivative >= rAlarm_CavPres_ROC_Trip THEN
    bTrip_CavPres_ROC := TRUE;
END_IF;

(* Melt Nozzle Pressure Alarm Thresholds *)
IF rMeltPres_Voted_Val >= rAlarm_MeltPres_HH_Trip THEN
    bTrip_MeltPres_HH := TRUE;
ELSIF rMeltPres_Voted_Val < (rAlarm_MeltPres_HH_Trip - rAlarm_MeltPres_Hyst) THEN
    bTrip_MeltPres_HH := FALSE;
END_IF;

IF rMeltPres_Voted_Val >= rAlarm_MeltPres_H_Warn THEN
    bWarn_MeltPres_H := TRUE;
ELSIF rMeltPres_Voted_Val < (rAlarm_MeltPres_H_Warn - rAlarm_MeltPres_Hyst) THEN
    bWarn_MeltPres_H := FALSE;
END_IF;

IF (iFSM_State = 5) AND (rMeltPres_Voted_Val <= rAlarm_MeltPres_L_Warn) THEN
    bWarn_MeltPres_L := TRUE;
ELSIF rMeltPres_Voted_Val > (rAlarm_MeltPres_L_Warn + rAlarm_MeltPres_Hyst) THEN
    bWarn_MeltPres_L := FALSE;
END_IF;

IF (iFSM_State = 5) AND (rFSM_StateTimer > 1.5) AND (rMeltPres_Voted_Val <= rAlarm_MeltPres_LL_Trip) THEN
    bTrip_MeltPres_LL := TRUE;
ELSIF rMeltPres_Voted_Val > (rAlarm_MeltPres_LL_Trip + rAlarm_MeltPres_Hyst) THEN
    bTrip_MeltPres_LL := FALSE;
END_IF;

(* Clamp Tonnage Alarm Thresholds *)
IF rTB_TotalClampForce >= rAlarm_Clamp_HH_Trip THEN
    bTrip_Clamp_HH := TRUE;
ELSIF rTB_TotalClampForce < (rAlarm_Clamp_HH_Trip - rAlarm_Clamp_Hyst) THEN
    bTrip_Clamp_HH := FALSE;
END_IF;

IF rTB_TotalClampForce >= rAlarm_Clamp_H_Warn THEN
    bWarn_Clamp_H := TRUE;
ELSIF rTB_TotalClampForce < (rAlarm_Clamp_H_Warn - rAlarm_Clamp_Hyst) THEN
    bWarn_Clamp_H := FALSE;
END_IF;

IF (iFSM_State >= 4) AND (iFSM_State <= 10) AND (rTB_TotalClampForce <= rAlarm_Clamp_L_Warn) THEN
    bWarn_Clamp_L := TRUE;
ELSIF rTB_TotalClampForce > (rAlarm_Clamp_L_Warn + rAlarm_Clamp_Hyst) THEN
    bWarn_Clamp_L := FALSE;
END_IF;

IF (iFSM_State >= 4) AND (iFSM_State <= 10) AND (rTB_TotalClampForce <= rAlarm_Clamp_LL_Trip) THEN
    bTrip_Clamp_LL := TRUE;
ELSIF rTB_TotalClampForce > (rAlarm_Clamp_LL_Trip + rAlarm_Clamp_Hyst) THEN
    bTrip_Clamp_LL := FALSE;
END_IF;

(* Tie-Bar Strain Tilt Parallelism Alarms *)
IF rPlaten_MaxDeviation >= rAlarm_TB_Tilt_HH_Trip THEN
    bTrip_TB_Tilt_HH := TRUE;
ELSIF rPlaten_MaxDeviation < (rAlarm_TB_Tilt_HH_Trip - rAlarm_TB_Tilt_Hyst) THEN
    bTrip_TB_Tilt_HH := FALSE;
END_IF;

IF rPlaten_MaxDeviation >= rAlarm_TB_Tilt_H_Warn THEN
    bWarn_TB_Tilt_H := TRUE;
ELSIF rPlaten_MaxDeviation < (rAlarm_TB_Tilt_H_Warn - rAlarm_TB_Tilt_Hyst) THEN
    bWarn_TB_Tilt_H := FALSE;
END_IF;

(* Barrel Temperature Zones 1-8 Peak Deviation Evaluation *)
rTemp_A := MAX(MAX(MAX(ABS(rPID_Err_Z1), ABS(rPID_Err_Z2)), MAX(ABS(rPID_Err_Z3), ABS(rPID_Err_Z4))),
               MAX(MAX(ABS(rPID_Err_Z5), ABS(rPID_Err_Z6)), MAX(ABS(rPID_Err_Z7), ABS(rPID_Err_Z8))));

IF rTemp_A >= rAlarm_Barrel_Dev_HH_Trip THEN
    bTrip_Barrel_Thermal_HH := TRUE;
ELSIF rTemp_A < (rAlarm_Barrel_Dev_HH_Trip - rAlarm_Barrel_Dev_Hyst) THEN
    bTrip_Barrel_Thermal_HH := FALSE;
END_IF;

IF rTemp_A >= rAlarm_Barrel_Dev_H_Warn THEN
    bWarn_Barrel_Thermal_H := TRUE;
ELSIF rTemp_A < (rAlarm_Barrel_Dev_H_Warn - rAlarm_Barrel_Dev_Hyst) THEN
    bWarn_Barrel_Thermal_H := FALSE;
END_IF;

(* Cold Screw Interlock Trip (Prevents screw rotation if barrel zones are below melting point) *)
IF (rBarrel_PV_Z2 < (rBarrel_SP_Z2 - rAlarm_Barrel_Dev_LL_Trip)) OR
   (rBarrel_PV_Z3 < (rBarrel_SP_Z3 - rAlarm_Barrel_Dev_LL_Trip)) OR
   (rBarrel_PV_Z4 < (rBarrel_SP_Z4 - rAlarm_Barrel_Dev_LL_Trip)) OR
   (rBarrel_PV_Z5 < (rBarrel_SP_Z5 - rAlarm_Barrel_Dev_LL_Trip)) THEN
    bTrip_Barrel_Thermal_LL := TRUE;
ELSE
    bTrip_Barrel_Thermal_LL := FALSE;
END_IF;

(* Emergency Stop Interlock *)
IF bCmd_EmergencyStop_In THEN
    bTrip_EmergencyStop_Active := TRUE;
ELSE
    bTrip_EmergencyStop_Active := FALSE;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * SUBSECTION 5.3: 32-BIT PACKED DIAGNOSTIC STATUS & ALARM WORDS
 * --------------------------------------------------------------------------------------------------------------------- *)
(* 1. Machine Operating Status Word (dwStatus_FSM) *)
dwStatus_FSM := INT_TO_DWORD(iFSM_State AND 16#000F); (* Bits 0-3: Operating State *)
IF bMachine_CycleActive_Out     THEN dwStatus_FSM := dwStatus_FSM OR 16#0000_0010; END_IF; (* Bit 4 *)
IF bVP_SwitchoverLatched        THEN dwStatus_FSM := dwStatus_FSM OR 16#0000_0020; END_IF; (* Bit 5 *)
IF bVP_TriggeredByCavity        THEN dwStatus_FSM := dwStatus_FSM OR 16#0000_0040; END_IF; (* Bit 6 *)
IF bVP_TriggeredByRate          THEN dwStatus_FSM := dwStatus_FSM OR 16#0000_0080; END_IF; (* Bit 7 *)
IF bVP_TriggeredByPosition      THEN dwStatus_FSM := dwStatus_FSM OR 16#0000_0100; END_IF; (* Bit 8 *)
IF bVP_TriggeredByMeltPres      THEN dwStatus_FSM := dwStatus_FSM OR 16#0000_0200; END_IF; (* Bit 9 *)
IF bRobot_PermissiveToEnter_Out THEN dwStatus_FSM := dwStatus_FSM OR 16#0000_0400; END_IF; (* Bit 10 *)
IF (rServo_EjectorStroke_Cmd_Out > 10.0) THEN dwStatus_FSM := dwStatus_FSM OR 16#0000_0800; END_IF; (* Bit 11 *)
IF bPneumatic_CorePull1_Fwd_Out THEN dwStatus_FSM := dwStatus_FSM OR 16#0000_1000; END_IF; (* Bit 12 *)
IF bPneumatic_AirEjectBlast_Out THEN dwStatus_FSM := dwStatus_FSM OR 16#0000_2000; END_IF; (* Bit 13 *)
IF (iFSM_State = 2)             THEN dwStatus_FSM := dwStatus_FSM OR 16#0000_4000; END_IF; (* Bit 14: LPMP Active *)
IF (rTB_TotalClampForce > 15000.0) THEN dwStatus_FSM := dwStatus_FSM OR 16#0000_8000; END_IF; (* Bit 15: Full Tonnage *)
IF bSafetyGate_FrontClosed_In   THEN dwStatus_FSM := dwStatus_FSM OR 16#0001_0000; END_IF; (* Bit 16 *)
IF bSafetyGate_RearClosed_In    THEN dwStatus_FSM := dwStatus_FSM OR 16#0002_0000; END_IF; (* Bit 17 *)
IF bRobot_PermissiveToClose_In  THEN dwStatus_FSM := dwStatus_FSM OR 16#0004_0000; END_IF; (* Bit 18 *)
IF bOptical_PartDropVerified_In THEN dwStatus_FSM := dwStatus_FSM OR 16#0008_0000; END_IF; (* Bit 19 *)
IF bPneumatics_AirPressureOK_In THEN dwStatus_FSM := dwStatus_FSM OR 16#0010_0000; END_IF; (* Bit 20 *)
IF bFSM_FirstScan               THEN dwStatus_FSM := dwStatus_FSM OR 16#0020_0000; END_IF; (* Bit 21 *)

(* 2. TMR Sensor Status Word (dwStatus_TMR) *)
dwStatus_TMR := 16#0000_0000;
dwStatus_TMR := dwStatus_TMR OR SHL(INT_TO_DWORD(iCavPres_TMR_HealthState AND 16#03), 0);
IF bCavPres_SensA_Fault         THEN dwStatus_TMR := dwStatus_TMR OR 16#0000_0004; END_IF;
IF bCavPres_SensB_Fault         THEN dwStatus_TMR := dwStatus_TMR OR 16#0000_0008; END_IF;
IF bCavPres_SensC_Fault         THEN dwStatus_TMR := dwStatus_TMR OR 16#0000_0010; END_IF;

dwStatus_TMR := dwStatus_TMR OR SHL(INT_TO_DWORD(iMeltPres_TMR_HealthState AND 16#03), 5);
IF bMeltPres_SensA_Fault        THEN dwStatus_TMR := dwStatus_TMR OR 16#0000_0080; END_IF;
IF bMeltPres_SensB_Fault        THEN dwStatus_TMR := dwStatus_TMR OR 16#0000_0100; END_IF;
IF bMeltPres_SensC_Fault        THEN dwStatus_TMR := dwStatus_TMR OR 16#0000_0200; END_IF;

dwStatus_TMR := dwStatus_TMR OR SHL(INT_TO_DWORD(iScrewPos_TMR_HealthState AND 16#03), 10);
IF bScrewPos_SensA_Fault        THEN dwStatus_TMR := dwStatus_TMR OR 16#0000_1000; END_IF;
IF bScrewPos_SensB_Fault        THEN dwStatus_TMR := dwStatus_TMR OR 16#0000_2000; END_IF;
IF bScrewPos_SensC_Fault        THEN dwStatus_TMR := dwStatus_TMR OR 16#0000_4000; END_IF;

dwStatus_TMR := dwStatus_TMR OR SHL(INT_TO_DWORD(iMeltTemp_TMR_HealthState AND 16#03), 15);
IF bMeltTemp_SensA_Fault        THEN dwStatus_TMR := dwStatus_TMR OR 16#0002_0000; END_IF;
IF bMeltTemp_SensB_Fault        THEN dwStatus_TMR := dwStatus_TMR OR 16#0004_0000; END_IF;
IF bMeltTemp_SensC_Fault        THEN dwStatus_TMR := dwStatus_TMR OR 16#0008_0000; END_IF;
IF bTrip_TMR_SensorCollapse     THEN dwStatus_TMR := dwStatus_TMR OR 16#0010_0000; END_IF;

(* 3. ISA-18.2 Critical Trips Word (dwTrip_Alarms) *)
dwTrip_Alarms := 16#0000_0000;
IF bTrip_EmergencyStop_Active   THEN dwTrip_Alarms := dwTrip_Alarms OR 16#0000_0001; END_IF;
IF bTrip_SafetyGate_Violation   THEN dwTrip_Alarms := dwTrip_Alarms OR 16#0000_0002; END_IF;
IF bTrip_TMR_SensorCollapse     THEN dwTrip_Alarms := dwTrip_Alarms OR 16#0000_0004; END_IF;
IF bTrip_CavPres_HH             THEN dwTrip_Alarms := dwTrip_Alarms OR 16#0000_0008; END_IF;
IF bTrip_CavPres_LL             THEN dwTrip_Alarms := dwTrip_Alarms OR 16#0000_0010; END_IF;
IF bTrip_CavPres_ROC            THEN dwTrip_Alarms := dwTrip_Alarms OR 16#0000_0020; END_IF;
IF bTrip_MeltPres_HH            THEN dwTrip_Alarms := dwTrip_Alarms OR 16#0000_0040; END_IF;
IF bTrip_MeltPres_LL            THEN dwTrip_Alarms := dwTrip_Alarms OR 16#0000_0080; END_IF;
IF bTrip_Clamp_HH               THEN dwTrip_Alarms := dwTrip_Alarms OR 16#0000_0100; END_IF;
IF bTrip_Clamp_LL               THEN dwTrip_Alarms := dwTrip_Alarms OR 16#0000_0200; END_IF;
IF bTrip_TB_Tilt_HH             THEN dwTrip_Alarms := dwTrip_Alarms OR 16#0000_0400; END_IF;
IF bAlarm_LPMP_ObstructionTrip  THEN dwTrip_Alarms := dwTrip_Alarms OR 16#0000_0800; END_IF;
IF bTrip_Barrel_Thermal_HH      THEN dwTrip_Alarms := dwTrip_Alarms OR 16#0000_1000; END_IF;
IF bTrip_Barrel_Thermal_LL      THEN dwTrip_Alarms := dwTrip_Alarms OR 16#0000_2000; END_IF;

(* 4. ISA-18.2 Process Warnings Word (dwWarn_Alarms) *)
dwWarn_Alarms := 16#0000_0000;
IF bWarn_CavPres_H              THEN dwWarn_Alarms := dwWarn_Alarms OR 16#0000_0001; END_IF;
IF bWarn_CavPres_L              THEN dwWarn_Alarms := dwWarn_Alarms OR 16#0000_0002; END_IF;
IF bWarn_MeltPres_H             THEN dwWarn_Alarms := dwWarn_Alarms OR 16#0000_0004; END_IF;
IF bWarn_MeltPres_L             THEN dwWarn_Alarms := dwWarn_Alarms OR 16#0000_0008; END_IF;
IF bWarn_Clamp_H                THEN dwWarn_Alarms := dwWarn_Alarms OR 16#0000_0010; END_IF;
IF bWarn_Clamp_L                THEN dwWarn_Alarms := dwWarn_Alarms OR 16#0000_0020; END_IF;
IF bWarn_TB_Tilt_H              THEN dwWarn_Alarms := dwWarn_Alarms OR 16#0000_0040; END_IF;
IF bWarn_Barrel_Thermal_H       THEN dwWarn_Alarms := dwWarn_Alarms OR 16#0000_0080; END_IF;
IF (rMoldWater_FlowRate_In < 45.0) THEN dwWarn_Alarms := dwWarn_Alarms OR 16#0000_0100; END_IF;
IF (rMoldWater_InletTemp_In > 32.0) THEN dwWarn_Alarms := dwWarn_Alarms OR 16#0000_0200; END_IF;

(* 5. MPC Optimization Diagnostic Word (dwDiag_MPC) *)
dwDiag_MPC := 16#0000_0000;
IF bMPC_Converged               THEN dwDiag_MPC := dwDiag_MPC OR 16#0000_0001; END_IF;
IF (u_Cmd[1] >= u_Max[1])       THEN dwDiag_MPC := dwDiag_MPC OR 16#0000_0002; END_IF;
IF (u_Cmd[2] >= u_Max[2])       THEN dwDiag_MPC := dwDiag_MPC OR 16#0000_0004; END_IF;
IF (u_Cmd[3] >= u_Max[3])       THEN dwDiag_MPC := dwDiag_MPC OR 16#0000_0008; END_IF;
IF (u_Cmd[4] >= u_Max[4])       THEN dwDiag_MPC := dwDiag_MPC OR 16#0000_0010; END_IF;
IF (u_Cmd[5] >= u_Max[5])       THEN dwDiag_MPC := dwDiag_MPC OR 16#0000_0020; END_IF;
dwDiag_MPC := dwDiag_MPC OR SHL(INT_TO_DWORD(iMPC_IterCounter AND 16#0F), 8);

(* ---------------------------------------------------------------------------------------------------------------------
 * SUBSECTION 5.4: OUTPUT ASSIGNMENTS & GLOBAL SAFETY LOCKOUT
 * --------------------------------------------------------------------------------------------------------------------- *)
dwStatusWord_Machine_Out := dwStatus_FSM;
dwStatusWord_TMR_Out     := dwStatus_TMR;
dwAlarmWord_Trip_Out     := dwTrip_Alarms;
dwAlarmWord_Warning_Out  := dwWarn_Alarms;
dwDiagnosticWord_MPC_Out := dwDiag_MPC;

(* Global Plant Lockout Determination *)
IF (dwTrip_Alarms <> 16#0000_0000) OR bCmd_EmergencyStop_In THEN
    bTrip_EmergencyLockout_Out := TRUE;
    rServo_InjVelocity_Cmd_Out := 0.0;
    rServo_HoldPressure_Cmd_Out := 0.0;
    rServo_ScrewRPM_Cmd_Out := 0.0;
    rServo_BackPressure_Cmd_Out := 0.0;
    rServo_ClampVelocity_Cmd_Out := 0.0;
    rServo_ClampTonnage_Cmd_Out := 0.0;
    rServo_EjectorStroke_Cmd_Out := 0.0;
    bPneumatic_AirEjectBlast_Out := FALSE;
    bRobot_PermissiveToEnter_Out := FALSE;
END_IF;

END_FUNCTION_BLOCK
