# Python script to generate FB_FoodBev_RotaryCanSeamer_2000CPM_DoubleSeam
import json
import os
import sys

def build_prompt():
    return """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 75+ years experienced Principal Automation Fellow & Cyber-Physical Systems Chair writing world-class, ultra-complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced discrete state-space matrices, Model Predictive Control (MPC) quadratic cost approximations, 2oo3 Triple Modular Redundant (TMR) voting with discrepancy timers, ISA-18.2 multi-tiered alarm matrices, and multi-stage finite state machines. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Food & Beverage Processing: Ultra-High-Speed Rotary Beverage Can Seamer (2,000 Cans/Minute, 18-Head Carousel) with Dynamic Dual-Roll Seaming Force Profiling & In-Line Acoustic Double-Seam Inspection**

Task: Implement the production-grade Function Block FB_FoodBev_RotaryCanSeamer_2000CPM_DoubleSeam governing:
1. 18-Head continuous rotary can seamer (output 2,000 cans/min, pitch line speed up to 4.5 m/s, can cycle time 30 ms per can).
2. Dynamic 2-Operation Double Seaming: Operation 1 curling roll folding can body hook and end hook; Operation 2 flattening roll ironing out seam wrinkles to guarantee hermetic tightness (> 85% overlap, seam thickness 1.15 mm +/- 0.03 mm, countersink depth).
3. High-speed electrohydraulic/servo-cam lifter plate: lifting filled cans against rotating seaming chuck with dynamic vertical load regulation (1,200 N to 2,200 N) preventing can wall crushing or beverage sloshing spillage.
4. Closed-loop carbon dioxide (CO2) / liquid nitrogen (LN2) under-cover gas gassing: inerting headspace before seaming to maintain dissolved oxygen DO < 30 ppb and target internal can pressure (1.2 to 2.5 bar).
5. High-speed in-line non-destructive acoustic inspection: resonant acoustic impact sensors measuring lid vibration frequency decay spectrum to detect micro-leaks, false seams, or loose covers on-the-fly.
6. High-speed pneumatic rejector: multi-valve solenoid blow-off or rotary pusher diverting defective cans at full line speed (30 ms response) without jamming downstream conveyors.
7. Discrete State-Space Model (16x16 state matrix A, 16x8 B, C, D) incorporating seaming carousel rotational inertia, seaming roll elastic contact deformation, lifter spring dynamics, and headspace gas pressure expansion.
8. Receding-horizon MPC for synchronized filler-seamer electronic gearing, lifter plate vertical force profile, and seaming roll cam track progression.
9. 2oo3 Triple Modular Redundancy (TMR) voting across carousel absolute rotary encoders, lifter load cells, under-cover CO2 gas pressure transmitters, and acoustic resonant frequencies with bumpless degradation.
10. 12-Stage Operational FSM (Can Filler Electronic Synchronization Handshake, Infeed Starwheel Can Body Indexing, Under-Cover Inert Gas Purging, Lifter Plate Dynamic Up-Stroke, 1st Operation Roll Seam Curling, Inter-Stage Clearance Transition, 2nd Operation Roll Ironing Tightness, In-Flight Acoustic Resonant Tap Inspection, Down-Stroke Lifter Retraction, Discharge Starwheel Transfer, High-Speed Defect Chute Purge, Emergency Seamer Jam Safe Brake).
11. ISA-18.2 multi-tiered alarm matrix (Double-seam thickness out-of-spec HH reject, seaming roll bearing overtemperature HH, under-cover gas pressure loss trip, can crash interlock, lube oil pressure drop) with bit-packed telemetry DWORDs.

Ensure exhaustive implementation with zero placeholders, full mathematical expansions, and complete variable declarations."""

