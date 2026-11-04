# build_logistics_asrs_dataset.py
# High-Performance IEC 61131-3 Structured Text Synthesizer for Mega-Scale Distribution Hub ASRS & Cross-Belt Sorter
import json
import os
import sys
import uuid
import re

def get_header():
    return """FUNCTION_BLOCK FB_Logistics_ASRS_HighSpeedShuttle_CrossBeltSorter
(* =====================================================================================================================
 * LUMINA CYBER-PHYSICAL AUTOMATION ENGINE - SYNTHETIC DATASET V7 MAX-PERSONA
 * COMMERCIAL INDUSTRIAL SECTOR : Automated Material Handling & High-Throughput E-Commerce Logistics
 * SYSTEM                       : Mega-Scale Distribution Hub Multi-Tier Automated Storage & Retrieval System (ASRS)
 *                                & High-Speed Cross-Belt Parcel Sorter
 * INTEGRATED SUBSYSTEMS        : - 4-Axis Rail-Guided High-Speed Shuttles (6.0 m/s Travel, 4.0 m/s2 Accel, 25.0 m/s3 Jerk)
 *                                - Common DC-Bus Regenerative Braking & Supercapacitor Buffer Energy Management (750 V DC)
 *                                - Dynamic 7-Segment Jerk-Limited S-Curve Trajectory Generation with Active Slip Compensation
 *                                - Telescopic Fork Multi-Depth Tote Retrieval Axis (0..1400 mm Stroke, Dual-Speed Drive)
 *                                - Linear Induction Motor (LIM) Continuous Cross-Belt Loop (3.0 m/s Velocity, 35,000 pph)
 *                                - 2D Cross-Belt Ejection Trajectory Calculator (Vector Kinematics Matching 45/60/90 deg Chutes)
 *                                - Dynamic Parcel Infeed Gap Optimizer (Active VFD Pacing for Min 250 mm Inter-Parcel Distance)
 *                                - 3D Time-of-Flight / Multi-Sided Barcode Volumetric Collation & Cart Allocation
 *                                - Fire-Compartment High-Speed Roll-Up Guillotine Shutter Dynamic Interlocks (< 20 ms Fast Trip)
 *                                - 8x8 Multivariable Discrete State-Space Cyber-Physical Dynamics (2.0 ms Deterministic Cycle)
 *                                - Receding-Horizon Model Predictive Control (MPC) with Projected Gradient Descent (PGD)
 *                                - 2oo3 Triple Modular Redundancy (TMR) Sensor Voting with Bumpless Degradation Across 14 Tag Groups
 *                                - ISA-18.2 5-Tier Process Alarm Hierarchy (HI_HI, HI, LO, LO_LO, ROC) & Packed Status Bitmasks
 *                                - 12-Stage Deterministic Production Finite State Machine (FSM)
 * =====================================================================================================================
 * CYBER-PHYSICAL LOGISTICS KINEMATICS, THERMODYNAMIC & ENERGY FORMULATIONS:
 * 1. 4-Axis Rail-Guided High-Speed Shuttle Kinematics:
 *    The longitudinal travel axis is driven by high-power synchronous servo motors with steel-on-steel polyurethane-clad wheels.
 *    Operating at velocities up to v_max = 6.0 m/s with accelerations up to a_max = 4.0 m/s2 requires continuous 7-segment
 *    jerk-limited S-curve motion profiling to prevent wheel slippage, structural chassis oscillation, and tote toppling:
 *      Phase 1: Concave acceleration jerk ramp:    a(t) = j_max * t,                  v(t) = 0.5 * j_max * t^2
 *      Phase 2: Constant acceleration cruise:      a(t) = a_max,                      v(t) = v_1 + a_max * (t - t_1)
 *      Phase 3: Convex acceleration jerk ramp:    a(t) = a_max - j_max * (t - t_2),  v(t) = v_2 + a_max * dt - 0.5 * j_max * dt^2
 *      Phase 4: Maximum velocity cruising:         a(t) = 0,                          v(t) = v_max
 *      Phase 5: Concave deceleration jerk ramp:    a(t) = -j_max * (t - t_4),         v(t) = v_max - 0.5 * j_max * dt^2
 *      Phase 6: Constant deceleration cruise:      a(t) = -a_max,                     v(t) = v_5 - a_max * (t - t_5)
 *      Phase 7: Convex deceleration jerk ramp:    a(t) = -a_max + j_max * (t - t_6), v(t) = v_6 - a_max * dt + 0.5 * j_max * dt^2
 *
 * 2. Rail Wheel Slip & Traction Friction Observer:
 *    Wheel slip ratio sigma is monitored by comparing drive wheel encoder velocity omega_w * r_w with absolute laser distance
 *    derivative v_laser:
 *      sigma = (omega_w * r_w - v_laser) / MAX(v_laser, 0.05)
 *    The Burckhardt tire-rail friction model determines the allowable tractive force before micro-slip transitions to macro-slip:
 *      mu(sigma) = c_1 * (1.0 - EXP(-c_2 * sigma)) - c_3 * sigma
 *    If slip exceeds sigma_threshold = 0.04 (4%), traction torque command is clamped via anti-slip modulation.
 *
 * 3. Regenerative DC-Bus Capacitor Energy Balancing:
 *    High-speed shuttles and vertical lifts share a common 750 V DC bus backed by a 120 mF supercapacitor buffer bank.
 *    During decelerations from 6.0 m/s, kinetic energy E_k = 0.5 * M_shuttle * v^2 is regenerated through the servo inverter:
 *      P_regen = eta_inv * M_shuttle * v(t) * |a_decel(t)|
 *    Simultaneously, shuttles accelerating in adjacent rack aisles absorb this energy. Surplus energy raising DC bus voltage
 *    above 820 V DC activates a pulsed dynamic braking chopper resistor bank:
 *      Duty_chop = MIN(1.0, MAX(0.0, (V_bus - 820.0) / (890.0 - 820.0)))
 *
 * 4. Linear Induction Motor (LIM) Continuous Cross-Belt Loop Sorter:
 *    The parcel sorter consists of a continuous chain of 240 articulated carriers propelled at v_sorter = 3.0 m/s by stationary
 *    LIM primary stators interacting with a continuous conductive aluminum/copper reaction plate on the cart underside.
 *    Synchronous speed: v_s = 2.0 * tau_p * f_e, where tau_p = 0.15 m (pole pitch) and f_e is inverter excitation frequency.
 *    Slip speed: v_slip = v_s - v_sorter. Electromagnetic thrust force F_thrust is governed by:
 *      F_thrust = (m * V_phase^2 * (R_r' / s)) / ( (R_s + R_r'/s)^2 + (omega_e * (L_sigma_s + L_sigma_r'))^2 ) * (1.0 / v_s)
 *    Thermal dissipation in the LIM primary windings is tracked via a 2-node thermal model (copper stator & core iron):
 *      C_th_cu * d(T_cu)/dt = I_lim^2 * R_s(T_cu) - (T_cu - T_fe) / R_th_cu_fe
 *      C_th_fe * d(T_fe)/dt = P_iron + (T_cu - T_fe) / R_th_cu_fe - (T_fe - T_amb) / R_th_fe_amb
 *    Air-gap magnetic flux decay due to velocity end-effects is accounted for by dynamic frequency-voltage boost.
 *
 * 5. 2D Cross-Belt Dynamic Ejection Trajectory Kinematics:
 *    When a parcel arrives at its destination chute, the carrier cross-belt motor accelerates perpendicular to sorter motion.
 *    Resultant parcel velocity vector:
 *      v_res_x = v_sorter (constant along loop track)
 *      v_res_y = v_crossbelt(t) (transverse ejection velocity, up to 2.5 m/s)
 *      theta_eject = ATAN2(v_res_y, v_res_x)
 *    The trajectory calculator coordinates cross-belt acceleration to align theta_eject with the chute divert angle (45 or 60 deg),
 *    ensuring the parcel enters the chute throat smoothly without impacting lateral sidewalls or tumbling.
 *
 * 6. Dynamic Infeed Parcel Gap Optimization:
 *    A 3-stage dynamic metering infeed belt line measures incoming parcel dimensions (length L_p, width W_p, weight M_p) via 3D ToF
 *    and optical curtains. The dynamic gap optimizer regulates belt speeds v_belt1, v_belt2, v_belt3 to establish an exact
 *    safety gap d_gap >= 250 mm and phase the parcel to land precisely at the center of an empty carrier cross-belt slot.
 *
 * 7. Receding-Horizon Model Predictive Control (MPC):
 *    Formulates an 8-state, 6-input discrete state-space representation at T_s = 2.0 ms:
 *      x[k+1] = A * x[k] + B * u[k]
 *      y[k]   = C * x[k] + D * u[k]
 *    Iterative Projected Gradient Descent (PGD) minimizes quadratic cost functional J over a receding prediction horizon:
 *      J = sum_{i=1..N} [ (x - x_ref)^T * Q * (x - x_ref) + u^T * R * u + Delta_u^T * S * Delta_u ] + x_N^T * P * x_N
 *    subject to torque, voltage, belt acceleration, and power balance hard saturation limits.
 * =====================================================================================================================
 *)
"""

def get_var_input():
    return """VAR_INPUT
    (* ========================================================================================= *)
    (* 1. MASTER SUPERVISORY PERMISSIVES, SAFETY GATES & OPERATION MODES                         *)
    (* ========================================================================================= *)
    bMasterEnable                       : BOOL := FALSE;    (* Master Facility Automation Enable Permissive Gate [BOOL] *)
    bEmergencyStop_NC                   : BOOL := TRUE;     (* Dual-Channel Hardwired E-Stop Circuit Active Low [BOOL] *)
    bFaultReset                         : BOOL := FALSE;    (* Operator Master Fault Reset & Trip Latch Acknowledge [BOOL] *)
    bAutoSortEnable                     : BOOL := FALSE;    (* Automatic Cross-Belt Sorter Continuous Induction Enable [BOOL] *)
    bAutoShuttleEnable                  : BOOL := FALSE;    (* Automatic Multi-Tier ASRS Rail Shuttle Dispatch Enable [BOOL] *)
    bFireAlarmZoneClear                 : BOOL := TRUE;     (* Fire Protection Smoke/Flame Detectors Zone Permissive [BOOL] *)
    bMaintenanceMode                    : BOOL := FALSE;    (* Manual Maintenance Jog & Diagnostic Bypass Permissive [BOOL] *)
    bRackZone1Permissive                : BOOL := TRUE;     (* ASRS Storage Rack Aisle 1 Safety Light Curtain Clear [BOOL] *)
    bRackZone2Permissive                : BOOL := TRUE;     (* ASRS Storage Rack Aisle 2 Safety Light Curtain Clear [BOOL] *)
    tTaskScanInterval                   : TIME := T#2MS;    (* Real-Time Deterministic Control Task Scan Period [TIME] *)

    (* ========================================================================================= *)
    (* 2. LOGISTICS RECIPE SETPOINTS & KINEMATIC TARGET CONSTRAINTS                              *)
    (* ========================================================================================= *)
    rSet_ShuttleTargetPos_m             : REAL := 48.500;   (* Commanded Shuttle Longitudinal Destination Position [m] *)
    rSet_ShuttleCruiseVel_mps           : REAL := 6.000;    (* Maximum Allowable Shuttle Cruise Travel Velocity [m/s] *)
    rSet_ShuttleMaxAccel_mps2           : REAL := 4.000;    (* Maximum Allowable Longitudinal Acceleration / Decel [m/s2] *)
    rSet_ShuttleMaxJerk_mps3            : REAL := 25.000;   (* Maximum Allowable S-Curve Trajectory Jerk Limit [m/s3] *)
    rSet_ForkTargetStroke_mm            : REAL := 1250.0;   (* Commanded Telescopic Fork Lateral Insertion Stroke [mm] *)
    rSet_CrossBeltNominalVel_mps        : REAL := 3.000;    (* Continuous Linear Induction Cross-Belt Sorter Speed [m/s] *)
    rSet_MinParcelGap_mm                : REAL := 250.0;    (* Dynamic Minimum Allowable Inter-Parcel Safety Margin [mm] *)
    nSet_TargetDischargeChuteID         : INT  := 42;       (* Assigned Parcel Destination Divert Chute Index [1..120] *)
    nSet_TargetRackBayTierID            : INT  := 18;       (* Assigned ASRS Storage Cell Bay Tier Level [1..40] *)
    rSet_ChuteEjectionAngle_deg         : REAL := 45.000;   (* Divert Chute Entrance Take-Off Velocity Vector Angle [deg] *)

    (* ========================================================================================= *)
    (* 3. 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) FIELD INSTRUMENTATION (14 TRANSMITTER TRIPLETS)   *)
    (* ========================================================================================= *)
    (* PE_SHUTTLE_LASER_DIST_101: Triplicated High-Speed Laser Distance Meters for Shuttle Axis [mm] *)
    PE_SHUTTLE_LASER_DIST_101A          : REAL := 0.0;      (* Shuttle Laser Distance Meter Transducer Channel A [mm] *)
    PE_SHUTTLE_LASER_DIST_101B          : REAL := 0.0;      (* Shuttle Laser Distance Meter Transducer Channel B [mm] *)
    PE_SHUTTLE_LASER_DIST_101C          : REAL := 0.0;      (* Shuttle Laser Distance Meter Transducer Channel C [mm] *)

    (* ST_SHUTTLE_DRIVE_VEL_102: Triplicated Optical Wheel Drive Motor Shaft Velocities [m/s] *)
    ST_SHUTTLE_DRIVE_VEL_102A           : REAL := 0.0;      (* Shuttle Traction Drive Wheel Optical Encoder Ch A [m/s] *)
    ST_SHUTTLE_DRIVE_VEL_102B           : REAL := 0.0;      (* Shuttle Traction Drive Wheel Optical Encoder Ch B [m/s] *)
    ST_SHUTTLE_DRIVE_VEL_102C           : REAL := 0.0;      (* Shuttle Traction Drive Wheel Optical Encoder Ch C [m/s] *)

    (* IT_SHUTTLE_SERVO_TORQUE_103: Triplicated Traction Motor Current / Torque Feedback [N*m] *)
    IT_SHUTTLE_SERVO_TORQUE_103A        : REAL := 0.0;      (* Shuttle Synchronous Servo Actual Torque Channel A [N*m] *)
    IT_SHUTTLE_SERVO_TORQUE_103B        : REAL := 0.0;      (* Shuttle Synchronous Servo Actual Torque Channel B [N*m] *)
    IT_SHUTTLE_SERVO_TORQUE_103C        : REAL := 0.0;      (* Shuttle Synchronous Servo Actual Torque Channel C [N*m] *)

    (* ZT_TELESCOPIC_FORK_POS_104: Triplicated Linear Magnetostrictive Stroke Transducers [mm] *)
    ZT_TELESCOPIC_FORK_POS_104A         : REAL := 0.0;      (* Telescopic Fork Stroke Position Sensor Channel A [mm] *)
    ZT_TELESCOPIC_FORK_POS_104B         : REAL := 0.0;      (* Telescopic Fork Stroke Position Sensor Channel B [mm] *)
    ZT_TELESCOPIC_FORK_POS_104C         : REAL := 0.0;      (* Telescopic Fork Stroke Position Sensor Channel C [mm] *)

    (* VT_DC_BUS_REGEN_VOLTAGE_105: Triplicated Common DC Bus Voltage Potential Transducers [V] *)
    VT_DC_BUS_REGEN_VOLTAGE_105A        : REAL := 750.0;    (* Common DC Bus Intermediate Potential Transducer Ch A [V] *)
    VT_DC_BUS_REGEN_VOLTAGE_105B        : REAL := 750.0;    (* Common DC Bus Intermediate Potential Transducer Ch B [V] *)
    VT_DC_BUS_REGEN_VOLTAGE_105C        : REAL := 750.0;    (* Common DC Bus Intermediate Potential Transducer Ch C [V] *)

    (* ST_CROSSBELT_LIM_VEL_201: Triplicated LIM Secondary Linear Reaction Plate Velocity [m/s] *)
    ST_CROSSBELT_LIM_VEL_201A           : REAL := 3.000;    (* Linear Induction Motor Carriage Loop Velocity Ch A [m/s] *)
    ST_CROSSBELT_LIM_VEL_201B           : REAL := 3.000;    (* Linear Induction Motor Carriage Loop Velocity Ch B [m/s] *)
    ST_CROSSBELT_LIM_VEL_201C           : REAL := 3.000;    (* Linear Induction Motor Carriage Loop Velocity Ch C [m/s] *)

    (* PE_CROSSBELT_CART_PULSE_202: Triplicated Carrier Cart Tooth Optical Proximity Transducers [pulses] *)
    PE_CROSSBELT_CART_PULSE_202A        : REAL := 1240.0;   (* Cross-Belt Cart Index Pulse Position Accumulator Ch A *)
    PE_CROSSBELT_CART_PULSE_202B        : REAL := 1240.0;   (* Cross-Belt Cart Index Pulse Position Accumulator Ch B *)
    PE_CROSSBELT_CART_PULSE_202C        : REAL := 1240.0;   (* Cross-Belt Cart Index Pulse Position Accumulator Ch C *)

    (* TT_LIM_STATOR_TEMP_203: Triplicated Pt100 RTD Primary Stator Copper Winding Temperatures [deg C] *)
    TT_LIM_STATOR_TEMP_203A             : REAL := 62.5;     (* LIM Primary Stator Winding Temperature RTD Ch A [deg C] *)
    TT_LIM_STATOR_TEMP_203B             : REAL := 62.5;     (* LIM Primary Stator Winding Temperature RTD Ch B [deg C] *)
    TT_LIM_STATOR_TEMP_203C             : REAL := 62.5;     (* LIM Primary Stator Winding Temperature RTD Ch C [deg C] *)

    (* PE_PARCEL_LEADING_EDGE_301: Triplicated High-Speed Infeed Optical Edge Photogates [BOOL] *)
    PE_PARCEL_LEADING_EDGE_301A         : BOOL := FALSE;    (* Infeed Dynamic Metering Leading Edge Photocell Ch A [BOOL] *)
    PE_PARCEL_LEADING_EDGE_301B         : BOOL := FALSE;    (* Infeed Dynamic Metering Leading Edge Photocell Ch B [BOOL] *)
    PE_PARCEL_LEADING_EDGE_301C         : BOOL := FALSE;    (* Infeed Dynamic Metering Leading Edge Photocell Ch C [BOOL] *)

    (* PE_PARCEL_TRAILING_EDGE_302: Triplicated High-Speed Infeed Optical Trailing Edge Photogates [BOOL] *)
    PE_PARCEL_TRAILING_EDGE_302A        : BOOL := FALSE;    (* Infeed Dynamic Metering Trailing Edge Photocell Ch A [BOOL] *)
    PE_PARCEL_TRAILING_EDGE_302B        : BOOL := FALSE;    (* Infeed Dynamic Metering Trailing Edge Photocell Ch B [BOOL] *)
    PE_PARCEL_TRAILING_EDGE_302C        : BOOL := FALSE;    (* Infeed Dynamic Metering Trailing Edge Photocell Ch C [BOOL] *)

    (* WT_INDUCTION_SCALE_303: Triplicated Dynamic Weigh-In-Motion Precision Strain Gauge Load Cells [kg] *)
    WT_INDUCTION_SCALE_303A             : REAL := 12.450;   (* Infeed Dynamic Weigh-In-Motion Transducer Ch A [kg] *)
    WT_INDUCTION_SCALE_303B             : REAL := 12.450;   (* Infeed Dynamic Weigh-In-Motion Transducer Ch B [kg] *)
    WT_INDUCTION_SCALE_303C             : REAL := 12.450;   (* Infeed Dynamic Weigh-In-Motion Transducer Ch C [kg] *)

    (* ZT_PARCEL_PROFILE_DIM_304: Triplicated 3D Time-of-Flight Dimensional Profiler Length [mm] *)
    ZT_PARCEL_PROFILE_DIM_304A          : REAL := 450.0;    (* 3D ToF Volumetric Parcel Length Dimension Ch A [mm] *)
    ZT_PARCEL_PROFILE_DIM_304B          : REAL := 450.0;    (* 3D ToF Volumetric Parcel Length Dimension Ch B [mm] *)
    ZT_PARCEL_PROFILE_DIM_304C          : REAL := 450.0;    (* 3D ToF Volumetric Parcel Length Dimension Ch C [mm] *)

    (* PE_DISCHARGE_CHUTE_FULL_401: Triplicated Destination Chute Backup Full Optical Sensors [BOOL] *)
    PE_DISCHARGE_CHUTE_FULL_401A        : BOOL := FALSE;    (* Destination Divert Chute Full Backup Sensor Ch A [BOOL] *)
    PE_DISCHARGE_CHUTE_FULL_401B        : BOOL := FALSE;    (* Destination Divert Chute Full Backup Sensor Ch B [BOOL] *)
    PE_DISCHARGE_CHUTE_FULL_401C        : BOOL := FALSE;    (* Destination Divert Chute Full Backup Sensor Ch C [BOOL] *)

    (* ZS_FIRE_ROLLUP_SHUTTER_501: Triplicated Fire Barrier Guillotine Roll-Up Shutter Position [mm] *)
    ZS_FIRE_ROLLUP_SHUTTER_501A         : REAL := 2200.0;   (* Fire-Wall Guillotine Shutter Position Sensor Ch A [mm] *)
    ZS_FIRE_ROLLUP_SHUTTER_501B         : REAL := 2200.0;   (* Fire-Wall Guillotine Shutter Position Sensor Ch B [mm] *)
    ZS_FIRE_ROLLUP_SHUTTER_501C         : REAL := 2200.0;   (* Fire-Wall Guillotine Shutter Position Sensor Ch C [mm] *)

    (* ========================================================================================= *)
    (* 4. AUXILIARY HARDWARE INTERLOCKS & OPTICAL IDENTIFICATION                                 *)
    (* ========================================================================================= *)
    bTotePresentOnFork                  : BOOL := FALSE;    (* Telescopic Fork Platform Tote Seated Photocell [BOOL] *)
    bToteCenteringClamped               : BOOL := FALSE;    (* Telescopic Fork Lateral Clamp Jaw Latched [BOOL] *)
    bElevatorVerticalReady              : BOOL := TRUE;     (* Tier Transfer Vertical Lifter Aligned & Ready [BOOL] *)
    bInfeedCartridgeClear               : BOOL := TRUE;     (* High-Speed Parcel Infeed Conveyor Jam Clear [BOOL] *)
    bBarcodeScannerGoodRead             : BOOL := TRUE;     (* 6-Sided Omnidirectional Barcode Imager Decoded [BOOL] *)
    rMeasuredParcelWidth_mm             : REAL := 320.0;    (* 3D ToF Measured Parcel Width Transverse [mm] *)
    rMeasuredParcelHeight_mm            : REAL := 280.0;    (* 3D ToF Measured Parcel Vertical Height [mm] *)
    rAmbientTemperature_degC           : REAL := 22.5;     (* Hub Logistic Hall Ambient Air Temperature [deg C] *)
    rGridLineVoltageRMS_V               : REAL := 480.0;    (* 3-Phase Main Utility Supply Voltage RMS [V] *)
END_VAR
"""

