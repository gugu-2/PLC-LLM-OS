# -*- coding: utf-8 -*-
"""
smt_builder/phase5_alarms_status.py
Generates Phase 5: ISA-18.2 Multi-Tier Alarms & 32-Bit Bit-Packed Status Words,
plus END_FUNCTION_BLOCK.
"""

def get_phase5_alarms():
    return """(*
========================================================================================================================
  PHASE 5: ISA-18.2 MULTI-TIER ALARMS & 32-BIT BIT-PACKED STATUS & DIAGNOSTIC WORDS
========================================================================================================================
  Monitors 16 cyber-physical process variables against multi-tier ISA-18.2 alarm thresholds:
    - High-High (HH) / Low-Low (LL) : Severity 1 Emergency Trips -> Category 0/1 Deceleration & Interlock Trip
    - High (H) / Low (L)           : Severity 2 Process Warnings -> Auto-Reject / Maintenance Advisory
    - Symmetrical Deadband Hysteresis: Prevents alarm chatter around boundary trip limits.
  Bit-packs diagnostic telemetry into standard 32-bit DWORD registers for plant SCADA/MES integration.
*)

(* -------------------------------------------------------------------------------------------------------------------- *)
(* SUB-PHASE 5.1: PROCESS VARIABLE TRACKING DEVIATIONS & FOLLOWING ERROR CALCULATIONS                                   *)
(* -------------------------------------------------------------------------------------------------------------------- *)
rCalc_FollowError_X := ABS(rActual_Gantry_X_Pos - rProfile_Pos_Target_X);
rCalc_FollowError_Y := ABS(rActual_Gantry_Y_Pos - rProfile_Pos_Target_Y);

(* -------------------------------------------------------------------------------------------------------------------- *)
(* SUB-PHASE 5.2: ISA-18.2 MULTI-TIER THRESHOLD EVALUATION WITH DEADBAND HYSTERESIS                                     *)
(* -------------------------------------------------------------------------------------------------------------------- *)
(* 1. Gantry X-Axis Following Error Alarm Evaluation *)
IF rCalc_FollowError_X >= rAlarmLimit_FollowError_HH_mm THEN
    bAlarm_FollowError_X_HH := TRUE;
ELSIF rCalc_FollowError_X < (rAlarmLimit_FollowError_HH_mm - rAlarmDeadband_FollowError_mm) THEN
    bAlarm_FollowError_X_HH := FALSE;
END_IF;

IF rCalc_FollowError_X >= rAlarmLimit_FollowError_H_mm THEN
    bAlarm_FollowError_X_H := TRUE;
ELSIF rCalc_FollowError_X < (rAlarmLimit_FollowError_H_mm - rAlarmDeadband_FollowError_mm) THEN
    bAlarm_FollowError_X_H := FALSE;
END_IF;

(* 2. Gantry Y-Axis Following Error Alarm Evaluation *)
IF rCalc_FollowError_Y >= rAlarmLimit_FollowError_HH_mm THEN
    bAlarm_FollowError_Y_HH := TRUE;
ELSIF rCalc_FollowError_Y < (rAlarmLimit_FollowError_HH_mm - rAlarmDeadband_FollowError_mm) THEN
    bAlarm_FollowError_Y_HH := FALSE;
END_IF;

IF rCalc_FollowError_Y >= rAlarmLimit_FollowError_H_mm THEN
    bAlarm_FollowError_Y_H := TRUE;
ELSIF rCalc_FollowError_Y < (rAlarmLimit_FollowError_H_mm - rAlarmDeadband_FollowError_mm) THEN
    bAlarm_FollowError_Y_H := FALSE;
END_IF;

(* 3. Vacuum Chamber Pressure Alarm Evaluation (Vacuum loss = pressure rising towards 0 kPa) *)
IF rActual_VacuumPressure_kPa >= rAlarmLimit_VacLeak_LL_kPa THEN
    bAlarm_VacuumLeak_LL := TRUE;
ELSIF rActual_VacuumPressure_kPa < (rAlarmLimit_VacLeak_LL_kPa - rAlarmDeadband_Vac_kPa) THEN
    bAlarm_VacuumLeak_LL := FALSE;
END_IF;

IF rActual_VacuumPressure_kPa >= rAlarmLimit_VacLow_L_kPa THEN
    bAlarm_VacuumLow_L := TRUE;
ELSIF rActual_VacuumPressure_kPa < (rAlarmLimit_VacLow_L_kPa - rAlarmDeadband_Vac_kPa) THEN
    bAlarm_VacuumLow_L := FALSE;
END_IF;

(* 4. Voice-Coil Landing Force Overshoot Alarm Evaluation *)
IF rEstimated_LandingForce_N >= rAlarmLimit_LandingForce_HH_N THEN
    bAlarm_LandingForce_HH := TRUE;
ELSIF rEstimated_LandingForce_N < (rAlarmLimit_LandingForce_HH_N - rAlarmDeadband_LandingForce_N) THEN
    bAlarm_LandingForce_HH := FALSE;
END_IF;

IF rEstimated_LandingForce_N >= rAlarmLimit_LandingForce_H_N THEN
    bAlarm_LandingForce_H := TRUE;
ELSIF rEstimated_LandingForce_N < (rAlarmLimit_LandingForce_H_N - rAlarmDeadband_LandingForce_N) THEN
    bAlarm_LandingForce_H := FALSE;
END_IF;

(* 5. Linear Scale Overtemperature Alarm Evaluation *)
IF (rTemp_LinearScale_X1 >= rAlarmLimit_ScaleTemp_HH_degC) OR
   (rTemp_LinearScale_X2 >= rAlarmLimit_ScaleTemp_HH_degC) OR
   (rTemp_LinearScale_Y  >= rAlarmLimit_ScaleTemp_HH_degC) THEN
    bAlarm_ScaleTemp_HH := TRUE;
ELSIF (rTemp_LinearScale_X1 < (rAlarmLimit_ScaleTemp_HH_degC - rAlarmDeadband_ScaleTemp_degC)) AND
      (rTemp_LinearScale_X2 < (rAlarmLimit_ScaleTemp_HH_degC - rAlarmDeadband_ScaleTemp_degC)) AND
      (rTemp_LinearScale_Y  < (rAlarmLimit_ScaleTemp_HH_degC - rAlarmDeadband_ScaleTemp_degC)) THEN
    bAlarm_ScaleTemp_HH := FALSE;
END_IF;

IF (rTemp_LinearScale_X1 >= rAlarmLimit_ScaleTemp_H_degC) OR
   (rTemp_LinearScale_X2 >= rAlarmLimit_ScaleTemp_H_degC) OR
   (rTemp_LinearScale_Y  >= rAlarmLimit_ScaleTemp_H_degC) THEN
    bAlarm_ScaleTemp_H := TRUE;
ELSIF (rTemp_LinearScale_X1 < (rAlarmLimit_ScaleTemp_H_degC - rAlarmDeadband_ScaleTemp_degC)) AND
      (rTemp_LinearScale_X2 < (rAlarmLimit_ScaleTemp_H_degC - rAlarmDeadband_ScaleTemp_degC)) AND
      (rTemp_LinearScale_Y  < (rAlarmLimit_ScaleTemp_H_degC - rAlarmDeadband_ScaleTemp_degC)) THEN
    bAlarm_ScaleTemp_H := FALSE;
END_IF;

(* 6. Main Pneumatic Supply Air Pressure Evaluation *)
IF rSupplyAirPressure <= rAlarmLimit_SupplyAir_LL_kPa THEN
    bAlarm_SupplyAir_LL := TRUE;
ELSIF rSupplyAirPressure > (rAlarmLimit_SupplyAir_LL_kPa + rAlarmDeadband_SupplyAir_kPa) THEN
    bAlarm_SupplyAir_LL := FALSE;
END_IF;

IF rSupplyAirPressure <= rAlarmLimit_SupplyAir_L_kPa THEN
    bAlarm_SupplyAir_L := TRUE;
ELSIF rSupplyAirPressure > (rAlarmLimit_SupplyAir_L_kPa + rAlarmDeadband_SupplyAir_kPa) THEN
    bAlarm_SupplyAir_L := FALSE;
END_IF;

(* 7. Optical Vision Component Translation Offset Exceedance *)
IF (ABS(rVision_OffsetX) >= rAlarmLimit_VisionOffset_HH_mm) OR
   (ABS(rVision_OffsetY) >= rAlarmLimit_VisionOffset_HH_mm) THEN
    bAlarm_VisionOffset_HH := TRUE;
ELSIF (ABS(rVision_OffsetX) < (rAlarmLimit_VisionOffset_HH_mm - rAlarmDeadband_VisionOffset_mm)) AND
      (ABS(rVision_OffsetY) < (rAlarmLimit_VisionOffset_HH_mm - rAlarmDeadband_VisionOffset_mm)) THEN
    bAlarm_VisionOffset_HH := FALSE;
END_IF;

IF (ABS(rVision_OffsetX) >= rAlarmLimit_VisionOffset_H_mm) OR
   (ABS(rVision_OffsetY) >= rAlarmLimit_VisionOffset_H_mm) THEN
    bAlarm_VisionOffset_H := TRUE;
ELSIF (ABS(rVision_OffsetX) < (rAlarmLimit_VisionOffset_H_mm - rAlarmDeadband_VisionOffset_mm)) AND
      (ABS(rVision_OffsetY) < (rAlarmLimit_VisionOffset_H_mm - rAlarmDeadband_VisionOffset_mm)) THEN
    bAlarm_VisionOffset_H := FALSE;
END_IF;

(* 8. Consecutive Component Mispick Rate Alarm *)
IF udiConsecutivePickFailsCount >= INT_TO_UDINT(rAlarmLimit_ConsecutiveFails_HH) THEN
    bAlarm_ConsecutiveMispick_HH := TRUE;
ELSE
    bAlarm_ConsecutiveMispick_HH := FALSE;
END_IF;

IF udiConsecutivePickFailsCount >= INT_TO_UDINT(rAlarmLimit_ConsecutiveFails_H) THEN
    bAlarm_ConsecutiveMispick_H := TRUE;
ELSE
    bAlarm_ConsecutiveMispick_H := FALSE;
END_IF;


(* -------------------------------------------------------------------------------------------------------------------- *)
(* SUB-PHASE 5.3: BIT-PACKED 32-BIT INDUSTRIAL DIAGNOSTIC & STATUS WORDS                                                *)
(* -------------------------------------------------------------------------------------------------------------------- *)
(* Reset status words before populating *)
dwStatus_GantryMotion := 16#00000000;
dwStatus_HeadSpindles := 16#00000000;
dwStatus_VisionInspection := 16#00000000;
dwAlarmWord1_ISA_CriticalTrips := 16#00000000;
dwAlarmWord2_ISA_ProcessWarnings := 16#00000000;
dwDiagnostic_FeederHealth := 16#00000000;

(* Bit-Pack Status Word 1: Gantry Motion & Servos *)
IF bSystemReady                               THEN dwStatus_GantryMotion := dwStatus_GantryMotion OR 16#00000001; END_IF;
IF bCycleBusy                                 THEN dwStatus_GantryMotion := dwStatus_GantryMotion OR 16#00000002; END_IF;
IF (rCalc_FollowError_X < 0.015)              THEN dwStatus_GantryMotion := dwStatus_GantryMotion OR 16#00000004; END_IF;
IF (rCalc_FollowError_Y < 0.015)              THEN dwStatus_GantryMotion := dwStatus_GantryMotion OR 16#00000008; END_IF;
IF (ABS(x_state[3]) < 0.003)                  THEN dwStatus_GantryMotion := dwStatus_GantryMotion OR 16#00000010; END_IF;
IF (ABS(x_state[9]) < 0.050)                  THEN dwStatus_GantryMotion := dwStatus_GantryMotion OR 16#00000020; END_IF;
IF (ABS(rComp_X_Total_mm) > 0.0001)           THEN dwStatus_GantryMotion := dwStatus_GantryMotion OR 16#00000040; END_IF;
IF (iTMR_X_DegradationState = 0)              THEN dwStatus_GantryMotion := dwStatus_GantryMotion OR 16#00000080; END_IF;
dwStatus_GantryMotion := dwStatus_GantryMotion OR SHL(INT_TO_DWORD(iFSM_State), 8);

(* Bit-Pack Status Word 2: 16-Spindle Head Part Presence (Bits 0-15) and Reject Flags (Bits 16-31) *)
FOR iIdxSpindle := 1 TO 16 DO
    IF arrSpindle_HasComponent[iIdxSpindle] THEN
        dwStatus_HeadSpindles := dwStatus_HeadSpindles OR SHL(16#00000001, iIdxSpindle - 1);
    END_IF;
    IF arrSpindle_RejectFlag[iIdxSpindle] THEN
        dwStatus_HeadSpindles := dwStatus_HeadSpindles OR SHL(16#00000001, iIdxSpindle + 15);
    END_IF;
END_FOR;

(* Bit-Pack Status Word 3: Optical Vision Inspection System *)
IF bCmd_VisionCamera_Strobe                   THEN dwStatus_VisionInspection := dwStatus_VisionInspection OR 16#00000001; END_IF;
IF bVision_TriggerAck                         THEN dwStatus_VisionInspection := dwStatus_VisionInspection OR 16#00000002; END_IF;
IF bVision_DataReady                          THEN dwStatus_VisionInspection := dwStatus_VisionInspection OR 16#00000004; END_IF;
IF bGlobalFiducialsAligned                    THEN dwStatus_VisionInspection := dwStatus_VisionInspection OR 16#00000008; END_IF;
IF bVision_LeadCoplanarPass                   THEN dwStatus_VisionInspection := dwStatus_VisionInspection OR 16#00000010; END_IF;
IF bVision_DefectRejectFlag                   THEN dwStatus_VisionInspection := dwStatus_VisionInspection OR 16#00000020; END_IF;
IF (iFSM_State = STATE_03_LASER_WARPAGE_SURFACE) THEN dwStatus_VisionInspection := dwStatus_VisionInspection OR 16#00000040; END_IF;

(* Bit-Pack Alarm Word 1: ISA-18.2 Severity 1 Critical Emergency Trips *)
IF NOT bEStop_SafetyInterlock                 THEN dwAlarmWord1_ISA_CriticalTrips := dwAlarmWord1_ISA_CriticalTrips OR 16#00000001; END_IF;
IF bTMR_X_MajorDiscrepancyTrip                THEN dwAlarmWord1_ISA_CriticalTrips := dwAlarmWord1_ISA_CriticalTrips OR 16#00000002; END_IF;
IF bTMR_Y_MajorDiscrepancyTrip                THEN dwAlarmWord1_ISA_CriticalTrips := dwAlarmWord1_ISA_CriticalTrips OR 16#00000004; END_IF;
IF bTMR_Theta_MajorDiscrepancyTrip            THEN dwAlarmWord1_ISA_CriticalTrips := dwAlarmWord1_ISA_CriticalTrips OR 16#00000008; END_IF;
IF bTMR_Vac_MajorDiscrepancyTrip              THEN dwAlarmWord1_ISA_CriticalTrips := dwAlarmWord1_ISA_CriticalTrips OR 16#00000010; END_IF;
IF bTMR_Laser_MajorDiscrepancyTrip            THEN dwAlarmWord1_ISA_CriticalTrips := dwAlarmWord1_ISA_CriticalTrips OR 16#00000020; END_IF;
IF bAlarm_FollowError_X_HH                    THEN dwAlarmWord1_ISA_CriticalTrips := dwAlarmWord1_ISA_CriticalTrips OR 16#00000040; END_IF;
IF bAlarm_FollowError_Y_HH                    THEN dwAlarmWord1_ISA_CriticalTrips := dwAlarmWord1_ISA_CriticalTrips OR 16#00000080; END_IF;
IF bAlarm_LandingForce_HH                     THEN dwAlarmWord1_ISA_CriticalTrips := dwAlarmWord1_ISA_CriticalTrips OR 16#00000100; END_IF;
IF bAlarm_ScaleTemp_HH                        THEN dwAlarmWord1_ISA_CriticalTrips := dwAlarmWord1_ISA_CriticalTrips OR 16#00000200; END_IF;
IF bAlarm_SupplyAir_LL                        THEN dwAlarmWord1_ISA_CriticalTrips := dwAlarmWord1_ISA_CriticalTrips OR 16#00000400; END_IF;
IF bAlarm_ConsecutiveMispick_HH               THEN dwAlarmWord1_ISA_CriticalTrips := dwAlarmWord1_ISA_CriticalTrips OR 16#00000800; END_IF;

(* Bit-Pack Alarm Word 2: ISA-18.2 Severity 2 Process Warnings & Degradations *)
IF bAlarm_FollowError_X_H                     THEN dwAlarmWord2_ISA_ProcessWarnings := dwAlarmWord2_ISA_ProcessWarnings OR 16#00000001; END_IF;
IF bAlarm_FollowError_Y_H                     THEN dwAlarmWord2_ISA_ProcessWarnings := dwAlarmWord2_ISA_ProcessWarnings OR 16#00000002; END_IF;
IF bAlarm_VacuumLow_L                         THEN dwAlarmWord2_ISA_ProcessWarnings := dwAlarmWord2_ISA_ProcessWarnings OR 16#00000004; END_IF;
IF bAlarm_VacuumLeak_LL                       THEN dwAlarmWord2_ISA_ProcessWarnings := dwAlarmWord2_ISA_ProcessWarnings OR 16#00000008; END_IF;
IF bAlarm_LandingForce_H                      THEN dwAlarmWord2_ISA_ProcessWarnings := dwAlarmWord2_ISA_ProcessWarnings OR 16#00000010; END_IF;
IF bAlarm_ScaleTemp_H                         THEN dwAlarmWord2_ISA_ProcessWarnings := dwAlarmWord2_ISA_ProcessWarnings OR 16#00000020; END_IF;
IF bAlarm_SupplyAir_L                         THEN dwAlarmWord2_ISA_ProcessWarnings := dwAlarmWord2_ISA_ProcessWarnings OR 16#00000040; END_IF;
IF bAlarm_VisionOffset_H                      THEN dwAlarmWord2_ISA_ProcessWarnings := dwAlarmWord2_ISA_ProcessWarnings OR 16#00000080; END_IF;
IF bAlarm_VisionOffset_HH                     THEN dwAlarmWord2_ISA_ProcessWarnings := dwAlarmWord2_ISA_ProcessWarnings OR 16#00000100; END_IF;
IF bAlarm_ConsecutiveMispick_H                THEN dwAlarmWord2_ISA_ProcessWarnings := dwAlarmWord2_ISA_ProcessWarnings OR 16#00000200; END_IF;
IF (iTMR_X_DegradationState = 1) OR
   (iTMR_Y_DegradationState = 1) OR
   (iTMR_Theta_DegradationState = 1)          THEN dwAlarmWord2_ISA_ProcessWarnings := dwAlarmWord2_ISA_ProcessWarnings OR 16#00000400; END_IF;

(* Bit-Pack Diagnostic Word: Feeder Bank Health *)
IF bFeederBank_Ready                          THEN dwDiagnostic_FeederHealth := dwDiagnostic_FeederHealth OR 16#00000001; END_IF;
IF bFeeder_TapeAdvanceDone                    THEN dwDiagnostic_FeederHealth := dwDiagnostic_FeederHealth OR 16#00000002; END_IF;
IF bFeeder_TapeJamDetected                    THEN dwDiagnostic_FeederHealth := dwDiagnostic_FeederHealth OR 16#00000004; END_IF;
IF bFeeder_CoverTapePeelError                 THEN dwDiagnostic_FeederHealth := dwDiagnostic_FeederHealth OR 16#00000008; END_IF;
IF bFeeder_SprocketDriveSlip                  THEN dwDiagnostic_FeederHealth := dwDiagnostic_FeederHealth OR 16#00000010; END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* SUB-PHASE 5.4: PRODUCTION TELEMETRY & PLACEMENT THROUGHPUT COMPUTATION                                               *)
(* -------------------------------------------------------------------------------------------------------------------- *)
udiPlacementIntervalTimer_ms := udiPlacementIntervalTimer_ms + 1;
IF udiPlacementIntervalTimer_ms >= 1000 THEN
    (* Compute CPH (Components Per Hour) throughput based on active placed parts and elapsed dwell *)
    IF udiTotalPartsPlacedCount > 0 THEN
        rPlacementRateSmoothed := (UDINT_TO_REAL(udiTotalPartsPlacedCount) * 3600000.0) /
                                  MAX(1000.0, UDINT_TO_REAL(udiFSM_StateDwell_ms + 10000));
        (* Saturate throughput to rated maximum: 100,000 CPH *)
        IF rPlacementRateSmoothed > 100000.0 THEN
            rPlacementRateSmoothed := 100000.0;
        END_IF;
        rActual_PlacementRate_CPH := rPlacementRateSmoothed;
    ELSE
        rActual_PlacementRate_CPH := 0.0;
    END_IF;
    udiPlacementIntervalTimer_ms := 0;
END_IF;

(* Master Cell Fault Summary Interlock Evaluation *)
IF (dwAlarmWord1_ISA_CriticalTrips <> 16#00000000) THEN
    bGeneralFault := TRUE;
    IF iFSM_State <> STATE_14_ESTOP_CONTROLLED_STOP THEN
        iFSM_State := STATE_14_ESTOP_CONTROLLED_STOP;
    END_IF;
END_IF;

END_FUNCTION_BLOCK
"""