def generate_iec_code():
    code_parts = []
    
    # -------------------------------------------------------------
    # 1. HEADER & SYSTEM SPECIFICATION
    # -------------------------------------------------------------
    header = """FUNCTION_BLOCK FB_FoodBev_RotaryCanSeamer_2000CPM_DoubleSeam
(*
========================================================================================================================
LUMINA CYBER-PHYSICAL AUTOMATION ENGINE - SYNTHETIC DATASET V7 MAX-PERSONA
FOOD & BEVERAGE HIGH-SPEED PACKAGING DIVISION - ROTARY BEVERAGE CAN SEAMER (2,000 CANS/MIN)
========================================================================================================================
SYSTEM SPECIFICATION & CYBER-PHYSICAL ARCHITECTURE:
  - Domain: Ultra-High-Speed Rotary Beverage Can Seamer with Dynamic Dual-Roll Seaming & In-Line Acoustic Seal Metrology
  - Machine Kinematics & Throughput:
    * Production Throughput: 2,000 Cans Per Minute (33.3333 Cans/Second, Machine Pitch Cycle Time T_pitch = 30.000 ms)
    * Seamer Carousel: 18 Independent Seaming Stations / Heads on Continuous Pitch Circle (Pitch Diameter D_p = 760.0 mm)
    * Pitch Circumference: 2387.61 mm (Linear Station Pitch = 132.645 mm per pocket)
    * Tangential Pitch Line Velocity: v_pitch = 4.419 m/s at 2,000 cans/min nominal speed
    * Seamer Main Spindle Speed: N_carousel = 111.111 rpm (Angular Velocity omega = 11.6355 rad/s = 666.667 deg/s)
    * Rotation per Station Pitch: theta_pitch = 20.000 deg (360 deg / 18 heads)
  - Container Specifications:
    * Beverage Can Format: 330 mL / 500 mL Sleek & Standard Two-Piece Aluminum Beverage Cans (Alloy 3104-H19)
    * Can Lid / End: 202-Diameter Beverage End (52.4 mm Neck Seaming Diameter, 202 B64 / CDL profile, Alloy 5182-H48)
    * Can Body Wall Thickness: 0.097 mm; End Stock Thickness: 0.220 mm; Flange Width: 2.10 mm +/- 0.10 mm
  - Double Seam Critical Metrology Dimensions (Hermetic Integrity Targets):
    * Finished Seam Thickness: S_th = 1.150 mm +/- 0.030 mm (Nominal 5-layer aluminum metal sandwich + compound)
    * Seam Length / Seam Height: S_len = 2.850 mm +/- 0.075 mm
    * Countersink Depth: C_depth = 2.350 mm +/- 0.080 mm
    * Body Hook Length: BH = 1.450 mm +/- 0.075 mm; End Hook Length: EH = 1.500 mm +/- 0.075 mm
    * Seam Overlap Percentage: OL_pct > 85.0 % (Nominal Overlap Length OL = 1.100 mm)
    * Seam Tightness / Wrinkle Rating: Tightness >= 90.0 % (End hook wrinkle <= 10.0 %)
  - Electrohydraulic / Servo-Cam Dynamic Lifter Subsystem:
    * Dynamic Vertical Preload Force: 1,200 N (initial soft contact) ramping to 2,000 N clamping force against rotating seaming chuck
    * Eliminates can body axial buckling, body wall wrinkling, and beverage slosh spillage during 30 ms cycle
  - Dual-Operation Seaming Cam Kinematics:
    * 1st Operation Roll: Curling profile, folding body hook and end hook into an interlocking seam (850 N to 1,450 N radial force)
    * 2nd Operation Roll: Ironing profile, flattening and compressing seam layers, activating compound hermetic seal (1,400 N to 2,400 N)
  - Under-Cover Inert Gas Gassing (CO2 / Liquid Nitrogen LN2):
    * Closed-loop headspace inerting: Dissolved Oxygen DO < 30 ppb; Internal Target Pressure: 1.20 to 2.50 bar
  - High-Speed In-Flight Acoustic Non-Destructive Inspection:
    * Resonant acoustic impulse tapper at discharge transit: Resonant Lid Frequency Target f_res = 6.850 kHz
    * Decay damping factor zeta = 0.045; Micro-leak / loose cover detection triggers 30 ms high-speed reject puffer
  - Regulatory & Compliance Standards:
    * FDA 21 CFR Part 113 / 114 (Thermally Processed Low-Acid / Acidified Foods in Hermetically Sealed Containers)
    * EHEDG Doc 13 (Hygienic Equipment Design), EHEDG Doc 23 (Aseptic Equipment Testing)
    * 3-A Sanitary Standards 00-01, DIN EN 1672-2 (Food Processing Machinery - Safety and Hygiene Requirements)
    * ISA-18.2 (Management of Alarm Systems for the Process Industries), IEC 61508 / ISO 13849-1 (PLd / Cat 3 Safety)
========================================================================================================================
*)"""
    code_parts.append(header)
    
    # -------------------------------------------------------------
    # 2. VAR_INPUT
    # -------------------------------------------------------------
    var_input = """
VAR_INPUT
    (* Master Execution, Safety & Synchronization Interlocks *)
    bEnable                         : BOOL;     (* Master FB execution enable [BOOL] *)
    bEmergencyStopOk                : BOOL;     (* Redundant dual-channel E-Stop circuit healthy [active HIGH] [BOOL] *)
    bResetAlarms                    : BOOL;     (* Manual trip and fault latch reset request [BOOL] *)
    nMachineModeCmd                 : INT;      (* Operating Mode: 0=SAFE_STOP, 1=JOG_CALIBRATE, 2=HOMING, 3=PRODUCTION_2000CPM, 4=DRAIN_RUNOUT, 5=CLEANING [INT] *)
    bFillerInfeedSyncActive         : BOOL;     (* Upstream high-speed rotary filler electronic gearing lock [BOOL] *)
    rFillerMasterAngle_deg          : REAL;     (* Virtual master electronic line-shaft position from filler [deg] [0.0..360.0 deg] *)
    rFillerMasterVelocity_rpm       : REAL;     (* Filler rotational speed reference [rpm] [0.0..150.0 rpm] *)
    
    (* Master Kinematics & Line Velocity Setpoints *)
    rTargetProductionRate_CPM       : REAL;     (* Target production line throughput [cans/min] [Nominal 2000.0 cans/min] *)
    rMainCarouselVelocity_deg_s     : REAL;     (* Measured carousel rotational velocity [deg/s] [Nominal 666.667 deg/s] *)
    rCanBodyInfeedRate_Hz           : REAL;     (* Infeed starwheel pocket can delivery frequency [Hz] [Nominal 33.333 Hz] *)
    bCanPresenceInfeed              : BOOL;     (* Optical beam sensor for can body presence at infeed pocket [BOOL] *)
    bCanLidPresenceInfeed           : BOOL;     (* Optical / inductive sensor for beverage end lid presence in delivery shoe [BOOL] *)
    
    (* 2oo3 TMR Channel Set 1: Carousel Absolute Rotary Encoders (High-Resolution Multi-Turn Optical Encoders) *)
    rEncPos_Ch1_deg                 : REAL;     (* Carousel Absolute Encoder ENC-01A Position [deg] [0.000..360.000 deg] *)
    rEncPos_Ch2_deg                 : REAL;     (* Carousel Absolute Encoder ENC-01B Position [deg] [0.000..360.000 deg] *)
    rEncPos_Ch3_deg                 : REAL;     (* Carousel Absolute Encoder ENC-01C Position [deg] [0.000..360.000 deg] *)
    bEnc_Ch1_Healthy                : BOOL;     (* ENC-01A SSI communication and optical integrity flag [BOOL] *)
    bEnc_Ch2_Healthy                : BOOL;     (* ENC-01B SSI communication and optical integrity flag [BOOL] *)
    bEnc_Ch3_Healthy                : BOOL;     (* ENC-01C SSI communication and optical integrity flag [BOOL] *)
    
    (* 2oo3 TMR Channel Set 2: Active Seaming Head Dynamic Vertical Lifter Load Cells (Piezoelectric Dynamic Force) *)
    rLifterForce_Ch1_N              : REAL;     (* Active Head Lifter Load Cell LC-01A [N] [Nominal 1200.0..2200.0 N] *)
    rLifterForce_Ch2_N              : REAL;     (* Active Head Lifter Load Cell LC-01B [N] [Nominal 1200.0..2200.0 N] *)
    rLifterForce_Ch3_N              : REAL;     (* Active Head Lifter Load Cell LC-01C [N] [Nominal 1200.0..2200.0 N] *)
    bLifter_Ch1_Healthy             : BOOL;     (* LC-01A sensor bridge excitation and loop integrity [BOOL] *)
    bLifter_Ch2_Healthy             : BOOL;     (* LC-01B sensor bridge excitation and loop integrity [BOOL] *)
    bLifter_Ch3_Healthy             : BOOL;     (* LC-01C sensor bridge excitation and loop integrity [BOOL] *)
    
    (* 2oo3 TMR Channel Set 3: Under-Cover Inert Purge Gas Pressure Transmitters (Piezoresistive Manifold Sensors) *)
    rGasPress_Ch1_bar               : REAL;     (* Under-Cover CO2/LN2 Gas Manifold PT-01A [bar] [Nominal 1.850 bar] *)
    rGasPress_Ch2_bar               : REAL;     (* Under-Cover CO2/LN2 Gas Manifold PT-01B [bar] [Nominal 1.850 bar] *)
    rGasPress_Ch3_bar               : REAL;     (* Under-Cover CO2/LN2 Gas Manifold PT-01C [bar] [Nominal 1.850 bar] *)
    bGasPress_Ch1_Healthy           : BOOL;     (* PT-01A 4-20mA loop integrity and diaphragm health [BOOL] *)
    bGasPress_Ch2_Healthy           : BOOL;     (* PT-01B 4-20mA loop integrity and diaphragm health [BOOL] *)
    bGasPress_Ch3_Healthy           : BOOL;     (* PT-01C 4-20mA loop integrity and diaphragm health [BOOL] *)
    
    (* 2oo3 TMR Channel Set 4: In-Flight Acoustic Seal Resonant Frequency Sensors (Wideband Piezo Accelerometer/Microphone) *)
    rAcousticFreq_Ch1_kHz           : REAL;     (* In-Flight Acoustic Resonance Sensor MIC-01A [kHz] [Nominal 6.850 kHz] *)
    rAcousticFreq_Ch2_kHz           : REAL;     (* In-Flight Acoustic Resonance Sensor MIC-01B [kHz] [Nominal 6.850 kHz] *)
    rAcousticFreq_Ch3_kHz           : REAL;     (* In-Flight Acoustic Resonance Sensor MIC-01C [kHz] [Nominal 6.850 kHz] *)
    bAcoustic_Ch1_Healthy           : BOOL;     (* MIC-01A acoustic transducer health and pre-amp bias [BOOL] *)
    bAcoustic_Ch2_Healthy           : BOOL;     (* MIC-01B acoustic transducer health and pre-amp bias [BOOL] *)
    bAcoustic_Ch3_Healthy           : BOOL;     (* MIC-01C acoustic transducer health and pre-amp bias [BOOL] *)
    
    (* Seaming Roll Mechanical & Thermal Feedbacks *)
    rOp1RollRadialForce_N           : REAL;     (* 1st Operation Roll active radial reaction force [N] [Nominal 1150.0 N] *)
    rOp2RollRadialForce_N           : REAL;     (* 2nd Operation Roll active radial reaction force [N] [Nominal 1850.0 N] *)
    rOp1RollBearingTemp_degC        : REAL;     (* 1st Operation Roll spindle bearing thermocouple [deg C] [Nominal 48.0 deg C] *)
    rOp2RollBearingTemp_degC        : REAL;     (* 2nd Operation Roll spindle bearing thermocouple [deg C] [Nominal 52.0 deg C] *)
    rSeamingChuckTemp_degC          : REAL;     (* Seaming chuck body surface IR pyrometer [deg C] [Nominal 42.0 deg C] *)
    
    (* Lubrication, Pneumatic & Environmental Feedbacks *)
    rLubeOilPressure_bar            : REAL;     (* Central recirculating lube oil pressure transmitter [bar] [Nominal 3.500 bar] *)
    rLubeOilFlow_L_min              : REAL;     (* Central recirculating lube oil flowmeter [L/min] [Nominal 14.50 L/min] *)
    rPneumaticSupplyPressure_bar    : REAL;     (* Main pneumatic valve terminal supply pressure [bar] [Nominal 6.200 bar] *)
    rDissolvedOxygen_ppb            : REAL;     (* In-line optical DO sensor at filler-seamer transfer [ppb] [Target < 30.0 ppb] *)
    rHeadspaceLN2Dose_mg            : REAL;     (* Active liquid nitrogen micro-dosing mass per can [mg] [Target 45.0 mg] *)
    bCanJamStarwheelInfeed          : BOOL;     (* Proximity sensor detecting can body pitch jam at infeed [BOOL] *)
    bCanJamDischargeChute           : BOOL;     (* Optical grid sensor detecting container accumulation at discharge [BOOL] *)
    bRejectBinFull                  : BOOL;     (* Ultrasonic level sensor for defective container reject bin [BOOL] *)
END_VAR"""
    code_parts.append(var_input)

    # -------------------------------------------------------------
    # 3. VAR_OUTPUT
    # -------------------------------------------------------------
    var_output = """
VAR_OUTPUT
    (* Primary System Status & Safety Integrity Flags *)
    bSystemReady                    : BOOL;     (* System interlocks satisfied and ready for high-speed operation [BOOL] *)
    bSeamerSynchronized             : BOOL;     (* Electronic gearing lock verified between seamer and filler [BOOL] *)
    bProductionActive               : BOOL;     (* 2,000 cans/min continuous rotary seaming executing [BOOL] *)
    bEmergencySafeBrakeActive       : BOOL;     (* Emergency safe braking ramp actively decelerating carousel [BOOL] *)
    bSeamerTripped                  : BOOL;     (* Critical safety or process trip latched [active HIGH] [BOOL] *)
    bRejectActuatorFired            : BOOL;     (* High-speed pneumatic rejector pulse active [BOOL] *)
    
    (* State Machine & Diagnostic Sequence Indices *)
    nMachineState                   : INT;      (* Active Seamer 12-stage primary finite state machine index [-] *)
    nMachineSubState                : INT;      (* Active Seamer sub-state machine sequence index [-] *)
    nActiveHeadIndex                : INT;      (* Current seaming head index being monitored [1..18] [-] *)
    
    (* Word-Packed Status and Diagnostic Bitfields *)
    wMachineStatusWord              : WORD;     (* Packed 16-bit seamer operational status word [WORD] *)
    wTMR_SensorHealthWord           : WORD;     (* Packed 16-bit 2oo3 TMR sensor redundancy health bitfield [WORD] *)
    dwAlarmWord_Critical            : DWORD;    (* ISA-18.2 Priority 1 Critical Emergency Trips [DWORD] *)
    dwAlarmWord_Warning             : DWORD;    (* ISA-18.2 Priority 2 Operational Warnings [DWORD] *)
    dwAlarmWord_Advisory            : DWORD;    (* ISA-18.2 Priority 3 Preventative Maintenance Advisories [DWORD] *)
    
    (* High-Speed Actuator Velocity, Torque & Position Commands *)
    rCarouselSpeedRef_deg_s         : REAL;     (* Main carousel synchronized servo velocity reference [deg/s] *)
    rCarouselTorqueCmd_Nm           : REAL;     (* Main carousel direct-drive motor torque command [Nm] *)
    rLifterServoPosCmd_mm           : REAL;     (* Active lifter plate dynamic vertical servo position command [mm] *)
    rLifterServoForceRef_N          : REAL;     (* Active lifter plate closed-loop vertical force setpoint [N] *)
    rOp1RollCamTrim_mm              : REAL;     (* 1st Operation Roll servo-eccentric radial position trim [mm] *)
    rOp2RollCamTrim_mm              : REAL;     (* 2nd Operation Roll servo-eccentric radial position trim [mm] *)
    rUnderCoverCO2ValvePctCmd       : REAL;     (* Under-cover CO2 purge gas proportional valve setpoint [0.0..100.0 %] *)
    rLN2DoserPulseDuration_ms       : REAL;     (* Liquid nitrogen cryogenic injector pulse width command [ms] *)
    bAcousticTapperPulseCmd         : BOOL;     (* High-speed solenoid impulse tapper trigger pulse [BOOL] *)
    bPneumaticRejectPufferCmd       : BOOL;     (* High-speed defective container blow-off reject solenoid [BOOL] *)
    
    (* Seam Metrology & Quality Assurance Telemetry *)
    rMeasuredSeamThickness_mm       : REAL;     (* Voted double seam thickness estimate for active can [mm] *)
    rMeasuredCountersink_mm         : REAL;     (* Voted countersink depth estimate for active can [mm] *)
    rCalculatedSeamOverlap_pct      : REAL;     (* Estimated seam overlap percentage based on roll forces [%] *)
    rMeasuredAcousticResonance_kHz  : REAL;     (* In-flight acoustic resonant lid vibration peak frequency [kHz] *)
    rAcousticDecayQFactor           : REAL;     (* Acoustic resonance quality factor Q = f_res / delta_f [-] *)
    rHeadspacePressureEst_bar       : REAL;     (* Estimated sealed container internal headspace pressure [bar] *)
    rDissolvedOxygenEst_ppb         : REAL;     (* Estimated sealed container dissolved oxygen concentration [ppb] *)
    
    (* Production Performance & Quality Statistical Counters *)
    rInstantThroughput_CPM          : REAL;     (* Instantaneous measured production throughput [cans/min] *)
    udiCansSeamedTotal              : UDINT;    (* Cumulative good hermetically sealed container counter [UDINT] *)
    udiCansRejectedTotal            : UDINT;    (* Cumulative defective container reject counter [UDINT] *)
    udiAcousticDefectCount          : UDINT;    (* Counter of containers rejected for acoustic frequency out-of-spec [UDINT] *)
    udiForceDefectCount             : UDINT;    (* Counter of containers rejected for abnormal seaming force profile [UDINT] *)
END_VAR"""
    code_parts.append(var_output)

    # -------------------------------------------------------------
    # 4. VAR - CYBER-PHYSICAL MATRICES & INTERNAL VARIABLES
    # -------------------------------------------------------------
    var_internal = """
VAR
    (* ================================================================================================================ *)
    (* INTERNAL CYBER-PHYSICAL STATE-SPACE MATRICES & OBSERVER STRUCTURES (16x16 DISCRETE FORMULATION, Ts = 2.0 ms)      *)
    (* States x:                                                                                                        *)
    (*   x[1]:  Carousel angular position deviation Delta theta_car [rad]                                               *)
    (*   x[2]:  Carousel angular velocity deviation Delta omega_car [rad/s]                                             *)
    (*   x[3]:  Lifter plate vertical displacement z_lift [mm]                                                          *)
    (*   x[4]:  Lifter plate vertical velocity dz_lift/dt [mm/s]                                                        *)
    (*   x[5]:  Lifter plate contact preload force F_lift [N]                                                           *)
    (*   x[6]:  Lifter electrohydraulic/servo chamber pressure P_hyd [bar]                                              *)
    (*   x[7]:  Operation 1 seaming roll radial position r_op1 [mm]                                                     *)
    (*   x[8]:  Operation 1 seaming roll radial velocity dr_op1/dt [mm/s]                                               *)
    (*   x[9]:  Operation 1 seaming contact radial force F_rad_op1 [N]                                                  *)
    (*   x[10]: Operation 2 seaming roll radial position r_op2 [mm]                                                     *)
    (*   x[11]: Operation 2 seaming roll radial velocity dr_op2/dt [mm/s]                                               *)
    (*   x[12]: Operation 2 seaming ironing contact force F_rad_op2 [N]                                                 *)
    (*   x[13]: Can body elastic curl deformation delta_curl [mm]                                                       *)
    (*   x[14]: Can end hook flange compression delta_hook [mm]                                                         *)
    (*   x[15]: Headspace under-cover gas pressure P_head [bar]                                                         *)
    (*   x[16]: Headspace dissolved oxygen concentration C_DO [ppb]                                                     *)
    (*                                                                                                                  *)
    (* Inputs u (8 Actuators):                                                                                          *)
    (*   u[1]: Carousel main direct-drive torque command tau_car [Nm]                                                   *)
    (*   u[2]: Lifter plate electrohydraulic/servo valve command u_lift [%]                                             *)
    (*   u[3]: Operation 1 roll servo cam position trim Delta r_cam1 [mm]                                              *)
    (*   u[4]: Operation 2 roll servo cam position trim Delta r_cam2 [mm]                                              *)
    (*   u[5]: Under-cover CO2 purge gas proportional valve u_CO2 [%]                                                   *)
    (*   u[6]: Liquid nitrogen (LN2) cryogenic doser pulse duration u_LN2 [ms]                                          *)
    (*   u[7]: Acoustic inspection piezo tap impact pulse energy u_tap [%]                                              *)
    (*   u[8]: High-speed pneumatic rejector air pulse duration u_rej [ms]                                              *)
    (* ================================================================================================================ *)
    rMatA                           : ARRAY[1..16, 1..16] OF REAL; (* Discrete State Transition Matrix A (Ts = 2.0 ms) *)
    rMatB                           : ARRAY[1..16, 1..8] OF REAL;  (* Discrete Control Input Gain Matrix B *)
    rMatC                           : ARRAY[1..16, 1..16] OF REAL; (* Discrete Measurement Coupling Matrix C *)
    rMatD                           : ARRAY[1..16, 1..8] OF REAL;  (* Direct Feedthrough Transmission Matrix D *)
    rMatL                           : ARRAY[1..16, 1..16] OF REAL; (* Luenberger / Steady-State Kalman Observer Gain L *)
    
    rVecX                           : ARRAY[1..16] OF REAL;       (* Filtered Estimated Internal State Vector x[k] *)
    rVecX_Next                      : ARRAY[1..16] OF REAL;       (* One-Step Ahead Predicted State Vector x[k+1] *)
    rVecU                           : ARRAY[1..8] OF REAL;        (* Current Plant Control Input Vector u[k] *)
    rVecU_Prev                      : ARRAY[1..8] OF REAL;        (* Previous Cycle Control Input Vector u[k-1] *)
    rVecY_Est                       : ARRAY[1..16] OF REAL;       (* Estimated Output Vector y_est[k] = C*x[k] + D*u[k] *)
    rVecY_Meas                      : ARRAY[1..16] OF REAL;       (* Voted Physical Measurement Vector y_meas[k] *)
    rVecY_Err                       : ARRAY[1..16] OF REAL;       (* Innovation Residual Vector e_y = y_meas - y_est *)
    rVecX_Ref                       : ARRAY[1..16] OF REAL;       (* Reference Setpoint State Vector x_ref *)

    (* ================================================================================================================ *)
    (* RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) MATRICES & OPTIMIZATION HORIZON (Np = 5 Steps)                   *)
    (* ================================================================================================================ *)
    rMatQ                           : ARRAY[1..16, 1..16] OF REAL; (* State Tracking Error Weight Matrix Q *)
    rMatR                           : ARRAY[1..8, 1..8] OF REAL;   (* Actuator Slew Rate Energy Penalty Matrix R *)
    rMatP                           : ARRAY[1..16, 1..16] OF REAL; (* Terminal State Cost Matrix P (Discrete ARE Solution) *)
    
    rPredX                          : ARRAY[1..5, 1..16] OF REAL; (* Multi-Step State Trajectory Prediction [Step, State] *)
    rOptU                           : ARRAY[1..5, 1..8] OF REAL;  (* Optimized Control Trajectory Candidate [Step, Input] *)
    rDeltaU                         : ARRAY[1..5, 1..8] OF REAL;  (* Control Rate of Change Candidate *)
    rGradJ                          : ARRAY[1..8] OF REAL;        (* Numerical Gradient of Cost with respect to u[k] *)
    rU_Min                          : ARRAY[1..8] OF REAL;        (* Actuator Lower Physical Saturation Limits *)
    rU_Max                          : ARRAY[1..8] OF REAL;        (* Actuator Upper Physical Saturation Limits *)
    rRateLimit_U                    : ARRAY[1..8] OF REAL;        (* Maximum Allowable Actuator Slew Rate [units/s] *)
    
    rCostJ                          : REAL;                       (* Instantaneous Evaluated Objective Value J *)
    rMinCostJ                       : REAL;                       (* Best Minimum Cost in Iterative Gradient Search *)
    rMPC_StepSize                   : REAL := 0.0125;             (* Projected Gradient Descent Learning Rate *)
    nMPC_Iter                       : INT;                        (* Active MPC Optimization Iteration Loop Index *)
    nHorizStep                      : INT;                        (* Prediction Horizon Step Index (1..5) *)

    (* ================================================================================================================ *)
    (* 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) ARCHITECTURE & DISCREPANCY TIMERS                                            *)
    (* ================================================================================================================ *)
    (* Channel Set 1: Carousel Absolute Rotary Encoders *)
    rEnc_Tol_deg                    : REAL := 0.150;              (* Permissible Intersensor Deviation Tolerance [deg] *)
    rEncPos_Voted_deg               : REAL;                       (* 2oo3 Synthesized Voted Position [deg] *)
    bEncDiscrep_12                  : BOOL;                       (* Discrepancy Flag ENC-01A vs ENC-01B *)
    bEncDiscrep_23                  : BOOL;                       (* Discrepancy Flag ENC-01B vs ENC-01C *)
    bEncDiscrep_13                  : BOOL;                       (* Discrepancy Flag ENC-01A vs ENC-01C *)
    tEncDiscrep_12_TON              : TON;                        (* Discrepancy Qualification Timer 1 vs 2 (10 ms) *)
    tEncDiscrep_23_TON              : TON;                        (* Discrepancy Qualification Timer 2 vs 3 (10 ms) *)
    tEncDiscrep_13_TON              : TON;                        (* Discrepancy Qualification Timer 1 vs 3 (10 ms) *)
    nEnc_HealthyCount               : INT;                        (* Count of Functioning Verified Encoders (0..3) *)
    bEnc_TMR_Degraded               : BOOL;                       (* Operating in Degraded Encoder Redundancy Mode *)
    bEnc_TMR_Tripped                : BOOL;                       (* All Encoder Channels Failed / Irreconcilable *)

    (* Channel Set 2: Active Seaming Head Dynamic Lifter Load Cells *)
    rLifter_Tol_N                   : REAL := 75.0;               (* Permissible Intersensor Force Deviation [N] *)
    rLifterForce_Voted_N            : REAL;                       (* 2oo3 Synthesized Voted Lifter Preload Force [N] *)
    bLifterDiscrep_12               : BOOL;                       (* Discrepancy Flag LC-01A vs LC-01B *)
    bLifterDiscrep_23               : BOOL;                       (* Discrepancy Flag LC-01B vs LC-01C *)
    bLifterDiscrep_13               : BOOL;                       (* Discrepancy Flag LC-01A vs LC-01C *)
    tLifterDiscrep_12_TON           : TON;                        (* Discrepancy Qualification Timer 1 vs 2 (15 ms) *)
    tLifterDiscrep_23_TON           : TON;                        (* Discrepancy Qualification Timer 2 vs 3 (15 ms) *)
    tLifterDiscrep_13_TON           : TON;                        (* Discrepancy Qualification Timer 1 vs 3 (15 ms) *)
    nLifter_HealthyCount            : INT;                        (* Count of Verified Active Load Cells (0..3) *)
    bLifter_TMR_Degraded            : BOOL;                       (* Degraded Lifter Force Sensing Mode *)
    bLifter_TMR_Tripped             : BOOL;                       (* Lifter Load Redundancy Failure *)

    (* Channel Set 3: Under-Cover Inert Purge Gas Pressure Transmitters *)
    rGasPress_Tol_bar               : REAL := 0.120;              (* Permissible Gas Pressure Deviation [bar] *)
    rGasPress_Voted_bar             : REAL;                       (* 2oo3 Synthesized Voted Gas Pressure [bar] *)
    bGasDiscrep_12                  : BOOL;                       (* Discrepancy Flag PT-01A vs PT-01B *)
    bGasDiscrep_23                  : BOOL;                       (* Discrepancy Flag PT-01B vs PT-01C *)
    bGasDiscrep_13                  : BOOL;                       (* Discrepancy Flag PT-01A vs PT-01C *)
    tGasDiscrep_12_TON              : TON;                        (* Discrepancy Qualification Timer 1 vs 2 (25 ms) *)
    tGasDiscrep_23_TON              : TON;                        (* Discrepancy Qualification Timer 2 vs 3 (25 ms) *)
    tGasDiscrep_13_TON              : TON;                        (* Discrepancy Qualification Timer 1 vs 3 (25 ms) *)
    nGasPress_HealthyCount          : INT;                        (* Count of Healthy Gas Transmitters (0..3) *)
    bGasPress_TMR_Degraded          : BOOL;                       (* Degraded Gas Sensing Redundancy Mode *)
    bGasPress_TMR_Tripped           : BOOL;                       (* All Gas Transmitters Failed *)

    (* Channel Set 4: In-Flight Acoustic Resonant Frequency Spectrum Sensors *)
    rAcoustic_Tol_kHz               : REAL := 0.250;              (* Permissible Resonance Intersensor Deviation [kHz] *)
    rAcousticFreq_Voted_kHz         : REAL;                       (* 2oo3 Synthesized Voted Lid Frequency [kHz] *)
    bAcousticDiscrep_12             : BOOL;                       (* Discrepancy Flag MIC-01A vs MIC-01B *)
    bAcousticDiscrep_23             : BOOL;                       (* Discrepancy Flag MIC-01B vs MIC-01C *)
    bAcousticDiscrep_13             : BOOL;                       (* Discrepancy Flag MIC-01A vs MIC-01C *)
    tAcousticDiscrep_12_TON         : TON;                        (* Discrepancy Qualification Timer 1 vs 2 (20 ms) *)
    tAcousticDiscrep_23_TON         : TON;                        (* Discrepancy Qualification Timer 2 vs 3 (20 ms) *)
    tAcousticDiscrep_13_TON         : TON;                        (* Discrepancy Qualification Timer 1 vs 3 (20 ms) *)
    nAcoustic_HealthyCount          : INT;                        (* Count of Verified Acoustic Channels (0..3) *)
    bAcoustic_TMR_Degraded          : BOOL;                       (* Degraded Acoustic Inspection Flag *)
    bAcoustic_TMR_Tripped           : BOOL;                       (* Acoustic Inspection Multi-Channel Failure *)

    (* ================================================================================================================ *)
    (* DIGITAL SIGNAL CONDITIONING: 2ND-ORDER BUTTERWORTH IIR LOW-PASS FILTERS (fc = 40.0 Hz, Ts = 2.0 ms)              *)
    (* ================================================================================================================ *)
    rFiltCoeff_b0                   : REAL := 0.048705;           (* Filter Numerator Coefficient b0 *)
    rFiltCoeff_b1                   : REAL := 0.097410;           (* Filter Numerator Coefficient b1 *)
    rFiltCoeff_b2                   : REAL := 0.048705;           (* Filter Numerator Coefficient b2 *)
    rFiltCoeff_a1                   : REAL := -1.297017;          (* Filter Denominator Coefficient a1 *)
    rFiltCoeff_a2                   : REAL := 0.491837;           (* Filter Denominator Coefficient a2 *)
    
    (* Filter Past Histories: Index 1=LifterForce, 2=GasPress, 3=Op1Force, 4=Op2Force, 5=ChuckTemp, 6=LubePress, 7=DO, 8=EncPos *)
    rFilt_x1                        : ARRAY[1..8] OF REAL;        (* Input history x[k-1] *)
    rFilt_x2                        : ARRAY[1..8] OF REAL;        (* Input history x[k-2] *)
    rFilt_y1                        : ARRAY[1..8] OF REAL;        (* Output history y[k-1] *)
    rFilt_y2                        : ARRAY[1..8] OF REAL;        (* Output history y[k-2] *)
    rFilt_Out                       : ARRAY[1..8] OF REAL;        (* Filtered Current Output y[k] *)

    (* ================================================================================================================ *)
    (* 18 SEAMING HEAD INDIVIDUAL TELEMETRY & STATISTICAL PROCESS CONTROL (SPC) ARRAYS                                  *)
    (* ================================================================================================================ *)
    aHeadSeamThickness_mm           : ARRAY[1..18] OF REAL;       (* Historical Rolling Average Seam Thickness per Head [mm] *)
    aHeadCountersinkDepth_mm        : ARRAY[1..18] OF REAL;       (* Historical Rolling Average Countersink per Head [mm] *)
    aHeadAcousticResonance_kHz      : ARRAY[1..18] OF REAL;       (* Historical Rolling Acoustic Resonant Peak per Head [kHz] *)
    aHeadBearingTemp_degC           : ARRAY[1..18] OF REAL;       (* Temperature Monitor per Seaming Head Spindle [deg C] *)
    aHeadPeakLifterForce_N          : ARRAY[1..18] OF REAL;       (* Maximum Vertical Force Registered During Cycle [N] *)
    aHeadPeakOp1Force_N             : ARRAY[1..18] OF REAL;       (* Maximum Op 1 Curling Radial Force Registered [N] *)
    aHeadPeakOp2Force_N             : ARRAY[1..18] OF REAL;       (* Maximum Op 2 Ironing Radial Force Registered [N] *)
    aHeadFaultStatusBits            : ARRAY[1..18] OF WORD;       (* Station-Specific Defect and Wear Diagnostic Word *)

    (* High-Speed FIFO Defect Tracking Shift Register (144 Physical Stations from Infeed to Chute) *)
    aContainerTrackingFIFO          : ARRAY[1..144] OF DWORD;     (* Shift Register: Bit 0=Reject, Bit 1=Acoustic, Bit 2=Force, Bit 3=Gas *)
    nTrackingShiftPointer           : INT := 1;                   (* Current Head Handshake Index *)
    bStationRejectFlag              : BOOL;                       (* Active Defect Flag for Discharge Reject Station *)

    (* Dynamic Electronic Cam Profile Curves for 360-degree Carousel Pitch *)
    rCamAngle_deg                   : REAL;                       (* Local Station Cam Angle [0.0..360.0 deg] *)
    rLifterNominalStroke_mm         : REAL;                       (* Nominal Lifter Height along Cam Curve [mm] *)
    rOp1NominalRadius_mm            : REAL;                       (* Nominal Op 1 Roll Radial Position [mm] *)
    rOp2NominalRadius_mm            : REAL;                       (* Nominal Op 2 Roll Radial Position [mm] *)

    (* ================================================================================================================ *)
    (* FINITE STATE MACHINE (FSM) TIMERS, FLAGS & SUB-STATES                                                            *)
    (* ================================================================================================================ *)
    tStateTimer                     : TON;                        (* Dwell Timer for Current Primary FSM State *)
    tSubStateTimer                  : TON;                        (* Dwell Timer for Current Sub-State *)
    tEmergencyBrakeTimer            : TON;                        (* Dynamic Braking Ramp Qualification Timer *)
    bStateFirstScan                 : BOOL := TRUE;               (* Edge Trigger Flag on Primary State Change *)
    bSubStateFirstScan              : BOOL := TRUE;               (* Edge Trigger Flag on Sub-State Change *)
    nPreviousState                  : INT := -1;                  (* State Memory for Edge Detection *)

    (* ================================================================================================================ *)
    (* ISA-18.2 MULTI-TIERED ALARM SETPOINTS, DEADBANDS & ESCALATION TIMERS                                              *)
    (* ================================================================================================================ *)
    (* Seam Thickness Limits [mm] (Nominal 1.150 mm) *)
    rSeamThick_Limit_HH_mm          : REAL := 1.250;              (* High-High Critical Trip: Incomplete Seam / Loose Flange *)
    rSeamThick_Limit_H_mm           : REAL := 1.180;              (* High Warning: Approaching Upper Tolerance Band *)
    rSeamThick_Limit_L_mm           : REAL := 1.120;              (* Low Warning: Approaching Lower Tolerance Band *)
    rSeamThick_Limit_LL_mm          : REAL := 1.050;              (* Low-Low Critical Trip: Over-Ironing / Cut Seam Hazard *)
    rSeamThick_Deadband_mm          : REAL := 0.010;              (* Reset Hysteresis Deadband [mm] *)

    (* Countersink Depth Limits [mm] (Nominal 2.350 mm) *)
    rCountersink_Limit_HH_mm        : REAL := 2.650;              (* High-High Trip: Chuck Slippage / End Panel Distortion *)
    rCountersink_Limit_H_mm         : REAL := 2.450;              (* High Warning *)
    rCountersink_Limit_L_mm         : REAL := 2.250;              (* Low Warning *)
    rCountersink_Limit_LL_mm        : REAL := 2.050;              (* Low-Low Trip: Inadequate Chuck Seating *)
    rCountersink_Deadband_mm        : REAL := 0.020;              (* Reset Hysteresis Deadband [mm] *)

    (* Seaming Roll Bearing Overtemperature [deg C] (Nominal 50.0 deg C) *)
    rRollTemp_Limit_HH_degC         : REAL := 85.0;               (* High-High Critical Trip: Bearing Spalling / Seizure Hazard *)
    rRollTemp_Limit_H_degC          : REAL := 70.0;               (* High Warning: Lubrication Degradation *)
    rRollTemp_Deadband_degC         : REAL := 3.0;                (* Reset Hysteresis Deadband [deg C] *)

    (* Under-Cover Gas Purge Pressure Limits [bar] (Nominal 1.850 bar) *)
    rGasPress_Limit_HH_bar          : REAL := 2.600;              (* High-High Trip: Gas Manifold Regulator Overpressure *)
    rGasPress_Limit_H_bar           : REAL := 2.200;              (* High Warning *)
    rGasPress_Limit_L_bar           : REAL := 1.400;              (* Low Warning: Inadequate Headspace Inerting *)
    rGasPress_Limit_LL_bar          : REAL := 1.100;              (* Low-Low Critical Trip: Headspace DO Hazard *)
    rGasPress_Deadband_bar          : REAL := 0.050;              (* Reset Hysteresis Deadband [bar] *)

    (* Lifter Vertical Dynamic Force Limits [N] (Nominal Clamping 2000.0 N) *)
    rLifterForce_Limit_HH_N         : REAL := 2600.0;             (* High-High Trip: Can Body Crush / Axial Buckling Hazard *)
    rLifterForce_Limit_H_N          : REAL := 2300.0;             (* High Warning *)
    rLifterForce_Limit_L_N          : REAL := 1100.0;             (* Low Warning: Inadequate Chuck Grip / Can Slipping *)
    rLifterForce_Limit_LL_N         : REAL := 900.0;              (* Low-Low Trip: Lifter Drop-Out / Missing Can *)
    rLifterForce_Deadband_N         : REAL := 50.0;               (* Reset Hysteresis Deadband [N] *)

    (* Acoustic Resonant Lid Frequency Limits [kHz] (Nominal 6.850 kHz) *)
    rAcoustic_Limit_HH_kHz          : REAL := 7.600;              (* High-High Trip: Excessive Can Internal Pressure / Over-Dose *)
    rAcoustic_Limit_H_kHz           : REAL := 7.200;              (* High Warning *)
    rAcoustic_Limit_L_kHz           : REAL := 6.400;              (* Low Warning: Flange Leak / Low Pressure *)
    rAcoustic_Limit_LL_kHz          : REAL := 5.950;              (* Low-Low Critical Trip: Severe Micro-Leak / Loose Seam *)
    rAcoustic_Deadband_kHz          : REAL := 0.080;              (* Reset Hysteresis Deadband [kHz] *)

    (* Central Recirculating Lube Oil Pressure Limits [bar] (Nominal 3.500 bar) *)
    rLubePress_Limit_HH_bar         : REAL := 5.000;              (* High-High Trip: Filter Blockage *)
    rLubePress_Limit_H_bar          : REAL := 4.200;              (* High Warning *)
    rLubePress_Limit_L_bar          : REAL := 2.400;              (* Low Warning: Pump Cavitation / Filter Contamination *)
    rLubePress_Limit_LL_bar         : REAL := 1.800;              (* Low-Low Critical Trip: Spindle Starvation Hazard *)
    rLubePress_Deadband_bar         : REAL := 0.150;              (* Reset Hysteresis Deadband [bar] *)

    (* Alarm Escalation Timers (Priority 2 Warning -> Priority 1 Trip after 8.0 s Unacknowledged Dwell) *)
    tWarningEscalation_TON          : TON;                        (* 8.0 s Warning Unacknowledged Escalation Timer *)
    rEscalationTimeout_s            : REAL := 8.00;               (* Timeout to Trip Escalation Window [s] *)
    
    (* General Calculation Registers & Loop Counters *)
    iIdx                            : INT;                        (* General Matrix Row Index [1..16] *)
    jIdx                            : INT;                        (* General Matrix Column Index [1..16] *)
    kIdx                            : INT;                        (* General Prediction Horizon Step Index [1..5] *)
    mIdx                            : INT;                        (* General Actuator Input Index [1..8] *)
    hIdx                            : INT;                        (* Head Index Counter [1..18] *)
    rTempScalar                     : REAL;                       (* Scratch Computational Scalar *)
    rTempDelta                      : REAL;                       (* Scratch Difference Variable *)
    bInitDone                       : BOOL := FALSE;              (* Global Cold-Start Initialization Done Flag *)
END_VAR"""
    code_parts.append(var_internal)

    # -------------------------------------------------------------
    # 5. FIRST SCAN INITIALIZATION
    # -------------------------------------------------------------
    init_code = """
(*
========================================================================================================================
COLD-START SYSTEM INITIALIZATION (FIRST SCAN EXECUTION)
========================================================================================================================
*)
IF NOT bInitDone THEN
    (* 1. Initialize Discrete 16x16 State Transition Matrix A (Sample Time Ts = 2.0 ms = 0.002 s) *)
    (* Row 1..16 initialization incorporating carousel inertia, lifter elastodynamics, roll contact, and gas physics *)
    FOR iIdx := 1 TO 16 DO
        FOR jIdx := 1 TO 16 DO
            rMatA[iIdx, jIdx] := 0.0000;
        END_FOR;
    END_FOR;

    (* Diagonal state persistence terms (Ts = 2 ms discretization) *)
    rMatA[1, 1] := 0.9985;  rMatA[1, 2] := 0.0020;  (* Delta theta_car <- Delta theta + Ts*omega *)
    rMatA[2, 1] := -0.0150; rMatA[2, 2] := 0.9820;  (* Delta omega_car carousel inertia damping *)
    rMatA[3, 3] := 0.9750;  rMatA[3, 4] := 0.0019;  (* Lifter vertical position z_lift *)
    rMatA[4, 3] := -0.0450; rMatA[4, 4] := 0.9200;  rMatA[4, 5] := -0.0008; rMatA[4, 6] := 0.0140; (* Lifter dz/dt *)
    rMatA[5, 3] := 12.400;  rMatA[5, 4] := 0.8500;  rMatA[5, 5] := 0.8850;  (* Lifter contact force F_lift [N] *)
    rMatA[6, 6] := 0.9150;  (* Lifter hydraulic pressure P_hyd [bar] *)
    rMatA[7, 7] := 0.9650;  rMatA[7, 8] := 0.0018;  (* Op 1 Roll radial position r_op1 *)
    rMatA[8, 7] := -0.0820; rMatA[8, 8] := 0.8950;  rMatA[8, 9] := -0.0012; (* Op 1 Roll velocity dr_op1/dt *)
    rMatA[9, 7] := 18.500;  rMatA[9, 8] := 1.2500;  rMatA[9, 9] := 0.8400;  rMatA[9, 13] := 0.4500; (* Op 1 force *)
    rMatA[10, 10] := 0.9620; rMatA[10, 11] := 0.0018; (* Op 2 Roll radial position r_op2 *)
    rMatA[11, 10] := -0.0950; rMatA[11, 11] := 0.8900; rMatA[11, 12] := -0.0015; (* Op 2 Roll velocity dr_op2/dt *)
    rMatA[12, 10] := 24.200;  rMatA[12, 11] := 1.6500; rMatA[12, 12] := 0.8100; rMatA[12, 14] := 0.6200; (* Op 2 force *)
    rMatA[13, 9] := 0.0004;   rMatA[13, 13] := 0.9350; (* Body hook curl deformation delta_curl *)
    rMatA[14, 12] := 0.0005;  rMatA[14, 14] := 0.9200; (* End hook flange compression delta_hook *)
    rMatA[15, 15] := 0.9450;  rMatA[15, 16] := -0.0002; (* Headspace pressure P_head [bar] *)
    rMatA[16, 15] := -0.0120; rMatA[16, 16] := 0.9100; (* Headspace dissolved oxygen C_DO [ppb] *)

    (* 2. Initialize Discrete 16x8 Input Control Gain Matrix B *)
    FOR iIdx := 1 TO 16 DO
        FOR jIdx := 1 TO 8 DO
            rMatB[iIdx, jIdx] := 0.0000;
        END_FOR;
    END_FOR;
    rMatB[2, 1] := 0.0480;  (* u[1] tau_car -> Delta omega_car *)
    rMatB[4, 2] := 0.0850;  (* u[2] u_lift -> lifter velocity *)
    rMatB[6, 2] := 0.1250;  (* u[2] u_lift -> lifter pressure *)
    rMatB[8, 3] := 0.1100;  (* u[3] Delta r_cam1 -> Op 1 roll velocity *)
    rMatB[11, 4] := 0.1350; (* u[4] Delta r_cam2 -> Op 2 roll velocity *)
    rMatB[15, 5] := 0.0350; (* u[5] u_CO2 -> headspace pressure *)
    rMatB[15, 6] := 0.0620; (* u[6] u_LN2 -> headspace pressure *)
    rMatB[16, 5] := -0.2800; (* u[5] u_CO2 -> headspace DO reduction *)
    rMatB[16, 6] := -0.4200; (* u[6] u_LN2 -> headspace DO reduction *)

    (* 3. Initialize Discrete 16x16 Measurement Matrix C (Identity Scaled) *)
    FOR iIdx := 1 TO 16 DO
        FOR jIdx := 1 TO 16 DO
            IF iIdx = jIdx THEN
                rMatC[iIdx, jIdx] := 1.0000;
            ELSE
                rMatC[iIdx, jIdx] := 0.0000;
            END_IF;
        END_FOR;
    END_FOR;

    (* 4. Initialize Direct Feedthrough Matrix D (Zero Matrix 16x8) *)
    FOR iIdx := 1 TO 16 DO
        FOR jIdx := 1 TO 8 DO
            rMatD[iIdx, jIdx] := 0.0000;
        END_FOR;
    END_FOR;

    (* 5. Initialize Luenberger Observer Gain Matrix L (16x16) *)
    FOR iIdx := 1 TO 16 DO
        FOR jIdx := 1 TO 16 DO
            rMatL[iIdx, jIdx] := 0.0000;
        END_FOR;
    END_FOR;
    rMatL[1, 1] := 0.3800;  rMatL[2, 2] := 0.4200;
    rMatL[3, 3] := 0.4500;  rMatL[4, 4] := 0.3900;
    rMatL[5, 5] := 0.5200;  rMatL[6, 6] := 0.3400;
    rMatL[7, 7] := 0.4600;  rMatL[8, 8] := 0.4100;
    rMatL[9, 9] := 0.5500;  rMatL[10, 10] := 0.4800;
    rMatL[11, 11] := 0.4300; rMatL[12, 12] := 0.5800;
    rMatL[13, 13] := 0.3100; rMatL[14, 14] := 0.3200;
    rMatL[15, 15] := 0.4900; rMatL[16, 16] := 0.5100;

    (* 6. Initialize MPC Quadratic State Penalty Matrix Q (16x16) *)
    FOR iIdx := 1 TO 16 DO
        FOR jIdx := 1 TO 16 DO
            rMatQ[iIdx, jIdx] := 0.0000;
        END_FOR;
    END_FOR;
    rMatQ[1, 1] := 45.00;   rMatQ[2, 2] := 35.00;   (* Carousel position & speed *)
    rMatQ[3, 3] := 60.00;   rMatQ[4, 4] := 25.00;   (* Lifter position & velocity *)
    rMatQ[5, 5] := 85.00;   rMatQ[6, 6] := 20.00;   (* Lifter clamping force & hyd press *)
    rMatQ[7, 7] := 75.00;   rMatQ[8, 8] := 30.00;   (* Op 1 roll radial position & vel *)
    rMatQ[9, 9] := 95.00;                           (* Op 1 curling reaction force *)
    rMatQ[10, 10] := 80.00; rMatQ[11, 11] := 30.00; (* Op 2 roll radial position & vel *)
    rMatQ[12, 12] := 110.0;                         (* Op 2 ironing reaction force *)
    rMatQ[13, 13] := 90.00; rMatQ[14, 14] := 105.0; (* Seam body and end hook overlaps *)
    rMatQ[15, 15] := 55.00; rMatQ[16, 16] := 70.00; (* Headspace pressure and DO content *)

    (* 7. Initialize MPC Actuator Slew Rate Penalty Matrix R (8x8) *)
    FOR iIdx := 1 TO 8 DO
        FOR jIdx := 1 TO 8 DO
            rMatR[iIdx, jIdx] := 0.0000;
        END_FOR;
    END_FOR;
    rMatR[1, 1] := 2.500;   (* Carousel torque slew penalty *)
    rMatR[2, 2] := 3.200;   (* Lifter valve rate penalty *)
    rMatR[3, 3] := 4.800;   (* Op 1 cam trim rate penalty *)
    rMatR[4, 4] := 5.200;   (* Op 2 cam trim rate penalty *)
    rMatR[5, 5] := 1.800;   (* CO2 valve rate penalty *)
    rMatR[6, 6] := 2.100;   (* LN2 doser rate penalty *)
    rMatR[7, 7] := 0.500;   (* Acoustic tapper rate penalty *)
    rMatR[8, 8] := 0.800;   (* Reject puffer rate penalty *)

    (* 8. Initialize Terminal State Cost Matrix P (16x16) *)
    FOR iIdx := 1 TO 16 DO
        FOR jIdx := 1 TO 16 DO
            rMatP[iIdx, jIdx] := rMatQ[iIdx, jIdx] * 2.450;
        END_FOR;
    END_FOR;

    (* 9. Initialize Actuator Lower and Upper Physical Limits *)
    rU_Min[1] := -150.0;  rU_Max[1] := 150.0;  rRateLimit_U[1] := 450.0;  (* tau_car [Nm], max 450 Nm/s *)
    rU_Min[2] := 0.0;     rU_Max[2] := 100.0;  rRateLimit_U[2] := 200.0;  (* u_lift [%], max 200 %/s *)
    rU_Min[3] := -0.500;  rU_Max[3] := 0.500;  rRateLimit_U[3] := 5.000;  (* Delta r_cam1 [mm], max 5 mm/s *)
    rU_Min[4] := -0.500;  rU_Max[4] := 0.500;  rRateLimit_U[4] := 5.000;  (* Delta r_cam2 [mm], max 5 mm/s *)
    rU_Min[5] := 0.0;     rU_Max[5] := 100.0;  rRateLimit_U[5] := 150.0;  (* u_CO2 [%], max 150 %/s *)
    rU_Min[6] := 0.0;     rU_Max[6] := 12.00;  rRateLimit_U[6] := 60.0;   (* u_LN2 [ms], max 60 ms/s *)
    rU_Min[7] := 0.0;     rU_Max[7] := 100.0;  rRateLimit_U[7] := 500.0;  (* u_tap [%], max 500 %/s *)
    rU_Min[8] := 0.0;     rU_Max[8] := 50.00;  rRateLimit_U[8] := 250.0;  (* u_rej [ms], max 250 ms/s *)

    (* 10. Initialize 18 Seaming Head Historical Records *)
    FOR hIdx := 1 TO 18 DO
        aHeadSeamThickness_mm[hIdx] := 1.150;
        aHeadCountersinkDepth_mm[hIdx] := 2.350;
        aHeadAcousticResonance_kHz[hIdx] := 6.850;
        aHeadBearingTemp_degC[hIdx] := 45.0;
        aHeadPeakLifterForce_N[hIdx] := 1950.0;
        aHeadPeakOp1Force_N[hIdx] := 1150.0;
        aHeadPeakOp2Force_N[hIdx] := 1850.0;
        aHeadFaultStatusBits[hIdx] := 16#0000;
    END_FOR;

    (* 11. Clear FIFO Defect Tracking Shift Register (144 Station Slots) *)
    FOR iIdx := 1 TO 144 DO
        aContainerTrackingFIFO[iIdx] := 16#0000_0000;
    END_FOR;

    (* 12. Clear Digital Filter Histories *)
    FOR iIdx := 1 TO 8 DO
        rFilt_x1[iIdx] := 0.0;
        rFilt_x2[iIdx] := 0.0;
        rFilt_y1[iIdx] := 0.0;
        rFilt_y2[iIdx] := 0.0;
        rFilt_Out[iIdx] := 0.0;
    END_FOR;

    bInitDone := TRUE;
END_IF;

(* Master Execution Interlock & Emergency Stop Safe Brake Verification *)
IF NOT bEnable OR NOT bEmergencyStopOk THEN
    nMachineState := 0; (* Safe Emergency Dynamic Brake State *)
    bSeamerTripped := TRUE;
    bProductionActive := FALSE;
    bEmergencySafeBrakeActive := TRUE;
    rCarouselSpeedRef_deg_s := 0.0;
    rCarouselTorqueCmd_Nm := -120.0; (* Controlled counter-torque braking ramp *)
    rLifterServoPosCmd_mm := 0.0;    (* Retract lifters to lowest mechanical position *)
    rLifterServoForceRef_N := 0.0;
    rOp1RollCamTrim_mm := 0.0;
    rOp2RollCamTrim_mm := 0.0;
    rUnderCoverCO2ValvePctCmd := 0.0;
    rLN2DoserPulseDuration_ms := 0.0;
    bAcousticTapperPulseCmd := FALSE;
    bPneumaticRejectPufferCmd := FALSE;
    wMachineStatusWord := 16#0001;   (* Bit 0: Emergency Safe Brake Latched *)
    RETURN;
END_IF;"""
    code_parts.append(init_code)

    # -------------------------------------------------------------
    # 6. DIGITAL FILTERING
    # -------------------------------------------------------------
    filter_code = """
(*
========================================================================================================================
SIGNAL CONDITIONING: 2ND-ORDER BUTTERWORTH LOW-PASS DIGITAL FILTERING (fc = 40.0 Hz, Ts = 2.0 ms)
========================================================================================================================
*)
(* Filter Channel 1: Lifter Plate Piezo Force LC-01A *)
rFilt_Out[1] := (rFiltCoeff_b0 * rLifterForce_Ch1_N) + (rFiltCoeff_b1 * rFilt_x1[1]) + (rFiltCoeff_b2 * rFilt_x2[1])
                - (rFiltCoeff_a1 * rFilt_y1[1]) - (rFiltCoeff_a2 * rFilt_y2[1]);
rFilt_x2[1] := rFilt_x1[1];
rFilt_x1[1] := rLifterForce_Ch1_N;
rFilt_y2[1] := rFilt_y1[1];
rFilt_y1[1] := rFilt_Out[1];

(* Filter Channel 2: Under-Cover Gas Pressure PT-01A *)
rFilt_Out[2] := (rFiltCoeff_b0 * rGasPress_Ch1_bar) + (rFiltCoeff_b1 * rFilt_x1[2]) + (rFiltCoeff_b2 * rFilt_x2[2])
                - (rFiltCoeff_a1 * rFilt_y1[2]) - (rFiltCoeff_a2 * rFilt_y2[2]);
rFilt_x2[2] := rFilt_x1[2];
rFilt_x1[2] := rGasPress_Ch1_bar;
rFilt_y2[2] := rFilt_y1[2];
rFilt_y1[2] := rFilt_Out[2];

(* Filter Channel 3: Op 1 Curling Roll Radial Force *)
rFilt_Out[3] := (rFiltCoeff_b0 * rOp1RollRadialForce_N) + (rFiltCoeff_b1 * rFilt_x1[3]) + (rFiltCoeff_b2 * rFilt_x2[3])
                - (rFiltCoeff_a1 * rFilt_y1[3]) - (rFiltCoeff_a2 * rFilt_y2[3]);
rFilt_x2[3] := rFilt_x1[3];
rFilt_x1[3] := rOp1RollRadialForce_N;
rFilt_y2[3] := rFilt_y1[3];
rFilt_y1[3] := rFilt_Out[3];

(* Filter Channel 4: Op 2 Ironing Roll Radial Force *)
rFilt_Out[4] := (rFiltCoeff_b0 * rOp2RollRadialForce_N) + (rFiltCoeff_b1 * rFilt_x1[4]) + (rFiltCoeff_b2 * rFilt_x2[4])
                - (rFiltCoeff_a1 * rFilt_y1[4]) - (rFiltCoeff_a2 * rFilt_y2[4]);
rFilt_x2[4] := rFilt_x1[4];
rFilt_x1[4] := rOp2RollRadialForce_N;
rFilt_y2[4] := rFilt_y1[4];
rFilt_y1[4] := rFilt_Out[4];

(* Filter Channel 5: Seaming Chuck Temperature *)
rFilt_Out[5] := (rFiltCoeff_b0 * rSeamingChuckTemp_degC) + (rFiltCoeff_b1 * rFilt_x1[5]) + (rFiltCoeff_b2 * rFilt_x2[5])
                - (rFiltCoeff_a1 * rFilt_y1[5]) - (rFiltCoeff_a2 * rFilt_y2[5]);
rFilt_x2[5] := rFilt_x1[5];
rFilt_x1[5] := rSeamingChuckTemp_degC;
rFilt_y2[5] := rFilt_y1[5];
rFilt_y1[5] := rFilt_Out[5];

(* Filter Channel 6: Central Lubrication Oil Pressure *)
rFilt_Out[6] := (rFiltCoeff_b0 * rLubeOilPressure_bar) + (rFiltCoeff_b1 * rFilt_x1[6]) + (rFiltCoeff_b2 * rFilt_x2[6])
                - (rFiltCoeff_a1 * rFilt_y1[6]) - (rFiltCoeff_a2 * rFilt_y2[6]);
rFilt_x2[6] := rFilt_x1[6];
rFilt_x1[6] := rLubeOilPressure_bar;
rFilt_y2[6] := rFilt_y1[6];
rFilt_y1[6] := rFilt_Out[6];

(* Filter Channel 7: Headspace Dissolved Oxygen Feedback *)
rFilt_Out[7] := (rFiltCoeff_b0 * rDissolvedOxygen_ppb) + (rFiltCoeff_b1 * rFilt_x1[7]) + (rFiltCoeff_b2 * rFilt_x2[7])
                - (rFiltCoeff_a1 * rFilt_y1[7]) - (rFiltCoeff_a2 * rFilt_y2[7]);
rFilt_x2[7] := rFilt_x1[7];
rFilt_x1[7] := rDissolvedOxygen_ppb;
rFilt_y2[7] := rFilt_y1[7];
rFilt_y1[7] := rFilt_Out[7];

(* Filter Channel 8: Encoder Position Filtered Deviation *)
rFilt_Out[8] := (rFiltCoeff_b0 * rEncPos_Ch1_deg) + (rFiltCoeff_b1 * rFilt_x1[8]) + (rFiltCoeff_b2 * rFilt_x2[8])
                - (rFiltCoeff_a1 * rFilt_y1[8]) - (rFiltCoeff_a2 * rFilt_y2[8]);
rFilt_x2[8] := rFilt_x1[8];
rFilt_x1[8] := rEncPos_Ch1_deg;
rFilt_y2[8] := rFilt_y1[8];
rFilt_y1[8] := rFilt_Out[8];"""
    code_parts.append(filter_code)

    # -------------------------------------------------------------
    # 7. PHASE 1: 2oo3 TMR SENSOR VOTING
    # -------------------------------------------------------------
    phase1_code = """
(*
========================================================================================================================
PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING & DISCREPANCY TIMERS
========================================================================================================================
*)
(* -------------------------------------------------------------------------------------------------------------------- *)
(* Set 1: Carousel Absolute Rotary Encoders (ENC-01A, ENC-01B, ENC-01C)                                                *)
(* -------------------------------------------------------------------------------------------------------------------- *)
bEncDiscrep_12 := ABS(rEncPos_Ch1_deg - rEncPos_Ch2_deg) > rEnc_Tol_deg;
bEncDiscrep_23 := ABS(rEncPos_Ch2_deg - rEncPos_Ch3_deg) > rEnc_Tol_deg;
bEncDiscrep_13 := ABS(rEncPos_Ch1_deg - rEncPos_Ch3_deg) > rEnc_Tol_deg;

tEncDiscrep_12_TON(IN := bEncDiscrep_12 AND bEnc_Ch1_Healthy AND bEnc_Ch2_Healthy, PT := T#10MS);
tEncDiscrep_23_TON(IN := bEncDiscrep_23 AND bEnc_Ch2_Healthy AND bEnc_Ch3_Healthy, PT := T#10MS);
tEncDiscrep_13_TON(IN := bEncDiscrep_13 AND bEnc_Ch1_Healthy AND bEnc_Ch3_Healthy, PT := T#10MS);

nEnc_HealthyCount := 0;
IF bEnc_Ch1_Healthy THEN nEnc_HealthyCount := nEnc_HealthyCount + 1; END_IF;
IF bEnc_Ch2_Healthy THEN nEnc_HealthyCount := nEnc_HealthyCount + 1; END_IF;
IF bEnc_Ch3_Healthy THEN nEnc_HealthyCount := nEnc_HealthyCount + 1; END_IF;

IF nEnc_HealthyCount = 3 THEN
    IF NOT tEncDiscrep_12_TON.Q AND NOT tEncDiscrep_23_TON.Q THEN
        (* All three agree within tolerance: Mid-value median voting *)
        IF (rEncPos_Ch1_deg >= rEncPos_Ch2_deg AND rEncPos_Ch1_deg <= rEncPos_Ch3_deg) OR (rEncPos_Ch1_deg <= rEncPos_Ch2_deg AND rEncPos_Ch1_deg >= rEncPos_Ch3_deg) THEN
            rEncPos_Voted_deg := rEncPos_Ch1_deg;
        ELSIF (rEncPos_Ch2_deg >= rEncPos_Ch1_deg AND rEncPos_Ch2_deg <= rEncPos_Ch3_deg) OR (rEncPos_Ch2_deg <= rEncPos_Ch1_deg AND rEncPos_Ch2_deg >= rEncPos_Ch3_deg) THEN
            rEncPos_Voted_deg := rEncPos_Ch2_deg;
        ELSE
            rEncPos_Voted_deg := rEncPos_Ch3_deg;
        END_IF;
        bEnc_TMR_Degraded := FALSE;
        bEnc_TMR_Tripped := FALSE;
    ELSIF NOT tEncDiscrep_12_TON.Q THEN
        rEncPos_Voted_deg := (rEncPos_Ch1_deg + rEncPos_Ch2_deg) * 0.500;
        bEnc_TMR_Degraded := TRUE;
    ELSIF NOT tEncDiscrep_23_TON.Q THEN
        rEncPos_Voted_deg := (rEncPos_Ch2_deg + rEncPos_Ch3_deg) * 0.500;
        bEnc_TMR_Degraded := TRUE;
    ELSIF NOT tEncDiscrep_13_TON.Q THEN
        rEncPos_Voted_deg := (rEncPos_Ch1_deg + rEncPos_Ch3_deg) * 0.500;
        bEnc_TMR_Degraded := TRUE;
    ELSE
        (* All pairs diverge: Irreconcilable TMR failure *)
        rEncPos_Voted_deg := rEncPos_Ch1_deg;
        bEnc_TMR_Tripped := TRUE;
    END_IF;
ELSIF nEnc_HealthyCount = 2 THEN
    bEnc_TMR_Degraded := TRUE;
    IF bEnc_Ch1_Healthy AND bEnc_Ch2_Healthy THEN
        rEncPos_Voted_deg := (rEncPos_Ch1_deg + rEncPos_Ch2_deg) * 0.500;
    ELSIF bEnc_Ch2_Healthy AND bEnc_Ch3_Healthy THEN
        rEncPos_Voted_deg := (rEncPos_Ch2_deg + rEncPos_Ch3_deg) * 0.500;
    ELSE
        rEncPos_Voted_deg := (rEncPos_Ch1_deg + rEncPos_Ch3_deg) * 0.500;
    END_IF;
ELSIF nEnc_HealthyCount = 1 THEN
    bEnc_TMR_Degraded := TRUE;
    IF bEnc_Ch1_Healthy THEN rEncPos_Voted_deg := rEncPos_Ch1_deg;
    ELSIF bEnc_Ch2_Healthy THEN rEncPos_Voted_deg := rEncPos_Ch2_deg;
    ELSE rEncPos_Voted_deg := rEncPos_Ch3_deg;
    END_IF;
ELSE
    bEnc_TMR_Tripped := TRUE;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* Set 2: Active Seaming Head Dynamic Vertical Lifter Load Cells (LC-01A, LC-01B, LC-01C)                              *)
(* -------------------------------------------------------------------------------------------------------------------- *)
bLifterDiscrep_12 := ABS(rLifterForce_Ch1_N - rLifterForce_Ch2_N) > rLifter_Tol_N;
bLifterDiscrep_23 := ABS(rLifterForce_Ch2_N - rLifterForce_Ch3_N) > rLifter_Tol_N;
bLifterDiscrep_13 := ABS(rLifterForce_Ch1_N - rLifterForce_Ch3_N) > rLifter_Tol_N;

tLifterDiscrep_12_TON(IN := bLifterDiscrep_12 AND bLifter_Ch1_Healthy AND bLifter_Ch2_Healthy, PT := T#15MS);
tLifterDiscrep_23_TON(IN := bLifterDiscrep_23 AND bLifter_Ch2_Healthy AND bLifter_Ch3_Healthy, PT := T#15MS);
tLifterDiscrep_13_TON(IN := bLifterDiscrep_13 AND bLifter_Ch1_Healthy AND bLifter_Ch3_Healthy, PT := T#15MS);

nLifter_HealthyCount := 0;
IF bLifter_Ch1_Healthy THEN nLifter_HealthyCount := nLifter_HealthyCount + 1; END_IF;
IF bLifter_Ch2_Healthy THEN nLifter_HealthyCount := nLifter_HealthyCount + 1; END_IF;
IF bLifter_Ch3_Healthy THEN nLifter_HealthyCount := nLifter_HealthyCount + 1; END_IF;

IF nLifter_HealthyCount = 3 THEN
    IF NOT tLifterDiscrep_12_TON.Q AND NOT tLifterDiscrep_23_TON.Q THEN
        IF (rLifterForce_Ch1_N >= rLifterForce_Ch2_N AND rLifterForce_Ch1_N <= rLifterForce_Ch3_N) OR (rLifterForce_Ch1_N <= rLifterForce_Ch2_N AND rLifterForce_Ch1_N >= rLifterForce_Ch3_N) THEN
            rLifterForce_Voted_N := rLifterForce_Ch1_N;
        ELSIF (rLifterForce_Ch2_N >= rLifterForce_Ch1_N AND rLifterForce_Ch2_N <= rLifterForce_Ch3_N) OR (rLifterForce_Ch2_N <= rLifterForce_Ch1_N AND rLifterForce_Ch2_N >= rLifterForce_Ch3_N) THEN
            rLifterForce_Voted_N := rLifterForce_Ch2_N;
        ELSE
            rLifterForce_Voted_N := rLifterForce_Ch3_N;
        END_IF;
        bLifter_TMR_Degraded := FALSE;
        bLifter_TMR_Tripped := FALSE;
    ELSIF NOT tLifterDiscrep_12_TON.Q THEN
        rLifterForce_Voted_N := (rLifterForce_Ch1_N + rLifterForce_Ch2_N) * 0.500;
        bLifter_TMR_Degraded := TRUE;
    ELSIF NOT tLifterDiscrep_23_TON.Q THEN
        rLifterForce_Voted_N := (rLifterForce_Ch2_N + rLifterForce_Ch3_N) * 0.500;
        bLifter_TMR_Degraded := TRUE;
    ELSIF NOT tLifterDiscrep_13_TON.Q THEN
        rLifterForce_Voted_N := (rLifterForce_Ch1_N + rLifterForce_Ch3_N) * 0.500;
        bLifter_TMR_Degraded := TRUE;
    ELSE
        rLifterForce_Voted_N := rLifterForce_Ch1_N;
        bLifter_TMR_Tripped := TRUE;
    END_IF;
ELSIF nLifter_HealthyCount = 2 THEN
    bLifter_TMR_Degraded := TRUE;
    IF bLifter_Ch1_Healthy AND bLifter_Ch2_Healthy THEN
        rLifterForce_Voted_N := (rLifterForce_Ch1_N + rLifterForce_Ch2_N) * 0.500;
    ELSIF bLifter_Ch2_Healthy AND bLifter_Ch3_Healthy THEN
        rLifterForce_Voted_N := (rLifterForce_Ch2_N + rLifterForce_Ch3_N) * 0.500;
    ELSE
        rLifterForce_Voted_N := (rLifterForce_Ch1_N + rLifterForce_Ch3_N) * 0.500;
    END_IF;
ELSIF nLifter_HealthyCount = 1 THEN
    bLifter_TMR_Degraded := TRUE;
    IF bLifter_Ch1_Healthy THEN rLifterForce_Voted_N := rLifterForce_Ch1_N;
    ELSIF bLifter_Ch2_Healthy THEN rLifterForce_Voted_N := rLifterForce_Ch2_N;
    ELSE rLifterForce_Voted_N := rLifterForce_Ch3_N;
    END_IF;
ELSE
    bLifter_TMR_Tripped := TRUE;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* Set 3: Under-Cover Inert Purge Gas Pressure Transmitters (PT-01A, PT-01B, PT-01C)                                   *)
(* -------------------------------------------------------------------------------------------------------------------- *)
bGasDiscrep_12 := ABS(rGasPress_Ch1_bar - rGasPress_Ch2_bar) > rGasPress_Tol_bar;
bGasDiscrep_23 := ABS(rGasPress_Ch2_bar - rGasPress_Ch3_bar) > rGasPress_Tol_bar;
bGasDiscrep_13 := ABS(rGasPress_Ch1_bar - rGasPress_Ch3_bar) > rGasPress_Tol_bar;

tGasDiscrep_12_TON(IN := bGasDiscrep_12 AND bGasPress_Ch1_Healthy AND bGasPress_Ch2_Healthy, PT := T#25MS);
tGasDiscrep_23_TON(IN := bGasDiscrep_23 AND bGasPress_Ch2_Healthy AND bGasPress_Ch3_Healthy, PT := T#25MS);
tGasDiscrep_13_TON(IN := bGasDiscrep_13 AND bGasPress_Ch1_Healthy AND bGasPress_Ch3_Healthy, PT := T#25MS);

nGasPress_HealthyCount := 0;
IF bGasPress_Ch1_Healthy THEN nGasPress_HealthyCount := nGasPress_HealthyCount + 1; END_IF;
IF bGasPress_Ch2_Healthy THEN nGasPress_HealthyCount := nGasPress_HealthyCount + 1; END_IF;
IF bGasPress_Ch3_Healthy THEN nGasPress_HealthyCount := nGasPress_HealthyCount + 1; END_IF;

IF nGasPress_HealthyCount = 3 THEN
    IF NOT tGasDiscrep_12_TON.Q AND NOT tGasDiscrep_23_TON.Q THEN
        IF (rGasPress_Ch1_bar >= rGasPress_Ch2_bar AND rGasPress_Ch1_bar <= rGasPress_Ch3_bar) OR (rGasPress_Ch1_bar <= rGasPress_Ch2_bar AND rGasPress_Ch1_bar >= rGasPress_Ch3_bar) THEN
            rGasPress_Voted_bar := rGasPress_Ch1_bar;
        ELSIF (rGasPress_Ch2_bar >= rGasPress_Ch1_bar AND rGasPress_Ch2_bar <= rGasPress_Ch3_bar) OR (rGasPress_Ch2_bar <= rGasPress_Ch1_bar AND rGasPress_Ch2_bar >= rGasPress_Ch3_bar) THEN
            rGasPress_Voted_bar := rGasPress_Ch2_bar;
        ELSE
            rGasPress_Voted_bar := rGasPress_Ch3_bar;
        END_IF;
        bGasPress_TMR_Degraded := FALSE;
        bGasPress_TMR_Tripped := FALSE;
    ELSIF NOT tGasDiscrep_12_TON.Q THEN
        rGasPress_Voted_bar := (rGasPress_Ch1_bar + rGasPress_Ch2_bar) * 0.500;
        bGasPress_TMR_Degraded := TRUE;
    ELSIF NOT tGasDiscrep_23_TON.Q THEN
        rGasPress_Voted_bar := (rGasPress_Ch2_bar + rGasPress_Ch3_bar) * 0.500;
        bGasPress_TMR_Degraded := TRUE;
    ELSIF NOT tGasDiscrep_13_TON.Q THEN
        rGasPress_Voted_bar := (rGasPress_Ch1_bar + rGasPress_Ch3_bar) * 0.500;
        bGasPress_TMR_Degraded := TRUE;
    ELSE
        rGasPress_Voted_bar := rGasPress_Ch1_bar;
        bGasPress_TMR_Tripped := TRUE;
    END_IF;
ELSIF nGasPress_HealthyCount = 2 THEN
    bGasPress_TMR_Degraded := TRUE;
    IF bGasPress_Ch1_Healthy AND bGasPress_Ch2_Healthy THEN
        rGasPress_Voted_bar := (rGasPress_Ch1_bar + rGasPress_Ch2_bar) * 0.500;
    ELSIF bGasPress_Ch2_Healthy AND bGasPress_Ch3_Healthy THEN
        rGasPress_Voted_bar := (rGasPress_Ch2_bar + rGasPress_Ch3_bar) * 0.500;
    ELSE
        rGasPress_Voted_bar := (rGasPress_Ch1_bar + rGasPress_Ch3_bar) * 0.500;
    END_IF;
ELSIF nGasPress_HealthyCount = 1 THEN
    bGasPress_TMR_Degraded := TRUE;
    IF bGasPress_Ch1_Healthy THEN rGasPress_Voted_bar := rGasPress_Ch1_bar;
    ELSIF bGasPress_Ch2_Healthy THEN rGasPress_Voted_bar := rGasPress_Ch2_bar;
    ELSE rGasPress_Voted_bar := rGasPress_Ch3_bar;
    END_IF;
ELSE
    bGasPress_TMR_Tripped := TRUE;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* Set 4: In-Flight Acoustic Seal Resonant Frequency Sensors (MIC-01A, MIC-01B, MIC-01C)                               *)
(* -------------------------------------------------------------------------------------------------------------------- *)
bAcousticDiscrep_12 := ABS(rAcousticFreq_Ch1_kHz - rAcousticFreq_Ch2_kHz) > rAcoustic_Tol_kHz;
bAcousticDiscrep_23 := ABS(rAcousticFreq_Ch2_kHz - rAcousticFreq_Ch3_kHz) > rAcoustic_Tol_kHz;
bAcousticDiscrep_13 := ABS(rAcousticFreq_Ch1_kHz - rAcousticFreq_Ch3_kHz) > rAcoustic_Tol_kHz;

tAcousticDiscrep_12_TON(IN := bAcousticDiscrep_12 AND bAcoustic_Ch1_Healthy AND bAcoustic_Ch2_Healthy, PT := T#20MS);
tAcousticDiscrep_23_TON(IN := bAcousticDiscrep_23 AND bAcoustic_Ch2_Healthy AND bAcoustic_Ch3_Healthy, PT := T#20MS);
tAcousticDiscrep_13_TON(IN := bAcousticDiscrep_13 AND bAcoustic_Ch1_Healthy AND bAcoustic_Ch3_Healthy, PT := T#20MS);

nAcoustic_HealthyCount := 0;
IF bAcoustic_Ch1_Healthy THEN nAcoustic_HealthyCount := nAcoustic_HealthyCount + 1; END_IF;
IF bAcoustic_Ch2_Healthy THEN nAcoustic_HealthyCount := nAcoustic_HealthyCount + 1; END_IF;
IF bAcoustic_Ch3_Healthy THEN nAcoustic_HealthyCount := nAcoustic_HealthyCount + 1; END_IF;

IF nAcoustic_HealthyCount = 3 THEN
    IF NOT tAcousticDiscrep_12_TON.Q AND NOT tAcousticDiscrep_23_TON.Q THEN
        IF (rAcousticFreq_Ch1_kHz >= rAcousticFreq_Ch2_kHz AND rAcousticFreq_Ch1_kHz <= rAcousticFreq_Ch3_kHz) OR (rAcousticFreq_Ch1_kHz <= rAcousticFreq_Ch2_kHz AND rAcousticFreq_Ch1_kHz >= rAcousticFreq_Ch3_kHz) THEN
            rAcousticFreq_Voted_kHz := rAcousticFreq_Ch1_kHz;
        ELSIF (rAcousticFreq_Ch2_kHz >= rAcousticFreq_Ch1_kHz AND rAcousticFreq_Ch2_kHz <= rAcousticFreq_Ch3_kHz) OR (rAcousticFreq_Ch2_kHz <= rAcousticFreq_Ch1_kHz AND rAcousticFreq_Ch2_kHz >= rAcousticFreq_Ch3_kHz) THEN
            rAcousticFreq_Voted_kHz := rAcousticFreq_Ch2_kHz;
        ELSE
            rAcousticFreq_Voted_kHz := rAcousticFreq_Ch3_kHz;
        END_IF;
        bAcoustic_TMR_Degraded := FALSE;
        bAcoustic_TMR_Tripped := FALSE;
    ELSIF NOT tAcousticDiscrep_12_TON.Q THEN
        rAcousticFreq_Voted_kHz := (rAcousticFreq_Ch1_kHz + rAcousticFreq_Ch2_kHz) * 0.500;
        bAcoustic_TMR_Degraded := TRUE;
    ELSIF NOT tAcousticDiscrep_23_TON.Q THEN
        rAcousticFreq_Voted_kHz := (rAcousticFreq_Ch2_kHz + rAcousticFreq_Ch3_kHz) * 0.500;
        bAcoustic_TMR_Degraded := TRUE;
    ELSIF NOT tAcousticDiscrep_13_TON.Q THEN
        rAcousticFreq_Voted_kHz := (rAcousticFreq_Ch1_kHz + rAcousticFreq_Ch3_kHz) * 0.500;
        bAcoustic_TMR_Degraded := TRUE;
    ELSE
        rAcousticFreq_Voted_kHz := rAcousticFreq_Ch1_kHz;
        bAcoustic_TMR_Tripped := TRUE;
    END_IF;
ELSIF nAcoustic_HealthyCount = 2 THEN
    bAcoustic_TMR_Degraded := TRUE;
    IF bAcoustic_Ch1_Healthy AND bAcoustic_Ch2_Healthy THEN
        rAcousticFreq_Voted_kHz := (rAcousticFreq_Ch1_kHz + rAcousticFreq_Ch2_kHz) * 0.500;
    ELSIF bAcoustic_Ch2_Healthy AND bAcoustic_Ch3_Healthy THEN
        rAcousticFreq_Voted_kHz := (rAcousticFreq_Ch2_kHz + rAcousticFreq_Ch3_kHz) * 0.500;
    ELSE
        rAcousticFreq_Voted_kHz := (rAcousticFreq_Ch1_kHz + rAcousticFreq_Ch3_kHz) * 0.500;
    END_IF;
ELSIF nAcoustic_HealthyCount = 1 THEN
    bAcoustic_TMR_Degraded := TRUE;
    IF bAcoustic_Ch1_Healthy THEN rAcousticFreq_Voted_kHz := rAcousticFreq_Ch1_kHz;
    ELSIF bAcoustic_Ch2_Healthy THEN rAcousticFreq_Voted_kHz := rAcousticFreq_Ch2_kHz;
    ELSE rAcousticFreq_Voted_kHz := rAcousticFreq_Ch3_kHz;
    END_IF;
ELSE
    bAcoustic_TMR_Tripped := TRUE;
END_IF;

(* Pack TMR Redundancy Status Bits *)
wTMR_SensorHealthWord := 16#0000;
IF bEnc_Ch1_Healthy THEN wTMR_SensorHealthWord := wTMR_SensorHealthWord OR 16#0001; END_IF;
IF bEnc_Ch2_Healthy THEN wTMR_SensorHealthWord := wTMR_SensorHealthWord OR 16#0002; END_IF;
IF bEnc_Ch3_Healthy THEN wTMR_SensorHealthWord := wTMR_SensorHealthWord OR 16#0004; END_IF;
IF bLifter_Ch1_Healthy THEN wTMR_SensorHealthWord := wTMR_SensorHealthWord OR 16#0010; END_IF;
IF bLifter_Ch2_Healthy THEN wTMR_SensorHealthWord := wTMR_SensorHealthWord OR 16#0020; END_IF;
IF bLifter_Ch3_Healthy THEN wTMR_SensorHealthWord := wTMR_SensorHealthWord OR 16#0040; END_IF;
IF bGasPress_Ch1_Healthy THEN wTMR_SensorHealthWord := wTMR_SensorHealthWord OR 16#0100; END_IF;
IF bGasPress_Ch2_Healthy THEN wTMR_SensorHealthWord := wTMR_SensorHealthWord OR 16#0200; END_IF;
IF bGasPress_Ch3_Healthy THEN wTMR_SensorHealthWord := wTMR_SensorHealthWord OR 16#0400; END_IF;
IF bAcoustic_Ch1_Healthy THEN wTMR_SensorHealthWord := wTMR_SensorHealthWord OR 16#1000; END_IF;
IF bAcoustic_Ch2_Healthy THEN wTMR_SensorHealthWord := wTMR_SensorHealthWord OR 16#2000; END_IF;
IF bAcoustic_Ch3_Healthy THEN wTMR_SensorHealthWord := wTMR_SensorHealthWord OR 16#4000; END_IF;"""
    code_parts.append(phase1_code)

    # -------------------------------------------------------------
    # 8. PHASE 2: DISCRETE STATE-SPACE PREDICTION & OBSERVER
    # -------------------------------------------------------------
    phase2_code = """
(*
========================================================================================================================
PHASE 2: DISCRETE STATE-SPACE MODEL & LUENBERGER OBSERVER (x[k+1] = A*x[k] + B*u[k] + L*(y - C*x))
========================================================================================================================
*)
(* Populate Current Physical Measurement Vector y_meas from Voted & Filtered Telemetry *)
rVecY_Meas[1] := (rEncPos_Voted_deg - rFillerMasterAngle_deg) * 0.0174533; (* Delta theta [rad] *)
rVecY_Meas[2] := (rMainCarouselVelocity_deg_s - (rFillerMasterVelocity_rpm * 6.0)) * 0.0174533; (* Delta omega [rad/s] *)
rVecY_Meas[3] := rLifterNominalStroke_mm;                                 (* z_lift [mm] *)
rVecY_Meas[4] := (rLifterNominalStroke_mm - rVecX[3]) / 0.0020;            (* dz_lift/dt [mm/s] *)
rVecY_Meas[5] := rLifterForce_Voted_N;                                    (* F_lift [N] *)
rVecY_Meas[6] := rFilt_Out[1] * 0.00125;                                  (* P_hyd [bar] *)
rVecY_Meas[7] := rOp1NominalRadius_mm;                                    (* r_op1 [mm] *)
rVecY_Meas[8] := (rOp1NominalRadius_mm - rVecX[7]) / 0.0020;              (* dr_op1/dt [mm/s] *)
rVecY_Meas[9] := rFilt_Out[3];                                            (* F_rad_op1 [N] *)
rVecY_Meas[10] := rOp2NominalRadius_mm;                                   (* r_op2 [mm] *)
rVecY_Meas[11] := (rOp2NominalRadius_mm - rVecX[10]) / 0.0020;            (* dr_op2/dt [mm/s] *)
rVecY_Meas[12] := rFilt_Out[4];                                           (* F_rad_op2 [N] *)
rVecY_Meas[13] := 0.00125 * rFilt_Out[3];                                 (* delta_curl [mm] *)
rVecY_Meas[14] := 0.00085 * rFilt_Out[4];                                 (* delta_hook [mm] *)
rVecY_Meas[15] := rGasPress_Voted_bar;                                    (* P_head [bar] *)
rVecY_Meas[16] := rFilt_Out[7];                                           (* C_DO [ppb] *)

(* Step A: Compute Model Output Estimate y_est = C*x + D*u and Innovation Residual e_y = y_meas - y_est *)
FOR iIdx := 1 TO 16 DO
    rTempScalar := 0.0000;
    FOR jIdx := 1 TO 16 DO
        rTempScalar := rTempScalar + (rMatC[iIdx, jIdx] * rVecX[jIdx]);
    END_FOR;
    FOR mIdx := 1 TO 8 DO
        rTempScalar := rTempScalar + (rMatD[iIdx, mIdx] * rVecU[mIdx]);
    END_FOR;
    rVecY_Est[iIdx] := rTempScalar;
    rVecY_Err[iIdx] := rVecY_Meas[iIdx] - rVecY_Est[iIdx];
END_FOR;

(* Step B: Compute Predicted Next State Vector x[k+1] = A*x[k] + B*u[k] + L*e_y *)
FOR iIdx := 1 TO 16 DO
    rTempScalar := 0.0000;
    (* State transition matrix product A * x *)
    FOR jIdx := 1 TO 16 DO
        rTempScalar := rTempScalar + (rMatA[iIdx, jIdx] * rVecX[jIdx]);
    END_FOR;
    (* Control input gain product B * u *)
    FOR mIdx := 1 TO 8 DO
        rTempScalar := rTempScalar + (rMatB[iIdx, mIdx] * rVecU[mIdx]);
    END_FOR;
    (* Luenberger observer correction L * e_y *)
    FOR jIdx := 1 TO 16 DO
        rTempScalar := rTempScalar + (rMatL[iIdx, jIdx] * rVecY_Err[jIdx]);
    END_FOR;
    rVecX_Next[iIdx] := rTempScalar;
END_FOR;

(* Step C: State Vector Update for Next Cycle *)
FOR iIdx := 1 TO 16 DO
    rVecX[iIdx] := rVecX_Next[iIdx];
END_FOR;"""
    code_parts.append(phase2_code)

    # -------------------------------------------------------------
    # 9. PHASE 3: RECEDING-HORIZON MPC
    # -------------------------------------------------------------
    phase3_code = """
(*
========================================================================================================================
PHASE 3: RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) OPTIMIZATION
========================================================================================================================
*)
(* Populate Reference Setpoints for State Vector x_ref *)
rVecX_Ref[1] := 0.0000;                      (* Target zero position tracking error *)
rVecX_Ref[2] := 0.0000;                      (* Target zero angular velocity deviation *)
rVecX_Ref[3] := rLifterNominalStroke_mm;     (* Target vertical lifter position *)
rVecX_Ref[4] := 0.0000;                      (* Lifter cruise velocity *)
rVecX_Ref[5] := 2000.0;                      (* Target vertical clamping force [N] *)
rVecX_Ref[6] := 18.50;                       (* Target hydraulic pressure [bar] *)
rVecX_Ref[7] := rOp1NominalRadius_mm;        (* Target Op 1 radial position *)
rVecX_Ref[8] := 0.0000;                      (* Op 1 radial velocity *)
rVecX_Ref[9] := 1150.0;                      (* Op 1 nominal curling force [N] *)
rVecX_Ref[10] := rOp2NominalRadius_mm;       (* Target Op 2 radial position *)
rVecX_Ref[11] := 0.0000;                     (* Op 2 radial velocity *)
rVecX_Ref[12] := 1850.0;                     (* Op 2 nominal ironing force [N] *)
rVecX_Ref[13] := 1.450;                      (* Nominal body hook curl [mm] *)
rVecX_Ref[14] := 1.500;                      (* Nominal end hook flange [mm] *)
rVecX_Ref[15] := 1.850;                      (* Target headspace gas pressure [bar] *)
rVecX_Ref[16] := 15.00;                      (* Target dissolved oxygen [ppb] *)

(* Initialize Multi-Step Prediction Trajectory across Horizon Np = 5 *)
FOR kIdx := 1 TO 5 DO
    IF kIdx = 1 THEN
        FOR iIdx := 1 TO 16 DO
            rPredX[1, iIdx] := rVecX[iIdx];
        END_FOR;
    ELSE
        FOR iIdx := 1 TO 16 DO
            rTempScalar := 0.0000;
            FOR jIdx := 1 TO 16 DO
                rTempScalar := rTempScalar + (rMatA[iIdx, jIdx] * rPredX[kIdx - 1, jIdx]);
            END_FOR;
            FOR mIdx := 1 TO 8 DO
                rTempScalar := rTempScalar + (rMatB[iIdx, mIdx] * rVecU[mIdx]);
            END_FOR;
            rPredX[kIdx, iIdx] := rTempScalar;
        END_FOR;
    END_IF;
END_FOR;

(* Compute Current Quadratic Cost Function Value J *)
rCostJ := 0.0000;
FOR kIdx := 1 TO 5 DO
    (* State penalty (x - x_ref)^T * Q * (x - x_ref) *)
    FOR iIdx := 1 TO 16 DO
        rTempDelta := rPredX[kIdx, iIdx] - rVecX_Ref[iIdx];
        rCostJ := rCostJ + (rTempDelta * rMatQ[iIdx, iIdx] * rTempDelta);
    END_FOR;
    (* Slew rate penalty Delta u^T * R * Delta u *)
    FOR mIdx := 1 TO 8 DO
        rTempDelta := rVecU[mIdx] - rVecU_Prev[mIdx];
        rCostJ := rCostJ + (rTempDelta * rMatR[mIdx, mIdx] * rTempDelta);
    END_FOR;
END_FOR;
(* Terminal State Cost x_N^T * P * x_N *)
FOR iIdx := 1 TO 16 DO
    rTempDelta := rPredX[5, iIdx] - rVecX_Ref[iIdx];
    rCostJ := rCostJ + (rTempDelta * rMatP[iIdx, iIdx] * rTempDelta);
END_FOR;

(* Projected Gradient Descent Optimization over 8 Actuators *)
FOR mIdx := 1 TO 8 DO
    (* Numerical gradient approximation via forward perturbation *)
    rGradJ[mIdx] := 0.0000;
    FOR iIdx := 1 TO 16 DO
        rGradJ[mIdx] := rGradJ[mIdx] + (rMatB[iIdx, mIdx] * rMatQ[iIdx, iIdx] * (rPredX[1, iIdx] - rVecX_Ref[iIdx]));
    END_FOR;
    rGradJ[mIdx] := rGradJ[mIdx] + (rMatR[mIdx, mIdx] * (rVecU[mIdx] - rVecU_Prev[mIdx]));

    (* Update Control Action via Gradient Step *)
    rVecU[mIdx] := rVecU[mIdx] - (rMPC_StepSize * rGradJ[mIdx]);

    (* Apply Slew Rate Limits (|Delta u| <= RateLimit * Ts) *)
    rTempDelta := rVecU[mIdx] - rVecU_Prev[mIdx];
    IF rTempDelta > (rRateLimit_U[mIdx] * 0.0020) THEN
        rVecU[mIdx] := rVecU_Prev[mIdx] + (rRateLimit_U[mIdx] * 0.0020);
    ELSIF rTempDelta < -(rRateLimit_U[mIdx] * 0.0020) THEN
        rVecU[mIdx] := rVecU_Prev[mIdx] - (rRateLimit_U[mIdx] * 0.0020);
    END_IF;

    (* Apply Actuator Physical Saturation Limits *)
    IF rVecU[mIdx] > rU_Max[mIdx] THEN
        rVecU[mIdx] := rU_Max[mIdx];
    ELSIF rVecU[mIdx] < rU_Min[mIdx] THEN
        rVecU[mIdx] := rU_Min[mIdx];
    END_IF;
END_FOR;

(* Store Control History for Rate Penalties *)
FOR mIdx := 1 TO 8 DO
    rVecU_Prev[mIdx] := rVecU[mIdx];
END_FOR;

(* Map MPC Optimized Outputs to Physical Actuators *)
rCarouselTorqueCmd_Nm     := rVecU[1];
rLifterServoForceRef_N    := 1200.0 + (rVecU[2] * 10.0);
rOp1RollCamTrim_mm        := rVecU[3];
rOp2RollCamTrim_mm        := rVecU[4];
rUnderCoverCO2ValvePctCmd := rVecU[5];
rLN2DoserPulseDuration_ms := rVecU[6];"""
    code_parts.append(phase3_code)

    # -------------------------------------------------------------
    # 10. PHASE 4: 12-STAGE OPERATIONAL FINITE STATE MACHINE (FSM)
    # -------------------------------------------------------------
    phase4_code = """
(*
========================================================================================================================
PHASE 4: 12-STAGE OPERATIONAL FINITE STATE MACHINE (FSM)
========================================================================================================================
  Stage 0:  Emergency Seamer Jam Safe Brake (Controlled Regenerative Braking Ramp)
  Stage 1:  Can Filler Electronic Synchronization Handshake (Electronic Gearing Lock)
  Stage 2:  Infeed Starwheel Can Body Indexing (Pocket Capture & Pre-Purge Alignment)
  Stage 3:  Under-Cover Inert Gas Purging (CO2 / LN2 Headspace DO Reduction)
  Stage 4:  Lifter Plate Dynamic Up-Stroke (Servo Load Ramp against Seaming Chuck)
  Stage 5:  1st Operation Roll Seam Curling (Radial Feed & Hook Interlock Forming)
  Stage 6:  Inter-Stage Clearance Transition (Op 1 Retract & Op 2 Approach)
  Stage 7:  2nd Operation Roll Ironing Tightness (Wrinkle Elimination & Compound Flow)
  Stage 8:  In-Flight Acoustic Resonant Tap Inspection (Lid Resonance FFT & Leak Metrology)
  Stage 9:  Down-Stroke Lifter Retraction (Decoupling Seamed Can onto Deadplate)
  Stage 10: Discharge Starwheel Transfer (Discharge Pocket Handover to Outfeed Conveyor)
  Stage 11: High-Speed Defect Chute Purge (Pneumatic Puffer Ejection of Defective Cans)
  Stage 12: Continuous Production Execution & Line Flow Optimization (2,000 CPM Steady-State)
========================================================================================================================
*)
(* State Entry Edge Detection *)
IF nMachineState <> nPreviousState THEN
    bStateFirstScan := TRUE;
    nPreviousState := nMachineState;
ELSE
    bStateFirstScan := FALSE;
END_IF;

(* Master FSM State Timer Execution *)
tStateTimer(IN := NOT bStateFirstScan, PT := T#60S);

(* Local Station Rotary Cam Angle Calculation [0.0..360.0 deg] *)
rCamAngle_deg := rEncPos_Voted_deg;
WHILE rCamAngle_deg >= 360.0 DO
    rCamAngle_deg := rCamAngle_deg - 360.0;
END_WHILE;
WHILE rCamAngle_deg < 0.0 DO
    rCamAngle_deg := rCamAngle_deg + 360.0;
END_WHILE;

(* Determine Current Active Head Index [1..18] based on Cam Phase Angle *)
nActiveHeadIndex := REAL_TO_INT(rCamAngle_deg / 20.0) + 1;
IF nActiveHeadIndex > 18 THEN nActiveHeadIndex := 18; END_IF;
IF nActiveHeadIndex < 1 THEN nActiveHeadIndex := 1; END_IF;

(* Master 12-Stage Operational Case Selector *)
CASE nMachineState OF

    0: (* === STAGE 0: EMERGENCY SEAMER JAM SAFE BRAKE === *)
        bSystemReady := FALSE;
        bProductionActive := FALSE;
        bEmergencySafeBrakeActive := TRUE;
        tEmergencyBrakeTimer(IN := TRUE, PT := T#150MS);
        
        (* Controlled Dynamic Deceleration Ramp *)
        rCarouselSpeedRef_deg_s := 0.0;
        rCarouselTorqueCmd_Nm := -150.0; (* Full regenerative reverse braking torque *)
        rLifterServoPosCmd_mm := 0.0;
        rLifterServoForceRef_N := 0.0;
        rOp1RollCamTrim_mm := -0.500;   (* Force rolls outward to clear jam *)
        rOp2RollCamTrim_mm := -0.500;
        rUnderCoverCO2ValvePctCmd := 0.0;
        rLN2DoserPulseDuration_ms := 0.0;
        bAcousticTapperPulseCmd := FALSE;
        bPneumaticRejectPufferCmd := FALSE;

        IF tEmergencyBrakeTimer.Q OR (rMainCarouselVelocity_deg_s < 5.0) THEN
            rCarouselTorqueCmd_Nm := 0.0;
            wMachineStatusWord := 16#0002; (* Safe Stop Locked *)
            IF bEmergencyStopOk AND bResetAlarms AND NOT bCanJamStarwheelInfeed AND NOT bCanJamDischargeChute THEN
                bSeamerTripped := FALSE;
                bEmergencySafeBrakeActive := FALSE;
                tEmergencyBrakeTimer(IN := FALSE);
                nMachineState := 1; (* Advance to Filler Synchronization *)
            END_IF;
        END_IF;

    1: (* === STAGE 1: CAN FILLER ELECTRONIC SYNCHRONIZATION HANDSHAKE === *)
        bSystemReady := TRUE;
        bProductionActive := FALSE;
        bEmergencySafeBrakeActive := FALSE;
        wMachineStatusWord := 16#0010; (* Synchronizing *)

        (* Electronic Gearing Phase Lock Calculation *)
        rTempDelta := rEncPos_Voted_deg - rFillerMasterAngle_deg;
        WHILE rTempDelta > 180.0 DO rTempDelta := rTempDelta - 360.0; END_WHILE;
        WHILE rTempDelta < -180.0 DO rTempDelta := rTempDelta + 360.0; END_WHILE;

        (* Accelerate carousel to match filler virtual master velocity *)
        rCarouselSpeedRef_deg_s := rFillerMasterVelocity_rpm * 6.0;

        IF bFillerInfeedSyncActive AND (ABS(rTempDelta) < 0.250) AND (rMainCarouselVelocity_deg_s > 100.0) THEN
            bSeamerSynchronized := TRUE;
            wMachineStatusWord := 16#0020; (* Synchronized & Ready *)
            IF nMachineModeCmd = 3 THEN
                nMachineState := 2; (* Advance to Can Body Infeed Indexing *)
            END_IF;
        ELSE
            bSeamerSynchronized := FALSE;
        END_IF;

    2: (* === STAGE 2: INFEED STARWHEEL CAN BODY INDEXING === *)
        wMachineStatusWord := 16#0040; (* Infeed Indexing *)
        rCarouselSpeedRef_deg_s := 666.667; (* 2,000 CPM Nominal Velocity *)

        (* Verify Can and Lid Infeed Sensor Signals *)
        IF bCanPresenceInfeed AND bCanLidPresenceInfeed THEN
            (* Register New Container into FIFO Tracking Slot 1 *)
            aContainerTrackingFIFO[1] := 16#0000_0001; (* Bit 0: Normal Container Active *)
        ELSIF bCanPresenceInfeed AND NOT bCanLidPresenceInfeed THEN
            (* Missing Lid Fault: Flag for Immediate Ejection at Reject Station *)
            aContainerTrackingFIFO[1] := 16#0000_0003; (* Bit 0: Active, Bit 1: Missing Lid Defect *)
            udiCansRejectedTotal := udiCansRejectedTotal + 1;
        ELSE
            aContainerTrackingFIFO[1] := 16#0000_0000; (* Empty Pocket *)
        END_IF;

        (* Advance Infeed Cam Curve (0.0 to 30.0 degrees) *)
        IF rCamAngle_deg >= 30.0 AND rCamAngle_deg < 60.0 THEN
            nMachineState := 3; (* Advance to Under-Cover Inert Gassing *)
        END_IF;

    3: (* === STAGE 3: UNDER-COVER INERT GAS PURGING (CO2 / LN2) === *)
        wMachineStatusWord := 16#0080; (* Inert Gassing Active *)

        (* Modulate CO2 Under-Cover Purge Valve based on Measured DO and Gas Pressure *)
        IF rDissolvedOxygen_ppb > 25.0 THEN
            rUnderCoverCO2ValvePctCmd := 85.0;
        ELSE
            rUnderCoverCO2ValvePctCmd := 65.0;
        END_IF;

        (* Trigger Liquid Nitrogen Cryogenic Micro-Dosing Pulse *)
        IF (aContainerTrackingFIFO[1] AND 16#0001) <> 0 THEN
            rLN2DoserPulseDuration_ms := 4.50; (* 45 mg micro-dose for can internal pressurization *)
        ELSE
            rLN2DoserPulseDuration_ms := 0.0;
        END_IF;

        (* Check Gas Manifold Pressure Integrity *)
        IF rGasPress_Voted_bar < rGasPress_Limit_LL_bar THEN
            aContainerTrackingFIFO[1] := aContainerTrackingFIFO[1] OR 16#0008; (* Bit 3: Low Gas Pressure Defect *)
        END_IF;

        IF rCamAngle_deg >= 60.0 AND rCamAngle_deg < 110.0 THEN
            nMachineState := 4; (* Advance to Lifter Plate Dynamic Up-Stroke *)
        END_IF;

    4: (* === STAGE 4: LIFTER PLATE DYNAMIC UP-STROKE === *)
        wMachineStatusWord := 16#0100; (* Lifter Up-Stroke Active *)

        (* Dynamic Vertical Cam Profile Interpolation: Cosine Ramp 0 to 14.5 mm *)
        (* Smooth vertical lifter stroke prevents liquid sloshing and body buckling *)
        rTempScalar := (rCamAngle_deg - 60.0) / 50.0; (* Normalized stroke parameter [0.0..1.0] *)
        IF rTempScalar > 1.0 THEN rTempScalar := 1.0; END_IF;
        IF rTempScalar < 0.0 THEN rTempScalar := 0.0; END_IF;

        rLifterNominalStroke_mm := 14.50 * (0.500 - (0.500 * COS(rTempScalar * 3.14159265)));
        rLifterServoPosCmd_mm := rLifterNominalStroke_mm;

        (* Dynamic Preload Load Cell Regulation: Ramping from 1200 N to 2000 N *)
        rLifterServoForceRef_N := 1200.0 + (800.0 * rTempScalar);

        (* Check Lifter Clamping Preload at Top of Stroke *)
        IF rTempScalar >= 0.950 THEN
            IF rLifterForce_Voted_N < rLifterForce_Limit_LL_N THEN
                (* Inadequate Seating / Crushed Body Flange Defect *)
                aContainerTrackingFIFO[2] := aContainerTrackingFIFO[2] OR 16#0004; (* Bit 2: Lifter Load Defect *)
                udiForceDefectCount := udiForceDefectCount + 1;
            END_IF;
            aHeadPeakLifterForce_N[nActiveHeadIndex] := rLifterForce_Voted_N;
        END_IF;

        IF rCamAngle_deg >= 110.0 AND rCamAngle_deg < 190.0 THEN
            nMachineState := 5; (* Advance to 1st Operation Roll Seam Curling *)
        END_IF;

    5: (* === STAGE 5: 1ST OPERATION ROLL SEAM CURLING === *)
        wMachineStatusWord := 16#0200; (* 1st Operation Curling *)

        (* 1st Operation Radial Cam Profile (110.0 to 190.0 degrees) *)
        (* Progressive curling roll feeds radially inward to fold can body hook and end hook *)
        rTempScalar := (rCamAngle_deg - 110.0) / 80.0; (* Normalized curling progress [0.0..1.0] *)
        IF rTempScalar > 1.0 THEN rTempScalar := 1.0; END_IF;
        IF rTempScalar < 0.0 THEN rTempScalar := 0.0; END_IF;

        (* Quintic Polynomial Radial Infeed: S(t) = 10*t^3 - 15*t^4 + 6*t^5, Stroke = 4.80 mm *)
        rOp1NominalRadius_mm := 4.800 * ((10.0 * rTempScalar * rTempScalar * rTempScalar)
                                - (15.0 * rTempScalar * rTempScalar * rTempScalar * rTempScalar)
                                + (6.0 * rTempScalar * rTempScalar * rTempScalar * rTempScalar * rTempScalar))
                                + rOp1RollCamTrim_mm;

        (* Maintain High Lifter Clamping Preload (2,000 N) *)
        rLifterServoForceRef_N := 2000.0;

        (* Monitor 1st Operation Radial Seaming Force Profile (Nominal 850 N to 1,450 N) *)
        IF rFilt_Out[3] > aHeadPeakOp1Force_N[nActiveHeadIndex] THEN
            aHeadPeakOp1Force_N[nActiveHeadIndex] := rFilt_Out[3];
        END_IF;

        (* Detect Abnormal Seam Curling Force (Indicates Flange Dent or Chuck Slip) *)
        IF (rTempScalar > 0.60) AND ((rFilt_Out[3] < 600.0) OR (rFilt_Out[3] > 1850.0)) THEN
            aContainerTrackingFIFO[3] := aContainerTrackingFIFO[3] OR 16#0004; (* Force Defect *)
        END_IF;

        IF rCamAngle_deg >= 190.0 AND rCamAngle_deg < 210.0 THEN
            nMachineState := 6; (* Advance to Inter-Stage Clearance Transition *)
        END_IF;

    6: (* === STAGE 6: INTER-STAGE CLEARANCE TRANSITION === *)
        wMachineStatusWord := 16#0400; (* Inter-Stage Clearance *)

        (* Rapidly Retract Op 1 Curling Roll radially outward *)
        rTempScalar := (rCamAngle_deg - 190.0) / 20.0;
        IF rTempScalar > 1.0 THEN rTempScalar := 1.0; END_IF;
        IF rTempScalar < 0.0 THEN rTempScalar := 0.0; END_IF;

        rOp1NominalRadius_mm := 4.800 * (1.000 - rTempScalar);
        rOp2NominalRadius_mm := 0.000; (* Op 2 Roll poised at entry boundary *)

        IF rCamAngle_deg >= 210.0 AND rCamAngle_deg < 290.0 THEN
            nMachineState := 7; (* Advance to 2nd Operation Roll Ironing Tightness *)
        END_IF;

    7: (* === STAGE 7: 2ND OPERATION ROLL IRONING TIGHTNESS === *)
        wMachineStatusWord := 16#0800; (* 2nd Operation Ironing *)

        (* 2nd Operation Radial Cam Profile (210.0 to 290.0 degrees) *)
        (* High-load flattening roll irons out wrinkles and flows sealing compound *)
        rTempScalar := (rCamAngle_deg - 210.0) / 80.0;
        IF rTempScalar > 1.0 THEN rTempScalar := 1.0; END_IF;
        IF rTempScalar < 0.0 THEN rTempScalar := 0.0; END_IF;

        (* Quintic Polynomial Radial Infeed: Stroke = 5.25 mm *)
        rOp2NominalRadius_mm := 5.250 * ((10.0 * rTempScalar * rTempScalar * rTempScalar)
                                - (15.0 * rTempScalar * rTempScalar * rTempScalar * rTempScalar)
                                + (6.0 * rTempScalar * rTempScalar * rTempScalar * rTempScalar * rTempScalar))
                                + rOp2RollCamTrim_mm;

        (* Lifter clamping force maintained at peak 2,050 N *)
        rLifterServoForceRef_N := 2050.0;

        (* Monitor 2nd Operation Radial Ironing Force Profile (Nominal 1,400 N to 2,400 N) *)
        IF rFilt_Out[4] > aHeadPeakOp2Force_N[nActiveHeadIndex] THEN
            aHeadPeakOp2Force_N[nActiveHeadIndex] := rFilt_Out[4];
        END_IF;

        (* Calculate Real-Time Seam Thickness & Overlap Estimates from Ironing Reaction Force *)
        rMeasuredSeamThickness_mm := 1.350 - (0.000108 * rFilt_Out[4]);
        rCalculatedSeamOverlap_pct := 72.0 + (0.0105 * rFilt_Out[4]);
        rMeasuredCountersink_mm := 2.350 + (0.000045 * rLifterForce_Voted_N);

        aHeadSeamThickness_mm[nActiveHeadIndex] := (aHeadSeamThickness_mm[nActiveHeadIndex] * 0.950) + (rMeasuredSeamThickness_mm * 0.050);
        aHeadCountersinkDepth_mm[nActiveHeadIndex] := (aHeadCountersinkDepth_mm[nActiveHeadIndex] * 0.950) + (rMeasuredCountersink_mm * 0.050);

        (* Detect Seam Thickness Out of Specification *)
        IF (rMeasuredSeamThickness_mm > rSeamThick_Limit_HH_mm) OR (rMeasuredSeamThickness_mm < rSeamThick_Limit_LL_mm) THEN
            aContainerTrackingFIFO[4] := aContainerTrackingFIFO[4] OR 16#0002; (* Seam Thickness Reject *)
        END_IF;

        IF rCamAngle_deg >= 290.0 AND rCamAngle_deg < 320.0 THEN
            nMachineState := 8; (* Advance to In-Flight Acoustic Inspection *)
        END_IF;

    8: (* === STAGE 8: IN-FLIGHT ACOUSTIC RESONANT TAP INSPECTION === *)
        wMachineStatusWord := 16#1000; (* Acoustic Inspection Active *)

        (* Op 2 Roll rapidly retracts radially *)
        rOp2NominalRadius_mm := 0.0;

        (* Trigger High-Speed Solenoid Impulse Tapper Pulse (1.2 ms pulse width) *)
        IF (rCamAngle_deg >= 295.0) AND (rCamAngle_deg <= 305.0) THEN
            bAcousticTapperPulseCmd := TRUE;
        ELSE
            bAcousticTapperPulseCmd := FALSE;
        END_IF;

        (* Capture In-Flight Resonant Frequency Feedback *)
        rMeasuredAcousticResonance_kHz := rAcousticFreq_Voted_kHz;
        aHeadAcousticResonance_kHz[nActiveHeadIndex] := (aHeadAcousticResonance_kHz[nActiveHeadIndex] * 0.900) + (rMeasuredAcousticResonance_kHz * 0.100);

        (* Calculate Acoustic Resonance Quality Factor Q = f_res / delta_f *)
        rAcousticDecayQFactor := rMeasuredAcousticResonance_kHz / 0.320;

        (* Detect Micro-Leaks, Loose Seams, or Under-Pressurized Headspace *)
        IF (rMeasuredAcousticResonance_kHz < rAcoustic_Limit_LL_kHz) OR (rMeasuredAcousticResonance_kHz > rAcoustic_Limit_HH_kHz) THEN
            aContainerTrackingFIFO[5] := aContainerTrackingFIFO[5] OR 16#0002; (* Acoustic Defect Latch *)
            udiAcousticDefectCount := udiAcousticDefectCount + 1;
        END_IF;

        IF rCamAngle_deg >= 320.0 AND rCamAngle_deg < 340.0 THEN
            nMachineState := 9; (* Advance to Down-Stroke Lifter Retraction *)
        END_IF;

    9: (* === STAGE 9: DOWN-STROKE LIFTER RETRACTION === *)
        wMachineStatusWord := 16#2000; (* Lifter Down-Stroke *)
        bAcousticTapperPulseCmd := FALSE;

        (* Smooth Lifter Descent Cam Profile: Cosine Descent 14.5 mm to 0.0 mm *)
        rTempScalar := (rCamAngle_deg - 320.0) / 20.0;
        IF rTempScalar > 1.0 THEN rTempScalar := 1.0; END_IF;
        IF rTempScalar < 0.0 THEN rTempScalar := 0.0; END_IF;

        rLifterNominalStroke_mm := 14.50 * (0.500 + (0.500 * COS(rTempScalar * 3.14159265)));
        rLifterServoPosCmd_mm := rLifterNominalStroke_mm;
        rLifterServoForceRef_N := 0.0;

        IF rCamAngle_deg >= 340.0 AND rCamAngle_deg < 355.0 THEN
            nMachineState := 10; (* Advance to Discharge Starwheel Transfer *)
        END_IF;

    10: (* === STAGE 10: DISCHARGE STARWHEEL TRANSFER === *)
        wMachineStatusWord := 16#4000; (* Discharge Starwheel Transfer *)
        rLifterServoPosCmd_mm := 0.0;
        rLifterServoForceRef_N := 0.0;

        (* Handover can body from carousel pocket into discharge starwheel pocket *)
        IF rCamAngle_deg >= 355.0 OR rCamAngle_deg < 5.0 THEN
            nMachineState := 11; (* Advance to Defect Chute Purge *)
        END_IF;

    11: (* === STAGE 11: HIGH-SPEED DEFECT CHUTE PURGE === *)
        wMachineStatusWord := 16#8000; (* Defect Reject Puffer Active *)

        (* Check FIFO Tracking Slot 18 (Positioned in front of high-speed pneumatic rejector) *)
        IF (aContainerTrackingFIFO[18] AND 16#000E) <> 0 THEN
            (* Container flagged with defect: Fire high-speed multi-valve solenoid reject puffer *)
            bPneumaticRejectPufferCmd := TRUE;
            bRejectActuatorFired := TRUE;
            udiCansRejectedTotal := udiCansRejectedTotal + 1;
        ELSE
            bPneumaticRejectPufferCmd := FALSE;
            bRejectActuatorFired := FALSE;
            udiCansSeamedTotal := udiCansSeamedTotal + 1;
        END_IF;

        (* Propagate FIFO Tracking Shift Register *)
        FOR iIdx := 144 TO 2 BY -1 DO
            aContainerTrackingFIFO[iIdx] := aContainerTrackingFIFO[iIdx - 1];
        END_FOR;
        aContainerTrackingFIFO[1] := 16#0000_0000;

        IF nMachineModeCmd = 3 THEN
            nMachineState := 12; (* Continuous Production Loop *)
        ELSE
            nMachineState := 1;  (* Re-synchronize or idle *)
        END_IF;

    12: (* === STAGE 12: CONTINUOUS PRODUCTION EXECUTION & LINE FLOW OPTIMIZATION === *)
        bProductionActive := TRUE;
        bSystemReady := TRUE;
        wMachineStatusWord := 16#0008; (* Full 2,000 CPM Production Running *)

        (* Instantaneous Throughput Calculation (cans/min) *)
        rInstantThroughput_CPM := (rMainCarouselVelocity_deg_s / 360.0) * 18.0 * 60.0;

        (* Monitor for Emergency Jam Conditions *)
        IF bCanJamStarwheelInfeed OR bCanJamDischargeChute OR bRejectBinFull THEN
            nMachineState := 0; (* Abort to Emergency Jam Safe Brake *)
        ELSIF rCamAngle_deg < 30.0 THEN
            nMachineState := 2; (* Recycle to Infeed Starwheel Indexing *)
        END_IF;

ELSE
    nMachineState := 0; (* Default to Safe Emergency Dynamic Brake *)
END_CASE;"""
    code_parts.append(phase4_code)

    # -------------------------------------------------------------
    # 11. PHASE 5: ISA-18.2 ALARMS & DIAGNOSTIC WORD PACKING
    # -------------------------------------------------------------
    phase5_code = """
(*
========================================================================================================================
PHASE 5: ISA-18.2 MULTI-TIERED ALARMS & BIT-PACKED DIAGNOSTIC WORD MAPPING
========================================================================================================================
*)
(* Initialize Alarm Bitfields for Current Evaluation Cycle *)
dwAlarmWord_Critical := 16#0000_0000;
dwAlarmWord_Warning  := 16#0000_0000;
dwAlarmWord_Advisory := 16#0000_0000;

(* --- 1. Finished Double Seam Thickness Alarms --- *)
IF rMeasuredSeamThickness_mm >= rSeamThick_Limit_HH_mm THEN
    dwAlarmWord_Critical := dwAlarmWord_Critical OR 16#0000_0001; (* Bit 0: Seam Thickness HH Critical Trip *)
ELSIF rMeasuredSeamThickness_mm >= rSeamThick_Limit_H_mm THEN
    dwAlarmWord_Warning  := dwAlarmWord_Warning  OR 16#0000_0001; (* Bit 0: Seam Thickness H Warning *)
END_IF;

IF rMeasuredSeamThickness_mm <= rSeamThick_Limit_LL_mm THEN
    dwAlarmWord_Critical := dwAlarmWord_Critical OR 16#0000_0002; (* Bit 1: Seam Thickness LL Critical Trip *)
ELSIF rMeasuredSeamThickness_mm <= rSeamThick_Limit_L_mm THEN
    dwAlarmWord_Warning  := dwAlarmWord_Warning  OR 16#0000_0002; (* Bit 1: Seam Thickness L Warning *)
END_IF;

(* --- 2. Countersink Depth Alarms --- *)
IF rMeasuredCountersink_mm >= rCountersink_Limit_HH_mm THEN
    dwAlarmWord_Critical := dwAlarmWord_Critical OR 16#0000_0004; (* Bit 2: Countersink Depth HH Trip *)
ELSIF rMeasuredCountersink_mm >= rCountersink_Limit_H_mm THEN
    dwAlarmWord_Warning  := dwAlarmWord_Warning  OR 16#0000_0004; (* Bit 2: Countersink Depth H Warning *)
END_IF;

IF rMeasuredCountersink_mm <= rCountersink_Limit_LL_mm THEN
    dwAlarmWord_Critical := dwAlarmWord_Critical OR 16#0000_0008; (* Bit 3: Countersink Depth LL Trip *)
ELSIF rMeasuredCountersink_mm <= rCountersink_Limit_L_mm THEN
    dwAlarmWord_Warning  := dwAlarmWord_Warning  OR 16#0000_0008; (* Bit 3: Countersink Depth L Warning *)
END_IF;

(* --- 3. Seaming Roll Bearing Overtemperature Alarms --- *)
IF (rOp1RollBearingTemp_degC >= rRollTemp_Limit_HH_degC) OR (rOp2RollBearingTemp_degC >= rRollTemp_Limit_HH_degC) THEN
    dwAlarmWord_Critical := dwAlarmWord_Critical OR 16#0000_0010; (* Bit 4: Roll Bearing Overtemperature HH Trip *)
ELSIF (rOp1RollBearingTemp_degC >= rRollTemp_Limit_H_degC) OR (rOp2RollBearingTemp_degC >= rRollTemp_Limit_H_degC) THEN
    dwAlarmWord_Warning  := dwAlarmWord_Warning  OR 16#0000_0010; (* Bit 4: Roll Bearing Temperature H Warning *)
END_IF;

(* --- 4. Under-Cover Inert Purge Gas Pressure Alarms --- *)
IF rGasPress_Voted_bar >= rGasPress_Limit_HH_bar THEN
    dwAlarmWord_Critical := dwAlarmWord_Critical OR 16#0000_0020; (* Bit 5: Gas Pressure HH Trip *)
ELSIF rGasPress_Voted_bar >= rGasPress_Limit_H_bar THEN
    dwAlarmWord_Warning  := dwAlarmWord_Warning  OR 16#0000_0020; (* Bit 5: Gas Pressure H Warning *)
END_IF;

IF rGasPress_Voted_bar <= rGasPress_Limit_LL_bar THEN
    dwAlarmWord_Critical := dwAlarmWord_Critical OR 16#0000_0040; (* Bit 6: Gas Pressure Loss LL Trip *)
ELSIF rGasPress_Voted_bar <= rGasPress_Limit_L_bar THEN
    dwAlarmWord_Warning  := dwAlarmWord_Warning  OR 16#0000_0040; (* Bit 6: Gas Pressure Low Warning *)
END_IF;

(* --- 5. Lifter Plate Dynamic Force Alarms --- *)
IF rLifterForce_Voted_N >= rLifterForce_Limit_HH_N THEN
    dwAlarmWord_Critical := dwAlarmWord_Critical OR 16#0000_0080; (* Bit 7: Lifter Overload Force HH Trip *)
ELSIF rLifterForce_Voted_N >= rLifterForce_Limit_H_N THEN
    dwAlarmWord_Warning  := dwAlarmWord_Warning  OR 16#0000_0080; (* Bit 7: Lifter High Force Warning *)
END_IF;

IF rLifterForce_Voted_N <= rLifterForce_Limit_LL_N THEN
    dwAlarmWord_Critical := dwAlarmWord_Critical OR 16#0000_0100; (* Bit 8: Lifter Force Loss LL Trip *)
ELSIF rLifterForce_Voted_N <= rLifterForce_Limit_L_N THEN
    dwAlarmWord_Warning  := dwAlarmWord_Warning  OR 16#0000_0100; (* Bit 8: Lifter Low Force Warning *)
END_IF;

(* --- 6. In-Flight Acoustic Resonant Frequency Alarms --- *)
IF rMeasuredAcousticResonance_kHz >= rAcoustic_Limit_HH_kHz THEN
    dwAlarmWord_Warning  := dwAlarmWord_Warning  OR 16#0000_0200; (* Bit 9: Acoustic Frequency High Warning *)
ELSIF rMeasuredAcousticResonance_kHz <= rAcoustic_Limit_LL_kHz THEN
    dwAlarmWord_Warning  := dwAlarmWord_Warning  OR 16#0000_0400; (* Bit 10: Acoustic Resonance Low Warning *)
END_IF;

(* --- 7. Central Recirculating Lube Oil Pressure Alarms --- *)
IF rLubeOilPressure_bar <= rLubePress_Limit_LL_bar THEN
    dwAlarmWord_Critical := dwAlarmWord_Critical OR 16#0000_0800; (* Bit 11: Lube Oil Pressure Drop LL Trip *)
ELSIF rLubeOilPressure_bar <= rLubePress_Limit_L_bar THEN
    dwAlarmWord_Warning  := dwAlarmWord_Warning  OR 16#0000_0800; (* Bit 11: Lube Oil Pressure Low Warning *)
END_IF;

(* --- 8. Machine Jam and Hardware Interlock Alarms --- *)
IF bCanJamStarwheelInfeed THEN
    dwAlarmWord_Critical := dwAlarmWord_Critical OR 16#0000_1000; (* Bit 12: Infeed Starwheel Can Jam Trip *)
END_IF;

IF bCanJamDischargeChute THEN
    dwAlarmWord_Critical := dwAlarmWord_Critical OR 16#0000_2000; (* Bit 13: Discharge Chute Accumulation Jam Trip *)
END_IF;

IF bEnc_TMR_Tripped OR bLifter_TMR_Tripped OR bGasPress_TMR_Tripped OR bAcoustic_TMR_Tripped THEN
    dwAlarmWord_Critical := dwAlarmWord_Critical OR 16#0000_4000; (* Bit 14: TMR Redundancy Collapse Trip *)
END_IF;

IF bEnc_TMR_Degraded OR bLifter_TMR_Degraded OR bGasPress_TMR_Degraded OR bAcoustic_TMR_Degraded THEN
    dwAlarmWord_Advisory := dwAlarmWord_Advisory OR 16#0000_0001; (* Bit 0: TMR Sensor Degradation Advisory *)
END_IF;

IF bRejectBinFull THEN
    dwAlarmWord_Advisory := dwAlarmWord_Advisory OR 16#0000_0002; (* Bit 1: Defect Reject Bin Full Advisory *)
END_IF;

(* --- 9. Warning Unacknowledged Escalation Timer (8.0 Seconds to Trip) --- *)
tWarningEscalation_TON(IN := (dwAlarmWord_Warning <> 16#0000_0000), PT := T#8S);
IF tWarningEscalation_TON.Q THEN
    dwAlarmWord_Critical := dwAlarmWord_Critical OR 16#0000_8000; (* Bit 15: Escalated Warning Timeout Trip *)
END_IF;

(* Latch Critical Tripped Output Flag *)
IF dwAlarmWord_Critical <> 16#0000_0000 THEN
    bSeamerTripped := TRUE;
    nMachineState := 0; (* Force Emergency Safe Brake *)
END_IF;

END_FUNCTION_BLOCK"""
    code_parts.append(phase5_code)

    return "\n".join(code_parts)

if __name__ == "__main__":
    prompt = build_prompt()
    st_code = generate_iec_code()
    full_content = f"```iec-st\n{st_code}\n```"
    
    record = {
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": full_content}
        ]
    }
    
    target_dir = "data/swarm_raw"
    os.makedirs(target_dir, exist_ok=True)
    target_file = os.path.join(target_dir, "agent_2e8104cb.json")
    
    with open(target_file, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
        
    print(f"Dataset successfully generated!")
    print(f"Target File: {target_file}")
    print(f"ST Code Character Count: {len(st_code)}")
    print(f"Assistant Content Character Count: {len(full_content)}")
