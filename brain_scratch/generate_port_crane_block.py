# -*- coding: utf-8 -*-
"""
Full generator for FB_Port_STS_GantryCrane_AntiSway_SpreaderLanding
Domain: Heavy Maritime Port Logistics & Automated Container Terminals
System: 65-Ton Twin-Lift Automated Ship-to-Shore (STS) Mega-Gantry Container Crane
"""

import sys
import os
import json
import uuid
import re

def generate_full_block():
    sections = []
    
    # -------------------------------------------------------------------------------------------------
    # HEADER & DOCUMENTATION
    # -------------------------------------------------------------------------------------------------
    sections.append("""FUNCTION_BLOCK FB_Port_STS_GantryCrane_AntiSway_SpreaderLanding
(* =====================================================================================================================
 * LUMINA CYBER-PHYSICAL AUTOMATION ENGINE - SYNTHETIC DATASET V7 MAX-PERSONA
 * COMMERCIAL INDUSTRIAL SECTOR : Heavy Maritime Port Logistics & Automated Container Terminals
 * SYSTEM                       : 65-Ton Twin-Lift Automated Ship-to-Shore (STS) Mega-Gantry Container Crane
 * INTEGRATED SUBSYSTEMS        : - Active Real-Time Pendulum Wire-Rope Anti-Sway & Skew Damping Control (< 0.10 deg Residual Sway)
 *                                - Dual-Hoist 4-Drum Closed-Loop Resolver Leveling Synchronization (1,200 kW Vector Inverter Drives)
 *                                - Laser Lidar Spreader-to-Cell-Guide Dynamic Trajectory Landing & Collision Avoidance
 *                                - 4-Corner Hydraulic Twistlock Seated & Locked Interlock Verification (180 bar Manifold)
 *                                - High-Wind Gust Storm Rail Clamp Hydraulic Interlocks & 50 ms Fast Mechanical Caliper Brake Trip
 *                                - 8x8 Multivariable Discrete State-Space Cyber-Physical Dynamics (10 ms Discrete Cycle)
 *                                - Receding-Horizon Model Predictive Control (MPC) with Projected Gradient Descent (PGD)
 *                                - 2oo3 Triple Modular Redundant (TMR) Sensor Voting with Bumpless Degradation
 *                                - ISA-18.2 5-Tier Process Alarm Hierarchy & Diagnostic Bit-Packed Words
 *                                - 12-Stage Deterministic Terminal Operational Finite State Machine (FSM)
 * =====================================================================================================================
 * MARITIME CRANE CYBER-PHYSICAL FORMULATIONS & THERMOMECHANICAL CONTROL FOUNDATIONS:
 * 1. Non-Linear Spherical Pendulum Dynamics with Time-Varying Rope Length L(t):
 *    A container suspended from a traveling trolley exhibits coupled non-linear spherical pendulum oscillations:
 *      d2(theta)/dt2 + (2 * dL/dt / L) * d(theta)/dt + (g / L) * sin(theta) = - (d2(x_tr)/dt2 / L) * cos(theta) - (F_wind_sway / (M_L * L))
 *    where theta is the planar sway angle in the trolley travel direction, L(t) is the instantaneous wire rope payout length,
 *    x_tr is the trolley coordinate, M_L is the total suspended mass (spreader + container load), and g = 9.80665 m/s2.
 *    The term (2 * dL/dt / L) represents Coriolis damping/amplification induced by simultaneous vertical hoisting/lowering.
 * 2. 4-Wire Reeving Torsional Skew Dynamics:
 *    The 4-point wire rope reeving geometry provides torsional restoring stiffness K_tors = (M_L * g * W_reev^2) / (4 * L),
 *    where W_reev is transverse reeving sheave spacing (2.45 m). The unforced skew dynamics satisfy:
 *      d2(phi)/dt2 + 2 * zeta_phi * omega_phi * d(phi)/dt + (g * W_reev^2 / (4 * L * R_gyr^2)) * phi = T_actuator / I_zz
 *    Active hydraulic skew trim cylinders on the headblock inject opposing torques to damp yaw oscillation < 0.08 deg.
 * 3. Dual-Hoist 4-Drum Leveling & Dynamic Load Equalization:
 *    Dual 1,200 kW flux-vector drives power water-side (drums 1 & 2) and land-side (drums 3 & 4) rope drums.
 *    High-resolution optical multi-turn resolvers track differential payout Delta_L_level = L_waterside - L_landside.
 *    Closed-loop leveling cross-coupling ensures Delta_L_level remains within +/- 10 mm during 1.5 m/s hoisting.
 * 4. Bluff-Body Aerodynamic Drag under Sea-Breeze & Storm Gusts:
 *    Standard 40-foot high-cube containers present 35.3 m2 frontal area and 7.06 m2 side area.
 *    Aerodynamic drag force is evaluated continuously via F_drag = 0.5 * rho_air * C_d * A_proj * (v_wind - v_trolley)^2.
 *    The calculated drag load is injected into the trolley flux-vector torque loop as feedforward compensation.
 * 5. Receding-Horizon Model Predictive Control (MPC):
 *    Optimizes a quadratic cost functional J over an 8-state, 6-input trajectory:
 *      J = 0.5 * (x[k+1] - x_ref)^T * Q * (x[k+1] - x_ref) + 0.5 * u^T * R * u + 0.5 * Delta_u^T * S * Delta_u + 0.5 * x[k+1]^T * P * x[k+1]
 *    Iterative Projected Gradient Descent (PGD) computes optimal trolley acceleration, hoist speeds, and skew valve trims,
 *    enforcing actuator saturation bounds, slew limits, and terminal deadbeat sway convergence in < 38 s per move.
 * =====================================================================================================================
 *)""")

    # -------------------------------------------------------------------------------------------------
    # VAR_INPUT
    # -------------------------------------------------------------------------------------------------
    sections.append("""VAR_INPUT
    (* Master Supervisory Permissives & Safety Interlocks *)
    bEnable                           : BOOL := FALSE;    (* Master Supervisory Automation Enable Permissive [BOOL] *)
    bResetFault                       : BOOL := FALSE;    (* Operator Master Fault Reset / Trip Acknowledge [BOOL] *)
    bEmergencyStop_NC                 : BOOL := TRUE;     (* Dual-Channel Hardwired E-Stop Circuit Active-Low [BOOL] *)
    bAutoCycleStart                   : BOOL := FALSE;    (* Automated Container Move Cycle Command Trigger [BOOL] *)
    bManualModeSelect                 : BOOL := FALSE;    (* Operator Manual Joystick Override Permissive [BOOL] *)
    bShipHoldModeSelect               : BOOL := TRUE;     (* Vessel Cell Guide Precision Landing Mode Active [BOOL] *)
    bQuayChassisModeSelect            : BOOL := FALSE;    (* Quay Apron AGV / Chassis Soft Landing Mode Active [BOOL] *)
    bHighWindOverrideKey              : BOOL := FALSE;    (* Harbor Master High-Wind Supervisory Key Switch [BOOL] *)
    bSpreader20ftMode                 : BOOL := FALSE;    (* Spreader Telescoping Setpoint: 20-Foot Container [BOOL] *)
    bSpreader40ftMode                 : BOOL := TRUE;     (* Spreader Telescoping Setpoint: 40-Foot Container [BOOL] *)
    bSpreader45ftMode                 : BOOL := FALSE;    (* Spreader Telescoping Setpoint: 45-Foot Container [BOOL] *)
    bTwinLiftMode                     : BOOL := FALSE;    (* Twin-Lift Mode Active (Two 20ft Containers Simultaneously) [BOOL] *)

    (* Trajectory Setpoints & Operational Limits *)
    rTargetTrolleyPos_m               : REAL := 45.000;   (* Target Trolley Destination Coordinate [m] *)
    rTargetHoistPos_m                 : REAL := 28.500;   (* Target Hoist Payout Length Coordinate [m] *)
    rTargetTrimAngle_deg              : REAL := 0.000;    (* Desired Spreader Fore/Aft Pitch Trim Angle [deg] *)
    rTargetListAngle_deg              : REAL := 0.000;    (* Desired Spreader Port/Starboard Roll List Angle [deg] *)
    rMaxTrolleySpeed_mps              : REAL := 4.000;    (* Maximum Allowable Trolley Velocity [m/s] *)
    rMaxHoistSpeed_mps                : REAL := 1.500;    (* Maximum Allowable Hoist Velocity [m/s] *)
    rMaxTrolleyAcc_mps2               : REAL := 1.200;    (* Maximum Trolley Acceleration / Deceleration [m/s2] *)

    (* 2oo3 Triple Modular Redundant (TMR) Process Transmitters & Sensors *)
    (* ZT_TROLLEY_ENCODER_101: Trolley Laser Absolute Position Transducers [m] *)
    ZT_TROLLEY_ENCODER_101A           : REAL := 0.000;    (* Trolley Laser Distance Transducer Channel A [m] *)
    ZT_TROLLEY_ENCODER_101B           : REAL := 0.000;    (* Trolley Laser Distance Transducer Channel B [m] *)
    ZT_TROLLEY_ENCODER_101C           : REAL := 0.000;    (* Trolley Laser Distance Transducer Channel C [m] *)

    (* ST_TROLLEY_MOTOR_RPM_102: Trolley Drive Motor Speed Resolvers [RPM] *)
    ST_TROLLEY_MOTOR_RPM_102A         : REAL := 0.0;      (* Trolley Flux-Vector Motor Resolver Channel A [RPM] *)
    ST_TROLLEY_MOTOR_RPM_102B         : REAL := 0.0;      (* Trolley Flux-Vector Motor Resolver Channel B [RPM] *)
    ST_TROLLEY_MOTOR_RPM_102C         : REAL := 0.0;      (* Trolley Flux-Vector Motor Resolver Channel C [RPM] *)

    (* ZT_HOIST_ROPE_LENGTH_201: Hoist Drum Absolute Wire Rope Payout Length L(t) [m] *)
    ZT_HOIST_ROPE_LENGTH_201A         : REAL := 12.000;   (* Hoist Drum Absolute Multi-Turn Encoder Channel A [m] *)
    ZT_HOIST_ROPE_LENGTH_201B         : REAL := 12.000;   (* Hoist Drum Absolute Multi-Turn Encoder Channel B [m] *)
    ZT_HOIST_ROPE_LENGTH_201C         : REAL := 12.000;   (* Hoist Drum Absolute Multi-Turn Encoder Channel C [m] *)

    (* ST_HOIST_MOTOR_RPM_202: Dual-Hoist Vector Drive Motor Resolvers [RPM] *)
    ST_HOIST_MOTOR_RPM_202A           : REAL := 0.0;      (* Hoist 1200 kW Main Inverter Drive Resolver Channel A [RPM] *)
    ST_HOIST_MOTOR_RPM_202B           : REAL := 0.0;      (* Hoist 1200 kW Main Inverter Drive Resolver Channel B [RPM] *)
    ST_HOIST_MOTOR_RPM_202C           : REAL := 0.0;      (* Hoist 1200 kW Main Inverter Drive Resolver Channel C [RPM] *)

    (* OPT_SPREADER_SWAY_ANGLE_301: Optical Infrared Camera Pendulum Sway Angle theta [deg] *)
    OPT_SPREADER_SWAY_ANGLE_301A      : REAL := 0.000;    (* Optical IR Camera Spreader Sway Angle Channel A [deg] *)
    OPT_SPREADER_SWAY_ANGLE_301B      : REAL := 0.000;    (* Optical IR Camera Spreader Sway Angle Channel B [deg] *)
    OPT_SPREADER_SWAY_ANGLE_301C      : REAL := 0.000;    (* Optical IR Camera Spreader Sway Angle Channel C [deg] *)

    (* OPT_SPREADER_SKEW_ANGLE_302: Optical Infrared Camera Spreader Skew Angle phi [deg] *)
    OPT_SPREADER_SKEW_ANGLE_302A      : REAL := 0.000;    (* Optical IR Camera Spreader Skew Angle Channel A [deg] *)
    OPT_SPREADER_SKEW_ANGLE_302B      : REAL := 0.000;    (* Optical IR Camera Spreader Skew Angle Channel B [deg] *)
    OPT_SPREADER_SKEW_ANGLE_302C      : REAL := 0.000;    (* Optical IR Camera Spreader Skew Angle Channel C [deg] *)

    (* LIDAR_CELL_GUIDE_DIST_401: 2D Laser Lidar Spreader-to-Cell-Guide Clearance [mm] *)
    LIDAR_CELL_GUIDE_DIST_401A        : REAL := 150.0;    (* 2D Laser Lidar Spreader-to-Cell-Guide Clearance Channel A [mm] *)
    LIDAR_CELL_GUIDE_DIST_401B        : REAL := 150.0;    (* 2D Laser Lidar Spreader-to-Cell-Guide Clearance Channel B [mm] *)
    LIDAR_CELL_GUIDE_DIST_401C        : REAL := 150.0;    (* 2D Laser Lidar Spreader-to-Cell-Guide Clearance Channel C [mm] *)

    (* WT_SPREADER_LOAD_CELL_501: 4-Corner Spreader Pin Load Cells [tonnes] *)
    WT_SPREADER_LOAD_CELL_501A        : REAL := 12.50;    (* 4-Corner Spreader Pin Load Cell Channel A [tonnes] *)
    WT_SPREADER_LOAD_CELL_501B        : REAL := 12.50;    (* 4-Corner Spreader Pin Load Cell Channel B [tonnes] *)
    WT_SPREADER_LOAD_CELL_501C        : REAL := 12.50;    (* 4-Corner Spreader Pin Load Cell Channel C [tonnes] *)

    (* PT_TWISTLOCK_HYDR_PRESS_601: Twistlock Hydraulic Manifold Actuation Pressure [bar] *)
    PT_TWISTLOCK_HYDR_PRESS_601A      : REAL := 185.0;    (* Twistlock Hydraulic Manifold Pressure Channel A [bar] *)
    PT_TWISTLOCK_HYDR_PRESS_601B      : REAL := 185.0;    (* Twistlock Hydraulic Manifold Pressure Channel B [bar] *)
    PT_TWISTLOCK_HYDR_PRESS_601C      : REAL := 185.0;    (* Twistlock Hydraulic Manifold Pressure Channel C [bar] *)

    (* AIT_ANEMOMETER_WIND_SPEED_701: Ultrasonic 2-Axis Boom Tip Anemometer [m/s] *)
    AIT_ANEMOMETER_WIND_SPEED_701A    : REAL := 6.50;     (* Ultrasonic Anemometer Boom Tip Channel A [m/s] *)
    AIT_ANEMOMETER_WIND_SPEED_701B    : REAL := 6.50;     (* Ultrasonic Anemometer Boom Tip Channel B [m/s] *)
    AIT_ANEMOMETER_WIND_SPEED_701C    : REAL := 6.50;     (* Ultrasonic Anemometer Boom Tip Channel C [m/s] *)

    (* ZT_RAIL_CLAMP_STATUS_801: Storm Rail Clamp Hydraulic Locking Pressure [bar] *)
    ZT_RAIL_CLAMP_STATUS_801A         : REAL := 160.0;    (* Storm Rail Clamp Hydraulic Pressure Channel A [bar] *)
    ZT_RAIL_CLAMP_STATUS_801B         : REAL := 160.0;    (* Storm Rail Clamp Hydraulic Pressure Channel B [bar] *)
    ZT_RAIL_CLAMP_STATUS_801C         : REAL := 160.0;    (* Storm Rail Clamp Hydraulic Pressure Channel C [bar] *)

    (* 4-Corner Twistlock Mechanical Limit & Seating Sensors *)
    bTwistlockSeated_FL               : BOOL := FALSE;    (* Corner Seated Proximity Sensor: Front-Left [BOOL] *)
    bTwistlockSeated_FR               : BOOL := FALSE;    (* Corner Seated Proximity Sensor: Front-Right [BOOL] *)
    bTwistlockSeated_RL               : BOOL := FALSE;    (* Corner Seated Proximity Sensor: Rear-Left [BOOL] *)
    bTwistlockSeated_RR               : BOOL := FALSE;    (* Corner Seated Proximity Sensor: Rear-Right [BOOL] *)
    bTwistlockLocked_FL               : BOOL := FALSE;    (* Twistlock Fully Locked Proximity Sensor: Front-Left [BOOL] *)
    bTwistlockLocked_FR               : BOOL := FALSE;    (* Twistlock Fully Locked Proximity Sensor: Front-Right [BOOL] *)
    bTwistlockLocked_RL               : BOOL := FALSE;    (* Twistlock Fully Locked Proximity Sensor: Rear-Left [BOOL] *)
    bTwistlockLocked_RR               : BOOL := FALSE;    (* Twistlock Fully Locked Proximity Sensor: Rear-Right [BOOL] *)
    bTwistlockUnlocked_FL             : BOOL := TRUE;     (* Twistlock Fully Unlocked Proximity Sensor: Front-Left [BOOL] *)
    bTwistlockUnlocked_FR             : BOOL := TRUE;     (* Twistlock Fully Unlocked Proximity Sensor: Front-Right [BOOL] *)
    bTwistlockUnlocked_RL             : BOOL := TRUE;     (* Twistlock Fully Unlocked Proximity Sensor: Rear-Left [BOOL] *)
    bTwistlockUnlocked_RR             : BOOL := TRUE;     (* Twistlock Fully Unlocked Proximity Sensor: Rear-Right [BOOL] *)

    (* Spreader Corner Guide Flippers & Quay Chassis Feedback *)
    bFlipperPosition_Retracted        : BOOL := TRUE;     (* Corner Guide Flippers Retracted Upper Limit [BOOL] *)
    bFlipperPosition_Deployed         : BOOL := FALSE;    (* Corner Guide Flippers Extended Lower Guide Limit [BOOL] *)
    bChassisPresentOnLane             : BOOL := TRUE;     (* Quay Apron Lane Ultrasonic Vehicle Present Sensor [BOOL] *)
    bChassisTwistlocksOpen            : BOOL := TRUE;     (* Quay Chassis Latch Receptors Cleared & Ready [BOOL] *)
END_VAR""")

    # -------------------------------------------------------------------------------------------------
    # VAR_OUTPUT
    # -------------------------------------------------------------------------------------------------
    sections.append("""VAR_OUTPUT
    (* Mega-Gantry Crane Operational Status Flags *)
    bReady                            : BOOL := FALSE;    (* Mega-Gantry Crane Automation Master System Ready Permissive [BOOL] *)
    bBusy                             : BOOL := FALSE;    (* Automated Move Cycle Currently Active on Quay/Vessel [BOOL] *)
    bCycleCompleted                   : BOOL := FALSE;    (* Container Cycle Completed With Zero Residual Sway [BOOL] *)
    bEmergencyStopTripped             : BOOL := FALSE;    (* Hardware/Software E-Stop Fast Abort Latched [BOOL] *)
    bStormRailClampDeployed           : BOOL := FALSE;    (* High-Wind Gust Storm Rail Clamp Hydraulics Clamped [BOOL] *)
    bTwistlockEngaged                 : BOOL := FALSE;    (* All 4 Twistlocks Verified Seated & Mechanically Locked [BOOL] *)
    bTwistlockReleased                : BOOL := TRUE;     (* All 4 Twistlocks Verified Fully Unlocked & Retracted [BOOL] *)
    bAntiSwayTargetReached            : BOOL := FALSE;    (* Target Position Reached with Residual Sway < 0.10 deg [BOOL] *)
    bCellGuideAligned                 : BOOL := FALSE;    (* Spreader Position Centered Within Cell Guide Tolerances [BOOL] *)
    bSoftTouchdownConfirmed           : BOOL := FALSE;    (* Landing Impact Force < 2.5 tonnes Soft Touchdown Verified [BOOL] *)
    bOverspeedBrakeDropped            : BOOL := FALSE;    (* Mechanical Emergency Disk Caliper Fast Brake Drop (< 50 ms) [BOOL] *)
    nActiveFSM_State                  : INT := 1;         (* Active Deterministic Operational FSM State Index [1..12] *)

    (* ISA-18.2 Diagnostic & Telemetry Status Words *)
    wDiagnosticWord01                 : WORD := 16#0000;  (* FSM State, Sequence Status & Actuator Interlock Feedback [WORD] *)
    wDiagnosticWord02                 : WORD := 16#0000;  (* 2oo3 TMR Sensor Health, Discrepancy & Channel Isolation Flags [WORD] *)
    wDiagnosticWord03                 : WORD := 16#0000;  (* ISA-18.2 Process Warning Alarms (HI / LO Process Flags) [WORD] *)
    wDiagnosticWord04                 : WORD := 16#0000;  (* ISA-18.2 Critical Process Trips (HI_HI / LO_LO / Redlines) [WORD] *)

    (* High-Speed Actuator Commands & Drive Setpoints *)
    rCmd_TrolleyDriveTorque_Nm        : REAL := 0.0;      (* Trolley Inverter Flux-Vector Torque Reference [N*m] *)
    rCmd_TrolleyDriveSpeed_RPM        : REAL := 0.0;      (* Trolley Drive Motor Speed Reference Setpoint [RPM] *)
    rCmd_HoistWatersideSpeed_RPM      : REAL := 0.0;      (* Hoist Water-Side Drums 1 & 2 Vector Drive Speed [RPM] *)
    rCmd_HoistLandsideSpeed_RPM       : REAL := 0.0;      (* Hoist Land-Side Drums 3 & 4 Vector Drive Speed [RPM] *)
    rCmd_SkewTrimValve1_pct           : REAL := 0.0;      (* Headblock Skew Hydraulic Cylinder 1 Servo Valve Command [%] *)
    rCmd_SkewTrimValve2_pct           : REAL := 0.0;      (* Headblock Skew Hydraulic Cylinder 2 Servo Valve Command [%] *)
    bCmd_HoistCaliperBrakeRelease     : BOOL := FALSE;    (* 50 ms Mechanical Disc Caliper Brake Release Solenoid [BOOL] *)
    bCmd_TrolleyParkingBrakeRelease   : BOOL := FALSE;    (* Trolley Motor Parking Disc Brake Release Solenoid [BOOL] *)
    bCmd_StormRailClampRelease        : BOOL := FALSE;    (* Hydraulic Storm Rail Clamp Lift/Release Solenoid [BOOL] *)
    bCmd_TwistlockLockSolenoid        : BOOL := FALSE;    (* Twistlock Hydraulic Directional Valve: Lock Command [BOOL] *)
    bCmd_TwistlockUnlockSolenoid      : BOOL := FALSE;    (* Twistlock Hydraulic Directional Valve: Unlock Command [BOOL] *)
    bCmd_SpreaderFlipperDown          : BOOL := FALSE;    (* Spreader Corner Guide Flipper Hydraulic Deploy Solenoid [BOOL] *)

    (* Cyber-Physical Voted & Computed Telemetry *)
    rTrolleyPosVoted_m                : REAL := 0.0;      (* 2oo3 Voted Trolley Absolute Position Coordinate [m] *)
    rTrolleySpeedVoted_mps            : REAL := 0.0;      (* 2oo3 Voted Trolley Linear Velocity [m/s] *)
    rHoistRopeLengthVoted_m           : REAL := 0.0;      (* 2oo3 Voted Hoist Wire Rope Payout Length L(t) [m] *)
    rHoistSpeedVoted_mps              : REAL := 0.0;      (* 2oo3 Voted Hoist Vertical Payout Velocity dL/dt [m/s] *)
    rSwayAngleVoted_deg               : REAL := 0.0;      (* 2oo3 Voted Spreader Pendulum Sway Angle theta [deg] *)
    rSwayAngularVel_deg_s             : REAL := 0.0;      (* Filtered Pendulum Sway Angular Velocity d(theta)/dt [deg/s] *)
    rSkewAngleVoted_deg               : REAL := 0.0;      (* 2oo3 Voted Spreader Skew Torsion Angle phi [deg] *)
    rSkewAngularVel_deg_s             : REAL := 0.0;      (* Filtered Spreader Skew Angular Velocity d(phi)/dt [deg/s] *)
    rCellGuideDistVoted_mm            : REAL := 0.0;      (* 2oo3 Voted Spreader-to-Cell-Guide Clearance [mm] *)
    rTotalLoadVoted_tonnes            : REAL := 0.0;      (* 2oo3 Voted 4-Corner Total Suspended Mass [tonnes] *)
    rTwistlockPressureVoted_bar       : REAL := 0.0;      (* 2oo3 Voted Twistlock Hydraulic Pressure [bar] *)
    rWindSpeedVoted_mps               : REAL := 0.0;      (* 2oo3 Voted Ultrasonic Wind Velocity [m/s] *)
    rStormRailClampPressureVoted_bar  : REAL := 0.0;      (* 2oo3 Voted Rail Clamp Hydraulic Pressure [bar] *)
    rResidualSwayAngle_deg            : REAL := 0.0;      (* Instantaneous Pendulum Phase-Plane Residual Sway [deg] *)
    rPendulumNaturalFreq_rad_s        : REAL := 0.0;      (* Pendulum Natural Frequency omega_n = sqrt(g/L) [rad/s] *)
    rDrumLevelingDiscrepancy_mm       : REAL := 0.0;      (* Water-Side vs Land-Side Drum Leveling Error [mm] *)
    rWindAerodynamicDragForce_kN      : REAL := 0.0;      (* Real-Time Wind Aerodynamic Bluff-Body Drag Force [kN] *)
    rMPC_ObjectiveCostJ               : REAL := 0.0;      (* Receding-Horizon Optimal Quadratic Objective Cost J [REAL] *)
END_VAR""")

    # -------------------------------------------------------------------------------------------------
    # VAR INTERNAL
    # -------------------------------------------------------------------------------------------------
    sections.append("""VAR
    (* Discrete Automation Scan Cycle & Timing Constants *)
    c_rTs                             : REAL := 0.010;    (* Discrete Control Cycle Period 10.0 milliseconds [s] *)
    c_rPi                             : REAL := 3.141592653589793; (* Mathematical Constant Pi *)
    c_rG                              : REAL := 9.80665;  (* Standard Acceleration of Gravity g0 [m/s2] *)
    c_rDegToRad                       : REAL := 0.017453292519943295; (* Radians per Degree Conversion Factor *)
    c_rRadToDeg                       : REAL := 57.29577951308232;    (* Degrees per Radian Conversion Factor *)

    (* Crane Structural & Kinematic Engineering Constants *)
    c_rTrolleyMass_kg                 : REAL := 38000.0;  (* Bare Trolley Structural Mass [kg] *)
    c_rSpreaderTareMass_kg            : REAL := 12500.0;  (* Telescopic Spreader Tare Mass [kg] *)
    c_rMaxRatedLoad_kg                : REAL := 65000.0;  (* Maximum Rated Twin-Lift Container Payload [kg] *)
    c_rReevingSheaveWidth_m           : REAL := 2.450;    (* Trolley Wire Rope Reeving Transverse Sheave Spacing [m] *)
    c_rSpreaderInertiaYaw_kg_m2       : REAL := 185000.0; (* Suspended Container Assembly Yaw Mass Moment of Inertia [kg*m2] *)
    c_rTrolleyWheelRadius_m           : REAL := 0.450;    (* Trolley Rail Steel Wheel Radius [m] *)
    c_rTrolleyGearRatio               : REAL := 14.850;   (* Trolley Drive Planetary Gearbox Reduction Ratio [-] *)
    c_rTrolleyMotorRatedTorque_Nm     : REAL := 4200.0;   (* Combined Trolley Inverter Vector Rated Torque [N*m] *)
    c_rHoistDrumRadius_m              : REAL := 0.750;    (* Hoist Wire Rope Drum Pitch Radius [m] *)
    c_rHoistGearRatio                 : REAL := 22.400;   (* Hoist Main Planetary Gearbox Reduction Ratio [-] *)
    c_rAirDensity_kg_m3               : REAL := 1.225;    (* Ambient Sea-Level Air Density [kg/m3] *)
    c_rDragCoeffContainer             : REAL := 1.150;    (* Container Aerodynamic Bluff-Body Drag Coefficient [-] *)
    c_rContainerFrontalArea_m2        : REAL := 35.300;   (* 40-ft High-Cube Container Projected Wind Area [m2] *)
    c_rContainerSideArea_m2           : REAL := 7.060;    (* Container Transverse End Projected Wind Area [m2] *)
    c_rSwayDampingRatio               : REAL := 0.015;    (* Equivalent Mechanical Damping Ratio for Wire Rope Sway [-] *)
    c_rSkewDampingRatio               : REAL := 0.050;    (* Equivalent Mechanical Damping Ratio for Skew Torsion [-] *)

    (* 8x8 Multivariable Discrete State-Space Model Arrays (x[k+1] = A*x[k] + B*u[k], y[k] = C*x[k] + D*u[k]) *)
    (* State Vector x[1..8]: *)
    (*   x[1]: Trolley Position Tracking Error Delta_x_tr = x_tr - x_ref [m] *)
    (*   x[2]: Trolley Velocity Tracking Error Delta_v_tr = v_tr - v_ref [m/s] *)
    (*   x[3]: Spreader Pendulum Sway Angle theta [rad] *)
    (*   x[4]: Spreader Pendulum Sway Angular Velocity d(theta)/dt [rad/s] *)
    (*   x[5]: Spreader Skew Torsion Angle phi [rad] *)
    (*   x[6]: Spreader Skew Angular Velocity d(phi)/dt [rad/s] *)
    (*   x[7]: Hoist Wire Rope Payout Length Deviation Delta_L = L - L_ref [m] *)
    (*   x[8]: Hoist Vertical Velocity Deviation Delta_v_h = v_h - v_ref [m/s] *)
    aA                                : ARRAY[1..8, 1..8] OF REAL; (* Discrete System Matrix A *)
    aB                                : ARRAY[1..8, 1..6] OF REAL; (* Discrete Input Coupling Matrix B *)
    aC                                : ARRAY[1..8, 1..8] OF REAL; (* Discrete Output Measurement Matrix C *)
    aD                                : ARRAY[1..8, 1..6] OF REAL; (* Discrete Direct Feedthrough Matrix D *)
    ax_state                          : ARRAY[1..8] OF REAL;      (* Current System State Vector x[k] *)
    ax_next                           : ARRAY[1..8] OF REAL;      (* Next Projected System State Vector x[k+1] *)
    ax_ref                            : ARRAY[1..8] OF REAL;      (* Desired System Equilibrium Reference Vector x_ref *)
    au_control                        : ARRAY[1..6] OF REAL;      (* Optimal Control Actuator Input Vector u[k] *)
    au_prev                           : ARRAY[1..6] OF REAL;      (* Prior Control Actuator Input Vector u[k-1] *)
    au_delta                          : ARRAY[1..6] OF REAL;      (* Slew Rate Vector Delta_u[k] = u[k] - u[k-1] *)
    ay_output                         : ARRAY[1..8] OF REAL;      (* Synthetic Sensor Output Measurement Vector y[k] *)

    (* Model Predictive Control (MPC) Cost Weighting & Hard Actuator Constraints *)
    (* Input Vector u[1..6]: *)
    (*   u[1]: Trolley Drive Acceleration Command a_tr_cmd [m/s2] (-1.20 to +1.20 m/s2) *)
    (*   u[2]: Water-Side Dual-Hoist Drum Acceleration a_h_ws [m/s2] (-1.50 to +1.50 m/s2) *)
    (*   u[3]: Land-Side Dual-Hoist Drum Acceleration a_h_ls [m/s2] (-1.50 to +1.50 m/s2) *)
    (*   u[4]: Skew Trim Cylinder 1 Valve Command v_skew1 [%] (-100.0 to +100.0 %) *)
    (*   u[5]: Skew Trim Cylinder 2 Valve Command v_skew2 [%] (-100.0 to +100.0 %) *)
    (*   u[6]: Anti-Sway Inverter Vector Feedforward Force F_anti_sway [kN] (-85.0 to +85.0 kN) *)
    aQ_Weight                         : ARRAY[1..8] OF REAL;      (* State Tracking Error Penalty Matrix Diag(Q) *)
    aR_Weight                         : ARRAY[1..6] OF REAL;      (* Actuator Effort Penalty Matrix Diag(R) *)
    aS_Weight                         : ARRAY[1..6] OF REAL;      (* Actuator Slew Rate Penalty Matrix Diag(S) *)
    aP_TerminalWeight                 : ARRAY[1..8] OF REAL;      (* Terminal Prediction Cost Matrix Diag(P) *)
    au_min                            : ARRAY[1..6] OF REAL;      (* Hard Lower Actuator Limits u_min *)
    au_max                            : ARRAY[1..6] OF REAL;      (* Hard Upper Actuator Limits u_max *)
    adelta_u_max                      : ARRAY[1..6] OF REAL;      (* Slew Rate Bounds per 10 ms Sample *)
    aGrad_u                           : ARRAY[1..6] OF REAL;      (* Cost Functional Analytical Gradient dJ/du *)
    aPredictedState                   : ARRAY[1..8] OF REAL;      (* 1-Step Horizon Predictive State Vector *)
    c_rPGD_Alpha                      : REAL := 0.00045;          (* Projected Gradient Descent Learning Rate *)

    (* 2oo3 Triple Modular Redundancy Discrepancy Limits & Timers *)
    c_rTol_TrolleyPos_m               : REAL := 0.010;    (* Trolley Laser Distance Discrepancy Limit (10 mm) [m] *)
    c_rTol_TrolleySpeed_RPM           : REAL := 25.0;     (* Trolley Motor Speed Discrepancy Limit [RPM] *)
    c_rTol_HoistRopeLength_m          : REAL := 0.015;    (* Hoist Wire Rope Payout Discrepancy Limit (15 mm) [m] *)
    c_rTol_HoistSpeed_RPM             : REAL := 20.0;     (* Hoist Motor Speed Discrepancy Limit [RPM] *)
    c_rTol_SwayAngle_deg              : REAL := 0.050;    (* Spreader Optical Sway Camera Discrepancy Limit [deg] *)
    c_rTol_SkewAngle_deg              : REAL := 0.050;    (* Spreader Optical Skew Camera Discrepancy Limit [deg] *)
    c_rTol_CellGuideDist_mm           : REAL := 20.0;     (* 2D Laser Lidar Clearance Discrepancy Limit [mm] *)
    c_rTol_LoadCell_tonnes            : REAL := 1.50;     (* 4-Corner Pin Load Cell Discrepancy Limit [tonnes] *)
    c_rTol_TwistlockPress_bar         : REAL := 10.0;     (* Twistlock Hydraulic Manifold Discrepancy Limit [bar] *)
    c_rTol_WindSpeed_mps              : REAL := 2.50;     (* Ultrasonic Anemometer Discrepancy Limit [m/s] *)
    c_rTol_RailClampPress_bar         : REAL := 15.0;     (* Storm Rail Clamp Hydraulic Discrepancy Limit [bar] *)
    c_rTMR_PersistencyTimeout_s       : REAL := 0.250;    (* 2oo3 Discrepancy Persistency Degraded Fault Filter (250 ms) [s] *)

    (* 2oo3 Discrepancy Persistency Timers *)
    rTimer_TrolleyPos_Disc_s          : REAL := 0.0;
    rTimer_TrolleySpeed_Disc_s        : REAL := 0.0;
    rTimer_HoistLength_Disc_s         : REAL := 0.0;
    rTimer_HoistSpeed_Disc_s          : REAL := 0.0;
    rTimer_SwayAngle_Disc_s           : REAL := 0.0;
    rTimer_SkewAngle_Disc_s           : REAL := 0.0;
    rTimer_CellGuide_Disc_s           : REAL := 0.0;
    rTimer_LoadCell_Disc_s            : REAL := 0.0;
    rTimer_TwistlockPress_Disc_s      : REAL := 0.0;
    rTimer_WindSpeed_Disc_s           : REAL := 0.0;
    rTimer_RailClampPress_Disc_s      : REAL := 0.0;

    (* 2oo3 Channel Isolation Latches *)
    bIso_TrolleyPos_ChA               : BOOL := FALSE;
    bIso_TrolleyPos_ChB               : BOOL := FALSE;
    bIso_TrolleyPos_ChC               : BOOL := FALSE;
    bIso_TrolleySpeed_ChA             : BOOL := FALSE;
    bIso_TrolleySpeed_ChB             : BOOL := FALSE;
    bIso_TrolleySpeed_ChC             : BOOL := FALSE;
    bIso_HoistLength_ChA              : BOOL := FALSE;
    bIso_HoistLength_ChB              : BOOL := FALSE;
    bIso_HoistLength_ChC              : BOOL := FALSE;
    bIso_HoistSpeed_ChA               : BOOL := FALSE;
    bIso_HoistSpeed_ChB               : BOOL := FALSE;
    bIso_HoistSpeed_ChC               : BOOL := FALSE;
    bIso_SwayAngle_ChA                : BOOL := FALSE;
    bIso_SwayAngle_ChB                : BOOL := FALSE;
    bIso_SwayAngle_ChC                : BOOL := FALSE;
    bIso_SkewAngle_ChA                : BOOL := FALSE;
    bIso_SkewAngle_ChB                : BOOL := FALSE;
    bIso_SkewAngle_ChC                : BOOL := FALSE;
    bIso_CellGuide_ChA                : BOOL := FALSE;
    bIso_CellGuide_ChB                : BOOL := FALSE;
    bIso_CellGuide_ChC                : BOOL := FALSE;
    bIso_LoadCell_ChA                 : BOOL := FALSE;
    bIso_LoadCell_ChB                 : BOOL := FALSE;
    bIso_LoadCell_ChC                 : BOOL := FALSE;
    bIso_TwistlockPress_ChA           : BOOL := FALSE;
    bIso_TwistlockPress_ChB           : BOOL := FALSE;
    bIso_TwistlockPress_ChC           : BOOL := FALSE;
    bIso_WindSpeed_ChA                : BOOL := FALSE;
    bIso_WindSpeed_ChB                : BOOL := FALSE;
    bIso_WindSpeed_ChC                : BOOL := FALSE;
    bIso_RailClampPress_ChA           : BOOL := FALSE;
    bIso_RailClampPress_ChB           : BOOL := FALSE;
    bIso_RailClampPress_ChC           : BOOL := FALSE;

    (* ISA-18.2 Process Alarm Trip Points, Deadbands & Prior Values *)
    c_rTrolleyPos_Trip_HI_HI          : REAL := 125.000;  (* Water-Side Overtravel Limit Redline [m] *)
    c_rTrolleyPos_Alarm_HI            : REAL := 120.000;  (* Water-Side Soft Deceleration Warning [m] *)
    c_rTrolleyPos_Alarm_LO            : REAL := 2.500;    (* Land-Side Soft Deceleration Warning [m] *)
    c_rTrolleyPos_Trip_LO_LO          : REAL := 0.500;    (* Land-Side Buffer Collision Redline [m] *)
    c_rTrolleyPos_Deadband            : REAL := 0.200;    (* Trolley Position Hysteresis [m] *)

    c_rTrolleySpeed_Trip_HI_HI        : REAL := 4.400;    (* Trolley Drive Overspeed Redline [m/s] *)
    c_rTrolleySpeed_Alarm_HI          : REAL := 4.100;    (* Trolley High Velocity Warning [m/s] *)
    c_rTrolleySpeed_Deadband          : REAL := 0.100;    (* Trolley Speed Hysteresis [m/s] *)

    c_rHoistSpeed_Trip_HI_HI          : REAL := 3.600;    (* Emergency Hoist Overspeed Redline Trip (< 50 ms Caliper Drop) [m/s] *)
    c_rHoistSpeed_Alarm_HI            : REAL := 1.700;    (* Hoist High Speed Warning [m/s] *)
    c_rHoistSpeed_Deadband            : REAL := 0.080;    (* Hoist Speed Hysteresis [m/s] *)

    c_rSwayAngle_Trip_HI_HI           : REAL := 3.500;    (* Catastrophic Container Pendulum Sway Redline [deg] *)
    c_rSwayAngle_Alarm_HI             : REAL := 1.500;    (* Excessive Pendulum Sway Advisory [deg] *)
    c_rSwayAngle_Deadband             : REAL := 0.150;    (* Sway Angle Clearance Hysteresis [deg] *)
    c_rSwayAngle_Max_ROC              : REAL := 4.500;    (* Sway Rate-of-Change Limit 4.50 deg/s *)

    c_rSkewAngle_Trip_HI_HI           : REAL := 2.000;    (* Spreader Torsional Skew Redline Trip [deg] *)
    c_rSkewAngle_Alarm_HI             : REAL := 0.800;    (* High Skew Torsion Advisory [deg] *)
    c_rSkewAngle_Deadband             : REAL := 0.100;    (* Skew Angle Hysteresis [deg] *)

    c_rWindSpeed_Trip_HI_HI           : REAL := 25.000;   (* Severe Storm Gust Redline: Hydraulic Rail Clamps Clamped [m/s] *)
    c_rWindSpeed_Alarm_HI             : REAL := 18.000;   (* High Wind Advisory: Operations Speed Reduced [m/s] *)
    c_rWindSpeed_Deadband             : REAL := 1.500;    (* Wind Speed Hysteresis [m/s] *)

    c_rTwistlockPress_Trip_LO_LO      : REAL := 90.00;    (* Twistlock Hydraulic Pressure Loss Abort Redline [bar] *)
    c_rTwistlockPress_Alarm_LO        : REAL := 140.00;   (* Low Hydraulic Manifold Pressure Warning [bar] *)
    c_rTwistlockPress_Deadband        : REAL := 5.00;     (* Hydraulic Pressure Clearance Hysteresis [bar] *)

    c_rEccentricLoad_Trip_HI_HI       : REAL := 15.000;   (* 4-Corner Diagonal Weight Imbalance Redline [tonnes] *)
    c_rEccentricLoad_Alarm_HI         : REAL := 8.000;    (* Uneven Container Loading Advisory [tonnes] *)
    c_rEccentricLoad_Deadband         : REAL := 1.000;    (* Load Imbalance Hysteresis [tonnes] *)

    c_rDrumLeveling_Trip_HI_HI        : REAL := 35.000;   (* Water-Side / Land-Side Drum Leveling Skew Trip [mm] *)
    c_rDrumLeveling_Alarm_HI          : REAL := 15.000;   (* Drum Differential Leveling Warning [mm] *)
    c_rDrumLeveling_Deadband          : REAL := 3.000;    (* Leveling Differential Hysteresis [mm] *)

    (* ISA-18.2 Internal Process Alarm Bit Latches *)
    rPrevSwayAngle_deg                : REAL := 0.0;
    rROC_SwayAngle                    : REAL := 0.0;
    rPrevWindSpeed_mps                : REAL := 6.5;
    rROC_WindSpeed                    : REAL := 0.0;

    bAlarm_TrolleyPos_HI_HI           : BOOL := FALSE;
    bAlarm_TrolleyPos_HI              : BOOL := FALSE;
    bAlarm_TrolleyPos_LO              : BOOL := FALSE;
    bAlarm_TrolleyPos_LO_LO           : BOOL := FALSE;
    bAlarm_TrolleySpeed_HI_HI         : BOOL := FALSE;
    bAlarm_TrolleySpeed_HI            : BOOL := FALSE;
    bAlarm_HoistSpeed_HI_HI           : BOOL := FALSE;
    bAlarm_HoistSpeed_HI              : BOOL := FALSE;
    bAlarm_SwayAngle_HI_HI            : BOOL := FALSE;
    bAlarm_SwayAngle_HI               : BOOL := FALSE;
    bAlarm_SwayAngle_ROC              : BOOL := FALSE;
    bAlarm_SkewAngle_HI_HI            : BOOL := FALSE;
    bAlarm_SkewAngle_HI               : BOOL := FALSE;
    bAlarm_WindSpeed_HI_HI            : BOOL := FALSE;
    bAlarm_WindSpeed_HI               : BOOL := FALSE;
    bAlarm_TwistlockPress_LO_LO       : BOOL := FALSE;
    bAlarm_TwistlockPress_LO          : BOOL := FALSE;
    bAlarm_EccentricLoad_HI_HI        : BOOL := FALSE;
    bAlarm_EccentricLoad_HI           : BOOL := FALSE;
    bAlarm_DrumLeveling_HI_HI         : BOOL := FALSE;
    bAlarm_DrumLeveling_HI            : BOOL := FALSE;
    bAlarm_TMR_SensorDegraded         : BOOL := FALSE;
    bAlarm_CellGuideCollision_HI_HI   : BOOL := FALSE;

    (* 12-Stage Operational FSM Registers & Sequence Step Timers *)
    iFSM_State                        : INT := 1;         (* Current Active FSM State [1..12] *)
    iNextFSM_State                    : INT := 1;         (* Next Projected FSM State [1..12] *)
    rStateDwellTimer_s                : REAL := 0.0;      (* Active FSM State Dwell Chronometer [s] *)
    rTotalCycleTimer_s                : REAL := 0.0;      (* Total Container Handling Move Duration [s] *)
    rPrecheckTimer_s                  : REAL := 0.0;      (* Pre-Flight Brake & Resolver Test Timer [s] *)
    rGantryTravelTimer_s              : REAL := 0.0;      (* Gantry Rail Alignment Dwell Timer [s] *)
    rDescendTimer_s                   : REAL := 0.0;      (* High-Speed Empty Spreader Descent Timer [s] *)
    rLidarAlignmentTimer_s            : REAL := 0.0;      (* Cell Guide Dynamic Centering Dwell Timer [s] *)
    rTwistlockLockTimer_s             : REAL := 0.0;      (* Twistlock Insertion & 180 bar Locking Timer [s] *)
    rHoistTensionTimer_s              : REAL := 0.0;      (* Pre-Lift Wire Rope Tensioning Dwell Timer [s] *)
    rAccRampTimer_s                   : REAL := 0.0;      (* Trolley Anti-Sway Acceleration Ramp Timer [s] *)
    rCruiseTimer_s                    : REAL := 0.0;      (* Constant Speed 4.0 m/s Quay Apron Cruise Timer [s] *)
    rDecelArrestTimer_s               : REAL := 0.0;      (* Deceleration Anti-Sway Terminal Damping Timer [s] *)
    rChassisLandingTimer_s            : REAL := 0.0;      (* Soft Landing Load Release Touchdown Timer [s] *)
    rTwistlockUnlockTimer_s           : REAL := 0.0;      (* Twistlock Hydraulic Unlock & Clear Timer [s] *)
    rEmergencyBrakeTimer_s            : REAL := 0.0;      (* Caliper Disc Emergency Brake Fast Arrest Timer [s] *)

    (* Internal Loop Iterators & Matrix Scratch Registers *)
    iIdx                              : INT := 0;
    jIdx                              : INT := 0;
    kIdx                              : INT := 0;
    mIdx                              : INT := 0;
    iterMPC                           : INT := 0;
    bMatricesInitialized              : BOOL := FALSE;
    rDiffAB                           : REAL := 0.0;
    rDiffBC                           : REAL := 0.0;
    rDiffCA                           : REAL := 0.0;
    bAgreeAB                          : BOOL := FALSE;
    bAgreeBC                          : BOOL := FALSE;
    bAgreeCA                          : BOOL := FALSE;
    rTempSum                          : REAL := 0.0;
    rTempGrad                         : REAL := 0.0;
    rTotalSuspendedMass_kg            : REAL := 50500.0;
    rCurrentRopeLength_m              : REAL := 30.0;
    rCurrentHoistSpeed_mps            : REAL := 0.0;
    rOmegaPendulum                    : REAL := 0.5717;
    rOmegaSkew                        : REAL := 0.1668;
    rRelWindSpeed                     : REAL := 0.0;
    rFrontalArea                      : REAL := 35.3;
    rLevelingError_mm                 : REAL := 0.0;
    rTrolleySpeedTarget_mps           : REAL := 0.0;
    rTrolleyAccTarget_mps2            : REAL := 0.0;
    rHoistSpeedTarget_mps             : REAL := 0.0;
END_VAR""")

    # -------------------------------------------------------------------------------------------------
    # PHASE 0: MODEL MATRICES & CONTROL COEFFICIENT INITIALIZATION
    # -------------------------------------------------------------------------------------------------
    sections.append("""(* ===================================================================================================================
 * PHASE 0: MODEL MATRICES & CONTROL COEFFICIENT INITIALIZATION
 * =================================================================================================================== *)
IF NOT bMatricesInitialized THEN
    (* 8x8 Multivariable State-Space System Matrix A Discretized at Ts = 10.0 ms *)
    (* States: 1=Delta_x_tr [m], 2=Delta_v_tr [m/s], 3=theta [rad], 4=d(theta)/dt [rad/s], 5=phi [rad], 6=d(phi)/dt [rad/s], 7=Delta_L [m], 8=Delta_v_h [m/s] *)
    (* Row 1: Trolley Position Kinematics (x_tr[k+1] = x_tr[k] + Ts * v_tr[k]) *)
    aA[1, 1] := 1.00000; aA[1, 2] := 0.01000; aA[1, 3] := 0.00000; aA[1, 4] := 0.00000; aA[1, 5] := 0.00000; aA[1, 6] := 0.00000; aA[1, 7] := 0.00000; aA[1, 8] := 0.00000;
    (* Row 2: Trolley Velocity Dynamics (Including Rail Rolling Resistance & Wire Rope Reaction) *)
    aA[2, 1] := 0.00000; aA[2, 2] := 0.99850; aA[2, 3] := 0.00015; aA[2, 4] := 0.00000; aA[2, 5] := 0.00000; aA[2, 6] := 0.00000; aA[2, 7] := 0.00000; aA[2, 8] := 0.00000;
    (* Row 3: Spreader Pendulum Sway Kinematics (theta[k+1] = theta[k] + Ts * d(theta)/dt[k]) *)
    aA[3, 1] := 0.00000; aA[3, 2] := 0.00000; aA[3, 3] := 1.00000; aA[3, 4] := 0.01000; aA[3, 5] := 0.00000; aA[3, 6] := 0.00000; aA[3, 7] := 0.00000; aA[3, 8] := 0.00000;
    (* Row 4: Pendulum Angular Acceleration: d2(theta)/dt2 = -(g/L)*theta - 2*(v_h/L)*d(theta)/dt - 2*zeta*omega*d(theta)/dt *)
    (* Nominal baseline at L0 = 30.0 m: -g/L0 * Ts = -(9.80665 / 30.0) * 0.010 = -0.0032689; 1.0 - 2*zeta*omega*Ts = 0.99983 *)
    aA[4, 1] := 0.00000; aA[4, 2] := 0.00000; aA[4, 3] := -0.00327; aA[4, 4] := 0.99983; aA[4, 5] := 0.00000; aA[4, 6] := 0.00000; aA[4, 7] := 0.00002; aA[4, 8] := 0.00000;
    (* Row 5: Spreader Skew Torsion Kinematics (phi[k+1] = phi[k] + Ts * d(phi)/dt[k]) *)
    aA[5, 1] := 0.00000; aA[5, 2] := 0.00000; aA[5, 3] := 0.00000; aA[5, 4] := 0.00000; aA[5, 5] := 1.00000; aA[5, 6] := 0.01000; aA[5, 7] := 0.00000; aA[5, 8] := 0.00000;
    (* Row 6: Skew Torsional Acceleration: d2(phi)/dt2 = -(K_tors/I_zz)*phi - 2*zeta_phi*omega_phi*d(phi)/dt *)
    (* Baseline at L0 = 30.0 m: -(g*W^2 / (4*L0*R_gyr^2)) * Ts = -0.0002781; 1.0 - 2*zeta_phi*omega_phi*Ts = 0.99983 *)
    aA[6, 1] := 0.00000; aA[6, 2] := 0.00000; aA[6, 3] := 0.00000; aA[6, 4] := 0.00000; aA[6, 5] := -0.00028; aA[6, 6] := 0.99983; aA[6, 7] := 0.00001; aA[6, 8] := 0.00000;
    (* Row 7: Hoist Rope Payout Kinematics (L[k+1] = L[k] + Ts * v_h[k]) *)
    aA[7, 1] := 0.00000; aA[7, 2] := 0.00000; aA[7, 3] := 0.00000; aA[7, 4] := 0.00000; aA[7, 5] := 0.00000; aA[7, 6] := 0.00000; aA[7, 7] := 1.00000; aA[7, 8] := 0.01000;
    (* Row 8: Hoist Vertical Velocity Dynamics (Inverter Speed Loop Closed Response) *)
    aA[8, 1] := 0.00000; aA[8, 2] := 0.00000; aA[8, 3] := 0.00000; aA[8, 4] := 0.00000; aA[8, 5] := 0.00000; aA[8, 6] := 0.00000; aA[8, 7] := 0.00000; aA[8, 8] := 0.99900;

    (* 8x6 Multivariable Discrete Input Coupling Matrix B *)
    (* Inputs: 1=a_tr_cmd [m/s2], 2=a_h_ws [m/s2], 3=a_h_ls [m/s2], 4=v_skew1 [%], 5=v_skew2 [%], 6=F_anti_sway [kN] *)
    (* Row 1: Delta_x_tr response *)
    aB[1, 1] := 0.00005; aB[1, 2] := 0.00000; aB[1, 3] := 0.00000; aB[1, 4] := 0.00000; aB[1, 5] := 0.00000; aB[1, 6] := 0.00000;
    (* Row 2: Delta_v_tr response *)
    aB[2, 1] := 0.01000; aB[2, 2] := 0.00000; aB[2, 3] := 0.00000; aB[2, 4] := 0.00000; aB[2, 5] := 0.00000; aB[2, 6] := 0.000002;
    (* Row 3: theta response *)
    aB[3, 1] := -0.0000017; aB[3, 2] := 0.00000; aB[3, 3] := 0.00000; aB[3, 4] := 0.00000; aB[3, 5] := 0.00000; aB[3, 6] := 0.00000;
    (* Row 4: d(theta)/dt response: -(1/L0)*Ts = -(1.0 / 30.0)*0.010 = -0.0003333 *)
    aB[4, 1] := -0.000333; aB[4, 2] := 0.00000; aB[4, 3] := 0.00000; aB[4, 4] := 0.00000; aB[4, 5] := 0.00000; aB[4, 6] := -0.0000008;
    (* Row 5: phi response *)
    aB[5, 1] := 0.00000; aB[5, 2] := 0.0000005; aB[5, 3] := -0.0000005; aB[5, 4] := 0.000004; aB[5, 5] := -0.000004; aB[5, 6] := 0.00000;
    (* Row 6: d(phi)/dt response: Skew hydraulic trim valves and differential hoist acceleration *)
    aB[6, 1] := 0.00000; aB[6, 2] := 0.00012; aB[6, 3] := -0.00012; aB[6, 4] := 0.00085; aB[6, 5] := -0.00085; aB[6, 6] := 0.00000;
    (* Row 7: Delta_L response *)
    aB[7, 1] := 0.00000; aB[7, 2] := 0.000025; aB[7, 3] := 0.000025; aB[7, 4] := 0.00000; aB[7, 5] := 0.00000; aB[7, 6] := 0.00000;
    (* Row 8: Delta_v_h response: Dual hoist acceleration (0.5 on each drum set) *)
    aB[8, 1] := 0.00000; aB[8, 2] := 0.00500; aB[8, 3] := 0.00500; aB[8, 4] := 0.00000; aB[8, 5] := 0.00000; aB[8, 6] := 0.00000;

    (* 8x8 Output Measurement Matrix C (Direct Diagonal State Reconstruction) *)
    FOR iIdx := 1 TO 8 DO
        FOR jIdx := 1 TO 8 DO
            IF iIdx = jIdx THEN
                aC[iIdx, jIdx] := 1.00000;
            ELSE
                aC[iIdx, jIdx] := 0.00000;
            END_IF;
        END_FOR;
    END_FOR;

    (* 8x6 Direct Feedthrough Matrix D (Strictly Proper Dynamics D = 0) *)
    FOR iIdx := 1 TO 8 DO
        FOR jIdx := 1 TO 6 DO
            aD[iIdx, jIdx] := 0.00000;
        END_FOR;
    END_FOR;

    (* Model Predictive Control (MPC) Cost Weighting Matrices Diag(Q), Diag(R), Diag(S), Diag(P) *)
    (* Q State Penalties: High penalties on sway angle (x3), sway velocity (x4), and skew angle (x5) *)
    aQ_Weight[1] := 15.0;     (* x1: Trolley Position Error [m] *)
    aQ_Weight[2] := 8.0;      (* x2: Trolley Velocity Error [m/s] *)
    aQ_Weight[3] := 125000.0; (* x3: Pendulum Sway Angle [rad] (Crucial: 0.10 deg = 0.00175 rad) *)
    aQ_Weight[4] := 45000.0;  (* x4: Sway Angular Velocity [rad/s] *)
    aQ_Weight[5] := 85000.0;  (* x5: Spreader Skew Torsion [rad] *)
    aQ_Weight[6] := 25000.0;  (* x6: Skew Angular Velocity [rad/s] *)
    aQ_Weight[7] := 12.0;     (* x7: Hoist Length Error [m] *)
    aQ_Weight[8] := 6.0;      (* x8: Hoist Velocity Error [m/s] *)

    (* R Actuator Effort Penalties *)
    aR_Weight[1] := 2.50;     (* u1: Trolley Accel [m/s2] *)
    aR_Weight[2] := 1.20;     (* u2: Hoist WS Accel [m/s2] *)
    aR_Weight[3] := 1.20;     (* u3: Hoist LS Accel [m/s2] *)
    aR_Weight[4] := 0.45;     (* u4: Skew Valve 1 [%] *)
    aR_Weight[5] := 0.45;     (* u5: Skew Valve 2 [%] *)
    aR_Weight[6] := 0.15;     (* u6: Anti-Sway Force [kN] *)

    (* S Actuator Slew Rate Penalties (Jerk Minimization) *)
    aS_Weight[1] := 18.0;     (* Delta_u1: Trolley Jerk *)
    aS_Weight[2] := 12.0;     (* Delta_u2: Hoist WS Jerk *)
    aS_Weight[3] := 12.0;     (* Delta_u3: Hoist LS Jerk *)
    aS_Weight[4] := 2.5;      (* Delta_u4: Skew Valve 1 Slew *)
    aS_Weight[5] := 2.5;      (* Delta_u5: Skew Valve 2 Slew *)
    aS_Weight[6] := 1.0;      (* Delta_u6: Anti-Sway Force Slew *)

    (* P Terminal Cost Penalties *)
    aP_TerminalWeight[1] := 35.0;
    aP_TerminalWeight[2] := 18.0;
    aP_TerminalWeight[3] := 250000.0; (* Massive terminal deadbeat penalty on residual sway *)
    aP_TerminalWeight[4] := 95000.0;
    aP_TerminalWeight[5] := 150000.0;
    aP_TerminalWeight[6] := 45000.0;
    aP_TerminalWeight[7] := 25.0;
    aP_TerminalWeight[8] := 12.0;

    (* Hard Actuator Saturation & Slew Bounds *)
    au_min[1] := -1.200;  au_max[1] := 1.200;   adelta_u_max[1] := 0.050; (* Trolley Accel Max Slew 5.0 m/s3 *)
    au_min[2] := -1.500;  au_max[2] := 1.500;   adelta_u_max[2] := 0.060; (* Hoist WS Accel Max Slew 6.0 m/s3 *)
    au_min[3] := -1.500;  au_max[3] := 1.500;   adelta_u_max[3] := 0.060; (* Hoist LS Accel Max Slew 6.0 m/s3 *)
    au_min[4] := -100.0;  au_max[4] := 100.0;   adelta_u_max[4] := 15.00; (* Skew Valve 1 Slew 15 %/scan *)
    au_min[5] := -100.0;  au_max[5] := 100.0;   adelta_u_max[5] := 15.00; (* Skew Valve 2 Slew 15 %/scan *)
    au_min[6] := -85.00;  au_max[6] := 85.00;   adelta_u_max[6] := 12.00; (* Anti-Sway Force Slew 12 kN/scan *)

    bMatricesInitialized := TRUE;
END_IF;""")

    # -------------------------------------------------------------------------------------------------
    # PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING ENGINES
    # -------------------------------------------------------------------------------------------------
    # Generate voting blocks for all 11 triplets!
    triplets = [
        ("ZT_TROLLEY_ENCODER_101", "rTrolleyPosVoted_m", "c_rTol_TrolleyPos_m", "rTimer_TrolleyPos_Disc_s", "bIso_TrolleyPos_ChA", "bIso_TrolleyPos_ChB", "bIso_TrolleyPos_ChC", "Trolley Laser Absolute Position [m]"),
        ("ST_TROLLEY_MOTOR_RPM_102", "rTrolleySpeedVoted_mps", "c_rTol_TrolleySpeed_RPM", "rTimer_TrolleySpeed_Disc_s", "bIso_TrolleySpeed_ChA", "bIso_TrolleySpeed_ChB", "bIso_TrolleySpeed_ChC", "Trolley Motor Drive Speed [RPM] (Converted to Linear Velocity m/s)"),
        ("ZT_HOIST_ROPE_LENGTH_201", "rHoistRopeLengthVoted_m", "c_rTol_HoistRopeLength_m", "rTimer_HoistLength_Disc_s", "bIso_HoistLength_ChA", "bIso_HoistLength_ChB", "bIso_HoistLength_ChC", "Hoist Wire Rope Payout Length L(t) [m]"),
        ("ST_HOIST_MOTOR_RPM_202", "rHoistSpeedVoted_mps", "c_rTol_HoistSpeed_RPM", "rTimer_HoistSpeed_Disc_s", "bIso_HoistSpeed_ChA", "bIso_HoistSpeed_ChB", "bIso_HoistSpeed_ChC", "Dual-Hoist Main Vector Drive Motor Resolvers [RPM] (Converted to Linear Payout Speed m/s)"),
        ("OPT_SPREADER_SWAY_ANGLE_301", "rSwayAngleVoted_deg", "c_rTol_SwayAngle_deg", "rTimer_SwayAngle_Disc_s", "bIso_SwayAngle_ChA", "bIso_SwayAngle_ChB", "bIso_SwayAngle_ChC", "Optical IR Spreader Sway Camera Angle theta [deg]"),
        ("OPT_SPREADER_SKEW_ANGLE_302", "rSkewAngleVoted_deg", "c_rTol_SkewAngle_deg", "rTimer_SkewAngle_Disc_s", "bIso_SkewAngle_ChA", "bIso_SkewAngle_ChB", "bIso_SkewAngle_ChC", "Optical IR Spreader Skew Camera Angle phi [deg]"),
        ("LIDAR_CELL_GUIDE_DIST_401", "rCellGuideDistVoted_mm", "c_rTol_CellGuideDist_mm", "rTimer_CellGuide_Disc_s", "bIso_CellGuide_ChA", "bIso_CellGuide_ChB", "bIso_CellGuide_ChC", "2D Laser Lidar Spreader-to-Cell-Guide Clearance [mm]"),
        ("WT_SPREADER_LOAD_CELL_501", "rTotalLoadVoted_tonnes", "c_rTol_LoadCell_tonnes", "rTimer_LoadCell_Disc_s", "bIso_LoadCell_ChA", "bIso_LoadCell_ChB", "bIso_LoadCell_ChC", "4-Corner Spreader Pin Load Cells [tonnes]"),
        ("PT_TWISTLOCK_HYDR_PRESS_601", "rTwistlockPressureVoted_bar", "c_rTol_TwistlockPress_bar", "rTimer_TwistlockPress_Disc_s", "bIso_TwistlockPress_ChA", "bIso_TwistlockPress_ChB", "bIso_TwistlockPress_ChC", "Twistlock Hydraulic Manifold Actuation Pressure [bar]"),
        ("AIT_ANEMOMETER_WIND_SPEED_701", "rWindSpeedVoted_mps", "c_rTol_WindSpeed_mps", "rTimer_WindSpeed_Disc_s", "bIso_WindSpeed_ChA", "bIso_WindSpeed_ChB", "bIso_WindSpeed_ChC", "Ultrasonic 2-Axis Boom Tip Anemometer [m/s]"),
        ("ZT_RAIL_CLAMP_STATUS_801", "rStormRailClampPressureVoted_bar", "c_rTol_RailClampPress_bar", "rTimer_RailClampPress_Disc_s", "bIso_RailClampPress_ChA", "bIso_RailClampPress_ChB", "bIso_RailClampPress_ChC", "Storm Rail Clamp Hydraulic Locking Pressure [bar]")
    ]

    tmr_st = []
    tmr_st.append("""(* ===================================================================================================================
 * PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING ENGINES
 * =================================================================================================================== *)""")
    
    for tag_base, out_var, tol_var, timer_var, iso_a, iso_b, iso_c, desc in triplets:
        sub = f"""(* --- Voter Engine: {tag_base} ({desc}) --- *)
rDiffAB := ABS({tag_base}A - {tag_base}B);
rDiffBC := ABS({tag_base}B - {tag_base}C);
rDiffCA := ABS({tag_base}C - {tag_base}A);
bAgreeAB := (rDiffAB <= {tol_var});
bAgreeBC := (rDiffBC <= {tol_var});
bAgreeCA := (rDiffCA <= {tol_var});

IF bAgreeAB AND bAgreeBC AND bAgreeCA THEN
    (* Unanimous Agreement: Select Median Value Across Channels A, B, C *)
    IF ({tag_base}A >= {tag_base}B AND {tag_base}A <= {tag_base}C) OR ({tag_base}A <= {tag_base}B AND {tag_base}A >= {tag_base}C) THEN
        {out_var} := {tag_base}A;
    ELSIF ({tag_base}B >= {tag_base}A AND {tag_base}B <= {tag_base}C) OR ({tag_base}B <= {tag_base}A AND {tag_base}B >= {tag_base}C) THEN
        {out_var} := {tag_base}B;
    ELSE
        {out_var} := {tag_base}C;
    END_IF;
    {timer_var} := 0.0;
    {iso_a} := FALSE;
    {iso_b} := FALSE;
    {iso_c} := FALSE;
ELSIF bAgreeAB THEN
    (* Channel C Outlier Detected: Degrade to 2-Channel Mean (A, B) *)
    {out_var} := ({tag_base}A + {tag_base}B) * 0.50;
    {timer_var} := {timer_var} + c_rTs;
    IF {timer_var} >= c_rTMR_PersistencyTimeout_s THEN
        {iso_c} := TRUE;
        bAlarm_TMR_SensorDegraded := TRUE;
    END_IF;
ELSIF bAgreeBC THEN
    (* Channel A Outlier Detected: Degrade to 2-Channel Mean (B, C) *)
    {out_var} := ({tag_base}B + {tag_base}C) * 0.50;
    {timer_var} := {timer_var} + c_rTs;
    IF {timer_var} >= c_rTMR_PersistencyTimeout_s THEN
        {iso_a} := TRUE;
        bAlarm_TMR_SensorDegraded := TRUE;
    END_IF;
ELSIF bAgreeCA THEN
    (* Channel B Outlier Detected: Degrade to 2-Channel Mean (C, A) *)
    {out_var} := ({tag_base}C + {tag_base}A) * 0.50;
    {timer_var} := {timer_var} + c_rTs;
    IF {timer_var} >= c_rTMR_PersistencyTimeout_s THEN
        {iso_b} := TRUE;
        bAlarm_TMR_SensorDegraded := TRUE;
    END_IF;
ELSE
    (* Catastrophic 2oo3 Discrepancy Fault: All Channels Diverged Beyond Safety Limits *)
    {timer_var} := {timer_var} + c_rTs;
    IF {timer_var} >= c_rTMR_PersistencyTimeout_s THEN
        {iso_a} := TRUE;
        {iso_b} := TRUE;
        {iso_c} := TRUE;
        bAlarm_TMR_SensorDegraded := TRUE;
    END_IF;
END_IF;"""
        if tag_base == "ST_TROLLEY_MOTOR_RPM_102":
            # Convert motor RPM to trolley linear speed: v = (RPM / 60) * (2*pi*R_wheel) / GearRatio
            sub += f"""
(* Convert Voted Resolver RPM to Linear Trolley Velocity [m/s] *)
rTrolleySpeedVoted_mps := ((rTrolleySpeedVoted_mps / 60.0) * (2.0 * c_rPi * c_rTrolleyWheelRadius_m)) / c_rTrolleyGearRatio;"""
        elif tag_base == "ST_HOIST_MOTOR_RPM_202":
            # Convert motor RPM to hoist linear payout speed: v = (RPM / 60) * (2*pi*R_drum) / GearRatio
            sub += f"""
(* Convert Voted Hoist Resolver RPM to Linear Payout Speed [m/s] *)
rHoistSpeedVoted_mps := ((rHoistSpeedVoted_mps / 60.0) * (2.0 * c_rPi * c_rHoistDrumRadius_m)) / c_rHoistGearRatio;"""

        tmr_st.append(sub)

    sections.append("\n\n".join(tmr_st))

    # -------------------------------------------------------------------------------------------------
    # PHASE 2: REAL-TIME CYBER-PHYSICAL PROPERTY ESTIMATION & DYNAMICS OBSERVER
    # -------------------------------------------------------------------------------------------------
    sections.append("""(* ===================================================================================================================
 * PHASE 2: REAL-TIME CYBER-PHYSICAL PROPERTY ESTIMATION & DYNAMICS OBSERVER
 * =================================================================================================================== *)
(* 1. Instantaneous Effective Pendulum Suspension Length L(t) & Vertical Speed *)
rCurrentRopeLength_m := MAX(rHoistRopeLengthVoted_m, 2.50); (* Enforce physical minimum boom limit 2.5 m *)
rCurrentHoistSpeed_mps := rHoistSpeedVoted_mps;

(* 2. Suspended Load Mass & Spreader Tare Dynamic Estimation *)
rTotalSuspendedMass_kg := c_rSpreaderTareMass_kg + (rTotalLoadVoted_tonnes * 1000.0);
IF rTotalSuspendedMass_kg > (c_rSpreaderTareMass_kg + c_rMaxRatedLoad_kg) THEN
    rTotalSuspendedMass_kg := c_rSpreaderTareMass_kg + c_rMaxRatedLoad_kg;
END_IF;

(* 3. Real-Time Spherical Pendulum Natural Frequency omega_n(t) = sqrt(g / L(t)) *)
rOmegaPendulum := SQRT(c_rG / rCurrentRopeLength_m);
rPendulumNaturalFreq_rad_s := rOmegaPendulum;

(* 4. 4-Wire Reeving Torsional Skew Natural Frequency omega_phi(t) *)
(* Torsional stiffness K_tors = (M_total * g * W_reev^2) / (4 * L) *)
rOmegaSkew := SQRT((rTotalSuspendedMass_kg * c_rG * (c_rReevingSheaveWidth_m * c_rReevingSheaveWidth_m)) / (4.0 * rCurrentRopeLength_m * c_rSpreaderInertiaYaw_kg_m2));

(* 5. Container Bluff-Body Aerodynamic Drag Load Estimation *)
(* Relative wind velocity in direction of trolley travel *)
rRelWindSpeed := rWindSpeedVoted_mps - rTrolleySpeedVoted_mps;
IF bSpreader20ftMode THEN
    rFrontalArea := 17.65; (* 20-foot container projected area [m2] *)
ELSIF bSpreader45ftMode THEN
    rFrontalArea := 39.70; (* 45-foot container projected area [m2] *)
ELSE
    rFrontalArea := c_rContainerFrontalArea_m2; (* Standard 40-foot High-Cube 35.3 m2 *)
END_IF;

(* Dynamic drag equation: F_drag = 0.5 * rho * C_d * A * v_rel * |v_rel| *)
rWindAerodynamicDragForce_kN := (0.50 * c_rAirDensity_kg_m3 * c_rDragCoeffContainer * rFrontalArea * rRelWindSpeed * ABS(rRelWindSpeed)) / 1000.0;

(* 6. Spreader Angular Velocity State Filtering (Low-Pass Differentiator) *)
rSwayAngularVel_deg_s := (rSwayAngleVoted_deg - rPrevSwayAngle_deg) / c_rTs;
rROC_SwayAngle := ABS(rSwayAngularVel_deg_s);
rPrevSwayAngle_deg := rSwayAngleVoted_deg;

(* Wind Speed Rate-of-Change Filter *)
rROC_WindSpeed := ABS(rWindSpeedVoted_mps - rPrevWindSpeed_mps) / c_rTs;
rPrevWindSpeed_mps := rWindSpeedVoted_mps;

(* 7. Phase-Plane Residual Sway Amplitude Calculation *)
(* State trajectory phase radius: theta_res = sqrt(theta^2 + (d_theta / omega_n)^2) *)
rResidualSwayAngle_deg := SQRT((rSwayAngleVoted_deg * rSwayAngleVoted_deg) + (((rSwayAngularVel_deg_s * c_rDegToRad) / MAX(rOmegaPendulum, 0.05)) * ((rSwayAngularVel_deg_s * c_rDegToRad) / MAX(rOmegaPendulum, 0.05)) * c_rRadToDeg * c_rRadToDeg));

(* 8. Dual-Hoist Drum Leveling Synchronization Discrepancy *)
(* Measure differential position between Water-Side Drums (1 & 2) and Land-Side Drums (3 & 4) *)
rLevelingError_mm := (ST_HOIST_MOTOR_RPM_202A - ST_HOIST_MOTOR_RPM_202B) * 0.125;
rDrumLevelingDiscrepancy_mm := rLevelingError_mm;""")

    # -------------------------------------------------------------------------------------------------
    # PHASE 3: DISCRETE STATE-SPACE MODEL & RECEDING-HORIZON MPC CONTROLLER
    # -------------------------------------------------------------------------------------------------
    sections.append("""(* ===================================================================================================================
 * PHASE 3: DISCRETE STATE-SPACE MODEL & RECEDING-HORIZON MPC CONTROLLER
 * =================================================================================================================== *)
(* 1. Populate System State Vector x[1..8] from Physical Transmitters & Observers *)
ax_state[1] := rTrolleyPosVoted_m - rTargetTrolleyPos_m;
ax_state[2] := rTrolleySpeedVoted_mps - rTrolleySpeedTarget_mps;
ax_state[3] := rSwayAngleVoted_deg * c_rDegToRad;
ax_state[4] := rSwayAngularVel_deg_s * c_rDegToRad;
ax_state[5] := rSkewAngleVoted_deg * c_rDegToRad;
ax_state[6] := rSkewAngularVel_deg_s * c_rDegToRad;
ax_state[7] := rHoistRopeLengthVoted_m - rTargetHoistPos_m;
ax_state[8] := rHoistSpeedVoted_mps - rHoistSpeedTarget_mps;

(* Desired Target State Equilibrium Vector x_ref[1..8] *)
FOR iIdx := 1 TO 8 DO
    ax_ref[iIdx] := 0.00000;
END_FOR;

(* 2. Real-Time Linearized Parameter Updates of Matrices A and B Based on L(t) and v_h(t) *)
(* Row 4: Pendulum dynamics update *)
aA[4, 3] := - (c_rG / rCurrentRopeLength_m) * c_rTs;
aA[4, 4] := 1.00000 - ((2.0 * c_rSwayDampingRatio * rOmegaPendulum) + (2.0 * rCurrentHoistSpeed_mps / rCurrentRopeLength_m)) * c_rTs;
aB[4, 1] := - (1.00000 / rCurrentRopeLength_m) * c_rTs;

(* Row 6: Skew dynamics update *)
aA[6, 5] := - (rOmegaSkew * rOmegaSkew) * c_rTs;
aA[6, 6] := 1.00000 - (2.0 * c_rSkewDampingRatio * rOmegaSkew) * c_rTs;

(* 3. Store Previous Actuator Input Vector u_prev *)
FOR mIdx := 1 TO 6 DO
    au_prev[mIdx] := au_control[mIdx];
END_FOR;

(* 4. Receding-Horizon Optimization via 3-Iteration Projected Gradient Descent (PGD) *)
FOR iterMPC := 1 TO 3 DO
    (* Step A: Predict 1-Step Horizon Future State: x_pred = A * x_state + B * u_control *)
    FOR iIdx := 1 TO 8 DO
        rTempSum := 0.0;
        FOR jIdx := 1 TO 8 DO
            rTempSum := rTempSum + (aA[iIdx, jIdx] * ax_state[jIdx]);
        END_FOR;
        FOR mIdx := 1 TO 6 DO
            rTempSum := rTempSum + (aB[iIdx, mIdx] * au_control[mIdx]);
        END_FOR;
        aPredictedState[iIdx] := rTempSum;
    END_FOR;

    (* Step B: Evaluate Quadratic Objective Cost Function J *)
    (* J = 0.5 * sum(Q_i * (x_pred_i - x_ref_i)^2) + 0.5 * sum(R_m * u_m^2) + 0.5 * sum(S_m * (u_m - u_prev_m)^2) + 0.5 * sum(P_i * x_pred_i^2) *)
    rMPC_ObjectiveCostJ := 0.0;
    FOR iIdx := 1 TO 8 DO
        rMPC_ObjectiveCostJ := rMPC_ObjectiveCostJ + (0.50 * aQ_Weight[iIdx] * (aPredictedState[iIdx] - ax_ref[iIdx]) * (aPredictedState[iIdx] - ax_ref[iIdx]));
        rMPC_ObjectiveCostJ := rMPC_ObjectiveCostJ + (0.50 * aP_TerminalWeight[iIdx] * aPredictedState[iIdx] * aPredictedState[iIdx]);
    END_FOR;
    FOR mIdx := 1 TO 6 DO
        rMPC_ObjectiveCostJ := rMPC_ObjectiveCostJ + (0.50 * aR_Weight[mIdx] * au_control[mIdx] * au_control[mIdx]);
        rMPC_ObjectiveCostJ := rMPC_ObjectiveCostJ + (0.50 * aS_Weight[mIdx] * (au_control[mIdx] - au_prev[mIdx]) * (au_control[mIdx] - au_prev[mIdx]));
    END_FOR;

    (* Step C: Compute Analytical Gradient of Cost Functional dJ/du_m *)
    (* grad_m = sum_i( B[i, m] * (Q[i] + P[i]) * (x_pred[i] - x_ref[i]) ) + R[m] * u[m] + S[m] * (u[m] - u_prev[m]) *)
    FOR mIdx := 1 TO 6 DO
        rTempGrad := 0.0;
        FOR iIdx := 1 TO 8 DO
            rTempGrad := rTempGrad + (aB[iIdx, mIdx] * (aQ_Weight[iIdx] + aP_TerminalWeight[iIdx]) * (aPredictedState[iIdx] - ax_ref[iIdx]));
        END_FOR;
        rTempGrad := rTempGrad + (aR_Weight[mIdx] * au_control[mIdx]);
        rTempGrad := rTempGrad + (aS_Weight[mIdx] * (au_control[mIdx] - au_prev[mIdx]));
        aGrad_u[mIdx] := rTempGrad;
    END_FOR;

    (* Step D: Projected Gradient Descent Step with Actuator Slew & Hard Saturation Constraints *)
    FOR mIdx := 1 TO 6 DO
        (* Unconstrained Gradient Descent Step *)
        au_control[mIdx] := au_control[mIdx] - (c_rPGD_Alpha * aGrad_u[mIdx]);

        (* Slew Rate Clamping *)
        au_delta[mIdx] := au_control[mIdx] - au_prev[mIdx];
        IF au_delta[mIdx] > adelta_u_max[mIdx] THEN
            au_delta[mIdx] := adelta_u_max[mIdx];
        ELSIF au_delta[mIdx] < -adelta_u_max[mIdx] THEN
            au_delta[mIdx] := -adelta_u_max[mIdx];
        END_IF;
        au_control[mIdx] := au_prev[mIdx] + au_delta[mIdx];

        (* Hard Saturation Limits *)
        IF au_control[mIdx] > au_max[mIdx] THEN
            au_control[mIdx] := au_max[mIdx];
        ELSIF au_control[mIdx] < au_min[mIdx] THEN
            au_control[mIdx] := au_min[mIdx];
        END_IF;
    END_FOR;
END_FOR;

(* 5. Actuator Command Synthesis from Optimal Inputs *)
(* u1: Trolley Acceleration Command -> Flux-Vector Torque Reference *)
(* T_trolley = ((M_trolley + M_load)*a_cmd + F_drag + F_antisway) * R_wheel / GearRatio *)
rCmd_TrolleyDriveTorque_Nm := (((c_rTrolleyMass_kg + rTotalSuspendedMass_kg) * au_control[1] + (rWindAerodynamicDragForce_kN * 1000.0) + (au_control[6] * 1000.0)) * c_rTrolleyWheelRadius_m) / c_rTrolleyGearRatio;

(* Enforce Trolley Vector Inverter Torque Limit *)
IF rCmd_TrolleyDriveTorque_Nm > c_rTrolleyMotorRatedTorque_Nm THEN
    rCmd_TrolleyDriveTorque_Nm := c_rTrolleyMotorRatedTorque_Nm;
ELSIF rCmd_TrolleyDriveTorque_Nm < -c_rTrolleyMotorRatedTorque_Nm THEN
    rCmd_TrolleyDriveTorque_Nm := -c_rTrolleyMotorRatedTorque_Nm;
END_IF;

(* Trolley Motor Speed Reference Setpoint [RPM] *)
rCmd_TrolleyDriveSpeed_RPM := ((rTrolleySpeedTarget_mps + (au_control[1] * c_rTs)) / (2.0 * c_rPi * c_rTrolleyWheelRadius_m)) * 60.0 * c_rTrolleyGearRatio;

(* u2 & u3: Dual-Hoist Water-Side & Land-Side Drum Speed References [RPM] with Cross-Coupled Leveling Compensation *)
rCmd_HoistWatersideSpeed_RPM := ((rHoistSpeedTarget_mps + (au_control[2] * c_rTs)) / (2.0 * c_rPi * c_rHoistDrumRadius_m)) * 60.0 * c_rHoistGearRatio - (rDrumLevelingDiscrepancy_mm * 1.50);
rCmd_HoistLandsideSpeed_RPM := ((rHoistSpeedTarget_mps + (au_control[3] * c_rTs)) / (2.0 * c_rPi * c_rHoistDrumRadius_m)) * 60.0 * c_rHoistGearRatio + (rDrumLevelingDiscrepancy_mm * 1.50);

(* u4 & u5: Skew Trim Hydraulic Cylinder Proportional Valve Commands [%] *)
rCmd_SkewTrimValve1_pct := au_control[4];
rCmd_SkewTrimValve2_pct := au_control[5];""")

    # -------------------------------------------------------------------------------------------------
    # PHASE 4: 12-STAGE DETERMINISTIC TERMINAL OPERATIONAL FSM
    # -------------------------------------------------------------------------------------------------
    sections.append("""(* ===================================================================================================================
 * PHASE 4: 12-STAGE DETERMINISTIC TERMINAL OPERATIONAL FINITE STATE MACHINE (FSM)
 * =================================================================================================================== *)
(* Chronometer Updates *)
rStateDwellTimer_s := rStateDwellTimer_s + c_rTs;
IF bBusy THEN
    rTotalCycleTimer_s := rTotalCycleTimer_s + c_rTs;
ELSE
    rTotalCycleTimer_s := 0.0;
END_IF;

(* Master Safety Circuit Interlock Override *)
IF NOT bEmergencyStop_NC OR bAlarm_WindSpeed_HI_HI THEN
    iNextFSM_State := 12; (* Fast Abort to Emergency Trip & Storm Clamp State *)
END_IF;

CASE iFSM_State OF
    1: (* SYSTEM_OFFLINE_BRAKE_LOCKED: Crane Parked, Mechanical Caliper Clamped, Drives Disabled *)
        bReady := FALSE;
        bBusy := FALSE;
        bCycleCompleted := FALSE;
        bEmergencyStopTripped := NOT bEmergencyStop_NC;
        bStormRailClampDeployed := TRUE;
        bCmd_HoistCaliperBrakeRelease := FALSE;
        bCmd_TrolleyParkingBrakeRelease := FALSE;
        bCmd_StormRailClampRelease := FALSE;
        bCmd_TwistlockLockSolenoid := FALSE;
        bCmd_TwistlockUnlockSolenoid := FALSE;
        bCmd_SpreaderFlipperDown := FALSE;
        rCmd_TrolleyDriveTorque_Nm := 0.0;
        rCmd_TrolleyDriveSpeed_RPM := 0.0;
        rCmd_HoistWatersideSpeed_RPM := 0.0;
        rCmd_HoistLandsideSpeed_RPM := 0.0;

        IF bEnable AND bEmergencyStop_NC AND NOT bAlarm_WindSpeed_HI_HI AND NOT bAlarm_TMR_SensorDegraded THEN
            bReady := TRUE;
            IF bAutoCycleStart THEN
                iNextFSM_State := 2; (* Transition to Pre-Check *)
            END_IF;
        END_IF;

    2: (* TROLLEY_HOIST_PRECHECK: Sensor Triplet Verification, Brake Lift Test & Hydraulic HPU Ready *)
        bReady := TRUE;
        bBusy := TRUE;
        bCmd_StormRailClampRelease := TRUE; (* Lift storm clamps for travel *)
        rPrecheckTimer_s := rPrecheckTimer_s + c_rTs;

        (* Check Hydraulic Clamp Release Pressure > 140 bar and No Sensor Trips *)
        IF rStormRailClampPressureVoted_bar >= 140.0 AND rPrecheckTimer_s >= 1.50 THEN
            bCmd_HoistCaliperBrakeRelease := TRUE;
            bCmd_TrolleyParkingBrakeRelease := TRUE;
            bStormRailClampDeployed := FALSE;
            rPrecheckTimer_s := 0.0;
            iNextFSM_State := 3; (* Transition to Bay Travel *)
        ELSIF rPrecheckTimer_s > 5.00 THEN
            (* Timeout Fault: Rail Clamps Failed to Lift *)
            iNextFSM_State := 12;
        END_IF;

    3: (* BAY_POSITION_GANTRY_TRAVEL: Gross Trolley & Gantry Alignment to Target Vessel Bay *)
        bBusy := TRUE;
        rGantryTravelTimer_s := rGantryTravelTimer_s + c_rTs;
        rTrolleySpeedTarget_mps := 2.000; (* Move trolley toward vessel bay center *)

        IF ABS(rTrolleyPosVoted_m - rTargetTrolleyPos_m) <= 0.150 THEN
            rTrolleySpeedTarget_mps := 0.000;
            rGantryTravelTimer_s := 0.0;
            iNextFSM_State := 4; (* Arrived at bay: Start Spreader Descent *)
        ELSIF rGantryTravelTimer_s > 45.0 THEN
            (* Bay Travel Timeout *)
            iNextFSM_State := 12;
        END_IF;

    4: (* SPREADER_EMPTY_HIGH_SPEED_DESCEND: High-Speed Descent (3.0 m/s) Towards Vessel Cell Guides *)
        bBusy := TRUE;
        rDescendTimer_s := rDescendTimer_s + c_rTs;
        rHoistSpeedTarget_mps := 3.000; (* High-speed lowering of empty spreader *)
        bCmd_SpreaderFlipperDown := FALSE;

        (* Transition to Precision Cell Guide Alignment when Spreader Approaches Guide Top (3.0 m above target) *)
        IF (rTargetHoistPos_m - rHoistRopeLengthVoted_m) <= 3.500 THEN
            rHoistSpeedTarget_mps := 0.800; (* Decelerate vertical speed *)
            rDescendTimer_s := 0.0;
            iNextFSM_State := 5; (* Aligning to cell guide *)
        ELSIF rDescendTimer_s > 30.0 THEN
            iNextFSM_State := 12;
        END_IF;

    5: (* CELL_GUIDE_LIDAR_ALIGNMENT: 2D Lidar Spreader Centering, Corner Flippers Deployed *)
        bBusy := TRUE;
        rLidarAlignmentTimer_s := rLidarAlignmentTimer_s + c_rTs;
        bCmd_SpreaderFlipperDown := TRUE; (* Deploy corner guide flippers *)
        rHoistSpeedTarget_mps := 0.250;   (* Slow creep speed for insertion *)

        (* Cell guide clearance verified by 2oo3 Lidar: Spreader within +/- 25 mm *)
        IF rCellGuideDistVoted_mm <= 35.0 AND ABS(rSwayAngleVoted_deg) <= 0.120 AND ABS(rSkewAngleVoted_deg) <= 0.100 THEN
            bCellGuideAligned := TRUE;
            IF bTwistlockSeated_FL AND bTwistlockSeated_FR AND bTwistlockSeated_RL AND bTwistlockSeated_RR THEN
                bSoftTouchdownConfirmed := TRUE;
                rHoistSpeedTarget_mps := 0.000;
                rLidarAlignmentTimer_s := 0.0;
                iNextFSM_State := 6; (* Spreader Landed: Engage Twistlocks *)
            END_IF;
        ELSE
            bCellGuideAligned := FALSE;
        END_IF;

        IF rLidarAlignmentTimer_s > 20.0 THEN
            iNextFSM_State := 12; (* Cell guide entry jam *)
        END_IF;

    6: (* TWISTLOCK_LOCK_HOIST_CONTAINER: 180 bar Hydraulic Lock & Wire Rope Pre-Tensioning *)
        bBusy := TRUE;
        rTwistlockLockTimer_s := rTwistlockLockTimer_s + c_rTs;
        bCmd_TwistlockLockSolenoid := TRUE;
        bCmd_TwistlockUnlockSolenoid := FALSE;

        (* Verify all 4 corner locks engaged and hydraulic pressure confirmed *)
        IF bTwistlockLocked_FL AND bTwistlockLocked_FR AND bTwistlockLocked_RL AND bTwistlockLocked_RR AND (rTwistlockPressureVoted_bar >= 165.0) THEN
            bTwistlockEngaged := TRUE;
            bTwistlockReleased := FALSE;
            rHoistTensionTimer_s := rHoistTensionTimer_s + c_rTs;
            rHoistSpeedTarget_mps := -0.200; (* Slow hoist to establish rope tension *)

            (* Confirm total load cell reading indicates container lifted off hold (> 18 tonnes) *)
            IF rTotalLoadVoted_tonnes >= 18.00 AND rHoistTensionTimer_s >= 1.00 THEN
                rTwistlockLockTimer_s := 0.0;
                rHoistTensionTimer_s := 0.0;
                iNextFSM_State := 7; (* Initiate Acceleration & Anti-Sway Move *)
            END_IF;
        END_IF;

        IF rTwistlockLockTimer_s > 10.0 THEN
            iNextFSM_State := 12; (* Twistlock lock failure fault *)
        END_IF;

    7: (* ACCELERATION_RAMP_ANTI_SWAY: 1.2 m/s2 Acceleration with Active Pendulum Damping *)
        bBusy := TRUE;
        rAccRampTimer_s := rAccRampTimer_s + c_rTs;
        rHoistSpeedTarget_mps := -1.500; (* Full speed hoisting out of vessel cell guides *)
        rTrolleySpeedTarget_mps := rMaxTrolleySpeed_mps; (* Command 4.0 m/s cruise speed *)

        IF rTrolleySpeedVoted_mps >= (rMaxTrolleySpeed_mps - 0.100) THEN
            rAccRampTimer_s := 0.0;
            iNextFSM_State := 8; (* Reached full speed: Enter cruise *)
        ELSIF rAccRampTimer_s > 8.0 THEN
            iNextFSM_State := 8;
        END_IF;

    8: (* CONSTANT_VELOCITY_CRUISE: 4.0 m/s High-Speed Quay Apron Transit & Zero Sway Tracking *)
        bBusy := TRUE;
        rCruiseTimer_s := rCruiseTimer_s + c_rTs;
        rTrolleySpeedTarget_mps := rMaxTrolleySpeed_mps;
        rHoistSpeedTarget_mps := 0.000; (* Hoist level cruise across quay coaming *)

        (* Trigger deceleration phase based on stopping distance: s_brake = v^2 / (2*a) + anti-sway offset *)
        IF ABS(rTargetTrolleyPos_m - rTrolleyPosVoted_m) <= 12.500 THEN
            rCruiseTimer_s := 0.0;
            iNextFSM_State := 9; (* Initiate Terminal Deceleration & Sway Arrest *)
        ELSIF rCruiseTimer_s > 25.0 THEN
            iNextFSM_State := 9;
        END_IF;

    9: (* DECELERATION_ANTI_SWAY_ARREST: 2-Stage Terminal Damping to Residual Sway < 0.10 deg *)
        bBusy := TRUE;
        rDecelArrestTimer_s := rDecelArrestTimer_s + c_rTs;
        rTrolleySpeedTarget_mps := 0.000; (* Command dead stop *)

        IF ABS(rTrolleySpeedVoted_mps) <= 0.050 AND ABS(rTrolleyPosVoted_m - rTargetTrolleyPos_m) <= 0.080 THEN
            IF rResidualSwayAngle_deg <= 0.100 THEN
                bAntiSwayTargetReached := TRUE;
                rDecelArrestTimer_s := 0.0;
                iNextFSM_State := 10; (* Anti-Sway Criteria Fulfilled: Descend to AGV/Chassis *)
            END_IF;
        END_IF;

        IF rDecelArrestTimer_s > 15.0 THEN
            (* Anti-Sway Convergence Timeout *)
            IF rResidualSwayAngle_deg <= 0.200 THEN
                iNextFSM_State := 10;
            ELSE
                iNextFSM_State := 12;
            END_IF;
        END_IF;

    10: (* QUAY_CHASSIS_SOFT_LANDING: Descent on AGV/Truck Chassis, Load Cell Impact < 2.5 t *)
        bBusy := TRUE;
        rChassisLandingTimer_s := rChassisLandingTimer_s + c_rTs;
        rHoistSpeedTarget_mps := 0.350; (* Creep descent speed *)
        bCmd_SpreaderFlipperDown := FALSE;

        (* Detect weight transfer onto chassis: Load cell drops below tare mass + 2.0 t *)
        IF rTotalLoadVoted_tonnes <= (c_rSpreaderTareMass_kg / 1000.0 + 2.00) AND bChassisPresentOnLane THEN
            bSoftTouchdownConfirmed := TRUE;
            rHoistSpeedTarget_mps := 0.000;
            rChassisLandingTimer_s := 0.0;
            iNextFSM_State := 11; (* Container Landed: Release Twistlocks *)
        END_IF;

        IF rChassisLandingTimer_s > 25.0 THEN
            iNextFSM_State := 12; (* Chassis landing timeout *)
        END_IF;

    11: (* TWISTLOCK_RELEASE_CONFIRM: Hydraulic Unlock to 180 bar & Clear Container *)
        bBusy := TRUE;
        rTwistlockUnlockTimer_s := rTwistlockUnlockTimer_s + c_rTs;
        bCmd_TwistlockLockSolenoid := FALSE;
        bCmd_TwistlockUnlockSolenoid := TRUE;

        (* Verify all 4 corner locks disengaged and cleared *)
        IF bTwistlockUnlocked_FL AND bTwistlockUnlocked_FR AND bTwistlockUnlocked_RL AND bTwistlockUnlocked_RR THEN
            bTwistlockEngaged := FALSE;
            bTwistlockReleased := TRUE;
            rHoistSpeedTarget_mps := -0.800; (* Hoist empty spreader clear of chassis *)

            IF rTwistlockUnlockTimer_s >= 2.50 THEN
                bCycleCompleted := TRUE;
                bBusy := FALSE;
                rTwistlockUnlockTimer_s := 0.0;
                iNextFSM_State := 1; (* Return to Ready / Standby *)
            END_IF;
        END_IF;

        IF rTwistlockUnlockTimer_s > 10.0 THEN
            iNextFSM_State := 12; (* Unlock failure *)
        END_IF;

    12: (* EMERGENCY_ESTOP_STORM_CLAMP: Fast Abort, 50 ms Caliper Brake Drop, Storm Rail Clamping *)
        bReady := FALSE;
        bBusy := FALSE;
        bEmergencyStopTripped := TRUE;
        rEmergencyBrakeTimer_s := rEmergencyBrakeTimer_s + c_rTs;

        (* Zero all drive inverter speed and torque commands immediately *)
        rCmd_TrolleyDriveTorque_Nm := 0.0;
        rCmd_TrolleyDriveSpeed_RPM := 0.0;
        rCmd_HoistWatersideSpeed_RPM := 0.0;
        rCmd_HoistLandsideSpeed_RPM := 0.0;
        rCmd_SkewTrimValve1_pct := 0.0;
        rCmd_SkewTrimValve2_pct := 0.0;

        (* Drop mechanical fail-safe spring-applied caliper disk brakes (< 50 ms latency) *)
        bCmd_HoistCaliperBrakeRelease := FALSE;
        bCmd_TrolleyParkingBrakeRelease := FALSE;
        bOverspeedBrakeDropped := TRUE;

        (* Deploy hydraulic high-wind storm rail clamps *)
        bCmd_StormRailClampRelease := FALSE;
        bStormRailClampDeployed := TRUE;

        (* Manual Reset Permissive *)
        IF bResetFault AND bEmergencyStop_NC AND NOT bAlarm_WindSpeed_HI_HI THEN
            bEmergencyStopTripped := FALSE;
            bOverspeedBrakeDropped := FALSE;
            rEmergencyBrakeTimer_s := 0.0;
            iNextFSM_State := 1; (* Return to offline state *)
        END_IF;

END_CASE;

(* Update State Transition and Output Indicator *)
iFSM_State := iNextFSM_State;
nActiveFSM_State := iFSM_State;""")

    # -------------------------------------------------------------------------------------------------
    # PHASE 5: ISA-18.2 PROCESS ALARMS & DIAGNOSTIC WORD BIT-PACKING
    # -------------------------------------------------------------------------------------------------
    sections.append("""(* ===================================================================================================================
 * PHASE 5: ISA-18.2 PROCESS ALARMS & DIAGNOSTIC WORD BIT-PACKING
 * =================================================================================================================== *)
(* 1. Trolley Absolute Position Limits *)
IF rTrolleyPosVoted_m >= c_rTrolleyPos_Trip_HI_HI THEN
    bAlarm_TrolleyPos_HI_HI := TRUE;
ELSIF rTrolleyPosVoted_m <= (c_rTrolleyPos_Trip_HI_HI - c_rTrolleyPos_Deadband) THEN
    bAlarm_TrolleyPos_HI_HI := FALSE;
END_IF;

IF rTrolleyPosVoted_m >= c_rTrolleyPos_Alarm_HI THEN
    bAlarm_TrolleyPos_HI := TRUE;
ELSIF rTrolleyPosVoted_m <= (c_rTrolleyPos_Alarm_HI - c_rTrolleyPos_Deadband) THEN
    bAlarm_TrolleyPos_HI := FALSE;
END_IF;

IF rTrolleyPosVoted_m <= c_rTrolleyPos_Trip_LO_LO THEN
    bAlarm_TrolleyPos_LO_LO := TRUE;
ELSIF rTrolleyPosVoted_m >= (c_rTrolleyPos_Trip_LO_LO + c_rTrolleyPos_Deadband) THEN
    bAlarm_TrolleyPos_LO_LO := FALSE;
END_IF;

IF rTrolleyPosVoted_m <= c_rTrolleyPos_Alarm_LO THEN
    bAlarm_TrolleyPos_LO := TRUE;
ELSIF rTrolleyPosVoted_m >= (c_rTrolleyPos_Alarm_LO + c_rTrolleyPos_Deadband) THEN
    bAlarm_TrolleyPos_LO := FALSE;
END_IF;

(* 2. Trolley Drive Speed Limits *)
IF ABS(rTrolleySpeedVoted_mps) >= c_rTrolleySpeed_Trip_HI_HI THEN
    bAlarm_TrolleySpeed_HI_HI := TRUE;
ELSIF ABS(rTrolleySpeedVoted_mps) <= (c_rTrolleySpeed_Trip_HI_HI - c_rTrolleySpeed_Deadband) THEN
    bAlarm_TrolleySpeed_HI_HI := FALSE;
END_IF;

IF ABS(rTrolleySpeedVoted_mps) >= c_rTrolleySpeed_Alarm_HI THEN
    bAlarm_TrolleySpeed_HI := TRUE;
ELSIF ABS(rTrolleySpeedVoted_mps) <= (c_rTrolleySpeed_Alarm_HI - c_rTrolleySpeed_Deadband) THEN
    bAlarm_TrolleySpeed_HI := FALSE;
END_IF;

(* 3. Hoist Vertical Payout Speed Limits & Fast Caliper Brake Drop (< 50 ms) *)
IF ABS(rHoistSpeedVoted_mps) >= c_rHoistSpeed_Trip_HI_HI THEN
    bAlarm_HoistSpeed_HI_HI := TRUE;
    bCmd_HoistCaliperBrakeRelease := FALSE; (* Immediate hardware brake drop *)
    bOverspeedBrakeDropped := TRUE;
    iNextFSM_State := 12;
ELSIF ABS(rHoistSpeedVoted_mps) <= (c_rHoistSpeed_Trip_HI_HI - c_rHoistSpeed_Deadband) THEN
    bAlarm_HoistSpeed_HI_HI := FALSE;
END_IF;

IF ABS(rHoistSpeedVoted_mps) >= c_rHoistSpeed_Alarm_HI THEN
    bAlarm_HoistSpeed_HI := TRUE;
ELSIF ABS(rHoistSpeedVoted_mps) <= (c_rHoistSpeed_Alarm_HI - c_rHoistSpeed_Deadband) THEN
    bAlarm_HoistSpeed_HI := FALSE;
END_IF;

(* 4. Spreader Pendulum Sway Angle Limits & Rate-of-Change Alarm *)
IF ABS(rSwayAngleVoted_deg) >= c_rSwayAngle_Trip_HI_HI THEN
    bAlarm_SwayAngle_HI_HI := TRUE;
    iNextFSM_State := 12;
ELSIF ABS(rSwayAngleVoted_deg) <= (c_rSwayAngle_Trip_HI_HI - c_rSwayAngle_Deadband) THEN
    bAlarm_SwayAngle_HI_HI := FALSE;
END_IF;

IF ABS(rSwayAngleVoted_deg) >= c_rSwayAngle_Alarm_HI THEN
    bAlarm_SwayAngle_HI := TRUE;
ELSIF ABS(rSwayAngleVoted_deg) <= (c_rSwayAngle_Alarm_HI - c_rSwayAngle_Deadband) THEN
    bAlarm_SwayAngle_HI := FALSE;
END_IF;

IF rROC_SwayAngle >= c_rSwayAngle_Max_ROC THEN
    bAlarm_SwayAngle_ROC := TRUE;
ELSE
    bAlarm_SwayAngle_ROC := FALSE;
END_IF;

(* 5. Spreader Skew Torsion Angle Limits *)
IF ABS(rSkewAngleVoted_deg) >= c_rSkewAngle_Trip_HI_HI THEN
    bAlarm_SkewAngle_HI_HI := TRUE;
    iNextFSM_State := 12;
ELSIF ABS(rSkewAngleVoted_deg) <= (c_rSkewAngle_Trip_HI_HI - c_rSkewAngle_Deadband) THEN
    bAlarm_SkewAngle_HI_HI := FALSE;
END_IF;

IF ABS(rSkewAngleVoted_deg) >= c_rSkewAngle_Alarm_HI THEN
    bAlarm_SkewAngle_HI := TRUE;
ELSIF ABS(rSkewAngleVoted_deg) <= (c_rSkewAngle_Alarm_HI - c_rSkewAngle_Deadband) THEN
    bAlarm_SkewAngle_HI := FALSE;
END_IF;

(* 6. Ultrasonic Wind Speed & Storm Rail Clamp Interlock *)
IF rWindSpeedVoted_mps >= c_rWindSpeed_Trip_HI_HI AND NOT bHighWindOverrideKey THEN
    bAlarm_WindSpeed_HI_HI := TRUE;
    bStormRailClampDeployed := TRUE;
    bCmd_StormRailClampRelease := FALSE;
    iNextFSM_State := 12; (* Force safe clamping *)
ELSIF rWindSpeedVoted_mps <= (c_rWindSpeed_Trip_HI_HI - c_rWindSpeed_Deadband) THEN
    bAlarm_WindSpeed_HI_HI := FALSE;
END_IF;

IF rWindSpeedVoted_mps >= c_rWindSpeed_Alarm_HI THEN
    bAlarm_WindSpeed_HI := TRUE;
ELSIF rWindSpeedVoted_mps <= (c_rWindSpeed_Alarm_HI - c_rWindSpeed_Deadband) THEN
    bAlarm_WindSpeed_HI := FALSE;
END_IF;

(* 7. Twistlock Hydraulic Manifold Actuation Pressure Limits *)
IF rTwistlockPressureVoted_bar <= c_rTwistlockPress_Trip_LO_LO AND bTwistlockEngaged THEN
    bAlarm_TwistlockPress_LO_LO := TRUE;
    iNextFSM_State := 12;
ELSIF rTwistlockPressureVoted_bar >= (c_rTwistlockPress_Trip_LO_LO + c_rTwistlockPress_Deadband) THEN
    bAlarm_TwistlockPress_LO_LO := FALSE;
END_IF;

IF rTwistlockPressureVoted_bar <= c_rTwistlockPress_Alarm_LO THEN
    bAlarm_TwistlockPress_LO := TRUE;
ELSIF rTwistlockPressureVoted_bar >= (c_rTwistlockPress_Alarm_LO + c_rTwistlockPress_Deadband) THEN
    bAlarm_TwistlockPress_LO := FALSE;
END_IF;

(* 8. Dual-Hoist Drum Leveling Skew Discrepancy Limits *)
IF ABS(rDrumLevelingDiscrepancy_mm) >= c_rDrumLeveling_Trip_HI_HI THEN
    bAlarm_DrumLeveling_HI_HI := TRUE;
    iNextFSM_State := 12;
ELSIF ABS(rDrumLevelingDiscrepancy_mm) <= (c_rDrumLeveling_Trip_HI_HI - c_rDrumLeveling_Deadband) THEN
    bAlarm_DrumLeveling_HI_HI := FALSE;
END_IF;

IF ABS(rDrumLevelingDiscrepancy_mm) >= c_rDrumLeveling_Alarm_HI THEN
    bAlarm_DrumLeveling_HI := TRUE;
ELSIF ABS(rDrumLevelingDiscrepancy_mm) <= (c_rDrumLeveling_Alarm_HI - c_rDrumLeveling_Deadband) THEN
    bAlarm_DrumLeveling_HI := FALSE;
END_IF;

(* 9. Diagnostic Word Bit Packing *)
(* Word 01: FSM State & Motion Sequence Status *)
wDiagnosticWord01 := INT_TO_WORD(iFSM_State);
IF bTwistlockEngaged THEN wDiagnosticWord01 := wDiagnosticWord01 OR 16#0010; END_IF;
IF bTwistlockReleased THEN wDiagnosticWord01 := wDiagnosticWord01 OR 16#0020; END_IF;
IF bTwistlockSeated_FL AND bTwistlockSeated_FR AND bTwistlockSeated_RL AND bTwistlockSeated_RR THEN wDiagnosticWord01 := wDiagnosticWord01 OR 16#0040; END_IF;
IF bCmd_HoistCaliperBrakeRelease THEN wDiagnosticWord01 := wDiagnosticWord01 OR 16#0080; END_IF;
IF bCmd_StormRailClampRelease THEN wDiagnosticWord01 := wDiagnosticWord01 OR 16#0100; END_IF;
IF bAntiSwayTargetReached THEN wDiagnosticWord01 := wDiagnosticWord01 OR 16#0200; END_IF;
IF bCellGuideAligned THEN wDiagnosticWord01 := wDiagnosticWord01 OR 16#0400; END_IF;
IF bSoftTouchdownConfirmed THEN wDiagnosticWord01 := wDiagnosticWord01 OR 16#0800; END_IF;
IF bCycleCompleted THEN wDiagnosticWord01 := wDiagnosticWord01 OR 16#1000; END_IF;
IF bBusy THEN wDiagnosticWord01 := wDiagnosticWord01 OR 16#2000; END_IF;
IF bReady THEN wDiagnosticWord01 := wDiagnosticWord01 OR 16#4000; END_IF;
IF bEnable THEN wDiagnosticWord01 := wDiagnosticWord01 OR 16#8000; END_IF;

(* Word 02: 2oo3 TMR Sensor Health, Discrepancies & Isolation Flags *)
wDiagnosticWord02 := 16#0000;
IF bIso_TrolleyPos_ChA OR bIso_TrolleyPos_ChB OR bIso_TrolleyPos_ChC THEN wDiagnosticWord02 := wDiagnosticWord02 OR 16#0001; END_IF;
IF bIso_TrolleySpeed_ChA OR bIso_TrolleySpeed_ChB OR bIso_TrolleySpeed_ChC THEN wDiagnosticWord02 := wDiagnosticWord02 OR 16#0002; END_IF;
IF bIso_HoistLength_ChA OR bIso_HoistLength_ChB OR bIso_HoistLength_ChC THEN wDiagnosticWord02 := wDiagnosticWord02 OR 16#0004; END_IF;
IF bIso_HoistSpeed_ChA OR bIso_HoistSpeed_ChB OR bIso_HoistSpeed_ChC THEN wDiagnosticWord02 := wDiagnosticWord02 OR 16#0008; END_IF;
IF bIso_SwayAngle_ChA OR bIso_SwayAngle_ChB OR bIso_SwayAngle_ChC THEN wDiagnosticWord02 := wDiagnosticWord02 OR 16#0010; END_IF;
IF bIso_SkewAngle_ChA OR bIso_SkewAngle_ChB OR bIso_SkewAngle_ChC THEN wDiagnosticWord02 := wDiagnosticWord02 OR 16#0020; END_IF;
IF bIso_CellGuide_ChA OR bIso_CellGuide_ChB OR bIso_CellGuide_ChC THEN wDiagnosticWord02 := wDiagnosticWord02 OR 16#0040; END_IF;
IF bIso_LoadCell_ChA OR bIso_LoadCell_ChB OR bIso_LoadCell_ChC THEN wDiagnosticWord02 := wDiagnosticWord02 OR 16#0080; END_IF;
IF bIso_TwistlockPress_ChA OR bIso_TwistlockPress_ChB OR bIso_TwistlockPress_ChC THEN wDiagnosticWord02 := wDiagnosticWord02 OR 16#0100; END_IF;
IF bIso_WindSpeed_ChA OR bIso_WindSpeed_ChB OR bIso_WindSpeed_ChC THEN wDiagnosticWord02 := wDiagnosticWord02 OR 16#0200; END_IF;
IF bIso_RailClampPress_ChA OR bIso_RailClampPress_ChB OR bIso_RailClampPress_ChC THEN wDiagnosticWord02 := wDiagnosticWord02 OR 16#0400; END_IF;
IF bAlarm_TMR_SensorDegraded THEN wDiagnosticWord02 := wDiagnosticWord02 OR 16#8000; END_IF;

(* Word 03: ISA-18.2 Process Warning Alarms (HI / LO Warnings) *)
wDiagnosticWord03 := 16#0000;
IF bAlarm_TrolleyPos_HI THEN wDiagnosticWord03 := wDiagnosticWord03 OR 16#0001; END_IF;
IF bAlarm_TrolleyPos_LO THEN wDiagnosticWord03 := wDiagnosticWord03 OR 16#0002; END_IF;
IF bAlarm_TrolleySpeed_HI THEN wDiagnosticWord03 := wDiagnosticWord03 OR 16#0004; END_IF;
IF bAlarm_HoistSpeed_HI THEN wDiagnosticWord03 := wDiagnosticWord03 OR 16#0008; END_IF;
IF bAlarm_SwayAngle_HI THEN wDiagnosticWord03 := wDiagnosticWord03 OR 16#0010; END_IF;
IF bAlarm_SkewAngle_HI THEN wDiagnosticWord03 := wDiagnosticWord03 OR 16#0020; END_IF;
IF bAlarm_WindSpeed_HI THEN wDiagnosticWord03 := wDiagnosticWord03 OR 16#0040; END_IF;
IF bAlarm_TwistlockPress_LO THEN wDiagnosticWord03 := wDiagnosticWord03 OR 16#0080; END_IF;
IF bAlarm_DrumLeveling_HI THEN wDiagnosticWord03 := wDiagnosticWord03 OR 16#0100; END_IF;
IF bAlarm_EccentricLoad_HI THEN wDiagnosticWord03 := wDiagnosticWord03 OR 16#0200; END_IF;
IF bAlarm_SwayAngle_ROC THEN wDiagnosticWord03 := wDiagnosticWord03 OR 16#0400; END_IF;

(* Word 04: ISA-18.2 Critical Process Trips & Emergency Fast-Aborts *)
wDiagnosticWord04 := 16#0000;
IF bAlarm_TrolleyPos_HI_HI THEN wDiagnosticWord04 := wDiagnosticWord04 OR 16#0001; END_IF;
IF bAlarm_TrolleyPos_LO_LO THEN wDiagnosticWord04 := wDiagnosticWord04 OR 16#0002; END_IF;
IF bAlarm_TrolleySpeed_HI_HI THEN wDiagnosticWord04 := wDiagnosticWord04 OR 16#0004; END_IF;
IF bAlarm_HoistSpeed_HI_HI THEN wDiagnosticWord04 := wDiagnosticWord04 OR 16#0008; END_IF;
IF bAlarm_SwayAngle_HI_HI THEN wDiagnosticWord04 := wDiagnosticWord04 OR 16#0010; END_IF;
IF bAlarm_SkewAngle_HI_HI THEN wDiagnosticWord04 := wDiagnosticWord04 OR 16#0020; END_IF;
IF bAlarm_WindSpeed_HI_HI THEN wDiagnosticWord04 := wDiagnosticWord04 OR 16#0040; END_IF;
IF bAlarm_TwistlockPress_LO_LO THEN wDiagnosticWord04 := wDiagnosticWord04 OR 16#0080; END_IF;
IF bAlarm_DrumLeveling_HI_HI THEN wDiagnosticWord04 := wDiagnosticWord04 OR 16#0100; END_IF;
IF bAlarm_EccentricLoad_HI_HI THEN wDiagnosticWord04 := wDiagnosticWord04 OR 16#0200; END_IF;
IF bOverspeedBrakeDropped THEN wDiagnosticWord04 := wDiagnosticWord04 OR 16#0400; END_IF;
IF bStormRailClampDeployed THEN wDiagnosticWord04 := wDiagnosticWord04 OR 16#0800; END_IF;
IF bEmergencyStopTripped THEN wDiagnosticWord04 := wDiagnosticWord04 OR 16#8000; END_IF;

END_FUNCTION_BLOCK""")

    return "\n\n".join(sections)

if __name__ == "__main__":
    code = generate_full_block()
    print(f"Generated character count: {len(code)}")
    print(f"Generated line count: {len(code.splitlines())}")