def get_var_output():
    return """VAR_OUTPUT
    (* ========================================================================================= *)
    (* 1. PRIMARY SYSTEM OPERATION & INTERLOCK STATUS FLAGS                                      *)
    (* ========================================================================================= *)
    bSystemReady                        : BOOL := FALSE;    (* Logistics Hub Master Automation Ready Permissive [BOOL] *)
    bSystemRunning                      : BOOL := FALSE;    (* Logistics ASRS & Cross-Belt System Active Production [BOOL] *)
    bEmergencyTripped                   : BOOL := FALSE;    (* Master Critical Safety Shutdown Latched Trip [BOOL] *)
    bCaliperBrakeClamped                : BOOL := TRUE;     (* High-Speed Rail Disc Caliper Mechanical Brake Clamped [BOOL] *)
    bFireGuillotineZoneBlocked          : BOOL := FALSE;    (* Fire Shutter Descent Path Obstructed by Parcel/Cart [BOOL] *)
    bShuttleTargetReached               : BOOL := FALSE;    (* Shuttle Axis Position Reached within Tolerance (+/- 1.5 mm) [BOOL] *)
    bTotePickCompleted                  : BOOL := FALSE;    (* Telescopic Fork Tote Retrieval / Insertion Handshake Done [BOOL] *)
    bParcelSortedSuccess                : BOOL := FALSE;    (* Cross-Belt Ejection Confirmed into Target Chute [BOOL] *)
    bChuteCongestionAlarm               : BOOL := FALSE;    (* Target Chute Backed Up / Overflow Full Warning [BOOL] *)
    nActiveFSM_State                    : INT  := 0;        (* Active Operational Finite State Machine Step [0..11] *)

    (* ========================================================================================= *)
    (* 2. HIGH-SPEED ACTUATOR COMMANDS & DRIVE SETPOINTS                                         *)
    (* ========================================================================================= *)
    rCmd_ShuttleTractionTorque_Nm       : REAL := 0.0;      (* Shuttle Traction Servo Motor Vector Torque Setpoint [N*m] *)
    rCmd_ShuttleDriveSpeed_RPM          : REAL := 0.0;      (* Shuttle Drive Motor Velocity Closed-Loop Setpoint [RPM] *)
    rCmd_TelescopicForkSpeed_mps        : REAL := 0.0;      (* Telescopic Fork Lateral Linear Velocity Command [m/s] *)
    rCmd_DCBusChopperDuty_pct           : REAL := 0.0;      (* Common DC Bus Dynamic Braking Resistor PWM Duty [0..100%] *)
    rCmd_LIM_InverterFreq_Hz            : REAL := 0.0;      (* Linear Induction Motor Drive Frequency Command [Hz] *)
    rCmd_LIM_VoltageCmd_V               : REAL := 0.0;      (* Linear Induction Motor Stator Voltage Amplitude [V] *)
    rCmd_InfeedBelt1_Speed_mps          : REAL := 0.0;      (* Dynamic Infeed Metering Belt 1 Velocity Command [m/s] *)
    rCmd_InfeedBelt2_Speed_mps          : REAL := 0.0;      (* Dynamic Infeed Acceleration Belt 2 Velocity Command [m/s] *)
    rCmd_InfeedBelt3_Speed_mps          : REAL := 0.0;      (* Dynamic Infeed Injection Belt 3 Velocity Command [m/s] *)
    rCmd_CrossBeltEjectVelocity_mps     : REAL := 0.0;      (* Cross-Belt Carrier Transverse Ejection Velocity [m/s] *)
    bCmd_CrossBeltEjectTrigger          : BOOL := FALSE;    (* Cross-Belt Carrier Ejection Solenoid / Motor Fire Pulse [BOOL] *)
    bCmd_CaliperBrakeRelease            : BOOL := FALSE;    (* High-Speed Rail Disc Caliper Brake Release Solenoid [BOOL] *)
    bCmd_FireShutterPermissive          : BOOL := TRUE;     (* High-Speed Fire Shutter Safe-to-Close Interlock Release [BOOL] *)
    bCmd_ElevatorInterlockRelease       : BOOL := FALSE;    (* Vertical Lifter Elevator Interlock Transfer Permissive [BOOL] *)

    (* ========================================================================================= *)
    (* 3. 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) VOTED TELEMETRY OUTPUTS                           *)
    (* ========================================================================================= *)
    rVoted_ShuttleLaserDist_mm          : REAL := 0.0;      (* 2oo3 Voted Shuttle Absolute Longitudinal Position [mm] *)
    rVoted_ShuttleDriveVel_mps          : REAL := 0.0;      (* 2oo3 Voted Shuttle Traction Drive Wheel Velocity [m/s] *)
    rVoted_ShuttleTorque_Nm             : REAL := 0.0;      (* 2oo3 Voted Shuttle Servo Actual Operating Torque [N*m] *)
    rVoted_TelescopicForkPos_mm         : REAL := 0.0;      (* 2oo3 Voted Telescopic Fork Lateral Extension Stroke [mm] *)
    rVoted_DCBusVoltage_V               : REAL := 750.0;    (* 2oo3 Voted Common DC Bus Potential Voltage [V] *)
    rVoted_CrossBeltLIMVel_mps          : REAL := 3.000;    (* 2oo3 Voted Cross-Belt Sorter Linear Travel Velocity [m/s] *)
    rVoted_CrossBeltCartPulse           : REAL := 1240.0;   (* 2oo3 Voted Sorter Articulated Cart Index Position *)
    rVoted_LIMStatorTemp_degC           : REAL := 62.5;     (* 2oo3 Voted LIM Primary Stator Copper Winding Temp [deg C] *)
    bVoted_ParcelLeadingEdge            : BOOL := FALSE;    (* 2oo3 Voted Infeed Parcel Front Edge Photogate Status [BOOL] *)
    bVoted_ParcelTrailingEdge           : BOOL := FALSE;    (* 2oo3 Voted Infeed Parcel Rear Edge Photogate Status [BOOL] *)
    rVoted_InductionScale_kg            : REAL := 12.450;   (* 2oo3 Voted Dynamic Weigh-In-Motion Parcel Weight [kg] *)
    rVoted_ParcelProfileLength_mm       : REAL := 450.0;    (* 2oo3 Voted 3D ToF Volumetric Parcel Length [mm] *)
    bVoted_DischargeChuteFull           : BOOL := FALSE;    (* 2oo3 Voted Destination Divert Chute Backup Full Flag [BOOL] *)
    rVoted_FireRollupShutterPos_mm      : REAL := 2200.0;   (* 2oo3 Voted Fire Wall Guillotine Shutter Position [mm] *)

    (* ========================================================================================= *)
    (* 4. CYBER-PHYSICAL OBSERVERS, KINEMATIC & PERFORMANCE METRICS                              *)
    (* ========================================================================================= *)
    rCalculated_Throughput_pph          : REAL := 0.0;      (* Instantaneous Parcel Sorting Throughput Rate [parcels/hour] *)
    rCalculated_DynamicGap_mm           : REAL := 250.0;    (* Measured Inter-Parcel Longitudinal Safety Separation [mm] *)
    rCalculated_WheelSlipRatio          : REAL := 0.0;      (* Observed Traction Wheel-to-Rail Longitudinal Slip Ratio [-] *)
    rCalculated_RegenPower_kW           : REAL := 0.0;      (* Instantaneous Deceleration Regenerative Power Flow [kW] *)
    rCalculated_DCBusCapacitorEnergy_kJ : REAL := 33.75;    (* Common Supercapacitor Bank Stored Electrostatic Energy [kJ] *)
    rCalculated_EjectionAngle_deg       : REAL := 45.000;   (* Realized Vector Ejection Trajectory Angle [deg] *)
    rCalculated_LIMThrustForce_N        : REAL := 0.0;      (* Observed Linear Induction Motor Electromagnetic Thrust [N] *)
    rCalculated_LIMAirGapFlux_Wb        : REAL := 0.350;    (* Observed Dynamic Air-Gap Magnetic Mutual Flux [Wb] *)
    rCalculated_LIMCoreTemp_degC        : REAL := 54.2;     (* 2-Node Thermal Observer Iron Stator Core Temp [deg C] *)
    rCalculated_InfeedSyncError_ms      : REAL := 0.0;      (* Temporal Synchronization Error with Cross-Belt Cart Slot [ms] *)
    rMPC_QuadraticCost_J                : REAL := 0.0;      (* Receding-Horizon Optimal Quadratic Cost Objective J [-] *)

    (* ========================================================================================= *)
    (* 5. ISA-18.2 BIT-PACKED DIAGNOSTIC & TELEMETRY STATUS WORDS                                *)
    (* ========================================================================================= *)
    dwStatusWord_Shuttle                : DWORD := 16#0000_0000; (* Bit-Packed Shuttle State, Brake & Rail Safety Flags *)
    dwStatusWord_Sorter                 : DWORD := 16#0000_0000; (* Bit-Packed Sorter Loop, Infeed & Chute Telemetry *)
    dwAlarmWord_Trip                    : DWORD := 16#0000_0000; (* Bit-Packed ISA-18.2 Priority 1 Fast Emergency Trips *)
    dwAlarmWord_Warning                 : DWORD := 16#0000_0000; (* Bit-Packed ISA-18.2 Priority 2 Process Deviations *)
    dwSensorHealthMask                  : DWORD := 16#0000_0000; (* Bit-Packed 2oo3 TMR Channel Discrepancy & Health Bits *)
END_VAR
"""

