# -*- coding: utf-8 -*-
"""
Builder script for FB_MetalProcessing_CoilSlitting_RotaryFlyingShear
Dataset target: data/swarm_raw/agent_519a712e.json
Commercial Sector: Continuous Coil Slitting & Rotary Flying Shear Metal Cut-to-Length Lines (Rank #98)
"""
import os
import json
import subprocess

def generate_iec_code():
    code_parts = []
    
    # 1. Opening line
    code_parts.append("FUNCTION_BLOCK FB_MetalProcessing_CoilSlitting_RotaryFlyingShear\n")
    
    # 2. Header documentation
    header = """(*
========================================================================================================================
LUMINA CYBER-PHYSICAL AUTOMATION ENGINE - SYNTHETIC DATASET V7 MAX-PERSONA
HIGH-SPEED METAL PROCESSING DIVISION - CONTINUOUS COIL SLITTING & ROTARY FLYING SHEAR CUT-TO-LENGTH
========================================================================================================================
SYSTEM ARCHITECTURE SPECIFICATION:
  - High-Speed Heavy-Gauge Continuous Steel Strip Slitting and Rotary Flying Shear Cut-to-Length Production Line.
  - Raw Material Envelope: Cold-Rolled Carbon Steel, Galvanized Automotive Sheet, HSLA Strip (0.5 mm to 4.5 mm gauge).
  - Coil Envelope: Strip Width 600 mm to 1,850 mm; Maximum Coil Mass 30,000 kg (30 metric tons); Outer Diameter to 2,000 mm.
  - Production Throughput: Continuous Web Processing Velocity 0 to 120.0 m/min (2.000 m/s steady-state line velocity).
  - High-Precision Rotary Flying Shear: Dual-Shaft Helical Knife Cylindrical Drums (Radius = 0.300 m, Circumference = 1.885 m).
  - Sheet Cut-Length Precision Target: Cut Length 500.0 mm to 6,000.0 mm with Tolerance Window < +/- 0.150 mm at 120 m/min.
  
CYBER-PHYSICAL CONTROL SUBSYSTEMS & MATHEMATICAL RIGOR:
  1. Discrete State-Space Dynamic Matrices (A, B, C, D) [8 States x 4 Inputs, Discretized at Ts = 0.001 s (1 kHz motion task)]:
     - State x1: Uncoiler Coil Outer Radius Dynamic Deviation / Tracking Error [m].
     - State x2: Payoff Reel Uncoiler Mandrel Angular Velocity [rad/s].
     - State x3: Entry Bridle Tension Accumulator / Dancer Roll Vertical Position Displacement [m].
     - State x4: Inter-Stand Elastic Web Tension Force [N] (Hooke's Viscoelastic Web Law with Cross-Sectional Area A = W * t).
     - State x5: Rotary Shear Blade Drum Synchronous Angle Relative to Moving Web [rad].
     - State x6: Rotary Shear Blade Drum Angular Velocity [rad/s].
     - State x7: Integrated Sheet Cut-Length Precision Error [m].
     - State x8: High-Speed Vacuum Run-Out Sheet Conveyor Linear Transport Speed [m/s].
  2. Payoff Reel Uncoiler Dynamic Inertia Observer & Back-Tension Torque Control:
     - Real-time strip consumption volumetric integration yielding continuous coil radius R(t).
     - High-inertia reel physics: Moment of inertia J(t) varies from J_mandrel (120 kg*m2) to J_full (> 3,850 kg*m2).
     - Dynamic feedforward torque decoupling: tau_payoff = T_target * R(t) + J(t) * alpha_payoff + b_bearing * omega.
  3. Receding-Horizon Model Predictive Control (MPC) Quadratic Optimization:
     - Dual-objective cost formulation: Minimizing inter-stand web tension error (eliminating web necking and strip buckling)
       while simultaneously driving rotary shear electronic cam synchronization error to zero prior to knife penetration.
     - State penalty matrix Q (8x8 diagonal), actuator rate penalty matrix R (4x4), and terminal algebraic Riccati cost P (8x8).
     - Active-set projected gradient numerical optimizer enforcing strict torque and acceleration actuator boundaries.
  4. 5th-Order Polynomial Electronic Cam Rotary Flying Shear Motion Profile:
     - Trajectory polynomial s(tau) = 10*tau^3 - 15*tau^4 + 6*tau^5 ensuring C2-continuous displacement, velocity, and zero jerk.
     - Blade tip tangential speed dynamically matched to 2oo3-voted strip velocity at cutting window (0.0% relative velocity slip).
     - Automatic dynamic cam phasing for short sheets (cut length < shear circumference) and long sheets (cut length > circumference).
  5. 2oo3 (Two-Out-Of-Three) Triple Modular Redundancy (TMR) Sensor Voting & Discrepancy Arbitration:
     - Speed Sensing: Triple Non-Contact Laser Doppler Velocimeters (LDV1, LDV2, LDV3).
     - Length & Position Sensing: Triple High-Resolution Optical Quadrature Master Line Encoders (Enc_A, Enc_B, Enc_C).
     - Tension Sensing: Triple S-Type Precision Dual-Flange Strain Gage Load Cell Transducers (LC1, LC2, LC3).
     - Discrepancy detection with programmable hysteresis dwell timers, degraded 1oo2 failover, and dual-sensor safety trip.
  6. Closed-Loop Electro-Hydraulic Edge Position Control (EPC / CPC):
     - High-frequency ultrasonic strip edge detection with servo-cylinder proportional-integral-derivative lateral centering.
  7. High-Speed Slitting Head Knife Penetration & Polyurethane Stripper Ring Dynamics:
     - Upper arbor vertical servo positioning maintaining exact blade overlap (0.2 mm to 1.5 mm depending on steel gauge).
  8. Run-Out Vacuum Sheet Conveyor, Solenoid Reject Scrap Divert Gate, and Magnetic Stacker Table:
     - High-speed belt speed lead (+10% line velocity) for creating inter-sheet transfer gaps.
     - Pneumatic scrap gate flipper actively diverting out-of-spec sheets (|error| > 0.20 mm or ultrasonic weld seam detection).
  9. ISA-18.2 Multi-Tiered Process Alarm Matrix:
     - Four-tier alarming (HH, H, L, LL) covering web tension collapse (breakage), shear synchronization fault, and mandrel pressure loss.
========================================================================================================================
*)
"""
    code_parts.append(header)
    
    # 3. VAR_INPUT
    var_input = """VAR_INPUT
    (* Master Automation Supervisory Commands & Safety Monitored Interlocks *)
    bEnableMasterLine           : BOOL;     (* Master line automation enable permit interlock [-] *)
    bAutoCycleStart             : BOOL;     (* Automatic cut-to-length continuous sequence start [TRUE=START] *)
    bEmergencyStopOk            : BOOL;     (* Monitored dual-channel hardwired E-stop safety circuit [TRUE=HEALTHY] *)
    bResetFault                 : BOOL;     (* Master system alarm acknowledgement and latch reset push-button [-] *)
    
    (* Master Line Speed & Coil Material Parameters *)
    rLineSpeedSet_m_min         : REAL;     (* Master process strip linear velocity setpoint reference [m/min] *)
    rTargetSheetLength_mm       : REAL;     (* Desired precision cut sheet target length setpoint [mm] *)
    rStripWidth_mm              : REAL;     (* Incoming master steel coil nominal strip width [mm] *)
    rStripThickness_mm          : REAL;     (* Steel strip nominal calibrated physical thickness [mm] *)
    rStripYieldStrength_MPa     : REAL;     (* Material mechanical yield strength for shear force model [MPa] *)
    rTargetTension_kN           : REAL;     (* Process inter-stand web tensile force setpoint reference [kN] *)
    rCoilOuterDiaInitial_mm     : REAL;     (* Raw master coil initial measured outer diameter at loading [mm] *)
    rMandrelCoreDia_mm          : REAL;     (* Uncoiler mandrel collapsed core drum diameter [mm] *)
    
    (* Hydraulic & Mechanical Actuator Transducers *)
    rMandrelHydPressure_bar     : REAL;     (* Payoff reel mandrel wedge expansion hydraulic cylinder pressure [bar] *)
    rEdgeGuideSensor_mm         : REAL;     (* Ultrasonic strip edge deviation displacement from centerline [mm] *)
    rSlitterArborPenetration_mm : REAL;     (* Upper rotary circular knife arbor vertical plunge position [mm] *)
    
    (* 2oo3 TMR Triplet 1: Strip Linear Velocity Sensors (Laser Doppler Velocimeters) *)
    rSpeedSensor_LDV1_m_min     : REAL;     (* Non-contact Laser Doppler Velocimeter optical channel 1 [m/min] *)
    rSpeedSensor_LDV2_m_min     : REAL;     (* Non-contact Laser Doppler Velocimeter optical channel 2 [m/min] *)
    rSpeedSensor_LDV3_m_min     : REAL;     (* Non-contact Laser Doppler Velocimeter optical channel 3 [m/min] *)
    
    (* 2oo3 TMR Triplet 2: Master Measuring Bridle Optical Incremental Encoders *)
    rEncoder_LineMaster_A_mm    : REAL;     (* Master measuring roll optical encoder channel A accumulated position [mm] *)
    rEncoder_LineMaster_B_mm    : REAL;     (* Master measuring roll optical encoder channel B accumulated position [mm] *)
    rEncoder_LineMaster_C_mm    : REAL;     (* Master measuring roll optical encoder channel C accumulated position [mm] *)
    
    (* 2oo3 TMR Triplet 3: Entry Bridle Web Tension Load Cells *)
    rTensionLoadCell_1_kN       : REAL;     (* Heavy-duty strain gage load cell sensor transducer channel 1 [kN] *)
    rTensionLoadCell_2_kN       : REAL;     (* Heavy-duty strain gage load cell sensor transducer channel 2 [kN] *)
    rTensionLoadCell_3_kN       : REAL;     (* Heavy-duty strain gage load cell sensor transducer channel 3 [kN] *)
    
    (* Dancer Roll & Shear Drum Motion Transducers *)
    rDancerPosition_mm          : REAL;     (* Counterbalanced tension dancer roll vertical stroke displacement [mm] *)
    rShearShaftAngle_deg        : REAL;     (* Rotary flying shear drum absolute optical resolver angle [deg] *)
    rShearShaftVelocity_RPM     : REAL;     (* Rotary flying shear drum servo motor angular velocity [RPM] *)
    
    (* Quality & Stacking Digital Sensors *)
    bWeldSeamDetected           : BOOL;     (* Ultrasonic coil-joining weld detector pulse [TRUE=DEFECTIVE_WELD] *)
    bManualScrapDumpCmd         : BOOL;     (* Operator console push-button to force scrap gate diversion [-] *)
    bPalletFullSignal           : BOOL;     (* Magnetic stacker hydraulic lift table bundle capacity full sensor [-] *)
END_VAR
"""
    code_parts.append(var_input)
    
    # 4. VAR_OUTPUT
    var_output = """VAR_OUTPUT
    (* Line Operational Status & Master Drive Interlocks *)
    bLineRunning                : BOOL;     (* Master continuous coil processing line running status [TRUE=RUN] *)
    bLineFaultActive            : BOOL;     (* Master process emergency fault trip condition present [TRUE=FAULT] *)
    bLineWarningActive          : BOOL;     (* Process operational advisory warning active [TRUE=WARNING] *)
    
    (* Real-Time Drive Motion Commands & Actuator Signals *)
    rUncoilerTorqueCommand_Nm   : REAL;     (* Payoff reel regenerative AC vector drive braking torque command [Nm] *)
    rEntryBridleSpeedRef_m_min  : REAL;     (* Entry S-wrap master pull bridle linear speed reference [m/min] *)
    rEdgeGuideCylinderCommand_pct: REAL;    (* Electro-hydraulic proportional directional valve command [-100..+100%] *)
    rSlitterArborTorque_Nm      : REAL;     (* Rotary circular knife slitting arbor motor torque reference [Nm] *)
    rRotaryShearTorqueCommand_Nm: REAL;     (* Rotary flying shear servo dynamic cutting torque reference command [Nm] *)
    rRotaryShearCamPosRef_deg   : REAL;     (* 5th-order electronic cam synchronous angular position command [deg] *)
    rRotaryShearCamVelRef_RPM   : REAL;     (* 5th-order electronic cam synchronous angular velocity command [RPM] *)
    rStackerBeltSpeed_m_min     : REAL;     (* Vacuum run-out sheet transport belt linear velocity command [m/min] *)
    bScrapDivertGateActive      : BOOL;     (* High-speed pneumatic scrap gate diverter solenoid valve [TRUE=DIVERT] *)
    bSheetCutStrokePulse        : BOOL;     (* Flying shear knife cutting synchronization point trigger pulse [-] *)
    
    (* 2oo3 Arbitrated Plant Measurements *)
    rActualStripSpeed_m_min     : REAL;     (* 2oo3 arbitrated true line strip linear velocity [m/min] *)
    rActualStripTension_kN      : REAL;     (* 2oo3 arbitrated true inter-stand strip tensile force [kN] *)
    rActualStripPosition_m      : REAL;     (* 2oo3 arbitrated master measuring roll integrated travel distance [m] *)
    rCurrentCoilRadius_mm       : REAL;     (* Real-time dynamic estimated outer radius of payoff coil [mm] *)
    rActualCutLength_mm         : REAL;     (* High-resolution measured physical length of last cut sheet [mm] *)
    rLengthErrorLastCut_mm      : REAL;     (* Mathematical deviation between target length and measured cut length [mm] *)
    
    (* Cumulative Production Counters & Diagnostic Diagnostics *)
    udiTotalCutCount            : UDINT;    (* Total prime cut sheets passed to magnetic stacking pallet [-] *)
    udiScrapCutCount            : UDINT;    (* Total rejected sheets diverted into scrap collection bin [-] *)
    eOperationalState           : INT;      (* Active finite state machine sequential state enumeration index [-] *)
    wAutomationStatusWord       : WORD;     (* Master automation bitfield packed status word [16#0000] *)
    wAlarmWord_Critical_ISA18   : WORD;     (* ISA-18.2 Critical Emergency Trip Bitfield Packed Word [16#0000] *)
    wAlarmWord_Warning_ISA18    : WORD;     (* ISA-18.2 Process Warning Advisory Bitfield Packed Word [16#0000] *)
END_VAR
"""
    code_parts.append(var_output)
    
    # 5. VAR block with extensive internal matrices and variables
    var_internal = """VAR
    (* ================================================================================================================ *)
    (* SECTION 0: DISCRETE STATE-SPACE MATRICES & OBSERVER STATE VECTORS (8x8 Plant Model, Ts = 0.001 s)                *)
    (* ================================================================================================================ *)
    matA                        : ARRAY[1..8, 1..8] OF REAL; (* Discrete State Transition Matrix A (8x8) *)
    matB                        : ARRAY[1..8, 1..4] OF REAL; (* Discrete Control Input Matrix B (8x4) *)
    matC                        : ARRAY[1..8, 1..8] OF REAL; (* State Output Measurement Matrix C (8x8) *)
    matD                        : ARRAY[1..8, 1..4] OF REAL; (* Direct Feedthrough Transmission Matrix D (8x4) *)
    matL                        : ARRAY[1..8, 1..8] OF REAL; (* Discrete Luenberger Observer State Gain Matrix L (8x8) *)
    
    vecX_hat                    : ARRAY[1..8] OF REAL;       (* Estimated State Vector [R_err, w_pay, y_dan, Ten, th_shr, w_shr, e_len, v_stk] *)
    vecX_pred                   : ARRAY[1..8] OF REAL;       (* One-Step Ahead Predictive State Propagation Vector *)
    vecU_cmd                    : ARRAY[1..4] OF REAL;       (* Plant Actuator Vector [tau_uncoil, v_bridle, tau_shear, a_stacker] *)
    vecY_meas                   : ARRAY[1..8] OF REAL;       (* Sensor Feedback Measurement Observation Vector *)
    vecY_err                    : ARRAY[1..8] OF REAL;       (* Observer Innovation Residual Error Vector (y - C*x_hat) *)
    
    bMatricesInitialized        : BOOL := FALSE;             (* One-Time Initialization Flag for Deterministic Arrays *)
    
    (* ================================================================================================================ *)
    (* SECTION 1: MODEL PREDICTIVE CONTROL (MPC) RECEDING-HORIZON QUADRATIC MATRICES (Q, R, P)                          *)
    (* ================================================================================================================ *)
    matQ                        : ARRAY[1..8, 1..8] OF REAL; (* State Deviation Quadratic Penalty Matrix Q (8x8 Diagonal) *)
    matR                        : ARRAY[1..4, 1..4] OF REAL; (* Actuator Effort Rate Quadratic Penalty Matrix R (4x4 Diagonal) *)
    matP                        : ARRAY[1..8, 1..8] OF REAL; (* Terminal Riccati Boundary Penalty Matrix P (8x8 Diagonal) *)
    
    matHessian                  : ARRAY[1..4, 1..4] OF REAL; (* Quadratic Cost Hessian Approximation Matrix H (4x4) *)
    vecGrad_J                   : ARRAY[1..4] OF REAL;       (* Cost Functional Gradient Vector grad(J) (4x1) *)
    vecDeltaU                   : ARRAY[1..4] OF REAL;       (* Optimal Incremental Control Correction Vector *)
    vecU_opt                    : ARRAY[1..4] OF REAL;       (* Unconstrained MPC Optimal Command Vector *)
    
    rMpcStepAlpha               : REAL := 0.035;             (* Projected Gradient Descent Numerical Step Size [-] *)
    iMpcIterIdx                 : INT;                       (* Active-Set Gradient Descent Loop Iteration Counter *)
    iMpcRow                     : INT;                       (* Row Loop Index for Matrix-Vector Dot Product Operations *)
    iMpcCol                     : INT;                       (* Column Loop Index for Matrix-Vector Dot Product Operations *)
    iMpcState                   : INT;                       (* State Index for Observer and Predictive Propagation *)
    
    (* Actuator Physical Saturation Boundary Constraints *)
    rUncoilerTorqueMin_Nm       : REAL := -12500.0;          (* Maximum Uncoiler Dynamic Regenerative Braking Torque [Nm] *)
    rUncoilerTorqueMax_Nm       : REAL := 4500.0;            (* Maximum Uncoiler Forward Threading / Jogging Torque [Nm] *)
    rBridleSpeedMin_m_min       : REAL := 0.0;               (* Minimum Allowable Bridle Strip Velocity [m/min] *)
    rBridleSpeedMax_m_min       : REAL := 125.0;             (* Maximum Nameplate Bridle Strip Velocity [m/min] *)
    rShearTorqueMin_Nm          : REAL := -4800.0;           (* Rotary Shear Servo Maximum Dynamic Braking Torque [Nm] *)
    rShearTorqueMax_Nm          : REAL := 4800.0;            (* Rotary Shear Servo Maximum Peak Cutting Torque [Nm] *)
    rStackerAccelMin_m_s2       : REAL := -8.5;              (* Stacker Vacuum Conveyor Maximum Deceleration Rate [m/s2] *)
    rStackerAccelMax_m_s2       : REAL := 8.5;               (* Stacker Vacuum Conveyor Maximum Acceleration Rate [m/s2] *)
    
    (* ================================================================================================================ *)
    (* SECTION 2: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING STRUCTURES & TIMERS                                *)
    (* ================================================================================================================ *)
    (* Strip Velocity Voting (Laser Doppler Velocimeters LDV 1, 2, 3) *)
    rSpeed_Voted_m_min          : REAL := 0.0;
    bSpeed_SensorFault_1        : BOOL := FALSE;
    bSpeed_SensorFault_2        : BOOL := FALSE;
    bSpeed_SensorFault_3        : BOOL := FALSE;
    rSpeed_DiscrepancyTimer_1_s : REAL := 0.0;
    rSpeed_DiscrepancyTimer_2_s : REAL := 0.0;
    rSpeed_DiscrepancyTimer_3_s : REAL := 0.0;
    rSpeed_DiscrepancyTol_m_min : REAL := 2.50;              (* Velocity Channel Discrepancy Tolerance Threshold [m/min] *)
    rSpeed_DiscrepancyTripTime_s: REAL := 0.120;             (* Maximum Allowable Discrepancy Dwell Persistence Time [s] *)
    
    (* Master Line Incremental Encoder Voting (Encoders A, B, C) *)
    rEncoder_Voted_mm           : REAL := 0.0;
    bEncoder_SensorFault_A      : BOOL := FALSE;
    bEncoder_SensorFault_B      : BOOL := FALSE;
    bEncoder_SensorFault_C      : BOOL := FALSE;
    rEncoder_DiscrepancyTimer_A_s:REAL := 0.0;
    rEncoder_DiscrepancyTimer_B_s:REAL := 0.0;
    rEncoder_DiscrepancyTimer_C_s:REAL := 0.0;
    rEncoder_DiscrepancyTol_mm  : REAL := 0.65;              (* Linear Position Encoder Discrepancy Tolerance [mm] *)
    rEncoder_DiscrepancyTripTime_s:REAL:= 0.080;             (* Encoder Discrepancy Persistence Trip Threshold [s] *)
    
    (* Inter-Stand Strip Tensile Force Voting (Load Cells 1, 2, 3) *)
    rTension_Voted_kN           : REAL := 0.0;
    bTension_SensorFault_1      : BOOL := FALSE;
    bTension_SensorFault_2      : BOOL := FALSE;
    bTension_SensorFault_3      : BOOL := FALSE;
    rTension_DiscrepancyTimer_1_s:REAL:= 0.0;
    rTension_DiscrepancyTimer_2_s:REAL:= 0.0;
    rTension_DiscrepancyTimer_3_s:REAL:= 0.0;
    rTension_DiscrepancyTol_kN  : REAL := 0.45;              (* Web Tension Load Cell Discrepancy Tolerance [kN] *)
    rTension_DiscrepancyTripTime_s:REAL:= 0.150;             (* Load Cell Discrepancy Persistence Trip Threshold [s] *)
    
    (* ================================================================================================================ *)
    (* SECTION 3: UNCOILER COIL RADIUS TRACKING & VARIABLE INERTIA PHYSICS MODEL                                         *)
    (* ================================================================================================================ *)
    rCoilRadius_Calc_m          : REAL := 0.500;             (* Estimated Instantaneous Coil Physical Outer Radius [m] *)
    rCoilRadiusInitial_m        : REAL := 0.850;             (* Calibrated Starting Coil Radius at Loading [m] *)
    rMandrelRadiusCore_m        : REAL := 0.254;             (* Mandrel Core Base Radius [m] *)
    rSteelDensity_kg_m3         : REAL := 7850.0;            (* Carbon Steel Volumetric Mass Density [kg/m3] *)
    rStripLengthUncoiled_m      : REAL := 0.0;               (* Cumulative Linear Length Unwound From Master Coil [m] *)
    rCoilMassCurrent_kg         : REAL := 15000.0;           (* Instantaneous Total Payoff Coil Mass [kg] *)
    rMandrelBaseInertia_kgm2    : REAL := 145.0;             (* Bare Mandrel Shaft and Bearing Mass Moment of Inertia [kg*m2] *)
    rCoilInertiaCurrent_kgm2    : REAL := 1250.0;            (* Total Combined Moment of Inertia of Reel and Steel [kg*m2] *)
    rUncoilerAngularVelocity_rad_s: REAL := 0.0;             (* Calculated Reel Shaft Angular Velocity [rad/s] *)
    rUncoilerAngularAccel_rad_s2: REAL := 0.0;               (* Payoff Reel Angular Acceleration Rate [rad/s2] *)
    rUncoilerTensionTorque_Nm   : REAL := 0.0;               (* Pure Strip Back-Tension Static Torque Component [Nm] *)
    rUncoilerInertiaTorque_Nm   : REAL := 0.0;               (* Dynamic Acceleration / Deceleration Torque Compensation [Nm] *)
    rUncoilerFrictionTorque_Nm  : REAL := 0.0;               (* Bearing Viscous Drag and Seal Mechanical Loss Torque [Nm] *)
    rUncoilerBearingViscousCoeff: REAL := 3.85;              (* Viscous Drag Proportionality Constant [N*m*s/rad] *)
    
    (* ================================================================================================================ *)
    (* SECTION 4: 5th-ORDER POLYNOMIAL ELECTRONIC CAM ROTARY FLYING SHEAR MOTION GENERATOR                              *)
    (* ================================================================================================================ *)
    rShearDrumRadius_m          : REAL := 0.300;             (* Rotary Flying Shear Cylindrical Drum Outer Radius [m] *)
    rShearDrumCircumference_m   : REAL := 1.8849556;         (* Drum Peripheral Circumference (2 * pi * r) [m] *)
    rTargetCutLength_m          : REAL := 2.000;             (* Scaled Target Sheet Cut Length [m] *)
    rShearBladeAngle_rad        : REAL := 0.0;               (* Instantaneous Angular Position of Cutting Blades [rad] *)
    rShearBladeAngleNormalized  : REAL := 0.0;               (* Drum Angle Modulo 2*pi [0 .. 2*pi] [rad] *)
    rShearAngularSpeed_rad_s    : REAL := 0.0;               (* Drum Angular Velocity [rad/s] *)
    rShearBladeLinearSpeed_m_s  : REAL := 0.0;               (* Blade Tip Tangential Linear Cutting Velocity [m/s] *)
    rWebLinearSpeed_m_s         : REAL := 0.0;               (* Process Web Linear Velocity [m/s] *)
    
    (* 5th-Order Cam Polynomial Coordinates: s(tau) = 10*tau^3 - 15*tau^4 + 6*tau^5 *)
    rCamNormTau                 : REAL := 0.0;               (* Normalized Non-Dimensional Time tau in [0.0 .. 1.0] [-] *)
    rCamPoly_Pos                : REAL := 0.0;               (* Normalized Cam Evaluated Position s(tau) [-] *)
    rCamPoly_Vel                : REAL := 0.0;               (* Normalized Cam Evaluated Velocity ds/dtau [-] *)
    rCamPoly_Acc                : REAL := 0.0;               (* Normalized Cam Evaluated Acceleration d2s/dtau2 [-] *)
    
    rCamCutWindowAngleWidth_rad : REAL := 0.1745329;         (* Synchronous Cut Window Angle Arc (10.0 deg) [rad] *)
    rCamCutCenterAngle_rad      : REAL := 3.14159265;        (* Center Cut Penetration Point at 180.0 deg Bottom Dead Center [rad] *)
    bInShearCutWindow           : BOOL := FALSE;             (* Flying Shear Blade Currently Inside Cut Collision Zone [-] *)
    rShearCamPhaseError_rad     : REAL := 0.0;               (* Radial Synchronization Deviation from Ideal Electronic Cam [rad] *)
    rShearArcLinearError_mm     : REAL := 0.0;               (* Peripheral Blade-to-Strip Tracking Error [mm] *)
    
    rCamAccelAngle_rad          : REAL := 1.0471975;         (* Angular Travel Allocated for Drum Acceleration (60.0 deg) [rad] *)
    rCamDecelAngle_rad          : REAL := 1.0471975;         (* Angular Travel Allocated for Drum Deceleration (60.0 deg) [rad] *)
    rCamDwellAngle_rad          : REAL := 0.8726646;         (* Drum Parking / Dwell Waiting Angle for Oversized Sheets [rad] *)
    rCamExecutionPhase          : INT := 0;                  (* Sub-Phase: 0=Park/Dwell, 1=Accel, 2=SyncCut, 3=Decel *)
    
    (* ================================================================================================================ *)
    (* SECTION 5: SAVITZKY-GOLAY 5-POINT NUMERICAL DIFFERENTIATION & FILTERING HISTORIES                                 *)
    (* ================================================================================================================ *)
    bufSpeedHistory_m_s         : ARRAY[0..4] OF REAL;       (* Historical Ring Buffer for Strip Velocity [m/s] *)
    bufTensionHistory_kN        : ARRAY[0..4] OF REAL;       (* Historical Ring Buffer for Inter-Stand Web Tension [kN] *)
    bufEncoderHistory_mm        : ARRAY[0..4] OF REAL;       (* Historical Ring Buffer for Master Linear Encoders [mm] *)
    rFilteredStripAccel_m_s2    : REAL := 0.0;               (* Savitzky-Golay Smoothed Strip Acceleration [m/s2] *)
    rFilteredTensionRate_kN_s   : REAL := 0.0;               (* Savitzky-Golay Smoothed Tension Gradient dT/dt [kN/s] *)
    
    (* ================================================================================================================ *)
    (* SECTION 6: CLOSED-LOOP ELECTRO-HYDRAULIC EDGE POSITION CONTROL (EPC / CPC)                                       *)
    (* ================================================================================================================ *)
    rEdgeGuideKp                : REAL := 3.20;              (* Proportional Servo Gain [% command / mm error] *)
    rEdgeGuideKi                : REAL := 0.45;              (* Integral Servo Gain [% command / (mm * s)] *)
    rEdgeGuideKd                : REAL := 0.12;              (* Derivative Stabilizing Gain [% command * s / mm] *)
    rEdgeError_mm               : REAL := 0.0;               (* Measured Strip Edge Lateral Deviation [mm] *)
    rPrevEdgeError_mm           : REAL := 0.0;               (* Previous Cycle Edge Error for Finite Difference [mm] *)
    rEdgeIntegral_mm_s          : REAL := 0.0;               (* Cumulative Anti-Windup Integral Error Accumulator [mm*s] *)
    rEdgeDeriv_mm_s             : REAL := 0.0;               (* Rate of Change of Strip Lateral Camber [mm/s] *)
    rEdgeCylinderCmd_Raw        : REAL := 0.0;               (* Unbounded Output from PID Equation [%] *)
    
    (* ================================================================================================================ *)
    (* SECTION 7: HIGH-SPEED SLITTING HEAD & UPPER ARBOR PENETRATION DYNAMICS                                           *)
    (* ================================================================================================================ *)
    rSlitterTargetPlunge_mm     : REAL := 0.85;              (* Target Knife Overlap Penetration for Strip Gauge [mm] *)
    rSlitterPlungeError_mm      : REAL := 0.0;               (* Vertical Arbor Screw Positioning Deviation [mm] *)
    rSlitterShearForceEst_N     : REAL := 0.0;               (* Dynamic Calculated Metal Shearing Resistance Force [N] *)
    rSlitterKnifeRadius_m       : REAL := 0.125;             (* Rotary Circular Slitting Knife Disc Radius [m] *)
    rSlitterKnifeFriction_Nm    : REAL := 42.0;              (* Bearing and Polyurethane Stripper Ring Friction Drag [Nm] *)
    rSlitterCalculatedTorque_Nm : REAL := 0.0;               (* Commanded Torque for Slitter Arbor Motor Drive [Nm] *)
    
    (* ================================================================================================================ *)
    (* SECTION 8: HIGH-SPEED CUT LENGTH MEASUREMENT & SCRAP GATE DIVERT LOGIC                                            *)
    (* ================================================================================================================ *)
    rSheetLengthAccumulator_mm  : REAL := 0.0;               (* Discrete Strip Length Travel Count Between Knife Cuts [mm] *)
    rPrevEncoderPosition_mm     : REAL := 0.0;               (* Previous Cycle Encoder Value for Incremental Delta [mm] *)
    rIncrementalDeltaLength_mm  : REAL := 0.0;               (* Master Roll Displaced Linear Travel in Last Ts [mm] *)
    rLastCutMeasuredLength_mm   : REAL := 0.0;               (* Latched Length Value at Moment of Knife Penetration [mm] *)
    rLengthDeviationError_mm    : REAL := 0.0;               (* Absolute Length Discrepancy Against Target Setpoint [mm] *)
    rMaxCutTolerance_mm         : REAL := 0.200;             (* Quality Acceptance Upper Tolerance Boundary Window [mm] *)
    bRejectScrapCutCurrent      : BOOL := FALSE;             (* Boolean Defect Flag for Current Severed Sheet [-] *)
    rScrapGateDwellTimer_s      : REAL := 0.0;               (* Diverter Solenoid Valve Actuation Holding Timer [s] *)
    rScrapGateHoldDuration_s    : REAL := 0.450;             (* Active Pulse Time to Ensure Full Scrap Clearance [s] *)
    rCutStrokePulseTimer_s      : REAL := 0.0;               (* Cut Output Signal Pulse Strobe Dwell Timer [s] *)
    
    (* ================================================================================================================ *)
    (* SECTION 9: MASTER FINITE STATE MACHINE (FSM) SEQUENCER & STATE TIMERS                                             *)
    (* ================================================================================================================ *)
    iCurrentFsmState            : INT := 0;                  (* Active Sequential Finite State Machine State Number *)
    iPreviousFsmState           : INT := -1;                 (* State Index in Previous Execution Scan Cycle *)
    rStateDwellTimer_s          : REAL := 0.0;               (* Cumulative Elapsed Time Within Current State [s] *)
    bStateFirstScan             : BOOL := TRUE;              (* One-Shot Rising Edge Transition Marker for State Entry *)
    
    (* Master FSM State Enumeration Constant Definitions:
       0   : STATE_STANDBY_IDLE
       10  : STATE_COIL_CAR_LOADING
       20  : STATE_MANDREL_EXPAND_CLAMP
       30  : STATE_PEELER_THREADING_JOG
       40  : STATE_EDGE_GUIDE_CALIBRATE
       50  : STATE_SLITTER_KNIFE_ENGAGE
       60  : STATE_BRIDLE_DANCER_PRELOAD
       70  : STATE_LINE_RAMP_ACCELERATION
       80  : STATE_ROTARY_SHEAR_ELECTRONIC_CAM_SYNC
       90  : STATE_FLYING_CUT_EXECUTION
       100 : STATE_VACUUM_SHEET_CONVEY
       110 : STATE_SCRAP_GATE_DIVERT
       120 : STATE_MAGNETIC_STACKING
       130 : STATE_LINE_DECEL_TAIL_OUT
       999 : STATE_EMERGENCY_FAULT_TRIP
    *)
    
    (* ================================================================================================================ *)
    (* SECTION 10: ISA-18.2 MULTI-TIERED ALARM SETPOINTS, DEADBANDS & TRIP FLAGS                                         *)
    (* ================================================================================================================ *)
    (* Tension Trip Points *)
    rAlarmSet_Tension_LL_Collapse_kN : REAL := 0.80;         (* Web Breakage / Sudden Tension Drop Emergency Trip [kN] *)
    rAlarmSet_Tension_L_Slack_kN     : REAL := 2.50;         (* Web Low Tension Slack Warning Threshold [kN] *)
    rAlarmSet_Tension_H_Necking_kN   : REAL := 8.50;         (* Web High Tension Material Necking Warning [kN] *)
    rAlarmSet_Tension_HH_Surge_kN    : REAL := 11.20;        (* Web Rupture / Extreme Tension Surge Emergency Trip [kN] *)
    rAlarmSet_Tension_Deadband_kN    : REAL := 0.25;         (* Tension Alarm Reset Hysteresis Deadband [kN] *)
    
    (* Mandrel Expansion Pressure Trip Points *)
    rAlarmSet_MandrelPres_LL_bar     : REAL := 120.0;        (* Hydraulic Pressure Collapse Coil Throwing Hazard Trip [bar] *)
    rAlarmSet_MandrelPres_L_bar      : REAL := 155.0;        (* Mandrel Hydraulic Clamping Low Pressure Advisory [bar] *)
    rAlarmSet_MandrelPres_Deadband   : REAL := 5.0;          (* Mandrel Pressure Reset Hysteresis [bar] *)
    
    (* Rotary Flying Shear Synchronization Error Trip Points *)
    rAlarmSet_ShearSync_H_ArcErr_mm  : REAL := 0.85;         (* Shear Electronic Cam Tracking Error Warning [mm] *)
    rAlarmSet_ShearSync_HH_Trip_mm   : REAL := 2.60;         (* Blade Collision / Extreme Mechanical Clash E-Stop [mm] *)
    rAlarmSet_ShearSync_Deadband_mm  : REAL := 0.15;         (* Shear Tracking Error Reset Deadband [mm] *)
    
    (* Lateral Edge Guide Deviation Trip Points *)
    rAlarmSet_EdgeGuide_H_Dev_mm     : REAL := 45.0;         (* Strip Off-Center Telescoping Warning [mm] *)
    rAlarmSet_EdgeGuide_HH_Trip_mm   : REAL := 85.0;         (* Payoff Lateral Travel Limit Switch E-Stop [mm] *)
    
    (* Sheet Cut Length Quality Tolerance Trip Points *)
    rAlarmSet_CutLength_H_Dev_mm     : REAL := 0.200;        (* Out-of-Spec Sheet Length Scrap Divert Trigger [mm] *)
    rAlarmSet_CutLength_HH_Dev_mm    : REAL := 0.850;        (* Catastrophic Length Encoder Slippage Alarm [mm] *)
    
    (* ISA-18.2 Discrete Latched Alarm Flags *)
    bAlarm_TensionBreakage_LL        : BOOL := FALSE;
    bAlarm_TensionSlack_L            : BOOL := FALSE;
    bAlarm_TensionNecking_H          : BOOL := FALSE;
    bAlarm_TensionSurge_HH           : BOOL := FALSE;
    bAlarm_MandrelPressureDrop_LL    : BOOL := FALSE;
    bAlarm_MandrelPressureLow_L      : BOOL := FALSE;
    bAlarm_ShearCamSyncWarning_H     : BOOL := FALSE;
    bAlarm_ShearCamSyncClash_HH      : BOOL := FALSE;
    bAlarm_EdgeGuideExcursion_H      : BOOL := FALSE;
    bAlarm_EdgeGuideExcursion_HH     : BOOL := FALSE;
    bAlarm_CutLengthOutTolerance_H   : BOOL := FALSE;
    bAlarm_CutLengthRunaway_HH       : BOOL := FALSE;
    bAlarm_SpeedSensorDiscrepancy_H  : BOOL := FALSE;
    bAlarm_SpeedSensorLoss_HH        : BOOL := FALSE;
    bAlarm_EncoderDiscrepancy_H      : BOOL := FALSE;
    bAlarm_EncoderFailure_HH         : BOOL := FALSE;
    bAlarm_TensionSensorDiscrepancy_H: BOOL := FALSE;
    bAlarm_TensionSensorLoss_HH      : BOOL := FALSE;
    bAlarm_EmergencyStopActive_HH    : BOOL := FALSE;
    
    (* General Loop Iteration and Time Base Variables *)
    rCycleTime_s                     : REAL := 0.001;        (* Deterministic Periodic Task Execution Time Step Ts [s] *)
    rMathPi                          : REAL := 3.14159265;   (* Standard Mathematical Constant Pi [-] *)
    rMath2Pi                         : REAL := 6.28318531;   (* Standard Mathematical Constant 2*Pi [-] *)
END_VAR
"""
    code_parts.append(var_internal)
    
    # 6. Algorithmic body:
    # PHASE 0: Deterministic State Space & MPC Matrix Initialization
    phase0 = """
(* ==================================================================================================================== *)
(* PHASE 0: ONE-TIME DETERMINISTIC INITIALIZATION OF DISCRETE STATE-SPACE & MPC MATRICES                                *)
(* ==================================================================================================================== *)
IF NOT bMatricesInitialized THEN
    (* 1. Initialize Discrete State-Space System Matrix A (8x8) Discretized at Ts = 0.001 s *)
    (* State Vector: [1: R_coil_err, 2: w_uncoil, 3: y_dancer, 4: Ten_web, 5: th_shear, 6: w_shear, 7: e_length, 8: v_stk] *)
    matA[1,1] := 0.999850; matA[1,2] := -0.000015; matA[1,3] := 0.000000; matA[1,4] := 0.000000; matA[1,5] := 0.000000; matA[1,6] := 0.000000; matA[1,7] := 0.000000; matA[1,8] := 0.000000;
    matA[2,1] := 0.000120; matA[2,2] := 0.997200;  matA[2,3] := 0.000450; matA[2,4] := -0.000085;matA[2,5] := 0.000000; matA[2,6] := 0.000000; matA[2,7] := 0.000000; matA[2,8] := 0.000000;
    matA[3,1] := 0.000000; matA[3,2] := 0.000350;  matA[3,3] := 0.994500; matA[3,4] := -0.000120;matA[3,5] := 0.000000; matA[3,6] := 0.000000; matA[3,7] := 0.000000; matA[3,8] := 0.000000;
    matA[4,1] := 0.000000; matA[4,2] := 0.012500;  matA[4,3] := 0.085000; matA[4,4] := 0.988500; matA[4,5] := 0.000000; matA[4,6] := 0.000000; matA[4,7] := 0.000000; matA[4,8] := 0.000000;
    matA[5,1] := 0.000000; matA[5,2] := 0.000000;  matA[5,3] := 0.000000; matA[5,4] := 0.000000; matA[5,5] := 1.000000; matA[5,6] := 0.001000; matA[5,7] := 0.000000; matA[5,8] := 0.000000;
    matA[6,1] := 0.000000; matA[6,2] := 0.000000;  matA[6,3] := 0.000000; matA[6,4] := 0.000000; matA[6,5] := -0.00250; matA[6,6] := 0.996500; matA[6,7] := 0.000000; matA[6,8] := 0.000000;
    matA[7,1] := 0.000000; matA[7,2] := 0.000000;  matA[7,3] := 0.000000; matA[7,4] := 0.000000; matA[7,5] := 0.000300; matA[7,6] := 0.000000; matA[7,7] := 1.000000; matA[7,8] := 0.000000;
    matA[8,1] := 0.000000; matA[8,2] := 0.000000;  matA[8,3] := 0.000000; matA[8,4] := 0.000000; matA[8,5] := 0.000000; matA[8,6] := 0.000000; matA[8,7] := 0.000000; matA[8,8] := 0.998200;

    (* 2. Initialize Discrete Control Input Matrix B (8x4) *)
    (* Inputs: [1: tau_uncoil [Nm], 2: v_bridle [m/min], 3: tau_shear [Nm], 4: a_stacker [m/s2]] *)
    matB[1,1] := 0.000000; matB[1,2] := -0.000010; matB[1,3] := 0.000000; matB[1,4] := 0.000000;
    matB[2,1] := 0.000850; matB[2,2] := 0.000120;  matB[2,3] := 0.000000; matB[2,4] := 0.000000;
    matB[3,1] := 0.000000; matB[3,2] := -0.000450; matB[3,3] := 0.000000; matB[3,4] := 0.000000;
    matB[4,1] := -0.00150; matB[4,2] := 0.035000;  matB[4,3] := 0.000000; matB[4,4] := 0.000000;
    matB[5,1] := 0.000000; matB[5,2] := 0.000000;  matB[5,3] := 0.000005; matB[5,4] := 0.000000;
    matB[6,1] := 0.000000; matB[6,2] := 0.000000;  matB[6,3] := 0.002200; matB[6,4] := 0.000000;
    matB[7,1] := 0.000000; matB[7,2] := 0.000000;  matB[7,3] := -0.00002; matB[7,4] := 0.000000;
    matB[8,1] := 0.000000; matB[8,2] := 0.000000;  matB[8,3] := 0.000000; matB[8,4] := 0.001000;

    (* 3. Initialize Measurement Output Matrix C (8x8 Identity) *)
    FOR iMpcRow := 1 TO 8 DO
        FOR iMpcCol := 1 TO 8 DO
            IF iMpcRow = iMpcCol THEN
                matC[iMpcRow, iMpcCol] := 1.0;
            ELSE
                matC[iMpcRow, iMpcCol] := 0.0;
            END_IF;
        END_FOR;
    END_FOR;

    (* 4. Initialize Direct Feedthrough Matrix D (8x4 Zeros) *)
    FOR iMpcRow := 1 TO 8 DO
        FOR iMpcCol := 1 TO 4 DO
            matD[iMpcRow, iMpcCol] := 0.0;
        END_FOR;
    END_FOR;

    (* 5. Initialize Discrete Luenberger Observer Gain Matrix L (8x8) *)
    matL[1,1] := 0.1250; matL[1,2] := 0.0000; matL[1,3] := 0.0000; matL[1,4] := 0.0000; matL[1,5] := 0.0000; matL[1,6] := 0.0000; matL[1,7] := 0.0000; matL[1,8] := 0.0000;
    matL[2,1] := 0.0020; matL[2,2] := 0.1850; matL[2,3] := 0.0015; matL[2,4] := 0.0008; matL[2,5] := 0.0000; matL[2,6] := 0.0000; matL[2,7] := 0.0000; matL[2,8] := 0.0000;
    matL[3,1] := 0.0000; matL[3,2] := 0.0012; matL[3,3] := 0.1550; matL[3,4] := 0.0025; matL[3,5] := 0.0000; matL[3,6] := 0.0000; matL[3,7] := 0.0000; matL[3,8] := 0.0000;
    matL[4,1] := 0.0000; matL[4,2] := 0.0045; matL[4,3] := 0.0150; matL[4,4] := 0.2200; matL[4,5] := 0.0000; matL[4,6] := 0.0000; matL[4,7] := 0.0000; matL[4,8] := 0.0000;
    matL[5,1] := 0.0000; matL[5,2] := 0.0000; matL[5,3] := 0.0000; matL[5,4] := 0.0000; matL[5,5] := 0.2450; matL[5,6] := 0.0035; matL[5,7] := 0.0000; matL[5,8] := 0.0000;
    matL[6,1] := 0.0000; matL[6,2] := 0.0000; matL[6,3] := 0.0000; matL[6,4] := 0.0000; matL[6,5] := 0.0080; matL[6,6] := 0.2100; matL[6,7] := 0.0000; matL[6,8] := 0.0000;
    matL[7,1] := 0.0000; matL[7,2] := 0.0000; matL[7,3] := 0.0000; matL[7,4] := 0.0000; matL[7,5] := 0.0000; matL[7,6] := 0.0000; matL[7,7] := 0.1900; matL[7,8] := 0.0000;
    matL[8,1] := 0.0000; matL[8,2] := 0.0000; matL[8,3] := 0.0000; matL[8,4] := 0.0000; matL[8,5] := 0.0000; matL[8,6] := 0.0000; matL[8,7] := 0.0000; matL[8,8] := 0.1650;

    (* 6. Initialize MPC State Penalty Matrix Q (8x8 Diagonal) *)
    FOR iMpcRow := 1 TO 8 DO
        FOR iMpcCol := 1 TO 8 DO
            matQ[iMpcRow, iMpcCol] := 0.0;
        END_FOR;
    END_FOR;
    matQ[1,1] := 15.0;   (* Penalty on coil radius estimation error *)
    matQ[2,2] := 8.5;    (* Penalty on payoff reel speed deviation *)
    matQ[3,3] := 25.0;   (* Penalty on dancer position displacement *)
    matQ[4,4] := 85.0;   (* High penalty on web tension error (prevents buckling and necking) *)
    matQ[5,5] := 120.0;  (* Extreme penalty on flying shear cam synchronous angle error *)
    matQ[6,6] := 45.0;   (* Penalty on flying shear blade angular velocity deviation *)
    matQ[7,7] := 180.0;  (* Maximum penalty on cut sheet length deviation *)
    matQ[8,8] := 12.0;   (* Penalty on stacker conveyor speed deviation *)

    (* 7. Initialize MPC Actuator Rate Penalty Matrix R (4x4 Diagonal) *)
    FOR iMpcRow := 1 TO 4 DO
        FOR iMpcCol := 1 TO 4 DO
            matR[iMpcRow, iMpcCol] := 0.0;
        END_FOR;
    END_FOR;
    matR[1,1] := 0.0045; (* Penalty on uncoiler back-torque rate of change *)
    matR[2,2] := 0.0120; (* Penalty on entry bridle acceleration rate *)
    matR[3,3] := 0.0080; (* Penalty on shear motor torque rate of change *)
    matR[4,4] := 0.0150; (* Penalty on stacker belt acceleration jerk *)

    (* 8. Initialize Terminal Riccati Cost Matrix P (8x8 Diagonal) *)
    FOR iMpcRow := 1 TO 8 DO
        FOR iMpcCol := 1 TO 8 DO
            matP[iMpcRow, iMpcCol] := 0.0;
        END_FOR;
    END_FOR;
    matP[1,1] := 35.0;
    matP[2,2] := 20.0;
    matP[3,3] := 60.0;
    matP[4,4] := 220.0;
    matP[5,5] := 310.0;
    matP[6,6] := 110.0;
    matP[7,7] := 450.0;
    matP[8,8] := 28.0;

    (* 9. Initialize Approximated Cost Hessian Matrix H (4x4) *)
    matHessian[1,1] := 2.500; matHessian[1,2] := 0.120; matHessian[1,3] := 0.000; matHessian[1,4] := 0.000;
    matHessian[2,1] := 0.120; matHessian[2,2] := 3.850; matHessian[2,3] := 0.000; matHessian[2,4] := 0.000;
    matHessian[3,1] := 0.000; matHessian[3,2] := 0.000; matHessian[3,3] := 4.200; matHessian[3,4] := 0.000;
    matHessian[4,1] := 0.000; matHessian[4,2] := 0.000; matHessian[4,3] := 0.000; matHessian[4,4] := 1.850;

    bMatricesInitialized := TRUE;
END_IF;
"""
    code_parts.append(phase0)
    
    # PHASE 1: 2oo3 TMR Sensor Voting & Discrepancy Arbitration
    phase1 = """
(* ==================================================================================================================== *)
(* PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING & DISCREPANCY ARBITRATION                                *)
(* ==================================================================================================================== *)

(* --- SUB-PHASE 1.1: 2oo3 LASER DOPPLER VELOCIMETER (LDV) STRIP VELOCITY VOTING --- *)
(* Check Channel Discrepancies Against Each Other *)
IF ABS(rSpeedSensor_LDV1_m_min - rSpeedSensor_LDV2_m_min) > rSpeedDiscrepancyTol_m_min THEN
    IF ABS(rSpeedSensor_LDV1_m_min - rSpeedSensor_LDV3_m_min) > rSpeedDiscrepancyTol_m_min THEN
        rSpeed_DiscrepancyTimer_1_s := rSpeed_DiscrepancyTimer_1_s + rCycleTime_s;
    ELSE
        rSpeed_DiscrepancyTimer_2_s := rSpeed_DiscrepancyTimer_2_s + rCycleTime_s;
    END_IF;
ELSE
    rSpeed_DiscrepancyTimer_1_s := MAX(0.0, rSpeed_DiscrepancyTimer_1_s - rCycleTime_s * 2.0);
    rSpeed_DiscrepancyTimer_2_s := MAX(0.0, rSpeed_DiscrepancyTimer_2_s - rCycleTime_s * 2.0);
END_IF;

IF ABS(rSpeedSensor_LDV3_m_min - rSpeedSensor_LDV1_m_min) > rSpeedDiscrepancyTol_m_min AND
   ABS(rSpeedSensor_LDV3_m_min - rSpeedSensor_LDV2_m_min) > rSpeedDiscrepancyTol_m_min THEN
    rSpeed_DiscrepancyTimer_3_s := rSpeed_DiscrepancyTimer_3_s + rCycleTime_s;
ELSE
    rSpeed_DiscrepancyTimer_3_s := MAX(0.0, rSpeed_DiscrepancyTimer_3_s - rCycleTime_s * 2.0);
END_IF;

(* Latch Individual Sensor Failure Flags on Persistent Discrepancy *)
IF rSpeed_DiscrepancyTimer_1_s > rSpeed_DiscrepancyTripTime_s THEN
    bSpeed_SensorFault_1 := TRUE;
END_IF;
IF rSpeed_DiscrepancyTimer_2_s > rSpeed_DiscrepancyTripTime_s THEN
    bSpeed_SensorFault_2 := TRUE;
END_IF;
IF rSpeed_DiscrepancyTimer_3_s > rSpeed_DiscrepancyTripTime_s THEN
    bSpeed_SensorFault_3 := TRUE;
END_IF;

(* Mid-Value Median Selection Voting Logic *)
IF NOT bSpeed_SensorFault_1 AND NOT bSpeed_SensorFault_2 AND NOT bSpeed_SensorFault_3 THEN
    (* All 3 Channels Healthy: Standard 2oo3 Mid-Value Selection *)
    IF (rSpeedSensor_LDV1_m_min >= rSpeedSensor_LDV2_m_min AND rSpeedSensor_LDV1_m_min <= rSpeedSensor_LDV3_m_min) OR
       (rSpeedSensor_LDV1_m_min <= rSpeedSensor_LDV2_m_min AND rSpeedSensor_LDV1_m_min >= rSpeedSensor_LDV3_m_min) THEN
        rSpeed_Voted_m_min := rSpeedSensor_LDV1_m_min;
    ELSIF (rSpeedSensor_LDV2_m_min >= rSpeedSensor_LDV1_m_min AND rSpeedSensor_LDV2_m_min <= rSpeedSensor_LDV3_m_min) OR
          (rSpeedSensor_LDV2_m_min <= rSpeedSensor_LDV1_m_min AND rSpeedSensor_LDV2_m_min >= rSpeedSensor_LDV3_m_min) THEN
        rSpeed_Voted_m_min := rSpeedSensor_LDV2_m_min;
    ELSE
        rSpeed_Voted_m_min := rSpeedSensor_LDV3_m_min;
    END_IF;
    bAlarm_SpeedSensorDiscrepancy_H := FALSE;
    bAlarm_SpeedSensorLoss_HH := FALSE;
ELSIF bSpeed_SensorFault_1 AND NOT bSpeed_SensorFault_2 AND NOT bSpeed_SensorFault_3 THEN
    (* Ch 1 Faulted: Degrade to Average of Ch 2 & Ch 3 *)
    rSpeed_Voted_m_min := (rSpeedSensor_LDV2_m_min + rSpeedSensor_LDV3_m_min) * 0.5;
    bAlarm_SpeedSensorDiscrepancy_H := TRUE;
    bAlarm_SpeedSensorLoss_HH := FALSE;
ELSIF bSpeed_SensorFault_2 AND NOT bSpeed_SensorFault_1 AND NOT bSpeed_SensorFault_3 THEN
    (* Ch 2 Faulted: Degrade to Average of Ch 1 & Ch 3 *)
    rSpeed_Voted_m_min := (rSpeedSensor_LDV1_m_min + rSpeedSensor_LDV3_m_min) * 0.5;
    bAlarm_SpeedSensorDiscrepancy_H := TRUE;
    bAlarm_SpeedSensorLoss_HH := FALSE;
ELSIF bSpeed_SensorFault_3 AND NOT bSpeed_SensorFault_1 AND NOT bSpeed_SensorFault_2 THEN
    (* Ch 3 Faulted: Degrade to Average of Ch 1 & Ch 2 *)
    rSpeed_Voted_m_min := (rSpeedSensor_LDV1_m_min + rSpeedSensor_LDV2_m_min) * 0.5;
    bAlarm_SpeedSensorDiscrepancy_H := TRUE;
    bAlarm_SpeedSensorLoss_HH := FALSE;
ELSE
    (* Multiple Sensors Faulted: Loss of TMR Redundancy Safety Trip *)
    rSpeed_Voted_m_min := 0.0;
    bAlarm_SpeedSensorDiscrepancy_H := TRUE;
    bAlarm_SpeedSensorLoss_HH := TRUE;
END_IF;

(* --- SUB-PHASE 1.2: 2oo3 MASTER MEASURING ROLL OPTICAL ENCODER VOTING --- *)
IF ABS(rEncoder_LineMaster_A_mm - rEncoder_LineMaster_B_mm) > rEncoder_DiscrepancyTol_mm THEN
    IF ABS(rEncoder_LineMaster_A_mm - rEncoder_LineMaster_C_mm) > rEncoder_DiscrepancyTol_mm THEN
        rEncoder_DiscrepancyTimer_A_s := rEncoder_DiscrepancyTimer_A_s + rCycleTime_s;
    ELSE
        rEncoder_DiscrepancyTimer_B_s := rEncoder_DiscrepancyTimer_B_s + rCycleTime_s;
    END_IF;
ELSE
    rEncoder_DiscrepancyTimer_A_s := MAX(0.0, rEncoder_DiscrepancyTimer_A_s - rCycleTime_s * 2.0);
    rEncoder_DiscrepancyTimer_B_s := MAX(0.0, rEncoder_DiscrepancyTimer_B_s - rCycleTime_s * 2.0);
END_IF;

IF ABS(rEncoder_LineMaster_C_mm - rEncoder_LineMaster_A_mm) > rEncoder_DiscrepancyTol_mm AND
   ABS(rEncoder_LineMaster_C_mm - rEncoder_LineMaster_B_mm) > rEncoder_DiscrepancyTol_mm THEN
    rEncoder_DiscrepancyTimer_C_s := rEncoder_DiscrepancyTimer_C_s + rCycleTime_s;
ELSE
    rEncoder_DiscrepancyTimer_C_s := MAX(0.0, rEncoder_DiscrepancyTimer_C_s - rCycleTime_s * 2.0);
END_IF;

IF rEncoder_DiscrepancyTimer_A_s > rEncoder_DiscrepancyTripTime_s THEN bEncoder_SensorFault_A := TRUE; END_IF;
IF rEncoder_DiscrepancyTimer_B_s > rEncoder_DiscrepancyTripTime_s THEN bEncoder_SensorFault_B := TRUE; END_IF;
IF rEncoder_DiscrepancyTimer_C_s > rEncoder_DiscrepancyTripTime_s THEN bEncoder_SensorFault_C := TRUE; END_IF;

IF NOT bEncoder_SensorFault_A AND NOT bEncoder_SensorFault_B AND NOT bEncoder_SensorFault_C THEN
    IF (rEncoder_LineMaster_A_mm >= rEncoder_LineMaster_B_mm AND rEncoder_LineMaster_A_mm <= rEncoder_LineMaster_C_mm) OR
       (rEncoder_LineMaster_A_mm <= rEncoder_LineMaster_B_mm AND rEncoder_LineMaster_A_mm >= rEncoder_LineMaster_C_mm) THEN
        rEncoder_Voted_mm := rEncoder_LineMaster_A_mm;
    ELSIF (rEncoder_LineMaster_B_mm >= rEncoder_LineMaster_A_mm AND rEncoder_LineMaster_B_mm <= rEncoder_LineMaster_C_mm) OR
          (rEncoder_LineMaster_B_mm <= rEncoder_LineMaster_A_mm AND rEncoder_LineMaster_B_mm >= rEncoder_LineMaster_C_mm) THEN
        rEncoder_Voted_mm := rEncoder_LineMaster_B_mm;
    ELSE
        rEncoder_Voted_mm := rEncoder_LineMaster_C_mm;
    END_IF;
    bAlarm_EncoderDiscrepancy_H := FALSE;
    bAlarm_EncoderFailure_HH := FALSE;
ELSIF bEncoder_SensorFault_A AND NOT bEncoder_SensorFault_B AND NOT bEncoder_SensorFault_C THEN
    rEncoder_Voted_mm := (rEncoder_LineMaster_B_mm + rEncoder_LineMaster_C_mm) * 0.5;
    bAlarm_EncoderDiscrepancy_H := TRUE;
    bAlarm_EncoderFailure_HH := FALSE;
ELSIF bEncoder_SensorFault_B AND NOT bEncoder_SensorFault_A AND NOT bEncoder_SensorFault_C THEN
    rEncoder_Voted_mm := (rEncoder_LineMaster_A_mm + rEncoder_LineMaster_C_mm) * 0.5;
    bAlarm_EncoderDiscrepancy_H := TRUE;
    bAlarm_EncoderFailure_HH := FALSE;
ELSIF bEncoder_SensorFault_C AND NOT bEncoder_SensorFault_A AND NOT bEncoder_SensorFault_B THEN
    rEncoder_Voted_mm := (rEncoder_LineMaster_A_mm + rEncoder_LineMaster_B_mm) * 0.5;
    bAlarm_EncoderDiscrepancy_H := TRUE;
    bAlarm_EncoderFailure_HH := FALSE;
ELSE
    rEncoder_Voted_mm := rEncoder_LineMaster_A_mm;
    bAlarm_EncoderDiscrepancy_H := TRUE;
    bAlarm_EncoderFailure_HH := TRUE;
END_IF;

(* --- SUB-PHASE 1.3: 2oo3 INTER-STAND STRIP TENSILE LOAD CELL VOTING --- *)
IF ABS(rTensionLoadCell_1_kN - rTensionLoadCell_2_kN) > rTension_DiscrepancyTol_kN THEN
    IF ABS(rTensionLoadCell_1_kN - rTensionLoadCell_3_kN) > rTension_DiscrepancyTol_kN THEN
        rTension_DiscrepancyTimer_1_s := rTension_DiscrepancyTimer_1_s + rCycleTime_s;
    ELSE
        rTension_DiscrepancyTimer_2_s := rTension_DiscrepancyTimer_2_s + rCycleTime_s;
    END_IF;
ELSE
    rTension_DiscrepancyTimer_1_s := MAX(0.0, rTension_DiscrepancyTimer_1_s - rCycleTime_s * 2.0);
    rTension_DiscrepancyTimer_2_s := MAX(0.0, rTension_DiscrepancyTimer_2_s - rCycleTime_s * 2.0);
END_IF;

IF ABS(rTensionLoadCell_3_kN - rTensionLoadCell_1_kN) > rTension_DiscrepancyTol_kN AND
   ABS(rTensionLoadCell_3_kN - rTensionLoadCell_2_kN) > rTension_DiscrepancyTol_kN THEN
    rTension_DiscrepancyTimer_3_s := rTension_DiscrepancyTimer_3_s + rCycleTime_s;
ELSE
    rTension_DiscrepancyTimer_3_s := MAX(0.0, rTension_DiscrepancyTimer_3_s - rCycleTime_s * 2.0);
END_IF;

IF rTension_DiscrepancyTimer_1_s > rTension_DiscrepancyTripTime_s THEN bTension_SensorFault_1 := TRUE; END_IF;
IF rTension_DiscrepancyTimer_2_s > rTension_DiscrepancyTripTime_s THEN bTension_SensorFault_2 := TRUE; END_IF;
IF rTension_DiscrepancyTimer_3_s > rTension_DiscrepancyTripTime_s THEN bTension_SensorFault_3 := TRUE; END_IF;

IF NOT bTension_SensorFault_1 AND NOT bTension_SensorFault_2 AND NOT bTension_SensorFault_3 THEN
    IF (rTensionLoadCell_1_kN >= rTensionLoadCell_2_kN AND rTensionLoadCell_1_kN <= rTensionLoadCell_3_kN) OR
       (rTensionLoadCell_1_kN <= rTensionLoadCell_2_kN AND rTensionLoadCell_1_kN >= rTensionLoadCell_3_kN) THEN
        rTension_Voted_kN := rTensionLoadCell_1_kN;
    ELSIF (rTensionLoadCell_2_kN >= rTensionLoadCell_1_kN AND rTensionLoadCell_2_kN <= rTensionLoadCell_3_kN) OR
          (rTensionLoadCell_2_kN <= rTensionLoadCell_1_kN AND rTensionLoadCell_2_kN >= rTensionLoadCell_3_kN) THEN
        rTension_Voted_kN := rTensionLoadCell_2_kN;
    ELSE
        rTension_Voted_kN := rTensionLoadCell_3_kN;
    END_IF;
    bAlarm_TensionSensorDiscrepancy_H := FALSE;
    bAlarm_TensionSensorLoss_HH := FALSE;
ELSIF bTension_SensorFault_1 AND NOT bTension_SensorFault_2 AND NOT bTension_SensorFault_3 THEN
    rTension_Voted_kN := (rTensionLoadCell_2_kN + rTensionLoadCell_3_kN) * 0.5;
    bAlarm_TensionSensorDiscrepancy_H := TRUE;
    bAlarm_TensionSensorLoss_HH := FALSE;
ELSIF bTension_SensorFault_2 AND NOT bTension_SensorFault_1 AND NOT bTension_SensorFault_3 THEN
    rTension_Voted_kN := (rTensionLoadCell_1_kN + rTensionLoadCell_3_kN) * 0.5;
    bAlarm_TensionSensorDiscrepancy_H := TRUE;
    bAlarm_TensionSensorLoss_HH := FALSE;
ELSIF bTension_SensorFault_3 AND NOT bTension_SensorFault_1 AND NOT bTension_SensorFault_2 THEN
    rTension_Voted_kN := (rTensionLoadCell_1_kN + rTensionLoadCell_2_kN) * 0.5;
    bAlarm_TensionSensorDiscrepancy_H := TRUE;
    bAlarm_TensionSensorLoss_HH := FALSE;
ELSE
    rTension_Voted_kN := 0.0;
    bAlarm_TensionSensorDiscrepancy_H := TRUE;
    bAlarm_TensionSensorLoss_HH := TRUE;
END_IF;

(* Map 2oo3 Arbitrated Values to Process Outputs *)
rActualStripSpeed_m_min := rSpeed_Voted_m_min;
rActualStripTension_kN  := rTension_Voted_kN;
rActualStripPosition_m  := rEncoder_Voted_mm / 1000.0;
rWebLinearSpeed_m_s     := rSpeed_Voted_m_min / 60.0;
"""
    code_parts.append(phase1)
    
    # PHASE 2: Savitzky-Golay Numerical Differentiation
    phase2 = """
(* ==================================================================================================================== *)
(* PHASE 2: SAVITZKY-GOLAY 5-POINT POLYNOMIAL NUMERICAL DIFFERENTIATION & DERIVATIVE ESTIMATION                        *)
(* ==================================================================================================================== *)
(* Shift Historical Sample Ring Buffers *)
bufSpeedHistory_m_s[4]  := bufSpeedHistory_m_s[3];
bufSpeedHistory_m_s[3]  := bufSpeedHistory_m_s[2];
bufSpeedHistory_m_s[2]  := bufSpeedHistory_m_s[1];
bufSpeedHistory_m_s[1]  := bufSpeedHistory_m_s[0];
bufSpeedHistory_m_s[0]  := rWebLinearSpeed_m_s;

bufTensionHistory_kN[4] := bufTensionHistory_kN[3];
bufTensionHistory_kN[3] := bufTensionHistory_kN[2];
bufTensionHistory_kN[2] := bufTensionHistory_kN[1];
bufTensionHistory_kN[1] := bufTensionHistory_kN[0];
bufTensionHistory_kN[0] := rTension_Voted_kN;

bufEncoderHistory_mm[4] := bufEncoderHistory_mm[3];
bufEncoderHistory_mm[3] := bufEncoderHistory_mm[2];
bufEncoderHistory_mm[2] := bufEncoderHistory_mm[1];
bufEncoderHistory_mm[1] := bufEncoderHistory_mm[0];
bufEncoderHistory_mm[0] := rEncoder_Voted_mm;

(* Savitzky-Golay 1st Derivative 5-Point Convolution Kernels *)
(* Formula: f'(x0) = (-2*f[k-2] - 1*f[k-1] + 0*f[k] + 1*f[k+1] + 2*f[k+2]) / (10 * Ts) *)
rFilteredStripAccel_m_s2 := (2.0 * bufSpeedHistory_m_s[0] +
                             1.0 * bufSpeedHistory_m_s[1] +
                             0.0 * bufSpeedHistory_m_s[2] -
                             1.0 * bufSpeedHistory_m_s[3] -
                             2.0 * bufSpeedHistory_m_s[4]) / (10.0 * rCycleTime_s);

rFilteredTensionRate_kN_s := (2.0 * bufTensionHistory_kN[0] +
                              1.0 * bufTensionHistory_kN[1] +
                              0.0 * bufTensionHistory_kN[2] -
                              1.0 * bufTensionHistory_kN[3] -
                              2.0 * bufTensionHistory_kN[4]) / (10.0 * rCycleTime_s);
"""
    code_parts.append(phase2)
    
    # PHASE 3: Uncoiler Coil Radius & Variable Inertia Physics
    phase3 = """
(* ==================================================================================================================== *)
(* PHASE 3: UNCOILER COIL RADIUS TRACKING & VARIABLE INERTIA DYNAMICS                                                  *)
(* ==================================================================================================================== *)
(* Initialize Coil Starting Dimensions Upon First Scan or New Coil Loading *)
IF rCoilRadiusInitial_m <= 0.254 THEN
    rCoilRadiusInitial_m := MAX(0.300, (rCoilOuterDiaInitial_mm * 0.0005));
    rCoilRadius_Calc_m := rCoilRadiusInitial_m;
    rStripLengthUncoiled_m := 0.0;
END_IF;

(* Continuous Web Travel Length Integration *)
rStripLengthUncoiled_m := rStripLengthUncoiled_m + (rWebLinearSpeed_m_s * rCycleTime_s);

(* Volumetric Kinematic Strip Equation for Outer Coil Radius R(t):
   V_coil(t) = pi * (R_init^2 - R(t)^2) * Width = Length * Width * Thickness
   => R(t) = SQRT(MAX(R_core^2, R_init^2 - (Thickness * Length / pi)))
*)
IF rStripThickness_mm > 0.05 AND rCoilRadiusInitial_m > 0.260 THEN
    rCoilRadius_Calc_m := SQRT(MAX((rMandrelCoreDia_mm * 0.0005) * (rMandrelCoreDia_mm * 0.0005),
                                   (rCoilRadiusInitial_m * rCoilRadiusInitial_m) -
                                   ((rStripThickness_mm * 0.001) * rStripLengthUncoiled_m / rMathPi)));
ELSE
    rCoilRadius_Calc_m := MAX(0.254, rCoilRadius_Calc_m);
END_IF;

rCurrentCoilRadius_mm := rCoilRadius_Calc_m * 1000.0;

(* Instantaneous Uncoiler Shaft Angular Velocity *)
IF rCoilRadius_Calc_m > 0.100 THEN
    rUncoilerAngularVelocity_rad_s := rWebLinearSpeed_m_s / rCoilRadius_Calc_m;
ELSE
    rUncoilerAngularVelocity_rad_s := 0.0;
END_IF;

(* Dynamic Coil Mass and Polar Moment of Inertia J(t):
   M_coil = pi * rho * Width * (R^2 - R_core^2)
   J_coil = 0.5 * M_coil * (R^2 + R_core^2)
*)
rCoilMassCurrent_kg := rMathPi * rSteelDensity_kg_m3 * (rStripWidth_mm * 0.001) *
                       MAX(0.0, (rCoilRadius_Calc_m * rCoilRadius_Calc_m) -
                                ((rMandrelCoreDia_mm * 0.0005) * (rMandrelCoreDia_mm * 0.0005)));

rCoilInertiaCurrent_kgm2 := rMandrelBaseInertia_kgm2 +
                            (0.5 * rCoilMassCurrent_kg *
                             ((rCoilRadius_Calc_m * rCoilRadius_Calc_m) +
                              ((rMandrelCoreDia_mm * 0.0005) * (rMandrelCoreDia_mm * 0.0005))));

(* Uncoiler Angular Acceleration: alpha = (a_web / R) - (v_web * dR_dt / R^2) *)
IF rCoilRadius_Calc_m > 0.100 THEN
    rUncoilerAngularAccel_rad_s2 := rFilteredStripAccel_m_s2 / rCoilRadius_Calc_m;
ELSE
    rUncoilerAngularAccel_rad_s2 := 0.0;
END_IF;

(* Feedforward Payoff Reel Back-Tension Braking Torque Components:
   tau_tension = -1.0 * T_target * R(t)  (Negative generates back-pull)
   tau_inertia = -1.0 * J(t) * alpha     (Compensates line acceleration/deceleration)
   tau_friction = -1.0 * b_bearing * omega (Friction naturally opposes rotation)
*)
rUncoilerTensionTorque_Nm  := -1.0 * (rTargetTension_kN * 1000.0) * rCoilRadius_Calc_m;
rUncoilerInertiaTorque_Nm  := -1.0 * rCoilInertiaCurrent_kgm2 * rUncoilerAngularAccel_rad_s2;
rUncoilerFrictionTorque_Nm := rUncoilerBearingViscousCoeff * rUncoilerAngularVelocity_rad_s;
"""
    code_parts.append(phase3)
    
    # PHASE 4: 5th-Order Electronic Cam Flying Shear
    phase4 = """
(* ==================================================================================================================== *)
(* PHASE 4: 5th-ORDER POLYNOMIAL ELECTRONIC CAM ROTARY FLYING SHEAR MOTION GENERATOR                                    *)
(* ==================================================================================================================== *)
rTargetCutLength_m := MAX(0.500, rTargetSheetLength_mm * 0.001);

(* Scale Resolver Angle to Radians [0.0 .. 2*pi] *)
rShearBladeAngle_rad := (rShearShaftAngle_deg * rMathPi) / 180.0;
WHILE rShearBladeAngle_rad >= rMath2Pi DO
    rShearBladeAngle_rad := rShearBladeAngle_rad - rMath2Pi;
END_WHILE;
WHILE rShearBladeAngle_rad < 0.0 DO
    rShearBladeAngle_rad := rShearBladeAngle_rad + rMath2Pi;
END_WHILE;
rShearBladeAngleNormalized := rShearBladeAngle_rad;

(* Instantaneous Blade Tangential Speed *)
rShearAngularSpeed_rad_s   := (rShearShaftVelocity_RPM * 2.0 * rMathPi) / 60.0;
rShearBladeLinearSpeed_m_s := rShearAngularSpeed_rad_s * rShearDrumRadius_m;

(* Synchronous Cutting Window: Blade Centered at 180.0 deg (Bottom Dead Center) *)
rCutWindowStartAngle_rad := rCamCutCenterAngle_rad - (rCamCutWindowAngleWidth_rad * 0.5);
rCutWindowEndAngle_rad   := rCamCutCenterAngle_rad + (rCamCutWindowAngleWidth_rad * 0.5);

IF rShearBladeAngleNormalized >= rCutWindowStartAngle_rad AND
   rShearBladeAngleNormalized <= rCutWindowEndAngle_rad THEN
    bInShearCutWindow := TRUE;
ELSE
    bInShearCutWindow := FALSE;
END_IF;

(* 5th-Order Electronic Cam Generation (Quintic Polynomial s(tau) = 10*tau^3 - 15*tau^4 + 6*tau^5):
   Provides zero boundary jerk (d3s/dtau3 = 0) at acceleration entry and cut synchronization.
*)
IF rTargetCutLength_m >= rShearDrumCircumference_m THEN
    (* Long Sheet Mode: Drum Accelerates, Cuts, Decelerates, and Dwells to wait for web *)
    IF rShearBladeAngleNormalized < (rCamCutCenterAngle_rad - rCamAccelAngle_rad) THEN
        (* Dwell / Parking Zone: Waiting for strip displacement trigger *)
        rCamExecutionPhase := 0;
        rCamNormTau := 0.0;
        rCamPoly_Pos := 0.0;
        rCamPoly_Vel := 0.0;
        rCamPoly_Acc := 0.0;
    ELSIF rShearBladeAngleNormalized >= (rCamCutCenterAngle_rad - rCamAccelAngle_rad) AND
          rShearBladeAngleNormalized < rCutWindowStartAngle_rad THEN
        (* Acceleration Cam Segment *)
        rCamExecutionPhase := 1;
        rCamNormTau := (rShearBladeAngleNormalized - (rCamCutCenterAngle_rad - rCamAccelAngle_rad)) /
                       MAX(0.001, (rCutWindowStartAngle_rad - (rCamCutCenterAngle_rad - rCamAccelAngle_rad)));
        rCamNormTau := LIMIT(0.0, rCamNormTau, 1.0);
        rCamPoly_Pos := (10.0 * rCamNormTau * rCamNormTau * rCamNormTau) -
                        (15.0 * rCamNormTau * rCamNormTau * rCamNormTau * rCamNormTau) +
                        (6.0  * rCamNormTau * rCamNormTau * rCamNormTau * rCamNormTau * rCamNormTau);
        rCamPoly_Vel := (30.0 * rCamNormTau * rCamNormTau) -
                        (60.0 * rCamNormTau * rCamNormTau * rCamNormTau) +
                        (30.0 * rCamNormTau * rCamNormTau * rCamNormTau * rCamNormTau);
        rCamPoly_Acc := (60.0 * rCamNormTau) -
                        (180.0 * rCamNormTau * rCamNormTau) +
                        (120.0 * rCamNormTau * rCamNormTau * rCamNormTau);
    ELSIF bInShearCutWindow THEN
        (* Synchronous Cutting Segment: Tangential blade speed = Strip linear speed *)
        rCamExecutionPhase := 2;
        rCamNormTau := 1.0;
        rCamPoly_Pos := 1.0;
        rCamPoly_Vel := 1.0;
        rCamPoly_Acc := 0.0;
    ELSE
        (* Deceleration Cam Segment *)
        rCamExecutionPhase := 3;
        rCamNormTau := (rShearBladeAngleNormalized - rCutWindowEndAngle_rad) /
                       MAX(0.001, rCamDecelAngle_rad);
        rCamNormTau := LIMIT(0.0, rCamNormTau, 1.0);
        rCamPoly_Pos := 1.0 - ((10.0 * rCamNormTau * rCamNormTau * rCamNormTau) -
                               (15.0 * rCamNormTau * rCamNormTau * rCamNormTau * rCamNormTau) +
                               (6.0  * rCamNormTau * rCamNormTau * rCamNormTau * rCamNormTau * rCamNormTau));
        rCamPoly_Vel := 1.0 - ((30.0 * rCamNormTau * rCamNormTau) -
                               (60.0 * rCamNormTau * rCamNormTau * rCamNormTau) +
                               (30.0 * rCamNormTau * rCamNormTau * rCamNormTau * rCamNormTau));
        rCamPoly_Acc := -1.0 * ((60.0 * rCamNormTau) -
                                (180.0 * rCamNormTau * rCamNormTau) +
                                (120.0 * rCamNormTau * rCamNormTau * rCamNormTau));
    END_IF;
ELSE
    (* Short Sheet Mode: Drum Must Rotate Faster Than Line Velocity Between Cuts *)
    rCamExecutionPhase := 2;
    rCamPoly_Pos := 1.0;
    rCamPoly_Vel := rShearDrumCircumference_m / MAX(0.100, rTargetCutLength_m);
    rCamPoly_Acc := 0.0;
END_IF;

(* Dynamic Cam Velocity Reference in RPM *)
IF bInShearCutWindow THEN
    (* Blade tip linear speed matches web speed: omega = v_web / r_drum *)
    rRotaryShearCamVelRef_RPM := ((rWebLinearSpeed_m_s / rShearDrumRadius_m) * 60.0) / (2.0 * rMathPi);
    rRotaryShearCamPosRef_deg := 180.0;
ELSE
    rRotaryShearCamVelRef_RPM := (((rWebLinearSpeed_m_s / rShearDrumRadius_m) * rCamPoly_Vel) * 60.0) / (2.0 * rMathPi);
    rRotaryShearCamPosRef_deg := (rShearBladeAngleNormalized * 180.0) / rMathPi;
END_IF;

(* Radial and Linear Cam Tracking Error *)
rShearCamPhaseError_rad := rShearBladeAngle_rad - ((rRotaryShearCamPosRef_deg * rMathPi) / 180.0);
rShearArcLinearError_mm := rShearCamPhaseError_rad * rShearDrumRadius_m * 1000.0;
"""
    code_parts.append(phase4)
    
    # PHASE 5: Closed-Loop Electro-Hydraulic Edge Guide
    phase5 = """
(* ==================================================================================================================== *)
(* PHASE 5: CLOSED-LOOP ELECTRO-HYDRAULIC EDGE POSITION CONTROL (EPC / CPC)                                             *)
(* ==================================================================================================================== *)
rEdgeError_mm := rEdgeGuideSensor_mm;

(* Numerical Differentiation for Edge Rate *)
rEdgeDeriv_mm_s := (rEdgeError_mm - rPrevEdgeError_mm) / rCycleTime_s;
rPrevEdgeError_mm := rEdgeError_mm;

(* Anti-Windup Trapezoidal Integral Accumulator *)
IF ABS(rEdgeCylinderCmd_Raw) < 95.0 THEN
    rEdgeIntegral_mm_s := rEdgeIntegral_mm_s + (rEdgeError_mm * rCycleTime_s);
END_IF;

(* PID Control Law for Payoff Reel Lateral Centering Cylinder *)
rEdgeCylinderCmd_Raw := (rEdgeGuideKp * rEdgeError_mm) +
                        (rEdgeGuideKi * rEdgeIntegral_mm_s) +
                        (rEdgeGuideKd * rEdgeDeriv_mm_s);

(* Saturation Limiting [-100.0% .. +100.0%] *)
rEdgeGuideCylinderCommand_pct := LIMIT(-100.0, rEdgeCylinderCmd_Raw, 100.0);
"""
    code_parts.append(phase5)
    
    # PHASE 6: Discrete State-Space Observer & State Vector Propagation
    phase6 = """
(* ==================================================================================================================== *)
(* PHASE 6: DISCRETE STATE-SPACE OBSERVER & PREDICTIVE STATE PROPAGATION                                                *)
(* ==================================================================================================================== *)
(* Populate Sensor Measurement Observation Vector vecY_meas *)
vecY_meas[1] := (rCoilRadius_Calc_m - rMandrelRadiusCore_m); (* Radius above core [m] *)
vecY_meas[2] := rUncoilerAngularVelocity_rad_s;              (* Payoff reel speed [rad/s] *)
vecY_meas[3] := rDancerPosition_mm * 0.001;                  (* Dancer stroke [m] *)
vecY_meas[4] := rTension_Voted_kN * 1000.0;                  (* Inter-stand web tension [N] *)
vecY_meas[5] := rShearBladeAngleNormalized;                  (* Rotary shear drum angle [rad] *)
vecY_meas[6] := rShearAngularSpeed_rad_s;                    (* Rotary shear drum speed [rad/s] *)
vecY_meas[7] := rLengthDeviationError_mm * 0.001;            (* Sheet cut length error [m] *)
vecY_meas[8] := (rStackerBeltSpeed_m_min / 60.0);            (* Stacker belt speed [m/s] *)

(* Calculate Innovation Residual Vector: y_err = y_meas - C * x_hat *)
FOR iMpcRow := 1 TO 8 DO
    vecY_err[iMpcRow] := vecY_meas[iMpcRow];
    FOR iMpcCol := 1 TO 8 DO
        vecY_err[iMpcRow] := vecY_err[iMpcRow] - (matC[iMpcRow, iMpcCol] * vecX_hat[iMpcCol]);
    END_FOR;
END_FOR;

(* Propagate Observer State: x_hat[k+1] = A * x_hat[k] + B * u[k] + L * y_err[k] *)
FOR iMpcRow := 1 TO 8 DO
    vecX_pred[iMpcRow] := 0.0;
    (* State Dynamic Transition A * x_hat *)
    FOR iMpcCol := 1 TO 8 DO
        vecX_pred[iMpcRow] := vecX_pred[iMpcRow] + (matA[iMpcRow, iMpcCol] * vecX_hat[iMpcCol]);
    END_FOR;
    (* Control Input Propagation B * u *)
    FOR iMpcCol := 1 TO 4 DO
        vecX_pred[iMpcRow] := vecX_pred[iMpcRow] + (matB[iMpcRow, iMpcCol] * vecU_cmd[iMpcCol]);
    END_FOR;
    (* Luenberger Innovation Correction L * y_err *)
    FOR iMpcCol := 1 TO 8 DO
        vecX_pred[iMpcRow] := vecX_pred[iMpcRow] + (matL[iMpcRow, iMpcCol] * vecY_err[iMpcCol]);
    END_FOR;
END_FOR;

(* Update State Estimates for Next Cycle *)
FOR iMpcState := 1 TO 8 DO
    vecX_hat[iMpcState] := vecX_pred[iMpcState];
END_FOR;
"""
    code_parts.append(phase6)
    
    # PHASE 7: Receding-Horizon MPC Quadratic Optimization
    phase7 = """
(* ==================================================================================================================== *)
(* PHASE 7: RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) QUADRATIC COST OPTIMIZATION                                 *)
(* ==================================================================================================================== *)
(* Formulate Active-Set Quadratic Optimization Objective:
   J(u) = (x - x_ref)^T * Q * (x - x_ref) + Delta_u^T * R * Delta_u + x_terminal^T * P * x_terminal
   Gradient grad(J) = H * u + g
*)
(* Calculate Linear Gradient Component g from State Errors *)
vecGrad_J[1] := (matQ[4,4] * (vecX_hat[4] - (rTargetTension_kN * 1000.0)) * 0.001) +
                (matQ[2,2] * (vecX_hat[2] - rUncoilerAngularVelocity_rad_s) * 0.05);

vecGrad_J[2] := (matQ[4,4] * (vecX_hat[4] - (rTargetTension_kN * 1000.0)) * 0.02) +
                (matQ[3,3] * (vecX_hat[3] - 0.0) * 15.0);

vecGrad_J[3] := (matQ[5,5] * (vecX_hat[5] - ((rRotaryShearCamPosRef_deg * rMathPi) / 180.0)) * 25.0) +
                (matQ[6,6] * (vecX_hat[6] - ((rRotaryShearCamVelRef_RPM * 2.0 * rMathPi) / 60.0)) * 5.0) +
                (matQ[7,7] * vecX_hat[7] * 40.0);

vecGrad_J[4] := (matQ[8,8] * (vecX_hat[8] - (rWebLinearSpeed_m_s * 1.10)) * 8.0);

(* Initialize Control Vector with Baseline Feedforward Profile *)
vecU_opt[1] := rUncoilerTensionTorque_Nm + rUncoilerInertiaTorque_Nm + rUncoilerFrictionTorque_Nm;
vecU_opt[2] := rLineSpeedSet_m_min;
vecU_opt[3] := 0.0;
vecU_opt[4] := 0.0;

(* Iterative Projected Gradient Descent Solver (5 Sequential Iterations) *)
FOR iMpcIterIdx := 1 TO 5 DO
    FOR iMpcRow := 1 TO 4 DO
        vecDeltaU[iMpcRow] := 0.0;
        FOR iMpcCol := 1 TO 4 DO
            vecDeltaU[iMpcRow] := vecDeltaU[iMpcRow] + (matHessian[iMpcRow, iMpcCol] * vecU_opt[iMpcCol]);
        END_FOR;
        vecDeltaU[iMpcRow] := vecDeltaU[iMpcRow] + vecGrad_J[iMpcRow];
        
        (* Gradient Step with Projection Onto Physical Actuator Saturation Bounds *)
        vecU_opt[iMpcRow] := vecU_opt[iMpcRow] - (rMpcStepAlpha * vecDeltaU[iMpcRow]);
    END_FOR;
    
    (* Hard Boundary Box Constraints *)
    vecU_opt[1] := LIMIT(rUncoilerTorqueMin_Nm, vecU_opt[1], rUncoilerTorqueMax_Nm);
    vecU_opt[2] := LIMIT(rBridleSpeedMin_m_min, vecU_opt[2], rBridleSpeedMax_m_min);
    vecU_opt[3] := LIMIT(rShearTorqueMin_Nm,    vecU_opt[3], rShearTorqueMax_Nm);
    vecU_opt[4] := LIMIT(rStackerAccelMin_m_s2, vecU_opt[4], rStackerAccelMax_m_s2);
END_FOR;

(* Bind Optimal Control Action to Vector Command *)
FOR iMpcCol := 1 TO 4 DO
    vecU_cmd[iMpcCol] := vecU_opt[iMpcCol];
END_FOR;
"""
    code_parts.append(phase7)
    
    # PHASE 8: Master Finite State Machine
    phase8 = """
(* ==================================================================================================================== *)
(* PHASE 8: MASTER HIGH-SPEED SLITTING & ROTARY SHEAR FINITE STATE MACHINE (14 STATES)                                 *)
(* ==================================================================================================================== *)
(* Track State Transition Dwell Timers and One-Shot Entry Markers *)
IF iCurrentFsmState <> iPreviousFsmState THEN
    rStateDwellTimer_s := 0.0;
    bStateFirstScan := TRUE;
    iPreviousFsmState := iCurrentFsmState;
ELSE
    rStateDwellTimer_s := rStateDwellTimer_s + rCycleTime_s;
    bStateFirstScan := FALSE;
END_IF;

(* Master Safety Circuit Interlock Override *)
IF NOT bEmergencyStopOk OR bAlarm_EmergencyStopActive_HH THEN
    iCurrentFsmState := 999; (* Force Immediate Trip *)
END_IF;

CASE iCurrentFsmState OF

    0: (* STATE_STANDBY_IDLE *)
        bLineRunning := FALSE;
        rUncoilerTorqueCommand_Nm := 0.0;
        rEntryBridleSpeedRef_m_min := 0.0;
        rSlitterArborTorque_Nm := 0.0;
        rRotaryShearTorqueCommand_Nm := 0.0;
        rStackerBeltSpeed_m_min := 0.0;
        bScrapDivertGateActive := FALSE;
        bSheetCutStrokePulse := FALSE;
        
        IF bAutoCycleStart AND bEmergencyStopOk AND NOT bLineFaultActive THEN
            iCurrentFsmState := 10; (* Proceed to Coil Loading *)
        END_IF;

    10: (* STATE_COIL_CAR_LOADING *)
        (* Coil car lifter elevates raw master coil and aligns with uncoiler mandrel axis *)
        bLineRunning := FALSE;
        rUncoilerTorqueCommand_Nm := 0.0;
        rEntryBridleSpeedRef_m_min := 0.0;
        
        IF rStateDwellTimer_s > 3.5 THEN
            (* Coil mechanically positioned on mandrel arbor *)
            iCurrentFsmState := 20;
        END_IF;

    20: (* STATE_MANDREL_EXPAND_CLAMP *)
        (* Hydraulic wedge cylinder expands mandrel drum segments to clamp coil ID *)
        bLineRunning := FALSE;
        rUncoilerTorqueCommand_Nm := 0.0;
        rEntryBridleSpeedRef_m_min := 0.0;
        
        IF rMandrelHydPressure_bar >= rAlarmSet_MandrelPres_L_bar AND rStateDwellTimer_s > 2.0 THEN
            (* Mandrel clamped securely under full hydraulic pressure *)
            iCurrentFsmState := 30;
        ELSIF rStateDwellTimer_s > 10.0 THEN
            (* Mandrel pressure build timeout fault *)
            bAlarm_MandrelPressureDrop_LL := TRUE;
            iCurrentFsmState := 999;
        END_IF;

    30: (* STATE_PEELER_THREADING_JOG *)
        (* Hydraulic hold-down snubber roll clamps coil OD, peeler blade extends, strip inched into flattener *)
        bLineRunning := FALSE;
        rUncoilerTorqueCommand_Nm := 150.0; (* Slight positive jog torque *)
        rEntryBridleSpeedRef_m_min := 5.0;  (* Inching jog speed 5 m/min *)
        
        IF rStateDwellTimer_s > 4.0 THEN
            (* Strip lead end threaded through entry pinch rolls *)
            iCurrentFsmState := 40;
        END_IF;

    40: (* STATE_EDGE_GUIDE_CALIBRATE *)
        (* Ultrasonic strip edge sensor active; payoff base shifted to center web *)
        bLineRunning := FALSE;
        rUncoilerTorqueCommand_Nm := 0.0;
        rEntryBridleSpeedRef_m_min := 0.0;
        
        IF ABS(rEdgeGuideSensor_mm) < 3.0 AND rStateDwellTimer_s > 1.5 THEN
            (* Strip edge centered within +/- 3 mm tolerance *)
            iCurrentFsmState := 50;
        ELSIF rStateDwellTimer_s > 8.0 THEN
            (* Edge alignment excursion timeout *)
            bAlarm_EdgeGuideExcursion_H := TRUE;
            iCurrentFsmState := 50; (* Continue with warning *)
        END_IF;

    50: (* STATE_SLITTER_KNIFE_ENGAGE *)
        (* Upper slitter arbor servo lowers rotary knives to specified penetration depth *)
        bLineRunning := FALSE;
        rSlitterTargetPlunge_mm := LIMIT(0.20, rStripThickness_mm * 0.35, 1.80);
        rSlitterArborTorque_Nm := 120.0; (* Pre-spin slitter circular knives *)
        
        IF ABS(rSlitterArborPenetration_mm - rSlitterTargetPlunge_mm) < 0.05 AND rStateDwellTimer_s > 2.0 THEN
            (* Knives engaged at precision overlap depth *)
            iCurrentFsmState := 60;
        ELSIF rStateDwellTimer_s > 6.0 THEN
            iCurrentFsmState := 60; (* Continue *)
        END_IF;

    60: (* STATE_BRIDLE_DANCER_PRELOAD *)
        (* Entry S-bridle closes pinch roll, tension dancer pneumatic cylinder charges *)
        bLineRunning := FALSE;
        rUncoilerTorqueCommand_Nm := vecU_cmd[1] * 0.50; (* Apply 50% preload back-tension *)
        rEntryBridleSpeedRef_m_min := 0.0;
        
        IF rTension_Voted_kN >= (rTargetTension_kN * 0.70) AND rStateDwellTimer_s > 2.0 THEN
            (* Web tension preloaded, dancer centered *)
            iCurrentFsmState := 70;
        ELSIF rStateDwellTimer_s > 7.0 THEN
            bAlarm_TensionSlack_L := TRUE;
            iCurrentFsmState := 70;
        END_IF;

    70: (* STATE_LINE_RAMP_ACCELERATION *)
        (* Line ramps up from thread speed to production setpoint (up to 120 m/min) *)
        bLineRunning := TRUE;
        rEntryBridleSpeedRef_m_min := MIN(rLineSpeedSet_m_min,
                                          rEntryBridleSpeedRef_m_min + (15.0 * rCycleTime_s)); (* 15 m/min/s ramp *)
        rUncoilerTorqueCommand_Nm := vecU_cmd[1];
        rSlitterArborTorque_Nm := 280.0 + (rWebLinearSpeed_m_s * 45.0);
        rStackerBeltSpeed_m_min := rActualStripSpeed_m_min * 1.10; (* Stacker leads by +10% *)
        
        IF rActualStripSpeed_m_min >= (rLineSpeedSet_m_min * 0.95) THEN
            (* Steady-state operating velocity achieved *)
            iCurrentFsmState := 80;
        END_IF;

    80: (* STATE_ROTARY_SHEAR_ELECTRONIC_CAM_SYNC *)
        (* Flying shear drum accelerates and synchronizes phase to strip displacement *)
        bLineRunning := TRUE;
        rEntryBridleSpeedRef_m_min := rLineSpeedSet_m_min;
        rUncoilerTorqueCommand_Nm := vecU_cmd[1];
        rSlitterArborTorque_Nm := 320.0;
        rStackerBeltSpeed_m_min := rActualStripSpeed_m_min * 1.10;
        
        (* Apply MPC Shear Servo Command *)
        rRotaryShearTorqueCommand_Nm := vecU_cmd[3];
        
        IF bInShearCutWindow AND ABS(rShearArcLinearError_mm) < rAlarmSet_ShearSync_H_ArcErr_mm THEN
            (* Blade synchronized and aligned for cut entry *)
            iCurrentFsmState := 90;
        END_IF;

    90: (* STATE_FLYING_CUT_EXECUTION *)
        (* Synchronous cut point: blade severs strip, cut pulse emitted, sheet measured *)
        bLineRunning := TRUE;
        rEntryBridleSpeedRef_m_min := rLineSpeedSet_m_min;
        rUncoilerTorqueCommand_Nm := vecU_cmd[1];
        rSlitterArborTorque_Nm := 320.0;
        rStackerBeltSpeed_m_min := rActualStripSpeed_m_min * 1.10;
        rRotaryShearTorqueCommand_Nm := vecU_cmd[3] + 450.0; (* Cutting resistance torque boost *)
        
        IF bStateFirstScan THEN
            bSheetCutStrokePulse := TRUE;
            rCutStrokePulseTimer_s := 0.050; (* 50 ms strobe pulse *)
        END_IF;
        
        IF NOT bInShearCutWindow THEN
            (* Blades cleared cut collision zone *)
            iCurrentFsmState := 100;
        END_IF;

    100: (* STATE_VACUUM_SHEET_CONVEY *)
        (* Severed sheet accelerates on vacuum belt, pulling gap behind trailing edge *)
        bLineRunning := TRUE;
        rEntryBridleSpeedRef_m_min := rLineSpeedSet_m_min;
        rUncoilerTorqueCommand_Nm := vecU_cmd[1];
        rSlitterArborTorque_Nm := 320.0;
        rStackerBeltSpeed_m_min := rActualStripSpeed_m_min * 1.12;
        rRotaryShearTorqueCommand_Nm := vecU_cmd[3];
        
        IF bRejectScrapCutCurrent OR bWeldSeamDetected OR bManualScrapDumpCmd THEN
            iCurrentFsmState := 110; (* Divert to Scrap Bin *)
        ELSE
            iCurrentFsmState := 120; (* Pass to Prime Stacker *)
        END_IF;

    110: (* STATE_SCRAP_GATE_DIVERT *)
        (* High-speed pneumatic diverter gate flips up; sheet falls into scrap hopper *)
        bLineRunning := TRUE;
        rEntryBridleSpeedRef_m_min := rLineSpeedSet_m_min;
        rUncoilerTorqueCommand_Nm := vecU_cmd[1];
        rStackerBeltSpeed_m_min := rActualStripSpeed_m_min * 1.10;
        rRotaryShearTorqueCommand_Nm := vecU_cmd[3];
        bScrapDivertGateActive := TRUE;
        
        IF rStateDwellTimer_s > rScrapGateHoldDuration_s THEN
            bScrapDivertGateActive := FALSE;
            bRejectScrapCutCurrent := FALSE;
            udiScrapCutCount := udiScrapCutCount + 1;
            iCurrentFsmState := 80; (* Return to Flying Cam Sync for next cut *)
        END_IF;

    120: (* STATE_MAGNETIC_STACKING *)
        (* Prime sheet conveyed over scissor lift table; overhead magnets release onto pallet *)
        bLineRunning := TRUE;
        rEntryBridleSpeedRef_m_min := rLineSpeedSet_m_min;
        rUncoilerTorqueCommand_Nm := vecU_cmd[1];
        rStackerBeltSpeed_m_min := rActualStripSpeed_m_min * 1.10;
        rRotaryShearTorqueCommand_Nm := vecU_cmd[3];
        bScrapDivertGateActive := FALSE;
        
        IF bStateFirstScan THEN
            udiTotalCutCount := udiTotalCutCount + 1;
        END_IF;
        
        IF bPalletFullSignal THEN
            (* Scissor lift pallet capacity reached *)
            iCurrentFsmState := 130;
        ELSIF rCoilRadius_Calc_m <= (rMandrelCoreDia_mm * 0.0005 + 0.005) THEN
            (* Coil Tail-Out Reached Mandrel Core *)
            iCurrentFsmState := 130;
        ELSE
            iCurrentFsmState := 80; (* Return to Flying Cam Sync for next cut *)
        END_IF;

    130: (* STATE_LINE_DECEL_TAIL_OUT *)
        (* Line ramps down to stop; slitter knives disengage; remaining strip expelled *)
        bLineRunning := FALSE;
        rEntryBridleSpeedRef_m_min := MAX(0.0, rEntryBridleSpeedRef_m_min - (20.0 * rCycleTime_s));
        rUncoilerTorqueCommand_Nm := 0.0;
        rSlitterArborTorque_Nm := 0.0;
        rRotaryShearTorqueCommand_Nm := 0.0;
        rStackerBeltSpeed_m_min := MAX(0.0, rStackerBeltSpeed_m_min - (25.0 * rCycleTime_s));
        
        IF rActualStripSpeed_m_min < 0.10 THEN
            iCurrentFsmState := 0; (* Return to Standby Idle *)
        END_IF;

    999: (* STATE_EMERGENCY_FAULT_TRIP *)
        (* Emergency Stop Activated: Fast Controlled Dynamic Braking & Actuator Shutdown *)
        bLineRunning := FALSE;
        bLineFaultActive := TRUE;
        rEntryBridleSpeedRef_m_min := 0.0;
        rUncoilerTorqueCommand_Nm := -12000.0; (* Full Regenerative Emergency Brake *)
        rSlitterArborTorque_Nm := 0.0;
        rRotaryShearTorqueCommand_Nm := -4500.0; (* Fast Shear Stop Before Collision *)
        rStackerBeltSpeed_m_min := 0.0;
        bScrapDivertGateActive := FALSE;
        bSheetCutStrokePulse := FALSE;
        
        IF bResetFault AND bEmergencyStopOk AND NOT bAlarm_EmergencyStopActive_HH THEN
            bLineFaultActive := FALSE;
            bAlarm_TensionBreakage_LL := FALSE;
            bAlarm_TensionSurge_HH := FALSE;
            bAlarm_MandrelPressureDrop_LL := FALSE;
            bAlarm_ShearCamSyncClash_HH := FALSE;
            bAlarm_EdgeGuideExcursion_HH := FALSE;
            bAlarm_CutLengthRunaway_HH := FALSE;
            bAlarm_SpeedSensorLoss_HH := FALSE;
            bAlarm_EncoderFailure_HH := FALSE;
            bAlarm_TensionSensorLoss_HH := FALSE;
            iCurrentFsmState := 0; (* Return to Standby *)
        END_IF;

END_CASE;

(* Update FSM Status Output *)
eOperationalState := iCurrentFsmState;

(* Manage Strobe Cut Pulse Timer *)
IF rCutStrokePulseTimer_s > 0.0 THEN
    rCutStrokePulseTimer_s := rCutStrokePulseTimer_s - rCycleTime_s;
    IF rCutStrokePulseTimer_s <= 0.0 THEN
        bSheetCutStrokePulse := FALSE;
    END_IF;
END_IF;
"""
    code_parts.append(phase8)
    
    # PHASE 9: Cut Length Observer & Reject Gate Divert Logic
    phase9 = """
(* ==================================================================================================================== *)
(* PHASE 9: HIGH-PRECISION CUT LENGTH OBSERVER & REJECT GATE DIVERT LOGIC                                              *)
(* ==================================================================================================================== *)
(* Track Incremental Master Encoder Displacement *)
IF rPrevEncoderPosition_mm > 0.0 THEN
    rIncrementalDeltaLength_mm := rEncoder_Voted_mm - rPrevEncoderPosition_mm;
    IF rIncrementalDeltaLength_mm < 0.0 THEN
        (* Encoder Wrap-Around Protection *)
        rIncrementalDeltaLength_mm := 0.0;
    END_IF;
ELSE
    rIncrementalDeltaLength_mm := 0.0;
END_IF;
rPrevEncoderPosition_mm := rEncoder_Voted_mm;

(* Accumulate Strip Displaced Linear Length *)
rSheetLengthAccumulator_mm := rSheetLengthAccumulator_mm + rIncrementalDeltaLength_mm;

(* Latch Cut Length Upon Flying Shear Cutting Point Pulse *)
IF bSheetCutStrokePulse THEN
    rLastCutMeasuredLength_mm := rSheetLengthAccumulator_mm;
    rActualCutLength_mm := rLastCutMeasuredLength_mm;
    rLengthDeviationError_mm := rLastCutMeasuredLength_mm - rTargetSheetLength_mm;
    rLengthErrorLastCut_mm := rLengthDeviationError_mm;
    
    (* Check Quality Tolerance Acceptance Window (< +/- 0.20 mm) *)
    IF ABS(rLengthDeviationError_mm) > rAlarmSet_CutLength_H_Dev_mm THEN
        bRejectScrapCutCurrent := TRUE;
        bAlarm_CutLengthOutTolerance_H := TRUE;
    ELSE
        bAlarm_CutLengthOutTolerance_H := FALSE;
    END_IF;
    
    IF ABS(rLengthDeviationError_mm) > rAlarmSet_CutLength_HH_Dev_mm THEN
        bAlarm_CutLengthRunaway_HH := TRUE;
    END_IF;
    
    (* Reset Length Accumulator for Next Sheet Interval *)
    rSheetLengthAccumulator_mm := 0.0;
END_IF;
"""
    code_parts.append(phase9)
    
    # PHASE 10: ISA-18.2 Alarms & Diagnostic Word Packing
    phase10 = """
(* ==================================================================================================================== *)
(* PHASE 10: ISA-18.2 MULTI-TIERED ALARM MATRIX & DIAGNOSTIC WORD PACKING                                               *)
(* ==================================================================================================================== *)

(* --- ISA-18.2 Web Tension Alarms with Deadband Hysteresis --- *)
IF rActualStripTension_kN < (rAlarmSet_Tension_LL_Collapse_kN) AND bLineRunning THEN
    bAlarm_TensionBreakage_LL := TRUE; (* Web Break / Strip Severed *)
ELSIF rActualStripTension_kN > (rAlarmSet_Tension_LL_Collapse_kN + rAlarmSet_Tension_Deadband_kN) THEN
    bAlarm_TensionBreakage_LL := FALSE;
END_IF;

IF rActualStripTension_kN < (rAlarmSet_Tension_L_Slack_kN) AND bLineRunning THEN
    bAlarm_TensionSlack_L := TRUE; (* Low Tension Sag / Buckling Risk *)
ELSIF rActualStripTension_kN > (rAlarmSet_Tension_L_Slack_kN + rAlarmSet_Tension_Deadband_kN) THEN
    bAlarm_TensionSlack_L := FALSE;
END_IF;

IF rActualStripTension_kN > (rAlarmSet_Tension_HH_Surge_kN) THEN
    bAlarm_TensionSurge_HH := TRUE; (* Tension Spike / Strip Rupture Hazard *)
ELSIF rActualStripTension_kN < (rAlarmSet_Tension_HH_Surge_kN - rAlarmSet_Tension_Deadband_kN) THEN
    bAlarm_TensionSurge_HH := FALSE;
END_IF;

IF rActualStripTension_kN > (rAlarmSet_Tension_H_Necking_kN) THEN
    bAlarm_TensionNecking_H := TRUE; (* High Tension Web Necking Warning *)
ELSIF rActualStripTension_kN < (rAlarmSet_Tension_H_Necking_kN - rAlarmSet_Tension_Deadband_kN) THEN
    bAlarm_TensionNecking_H := FALSE;
END_IF;

(* --- ISA-18.2 Mandrel Hydraulic Pressure Alarms --- *)
IF rMandrelHydPressure_bar < (rAlarmSet_MandrelPres_LL_bar) THEN
    bAlarm_MandrelPressureDrop_LL := TRUE; (* Severe Clamping Loss *)
ELSIF rMandrelHydPressure_bar > (rAlarmSet_MandrelPres_LL_bar + rAlarmSet_MandrelPres_Deadband) THEN
    bAlarm_MandrelPressureDrop_LL := FALSE;
END_IF;

IF rMandrelHydPressure_bar < (rAlarmSet_MandrelPres_L_bar) THEN
    bAlarm_MandrelPressureLow_L := TRUE; (* Clamping Pressure Advisory *)
ELSIF rMandrelHydPressure_bar > (rAlarmSet_MandrelPres_L_bar + rAlarmSet_MandrelPres_Deadband) THEN
    bAlarm_MandrelPressureLow_L := FALSE;
END_IF;

(* --- ISA-18.2 Rotary Flying Shear Cam Tracking Error Alarms --- *)
IF ABS(rShearArcLinearError_mm) > (rAlarmSet_ShearSync_HH_Trip_mm) AND bLineRunning THEN
    bAlarm_ShearCamSyncClash_HH := TRUE; (* Blade Collision Imminent *)
ELSIF ABS(rShearArcLinearError_mm) < (rAlarmSet_ShearSync_HH_Trip_mm - rAlarmSet_ShearSync_Deadband_mm) THEN
    bAlarm_ShearCamSyncClash_HH := FALSE;
END_IF;

IF ABS(rShearArcLinearError_mm) > (rAlarmSet_ShearSync_H_ArcErr_mm) AND bLineRunning THEN
    bAlarm_ShearCamSyncWarning_H := TRUE; (* Electronic Cam Deviation Advisory *)
ELSIF ABS(rShearArcLinearError_mm) < (rAlarmSet_ShearSync_H_ArcErr_mm - rAlarmSet_ShearSync_Deadband_mm) THEN
    bAlarm_ShearCamSyncWarning_H := FALSE;
END_IF;

(* --- ISA-18.2 Lateral Edge Guide Excursion Alarms --- *)
IF ABS(rEdgeGuideSensor_mm) > rAlarmSet_EdgeGuide_HH_Trip_mm THEN
    bAlarm_EdgeGuideExcursion_HH := TRUE;
ELSE
    bAlarm_EdgeGuideExcursion_HH := FALSE;
END_IF;

IF ABS(rEdgeGuideSensor_mm) > rAlarmSet_EdgeGuide_H_Dev_mm THEN
    bAlarm_EdgeGuideExcursion_H := TRUE;
ELSE
    bAlarm_EdgeGuideExcursion_H := FALSE;
END_IF;

(* --- Emergency Stop Safety Circuit Alarm --- *)
bAlarm_EmergencyStopActive_HH := NOT bEmergencyStopOk;

(* --- ISA-18.2 Bitfield Word Packing --- *)

(* 1. Critical Emergency Trip Word (16#0000 = Clean, Any Bit High = E-Stop) *)
wAlarmWord_Critical_ISA18 := 16#0000;
IF bAlarm_EmergencyStopActive_HH   THEN wAlarmWord_Critical_ISA18 := wAlarmWord_Critical_ISA18 OR 16#0001; END_IF;
IF bAlarm_TensionBreakage_LL       THEN wAlarmWord_Critical_ISA18 := wAlarmWord_Critical_ISA18 OR 16#0002; END_IF;
IF bAlarm_TensionSurge_HH          THEN wAlarmWord_Critical_ISA18 := wAlarmWord_Critical_ISA18 OR 16#0004; END_IF;
IF bAlarm_MandrelPressureDrop_LL   THEN wAlarmWord_Critical_ISA18 := wAlarmWord_Critical_ISA18 OR 16#0008; END_IF;
IF bAlarm_ShearCamSyncClash_HH     THEN wAlarmWord_Critical_ISA18 := wAlarmWord_Critical_ISA18 OR 16#0010; END_IF;
IF bAlarm_EdgeGuideExcursion_HH    THEN wAlarmWord_Critical_ISA18 := wAlarmWord_Critical_ISA18 OR 16#0020; END_IF;
IF bAlarm_CutLengthRunaway_HH      THEN wAlarmWord_Critical_ISA18 := wAlarmWord_Critical_ISA18 OR 16#0040; END_IF;
IF bAlarm_SpeedSensorLoss_HH       THEN wAlarmWord_Critical_ISA18 := wAlarmWord_Critical_ISA18 OR 16#0080; END_IF;
IF bAlarm_EncoderFailure_HH        THEN wAlarmWord_Critical_ISA18 := wAlarmWord_Critical_ISA18 OR 16#0100; END_IF;
IF bAlarm_TensionSensorLoss_HH     THEN wAlarmWord_Critical_ISA18 := wAlarmWord_Critical_ISA18 OR 16#0200; END_IF;

(* 2. Warning Advisory Word (16#0000 = Clean) *)
wAlarmWord_Warning_ISA18 := 16#0000;
IF bAlarm_TensionSlack_L           THEN wAlarmWord_Warning_ISA18 := wAlarmWord_Warning_ISA18 OR 16#0001; END_IF;
IF bAlarm_TensionNecking_H         THEN wAlarmWord_Warning_ISA18 := wAlarmWord_Warning_ISA18 OR 16#0002; END_IF;
IF bAlarm_MandrelPressureLow_L     THEN wAlarmWord_Warning_ISA18 := wAlarmWord_Warning_ISA18 OR 16#0004; END_IF;
IF bAlarm_ShearCamSyncWarning_H    THEN wAlarmWord_Warning_ISA18 := wAlarmWord_Warning_ISA18 OR 16#0008; END_IF;
IF bAlarm_EdgeGuideExcursion_H     THEN wAlarmWord_Warning_ISA18 := wAlarmWord_Warning_ISA18 OR 16#0010; END_IF;
IF bAlarm_CutLengthOutTolerance_H  THEN wAlarmWord_Warning_ISA18 := wAlarmWord_Warning_ISA18 OR 16#0020; END_IF;
IF bAlarm_SpeedSensorDiscrepancy_H THEN wAlarmWord_Warning_ISA18 := wAlarmWord_Warning_ISA18 OR 16#0040; END_IF;
IF bAlarm_EncoderDiscrepancy_H     THEN wAlarmWord_Warning_ISA18 := wAlarmWord_Warning_ISA18 OR 16#0080; END_IF;
IF bAlarm_TensionSensorDiscrepancy_H THEN wAlarmWord_Warning_ISA18 := wAlarmWord_Warning_ISA18 OR 16#0100; END_IF;

(* 3. Operational Automation Status Word *)
wAutomationStatusWord := 16#0000;
IF bLineRunning                    THEN wAutomationStatusWord := wAutomationStatusWord OR 16#0001; END_IF;
IF (iCurrentFsmState >= 70 AND iCurrentFsmState <= 120) THEN wAutomationStatusWord := wAutomationStatusWord OR 16#0002; END_IF;
IF bInShearCutWindow               THEN wAutomationStatusWord := wAutomationStatusWord OR 16#0004; END_IF;
IF bScrapDivertGateActive          THEN wAutomationStatusWord := wAutomationStatusWord OR 16#0008; END_IF;
IF bSheetCutStrokePulse            THEN wAutomationStatusWord := wAutomationStatusWord OR 16#0010; END_IF;
IF bSpeed_SensorFault_1 OR bSpeed_SensorFault_2 OR bSpeed_SensorFault_3 THEN wAutomationStatusWord := wAutomationStatusWord OR 16#0020; END_IF;
IF bEncoder_SensorFault_A OR bEncoder_SensorFault_B OR bEncoder_SensorFault_C THEN wAutomationStatusWord := wAutomationStatusWord OR 16#0040; END_IF;
IF bTension_SensorFault_1 OR bTension_SensorFault_2 OR bTension_SensorFault_3 THEN wAutomationStatusWord := wAutomationStatusWord OR 16#0080; END_IF;
IF (iCurrentFsmState = 999)        THEN wAutomationStatusWord := wAutomationStatusWord OR 16#8000; END_IF;

(* Cumulative Fault & Warning Outputs *)
bLineFaultActive := (wAlarmWord_Critical_ISA18 <> 16#0000);
bLineWarningActive := (wAlarmWord_Warning_ISA18 <> 16#0000);

(* Command Actuator Output Binding *)
rUncoilerTorqueCommand_Nm     := LIMIT(rUncoilerTorqueMin_Nm, rUncoilerTorqueCommand_Nm, rUncoilerTorqueMax_Nm);
rRotaryShearTorqueCommand_Nm := LIMIT(rShearTorqueMin_Nm,    rRotaryShearTorqueCommand_Nm, rShearTorqueMax_Nm);
"""
    code_parts.append(phase10)
    
    # 7. Closing declaration
    code_parts.append("\nEND_FUNCTION_BLOCK")
    
    full_code = "".join(code_parts)
    return full_code

