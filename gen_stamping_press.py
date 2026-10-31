# Generator script for FB_StampingPress_4000Ton_TransferGantry_DieCushion
# Lumina Elite Synthetic Data Swarm - V7 Max Persona

import json
import os
import sys
import re

def build_prompt():
    return """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.
You are instructed to CONSUME EXTREME TOKENS: make your output massively exhaustive, mathematically rigorous, and structurally pristine. Include complete state-space matrices (A, B, C, D), Model Predictive Control (MPC) quadratic cost approximation, 2oo3 TMR voting logic, complex alarm trees, and graceful degradation.

**Your assigned domain is: Heavy Machinery & Metal Stamping: 4,000-Ton Multi-Station Automotive Transfer Stamping Press with 7-Axis Tri-Axis Transfer Gantry, Multi-Point Hydraulic Die Cushion & Eccentricity Tonnage Balancing**

CRITICAL RULES:
1. CODE FENCE: Use TRIPLE backticks + iec-st (```iec-st).
2. STRUCTURE:
   a. First line: FUNCTION_BLOCK FB_StampingPress_4000Ton_TransferGantry_DieCushion
   b. VAR_INPUT ... END_VAR (min 8 typed inputs with physical units [kN], [bar], [mm], [m/s], [deg], [strokes/min], [kN m], [%], [kW], [ms])
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
FUNCTION_BLOCK FB_StampingPress_4000Ton_TransferGantry_DieCushion
//...
END_FUNCTION_BLOCK
```\"\"\"
   record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
   with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
       json.dump(record, f, ensure_ascii=False)
6. REPLY with: EVOLUTION COMPLETE: Heavy Machinery & Metal Stamping: 4,000-Ton Multi-Station Automotive Transfer Stamping Press with 7-Axis Tri-Axis Transfer Gantry, Multi-Point Hydraulic Die Cushion & Eccentricity Tonnage Balancing"""

