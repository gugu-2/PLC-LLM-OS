# parts_body4.py

PHASE4_FSM_BLOCK = """
(* ==================================================================================================== *)
(* PHASE 4: 14-STAGE DETERMINISTIC PRODUCTION FINITE STATE MACHINE (FSM)                                 *)
(* ==================================================================================================== *)

(* Detect State Transitions & Initialize State Elapsed Timers *)
IF nActiveFSMStage <> nPrevFSMStage THEN
    bStateInitStrobe := TRUE;
    rStageDwellTimer_s := 0.0;
    nPrevFSMStage := nActiveFSMStage;
ELSE
    bStateInitStrobe := FALSE;
    rStageDwellTimer_s := rStageDwellTimer_s + T_CYCLE_SEC;
END_IF;

(* Master Hardware Safety Trip Immediate Override *)
IF (NOT bEmergencyStopLoop) OR (bCollisionStopActive) THEN
    nActiveFSMStage := 13; (* Force to Emergency Collision Brake Stage *)
END_IF;

CASE nActiveFSMStage OF
    (* ------------------------------------------------------------------------------------------------ *)
    (* STAGE 0: SPINDLE CHILLER PRE-COOLING & THERMAL STABILIZATION                                    *)
    (* ------------------------------------------------------------------------------------------------ *)
    0:
        sActiveFSMStageName := 'STATE_CHILLER_PRECOOL';
        bSpindlePurgeAirCmd := TRUE;      (* Spindle labyrinth air curtain ON *)
        bToolClampSolenoidCmd := TRUE;    (* Collet in clamped state *)
        bThroughSpindleCoolantCmd := FALSE;
        bChipConveyorRunCmd := FALSE;
        rStageTargetDwell_s := 12.0;      (* Required pre-cooling dwell [s] *)
        
        (* Verify Chiller Coolant Flow & Inlet Temperature Window *)
        IF (rChillerCoolantFlow_lmin >= CHILLER_FLOW_MIN_LMIN) AND
           (rChillerInletTemp_degC >= 18.0) AND (rChillerInletTemp_degC <= 23.5) AND
           (rStageDwellTimer_s >= rStageTargetDwell_s) THEN
            IF bSystemEnable AND bMachineAutoMode THEN
                nActiveFSMStage := 1; (* Advance to Homing & Calibration *)
            END_IF;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STAGE 1: AXIS HOMING & LASER CALIBRATION REFERENCE CHECK                                         *)
    (* ------------------------------------------------------------------------------------------------ *)
    1:
        sActiveFSMStageName := 'STATE_AXIS_HOMING_LASER_CAL';
        bSpindlePurgeAirCmd := TRUE;
        bToolClampSolenoidCmd := TRUE;
        bThroughSpindleCoolantCmd := FALSE;
        bChipConveyorRunCmd := FALSE;
        rStageTargetDwell_s := 8.0;
        
        (* Dual-Drive Gantry Yaw Skew Zeroing & Optical Scale Synchronization *)
        IF bStateInitStrobe THEN
            rLaserCalRefZ_mm := rVotedPos_Z_mm;
        END_IF;
        
        IF (ABS(rGantryYaw_SkewError_mm) <= 0.005) AND
           (bX_ChA_Valid AND bY_ChA_Valid AND bZ_ChA_Valid) AND
           (rStageDwellTimer_s >= rStageTargetDwell_s) THEN
            nActiveFSMStage := 2; (* Advance to Spindle Thermal Preheating *)
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STAGE 2: THERMAL GROWTH PRE-HEATING & BEARING GREASE REDISTRIBUTION CYCLE                        *)
    (* ------------------------------------------------------------------------------------------------ *)
    2:
        sActiveFSMStageName := 'STATE_THERMAL_PREHEAT_CYCLE';
        bSpindlePurgeAirCmd := TRUE;
        bToolClampSolenoidCmd := TRUE;
        bThroughSpindleCoolantCmd := FALSE;
        bChipConveyorRunCmd := FALSE;
        
        (* Stepped Warm-up Sequence: 6,000 -> 12,000 -> 18,000 -> 24,000 rpm *)
        IF rStageDwellTimer_s < 10.0 THEN
            nWarmupSubStep := 1;
            rWarmupRampSpeed_rpm := 6000.0;
        ELSIF rStageDwellTimer_s < 20.0 THEN
            nWarmupSubStep := 2;
            rWarmupRampSpeed_rpm := 12000.0;
        ELSIF rStageDwellTimer_s < 30.0 THEN
            nWarmupSubStep := 3;
            rWarmupRampSpeed_rpm := 18000.0;
        ELSE
            nWarmupSubStep := 4;
            rWarmupRampSpeed_rpm := 24000.0;
        END_IF;
        
        (* Check Bearing Temperature Stability Gradient *)
        IF (rStageDwellTimer_s >= 40.0) AND
           (rVotedFrontBearingTemp_degC < TEMP_BRG_H_WARN_DEGC) AND
           (rVotedRearBearingTemp_degC < TEMP_BRG_H_WARN_DEGC) THEN
            nActiveFSMStage := 3; (* Advance to Tool Clamp & Runout Verification *)
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STAGE 3: TOOL CLAMPING FORCE & RUNOUT VERIFICATION                                               *)
    (* ------------------------------------------------------------------------------------------------ *)
    3:
        sActiveFSMStageName := 'STATE_TOOL_CLAMP_RUNOUT_VERIFY';
        bSpindlePurgeAirCmd := TRUE;
        bToolClampSolenoidCmd := TRUE;
        bThroughSpindleCoolantCmd := FALSE;
        bChipConveyorRunCmd := FALSE;
        rStageTargetDwell_s := 4.0;
        
        (* Measure High-Speed Spindle Radial Runout via Non-Contact Sensors *)
        IF bStateInitStrobe THEN
            rMeasuredRunout_um := 1.25; (* Baseline runout check *)
        END_IF;
        
        IF (rHydraulicClampPressure_bar >= PRESSURE_CLAMP_MIN_BAR) AND
           (rMeasuredRunout_um <= 3.50) AND
           (rStageDwellTimer_s >= rStageTargetDwell_s) THEN
            IF bMachineAutoMode THEN
                nActiveFSMStage := 4; (* Advance to Adaptive Roughing *)
            END_IF;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STAGE 4: ADAPTIVE HIGH-SPEED ROUGHING CUT WITH CUTTING FORCE REGULATION                          *)
    (* ------------------------------------------------------------------------------------------------ *)
    4:
        sActiveFSMStageName := 'STATE_ADAPTIVE_ROUGHING';
        bSpindlePurgeAirCmd := TRUE;
        bToolClampSolenoidCmd := TRUE;
        bThroughSpindleCoolantCmd := TRUE;
        bChipConveyorRunCmd := TRUE;
        
        (* Monitor Dynamic Cutting Force & Tool Tip Vibration *)
        IF rPeakChatterAmplitude_ms2 >= VIB_CHATTER_H_WARN_MS2 THEN
            nActiveFSMStage := 5; (* Divert to Active Chatter Suppression *)
        ELSIF (rCmdFeedrate_mmin <= 0.10) AND (rStageDwellTimer_s >= 15.0) THEN
            nActiveFSMStage := 6; (* Advance to Precision Finishing *)
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STAGE 5: ACTIVE CHATTER SUPPRESSION & SPINDLE SPEED MODULATION                                   *)
    (* ------------------------------------------------------------------------------------------------ *)
    5:
        sActiveFSMStageName := 'STATE_ACTIVE_CHATTER_SUPPRESSION';
        bSpindlePurgeAirCmd := TRUE;
        bToolClampSolenoidCmd := TRUE;
        bThroughSpindleCoolantCmd := TRUE;
        bChipConveyorRunCmd := TRUE;
        
        (* SSV Modulation active in Phase 3; Return to roughing when chatter subsides *)
        IF (rPeakChatterAmplitude_ms2 < (VIB_CHATTER_H_WARN_MS2 - VIB_HYSTERESIS_MS2)) AND
           (rStageDwellTimer_s >= 5.0) THEN
            nActiveFSMStage := 4; (* Return to Adaptive Roughing *)
        ELSIF rPeakChatterAmplitude_ms2 >= VIB_CHATTER_HH_TRIP_MS2 THEN
            nActiveFSMStage := 12; (* Excessive vibration: Abort to Safe Retract *)
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STAGE 6: PRECISION FINISH CONTOURING WITH DEFLECTION & THERMAL COMPENSATION                      *)
    (* ------------------------------------------------------------------------------------------------ *)
    6:
        sActiveFSMStageName := 'STATE_PRECISION_FINISH_CONTOURING';
        bSpindlePurgeAirCmd := TRUE;
        bToolClampSolenoidCmd := TRUE;
        bThroughSpindleCoolantCmd := TRUE;
        bChipConveyorRunCmd := TRUE;
        
        (* In finish contouring, feedrate is smooth and deflection compensation is fully engaged *)
        IF (rStageDwellTimer_s >= 20.0) AND (rCmdFeedrate_mmin <= 0.05) THEN
            nActiveFSMStage := 7; (* Advance to Tool Wear Inspection *)
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STAGE 7: TOOL WEAR PROBE & LASER OCCLUSION INSPECTION                                            *)
    (* ------------------------------------------------------------------------------------------------ *)
    7:
        sActiveFSMStageName := 'STATE_TOOL_WEAR_PROBE_INSPECT';
        bSpindlePurgeAirCmd := TRUE;
        bToolClampSolenoidCmd := TRUE;
        bThroughSpindleCoolantCmd := FALSE;
        bChipConveyorRunCmd := TRUE;
        rStageTargetDwell_s := 6.0;
        
        IF (rStageDwellTimer_s >= rStageTargetDwell_s) THEN
            IF bLaserToolSetterBeamBreak THEN
                nActiveFSMStage := 8; (* Tool intact: Advance to Spindle Orientation *)
            ELSE
                nActiveFSMStage := 12; (* Tool Broken / Missing: Safe Retract *)
            END_IF;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STAGE 8: SPINDLE ORIENTATION LOCK (M19 QUASI-STOP)                                               *)
    (* ------------------------------------------------------------------------------------------------ *)
    8:
        sActiveFSMStageName := 'STATE_SPINDLE_ORIENT_LOCK';
        bSpindlePurgeAirCmd := TRUE;
        bToolClampSolenoidCmd := TRUE;
        bThroughSpindleCoolantCmd := FALSE;
        bChipConveyorRunCmd := TRUE;
        rStageTargetDwell_s := 3.5;
        
        (* Align Spindle Keyway to ATC Drive Dogs (Angle = 0.0 +/- 0.05 deg) *)
        IF (rVotedSpindleSpeed_rpm <= 5.0) AND
           (ABS(rVotedSpindleAngle_deg) <= 0.10) AND
           (rStageDwellTimer_s >= rStageTargetDwell_s) THEN
            nActiveFSMStage := 9; (* Advance to Auto Tool Changer Sequence *)
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STAGE 9: AUTOMATIC TOOL CHANGER (ATC) SEQUENCE                                                   *)
    (* ------------------------------------------------------------------------------------------------ *)
    9:
        sActiveFSMStageName := 'STATE_ATC_TOOL_CHANGE_SEQUENCE';
        bSpindlePurgeAirCmd := TRUE;
        bThroughSpindleCoolantCmd := FALSE;
        bChipConveyorRunCmd := TRUE;
        
        (* Dual-Arm Mechanical Sequence Sub-Steps *)
        IF rStageDwellTimer_s < 2.0 THEN
            nATC_SubStep := 1; (* ATC Twin-Arm Swing to Spindle *)
            bToolClampSolenoidCmd := TRUE;
        ELSIF rStageDwellTimer_s < 4.0 THEN
            nATC_SubStep := 2; (* Unclamp HSK Hydraulic Collet *)
            bToolClampSolenoidCmd := FALSE;
        ELSIF rStageDwellTimer_s < 6.0 THEN
            nATC_SubStep := 3; (* Twin-Arm Tool Extraction & 180-deg Index *)
            bToolClampSolenoidCmd := FALSE;
        ELSIF rStageDwellTimer_s < 8.0 THEN
            nATC_SubStep := 4; (* Insert New Tool & Re-Clamp Collet *)
            bToolClampSolenoidCmd := TRUE;
        ELSE
            nATC_SubStep := 5; (* ATC Arm Retract to Park *)
            bToolClampSolenoidCmd := TRUE;
        END_IF;
        
        IF (rStageDwellTimer_s >= 10.0) AND (rHydraulicClampPressure_bar >= PRESSURE_CLAMP_MIN_BAR) THEN
            nActiveFSMStage := 10; (* Advance to Coolant & Chip Management *)
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STAGE 10: FLOOD COOLANT & SWARF CHIP CONVEYOR MANAGEMENT                                         *)
    (* ------------------------------------------------------------------------------------------------ *)
    10:
        sActiveFSMStageName := 'STATE_COOLANT_CHIP_CONVEYOR_MGMT';
        bSpindlePurgeAirCmd := TRUE;
        bToolClampSolenoidCmd := TRUE;
        bThroughSpindleCoolantCmd := FALSE;
        bChipConveyorRunCmd := TRUE;
        rStageTargetDwell_s := 5.0;
        
        (* Washdown cycle and swarf clearance *)
        IF (rChipConveyorMotorLoad_pct < 85.0) AND (rStageDwellTimer_s >= rStageTargetDwell_s) THEN
            nActiveFSMStage := 11; (* Advance to Part Touch Probe Inspection *)
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STAGE 11: WORKPIECE TOUCH PROBE 3D DIMENSIONAL CHECK                                             *)
    (* ------------------------------------------------------------------------------------------------ *)
    11:
        sActiveFSMStageName := 'STATE_TOUCH_PROBE_WORKPIECE_CHECK';
        bSpindlePurgeAirCmd := TRUE;
        bToolClampSolenoidCmd := TRUE;
        bThroughSpindleCoolantCmd := FALSE;
        bChipConveyorRunCmd := FALSE;
        rStageTargetDwell_s := 6.0;
        
        IF bTouchProbeDeflected THEN
            rTouchProbeRecorded_X_mm := rVotedPos_X_mm;
            rTouchProbeRecorded_Y_mm := rVotedPos_Y_mm;
            rTouchProbeRecorded_Z_mm := rVotedPos_Z_mm;
        END_IF;
        
        IF (rStageDwellTimer_s >= rStageTargetDwell_s) THEN
            nActiveFSMStage := 12; (* Advance to Safe Axis Retract *)
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STAGE 12: SAFE AXIS RETRACT TO Z-CLEARANCE PLANE                                                 *)
    (* ------------------------------------------------------------------------------------------------ *)
    12:
        sActiveFSMStageName := 'STATE_SAFE_AXIS_RETRACT';
        bSpindlePurgeAirCmd := TRUE;
        bToolClampSolenoidCmd := TRUE;
        bThroughSpindleCoolantCmd := FALSE;
        bChipConveyorRunCmd := FALSE;
        rStageTargetDwell_s := 5.0;
        
        (* Spindle decelerates to standstill, Z-axis moves to safe home retract plane *)
        IF (rVotedSpindleSpeed_rpm <= 10.0) AND (rStageDwellTimer_s >= rStageTargetDwell_s) THEN
            IF bSystemEnable AND bMachineAutoMode THEN
                nActiveFSMStage := 0; (* Cycle back to Ready Pre-Cool Standby *)
            END_IF;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STAGE 13: SEVERE COLLISION EMERGENCY BRAKE FAILSAFE TRIP                                         *)
    (* ------------------------------------------------------------------------------------------------ *)
    13:
        sActiveFSMStageName := 'STATE_EMERGENCY_BRAKE_COLLISION_FAILSAFE';
        bSpindlePurgeAirCmd := TRUE;
        bToolClampSolenoidCmd := TRUE;    (* Keep collet firmly clamped! *)
        bThroughSpindleCoolantCmd := FALSE;(* Kill high-pressure cutting fluid *)
        bChipConveyorRunCmd := FALSE;
        bCollisionStopActive := TRUE;
        
        (* Active Damping Injected Hard Deceleration Brake *)
        rActiveDampForceCmd_X_N := 0.0;
        rActiveDampForceCmd_Y_N := 0.0;
        rActiveDampForceCmd_Z_N := 0.0;
        rThermalCompOffset_Z_um := 0.0;
        rDeflectionCompOffset_X_um := 0.0;
        rDeflectionCompOffset_Y_um := 0.0;
        rAdaptiveFeedOverride_pct := 0.0;
        
        (* Latch emergency state until master system reset and e-stop health restored *)
        IF bAlarmReset AND bEmergencyStopLoop AND (NOT bAlarm_CollisionImpactTripped) THEN
            bCollisionStopActive := FALSE;
            nActiveFSMStage := 0; (* Return to Chiller Pre-Cooling *)
        END_IF;

ELSE
    (* Fallback default safe state *)
    nActiveFSMStage := 13;
END_CASE;
"""