if __name__ == "__main__":
    st_code = generate_iec_code()
    print(f"Generated ST code length: {len(st_code)} characters")
    
    prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 75+ years experienced Principal Automation Fellow & Cyber-Physical Systems Chair writing world-class, ultra-complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced discrete state-space matrices, Model Predictive Control (MPC) quadratic cost approximations, 2oo3 Triple Modular Redundant (TMR) voting with discrepancy timers, ISA-18.2 multi-tiered alarm matrices, and multi-stage finite state machines. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Commercial Continuous Coil Slitting & Rotary Flying Shear Metal Cut-to-Length Lines (Rank #98)**

Task: Implement the production-grade Function Block `FB_MetalProcessing_CoilSlitting_RotaryFlyingShear` governing:
1. Discrete State-Space Matrices (A, B, C, D) modeling steel strip payoff reel inertia change, entry bridle tension dancer loop, rotary shear blade angular velocity synchronization to moving web (electronic cam 5th-order polynomial matching line speed at cutting point), and magnetic stacker conveyor deceleration.
2. MPC quadratic cost formulation for active strip tension regulation (eliminating strip buckle or necking under 120 m/min throughput), electronic cam engagement phasing, and sheet cut-length error minimization (< 0.2 mm tolerance).
3. 2oo3 TMR voting logic for laser Doppler strip speed sensors, high-resolution optical master line encoders, and strip tension load cells.
4. High-Speed Slitting FSM: coil car loading, hydraulic mandrel expansion, automatic edge guide sensing, slitter knife engagement, rotary flying shear synchronization & cut, vacuum belt sheet transport, and reject scrap gate divert.
5. ISA-18.2 multi-tiered alarm matrix (HH, H, L, LL, web breakage tension collapse trip, flying shear cam synchronization error trip, hydraulic mandrel pressure drop).

Ensure exhaustive implementation with zero placeholders, full mathematical expansions, and complete variable declarations."""

    content_with_fence = "```iec-st\n" + st_code + "\n```"
    record = {
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": content_with_fence}
        ]
    }
    
    os.makedirs("data/swarm_raw", exist_ok=True)
    target_path = "data/swarm_raw/agent_519a712e.json"
    with open(target_path, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)
    print(f"Successfully saved to {target_path}")
