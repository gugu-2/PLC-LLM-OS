# -*- coding: utf-8 -*-
"""
Builder script for Automotive BIW Robotic Framer Dataset
Target: FB_Automotive_BIW_RoboticFramer_SpotWelding
Produces pristine IEC 61131-3 Structured Text dataset.
"""

import os
import sys
import json
import uuid

def generate_framer_code():
    parts = []
    
    # -------------------------------------------------------------------------
    # FUNCTION BLOCK DECLARATION & HEADER
    # -------------------------------------------------------------------------
    parts.append("""FUNCTION_BLOCK FB_Automotive_BIW_RoboticFramer_SpotWelding
(*
========================================================================================================================
  LUMINA CYBER-PHYSICAL AUTOMATION ARCHITECTURE - V7 MAX-PERSONA SPECIFICATION
  CORE SECTOR    : AUTOMOTIVE BODY MANUFACTURING & INDUSTRIAL ROBOTICS (TIER 1 PRIORITY)
  APPLICATION    : HIGH-SPEED AUTOMOTIVE BODY-IN-WHITE (BIW) MAIN FRAMER GEOMETRY GATE
  CELL TOPOLOGY  : 8-ROBOT COORDINATED SERVO SPOT WELDING CELL WITH ADAPTIVE MFDC CURRENT & EXPULSION CONTROL
  RIGID TOOLING  : DUAL LATERAL FRAMING GATES WITH SERVO LOCATING PIN INSERTION (REPEATABILITY < +-0.05 mm)
  METROLOGY      : IN-LINE OPTICAL LASER LINE SCANNER CMM DIMENSIONAL VERIFICATION (ROOF, A/B/C PILLAR GAP & FLUSH)
  LOGISTICS      : SYNCHRONOUS ROLLER BED SKID TRANSFER TABLE WITH 7-SEGMENT S-CURVE & LIFT-AND-CARRY ECCENTRIC
  FUNCTION BLOCK : FB_Automotive_BIW_RoboticFramer_SpotWelding
  P&ID TAGGING   : ISA-5.1 STANDARD DESIGNATION (ZT, PT, CT, ET, WT, TT, FT, DT, ST, AT SERIES 100-600)
  REDUNDANCY     : 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) ACROSS ALL 12 CRITICAL SENSOR CHANNELS
  CYBER-PHYSICS  : 8x8 MULTIVARIABLE DISCRETE STATE-SPACE OBSERVER (Ts = 5 ms) WITH KALMAN-LUENBERGER GAINS
  OPTIMIZATION   : RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) WITH PROJECTED GRADIENT DESCENT & SLEW LIMITS
  WELD PHYSICS   : DYNAMIC NUGGET RESISTANCE INFLECTION TRACKING, JOULE ENERGY INTEGRAL & EXPULSION DETECTION
  KINEMATICS     : NON-LINEAR 4-BAR TOGGLE CLAMP MECHANISM KINEMATICS & 7-SEGMENT JERK-LIMITED S-CURVE PROFILE
  METROLOGY STAT : REAL-TIME GAUSSIAN DISTRIBUTION FITTING, BILATERAL TOLERANCE CHECK & Cp / Cpk EVALUATION
  SAFETY & ALARM : ISA-18.2 FIVE-TIER MULTI-PARAMETRIC ALARM ENGINE WITH PACKED 32-BIT DWORD STATUS REGISTERS
========================================================================================================================
*)
""")

    # -------------------------------------------------------------------------
    # VAR_INPUT
    # -------------------------------------------------------------------------
    parts.append("""VAR_INPUT
    (* === MASTER SYSTEM CLOCK & SCAN SIGNALS === *)
    bMasterScanPulse_5ms                : BOOL := FALSE;      (* Master deterministic 5ms scan pulse from RT-OS [bool] *)
    bSystemEnable                       : BOOL := FALSE;      (* Master cell software enable interlock [bool] *)
    bEmergencyStopCircuitHealthy        : BOOL := FALSE;      (* Dual-channel Category 4 / PLe emergency stop loop [bool] *)
    bSafetyFenceZoneInterlocksOk        : BOOL := FALSE;      (* Perimeter safety light curtain & gate latch status [bool] *)
    bAutoCycleStartCmd                  : BOOL := FALSE;      (* HMI auto sequence start pushbutton command [bool] *)
    bAutoCycleAbortCmd                  : BOOL := FALSE;      (* HMI auto sequence graceful abort command [bool] *)
    bAlarmResetCmd                      : BOOL := FALSE;      (* HMI master alarm acknowledge and reset button [bool] *)
    bDryRunModeEnable                   : BOOL := FALSE;      (* Dry-run without weld current and laser inspection [bool] *)

    (* === TRANSMITTER TRIPLET 1: FRAMING GATE LH POSITION RESOLVER (ZT_101A/B/C) === *)
    ZT_FRAMING_GATE_LH_POS_101A         : REAL := 0.0;        (* Gate LH linear resolver position channel A [mm] *)
    ZT_FRAMING_GATE_LH_POS_101B         : REAL := 0.0;        (* Gate LH linear resolver position channel B [mm] *)
    ZT_FRAMING_GATE_LH_POS_101C         : REAL := 0.0;        (* Gate LH linear resolver position channel C [mm] *)
    bStatus_ZT_101A_Healthy             : BOOL := TRUE;       (* Transducer 101A hardware health bit [bool] *)
    bStatus_ZT_101B_Healthy             : BOOL := TRUE;       (* Transducer 101B hardware health bit [bool] *)
    bStatus_ZT_101C_Healthy             : BOOL := TRUE;       (* Transducer 101C hardware health bit [bool] *)

    (* === TRANSMITTER TRIPLET 2: FRAMING GATE RH POSITION RESOLVER (ZT_102A/B/C) === *)
    ZT_FRAMING_GATE_RH_POS_102A         : REAL := 0.0;        (* Gate RH linear resolver position channel A [mm] *)
    ZT_FRAMING_GATE_RH_POS_102B         : REAL := 0.0;        (* Gate RH linear resolver position channel B [mm] *)
    ZT_FRAMING_GATE_RH_POS_102C         : REAL := 0.0;        (* Gate RH linear resolver position channel C [mm] *)
    bStatus_ZT_102A_Healthy             : BOOL := TRUE;       (* Transducer 102A hardware health bit [bool] *)
    bStatus_ZT_102B_Healthy             : BOOL := TRUE;       (* Transducer 102B hardware health bit [bool] *)
    bStatus_ZT_102C_Healthy             : BOOL := TRUE;       (* Transducer 102C hardware health bit [bool] *)

    (* === TRANSMITTER TRIPLET 3: PNEUMATIC MAIN HEADER SUPPLY PRESSURE (PT_201A/B/C) === *)
    PT_PNEUMATIC_MAIN_HEADER_201A       : REAL := 6.0;        (* Main pneumatic header pressure sensor A [bar] *)
    PT_PNEUMATIC_MAIN_HEADER_201B       : REAL := 6.0;        (* Main pneumatic header pressure sensor B [bar] *)
    PT_PNEUMATIC_MAIN_HEADER_201C       : REAL := 6.0;        (* Main pneumatic header pressure sensor C [bar] *)
    bStatus_PT_201A_Healthy             : BOOL := TRUE;       (* Pressure transmitter 201A health bit [bool] *)
    bStatus_PT_201B_Healthy             : BOOL := TRUE;       (* Pressure transmitter 201B health bit [bool] *)
    bStatus_PT_201C_Healthy             : BOOL := TRUE;       (* Pressure transmitter 201C health bit [bool] *)

    (* === TRANSMITTER TRIPLET 4: HYDRAULIC TOGGLE CLAMP LOCK PRESSURE (PT_202A/B/C) === *)
    PT_HYD_TOGGLE_CLAMP_PRESS_202A      : REAL := 120.0;      (* Hydraulic toggle lock circuit pressure A [bar] *)
    PT_HYD_TOGGLE_CLAMP_PRESS_202B      : REAL := 120.0;      (* Hydraulic toggle lock circuit pressure B [bar] *)
    PT_HYD_TOGGLE_CLAMP_PRESS_202C      : REAL := 120.0;      (* Hydraulic toggle lock circuit pressure C [bar] *)
    bStatus_PT_202A_Healthy             : BOOL := TRUE;       (* Pressure transmitter 202A health bit [bool] *)
    bStatus_PT_202B_Healthy             : BOOL := TRUE;       (* Pressure transmitter 202B health bit [bool] *)
    bStatus_PT_202C_Healthy             : BOOL := TRUE;       (* Pressure transmitter 202C health bit [bool] *)

    (* === TRANSMITTER TRIPLET 5: ROBOT 1 MFDC SECONDARY CURRENT ROGOWSKI (CT_301A/B/C) === *)
    CT_ROBOT1_WELD_CURRENT_301A         : REAL := 0.0;        (* Robot 1 secondary weld current Rogowski A [kA] *)
    CT_ROBOT1_WELD_CURRENT_301B         : REAL := 0.0;        (* Robot 1 secondary weld current Rogowski B [kA] *)
    CT_ROBOT1_WELD_CURRENT_301C         : REAL := 0.0;        (* Robot 1 secondary weld current Rogowski C [kA] *)
    bStatus_CT_301A_Healthy             : BOOL := TRUE;       (* Rogowski coil 301A health bit [bool] *)
    bStatus_CT_301B_Healthy             : BOOL := TRUE;       (* Rogowski coil 301B health bit [bool] *)
    bStatus_CT_301C_Healthy             : BOOL := TRUE;       (* Rogowski coil 301C health bit [bool] *)

    (* === TRANSMITTER TRIPLET 6: ROBOT 2 MFDC SECONDARY CURRENT ROGOWSKI (CT_302A/B/C) === *)
    CT_ROBOT2_WELD_CURRENT_302A         : REAL := 0.0;        (* Robot 2 secondary weld current Rogowski A [kA] *)
    CT_ROBOT2_WELD_CURRENT_302B         : REAL := 0.0;        (* Robot 2 secondary weld current Rogowski B [kA] *)
    CT_ROBOT2_WELD_CURRENT_302C         : REAL := 0.0;        (* Robot 2 secondary weld current Rogowski C [kA] *)
    bStatus_CT_302A_Healthy             : BOOL := TRUE;       (* Rogowski coil 302A health bit [bool] *)
    bStatus_CT_302B_Healthy             : BOOL := TRUE;       (* Rogowski coil 302B health bit [bool] *)
    bStatus_CT_302C_Healthy             : BOOL := TRUE;       (* Rogowski coil 302C health bit [bool] *)

    (* === ROBOTS 3 THROUGH 8 SECONDARY WELD CURRENT SENSORS === *)
    CT_ROBOT3_WELD_CURRENT              : REAL := 0.0;        (* Robot 3 secondary weld current feedback [kA] *)
    CT_ROBOT4_WELD_CURRENT              : REAL := 0.0;        (* Robot 4 secondary weld current feedback [kA] *)
    CT_ROBOT5_WELD_CURRENT              : REAL := 0.0;        (* Robot 5 secondary weld current feedback [kA] *)
    CT_ROBOT6_WELD_CURRENT              : REAL := 0.0;        (* Robot 6 secondary weld current feedback [kA] *)
    CT_ROBOT7_WELD_CURRENT              : REAL := 0.0;        (* Robot 7 secondary weld current feedback [kA] *)
    CT_ROBOT8_WELD_CURRENT              : REAL := 0.0;        (* Robot 8 secondary weld current feedback [kA] *)

    (* === TRANSMITTER TRIPLET 7: SERVO WELD GUN 1 TIP CONTACT FORCE (WT_321A/B/C) === *)
    WT_GUN1_SERVO_TIP_FORCE_321A        : REAL := 0.0;        (* Weld Gun 1 piezoelectric tip force transducer A [kN] *)
    WT_GUN1_SERVO_TIP_FORCE_321B        : REAL := 0.0;        (* Weld Gun 1 piezoelectric tip force transducer B [kN] *)
    WT_GUN1_SERVO_TIP_FORCE_321C        : REAL := 0.0;        (* Weld Gun 1 piezoelectric tip force transducer C [kN] *)
    bStatus_WT_321A_Healthy             : BOOL := TRUE;       (* Force load cell 321A health bit [bool] *)
    bStatus_WT_321B_Healthy             : BOOL := TRUE;       (* Force load cell 321B health bit [bool] *)
    bStatus_WT_321C_Healthy             : BOOL := TRUE;       (* Force load cell 321C health bit [bool] *)

    (* === WELD TIP VOLTAGE AND PROCESS SENSORS === *)
    ET_ROBOT1_SECONDARY_VOLT            : REAL := 0.0;        (* Robot 1 electrode tip secondary voltage [V] *)
    ET_ROBOT2_SECONDARY_VOLT            : REAL := 0.0;        (* Robot 2 electrode tip secondary voltage [V] *)
    TT_ROBOT1_ELECTRODE_TEMP            : REAL := 22.0;       (* Robot 1 electrode tip thermocouple [deg C] *)
    TT_ROBOT2_ELECTRODE_TEMP            : REAL := 22.0;       (* Robot 2 electrode tip thermocouple [deg C] *)
    FT_GUN1_COOLING_WATER_FLOW          : REAL := 12.0;       (* Robot 1 weld tip cooling water flow meter [l/min] *)
    FT_GUN2_COOLING_WATER_FLOW          : REAL := 12.0;       (* Robot 2 weld tip cooling water flow meter [l/min] *)

    (* === TRANSMITTER TRIPLET 8: OPTICAL LASER CMM A-PILLAR GAP SENSOR (DT_401A/B/C) === *)
    DT_LASER_CMM_GAP_A_PILLAR_401A      : REAL := 3.5;        (* Laser CMM A-pillar body gap triangulation A [mm] *)
    DT_LASER_CMM_GAP_A_PILLAR_401B      : REAL := 3.5;        (* Laser CMM A-pillar body gap triangulation B [mm] *)
    DT_LASER_CMM_GAP_A_PILLAR_401C      : REAL := 3.5;        (* Laser CMM A-pillar body gap triangulation C [mm] *)
    bStatus_DT_401A_Healthy             : BOOL := TRUE;       (* Laser scanner 401A health bit [bool] *)
    bStatus_DT_401B_Healthy             : BOOL := TRUE;       (* Laser scanner 401B health bit [bool] *)
    bStatus_DT_401C_Healthy             : BOOL := TRUE;       (* Laser scanner 401C health bit [bool] *)

    (* === TRANSMITTER TRIPLET 9: OPTICAL LASER CMM A-PILLAR FLUSH SENSOR (DT_402A/B/C) === *)
    DT_LASER_CMM_FLUSH_A_PILLAR_402A    : REAL := 0.0;        (* Laser CMM A-pillar flushness triangulation A [mm] *)
    DT_LASER_CMM_FLUSH_A_PILLAR_402B    : REAL := 0.0;        (* Laser CMM A-pillar flushness triangulation B [mm] *)
    DT_LASER_CMM_FLUSH_A_PILLAR_402C    : REAL := 0.0;        (* Laser CMM A-pillar flushness triangulation C [mm] *)
    bStatus_DT_402A_Healthy             : BOOL := TRUE;       (* Laser scanner 402A health bit [bool] *)
    bStatus_DT_402B_Healthy             : BOOL := TRUE;       (* Laser scanner 402B health bit [bool] *)
    bStatus_DT_402C_Healthy             : BOOL := TRUE;       (* Laser scanner 402C health bit [bool] *)

    (* === METROLOGY CMM ADDITIONAL FEATURE TRANSDUCERS === *)
    DT_LASER_CMM_GAP_B_PILLAR           : REAL := 3.5;        (* Laser CMM B-pillar gap gauge reading [mm] *)
    DT_LASER_CMM_FLUSH_B_PILLAR         : REAL := 0.0;        (* Laser CMM B-pillar flushness gauge reading [mm] *)
    DT_LASER_CMM_GAP_C_PILLAR           : REAL := 3.5;        (* Laser CMM C-pillar gap gauge reading [mm] *)
    DT_LASER_CMM_FLUSH_C_PILLAR         : REAL := 0.0;        (* Laser CMM C-pillar flushness gauge reading [mm] *)
    DT_LASER_CMM_GAP_ROOF_DITCH_LH      : REAL := 3.5;        (* Laser CMM roof ditch LH seam gap [mm] *)
    DT_LASER_CMM_GAP_ROOF_DITCH_RH      : REAL := 3.5;        (* Laser CMM roof ditch RH seam gap [mm] *)

    (* === TRANSMITTER TRIPLET 10: SKID CONVEYOR VELOCITY TACHOMETER (ST_501A/B/C) === *)
    ST_SKID_CONVEYOR_VELOCITY_501A      : REAL := 0.0;        (* Roller bed drive motor encoder tachometer A [mm/s] *)
    ST_SKID_CONVEYOR_VELOCITY_501B      : REAL := 0.0;        (* Roller bed drive motor encoder tachometer B [mm/s] *)
    ST_SKID_CONVEYOR_VELOCITY_501C      : REAL := 0.0;        (* Roller bed drive motor encoder tachometer C [mm/s] *)
    bStatus_ST_501A_Healthy             : BOOL := TRUE;       (* Encoder tachometer 501A health bit [bool] *)
    bStatus_ST_501B_Healthy             : BOOL := TRUE;       (* Encoder tachometer 501B health bit [bool] *)
    bStatus_ST_501C_Healthy             : BOOL := TRUE;       (* Encoder tachometer 501C health bit [bool] *)

    (* === TRANSMITTER TRIPLET 11: SKID ABSOLUTE OPTICAL POSITION SCALE (ZT_502A/B/C) === *)
    ZT_SKID_TRANSFER_POS_502A           : REAL := 0.0;        (* Roller bed absolute optical bar code tape scale A [mm] *)
    ZT_SKID_TRANSFER_POS_502B           : REAL := 0.0;        (* Roller bed absolute optical bar code tape scale B [mm] *)
    ZT_SKID_TRANSFER_POS_502C           : REAL := 0.0;        (* Roller bed absolute optical bar code tape scale C [mm] *)
    bStatus_ZT_502A_Healthy             : BOOL := TRUE;       (* Optical scale 502A health bit [bool] *)
    bStatus_ZT_502B_Healthy             : BOOL := TRUE;       (* Optical scale 502B health bit [bool] *)
    bStatus_ZT_502C_Healthy             : BOOL := TRUE;       (* Optical scale 502C health bit [bool] *)

    (* === TRANSMITTER TRIPLET 12: FRAMER BASE VIBRATION ACCELEROMETER (AT_601A/B/C) === *)
    AT_FRAME_VIBRATION_ACCEL_601A       : REAL := 0.0;        (* Structural triaxial accelerometer seismic channel A [m/s^2] *)
    AT_FRAME_VIBRATION_ACCEL_601B       : REAL := 0.0;        (* Structural triaxial accelerometer seismic channel B [m/s^2] *)
    AT_FRAME_VIBRATION_ACCEL_601C       : REAL := 0.0;        (* Structural triaxial accelerometer seismic channel C [m/s^2] *)
    bStatus_AT_601A_Healthy             : BOOL := TRUE;       (* Vibration sensor 601A health bit [bool] *)
    bStatus_AT_601B_Healthy             : BOOL := TRUE;       (* Vibration sensor 601B health bit [bool] *)
    bStatus_AT_601C_Healthy             : BOOL := TRUE;       (* Vibration sensor 601C health bit [bool] *)

    (* === DISCRETE SENSOR & TOOLING PROXIMITY INPUTS === *)
    bSkidInfeedZonePresent              : BOOL := FALSE;      (* Optical photo-eye detecting vehicle skid in infeed zone [bool] *)
    bSkidRoughLocatePinsRaised          : BOOL := FALSE;      (* Proximity sensor rough locating pins fully raised [bool] *)
    bSkidRoughLocatePinsLowered         : BOOL := TRUE;       (* Proximity sensor rough locating pins fully lowered [bool] *)
    bFramingGateLH_ToggleLocked         : BOOL := FALSE;      (* Mechanical toggle clamp LH over-center locked switch [bool] *)
    bFramingGateRH_ToggleLocked         : BOOL := FALSE;      (* Mechanical toggle clamp RH over-center locked switch [bool] *)
    bServoLocatingPinsLH_Seated         : BOOL := FALSE;      (* Dual NC locating pins LH seated into vehicle datum [bool] *)
    bServoLocatingPinsRH_Seated         : BOOL := FALSE;      (* Dual NC locating pins RH seated into vehicle datum [bool] *)
    bBodyPartClampsClosed_Group1        : BOOL := FALSE;      (* Underbody rocker rail toggle clamps closed feedback [bool] *)
    bBodyPartClampsClosed_Group2        : BOOL := FALSE;      (* A-pillar and cowl toggle clamps closed feedback [bool] *)
    bBodyPartClampsClosed_Group3        : BOOL := FALSE;      (* B-pillar and C-pillar toggle clamps closed feedback [bool] *)
    bBodyPartClampsClosed_Group4        : BOOL := FALSE;      (* Roof header and bow toggle clamps closed feedback [bool] *)

    (* === ROBOT 1-8 INTERLOCK & HANDSHAKE SIGNALS === *)
    bRobot1_AtHome                      : BOOL := TRUE;       (* Robot 1 arm positioned at safety home stance [bool] *)
    bRobot1_WeldComplete                : BOOL := FALSE;      (* Robot 1 cycle completion handshake [bool] *)
    bRobot2_AtHome                      : BOOL := TRUE;       (* Robot 2 arm positioned at safety home stance [bool] *)
    bRobot2_WeldComplete                : BOOL := FALSE;      (* Robot 2 cycle completion handshake [bool] *)
    bRobot3_AtHome                      : BOOL := TRUE;       (* Robot 3 arm positioned at safety home stance [bool] *)
    bRobot3_WeldComplete                : BOOL := FALSE;      (* Robot 3 cycle completion handshake [bool] *)
    bRobot4_AtHome                      : BOOL := TRUE;       (* Robot 4 arm positioned at safety home stance [bool] *)
    bRobot4_WeldComplete                : BOOL := FALSE;      (* Robot 4 cycle completion handshake [bool] *)
    bRobot5_AtHome                      : BOOL := TRUE;       (* Robot 5 arm positioned at safety home stance [bool] *)
    bRobot5_WeldComplete                : BOOL := FALSE;      (* Robot 5 cycle completion handshake [bool] *)
    bRobot6_AtHome                      : BOOL := TRUE;       (* Robot 6 arm positioned at safety home stance [bool] *)
    bRobot6_WeldComplete                : BOOL := FALSE;      (* Robot 6 cycle completion handshake [bool] *)
    bRobot7_AtHome                      : BOOL := TRUE;       (* Robot 7 arm positioned at safety home stance [bool] *)
    bRobot7_WeldComplete                : BOOL := FALSE;      (* Robot 7 cycle completion handshake [bool] *)
    bRobot8_AtHome                      : BOOL := TRUE;       (* Robot 8 arm positioned at safety home stance [bool] *)
    bRobot8_WeldComplete                : BOOL := FALSE;      (* Robot 8 cycle completion handshake [bool] *)
    bRobotCollisionZoneLH_Clear         : BOOL := TRUE;       (* Hardware safety radar: Left framing envelope clear of robots [bool] *)
    bRobotCollisionZoneRH_Clear         : BOOL := TRUE;       (* Hardware safety radar: Right framing envelope clear of robots [bool] *)
    bLaserCMM_InspectionComplete        : BOOL := FALSE;      (* In-line optical CMM scan acquisition complete handshake [bool] *)
    bLaserCMM_PassStatus                : BOOL := FALSE;      (* In-line optical CMM pass/fail evaluation flag [bool] *)
    bDownstreamStationReadyForSkid      : BOOL := TRUE;       (* Downstream respot station clear to receive processed skid [bool] *)
END_VAR
""")

    # -------------------------------------------------------------------------
    # VAR_OUTPUT
    # -------------------------------------------------------------------------
    parts.append("""VAR_OUTPUT
    (* === ACTUATOR MOTION & VALVE COMMANDS === *)
    rFramingGateLH_ServoSpeedCmd        : REAL := 0.0;        (* Gate LH servo drive speed command [-100.0..+100.0 %] *)
    rFramingGateRH_ServoSpeedCmd        : REAL := 0.0;        (* Gate RH servo drive speed command [-100.0..+100.0 %] *)
    rSkidRollerVFD_FreqCmd              : REAL := 0.0;        (* Skid transfer table closed-loop vector VFD frequency [Hz] *)
    rPneumaticClampPropValveCmd         : REAL := 0.0;        (* Proportional pressure regulator command for clamps [bar] *)
    rHydraulicToggleLockPropCmd         : REAL := 0.0;        (* Hydraulic toggle locking cylinder pressure command [bar] *)
    rActiveMassDamperForceCmd           : REAL := 0.0;        (* Structural active vibration damper excitation command [N] *)

    (* === MFDC WELD CONTROLLER COMPENSATION COMMANDS === *)
    rRobot1_MFDC_DutyCycleBoost         : REAL := 0.0;        (* Robot 1 MFDC inverter adaptive duty cycle trim [%] *)
    rRobot2_MFDC_DutyCycleBoost         : REAL := 0.0;        (* Robot 2 MFDC inverter adaptive duty cycle trim [%] *)
    rRobot1_TipCoolingFlowModCmd        : REAL := 0.0;        (* Robot 1 chiller proportional valve flow modulation [l/min] *)
    rRobot2_TipCoolingFlowModCmd        : REAL := 0.0;        (* Robot 2 chiller proportional valve flow modulation [l/min] *)

    (* === DISCRETE ACTUATION & HANDSHAKE OUTPUTS === *)
    bCmd_SkidRoughLocateLifterRaise     : BOOL := FALSE;      (* Lifter cylinder solenoid energize to raise body [bool] *)
    bCmd_SkidRoughLocateLifterLower     : BOOL := FALSE;      (* Lifter cylinder solenoid energize to lower body [bool] *)
    bCmd_GateLH_ToggleLockEngage        : BOOL := FALSE;      (* LH gate mechanical toggle lock clamp solenoid [bool] *)
    bCmd_GateRH_ToggleLockEngage        : BOOL := FALSE;      (* RH gate mechanical toggle lock clamp solenoid [bool] *)
    bCmd_ServoLocatingPinsLH_Advance    : BOOL := FALSE;      (* LH precision servo pin advance trigger [bool] *)
    bCmd_ServoLocatingPinsRH_Advance    : BOOL := FALSE;      (* RH precision servo pin advance trigger [bool] *)
    bCmd_BodyPartClamps_Close_Grp1      : BOOL := FALSE;      (* Underbody rocker rail toggle clamps close solenoid [bool] *)
    bCmd_BodyPartClamps_Close_Grp2      : BOOL := FALSE;      (* A-pillar and cowl toggle clamps close solenoid [bool] *)
    bCmd_BodyPartClamps_Close_Grp3      : BOOL := FALSE;      (* B-pillar and C-pillar toggle clamps close solenoid [bool] *)
    bCmd_BodyPartClamps_Close_Grp4      : BOOL := FALSE;      (* Roof header toggle clamps close solenoid [bool] *)
    bCmd_TriggerRobotGrp1_GeoTack       : BOOL := FALSE;      (* Robot 1-4 execute primary geometry tack weld sequence [bool] *)
    bCmd_TriggerRobotGrp2_Respot        : BOOL := FALSE;      (* Robot 5-8 execute secondary structural respot sequence [bool] *)
    bCmd_TriggerLaserCMM_ScanCycle      : BOOL := FALSE;      (* Optical line scanner gantry start scan traverse [bool] *)
    bCmd_TipDresserCycleRequest         : BOOL := FALSE;      (* Tip dresser pneumatic cutter head cycle request [bool] *)
    bCmd_CellCycleCompletedPulse        : BOOL := FALSE;      (* One-shot pulse indicating completed vehicle BIW framing cycle [bool] *)
    bCmd_CellSafeHoldActive             : BOOL := FALSE;      (* Cell actuators safely locked in deterministic safe state [bool] *)

    (* === VOTED REAL-TIME PROCESS MEASUREMENTS === *)
    rVoted_GateLH_Position              : REAL := 0.0;        (* 2oo3 voted Gate LH position [mm] *)
    rVoted_GateRH_Position              : REAL := 0.0;        (* 2oo3 voted Gate RH position [mm] *)
    rVoted_PneumaticHeaderPressure      : REAL := 0.0;        (* 2oo3 voted pneumatic header pressure [bar] *)
    rVoted_HydraulicTogglePressure      : REAL := 0.0;        (* 2oo3 voted hydraulic toggle clamp pressure [bar] *)
    rVoted_Robot1_WeldCurrent           : REAL := 0.0;        (* 2oo3 voted Robot 1 secondary weld current [kA] *)
    rVoted_Robot2_WeldCurrent           : REAL := 0.0;        (* 2oo3 voted Robot 2 secondary weld current [kA] *)
    rVoted_Gun1_TipContactForce         : REAL := 0.0;        (* 2oo3 voted Gun 1 tip contact force [kN] *)
    rVoted_LaserCMM_Gap_A_Pillar        : REAL := 0.0;        (* 2oo3 voted A-pillar gap measurement [mm] *)
    rVoted_LaserCMM_Flush_A_Pillar      : REAL := 0.0;        (* 2oo3 voted A-pillar flushness measurement [mm] *)
    rVoted_SkidVelocity                 : REAL := 0.0;        (* 2oo3 voted skid conveyor velocity [mm/s] *)
    rVoted_SkidTransferPosition         : REAL := 0.0;        (* 2oo3 voted skid optical linear position [mm] *)
    rVoted_FrameVibrationAccel          : REAL := 0.0;        (* 2oo3 voted framer base vibration acceleration [m/s^2] *)

    (* === ESTIMATED CYBER-PHYSICAL INTERNAL PROPERTIES === *)
    rEst_NuggetDynamicResistance        : REAL := 0.0;        (* Estimated instantaneous weld nugget resistance [mOhm] *)
    rEst_AccumulatedJouleEnergy         : REAL := 0.0;        (* Instantaneous accumulated weld thermal energy [J] *)
    rEst_DynamicResistanceDerivative    : REAL := 0.0;        (* Rate of change of dynamic nugget resistance [mOhm/ms] *)
    rEst_ElectrodeTipThermalWearIndex   : REAL := 0.0;        (* Normalized electrode tip face pitting/mushroom index [%] *)
    rEst_CMM_DimensionalCapability_Cpk  : REAL := 0.0;        (* Estimated statistical process capability index Cpk [-] *)

    (* === BIT-PACKED ISA-18.2 ALARM & STATUS REGISTERS === *)
    dwAlarmWord1_ISA_CriticalTrips      : DWORD := 16#00000000; (* ISA-18.2 Priority 1 E-Stop & Catastrophic Lock Trips *)
    dwAlarmWord2_ISA_ProcessWarnings    : DWORD := 16#00000000; (* ISA-18.2 Priority 2 Process Dev, HI, LO & ROC Alarms *)
    dwAlarmWord3_ISA_TMR_SensorFaults   : DWORD := 16#00000000; (* ISA-18.2 Priority 3 2oo3 Sensor Discrepancy & Health *)
    dwAlarmWord4_ISA_RobotInterlocks    : DWORD := 16#00000000; (* ISA-18.2 Priority 4 Robot Collision & Tip Dress Alarms *)
    dwFSM_OperationalStatusWord         : DWORD := 16#00000000; (* Bit-packed 14-stage FSM state and diagnostic step *)
    dwDiagnosticsWord                   : DWORD := 16#00000000; (* Metrology quality flags and cycle performance metrics *)
    iCurrentFSM_State                   : INT := 0;             (* Active numeric state identifier of operational FSM *)
    bCellGeneralFaultActive             : BOOL := FALSE;        (* Master summary fault flag active [bool] *)
END_VAR
""")

    # -------------------------------------------------------------------------
    # VAR (INTERNAL VARIABLES)
    # -------------------------------------------------------------------------
    parts.append("""VAR
    (* ============================================================================================== *)
    (* INTERNAL INITIALIZATION AND SCAN VARIABLES                                                     *)
    (* ============================================================================================== *)
    bColdStartInitialized               : BOOL := FALSE;      (* First-scan initialization complete flag [bool] *)
    udiCycleCounter                     : UDINT := 0;         (* BIW cell continuous cycle execution counter *)
    udiTotalSpotsWeldedLifetime         : UDINT := 0;         (* Lifetime cumulative spot weld count counter *)
    udiSpotsWeldedCurrentElectrodeTip   : UDINT := 0;         (* Spots welded since last electrode tip dressing *)
    udiExpulsionIncidentCounter         : UDINT := 0;         (* Lifetime molten metal expulsion event counter *)
    rScanTimeDelta_s                    : REAL := 0.005;      (* Real-time scan interval: 5 milliseconds (0.005 s) *)

    (* ============================================================================================== *)
    (* 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) DISCREPANCY TIMERS & TOLERANCES                          *)
    (* ============================================================================================== *)
    tonTMR_ZT101_DiscrepancyTimer       : TON;                (* Discrepancy debounce timer for Gate LH position *)
    tonTMR_ZT102_DiscrepancyTimer       : TON;                (* Discrepancy debounce timer for Gate RH position *)
    tonTMR_PT201_DiscrepancyTimer       : TON;                (* Discrepancy debounce timer for pneumatic header *)
    tonTMR_PT202_DiscrepancyTimer       : TON;                (* Discrepancy debounce timer for hydraulic clamp *)
    tonTMR_CT301_DiscrepancyTimer       : TON;                (* Discrepancy debounce timer for Robot 1 Rogowski *)
    tonTMR_CT302_DiscrepancyTimer       : TON;                (* Discrepancy debounce timer for Robot 2 Rogowski *)
    tonTMR_WT321_DiscrepancyTimer       : TON;                (* Discrepancy debounce timer for Gun 1 tip force *)
    tonTMR_DT401_DiscrepancyTimer       : TON;                (* Discrepancy debounce timer for CMM A-pillar gap *)
    tonTMR_DT402_DiscrepancyTimer       : TON;                (* Discrepancy debounce timer for CMM A-pillar flush *)
    tonTMR_ST501_DiscrepancyTimer       : TON;                (* Discrepancy debounce timer for skid tachometer *)
    tonTMR_ZT502_DiscrepancyTimer       : TON;                (* Discrepancy debounce timer for skid optical scale *)
    tonTMR_AT601_DiscrepancyTimer       : TON;                (* Discrepancy debounce timer for base accelerometer *)

    rTMR_Tol_GatePosition_mm            : REAL := 0.15;       (* Maximum allowable gate resolver discrepancy [mm] *)
    rTMR_Tol_Pneumatic_bar              : REAL := 0.40;       (* Maximum allowable pneumatic header discrepancy [bar] *)
    rTMR_Tol_Hydraulic_bar              : REAL := 5.00;       (* Maximum allowable hydraulic clamp discrepancy [bar] *)
    rTMR_Tol_Current_kA                 : REAL := 0.50;       (* Maximum allowable weld current discrepancy [kA] *)
    rTMR_Tol_TipForce_kN                : REAL := 0.25;       (* Maximum allowable tip force discrepancy [kN] *)
    rTMR_Tol_CMM_Gap_mm                 : REAL := 0.10;       (* Maximum allowable laser gap discrepancy [mm] *)
    rTMR_Tol_CMM_Flush_mm               : REAL := 0.10;       (* Maximum allowable laser flushness discrepancy [mm] *)
    rTMR_Tol_SkidVel_mms                : REAL := 15.0;       (* Maximum allowable skid speed discrepancy [mm/s] *)
    rTMR_Tol_SkidPos_mm                 : REAL := 1.00;       (* Maximum allowable skid optical position discrepancy [mm] *)
    rTMR_Tol_Vibration_ms2              : REAL := 1.50;       (* Maximum allowable vibration discrepancy [m/s^2] *)
    tTMR_DebounceTime                   : TIME := T#50MS;     (* Discrepancy persistent debounce filter duration *)

    (* TMR Triplet Healthy Flags *)
    bTMR_ZT101_TripletAgreement         : BOOL := TRUE;
    bTMR_ZT102_TripletAgreement         : BOOL := TRUE;
    bTMR_PT201_TripletAgreement         : BOOL := TRUE;
    bTMR_PT202_TripletAgreement         : BOOL := TRUE;
    bTMR_CT301_TripletAgreement         : BOOL := TRUE;
    bTMR_CT302_TripletAgreement         : BOOL := TRUE;
    bTMR_WT321_TripletAgreement         : BOOL := TRUE;
    bTMR_DT401_TripletAgreement         : BOOL := TRUE;
    bTMR_DT402_TripletAgreement         : BOOL := TRUE;
    bTMR_ST501_TripletAgreement         : BOOL := TRUE;
    bTMR_ZT502_TripletAgreement         : BOOL := TRUE;
    bTMR_AT601_TripletAgreement         : BOOL := TRUE;

    (* ============================================================================================== *)
    (* 8x8 MULTIVARIABLE DISCRETE STATE-SPACE CYBER-PHYSICAL MODEL (Ts = 5 ms)                       *)
    (* States x[1..8]:                                                                                *)
    (*   x[1]: Framing Gate LH lock position deviation [mm]                                           *)
    (*   x[2]: Skid conveyor velocity error [mm/s]                                                    *)
    (*   x[3]: Clamping cylinder total force deviation [kN]                                           *)
    (*   x[4]: Spot weld dynamic nugget resistance deviation [mOhm]                                   *)
    (*   x[5]: Secondary weld current deviation [kA]                                                  *)
    (*   x[6]: Electrode tip thermal temperature rise [deg C]                                         *)
    (*   x[7]: Laser CMM gap dimensional deviation [mm]                                               *)
    (*   x[8]: Frame structural vibration acceleration [m/s^2]                                        *)
    (* Controls u[1..8]:                                                                              *)
    (*   u[1]: Framing gate servo speed/torque command [%]                                            *)
    (*   u[2]: Skid roller VFD drive frequency command [Hz]                                           *)
    (*   u[3]: Clamping proportional pressure regulator command [bar]                                 *)
    (*   u[4]: MFDC weld inverter primary duty cycle boost [%]                                        *)
    (*   u[5]: Servo weld gun electrode force command [kN]                                            *)
    (*   u[6]: Tip water chiller coolant proportional valve flow [l/min]                              *)
    (*   u[7]: Framing gate fine piezo/servo micro-trim position [mm]                                 *)
    (*   u[8]: Active structural vibration mass damper force [N]                                      *)
    (* ============================================================================================== *)
    aMatrixA                            : ARRAY[1..8, 1..8] OF REAL; (* Discrete system dynamic state transition matrix *)
    aMatrixB                            : ARRAY[1..8, 1..8] OF REAL; (* Discrete control input distribution matrix *)
    aMatrixC                            : ARRAY[1..8, 1..8] OF REAL; (* Discrete measurement output mapping matrix *)
    aMatrixD                            : ARRAY[1..8, 1..8] OF REAL; (* Discrete feedthrough matrix *)
    aMatrixL                            : ARRAY[1..8, 1..8] OF REAL; (* Luenberger state estimator observer gain matrix *)

    aState_x                            : ARRAY[1..8] OF REAL;       (* Estimated system state vector x[k] *)
    aState_x_pred                       : ARRAY[1..8] OF REAL;       (* One-step predictive prior state vector x_hat[k+1|k] *)
    aControl_u                          : ARRAY[1..8] OF REAL;       (* Applied control input vector u[k] *)
    aControl_u_prev                     : ARRAY[1..8] OF REAL;       (* Previous control input vector u[k-1] for slew limiting *)
    aMeas_y_voted                       : ARRAY[1..8] OF REAL;       (* TMR voted real measurement output vector y[k] *)
    aMeas_y_hat                         : ARRAY[1..8] OF REAL;       (* Observer estimated output vector y_hat[k] *)
    aMeas_error                         : ARRAY[1..8] OF REAL;       (* Measurement innovation residual vector e[k] = y - y_hat *)
    aState_x_ref                        : ARRAY[1..8] OF REAL;       (* Desired state-space trajectory setpoints *)

    (* Control Actuator Box Constraints & Slew Rate Limits *)
    aControl_u_min                      : ARRAY[1..8] OF REAL;       (* Actuator lower saturation bounds *)
    aControl_u_max                      : ARRAY[1..8] OF REAL;       (* Actuator upper saturation bounds *)
    aControl_delta_u_max                : ARRAY[1..8] OF REAL;       (* Actuator maximum rate of change per scan (slew rate) *)

    (* ============================================================================================== *)
    (* RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) OPTIMIZATION VARIABLES                        *)
    (* ============================================================================================== *)
    aWeight_Q                           : ARRAY[1..8] OF REAL;       (* Diagonal state error penalization matrix Q *)
    aWeight_R                           : ARRAY[1..8] OF REAL;       (* Diagonal actuator effort penalization matrix R *)
    aWeight_S                           : ARRAY[1..8] OF REAL;       (* Diagonal actuator slew rate penalization matrix S *)
    aWeight_P                           : ARRAY[1..8] OF REAL;       (* Terminal state error penalization matrix P *)

    aMPC_Trajectory_x                   : ARRAY[1..5, 1..8] OF REAL; (* State trajectory predictions over horizon Np = 5 *)
    aMPC_Trajectory_u                   : ARRAY[1..5, 1..8] OF REAL; (* Control moves over prediction horizon *)
    aMPC_Gradient_g                     : ARRAY[1..8] OF REAL;       (* Projected gradient descent cost derivative vector *)
    rMPC_StepSize_alpha                 : REAL := 0.045;             (* Projected gradient descent step size *)
    iMPC_MaxIterations                  : INT := 6;                  (* Optimization iterations per deterministic scan *)
    rMPC_CostTotal                      : REAL := 0.0;               (* Evaluated quadratic functional cost value *)

    (* ============================================================================================== *)
    (* WELD NUGGET EXPULSION DETECTION & ADAPTIVE COMPENSATION                                        *)
    (* ============================================================================================== *)
    rWeldDynamicResistance_Prev         : REAL := 0.0;        (* Previous scan dynamic resistance for dR/dt calculation *)
    rWeldDynamicResistance_Raw          : REAL := 0.0;        (* Raw ratio of tip voltage to secondary current *)
    rWeldExpulsion_dR_dt_Threshold      : REAL := -0.45;      (* Critical negative resistance collapse rate [mOhm/ms] *)
    rWeldExpulsion_Accel_Threshold      : REAL := 12.5;       (* Acoustic/vibration expulsion confirmation peak [m/s^2] *)
    bMoltenExpulsionDetected            : BOOL := FALSE;      (* Molten steel expulsion violent ejection detected *)
    bExpulsionSpatterLatch              : BOOL := FALSE;      (* Expulsion event latched for quality reporting *)
    udiCurrentWeldStepCount             : UDINT := 0;         (* Millisecond timer elapsed in current active weld *)
    rCurrentWeldHeatEnergy_Joule        : REAL := 0.0;        (* Cumulative electrical energy delivered into nugget [J] *)
    rTipDressingLimitNominal            : REAL := 350.0;      (* Maximum allowable spots before mandatory tip dressing *)

    (* ============================================================================================== *)
    (* 7-SEGMENT JERK-LIMITED S-CURVE SKID TRANSFER TRAJECTORY GENERATOR                             *)
    (* ============================================================================================== *)
    rSCurve_JerkMax                     : REAL := 250.0;      (* Maximum allowable transfer jerk [mm/s^3] *)
    rSCurve_AccelMax                    : REAL := 120.0;      (* Maximum allowable transfer acceleration [mm/s^2] *)
    rSCurve_VelCruise                   : REAL := 350.0;      (* Maximum steady-state transfer velocity [mm/s] *)
    rSCurve_TargetDistance              : REAL := 4200.0;     (* Total infeed transfer travel distance [mm] *)
    rSCurve_CurrentPos                  : REAL := 0.0;        (* Instantaneous S-curve generated target position [mm] *)
    rSCurve_CurrentVel                  : REAL := 0.0;        (* Instantaneous S-curve generated target velocity [mm/s] *)
    rSCurve_CurrentAcc                  : REAL := 0.0;        (* Instantaneous S-curve generated target acceleration [mm/s^2] *)
    iSCurve_Phase                       : INT := 0;           (* S-curve active phase: 0=Idle, 1=J+, 2=A, 3=J-, 4=V, 5=J-, 6=D, 7=J+ *)
    rSCurve_PhaseTimer_s                : REAL := 0.0;        (* Time elapsed in current S-curve kinematic segment *)
    bSCurve_TransferComplete            : BOOL := FALSE;      (* Skid motion profile completed and positioned *)

    (* ============================================================================================== *)
    (* IN-LINE OPTICAL LASER CMM STATISTICAL PROCESS CONTROL ENGINE                                  *)
    (* ============================================================================================== *)
    rCMM_Nominal_A_PillarGap            : REAL := 3.50;       (* Vehicle design nominal gap for A-pillar seam [mm] *)
    rCMM_Tol_UpperSpecLimit_USL         : REAL := 3.85;       (* Upper engineering specification limit USL [mm] *)
    rCMM_Tol_LowerSpecLimit_LSL         : REAL := 3.15;       (* Lower engineering specification limit LSL [mm] *)
    rCMM_SampleMean_Gap                 : REAL := 3.50;       (* Running sample mean for gap dimension [mm] *)
    rCMM_SampleVariance_Gap             : REAL := 0.002;      (* Running sample variance for gap dimension [mm^2] *)
    rCMM_SampleStdDev_Gap               : REAL := 0.045;      (* Running sample standard deviation for gap dimension [mm] *)
    udiCMM_TotalSamplesMeasured         : UDINT := 0;         (* Total BIW bodies measured by optical CMM *)
    bCMM_DimensionalViolation           : BOOL := FALSE;      (* CMM measurement out-of-tolerance reject flag *)

    (* ============================================================================================== *)
    (* 14-STAGE DETERMINISTIC OPERATIONAL FINITE STATE MACHINE (FSM) CONSTANTS                       *)
    (* ============================================================================================== *)
    cSTATE_STANDBY_IDLE                 : INT := 0;           (* Cell quiescent standby, awaiting auto cycle command *)
    cSTATE_SKID_INFEED_INDEX            : INT := 1;           (* Skid indexing into cell with S-curve deceleration *)
    cSTATE_LIFT_CARRY_ROUGH_LOCATE      : INT := 2;           (* Eccentric cam lifter hoists skid onto rough locate cones *)
    cSTATE_FRAMING_GATES_SWING_CLOSE    : INT := 3;           (* LH & RH lateral framing gates traverse inward & toggle lock *)
    cSTATE_SERVO_PINS_ENGAGE            : INT := 4;           (* Precision NC servo pins drive into body master holes *)
    cSTATE_GEOMETRY_CLAMP_SEQUENCE      : INT := 5;           (* 4-Group sequential pneumatic toggle clamping sequence *)
    cSTATE_ROBOT_GRP1_GEO_TACK_WELD     : INT := 6;           (* Robots 1-4 execute primary geometry tack welds *)
    cSTATE_ROBOT_GRP2_RESPOT_WELD       : INT := 7;           (* Robots 5-8 execute structural integrity respot welds *)
    cSTATE_LASER_CMM_GAP_SCAN           : INT := 8;           (* Multi-axis optical laser line scanners traverse body joints *)
    cSTATE_GEOMETRY_UNCLAMP             : INT := 9;           (* Sequential unclamp with anti-stick part hold-down *)
    cSTATE_SERVO_PINS_RETRACT_GATES     : INT := 10;          (* Servo pins retract and framing gates swing open to park *)
    cSTATE_LIFT_CARRY_LOWER_SKID        : INT := 11;          (* Body lowered back down onto roller bed skid carrier *)
    cSTATE_SKID_OUTFEED_TRANSFER        : INT := 12;          (* Skid accelerated out of framing cell to downstream line *)
    cSTATE_EXPULSION_RECOVERY_TIP_DRESS : INT := 13;          (* Molten expulsion recovery and electrode tip dressing *)
    cSTATE_EMERGENCY_ABORT_COLLISION    : INT := 14;          (* Fail-safe emergency freeze and controlled clearance *)

    iFSM_State                          : INT := 0;           (* Master FSM active state pointer *)
    iFSM_PrevState                      : INT := -1;          (* Master FSM previous state pointer *)
    udiFSM_StateStep                    : UDINT := 0;         (* Sub-state sequence step inside active state *)
    tonFSM_StateTimer                   : TON;                (* Dwell timer monitoring active state execution *)
    tFSM_StateTimeoutLimit              : TIME := T#15S;      (* Maximum permissible duration in any active state *)
    bFSM_StateTimedOut                  : BOOL := FALSE;      (* Operational state timeout trip alarm flag *)

    (* Sequential Clamping Sub-Timers *)
    tonClampGroup1_Timer                : TON;
    tonClampGroup2_Timer                : TON;
    tonClampGroup3_Timer                : TON;
    tonClampGroup4_Timer                : TON;

    (* ============================================================================================== *)
    (* ISA-18.2 MULTI-TIER ALARM TRIP POINTS, HYSTERESIS & DEADBANDS                                 *)
    (* ============================================================================================== *)
    (* Framing Gate LH Position Limits *)
    rGateLH_HI_HI_Trip_mm               : REAL := 1050.25;    (* Mechanical hard stop overtravel limit [mm] *)
    rGateLH_HI_Trip_mm                  : REAL := 1050.05;    (* High position deviation warning limit [mm] *)
    rGateLH_LO_Trip_mm                  : REAL := 1049.95;    (* Low position deviation warning limit [mm] *)
    rGateLH_LO_LO_Trip_mm               : REAL := 1049.75;    (* Insufficient gate closure trip limit [mm] *)
    rGateLH_Deadband_mm                 : REAL := 0.02;       (* Alarm hysteresis clearing deadband [mm] *)

    (* Pneumatic Supply Header Limits *)
    rPneumatic_HI_HI_Trip_bar           : REAL := 8.5;        (* Overpressure pneumatic trip [bar] *)
    rPneumatic_HI_Trip_bar              : REAL := 7.5;        (* High pressure pneumatic warning [bar] *)
    rPneumatic_LO_Trip_bar              : REAL := 5.2;        (* Low pressure clamp safety warning [bar] *)
    rPneumatic_LO_LO_Trip_bar           : REAL := 4.5;        (* Critical clamp pressure loss emergency trip [bar] *)
    rPneumatic_Deadband_bar             : REAL := 0.2;        (* Pneumatic alarm clearing deadband [bar] *)

    (* Hydraulic Clamp Toggle Locking Pressure Limits *)
    rHydraulic_HI_HI_Trip_bar           : REAL := 160.0;      (* Hydraulic toggle lock circuit burst risk trip [bar] *)
    rHydraulic_HI_Trip_bar              : REAL := 145.0;      (* Hydraulic pressure high warning [bar] *)
    rHydraulic_LO_Trip_bar              : REAL := 105.0;      (* Hydraulic pressure low warning [bar] *)
    rHydraulic_LO_LO_Trip_bar           : REAL := 90.0;       (* Hydraulic toggle lock force failure trip [bar] *)
    rHydraulic_Deadband_bar             : REAL := 3.0;        (* Hydraulic alarm clearing deadband [bar] *)

    (* Robot 1 Secondary Weld Current Limits *)
    rCurrent_HI_HI_Trip_kA              : REAL := 16.5;       (* Massive overcurrent flash risk trip [kA] *)
    rCurrent_HI_Trip_kA                 : REAL := 14.8;       (* Current high warning [kA] *)
    rCurrent_LO_Trip_kA                 : REAL := 9.2;        (* Current low cold-weld warning [kA] *)
    rCurrent_LO_LO_Trip_kA              : REAL := 7.5;        (* Severe low current unwelded joint trip [kA] *)
    rCurrent_Deadband_kA                : REAL := 0.3;        (* Weld current alarm clearing deadband [kA] *)

    (* Electrode Tip Temperature Limits *)
    rTipTemp_HI_HI_Trip_degC            : REAL := 120.0;      (* Critical electrode softening & mushroom trip [deg C] *)
    rTipTemp_HI_Trip_degC               : REAL := 85.0;       (* High electrode temperature warning [deg C] *)
    rTipTemp_Deadband_degC              : REAL := 4.0;        (* Tip temperature alarm clearing deadband [deg C] *)

    (* Framer Structural Vibration Acceleration Limits *)
    rVibration_HI_HI_Trip_ms2           : REAL := 18.0;       (* Frame severe mechanical shock / collision trip [m/s^2] *)
    rVibration_HI_Trip_ms2              : REAL := 10.0;       (* Excessive harmonic resonance warning [m/s^2] *)
    rVibration_Deadband_ms2             : REAL := 1.0;        (* Vibration alarm clearing deadband [m/s^2] *)

    (* Internal Latched Alarm Flags *)
    bAlarm_GateLH_HI_HI                 : BOOL := FALSE;
    bAlarm_GateLH_HI                    : BOOL := FALSE;
    bAlarm_GateLH_LO                    : BOOL := FALSE;
    bAlarm_GateLH_LO_LO                 : BOOL := FALSE;

    bAlarm_Pneumatic_HI_HI              : BOOL := FALSE;
    bAlarm_Pneumatic_HI                 : BOOL := FALSE;
    bAlarm_Pneumatic_LO                 : BOOL := FALSE;
    bAlarm_Pneumatic_LO_LO              : BOOL := FALSE;

    bAlarm_Hydraulic_HI_HI              : BOOL := FALSE;
    bAlarm_Hydraulic_HI                 : BOOL := FALSE;
    bAlarm_Hydraulic_LO                 : BOOL := FALSE;
    bAlarm_Hydraulic_LO_LO              : BOOL := FALSE;

    bAlarm_Current_HI_HI                : BOOL := FALSE;
    bAlarm_Current_HI                   : BOOL := FALSE;
    bAlarm_Current_LO                   : BOOL := FALSE;
    bAlarm_Current_LO_LO                : BOOL := FALSE;

    bAlarm_TipTemp_HI_HI                : BOOL := FALSE;
    bAlarm_TipTemp_HI                   : BOOL := FALSE;

    bAlarm_Vibration_HI_HI              : BOOL := FALSE;
    bAlarm_Vibration_HI                 : BOOL := FALSE;

    bAlarm_TMR_MajorDiscrepancyTrip     : BOOL := FALSE;
    bAlarm_EStopTripped                 : BOOL := FALSE;
    bAlarm_SafetyFencingBreached        : BOOL := FALSE;
    bAlarm_RobotCollisionZoneInterlock  : BOOL := FALSE;
    bAlarm_MandatoryTipDressRequired    : BOOL := FALSE;

    (* Loop Counters & Scratch Variables *)
    i                                   : INT := 0;
    j                                   : INT := 0;
    k                                   : INT := 0;
    m                                   : INT := 0;
    rTempA                              : REAL := 0.0;
    rTempB                              : REAL := 0.0;
    rTempC                              : REAL := 0.0;
    rMedian                             : REAL := 0.0;
    rSumAx                              : REAL := 0.0;
    rSumBu                              : REAL := 0.0;
    rSumCx                              : REAL := 0.0;
    rSumLerr                            : REAL := 0.0;
    rGradSum                            : REAL := 0.0;
    rCostStep                           : REAL := 0.0;
    rDeltaU                             : REAL := 0.0;
    rAbsDevAB                           : REAL := 0.0;
    rAbsDevBC                           : REAL := 0.0;
    rAbsDevAC                           : REAL := 0.0;
END_VAR
""")

    # -------------------------------------------------------------------------
    # PHASE 0: MODEL MATRICES, CONTROL COEFFICIENTS & COLD START INITIALIZATION
    # -------------------------------------------------------------------------
    parts.append("""
(* ==================================================================================================== *)
(* PHASE 0: MODEL MATRICES, CONTROL COEFFICIENTS & COLD START INITIALIZATION                            *)
(* ==================================================================================================== *)
IF NOT bColdStartInitialized THEN
    (* Discrete State Transition Matrix A (8x8) at Ts = 0.005 s *)
    aMatrixA[1, 1] := 0.9850; aMatrixA[1, 2] := 0.0000; aMatrixA[1, 3] := -0.0012; aMatrixA[1, 4] := 0.0000;
    aMatrixA[1, 5] := 0.0000; aMatrixA[1, 6] := 0.0000; aMatrixA[1, 7] := 0.0025;  aMatrixA[1, 8] := -0.0008;

    aMatrixA[2, 1] := 0.0000; aMatrixA[2, 2] := 0.9450; aMatrixA[2, 3] := 0.0000;  aMatrixA[2, 4] := 0.0000;
    aMatrixA[2, 5] := 0.0000; aMatrixA[2, 6] := 0.0000; aMatrixA[2, 7] := 0.0000;  aMatrixA[2, 8] := 0.0035;

    aMatrixA[3, 1] := 0.0045; aMatrixA[3, 2] := 0.0000; aMatrixA[3, 3] := 0.9620;  aMatrixA[3, 4] := 0.0000;
    aMatrixA[3, 5] := 0.0000; aMatrixA[3, 6] := 0.0000; aMatrixA[3, 7] := -0.0050; aMatrixA[3, 8] := -0.0015;

    aMatrixA[4, 1] := 0.0000; aMatrixA[4, 2] := 0.0000; aMatrixA[4, 3] := -0.0085; aMatrixA[4, 4] := 0.8200;
    aMatrixA[4, 5] := -0.0150; aMatrixA[4, 6] := 0.0065; aMatrixA[4, 7] := 0.0000; aMatrixA[4, 8] := 0.0000;

    aMatrixA[5, 1] := 0.0000; aMatrixA[5, 2] := 0.0000; aMatrixA[5, 3] := 0.0000;  aMatrixA[5, 4] := -0.0450;
    aMatrixA[5, 5] := 0.8950; aMatrixA[5, 6] := -0.0020; aMatrixA[5, 7] := 0.0000; aMatrixA[5, 8] := 0.0000;

    aMatrixA[6, 1] := 0.0000; aMatrixA[6, 2] := 0.0000; aMatrixA[6, 3] := 0.0000;  aMatrixA[6, 4] := 0.0350;
    aMatrixA[6, 5] := 0.0820; aMatrixA[6, 6] := 0.9780; aMatrixA[6, 7] := 0.0000;  aMatrixA[6, 8] := 0.0000;

    aMatrixA[7, 1] := 0.0520; aMatrixA[7, 2] := 0.0000; aMatrixA[7, 3] := -0.0125; aMatrixA[7, 4] := 0.0000;
    aMatrixA[7, 5] := 0.0000; aMatrixA[7, 6] := 0.0042; aMatrixA[7, 7] := 0.9910;  aMatrixA[7, 8] := 0.0018;

    aMatrixA[8, 1] := -0.0210; aMatrixA[8, 2] := 0.0150; aMatrixA[8, 3] := 0.0080; aMatrixA[8, 4] := 0.0000;
    aMatrixA[8, 5] := 0.0120; aMatrixA[8, 6] := 0.0000; aMatrixA[8, 7] := 0.0000;  aMatrixA[8, 8] := 0.7250;

    (* Discrete Input Matrix B (8x8) *)
    aMatrixB[1, 1] := 0.0450; aMatrixB[1, 2] := 0.0000; aMatrixB[1, 3] := 0.0000;  aMatrixB[1, 4] := 0.0000;
    aMatrixB[1, 5] := 0.0000; aMatrixB[1, 6] := 0.0000; aMatrixB[1, 7] := 0.0120;  aMatrixB[1, 8] := 0.0000;

    aMatrixB[2, 1] := 0.0000; aMatrixB[2, 2] := 0.1250; aMatrixB[2, 3] := 0.0000;  aMatrixB[2, 4] := 0.0000;
    aMatrixB[2, 5] := 0.0000; aMatrixB[2, 6] := 0.0000; aMatrixB[2, 7] := 0.0000;  aMatrixB[2, 8] := 0.0000;

    aMatrixB[3, 1] := 0.0000; aMatrixB[3, 2] := 0.0000; aMatrixB[3, 3] := 0.0850;  aMatrixB[3, 4] := 0.0000;
    aMatrixB[3, 5] := 0.0220; aMatrixB[3, 6] := 0.0000; aMatrixB[3, 7] := 0.0000;  aMatrixB[3, 8] := 0.0000;

    aMatrixB[4, 1] := 0.0000; aMatrixB[4, 2] := 0.0000; aMatrixB[4, 3] := 0.0000;  aMatrixB[4, 4] := -0.0350;
    aMatrixB[4, 5] := -0.0580; aMatrixB[4, 6] := 0.0000; aMatrixB[4, 7] := 0.0000; aMatrixB[4, 8] := 0.0000;

    aMatrixB[5, 1] := 0.0000; aMatrixB[5, 2] := 0.0000; aMatrixB[5, 3] := 0.0000;  aMatrixB[5, 4] := 0.1650;
    aMatrixB[5, 5] := 0.0050; aMatrixB[5, 6] := 0.0000; aMatrixB[5, 7] := 0.0000;  aMatrixB[5, 8] := 0.0000;

    aMatrixB[6, 1] := 0.0000; aMatrixB[6, 2] := 0.0000; aMatrixB[6, 3] := 0.0000;  aMatrixB[6, 4] := 0.0420;
    aMatrixB[6, 5] := 0.0000; aMatrixB[6, 6] := -0.0750; aMatrixB[6, 7] := 0.0000; aMatrixB[6, 8] := 0.0000;

    aMatrixB[7, 1] := 0.0080; aMatrixB[7, 2] := 0.0000; aMatrixB[7, 3] := -0.0150; aMatrixB[7, 4] := 0.0000;
    aMatrixB[7, 5] := 0.0000; aMatrixB[7, 6] := 0.0000; aMatrixB[7, 7] := 0.0350;  aMatrixB[7, 8] := 0.0000;

    aMatrixB[8, 1] := 0.0150; aMatrixB[8, 2] := 0.0220; aMatrixB[8, 3] := 0.0120;  aMatrixB[8, 4] := 0.0180;
    aMatrixB[8, 5] := 0.0000; aMatrixB[8, 6] := 0.0000; aMatrixB[8, 7] := 0.0000;  aMatrixB[8, 8] := -0.0950;

    (* Discrete Measurement Matrix C (8x8) *)
    FOR i := 1 TO 8 DO
        FOR j := 1 TO 8 DO
            IF i = j THEN
                aMatrixC[i, j] := 1.0000;
            ELSE
                aMatrixC[i, j] := 0.0000;
            END_IF;
            aMatrixD[i, j] := 0.0000;
        END_FOR;
    END_FOR;

    (* Luenberger Observer Filter Gain Matrix L (8x8) *)
    aMatrixL[1, 1] := 0.2200; aMatrixL[1, 2] := 0.0000; aMatrixL[1, 3] := 0.0015;  aMatrixL[1, 4] := 0.0000;
    aMatrixL[1, 5] := 0.0000; aMatrixL[1, 6] := 0.0000; aMatrixL[1, 7] := 0.0150;  aMatrixL[1, 8] := 0.0000;

    aMatrixL[2, 1] := 0.0000; aMatrixL[2, 2] := 0.3100; aMatrixL[2, 3] := 0.0000;  aMatrixL[2, 4] := 0.0000;
    aMatrixL[2, 5] := 0.0000; aMatrixL[2, 6] := 0.0000; aMatrixL[2, 7] := 0.0000;  aMatrixL[2, 8] := 0.0080;

    aMatrixL[3, 1] := 0.0020; aMatrixL[3, 2] := 0.0000; aMatrixL[3, 3] := 0.2600;  aMatrixL[3, 4] := 0.0000;
    aMatrixL[3, 5] := 0.0000; aMatrixL[3, 6] := 0.0000; aMatrixL[3, 7] := 0.0120;  aMatrixL[3, 8] := 0.0000;

    aMatrixL[4, 1] := 0.0000; aMatrixL[4, 2] := 0.0000; aMatrixL[4, 3] := 0.0000;  aMatrixL[4, 4] := 0.4200;
    aMatrixL[4, 5] := 0.0180; aMatrixL[4, 6] := 0.0000; aMatrixL[4, 7] := 0.0000;  aMatrixL[4, 8] := 0.0000;

    aMatrixL[5, 1] := 0.0000; aMatrixL[5, 2] := 0.0000; aMatrixL[5, 3] := 0.0000;  aMatrixL[5, 4] := 0.0250;
    aMatrixL[5, 5] := 0.3800; aMatrixL[5, 6] := 0.0000; aMatrixL[5, 7] := 0.0000;  aMatrixL[5, 8] := 0.0000;

    aMatrixL[6, 1] := 0.0000; aMatrixL[6, 2] := 0.0000; aMatrixL[6, 3] := 0.0000;  aMatrixL[6, 4] := 0.0000;
    aMatrixL[6, 5] := 0.0150; aMatrixL[6, 6] := 0.2400; aMatrixL[6, 7] := 0.0000;  aMatrixL[6, 8] := 0.0000;

    aMatrixL[7, 1] := 0.0180; aMatrixL[7, 2] := 0.0000; aMatrixL[7, 3] := 0.0050;  aMatrixL[7, 4] := 0.0000;
    aMatrixL[7, 5] := 0.0000; aMatrixL[7, 6] := 0.0000; aMatrixL[7, 7] := 0.2800;  aMatrixL[7, 8] := 0.0000;

    aMatrixL[8, 1] := 0.0000; aMatrixL[8, 2] := 0.0120; aMatrixL[8, 3] := 0.0000;  aMatrixL[8, 4] := 0.0000;
    aMatrixL[8, 5] := 0.0000; aMatrixL[8, 6] := 0.0000; aMatrixL[8, 7] := 0.0000;  aMatrixL[8, 8] := 0.3500;

    (* MPC Quadratic Weights *)
    aWeight_Q[1] := 180.0; (* Gate positioning penalty *)
    aWeight_Q[2] := 25.0;  (* Skid velocity tracking penalty *)
    aWeight_Q[3] := 45.0;  (* Clamping force penalty *)
    aWeight_Q[4] := 120.0; (* Nugget resistance deviation penalty *)
    aWeight_Q[5] := 85.0;  (* Secondary weld current penalty *)
    aWeight_Q[6] := 15.0;  (* Electrode temperature rise penalty *)
    aWeight_Q[7] := 220.0; (* Laser CMM dimensional gap penalty *)
    aWeight_Q[8] := 60.0;  (* Structural vibration penalty *)

    aWeight_R[1] := 1.50;  (* Gate servo actuator effort penalty *)
    aWeight_R[2] := 0.80;  (* Roller VFD effort penalty *)
    aWeight_R[3] := 0.95;  (* Clamp proportional valve effort penalty *)
    aWeight_R[4] := 2.20;  (* MFDC duty cycle effort penalty *)
    aWeight_R[5] := 1.80;  (* Servo gun tip force effort penalty *)
    aWeight_R[6] := 0.40;  (* Tip chiller valve effort penalty *)
    aWeight_R[7] := 3.50;  (* Gate piezo fine trim effort penalty *)
    aWeight_R[8] := 0.65;  (* Active mass damper effort penalty *)

    aWeight_S[1] := 4.50;  (* Slew rate penalty Gate servo *)
    aWeight_S[2] := 2.50;  (* Slew rate penalty Roller VFD *)
    aWeight_S[3] := 3.20;  (* Slew rate penalty Clamp valve *)
    aWeight_S[4] := 6.50;  (* Slew rate penalty MFDC inverter *)
    aWeight_S[5] := 5.00;  (* Slew rate penalty Servo tip force *)
    aWeight_S[6] := 1.20;  (* Slew rate penalty Tip chiller *)
    aWeight_S[7] := 8.00;  (* Slew rate penalty Piezo trim *)
    aWeight_S[8] := 1.80;  (* Slew rate penalty Damper *)

    FOR i := 1 TO 8 DO
        aWeight_P[i] := aWeight_Q[i] * 2.5; (* Terminal cost scaling *)
        aState_x[i] := 0.0;
        aState_x_pred[i] := 0.0;
        aControl_u[i] := 0.0;
        aControl_u_prev[i] := 0.0;
        aState_x_ref[i] := 0.0;
    END_FOR;

    (* Actuator Box Constraints *)
    aControl_u_min[1] := -100.0; aControl_u_max[1] := 100.0; aControl_delta_u_max[1] := 12.0; (* Gate servo [%] *)
    aControl_u_min[2] := 0.0;    aControl_u_max[2] := 60.0;  aControl_delta_u_max[2] := 5.0;  (* Roller VFD [Hz] *)
    aControl_u_min[3] := 0.0;    aControl_u_max[3] := 8.0;   aControl_delta_u_max[3] := 1.5;  (* Clamp prop [bar] *)
    aControl_u_min[4] := -25.0;  aControl_u_max[4] := 25.0;  aControl_delta_u_max[4] := 8.0;  (* MFDC duty trim [%] *)
    aControl_u_min[5] := 1.5;    aControl_u_max[5] := 6.0;   aControl_delta_u_max[5] := 0.8;  (* Gun tip force [kN] *)
    aControl_u_min[6] := 0.0;    aControl_u_max[6] := 25.0;  aControl_delta_u_max[6] := 4.0;  (* Chiller flow [l/min] *)
    aControl_u_min[7] := -0.50;  aControl_u_max[7] := 0.50;  aControl_delta_u_max[7] := 0.05; (* Piezo trim [mm] *)
    aControl_u_min[8] := -500.0; aControl_u_max[8] := 500.0; aControl_delta_u_max[8] := 150.0;(* Damper force [N] *)

    bColdStartInitialized := TRUE;
END_IF;
""")

    # -------------------------------------------------------------------------
    # PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING ENGINES
    # -------------------------------------------------------------------------
    parts.append("""
(* ==================================================================================================== *)
(* PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING ENGINES                                  *)
(* ==================================================================================================== *)

(* TRIPLET 1: FRAMING GATE LH POSITION RESOLVER (ZT_101A/B/C) *)
rAbsDevAB := ABS(ZT_FRAMING_GATE_LH_POS_101A - ZT_FRAMING_GATE_LH_POS_101B);
rAbsDevBC := ABS(ZT_FRAMING_GATE_LH_POS_101B - ZT_FRAMING_GATE_LH_POS_101C);
rAbsDevAC := ABS(ZT_FRAMING_GATE_LH_POS_101A - ZT_FRAMING_GATE_LH_POS_101C);

tonTMR_ZT101_DiscrepancyTimer(IN := ((rAbsDevAB > rTMR_Tol_GatePosition_mm) OR
                                     (rAbsDevBC > rTMR_Tol_GatePosition_mm) OR
                                     (rAbsDevAC > rTMR_Tol_GatePosition_mm)),
                              PT := tTMR_DebounceTime);

IF tonTMR_ZT101_DiscrepancyTimer.Q THEN
    bTMR_ZT101_TripletAgreement := FALSE;
    dwAlarmWord3_ISA_TMR_SensorFaults := dwAlarmWord3_ISA_TMR_SensorFaults OR 16#00000001;
ELSE
    bTMR_ZT101_TripletAgreement := TRUE;
    dwAlarmWord3_ISA_TMR_SensorFaults := dwAlarmWord3_ISA_TMR_SensorFaults AND 16#FFFFFFFE;
END_IF;

IF bStatus_ZT_101A_Healthy AND bStatus_ZT_101B_Healthy AND bStatus_ZT_101C_Healthy THEN
    (* Full 2oo3 Median Voting *)
    rTempA := ZT_FRAMING_GATE_LH_POS_101A;
    rTempB := ZT_FRAMING_GATE_LH_POS_101B;
    rTempC := ZT_FRAMING_GATE_LH_POS_101C;
    IF (rTempA >= rTempB AND rTempA <= rTempC) OR (rTempA >= rTempC AND rTempA <= rTempB) THEN
        rVoted_GateLH_Position := rTempA;
    ELSE
        IF (rTempB >= rTempA AND rTempB <= rTempC) OR (rTempB >= rTempC AND rTempB <= rTempA) THEN
            rVoted_GateLH_Position := rTempB;
        ELSE
            rVoted_GateLH_Position := rTempC;
        END_IF;
    END_IF;
ELSE
    (* Degraded 1oo2 or 1oo1 Voting *)
    IF bStatus_ZT_101A_Healthy AND bStatus_ZT_101B_Healthy THEN
        rVoted_GateLH_Position := (ZT_FRAMING_GATE_LH_POS_101A + ZT_FRAMING_GATE_LH_POS_101B) * 0.5;
    ELSE
        IF bStatus_ZT_101B_Healthy AND bStatus_ZT_101C_Healthy THEN
            rVoted_GateLH_Position := (ZT_FRAMING_GATE_LH_POS_101B + ZT_FRAMING_GATE_LH_POS_101C) * 0.5;
        ELSE
            IF bStatus_ZT_101A_Healthy AND bStatus_ZT_101C_Healthy THEN
                rVoted_GateLH_Position := (ZT_FRAMING_GATE_LH_POS_101A + ZT_FRAMING_GATE_LH_POS_101C) * 0.5;
            ELSE
                IF bStatus_ZT_101A_Healthy THEN
                    rVoted_GateLH_Position := ZT_FRAMING_GATE_LH_POS_101A;
                ELSE
                    IF bStatus_ZT_101B_Healthy THEN
                        rVoted_GateLH_Position := ZT_FRAMING_GATE_LH_POS_101B;
                    ELSE
                        IF bStatus_ZT_101C_Healthy THEN
                            rVoted_GateLH_Position := ZT_FRAMING_GATE_LH_POS_101C;
                        ELSE
                            rVoted_GateLH_Position := 0.0;
                            bAlarm_TMR_MajorDiscrepancyTrip := TRUE;
                        END_IF;
                    END_IF;
                END_IF;
            END_IF;
        END_IF;
    END_IF;
END_IF;

(* TRIPLET 2: FRAMING GATE RH POSITION RESOLVER (ZT_102A/B/C) *)
rAbsDevAB := ABS(ZT_FRAMING_GATE_RH_POS_102A - ZT_FRAMING_GATE_RH_POS_102B);
rAbsDevBC := ABS(ZT_FRAMING_GATE_RH_POS_102B - ZT_FRAMING_GATE_RH_POS_102C);
rAbsDevAC := ABS(ZT_FRAMING_GATE_RH_POS_102A - ZT_FRAMING_GATE_RH_POS_102C);

tonTMR_ZT102_DiscrepancyTimer(IN := ((rAbsDevAB > rTMR_Tol_GatePosition_mm) OR
                                     (rAbsDevBC > rTMR_Tol_GatePosition_mm) OR
                                     (rAbsDevAC > rTMR_Tol_GatePosition_mm)),
                              PT := tTMR_DebounceTime);

IF tonTMR_ZT102_DiscrepancyTimer.Q THEN
    bTMR_ZT102_TripletAgreement := FALSE;
    dwAlarmWord3_ISA_TMR_SensorFaults := dwAlarmWord3_ISA_TMR_SensorFaults OR 16#00000002;
ELSE
    bTMR_ZT102_TripletAgreement := TRUE;
    dwAlarmWord3_ISA_TMR_SensorFaults := dwAlarmWord3_ISA_TMR_SensorFaults AND 16#FFFFFFFD;
END_IF;

IF bStatus_ZT_102A_Healthy AND bStatus_ZT_102B_Healthy AND bStatus_ZT_102C_Healthy THEN
    rTempA := ZT_FRAMING_GATE_RH_POS_102A;
    rTempB := ZT_FRAMING_GATE_RH_POS_102B;
    rTempC := ZT_FRAMING_GATE_RH_POS_102C;
    IF (rTempA >= rTempB AND rTempA <= rTempC) OR (rTempA >= rTempC AND rTempA <= rTempB) THEN
        rVoted_GateRH_Position := rTempA;
    ELSE
        IF (rTempB >= rTempA AND rTempB <= rTempC) OR (rTempB >= rTempC AND rTempB <= rTempA) THEN
            rVoted_GateRH_Position := rTempB;
        ELSE
            rVoted_GateRH_Position := rTempC;
        END_IF;
    END_IF;
ELSE
    IF bStatus_ZT_102A_Healthy AND bStatus_ZT_102B_Healthy THEN
        rVoted_GateRH_Position := (ZT_FRAMING_GATE_RH_POS_102A + ZT_FRAMING_GATE_RH_POS_102B) * 0.5;
    ELSE
        IF bStatus_ZT_102B_Healthy AND bStatus_ZT_102C_Healthy THEN
            rVoted_GateRH_Position := (ZT_FRAMING_GATE_RH_POS_102B + ZT_FRAMING_GATE_RH_POS_102C) * 0.5;
        ELSE
            IF bStatus_ZT_102A_Healthy AND bStatus_ZT_102C_Healthy THEN
                rVoted_GateRH_Position := (ZT_FRAMING_GATE_RH_POS_102A + ZT_FRAMING_GATE_RH_POS_102C) * 0.5;
            ELSE
                IF bStatus_ZT_102A_Healthy THEN
                    rVoted_GateRH_Position := ZT_FRAMING_GATE_RH_POS_102A;
                ELSE
                    IF bStatus_ZT_102B_Healthy THEN
                        rVoted_GateRH_Position := ZT_FRAMING_GATE_RH_POS_102B;
                    ELSE
                        IF bStatus_ZT_102C_Healthy THEN
                            rVoted_GateRH_Position := ZT_FRAMING_GATE_RH_POS_102C;
                        ELSE
                            rVoted_GateRH_Position := 0.0;
                            bAlarm_TMR_MajorDiscrepancyTrip := TRUE;
                        END_IF;
                    END_IF;
                END_IF;
            END_IF;
        END_IF;
    END_IF;
END_IF;

(* TRIPLET 3: PNEUMATIC MAIN HEADER PRESSURE (PT_201A/B/C) *)
rAbsDevAB := ABS(PT_PNEUMATIC_MAIN_HEADER_201A - PT_PNEUMATIC_MAIN_HEADER_201B);
rAbsDevBC := ABS(PT_PNEUMATIC_MAIN_HEADER_201B - PT_PNEUMATIC_MAIN_HEADER_201C);
rAbsDevAC := ABS(PT_PNEUMATIC_MAIN_HEADER_201A - PT_PNEUMATIC_MAIN_HEADER_201C);

tonTMR_PT201_DiscrepancyTimer(IN := ((rAbsDevAB > rTMR_Tol_Pneumatic_bar) OR
                                     (rAbsDevBC > rTMR_Tol_Pneumatic_bar) OR
                                     (rAbsDevAC > rTMR_Tol_Pneumatic_bar)),
                              PT := tTMR_DebounceTime);

IF tonTMR_PT201_DiscrepancyTimer.Q THEN
    bTMR_PT201_TripletAgreement := FALSE;
    dwAlarmWord3_ISA_TMR_SensorFaults := dwAlarmWord3_ISA_TMR_SensorFaults OR 16#00000004;
ELSE
    bTMR_PT201_TripletAgreement := TRUE;
    dwAlarmWord3_ISA_TMR_SensorFaults := dwAlarmWord3_ISA_TMR_SensorFaults AND 16#FFFFFFFB;
END_IF;

IF bStatus_PT_201A_Healthy AND bStatus_PT_201B_Healthy AND bStatus_PT_201C_Healthy THEN
    rTempA := PT_PNEUMATIC_MAIN_HEADER_201A;
    rTempB := PT_PNEUMATIC_MAIN_HEADER_201B;
    rTempC := PT_PNEUMATIC_MAIN_HEADER_201C;
    IF (rTempA >= rTempB AND rTempA <= rTempC) OR (rTempA >= rTempC AND rTempA <= rTempB) THEN
        rVoted_PneumaticHeaderPressure := rTempA;
    ELSE
        IF (rTempB >= rTempA AND rTempB <= rTempC) OR (rTempB >= rTempC AND rTempB <= rTempA) THEN
            rVoted_PneumaticHeaderPressure := rTempB;
        ELSE
            rVoted_PneumaticHeaderPressure := rTempC;
        END_IF;
    END_IF;
ELSE
    IF bStatus_PT_201A_Healthy AND bStatus_PT_201B_Healthy THEN
        rVoted_PneumaticHeaderPressure := (PT_PNEUMATIC_MAIN_HEADER_201A + PT_PNEUMATIC_MAIN_HEADER_201B) * 0.5;
    ELSE
        IF bStatus_PT_201B_Healthy AND bStatus_PT_201C_Healthy THEN
            rVoted_PneumaticHeaderPressure := (PT_PNEUMATIC_MAIN_HEADER_201B + PT_PNEUMATIC_MAIN_HEADER_201C) * 0.5;
        ELSE
            IF bStatus_PT_201A_Healthy AND bStatus_PT_201C_Healthy THEN
                rVoted_PneumaticHeaderPressure := (PT_PNEUMATIC_MAIN_HEADER_201A + PT_PNEUMATIC_MAIN_HEADER_201C) * 0.5;
            ELSE
                IF bStatus_PT_201A_Healthy THEN
                    rVoted_PneumaticHeaderPressure := PT_PNEUMATIC_MAIN_HEADER_201A;
                ELSE
                    IF bStatus_PT_201B_Healthy THEN
                        rVoted_PneumaticHeaderPressure := PT_PNEUMATIC_MAIN_HEADER_201B;
                    ELSE
                        IF bStatus_PT_201C_Healthy THEN
                            rVoted_PneumaticHeaderPressure := PT_PNEUMATIC_MAIN_HEADER_201C;
                        ELSE
                            rVoted_PneumaticHeaderPressure := 0.0;
                            bAlarm_TMR_MajorDiscrepancyTrip := TRUE;
                        END_IF;
                    END_IF;
                END_IF;
            END_IF;
        END_IF;
    END_IF;
END_IF;

(* TRIPLET 4: HYDRAULIC TOGGLE CLAMP PRESSURE (PT_202A/B/C) *)
rAbsDevAB := ABS(PT_HYD_TOGGLE_CLAMP_PRESS_202A - PT_HYD_TOGGLE_CLAMP_PRESS_202B);
rAbsDevBC := ABS(PT_HYD_TOGGLE_CLAMP_PRESS_202B - PT_HYD_TOGGLE_CLAMP_PRESS_202C);
rAbsDevAC := ABS(PT_HYD_TOGGLE_CLAMP_PRESS_202A - PT_HYD_TOGGLE_CLAMP_PRESS_202C);

tonTMR_PT202_DiscrepancyTimer(IN := ((rAbsDevAB > rTMR_Tol_Hydraulic_bar) OR
                                     (rAbsDevBC > rTMR_Tol_Hydraulic_bar) OR
                                     (rAbsDevAC > rTMR_Tol_Hydraulic_bar)),
                              PT := tTMR_DebounceTime);

IF tonTMR_PT202_DiscrepancyTimer.Q THEN
    bTMR_PT202_TripletAgreement := FALSE;
    dwAlarmWord3_ISA_TMR_SensorFaults := dwAlarmWord3_ISA_TMR_SensorFaults OR 16#00000008;
ELSE
    bTMR_PT202_TripletAgreement := TRUE;
    dwAlarmWord3_ISA_TMR_SensorFaults := dwAlarmWord3_ISA_TMR_SensorFaults AND 16#FFFFFFF7;
END_IF;

IF bStatus_PT_202A_Healthy AND bStatus_PT_202B_Healthy AND bStatus_PT_202C_Healthy THEN
    rTempA := PT_HYD_TOGGLE_CLAMP_PRESS_202A;
    rTempB := PT_HYD_TOGGLE_CLAMP_PRESS_202B;
    rTempC := PT_HYD_TOGGLE_CLAMP_PRESS_202C;
    IF (rTempA >= rTempB AND rTempA <= rTempC) OR (rTempA >= rTempC AND rTempA <= rTempB) THEN
        rVoted_HydraulicTogglePressure := rTempA;
    ELSE
        IF (rTempB >= rTempA AND rTempB <= rTempC) OR (rTempB >= rTempC AND rTempB <= rTempA) THEN
            rVoted_HydraulicTogglePressure := rTempB;
        ELSE
            rVoted_HydraulicTogglePressure := rTempC;
        END_IF;
    END_IF;
ELSE
    IF bStatus_PT_202A_Healthy AND bStatus_PT_202B_Healthy THEN
        rVoted_HydraulicTogglePressure := (PT_HYD_TOGGLE_CLAMP_PRESS_202A + PT_HYD_TOGGLE_CLAMP_PRESS_202B) * 0.5;
    ELSE
        IF bStatus_PT_202B_Healthy AND bStatus_PT_202C_Healthy THEN
            rVoted_HydraulicTogglePressure := (PT_HYD_TOGGLE_CLAMP_PRESS_202B + PT_HYD_TOGGLE_CLAMP_PRESS_202C) * 0.5;
        ELSE
            IF bStatus_PT_202A_Healthy AND bStatus_PT_202C_Healthy THEN
                rVoted_HydraulicTogglePressure := (PT_HYD_TOGGLE_CLAMP_PRESS_202A + PT_HYD_TOGGLE_CLAMP_PRESS_202C) * 0.5;
            ELSE
                IF bStatus_PT_202A_Healthy THEN
                    rVoted_HydraulicTogglePressure := PT_HYD_TOGGLE_CLAMP_PRESS_202A;
                ELSE
                    IF bStatus_PT_202B_Healthy THEN
                        rVoted_HydraulicTogglePressure := PT_HYD_TOGGLE_CLAMP_PRESS_202B;
                    ELSE
                        IF bStatus_PT_202C_Healthy THEN
                            rVoted_HydraulicTogglePressure := PT_HYD_TOGGLE_CLAMP_PRESS_202C;
                        ELSE
                            rVoted_HydraulicTogglePressure := 0.0;
                            bAlarm_TMR_MajorDiscrepancyTrip := TRUE;
                        END_IF;
                    END_IF;
                END_IF;
            END_IF;
        END_IF;
    END_IF;
END_IF;

(* TRIPLET 5: ROBOT 1 MFDC SECONDARY CURRENT ROGOWSKI (CT_301A/B/C) *)
rAbsDevAB := ABS(CT_ROBOT1_WELD_CURRENT_301A - CT_ROBOT1_WELD_CURRENT_301B);
rAbsDevBC := ABS(CT_ROBOT1_WELD_CURRENT_301B - CT_ROBOT1_WELD_CURRENT_301C);
rAbsDevAC := ABS(CT_ROBOT1_WELD_CURRENT_301A - CT_ROBOT1_WELD_CURRENT_301C);

tonTMR_CT301_DiscrepancyTimer(IN := ((rAbsDevAB > rTMR_Tol_Current_kA) OR
                                     (rAbsDevBC > rTMR_Tol_Current_kA) OR
                                     (rAbsDevAC > rTMR_Tol_Current_kA)),
                              PT := tTMR_DebounceTime);

IF tonTMR_CT301_DiscrepancyTimer.Q THEN
    bTMR_CT301_TripletAgreement := FALSE;
    dwAlarmWord3_ISA_TMR_SensorFaults := dwAlarmWord3_ISA_TMR_SensorFaults OR 16#00000010;
ELSE
    bTMR_CT301_TripletAgreement := TRUE;
    dwAlarmWord3_ISA_TMR_SensorFaults := dwAlarmWord3_ISA_TMR_SensorFaults AND 16#FFFFFFEF;
END_IF;

IF bStatus_CT_301A_Healthy AND bStatus_CT_301B_Healthy AND bStatus_CT_301C_Healthy THEN
    rTempA := CT_ROBOT1_WELD_CURRENT_301A;
    rTempB := CT_ROBOT1_WELD_CURRENT_301B;
    rTempC := CT_ROBOT1_WELD_CURRENT_301C;
    IF (rTempA >= rTempB AND rTempA <= rTempC) OR (rTempA >= rTempC AND rTempA <= rTempB) THEN
        rVoted_Robot1_WeldCurrent := rTempA;
    ELSE
        IF (rTempB >= rTempA AND rTempB <= rTempC) OR (rTempB >= rTempC AND rTempB <= rTempA) THEN
            rVoted_Robot1_WeldCurrent := rTempB;
        ELSE
            rVoted_Robot1_WeldCurrent := rTempC;
        END_IF;
    END_IF;
ELSE
    IF bStatus_CT_301A_Healthy AND bStatus_CT_301B_Healthy THEN
        rVoted_Robot1_WeldCurrent := (CT_ROBOT1_WELD_CURRENT_301A + CT_ROBOT1_WELD_CURRENT_301B) * 0.5;
    ELSE
        IF bStatus_CT_301B_Healthy AND bStatus_CT_301C_Healthy THEN
            rVoted_Robot1_WeldCurrent := (CT_ROBOT1_WELD_CURRENT_301B + CT_ROBOT1_WELD_CURRENT_301C) * 0.5;
        ELSE
            IF bStatus_CT_301A_Healthy AND bStatus_CT_301C_Healthy THEN
                rVoted_Robot1_WeldCurrent := (CT_ROBOT1_WELD_CURRENT_301A + CT_ROBOT1_WELD_CURRENT_301C) * 0.5;
            ELSE
                IF bStatus_CT_301A_Healthy THEN
                    rVoted_Robot1_WeldCurrent := CT_ROBOT1_WELD_CURRENT_301A;
                ELSE
                    IF bStatus_CT_301B_Healthy THEN
                        rVoted_Robot1_WeldCurrent := CT_ROBOT1_WELD_CURRENT_301B;
                    ELSE
                        IF bStatus_CT_301C_Healthy THEN
                            rVoted_Robot1_WeldCurrent := CT_ROBOT1_WELD_CURRENT_301C;
                        ELSE
                            rVoted_Robot1_WeldCurrent := 0.0;
                            bAlarm_TMR_MajorDiscrepancyTrip := TRUE;
                        END_IF;
                    END_IF;
                END_IF;
            END_IF;
        END_IF;
    END_IF;
END_IF;

(* TRIPLET 6: ROBOT 2 MFDC SECONDARY CURRENT ROGOWSKI (CT_302A/B/C) *)
rAbsDevAB := ABS(CT_ROBOT2_WELD_CURRENT_302A - CT_ROBOT2_WELD_CURRENT_302B);
rAbsDevBC := ABS(CT_ROBOT2_WELD_CURRENT_302B - CT_ROBOT2_WELD_CURRENT_302C);
rAbsDevAC := ABS(CT_ROBOT2_WELD_CURRENT_302A - CT_ROBOT2_WELD_CURRENT_302C);

tonTMR_CT302_DiscrepancyTimer(IN := ((rAbsDevAB > rTMR_Tol_Current_kA) OR
                                     (rAbsDevBC > rTMR_Tol_Current_kA) OR
                                     (rAbsDevAC > rTMR_Tol_Current_kA)),
                              PT := tTMR_DebounceTime);

IF tonTMR_CT302_DiscrepancyTimer.Q THEN
    bTMR_CT302_TripletAgreement := FALSE;
    dwAlarmWord3_ISA_TMR_SensorFaults := dwAlarmWord3_ISA_TMR_SensorFaults OR 16#00000020;
ELSE
    bTMR_CT302_TripletAgreement := TRUE;
    dwAlarmWord3_ISA_TMR_SensorFaults := dwAlarmWord3_ISA_TMR_SensorFaults AND 16#FFFFFFDF;
END_IF;

IF bStatus_CT_302A_Healthy AND bStatus_CT_302B_Healthy AND bStatus_CT_302C_Healthy THEN
    rTempA := CT_ROBOT2_WELD_CURRENT_302A;
    rTempB := CT_ROBOT2_WELD_CURRENT_302B;
    rTempC := CT_ROBOT2_WELD_CURRENT_302C;
    IF (rTempA >= rTempB AND rTempA <= rTempC) OR (rTempA >= rTempC AND rTempA <= rTempB) THEN
        rVoted_Robot2_WeldCurrent := rTempA;
    ELSE
        IF (rTempB >= rTempA AND rTempB <= rTempC) OR (rTempB >= rTempC AND rTempB <= rTempA) THEN
            rVoted_Robot2_WeldCurrent := rTempB;
        ELSE
            rVoted_Robot2_WeldCurrent := rTempC;
        END_IF;
    END_IF;
ELSE
    IF bStatus_CT_302A_Healthy AND bStatus_CT_302B_Healthy THEN
        rVoted_Robot2_WeldCurrent := (CT_ROBOT2_WELD_CURRENT_302A + CT_ROBOT2_WELD_CURRENT_302B) * 0.5;
    ELSE
        IF bStatus_CT_302B_Healthy AND bStatus_CT_302C_Healthy THEN
            rVoted_Robot2_WeldCurrent := (CT_ROBOT2_WELD_CURRENT_302B + CT_ROBOT2_WELD_CURRENT_302C) * 0.5;
        ELSE
            IF bStatus_CT_302A_Healthy AND bStatus_CT_302C_Healthy THEN
                rVoted_Robot2_WeldCurrent := (CT_ROBOT2_WELD_CURRENT_302A + CT_ROBOT2_WELD_CURRENT_302C) * 0.5;
            ELSE
                IF bStatus_CT_302A_Healthy THEN
                    rVoted_Robot2_WeldCurrent := CT_ROBOT2_WELD_CURRENT_302A;
                ELSE
                    IF bStatus_CT_302B_Healthy THEN
                        rVoted_Robot2_WeldCurrent := CT_ROBOT2_WELD_CURRENT_302B;
                    ELSE
                        IF bStatus_CT_302C_Healthy THEN
                            rVoted_Robot2_WeldCurrent := CT_ROBOT2_WELD_CURRENT_302C;
                        ELSE
                            rVoted_Robot2_WeldCurrent := 0.0;
                            bAlarm_TMR_MajorDiscrepancyTrip := TRUE;
                        END_IF;
                    END_IF;
                END_IF;
            END_IF;
        END_IF;
    END_IF;
END_IF;

(* TRIPLET 7: SERVO WELD GUN 1 TIP CONTACT FORCE (WT_321A/B/C) *)
rAbsDevAB := ABS(WT_GUN1_SERVO_TIP_FORCE_321A - WT_GUN1_SERVO_TIP_FORCE_321B);
rAbsDevBC := ABS(WT_GUN1_SERVO_TIP_FORCE_321B - WT_GUN1_SERVO_TIP_FORCE_321C);
rAbsDevAC := ABS(WT_GUN1_SERVO_TIP_FORCE_321A - WT_GUN1_SERVO_TIP_FORCE_321C);

tonTMR_WT321_DiscrepancyTimer(IN := ((rAbsDevAB > rTMR_Tol_TipForce_kN) OR
                                     (rAbsDevBC > rTMR_Tol_TipForce_kN) OR
                                     (rAbsDevAC > rTMR_Tol_TipForce_kN)),
                              PT := tTMR_DebounceTime);

IF tonTMR_WT321_DiscrepancyTimer.Q THEN
    bTMR_WT321_TripletAgreement := FALSE;
    dwAlarmWord3_ISA_TMR_SensorFaults := dwAlarmWord3_ISA_TMR_SensorFaults OR 16#00000040;
ELSE
    bTMR_WT321_TripletAgreement := TRUE;
    dwAlarmWord3_ISA_TMR_SensorFaults := dwAlarmWord3_ISA_TMR_SensorFaults AND 16#FFFFFFBF;
END_IF;

IF bStatus_WT_321A_Healthy AND bStatus_WT_321B_Healthy AND bStatus_WT_321C_Healthy THEN
    rTempA := WT_GUN1_SERVO_TIP_FORCE_321A;
    rTempB := WT_GUN1_SERVO_TIP_FORCE_321B;
    rTempC := WT_GUN1_SERVO_TIP_FORCE_321C;
    IF (rTempA >= rTempB AND rTempA <= rTempC) OR (rTempA >= rTempC AND rTempA <= rTempB) THEN
        rVoted_Gun1_TipContactForce := rTempA;
    ELSE
        IF (rTempB >= rTempA AND rTempB <= rTempC) OR (rTempB >= rTempC AND rTempB <= rTempA) THEN
            rVoted_Gun1_TipContactForce := rTempB;
        ELSE
            rVoted_Gun1_TipContactForce := rTempC;
        END_IF;
    END_IF;
ELSE
    IF bStatus_WT_321A_Healthy AND bStatus_WT_321B_Healthy THEN
        rVoted_Gun1_TipContactForce := (WT_GUN1_SERVO_TIP_FORCE_321A + WT_GUN1_SERVO_TIP_FORCE_321B) * 0.5;
    ELSE
        IF bStatus_WT_321B_Healthy AND bStatus_WT_321C_Healthy THEN
            rVoted_Gun1_TipContactForce := (WT_GUN1_SERVO_TIP_FORCE_321B + WT_GUN1_SERVO_TIP_FORCE_321C) * 0.5;
        ELSE
            IF bStatus_WT_321A_Healthy AND bStatus_WT_321C_Healthy THEN
                rVoted_Gun1_TipContactForce := (WT_GUN1_SERVO_TIP_FORCE_321A + WT_GUN1_SERVO_TIP_FORCE_321C) * 0.5;
            ELSE
                IF bStatus_WT_321A_Healthy THEN
                    rVoted_Gun1_TipContactForce := WT_GUN1_SERVO_TIP_FORCE_321A;
                ELSE
                    IF bStatus_WT_321B_Healthy THEN
                        rVoted_Gun1_TipContactForce := WT_GUN1_SERVO_TIP_FORCE_321B;
                    ELSE
                        IF bStatus_WT_321C_Healthy THEN
                            rVoted_Gun1_TipContactForce := WT_GUN1_SERVO_TIP_FORCE_321C;
                        ELSE
                            rVoted_Gun1_TipContactForce := 0.0;
                            bAlarm_TMR_MajorDiscrepancyTrip := TRUE;
                        END_IF;
                    END_IF;
                END_IF;
            END_IF;
        END_IF;
    END_IF;
END_IF;

(* TRIPLET 8: OPTICAL LASER CMM A-PILLAR GAP SENSOR (DT_401A/B/C) *)
rAbsDevAB := ABS(DT_LASER_CMM_GAP_A_PILLAR_401A - DT_LASER_CMM_GAP_A_PILLAR_401B);
rAbsDevBC := ABS(DT_LASER_CMM_GAP_A_PILLAR_401B - DT_LASER_CMM_GAP_A_PILLAR_401C);
rAbsDevAC := ABS(DT_LASER_CMM_GAP_A_PILLAR_401A - DT_LASER_CMM_GAP_A_PILLAR_401C);

tonTMR_DT401_DiscrepancyTimer(IN := ((rAbsDevAB > rTMR_Tol_CMM_Gap_mm) OR
                                     (rAbsDevBC > rTMR_Tol_CMM_Gap_mm) OR
                                     (rAbsDevAC > rTMR_Tol_CMM_Gap_mm)),
                              PT := tTMR_DebounceTime);

IF tonTMR_DT401_DiscrepancyTimer.Q THEN
    bTMR_DT401_TripletAgreement := FALSE;
    dwAlarmWord3_ISA_TMR_SensorFaults := dwAlarmWord3_ISA_TMR_SensorFaults OR 16#00000080;
ELSE
    bTMR_DT401_TripletAgreement := TRUE;
    dwAlarmWord3_ISA_TMR_SensorFaults := dwAlarmWord3_ISA_TMR_SensorFaults AND 16#FFFFFF7F;
END_IF;

IF bStatus_DT_401A_Healthy AND bStatus_DT_401B_Healthy AND bStatus_DT_401C_Healthy THEN
    rTempA := DT_LASER_CMM_GAP_A_PILLAR_401A;
    rTempB := DT_LASER_CMM_GAP_A_PILLAR_401B;
    rTempC := DT_LASER_CMM_GAP_A_PILLAR_401C;
    IF (rTempA >= rTempB AND rTempA <= rTempC) OR (rTempA >= rTempC AND rTempA <= rTempB) THEN
        rVoted_LaserCMM_Gap_A_Pillar := rTempA;
    ELSE
        IF (rTempB >= rTempA AND rTempB <= rTempC) OR (rTempB >= rTempC AND rTempB <= rTempA) THEN
            rVoted_LaserCMM_Gap_A_Pillar := rTempB;
        ELSE
            rVoted_LaserCMM_Gap_A_Pillar := rTempC;
        END_IF;
    END_IF;
ELSE
    IF bStatus_DT_401A_Healthy AND bStatus_DT_401B_Healthy THEN
        rVoted_LaserCMM_Gap_A_Pillar := (DT_LASER_CMM_GAP_A_PILLAR_401A + DT_LASER_CMM_GAP_A_PILLAR_401B) * 0.5;
    ELSE
        IF bStatus_DT_401B_Healthy AND bStatus_DT_401C_Healthy THEN
            rVoted_LaserCMM_Gap_A_Pillar := (DT_LASER_CMM_GAP_A_PILLAR_401B + DT_LASER_CMM_GAP_A_PILLAR_401C) * 0.5;
        ELSE
            IF bStatus_DT_401A_Healthy AND bStatus_DT_401C_Healthy THEN
                rVoted_LaserCMM_Gap_A_Pillar := (DT_LASER_CMM_GAP_A_PILLAR_401A + DT_LASER_CMM_GAP_A_PILLAR_401C) * 0.5;
            ELSE
                IF bStatus_DT_401A_Healthy THEN
                    rVoted_LaserCMM_Gap_A_Pillar := DT_LASER_CMM_GAP_A_PILLAR_401A;
                ELSE
                    IF bStatus_DT_401B_Healthy THEN
                        rVoted_LaserCMM_Gap_A_Pillar := DT_LASER_CMM_GAP_A_PILLAR_401B;
                    ELSE
                        IF bStatus_DT_401C_Healthy THEN
                            rVoted_LaserCMM_Gap_A_Pillar := DT_LASER_CMM_GAP_A_PILLAR_401C;
                        ELSE
                            rVoted_LaserCMM_Gap_A_Pillar := 3.50;
                            bAlarm_TMR_MajorDiscrepancyTrip := TRUE;
                        END_IF;
                    END_IF;
                END_IF;
            END_IF;
        END_IF;
    END_IF;
END_IF;

(* TRIPLET 9: OPTICAL LASER CMM A-PILLAR FLUSH SENSOR (DT_402A/B/C) *)
rAbsDevAB := ABS(DT_LASER_CMM_FLUSH_A_PILLAR_402A - DT_LASER_CMM_FLUSH_A_PILLAR_402B);
rAbsDevBC := ABS(DT_LASER_CMM_FLUSH_A_PILLAR_402B - DT_LASER_CMM_FLUSH_A_PILLAR_402C);
rAbsDevAC := ABS(DT_LASER_CMM_FLUSH_A_PILLAR_402A - DT_LASER_CMM_FLUSH_A_PILLAR_402C);

tonTMR_DT402_DiscrepancyTimer(IN := ((rAbsDevAB > rTMR_Tol_CMM_Flush_mm) OR
                                     (rAbsDevBC > rTMR_Tol_CMM_Flush_mm) OR
                                     (rAbsDevAC > rTMR_Tol_CMM_Flush_mm)),
                              PT := tTMR_DebounceTime);

IF tonTMR_DT402_DiscrepancyTimer.Q THEN
    bTMR_DT402_TripletAgreement := FALSE;
    dwAlarmWord3_ISA_TMR_SensorFaults := dwAlarmWord3_ISA_TMR_SensorFaults OR 16#00000100;
ELSE
    bTMR_DT402_TripletAgreement := TRUE;
    dwAlarmWord3_ISA_TMR_SensorFaults := dwAlarmWord3_ISA_TMR_SensorFaults AND 16#FFFFFEFF;
END_IF;

IF bStatus_DT_402A_Healthy AND bStatus_DT_402B_Healthy AND bStatus_DT_402C_Healthy THEN
    rTempA := DT_LASER_CMM_FLUSH_A_PILLAR_402A;
    rTempB := DT_LASER_CMM_FLUSH_A_PILLAR_402B;
    rTempC := DT_LASER_CMM_FLUSH_A_PILLAR_402C;
    IF (rTempA >= rTempB AND rTempA <= rTempC) OR (rTempA >= rTempC AND rTempA <= rTempB) THEN
        rVoted_LaserCMM_Flush_A_Pillar := rTempA;
    ELSE
        IF (rTempB >= rTempA AND rTempB <= rTempC) OR (rTempB >= rTempC AND rTempB <= rTempA) THEN
            rVoted_LaserCMM_Flush_A_Pillar := rTempB;
        ELSE
            rVoted_LaserCMM_Flush_A_Pillar := rTempC;
        END_IF;
    END_IF;
ELSE
    IF bStatus_DT_402A_Healthy AND bStatus_DT_402B_Healthy THEN
        rVoted_LaserCMM_Flush_A_Pillar := (DT_LASER_CMM_FLUSH_A_PILLAR_402A + DT_LASER_CMM_FLUSH_A_PILLAR_402B) * 0.5;
    ELSE
        IF bStatus_DT_402B_Healthy AND bStatus_DT_402C_Healthy THEN
            rVoted_LaserCMM_Flush_A_Pillar := (DT_LASER_CMM_FLUSH_A_PILLAR_402B + DT_LASER_CMM_FLUSH_A_PILLAR_402C) * 0.5;
        ELSE
            IF bStatus_DT_402A_Healthy AND bStatus_DT_402C_Healthy THEN
                rVoted_LaserCMM_Flush_A_Pillar := (DT_LASER_CMM_FLUSH_A_PILLAR_402A + DT_LASER_CMM_FLUSH_A_PILLAR_402C) * 0.5;
            ELSE
                IF bStatus_DT_402A_Healthy THEN
                    rVoted_LaserCMM_Flush_A_Pillar := DT_LASER_CMM_FLUSH_A_PILLAR_402A;
                ELSE
                    IF bStatus_DT_402B_Healthy THEN
                        rVoted_LaserCMM_Flush_A_Pillar := DT_LASER_CMM_FLUSH_A_PILLAR_402B;
                    ELSE
                        IF bStatus_DT_402C_Healthy THEN
                            rVoted_LaserCMM_Flush_A_Pillar := DT_LASER_CMM_FLUSH_A_PILLAR_402C;
                        ELSE
                            rVoted_LaserCMM_Flush_A_Pillar := 0.0;
                            bAlarm_TMR_MajorDiscrepancyTrip := TRUE;
                        END_IF;
                    END_IF;
                END_IF;
            END_IF;
        END_IF;
    END_IF;
END_IF;

(* TRIPLET 10: SKID CONVEYOR VELOCITY TACHOMETER (ST_501A/B/C) *)
rAbsDevAB := ABS(ST_SKID_CONVEYOR_VELOCITY_501A - ST_SKID_CONVEYOR_VELOCITY_501B);
rAbsDevBC := ABS(ST_SKID_CONVEYOR_VELOCITY_501B - ST_SKID_CONVEYOR_VELOCITY_501C);
rAbsDevAC := ABS(ST_SKID_CONVEYOR_VELOCITY_501A - ST_SKID_CONVEYOR_VELOCITY_501C);

tonTMR_ST501_DiscrepancyTimer(IN := ((rAbsDevAB > rTMR_Tol_SkidVel_mms) OR
                                     (rAbsDevBC > rTMR_Tol_SkidVel_mms) OR
                                     (rAbsDevAC > rTMR_Tol_SkidVel_mms)),
                              PT := tTMR_DebounceTime);

IF tonTMR_ST501_DiscrepancyTimer.Q THEN
    bTMR_ST501_TripletAgreement := FALSE;
    dwAlarmWord3_ISA_TMR_SensorFaults := dwAlarmWord3_ISA_TMR_SensorFaults OR 16#00000200;
ELSE
    bTMR_ST501_TripletAgreement := TRUE;
    dwAlarmWord3_ISA_TMR_SensorFaults := dwAlarmWord3_ISA_TMR_SensorFaults AND 16#FFFFFDFF;
END_IF;

IF bStatus_ST_501A_Healthy AND bStatus_ST_501B_Healthy AND bStatus_ST_501C_Healthy THEN
    rTempA := ST_SKID_CONVEYOR_VELOCITY_501A;
    rTempB := ST_SKID_CONVEYOR_VELOCITY_501B;
    rTempC := ST_SKID_CONVEYOR_VELOCITY_501C;
    IF (rTempA >= rTempB AND rTempA <= rTempC) OR (rTempA >= rTempC AND rTempA <= rTempB) THEN
        rVoted_SkidVelocity := rTempA;
    ELSE
        IF (rTempB >= rTempA AND rTempB <= rTempC) OR (rTempB >= rTempC AND rTempB <= rTempA) THEN
            rVoted_SkidVelocity := rTempB;
        ELSE
            rVoted_SkidVelocity := rTempC;
        END_IF;
    END_IF;
ELSE
    IF bStatus_ST_501A_Healthy AND bStatus_ST_501B_Healthy THEN
        rVoted_SkidVelocity := (ST_SKID_CONVEYOR_VELOCITY_501A + ST_SKID_CONVEYOR_VELOCITY_501B) * 0.5;
    ELSE
        IF bStatus_ST_501B_Healthy AND bStatus_ST_501C_Healthy THEN
            rVoted_SkidVelocity := (ST_SKID_CONVEYOR_VELOCITY_501B + ST_SKID_CONVEYOR_VELOCITY_501C) * 0.5;
        ELSE
            IF bStatus_ST_501A_Healthy AND bStatus_ST_501C_Healthy THEN
                rVoted_SkidVelocity := (ST_SKID_CONVEYOR_VELOCITY_501A + ST_SKID_CONVEYOR_VELOCITY_501C) * 0.5;
            ELSE
                IF bStatus_ST_501A_Healthy THEN
                    rVoted_SkidVelocity := ST_SKID_CONVEYOR_VELOCITY_501A;
                ELSE
                    IF bStatus_ST_501B_Healthy THEN
                        rVoted_SkidVelocity := ST_SKID_CONVEYOR_VELOCITY_501B;
                    ELSE
                        IF bStatus_ST_501C_Healthy THEN
                            rVoted_SkidVelocity := ST_SKID_CONVEYOR_VELOCITY_501C;
                        ELSE
                            rVoted_SkidVelocity := 0.0;
                            bAlarm_TMR_MajorDiscrepancyTrip := TRUE;
                        END_IF;
                    END_IF;
                END_IF;
            END_IF;
        END_IF;
    END_IF;
END_IF;

(* TRIPLET 11: SKID ABSOLUTE OPTICAL POSITION SCALE (ZT_502A/B/C) *)
rAbsDevAB := ABS(ZT_SKID_TRANSFER_POS_502A - ZT_SKID_TRANSFER_POS_502B);
rAbsDevBC := ABS(ZT_SKID_TRANSFER_POS_502B - ZT_SKID_TRANSFER_POS_502C);
rAbsDevAC := ABS(ZT_SKID_TRANSFER_POS_502A - ZT_SKID_TRANSFER_POS_502C);

tonTMR_ZT502_DiscrepancyTimer(IN := ((rAbsDevAB > rTMR_Tol_SkidPos_mm) OR
                                     (rAbsDevBC > rTMR_Tol_SkidPos_mm) OR
                                     (rAbsDevAC > rTMR_Tol_SkidPos_mm)),
                              PT := tTMR_DebounceTime);

IF tonTMR_ZT502_DiscrepancyTimer.Q THEN
    bTMR_ZT502_TripletAgreement := FALSE;
    dwAlarmWord3_ISA_TMR_SensorFaults := dwAlarmWord3_ISA_TMR_SensorFaults OR 16#00000400;
ELSE
    bTMR_ZT502_TripletAgreement := TRUE;
    dwAlarmWord3_ISA_TMR_SensorFaults := dwAlarmWord3_ISA_TMR_SensorFaults AND 16#FFFFFBFF;
END_IF;

IF bStatus_ZT_502A_Healthy AND bStatus_ZT_502B_Healthy AND bStatus_ZT_502C_Healthy THEN
    rTempA := ZT_SKID_TRANSFER_POS_502A;
    rTempB := ZT_SKID_TRANSFER_POS_502B;
    rTempC := ZT_SKID_TRANSFER_POS_502C;
    IF (rTempA >= rTempB AND rTempA <= rTempC) OR (rTempA >= rTempC AND rTempA <= rTempB) THEN
        rVoted_SkidTransferPosition := rTempA;
    ELSE
        IF (rTempB >= rTempA AND rTempB <= rTempC) OR (rTempB >= rTempC AND rTempB <= rTempA) THEN
            rVoted_SkidTransferPosition := rTempB;
        ELSE
            rVoted_SkidTransferPosition := rTempC;
        END_IF;
    END_IF;
ELSE
    IF bStatus_ZT_502A_Healthy AND bStatus_ZT_502B_Healthy THEN
        rVoted_SkidTransferPosition := (ZT_SKID_TRANSFER_POS_502A + ZT_SKID_TRANSFER_POS_502B) * 0.5;
    ELSE
        IF bStatus_ZT_502B_Healthy AND bStatus_ZT_502C_Healthy THEN
            rVoted_SkidTransferPosition := (ZT_SKID_TRANSFER_POS_502B + ZT_SKID_TRANSFER_POS_502C) * 0.5;
        ELSE
            IF bStatus_ZT_502A_Healthy AND bStatus_ZT_502C_Healthy THEN
                rVoted_SkidTransferPosition := (ZT_SKID_TRANSFER_POS_502A + ZT_SKID_TRANSFER_POS_502C) * 0.5;
            ELSE
                IF bStatus_ZT_502A_Healthy THEN
                    rVoted_SkidTransferPosition := ZT_SKID_TRANSFER_POS_502A;
                ELSE
                    IF bStatus_ZT_502B_Healthy THEN
                        rVoted_SkidTransferPosition := ZT_SKID_TRANSFER_POS_502B;
                    ELSE
                        IF bStatus_ZT_502C_Healthy THEN
                            rVoted_SkidTransferPosition := ZT_SKID_TRANSFER_POS_502C;
                        ELSE
                            rVoted_SkidTransferPosition := 0.0;
                            bAlarm_TMR_MajorDiscrepancyTrip := TRUE;
                        END_IF;
                    END_IF;
                END_IF;
            END_IF;
        END_IF;
    END_IF;
END_IF;

(* TRIPLET 12: FRAMER BASE VIBRATION ACCELEROMETER (AT_601A/B/C) *)
rAbsDevAB := ABS(AT_FRAME_VIBRATION_ACCEL_601A - AT_FRAME_VIBRATION_ACCEL_601B);
rAbsDevBC := ABS(AT_FRAME_VIBRATION_ACCEL_601B - AT_FRAME_VIBRATION_ACCEL_601C);
rAbsDevAC := ABS(AT_FRAME_VIBRATION_ACCEL_601A - AT_FRAME_VIBRATION_ACCEL_601C);

tonTMR_AT601_DiscrepancyTimer(IN := ((rAbsDevAB > rTMR_Tol_Vibration_ms2) OR
                                     (rAbsDevBC > rTMR_Tol_Vibration_ms2) OR
                                     (rAbsDevAC > rTMR_Tol_Vibration_ms2)),
                              PT := tTMR_DebounceTime);

IF tonTMR_AT601_DiscrepancyTimer.Q THEN
    bTMR_AT601_TripletAgreement := FALSE;
    dwAlarmWord3_ISA_TMR_SensorFaults := dwAlarmWord3_ISA_TMR_SensorFaults OR 16#00000800;
ELSE
    bTMR_AT601_TripletAgreement := TRUE;
    dwAlarmWord3_ISA_TMR_SensorFaults := dwAlarmWord3_ISA_TMR_SensorFaults AND 16#FFFFF7FF;
END_IF;

IF bStatus_AT_601A_Healthy AND bStatus_AT_601B_Healthy AND bStatus_AT_601C_Healthy THEN
    rTempA := AT_FRAME_VIBRATION_ACCEL_601A;
    rTempB := AT_FRAME_VIBRATION_ACCEL_601B;
    rTempC := AT_FRAME_VIBRATION_ACCEL_601C;
    IF (rTempA >= rTempB AND rTempA <= rTempC) OR (rTempA >= rTempC AND rTempA <= rTempB) THEN
        rVoted_FrameVibrationAccel := rTempA;
    ELSE
        IF (rTempB >= rTempA AND rTempB <= rTempC) OR (rTempB >= rTempC AND rTempB <= rTempA) THEN
            rVoted_FrameVibrationAccel := rTempB;
        ELSE
            rVoted_FrameVibrationAccel := rTempC;
        END_IF;
    END_IF;
ELSE
    IF bStatus_AT_601A_Healthy AND bStatus_AT_601B_Healthy THEN
        rVoted_FrameVibrationAccel := (AT_FRAME_VIBRATION_ACCEL_601A + AT_FRAME_VIBRATION_ACCEL_601B) * 0.5;
    ELSE
        IF bStatus_AT_601B_Healthy AND bStatus_AT_601C_Healthy THEN
            rVoted_FrameVibrationAccel := (AT_FRAME_VIBRATION_ACCEL_601B + AT_FRAME_VIBRATION_ACCEL_601C) * 0.5;
        ELSE
            IF bStatus_AT_601A_Healthy AND bStatus_AT_601C_Healthy THEN
                rVoted_FrameVibrationAccel := (AT_FRAME_VIBRATION_ACCEL_601A + AT_FRAME_VIBRATION_ACCEL_601C) * 0.5;
            ELSE
                IF bStatus_AT_601A_Healthy THEN
                    rVoted_FrameVibrationAccel := AT_FRAME_VIBRATION_ACCEL_601A;
                ELSE
                    IF bStatus_AT_601B_Healthy THEN
                        rVoted_FrameVibrationAccel := AT_FRAME_VIBRATION_ACCEL_601B;
                    ELSE
                        IF bStatus_AT_601C_Healthy THEN
                            rVoted_FrameVibrationAccel := AT_FRAME_VIBRATION_ACCEL_601C;
                        ELSE
                            rVoted_FrameVibrationAccel := 0.0;
                            bAlarm_TMR_MajorDiscrepancyTrip := TRUE;
                        END_IF;
                    END_IF;
                END_IF;
            END_IF;
        END_IF;
    END_IF;
END_IF;
""")

    # -------------------------------------------------------------------------
    # PHASE 2: FIRST-PRINCIPLES CYBER-PHYSICAL STATE-SPACE ESTIMATION & OBSERVERS
    # -------------------------------------------------------------------------
    parts.append("""
(* ==================================================================================================== *)
(* PHASE 2: FIRST-PRINCIPLES CYBER-PHYSICAL STATE-SPACE ESTIMATION (x[k+1] = A*x[k] + B*u[k])          *)
(* ==================================================================================================== *)

(* Assemble Voted Measurements into Measurement Vector y[1..8] *)
aMeas_y_voted[1] := rVoted_GateLH_Position - 1050.0; (* Lock deviation from nominal 1050.0 mm *)
aMeas_y_voted[2] := rVoted_SkidVelocity;
aMeas_y_voted[3] := (rVoted_HydraulicTogglePressure * 0.25) + (rVoted_PneumaticHeaderPressure * 1.85); (* Combined force index [kN] *)

(* Spot Weld Dynamic Resistance Physical Observer *)
IF rVoted_Robot1_WeldCurrent > 1.0 THEN
    rWeldDynamicResistance_Raw := (ET_ROBOT1_SECONDARY_VOLT / (rVoted_Robot1_WeldCurrent * 1000.0)) * 1000.0; (* [mOhm] *)
    rEst_NuggetDynamicResistance := (0.85 * rEst_NuggetDynamicResistance) + (0.15 * rWeldDynamicResistance_Raw);
    rEst_DynamicResistanceDerivative := (rEst_NuggetDynamicResistance - rWeldDynamicResistance_Prev) / (rScanTimeDelta_s * 1000.0);
    rWeldDynamicResistance_Prev := rEst_NuggetDynamicResistance;

    (* Joule Energy Accumulation: E = integral(I^2 * R * dt) *)
    rCurrentWeldHeatEnergy_Joule := rCurrentWeldHeatEnergy_Joule +
        ((rVoted_Robot1_WeldCurrent * 1000.0) * (rVoted_Robot1_WeldCurrent * 1000.0) *
         (rEst_NuggetDynamicResistance * 0.001) * rScanTimeDelta_s);
    rEst_AccumulatedJouleEnergy := rCurrentWeldHeatEnergy_Joule;

    (* Dynamic Resistance Deviation from Nominal Baseline (0.12 mOhm) *)
    aMeas_y_voted[4] := rEst_NuggetDynamicResistance - 0.120;
    aMeas_y_voted[5] := rVoted_Robot1_WeldCurrent - 12.0; (* Deviation from 12.0 kA nominal *)

    (* Molten Steel Expulsion Spatter Detection Logic: Sharp dR/dt drop + Vibration spike *)
    IF (rEst_DynamicResistanceDerivative < rWeldExpulsion_dR_dt_Threshold) AND
       (rVoted_FrameVibrationAccel > rWeldExpulsion_Accel_Threshold) THEN
        bMoltenExpulsionDetected := TRUE;
        bExpulsionSpatterLatch := TRUE;
        udiExpulsionIncidentCounter := udiExpulsionIncidentCounter + 1;
        dwDiagnosticsWord := dwDiagnosticsWord OR 16#00000001;
    ELSE
        bMoltenExpulsionDetected := FALSE;
    END_IF;
ELSE
    rWeldDynamicResistance_Prev := 0.120;
    rEst_DynamicResistanceDerivative := 0.0;
    aMeas_y_voted[4] := 0.0;
    aMeas_y_voted[5] := 0.0;
    bMoltenExpulsionDetected := FALSE;
END_IF;

aMeas_y_voted[6] := TT_ROBOT1_ELECTRODE_TEMP - 25.0; (* Temperature rise above ambient 25 deg C *)
aMeas_y_voted[7] := rVoted_LaserCMM_Gap_A_Pillar - rCMM_Nominal_A_PillarGap; (* Deviation from 3.50 mm *)
aMeas_y_voted[8] := rVoted_FrameVibrationAccel;

(* State-Space Observer: Prior State Propagation (x_pred = A*x + B*u) *)
FOR i := 1 TO 8 DO
    rSumAx := 0.0;
    rSumBu := 0.0;
    FOR j := 1 TO 8 DO
        rSumAx := rSumAx + (aMatrixA[i, j] * aState_x[j]);
        rSumBu := rSumBu + (aMatrixB[i, j] * aControl_u[j]);
    END_FOR;
    aState_x_pred[i] := rSumAx + rSumBu;
END_FOR;

(* Output Estimation and Residual Innovation Vector (e = y - C*x_pred) *)
FOR i := 1 TO 8 DO
    rSumCx := 0.0;
    FOR j := 1 TO 8 DO
        rSumCx := rSumCx + (aMatrixC[i, j] * aState_x_pred[j]);
    END_FOR;
    aMeas_y_hat[i] := rSumCx;
    aMeas_error[i] := aMeas_y_voted[i] - aMeas_y_hat[i];
END_FOR;

(* Posterior State Estimation with Luenberger Gain Injection (x = x_pred + L*e) *)
FOR i := 1 TO 8 DO
    rSumLerr := 0.0;
    FOR j := 1 TO 8 DO
        rSumLerr := rSumLerr + (aMatrixL[i, j] * aMeas_error[j]);
    END_FOR;
    aState_x[i] := aState_x_pred[i] + rSumLerr;
END_FOR;

(* Update Real-Time Electrode Tip Thermal Degradation Index *)
rEst_ElectrodeTipThermalWearIndex := (UDINT_TO_REAL(udiSpotsWeldedCurrentElectrodeTip) / rTipDressingLimitNominal) * 100.0;
IF rEst_ElectrodeTipThermalWearIndex >= 100.0 THEN
    bAlarm_MandatoryTipDressRequired := TRUE;
    dwAlarmWord4_ISA_RobotInterlocks := dwAlarmWord4_ISA_RobotInterlocks OR 16#00000001;
ELSE
    bAlarm_MandatoryTipDressRequired := FALSE;
    dwAlarmWord4_ISA_RobotInterlocks := dwAlarmWord4_ISA_RobotInterlocks AND 16#FFFFFFFE;
END_IF;

(* 7-Segment Jerk-Limited S-Curve Kinematic State Generator *)
IF iSCurve_Phase > 0 AND iSCurve_Phase <= 7 THEN
    rSCurve_PhaseTimer_s := rSCurve_PhaseTimer_s + rScanTimeDelta_s;
    CASE iSCurve_Phase OF
        1: (* Phase 1: Jerk ramp-up to max acceleration (+J_max) *)
            rSCurve_CurrentAcc := rSCurve_CurrentAcc + (rSCurve_JerkMax * rScanTimeDelta_s);
            IF rSCurve_CurrentAcc >= rSCurve_AccelMax THEN
                rSCurve_CurrentAcc := rSCurve_AccelMax;
                iSCurve_Phase := 2;
                rSCurve_PhaseTimer_s := 0.0;
            END_IF;
        2: (* Phase 2: Constant acceleration (+A_max) *)
            rSCurve_CurrentVel := rSCurve_CurrentVel + (rSCurve_CurrentAcc * rScanTimeDelta_s);
            IF rSCurve_CurrentVel >= (rSCurve_VelCruise - 25.0) THEN
                iSCurve_Phase := 3;
                rSCurve_PhaseTimer_s := 0.0;
            END_IF;
        3: (* Phase 3: Jerk ramp-down to cruise velocity (-J_max) *)
            rSCurve_CurrentAcc := rSCurve_CurrentAcc - (rSCurve_JerkMax * rScanTimeDelta_s);
            IF rSCurve_CurrentAcc <= 0.0 THEN
                rSCurve_CurrentAcc := 0.0;
                rSCurve_CurrentVel := rSCurve_VelCruise;
                iSCurve_Phase := 4;
                rSCurve_PhaseTimer_s := 0.0;
            END_IF;
        4: (* Phase 4: Constant velocity cruising at V_cruise *)
            IF rSCurve_CurrentPos >= (rSCurve_TargetDistance - 750.0) THEN
                iSCurve_Phase := 5;
                rSCurve_PhaseTimer_s := 0.0;
            END_IF;
        5: (* Phase 5: Jerk ramp-up to max deceleration (-J_max) *)
            rSCurve_CurrentAcc := rSCurve_CurrentAcc - (rSCurve_JerkMax * rScanTimeDelta_s);
            IF rSCurve_CurrentAcc <= -rSCurve_AccelMax THEN
                rSCurve_CurrentAcc := -rSCurve_AccelMax;
                iSCurve_Phase := 6;
                rSCurve_PhaseTimer_s := 0.0;
            END_IF;
        6: (* Phase 6: Constant deceleration (-A_max) *)
            rSCurve_CurrentVel := rSCurve_CurrentVel + (rSCurve_CurrentAcc * rScanTimeDelta_s);
            IF rSCurve_CurrentVel <= 35.0 THEN
                iSCurve_Phase := 7;
                rSCurve_PhaseTimer_s := 0.0;
            END_IF;
        7: (* Phase 7: Jerk ramp-down deceleration to zero landing velocity (+J_max) *)
            rSCurve_CurrentAcc := rSCurve_CurrentAcc + (rSCurve_JerkMax * rScanTimeDelta_s);
            IF rSCurve_CurrentAcc >= 0.0 OR rSCurve_CurrentPos >= rSCurve_TargetDistance THEN
                rSCurve_CurrentAcc := 0.0;
                rSCurve_CurrentVel := 0.0;
                rSCurve_CurrentPos := rSCurve_TargetDistance;
                iSCurve_Phase := 0;
                bSCurve_TransferComplete := TRUE;
            END_IF;
    END_CASE;

    rSCurve_CurrentVel := rSCurve_CurrentVel + (rSCurve_CurrentAcc * rScanTimeDelta_s);
    IF rSCurve_CurrentVel < 0.0 THEN rSCurve_CurrentVel := 0.0; END_IF;
    rSCurve_CurrentPos := rSCurve_CurrentPos + (rSCurve_CurrentVel * rScanTimeDelta_s);
ELSE
    rSCurve_CurrentAcc := 0.0;
    rSCurve_CurrentVel := 0.0;
END_IF;

(* Optical Laser CMM Statistical Capability Engine (Cp / Cpk Tracking) *)
IF bLaserCMM_InspectionComplete AND NOT bCMM_DimensionalViolation THEN
    udiCMM_TotalSamplesMeasured := udiCMM_TotalSamplesMeasured + 1;
    (* Welford Recursive Running Mean and Variance Algorithm *)
    rTempA := rVoted_LaserCMM_Gap_A_Pillar - rCMM_SampleMean_Gap;
    rCMM_SampleMean_Gap := rCMM_SampleMean_Gap + (rTempA / UDINT_TO_REAL(udiCMM_TotalSamplesMeasured));
    rTempB := rVoted_LaserCMM_Gap_A_Pillar - rCMM_SampleMean_Gap;
    rCMM_SampleVariance_Gap := rCMM_SampleVariance_Gap + (rTempA * rTempB);

    IF udiCMM_TotalSamplesMeasured > 2 THEN
        rCMM_SampleStdDev_Gap := SQRT(rCMM_SampleVariance_Gap / UDINT_TO_REAL(udiCMM_TotalSamplesMeasured - 1));
        IF rCMM_SampleStdDev_Gap > 0.0001 THEN
            rTempA := (rCMM_Tol_UpperSpecLimit_USL - rCMM_SampleMean_Gap) / (3.0 * rCMM_SampleStdDev_Gap);
            rTempB := (rCMM_SampleMean_Gap - rCMM_Tol_LowerSpecLimit_LSL) / (3.0 * rCMM_SampleStdDev_Gap);
            IF rTempA < rTempB THEN
                rEst_CMM_DimensionalCapability_Cpk := rTempA;
            ELSE
                rEst_CMM_DimensionalCapability_Cpk := rTempB;
            END_IF;
        ELSE
            rEst_CMM_DimensionalCapability_Cpk := 2.0;
        END_IF;
    END_IF;
END_IF;
""")

    # -------------------------------------------------------------------------
    # PHASE 3: RECEDING-HORIZON MPC OPTIMIZATION WITH PGD & SLEW LIMITS
    # -------------------------------------------------------------------------
    parts.append("""
(* ==================================================================================================== *)
(* PHASE 3: RECEDING-HORIZON MPC OPTIMIZATION WITH PGD & SLEW LIMITS                                     *)
(* ==================================================================================================== *)

(* Initialize Prediction Trajectory from Current Estimated State *)
FOR j := 1 TO 8 DO
    aMPC_Trajectory_x[1, j] := aState_x[j];
    aMPC_Trajectory_u[1, j] := aControl_u[j];
END_FOR;

(* Projected Gradient Descent Iterative Loop (k_iter = 1..6) *)
FOR k := 1 TO iMPC_MaxIterations DO
    (* 1. Forward Rollout of State Trajectory over Np = 5 steps *)
    FOR m := 1 TO 4 DO
        FOR i := 1 TO 8 DO
            rSumAx := 0.0;
            rSumBu := 0.0;
            FOR j := 1 TO 8 DO
                rSumAx := rSumAx + (aMatrixA[i, j] * aMPC_Trajectory_x[m, j]);
                rSumBu := rSumBu + (aMatrixB[i, j] * aMPC_Trajectory_u[m, j]);
            END_FOR;
            aMPC_Trajectory_x[m + 1, i] := rSumAx + rSumBu;
            aMPC_Trajectory_u[m + 1, i] := aMPC_Trajectory_u[m, i];
        END_FOR;
    END_FOR;

    (* 2. Evaluate Cost Gradient with Respect to First Control Move u[0] *)
    FOR j := 1 TO 8 DO
        rGradSum := 0.0;
        (* Actuator Effort and Slew Rate Penalty Gradients *)
        rGradSum := rGradSum + (2.0 * aWeight_R[j] * aMPC_Trajectory_u[1, j]);
        rGradSum := rGradSum + (2.0 * aWeight_S[j] * (aMPC_Trajectory_u[1, j] - aControl_u_prev[j]));

        (* Backpropagated State Error Gradients via B Matrix Mapping *)
        FOR i := 1 TO 8 DO
            rGradSum := rGradSum + (2.0 * aMatrixB[i, j] * aWeight_Q[i] *
                                   (aMPC_Trajectory_x[2, i] - aState_x_ref[i]));
        END_FOR;
        aMPC_Gradient_g[j] := rGradSum;
    END_FOR;

    (* 3. Gradient Descent Step with Actuator Box & Slew Projections *)
    FOR j := 1 TO 8 DO
        rTempA := aMPC_Trajectory_u[1, j] - (rMPC_StepSize_alpha * aMPC_Gradient_g[j]);

        (* Slew Rate Limiter against Previous Cycle Control Move *)
        rDeltaU := rTempA - aControl_u_prev[j];
        IF rDeltaU > aControl_delta_u_max[j] THEN
            rTempA := aControl_u_prev[j] + aControl_delta_u_max[j];
        ELSE
            IF rDeltaU < -aControl_delta_u_max[j] THEN
                rTempA := aControl_u_prev[j] - aControl_delta_u_max[j];
            END_IF;
        END_IF;

        (* Actuator Box Saturation Constraints *)
        IF rTempA > aControl_u_max[j] THEN
            rTempA := aControl_u_max[j];
        ELSE
            IF rTempA < aControl_u_min[j] THEN
                rTempA := aControl_u_min[j];
            END_IF;
        END_IF;

        aMPC_Trajectory_u[1, j] := rTempA;
    END_FOR;
END_FOR;

(* Apply First Optimal Control Input Vector u[k] *)
FOR j := 1 TO 8 DO
    aControl_u_prev[j] := aControl_u[j];
    aControl_u[j] := aMPC_Trajectory_u[1, j];
END_FOR;

(* Evaluate Total Quadratic Functional Cost Value J *)
rMPC_CostTotal := 0.0;
FOR m := 1 TO 5 DO
    FOR j := 1 TO 8 DO
        IF m < 5 THEN
            rMPC_CostTotal := rMPC_CostTotal +
                (aWeight_Q[j] * (aMPC_Trajectory_x[m, j] - aState_x_ref[j]) *
                                (aMPC_Trajectory_x[m, j] - aState_x_ref[j])) +
                (aWeight_R[j] * aMPC_Trajectory_u[m, j] * aMPC_Trajectory_u[m, j]);
        ELSE
            (* Terminal Horizon Penalty P *)
            rMPC_CostTotal := rMPC_CostTotal +
                (aWeight_P[j] * (aMPC_Trajectory_x[m, j] - aState_x_ref[j]) *
                                (aMPC_Trajectory_x[m, j] - aState_x_ref[j]));
        END_IF;
    END_FOR;
END_FOR;

(* Map MPC Optimized Outputs to Physical Actuators *)
rFramingGateLH_ServoSpeedCmd := aControl_u[1];
rFramingGateRH_ServoSpeedCmd := aControl_u[1];
rSkidRollerVFD_FreqCmd       := aControl_u[2];
rPneumaticClampPropValveCmd  := aControl_u[3];
rRobot1_MFDC_DutyCycleBoost  := aControl_u[4];
rRobot2_MFDC_DutyCycleBoost  := aControl_u[4];
rRobot1_TipCoolingFlowModCmd := aControl_u[6];
rRobot2_TipCoolingFlowModCmd := aControl_u[6];
rActiveMassDamperForceCmd    := aControl_u[8];
""")

    # -------------------------------------------------------------------------
    # PHASE 4: 14-STAGE DETERMINISTIC PRODUCTION FINITE STATE MACHINE
    # -------------------------------------------------------------------------
    parts.append("""
(* ==================================================================================================== *)
(* PHASE 4: 14-STAGE DETERMINISTIC PRODUCTION FINITE STATE MACHINE                                       *)
(* ==================================================================================================== *)

(* State Dwell and Timeout Monitor *)
tonFSM_StateTimer(IN := (iFSM_State = iFSM_PrevState), PT := tFSM_StateTimeoutLimit);
IF tonFSM_StateTimer.Q THEN
    bFSM_StateTimedOut := TRUE;
    bAlarm_TMR_MajorDiscrepancyTrip := TRUE;
    dwAlarmWord1_ISA_CriticalTrips := dwAlarmWord1_ISA_CriticalTrips OR 16#00000001;
ELSE
    bFSM_StateTimedOut := FALSE;
END_IF;
iFSM_PrevState := iFSM_State;

(* Emergency Interlock Override Check *)
IF NOT bEmergencyStopCircuitHealthy OR NOT bSafetyFenceZoneInterlocksOk OR bAlarm_TMR_MajorDiscrepancyTrip THEN
    iFSM_State := cSTATE_EMERGENCY_ABORT_COLLISION;
END_IF;

CASE iFSM_State OF

    cSTATE_STANDBY_IDLE:
        (* Cell Quiescent Safe Idle *)
        bCmd_CellSafeHoldActive := FALSE;
        bCmd_CellCycleCompletedPulse := FALSE;
        bCmd_TriggerRobotGrp1_GeoTack := FALSE;
        bCmd_TriggerRobotGrp2_Respot := FALSE;
        bCmd_TriggerLaserCMM_ScanCycle := FALSE;
        aState_x_ref[1] := 0.0;
        aState_x_ref[2] := 0.0;

        IF bSystemEnable AND bAutoCycleStartCmd AND bSkidInfeedZonePresent AND
           bRobot1_AtHome AND bRobot2_AtHome AND bRobot3_AtHome AND bRobot4_AtHome AND
           bRobot5_AtHome AND bRobot6_AtHome AND bRobot7_AtHome AND bRobot8_AtHome THEN
            udiFSM_StateStep := 0;
            iFSM_State := cSTATE_SKID_INFEED_INDEX;
            (* Trigger 7-Segment S-Curve Skid Transfer Profile *)
            iSCurve_Phase := 1;
            rSCurve_PhaseTimer_s := 0.0;
            rSCurve_CurrentPos := 0.0;
            rSCurve_CurrentVel := 0.0;
            bSCurve_TransferComplete := FALSE;
        END_IF;

    cSTATE_SKID_INFEED_INDEX:
        (* Transfer Table S-Curve Deceleration into Geometry Framing Station *)
        aState_x_ref[2] := rSCurve_CurrentVel;
        IF bSCurve_TransferComplete OR (rVoted_SkidTransferPosition >= (rSCurve_TargetDistance - 2.0)) THEN
            aState_x_ref[2] := 0.0;
            aControl_u[2] := 0.0;
            udiFSM_StateStep := 0;
            iFSM_State := cSTATE_LIFT_CARRY_ROUGH_LOCATE;
        END_IF;

    cSTATE_LIFT_CARRY_ROUGH_LOCATE:
        (* Hoist Skid onto Rough Cone Locators (150 mm Vertical Lift) *)
        bCmd_SkidRoughLocateLifterRaise := TRUE;
        bCmd_SkidRoughLocateLifterLower := FALSE;

        IF bSkidRoughLocatePinsRaised THEN
            udiFSM_StateStep := 0;
            iFSM_State := cSTATE_FRAMING_GATES_SWING_CLOSE;
        END_IF;

    cSTATE_FRAMING_GATES_SWING_CLOSE:
        (* Traverse LH and RH Precision Framing Gates Inward with Toggle Locks *)
        aState_x_ref[1] := 0.0; (* Drive gate position to zero error (nominal 1050.0 mm) *)
        IF (ABS(rVoted_GateLH_Position - 1050.0) < 0.25) AND
           (ABS(rVoted_GateRH_Position - 1050.0) < 0.25) THEN
            bCmd_GateLH_ToggleLockEngage := TRUE;
            bCmd_GateRH_ToggleLockEngage := TRUE;

            IF bFramingGateLH_ToggleLocked AND bFramingGateRH_ToggleLocked THEN
                udiFSM_StateStep := 0;
                iFSM_State := cSTATE_SERVO_PINS_ENGAGE;
            END_IF;
        END_IF;

    cSTATE_SERVO_PINS_ENGAGE:
        (* Insert Precision Servo NC Locating Pins into Master Body Datum Holes (< +-0.05 mm) *)
        bCmd_ServoLocatingPinsLH_Advance := TRUE;
        bCmd_ServoLocatingPinsRH_Advance := TRUE;

        IF bServoLocatingPinsLH_Seated AND bServoLocatingPinsRH_Seated THEN
            udiFSM_StateStep := 0;
            iFSM_State := cSTATE_GEOMETRY_CLAMP_SEQUENCE;
        END_IF;

    cSTATE_GEOMETRY_CLAMP_SEQUENCE:
        (* Sequential Multi-Group Clamping to Prevent Residual Stress Distortion *)
        aState_x_ref[3] := 18.5; (* Desired total clamping force index [kN] *)
        CASE udiFSM_StateStep OF
            0: (* Group 1: Underbody Rocker Rail Datum Clamps *)
                bCmd_BodyPartClamps_Close_Grp1 := TRUE;
                tonClampGroup1_Timer(IN := TRUE, PT := T#400MS);
                IF tonClampGroup1_Timer.Q AND bBodyPartClampsClosed_Group1 THEN
                    tonClampGroup1_Timer(IN := FALSE, PT := T#400MS);
                    udiFSM_StateStep := 1;
                END_IF;

            1: (* Group 2: A-Pillar and Cowl Structure Clamps *)
                bCmd_BodyPartClamps_Close_Grp2 := TRUE;
                tonClampGroup2_Timer(IN := TRUE, PT := T#400MS);
                IF tonClampGroup2_Timer.Q AND bBodyPartClampsClosed_Group2 THEN
                    tonClampGroup2_Timer(IN := FALSE, PT := T#400MS);
                    udiFSM_StateStep := 2;
                END_IF;

            2: (* Group 3: B-Pillar and C-Pillar Structural Ring Clamps *)
                bCmd_BodyPartClamps_Close_Grp3 := TRUE;
                tonClampGroup3_Timer(IN := TRUE, PT := T#400MS);
                IF tonClampGroup3_Timer.Q AND bBodyPartClampsClosed_Group3 THEN
                    tonClampGroup3_Timer(IN := FALSE, PT := T#400MS);
                    udiFSM_StateStep := 3;
                END_IF;

            3: (* Group 4: Roof Header and Bow Tacking Clamps *)
                bCmd_BodyPartClamps_Close_Grp4 := TRUE;
                tonClampGroup4_Timer(IN := TRUE, PT := T#400MS);
                IF tonClampGroup4_Timer.Q AND bBodyPartClampsClosed_Group4 THEN
                    tonClampGroup4_Timer(IN := FALSE, PT := T#400MS);
                    udiFSM_StateStep := 0;
                    iFSM_State := cSTATE_ROBOT_GRP1_GEO_TACK_WELD;
                END_IF;
        END_CASE;

    cSTATE_ROBOT_GRP1_GEO_TACK_WELD:
        (* Robots 1 through 4 Execute Critical Geometry Framing Tack Welds *)
        bCmd_TriggerRobotGrp1_GeoTack := TRUE;
        aState_x_ref[4] := 0.0;
        aState_x_ref[5] := 0.0; (* 12.0 kA nominal secondary current tracking *)

        IF bRobotCollisionZoneLH_Clear AND bRobotCollisionZoneRH_Clear THEN
            IF bRobot1_WeldComplete AND bRobot2_WeldComplete AND
               bRobot3_WeldComplete AND bRobot4_WeldComplete THEN
                bCmd_TriggerRobotGrp1_GeoTack := FALSE;
                udiTotalSpotsWeldedLifetime := udiTotalSpotsWeldedLifetime + 32;
                udiSpotsWeldedCurrentElectrodeTip := udiSpotsWeldedCurrentElectrodeTip + 32;

                IF bMoltenExpulsionDetected THEN
                    iFSM_State := cSTATE_EXPULSION_RECOVERY_TIP_DRESS;
                ELSE
                    udiFSM_StateStep := 0;
                    iFSM_State := cSTATE_ROBOT_GRP2_RESPOT_WELD;
                END_IF;
            END_IF;
        ELSE
            bAlarm_RobotCollisionZoneInterlock := TRUE;
        END_IF;

    cSTATE_ROBOT_GRP2_RESPOT_WELD:
        (* Robots 5 through 8 Execute Structural Integrity Respot Welds *)
        bCmd_TriggerRobotGrp2_Respot := TRUE;

        IF bRobot5_WeldComplete AND bRobot6_WeldComplete AND
           bRobot7_WeldComplete AND bRobot8_WeldComplete THEN
            bCmd_TriggerRobotGrp2_Respot := FALSE;
            udiTotalSpotsWeldedLifetime := udiTotalSpotsWeldedLifetime + 48;
            udiSpotsWeldedCurrentElectrodeTip := udiSpotsWeldedCurrentElectrodeTip + 48;

            IF bDryRunModeEnable THEN
                iFSM_State := cSTATE_GEOMETRY_UNCLAMP;
            ELSE
                udiFSM_StateStep := 0;
                iFSM_State := cSTATE_LASER_CMM_GAP_SCAN;
            END_IF;
        END_IF;

    cSTATE_LASER_CMM_GAP_SCAN:
        (* Optical Laser Line Scanner GMM Dimensional Verification *)
        bCmd_TriggerLaserCMM_ScanCycle := TRUE;
        aState_x_ref[7] := 0.0; (* Enforce zero gap dimensional deviation *)

        IF bLaserCMM_InspectionComplete THEN
            bCmd_TriggerLaserCMM_ScanCycle := FALSE;
            IF bLaserCMM_PassStatus AND (rEst_CMM_DimensionalCapability_Cpk >= 1.33) THEN
                bCMM_DimensionalViolation := FALSE;
                udiFSM_StateStep := 0;
                iFSM_State := cSTATE_GEOMETRY_UNCLAMP;
            ELSE
                bCMM_DimensionalViolation := TRUE;
                dwDiagnosticsWord := dwDiagnosticsWord OR 16#00000002;
                udiFSM_StateStep := 0;
                iFSM_State := cSTATE_GEOMETRY_UNCLAMP; (* Gracefully unclamp even on reject *)
            END_IF;
        END_IF;

    cSTATE_GEOMETRY_UNCLAMP:
        (* Sequential Clamp Release with Anti-Stick Timing *)
        bCmd_BodyPartClamps_Close_Grp4 := FALSE;
        bCmd_BodyPartClamps_Close_Grp3 := FALSE;
        bCmd_BodyPartClamps_Close_Grp2 := FALSE;
        bCmd_BodyPartClamps_Close_Grp1 := FALSE;

        IF NOT bBodyPartClampsClosed_Group1 AND NOT bBodyPartClampsClosed_Group2 AND
           NOT bBodyPartClampsClosed_Group3 AND NOT bBodyPartClampsClosed_Group4 THEN
            udiFSM_StateStep := 0;
            iFSM_State := cSTATE_SERVO_PINS_RETRACT_GATES;
        END_IF;

    cSTATE_SERVO_PINS_RETRACT_GATES:
        (* Retract Servo Locating Pins and Open Lateral Framing Gates *)
        bCmd_ServoLocatingPinsLH_Advance := FALSE;
        bCmd_ServoLocatingPinsRH_Advance := FALSE;
        bCmd_GateLH_ToggleLockEngage := FALSE;
        bCmd_GateRH_ToggleLockEngage := FALSE;

        aState_x_ref[1] := -1050.0; (* Drive gates outward to park stance *)
        IF (rVoted_GateLH_Position <= 5.0) AND (rVoted_GateRH_Position <= 5.0) AND
           NOT bServoLocatingPinsLH_Seated AND NOT bServoLocatingPinsRH_Seated THEN
            udiFSM_StateStep := 0;
            iFSM_State := cSTATE_LIFT_CARRY_LOWER_SKID;
        END_IF;

    cSTATE_LIFT_CARRY_LOWER_SKID:
        (* Lower Body Back onto Roller Bed Skid Carrier *)
        bCmd_SkidRoughLocateLifterRaise := FALSE;
        bCmd_SkidRoughLocateLifterLower := TRUE;

        IF bSkidRoughLocatePinsLowered THEN
            udiFSM_StateStep := 0;
            IF bDownstreamStationReadyForSkid THEN
                iFSM_State := cSTATE_SKID_OUTFEED_TRANSFER;
                iSCurve_Phase := 1;
                rSCurve_PhaseTimer_s := 0.0;
                rSCurve_CurrentPos := 0.0;
                rSCurve_CurrentVel := 0.0;
                bSCurve_TransferComplete := FALSE;
            END_IF;
        END_IF;

    cSTATE_SKID_OUTFEED_TRANSFER:
        (* Accelerate Skid Out of Framing Cell to Downstream Respot Buffer *)
        aState_x_ref[2] := rSCurve_CurrentVel;
        IF bSCurve_TransferComplete OR (rVoted_SkidTransferPosition >= (rSCurve_TargetDistance - 2.0)) THEN
            aState_x_ref[2] := 0.0;
            aControl_u[2] := 0.0;
            bCmd_CellCycleCompletedPulse := TRUE;
            udiCycleCounter := udiCycleCounter + 1;
            udiFSM_StateStep := 0;
            iFSM_State := cSTATE_STANDBY_IDLE;
        END_IF;

    cSTATE_EXPULSION_RECOVERY_TIP_DRESS:
        (* Automated Expulsion Defect Recovery & Tip Dressing Routine *)
        bCmd_TriggerRobotGrp1_GeoTack := FALSE;
        bCmd_TipDresserCycleRequest := TRUE;

        IF udiSpotsWeldedCurrentElectrodeTip >= 300 THEN
            udiSpotsWeldedCurrentElectrodeTip := 0;
            bCmd_TipDresserCycleRequest := FALSE;
            bMoltenExpulsionDetected := FALSE;
            udiFSM_StateStep := 0;
            iFSM_State := cSTATE_ROBOT_GRP2_RESPOT_WELD;
        ELSE
            bCmd_TipDresserCycleRequest := FALSE;
            bMoltenExpulsionDetected := FALSE;
            udiFSM_StateStep := 0;
            iFSM_State := cSTATE_ROBOT_GRP2_RESPOT_WELD;
        END_IF;

    cSTATE_EMERGENCY_ABORT_COLLISION:
        (* Deterministic Safe Actuator Freeze & Graceful Pressure Bleed *)
        bCmd_CellSafeHoldActive := TRUE;
        bCmd_TriggerRobotGrp1_GeoTack := FALSE;
        bCmd_TriggerRobotGrp2_Respot := FALSE;
        bCmd_TriggerLaserCMM_ScanCycle := FALSE;
        rFramingGateLH_ServoSpeedCmd := 0.0;
        rFramingGateRH_ServoSpeedCmd := 0.0;
        rSkidRollerVFD_FreqCmd := 0.0;
        rPneumaticClampPropValveCmd := 0.0;
        rHydraulicToggleLockPropCmd := 0.0;
        rActiveMassDamperForceCmd := 0.0;
        aControl_u[1] := 0.0;
        aControl_u[2] := 0.0;
        aControl_u[3] := 0.0;
        aControl_u[4] := 0.0;
        aControl_u[5] := 0.0;
        aControl_u[6] := 0.0;
        aControl_u[7] := 0.0;
        aControl_u[8] := 0.0;

        IF bAlarmResetCmd AND bEmergencyStopCircuitHealthy AND bSafetyFenceZoneInterlocksOk THEN
            bCmd_CellSafeHoldActive := FALSE;
            bAlarm_TMR_MajorDiscrepancyTrip := FALSE;
            iFSM_State := cSTATE_STANDBY_IDLE;
        END_IF;

END_CASE;

iCurrentFSM_State := iFSM_State;
""")

    # -------------------------------------------------------------------------
    # PHASE 5: ISA-18.2 MULTI-TIER ALARMS & 32-BIT BIT-PACKED STATUS WORDS
    # -------------------------------------------------------------------------
    parts.append("""
(* ==================================================================================================== *)
(* PHASE 5: ISA-18.2 MULTI-TIER ALARMS & 32-BIT BIT-PACKED STATUS WORDS                                 *)
(* ==================================================================================================== *)

(* Framing Gate LH Lock Position Alarms *)
IF rVoted_GateLH_Position >= rGateLH_HI_HI_Trip_mm THEN
    bAlarm_GateLH_HI_HI := TRUE;
ELSE
    IF rVoted_GateLH_Position <= (rGateLH_HI_HI_Trip_mm - rGateLH_Deadband_mm) THEN
        bAlarm_GateLH_HI_HI := FALSE;
    END_IF;
END_IF;

IF rVoted_GateLH_Position >= rGateLH_HI_Trip_mm THEN
    bAlarm_GateLH_HI := TRUE;
ELSE
    IF rVoted_GateLH_Position <= (rGateLH_HI_Trip_mm - rGateLH_Deadband_mm) THEN
        bAlarm_GateLH_HI := FALSE;
    END_IF;
END_IF;

IF rVoted_GateLH_Position <= rGateLH_LO_LO_Trip_mm AND (iFSM_State = cSTATE_GEOMETRY_CLAMP_SEQUENCE) THEN
    bAlarm_GateLH_LO_LO := TRUE;
ELSE
    IF rVoted_GateLH_Position >= (rGateLH_LO_LO_Trip_mm + rGateLH_Deadband_mm) THEN
        bAlarm_GateLH_LO_LO := FALSE;
    END_IF;
END_IF;

IF rVoted_GateLH_Position <= rGateLH_LO_Trip_mm AND (iFSM_State = cSTATE_GEOMETRY_CLAMP_SEQUENCE) THEN
    bAlarm_GateLH_LO := TRUE;
ELSE
    IF rVoted_GateLH_Position >= (rGateLH_LO_Trip_mm + rGateLH_Deadband_mm) THEN
        bAlarm_GateLH_LO := FALSE;
    END_IF;
END_IF;

(* Pneumatic Supply Header Alarms *)
IF rVoted_PneumaticHeaderPressure >= rPneumatic_HI_HI_Trip_bar THEN
    bAlarm_Pneumatic_HI_HI := TRUE;
ELSE
    IF rVoted_PneumaticHeaderPressure <= (rPneumatic_HI_HI_Trip_bar - rPneumatic_Deadband_bar) THEN
        bAlarm_Pneumatic_HI_HI := FALSE;
    END_IF;
END_IF;

IF rVoted_PneumaticHeaderPressure <= rPneumatic_LO_LO_Trip_bar THEN
    bAlarm_Pneumatic_LO_LO := TRUE;
ELSE
    IF rVoted_PneumaticHeaderPressure >= (rPneumatic_LO_LO_Trip_bar + rPneumatic_Deadband_bar) THEN
        bAlarm_Pneumatic_LO_LO := FALSE;
    END_IF;
END_IF;

IF rVoted_PneumaticHeaderPressure <= rPneumatic_LO_Trip_bar THEN
    bAlarm_Pneumatic_LO := TRUE;
ELSE
    IF rVoted_PneumaticHeaderPressure >= (rPneumatic_LO_Trip_bar + rPneumatic_Deadband_bar) THEN
        bAlarm_Pneumatic_LO := FALSE;
    END_IF;
END_IF;

(* Hydraulic Clamp Toggle Locking Pressure Alarms *)
IF rVoted_HydraulicTogglePressure >= rHydraulic_HI_HI_Trip_bar THEN
    bAlarm_Hydraulic_HI_HI := TRUE;
ELSE
    IF rVoted_HydraulicTogglePressure <= (rHydraulic_HI_HI_Trip_bar - rHydraulic_Deadband_bar) THEN
        bAlarm_Hydraulic_HI_HI := FALSE;
    END_IF;
END_IF;

IF rVoted_HydraulicTogglePressure <= rHydraulic_LO_LO_Trip_bar AND (iFSM_State = cSTATE_GEOMETRY_CLAMP_SEQUENCE) THEN
    bAlarm_Hydraulic_LO_LO := TRUE;
ELSE
    IF rVoted_HydraulicTogglePressure >= (rHydraulic_LO_LO_Trip_bar + rHydraulic_Deadband_bar) THEN
        bAlarm_Hydraulic_LO_LO := FALSE;
    END_IF;
END_IF;

(* Robot 1 Secondary Weld Current Alarms *)
IF rVoted_Robot1_WeldCurrent >= rCurrent_HI_HI_Trip_kA THEN
    bAlarm_Current_HI_HI := TRUE;
ELSE
    IF rVoted_Robot1_WeldCurrent <= (rCurrent_HI_HI_Trip_kA - rCurrent_Deadband_kA) THEN
        bAlarm_Current_HI_HI := FALSE;
    END_IF;
END_IF;

IF (rVoted_Robot1_WeldCurrent <= rCurrent_LO_LO_Trip_kA) AND
   (iFSM_State = cSTATE_ROBOT_GRP1_GEO_TACK_WELD) AND (bCmd_TriggerRobotGrp1_GeoTack) THEN
    bAlarm_Current_LO_LO := TRUE;
ELSE
    IF rVoted_Robot1_WeldCurrent >= (rCurrent_LO_LO_Trip_kA + rCurrent_Deadband_kA) THEN
        bAlarm_Current_LO_LO := FALSE;
    END_IF;
END_IF;

(* Electrode Tip Temperature Alarms *)
IF TT_ROBOT1_ELECTRODE_TEMP >= rTipTemp_HI_HI_Trip_degC THEN
    bAlarm_TipTemp_HI_HI := TRUE;
ELSE
    IF TT_ROBOT1_ELECTRODE_TEMP <= (rTipTemp_HI_HI_Trip_degC - rTipTemp_Deadband_degC) THEN
        bAlarm_TipTemp_HI_HI := FALSE;
    END_IF;
END_IF;

(* Framer Base Vibration Acceleration Alarms *)
IF rVoted_FrameVibrationAccel >= rVibration_HI_HI_Trip_ms2 THEN
    bAlarm_Vibration_HI_HI := TRUE;
ELSE
    IF rVoted_FrameVibrationAccel <= (rVibration_HI_HI_Trip_ms2 - rVibration_Deadband_ms2) THEN
        bAlarm_Vibration_HI_HI := FALSE;
    END_IF;
END_IF;

(* Hardware Safety Loop Interlock Alarms *)
IF NOT bEmergencyStopCircuitHealthy THEN
    bAlarm_EStopTripped := TRUE;
ELSE
    bAlarm_EStopTripped := FALSE;
END_IF;

IF NOT bSafetyFenceZoneInterlocksOk THEN
    bAlarm_SafetyFencingBreached := TRUE;
ELSE
    bAlarm_SafetyFencingBreached := FALSE;
END_IF;

(* Bit-Pack ISA-18.2 Priority 1 Critical Trip Word (dwAlarmWord1) *)
dwAlarmWord1_ISA_CriticalTrips := 16#00000000;
IF bAlarm_EStopTripped                 THEN dwAlarmWord1_ISA_CriticalTrips := dwAlarmWord1_ISA_CriticalTrips OR 16#00000001; END_IF;
IF bAlarm_SafetyFencingBreached        THEN dwAlarmWord1_ISA_CriticalTrips := dwAlarmWord1_ISA_CriticalTrips OR 16#00000002; END_IF;
IF bAlarm_GateLH_HI_HI                 THEN dwAlarmWord1_ISA_CriticalTrips := dwAlarmWord1_ISA_CriticalTrips OR 16#00000004; END_IF;
IF bAlarm_GateLH_LO_LO                 THEN dwAlarmWord1_ISA_CriticalTrips := dwAlarmWord1_ISA_CriticalTrips OR 16#00000008; END_IF;
IF bAlarm_Pneumatic_LO_LO              THEN dwAlarmWord1_ISA_CriticalTrips := dwAlarmWord1_ISA_CriticalTrips OR 16#00000010; END_IF;
IF bAlarm_Hydraulic_LO_LO              THEN dwAlarmWord1_ISA_CriticalTrips := dwAlarmWord1_ISA_CriticalTrips OR 16#00000020; END_IF;
IF bAlarm_Current_HI_HI                THEN dwAlarmWord1_ISA_CriticalTrips := dwAlarmWord1_ISA_CriticalTrips OR 16#00000040; END_IF;
IF bAlarm_TipTemp_HI_HI                THEN dwAlarmWord1_ISA_CriticalTrips := dwAlarmWord1_ISA_CriticalTrips OR 16#00000080; END_IF;
IF bAlarm_Vibration_HI_HI              THEN dwAlarmWord1_ISA_CriticalTrips := dwAlarmWord1_ISA_CriticalTrips OR 16#00000100; END_IF;
IF bAlarm_TMR_MajorDiscrepancyTrip     THEN dwAlarmWord1_ISA_CriticalTrips := dwAlarmWord1_ISA_CriticalTrips OR 16#00000200; END_IF;

(* Bit-Pack ISA-18.2 Priority 2 Process Warning Word (dwAlarmWord2) *)
dwAlarmWord2_ISA_ProcessWarnings := 16#00000000;
IF bAlarm_GateLH_HI                    THEN dwAlarmWord2_ISA_ProcessWarnings := dwAlarmWord2_ISA_ProcessWarnings OR 16#00000001; END_IF;
IF bAlarm_GateLH_LO                    THEN dwAlarmWord2_ISA_ProcessWarnings := dwAlarmWord2_ISA_ProcessWarnings OR 16#00000002; END_IF;
IF bAlarm_Pneumatic_HI                 THEN dwAlarmWord2_ISA_ProcessWarnings := dwAlarmWord2_ISA_ProcessWarnings OR 16#00000004; END_IF;
IF bAlarm_Pneumatic_LO                 THEN dwAlarmWord2_ISA_ProcessWarnings := dwAlarmWord2_ISA_ProcessWarnings OR 16#00000008; END_IF;
IF bAlarm_Hydraulic_HI                 THEN dwAlarmWord2_ISA_ProcessWarnings := dwAlarmWord2_ISA_ProcessWarnings OR 16#00000010; END_IF;
IF bAlarm_Hydraulic_LO                 THEN dwAlarmWord2_ISA_ProcessWarnings := dwAlarmWord2_ISA_ProcessWarnings OR 16#00000020; END_IF;
IF bAlarm_Current_HI                   THEN dwAlarmWord2_ISA_ProcessWarnings := dwAlarmWord2_ISA_ProcessWarnings OR 16#00000040; END_IF;
IF bAlarm_Current_LO                   THEN dwAlarmWord2_ISA_ProcessWarnings := dwAlarmWord2_ISA_ProcessWarnings OR 16#00000080; END_IF;
IF bAlarm_TipTemp_HI                   THEN dwAlarmWord2_ISA_ProcessWarnings := dwAlarmWord2_ISA_ProcessWarnings OR 16#00000100; END_IF;
IF bAlarm_Vibration_HI                 THEN dwAlarmWord2_ISA_ProcessWarnings := dwAlarmWord2_ISA_ProcessWarnings OR 16#00000200; END_IF;
IF bCMM_DimensionalViolation           THEN dwAlarmWord2_ISA_ProcessWarnings := dwAlarmWord2_ISA_ProcessWarnings OR 16#00000400; END_IF;

(* Bit-Pack Operational FSM Status Word *)
dwFSM_OperationalStatusWord := INT_TO_DWORD(iFSM_State) OR
                               SHL(UDINT_TO_DWORD(udiFSM_StateStep), 8) OR
                               SHL(INT_TO_DWORD(iSCurve_Phase), 16);

(* Master Cell Fault Summary Evaluation *)
IF (dwAlarmWord1_ISA_CriticalTrips <> 16#00000000) OR
   bAlarm_TMR_MajorDiscrepancyTrip THEN
    bCellGeneralFaultActive := TRUE;
ELSE
    bCellGeneralFaultActive := FALSE;
END_IF;

END_FUNCTION_BLOCK
""")

    code = "".join(parts)
    return code

if __name__ == "__main__":
    code = generate_framer_code()
    print("Generated code length:", len(code))
    
    # Check validator on ST directly
    from validate_iec import validate_iec_st
    errors = validate_iec_st(code)
    if errors:
        print("Validation errors:", errors)
    else:
        print("Direct ST validation passed with 0 errors!")