def get_var_internal():
    return """VAR
    (* ========================================================================================= *)
    (* 1. DISCRETE TASK CYCLE & PHYSICAL / LOGISTICS ENGINEERING CONSTANTS                       *)
    (* ========================================================================================= *)
    c_rTs                               : REAL := 0.002;    (* Deterministic Control Task Scan Period (2.0 ms) [s] *)
    c_rPi                               : REAL := 3.141592653589793; (* Mathematical Constant Pi *)
    c_rGravity                          : REAL := 9.80665;  (* Standard Acceleration of Gravity [m/s2] *)
    c_rShuttleBareMass_kg               : REAL := 185.0;    (* 4-Axis Rail Shuttle Bare Chassis Tare Mass [kg] *)
    c_rToteMaxPayload_kg                : REAL := 50.0;     (* Maximum Allowable Storage Container Tote Mass [kg] *)
    c_rShuttleWheelRadius_m             : REAL := 0.080;    (* Polyurethane-Clad Steel Traction Wheel Radius [m] *)
    c_rShuttleGearboxRatio              : REAL := 5.250;    (* Traction Servo Planetary Gearbox Reduction Ratio [-] *)
    c_rShuttleMotorRatedTorque_Nm       : REAL := 38.5;     (* Traction Servo Motor Nominal Continuous Torque [N*m] *)
    c_rShuttleMotorPeakTorque_Nm        : REAL := 115.0;    (* Traction Servo Motor Peak Transient Torque [N*m] *)
    c_rDCBusCapacitance_F               : REAL := 0.120;    (* Common Supercapacitor Buffer Storage Capacitance [F] *)
    c_rDCBusNominalVoltage_V            : REAL := 750.0;    (* Common Intermediate DC Bus Nominal Operating Voltage [V] *)
    c_rDCBusChopperOnVoltage_V          : REAL := 820.0;    (* Dynamic Braking Chopper Activation Threshold Voltage [V] *)
    c_rDCBusChopperMaxVoltage_V         : REAL := 890.0;    (* Dynamic Braking Chopper 100% Saturation Voltage [V] *)
    c_rBrakingResistorResistance_Ohm    : REAL := 4.500;    (* Dynamic Braking Energy Dump Resistor Bank [Ohm] *)
    c_nSorterTotalCarts                 : INT  := 240;      (* Total Number of Articulated Cross-Belt Carrier Carts *)
    c_rCartPitchLength_m                : REAL := 0.800;    (* Center-to-Center Spacing Pitch per Cross-Belt Cart [m] *)
    c_rSorterLoopLength_m               : REAL := 192.0;    (* Total Continuous Articulated Loop Perimeter [m] *)
    c_rLIMPolePitch_m                   : REAL := 0.150;    (* Linear Induction Motor Primary Stator Pole Pitch tau_p [m] *)
    c_rLIMStatorResistance_Ohm          : REAL := 0.850;    (* LIM Primary Stator Copper Phase Resistance R_s [Ohm] *)
    c_rLIMRotorResistance_Ohm           : REAL := 1.150;    (* LIM Secondary Reaction Plate Referred Resistance R_r' [Ohm] *)
    c_rLIMStatorLeakageInductance_H     : REAL := 0.0042;   (* LIM Primary Stator Leakage Inductance L_sigma_s [H] *)
    c_rLIMRotorLeakageInductance_H      : REAL := 0.0038;   (* LIM Secondary Referred Leakage Inductance L_sigma_r' [H] *)
    c_rLIMMutualInductance_H            : REAL := 0.0480;   (* LIM Air-Gap Mutual Magnetizing Inductance L_m [H] *)
    c_rBurckhardt_C1                    : REAL := 0.650;    (* Burckhardt Wheel-Rail Friction Maximum Coefficient *)
    c_rBurckhardt_C2                    : REAL := 35.000;   (* Burckhardt Wheel-Rail Friction Shape Factor *)
    c_rBurckhardt_C3                    : REAL := 0.180;    (* Burckhardt Wheel-Rail Friction Linear Degradation *)
    c_rLIM_ThermalCap_Cu_J_K            : REAL := 1450.0;   (* LIM Stator Copper Winding Thermal Capacitance [J/K] *)
    c_rLIM_ThermalCap_Fe_J_K            : REAL := 8200.0;   (* LIM Stator Iron Core Lamination Thermal Capacitance [J/K] *)
    c_rLIM_ThermalRes_Cu_Fe_K_W         : REAL := 0.085;    (* Copper Winding to Iron Core Thermal Resistance [K/W] *)
    c_rLIM_ThermalRes_Fe_Amb_K_W        : REAL := 0.145;    (* Iron Core to Forced Cooling Ambient Thermal Resistance [K/W] *)

    (* ========================================================================================= *)
    (* 2. 8x8 MULTIVARIABLE STATE-SPACE DYNAMICS MATRICES (2.0 ms DISCRETE CYCLE)                *)
    (* States x[1..8]:                                                                           *)
    (*   x[1]: Shuttle 1 Position Tracking Error Delta_x_sh1 [m]                                 *)
    (*   x[2]: Shuttle 1 Velocity Tracking Error Delta_v_sh1 [m/s]                               *)
    (*   x[3]: Common DC Bus Voltage Potential Deviation Delta_V_bus [V]                         *)
    (*   x[4]: Cross-Belt Sorter Loop Linear Velocity Error Delta_v_sorter [m/s]                 *)
    (*   x[5]: Dynamic Infeed Inter-Parcel Gap Tracking Error Delta_d_gap [m]                    *)
    (*   x[6]: Telescopic Fork Stroke Position Error Delta_z_fork [m]                            *)
    (*   x[7]: LIM Primary Stator Winding Thermal Rise Delta_T_stator [deg C]                    *)
    (*   x[8]: Net Common DC Bus Regenerative Power Imbalance Delta_P_regen [kW]                 *)
    (* Controls u[1..6]:                                                                         *)
    (*   u[1]: Shuttle Traction Servo Vector Torque Command T_sh_cmd [N*m]                       *)
    (*   u[2]: Dynamic Braking Chopper Resistor Duty Cycle D_chop_cmd [%]                        *)
    (*   u[3]: Linear Induction Motor Inverter Voltage Amplitude V_LIM_cmd [V]                   *)
    (*   u[4]: Dynamic Infeed Metering Belt Acceleration a_infeed_cmd [m/s2]                     *)
    (*   u[5]: Cross-Belt Carrier Transverse Ejection Drive Command u_eject_cmd [%]              *)
    (*   u[6]: Telescopic Fork Lateral Linear Velocity Command v_fork_cmd [m/s]                  *)
    (* ========================================================================================= *)
    bMatricesInitialized                : BOOL := FALSE;
    aA                                  : ARRAY[1..8, 1..8] OF REAL; (* Discrete System Transition Matrix A *)
    aB                                  : ARRAY[1..8, 1..6] OF REAL; (* Discrete Input Coupling Matrix B *)
    aC                                  : ARRAY[1..8, 1..8] OF REAL; (* Discrete Output Measurement Matrix C *)
    aD                                  : ARRAY[1..8, 1..6] OF REAL; (* Discrete Feedthrough Matrix D *)
    ax_state                            : ARRAY[1..8] OF REAL;       (* Current Dynamic State Vector x[k] *)
    ax_next                             : ARRAY[1..8] OF REAL;       (* Projected Next State Vector x[k+1] *)
    ax_ref                              : ARRAY[1..8] OF REAL;       (* Reference Equilibrium State Vector x_ref *)
    au_control                          : ARRAY[1..6] OF REAL;       (* Optimal Actuator Control Vector u[k] *)
    au_prev                             : ARRAY[1..6] OF REAL;       (* Prior Actuator Control Vector u[k-1] *)
    au_delta                            : ARRAY[1..6] OF REAL;       (* Actuator Slew Rate Vector Delta_u[k] *)
    ay_output                           : ARRAY[1..8] OF REAL;       (* Reconstructed Measurement Vector y[k] *)

    (* Model Predictive Control (MPC) Cost Weighting & Actuator Bounds *)
    aQ_Weight                           : ARRAY[1..8] OF REAL;       (* State Tracking Penalty Diagonal Diag(Q) *)
    aR_Weight                           : ARRAY[1..6] OF REAL;       (* Control Effort Penalty Diagonal Diag(R) *)
    aS_Weight                           : ARRAY[1..6] OF REAL;       (* Actuator Slew Rate Penalty Diagonal Diag(S) *)
    aP_TerminalWeight                   : ARRAY[1..8] OF REAL;       (* Terminal Horizon Cost Diagonal Diag(P) *)
    au_min                              : ARRAY[1..6] OF REAL;       (* Hard Lower Actuator Saturation Bounds *)
    au_max                              : ARRAY[1..6] OF REAL;       (* Hard Upper Actuator Saturation Bounds *)
    adelta_u_max                        : ARRAY[1..6] OF REAL;       (* Maximum Allowable Slew Rate per 2 ms Sample *)
    aGrad_u                             : ARRAY[1..6] OF REAL;       (* Analytical Cost Objective Gradient Vector dJ/du *)
    aPredictedState                     : ARRAY[1..8] OF REAL;       (* 1-Step Horizon State Projection Register *)
    c_rPGD_Alpha                        : REAL := 0.00028;           (* Projected Gradient Descent Learning Step Size *)
    rMPC_QuadraticCostAccum             : REAL := 0.0;               (* Accumulated Cost Functional Value J *)

    (* ========================================================================================= *)
    (* 3. 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) DISCREPANCY TIMERS & HEALTH LATOHES               *)
    (* ========================================================================================= *)
    c_rTol_ShuttleLaser_mm              : REAL := 3.000;    (* Laser Distance Discrepancy Tolerance [mm] *)
    c_rTol_ShuttleVel_mps               : REAL := 0.050;    (* Traction Drive Wheel Velocity Tolerance [m/s] *)
    c_rTol_ShuttleTorque_Nm             : REAL := 2.500;    (* Servo Torque Transducer Tolerance [N*m] *)
    c_rTol_TelescopicFork_mm            : REAL := 1.500;    (* Telescopic Fork Stroke Tolerance [mm] *)
    c_rTol_DCBusVoltage_V               : REAL := 8.000;    (* Common DC Bus Potential Tolerance [V] *)
    c_rTol_CrossBeltVel_mps             : REAL := 0.040;    (* Sorter Linear Travel Velocity Tolerance [m/s] *)
    c_rTol_CartPulse                    : REAL := 5.000;    (* Articulated Cart Position Pulse Tolerance *)
    c_rTol_LIMTemp_degC                 : REAL := 2.500;    (* Primary Stator RTD Temperature Tolerance [deg C] *)
    c_rTol_ScaleWeight_kg               : REAL := 0.150;    (* Dynamic Weigh Scale Tolerance [kg] *)
    c_rTol_ParcelLength_mm              : REAL := 10.000;   (* 3D ToF Dimensional Profiler Tolerance [mm] *)
    c_rTol_FireShutter_mm               : REAL := 25.000;   (* Fire Guillotine Shutter Position Tolerance [mm] *)
    c_rTMR_PersistencyTimeout_s         : REAL := 0.030;    (* 2oo3 Discrepancy Debounce Persistence Limit (30 ms) [s] *)

    (* Discrepancy Integration Chronometer Timers *)
    rTimer_ShuttleLaser_Disc_s          : REAL := 0.0;
    rTimer_ShuttleVel_Disc_s            : REAL := 0.0;
    rTimer_ShuttleTorque_Disc_s         : REAL := 0.0;
    rTimer_TelescopicFork_Disc_s        : REAL := 0.0;
    rTimer_DCBusVoltage_Disc_s          : REAL := 0.0;
    rTimer_CrossBeltVel_Disc_s          : REAL := 0.0;
    rTimer_CartPulse_Disc_s             : REAL := 0.0;
    rTimer_LIMTemp_Disc_s               : REAL := 0.0;
    rTimer_InfeedLeading_Disc_s         : REAL := 0.0;
    rTimer_InfeedTrailing_Disc_s        : REAL := 0.0;
    rTimer_ScaleWeight_Disc_s           : REAL := 0.0;
    rTimer_ParcelLength_Disc_s          : REAL := 0.0;
    rTimer_ChuteFull_Disc_s             : REAL := 0.0;
    rTimer_FireShutter_Disc_s           : REAL := 0.0;

    (* Channel Health Isolation Latches (TRUE = Channel Quarantined) *)
    bIso_ShuttleLaser_ChA               : BOOL := FALSE;
    bIso_ShuttleLaser_ChB               : BOOL := FALSE;
    bIso_ShuttleLaser_ChC               : BOOL := FALSE;
    bIso_ShuttleVel_ChA                 : BOOL := FALSE;
    bIso_ShuttleVel_ChB                 : BOOL := FALSE;
    bIso_ShuttleVel_ChC                 : BOOL := FALSE;
    bIso_ShuttleTorque_ChA              : BOOL := FALSE;
    bIso_ShuttleTorque_ChB              : BOOL := FALSE;
    bIso_ShuttleTorque_ChC              : BOOL := FALSE;
    bIso_TelescopicFork_ChA             : BOOL := FALSE;
    bIso_TelescopicFork_ChB             : BOOL := FALSE;
    bIso_TelescopicFork_ChC             : BOOL := FALSE;
    bIso_DCBusVoltage_ChA               : BOOL := FALSE;
    bIso_DCBusVoltage_ChB               : BOOL := FALSE;
    bIso_DCBusVoltage_ChC               : BOOL := FALSE;
    bIso_CrossBeltVel_ChA               : BOOL := FALSE;
    bIso_CrossBeltVel_ChB               : BOOL := FALSE;
    bIso_CrossBeltVel_ChC               : BOOL := FALSE;
    bIso_CartPulse_ChA                  : BOOL := FALSE;
    bIso_CartPulse_ChB                  : BOOL := FALSE;
    bIso_CartPulse_ChC                  : BOOL := FALSE;
    bIso_LIMTemp_ChA                    : BOOL := FALSE;
    bIso_LIMTemp_ChB                    : BOOL := FALSE;
    bIso_LIMTemp_ChC                    : BOOL := FALSE;
    bIso_InfeedLeading_ChA              : BOOL := FALSE;
    bIso_InfeedLeading_ChB              : BOOL := FALSE;
    bIso_InfeedLeading_ChC              : BOOL := FALSE;
    bIso_InfeedTrailing_ChA             : BOOL := FALSE;
    bIso_InfeedTrailing_ChB             : BOOL := FALSE;
    bIso_InfeedTrailing_ChC             : BOOL := FALSE;
    bIso_ScaleWeight_ChA                : BOOL := FALSE;
    bIso_ScaleWeight_ChB                : BOOL := FALSE;
    bIso_ScaleWeight_ChC                : BOOL := FALSE;
    bIso_ParcelLength_ChA               : BOOL := FALSE;
    bIso_ParcelLength_ChB               : BOOL := FALSE;
    bIso_ParcelLength_ChC               : BOOL := FALSE;
    bIso_ChuteFull_ChA                  : BOOL := FALSE;
    bIso_ChuteFull_ChB                  : BOOL := FALSE;
    bIso_ChuteFull_ChC                  : BOOL := FALSE;
    bIso_FireShutter_ChA                : BOOL := FALSE;
    bIso_FireShutter_ChB                : BOOL := FALSE;
    bIso_FireShutter_ChC                : BOOL := FALSE;

    (* ========================================================================================= *)
    (* 4. 7-SEGMENT JERK-LIMITED S-CURVE MOTION PROFILE GENERATOR REGISTERS                      *)
    (* ========================================================================================= *)
    rTraj_TotalDistance_m               : REAL := 0.0;      (* Net Move Distance to Target [m] *)
    rTraj_SignDirection                 : REAL := 1.0;      (* Move Direction Sign (+1.0 forward, -1.0 reverse) *)
    rTraj_T1_JerkAcc_s                  : REAL := 0.160;    (* Segment 1 Duration: Jerk Ramp-Up to Max Accel [s] *)
    rTraj_T2_ConstAcc_s                 : REAL := 0.840;    (* Segment 2 Duration: Constant Acceleration Cruise [s] *)
    rTraj_T3_JerkDec_s                  : REAL := 0.160;    (* Segment 3 Duration: Jerk Ramp-Down to Zero Accel [s] *)
    rTraj_T4_ConstVel_s                 : REAL := 6.500;    (* Segment 4 Duration: Maximum Velocity Cruise [s] *)
    rTraj_T5_JerkDecRamp_s              : REAL := 0.160;    (* Segment 5 Duration: Jerk Ramp-Up to Max Decel [s] *)
    rTraj_T6_ConstDec_s                 : REAL := 0.840;    (* Segment 6 Duration: Constant Deceleration Cruise [s] *)
    rTraj_T7_JerkDecZero_s              : REAL := 0.160;    (* Segment 7 Duration: Jerk Ramp-Down to Zero Decel [s] *)
    rTraj_TimeElapsed_s                 : REAL := 0.0;      (* S-Curve Trajectory Move Chronometer [s] *)
    rTraj_TotalMoveTime_s               : REAL := 8.820;    (* Calculated Aggregate Move Time [s] *)
    rTraj_JerkCmd_mps3                  : REAL := 0.0;      (* Real-Time Trajectory Instantaneous Jerk [m/s3] *)
    rTraj_AccCmd_mps2                   : REAL := 0.0;      (* Real-Time Trajectory Instantaneous Acceleration [m/s2] *)
    rTraj_VelCmd_mps                    : REAL := 0.0;      (* Real-Time Trajectory Instantaneous Velocity [m/s] *)
    rTraj_PosCmd_m                      : REAL := 0.0;      (* Real-Time Trajectory Instantaneous Target Position [m] *)
    bTraj_MoveActive                    : BOOL := FALSE;    (* Trajectory Profile Active Execution Flag *)
    bTraj_MoveCompleted                 : BOOL := FALSE;    (* Trajectory Profile Terminal Destination Reached *)

    (* ========================================================================================= *)
    (* 5. CYBER-PHYSICAL OBSERVER & THERMAL / ENERGY INTERNAL REGISTERS                          *)
    (* ========================================================================================= *)
    rObs_LinearVelocity_mps             : REAL := 0.0;      (* Observed Shuttle True Longitudinal Velocity [m/s] *)
    rObs_WheelVelocity_mps              : REAL := 0.0;      (* Observed Drive Wheel Linear Surface Speed [m/s] *)
    rObs_SlipRatio                      : REAL := 0.0;      (* Observed Traction Longitudinal Wheel Slip Ratio *)
    rObs_AdhesionCoeff                  : REAL := 0.65;     (* Burckhardt Instantaneous Wheel-Rail Friction Coeff *)
    rObs_MaxTractionForce_N             : REAL := 1250.0;   (* Dynamic Non-Skid Traction Force Boundary [N] *)
    rObs_EffectiveMass_kg               : REAL := 235.0;    (* Aggregate Inertial Mass (Shuttle + Container) [kg] *)
    rObs_RegenCurrent_A                 : REAL := 0.0;      (* Inverter Regenerated Braking DC Current [A] *)
    rObs_RegenPower_kW                  : REAL := 0.0;      (* Dynamic Braking Power Generation [kW] *)
    rObs_ChopperCurrent_A               : REAL := 0.0;      (* Chopper Resistor Dissipation Current [A] *)
    rObs_ChopperPower_kW                : REAL := 0.0;      (* Chopper Resistor Dissipation Power [kW] *)
    rObs_LIM_SynchronousSpeed_mps       : REAL := 3.600;    (* LIM Stator Synchronous Linear Wave Velocity [m/s] *)
    rObs_LIM_SlipSpeed_mps              : REAL := 0.600;    (* LIM Relative Slip Velocity (v_s - v_sorter) [m/s] *)
    rObs_LIM_SlipFraction               : REAL := 0.1667;   (* LIM Slip Frequency Ratio s = v_slip / v_s *)
    rObs_LIM_ImpedanceReal              : REAL := 7.750;    (* Equivalent Total Real Stator-Rotor Impedance [Ohm] *)
    rObs_LIM_ImpedanceImag              : REAL := 2.650;    (* Equivalent Total Reactive Leakage Impedance [Ohm] *)
    rObs_LIM_ImpedanceMag               : REAL := 8.190;    (* Total Equivalent Input Impedance Magnitude [Ohm] *)
    rObs_LIM_ThrustForce_N              : REAL := 1850.0;   (* Linear Induction Motor Developed Thrust [N] *)
    rObs_LIM_WindingCopperTemp_degC     : REAL := 62.5;     (* 2-Node Thermal Model Copper Temperature [deg C] *)
    rObs_LIM_CoreIronTemp_degC          : REAL := 54.2;     (* 2-Node Thermal Model Stator Core Iron Temp [deg C] *)
    rObs_LIM_AirGapMutualFlux_Wb        : REAL := 0.350;    (* Effective Dynamic Air-Gap Magnetic Flux [Wb] *)

    (* Dynamic Gap & Cross-Belt Ejection Kinematics Registers *)
    rObs_ParcelFrontEdgeTime_s          : REAL := 0.0;      (* High-Speed Timestamp of Parcel Front Edge Infeed [s] *)
    rObs_ParcelRearEdgeTime_s           : REAL := 0.0;      (* High-Speed Timestamp of Parcel Rear Edge Infeed [s] *)
    rObs_ParcelTransitDuration_s        : REAL := 0.150;    (* Photogate Transit Dwell Period [s] *)
    rObs_MeasuredParcelSpeed_mps        : REAL := 3.000;    (* Dynamically Measured Infeed Belt Speed [m/s] *)
    rObs_DynamicGapSeparation_mm        : REAL := 250.0;    (* Observed Separation to Preceding Parcel [mm] *)
    rObs_TargetCartSlotPulse            : REAL := 0.0;      (* Target Empty Cross-Belt Cart Encoder Pulse Reference *)
    rObs_CartSlotArrivalLeadTime_s      : REAL := 0.0;      (* Projected Seconds to Target Sorter Slot Arrival [s] *)
    rObs_EjectionVelocity_Y_mps         : REAL := 2.121;    (* Required Cross-Belt Carrier Transverse Velocity [m/s] *)
    rObs_EjectionAngle_Rad              : REAL := 0.6155;   (* Resolved Vector Angle (ATAN2(v_y, v_sorter)) [rad] *)
    rObs_EjectionTrajectoryTime_s       : REAL := 0.380;    (* Cross-Belt Ejection Pulse Duration [s] *)
    bObs_EjectionInFlight               : BOOL := FALSE;    (* Parcel Currently Undergoing Cross-Belt Transfer *)

    (* Fire Guillotine Roll-Up Shutter Interlock Registers *)
    bGuillotineEmergencyDropActive      : BOOL := FALSE;    (* Zone Smoke/Fire Hazard Fast Descent Signal *)
    rGuillotineClearanceZone_m          : REAL := 1.200;    (* Safety Distance Margin Upstream/Downstream of Gate [m] *)
    bCartInGuillotineZone               : BOOL := FALSE;    (* Sorter Cart or Parcel Straddling Drop Line *)

    (* ========================================================================================= *)
    (* 6. 12-STAGE DETERMINISTIC OPERATIONAL FINITE STATE MACHINE (FSM) REGISTERS                *)
    (* ========================================================================================= *)
    STATE_STANDBY_HOMING_CALIBRATION    : INT := 0;  (* 0: System Idle, Zero Calibration & Optical Alignment *)
    STATE_DC_BUS_PRECHARGE_AND_SYNC     : INT := 1;  (* 1: DC Bus Soft-Charge to 750 V & Sorter Inverter Sync *)
    STATE_EMPTY_TOTE_BUFFER_ALLOCATION  : INT := 2;  (* 2: MES WMS Tote Retrieval Mission Dispatch & Bay Calc *)
    STATE_SHUTTLE_HIGH_SPEED_RACK_TRAVEL: INT := 3;  (* 3: 6 m/s S-Curve Travel to Assigned Rack Bay *)
    STATE_TELESCOPIC_FORK_EXTEND_AND_PICK:INT := 4;  (* 4: 1250 mm Fork Stroke Extraction & Tote Clamping *)
    STATE_DECELERATION_AND_ELEVATOR_HANDOFF:INT := 5;(* 5: Deceleration to Lifter Bay & Tote Handoff Handshake *)
    STATE_CROSSBELT_LOOP_ACCELERATION_3MPS:INT := 6; (* 6: LIM Continuous Loop Ramp-Up to 3.0 m/s Sort Speed *)
    STATE_DYNAMIC_INFEED_GAP_REGULATION : INT := 7;  (* 7: 3-Stage Dynamic Metering Belts Pacing & Gap Control *)
    STATE_HIGH_SPEED_DISCHARGE_EJECTION : INT := 8;  (* 8: 45-deg Vector Ejection into Assigned Divert Chute *)
    STATE_REGENERATIVE_ENERGY_BALANCING : INT := 9;  (* 9: Dynamic Chopper Resistor Regulation & Peak Shaving *)
    STATE_CONTROLLED_LOOP_PURGE_EMPTY   : INT := 10; (* 10: Graceful Emptying of Active Infeeds & Safe Stoppage *)
    STATE_EMERGENCY_ESTOP_RAIL_CLAMP    : INT := 11; (* 11: 20 ms Fast Caliper Disc Brake Drop & Immediate Halt *)

    iFSM_State                          : INT := 0;         (* Current Operating FSM State Index [0..11] *)
    iNextFSM_State                      : INT := 0;         (* Projected Next Operational State Target *)
    rStateDwellTimer_s                  : REAL := 0.0;      (* Active Operational State Dwell Chronometer [s] *)
    rOperationalTimer_h                 : REAL := 0.0;      (* Aggregate Active Production Life Chronometer [h] *)
    rThroughputCounter                  : DINT := 0;        (* Accumulated Successful Parcel Sort Counter *)
    rThroughputTimer_s                  : REAL := 0.0;      (* Rolling 1-Hour Throughput Calculation Timer [s] *)

    (* Sequence Specific Step Chronometers *)
    rPrechargeTimer_s                   : REAL := 0.0;
    rForkStrokeTimer_s                  : REAL := 0.0;
    rElevatorSyncTimer_s                : REAL := 0.0;
    rLIMRampTimer_s                     : REAL := 0.0;
    rInfeedGapTimer_s                   : REAL := 0.0;
    rEjectionDwellTimer_s               : REAL := 0.0;
    rPurgeCycleTimer_s                  : REAL := 0.0;
    rCaliperBrakeTimer_s                : REAL := 0.0;

    (* ========================================================================================= *)
    (* 7. ISA-18.2 MULTI-TIERED ALARM THRESHOLDS, DEADBANDS & HYSTERESIS                         *)
    (* ========================================================================================= *)
    c_rAlm_ShuttleVel_HH                : REAL := 6.600;    (* [m/s] Overspeed Critical Redline Trip *)
    c_rAlm_ShuttleVel_H                 : REAL := 6.200;    (* [m/s] High Velocity Warning Advisory *)
    c_rAlm_ShuttleVel_Deadband          : REAL := 0.100;    (* [m/s] Velocity Hysteresis Deadband *)

    c_rAlm_DCBusVolt_HH                 : REAL := 910.0;    (* [V] DC Bus Overvoltage Fast Hardware Trip *)
    c_rAlm_DCBusVolt_H                  : REAL := 830.0;    (* [V] DC Bus High Potential Warning *)
    c_rAlm_DCBusVolt_L                  : REAL := 660.0;    (* [V] DC Bus Low Voltage Pre-Warning *)
    c_rAlm_DCBusVolt_LL                 : REAL := 590.0;    (* [V] DC Bus Undervoltage Brownout Trip *)
    c_rAlm_DCBusVolt_Deadband           : REAL := 10.0;     (* [V] Bus Voltage Hysteresis Deadband *)

    c_rAlm_LIMTemp_HH                   : REAL := 135.0;    (* [deg C] Primary Stator Winding Thermal Trip *)
    c_rAlm_LIMTemp_H                    : REAL := 115.0;    (* [deg C] High Stator Winding Temperature Advisory *)
    c_rAlm_LIMTemp_Deadband             : REAL := 4.0;      (* [deg C] Temperature Hysteresis Deadband *)

    c_rAlm_WheelSlip_HH                 : REAL := 0.120;    (* [-] Severe Wheel Spin / Slip Derailment Risk Trip *)
    c_rAlm_WheelSlip_H                  : REAL := 0.050;    (* [-] Micro-Slip Traction Modulation Warning *)
    c_rAlm_WheelSlip_Deadband           : REAL := 0.010;    (* [-] Slip Ratio Hysteresis Deadband *)

    c_rAlm_ParcelGap_LL                 : REAL := 120.0;    (* [mm] Critical Parcel Collision Jam Threat Trip *)
    c_rAlm_ParcelGap_L                  : REAL := 220.0;    (* [mm] Sub-Nominal Parcel Gap Spacing Warning *)
    c_rAlm_ParcelGap_Deadband           : REAL := 15.0;     (* [mm] Gap Separation Hysteresis Deadband *)

    c_rAlm_ForkStroke_HH                : REAL := 1450.0;   (* [mm] Telescopic Fork Mechanical Overtravel Trip *)
    c_rAlm_ForkStroke_Deadband          : REAL := 10.0;     (* [mm] Fork Stroke Hysteresis Deadband *)

    (* ISA-18.2 Discrete Alarm Latches *)
    bAlm_ShuttleVel_HH                  : BOOL := FALSE;
    bAlm_ShuttleVel_H                   : BOOL := FALSE;
    bAlm_DCBusVolt_HH                   : BOOL := FALSE;
    bAlm_DCBusVolt_H                    : BOOL := FALSE;
    bAlm_DCBusVolt_L                    : BOOL := FALSE;
    bAlm_DCBusVolt_LL                   : BOOL := FALSE;
    bAlm_LIMTemp_HH                     : BOOL := FALSE;
    bAlm_LIMTemp_H                      : BOOL := FALSE;
    bAlm_WheelSlip_HH                   : BOOL := FALSE;
    bAlm_WheelSlip_H                    : BOOL := FALSE;
    bAlm_ParcelGap_LL                   : BOOL := FALSE;
    bAlm_ParcelGap_L                    : BOOL := FALSE;
    bAlm_ForkStroke_HH                  : BOOL := FALSE;
    bAlm_TMR_SensorDegraded             : BOOL := FALSE;
    bAlm_FireZoneGuillotine_Trip        : BOOL := FALSE;
    bAlm_ChuteBackupFull_Warning        : BOOL := FALSE;

    (* Auxiliary Iterator, Intermediate Math & Scan Registers *)
    rDeltaTime_s                        : REAL := 0.002;
    rDiffAB, rDiffBC, rDiffCA           : REAL := 0.0;
    bAgreeAB, bAgreeBC, bAgreeCA        : BOOL := FALSE;
    iMatRow, iMatCol, kStateIdx, mInIdx : INT := 1;
    iterMPC                             : INT := 1;
    rTempSum, rTempGrad                 : REAL := 0.0;
    rPrevLaserPos_mm                    : REAL := 0.0;
    rLaserVelocity_Calc_mps             : REAL := 0.0;
    rPrevDCBusVolt                      : REAL := 750.0;
    rDCBusVoltROC_V_s                   : REAL := 0.0;
END_VAR
"""

