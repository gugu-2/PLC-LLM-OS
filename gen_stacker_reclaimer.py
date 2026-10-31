# Python script to generate FB_Mining_StackerReclaimer_8000TPH_SlewLuff
import json
import os
import re
import sys

def build_iec_code():
    parts = []
    
    # 1. Opening Header & Cyber-Physical System Specification
    parts.append("""FUNCTION_BLOCK FB_Mining_StackerReclaimer_8000TPH_SlewLuff
(*
====================================================================================================
CYBER-PHYSICAL SYSTEM ARCHITECTURE SPECIFICATION:
PROJECT: LUMINA AUTOMATION HEAVY BULK MATERIALS HANDLING & STOCKYARD ROBOTICS
SYSTEM:  8,000 TPH DUAL-BOOM BUCKET-WHEEL STACKER-RECLAIMER WITH DYNAMIC SLEW
         ANTI-COLLISION, LUFFING HYDRAULIC LEVELING & CONTINUOUS BELT WEIGHER
MACHINE SPECIFICATIONS:
  - Stacking Throughput Capacity: 8,000 metric tons/hour (iron ore bulk density: 2.2 - 2.8 t/m3)
  - Reclaiming Throughput Capacity: 6,000 metric tons/hour
  - Main Boom Operating Length: 55.0 m (pivot center to bucket wheel center)
  - Counterweight Boom Length: 38.0 m (with 320-ton ballast box)
  - Bucket Wheel Geometry: 10.5 m outer diameter, 9 cell-less manganese alloy buckets (1.4 m3 each)
  - Bucket Wheel Electric Drive: 800 kW vector-controlled VFD motor with bevel-helical planetary reducer
  - Slew Superstructure Drive: 4x 75 kW synchronized AC induction planetary pinion drives engaging
    internal spur ring gear (m = 24 mm, z = 320, pitch diameter 7.68 m) with hydraulic multi-disc slip clutches
  - Dynamic Slewing Speed Range: 0.05 to 0.35 RPM with automated cosine speed pacing
  - Hydraulic Luffing System: Twin double-acting heavy-duty cylinders (bore 480 mm, rod 280 mm, stroke 4,200 mm)
    supporting 450-ton boom structure across -15.0 deg (trench reclaim) to +18.0 deg (high crest stack)
  - Hydraulic Power Unit: 4x 110 kW variable displacement axial piston pumps with proportional counterbalance
    valves and dynamic pressure equalization
  - Multi-Sensor 3D Stockyard LiDAR Profiling: Dual boom-tip rotating pulsed time-of-flight LiDAR scanners
    mapping stockpile surface contours, detecting crest encroachment, and calculating 3D safety clearance
  - In-Line Continuous Belt Scale: Dual-idler dynamic weigher with high-speed load cell array,
    optical belt speed tachometer, digital FIR/Butterworth low-pass filtering, and auto-tare tracking
  - Gantry Rail Travel Drive: 8 four-wheel articulated bogies (32 driven wheels total), rail gauge 12.0 m,
    active skew compensation via left/right laser distance sensors preventing crab binding
  - Receding-Horizon Model Predictive Control (MPC): 16-state, 8-input discrete state-space formulation
    jointly pacing slew angular speed, bucket wheel penetration depth, and luffing elevation angle
  - Triple Modular Redundancy (TMR): 2oo3 voting across slew absolute encoders, luffing stroke transducers,
    belt weigher load cells, and bucket wheel torque transducers with bumpless degradation
  - Finite State Machine: 12-stage automated operation from rail travel alignment to emergency SIL-3 brake dump
  - ISA-18.2 Alarm Management: Bit-packed telemetry DWORDs, multi-tiered trip escalation, and deadband hysteresis

MATHEMATICAL FOUNDATIONS & GOVERNING CYBER-PHYSICAL EQUATIONS:
  1. Boom Structural Mechanics & Torsional/Flexural Dynamics (Euler-Bernoulli):
     J_slew * d2(theta_slew)/dt2 + d_slew * d(theta_slew)/dt + k_tors * (theta_slew - theta_tip) = tau_slew
     m_boom * d2(y_lat)/dt2 + c_lat * d(y_lat)/dt + k_lat * y_lat = F_cut_lat(t) - F_inertial_lat(t)
     m_boom * d2(z_vert)/dt2 + c_vert * d(z_vert)/dt + k_vert * z_vert = F_luff_cyl(t) - m_boom * g - F_cut_vert(t)

  2. Dual-Cylinder Hydraulic Luffing Fluid Dynamics with Oil Bulk Modulus:
     dP_cap/dt = (Beta_oil / V_cap(x_cyl)) * (Q_in_cap - A_cap * dx_cyl/dt - Q_leak_internal)
     dP_rod/dt = (Beta_oil / V_rod(x_cyl)) * (-Q_out_rod + A_rod * dx_cyl/dt + Q_leak_internal)
     F_hyd_net = P_cap * A_cap - P_rod * A_rod - F_friction(dx_cyl/dt)
     Torque_luff = F_hyd_net * L_cylinder_moment_arm(alpha_luff) - m_boom_total * g * L_cg * cos(alpha_luff)

  3. Cosine Slew Velocity Compensation for Constant Volumetric Reclaim Slice:
     Volumetric cut rate: V_dot(t) = S_slice * v_slew_linear(theta) = S_slice * (omega_slew * L_boom)
     For a rectilinear bench face at azimuth angle theta relative to bench normal theta_0:
     Effective slice depth: d_eff(theta) = d_nominal * cos(theta - theta_0)
     To maintain constant instantaneous tonnage throughput:
     omega_slew(theta) = omega_slew_nominal / max(cos(theta - theta_0), 0.25)

  4. Bucket Wheel Specific Cutting Energy & Resistance Torque:
     F_cut_tangential = k_spec_ore * A_chip_cross_section(theta_cut, h_bench)
     tau_cut_resistance = F_cut_tangential * R_bucket_wheel
     P_electric_wheel = (tau_cut_resistance * omega_wheel) / eta_gearbox + P_lifting_material

  5. Dynamic Dual-Idler Continuous Belt Weigher Integration:
     Linear material loading: q_belt(t) = (F_LC1(t) + F_LC2(t) - F_tare) / (g * L_idler_pitch * cos(alpha_luff))
     Instantaneous mass flow rate: m_dot(t) = 3.6 * q_belt(t) * v_belt(t)  [metric t/h]
     Cumulative total tonnage: M_total(t) = M_total(t-1) + (m_dot(t) * Delta_t / 3600.0)  [metric tonnes]

  6. Rail Travel Gantry Active Skew Dynamics:
     Skew displacement: Delta_s_skew(t) = s_rail_left(t) - s_rail_right(t)
     Active anti-crabbing yaw correction moment:
     M_skew_correct = K_p_skew * Delta_s_skew + K_i_skew * Integral(Delta_s_skew dt) + K_d_skew * d(Delta_s_skew)/dt
     Biased motor drive torque commands:
     tau_bog_left = tau_travel_nom - 0.5 * (M_skew_correct / R_wheel)
     tau_bog_right = tau_travel_nom + 0.5 * (M_skew_correct / R_wheel)

  7. Discrete State-Space Cyber-Physical System Formulation:
     x[k+1] = A * x[k] + B * u[k] + E * d[k]
     y[k]   = C * x[k] + D * u[k]
     State vector (16x1):
       x1:  Boom slew azimuth angle [rad]
       x2:  Boom slew angular velocity [rad/s]
       x3:  Boom structural torsional deflection [rad]
       x4:  Boom structural lateral flexural bending deflection [m]
       x5:  Boom structural lateral bending velocity [m/s]
       x6:  Boom luffing elevation angle [rad]
       x7:  Boom luffing angular velocity [rad/s]
       x8:  Luffing cylinder cap chamber pressure [bar]
       x9:  Luffing cylinder rod chamber pressure [bar]
       x10: Boom vertical flexural deflection [m]
       x11: Bucket wheel rotational speed [rad/s]
       x12: Bucket wheel cutting resistance torque disturbance [kN m]
       x13: Gantry longitudinal rail position [m]
       x14: Gantry rail travel velocity [m/s]
       x15: Gantry skew misalignment error [mm]
       x16: Boom conveyor linear material loading [kg/m]
     Control vector (8x1):
       u1: Slew drive torque command [kN m]
       u2: Hydraulic luffing proportional valve flow command [L/min]
       u3: Bucket wheel motor torque command [kN m]
       u4: Gantry left bogie drive torque command [kN m]
       u5: Gantry right bogie drive torque command [kN m]
       u6: Boom conveyor belt speed reference [m/s]
       u7: Counterbalance valve dynamic pressure bias command [bar]
       u8: Rail skew active steering trim moment [kN m]
====================================================================================================
*)
""")

    # 2. VAR_INPUT
    parts.append("""VAR_INPUT
    (* ========================================================================= *)
    (* 1. SLEW SUPERSTRUCTURE BEARING ABSOLUTE ENCODERS (2oo3 TMR ARCHITECTURE) *)
    (* ========================================================================= *)
    rSlew_Angle_Sens1_deg           : REAL;     (* [deg] Slew Bearing Absolute Optical Multi-Turn Encoder Ch A (2oo3 TMR) *)
    rSlew_Angle_Sens2_deg           : REAL;     (* [deg] Slew Bearing Absolute Optical Multi-Turn Encoder Ch B (2oo3 TMR) *)
    rSlew_Angle_Sens3_deg           : REAL;     (* [deg] Slew Bearing Absolute Optical Multi-Turn Encoder Ch C (2oo3 TMR) *)
    rSlew_Velocity_Meas_rpm         : REAL;     (* [rpm] Slew Pinion Vector Inverter Resolver Angular Velocity Feedback *)

    (* ========================================================================= *)
    (* 2. HYDRAULIC LUFFING SYSTEM TRANSDUCERS & DUAL-AXIS INCLINOMETERS (2oo3)  *)
    (* ========================================================================= *)
    rLuff_Stroke_Cyl1_Sens1_mm      : REAL;     (* [mm] Left Luffing Cylinder Magnetostrictive Stroke Transducer Ch 1 (2oo3) *)
    rLuff_Stroke_Cyl1_Sens2_mm      : REAL;     (* [mm] Left Luffing Cylinder Magnetostrictive Stroke Transducer Ch 2 (2oo3) *)
    rLuff_Stroke_Cyl1_Sens3_mm      : REAL;     (* [mm] Left Luffing Cylinder Magnetostrictive Stroke Transducer Ch 3 (2oo3) *)
    rLuff_Stroke_Cyl2_mm            : REAL;     (* [mm] Right Luffing Cylinder Magnetostrictive Stroke Transducer Feedback *)
    rLuff_Pressure_Cap_bar          : REAL;     (* [bar] Twin Luffing Cylinder Cap (Piston Full Bore) Operating Pressure *)
    rLuff_Pressure_Rod_bar          : REAL;     (* [bar] Twin Luffing Cylinder Rod (Annular) Operating Pressure *)
    rLuff_Pressure_Pump_bar         : REAL;     (* [bar] Hydraulic Power Unit Main Supply Rail Pressure *)
    rLuff_Boom_Inclinometer_deg     : REAL;     (* [deg] Boom Primary Precision Dual-Axis Inclinometer Angle Ground Datum *)

    (* ========================================================================= *)
    (* 3. 800 KW BUCKET WHEEL DRIVE TRANSDUCTOR SENSORS (2oo3 TMR ARCHITECTURE)  *)
    (* ========================================================================= *)
    rBW_Motor_Torque_Sens1_kNm      : REAL;     (* [kN m] Bucket Wheel Electric Motor Shaft Torque Transducer Ch A (2oo3) *)
    rBW_Motor_Torque_Sens2_kNm      : REAL;     (* [kN m] Bucket Wheel Electric Motor Shaft Torque Transducer Ch B (2oo3) *)
    rBW_Motor_Torque_Sens3_kNm      : REAL;     (* [kN m] Bucket Wheel Electric Motor Shaft Torque Transducer Ch C (2oo3) *)
    rBW_Motor_Speed_rpm             : REAL;     (* [rpm] Bucket Wheel VFD Inverter Motor Output Shaft Velocity *)
    rBW_Motor_Power_kW              : REAL;     (* [kW] Bucket Wheel Electric Drive Active Power Consumption *)
    rBW_Motor_Current_A             : REAL;     (* [A] Bucket Wheel Stator RMS Phase Current *)

    (* ========================================================================= *)
    (* 4. CONTINUOUS DUAL-IDLER DYNAMIC BELT WEIGHER (2oo3 TMR ARCHITECTURE)     *)
    (* ========================================================================= *)
    rBelt_Load_Cell1_kN             : REAL;     (* [kN] Dual-Idler Belt Weigher Hermetic Stainless Load Cell Ch 1 (2oo3) *)
    rBelt_Load_Cell2_kN             : REAL;     (* [kN] Dual-Idler Belt Weigher Hermetic Stainless Load Cell Ch 2 (2oo3) *)
    rBelt_Load_Cell3_kN             : REAL;     (* [kN] Dual-Idler Belt Weigher Hermetic Stainless Load Cell Ch 3 (2oo3) *)
    rBelt_Speed_Encoder_mps         : REAL;     (* [m/s] Tri-Boom Conveyor High-Precision Digital Pulse Belt Speed Tachometer *)

    (* ========================================================================= *)
    (* 5. RAIL TRAVEL GANTRY DRIVE & ACTIVE SKEW DISTANCE TRANSDUCERS            *)
    (* ========================================================================= *)
    rRail_Gantry_Pos_Left_m         : REAL;     (* [m] Gantry Left Rail Long-Travel Laser Distance Telemetry *)
    rRail_Gantry_Pos_Right_m        : REAL;     (* [m] Gantry Right Rail Long-Travel Laser Distance Telemetry *)
    rRail_Gantry_Speed_mps          : REAL;     (* [m/s] Gantry Wheel Bogie Tachometer Travel Speed *)
    rRail_Flange_Proximity_Left_mm  : REAL;     (* [mm] Left Rail Flange Inductive Clearance Sensor *)
    rRail_Flange_Proximity_Right_mm : REAL;     (* [mm] Right Rail Flange Inductive Clearance Sensor *)

    (* ========================================================================= *)
    (* 6. BOOM-TIP ROTATING 3D LIDAR SURFACE MAPPING & ANTI-COLLISION TELEMETRY  *)
    (* ========================================================================= *)
    rLiDAR1_Distance_m              : REAL;     (* [m] Boom Tip 3D Rotating LiDAR Scanner 1 Beam Range Telemetry *)
    rLiDAR1_Azimuth_deg             : REAL;     (* [deg] Boom Tip 3D Rotating LiDAR Scanner 1 Beam Azimuth Angle *)
    rLiDAR1_Elevation_deg           : REAL;     (* [deg] Boom Tip 3D Rotating LiDAR Scanner 1 Beam Elevation Angle *)
    rLiDAR2_Distance_m              : REAL;     (* [m] Boom Tip 3D Rotating LiDAR Scanner 2 Beam Range Telemetry *)
    rLiDAR2_Azimuth_deg             : REAL;     (* [deg] Boom Tip 3D Rotating LiDAR Scanner 2 Beam Azimuth Angle *)
    rLiDAR2_Elevation_deg           : REAL;     (* [deg] Boom Tip 3D Rotating LiDAR Scanner 2 Beam Elevation Angle *)

    (* ========================================================================= *)
    (* 7. STOCKYARD OPERATIONAL TARGETS, BENCH GEOMETRY & EXECUTION COMMANDS     *)
    (* ========================================================================= *)
    rTarget_Throughput_TPH          : REAL;     (* [t/h] Production Target Material Reclaim/Stack Mass Flow Rate (Nominal 6,000 / 8,000 t/h) *)
    rBench_Cut_Depth_Setpt_m        : REAL;     (* [m] Automated Reclaiming Slicing Depth Setpoint (Nominal 0.5m to 2.2m) *)
    rSlew_Sector_Min_deg            : REAL;     (* [deg] Reclaiming Bench Slew Left Travel Boundary Limit *)
    rSlew_Sector_Max_deg            : REAL;     (* [deg] Reclaiming Bench Slew Right Travel Boundary Limit *)
    rLuff_Angle_Setpt_deg           : REAL;     (* [deg] Boom Hydraulic Luffing Angle Target Command (-15.0 deg to +18.0 deg) *)
    rDelta_T_ms                     : REAL := 10.0; (* [ms] Controller Fast Deterministic Real-Time Scan Cycle Interval (10 ms) *)

    (* ========================================================================= *)
    (* 8. DISCRETE OPERATIONAL & SAFETY PERMISSIVE INTERLOCK SIGNALS             *)
    (* ========================================================================= *)
    bMaster_Enable_Cmd              : BOOL;     (* Operator Supervisory Master Run Enable Permissive *)
    bAuto_Reclaim_Start_Cmd         : BOOL;     (* Automated Bench Reclaiming Execution Start Command *)
    bAuto_Stack_Start_Cmd           : BOOL;     (* Automated Chevron/Windrow Stacking Execution Start Command *)
    bEmergency_Stop_PB              : BOOL;     (* Dual-Channel Hardwired Emergency Stop Pushbutton Contact *)
    bFault_Reset_PB                 : BOOL;     (* Manual Safety Trip Reset & Diagnostic Latched Error Clear *)
    bRail_Clamps_Engaged_FB         : BOOL;     (* Hydraulic Rail Storm Clamps Engaged Feedback *)
    bSlew_Storm_Pin_Engaged_FB      : BOOL;     (* High-Tonnage Mechanical Slew Locking Pin Feedback *)
    bBelt_Rip_Detector_OK           : BOOL;     (* Continuous Ultrasonic Boom Belt Rip Detection Sensor Healthy *)
    bChute_Plugged_Sensor_OK        : BOOL;     (* Discharge Transfer Chute Nuclear/Microwave Non-Plugged Permissive *)
END_VAR
""")

    # 3. VAR_OUTPUT
    parts.append("""VAR_OUTPUT
    (* ========================================================================= *)
    (* 1. SLEW & HYDRAULIC LUFFING ACTUATOR MULTI-DRIVE CONTROL COMMANDS        *)
    (* ========================================================================= *)
    rSlew_Torque_Cmd_kNm            : REAL;     (* [kN m] Total Slew Dynamic Torque Vector Command Distributed to 4 Planetary Drives *)
    rSlew_Speed_Cmd_rpm             : REAL;     (* [rpm] Vector Inverter Slew Velocity Reference with Cosine Compensation *)
    rLuff_Prop_Flow_Cmd_Lmin        : REAL;     (* [L/min] Twin Luffing Cylinder Proportional Valve Volumetric Flow Command *)
    rLuff_Angle_Cmd_deg             : REAL;     (* [deg] Boom Hydraulic Luffing Angle Closed-Loop Actuator Setpoint *)
    rCounterbalance_Valve_Bias_bar  : REAL;     (* [bar] Twin Luffing Cylinder Dynamic Pressure Equalization Bias Command *)

    (* ========================================================================= *)
    (* 2. BUCKET WHEEL, GANTRY BOGIES & BOOM CONVEYOR ACTUATION OUTPUTS          *)
    (* ========================================================================= *)
    rBW_VFD_Torque_Limit_kNm        : REAL;     (* [kN m] Bucket Wheel 800 kW VFD Drive Dynamic Stall Torque Limit *)
    rBW_VFD_Speed_Cmd_rpm           : REAL;     (* [rpm] Bucket Wheel VFD Inverter Speed Target (5.0 to 9.5 RPM) *)
    rGantry_Speed_Cmd_Left_mps      : REAL;     (* [m/s] Gantry Left Rail 16-Wheel Bogie Group Travel Velocity Reference *)
    rGantry_Speed_Cmd_Right_mps     : REAL;     (* [m/s] Gantry Right Rail 16-Wheel Bogie Group Travel Velocity Reference *)
    rBoom_Conveyor_Speed_Cmd_mps    : REAL;     (* [m/s] 2000 mm Boom Conveyor Belt Drive Speed Setpoint *)

    (* ========================================================================= *)
    (* 3. PROCESS, STOCKYARD TELEMETRY & STRUCTURAL MONITORING METRICS           *)
    (* ========================================================================= *)
    rInstantaneous_Throughput_TPH   : REAL;     (* [t/h] Continuous Dynamically Compensated Mass Flow Rate *)
    rCumulative_Tonnage_Tonnes      : REAL;     (* [t] Total Cumulative Material Shift Production Totalizer *)
    rCosine_Compensation_Factor     : REAL;     (* Dimensionless Cosine Slew Volume Pacing Multiplier *)
    rLiDAR_Min_Clearance_m          : REAL;     (* [m] Minimum Distance to Stockpile Crest, Toe, or Yard Obstruction *)
    rRail_Skew_Error_mm             : REAL;     (* [mm] Real-Time Longitudinal Gantry Skew Misalignment Error *)
    rBoom_Tip_Deflection_Lat_mm     : REAL;     (* [mm] Estimated Dynamic Boom Lateral Flexural Deflection *)
    rBoom_Tip_Deflection_Vert_mm    : REAL;     (* [mm] Estimated Dynamic Boom Vertical Flexural Deflection *)
    rBucket_Cutting_Depth_Actual_m  : REAL;     (* [m] Estimated Active Bench Slice Penetration Depth *)
    rLuff_Cylinder_Differential_Press_bar: REAL;(* [bar] Net Effective Hydraulic Lifting Force Differential Pressure *)

    (* ========================================================================= *)
    (* 4. OPERATIONAL STATUS, INTERLOCKS & SAFETY DISCRETE SIGNALS               *)
    (* ========================================================================= *)
    bSlew_In_Position               : BOOL;     (* Boom Azimuth Angle Within Target Bench Boundary Window *)
    bLuff_Target_Reached            : BOOL;     (* Boom Elevation Angle Within Closed-Loop Positioning Tolerance *)
    bBench_Slice_Completed          : BOOL;     (* Active Horizontal Bench Slew Sweep Completed *)
    bReclaim_Cycle_Active           : BOOL;     (* Automated Bucket Wheel Reclaiming Cycle Currently Sweeping *)
    bStack_Cycle_Active             : BOOL;     (* Automated Chevron/Windrow Stacking Sequence Active *)
    bAnti_Collision_Trip            : BOOL;     (* Stockpile Encroachment or Yard Infrastructure Clearance Envelope Breach *)
    bSIL3_Emergency_Brake_Tripped   : BOOL;     (* Fail-Safe Hydraulic & Rail Storm Brake Dump De-Energized *)
    iFSM_Current_State              : INT;      (* Active 12-Stage Finite State Machine Operational Stage Index (1..12) *)

    (* ========================================================================= *)
    (* 5. STATUS, WARNING & TRIP DIAGNOSTIC BITFIELDS                            *)
    (* ========================================================================= *)
    wStatus_Word                    : WORD;     (* 16-Bit Packed Stacker-Reclaimer Operating Status Word *)
    dwAlarm_Warnings                : DWORD;    (* 32-Bit Packed ISA-18.2 Process & Sensor Degradation Warnings *)
    dwAlarm_Critical_Trips          : DWORD;    (* 32-Bit Packed ISA-18.2 Safety-Critical Hardware Lockout Trips *)
END_VAR
""")

    # 4. VAR - System Constants, State-Space Matrices, MPC Weights, TMR variables, etc.
    parts.append("""VAR
    (* ========================================================================= *)
    (* CYBER-PHYSICAL CONSTANTS & FIXED MACHINE MECHANICAL PROPERTIES            *)
    (* ========================================================================= *)
    L_BOOM_LENGTH_M                 : REAL := 55.0;         (* [m] Main Boom Pivot Pin to Bucket Wheel Center *)
    R_BUCKET_WHEEL_M                : REAL := 5.250;        (* [m] Bucket Wheel Radius (10.5 m Diameter) *)
    M_BOOM_TOTAL_TONNES             : REAL := 450.0;        (* [t] Total Structural Mass of Boom Assembly *)
    M_COUNTERWEIGHT_TONNES          : REAL := 320.0;        (* [t] Total Mass of Counterweight Structure *)
    A_CYL_CAP_M2                    : REAL := 0.180956;     (* [m2] Cap Bore Area for 480 mm Bore Cylinder *)
    A_CYL_ROD_M2                    : REAL := 0.119381;     (* [m2] Annular Rod Area for 280 mm Rod Diameter *)
    BETA_OIL_BULK_MODULUS_BAR       : REAL := 16000.0;      (* [bar] Hydraulic Fluid Effective Bulk Modulus *)
    K_SPECIFIC_CUTTING_ORE_KPA      : REAL := 285.0;        (* [kPa] Specific Iron Ore Cutting Resistance *)
    IDLER_SPACING_M                 : REAL := 1.250;        (* [m] Dual-Idler Belt Weigher Idler Spacing *)
    GRAVITY_ACCEL_MPS2              : REAL := 9.80665;      (* [m/s2] Standard Acceleration of Gravity *)
    PI_CONST                        : REAL := 3.141592653589793;
    TWO_PI                          : REAL := 6.283185307179586;
    RAD_TO_DEG                      : REAL := 57.29577951308232;
    DEG_TO_RAD                      : REAL := 0.017453292519943;

    (* ========================================================================= *)
    (* 16x16 DISCRETE STATE-SPACE SYSTEM MATRICES (Delta_T = 10 ms)             *)
    (* x = [theta_slew, omega_slew, phi_tors, y_lat, dy_lat,                     *)
    (*      alpha_luff, omega_luff, P_cap, P_rod, z_vert,                        *)
    (*      omega_bw, tau_cut, s_gantry, v_gantry, delta_skew, q_belt]^T         *)
    (* ========================================================================= *)
""")

    # 16x16 A Matrix
    parts.append("    aMatrix_A_Sys                   : ARRAY[1..16, 1..16] OF REAL := [\n")
    a_rows = [
        [1.0000, 0.0100, 0.0005, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
        [0.0000, 0.9850, 0.0420, 0.0015, 0.0002, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000,-0.0035, 0.0000, 0.0000, 0.0000, 0.0000],
        [0.0000,-0.0085, 0.9650, 0.0025, 0.0004, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000,-0.0082, 0.0000, 0.0000, 0.0000, 0.0000],
        [0.0000, 0.0000, 0.0000, 0.9995, 0.0098, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000,-0.0012, 0.0000, 0.0000, 0.0000, 0.0000],
        [0.0000, 0.0012, 0.0020,-0.1250, 0.9780, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000,-0.0150, 0.0000, 0.0000, 0.0000, 0.0000],
        [0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 1.0000, 0.0100, 0.0008,-0.0005, 0.0001, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000,-0.0002],
        [0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.9820, 0.0145,-0.0095, 0.0035, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000,-0.0045],
        [0.0000, 0.0000, 0.0000, 0.0000, 0.0000,-0.0012,-0.2850, 0.9750, 0.0050, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
        [0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0008, 0.1950, 0.0045, 0.9800, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
        [0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0025, 0.0000, 0.0015,-0.0010, 0.9950, 0.0000,-0.0005, 0.0000, 0.0000, 0.0000,-0.0018],
        [0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.9650,-0.0450, 0.0000, 0.0000, 0.0000, 0.0000],
        [0.0000, 0.0085, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0250, 0.9200, 0.0000, 0.0000, 0.0000, 0.0000],
        [0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 1.0000, 0.0100, 0.0000, 0.0000],
        [0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.9750,-0.0015, 0.0000],
        [0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0085, 0.9850, 0.0000],
        [0.0000, 0.0025, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0350, 0.0150, 0.0000, 0.0000, 0.0000, 0.9450]
    ]
    for r_idx, r in enumerate(a_rows):
        line = "        " + ", ".join(f"{val:7.4f}" for val in r)
        if r_idx < 15:
            line += ",\n"
        else:
            line += "\n    ];\n"
        parts.append(line)

    # 16x8 B Matrix
    parts.append("\n    (* 16x8 Input Actuator Coupling Matrix B *)\n")
    parts.append("    aMatrix_B_Sys                   : ARRAY[1..16, 1..8] OF REAL := [\n")
    b_rows = [
        [ 0.0005,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000],
        [ 0.0245,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000],
        [ 0.0120,  0.0000, -0.0045,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000],
        [ 0.0008,  0.0000, -0.0015,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000],
        [ 0.0185,  0.0000, -0.0125,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000],
        [ 0.0000,  0.0015,  0.0000,  0.0000,  0.0000,  0.0000,  0.0002,  0.0000],
        [ 0.0000,  0.0480,  0.0000,  0.0000,  0.0000,  0.0000,  0.0065,  0.0000],
        [ 0.0000,  0.3850,  0.0000,  0.0000,  0.0000,  0.0000,  0.0450,  0.0000],
        [ 0.0000, -0.2650,  0.0000,  0.0000,  0.0000,  0.0000, -0.0380,  0.0000],
        [ 0.0000,  0.0035,  0.0000,  0.0000,  0.0000,  0.0000,  0.0008,  0.0000],
        [ 0.0000,  0.0000,  0.0850,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000],
        [ 0.0000,  0.0000,  0.0320,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000],
        [ 0.0000,  0.0000,  0.0000,  0.0005,  0.0005,  0.0000,  0.0000,  0.0000],
        [ 0.0000,  0.0000,  0.0000,  0.0165,  0.0165,  0.0000,  0.0000,  0.0000],
        [ 0.0000,  0.0000,  0.0000,  0.0125, -0.0125,  0.0000,  0.0000, -0.0245],
        [ 0.0000,  0.0000,  0.0140,  0.0000,  0.0000, -0.0480,  0.0000,  0.0000]
    ]
    for r_idx, r in enumerate(b_rows):
        line = "        " + ", ".join(f"{val:7.4f}" for val in r)
        if r_idx < 15:
            line += ",\n"
        else:
            line += "\n    ];\n"
        parts.append(line)

    # 16x16 C Matrix (Identity measurement matrix)
    parts.append("\n    (* 16x16 State Measurement Output Matrix C *)\n")
    parts.append("    aMatrix_C_Sys                   : ARRAY[1..16, 1..16] OF REAL := [\n")
    for r_idx in range(16):
        row = [1.0 if c_idx == r_idx else 0.0 for c_idx in range(16)]
        line = "        " + ", ".join(f"{val:6.4f}" for val in row)
        if r_idx < 15:
            line += ",\n"
        else:
            line += "\n    ];\n"
        parts.append(line)

    # 16x8 D Matrix (Zeros)
    parts.append("\n    (* 16x8 Direct Feedthrough Matrix D *)\n")
    parts.append("    aMatrix_D_Sys                   : ARRAY[1..16, 1..8] OF REAL := [\n")
    for r_idx in range(16):
        row = [0.0] * 8
        line = "        " + ", ".join(f"{val:6.4f}" for val in row)
        if r_idx < 15:
            line += ",\n"
        else:
            line += "\n    ];\n"
        parts.append(line)

    # 16x16 Q MPC Matrix
    parts.append("\n    (* 16x16 MPC State-Penalty Diagonal Weighting Matrix Q *)\n")
    parts.append("    aMatrix_Q_Weight                : ARRAY[1..16, 1..16] OF REAL := [\n")
    q_diag = [350.0, 120.0, 500.0, 850.0, 250.0, 600.0, 150.0, 45.0, 45.0, 400.0, 220.0, 180.0, 80.0, 140.0, 950.0, 450.0]
    for r_idx in range(16):
        row = [q_diag[r_idx] if c_idx == r_idx else 0.0 for c_idx in range(16)]
        line = "        " + ", ".join(f"{val:7.2f}" for val in row)
        if r_idx < 15:
            line += ",\n"
        else:
            line += "\n    ];\n"
        parts.append(line)

    # 8x8 R MPC Matrix
    parts.append("\n    (* 8x8 MPC Actuator-Penalty Diagonal Weighting Matrix R *)\n")
    parts.append("    aMatrix_R_Weight                : ARRAY[1..8, 1..8] OF REAL := [\n")
    r_diag = [18.5, 12.0, 25.0, 15.0, 15.0, 8.0, 6.5, 32.0]
    for r_idx in range(8):
        row = [r_diag[r_idx] if c_idx == r_idx else 0.0 for c_idx in range(8)]
        line = "        " + ", ".join(f"{val:6.2f}" for val in row)
        if r_idx < 7:
            line += ",\n"
        else:
            line += "\n    ];\n"
        parts.append(line)

    # 8x16 K_MPC Gain Matrix
    parts.append("\n    (* 8x16 Discrete Receding-Horizon Steady-State LQR/MPC Gain Matrix K_mpc *)\n")
    parts.append("    aMatrix_K_MPC_Gain              : ARRAY[1..8, 1..16] OF REAL := [\n")
    k_rows = [
        [ 2.450,  0.850, -0.145, -0.320, -0.085,  0.000,  0.000,  0.000,  0.000,  0.000,  0.000, -0.045,  0.000,  0.000,  0.000, -0.012],
        [ 0.000,  0.000,  0.000,  0.000,  0.000,  3.250,  1.120, -0.085,  0.065, -0.145,  0.000,  0.000,  0.000,  0.000,  0.000, -0.035],
        [ 0.000, -0.025, -0.055,  0.000,  0.000,  0.000,  0.000,  0.000,  0.000,  0.000,  1.850,  0.640,  0.000,  0.000,  0.000,  0.180],
        [ 0.000,  0.000,  0.000,  0.000,  0.000,  0.000,  0.000,  0.000,  0.000,  0.000,  0.000,  0.000,  0.850,  0.420, -0.680,  0.000],
        [ 0.000,  0.000,  0.000,  0.000,  0.000,  0.000,  0.000,  0.000,  0.000,  0.000,  0.000,  0.000,  0.850,  0.420,  0.680,  0.000],
        [ 0.000,  0.000,  0.000,  0.000,  0.000,  0.000,  0.000,  0.000,  0.000,  0.000,  0.045,  0.000,  0.000,  0.000,  0.000,  1.250],
        [ 0.000,  0.000,  0.000,  0.000,  0.000,  0.150,  0.085,  0.420, -0.380,  0.000,  0.000,  0.000,  0.000,  0.000,  0.000,  0.000],
        [ 0.000,  0.000,  0.000,  0.000,  0.000,  0.000,  0.000,  0.000,  0.000,  0.000,  0.000,  0.000,  0.000,  0.015,  2.850,  0.000]
    ]
    for r_idx, r in enumerate(k_rows):
        line = "        " + ", ".join(f"{val:7.3f}" for val in r)
        if r_idx < 7:
            line += ",\n"
        else:
            line += "\n    ];\n"
        parts.append(line)

    # 16x16 L_OBS Kalman Observer Matrix
    parts.append("\n    (* 16x16 Kalman / Luenberger State Observer Feedback Gain Matrix L_obs *)\n")
    parts.append("    aMatrix_L_Obs_Gain              : ARRAY[1..16, 1..16] OF REAL := [\n")
    l_diag = [0.28, 0.32, 0.15, 0.18, 0.22, 0.35, 0.30, 0.25, 0.25, 0.16, 0.40, 0.28, 0.25, 0.30, 0.45, 0.38]
    for r_idx in range(16):
        row = [l_diag[r_idx] if c_idx == r_idx else (0.015 if abs(c_idx - r_idx) == 1 else 0.0) for c_idx in range(16)]
        line = "        " + ", ".join(f"{val:6.3f}" for val in row)
        if r_idx < 15:
            line += ",\n"
        else:
            line += "\n    ];\n"
        parts.append(line)

    # Internal state vectors & TMR structures & timers
    parts.append("""
    (* Internal State Vectors & Estimator Variables *)
    aState_x_est                    : ARRAY[1..16] OF REAL;     (* Current Filtered / Estimated State Vector *)
    aState_x_pred                   : ARRAY[1..16] OF REAL;     (* 1-Step Ahead State Prediction Vector *)
    aState_x_ref                    : ARRAY[1..16] OF REAL;     (* Target State Trajectory Reference Vector *)
    aControl_u                      : ARRAY[1..8] OF REAL;      (* Optimal Computed Control Actuation Vector *)
    aControl_u_prev                 : ARRAY[1..8] OF REAL;      (* Previous Actuation Vector for Slew Limiting *)
    aObserver_Residual              : ARRAY[1..16] OF REAL;     (* Innovation Measurement Residual Vector *)
    aMeasurement_y                  : ARRAY[1..16] OF REAL;     (* Synthesized Physical Sensor Measurement Vector *)

    (* MPC Quadratic Optimization Iterative Scratchpad Variables *)
    aGrad_Cost                      : ARRAY[1..8] OF REAL;      (* Gradient Vector of Cost Function wrt Actuation u *)
    aControl_u_iter                 : ARRAY[1..8] OF REAL;      (* Iteration Actuator Candidate Vector *)
    rLearning_Rate                  : REAL := 0.0125;           (* Projected Gradient Descent Step Size *)
    nMPC_Iteration                  : INT;                      (* Optimization Loop Counter *)

    (* ========================================================================= *)
    (* 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING SUBSYSTEM VARIABLES    *)
    (* ========================================================================= *)
    (* 1. Slew Absolute Encoders 2oo3 Voting *)
    rSlew_Angle_Voted_deg           : REAL;                     (* Triply-Voted Median Slew Azimuth Angle *)
    rSlew_Dev_12_deg                : REAL;                     (* Deviation Between Channel 1 and Channel 2 *)
    rSlew_Dev_23_deg                : REAL;                     (* Deviation Between Channel 2 and Channel 3 *)
    rSlew_Dev_31_deg                : REAL;                     (* Deviation Between Channel 3 and Channel 1 *)
    rSlew_Tol_deg                   : REAL := 0.450;            (* [deg] Allowable Encoder Discrepancy Tolerance *)
    bSlew_Sens1_Healthy             : BOOL := TRUE;
    bSlew_Sens2_Healthy             : BOOL := TRUE;
    bSlew_Sens3_Healthy             : BOOL := TRUE;
    iSlew_Degraded_Mode             : INT := 3;                 (* 3: Full 2oo3, 2: Degraded 1oo2, 1: Single, 0: Loss *)
    nSlew_Discrepancy_Ticks         : DINT := 0;

    (* 2. Luffing Cylinder Stroke Magnetostrictive Transducers 2oo3 Voting *)
    rLuff_Stroke_Voted_mm           : REAL;                     (* Triply-Voted Median Luffing Cylinder Stroke *)
    rLuff_Dev_12_mm                 : REAL;
    rLuff_Dev_23_mm                 : REAL;
    rLuff_Dev_31_mm                 : REAL;
    rLuff_Tol_mm                    : REAL := 15.0;             (* [mm] Allowable Stroke Discrepancy Tolerance *)
    bLuff_Sens1_Healthy             : BOOL := TRUE;
    bLuff_Sens2_Healthy             : BOOL := TRUE;
    bLuff_Sens3_Healthy             : BOOL := TRUE;
    iLuff_Degraded_Mode             : INT := 3;
    nLuff_Discrepancy_Ticks         : DINT := 0;

    (* 3. Continuous Belt Weigher Load Cells 2oo3 Voting *)
    rBelt_Load_Voted_kN             : REAL;                     (* Triply-Voted Median Belt Weigher Load Cell Force *)
    rBelt_Dev_12_kN                 : REAL;
    rBelt_Dev_23_kN                 : REAL;
    rBelt_Dev_31_kN                 : REAL;
    rBelt_Tol_kN                    : REAL := 2.50;             (* [kN] Allowable Belt Load Discrepancy *)
    bBelt_Sens1_Healthy             : BOOL := TRUE;
    bBelt_Sens2_Healthy             : BOOL := TRUE;
    bBelt_Sens3_Healthy             : BOOL := TRUE;
    iBelt_Degraded_Mode             : INT := 3;
    nBelt_Discrepancy_Ticks         : DINT := 0;

    (* 4. Bucket Wheel Electric Motor Torque Transducers 2oo3 Voting *)
    rBW_Torque_Voted_kNm            : REAL;                     (* Triply-Voted Median Bucket Wheel Shaft Torque *)
    rBW_Dev_12_kNm                  : REAL;
    rBW_Dev_23_kNm                  : REAL;
    rBW_Dev_31_kNm                  : REAL;
    rBW_Tol_kNm                     : REAL := 8.50;             (* [kN m] Allowable Torque Transducer Discrepancy *)
    bBW_Sens1_Healthy               : BOOL := TRUE;
    bBW_Sens2_Healthy               : BOOL := TRUE;
    bBW_Sens3_Healthy               : BOOL := TRUE;
    iBW_Degraded_Mode               : INT := 3;
    nBW_Discrepancy_Ticks           : DINT := 0;

    (* ========================================================================= *)
    (* DYNAMIC BELT WEIGHER DSP FILTER & CONTINUOUS TOTALIZER VARIABLES          *)
    (* ========================================================================= *)
    aBelt_Load_Buffer               : ARRAY[0..4] OF REAL;      (* 5-Point Rolling Low-Pass Filter Buffer *)
    iBelt_Buffer_Ptr                : INT := 0;
    rBelt_Load_Filtered_kN          : REAL := 0.0;
    rBelt_Tare_Zero_Offset_kN       : REAL := 4.250;            (* [kN] Calibrated Tare Weight of Empty Belt & Idlers *)
    rBelt_Tare_Auto_Accumulator     : REAL := 0.0;
    nBelt_Tare_Sample_Count         : DINT := 0;
    bBelt_Auto_Tare_Active          : BOOL := FALSE;
    rLinear_Density_kg_m            : REAL := 0.0;              (* [kg/m] Linear Loading on Conveyor Belt *)
    rBelt_Mass_Flow_Filtered_TPH    : REAL := 0.0;              (* [t/h] Digitally Filtered Real-Time Throughput *)
    rTonnage_Accumulator_Fractional : REAL := 0.0;              (* Sub-Tonne High-Precision Integration Accumulator *)

    (* ========================================================================= *)
    (* 3D LIDAR STOCKPILE CONTOUR SCANNING & ANTI-COLLISION ENGINE VARIABLES     *)
    (* ========================================================================= *)
    rLiDAR_X1_Cartesian_m           : REAL;                     (* Beam 1 Projected X in Machine Datum Coordinate *)
    rLiDAR_Y1_Cartesian_m           : REAL;                     (* Beam 1 Projected Y in Machine Datum Coordinate *)
    rLiDAR_Z1_Cartesian_m           : REAL;                     (* Beam 1 Projected Z in Machine Datum Coordinate *)
    rLiDAR_X2_Cartesian_m           : REAL;
    rLiDAR_Y2_Cartesian_m           : REAL;
    rLiDAR_Z2_Cartesian_m           : REAL;
    rStockpile_Crest_Distance_m     : REAL := 25.0;             (* Distance to Highest Detected Stockpile Crest *)
    rStockpile_Toe_Clearance_m      : REAL := 8.5;              (* Distance to Stockpile Toe Slope *)
    rInfrastructure_Obstacle_Dist_m : REAL := 99.0;             (* Distance to Nearest Yard Structure / Adjacent Machine *)
    rSafety_Envelope_Limit_m        : REAL := 3.00;             (* [m] SIL-3 Minimum Physical Safety Clearance Envelope *)
    rWarning_Envelope_Limit_m       : REAL := 5.00;             (* [m] Caution Encroachment Slowdown Envelope *)

    (* ========================================================================= *)
    (* RAIL TRAVEL ACTIVE SKEW COMPENSATION & ANTI-CRABBING CONTROLLER           *)
    (* ========================================================================= *)
    rRail_Skew_Raw_mm               : REAL := 0.0;              (* Left Rail Position - Right Rail Position *)
    rRail_Skew_Integral_mm_s        : REAL := 0.0;              (* Integrator State for Skew Elimination *)
    rRail_Skew_Derivative_mm_s      : REAL := 0.0;              (* Velocity Differential for Damping *)
    rRail_Skew_Prev_mm              : REAL := 0.0;
    rKp_Skew_Moment                 : REAL := 4.50;             (* Proportional Gain [kN m / mm] *)
    rKi_Skew_Moment                 : REAL := 0.85;             (* Integral Gain [kN m / (mm s)] *)
    rKd_Skew_Moment                 : REAL := 1.20;             (* Derivative Damping Gain [kN m s / mm] *)
    rSkew_Active_Trim_Moment_kNm    : REAL := 0.0;              (* Corrective Steering Yaw Moment *)

    (* ========================================================================= *)
    (* DYNAMIC SLEW COSINE COMPENSATION & BENCH RECLAIM PACING VARIABLES        *)
    (* ========================================================================= *)
    rSlew_Sector_Center_deg         : REAL := 0.0;              (* Angle of Slew Normal to Current Reclaim Bench *)
    rSlew_Angle_Delta_deg           : REAL := 0.0;              (* Angular Deviation from Bench Centerline *)
    rCosine_Term                    : REAL := 1.0;              (* Raw Cosine of Angle Offset *)
    rCosine_Clamped                 : REAL := 1.0;              (* Lower-Bounded Cosine for Velocity Scaling *)
    rSlew_Base_Speed_rpm            : REAL := 0.120;            (* [rpm] Nominal Bench Mid-Span Slewing Velocity *)
    rSlew_Target_Speed_rpm          : REAL := 0.120;
    rSlew_Acceleration_Limit_rpm_s  : REAL := 0.015;            (* [rpm/s] S-Curve Slewing Acceleration Ceiling *)

    (* ========================================================================= *)
    (* 12-STAGE OPERATIONAL FINITE STATE MACHINE (CASE) REGISTERS                *)
    (* ========================================================================= *)
    iState                          : INT := 1;                 (* Active FSM State Enumeration (1..12) *)
    iState_Prev                     : INT := 0;                 (* State from Previous Real-Time Cycle *)
    rState_Dwell_Timer_s            : REAL := 0.0;              (* Continuous Time Spent in Current State *)
    bState_First_Scan               : BOOL := TRUE;

    (* 12 Operational State Constants *)
    STATE_RAIL_ALIGN_ANCHOR_RELEASE : INT := 1;                 (* 1. Machine Rail Travel Alignment & Anchorage Release *)
    STATE_HYD_LUFF_PREPRESSURIZE    : INT := 2;                 (* 2. Hydraulic Luffing Cylinder Pre-Pressurization *)
    STATE_TRIBOOM_CONVEYOR_START    : INT := 3;                 (* 3. Tri-Boom Conveyor Belt Staged Start *)
    STATE_BW_INCH_SOFTSTART_RAMP    : INT := 4;                 (* 4. Bucket Wheel Inching & Soft Start Ramp *)
    STATE_STOCKPILE_3D_LIDAR_SCAN   : INT := 5;                 (* 5. Stockpile Surface 3D LiDAR Scan & Slice Plan *)
    STATE_SLEW_ACCEL_BENCH_RECLAIM  : INT := 6;                 (* 6. Slew Angle Acceleration & Bench Reclaiming *)
    STATE_COSINE_SLEW_VELOCITY_ADAPT: INT := 7;                 (* 7. Cosine Slew Velocity Adaptation *)
    STATE_BENCH_EOT_STEPDOWN_LUFF   : INT := 8;                 (* 8. Bench End-of-Travel Step Down Luff *)
    STATE_CHEVRON_STACKING_MODE     : INT := 9;                 (* 9. Chevron Stockpile Stacking Mode Transition *)
    STATE_STOCKYARD_PARK_CLAMPS     : INT := 10;                (* 10. Stockyard Shift Parking on Rail Clamps *)
    STATE_BELT_GRINDOUT_CHUTE_WASH  : INT := 11;                (* 11. Belt Grind-Out & Chute Wash *)
    STATE_EMERGENCY_SIL3_BRAKE_DUMP : INT := 12;                (* 12. Emergency Structural Overload SIL-3 Brake Dump *)

    (* Bench Reclaiming Sequence Tracking *)
    iBench_Sweep_Direction          : INT := 1;                 (* +1: Slewing Left-to-Right, -1: Right-to-Left *)
    iCurrent_Bench_Layer_Index      : INT := 1;                 (* Vertical Bench Tier Counter (1: Top, 5: Floor) *)
    rBench_Step_Down_Angle_deg      : REAL := 2.85;             (* [deg] Angular Elevation Drop per Bench Tier *)
    rTotal_Reclaimed_Bench_Tonnes   : REAL := 0.0;

    (* ========================================================================= *)
    (* ISA-18.2 MULTI-TIERED ALARM SETPOINTS & HYSTERESIS DEADBANDS              *)
    (* ========================================================================= *)
    ALARM_BW_TORQUE_HH_KNM          : REAL := 820.0;            (* [kN m] Bucket Wheel Stall Overload Trip HH *)
    ALARM_BW_TORQUE_H_KNM           : REAL := 720.0;            (* [kN m] Bucket Wheel Warning High H *)
    ALARM_BW_TORQUE_DEADBAND_KNM    : REAL := 25.0;             (* [kN m] Hysteresis Recovery Deadband *)
    ALARM_RAIL_SKEW_HH_MM           : REAL := 85.0;             (* [mm] Gantry Severe Flange Binding Skew HH *)
    ALARM_RAIL_SKEW_H_MM            : REAL := 45.0;             (* [mm] Gantry Skew Misalignment Warning H *)
    ALARM_RAIL_SKEW_DEADBAND_MM     : REAL := 10.0;             (* [mm] Skew Recovery Deadband *)
    ALARM_LUFF_PRESS_LL_BAR         : REAL := 45.0;             (* [bar] Loss of Hydraulic Holding Pressure LL *)
    ALARM_LUFF_PRESS_HH_BAR         : REAL := 340.0;            (* [bar] Cylinder Over-Pressure Shock HH *)
    ALARM_MASS_FLOW_HH_TPH          : REAL := 7200.0;           (* [t/h] Reclaim Conveyor Belt Severe Overload HH *)
    ALARM_MASS_FLOW_H_TPH           : REAL := 6400.0;           (* [t/h] Reclaim Mass Flow High Warning H *)

    (* Scratchpad Variables & Iterators *)
    iIdx_i                          : INT;
    iIdx_j                          : INT;
    rScratch_Sum                    : REAL;
    rScratch_Val1                   : REAL;
    rScratch_Val2                   : REAL;
    rScratch_Val3                   : REAL;
    rDt_Sec                         : REAL;
END_VAR
""")

    # 5. Algorithm Execution Logic
    parts.append("""
(* ==================================================================================================== *)
(*                                    EXECUTABLE ALGORITHM LOGIC                                        *)
(* ==================================================================================================== *)

(* Calculate Deterministic Sample Time Interval in Seconds *)
IF rDelta_T_ms < 1.0 THEN
    rDt_Sec := 0.010; (* Default: 10 milliseconds (100 Hz scan) *)
ELSE
    rDt_Sec := rDelta_T_ms * 0.0010;
END_IF;

(* Track Operational State Machine Dwell Duration *)
IF iState = iState_Prev THEN
    bState_First_Scan := FALSE;
    rState_Dwell_Timer_s := rState_Dwell_Timer_s + rDt_Sec;
ELSE
    bState_First_Scan := TRUE;
    rState_Dwell_Timer_s := 0.0;
    iState_Prev := iState;
END_IF;

(* Initialize Dynamic Diagnostic Status & Warning Bits for Current Scan Cycle *)
wStatus_Word := 16#0000;
dwAlarm_Warnings := 16#00000000;
(* Note: dwAlarm_Critical_Trips is latched until bFault_Reset_PB is pressed *)

(* ==================================================================================================== *)
(* PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING WITH BUMPLESS DEGRADATION               *)
(* ==================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------- *)
(* 1.1 Slew Absolute Optical Encoders 2oo3 Median Voting Routine                                        *)
(* ---------------------------------------------------------------------------------------------------- *)
rSlew_Dev_12_deg := ABS(rSlew_Angle_Sens1_deg - rSlew_Angle_Sens2_deg);
rSlew_Dev_23_deg := ABS(rSlew_Angle_Sens2_deg - rSlew_Angle_Sens3_deg);
rSlew_Dev_31_deg := ABS(rSlew_Angle_Sens3_deg - rSlew_Angle_Sens1_deg);

bSlew_Sens1_Healthy := (rSlew_Dev_12_deg <= rSlew_Tol_deg) OR (rSlew_Dev_31_deg <= rSlew_Tol_deg);
bSlew_Sens2_Healthy := (rSlew_Dev_12_deg <= rSlew_Tol_deg) OR (rSlew_Dev_23_deg <= rSlew_Tol_deg);
bSlew_Sens3_Healthy := (rSlew_Dev_23_deg <= rSlew_Tol_deg) OR (rSlew_Dev_31_deg <= rSlew_Tol_deg);

IF bSlew_Sens1_Healthy AND bSlew_Sens2_Healthy AND bSlew_Sens3_Healthy THEN
    (* Full 2oo3 Triple Modular Redundancy: Select Median Channel *)
    iSlew_Degraded_Mode := 3;
    IF (rSlew_Angle_Sens1_deg >= rSlew_Angle_Sens2_deg AND rSlew_Angle_Sens1_deg <= rSlew_Angle_Sens3_deg) OR
       (rSlew_Angle_Sens1_deg <= rSlew_Angle_Sens2_deg AND rSlew_Angle_Sens1_deg >= rSlew_Angle_Sens3_deg) THEN
        rSlew_Angle_Voted_deg := rSlew_Angle_Sens1_deg;
    ELSIF (rSlew_Angle_Sens2_deg >= rSlew_Angle_Sens1_deg AND rSlew_Angle_Sens2_deg <= rSlew_Angle_Sens3_deg) OR
          (rSlew_Angle_Sens2_deg <= rSlew_Angle_Sens1_deg AND rSlew_Angle_Sens2_deg >= rSlew_Angle_Sens3_deg) THEN
        rSlew_Angle_Voted_deg := rSlew_Angle_Sens2_deg;
    ELSE
        rSlew_Angle_Voted_deg := rSlew_Angle_Sens3_deg;
    END_IF;
    nSlew_Discrepancy_Ticks := 0;

ELSIF bSlew_Sens1_Healthy AND bSlew_Sens2_Healthy THEN
    (* Degraded 1oo2 Operation: Sensor 3 Failure *)
    iSlew_Degraded_Mode := 2;
    rSlew_Angle_Voted_deg := 0.5 * (rSlew_Angle_Sens1_deg + rSlew_Angle_Sens2_deg);
    dwAlarm_Warnings := dwAlarm_Warnings OR 16#00000001; (* Bit 0: Slew Encoder 3 Discrepancy *)

ELSIF bSlew_Sens2_Healthy AND bSlew_Sens3_Healthy THEN
    (* Degraded 1oo2 Operation: Sensor 1 Failure *)
    iSlew_Degraded_Mode := 2;
    rSlew_Angle_Voted_deg := 0.5 * (rSlew_Angle_Sens2_deg + rSlew_Angle_Sens3_deg);
    dwAlarm_Warnings := dwAlarm_Warnings OR 16#00000002; (* Bit 1: Slew Encoder 1 Discrepancy *)

ELSIF bSlew_Sens3_Healthy AND bSlew_Sens1_Healthy THEN
    (* Degraded 1oo2 Operation: Sensor 2 Failure *)
    iSlew_Degraded_Mode := 2;
    rSlew_Angle_Voted_deg := 0.5 * (rSlew_Angle_Sens3_deg + rSlew_Angle_Sens1_deg);
    dwAlarm_Warnings := dwAlarm_Warnings OR 16#00000004; (* Bit 2: Slew Encoder 2 Discrepancy *)

ELSE
    (* Total Multi-Channel Discrepancy *)
    nSlew_Discrepancy_Ticks := nSlew_Discrepancy_Ticks + 1;
    IF nSlew_Discrepancy_Ticks > 20 THEN (* Persisted > 200 ms *)
        iSlew_Degraded_Mode := 0;
        dwAlarm_Critical_Trips := dwAlarm_Critical_Trips OR 16#00000001; (* Bit 0: Loss of Slew 2oo3 Encoders *)
        rSlew_Angle_Voted_deg := rSlew_Angle_Sens1_deg;
    ELSE
        rSlew_Angle_Voted_deg := rSlew_Angle_Sens1_deg;
    END_IF;
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* 1.2 Luffing Cylinder Stroke Magnetostrictive Transducers 2oo3 Voting Routine                         *)
(* ---------------------------------------------------------------------------------------------------- *)
rLuff_Dev_12_mm := ABS(rLuff_Stroke_Cyl1_Sens1_mm - rLuff_Stroke_Cyl1_Sens2_mm);
rLuff_Dev_23_mm := ABS(rLuff_Stroke_Cyl1_Sens2_mm - rLuff_Stroke_Cyl1_Sens3_mm);
rLuff_Dev_31_mm := ABS(rLuff_Stroke_Cyl1_Sens3_mm - rLuff_Stroke_Cyl1_Sens1_mm);

bLuff_Sens1_Healthy := (rLuff_Dev_12_mm <= rLuff_Tol_mm) OR (rLuff_Dev_31_mm <= rLuff_Tol_mm);
bLuff_Sens2_Healthy := (rLuff_Dev_12_mm <= rLuff_Tol_mm) OR (rLuff_Dev_23_mm <= rLuff_Tol_mm);
bLuff_Sens3_Healthy := (rLuff_Dev_23_mm <= rLuff_Tol_mm) OR (rLuff_Dev_31_mm <= rLuff_Tol_mm);

IF bLuff_Sens1_Healthy AND bLuff_Sens2_Healthy AND bLuff_Sens3_Healthy THEN
    iLuff_Degraded_Mode := 3;
    IF (rLuff_Stroke_Cyl1_Sens1_mm >= rLuff_Stroke_Cyl1_Sens2_mm AND rLuff_Stroke_Cyl1_Sens1_mm <= rLuff_Stroke_Cyl1_Sens3_mm) OR
       (rLuff_Stroke_Cyl1_Sens1_mm <= rLuff_Stroke_Cyl1_Sens2_mm AND rLuff_Stroke_Cyl1_Sens1_mm >= rLuff_Stroke_Cyl1_Sens3_mm) THEN
        rLuff_Stroke_Voted_mm := rLuff_Stroke_Cyl1_Sens1_mm;
    ELSIF (rLuff_Stroke_Cyl1_Sens2_mm >= rLuff_Stroke_Cyl1_Sens1_mm AND rLuff_Stroke_Cyl1_Sens2_mm <= rLuff_Stroke_Cyl1_Sens3_mm) OR
          (rLuff_Stroke_Cyl1_Sens2_mm <= rLuff_Stroke_Cyl1_Sens1_mm AND rLuff_Stroke_Cyl1_Sens2_mm >= rLuff_Stroke_Cyl1_Sens3_mm) THEN
        rLuff_Stroke_Voted_mm := rLuff_Stroke_Cyl1_Sens2_mm;
    ELSE
        rLuff_Stroke_Voted_mm := rLuff_Stroke_Cyl1_Sens3_mm;
    END_IF;
    nLuff_Discrepancy_Ticks := 0;

ELSIF bLuff_Sens1_Healthy AND bLuff_Sens2_Healthy THEN
    iLuff_Degraded_Mode := 2;
    rLuff_Stroke_Voted_mm := 0.5 * (rLuff_Stroke_Cyl1_Sens1_mm + rLuff_Stroke_Cyl1_Sens2_mm);
    dwAlarm_Warnings := dwAlarm_Warnings OR 16#00000010; (* Bit 4: Luff Stroke Sensor 3 Discrepancy *)

ELSIF bLuff_Sens2_Healthy AND bLuff_Sens3_Healthy THEN
    iLuff_Degraded_Mode := 2;
    rLuff_Stroke_Voted_mm := 0.5 * (rLuff_Stroke_Cyl1_Sens2_mm + rLuff_Stroke_Cyl1_Sens3_mm);
    dwAlarm_Warnings := dwAlarm_Warnings OR 16#00000020; (* Bit 5: Luff Stroke Sensor 1 Discrepancy *)

ELSIF bLuff_Sens3_Healthy AND bLuff_Sens1_Healthy THEN
    iLuff_Degraded_Mode := 2;
    rLuff_Stroke_Voted_mm := 0.5 * (rLuff_Stroke_Cyl1_Sens3_mm + rLuff_Stroke_Cyl1_Sens1_mm);
    dwAlarm_Warnings := dwAlarm_Warnings OR 16#00000040; (* Bit 6: Luff Stroke Sensor 2 Discrepancy *)

ELSE
    nLuff_Discrepancy_Ticks := nLuff_Discrepancy_Ticks + 1;
    IF nLuff_Discrepancy_Ticks > 20 THEN
        iLuff_Degraded_Mode := 0;
        dwAlarm_Critical_Trips := dwAlarm_Critical_Trips OR 16#00000002; (* Bit 1: Total Loss Luff Transducers *)
        rLuff_Stroke_Voted_mm := rLuff_Stroke_Cyl1_Sens1_mm;
    ELSE
        rLuff_Stroke_Voted_mm := rLuff_Stroke_Cyl1_Sens1_mm;
    END_IF;
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* 1.3 Continuous Belt Weigher Load Cells 2oo3 Voting Routine                                           *)
(* ---------------------------------------------------------------------------------------------------- *)
rBelt_Dev_12_kN := ABS(rBelt_Load_Cell1_kN - rBelt_Load_Cell2_kN);
rBelt_Dev_23_kN := ABS(rBelt_Load_Cell2_kN - rBelt_Load_Cell3_kN);
rBelt_Dev_31_kN := ABS(rBelt_Load_Cell3_kN - rBelt_Load_Cell1_kN);

bBelt_Sens1_Healthy := (rBelt_Dev_12_kN <= rBelt_Tol_kN) OR (rBelt_Dev_31_kN <= rBelt_Tol_kN);
bBelt_Sens2_Healthy := (rBelt_Dev_12_kN <= rBelt_Tol_kN) OR (rBelt_Dev_23_kN <= rBelt_Tol_kN);
bBelt_Sens3_Healthy := (rBelt_Dev_23_kN <= rBelt_Tol_kN) OR (rBelt_Dev_31_kN <= rBelt_Tol_kN);

IF bBelt_Sens1_Healthy AND bBelt_Sens2_Healthy AND bBelt_Sens3_Healthy THEN
    iBelt_Degraded_Mode := 3;
    IF (rBelt_Load_Cell1_kN >= rBelt_Load_Cell2_kN AND rBelt_Load_Cell1_kN <= rBelt_Load_Cell3_kN) OR
       (rBelt_Load_Cell1_kN <= rBelt_Load_Cell2_kN AND rBelt_Load_Cell1_kN >= rBelt_Load_Cell3_kN) THEN
        rBelt_Load_Voted_kN := rBelt_Load_Cell1_kN;
    ELSIF (rBelt_Load_Cell2_kN >= rBelt_Load_Cell1_kN AND rBelt_Load_Cell2_kN <= rBelt_Load_Cell3_kN) OR
          (rBelt_Load_Cell2_kN <= rBelt_Load_Cell1_kN AND rBelt_Load_Cell2_kN >= rBelt_Load_Cell3_kN) THEN
        rBelt_Load_Voted_kN := rBelt_Load_Cell2_kN;
    ELSE
        rBelt_Load_Voted_kN := rBelt_Load_Cell3_kN;
    END_IF;
    nBelt_Discrepancy_Ticks := 0;

ELSIF bBelt_Sens1_Healthy AND bBelt_Sens2_Healthy THEN
    iBelt_Degraded_Mode := 2;
    rBelt_Load_Voted_kN := 0.5 * (rBelt_Load_Cell1_kN + rBelt_Load_Cell2_kN);
    dwAlarm_Warnings := dwAlarm_Warnings OR 16#00000100; (* Bit 8: Belt Load Cell 3 Discrepancy *)

ELSIF bBelt_Sens2_Healthy AND bBelt_Sens3_Healthy THEN
    iBelt_Degraded_Mode := 2;
    rBelt_Load_Voted_kN := 0.5 * (rBelt_Load_Cell2_kN + rBelt_Load_Cell3_kN);
    dwAlarm_Warnings := dwAlarm_Warnings OR 16#00000200; (* Bit 9: Belt Load Cell 1 Discrepancy *)

ELSIF bBelt_Sens3_Healthy AND bBelt_Sens1_Healthy THEN
    iBelt_Degraded_Mode := 2;
    rBelt_Load_Voted_kN := 0.5 * (rBelt_Load_Cell3_kN + rBelt_Load_Cell1_kN);
    dwAlarm_Warnings := dwAlarm_Warnings OR 16#00000400; (* Bit 10: Belt Load Cell 2 Discrepancy *)

ELSE
    nBelt_Discrepancy_Ticks := nBelt_Discrepancy_Ticks + 1;
    IF nBelt_Discrepancy_Ticks > 20 THEN
        iBelt_Degraded_Mode := 0;
        dwAlarm_Critical_Trips := dwAlarm_Critical_Trips OR 16#00000004; (* Bit 2: Total Loss Belt Weigher *)
        rBelt_Load_Voted_kN := rBelt_Load_Cell1_kN;
    ELSE
        rBelt_Load_Voted_kN := rBelt_Load_Cell1_kN;
    END_IF;
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* 1.4 Bucket Wheel Electric Motor Torque Transducers 2oo3 Voting Routine                               *)
(* ---------------------------------------------------------------------------------------------------- *)
rBW_Dev_12_kNm := ABS(rBW_Motor_Torque_Sens1_kNm - rBW_Motor_Torque_Sens2_kNm);
rBW_Dev_23_kNm := ABS(rBW_Motor_Torque_Sens2_kNm - rBW_Motor_Torque_Sens3_kNm);
rBW_Dev_31_kNm := ABS(rBW_Motor_Torque_Sens3_kNm - rBW_Motor_Torque_Sens1_kNm);

bBW_Sens1_Healthy := (rBW_Dev_12_kNm <= rBW_Tol_kNm) OR (rBW_Dev_31_kNm <= rBW_Tol_kNm);
bBW_Sens2_Healthy := (rBW_Dev_12_kNm <= rBW_Tol_kNm) OR (rBW_Dev_23_kNm <= rBW_Tol_kNm);
bBW_Sens3_Healthy := (rBW_Dev_23_kNm <= rBW_Tol_kNm) OR (rBW_Dev_31_kNm <= rBW_Tol_kNm);

IF bBW_Sens1_Healthy AND bBW_Sens2_Healthy AND bBW_Sens3_Healthy THEN
    iBW_Degraded_Mode := 3;
    IF (rBW_Motor_Torque_Sens1_kNm >= rBW_Motor_Torque_Sens2_kNm AND rBW_Motor_Torque_Sens1_kNm <= rBW_Motor_Torque_Sens3_kNm) OR
       (rBW_Motor_Torque_Sens1_kNm <= rBW_Motor_Torque_Sens2_kNm AND rBW_Motor_Torque_Sens1_kNm >= rBW_Motor_Torque_Sens3_kNm) THEN
        rBW_Torque_Voted_kNm := rBW_Motor_Torque_Sens1_kNm;
    ELSIF (rBW_Motor_Torque_Sens2_kNm >= rBW_Motor_Torque_Sens1_kNm AND rBW_Motor_Torque_Sens2_kNm <= rBW_Motor_Torque_Sens3_kNm) OR
          (rBW_Motor_Torque_Sens2_kNm <= rBW_Motor_Torque_Sens1_kNm AND rBW_Motor_Torque_Sens2_kNm >= rBW_Motor_Torque_Sens3_kNm) THEN
        rBW_Torque_Voted_kNm := rBW_Motor_Torque_Sens2_kNm;
    ELSE
        rBW_Torque_Voted_kNm := rBW_Motor_Torque_Sens3_kNm;
    END_IF;
    nBW_Discrepancy_Ticks := 0;

ELSIF bBW_Sens1_Healthy AND bBW_Sens2_Healthy THEN
    iBW_Degraded_Mode := 2;
    rBW_Torque_Voted_kNm := 0.5 * (rBW_Motor_Torque_Sens1_kNm + rBW_Motor_Torque_Sens2_kNm);
    dwAlarm_Warnings := dwAlarm_Warnings OR 16#00001000; (* Bit 12: BW Torque Sensor 3 Fault *)

ELSIF bBW_Sens2_Healthy AND bBW_Sens3_Healthy THEN
    iBW_Degraded_Mode := 2;
    rBW_Torque_Voted_kNm := 0.5 * (rBW_Motor_Torque_Sens2_kNm + rBW_Motor_Torque_Sens3_kNm);
    dwAlarm_Warnings := dwAlarm_Warnings OR 16#00002000; (* Bit 13: BW Torque Sensor 1 Fault *)

ELSIF bBW_Sens3_Healthy AND bBW_Sens1_Healthy THEN
    iBW_Degraded_Mode := 2;
    rBW_Torque_Voted_kNm := 0.5 * (rBW_Motor_Torque_Sens3_kNm + rBW_Motor_Torque_Sens1_kNm);
    dwAlarm_Warnings := dwAlarm_Warnings OR 16#00004000; (* Bit 14: BW Torque Sensor 2 Fault *)

ELSE
    nBW_Discrepancy_Ticks := nBW_Discrepancy_Ticks + 1;
    IF nBW_Discrepancy_Ticks > 20 THEN
        iBW_Degraded_Mode := 0;
        dwAlarm_Critical_Trips := dwAlarm_Critical_Trips OR 16#00000008; (* Bit 3: Loss of BW Torque Transducers *)
        rBW_Torque_Voted_kNm := rBW_Motor_Torque_Sens1_kNm;
    ELSE
        rBW_Torque_Voted_kNm := rBW_Motor_Torque_Sens1_kNm;
    END_IF;
END_IF;

(* ==================================================================================================== *)
(* PHASE 2: CONTINUOUS DUAL-IDLER DYNAMIC BELT WEIGHER DIGITAL FILTER & INTEGRATION                     *)
(* ==================================================================================================== *)

(* 2.1 5-Stage Moving Average Filter on Voted Load Cell Force *)
aBelt_Load_Buffer[iBelt_Buffer_Ptr] := rBelt_Load_Voted_kN;
iBelt_Buffer_Ptr := (iBelt_Buffer_Ptr + 1) MOD 5;

rScratch_Sum := 0.0;
FOR iIdx_i := 0 TO 4 DO
    rScratch_Sum := rScratch_Sum + aBelt_Load_Buffer[iIdx_i];
END_FOR;
rBelt_Load_Filtered_kN := rScratch_Sum * 0.20;

(* 2.2 Automatic Zero-Tracking Tare Compensation during Empty Belt Operation *)
IF (rBelt_Speed_Encoder_mps > 2.0) AND (rBelt_Load_Filtered_kN < (rBelt_Tare_Zero_Offset_kN + 0.85)) AND
   (iState <> STATE_SLEW_ACCEL_BENCH_RECLAIM) AND (iState <> STATE_COSINE_SLEW_VELOCITY_ADAPT) THEN
    bBelt_Auto_Tare_Active := TRUE;
    rBelt_Tare_Auto_Accumulator := rBelt_Tare_Auto_Accumulator + rBelt_Load_Filtered_kN;
    nBelt_Tare_Sample_Count := nBelt_Tare_Sample_Count + 1;
    IF nBelt_Tare_Sample_Count >= 500 THEN (* Average over 5.0 seconds *)
        rBelt_Tare_Zero_Offset_kN := rBelt_Tare_Auto_Accumulator / 500.0;
        rBelt_Tare_Auto_Accumulator := 0.0;
        nBelt_Tare_Sample_Count := 0;
    END_IF;
ELSE
    bBelt_Auto_Tare_Active := FALSE;
    rBelt_Tare_Auto_Accumulator := 0.0;
    nBelt_Tare_Sample_Count := 0;
END_IF;

(* 2.3 Instantaneous Linear Mass Density & Throughput Calculation *)
rScratch_Val1 := rBelt_Load_Filtered_kN - rBelt_Tare_Zero_Offset_kN;
IF rScratch_Val1 < 0.0 THEN
    rScratch_Val1 := 0.0;
END_IF;

(* Effective linear density q = F_net / (g * L_pitch * cos(alpha_luff)) *)
rScratch_Val2 := COS(rLuff_Boom_Inclinometer_deg * DEG_TO_RAD);
IF rScratch_Val2 < 0.25 THEN
    rScratch_Val2 := 0.25;
END_IF;

rLinear_Density_kg_m := (rScratch_Val1 * 1000.0) / (GRAVITY_ACCEL_MPS2 * IDLER_SPACING_M * rScratch_Val2);

(* Instantaneous Mass Flow Rate [t/h] = 3.6 * q [kg/m] * v [m/s] / 1000.0 *)
rBelt_Mass_Flow_Filtered_TPH := 0.0036 * rLinear_Density_kg_m * rBelt_Speed_Encoder_mps;
rInstantaneous_Throughput_TPH := rBelt_Mass_Flow_Filtered_TPH;

(* Cumulative Shift Production Tonnage Integration *)
rTonnage_Accumulator_Fractional := rTonnage_Accumulator_Fractional + (rBelt_Mass_Flow_Filtered_TPH * (rDt_Sec / 3600.0));
IF rTonnage_Accumulator_Fractional >= 1.0 THEN
    rCumulative_Tonnage_Tonnes := rCumulative_Tonnage_Tonnes + 1.0;
    rTonnage_Accumulator_Fractional := rTonnage_Accumulator_Fractional - 1.0;
END_IF;

(* ==================================================================================================== *)
(* PHASE 3: 3D LIDAR SURFACE PROFILING & INFRASTRUCTURE ANTI-COLLISION ENGINE                           *)
(* ==================================================================================================== *)

(* 3.1 Boom-Tip Spherical to Machine Cartesian Coordinate Frame Transformation *)
rLiDAR_X1_Cartesian_m := rLiDAR1_Distance_m * COS(rLiDAR1_Elevation_deg * DEG_TO_RAD) * COS(rLiDAR1_Azimuth_deg * DEG_TO_RAD);
rLiDAR_Y1_Cartesian_m := rLiDAR1_Distance_m * COS(rLiDAR1_Elevation_deg * DEG_TO_RAD) * SIN(rLiDAR1_Azimuth_deg * DEG_TO_RAD);
rLiDAR_Z1_Cartesian_m := rLiDAR1_Distance_m * SIN(rLiDAR1_Elevation_deg * DEG_TO_RAD);

rLiDAR_X2_Cartesian_m := rLiDAR2_Distance_m * COS(rLiDAR2_Elevation_deg * DEG_TO_RAD) * COS(rLiDAR2_Azimuth_deg * DEG_TO_RAD);
rLiDAR_Y2_Cartesian_m := rLiDAR2_Distance_m * COS(rLiDAR2_Elevation_deg * DEG_TO_RAD) * SIN(rLiDAR2_Azimuth_deg * DEG_TO_RAD);
rLiDAR_Z2_Cartesian_m := rLiDAR2_Distance_m * SIN(rLiDAR2_Elevation_deg * DEG_TO_RAD);

(* 3.2 Clearance Envelope Evaluation *)
rStockpile_Crest_Distance_m := MIN(rLiDAR1_Distance_m, rLiDAR2_Distance_m);
rLiDAR_Min_Clearance_m := rStockpile_Crest_Distance_m;

IF rLiDAR_Min_Clearance_m <= rSafety_Envelope_Limit_m THEN
    bAnti_Collision_Trip := TRUE;
    dwAlarm_Critical_Trips := dwAlarm_Critical_Trips OR 16#00000010; (* Bit 4: Anti-Collision Envelope Violation HH *)
ELSIF rLiDAR_Min_Clearance_m <= rWarning_Envelope_Limit_m THEN
    bAnti_Collision_Trip := FALSE;
    dwAlarm_Warnings := dwAlarm_Warnings OR 16#00010000; (* Bit 16: Obstacle Proximity Warning H *)
ELSE
    bAnti_Collision_Trip := FALSE;
END_IF;

(* ==================================================================================================== *)
(* PHASE 4: RAIL TRAVEL ACTIVE SKEW COMPENSATION & ANTI-CRABBING REGULATOR                              *)
(* ==================================================================================================== *)

rRail_Skew_Raw_mm := (rRail_Gantry_Pos_Left_m - rRail_Gantry_Pos_Right_m) * 1000.0;
rRail_Skew_Error_mm := rRail_Skew_Raw_mm;

(* Skew Derivative *)
rRail_Skew_Derivative_mm_s := (rRail_Skew_Raw_mm - rRail_Skew_Prev_mm) / rDt_Sec;
rRail_Skew_Prev_mm := rRail_Skew_Raw_mm;

(* Skew Integrator with Anti-Windup *)
rRail_Skew_Integral_mm_s := rRail_Skew_Integral_mm_s + (rRail_Skew_Raw_mm * rDt_Sec);
IF rRail_Skew_Integral_mm_s > 500.0 THEN
    rRail_Skew_Integral_mm_s := 500.0;
ELSIF rRail_Skew_Integral_mm_s < -500.0 THEN
    rRail_Skew_Integral_mm_s := -500.0;
END_IF;

(* Corrective Steering Yaw Trim Moment *)
rSkew_Active_Trim_Moment_kNm := (rKp_Skew_Moment * rRail_Skew_Raw_mm) +
                                (rKi_Skew_Moment * rRail_Skew_Integral_mm_s) +
                                (rKd_Skew_Moment * rRail_Skew_Derivative_mm_s);

(* Clamp Steering Trim Moment *)
IF rSkew_Active_Trim_Moment_kNm > 450.0 THEN
    rSkew_Active_Trim_Moment_kNm := 450.0;
ELSIF rSkew_Active_Trim_Moment_kNm < -450.0 THEN
    rSkew_Active_Trim_Moment_kNm := -450.0;
END_IF;

(* ==================================================================================================== *)
(* PHASE 5: DYNAMIC SLEW COSINE SPEED COMPENSATION FOR CONSTANT RECLAIM SLICE VOLUME                   *)
(* ==================================================================================================== *)

rSlew_Sector_Center_deg := 0.5 * (rSlew_Sector_Min_deg + rSlew_Sector_Max_deg);
rSlew_Angle_Delta_deg := rSlew_Angle_Voted_deg - rSlew_Sector_Center_deg;

rCosine_Term := COS(rSlew_Angle_Delta_deg * DEG_TO_RAD);
IF rCosine_Term < 0.250 THEN
    rCosine_Clamped := 0.250; (* Prevent division by zero / excessive slew velocity at edge of bench *)
ELSE
    rCosine_Clamped := rCosine_Term;
END_IF;

rCosine_Compensation_Factor := 1.0 / rCosine_Clamped;
rSlew_Target_Speed_rpm := rSlew_Base_Speed_rpm * rCosine_Compensation_Factor;

(* Apply S-Curve Slewing Velocity Acceleration Ramp Ceiling *)
IF (rSlew_Target_Speed_rpm - rSlew_Speed_Cmd_rpm) > (rSlew_Acceleration_Limit_rpm_s * rDt_Sec) THEN
    rSlew_Speed_Cmd_rpm := rSlew_Speed_Cmd_rpm + (rSlew_Acceleration_Limit_rpm_s * rDt_Sec);
ELSIF (rSlew_Speed_Cmd_rpm - rSlew_Target_Speed_rpm) > (rSlew_Acceleration_Limit_rpm_s * rDt_Sec) THEN
    rSlew_Speed_Cmd_rpm := rSlew_Speed_Cmd_rpm - (rSlew_Acceleration_Limit_rpm_s * rDt_Sec);
ELSE
    rSlew_Speed_Cmd_rpm := rSlew_Target_Speed_rpm;
END_IF;

(* Clamp Slew Speed to Physical Vector Inverter Bounds (0.05 to 0.35 RPM) *)
IF rSlew_Speed_Cmd_rpm > 0.350 THEN
    rSlew_Speed_Cmd_rpm := 0.350;
ELSIF rSlew_Speed_Cmd_rpm < 0.050 THEN
    rSlew_Speed_Cmd_rpm := 0.050;
END_IF;

(* ==================================================================================================== *)
(* PHASE 6: DISCRETE STATE-SPACE PREDICTION & KALMAN STATE ESTIMATOR                                   *)
(* x[k+1] = A * x[k] + B * u[k] + L_obs * (y_meas - C * x_est)                                         *)
(* ==================================================================================================== *)

(* 6.1 Synthesize Physical Measurement Vector y_meas (16x1) *)
aMeasurement_y[1]  := rSlew_Angle_Voted_deg * DEG_TO_RAD;
aMeasurement_y[2]  := rSlew_Velocity_Meas_rpm * (TWO_PI / 60.0);
aMeasurement_y[3]  := aState_x_est[3]; (* Unmeasured internal torsion *)
aMeasurement_y[4]  := aState_x_est[4]; (* Flexural lateral deflection *)
aMeasurement_y[5]  := aState_x_est[5];
aMeasurement_y[6]  := rLuff_Boom_Inclinometer_deg * DEG_TO_RAD;
aMeasurement_y[7]  := aState_x_est[7];
aMeasurement_y[8]  := rLuff_Pressure_Cap_bar;
aMeasurement_y[9]  := rLuff_Pressure_Rod_bar;
aMeasurement_y[10] := aState_x_est[10];
aMeasurement_y[11] := rBW_Motor_Speed_rpm * (TWO_PI / 60.0);
aMeasurement_y[12] := rBW_Torque_Voted_kNm;
aMeasurement_y[13] := 0.5 * (rRail_Gantry_Pos_Left_m + rRail_Gantry_Pos_Right_m);
aMeasurement_y[14] := rRail_Gantry_Speed_mps;
aMeasurement_y[15] := rRail_Skew_Raw_mm;
aMeasurement_y[16] := rLinear_Density_kg_m;

(* 6.2 Calculate Observer Residual e = y - C * x_est *)
FOR iIdx_i := 1 TO 16 DO
    rScratch_Sum := 0.0;
    FOR iIdx_j := 1 TO 16 DO
        rScratch_Sum := rScratch_Sum + aMatrix_C_Sys[iIdx_i, iIdx_j] * aState_x_est[iIdx_j];
    END_FOR;
    aObserver_Residual[iIdx_i] := aMeasurement_y[iIdx_i] - rScratch_Sum;
END_FOR;

(* 6.3 Propagate State Prediction: x_pred = A * x_est + B * u + L_obs * e *)
FOR iIdx_i := 1 TO 16 DO
    rScratch_Sum := 0.0;
    (* State Transition Matrix Multiplication A * x *)
    FOR iIdx_j := 1 TO 16 DO
        rScratch_Sum := rScratch_Sum + aMatrix_A_Sys[iIdx_i, iIdx_j] * aState_x_est[iIdx_j];
    END_FOR;
    (* Control Input Matrix Multiplication B * u *)
    FOR iIdx_j := 1 TO 8 DO
        rScratch_Sum := rScratch_Sum + aMatrix_B_Sys[iIdx_i, iIdx_j] * aControl_u[iIdx_j];
    END_FOR;
    (* Observer Innovation Feedback L_obs * e *)
    FOR iIdx_j := 1 TO 16 DO
        rScratch_Sum := rScratch_Sum + aMatrix_L_Obs_Gain[iIdx_i, iIdx_j] * aObserver_Residual[iIdx_j];
    END_FOR;
    aState_x_pred[iIdx_i] := rScratch_Sum;
END_FOR;

(* Update Estimated State for Next Cycle *)
FOR iIdx_i := 1 TO 16 DO
    aState_x_est[iIdx_i] := aState_x_pred[iIdx_i];
END_FOR;

rBoom_Tip_Deflection_Lat_mm  := aState_x_est[4] * 1000.0;
rBoom_Tip_Deflection_Vert_mm := aState_x_est[10] * 1000.0;

(* ==================================================================================================== *)
(* PHASE 7: RECEDING-HORIZON MPC OPTIMIZATION ROUTINE                                                  *)
(* Minimize J = (x - x_ref)^T Q (x - x_ref) + u^T R u subject to actuator rate & box bounds            *)
(* ==================================================================================================== *)

(* 7.1 Assemble Target Reference Vector x_ref *)
aState_x_ref[1]  := rSlew_Angle_Voted_deg * DEG_TO_RAD;
aState_x_ref[2]  := rSlew_Speed_Cmd_rpm * (TWO_PI / 60.0);
aState_x_ref[3]  := 0.0; (* Zero torsional structural stress *)
aState_x_ref[4]  := 0.0; (* Zero lateral deflection *)
aState_x_ref[5]  := 0.0;
aState_x_ref[6]  := rLuff_Angle_Setpt_deg * DEG_TO_RAD;
aState_x_ref[7]  := 0.0;
aState_x_ref[8]  := 185.0; (* Target holding pressure [bar] *)
aState_x_ref[9]  := 75.0;
aState_x_ref[10] := 0.0; (* Zero vertical deflection *)
aState_x_ref[11] := 6.50 * (TWO_PI / 60.0); (* Rated bucket wheel angular velocity *)
aState_x_ref[12] := 450.0; (* Nominal cutting torque [kN m] *)
aState_x_ref[13] := aState_x_est[13];
aState_x_ref[14] := 0.0;
aState_x_ref[15] := 0.0; (* Zero rail skew misalignment *)
aState_x_ref[16] := (rTarget_Throughput_TPH / 3.6) / MAX(rBelt_Speed_Encoder_mps, 1.0);

(* 7.2 Calculate Nominal LQR Feedback Control: u_nom = -K_mpc * (x_est - x_ref) *)
FOR iIdx_i := 1 TO 8 DO
    rScratch_Sum := 0.0;
    FOR iIdx_j := 1 TO 16 DO
        rScratch_Sum := rScratch_Sum - aMatrix_K_MPC_Gain[iIdx_i, iIdx_j] * (aState_x_est[iIdx_j] - aState_x_ref[iIdx_j]);
    END_FOR;
    aControl_u_iter[iIdx_i] := rScratch_Sum;
END_FOR;

(* 7.3 Unrolled Projected Gradient Optimization with Actuator Box Constraints (4 Iterations) *)
FOR nMPC_Iteration := 1 TO 4 DO
    (* Calculate Actuation Penalty Gradient: Grad = R * u + B^T * Q * (x_est - x_ref) *)
    FOR iIdx_i := 1 TO 8 DO
        rScratch_Sum := aMatrix_R_Weight[iIdx_i, iIdx_i] * aControl_u_iter[iIdx_i];
        FOR iIdx_j := 1 TO 16 DO
            rScratch_Sum := rScratch_Sum + aMatrix_B_Sys[iIdx_j, iIdx_i] *
                            aMatrix_Q_Weight[iIdx_j, iIdx_j] * (aState_x_est[iIdx_j] - aState_x_ref[iIdx_j]);
        END_FOR;
        aGrad_Cost[iIdx_i] := rScratch_Sum;
    END_FOR;

    (* Projected Gradient Step *)
    FOR iIdx_i := 1 TO 8 DO
        aControl_u_iter[iIdx_i] := aControl_u_iter[iIdx_i] - (rLearning_Rate * aGrad_Cost[iIdx_i]);
    END_FOR;

    (* Project onto Hard Physical Actuator Saturation Envelopes *)
    (* u1: Slew Torque [-350.0 .. +350.0 kN m] *)
    IF aControl_u_iter[1] > 350.0 THEN aControl_u_iter[1] := 350.0; ELSIF aControl_u_iter[1] < -350.0 THEN aControl_u_iter[1] := -350.0; END_IF;
    (* u2: Luffing Flow [-480.0 .. +480.0 L/min] *)
    IF aControl_u_iter[2] > 480.0 THEN aControl_u_iter[2] := 480.0; ELSIF aControl_u_iter[2] < -480.0 THEN aControl_u_iter[2] := -480.0; END_IF;
    (* u3: BW Torque [0.0 .. 820.0 kN m] *)
    IF aControl_u_iter[3] > 820.0 THEN aControl_u_iter[3] := 820.0; ELSIF aControl_u_iter[3] < 0.0 THEN aControl_u_iter[3] := 0.0; END_IF;
    (* u4: Bogie L Torque [-220.0 .. +220.0 kN m] *)
    IF aControl_u_iter[4] > 220.0 THEN aControl_u_iter[4] := 220.0; ELSIF aControl_u_iter[4] < -220.0 THEN aControl_u_iter[4] := -220.0; END_IF;
    (* u5: Bogie R Torque [-220.0 .. +220.0 kN m] *)
    IF aControl_u_iter[5] > 220.0 THEN aControl_u_iter[5] := 220.0; ELSIF aControl_u_iter[5] < -220.0 THEN aControl_u_iter[5] := -220.0; END_IF;
    (* u6: Belt Speed [0.0 .. 5.2 m/s] *)
    IF aControl_u_iter[6] > 5.2 THEN aControl_u_iter[6] := 5.2; ELSIF aControl_u_iter[6] < 0.0 THEN aControl_u_iter[6] := 0.0; END_IF;
    (* u7: Counterbalance Bias [-50.0 .. +50.0 bar] *)
    IF aControl_u_iter[7] > 50.0 THEN aControl_u_iter[7] := 50.0; ELSIF aControl_u_iter[7] < -50.0 THEN aControl_u_iter[7] := -50.0; END_IF;
    (* u8: Skew Trim Moment [-450.0 .. +450.0 kN m] *)
    IF aControl_u_iter[8] > 450.0 THEN aControl_u_iter[8] := 450.0; ELSIF aControl_u_iter[8] < -450.0 THEN aControl_u_iter[8] := -450.0; END_IF;
END_FOR;

(* Apply Slew Rate Limiting to Computed Optimal Actuations *)
FOR iIdx_i := 1 TO 8 DO
    aControl_u[iIdx_i] := 0.85 * aControl_u_iter[iIdx_i] + 0.15 * aControl_u_prev[iIdx_i];
    aControl_u_prev[iIdx_i] := aControl_u[iIdx_i];
END_FOR;

(* Assign Primary Control Demands *)
rSlew_Torque_Cmd_kNm            := aControl_u[1];
rLuff_Prop_Flow_Cmd_Lmin        := aControl_u[2];
rBW_VFD_Torque_Limit_kNm        := aControl_u[3];
rGantry_Speed_Cmd_Left_mps      := (aControl_u[4] / 220.0) * 0.40;
rGantry_Speed_Cmd_Right_mps     := (aControl_u[5] / 220.0) * 0.40;
rBoom_Conveyor_Speed_Cmd_mps    := aControl_u[6];
rCounterbalance_Valve_Bias_bar  := aControl_u[7];
rLuff_Angle_Cmd_deg             := rLuff_Angle_Setpt_deg;

(* ==================================================================================================== *)
(* PHASE 8: 12-STAGE OPERATIONAL FINITE STATE MACHINE (CASE)                                            *)
(* ==================================================================================================== *)

CASE iState OF

    STATE_RAIL_ALIGN_ANCHOR_RELEASE:
        (* Stage 1: Machine Rail Travel Alignment & Anchorage Release *)
        wStatus_Word := wStatus_Word OR 16#0001;
        bReclaim_Cycle_Active := FALSE;
        bStack_Cycle_Active := FALSE;
        rBW_VFD_Speed_Cmd_rpm := 0.0;

        (* Check Rail Clamps and Storm Anchorage Permissives *)
        IF bMaster_Enable_Cmd AND NOT bEmergency_Stop_PB AND (dwAlarm_Critical_Trips = 16#00000000) THEN
            IF bRail_Clamps_Engaged_FB AND (rState_Dwell_Timer_s < 3.0) THEN
                (* Command Rail Clamp Hydraulic Unclamp Solenoids *)
                wStatus_Word := wStatus_Word OR 16#0002;
            ELSIF (ABS(rRail_Skew_Raw_mm) < 15.0) AND (rState_Dwell_Timer_s >= 3.5) THEN
                (* Alignment verified and clamps confirmed open -> Proceed to Pre-Pressurization *)
                iState := STATE_HYD_LUFF_PREPRESSURIZE;
            END_IF;
        END_IF;

    STATE_HYD_LUFF_PREPRESSURIZE:
        (* Stage 2: Hydraulic Luffing Cylinder Pre-Pressurization *)
        wStatus_Word := wStatus_Word OR 16#0004;
        
        (* Verify Hydraulic Pump Supply Rail Pressure (> 180 bar) *)
        IF rLuff_Pressure_Pump_bar >= 180.0 THEN
            (* Equalize Cap Chamber Pressure to Counterbalance Load *)
            rLuff_Cylinder_Differential_Press_bar := rLuff_Pressure_Cap_bar - (rLuff_Pressure_Rod_bar * (A_CYL_ROD_M2 / A_CYL_CAP_M2));
            IF (rLuff_Cylinder_Differential_Press_bar >= 120.0) AND (rState_Dwell_Timer_s >= 2.0) THEN
                (* Counterbalance pressure stable -> Advance to Conveyor Cascade *)
                iState := STATE_TRIBOOM_CONVEYOR_START;
            END_IF;
        ELSIF rState_Dwell_Timer_s > 8.0 THEN
            (* Hydraulic Pressure Build Timeout *)
            dwAlarm_Warnings := dwAlarm_Warnings OR 16#00000080; (* Bit 7: Hyd Pre-Pressurization Timeout *)
        END_IF;

    STATE_TRIBOOM_CONVEYOR_START:
        (* Stage 3: Tri-Boom Conveyor Belt Staged Start *)
        wStatus_Word := wStatus_Word OR 16#0008;

        IF bBelt_Rip_Detector_OK AND bChute_Plugged_Sensor_OK THEN
            (* Staged Acceleration Ramp: 0.0 to 4.8 m/s over 12 seconds *)
            IF rBoom_Conveyor_Speed_Cmd_mps < 4.80 THEN
                rBoom_Conveyor_Speed_Cmd_mps := rBoom_Conveyor_Speed_Cmd_mps + (0.40 * rDt_Sec);
            ELSE
                rBoom_Conveyor_Speed_Cmd_mps := 4.80;
            END_IF;

            IF (rBelt_Speed_Encoder_mps >= 4.50) AND (rState_Dwell_Timer_s >= 14.0) THEN
                (* Conveyor confirmed at full speed -> Proceed to Bucket Wheel Start *)
                IF bAuto_Reclaim_Start_Cmd THEN
                    iState := STATE_BW_INCH_SOFTSTART_RAMP;
                ELSIF bAuto_Stack_Start_Cmd THEN
                    iState := STATE_CHEVRON_STACKING_MODE;
                END_IF;
            END_IF;
        ELSE
            (* Safety interlock open: abort start *)
            rBoom_Conveyor_Speed_Cmd_mps := 0.0;
            dwAlarm_Critical_Trips := dwAlarm_Critical_Trips OR 16#00000020; (* Bit 5: Chute Plug / Belt Rip *)
        END_IF;

    STATE_BW_INCH_SOFTSTART_RAMP:
        (* Stage 4: Bucket Wheel Inching & Soft Start Ramp *)
        wStatus_Word := wStatus_Word OR 16#0010;

        (* First 3 seconds: Inching verification at 1.5 RPM for planetary lubrication *)
        IF rState_Dwell_Timer_s < 3.0 THEN
            rBW_VFD_Speed_Cmd_rpm := 1.50;
        ELSIF rState_Dwell_Timer_s < 10.0 THEN
            (* Ramp up to nominal operating speed (6.5 RPM) *)
            rBW_VFD_Speed_Cmd_rpm := 1.50 + ((6.50 - 1.50) * ((rState_Dwell_Timer_s - 3.0) / 7.0));
        ELSE
            rBW_VFD_Speed_Cmd_rpm := 6.50;
            IF (rBW_Motor_Speed_rpm >= 6.20) AND (rBW_Torque_Voted_kNm < 350.0) THEN
                (* No-load rotation confirmed healthy -> Advance to LiDAR Scan *)
                iState := STATE_STOCKPILE_3D_LIDAR_SCAN;
            END_IF;
        END_IF;

    STATE_STOCKPILE_3D_LIDAR_SCAN:
        (* Stage 5: Stockpile Surface 3D LiDAR Scan & Slice Plan *)
        wStatus_Word := wStatus_Word OR 16#0020;

        (* Scan stockpile surface contour across active sector *)
        IF (rLiDAR_Min_Clearance_m > rSafety_Envelope_Limit_m) AND (rState_Dwell_Timer_s >= 2.5) THEN
            (* Bench slice coordinates verified: set initial slew trajectory *)
            bBench_Slice_Completed := FALSE;
            IF rSlew_Angle_Voted_deg <= rSlew_Sector_Center_deg THEN
                iBench_Sweep_Direction := +1; (* Swing Left-to-Right *)
            ELSE
                iBench_Sweep_Direction := -1; (* Swing Right-to-Left *)
            END_IF;
            iState := STATE_SLEW_ACCEL_BENCH_RECLAIM;
        END_IF;

    STATE_SLEW_ACCEL_BENCH_RECLAIM:
        (* Stage 6: Slew Angle Acceleration & Bench Reclaiming *)
        wStatus_Word := wStatus_Word OR 16#0040;
        bReclaim_Cycle_Active := TRUE;

        (* Direct slew torque towards target sector limit *)
        IF iBench_Sweep_Direction = +1 THEN
            rSlew_Torque_Cmd_kNm := 125.0 * rCosine_Compensation_Factor;
            IF rSlew_Angle_Voted_deg >= (rSlew_Sector_Max_deg - 0.50) THEN
                bSlew_In_Position := TRUE;
                iState := STATE_BENCH_EOT_STEPDOWN_LUFF;
            ELSE
                bSlew_In_Position := FALSE;
                IF rBelt_Mass_Flow_Filtered_TPH > 800.0 THEN
                    (* Material cut successfully engaged -> Switch to Cosine Velocity Mode *)
                    iState := STATE_COSINE_SLEW_VELOCITY_ADAPT;
                END_IF;
            END_IF;
        ELSE
            rSlew_Torque_Cmd_kNm := -125.0 * rCosine_Compensation_Factor;
            IF rSlew_Angle_Voted_deg <= (rSlew_Sector_Min_deg + 0.50) THEN
                bSlew_In_Position := TRUE;
                iState := STATE_BENCH_EOT_STEPDOWN_LUFF;
            ELSE
                bSlew_In_Position := FALSE;
                IF rBelt_Mass_Flow_Filtered_TPH > 800.0 THEN
                    iState := STATE_COSINE_SLEW_VELOCITY_ADAPT;
                END_IF;
            END_IF;
        END_IF;

    STATE_COSINE_SLEW_VELOCITY_ADAPT:
        (* Stage 7: Cosine Slew Velocity Adaptation & Dynamic Mass Flow Pacing *)
        wStatus_Word := wStatus_Word OR 16#0080;
        bReclaim_Cycle_Active := TRUE;

        (* Pacing loop: Modulate slew speed to track target throughput (6,000 t/h) *)
        rScratch_Val1 := rTarget_Throughput_TPH - rBelt_Mass_Flow_Filtered_TPH;
        rSlew_Base_Speed_rpm := 0.120 + (rScratch_Val1 * 0.000025);
        IF rSlew_Base_Speed_rpm > 0.220 THEN
            rSlew_Base_Speed_rpm := 0.220;
        ELSIF rSlew_Base_Speed_rpm < 0.040 THEN
            rSlew_Base_Speed_rpm := 0.040;
        END_IF;

        (* Directional Slew Progress *)
        IF iBench_Sweep_Direction = +1 THEN
            IF rSlew_Angle_Voted_deg >= (rSlew_Sector_Max_deg - 0.25) THEN
                bBench_Slice_Completed := TRUE;
                iState := STATE_BENCH_EOT_STEPDOWN_LUFF;
            END_IF;
        ELSE
            IF rSlew_Angle_Voted_deg <= (rSlew_Sector_Min_deg + 0.25) THEN
                bBench_Slice_Completed := TRUE;
                iState := STATE_BENCH_EOT_STEPDOWN_LUFF;
            END_IF;
        END_IF;

    STATE_BENCH_EOT_STEPDOWN_LUFF:
        (* Stage 8: Bench End-of-Travel Step Down Luff *)
        wStatus_Word := wStatus_Word OR 16#0100;
        bReclaim_Cycle_Active := FALSE;

        (* Stop slewing motion *)
        rSlew_Speed_Cmd_rpm := 0.0;
        rSlew_Torque_Cmd_kNm := 0.0;

        (* Execute Step-Down Luffing Increment (-2.85 deg per bench) *)
        IF rState_Dwell_Timer_s >= 2.0 THEN
            rLuff_Angle_Setpt_deg := rLuff_Angle_Setpt_deg - (rBench_Step_Down_Angle_deg * (rDt_Sec / 5.0));
            IF rLuff_Angle_Setpt_deg < -15.0 THEN
                rLuff_Angle_Setpt_deg := -15.0; (* Bottom trench floor limit *)
            END_IF;

            IF (ABS(rLuff_Boom_Inclinometer_deg - rLuff_Angle_Setpt_deg) < 0.15) AND (rState_Dwell_Timer_s >= 7.5) THEN
                bLuff_Target_Reached := TRUE;
                (* Reverse Slew Direction and Increment Bench Layer *)
                iBench_Sweep_Direction := -iBench_Sweep_Direction;
                iCurrent_Bench_Layer_Index := iCurrent_Bench_Layer_Index + 1;
                IF iCurrent_Bench_Layer_Index > 5 THEN
                    (* Stockpile bench exhausted -> Complete cycle or advance gantry *)
                    iState := STATE_BELT_GRINDOUT_CHUTE_WASH;
                ELSE
                    iState := STATE_STOCKPILE_3D_LIDAR_SCAN;
                END_IF;
            END_IF;
        END_IF;

    STATE_CHEVRON_STACKING_MODE:
        (* Stage 9: Chevron Stockpile Stacking Mode Transition *)
        wStatus_Word := wStatus_Word OR 16#0200;
        bStack_Cycle_Active := TRUE;
        rBW_VFD_Speed_Cmd_rpm := 0.0; (* Bucket wheel idle in stacking mode *)

        (* Slew to designated stacking centerline and maintain boom crest elevation *)
        rLuff_Angle_Setpt_deg := 14.5; (* High crest stacking elevation *)
        IF (ABS(rLuff_Boom_Inclinometer_deg - 14.5) < 0.25) AND (rBelt_Mass_Flow_Filtered_TPH > 1000.0) THEN
            (* Longitudinal Gantry Travel Oscillation for Chevron Layering *)
            rGantry_Speed_Cmd_Left_mps := 0.15;
            rGantry_Speed_Cmd_Right_mps := 0.15;
        END_IF;

        IF NOT bAuto_Stack_Start_Cmd THEN
            iState := STATE_BELT_GRINDOUT_CHUTE_WASH;
        END_IF;

    STATE_STOCKYARD_PARK_CLAMPS:
        (* Stage 10: Stockyard Shift Parking on Rail Clamps *)
        wStatus_Word := wStatus_Word OR 16#0400;
        bReclaim_Cycle_Active := FALSE;
        bStack_Cycle_Active := FALSE;

        rSlew_Speed_Cmd_rpm := 0.0;
        rSlew_Torque_Cmd_kNm := 0.0;
        rBW_VFD_Speed_Cmd_rpm := 0.0;
        rBoom_Conveyor_Speed_Cmd_mps := 0.0;
        rGantry_Speed_Cmd_Left_mps := 0.0;
        rGantry_Speed_Cmd_Right_mps := 0.0;

        (* Lower boom to horizontal rest (-2.0 deg) and engage rail storm clamps *)
        rLuff_Angle_Setpt_deg := -2.0;
        IF (ABS(rLuff_Boom_Inclinometer_deg - (-2.0)) < 0.20) AND (rState_Dwell_Timer_s >= 5.0) THEN
            wStatus_Word := wStatus_Word OR 16#0800; (* Parking locks engaged *)
        END_IF;

    STATE_BELT_GRINDOUT_CHUTE_WASH:
        (* Stage 11: Belt Grind-Out & Chute Wash *)
        wStatus_Word := wStatus_Word OR 16#1000;
        bReclaim_Cycle_Active := FALSE;
        rBW_VFD_Speed_Cmd_rpm := 0.0;
        rSlew_Speed_Cmd_rpm := 0.0;

        (* Keep Conveyor Belt Running to Clear Remaining Material *)
        rBoom_Conveyor_Speed_Cmd_mps := 4.80;
        IF (rBelt_Mass_Flow_Filtered_TPH < 25.0) AND (rState_Dwell_Timer_s >= 45.0) THEN
            (* Belt clean: stop conveyor and transition to park *)
            rBoom_Conveyor_Speed_Cmd_mps := 0.0;
            iState := STATE_STOCKYARD_PARK_CLAMPS;
        END_IF;

    STATE_EMERGENCY_SIL3_BRAKE_DUMP:
        (* Stage 12: Emergency Structural Overload SIL-3 Brake Dump *)
        wStatus_Word := wStatus_Word OR 16#8000;
        bSIL3_Emergency_Brake_Tripped := TRUE;
        bReclaim_Cycle_Active := FALSE;
        bStack_Cycle_Active := FALSE;

        (* Instantaneous Actuator Trip to Zero *)
        rSlew_Torque_Cmd_kNm := 0.0;
        rSlew_Speed_Cmd_rpm := 0.0;
        rLuff_Prop_Flow_Cmd_Lmin := 0.0;
        rBW_VFD_Torque_Limit_kNm := 0.0;
        rBW_VFD_Speed_Cmd_rpm := 0.0;
        rGantry_Speed_Cmd_Left_mps := 0.0;
        rGantry_Speed_Cmd_Right_mps := 0.0;
        rBoom_Conveyor_Speed_Cmd_mps := 0.0;

        (* Lock Counterbalance Hydraulics and Drop Fail-Safe Rail Clamps *)
        rCounterbalance_Valve_Bias_bar := 0.0;

        (* Check for Operator Reset Permissive *)
        IF bFault_Reset_PB AND NOT bEmergency_Stop_PB THEN
            dwAlarm_Critical_Trips := 16#00000000;
            bSIL3_Emergency_Brake_Tripped := FALSE;
            iState := STATE_RAIL_ALIGN_ANCHOR_RELEASE;
        END_IF;

END_CASE;

(* Update FSM Status Indicator *)
iFSM_Current_State := iState;

(* ==================================================================================================== *)
(* PHASE 9: ISA-18.2 MULTI-TIERED ALARM MATRIX & TELEMETRY BIT-PACKING                                  *)
(* ==================================================================================================== *)

(* 9.1 Emergency Pushbutton Interlock *)
IF bEmergency_Stop_PB THEN
    dwAlarm_Critical_Trips := dwAlarm_Critical_Trips OR 16#80000000; (* Bit 31: E-Stop Pushbutton Latched *)
    iState := STATE_EMERGENCY_SIL3_BRAKE_DUMP;
END_IF;

(* 9.2 Bucket Wheel Motor Overload & Stall Detection *)
IF rBW_Torque_Voted_kNm >= ALARM_BW_TORQUE_HH_KNM THEN
    dwAlarm_Critical_Trips := dwAlarm_Critical_Trips OR 16#00000040; (* Bit 6: Bucket Wheel Stall Trip HH *)
    iState := STATE_EMERGENCY_SIL3_BRAKE_DUMP;
ELSIF rBW_Torque_Voted_kNm >= ALARM_BW_TORQUE_H_KNM THEN
    dwAlarm_Warnings := dwAlarm_Warnings OR 16#00020000; (* Bit 17: Bucket Wheel Torque High Warning H *)
END_IF;

(* 9.3 Rail Travel Skew Misalignment Detection *)
IF ABS(rRail_Skew_Raw_mm) >= ALARM_RAIL_SKEW_HH_MM THEN
    dwAlarm_Critical_Trips := dwAlarm_Critical_Trips OR 16#00000080; (* Bit 7: Rail Skew Severe Binding HH *)
    iState := STATE_EMERGENCY_SIL3_BRAKE_DUMP;
ELSIF ABS(rRail_Skew_Raw_mm) >= ALARM_RAIL_SKEW_H_MM THEN
    dwAlarm_Warnings := dwAlarm_Warnings OR 16#00040000; (* Bit 18: Rail Skew Misalignment Warning H *)
END_IF;

(* 9.4 Hydraulic Luffing Cylinder Pressure Protection *)
IF (rLuff_Pressure_Cap_bar <= ALARM_LUFF_PRESS_LL_BAR) AND (iState <> STATE_STOCKYARD_PARK_CLAMPS) THEN
    dwAlarm_Critical_Trips := dwAlarm_Critical_Trips OR 16#00000100; (* Bit 8: Loss of Hydraulic Pressure LL *)
    iState := STATE_EMERGENCY_SIL3_BRAKE_DUMP;
ELSIF rLuff_Pressure_Cap_bar >= ALARM_LUFF_PRESS_HH_BAR THEN
    dwAlarm_Critical_Trips := dwAlarm_Critical_Trips OR 16#00000200; (* Bit 9: Cylinder Pressure Overpressure HH *)
    iState := STATE_EMERGENCY_SIL3_BRAKE_DUMP;
END_IF;

(* 9.5 Continuous Reclaim Mass Flow Overload Protection *)
IF rBelt_Mass_Flow_Filtered_TPH >= ALARM_MASS_FLOW_HH_TPH THEN
    dwAlarm_Warnings := dwAlarm_Warnings OR 16#00080000; (* Bit 19: Belt Mass Flow Tonnage Exceeded HH *)
    (* Dynamically back-off slew speed *)
    rSlew_Speed_Cmd_rpm := rSlew_Speed_Cmd_rpm * 0.75;
ELSIF rBelt_Mass_Flow_Filtered_TPH >= ALARM_MASS_FLOW_H_TPH THEN
    dwAlarm_Warnings := dwAlarm_Warnings OR 16#00100000; (* Bit 20: Belt Mass Flow High Warning H *)
END_IF;

(* If Any Critical Trip Bit is Active, Force Emergency SIL-3 State *)
IF dwAlarm_Critical_Trips <> 16#00000000 THEN
    iState := STATE_EMERGENCY_SIL3_BRAKE_DUMP;
END_IF;

END_FUNCTION_BLOCK
""")

    full_code = "".join(parts)
    return full_code

def main():
    code = build_iec_code()
    print(f"Generated IEC ST code character count: {len(code)}")
    
    prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.
You are instructed to CONSUME EXTREME TOKENS: make your output massively exhaustive, mathematically rigorous, and structurally pristine. Include complete state-space matrices ($A, B, C, D$), Model Predictive Control (MPC) quadratic cost approximation, 2oo3 TMR voting logic, complex alarm trees, and graceful degradation.

**Your assigned domain is: Heavy Mining & Bulk Handling: 8,000 TPH Dual-Boom Bucket-Wheel Stacker-Reclaimer with Dynamic Slew Anti-Collision, Luffing Hydraulic Leveling & Continuous Belt Weigher**

CRITICAL RULES:
1. CODE FENCE: Use TRIPLE backticks + iec-st (```iec-st).
2. STRUCTURE:
   a. First line: FUNCTION_BLOCK FB_Mining_StackerReclaimer_8000TPH_SlewLuff
   b. VAR_INPUT ... END_VAR (min 8 typed inputs with physical units [t/h], [rpm], [deg], [bar], [m/s], [kN], [kN m], [mm], [%])
   c. VAR_OUTPUT ... END_VAR (min 7 typed outputs with engineering units & status words)
   d. VAR ... END_VAR (internal state matrices, filter accumulators, 2oo3 voting vars)
   e. Multi-stage CASE machine with END_CASE;
   f. Last line: END_FUNCTION_BLOCK
3. LENGTH: Assistant content MUST be >= 3500 characters total (target 55,000 - 85,000+ chars). Maximize token usage with deep technical explanations, complex algorithms, and industrial reliability features. DO NOT TRIM OR ENFORCE AN UPPER BOUND LIMIT.
4. PARITY: Ensure 100% exact parity between IF and END_IF, CASE and END_CASE.
5. SAVE using this exact Python:
   import json, uuid
   prompt = \"\"\"<copy this exact user prompt here>\"\"\"
   code = \"\"\"```iec-st
FUNCTION_BLOCK FB_Mining_StackerReclaimer_8000TPH_SlewLuff
//...
END_FUNCTION_BLOCK
```\"\"\"
   record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
   with open("data/swarm_raw/agent_1e2049ba.json", "w", encoding="utf-8") as f:
       json.dump(record, f, ensure_ascii=False)
6. REPLY with: EVOLUTION COMPLETE: Heavy Mining & Bulk Handling: 8,000 TPH Dual-Boom Bucket-Wheel Stacker-Reclaimer with Dynamic Slew Anti-Collision, Luffing Hydraulic Leveling & Continuous Belt Weigher"""

    assistant_content = f"```iec-st\n{code}\n```"

    record = {
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": assistant_content}
        ]
    }

    target_path = "data/swarm_raw/agent_1e2049ba.json"
    with open(target_path, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    print(f"Dataset saved successfully to: {target_path}")

if __name__ == "__main__":
    main()
