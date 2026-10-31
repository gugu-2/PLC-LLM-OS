# -*- coding: utf-8 -*-

part5_logic3 = """(* ================================================================================================= *)
(* === PHASE 5: SIL 3 MULTI-STAGE FINITE STATE MACHINE (FSM) ARCHITECTURE                        === *)
(* ================================================================================================= *)

(* Master Safety Interlock Check *)
IF NOT bEmergencyStopCircuitOK OR bManualTripEmergencyClamp THEN
    bCriticalSafetyTrip := TRUE;
    bEmergencyClampDeployCmd := TRUE;
    iState := 99; (* Transition Immediately to Emergency Clamp Drop State *)
END_IF;

(* Track State Dwell Time *)
IF iState = iPrevState THEN
    rStateDwellTimer_s := rStateDwellTimer_s + c_rScanTime_Ts;
ELSE
    rStateDwellTimer_s := 0.0;
    rDoorActionTimer_s := 0.0;
    rPalletClampTimer_s := 0.0;
    rCombArmCycleTimer_s := 0.0;
    iPrevState := iState;
END_IF;

CASE iState OF
    0: (* STATE 0: BOOT, HOMING & SAFETY CLAMP ARMED VERIFICATION *)
        bHoistMotorRun := FALSE;
        bHoistMechanicalBrakeRelease := FALSE;
        bShuttleMotorRun := FALSE;
        bShuttleBrakeRelease := FALSE;
        bCombArmsExtendCommand := FALSE;
        bCombArmsRetractCommand := TRUE;
        bPalletLockEngageCommand := TRUE;
        bPalletLockDisengageCommand := FALSE;
        bEmergencyClampDeployCmd := FALSE;
        bSystemInCycle := FALSE;

        (* Verify hydraulic safety wedge clamp pressure is charged and latched *)
        IF (rHydraulicClampPressure_bar >= c_rClampPressure_L_bar) AND bEmergencyWedgeClampLatched AND
           bEmergencyStopCircuitOK AND NOT bCriticalSafetyTrip THEN
            IF bEnableSystem THEN
                iState := 10; (* Transition to Cabin Check-In & Profiling *)
            END_IF;
        END_IF;

    10: (* STATE 10: ENTRY CABIN VEHICLE CHECK-IN & VOLUMETRIC PROFILING *)
        bHoistMotorRun := FALSE;
        bHoistMechanicalBrakeRelease := FALSE;
        bShuttleMotorRun := FALSE;
        bShuttleBrakeRelease := FALSE;
        bCabinShutterDoorOpenCmd := TRUE;
        bCabinShutterDoorCloseCmd := FALSE;
        bSystemInCycle := FALSE;

        (* Vehicle presence detected via platform load cells *)
        IF rVotedVehicleWeight_kg >= c_rMinVehicleMass_kg THEN
            (* Validate vehicle envelope against strict physical silo rack bounds *)
            IF (rVehicleLength_Measured_mm <= c_rMaxVehicleLength_mm) AND
               (rVehicleWidth_Measured_mm <= c_rMaxVehicleWidth_mm) AND
               (rVehicleHeight_Measured_mm <= c_rMaxVehicleHeight_mm) AND
               (rVotedVehicleWeight_kg <= c_rMaxVehicleMass_kg) AND
               bOverhangSensorsClear AND bRoofLuggageClear THEN
                bVehicleProfileAccepted := TRUE;
            ELSE
                bVehicleProfileAccepted := FALSE;
            END_IF;

            (* Once vehicle profile accepted, verify human driver has vacated cabin *)
            IF bVehicleProfileAccepted AND bCabinVacateMotionCleared AND bSafetyCurtainCabinClear THEN
                (* Require 2.0 seconds sustained empty cabin detection *)
                IF rStateDwellTimer_s >= 2.0 THEN
                    bPalletOccupiedWithVehicle := TRUE;
                    iMissionType := 1; (* Store Vehicle Mission *)
                    iState := 20; (* Proceed to Cabin Vacate Interlock & Door Closure *)
                END_IF;
            END_IF;
        ELSIF bExecuteRetrievalCycle THEN
            (* Retrieval dispatch command received for empty carriage hoist run *)
            bPalletOccupiedWithVehicle := FALSE;
            iMissionType := 2; (* Retrieve Vehicle Mission *)
            iState := 20;
        END_IF;

    20: (* STATE 20: CABIN VACATE INTERLOCK & SECURITY SHUTTER CLOSURE *)
        bCabinShutterDoorOpenCmd := FALSE;
        bCabinShutterDoorCloseCmd := TRUE;
        rDoorActionTimer_s := rDoorActionTimer_s + c_rScanTime_Ts;

        (* Safety light curtain must remain unbroken during entire door descent *)
        IF NOT bSafetyCurtainCabinClear THEN
            bCabinShutterDoorCloseCmd := FALSE;
            bCabinShutterDoorOpenCmd := TRUE; (* Re-open immediately upon obstruction *)
            bAlarm_CabinCurtainBreach := TRUE;
        ELSIF bCabinShutterDoorClosed AND bVehicleWheelChocksEngaged THEN
            bCabinShutterDoorCloseCmd := FALSE;
            iState := 30; (* Proceed to Mechanical Pallet Locking *)
        ELSIF rDoorActionTimer_s >= 12.0 THEN
            (* Door closure timeout fault *)
            bCriticalSafetyTrip := TRUE;
            iState := 99;
        END_IF;

    30: (* STATE 30: MECHANICAL PALLET LOCKING & SILO TARGET LATCHING *)
        bPalletLockEngageCommand := TRUE;
        bPalletLockDisengageCommand := FALSE;
        rPalletClampTimer_s := rPalletClampTimer_s + c_rScanTime_Ts;

        IF bPalletLockEngaged_Feedback THEN
            (* Latch target parking coordinates from supervisory WMS *)
            iAssignedStorageLevel := iTargetLevelNumber;
            iAssignedStorageBay := iTargetBayColumn;

            (* Bound target level index between 1 and 15 *)
            IF iAssignedStorageLevel < 1 THEN iAssignedStorageLevel := 1;
            ELSIF iAssignedStorageLevel > 15 THEN iAssignedStorageLevel := 15; END_IF;

            (* Arm Jerk-Limited S-Curve Trajectory Generator for Hoist *)
            rSCurveStartPos_mm := rVotedHoistPosition_mm;
            rSCurveTargetDistance_mm := aFloorElevations_mm[iAssignedStorageLevel];
            rProfileCurrentPos_mm := rSCurveStartPos_mm;
            rProfileCurrentVel_m_s := 0.0;
            rProfileCurrentAccel_m_s2 := 0.0;
            rSCurveElapsedTimer_s := 0.0;
            iSCurvePhase := 1;
            bSCurveProfileActive := TRUE;
            bSCurveProfileCompleted := FALSE;
            bFloorAlignedSubMillimeter := FALSE;
            bSystemInCycle := TRUE;

            iState := 40; (* Proceed to High-Speed Vertical Hoist Motion *)
        ELSIF rPalletClampTimer_s >= 4.0 THEN
            (* Pallet clamping mechanism failed to engage *)
            bCriticalSafetyTrip := TRUE;
            iState := 99;
        END_IF;

    40: (* STATE 40: HIGH-SPEED VERTICAL HOIST S-CURVE ASCENT / DESCENT *)
        bHoistMotorRun := TRUE;
        bHoistMechanicalBrakeRelease := TRUE;
        bShuttleMotorRun := FALSE;
        bShuttleBrakeRelease := FALSE;

        (* Trajectory actively modulated by Phase 3 S-curve profiler and MPC *)
        IF iSCurvePhase = 7 THEN
            (* Trajectory entered terminal sub-millimeter creep approach *)
            iState := 50;
        END_IF;

        (* Continuous motion safety supervision *)
        IF ABS(rVotedHoistVelocity_m_s) > c_rSpeed_HH_m_s THEN
            bAlarm_Speed_HH := TRUE;
            bCriticalSafetyTrip := TRUE;
            bEmergencyClampDeployCmd := TRUE;
            iState := 99;
        END_IF;

    50: (* STATE 50: SUB-MILLIMETER FLOOR LEVELING & SILL PIN DOCKING *)
        bHoistMotorRun := TRUE;
        bHoistMechanicalBrakeRelease := TRUE;

        (* Once sub-millimeter precision achieved (< 0.5 mm for 150 ms) *)
        IF bFloorAlignedSubMillimeter AND bSCurveProfileCompleted THEN
            (* Apply mechanical holding disc brake *)
            bHoistMechanicalBrakeRelease := FALSE;
            bHoistMotorRun := FALSE;

            (* Verify floor leveling tolerance *)
            IF ABS(rHoistFloorLevelingError_mm) <= c_rFloorLevelTolerance_mm THEN
                (* Arm Horizontal Shuttle Motion to Target Bay Column *)
                IF iAssignedStorageBay < 1 THEN iAssignedStorageBay := 1;
                ELSIF iAssignedStorageBay > 24 THEN iAssignedStorageBay := 24; END_IF;

                rShuttleStartPos_mm := rVotedShuttlePosition_mm;
                rShuttleTargetDist_mm := aBayColumnPositions_mm[iAssignedStorageBay];
                rShuttleProfilePos_mm := rShuttleStartPos_mm;
                rShuttleProfileVel_m_s := 0.0;
                bShuttleProfileActive := TRUE;
                bShuttleProfileCompleted := FALSE;

                iState := 60; (* Proceed to Shuttle Aisle Deployment *)
            ELSE
                bAlarm_LevelAlign_HH := TRUE;
                bCriticalSafetyTrip := TRUE;
                iState := 99;
            END_IF;
        END_IF;

    60: (* STATE 60: HORIZONTAL SHUTTLE AISLE TRAVERSE TO TARGET BAY *)
        bHoistMotorRun := FALSE;
        bHoistMechanicalBrakeRelease := FALSE;
        bShuttleMotorRun := TRUE;
        bShuttleBrakeRelease := TRUE;

        IF bShuttleProfileCompleted THEN
            bShuttleMotorRun := FALSE;
            bShuttleBrakeRelease := FALSE;
            rCombArmCycleTimer_s := 0.0;
            iState := 70; (* Proceed to Rack Bay Telescopic Comb Transfer *)
        END_IF;

    70: (* STATE 70: RACK BAY TELESCOPIC COMB TRANSFER SATELLITE ACTION *)
        bHoistMotorRun := FALSE;
        bHoistMechanicalBrakeRelease := FALSE;
        bShuttleMotorRun := FALSE;
        bShuttleBrakeRelease := FALSE;
        rCombArmCycleTimer_s := rCombArmCycleTimer_s + c_rScanTime_Ts;

        IF iMissionType = 1 THEN
            (* Vehicle Storage: Extend arms with vehicle, deposit into rack bay *)
            IF NOT bCombArmsExtended_Feedback AND (rCombArmCycleTimer_s < 4.0) THEN
                bCombArmsExtendCommand := TRUE;
                bCombArmsRetractCommand := FALSE;
            ELSIF bCombArmsExtended_Feedback AND (rCombArmCycleTimer_s < 6.0) THEN
                (* Retract arms leaving vehicle on rack support fingers *)
                bCombArmsExtendCommand := FALSE;
                bCombArmsRetractCommand := TRUE;
            ELSIF bCombArmsRetracted_Feedback THEN
                bCombArmsRetractCommand := FALSE;
                bPalletOccupiedWithVehicle := FALSE;
                iState := 80; (* Retract Shuttle to Carriage *)
            ELSIF rCombArmCycleTimer_s >= 8.0 THEN
                bCriticalSafetyTrip := TRUE;
                iState := 99;
            END_IF;
        ELSE
            (* Vehicle Retrieval: Extend empty arms, lift vehicle from rack, retract *)
            IF NOT bCombArmsExtended_Feedback AND (rCombArmCycleTimer_s < 4.0) THEN
                bCombArmsExtendCommand := TRUE;
                bCombArmsRetractCommand := FALSE;
            ELSIF bCombArmsExtended_Feedback AND (rCombArmCycleTimer_s < 6.0) THEN
                bCombArmsExtendCommand := FALSE;
                bCombArmsRetractCommand := TRUE;
            ELSIF bCombArmsRetracted_Feedback THEN
                bCombArmsRetractCommand := FALSE;
                bPalletOccupiedWithVehicle := TRUE;
                iState := 80;
            ELSIF rCombArmCycleTimer_s >= 8.0 THEN
                bCriticalSafetyTrip := TRUE;
                iState := 99;
            END_IF;
        END_IF;

    80: (* STATE 80: SHUTTLE RETRACTION & MECHANICAL DOCKING TO HOIST BED *)
        bShuttleMotorRun := TRUE;
        bShuttleBrakeRelease := TRUE;
        rShuttleTargetDist_mm := 1800.0; (* Hoist carriage home dock column position *)
        bShuttleProfileActive := TRUE;

        IF bShuttleProfileCompleted THEN
            bShuttleMotorRun := FALSE;
            bShuttleBrakeRelease := FALSE;

            (* Arm Jerk-Limited S-Curve Trajectory for Hoist Return to Ground Level 1 *)
            rSCurveStartPos_mm := rVotedHoistPosition_mm;
            rSCurveTargetDistance_mm := aFloorElevations_mm[1];
            rProfileCurrentPos_mm := rSCurveStartPos_mm;
            rProfileCurrentVel_m_s := 0.0;
            rProfileCurrentAccel_m_s2 := 0.0;
            rSCurveElapsedTimer_s := 0.0;
            iSCurvePhase := 1;
            bSCurveProfileActive := TRUE;
            bSCurveProfileCompleted := FALSE;
            bFloorAlignedSubMillimeter := FALSE;

            iState := 90; (* Proceed to Hoist Return Descent *)
        END_IF;

    90: (* STATE 90: HOIST RETURN DESCENT WITH REGENERATIVE BRAKING *)
        bHoistMotorRun := TRUE;
        bHoistMechanicalBrakeRelease := TRUE;

        (* Active regeneration managed in Phase 3 *)
        IF bFloorAlignedSubMillimeter AND bSCurveProfileCompleted THEN
            bHoistMechanicalBrakeRelease := FALSE;
            bHoistMotorRun := FALSE;
            bSystemInCycle := FALSE;

            IF iMissionType = 2 THEN
                (* Vehicle retrieved to ground cabin - open security door for driver *)
                bCabinShutterDoorOpenCmd := TRUE;
                bPalletLockDisengageCommand := TRUE;
                iState := 10;
            ELSE
                (* Cycle successfully completed, return to Standby *)
                iState := 0;
            END_IF;
        END_IF;

    99: (* STATE 99: CRITICAL SAFETY TRIP / EMERGENCY HYDRAULIC CLAMP DROP *)
        bHoistMotorRun := FALSE;
        bHoistMechanicalBrakeRelease := FALSE; (* De-energize brake coil -> spring apply *)
        bShuttleMotorRun := FALSE;
        bShuttleBrakeRelease := FALSE;
        bCombArmsExtendCommand := FALSE;
        bCombArmsRetractCommand := FALSE;
        bEmergencyClampDeployCmd := TRUE; (* Instantly drop hydraulic safety wedge clamps *)
        bPalletLockEngageCommand := TRUE;
        bCabinShutterDoorOpenCmd := FALSE;
        bCabinShutterDoorCloseCmd := FALSE;
        bSCurveProfileActive := FALSE;
        bShuttleProfileActive := FALSE;
        bSystemInCycle := FALSE;

        (* Manual reset requirement: E-stop healthy + manual reset pulse *)
        IF bEmergencyStopCircuitOK AND bMasterAlarmReset AND NOT bManualTripEmergencyClamp THEN
            bCriticalSafetyTrip := FALSE;
            bEmergencyClampDeployCmd := FALSE;
            bAlarm_Speed_HH := FALSE;
            bAlarm_CableTension_LL := FALSE;
            bAlarm_CableOsc_HH := FALSE;
            bAlarm_LevelAlign_HH := FALSE;
            bAlarm_DCLink_HH := FALSE;
            bAlarm_StatorTemp_HH := FALSE;
            bAlarm_BrakeDiscTemp_HH := FALSE;
            bAlarm_ClampPressure_LL := FALSE;
            bAlarm_LaserSpread_Trip := FALSE;
            bAlarm_EncoderSpread_Trip := FALSE;
            bAlarm_ShuttleSpread_Trip := FALSE;
            bAlarm_LoadCellSpread_Trip := FALSE;
            bAlarm_TractionRopeSlip := FALSE;
            bAlarm_EmergencyClampDropped := FALSE;
            iState := 0; (* Return to State 0 for Homing & Safety Re-Arming *)
        END_IF;

END_CASE;

iOperationalState := iState;

(* ================================================================================================= *)
(* === PHASE 6: ISA-18.2 MULTI-TIERED ALARMS & DIAGNOSTIC WORD PACKING                           === *)
(* ================================================================================================= *)

(* --- 6.1 HOIST SPEED ALARMS (HH, H) --- *)
IF ABS(rVotedHoistVelocity_m_s) >= c_rSpeed_HH_m_s THEN
    bAlarm_Speed_HH := TRUE;
ELSIF ABS(rVotedHoistVelocity_m_s) <= (c_rSpeed_HH_m_s - c_rSpeed_Deadband_m_s) THEN
    bAlarm_Speed_HH := FALSE;
END_IF;

IF ABS(rVotedHoistVelocity_m_s) >= c_rSpeed_H_m_s THEN
    bAlarm_Speed_H := TRUE;
ELSIF ABS(rVotedHoistVelocity_m_s) <= (c_rSpeed_H_m_s - c_rSpeed_Deadband_m_s) THEN
    bAlarm_Speed_H := FALSE;
END_IF;

(* --- 6.2 CABLE TENSION ALARMS (HH, L, LL) --- *)
IF rHoistCableTension_kN <= c_rCableTension_LL_kN THEN
    bAlarm_CableTension_LL := TRUE;
ELSIF rHoistCableTension_kN >= (c_rCableTension_LL_kN + c_rCableTension_Deadband_kN) THEN
    bAlarm_CableTension_LL := FALSE;
END_IF;

IF rHoistCableTension_kN <= c_rCableTension_L_kN THEN
    bAlarm_CableTension_L := TRUE;
ELSIF rHoistCableTension_kN >= (c_rCableTension_L_kN + c_rCableTension_Deadband_kN) THEN
    bAlarm_CableTension_L := FALSE;
END_IF;

IF rHoistCableTension_kN >= c_rCableTension_HH_kN THEN
    bAlarm_CableTension_HH := TRUE;
ELSIF rHoistCableTension_kN <= (c_rCableTension_HH_kN - c_rCableTension_Deadband_kN) THEN
    bAlarm_CableTension_HH := FALSE;
END_IF;

(* --- 6.3 CABLE LONGITUDINAL OSCILLATION ALARMS (HH, H) --- *)
IF rCableVibrationAmplitude_mm >= c_rCableOsc_HH_mm THEN
    bAlarm_CableOsc_HH := TRUE;
ELSIF rCableVibrationAmplitude_mm <= (c_rCableOsc_HH_mm - c_rCableOsc_Deadband_mm) THEN
    bAlarm_CableOsc_HH := FALSE;
END_IF;

IF rCableVibrationAmplitude_mm >= c_rCableOsc_H_mm THEN
    bAlarm_CableOsc_H := TRUE;
ELSIF rCableVibrationAmplitude_mm <= (c_rCableOsc_H_mm - c_rCableOsc_Deadband_mm) THEN
    bAlarm_CableOsc_H := FALSE;
END_IF;

(* --- 6.4 SUB-MILLIMETER LEVELING ALIGNMENT ALARMS (HH, H) --- *)
IF ABS(rHoistFloorLevelingError_mm) >= c_rLevelAlign_HH_mm THEN
    bAlarm_LevelAlign_HH := TRUE;
ELSIF ABS(rHoistFloorLevelingError_mm) <= (c_rLevelAlign_HH_mm - c_rLevelAlign_Deadband_mm) THEN
    bAlarm_LevelAlign_HH := FALSE;
END_IF;

IF ABS(rHoistFloorLevelingError_mm) >= c_rLevelAlign_H_mm THEN
    bAlarm_LevelAlign_H := TRUE;
ELSIF ABS(rHoistFloorLevelingError_mm) <= (c_rLevelAlign_H_mm - c_rLevelAlign_Deadband_mm) THEN
    bAlarm_LevelAlign_H := FALSE;
END_IF;

(* --- 6.5 DC LINK VOLTAGE ALARMS (HH, H, L, LL) --- *)
IF rDCLinkVoltage_V >= c_rDCLink_HH_V THEN
    bAlarm_DCLink_HH := TRUE;
ELSIF rDCLinkVoltage_V <= (c_rDCLink_HH_V - c_rDCLink_Deadband_V) THEN
    bAlarm_DCLink_HH := FALSE;
END_IF;

IF rDCLinkVoltage_V >= c_rDCLink_H_V THEN
    bAlarm_DCLink_H := TRUE;
ELSIF rDCLinkVoltage_V <= (c_rDCLink_H_V - c_rDCLink_Deadband_V) THEN
    bAlarm_DCLink_H := FALSE;
END_IF;

IF rDCLinkVoltage_V <= c_rDCLink_L_V THEN
    bAlarm_DCLink_L := TRUE;
ELSIF rDCLinkVoltage_V >= (c_rDCLink_L_V + c_rDCLink_Deadband_V) THEN
    bAlarm_DCLink_L := FALSE;
END_IF;

IF rDCLinkVoltage_V <= c_rDCLink_LL_V THEN
    bAlarm_DCLink_LL := TRUE;
ELSIF rDCLinkVoltage_V >= (c_rDCLink_LL_V + c_rDCLink_Deadband_V) THEN
    bAlarm_DCLink_LL := FALSE;
END_IF;

(* --- 6.6 STATOR & BRAKE DISC THERMAL ALARMS (HH, H) --- *)
IF rSimStatorTemp_degC >= c_rStatorTemp_HH_degC THEN
    bAlarm_StatorTemp_HH := TRUE;
ELSIF rSimStatorTemp_degC <= (c_rStatorTemp_HH_degC - c_rTemp_Deadband_degC) THEN
    bAlarm_StatorTemp_HH := FALSE;
END_IF;

IF rSimStatorTemp_degC >= c_rStatorTemp_H_degC THEN
    bAlarm_StatorTemp_H := TRUE;
ELSIF rSimStatorTemp_degC <= (c_rStatorTemp_H_degC - c_rTemp_Deadband_degC) THEN
    bAlarm_StatorTemp_H := FALSE;
END_IF;

IF rSimBrakeTemp_degC >= c_rBrakeDiscTemp_HH_degC THEN
    bAlarm_BrakeDiscTemp_HH := TRUE;
ELSIF rSimBrakeTemp_degC <= (c_rBrakeDiscTemp_HH_degC - c_rTemp_Deadband_degC) THEN
    bAlarm_BrakeDiscTemp_HH := FALSE;
END_IF;

IF rSimBrakeTemp_degC >= c_rBrakeDiscTemp_H_degC THEN
    bAlarm_BrakeDiscTemp_H := TRUE;
ELSIF rSimBrakeTemp_degC <= (c_rBrakeDiscTemp_H_degC - c_rTemp_Deadband_degC) THEN
    bAlarm_BrakeDiscTemp_H := FALSE;
END_IF;

(* --- 6.7 HYDRAULIC CLAMP PRESSURE ALARMS (L, LL) --- *)
IF rHydraulicClampPressure_bar <= c_rClampPressure_LL_bar THEN
    bAlarm_ClampPressure_LL := TRUE;
ELSIF rHydraulicClampPressure_bar >= (c_rClampPressure_LL_bar + c_rClampPressure_Deadband_bar) THEN
    bAlarm_ClampPressure_LL := FALSE;
END_IF;

IF rHydraulicClampPressure_bar <= c_rClampPressure_L_bar THEN
    bAlarm_ClampPressure_L := TRUE;
ELSIF rHydraulicClampPressure_bar >= (c_rClampPressure_L_bar + c_rClampPressure_Deadband_bar) THEN
    bAlarm_ClampPressure_L := FALSE;
END_IF;

(* --- 6.8 VEHICLE MASS & DIMENSION ALARMS --- *)
IF rVotedVehicleWeight_kg >= c_rWeight_HH_kg THEN
    bAlarm_Weight_HH := TRUE;
ELSIF rVotedVehicleWeight_kg <= (c_rWeight_HH_kg - c_rWeight_Deadband_kg) THEN
    bAlarm_Weight_HH := FALSE;
END_IF;

IF rVehicleLength_Measured_mm > c_rMaxVehicleLength_mm THEN
    bAlarm_VehicleLength_HH := TRUE;
ELSE
    bAlarm_VehicleLength_HH := FALSE;
END_IF;

IF rVehicleWidth_Measured_mm > c_rMaxVehicleWidth_mm THEN
    bAlarm_VehicleWidth_HH := TRUE;
ELSE
    bAlarm_VehicleWidth_HH := FALSE;
END_IF;

IF rVehicleHeight_Measured_mm > c_rMaxVehicleHeight_mm THEN
    bAlarm_VehicleHeight_HH := TRUE;
ELSE
    bAlarm_VehicleHeight_HH := FALSE;
END_IF;

IF NOT bOverhangSensorsClear OR NOT bRoofLuggageClear THEN
    bAlarm_OverhangObstruction := TRUE;
ELSE
    bAlarm_OverhangObstruction := FALSE;
END_IF;

(* --- 6.9 EMERGENCY CLAMP DROP TRIP EVALUATION --- *)
IF bAlarm_Speed_HH OR bAlarm_CableTension_LL OR bAlarm_CableOsc_HH OR
   bAlarm_LevelAlign_HH OR bAlarm_DCLink_HH OR bAlarm_StatorTemp_HH OR
   bAlarm_BrakeDiscTemp_HH OR bAlarm_ClampPressure_LL OR
   bAlarm_LaserSpread_Trip OR bAlarm_EncoderSpread_Trip OR
   bEmergencyClampDeployCmd THEN
    bCriticalSafetyTrip := TRUE;
    bAlarm_EmergencyClampDropped := TRUE;
    iState := 99;
END_IF;

(* Evaluate System Safety Permissives Healthy Status *)
bSafetyInterlocksSatisfied := NOT bCriticalSafetyTrip AND bEmergencyStopCircuitOK AND
                              bSafetyCurtainCabinClear AND (rHydraulicClampPressure_bar >= c_rClampPressure_L_bar);

(* --- 6.10 32-BIT SCADA TELEMETRY & DIAGNOSTIC WORD BITWISE PACKING --- *)
(* Word 1: System Status Word *)
dwSystemStatusWord := 16#00000000;
IF bEnableSystem THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00000001; END_IF;
IF bHoistMotorRun THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00000002; END_IF;
IF bHoistMechanicalBrakeRelease THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00000004; END_IF;
IF bShuttleMotorRun THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00000008; END_IF;
IF bShuttleBrakeRelease THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00000010; END_IF;
IF bCombArmsExtended_Feedback THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00000020; END_IF;
IF bCombArmsRetracted_Feedback THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00000040; END_IF;
IF bPalletLockEngaged_Feedback THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00000080; END_IF;
IF bCabinShutterDoorClosed THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00000100; END_IF;
IF bCabinShutterDoorOpened THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00000200; END_IF;
IF bFloorAlignedSubMillimeter THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00000400; END_IF;
IF bSystemInCycle THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00000800; END_IF;
IF bPalletOccupiedWithVehicle THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00001000; END_IF;
IF bSCurveProfileActive THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00002000; END_IF;
IF bShuttleProfileActive THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00004000; END_IF;
IF bActiveFrontEndRegenReady THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00008000; END_IF;
IF bRegenerativeBrakeChopperFire THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00010000; END_IF;
IF bSafetyInterlocksSatisfied THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00020000; END_IF;
IF bDegradedSensorWarning THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00040000; END_IF;
IF bCriticalSafetyTrip THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00080000; END_IF;

(* Word 2: ISA-18.2 Priority 1 Safety Alarm Word *)
dwAlarmWord_Safety := 16#00000000;
IF NOT bEmergencyStopCircuitOK THEN dwAlarmWord_Safety := dwAlarmWord_Safety OR 16#00000001; END_IF;
IF bAlarm_Speed_HH THEN dwAlarmWord_Safety := dwAlarmWord_Safety OR 16#00000002; END_IF;
IF bAlarm_CableTension_LL THEN dwAlarmWord_Safety := dwAlarmWord_Safety OR 16#00000004; END_IF;
IF bAlarm_CableTension_HH THEN dwAlarmWord_Safety := dwAlarmWord_Safety OR 16#00000008; END_IF;
IF bAlarm_ClampPressure_LL THEN dwAlarmWord_Safety := dwAlarmWord_Safety OR 16#00000010; END_IF;
IF bAlarm_Weight_HH THEN dwAlarmWord_Safety := dwAlarmWord_Safety OR 16#00000020; END_IF;
IF bAlarm_VehicleLength_HH THEN dwAlarmWord_Safety := dwAlarmWord_Safety OR 16#00000040; END_IF;
IF bAlarm_VehicleWidth_HH THEN dwAlarmWord_Safety := dwAlarmWord_Safety OR 16#00000080; END_IF;
IF bAlarm_VehicleHeight_HH THEN dwAlarmWord_Safety := dwAlarmWord_Safety OR 16#00000100; END_IF;
IF bAlarm_OverhangObstruction THEN dwAlarmWord_Safety := dwAlarmWord_Safety OR 16#00000200; END_IF;
IF bAlarm_CabinCurtainBreach THEN dwAlarmWord_Safety := dwAlarmWord_Safety OR 16#00000400; END_IF;
IF bAlarm_LaserSpread_Trip THEN dwAlarmWord_Safety := dwAlarmWord_Safety OR 16#00000800; END_IF;
IF bAlarm_EncoderSpread_Trip THEN dwAlarmWord_Safety := dwAlarmWord_Safety OR 16#00001000; END_IF;
IF bAlarm_ShuttleSpread_Trip THEN dwAlarmWord_Safety := dwAlarmWord_Safety OR 16#00002000; END_IF;
IF bAlarm_LoadCellSpread_Trip THEN dwAlarmWord_Safety := dwAlarmWord_Safety OR 16#00004000; END_IF;
IF bAlarm_EmergencyClampDropped THEN dwAlarmWord_Safety := dwAlarmWord_Safety OR 16#00008000; END_IF;

(* Word 3: ISA-18.2 Priority 2 Process & Electrical Alarm Word *)
dwAlarmWord_Process := 16#00000000;
IF bAlarm_Speed_H THEN dwAlarmWord_Process := dwAlarmWord_Process OR 16#00000001; END_IF;
IF bAlarm_CableTension_L THEN dwAlarmWord_Process := dwAlarmWord_Process OR 16#00000002; END_IF;
IF bAlarm_CableOsc_HH THEN dwAlarmWord_Process := dwAlarmWord_Process OR 16#00000004; END_IF;
IF bAlarm_CableOsc_H THEN dwAlarmWord_Process := dwAlarmWord_Process OR 16#00000008; END_IF;
IF bAlarm_LevelAlign_HH THEN dwAlarmWord_Process := dwAlarmWord_Process OR 16#00000010; END_IF;
IF bAlarm_LevelAlign_H THEN dwAlarmWord_Process := dwAlarmWord_Process OR 16#00000020; END_IF;
IF bAlarm_DCLink_HH THEN dwAlarmWord_Process := dwAlarmWord_Process OR 16#00000040; END_IF;
IF bAlarm_DCLink_H THEN dwAlarmWord_Process := dwAlarmWord_Process OR 16#00000080; END_IF;
IF bAlarm_DCLink_L THEN dwAlarmWord_Process := dwAlarmWord_Process OR 16#00000100; END_IF;
IF bAlarm_DCLink_LL THEN dwAlarmWord_Process := dwAlarmWord_Process OR 16#00000200; END_IF;
IF bAlarm_StatorTemp_HH THEN dwAlarmWord_Process := dwAlarmWord_Process OR 16#00000400; END_IF;
IF bAlarm_StatorTemp_H THEN dwAlarmWord_Process := dwAlarmWord_Process OR 16#00000800; END_IF;
IF bAlarm_BrakeDiscTemp_HH THEN dwAlarmWord_Process := dwAlarmWord_Process OR 16#00001000; END_IF;
IF bAlarm_BrakeDiscTemp_H THEN dwAlarmWord_Process := dwAlarmWord_Process OR 16#00002000; END_IF;
IF bAlarm_ClampPressure_L THEN dwAlarmWord_Process := dwAlarmWord_Process OR 16#00004000; END_IF;
IF bAlarm_TractionRopeSlip THEN dwAlarmWord_Process := dwAlarmWord_Process OR 16#00008000; END_IF;

(* Word 4: Sensor Redundancy & MPC Diagnostic Word *)
dwDiagnosticsWord := 16#00000000;
IF bHoistLaser_Degraded THEN dwDiagnosticsWord := dwDiagnosticsWord OR 16#00000001; END_IF;
IF bHoistLaser_Fault THEN dwDiagnosticsWord := dwDiagnosticsWord OR 16#00000002; END_IF;
IF bHoistEncoder_Degraded THEN dwDiagnosticsWord := dwDiagnosticsWord OR 16#00000004; END_IF;
IF bHoistEncoder_Fault THEN dwDiagnosticsWord := dwDiagnosticsWord OR 16#00000008; END_IF;
IF bShuttleLaser_Degraded THEN dwDiagnosticsWord := dwDiagnosticsWord OR 16#00000010; END_IF;
IF bShuttleLaser_Fault THEN dwDiagnosticsWord := dwDiagnosticsWord OR 16#00000020; END_IF;
IF bLoadCell_Degraded THEN dwDiagnosticsWord := dwDiagnosticsWord OR 16#00000040; END_IF;
IF bLoadCell_Fault THEN dwDiagnosticsWord := dwDiagnosticsWord OR 16#00000080; END_IF;
IF bTractionRopeSlipWarning THEN dwDiagnosticsWord := dwDiagnosticsWord OR 16#00000100; END_IF;
IF ABS(x1_PosDev) > 5.0 THEN dwDiagnosticsWord := dwDiagnosticsWord OR 16#00000200; END_IF;
IF ABS(x3_CableStretchDev) > 10.0 THEN dwDiagnosticsWord := dwDiagnosticsWord OR 16#00000400; END_IF;
IF ABS(x8_DCLinkDev) > 50.0 THEN dwDiagnosticsWord := dwDiagnosticsWord OR 16#00000800; END_IF;

END_FUNCTION_BLOCK
"""
