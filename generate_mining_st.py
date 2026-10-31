# generate_mining_st.py
# High-density IEC 61131-3 generator for FB_Mining_OverlandConveyor_MultiDriveTorque

def build_mining_block():
    sections = []

    # -------------------------------------------------------------------------
    # SECTION 1: HEADER & DECLARATION
    # -------------------------------------------------------------------------
    s1 = """FUNCTION_BLOCK FB_Mining_OverlandConveyor_MultiDriveTorque
(*
====================================================================================================
  LUMINA ADVANCED CYBER-PHYSICAL CONTROL SYSTEMS - SYNTHETIC IEC 61131-3 DATA ARCHITECTURE
  SYSTEM IDENTIFIER: MINING-BULK-OVERLAND-CONVEYOR-ABB-REV13.8
  CORE DOMAIN:
    25-Kilometer Continuous Overland Bulk Ore Conveyor Network:
    Multi-Drive Master-Follower Torque Load Sharing across 4 x 2,500 kW Medium-Voltage VFDs,
    Dynamic Hydraulic Take-Up Trolley Belt Tension Regulation (Preventing Belt Wave Oscillation
    and Sag), Belt Rip Continuous Ultrasonic Detection, and Transfer Chute Plug Level Prevention
    (Rockwell ControlLogix 5580 / ABB Mining PAC Architecture).
  STANDARDS & REGULATORY COMPLIANCE:
    - ISO 5048 Continuous Mechanical Handling Equipment - Belt Conveyors with Carrying Idlers - Calculation of Operating Power and Tensile Forces
    - CEMA 7th Edition (Conveyor Equipment Manufacturers Association) Belt Conveyors for Bulk Materials
    - DIN 22101 Continuous Conveyors - Belt Conveyors for Bulk Materials - Bases for Calculation and Dimensioning
    - AS 1332 / AS 1755 Conveyor Safety Requirements & Australian Bulk Handling Standards
    - IEC 61508 / IEC 61511 Functional Safety (SIL-2 / SIL-3 Emergency Stop & Belt Rip Mitigation)
    - ISA-18.2 / EEMUA 191 Management of Alarm Systems for Mining and Mineral Processing
  ARCHITECT:
    Principal Automation Fellow & Cyber-Physical Systems Chair (75+ Years Veteran Experience)
----------------------------------------------------------------------------------------------------
  OVERLAND BULK CONVEYOR ELASTIC DYNAMICS & MULTI-DRIVE CONTROL THEORY:
    The 25-kilometer overland conveyor transports copper/iron ore from an open-pit primary gyratory
    crusher to the processing plant at 8,500 metric tons per hour (t/h) at a nominal belt velocity
    of 7.50 m/s. The belting is heavy-duty steel-cord (ST-6800 specification: 6,800 N/mm nominal
    breaking strength, 1,800 mm width, 48.5 kg/m per run). The total moving mass of the belt and
    ore exceeds 14,200 metric tons, possessing immense kinetic energy (> 400 MJ).

    1. One-Dimensional Viscoelastic Stress-Wave Propagation:
       The multi-kilometer rubber belt exhibits viscoelastic rheological properties described by the
       one-dimensional damped hyperbolic wave equation:
         rho_linear * d^2(u)/dt^2 = E_cord * A_cord * d^2(u)/dx^2 + eta_visco * d^3(u)/(dx^2 * dt) - f_friction
       where the acoustic stress-wave velocity through the steel cord core is:
         c_wave = sqrt(E_cord * A_cord / rho_linear) ~ 1,650 m/s.
       A mechanical tension wave launched at the head drive station takes:
         T_transit = L_conveyor / c_wave = 25,000 m / 1,650 m/s = 15.15 seconds
       to reach the tail return pulley. Sudden acceleration launches reflective tensile and compressive
       shockwaves that bounce between pulleys. Compressive waves drop local belt tension to zero,
       causing catenary sag between idlers, severe spillage, and dynamic wave whip that derails the belt.

    2. S-Curve Dynamic Belt Tension Controller (180-Second Acceleration):
       To prevent destructive dynamic peak tension spikes (T_dyn <= 1.25 * T_rated) during fully-loaded
       startups, an S-shaped cubic jerk-limited acceleration trajectory is enforced over 180.0 seconds:
         a(t) = a_max * [ 1.0 - cos(2*pi * t / T_ramp) ]
       The active hydraulic take-up winch modulates trolley displacement in real time to compensate
       for elastic belt elongation (Delta_L up to 32.5 meters during full load pull):
         F_takeup = 2 * T_slack = 2 * [ T_tight * exp(-mu * theta) ]
       maintaining idler sag ratio strictly below 1.0% (sag <= 0.010 * IdlerSpacing).

    3. Multi-Drive Master-Follower Torque Sharing (4 x 2,500 kW VFDs):
       Drive 1 & Drive 2 (Primary & Secondary Head Pulleys) and Drive 3 & Drive 4 (Tail Pulleys)
       utilize medium-voltage direct torque control (DTC) synchronized via dedicated optical fiber.
       - Master Drive 1 regulates conveyor belt velocity trajectory.
       - Follower Drives 2, 3, 4 receive fast torque references with dynamic load sharing trim:
           tau_follow_cmd = tau_master * K_share_ratio + Delta_tau_slip_compensator
       An observer continuously monitors motor currents, torque discrepancies, and slip speed.

    4. Ultrasonic / Inductive Belt Rip & Chute Blockage Protection:
       Embedded vulcanized sensor loops (spaced every 50 m) or ultrasonic beam transceivers detect
       longitudinal tears caused by trapped tramp metal. If an antenna loop fails continuity during
       transducer interrogation, the system fires emergency braking within 350 ms.
====================================================================================================
*)

VAR_INPUT
    (* ========================================================================================= *)
    (* PRIMARY CONVEYOR SENSORS & TRANSDUCER TELEMETRY (STRONGLY TYPED PHYSICAL INPUTS)          *)
    (* ========================================================================================= *)
    (* 2oo3 Redundant Head Station Belt Tension Load Cell Triplet [kN] *)
    rHeadTension_kN_A           : REAL := 685.0;    (* Channel A strain-gauge load cell at head drive carriage [kN] *)
    rHeadTension_kN_B           : REAL := 685.0;    (* Channel B strain-gauge load cell at head drive carriage [kN] *)
    rHeadTension_kN_C           : REAL := 685.0;    (* Channel C strain-gauge load cell at head drive carriage [kN] *)

    (* 2oo3 Redundant Hydraulic Take-Up Winch Tension Triplet [kN] *)
    rTakeUpTension_kN_A         : REAL := 450.0;    (* Channel A tension load cell on take-up trolley sheave [kN] *)
    rTakeUpTension_kN_B         : REAL := 450.0;    (* Channel B tension load cell on take-up trolley sheave [kN] *)
    rTakeUpTension_kN_C         : REAL := 450.0;    (* Channel C tension load cell on take-up trolley sheave [kN] *)

    (* 2oo3 Redundant Tail Return Station Belt Tension Triplet [kN] *)
    rTailTension_kN_A           : REAL := 380.0;    (* Channel A tension load cell at tail turnaround station [kN] *)
    rTailTension_kN_B           : REAL := 380.0;    (* Channel B tension load cell at tail turnaround station [kN] *)
    rTailTension_kN_C           : REAL := 380.0;    (* Channel C tension load cell at tail turnaround station [kN] *)

    (* 2oo3 Redundant Doppler Radar Non-Contact Belt Velocity Triplet [m/s] *)
    rDopplerBeltSpeed_ms_A      : REAL := 7.50;     (* Channel A microwave Doppler radar belt surface speed [m/s] *)
    rDopplerBeltSpeed_ms_B      : REAL := 7.50;     (* Channel B microwave Doppler radar belt surface speed [m/s] *)
    rDopplerBeltSpeed_ms_C      : REAL := 7.50;     (* Channel C microwave Doppler radar belt surface speed [m/s] *)

    (* 4 x 2,500 kW VFD Motor Actual Torque Feedback [% of rated motor torque] *)
    rMotor1_TorqueFeedback_Pct  : REAL := 74.50;    (* Drive 1 (Head Primary) actual motor torque feedback [%] *)
    rMotor2_TorqueFeedback_Pct  : REAL := 74.20;    (* Drive 2 (Head Secondary) actual motor torque feedback [%] *)
    rMotor3_TorqueFeedback_Pct  : REAL := 73.80;    (* Drive 3 (Tail Primary) actual motor torque feedback [%] *)
    rMotor4_TorqueFeedback_Pct  : REAL := 73.90;    (* Drive 4 (Tail Secondary) actual motor torque feedback [%] *)

    (* 4 x 2,500 kW VFD Motor Actual Shaft Speed Feedback [rpm] *)
    rMotor1_Speed_rpm           : REAL := 992.0;    (* Drive 1 optical shaft encoder speed [rpm] *)
    rMotor2_Speed_rpm           : REAL := 992.0;    (* Drive 2 optical shaft encoder speed [rpm] *)
    rMotor3_Speed_rpm           : REAL := 991.5;    (* Drive 3 optical shaft encoder speed [rpm] *)
    rMotor4_Speed_rpm           : REAL := 991.5;    (* Drive 4 optical shaft encoder speed [rpm] *)

    (* Hydraulic Take-Up Trolley Position & Pressure Transducers *)
    rTakeUpTrolleyPos_m         : REAL := 14.85;    (* Linear wire-draw encoder take-up trolley travel [m] *)
    rTakeUpHydPressure_bar      : REAL := 185.0;    (* Hydraulic tensioning cylinder pressure [bar] *)

    (* Conveyor Process Material Loading & Environmental Inputs *)
    rOreMassFlowRate_t_h        : REAL := 8250.0;   (* Dual nuclear belt scale ore throughput [tons/h] *)
    rChuteMaterialLevel_Pct     : REAL := 28.5;     (* Microwave transfer chute fill level [%] *)
    rAmbientAirTemp_degC        : REAL := 22.5;     (* Ambient temperature along overland route [deg C] *)

    (* Discrete Safety Interlocks & Sensors *)
    bBeltRipLoopContinuity_OK   : BOOL := TRUE;     (* High-frequency embedded antenna belt rip loop monitor *)
    bEmergencyPullWireSwitchesOK: BOOL := TRUE;     (* Continuous 25 km safety pull-wire rope switch circuit *)
    bTransferChutePlugged       : BOOL := FALSE;    (* Nuclear radiometric chute high-high blockage detector *)
    bBrakePadsRetractedPermissiv: BOOL := TRUE;     (* Mechanical high-speed caliper disk brakes released *)
    bEmergencyStopCommand       : BOOL := FALSE;    (* Hardwired control room emergency stop push-button *)
    bResetTripAlarms            : BOOL := FALSE;    (* Master trip latch reset push-button *)
    bEnable                     : BOOL := TRUE;     (* Functional block master execution enable *)
    tScanTime_s                 : REAL := 0.020;    (* Deterministic controller cycle period [s] (50 Hz task) *)
END_VAR
"""
    sections.append(s1)

    # -------------------------------------------------------------------------
    # SECTION 2: VAR_OUTPUT & VAR
    # -------------------------------------------------------------------------
    s2 = """VAR_OUTPUT
    (* ========================================================================================= *)
    (* ACTUATOR COMMANDS, PROCESS TELEMETRY & STATUS WORDS (STRONGLY TYPED PHYSICAL OUTPUTS)    *)
    (* ========================================================================================= *)
    rDrive1_MasterSpeedCmd_Pct  : REAL := 0.00;     (* Drive 1 VFD master speed reference [% of base speed] *)
    rDrive2_TorqueFollower_Pct  : REAL := 0.00;     (* Drive 2 VFD torque trim demand [%] *)
    rDrive3_TorqueFollower_Pct  : REAL := 0.00;     (* Drive 3 VFD torque trim demand [%] *)
    rDrive4_TorqueFollower_Pct  : REAL := 0.00;     (* Drive 4 VFD torque trim demand [%] *)
    rTakeUpHydraulicValve_Pct   : REAL := 50.00;    (* Hydraulic take-up proportional valve spool demand [%] *)
    bMechanicalBrakeEngageCmd   : BOOL := FALSE;    (* High-speed caliper fail-safe disk brake drop cmd *)
    rVoted_BeltSpeed_ms         : REAL := 0.00;     (* 2oo3 Voted actual conveyor belt linear velocity [m/s] *)
    rVoted_HeadTension_kN       : REAL := 685.0;    (* 2oo3 Voted head drive carriage belt tension [kN] *)
    rVoted_TakeUpTension_kN     : REAL := 450.0;    (* 2oo3 Voted take-up trolley belt tension [kN] *)
    rTorqueUnbalance_Pct        : REAL := 0.00;     (* Maximum torque discrepancy among 4 drive motors [%] *)
    rBeltSagRatio_Pct           : REAL := 0.65;     (* Calculated mid-span belt sag percentage between idlers [%] *)
    rStressWaveVelocity_ms      : REAL := 1650.0;   (* Real-time calculated viscoelastic stress wave speed [m/s] *)
    rTotalElectricalPower_MW    : REAL := 7.42;     (* Total combined real power consumption of 4 drives [MW] *)
    dwConveyorStatusWord        : DWORD := 16#0000_0000; (* 32-bit packed overland conveyor operational status word *)
    dwConveyorAlarmWord_Pri     : DWORD := 16#0000_0000; (* 32-bit packed ISA-18.2 Priority 1 / Trip Alarms *)
    dwConveyorAlarmWord_Sec     : DWORD := 16#0000_0000; (* 32-bit packed ISA-18.2 Priority 2 / Advisory & Warning *)
    dwTMR_DiagnosticWord        : DWORD := 16#0000_0000; (* 32-bit packed 2oo3 sensor health & degradation status *)
    bDriveSlipWarning           : BOOL := FALSE;    (* Warning: Pulley tangential velocity vs belt speed mismatch *)
    bTorqueUnbalanceTrip        : BOOL := FALSE;    (* Severe torque divergence among 4 x 2.5 MW drives *)
    bBeltRipFaultDetected       : BOOL := FALSE;    (* Longitudinal rip antenna severance confirmed *)
    bTakeUpOverTravelFault      : BOOL := FALSE;    (* Take-up trolley reached mechanical travel stop limits *)
    bMPC_Active                 : BOOL := FALSE;    (* Model Predictive Controller active & in regulation *)
    bGracefulDegradation        : BOOL := FALSE;    (* Secondary fallback control active due to sensor fault *)
END_VAR

VAR
    (* ========================================================================================= *)
    (* INTERNAL REGISTERS: MATRICES, 2oo3 TMR ENGINE, WAVE EQUATIONS, MPC SOLVER & FSM           *)
    (* ========================================================================================= *)
    bFirstScanDone              : BOOL := FALSE;    (* Cold-start memory and matrix allocation flag *)

    (* ----------------------------------------------------------------------------------------- *)
    (* 1. MECHANICAL, VISCOELASTIC & HYDRAULIC CONVEYOR CONSTANTS                                *)
    (* ----------------------------------------------------------------------------------------- *)
    rConveyorLength_m           : REAL := 25000.0;  (* Total center-to-center conveyor route length [m] *)
    rBeltNominalWidth_m         : REAL := 1.800;    (* Belt width [m] *)
    rBeltLinearDensity_kg_m     : REAL := 48.50;    (* Unloaded belt linear mass per run [kg/m] *)
    rBeltSteelCordModulus_MPa   : REAL := 185000.0; (* Steel cord equivalent elastic modulus [MPa] *)
    rBeltCrossSection_m2        : REAL := 0.0540;   (* Total belt composite cross-sectional area [m2] *)
    rBeltViscousDamping_Nsm     : REAL := 145000.0; (* Kelvin-Voigt internal viscoelastic damping [N*s/m] *)
    rIdlerSpacing_Carry_m       : REAL := 3.00;     (* Distance between carrying idler sets [m] *)
    rIdlerRollResistance_DIN_f  : REAL := 0.0125;   (* DIN 22101 global artificial friction coefficient f [-] *)
    rDrivePulleyDiameter_m      : REAL := 1.600;    (* Drive pulley shell outer diameter [m] *)
    rMotorRatedPower_kW         : REAL := 2500.0;   (* Rated capacity per motor (4 x 2,500 kW = 10 MW total) *)
    rMotorRatedTorque_kNm       : REAL := 24.15;    (* Motor nominal rated shaft torque [kN*m] *)
    rGearboxRatio               : REAL := 10.55;    (* Drive transmission reduction gear ratio [-] *)
    rEulerFrictionCoeff_mu      : REAL := 0.380;    (* Ceramic lagged pulley to rubber belt friction coefficient *)
    rPulleyWrapAngle_rad        : REAL := 3.490;    (* Drive pulley wrap angle (200 deg = 3.49 rad) *)

    (* Dynamic S-Curve Acceleration Tuning Parameters *)
    rFullSpeedTarget_ms         : REAL := 7.50;     (* Target nominal bulk belt velocity [m/s] *)
    rStartupDuration_s          : REAL := 180.0;    (* Full acceleration ramp duration [s] *)
    rDecelDuration_s            : REAL := 120.0;    (* Controlled stop ramp duration [s] *)
    rTargetPrechargeTension_kN  : REAL := 450.0;    (* Hydraulic take-up precharge setpoint [kN] *)
    rMaxAllowableTension_kN     : REAL := 1150.0;   (* Dynamic peak tension rating limit [kN] *)
    rMinAllowableTension_kN     : REAL := 280.0;    (* Minimum tension to prevent pulley slippage [kN] *)
    rTrolleyTravelMin_m         : REAL := 1.50;     (* Physical minimum take-up stroke limit [m] *)
    rTrolleyTravelMax_m         : REAL := 38.50;    (* Physical maximum take-up stroke limit [m] *)

    (* ----------------------------------------------------------------------------------------- *)
    (* 2. TRIPLE MODULAR REDUNDANCY (2oo3 TMR) FILTERING & REGISTRATION                          *)
    (* ----------------------------------------------------------------------------------------- *)
    rVoted_TailTension_kN       : REAL := 380.0;

    (* Tolerance Deviation Limits *)
    rTol_Tension_kN             : REAL := 35.0;
    rTol_BeltSpeed_ms           : REAL := 0.45;

    (* Stuck-Sensor Frozen Telemetry Counters *)
    iStuck_HT_A  : INT := 0; iStuck_HT_B  : INT := 0; iStuck_HT_C  : INT := 0;
    iStuck_TT_A  : INT := 0; iStuck_TT_B  : INT := 0; iStuck_TT_C  : INT := 0;
    iStuck_TL_A  : INT := 0; iStuck_TL_B  : INT := 0; iStuck_TL_C  : INT := 0;
    iStuck_BS_A  : INT := 0; iStuck_BS_B  : INT := 0; iStuck_BS_C  : INT := 0;

    (* Previous Scan Telemetry *)
    rPrev_HT_A   : REAL := 685.0; rPrev_HT_B   : REAL := 685.0; rPrev_HT_C   : REAL := 685.0;
    rPrev_TT_A   : REAL := 450.0; rPrev_TT_B   : REAL := 450.0; rPrev_TT_C   : REAL := 450.0;
    rPrev_TL_A   : REAL := 380.0; rPrev_TL_B   : REAL := 380.0; rPrev_TL_C   : REAL := 380.0;
    rPrev_BS_A   : REAL := 7.50;  rPrev_BS_B   : REAL := 7.50;  rPrev_BS_C   : REAL := 7.50;

    (* Transducer Health Flags *)
    bHealth_HT_A : BOOL := TRUE; bHealth_HT_B : BOOL := TRUE; bHealth_HT_C : BOOL := TRUE;
    bHealth_TT_A : BOOL := TRUE; bHealth_TT_B : BOOL := TRUE; bHealth_TT_C : BOOL := TRUE;
    bHealth_TL_A : BOOL := TRUE; bHealth_TL_B : BOOL := TRUE; bHealth_TL_C : BOOL := TRUE;
    bHealth_BS_A : BOOL := TRUE; bHealth_BS_B : BOOL := TRUE; bHealth_BS_C : BOOL := TRUE;

    (* Degraded Voting Status Flags *)
    bDegraded_HT_1oo2 : BOOL := FALSE; bDegraded_HT_1oo1 : BOOL := FALSE;
    bDegraded_TT_1oo2 : BOOL := FALSE; bDegraded_TT_1oo1 : BOOL := FALSE;
    bDegraded_TL_1oo2 : BOOL := FALSE; bDegraded_TL_1oo1 : BOOL := FALSE;
    bDegraded_BS_1oo2 : BOOL := FALSE; bDegraded_BS_1oo1 : BOOL := FALSE;

    (* ----------------------------------------------------------------------------------------- *)
    (* 3. 8x8 DISCRETE STATE-SPACE MODEL & KALMAN OBSERVER ARRAYS                                *)
    (* ----------------------------------------------------------------------------------------- *)
    (* State Vector x[0..7]:
         x[0]: Head drive belt velocity deviation Delta v_head [m/s]
         x[1]: Tail turnaround belt velocity deviation Delta v_tail [m/s]
         x[2]: Head drive belt tension deviation Delta T_head [kN]
         x[3]: Take-up trolley tension deviation Delta T_takeup [kN]
         x[4]: Tail turnaround belt tension deviation Delta T_tail [kN]
         x[5]: Hydraulic take-up trolley position deviation Delta x_trolley [m]
         x[6]: Drive motor torque unbalance Delta tau_unbalance [%]
         x[7]: Distributed ore linear mass loading deviation Delta m_ore [kg/m] *)
    aState_x                    : ARRAY[0..7] OF REAL := [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0];
    aState_x_hat                : ARRAY[0..7] OF REAL := [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0];
    aState_x_pred               : ARRAY[0..7] OF REAL := [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0];

    (* Control Vector u[0..3]:
         u[0]: Drive 1 VFD master speed reference demand [%] (0 to 100%)
         u[1]: Drive 2 torque trim demand [%] (-25 to +25%)
         u[2]: Drive 3 & 4 tail torque trim demand [%] (-25 to +25%)
         u[3]: Hydraulic take-up winch proportional valve demand [%] (0 to 100%) *)
    aControl_u                  : ARRAY[0..3] OF REAL := [0.0, 0.0, 0.0, 50.0];
    aControl_u_prev             : ARRAY[0..3] OF REAL := [0.0, 0.0, 0.0, 50.0];
    aControl_du                 : ARRAY[0..3] OF REAL := [0.0, 0.0, 0.0, 0.0];

    (* Disturbance Vector d[0..2]:
         d[0]: Crusher surge feed rate deviation Delta m_dot [tons/h]
         d[1]: Idler bearing ambient rolling resistance fluctuation Delta f_res [-]
         d[2]: Wet belt rain friction reduction Delta mu [-] *)
    aDisturb_d                  : ARRAY[0..2] OF REAL := [0.0, 0.0, 0.0];

    (* Controlled Measurement Vector y[0..3]:
         y[0]: Conveyor belt linear velocity v_belt [m/s]
         y[1]: Head drive carriage belt tension T_head [kN]
         y[2]: Take-up trolley tension T_takeup [kN]
         y[3]: Motor torque unbalance tau_unbal [%] *)
    aOutput_y                   : ARRAY[0..3] OF REAL := [0.0, 685.0, 450.0, 0.0];
    aOutput_y_sp                : ARRAY[0..3] OF REAL := [0.0, 685.0, 450.0, 0.0];
    aOutput_y_error             : ARRAY[0..3] OF REAL := [0.0, 0.0, 0.0, 0.0];

    (* Continuous-to-Discrete 8x8 State Transition Matrix A (Ts = 0.020 s) *)
    aMatrix_A                   : ARRAY[0..7, 0..7] OF REAL;
    (* Input Coupling Matrix B (8x4) *)
    aMatrix_B                   : ARRAY[0..7, 0..3] OF REAL;
    (* Output Mapping Matrix C (4x8) *)
    aMatrix_C                   : ARRAY[0..3, 0..7] OF REAL;
    (* Direct Feedthrough Matrix D (4x4) *)
    aMatrix_D                   : ARRAY[0..3, 0..3] OF REAL;
    (* Disturbance Coupling Matrix E (8x3) *)
    aMatrix_E                   : ARRAY[0..7, 0..2] OF REAL;
    (* Kalman / Luenberger Observer Gain Matrix L_obs (8x4) *)
    aMatrix_L_obs               : ARRAY[0..7, 0..3] OF REAL;

    (* ----------------------------------------------------------------------------------------- *)
    (* 4. MODEL PREDICTIVE CONTROL OPTIMIZATION WEIGHTS & BOUNDS                                 *)
    (* ----------------------------------------------------------------------------------------- *)
    aWeight_Q                   : ARRAY[0..3] OF REAL := [140.0, 85.0, 220.0, 18.0]; (* Velocity & tension prioritized *)
    aWeight_R                   : ARRAY[0..3] OF REAL := [0.15, 0.25, 0.25, 0.08];   (* Low penalty on smooth adjustments *)
    aLimit_du_Max               : ARRAY[0..3] OF REAL := [0.085, 0.45, 0.45, 1.25];  (* Bounded jerk limits *)
    aLimit_du_Min               : ARRAY[0..3] OF REAL := [-0.085, -0.45, -0.45, -1.25];
    aLimit_u_Max                : ARRAY[0..3] OF REAL := [100.0, 25.0, 25.0, 100.0];
    aLimit_u_Min                : ARRAY[0..3] OF REAL := [0.0, -25.0, -25.0, 0.0];

    (* Optimization Workspace *)
    aGrad_g                     : ARRAY[0..3] OF REAL;
    aHessian_diag               : ARRAY[0..3] OF REAL;
    aStep_du                    : ARRAY[0..3] OF REAL;
    iIterQP                     : INT := 0;
    iMaxIterQP                  : INT := 10;
    rAlphaStep                  : REAL := 0.035;

    (* Fallback Decoupled PID Controllers *)
    rPID_Kp_Speed               : REAL := 1.450;
    rPID_Ki_Speed               : REAL := 0.065;
    rPID_Kd_Speed               : REAL := 0.018;
    rPID_Integ_Speed            : REAL := 0.0;
    rPID_PrevErr_Speed          : REAL := 0.0;

    rPID_Kp_Tension             : REAL := 0.850;
    rPID_Ki_Tension             : REAL := 0.045;
    rPID_Kd_Tension             : REAL := 0.012;
    rPID_Integ_Tension          : REAL := 50.0;
    rPID_PrevErr_Tension        : REAL := 0.0;

    (* ----------------------------------------------------------------------------------------- *)
    (* 5. FINITE STATE MACHINE (FSM) VARIABLES                                                   *)
    (* ----------------------------------------------------------------------------------------- *)
    (* Machine States:
         0  : SYSTEM_INSPECTION_PURGE        - Brakes set, pull wires checked, rip loops verified
         10 : HYDRAULIC_TENSION_PRECHARGE    - Hydraulic take-up precharges trolley to 450 kN
         20 : CONTROLLED_180S_STARTUP        - S-curve acceleration ramp over 180 seconds
         30 : FULL_SPEED_BULK_RUN            - Full speed 7.5 m/s, master-follower torque active
         40 : CONTROLLED_INERTIA_STOP        - 120-second regenerative stop to prevent wave shock
         90 : EMERGENCY_BRAKE_ABORT          - Mechanical caliper disk brake drop, rip/jam trip *)
    iFSM_State                  : INT := 0;
    iPreviousFSM_State          : INT := 0;
    rStateTimer_s               : REAL := 0.0;
    rStartupTimer_s             : REAL := 0.0;
    rStopTimer_s                : REAL := 0.0;

    (* ----------------------------------------------------------------------------------------- *)
    (* 6. INTERMEDIATE KINEMATIC & ELASTIC WAVE COMPUTATION REGISTERS                            *)
    (* ----------------------------------------------------------------------------------------- *)
    rEffectiveMovingMass_kg     : REAL := 14200000.0; (* Total conveyor dynamic moving mass [kg] *)
    rOreLinearMass_kg_m         : REAL := 305.5;    (* Ore payload per linear meter [kg/m] *)
    rSCurveRampFraction         : REAL := 0.00;     (* Normalized ramp progress [0.0 to 1.0] *)
    rTargetVelocity_ms          : REAL := 0.00;     (* S-curve reference speed [m/s] *)
    rTotalOreWeightOnBelt_t     : REAL := 7637.5;   (* Total ore inventory on 25 km carry strand [tons] *)
    rDriveSlipSpeed_ms          : REAL := 0.00;     (* Tangential pulley vs belt speed slip [m/s] *)
    rPulleyTangentialSpeed_ms   : REAL := 0.00;     (* Drive pulley surface speed [m/s] *)

    (* Loop iterators *)
    iIdx                        : INT := 0;
    jIdx                        : INT := 0;
    rTmpSum                     : REAL := 0.0;
END_VAR
"""
    sections.append(s2)

    # -------------------------------------------------------------------------
    # SECTION 3: LOGIC PART 1 - SAFETY RELAYS & FIRST SCAN INITIALIZATION
    # -------------------------------------------------------------------------
    s3 = """(* ============================================================================================= *)
(* SECTION 1: HARDWIRED SAFETY INTERLOCKS & FIRST-SCAN MATRIX INITIALIZATION                     *)
(* ============================================================================================= *)
(* Hardwired Emergency Stop & Pull-Wire Interlock Supervision *)
IF bEmergencyStopCommand OR (NOT bEmergencyPullWireSwitchesOK) THEN
    iFSM_State                  := 90;              (* Jump to EMERGENCY_BRAKE_ABORT *)
    rDrive1_MasterSpeedCmd_Pct  := 0.00;            (* Trip all 4 VFD drives immediately *)
    rDrive2_TorqueFollower_Pct  := 0.00;
    rDrive3_TorqueFollower_Pct  := 0.00;
    rDrive4_TorqueFollower_Pct  := 0.00;
    bMechanicalBrakeEngageCmd   := TRUE;            (* Drop fail-safe disk caliper brakes *)
    bMPC_Active                 := FALSE;
    dwConveyorAlarmWord_Pri     := dwConveyorAlarmWord_Pri OR 16#8000_0000; (* Bit 31: EMERGENCY_STOP_ACTIVE *)
END_IF;

(* Master Block Execution Disabled *)
IF NOT bEnable THEN
    rDrive1_MasterSpeedCmd_Pct  := 0.00;
    rDrive2_TorqueFollower_Pct  := 0.00;
    rDrive3_TorqueFollower_Pct  := 0.00;
    rDrive4_TorqueFollower_Pct  := 0.00;
    bMechanicalBrakeEngageCmd   := TRUE;
    rTakeUpHydraulicValve_Pct   := 50.0;            (* Hydraulic lock *)
    bMPC_Active                 := FALSE;
    bGracefulDegradation        := FALSE;
    bDriveSlipWarning           := FALSE;
    bTorqueUnbalanceTrip        := FALSE;
    bBeltRipFaultDetected       := FALSE;
    bTakeUpOverTravelFault      := FALSE;
    dwConveyorStatusWord        := 16#0000_0000;
    RETURN;
END_IF;

(* First-Scan State-Space Matrix Allocation *)
IF NOT bFirstScanDone THEN
    (* ------------------------------------------------------------------------------------- *)
    (* Discrete 8x8 Transition Matrix A (Ts = 0.020 s, 50 Hz Deterministic Loop)             *)
    (* Models 25 km elastic stress-wave propagation, take-up trolley motion, and torque load  *)
    (* ------------------------------------------------------------------------------------- *)
    (* Row 0: Head drive belt velocity v_head *)
    aMatrix_A[0,0] := 0.9850; aMatrix_A[0,1] := 0.0045; aMatrix_A[0,2] := -0.0018; aMatrix_A[0,3] := 0.0008;
    aMatrix_A[0,4] := 0.0000; aMatrix_A[0,5] := 0.0000; aMatrix_A[0,6] := -0.0125; aMatrix_A[0,7] := -0.0045;

    (* Row 1: Tail turnaround belt velocity v_tail (delayed by stress-wave transit) *)
    aMatrix_A[1,0] := 0.0035; aMatrix_A[1,1] := 0.9820; aMatrix_A[1,2] := 0.0000;  aMatrix_A[1,3] := -0.0012;
    aMatrix_A[1,4] := -0.0025; aMatrix_A[1,5] := 0.0000; aMatrix_A[1,6] := 0.0000; aMatrix_A[1,7] := -0.0045;

    (* Row 2: Head drive belt tension T_head *)
    aMatrix_A[2,0] := 18.500; aMatrix_A[2,1] := -4.250; aMatrix_A[2,2] := 0.9650; aMatrix_A[2,3] := 0.0180;
    aMatrix_A[2,4] := 0.0085; aMatrix_A[2,5] := -0.450; aMatrix_A[2,6] := 0.0850; aMatrix_A[2,7] := 0.1250;

    (* Row 3: Take-up trolley tension T_takeup *)
    aMatrix_A[3,0] := -2.450; aMatrix_A[3,1] := 1.850;  aMatrix_A[3,2] := 0.0150; aMatrix_A[3,3] := 0.9550;
    aMatrix_A[3,4] := 0.0120; aMatrix_A[3,5] := 1.250;  aMatrix_A[3,6] := 0.0000; aMatrix_A[3,7] := 0.0000;

    (* Row 4: Tail turnaround tension T_tail *)
    aMatrix_A[4,0] := 0.0000; aMatrix_A[4,1] := 14.500; aMatrix_A[4,2] := 0.0080; aMatrix_A[4,3] := 0.0150;
    aMatrix_A[4,4] := 0.9620; aMatrix_A[4,5] := -0.250; aMatrix_A[4,6] := 0.0000; aMatrix_A[4,7] := 0.0850;

    (* Row 5: Hydraulic take-up trolley position x_trolley *)
    aMatrix_A[5,0] := 0.0000; aMatrix_A[5,1] := 0.0000; aMatrix_A[5,2] := 0.0000; aMatrix_A[5,3] := -0.0018;
    aMatrix_A[5,4] := 0.0000; aMatrix_A[5,5] := 0.9850; aMatrix_A[5,6] := 0.0000; aMatrix_A[5,7] := 0.0000;

    (* Row 6: Motor torque unbalance tau_unbal *)
    aMatrix_A[6,0] := 0.0450; aMatrix_A[6,1] := 0.0000; aMatrix_A[6,2] := 0.0000; aMatrix_A[6,3] := 0.0000;
    aMatrix_A[6,4] := 0.0000; aMatrix_A[6,5] := 0.0000; aMatrix_A[6,6] := 0.8850; aMatrix_A[6,7] := 0.0000;

    (* Row 7: Ore mass loading rate m_ore *)
    aMatrix_A[7,0] := 0.0000; aMatrix_A[7,1] := 0.0000; aMatrix_A[7,2] := 0.0000; aMatrix_A[7,3] := 0.0000;
    aMatrix_A[7,4] := 0.0000; aMatrix_A[7,5] := 0.0000; aMatrix_A[7,6] := 0.0000; aMatrix_A[7,7] := 0.9990;

    (* ------------------------------------------------------------------------------------- *)
    (* Discrete 8x4 Input Coupling Matrix B                                                  *)
    (* Inputs: u[0]=Master Speed [%], u[1]=Drive 2 Trim [%], u[2]=Tail Trim [%], u[3]=TakeUp Valve [%] *)
    (* ------------------------------------------------------------------------------------- *)
    aMatrix_B[0,0] := 0.0385; aMatrix_B[0,1] := 0.0125; aMatrix_B[0,2] := 0.0085; aMatrix_B[0,3] := 0.0000;
    aMatrix_B[1,0] := 0.0045; aMatrix_B[1,1] := 0.0020; aMatrix_B[1,2] := 0.0245; aMatrix_B[1,3] := 0.0000;
    aMatrix_B[2,0] := 0.4500; aMatrix_B[2,1] := 0.1850; aMatrix_B[2,2] := 0.0850; aMatrix_B[2,3] := -0.1250;
    aMatrix_B[3,0] := -0.0450; aMatrix_B[3,1] := 0.0000; aMatrix_B[3,2] := 0.0000; aMatrix_B[3,3] := 0.3850;
    aMatrix_B[4,0] := 0.0120; aMatrix_B[4,1] := 0.0000; aMatrix_B[4,2] := 0.2850; aMatrix_B[4,3] := -0.0850;
    aMatrix_B[5,0] := 0.0000; aMatrix_B[5,1] := 0.0000; aMatrix_B[5,2] := 0.0000; aMatrix_B[5,3] := 0.0145;
    aMatrix_B[6,0] := 0.0000; aMatrix_B[6,1] := 0.1250; aMatrix_B[6,2] := 0.0850; aMatrix_B[6,3] := 0.0000;
    aMatrix_B[7,0] := 0.0000; aMatrix_B[7,1] := 0.0000; aMatrix_B[7,2] := 0.0000; aMatrix_B[7,3] := 0.0000;

    (* ------------------------------------------------------------------------------------- *)
    (* Discrete 4x8 Output Mapping Matrix C                                                  *)
    (* Outputs: y[0]=v_belt, y[1]=T_head, y[2]=T_takeup, y[3]=tau_unbalance                  *)
    (* ------------------------------------------------------------------------------------- *)
    aMatrix_C[0,0] := 1.0; aMatrix_C[0,1] := 0.0; aMatrix_C[0,2] := 0.0; aMatrix_C[0,3] := 0.0;
    aMatrix_C[0,4] := 0.0; aMatrix_C[0,5] := 0.0; aMatrix_C[0,6] := 0.0; aMatrix_C[0,7] := 0.0;

    aMatrix_C[1,0] := 0.0; aMatrix_C[1,1] := 0.0; aMatrix_C[1,2] := 1.0; aMatrix_C[1,3] := 0.0;
    aMatrix_C[1,4] := 0.0; aMatrix_C[1,5] := 0.0; aMatrix_C[1,6] := 0.0; aMatrix_C[1,7] := 0.0;

    aMatrix_C[2,0] := 0.0; aMatrix_C[2,1] := 0.0; aMatrix_C[2,2] := 0.0; aMatrix_C[2,3] := 1.0;
    aMatrix_C[2,4] := 0.0; aMatrix_C[2,5] := 0.0; aMatrix_C[2,6] := 0.0; aMatrix_C[2,7] := 0.0;

    aMatrix_C[3,0] := 0.0; aMatrix_C[3,1] := 0.0; aMatrix_C[3,2] := 0.0; aMatrix_C[3,3] := 0.0;
    aMatrix_C[3,4] := 0.0; aMatrix_C[3,5] := 0.0; aMatrix_C[3,6] := 1.0; aMatrix_C[3,7] := 0.0;

    (* Direct Feedthrough Matrix D (4x4) *)
    FOR iIdx := 0 TO 3 DO
        FOR jIdx := 0 TO 3 DO
            aMatrix_D[iIdx, jIdx] := 0.0;
        END_FOR;
    END_FOR;

    (* ------------------------------------------------------------------------------------- *)
    (* Disturbance Coupling Matrix E (8x3)                                                   *)
    (* ------------------------------------------------------------------------------------- *)
    aMatrix_E[0,0] := -0.0085; aMatrix_E[0,1] := -0.0150; aMatrix_E[0,2] := -0.0250;
    aMatrix_E[1,0] := -0.0085; aMatrix_E[1,1] := -0.0150; aMatrix_E[1,2] := -0.0250;
    aMatrix_E[2,0] := 0.1450;  aMatrix_E[2,1] := 0.0850;  aMatrix_E[2,2] := 0.1850;
    aMatrix_E[3,0] := 0.0250;  aMatrix_E[3,1] := 0.0120;  aMatrix_E[3,2] := 0.0450;
    aMatrix_E[4,0] := 0.0850;  aMatrix_E[4,1] := 0.0650;  aMatrix_E[4,2] := 0.0950;
    aMatrix_E[5,0] := 0.0000;  aMatrix_E[5,1] := 0.0000;  aMatrix_E[5,2] := 0.0000;
    aMatrix_E[6,0] := 0.0000;  aMatrix_E[6,1] := 0.0000;  aMatrix_E[6,2] := 0.0000;
    aMatrix_E[7,0] := 0.2850;  aMatrix_E[7,1] := 0.0000;  aMatrix_E[7,2] := 0.0000;

    (* ------------------------------------------------------------------------------------- *)
    (* Kalman / Luenberger Observer Gain Matrix L_obs (8x4)                                  *)
    (* ------------------------------------------------------------------------------------- *)
    aMatrix_L_obs[0,0] := 0.3150; aMatrix_L_obs[0,1] := 0.0045; aMatrix_L_obs[0,2] := 0.0000; aMatrix_L_obs[0,3] := 0.0000;
    aMatrix_L_obs[1,0] := 0.1850; aMatrix_L_obs[1,1] := 0.0000; aMatrix_L_obs[1,2] := 0.0025; aMatrix_L_obs[1,3] := 0.0000;
    aMatrix_L_obs[2,0] := 0.0450; aMatrix_L_obs[2,1] := 0.2850; aMatrix_L_obs[2,2] := 0.0150; aMatrix_L_obs[2,3] := 0.0000;
    aMatrix_L_obs[3,0] := 0.0000; aMatrix_L_obs[3,1] := 0.0120; aMatrix_L_obs[3,2] := 0.3450; aMatrix_L_obs[3,3] := 0.0000;
    aMatrix_L_obs[4,0] := 0.0000; aMatrix_L_obs[4,1] := 0.0150; aMatrix_L_obs[4,2] := 0.0180; aMatrix_L_obs[4,3] := 0.0000;
    aMatrix_L_obs[5,0] := 0.0000; aMatrix_L_obs[5,1] := 0.0000; aMatrix_L_obs[5,2] := 0.0850; aMatrix_L_obs[5,3] := 0.0000;
    aMatrix_L_obs[6,0] := 0.0000; aMatrix_L_obs[6,1] := 0.0000; aMatrix_L_obs[6,2] := 0.0000; aMatrix_L_obs[6,3] := 0.4200;
    aMatrix_L_obs[7,0] := -0.0150; aMatrix_L_obs[7,1] := 0.0450; aMatrix_L_obs[7,2] := 0.0000; aMatrix_L_obs[7,3] := 0.0000;

    bFirstScanDone := TRUE;
END_IF;
"""
    sections.append(s3)

    # -------------------------------------------------------------------------
    # SECTION 4: LOGIC PART 2 - 2oo3 TMR VOTING
    # -------------------------------------------------------------------------
    s4 = """(* ============================================================================================= *)
(* SECTION 2: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) VOTING & FAULT DEGRADATION ENGINE            *)
(* ============================================================================================= *)
(* --------------------------------------------------------------------------------------------- *)
(* 1. Head Station Belt Tension Transducers (rHeadTension_kN_A, B, C)                            *)
(* --------------------------------------------------------------------------------------------- *)
IF ABS(rHeadTension_kN_A - rPrev_HT_A) < 0.001 THEN iStuck_HT_A := iStuck_HT_A + 1; ELSE iStuck_HT_A := 0; END_IF;
IF ABS(rHeadTension_kN_B - rPrev_HT_B) < 0.001 THEN iStuck_HT_B := iStuck_HT_B + 1; ELSE iStuck_HT_B := 0; END_IF;
IF ABS(rHeadTension_kN_C - rPrev_HT_C) < 0.001 THEN iStuck_HT_C := iStuck_HT_C + 1; ELSE iStuck_HT_C := 0; END_IF;
rPrev_HT_A := rHeadTension_kN_A; rPrev_HT_B := rHeadTension_kN_B; rPrev_HT_C := rHeadTension_kN_C;

bHealth_HT_A := (rHeadTension_kN_A >= 50.0) AND (rHeadTension_kN_A <= 1500.0) AND (iStuck_HT_A < 250);
bHealth_HT_B := (rHeadTension_kN_B >= 50.0) AND (rHeadTension_kN_B <= 1500.0) AND (iStuck_HT_B < 250);
bHealth_HT_C := (rHeadTension_kN_C >= 50.0) AND (rHeadTension_kN_C <= 1500.0) AND (iStuck_HT_C < 250);

IF bHealth_HT_A AND bHealth_HT_B AND bHealth_HT_C THEN
    bDegraded_HT_1oo2 := FALSE; bDegraded_HT_1oo1 := FALSE;
    IF ((rHeadTension_kN_A >= rHeadTension_kN_B) AND (rHeadTension_kN_A <= rHeadTension_kN_C)) OR
       ((rHeadTension_kN_A >= rHeadTension_kN_C) AND (rHeadTension_kN_A <= rHeadTension_kN_B)) THEN
        rVoted_HeadTension_kN := rHeadTension_kN_A;
    ELSIF ((rHeadTension_kN_B >= rHeadTension_kN_A) AND (rHeadTension_kN_B <= rHeadTension_kN_C)) OR
          ((rHeadTension_kN_B >= rHeadTension_kN_C) AND (rHeadTension_kN_B <= rHeadTension_kN_A)) THEN
        rVoted_HeadTension_kN := rHeadTension_kN_B;
    ELSE
        rVoted_HeadTension_kN := rHeadTension_kN_C;
    END_IF;
    IF (ABS(rHeadTension_kN_A - rHeadTension_kN_B) > rTol_Tension_kN) OR
       (ABS(rHeadTension_kN_B - rHeadTension_kN_C) > rTol_Tension_kN) OR
       (ABS(rHeadTension_kN_A - rHeadTension_kN_C) > rTol_Tension_kN) THEN
        dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0001; (* Bit 0: Head Tension Discrepancy *)
    END_IF;
ELSIF bHealth_HT_A AND bHealth_HT_B THEN
    bDegraded_HT_1oo2 := TRUE; rVoted_HeadTension_kN := (rHeadTension_kN_A + rHeadTension_kN_B) * 0.5;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0002;
ELSIF bHealth_HT_A AND bHealth_HT_C THEN
    bDegraded_HT_1oo2 := TRUE; rVoted_HeadTension_kN := (rHeadTension_kN_A + rHeadTension_kN_C) * 0.5;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0002;
ELSIF bHealth_HT_B AND bHealth_HT_C THEN
    bDegraded_HT_1oo2 := TRUE; rVoted_HeadTension_kN := (rHeadTension_kN_B + rHeadTension_kN_C) * 0.5;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0002;
ELSIF bHealth_HT_A THEN
    bDegraded_HT_1oo1 := TRUE; rVoted_HeadTension_kN := rHeadTension_kN_A;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0004;
ELSIF bHealth_HT_B THEN
    bDegraded_HT_1oo1 := TRUE; rVoted_HeadTension_kN := rHeadTension_kN_B;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0004;
ELSIF bHealth_HT_C THEN
    bDegraded_HT_1oo1 := TRUE; rVoted_HeadTension_kN := rHeadTension_kN_C;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0004;
ELSE
    rVoted_HeadTension_kN := 450.0;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0008;
    bGracefulDegradation := TRUE;
END_IF;

(* --------------------------------------------------------------------------------------------- *)
(* 2. Take-Up Winch Tension Transducers (rTakeUpTension_kN_A, B, C)                              *)
(* --------------------------------------------------------------------------------------------- *)
IF ABS(rTakeUpTension_kN_A - rPrev_TT_A) < 0.001 THEN iStuck_TT_A := iStuck_TT_A + 1; ELSE iStuck_TT_A := 0; END_IF;
IF ABS(rTakeUpTension_kN_B - rPrev_TT_B) < 0.001 THEN iStuck_TT_B := iStuck_TT_B + 1; ELSE iStuck_TT_B := 0; END_IF;
IF ABS(rTakeUpTension_kN_C - rPrev_TT_C) < 0.001 THEN iStuck_TT_C := iStuck_TT_C + 1; ELSE iStuck_TT_C := 0; END_IF;
rPrev_TT_A := rTakeUpTension_kN_A; rPrev_TT_B := rTakeUpTension_kN_B; rPrev_TT_C := rTakeUpTension_kN_C;

bHealth_TT_A := (rTakeUpTension_kN_A >= 50.0) AND (rTakeUpTension_kN_A <= 1000.0) AND (iStuck_TT_A < 250);
bHealth_TT_B := (rTakeUpTension_kN_B >= 50.0) AND (rTakeUpTension_kN_B <= 1000.0) AND (iStuck_TT_B < 250);
bHealth_TT_C := (rTakeUpTension_kN_C >= 50.0) AND (rTakeUpTension_kN_C <= 1000.0) AND (iStuck_TT_C < 250);

IF bHealth_TT_A AND bHealth_TT_B AND bHealth_TT_C THEN
    bDegraded_TT_1oo2 := FALSE; bDegraded_TT_1oo1 := FALSE;
    IF ((rTakeUpTension_kN_A >= rTakeUpTension_kN_B) AND (rTakeUpTension_kN_A <= rTakeUpTension_kN_C)) OR
       ((rTakeUpTension_kN_A >= rTakeUpTension_kN_C) AND (rTakeUpTension_kN_A <= rTakeUpTension_kN_B)) THEN
        rVoted_TakeUpTension_kN := rTakeUpTension_kN_A;
    ELSIF ((rTakeUpTension_kN_B >= rTakeUpTension_kN_A) AND (rTakeUpTension_kN_B <= rTakeUpTension_kN_C)) OR
          ((rTakeUpTension_kN_B >= rTakeUpTension_kN_C) AND (rTakeUpTension_kN_B <= rTakeUpTension_kN_A)) THEN
        rVoted_TakeUpTension_kN := rTakeUpTension_kN_B;
    ELSE
        rVoted_TakeUpTension_kN := rTakeUpTension_kN_C;
    END_IF;
    IF (ABS(rTakeUpTension_kN_A - rTakeUpTension_kN_B) > rTol_Tension_kN) OR
       (ABS(rTakeUpTension_kN_B - rTakeUpTension_kN_C) > rTol_Tension_kN) OR
       (ABS(rTakeUpTension_kN_A - rTakeUpTension_kN_C) > rTol_Tension_kN) THEN
        dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0010;
    END_IF;
ELSIF bHealth_TT_A AND bHealth_TT_B THEN
    bDegraded_TT_1oo2 := TRUE; rVoted_TakeUpTension_kN := (rTakeUpTension_kN_A + rTakeUpTension_kN_B) * 0.5;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0020;
ELSIF bHealth_TT_A AND bHealth_TT_C THEN
    bDegraded_TT_1oo2 := TRUE; rVoted_TakeUpTension_kN := (rTakeUpTension_kN_A + rTakeUpTension_kN_C) * 0.5;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0020;
ELSIF bHealth_TT_B AND bHealth_TT_C THEN
    bDegraded_TT_1oo2 := TRUE; rVoted_TakeUpTension_kN := (rTakeUpTension_kN_B + rTakeUpTension_kN_C) * 0.5;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0020;
ELSIF bHealth_TT_A THEN
    bDegraded_TT_1oo1 := TRUE; rVoted_TakeUpTension_kN := rTakeUpTension_kN_A;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0040;
ELSIF bHealth_TT_B THEN
    bDegraded_TT_1oo1 := TRUE; rVoted_TakeUpTension_kN := rTakeUpTension_kN_B;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0040;
ELSIF bHealth_TT_C THEN
    bDegraded_TT_1oo1 := TRUE; rVoted_TakeUpTension_kN := rTakeUpTension_kN_C;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0040;
ELSE
    rVoted_TakeUpTension_kN := 450.0;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0080;
    bGracefulDegradation := TRUE;
END_IF;

(* --------------------------------------------------------------------------------------------- *)
(* 3. Doppler Radar Non-Contact Belt Speed Transducers (rDopplerBeltSpeed_ms_A, B, C)            *)
(* --------------------------------------------------------------------------------------------- *)
bHealth_BS_A := (rDopplerBeltSpeed_ms_A >= -1.0) AND (rDopplerBeltSpeed_ms_A <= 12.0);
bHealth_BS_B := (rDopplerBeltSpeed_ms_B >= -1.0) AND (rDopplerBeltSpeed_ms_B <= 12.0);
bHealth_BS_C := (rDopplerBeltSpeed_ms_C >= -1.0) AND (rDopplerBeltSpeed_ms_C <= 12.0);

IF bHealth_BS_A AND bHealth_BS_B AND bHealth_BS_C THEN
    IF ((rDopplerBeltSpeed_ms_A >= rDopplerBeltSpeed_ms_B) AND (rDopplerBeltSpeed_ms_A <= rDopplerBeltSpeed_ms_C)) OR
       ((rDopplerBeltSpeed_ms_A >= rDopplerBeltSpeed_ms_C) AND (rDopplerBeltSpeed_ms_A <= rDopplerBeltSpeed_ms_B)) THEN
        rVoted_BeltSpeed_ms := rDopplerBeltSpeed_ms_A;
    ELSIF ((rDopplerBeltSpeed_ms_B >= rDopplerBeltSpeed_ms_A) AND (rDopplerBeltSpeed_ms_B <= rDopplerBeltSpeed_ms_C)) OR
          ((rDopplerBeltSpeed_ms_B >= rDopplerBeltSpeed_ms_C) AND (rDopplerBeltSpeed_ms_B <= rDopplerBeltSpeed_ms_A)) THEN
        rVoted_BeltSpeed_ms := rDopplerBeltSpeed_ms_B;
    ELSE
        rVoted_BeltSpeed_ms := rDopplerBeltSpeed_ms_C;
    END_IF;
ELSE
    rVoted_BeltSpeed_ms := rDopplerBeltSpeed_ms_A;
END_IF;

(* --------------------------------------------------------------------------------------------- *)
(* 4. Tail Turnaround Belt Tension Voting (2oo3)                                                 *)
(* --------------------------------------------------------------------------------------------- *)
bHealth_TL_A := (rTailTension_kN_A >= 20.0) AND (rTailTension_kN_A <= 1000.0);
bHealth_TL_B := (rTailTension_kN_B >= 20.0) AND (rTailTension_kN_B <= 1000.0);
bHealth_TL_C := (rTailTension_kN_C >= 20.0) AND (rTailTension_kN_C <= 1000.0);

IF bHealth_TL_A AND bHealth_TL_B AND bHealth_TL_C THEN
    IF ((rTailTension_kN_A >= rTailTension_kN_B) AND (rTailTension_kN_A <= rTailTension_kN_C)) OR
       ((rTailTension_kN_A >= rTailTension_kN_C) AND (rTailTension_kN_A <= rTailTension_kN_B)) THEN
        rVoted_TailTension_kN := rTailTension_kN_A;
    ELSIF ((rTailTension_kN_B >= rTailTension_kN_A) AND (rTailTension_kN_B <= rTailTension_kN_C)) OR
          ((rTailTension_kN_B >= rTailTension_kN_C) AND (rTailTension_kN_B <= rTailTension_kN_A)) THEN
        rVoted_TailTension_kN := rTailTension_kN_B;
    ELSE
        rVoted_TailTension_kN := rTailTension_kN_C;
    END_IF;
ELSE
    rVoted_TailTension_kN := rTailTension_kN_A;
END_IF;
"""
    sections.append(s4)

    # -------------------------------------------------------------------------
    # SECTION 5: LOGIC PART 3 - VISCOELASTIC PHYSICS & TORQUE LOAD SHARING
    # -------------------------------------------------------------------------
    s5 = """(* ============================================================================================= *)
(* SECTION 3: VISCOELASTIC STRESS WAVE PHYSICS & MASTER-FOLLOWER TORQUE LOAD SHARING             *)
(* ============================================================================================= *)
(* Effective Linear Density including Distributed Ore Payload: rho_eff = rho_belt + m_ore [kg/m] *)
IF rVoted_BeltSpeed_ms > 0.50 THEN
    rOreLinearMass_kg_m := (rOreMassFlowRate_t_h * 1000.0 / 3600.0) / rVoted_BeltSpeed_ms;
ELSE
    rOreLinearMass_kg_m := 0.0;
END_IF;

(* Viscoelastic 1D Stress-Wave Velocity: c = sqrt(E_cord * A_cord / rho_linear) [m/s] *)
rTmpSum := (rBeltSteelCordModulus_MPa * 1.0E6 * rBeltCrossSection_m2) / (rBeltLinearDensity_kg_m + rOreLinearMass_kg_m);
IF rTmpSum > 100000.0 THEN
    rStressWaveVelocity_ms := SQRT(rTmpSum);
ELSE
    rStressWaveVelocity_ms := 1650.0;
END_IF;

(* Drive Pulley Tangential Surface Velocity: v_pulley = pi * D * N_motor / (60 * GearboxRatio) *)
rPulleyTangentialSpeed_ms := (3.14159265 * rDrivePulleyDiameter_m * rMotor1_Speed_rpm) / (60.0 * rGearboxRatio);

(* Drive Pulley Slip Speed: v_slip = |v_pulley - v_belt| *)
rDriveSlipSpeed_ms := ABS(rPulleyTangentialSpeed_ms - rVoted_BeltSpeed_ms);
bDriveSlipWarning  := (rDriveSlipSpeed_ms >= 0.450) AND (rVoted_BeltSpeed_ms >= 1.0);
IF bDriveSlipWarning THEN
    dwConveyorAlarmWord_Sec := dwConveyorAlarmWord_Sec OR 16#0000_0001; (* Bit 0: DRIVE_PULLEY_SLIP_WARN *)
END_IF;

(* Multi-Drive Motor Torque Discrepancy & Unbalance Calculation *)
(* Max torque minus min torque across 4 x 2,500 kW drives *)
rTmpSum := rMotor1_TorqueFeedback_Pct;
IF rMotor2_TorqueFeedback_Pct > rTmpSum THEN rTmpSum := rMotor2_TorqueFeedback_Pct; END_IF;
IF rMotor3_TorqueFeedback_Pct > rTmpSum THEN rTmpSum := rMotor3_TorqueFeedback_Pct; END_IF;
IF rMotor4_TorqueFeedback_Pct > rTmpSum THEN rTmpSum := rMotor4_TorqueFeedback_Pct; END_IF;

rTorqueUnbalance_Pct := rTmpSum;
rTmpSum := rMotor1_TorqueFeedback_Pct;
IF rMotor2_TorqueFeedback_Pct < rTmpSum THEN rTmpSum := rMotor2_TorqueFeedback_Pct; END_IF;
IF rMotor3_TorqueFeedback_Pct < rTmpSum THEN rTmpSum := rMotor3_TorqueFeedback_Pct; END_IF;
IF rMotor4_TorqueFeedback_Pct < rTmpSum THEN rTmpSum := rMotor4_TorqueFeedback_Pct; END_IF;

rTorqueUnbalance_Pct := rTorqueUnbalance_Pct - rTmpSum;

(* Torque Unbalance Alarms *)
IF rTorqueUnbalance_Pct >= 18.0 THEN
    bTorqueUnbalanceTrip     := TRUE;
    dwConveyorAlarmWord_Pri  := dwConveyorAlarmWord_Pri OR 16#0000_0001; (* Bit 0: TORQUE_UNBALANCE_HH_TRIP *)
ELSIF rTorqueUnbalance_Pct >= 10.0 THEN
    dwConveyorAlarmWord_Sec  := dwConveyorAlarmWord_Sec OR 16#0000_0002; (* Bit 1: TORQUE_UNBALANCE_H_WARN *)
ELSE
    bTorqueUnbalanceTrip     := FALSE;
END_IF;

(* CEMA Mid-Span Belt Sag Ratio: sag% = (m_total * g * a^2) / (8 * T_belt) * 100% *)
IF rVoted_TakeUpTension_kN > 10.0 THEN
    rBeltSagRatio_Pct := (((rBeltLinearDensity_kg_m + rOreLinearMass_kg_m) * rGravity_m_s2 * (rIdlerSpacing_Carry_m * rIdlerSpacing_Carry_m)) /
                          (8.0 * (rVoted_TakeUpTension_kN * 1000.0))) * 100.0;
ELSE
    rBeltSagRatio_Pct := 2.5;
END_IF;

(* Total 4-Drive Electrical Power Consumption [MW] *)
rTotalElectricalPower_MW := ((rMotor1_TorqueFeedback_Pct + rMotor2_TorqueFeedback_Pct +
                              rMotor3_TorqueFeedback_Pct + rMotor4_TorqueFeedback_Pct) * 0.01 * rMotorRatedPower_kW * 4.0 * 0.001);

(* Ultrasonic Belt Rip Loop Integrity Monitoring *)
IF NOT bBeltRipLoopContinuity_OK THEN
    bBeltRipFaultDetected    := TRUE;
    iFSM_State               := 90;         (* Instantaneous emergency brake drop *)
    dwConveyorAlarmWord_Pri  := dwConveyorAlarmWord_Pri OR 16#0000_0002; (* Bit 1: BELT_RIP_SEVERANCE_HH_TRIP *)
ELSE
    bBeltRipFaultDetected := FALSE;
END_IF;

(* Take-Up Trolley Travel Limit Monitoring *)
IF (rTakeUpTrolleyPos_m <= rTrolleyTravelMin_m) OR (rTakeUpTrolleyPos_m >= rTrolleyTravelMax_m) THEN
    bTakeUpOverTravelFault   := TRUE;
    dwConveyorAlarmWord_Pri  := dwConveyorAlarmWord_Pri OR 16#0000_0004; (* Bit 2: TROLLEY_OVERTRAVEL_HH_TRIP *)
ELSE
    bTakeUpOverTravelFault := FALSE;
END_IF;
"""
    sections.append(s5)

    # -------------------------------------------------------------------------
    # SECTION 6: LOGIC PART 4 - 8x8 STATE-SPACE & KALMAN OBSERVER
    # -------------------------------------------------------------------------
    s6 = """(* ============================================================================================= *)
(* SECTION 4: 8x8 DISCRETE STATE-SPACE TIME PROPAGATION & KALMAN OBSERVER UPDATE                 *)
(* ============================================================================================= *)
(* Map Disturbance Vector d *)
aDisturb_d[0] := (rOreMassFlowRate_t_h - 8250.0) / 1000.0;
aDisturb_d[1] := 0.0;
aDisturb_d[2] := 0.0;

(* State Propagation: x_pred = A * x_hat + B * u + E * d *)
FOR iIdx := 0 TO 7 DO
    rTmpSum := 0.0;
    FOR jIdx := 0 TO 7 DO
        rTmpSum := rTmpSum + aMatrix_A[iIdx, jIdx] * aState_x_hat[jIdx];
    END_FOR;
    FOR jIdx := 0 TO 3 DO
        rTmpSum := rTmpSum + aMatrix_B[iIdx, jIdx] * aControl_u[jIdx];
    END_FOR;
    FOR jIdx := 0 TO 2 DO
        rTmpSum := rTmpSum + aMatrix_E[iIdx, jIdx] * aDisturb_d[jIdx];
    END_FOR;
    aState_x_pred[iIdx] := rTmpSum;
END_FOR;

(* Measured Physical Outputs y_meas *)
aOutput_y[0] := rVoted_BeltSpeed_ms;
aOutput_y[1] := rVoted_HeadTension_kN;
aOutput_y[2] := rVoted_TakeUpTension_kN;
aOutput_y[3] := rTorqueUnbalance_Pct;

(* Observer Innovation Correction: x_hat = x_pred + L_obs * (y_meas - C * x_pred) *)
FOR iIdx := 0 TO 7 DO
    rTmpSum := aState_x_pred[iIdx];
    FOR jIdx := 0 TO 3 DO
        rTmpSum := rTmpSum + aMatrix_L_obs[iIdx, jIdx] * (aOutput_y[jIdx] -
            (aMatrix_C[jIdx, 0]*aState_x_pred[0] + aMatrix_C[jIdx, 1]*aState_x_pred[1] +
             aMatrix_C[jIdx, 2]*aState_x_pred[2] + aMatrix_C[jIdx, 3]*aState_x_pred[3] +
             aMatrix_C[jIdx, 4]*aState_x_pred[4] + aMatrix_C[jIdx, 5]*aState_x_pred[5] +
             aMatrix_C[jIdx, 6]*aState_x_pred[6] + aMatrix_C[jIdx, 7]*aState_x_pred[7]));
    END_FOR;
    aState_x_hat[iIdx] := rTmpSum;
END_FOR;
"""
    sections.append(s6)

    # -------------------------------------------------------------------------
    # SECTION 7: LOGIC PART 5 - MPC SOLVER & MASTER-FOLLOWER TORQUE
    # -------------------------------------------------------------------------
    s7 = """(* ============================================================================================= *)
(* SECTION 5: MODEL PREDICTIVE CONTROL & S-CURVE TENSION TRACKING                                *)
(* ============================================================================================= *)
(* Determine Output Setpoints from FSM Mode *)
IF iFSM_State = 30 THEN
    aOutput_y_sp[0] := rFullSpeedTarget_ms;     (* 7.50 m/s *)
    aOutput_y_sp[1] := 685.0;                   (* Head tension setpoint [kN] *)
    aOutput_y_sp[2] := 450.0;                   (* Take-up tension setpoint [kN] *)
    aOutput_y_sp[3] := 0.00;                    (* Zero torque unbalance target *)
ELSIF iFSM_State = 20 THEN
    aOutput_y_sp[0] := rTargetVelocity_ms;      (* Ramp velocity *)
    aOutput_y_sp[1] := 720.0;                   (* Elevated start tension *)
    aOutput_y_sp[2] := 480.0;                   (* Elevated take-up precharge *)
    aOutput_y_sp[3] := 0.00;
ELSE
    aOutput_y_sp[0] := 0.00;
    aOutput_y_sp[1] := 450.0;
    aOutput_y_sp[2] := 450.0;
    aOutput_y_sp[3] := 0.00;
END_IF;

(* Tracking Error *)
aOutput_y_error[0] := aOutput_y[0] - aOutput_y_sp[0];
aOutput_y_error[1] := aOutput_y[1] - aOutput_y_sp[1];
aOutput_y_error[2] := aOutput_y[2] - aOutput_y_sp[2];
aOutput_y_error[3] := aOutput_y[3] - aOutput_y_sp[3];

IF NOT bGracefulDegradation AND (iFSM_State = 30 OR iFSM_State = 20) THEN
    bMPC_Active := TRUE;

    (* Approximate Diagonal Hessian *)
    aHessian_diag[0] := aWeight_Q[0] * 0.0015 + aWeight_R[0]; (* Master speed command *)
    aHessian_diag[1] := aWeight_Q[3] * 0.0150 + aWeight_R[1]; (* Drive 2 torque trim *)
    aHessian_diag[2] := aWeight_Q[3] * 0.0150 + aWeight_R[2]; (* Drive 3/4 tail trim *)
    aHessian_diag[3] := aWeight_Q[2] * 0.0025 + aWeight_R[3]; (* Take-up hydraulic valve *)

    (* Gradient Calculation *)
    aGrad_g[0] := aWeight_Q[0] * aOutput_y_error[0] * 0.0385 + aWeight_R[0] * aControl_du[0];
    aGrad_g[1] := aWeight_Q[3] * aOutput_y_error[3] * 0.1250 + aWeight_R[1] * aControl_du[1];
    aGrad_g[2] := aWeight_Q[3] * aOutput_y_error[3] * 0.0850 + aWeight_R[2] * aControl_du[2];
    aGrad_g[3] := aWeight_Q[2] * aOutput_y_error[2] * 0.3850 + aWeight_R[3] * aControl_du[3];

    (* Iterative Projected Gradient Descent *)
    FOR iIterQP := 1 TO iMaxIterQP DO
        FOR iIdx := 0 TO 3 DO
            aStep_du[iIdx] := aControl_du[iIdx] - (rAlphaStep / aHessian_diag[iIdx]) * aGrad_g[iIdx];

            (* Slew rate constraints *)
            IF aStep_du[iIdx] > aLimit_du_Max[iIdx] THEN
                aStep_du[iIdx] := aLimit_du_Max[iIdx];
            ELSIF aStep_du[iIdx] < aLimit_du_Min[iIdx] THEN
                aStep_du[iIdx] := aLimit_du_Min[iIdx];
            END_IF;

            (* Actuator bounds *)
            IF (aControl_u[iIdx] + aStep_du[iIdx]) > aLimit_u_Max[iIdx] THEN
                aStep_du[iIdx] := aLimit_u_Max[iIdx] - aControl_u[iIdx];
            ELSIF (aControl_u[iIdx] + aStep_du[iIdx]) < aLimit_u_Min[iIdx] THEN
                aStep_du[iIdx] := aLimit_u_Min[iIdx] - aControl_u[iIdx];
            END_IF;

            aControl_du[iIdx] := aStep_du[iIdx];
        END_FOR;
    END_FOR;

    (* Apply Moves *)
    aControl_u[0] := aControl_u[0] + aControl_du[0];
    aControl_u[1] := aControl_u[1] + aControl_du[1];
    aControl_u[2] := aControl_u[2] + aControl_du[2];
    aControl_u[3] := aControl_u[3] + aControl_du[3];

    rDrive1_MasterSpeedCmd_Pct := aControl_u[0];
    rDrive2_TorqueFollower_Pct := aControl_u[1];
    rDrive3_TorqueFollower_Pct := aControl_u[2];
    rDrive4_TorqueFollower_Pct := aControl_u[2]; (* Drive 4 shares tail trim *)
    rTakeUpHydraulicValve_Pct  := aControl_u[3];
ELSE
    (* Fallback Decoupled Control *)
    bMPC_Active := FALSE;

    (* Speed PID *)
    rTmpSum := (aOutput_y_sp[0] - rVoted_BeltSpeed_ms);
    rPID_Integ_Speed := rPID_Integ_Speed + rTmpSum * tScanTime_s;
    IF rPID_Integ_Speed > 20.0 THEN rPID_Integ_Speed := 20.0; END_IF;
    IF rPID_Integ_Speed < -20.0 THEN rPID_Integ_Speed := -20.0; END_IF;
    rDrive1_MasterSpeedCmd_Pct := (aOutput_y_sp[0] / rFullSpeedTarget_ms) * 100.0 + rPID_Kp_Speed * rTmpSum + rPID_Ki_Speed * rPID_Integ_Speed;

    (* Take-Up Tension PID *)
    rTmpSum := (aOutput_y_sp[2] - rVoted_TakeUpTension_kN);
    rPID_Integ_Tension := rPID_Integ_Tension + rTmpSum * tScanTime_s;
    IF rPID_Integ_Tension > 25.0 THEN rPID_Integ_Tension := 25.0; END_IF;
    IF rPID_Integ_Tension < -25.0 THEN rPID_Integ_Tension := -25.0; END_IF;
    rTakeUpHydraulicValve_Pct := 50.0 + rPID_Kp_Tension * rTmpSum * 0.10 + rPID_Ki_Tension * rPID_Integ_Tension * 0.10;

    rDrive2_TorqueFollower_Pct := 0.0;
    rDrive3_TorqueFollower_Pct := 0.0;
    rDrive4_TorqueFollower_Pct := 0.0;
END_IF;
"""
    sections.append(s7)

    # -------------------------------------------------------------------------
    # SECTION 8: LOGIC PART 6 - FSM MACHINE SEQUENCER
    # -------------------------------------------------------------------------
    s8 = """(* ============================================================================================= *)
(* SECTION 6: MULTI-STAGE FINITE STATE MACHINE (FSM) SEQUENCING                                  *)
(* ============================================================================================= *)
IF iFSM_State = iPreviousFSM_State THEN
    rStateTimer_s := rStateTimer_s + tScanTime_s;
ELSE
    rStateTimer_s      := 0.0;
    iPreviousFSM_State := iFSM_State;
END_IF;

CASE iFSM_State OF
    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 0: SYSTEM_INSPECTION_PURGE (Safety Pull-Wires & Brakes Locked, Rip Loops Checked)   *)
    (* ----------------------------------------------------------------------------------------- *)
    0:
        rDrive1_MasterSpeedCmd_Pct := 0.00;
        rDrive2_TorqueFollower_Pct := 0.00;
        rDrive3_TorqueFollower_Pct := 0.00;
        rDrive4_TorqueFollower_Pct := 0.00;
        bMechanicalBrakeEngageCmd  := TRUE;         (* Mechanical caliper disk brakes applied *)

        (* Advance to Tension Precharge when pull-wires clear, rip loop OK, and chute clear *)
        IF bEmergencyPullWireSwitchesOK AND bBeltRipLoopContinuity_OK AND (NOT bTransferChutePlugged) THEN
            iFSM_State := 10;                       (* Advance to HYDRAULIC_TENSION_PRECHARGE *)
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 10: HYDRAULIC_TENSION_PRECHARGE (Hydraulic Winch Pre-tensions Belt to 450 kN)       *)
    (* ----------------------------------------------------------------------------------------- *)
    10:
        rDrive1_MasterSpeedCmd_Pct := 0.00;
        bMechanicalBrakeEngageCmd  := TRUE;         (* Maintain brakes while tensioning *)

        (* Modulate hydraulic valve to reach target 450 kN precharge *)
        IF rVoted_TakeUpTension_kN < rTargetPrechargeTension_kN THEN
            rTakeUpHydraulicValve_Pct := 65.0;      (* Hydraulic cylinder pull *)
        ELSE
            rTakeUpHydraulicValve_Pct := 50.0;      (* Hold position *)
        END_IF;

        (* Verify tension precharged and brakes ready to release *)
        IF (rVoted_TakeUpTension_kN >= 440.0) AND (rStateTimer_s >= 10.0) THEN
            bMechanicalBrakeEngageCmd := FALSE;     (* Lift mechanical caliper brakes *)
            IF bBrakePadsRetractedPermissiv THEN
                rStartupTimer_s := 0.0;
                iFSM_State      := 20;              (* Advance to CONTROLLED_180S_STARTUP *)
            END_IF;
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 20: CONTROLLED_180S_STARTUP (Jerk-Limited Cubic S-Curve Ramp over 180 Seconds)     *)
    (* ----------------------------------------------------------------------------------------- *)
    20:
        bMechanicalBrakeEngageCmd := FALSE;
        rStartupTimer_s := rStartupTimer_s + tScanTime_s;

        (* Normalized S-Curve Trajectory Progress [0.0 to 1.0] *)
        IF rStartupTimer_s < rStartupDuration_s THEN
            rSCurveRampFraction := rStartupTimer_s / rStartupDuration_s;
            (* S-Curve: v(t) = v_max * [ 0.5 * (1.0 - cos(pi * fraction)) ] *)
            rTargetVelocity_ms := rFullSpeedTarget_ms * (0.50 * (1.0 - COS(3.14159265 * rSCurveRampFraction)));
        ELSE
            rTargetVelocity_ms := rFullSpeedTarget_ms;
            iFSM_State         := 30;               (* Advance to FULL_SPEED_BULK_RUN *)
        END_IF;

        (* Abort startup if excessive tension surge or belt rip detected *)
        IF (rVoted_HeadTension_kN >= rMaxAllowableTension_kN) OR (NOT bBeltRipLoopContinuity_OK) THEN
            iFSM_State := 90;
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 30: FULL_SPEED_BULK_RUN (Full Speed 7.50 m/s Bulk Ore Operation & Torque Sharing)   *)
    (* ----------------------------------------------------------------------------------------- *)
    30:
        bMechanicalBrakeEngageCmd := FALSE;
        rTargetVelocity_ms        := rFullSpeedTarget_ms;

        (* Trip to emergency brake if chute plugged or belt rip detected *)
        IF bTransferChutePlugged OR (NOT bBeltRipLoopContinuity_OK) OR bTorqueUnbalanceTrip THEN
            iFSM_State := 90;
        END_IF;

        (* Controlled operator stop *)
        IF NOT bEnable THEN
            rStopTimer_s := 0.0;
            iFSM_State   := 40;                     (* CONTROLLED_INERTIA_STOP *)
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 40: CONTROLLED_INERTIA_STOP (120-Second Regenerative Deceleration Ramp)            *)
    (* ----------------------------------------------------------------------------------------- *)
    40:
        rStopTimer_s := rStopTimer_s + tScanTime_s;
        IF rStopTimer_s < rDecelDuration_s THEN
            rSCurveRampFraction := rStopTimer_s / rDecelDuration_s;
            rTargetVelocity_ms  := rFullSpeedTarget_ms * (0.50 * (1.0 + COS(3.14159265 * rSCurveRampFraction)));
        ELSE
            rTargetVelocity_ms         := 0.00;
            rDrive1_MasterSpeedCmd_Pct := 0.00;
            bMechanicalBrakeEngageCmd  := TRUE;     (* Set parking brakes once stopped *)
            iFSM_State                 := 0;
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 90: EMERGENCY_BRAKE_ABORT (Immediate Caliper Disk Brake Drop & Drive Tripping)     *)
    (* ----------------------------------------------------------------------------------------- *)
    90:
        rDrive1_MasterSpeedCmd_Pct := 0.00;
        rDrive2_TorqueFollower_Pct := 0.00;
        rDrive3_TorqueFollower_Pct := 0.00;
        rDrive4_TorqueFollower_Pct := 0.00;
        bMechanicalBrakeEngageCmd  := TRUE;         (* Explosive disk brake clamp *)

        (* Reset mechanism *)
        IF bResetTripAlarms AND (rVoted_BeltSpeed_ms <= 0.10) AND (NOT bEmergencyStopCommand) THEN
            iFSM_State := 0;
        END_IF;
END_CASE;

(* Transfer Chute Blockage Detection *)
IF (rChuteMaterialLevel_Pct >= 85.0) OR bTransferChutePlugged THEN
    dwConveyorAlarmWord_Pri := dwConveyorAlarmWord_Pri OR 16#0000_0008; (* Bit 3: CHUTE_PLUGGED_HH_TRIP *)
ELSIF rChuteMaterialLevel_Pct >= 70.0 THEN
    dwConveyorAlarmWord_Sec := dwConveyorAlarmWord_Sec OR 16#0000_0004; (* Bit 2: CHUTE_HIGH_LEVEL_WARN *)
END_IF;
"""
    sections.append(s8)

    # -------------------------------------------------------------------------
    # SECTION 9: LOGIC PART 7 - ISA-18.2 ALARMS & DIAGNOSTIC PACKING
    # -------------------------------------------------------------------------
    s9 = """(* ============================================================================================= *)
(* SECTION 7: ISA-18.2 ALARM MATRIX, LATCHING & STATUS WORD BIT-PACKING                          *)
(* ============================================================================================= *)
(* 1. Belt Tension Limit Alarms *)
IF rVoted_HeadTension_kN >= rMaxAllowableTension_kN THEN
    dwConveyorAlarmWord_Pri := dwConveyorAlarmWord_Pri OR 16#0000_0010; (* Bit 4: HEAD_TENSION_HH_TRIP *)
ELSIF rVoted_HeadTension_kN >= 950.0 THEN
    dwConveyorAlarmWord_Sec := dwConveyorAlarmWord_Sec OR 16#0000_0008; (* Bit 3: HEAD_TENSION_H_WARN *)
END_IF;

IF rVoted_TakeUpTension_kN <= rMinAllowableTension_kN THEN
    dwConveyorAlarmWord_Pri := dwConveyorAlarmWord_Pri OR 16#0000_0020; (* Bit 5: TENSION_LOSS_LL_TRIP *)
END_IF;

(* 2. Belt Sag Warning *)
IF rBeltSagRatio_Pct >= 1.50 THEN
    dwConveyorAlarmWord_Sec := dwConveyorAlarmWord_Sec OR 16#0000_0010; (* Bit 4: EXCESSIVE_BELT_SAG_WARN *)
END_IF;

(* Master Reset *)
IF bResetTripAlarms THEN
    dwConveyorAlarmWord_Pri := 16#0000_0000;
    dwConveyorAlarmWord_Sec := 16#0000_0000;
END_IF;

(* --------------------------------------------------------------------------------------------- *)
(* 3. 32-Bit Overland Conveyor Status Word Packing (dwConveyorStatusWord)                        *)
(* --------------------------------------------------------------------------------------------- *)
(* Bits 0..7  : Current FSM State Integer [0..90] *)
(* Bit 8      : bDriveSlipWarning *)
(* Bit 9      : bTorqueUnbalanceTrip *)
(* Bit 10     : bBeltRipFaultDetected *)
(* Bit 11     : bTakeUpOverTravelFault *)
(* Bit 12     : bMPC_Active *)
(* Bit 13     : bGracefulDegradation *)
(* Bit 14     : bMechanicalBrakeEngageCmd *)
(* Bit 15     : bBeltRipLoopContinuity_OK *)
(* Bit 31     : Master Emergency Trip Flag *)
dwConveyorStatusWord := INT_TO_DWORD(iFSM_State);
IF bDriveSlipWarning           THEN dwConveyorStatusWord := dwConveyorStatusWord OR 16#0000_0100; END_IF;
IF bTorqueUnbalanceTrip        THEN dwConveyorStatusWord := dwConveyorStatusWord OR 16#0000_0200; END_IF;
IF bBeltRipFaultDetected       THEN dwConveyorStatusWord := dwConveyorStatusWord OR 16#0000_0400; END_IF;
IF bTakeUpOverTravelFault      THEN dwConveyorStatusWord := dwConveyorStatusWord OR 16#0000_0800; END_IF;
IF bMPC_Active                 THEN dwConveyorStatusWord := dwConveyorStatusWord OR 16#0000_1000; END_IF;
IF bGracefulDegradation        THEN dwConveyorStatusWord := dwConveyorStatusWord OR 16#0000_2000; END_IF;
IF bMechanicalBrakeEngageCmd   THEN dwConveyorStatusWord := dwConveyorStatusWord OR 16#0000_4000; END_IF;
IF bBeltRipLoopContinuity_OK   THEN dwConveyorStatusWord := dwConveyorStatusWord OR 16#0000_8000; END_IF;
IF (iFSM_State = 90)           THEN dwConveyorStatusWord := dwConveyorStatusWord OR 16#8000_0000; END_IF;

END_FUNCTION_BLOCK
"""
    sections.append(s9)

    return "".join(sections)

if __name__ == "__main__":
    code = build_mining_block()
    print(f"Total ST code length: {len(code)} characters")
