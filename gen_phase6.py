# gen_phase6.py - Generates Phase 6: ISA-18.2 Alarms & Bitfield Packing

def generate_phase6():
    return """(* ==================================================================================================================== *)
(* PHASE 6: ISA-18.2 MULTI-TIERED ALARM MATRIX & TELEMETRY BITFIELD PACKING                                             *)
(* ==================================================================================================================== *)

(* --- 6.1: ISA-18.2 Priority 1 (Emergency Trip) & Priority 2 (Warning) Alarm Evaluations --- *)

(* 1. Product Cake Collapse Danger (HH) during Primary Drying *)
IF ((eCurrentState = 60) OR (eCurrentState = 70)) AND (rVotedProductTemperatureActual >= rAlarmSet_ProductCollapse_HH) THEN
    bAlarm_ProductCollapseRisk_HH := TRUE;
ELSIF rVotedProductTemperatureActual < (rAlarmSet_ProductCollapse_HH - rAlarmSet_ProductTempDeadband) THEN
    bAlarm_ProductCollapseRisk_HH := FALSE;
END_IF;

(* 2. Product Sublimation High Temperature Alert (H) *)
IF ((eCurrentState = 60) OR (eCurrentState = 70)) AND (rVotedProductTemperatureActual >= rAlarmSet_ProductTempHigh_H) THEN
    bAlarm_ProductTempHigh_H := TRUE;
ELSIF rVotedProductTemperatureActual < (rAlarmSet_ProductTempHigh_H - rAlarmSet_ProductTempDeadband) THEN
    bAlarm_ProductTempHigh_H := FALSE;
END_IF;

(* 3. Chamber Vacuum Loss (HH) during Drying *)
IF ((eCurrentState >= 50) AND (eCurrentState <= 80)) AND (rVotedChamberPressure_CM_Actual >= rAlarmSet_VacuumLost_HH) THEN
    bAlarm_VacuumLost_HH := TRUE;
ELSIF rVotedChamberPressure_CM_Actual < (rAlarmSet_VacuumLost_HH - rAlarmSet_VacuumDeadband) THEN
    bAlarm_VacuumLost_HH := FALSE;
END_IF;

(* 4. Chamber Vacuum High Warning (H) *)
IF ((eCurrentState = 60) OR (eCurrentState = 70)) AND (rVotedChamberPressure_CM_Actual >= rAlarmSet_VacuumHigh_H) THEN
    bAlarm_VacuumHigh_H := TRUE;
ELSIF rVotedChamberPressure_CM_Actual < (rAlarmSet_VacuumHigh_H - rAlarmSet_VacuumDeadband) THEN
    bAlarm_VacuumHigh_H := FALSE;
END_IF;

(* 5. Ice Condenser Refrigeration Surface Temperature High (HH) *)
IF ((eCurrentState >= 50) AND (eCurrentState <= 80)) AND (rVotedCondenserCoilTempActual >= rAlarmSet_CondenserTempHigh_HH) THEN
    bAlarm_CondenserTempHigh_HH := TRUE;
ELSIF rVotedCondenserCoilTempActual < (rAlarmSet_CondenserTempHigh_HH - rAlarmSet_CondenserDeadband) THEN
    bAlarm_CondenserTempHigh_HH := FALSE;
END_IF;

(* 6. Ice Condenser Surface Temperature High Alert (H) *)
IF ((eCurrentState >= 50) AND (eCurrentState <= 80)) AND (rVotedCondenserCoilTempActual >= rAlarmSet_CondenserTempHigh_H) THEN
    bAlarm_CondenserTempHigh_H := TRUE;
ELSIF rVotedCondenserCoilTempActual < (rAlarmSet_CondenserTempHigh_H - rAlarmSet_CondenserDeadband) THEN
    bAlarm_CondenserTempHigh_H := FALSE;
END_IF;

(* 7. Shelf Silicone Oil Recirculation Flow Rate Low (LL) *)
IF (eCurrentState > 0) AND (rSiliconeOilCirculationFlowRate <= rAlarmSet_SiliconeOilFlow_LL) THEN
    bAlarm_SiliconeOilFlow_LL := TRUE;
ELSIF rSiliconeOilCirculationFlowRate > (rAlarmSet_SiliconeOilFlow_LL + rAlarmSet_SiliconeOilFlowDeadband) THEN
    bAlarm_SiliconeOilFlow_LL := FALSE;
END_IF;

(* 8. Shelf Electric SCR Heater Runaway High (HH) *)
IF rVotedShelfTemperatureActual >= rAlarmSet_ShelfThermalRunaway_HH THEN
    bAlarm_ShelfThermalRunaway_HH := TRUE;
ELSIF rVotedShelfTemperatureActual < (rAlarmSet_ShelfThermalRunaway_HH - rAlarmSet_ShelfTempDeadband) THEN
    bAlarm_ShelfThermalRunaway_HH := FALSE;
END_IF;

(* 9. Shelf Spatial Thermal Spread Gradient (H) *)
IF ABS(rShelfDeltaT_InletOutlet) >= rAlarmSet_ShelfSpread_H THEN
    bAlarm_ShelfSpread_H := TRUE;
ELSIF ABS(rShelfDeltaT_InletOutlet) < (rAlarmSet_ShelfSpread_H - rAlarmSet_ShelfSpreadDeadband) THEN
    bAlarm_ShelfSpread_H := FALSE;
END_IF;

(* 10. Dual-Stage Screw Compressor High Discharge Head Pressure (HH) *)
IF (rCompressor1_DischargePressure >= rAlarmSet_CompressorHead_HH) OR (rCompressor2_DischargePressure >= rAlarmSet_CompressorHead_HH) THEN
    bAlarm_CompressorHead_HH := TRUE;
ELSIF (rCompressor1_DischargePressure < (rAlarmSet_CompressorHead_HH - rAlarmSet_CompressorDeadband)) AND
      (rCompressor2_DischargePressure < (rAlarmSet_CompressorHead_HH - rAlarmSet_CompressorDeadband)) THEN
    bAlarm_CompressorHead_HH := FALSE;
END_IF;

(* 11. Shelf Stoppering Compaction Force Shortfall (LL) during Stoppering Dwell *)
IF (eCurrentState = 100) AND (nSubPhaseStep = 1) AND (rVotedHydraulicRamForceActual <= rAlarmSet_StopperingForce_LL) THEN
    bAlarm_StopperingForce_LL := TRUE;
ELSIF rVotedHydraulicRamForceActual > (rAlarmSet_StopperingForce_LL + rAlarmSet_StopperingForceDeadband) THEN
    bAlarm_StopperingForce_LL := FALSE;
END_IF;

(* 12. Hydraulic Skid System Overpressure (HH) *)
IF rHydraulicSystemLinePressure >= rAlarmSet_HydraulicOilPres_HH THEN
    bAlarm_HydraulicOilPres_HH := TRUE;
ELSIF rHydraulicSystemLinePressure < (rAlarmSet_HydraulicOilPres_HH - rAlarmSet_HydraulicDeadband) THEN
    bAlarm_HydraulicOilPres_HH := FALSE;
END_IF;

(* 13. Aseptic Chamber Door Interlock Violated (HH) *)
IF (NOT bChamberDoorClosedLocked_NC) AND (eCurrentState >= 30) AND (eCurrentState <= 100) THEN
    bAlarm_DoorInterlockViolated_HH := TRUE;
ELSE
    bAlarm_DoorInterlockViolated_HH := FALSE;
END_IF;

(* 14. Emergency Stop Circuit Tripped (HH) *)
IF NOT bEmergencyStopCircuit_NC THEN
    bAlarm_EmergencyStopTripped_HH := TRUE;
ELSE
    bAlarm_EmergencyStopTripped_HH := FALSE;
END_IF;

(* 15. Sterile Nitrogen Supply Header Pressure Low (L) *)
IF rSterileN2HeaderSupplyPressure <= rAlarmSet_SterileN2Supply_L THEN
    bAlarm_SterileN2Supply_L := TRUE;
ELSIF rSterileN2HeaderSupplyPressure > (rAlarmSet_SterileN2Supply_L + rAlarmSet_SterileN2Deadband) THEN
    bAlarm_SterileN2Supply_L := FALSE;
END_IF;

(* --- 6.2: Global Safety Trip Transition Evaluation --- *)
IF bAlarm_ProductCollapseRisk_HH OR
   bAlarm_VacuumLost_HH OR
   bAlarm_CondenserTempHigh_HH OR
   bAlarm_SiliconeOilFlow_LL OR
   bAlarm_ShelfThermalRunaway_HH OR
   bAlarm_CompressorHead_HH OR
   bAlarm_HydraulicOilPres_HH OR
   bAlarm_DoorInterlockViolated_HH OR
   bAlarm_EmergencyStopTripped_HH THEN
    eCurrentState := 999; (* Transition directly to emergency hold *)
    bEmergencySafetyInterlockTripped := TRUE;
END_IF;

(* --- 6.3: ISA-18.2 Bitfield Word Telemetry Packing --- *)

(* 1. Emergency Safety Trips DWORD (Priority 1) *)
dwAlarms_ISA18_EmergencyTrips := 16#00000000;
IF bAlarm_ProductCollapseRisk_HH   THEN dwAlarms_ISA18_EmergencyTrips := dwAlarms_ISA18_EmergencyTrips OR 16#00000001; END_IF;
IF bAlarm_VacuumLost_HH            THEN dwAlarms_ISA18_EmergencyTrips := dwAlarms_ISA18_EmergencyTrips OR 16#00000002; END_IF;
IF bAlarm_CondenserTempHigh_HH     THEN dwAlarms_ISA18_EmergencyTrips := dwAlarms_ISA18_EmergencyTrips OR 16#00000004; END_IF;
IF bAlarm_SiliconeOilFlow_LL       THEN dwAlarms_ISA18_EmergencyTrips := dwAlarms_ISA18_EmergencyTrips OR 16#00000008; END_IF;
IF bAlarm_ShelfThermalRunaway_HH   THEN dwAlarms_ISA18_EmergencyTrips := dwAlarms_ISA18_EmergencyTrips OR 16#00000010; END_IF;
IF bAlarm_CompressorHead_HH        THEN dwAlarms_ISA18_EmergencyTrips := dwAlarms_ISA18_EmergencyTrips OR 16#00000020; END_IF;
IF bAlarm_HydraulicOilPres_HH      THEN dwAlarms_ISA18_EmergencyTrips := dwAlarms_ISA18_EmergencyTrips OR 16#00000040; END_IF;
IF bAlarm_DoorInterlockViolated_HH THEN dwAlarms_ISA18_EmergencyTrips := dwAlarms_ISA18_EmergencyTrips OR 16#00000080; END_IF;
IF bAlarm_EmergencyStopTripped_HH  THEN dwAlarms_ISA18_EmergencyTrips := dwAlarms_ISA18_EmergencyTrips OR 16#00000100; END_IF;

(* 2. Process Deviation Warnings DWORD (Priority 2) *)
dwAlarms_ISA18_ProcessWarnings := 16#00000000;
IF bAlarm_ProductTempHigh_H        THEN dwAlarms_ISA18_ProcessWarnings := dwAlarms_ISA18_ProcessWarnings OR 16#00000001; END_IF;
IF bAlarm_VacuumHigh_H             THEN dwAlarms_ISA18_ProcessWarnings := dwAlarms_ISA18_ProcessWarnings OR 16#00000002; END_IF;
IF bAlarm_CondenserTempHigh_H      THEN dwAlarms_ISA18_ProcessWarnings := dwAlarms_ISA18_ProcessWarnings OR 16#00000004; END_IF;
IF bAlarm_ShelfSpread_H            THEN dwAlarms_ISA18_ProcessWarnings := dwAlarms_ISA18_ProcessWarnings OR 16#00000008; END_IF;
IF bAlarm_StopperingForce_LL       THEN dwAlarms_ISA18_ProcessWarnings := dwAlarms_ISA18_ProcessWarnings OR 16#00000010; END_IF;
IF bAlarm_SterileN2Supply_L        THEN dwAlarms_ISA18_ProcessWarnings := dwAlarms_ISA18_ProcessWarnings OR 16#00000020; END_IF;
IF bAlarm_SensorTMR_Discrepancy_H  THEN dwAlarms_ISA18_ProcessWarnings := dwAlarms_ISA18_ProcessWarnings OR 16#00000040; END_IF;

(* 3. 2oo3 TMR Sensor Health Bitfield DWORD *)
dwSensorHealth_TMR_Status := 16#00000000;
IF bTMR_Shelf_Fault_A  THEN dwSensorHealth_TMR_Status := dwSensorHealth_TMR_Status OR 16#00000001; END_IF;
IF bTMR_Shelf_Fault_B  THEN dwSensorHealth_TMR_Status := dwSensorHealth_TMR_Status OR 16#00000002; END_IF;
IF bTMR_Shelf_Fault_C  THEN dwSensorHealth_TMR_Status := dwSensorHealth_TMR_Status OR 16#00000004; END_IF;
IF bTMR_Prod_Fault_A   THEN dwSensorHealth_TMR_Status := dwSensorHealth_TMR_Status OR 16#00000008; END_IF;
IF bTMR_Prod_Fault_B   THEN dwSensorHealth_TMR_Status := dwSensorHealth_TMR_Status OR 16#00000010; END_IF;
IF bTMR_Prod_Fault_C   THEN dwSensorHealth_TMR_Status := dwSensorHealth_TMR_Status OR 16#00000020; END_IF;
IF bTMR_CM_Fault_A     THEN dwSensorHealth_TMR_Status := dwSensorHealth_TMR_Status OR 16#00000040; END_IF;
IF bTMR_CM_Fault_B     THEN dwSensorHealth_TMR_Status := dwSensorHealth_TMR_Status OR 16#00000080; END_IF;
IF bTMR_CM_Fault_C     THEN dwSensorHealth_TMR_Status := dwSensorHealth_TMR_Status OR 16#00000100; END_IF;
IF bTMR_Pirani_Fault_A THEN dwSensorHealth_TMR_Status := dwSensorHealth_TMR_Status OR 16#00000200; END_IF;
IF bTMR_Pirani_Fault_B THEN dwSensorHealth_TMR_Status := dwSensorHealth_TMR_Status OR 16#00000400; END_IF;
IF bTMR_Pirani_Fault_C THEN dwSensorHealth_TMR_Status := dwSensorHealth_TMR_Status OR 16#00000800; END_IF;
IF bTMR_Cond_Fault_A   THEN dwSensorHealth_TMR_Status := dwSensorHealth_TMR_Status OR 16#00001000; END_IF;
IF bTMR_Cond_Fault_B   THEN dwSensorHealth_TMR_Status := dwSensorHealth_TMR_Status OR 16#00002000; END_IF;
IF bTMR_Cond_Fault_C   THEN dwSensorHealth_TMR_Status := dwSensorHealth_TMR_Status OR 16#00004000; END_IF;
IF bTMR_Ram_Fault_A    THEN dwSensorHealth_TMR_Status := dwSensorHealth_TMR_Status OR 16#00008000; END_IF;
IF bTMR_Ram_Fault_B    THEN dwSensorHealth_TMR_Status := dwSensorHealth_TMR_Status OR 16#00010000; END_IF;
IF bTMR_Ram_Fault_C    THEN dwSensorHealth_TMR_Status := dwSensorHealth_TMR_Status OR 16#00020000; END_IF;

(* 4. Real-Time Actuator Status Word DWORD *)
dwActuatorStatusWord := 16#00000000;
IF bCmd_MainIsolationMushroomValveOpen  THEN dwActuatorStatusWord := dwActuatorStatusWord OR 16#00000001; END_IF;
IF bCmd_ChamberVentSterileN2ValveOpen   THEN dwActuatorStatusWord := dwActuatorStatusWord OR 16#00000002; END_IF;
IF bCmd_CondenserDefrostSteamValveOpen  THEN dwActuatorStatusWord := dwActuatorStatusWord OR 16#00000004; END_IF;
IF bCmd_CondenserCondensateDrainPumpRun THEN dwActuatorStatusWord := dwActuatorStatusWord OR 16#00000008; END_IF;
IF bCmd_ChamberDoorPneumaticSealInflate THEN dwActuatorStatusWord := dwActuatorStatusWord OR 16#00000010; END_IF;
IF rCmd_ShelfHeaterSCR_DutyPct > 1.0    THEN dwActuatorStatusWord := dwActuatorStatusWord OR 16#00000020; END_IF;
IF rCmd_ScrewCompressorSlideValvePct > 5.0 THEN dwActuatorStatusWord := dwActuatorStatusWord OR 16#00000040; END_IF;
IF rCmd_LN2_BoosterCoolingValvePct > 1.0 THEN dwActuatorStatusWord := dwActuatorStatusWord OR 16#00000080; END_IF;
IF rCmd_RootsVacuumBlowerSpeedPct > 5.0 THEN dwActuatorStatusWord := dwActuatorStatusWord OR 16#00000100; END_IF;
IF rCmd_SterileN2_MicroBleedDosingPct > 1.0 THEN dwActuatorStatusWord := dwActuatorStatusWord OR 16#00000200; END_IF;
IF rCmd_CondenserRefrigExpansionValvePct > 5.0 THEN dwActuatorStatusWord := dwActuatorStatusWord OR 16#00000400; END_IF;
IF rCmd_HydraulicStopperingServoPct > 1.0 THEN dwActuatorStatusWord := dwActuatorStatusWord OR 16#00000800; END_IF;
IF rCmd_NucleationDepressPulseValvePct > 1.0 THEN dwActuatorStatusWord := dwActuatorStatusWord OR 16#00001000; END_IF;

(* 5. Lyophilization Batch Cycle Telemetry DWORD *)
dwBatchCycleTelemetry := 16#00000000;
IF bMasterBatchRunPermissive        THEN dwBatchCycleTelemetry := dwBatchCycleTelemetry OR 16#00000001; END_IF;
IF bLeakRateTestPassed              THEN dwBatchCycleTelemetry := dwBatchCycleTelemetry OR 16#00000002; END_IF;
IF eCurrentState >= 30              THEN dwBatchCycleTelemetry := dwBatchCycleTelemetry OR 16#00000004; END_IF;
IF eCurrentState >= 40              THEN dwBatchCycleTelemetry := dwBatchCycleTelemetry OR 16#00000008; END_IF;
IF (eCurrentState = 60) OR (eCurrentState = 70) THEN dwBatchCycleTelemetry := dwBatchCycleTelemetry OR 16#00000010; END_IF;
IF bPrimaryDryingEndpointDetected   THEN dwBatchCycleTelemetry := dwBatchCycleTelemetry OR 16#00000020; END_IF;
IF bPRT_ActiveInProgress            THEN dwBatchCycleTelemetry := dwBatchCycleTelemetry OR 16#00000040; END_IF;
IF eCurrentState = 80               THEN dwBatchCycleTelemetry := dwBatchCycleTelemetry OR 16#00000080; END_IF;
IF bSecondaryDryingCompleteFlag     THEN dwBatchCycleTelemetry := dwBatchCycleTelemetry OR 16#00000100; END_IF;
IF bStopperingCompleteFlag          THEN dwBatchCycleTelemetry := dwBatchCycleTelemetry OR 16#00000200; END_IF;
IF eCurrentState = 120              THEN dwBatchCycleTelemetry := dwBatchCycleTelemetry OR 16#00000400; END_IF;
IF bBatchCycleSuccessfullyComplete  THEN dwBatchCycleTelemetry := dwBatchCycleTelemetry OR 16#00000800; END_IF;
IF bEmergencySafetyInterlockTripped THEN dwBatchCycleTelemetry := dwBatchCycleTelemetry OR 16#00001000; END_IF;

(* 6. Unified 16-Bit Automation Status Word *)
wAutomationStatusWord := INT_TO_WORD(eCurrentState) AND 16#00FF;
IF bMasterBatchRunPermissive THEN
    wAutomationStatusWord := wAutomationStatusWord OR 16#0100;
END_IF;
IF bBatchCycleSuccessfullyComplete THEN
    wAutomationStatusWord := wAutomationStatusWord OR 16#0200;
END_IF;
IF dwAlarms_ISA18_ProcessWarnings <> 16#00000000 THEN
    wAutomationStatusWord := wAutomationStatusWord OR 16#4000;
END_IF;
IF dwAlarms_ISA18_EmergencyTrips <> 16#00000000 THEN
    wAutomationStatusWord := wAutomationStatusWord OR 16#8000;
END_IF;

END_FUNCTION_BLOCK
"""

print("generate_phase6 loaded.")