def get_control_logic_phase0():
    return """(* ===================================================================================================================
 * MASTER SAFETY INTERLOCK & HIGH-SPEED EMERGENCY TRIP EVALUATION
 * =================================================================================================================== *)
(* Scan duration normalization *)
rDeltaTime_s := TIME_TO_REAL(tTaskScanInterval) / 1000.0;
IF rDeltaTime_s < 0.001 OR rDeltaTime_s > 0.010 THEN
    rDeltaTime_s := 0.002;
END_IF;

(* Master Hardware Safety Circuit & E-Stop Interlock Evaluation *)
IF NOT bMasterEnable OR NOT bEmergencyStop_NC THEN
    bEmergencyTripped                   := TRUE;
    bSystemRunning                      := FALSE;
    bSystemReady                        := FALSE;
    bCaliperBrakeClamped                := TRUE;  (* Fast < 20 ms Spring-Applied Caliper Brake Clamp *)
    bCmd_CaliperBrakeRelease            := FALSE;
    rCmd_ShuttleTractionTorque_Nm       := 0.0;
    rCmd_ShuttleDriveSpeed_RPM          := 0.0;
    rCmd_TelescopicForkSpeed_mps        := 0.0;
    rCmd_InfeedBelt1_Speed_mps          := 0.0;
    rCmd_InfeedBelt2_Speed_mps          := 0.0;
    rCmd_InfeedBelt3_Speed_mps          := 0.0;
    rCmd_CrossBeltEjectVelocity_mps     := 0.0;
    bCmd_CrossBeltEjectTrigger          := FALSE;
    rCmd_LIM_VoltageCmd_V               := 0.0;
    rCmd_LIM_InverterFreq_Hz            := 0.0;
    rCmd_DCBusChopperDuty_pct           := 100.0; (* Full Energy Dump to Absorb Residual Inverter Surge *)
    iFSM_State                          := STATE_EMERGENCY_ESTOP_RAIL_CLAMP;
    nActiveFSM_State                    := 11;
    dwStatusWord_Shuttle                := 16#0000_0001; (* Tripped Flag *)
    dwAlarmWord_Trip                    := dwAlarmWord_Trip OR 16#0000_0001;
    RETURN;
END_IF;

(* ===================================================================================================================
 * PHASE 0: DETERMINISTIC INITIALIZATION OF DISCRETE STATE-SPACE (8x8) & MPC MATRICES
 * =================================================================================================================== *)
IF NOT bMatricesInitialized THEN
    (* ---------------------------------------------------------------------------------------------------------------
     * Discrete System Transition Matrix A (8x8) Discretized at Ts = 0.002 s (2.0 ms)
     * States: 1:Delta_x_sh1 [m], 2:Delta_v_sh1 [m/s], 3:Delta_V_bus [V], 4:Delta_v_sorter [m/s],
     *         5:Delta_d_gap [m], 6:Delta_z_fork [m], 7:Delta_T_stator [deg C], 8:Delta_P_regen [kW]
     * --------------------------------------------------------------------------------------------------------------- *)
    (* Row 1: Shuttle Position Kinematics (x[k+1] = x[k] + Ts * v[k]) *)
    aA[1, 1] := 1.00000; aA[1, 2] := 0.00200; aA[1, 3] := 0.00000; aA[1, 4] := 0.00000; aA[1, 5] := 0.00000; aA[1, 6] := 0.00000; aA[1, 7] := 0.00000; aA[1, 8] := 0.00000;
    (* Row 2: Shuttle Velocity Dynamics with Rail Rolling Friction & Polyurethane Viscous Drag *)
    aA[2, 1] := 0.00000; aA[2, 2] := 0.99920; aA[2, 3] := 0.00005; aA[2, 4] := 0.00000; aA[2, 5] := 0.00000; aA[2, 6] := 0.00000; aA[2, 7] := 0.00000; aA[2, 8] := 0.00000;
    (* Row 3: Common DC Bus Intermediate Potential Dynamics (Supercapacitor Storage RC Decay) *)
    aA[3, 1] := 0.00000; aA[3, 2] := 0.00012; aA[3, 3] := 0.99850; aA[3, 4] := -0.00015; aA[3, 5] := 0.00000; aA[3, 6] := 0.00000; aA[3, 7] := 0.00000; aA[3, 8] := 0.00222;
    (* Row 4: Linear Induction Motor Continuous Sorter Loop Linear Velocity Dynamics *)
    aA[4, 1] := 0.00000; aA[4, 2] := 0.00000; aA[4, 3] := 0.00008; aA[4, 4] := 0.99960; aA[4, 5] := 0.00000; aA[4, 6] := 0.00000; aA[4, 7] := -0.00002; aA[4, 8] := 0.00000;
    (* Row 5: Dynamic Infeed Inter-Parcel Gap Separation Tracking Kinematics *)
    aA[5, 1] := 0.00000; aA[5, 2] := 0.00000; aA[5, 3] := 0.00000; aA[5, 4] := -0.00200; aA[5, 5] := 1.00000; aA[5, 6] := 0.00000; aA[5, 7] := 0.00000; aA[5, 8] := 0.00000;
    (* Row 6: Telescopic Fork Lateral Linear Stroke Kinematics *)
    aA[6, 1] := 0.00000; aA[6, 2] := 0.00000; aA[6, 3] := 0.00000; aA[6, 4] := 0.00000; aA[6, 5] := 0.00000; aA[6, 6] := 1.00000; aA[6, 7] := 0.00000; aA[6, 8] := 0.00000;
    (* Row 7: LIM Primary Stator Copper Winding 2-Node Thermal Conduction Dissipation *)
    aA[7, 1] := 0.00000; aA[7, 2] := 0.00000; aA[7, 3] := 0.00000; aA[7, 4] := 0.00004; aA[7, 5] := 0.00000; aA[7, 6] := 0.00000; aA[7, 7] := 0.99984; aA[7, 8] := 0.00000;
    (* Row 8: Net Common DC Bus Regenerative Power Imbalance (Decel Kinetic Inertia Coupling) *)
    aA[8, 1] := 0.00000; aA[8, 2] := -0.04500; aA[8, 3] := 0.00010; aA[8, 4] := 0.00250; aA[8, 5] := 0.00000; aA[8, 6] := 0.00000; aA[8, 7] := 0.00000; aA[8, 8] := 0.98500;

    (* ---------------------------------------------------------------------------------------------------------------
     * Discrete Input Coupling Matrix B (8x6) Discretized at Ts = 0.002 s (2.0 ms)
     * Inputs: 1:T_sh_cmd [N*m], 2:D_chop_cmd [%], 3:V_LIM_cmd [V], 4:a_infeed_cmd [m/s2], 5:u_eject_cmd [%], 6:v_fork_cmd [m/s]
     * --------------------------------------------------------------------------------------------------------------- *)
    (* Row 1: Delta_x_sh1 response to controls *)
    aB[1, 1] := 0.00000056; aB[1, 2] := 0.00000; aB[1, 3] := 0.00000; aB[1, 4] := 0.00000; aB[1, 5] := 0.00000; aB[1, 6] := 0.00000;
    (* Row 2: Delta_v_sh1 response (T_sh * i_gear / (M * r_w) * Ts = 5.25 * 0.002 / (235.0 * 0.080) = 0.0005585 m/(s*N*m)) *)
    aB[2, 1] := 0.00055851; aB[2, 2] := 0.00000; aB[2, 3] := 0.00000; aB[2, 4] := 0.00000; aB[2, 5] := 0.00000; aB[2, 6] := 0.00000;
    (* Row 3: Delta_V_bus response (-V_bus * Ts / (C * R_chop * 100) = -750.0 * 0.002 / (0.120 * 4.5 * 100.0) = -0.02778 V/%) *)
    aB[3, 1] := 0.00035000; aB[3, 2] := -0.0277778; aB[3, 3] := -0.000150; aB[3, 4] := 0.00000; aB[3, 5] := -0.000050; aB[3, 6] := 0.00000;
    (* Row 4: Delta_v_sorter response to LIM inverter voltage amplitude command *)
    aB[4, 1] := 0.00000000; aB[4, 2] := 0.00000; aB[4, 3] := 0.0000425; aB[4, 4] := 0.00000; aB[4, 5] := 0.00000; aB[4, 6] := 0.00000;
    (* Row 5: Delta_d_gap response to dynamic infeed belt acceleration *)
    aB[5, 1] := 0.00000000; aB[5, 2] := 0.00000; aB[5, 3] := 0.0000000; aB[5, 4] := 0.0000020; aB[5, 5] := 0.00000; aB[5, 6] := 0.00000;
    (* Row 6: Delta_z_fork response to lateral linear velocity command (Ts = 0.002 m/(m/s)) *)
    aB[6, 1] := 0.00000000; aB[6, 2] := 0.00000; aB[6, 3] := 0.0000000; aB[6, 4] := 0.00000; aB[6, 5] := 0.00000; aB[6, 6] := 0.0020000;
    (* Row 7: Delta_T_stator thermal rise response to LIM stator voltage amplitude *)
    aB[7, 1] := 0.00000000; aB[7, 2] := 0.00000; aB[7, 3] := 0.0000085; aB[7, 4] := 0.00000; aB[7, 5] := 0.00000; aB[7, 6] := 0.00000;
    (* Row 8: Delta_P_regen power response to shuttle servo torque and chopper duty *)
    aB[8, 1] := -0.0125000; aB[8, 2] := -1.2500000; aB[8, 3] := 0.0050000; aB[8, 4] := 0.00000; aB[8, 5] := 0.00000; aB[8, 6] := 0.00000;

    (* ---------------------------------------------------------------------------------------------------------------
     * Discrete Output Measurement Matrix C (8x8) & Direct Feedthrough Matrix D (8x6)
     * --------------------------------------------------------------------------------------------------------------- *)
    FOR iMatRow := 1 TO 8 DO
        FOR iMatCol := 1 TO 8 DO
            IF iMatRow = iMatCol THEN
                aC[iMatRow, iMatCol] := 1.00000;
            ELSE
                aC[iMatRow, iMatCol] := 0.00000;
            END_IF;
        END_FOR;
        FOR mInIdx := 1 TO 6 DO
            aD[iMatRow, mInIdx] := 0.00000;
        END_FOR;
    END_FOR;

    (* ---------------------------------------------------------------------------------------------------------------
     * Model Predictive Control (MPC) Quadratic Weight Matrices Diag(Q), Diag(R), Diag(S), Diag(P)
     * --------------------------------------------------------------------------------------------------------------- *)
    aQ_Weight[1] := 250.0;   (* x1: Shuttle Position Error Penalty [1/m2] *)
    aQ_Weight[2] := 80.0;    (* x2: Shuttle Velocity Tracking Error Penalty [s2/m2] *)
    aQ_Weight[3] := 0.45;    (* x3: DC Bus Voltage Deviation Penalty [1/V2] *)
    aQ_Weight[4] := 120.0;   (* x4: Sorter Loop Velocity Error Penalty [s2/m2] *)
    aQ_Weight[5] := 15.0;    (* x5: Dynamic Infeed Gap Spacing Error Penalty [1/m2] *)
    aQ_Weight[6] := 180.0;   (* x6: Telescopic Fork Position Error Penalty [1/m2] *)
    aQ_Weight[7] := 0.08;    (* x7: LIM Stator Thermal Rise Penalty [1/K2] *)
    aQ_Weight[8] := 0.12;    (* x8: Regenerative Power Imbalance Penalty [1/kW2] *)

    aR_Weight[1] := 0.015;   (* u1: Shuttle Servo Torque Effort Penalty [1/(N*m)2] *)
    aR_Weight[2] := 0.002;   (* u2: Chopper Duty Dissipation Penalty [1/%2] *)
    aR_Weight[3] := 0.0005;  (* u3: LIM Inverter Voltage Effort Penalty [1/V2] *)
    aR_Weight[4] := 0.080;   (* u4: Dynamic Infeed Belt Acceleration Penalty [s4/m2] *)
    aR_Weight[5] := 0.005;   (* u5: Cross-Belt Transverse Ejection Effort Penalty [1/%2] *)
    aR_Weight[6] := 0.040;   (* u6: Telescopic Fork Linear Velocity Effort Penalty [s2/m2] *)

    aS_Weight[1] := 0.050;   (* Slew Penalty Delta_u1: Shuttle Torque Slew *)
    aS_Weight[2] := 0.010;   (* Slew Penalty Delta_u2: Chopper Duty Slew *)
    aS_Weight[3] := 0.002;   (* Slew Penalty Delta_u3: LIM Voltage Slew *)
    aS_Weight[4] := 0.150;   (* Slew Penalty Delta_u4: Infeed Accel Slew *)
    aS_Weight[5] := 0.020;   (* Slew Penalty Delta_u5: Ejection Slew *)
    aS_Weight[6] := 0.080;   (* Slew Penalty Delta_u6: Fork Velocity Slew *)

    FOR kStateIdx := 1 TO 8 DO
        aP_TerminalWeight[kStateIdx] := aQ_Weight[kStateIdx] * 3.50; (* Terminal Riccati Cost Weighting *)
    END_FOR;

    (* Actuator Hard Saturation Constraints *)
    au_min[1] := -115.0;  au_max[1] := 115.0;   (* u1: Shuttle Torque Limits [-115 .. +115 N*m] *)
    au_min[2] := 0.0;     au_max[2] := 100.0;   (* u2: Chopper Resistor Duty Limits [0 .. 100%] *)
    au_min[3] := 0.0;     au_max[3] := 480.0;   (* u3: LIM Stator Inverter Voltage Limits [0 .. 480 V] *)
    au_min[4] := -5.0;    au_max[4] := 5.0;     (* u4: Infeed Belt Acceleration Limits [-5.0 .. +5.0 m/s2] *)
    au_min[5] := 0.0;     au_max[5] := 100.0;   (* u5: Cross-Belt Ejection Motor Duty [0 .. 100%] *)
    au_min[6] := -1.8;    au_max[6] := 1.8;     (* u6: Telescopic Fork Velocity Limits [-1.8 .. +1.8 m/s] *)

    (* Slew Rate Bounds per 2.0 ms Control Execution Sample *)
    adelta_u_max[1] := 8.5;   (* Max 8.5 N*m change per 2 ms *)
    adelta_u_max[2] := 15.0;  (* Max 15% duty change per 2 ms *)
    adelta_u_max[3] := 12.0;  (* Max 12 V change per 2 ms *)
    adelta_u_max[4] := 0.25;  (* Max 0.25 m/s2 change per 2 ms *)
    adelta_u_max[5] := 20.0;  (* Max 20% change per 2 ms *)
    adelta_u_max[6] := 0.08;  (* Max 0.08 m/s change per 2 ms *)

    bMatricesInitialized := TRUE;
END_IF;
"""

