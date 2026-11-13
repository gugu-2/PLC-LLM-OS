# -*- coding: utf-8 -*-
"""
Full Generator for FB_Mechanical_HeavyPress_ServoDieCushion_TonnageSync
Lumina V7 Max-Persona Protocol: 3,500-Ton BIW Servo Press Automation
"""

import sys
import os
import json
import uuid
import re

def build_full_iec_st():
    parts = []

    # 1. Header
    parts.append("""FUNCTION_BLOCK FB_Mechanical_HeavyPress_ServoDieCushion_TonnageSync
(*
====================================================================================================
 LUMINA CYBER-PHYSICAL AUTOMATION ARCHITECTURE - V7 MAX-PERSONA SPECIFICATION
 CORE SECTOR  : HEAVY MECHANICAL ENGINEERING & COMMERCIAL AUTOMOTIVE STAMPING (TIER 1 PRIORITY)
 SYSTEM       : 3,500-TON (35,000 kN) AUTOMOTIVE BODY-IN-WHITE (BIW) SERVO-MECHANICAL STAMPING PRESS
 FUNCTION     : SYNCHRONIZED MULTI-POINT SERVO DIE CUSHIONING, ECCENTRIC TONNAGE BALANCING & SAFETY
 P&ID TAGGING : ISA-5.1 STANDARD DESIGNATION (WT/ZT/PT/ST/TT/AT/DI/DO/AO SERIES 100-800)
 STANDARDS    : EN ISO 13849-1 (PL e, CAT 4), EN 692 (MECHANICAL PRESS SAFETY), ANSI B11.1, ISA-18.2
 CYBER-PHYSICS: 8x8 DISCRETE STATE-SPACE (Ts = 2 ms) COUPLED WITH RECEDING-HORIZON MPC CONTROLLER
 KINEMATICS   : NON-LINEAR SLIDER-CRANK ECCENTRIC LINK KINEMATICS WITH ELASTIC FRAME DEFLECTION
 CUSHION DYN  : 8-POINT SERVO-HYDRAULIC DIE CUSHION WITH ACTIVE ANTI-REBOUND DAMPING & PRE-ACCELERATION
 ECCENTRICITY : REAL-TIME 4-CORNER LOAD CELL SUMMATION, TIPPING MOMENT (Mx, My) & PARALLELISM LEVELING
 SAFETY SYSTEM: DUAL-CHANNEL OPTICAL LIGHT CURTAIN MUTING, DIE PROTECTION & MECHANICAL BRAKE MONITOR
 REDUNDANCY   : 19-CHANNEL 2oo3 TRIPLE MODULAR REDUNDANCY VOTING ENGINES WITH PERSISTENCE TIMERS
 ALARM ENGINE : ISA-18.2 MULTI-TIER PROCESS ALARM HIERARCHY (HH/H/L/LL) & 4x32-BIT PACKED STATUS WORDS
 FSM TOPOLOGY : 14-STAGE DETERMINISTIC OPERATIONAL FINITE STATE MACHINE (TDC TO BDC FORMING CYCLE)
====================================================================================================
*)
""")

    # 2. VAR_INPUT
    parts.append("""VAR_INPUT
    (* ============================================================================================== *)
    (* SECTION 1: CRANKSHAFT ANGLE 2oo3 RESOLVER & OPTICAL SHAFT ENCODERS                            *)
    (* ============================================================================================== *)
    ST_CRANK_RESOLVER_A               : REAL := 0.000;    (* Crankshaft Absolute Resolver Angle Ch A [deg] *)
    ST_CRANK_RESOLVER_B               : REAL := 0.000;    (* Crankshaft Absolute Resolver Angle Ch B [deg] *)
    ST_CRANK_RESOLVER_C               : REAL := 0.000;    (* Crankshaft Absolute Resolver Angle Ch C [deg] *)

    (* ============================================================================================== *)
    (* SECTION 2: 4-CORNER SLIDE POSITION LINEAR OPTICAL SCALE ENCODERS (2oo3 REDUNDANT)             *)
    (* ============================================================================================== *)
    ZT_SLIDE_POS_FL_A                 : REAL := 0.000;    (* Slide Front-Left Linear Scale Position Ch A [mm] *)
    ZT_SLIDE_POS_FL_B                 : REAL := 0.000;    (* Slide Front-Left Linear Scale Position Ch B [mm] *)
    ZT_SLIDE_POS_FL_C                 : REAL := 0.000;    (* Slide Front-Left Linear Scale Position Ch C [mm] *)
    ZT_SLIDE_POS_FR_A                 : REAL := 0.000;    (* Slide Front-Right Linear Scale Position Ch A [mm] *)
    ZT_SLIDE_POS_FR_B                 : REAL := 0.000;    (* Slide Front-Right Linear Scale Position Ch B [mm] *)
    ZT_SLIDE_POS_FR_C                 : REAL := 0.000;    (* Slide Front-Right Linear Scale Position Ch C [mm] *)
    ZT_SLIDE_POS_RL_A                 : REAL := 0.000;    (* Slide Rear-Left Linear Scale Position Ch A [mm] *)
    ZT_SLIDE_POS_RL_B                 : REAL := 0.000;    (* Slide Rear-Left Linear Scale Position Ch B [mm] *)
    ZT_SLIDE_POS_RL_C                 : REAL := 0.000;    (* Slide Rear-Left Linear Scale Position Ch C [mm] *)
    ZT_SLIDE_POS_RR_A                 : REAL := 0.000;    (* Slide Rear-Right Linear Scale Position Ch A [mm] *)
    ZT_SLIDE_POS_RR_B                 : REAL := 0.000;    (* Slide Rear-Right Linear Scale Position Ch B [mm] *)
    ZT_SLIDE_POS_RR_C                 : REAL := 0.000;    (* Slide Rear-Right Linear Scale Position Ch C [mm] *)

    (* ============================================================================================== *)
    (* SECTION 3: 4-CORNER PRESS FRAME TIE-ROD STRAIN GAUGE TONNAGE LOAD CELLS (2oo3 REDUNDANT)      *)
    (* ============================================================================================== *)
    WT_LOAD_FL_A                      : REAL := 0.000;    (* Front-Left Corner Press Tonnage Load Cell Ch A [kN] *)
    WT_LOAD_FL_B                      : REAL := 0.000;    (* Front-Left Corner Press Tonnage Load Cell Ch B [kN] *)
    WT_LOAD_FL_C                      : REAL := 0.000;    (* Front-Left Corner Press Tonnage Load Cell Ch C [kN] *)
    WT_LOAD_FR_A                      : REAL := 0.000;    (* Front-Right Corner Press Tonnage Load Cell Ch A [kN] *)
    WT_LOAD_FR_B                      : REAL := 0.000;    (* Front-Right Corner Press Tonnage Load Cell Ch B [kN] *)
    WT_LOAD_FR_C                      : REAL := 0.000;    (* Front-Right Corner Press Tonnage Load Cell Ch C [kN] *)
    WT_LOAD_RL_A                      : REAL := 0.000;    (* Rear-Left Corner Press Tonnage Load Cell Ch A [kN] *)
    WT_LOAD_RL_B                      : REAL := 0.000;    (* Rear-Left Corner Press Tonnage Load Cell Ch B [kN] *)
    WT_LOAD_RL_C                      : REAL := 0.000;    (* Rear-Left Corner Press Tonnage Load Cell Ch C [kN] *)
    WT_LOAD_RR_A                      : REAL := 0.000;    (* Rear-Right Corner Press Tonnage Load Cell Ch A [kN] *)
    WT_LOAD_RR_B                      : REAL := 0.000;    (* Rear-Right Corner Press Tonnage Load Cell Ch B [kN] *)
    WT_LOAD_RR_C                      : REAL := 0.000;    (* Rear-Right Corner Press Tonnage Load Cell Ch C [kN] *)

    (* ============================================================================================== *)
    (* SECTION 4: 8-POINT SERVO DIE CUSHION HYDRAULIC PRESSURE TRANSMITTERS (2oo3 REDUNDANT)         *)
    (* ============================================================================================== *)
    PT_CUSH_P1_A                      : REAL := 15.000;   (* Die Cushion Cylinder 1 Chamber Pressure Ch A [bar] *)
    PT_CUSH_P1_B                      : REAL := 15.000;   (* Die Cushion Cylinder 1 Chamber Pressure Ch B [bar] *)
    PT_CUSH_P1_C                      : REAL := 15.000;   (* Die Cushion Cylinder 1 Chamber Pressure Ch C [bar] *)
    PT_CUSH_P2_A                      : REAL := 15.000;   (* Die Cushion Cylinder 2 Chamber Pressure Ch A [bar] *)
    PT_CUSH_P2_B                      : REAL := 15.000;   (* Die Cushion Cylinder 2 Chamber Pressure Ch B [bar] *)
    PT_CUSH_P2_C                      : REAL := 15.000;   (* Die Cushion Cylinder 2 Chamber Pressure Ch C [bar] *)
    PT_CUSH_P3_A                      : REAL := 15.000;   (* Die Cushion Cylinder 3 Chamber Pressure Ch A [bar] *)
    PT_CUSH_P3_B                      : REAL := 15.000;   (* Die Cushion Cylinder 3 Chamber Pressure Ch B [bar] *)
    PT_CUSH_P3_C                      : REAL := 15.000;   (* Die Cushion Cylinder 3 Chamber Pressure Ch C [bar] *)
    PT_CUSH_P4_A                      : REAL := 15.000;   (* Die Cushion Cylinder 4 Chamber Pressure Ch A [bar] *)
    PT_CUSH_P4_B                      : REAL := 15.000;   (* Die Cushion Cylinder 4 Chamber Pressure Ch B [bar] *)
    PT_CUSH_P4_C                      : REAL := 15.000;   (* Die Cushion Cylinder 4 Chamber Pressure Ch C [bar] *)
    PT_CUSH_P5_A                      : REAL := 15.000;   (* Die Cushion Cylinder 5 Chamber Pressure Ch A [bar] *)
    PT_CUSH_P5_B                      : REAL := 15.000;   (* Die Cushion Cylinder 5 Chamber Pressure Ch B [bar] *)
    PT_CUSH_P5_C                      : REAL := 15.000;   (* Die Cushion Cylinder 5 Chamber Pressure Ch C [bar] *)
    PT_CUSH_P6_A                      : REAL := 15.000;   (* Die Cushion Cylinder 6 Chamber Pressure Ch A [bar] *)
    PT_CUSH_P6_B                      : REAL := 15.000;   (* Die Cushion Cylinder 6 Chamber Pressure Ch B [bar] *)
    PT_CUSH_P6_C                      : REAL := 15.000;   (* Die Cushion Cylinder 6 Chamber Pressure Ch C [bar] *)
    PT_CUSH_P7_A                      : REAL := 15.000;   (* Die Cushion Cylinder 7 Chamber Pressure Ch A [bar] *)
    PT_CUSH_P7_B                      : REAL := 15.000;   (* Die Cushion Cylinder 7 Chamber Pressure Ch B [bar] *)
    PT_CUSH_P7_C                      : REAL := 15.000;   (* Die Cushion Cylinder 7 Chamber Pressure Ch C [bar] *)
    PT_CUSH_P8_A                      : REAL := 15.000;   (* Die Cushion Cylinder 8 Chamber Pressure Ch A [bar] *)
    PT_CUSH_P8_B                      : REAL := 15.000;   (* Die Cushion Cylinder 8 Chamber Pressure Ch B [bar] *)
    PT_CUSH_P8_C                      : REAL := 15.000;   (* Die Cushion Cylinder 8 Chamber Pressure Ch C [bar] *)

    (* ============================================================================================== *)
    (* SECTION 5: DIE CUSHION BED LINEAR DISPLACEMENT TRANSDUCERS (2oo3 REDUNDANT)                   *)
    (* ============================================================================================== *)
    ZT_CUSH_POS_L_A                   : REAL := 0.000;    (* Die Cushion Left Bed Displacement Scale Ch A [mm] *)
    ZT_CUSH_POS_L_B                   : REAL := 0.000;    (* Die Cushion Left Bed Displacement Scale Ch B [mm] *)
    ZT_CUSH_POS_L_C                   : REAL := 0.000;    (* Die Cushion Left Bed Displacement Scale Ch C [mm] *)
    ZT_CUSH_POS_R_A                   : REAL := 0.000;    (* Die Cushion Right Bed Displacement Scale Ch A [mm] *)
    ZT_CUSH_POS_R_B                   : REAL := 0.000;    (* Die Cushion Right Bed Displacement Scale Ch B [mm] *)
    ZT_CUSH_POS_R_C                   : REAL := 0.000;    (* Die Cushion Right Bed Displacement Scale Ch C [mm] *)

    (* ============================================================================================== *)
    (* SECTION 6: HYDRAULIC POWER UNIT (HPU) AUXILIARY PROCESS SENSORS                               *)
    (* ============================================================================================== *)
    PT_HYD_SUPPLY                     : REAL := 250.000;  (* Main HPU High Pressure Supply Manifold [bar] *)
    PT_HYD_RETURN                     : REAL := 3.500;    (* Main HPU Return Line Tank Back-Pressure [bar] *)
    PT_HYD_ACCUMULATOR                : REAL := 240.000;  (* Nitrogen Piston Accumulator Pre-Charge Pressure [bar] *)
    PT_HYD_PILOT                      : REAL := 45.000;   (* Proportional Servo Valve Pilot Control Pressure [bar] *)
    PT_SLIDE_COUNTERBALANCE           : REAL := 55.000;   (* Pneumatic/Hydraulic Slide Counterbalance Pressure [bar] *)
    TT_HYD_OIL_TEMP                   : REAL := 42.500;   (* Main Hydraulic Reservoir Bulk Oil Temperature [deg C] *)

    (* ============================================================================================== *)
    (* SECTION 7: SAFETY OPTICAL LIGHT CURTAINS & MUTING DISCRETE SENSORS                             *)
    (* ============================================================================================== *)
    DI_OPTICAL_CURTAIN_FRONT_OSSD1    : BOOL := TRUE;     (* Front Light Curtain Safe Channel OSSD 1 [BOOL] *)
    DI_OPTICAL_CURTAIN_FRONT_OSSD2    : BOOL := TRUE;     (* Front Light Curtain Safe Channel OSSD 2 [BOOL] *)
    DI_OPTICAL_CURTAIN_REAR_OSSD1     : BOOL := TRUE;     (* Rear Light Curtain Safe Channel OSSD 1 [BOOL] *)
    DI_OPTICAL_CURTAIN_REAR_OSSD2     : BOOL := TRUE;     (* Rear Light Curtain Safe Channel OSSD 2 [BOOL] *)
    DI_MUTING_SENSOR_MS1              : BOOL := FALSE;    (* Optical Muting Initiator Sensor MS1 Entrance [BOOL] *)
    DI_MUTING_SENSOR_MS2              : BOOL := FALSE;    (* Optical Muting Initiator Sensor MS2 Inner [BOOL] *)
    DI_MUTING_SENSOR_MS3              : BOOL := FALSE;    (* Optical Muting Initiator Sensor MS3 Outer [BOOL] *)
    DI_MUTING_SENSOR_MS4              : BOOL := FALSE;    (* Optical Muting Initiator Sensor MS4 Exit [BOOL] *)

    (* ============================================================================================== *)
    (* SECTION 8: DIE PROTECTION & MECHANICAL BRAKE MONITORS                                         *)
    (* ============================================================================================== *)
    DI_DIE_PROT_DOUBLE_BLANK          : BOOL := FALSE;    (* Die Protection Laser Double Blank Detection Sensor [BOOL] *)
    DI_DIE_PROT_PART_SEATED           : BOOL := TRUE;     (* Die Lower Cavity Blank In-Nest Seating Sensor [BOOL] *)
    DI_DIE_PROT_PART_EJECTED          : BOOL := FALSE;    (* Upper Die Part Stripped and Ejected Optical Barrier [BOOL] *)
    DI_DIE_PROT_SCRAP_CHUTE_CLEAR     : BOOL := TRUE;     (* Scrap Discharge Chute Obstruction Laser Monitor [BOOL] *)
    DI_BRAKE_PRESSURE_SWITCH          : BOOL := TRUE;     (* Mechanical Flywheel Brake Release Hydraulic Switch [BOOL] *)
    DI_BRAKE_LINING_WEAR_SWITCH       : BOOL := FALSE;    (* Mechanical Brake Pad Friction Lining Wear Limit [BOOL] *)
    DI_BRAKE_ENGAGEMENT_FEEDBACK      : BOOL := FALSE;    (* Mechanical Brake Caliper Microswitch Contact [BOOL] *)
    DI_SAFETY_GATE_INTERLOCKS_OK      : BOOL := TRUE;     (* Perimeter Guard Safety Interlock Gate Circuit OK [BOOL] *)
    DI_EMERGENCY_STOP_HARDWIRE_OK     : BOOL := TRUE;     (* Dual-Channel Hardwired Emergency Stop Relay Healthy [BOOL] *)

    (* ============================================================================================== *)
    (* SECTION 9: RECIPE SETPOINTS, OPERATIONAL LIMITS & CONTROL COMMANDS                            *)
    (* ============================================================================================== *)
    SETPOINT_PRESS_SPEED_SPM          : REAL := 22.000;   (* Nominal Continuous Operating Speed [1/min] *)
    SETPOINT_NOMINAL_TONNAGE          : REAL := 30000.00; (* Stamping Stroke Nominal Target Total Force [kN] *)
    SETPOINT_MAX_ALLOWABLE_TONNAGE    : REAL := 35000.00; (* Maximum Permissible Press Structural Rating [kN] *)
    SETPOINT_CUSHION_FORCE_TOTAL      : REAL := 6000.00;  (* Total Synchronized Die Cushion Blank Holder Force [kN] *)
    SETPOINT_CUSHION_PRE_ACCEL_STROKE : REAL := 35.000;   (* Die Cushion Pre-Acceleration Downward Stroke [mm] *)
    SETPOINT_PRE_ACCEL_ADVANCE_ANGLE  : REAL := 115.000;  (* Crankshaft Angle Initiating Cushion Pre-Accel [deg] *)
    SETPOINT_BDC_DWELL_TIME_MS        : REAL := 40.000;   (* Bottom Dead Center Deep Draw Coining Dwell Time [ms] *)
    SETPOINT_DECOMPRESSION_TIME_MS    : REAL := 55.000;   (* Controlled Hydraulic Decompression Time Window [ms] *)
    SETPOINT_ANTI_REBOUND_DAMP_GAIN   : REAL := 85.000;   (* Active Anti-Rebound Dynamic Hydraulic Damping Gain [%] *)
    SETPOINT_TOLERANCE_TILT_MAX       : REAL := 0.120;    (* Maximum Allowable Slide Parallelism Tilt Error [mm] *)
    SETPOINT_ECCENTRIC_MOMENT_LIMIT   : REAL := 750.000;  (* Maximum Permissible Press Eccentric Tipping Moment [kNm] *)
    SETPOINT_BRAKE_MAX_STOP_TIME_MS   : REAL := 145.000;  (* Mechanical Brake Dynamic Stopping Time HH Trip Limit [ms] *)
    SETPOINT_BRAKE_MAX_OVERRUN_ANGLE  : REAL := 18.500;   (* Crankshaft Dynamic Stopping Angle Overrun HH Limit [deg] *)
    ENABLE_AUTO_CYCLE                 : BOOL := FALSE;    (* Supervisory Automatic Continuous Cycling Permissive [BOOL] *)
    REQUEST_SINGLE_STROKE             : BOOL := FALSE;    (* Operator Single Stamping Stroke Command Pulse [BOOL] *)
    MANUAL_INCHING_FORWARD            : BOOL := FALSE;    (* Manual Maintenance Inching Downward Jog Command [BOOL] *)
    MANUAL_INCHING_REVERSE            : BOOL := FALSE;    (* Manual Maintenance Inching Upward Jog Command [BOOL] *)
    RESET_ALARMS                      : BOOL := FALSE;    (* Supervisory Master Alarm Reset Pushbutton Command [BOOL] *)
    ENABLE_PARALLELISM_ACTIVE_COMP    : BOOL := TRUE;     (* Enable 4-Corner Real-Time Hydraulic Leveling Trim [BOOL] *)
    ENABLE_CUSHION_PRE_ACCELERATION   : BOOL := TRUE;     (* Enable Cushion Impact Velocity Matching Sequence [BOOL] *)
END_VAR
""")

    # 3. VAR_OUTPUT
    parts.append("""VAR_OUTPUT
    (* ============================================================================================== *)
    (* SECTION 1: SERVO RAM DRIVE & MECHANICAL CLUTCH/BRAKE ACTUATION COMMANDS                       *)
    (* ============================================================================================== *)
    OUT_SERVO_RAM_SPEED_REF           : REAL := 0.000;    (* Direct-Drive Servo Ram Velocity Command [mm/s] *)
    OUT_SERVO_RAM_TORQUE_LIMIT        : REAL := 100.000;  (* Main Drive Motor Dynamic Torque Clamping Limit [%] *)
    OUT_BRAKE_RELEASE_SOLENOID        : BOOL := FALSE;    (* Mechanical Flywheel Brake Pneumatic Release Solenoid [BOOL] *)
    OUT_CLUTCH_ENGAGE_SOLENOID        : BOOL := FALSE;    (* Press Main Mechanical Drive Clutch Solenoid [BOOL] *)

    (* ============================================================================================== *)
    (* SECTION 2: 8-POINT PROPORTIONAL SERVO CUSHION PRESSURE/FLOW VALVE COMMANDS                    *)
    (* ============================================================================================== *)
    OUT_CUSH_VALVE_CMD_P1             : REAL := 0.000;    (* Cushion Point 1 Proportional Servo Valve Command [%] *)
    OUT_CUSH_VALVE_CMD_P2             : REAL := 0.000;    (* Cushion Point 2 Proportional Servo Valve Command [%] *)
    OUT_CUSH_VALVE_CMD_P3             : REAL := 0.000;    (* Cushion Point 3 Proportional Servo Valve Command [%] *)
    OUT_CUSH_VALVE_CMD_P4             : REAL := 0.000;    (* Cushion Point 4 Proportional Servo Valve Command [%] *)
    OUT_CUSH_VALVE_CMD_P5             : REAL := 0.000;    (* Cushion Point 5 Proportional Servo Valve Command [%] *)
    OUT_CUSH_VALVE_CMD_P6             : REAL := 0.000;    (* Cushion Point 6 Proportional Servo Valve Command [%] *)
    OUT_CUSH_VALVE_CMD_P7             : REAL := 0.000;    (* Cushion Point 7 Proportional Servo Valve Command [%] *)
    OUT_CUSH_VALVE_CMD_P8             : REAL := 0.000;    (* Cushion Point 8 Proportional Servo Valve Command [%] *)

    (* ============================================================================================== *)
    (* SECTION 3: 4-CORNER SLIDE PARALLELISM ACTIVE LEVELING TILT VALVE COMMANDS                     *)
    (* ============================================================================================== *)
    OUT_TILT_VALVE_CMD_FL             : REAL := 0.000;    (* Slide Leveling Cylinder Front-Left Hydraulic Valve [%] *)
    OUT_TILT_VALVE_CMD_FR             : REAL := 0.000;    (* Slide Leveling Cylinder Front-Right Hydraulic Valve [%] *)
    OUT_TILT_VALVE_CMD_RL             : REAL := 0.000;    (* Slide Leveling Cylinder Rear-Left Hydraulic Valve [%] *)
    OUT_TILT_VALVE_CMD_RR             : REAL := 0.000;    (* Slide Leveling Cylinder Rear-Right Hydraulic Valve [%] *)

    (* ============================================================================================== *)
    (* SECTION 4: FAST DECOMPRESSION DUMP & ANTI-REBOUND DAMPING ACTUATION                           *)
    (* ============================================================================================== *)
    OUT_FAST_DECOMP_VALVE_FL          : BOOL := FALSE;    (* High-Speed Hydraulic Decompression Poppet Valve FL [BOOL] *)
    OUT_FAST_DECOMP_VALVE_FR          : BOOL := FALSE;    (* High-Speed Hydraulic Decompression Poppet Valve FR [BOOL] *)
    OUT_FAST_DECOMP_VALVE_RL          : BOOL := FALSE;    (* High-Speed Hydraulic Decompression Poppet Valve RL [BOOL] *)
    OUT_FAST_DECOMP_VALVE_RR          : BOOL := FALSE;    (* High-Speed Hydraulic Decompression Poppet Valve RR [BOOL] *)
    OUT_ANTI_REBOUND_DAMP_L           : REAL := 0.000;    (* Die Cushion Left Side Active Counter-Pressure Valve [%] *)
    OUT_ANTI_REBOUND_DAMP_R           : REAL := 0.000;    (* Die Cushion Right Side Active Counter-Pressure Valve [%] *)
    OUT_CUSH_PRE_ACCEL_VALVE          : REAL := 0.000;    (* Cushion Pre-Acceleration Downward Boost Valve Command [%] *)
    OUT_PART_LIFTER_EXTEND            : BOOL := FALSE;    (* Die Cushion Pin Part Ejection Lifter Hydraulic Extend [BOOL] *)

    (* ============================================================================================== *)
    (* SECTION 5: SAFETY STATUS, MUTING & BRAKE PERFORMANCE MONITORING                               *)
    (* ============================================================================================== *)
    OUT_SAFETY_MUTING_ACTIVE          : BOOL := FALSE;    (* Optical Light Curtain Certified Muting Condition Active [BOOL] *)
    OUT_SAFETY_READY_INTERLOCK        : BOOL := FALSE;    (* Press Master Safety Permissive Circuit Closed & Ready [BOOL] *)
    OUT_BRAKE_STOPPING_TIME_MS        : REAL := 0.000;    (* Measured Mechanical Brake Full Stopping Time Latency [ms] *)
    OUT_BRAKE_STOPPING_ANGLE_DEG      : REAL := 0.000;    (* Measured Mechanical Brake Crankshaft Overrun Angle [deg] *)
    OUT_TRIP_EMERGENCY_ACTIVE         : BOOL := FALSE;    (* Master Critical Safety System Trip & Fast Dump Active [BOOL] *)

    (* ============================================================================================== *)
    (* SECTION 6: PROCESS VALUES, CYBER-PHYSICAL OBSERVER STATES & TONNAGE METRICS                   *)
    (* ============================================================================================== *)
    OUT_VOTED_CRANK_ANGLE             : REAL := 0.000;    (* Triply Redundant Voted Crankshaft Angular Position [deg] *)
    OUT_VOTED_SLIDE_POSITION          : REAL := 0.000;    (* Mean Voted Slide Linear Displacement from TDC [mm] *)
    OUT_ESTIMATED_RAM_VELOCITY        : REAL := 0.000;    (* First-Principles Cyber-Physical Slide Velocity [mm/s] *)
    OUT_ESTIMATED_TOTAL_TONNAGE       : REAL := 0.000;    (* Summed 4-Corner Measured Press Forming Force [kN] *)
    OUT_ESTIMATED_TONNAGE_FL          : REAL := 0.000;    (* Front-Left Corner Press Tonnage Load [kN] *)
    OUT_ESTIMATED_TONNAGE_FR          : REAL := 0.000;    (* Front-Right Corner Press Tonnage Load [kN] *)
    OUT_ESTIMATED_TONNAGE_RL          : REAL := 0.000;    (* Rear-Left Corner Press Tonnage Load [kN] *)
    OUT_ESTIMATED_TONNAGE_RR          : REAL := 0.000;    (* Rear-Right Corner Press Tonnage Load [kN] *)
    OUT_ESTIMATED_ECCENTRIC_MOMENT_X  : REAL := 0.000;    (* Calculated Press Pitch Overturning Moment Mx [kNm] *)
    OUT_ESTIMATED_ECCENTRIC_MOMENT_Y  : REAL := 0.000;    (* Calculated Press Roll Overturning Moment My [kNm] *)
    OUT_SLIDE_PARALLELISM_TILT_X      : REAL := 0.000;    (* Measured Slide Front-to-Back Pitch Tilt Deviation [mm] *)
    OUT_SLIDE_PARALLELISM_TILT_Y      : REAL := 0.000;    (* Measured Slide Left-to-Right Roll Tilt Deviation [mm] *)
    OUT_TOTAL_CUSHION_FORCE           : REAL := 0.000;    (* Summed 8-Point Dynamic Hydraulic Cushion Resistance [kN] *)
    OUT_MEAN_CUSHION_PRESSURE         : REAL := 0.000;    (* Mean Hydraulic Chamber Pressure Across 8 Cushion Points [bar] *)
    OUT_FRAME_ELASTIC_DEFLECTION      : REAL := 0.000;    (* Estimated Structural Tie-Rod Column Stretch [um] *)

    (* ============================================================================================== *)
    (* SECTION 7: FSM EXECUTION, METRICS & PACKED 32-BIT STATUS WORDS                                *)
    (* ============================================================================================== *)
    OUT_ACTIVE_FSM_STATE              : INT  := 0;        (* Current Operational Finite State Machine State Code [INT] *)
    OUT_CYCLE_TIME_CURRENT_MS         : REAL := 0.000;    (* Active Press Forming Stroke Cycle Duration [ms] *)
    OUT_CYCLE_TIME_LAST_MS            : REAL := 0.000;    (* Completed Previous Stroke Total Cycle Time [ms] *)
    OUT_TOTAL_STROKE_COUNT            : DINT := 0;        (* Total Press Operational Lifetime Stroke Counter [DINT] *)
    OUT_STROKE_COMPLETED_PULSE        : BOOL := FALSE;    (* Single Scan Cycle Completion Strobe Indicator [BOOL] *)
    OUT_STATUS_WORD_01_SYS            : DWORD := 16#00000000; (* Bit-Packed Operational State & Execution Word [DWORD] *)
    OUT_STATUS_WORD_02_ALM            : DWORD := 16#00000000; (* Bit-Packed ISA-18.2 Process Alarm Matrix Word [DWORD] *)
    OUT_STATUS_WORD_03_SAFETY         : DWORD := 16#00000000; (* Bit-Packed Safety Interlock & Brake Monitor Word [DWORD] *)
    OUT_STATUS_WORD_04_CUSH           : DWORD := 16#00000000; (* Bit-Packed 8-Point Cushion & 2oo3 Sensor Health [DWORD] *)
END_VAR
""")

    # 4. VAR
    parts.append("""VAR
    (* ============================================================================================== *)
    (* INTERNAL CYBER-PHYSICAL STATE-SPACE MATRICES (8x8 A, C, L; 8x5 B, D; Ts = 2 ms)               *)
    (* States x: [theta_deg, z_pos_mm, v_ram_mms, tilt_x_mm, tilt_y_mm, p_cush_bar, f_bh_kn, def_um] *)
    (* Inputs u: [t_ram_pct, q_cush_pct, m_bal_x_kNm, m_bal_y_kNm, x_decomp_pct]                     *)
    (* ============================================================================================== *)
    A_MAT : ARRAY[1..8, 1..8] OF REAL; (* Discrete System Dynamics Transition Matrix A *)
    B_MAT : ARRAY[1..8, 1..5] OF REAL; (* Discrete Control Input Coupling Matrix B *)
    C_MAT : ARRAY[1..8, 1..8] OF REAL; (* Discrete State Measurement Mapping Matrix C *)
    D_MAT : ARRAY[1..8, 1..5] OF REAL; (* Discrete Direct Transmission Matrix D *)
    L_OBS : ARRAY[1..8, 1..8] OF REAL; (* Luenberger Cyber-Physical State Observer Gain Matrix L *)

    (* State Estimation Vectors *)
    x_state_hat     : ARRAY[1..8] OF REAL; (* Estimated System State Vector [k] *)
    x_state_pred    : ARRAY[1..8] OF REAL; (* Predicted System State Vector [k+1|k] *)
    y_meas_vec      : ARRAY[1..8] OF REAL; (* Current Sensor Measurement Vector [k] *)
    y_pred_vec      : ARRAY[1..8] OF REAL; (* Predicted Output Vector [k|k-1] *)
    innov_vec       : ARRAY[1..8] OF REAL; (* Innovation Vector e = y_meas - y_pred *)
    u_control_cmd   : ARRAY[1..5] OF REAL; (* Current Optimized Control Effort Vector [k] *)
    u_control_prev  : ARRAY[1..5] OF REAL; (* Previous Execution Cycle Control Effort Vector [k-1] *)

    (* ============================================================================================== *)
    (* RECEDING-HORIZON MPC QUADRATIC COST WEIGHT MATRICES & OPTIMIZER DATA STRUCTURES                *)
    (* Horizon: Np = 10, Nc = 4. Optimization: Projected Gradient Descent (PGD) with Box Constraints *)
    (* ============================================================================================== *)
    Q_WEIGHT_DIAG   : ARRAY[1..8] OF REAL; (* State Tracking Error Diagonal Penalties Q *)
    R_WEIGHT_DIAG   : ARRAY[1..5] OF REAL; (* Actuator Effort Deviation Diagonal Penalties R *)
    S_WEIGHT_DIAG   : ARRAY[1..5] OF REAL; (* Actuator Slew Rate Variation Diagonal Penalties S *)
    P_WEIGHT_DIAG   : ARRAY[1..8] OF REAL; (* Terminal State Cost Horizon Diagonal Penalties P *)
    x_ref_trajectory: ARRAY[1..10, 1..8] OF REAL; (* Predictive Target Trajectory Over Horizon Np *)
    u_opt_horizon   : ARRAY[1..4, 1..5] OF REAL;  (* Predictive Control Actuation Sequence Over Nc *)
    grad_J_u        : ARRAY[1..4, 1..5] OF REAL;  (* Quadratic Cost Functional Gradient Vector *)
    u_box_min       : ARRAY[1..5] OF REAL; (* Physical Lower Saturation Bounds for Actuators *)
    u_box_max       : ARRAY[1..5] OF REAL; (* Physical Upper Saturation Bounds for Actuators *)
    u_slew_max      : ARRAY[1..5] OF REAL; (* Dynamic Maximum Permissible Slew Rates per Cycle *)

    (* ============================================================================================== *)
    (* 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING STRUCTURES (19 SENSOR CHANNELS)            *)
    (* ============================================================================================== *)
    (* Channel 1: Crankshaft Resolver Angle *)
    TMR_CRANK_CH_A_VAL      : REAL;
    TMR_CRANK_CH_B_VAL      : REAL;
    TMR_CRANK_CH_C_VAL      : REAL;
    TMR_CRANK_DEV_AB        : REAL;
    TMR_CRANK_DEV_BC        : REAL;
    TMR_CRANK_DEV_CA        : REAL;
    TMR_CRANK_TOLERANCE     : REAL := 1.250; (* [deg] *)
    TMR_CRANK_DISC_TMR_A    : DINT := 0;
    TMR_CRANK_DISC_TMR_B    : DINT := 0;
    TMR_CRANK_DISC_TMR_C    : DINT := 0;
    TMR_CRANK_CH_A_HEALTHY  : BOOL := TRUE;
    TMR_CRANK_CH_B_HEALTHY  : BOOL := TRUE;
    TMR_CRANK_CH_C_HEALTHY  : BOOL := TRUE;
    TMR_CRANK_VOTED_RESULT  : REAL := 0.000;
    TMR_CRANK_DEGRADED_MODE : INT  := 0; (* 0=3ch, 1=2ch, 2=Degraded 1ch, 3=Fault Hold *)

    (* Channel 2 to 5: 4-Corner Slide Optical Scales (FL, FR, RL, RR) *)
    TMR_SLIDE_FL_CH_A_VAL   : REAL; TMR_SLIDE_FL_CH_B_VAL : REAL; TMR_SLIDE_FL_CH_C_VAL : REAL;
    TMR_SLIDE_FL_DEV_AB     : REAL; TMR_SLIDE_FL_DEV_BC   : REAL; TMR_SLIDE_FL_DEV_CA   : REAL;
    TMR_SLIDE_FL_DISC_TMR_A : DINT := 0; TMR_SLIDE_FL_DISC_TMR_B : DINT := 0; TMR_SLIDE_FL_DISC_TMR_C : DINT := 0;
    TMR_SLIDE_FL_HEALTHY_A  : BOOL := TRUE; TMR_SLIDE_FL_HEALTHY_B : BOOL := TRUE; TMR_SLIDE_FL_HEALTHY_C : BOOL := TRUE;
    TMR_SLIDE_FL_VOTED      : REAL := 0.000; TMR_SLIDE_FL_DEGRADED : INT := 0;

    TMR_SLIDE_FR_CH_A_VAL   : REAL; TMR_SLIDE_FR_CH_B_VAL : REAL; TMR_SLIDE_FR_CH_C_VAL : REAL;
    TMR_SLIDE_FR_DEV_AB     : REAL; TMR_SLIDE_FR_DEV_BC   : REAL; TMR_SLIDE_FR_DEV_CA   : REAL;
    TMR_SLIDE_FR_DISC_TMR_A : DINT := 0; TMR_SLIDE_FR_DISC_TMR_B : DINT := 0; TMR_SLIDE_FR_DISC_TMR_C : DINT := 0;
    TMR_SLIDE_FR_HEALTHY_A  : BOOL := TRUE; TMR_SLIDE_FR_HEALTHY_B : BOOL := TRUE; TMR_SLIDE_FR_HEALTHY_C : BOOL := TRUE;
    TMR_SLIDE_FR_VOTED      : REAL := 0.000; TMR_SLIDE_FR_DEGRADED : INT := 0;

    TMR_SLIDE_RL_CH_A_VAL   : REAL; TMR_SLIDE_RL_CH_B_VAL : REAL; TMR_SLIDE_RL_CH_C_VAL : REAL;
    TMR_SLIDE_RL_DEV_AB     : REAL; TMR_SLIDE_RL_DEV_BC   : REAL; TMR_SLIDE_RL_DEV_CA   : REAL;
    TMR_SLIDE_RL_DISC_TMR_A : DINT := 0; TMR_SLIDE_RL_DISC_TMR_B : DINT := 0; TMR_SLIDE_RL_DISC_TMR_C : DINT := 0;
    TMR_SLIDE_RL_HEALTHY_A  : BOOL := TRUE; TMR_SLIDE_RL_HEALTHY_B : BOOL := TRUE; TMR_SLIDE_RL_HEALTHY_C : BOOL := TRUE;
    TMR_SLIDE_RL_VOTED      : REAL := 0.000; TMR_SLIDE_RL_DEGRADED : INT := 0;

    TMR_SLIDE_RR_CH_A_VAL   : REAL; TMR_SLIDE_RR_CH_B_VAL : REAL; TMR_SLIDE_RR_CH_C_VAL : REAL;
    TMR_SLIDE_RR_DEV_AB     : REAL; TMR_SLIDE_RR_DEV_BC   : REAL; TMR_SLIDE_RR_DEV_CA   : REAL;
    TMR_SLIDE_RR_DISC_TMR_A : DINT := 0; TMR_SLIDE_RR_DISC_TMR_B : DINT := 0; TMR_SLIDE_RR_DISC_TMR_C : DINT := 0;
    TMR_SLIDE_RR_HEALTHY_A  : BOOL := TRUE; TMR_SLIDE_RR_HEALTHY_B : BOOL := TRUE; TMR_SLIDE_RR_HEALTHY_C : BOOL := TRUE;
    TMR_SLIDE_RR_VOTED      : REAL := 0.000; TMR_SLIDE_RR_DEGRADED : INT := 0;

    (* Channel 6 to 9: 4-Corner Tonnage Strain Gauge Load Cells (FL, FR, RL, RR) *)
    TMR_LOAD_FL_CH_A_VAL    : REAL; TMR_LOAD_FL_CH_B_VAL : REAL; TMR_LOAD_FL_CH_C_VAL : REAL;
    TMR_LOAD_FL_DEV_AB      : REAL; TMR_LOAD_FL_DEV_BC   : REAL; TMR_LOAD_FL_DEV_CA   : REAL;
    TMR_LOAD_FL_DISC_TMR_A  : DINT := 0; TMR_LOAD_FL_DISC_TMR_B : DINT := 0; TMR_LOAD_FL_DISC_TMR_C : DINT := 0;
    TMR_LOAD_FL_HEALTHY_A   : BOOL := TRUE; TMR_LOAD_FL_HEALTHY_B : BOOL := TRUE; TMR_LOAD_FL_HEALTHY_C : BOOL := TRUE;
    TMR_LOAD_FL_VOTED       : REAL := 0.000; TMR_LOAD_FL_DEGRADED : INT := 0;

    TMR_LOAD_FR_CH_A_VAL    : REAL; TMR_LOAD_FR_CH_B_VAL : REAL; TMR_LOAD_FR_CH_C_VAL : REAL;
    TMR_LOAD_FR_DEV_AB      : REAL; TMR_LOAD_FR_DEV_BC   : REAL; TMR_LOAD_FR_DEV_CA   : REAL;
    TMR_LOAD_FR_DISC_TMR_A  : DINT := 0; TMR_LOAD_FR_DISC_TMR_B : DINT := 0; TMR_LOAD_FR_DISC_TMR_C : DINT := 0;
    TMR_LOAD_FR_HEALTHY_A   : BOOL := TRUE; TMR_LOAD_FR_HEALTHY_B : BOOL := TRUE; TMR_LOAD_FR_HEALTHY_C : BOOL := TRUE;
    TMR_LOAD_FR_VOTED       : REAL := 0.000; TMR_LOAD_FR_DEGRADED : INT := 0;

    TMR_LOAD_RL_CH_A_VAL    : REAL; TMR_LOAD_RL_CH_B_VAL : REAL; TMR_LOAD_RL_CH_C_VAL : REAL;
    TMR_LOAD_RL_DEV_AB      : REAL; TMR_LOAD_RL_DEV_BC   : REAL; TMR_LOAD_RL_DEV_CA   : REAL;
    TMR_LOAD_RL_DISC_TMR_A  : DINT := 0; TMR_LOAD_RL_DISC_TMR_B : DINT := 0; TMR_LOAD_RL_DISC_TMR_C : DINT := 0;
    TMR_LOAD_RL_HEALTHY_A   : BOOL := TRUE; TMR_LOAD_RL_HEALTHY_B : BOOL := TRUE; TMR_LOAD_RL_HEALTHY_C : BOOL := TRUE;
    TMR_LOAD_RL_VOTED       : REAL := 0.000; TMR_LOAD_RL_DEGRADED : INT := 0;

    TMR_LOAD_RR_CH_A_VAL    : REAL; TMR_LOAD_RR_CH_B_VAL : REAL; TMR_LOAD_RR_CH_C_VAL : REAL;
    TMR_LOAD_RR_DEV_AB      : REAL; TMR_LOAD_RR_DEV_BC   : REAL; TMR_LOAD_RR_DEV_CA   : REAL;
    TMR_LOAD_RR_DISC_TMR_A  : DINT := 0; TMR_LOAD_RR_DISC_TMR_B : DINT := 0; TMR_LOAD_RR_DISC_TMR_C : DINT := 0;
    TMR_LOAD_RR_HEALTHY_A   : BOOL := TRUE; TMR_LOAD_RR_HEALTHY_B : BOOL := TRUE; TMR_LOAD_RR_HEALTHY_C : BOOL := TRUE;
    TMR_LOAD_RR_VOTED       : REAL := 0.000; TMR_LOAD_RR_DEGRADED : INT := 0;

    (* Channel 10 to 17: 8-Point Cushion Pressure Transmitters (P1 to P8) *)
    TMR_PRESS_P1_VOTED : REAL := 15.0; TMR_PRESS_P1_DEGRADED : INT := 0;
    TMR_PRESS_P2_VOTED : REAL := 15.0; TMR_PRESS_P2_DEGRADED : INT := 0;
    TMR_PRESS_P3_VOTED : REAL := 15.0; TMR_PRESS_P3_DEGRADED : INT := 0;
    TMR_PRESS_P4_VOTED : REAL := 15.0; TMR_PRESS_P4_DEGRADED : INT := 0;
    TMR_PRESS_P5_VOTED : REAL := 15.0; TMR_PRESS_P5_DEGRADED : INT := 0;
    TMR_PRESS_P6_VOTED : REAL := 15.0; TMR_PRESS_P6_DEGRADED : INT := 0;
    TMR_PRESS_P7_VOTED : REAL := 15.0; TMR_PRESS_P7_DEGRADED : INT := 0;
    TMR_PRESS_P8_VOTED : REAL := 15.0; TMR_PRESS_P8_DEGRADED : INT := 0;
    TMR_P_DISC_TMR_A : ARRAY[1..8] OF DINT;
    TMR_P_DISC_TMR_B : ARRAY[1..8] OF DINT;
    TMR_P_DISC_TMR_C : ARRAY[1..8] OF DINT;
    TMR_P_HEALTHY_A  : ARRAY[1..8] OF BOOL;
    TMR_P_HEALTHY_B  : ARRAY[1..8] OF BOOL;
    TMR_P_HEALTHY_C  : ARRAY[1..8] OF BOOL;

    (* Channel 18 to 19: Cushion Left & Right Bed Linear Scale Displacements *)
    TMR_CUSH_POS_L_VOTED : REAL := 0.0; TMR_CUSH_POS_L_DEGRADED : INT := 0;
    TMR_CUSH_POS_R_VOTED : REAL := 0.0; TMR_CUSH_POS_R_DEGRADED : INT := 0;
    TMR_CUSH_DISC_TMR_L_A : DINT := 0; TMR_CUSH_DISC_TMR_L_B : DINT := 0; TMR_CUSH_DISC_TMR_L_C : DINT := 0;
    TMR_CUSH_DISC_TMR_R_A : DINT := 0; TMR_CUSH_DISC_TMR_R_B : DINT := 0; TMR_CUSH_DISC_TMR_R_C : DINT := 0;
    TMR_CUSH_HLTH_L_A : BOOL := TRUE; TMR_CUSH_HLTH_L_B : BOOL := TRUE; TMR_CUSH_HLTH_L_C : BOOL := TRUE;
    TMR_CUSH_HLTH_R_A : BOOL := TRUE; TMR_CUSH_HLTH_R_B : BOOL := TRUE; TMR_CUSH_HLTH_R_C : BOOL := TRUE;

    (* ============================================================================================== *)
    (* MECHANICAL KINEMATICS, ECCENTRIC MOMENTS & LEVELING CONTROLLER VARIABLES                       *)
    (* ============================================================================================== *)
    CONST_CRANK_RADIUS_RC   : REAL := 350.000;   (* Eccentric Crank Radius [mm] *)
    CONST_CONROD_LENGTH_LR  : REAL := 1400.000;  (* Main Connecting Rod Link Length [mm] *)
    CONST_LINK_RATIO_LAMBDA : REAL := 0.250000;  (* Kinematic Ratio Lambda = Rc / Lr *)
    CONST_FRAME_STIFFNESS_K : REAL := 17500.00;  (* Stamping Press Bed/Crown Elastic Stiffness [kN/mm] *)
    CONST_BED_WIDTH_X       : REAL := 4500.000;  (* Stamping Press Bolster Bed Span Across X-Axis [mm] *)
    CONST_BED_DEPTH_Y       : REAL := 2500.000;  (* Stamping Press Bolster Bed Span Across Y-Axis [mm] *)
    CONST_CUSH_BORE_AREA_M2 : REAL := 0.031416;  (* Die Cushion 200 mm Bore Cylinder Piston Area [m2] *)

    (* Calculated Kinematic Properties *)
    theta_crank_rad         : REAL;
    sin_theta               : REAL;
    cos_theta               : REAL;
    sin_2theta              : REAL;
    kinematic_stroke_z      : REAL;
    kinematic_velocity_vz   : REAL;
    kinematic_accel_az      : REAL;
    omega_crank_rad_s       : REAL;

    (* Eccentric Load Cell Balancing Properties *)
    sum_tonnage_front       : REAL;
    sum_tonnage_rear        : REAL;
    sum_tonnage_left        : REAL;
    sum_tonnage_right       : REAL;
    eccentric_offset_x_mm   : REAL;
    eccentric_offset_y_mm   : REAL;
    overturning_moment_mx   : REAL;
    overturning_moment_my   : REAL;
    parallelism_tilt_pitch  : REAL;
    parallelism_tilt_roll   : REAL;

    (* 4-Corner Parallelism Active Leveling PID Controllers *)
    pid_pitch_error         : REAL;
    pid_pitch_integral      : REAL := 0.000;
    pid_pitch_deriv         : REAL;
    pid_pitch_error_prev    : REAL := 0.000;
    pid_pitch_out           : REAL;

    pid_roll_error          : REAL;
    pid_roll_integral       : REAL := 0.000;
    pid_roll_deriv          : REAL;
    pid_roll_error_prev     : REAL := 0.000;
    pid_roll_out            : REAL;

    (* ============================================================================================== *)
    (* 8-POINT SERVO DIE CUSHION DYNAMIC CONTROL & ANTI-REBOUND STRUCTURES                            *)
    (* ============================================================================================== *)
    cush_target_force_table : ARRAY[1..10] OF REAL; (* Force vs Depth Profile Table [kN] *)
    cush_depth_breakpoints  : ARRAY[1..10] OF REAL; (* Displacement Breakpoints 0 to 250 mm [mm] *)
    cush_target_current_kn  : REAL;
    cush_target_press_bar   : REAL;
    cush_pre_accel_target_v : REAL;
    cush_anti_rebound_damping_effort : REAL;
    decomp_decay_factor     : REAL;
    decomp_time_elapsed_ms  : REAL := 0.000;
    bdc_latched_pressure    : REAL := 0.000;

    (* ============================================================================================== *)
    (* OPTICAL SAFETY LIGHT CURTAIN MUTING & MECHANICAL BRAKE MONITOR INTERNAL REGISTERS              *)
    (* ============================================================================================== *)
    muting_entry_latch      : BOOL := FALSE;
    muting_active_flag      : BOOL := FALSE;
    muting_timer_ms         : REAL := 0.000;
    muting_direction_valid  : BOOL := FALSE;
    ossd_discrepancy_timer  : REAL := 0.000;

    brake_monitor_in_test   : BOOL := FALSE;
    brake_stop_cmd_angle    : REAL := 0.000;
    brake_stop_cmd_timer_ms : REAL := 0.000;
    brake_measured_stop_time: REAL := 0.000;
    brake_measured_stop_ang : REAL := 0.000;
    brake_speed_at_trip_spm : REAL := 0.000;

    (* ============================================================================================== *)
    (* ISA-18.2 MULTI-TIER PROCESS ALARM RECORDS (16 ALARM BLOCKS)                                    *)
    (* Trip Points: High-High (HH), High (H), Low (L), Low-Low (LL) with Clearance Deadband          *)
    (* ============================================================================================== *)
    ALM_TONNAGE_TOTAL_HH_TRIP   : BOOL := FALSE;
    ALM_TONNAGE_TOTAL_H_WARN    : BOOL := FALSE;
    ALM_MOMENT_MX_HH_TRIP       : BOOL := FALSE;
    ALM_MOMENT_MX_H_WARN        : BOOL := FALSE;
    ALM_MOMENT_MY_HH_TRIP       : BOOL := FALSE;
    ALM_MOMENT_MY_H_WARN        : BOOL := FALSE;
    ALM_TILT_PARALLEL_HH_TRIP   : BOOL := FALSE;
    ALM_TILT_PARALLEL_H_WARN    : BOOL := FALSE;
    ALM_CUSH_PRESS_HH_TRIP      : BOOL := FALSE;
    ALM_CUSH_PRESS_H_WARN       : BOOL := FALSE;
    ALM_CUSH_CAVITATION_LL_TRIP : BOOL := FALSE;
    ALM_BRAKE_STOP_TIME_HH_TRIP : BOOL := FALSE;
    ALM_BRAKE_OVERRUN_HH_TRIP   : BOOL := FALSE;
    ALM_SAFETY_CURTAIN_TRIP     : BOOL := FALSE;
    ALM_DIE_DOUBLE_BLANK_TRIP   : BOOL := FALSE;
    ALM_DIE_PART_NOT_SEATED     : BOOL := FALSE;
    ALM_DIE_PART_NOT_EJECTED    : BOOL := FALSE;
    ALM_TMR_SENSOR_DEGRADED     : BOOL := FALSE;
    ALM_HYD_SUPPLY_PRESS_LOW    : BOOL := FALSE;
    ALM_HYD_OIL_TEMP_HIGH       : BOOL := FALSE;

    (* Alarm Threshold Constants *)
    CFG_DEADBAND_TONNAGE        : REAL := 350.00; (* [kN] *)
    CFG_DEADBAND_MOMENT         : REAL := 25.00;  (* [kNm] *)
    CFG_DEADBAND_TILT           : REAL := 0.015;  (* [mm] *)
    CFG_DEADBAND_PRESSURE       : REAL := 4.50;   (* [bar] *)

    (* ============================================================================================== *)
    (* FINITE STATE MACHINE (FSM) CONTROL STRUCTURES (14 STAGES)                                      *)
    (* ============================================================================================== *)
    nFSM_CurrentState           : INT := 0;
    nFSM_PreviousState          : INT := 0;
    fsm_state_timer_ms          : REAL := 0.000;
    fsm_cycle_timer_ms          : REAL := 0.000;
    fsm_dwell_timer_ms          : REAL := 0.000;
    fsm_eject_timer_ms          : REAL := 0.000;
    fsm_init_complete           : BOOL := FALSE;
    bFirstScanDone              : BOOL := FALSE;

    (* Iteration and Index Loop Counters *)
    i_loop                      : INT;
    j_loop                      : INT;
    k_loop                      : INT;
    pgd_iter                    : INT;
    step_idx                    : INT;
    val_temp                    : REAL;
    diff_temp                   : REAL;
    cost_current                : REAL;
END_VAR
""")

    return "".join(parts)

print("VAR declarations constructed.")
