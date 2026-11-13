# ldpe_reactor_builder/st_phase5_alarms.py

def get_phase5_alarms():
    return """(* ============================================================================================== *)
(* PHASE 5: ISA-18.2 MULTI-TIER PROCESS ALARM MATRIX, SUB-5 MS DECOMP ENGINE & BIT-PACKING       *)
(* 32-BIT TELEMETRY REGISTERS (ALARMWORD 1..3, STATUSWORD 1..2) & END_FUNCTION_BLOCK              *)
(* ============================================================================================== *)

(* ---------------------------------------------------------------------------------------------- *)
(* STEP 5.1: SUB-5 MS EXPLOSIVE DECOMPOSITION FAST DETECTION ENGINE                               *)
(* Ethylene spontaneous dissociation: C2H4 -> C + CH4 + H2 release explosive thermal wave         *)
(* Requires immediate hydraulic snort venting within 20 to 30 ms to prevent vessel rupture       *)
(* ---------------------------------------------------------------------------------------------- *)
IF (rFast_dP_dt_bar_s >= rThreshold_Decomp_dP_dt_bar_s) OR
   (rFast_dT_dt_K_s >= rThreshold_Decomp_dT_dt_K_s) OR
   (rVoted_AcousticEmission_dB >= rThreshold_Decomp_Acoustic_dB) OR
   (rVoted_ReactorPressure_bar >= rThreshold_Decomp_AbsPress_bar) OR
   (rVoted_PeakTemperature_degC >= rThreshold_Decomp_AbsTemp_degC) THEN

    bDecomp_TripQualified := TRUE;
    bDecompDetected       := TRUE;
    bLatched_RatePress_HH := TRUE;
    bLatched_RateTemp_HH  := TRUE;
    bLatched_Acoustic_HH  := TRUE;
END_IF;


(* ---------------------------------------------------------------------------------------------- *)
(* STEP 5.2: ISA-18.2 MULTI-TIER ALARM ENGINE (HH, H, L, LL) WITH HYSTERESIS DEADBANDS           *)
(* ---------------------------------------------------------------------------------------------- *)

(* --- REACTOR PRESSURE ALARM TIER --- *)
(* High-High Trip (3,280 bar) *)
IF rVoted_ReactorPressure_bar >= rAlarm_Press_HH_bar THEN
    tAlarm_Press_HH_Timer_s := tAlarm_Press_HH_Timer_s + tScanCycleTime_s;
    IF tAlarm_Press_HH_Timer_s >= 0.050 THEN (* 50 ms qualification *)
        bLatched_Press_HH := TRUE;
    END_IF;
ELSIF rVoted_ReactorPressure_bar <= (rAlarm_Press_HH_bar - rAlarm_Press_Deadband_bar) THEN
    tAlarm_Press_HH_Timer_s := 0.0;
    IF bResetAlarms THEN
        bLatched_Press_HH := FALSE;
    END_IF;
END_IF;

(* High Warning (3,150 bar) *)
IF rVoted_ReactorPressure_bar >= rAlarm_Press_H_bar THEN
    tAlarm_Press_H_Timer_s := tAlarm_Press_H_Timer_s + tScanCycleTime_s;
    IF tAlarm_Press_H_Timer_s >= 0.200 THEN
        bLatched_Press_H := TRUE;
    END_IF;
ELSIF rVoted_ReactorPressure_bar <= (rAlarm_Press_H_bar - rAlarm_Press_Deadband_bar) THEN
    tAlarm_Press_H_Timer_s := 0.0;
    IF bResetAlarms THEN
        bLatched_Press_H := FALSE;
    END_IF;
END_IF;

(* Low Warning (2,750 bar) *)
IF (rVoted_ReactorPressure_bar <= rAlarm_Press_L_bar) AND (iState >= STATE_NOMINAL_EXOTHERMIC_RUN) THEN
    tAlarm_Press_L_Timer_s := tAlarm_Press_L_Timer_s + tScanCycleTime_s;
    IF tAlarm_Press_L_Timer_s >= 0.500 THEN
        bLatched_Press_L := TRUE;
    END_IF;
ELSIF rVoted_ReactorPressure_bar >= (rAlarm_Press_L_bar + rAlarm_Press_Deadband_bar) THEN
    tAlarm_Press_L_Timer_s := 0.0;
    IF bResetAlarms THEN
        bLatched_Press_L := FALSE;
    END_IF;
END_IF;

(* Low-Low Trip (2,450 bar) *)
IF (rVoted_ReactorPressure_bar <= rAlarm_Press_LL_bar) AND (iState >= STATE_NOMINAL_EXOTHERMIC_RUN) THEN
    tAlarm_Press_LL_Timer_s := tAlarm_Press_LL_Timer_s + tScanCycleTime_s;
    IF tAlarm_Press_LL_Timer_s >= 0.300 THEN
        bLatched_Press_LL := TRUE;
    END_IF;
ELSIF rVoted_ReactorPressure_bar >= (rAlarm_Press_LL_bar + rAlarm_Press_Deadband_bar) THEN
    tAlarm_Press_LL_Timer_s := 0.0;
    IF bResetAlarms THEN
        bLatched_Press_LL := FALSE;
    END_IF;
END_IF;


(* --- PEAK EXOTHERM TEMPERATURE ALARM TIER --- *)
(* High-High Trip (316 deg C) *)
IF rVoted_PeakTemperature_degC >= rAlarm_Temp_HH_degC THEN
    tAlarm_Temp_HH_Timer_s := tAlarm_Temp_HH_Timer_s + tScanCycleTime_s;
    IF tAlarm_Temp_HH_Timer_s >= 0.040 THEN (* 40 ms fast qualification *)
        bLatched_Temp_HH := TRUE;
    END_IF;
ELSIF rVoted_PeakTemperature_degC <= (rAlarm_Temp_HH_degC - rAlarm_Temp_Deadband_degC) THEN
    tAlarm_Temp_HH_Timer_s := 0.0;
    IF bResetAlarms THEN
        bLatched_Temp_HH := FALSE;
    END_IF;
END_IF;

(* High Warning (308 deg C) *)
IF rVoted_PeakTemperature_degC >= rAlarm_Temp_H_degC THEN
    tAlarm_Temp_H_Timer_s := tAlarm_Temp_H_Timer_s + tScanCycleTime_s;
    IF tAlarm_Temp_H_Timer_s >= 0.150 THEN
        bLatched_Temp_H := TRUE;
    END_IF;
ELSIF rVoted_PeakTemperature_degC <= (rAlarm_Temp_H_degC - rAlarm_Temp_Deadband_degC) THEN
    tAlarm_Temp_H_Timer_s := 0.0;
    IF bResetAlarms THEN
        bLatched_Temp_H := FALSE;
    END_IF;
END_IF;

(* Low Warning (220 deg C) during production *)
IF (rVoted_PeakTemperature_degC <= rAlarm_Temp_L_degC) AND (iState >= STATE_NOMINAL_EXOTHERMIC_RUN) THEN
    tAlarm_Temp_L_Timer_s := tAlarm_Temp_L_Timer_s + tScanCycleTime_s;
    IF tAlarm_Temp_L_Timer_s >= 1.0 THEN
        bLatched_Temp_L := TRUE;
    END_IF;
ELSIF rVoted_PeakTemperature_degC >= (rAlarm_Temp_L_degC + rAlarm_Temp_Deadband_degC) THEN
    tAlarm_Temp_L_Timer_s := 0.0;
    IF bResetAlarms THEN
        bLatched_Temp_L := FALSE;
    END_IF;
END_IF;

(* Low-Low Flameout Trip (170 deg C) *)
IF (rVoted_PeakTemperature_degC <= rAlarm_Temp_LL_degC) AND (iState >= STATE_NOMINAL_EXOTHERMIC_RUN) THEN
    tAlarm_Temp_LL_Timer_s := tAlarm_Temp_LL_Timer_s + tScanCycleTime_s;
    IF tAlarm_Temp_LL_Timer_s >= 0.800 THEN
        bLatched_Temp_LL := TRUE;
    END_IF;
ELSIF rVoted_PeakTemperature_degC >= (rAlarm_Temp_LL_degC + rAlarm_Temp_Deadband_degC) THEN
    tAlarm_Temp_LL_Timer_s := 0.0;
    IF bResetAlarms THEN
        bLatched_Temp_LL := FALSE;
    END_IF;
END_IF;


(* --- PEROXIDE DOSING FLOW ALARMS --- *)
IF rVoted_PeroxideFlow_kgh >= rAlarm_Flow_H_kgh THEN
    bLatched_Flow_H := TRUE;
ELSIF rVoted_PeroxideFlow_kgh <= (rAlarm_Flow_H_kgh - rAlarm_Flow_Deadband_kgh) THEN
    IF bResetAlarms THEN
        bLatched_Flow_H := FALSE;
    END_IF;
END_IF;

IF (rVoted_PeroxideFlow_kgh <= rAlarm_Flow_L_kgh) AND (iState >= STATE_NOMINAL_EXOTHERMIC_RUN) THEN
    bLatched_Flow_L := TRUE;
ELSIF rVoted_PeroxideFlow_kgh >= (rAlarm_Flow_L_kgh + rAlarm_Flow_Deadband_kgh) THEN
    IF bResetAlarms THEN
        bLatched_Flow_L := FALSE;
    END_IF;
END_IF;


(* --- ACOUSTIC EMISSION STRESS ALARMS --- *)
IF rVoted_AcousticEmission_dB >= rAlarm_Acoustic_HH_dB THEN
    bLatched_Acoustic_HH := TRUE;
ELSIF rVoted_AcousticEmission_dB < 95.0 THEN
    IF bResetAlarms THEN
        bLatched_Acoustic_HH := FALSE;
    END_IF;
END_IF;

IF rVoted_AcousticEmission_dB >= rAlarm_Acoustic_H_dB THEN
    bLatched_Acoustic_H := TRUE;
ELSIF rVoted_AcousticEmission_dB < 75.0 THEN
    IF bResetAlarms THEN
        bLatched_Acoustic_H := FALSE;
    END_IF;
END_IF;


(* ---------------------------------------------------------------------------------------------- *)
(* STEP 5.3: BIT-PACKED 32-BIT TELEMETRY REGISTERS                                                *)
(* ---------------------------------------------------------------------------------------------- *)

(* === ALARM WORD 1: DECOMPOSITION & EXTREME PRESSURE ALARMS === *)
dwAlarmWord1_Decomposition := 16#00000000;
IF bDecomp_TripQualified       THEN dwAlarmWord1_Decomposition := dwAlarmWord1_Decomposition OR 16#00000001; END_IF;
IF bLatched_RatePress_HH       THEN dwAlarmWord1_Decomposition := dwAlarmWord1_Decomposition OR 16#00000002; END_IF;
IF bLatched_RateTemp_HH        THEN dwAlarmWord1_Decomposition := dwAlarmWord1_Decomposition OR 16#00000004; END_IF;
IF bLatched_Acoustic_HH        THEN dwAlarmWord1_Decomposition := dwAlarmWord1_Decomposition OR 16#00000008; END_IF;
IF (rVoted_ReactorPressure_bar >= rThreshold_Decomp_AbsPress_bar) THEN dwAlarmWord1_Decomposition := dwAlarmWord1_Decomposition OR 16#00000010; END_IF;
IF (rVoted_PeakTemperature_degC >= rThreshold_Decomp_AbsTemp_degC) THEN dwAlarmWord1_Decomposition := dwAlarmWord1_Decomposition OR 16#00000020; END_IF;
IF bLatched_Press_HH           THEN dwAlarmWord1_Decomposition := dwAlarmWord1_Decomposition OR 16#00000040; END_IF;
IF bLatched_Press_H            THEN dwAlarmWord1_Decomposition := dwAlarmWord1_Decomposition OR 16#00000080; END_IF;
IF bLatched_Press_L            THEN dwAlarmWord1_Decomposition := dwAlarmWord1_Decomposition OR 16#00000100; END_IF;
IF bLatched_Press_LL           THEN dwAlarmWord1_Decomposition := dwAlarmWord1_Decomposition OR 16#00000200; END_IF;
IF bLatched_Temp_HH            THEN dwAlarmWord1_Decomposition := dwAlarmWord1_Decomposition OR 16#00000400; END_IF;
IF bLatched_Temp_H             THEN dwAlarmWord1_Decomposition := dwAlarmWord1_Decomposition OR 16#00000800; END_IF;
IF bLatched_Temp_L             THEN dwAlarmWord1_Decomposition := dwAlarmWord1_Decomposition OR 16#00001000; END_IF;
IF bLatched_Temp_LL            THEN dwAlarmWord1_Decomposition := dwAlarmWord1_Decomposition OR 16#00002000; END_IF;
IF bLatched_Flow_H             THEN dwAlarmWord1_Decomposition := dwAlarmWord1_Decomposition OR 16#00004000; END_IF;
IF bLatched_Flow_L             THEN dwAlarmWord1_Decomposition := dwAlarmWord1_Decomposition OR 16#00008000; END_IF;
IF bLatched_Acoustic_H         THEN dwAlarmWord1_Decomposition := dwAlarmWord1_Decomposition OR 16#00010000; END_IF;
IF (rCurrent_FoulingResistance_m2K_kW > 0.85) THEN dwAlarmWord1_Decomposition := dwAlarmWord1_Decomposition OR 16#00020000; END_IF;
IF (rCurrent_WallGelThickness_um > 500.0)    THEN dwAlarmWord1_Decomposition := dwAlarmWord1_Decomposition OR 16#00040000; END_IF;
IF (rHyperComp_PlungerMotorPower_kW > 21000.0) THEN dwAlarmWord1_Decomposition := dwAlarmWord1_Decomposition OR 16#00080000; END_IF;
IF (rHyperComp_SealOilDiffPress_bar < 90.0)   THEN dwAlarmWord1_Decomposition := dwAlarmWord1_Decomposition OR 16#00100000; END_IF;
IF (bHPLDV_InPulseExecution AND (rEst_HPLDV_PulseAmplitude_bar < 180.0)) THEN dwAlarmWord1_Decomposition := dwAlarmWord1_Decomposition OR 16#00200000; END_IF;
IF (rJacketWater_ReturnTemp_degC > 235.0)     THEN dwAlarmWord1_Decomposition := dwAlarmWord1_Decomposition OR 16#00400000; END_IF;
IF (rJacketWater_CirculationFlow_m3h < 450.0) THEN dwAlarmWord1_Decomposition := dwAlarmWord1_Decomposition OR 16#00800000; END_IF;
IF (rSeparatorPress_HPS_bar > 285.0)          THEN dwAlarmWord1_Decomposition := dwAlarmWord1_Decomposition OR 16#01000000; END_IF;


(* === ALARM WORD 2: PROCESS EXCURSIONS & KINETIC IMBALANCES === *)
dwAlarmWord2_ProcessExcursions := 16#00000000;
IF (vecX_Est[iState_Xconv] < 20.0) AND (iState = STATE_NOMINAL_EXOTHERMIC_RUN) THEN dwAlarmWord2_ProcessExcursions := dwAlarmWord2_ProcessExcursions OR 16#00000001; END_IF;
IF (vecX_Est[iState_Xconv] > 38.0) THEN dwAlarmWord2_ProcessExcursions := dwAlarmWord2_ProcessExcursions OR 16#00000002; END_IF;
IF (vecX_Est[iState_Zpeak] > 1200.0) THEN dwAlarmWord2_ProcessExcursions := dwAlarmWord2_ProcessExcursions OR 16#00000004; END_IF;
IF (vecX_Est[iState_Zpeak] < 400.0)  THEN dwAlarmWord2_ProcessExcursions := dwAlarmWord2_ProcessExcursions OR 16#00000008; END_IF;
IF (vecX_Est[iState_MFI] < 0.50)     THEN dwAlarmWord2_ProcessExcursions := dwAlarmWord2_ProcessExcursions OR 16#00000010; END_IF;
IF (vecX_Est[iState_MFI] > 15.0)     THEN dwAlarmWord2_ProcessExcursions := dwAlarmWord2_ProcessExcursions OR 16#00000020; END_IF;
IF (rTemp_Zone1_Reaction_degC > 305.0) THEN dwAlarmWord2_ProcessExcursions := dwAlarmWord2_ProcessExcursions OR 16#00000040; END_IF;
IF (rTemp_Zone2_Reaction_degC > 310.0) THEN dwAlarmWord2_ProcessExcursions := dwAlarmWord2_ProcessExcursions OR 16#00000080; END_IF;
IF (rTemp_Zone3_Reaction_degC > 305.0) THEN dwAlarmWord2_ProcessExcursions := dwAlarmWord2_ProcessExcursions OR 16#00000100; END_IF;
IF (rTemp_Zone4_Reaction_degC > 295.0) THEN dwAlarmWord2_ProcessExcursions := dwAlarmWord2_ProcessExcursions OR 16#00000200; END_IF;
IF (rTemp_DischargeOutlet_degC > 275.0) THEN dwAlarmWord2_ProcessExcursions := dwAlarmWord2_ProcessExcursions OR 16#00000400; END_IF;
IF (rRecycleGasFlowRate_tph < 50.0)  THEN dwAlarmWord2_ProcessExcursions := dwAlarmWord2_ProcessExcursions OR 16#00000800; END_IF;
IF (rHyperComp_SuctionPress_bar < 210.0) THEN dwAlarmWord2_ProcessExcursions := dwAlarmWord2_ProcessExcursions OR 16#00001000; END_IF;
IF (rHyperComp_SuctionPress_bar > 275.0) THEN dwAlarmWord2_ProcessExcursions := dwAlarmWord2_ProcessExcursions OR 16#00002000; END_IF;


(* === ALARM WORD 3: 2oo3 TMR TRANSDUCER DIAGNOSTICS & DISCREPANCIES === *)
dwAlarmWord3_SensorDiagnostics := 16#00000000;
IF bFault_Press_Ch1     THEN dwAlarmWord3_SensorDiagnostics := dwAlarmWord3_SensorDiagnostics OR 16#00000001; END_IF;
IF bFault_Press_Ch2     THEN dwAlarmWord3_SensorDiagnostics := dwAlarmWord3_SensorDiagnostics OR 16#00000002; END_IF;
IF bFault_Press_Ch3     THEN dwAlarmWord3_SensorDiagnostics := dwAlarmWord3_SensorDiagnostics OR 16#00000004; END_IF;
IF bFault_Temp_Ch1      THEN dwAlarmWord3_SensorDiagnostics := dwAlarmWord3_SensorDiagnostics OR 16#00000008; END_IF;
IF bFault_Temp_Ch2      THEN dwAlarmWord3_SensorDiagnostics := dwAlarmWord3_SensorDiagnostics OR 16#00000010; END_IF;
IF bFault_Temp_Ch3      THEN dwAlarmWord3_SensorDiagnostics := dwAlarmWord3_SensorDiagnostics OR 16#00000020; END_IF;
IF bFault_Flow_Ch1      THEN dwAlarmWord3_SensorDiagnostics := dwAlarmWord3_SensorDiagnostics OR 16#00000040; END_IF;
IF bFault_Flow_Ch2      THEN dwAlarmWord3_SensorDiagnostics := dwAlarmWord3_SensorDiagnostics OR 16#00000080; END_IF;
IF bFault_Flow_Ch3      THEN dwAlarmWord3_SensorDiagnostics := dwAlarmWord3_SensorDiagnostics OR 16#00000100; END_IF;
IF bFault_Acoustic_Ch1  THEN dwAlarmWord3_SensorDiagnostics := dwAlarmWord3_SensorDiagnostics OR 16#00000200; END_IF;
IF bFault_Acoustic_Ch2  THEN dwAlarmWord3_SensorDiagnostics := dwAlarmWord3_SensorDiagnostics OR 16#00000400; END_IF;
IF bFault_Acoustic_Ch3  THEN dwAlarmWord3_SensorDiagnostics := dwAlarmWord3_SensorDiagnostics OR 16#00000800; END_IF;
IF (rTMR_Health_Overall_pct < 65.0) THEN dwAlarmWord3_SensorDiagnostics := dwAlarmWord3_SensorDiagnostics OR 16#00001000; END_IF;
IF bTMR_DiscrepancyAlarm THEN dwAlarmWord3_SensorDiagnostics := dwAlarmWord3_SensorDiagnostics OR 16#00002000; END_IF;


(* === STATUS WORD 1: 14-STAGE FSM STATE & OPERATIONAL PERMISSIVES === *)
dwStatusWord1_FSM_Permissives := 16#00000000;
(* Bit-encode Active State Number (0..13) into Bits 0..13 *)
IF iState = 0  THEN dwStatusWord1_FSM_Permissives := dwStatusWord1_FSM_Permissives OR 16#00000001; END_IF;
IF iState = 1  THEN dwStatusWord1_FSM_Permissives := dwStatusWord1_FSM_Permissives OR 16#00000002; END_IF;
IF iState = 2  THEN dwStatusWord1_FSM_Permissives := dwStatusWord1_FSM_Permissives OR 16#00000004; END_IF;
IF iState = 3  THEN dwStatusWord1_FSM_Permissives := dwStatusWord1_FSM_Permissives OR 16#00000008; END_IF;
IF iState = 4  THEN dwStatusWord1_FSM_Permissives := dwStatusWord1_FSM_Permissives OR 16#00000010; END_IF;
IF iState = 5  THEN dwStatusWord1_FSM_Permissives := dwStatusWord1_FSM_Permissives OR 16#00000020; END_IF;
IF iState = 6  THEN dwStatusWord1_FSM_Permissives := dwStatusWord1_FSM_Permissives OR 16#00000040; END_IF;
IF iState = 7  THEN dwStatusWord1_FSM_Permissives := dwStatusWord1_FSM_Permissives OR 16#00000080; END_IF;
IF iState = 8  THEN dwStatusWord1_FSM_Permissives := dwStatusWord1_FSM_Permissives OR 16#00000100; END_IF;
IF iState = 9  THEN dwStatusWord1_FSM_Permissives := dwStatusWord1_FSM_Permissives OR 16#00000200; END_IF;
IF iState = 10 THEN dwStatusWord1_FSM_Permissives := dwStatusWord1_FSM_Permissives OR 16#00000400; END_IF;
IF iState = 11 THEN dwStatusWord1_FSM_Permissives := dwStatusWord1_FSM_Permissives OR 16#00000800; END_IF;
IF iState = 12 THEN dwStatusWord1_FSM_Permissives := dwStatusWord1_FSM_Permissives OR 16#00001000; END_IF;
IF iState = 13 THEN dwStatusWord1_FSM_Permissives := dwStatusWord1_FSM_Permissives OR 16#00002000; END_IF;

IF bEnable       THEN dwStatusWord1_FSM_Permissives := dwStatusWord1_FSM_Permissives OR 16#00010000; END_IF;
IF bAutoMode     THEN dwStatusWord1_FSM_Permissives := dwStatusWord1_FSM_Permissives OR 16#00020000; END_IF;
IF bStartProduction THEN dwStatusWord1_FSM_Permissives := dwStatusWord1_FSM_Permissives OR 16#00040000; END_IF;
IF bControlledTurndown THEN dwStatusWord1_FSM_Permissives := dwStatusWord1_FSM_Permissives OR 16#00080000; END_IF;
IF (rTMR_Health_Overall_pct >= 85.0) THEN dwStatusWord1_FSM_Permissives := dwStatusWord1_FSM_Permissives OR 16#00100000; END_IF;


(* === STATUS WORD 2: ACTUATOR SUBSYSTEMS & INTERLOCK ENGAGEMENTS === *)
dwStatusWord2_Subsystems_Interlocks := 16#00000000;
IF bCmd_SnortValve_EmergencyDump   THEN dwStatusWord2_Subsystems_Interlocks := dwStatusWord2_Subsystems_Interlocks OR 16#00000001; END_IF;
IF bCmd_HyperComp_EmergencyTrip    THEN dwStatusWord2_Subsystems_Interlocks := dwStatusWord2_Subsystems_Interlocks OR 16#00000002; END_IF;
IF bCmd_Peroxide_EmergencyBlockBleed THEN dwStatusWord2_Subsystems_Interlocks := dwStatusWord2_Subsystems_Interlocks OR 16#00000004; END_IF;
IF bCmd_JacketWater_ColdDelugeTrip THEN dwStatusWord2_Subsystems_Interlocks := dwStatusWord2_Subsystems_Interlocks OR 16#00000008; END_IF;
IF bCmd_HPLDV_PulseActive          THEN dwStatusWord2_Subsystems_Interlocks := dwStatusWord2_Subsystems_Interlocks OR 16#00000010; END_IF;
IF bHPLDV_InPulseExecution         THEN dwStatusWord2_Subsystems_Interlocks := dwStatusWord2_Subsystems_Interlocks OR 16#00000020; END_IF;
IF (rCmd_PeroxidePump1_Stroke_pct > 1.0) THEN dwStatusWord2_Subsystems_Interlocks := dwStatusWord2_Subsystems_Interlocks OR 16#00000040; END_IF;
IF (rCmd_PeroxidePump2_Stroke_pct > 1.0) THEN dwStatusWord2_Subsystems_Interlocks := dwStatusWord2_Subsystems_Interlocks OR 16#00000080; END_IF;
IF (rCmd_PeroxidePump3_Stroke_pct > 1.0) THEN dwStatusWord2_Subsystems_Interlocks := dwStatusWord2_Subsystems_Interlocks OR 16#00000100; END_IF;
IF (rCmd_PeroxidePump4_Stroke_pct > 1.0) THEN dwStatusWord2_Subsystems_Interlocks := dwStatusWord2_Subsystems_Interlocks OR 16#00000200; END_IF;
IF bMatricesInitialized            THEN dwStatusWord2_Subsystems_Interlocks := dwStatusWord2_Subsystems_Interlocks OR 16#00000400; END_IF;

END_FUNCTION_BLOCK
"""
