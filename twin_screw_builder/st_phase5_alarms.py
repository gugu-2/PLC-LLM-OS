(* =====================================================================================================================
 * PHASE 5: ISA-18.2 MULTI-TIER ALARM ENGINE & 32-BIT BIT-PACKED STATUS WORDS
 * Priority 1: Critical Emergency Trips (Unlatched only via Operator Reset when Safe)
 * Priority 2: Process Out-Of-Specification Warnings (Automatic Deadband Clearance)
 * Priority 3: Equipment Diagnostic & Sensor Redundancy Degradation Advisories
 * ===================================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------------------------
 * STEP 5.1: RATE-OF-CHANGE (ROC) DIFFERENTIATION FILTERS
 * --------------------------------------------------------------------------------------------------------------------- *)
IF T_SAMPLE > 0.001 THEN
    rROC_DieMeltPres := (rVoted_DieMeltPres_Out - rHist_DieMeltPres) / T_SAMPLE;
    rROC_MeltTemp    := (rVoted_MeltTemp_Out - rHist_MeltTemp) / T_SAMPLE;
    rROC_ScrewTorque := (rVoted_ScrewTorque_Out - rHist_ScrewTorque) / T_SAMPLE;
ELSE
    rROC_DieMeltPres := 0.0;
    rROC_MeltTemp    := 0.0;
    rROC_ScrewTorque := 0.0;
END_IF;

rHist_DieMeltPres := rVoted_DieMeltPres_Out;
rHist_MeltTemp    := rVoted_MeltTemp_Out;
rHist_ScrewTorque := rVoted_ScrewTorque_Out;

(* ---------------------------------------------------------------------------------------------------------------------
 * STEP 5.2: THRESHOLD EVALUATION WITH DEADBAND HYSTERESIS
 * --------------------------------------------------------------------------------------------------------------------- *)
(* 1. Die Melt Pressure PT-101 Alarms *)
IF rVoted_DieMeltPres_Out >= ALM_PT_HH THEN
    bAlm_PT_HH_Latched := TRUE;
ELSIF bAlarmReset_Cmd_In AND (rVoted_DieMeltPres_Out < (ALM_PT_HH - ALM_PT_DB)) THEN
    bAlm_PT_HH_Latched := FALSE;
END_IF;

IF rVoted_DieMeltPres_Out >= ALM_PT_H THEN
    bAlm_PT_H_Active := TRUE;
ELSIF rVoted_DieMeltPres_Out < (ALM_PT_H - ALM_PT_DB) THEN
    bAlm_PT_H_Active := FALSE;
END_IF;

IF (rVoted_DieMeltPres_Out <= ALM_PT_L) AND (uiCurrentState >= STATE_DIE_HEAD_BUILDUP) THEN
    bAlm_PT_L_Active := TRUE;
ELSIF rVoted_DieMeltPres_Out > (ALM_PT_L + ALM_PT_DB) THEN
    bAlm_PT_L_Active := FALSE;
END_IF;

IF (rVoted_DieMeltPres_Out <= ALM_PT_LL) AND (uiCurrentState >= STATE_GEAR_PUMP_SYNC) THEN
    bAlm_PT_LL_Latched := TRUE;
ELSIF bAlarmReset_Cmd_In AND (rVoted_DieMeltPres_Out > (ALM_PT_LL + ALM_PT_DB)) THEN
    bAlm_PT_LL_Latched := FALSE;
END_IF;

(* 2. Polymer Melt Temperature TT-201 Alarms *)
IF rVoted_MeltTemp_Out >= ALM_TT_HH THEN
    bAlm_TT_HH_Latched := TRUE;
ELSIF bAlarmReset_Cmd_In AND (rVoted_MeltTemp_Out < (ALM_TT_HH - ALM_TT_DB)) THEN
    bAlm_TT_HH_Latched := FALSE;
END_IF;

IF rVoted_MeltTemp_Out >= ALM_TT_H THEN
    bAlm_TT_H_Active := TRUE;
ELSIF rVoted_MeltTemp_Out < (ALM_TT_H - ALM_TT_DB) THEN
    bAlm_TT_H_Active := FALSE;
END_IF;

IF (rVoted_MeltTemp_Out <= ALM_TT_L) AND (uiCurrentState >= STATE_RAW_POLYMER_RAMP) THEN
    bAlm_TT_L_Active := TRUE;
ELSIF rVoted_MeltTemp_Out > (ALM_TT_L + ALM_TT_DB) THEN
    bAlm_TT_L_Active := FALSE;