def get_control_logic_phase1():
    return """(* ===================================================================================================================
 * PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING ENGINE ACROSS 14 FIELD TAGS
 * =================================================================================================================== *)
(* Initialize Diagnostic Sensor Health Word *)
dwSensorHealthMask := 16#0000_0000;

(* -------------------------------------------------------------------------------------------------------------------
 * TAG GROUP 1: PE_SHUTTLE_LASER_DIST_101 (Laser Distance Meter [mm])
 * ------------------------------------------------------------------------------------------------------------------- *)
rDiffAB  := ABS(PE_SHUTTLE_LASER_DIST_101A - PE_SHUTTLE_LASER_DIST_101B);
rDiffBC  := ABS(PE_SHUTTLE_LASER_DIST_101B - PE_SHUTTLE_LASER_DIST_101C);
rDiffCA  := ABS(PE_SHUTTLE_LASER_DIST_101C - PE_SHUTTLE_LASER_DIST_101A);
bAgreeAB := (rDiffAB <= c_rTol_ShuttleLaser_mm);
bAgreeBC := (rDiffBC <= c_rTol_ShuttleLaser_mm);
bAgreeCA := (rDiffCA <= c_rTol_ShuttleLaser_mm);

IF bAgreeAB AND bAgreeBC AND bAgreeCA THEN
    rTimer_ShuttleLaser_Disc_s := MAX(0.0, rTimer_ShuttleLaser_Disc_s - (rDeltaTime_s * 2.0));
ELSE
    rTimer_ShuttleLaser_Disc_s := rTimer_ShuttleLaser_Disc_s + rDeltaTime_s;
    IF rTimer_ShuttleLaser_Disc_s >= c_rTMR_PersistencyTimeout_s THEN
        IF bAgreeAB AND NOT bAgreeBC THEN
            bIso_ShuttleLaser_ChC := TRUE;
        ELSIF bAgreeBC AND NOT bAgreeCA THEN
            bIso_ShuttleLaser_ChA := TRUE;
        ELSIF bAgreeCA AND NOT bAgreeAB THEN
            bIso_ShuttleLaser_ChB := TRUE;
        END_IF;
    END_IF;
END_IF;

IF NOT bIso_ShuttleLaser_ChA AND NOT bIso_ShuttleLaser_ChB AND NOT bIso_ShuttleLaser_ChC THEN
    (* 3 Channels Healthy: Median Selection *)
    rVoted_ShuttleLaserDist_mm := MAX(MIN(PE_SHUTTLE_LASER_DIST_101A, PE_SHUTTLE_LASER_DIST_101B),
                                      MIN(MAX(PE_SHUTTLE_LASER_DIST_101A, PE_SHUTTLE_LASER_DIST_101B), PE_SHUTTLE_LASER_DIST_101C));
ELSIF bIso_ShuttleLaser_ChC AND NOT bIso_ShuttleLaser_ChA AND NOT bIso_ShuttleLaser_ChB THEN
    rVoted_ShuttleLaserDist_mm := 0.5 * (PE_SHUTTLE_LASER_DIST_101A + PE_SHUTTLE_LASER_DIST_101B);
    dwSensorHealthMask := dwSensorHealthMask OR 16#0000_0001;
ELSIF bIso_ShuttleLaser_ChB AND NOT bIso_ShuttleLaser_ChA AND NOT bIso_ShuttleLaser_ChC THEN
    rVoted_ShuttleLaserDist_mm := 0.5 * (PE_SHUTTLE_LASER_DIST_101A + PE_SHUTTLE_LASER_DIST_101C);
    dwSensorHealthMask := dwSensorHealthMask OR 16#0000_0002;
ELSIF bIso_ShuttleLaser_ChA AND NOT bIso_ShuttleLaser_ChB AND NOT bIso_ShuttleLaser_ChC THEN
    rVoted_ShuttleLaserDist_mm := 0.5 * (PE_SHUTTLE_LASER_DIST_101B + PE_SHUTTLE_LASER_DIST_101C);
    dwSensorHealthMask := dwSensorHealthMask OR 16#0000_0004;
ELSIF NOT bIso_ShuttleLaser_ChA THEN
    rVoted_ShuttleLaserDist_mm := PE_SHUTTLE_LASER_DIST_101A;
    bAlm_TMR_SensorDegraded := TRUE;
ELSIF NOT bIso_ShuttleLaser_ChB THEN
    rVoted_ShuttleLaserDist_mm := PE_SHUTTLE_LASER_DIST_101B;
    bAlm_TMR_SensorDegraded := TRUE;
ELSIF NOT bIso_ShuttleLaser_ChC THEN
    rVoted_ShuttleLaserDist_mm := PE_SHUTTLE_LASER_DIST_101C;
    bAlm_TMR_SensorDegraded := TRUE;
ELSE
    bEmergencyTripped := TRUE; (* Total Loss of Position Feedback *)
END_IF;

(* -------------------------------------------------------------------------------------------------------------------
 * TAG GROUP 2: ST_SHUTTLE_DRIVE_VEL_102 (Wheel Drive Velocity [m/s])
 * ------------------------------------------------------------------------------------------------------------------- *)
rDiffAB  := ABS(ST_SHUTTLE_DRIVE_VEL_102A - ST_SHUTTLE_DRIVE_VEL_102B);
rDiffBC  := ABS(ST_SHUTTLE_DRIVE_VEL_102B - ST_SHUTTLE_DRIVE_VEL_102C);
rDiffCA  := ABS(ST_SHUTTLE_DRIVE_VEL_102C - ST_SHUTTLE_DRIVE_VEL_102A);
bAgreeAB := (rDiffAB <= c_rTol_ShuttleVel_mps);
bAgreeBC := (rDiffBC <= c_rTol_ShuttleVel_mps);
bAgreeCA := (rDiffCA <= c_rTol_ShuttleVel_mps);

IF bAgreeAB AND bAgreeBC AND bAgreeCA THEN
    rTimer_ShuttleVel_Disc_s := MAX(0.0, rTimer_ShuttleVel_Disc_s - (rDeltaTime_s * 2.0));
ELSE
    rTimer_ShuttleVel_Disc_s := rTimer_ShuttleVel_Disc_s + rDeltaTime_s;
    IF rTimer_ShuttleVel_Disc_s >= c_rTMR_PersistencyTimeout_s THEN
        IF bAgreeAB AND NOT bAgreeBC THEN
            bIso_ShuttleVel_ChC := TRUE;
        ELSIF bAgreeBC AND NOT bAgreeCA THEN
            bIso_ShuttleVel_ChA := TRUE;
        ELSIF bAgreeCA AND NOT bAgreeAB THEN
            bIso_ShuttleVel_ChB := TRUE;
        END_IF;
    END_IF;
END_IF;

IF NOT bIso_ShuttleVel_ChA AND NOT bIso_ShuttleVel_ChB AND NOT bIso_ShuttleVel_ChC THEN
    rVoted_ShuttleDriveVel_mps := MAX(MIN(ST_SHUTTLE_DRIVE_VEL_102A, ST_SHUTTLE_DRIVE_VEL_102B),
                                      MIN(MAX(ST_SHUTTLE_DRIVE_VEL_102A, ST_SHUTTLE_DRIVE_VEL_102B), ST_SHUTTLE_DRIVE_VEL_102C));
ELSIF bIso_ShuttleVel_ChC AND NOT bIso_ShuttleVel_ChA AND NOT bIso_ShuttleVel_ChB THEN
    rVoted_ShuttleDriveVel_mps := 0.5 * (ST_SHUTTLE_DRIVE_VEL_102A + ST_SHUTTLE_DRIVE_VEL_102B);
    dwSensorHealthMask := dwSensorHealthMask OR 16#0000_0010;
ELSIF bIso_ShuttleVel_ChB AND NOT bIso_ShuttleVel_ChA AND NOT bIso_ShuttleVel_ChC THEN
    rVoted_ShuttleDriveVel_mps := 0.5 * (ST_SHUTTLE_DRIVE_VEL_102A + ST_SHUTTLE_DRIVE_VEL_102C);
    dwSensorHealthMask := dwSensorHealthMask OR 16#0000_0020;
ELSIF bIso_ShuttleVel_ChA AND NOT bIso_ShuttleVel_ChB AND NOT bIso_ShuttleVel_ChC THEN
    rVoted_ShuttleDriveVel_mps := 0.5 * (ST_SHUTTLE_DRIVE_VEL_102B + ST_SHUTTLE_DRIVE_VEL_102C);
    dwSensorHealthMask := dwSensorHealthMask OR 16#0000_0040;
ELSE
    rVoted_ShuttleDriveVel_mps := ST_SHUTTLE_DRIVE_VEL_102A;
    bAlm_TMR_SensorDegraded := TRUE;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------
 * TAG GROUP 3: IT_SHUTTLE_SERVO_TORQUE_103 (Traction Servo Actual Torque [N*m])
 * ------------------------------------------------------------------------------------------------------------------- *)
rDiffAB  := ABS(IT_SHUTTLE_SERVO_TORQUE_103A - IT_SHUTTLE_SERVO_TORQUE_103B);
rDiffBC  := ABS(IT_SHUTTLE_SERVO_TORQUE_103B - IT_SHUTTLE_SERVO_TORQUE_103C);
rDiffCA  := ABS(IT_SHUTTLE_SERVO_TORQUE_103C - IT_SHUTTLE_SERVO_TORQUE_103A);
bAgreeAB := (rDiffAB <= c_rTol_ShuttleTorque_Nm);
bAgreeBC := (rDiffBC <= c_rTol_ShuttleTorque_Nm);
bAgreeCA := (rDiffCA <= c_rTol_ShuttleTorque_Nm);

IF bAgreeAB AND bAgreeBC AND bAgreeCA THEN
    rTimer_ShuttleTorque_Disc_s := MAX(0.0, rTimer_ShuttleTorque_Disc_s - (rDeltaTime_s * 2.0));
ELSE
    rTimer_ShuttleTorque_Disc_s := rTimer_ShuttleTorque_Disc_s + rDeltaTime_s;
    IF rTimer_ShuttleTorque_Disc_s >= c_rTMR_PersistencyTimeout_s THEN
        IF bAgreeAB AND NOT bAgreeBC THEN
            bIso_ShuttleTorque_ChC := TRUE;
        ELSIF bAgreeBC AND NOT bAgreeCA THEN
            bIso_ShuttleTorque_ChA := TRUE;
        ELSIF bAgreeCA AND NOT bAgreeAB THEN
            bIso_ShuttleTorque_ChB := TRUE;
        END_IF;
    END_IF;
END_IF;

IF NOT bIso_ShuttleTorque_ChA AND NOT bIso_ShuttleTorque_ChB AND NOT bIso_ShuttleTorque_ChC THEN
    rVoted_ShuttleTorque_Nm := MAX(MIN(IT_SHUTTLE_SERVO_TORQUE_103A, IT_SHUTTLE_SERVO_TORQUE_103B),
                                   MIN(MAX(IT_SHUTTLE_SERVO_TORQUE_103A, IT_SHUTTLE_SERVO_TORQUE_103B), IT_SHUTTLE_SERVO_TORQUE_103C));
ELSIF bIso_ShuttleTorque_ChC THEN
    rVoted_ShuttleTorque_Nm := 0.5 * (IT_SHUTTLE_SERVO_TORQUE_103A + IT_SHUTTLE_SERVO_TORQUE_103B);
    dwSensorHealthMask := dwSensorHealthMask OR 16#0000_0100;
ELSIF bIso_ShuttleTorque_ChB THEN
    rVoted_ShuttleTorque_Nm := 0.5 * (IT_SHUTTLE_SERVO_TORQUE_103A + IT_SHUTTLE_SERVO_TORQUE_103C);
    dwSensorHealthMask := dwSensorHealthMask OR 16#0000_0200;
ELSE
    rVoted_ShuttleTorque_Nm := 0.5 * (IT_SHUTTLE_SERVO_TORQUE_103B + IT_SHUTTLE_SERVO_TORQUE_103C);
    dwSensorHealthMask := dwSensorHealthMask OR 16#0000_0400;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------
 * TAG GROUP 4: ZT_TELESCOPIC_FORK_POS_104 (Telescopic Fork Linear Stroke [mm])
 * ------------------------------------------------------------------------------------------------------------------- *)
rDiffAB  := ABS(ZT_TELESCOPIC_FORK_POS_104A - ZT_TELESCOPIC_FORK_POS_104B);
rDiffBC  := ABS(ZT_TELESCOPIC_FORK_POS_104B - ZT_TELESCOPIC_FORK_POS_104C);
rDiffCA  := ABS(ZT_TELESCOPIC_FORK_POS_104C - ZT_TELESCOPIC_FORK_POS_104A);
bAgreeAB := (rDiffAB <= c_rTol_TelescopicFork_mm);
bAgreeBC := (rDiffBC <= c_rTol_TelescopicFork_mm);
bAgreeCA := (rDiffCA <= c_rTol_TelescopicFork_mm);

IF bAgreeAB AND bAgreeBC AND bAgreeCA THEN
    rTimer_TelescopicFork_Disc_s := MAX(0.0, rTimer_TelescopicFork_Disc_s - (rDeltaTime_s * 2.0));
ELSE
    rTimer_TelescopicFork_Disc_s := rTimer_TelescopicFork_Disc_s + rDeltaTime_s;
    IF rTimer_TelescopicFork_Disc_s >= c_rTMR_PersistencyTimeout_s THEN
        IF bAgreeAB AND NOT bAgreeBC THEN
            bIso_TelescopicFork_ChC := TRUE;
        ELSIF bAgreeBC AND NOT bAgreeCA THEN
            bIso_TelescopicFork_ChA := TRUE;
        ELSIF bAgreeCA AND NOT bAgreeAB THEN
            bIso_TelescopicFork_ChB := TRUE;
        END_IF;
    END_IF;
END_IF;

IF NOT bIso_TelescopicFork_ChA AND NOT bIso_TelescopicFork_ChB AND NOT bIso_TelescopicFork_ChC THEN
    rVoted_TelescopicForkPos_mm := MAX(MIN(ZT_TELESCOPIC_FORK_POS_104A, ZT_TELESCOPIC_FORK_POS_104B),
                                       MIN(MAX(ZT_TELESCOPIC_FORK_POS_104A, ZT_TELESCOPIC_FORK_POS_104B), ZT_TELESCOPIC_FORK_POS_104C));
ELSIF bIso_TelescopicFork_ChC THEN
    rVoted_TelescopicForkPos_mm := 0.5 * (ZT_TELESCOPIC_FORK_POS_104A + ZT_TELESCOPIC_FORK_POS_104B);
    dwSensorHealthMask := dwSensorHealthMask OR 16#0000_1000;
ELSIF bIso_TelescopicFork_ChB THEN
    rVoted_TelescopicForkPos_mm := 0.5 * (ZT_TELESCOPIC_FORK_POS_104A + ZT_TELESCOPIC_FORK_POS_104C);
    dwSensorHealthMask := dwSensorHealthMask OR 16#0000_2000;
ELSE
    rVoted_TelescopicForkPos_mm := 0.5 * (ZT_TELESCOPIC_FORK_POS_104B + ZT_TELESCOPIC_FORK_POS_104C);
    dwSensorHealthMask := dwSensorHealthMask OR 16#0000_4000;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------
 * TAG GROUP 5: VT_DC_BUS_REGEN_VOLTAGE_105 (Common DC Bus Potential [V])
 * ------------------------------------------------------------------------------------------------------------------- *)
rDiffAB  := ABS(VT_DC_BUS_REGEN_VOLTAGE_105A - VT_DC_BUS_REGEN_VOLTAGE_105B);
rDiffBC  := ABS(VT_DC_BUS_REGEN_VOLTAGE_105B - VT_DC_BUS_REGEN_VOLTAGE_105C);
rDiffCA  := ABS(VT_DC_BUS_REGEN_VOLTAGE_105C - VT_DC_BUS_REGEN_VOLTAGE_105A);
bAgreeAB := (rDiffAB <= c_rTol_DCBusVoltage_V);
bAgreeBC := (rDiffBC <= c_rTol_DCBusVoltage_V);
bAgreeCA := (rDiffCA <= c_rTol_DCBusVoltage_V);

IF bAgreeAB AND bAgreeBC AND bAgreeCA THEN
    rTimer_DCBusVoltage_Disc_s := MAX(0.0, rTimer_DCBusVoltage_Disc_s - (rDeltaTime_s * 2.0));
ELSE
    rTimer_DCBusVoltage_Disc_s := rTimer_DCBusVoltage_Disc_s + rDeltaTime_s;
    IF rTimer_DCBusVoltage_Disc_s >= c_rTMR_PersistencyTimeout_s THEN
        IF bAgreeAB AND NOT bAgreeBC THEN
            bIso_DCBusVoltage_ChC := TRUE;
        ELSIF bAgreeBC AND NOT bAgreeCA THEN
            bIso_DCBusVoltage_ChA := TRUE;
        ELSIF bAgreeCA AND NOT bAgreeAB THEN
            bIso_DCBusVoltage_ChB := TRUE;
        END_IF;
    END_IF;
END_IF;

IF NOT bIso_DCBusVoltage_ChA AND NOT bIso_DCBusVoltage_ChB AND NOT bIso_DCBusVoltage_ChC THEN
    rVoted_DCBusVoltage_V := MAX(MIN(VT_DC_BUS_REGEN_VOLTAGE_105A, VT_DC_BUS_REGEN_VOLTAGE_105B),
                                 MIN(MAX(VT_DC_BUS_REGEN_VOLTAGE_105A, VT_DC_BUS_REGEN_VOLTAGE_105B), VT_DC_BUS_REGEN_VOLTAGE_105C));
ELSIF bIso_DCBusVoltage_ChC THEN
    rVoted_DCBusVoltage_V := 0.5 * (VT_DC_BUS_REGEN_VOLTAGE_105A + VT_DC_BUS_REGEN_VOLTAGE_105B);
    dwSensorHealthMask := dwSensorHealthMask OR 16#0001_0000;
ELSIF bIso_DCBusVoltage_ChB THEN
    rVoted_DCBusVoltage_V := 0.5 * (VT_DC_BUS_REGEN_VOLTAGE_105A + VT_DC_BUS_REGEN_VOLTAGE_105C);
    dwSensorHealthMask := dwSensorHealthMask OR 16#0002_0000;
ELSE
    rVoted_DCBusVoltage_V := 0.5 * (VT_DC_BUS_REGEN_VOLTAGE_105B + VT_DC_BUS_REGEN_VOLTAGE_105C);
    dwSensorHealthMask := dwSensorHealthMask OR 16#0004_0000;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------
 * TAG GROUP 6: ST_CROSSBELT_LIM_VEL_201 (LIM Linear Loop Travel Velocity [m/s])
 * ------------------------------------------------------------------------------------------------------------------- *)
rDiffAB  := ABS(ST_CROSSBELT_LIM_VEL_201A - ST_CROSSBELT_LIM_VEL_201B);
rDiffBC  := ABS(ST_CROSSBELT_LIM_VEL_201B - ST_CROSSBELT_LIM_VEL_201C);
rDiffCA  := ABS(ST_CROSSBELT_LIM_VEL_201C - ST_CROSSBELT_LIM_VEL_201A);
bAgreeAB := (rDiffAB <= c_rTol_CrossBeltVel_mps);
bAgreeBC := (rDiffBC <= c_rTol_CrossBeltVel_mps);
bAgreeCA := (rDiffCA <= c_rTol_CrossBeltVel_mps);

IF bAgreeAB AND bAgreeBC AND bAgreeCA THEN
    rTimer_CrossBeltVel_Disc_s := MAX(0.0, rTimer_CrossBeltVel_Disc_s - (rDeltaTime_s * 2.0));
ELSE
    rTimer_CrossBeltVel_Disc_s := rTimer_CrossBeltVel_Disc_s + rDeltaTime_s;
    IF rTimer_CrossBeltVel_Disc_s >= c_rTMR_PersistencyTimeout_s THEN
        IF bAgreeAB AND NOT bAgreeBC THEN
            bIso_CrossBeltVel_ChC := TRUE;
        ELSIF bAgreeBC AND NOT bAgreeCA THEN
            bIso_CrossBeltVel_ChA := TRUE;
        ELSIF bAgreeCA AND NOT bAgreeAB THEN
            bIso_CrossBeltVel_ChB := TRUE;
        END_IF;
    END_IF;
END_IF;

IF NOT bIso_CrossBeltVel_ChA AND NOT bIso_CrossBeltVel_ChB AND NOT bIso_CrossBeltVel_ChC THEN
    rVoted_CrossBeltLIMVel_mps := MAX(MIN(ST_CROSSBELT_LIM_VEL_201A, ST_CROSSBELT_LIM_VEL_201B),
                                      MIN(MAX(ST_CROSSBELT_LIM_VEL_201A, ST_CROSSBELT_LIM_VEL_201B), ST_CROSSBELT_LIM_VEL_201C));
ELSIF bIso_CrossBeltVel_ChC THEN
    rVoted_CrossBeltLIMVel_mps := 0.5 * (ST_CROSSBELT_LIM_VEL_201A + ST_CROSSBELT_LIM_VEL_201B);
    dwSensorHealthMask := dwSensorHealthMask OR 16#0010_0000;
ELSIF bIso_CrossBeltVel_ChB THEN
    rVoted_CrossBeltLIMVel_mps := 0.5 * (ST_CROSSBELT_LIM_VEL_201A + ST_CROSSBELT_LIM_VEL_201C);
    dwSensorHealthMask := dwSensorHealthMask OR 16#0020_0000;
ELSE
    rVoted_CrossBeltLIMVel_mps := 0.5 * (ST_CROSSBELT_LIM_VEL_201B + ST_CROSSBELT_LIM_VEL_201C);
    dwSensorHealthMask := dwSensorHealthMask OR 16#0040_0000;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------
 * TAG GROUP 7: PE_CROSSBELT_CART_PULSE_202 (Cart Tooth Index Optical Pulse)
 * ------------------------------------------------------------------------------------------------------------------- *)
rDiffAB  := ABS(PE_CROSSBELT_CART_PULSE_202A - PE_CROSSBELT_CART_PULSE_202B);
rDiffBC  := ABS(PE_CROSSBELT_CART_PULSE_202B - PE_CROSSBELT_CART_PULSE_202C);
rDiffCA  := ABS(PE_CROSSBELT_CART_PULSE_202C - PE_CROSSBELT_CART_PULSE_202A);
bAgreeAB := (rDiffAB <= c_rTol_CartPulse);
bAgreeBC := (rDiffBC <= c_rTol_CartPulse);
bAgreeCA := (rDiffCA <= c_rTol_CartPulse);

IF bAgreeAB AND bAgreeBC AND bAgreeCA THEN
    rTimer_CartPulse_Disc_s := MAX(0.0, rTimer_CartPulse_Disc_s - (rDeltaTime_s * 2.0));
ELSE
    rTimer_CartPulse_Disc_s := rTimer_CartPulse_Disc_s + rDeltaTime_s;
END_IF;

rVoted_CrossBeltCartPulse := MAX(MIN(PE_CROSSBELT_CART_PULSE_202A, PE_CROSSBELT_CART_PULSE_202B),
                                 MIN(MAX(PE_CROSSBELT_CART_PULSE_202A, PE_CROSSBELT_CART_PULSE_202B), PE_CROSSBELT_CART_PULSE_202C));

(* -------------------------------------------------------------------------------------------------------------------
 * TAG GROUP 8: TT_LIM_STATOR_TEMP_203 (Primary Stator Winding Pt100 RTD [deg C])
 * ------------------------------------------------------------------------------------------------------------------- *)
rDiffAB  := ABS(TT_LIM_STATOR_TEMP_203A - TT_LIM_STATOR_TEMP_203B);
rDiffBC  := ABS(TT_LIM_STATOR_TEMP_203B - TT_LIM_STATOR_TEMP_203C);
rDiffCA  := ABS(TT_LIM_STATOR_TEMP_203C - TT_LIM_STATOR_TEMP_203A);
bAgreeAB := (rDiffAB <= c_rTol_LIMTemp_degC);
bAgreeBC := (rDiffBC <= c_rTol_LIMTemp_degC);
bAgreeCA := (rDiffCA <= c_rTol_LIMTemp_degC);

IF bAgreeAB AND bAgreeBC AND bAgreeCA THEN
    rTimer_LIMTemp_Disc_s := MAX(0.0, rTimer_LIMTemp_Disc_s - (rDeltaTime_s * 2.0));
ELSE
    rTimer_LIMTemp_Disc_s := rTimer_LIMTemp_Disc_s + rDeltaTime_s;
    IF rTimer_LIMTemp_Disc_s >= c_rTMR_PersistencyTimeout_s THEN
        IF bAgreeAB AND NOT bAgreeBC THEN
            bIso_LIMTemp_ChC := TRUE;
        ELSIF bAgreeBC AND NOT bAgreeCA THEN
            bIso_LIMTemp_ChA := TRUE;
        ELSIF bAgreeCA AND NOT bAgreeAB THEN
            bIso_LIMTemp_ChB := TRUE;
        END_IF;
    END_IF;
END_IF;

IF NOT bIso_LIMTemp_ChA AND NOT bIso_LIMTemp_ChB AND NOT bIso_LIMTemp_ChC THEN
    rVoted_LIMStatorTemp_degC := MAX(MIN(TT_LIM_STATOR_TEMP_203A, TT_LIM_STATOR_TEMP_203B),
                                     MIN(MAX(TT_LIM_STATOR_TEMP_203A, TT_LIM_STATOR_TEMP_203B), TT_LIM_STATOR_TEMP_203C));
ELSIF bIso_LIMTemp_ChC THEN
    rVoted_LIMStatorTemp_degC := 0.5 * (TT_LIM_STATOR_TEMP_203A + TT_LIM_STATOR_TEMP_203B);
    dwSensorHealthMask := dwSensorHealthMask OR 16#0100_0000;
ELSIF bIso_LIMTemp_ChB THEN
    rVoted_LIMStatorTemp_degC := 0.5 * (TT_LIM_STATOR_TEMP_203A + TT_LIM_STATOR_TEMP_203C);
    dwSensorHealthMask := dwSensorHealthMask OR 16#0200_0000;
ELSE
    rVoted_LIMStatorTemp_degC := 0.5 * (TT_LIM_STATOR_TEMP_203B + TT_LIM_STATOR_TEMP_203C);
    dwSensorHealthMask := dwSensorHealthMask OR 16#0400_0000;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------
 * TAG GROUP 9 & 10: PE_PARCEL_LEADING_EDGE_301 & PE_PARCEL_TRAILING_EDGE_302 (Photogate Booleans)
 * ------------------------------------------------------------------------------------------------------------------- *)
bVoted_ParcelLeadingEdge  := (PE_PARCEL_LEADING_EDGE_301A AND PE_PARCEL_LEADING_EDGE_301B) OR
                             (PE_PARCEL_LEADING_EDGE_301B AND PE_PARCEL_LEADING_EDGE_301C) OR
                             (PE_PARCEL_LEADING_EDGE_301C AND PE_PARCEL_LEADING_EDGE_301A);

bVoted_ParcelTrailingEdge := (PE_PARCEL_TRAILING_EDGE_302A AND PE_PARCEL_TRAILING_EDGE_302B) OR
                             (PE_PARCEL_TRAILING_EDGE_302B AND PE_PARCEL_TRAILING_EDGE_302C) OR
                             (PE_PARCEL_TRAILING_EDGE_302C AND PE_PARCEL_TRAILING_EDGE_302A);

(* -------------------------------------------------------------------------------------------------------------------
 * TAG GROUP 11: WT_INDUCTION_SCALE_303 (Dynamic Weigh-In-Motion Scale [kg])
 * ------------------------------------------------------------------------------------------------------------------- *)
rDiffAB  := ABS(WT_INDUCTION_SCALE_303A - WT_INDUCTION_SCALE_303B);
rDiffBC  := ABS(WT_INDUCTION_SCALE_303B - WT_INDUCTION_SCALE_303C);
rDiffCA  := ABS(WT_INDUCTION_SCALE_303C - WT_INDUCTION_SCALE_303A);
bAgreeAB := (rDiffAB <= c_rTol_ScaleWeight_kg);
bAgreeBC := (rDiffBC <= c_rTol_ScaleWeight_kg);
bAgreeCA := (rDiffCA <= c_rTol_ScaleWeight_kg);

IF bAgreeAB AND bAgreeBC AND bAgreeCA THEN
    rTimer_ScaleWeight_Disc_s := MAX(0.0, rTimer_ScaleWeight_Disc_s - (rDeltaTime_s * 2.0));
ELSE
    rTimer_ScaleWeight_Disc_s := rTimer_ScaleWeight_Disc_s + rDeltaTime_s;
    IF rTimer_ScaleWeight_Disc_s >= c_rTMR_PersistencyTimeout_s THEN
        IF bAgreeAB AND NOT bAgreeBC THEN
            bIso_ScaleWeight_ChC := TRUE;
        ELSIF bAgreeBC AND NOT bAgreeCA THEN
            bIso_ScaleWeight_ChA := TRUE;
        ELSIF bAgreeCA AND NOT bAgreeAB THEN
            bIso_ScaleWeight_ChB := TRUE;
        END_IF;
    END_IF;
END_IF;

IF NOT bIso_ScaleWeight_ChA AND NOT bIso_ScaleWeight_ChB AND NOT bIso_ScaleWeight_ChC THEN
    rVoted_InductionScale_kg := MAX(MIN(WT_INDUCTION_SCALE_303A, WT_INDUCTION_SCALE_303B),
                                    MIN(MAX(WT_INDUCTION_SCALE_303A, WT_INDUCTION_SCALE_303B), WT_INDUCTION_SCALE_303C));
ELSIF bIso_ScaleWeight_ChC THEN
    rVoted_InductionScale_kg := 0.5 * (WT_INDUCTION_SCALE_303A + WT_INDUCTION_SCALE_303B);
    dwSensorHealthMask := dwSensorHealthMask OR 16#1000_0000;
ELSIF bIso_ScaleWeight_ChB THEN
    rVoted_InductionScale_kg := 0.5 * (WT_INDUCTION_SCALE_303A + WT_INDUCTION_SCALE_303C);
    dwSensorHealthMask := dwSensorHealthMask OR 16#2000_0000;
ELSE
    rVoted_InductionScale_kg := 0.5 * (WT_INDUCTION_SCALE_303B + WT_INDUCTION_SCALE_303C);
    dwSensorHealthMask := dwSensorHealthMask OR 16#4000_0000;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------
 * TAG GROUP 12: ZT_PARCEL_PROFILE_DIM_304 (3D ToF Dimensional Profiler Length [mm])
 * ------------------------------------------------------------------------------------------------------------------- *)
rDiffAB  := ABS(ZT_PARCEL_PROFILE_DIM_304A - ZT_PARCEL_PROFILE_DIM_304B);
rDiffBC  := ABS(ZT_PARCEL_PROFILE_DIM_304B - ZT_PARCEL_PROFILE_DIM_304C);
rDiffCA  := ABS(ZT_PARCEL_PROFILE_DIM_304C - ZT_PARCEL_PROFILE_DIM_304A);
bAgreeAB := (rDiffAB <= c_rTol_ParcelLength_mm);
bAgreeBC := (rDiffBC <= c_rTol_ParcelLength_mm);
bAgreeCA := (rDiffCA <= c_rTol_ParcelLength_mm);

rVoted_ParcelProfileLength_mm := MAX(MIN(ZT_PARCEL_PROFILE_DIM_304A, ZT_PARCEL_PROFILE_DIM_304B),
                                     MIN(MAX(ZT_PARCEL_PROFILE_DIM_304A, ZT_PARCEL_PROFILE_DIM_304B), ZT_PARCEL_PROFILE_DIM_304C));

(* -------------------------------------------------------------------------------------------------------------------
 * TAG GROUP 13: PE_DISCHARGE_CHUTE_FULL_401 (Destination Divert Chute Backup Full [BOOL])
 * ------------------------------------------------------------------------------------------------------------------- *)
bVoted_DischargeChuteFull := (PE_DISCHARGE_CHUTE_FULL_401A AND PE_DISCHARGE_CHUTE_FULL_401B) OR
                             (PE_DISCHARGE_CHUTE_FULL_401B AND PE_DISCHARGE_CHUTE_FULL_401C) OR
                             (PE_DISCHARGE_CHUTE_FULL_401C AND PE_DISCHARGE_CHUTE_FULL_401A);

(* -------------------------------------------------------------------------------------------------------------------
 * TAG GROUP 14: ZS_FIRE_ROLLUP_SHUTTER_501 (Fire Barrier Guillotine Shutter Position [mm])
 * ------------------------------------------------------------------------------------------------------------------- *)
rDiffAB  := ABS(ZS_FIRE_ROLLUP_SHUTTER_501A - ZS_FIRE_ROLLUP_SHUTTER_501B);
rDiffBC  := ABS(ZS_FIRE_ROLLUP_SHUTTER_501B - ZS_FIRE_ROLLUP_SHUTTER_501C);
rDiffCA  := ABS(ZS_FIRE_ROLLUP_SHUTTER_501C - ZS_FIRE_ROLLUP_SHUTTER_501A);
bAgreeAB := (rDiffAB <= c_rTol_FireShutter_mm);
bAgreeBC := (rDiffBC <= c_rTol_FireShutter_mm);
bAgreeCA := (rDiffCA <= c_rTol_FireShutter_mm);

rVoted_FireRollupShutterPos_mm := MAX(MIN(ZS_FIRE_ROLLUP_SHUTTER_501A, ZS_FIRE_ROLLUP_SHUTTER_501B),
                                      MIN(MAX(ZS_FIRE_ROLLUP_SHUTTER_501A, ZS_FIRE_ROLLUP_SHUTTER_501B), ZS_FIRE_ROLLUP_SHUTTER_501C));
"""

