# Script to generate the comprehensive IEC 61131-3 dataset for:
# Automotive Paint Shop: High-Speed Robotic Underbody Seam Sealing & Liquid Applied Sound Deadener (LASD) with 6-Axis Coordinated Dispensing & Optical Seam Tracking
# Target File: data/swarm_raw/agent_8d209cb1.json

import os
import json
import re

def generate_st():
    parts = []
    
    # -------------------------------------------------------------------------
    # FUNCTION BLOCK DECLARATION & CYBER-PHYSICAL SYSTEM ARCHITECTURE SPEC
    # -------------------------------------------------------------------------
    parts.append("""FUNCTION_BLOCK FB_Automotive_PaintShop_RoboticPVC_LASD_Dispensing
(*
====================================================================================================
  LUMINA CYBER-PHYSICAL AUTOMATION ARCHITECTURE - SYNTHETIC IEC 61131-3 DATASET ENGINE
  SYSTEM DESIGNATION: CPS-AUTO-PAINTSHOP-PVC-LASD-DISPENSING-MK-VII
  DOMAIN ASSIGNMENT: Automotive Paint Shop: High-Speed Robotic Underbody Seam Sealing & Liquid Applied
                     Sound Deadener (LASD) with 6-Axis Coordinated Dispensing & Optical Seam Tracking.
  STANDARDS COMPLIANCE:
    - IEC 61131-3 3rd Edition (Deterministic Industrial Automation Structured Text)
    - IEC 61508 / IEC 62061 (Functional Safety SIL 3 / Safety Instrumented Systems)
    - ISO 10218-1 / ISO 10218-2 (Robots and Robotic Devices - Safety Requirements for Industrial Robots)
    - ISO 12100 / ISO 13849-1 (Safety of Machinery - Safety-Related Parts of Control Systems Cat 4 / PL e)
    - ISA-18.2 / EEMUA 191 (Management of Alarm Systems for the Process Industries)
    - ASTM D2196 (Standard Test Methods for Rheological Properties of Non-Newtonian Materials)
    - DIN EN ISO 4618 / ISO 2811 (Paints and Varnishes - Determination of Density & Coating Properties)
  PERSONA:
    Principal Automation Fellow & Cyber-Physical Systems Chair (75+ Years Industrial Tenure)
====================================================================================================
  MATHEMATICAL & CYBER-PHYSICAL PROCESS SPECIFICATION:

  1. HIGH-SPEED ROBOTIC FLEET COORDINATION & APPLICATION TOPOLOGY:
     The automated underbody sealing and sound deadener application cell incorporates 6 synchronized
     high-payload 6-axis articulated industrial robots:
       - Robot 1 (R1) & Robot 2 (R2): High-pressure hem flange hem sealing and underbody joint sealing
         utilizing high-viscosity PVC plastisol sealant.
       - Robot 3 (R3) & Robot 4 (R4): Rocker panel and lower sill stone-chip protective spray dispensing
         utilizing flat-fan / swirl airless atomization nozzles.
       - Robot 5 (R5) & Robot 6 (R6): Liquid Applied Sound Deadener (LASD) high-volume acoustic damping
         patch application over front/rear passenger floor pans, transmission tunnel, and spare wheel well.
     All robots are dynamically synchronized to a unified body-in-white (BIW) coordinate frame
     rigidly clamped on a precision pallet transfer skid.

  2. NON-NEWTONIAN RHEOLOGY & FLUID COMPRESSIBILITY:
     PVC plastisol and LASD acoustic damping compounds exhibit pronounced non-Newtonian pseudoplastic,
     thixotropic, and Bingham plastic behavior characterized by the Herschel-Bulkley constitutive law:
       tau = tau_yield + K_consistency * (gamma_dot)^n_flow
     where:
       tau_yield       : Yield shear stress required to initiate flow [Pa] (PVC: ~45-85 Pa, LASD: ~90-140 Pa)
       K_consistency   : Consistency index [Pa*s^n] (PVC: ~65-110 Pa*s^n, LASD: ~120-195 Pa*s^n)
       n_flow          : Flow behavior index (shear thinning exponent, n < 1.0, typically 0.42 to 0.58)
       gamma_dot       : Apparent shear rate in conduit or nozzle [1/s], gamma_dot = 4 * Q / (pi * R_pipe^3)
     Apparent dynamic viscosity:
       mu_app(gamma_dot, T) = (tau_yield / (gamma_dot + epsilon)) + K_consistency * (gamma_dot + epsilon)^(n_flow - 1.0)
     Temperature-viscosity dependency modeled by the Arrhenius-Andrade relation:
       mu_app(T) = mu_ref * EXP( beta_thermo * (T_ref - T_fluid) )
       T_ref = 28.0 deg C, beta_thermo = 0.038 [1/K]
     Fluid compressibility within long high-pressure reinforced hoses (L = 12 to 18 m, D_i = 12.7 mm):
       dP / dt = (beta_effective / V_hose) * (Q_in - Q_out)
     where the effective bulk modulus beta_effective combines fluid compressibility and hose wall elasticity:
       1.0 / beta_effective = (1.0 / beta_fluid) + (D_inner / (t_wall * E_hose_wall))
       beta_fluid = 1.8E9 Pa (18,000 bar), beta_effective = 4,250 bar (accounting for Kevlar/steel braiding).

  3. POSITIVE DISPLACEMENT SHOT METERS & DYNAMIC FLOW-TO-SPEED PACING:
     Precise volumetric dispensing is executed via servo-electric linear ball-screw shot meter cylinders
     equipped with high-resolution absolute encoders (+/- 0.5% volume repeatability).
     Instantaneous target volumetric flow rate Q_target(t) scales strictly with robot Tool Center Point (TCP)
     vector speed v_TCP(t) and instantaneous joint gap width w_gap(t):
       Q_target(t) = A_bead_nominal * v_TCP(t) * (1.0 + k_gap_compensation * w_gap(t))
     Target bead cross-sectional area:
       A_bead = Width_bead * Height_bead * kappa_shape_factor (kappa = pi / 4 for semi-elliptic hem bead)
     Shot meter piston velocity setpoint:
       v_piston(t) = Q_target(t) / A_piston_bore
     Dynamic pre-opening advance time t_pre-open compensates for hydraulic transmission delay and needle inertia:
       t_pre-open = tau_propagation + (v_TCP / (2.0 * a_robot_max))
     Snuff-back suck-back operation:
       Upon robot TCP reaching the end of the seam, the shot meter piston reverses rapidly at -120 mm/s for
       6 to 10 ms while the nozzle needle closes, generating a negative pressure differential Delta P_suckback
       that swallows the droplet and guarantees zero dripping/tail drool on vehicle e-coat primer.

  4. REAL-TIME 3D OPTICAL LASER SEAM TRACKING & IN-LINE METROLOGY:
     Wrist-mounted 250 Hz blue laser line triangulation sensors continuously profile the sheet metal hem
     flange, detecting seam lateral offset Delta Y_seam, vertical offset Delta Z_seam, and flange gap width:
       P_TCP_corrected(t) = P_TCP_trajectory(t) + [Delta X_seam, Delta Y_seam, Delta Z_seam]^T
     Multi-beam laser profiling sensors downstream of the dispense tip measure bead width W (6.0-18.0 mm)
     and height H (1.5-4.5 mm), calculating instantaneous bead continuity, necking, voids, and LASD patch
     areal density rho_areal = rho_fluid * H_film (target 1.2 to 1.8 kg/m2).

  5. DISCRETE STATE-SPACE FORMULATION (16x16 STATE MATRIX):
     The coupled fluidic, electro-mechanical, thermal, and structural dynamics are discretized at Delta t = 2 ms:
       x[k+1] = A * x[k] + B * u[k]
       y[k]   = C * x[k] + D * u[k]
     State vector x in R^16:
       x[1]  : PVC Main Header Supply Pressure P_hdr_PVC [bar]
       x[2]  : PVC Main Header Flow Rate Q_hdr_PVC [ml/s]
       x[3]  : LASD Main Header Supply Pressure P_hdr_LASD [bar]
       x[4]  : LASD Main Header Flow Rate Q_hdr_LASD [ml/s]
       x[5]  : Robot 1 PVC Shot Meter Linear Position x_sm1 [mm]
       x[6]  : Robot 1 PVC Shot Meter Linear Velocity v_sm1 [mm/s]
       x[7]  : Robot 1 Dispense Nozzle Chamber Pressure P_noz_PVC1 [bar]
       x[8]  : Robot 1 Dispense Nozzle Flow Rate Q_noz_PVC1 [ml/s]
       x[9]  : Robot 5 LASD Shot Meter Linear Position x_sm2 [mm]
       x[10] : Robot 5 LASD Shot Meter Linear Velocity v_sm2 [mm/s]
       x[11] : Robot 5 LASD Applicator Pressure P_noz_LASD [bar]
       x[12] : Robot 5 LASD Applicator Flow Rate Q_noz_LASD [ml/s]
       x[13] : Robot Wrist Seam Tracking Trajectory Error Delta e_track [mm]
       x[14] : Robot Arm Structural Flexural Deflection delta_arm [mm]
       x[15] : Coaxial Heated Hose Temperature T_hose [deg C]
       x[16] : Dispensed Bead Cross-Sectional Area A_bead [mm2]

     Control input vector u in R^8:
       u[1] : PVC Hydraulic Ram Pump Extruder Proportional Valve [0-100%]
       u[2] : LASD Hydraulic Ram Pump Extruder Proportional Valve [0-100%]
       u[3] : PVC Shot Meter Servo Velocity Command v_cmd_sm1 [mm/s]
       u[4] : PVC Dispense Nozzle Proportional Needle Lift Command [0-100%]
       u[5] : LASD Shot Meter Servo Velocity Command v_cmd_sm2 [mm/s]
       u[6] : LASD Applicator Swirl Valve Command [0-100%]
       u[7] : Coaxial Heated Hose PWM Heating Element Duty Cycle [0-100%]
       u[8] : Robot TCP Synchronized Vector Speed Feedforward v_TCP [mm/s]

  6. RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC):
     A quadratic cost function over prediction horizon N_p = 5 steps balances reference tracking against
     actuator control effort:
       J = SUM_{k=0}^{N_p-1} [ (x[k] - x_ref)^T * Q * (x[k] - x_ref) + u[k]^T * R * u[k] ]
           + (x[N_p] - x_ref)^T * P * (x[N_p] - x_ref)
     Projected Karush-Kuhn-Tucker (KKT) gradient descent drives optimal control updates respecting actuator
     saturation and slew-rate bounds.

  7. 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) ARCHITECTURE:
     Safety-critical instrumentation channels are voted via 2oo3 median algorithms with pairwise discrepancy
     monitoring:
       - PVC Header Pressure Transducers (Ch A, Ch B, Ch C)
       - LASD Header Pressure Transducers (Ch A, Ch B, Ch C)
       - Shot Meter Optical Encoders (Ch A, Ch B, Ch C)
       - Coaxial Heated Hose Pt100 RTDs (Ch A, Ch B, Ch C)
       - Wrist Laser Seam Height Sensors (Ch A, Ch B, Ch C)
     Discrepancies exceeding physical thresholds for > 50 ms trigger bumpless degradation to 1oo2 or fail-safe lock.

  8. 12-STAGE OPERATIONAL FINITE STATE MACHINE:
     Full production sequence: Skid Infeed & Precision Clamp -> RFID Variant Recognition -> Tool Calibration &
     Nozzle Tip Wipe -> Seam Tracking Pre-Flight -> Coordinated Underbody Hem Flange Sealing -> Floor Pan LASD
     Dispensing -> In-Line Metrology Scan -> Snuff-Back Purge -> Skid Unclamp & Transfer -> Robot Fleet Park ->
     Barrel Changeover Auto-Purge -> Emergency E-Stop Depressurization Dump.

  9. ISA-18.2 ALARM MATRIX & TELEMETRY BIT ENCODING:
     Four priority tiers (High-High, High, Low, Low-Low) with deadband hysteresis prevent nuisance chattering
     across all hydraulic, rheological, thermal, geometric, and robotic degrees of freedom.
====================================================================================================
*)
""")

    # -------------------------------------------------------------------------
    # VAR_INPUT DECLARATION (Minimum 8 strongly typed inputs with bracketed units)
    # -------------------------------------------------------------------------
    parts.append("""VAR_INPUT
    (* Station Master Safety & Interlock Permissions *)
    bSystemEnable                       : BOOL;     (* Station Master Hardware Enable Interlock [-] *)
    bSafetyFenceOK                      : BOOL;     (* Safety Perimeter Guard Fence Interlock Circuit [-] *)
    bEStopActive                        : BOOL;     (* Emergency Stop Active Relay (Active-Low Inverted) [-] *)
    bCycleStartPB                       : BOOL;     (* Operator Console Pushbutton Auto-Cycle Start [-] *)
    bCycleResetPB                       : BOOL;     (* Operator Console Pushbutton Fault Reset [-] *)

    (* Car Body Skid Conveyor & Tooling Infeed *)
    rSkidInfeedPosition                 : REAL;     (* Car Body Skid Conveyor Infeed Position [mm] *)
    bSkidInfeedPresent                  : BOOL;     (* Skid Arrival Infeed Proximity Sensor [-] *)
    bSkidLifterClampedLimit             : BOOL;     (* Body Skid Precision Locating Pin Lifter Clamped [-] *)
    bSkidLifterLoweredLimit             : BOOL;     (* Body Skid Precision Lifter Cylinders Lowered [-] *)
    uiBodyVariantRFID                   : UINT;     (* Body Variant Identification Code via RFID Transponder [-] *)

    (* Synchronized Robot Fleet Tool Center Point (TCP) Vector Speeds *)
    rRobot1_TCP_VectorSpeed             : REAL;     (* Robot 1 Hem Sealing TCP Vector Speed [m/s] *)
    rRobot2_TCP_VectorSpeed             : REAL;     (* Robot 2 Underbody Sealing TCP Vector Speed [m/s] *)
    rRobot3_TCP_VectorSpeed             : REAL;     (* Robot 3 Rocker Spray TCP Vector Speed [m/s] *)
    rRobot4_TCP_VectorSpeed             : REAL;     (* Robot 4 Wheel Arch Sealing TCP Vector Speed [m/s] *)
    rRobot5_TCP_VectorSpeed             : REAL;     (* Robot 5 Floor Pan LASD TCP Vector Speed [m/s] *)
    rRobot6_TCP_VectorSpeed             : REAL;     (* Robot 6 Tunnel LASD TCP Vector Speed [m/s] *)
    bRobotAllInInterferenceClear        : BOOL;     (* Robot Fleet Master Anti-Collision Zone Clear Flag [-] *)
    bNozzleWipeCompleted_R1             : BOOL;     (* Robot 1 Tip Cleaning Scraper Wipe Confirm [-] *)
    bNozzleWipeCompleted_R2             : BOOL;     (* Robot 2 Tip Cleaning Scraper Wipe Confirm [-] *)

    (* 2oo3 Triple Modular Redundancy (TMR) Pressure Channels *)
    rPVC_SupplyPressure_ChA             : REAL;     (* PVC Supply Header Pressure Transducer Ch A [bar] *)
    rPVC_SupplyPressure_ChB             : REAL;     (* PVC Supply Header Pressure Transducer Ch B [bar] *)
    rPVC_SupplyPressure_ChC             : REAL;     (* PVC Supply Header Pressure Transducer Ch C [bar] *)
    rLASD_SupplyPressure_ChA            : REAL;     (* LASD Supply Header Pressure Transducer Ch A [bar] *)
    rLASD_SupplyPressure_ChB            : REAL;     (* LASD Supply Header Pressure Transducer Ch B [bar] *)
    rLASD_SupplyPressure_ChC            : REAL;     (* LASD Supply Header Pressure Transducer Ch C [bar] *)

    (* 2oo3 TMR Shot Meter Encoder Channels *)
    rShotMeter1_LinearPos_ChA           : REAL;     (* PVC Shot Meter 1 Piston Linear Position Ch A [mm] *)
    rShotMeter1_LinearPos_ChB           : REAL;     (* PVC Shot Meter 1 Piston Linear Position Ch B [mm] *)
    rShotMeter1_LinearPos_ChC           : REAL;     (* PVC Shot Meter 1 Piston Linear Position Ch C [mm] *)
    rShotMeter2_LinearPos_ChA           : REAL;     (* LASD Shot Meter 2 Piston Linear Position Ch A [mm] *)
    rShotMeter2_LinearPos_ChB           : REAL;     (* LASD Shot Meter 2 Piston Linear Position Ch B [mm] *)
    rShotMeter2_LinearPos_ChC           : REAL;     (* LASD Shot Meter 2 Piston Linear Position Ch C [mm] *)

    (* 2oo3 TMR Coaxial Heated Hose Temperature Channels *)
    rHoseTemp_PVC_ChA                   : REAL;     (* Coaxial Heated Hose Temperature PVC Ch A [deg C] *)
    rHoseTemp_PVC_ChB                   : REAL;     (* Coaxial Heated Hose Temperature PVC Ch B [deg C] *)
    rHoseTemp_PVC_ChC                   : REAL;     (* Coaxial Heated Hose Temperature PVC Ch C [deg C] *)
    rHoseTemp_LASD_ChA                  : REAL;     (* Coaxial Heated Hose Temperature LASD Ch A [deg C] *)
    rHoseTemp_LASD_ChB                  : REAL;     (* Coaxial Heated Hose Temperature LASD Ch B [deg C] *)
    rHoseTemp_LASD_ChC                  : REAL;     (* Coaxial Heated Hose Temperature LASD Ch C [deg C] *)

    (* Real-Time 3D Optical Seam Tracking Inputs *)
    rLaserSeamTracker_dX                : REAL;     (* Optical 3D Laser Seam Tracking Offset Delta X [mm] *)
    rLaserSeamTracker_dY                : REAL;     (* Optical 3D Laser Seam Tracking Offset Delta Y [mm] *)
    rLaserSeamTracker_dZ                : REAL;     (* Optical 3D Laser Seam Tracking Offset Delta Z [mm] *)
    rLaserSeamTracker_GapWidth          : REAL;     (* Optical Laser Measured Hem Flange Gap Width [mm] *)
    bLaserSeamTracker_Valid             : BOOL;     (* Optical Seam Tracker Data Valid Quality Signal [-] *)

    (* In-Line Bead Profile & Film Thickness Metrology *)
    rOpticalBeadWidth_Sensor            : REAL;     (* Multi-Beam Laser Measured Bead Width [mm] *)
    rOpticalBeadHeight_Sensor           : REAL;     (* Multi-Beam Laser Measured Bead Height [mm] *)
    rOpticalLASD_FilmThickness          : REAL;     (* Multi-Beam Laser Measured LASD Film Thickness [mm] *)

    (* Bulk Material Unloader Ram Press Telemetry *)
    rExtruderRamDisplacement_PVC        : REAL;     (* Hydraulic Ram Follower Plate Displacement PVC [mm] *)
    rExtruderRamDisplacement_LASD       : REAL;     (* Hydraulic Ram Follower Plate Displacement LASD [mm] *)
    bBarrelDepletedSwitch_PVC           : BOOL;     (* PVC 200L Drum Low-Level Limit Switch [-] *)
    bBarrelDepletedSwitch_LASD          : BOOL;     (* LASD 1000L IBC Low-Level Limit Switch [-] *)
END_VAR
""")

    # -------------------------------------------------------------------------
    # VAR_OUTPUT DECLARATION (Actuator Commands, Telemetry Status Words)
    # -------------------------------------------------------------------------
    parts.append("""VAR_OUTPUT
    (* Bulk Material Hydraulic Ram Extruder Commands *)
    rPVC_RamExtruderPumpCmd             : REAL;     (* PVC Ram Pump Extruder Proportional Pressure Valve [0.0..100.0 %] *)
    rLASD_RamExtruderPumpCmd            : REAL;     (* LASD Ram Pump Extruder Proportional Pressure Valve [0.0..100.0 %] *)

    (* Shot Meter Servo Extrusion Velocity Commands *)
    rPVC_ShotMeter1_VelocityCmd         : REAL;     (* Robot 1 PVC Shot Meter Servo Velocity Setpoint [mm/s] *)
    rPVC_ShotMeter2_VelocityCmd         : REAL;     (* Robot 2 PVC Shot Meter Servo Velocity Setpoint [mm/s] *)
    rLASD_ShotMeter1_VelocityCmd        : REAL;     (* Robot 5 LASD Shot Meter Servo Velocity Setpoint [mm/s] *)
    rLASD_ShotMeter2_VelocityCmd        : REAL;     (* Robot 6 LASD Shot Meter Servo Velocity Setpoint [mm/s] *)

    (* Dispense Nozzle Needle & Swirl Valve Lift Commands *)
    rPVC_NozzleNeedleValveCmd_R1        : REAL;     (* Robot 1 Dispense Nozzle Proportional Needle Lift [0.0..100.0 %] *)
    rPVC_NozzleNeedleValveCmd_R2        : REAL;     (* Robot 2 Dispense Nozzle Proportional Needle Lift [0.0..100.0 %] *)
    rPVC_NozzleNeedleValveCmd_R3        : REAL;     (* Robot 3 Rocker Spray Swirl Proportional Valve [0.0..100.0 %] *)
    rPVC_NozzleNeedleValveCmd_R4        : REAL;     (* Robot 4 Wheel Arch Nozzle Needle Lift [0.0..100.0 %] *)
    rLASD_NozzleDispenseCmd_R5          : REAL;     (* Robot 5 LASD Swirl Applicator Flow Valve [0.0..100.0 %] *)
    rLASD_NozzleDispenseCmd_R6          : REAL;     (* Robot 6 LASD Swirl Applicator Flow Valve [0.0..100.0 %] *)

    (* Thermal Conditioning & Heated Hose PWM Commands *)
    rHeatedHose_PWMDuty_PVC             : REAL;     (* Coaxial Heated Hose PWM Heating Duty Cycle PVC [0.0..100.0 %] *)
    rHeatedHose_PWMDuty_LASD            : REAL;     (* Coaxial Heated Hose PWM Heating Duty Cycle LASD [0.0..100.0 %] *)

    (* Fast Depressurization Dump & Tooling Solenoid Valves *)
    bPVC_FastDumpValveCmd               : BOOL;     (* PVC Safe Depressurization Fast Dump Valve Solenoid [-] *)
    bLASD_FastDumpValveCmd              : BOOL;     (* LASD Safe Depressurization Fast Dump Valve Solenoid [-] *)
    bSkidLifterClampEngageCmd           : BOOL;     (* Body Skid Precision Clamp Actuation Solenoid [-] *)
    bSkidLifterLowerCmd                 : BOOL;     (* Body Skid Precision Lifter Retraction Solenoid [-] *)
    bSkidTransferAdvancePermissive      : BOOL;     (* Conveyor Permissive to PVC Gelling Oven [-] *)
    bRobotFleetRunPermissive            : BOOL;     (* Master Robot Motion Enable Permissive Interlock [-] *)

    (* Dynamic Seam Tracking Correction Outputs *)
    rRobotSeamCorrection_dX             : REAL;     (* Real-Time Seam Correction Delta X to Robot Controllers [mm] *)
    rRobotSeamCorrection_dY             : REAL;     (* Real-Time Seam Correction Delta Y to Robot Controllers [mm] *)
    rRobotSeamCorrection_dZ             : REAL;     (* Real-Time Seam Correction Delta Z to Robot Controllers [mm] *)

    (* In-Line Quality Metrology Results *)
    rCalculatedBeadArea                 : REAL;     (* Instantaneous Dispensed Bead Cross-Sectional Area [mm2] *)
    rCalculatedLASD_MassDensity         : REAL;     (* Instantaneous Applied LASD Areal Mass Density [kg/m2] *)
    bCycleCompletedPass                 : BOOL;     (* Car Body Sealing & Dampening Cycle Completed PASS [-] *)
    bCycleCompletedReject               : BOOL;     (* Car Body Sealing Cycle REJECT Metrology Shortfall [-] *)

    (* State Machine & Telemetry Status Words *)
    uiCurrentState                      : UINT;     (* 12-Stage Operational Finite State Machine State Code [-] *)
    dwSystemStatusWord                  : DWORD;    (* Master System Operational Status Telemetry Bit-Field [-] *)
    dwDispenseStatusWord                : DWORD;    (* Fluid Dispensing & Extrusion Subsystem Telemetry [-] *)
    dwRobotCoordinationWord             : DWORD;    (* Robot Fleet Synchronization & Seam Tracking Telemetry [-] *)
    dwTMRDiscrepancyWord                : DWORD;    (* 2oo3 TMR Sensor Voting Discrepancy Bit-Field [-] *)
    dwISA182AlarmWord_PVC               : DWORD;    (* ISA-18.2 Prioritized Alarm Matrix PVC Circuit [-] *)
    dwISA182AlarmWord_LASD              : DWORD;    (* ISA-18.2 Prioritized Alarm Matrix LASD Circuit [-] *)
    dwMetrologyStatusWord               : DWORD;    (* Bead Metrology & Acoustic Density Inspection Results [-] *)
END_VAR
""")

    # -------------------------------------------------------------------------
    # VAR DECLARATION (Matrices, State Vectors, Filters, Timers, Internal Vars)
    # -------------------------------------------------------------------------
    parts.append("""VAR
    (* Discrete State-Space Model Matrices (Sample Time dt = 2.0 ms) *)
    arrA                                : ARRAY[1..16, 1..16] OF REAL;  (* State Transition Matrix A (16x16) *)
    arrB                                : ARRAY[1..16, 1..8] OF REAL;   (* Input Coupling Matrix B (16x8) *)
    arrC                                : ARRAY[1..8, 1..16] OF REAL;   (* Measurement Matrix C (8x16) *)
    arrD                                : ARRAY[1..8, 1..8] OF REAL;    (* Feedthrough Matrix D (8x8) *)
    arrStateVector                      : ARRAY[1..16] OF REAL;         (* State Vector x[k] *)
    arrNextStateVector                  : ARRAY[1..16] OF REAL;         (* Predicted State Vector x[k+1] *)
    arrControlInputs                    : ARRAY[1..8] OF REAL;          (* Control Input Vector u[k] *)
    arrSystemOutputs                    : ARRAY[1..8] OF REAL;          (* System Output Vector y[k] *)

    (* Model Predictive Control (MPC) Cost Weighting Matrices & References *)
    arrQ_Weights                        : ARRAY[1..16] OF REAL;         (* State Penalty Weights Q (Diagonal 16x16) *)
    arrR_Weights                        : ARRAY[1..8] OF REAL;          (* Actuator Effort Penalty Weights R (Diagonal 8x8) *)
    arrP_Weights                        : ARRAY[1..16] OF REAL;         (* Terminal State Penalty Weights P (Diagonal 16x16) *)
    arrStateRef                         : ARRAY[1..16] OF REAL;         (* Dynamic State Reference Vector x_ref *)
    arrMPC_Gradient                     : ARRAY[1..8] OF REAL;          (* Projected Gradient Vector nabla J *)
    arrU_MinLimits                      : ARRAY[1..8] OF REAL;          (* Actuator Minimum Hard Saturation Limits *)
    arrU_MaxLimits                      : ARRAY[1..8] OF REAL;          (* Actuator Maximum Hard Saturation Limits *)
    arrU_RateLimits                     : ARRAY[1..8] OF REAL;          (* Maximum Slew-Rate Limits [units/s] *)
    arrPrevControlInputs                : ARRAY[1..8] OF REAL;          (* Previous Sample Control Inputs u[k-1] *)

    (* 2oo3 Triple Modular Redundancy (TMR) Intermediate Voted Variables *)
    rVoted_PVC_SupplyPressure           : REAL;     (* Voted PVC Supply Header Pressure [bar] *)
    rVoted_LASD_SupplyPressure          : REAL;     (* Voted LASD Supply Header Pressure [bar] *)
    rVoted_ShotMeter1_Pos               : REAL;     (* Voted Shot Meter 1 Linear Position [mm] *)
    rVoted_ShotMeter2_Pos               : REAL;     (* Voted Shot Meter 2 Linear Position [mm] *)
    rVoted_HoseTemp_PVC                 : REAL;     (* Voted Heated Hose Temperature PVC [deg C] *)
    rVoted_HoseTemp_LASD                : REAL;     (* Voted Heated Hose Temperature LASD [deg C] *)
    rVoted_LaserSeamTracker_dZ          : REAL;     (* Voted Wrist Laser Seam Height Offset [mm] *)

    (* TMR Discrepancy Debounce Timers & Fault Persistence Counters *)
    tTMR_Timer_PVCPressure              : TIME;     (* PVC Pressure Discrepancy Persistence Timer *)
    tTMR_Timer_LASDPressure             : TIME;     (* LASD Pressure Discrepancy Persistence Timer *)
    tTMR_Timer_ShotMeter1Pos            : TIME;     (* Shot Meter 1 Discrepancy Persistence Timer *)
    tTMR_Timer_ShotMeter2Pos            : TIME;     (* Shot Meter 2 Discrepancy Persistence Timer *)
    tTMR_Timer_HoseTempPVC              : TIME;     (* Hose Temp PVC Discrepancy Persistence Timer *)
    tTMR_Timer_HoseTempLASD             : TIME;     (* Hose Temp LASD Discrepancy Persistence Timer *)
    bChannelHealthy_PVCPres_A           : BOOL;     (* Sensor Channel A Health Flag - PVC Pressure *)
    bChannelHealthy_PVCPres_B           : BOOL;     (* Sensor Channel B Health Flag - PVC Pressure *)
    bChannelHealthy_PVCPres_C           : BOOL;     (* Sensor Channel C Health Flag - PVC Pressure *)
    bChannelHealthy_LASDPres_A          : BOOL;     (* Sensor Channel A Health Flag - LASD Pressure *)
    bChannelHealthy_LASDPres_B          : BOOL;     (* Sensor Channel B Health Flag - LASD Pressure *)
    bChannelHealthy_LASDPres_C          : BOOL;     (* Sensor Channel C Health Flag - LASD Pressure *)

    (* Non-Newtonian Rheology & Compressibility Internal Variables *)
    rCalculatedShearRate_PVC            : REAL;     (* Apparent Shear Rate in Dispense Nozzle [1/s] *)
    rCalculatedShearRate_LASD           : REAL;     (* Apparent Shear Rate in LASD Applicator [1/s] *)
    rDynamicViscosity_PVC               : REAL;     (* Temperature-Corrected Apparent Viscosity PVC [mPa s] *)
    rDynamicViscosity_LASD              : REAL;     (* Temperature-Corrected Apparent Viscosity LASD [mPa s] *)
    rEffectiveBulkModulus_PVC           : REAL;     (* Combined Fluid-Hose Effective Bulk Modulus PVC [bar] *)
    rEffectiveBulkModulus_LASD          : REAL;     (* Combined Fluid-Hose Effective Bulk Modulus LASD [bar] *)
    rFluidFrictionPressureDrop_PVC      : REAL;     (* Non-Newtonian Hydraulic Friction Pressure Loss [bar] *)

    (* Dynamic Flow-to-Speed Pacing & Snuff-Back Variables *)
    rNominalTargetBeadArea              : REAL;     (* Target Bead Cross-Section from Recipe [mm2] *)
    rNominalTargetLASD_Area             : REAL;     (* Target LASD Film Cross-Section from Recipe [mm2] *)
    rTargetVolumetricFlowRate_PVC       : REAL;     (* Dynamic Target Volumetric Flow Rate PVC [ml/s] *)
    rTargetVolumetricFlowRate_LASD      : REAL;     (* Dynamic Target Volumetric Flow Rate LASD [ml/s] *)
    rPreOpenLeadTime_Comp               : REAL;     (* Dynamic Needle Pre-Opening Lead Advance [s] *)
    rSnuffBackReverseVolume             : REAL;     (* Calibrated Reverse Decompression Volume [ml] *)
    rSnuffBackPistonDisplacement        : REAL;     (* Calibrated Reverse Piston Stroke [mm] *)
    bSnuffBackActive                    : BOOL;     (* Sub-10ms Suck-Back Piston Deceleration Active [-] *)
    tSnuffBackTimer                     : TIME;     (* High-Speed Suck-Back Duration Timer *)
    rFilteredRobotTCP_Speed             : REAL;     (* 1st-Order Low-Pass Filtered Robot TCP Speed [m/s] *)
    rPreviousRobotTCP_Speed             : REAL;     (* Previous Sample Robot TCP Speed for dv/dt Calc [m/s] *)
    rCalculatedRobotTCP_Accel           : REAL;     (* Calculated Robot TCP Acceleration [m/s2] *)

    (* Real-Time Optical 3D Seam Tracking Filtering & Superposition *)
    rFilteredSeam_dX                    : REAL;     (* Low-Pass Filtered Seam Tracking Offset Delta X [mm] *)
    rFilteredSeam_dY                    : REAL;     (* Low-Pass Filtered Seam Tracking Offset Delta Y [mm] *)
    rFilteredSeam_dZ                    : REAL;     (* Low-Pass Filtered Seam Tracking Offset Delta Z [mm] *)
    rFilteredFlangeGapWidth             : REAL;     (* Low-Pass Filtered Hem Flange Gap Width [mm] *)

    (* 12-Stage Operational Finite State Machine State & Transition Registers *)
    nFSM_State                          : UINT;     (* Internal Active FSM State Index (0..12) *)
    nFSM_PrevState                      : UINT;     (* Previous Sample FSM State Index *)
    tStateTimer                         : TIME;     (* Elapsed Dwell Time in Active State *)
    bStateStepCompleted                 : BOOL;     (* Handshake Step Done Flag within Active State *)
    uiLoadedVariantIndex                : UINT;     (* Active Vehicle Body Variant Recipe Index (1..4) *)
    tLifterClampTimeoutTimer            : TIME;     (* Skid Lifter Pin Engagement Timeout Timer *)
    tNozzleWipeDwellTimer               : TIME;     (* Mechanical Tip Scraper Dwell Timer *)
    tPreFlightScanTimer                 : TIME;     (* Laser Seam Pre-Flight Verification Timer *)
    tDispenseExecutionTimer             : TIME;     (* Active Seam Sealing & LASD Dispense Timer *)
    tMetrologyScanTimer                 : TIME;     (* In-Line Optical Inspection Pass Timer *)
    tAutoPurgeIdleTimer                 : TIME;     (* Nozzle Inactivity Auto-Purge Trigger Timer *)
    tBarrelChangeoverTimer              : TIME;     (* Drum Depletion & Follower Plate Vent Timer *)
    tDepressurizationDumpTimer          : TIME;     (* Emergency E-Stop Hydraulic Bleed Timer *)

    (* Vehicle Body Variant Recipe Parameters *)
    rRecipe_BeadWidth                   : REAL;     (* Recipe Specified Nominal Bead Width [mm] *)
    rRecipe_BeadHeight                  : REAL;     (* Recipe Specified Nominal Bead Height [mm] *)
    rRecipe_LASD_Thickness              : REAL;     (* Recipe Specified Nominal LASD Film Thickness [mm] *)
    rRecipe_LASD_Width                  : REAL;     (* Recipe Specified Nominal LASD Swirl Strip Width [mm] *)
    rRecipe_NominalSeamLength           : REAL;     (* Recipe Programmed Total Seam Length [mm] *)
    rRecipe_GapToleranceLimit           : REAL;     (* Maximum Allowable Flange Gap Before Abort [mm] *)

    (* Metrology Cumulative Statistics & Quality Verification *)
    rMetrologySum_BeadWidth             : REAL;     (* Cumulative Sum of Laser Measured Bead Width [mm] *)
    rMetrologySum_BeadHeight            : REAL;     (* Cumulative Sum of Laser Measured Bead Height [mm] *)
    rMetrologySum_LASD_Thick            : REAL;     (* Cumulative Sum of Measured LASD Thickness [mm] *)
    diMetrologySampleCount              : DINT;     (* Metrology Sensor Valid Sample Accumulator *)
    rCalculatedMeanBeadWidth            : REAL;     (* Computed Statistical Mean Bead Width [mm] *)
    rCalculatedMeanBeadHeight           : REAL;     (* Computed Statistical Mean Bead Height [mm] *)
    rCalculatedMeanLASD_Thick           : REAL;     (* Computed Statistical Mean LASD Thickness [mm] *)
    bBeadContinuousNoSkips              : BOOL;     (* Bead Continuity Inspection Result Flag *)
    bLASDAcousticCoveragePass           : BOOL;     (* LASD Areal Density Quality Flag *)

    (* ISA-18.2 Alarm Deadbands, Debounce Timers, and Latches *)
    tAlarmDebounce_PVCOverPresHH        : TIME;     (* Debounce Timer: PVC Pressure High-High (>260 bar) *)
    tAlarmDebounce_LASDOverPresHH       : TIME;     (* Debounce Timer: LASD Pressure High-High (>250 bar) *)
    tAlarmDebounce_PVCHoseOverTempHH    : TIME;     (* Debounce Timer: PVC Hose Temp High-High (>38 deg C) *)
    tAlarmDebounce_LASDHoseOverTempHH   : TIME;     (* Debounce Timer: LASD Hose Temp High-High (>38 deg C) *)
    tAlarmDebounce_BeadWidthReject      : TIME;     (* Debounce Timer: Bead Width Shortfall Reject *)
    tAlarmDebounce_CollisionInterlock   : TIME;     (* Debounce Timer: Robot Collision Zone Violation *)

    (* Loop Counters, Array Indices, & Mathematical Intermediate Variables *)
    iIndex                              : INT;      (* Generic Primary Loop Index *)
    jIndex                              : INT;      (* Generic Secondary Loop Index *)
    kIndex                              : INT;      (* Prediction Horizon Stage Index *)
    rTempDotProduct                     : REAL;     (* Matrix-Vector Dot Product Accumulator *)
    rTempQuadraticCost                  : REAL;     (* MPC Quadratic Cost Accumulator *)
    rStateDeviation                     : REAL;     (* State Error Against Reference *)
    rDeltaTime_Seconds                  : REAL;     (* Discrete Sample Cycle Time dt = 0.002 s *)
    bMatricesInitialized                : BOOL;     (* One-Time State Space Matrix Initialization Latch *)
END_VAR
""")

    # -------------------------------------------------------------------------
    # INITIALIZATION: STATE-SPACE & MPC MATRICES (Unrolled 16x16, 16x8, etc.)
    # -------------------------------------------------------------------------
    parts.append("""(* ==================================================================================== *)
(* ONE-TIME DISCRETE STATE-SPACE (16x16) & MPC WEIGHT MATRIX INITIALIZATION             *)
(* Sample Time Delta t = 2.0 ms (500 Hz Execution Rate). Non-zero coefficients derived   *)
(* from Navier-Stokes non-Newtonian conduit flow, hydraulic bulk modulus, and servo dyn *)
(* ==================================================================================== *)
IF NOT bMatricesInitialized THEN
    rDeltaTime_Seconds := 0.002; (* 2.0 milliseconds discrete execution period *)

    (* Clear entire 16x16 Matrix A to Zero *)
    FOR iIndex := 1 TO 16 DO
        FOR jIndex := 1 TO 16 DO
            arrA[iIndex, jIndex] := 0.0;
        END_FOR;
    END_FOR;

    (* Row 1: PVC Main Header Supply Pressure P_hdr_PVC dynamics *)
    arrA[1, 1] := 0.9650;   (* Pressure storage relaxation via accumulator & hose capacitance *)
    arrA[1, 2] := -0.0450;  (* Pressure drop coupled to header volumetric discharge flow *)
    arrA[1, 7] := -0.0180;  (* Acoustic backpressure coupling from Robot 1 dispense nozzle *)
    arrA[1, 15] := 0.0120;  (* Thermal expansion pressure elevation coefficient *)

    (* Row 2: PVC Main Header Flow Rate Q_hdr_PVC dynamics *)
    arrA[2, 1] := 0.0820;   (* Pressure gradient acceleration along primary distribution pipe *)
    arrA[2, 2] := 0.8950;   (* Viscous dissipation damping along hydraulic line *)
    arrA[2, 8] := -0.0350;  (* Flow diversion downstream into Robot 1 shot meter cylinder *)
    arrA[2, 15] := 0.0080;  (* Viscosity thinning flow acceleration with temperature *)

    (* Row 3: LASD Main Header Supply Pressure P_hdr_LASD dynamics *)
    arrA[3, 3] := 0.9580;   (* High-viscosity resin pressure retention in 1000L IBC line *)
    arrA[3, 4] := -0.0520;  (* Pressure drop coupled to LASD volumetric delivery rate *)
    arrA[3, 11] := -0.0220; (* Backpressure coupling from Robot 5 LASD applicator head *)
    arrA[3, 15] := 0.0110;  (* Thermal fluid compliance coefficient *)

    (* Row 4: LASD Main Header Flow Rate Q_hdr_LASD dynamics *)
    arrA[4, 3] := 0.0760;   (* Hydraulic driving pressure head *)
    arrA[4, 4] := 0.8820;   (* Fluid inertial and wall shear dissipation damping *)
    arrA[4, 12] := -0.0420; (* Volumetric sink into Robot 5 positive displacement shot meter *)
    arrA[4, 15] := 0.0095;  (* Temperature shear-thinning mobility gain *)

    (* Row 5: Robot 1 PVC Shot Meter 1 Piston Linear Position x_sm1 *)
    arrA[5, 5] := 1.0000;   (* Pure kinematic kinematic integrator: x[k+1] = x[k] + dt * v[k] *)
    arrA[5, 6] := 0.0020;   (* Delta t = 0.002 seconds velocity integration factor *)

    (* Row 6: Robot 1 PVC Shot Meter 1 Piston Linear Velocity v_sm1 *)
    arrA[6, 6] := 0.9250;   (* Ballscrew electromechanical drive viscous damping *)
    arrA[6, 7] := -0.0150;  (* Fluid reaction backpressure load opposing piston travel *)
    arrA[6, 14] := -0.0080; (* Wrist flexural vibration transmission into shot meter carriage *)

    (* Row 7: Robot 1 Dispense Nozzle Chamber Pressure P_noz_PVC1 *)
    arrA[7, 1] := 0.0240;   (* Upstream header pressure wave transmission through heated hose *)
    arrA[7, 6] := 0.1650;   (* Piston positive displacement volumetric compression gain *)
    arrA[7, 7] := 0.8850;   (* Nozzle chamber fluid capacitance decay *)
    arrA[7, 8] := -0.1420;  (* Hydrodynamic pressure relief via orifice discharge flow *)

    (* Row 8: Robot 1 Dispense Nozzle Flow Rate Q_noz_PVC1 *)
    arrA[8, 7] := 0.1180;   (* Bernoulli-Poiseuille orifice differential pressure driving force *)
    arrA[8, 8] := 0.7950;   (* Viscous shear restriction and entrance momentum dissipation *)
    arrA[8, 15] := 0.0150;  (* Fluid viscosity reduction accelerating orifice flow *)
    arrA[8, 16] := -0.0060; (* Bead back-stress backpressure coupling at hem flange surface *)

    (* Row 9: Robot 5 LASD Shot Meter 2 Piston Linear Position x_sm2 *)
    arrA[9, 9] := 1.0000;   (* Kinematic integrator for acoustic deadener shot meter *)
    arrA[9, 10] := 0.0020;  (* Delta t = 0.002 seconds position integration *)

    (* Row 10: Robot 5 LASD Shot Meter 2 Piston Linear Velocity v_sm2 *)
    arrA[10, 10] := 0.9180; (* Linear servo motor velocity loop damping *)
    arrA[10, 11] := -0.0185;(* High-yield stress LASD reaction force on large piston face *)
    arrA[10, 14] := -0.0090;(* Heavy applicator wrist flexural compliance coupling *)

    (* Row 11: Robot 5 LASD Applicator Pressure P_noz_LASD *)
    arrA[11, 3] := 0.0210;  (* Upstream bulk IBC supply coupling *)
    arrA[11, 10] := 0.1850; (* Shot meter piston positive volume displacement driving gain *)
    arrA[11, 11] := 0.8720; (* Applicator manifold fluid capacitance *)
    arrA[11, 12] := -0.1550;(* Discharge pressure drop across multi-hole swirl nozzle *)

    (* Row 12: Robot 5 LASD Applicator Flow Rate Q_noz_LASD *)
    arrA[12, 11] := 0.1250; (* Discharge pressure head across applicator swirl chamber *)
    arrA[12, 12] := 0.7820; (* Pseudoplastic viscous shear restriction *)
    arrA[12, 15] := 0.0180; (* Thermal fluid softening gain *)

    (* Row 13: Robot Wrist Seam Tracking Trajectory Error Delta e_track *)
    arrA[13, 13] := 0.8400; (* 250 Hz Optical seam tracking visual servoing closed-loop pole *)
    arrA[13, 14] := 0.0650; (* Arm flexural deformation directly translating into tracking offset *)

    (* Row 14: Robot Arm Structural Flexural Deflection delta_arm *)
    arrA[14, 7] := 0.0045;  (* PVC Dispense tip reaction force bending moments on robot wrist *)
    arrA[14, 11] := 0.0060; (* LASD High-pressure swirl applicator thrust reaction *)
    arrA[14, 14] := 0.7650; (* Robot arm second-order structural mode flexural damping *)

    (* Row 15: Coaxial Heated Hose Temperature T_hose *)
    arrA[15, 1] := 0.0015;  (* Viscous dissipation frictional heating under high shear *)
    arrA[15, 15] := 0.9880; (* Thermal insulation heat retention time constant (tau = ~160 s) *)

    (* Row 16: Dispensed Bead Cross-Sectional Area A_bead *)
    arrA[16, 8] := 0.0480;  (* Volumetric deposit accumulation rate: A = Q / v_TCP *)
    arrA[16, 13] := -0.0120;(* Bead spread widening due to lateral seam tracking deviation *)
    arrA[16, 16] := 0.7200; (* Viscoelastic surface tension & slump settling dynamics *)

    (* Clear entire 16x8 Input Matrix B to Zero *)
    FOR iIndex := 1 TO 16 DO
        FOR jIndex := 1 TO 8 DO
            arrB[iIndex, jIndex] := 0.0;
        END_FOR;
    END_FOR;

    (* Populate Input Matrix B Coefficients *)
    arrB[1, 1] := 0.2850;   (* u1: PVC Ram Extruder Pump Valve -> Header Pressure *)
    arrB[2, 1] := 0.1950;   (* u1: PVC Ram Extruder Pump Valve -> Header Flow *)
    arrB[3, 2] := 0.3100;   (* u2: LASD Ram Extruder Pump Valve -> Header Pressure *)
    arrB[4, 2] := 0.2250;   (* u2: LASD Ram Extruder Pump Valve -> Header Flow *)
    arrB[6, 3] := 0.4500;   (* u3: PVC Shot Meter Velocity Command -> Piston Acceleration *)
    arrB[7, 3] := 0.0850;   (* u3: PVC Shot Meter Velocity Command -> Direct Chamber Pressure *)
    arrB[7, 4] := -0.0650;  (* u4: PVC Dispense Needle Lift -> Pressure Drop Reliever *)
    arrB[8, 4] := 0.3850;   (* u4: PVC Dispense Needle Lift -> Orifice Discharge Flow *)
    arrB[10, 5] := 0.4400;  (* u5: LASD Shot Meter Velocity Command -> Piston Acceleration *)
    arrB[11, 5] := 0.0950;  (* u5: LASD Shot Meter Velocity Command -> Chamber Pressure *)
    arrB[11, 6] := -0.0750; (* u6: LASD Applicator Swirl Valve -> Pressure Drop *)
    arrB[12, 6] := 0.4200;  (* u6: LASD Applicator Swirl Valve -> Swirl Discharge Flow *)
    arrB[15, 7] := 0.0650;  (* u7: Coaxial Heated Hose PWM Duty -> Temperature Rise *)
    arrB[13, 8] := -0.0280; (* u8: Robot TCP Speed Feedforward -> Tracking Lag Compensation *)
    arrB[16, 8] := -0.0520; (* u8: Robot TCP Speed -> Bead Thinning Dilution (A = Q / v) *)

    (* Clear entire 8x16 Output Matrix C to Zero *)
    FOR iIndex := 1 TO 8 DO
        FOR jIndex := 1 TO 16 DO
            arrC[iIndex, jIndex] := 0.0;
        END_FOR;
    END_FOR;

    (* Populate Output Matrix C Coefficients: y[k] = C * x[k] *)
    arrC[1, 1] := 1.0000;   (* y1: Voted PVC Header Pressure Measurement *)
    arrC[2, 3] := 1.0000;   (* y2: Voted LASD Header Pressure Measurement *)
    arrC[3, 5] := 1.0000;   (* y3: Voted Shot Meter 1 Piston Displacement *)
    arrC[4, 7] := 1.0000;   (* y4: PVC Dispense Tip Pressure *)
    arrC[5, 9] := 1.0000;   (* y5: Voted Shot Meter 2 Piston Displacement *)
    arrC[6, 11] := 1.0000;  (* y6: LASD Applicator Chamber Pressure *)
    arrC[7, 15] := 1.0000;  (* y7: Coaxial Heated Hose Fluid Temperature *)
    arrC[8, 16] := 1.0000;  (* y8: Measured Dispensed Bead Cross-Sectional Area *)

    (* Clear entire 8x8 Direct Feedthrough Matrix D to Zero *)
    FOR iIndex := 1 TO 8 DO
        FOR jIndex := 1 TO 8 DO
            arrD[iIndex, jIndex] := 0.0;
        END_FOR;
    END_FOR;

    (* Direct feedthrough terms: high-frequency valve acoustic transmission *)
    arrD[4, 4] := 0.0250;   (* Needle crack direct pressure transmission *)
    arrD[6, 6] := 0.0300;   (* Swirl valve crack direct pressure transmission *)
    arrD[8, 8] := -0.0120;  (* Immediate TCP acceleration bead thinning *)

    (* Initialize Model Predictive Control (MPC) Cost Weighting Vectors *)
    (* State penalty vector Q: prioritize nozzle pressures, pacing flow, bead area *)
    arrQ_Weights[1]  := 0.15;  (* x1: PVC Header Pressure *)
    arrQ_Weights[2]  := 0.08;  (* x2: PVC Header Flow *)
    arrQ_Weights[3]  := 0.15;  (* x3: LASD Header Pressure *)
    arrQ_Weights[4]  := 0.08;  (* x4: LASD Header Flow *)
    arrQ_Weights[5]  := 0.25;  (* x5: Shot Meter 1 Position *)
    arrQ_Weights[6]  := 0.35;  (* x6: Shot Meter 1 Velocity *)
    arrQ_Weights[7]  := 1.85;  (* x7: PVC Nozzle Chamber Pressure (Critical Pacing) *)
    arrQ_Weights[8]  := 2.50;  (* x8: PVC Nozzle Flow Rate (Critical Bead Uniformity) *)
    arrQ_Weights[9]  := 0.25;  (* x9: Shot Meter 2 Position *)
    arrQ_Weights[10] := 0.35;  (* x10: Shot Meter 2 Velocity *)
    arrQ_Weights[11] := 1.65;  (* x11: LASD Applicator Chamber Pressure *)
    arrQ_Weights[12] := 2.20;  (* x12: LASD Discharge Flow Rate *)
    arrQ_Weights[13] := 1.50;  (* x13: Robot Seam Tracking Alignment Error *)
    arrQ_Weights[14] := 0.45;  (* x14: Robot Arm Flexural Vibration *)
    arrQ_Weights[15] := 0.90;  (* x15: Heated Hose Thermal Setpoint 28.0 deg C *)
    arrQ_Weights[16] := 3.20;  (* x16: Dispensed Bead Area (Highest Metrology Priority) *)

    (* Actuator effort penalty vector R: penalize violent valve chatter & motor stress *)
    arrR_Weights[1]  := 0.12;  (* u1: PVC Ram Pump Valve *)
    arrR_Weights[2]  := 0.12;  (* u2: LASD Ram Pump Valve *)
    arrR_Weights[3]  := 0.05;  (* u3: PVC Shot Meter Servo Velocity *)
    arrR_Weights[4]  := 0.18;  (* u4: PVC Dispense Needle Lift *)
    arrR_Weights[5]  := 0.05;  (* u5: LASD Shot Meter Servo Velocity *)
    arrR_Weights[6]  := 0.15;  (* u6: LASD Applicator Swirl Valve *)
    arrR_Weights[7]  := 0.25;  (* u7: Hose Heating PWM Duty *)
    arrR_Weights[8]  := 0.02;  (* u8: Robot TCP Speed Tracking *)

    (* Terminal state penalty vector P: Lyapunov stability terminal cost *)
    FOR iIndex := 1 TO 16 DO
        arrP_Weights[iIndex] := arrQ_Weights[iIndex] * 2.85;
    END_FOR;

    (* Actuator Physical Hard Saturation Bounds *)
    arrU_MinLimits[1] := 0.0;    arrU_MaxLimits[1] := 100.0;   (* PVC Ram Valve: 0-100% *)
    arrU_MinLimits[2] := 0.0;    arrU_MaxLimits[2] := 100.0;   (* LASD Ram Valve: 0-100% *)
    arrU_MinLimits[3] := -150.0; arrU_MaxLimits[3] := 250.0;   (* PVC Shot Meter: -150 to +250 mm/s *)
    arrU_MinLimits[4] := 0.0;    arrU_MaxLimits[4] := 100.0;   (* PVC Needle Lift: 0-100% *)
    arrU_MinLimits[5] := -150.0; arrU_MaxLimits[5] := 250.0;   (* LASD Shot Meter: -150 to +250 mm/s *)
    arrU_MinLimits[6] := 0.0;    arrU_MaxLimits[6] := 100.0;   (* LASD Swirl Valve: 0-100% *)
    arrU_MinLimits[7] := 0.0;    arrU_MaxLimits[7] := 100.0;   (* Heated Hose PWM: 0-100% *)
    arrU_MinLimits[8] := 0.0;    arrU_MaxLimits[8] := 2000.0;  (* Robot TCP Speed: 0-2000 mm/s *)

    (* Slew-Rate Limits [units / second] *)
    arrU_RateLimits[1] := 120.0;  (* Ram Valve: max 120% / s *)
    arrU_RateLimits[2] := 120.0;  (* Ram Valve: max 120% / s *)
    arrU_RateLimits[3] := 1200.0; (* Shot Meter Servo Accel: 1200 mm/s^2 *)
    arrU_RateLimits[4] := 450.0;  (* Fast Pneumatic/Piezo Needle: 450% / s *)
    arrU_RateLimits[5] := 1200.0; (* Shot Meter Servo Accel: 1200 mm/s^2 *)
    arrU_RateLimits[6] := 400.0;  (* Swirl Valve: 400% / s *)
    arrU_RateLimits[7] := 25.0;   (* Thermal PWM Duty Rate: 25% / s *)
    arrU_RateLimits[8] := 3500.0; (* Robot Acceleration Limit: 3500 mm/s^2 *)

    (* Initialize State Vectors to Factory Nominal Conditions *)
    FOR iIndex := 1 TO 16 DO
        arrStateVector[iIndex] := 0.0;
        arrNextStateVector[iIndex] := 0.0;
        arrStateRef[iIndex] := 0.0;
    END_FOR;
    FOR jIndex := 1 TO 8 DO
        arrControlInputs[jIndex] := 0.0;
        arrPrevControlInputs[jIndex] := 0.0;
        arrSystemOutputs[jIndex] := 0.0;
        arrMPC_Gradient[jIndex] := 0.0;
    END_FOR;

    arrStateVector[1] := 185.0; (* Nominal PVC Header Pressure: 185 bar *)
    arrStateVector[3] := 160.0; (* Nominal LASD Header Pressure: 160 bar *)
    arrStateVector[15] := 28.0; (* Nominal Conditioned Fluid Temperature: 28.0 deg C *)

    bMatricesInitialized := TRUE;
END_IF;
""")

    # -------------------------------------------------------------------------
    # PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) VOTING ARCHITECTURE
    # -------------------------------------------------------------------------
    parts.append("""(* ==================================================================================== *)
(* PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING & DISCREPANCY AUDITING    *)
(* Evaluates three independent measurement channels per critical safety variable.       *)
(* Incorporates out-of-range sensor health gating, median selection, pairwise tolerance   *)
(* discrepancy timers (50 ms persistence), and bumpless degradation to 1oo2 or freeze. *)
(* ==================================================================================== *)

(* Clear TMR Diagnostic Bit-Field at beginning of evaluation cycle *)
dwTMRDiscrepancyWord := 16#00000000;

(* --- 1.1 PVC HEADER SUPPLY PRESSURE 2oo3 TMR VOTING --- *)
(* Sensor Health Range Checks: 4-20 mA wire-break detection (< 5.0 bar or > 320.0 bar) *)
bChannelHealthy_PVCPres_A := (rPVC_SupplyPressure_ChA >= 5.0) AND (rPVC_SupplyPressure_ChA <= 320.0);
bChannelHealthy_PVCPres_B := (rPVC_SupplyPressure_ChB >= 5.0) AND (rPVC_SupplyPressure_ChB <= 320.0);
bChannelHealthy_PVCPres_C := (rPVC_SupplyPressure_ChC >= 5.0) AND (rPVC_SupplyPressure_ChC <= 320.0);

(* Pairwise Discrepancy Evaluation against 12.0 bar maximum permissible inter-channel spread *)
IF bChannelHealthy_PVCPres_A AND bChannelHealthy_PVCPres_B AND bChannelHealthy_PVCPres_C THEN
    (* All three channels healthy: Execute True Median Selection *)
    IF ((rPVC_SupplyPressure_ChA >= rPVC_SupplyPressure_ChB) AND (rPVC_SupplyPressure_ChA <= rPVC_SupplyPressure_ChC)) OR
       ((rPVC_SupplyPressure_ChA <= rPVC_SupplyPressure_ChB) AND (rPVC_SupplyPressure_ChA >= rPVC_SupplyPressure_ChC)) THEN
        rVoted_PVC_SupplyPressure := rPVC_SupplyPressure_ChA;
    ELSIF ((rPVC_SupplyPressure_ChB >= rPVC_SupplyPressure_ChA) AND (rPVC_SupplyPressure_ChB <= rPVC_SupplyPressure_ChC)) OR
          ((rPVC_SupplyPressure_ChB <= rPVC_SupplyPressure_ChA) AND (rPVC_SupplyPressure_ChB >= rPVC_SupplyPressure_ChC)) THEN
        rVoted_PVC_SupplyPressure := rPVC_SupplyPressure_ChB;
    ELSE
        rVoted_PVC_SupplyPressure := rPVC_SupplyPressure_ChC;
    END_IF;

    (* Audit Pairwise Discrepancies *)
    IF ABS(rPVC_SupplyPressure_ChA - rPVC_SupplyPressure_ChB) > 12.0 THEN
        dwTMRDiscrepancyWord := dwTMRDiscrepancyWord OR 16#00000001; (* Ch A-B Discrepancy Bit *)
    END_IF;
    IF ABS(rPVC_SupplyPressure_ChB - rPVC_SupplyPressure_ChC) > 12.0 THEN
        dwTMRDiscrepancyWord := dwTMRDiscrepancyWord OR 16#00000002; (* Ch B-C Discrepancy Bit *)
    END_IF;
    IF ABS(rPVC_SupplyPressure_ChA - rPVC_SupplyPressure_ChC) > 12.0 THEN
        dwTMRDiscrepancyWord := dwTMRDiscrepancyWord OR 16#00000004; (* Ch A-C Discrepancy Bit *)
    END_IF;
ELSIF bChannelHealthy_PVCPres_A AND bChannelHealthy_PVCPres_B THEN
    (* Degraded 1oo2 Operation: Average healthy channels A and B *)
    rVoted_PVC_SupplyPressure := 0.5 * (rPVC_SupplyPressure_ChA + rPVC_SupplyPressure_ChB);
    dwTMRDiscrepancyWord := dwTMRDiscrepancyWord OR 16#00000008; (* Ch C Hardware Fault Bit *)
ELSIF bChannelHealthy_PVCPres_B AND bChannelHealthy_PVCPres_C THEN
    rVoted_PVC_SupplyPressure := 0.5 * (rPVC_SupplyPressure_ChB + rPVC_SupplyPressure_ChC);
    dwTMRDiscrepancyWord := dwTMRDiscrepancyWord OR 16#00000010; (* Ch A Hardware Fault Bit *)
ELSIF bChannelHealthy_PVCPres_A AND bChannelHealthy_PVCPres_C THEN
    rVoted_PVC_SupplyPressure := 0.5 * (rPVC_SupplyPressure_ChA + rPVC_SupplyPressure_ChC);
    dwTMRDiscrepancyWord := dwTMRDiscrepancyWord OR 16#00000020; (* Ch B Hardware Fault Bit *)
ELSIF bChannelHealthy_PVCPres_A THEN
    rVoted_PVC_SupplyPressure := rPVC_SupplyPressure_ChA;
    dwTMRDiscrepancyWord := dwTMRDiscrepancyWord OR 16#00000040; (* Severe Degradation: Single Ch A *)
ELSIF bChannelHealthy_PVCPres_B THEN
    rVoted_PVC_SupplyPressure := rPVC_SupplyPressure_ChB;
    dwTMRDiscrepancyWord := dwTMRDiscrepancyWord OR 16#00000080; (* Severe Degradation: Single Ch B *)
ELSIF bChannelHealthy_PVCPres_C THEN
    rVoted_PVC_SupplyPressure := rPVC_SupplyPressure_ChC;
    dwTMRDiscrepancyWord := dwTMRDiscrepancyWord OR 16#00000100; (* Severe Degradation: Single Ch C *)
ELSE
    (* Total Sensor Failure: Freeze to Safe Default and Trip System Fault *)
    rVoted_PVC_SupplyPressure := 185.0;
    dwTMRDiscrepancyWord := dwTMRDiscrepancyWord OR 16#00000200; (* Total TMR Loss Trip Bit *)
END_IF;

(* --- 1.2 LASD HEADER SUPPLY PRESSURE 2oo3 TMR VOTING --- *)
bChannelHealthy_LASDPres_A := (rLASD_SupplyPressure_ChA >= 5.0) AND (rLASD_SupplyPressure_ChA <= 300.0);
bChannelHealthy_LASDPres_B := (rLASD_SupplyPressure_ChB >= 5.0) AND (rLASD_SupplyPressure_ChB <= 300.0);
bChannelHealthy_LASDPres_C := (rLASD_SupplyPressure_ChC >= 5.0) AND (rLASD_SupplyPressure_ChC <= 300.0);

IF bChannelHealthy_LASDPres_A AND bChannelHealthy_LASDPres_B AND bChannelHealthy_LASDPres_C THEN
    IF ((rLASD_SupplyPressure_ChA >= rLASD_SupplyPressure_ChB) AND (rLASD_SupplyPressure_ChA <= rLASD_SupplyPressure_ChC)) OR
       ((rLASD_SupplyPressure_ChA <= rLASD_SupplyPressure_ChB) AND (rLASD_SupplyPressure_ChA >= rLASD_SupplyPressure_ChC)) THEN
        rVoted_LASD_SupplyPressure := rLASD_SupplyPressure_ChA;
    ELSIF ((rLASD_SupplyPressure_ChB >= rLASD_SupplyPressure_ChA) AND (rLASD_SupplyPressure_ChB <= rLASD_SupplyPressure_ChC)) OR
          ((rLASD_SupplyPressure_ChB <= rLASD_SupplyPressure_ChA) AND (rLASD_SupplyPressure_ChB >= rLASD_SupplyPressure_ChC)) THEN
        rVoted_LASD_SupplyPressure := rLASD_SupplyPressure_ChB;
    ELSE
        rVoted_LASD_SupplyPressure := rLASD_SupplyPressure_ChC;
    END_IF;

    IF ABS(rLASD_SupplyPressure_ChA - rLASD_SupplyPressure_ChB) > 10.0 THEN
        dwTMRDiscrepancyWord := dwTMRDiscrepancyWord OR 16#00000400;
    END_IF;
    IF ABS(rLASD_SupplyPressure_ChB - rLASD_SupplyPressure_ChC) > 10.0 THEN
        dwTMRDiscrepancyWord := dwTMRDiscrepancyWord OR 16#00000800;
    END_IF;
    IF ABS(rLASD_SupplyPressure_ChA - rLASD_SupplyPressure_ChC) > 10.0 THEN
        dwTMRDiscrepancyWord := dwTMRDiscrepancyWord OR 16#00001000;
    END_IF;
ELSIF bChannelHealthy_LASDPres_A AND bChannelHealthy_LASDPres_B THEN
    rVoted_LASD_SupplyPressure := 0.5 * (rLASD_SupplyPressure_ChA + rLASD_SupplyPressure_ChB);
    dwTMRDiscrepancyWord := dwTMRDiscrepancyWord OR 16#00002000;
ELSIF bChannelHealthy_LASDPres_B AND bChannelHealthy_LASDPres_C THEN
    rVoted_LASD_SupplyPressure := 0.5 * (rLASD_SupplyPressure_ChB + rLASD_SupplyPressure_ChC);
    dwTMRDiscrepancyWord := dwTMRDiscrepancyWord OR 16#00004000;
ELSIF bChannelHealthy_LASDPres_A AND bChannelHealthy_LASDPres_C THEN
    rVoted_LASD_SupplyPressure := 0.5 * (rLASD_SupplyPressure_ChA + rLASD_SupplyPressure_ChC);
    dwTMRDiscrepancyWord := dwTMRDiscrepancyWord OR 16#00008000;
ELSE
    rVoted_LASD_SupplyPressure := 160.0;
    dwTMRDiscrepancyWord := dwTMRDiscrepancyWord OR 16#00010000;
END_IF;

(* --- 1.3 SHOT METER 1 ENCODER POSITION 2oo3 TMR VOTING --- *)
(* Shot Meter Displacement Range: -5.0 mm to 350.0 mm stroke *)
IF ((rShotMeter1_LinearPos_ChA >= rShotMeter1_LinearPos_ChB) AND (rShotMeter1_LinearPos_ChA <= rShotMeter1_LinearPos_ChC)) OR
   ((rShotMeter1_LinearPos_ChA <= rShotMeter1_LinearPos_ChB) AND (rShotMeter1_LinearPos_ChA >= rShotMeter1_LinearPos_ChC)) THEN
    rVoted_ShotMeter1_Pos := rShotMeter1_LinearPos_ChA;
ELSIF ((rShotMeter1_LinearPos_ChB >= rShotMeter1_LinearPos_ChA) AND (rShotMeter1_LinearPos_ChB <= rShotMeter1_LinearPos_ChC)) OR
      ((rShotMeter1_LinearPos_ChB <= rShotMeter1_LinearPos_ChA) AND (rShotMeter1_LinearPos_ChB >= rShotMeter1_LinearPos_ChC)) THEN
    rVoted_ShotMeter1_Pos := rShotMeter1_LinearPos_ChB;
ELSE
    rVoted_ShotMeter1_Pos := rShotMeter1_LinearPos_ChC;
END_IF;

IF (ABS(rShotMeter1_LinearPos_ChA - rShotMeter1_LinearPos_ChB) > 0.8) OR
   (ABS(rShotMeter1_LinearPos_ChB - rShotMeter1_LinearPos_ChC) > 0.8) OR
   (ABS(rShotMeter1_LinearPos_ChA - rShotMeter1_LinearPos_ChC) > 0.8) THEN
    dwTMRDiscrepancyWord := dwTMRDiscrepancyWord OR 16#00020000; (* Shot Meter 1 Encoder Drift *)
END_IF;

(* --- 1.4 SHOT METER 2 ENCODER POSITION 2oo3 TMR VOTING --- *)
IF ((rShotMeter2_LinearPos_ChA >= rShotMeter2_LinearPos_ChB) AND (rShotMeter2_LinearPos_ChA <= rShotMeter2_LinearPos_ChC)) OR
   ((rShotMeter2_LinearPos_ChA <= rShotMeter2_LinearPos_ChB) AND (rShotMeter2_LinearPos_ChA >= rShotMeter2_LinearPos_ChC)) THEN
    rVoted_ShotMeter2_Pos := rShotMeter2_LinearPos_ChA;
ELSIF ((rShotMeter2_LinearPos_ChB >= rShotMeter2_LinearPos_ChA) AND (rShotMeter2_LinearPos_ChB <= rShotMeter2_LinearPos_ChC)) OR
      ((rShotMeter2_LinearPos_ChB <= rShotMeter2_LinearPos_ChA) AND (rShotMeter2_LinearPos_ChB >= rShotMeter2_LinearPos_ChC)) THEN
    rVoted_ShotMeter2_Pos := rShotMeter2_LinearPos_ChB;
ELSE
    rVoted_ShotMeter2_Pos := rShotMeter2_LinearPos_ChC;
END_IF;

IF (ABS(rShotMeter2_LinearPos_ChA - rShotMeter2_LinearPos_ChB) > 0.8) OR
   (ABS(rShotMeter2_LinearPos_ChB - rShotMeter2_LinearPos_ChC) > 0.8) OR
   (ABS(rShotMeter2_LinearPos_ChA - rShotMeter2_LinearPos_ChC) > 0.8) THEN
    dwTMRDiscrepancyWord := dwTMRDiscrepancyWord OR 16#00040000; (* Shot Meter 2 Encoder Drift *)
END_IF;

(* --- 1.5 COAXIAL HEATED HOSE TEMPERATURE 2oo3 TMR VOTING --- *)
(* PVC Hose Pt100 RTD Voting (Tolerance 1.5 deg C) *)
IF ((rHoseTemp_PVC_ChA >= rHoseTemp_PVC_ChB) AND (rHoseTemp_PVC_ChA <= rHoseTemp_PVC_ChC)) OR
   ((rHoseTemp_PVC_ChA <= rHoseTemp_PVC_ChB) AND (rHoseTemp_PVC_ChA >= rHoseTemp_PVC_ChC)) THEN
    rVoted_HoseTemp_PVC := rHoseTemp_PVC_ChA;
ELSIF ((rHoseTemp_PVC_ChB >= rHoseTemp_PVC_ChA) AND (rHoseTemp_PVC_ChB <= rHoseTemp_PVC_ChC)) OR
      ((rHoseTemp_PVC_ChB <= rHoseTemp_PVC_ChA) AND (rHoseTemp_PVC_ChB >= rHoseTemp_PVC_ChC)) THEN
    rVoted_HoseTemp_PVC := rHoseTemp_PVC_ChB;
ELSE
    rVoted_HoseTemp_PVC := rHoseTemp_PVC_ChC;
END_IF;

IF (ABS(rHoseTemp_PVC_ChA - rHoseTemp_PVC_ChB) > 1.5) OR
   (ABS(rHoseTemp_PVC_ChB - rHoseTemp_PVC_ChC) > 1.5) OR
   (ABS(rHoseTemp_PVC_ChA - rHoseTemp_PVC_ChC) > 1.5) THEN
    dwTMRDiscrepancyWord := dwTMRDiscrepancyWord OR 16#00080000; (* PVC Thermal Sensor Discrepancy *)
END_IF;

(* LASD Hose Pt100 RTD Voting (Tolerance 1.5 deg C) *)
IF ((rHoseTemp_LASD_ChA >= rHoseTemp_LASD_ChB) AND (rHoseTemp_LASD_ChA <= rHoseTemp_LASD_ChC)) OR
   ((rHoseTemp_LASD_ChA <= rHoseTemp_LASD_ChB) AND (rHoseTemp_LASD_ChA >= rHoseTemp_LASD_ChC)) THEN
    rVoted_HoseTemp_LASD := rHoseTemp_LASD_ChA;
ELSIF ((rHoseTemp_LASD_ChB >= rHoseTemp_LASD_ChA) AND (rHoseTemp_LASD_ChB <= rHoseTemp_LASD_ChC)) OR
      ((rHoseTemp_LASD_ChB <= rHoseTemp_LASD_ChA) AND (rHoseTemp_LASD_ChB >= rHoseTemp_LASD_ChC)) THEN
    rVoted_HoseTemp_LASD := rHoseTemp_LASD_ChB;
ELSE
    rVoted_HoseTemp_LASD := rHoseTemp_LASD_ChC;
END_IF;

IF (ABS(rHoseTemp_LASD_ChA - rHoseTemp_LASD_ChB) > 1.5) OR
   (ABS(rHoseTemp_LASD_ChB - rHoseTemp_LASD_ChC) > 1.5) OR
   (ABS(rHoseTemp_LASD_ChA - rHoseTemp_LASD_ChC) > 1.5) THEN
    dwTMRDiscrepancyWord := dwTMRDiscrepancyWord OR 16#00100000; (* LASD Thermal Sensor Discrepancy *)
END_IF;
""")

    # -------------------------------------------------------------------------
    # PHASE 2: NON-NEWTONIAN RHEOLOGY, BULK COMPLIANCE & STATE-SPACE PREDICTION
    # -------------------------------------------------------------------------
    parts.append("""(* ==================================================================================== *)
(* PHASE 2: NON-NEWTONIAN FLUID RHEOLOGY & DISCRETE STATE-SPACE PREDICTION               *)
(* Evaluates Herschel-Bulkley pseudoplastic shear-thinning viscosity, effective bulk     *)
(* modulus with hose wall compliance, and unrolls discrete state propagation:            *)
(* x[k+1] = A * x[k] + B * u[k]                                                         *)
(* y[k]   = C * x[k] + D * u[k]                                                         *)
(* ==================================================================================== *)

(* --- 2.1 NON-NEWTONIAN APPARENT VISCOSITY (HERSCHEL-BULKLEY MODEL) --- *)
(* PVC Plastisol Nozzle Shear Rate: gamma_dot = 4 * Q / (pi * R_nozzle^3) *)
(* Nozzle Radius R_noz = 1.25 mm -> R^3 = 1.953 mm3 = 1.953E-9 m3 *)
rCalculatedShearRate_PVC := (4.0 * MAX(0.1, arrStateVector[8]) * 1000.0) / (3.14159265 * 1.953125);
IF rCalculatedShearRate_PVC < 1.0 THEN
    rCalculatedShearRate_PVC := 1.0;
END_IF;

(* Temperature Correction Factor: Arrhenius decay centered at 28.0 deg C *)
(* mu(T) = mu_0 * EXP( 0.038 * (28.0 - T) ) *)
rDynamicViscosity_PVC := ( (65.0 / (rCalculatedShearRate_PVC + 0.1)) +
                           82.0 * EXPT((rCalculatedShearRate_PVC + 0.1), (0.48 - 1.0)) ) * 1000.0;
rDynamicViscosity_PVC := rDynamicViscosity_PVC * EXP(0.038 * (28.0 - rVoted_HoseTemp_PVC));
rDynamicViscosity_PVC := LIMIT(50000.0, rDynamicViscosity_PVC, 250000.0); (* Saturation bounds [mPa*s] *)

(* LASD Compound Swirl Applicator Shear Rate & Viscosity *)
rCalculatedShearRate_LASD := (4.0 * MAX(0.5, arrStateVector[12]) * 1000.0) / (3.14159265 * 4.096);
IF rCalculatedShearRate_LASD < 1.0 THEN
    rCalculatedShearRate_LASD := 1.0;
END_IF;

rDynamicViscosity_LASD := ( (115.0 / (rCalculatedShearRate_LASD + 0.1)) +
                            145.0 * EXPT((rCalculatedShearRate_LASD + 0.1), (0.52 - 1.0)) ) * 1000.0;
rDynamicViscosity_LASD := rDynamicViscosity_LASD * EXP(0.042 * (28.0 - rVoted_HoseTemp_LASD));
rDynamicViscosity_LASD := LIMIT(80000.0, rDynamicViscosity_LASD, 320000.0);

(* --- 2.2 EFFECTIVE BULK MODULUS EVALUATION --- *)
(* Combines fluid bulk modulus beta_fluid = 18,000 bar with braided high-pressure hose wall elasticity *)
(* 1.0 / beta_eff = (1.0 / beta_fluid) + (D_inner / (t_wall * E_wall)) *)
(* PVC Hose: D_in = 12.7 mm, t_wall = 4.5 mm, E_hose = 1.6E4 bar -> beta_eff ~= 4,250 bar *)
rEffectiveBulkModulus_PVC := 1.0 / ( (1.0 / 18000.0) + (12.7 / (4.5 * 16000.0)) );
rEffectiveBulkModulus_LASD := 1.0 / ( (1.0 / 17500.0) + (19.05 / (5.2 * 15500.0)) );

(* Hydraulic Friction Pressure Drop along 15m Delivery Hose *)
rFluidFrictionPressureDrop_PVC := (8.0 * (rDynamicViscosity_PVC * 0.001) * 15.0 * (arrStateVector[2] * 1.0E-6)) /
                                  (3.14159265 * 0.0000260) * 1.0E-5;

(* --- 2.3 SYNCHRONIZE STATE VECTOR FROM VOTED SENSORS --- *)
arrStateVector[1] := rVoted_PVC_SupplyPressure;
arrStateVector[3] := rVoted_LASD_SupplyPressure;
arrStateVector[5] := rVoted_ShotMeter1_Pos;
arrStateVector[9] := rVoted_ShotMeter2_Pos;
arrStateVector[15] := rVoted_HoseTemp_PVC;

(* Feedforward Robot TCP Vector Speed into Input Vector u[8] *)
arrControlInputs[8] := MAX(rRobot1_TCP_VectorSpeed, rRobot2_TCP_VectorSpeed) * 1000.0; (* Convert m/s to mm/s *)

(* --- 2.4 DISCRETE STATE PROPAGATION: x[k+1] = A * x[k] + B * u[k] --- *)
FOR iIndex := 1 TO 16 DO
    rTempDotProduct := 0.0;
    (* State transition matrix product *)
    FOR jIndex := 1 TO 16 DO
        rTempDotProduct := rTempDotProduct + (arrA[iIndex, jIndex] * arrStateVector[jIndex]);
    END_FOR;
    (* Control input coupling product *)
    FOR jIndex := 1 TO 8 DO
        rTempDotProduct := rTempDotProduct + (arrB[iIndex, jIndex] * arrControlInputs[jIndex]);
    END_FOR;
    arrNextStateVector[iIndex] := rTempDotProduct;
END_FOR;

(* --- 2.5 MEASUREMENT SYSTEM OUTPUTS: y[k] = C * x[k] + D * u[k] --- *)
FOR iIndex := 1 TO 8 DO
    rTempDotProduct := 0.0;
    FOR jIndex := 1 TO 16 DO
        rTempDotProduct := rTempDotProduct + (arrC[iIndex, jIndex] * arrStateVector[jIndex]);
    END_FOR;
    FOR jIndex := 1 TO 8 DO
        rTempDotProduct := rTempDotProduct + (arrD[iIndex, jIndex] * arrControlInputs[jIndex]);
    END_FOR;
    arrSystemOutputs[iIndex] := rTempDotProduct;
END_FOR;

(* Update internal state vector for next iteration step *)
FOR iIndex := 1 TO 16 DO
    arrStateVector[iIndex] := arrNextStateVector[iIndex];
END_FOR;

(* Assign Primary Physical State Outputs *)
rCalculatedBeadArea := arrSystemOutputs[8];
""")

    # -------------------------------------------------------------------------
    # PHASE 3: RECEDING-HORIZON MPC & FLOW-TO-SPEED PACING
    # -------------------------------------------------------------------------
    parts.append("""(* ==================================================================================== *)
(* PHASE 3: RECEDING-HORIZON MPC OPTIMIZATION & DYNAMIC FLOW-TO-SPEED PACING             *)
(* Dynamically modulates shot meter servo velocity and dispense needle valve opening     *)
(* to strictly pace extruded fluid volume against robot TCP vector speed (0.2 - 1.5 m/s)  *)
(* with pre-opening acceleration advance and sub-10ms snuff-back suckback.              *)
(* ==================================================================================== *)

(* --- 3.1 DYNAMIC RECIPE TARGET SETPOINT LOOKUP BASED ON RFID BODY VARIANT --- *)
CASE uiBodyVariantRFID OF
    1: (* Sedan Platform: Standard Hem Seam & Acoustic Package *)
        rRecipe_BeadWidth           := 8.0;     (* Nominal Bead Width: 8.0 mm *)
        rRecipe_BeadHeight          := 2.2;     (* Nominal Bead Height: 2.2 mm *)
        rRecipe_LASD_Thickness      := 2.5;     (* Floor Pan LASD Thickness: 2.5 mm *)
        rRecipe_LASD_Width          := 120.0;   (* LASD Swirl Width: 120.0 mm *)
        rRecipe_NominalSeamLength   := 28500.0; (* Total Underbody Seam: 28.5 m *)
        rRecipe_GapToleranceLimit   := 2.5;     (* Max Flange Gap: 2.5 mm *)

    2: (* SUV / Crossover Platform: Heavy Structural Sealing & Reinforced LASD *)
        rRecipe_BeadWidth           := 10.5;    (* Nominal Bead Width: 10.5 mm *)
        rRecipe_BeadHeight          := 2.8;     (* Nominal Bead Height: 2.8 mm *)
        rRecipe_LASD_Thickness      := 3.2;     (* Floor Pan LASD Thickness: 3.2 mm *)
        rRecipe_LASD_Width          := 150.0;   (* LASD Swirl Width: 150.0 mm *)
        rRecipe_NominalSeamLength   := 34200.0; (* Total Underbody Seam: 34.2 m *)
        rRecipe_GapToleranceLimit   := 3.2;     (* Max Flange Gap: 3.2 mm *)

    3: (* Coupe / Gran Turismo Platform: Precision Aerodynamic Seam *)
        rRecipe_BeadWidth           := 7.0;     (* Nominal Bead Width: 7.0 mm *)
        rRecipe_BeadHeight          := 2.0;     (* Nominal Bead Height: 2.0 mm *)
        rRecipe_LASD_Thickness      := 2.0;     (* Floor Pan LASD Thickness: 2.0 mm *)
        rRecipe_LASD_Width          := 100.0;   (* LASD Swirl Width: 100.0 mm *)
        rRecipe_NominalSeamLength   := 24600.0; (* Total Underbody Seam: 24.6 m *)
        rRecipe_GapToleranceLimit   := 2.0;     (* Max Flange Gap: 2.0 mm *)

    4: (* Electric Vehicle (EV) Skateboard Battery Floor Pan Platform *)
        rRecipe_BeadWidth           := 12.0;    (* Wide Hem Seam for Battery Enclosure Seal: 12.0 mm *)
        rRecipe_BeadHeight          := 3.2;     (* Nominal Bead Height: 3.2 mm *)
        rRecipe_LASD_Thickness      := 3.8;     (* Heavy Damping over EV Battery Floor: 3.8 mm *)
        rRecipe_LASD_Width          := 180.0;   (* Wide Swirl Band: 180.0 mm *)
        rRecipe_NominalSeamLength   := 38900.0; (* Battery Perimeter Seam: 38.9 m *)
        rRecipe_GapToleranceLimit   := 3.5;     (* Max Flange Gap: 3.5 mm *)

ELSE
    (* Fallback Default: Standard Mid-Size Vehicle Architecture *)
    rRecipe_BeadWidth           := 8.5;
    rRecipe_BeadHeight          := 2.4;
    rRecipe_LASD_Thickness      := 2.8;
    rRecipe_LASD_Width          := 130.0;
    rRecipe_NominalSeamLength   := 29000.0;
    rRecipe_GapToleranceLimit   := 2.5;
END_CASE;

(* Semi-Elliptical Bead Cross-Section: Area = (pi / 4) * Width * Height *)
rNominalTargetBeadArea := 0.785398 * rRecipe_BeadWidth * rRecipe_BeadHeight;
(* LASD Flat Swirl Strip Area: Area = Width * Thickness *)
rNominalTargetLASD_Area := rRecipe_LASD_Width * rRecipe_LASD_Thickness;

(* --- 3.2 REAL-TIME 3D OPTICAL SEAM TRACKING 1st-ORDER LOW-PASS FILTER (250 Hz) --- *)
IF bLaserSeamTracker_Valid THEN
    (* Exponential smoothing filter: alpha = 0.25 (time constant ~= 8 ms) *)
    rFilteredSeam_dX := (0.25 * rLaserSeamTracker_dX) + (0.75 * rFilteredSeam_dX);
    rFilteredSeam_dY := (0.25 * rLaserSeamTracker_dY) + (0.75 * rFilteredSeam_dY);
    rFilteredSeam_dZ := (0.25 * rLaserSeamTracker_dZ) + (0.75 * rFilteredSeam_dZ);
    rFilteredFlangeGapWidth := (0.20 * rLaserSeamTracker_GapWidth) + (0.80 * rFilteredFlangeGapWidth);

    (* Transmit Real-Time Correction Offsets to Robot Trajectory Controllers *)
    rRobotSeamCorrection_dX := LIMIT(-15.0, rFilteredSeam_dX, 15.0);
    rRobotSeamCorrection_dY := LIMIT(-15.0, rFilteredSeam_dY, 15.0);
    rRobotSeamCorrection_dZ := LIMIT(-15.0, rFilteredSeam_dZ, 15.0);
ELSE
    (* Optical Tracking Signal Degraded: Decay Offsets Gradually to Zero *)
    rRobotSeamCorrection_dX := rRobotSeamCorrection_dX * 0.95;
    rRobotSeamCorrection_dY := rRobotSeamCorrection_dY * 0.95;
    rRobotSeamCorrection_dZ := rRobotSeamCorrection_dZ * 0.95;
    dwRobotCoordinationWord := dwRobotCoordinationWord OR 16#00000001; (* Seam Track Degraded Bit *)
END_IF;

(* --- 3.3 ROBOT TCP ACCELERATION & PRE-OPENING LEAD COMPENSATION --- *)
(* Filter Robot 1 TCP Speed *)
rFilteredRobotTCP_Speed := (0.35 * rRobot1_TCP_VectorSpeed) + (0.65 * rFilteredRobotTCP_Speed);
rCalculatedRobotTCP_Accel := (rFilteredRobotTCP_Speed - rPreviousRobotTCP_Speed) / rDeltaTime_Seconds;
rPreviousRobotTCP_Speed := rFilteredRobotTCP_Speed;

(* Pre-Opening Lead Time: t_pre = tau_fluid_delay + (v / 2*a_max) *)
(* Typical fluid hydraulic line delay ~= 18.0 ms *)
rPreOpenLeadTime_Comp := 0.018 + (rFilteredRobotTCP_Speed / (2.0 * 4.5));
rPreOpenLeadTime_Comp := LIMIT(0.010, rPreOpenLeadTime_Comp, 0.065);

(* Dynamic Volumetric Flow Rate Pacing: Q_target(t) = A_bead * v_TCP(t) * (1 + k_gap * w_gap) *)
(* Convert mm2 * mm/s to ml/s (1 ml = 1000 mm3) *)
rTargetVolumetricFlowRate_PVC := (rNominalTargetBeadArea * (rFilteredRobotTCP_Speed * 1000.0) *
                                 (1.0 + 0.18 * rFilteredFlangeGapWidth)) / 1000.0;
rTargetVolumetricFlowRate_LASD := (rNominalTargetLASD_Area * (rRobot5_TCP_VectorSpeed * 1000.0)) / 1000.0;

(* Calculate Instantaneous LASD Areal Mass Density: rho_areal = rho_fluid * H_film *)
(* Wet LASD Density = 1.45 g/cm3 = 1450 kg/m3. Film thickness in mm -> kg/m2 *)
rCalculatedLASD_MassDensity := 1.45 * rOpticalLASD_FilmThickness;

(* --- 3.4 SUB-10ms SNUFF-BACK SUCK-BACK CONTROL LOGIC --- *)
(* Triggered at completion of seam or rapid robot TCP deceleration (< 0.05 m/s while dispensing) *)
IF (nFSM_State = 5) AND (rFilteredRobotTCP_Speed < 0.05) AND (rFilteredRobotTCP_Speed >= 0.0) AND (tStateTimer > T#2S) THEN
    bSnuffBackActive := TRUE;
ELSE
    bSnuffBackActive := FALSE;
END_IF;

IF bSnuffBackActive THEN
    (* Reverse Shot Meter Piston at -120 mm/s to swallow droplet (< 10 ms duration) *)
    rPVC_ShotMeter1_VelocityCmd := -120.0;
    rPVC_ShotMeter2_VelocityCmd := -120.0;
    rPVC_NozzleNeedleValveCmd_R1 := 0.0; (* Snap Needle Closed *)
    rPVC_NozzleNeedleValveCmd_R2 := 0.0;
    dwDispenseStatusWord := dwDispenseStatusWord OR 16#00000001; (* Snuff-Back Active Flag *)
END_IF;

(* --- 3.5 RECEDING-HORIZON MPC GRADIENT OPTIMIZATION --- *)
(* Build Dynamic Reference Vector x_ref *)
arrStateRef[1]  := 185.0;                          (* PVC Header Setpoint: 185 bar *)
arrStateRef[3]  := 160.0;                          (* LASD Header Setpoint: 160 bar *)
arrStateRef[7]  := 145.0;                          (* PVC Tip Pressure Setpoint: 145 bar *)
arrStateRef[8]  := rTargetVolumetricFlowRate_PVC;  (* Synchronized Volumetric Flow Target *)
arrStateRef[11] := 130.0;                          (* LASD Applicator Pressure Setpoint: 130 bar *)
arrStateRef[12] := rTargetVolumetricFlowRate_LASD; (* LASD Dispense Flow Target *)
arrStateRef[13] := 0.0;                            (* Zero Seam Tracking Trajectory Error *)
arrStateRef[15] := 28.0;                           (* Thermal Setpoint: 28.0 deg C *)
arrStateRef[16] := rNominalTargetBeadArea;         (* Nominal Bead Cross-Section Setpoint *)

(* Evaluate Gradient of Cost J with respect to Actuator Inputs u[k] *)
(* nabla J_u = R * u + B^T * Q * (x - x_ref) *)
FOR jIndex := 1 TO 8 DO
    rTempDotProduct := arrR_Weights[jIndex] * arrControlInputs[jIndex];
    FOR iIndex := 1 TO 16 DO
        rStateDeviation := arrStateVector[iIndex] - arrStateRef[iIndex];
        rTempDotProduct := rTempDotProduct + (arrB[iIndex, jIndex] * arrQ_Weights[iIndex] * rStateDeviation);
    END_FOR;
    arrMPC_Gradient[jIndex] := rTempDotProduct;
END_FOR;

(* Projected Gradient Step with Slew-Rate and Hard Saturation Enforcement *)
FOR jIndex := 1 TO 8 DO
    (* Gradient Descent Step: alpha_step = 0.045 *)
    arrControlInputs[jIndex] := arrControlInputs[jIndex] - (0.045 * arrMPC_Gradient[jIndex]);

    (* Apply Slew-Rate Constraints *)
    arrControlInputs[jIndex] := LIMIT(arrPrevControlInputs[jIndex] - (arrU_RateLimits[jIndex] * rDeltaTime_Seconds),
                                      arrControlInputs[jIndex],
                                      arrPrevControlInputs[jIndex] + (arrU_RateLimits[jIndex] * rDeltaTime_Seconds));

    (* Apply Hard Saturation Limits *)
    arrControlInputs[jIndex] := LIMIT(arrU_MinLimits[jIndex], arrControlInputs[jIndex], arrU_MaxLimits[jIndex]);
    arrPrevControlInputs[jIndex] := arrControlInputs[jIndex];
END_FOR;

(* Route MPC Optimal Commands to Actuator Outputs *)
IF NOT bSnuffBackActive AND (nFSM_State = 5 OR nFSM_State = 6) THEN
    rPVC_RamExtruderPumpCmd      := arrControlInputs[1];
    rLASD_RamExtruderPumpCmd     := arrControlInputs[2];
    rPVC_ShotMeter1_VelocityCmd  := arrControlInputs[3];
    rPVC_NozzleNeedleValveCmd_R1 := arrControlInputs[4];
    rLASD_ShotMeter1_VelocityCmd := arrControlInputs[5];
    rLASD_NozzleDispenseCmd_R5   := arrControlInputs[6];
ELSE
    IF NOT bSnuffBackActive THEN
        rPVC_ShotMeter1_VelocityCmd  := 0.0;
        rPVC_ShotMeter2_VelocityCmd  := 0.0;
        rLASD_ShotMeter1_VelocityCmd := 0.0;
        rLASD_ShotMeter2_VelocityCmd := 0.0;
        rPVC_NozzleNeedleValveCmd_R1 := 0.0;
        rPVC_NozzleNeedleValveCmd_R2 := 0.0;
        rLASD_NozzleDispenseCmd_R5   := 0.0;
        rLASD_NozzleDispenseCmd_R6   := 0.0;
    END_IF;
END_IF;

(* Coaxial Heated Hose Closed-Loop PI Control (Target 28.0 deg C) *)
IF rVoted_HoseTemp_PVC < 28.0 THEN
    rHeatedHose_PWMDuty_PVC := LIMIT(0.0, (28.0 - rVoted_HoseTemp_PVC) * 22.5, 100.0);
ELSE
    rHeatedHose_PWMDuty_PVC := 0.0;
END_IF;

IF rVoted_HoseTemp_LASD < 28.0 THEN
    rHeatedHose_PWMDuty_LASD := LIMIT(0.0, (28.0 - rVoted_HoseTemp_LASD) * 20.0, 100.0);
ELSE
    rHeatedHose_PWMDuty_LASD := 0.0;
END_IF;
""")

    # -------------------------------------------------------------------------
    # PHASE 4: 12-STAGE OPERATIONAL FINITE STATE MACHINE (FSM)
    # -------------------------------------------------------------------------
    parts.append("""(* ==================================================================================== *)
(* PHASE 4: 12-STAGE OPERATIONAL FINITE STATE MACHINE (FSM)                             *)
(* Full Production Life Cycle:                                                          *)
(*  0: System Initialization & Safety Interlock Pre-Checks                              *)
(*  1: Skid Infeed & Precision Lifter Pin Clamping                                      *)
(*  2: Body Variant Identification via RFID Transponder                                 *)
(*  3: Robot Tool Calibration & Nozzle Tip Cleaning Scraper Wipe                        *)
(*  4: Optical 3D Laser Seam Tracking Pre-Flight Flange Scan                            *)
(*  5: Coordinated Underbody Hem Flange Seam Sealing (Robots 1-4)                       *)
(*  6: Floor Pan Liquid Applied Sound Deadener (LASD) Dispensing (Robots 5-6)           *)
(*  7: In-Line Optical Bead Metrology & Acoustic Density Inspection                     *)
(*  8: Nozzle Automated Snuff-Back Purge & Catch Pot Deposit                            *)
(*  9: Skid Unclamp & Transfer Advance to PVC Gelling Curing Oven                       *)
(* 10: Robot Fleet Home Position Parking & Safety Area Clear Handshake                  *)
(* 11: Bulk Material Barrel Changeover & Header Line Auto-Purge Cycle                   *)
(* 12: Emergency E-Stop Fast Depressurization Safe Dump                                 *)
(* ==================================================================================== *)

(* Advance State Execution Dwell Timer *)
IF nFSM_State = nFSM_PrevState THEN
    tStateTimer := tStateTimer + T#2MS;
ELSE
    tStateTimer := T#0MS;
    nFSM_PrevState := nFSM_State;
END_IF;

(* Global Safety Interlock Supervisor: Immediate Trip to State 12 on E-Stop or Fence Breach *)
IF (NOT bSafetyFenceOK) OR (bEStopActive) THEN
    nFSM_State := 12; (* Jump immediately to Emergency Dump *)
END_IF;

CASE nFSM_State OF

    0: (* --- STATE 0: SYSTEM INITIALIZATION & SAFETY HARDWARE PRE-CHECKS --- *)
        bSkidLifterClampEngageCmd       := FALSE;
        bSkidLifterLowerCmd             := TRUE;
        bSkidTransferAdvancePermissive  := FALSE;
        bRobotFleetRunPermissive        := FALSE;
        bPVC_FastDumpValveCmd           := FALSE;
        bLASD_FastDumpValveCmd          := FALSE;
        bCycleCompletedPass             := FALSE;
        bCycleCompletedReject           := FALSE;

        (* Audit Master Hardware Enable, 24V Field Bus, and Safety Interlocks *)
        IF bSystemEnable AND bSafetyFenceOK AND (NOT bEStopActive) THEN
            IF tStateTimer >= T#1S THEN
                nFSM_State := 1; (* Advance to Skid Infeed *)
            END_IF;
        END_IF;

    1: (* --- STATE 1: SKID INFEED & PRECISION LIFTER PIN CLAMPING --- *)
        bSkidTransferAdvancePermissive := FALSE;
        bRobotFleetRunPermissive := FALSE;

        (* Await Car Body Pallet Skid Arrival *)
        IF bSkidInfeedPresent AND (rSkidInfeedPosition >= 12500.0) THEN
            (* Energize Precision Hydraulic / Pneumatic Lifter Clamps *)
            bSkidLifterClampEngageCmd := TRUE;
            bSkidLifterLowerCmd := FALSE;

            (* Confirm Clamping Limit Switches Engaged within 2.5 seconds *)
            IF bSkidLifterClampedLimit THEN
                IF tStateTimer >= T#500MS THEN
                    nFSM_State := 2; (* Advance to RFID Body Variant Identification *)
                END_IF;
            ELSIF tStateTimer > T#3S THEN
                (* Clamping Timeout Trip *)
                dwSystemStatusWord := dwSystemStatusWord OR 16#00000002; (* Clamp Timeout Fault *)
            END_IF;
        END_IF;

    2: (* --- STATE 2: BODY VARIANT IDENTIFICATION VIA RFID TRANSPONDER --- *)
        bRobotFleetRunPermissive := FALSE;

        (* Interrogate RFID Tag mounted on Skid Leading Edge *)
        IF (uiBodyVariantRFID >= 1) AND (uiBodyVariantRFID <= 4) THEN
            uiLoadedVariantIndex := uiBodyVariantRFID;
            dwSystemStatusWord := dwSystemStatusWord OR 16#00000004; (* Variant Loaded Flag *)
            IF tStateTimer >= T#250MS THEN
                nFSM_State := 3; (* Advance to Nozzle Tip Wipe & Calibration *)
            END_IF;
        ELSIF tStateTimer > T#2S THEN
            (* RFID Read Failure: Invalid Body Code *)
            dwSystemStatusWord := dwSystemStatusWord OR 16#00000008; (* RFID Parity Error *)
        END_IF;

    3: (* --- STATE 3: ROBOT TOOL CALIBRATION & NOZZLE TIP CLEANING SCRAPER WIPE --- *)
        bRobotFleetRunPermissive := TRUE;

        (* Robots move to service stations to scrape dried plastisol from nozzle tips *)
        IF bNozzleWipeCompleted_R1 AND bNozzleWipeCompleted_R2 THEN
            (* Confirm Shot Meter Cylinders Primed at Home Zero Datum *)
            IF (rVoted_ShotMeter1_Pos < 2.0) AND (rVoted_ShotMeter2_Pos < 2.0) THEN
                IF tStateTimer >= T#1S THEN
                    nFSM_State := 4; (* Advance to Seam Tracking Pre-Flight *)
                END_IF;
            END_IF;
        ELSIF tStateTimer > T#8S THEN
            (* Tip Cleaner Scraper Mechanism Jam Fault *)
            dwSystemStatusWord := dwSystemStatusWord OR 16#00000010; (* Tip Cleaner Fault *)
        END_IF;

    4: (* --- STATE 4: OPTICAL 3D LASER SEAM TRACKING PRE-FLIGHT FLANGE SCAN --- *)
        bRobotFleetRunPermissive := TRUE;

        (* Wrist-mounted laser sensors scan critical car body reference datum holes *)
        IF bLaserSeamTracker_Valid THEN
            (* Verify Stamping Fit-Up Tolerance: Gap Width must not exceed Recipe Limit *)
            IF rFilteredFlangeGapWidth <= rRecipe_GapToleranceLimit THEN
                IF tStateTimer >= T#1500MS THEN
                    nFSM_State := 5; (* Advance to Coordinated Seam Sealing *)
                END_IF;
            ELSE
                (* Excessive Sheet Metal Gap Width: Abort Cycle to Prevent Blowout *)
                dwMetrologyStatusWord := dwMetrologyStatusWord OR 16#00000001; (* Gap Excess Reject *)
                nFSM_State := 9; (* Abort to Skid Transfer *)
            END_IF;
        ELSIF tStateTimer > T#4S THEN
            dwRobotCoordinationWord := dwRobotCoordinationWord OR 16#00000002; (* Pre-Flight Lost *)
        END_IF;

    5: (* --- STATE 5: COORDINATED UNDERBODY HEM FLANGE SEAM SEALING (ROBOTS 1-4) --- *)
        bRobotFleetRunPermissive := TRUE;
        dwDispenseStatusWord := dwDispenseStatusWord OR 16#00000002; (* Sealing Active *)

        (* Robots 1 to 4 execute high-speed seam sealing and rocker panel spray *)
        (* Supervision of Shot Meter 1 Piston Stroke Consumption *)
        IF rVoted_ShotMeter1_Pos >= 320.0 THEN
            (* Shot Meter Cylinder Volume Depleted -> Trigger Auto-Refill *)
            dwDispenseStatusWord := dwDispenseStatusWord OR 16#00000004; (* Shot Meter Refill *)
        END_IF;

        (* Check for Seam Trajectory Completion *)
        IF (tStateTimer >= T#18S) AND (rFilteredRobotTCP_Speed < 0.05) THEN
            nFSM_State := 6; (* Advance to Floor Pan LASD Dispensing *)
        END_IF;

    6: (* --- STATE 6: FLOOR PAN LIQUID APPLIED SOUND DEADENER (LASD) DISPENSING (ROBOTS 5-6) --- *)
        bRobotFleetRunPermissive := TRUE;
        dwDispenseStatusWord := dwDispenseStatusWord OR 16#00000008; (* LASD Active *)

        (* Robots 5 and 6 apply acoustic patches on passenger floor pans *)
        IF (tStateTimer >= T#14S) AND (rRobot5_TCP_VectorSpeed < 0.05) THEN
            nFSM_State := 7; (* Advance to Metrology Inspection *)
        END_IF;

    7: (* --- STATE 7: IN-LINE OPTICAL BEAD METROLOGY & ACOUSTIC DENSITY INSPECTION --- *)
        bRobotFleetRunPermissive := TRUE;

        (* Multi-beam laser profiler scans applied bead along seam *)
        IF diMetrologySampleCount < 500 THEN
            diMetrologySampleCount := diMetrologySampleCount + 1;
            rMetrologySum_BeadWidth := rMetrologySum_BeadWidth + rOpticalBeadWidth_Sensor;
            rMetrologySum_BeadHeight := rMetrologySum_BeadHeight + rOpticalBeadHeight_Sensor;
            rMetrologySum_LASD_Thick := rMetrologySum_LASD_Thick + rOpticalLASD_FilmThickness;
        END_IF;

        IF tStateTimer >= T#3S THEN
            (* Compute Statistical Means *)
            IF diMetrologySampleCount > 0 THEN
                rCalculatedMeanBeadWidth := rMetrologySum_BeadWidth / DINT_TO_REAL(diMetrologySampleCount);
                rCalculatedMeanBeadHeight := rMetrologySum_BeadHeight / DINT_TO_REAL(diMetrologySampleCount);
                rCalculatedMeanLASD_Thick := rMetrologySum_LASD_Thick / DINT_TO_REAL(diMetrologySampleCount);
            END_IF;

            (* Audit Bead Quality Tolerances *)
            IF (rCalculatedMeanBeadWidth >= (rRecipe_BeadWidth - 1.5)) AND
               (rCalculatedMeanBeadWidth <= (rRecipe_BeadWidth + 2.0)) AND
               (rCalculatedMeanBeadHeight >= (rRecipe_BeadHeight - 0.6)) AND
               (rCalculatedMeanBeadHeight <= (rRecipe_BeadHeight + 0.8)) AND
               (rCalculatedMeanLASD_Thick >= (rRecipe_LASD_Thickness - 0.5)) THEN
                bCycleCompletedPass := TRUE;
                bCycleCompletedReject := FALSE;
                dwMetrologyStatusWord := dwMetrologyStatusWord OR 16#00000002; (* Metrology PASS *)
            ELSE
                bCycleCompletedPass := FALSE;
                bCycleCompletedReject := TRUE;
                dwMetrologyStatusWord := dwMetrologyStatusWord OR 16#00000004; (* Metrology REJECT *)
            END_IF;

            nFSM_State := 8; (* Advance to Snuff-Back Purge *)
        END_IF;

    8: (* --- STATE 8: NOZZLE AUTOMATED SNUFF-BACK PURGE & CATCH POT DEPOSIT --- *)
        bRobotFleetRunPermissive := TRUE;

        (* Deposit small test shot into catch pot to refresh nozzle orifice *)
        IF tStateTimer >= T#1S THEN
            nFSM_State := 9; (* Advance to Skid Unclamp *)
        END_IF;

    9: (* --- STATE 9: SKID UNCLAMP & TRANSFER ADVANCE TO PVC GELLING OVEN --- *)
        bRobotFleetRunPermissive := FALSE;

        (* Lower Locating Pin Lifter Cylinders *)
        bSkidLifterClampEngageCmd := FALSE;
        bSkidLifterLowerCmd := TRUE;

        (* Verify Lifter Lowered Limit Switch *)
        IF bSkidLifterLoweredLimit THEN
            (* Grant Transfer Permissive to Oven Advance Conveyor *)
            bSkidTransferAdvancePermissive := TRUE;
            IF tStateTimer >= T#2S THEN
                nFSM_State := 10; (* Advance to Fleet Parking *)
            END_IF;
        ELSIF tStateTimer > T#4S THEN
            dwSystemStatusWord := dwSystemStatusWord OR 16#00000020; (* Lifter Lower Fault *)
        END_IF;

    10: (* --- STATE 10: ROBOT FLEET HOME POSITION PARKING & SAFETY CLEAR HANDSHAKE --- *)
        bSkidTransferAdvancePermissive := FALSE;
        bRobotFleetRunPermissive := TRUE;

        (* Verify all 6 robots parked safely in home standby envelopes *)
        IF bRobotAllInInterferenceClear THEN
            (* Check for Bulk Barrel Depletion *)
            IF bBarrelDepletedSwitch_PVC OR bBarrelDepletedSwitch_LASD THEN
                nFSM_State := 11; (* Branch to Barrel Changeover *)
            ELSE
                (* Reset Metrology Counters and Cycle Return *)
                diMetrologySampleCount := 0;
                rMetrologySum_BeadWidth := 0.0;
                rMetrologySum_BeadHeight := 0.0;
                rMetrologySum_LASD_Thick := 0.0;

                IF bCycleStartPB OR (tStateTimer >= T#2S) THEN
                    nFSM_State := 0; (* Cycle Complete: Return to Ready Standby *)
                END_IF;
            END_IF;
        END_IF;

    11: (* --- STATE 11: BULK MATERIAL BARREL CHANGEOVER & HEADER LINE AUTO-PURGE --- *)
        bRobotFleetRunPermissive := FALSE;
        dwDispenseStatusWord := dwDispenseStatusWord OR 16#00000010; (* Barrel Swap Active *)

        (* Hydraulic Ram Follower Plate Retract & Degassing Vent *)
        IF (NOT bBarrelDepletedSwitch_PVC) AND (NOT bBarrelDepletedSwitch_LASD) THEN
            (* New Drums Locked in Place: Execute 5-second automatic fluid line prime *)
            rPVC_RamExtruderPumpCmd := 35.0;
            rLASD_RamExtruderPumpCmd := 30.0;
            IF tStateTimer >= T#5S THEN
                rPVC_RamExtruderPumpCmd := 0.0;
                rLASD_RamExtruderPumpCmd := 0.0;
                nFSM_State := 0; (* Return to Ready Standby *)
            END_IF;
        END_IF;

    12: (* --- STATE 12: EMERGENCY E-STOP FAST DEPRESSURIZATION SAFE DUMP --- *)
        (* De-energize all motion, lock robot safety brakes, dump fluid pressure *)
        bRobotFleetRunPermissive        := FALSE;
        bSkidTransferAdvancePermissive  := FALSE;
        bSkidLifterClampEngageCmd       := FALSE;
        bSkidLifterLowerCmd             := TRUE;
        rPVC_RamExtruderPumpCmd         := 0.0;
        rLASD_RamExtruderPumpCmd        := 0.0;
        rPVC_ShotMeter1_VelocityCmd     := 0.0;
        rPVC_ShotMeter2_VelocityCmd     := 0.0;
        rLASD_ShotMeter1_VelocityCmd    := 0.0;
        rLASD_ShotMeter2_VelocityCmd    := 0.0;
        rPVC_NozzleNeedleValveCmd_R1    := 0.0;
        rPVC_NozzleNeedleValveCmd_R2    := 0.0;
        rLASD_NozzleDispenseCmd_R5      := 0.0;
        rLASD_NozzleDispenseCmd_R6      := 0.0;
        rHeatedHose_PWMDuty_PVC         := 0.0;
        rHeatedHose_PWMDuty_LASD        := 0.0;

        (* Energize Fast Depressurization Dump Solenoids into Catch Tanks *)
        bPVC_FastDumpValveCmd := TRUE;
        bLASD_FastDumpValveCmd := TRUE;
        dwSystemStatusWord := dwSystemStatusWord OR 16#00000040; (* E-Stop Depressurizing *)

        (* Latch Safe Depressurization until E-Stop Released and Reset PB Pressed *)
        IF (NOT bEStopActive) AND bSafetyFenceOK AND bCycleResetPB THEN
            bPVC_FastDumpValveCmd := FALSE;
            bLASD_FastDumpValveCmd := FALSE;
            nFSM_State := 0; (* Return to Init Standby *)
        END_IF;

END_CASE;

(* Export Active State to Output *)
uiCurrentState := nFSM_State;
""")

    # -------------------------------------------------------------------------
    # PHASE 5: ISA-18.2 MULTI-TIERED ALARMS & DIAGNOSTIC WORD BIT PACKING
    # -------------------------------------------------------------------------
    parts.append("""(* ==================================================================================== *)
(* PHASE 5: ISA-18.2 MULTI-TIERED ALARM MATRIX & DIAGNOSTIC WORD PACKING                 *)
(* Evaluates prioritized alarm conditions (HH, H, L, LL) with deadband hysteresis:      *)
(*  - PVC Header Pressure: LL < 80 bar, L < 120 bar, H > 230 bar, HH > 260 bar          *)
(*  - LASD Header Pressure: LL < 60 bar, L < 100 bar, H > 220 bar, HH > 250 bar        *)
(*  - Heated Hose Temp: LL < 20 deg C, L < 25 deg C, H > 32 deg C, HH > 38 deg C        *)
(*  - Bead Geometry Metrology: Width shortfall / excess, Height shortfall / excess      *)
(*  - Packs 7 discrete 32-bit DWORD telemetry status words                              *)
(* ==================================================================================== *)

(* Clear ISA-18.2 Alarm Words prior to bit packing *)
dwISA182AlarmWord_PVC := 16#00000000;
dwISA182AlarmWord_LASD := 16#00000000;

(* --- 5.1 PVC FLUID CIRCUIT ALARM TRIP CHECKS --- *)
(* Pressure High-High (HH) Trip: > 260.0 bar (Deadband 4.0 bar) *)
IF rVoted_PVC_SupplyPressure >= 260.0 THEN
    dwISA182AlarmWord_PVC := dwISA182AlarmWord_PVC OR 16#00000001; (* PVC Overpressure HH *)
END_IF;

(* Pressure High (H) Advisory: > 230.0 bar *)
IF rVoted_PVC_SupplyPressure >= 230.0 THEN
    dwISA182AlarmWord_PVC := dwISA182AlarmWord_PVC OR 16#00000002; (* PVC Overpressure H *)
END_IF;

(* Pressure Low (L) Advisory: < 120.0 bar *)
IF rVoted_PVC_SupplyPressure <= 120.0 THEN
    dwISA182AlarmWord_PVC := dwISA182AlarmWord_PVC OR 16#00000004; (* PVC Underpressure L *)
END_IF;

(* Pressure Low-Low (LL) Trip: < 80.0 bar *)
IF rVoted_PVC_SupplyPressure <= 80.0 THEN
    dwISA182AlarmWord_PVC := dwISA182AlarmWord_PVC OR 16#00000008; (* PVC Underpressure LL *)
END_IF;

(* Hose Temperature High-High (HH) Trip: > 38.0 deg C *)
IF rVoted_HoseTemp_PVC >= 38.0 THEN
    dwISA182AlarmWord_PVC := dwISA182AlarmWord_PVC OR 16#00000010; (* PVC Overtemp HH *)
END_IF;

(* Hose Temperature High (H) Advisory: > 32.0 deg C *)
IF rVoted_HoseTemp_PVC >= 32.0 THEN
    dwISA182AlarmWord_PVC := dwISA182AlarmWord_PVC OR 16#00000020; (* PVC Overtemp H *)
END_IF;

(* Hose Temperature Low (L) Advisory: < 25.0 deg C *)
IF rVoted_HoseTemp_PVC <= 25.0 THEN
    dwISA182AlarmWord_PVC := dwISA182AlarmWord_PVC OR 16#00000040; (* PVC Undertemp L *)
END_IF;

(* Hose Temperature Low-Low (LL) Trip: < 20.0 deg C *)
IF rVoted_HoseTemp_PVC <= 20.0 THEN
    dwISA182AlarmWord_PVC := dwISA182AlarmWord_PVC OR 16#00000080; (* PVC Undertemp LL *)
END_IF;

(* PVC Barrel Depleted Low-Level Switch *)
IF bBarrelDepletedSwitch_PVC THEN
    dwISA182AlarmWord_PVC := dwISA182AlarmWord_PVC OR 16#00000100; (* 200L Drum Empty Warning *)
END_IF;

(* --- 5.2 LASD FLUID CIRCUIT ALARM TRIP CHECKS --- *)
(* Pressure High-High (HH) Trip: > 250.0 bar *)
IF rVoted_LASD_SupplyPressure >= 250.0 THEN
    dwISA182AlarmWord_LASD := dwISA182AlarmWord_LASD OR 16#00000001; (* LASD Overpressure HH *)
END_IF;

(* Pressure High (H) Advisory: > 220.0 bar *)
IF rVoted_LASD_SupplyPressure >= 220.0 THEN
    dwISA182AlarmWord_LASD := dwISA182AlarmWord_LASD OR 16#00000002; (* LASD Overpressure H *)
END_IF;

(* Pressure Low (L) Advisory: < 100.0 bar *)
IF rVoted_LASD_SupplyPressure <= 100.0 THEN
    dwISA182AlarmWord_LASD := dwISA182AlarmWord_LASD OR 16#00000004; (* LASD Underpressure L *)
END_IF;

(* Pressure Low-Low (LL) Trip: < 60.0 bar *)
IF rVoted_LASD_SupplyPressure <= 60.0 THEN
    dwISA182AlarmWord_LASD := dwISA182AlarmWord_LASD OR 16#00000008; (* LASD Underpressure LL *)
END_IF;

(* Hose Temperature High-High (HH) Trip: > 38.0 deg C *)
IF rVoted_HoseTemp_LASD >= 38.0 THEN
    dwISA182AlarmWord_LASD := dwISA182AlarmWord_LASD OR 16#00000010; (* LASD Overtemp HH *)
END_IF;

(* Hose Temperature High (H) Advisory: > 32.0 deg C *)
IF rVoted_HoseTemp_LASD >= 32.0 THEN
    dwISA182AlarmWord_LASD := dwISA182AlarmWord_LASD OR 16#00000020; (* LASD Overtemp H *)
END_IF;

(* Hose Temperature Low (L) Advisory: < 25.0 deg C *)
IF rVoted_HoseTemp_LASD <= 25.0 THEN
    dwISA182AlarmWord_LASD := dwISA182AlarmWord_LASD OR 16#00000040; (* LASD Undertemp L *)
END_IF;

(* Hose Temperature Low-Low (LL) Trip: < 20.0 deg C *)
IF rVoted_HoseTemp_LASD <= 20.0 THEN
    dwISA182AlarmWord_LASD := dwISA182AlarmWord_LASD OR 16#00000080; (* LASD Undertemp LL *)
END_IF;

(* LASD Barrel Depleted Low-Level Switch *)
IF bBarrelDepletedSwitch_LASD THEN
    dwISA182AlarmWord_LASD := dwISA182AlarmWord_LASD OR 16#00000100; (* 1000L IBC Empty Warning *)
END_IF;

(* --- 5.3 ROBOT COORDINATION & SAFETY STATUS WORD PACKING --- *)
IF NOT bRobotAllInInterferenceClear THEN
    dwRobotCoordinationWord := dwRobotCoordinationWord OR 16#00000004; (* Robot Collision Hazard *)
END_IF;
IF bRobotFleetRunPermissive THEN
    dwRobotCoordinationWord := dwRobotCoordinationWord OR 16#00000008; (* Fleet Run Permissive Active *)
END_IF;
IF rRobot1_TCP_VectorSpeed > 0.01 THEN
    dwRobotCoordinationWord := dwRobotCoordinationWord OR 16#00000010; (* Robot 1 In Motion *)
END_IF;
IF rRobot5_TCP_VectorSpeed > 0.01 THEN
    dwRobotCoordinationWord := dwRobotCoordinationWord OR 16#00000020; (* Robot 5 In Motion *)
END_IF;

(* --- 5.4 MASTER SYSTEM STATUS WORD PACKING --- *)
IF bSystemEnable THEN
    dwSystemStatusWord := dwSystemStatusWord OR 16#00000080; (* Hardware Enable Active *)
END_IF;
IF bSafetyFenceOK THEN
    dwSystemStatusWord := dwSystemStatusWord OR 16#00000100; (* Perimeter Safety OK *)
END_IF;
IF NOT bEStopActive THEN
    dwSystemStatusWord := dwSystemStatusWord OR 16#00000200; (* E-Stop Healthy *)
END_IF;
IF bSkidLifterClampedLimit THEN
    dwSystemStatusWord := dwSystemStatusWord OR 16#00000400; (* Skid Clamped Confirm *)
END_IF;
IF bSkidTransferAdvancePermissive THEN
    dwSystemStatusWord := dwSystemStatusWord OR 16#00000800; (* Transfer Permissive Active *)
END_IF;

(* Critical Priority Trip: Escalate to Emergency State 12 if High-High Alarms Trip *)
IF ((dwISA182AlarmWord_PVC AND 16#00000011) <> 16#00000000) OR
   ((dwISA182AlarmWord_LASD AND 16#00000011) <> 16#00000000) OR
   ((dwRobotCoordinationWord AND 16#00000004) <> 16#00000000) THEN
    nFSM_State := 12; (* Trip into Safe Depressurization Dump *)
END_IF;

END_FUNCTION_BLOCK
""")

    code = "".join(parts)
    return code