END_IF;

IF (rVoted_MeltTemp_Out <= ALM_TT_LL) AND (uiCurrentState >= STATE_RAW_POLYMER_RAMP) THEN
    bAlm_TT_LL_Latched := TRUE;
ELSIF bAlarmReset_Cmd_In AND (rVoted_MeltTemp_Out > (ALM_TT_LL + ALM_TT_DB)) THEN
    bAlm_TT_LL_Latched := FALSE;
END_IF;

(* 3. Extruder Screw Drive Shaft Torque TT-301 Alarms *)
IF rVoted_ScrewTorque_Out >= ALM_TQ_HH THEN
    bAlm_TQ_HH_Latched := TRUE;
ELSIF bAlarmReset_Cmd_In AND (rVoted_ScrewTorque_Out < (ALM_TQ_HH - ALM_TQ_DB)) THEN
    bAlm_TQ_HH_Latched := FALSE;
END_IF;

IF rVoted_ScrewTorque_Out >= ALM_TQ_H THEN
    bAlm_TQ_H_Active := TRUE;
ELSIF rVoted_ScrewTorque_Out < (ALM_TQ_H - ALM_TQ_DB) THEN
    bAlm_TQ_H_Active := FALSE;
END_IF;

IF (rVoted_ScrewTorque_Out <= ALM_TQ_L) AND (uiCurrentState >= STATE_CONTINUOUS_COMPOUND) THEN
    bAlm_TQ_L_Active := TRUE;
ELSIF rVoted_ScrewTorque_Out > (ALM_TQ_L + ALM_TQ_DB) THEN
    bAlm_TQ_L_Active := FALSE;
END_IF;

(* 4. Melt Gear Pump Suction Flange Pressure PT-102 Alarms *)
IF rGearPump_SuctPres_In >= ALM_SUCT_HH THEN
    bAlm_SUCT_HH_Latched := TRUE;
ELSIF bAlarmReset_Cmd_In AND (rGearPump_SuctPres_In < (ALM_SUCT_HH - ALM_SUCT_DB)) THEN
    bAlm_SUCT_HH_Latched := FALSE;
END_IF;

IF rGearPump_SuctPres_In >= ALM_SUCT_H THEN
    bAlm_SUCT_H_Active := TRUE;
ELSIF rGearPump_SuctPres_In < (ALM_SUCT_H - ALM_SUCT_DB) THEN
    bAlm_SUCT_H_Active := FALSE;
END_IF;

IF (rGearPump_SuctPres_In <= ALM_SUCT_L) AND (uiCurrentState >= STATE_GEAR_PUMP_SYNC) THEN
    bAlm_SUCT_L_Active := TRUE;
ELSIF rGearPump_SuctPres_In > (ALM_SUCT_L + ALM_SUCT_DB) THEN
    bAlm_SUCT_L_Active := FALSE;
END_IF;

IF (rGearPump_SuctPres_In <= ALM_SUCT_LL) AND (uiCurrentState >= STATE_GEAR_PUMP_SYNC) THEN
    bAlm_SUCT_LL_Latched := TRUE;
ELSIF bAlarmReset_Cmd_In AND (rGearPump_SuctPres_In > (ALM_SUCT_LL + ALM_SUCT_DB)) THEN
    bAlm_SUCT_LL_Latched := FALSE;
END_IF;

(* 5. Underwater Pelletizer Supply Water Temperature TT-401 Alarms *)
IF rVoted_PelletWaterTemp_Out >= ALM_WT_HH THEN
    bAlm_WT_HH_Latched := TRUE;
ELSIF bAlarmReset_Cmd_In AND (rVoted_PelletWaterTemp_Out < (ALM_WT_HH - ALM_WT_DB)) THEN
    bAlm_WT_HH_Latched := FALSE;
END_IF;

IF rVoted_PelletWaterTemp_Out >= ALM_WT_H THEN
    bAlm_WT_H_Active := TRUE;
ELSIF rVoted_PelletWaterTemp_Out < (ALM_WT_H - ALM_WT_DB) THEN
    bAlm_WT_H_Active := FALSE;
END_IF;

IF (rVoted_PelletWaterTemp_Out <= ALM_WT_L) AND (uiCurrentState >= STATE_PELLETIZER_SPIN_CLOSE) THEN
    bAlm_WT_L_Active := TRUE;
ELSIF rVoted_PelletWaterTemp_Out > (ALM_WT_L + ALM_WT_DB) THEN
    bAlm_WT_L_Active := FALSE;