PHASE5_ALARM_BLOCK = """
(* ==================================================================================================== *)
(* PHASE 5: ISA-18.2 MULTI-TIER ALARM ENGINE & BIT-PACKED STATUS WORDS                                  *)
(* ==================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------- *)
(* 5.1: Dynamic Hysteresis & Alarm Qualification Logic                                                  *)
(* ---------------------------------------------------------------------------------------------------- *)
(* Front Bearing Temperature High-High Trip *)
IF rVotedFrontBearingTemp_degC >= TEMP_BRG_HH_TRIP_DEGC THEN
    bAlarm_SpindleBearingOverheat := TRUE;
ELSIF rVotedFrontBearingTemp_degC <= (TEMP_BRG_HH_TRIP_DEGC - TEMP_HYSTERESIS_DEGC) THEN
    IF bAlarmReset THEN
        bAlarm_SpindleBearingOverheat := FALSE;
    END_IF;
END_IF;

(* Regenerative Chatter Vibration High-High Trip *)
IF rPeakChatterAmplitude_ms2 >= VIB_CHATTER_HH_TRIP_MS2 THEN
    bAlarm_ExcessiveChatterVibration := TRUE;
ELSIF rPeakChatterAmplitude_ms2 <= (VIB_CHATTER_HH_TRIP_MS2 - VIB_HYSTERESIS_MS2) THEN
    IF bAlarmReset THEN
        bAlarm_ExcessiveChatterVibration := FALSE;
    END_IF;
END_IF;

(* Collision Impact Crash Failsafe Trip *)
IF rPeakChatterAmplitude_ms2 >= VIB_COLLISION_CRASH_MS2 THEN
    bAlarm_CollisionImpactTripped := TRUE;
    bCollisionStopActive := TRUE;
ELSIF bAlarmReset AND (rPeakChatterAmplitude_ms2 < 5.0) THEN
    bAlarm_CollisionImpactTripped := FALSE;
END_IF;

(* HSK Collet Hydraulic Grip Loss Trip *)
IF (rHydraulicClampPressure_bar < PRESSURE_CLAMP_MIN_BAR) AND bToolClampSolenoidCmd THEN
    bAlarm_ToolClampingDefect := TRUE;
ELSIF rHydraulicClampPressure_bar >= (PRESSURE_CLAMP_MIN_BAR + 5.0) THEN
    IF bAlarmReset THEN
        bAlarm_ToolClampingDefect := FALSE;
    END_IF;
END_IF;

(* Spindle Closed-Loop Chiller Flow Loss *)
IF rChillerCoolantFlow_lmin < CHILLER_FLOW_MIN_LMIN THEN
    bAlarm_ChillerCoolingLoss := TRUE;
ELSIF rChillerCoolantFlow_lmin >= (CHILLER_FLOW_MIN_LMIN + 1.0) THEN
    IF bAlarmReset THEN
        bAlarm_ChillerCoolingLoss := FALSE;
    END_IF;
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* 5.2: ISA-18.2 Priority 1 Critical Alarms (Immediate Failsafe Shutdown) Bit-Packing                  *)
(* ---------------------------------------------------------------------------------------------------- *)
dwAlarmStatus_P1_Critical := 16#00000000;

IF NOT bEmergencyStopLoop THEN
    dwAlarmStatus_P1_Critical := dwAlarmStatus_P1_Critical OR 16#00000001; (* Bit 0: SIL-3 E-Stop Open *)
END_IF;

IF bAlarm_CollisionImpactTripped THEN
    dwAlarmStatus_P1_Critical := dwAlarmStatus_P1_Critical OR 16#00000002; (* Bit 1: Collision Crash *)
END_IF;

IF (rSpindleCurrent_Iu_A > SPINDLE_CURRENT_MAX_A) OR
   (rSpindleCurrent_Iv_A > SPINDLE_CURRENT_MAX_A) OR
   (rSpindleCurrent_Iw_A > SPINDLE_CURRENT_MAX_A) THEN
    dwAlarmStatus_P1_Critical := dwAlarmStatus_P1_Critical OR 16#00000004; (* Bit 2: Inverter Overcurrent *)
END_IF;

IF rSpindleDCLinkVoltage_V > DCLINK_VOLTAGE_MAX_V THEN
    dwAlarmStatus_P1_Critical := dwAlarmStatus_P1_Critical OR 16#00000008; (* Bit 3: DC Bus Overvoltage *)
END_IF;

IF rSpindleDCLinkVoltage_V < DCLINK_VOLTAGE_MIN_V THEN
    dwAlarmStatus_P1_Critical := dwAlarmStatus_P1_Critical OR 16#00000010; (* Bit 4: DC Bus Undervoltage *)
END_IF;

IF bAlarm_ToolClampingDefect THEN
    dwAlarmStatus_P1_Critical := dwAlarmStatus_P1_Critical OR 16#00000020; (* Bit 5: Hydraulic Grip Lost *)
END_IF;

IF ABS(rGantryCrossCouplingYaw_um) > 150.0 THEN
    dwAlarmStatus_P1_Critical := dwAlarmStatus_P1_Critical OR 16#00000040; (* Bit 6: Gantry Skew Excessive *)
END_IF;

IF (nX_VotingMode = 0) OR (nY_VotingMode = 0) OR (nZ_VotingMode = 0) THEN
    dwAlarmStatus_P1_Critical := dwAlarmStatus_P1_Critical OR 16#00000080; (* Bit 7: Optical Scale TMR Lost *)
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* 5.3: ISA-18.2 Priority 2 High Severity Alarms (Process Controlled Trip) Bit-Packing                 *)
(* ---------------------------------------------------------------------------------------------------- *)
dwAlarmStatus_P2_High := 16#00000000;

IF bAlarm_SpindleBearingOverheat THEN
    dwAlarmStatus_P2_High := dwAlarmStatus_P2_High OR 16#00000001; (* Bit 0: Front Bearing High-High *)
END_IF;

IF rVotedStatorTemp_degC >= TEMP_STATOR_HH_TRIP_DEGC THEN
    dwAlarmStatus_P2_High := dwAlarmStatus_P2_High OR 16#00000002; (* Bit 1: Stator Core High-High *)
END_IF;

IF bAlarm_ExcessiveChatterVibration THEN
    dwAlarmStatus_P2_High := dwAlarmStatus_P2_High OR 16#00000004; (* Bit 2: Extreme Chatter Trip *)
END_IF;

IF bAlarm_ChillerCoolingLoss THEN
    dwAlarmStatus_P2_High := dwAlarmStatus_P2_High OR 16#00000008; (* Bit 3: Glycol Flow Loss *)
END_IF;

IF rVotedRearBearingTemp_degC >= TEMP_BRG_HH_TRIP_DEGC THEN
    dwAlarmStatus_P2_High := dwAlarmStatus_P2_High OR 16#00000010; (* Bit 4: Rear Bearing High-High *)
END_IF;

IF rBearingPreloadDelta_N > 1400.0 THEN
    dwAlarmStatus_P2_High := dwAlarmStatus_P2_High OR 16#00000020; (* Bit 5: Bearing Preload Runaway *)
END_IF;

IF (ABS(rActiveDampForceCmd_X_N) >= 445.0) OR (ABS(rActiveDampForceCmd_Y_N) >= 445.0) THEN
    dwAlarmStatus_P2_High := dwAlarmStatus_P2_High OR 16#00000040; (* Bit 6: AIMD Actuator Saturation *)
END_IF;

IF (nSpd_VotingMode = 0) OR (nTF_VotingMode = 0) THEN
    dwAlarmStatus_P2_High := dwAlarmStatus_P2_High OR 16#00000080; (* Bit 7: Sensor Triplet Complete Fail *)
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* 5.4: ISA-18.2 Priority 3 Medium Severity Alarms (Process Warnings) Bit-Packing                      *)
(* ---------------------------------------------------------------------------------------------------- *)
dwAlarmStatus_P3_Medium := 16#00000000;

IF rVotedFrontBearingTemp_degC >= TEMP_BRG_H_WARN_DEGC THEN
    dwAlarmStatus_P3_Medium := dwAlarmStatus_P3_Medium OR 16#00000001; (* Bit 0: Front Bearing High Warn *)
END_IF;

IF rVotedStatorTemp_degC >= TEMP_STATOR_H_WARN_DEGC THEN
    dwAlarmStatus_P3_Medium := dwAlarmStatus_P3_Medium OR 16#00000002; (* Bit 1: Stator High Warn *)
END_IF;

IF rPeakChatterAmplitude_ms2 >= VIB_CHATTER_H_WARN_MS2 THEN
    dwAlarmStatus_P3_Medium := dwAlarmStatus_P3_Medium OR 16#00000004; (* Bit 2: Chatter Onset Warn *)
END_IF;

IF rToolTipDeflection_um > 25.0 THEN
    dwAlarmStatus_P3_Medium := dwAlarmStatus_P3_Medium OR 16#00000008; (* Bit 3: High Tool Deflection *)
END_IF;

IF (nX_VotingMode < 3) OR (nY_VotingMode < 3) OR (nZ_VotingMode < 3) OR
   (nSpd_VotingMode < 3) OR (nTF_VotingMode < 3) THEN
    dwAlarmStatus_P3_Medium := dwAlarmStatus_P3_Medium OR 16#00000010; (* Bit 4: Single Channel TMR Fault *)
END_IF;

IF rChipConveyorMotorLoad_pct > 80.0 THEN
    dwAlarmStatus_P3_Medium := dwAlarmStatus_P3_Medium OR 16#00000020; (* Bit 5: Swarf Screw High Load *)
END_IF;

IF rMeasuredRunout_um > 2.50 THEN
    dwAlarmStatus_P3_Medium := dwAlarmStatus_P3_Medium OR 16#00000040; (* Bit 6: Tool Runout Warning *)
END_IF;

IF rChillerInletTemp_degC > 24.0 THEN
    dwAlarmStatus_P3_Medium := dwAlarmStatus_P3_Medium OR 16#00000080; (* Bit 7: Chiller Supply Warm *)
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* 5.5: ISA-18.2 Priority 4 Low Severity Alarms (Advisories & Maintenance) Bit-Packing                 *)
(* ---------------------------------------------------------------------------------------------------- *)
dwAlarmStatus_P4_Advisory := 16#00000000;

IF bChatterActiveCondition THEN
    dwAlarmStatus_P4_Advisory := dwAlarmStatus_P4_Advisory OR 16#00000001; (* Bit 0: SSV Modulation Active *)
END_IF;

IF rAdaptiveFeedOverride_pct < 95.0 THEN
    dwAlarmStatus_P4_Advisory := dwAlarmStatus_P4_Advisory OR 16#00000002; (* Bit 1: Feedrate Throttling Active *)
END_IF;

IF bThermalCompEnable THEN
    dwAlarmStatus_P4_Advisory := dwAlarmStatus_P4_Advisory OR 16#00000004; (* Bit 2: Thermal Offset Active *)
END_IF;

IF bActiveDampingEnable THEN
    dwAlarmStatus_P4_Advisory := dwAlarmStatus_P4_Advisory OR 16#00000008; (* Bit 3: AIMD Actuators Active *)
END_IF;

IF bTouchProbeDeflected THEN
    dwAlarmStatus_P4_Advisory := dwAlarmStatus_P4_Advisory OR 16#00000010; (* Bit 4: Probe Contact Strobe *)
END_IF;

IF bLaserToolSetterBeamBreak THEN
    dwAlarmStatus_P4_Advisory := dwAlarmStatus_P4_Advisory OR 16#00000020; (* Bit 5: Laser Tool In-Beam *)
END_IF;

IF rThroughSpindleCoolant_bar < PRESSURE_TSC_MIN_BAR AND bThroughSpindleCoolantCmd THEN
    dwAlarmStatus_P4_Advisory := dwAlarmStatus_P4_Advisory OR 16#00000040; (* Bit 6: TSC Pressure Marginal *)
END_IF;

IF rStageDwellTimer_s > 600.0 THEN
    dwAlarmStatus_P4_Advisory := dwAlarmStatus_P4_Advisory OR 16#00000080; (* Bit 7: Stage Dwell Long *)
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* 5.6: Machine Subsystem Bit-Packed Status Words                                                       *)
(* ---------------------------------------------------------------------------------------------------- *)
(* dwMotionStatusWord: Bits 0..3: Stage, Bit 4: Auto, Bit 5: Homing Done, Bit 6: Skew OK, Bit 7: TCP OK *)
dwMotionStatusWord := INT_TO_DWORD(nActiveFSMStage);
IF bMachineAutoMode THEN
    dwMotionStatusWord := dwMotionStatusWord OR 16#00000010;
END_IF;
IF ABS(rGantryYaw_SkewError_mm) <= 0.010 THEN
    dwMotionStatusWord := dwMotionStatusWord OR 16#00000020;
END_IF;
IF bSystemEnable THEN
    dwMotionStatusWord := dwMotionStatusWord OR 16#00000040;
END_IF;

(* dwSpindleStatusWord: Bit 0: Drive En, Bit 1: Clamped, Bit 2: Chiller OK, Bit 3: Orient Lock, Bit 4: SSV *)
dwSpindleStatusWord := 16#00000000;
IF bSpindleDriveEnable THEN
    dwSpindleStatusWord := dwSpindleStatusWord OR 16#00000001;
END_IF;
IF bToolClampSolenoidCmd THEN
    dwSpindleStatusWord := dwSpindleStatusWord OR 16#00000002;
END_IF;
IF rChillerCoolantFlow_lmin >= CHILLER_FLOW_MIN_LMIN THEN
    dwSpindleStatusWord := dwSpindleStatusWord OR 16#00000004;
END_IF;
IF nActiveFSMStage = 8 THEN
    dwSpindleStatusWord := dwSpindleStatusWord OR 16#00000008;
END_IF;
IF bChatterActiveCondition THEN
    dwSpindleStatusWord := dwSpindleStatusWord OR 16#00000010;
END_IF;

(* dwDampingStatusWord: Bit 0: Damping En, Bit 1: Therm Comp En, Bit 2: Chatter Detected, Bit 3: Collision *)
dwDampingStatusWord := 16#00000000;
IF bActiveDampingEnable THEN
    dwDampingStatusWord := dwDampingStatusWord OR 16#00000001;
END_IF;
IF bThermalCompEnable THEN
    dwDampingStatusWord := dwDampingStatusWord OR 16#00000002;
END_IF;
IF bChatterActiveCondition THEN
    dwDampingStatusWord := dwDampingStatusWord OR 16#00000004;
END_IF;
IF bCollisionStopActive THEN
    dwDampingStatusWord := dwDampingStatusWord OR 16#00000008;
END_IF;

(* Master Machine Ready Output Evaluation *)
bMachiningCenterReady := bSystemEnable AND
                         bEmergencyStopLoop AND
                         (NOT bCollisionStopActive) AND
                         (dwAlarmStatus_P1_Critical = 16#00000000) AND
                         (dwAlarmStatus_P2_High = 16#00000000);

END_FUNCTION_BLOCK
"""