def get_control_logic_phase2():
    return """(* ===================================================================================================================
 * PHASE 2: CYBER-PHYSICAL OBSERVERS, S-CURVE KINEMATICS, THERMAL & REGENERATIVE CALCULATIONS
 * =================================================================================================================== *)

(* -------------------------------------------------------------------------------------------------------------------
 * 1. 7-SEGMENT JERK-LIMITED S-CURVE MOTION PROFILE GENERATOR
 * ------------------------------------------------------------------------------------------------------------------- *)
rTraj_TotalDistance_m := rSet_ShuttleTargetPos_m - (rVoted_ShuttleLaserDist_mm / 1000.0);

IF ABS(rTraj_TotalDistance_m) > 0.005 THEN
    IF NOT bTraj_MoveActive THEN
        (* Trajectory Profile Initialization *)
        bTraj_MoveActive        := TRUE;
        bTraj_MoveCompleted     := FALSE;
        rTraj_TimeElapsed_s     := 0.0;
        
        IF rTraj_TotalDistance_m >= 0.0 THEN
            rTraj_SignDirection := 1.0;
        ELSE
            rTraj_SignDirection := -1.0;
        END_IF;

        (* Segment Time Durations *)
        (* T1: Jerk ramp-up to max acceleration (a_max / j_max = 4.0 / 25.0 = 0.160 s) *)
        rTraj_T1_JerkAcc_s     := rSet_ShuttleMaxAccel_mps2 / rSet_ShuttleMaxJerk_mps3;
        rTraj_T3_JerkDec_s     := rTraj_T1_JerkAcc_s;
        rTraj_T5_JerkDecRamp_s := rTraj_T1_JerkAcc_s;
        rTraj_T7_JerkDecZero_s := rTraj_T1_JerkAcc_s;

        (* Velocity acquired during quadratic jerk ramps *)
        rTempSum := rSet_ShuttleMaxJerk_mps3 * rTraj_T1_JerkAcc_s * rTraj_T1_JerkAcc_s; (* v_ramp = j * t^2 *)
        
        (* T2: Constant acceleration duration *)
        IF rSet_ShuttleCruiseVel_mps > rTempSum THEN
            rTraj_T2_ConstAcc_s := (rSet_ShuttleCruiseVel_mps - rTempSum) / rSet_ShuttleMaxAccel_mps2;
        ELSE
            rTraj_T2_ConstAcc_s := 0.0;
        END_IF;
        rTraj_T6_ConstDec_s := rTraj_T2_ConstAcc_s;

        (* Distance consumed during acceleration and deceleration phases *)
        rTempGrad := (2.0 * rTraj_T1_JerkAcc_s + rTraj_T2_ConstAcc_s) * rSet_ShuttleCruiseVel_mps;

        (* T4: Constant velocity cruising duration *)
        IF ABS(rTraj_TotalDistance_m) > rTempGrad THEN
            rTraj_T4_ConstVel_s := (ABS(rTraj_TotalDistance_m) - rTempGrad) / rSet_ShuttleCruiseVel_mps;
        ELSE
            rTraj_T4_ConstVel_s := 0.0;
        END_IF;

        rTraj_TotalMoveTime_s := (4.0 * rTraj_T1_JerkAcc_s) + (2.0 * rTraj_T2_ConstAcc_s) + rTraj_T4_ConstVel_s;
    END_IF;

    (* Advance Trajectory Chronometer *)
    rTraj_TimeElapsed_s := rTraj_TimeElapsed_s + rDeltaTime_s;

    (* Evaluate 7-Segment Piecewise Jerk, Acceleration, Velocity, and Position *)
    IF rTraj_TimeElapsed_s <= rTraj_T1_JerkAcc_s THEN
        (* Phase 1: Concave Jerk Ramp-Up *)
        rTraj_JerkCmd_mps3 := rTraj_SignDirection * rSet_ShuttleMaxJerk_mps3;
        rTraj_AccCmd_mps2  := rTraj_JerkCmd_mps3 * rTraj_TimeElapsed_s;
        rTraj_VelCmd_mps   := 0.5 * rTraj_JerkCmd_mps3 * rTraj_TimeElapsed_s * rTraj_TimeElapsed_s;
        rTraj_PosCmd_m     := (rVoted_ShuttleLaserDist_mm / 1000.0) + (1.0 / 6.0) * rTraj_JerkCmd_mps3 * rTraj_TimeElapsed_s * rTraj_TimeElapsed_s * rTraj_TimeElapsed_s;

    ELSIF rTraj_TimeElapsed_s <= (rTraj_T1_JerkAcc_s + rTraj_T2_ConstAcc_s) THEN
        (* Phase 2: Constant Linear Acceleration Cruise *)
        rTempSum           := rTraj_TimeElapsed_s - rTraj_T1_JerkAcc_s;
        rTraj_JerkCmd_mps3 := 0.0;
        rTraj_AccCmd_mps2  := rTraj_SignDirection * rSet_ShuttleMaxAccel_mps2;
        rTraj_VelCmd_mps   := rTraj_SignDirection * (0.5 * rSet_ShuttleMaxJerk_mps3 * rTraj_T1_JerkAcc_s * rTraj_T1_JerkAcc_s + rSet_ShuttleMaxAccel_mps2 * rTempSum);
        rTraj_PosCmd_m     := (rVoted_ShuttleLaserDist_mm / 1000.0) + rTraj_VelCmd_mps * rTempSum;

    ELSIF rTraj_TimeElapsed_s <= (2.0 * rTraj_T1_JerkAcc_s + rTraj_T2_ConstAcc_s) THEN
        (* Phase 3: Convex Jerk Ramp-Down to Zero Acceleration *)
        rTempSum           := rTraj_TimeElapsed_s - (rTraj_T1_JerkAcc_s + rTraj_T2_ConstAcc_s);
        rTraj_JerkCmd_mps3 := -rTraj_SignDirection * rSet_ShuttleMaxJerk_mps3;
        rTraj_AccCmd_mps2  := rTraj_SignDirection * (rSet_ShuttleMaxAccel_mps2 - rSet_ShuttleMaxJerk_mps3 * rTempSum);
        rTraj_VelCmd_mps   := rTraj_SignDirection * rSet_ShuttleCruiseVel_mps - (0.5 * rSet_ShuttleMaxJerk_mps3 * (rTraj_T1_JerkAcc_s - rTempSum) * (rTraj_T1_JerkAcc_s - rTempSum));
        rTraj_PosCmd_m     := (rVoted_ShuttleLaserDist_mm / 1000.0) + rTraj_VelCmd_mps * rDeltaTime_s;

    ELSIF rTraj_TimeElapsed_s <= (2.0 * rTraj_T1_JerkAcc_s + rTraj_T2_ConstAcc_s + rTraj_T4_ConstVel_s) THEN
        (* Phase 4: Maximum Velocity Cruising *)
        rTraj_JerkCmd_mps3 := 0.0;
        rTraj_AccCmd_mps2  := 0.0;
        rTraj_VelCmd_mps   := rTraj_SignDirection * rSet_ShuttleCruiseVel_mps;
        rTraj_PosCmd_m     := (rVoted_ShuttleLaserDist_mm / 1000.0) + rTraj_VelCmd_mps * rDeltaTime_s;

    ELSIF rTraj_TimeElapsed_s <= (3.0 * rTraj_T1_JerkAcc_s + rTraj_T2_ConstAcc_s + rTraj_T4_ConstVel_s) THEN
        (* Phase 5: Concave Deceleration Jerk Ramp-Up *)
        rTempSum           := rTraj_TimeElapsed_s - (2.0 * rTraj_T1_JerkAcc_s + rTraj_T2_ConstAcc_s + rTraj_T4_ConstVel_s);
        rTraj_JerkCmd_mps3 := -rTraj_SignDirection * rSet_ShuttleMaxJerk_mps3;
        rTraj_AccCmd_mps2  := -rTraj_SignDirection * rSet_ShuttleMaxJerk_mps3 * rTempSum;
        rTraj_VelCmd_mps   := rTraj_SignDirection * (rSet_ShuttleCruiseVel_mps - 0.5 * rSet_ShuttleMaxJerk_mps3 * rTempSum * rTempSum);
        rTraj_PosCmd_m     := (rVoted_ShuttleLaserDist_mm / 1000.0) + rTraj_VelCmd_mps * rDeltaTime_s;

    ELSIF rTraj_TimeElapsed_s <= (3.0 * rTraj_T1_JerkAcc_s + 2.0 * rTraj_T2_ConstAcc_s + rTraj_T4_ConstVel_s) THEN
        (* Phase 6: Constant Deceleration Cruise *)
        rTempSum           := rTraj_TimeElapsed_s - (3.0 * rTraj_T1_JerkAcc_s + rTraj_T2_ConstAcc_s + rTraj_T4_ConstVel_s);
        rTraj_JerkCmd_mps3 := 0.0;
        rTraj_AccCmd_mps2  := -rTraj_SignDirection * rSet_ShuttleMaxAccel_mps2;
        rTraj_VelCmd_mps   := rTraj_SignDirection * (rSet_ShuttleCruiseVel_mps - rSet_ShuttleMaxAccel_mps2 * rTempSum);
        rTraj_PosCmd_m     := (rVoted_ShuttleLaserDist_mm / 1000.0) + rTraj_VelCmd_mps * rDeltaTime_s;

    ELSIF rTraj_TimeElapsed_s <= rTraj_TotalMoveTime_s THEN
        (* Phase 7: Convex Deceleration Jerk Ramp-Down to Zero *)
        rTempSum           := rTraj_TimeElapsed_s - (3.0 * rTraj_T1_JerkAcc_s + 2.0 * rTraj_T2_ConstAcc_s + rTraj_T4_ConstVel_s);
        rTraj_JerkCmd_mps3 := rTraj_SignDirection * rSet_ShuttleMaxJerk_mps3;
        rTraj_AccCmd_mps2  := -rTraj_SignDirection * (rSet_ShuttleMaxAccel_mps2 - rSet_ShuttleMaxJerk_mps3 * rTempSum);
        rTraj_VelCmd_mps   := rTraj_SignDirection * (0.5 * rSet_ShuttleMaxJerk_mps3 * (rTraj_T1_JerkAcc_s - rTempSum) * (rTraj_T1_JerkAcc_s - rTempSum));
        rTraj_PosCmd_m     := (rVoted_ShuttleLaserDist_mm / 1000.0) + rTraj_VelCmd_mps * rDeltaTime_s;
    ELSE
        (* Terminal Target Reached *)
        rTraj_JerkCmd_mps3  := 0.0;
        rTraj_AccCmd_mps2   := 0.0;
        rTraj_VelCmd_mps    := 0.0;
        rTraj_PosCmd_m      := rSet_ShuttleTargetPos_m;
        bTraj_MoveActive    := FALSE;
        bTraj_MoveCompleted := TRUE;
    END_IF;
ELSE
    bTraj_MoveActive    := FALSE;
    bTraj_MoveCompleted := TRUE;
    rTraj_VelCmd_mps    := 0.0;
    rTraj_AccCmd_mps2   := 0.0;
    rTraj_JerkCmd_mps3  := 0.0;
    rTraj_PosCmd_m      := rSet_ShuttleTargetPos_m;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------
 * 2. RAIL WHEEL SLIP OBSERVER & BURCKHARDT ADHESION LIMITATION
 * ------------------------------------------------------------------------------------------------------------------- *)
(* Differentiate laser distance for true ground velocity *)
rLaserVelocity_Calc_mps := (rVoted_ShuttleLaserDist_mm - rPrevLaserPos_mm) / (1000.0 * rDeltaTime_s);
rPrevLaserPos_mm        := rVoted_ShuttleLaserDist_mm;

(* Observed wheel linear velocity: omega_w * r_w *)
rObs_WheelVelocity_mps  := rVoted_ShuttleDriveVel_mps;
rObs_LinearVelocity_mps := rLaserVelocity_Calc_mps;

(* Longitudinal wheel slip ratio sigma *)
IF ABS(rObs_LinearVelocity_mps) > 0.050 THEN
    rObs_SlipRatio := (rObs_WheelVelocity_mps - rObs_LinearVelocity_mps) / ABS(rObs_LinearVelocity_mps);
ELSE
    rObs_SlipRatio := 0.0;
END_IF;
rCalculated_WheelSlipRatio := rObs_SlipRatio;

(* Burckhardt Wheel-Rail Friction Model: mu(sigma) = c1*(1 - exp(-c2*|sigma|)) - c3*|sigma| *)
rTempSum := ABS(rObs_SlipRatio);
IF rTempSum > 0.0001 THEN
    rObs_AdhesionCoeff := c_rBurckhardt_C1 * (1.0 - EXP(-c_rBurckhardt_C2 * rTempSum)) - (c_rBurckhardt_C3 * rTempSum);
ELSE
    rObs_AdhesionCoeff := 0.650;
END_IF;

(* Maximum allowable tractive force before macro-slip: F_max = mu * M_total * g *)
IF bTotePresentOnFork THEN
    rObs_EffectiveMass_kg := c_rShuttleBareMass_kg + c_rToteMaxPayload_kg;
ELSE
    rObs_EffectiveMass_kg := c_rShuttleBareMass_kg;
END_IF;

rObs_MaxTractionForce_N := rObs_AdhesionCoeff * rObs_EffectiveMass_kg * c_rGravity;

(* -------------------------------------------------------------------------------------------------------------------
 * 3. REGENERATIVE COMMON DC BUS ENERGY BALANCING & CHOPPER RESISTOR REGULATION
 * ------------------------------------------------------------------------------------------------------------------- *)
(* Dynamic mechanical power flow on traction axis *)
rObs_RegenPower_kW := rVoted_ShuttleTorque_Nm * (rObs_WheelVelocity_mps / c_rShuttleWheelRadius_m) / 1000.0;
rCalculated_RegenPower_kW := rObs_RegenPower_kW;

(* Supercapacitor bank electrostatic energy: E = 0.5 * C * V^2 *)
rCalculated_DCBusCapacitorEnergy_kJ := 0.5 * c_rDCBusCapacitance_F * rVoted_DCBusVoltage_V * rVoted_DCBusVoltage_V / 1000.0;

(* Dynamic Braking Chopper PWM Duty Modulation *)
IF rVoted_DCBusVoltage_V >= c_rDCBusChopperOnVoltage_V THEN
    rCmd_DCBusChopperDuty_pct := MIN(100.0, ((rVoted_DCBusVoltage_V - c_rDCBusChopperOnVoltage_V) /
                                             (c_rDCBusChopperMaxVoltage_V - c_rDCBusChopperOnVoltage_V)) * 100.0);
    rObs_ChopperCurrent_A     := (rVoted_DCBusVoltage_V / c_rBrakingResistorResistance_Ohm) * (rCmd_DCBusChopperDuty_pct / 100.0);
    rObs_ChopperPower_kW      := (rVoted_DCBusVoltage_V * rObs_ChopperCurrent_A) / 1000.0;
ELSE
    rCmd_DCBusChopperDuty_pct := 0.0;
    rObs_ChopperCurrent_A     := 0.0;
    rObs_ChopperPower_kW      := 0.0;
END_IF;

(* Rate-of-Change of DC Bus Voltage *)
rDCBusVoltROC_V_s := (rVoted_DCBusVoltage_V - rPrevDCBusVolt) / rDeltaTime_s;
rPrevDCBusVolt    := rVoted_DCBusVoltage_V;

(* -------------------------------------------------------------------------------------------------------------------
 * 4. LINEAR INDUCTION MOTOR (LIM) ELECTROMAGNETIC & 2-NODE THERMAL OBSERVER
 * ------------------------------------------------------------------------------------------------------------------- *)
(* Synchronous linear wave speed: v_s = 2 * tau_p * f_e *)
rObs_LIM_SynchronousSpeed_mps := 2.0 * c_rLIMPolePitch_m * MAX(1.0, rCmd_LIM_InverterFreq_Hz);
rObs_LIM_SlipSpeed_mps        := rObs_LIM_SynchronousSpeed_mps - rVoted_CrossBeltLIMVel_mps;

IF rObs_LIM_SynchronousSpeed_mps > 0.1 THEN
    rObs_LIM_SlipFraction := rObs_LIM_SlipSpeed_mps / rObs_LIM_SynchronousSpeed_mps;
ELSE
    rObs_LIM_SlipFraction := 0.05;
END_IF;

(* LIM Equivalent Circuit Impedance Formulation *)
IF ABS(rObs_LIM_SlipFraction) > 0.001 THEN
    rObs_LIM_ImpedanceReal := c_rLIMStatorResistance_Ohm + (c_rLIMRotorResistance_Ohm / rObs_LIM_SlipFraction);
ELSE
    rObs_LIM_ImpedanceReal := c_rLIMStatorResistance_Ohm + (c_rLIMRotorResistance_Ohm / 0.001);
END_IF;

rObs_LIM_ImpedanceImag := 2.0 * c_rPi * MAX(1.0, rCmd_LIM_InverterFreq_Hz) * (c_rLIMStatorLeakageInductance_H + c_rLIMRotorLeakageInductance_H);
rObs_LIM_ImpedanceMag  := SQRT((rObs_LIM_ImpedanceReal * rObs_LIM_ImpedanceReal) + (rObs_LIM_ImpedanceImag * rObs_LIM_ImpedanceImag));

(* LIM Developed Electromagnetic Thrust Force *)
IF rObs_LIM_ImpedanceMag > 0.1 AND rObs_LIM_SynchronousSpeed_mps > 0.1 THEN
    rObs_LIM_ThrustForce_N := (3.0 * (rCmd_LIM_VoltageCmd_V * rCmd_LIM_VoltageCmd_V) * (c_rLIMRotorResistance_Ohm / MAX(0.005, ABS(rObs_LIM_SlipFraction)))) /
                              ((rObs_LIM_ImpedanceMag * rObs_LIM_ImpedanceMag) * rObs_LIM_SynchronousSpeed_mps);
ELSE
    rObs_LIM_ThrustForce_N := 0.0;
END_IF;
rCalculated_LIMThrustForce_N := rObs_LIM_ThrustForce_N;

(* Air-Gap Dynamic Mutual Magnetic Flux with High-Speed End-Effect Attenuation *)
rTempSum := 1.0 / (1.0 + 0.12 * (rVoted_CrossBeltLIMVel_mps / 3.00)); (* End-effect decay factor *)
rObs_LIM_AirGapMutualFlux_Wb := (rCmd_LIM_VoltageCmd_V / (2.0 * c_rPi * MAX(1.0, rCmd_LIM_InverterFreq_Hz))) * rTempSum * 0.0055;
rCalculated_LIMAirGapFlux_Wb := rObs_LIM_AirGapMutualFlux_Wb;

(* 2-Node Thermal Observer: Copper Winding and Stator Iron Core Lamination *)
rTempGrad := (rVoted_LIMStatorTemp_degC - rObs_LIM_CoreIronTemp_degC) / c_rLIM_ThermalRes_Cu_Fe_K_W;
rObs_LIM_WindingCopperTemp_degC := rVoted_LIMStatorTemp_degC;

(* Core Iron Dynamic Thermal Balance *)
rObs_LIM_CoreIronTemp_degC := rObs_LIM_CoreIronTemp_degC + (rDeltaTime_s / c_rLIM_ThermalCap_Fe_J_K) *
                              (rTempGrad - ((rObs_LIM_CoreIronTemp_degC - rAmbientTemperature_degC) / c_rLIM_ThermalRes_Fe_Amb_K_W));
rCalculated_LIMCoreTemp_degC := rObs_LIM_CoreIronTemp_degC;

(* -------------------------------------------------------------------------------------------------------------------
 * 5. DYNAMIC PARCEL INFEED GAP OPTIMIZER & PACING LOGIC
 * ------------------------------------------------------------------------------------------------------------------- *)
IF bVoted_ParcelLeadingEdge AND NOT bVoted_ParcelTrailingEdge THEN
    rObs_ParcelFrontEdgeTime_s := rStateDwellTimer_s;
ELSIF bVoted_ParcelTrailingEdge THEN
    rObs_ParcelRearEdgeTime_s  := rStateDwellTimer_s;
    rObs_ParcelTransitDuration_s := MAX(0.010, rObs_ParcelRearEdgeTime_s - rObs_ParcelFrontEdgeTime_s);
    IF rObs_ParcelTransitDuration_s > 0.020 THEN
        rObs_MeasuredParcelSpeed_mps := (rVoted_ParcelProfileLength_mm / 1000.0) / rObs_ParcelTransitDuration_s;
    END_IF;
END_IF;

(* Measured Dynamic Inter-Parcel Safety Margin *)
rObs_DynamicGapSeparation_mm := MAX(50.0, (rObs_MeasuredParcelSpeed_mps * rObs_ParcelTransitDuration_s * 1000.0) - rVoted_ParcelProfileLength_mm);
rCalculated_DynamicGap_mm    := rObs_DynamicGapSeparation_mm;

(* 3-Stage Infeed Belt Speed Regulation *)
IF bAutoSortEnable THEN
    rCmd_InfeedBelt1_Speed_mps := 1.800; (* Metering Infeed Belt *)
    IF rCalculated_DynamicGap_mm < rSet_MinParcelGap_mm THEN
        (* Expand inter-parcel gap via differential acceleration on Belt 2 *)
        rCmd_InfeedBelt2_Speed_mps := 2.200;
        rCmd_InfeedBelt3_Speed_mps := 3.000;
    ELSE
        rCmd_InfeedBelt2_Speed_mps := 2.600;
        rCmd_InfeedBelt3_Speed_mps := 3.000; (* Synchronous Injection to 3.0 m/s Sorter *)
    END_IF;
ELSE
    rCmd_InfeedBelt1_Speed_mps := 0.0;
    rCmd_InfeedBelt2_Speed_mps := 0.0;
    rCmd_InfeedBelt3_Speed_mps := 0.0;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------
 * 6. 2D CROSS-BELT DIVERTER EJECTION KINEMATICS
 * ------------------------------------------------------------------------------------------------------------------- *)
(* Solve 2D resultant takeoff velocity vector: v_res = [v_sorter, v_crossbelt]^T *)
rObs_EjectionAngle_Rad      := rSet_ChuteEjectionAngle_deg * (c_rPi / 180.0);
(* v_crossbelt = v_sorter * TAN(theta_eject) *)
rObs_EjectionVelocity_Y_mps := rVoted_CrossBeltLIMVel_mps * (SIN(rObs_EjectionAngle_Rad) / MAX(0.1, COS(rObs_EjectionAngle_Rad)));
rObs_EjectionVelocity_Y_mps := MIN(2.500, MAX(0.500, rObs_EjectionVelocity_Y_mps));
rCalculated_EjectionAngle_deg := ATAN2(rObs_EjectionVelocity_Y_mps, MAX(0.1, rVoted_CrossBeltLIMVel_mps)) * (180.0 / c_rPi);

(* -------------------------------------------------------------------------------------------------------------------
 * 7. FIRE COMPARTMENT HIGH-SPEED ROLL-UP GUILLOTINE SHUTTER INTERLOCK
 * ------------------------------------------------------------------------------------------------------------------- *)
IF NOT bFireAlarmZoneClear OR (rVoted_FireRollupShutterPos_mm < 2100.0) THEN
    bGuillotineEmergencyDropActive := TRUE;
    (* Verify no cart/parcel is straddling the guillotine descent line *)
    rTempSum := ABS((rVoted_CrossBeltCartPulse * c_rCartPitchLength_m) - 96.000); (* Gate coordinate at 96.0 m *)
    IF rTempSum < rGuillotineClearanceZone_m THEN
        bFireGuillotineZoneBlocked := TRUE;
        bCmd_FireShutterPermissive := FALSE; (* Inhibit Guillotine Drop to Prevent Trapping/Damage *)
    ELSE
        bFireGuillotineZoneBlocked := FALSE;
        bCmd_FireShutterPermissive := TRUE;  (* Zone Clear: Allow Fast Drop *)
    END_IF;
ELSE
    bGuillotineEmergencyDropActive := FALSE;
    bFireGuillotineZoneBlocked     := FALSE;
    bCmd_FireShutterPermissive     := TRUE;
END_IF;
"""