END_IF;

IF (rVoted_PelletWaterTemp_Out <= ALM_WT_LL) AND (uiCurrentState >= STATE_PELLETIZER_SPIN_CLOSE) THEN
    bAlm_WT_LL_Latched := TRUE;
ELSIF bAlarmReset_Cmd_In AND (rVoted_PelletWaterTemp_Out > (ALM_WT_LL + ALM_WT_DB)) THEN
    bAlm_WT_LL_Latched := FALSE;
END_IF;

(* 6. Vacuum Degassing Chamber Pressure Zone 9 Alarms *)
IF (rVacuumPres_FB_In >= ALM_VAC_HH) AND (uiCurrentState >= STATE_VACUUM_DEGASSING_PULL) THEN
    bAlm_VAC_HH_Latched := TRUE;
ELSIF bAlarmReset_Cmd_In AND (rVacuumPres_FB_In < (ALM_VAC_HH - ALM_VAC_DB)) THEN
    bAlm_VAC_HH_Latched := FALSE;
END_IF;

IF (rVacuumPres_FB_In >= ALM_VAC_H) AND (uiCurrentState >= STATE_VACUUM_DEGASSING_PULL) THEN
    bAlm_VAC_H_Active := TRUE;
ELSIF rVacuumPres_FB_In < (ALM_VAC_H - ALM_VAC_DB) THEN
    bAlm_VAC_H_Active := FALSE;
END_IF;

(* 7. Rupture Disc Hardware Burst Detection (Fail-Safe True = Intact) *)
IF NOT bRuptureDisc_Intact_In THEN
    bAlm_RuptureDisc_Latched := TRUE;
ELSIF bAlarmReset_Cmd_In AND bRuptureDisc_Intact_In THEN
    bAlm_RuptureDisc_Latched := FALSE;
END_IF;

(* 8. Gravimetric Feeder Ratio Deviation Check (> 8% Deviation during Production) *)
IF uiCurrentState = STATE_CONTINUOUS_COMPOUND THEN
    IF (ABS(rFeeder_ActFlow_01_In - rFeeder_CmdFlow_01_Out) > (0.08 * (rFeeder_CmdFlow_01_Out + 1.0))) OR
       (ABS(rFeeder_ActFlow_05_In - rFeeder_CmdFlow_05_Out) > (0.08 * (rFeeder_CmdFlow_05_Out + 1.0))) THEN
        bAlm_FeederRatioDev_Active := TRUE;
    ELSE
        bAlm_FeederRatioDev_Active := FALSE;
    END_IF;
ELSE
    bAlm_FeederRatioDev_Active := FALSE;
END_IF;

(* Master Safety Trip Interlock Evaluation *)
IF bAlm_PT_HH_Latched OR bAlm_TT_HH_Latched OR bAlm_TQ_HH_Latched OR
   bAlm_SUCT_HH_Latched OR bAlm_SUCT_LL_Latched OR bAlm_WT_HH_Latched OR
   bAlm_WT_LL_Latched OR bAlm_VAC_HH_Latched OR bAlm_RuptureDisc_Latched OR
   (NOT bSafetyLine_Healthy_In) THEN
    bTripInterlocked_Out := TRUE;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * STEP 5.3: ISA-18.2 32-BIT BIT-PACKED STATUS & ALARM WORD REGISTERS
 * --------------------------------------------------------------------------------------------------------------------- *)
(* Reset Temporary Bit-Packing Registers *)
dwStatus01 := 16#00000000;
dwStatus02 := 16#00000000;
dwStatus03 := 16#00000000;
dwAlarm01  := 16#00000000;
dwAlarm02  := 16#00000000;
dwAlarm03  := 16#00000000;