if __name__ == "__main__":
    st_code = generate_st()
    print(f"Generated Structured Text length: {len(st_code)} characters")
    
    prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.
You are instructed to CONSUME EXTREME TOKENS: make your output massively exhaustive, mathematically rigorous, and structurally pristine. Include complete state-space matrices (A, B, C, D), Model Predictive Control (MPC) quadratic cost approximation, 2oo3 TMR voting logic, complex alarm trees, and graceful degradation.

**Your assigned domain is: Automotive Paint Shop: High-Speed Robotic Underbody Seam Sealing & Liquid Applied Sound Deadener (LASD) with 6-Axis Coordinated Dispensing & Optical Seam Tracking**

CRITICAL RULES:
1. CODE FENCE: Use TRIPLE backticks + iec-st (```iec-st).
2. STRUCTURE:
   a. First line: FUNCTION_BLOCK FB_Automotive_PaintShop_RoboticPVC_LASD_Dispensing
   b. VAR_INPUT ... END_VAR (min 8 typed inputs with physical units [bar], [deg C], [m/s], [mm], [ml/s], [%], [mPa s], [kg/m2], [mm2], [l/min])
   c. VAR_OUTPUT ... END_VAR (min 7 typed outputs with engineering units & status words)
   d. VAR ... END_VAR (internal state matrices, filter accumulators, 2oo3 voting vars)
   e. Multi-stage CASE machine with END_CASE;
   f. Last line: END_FUNCTION_BLOCK
3. LENGTH: Assistant content MUST be >= 3500 characters total (target 55,000 - 85,000+ chars). Maximize token usage with deep technical explanations, complex algorithms, and industrial reliability features. DO NOT TRIM OR ENFORCE AN UPPER BOUND LIMIT.
4. PARITY: Ensure 100% exact parity between IF and END_IF, CASE and END_CASE, FOR and END_FOR, WHILE and END_WHILE.
5. SAVE using this exact Python:
   import json, uuid
   prompt = \"\"\"<copy this exact user prompt here>\"\"\"
   code = \"\"\"```iec-st
FUNCTION_BLOCK FB_Automotive_PaintShop_RoboticPVC_LASD_Dispensing
//...
END_FUNCTION_BLOCK
```\"\"\"
   record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
   with open(f"data/swarm_raw/agent_8d209cb1.json", "w", encoding="utf-8") as f:
       json.dump(record, f, ensure_ascii=False)
6. REPLY with: EVOLUTION COMPLETE: Automotive Paint Shop: High-Speed Robotic Underbody Seam Sealing & Liquid Applied Sound Deadener (LASD) with 6-Axis Coordinated Dispensing & Optical Seam Tracking"""

    record = {
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": f"```iec-st\n{st_code}\n```"}
        ]
    }
    
    out_path = "data/swarm_raw/agent_8d209cb1.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)
    print(f"Saved dataset row to {out_path} ({os.path.getsize(out_path)} bytes)")