def get_control_logic_phase3():
    return """(* ===================================================================================================================
 * PHASE 3: RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) & PROJECTED GRADIENT DESCENT (PGD)
 * =================================================================================================================== *)
(* Construct Normalized Dynamic State Error Vector x[1..8] *)
ax_state[1] := (rVoted_ShuttleLaserDist_mm / 1000.0) - rTraj_PosCmd_m;
ax_state[2] := rVoted_ShuttleDriveVel_mps - rTraj_VelCmd_mps;
ax_state[3] := rVoted_DCBusVoltage_V - c_rDCBusNominalVoltage_V;
ax_state[4] := rVoted_CrossBeltLIMVel_mps - rSet_CrossBeltNominalVel_mps;
ax_state[5] := (rCalculated_DynamicGap_mm / 1000.0) - (rSet_MinParcelGap_mm / 1000.0);
ax_state[6] := (rVoted_TelescopicForkPos_mm / 1000.0) - (rSet_ForkTargetStroke_mm / 1000.0);
ax_state[7] := rVoted_LIMStatorTemp_degC - 60.0;
ax_state[8] := rObs_RegenPower_kW;

(* Reference State Equilibrium Setpoint Vector x_ref[1..8] *)
FOR kStateIdx := 1 TO 8 DO
    ax_ref[kStateIdx] := 0.0;
END_FOR;

(* Projected Gradient Descent (PGD) Iterative Receding Horizon Solver (3 Iterations per 2 ms Cycle) *)
FOR iterMPC := 1 TO 3 DO
    (* 1. Propagate 1-Step Predictive State Vector: x_pred = A * x + B * u *)
    FOR iMatRow := 1 TO 8 DO
        rTempSum := 0.0;
        FOR iMatCol := 1 TO 8 DO
            rTempSum := rTempSum + (aA[iMatRow, iMatCol] * ax_state[iMatCol]);
        END_FOR;
        FOR mInIdx := 1 TO 6 DO
            rTempSum := rTempSum + (aB[iMatRow, mInIdx] * au_control[mInIdx]);
        END_FOR;
        aPredictedState[iMatRow] := rTempSum;
    END_FOR;

    (* 2. Evaluate Analytical Gradient dJ/du across all 6 Actuators *)
    FOR mInIdx := 1 TO 6 DO
        rTempGrad := 0.0;
        (* State tracking and terminal cost error sensitivity: 2 * sum((Q + P) * (x_pred - x_ref) * B) *)
        FOR iMatRow := 1 TO 8 DO
            rTempGrad := rTempGrad + (2.0 * (aQ_Weight[iMatRow] + aP_TerminalWeight[iMatRow]) *
                                      (aPredictedState[iMatRow] - ax_ref[iMatRow]) * aB[iMatRow, mInIdx]);
        END_FOR;
        (* Control effort regularization: 2 * R * u *)
        rTempGrad := rTempGrad + (2.0 * aR_Weight[mInIdx] * au_control[mInIdx]);
        (* Control slew rate penalty: 2 * S * (u - u_prev) *)
        rTempGrad := rTempGrad + (2.0 * aS_Weight[mInIdx] * (au_control[mInIdx] - au_prev[mInIdx]));
        aGrad_u[mInIdx] := rTempGrad;

        (* 3. Update Actuator Control via Gradient Step *)
        au_control[mInIdx] := au_control[mInIdx] - (c_rPGD_Alpha * aGrad_u[mInIdx]);

        (* 4. Slew Rate Limiting Constraints: |Delta_u| <= adelta_u_max *)
        au_delta[mInIdx] := au_control[mInIdx] - au_prev[mInIdx];
        IF au_delta[mInIdx] > adelta_u_max[mInIdx] THEN
            au_control[mInIdx] := au_prev[mInIdx] + adelta_u_max[mInIdx];
        ELSIF au_delta[mInIdx] < -adelta_u_max[mInIdx] THEN
            au_control[mInIdx] := au_prev[mInIdx] - adelta_u_max[mInIdx];
        END_IF;

        (* 5. Hard Physical Saturation Clamping: au_min <= u <= au_max *)
        IF au_control[mInIdx] > au_max[mInIdx] THEN
            au_control[mInIdx] := au_max[mInIdx];
        ELSIF au_control[mInIdx] < au_min[mInIdx] THEN
            au_control[mInIdx] := au_min[mInIdx];
        END_IF;
    END_FOR;
END_FOR;

(* Store Control History for Slew Damping *)
FOR mInIdx := 1 TO 6 DO
    au_prev[mInIdx] := au_control[mInIdx];
END_FOR;

(* Calculate Realized Objective Cost Function J *)
rMPC_QuadraticCostAccum := 0.0;
FOR iMatRow := 1 TO 8 DO
    rMPC_QuadraticCostAccum := rMPC_QuadraticCostAccum +
                               (aQ_Weight[iMatRow] * (aPredictedState[iMatRow] - ax_ref[iMatRow]) * (aPredictedState[iMatRow] - ax_ref[iMatRow]));
END_FOR;
FOR mInIdx := 1 TO 6 DO
    rMPC_QuadraticCostAccum := rMPC_QuadraticCostAccum +
                               (aR_Weight[mInIdx] * au_control[mInIdx] * au_control[mInIdx]) +
                               (aS_Weight[mInIdx] * au_delta[mInIdx] * au_delta[mInIdx]);
END_FOR;
rMPC_QuadraticCost_J := rMPC_QuadraticCostAccum;

(* -------------------------------------------------------------------------------------------------------------------
 * ACTUATOR DISPATCH: MAP OPTIMAL MPC INPUTS TO PHYSICAL HARDWARE LOOPS
 * ------------------------------------------------------------------------------------------------------------------- *)
(* u1 -> Shuttle Traction Torque: Inertial Feedforward + MPC Correction *)
rTempSum := (rObs_EffectiveMass_kg * rTraj_AccCmd_mps2 * c_rShuttleWheelRadius_m) / c_rShuttleGearboxRatio; (* Feedforward torque *)
rTempSum := rTempSum + au_control[1]; (* Add MPC Closed-Loop Vector Correction *)

(* Clamp Torque Command to Non-Skid Rail Adhesion Boundary *)
rTempGrad := (rObs_MaxTractionForce_N * c_rShuttleWheelRadius_m) / c_rShuttleGearboxRatio;
IF rTempSum > rTempGrad THEN
    rTempSum := rTempGrad;
ELSIF rTempSum < -rTempGrad THEN
    rTempSum := -rTempGrad;
END_IF;

rCmd_ShuttleTractionTorque_Nm := rTempSum;
rCmd_ShuttleDriveSpeed_RPM    := (rTraj_VelCmd_mps / (2.0 * c_rPi * c_rShuttleWheelRadius_m)) * c_rShuttleGearboxRatio * 60.0;

(* u2 -> DC Bus Chopper Duty: Combine MPC with Voltage Threshold Hysteresis *)
rCmd_DCBusChopperDuty_pct     := MAX(rCmd_DCBusChopperDuty_pct, au_control[2]);

(* u3 -> LIM Inverter Voltage & Frequency Coordination *)
rCmd_LIM_VoltageCmd_V         := MIN(480.0, MAX(0.0, 380.0 + au_control[3]));
rCmd_LIM_InverterFreq_Hz      := (rSet_CrossBeltNominalVel_mps / (2.0 * c_rLIMPolePitch_m)) * (1.0 + rObs_LIM_SlipFraction);

(* u6 -> Telescopic Fork Lateral Linear Velocity *)
rCmd_TelescopicForkSpeed_mps  := au_control[6];
"""

def get_control_logic_phase4():
    return """(* ===================================================================================================================
 * PHASE 4: 12-STAGE DETERMINISTIC OPERATIONAL FINITE STATE MACHINE (FSM)
 * =================================================================================================================== *)
(* Advance Operational Chronometers *)
rStateDwellTimer_s  := rStateDwellTimer_s + rDeltaTime_s;
rOperationalTimer_h := rOperationalTimer_h + (rDeltaTime_s / 3600.0);
rThroughputTimer_s  := rThroughputTimer_s + rDeltaTime_s;

(* Compute Instantaneous Throughput Rate (parcels per hour) *)
IF rThroughputTimer_s >= 60.0 THEN
    rCalculated_Throughput_pph := (DINT_TO_REAL(rThroughputCounter) / rThroughputTimer_s) * 3600.0;
    rThroughputCounter := 0;
    rThroughputTimer_s := 0.0;
END_IF;

CASE iFSM_State OF
    (* ---------------------------------------------------------------------------------------------------------------
     * STATE 0: STANDBY_HOMING_CALIBRATION
     * --------------------------------------------------------------------------------------------------------------- *)
    0:
        bSystemReady             := TRUE;
        bSystemRunning           := FALSE;
        bCaliperBrakeClamped     := TRUE;
        bCmd_CaliperBrakeRelease := FALSE;
        rCmd_ShuttleTractionTorque_Nm   := 0.0;
        rCmd_ShuttleDriveSpeed_RPM      := 0.0;
        rCmd_TelescopicForkSpeed_mps    := 0.0;
        rCmd_LIM_VoltageCmd_V           := 0.0;
        rCmd_LIM_InverterFreq_Hz        := 0.0;
        rCmd_InfeedBelt1_Speed_mps      := 0.0;
        rCmd_InfeedBelt2_Speed_mps      := 0.0;
        rCmd_InfeedBelt3_Speed_mps      := 0.0;
        bCmd_CrossBeltEjectTrigger      := FALSE;

        (* Verify Laser Distance Calibration & Fork Retraction *)
        IF ABS(rVoted_TelescopicForkPos_mm) < 2.0 THEN
            bShuttleTargetReached := TRUE;
        ELSE
            (* Retract fork to home position at low speed *)
            rCmd_TelescopicForkSpeed_mps := -0.150;
        END_IF;

        IF bMasterEnable AND bAutoShuttleEnable AND NOT bEmergencyTripped THEN
            rStateDwellTimer_s := 0.0;
            iFSM_State         := STATE_DC_BUS_PRECHARGE_AND_SYNC;
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------
     * STATE 1: DC_BUS_PRECHARGE_AND_SYNC
     * --------------------------------------------------------------------------------------------------------------- *)
    1:
        bSystemReady             := TRUE;
        bSystemRunning           := FALSE;
        bCaliperBrakeClamped     := TRUE;
        bCmd_CaliperBrakeRelease := FALSE;

        rPrechargeTimer_s := rPrechargeTimer_s + rDeltaTime_s;

        (* Verify Intermediate DC Bus Potential reaches nominal 750 V (+/- 30 V) *)
        IF (rVoted_DCBusVoltage_V >= 720.0) AND (rPrechargeTimer_s >= 1.200) THEN
            rPrechargeTimer_s  := 0.0;
            rStateDwellTimer_s := 0.0;
            IF bAutoSortEnable THEN
                iFSM_State := STATE_CROSSBELT_LOOP_ACCELERATION_3MPS;
            ELSE
                iFSM_State := STATE_EMPTY_TOTE_BUFFER_ALLOCATION;
            END_IF;
        ELSIF rPrechargeTimer_s > 8.000 THEN
            (* Precharge Timeout: DC Bus Undervoltage Brownout *)
            bEmergencyTripped := TRUE;
            iFSM_State        := STATE_EMERGENCY_ESTOP_RAIL_CLAMP;
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------
     * STATE 2: EMPTY_TOTE_BUFFER_ALLOCATION
     * --------------------------------------------------------------------------------------------------------------- *)
    2:
        bSystemReady             := TRUE;
        bSystemRunning           := TRUE;
        bCaliperBrakeClamped     := FALSE;
        bCmd_CaliperBrakeRelease := TRUE; (* Release Caliper Disc Brakes for Travel *)

        (* Parse Assigned Storage Bay Destination & Verify Safety Curtains *)
        IF bRackZone1Permissive AND bRackZone2Permissive THEN
            bTraj_MoveActive    := FALSE;
            bTraj_MoveCompleted := FALSE;
            rStateDwellTimer_s  := 0.0;
            iFSM_State          := STATE_SHUTTLE_HIGH_SPEED_RACK_TRAVEL;
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------
     * STATE 3: SHUTTLE_HIGH_SPEED_RACK_TRAVEL
     * --------------------------------------------------------------------------------------------------------------- *)
    3:
        bSystemReady             := TRUE;
        bSystemRunning           := TRUE;
        bCaliperBrakeClamped     := FALSE;
        bCmd_CaliperBrakeRelease := TRUE;

        (* S-Curve Motion Profile & MPC Vector Velocity Execution Active *)
        IF bTraj_MoveCompleted AND (ABS(rTraj_TotalDistance_m) <= 0.002) AND (ABS(rVoted_ShuttleDriveVel_mps) < 0.010) THEN
            bShuttleTargetReached := TRUE;
            rStateDwellTimer_s    := 0.0;
            rForkStrokeTimer_s    := 0.0;
            iFSM_State            := STATE_TELESCOPIC_FORK_EXTEND_AND_PICK;
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------
     * STATE 4: TELESCOPIC_FORK_EXTEND_AND_PICK
     * --------------------------------------------------------------------------------------------------------------- *)
    4:
        bSystemReady             := TRUE;
        bSystemRunning           := TRUE;
        bCaliperBrakeClamped     := FALSE;
        bCmd_CaliperBrakeRelease := TRUE;
        rForkStrokeTimer_s       := rForkStrokeTimer_s + rDeltaTime_s;

        (* Step 1: Extend Telescopic Fork into Bay (0 to 1250 mm) *)
        IF NOT bToteCenteringClamped THEN
            IF rVoted_TelescopicForkPos_mm < (rSet_ForkTargetStroke_mm - 5.0) THEN
                rCmd_TelescopicForkSpeed_mps := 0.850; (* High-Speed Lateral Stroke Insertion *)
            ELSE
                rCmd_TelescopicForkSpeed_mps := 0.0;
                bToteCenteringClamped        := TRUE; (* Clamping Jaws Engage Tote Handles *)
            END_IF;
        ELSE
            (* Step 2: Retract Fork with Tote Loaded back to Shuttle Carriage *)
            IF rVoted_TelescopicForkPos_mm > 5.0 THEN
                rCmd_TelescopicForkSpeed_mps := -0.850; (* High-Speed Retraction *)
            ELSE
                rCmd_TelescopicForkSpeed_mps := 0.0;
                bTotePickCompleted           := TRUE;
                rStateDwellTimer_s           := 0.0;
                iFSM_State                   := STATE_DECELERATION_AND_ELEVATOR_HANDOFF;
            END_IF;
        END_IF;

        IF rForkStrokeTimer_s > 6.500 THEN
            (* Telescopic Fork Jam Timeout *)
            bEmergencyTripped := TRUE;
            iFSM_State        := STATE_EMERGENCY_ESTOP_RAIL_CLAMP;
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------
     * STATE 5: DECELERATION_AND_ELEVATOR_HANDOFF
     * --------------------------------------------------------------------------------------------------------------- *)
    5:
        bSystemReady             := TRUE;
        bSystemRunning           := TRUE;
        bCaliperBrakeClamped     := FALSE;
        bCmd_CaliperBrakeRelease := TRUE;
        rElevatorSyncTimer_s     := rElevatorSyncTimer_s + rDeltaTime_s;

        (* Verify Elevator Lifter Station Alignment *)
        IF bElevatorVerticalReady THEN
            bCmd_ElevatorInterlockRelease := TRUE;
            IF rElevatorSyncTimer_s >= 0.800 THEN
                bTotePickCompleted            := FALSE;
                bCmd_ElevatorInterlockRelease := FALSE;
                rElevatorSyncTimer_s          := 0.0;
                rStateDwellTimer_s            := 0.0;
                IF bAutoSortEnable THEN
                    iFSM_State := STATE_CROSSBELT_LOOP_ACCELERATION_3MPS;
                ELSE
                    iFSM_State := STATE_EMPTY_TOTE_BUFFER_ALLOCATION;
                END_IF;
            END_IF;
        ELSE
            bCmd_ElevatorInterlockRelease := FALSE;
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------
     * STATE 6: CROSSBELT_LOOP_ACCELERATION_3MPS
     * --------------------------------------------------------------------------------------------------------------- *)
    6:
        bSystemReady   := TRUE;
        bSystemRunning := TRUE;
        rLIMRampTimer_s := rLIMRampTimer_s + rDeltaTime_s;

        (* Linear Induction Motor Frequency Ramp to 3.0 m/s Carrier Velocity *)
        IF rVoted_CrossBeltLIMVel_mps < 2.950 THEN
            rCmd_LIM_InverterFreq_Hz := MIN(10.50, rLIMRampTimer_s * 2.25);
            rCmd_LIM_VoltageCmd_V    := MIN(400.0, rLIMRampTimer_s * 85.0);
        ELSE
            rCmd_LIM_InverterFreq_Hz := 10.50;
            rCmd_LIM_VoltageCmd_V    := 400.0;
            rLIMRampTimer_s          := 0.0;
            rStateDwellTimer_s       := 0.0;
            iFSM_State               := STATE_DYNAMIC_INFEED_GAP_REGULATION;
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------
     * STATE 7: DYNAMIC_INFEED_GAP_REGULATION
     * --------------------------------------------------------------------------------------------------------------- *)
    7:
        bSystemReady   := TRUE;
        bSystemRunning := TRUE;

        (* Continuous Infeed Gap Regulation & Sorter Cart Slot Injection *)
        IF bVoted_ParcelLeadingEdge THEN
            rInfeedGapTimer_s := rInfeedGapTimer_s + rDeltaTime_s;
            (* Check if parcel is ready for high-speed divert *)
            IF rInfeedGapTimer_s >= 0.250 THEN
                rInfeedGapTimer_s  := 0.0;
                rStateDwellTimer_s := 0.0;
                iFSM_State         := STATE_HIGH_SPEED_DISCHARGE_EJECTION;
            END_IF;
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------
     * STATE 8: HIGH_SPEED_DISCHARGE_EJECTION
     * --------------------------------------------------------------------------------------------------------------- *)
    8:
        bSystemReady   := TRUE;
        bSystemRunning := TRUE;
        rEjectionDwellTimer_s := rEjectionDwellTimer_s + rDeltaTime_s;

        (* Check Target Chute Congestion *)
        IF bVoted_DischargeChuteFull THEN
            bChuteCongestionAlarm      := TRUE;
            bCmd_CrossBeltEjectTrigger := FALSE; (* Inhibit Divert to Prevent Chute Pile-Up *)
            rCmd_CrossBeltEjectVelocity_mps := 0.0;
            (* Re-circulate parcel around sorter loop *)
            iFSM_State := STATE_REGENERATIVE_ENERGY_BALANCING;
        ELSE
            bChuteCongestionAlarm      := FALSE;
            bCmd_CrossBeltEjectTrigger := TRUE;
            rCmd_CrossBeltEjectVelocity_mps := rObs_EjectionVelocity_Y_mps;

            IF rEjectionDwellTimer_s >= rObs_EjectionTrajectoryTime_s THEN
                bCmd_CrossBeltEjectTrigger      := FALSE;
                rCmd_CrossBeltEjectVelocity_mps := 0.0;
                bParcelSortedSuccess            := TRUE;
                rThroughputCounter              := rThroughputCounter + 1;
                rEjectionDwellTimer_s           := 0.0;
                rStateDwellTimer_s              := 0.0;
                iFSM_State                      := STATE_REGENERATIVE_ENERGY_BALANCING;
            END_IF;
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------
     * STATE 9: REGENERATIVE_ENERGY_BALANCING
     * --------------------------------------------------------------------------------------------------------------- *)
    9:
        bSystemReady   := TRUE;
        bSystemRunning := TRUE;

        (* Balance DC bus potential across accelerating shuttles and braking sorters *)
        IF NOT bAutoSortEnable AND NOT bAutoShuttleEnable THEN
            rStateDwellTimer_s := 0.0;
            iFSM_State         := STATE_CONTROLLED_LOOP_PURGE_EMPTY;
        ELSE
            rStateDwellTimer_s := 0.0;
            iFSM_State         := STATE_DYNAMIC_INFEED_GAP_REGULATION;
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------
     * STATE 10: CONTROLLED_LOOP_PURGE_EMPTY
     * --------------------------------------------------------------------------------------------------------------- *)
    10:
        bSystemReady   := TRUE;
        bSystemRunning := FALSE;
        rPurgeCycleTimer_s := rPurgeCycleTimer_s + rDeltaTime_s;

        (* Stop Infeed Conveyors *)
        rCmd_InfeedBelt1_Speed_mps := 0.0;
        rCmd_InfeedBelt2_Speed_mps := 0.0;
        rCmd_InfeedBelt3_Speed_mps := 0.0;

        (* Ramp Down Linear Induction Motor Sorter to Rest *)
        IF rVoted_CrossBeltLIMVel_mps > 0.050 THEN
            rCmd_LIM_InverterFreq_Hz := MAX(0.0, 10.50 - (rPurgeCycleTimer_s * 1.50));
            rCmd_LIM_VoltageCmd_V    := MAX(0.0, 400.0 - (rPurgeCycleTimer_s * 55.0));
        ELSE
            rCmd_LIM_InverterFreq_Hz := 0.0;
            rCmd_LIM_VoltageCmd_V    := 0.0;
            rPurgeCycleTimer_s       := 0.0;
            rStateDwellTimer_s       := 0.0;
            iFSM_State               := STATE_STANDBY_HOMING_CALIBRATION;
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------
     * STATE 11: EMERGENCY_ESTOP_RAIL_CLAMP
     * --------------------------------------------------------------------------------------------------------------- *)
    11:
        bSystemReady             := FALSE;
        bSystemRunning           := FALSE;
        bEmergencyTripped        := TRUE;
        bCaliperBrakeClamped     := TRUE;  (* Mechanical Rail Caliper Disc Brake Clamped (< 20 ms) *)
        bCmd_CaliperBrakeRelease := FALSE;
        rCmd_ShuttleTractionTorque_Nm   := 0.0;
        rCmd_ShuttleDriveSpeed_RPM      := 0.0;
        rCmd_TelescopicForkSpeed_mps    := 0.0;
        rCmd_LIM_VoltageCmd_V           := 0.0;
        rCmd_LIM_InverterFreq_Hz        := 0.0;
        rCmd_InfeedBelt1_Speed_mps      := 0.0;
        rCmd_InfeedBelt2_Speed_mps      := 0.0;
        rCmd_InfeedBelt3_Speed_mps      := 0.0;
        bCmd_CrossBeltEjectTrigger      := FALSE;
        rCaliperBrakeTimer_s            := rCaliperBrakeTimer_s + rDeltaTime_s;

        (* Manual Reset Pushbutton Handshake Required *)
        IF bFaultReset AND bEmergencyStop_NC AND bMasterEnable THEN
            bEmergencyTripped    := FALSE;
            bCaliperBrakeClamped := TRUE;
            rCaliperBrakeTimer_s := 0.0;
            rStateDwellTimer_s   := 0.0;
            iFSM_State           := STATE_STANDBY_HOMING_CALIBRATION;
        END_IF;

    ELSE
        (* Illegal State Recovery Handler *)
        bEmergencyTripped := TRUE;
        iFSM_State        := STATE_EMERGENCY_ESTOP_RAIL_CLAMP;
END_CASE;

nActiveFSM_State := iFSM_State;
"""

