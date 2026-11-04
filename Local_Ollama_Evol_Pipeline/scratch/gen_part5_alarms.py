# gen_part5_alarms.py
def get_part5_alarms():
    return """
(* ==================================================================================================================== *)
(* PHASE 5: ISA-18.2 MULTI-TIERED ALARM MANAGEMENT, DEAD-BAND HYSTERESIS & DIAGNOSTIC WORD PACKING                    *)
(* Prioritized alarm hierarchy:                                                                                         *)
(*   Priority 1 (Critical): Catastrophic mechanical over-stress, chamber breach, safety e-stop.                         *)
(*   Priority 2 (Warning): Quality out-of-tolerance, micro-leak rate-of-change, defective container diversion.          *)
(*   Priority 3 (Advisory): Process drift, sensor channel degradation, predictive maintenance wear warnings.            *)
(* Packed 16-bit status registers for deterministic SCADA / MES telemetry integration.                                  *)
(* ==================================================================================================================== *)

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 5.1: RATE-OF-CHANGE (ROC) DIFFERENTIATOR FOR PRESSURE LEAK DETECTION & FORCE SPIKES                                  *)
(* -------------------------------------------------------------------------------------------------------------------- *)
IF rCycleScanDeltaTime > 0.0 THEN
    rRateOfChange_Pressure_bar_per_s := (rVoted_AcousticPressure_bar - rPrevPressureSample_bar) / rCycleScanDeltaTime;
    rRateOfChange_Force1stOp_N_per_s := (rVoted_Force1stOp_N - rPrevForce1stOpSample_N) / rCycleScanDeltaTime;
    rPrevPressureSample_bar := rVoted_AcousticPressure_bar;
    rPrevForce1stOpSample_N := rVoted_Force1stOp_N;
END_IF;

(* Sudden pressure drop indicative of instant can puncture / wall blow-out *)
IF rRateOfChange_Pressure_bar_per_s < -15.0 THEN
    bAlarm_PressureLeakRateOfChange := TRUE;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 5.2: ANALOG LIMIT COMPARATORS WITH DEADBAND HYSTERESIS                                                               *)
(* -------------------------------------------------------------------------------------------------------------------- *)
(* 1st Operation Roll Force Hysteresis Logic *)
IF rVoted_Force1stOp_N >= rLim_1stOpForce_HH_N THEN
    bAlarm_Force1stOp_HH := TRUE;
ELSIF rVoted_Force1stOp_N <= (rLim_1stOpForce_HH_N - rDeadband_Force_N) THEN
    bAlarm_Force1stOp_HH := FALSE;
END_IF;

IF rVoted_Force1stOp_N >= rLim_1stOpForce_H_N THEN
    bAlarm_Force1stOp_H := TRUE;
ELSIF rVoted_Force1stOp_N <= (rLim_1stOpForce_H_N - rDeadband_Force_N) THEN
    bAlarm_Force1stOp_H := FALSE;
END_IF;

IF rVoted_Force1stOp_N <= rLim_1stOpForce_L_N THEN
    bAlarm_Force1stOp_L := TRUE;
ELSIF rVoted_Force1stOp_N >= (rLim_1stOpForce_L_N + rDeadband_Force_N) THEN
    bAlarm_Force1stOp_L := FALSE;
END_IF;

IF rVoted_Force1stOp_N <= rLim_1stOpForce_LL_N THEN
    bAlarm_Force1stOp_LL := TRUE;
ELSIF rVoted_Force1stOp_N >= (rLim_1stOpForce_LL_N + rDeadband_Force_N) THEN
    bAlarm_Force1stOp_LL := FALSE;
END_IF;

(* 2nd Operation Roll Crimp Force Hysteresis Logic *)
IF rVoted_Force2ndOp_N >= rLim_2ndOpForce_HH_N THEN
    bAlarm_Force2ndOp_HH := TRUE;
ELSIF rVoted_Force2ndOp_N <= (rLim_2ndOpForce_HH_N - rDeadband_Force_N) THEN
    bAlarm_Force2ndOp_HH := FALSE;
END_IF;

IF rVoted_Force2ndOp_N >= rLim_2ndOpForce_H_N THEN
    bAlarm_Force2ndOp_H := TRUE;
ELSIF rVoted_Force2ndOp_N <= (rLim_2ndOpForce_H_N - rDeadband_Force_N) THEN
    bAlarm_Force2ndOp_H := FALSE;
END_IF;

IF rVoted_Force2ndOp_N <= rLim_2ndOpForce_L_N THEN
    bAlarm_Force2ndOp_L := TRUE;
ELSIF rVoted_Force2ndOp_N >= (rLim_2ndOpForce_L_N + rDeadband_Force_N) THEN
    bAlarm_Force2ndOp_L := FALSE;
END_IF;

IF rVoted_Force2ndOp_N <= rLim_2ndOpForce_LL_N THEN
    bAlarm_Force2ndOp_LL := TRUE;
ELSIF rVoted_Force2ndOp_N >= (rLim_2ndOpForce_LL_N + rDeadband_Force_N) THEN
    bAlarm_Force2ndOp_LL := FALSE;
END_IF;

(* Can Internal Pressure Hysteresis Logic *)
IF rVoted_AcousticPressure_bar >= rLim_InternalPres_HH_bar THEN
    bAlarm_InternalPres_HH := TRUE;
ELSIF rVoted_AcousticPressure_bar <= (rLim_InternalPres_HH_bar - rDeadband_Pressure_bar) THEN
    bAlarm_InternalPres_HH := FALSE;
END_IF;

IF rVoted_AcousticPressure_bar >= rLim_InternalPres_H_bar THEN
    bAlarm_InternalPres_H := TRUE;
ELSIF rVoted_AcousticPressure_bar <= (rLim_InternalPres_H_bar - rDeadband_Pressure_bar) THEN
    bAlarm_InternalPres_H := FALSE;
END_IF;

IF rVoted_AcousticPressure_bar <= rLim_InternalPres_L_bar THEN
    bAlarm_InternalPres_L := TRUE;
ELSIF rVoted_AcousticPressure_bar >= (rLim_InternalPres_L_bar + rDeadband_Pressure_bar) THEN
    bAlarm_InternalPres_L := FALSE;
END_IF;

IF rVoted_AcousticPressure_bar <= rLim_InternalPres_LL_bar THEN
    bAlarm_InternalPres_LL := TRUE;
ELSIF rVoted_AcousticPressure_bar >= (rLim_InternalPres_LL_bar + rDeadband_Pressure_bar) THEN
    bAlarm_InternalPres_LL := FALSE;
END_IF;

(* Acoustic Resonance Frequency Hysteresis Logic *)
IF rVoted_AcousticResonanceFreq_Hz >= rLim_AcousticResonance_HH_Hz THEN
    bAlarm_AcousticResonance_HH := TRUE;
ELSIF rVoted_AcousticResonanceFreq_Hz <= (rLim_AcousticResonance_HH_Hz - rDeadband_Acoustic_Hz) THEN
    bAlarm_AcousticResonance_HH := FALSE;
END_IF;

IF rVoted_AcousticResonanceFreq_Hz <= rLim_AcousticResonance_LL_Hz THEN
    bAlarm_AcousticResonance_LL := TRUE;
ELSIF rVoted_AcousticResonanceFreq_Hz >= (rLim_AcousticResonance_LL_Hz + rDeadband_Acoustic_Hz) THEN
    bAlarm_AcousticResonance_LL := FALSE;
END_IF;

(* Aseptic Isolator PAA Concentration Hysteresis Logic *)
IF rVoted_PAAConcentration_ppm >= rLim_PAAConc_HH_ppm THEN
    bAlarm_PAAConc_HH := TRUE;
ELSIF rVoted_PAAConcentration_ppm <= (rLim_PAAConc_HH_ppm - rDeadband_PAA_ppm) THEN
    bAlarm_PAAConc_HH := FALSE;
END_IF;

IF rVoted_PAAConcentration_ppm <= rLim_PAAConc_LL_ppm THEN
    bAlarm_PAAConc_LL := TRUE;
ELSIF rVoted_PAAConcentration_ppm >= (rLim_PAAConc_LL_ppm + rDeadband_PAA_ppm) THEN
    bAlarm_PAAConc_LL := FALSE;
END_IF;

(* Sterile Air Overpressure Hysteresis Logic *)
IF rVoted_SterileAirPres_Pa >= rLim_SterileAir_HH_Pa THEN
    bAlarm_SterileAir_HH := TRUE;
ELSIF rVoted_SterileAirPres_Pa <= (rLim_SterileAir_HH_Pa - rDeadband_SterileAir_Pa) THEN
    bAlarm_SterileAir_HH := FALSE;
END_IF;

IF rVoted_SterileAirPres_Pa <= rLim_SterileAir_LL_Pa THEN
    bAlarm_SterileAir_LL := TRUE;
ELSIF rVoted_SterileAirPres_Pa >= (rLim_SterileAir_LL_Pa + rDeadband_SterileAir_Pa) THEN
    bAlarm_SterileAir_LL := FALSE;
END_IF;

(* Chuck Bearing Temperature Hysteresis Logic *)
IF rVoted_ChuckBearingTemp_C >= rLim_ChuckBearingTemp_HH_C THEN
    bAlarm_ChuckBearingTemp_HH := TRUE;
ELSIF rVoted_ChuckBearingTemp_C <= (rLim_ChuckBearingTemp_HH_C - rDeadband_BearingTemp_C) THEN
    bAlarm_ChuckBearingTemp_HH := FALSE;
END_IF;

IF rVoted_ChuckBearingTemp_C >= rLim_ChuckBearingTemp_H_C THEN
    bAlarm_ChuckBearingTemp_H := TRUE;
ELSIF rVoted_ChuckBearingTemp_C <= (rLim_ChuckBearingTemp_H_C - rDeadband_BearingTemp_C) THEN
    bAlarm_ChuckBearingTemp_H := FALSE;
END_IF;

(* Master Fault Reset Command *)
IF bResetFaultLatches THEN
    bAlarm_Force1stOp_HH := FALSE;
    bAlarm_Force1stOp_H := FALSE;
    bAlarm_Force1stOp_L := FALSE;
    bAlarm_Force1stOp_LL := FALSE;
    bAlarm_Force2ndOp_HH := FALSE;
    bAlarm_Force2ndOp_H := FALSE;
    bAlarm_Force2ndOp_L := FALSE;
    bAlarm_Force2ndOp_LL := FALSE;
    bAlarm_InternalPres_HH := FALSE;
    bAlarm_InternalPres_H := FALSE;
    bAlarm_InternalPres_L := FALSE;
    bAlarm_InternalPres_LL := FALSE;
    bAlarm_AcousticResonance_HH := FALSE;
    bAlarm_AcousticResonance_H := FALSE;
    bAlarm_AcousticResonance_L := FALSE;
    bAlarm_AcousticResonance_LL := FALSE;
    bAlarm_PressureLeakRateOfChange := FALSE;
    bAlarm_PAAConc_HH := FALSE;
    bAlarm_PAAConc_H := FALSE;
    bAlarm_PAAConc_L := FALSE;
    bAlarm_PAAConc_LL := FALSE;
    bAlarm_SterileAir_HH := FALSE;
    bAlarm_SterileAir_H := FALSE;
    bAlarm_SterileAir_L := FALSE;
    bAlarm_SterileAir_LL := FALSE;
    bAlarm_ChuckBearingTemp_HH := FALSE;
    bAlarm_ChuckBearingTemp_H := FALSE;
    bAlarm_SeamOverlapDeficiency := FALSE;
    bAlarm_CanJamInfeedLifter := FALSE;
    bAlarm_EStopDepressurized := FALSE;
    bDiscrepAlarm_Force1stOp := FALSE;
    bDiscrepAlarm_Force2ndOp := FALSE;
    bDiscrepAlarm_TurretResolver := FALSE;
    bDiscrepAlarm_LN2DoseMass := FALSE;
    bDiscrepAlarm_AcousticResonance := FALSE;
    bDiscrepAlarm_PAAConcentration := FALSE;
    bDiscrepAlarm_SterileAirPres := FALSE;
    bDiscrepAlarm_ChuckBearingTemp := FALSE;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 5.3: PACK ISA-18.2 PRIORITY 1 CRITICAL SHUTDOWN ALARMS (wAlarmWord_ISA18_Critical)                                   *)
(* -------------------------------------------------------------------------------------------------------------------- *)
wAlarmWord_ISA18_Critical := 16#0000;
IF bAlarm_Force1stOp_HH         THEN wAlarmWord_ISA18_Critical := wAlarmWord_ISA18_Critical OR 16#0001; END_IF;
IF bAlarm_Force2ndOp_HH         THEN wAlarmWord_ISA18_Critical := wAlarmWord_ISA18_Critical OR 16#0002; END_IF;
IF bAlarm_InternalPres_HH       THEN wAlarmWord_ISA18_Critical := wAlarmWord_ISA18_Critical OR 16#0004; END_IF;
IF bAlarm_InternalPres_LL       THEN wAlarmWord_ISA18_Critical := wAlarmWord_ISA18_Critical OR 16#0008; END_IF;
IF bAlarm_PAAConc_LL            THEN wAlarmWord_ISA18_Critical := wAlarmWord_ISA18_Critical OR 16#0010; END_IF;
IF bAlarm_SterileAir_LL         THEN wAlarmWord_ISA18_Critical := wAlarmWord_ISA18_Critical OR 16#0020; END_IF;
IF bAlarm_ChuckBearingTemp_HH   THEN wAlarmWord_ISA18_Critical := wAlarmWord_ISA18_Critical OR 16#0040; END_IF;
IF bAlarm_EStopDepressurized     THEN wAlarmWord_ISA18_Critical := wAlarmWord_ISA18_Critical OR 16#0080; END_IF;
IF bDiscrepAlarm_TurretResolver THEN wAlarmWord_ISA18_Critical := wAlarmWord_ISA18_Critical OR 16#0100; END_IF;
IF bAlarm_CanJamInfeedLifter    THEN wAlarmWord_ISA18_Critical := wAlarmWord_ISA18_Critical OR 16#0200; END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 5.4: PACK ISA-18.2 PRIORITY 2 PROCESS WARNINGS & REJECTIONS (wAlarmWord_ISA18_Warning)                              *)
(* -------------------------------------------------------------------------------------------------------------------- *)
wAlarmWord_ISA18_Warning := 16#0000;
IF bAlarm_Force1stOp_H          THEN wAlarmWord_ISA18_Warning := wAlarmWord_ISA18_Warning OR 16#0001; END_IF;
IF bAlarm_Force1stOp_L          THEN wAlarmWord_ISA18_Warning := wAlarmWord_ISA18_Warning OR 16#0002; END_IF;
IF bAlarm_Force2ndOp_H          THEN wAlarmWord_ISA18_Warning := wAlarmWord_ISA18_Warning OR 16#0004; END_IF;
IF bAlarm_Force2ndOp_L          THEN wAlarmWord_ISA18_Warning := wAlarmWord_ISA18_Warning OR 16#0008; END_IF;
IF bAlarm_InternalPres_H        THEN wAlarmWord_ISA18_Warning := wAlarmWord_ISA18_Warning OR 16#0010; END_IF;
IF bAlarm_InternalPres_L        THEN wAlarmWord_ISA18_Warning := wAlarmWord_ISA18_Warning OR 16#0020; END_IF;
IF bAlarm_AcousticResonance_H   THEN wAlarmWord_ISA18_Warning := wAlarmWord_ISA18_Warning OR 16#0040; END_IF;
IF bAlarm_AcousticResonance_L   THEN wAlarmWord_ISA18_Warning := wAlarmWord_ISA18_Warning OR 16#0080; END_IF;
IF bAlarm_PressureLeakRateOfChange THEN wAlarmWord_ISA18_Warning := wAlarmWord_ISA18_Warning OR 16#0100; END_IF;
IF bAlarm_SeamOverlapDeficiency THEN wAlarmWord_ISA18_Warning := wAlarmWord_ISA18_Warning OR 16#0200; END_IF;
IF bAlarm_ChuckBearingTemp_H    THEN wAlarmWord_ISA18_Warning := wAlarmWord_ISA18_Warning OR 16#0400; END_IF;
IF bAlarm_SterileAir_H          THEN wAlarmWord_ISA18_Warning := wAlarmWord_ISA18_Warning OR 16#0800; END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 5.5: PACK 2oo3 TMR SENSOR CHANNEL HEALTH STATUS WORD (wSensorHealthStatusWord)                                       *)
(* -------------------------------------------------------------------------------------------------------------------- *)
wSensorHealthStatusWord := 16#0000;
IF bTMR_Force1st_Fault_A     THEN wSensorHealthStatusWord := wSensorHealthStatusWord OR 16#0001; END_IF;
IF bTMR_Force1st_Fault_B     THEN wSensorHealthStatusWord := wSensorHealthStatusWord OR 16#0002; END_IF;
IF bTMR_Force1st_Fault_C     THEN wSensorHealthStatusWord := wSensorHealthStatusWord OR 16#0004; END_IF;
IF bTMR_Force2nd_Fault_A     THEN wSensorHealthStatusWord := wSensorHealthStatusWord OR 16#0008; END_IF;
IF bTMR_Force2nd_Fault_B     THEN wSensorHealthStatusWord := wSensorHealthStatusWord OR 16#0010; END_IF;
IF bTMR_Force2nd_Fault_C     THEN wSensorHealthStatusWord := wSensorHealthStatusWord OR 16#0020; END_IF;
IF bTMR_Resolver_Fault_A     THEN wSensorHealthStatusWord := wSensorHealthStatusWord OR 16#0040; END_IF;
IF bTMR_Resolver_Fault_B     THEN wSensorHealthStatusWord := wSensorHealthStatusWord OR 16#0080; END_IF;
IF bTMR_Resolver_Fault_C     THEN wSensorHealthStatusWord := wSensorHealthStatusWord OR 16#0100; END_IF;
IF bTMR_LN2Mass_Fault_A      THEN wSensorHealthStatusWord := wSensorHealthStatusWord OR 16#0200; END_IF;
IF bTMR_LN2Mass_Fault_B      THEN wSensorHealthStatusWord := wSensorHealthStatusWord OR 16#0400; END_IF;
IF bTMR_LN2Mass_Fault_C      THEN wSensorHealthStatusWord := wSensorHealthStatusWord OR 16#0800; END_IF;
IF bTMR_Acoustic_Fault_A     THEN wSensorHealthStatusWord := wSensorHealthStatusWord OR 16#1000; END_IF;
IF bTMR_PAA_Fault_A          THEN wSensorHealthStatusWord := wSensorHealthStatusWord OR 16#2000; END_IF;
IF bTMR_SterileAir_Fault_A   THEN wSensorHealthStatusWord := wSensorHealthStatusWord OR 16#4000; END_IF;
IF bTMR_BearingTemp_Fault_A  THEN wSensorHealthStatusWord := wSensorHealthStatusWord OR 16#8000; END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 5.6: PACK MACHINE AUTOMATION STATUS WORD (wAutomationStatusWord)                                                    *)
(* -------------------------------------------------------------------------------------------------------------------- *)
wAutomationStatusWord := 16#0000;
IF eState = 10  THEN wAutomationStatusWord := wAutomationStatusWord OR 16#0001; END_IF; (* Sterilization CIP/SIP *)
IF eState = 20  THEN wAutomationStatusWord := wAutomationStatusWord OR 16#0002; END_IF; (* Pressure Barrier Lock *)
IF eState = 30  THEN wAutomationStatusWord := wAutomationStatusWord OR 16#0004; END_IF; (* Infeed Pacing *)
IF eState = 40  THEN wAutomationStatusWord := wAutomationStatusWord OR 16#0008; END_IF; (* Lifter Engage *)
IF eState = 50  THEN wAutomationStatusWord := wAutomationStatusWord OR 16#0010; END_IF; (* LN2 Micro-Dose *)
IF eState = 60  THEN wAutomationStatusWord := wAutomationStatusWord OR 16#0020; END_IF; (* 1st Op Curl *)
IF eState = 70  THEN wAutomationStatusWord := wAutomationStatusWord OR 16#0040; END_IF; (* 2nd Op Crimp *)
IF eState = 80  THEN wAutomationStatusWord := wAutomationStatusWord OR 16#0080; END_IF; (* Acoustic Leak Test *)
IF eState = 90  THEN wAutomationStatusWord := wAutomationStatusWord OR 16#0100; END_IF; (* Divert Reject *)
IF eState = 100 THEN wAutomationStatusWord := wAutomationStatusWord OR 16#0200; END_IF; (* Discharge Sync *)
IF eState = 110 THEN wAutomationStatusWord := wAutomationStatusWord OR 16#0400; END_IF; (* Controlled Jam Stop *)
IF eState = 120 THEN wAutomationStatusWord := wAutomationStatusWord OR 16#0800; END_IF; (* Emergency Depressurize *)
IF bAsepticBarrierIntegrityOK THEN wAutomationStatusWord := wAutomationStatusWord OR 16#1000; END_IF;
IF bMachineSynchronized       THEN wAutomationStatusWord := wAutomationStatusWord OR 16#2000; END_IF;
IF bMasterLineRunPermissive   THEN wAutomationStatusWord := wAutomationStatusWord OR 16#4000; END_IF;
IF bEmergencyStopCircuit_NC   THEN wAutomationStatusWord := wAutomationStatusWord OR 16#8000; END_IF;

END_FUNCTION_BLOCK
"""