(* --- DWORD Alarm 01: Priority 1 Critical Protective Safety Trips --- *)
IF bAlm_PT_HH_Latched       THEN dwAlarm01 := dwAlarm01 OR 16#00000001; END_IF; (* Bit 0: Die Pressure HH *)
IF bAlm_TT_HH_Latched       THEN dwAlarm01 := dwAlarm01 OR 16#00000002; END_IF; (* Bit 1: Melt Temperature HH *)
IF bAlm_TQ_HH_Latched       THEN dwAlarm01 := dwAlarm01 OR 16#00000004; END_IF; (* Bit 2: Screw Torque Overload HH *)
IF bAlm_SUCT_HH_Latched     THEN dwAlarm01 := dwAlarm01 OR 16#00000008; END_IF; (* Bit 3: Pump Suction Pressure HH *)
IF bAlm_SUCT_LL_Latched     THEN dwAlarm01 := dwAlarm01 OR 16#00000010; END_IF; (* Bit 4: Pump Suction Cavitation LL *)
IF bAlm_WT_HH_Latched       THEN dwAlarm01 := dwAlarm01 OR 16#00000020; END_IF; (* Bit 5: Water Temperature Wrap HH *)
IF bAlm_WT_LL_Latched       THEN dwAlarm01 := dwAlarm01 OR 16#00000040; END_IF; (* Bit 6: Water Temperature Freeze LL *)
IF bAlm_VAC_HH_Latched      THEN dwAlarm01 := dwAlarm01 OR 16#00000080; END_IF; (* Bit 7: Vacuum Loss Vent Flooding HH *)
IF bAlm_RuptureDisc_Latched THEN dwAlarm01 := dwAlarm01 OR 16#00000100; END_IF; (* Bit 8: Rupture Disc Burst Sensor *)
IF NOT bSafetyLine_Healthy_In THEN dwAlarm01 := dwAlarm01 OR 16#00000200; END_IF; (* Bit 9: Master Safety Line E-Stop *)
IF bAlm_PT_LL_Latched       THEN dwAlarm01 := dwAlarm01 OR 16#00000400; END_IF; (* Bit 10: Die Melt Pressure LL *)
IF bAlm_TT_LL_Latched       THEN dwAlarm01 := dwAlarm01 OR 16#00000800; END_IF; (* Bit 11: Melt Cold Plug Freeze LL *)
dwExtruderAlarmWord_01_Out := dwAlarm01;

(* --- DWORD Alarm 02: Priority 2 Process Out-of-Tolerance Warnings --- *)
IF bAlm_PT_H_Active           THEN dwAlarm02 := dwAlarm02 OR 16#00000001; END_IF; (* Bit 0: Die Pressure High *)
IF bAlm_PT_L_Active           THEN dwAlarm02 := dwAlarm02 OR 16#00000002; END_IF; (* Bit 1: Die Pressure Low *)
IF bAlm_TT_H_Active           THEN dwAlarm02 := dwAlarm02 OR 16#00000004; END_IF; (* Bit 2: Melt Temperature High *)
IF bAlm_TT_L_Active           THEN dwAlarm02 := dwAlarm02 OR 16#00000008; END_IF; (* Bit 3: Melt Temperature Low *)
IF bAlm_TQ_H_Active           THEN dwAlarm02 := dwAlarm02 OR 16#00000010; END_IF; (* Bit 4: Screw Drive Torque High *)
IF bAlm_TQ_L_Active           THEN dwAlarm02 := dwAlarm02 OR 16#00000020; END_IF; (* Bit 5: Screw Starvation Torque Low *)
IF bAlm_SUCT_H_Active         THEN dwAlarm02 := dwAlarm02 OR 16#00000040; END_IF; (* Bit 6: Pump Suction Pressure High *)
IF bAlm_SUCT_L_Active         THEN dwAlarm02 := dwAlarm02 OR 16#00000080; END_IF; (* Bit 7: Pump Suction Cavitation Warn *)
IF bAlm_WT_H_Active           THEN dwAlarm02 := dwAlarm02 OR 16#00000100; END_IF; (* Bit 8: Pellet Water Temp High *)
IF bAlm_WT_L_Active           THEN dwAlarm02 := dwAlarm02 OR 16#00000200; END_IF; (* Bit 9: Pellet Water Temp Low *)
IF bAlm_VAC_H_Active          THEN dwAlarm02 := dwAlarm02 OR 16#00000400; END_IF; (* Bit 10: Degassing Vacuum Low Warn *)
IF bAlm_FeederRatioDev_Active THEN dwAlarm02 := dwAlarm02 OR 16#00000800; END_IF; (* Bit 11: Feeder Ratio Drift Warn *)
IF ABS(rROC_DieMeltPres) > 25.0 THEN dwAlarm02 := dwAlarm02 OR 16#00001000; END_IF; (* Bit 12: High dP/dt Surge *)
IF ABS(rROC_MeltTemp) > 4.0     THEN dwAlarm02 := dwAlarm02 OR 16#00002000; END_IF; (* Bit 13: High dT/dt Thermal Shock *)
IF ABS(rROC_ScrewTorque) > 500.0 THEN dwAlarm02 := dwAlarm02 OR 16#00004000; END_IF; (* Bit 14: High dTorque/dt Spike *)
dwExtruderAlarmWord_02_Out := dwAlarm02;

