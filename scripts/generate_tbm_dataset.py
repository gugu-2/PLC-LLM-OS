# -*- coding: utf-8 -*-
"""
Generator script for FB_HeavyCivil_TBM_EPBCutterhead_SlurryPressure
IEC 61131-3 Structured Text Synthetic Dataset
"""

import os
import json
import uuid

def generate_iec_code():
    code = '''```iec-st
FUNCTION_BLOCK FB_HeavyCivil_TBM_EPBCutterhead_SlurryPressure
(*
 ====================================================================================================
  PROJECT:       15.2-METER LARGE-DIAMETER EARTH PRESSURE BALANCE (EPB) / SLURRY DUAL-MODE TBM
  SUBSYSTEM:     CUTTERHEAD MULTI-MOTOR TORQUE COORDINATION & EXCAVATION CHAMBER PRESSURE STABILIZATION
  DISCIPLINE:    HEAVY CIVIL INFRASTRUCTURE / TUNNELING MECHATRONICS / ADVANCED CYBER-PHYSICAL MPC
  IEC STANDARD:  IEC 61131-3 3RD EDITION (DETERMINISTIC EMBEDDED EXECUTION)
  SAFETY NORMS:  EN 16191 (SAFETY OF TUNNELING MACHINERY), EN ISO 13849-1 (CAT 3, PL d SIL 2)
  GEOTECHNICAL:  TERZAGHI EFFECTIVE STRESS BALANCE & BINGHAM PLASTIC CONDITIONED MUCK RHEOLOGY
  AUTHOR:        LUMINA SYNTHETIC DATA ARCHITECT (V7 MAX-PERSONA: CPS AUTOMATION FELLOW & CHAIR)
 ====================================================================================================

  1. COMPREHENSIVE CYBER-PHYSICAL ENGINEERING CONTEXT & SYSTEM ARCHITECTURE:
  ----------------------------------------------------------------------------------------------------
  This Function Block provides real-time deterministic cyber-physical control, multi-variable Model
  Predictive Control (MPC), Triple Modular Redundant (2oo3 TMR) sensor voting, multi-motor load-sharing,
  and ISA-18.2 certified alarm management for a massive 15.2-meter outer diameter Earth Pressure Balance
  (EPB) and Slurry Dual-Mode Tunnel Boring Machine (TBM).

  The machine is deployed in complex sub-sea / urban soft ground tunneling traversing heterogeneous mixed
  face geology comprising water-bearing sands, gravels, high-permeability cobble layers, and fractured
  weathered bedrock beneath a hydrostatic groundwater head of up to 45.0 meters water column (mWC).

  A. CUTTERHEAD DRIVE TRAIN & TORQUE DYNAMICS:
     - The cutterhead is driven by 16 x 350 kW squirrel-cage induction electric motors (total rated power
       5.6 MW, continuous rated mechanical torque 38,000 kNm, maximum intermittent breakout torque up
       to 48,000 kNm) fed by individual 4-quadrant active front end (AFE) Variable Frequency Drives (VFDs).
     - Each drive motor couples through an elastomeric torsional vibration damping coupling into a multi-
       stage planetary reduction gearbox (gear ratio i = 185.4:1). The planetary output pinions mesh
       directly with an internal spur ring gear integral to a 10.5-meter diameter three-row roller
       slewing main bearing.
     - Dynamic load-sharing is critical: slight structural flexure of the machine front shield under
       220,000 kN thrust introduces pinion-gear center-distance variations, inducing catastrophic torque
       imbalances across the 16 drives. This block executes high-speed droop-based torque load sharing
       with active torque ripple damping to eliminate gearbox backlash impact and prevent pinion tooth
       root fatigue scuffing.

  B. EXCAVATION CHAMBER PRESSURE EQUILIBRIUM & 2oo3 TMR BULKHEAD INSTRUMENTATION:
     - Excavation face stability is maintained by strictly balancing the combined total horizontal stress:
         sigma_h0 = K0 * sigma_v' + u_w
       where K0 is the at-rest earth pressure coefficient (0.45 - 0.65), sigma_v' is effective overburden
       stress, and u_w is hydrostatic pore water pressure.
     - Bulkhead pressure must be held within a narrow envelope of target +/- 0.15 bar:
       * Under-pressurization (< L / LL thresholds) induces ground volume loss, leading to catastrophic
         surface settlement troughs, subterranean utility shearing, and sinkhole face collapse.
       * Over-pressurization (> H / HH thresholds) exceeds the passive geotechnical limit (Kp) and soil
         shear strength, causing hydraulic fracturing, bentonite slurry blowouts to surface/seabed,
         and catastrophic ground heave.
     - The bulkhead crown (the critical high-risk top 120-degree arc where blowout or collapse initiates)
       is instrumented with 3 heavy-duty flush-mounted piezoresistive diaphragm earth pressure transmitters
       (PT101, PT102, PT103). The block executes a hardened 2oo3 voting ladder with online discrepancy
       isolation (0.35 bar divergence threshold), discrepancy integration timers, bumpless failover
       to 1oo2, and springline hydrostatic extrapolation backup.

  C. VARIABLE-SPEED DISCHARGE SCREW CONVEYOR & MASS FLOW BALANCE:
     - Conditioned muck is continuously evacuated from the bottom of the excavation chamber through a
       1.2-meter diameter, 14.5-meter long variable-pitch twin-drive discharge screw conveyor driven by
       secondary electric/hydraulic motors operating from 0.0 to 22.0 RPM.
     - A hydraulic guillotine gate and variable choke discharge cone create controlled friction drop,
       dissipating up to 4.5 bar chamber pressure down to 0 bar atmospheric discharge.
     - Real-time mass flow displacement balance matches theoretical excavated in-situ volume
       V_th = (pi * D^2 / 4) * v_advance against continuous nuclear/belt-scale mass rate measurement
       W_muck [t/h], detecting over-excavation (sinkhole formation) or under-excavation (compaction plug).

  D. BENTONITE FOAM & POLYMER SOIL CONDITIONING SYSTEM:
     - To transform permeable sand/gravel into an impermeable, plastic, compressible paste satisfying
       Bingham plastic rheology (yield stress tau_0 = 50 - 150 Pa, plastic viscosity mu_p = 10 - 30 Pa*s),
       the block regulates multi-nozzle injection lines delivering compressed air, surfactant foam solution
       (Foam Expansion Ratio FER 8 - 15, Foam Injection Ratio FIR 30% - 60%), and high-molecular-weight
       polymer additives.

  E. THRUST PROPULSION SYSTEM & LASER TARGET GUIDANCE COORDINATION:
     - 40 double-acting high-pressure hydraulic thrust cylinders (p_max = 350 bar) grouped into 4 distinct
       spatial quadrants:
       * Quadrant 1 (Q1): Top-Right (10 cylinders)
       * Quadrant 2 (Q2): Bottom-Right (10 cylinders)
       * Quadrant 3 (Q3): Bottom-Left (10 cylinders)
       * Quadrant 4 (Q4): Top-Left (10 cylinders)
     - Total machine thrust capacity: 220,000 kN (22,400 tonnes-force).
     - Proportional-directional servo valves modulate quadrant hydraulic flows to introduce differential
       thrust moments, actively correcting trajectory deviations (pitch, yaw, roll) measured by the laser
       guidance optical target system relative to the Design Tunnel Alignment (DTA).

  F. MULTIVARIABLE STATE-SPACE DISCRETE MODEL & RECEDING-HORIZON MPC:
     - 4-state, 3-input discrete state-space model running at Ts = 50 ms (20 Hz execution rate):
       States:  x1 = Bulkhead Crown Pressure [bar]
                x2 = Total Cutterhead Torque [kNm]
                x3 = Screw Conveyor Fill Ratio [-] (0.0 to 1.0)
                x4 = Thrust Advance Rate [mm/min]
       Inputs:  u1 = Screw Conveyor Speed Command [RPM]
                u2 = Main Thrust Servo Pressure Command [bar]
                u3 = Bentonite Foam Injection Flow Command [%]
     - Projected gradient descent optimization minimizes quadratic error cost J over prediction horizon
       Np = 5 steps and control horizon Nc = 3 steps with strict actuator slew-rate constraints.
*)

VAR_INPUT
    (* ============================================================================================== *)
    (* MASTER SYSTEM PERMISSIVES & OPERATOR CONTROLS                                                 *)
    (* ============================================================================================== *)
    bEnable                         : BOOL;         (* Master Execution Enable [True = Run] *)
    bReset                          : BOOL;         (* Master Alarm & Trip Reset Pulse *)
    bEStopActivated                 : BOOL;         (* EN 16191 Hardwired Emergency Stop [Active Low Safe] *)
    bStartExcavationCmd             : BOOL;         (* Operator Command: Begin Excavation Advance Cycle *)
    bHoldAdvanceCmd                 : BOOL;         (* Operator Command: Pause Advance / Maintain Face Pressure *)
    bRingErectInterlockClear        : BOOL;         (* Erector Interlock: True = Erector Arm Parked & Locked *)
    bToolInspectSelectCmd           : BOOL;         (* Compressed Air Chamber Intervention Mode Request *)
    bAlarmAckCmd                    : BOOL;         (* Operator ISA-18.2 Alarm Acknowledgment Pushbutton *)

    (* ============================================================================================== *)
    (* GEOTECHNICAL & PROCESS SETPOINTS                                                               *)
    (* ============================================================================================== *)
    rTargetChamberPressure_bar      : REAL;         (* Geotechnical Target Earth/Slurry Face Pressure [bar] (1.50 .. 4.50) *)
    rTargetAdvanceRate_mm_min       : REAL;         (* Target TBM Penetration Advance Speed [mm/min] (0.0 .. 60.0) *)
    rTargetCutterheadSpeed_RPM      : REAL;         (* Nominal Cutterhead Rotation Speed Target [RPM] (0.0 .. 3.20) *)
    rSoilSpecificWeight_kN_m3       : REAL;         (* Saturated In-situ Soil Unit Weight [kN/m3] (18.5 .. 22.0) *)
    rGroundwaterHead_mWC            : REAL;         (* Hydrostatic Water Head Above Bulkhead Crown [mWC] (0.0 .. 50.0) *)

    (* ============================================================================================== *)
    (* 2oo3 TRIPLE MODULAR REDUNDANT (TMR) BULKHEAD PRESSURE TRANSDUCERS                              *)
    (* ============================================================================================== *)
    rCrownPressure_PT101_bar        : REAL;         (* Bulkhead Crown Diaphragm Pressure Transmitter A [bar] (0.0 .. 10.0) *)
    rCrownPressure_PT102_bar        : REAL;         (* Bulkhead Crown Diaphragm Pressure Transmitter B [bar] (0.0 .. 10.0) *)
    rCrownPressure_PT103_bar        : REAL;         (* Bulkhead Crown Diaphragm Pressure Transmitter C [bar] (0.0 .. 10.0) *)

    (* ============================================================================================== *)
    (* AUXILIARY BULKHEAD WALL PRESSURE SENSORS (HYDROSTATIC PROFILE MONITORING)                      *)
    (* ============================================================================================== *)
    rBulkheadPressure_Spring_L_bar  : REAL;         (* Left Springline Wall Pressure Transmitter [bar] (0.0 .. 10.0) *)
    rBulkheadPressure_Spring_R_bar  : REAL;         (* Right Springline Wall Pressure Transmitter [bar] (0.0 .. 10.0) *)
    rBulkheadPressure_Invert_bar    : REAL;         (* Invert / Bulkhead Bottom Pressure Transmitter [bar] (0.0 .. 10.0) *)

    (* ============================================================================================== *)
    (* 16-MOTOR CUTTERHEAD DRIVE VFD FEEDBACK ARRAYS                                                  *)
    (* ============================================================================================== *)
    aMotorTorques_kNm               : ARRAY[1..16] OF REAL;  (* Motor Pinion Shaft Mechanical Torques [kNm] (-500.0 .. 4000.0) *)
    aMotorSpeeds_RPM                : ARRAY[1..16] OF REAL;  (* Motor Rotor Shaft Speeds [RPM] (0.0 .. 1800.0) *)
    aMotorTemperatures_C            : ARRAY[1..16] OF REAL;  (* Stator Winding PT100 RTD Temperatures [deg C] (0.0 .. 180.0) *)
    aMotorVFD_Fault                 : ARRAY[1..16] OF BOOL;  (* VFD Hardware Trip / Overcurrent Status Flags [True = Fault] *)

    (* ============================================================================================== *)
    (* HYDRAULIC PROPULSION THRUST CYLINDER FEEDBACKS (4 QUADRANTS)                                   *)
    (* ============================================================================================== *)
    rThrustPressure_Q1_bar          : REAL;         (* Quadrant 1 (Top-Right) Hydraulic Pressure [bar] (0.0 .. 380.0) *)
    rThrustPressure_Q2_bar          : REAL;         (* Quadrant 2 (Bottom-Right) Hydraulic Pressure [bar] (0.0 .. 380.0) *)
    rThrustPressure_Q3_bar          : REAL;         (* Quadrant 3 (Bottom-Left) Hydraulic Pressure [bar] (0.0 .. 380.0) *)
    rThrustPressure_Q4_bar          : REAL;         (* Quadrant 4 (Top-Left) Hydraulic Pressure [bar] (0.0 .. 380.0) *)
    rCylinderStroke_Avg_mm          : REAL;         (* Average Thrust Cylinder Extension Stroke [mm] (0.0 .. 2200.0) *)
    rAdvanceRateActual_mm_min       : REAL;         (* Actual TBM Forward Advance Velocity [mm/min] (0.0 .. 60.0) *)

    (* ============================================================================================== *)
    (* DISCHARGE SCREW CONVEYOR & MUCK SCALE INSTRUMENTATION                                          *)
    (* ============================================================================================== *)
    rScrewConveyorSpeedActual_RPM   : REAL;         (* Screw Conveyor Tachometer Speed Feedback [RPM] (0.0 .. 25.0) *)
    rScrewConveyorTorque_kNm        : REAL;         (* Screw Drive Hydraulic/Electric Torque [kNm] (0.0 .. 450.0) *)
    rScrewMuckGateOpening_pct       : REAL;         (* Discharge Choke Guillotine Gate Actual Position [%] (0.0 .. 100.0) *)
    rMuckBeltScale_MassFlow_t_h     : REAL;         (* Continuous Nuclear/Belt Scale Muck Mass Flow [t/h] (0.0 .. 3500.0) *)

    (* ============================================================================================== *)
    (* BENTONITE SLURRY, FOAM & POLYMER CONDITIONING INSTRUMENTATION                                  *)
    (* ============================================================================================== *)
    rBentoniteFlowActual_L_min      : REAL;         (* Slurry Injection Total Mass Flow Rate [L/min] (0.0 .. 4000.0) *)
    rFoamAirPressure_bar            : REAL;         (* Conditioning Compressed Air Injection Pressure [bar] (0.0 .. 8.0) *)
    rFoamLiquidFlowActual_L_min     : REAL;         (* Foaming Solution Liquid Surfactant Flow [L/min] (0.0 .. 600.0) *)
    rPolymerDosingRate_L_min        : REAL;         (* High Molecular Polymer Injection Flow Rate [L/min] (0.0 .. 120.0) *)

    (* ============================================================================================== *)
    (* MAIN SLEWING BEARING LUBRICATION & DIAGNOSTIC TRANSDUCERS                                      *)
    (* ============================================================================================== *)
    rMainBearingOilTemp_C           : REAL;         (* Main Roller Slewing Bearing Sump Temp [deg C] (0.0 .. 120.0) *)
    rMainBearingWaterContent_ppm    : REAL;         (* Sump Lubricant Moisture / Water Ingress Sensor [ppm] (0.0 .. 2000.0) *)
    rMainBearingSealPressure_bar    : REAL;         (* Outer Triple Lip Seal Cavity Grease Pressure [bar] (0.0 .. 12.0) *)

    (* ============================================================================================== *)
    (* LASER TARGET GUIDANCE SYSTEM & ARTICULATED STEERING FEEDBACK                                   *)
    (* ============================================================================================== *)
    rLaserDeviationHoriz_mm         : REAL;         (* DTA Target Horizontal Alignment Offset [mm] (-250.0 .. +250.0) *)
    rLaserDeviationVert_mm          : REAL;         (* DTA Target Vertical Alignment Offset [mm] (-250.0 .. +250.0) *)
    rTBM_Pitch_deg                  : REAL;         (* Machine Longitudinal Pitch Inclinometer [deg] (-5.0 .. +5.0) *)
    rTBM_Roll_deg                   : REAL;         (* Machine Shield Torsional Roll Inclinometer [deg] (-3.0 .. +3.0) *)

    (* ============================================================================================== *)
    (* SYSTEM TIMING & DISCRETE CLOCK                                                                 *)
    (* ============================================================================================== *)
    rScanTime_s                     : REAL;         (* Discrete Task Scan Time Cycle [s] (e.g. 0.050 s = 50ms) *)
END_VAR

VAR_OUTPUT
    (* ============================================================================================== *)
    (* WORD-PACKED STATE REGISTERS & DIAGNOSTIC TELEMETRY                                             *)
    (* ============================================================================================== *)
    wStateStatusWord                : WORD;         (* Packaged FSM Operational Status Register *)
    wAlarmWord_Priority1            : WORD;         (* ISA-18.2 Critical Trip & Emergency Alarms Register *)
    wAlarmWord_Priority2            : WORD;         (* ISA-18.2 Warning & Process Deviation Register *)
    wDiagnosticWord                 : DWORD;        (* Detailed Diagnostic Telemetry & Degraded Modes *)

    (* ============================================================================================== *)
    (* CUTTERHEAD MULTI-MOTOR ACTUATOR TARGETS                                                        *)
    (* ============================================================================================== *)
    rCutterheadSpeedTarget_RPM      : REAL;         (* Master Coordinated Cutterhead Speed Target [RPM] (0.0 .. 3.20) *)
    aMotorTorqueLimits_kNm          : ARRAY[1..16] OF REAL; (* Coordinated Torque Limits for 16 Pinion Drives [kNm] *)
    rCutterheadTotalTorque_kNm      : REAL;         (* Total Measured Mechanical Cutterhead Torque [kNm] *)
    rCutterheadTorqueImbalance_pct  : REAL;         (* Torque Imbalance Variance Across Pinions [%] *)

    (* ============================================================================================== *)
    (* PROCESS ACTUATION COMMANDS (MPC OPTIMIZED)                                                     *)
    (* ============================================================================================== *)
    rScrewConveyorSpeedCmd_RPM      : REAL;         (* Commanded Discharge Screw Velocity [RPM] (0.0 .. 22.0) *)
    rScrewMuckGatePositionCmd_pct   : REAL;         (* Commanded Discharge Guillotine Choke Gate [%] (0.0 .. 100.0) *)
    rThrustPressureSetpoint_bar     : REAL;         (* Main Propulsion Hydraulic Pump Setpoint [bar] (0.0 .. 350.0) *)
    rThrustAdvanceRateCmd_mm_min    : REAL;         (* Commanded Advance Penetration Velocity [mm/min] (0.0 .. 60.0) *)
    aQuadrantThrustBias_pct         : ARRAY[1..4] OF REAL; (* Guidance Steering Quadrant Flow Trim [%] (-30.0 .. +30.0) *)
    rTotalThrustForce_kN            : REAL;         (* Instantaneous Total Vector Thrust Force [kN] *)

    (* ============================================================================================== *)
    (* BENTONITE SLURRY & CONDITIONING ACTUATOR OUTPUTS                                               *)
    (* ============================================================================================== *)
    rBentonitePumpCmd_pct           : REAL;         (* Primary Bentonite Slurry Feed Pump Command [%] (0.0 .. 100.0) *)
    rFoamAirValveCmd_pct            : REAL;         (* Compressed Air Chamber Conditioning Valve [%] (0.0 .. 100.0) *)
    rPolymerPumpCmd_pct             : REAL;         (* Polymer Injection Dosing Pump Stroke Command [%] (0.0 .. 100.0) *)

    (* ============================================================================================== *)
    (* VOTED PRESSURES & GEOTECHNICAL MONITORING METRICS                                              *)
    (* ============================================================================================== *)
    rBulkheadCrownPressure_Voted_bar: REAL;         (* 2oo3 TMR High-Reliability Voted Crown Earth Pressure [bar] *)
    rBulkheadMeanPressure_bar       : REAL;         (* Hydrostatically Area-Weighted Bulkhead Face Pressure [bar] *)
    rBulkheadPressureGradient_bar_m : REAL;         (* Vertical Pressure Gradient Across Bulkhead [bar/m] *)
    rMuckDischargeRatio             : REAL;         (* Measured/Theoretical Muck Volumetric Displacement Ratio [-] *)

    (* ============================================================================================== *)
    (* DISCRETE STATUS & SAFETY INTERLOCK FLAGS                                                       *)
    (* ============================================================================================== *)
    bChamberPressureStabilized      : BOOL;         (* Bulkhead Pressure Within Geotechnical Deadband (+/- 0.15 bar) *)
    bRingAdvanceComplete            : BOOL;         (* Full Segment Ring Stroke (2,000 mm) Achieved *)
    bEmergencyStopTriggered         : BOOL;         (* Emergency Stop Shutdown Latch Active *)
    bDegradedSensorMode             : BOOL;         (* Operating in 1oo2 or Fallback Sensor Mode *)
    bObstacleDetected               : BOOL;         (* High Resistance Boulder / Mixed-Face Obstacle Encountered *)
END_VAR

VAR
    (* ============================================================================================== *)
    (* FINITE STATE MACHINE (FSM) STEP CONTROL & TIMERS                                               *)
    (* ============================================================================================== *)
    nState                          : INT := 0;     (* Current Operational Step Index *)
    nPrevState                      : INT := -1;    (* Previous Step Index for Transition Edge Detection *)
    rStateTimer_s                   : REAL := 0.0;  (* Continuous In-State Elapsed Timer [s] *)
    bStateFirstScan                 : BOOL := TRUE; (* First-Scan Pulse Inside Active FSM Step *)
    nSubState                       : INT := 0;     (* Internal Sub-State Execution Step *)

    (* ============================================================================================== *)
    (* 2oo3 TMR SENSOR VOTING INTERNAL VARIABLES & TIMERS                                             *)
    (* ============================================================================================== *)
    rPT101_Filtered_bar             : REAL := 0.0;  (* First-Order Low-Pass Filtered Signal PT101 [bar] *)
    rPT102_Filtered_bar             : REAL := 0.0;  (* First-Order Low-Pass Filtered Signal PT102 [bar] *)
    rPT103_Filtered_bar             : REAL := 0.0;  (* First-Order Low-Pass Filtered Signal PT103 [bar] *)
    rDev_12_bar                     : REAL := 0.0;  (* Absolute Deviation |PT101 - PT102| [bar] *)
    rDev_23_bar                     : REAL := 0.0;  (* Absolute Deviation |PT102 - PT103| [bar] *)
    rDev_31_bar                     : REAL := 0.0;  (* Absolute Deviation |PT103 - PT101| [bar] *)
    rPT101_DiscrepancyTimer_s       : REAL := 0.0;  (* Persistent Discrepancy Integrator for PT101 [s] *)
    rPT102_DiscrepancyTimer_s       : REAL := 0.0;  (* Persistent Discrepancy Integrator for PT102 [s] *)
    rPT103_DiscrepancyTimer_s       : REAL := 0.0;  (* Persistent Discrepancy Integrator for PT103 [s] *)
    bPT101_Failed                   : BOOL := FALSE;(* Sensor PT101 Latched Hardware Failure Flag *)
    bPT102_Failed                   : BOOL := FALSE;(* Sensor PT102 Latched Hardware Failure Flag *)
    bPT103_Failed                   : BOOL := FALSE;(* Sensor PT103 Latched Hardware Failure Flag *)
    nHealthySensorCount             : INT := 3;     (* Number of Valid Transmitters in Crown Cluster (0..3) *)
    rCrownPressure_RawVoted_bar     : REAL := 0.0;  (* Unfiltered Voted Pressure Result [bar] *)
    rCrownPressure_PrevVoted_bar    : REAL := 0.0;  (* Rate-of-Change Limiting Tracking Memory [bar] *)

    (* ============================================================================================== *)
    (* DISCRETE STATE-SPACE MODEL MATRICES & VECTORS (Ts = 50ms)                                      *)
    (* States x = [P_crown (bar), Torque (kNm), Fill_Ratio (-), Advance_Rate (mm/min)]                *)
    (* Inputs u = [Screw_RPM (RPM), Thrust_Servo_Press (bar), Foam_Valve (%)]                         *)
    (* ============================================================================================== *)
    matA                            : ARRAY[1..4, 1..4] OF REAL; (* Discrete State Transition Matrix A *)
    matB                            : ARRAY[1..4, 1..3] OF REAL; (* Discrete Input Coupling Matrix B *)
    matC                            : ARRAY[1..4, 1..4] OF REAL; (* Output Observation Matrix C *)
    matL_Obs                        : ARRAY[1..4, 1..4] OF REAL; (* Luenberger Observer Correction Gain Matrix *)
    vecX_hat                        : ARRAY[1..4] OF REAL;       (* Estimated / Filtered State Vector x_hat[k] *)
    vecX_pred                       : ARRAY[1..4] OF REAL;       (* Dynamic State Prediction Vector x_pred[k+1] *)
    vecX_ref                        : ARRAY[1..4] OF REAL;       (* Target State Reference Trajectory Vector *)
    vecU_cmd                        : ARRAY[1..3] OF REAL;       (* Active Control Input Vector u[k] *)
    vecU_prev                       : ARRAY[1..3] OF REAL;       (* Slew-Rate Memory Control Input Vector u[k-1] *)
    vecY_meas                       : ARRAY[1..4] OF REAL;       (* Plant Physical Output Feedback Vector y[k] *)
    vecY_err                        : ARRAY[1..4] OF REAL;       (* Observer Innovation Error Vector e_obs[k] *)

    (* ============================================================================================== *)
    (* MODEL PREDICTIVE CONTROL (MPC) QUADRATIC COST WEIGHTING MATRICES & SOLVER STORAGE              *)
    (* ============================================================================================== *)
    diagQ                           : ARRAY[1..4] OF REAL; (* State Tracking Error Quadratic Penalty Q *)
    diagR                           : ARRAY[1..3] OF REAL; (* Control Actuation Slew Effort Penalty R *)
    diagP                           : ARRAY[1..4] OF REAL; (* Terminal State Error Quadratic Penalty P *)
    matHorizStates                  : ARRAY[1..5, 1..4] OF REAL; (* Predicted State Trajectory across Horizon Np=5 *)
    matHorizInputs                  : ARRAY[1..5, 1..3] OF REAL; (* Control Input Plan across Horizon Nc=3 *)
    vecGradJ                        : ARRAY[1..3] OF REAL; (* Calculated Gradient Vector dJ/du at Active Step *)
    vecDeltaU_opt                   : ARRAY[1..3] OF REAL; (* Optimal Projected Control Adjustment du* *)
    rMPC_StepSize                   : REAL := 0.0425;      (* Gradient Descent Convergence Step Parameter *)
    rCostJ                          : REAL := 0.0;         (* Instantaneous Quadratic Cost Functional Value *)

    (* ============================================================================================== *)
    (* 16-MOTOR CUTTERHEAD LOAD-SHARING & ANTI-RIPPLE VARIABLES                                       *)
    (* ============================================================================================== *)
    rMotorTorqueSum_kNm             : REAL := 0.0;  (* Aggregate Instantaneous Mechanical Torque [kNm] *)
    rMotorTorqueMean_kNm            : REAL := 0.0;  (* Instantaneous Average Pinion Torque [kNm] *)
    rMotorTorqueMaxDev_kNm          : REAL := 0.0;  (* Peak Absolute Deviation from Mean Pinion Torque [kNm] *)
    aMotorDroopTrim_RPM             : ARRAY[1..16] OF REAL; (* Individual Motor Speed Trims for Load Equalization *)
    aMotorThermalDerateFactor       : ARRAY[1..16] OF REAL; (* Thermal Derating Multiplier (0.2 .. 1.0) *)
    rTorqueDroopGain                : REAL := 0.00045;      (* Virtual Droop Compliance Gain [RPM / kNm] *)
    rCutterheadSpeedRamp_RPM        : REAL := 0.0;  (* S-Curve Rate-Limited Speed Reference [RPM] *)

    (* ============================================================================================== *)
    (* HYDRAULIC PROPULSION & LASER GUIDANCE STEERING DYNAMICS                                        *)
    (* ============================================================================================== *)
    rThrustPressureBase_bar         : REAL := 0.0;  (* Symmetrical Propulsion Pressure Component [bar] *)
    rSteeringDeltaP_Yaw_bar         : REAL := 0.0;  (* Differential Pressure Bias for Yaw Steering [bar] *)
    rSteeringDeltaP_Pitch_bar       : REAL := 0.0;  (* Differential Pressure Bias for Pitch Steering [bar] *)
    rSteeringDeltaP_Roll_bar        : REAL := 0.0;  (* Counter-Roll Reaction Bias [bar] *)
    aQuadrantPressure_bar           : ARRAY[1..4] OF REAL; (* Synthesized Target Pressures for Quadrants 1..4 *)
    rTotalPistonArea_Quadrant_m2    : REAL := 0.3848;      (* Effective Piston Hydraulic Annular Area Per Quadrant [m2] *)
    rGuidanceGainYaw                : REAL := 0.285;       (* Horizontal Offset Guidance Proportional Gain [bar / mm] *)
    rGuidanceGainPitch              : REAL := 0.315;       (* Vertical Offset Guidance Proportional Gain [bar / mm] *)
    rGuidanceGainRoll               : REAL := 8.500;       (* Roll Offset Inclinometer Proportional Gain [bar / deg] *)

    (* ============================================================================================== *)
    (* MUCK DISPLACEMENT MASS FLOW BALANCE & CONDITIONING METRICS                                     *)
    (* ============================================================================================== *)
    rTheoreticalMuckVolRate_m3_s    : REAL := 0.0;  (* In-Situ Excavated Volume Generation Rate [m3/s] *)
    rMeasuredMuckVolRate_m3_s       : REAL := 0.0;  (* Discharge Belt Volumetric Rate (rho = 1.65 t/m3) [m3/s] *)
    rMuckBalanceErrorIntegral_m3    : REAL := 0.0;  (* Cumulative Mass Balance Volume Discrepancy Integral [m3] *)
    rFoamExpansionRatio_FER         : REAL := 11.2; (* Dynamic Foam Expansion Ratio Calculation [-] *)
    rFoamInjectionRatio_FIR_pct     : REAL := 42.5; (* Foam Injection Ratio to Soil In-Situ Volume [%] *)

    (* ============================================================================================== *)
    (* ISA-18.2 MULTI-TIERED ALARM ENGINE STRUCTURES & TIMERS                                         *)
    (* States: 0=NORM, 1=UNACK_ALARM, 2=ACK_ALARM, 3=UNACK_RTN                                      *)
    (* ============================================================================================== *)
    nAlmState_CrownHH               : INT := 0;     (* Crown Pressure High-High (Blowout / Heave Risk) *)
    nAlmState_CrownH                : INT := 0;     (* Crown Pressure High (Pressure Escalation) *)
    nAlmState_CrownL                : INT := 0;     (* Crown Pressure Low (Ground Settlement Risk) *)
    nAlmState_CrownLL               : INT := 0;     (* Crown Pressure Low-Low (Catastrophic Collapse Abort) *)
    nAlmState_TorqueHH              : INT := 0;     (* Cutterhead Torque High-High (Thermal Overload Trip) *)
    nAlmState_TorqueH               : INT := 0;     (* Cutterhead Torque High (Obstacle Resistance Warning) *)
    nAlmState_WaterHH               : INT := 0;     (* Main Bearing Water Ingress High-High (Seal Failure) *)
    nAlmState_WaterH                : INT := 0;     (* Main Bearing Water Ingress High (Seal Warning) *)
    nAlmState_LubeTempHH            : INT := 0;     (* Main Bearing Oil Temperature High-High Trip *)
    nAlmState_ThrustHydrHH          : INT := 0;     (* Thrust Hydraulic Pressure High-High Relief Trip *)

    rAlmTimer_CrownHH_s             : REAL := 0.0;  (* Persistence Qualification Delay Timer [s] *)
    rAlmTimer_CrownH_s              : REAL := 0.0;
    rAlmTimer_CrownL_s              : REAL := 0.0;
    rAlmTimer_CrownLL_s             : REAL := 0.0;
    rAlmTimer_TorqueHH_s            : REAL := 0.0;
    rAlmTimer_TorqueH_s             : REAL := 0.0;
    rAlmTimer_WaterHH_s             : REAL := 0.0;
    rAlmTimer_WaterH_s              : REAL := 0.0;
    rAlmTimer_LubeTempHH_s          : REAL := 0.0;
    rAlmTimer_ThrustHydrHH_s        : REAL := 0.0;

    (* Alarm Thresholds & Hysteresis Constants *)
    rSp_CrownHH_bar                 : REAL := 4.80; (* Crown Pressure HH Trip Threshold [bar] *)
    rSp_CrownH_bar                  : REAL := 4.20; (* Crown Pressure H Warning Threshold [bar] *)
    rSp_CrownL_bar                  : REAL := 1.80; (* Crown Pressure L Warning Threshold [bar] *)
    rSp_CrownLL_bar                 : REAL := 1.20; (* Crown Pressure LL Abort Threshold [bar] *)
    rHyst_Crown_bar                 : REAL := 0.10; (* Crown Pressure Trip Hysteresis Deadband [bar] *)

    rSp_TorqueHH_kNm                : REAL := 46000.0; (* Cutterhead Breakout Torque Trip [kNm] *)
    rSp_TorqueH_kNm                 : REAL := 40000.0; (* Cutterhead Torque Warning [kNm] *)
    rHyst_Torque_kNm                : REAL := 1200.0;  (* Cutterhead Torque Reset Hysteresis [kNm] *)

    rSp_WaterHH_ppm                 : REAL := 500.0;(* Main Bearing Lube Water Ingress Trip [ppm] *)
    rSp_WaterH_ppm                  : REAL := 250.0;(* Main Bearing Lube Water Ingress Warning [ppm] *)
    rHyst_Water_ppm                 : REAL := 40.0; (* Water Ingress Hysteresis [ppm] *)

    rSp_LubeTempHH_C                : REAL := 75.0; (* Main Bearing Temperature Trip [deg C] *)
    rHyst_LubeTemp_C                : REAL := 4.0;  (* Main Bearing Temperature Hysteresis [deg C] *)

    rSp_ThrustHydrHH_bar            : REAL := 350.0;(* Hydraulic Thrust Pressure Relief [bar] *)
    rHyst_ThrustHydr_bar            : REAL := 12.0; (* Thrust Hydraulic Hysteresis [bar] *)

    (* Multi-Motor Coordination Internal Iterators *)
    iMotor                          : INT := 1;     (* Motor Loop Index *)
    iQuad                           : INT := 1;     (* Quadrant Loop Index *)
    iHoriz                          : INT := 1;     (* MPC Horizon Outer Loop Index *)
    jHoriz                          : INT := 1;     (* MPC Horizon Inner Loop Index *)
    kState                          : INT := 1;     (* State Vector Loop Index *)
    mInput                          : INT := 1;     (* Input Vector Loop Index *)
    rTempSum                        : REAL := 0.0;  (* Intermediate Scalar Math Accumulator *)
    rTempDiff                       : REAL := 0.0;  (* Intermediate Scalar Math Difference *)
    rGradStep                       : REAL := 0.0;  (* Scalar Projected Slew Rate *)
END_VAR

(*
 ====================================================================================================
  INITIALIZATION OF DISCRETE STATE-SPACE MATRICES & MPC PARAMETERS
 ====================================================================================================
  Sampling Scan Period Ts = 0.050 seconds (50 ms).
  Continuous system linearised around nominal excavation operating point:
    P_crown_0 = 2.80 bar, Torque_0 = 24,000 kNm, Fill_0 = 0.72, Advance_Rate_0 = 35.0 mm/min.
    Screw_RPM_0 = 11.5 RPM, Thrust_Press_0 = 210.0 bar, Foam_0 = 45.0%.
*)
IF bStateFirstScan AND (nPrevState = -1) THEN
    (* Discrete State Transition Matrix A (4x4) *)
    matA[1, 1] := 0.9820;  matA[1, 2] := 0.000012; matA[1, 3] := 0.0450;  matA[1, 4] := 0.00185;
    matA[2, 1] := 0.0210;  matA[2, 2] := 0.945000; matA[2, 3] := 12.500;  matA[2, 4] := 38.6500;
    matA[3, 1] := 0.0045;  matA[3, 2] := 0.000005; matA[3, 3] := 0.9650;  matA[3, 4] := 0.00115;
    matA[4, 1] := -0.0520; matA[4, 2] := -0.000180;matA[4, 3] := -0.1250; matA[4, 4] := 0.89500;

    (* Discrete Input Coupling Matrix B (4x3) *)
    matB[1, 1] := -0.01250; matB[1, 2] := 0.000420; matB[1, 3] := 0.00850;
    matB[2, 1] := -4.25000; matB[2, 2] := 8.120000; matB[2, 3] := -2.8500;
    matB[3, 1] := -0.00385; matB[3, 2] := 0.000210; matB[3, 3] := 0.00150;
    matB[4, 1] := 0.00820;  matB[4, 2] := 0.095000; matB[4, 3] := 0.00210;

    (* State Observation Matrix C (4x4 Identity) *)
    matC[1, 1] := 1.0; matC[1, 2] := 0.0; matC[1, 3] := 0.0; matC[1, 4] := 0.0;
    matC[2, 1] := 0.0; matC[2, 2] := 1.0; matC[2, 3] := 0.0; matC[2, 4] := 0.0;
    matC[3, 1] := 0.0; matC[3, 2] := 0.0; matC[3, 3] := 1.0; matC[3, 4] := 0.0;
    matC[4, 1] := 0.0; matC[4, 2] := 0.0; matC[4, 3] := 0.0; matC[4, 4] := 1.0;

    (* Luenberger State Observer Gain Matrix L (4x4) *)
    matL_Obs[1, 1] := 0.2850; matL_Obs[1, 2] := 0.00000; matL_Obs[1, 3] := 0.0050; matL_Obs[1, 4] := 0.0002;
    matL_Obs[2, 1] := 0.0120; matL_Obs[2, 2] := 0.32500; matL_Obs[2, 3] := 0.4500; matL_Obs[2, 4] := 0.8500;
    matL_Obs[3, 1] := 0.0015; matL_Obs[3, 2] := 0.00000; matL_Obs[3, 3] := 0.2450; matL_Obs[3, 4] := 0.0005;
    matL_Obs[4, 1] := -0.008; matL_Obs[4, 2] := -0.00001;matL_Obs[4, 3] := -0.0120;matL_Obs[4, 4] := 0.3150;

    (* MPC Quadratic Error Weighting Matrices *)
    diagQ[1] := 450.0;  (* Extreme penalty on Bulkhead Earth Pressure deviation [bar^-2] *)
    diagQ[2] := 0.025;  (* Penalty on Cutterhead Torque fluctuation [kNm^-2] *)
    diagQ[3] := 85.0;   (* Penalty on Screw Conveyor Fill Ratio packing error [-] *)
    diagQ[4] := 15.0;   (* Penalty on Advance Penetration velocity error [(mm/min)^-2] *)

    diagR[1] := 14.5;   (* Actuator slew penalty on Screw Conveyor Speed [RPM^-2] *)
    diagR[2] := 0.95;   (* Actuator slew penalty on Thrust Hydraulic Pressure [bar^-2] *)
    diagR[3] := 2.80;   (* Actuator slew penalty on Bentonite Foam Air Valve [%^-2] *)

    diagP[1] := 950.0;  (* Terminal state stability weight for Bulkhead Pressure *)
    diagP[2] := 0.050;  (* Terminal state stability weight for Torque *)
    diagP[3] := 160.0;  (* Terminal state stability weight for Fill Ratio *)
    diagP[4] := 35.0;   (* Terminal state stability weight for Advance Velocity *)

    (* Initialize State Estimator Memory *)
    vecX_hat[1] := rTargetChamberPressure_bar;
    vecX_hat[2] := 24000.0;
    vecX_hat[3] := 0.70;
    vecX_hat[4] := rTargetAdvanceRate_mm_min;

    vecU_prev[1] := 10.0;
    vecU_prev[2] := 180.0;
    vecU_prev[3] := 40.0;
END_IF;

(* Continuous Task Clock & First-Scan Edge Logic *)
IF nState <> nPrevState THEN
    rStateTimer_s := 0.0;
    bStateFirstScan := TRUE;
    nPrevState := nState;
ELSE
    rStateTimer_s := rStateTimer_s + rScanTime_s;
    bStateFirstScan := FALSE;
END_IF;

(*
 ====================================================================================================
  PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANT (TMR) BULKHEAD CROWN SENSOR VOTING
 ====================================================================================================
  Three independent piezoresistive diaphragm transducers (PT101, PT102, PT103) measure earth pressure
  at the bulkhead crown. The voting block executes:
  1. Low-pass noise filtering (tau = 0.25 s).
  2. Pairwise divergence computation (|PT_i - PT_j| > 0.35 bar limit).
  3. Continuous discrepancy integration timers (1.50 s trip threshold).
  4. Fault isolation: isolates a single drifting or blown sensor.
  5. 2oo3 Median voting when 3 sensors healthy; bumpless fallback to 1oo2 average if 1 fails;
     degraded single-sensor mode if 2 fail; and hydrostatic springline estimation if all 3 fail.
*)

(* Low-pass noise suppression filtering: y_filt[k] = y_filt[k-1] + alpha * (u[k] - y_filt[k-1]) *)
rPT101_Filtered_bar := rPT101_Filtered_bar + 0.1812 * (rCrownPressure_PT101_bar - rPT101_Filtered_bar);
rPT102_Filtered_bar := rPT102_Filtered_bar + 0.1812 * (rCrownPressure_PT102_bar - rPT102_Filtered_bar);
rPT103_Filtered_bar := rPT103_Filtered_bar + 0.1812 * (rCrownPressure_PT103_bar - rPT103_Filtered_bar);

(* Pairwise deviation computation *)
rDev_12_bar := ABS(rPT101_Filtered_bar - rPT102_Filtered_bar);
rDev_23_bar := ABS(rPT102_Filtered_bar - rPT103_Filtered_bar);
rDev_31_bar := ABS(rPT103_Filtered_bar - rPT101_Filtered_bar);

(* Transmitter PT101 Discrepancy & Health Verification *)
IF (rDev_12_bar > 0.35) AND (rDev_31_bar > 0.35) THEN
    rPT101_DiscrepancyTimer_s := rPT101_DiscrepancyTimer_s + rScanTime_s;
    IF rPT101_DiscrepancyTimer_s >= 1.50 THEN
        bPT101_Failed := TRUE;
    END_IF;
ELSE
    rPT101_DiscrepancyTimer_s := MAX(0.0, rPT101_DiscrepancyTimer_s - (rScanTime_s * 2.0));
    IF bReset THEN
        bPT101_Failed := FALSE;
    END_IF;
END_IF;

(* Transmitter PT102 Discrepancy & Health Verification *)
IF (rDev_12_bar > 0.35) AND (rDev_23_bar > 0.35) THEN
    rPT102_DiscrepancyTimer_s := rPT102_DiscrepancyTimer_s + rScanTime_s;
    IF rPT102_DiscrepancyTimer_s >= 1.50 THEN
        bPT102_Failed := TRUE;
    END_IF;
ELSE
    rPT102_DiscrepancyTimer_s := MAX(0.0, rPT102_DiscrepancyTimer_s - (rScanTime_s * 2.0));
    IF bReset THEN
        bPT102_Failed := FALSE;
    END_IF;
END_IF;

(* Transmitter PT103 Discrepancy & Health Verification *)
IF (rDev_23_bar > 0.35) AND (rDev_31_bar > 0.35) THEN
    rPT103_DiscrepancyTimer_s := rPT103_DiscrepancyTimer_s + rScanTime_s;
    IF rPT103_DiscrepancyTimer_s >= 1.50 THEN
        bPT103_Failed := TRUE;
    END_IF;
ELSE
    rPT103_DiscrepancyTimer_s := MAX(0.0, rPT103_DiscrepancyTimer_s - (rScanTime_s * 2.0));
    IF bReset THEN
        bPT103_Failed := FALSE;
    END_IF;
END_IF;

(* Compute Active Healthy Sensor Count in Crown Cluster *)
nHealthySensorCount := 3;
IF bPT101_Failed THEN nHealthySensorCount := nHealthySensorCount - 1; END_IF;
IF bPT102_Failed THEN nHealthySensorCount := nHealthySensorCount - 1; END_IF;
IF bPT103_Failed THEN nHealthySensorCount := nHealthySensorCount - 1; END_IF;

(* Multi-Tier Voting & Degradation Matrix Execution *)
IF nHealthySensorCount = 3 THEN
    (* 2oo3 MEDIAN SELECTION: Sorts 3 healthy signals and extracts middle value *)
    IF ((rPT101_Filtered_bar >= rPT102_Filtered_bar) AND (rPT101_Filtered_bar <= rPT103_Filtered_bar)) OR
       ((rPT101_Filtered_bar <= rPT102_Filtered_bar) AND (rPT101_Filtered_bar >= rPT103_Filtered_bar)) THEN
        rCrownPressure_RawVoted_bar := rPT101_Filtered_bar;
    ELSIF ((rPT102_Filtered_bar >= rPT101_Filtered_bar) AND (rPT102_Filtered_bar <= rPT103_Filtered_bar)) OR
          ((rPT102_Filtered_bar <= rPT101_Filtered_bar) AND (rPT102_Filtered_bar >= rPT103_Filtered_bar)) THEN
        rCrownPressure_RawVoted_bar := rPT102_Filtered_bar;
    ELSE
        rCrownPressure_RawVoted_bar := rPT103_Filtered_bar;
    END_IF;
    bDegradedSensorMode := FALSE;

ELSIF nHealthySensorCount = 2 THEN
    (* 1oo2 AVERAGE VOTING: Averages the remaining two operational transducers *)
    IF NOT bPT101_Failed AND NOT bPT102_Failed THEN
        rCrownPressure_RawVoted_bar := (rPT101_Filtered_bar + rPT102_Filtered_bar) * 0.50;
    ELSIF NOT bPT102_Failed AND NOT bPT103_Failed THEN
        rCrownPressure_RawVoted_bar := (rPT102_Filtered_bar + rPT103_Filtered_bar) * 0.50;
    ELSE
        rCrownPressure_RawVoted_bar := (rPT101_Filtered_bar + rPT103_Filtered_bar) * 0.50;
    END_IF;
    bDegradedSensorMode := TRUE;

ELSIF nHealthySensorCount = 1 THEN
    (* 1oo1 SINGLE-CHANNEL DEGRADED SURVIVAL: Uses the sole surviving healthy transmitter *)
    IF NOT bPT101_Failed THEN
        rCrownPressure_RawVoted_bar := rPT101_Filtered_bar;
    ELSIF NOT bPT102_Failed THEN
        rCrownPressure_RawVoted_bar := rPT102_Filtered_bar;
    ELSE
        rCrownPressure_RawVoted_bar := rPT103_Filtered_bar;
    END_IF;
    bDegradedSensorMode := TRUE;

ELSE
    (* FAILOVER FALLBACK: All 3 crown sensors failed. Synthesize crown pressure from springline wall sensors *)
    (* Hydrostatic correction: P_crown = P_springline_mean - (gamma_slurry * h), where h = D_tbm / 4 = 3.80 m *)
    rTempSum := (rBulkheadPressure_Spring_L_bar + rBulkheadPressure_Spring_R_bar) * 0.50;
    rCrownPressure_RawVoted_bar := MAX(0.50, rTempSum - ((rSoilSpecificWeight_kN_m3 * 3.80) / 100.0));
    bDegradedSensorMode := TRUE;
END_IF;

(* Slew-Rate Limiting on Voted Output to prevent step disturbances during bumpless sensor degradation *)
rTempDiff := rCrownPressure_RawVoted_bar - rCrownPressure_PrevVoted_bar;
IF rTempDiff > (0.25 * rScanTime_s) THEN
    rBulkheadCrownPressure_Voted_bar := rCrownPressure_PrevVoted_bar + (0.25 * rScanTime_s);
ELSIF rTempDiff < (-0.25 * rScanTime_s) THEN
    rBulkheadCrownPressure_Voted_bar := rCrownPressure_PrevVoted_bar - (0.25 * rScanTime_s);
ELSE
    rBulkheadCrownPressure_Voted_bar := rCrownPressure_RawVoted_bar;
END_IF;
rCrownPressure_PrevVoted_bar := rBulkheadCrownPressure_Voted_bar;

(* Area-Weighted Multi-Point Bulkhead Mean Pressure & Vertical Hydrostatic Gradient *)
(* Weighting factors: Crown (25%), Springline Left (25%), Springline Right (25%), Invert (25%) *)
rBulkheadMeanPressure_bar := (rBulkheadCrownPressure_Voted_bar * 0.250) +
                             (rBulkheadPressure_Spring_L_bar * 0.250) +
                             (rBulkheadPressure_Spring_R_bar * 0.250) +
                             (rBulkheadPressure_Invert_bar * 0.250);

(* Measured vertical pressure gradient across bulkhead diameter (15.2 m) [bar/m] *)
rBulkheadPressureGradient_bar_m := (rBulkheadPressure_Invert_bar - rBulkheadCrownPressure_Voted_bar) / 15.20;

(* Pressure stabilization check: True if crown pressure is tightly locked within +/- 0.15 bar of target *)
bChamberPressureStabilized := (ABS(rBulkheadCrownPressure_Voted_bar - rTargetChamberPressure_bar) <= 0.15);

(*
 ====================================================================================================
  PHASE 2: DISCRETE STATE-SPACE PREDICTION & OBSERVER ESTIMATION
 ====================================================================================================
  State observer combines physical plant feedback vector y[k] with internal state-space model:
    e_obs[k] = y_meas[k] - C * x_hat[k|k-1]
    x_hat[k] = x_hat[k|k-1] + L_obs * e_obs[k]
    x_pred[k+1] = A * x_hat[k] + B * u[k]
*)

(* Extract physical output measurement vector y[k] *)
vecY_meas[1] := rBulkheadCrownPressure_Voted_bar;
vecY_meas[2] := rCutterheadTotalTorque_kNm;
vecY_meas[3] := LIMIT(0.0, (rScrewConveyorTorque_kNm / 400.0) * (rScrewConveyorSpeedActual_RPM / 15.0), 1.0);
vecY_meas[4] := rAdvanceRateActual_mm_min;

(* Compute Observer Innovation Error: e_obs = y_meas - C * x_hat *)
FOR kState := 1 TO 4 DO
    rTempSum := 0.0;
    FOR jHoriz := 1 TO 4 DO
        rTempSum := rTempSum + (matC[kState, jHoriz] * vecX_hat[jHoriz]);
    END_FOR;
    vecY_err[kState] := vecY_meas[kState] - rTempSum;
END_FOR;

(* Correct State Estimate with Luenberger Gain: x_hat = x_hat + L_obs * e_obs *)
FOR kState := 1 TO 4 DO
    rTempSum := 0.0;
    FOR jHoriz := 1 TO 4 DO
        rTempSum := rTempSum + (matL_Obs[kState, jHoriz] * vecY_err[jHoriz]);
    END_FOR;
    vecX_hat[kState] := vecX_hat[kState] + rTempSum;
END_FOR;

(* Bound physical states to prevent numerical drift *)
vecX_hat[1] := LIMIT(0.0, vecX_hat[1], 10.0);       (* Pressure [bar] *)
vecX_hat[2] := LIMIT(0.0, vecX_hat[2], 55000.0);    (* Torque [kNm] *)
vecX_hat[3] := LIMIT(0.0, vecX_hat[3], 1.0);        (* Fill Ratio [-] *)
vecX_hat[4] := LIMIT(0.0, vecX_hat[4], 75.0);       (* Advance Rate [mm/min] *)

(* Assemble Active Control Input Vector u[k] *)
vecU_cmd[1] := rScrewConveyorSpeedCmd_RPM;
vecU_cmd[2] := rThrustPressureSetpoint_bar;
vecU_cmd[3] := rFoamAirValveCmd_pct;

(* Propagate Dynamic State Prediction: x_pred[k+1] = A * x_hat[k] + B * u[k] *)
FOR kState := 1 TO 4 DO
    rTempSum := 0.0;
    FOR jHoriz := 1 TO 4 DO
        rTempSum := rTempSum + (matA[kState, jHoriz] * vecX_hat[jHoriz]);
    END_FOR;
    FOR mInput := 1 TO 3 DO
        rTempSum := rTempSum + (matB[kState, mInput] * vecU_cmd[mInput]);
    END_FOR;
    vecX_pred[kState] := rTempSum;
END_FOR;

(*
 ====================================================================================================
  PHASE 3: RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) OPTIMIZATION
 ====================================================================================================
  Minimizes multi-objective quadratic performance index J over prediction horizon Np = 5:
    J = SUM_i (x_i - x_ref)^T * Q * (x_i - x_ref) + SUM_j (du_j)^T * R * (du_j) + (x_Np - x_ref)^T * P * (x_Np - x_ref)
  Uses projected gradient descent to calculate optimal slew-limited actuation increments:
    du1* = dScrew_RPM, du2* = dThrust_Pressure, du3* = dFoam_Valve.
*)

(* Establish Reference Trajectory Vector *)
vecX_ref[1] := rTargetChamberPressure_bar;
vecX_ref[2] := 26000.0;                                     (* Target Cutterhead Baseline Torque [kNm] *)
vecX_ref[3] := 0.72;                                        (* Target Screw Conveyor Volumetric Fill Fraction *)
vecX_ref[4] := rTargetAdvanceRate_mm_min;                   (* Target Penetration Advance Speed [mm/min] *)

(* Predict State Trajectory across Horizon Np = 5 steps *)
FOR kState := 1 TO 4 DO
    matHorizStates[1, kState] := vecX_pred[kState];
END_FOR;

FOR iHoriz := 2 TO 5 DO
    FOR kState := 1 TO 4 DO
        rTempSum := 0.0;
        FOR jHoriz := 1 TO 4 DO
            rTempSum := rTempSum + (matA[kState, jHoriz] * matHorizStates[iHoriz - 1, jHoriz]);
        END_FOR;
        FOR mInput := 1 TO 3 DO
            rTempSum := rTempSum + (matB[kState, mInput] * vecU_cmd[mInput]);
        END_FOR;
        matHorizStates[iHoriz, kState] := rTempSum;
    END_FOR;
END_FOR;

(* Compute Instantaneous Quadratic Performance Cost J *)
rCostJ := 0.0;
FOR iHoriz := 1 TO 4 DO
    FOR kState := 1 TO 4 DO
        rTempDiff := matHorizStates[iHoriz, kState] - vecX_ref[kState];
        rCostJ := rCostJ + (rTempDiff * rTempDiff * diagQ[kState]);
    END_FOR;
END_FOR;

(* Terminal Horizon Penalty P *)
FOR kState := 1 TO 4 DO
    rTempDiff := matHorizStates[5, kState] - vecX_ref[kState];
    rCostJ := rCostJ + (rTempDiff * rTempDiff * diagP[kState]);
END_FOR;

(* Add Control Slew Effort Penalty R *)
FOR mInput := 1 TO 3 DO
    rTempDiff := vecU_cmd[mInput] - vecU_prev[mInput];
    rCostJ := rCostJ + (rTempDiff * rTempDiff * diagR[mInput]);
END_FOR;

(*
  Analytical Gradient Approximation of Cost Functional with respect to Input Moves:
  dJ/du_m ~= SUM_k [ 2 * Q_k * (x_k - x_ref_k) * B_k,m ] + 2 * R_m * (u_m - u_prev_m)
*)
FOR mInput := 1 TO 3 DO
    rTempSum := 0.0;
    FOR kState := 1 TO 4 DO
        rTempDiff := matHorizStates[1, kState] - vecX_ref[kState];
        rTempSum := rTempSum + (2.0 * diagQ[kState] * rTempDiff * matB[kState, mInput]);
    END_FOR;
    (* Terminal Step Gradient Influence *)
    FOR kState := 1 TO 4 DO
        rTempDiff := matHorizStates[5, kState] - vecX_ref[kState];
        rTempSum := rTempSum + (1.5 * diagP[kState] * rTempDiff * matB[kState, mInput]);
    END_FOR;
    (* Slew Penalty Gradient Component *)
    rTempSum := rTempSum + (2.0 * diagR[mInput] * (vecU_cmd[mInput] - vecU_prev[mInput]));
    vecGradJ[mInput] := rTempSum;
END_FOR;

(* Projected Gradient Descent Adjustment: du* = -gamma * grad(J) *)
FOR mInput := 1 TO 3 DO
    vecDeltaU_opt[mInput] := -rMPC_StepSize * vecGradJ[mInput];
END_FOR;

(*
 ====================================================================================================
  PHASE 4: MULTI-STAGE FINITE STATE MACHINE (FSM) CONTROL ENGINE
 ====================================================================================================
  States:
    0  : TBM_PARKED_IDLE
    10 : CHAMBER_PRESSURE_PRECHARGE
    20 : CUTTERHEAD_ROTATION_START
    30 : THRUST_CYLINDER_STROKE_EXTEND
    40 : STEADY_STATE_EPB_EXCAVATION
    50 : RING_ADVANCE_STROKE_END
    60 : SEGMENT_RING_ERECT_INTERLOCK
    70 : BENTONITE_FOAM_CONDITIONING_TRIM
    80 : GEOLOGY_OBSTACLE_TORQUE_DECEL
    90 : PLANNED_CUTTER_TOOL_INSPECT
    99 : FACE_COLLAPSE_EMERGENCY_SHUTDOWN
*)

(* Global Emergency Stop Check *)
IF NOT bEStopActivated OR (nAlmState_CrownLL = 1) OR (nAlmState_CrownHH = 1) OR (nAlmState_TorqueHH = 1) THEN
    nState := 99; (* Instantaneous Abort to Safety State *)
END_IF;

CASE nState OF
    0: (* ------------------------------------------------------------------------------------------ *)
       (* STATE 0: TBM_PARKED_IDLE                                                                  *)
       (* Machine completely secured, zero cutterhead rotation, thrust pumps unloading to tank.      *)
       (* Permissive check: Lubrication verified, Erector interlock clear, E-Stop clear.             *)
       (* ------------------------------------------------------------------------------------------ *)
        rCutterheadSpeedTarget_RPM      := 0.0;
        rThrustAdvanceRateCmd_mm_min    := 0.0;
        rThrustPressureSetpoint_bar     := 25.0; (* Standby hydraulic circulation pressure *)
        rScrewConveyorSpeedCmd_RPM      := 0.0;
        rScrewMuckGatePositionCmd_pct   := 0.0;
        rBentonitePumpCmd_pct           := 0.0;
        rFoamAirValveCmd_pct            := 0.0;
        rPolymerPumpCmd_pct             := 0.0;
        bRingAdvanceComplete            := FALSE;
        bObstacleDetected               := FALSE;
        bEmergencyStopTriggered         := FALSE;

        FOR iMotor := 1 TO 16 DO
            aMotorTorqueLimits_kNm[iMotor] := 0.0;
        END_FOR;
        FOR iQuad := 1 TO 4 DO
            aQuadrantThrustBias_pct[iQuad] := 0.0;
        END_FOR;

        (* Transition: Operator start command AND lubrication temperature acceptable *)
        IF bEnable AND bStartExcavationCmd AND (rMainBearingOilTemp_C < 65.0) AND bRingErectInterlockClear THEN
            nState := 10; (* Advance to Chamber Pressure Precharge *)
        END_IF;

    10: (* ----------------------------------------------------------------------------------------- *)
        (* STATE 10: CHAMBER_PRESSURE_PRECHARGE                                                     *)
        (* Inject bentonite slurry and foam air cushion to pressurize excavation chamber up to      *)
        (* hydrostatic groundwater head prior to initiating cutterhead rotation.                     *)
        (* Prevents immediate settlement trough when machine seals are opened.                      *)
        (* ----------------------------------------------------------------------------------------- *)
        rCutterheadSpeedTarget_RPM      := 0.0;
        rThrustAdvanceRateCmd_mm_min    := 0.0;
        rThrustPressureSetpoint_bar     := 35.0;
        rScrewConveyorSpeedCmd_RPM      := 0.0;
        rScrewMuckGatePositionCmd_pct   := 0.0; (* Keep muck gate tightly sealed *)

        (* Ramp conditioning delivery to charge chamber cushion *)
        rBentonitePumpCmd_pct           := 65.0;
        rFoamAirValveCmd_pct            := 55.0;
        rPolymerPumpCmd_pct             := 20.0;

        FOR iMotor := 1 TO 16 DO
            aMotorTorqueLimits_kNm[iMotor] := 500.0; (* Minimum holding pre-torque *)
        END_FOR;

        (* Transition: Crown pressure reaches target minus 0.20 bar within timeout OR operator abort *)
        IF (rBulkheadCrownPressure_Voted_bar >= (rTargetChamberPressure_bar - 0.20)) AND (rStateTimer_s >= 5.0) THEN
            nState := 20; (* Proceed to Cutterhead Soft Rotation Start *)
        ELSIF rStateTimer_s > 180.0 THEN
            (* Precharge timeout: slurry loss into permeable fissure or leakage detected *)
            nState := 99;
        END_IF;

    20: (* ----------------------------------------------------------------------------------------- *)
        (* STATE 20: CUTTERHEAD_ROTATION_START                                                      *)
        (* Controlled S-curve ramp-up of 16 electric VFD drives up to nominal rotation (1.50 RPM).  *)
        (* Anti-backlash pre-torquing engages gear mesh smoothly, eliminating shock loads.          *)
        (* ----------------------------------------------------------------------------------------- *)
        IF bStateFirstScan THEN
            rCutterheadSpeedRamp_RPM := 0.20;
        END_IF;

        (* Smooth acceleration ramp: 0.15 RPM / sec *)
        rCutterheadSpeedRamp_RPM := MIN(rTargetCutterheadSpeed_RPM, rCutterheadSpeedRamp_RPM + (0.15 * rScanTime_s));
        rCutterheadSpeedTarget_RPM := rCutterheadSpeedRamp_RPM;

        rThrustAdvanceRateCmd_mm_min    := 0.0;
        rThrustPressureSetpoint_bar     := 45.0;
        rScrewConveyorSpeedCmd_RPM      := 1.5;  (* Slow idle rotation to lubricate flight ribbons *)
        rScrewMuckGatePositionCmd_pct   := 5.0;
        rBentonitePumpCmd_pct           := 45.0;
        rFoamAirValveCmd_pct            := 40.0;
        rPolymerPumpCmd_pct             := 15.0;

        (* Transition: Speed target achieved and torque variance across 16 pinions balanced *)
        IF (rCutterheadSpeedRamp_RPM >= (rTargetCutterheadSpeed_RPM - 0.05)) AND (rCutterheadTorqueImbalance_pct < 18.0) AND (rStateTimer_s >= 8.0) THEN
            nState := 30; (* Advance to Thrust Propulsion Stroke Extension *)
        ELSIF rCutterheadTotalTorque_kNm > rSp_TorqueH_kNm THEN
            nState := 80; (* Cutterhead jammed by boulder or collapsed face *)
        END_IF;

    30: (* ----------------------------------------------------------------------------------------- *)
        (* STATE 30: THRUST_CYLINDER_STROKE_EXTEND                                                  *)
        (* Proportional thrust valves extend 40 cylinders to engage segment ring thrust shoes.      *)
        (* Pressure ramps smoothly up to advance penetration contact (0 to 180 bar).                 *)
        (* ----------------------------------------------------------------------------------------- *)
        rCutterheadSpeedTarget_RPM      := rTargetCutterheadSpeed_RPM;
        rThrustAdvanceRateCmd_mm_min    := MIN(15.0, rTargetAdvanceRate_mm_min * 0.35);
        rThrustPressureSetpoint_bar     := MIN(185.0, 45.0 + (rStateTimer_s * 25.0));
        rScrewConveyorSpeedCmd_RPM      := 3.5;
        rScrewMuckGatePositionCmd_pct   := 15.0;
        rBentonitePumpCmd_pct           := 50.0;
        rFoamAirValveCmd_pct            := 45.0;
        rPolymerPumpCmd_pct             := 20.0;

        (* Transition: Disc cutters make rock contact, thrust force exceeds 40,000 kN, advance > 8 mm/min *)
        IF (rTotalThrustForce_kN >= 40000.0) AND (rAdvanceRateActual_mm_min >= 8.0) AND (rStateTimer_s >= 6.0) THEN
            nState := 40; (* Advance to Steady-State Closed-Loop EPB Excavation *)
        ELSIF bHoldAdvanceCmd THEN
            nState := 0;
        END_IF;

    40: (* ----------------------------------------------------------------------------------------- *)
        (* STATE 40: STEADY_STATE_EPB_EXCAVATION                                                    *)
        (* Primary high-performance closed-loop tunneling advance.                                   *)
        (* MPC coordinates Screw Conveyor RPM, Thrust Pressure, and Foam Injection to hold face     *)
        (* pressure within target +/- 0.15 bar while laser guidance trims quadrant steering biases.  *)
        (* ----------------------------------------------------------------------------------------- *)
        rCutterheadSpeedTarget_RPM := rTargetCutterheadSpeed_RPM;

        (* Apply MPC Optimal Actuator Corrections with Slew-Rate Limiting *)
        (* 1. Screw Conveyor Velocity Control: limits rate to +/- 0.075 RPM per 50ms scan (1.5 RPM/s) *)
        rGradStep := LIMIT(-0.075, vecDeltaU_opt[1], 0.075);
        rScrewConveyorSpeedCmd_RPM := LIMIT(0.0, rScrewConveyorSpeedCmd_RPM + rGradStep, 22.0);

        (* 2. Main Thrust Pressure Slew: limits rate to +/- 0.50 bar per 50ms scan (10.0 bar/s) *)
        rGradStep := LIMIT(-0.50, vecDeltaU_opt[2], 0.50);
        rThrustPressureSetpoint_bar := LIMIT(80.0, rThrustPressureSetpoint_bar + rGradStep, 340.0);

        (* 3. Foam Injection Air Valve: limits rate to +/- 1.0% per 50ms scan (20.0 %/s) *)
        rGradStep := LIMIT(-1.0, vecDeltaU_opt[3], 1.0);
        rFoamAirValveCmd_pct := LIMIT(10.0, rFoamAirValveCmd_pct + rGradStep, 100.0);

        (* Coordinate Advance Rate Target to match hydraulic pressure capacity *)
        rThrustAdvanceRateCmd_mm_min := LIMIT(5.0, (rThrustPressureSetpoint_bar / 300.0) * rTargetAdvanceRate_mm_min, 60.0);

        (* Discharge Gate Modulation: adjusts choke based on screw torque and chamber pressure *)
        IF rBulkheadCrownPressure_Voted_bar > (rTargetChamberPressure_bar + 0.10) THEN
            rScrewMuckGatePositionCmd_pct := MIN(100.0, rScrewMuckGatePositionCmd_pct + (0.50 * rScanTime_s));
        ELSIF rBulkheadCrownPressure_Voted_bar < (rTargetChamberPressure_bar - 0.10) THEN
            rScrewMuckGatePositionCmd_pct := MAX(10.0, rScrewMuckGatePositionCmd_pct - (0.80 * rScanTime_s));
        END_IF;

        (* Bentonite Slurry and Polymer Proportional Follower *)
        rBentonitePumpCmd_pct := LIMIT(20.0, (rAdvanceRateActual_mm_min / 50.0) * 80.0, 100.0);
        rPolymerPumpCmd_pct   := LIMIT(10.0, (rAdvanceRateActual_mm_min / 50.0) * 45.0, 90.0);

        (* Transition: Full segment stroke (e.g. 2,000 mm for 1.8m universal ring) reached *)
        IF rCylinderStroke_Avg_mm >= 2000.0 THEN
            bRingAdvanceComplete := TRUE;
            nState := 50; (* Advance to Ring Stroke End Deceleration *)
        ELSIF bHoldAdvanceCmd THEN
            nState := 50; (* Operator requested advance pause *)
        ELSIF (rCutterheadTotalTorque_kNm >= rSp_TorqueH_kNm) OR (rScrewConveyorTorque_kNm > 390.0) THEN
            nState := 80; (* Encountered high cutting resistance or boulder *)
        ELSIF (ABS(rMuckDischargeRatio - 1.0) > 0.25) AND (rStateTimer_s > 30.0) THEN
            nState := 70; (* Muck conditioning rheology drift detected *)
        END_IF;

    50: (* ----------------------------------------------------------------------------------------- *)
        (* STATE 50: RING_ADVANCE_STROKE_END                                                        *)
        (* Coordinated smooth deceleration of thrust advance and cutterhead drive at stroke limit.   *)
        (* Bulkhead pressure locked and maintained by compressed air cushion while screw stops.      *)
        (* ----------------------------------------------------------------------------------------- *)
        (* Decelerate advance penetration to 0 mm/min *)
        rThrustAdvanceRateCmd_mm_min    := MAX(0.0, rThrustAdvanceRateCmd_mm_min - (8.0 * rScanTime_s));
        rThrustPressureSetpoint_bar     := MAX(40.0, rThrustPressureSetpoint_bar - (20.0 * rScanTime_s));

        (* Decelerate cutterhead rotation *)
        rCutterheadSpeedTarget_RPM      := MAX(0.0, rCutterheadSpeedTarget_RPM - (0.45 * rScanTime_s));

        (* Ramp down screw conveyor and close guillotine muck gate to seal chamber *)
        rScrewConveyorSpeedCmd_RPM      := MAX(0.0, rScrewConveyorSpeedCmd_RPM - (2.5 * rScanTime_s));
        rScrewMuckGatePositionCmd_pct   := MAX(0.0, rScrewMuckGatePositionCmd_pct - (15.0 * rScanTime_s));

        (* Maintain air cushion to prevent settlement during standstill *)
        rBentonitePumpCmd_pct           := 15.0;
        rFoamAirValveCmd_pct            := 40.0;
        rPolymerPumpCmd_pct             := 0.0;

        (* Transition: Machine fully arrested and gate sealed *)
        IF (rCutterheadSpeedTarget_RPM <= 0.05) AND (rThrustAdvanceRateCmd_mm_min <= 0.5) AND (rScrewMuckGatePositionCmd_pct <= 1.0) THEN
            IF bRingAdvanceComplete THEN
                nState := 60; (* Proceed to Segment Ring Erection Interlock *)
            ELSE
                nState := 0;  (* Return to Parked Idle *)
            END_IF;
        END_IF;

    60: (* ----------------------------------------------------------------------------------------- *)
        (* STATE 60: SEGMENT_RING_ERECT_INTERLOCK                                                   *)
        (* Tunnel advance held. Mechanical cutterhead brake applied. Hydraulic thrust cylinders     *)
        (* retracted in sequential pairs/quadrants to allow erector crane to place precast segments. *)
        (* Safety interlock ensures thrust cannot advance while erector arm is in ring plane.        *)
        (* ----------------------------------------------------------------------------------------- *)
        rCutterheadSpeedTarget_RPM      := 0.0;
        rThrustAdvanceRateCmd_mm_min    := 0.0;
        rThrustPressureSetpoint_bar     := 30.0;
        rScrewConveyorSpeedCmd_RPM      := 0.0;
        rScrewMuckGatePositionCmd_pct   := 0.0;
        rBentonitePumpCmd_pct           := 0.0;
        rFoamAirValveCmd_pct            := 25.0; (* Low purge air to prevent nozzle back-silting *)
        rPolymerPumpCmd_pct             := 0.0;

        FOR iMotor := 1 TO 16 DO
            aMotorTorqueLimits_kNm[iMotor] := 0.0;
        END_FOR;

        (* Transition: Segment ring build completed, key segment inserted, erector parked and locked *)
        IF bRingErectInterlockClear AND (rCylinderStroke_Avg_mm <= 150.0) AND bReset THEN
            bRingAdvanceComplete := FALSE;
            nState := 0; (* Reset to Parked Idle, ready for next advance stroke *)
        ELSIF bToolInspectSelectCmd THEN
            nState := 90; (* Divert to Planned Cutter Tool Hyperbaric Inspection *)
        END_IF;

    70: (* ----------------------------------------------------------------------------------------- *)
        (* STATE 70: BENTONITE_FOAM_CONDITIONING_TRIM                                               *)
        (* Adaptive conditioning trim: Activated when muck discharge balance or torque suggests     *)
        (* chamber clogging, cake consolidation, or high friction in sticky clay / sand transitions. *)
        (* ----------------------------------------------------------------------------------------- *)
        rCutterheadSpeedTarget_RPM      := MIN(1.80, rTargetCutterheadSpeed_RPM * 0.70);
        rThrustAdvanceRateCmd_mm_min    := MIN(18.0, rTargetAdvanceRate_mm_min * 0.50);
        rThrustPressureSetpoint_bar     := 175.0;

        (* Boost polymer surfactant and foam injection ratios (+40%) *)
        rBentonitePumpCmd_pct           := 85.0;
        rFoamAirValveCmd_pct            := 75.0;
        rPolymerPumpCmd_pct             := 65.0;

        (* Trim screw conveyor to break chamber stagnation *)
        rScrewConveyorSpeedCmd_RPM      := 8.5;
        rScrewMuckGatePositionCmd_pct   := 35.0;

        (* Transition: Torque drops below warning and muck balance normalizes *)
        IF (rCutterheadTotalTorque_kNm < 30000.0) AND (ABS(rMuckDischargeRatio - 1.0) <= 0.12) AND (rStateTimer_s >= 20.0) THEN
            nState := 40; (* Return to Steady-State EPB Excavation *)
        ELSIF rStateTimer_s > 120.0 THEN
            (* Conditioning ineffective, transition to obstacle decel *)
            nState := 80;
        END_IF;

    80: (* ----------------------------------------------------------------------------------------- *)
        (* STATE 80: GEOLOGY_OBSTACLE_TORQUE_DECEL                                                  *)
        (* Encountered severe mixed face, erratic quartzite boulder, or timber/pile obstruction.    *)
        (* Throttles advance rate immediately, increases cutterhead torque breakout limit, reduces   *)
        (* cutterhead RPM to maximize penetration per revolution and crush rock without stalling.   *)
        (* ----------------------------------------------------------------------------------------- *)
        bObstacleDetected := TRUE;

        (* Drop cutterhead rotational speed to 0.75 RPM to increase torque per tool *)
        rCutterheadSpeedTarget_RPM      := 0.75;
        rThrustAdvanceRateCmd_mm_min    := 4.5;   (* Creep advance velocity *)
        rThrustPressureSetpoint_bar     := 285.0; (* Maintain high hydraulic thrust for tool penetration *)
        rScrewConveyorSpeedCmd_RPM      := 4.0;
        rScrewMuckGatePositionCmd_pct   := 25.0;
        rBentonitePumpCmd_pct           := 70.0;
        rFoamAirValveCmd_pct            := 60.0;
        rPolymerPumpCmd_pct             := 40.0;

        (* Transition: Obstacle crushed or cut through, torque falls back below warning threshold *)
        IF (rCutterheadTotalTorque_kNm < 32000.0) AND (rStateTimer_s >= 30.0) THEN
            bObstacleDetected := FALSE;
            nState := 40; (* Resume normal excavation *)
        ELSIF rCutterheadTotalTorque_kNm >= rSp_TorqueHH_kNm THEN
            (* Insoluble obstruction: trip to abort *)
            nState := 99;
        END_IF;

    90: (* ----------------------------------------------------------------------------------------- *)
        (* STATE 90: PLANNED_CUTTER_TOOL_INSPECT                                                    *)
        (* Preparation for compressed air intervention: Chamber muck evacuated, bentonite filter    *)
        (* cake built against face, hyperbaric air pressure equalized to groundwater head.          *)
        (* Strict safety lockouts prevent any drive or thrust actuation.                            *)
        (* ----------------------------------------------------------------------------------------- *)
        rCutterheadSpeedTarget_RPM      := 0.0;
        rThrustAdvanceRateCmd_mm_min    := 0.0;
        rThrustPressureSetpoint_bar     := 0.0;
        rScrewConveyorSpeedCmd_RPM      := 0.0;
        rScrewMuckGatePositionCmd_pct   := 0.0;
        rBentonitePumpCmd_pct           := 0.0;
        rPolymerPumpCmd_pct             := 0.0;

        (* Precise hyperbaric compressed air regulation equal to groundwater head *)
        rFoamAirValveCmd_pct            := LIMIT(10.0, (rGroundwaterHead_mWC / 10.0) * 22.0, 85.0);

        FOR iMotor := 1 TO 16 DO
            aMotorTorqueLimits_kNm[iMotor] := 0.0;
        END_FOR;

        (* Transition: Operator cancels inspection and clears interlocks *)
        IF NOT bToolInspectSelectCmd AND bReset THEN
            nState := 0;
        END_IF;

    99: (* ----------------------------------------------------------------------------------------- *)
        (* STATE 99: FACE_COLLAPSE_EMERGENCY_SHUTDOWN                                               *)
        (* Catastrophic safety shutdown: Emergency stop pressed, face blowout (HH), collapse (LL),  *)
        (* drive overload, or seal breach. Guillotine gate slammed shut in < 1.2s to prevent blowout. *)
        (* ----------------------------------------------------------------------------------------- *)
        bEmergencyStopTriggered         := TRUE;
        rCutterheadSpeedTarget_RPM      := 0.0;
        rThrustAdvanceRateCmd_mm_min    := 0.0;
        rThrustPressureSetpoint_bar     := 0.0;   (* Dump propulsion pressure to tank *)
        rScrewConveyorSpeedCmd_RPM      := 0.0;
        rScrewMuckGatePositionCmd_pct   := 0.0;   (* EMERGENCY CHOKE SHUT *)
        rBentonitePumpCmd_pct           := 0.0;
        rFoamAirValveCmd_pct            := 0.0;
        rPolymerPumpCmd_pct             := 0.0;

        FOR iMotor := 1 TO 16 DO
            aMotorTorqueLimits_kNm[iMotor] := 0.0;
        END_FOR;
        FOR iQuad := 1 TO 4 DO
            aQuadrantThrustBias_pct[iQuad] := 0.0;
        END_FOR;

        (* Latch emergency state until hardware reset and explicit clearance *)
        IF bReset AND bEStopActivated AND (nAlmState_CrownHH = 0) AND (nAlmState_CrownLL = 0) AND (nAlmState_TorqueHH = 0) THEN
            bEmergencyStopTriggered := FALSE;
            nState := 0; (* Reset to Parked Idle *)
        END_IF;

ELSE
    nState := 99; (* Invalid State Trap -> Abort *)
END_CASE;

(* Update Previous Control Vector Memory for MPC Slew Penalty *)
vecU_prev[1] := rScrewConveyorSpeedCmd_RPM;
vecU_prev[2] := rThrustPressureSetpoint_bar;
vecU_prev[3] := rFoamAirValveCmd_pct;

(*
 ====================================================================================================
  16-MOTOR CUTTERHEAD DRIVE COORDINATION, DROOP LOAD-SHARING & THERMAL DERATING
 ====================================================================================================
  Executes real-time multi-motor torque summation, mean calculation, droop load sharing, and thermal
  derating for the 16 x 350 kW pinion drive motors.
*)
rMotorTorqueSum_kNm := 0.0;
rMotorTorqueMaxDev_kNm := 0.0;

(* Calculate aggregate torque across all 16 pinion drives *)
FOR iMotor := 1 TO 16 DO
    rMotorTorqueSum_kNm := rMotorTorqueSum_kNm + aMotorTorques_kNm[iMotor];
END_FOR;
rCutterheadTotalTorque_kNm := rMotorTorqueSum_kNm;
rMotorTorqueMean_kNm := rMotorTorqueSum_kNm / 16.0;

(* Evaluate Pinion Torque Variance & Maximum Imbalance *)
FOR iMotor := 1 TO 16 DO
    rTempDiff := ABS(aMotorTorques_kNm[iMotor] - rMotorTorqueMean_kNm);
    IF rTempDiff > rMotorTorqueMaxDev_kNm THEN
        rMotorTorqueMaxDev_kNm := rTempDiff;
    END_IF;
END_FOR;

IF rMotorTorqueMean_kNm > 500.0 THEN
    rCutterheadTorqueImbalance_pct := (rMotorTorqueMaxDev_kNm / rMotorTorqueMean_kNm) * 100.0;
ELSE
    rCutterheadTorqueImbalance_pct := 0.0;
END_IF;

(* Individual Motor Stator Winding Thermal Derating (PT100 RTD curves) *)
(* Class H insulation: 130 deg C threshold begins linear derating down to 20% torque at 155 deg C *)
FOR iMotor := 1 TO 16 DO
    IF aMotorTemperatures_C[iMotor] > 130.0 THEN
        aMotorThermalDerateFactor[iMotor] := MAX(0.20, 1.0 - ((aMotorTemperatures_C[iMotor] - 130.0) / 25.0));
    ELSE
        aMotorThermalDerateFactor[iMotor] := 1.0;
    END_IF;

    (* Speed droop trim calculation to shed torque on overloaded pinions *)
    aMotorDroopTrim_RPM[iMotor] := -rTorqueDroopGain * (aMotorTorques_kNm[iMotor] - rMotorTorqueMean_kNm);

    (* Command Individual VFD Torque Limits during Active Excavation States *)
    IF (nState >= 20) AND (nState <= 80) THEN
        IF NOT aMotorVFD_Fault[iMotor] THEN
            (* Base share + droop compensation * thermal derating *)
            rTempSum := (3000.0 * aMotorThermalDerateFactor[iMotor]) + (aMotorDroopTrim_RPM[iMotor] * 250.0);
            aMotorTorqueLimits_kNm[iMotor] := LIMIT(200.0, rTempSum, 3750.0);
        ELSE
            aMotorTorqueLimits_kNm[iMotor] := 0.0; (* Tripped VFD isolated *)
        END_IF;
    ELSIF nState = 10 THEN
        aMotorTorqueLimits_kNm[iMotor] := 500.0;
    ELSE
        aMotorTorqueLimits_kNm[iMotor] := 0.0;
    END_IF;
END_FOR;

(*
 ====================================================================================================
  HYDRAULIC PROPULSION QUADRANT STEERING & LASER GUIDANCE COORDINATION
 ====================================================================================================
  Calculates differential steering pressure biases for the 4 quadrants based on laser target offsets:
    - Horizontal deviation (dx) induces Yaw differential pressure (Q1+Q2 vs Q3+Q4).
    - Vertical deviation (dy) induces Pitch differential pressure (Q1+Q4 vs Q2+Q3).
    - Shield roll angle introduces counter-torsional pressure trim.
*)
IF (nState = 40) OR (nState = 70) OR (nState = 80) THEN
    (* Guidance Steering Moments *)
    rSteeringDeltaP_Yaw_bar   := LIMIT(-35.0, rLaserDeviationHoriz_mm * rGuidanceGainYaw, 35.0);
    rSteeringDeltaP_Pitch_bar := LIMIT(-35.0, rLaserDeviationVert_mm * rGuidanceGainPitch, 35.0);
    rSteeringDeltaP_Roll_bar  := LIMIT(-15.0, -rTBM_Roll_deg * rGuidanceGainRoll, 15.0);

    rThrustPressureBase_bar := rThrustPressureSetpoint_bar;

    (* Synthesize Quadrant Target Pressures *)
    (* Quadrant 1: Top-Right    (+Yaw, +Pitch) *)
    aQuadrantPressure_bar[1] := rThrustPressureBase_bar + rSteeringDeltaP_Yaw_bar + rSteeringDeltaP_Pitch_bar + rSteeringDeltaP_Roll_bar;
    (* Quadrant 2: Bottom-Right (+Yaw, -Pitch) *)
    aQuadrantPressure_bar[2] := rThrustPressureBase_bar + rSteeringDeltaP_Yaw_bar - rSteeringDeltaP_Pitch_bar - rSteeringDeltaP_Roll_bar;
    (* Quadrant 3: Bottom-Left  (-Yaw, -Pitch) *)
    aQuadrantPressure_bar[3] := rThrustPressureBase_bar - rSteeringDeltaP_Yaw_bar - rSteeringDeltaP_Pitch_bar + rSteeringDeltaP_Roll_bar;
    (* Quadrant 4: Top-Left     (-Yaw, +Pitch) *)
    aQuadrantPressure_bar[4] := rThrustPressureBase_bar - rSteeringDeltaP_Yaw_bar + rSteeringDeltaP_Pitch_bar - rSteeringDeltaP_Roll_bar;

    FOR iQuad := 1 TO 4 DO
        aQuadrantPressure_bar[iQuad] := LIMIT(30.0, aQuadrantPressure_bar[iQuad], 345.0);
        (* Compute percentage bias relative to base setpoint *)
        aQuadrantThrustBias_pct[iQuad] := ((aQuadrantPressure_bar[iQuad] - rThrustPressureBase_bar) / rThrustPressureBase_bar) * 100.0;
    END_FOR;
ELSE
    FOR iQuad := 1 TO 4 DO
        aQuadrantPressure_bar[iQuad] := rThrustPressureSetpoint_bar;
        aQuadrantThrustBias_pct[iQuad] := 0.0;
    END_FOR;
END_IF;

(* Total Hydraulic Thrust Force: Sum of 4 Quadrants * Piston Area * 10,000 kN/MN *)
(* 10 cylinders per quadrant, effective piston area per quadrant = 0.3848 m2 *)
rTempSum := 0.0;
FOR iQuad := 1 TO 4 DO
    (* Force_kN = Pressure_bar * 100 [kN/m2] * Area_m2 *)
    rTempSum := rTempSum + (aQuadrantPressure_bar[iQuad] * 100.0 * rTotalPistonArea_Quadrant_m2);
END_FOR;
rTotalThrustForce_kN := rTempSum;

(*
 ====================================================================================================
  MUCK DISPLACEMENT MASS BALANCE & FOAM CONDITIONING METRICS
 ====================================================================================================
  Theoretical excavation volume rate: V_th = pi * (D/2)^2 * (v_adv / 60000) [m3/s]
  15.2-meter diameter: Face Area = pi * (15.2 / 2)^2 = 181.458 m2.
  At v_adv = 35.0 mm/min: V_th = 181.458 * (0.035 / 60) = 0.10585 m3/s = 381.0 m3/h.
*)
rTheoreticalMuckVolRate_m3_s := 181.458 * ((rAdvanceRateActual_mm_min / 60000.0));

(* Measured volumetric rate from belt scale (assuming average bulk muck density 1.65 t/m3) *)
IF rMuckBeltScale_MassFlow_t_h > 10.0 THEN
    rMeasuredMuckVolRate_m3_s := (rMuckBeltScale_MassFlow_t_h / 1.65) / 3600.0;
    IF rTheoreticalMuckVolRate_m3_s > 0.001 THEN
        rMuckDischargeRatio := rMeasuredMuckVolRate_m3_s / rTheoreticalMuckVolRate_m3_s;
    ELSE
        rMuckDischargeRatio := 1.0;
    END_IF;
ELSE
    rMeasuredMuckVolRate_m3_s := 0.0;
    rMuckDischargeRatio := 1.0;
END_IF;

(* Cumulative mass balance volume integration for over-excavation / sinkhole detection *)
IF (nState = 40) AND (rTheoreticalMuckVolRate_m3_s > 0.005) THEN
    rMuckBalanceErrorIntegral_m3 := rMuckBalanceErrorIntegral_m3 + ((rMeasuredMuckVolRate_m3_s - rTheoreticalMuckVolRate_m3_s) * rScanTime_s);
ELSIF nState = 0 THEN
    rMuckBalanceErrorIntegral_m3 := 0.0; (* Reset at ring start *)
END_IF;

(* Dynamic Foam Expansion Ratio (FER) and Foam Injection Ratio (FIR) calculation *)
IF rFoamLiquidFlowActual_L_min > 5.0 THEN
    (* FER = Total Foam Volume / Liquid Volume *)
    rFoamExpansionRatio_FER := LIMIT(4.0, (rFoamAirPressure_bar * 120.0) / rFoamLiquidFlowActual_L_min, 20.0);
ELSE
    rFoamExpansionRatio_FER := 11.2;
END_IF;

IF rTheoreticalMuckVolRate_m3_s > 0.005 THEN
    (* FIR = Generated Foam Volume [m3/s] / Excavated In-situ Soil Volume [m3/s] * 100 *)
    rFoamInjectionRatio_FIR_pct := LIMIT(10.0, (((rFoamLiquidFlowActual_L_min / 60000.0) * rFoamExpansionRatio_FER) / rTheoreticalMuckVolRate_m3_s) * 100.0, 95.0);
ELSE
    rFoamInjectionRatio_FIR_pct := 42.5;
END_IF;

(*
 ====================================================================================================
  PHASE 5: ISA-18.2 MULTI-TIERED ALARMS & DIAGNOSTIC WORD BITPACKING
 ====================================================================================================
  Implements standard ISA-18.2 finite-state alarm machines:
    State 0: NORMAL
    State 1: UNACKNOWLEDGED ALARM (Flashing indication)
    State 2: ACKNOWLEDGED ALARM (Steady indication)
    State 3: UNACKNOWLEDGED RETURN TO NORMAL (Latched ringdown)

  Monitors 10 distinct trip and warning points with strict hysteresis deadbands:
  1. Crown Pressure High-High (HH > 4.80 bar) -> Ground Heave Blowout Risk
  2. Crown Pressure High (H > 4.20 bar)      -> Slurry Chamber Overpressure
  3. Crown Pressure Low (L < 1.80 bar)       -> Surface Settlement Risk
  4. Crown Pressure Low-Low (LL < 1.20 bar)  -> Face Collapse Catastrophic Abort
  5. Cutterhead Torque High-High (HH > 46,000 kNm) -> Thermal Drive Breakdown
  6. Cutterhead Torque High (H > 40,000 kNm)       -> High Cutting Resistance
  7. Main Bearing Lube Water Ingress HH (> 500 ppm)-> Triple Lip Seal Failure
  8. Main Bearing Lube Water Ingress H (> 250 ppm) -> Grease Purge Degradation
  9. Main Bearing Sump Oil Temp HH (> 75.0 deg C)  -> Roller Scuffing Trip
  10. Propulsion Hydraulic Pressure HH (> 350.0 bar) -> Relief Valve Lift
*)

(* 1. Bulkhead Crown Earth Pressure High-High (HH > 4.80 bar, Hyst 0.10 bar) *)
IF rBulkheadCrownPressure_Voted_bar >= rSp_CrownHH_bar THEN
    rAlmTimer_CrownHH_s := rAlmTimer_CrownHH_s + rScanTime_s;
    IF rAlmTimer_CrownHH_s >= 0.15 THEN (* 150ms confirmation delay *)
        IF nAlmState_CrownHH = 0 THEN nAlmState_CrownHH := 1; END_IF;
    END_IF;
ELSIF rBulkheadCrownPressure_Voted_bar <= (rSp_CrownHH_bar - rHyst_Crown_bar) THEN
    rAlmTimer_CrownHH_s := 0.0;
    IF nAlmState_CrownHH = 1 THEN nAlmState_CrownHH := 3;
    ELSIF nAlmState_CrownHH = 2 THEN nAlmState_CrownHH := 0;
    END_IF;
END_IF;
IF bAlarmAckCmd THEN
    IF nAlmState_CrownHH = 1 THEN nAlmState_CrownHH := 2;
    ELSIF nAlmState_CrownHH = 3 THEN nAlmState_CrownHH := 0;
    END_IF;
END_IF;

(* 2. Bulkhead Crown Earth Pressure High (H > 4.20 bar, Hyst 0.10 bar) *)
IF rBulkheadCrownPressure_Voted_bar >= rSp_CrownH_bar THEN
    rAlmTimer_CrownH_s := rAlmTimer_CrownH_s + rScanTime_s;
    IF rAlmTimer_CrownH_s >= 0.50 THEN
        IF nAlmState_CrownH = 0 THEN nAlmState_CrownH := 1; END_IF;
    END_IF;
ELSIF rBulkheadCrownPressure_Voted_bar <= (rSp_CrownH_bar - rHyst_Crown_bar) THEN
    rAlmTimer_CrownH_s := 0.0;
    IF nAlmState_CrownH = 1 THEN nAlmState_CrownH := 3;
    ELSIF nAlmState_CrownH = 2 THEN nAlmState_CrownH := 0;
    END_IF;
END_IF;
IF bAlarmAckCmd THEN
    IF nAlmState_CrownH = 1 THEN nAlmState_CrownH := 2;
    ELSIF nAlmState_CrownH = 3 THEN nAlmState_CrownH := 0;
    END_IF;
END_IF;

(* 3. Bulkhead Crown Earth Pressure Low (L < 1.80 bar, Hyst 0.10 bar) *)
IF (rBulkheadCrownPressure_Voted_bar <= rSp_CrownL_bar) AND (nState >= 10) THEN
    rAlmTimer_CrownL_s := rAlmTimer_CrownL_s + rScanTime_s;
    IF rAlmTimer_CrownL_s >= 0.50 THEN
        IF nAlmState_CrownL = 0 THEN nAlmState_CrownL := 1; END_IF;
    END_IF;
ELSIF rBulkheadCrownPressure_Voted_bar >= (rSp_CrownL_bar + rHyst_Crown_bar) THEN
    rAlmTimer_CrownL_s := 0.0;
    IF nAlmState_CrownL = 1 THEN nAlmState_CrownL := 3;
    ELSIF nAlmState_CrownL = 2 THEN nAlmState_CrownL := 0;
    END_IF;
END_IF;
IF bAlarmAckCmd THEN
    IF nAlmState_CrownL = 1 THEN nAlmState_CrownL := 2;
    ELSIF nAlmState_CrownL = 3 THEN nAlmState_CrownL := 0;
    END_IF;
END_IF;

(* 4. Bulkhead Crown Earth Pressure Low-Low (LL < 1.20 bar, Hyst 0.10 bar) *)
IF (rBulkheadCrownPressure_Voted_bar <= rSp_CrownLL_bar) AND (nState >= 10) THEN
    rAlmTimer_CrownLL_s := rAlmTimer_CrownLL_s + rScanTime_s;
    IF rAlmTimer_CrownLL_s >= 0.20 THEN
        IF nAlmState_CrownLL = 0 THEN nAlmState_CrownLL := 1; END_IF;
    END_IF;
ELSIF rBulkheadCrownPressure_Voted_bar >= (rSp_CrownLL_bar + rHyst_Crown_bar) THEN
    rAlmTimer_CrownLL_s := 0.0;
    IF nAlmState_CrownLL = 1 THEN nAlmState_CrownLL := 3;
    ELSIF nAlmState_CrownLL = 2 THEN nAlmState_CrownLL := 0;
    END_IF;
END_IF;
IF bAlarmAckCmd THEN
    IF nAlmState_CrownLL = 1 THEN nAlmState_CrownLL := 2;
    ELSIF nAlmState_CrownLL = 3 THEN nAlmState_CrownLL := 0;
    END_IF;
END_IF;

(* 5. Cutterhead Total Mechanical Torque High-High (HH > 46,000 kNm, Hyst 1200 kNm) *)
IF rCutterheadTotalTorque_kNm >= rSp_TorqueHH_kNm THEN
    rAlmTimer_TorqueHH_s := rAlmTimer_TorqueHH_s + rScanTime_s;
    IF rAlmTimer_TorqueHH_s >= 0.10 THEN (* 100ms rapid electrical trip *)
        IF nAlmState_TorqueHH = 0 THEN nAlmState_TorqueHH := 1; END_IF;
    END_IF;
ELSIF rCutterheadTotalTorque_kNm <= (rSp_TorqueHH_kNm - rHyst_Torque_kNm) THEN
    rAlmTimer_TorqueHH_s := 0.0;
    IF nAlmState_TorqueHH = 1 THEN nAlmState_TorqueHH := 3;
    ELSIF nAlmState_TorqueHH = 2 THEN nAlmState_TorqueHH := 0;
    END_IF;
END_IF;
IF bAlarmAckCmd THEN
    IF nAlmState_TorqueHH = 1 THEN nAlmState_TorqueHH := 2;
    ELSIF nAlmState_TorqueHH = 3 THEN nAlmState_TorqueHH := 0;
    END_IF;
END_IF;

(* 6. Cutterhead Total Mechanical Torque High (H > 40,000 kNm, Hyst 1200 kNm) *)
IF rCutterheadTotalTorque_kNm >= rSp_TorqueH_kNm THEN
    rAlmTimer_TorqueH_s := rAlmTimer_TorqueH_s + rScanTime_s;
    IF rAlmTimer_TorqueH_s >= 1.00 THEN
        IF nAlmState_TorqueH = 0 THEN nAlmState_TorqueH := 1; END_IF;
    END_IF;
ELSIF rCutterheadTotalTorque_kNm <= (rSp_TorqueH_kNm - rHyst_Torque_kNm) THEN
    rAlmTimer_TorqueH_s := 0.0;
    IF nAlmState_TorqueH = 1 THEN nAlmState_TorqueH := 3;
    ELSIF nAlmState_TorqueH = 2 THEN nAlmState_TorqueH := 0;
    END_IF;
END_IF;
IF bAlarmAckCmd THEN
    IF nAlmState_TorqueH = 1 THEN nAlmState_TorqueH := 2;
    ELSIF nAlmState_TorqueH = 3 THEN nAlmState_TorqueH := 0;
    END_IF;
END_IF;

(* 7. Main Slewing Bearing Water Ingress High-High (HH > 500 ppm, Hyst 40 ppm) *)
IF rMainBearingWaterContent_ppm >= rSp_WaterHH_ppm THEN
    rAlmTimer_WaterHH_s := rAlmTimer_WaterHH_s + rScanTime_s;
    IF rAlmTimer_WaterHH_s >= 2.00 THEN
        IF nAlmState_WaterHH = 0 THEN nAlmState_WaterHH := 1; END_IF;
    END_IF;
ELSIF rMainBearingWaterContent_ppm <= (rSp_WaterHH_ppm - rHyst_Water_ppm) THEN
    rAlmTimer_WaterHH_s := 0.0;
    IF nAlmState_WaterHH = 1 THEN nAlmState_WaterHH := 3;
    ELSIF nAlmState_WaterHH = 2 THEN nAlmState_WaterHH := 0;
    END_IF;
END_IF;
IF bAlarmAckCmd THEN
    IF nAlmState_WaterHH = 1 THEN nAlmState_WaterHH := 2;
    ELSIF nAlmState_WaterHH = 3 THEN nAlmState_WaterHH := 0;
    END_IF;
END_IF;

(* 8. Main Slewing Bearing Water Ingress High (H > 250 ppm, Hyst 40 ppm) *)
IF rMainBearingWaterContent_ppm >= rSp_WaterH_ppm THEN
    rAlmTimer_WaterH_s := rAlmTimer_WaterH_s + rScanTime_s;
    IF rAlmTimer_WaterH_s >= 5.00 THEN
        IF nAlmState_WaterH = 0 THEN nAlmState_WaterH := 1; END_IF;
    END_IF;
ELSIF rMainBearingWaterContent_ppm <= (rSp_WaterH_ppm - rHyst_Water_ppm) THEN
    rAlmTimer_WaterH_s := 0.0;
    IF nAlmState_WaterH = 1 THEN nAlmState_WaterH := 3;
    ELSIF nAlmState_WaterH = 2 THEN nAlmState_WaterH := 0;
    END_IF;
END_IF;
IF bAlarmAckCmd THEN
    IF nAlmState_WaterH = 1 THEN nAlmState_WaterH := 2;
    ELSIF nAlmState_WaterH = 3 THEN nAlmState_WaterH := 0;
    END_IF;
END_IF;

(* 9. Main Bearing Sump Oil Temperature High-High (HH > 75.0 deg C, Hyst 4.0 deg C) *)
IF rMainBearingOilTemp_C >= rSp_LubeTempHH_C THEN
    rAlmTimer_LubeTempHH_s := rAlmTimer_LubeTempHH_s + rScanTime_s;
    IF rAlmTimer_LubeTempHH_s >= 1.50 THEN
        IF nAlmState_LubeTempHH = 0 THEN nAlmState_LubeTempHH := 1; END_IF;
    END_IF;
ELSIF rMainBearingOilTemp_C <= (rSp_LubeTempHH_C - rHyst_LubeTemp_C) THEN
    rAlmTimer_LubeTempHH_s := 0.0;
    IF nAlmState_LubeTempHH = 1 THEN nAlmState_LubeTempHH := 3;
    ELSIF nAlmState_LubeTempHH = 2 THEN nAlmState_LubeTempHH := 0;
    END_IF;
END_IF;
IF bAlarmAckCmd THEN
    IF nAlmState_LubeTempHH = 1 THEN nAlmState_LubeTempHH := 2;
    ELSIF nAlmState_LubeTempHH = 3 THEN nAlmState_LubeTempHH := 0;
    END_IF;
END_IF;

(* 10. Hydraulic Propulsion Pressure High-High (HH > 350.0 bar, Hyst 12.0 bar) *)
IF (rThrustPressure_Q1_bar >= rSp_ThrustHydrHH_bar) OR
   (rThrustPressure_Q2_bar >= rSp_ThrustHydrHH_bar) OR
   (rThrustPressure_Q3_bar >= rSp_ThrustHydrHH_bar) OR
   (rThrustPressure_Q4_bar >= rSp_ThrustHydrHH_bar) THEN
    rAlmTimer_ThrustHydrHH_s := rAlmTimer_ThrustHydrHH_s + rScanTime_s;
    IF rAlmTimer_ThrustHydrHH_s >= 0.10 THEN
        IF nAlmState_ThrustHydrHH = 0 THEN nAlmState_ThrustHydrHH := 1; END_IF;
    END_IF;
ELSE
    rAlmTimer_ThrustHydrHH_s := 0.0;
    IF nAlmState_ThrustHydrHH = 1 THEN nAlmState_ThrustHydrHH := 3;
    ELSIF nAlmState_ThrustHydrHH = 2 THEN nAlmState_ThrustHydrHH := 0;
    END_IF;
END_IF;
IF bAlarmAckCmd THEN
    IF nAlmState_ThrustHydrHH = 1 THEN nAlmState_ThrustHydrHH := 2;
    ELSIF nAlmState_ThrustHydrHH = 3 THEN nAlmState_ThrustHydrHH := 0;
    END_IF;
END_IF;

(*
 ====================================================================================================
  DIAGNOSTIC WORD BITPACKING & OPERATIONAL STATUS PACKAGING
 ====================================================================================================
*)

(* Pack wAlarmWord_Priority1 (Emergency Trips) *)
wAlarmWord_Priority1 := 16#0000;
IF (nAlmState_CrownHH = 1) OR (nAlmState_CrownHH = 2) THEN wAlarmWord_Priority1 := wAlarmWord_Priority1 OR 16#0001; END_IF;
IF (nAlmState_CrownLL = 1) OR (nAlmState_CrownLL = 2) THEN wAlarmWord_Priority1 := wAlarmWord_Priority1 OR 16#0002; END_IF;
IF (nAlmState_TorqueHH = 1) OR (nAlmState_TorqueHH = 2) THEN wAlarmWord_Priority1 := wAlarmWord_Priority1 OR 16#0004; END_IF;
IF (nAlmState_WaterHH = 1) OR (nAlmState_WaterHH = 2) THEN wAlarmWord_Priority1 := wAlarmWord_Priority1 OR 16#0008; END_IF;
IF (nAlmState_LubeTempHH = 1) OR (nAlmState_LubeTempHH = 2) THEN wAlarmWord_Priority1 := wAlarmWord_Priority1 OR 16#0010; END_IF;
IF (nAlmState_ThrustHydrHH = 1) OR (nAlmState_ThrustHydrHH = 2) THEN wAlarmWord_Priority1 := wAlarmWord_Priority1 OR 16#0020; END_IF;
IF NOT bEStopActivated THEN wAlarmWord_Priority1 := wAlarmWord_Priority1 OR 16#0040; END_IF;
IF bDegradedSensorMode AND (nHealthySensorCount = 0) THEN wAlarmWord_Priority1 := wAlarmWord_Priority1 OR 16#0080; END_IF;

(* Pack wAlarmWord_Priority2 (Operating Warnings) *)
wAlarmWord_Priority2 := 16#0000;
IF (nAlmState_CrownH = 1) OR (nAlmState_CrownH = 2) THEN wAlarmWord_Priority2 := wAlarmWord_Priority2 OR 16#0001; END_IF;
IF (nAlmState_CrownL = 1) OR (nAlmState_CrownL = 2) THEN wAlarmWord_Priority2 := wAlarmWord_Priority2 OR 16#0002; END_IF;
IF (nAlmState_TorqueH = 1) OR (nAlmState_TorqueH = 2) THEN wAlarmWord_Priority2 := wAlarmWord_Priority2 OR 16#0004; END_IF;
IF (nAlmState_WaterH = 1) OR (nAlmState_WaterH = 2) THEN wAlarmWord_Priority2 := wAlarmWord_Priority2 OR 16#0008; END_IF;
IF bDegradedSensorMode THEN wAlarmWord_Priority2 := wAlarmWord_Priority2 OR 16#0010; END_IF;
IF (rCutterheadTorqueImbalance_pct > 20.0) THEN wAlarmWord_Priority2 := wAlarmWord_Priority2 OR 16#0020; END_IF;
IF (ABS(rMuckDischargeRatio - 1.0) > 0.20) THEN wAlarmWord_Priority2 := wAlarmWord_Priority2 OR 16#0040; END_IF;
IF (ABS(rLaserDeviationHoriz_mm) > 100.0) OR (ABS(rLaserDeviationVert_mm) > 100.0) THEN wAlarmWord_Priority2 := wAlarmWord_Priority2 OR 16#0080; END_IF;

(* Pack wStateStatusWord (FSM State & Operational Discrete Telemetry) *)
wStateStatusWord := INT_TO_WORD(nState) AND 16#00FF;
IF bChamberPressureStabilized THEN wStateStatusWord := wStateStatusWord OR 16#0100; END_IF;
IF bRingAdvanceComplete THEN wStateStatusWord := wStateStatusWord OR 16#0200; END_IF;
IF bObstacleDetected THEN wStateStatusWord := wStateStatusWord OR 16#0400; END_IF;
IF bDegradedSensorMode THEN wStateStatusWord := wStateStatusWord OR 16#0800; END_IF;
IF bEmergencyStopTriggered THEN wStateStatusWord := wStateStatusWord OR 16#1000; END_IF;
IF bRingErectInterlockClear THEN wStateStatusWord := wStateStatusWord OR 16#2000; END_IF;
IF (rAdvanceRateActual_mm_min > 1.0) THEN wStateStatusWord := wStateStatusWord OR 16#4000; END_IF;
IF (rCutterheadSpeedTarget_RPM > 0.1) THEN wStateStatusWord := wStateStatusWord OR 16#8000; END_IF;

(* Pack wDiagnosticWord (Sensor Health Bits, VFD Status, Subsystem Health) *)
wDiagnosticWord := 16#00000000;
IF NOT bPT101_Failed THEN wDiagnosticWord := wDiagnosticWord OR 16#00000001; END_IF;
IF NOT bPT102_Failed THEN wDiagnosticWord := wDiagnosticWord OR 16#00000002; END_IF;
IF NOT bPT103_Failed THEN wDiagnosticWord := wDiagnosticWord OR 16#00000004; END_IF;
IF (rMainBearingSealPressure_bar >= 2.5) THEN wDiagnosticWord := wDiagnosticWord OR 16#00000008; END_IF;

(* Check individual motor VFD health into bits 8..23 *)
FOR iMotor := 1 TO 16 DO
    IF NOT aMotorVFD_Fault[iMotor] THEN
        wDiagnosticWord := wDiagnosticWord OR SHL(16#00000001, 7 + iMotor);
    END_IF;
END_FOR;

IF (nHealthySensorCount = 3) THEN wDiagnosticWord := wDiagnosticWord OR 16#01000000; END_IF;
IF (nHealthySensorCount = 2) THEN wDiagnosticWord := wDiagnosticWord OR 16#02000000; END_IF;
IF (nHealthySensorCount = 1) THEN wDiagnosticWord := wDiagnosticWord OR 16#04000000; END_IF;
IF (nHealthySensorCount = 0) THEN wDiagnosticWord := wDiagnosticWord OR 16#08000000; END_IF;
IF (rCostJ < 5000.0) THEN wDiagnosticWord := wDiagnosticWord OR 16#10000000; END_IF; (* MPC Converged *)
IF (rMuckBalanceErrorIntegral_m3 > 50.0) THEN wDiagnosticWord := wDiagnosticWord OR 16#20000000; END_IF; (* Over-excavation risk *)
IF (rMuckBalanceErrorIntegral_m3 < -50.0) THEN wDiagnosticWord := wDiagnosticWord OR 16#40000000; END_IF; (* Chamber clogging risk *)

END_FUNCTION_BLOCK
```'''
    return code