def get_control_logic_phase5():
    return """(* ===================================================================================================================
 * PHASE 5: ISA-18.2 MULTI-TIERED ALARM ENGINE & DIAGNOSTIC WORD BIT-PACKING
 * =================================================================================================================== *)

(* -------------------------------------------------------------------------------------------------------------------
 * 1. PROCESS ALARM EVALUATION WITH DEADBAND HYSTERESIS
 * ------------------------------------------------------------------------------------------------------------------- *)
(* Shuttle Velocity Alarms *)
IF ABS(rVoted_ShuttleDriveVel_mps) >= c_rAlm_ShuttleVel_HH THEN
    bAlm_ShuttleVel_HH := TRUE;
    bEmergencyTripped  := TRUE;
    iFSM_State         := STATE_EMERGENCY_ESTOP_RAIL_CLAMP;
ELSIF ABS(rVoted_ShuttleDriveVel_mps) < (c_rAlm_ShuttleVel_HH - c_rAlm_ShuttleVel_Deadband) THEN
    bAlm_ShuttleVel_HH := FALSE;
END_IF;

IF ABS(rVoted_ShuttleDriveVel_mps) >= c_rAlm_ShuttleVel_H THEN
    bAlm_ShuttleVel_H := TRUE;
ELSIF ABS(rVoted_ShuttleDriveVel_mps) < (c_rAlm_ShuttleVel_H - c_rAlm_ShuttleVel_Deadband) THEN
    bAlm_ShuttleVel_H := FALSE;
END_IF;

(* DC Bus Voltage Alarms *)
IF rVoted_DCBusVoltage_V >= c_rAlm_DCBusVolt_HH THEN
    bAlm_DCBusVolt_HH := TRUE;
    bEmergencyTripped := TRUE;
    iFSM_State        := STATE_EMERGENCY_ESTOP_RAIL_CLAMP;
ELSIF rVoted_DCBusVoltage_V < (c_rAlm_DCBusVolt_HH - c_rAlm_DCBusVolt_Deadband) THEN
    bAlm_DCBusVolt_HH := FALSE;
END_IF;

IF rVoted_DCBusVoltage_V >= c_rAlm_DCBusVolt_H THEN
    bAlm_DCBusVolt_H := TRUE;
ELSIF rVoted_DCBusVoltage_V < (c_rAlm_DCBusVolt_H - c_rAlm_DCBusVolt_Deadband) THEN
    bAlm_DCBusVolt_H := FALSE;
END_IF;

IF rVoted_DCBusVoltage_V <= c_rAlm_DCBusVolt_LL THEN
    bAlm_DCBusVolt_LL := TRUE;
    bEmergencyTripped := TRUE;
    iFSM_State        := STATE_EMERGENCY_ESTOP_RAIL_CLAMP;
ELSIF rVoted_DCBusVoltage_V > (c_rAlm_DCBusVolt_LL + c_rAlm_DCBusVolt_Deadband) THEN
    bAlm_DCBusVolt_LL := FALSE;
END_IF;

IF rVoted_DCBusVoltage_V <= c_rAlm_DCBusVolt_L THEN
    bAlm_DCBusVolt_L := TRUE;
ELSIF rVoted_DCBusVoltage_V > (c_rAlm_DCBusVolt_L + c_rAlm_DCBusVolt_Deadband) THEN
    bAlm_DCBusVolt_L := FALSE;
END_IF;

(* LIM Stator Temperature Alarms *)
IF rVoted_LIMStatorTemp_degC >= c_rAlm_LIMTemp_HH THEN
    bAlm_LIMTemp_HH   := TRUE;
    bEmergencyTripped := TRUE;
    iFSM_State        := STATE_EMERGENCY_ESTOP_RAIL_CLAMP;
ELSIF rVoted_LIMStatorTemp_degC < (c_rAlm_LIMTemp_HH - c_rAlm_LIMTemp_Deadband) THEN
    bAlm_LIMTemp_HH := FALSE;
END_IF;

IF rVoted_LIMStatorTemp_degC >= c_rAlm_LIMTemp_H THEN
    bAlm_LIMTemp_H := TRUE;
ELSIF rVoted_LIMStatorTemp_degC < (c_rAlm_LIMTemp_H - c_rAlm_LIMTemp_Deadband) THEN
    bAlm_LIMTemp_H := FALSE;
END_IF;

(* Traction Wheel Slip Derailment Alarms *)
IF ABS(rCalculated_WheelSlipRatio) >= c_rAlm_WheelSlip_HH THEN
    bAlm_WheelSlip_HH := TRUE;
    bEmergencyTripped := TRUE;
    iFSM_State        := STATE_EMERGENCY_ESTOP_RAIL_CLAMP;
ELSIF ABS(rCalculated_WheelSlipRatio) < (c_rAlm_WheelSlip_HH - c_rAlm_WheelSlip_Deadband) THEN
    bAlm_WheelSlip_HH := FALSE;
END_IF;

IF ABS(rCalculated_WheelSlipRatio) >= c_rAlm_WheelSlip_H THEN
    bAlm_WheelSlip_H := TRUE;
ELSIF ABS(rCalculated_WheelSlipRatio) < (c_rAlm_WheelSlip_H - c_rAlm_WheelSlip_Deadband) THEN
    bAlm_WheelSlip_H := FALSE;
END_IF;

(* Dynamic Infeed Parcel Gap Alarms *)
IF rCalculated_DynamicGap_mm <= c_rAlm_ParcelGap_LL THEN
    bAlm_ParcelGap_LL := TRUE;
    bEmergencyTripped := TRUE;
    iFSM_State        := STATE_EMERGENCY_ESTOP_RAIL_CLAMP;
ELSIF rCalculated_DynamicGap_mm > (c_rAlm_ParcelGap_LL + c_rAlm_ParcelGap_Deadband) THEN
    bAlm_ParcelGap_LL := FALSE;
END_IF;

IF rCalculated_DynamicGap_mm <= c_rAlm_ParcelGap_L THEN
    bAlm_ParcelGap_L := TRUE;
ELSIF rCalculated_DynamicGap_mm > (c_rAlm_ParcelGap_L + c_rAlm_ParcelGap_Deadband) THEN
    bAlm_ParcelGap_L := FALSE;
END_IF;

(* Telescopic Fork Mechanical Overtravel Alarm *)
IF ABS(rVoted_TelescopicForkPos_mm) >= c_rAlm_ForkStroke_HH THEN
    bAlm_ForkStroke_HH := TRUE;
    bEmergencyTripped  := TRUE;
    iFSM_State         := STATE_EMERGENCY_ESTOP_RAIL_CLAMP;
ELSIF ABS(rVoted_TelescopicForkPos_mm) < (c_rAlm_ForkStroke_HH - c_rAlm_ForkStroke_Deadband) THEN
    bAlm_ForkStroke_HH := FALSE;
END_IF;

(* Chute Backup Overflow Warning *)
bAlm_ChuteBackupFull_Warning := bVoted_DischargeChuteFull;

(* Alarm Reset Latch *)
IF bFaultReset THEN
    bAlm_ShuttleVel_HH           := FALSE;
    bAlm_DCBusVolt_HH            := FALSE;
    bAlm_DCBusVolt_LL            := FALSE;
    bAlm_LIMTemp_HH              := FALSE;
    bAlm_WheelSlip_HH            := FALSE;
    bAlm_ParcelGap_LL            := FALSE;
    bAlm_ForkStroke_HH           := FALSE;
    bAlm_TMR_SensorDegraded      := FALSE;
    bAlm_FireZoneGuillotine_Trip := FALSE;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------
 * 2. DIAGNOSTIC WORD BIT-PACKING FOR SCADA / INDUSTRIAL TELEMETRY
 * ------------------------------------------------------------------------------------------------------------------- *)
(* dwStatusWord_Shuttle: Operational Flags and FSM Index *)
dwStatusWord_Shuttle := 16#0000_0000;
IF bSystemReady                   THEN dwStatusWord_Shuttle := dwStatusWord_Shuttle OR 16#0000_0001; END_IF;
IF bSystemRunning                 THEN dwStatusWord_Shuttle := dwStatusWord_Shuttle OR 16#0000_0002; END_IF;
IF bEmergencyTripped              THEN dwStatusWord_Shuttle := dwStatusWord_Shuttle OR 16#0000_0004; END_IF;
IF bCaliperBrakeClamped           THEN dwStatusWord_Shuttle := dwStatusWord_Shuttle OR 16#0000_0008; END_IF;
IF bShuttleTargetReached          THEN dwStatusWord_Shuttle := dwStatusWord_Shuttle OR 16#0000_0010; END_IF;
IF bTotePresentOnFork             THEN dwStatusWord_Shuttle := dwStatusWord_Shuttle OR 16#0000_0020; END_IF;
IF bToteCenteringClamped          THEN dwStatusWord_Shuttle := dwStatusWord_Shuttle OR 16#0000_0040; END_IF;
IF bTotePickCompleted             THEN dwStatusWord_Shuttle := dwStatusWord_Shuttle OR 16#0000_0080; END_IF;
IF bRackZone1Permissive           THEN dwStatusWord_Shuttle := dwStatusWord_Shuttle OR 16#0000_0100; END_IF;
IF bRackZone2Permissive           THEN dwStatusWord_Shuttle := dwStatusWord_Shuttle OR 16#0000_0200; END_IF;
IF bElevatorVerticalReady         THEN dwStatusWord_Shuttle := dwStatusWord_Shuttle OR 16#0000_0400; END_IF;
IF bCmd_ElevatorInterlockRelease  THEN dwStatusWord_Shuttle := dwStatusWord_Shuttle OR 16#0000_0800; END_IF;
dwStatusWord_Shuttle := dwStatusWord_Shuttle OR SHL(INT_TO_DWORD(iFSM_State AND 16#0F), 12);

(* dwStatusWord_Sorter: Sorter Loop & Dynamic Infeed Status *)
dwStatusWord_Sorter := 16#0000_0000;
IF bAutoSortEnable                THEN dwStatusWord_Sorter := dwStatusWord_Sorter OR 16#0000_0001; END_IF;
IF bVoted_ParcelLeadingEdge       THEN dwStatusWord_Sorter := dwStatusWord_Sorter OR 16#0000_0002; END_IF;
IF bVoted_ParcelTrailingEdge      THEN dwStatusWord_Sorter := dwStatusWord_Sorter OR 16#0000_0004; END_IF;
IF bBarcodeScannerGoodRead        THEN dwStatusWord_Sorter := dwStatusWord_Sorter OR 16#0000_0008; END_IF;
IF bCmd_CrossBeltEjectTrigger     THEN dwStatusWord_Sorter := dwStatusWord_Sorter OR 16#0000_0010; END_IF;
IF bParcelSortedSuccess           THEN dwStatusWord_Sorter := dwStatusWord_Sorter OR 16#0000_0020; END_IF;
IF bChuteCongestionAlarm          THEN dwStatusWord_Sorter := dwStatusWord_Sorter OR 16#0000_0040; END_IF;
IF bVoted_DischargeChuteFull      THEN dwStatusWord_Sorter := dwStatusWord_Sorter OR 16#0000_0080; END_IF;
IF bFireAlarmZoneClear            THEN dwStatusWord_Sorter := dwStatusWord_Sorter OR 16#0000_0100; END_IF;
IF bFireGuillotineZoneBlocked     THEN dwStatusWord_Sorter := dwStatusWord_Sorter OR 16#0000_0200; END_IF;
IF bCmd_FireShutterPermissive     THEN dwStatusWord_Sorter := dwStatusWord_Sorter OR 16#0000_0400; END_IF;
IF bGuillotineEmergencyDropActive THEN dwStatusWord_Sorter := dwStatusWord_Sorter OR 16#0000_0800; END_IF;

(* dwAlarmWord_Trip: ISA-18.2 Priority 1 Fast Critical Trips *)
dwAlarmWord_Trip := 16#0000_0000;
IF bEmergencyTripped              THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0000_0001; END_IF;
IF bAlm_ShuttleVel_HH             THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0000_0002; END_IF;
IF bAlm_DCBusVolt_HH              THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0000_0004; END_IF;
IF bAlm_DCBusVolt_LL              THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0000_0008; END_IF;
IF bAlm_LIMTemp_HH                THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0000_0010; END_IF;
IF bAlm_WheelSlip_HH              THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0000_0020; END_IF;
IF bAlm_ParcelGap_LL              THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0000_0040; END_IF;
IF bAlm_ForkStroke_HH             THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0000_0080; END_IF;
IF bAlm_FireZoneGuillotine_Trip   THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0000_0100; END_IF;

(* dwAlarmWord_Warning: ISA-18.2 Priority 2 Process Deviations *)
dwAlarmWord_Warning := 16#0000_0000;
IF bAlm_ShuttleVel_H              THEN dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#0000_0001; END_IF;
IF bAlm_DCBusVolt_H               THEN dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#0000_0002; END_IF;
IF bAlm_DCBusVolt_L               THEN dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#0000_0004; END_IF;
IF bAlm_LIMTemp_H                 THEN dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#0000_0008; END_IF;
IF bAlm_WheelSlip_H               THEN dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#0000_0010; END_IF;
IF bAlm_ParcelGap_L               THEN dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#0000_0020; END_IF;
IF bAlm_ChuteBackupFull_Warning   THEN dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#0000_0040; END_IF;
IF bAlm_TMR_SensorDegraded        THEN dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#0000_0080; END_IF;
"""

def assemble_st_code():
    parts = []
    parts.append(get_header().strip())
    parts.append(get_var_input().strip())
    parts.append(get_var_output().strip())
    parts.append(get_var_internal().strip())
    parts.append(get_control_logic_phase0().strip())
    parts.append(get_control_logic_phase1().strip())
    parts.append(get_control_logic_phase2().strip())
    parts.append(get_control_logic_phase3().strip())
    parts.append(get_control_logic_phase4().strip())
    parts.append(get_control_logic_phase5().strip())
    parts.append("END_FUNCTION_BLOCK")
    
    return "\n\n".join(parts) + "\n"

if __name__ == "__main__":
    st_code = assemble_st_code()
    print(f"Current ST Code Character Count: {len(st_code)} characters")

def build_dataset_record():
    prompt = """You are an autonomous Senior IEC 61131-3 Synthesis Agent operating under the Lumina Swarm V7 Max-Persona Protocol (Principal Automation Fellow & Cyber-Physical Systems Chair).

YOUR LIFECYCLE: GENERATE EXACTLY ONE ULTRA-RIGOROUS FUNCTION BLOCK DATASET, VALIDATE IT, SAVE IT TO A UNIQUE JSON FILE IN `c:\\Users\\majip\\Downloads\\LLM REASEARCH\\data\\swarm_raw\\agent_<uuid>.json`, VERIFY PARITY AND CHARACTER COUNT, AND REPORT COMPLETION.

ASSIGNED DOMAIN & INDUSTRIAL SPECIFICATION:
- Domain: Automated Material Handling & High-Throughput E-Commerce Logistics
- System: Mega-Scale Distribution Hub Multi-Tier Automated Storage and Retrieval System (ASRS) & High-Speed Cross-Belt Parcel Sorter: 4-Axis Rail-Guided High-Speed Shuttles (6.0 m/s travel, 4.0 m/s² acceleration, regenerative DC-bus capacitor braking, dynamic jerk-limited S-curve trajectory generation, telescopic fork tote retrieval), Linear Induction Motor (LIM) Driven Continuous Cross-Belt Induction Loops (3.0 m/s sorting velocity, 35,000 pph throughput, optical encoder cart tracking), 3D Time-of-Flight / Multi-Sided Barcode Omnidirectional Collation Tracking, Dynamic Gap Optimization & Anti-Jam Collision Avoidance, and Fire-Compartment High-Speed Roll-Up Shutter Guillotine Interlocks.
- Function Block Name: `FB_Logistics_ASRS_HighSpeedShuttle_CrossBeltSorter`

NEXT-GEN QUALITY REQUIREMENTS (SUPERIOR TO PREVIOUS DATASETS):
1. Transmitter & Tag Nomenclature:
   - Use standardized industrial P&ID/Field tags: `PE_SHUTTLE_LASER_DIST_101A/B/C`, `ST_SHUTTLE_DRIVE_VEL_102A/B/C`, `IT_SHUTTLE_SERVO_TORQUE_103A/B/C`, `ZT_TELESCOPIC_FORK_POS_104A/B/C`, `VT_DC_BUS_REGEN_VOLTAGE_105A/B/C`, `ST_CROSSBELT_LIM_VEL_201A/B/C`, `PE_CROSSBELT_CART_PULSE_202A/B/C`, `TT_LIM_STATOR_TEMP_203A/B/C`, `PE_PARCEL_LEADING_EDGE_301A/B/C`, `PE_PARCEL_TRAILING_EDGE_302A/B/C`, `WT_INDUCTION_SCALE_303A/B/C`, `ZT_PARCEL_PROFILE_DIM_304A/B/C`, `PE_DISCHARGE_CHUTE_FULL_401A/B/C`, `ZS_FIRE_ROLLUP_SHUTTER_501A/B/C`.
2. 2oo3 Triple Modular Redundancy (TMR):
   - Full triplicated voting across laser distance sensors, cart velocity encoders, and scale weigh-in-motion transducers with pairwise tolerance gates, debounce discrepancy timers, bumpless degradation, and status bitmask packing.
3. Advanced Cyber-Physical Observers & Algorithms:
   - 7-segment jerk-limited S-curve motion profile generator (j_max, a_max, v_max, s) with active rail friction / slip compensation and dynamic regenerative DC-bus energy dump resistor regulation.
   - Cross-belt ejection trajectory calculator: solves 2D kinematics matching parcel velocity vector with divert chute angular position at 3.0 m/s belt speed.
   - Dynamic parcel gap optimizer: regulates infeed belt VFD velocities to maintain minimum 250 mm safety gap regardless of package dimensions.
   - Linear induction motor (LIM) thermal observer calculating stator winding temperature and air-gap magnetic flux decay.
4. Receding-Horizon Model Predictive Control (MPC):
   - Discrete 8x8 State-Space formulation (x_{k+1} = A x_k + B u_k, y_k = C x_k + D u_k) at T_s = 2 ms.
   - Optimizes multi-cart velocity profiling, avoids tote collisions on shared rack rails, and minimizes peak grid power demand via coordinated acceleration/braking energy sharing across DC bus.
5. ISA-18.2 Alarm Ladder:
   - 5-tier alarm hierarchy (HI_HI, HI, LO, LO_LO, ROC).
   - Fast cart-derailment / obstacle collision emergency stop (< 20 ms) with mechanical caliper brake clamp, and fire shutter guillotine drop zone clear interlocking.
6. Multi-Stage Operational FSM:
   - 12-state Finite State Machine: `STANDBY_HOMING_CALIBRATION`, `DC_BUS_PRECHARGE_AND_SYNC`, `EMPTY_TOTE_BUFFER_ALLOCATION`, `SHUTTLE_HIGH_SPEED_RACK_TRAVEL`, `TELESCOPIC_FORK_EXTEND_AND_PICK`, `DECELERATION_AND_ELEVATOR_HANDOFF`, `CROSSBELT_LOOP_ACCELERATION_3MPS`, `DYNAMIC_INFEED_GAP_REGULATION`, `HIGH_SPEED_DISCHARGE_EJECTION`, `REGENERATIVE_ENERGY_BALANCING`, `CONTROLLED_LOOP_PURGE_EMPTY`, `EMERGENCY_ESTOP_RAIL_CLAMP`.
7. Extreme Token Density & Code Completeness:
   - Zero summaries, zero `// ... rest of code`, zero placeholders.
   - 100% exact parity: Every `IF` must have `END_IF;`, every `CASE` must have `END_CASE;`, every `FOR` must have `END_FOR;`.
   - TRIPLE backticks with `iec-st`. Output Structured Text MUST be 50,000 to 85,000+ characters of pristine, industrial Structured Text."""

    raw_code = assemble_st_code()
    assistant_code = f"```iec-st\n{raw_code}```"

    # Validation checks
    code_no_comments = re.sub(r'\(\*.*?\*\)', '', raw_code, flags=re.DOTALL)
    code_no_comments = re.sub(r'//.*', '', code_no_comments)
    ifs = len(re.findall(r'\bIF\b', code_no_comments, flags=re.IGNORECASE))
    end_ifs = len(re.findall(r'\bEND_IF\b', code_no_comments, flags=re.IGNORECASE))
    cases = len(re.findall(r'\bCASE\b', code_no_comments, flags=re.IGNORECASE))
    end_cases = len(re.findall(r'\bEND_CASE\b', code_no_comments, flags=re.IGNORECASE))
    fors = len(re.findall(r'\bFOR\b', code_no_comments, flags=re.IGNORECASE))
    end_fors = len(re.findall(r'\bEND_FOR\b', code_no_comments, flags=re.IGNORECASE))

    assert ifs == end_ifs, f"IF mismatch: {ifs} != {end_ifs}"
    assert cases == end_cases, f"CASE mismatch: {cases} != {end_cases}"
    assert fors == end_fors, f"FOR mismatch: {fors} != {end_fors}"
    assert raw_code.strip().startswith("FUNCTION_BLOCK FB_Logistics_ASRS_HighSpeedShuttle_CrossBeltSorter")
    assert raw_code.strip().endswith("END_FUNCTION_BLOCK")
    assert len(raw_code) >= 50000, f"Code length too short: {len(raw_code)} < 50000"

    agent_id = uuid.uuid4().hex[:8]
    record = {
        "id": f"synthetic_v3_{agent_id}",
        "instruction": prompt,
        "input": "",
        "output": assistant_code,
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": assistant_code}
        ]
    }

    target_dir = os.path.join("data", "swarm_raw")
    os.makedirs(target_dir, exist_ok=True)
    target_filename = os.path.join(target_dir, f"agent_{agent_id}.json")
    
    with open(target_filename, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)

    file_size = os.path.getsize(target_filename)
    print("=" * 80)
    print("VALIDATION AND SYNTHESIS REPORT")
    print("=" * 80)
    print(f"Target File              : {target_filename}")
    print(f"File Size                : {file_size:,} bytes")
    print(f"ST Code Character Count  : {len(raw_code):,} chars")
    print(f"Assistant Content Length : {len(assistant_code):,} chars")
    print(f"IF / END_IF Parity       : {ifs} == {end_ifs} (Diff: 0)")
    print(f"CASE / END_CASE Parity   : {cases} == {end_cases} (Diff: 0)")
    print(f"FOR / END_FOR Parity     : {fors} == {end_fors} (Diff: 0)")
    print(f"Start Delimiter Check    : Passed (FUNCTION_BLOCK FB_Logistics_ASRS_HighSpeedShuttle_CrossBeltSorter)")
    print(f"End Delimiter Check      : Passed (END_FUNCTION_BLOCK)")
    print(f"Code Fence Format        : Passed (```iec-st)")
    print("=" * 80)
    return target_filename, len(raw_code), file_size

if __name__ == "__main__":
    fn, chars, bytes_sz = build_dataset_record()