(* --- DWORD Alarm 03: Priority 3 Diagnostics & Sensor Redundancy Degradation --- *)
IF uiDegrade_DieMeltPres < 3  THEN dwAlarm03 := dwAlarm03 OR 16#00000001; END_IF; (* Bit 0: TMR Die Pres Degraded *)
IF uiDegrade_MeltTemp < 3     THEN dwAlarm03 := dwAlarm03 OR 16#00000002; END_IF; (* Bit 1: TMR Melt Temp Degraded *)
IF uiDegrade_ScrewTorque < 3  THEN dwAlarm03 := dwAlarm03 OR 16#00000004; END_IF; (* Bit 2: TMR Torque Degraded *)
IF uiDegrade_WaterTemp < 3    THEN dwAlarm03 := dwAlarm03 OR 16#00000008; END_IF; (* Bit 3: TMR Water Temp Degraded *)
IF uiDegrade_DieMeltPres = 0  THEN dwAlarm03 := dwAlarm03 OR 16#00000010; END_IF; (* Bit 4: TMR Die Pres Total Fail *)
IF uiDegrade_MeltTemp = 0     THEN dwAlarm03 := dwAlarm03 OR 16#00000020; END_IF; (* Bit 5: TMR Melt Temp Total Fail *)
IF uiDegrade_ScrewTorque = 0  THEN dwAlarm03 := dwAlarm03 OR 16#00000040; END_IF; (* Bit 6: TMR Torque Total Fail *)
IF uiDegrade_WaterTemp = 0    THEN dwAlarm03 := dwAlarm03 OR 16#00000080; END_IF; (* Bit 7: TMR Water Temp Total Fail *)
(* Barrel Zone 1..12 Tracking Error Diagnostics (Bit 8 to Bit 19) *)
FOR idx_z := 1 TO 12 DO
    IF ABS(rPID_Zone_Err[idx_z]) > 10.0 THEN
        dwAlarm03 := dwAlarm03 OR SHL(16#00000100, (idx_z - 1));
    END_IF;
END_FOR;
dwExtruderAlarmWord_03_Out := dwAlarm03;

(* --- DWORD Status 01: Operating Modes & FSM Execution Tracking --- *)
dwStatus01 := dwStatus01 OR (UINT_TO_DWORD(uiCurrentState) AND 16#0000000F);
dwStatus01 := dwStatus01 OR SHL((UINT_TO_DWORD(uiCurrentSubState) AND 16#0000000F), 4);
IF bExtruderReady_Out      THEN dwStatus01 := dwStatus01 OR 16#00000100; END_IF; (* Bit 8: Ready for Production *)
IF bTripInterlocked_Out    THEN dwStatus01 := dwStatus01 OR 16#00000200; END_IF; (* Bit 9: Safety Trip Interlocked *)
IF bPurgeSequenceActive    THEN dwStatus01 := dwStatus01 OR 16#00000400; END_IF; (* Bit 10: Purge Transition Mode *)
IF bAutoMode_Cmd_In        THEN dwStatus01 := dwStatus01 OR 16#00000800; END_IF; (* Bit 11: Auto Production Mode *)
IF tSoakHoldTimer >= 1800.0 THEN dwStatus01 := dwStatus01 OR 16#00001000; END_IF; (* Bit 12: Core Soak Complete *)
IF bDieFastDump_Valve_Out  THEN dwStatus01 := dwStatus01 OR 16#00002000; END_IF; (* Bit 13: Fast Dump Open *)
dwExtruderStatusWord_01_Out := dwStatus01;

(* --- DWORD Status 02: Drive & Subsystem Operational State --- *)
IF rScrewSpeed_Act_In > 1.0        THEN dwStatus02 := dwStatus02 OR 16#00000001; END_IF; (* Bit 0: Extruder Drive Run *)
IF rGearPumpSpeed_Act_In > 0.5     THEN dwStatus02 := dwStatus02 OR 16#00000002; END_IF; (* Bit 1: Gear Pump Servo Run *)
IF rSideFeederSpeed_Cmd_Out > 1.0  THEN dwStatus02 := dwStatus02 OR 16#00000004; END_IF; (* Bit 2: Glass Side Feeder Run *)
IF rPelletCutter_Speed_FB_In > 50.0 THEN dwStatus02 := dwStatus02 OR 16#00000008; END_IF; (* Bit 3: Pelletizer Cutter Run *)
IF bWaterCircPump_Run_Out          THEN dwStatus02 := dwStatus02 OR 16#00000010; END_IF; (* Bit 4: Water Pump Run *)
IF bWaterBox_Clamp_Out             THEN dwStatus02 := dwStatus02 OR 16#00000020; END_IF; (* Bit 5: Water Box Clamped *)
IF bWaterBox_Diverter_Out          THEN dwStatus02 := dwStatus02 OR 16#00000040; END_IF; (* Bit 6: Water Flow In Box *)
IF bVacuumPump_Run_Out             THEN dwStatus02 := dwStatus02 OR 16#00000080; END_IF; (* Bit 7: Vacuum Skid Run *)
IF rFeeder_ActFlow_01_In > 10.0    THEN dwStatus02 := dwStatus02 OR 16#00000100; END_IF; (* Bit 8: Feeder 1 Infeed *)
IF rFeeder_ActFlow_02_In > 1.0     THEN dwStatus02 := dwStatus02 OR 16#00000200; END_IF; (* Bit 9: Feeder 2 Infeed *)
IF rFeeder_ActFlow_03_In > 1.0     THEN dwStatus02 := dwStatus02 OR 16#00000400; END_IF; (* Bit 10: Feeder 3 Infeed *)
IF rFeeder_ActFlow_04_In > 0.2     THEN dwStatus02 := dwStatus02 OR 16#00000800; END_IF; (* Bit 11: Feeder 4 Infeed *)
IF rFeeder_ActFlow_05_In > 10.0    THEN dwStatus02 := dwStatus02 OR 16#00001000; END_IF; (* Bit 12: Glass Feeder Infeed *)
dwExtruderStatusWord_02_Out := dwStatus02;

(* --- DWORD Status 03: TMR Sensor Channel Physical Integrity --- *)
IF bHealth_DMP_A THEN dwStatus03 := dwStatus03 OR 16#00000001; END_IF; (* Bit 0: DMP Ch A Healthy *)
IF bHealth_DMP_B THEN dwStatus03 := dwStatus03 OR 16#00000002; END_IF; (* Bit 1: DMP Ch B Healthy *)
IF bHealth_DMP_C THEN dwStatus03 := dwStatus03 OR 16#00000004; END_IF; (* Bit 2: DMP Ch C Healthy *)
IF bHealth_MT_A  THEN dwStatus03 := dwStatus03 OR 16#00000008; END_IF; (* Bit 3: MT Ch A Healthy *)
IF bHealth_MT_B  THEN dwStatus03 := dwStatus03 OR 16#00000010; END_IF; (* Bit 4: MT Ch B Healthy *)
IF bHealth_MT_C  THEN dwStatus03 := dwStatus03 OR 16#00000020; END_IF; (* Bit 5: MT Ch C Healthy *)
IF bHealth_ST_A  THEN dwStatus03 := dwStatus03 OR 16#00000040; END_IF; (* Bit 6: ST Ch A Healthy *)
IF bHealth_ST_B  THEN dwStatus03 := dwStatus03 OR 16#00000080; END_IF; (* Bit 7: ST Ch B Healthy *)
IF bHealth_ST_C  THEN dwStatus03 := dwStatus03 OR 16#00000100; END_IF; (* Bit 8: ST Ch C Healthy *)
IF bHealth_WT_A  THEN dwStatus03 := dwStatus03 OR 16#00000200; END_IF; (* Bit 9: WT Ch A Healthy *)
IF bHealth_WT_B  THEN dwStatus03 := dwStatus03 OR 16#00000400; END_IF; (* Bit 10: WT Ch B Healthy *)
IF bHealth_WT_C  THEN dwStatus03 := dwStatus03 OR 16#00000800; END_IF; (* Bit 11: WT Ch C Healthy *)
IF bRuptureDisc_Intact_In    THEN dwStatus03 := dwStatus03 OR 16#00001000; END_IF; (* Bit 12: Rupture Disc Normal *)
IF bSafetyLine_Healthy_In    THEN dwStatus03 := dwStatus03 OR 16#00002000; END_IF; (* Bit 13: Safety Relay Closed *)
IF bMasterEnable_In          THEN dwStatus03 := dwStatus03 OR 16#00004000; END_IF; (* Bit 14: Master Enable High *)
dwExtruderStatusWord_03_Out := dwStatus03;

END_FUNCTION_BLOCK