def build_code():
    parts = []

    # Opening
    parts.append("FUNCTION_BLOCK FB_StampingPress_4000Ton_TransferGantry_DieCushion\n(*\n" +
""" ====================================================================================================
  PROJECT:       COMMERCIAL AUTOMOTIVE METAL STAMPING & BODY-IN-WHITE (BIW) MANUFACTURING LINE
  MODULE:        FB_StampingPress_4000Ton_TransferGantry_DieCushion
  DISCIPLINE:    CYBER-PHYSICAL ADVANCED AUTOMATION / HEAVY METAL FORMING / MULTI-AXIS GANTRY TRANSFER
  STANDARDS:     DIN EN 16092-1 / -2 / -3 (SAFETY OF MACHINE TOOLS - MECHANICAL & HYDRAULIC PRESSES),
                 ISO 13849-1 (SAFETY-RELATED PARTS OF CONTROL SYSTEMS - PL e / CATEGORY 4),
                 IEC 61508 (FUNCTIONAL SAFETY OF ELECTRICAL / ELECTRONIC / PROGRAMMABLE SYSTEMS - SIL 3),
                 VDI 3140 / VDI 3388 (SHEET METAL FORMING TOOLS & PRESS DYNAMICS),
                 ISA-18.2 (MANAGEMENT OF ALARM SYSTEMS FOR THE PROCESS & AUTOMATION INDUSTRIES),
                 IEC 61800-5-2 (ADJUSTABLE SPEED ELECTRICAL POWER DRIVE SYSTEMS - FUNCTIONAL SAFETY).
  AUTHOR:        LUMINA AI CLOUD SWARM - PRINCIPAL AUTOMATION FELLOW & CPS CHAIR (V7 MAX)
  MACHINE CLASS: 4,000 METRIC TON (40,000 kN) MULTI-STATION PROGRESSIVE/TRANSFER STAMPING PRESS
  ACTUATION:     DUAL DIRECT-DRIVE 1,500 kW SYNCHRONOUS TORQUE MOTORS WITH TWIN ECCENTRIC GEAR TRAINS,
                 8-POINT HYDROSTATIC GIB SLIDE GUIDING WITH DYNAMIC OIL FILM GAP MONITORING,
                 8-POINT MULTI-CYLINDER CLOSED-LOOP HYDRAULIC DIE CUSHION (8,000 kN TOTAL HOLDING FORCE),
                 4 DYNAMIC HYDRAULIC TILT-LEVELING CYLINDERS IN BED CORNERS FOR ECCENTRICITY BALANCING,
                 7-AXIS HIGH-SPEED TRI-AXIS TRANSFER GANTRY (X: FEED 2.5 m/s, Y: CLAMP, Z: LIFT 15 m/s^2),
                 HIGH-SPEED DESTACKER BLANK FEEDER WITH DUAL AIR-KNIFE FANNING & 20 ms DOUBLE-BLANK DIVERT,
                 IN-LINE REAL-TIME MULTI-CAMERA OPTICAL PHOTOGRAMMETRY FOR DRAW DEPTH & FLANGE WRINKLING.
  SCAN PERIOD:   T_s = 0.002 s (2 MILLISECONDS DETERMINISTIC REAL-TIME SAFETY & MOTION SCAN CYCLE)
 ----------------------------------------------------------------------------------------------------
  CYBER-PHYSICAL ARCHITECTURAL ARCHITECTURE & MATHEMATICAL FORMULATIONS:
   1. Triple Modular Redundancy (2oo3 TMR) Voting & Discrepancy Fault Integration:
      Performs real-time median voting, spread delta computation, and cumulative discrepancy timing across:
      - Press Main Crank Angle Resolvers (Resolvers 1, 2, 3) [deg]
      - 4-Corner Tie-Rod & Upright Strain Gauge Load Cells (FL, FR, RL, RR - Channels A, B, C) [kN]
      - Multi-Point Hydraulic Die Cushion Manifold Pressure Transmitters (Transmitters A, B, C) [bar]
      - Destacker Laser Sheet Thickness Displacement Transducers (Sensors A, B, C) [mm]
      - Redundant Optical Safety Light Curtain Channels with Hardware Muting & Bumpless Degradation.
   2. Discrete Cyber-Physical State-Space Dynamics (16x16 A_d, 16x8 B_d, 8x16 C_d, 8x8 D_d):
      Models high-order electro-mechanical-hydraulic coupling discretized at T_s = 2.0 ms:
      - x1:  Press slide vertical displacement deviation Delta_z_ram [mm]
      - x2:  Press slide vertical velocity Delta_v_ram [mm/s]
      - x3:  Press structural upright frame strain Delta_epsilon_frame [um/m]
      - x4:  Press upright structural strain rate Delta_dot_epsilon [um/m/s]
      - x5:  Slide tilting pitch angle deviation Delta_theta_pitch [mrad]
      - x6:  Slide tilting roll angle deviation Delta_theta_roll [mrad]
      - x7:  Slide tilting pitch angular velocity Delta_omega_pitch [mrad/s]
      - x8:  Slide tilting roll angular velocity Delta_omega_roll [mrad/s]
      - x9:  Hydraulic die cushion blankholder vertical position Delta_z_cush [mm]
      - x10: Die cushion main hydraulic manifold pressure deviation Delta_P_cush [bar]
      - x11: Die cushion hydraulic fluid compressibility rate Delta_dot_P_cush [bar/s]
      - x12: Transfer gantry feed carriage linear position error Delta_x_gantry [mm]
      - x13: Transfer gantry feed carriage linear velocity Delta_v_gantry [mm/s]
      - x14: Transfer gantry tooling rail 1st structural bending vibration deflection Delta_xi_vibe [mm]
      - x15: Transfer gantry structural vibration velocity Delta_dot_xi_vibe [mm/s]
      - x16: Sheet metal dynamic plastic drawing resistance force perturbation Delta_F_metal [kN]
      Driven by 8 physical control inputs:
      - u1: Dual torque motor master torque reference [kN m]
      - u2: Front-Left (FL) hydraulic dynamic tilt leveling cylinder flow demand [L/min]
      - u3: Front-Right (FR) hydraulic dynamic tilt leveling cylinder flow demand [L/min]
      - u4: Rear-Left (RL) hydraulic dynamic tilt leveling cylinder flow demand [L/min]
      - u5: Rear-Right (RR) hydraulic dynamic tilt leveling cylinder flow demand [L/min]
      - u6: Die cushion proportional servo valve spool flow command [mA]
      - u7: Tri-axis transfer gantry feed carriage X-axis servo torque demand [N m]
      - u8: Tri-axis transfer gantry lift Z-axis servo torque demand [N m]
   3. Receding-Horizon Model Predictive Control (MPC) Quadratic Optimization:
      Formulates an online QP cost functional:
        J = sum_{k=1..Np} [ (x_k - x_ref)' * Q * (x_k - x_ref) + u_k' * R * u_k + Delta_u_k' * R_d * Delta_u_k ]
      Computes analytical gradients grad_J = B_d' * Q * (x_pred - x_ref) + R * u_prev + R_d * Delta_u
      and diagonal Hessian components to execute constrained projected gradient descent with box limits.
   4. Real-Time 4-Corner Center-of-Loading & Dynamic Hydrostatic Tilt Leveling:
      Calculates real-time center of pressure (X_c, Y_c) and eccentric tilting moments (M_x, M_y) from
      the 4-corner load cell array:
        F_total = F_FL + F_FR + F_RL + F_RR
        X_c = [ (F_FR + F_RR) - (F_FL + F_RL) ] / F_total * (W_bed / 2.0)
        Y_c = [ (F_FL + F_FR) - (F_RL + F_RR) ] / F_total * (L_bed / 2.0)
        M_x = F_total * (Y_c / 1000.0) [kN m],  M_y = F_total * (X_c / 1000.0) [kN m]
      Injects closed-loop hydraulic counter-pressure commands into the 4 bed leveling cylinders to cancel
      slide tipping, preventing severe gib scuffing and die guide pillar galling.
   5. 8-Point Multi-Cylinder Hydraulic Die Cushion Profiling & Pre-Acceleration:
      Pre-accelerates cushion cylinders 1..8 upwards prior to punch contact (theta = 110 deg to 125 deg)
      to match instantaneous slide downward velocity v_ram(theta), eliminating impact tonnage shock.
      Executes independent closed-loop servo valve PID profiling during deep draw (theta = 125 deg to 180 deg)
      and provides delayed breakaway cushion lift (theta = 195 deg to 230 deg) preventing vacuum distortion.
   6. High-Speed 7-Axis Tri-Axis Transfer Gantry Electronic Cam (E-Cam) Synchronization:
      Synchronizes transfer gantry Feed X, Clamp Y, and Lift Z axes to virtual master crank angle theta
      using quintic polynomial (5th-order) S-curves. Computes dynamic 3D collision envelope boundaries
      between slide tooling and transfer gripper fingers with hardware-latched SIL-3 interlocks.
   7. Destacker Blank Feeder, Double-Blank Laser Gauging & In-Line Photogrammetry Quality Metrics:
      Coordinates magnetic fanning air-knives, evaluates laser thickness gauge (rejecting double blanks
      > 1.25x t_nom within 20 ms via pneumatic divert gate), and analyzes high-speed photogrammetry
      data (draw depth, flange wrinkle wave amplitude, thinning percentage, split detection).
   8. 12-Stage Operational Finite State Machine (FSM):
      Sequences the complete press cycle from blank pickup to panel egress with sub-millisecond precision.
   9. ISA-18.2 Multi-Tiered Alarm Matrix & Diagnostics Telemetry:
      Categorizes faults into High-High (HH), High (H), Low (L), Low-Low (LL) tiers with deadband hysteresis,
      fail-safe hydraulic overload dump valve tripping, and telemetry bit-packing.
 ====================================================================================================
*)\n")

    # We will append the rest of the python generator logic...
    return "".join(parts)

print("Build code stub defined.")
