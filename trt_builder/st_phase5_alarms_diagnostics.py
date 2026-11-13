# trt_builder/st_phase5_alarms_diagnostics.py
"""
Phase 5: ISA-18.2 Multi-Tier Alarms, SIL-3 Emergency Trips & Bit-Packed Telemetry
for FB_Steel_BlastFurnace_TopGas_TRT_PowerRecovery
"""

def get_phase5_alarms_diagnostics():
    return """(* ==================================================================================================== *)
(* PHASE 5: ISA-18.2 MULTI-TIER ALARMS, SIL-3 EMERGENCY TRIPS & BIT-PACKED TELEMETRY                   *)
(* ==================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------- *)
(* 5.1 PROCESS VARIABLE ALARM MONITORING WITH DEADBAND HYSTERESIS                                        *)
(* ---------------------------------------------------------------------------------------------------- *)

(* Top Gas Pressure PT-101 Alarms & Trips *)
IF rVoted_TopGasPressure >= cTopGasPress_TripHH THEN
    bAlarm_TopPress_HH := TRUE;
ELSIF rVoted_TopGasPressure <= (cTopGasPress_TripHH - cTopGasPress_Hysteresis) THEN
    bAlarm_TopPress_HH := FALSE;
END_IF;

IF rVoted_TopGasPressure >= cTopGasPress_AlarmH THEN
    bAlarm_TopPress_H := TRUE;
ELSIF rVoted_TopGasPressure <= (cTopGasPress_AlarmH - cTopGasPress_Hysteresis) THEN
    bAlarm_TopPress_H := FALSE;
END_IF;

IF rVoted_TopGasPressure <= cTopGasPress_AlarmL THEN
    bAlarm_TopPress_L := TRUE;
ELSIF rVoted_TopGasPressure >= (cTopGasPress_AlarmL + cTopGasPress_Hysteresis) THEN
    bAlarm_TopPress_L := FALSE;
END_IF;

IF rVoted_TopGasPressure <= cTopGasPress_TripLL THEN
    bAlarm_TopPress_LL := TRUE;
ELSIF rVoted_TopGasPressure >= (cTopGasPress_TripLL + cTopGasPress_Hysteresis) THEN
    bAlarm_TopPress_LL := FALSE;
END_IF;

(* Blast Furnace Slip Rapid Pressure Surge Rate-of-Change Alarm *)
IF rTopGasPressure_ROC >= cTopGasPress_SlipROC_Threshold THEN
    bAlarm_TopPress_SlipROC := TRUE;
ELSIF rTopGasPressure_ROC <= (cTopGasPress_SlipROC_Threshold - 8.0) THEN
    bAlarm_TopPress_SlipROC := FALSE;
END_IF;

(* Turbine Rotor Speed Alarms & Overspeed Trip (SIL-3) *)
IF rTurbineSpeed_Filtered >= cTurbineOverspeed_TripHH THEN
    bAlarm_TurbineSpeed_HH := TRUE;
ELSIF rTurbineSpeed_Filtered <= (cTurbineOverspeed_TripHH - cTurbineOverspeed_Hysteresis) THEN
    bAlarm_TurbineSpeed_HH := FALSE;
END_IF;

IF rTurbineSpeed_Filtered >= cTurbineOverspeed_AlarmH THEN
    bAlarm_TurbineSpeed_H := TRUE;
ELSIF rTurbineSpeed_Filtered <= (cTurbineOverspeed_AlarmH - cTurbineOverspeed_Hysteresis) THEN
    bAlarm_TurbineSpeed_H := FALSE;
END_IF;

(* Turbine Bearing Radial Vibration Alarms & Trip (ISO 10816 Zone D) *)
IF rVoted_TurbineVibration >= cTurbineVib_TripHH THEN
    bAlarm_TurbineVib_HH := TRUE;
ELSIF rVoted_TurbineVibration <= (cTurbineVib_TripHH - cTurbineVib_Hysteresis) THEN
    bAlarm_TurbineVib_HH := FALSE;
END_IF;

IF rVoted_TurbineVibration >= cTurbineVib_AlarmH THEN
    bAlarm_TurbineVib_H := TRUE;
ELSIF rVoted_TurbineVibration <= (cTurbineVib_AlarmH - cTurbineVib_Hysteresis) THEN
    bAlarm_TurbineVib_H := FALSE;
END_IF;

(* Dry Bag Filter Array Differential Pressure Alarms & Trips *)
IF rVoted_BagFilterDiffPress >= cBagFilter_dPTripHH THEN
    bAlarm_BagFilter_dPHH := TRUE;
ELSIF rVoted_BagFilterDiffPress <= (cBagFilter_dPTripHH - cBagFilter_dPHysteresis) THEN
    bAlarm_BagFilter_dPHH := FALSE;
END_IF;

IF rVoted_BagFilterDiffPress >= cBagFilter_dPAlarmH THEN
    bAlarm_BagFilter_dPH := TRUE;
ELSIF rVoted_BagFilterDiffPress <= (cBagFilter_dPAlarmH - cBagFilter_dPHysteresis) THEN
    bAlarm_BagFilter_dPH := FALSE;
END_IF;

IF rVoted_BagFilterDiffPress <= cBagFilter_dPTripLL THEN
    bAlarm_BagFilter_dPLL := TRUE;
ELSIF rVoted_BagFilterDiffPress >= (cBagFilter_dPTripLL + cBagFilter_dPHysteresis) THEN
    bAlarm_BagFilter_dPLL := FALSE;
END_IF;

(* Bag Filter Inlet Gas Temperature Alarms & Trips *)
IF rTopGasInletTemp_TT102 >= cBagFilterTemp_TripHH THEN
    bAlarm_BagFilter_TempHH := TRUE;
ELSIF rTopGasInletTemp_TT102 <= (cBagFilterTemp_TripHH - 5.0) THEN
    bAlarm_BagFilter_TempHH := FALSE;
END_IF;

IF rTopGasInletTemp_TT102 <= cBagFilterTemp_TripLL THEN
    bAlarm_BagFilter_TempLL := TRUE;
ELSIF rTopGasInletTemp_TT102 >= (cBagFilterTemp_TripLL + 5.0) THEN
    bAlarm_BagFilter_TempLL := FALSE;
END_IF;

(* Turbine and Generator Bearing Metal Temperatures *)
IF (rTurbineBearingTemp_TT502A >= cBearingTemp_TripHH)
   OR (rTurbineBearingTemp_TT502B >= cBearingTemp_TripHH)
   OR (rTurbineThrustBearingTemp_TT503 >= cBearingTemp_TripHH)
   OR (rGeneratorBearingTemp_TT402 >= cBearingTemp_TripHH) THEN
    bAlarm_BearingTemp_HH := TRUE;
ELSE
    IF (rTurbineBearingTemp_TT502A < (cBearingTemp_TripHH - 4.0))
       AND (rTurbineBearingTemp_TT502B < (cBearingTemp_TripHH - 4.0))
       AND (rTurbineThrustBearingTemp_TT503 < (cBearingTemp_TripHH - 4.0))
       AND (rGeneratorBearingTemp_TT402 < (cBearingTemp_TripHH - 4.0)) THEN
        bAlarm_BearingTemp_HH := FALSE;
    END_IF;
END_IF;

IF (rTurbineBearingTemp_TT502A >= cBearingTemp_AlarmH)
   OR (rTurbineBearingTemp_TT502B >= cBearingTemp_AlarmH)
   OR (rTurbineThrustBearingTemp_TT503 >= cBearingTemp_AlarmH)
   OR (rGeneratorBearingTemp_TT402 >= cBearingTemp_AlarmH) THEN
    bAlarm_BearingTemp_H := TRUE;
ELSE
    IF (rTurbineBearingTemp_TT502A < (cBearingTemp_AlarmH - 3.0))
       AND (rTurbineBearingTemp_TT502B < (cBearingTemp_AlarmH - 3.0))
       AND (rTurbineThrustBearingTemp_TT503 < (cBearingTemp_AlarmH - 3.0))
       AND (rGeneratorBearingTemp_TT402 < (cBearingTemp_AlarmH - 3.0)) THEN
        bAlarm_BearingTemp_H := FALSE;
    END_IF;
END_IF;

(* Lubrication Oil Header Pressure Collapse *)
IF rLubeOilSupplyPress_PT801 <= cLubeOilPress_TripLL THEN
    bAlarm_LubeOil_LL := TRUE;
ELSIF rLubeOilSupplyPress_PT801 >= (cLubeOilPress_TripLL + 0.3) THEN
    bAlarm_LubeOil_LL := FALSE;
END_IF;

IF rLubeOilSupplyPress_PT801 <= cLubeOilPress_AlarmL THEN
    bAlarm_LubeOil_L := TRUE;
ELSIF rLubeOilSupplyPress_PT801 >= (cLubeOilPress_AlarmL + 0.3) THEN
    bAlarm_LubeOil_L := FALSE;
END_IF;

(* Nitrogen Shaft Seal Differential Pressure *)
IF rN2SealGasDiffPress_DPT901 <= cN2SealDiffPress_TripLL THEN
    bAlarm_N2Seal_LL := TRUE;
ELSIF rN2SealGasDiffPress_DPT901 >= (cN2SealDiffPress_TripLL + 3.0) THEN
    bAlarm_N2Seal_LL := FALSE;
END_IF;

IF rN2SealGasDiffPress_DPT901 <= cN2SealDiffPress_AlarmL THEN
    bAlarm_N2Seal_L := TRUE;
ELSIF rN2SealGasDiffPress_DPT901 >= (cN2SealDiffPress_AlarmL + 3.0) THEN
    bAlarm_N2Seal_L := FALSE;
END_IF;

(* Flammable Gas Oxygen Ingress Alarm *)
IF rGasOxygenConcentration_AT101 >= cOxygenConc_TripHH THEN
    bAlarm_Oxygen_HH := TRUE;
ELSIF rGasOxygenConcentration_AT101 <= 0.60 THEN
    bAlarm_Oxygen_HH := FALSE;
END_IF;

(* Fast Bypass Hydraulic Accumulator Depressurization *)
IF rFastBypassAccumPress_PT804 < 145.0 THEN
    bAlarm_FastBypassHydraulic_Low := TRUE;
ELSIF rFastBypassAccumPress_PT804 > 165.0 THEN
    bAlarm_FastBypassHydraulic_Low := FALSE;
END_IF;

(* Generator Electrical Reverse Power Protection *)
IF bGridBreakerClosed_Feedback AND (rVoted_GeneratorActivePower < -0.35) AND (nFsmStateTimer_ms > 4000) THEN
    bAlarm_GeneratorReversePower := TRUE;
ELSE
    IF rVoted_GeneratorActivePower > 0.10 THEN
        bAlarm_GeneratorReversePower := FALSE;
    END_IF;
END_IF;

(* TMR Multi-Channel Sensor Failure Alarm *)
IF (nCh1_HealthyCount <= 1) OR (nCh2_HealthyCount <= 1) OR (nCh3_HealthyCount <= 1)
   OR (nCh4_HealthyCount <= 1) OR (nCh5_HealthyCount <= 1) OR (nCh6_HealthyCount <= 1) THEN
    bAlarm_TMR_MajorSensorFailure := TRUE;
ELSE
    bAlarm_TMR_MajorSensorFailure := FALSE;
END_IF;


(* ---------------------------------------------------------------------------------------------------- *)
(* 5.2 FIRST-OUT EMERGENCY HARDWARE TRIP DETERMINATION & REGISTRATION                                   *)
(* ---------------------------------------------------------------------------------------------------- *)
IF NOT bEmergencyMasterTripActive THEN
    IF bEmergencyTripManual THEN
        nFirstOutTripReasonCode := 1; (* Manual Operator Emergency Trip *)
        bEmergencyMasterTripActive := TRUE;
        bHardwareMasterTripEngaged := TRUE;
    ELSIF bAlarm_TurbineSpeed_HH THEN
        nFirstOutTripReasonCode := 2; (* Turbine Overspeed Hardware Trip *)
        bEmergencyMasterTripActive := TRUE;
        bHardwareMasterTripEngaged := TRUE;
    ELSIF bAlarm_TurbineVib_HH THEN
        nFirstOutTripReasonCode := 3; (* Shaft Radial Vibration ISO 10816 Zone D Trip *)
        bEmergencyMasterTripActive := TRUE;
        bHardwareMasterTripEngaged := TRUE;
    ELSIF bAlarm_BearingTemp_HH THEN
        nFirstOutTripReasonCode := 4; (* Bearing Metal Temperature High-High Trip *)
        bEmergencyMasterTripActive := TRUE;
        bHardwareMasterTripEngaged := TRUE;
    ELSIF bAlarm_LubeOil_LL THEN
        nFirstOutTripReasonCode := 5; (* Lubrication Oil Pressure Loss Trip *)
        bEmergencyMasterTripActive := TRUE;
        bHardwareMasterTripEngaged := TRUE;
    ELSIF bAlarm_N2Seal_LL THEN
        nFirstOutTripReasonCode := 6; (* Nitrogen Labyrinth Seal Pressure Collapse Trip *)
        bEmergencyMasterTripActive := TRUE;
        bHardwareMasterTripEngaged := TRUE;
    ELSIF bAlarm_TopPress_HH THEN
        nFirstOutTripReasonCode := 7; (* Catastrophic Blast Furnace Top Overpressure Trip *)
        bEmergencyMasterTripActive := TRUE;
        bHardwareMasterTripEngaged := TRUE;
    ELSIF bAlarm_TopPress_LL THEN
        nFirstOutTripReasonCode := 8; (* Dangerous Blast Furnace Low Pressure Trip *)
        bEmergencyMasterTripActive := TRUE;
        bHardwareMasterTripEngaged := TRUE;
    ELSIF bAlarm_BagFilter_dPHH THEN
        nFirstOutTripReasonCode := 9; (* Bag Filter Blinding / High Differential Pressure Trip *)
        bEmergencyMasterTripActive := TRUE;
        bHardwareMasterTripEngaged := TRUE;
    ELSIF bAlarm_BagFilter_dPLL THEN
        nFirstOutTripReasonCode := 10; (* Bag Filter Membrane Rupture / Fly Ash Ingress Trip *)
        bEmergencyMasterTripActive := TRUE;
        bHardwareMasterTripEngaged := TRUE;
    ELSIF bAlarm_BagFilter_TempHH THEN
        nFirstOutTripReasonCode := 11; (* Bag Filter High Temperature Scorch Trip *)
        bEmergencyMasterTripActive := TRUE;
        bHardwareMasterTripEngaged := TRUE;
    ELSIF bAlarm_BagFilter_TempLL THEN
        nFirstOutTripReasonCode := 12; (* Bag Filter Acid Dewpoint Condensation Trip *)
        bEmergencyMasterTripActive := TRUE;
        bHardwareMasterTripEngaged := TRUE;
    ELSIF bAlarm_Oxygen_HH THEN
        nFirstOutTripReasonCode := 13; (* Flammable Oxygen Infiltration Trip *)
        bEmergencyMasterTripActive := TRUE;
        bHardwareMasterTripEngaged := TRUE;
    ELSIF bAlarm_FastBypassHydraulic_Low THEN
        nFirstOutTripReasonCode := 14; (* Fast Bypass Hydraulic Accumulator Depressurization Trip *)
        bEmergencyMasterTripActive := TRUE;
        bHardwareMasterTripEngaged := TRUE;
    ELSIF bAlarm_GeneratorReversePower THEN
        nFirstOutTripReasonCode := 15; (* Generator Reverse Power Motoring Trip *)
        bEmergencyMasterTripActive := TRUE;
        bHardwareMasterTripEngaged := TRUE;
    ELSIF bAlarm_TMR_MajorSensorFailure THEN
        nFirstOutTripReasonCode := 16; (* Multiple Redundant Instrumentation Loss Trip *)
        bEmergencyMasterTripActive := TRUE;
        bHardwareMasterTripEngaged := TRUE;
    ELSIF NOT bGeneratorElectricalProtectionOK THEN
        nFirstOutTripReasonCode := 17; (* Generator Protection Relay Differential/Stator Fault *)
        bEmergencyMasterTripActive := TRUE;
        bHardwareMasterTripEngaged := TRUE;
    END_IF;

    (* Force FSM to Emergency Trip State *)
    IF bEmergencyMasterTripActive THEN
        eFsmCurrentState := 12;
    END_IF;
END_IF;

(* Clear First-Out Reason on Complete Reset *)
IF bReset AND (NOT bEmergencyMasterTripActive) THEN
    bHardwareMasterTripEngaged := FALSE;
    nFirstOutTripReasonCode := 0;
END_IF;


(* ---------------------------------------------------------------------------------------------------- *)
(* 5.3 32-BIT BIT-PACKED TELEMETRY WORDS (STATUS, ALARMS & TMR DIAGNOSTICS)                             *)
(* ---------------------------------------------------------------------------------------------------- *)
(* Word 1: Critical Alarms and Emergency Trips (udwAlarmWord1) *)
udwAlarmWord1 := 16#00000000;
IF bAlarm_TopPress_HH              THEN udwAlarmWord1 := udwAlarmWord1 OR 16#00000001; END_IF;
IF bAlarm_TopPress_H               THEN udwAlarmWord1 := udwAlarmWord1 OR 16#00000002; END_IF;
IF bAlarm_TopPress_L               THEN udwAlarmWord1 := udwAlarmWord1 OR 16#00000004; END_IF;
IF bAlarm_TopPress_LL              THEN udwAlarmWord1 := udwAlarmWord1 OR 16#00000008; END_IF;
IF bAlarm_TopPress_SlipROC         THEN udwAlarmWord1 := udwAlarmWord1 OR 16#00000010; END_IF;
IF bAlarm_TurbineSpeed_HH          THEN udwAlarmWord1 := udwAlarmWord1 OR 16#00000020; END_IF;
IF bAlarm_TurbineSpeed_H           THEN udwAlarmWord1 := udwAlarmWord1 OR 16#00000040; END_IF;
IF bAlarm_TurbineVib_HH            THEN udwAlarmWord1 := udwAlarmWord1 OR 16#00000080; END_IF;
IF bAlarm_TurbineVib_H             THEN udwAlarmWord1 := udwAlarmWord1 OR 16#00000100; END_IF;
IF bAlarm_BagFilter_dPHH           THEN udwAlarmWord1 := udwAlarmWord1 OR 16#00000200; END_IF;
IF bAlarm_BagFilter_dPH            THEN udwAlarmWord1 := udwAlarmWord1 OR 16#00000400; END_IF;
IF bAlarm_BagFilter_dPLL           THEN udwAlarmWord1 := udwAlarmWord1 OR 16#00000800; END_IF;
IF bAlarm_BagFilter_TempHH         THEN udwAlarmWord1 := udwAlarmWord1 OR 16#00001000; END_IF;
IF bAlarm_BagFilter_TempLL         THEN udwAlarmWord1 := udwAlarmWord1 OR 16#00002000; END_IF;
IF bAlarm_BearingTemp_HH           THEN udwAlarmWord1 := udwAlarmWord1 OR 16#00004000; END_IF;
IF bAlarm_BearingTemp_H            THEN udwAlarmWord1 := udwAlarmWord1 OR 16#00008000; END_IF;
IF bAlarm_LubeOil_LL               THEN udwAlarmWord1 := udwAlarmWord1 OR 16#00010000; END_IF;
IF bAlarm_LubeOil_L                THEN udwAlarmWord1 := udwAlarmWord1 OR 16#00020000; END_IF;
IF bAlarm_N2Seal_LL                THEN udwAlarmWord1 := udwAlarmWord1 OR 16#00040000; END_IF;
IF bAlarm_N2Seal_L                 THEN udwAlarmWord1 := udwAlarmWord1 OR 16#00080000; END_IF;
IF bAlarm_Oxygen_HH                THEN udwAlarmWord1 := udwAlarmWord1 OR 16#00100000; END_IF;
IF bAlarm_FastBypassHydraulic_Low  THEN udwAlarmWord1 := udwAlarmWord1 OR 16#00200000; END_IF;
IF bAlarm_GeneratorReversePower    THEN udwAlarmWord1 := udwAlarmWord1 OR 16#00400000; END_IF;
IF bAlarm_TMR_MajorSensorFailure   THEN udwAlarmWord1 := udwAlarmWord1 OR 16#00800000; END_IF;
IF NOT bGeneratorElectricalProtectionOK THEN udwAlarmWord1 := udwAlarmWord1 OR 16#01000000; END_IF;
IF bEmergencyTripManual            THEN udwAlarmWord1 := udwAlarmWord1 OR 16#02000000; END_IF;
IF bEmergencyMasterTripActive      THEN udwAlarmWord1 := udwAlarmWord1 OR 16#80000000; END_IF;

(* Word 2: Equipment Warnings & Operational Flags (udwAlarmWord2) *)
udwAlarmWord2 := 16#00000000;
IF bCh1_DegradedLatch              THEN udwAlarmWord2 := udwAlarmWord2 OR 16#00000001; END_IF;
IF bCh2_DegradedLatch              THEN udwAlarmWord2 := udwAlarmWord2 OR 16#00000002; END_IF;
IF bCh3_DegradedLatch              THEN udwAlarmWord2 := udwAlarmWord2 OR 16#00000004; END_IF;
IF bCh4_DegradedLatch              THEN udwAlarmWord2 := udwAlarmWord2 OR 16#00000008; END_IF;
IF bCh5_DegradedLatch              THEN udwAlarmWord2 := udwAlarmWord2 OR 16#00000010; END_IF;
IF bCh6_DegradedLatch              THEN udwAlarmWord2 := udwAlarmWord2 OR 16#00000020; END_IF;
IF NOT bSpeed_SensorA_Healthy      THEN udwAlarmWord2 := udwAlarmWord2 OR 16#00000040; END_IF;
IF NOT bSpeed_SensorB_Healthy      THEN udwAlarmWord2 := udwAlarmWord2 OR 16#00000080; END_IF;
IF NOT bScouringSprayHeader_PressOK THEN udwAlarmWord2 := udwAlarmWord2 OR 16#00000100; END_IF;
IF NOT bBagFilterPulseJet_Running  THEN udwAlarmWord2 := udwAlarmWord2 OR 16#00000200; END_IF;

(* Word 3: Supervisory Status Word (udwStatusWord) *)
udwStatusWord := INT_TO_DWORD(eFsmCurrentState) AND 16#0000000F;
IF bAutoMode                       THEN udwStatusWord := udwStatusWord OR 16#00000010; END_IF;
IF bGridBreakerClosed_Feedback     THEN udwStatusWord := udwStatusWord OR 16#00000020; END_IF;
IF bTRT_PowerRecoveryActive        THEN udwStatusWord := udwStatusWord OR 16#00000040; END_IF;
IF bClosedLoopPressureLocked       THEN udwStatusWord := udwStatusWord OR 16#00000080; END_IF;
IF bSystemReadyToStart             THEN udwStatusWord := udwStatusWord OR 16#00000100; END_IF;
IF bJackingOilPumpRunning          THEN udwStatusWord := udwStatusWord OR 16#00000200; END_IF;
IF bLubeOilPumpsRunning            THEN udwStatusWord := udwStatusWord OR 16#00000400; END_IF;
IF bFastBypassValve_TripOpen       THEN udwStatusWord := udwStatusWord OR 16#00000800; END_IF;
IF NOT bInletESV_TripClose         THEN udwStatusWord := udwStatusWord OR 16#00001000; END_IF;
IF bBleederValves_EmergencyCrackOpen THEN udwStatusWord := udwStatusWord OR 16#00002000; END_IF;
IF bScouringSpraySolenoid_Open     THEN udwStatusWord := udwStatusWord OR 16#00004000; END_IF;
IF bCasingN2Purge_Solenoid_Open    THEN udwStatusWord := udwStatusWord OR 16#00008000; END_IF;

(* Word 4: 2oo3 TMR Channel Health Diagnostics (udwTMRDiagWord) *)
udwTMRDiagWord := 16#00000000;
IF bCh1_HealthA THEN udwTMRDiagWord := udwTMRDiagWord OR 16#00000001; END_IF;
IF bCh1_HealthB THEN udwTMRDiagWord := udwTMRDiagWord OR 16#00000002; END_IF;
IF bCh1_HealthC THEN udwTMRDiagWord := udwTMRDiagWord OR 16#00000004; END_IF;
IF bCh2_HealthA THEN udwTMRDiagWord := udwTMRDiagWord OR 16#00000008; END_IF;
IF bCh2_HealthB THEN udwTMRDiagWord := udwTMRDiagWord OR 16#00000010; END_IF;
IF bCh2_HealthC THEN udwTMRDiagWord := udwTMRDiagWord OR 16#00000020; END_IF;
IF bCh3_HealthA THEN udwTMRDiagWord := udwTMRDiagWord OR 16#00000040; END_IF;
IF bCh3_HealthB THEN udwTMRDiagWord := udwTMRDiagWord OR 16#00000080; END_IF;
IF bCh3_HealthC THEN udwTMRDiagWord := udwTMRDiagWord OR 16#00000100; END_IF;
IF bCh4_HealthA THEN udwTMRDiagWord := udwTMRDiagWord OR 16#00000200; END_IF;
IF bCh4_HealthB THEN udwTMRDiagWord := udwTMRDiagWord OR 16#00000400; END_IF;
IF bCh4_HealthC THEN udwTMRDiagWord := udwTMRDiagWord OR 16#00000800; END_IF;
IF bCh5_HealthA THEN udwTMRDiagWord := udwTMRDiagWord OR 16#00001000; END_IF;
IF bCh5_HealthB THEN udwTMRDiagWord := udwTMRDiagWord OR 16#00002000; END_IF;
IF bCh5_HealthC THEN udwTMRDiagWord := udwTMRDiagWord OR 16#00004000; END_IF;
IF bCh6_HealthA THEN udwTMRDiagWord := udwTMRDiagWord OR 16#00008000; END_IF;
IF bCh6_HealthB THEN udwTMRDiagWord := udwTMRDiagWord OR 16#00010000; END_IF;
IF bCh6_HealthC THEN udwTMRDiagWord := udwTMRDiagWord OR 16#00020000; END_IF;
IF bSpeed_SensorA_Healthy THEN udwTMRDiagWord := udwTMRDiagWord OR 16#00040000; END_IF;
IF bSpeed_SensorB_Healthy THEN udwTMRDiagWord := udwTMRDiagWord OR 16#00080000; END_IF;

(* Word 5: First-Out Emergency Trip Word *)
udwFirstOutTripWord := INT_TO_DWORD(nFirstOutTripReasonCode);


(* ---------------------------------------------------------------------------------------------------- *)
(* 5.4 FINAL ACTUATOR POSITION CLAMPING & REGISTER MEMORY UPDATE                                        *)
(* ---------------------------------------------------------------------------------------------------- *)
(* Rate Slew Clamping on VSV Actuator Demand *)
IF (rVSV_Demand_RateClamped - aControlPrev[1]) > aActuatorMaxSlewRate[1] THEN
    rVSV_Demand_RateClamped := aControlPrev[1] + aActuatorMaxSlewRate[1];
ELSIF (rVSV_Demand_RateClamped - aControlPrev[1]) < -aActuatorMaxSlewRate[1] THEN
    rVSV_Demand_RateClamped := aControlPrev[1] - aActuatorMaxSlewRate[1];
END_IF;

(* Rate Slew Clamping on Septum Valve 1 *)
IF (rSeptumV1_Demand_RateClamped - aControlPrev[2]) > aActuatorMaxSlewRate[2] THEN
    rSeptumV1_Demand_RateClamped := aControlPrev[2] + aActuatorMaxSlewRate[2];
ELSIF (rSeptumV1_Demand_RateClamped - aControlPrev[2]) < -aActuatorMaxSlewRate[2] THEN
    rSeptumV1_Demand_RateClamped := aControlPrev[2] - aActuatorMaxSlewRate[2];
END_IF;

(* Rate Slew Clamping on Septum Valve 2 *)
IF (rSeptumV2_Demand_RateClamped - aControlPrev[3]) > aActuatorMaxSlewRate[3] THEN
    rSeptumV2_Demand_RateClamped := aControlPrev[3] + aActuatorMaxSlewRate[3];
ELSIF (rSeptumV2_Demand_RateClamped - aControlPrev[3]) < -aActuatorMaxSlewRate[3] THEN
    rSeptumV2_Demand_RateClamped := aControlPrev[3] - aActuatorMaxSlewRate[3];
END_IF;

(* Rate Slew Clamping on Septum Valve 3 (Fine Trim) *)
IF (rSeptumV3_Demand_RateClamped - aControlPrev[4]) > aActuatorMaxSlewRate[4] THEN
    rSeptumV3_Demand_RateClamped := aControlPrev[4] + aActuatorMaxSlewRate[4];
ELSIF (rSeptumV3_Demand_RateClamped - aControlPrev[4]) < -aActuatorMaxSlewRate[4] THEN
    rSeptumV3_Demand_RateClamped := aControlPrev[4] - aActuatorMaxSlewRate[4];
END_IF;

(* Final Physical Actuator Boundaries Clamping [0.0..100.0%] *)
IF rVSV_Demand_RateClamped > 100.0 THEN rVSV_Demand_RateClamped := 100.0; END_IF;
IF rVSV_Demand_RateClamped < 0.0 THEN rVSV_Demand_RateClamped := 0.0; END_IF;

IF rSeptumV1_Demand_RateClamped > 100.0 THEN rSeptumV1_Demand_RateClamped := 100.0; END_IF;
IF rSeptumV1_Demand_RateClamped < 0.0 THEN rSeptumV1_Demand_RateClamped := 0.0; END_IF;

IF rSeptumV2_Demand_RateClamped > 100.0 THEN rSeptumV2_Demand_RateClamped := 100.0; END_IF;
IF rSeptumV2_Demand_RateClamped < 0.0 THEN rSeptumV2_Demand_RateClamped := 0.0; END_IF;

IF rSeptumV3_Demand_RateClamped > 100.0 THEN rSeptumV3_Demand_RateClamped := 100.0; END_IF;
IF rSeptumV3_Demand_RateClamped < 0.0 THEN rSeptumV3_Demand_RateClamped := 0.0; END_IF;

(* Drive Output Port Demands *)
rVSV_PositionDemand      := rVSV_Demand_RateClamped;
rSeptumV1_PositionDemand := rSeptumV1_Demand_RateClamped;
rSeptumV2_PositionDemand := rSeptumV2_Demand_RateClamped;
rSeptumV3_PositionDemand := rSeptumV3_Demand_RateClamped;

(* Update Actuator Control Memory Registers for Next Discrete Scan *)
aControlDemand[1] := rVSV_PositionDemand;
aControlDemand[2] := rSeptumV1_PositionDemand;
aControlDemand[3] := rSeptumV2_PositionDemand;
aControlDemand[4] := rSeptumV3_PositionDemand;
aControlDemand[5] := rVoted_GeneratorActivePower;

aControlPrev[1] := aControlDemand[1];
aControlPrev[2] := aControlDemand[2];
aControlPrev[3] := aControlDemand[3];
aControlPrev[4] := aControlDemand[4];
aControlPrev[5] := aControlDemand[5];

bEmergencyMasterTripActive := bHardwareMasterTripEngaged;

END_FUNCTION_BLOCK
"""