def main():
    prompt = """You are generating a SINGLE ultra-dense IEC 61131-3 Structured Text dataset for the **Heavy Civil Infrastructure & Tunneling** industry.

**Domain**: 15-Meter Large-Diameter Earth Pressure Balance (EPB) Tunnel Boring Machine (TBM) with Multi-Motor Cutterhead Drive Torque Coordination & Bentonite Slurry Chamber Pressure Stabilization.

**Function Block Name**: `FB_HeavyCivil_TBM_EPBCutterhead_SlurryPressure`

**Engineering Context**:
- 15.2-meter diameter multi-mode EPB / slurry shield TBM boring through mixed face geology (water-bearing sands, gravels, weathered rock)
- 16 × 350 kW variable-frequency drive (VFD) electric cutterhead motors (total drive power 5.6 MW, maximum breakout torque up to 48,000 kNm)
- Closed excavation chamber with bentonite foam/polymer conditioning injection nozzles (air pressure regulation 1.5 to 4.5 bar)
- 40 thrust hydraulic cylinders arranged in 4 quadrants (thrust force up to 220,000 kN, advance speed 0 to 60 mm/min)
- Earth pressure balance: 12 earth pressure sensors mounted across the bulkhead wall balancing hydrostatic groundwater pressure
- Variable-speed screw conveyor (1.2m diameter, twin drive, 0 to 22 RPM) discharging conditioned muck with displacement mass flow balance
- Laser target guidance system (active articulated steering cylinders monitoring roll, pitch, and yaw ring articulation offsets)
- EN 16191 safety of tunneling machinery compliance

**Required Mathematical Rigor** (ALL must be explicitly coded with complete equations and matrix constants):
1. **Discrete State-Space Matrix Model** for excavation chamber face pressure, cutterhead torque ripple & advance rate:
   - State vector x = [bulkhead_pressure_bar, cutterhead_torque_knm, screw_conveyor_fill_ratio, thrust_advance_rate_mm_min]
   - Full numerical matrices A (4×4) and B (4×3 screw RPM / thrust cylinder servo / foam injection commands)
   - Dynamic propagation: x_{k+1} = A*x_k + B*u_k evaluated at 50ms scan
2. **Model Predictive Control (MPC) Quadratic Cost Approximation**:
   - Excavation face earth pressure stabilization (target ±0.15 bar) to prevent surface subsidence settlement or blow-out heave
   - Q matrix (4×4 earth pressure/torque error penalty) and R matrix (3×3 screw conveyor/thrust slew penalty)
   - Terminal cost matrix P (4×4)
3. **2oo3 (Two-out-of-Three) Triple Modular Redundant (TMR) Voting**:
   - 3 diaphragm earth pressure transmitters located at the bulkhead crown (top zone)
   - Discrepancy trip (0.35 bar limit) with automated screw conveyor speed trim and foam injection adjustment
4. **ISA-18.2 Multi-Tiered Alarm Ladder**:
   - Bulkhead earth pressure: HH (> 4.8 bar ground heave blowout risk), H (> 4.2 bar), L (< 1.8 bar ground settlement risk), LL (< 1.2 bar face collapse abort)
   - Cutterhead torque overload: HH (> 46,000 kNm motor thermal trip), H (> 40,000 kNm)
   - Main bearing lube oil contamination: HH (water ingress detected)
5. **Multi-Stage Finite State Machine (FSM)**:
   - States: TBM_PARKED_IDLE (0) -> CHAMBER_PRESSURE_PRECHARGE (10) -> CUTTERHEAD_ROTATION_START (20) -> THRUST_CYLINDER_STROKE_EXTEND (30) -> STEADY_STATE_EPB_EXCAVATION (40) -> RING_ADVANCE_STROKE_END (50) -> SEGMENT_RING_ERECT_INTERLOCK (60) -> BENTONITE_FOAM_CONDITIONING_TRIM (70) -> GEOLOGY_OBSTACLE_TORQUE_DECEL (80) -> PLANNED_CUTTER_TOOL_INSPECT (90) -> FACE_COLLAPSE_EMERGENCY_SHUTDOWN (99)

**Output Format**:
- Code fenced with TRIPLE backticks and `iec-st`: ` ```iec-st `
- First line: `FUNCTION_BLOCK FB_HeavyCivil_TBM_EPBCutterhead_SlurryPressure`
- Last line: `END_FUNCTION_BLOCK`
- Minimum length: 45,000 to 75,000+ characters of deeply engineered Structured Text.

Save output to `data/swarm_raw/agent_<uuid>.json` and reply: `EVOLUTION COMPLETE: Heavy Civil TBM EPB Cutterhead Slurry Pressure`"""

    code = generate_iec_code()
    print(f"Generated Code Character Count: {len(code)}")

    # Parity checks with proper regex on clean code
    import re
    clean_code = re.sub(r'\(\*.*?\*\)', '', code, flags=re.DOTALL)
    clean_code = re.sub(r'//.*', '', clean_code)

    if_count = len(re.findall(r'\bIF\b', clean_code))
    end_if_count = len(re.findall(r'\bEND_IF\b', clean_code))
    case_count = len(re.findall(r'\bCASE\b', clean_code))
    end_case_count = len(re.findall(r'\bEND_CASE\b', clean_code))
    for_count = len(re.findall(r'\bFOR\b', clean_code))
    end_for_count = len(re.findall(r'\bEND_FOR\b', clean_code))

    print(f"Parity: IF={if_count}, END_IF={end_if_count}")
    print(f"Parity: CASE={case_count}, END_CASE={end_case_count}")
    print(f"Parity: FOR={for_count}, END_FOR={end_for_count}")

    assert if_count == end_if_count, f"IF parity mismatch: {if_count} != {end_if_count}"
    assert case_count == end_case_count, f"CASE parity mismatch: {case_count} != {end_case_count}"
    assert for_count == end_for_count, f"FOR parity mismatch: {for_count} != {end_for_count}"

    assert code.startswith("```iec-st\nFUNCTION_BLOCK FB_HeavyCivil_TBM_EPBCutterhead_SlurryPressure")
    assert code.strip().endswith("END_FUNCTION_BLOCK\n```")

    record = {
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": code}
        ]
    }

    agent_id = uuid.uuid4().hex[:8]
    filename = f"data/swarm_raw/agent_{agent_id}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)

    print(f"Successfully saved record to: {filename}")
    print(f"Total file size: {os.path.getsize(filename)} bytes")
    print(f"Agent ID: {agent_id}")

if __name__ == "__main__":
    main()
