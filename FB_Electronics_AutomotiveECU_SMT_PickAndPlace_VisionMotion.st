FUNCTION_BLOCK FB_Electronics_AutomotiveECU_SMT_PickAndPlace_VisionMotion
(*
========================================================================================================================
  LUMINA ADVANCED INDUSTRIAL AUTOMATION AI SWARM — HIGH-DENSITY SYNTHETIC IEC 61131-3 DATASET ENGINE
  PERSONA: 75+ YEARS VETERAN PRINCIPAL AUTOMATION FELLOW & CYBER-PHYSICAL SYSTEMS CHAIR
  
  SYSTEM DESIGNATION : 120,000 CPH HIGH-SPEED DUAL-GANTRY DUAL-LANE SMT PICK-AND-PLACE ASSEMBLY CELL
  APPLICATION        : AUTOMOTIVE ELECTRONIC CONTROL UNITS (ECU), ADAS DOMAIN CONTROLLERS & EV INVERTER GATE DRIVERS
  CORE DISCIPLINE    : ADVANCED ELECTRONICS MANUFACTURING, HIGH-DENSITY PACKAGING & CLOSED-LOOP CYBER-PHYSICAL MOTION
  TARGET MECHANISMS  : DUAL-GANTRY DIRECT-DRIVE LINEAR BRUSHLESS SYNCHRONOUS MOTORS WITH 5TH-ORDER S-CURVE JERK LIMITING,
                       MULTI-NOZZLE ROTARY VACUUM TURRET WITH FAST PIEZORESISTIVE PNEUMATIC DECAY ANALYSIS,
                       ON-THE-FLY HIGH-SPEED CMOS STROBE FLYING VISION ALIGNMENT & SUB-PIXEL EDGE CENTROIDING,
                       DUAL-LANE CONTINUOUS CONVEYOR STAGING WITH LASER BOARD WARPAGE TRIANGULATION COMPENSATION,
                       VOICE-COIL CLOSED-LOOP PIEZO TOUCHDOWN FORCE CONTROL FOR AUTOMOTIVE DIE MICRO-CRACKING PREVENTION.
  DETERMINISTIC Ts   : 0.0005 s (500.0 microseconds / 2.0 kHz Deterministic Hardware Servo Task Scan)
  APPLICABLE CODES   : IPC-9850 (Surface Mount Placement Equipment Performance Verification),
                       IPC-A-610 Class 3 (Acceptability of High-Reliability Automotive Electronics),
                       IPC-7095 (Design and Assembly Process Implementation for BGAs & Micro-BGA Packages),
                       AEC-Q100 / AEC-Q104 (Automotive Electronic Component Stress Qualification),
                       JEDEC J-STD-020E (Moisture/Reflow Sensitivity Classification for Semiconductor Packages),
                       IEC 61508 SIL-3 / ISO 13849-1 PLe Category 4 (Functional Safety of Machinery),
                       ISA-18.2 / IEC 62682 (Management of Alarm Systems for Discrete Manufacturing Industries).
========================================================================================================================

  THEORETICAL & CYBER-PHYSICAL ARCHITECTURE OF 120,000 CPH SMT PLACEMENT FOR AUTOMOTIVE ECUS:
  ----------------------------------------------------------------------------------------------------------------------
  1. DUAL-GANTRY DIRECT-DRIVE LINEAR MOTORS & 5TH-ORDER POLYNOMIAL S-CURVE MOTION PROFILE:
     - High-density automotive ECUs (e.g., ADAS multi-core processing boards with high-pin-count BGA, QFN, and 0201/01005
       decoupling arrays) require unprecedented throughput and sub-micron positioning repeatability.
     - The dual-gantry architecture consists of Master and Slave overhead linear carriages driven by ironless core
       direct-drive synchronous linear brushless servomotors. Operating at accelerations up to a_max = 50.0 m/s2 (5.1 G)
       and a maximum jerk constraint j_max = 250.0 m/s3, conventional 3rd-order trapezoidal or bell-curve profiles generate
       severe high-frequency mechanical frame excitation, leading to gantry flexure, linear encoder misreads, and placement
       inaccuracies exceeding automotive Class 3 allowances.
     - To eliminate high-frequency shock spectra and achieve gantry structural settling times < 8.0 ms upon trajectory arrival,
       the kinematic generator synthesizes a 5th-order polynomial continuous jerk-rate motion trajectory:
           s(tau) = 10 * tau^3 - 15 * tau^4 + 6 * tau^5,   where tau = t / T_motion, tau in [0, 1]
     - The continuous derivatives guarantee that jerk, acceleration, velocity, and displacement are everywhere analytic
       and free of instantaneous step discontinuities, completely eliminating structural resonance modes between 180 Hz
       and 420 Hz in the extruded aluminum and carbon-fiber gantry superstructure.

  2. MULTI-NOZZLE VACUUM MANIFOLD PNEUMATIC DECAY & TOMBSTONE DETECTION DYNAMICS:
     - The placement head integrates a high-speed multi-nozzle rotary turret equipped with micro-piezoresistive vacuum
       pressure transducers (PT_VAC_301A/B/C) with a response bandwidth exceeding 3.5 kHz.
     - Dynamic suction vacuum pressure inside the nozzle channel obeys the first-order pneumatic differential equation:
           d(P_vac)/dt = -(C_eff / V_manifold) * (P_vac - P_venturi) + (Q_leak / V_manifold) * (P_atm - P_vac)
     - For conforming pickup of passive 0201 chip capacitors, ferrite beads, or automotive micro-QFN packages, the vacuum
       must draw down below -75.0 kPa within 12.0 ms of nozzle contact with the embossed tape carrier.
     - A pneumatic decay rate d(P_vac)/dt exceeding 1.85 kPa/ms indicates nozzle tip seal degradation, chipped ceramic nozzle
       orifices, or component tombstoning (angular tilt in the carrier pocket preventing coplanar vacuum seal).
     - If vacuum fails to achieve -75.0 kPa before gantry lift-off, the component pick is categorized as defective,
       preventing the head from traversing over the PCB and preventing solder paste disturbance.

  3. ON-THE-FLY HIGH-SPEED FLYING VISION & SUB-PIXEL CENTROID CORRECTION:
     - While traversing from the motorized feeder bank to the PCB placement site at velocities up to 4.5 m/s, the gantry passes
       over an upward-looking high-speed line/area-scan CMOS camera with synchronous dual-wavelength LED flash strobes (1.2 us).
     - Dedicated hardware FPGA vision processors calculate sub-pixel optical edge coordinates and evaluate:
           Delta_X_fly   : Lateral offset along gantry X-axis [um]
           Delta_Y_fly   : Longitudinal offset along gantry Y-axis [um]
           Delta_Theta   : Angular rotation error [mrad]
           Coplanarity   : 3D laser sheet triangulation ball/lead height deviation [um]
     - The calculated Cartesian corrections (Delta_X, Delta_Y, Delta_Theta) are synthesized directly into the active MPC
       reference trajectory while in flight, achieving zero-stop optical alignment at 120,000 components per hour (CPH).

  4. DUAL-LANE CONVEYOR CLAMPING & LASER BOARD WARPAGE TRIANGULATION:
     - To sustain continuous 120,000 CPH assembly, the machine utilizes an asynchronous dual-lane staging conveyor.
       While Lane 1 executes pick-and-place assembly, Lane 2 indexes the next bare PCB, clamps it dynamically with pneumatic
       side rails, and raises motorized hydraulic support pins beneath the board to counteract placement deflection.
     - Automotive ECUs utilize multi-layer FR4 / High-Tg polyimide substrates (10 to 18 layers) which exhibit thermal and
       manufacturing warpage up to 450 um across a 300 mm x 250 mm panel.
     - A 5-point laser triangulation displacement sensor suite scans the board corners and center, fitting a 2nd-order surface:
           Z_warpage(x, y) = a0 + a1*x + a2*y + a3*x*y + a4*x^2 + a5*y^2   [um]
     - During placement descent, the calculated Z_warpage(x, y) offset is added to the Z voice-coil landing setpoint,
       ensuring exact contact height compensation across the entire warped panel.

  5. VOICE-COIL TOUCHDOWN FORCE & AUTOMOTIVE DIE MICRO-CRACK PREVENTION:
     - Automotive electronic packaging standards (AEC-Q100 / AEC-Q104) strictly prohibit semiconductor die micro-cracking,
       silicon chipping, or solder paste bridging resulting from excessive placement impact.
     - Contact mechanics are governed by viscoelastic Hertzian interaction between the vacuum nozzle ceramic tip, silicon
       die surface, solder paste flux suspension, and copper pad:
           F_contact(t) = K_contact * (Z_head - Z_substrate)^1.5 + C_damping * dZ/dt
     - The maximum allowable placement force is strictly constrained: F_placement <= 2.50 N.
     - Triplicated piezoelectric load cells (WT_FORCE_401A/B/C) sample contact force at 2.0 kHz.
     - If F_placement exceeds 2.50 N, or rises at a rate > 120.0 N/s, a hardware fast interrupt initiates immediate voice coil
       back-off within < 0.5 ms, preventing catastrophic micro-cracking of fragile bare-die silicon.
*)

VAR_INPUT
    (* ============================================================================================== *)
    (* MASTER SAFETY CIRCUITS, HARDWIRED PERMISSIVES & OPERATIONAL CONTROL SIGNALS                   *)
    (* ============================================================================================== *)
    bSystemEnable                       : BOOL;     (* Master 24V DC Hardware Automation Permissive [1=Run] *)
    bProductionRunCmd                   : BOOL;     (* 120,000 CPH Pick-and-Place Production Cycle Run Command [1=Start] *)
    bEmergencyStopHealthy               : BOOL;     (* Dual-Channel Hardwired SIL-3 Safety Circuit Status [1=Healthy] *)
    bAlarmAcknowledge                   : BOOL;     (* HMI Operator Alarm Acknowledge Pushbutton [1=Ack] *)
    bAlarmReset                         : BOOL;     (* Master Safety Interlock & Fault Reset Pushbutton [1=Reset] *)
    bSafetyDoorInterlockLocked          : BOOL;     (* Guard Locking Safety Switch Feedback Status [1=Locked] *)
    bPneumaticPressureMainOK            : BOOL;     (* Cleanroom Dry Air (CDA) Header Pressure Switch (>= 0.60 MPa) [bar] *)
    bMainVacuumSupplyOK                 : BOOL;     (* Central Vacuum Header Supply Pressure Switch (<= -85.0 kPa) [kPa] *)
    
    (* ============================================================================================== *)
    (* DUAL-LANE CONVEYOR STAGING, PCB CLAMPING & SUPPORT PIN HARDWARE FEEDBACK                        *)
    (* ============================================================================================== *)
    nLaneSelectCmd                      : INT;      (* Active Staging Lane Designation Command [1=Lane 1, 2=Lane 2] *)
    bLane1PcbPresent                    : BOOL;     (* Lane 1 Optical Entry Sensor Board Detected Feedback *)
    bLane2PcbPresent                    : BOOL;     (* Lane 2 Optical Entry Sensor Board Detected Feedback *)
    bLane1PcbClamped                    : BOOL;     (* Lane 1 Pneumatic Edge Clamping Cylinder Extended [1=Clamped] *)
    bLane2PcbClamped                    : BOOL;     (* Lane 2 Pneumatic Edge Clamping Cylinder Extended [1=Clamped] *)
    bSupportPinsEngagedFeedback         : BOOL;     (* Motorized Hydraulic Bottom Support Pins Elevated [1=Engaged] *)
    
    (* ============================================================================================== *)
    (* 2oo3 TMR CHANNEL 1: GANTRY X-AXIS OPTICAL LINEAR SCALE ENCODERS (ST_SCALE_101)                 *)
    (* ============================================================================================== *)
    rGantryScale_X_A_um                 : REAL;     (* Gantry X Linear Optical Scale Channel A [um] *)
    rGantryScale_X_B_um                 : REAL;     (* Gantry X Linear Optical Scale Channel B [um] *)
    rGantryScale_X_C_um                 : REAL;     (* Gantry X Linear Optical Scale Channel C [um] *)
    
    (* ============================================================================================== *)
    (* 2oo3 TMR CHANNEL 2: GANTRY Y-AXIS OPTICAL LINEAR SCALE ENCODERS (ST_SCALE_201)                 *)
    (* ============================================================================================== *)
    rGantryScale_Y_A_um                 : REAL;     (* Gantry Y Linear Optical Scale Channel A [um] *)
    rGantryScale_Y_B_um                 : REAL;     (* Gantry Y Linear Optical Scale Channel B [um] *)
    rGantryScale_Y_C_um                 : REAL;     (* Gantry Y Linear Optical Scale Channel C [um] *)
    
    (* ============================================================================================== *)
    (* 2oo3 TMR CHANNEL 3: ROTARY NOZZLE MICRO-PIEZORESISTIVE VACUUM SENSORS (PT_VAC_301)             *)
    (* ============================================================================================== *)
    rNozzleVac_Sensor_A_kPa             : REAL;     (* Placement Nozzle Suction Vacuum Pressure Transducer A [kPa] *)
    rNozzleVac_Sensor_B_kPa             : REAL;     (* Placement Nozzle Suction Vacuum Pressure Transducer B [kPa] *)
    rNozzleVac_Sensor_C_kPa             : REAL;     (* Placement Nozzle Suction Vacuum Pressure Transducer C [kPa] *)
    
    (* ============================================================================================== *)
    (* 2oo3 TMR CHANNEL 4: PIEZOELECTRIC TOUCHDOWN CONTACT FORCE LOAD CELLS (WT_FORCE_401)             *)
    (* ============================================================================================== *)
    rContactForce_Sensor_A_N            : REAL;     (* High-Speed Piezo Touchdown Contact Force Sensor A [N] *)
    rContactForce_Sensor_B_N            : REAL;     (* High-Speed Piezo Touchdown Contact Force Sensor B [N] *)
    rContactForce_Sensor_C_N            : REAL;     (* High-Speed Piezo Touchdown Contact Force Sensor C [N] *)
    
    (* ============================================================================================== *)
    (* 2oo3 TMR CHANNEL 5: MACHINE FRAME TRIAXIAL ACCELEROMETERS (AT_VIB_501)                         *)
    (* ============================================================================================== *)
    rFrameAcc_Sensor_A_mps2             : REAL;     (* Gantry Frame Dynamic Vibration Accelerometer Channel A [m/s2] *)
    rFrameAcc_Sensor_B_mps2             : REAL;     (* Gantry Frame Dynamic Vibration Accelerometer Channel B [m/s2] *)
    rFrameAcc_Sensor_C_mps2             : REAL;     (* Gantry Frame Dynamic Vibration Accelerometer Channel C [m/s2] *)
    
    (* ============================================================================================== *)
    (* BOARD WARPAGE LASER HEIGHT TRIANGULATION SENSORS (LT_WARP_601)                                 *)
    (* ============================================================================================== *)
    rLaserWarpageCorner1_um             : REAL;     (* Laser Triangulation Height Sensor Top-Left Corner [um] *)
    rLaserWarpageCorner2_um             : REAL;     (* Laser Triangulation Height Sensor Top-Right Corner [um] *)
    rLaserWarpageCorner3_um             : REAL;     (* Laser Triangulation Height Sensor Bottom-Left Corner [um] *)
    rLaserWarpageCorner4_um             : REAL;     (* Laser Triangulation Height Sensor Bottom-Right Corner [um] *)
    rLaserWarpageCenter_um              : REAL;     (* Laser Triangulation Height Sensor Board Center [um] *)
    
    (* ============================================================================================== *)
    (* ON-THE-FLY HIGH-SPEED FLYING VISION CAMERA & FPGA COPROCESSOR INPUTS                           *)
    (* ============================================================================================== *)
    rVisionDeltaX_um                    : REAL;     (* Flying Vision Sub-Pixel Optical Offset X-Axis [um] *)
    rVisionDeltaY_um                    : REAL;     (* Flying Vision Sub-Pixel Optical Offset Y-Axis [um] *)
    rVisionDeltaTheta_mrad              : REAL;     (* Flying Vision Sub-Pixel Rotary Theta Offset [mrad] *)
    rVisionCoplanarityMaxDev_um         : REAL;     (* 3D Vision Laser Inspection Max Ball/Lead Non-Coplanarity [um] *)
    bVisionCaptureDone                  : BOOL;     (* Camera FPGA Strobe Image Acquisition Complete Handshake *)
    bVisionInspectionPassed             : BOOL;     (* Optical Edge, Polarity & Packaging Integrity Evaluation [1=Pass] *)
    
    (* ============================================================================================== *)
    (* SMART TAPE FEEDER BANK & DIE PACKAGING SENSORS                                                 *)
    (* ============================================================================================== *)
    bFeederTapeIndexed                  : BOOL;     (* Motorized Feeder Sprocket Pocket Advance Done Handshake *)
    bFeederPartPresent                  : BOOL;     (* Optical Through-Beam Carrier Pocket Part Present Feedback *)
    
    (* ============================================================================================== *)
    (* CAD RECIPE TARGET COORDINATES & AUTOMOTIVE DIE PROTECTION LIMITS                              *)
    (* ============================================================================================== *)
    rCadTargetX_mm                      : REAL;     (* CAD Recipe Nominal Target Placement Position X [mm] *)
    rCadTargetY_mm                      : REAL;     (* CAD Recipe Nominal Target Placement Position Y [mm] *)
    rCadTargetTheta_mrad                : REAL;     (* CAD Recipe Nominal Target Component Orientation [mrad] *)
    rTargetPlacementForce_N             : REAL;     (* Closed-Loop Target Placement Contact Force [N] *)
    rMaxAllowableContactForce_N         : REAL;     (* Automotive Semiconductor Die Micro-Crack Hard Trip Limit (2.50 N) [N] *)
    rMachineFrameTemp_degC              : REAL;     (* Granite Bed / Invar Optical Scale Reference Temperature [deg C] *)
END_VAR

VAR_OUTPUT
    (* ============================================================================================== *)
    (* CELL SUPERVISORY STATUS, ACTIVE LANE & 14-STAGE FINITE STATE MACHINE OUTPUTS                  *)
    (* ============================================================================================== *)
    bSystemReady                        : BOOL;     (* SMT Placement Machine Initialized, Clamped & Ready [1=Ready] *)
    bPickAndPlaceActive                 : BOOL;     (* 120,000 CPH High-Speed Assembly Cycle Actively Running [1=Active] *)
    bEmergencyTripActive                : BOOL;     (* SIL-3 Dynamic Regenerative Braking Contactor Tripped [1=Tripped] *)
    nProductionState                    : INT;      (* 14-Stage Production Finite State Machine Code [0..13] *)
    nActiveLaneUnderPlacement           : INT;      (* Current Active Conveyor Production Lane [1 or 2] *)
    
    (* ============================================================================================== *)
    (* 2oo3 TMR VOTED SENSOR OUTPUT VALUES & PROCESS METRICS                                          *)
    (* ============================================================================================== *)
    rVotedGantryPosX_mm                 : REAL;     (* 2oo3 TMR Voted Gantry Carriage Position X [mm] *)
    rVotedGantryPosY_mm                 : REAL;     (* 2oo3 TMR Voted Gantry Carriage Position Y [mm] *)
    rVotedNozzleVacuum_kPa              : REAL;     (* 2oo3 TMR Voted Placement Nozzle Suction Vacuum [kPa] *)
    rVotedContactForce_N                : REAL;     (* 2oo3 TMR Voted Touchdown Piezoelectric Impact Force [N] *)
    rVotedFrameVib_mps2                 : REAL;     (* 2oo3 TMR Voted Gantry Structural Dynamic Vibration [m/s2] *)
    rVotedPcbWarpageOffsetZ_um          : REAL;     (* Bilinear Interpolated Board Warpage Z Height Offset [um] *)
    
    (* ============================================================================================== *)
    (* 6-STATE CYBER-PHYSICAL OBSERVER ESTIMATES & PROCESS PHENOMENOLOGY                              *)
    (* ============================================================================================== *)
    rEstTrackingErrorX_um               : REAL;     (* Real-Time Estimated Gantry X Tracking Error (x1) [um] *)
    rEstTrackingErrorY_um               : REAL;     (* Real-Time Estimated Gantry Y Tracking Error (x2) [um] *)
    rEstVacuumDecayRate_kPas            : REAL;     (* Real-Time Estimated Vacuum Pneumatic Decay Rate (x3) [kPa/s] *)
    rEstContactForce_N                  : REAL;     (* Real-Time Estimated Die Touchdown Contact Force (x4) [N] *)
    rEstThetaOffset_mrad                : REAL;     (* Real-Time Estimated Component Angular Offset (x5) [mrad] *)
    rEstStructuralVibRMS_mps2           : REAL;     (* Real-Time Estimated Structural Vibration RMS (x6) [m/s2] *)
    
    (* ============================================================================================== *)
    (* DIRECT ACTUATOR MANIPULATED COMMAND SIGNALS                                                    *)
    (* ============================================================================================== *)
    rLinearMotorCurrentCmdX_pct         : REAL;     (* Linear Motor X-Axis High-Bandwidth PWM Current Command [%] *)
    rLinearMotorCurrentCmdY_pct         : REAL;     (* Linear Motor Y-Axis High-Bandwidth PWM Current Command [%] *)
    rVoiceCoilZForceCmd_pct             : REAL;     (* Placement Head Voice Coil Z-Axis Touchdown Force Servo [%] *)
    rVacuumVenturiSolenoidCmd_pct       : REAL;     (* Multi-Nozzle Fast High-Flow Vacuum Venturi Solenoid [%] *)
    rPositiveBlowOffPuffCmd_pct         : REAL;     (* Positive Pressure Micro-Pulse Component Release Puff Valve [%] *)
    
    (* ============================================================================================== *)
    (* CONVEYOR STAGING, TOOLING & OPTICAL STROBE HARDWARE COMMANDS                                   *)
    (* ============================================================================================== *)
    bConveyorRunLane1                   : BOOL;     (* Lane 1 Motorized Belt Conveyor Feed Command *)
    bConveyorRunLane2                   : BOOL;     (* Lane 2 Motorized Belt Conveyor Feed Command *)
    bLaneClampEngaged                   : BOOL;     (* Pneumatic Board Edge Clamp Solenoid Energize Command *)
    bSupportPinsEngaged                 : BOOL;     (* Hydraulic Underside PCB Support Pins Elevate Command *)
    bFeederAdvancePulse                 : BOOL;     (* Smart Feeder Motorized Sprocket Index Advance Pulse *)
    bVisionStrobeTrigger                : BOOL;     (* Flying Vision Ultra-Fast FPGA Flash Strobe Trigger *)
    
    (* ============================================================================================== *)
    (* PRODUCTION TELEMETRY, THROUGHPUT & VIBRATION SETTLING METRICS                                  *)
    (* ============================================================================================== *)
    nComponentsPlacedTotal              : DINT;     (* Cumulative Placed Conforming Components Production Counter *)
    rInstantaneousCPH                   : REAL;     (* Real-Time Placement Throughput [components/hour] *)
    rCycleTimePlacement_ms              : REAL;     (* Last Single Component Pick-to-Place Cycle Duration [ms] *)
    rStructuralVibrationSettlingTime_ms : REAL;     (* Mechanical Frame Acceleration Settling Time (< 8.0 ms) [ms] *)
    
    (* ============================================================================================== *)
    (* BIT-PACKED STATUS WORDS & ISA-18.2 TELEMETRY REGISTERS                                         *)
    (* ============================================================================================== *)
    dwStatusWord1                       : DWORD;    (* Bit-Packed Operational State, Interlocks & Staging Permissives *)
    dwStatusWord2                       : DWORD;    (* Bit-Packed TMR Channel Degradation Modes & Vision Status *)
    dwAlarmWord1                        : DWORD;    (* ISA-18.2 High-High & Low-Low Safety Critical Trips *)
    dwAlarmWord2                        : DWORD;    (* ISA-18.2 High & Low Process Warnings & Minor Degradations *)
    dwFirstOutWord                      : DWORD;    (* Root-Cause First-Out Diagnostic Alarm Register *)
END_VAR

VAR
    (* ============================================================================================== *)
    (* DETERMINISTIC EXECUTION CONSTANTS & ARCHITECTURAL DIMENSIONS                                   *)
    (* ============================================================================================== *)
    T_SCAN_SEC                          : REAL := 0.0005;   (* Servo Task Deterministic Scan Cycle dt = 0.5 ms [s] *)
    DIM_STATE                           : INT := 6;         (* Cyber-Physical State Vector Dimension (6x6) *)
    DIM_INPUT                           : INT := 5;         (* Manipulated Actuator Vector Dimension (u1..u5) *)
    DIM_OUTPUT                          : INT := 6;         (* Measured Process Vector Dimension (y1..y6) *)
    MPC_HORIZON_STEPS                   : INT := 5;         (* Receding-Horizon Prediction Steps N = 5 *)
    MPC_PGD_ITERATIONS                  : INT := 10;        (* 10 Unrolled Projected Gradient Descent Iterations *)
    
    (* ============================================================================================== *)
    (* 6-STATE FIRST-PRINCIPLES DISCRETE STATE-SPACE MATRICES                                         *)
    (* x[k+1] = A * x[k] + B * u[k]                                                                   *)
    (* y[k]   = C * x[k] + D * u[k]                                                                   *)
    (* x_hat[k+1] = A * x_hat[k] + B * u[k] + L * (y[k] - C * x_hat[k])                                *)
    (* States:                                                                                        *)
    (* x1 = Gantry X-axis position tracking error [um]                                                *)
    (* x2 = Gantry Y-axis position tracking error [um]                                                *)
    (* x3 = Placement head rotary nozzle vacuum pressure [kPa]                                        *)
    (* x4 = Placement component Z-axis contact force [N]                                              *)
    (* x5 = Placement angular theta offset [mrad]                                                     *)
    (* x6 = Structural gantry vibration RMS acceleration [m/s2]                                       *)
    (* Actuators:                                                                                     *)
    (* u1 = Linear motor X-axis drive current [%]                                                     *)
    (* u2 = Linear motor Y-axis drive current [%]                                                     *)
    (* u3 = Rotary placement head voice coil Z-axis force servo [%]                                   *)
    (* u4 = Multi-nozzle vacuum venturi solenoid [%]                                                  *)
    (* u5 = High-speed positive pressure blow-off puff valve [%]                                      *)
    (* ============================================================================================== *)
    mat_A                               : ARRAY[1..6, 1..6] OF REAL;    (* State Transition Matrix A (6x6) *)
    mat_B                               : ARRAY[1..6, 1..5] OF REAL;    (* Input Coupling Matrix B (6x5) *)
    mat_C                               : ARRAY[1..6, 1..6] OF REAL;    (* Measurement Output Matrix C (6x6) *)
    mat_D                               : ARRAY[1..6, 1..5] OF REAL;    (* Direct Feedthrough Matrix D (6x5) *)
    mat_L                               : ARRAY[1..6, 1..6] OF REAL;    (* Observer Innovation Gain L (6x6) *)
    bMatricesInitialized                : BOOL := FALSE;                (* Matrix Static Load Latch *)
    
    (* State, Measurement & Control Vectors *)
    vec_x                               : ARRAY[1..6] OF REAL;          (* Cyber-Physical Estimated State x[k] *)
    vec_x_pred                          : ARRAY[1..6] OF REAL;          (* A-Priori Predicted State x_pred[k+1] *)
    vec_y_meas                          : ARRAY[1..6] OF REAL;          (* Measured Output Vector y[k] *)
    vec_y_est                           : ARRAY[1..6] OF REAL;          (* Observer Estimated Output y_hat[k] *)
    vec_innov                           : ARRAY[1..6] OF REAL;          (* Innovation Residual Vector y - y_hat *)
    vec_u                               : ARRAY[1..5] OF REAL;          (* Current Manipulated Actuator Vector u[k] *)
    vec_u_prev                          : ARRAY[1..5] OF REAL;          (* Previous Step Actuator Vector u[k-1] *)
    vec_x_ref                           : ARRAY[1..6] OF REAL;          (* Reference State Setpoint Vector x_ref *)
    vec_u_ref                           : ARRAY[1..5] OF REAL;          (* Nominal Equilibrium Actuator Vector u_ref *)
    
    (* ============================================================================================== *)
    (* MODEL PREDICTIVE CONTROL (MPC) COST MATRICES, BOUNDS & TRAJECTORY BUFFERS                     *)
    (* Quadratic Cost: J = sum( (x-xref)^T*Q*(x-xref) + (u-uref)^T*R*(u-uref) + du^T*S*du ) + Term(P) *)
    (* ============================================================================================== *)
    vec_Q_diag                          : ARRAY[1..6] OF REAL;          (* State Tracking Error Penalty Diagonal Q *)
    vec_R_diag                          : ARRAY[1..5] OF REAL;          (* Actuator Effort Penalty Diagonal R *)
    vec_S_diag                          : ARRAY[1..5] OF REAL;          (* Actuator Slew Rate Penalty Diagonal S *)
    vec_P_diag                          : ARRAY[1..6] OF REAL;          (* Terminal State Penalty Diagonal P *)
    vec_u_min                           : ARRAY[1..5] OF REAL;          (* Actuator Lower Saturation Limit Box *)
    vec_u_max                           : ARRAY[1..5] OF REAL;          (* Actuator Upper Saturation Limit Box *)
    vec_du_slew_max                     : ARRAY[1..5] OF REAL;          (* Max Allowable Actuator Rate of Change per Ts *)
    
    arr_x_traj                          : ARRAY[0..5, 1..6] OF REAL;    (* MPC Predicted State Trajectory [k, state] *)
    arr_u_traj                          : ARRAY[0..4, 1..5] OF REAL;    (* MPC Predicted Control Input Trajectory [k, act] *)
    arr_grad_u                          : ARRAY[0..4, 1..5] OF REAL;    (* Projected Gradient Vector arr_grad_u [k, act] *)
    arr_cost_state                      : ARRAY[1..5, 1..6] OF REAL;    (* Backwards Adjoint Cost Multipliers *)
    rPgdAlpha                           : REAL := 0.0385;               (* PGD Optimization Gradient Step Factor *)
    rMpcTotalCost                       : REAL := 0.0;                  (* Evaluated Objective Cost Functional *)
    
    (* ============================================================================================== *)
    (* 5TH-ORDER POLYNOMIAL S-CURVE JERK-LIMITED TRAJECTORY REGISTERS                                 *)
    (* j_max = 250 m/s3, a_max = 50 m/s2, v_max = 5.0 m/s, Structural Settling Time < 8.0 ms         *)
    (* ============================================================================================== *)
    rKinJerkMax_mps3                    : REAL := 250.0;    (* Maximum Allowable Kinematic Jerk [m/s3] *)
    rKinAccMax_mps2                     : REAL := 50.0;     (* Maximum Allowable Linear Motor Acceleration [m/s2] *)
    rKinVelMax_mps                      : REAL := 5.0;      (* Maximum High-Speed Rapid Traverse Velocity [m/s] *)
    rProfileCurrentPosX_mm              : REAL := 0.0;      (* S-Curve Commanded Profile Position X [mm] *)
    rProfileCurrentPosY_mm              : REAL := 0.0;      (* S-Curve Commanded Profile Position Y [mm] *)
    rProfileCurrentVelX_mps             : REAL := 0.0;      (* Profile Velocity X [m/s] *)
    rProfileCurrentVelY_mps             : REAL := 0.0;      (* Profile Velocity Y [m/s] *)
    rProfileCurrentAccX_mps2            : REAL := 0.0;      (* Profile Acceleration X [m/s2] *)
    rProfileCurrentAccY_mps2            : REAL := 0.0;      (* Profile Acceleration Y [m/s2] *)
    rPolyTau                            : REAL := 0.0;      (* Normalized Polynomial Time Parameter tau in [0, 1] *)
    rTrajectoryTotalTime_s              : REAL := 0.045;    (* Trajectory Segment Duration [s] *)
    rTrajectoryTimer_s                  : REAL := 0.0;      (* Trajectory Elapsed Timer [s] *)
    bTrajectoryActive                   : BOOL := FALSE;    (* High-Speed Trajectory S-Curve Running Flag *)
    
    (* ============================================================================================== *)
    (* VACUUM PNEUMATIC DECAY ODE & TOMBSTONE DETECTION DYNAMICS                                      *)
    (* dP/dt = -(C_eff/V)*(P_vac - P_venturi) + Q_leak; Threshold P_vac <= -75 kPa                    *)
    (* ============================================================================================== *)
    rNozzleVacPrev_kPa                  : REAL := 0.0;      (* Previous Scan Vacuum Value [kPa] *)
    rCalculatedDecaySlope_kPas          : REAL := 0.0;      (* Differential Vacuum Rate d(P_vac)/dt [kPa/s] *)
    rVacuumDwellTimer_s                 : REAL := 0.0;      (* Vacuum Draw-Down Verification Timer [s] *)
    bComponentTombstoneDetected         : BOOL := FALSE;    (* Tombstone Angular Leak Flaw Flag *)
    bNozzleSealConforming               : BOOL := FALSE;    (* P_vac <= -75.0 kPa Seal Conformance Flag *)
    
    (* ============================================================================================== *)
    (* BOARD WARPAGE LASER BILINEAR SURFACE MODEL REGISTERS                                           *)
    (* Z_warpage(x, y) = a0 + a1*x + a2*y + a3*x*y                                                    *)
    (* ============================================================================================== *)
    rWarpCoeff_a0                       : REAL := 0.0;      (* Baseline Center Height Bias [um] *)
    rWarpCoeff_a1                       : REAL := 0.0;      (* Linear Tilt Coefficient along X [um/mm] *)
    rWarpCoeff_a2                       : REAL := 0.0;      (* Linear Tilt Coefficient along Y [um/mm] *)
    rWarpCoeff_a3                       : REAL := 0.0;      (* Cross-Coupling Twisting Warpage [um/mm2] *)
    bWarpageMapValid                    : BOOL := FALSE;    (* Active PCB Warpage Surface Model Latch *)
    
    (* ============================================================================================== *)
    (* 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) VOTING STRUCTURES & 20 MS PERSISTENCE TIMERS             *)
    (* ============================================================================================== *)
    (* TMR Triplet 1: Gantry X Linear Scale Encoders *)
    rScaleX_Delta_AB                    : REAL;     (* Delta |ScaleX A - ScaleX B| [um] *)
    rScaleX_Delta_BC                    : REAL;     (* Delta |ScaleX B - ScaleX C| [um] *)
    rScaleX_Delta_CA                    : REAL;     (* Delta |ScaleX C - ScaleX A| [um] *)
    rScaleX_DiscrepancyLimit_um         : REAL := 5.0;      (* Permissible Scale Deviation Margin [um] *)
    rScaleX_DiscrepancyTimer_s          : REAL := 0.0;      (* Discrepancy Persistence Timer (20 ms) [s] *)
    bScaleX_ChanA_Healthy               : BOOL := TRUE;     (* Scale X Channel A Health State *)
    bScaleX_ChanB_Healthy               : BOOL := TRUE;     (* Scale X Channel B Health State *)
    bScaleX_ChanC_Healthy               : BOOL := TRUE;     (* Scale X Channel C Health State *)
    nScaleX_VotingMode                  : INT := 3;         (* 3=2oo3 Median, 2=1oo2 Avg, 1=1oo1, 0=Trip *)
    
    (* TMR Triplet 2: Gantry Y Linear Scale Encoders *)
    rScaleY_Delta_AB                    : REAL;     (* Delta |ScaleY A - ScaleY B| [um] *)
    rScaleY_Delta_BC                    : REAL;     (* Delta |ScaleY B - ScaleY C| [um] *)
    rScaleY_Delta_CA                    : REAL;     (* Delta |ScaleY C - ScaleY A| [um] *)
    rScaleY_DiscrepancyLimit_um         : REAL := 5.0;      (* Permissible Scale Deviation Margin [um] *)
    rScaleY_DiscrepancyTimer_s          : REAL := 0.0;      (* Discrepancy Persistence Timer (20 ms) [s] *)
    bScaleY_ChanA_Healthy               : BOOL := TRUE;     (* Scale Y Channel A Health State *)
    bScaleY_ChanB_Healthy               : BOOL := TRUE;     (* Scale Y Channel B Health State *)
    bScaleY_ChanC_Healthy               : BOOL := TRUE;     (* Scale Y Channel C Health State *)
    nScaleY_VotingMode                  : INT := 3;         (* 3=2oo3 Median, 2=1oo2 Avg, 1=1oo1, 0=Trip *)
    
    (* TMR Triplet 3: Rotary Nozzle Piezoresistive Vacuum Transducers *)
    rVac_Delta_AB                       : REAL;     (* Delta |Vac A - Vac B| [kPa] *)
    rVac_Delta_BC                       : REAL;     (* Delta |Vac B - Vac C| [kPa] *)
    rVac_Delta_CA                       : REAL;     (* Delta |Vac C - Vac A| [kPa] *)
    rVac_DiscrepancyLimit_kPa           : REAL := 5.5;      (* Vacuum Discrepancy Margin [kPa] *)
    rVac_DiscrepancyTimer_s             : REAL := 0.0;      (* Discrepancy Persistence Timer (20 ms) [s] *)
    bVac_ChanA_Healthy                  : BOOL := TRUE;     (* Vacuum Sensor A Health State *)
    bVac_ChanB_Healthy                  : BOOL := TRUE;     (* Vacuum Sensor B Health State *)
    bVac_ChanC_Healthy                  : BOOL := TRUE;     (* Vacuum Sensor C Health State *)
    nVac_VotingMode                     : INT := 3;         (* 3=2oo3 Median, 2=1oo2, 1=1oo1, 0=Trip *)
    
    (* TMR Triplet 4: Touchdown Contact Force Piezo Load Cells *)
    rForce_Delta_AB                     : REAL;     (* Delta |Force A - Force B| [N] *)
    rForce_Delta_BC                     : REAL;     (* Delta |Force B - Force C| [N] *)
    rForce_Delta_CA                     : REAL;     (* Delta |Force C - Force A| [N] *)
    rForce_DiscrepancyLimit_N           : REAL := 0.35;     (* Force Sensor Discrepancy Margin [N] *)
    rForce_DiscrepancyTimer_s           : REAL := 0.0;      (* Discrepancy Persistence Timer (20 ms) [s] *)
    bForce_ChanA_Healthy                : BOOL := TRUE;     (* Force Sensor A Health State *)
    bForce_ChanB_Healthy                : BOOL := TRUE;     (* Force Sensor B Health State *)
    bForce_ChanC_Healthy                : BOOL := TRUE;     (* Force Sensor C Health State *)
    nForce_VotingMode                   : INT := 3;         (* 3=2oo3 Median, 2=1oo2, 1=1oo1, 0=Trip *)
    
    (* TMR Triplet 5: Gantry Frame Triaxial Accelerometers *)
    rVib_Delta_AB                       : REAL;     (* Delta |Vib A - Vib B| [m/s2] *)
    rVib_Delta_BC                       : REAL;     (* Delta |Vib B - Vib C| [m/s2] *)
    rVib_Delta_CA                       : REAL;     (* Delta |Vib C - Vib A| [m/s2] *)
    rVib_DiscrepancyLimit_mps2          : REAL := 4.5;      (* Vibration Discrepancy Margin [m/s2] *)
    rVib_DiscrepancyTimer_s             : REAL := 0.0;      (* Discrepancy Persistence Timer (20 ms) [s] *)
    bVib_ChanA_Healthy                  : BOOL := TRUE;     (* Vibration Sensor A Health State *)
    bVib_ChanB_Healthy                  : BOOL := TRUE;     (* Vibration Sensor B Health State *)
    bVib_ChanC_Healthy                  : BOOL := TRUE;     (* Vibration Sensor C Health State *)
    nVib_VotingMode                     : INT := 3;         (* 3=2oo3 Median, 2=1oo2, 1=1oo1, 0=Trip *)
    
    (* ============================================================================================== *)
    (* 14-STAGE FINITE STATE MACHINE (FSM) STEP REGISTERS & ACTION TIMERS                             *)
    (* ============================================================================================== *)
    nFsmState                           : INT := 0;         (* Current Active Execution Stage [0..13] *)
    nFsmStatePrev                       : INT := -1;        (* Previous Cycle State Register *)
    rFsmStateDwell_s                    : REAL := 0.0;      (* Active State Elapsed Timer [s] *)
    rFeederIndexDwell_s                 : REAL := 0.0;      (* Feeder Tape Advance Wait Timer [s] *)
    rPickupDescentTimer_s               : REAL := 0.0;      (* Pickup Descent Voice Coil Timer [s] *)
    rVisionStrobeSyncTimer_s            : REAL := 0.0;      (* Camera Trigger Synchronization Timer [s] *)
    rTouchdownForceDwell_s              : REAL := 0.0;      (* Placement Wetting Force Dwell [s] *)
    rBlowOffPuffTimer_s                 : REAL := 0.0;      (* Positive Pressure Puff Duration [s] *)
    rEmergencyBrakeHoldTimer_s          : REAL := 0.0;      (* Dynamic Braking Hold-Off Timer [s] *)
    
    (* Cycle & Throughput Diagnostics *)
    rCycleTimer_s                       : REAL := 0.0;      (* Current Component Placement Cycle Timer [s] *)
    rLastCycleDuration_s                : REAL := 0.030;    (* Measured Duration of Last Completed Part [s] *)
    rSettlingTimerAccum_s               : REAL := 0.0;      (* Mechanical Structural Vibration Settling Integrator [s] *)
    nPlacementsCountInternal            : DINT := 0;        (* Conforming Automotive Component Placements *)
    nDefectiveRejectionsCount           : DINT := 0;        (* Optical / Vacuum / Force Rejection Counter *)
    
    (* ============================================================================================== *)
    (* ISA-18.2 MULTI-TIER PROCESS ALARM SETPOINTS, DEADBANDS & INTERLOCK LATCHES                     *)
    (* ============================================================================================== *)
    (* Contact Force Alarms (Die Micro-Crack Protection: Hard Limit 2.50 N) *)
    rAlmForce_HH_N                      : REAL := 2.50;     (* High-High Touchdown Force Hard Trip (Die Crack Hazard) [N] *)
    rAlmForce_H_N                       : REAL := 2.10;     (* High Touchdown Force Process Warning [N] *)
    rAlmForce_L_N                       : REAL := 1.20;     (* Low Placement Force Solder Wetting Warning [N] *)
    rAlmForce_LL_N                      : REAL := 0.20;     (* Low-Low No-Contact Missing Solder Deposit Trip [N] *)
    rAlmForce_Deadband_N                : REAL := 0.08;     (* Contact Force Clearance Hysteresis Deadband [N] *)
    
    (* Vacuum Pressure Alarms (Suction Loss & Tombstone Detection) *)
    rAlmVac_HH_kPa                      : REAL := -45.0;    (* High-High Suction Failure Trip (Dropped Die) [kPa] *)
    rAlmVac_H_kPa                       : REAL := -65.0;    (* High Vacuum Flow Restriction / Partial Seal Warning [kPa] *)
    rAlmVac_L_kPa                       : REAL := -75.0;    (* Low Vacuum Conforming Pickup Threshold [kPa] *)
    rAlmVac_LL_kPa                      : REAL := -90.0;    (* Low-Low Deep Vacuum Manifold Saturation [kPa] *)
    rAlmVac_Deadband_kPa                : REAL := 2.5;      (* Vacuum Clearance Hysteresis Deadband [kPa] *)
    
    (* Structural Gantry Vibration Alarms (Shock & Settling Verification) *)
    rAlmVib_HH_mps2                     : REAL := 45.0;     (* High-High Severe Structural Impact Collision Trip [m/s2] *)
    rAlmVib_H_mps2                      : REAL := 25.0;     (* High Gantry Resonance Harmonic Vibration Warning [m/s2] *)
    rAlmVib_Deadband_mps2               : REAL := 3.0;      (* Vibration Clearance Hysteresis Deadband [m/s2] *)
    
    (* Gantry Tracking Error Alarms *)
    rAlmTrack_HH_um                     : REAL := 15.0;     (* High-High Linear Contouring Deviation Trip [um] *)
    rAlmTrack_H_um                      : REAL := 6.0;      (* High Linear Motor S-Curve Following Warning [um] *)
    rAlmTrack_Deadband_um               : REAL := 1.0;      (* Tracking Clearance Hysteresis Deadband [um] *)
    
    (* Component Angular Alignment Alarms *)
    rAlmTheta_HH_mrad                   : REAL := 8.0;      (* High-High Angular Misalignment Optical Reject Trip [mrad] *)
    rAlmTheta_H_mrad                    : REAL := 3.5;      (* High Component Theta Skew Process Warning [mrad] *)
    rAlmTheta_Deadband_mrad             : REAL := 0.5;      (* Angular Clearance Hysteresis Deadband [mrad] *)
    
    (* Active Alarm Condition Bit Latches *)
    bAlmForce_HH_Active                 : BOOL := FALSE;    (* Latched Force High-High Trip *)
    bAlmForce_H_Active                  : BOOL := FALSE;    (* Latched Force High Warning *)
    bAlmForce_L_Active                  : BOOL := FALSE;    (* Latched Force Low Warning *)
    bAlmForce_LL_Active                 : BOOL := FALSE;    (* Latched Force Low-Low Trip *)
    bAlmVac_HH_Active                   : BOOL := FALSE;    (* Latched Vacuum High-High Trip *)
    bAlmVac_H_Active                    : BOOL := FALSE;    (* Latched Vacuum High Warning *)
    bAlmVib_HH_Active                   : BOOL := FALSE;    (* Latched Vibration High-High Trip *)
    bAlmVib_H_Active                    : BOOL := FALSE;    (* Latched Vibration High Warning *)
    bAlmTrack_HH_Active                 : BOOL := FALSE;    (* Latched Tracking Error High-High Trip *)
    bAlmTrack_H_Active                  : BOOL := FALSE;    (* Latched Tracking Error High Warning *)
    bAlmTheta_HH_Active                 : BOOL := FALSE;    (* Latched Theta High-High Trip *)
    bAlmTheta_H_Active                  : BOOL := FALSE;    (* Latched Theta High Warning *)
    bFastInterruptBrakeTrip             : BOOL := FALSE;    (* Fast Interrupt Dynamic Regenerative Brake Trip *)
    
    (* Loop Indices & Scratchpad Computational Scalars *)
    idx_i                               : INT;              (* Primary Outer Matrix Row Index *)
    idx_j                               : INT;              (* Secondary Matrix Column Index *)
    idx_k                               : INT;              (* Tertiary Prediction Horizon Step Index *)
    idx_m                               : INT;              (* Quaternary Manipulated Actuator Index *)
    idx_iter                            : INT;              (* Unrolled Projected Gradient Descent Loop Counter *)
    rTempSum                            : REAL;             (* Accumulation Storage Scalar *)
    rTempGrad                           : REAL;             (* Analytical Gradient Component *)
    rTempCand                           : REAL;             (* PGD Step Candidate Scalar *)
END_VAR

(* ==================================================================================================================== *)
(* INITIALIZATION PHASE: FIRST-PRINCIPLES CYBER-PHYSICAL STATE-SPACE MATRICES A, B, C, D, L & MPC WEIGHTS               *)
(* Discrete-time model evaluated at Ts = 0.5 ms (500.0 microseconds):                                                  *)
(* x1 = Gantry X-axis tracking error [um]                                                                              *)
(* x2 = Gantry Y-axis tracking error [um]                                                                              *)
(* x3 = Placement head rotary nozzle vacuum pressure [kPa]                                                            *)
(* x4 = Placement component Z-axis contact force [N]                                                                  *)
(* x5 = Placement angular theta offset [mrad]                                                                         *)
(* x6 = Structural gantry vibration RMS acceleration [m/s2]                                                           *)
(* Actuators: u1=LinMotX [%], u2=LinMotY [%], u3=VoiceCoilZ [%], u4=VenturiVac [%], u5=BlowOffPuff [%]                 *)
(* ==================================================================================================================== *)
IF NOT bMatricesInitialized THEN
    (* Reset all discrete state-space matrices *)
    FOR idx_i := 1 TO 6 DO
        FOR idx_j := 1 TO 6 DO
            mat_A[idx_i, idx_j] := 0.0;
            mat_C[idx_i, idx_j] := 0.0;
            mat_L[idx_i, idx_j] := 0.0;
        END_FOR;
        FOR idx_m := 1 TO 5 DO
            mat_B[idx_i, idx_m] := 0.0;
            mat_D[idx_i, idx_m] := 0.0;
        END_FOR;
    END_FOR;
    
    (* State Transition Matrix A (6x6) *)
    mat_A[1, 1] := 0.98540;
    mat_A[1, 2] := 0.00120;
    mat_A[1, 3] := 0.00000;
    mat_A[1, 4] := 0.00000;
    mat_A[1, 5] := 0.00045;
    mat_A[1, 6] := 0.00280;
    mat_A[2, 1] := 0.00085;
    mat_A[2, 2] := 0.98420;
    mat_A[2, 3] := 0.00000;
    mat_A[2, 4] := 0.00000;
    mat_A[2, 5] := 0.00062;
    mat_A[2, 6] := 0.00315;
    mat_A[3, 1] := 0.00000;
    mat_A[3, 2] := 0.00000;
    mat_A[3, 3] := 0.96520;
    mat_A[3, 4] := 0.00210;
    mat_A[3, 5] := 0.00000;
    mat_A[3, 6] := 0.00000;
    mat_A[4, 1] := 0.00000;
    mat_A[4, 2] := 0.00000;
    mat_A[4, 3] := 0.00140;
    mat_A[4, 4] := 0.89250;
    mat_A[4, 5] := 0.00000;
    mat_A[4, 6] := -0.01450;
    mat_A[5, 1] := 0.00012;
    mat_A[5, 2] := 0.00015;
    mat_A[5, 3] := 0.00000;
    mat_A[5, 4] := 0.00000;
    mat_A[5, 5] := 0.97850;
    mat_A[5, 6] := 0.00185;
    mat_A[6, 1] := 0.00850;
    mat_A[6, 2] := 0.00920;
    mat_A[6, 3] := 0.00000;
    mat_A[6, 4] := 0.01250;
    mat_A[6, 5] := 0.00210;
    mat_A[6, 6] := 0.88500;
    
    (* Input Coupling Matrix B (6x5) *)
    mat_B[1, 1] := -0.04520;
    mat_B[1, 2] := -0.00110;
    mat_B[1, 3] := 0.00000;
    mat_B[1, 4] := 0.00000;
    mat_B[1, 5] := 0.00000;
    mat_B[2, 1] := -0.00095;
    mat_B[2, 2] := -0.04680;
    mat_B[2, 3] := 0.00000;
    mat_B[2, 4] := 0.00000;
    mat_B[2, 5] := 0.00000;
    mat_B[3, 1] := 0.00000;
    mat_B[3, 2] := 0.00000;
    mat_B[3, 3] := 0.00000;
    mat_B[3, 4] := -0.42500;
    mat_B[3, 5] := 0.68500;
    mat_B[4, 1] := 0.00000;
    mat_B[4, 2] := 0.00000;
    mat_B[4, 3] := 0.07850;
    mat_B[4, 4] := 0.00000;
    mat_B[4, 5] := -0.01200;
    mat_B[5, 1] := 0.00000;
    mat_B[5, 2] := 0.00000;
    mat_B[5, 3] := 0.00000;
    mat_B[5, 4] := 0.00000;
    mat_B[5, 5] := 0.00000;
    mat_B[6, 1] := 0.05200;
    mat_B[6, 2] := 0.05450;
    mat_B[6, 3] := 0.01850;
    mat_B[6, 4] := 0.00000;
    mat_B[6, 5] := 0.00450;
    
    (* Measurement Output Matrix C (6x6) *)
    mat_C[1, 1] := 1.00000;
    mat_C[1, 2] := 0.00000;
    mat_C[1, 3] := 0.00000;
    mat_C[1, 4] := 0.00000;
    mat_C[1, 5] := 0.00000;
    mat_C[1, 6] := 0.00000;
    mat_C[2, 1] := 0.00000;
    mat_C[2, 2] := 1.00000;
    mat_C[2, 3] := 0.00000;
    mat_C[2, 4] := 0.00000;
    mat_C[2, 5] := 0.00000;
    mat_C[2, 6] := 0.00000;
    mat_C[3, 1] := 0.00000;
    mat_C[3, 2] := 0.00000;
    mat_C[3, 3] := 1.00000;
    mat_C[3, 4] := 0.00000;
    mat_C[3, 5] := 0.00000;
    mat_C[3, 6] := 0.00000;
    mat_C[4, 1] := 0.00000;
    mat_C[4, 2] := 0.00000;
    mat_C[4, 3] := 0.00000;
    mat_C[4, 4] := 1.00000;
    mat_C[4, 5] := 0.00000;
    mat_C[4, 6] := 0.00000;
    mat_C[5, 1] := 0.00000;
    mat_C[5, 2] := 0.00000;
    mat_C[5, 3] := 0.00000;
    mat_C[5, 4] := 0.00000;
    mat_C[5, 5] := 1.00000;
    mat_C[5, 6] := 0.00000;
    mat_C[6, 1] := 0.00000;
    mat_C[6, 2] := 0.00000;
    mat_C[6, 3] := 0.00000;
    mat_C[6, 4] := 0.00000;
    mat_C[6, 5] := 0.00000;
    mat_C[6, 6] := 1.00000;
    
    (* Direct Feedthrough Matrix D (6x5) *)
    mat_D[1, 1] := 0.00050;
    mat_D[1, 2] := 0.00000;
    mat_D[1, 3] := 0.00000;
    mat_D[1, 4] := 0.00000;
    mat_D[1, 5] := 0.00000;
    mat_D[2, 1] := 0.00000;
    mat_D[2, 2] := 0.00050;
    mat_D[2, 3] := 0.00000;
    mat_D[2, 4] := 0.00000;
    mat_D[2, 5] := 0.00000;
    mat_D[3, 1] := 0.00000;
    mat_D[3, 2] := 0.00000;
    mat_D[3, 3] := 0.00000;
    mat_D[3, 4] := 0.01500;
    mat_D[3, 5] := -0.01800;
    mat_D[4, 1] := 0.00000;
    mat_D[4, 2] := 0.00000;
    mat_D[4, 3] := 0.00420;
    mat_D[4, 4] := 0.00000;
    mat_D[4, 5] := 0.00000;
    mat_D[5, 1] := 0.00000;
    mat_D[5, 2] := 0.00000;
    mat_D[5, 3] := 0.00000;
    mat_D[5, 4] := 0.00000;
    mat_D[5, 5] := 0.00000;
    mat_D[6, 1] := 0.00250;
    mat_D[6, 2] := 0.00280;
    mat_D[6, 3] := 0.00085;
    mat_D[6, 4] := 0.00000;
    mat_D[6, 5] := 0.00000;
    
    (* Observer Innovation Gain Matrix L (6x6) *)
    mat_L[1, 1] := 0.34500;
    mat_L[1, 2] := 0.00850;
    mat_L[1, 3] := 0.00000;
    mat_L[1, 4] := 0.00000;
    mat_L[1, 5] := 0.00120;
    mat_L[1, 6] := 0.00450;
    mat_L[2, 1] := 0.00780;
    mat_L[2, 2] := 0.35200;
    mat_L[2, 3] := 0.00000;
    mat_L[2, 4] := 0.00000;
    mat_L[2, 5] := 0.00150;
    mat_L[2, 6] := 0.00520;
    mat_L[3, 1] := 0.00000;
    mat_L[3, 2] := 0.00000;
    mat_L[3, 3] := 0.42500;
    mat_L[3, 4] := 0.00580;
    mat_L[3, 5] := 0.00000;
    mat_L[3, 6] := 0.00000;
    mat_L[4, 1] := 0.00000;
    mat_L[4, 2] := 0.00000;
    mat_L[4, 3] := 0.00350;
    mat_L[4, 4] := 0.46800;
    mat_L[4, 5] := 0.00000;
    mat_L[4, 6] := -0.01500;
    mat_L[5, 1] := 0.00180;
    mat_L[5, 2] := 0.00220;
    mat_L[5, 3] := 0.00000;
    mat_L[5, 4] := 0.00000;
    mat_L[5, 5] := 0.38500;
    mat_L[5, 6] := 0.00250;
    mat_L[6, 1] := 0.01450;
    mat_L[6, 2] := 0.01580;
    mat_L[6, 3] := 0.00000;
    mat_L[6, 4] := 0.01850;
    mat_L[6, 5] := 0.00420;
    mat_L[6, 6] := 0.41500;
    
    (* Quadratic Cost Matrix Penalties *)
    vec_Q_diag[1] := 25.0;     (* x1: Gantry X Position Tracking Error Penalty *)
    vec_Q_diag[2] := 25.0;     (* x2: Gantry Y Position Tracking Error Penalty *)
    vec_Q_diag[3] := 18.0;     (* x3: Rotary Nozzle Vacuum Suction Pressure Penalty *)
    vec_Q_diag[4] := 180.0;    (* x4: Placement Touchdown Force Penalty (Die Crack Hazard: F <= 2.5 N) *)
    vec_Q_diag[5] := 35.0;     (* x5: Component Placement Angular Theta Offset Penalty *)
    vec_Q_diag[6] := 12.0;     (* x6: Machine Frame Structural Vibration RMS Acceleration Penalty *)
    
    vec_P_diag[1] := 55.0;     (* Terminal State Penalty x1 *)
    vec_P_diag[2] := 55.0;     (* Terminal State Penalty x2 *)
    vec_P_diag[3] := 32.0;     (* Terminal State Penalty x3 *)
    vec_P_diag[4] := 350.0;    (* Terminal State Penalty x4 (Soft Landing Die Preservation) *)
    vec_P_diag[5] := 75.0;     (* Terminal State Penalty x5 *)
    vec_P_diag[6] := 24.0;     (* Terminal State Penalty x6 *)
    
    vec_R_diag[1] := 1.15;     (* u1: Linear Motor X-Axis PWM Current Effort Penalty *)
    vec_R_diag[2] := 1.15;     (* u2: Linear Motor Y-Axis PWM Current Effort Penalty *)
    vec_R_diag[3] := 3.20;     (* u3: Voice Coil Z Touchdown Force Actuator Penalty *)
    vec_R_diag[4] := 0.65;     (* u4: Vacuum Venturi Solenoid Penalty *)
    vec_R_diag[5] := 0.85;     (* u5: Positive Pressure Blow-off Solenoid Penalty *)
    
    vec_S_diag[1] := 2.65;     (* u1: Slew Rate Damping Penalty *)
    vec_S_diag[2] := 2.65;     (* u2: Slew Rate Damping Penalty *)
    vec_S_diag[3] := 5.80;     (* u3: Slew Rate Damping Penalty (Suppresses Contact Impact Spikes) *)
    vec_S_diag[4] := 1.20;     (* u4: Slew Rate Damping Penalty *)
    vec_S_diag[5] := 1.45;     (* u5: Slew Rate Damping Penalty *)
    
    (* Actuator Box Constraints [%] *)
    vec_u_min[1] := -100.0;    vec_u_max[1] := 100.0;     (* Motor X Current Command [-100%..+100%] *)
    vec_u_min[2] := -100.0;    vec_u_max[2] := 100.0;     (* Motor Y Current Command [-100%..+100%] *)
    vec_u_min[3] := -100.0;    vec_u_max[3] := 100.0;     (* Voice Coil Z Command [-100%..+100%] *)
    vec_u_min[4] := 0.0;       vec_u_max[4] := 100.0;     (* Venturi Vacuum Valve [0%..100%] *)
    vec_u_min[5] := 0.0;       vec_u_max[5] := 100.0;     (* Blow-Off Puff Solenoid [0%..100%] *)
    
    (* Actuator Maximum Slew Limits per Ts (0.5 ms) [% / step] *)
    vec_du_slew_max[1] := 15.0;    (* Motor X Slew Limit *)
    vec_du_slew_max[2] := 15.0;    (* Motor Y Slew Limit *)
    vec_du_slew_max[3] := 18.0;    (* Voice Coil Z Slew Limit *)
    vec_du_slew_max[4] := 30.0;    (* Vacuum Solenoid Slew Limit *)
    vec_du_slew_max[5] := 60.0;    (* Fast Blow-Off Puff Slew Limit *)
    
    (* Zero Vector Initialization *)
    FOR idx_i := 1 TO 6 DO
        vec_x[idx_i] := 0.0;
        vec_x_pred[idx_i] := 0.0;
        vec_x_ref[idx_i] := 0.0;
    END_FOR;
    FOR idx_m := 1 TO 5 DO
        vec_u[idx_m] := 0.0;
        vec_u_prev[idx_m] := 0.0;
        vec_u_ref[idx_m] := 0.0;
    END_FOR;
    
    bMatricesInitialized := TRUE;
END_IF;

(* ==================================================================================================================== *)
(* PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING SUITE WITH 20 MS PERSISTENCE TIMERS                    *)
(* Independent Triplets: 1) Gantry Scale X, 2) Gantry Scale Y, 3) Vacuum, 4) Force, 5) Vibration Accelerometer        *)
(* Includes Bilinear Board Warpage Laser Triangulation Surface Interpolation                                           *)
(* ==================================================================================================================== *)
(* --- CHANNEL 1: Gantry X Linear Optical Scale Encoders (ST_SCALE_101) --- *)
rScaleX_Delta_AB := ABS(rGantryScale_X_A_um - rGantryScale_X_B_um);
rScaleX_Delta_BC := ABS(rGantryScale_X_B_um - rGantryScale_X_C_um);
rScaleX_Delta_CA := ABS(rGantryScale_X_C_um - rGantryScale_X_A_um);

IF (rScaleX_Delta_AB > rScaleX_DiscrepancyLimit_um) OR 
   (rScaleX_Delta_BC > rScaleX_DiscrepancyLimit_um) OR 
   (rScaleX_Delta_CA > rScaleX_DiscrepancyLimit_um) THEN
    rScaleX_DiscrepancyTimer_s := rScaleX_DiscrepancyTimer_s + T_SCAN_SEC;
    IF rScaleX_DiscrepancyTimer_s >= 0.020 THEN
        IF (rScaleX_Delta_AB > rScaleX_DiscrepancyLimit_um) AND (rScaleX_Delta_CA > rScaleX_DiscrepancyLimit_um) THEN
            bScaleX_ChanA_Healthy := FALSE;
        ELSIF (rScaleX_Delta_AB > rScaleX_DiscrepancyLimit_um) AND (rScaleX_Delta_BC > rScaleX_DiscrepancyLimit_um) THEN
            bScaleX_ChanB_Healthy := FALSE;
        ELSIF (rScaleX_Delta_BC > rScaleX_DiscrepancyLimit_um) AND (rScaleX_Delta_CA > rScaleX_DiscrepancyLimit_um) THEN
            bScaleX_ChanC_Healthy := FALSE;
        END_IF;
    END_IF;
ELSE
    rScaleX_DiscrepancyTimer_s := MAX(0.0, rScaleX_DiscrepancyTimer_s - (T_SCAN_SEC * 0.5));
END_IF;

(* Bumpless Voting for Gantry X Scale *)
IF bScaleX_ChanA_Healthy AND bScaleX_ChanB_Healthy AND bScaleX_ChanC_Healthy THEN
    nScaleX_VotingMode := 3;  (* 2oo3 Median Voting *)
    IF (rGantryScale_X_A_um >= rGantryScale_X_B_um AND rGantryScale_X_A_um <= rGantryScale_X_C_um) OR
       (rGantryScale_X_A_um <= rGantryScale_X_B_um AND rGantryScale_X_A_um >= rGantryScale_X_C_um) THEN
        rVotedGantryPosX_mm := rGantryScale_X_A_um * 0.001;
    ELSIF (rGantryScale_X_B_um >= rGantryScale_X_A_um AND rGantryScale_X_B_um <= rGantryScale_X_C_um) OR
          (rGantryScale_X_B_um <= rGantryScale_X_A_um AND rGantryScale_X_B_um >= rGantryScale_X_C_um) THEN
        rVotedGantryPosX_mm := rGantryScale_X_B_um * 0.001;
    ELSE
        rVotedGantryPosX_mm := rGantryScale_X_C_um * 0.001;
    END_IF;
ELSIF bScaleX_ChanA_Healthy AND bScaleX_ChanB_Healthy THEN
    nScaleX_VotingMode := 2;  (* Degraded 1oo2 Average of A and B *)
    rVotedGantryPosX_mm := (rGantryScale_X_A_um + rGantryScale_X_B_um) * 0.0005;
ELSIF bScaleX_ChanB_Healthy AND bScaleX_ChanC_Healthy THEN
    nScaleX_VotingMode := 2;  (* Degraded 1oo2 Average of B and C *)
    rVotedGantryPosX_mm := (rGantryScale_X_B_um + rGantryScale_X_C_um) * 0.0005;
ELSIF bScaleX_ChanA_Healthy AND bScaleX_ChanC_Healthy THEN
    nScaleX_VotingMode := 2;  (* Degraded 1oo2 Average of A and C *)
    rVotedGantryPosX_mm := (rGantryScale_X_A_um + rGantryScale_X_C_um) * 0.0005;
ELSIF bScaleX_ChanA_Healthy THEN
    nScaleX_VotingMode := 1;  (* Degraded Single Channel A *)
    rVotedGantryPosX_mm := rGantryScale_X_A_um * 0.001;
ELSIF bScaleX_ChanB_Healthy THEN
    nScaleX_VotingMode := 1;  (* Degraded Single Channel B *)
    rVotedGantryPosX_mm := rGantryScale_X_B_um * 0.001;
ELSIF bScaleX_ChanC_Healthy THEN
    nScaleX_VotingMode := 1;  (* Degraded Single Channel C *)
    rVotedGantryPosX_mm := rGantryScale_X_C_um * 0.001;
ELSE
    nScaleX_VotingMode := 0;  (* Total Scale X Failure - Emergency Trip *)
    bFastInterruptBrakeTrip := TRUE;
END_IF;

(* --- CHANNEL 2: Gantry Y Linear Optical Scale Encoders (ST_SCALE_201) --- *)
rScaleY_Delta_AB := ABS(rGantryScale_Y_A_um - rGantryScale_Y_B_um);
rScaleY_Delta_BC := ABS(rGantryScale_Y_B_um - rGantryScale_Y_C_um);
rScaleY_Delta_CA := ABS(rGantryScale_Y_C_um - rGantryScale_Y_A_um);

IF (rScaleY_Delta_AB > rScaleY_DiscrepancyLimit_um) OR 
   (rScaleY_Delta_BC > rScaleY_DiscrepancyLimit_um) OR 
   (rScaleY_Delta_CA > rScaleY_DiscrepancyLimit_um) THEN
    rScaleY_DiscrepancyTimer_s := rScaleY_DiscrepancyTimer_s + T_SCAN_SEC;
    IF rScaleY_DiscrepancyTimer_s >= 0.020 THEN
        IF (rScaleY_Delta_AB > rScaleY_DiscrepancyLimit_um) AND (rScaleY_Delta_CA > rScaleY_DiscrepancyLimit_um) THEN
            bScaleY_ChanA_Healthy := FALSE;
        ELSIF (rScaleY_Delta_AB > rScaleY_DiscrepancyLimit_um) AND (rScaleY_Delta_BC > rScaleY_DiscrepancyLimit_um) THEN
            bScaleY_ChanB_Healthy := FALSE;
        ELSIF (rScaleY_Delta_BC > rScaleY_DiscrepancyLimit_um) AND (rScaleY_Delta_CA > rScaleY_DiscrepancyLimit_um) THEN
            bScaleY_ChanC_Healthy := FALSE;
        END_IF;
    END_IF;
ELSE
    rScaleY_DiscrepancyTimer_s := MAX(0.0, rScaleY_DiscrepancyTimer_s - (T_SCAN_SEC * 0.5));
END_IF;

IF bScaleY_ChanA_Healthy AND bScaleY_ChanB_Healthy AND bScaleY_ChanC_Healthy THEN
    nScaleY_VotingMode := 3;
    IF (rGantryScale_Y_A_um >= rGantryScale_Y_B_um AND rGantryScale_Y_A_um <= rGantryScale_Y_C_um) OR
       (rGantryScale_Y_A_um <= rGantryScale_Y_B_um AND rGantryScale_Y_A_um >= rGantryScale_Y_C_um) THEN
        rVotedGantryPosY_mm := rGantryScale_Y_A_um * 0.001;
    ELSIF (rGantryScale_Y_B_um >= rGantryScale_Y_A_um AND rGantryScale_Y_B_um <= rGantryScale_Y_C_um) OR
          (rGantryScale_Y_B_um <= rGantryScale_Y_A_um AND rGantryScale_Y_B_um >= rGantryScale_Y_C_um) THEN
        rVotedGantryPosY_mm := rGantryScale_Y_B_um * 0.001;
    ELSE
        rVotedGantryPosY_mm := rGantryScale_Y_C_um * 0.001;
    END_IF;
ELSIF bScaleY_ChanA_Healthy AND bScaleY_ChanB_Healthy THEN
    nScaleY_VotingMode := 2;
    rVotedGantryPosY_mm := (rGantryScale_Y_A_um + rGantryScale_Y_B_um) * 0.0005;
ELSIF bScaleY_ChanB_Healthy AND bScaleY_ChanC_Healthy THEN
    nScaleY_VotingMode := 2;
    rVotedGantryPosY_mm := (rGantryScale_Y_B_um + rGantryScale_Y_C_um) * 0.0005;
ELSIF bScaleY_ChanA_Healthy AND bScaleY_ChanC_Healthy THEN
    nScaleY_VotingMode := 2;
    rVotedGantryPosY_mm := (rGantryScale_Y_A_um + rGantryScale_Y_C_um) * 0.0005;
ELSIF bScaleY_ChanA_Healthy THEN
    nScaleY_VotingMode := 1;
    rVotedGantryPosY_mm := rGantryScale_Y_A_um * 0.001;
ELSIF bScaleY_ChanB_Healthy THEN
    nScaleY_VotingMode := 1;
    rVotedGantryPosY_mm := rGantryScale_Y_B_um * 0.001;
ELSIF bScaleY_ChanC_Healthy THEN
    nScaleY_VotingMode := 1;
    rVotedGantryPosY_mm := rGantryScale_Y_C_um * 0.001;
ELSE
    nScaleY_VotingMode := 0;
    bFastInterruptBrakeTrip := TRUE;
END_IF;

(* --- CHANNEL 3: Rotary Nozzle Piezoresistive Vacuum Transducers (PT_VAC_301) --- *)
rVac_Delta_AB := ABS(rNozzleVac_Sensor_A_kPa - rNozzleVac_Sensor_B_kPa);
rVac_Delta_BC := ABS(rNozzleVac_Sensor_B_kPa - rNozzleVac_Sensor_C_kPa);
rVac_Delta_CA := ABS(rNozzleVac_Sensor_C_kPa - rNozzleVac_Sensor_A_kPa);

IF (rVac_Delta_AB > rVac_DiscrepancyLimit_kPa) OR 
   (rVac_Delta_BC > rVac_DiscrepancyLimit_kPa) OR 
   (rVac_Delta_CA > rVac_DiscrepancyLimit_kPa) THEN
    rVac_DiscrepancyTimer_s := rVac_DiscrepancyTimer_s + T_SCAN_SEC;
    IF rVac_DiscrepancyTimer_s >= 0.020 THEN
        IF (rVac_Delta_AB > rVac_DiscrepancyLimit_kPa) AND (rVac_Delta_CA > rVac_DiscrepancyLimit_kPa) THEN
            bVac_ChanA_Healthy := FALSE;
        ELSIF (rVac_Delta_AB > rVac_DiscrepancyLimit_kPa) AND (rVac_Delta_BC > rVac_DiscrepancyLimit_kPa) THEN
            bVac_ChanB_Healthy := FALSE;
        ELSIF (rVac_Delta_BC > rVac_DiscrepancyLimit_kPa) AND (rVac_Delta_CA > rVac_DiscrepancyLimit_kPa) THEN
            bVac_ChanC_Healthy := FALSE;
        END_IF;
    END_IF;
ELSE
    rVac_DiscrepancyTimer_s := MAX(0.0, rVac_DiscrepancyTimer_s - (T_SCAN_SEC * 0.5));
END_IF;

IF bVac_ChanA_Healthy AND bVac_ChanB_Healthy AND bVac_ChanC_Healthy THEN
    nVac_VotingMode := 3;
    IF (rNozzleVac_Sensor_A_kPa >= rNozzleVac_Sensor_B_kPa AND rNozzleVac_Sensor_A_kPa <= rNozzleVac_Sensor_C_kPa) OR
       (rNozzleVac_Sensor_A_kPa <= rNozzleVac_Sensor_B_kPa AND rNozzleVac_Sensor_A_kPa >= rNozzleVac_Sensor_C_kPa) THEN
        rVotedNozzleVacuum_kPa := rNozzleVac_Sensor_A_kPa;
    ELSIF (rNozzleVac_Sensor_B_kPa >= rNozzleVac_Sensor_A_kPa AND rNozzleVac_Sensor_B_kPa <= rNozzleVac_Sensor_C_kPa) OR
          (rNozzleVac_Sensor_B_kPa <= rNozzleVac_Sensor_A_kPa AND rNozzleVac_Sensor_B_kPa >= rNozzleVac_Sensor_C_kPa) THEN
        rVotedNozzleVacuum_kPa := rNozzleVac_Sensor_B_kPa;
    ELSE
        rVotedNozzleVacuum_kPa := rNozzleVac_Sensor_C_kPa;
    END_IF;
ELSIF bVac_ChanA_Healthy AND bVac_ChanB_Healthy THEN
    nVac_VotingMode := 2;
    rVotedNozzleVacuum_kPa := (rNozzleVac_Sensor_A_kPa + rNozzleVac_Sensor_B_kPa) * 0.5;
ELSIF bVac_ChanB_Healthy AND bVac_ChanC_Healthy THEN
    nVac_VotingMode := 2;
    rVotedNozzleVacuum_kPa := (rNozzleVac_Sensor_B_kPa + rNozzleVac_Sensor_C_kPa) * 0.5;
ELSIF bVac_ChanA_Healthy AND bVac_ChanC_Healthy THEN
    nVac_VotingMode := 2;
    rVotedNozzleVacuum_kPa := (rNozzleVac_Sensor_A_kPa + rNozzleVac_Sensor_C_kPa) * 0.5;
ELSIF bVac_ChanA_Healthy THEN
    nVac_VotingMode := 1;
    rVotedNozzleVacuum_kPa := rNozzleVac_Sensor_A_kPa;
ELSIF bVac_ChanB_Healthy THEN
    nVac_VotingMode := 1;
    rVotedNozzleVacuum_kPa := rNozzleVac_Sensor_B_kPa;
ELSIF bVac_ChanC_Healthy THEN
    nVac_VotingMode := 1;
    rVotedNozzleVacuum_kPa := rNozzleVac_Sensor_C_kPa;
ELSE
    nVac_VotingMode := 0;
    bFastInterruptBrakeTrip := TRUE;
END_IF;

(* --- CHANNEL 4: Touchdown Piezo Contact Force Load Cells (WT_FORCE_401) --- *)
rForce_Delta_AB := ABS(rContactForce_Sensor_A_N - rContactForce_Sensor_B_N);
rForce_Delta_BC := ABS(rContactForce_Sensor_B_N - rContactForce_Sensor_C_N);
rForce_Delta_CA := ABS(rContactForce_Sensor_C_N - rContactForce_Sensor_A_N);

IF (rForce_Delta_AB > rForce_DiscrepancyLimit_N) OR 
   (rForce_Delta_BC > rForce_DiscrepancyLimit_N) OR 
   (rForce_Delta_CA > rForce_DiscrepancyLimit_N) THEN
    rForce_DiscrepancyTimer_s := rForce_DiscrepancyTimer_s + T_SCAN_SEC;
    IF rForce_DiscrepancyTimer_s >= 0.020 THEN
        IF (rForce_Delta_AB > rForce_DiscrepancyLimit_N) AND (rForce_Delta_CA > rForce_DiscrepancyLimit_N) THEN
            bForce_ChanA_Healthy := FALSE;
        ELSIF (rForce_Delta_AB > rForce_DiscrepancyLimit_N) AND (rForce_Delta_BC > rForce_DiscrepancyLimit_N) THEN
            bForce_ChanB_Healthy := FALSE;
        ELSIF (rForce_Delta_BC > rForce_DiscrepancyLimit_N) AND (rForce_Delta_CA > rForce_DiscrepancyLimit_N) THEN
            bForce_ChanC_Healthy := FALSE;
        END_IF;
    END_IF;
ELSE
    rForce_DiscrepancyTimer_s := MAX(0.0, rForce_DiscrepancyTimer_s - (T_SCAN_SEC * 0.5));
END_IF;

IF bForce_ChanA_Healthy AND bForce_ChanB_Healthy AND bForce_ChanC_Healthy THEN
    nForce_VotingMode := 3;
    IF (rContactForce_Sensor_A_N >= rContactForce_Sensor_B_N AND rContactForce_Sensor_A_N <= rContactForce_Sensor_C_N) OR
       (rContactForce_Sensor_A_N <= rContactForce_Sensor_B_N AND rContactForce_Sensor_A_N >= rContactForce_Sensor_C_N) THEN
        rVotedContactForce_N := rContactForce_Sensor_A_N;
    ELSIF (rContactForce_Sensor_B_N >= rContactForce_Sensor_A_N AND rContactForce_Sensor_B_N <= rContactForce_Sensor_C_N) OR
          (rContactForce_Sensor_B_N <= rContactForce_Sensor_A_N AND rContactForce_Sensor_B_N >= rContactForce_Sensor_C_N) THEN
        rVotedContactForce_N := rContactForce_Sensor_B_N;
    ELSE
        rVotedContactForce_N := rContactForce_Sensor_C_N;
    END_IF;
ELSIF bForce_ChanA_Healthy AND bForce_ChanB_Healthy THEN
    nForce_VotingMode := 2;
    rVotedContactForce_N := (rContactForce_Sensor_A_N + rContactForce_Sensor_B_N) * 0.5;
ELSIF bForce_ChanB_Healthy AND bForce_ChanC_Healthy THEN
    nForce_VotingMode := 2;
    rVotedContactForce_N := (rContactForce_Sensor_B_N + rContactForce_Sensor_C_N) * 0.5;
ELSIF bForce_ChanA_Healthy AND bForce_ChanC_Healthy THEN
    nForce_VotingMode := 2;
    rVotedContactForce_N := (rContactForce_Sensor_A_N + rContactForce_Sensor_C_N) * 0.5;
ELSIF bForce_ChanA_Healthy THEN
    nForce_VotingMode := 1;
    rVotedContactForce_N := rContactForce_Sensor_A_N;
ELSIF bForce_ChanB_Healthy THEN
    nForce_VotingMode := 1;
    rVotedContactForce_N := rContactForce_Sensor_B_N;
ELSIF bForce_ChanC_Healthy THEN
    nForce_VotingMode := 1;
    rVotedContactForce_N := rContactForce_Sensor_C_N;
ELSE
    nForce_VotingMode := 0;
    bFastInterruptBrakeTrip := TRUE;
END_IF;

(* --- CHANNEL 5: Gantry Frame Triaxial Accelerometers (AT_VIB_501) --- *)
rVib_Delta_AB := ABS(rFrameAcc_Sensor_A_mps2 - rFrameAcc_Sensor_B_mps2);
rVib_Delta_BC := ABS(rFrameAcc_Sensor_B_mps2 - rFrameAcc_Sensor_C_mps2);
rVib_Delta_CA := ABS(rFrameAcc_Sensor_C_mps2 - rFrameAcc_Sensor_A_mps2);

IF (rVib_Delta_AB > rVib_DiscrepancyLimit_mps2) OR 
   (rVib_Delta_BC > rVib_DiscrepancyLimit_mps2) OR 
   (rVib_Delta_CA > rVib_DiscrepancyLimit_mps2) THEN
    rVib_DiscrepancyTimer_s := rVib_DiscrepancyTimer_s + T_SCAN_SEC;
    IF rVib_DiscrepancyTimer_s >= 0.020 THEN
        IF (rVib_Delta_AB > rVib_DiscrepancyLimit_mps2) AND (rVib_Delta_CA > rVib_DiscrepancyLimit_mps2) THEN
            bVib_ChanA_Healthy := FALSE;
        ELSIF (rVib_Delta_AB > rVib_DiscrepancyLimit_mps2) AND (rVib_Delta_BC > rVib_DiscrepancyLimit_mps2) THEN
            bVib_ChanB_Healthy := FALSE;
        ELSIF (rVib_Delta_BC > rVib_DiscrepancyLimit_mps2) AND (rVib_Delta_CA > rVib_DiscrepancyLimit_mps2) THEN
            bVib_ChanC_Healthy := FALSE;
        END_IF;
    END_IF;
ELSE
    rVib_DiscrepancyTimer_s := MAX(0.0, rVib_DiscrepancyTimer_s - (T_SCAN_SEC * 0.5));
END_IF;

IF bVib_ChanA_Healthy AND bVib_ChanB_Healthy AND bVib_ChanC_Healthy THEN
    nVib_VotingMode := 3;
    IF (rFrameAcc_Sensor_A_mps2 >= rFrameAcc_Sensor_B_mps2 AND rFrameAcc_Sensor_A_mps2 <= rFrameAcc_Sensor_C_mps2) OR
       (rFrameAcc_Sensor_A_mps2 <= rFrameAcc_Sensor_B_mps2 AND rFrameAcc_Sensor_A_mps2 >= rFrameAcc_Sensor_C_mps2) THEN
        rVotedFrameVib_mps2 := rFrameAcc_Sensor_A_mps2;
    ELSIF (rFrameAcc_Sensor_B_mps2 >= rFrameAcc_Sensor_A_mps2 AND rFrameAcc_Sensor_B_mps2 <= rFrameAcc_Sensor_C_mps2) OR
          (rFrameAcc_Sensor_B_mps2 <= rFrameAcc_Sensor_A_mps2 AND rFrameAcc_Sensor_B_mps2 >= rFrameAcc_Sensor_C_mps2) THEN
        rVotedFrameVib_mps2 := rFrameAcc_Sensor_B_mps2;
    ELSE
        rVotedFrameVib_mps2 := rFrameAcc_Sensor_C_mps2;
    END_IF;
ELSIF bVib_ChanA_Healthy AND bVib_ChanB_Healthy THEN
    nVib_VotingMode := 2;
    rVotedFrameVib_mps2 := (rFrameAcc_Sensor_A_mps2 + rFrameAcc_Sensor_B_mps2) * 0.5;
ELSIF bVib_ChanB_Healthy AND bVib_ChanC_Healthy THEN
    nVib_VotingMode := 2;
    rVotedFrameVib_mps2 := (rFrameAcc_Sensor_B_mps2 + rFrameAcc_Sensor_C_mps2) * 0.5;
ELSIF bVib_ChanA_Healthy AND bVib_ChanC_Healthy THEN
    nVib_VotingMode := 2;
    rVotedFrameVib_mps2 := (rFrameAcc_Sensor_A_mps2 + rFrameAcc_Sensor_C_mps2) * 0.5;
ELSIF bVib_ChanA_Healthy THEN
    nVib_VotingMode := 1;
    rVotedFrameVib_mps2 := rFrameAcc_Sensor_A_mps2;
ELSIF bVib_ChanB_Healthy THEN
    nVib_VotingMode := 1;
    rVotedFrameVib_mps2 := rFrameAcc_Sensor_B_mps2;
ELSIF bVib_ChanC_Healthy THEN
    nVib_VotingMode := 1;
    rVotedFrameVib_mps2 := rFrameAcc_Sensor_C_mps2;
ELSE
    nVib_VotingMode := 0;
    bFastInterruptBrakeTrip := TRUE;
END_IF;

(* --- DUAL-LANE BOARD WARPAGE BILINEAR SURFACE INTERPOLATION --- *)
(* Interpolates Z height warpage across the active PCB from 5 laser triangulation points *)
rWarpCoeff_a0 := rLaserWarpageCenter_um;
rWarpCoeff_a1 := ((rLaserWarpageCorner2_um + rLaserWarpageCorner4_um) - (rLaserWarpageCorner1_um + rLaserWarpageCorner3_um)) * 0.00167;
rWarpCoeff_a2 := ((rLaserWarpageCorner1_um + rLaserWarpageCorner2_um) - (rLaserWarpageCorner3_um + rLaserWarpageCorner4_um)) * 0.00200;
rWarpCoeff_a3 := ((rLaserWarpageCorner2_um - rLaserWarpageCorner1_um) - (rLaserWarpageCorner4_um - rLaserWarpageCorner3_um)) * 0.0000133;
bWarpageMapValid := TRUE;

(* Evaluate dynamic warpage offset at active placement target coordinate *)
rVotedPcbWarpageOffsetZ_um := rWarpCoeff_a0 + (rWarpCoeff_a1 * (rCadTargetX_mm - 150.0)) + 
                              (rWarpCoeff_a2 * (rCadTargetY_mm - 125.0)) + 
                              (rWarpCoeff_a3 * (rCadTargetX_mm - 150.0) * (rCadTargetY_mm - 125.0));

(* ==================================================================================================================== *)
(* PHASE 2: FIRST-PRINCIPLES CYBER-PHYSICAL STATE-SPACE ESTIMATION (x[k+1] = A*x[k] + B*u[k])                         *)
(* Observer Correction: x_hat = x_pred + L * (y_meas - y_est)                                                          *)
(* Calculates Gantry Tracking Errors, Vacuum Decay Rate, Contact Force & Vibration RMS Settling                       *)
(* ==================================================================================================================== *)
(* 1. Assemble process measurement vector y_meas *)
vec_y_meas[1] := (rVotedGantryPosX_mm - rCadTargetX_mm) * 1000.0; (* y1: Gantry X Position Error [um] *)
vec_y_meas[2] := (rVotedGantryPosY_mm - rCadTargetY_mm) * 1000.0; (* y2: Gantry Y Position Error [um] *)
vec_y_meas[3] := rVotedNozzleVacuum_kPa;                         (* y3: Nozzle Suction Vacuum [kPa] *)
vec_y_meas[4] := rVotedContactForce_N;                         (* y4: Placement Touchdown Force [N] *)
vec_y_meas[5] := rVisionDeltaTheta_mrad;                        (* y5: Component Rotary Theta Offset [mrad] *)
vec_y_meas[6] := rVotedFrameVib_mps2;                           (* y6: Machine Frame Structural Vibration [m/s2] *)

(* 2. Compute estimated output: y_est = C * x + D * u *)
FOR idx_i := 1 TO 6 DO
    rTempSum := 0.0;
    FOR idx_j := 1 TO 6 DO
        rTempSum := rTempSum + (mat_C[idx_i, idx_j] * vec_x[idx_j]);
    END_FOR;
    FOR idx_m := 1 TO 5 DO
        rTempSum := rTempSum + (mat_D[idx_i, idx_m] * vec_u[idx_m]);
    END_FOR;
    vec_y_est[idx_i] := rTempSum;
    vec_innov[idx_i] := vec_y_meas[idx_i] - vec_y_est[idx_i];
END_FOR;

(* 3. Apply Observer Correction: x_corrected = vec_x + L * vec_innov *)
FOR idx_i := 1 TO 6 DO
    rTempSum := 0.0;
    FOR idx_j := 1 TO 6 DO
        rTempSum := rTempSum + (mat_L[idx_i, idx_j] * vec_innov[idx_j]);
    END_FOR;
    vec_x[idx_i] := vec_x[idx_i] + rTempSum;
END_FOR;

(* 4. Non-Linear Pneumatic Vacuum Decay & Tombstone Evaluation *)
rCalculatedDecaySlope_kPas := (rVotedNozzleVacuum_kPa - rNozzleVacPrev_kPa) / T_SCAN_SEC;
rNozzleVacPrev_kPa := rVotedNozzleVacuum_kPa;

IF (nProductionState = 5) THEN
    (* If vacuum decay rate is positive (pressure rising towards atmospheric) and exceeds 1.85 kPa/ms *)
    IF (rCalculatedDecaySlope_kPas > 1850.0) AND (rVotedNozzleVacuum_kPa > -75.0) THEN
        bComponentTombstoneDetected := TRUE;
    ELSE
        bComponentTombstoneDetected := FALSE;
    END_IF;
    
    IF (rVotedNozzleVacuum_kPa <= -75.0) THEN
        bNozzleSealConforming := TRUE;
    ELSE
        bNozzleSealConforming := FALSE;
    END_IF;
ELSE
    bComponentTombstoneDetected := FALSE;
END_IF;

(* 5. Vibration RMS & Mechanical Settling Time Estimation *)
IF vec_x[6] < 3.5 THEN
    rSettlingTimerAccum_s := rSettlingTimerAccum_s + T_SCAN_SEC;
ELSE
    rSettlingTimerAccum_s := 0.0;
END_IF;
rStructuralVibrationSettlingTime_ms := rSettlingTimerAccum_s * 1000.0;

(* 6. State Propagation to Next Cycle: x_pred = A * x + B * u *)
FOR idx_i := 1 TO 6 DO
    rTempSum := 0.0;
    FOR idx_j := 1 TO 6 DO
        rTempSum := rTempSum + (mat_A[idx_i, idx_j] * vec_x[idx_j]);
    END_FOR;
    FOR idx_m := 1 TO 5 DO
        rTempSum := rTempSum + (mat_B[idx_i, idx_m] * vec_u[idx_m]);
    END_FOR;
    vec_x_pred[idx_i] := rTempSum;
END_FOR;

(* Assign Observer Derived Outputs *)
rEstTrackingErrorX_um    := vec_x[1];
rEstTrackingErrorY_um    := vec_x[2];
rEstVacuumDecayRate_kPas := rCalculatedDecaySlope_kPas;
rEstContactForce_N       := vec_x[4];
rEstThetaOffset_mrad     := vec_x[5];
rEstStructuralVibRMS_mps2:= vec_x[6];

(* ==================================================================================================================== *)
(* PHASE 3: RECEDING-HORIZON MPC OPTIMIZATION WITH 10 UNROLLED PROJECTED GRADIENT DESCENT ITERATIONS                  *)
(* Horizon N = 5, Ts = 0.5 ms, Dynamic Jerk-Limited S-Curve Tracking & Die Micro-Cracking Constraint (F <= 2.50 N)    *)
(* ==================================================================================================================== *)
(* Formulate Reference Vector vec_x_ref based on Production Phase *)
vec_x_ref[1] := 0.0; (* Tracking Error X Setpoint: EXACT ZERO [um] *)
vec_x_ref[2] := 0.0; (* Tracking Error Y Setpoint: EXACT ZERO [um] *)

IF (nProductionState >= 4) AND (nProductionState <= 9) THEN
    vec_x_ref[3] := -82.0; (* Target Suction Vacuum: -82.0 kPa (Component Retained) *)
ELSIF (nProductionState = 10) THEN
    vec_x_ref[3] := 0.0;   (* Target Vacuum: 0 kPa (Puff Release) *)
ELSE
    vec_x_ref[3] := -15.0; (* Standby Vacuum *)
END_IF;

IF (nProductionState = 9) OR (nProductionState = 10) THEN
    vec_x_ref[4] := rTargetPlacementForce_N; (* Closed-loop target placement force (Nominal 1.80 N) *)
ELSE
    vec_x_ref[4] := 0.0;                    (* Zero contact force in free flight *)
END_IF;

vec_x_ref[5] := 0.0; (* Target Theta Error: Zero [mrad] *)
vec_x_ref[6] := 0.0; (* Target Vibration RMS: Zero [m/s2] *)

(* Initialize MPC Optimization Buffers with current states and previous commands *)
FOR idx_j := 1 TO 6 DO
    arr_x_traj[0, idx_j] := vec_x[idx_j];
END_FOR;
FOR idx_k := 0 TO 4 DO
    FOR idx_m := 1 TO 5 DO
        arr_u_traj[idx_k, idx_m] := vec_u_prev[idx_m];
    END_FOR;
END_FOR;

(* Unrolled Projected Gradient Descent (PGD) — Exactly 10 Iterations *)
(* --- PGD ITERATION 01 OF 10 --- *)
(* Step 1.1: Forward State Trajectory Simulation over N = 5 Horizon *)
FOR idx_k := 0 TO 4 DO
    FOR idx_i := 1 TO 6 DO
        rTempSum := 0.0;
        FOR idx_j := 1 TO 6 DO
            rTempSum := rTempSum + (mat_A[idx_i, idx_j] * arr_x_traj[idx_k, idx_j]);
        END_FOR;
        FOR idx_m := 1 TO 5 DO
            rTempSum := rTempSum + (mat_B[idx_i, idx_m] * arr_u_traj[idx_k, idx_m]);
        END_FOR;
        arr_x_traj[idx_k + 1, idx_i] := rTempSum;
    END_FOR;
END_FOR;

(* Step 2.1: Compute Terminal Adjoint Costates at k = 5 *)
FOR idx_i := 1 TO 6 DO
    arr_cost_state[5, idx_i] := vec_P_diag[idx_i] * (arr_x_traj[5, idx_i] - vec_x_ref[idx_i]);
END_FOR;

(* Step 3.1: Backwards Adjoint Recursion for k = 4 down to 1 *)
FOR idx_k := 4 TO 1 BY -1 DO
    FOR idx_i := 1 TO 6 DO
        rTempSum := vec_Q_diag[idx_i] * (arr_x_traj[idx_k, idx_i] - vec_x_ref[idx_i]);
        FOR idx_j := 1 TO 6 DO
            rTempSum := rTempSum + (mat_A[idx_j, idx_i] * arr_cost_state[idx_k + 1, idx_j]);
        END_FOR;
        arr_cost_state[idx_k, idx_i] := rTempSum;
    END_FOR;
END_FOR;

(* Step 4.1: Gradient Evaluation, Projected Gradient Descent Step & Slew/Box Clamping *)
FOR idx_k := 0 TO 4 DO
    FOR idx_m := 1 TO 5 DO
        IF idx_k = 0 THEN
            rTempGrad := (vec_R_diag[idx_m] * (arr_u_traj[idx_k, idx_m] - vec_u_ref[idx_m])) +
                         (vec_S_diag[idx_m] * (arr_u_traj[idx_k, idx_m] - vec_u_prev[idx_m]));
        ELSE
            rTempGrad := (vec_R_diag[idx_m] * (arr_u_traj[idx_k, idx_m] - vec_u_ref[idx_m])) +
                         (vec_S_diag[idx_m] * (arr_u_traj[idx_k, idx_m] - arr_u_traj[idx_k - 1, idx_m]));
        END_IF;
        FOR idx_j := 1 TO 6 DO
            rTempGrad := rTempGrad + (mat_B[idx_j, idx_m] * arr_cost_state[idx_k + 1, idx_j]);
        END_FOR;
        arr_grad_u[idx_k, idx_m] := rTempGrad;
        
        (* Projected Gradient Step *)
        rTempCand := arr_u_traj[idx_k, idx_m] - (rPgdAlpha * rTempGrad);
        
        (* Actuator Slew Rate Dynamic Clamping *)
        IF idx_k = 0 THEN
            rTempCand := MAX(vec_u_prev[idx_m] - vec_du_slew_max[idx_m],
                         MIN(vec_u_prev[idx_m] + vec_du_slew_max[idx_m], rTempCand));
        ELSE
            rTempCand := MAX(arr_u_traj[idx_k - 1, idx_m] - vec_du_slew_max[idx_m],
                         MIN(arr_u_traj[idx_k - 1, idx_m] + vec_du_slew_max[idx_m], rTempCand));
        END_IF;
        
        (* Box Constraint Clamping *)
        rTempCand := MAX(vec_u_min[idx_m], MIN(vec_u_max[idx_m], rTempCand));
        
        (* Automotive Die Micro-Crack Protection: Enforce Voice Coil Z Force Bound *)
        IF (idx_m = 3) AND (arr_x_traj[idx_k, 4] >= 2.30) THEN
            rTempCand := MIN(rTempCand, 12.0); (* Cap voice coil force to prevent F > 2.50 N *)
        END_IF;
        
        arr_u_traj[idx_k, idx_m] := rTempCand;
    END_FOR;
END_FOR;

(* --- PGD ITERATION 02 OF 10 --- *)
(* Step 1.2: Forward State Trajectory Simulation over N = 5 Horizon *)
FOR idx_k := 0 TO 4 DO
    FOR idx_i := 1 TO 6 DO
        rTempSum := 0.0;
        FOR idx_j := 1 TO 6 DO
            rTempSum := rTempSum + (mat_A[idx_i, idx_j] * arr_x_traj[idx_k, idx_j]);
        END_FOR;
        FOR idx_m := 1 TO 5 DO
            rTempSum := rTempSum + (mat_B[idx_i, idx_m] * arr_u_traj[idx_k, idx_m]);
        END_FOR;
        arr_x_traj[idx_k + 1, idx_i] := rTempSum;
    END_FOR;
END_FOR;

(* Step 2.2: Compute Terminal Adjoint Costates at k = 5 *)
FOR idx_i := 1 TO 6 DO
    arr_cost_state[5, idx_i] := vec_P_diag[idx_i] * (arr_x_traj[5, idx_i] - vec_x_ref[idx_i]);
END_FOR;

(* Step 3.2: Backwards Adjoint Recursion for k = 4 down to 1 *)
FOR idx_k := 4 TO 1 BY -1 DO
    FOR idx_i := 1 TO 6 DO
        rTempSum := vec_Q_diag[idx_i] * (arr_x_traj[idx_k, idx_i] - vec_x_ref[idx_i]);
        FOR idx_j := 1 TO 6 DO
            rTempSum := rTempSum + (mat_A[idx_j, idx_i] * arr_cost_state[idx_k + 1, idx_j]);
        END_FOR;
        arr_cost_state[idx_k, idx_i] := rTempSum;
    END_FOR;
END_FOR;

(* Step 4.2: Gradient Evaluation, Projected Gradient Descent Step & Slew/Box Clamping *)
FOR idx_k := 0 TO 4 DO
    FOR idx_m := 1 TO 5 DO
        IF idx_k = 0 THEN
            rTempGrad := (vec_R_diag[idx_m] * (arr_u_traj[idx_k, idx_m] - vec_u_ref[idx_m])) +
                         (vec_S_diag[idx_m] * (arr_u_traj[idx_k, idx_m] - vec_u_prev[idx_m]));
        ELSE
            rTempGrad := (vec_R_diag[idx_m] * (arr_u_traj[idx_k, idx_m] - vec_u_ref[idx_m])) +
                         (vec_S_diag[idx_m] * (arr_u_traj[idx_k, idx_m] - arr_u_traj[idx_k - 1, idx_m]));
        END_IF;
        FOR idx_j := 1 TO 6 DO
            rTempGrad := rTempGrad + (mat_B[idx_j, idx_m] * arr_cost_state[idx_k + 1, idx_j]);
        END_FOR;
        arr_grad_u[idx_k, idx_m] := rTempGrad;
        
        (* Projected Gradient Step *)
        rTempCand := arr_u_traj[idx_k, idx_m] - (rPgdAlpha * rTempGrad);
        
        (* Actuator Slew Rate Dynamic Clamping *)
        IF idx_k = 0 THEN
            rTempCand := MAX(vec_u_prev[idx_m] - vec_du_slew_max[idx_m],
                         MIN(vec_u_prev[idx_m] + vec_du_slew_max[idx_m], rTempCand));
        ELSE
            rTempCand := MAX(arr_u_traj[idx_k - 1, idx_m] - vec_du_slew_max[idx_m],
                         MIN(arr_u_traj[idx_k - 1, idx_m] + vec_du_slew_max[idx_m], rTempCand));
        END_IF;
        
        (* Box Constraint Clamping *)
        rTempCand := MAX(vec_u_min[idx_m], MIN(vec_u_max[idx_m], rTempCand));
        
        (* Automotive Die Micro-Crack Protection: Enforce Voice Coil Z Force Bound *)
        IF (idx_m = 3) AND (arr_x_traj[idx_k, 4] >= 2.30) THEN
            rTempCand := MIN(rTempCand, 12.0); (* Cap voice coil force to prevent F > 2.50 N *)
        END_IF;
        
        arr_u_traj[idx_k, idx_m] := rTempCand;
    END_FOR;
END_FOR;

(* --- PGD ITERATION 03 OF 10 --- *)
(* Step 1.3: Forward State Trajectory Simulation over N = 5 Horizon *)
FOR idx_k := 0 TO 4 DO
    FOR idx_i := 1 TO 6 DO
        rTempSum := 0.0;
        FOR idx_j := 1 TO 6 DO
            rTempSum := rTempSum + (mat_A[idx_i, idx_j] * arr_x_traj[idx_k, idx_j]);
        END_FOR;
        FOR idx_m := 1 TO 5 DO
            rTempSum := rTempSum + (mat_B[idx_i, idx_m] * arr_u_traj[idx_k, idx_m]);
        END_FOR;
        arr_x_traj[idx_k + 1, idx_i] := rTempSum;
    END_FOR;
END_FOR;

(* Step 2.3: Compute Terminal Adjoint Costates at k = 5 *)
FOR idx_i := 1 TO 6 DO
    arr_cost_state[5, idx_i] := vec_P_diag[idx_i] * (arr_x_traj[5, idx_i] - vec_x_ref[idx_i]);
END_FOR;

(* Step 3.3: Backwards Adjoint Recursion for k = 4 down to 1 *)
FOR idx_k := 4 TO 1 BY -1 DO
    FOR idx_i := 1 TO 6 DO
        rTempSum := vec_Q_diag[idx_i] * (arr_x_traj[idx_k, idx_i] - vec_x_ref[idx_i]);
        FOR idx_j := 1 TO 6 DO
            rTempSum := rTempSum + (mat_A[idx_j, idx_i] * arr_cost_state[idx_k + 1, idx_j]);
        END_FOR;
        arr_cost_state[idx_k, idx_i] := rTempSum;
    END_FOR;
END_FOR;

(* Step 4.3: Gradient Evaluation, Projected Gradient Descent Step & Slew/Box Clamping *)
FOR idx_k := 0 TO 4 DO
    FOR idx_m := 1 TO 5 DO
        IF idx_k = 0 THEN
            rTempGrad := (vec_R_diag[idx_m] * (arr_u_traj[idx_k, idx_m] - vec_u_ref[idx_m])) +
                         (vec_S_diag[idx_m] * (arr_u_traj[idx_k, idx_m] - vec_u_prev[idx_m]));
        ELSE
            rTempGrad := (vec_R_diag[idx_m] * (arr_u_traj[idx_k, idx_m] - vec_u_ref[idx_m])) +
                         (vec_S_diag[idx_m] * (arr_u_traj[idx_k, idx_m] - arr_u_traj[idx_k - 1, idx_m]));
        END_IF;
        FOR idx_j := 1 TO 6 DO
            rTempGrad := rTempGrad + (mat_B[idx_j, idx_m] * arr_cost_state[idx_k + 1, idx_j]);
        END_FOR;
        arr_grad_u[idx_k, idx_m] := rTempGrad;
        
        (* Projected Gradient Step *)
        rTempCand := arr_u_traj[idx_k, idx_m] - (rPgdAlpha * rTempGrad);
        
        (* Actuator Slew Rate Dynamic Clamping *)
        IF idx_k = 0 THEN
            rTempCand := MAX(vec_u_prev[idx_m] - vec_du_slew_max[idx_m],
                         MIN(vec_u_prev[idx_m] + vec_du_slew_max[idx_m], rTempCand));
        ELSE
            rTempCand := MAX(arr_u_traj[idx_k - 1, idx_m] - vec_du_slew_max[idx_m],
                         MIN(arr_u_traj[idx_k - 1, idx_m] + vec_du_slew_max[idx_m], rTempCand));
        END_IF;
        
        (* Box Constraint Clamping *)
        rTempCand := MAX(vec_u_min[idx_m], MIN(vec_u_max[idx_m], rTempCand));
        
        (* Automotive Die Micro-Crack Protection: Enforce Voice Coil Z Force Bound *)
        IF (idx_m = 3) AND (arr_x_traj[idx_k, 4] >= 2.30) THEN
            rTempCand := MIN(rTempCand, 12.0); (* Cap voice coil force to prevent F > 2.50 N *)
        END_IF;
        
        arr_u_traj[idx_k, idx_m] := rTempCand;
    END_FOR;
END_FOR;

(* --- PGD ITERATION 04 OF 10 --- *)
(* Step 1.4: Forward State Trajectory Simulation over N = 5 Horizon *)
FOR idx_k := 0 TO 4 DO
    FOR idx_i := 1 TO 6 DO
        rTempSum := 0.0;
        FOR idx_j := 1 TO 6 DO
            rTempSum := rTempSum + (mat_A[idx_i, idx_j] * arr_x_traj[idx_k, idx_j]);
        END_FOR;
        FOR idx_m := 1 TO 5 DO
            rTempSum := rTempSum + (mat_B[idx_i, idx_m] * arr_u_traj[idx_k, idx_m]);
        END_FOR;
        arr_x_traj[idx_k + 1, idx_i] := rTempSum;
    END_FOR;
END_FOR;

(* Step 2.4: Compute Terminal Adjoint Costates at k = 5 *)
FOR idx_i := 1 TO 6 DO
    arr_cost_state[5, idx_i] := vec_P_diag[idx_i] * (arr_x_traj[5, idx_i] - vec_x_ref[idx_i]);
END_FOR;

(* Step 3.4: Backwards Adjoint Recursion for k = 4 down to 1 *)
FOR idx_k := 4 TO 1 BY -1 DO
    FOR idx_i := 1 TO 6 DO
        rTempSum := vec_Q_diag[idx_i] * (arr_x_traj[idx_k, idx_i] - vec_x_ref[idx_i]);
        FOR idx_j := 1 TO 6 DO
            rTempSum := rTempSum + (mat_A[idx_j, idx_i] * arr_cost_state[idx_k + 1, idx_j]);
        END_FOR;
        arr_cost_state[idx_k, idx_i] := rTempSum;
    END_FOR;
END_FOR;

(* Step 4.4: Gradient Evaluation, Projected Gradient Descent Step & Slew/Box Clamping *)
FOR idx_k := 0 TO 4 DO
    FOR idx_m := 1 TO 5 DO
        IF idx_k = 0 THEN
            rTempGrad := (vec_R_diag[idx_m] * (arr_u_traj[idx_k, idx_m] - vec_u_ref[idx_m])) +
                         (vec_S_diag[idx_m] * (arr_u_traj[idx_k, idx_m] - vec_u_prev[idx_m]));
        ELSE
            rTempGrad := (vec_R_diag[idx_m] * (arr_u_traj[idx_k, idx_m] - vec_u_ref[idx_m])) +
                         (vec_S_diag[idx_m] * (arr_u_traj[idx_k, idx_m] - arr_u_traj[idx_k - 1, idx_m]));
        END_IF;
        FOR idx_j := 1 TO 6 DO
            rTempGrad := rTempGrad + (mat_B[idx_j, idx_m] * arr_cost_state[idx_k + 1, idx_j]);
        END_FOR;
        arr_grad_u[idx_k, idx_m] := rTempGrad;
        
        (* Projected Gradient Step *)
        rTempCand := arr_u_traj[idx_k, idx_m] - (rPgdAlpha * rTempGrad);
        
        (* Actuator Slew Rate Dynamic Clamping *)
        IF idx_k = 0 THEN
            rTempCand := MAX(vec_u_prev[idx_m] - vec_du_slew_max[idx_m],
                         MIN(vec_u_prev[idx_m] + vec_du_slew_max[idx_m], rTempCand));
        ELSE
            rTempCand := MAX(arr_u_traj[idx_k - 1, idx_m] - vec_du_slew_max[idx_m],
                         MIN(arr_u_traj[idx_k - 1, idx_m] + vec_du_slew_max[idx_m], rTempCand));
        END_IF;
        
        (* Box Constraint Clamping *)
        rTempCand := MAX(vec_u_min[idx_m], MIN(vec_u_max[idx_m], rTempCand));
        
        (* Automotive Die Micro-Crack Protection: Enforce Voice Coil Z Force Bound *)
        IF (idx_m = 3) AND (arr_x_traj[idx_k, 4] >= 2.30) THEN
            rTempCand := MIN(rTempCand, 12.0); (* Cap voice coil force to prevent F > 2.50 N *)
        END_IF;
        
        arr_u_traj[idx_k, idx_m] := rTempCand;
    END_FOR;
END_FOR;

(* --- PGD ITERATION 05 OF 10 --- *)
(* Step 1.5: Forward State Trajectory Simulation over N = 5 Horizon *)
FOR idx_k := 0 TO 4 DO
    FOR idx_i := 1 TO 6 DO
        rTempSum := 0.0;
        FOR idx_j := 1 TO 6 DO
            rTempSum := rTempSum + (mat_A[idx_i, idx_j] * arr_x_traj[idx_k, idx_j]);
        END_FOR;
        FOR idx_m := 1 TO 5 DO
            rTempSum := rTempSum + (mat_B[idx_i, idx_m] * arr_u_traj[idx_k, idx_m]);
        END_FOR;
        arr_x_traj[idx_k + 1, idx_i] := rTempSum;
    END_FOR;
END_FOR;

(* Step 2.5: Compute Terminal Adjoint Costates at k = 5 *)
FOR idx_i := 1 TO 6 DO
    arr_cost_state[5, idx_i] := vec_P_diag[idx_i] * (arr_x_traj[5, idx_i] - vec_x_ref[idx_i]);
END_FOR;

(* Step 3.5: Backwards Adjoint Recursion for k = 4 down to 1 *)
FOR idx_k := 4 TO 1 BY -1 DO
    FOR idx_i := 1 TO 6 DO
        rTempSum := vec_Q_diag[idx_i] * (arr_x_traj[idx_k, idx_i] - vec_x_ref[idx_i]);
        FOR idx_j := 1 TO 6 DO
            rTempSum := rTempSum + (mat_A[idx_j, idx_i] * arr_cost_state[idx_k + 1, idx_j]);
        END_FOR;
        arr_cost_state[idx_k, idx_i] := rTempSum;
    END_FOR;
END_FOR;

(* Step 4.5: Gradient Evaluation, Projected Gradient Descent Step & Slew/Box Clamping *)
FOR idx_k := 0 TO 4 DO
    FOR idx_m := 1 TO 5 DO
        IF idx_k = 0 THEN
            rTempGrad := (vec_R_diag[idx_m] * (arr_u_traj[idx_k, idx_m] - vec_u_ref[idx_m])) +
                         (vec_S_diag[idx_m] * (arr_u_traj[idx_k, idx_m] - vec_u_prev[idx_m]));
        ELSE
            rTempGrad := (vec_R_diag[idx_m] * (arr_u_traj[idx_k, idx_m] - vec_u_ref[idx_m])) +
                         (vec_S_diag[idx_m] * (arr_u_traj[idx_k, idx_m] - arr_u_traj[idx_k - 1, idx_m]));
        END_IF;
        FOR idx_j := 1 TO 6 DO
            rTempGrad := rTempGrad + (mat_B[idx_j, idx_m] * arr_cost_state[idx_k + 1, idx_j]);
        END_FOR;
        arr_grad_u[idx_k, idx_m] := rTempGrad;
        
        (* Projected Gradient Step *)
        rTempCand := arr_u_traj[idx_k, idx_m] - (rPgdAlpha * rTempGrad);
        
        (* Actuator Slew Rate Dynamic Clamping *)
        IF idx_k = 0 THEN
            rTempCand := MAX(vec_u_prev[idx_m] - vec_du_slew_max[idx_m],
                         MIN(vec_u_prev[idx_m] + vec_du_slew_max[idx_m], rTempCand));
        ELSE
            rTempCand := MAX(arr_u_traj[idx_k - 1, idx_m] - vec_du_slew_max[idx_m],
                         MIN(arr_u_traj[idx_k - 1, idx_m] + vec_du_slew_max[idx_m], rTempCand));
        END_IF;
        
        (* Box Constraint Clamping *)
        rTempCand := MAX(vec_u_min[idx_m], MIN(vec_u_max[idx_m], rTempCand));
        
        (* Automotive Die Micro-Crack Protection: Enforce Voice Coil Z Force Bound *)
        IF (idx_m = 3) AND (arr_x_traj[idx_k, 4] >= 2.30) THEN
            rTempCand := MIN(rTempCand, 12.0); (* Cap voice coil force to prevent F > 2.50 N *)
        END_IF;
        
        arr_u_traj[idx_k, idx_m] := rTempCand;
    END_FOR;
END_FOR;

(* --- PGD ITERATION 06 OF 10 --- *)
(* Step 1.6: Forward State Trajectory Simulation over N = 5 Horizon *)
FOR idx_k := 0 TO 4 DO
    FOR idx_i := 1 TO 6 DO
        rTempSum := 0.0;
        FOR idx_j := 1 TO 6 DO
            rTempSum := rTempSum + (mat_A[idx_i, idx_j] * arr_x_traj[idx_k, idx_j]);
        END_FOR;
        FOR idx_m := 1 TO 5 DO
            rTempSum := rTempSum + (mat_B[idx_i, idx_m] * arr_u_traj[idx_k, idx_m]);
        END_FOR;
        arr_x_traj[idx_k + 1, idx_i] := rTempSum;
    END_FOR;
END_FOR;

(* Step 2.6: Compute Terminal Adjoint Costates at k = 5 *)
FOR idx_i := 1 TO 6 DO
    arr_cost_state[5, idx_i] := vec_P_diag[idx_i] * (arr_x_traj[5, idx_i] - vec_x_ref[idx_i]);
END_FOR;

(* Step 3.6: Backwards Adjoint Recursion for k = 4 down to 1 *)
FOR idx_k := 4 TO 1 BY -1 DO
    FOR idx_i := 1 TO 6 DO
        rTempSum := vec_Q_diag[idx_i] * (arr_x_traj[idx_k, idx_i] - vec_x_ref[idx_i]);
        FOR idx_j := 1 TO 6 DO
            rTempSum := rTempSum + (mat_A[idx_j, idx_i] * arr_cost_state[idx_k + 1, idx_j]);
        END_FOR;
        arr_cost_state[idx_k, idx_i] := rTempSum;
    END_FOR;
END_FOR;

(* Step 4.6: Gradient Evaluation, Projected Gradient Descent Step & Slew/Box Clamping *)
FOR idx_k := 0 TO 4 DO
    FOR idx_m := 1 TO 5 DO
        IF idx_k = 0 THEN
            rTempGrad := (vec_R_diag[idx_m] * (arr_u_traj[idx_k, idx_m] - vec_u_ref[idx_m])) +
                         (vec_S_diag[idx_m] * (arr_u_traj[idx_k, idx_m] - vec_u_prev[idx_m]));
        ELSE
            rTempGrad := (vec_R_diag[idx_m] * (arr_u_traj[idx_k, idx_m] - vec_u_ref[idx_m])) +
                         (vec_S_diag[idx_m] * (arr_u_traj[idx_k, idx_m] - arr_u_traj[idx_k - 1, idx_m]));
        END_IF;
        FOR idx_j := 1 TO 6 DO
            rTempGrad := rTempGrad + (mat_B[idx_j, idx_m] * arr_cost_state[idx_k + 1, idx_j]);
        END_FOR;
        arr_grad_u[idx_k, idx_m] := rTempGrad;
        
        (* Projected Gradient Step *)
        rTempCand := arr_u_traj[idx_k, idx_m] - (rPgdAlpha * rTempGrad);
        
        (* Actuator Slew Rate Dynamic Clamping *)
        IF idx_k = 0 THEN
            rTempCand := MAX(vec_u_prev[idx_m] - vec_du_slew_max[idx_m],
                         MIN(vec_u_prev[idx_m] + vec_du_slew_max[idx_m], rTempCand));
        ELSE
            rTempCand := MAX(arr_u_traj[idx_k - 1, idx_m] - vec_du_slew_max[idx_m],
                         MIN(arr_u_traj[idx_k - 1, idx_m] + vec_du_slew_max[idx_m], rTempCand));
        END_IF;
        
        (* Box Constraint Clamping *)
        rTempCand := MAX(vec_u_min[idx_m], MIN(vec_u_max[idx_m], rTempCand));
        
        (* Automotive Die Micro-Crack Protection: Enforce Voice Coil Z Force Bound *)
        IF (idx_m = 3) AND (arr_x_traj[idx_k, 4] >= 2.30) THEN
            rTempCand := MIN(rTempCand, 12.0); (* Cap voice coil force to prevent F > 2.50 N *)
        END_IF;
        
        arr_u_traj[idx_k, idx_m] := rTempCand;
    END_FOR;
END_FOR;

(* --- PGD ITERATION 07 OF 10 --- *)
(* Step 1.7: Forward State Trajectory Simulation over N = 5 Horizon *)
FOR idx_k := 0 TO 4 DO
    FOR idx_i := 1 TO 6 DO
        rTempSum := 0.0;
        FOR idx_j := 1 TO 6 DO
            rTempSum := rTempSum + (mat_A[idx_i, idx_j] * arr_x_traj[idx_k, idx_j]);
        END_FOR;
        FOR idx_m := 1 TO 5 DO
            rTempSum := rTempSum + (mat_B[idx_i, idx_m] * arr_u_traj[idx_k, idx_m]);
        END_FOR;
        arr_x_traj[idx_k + 1, idx_i] := rTempSum;
    END_FOR;
END_FOR;

(* Step 2.7: Compute Terminal Adjoint Costates at k = 5 *)
FOR idx_i := 1 TO 6 DO
    arr_cost_state[5, idx_i] := vec_P_diag[idx_i] * (arr_x_traj[5, idx_i] - vec_x_ref[idx_i]);
END_FOR;

(* Step 3.7: Backwards Adjoint Recursion for k = 4 down to 1 *)
FOR idx_k := 4 TO 1 BY -1 DO
    FOR idx_i := 1 TO 6 DO
        rTempSum := vec_Q_diag[idx_i] * (arr_x_traj[idx_k, idx_i] - vec_x_ref[idx_i]);
        FOR idx_j := 1 TO 6 DO
            rTempSum := rTempSum + (mat_A[idx_j, idx_i] * arr_cost_state[idx_k + 1, idx_j]);
        END_FOR;
        arr_cost_state[idx_k, idx_i] := rTempSum;
    END_FOR;
END_FOR;

(* Step 4.7: Gradient Evaluation, Projected Gradient Descent Step & Slew/Box Clamping *)
FOR idx_k := 0 TO 4 DO
    FOR idx_m := 1 TO 5 DO
        IF idx_k = 0 THEN
            rTempGrad := (vec_R_diag[idx_m] * (arr_u_traj[idx_k, idx_m] - vec_u_ref[idx_m])) +
                         (vec_S_diag[idx_m] * (arr_u_traj[idx_k, idx_m] - vec_u_prev[idx_m]));
        ELSE
            rTempGrad := (vec_R_diag[idx_m] * (arr_u_traj[idx_k, idx_m] - vec_u_ref[idx_m])) +
                         (vec_S_diag[idx_m] * (arr_u_traj[idx_k, idx_m] - arr_u_traj[idx_k - 1, idx_m]));
        END_IF;
        FOR idx_j := 1 TO 6 DO
            rTempGrad := rTempGrad + (mat_B[idx_j, idx_m] * arr_cost_state[idx_k + 1, idx_j]);
        END_FOR;
        arr_grad_u[idx_k, idx_m] := rTempGrad;
        
        (* Projected Gradient Step *)
        rTempCand := arr_u_traj[idx_k, idx_m] - (rPgdAlpha * rTempGrad);
        
        (* Actuator Slew Rate Dynamic Clamping *)
        IF idx_k = 0 THEN
            rTempCand := MAX(vec_u_prev[idx_m] - vec_du_slew_max[idx_m],
                         MIN(vec_u_prev[idx_m] + vec_du_slew_max[idx_m], rTempCand));
        ELSE
            rTempCand := MAX(arr_u_traj[idx_k - 1, idx_m] - vec_du_slew_max[idx_m],
                         MIN(arr_u_traj[idx_k - 1, idx_m] + vec_du_slew_max[idx_m], rTempCand));
        END_IF;
        
        (* Box Constraint Clamping *)
        rTempCand := MAX(vec_u_min[idx_m], MIN(vec_u_max[idx_m], rTempCand));
        
        (* Automotive Die Micro-Crack Protection: Enforce Voice Coil Z Force Bound *)
        IF (idx_m = 3) AND (arr_x_traj[idx_k, 4] >= 2.30) THEN
            rTempCand := MIN(rTempCand, 12.0); (* Cap voice coil force to prevent F > 2.50 N *)
        END_IF;
        
        arr_u_traj[idx_k, idx_m] := rTempCand;
    END_FOR;
END_FOR;

(* --- PGD ITERATION 08 OF 10 --- *)
(* Step 1.8: Forward State Trajectory Simulation over N = 5 Horizon *)
FOR idx_k := 0 TO 4 DO
    FOR idx_i := 1 TO 6 DO
        rTempSum := 0.0;
        FOR idx_j := 1 TO 6 DO
            rTempSum := rTempSum + (mat_A[idx_i, idx_j] * arr_x_traj[idx_k, idx_j]);
        END_FOR;
        FOR idx_m := 1 TO 5 DO
            rTempSum := rTempSum + (mat_B[idx_i, idx_m] * arr_u_traj[idx_k, idx_m]);
        END_FOR;
        arr_x_traj[idx_k + 1, idx_i] := rTempSum;
    END_FOR;
END_FOR;

(* Step 2.8: Compute Terminal Adjoint Costates at k = 5 *)
FOR idx_i := 1 TO 6 DO
    arr_cost_state[5, idx_i] := vec_P_diag[idx_i] * (arr_x_traj[5, idx_i] - vec_x_ref[idx_i]);
END_FOR;

(* Step 3.8: Backwards Adjoint Recursion for k = 4 down to 1 *)
FOR idx_k := 4 TO 1 BY -1 DO
    FOR idx_i := 1 TO 6 DO
        rTempSum := vec_Q_diag[idx_i] * (arr_x_traj[idx_k, idx_i] - vec_x_ref[idx_i]);
        FOR idx_j := 1 TO 6 DO
            rTempSum := rTempSum + (mat_A[idx_j, idx_i] * arr_cost_state[idx_k + 1, idx_j]);
        END_FOR;
        arr_cost_state[idx_k, idx_i] := rTempSum;
    END_FOR;
END_FOR;

(* Step 4.8: Gradient Evaluation, Projected Gradient Descent Step & Slew/Box Clamping *)
FOR idx_k := 0 TO 4 DO
    FOR idx_m := 1 TO 5 DO
        IF idx_k = 0 THEN
            rTempGrad := (vec_R_diag[idx_m] * (arr_u_traj[idx_k, idx_m] - vec_u_ref[idx_m])) +
                         (vec_S_diag[idx_m] * (arr_u_traj[idx_k, idx_m] - vec_u_prev[idx_m]));
        ELSE
            rTempGrad := (vec_R_diag[idx_m] * (arr_u_traj[idx_k, idx_m] - vec_u_ref[idx_m])) +
                         (vec_S_diag[idx_m] * (arr_u_traj[idx_k, idx_m] - arr_u_traj[idx_k - 1, idx_m]));
        END_IF;
        FOR idx_j := 1 TO 6 DO
            rTempGrad := rTempGrad + (mat_B[idx_j, idx_m] * arr_cost_state[idx_k + 1, idx_j]);
        END_FOR;
        arr_grad_u[idx_k, idx_m] := rTempGrad;
        
        (* Projected Gradient Step *)
        rTempCand := arr_u_traj[idx_k, idx_m] - (rPgdAlpha * rTempGrad);
        
        (* Actuator Slew Rate Dynamic Clamping *)
        IF idx_k = 0 THEN
            rTempCand := MAX(vec_u_prev[idx_m] - vec_du_slew_max[idx_m],
                         MIN(vec_u_prev[idx_m] + vec_du_slew_max[idx_m], rTempCand));
        ELSE
            rTempCand := MAX(arr_u_traj[idx_k - 1, idx_m] - vec_du_slew_max[idx_m],
                         MIN(arr_u_traj[idx_k - 1, idx_m] + vec_du_slew_max[idx_m], rTempCand));
        END_IF;
        
        (* Box Constraint Clamping *)
        rTempCand := MAX(vec_u_min[idx_m], MIN(vec_u_max[idx_m], rTempCand));
        
        (* Automotive Die Micro-Crack Protection: Enforce Voice Coil Z Force Bound *)
        IF (idx_m = 3) AND (arr_x_traj[idx_k, 4] >= 2.30) THEN
            rTempCand := MIN(rTempCand, 12.0); (* Cap voice coil force to prevent F > 2.50 N *)
        END_IF;
        
        arr_u_traj[idx_k, idx_m] := rTempCand;
    END_FOR;
END_FOR;

(* --- PGD ITERATION 09 OF 10 --- *)
(* Step 1.9: Forward State Trajectory Simulation over N = 5 Horizon *)
FOR idx_k := 0 TO 4 DO
    FOR idx_i := 1 TO 6 DO
        rTempSum := 0.0;
        FOR idx_j := 1 TO 6 DO
            rTempSum := rTempSum + (mat_A[idx_i, idx_j] * arr_x_traj[idx_k, idx_j]);
        END_FOR;
        FOR idx_m := 1 TO 5 DO
            rTempSum := rTempSum + (mat_B[idx_i, idx_m] * arr_u_traj[idx_k, idx_m]);
        END_FOR;
        arr_x_traj[idx_k + 1, idx_i] := rTempSum;
    END_FOR;
END_FOR;

(* Step 2.9: Compute Terminal Adjoint Costates at k = 5 *)
FOR idx_i := 1 TO 6 DO
    arr_cost_state[5, idx_i] := vec_P_diag[idx_i] * (arr_x_traj[5, idx_i] - vec_x_ref[idx_i]);
END_FOR;

(* Step 3.9: Backwards Adjoint Recursion for k = 4 down to 1 *)
FOR idx_k := 4 TO 1 BY -1 DO
    FOR idx_i := 1 TO 6 DO
        rTempSum := vec_Q_diag[idx_i] * (arr_x_traj[idx_k, idx_i] - vec_x_ref[idx_i]);
        FOR idx_j := 1 TO 6 DO
            rTempSum := rTempSum + (mat_A[idx_j, idx_i] * arr_cost_state[idx_k + 1, idx_j]);
        END_FOR;
        arr_cost_state[idx_k, idx_i] := rTempSum;
    END_FOR;
END_FOR;

(* Step 4.9: Gradient Evaluation, Projected Gradient Descent Step & Slew/Box Clamping *)
FOR idx_k := 0 TO 4 DO
    FOR idx_m := 1 TO 5 DO
        IF idx_k = 0 THEN
            rTempGrad := (vec_R_diag[idx_m] * (arr_u_traj[idx_k, idx_m] - vec_u_ref[idx_m])) +
                         (vec_S_diag[idx_m] * (arr_u_traj[idx_k, idx_m] - vec_u_prev[idx_m]));
        ELSE
            rTempGrad := (vec_R_diag[idx_m] * (arr_u_traj[idx_k, idx_m] - vec_u_ref[idx_m])) +
                         (vec_S_diag[idx_m] * (arr_u_traj[idx_k, idx_m] - arr_u_traj[idx_k - 1, idx_m]));
        END_IF;
        FOR idx_j := 1 TO 6 DO
            rTempGrad := rTempGrad + (mat_B[idx_j, idx_m] * arr_cost_state[idx_k + 1, idx_j]);
        END_FOR;
        arr_grad_u[idx_k, idx_m] := rTempGrad;
        
        (* Projected Gradient Step *)
        rTempCand := arr_u_traj[idx_k, idx_m] - (rPgdAlpha * rTempGrad);
        
        (* Actuator Slew Rate Dynamic Clamping *)
        IF idx_k = 0 THEN
            rTempCand := MAX(vec_u_prev[idx_m] - vec_du_slew_max[idx_m],
                         MIN(vec_u_prev[idx_m] + vec_du_slew_max[idx_m], rTempCand));
        ELSE
            rTempCand := MAX(arr_u_traj[idx_k - 1, idx_m] - vec_du_slew_max[idx_m],
                         MIN(arr_u_traj[idx_k - 1, idx_m] + vec_du_slew_max[idx_m], rTempCand));
        END_IF;
        
        (* Box Constraint Clamping *)
        rTempCand := MAX(vec_u_min[idx_m], MIN(vec_u_max[idx_m], rTempCand));
        
        (* Automotive Die Micro-Crack Protection: Enforce Voice Coil Z Force Bound *)
        IF (idx_m = 3) AND (arr_x_traj[idx_k, 4] >= 2.30) THEN
            rTempCand := MIN(rTempCand, 12.0); (* Cap voice coil force to prevent F > 2.50 N *)
        END_IF;
        
        arr_u_traj[idx_k, idx_m] := rTempCand;
    END_FOR;
END_FOR;

(* --- PGD ITERATION 10 OF 10 --- *)
(* Step 1.10: Forward State Trajectory Simulation over N = 5 Horizon *)
FOR idx_k := 0 TO 4 DO
    FOR idx_i := 1 TO 6 DO
        rTempSum := 0.0;
        FOR idx_j := 1 TO 6 DO
            rTempSum := rTempSum + (mat_A[idx_i, idx_j] * arr_x_traj[idx_k, idx_j]);
        END_FOR;
        FOR idx_m := 1 TO 5 DO
            rTempSum := rTempSum + (mat_B[idx_i, idx_m] * arr_u_traj[idx_k, idx_m]);
        END_FOR;
        arr_x_traj[idx_k + 1, idx_i] := rTempSum;
    END_FOR;
END_FOR;

(* Step 2.10: Compute Terminal Adjoint Costates at k = 5 *)
FOR idx_i := 1 TO 6 DO
    arr_cost_state[5, idx_i] := vec_P_diag[idx_i] * (arr_x_traj[5, idx_i] - vec_x_ref[idx_i]);
END_FOR;

(* Step 3.10: Backwards Adjoint Recursion for k = 4 down to 1 *)
FOR idx_k := 4 TO 1 BY -1 DO
    FOR idx_i := 1 TO 6 DO
        rTempSum := vec_Q_diag[idx_i] * (arr_x_traj[idx_k, idx_i] - vec_x_ref[idx_i]);
        FOR idx_j := 1 TO 6 DO
            rTempSum := rTempSum + (mat_A[idx_j, idx_i] * arr_cost_state[idx_k + 1, idx_j]);
        END_FOR;
        arr_cost_state[idx_k, idx_i] := rTempSum;
    END_FOR;
END_FOR;

(* Step 4.10: Gradient Evaluation, Projected Gradient Descent Step & Slew/Box Clamping *)
FOR idx_k := 0 TO 4 DO
    FOR idx_m := 1 TO 5 DO
        IF idx_k = 0 THEN
            rTempGrad := (vec_R_diag[idx_m] * (arr_u_traj[idx_k, idx_m] - vec_u_ref[idx_m])) +
                         (vec_S_diag[idx_m] * (arr_u_traj[idx_k, idx_m] - vec_u_prev[idx_m]));
        ELSE
            rTempGrad := (vec_R_diag[idx_m] * (arr_u_traj[idx_k, idx_m] - vec_u_ref[idx_m])) +
                         (vec_S_diag[idx_m] * (arr_u_traj[idx_k, idx_m] - arr_u_traj[idx_k - 1, idx_m]));
        END_IF;
        FOR idx_j := 1 TO 6 DO
            rTempGrad := rTempGrad + (mat_B[idx_j, idx_m] * arr_cost_state[idx_k + 1, idx_j]);
        END_FOR;
        arr_grad_u[idx_k, idx_m] := rTempGrad;
        
        (* Projected Gradient Step *)
        rTempCand := arr_u_traj[idx_k, idx_m] - (rPgdAlpha * rTempGrad);
        
        (* Actuator Slew Rate Dynamic Clamping *)
        IF idx_k = 0 THEN
            rTempCand := MAX(vec_u_prev[idx_m] - vec_du_slew_max[idx_m],
                         MIN(vec_u_prev[idx_m] + vec_du_slew_max[idx_m], rTempCand));
        ELSE
            rTempCand := MAX(arr_u_traj[idx_k - 1, idx_m] - vec_du_slew_max[idx_m],
                         MIN(arr_u_traj[idx_k - 1, idx_m] + vec_du_slew_max[idx_m], rTempCand));
        END_IF;
        
        (* Box Constraint Clamping *)
        rTempCand := MAX(vec_u_min[idx_m], MIN(vec_u_max[idx_m], rTempCand));
        
        (* Automotive Die Micro-Crack Protection: Enforce Voice Coil Z Force Bound *)
        IF (idx_m = 3) AND (arr_x_traj[idx_k, 4] >= 2.30) THEN
            rTempCand := MIN(rTempCand, 12.0); (* Cap voice coil force to prevent F > 2.50 N *)
        END_IF;
        
        arr_u_traj[idx_k, idx_m] := rTempCand;
    END_FOR;
END_FOR;

(* Extract Receding Horizon Optimal Actuator Commands: u[k] = arr_u_traj[0] *)
FOR idx_m := 1 TO 5 DO
    vec_u[idx_m] := arr_u_traj[0, idx_m];
END_FOR;

(* Calculate Total Evaluated Quadratic Cost Functional *)
rMpcTotalCost := 0.0;
FOR idx_k := 1 TO 5 DO
    FOR idx_i := 1 TO 6 DO
        rMpcTotalCost := rMpcTotalCost + (vec_Q_diag[idx_i] * (arr_x_traj[idx_k, idx_i] - vec_x_ref[idx_i]) * (arr_x_traj[idx_k, idx_i] - vec_x_ref[idx_i]));
    END_FOR;
END_FOR;

(* ==================================================================================================================== *)
(* PHASE 4: 14-STAGE DETERMINISTIC PRODUCTION FINITE STATE MACHINE (FSM)                                               *)
(* States 0 to 13: Idle, Dual-Lane Conveyor Feed, Hydraulic Pins, Feeder Bank Slew, Vacuum Pick, Tombstone Check,     *)
(* Flying Vision, Sub-pixel Alignment, Theta Correction, Descent MPC, Soft Touchdown, AOI Inspect, Unclamp, Trip     *)
(* ==================================================================================================================== *)
IF bEmergencyStopHealthy AND bSystemEnable AND NOT bFastInterruptBrakeTrip THEN
    (* State Dwell Time Accumulation *)
    IF nFsmState = nFsmStatePrev THEN
        rFsmStateDwell_s := rFsmStateDwell_s + T_SCAN_SEC;
    ELSE
        rFsmStateDwell_s := 0.0;
        nFsmStatePrev := nFsmState;
    END_IF;
    
    CASE nFsmState OF
        0: (* STATE_IDLE *)
            bSystemReady              := FALSE;
            bPickAndPlaceActive       := FALSE;
            bConveyorRunLane1         := FALSE;
            bConveyorRunLane2         := FALSE;
            bLaneClampEngaged         := FALSE;
            bSupportPinsEngaged       := FALSE;
            bFeederAdvancePulse       := FALSE;
            bVisionStrobeTrigger      := FALSE;
            rTrajectoryTimer_s        := 0.0;
            bTrajectoryActive         := FALSE;
            rCycleTimer_s             := 0.0;
            
            (* Standby Actuator Commands *)
            vec_u[1] := 0.0; (* Motor X Current *)
            vec_u[2] := 0.0; (* Motor Y Current *)
            vec_u[3] := -25.0; (* Voice Coil Z Retracted *)
            vec_u[4] := 0.0; (* Vacuum Off *)
            vec_u[5] := 0.0; (* Blow-Off Off *)
            
            IF bSafetyDoorInterlockLocked AND bPneumaticPressureMainOK AND bMainVacuumSupplyOK THEN
                bSystemReady := TRUE;
                IF bProductionRunCmd THEN
                    IF nLaneSelectCmd = 2 THEN
                        nActiveLaneUnderPlacement := 2;
                    ELSE
                        nActiveLaneUnderPlacement := 1;
                    END_IF;
                    nFsmState := 1; (* Advance to Conveyor Feed and Warpage Scan *)
                END_IF;
            END_IF;
            
        1: (* STATE_DUAL_LANE_CONVEYOR_PCB_FEED_AND_WARPAGE_SCAN *)
            bPickAndPlaceActive := TRUE;
            IF nActiveLaneUnderPlacement = 1 THEN
                bConveyorRunLane1 := NOT bLane1PcbPresent;
                bConveyorRunLane2 := FALSE;
                IF bLane1PcbPresent THEN
                    bLaneClampEngaged := TRUE;
                END_IF;
            ELSE
                bConveyorRunLane1 := FALSE;
                bConveyorRunLane2 := NOT bLane2PcbPresent;
                IF bLane2PcbPresent THEN
                    bLaneClampEngaged := TRUE;
                END_IF;
            END_IF;
            
            vec_u[1] := 0.0;
            vec_u[2] := 0.0;
            vec_u[3] := -25.0;
            vec_u[4] := 0.0;
            vec_u[5] := 0.0;
            
            IF bWarpageMapValid AND (rFsmStateDwell_s >= 0.035) THEN
                nFsmState := 2; (* Advance to Hydraulic Bottom Support Pin Engagement *)
            END_IF;
            
        2: (* STATE_PCB_HYDRAULIC_BOTTOM_SUPPORT_PIN_ENGAGEMENT *)
            bPickAndPlaceActive := TRUE;
            bSupportPinsEngaged := TRUE; (* Elevate motorized hydraulic underside support pins *)
            vec_u[1] := 0.0;
            vec_u[2] := 0.0;
            vec_u[3] := -25.0;
            vec_u[4] := 15.0; (* Pre-charge vacuum manifold *)
            vec_u[5] := 0.0;
            
            IF bSupportPinsEngagedFeedback AND (rFsmStateDwell_s >= 0.020) THEN
                nFsmState := 3; (* Advance to Gantry High Speed Slew to Feeder Bank *)
            END_IF;
            
        3: (* STATE_GANTRY_HIGH_SPEED_SLEW_TO_FEEDER_BANK *)
            bPickAndPlaceActive := TRUE;
            bTrajectoryActive := TRUE;
            rTrajectoryTimer_s := rTrajectoryTimer_s + T_SCAN_SEC;
            rPolyTau := MIN(1.0, rTrajectoryTimer_s / rTrajectoryTotalTime_s);
            
            (* 5th-Order Polynomial S-Curve Jerk Limiting Evaluation *)
            rProfileCurrentPosX_mm := 50.0 + (350.0 * ((10.0 * rPolyTau * rPolyTau * rPolyTau) - (15.0 * rPolyTau * rPolyTau * rPolyTau * rPolyTau) + (6.0 * rPolyTau * rPolyTau * rPolyTau * rPolyTau * rPolyTau)));
            vec_u[1] := arr_u_traj[0, 1];
            vec_u[2] := arr_u_traj[0, 2];
            vec_u[3] := -25.0; (* Voice coil retracted *)
            vec_u[4] := 20.0;  (* Manifold vacuum primed *)
            vec_u[5] := 0.0;
            
            IF (rPolyTau >= 1.0) AND (rStructuralVibrationSettlingTime_ms >= 7.5) THEN
                bTrajectoryActive := FALSE;
                rTrajectoryTimer_s := 0.0;
                nFsmState := 4; (* Advance to Multi-Nozzle Simultaneous Pickup Descent *)
            END_IF;
            
        4: (* STATE_MULTI_NOZZLE_SIMULTANEOUS_PICKUP_DESCENT *)
            bPickAndPlaceActive := TRUE;
            bFeederAdvancePulse := TRUE; (* Index motorized tape feeder *)
            vec_u[1] := arr_u_traj[0, 1];
            vec_u[2] := arr_u_traj[0, 2];
            vec_u[3] := 65.0;  (* Drive voice coil down into feeder tape embossed pocket *)
            vec_u[4] := 100.0; (* Full suction vacuum 100% *)
            vec_u[5] := 0.0;
            
            rPickupDescentTimer_s := rPickupDescentTimer_s + T_SCAN_SEC;
            IF (rPickupDescentTimer_s >= 0.008) THEN
                bFeederAdvancePulse := FALSE;
                rPickupDescentTimer_s := 0.0;
                nFsmState := 5; (* Advance to Vacuum Level Verification & Tombstone Check *)
            END_IF;
            
        5: (* STATE_VACUUM_LEVEL_VERIFICATION_AND_TOMBSTONE_CHECK *)
            bPickAndPlaceActive := TRUE;
            vec_u[1] := 0.0;
            vec_u[2] := 0.0;
            vec_u[3] := 45.0;
            vec_u[4] := 100.0;
            vec_u[5] := 0.0;
            
            (* Verify vacuum draw-down <= -75.0 kPa threshold and zero tombstone leak *)
            IF bNozzleSealConforming AND NOT bComponentTombstoneDetected THEN
                vec_u[3] := -45.0; (* Fast upward voice coil retraction *)
                nFsmState := 6;    (* Advance to High Speed Traverse over Flying Vision Camera *)
            ELSIF (rFsmStateDwell_s > 0.025) THEN
                (* Missed pick or tombstoned component recovery *)
                nDefectiveRejectionsCount := nDefectiveRejectionsCount + 1;
                vec_u[3] := -45.0;
                vec_u[4] := 0.0;   (* Release suction *)
                vec_u[5] := 80.0;  (* Air puff into reject collection bin *)
                nFsmState := 4;    (* Retry next component pickup *)
            END_IF;
            
        6: (* STATE_HIGH_SPEED_TRAVERSE_OVER_FLYING_VISION_CAMERA *)
            bPickAndPlaceActive := TRUE;
            vec_u[1] := arr_u_traj[0, 1];
            vec_u[2] := arr_u_traj[0, 2];
            vec_u[3] := -25.0;
            vec_u[4] := 95.0;  (* Hold vacuum *)
            vec_u[5] := 0.0;
            
            (* Trigger camera strobe pulse when traversing optical corridor *)
            IF (rVotedGantryPosX_mm >= 180.0) AND (rVotedGantryPosX_mm <= 190.0) THEN
                bVisionStrobeTrigger := TRUE;
            ELSE
                bVisionStrobeTrigger := FALSE;
            END_IF;
            
            IF bVisionCaptureDone AND (rFsmStateDwell_s >= 0.012) THEN
                bVisionStrobeTrigger := FALSE;
                nFsmState := 7; (* Advance to On-the-Fly Optical Alignment Offset Computation *)
            END_IF;
            
        7: (* STATE_ON_THE_FLY_OPTICAL_ALIGNMENT_OFFSET_COMPUTATION *)
            bPickAndPlaceActive := TRUE;
            vec_u[1] := arr_u_traj[0, 1];
            vec_u[2] := arr_u_traj[0, 2];
            vec_u[3] := -25.0;
            vec_u[4] := 95.0;
            vec_u[5] := 0.0;
            
            IF bVisionInspectionPassed AND (rVisionCoplanarityMaxDev_um <= 28.0) THEN
                (* Inject sub-pixel optical offsets into target trajectory *)
                rCadTargetX_mm       := rCadTargetX_mm + (rVisionDeltaX_um * 0.001);
                rCadTargetY_mm       := rCadTargetY_mm + (rVisionDeltaY_um * 0.001);
                rCadTargetTheta_mrad := rCadTargetTheta_mrad + rVisionDeltaTheta_mrad;
                nFsmState := 8; (* Advance to Rotary Nozzle Theta Orientation Correction *)
            ELSE
                (* Reject defective packaging: chipped silicon, bent ball grid array *)
                nDefectiveRejectionsCount := nDefectiveRejectionsCount + 1;
                vec_u[4] := 0.0;   (* Drop vacuum *)
                vec_u[5] := 85.0;  (* Air puff eject *)
                nFsmState := 3;    (* Return to feeder bank for replacement part *)
            END_IF;
            
        8: (* STATE_ROTARY_NOZZLE_THETA_ORIENTATION_CORRECTION *)
            bPickAndPlaceActive := TRUE;
            vec_u[1] := arr_u_traj[0, 1];
            vec_u[2] := arr_u_traj[0, 2];
            vec_u[3] := -20.0;
            vec_u[4] := 95.0;
            vec_u[5] := 0.0;
            
            (* Check angular convergence within 0.85 mrad *)
            IF (ABS(vec_x[5]) <= 0.85) AND (rFsmStateDwell_s >= 0.008) THEN
                nFsmState := 9; (* Advance to Precision Placement Descent MPC Run *)
            END_IF;
            
        9: (* STATE_PRECISION_PLACEMENT_DESCENT_MPC_RUN *)
            bPickAndPlaceActive := TRUE;
            (* MPC optimizes Voice Coil Z descent while incorporating Board Warpage Offset Z *)
            vec_u[1] := arr_u_traj[0, 1];
            vec_u[2] := arr_u_traj[0, 2];
            vec_u[3] := arr_u_traj[0, 3]; (* Controlled voice coil descent *)
            vec_u[4] := 85.0;             (* Hold vacuum until landing confirmed *)
            vec_u[5] := 0.0;
            
            (* Detect touchdown contact force breaking through solder paste: 1.50 N <= F <= 2.20 N *)
            IF (rVotedContactForce_N >= 1.50) AND (rVotedContactForce_N <= 2.20) THEN
                rTouchdownForceDwell_s := rTouchdownForceDwell_s + T_SCAN_SEC;
                IF rTouchdownForceDwell_s >= 0.006 THEN
                    rTouchdownForceDwell_s := 0.0;
                    nFsmState := 10; (* Advance to Controlled Contact Landing & Puff Release *)
                END_IF;
            ELSE
                rTouchdownForceDwell_s := 0.0;
            END_IF;
            
            (* Hard limit enforcement: If force spikes towards 2.50 N, abort immediately *)
            IF rVotedContactForce_N > rMaxAllowableContactForce_N THEN
                bFastInterruptBrakeTrip := TRUE;
                vec_u[3] := -100.0; (* Instantaneous Voice Coil Retract *)
                nFsmState := 13;    (* Jump to Emergency Lockout *)
            END_IF;
            
        10: (* STATE_CONTROLLED_CONTACT_FORCE_LANDING_AND_PUFF_RELEASE *)
            bPickAndPlaceActive := TRUE;
            vec_u[1] := 0.0;
            vec_u[2] := 0.0;
            vec_u[3] := 15.0;  (* Gentle holding force on die *)
            vec_u[4] := 0.0;   (* Turn off suction vacuum *)
            vec_u[5] := 75.0;  (* Fire micro-pulse positive blow-off release puff *)
            
            rBlowOffPuffTimer_s := rBlowOffPuffTimer_s + T_SCAN_SEC;
            IF rBlowOffPuffTimer_s >= 0.008 THEN
                rBlowOffPuffTimer_s := 0.0;
                vec_u[5] := 0.0; (* Terminate puff *)
                nFsmState := 11; (* Advance to Nozzle Rapid Retract & Optical AOI Inspect *)
            END_IF;
            
        11: (* STATE_NOZZLE_RAPID_RETRACT_AND_OPTICAL_AOI_INSPECT *)
            bPickAndPlaceActive := TRUE;
            vec_u[3] := -50.0; (* Rapid Z upward retraction to clearance height *)
            vec_u[4] := 0.0;
            vec_u[5] := 0.0;
            
            (* Increment conforming placement production counters *)
            nPlacementsCountInternal := nPlacementsCountInternal + 1;
            rLastCycleDuration_s := MAX(0.015, rCycleTimer_s);
            rCycleTimer_s := 0.0;
            rInstantaneousCPH := 3600.0 / rLastCycleDuration_s;
            rCycleTimePlacement_ms := rLastCycleDuration_s * 1000.0;
            
            (* Check whether current PCB pattern is complete (e.g. 240 components per panel) *)
            IF (nPlacementsCountInternal MOD 240 = 0) THEN
                nFsmState := 12; (* Advance to Finished PCB Unclamp & Lane Discharge *)
            ELSE
                nFsmState := 3;  (* High-speed loop to next component pickup *)
            END_IF;
            
        12: (* STATE_FINISHED_PCB_UNCLAMP_AND_LANE_DISCHARGE *)
            bPickAndPlaceActive := FALSE;
            bSupportPinsEngaged := FALSE; (* Retract underside hydraulic support pins *)
            bLaneClampEngaged   := FALSE; (* Release pneumatic edge clamps *)
            vec_u[1] := 0.0;
            vec_u[2] := 0.0;
            vec_u[3] := -30.0;
            vec_u[4] := 0.0;
            vec_u[5] := 0.0;
            
            (* Discharge populated automotive ECU PCB to downstream reflow oven conveyor *)
            IF nActiveLaneUnderPlacement = 1 THEN
                bConveyorRunLane1 := TRUE;
                bConveyorRunLane2 := FALSE;
            ELSE
                bConveyorRunLane1 := FALSE;
                bConveyorRunLane2 := TRUE;
            END_IF;
            
            IF (rFsmStateDwell_s >= 0.080) THEN
                (* Seamlessly toggle to opposite lane to maintain non-stop 120,000 CPH throughput *)
                IF nActiveLaneUnderPlacement = 1 THEN
                    nActiveLaneUnderPlacement := 2;
                ELSE
                    nActiveLaneUnderPlacement := 1;
                END_IF;
                bConveyorRunLane1 := FALSE;
                bConveyorRunLane2 := FALSE;
                nFsmState := 1; (* Feed and scan incoming PCB on toggled lane *)
            END_IF;
            
        13: (* STATE_EMERGENCY_HEAD_COLLISION_OR_VACUUM_LOSS_TRIP *)
            bPickAndPlaceActive := FALSE;
            bEmergencyTripActive := TRUE;
            vec_u[1] := 0.0; (* Dynamic regenerative braking current zeroing *)
            vec_u[2] := 0.0;
            vec_u[3] := -100.0; (* Maximum Voice Coil Retraction *)
            vec_u[4] := 0.0;
            vec_u[5] := 0.0;
            
            rEmergencyBrakeHoldTimer_s := rEmergencyBrakeHoldTimer_s + T_SCAN_SEC;
            IF bAlarmReset AND (rEmergencyBrakeHoldTimer_s >= 0.500) THEN
                bFastInterruptBrakeTrip := FALSE;
                bEmergencyTripActive   := FALSE;
                rEmergencyBrakeHoldTimer_s := 0.0;
                nFsmState := 0; (* Reset to State 0: Idle *)
            END_IF;
    END_CASE;
ELSE
    (* Master E-Stop or Safety Interlock Trip *)
    nFsmState := 13;
    bEmergencyTripActive := TRUE;
    bPickAndPlaceActive  := FALSE;
    vec_u[1] := 0.0;
    vec_u[2] := 0.0;
    vec_u[3] := -100.0;
    vec_u[4] := 0.0;
    vec_u[5] := 0.0;
END_IF;

(* Advance Single Component Cycle Timer *)
rCycleTimer_s := rCycleTimer_s + T_SCAN_SEC;

(* ==================================================================================================================== *)
(* PHASE 5: ISA-18.2 MULTI-TIER ALARMS & 32-BIT BIT-PACKED STATUS / TELEMETRY DWORDS                                   *)
(* Multi-Tier Matrix: High-High (HH), High (H), Low (L), Low-Low (LL) with Clearance Deadband Hysteresis              *)
(* ==================================================================================================================== *)
(* 1. Touchdown Contact Force Alarms (Die Micro-Crack Protection: Hard Limit 2.50 N) *)
IF rVotedContactForce_N >= rAlmForce_HH_N THEN
    bAlmForce_HH_Active := TRUE;
    bFastInterruptBrakeTrip := TRUE; (* Ultra-fast <0.5ms voice coil back-off to protect silicon die *)
    IF dwFirstOutWord = 16#00000000 THEN
        dwFirstOutWord := 16#00000001; (* First-Out Root Cause 1: Touchdown Force HH Die Crack Limit Exceeded *)
    END_IF;
ELSIF rVotedContactForce_N < (rAlmForce_HH_N - rAlmForce_Deadband_N) THEN
    IF bAlarmAcknowledge THEN
        bAlmForce_HH_Active := FALSE;
    END_IF;
END_IF;

IF rVotedContactForce_N >= rAlmForce_H_N THEN
    bAlmForce_H_Active := TRUE;
ELSIF rVotedContactForce_N < (rAlmForce_H_N - rAlmForce_Deadband_N) THEN
    bAlmForce_H_Active := FALSE;
END_IF;

IF (nProductionState = 9) AND (rVotedContactForce_N <= rAlmForce_LL_N) AND (rFsmStateDwell_s > 0.015) THEN
    bAlmForce_LL_Active := TRUE;
    IF dwFirstOutWord = 16#00000000 THEN
        dwFirstOutWord := 16#00000002; (* First-Out Root Cause 2: Missing Component / No Touchdown Contact *)
    END_IF;
ELSIF rVotedContactForce_N > (rAlmForce_LL_N + rAlmForce_Deadband_N) THEN
    IF bAlarmAcknowledge THEN
        bAlmForce_LL_Active := FALSE;
    END_IF;
END_IF;

(* 2. Nozzle Vacuum Pressure Alarms *)
IF (nProductionState >= 4) AND (nProductionState <= 9) AND (rVotedNozzleVacuum_kPa >= rAlmVac_HH_kPa) THEN
    bAlmVac_HH_Active := TRUE;
    IF dwFirstOutWord = 16#00000000 THEN
        dwFirstOutWord := 16#00000004; (* First-Out Root Cause 4: Component Dropped In Flight *)
    END_IF;
ELSIF rVotedNozzleVacuum_kPa < (rAlmVac_HH_kPa - rAlmVac_Deadband_kPa) THEN
    IF bAlarmAcknowledge THEN
        bAlmVac_HH_Active := FALSE;
    END_IF;
END_IF;

IF rVotedNozzleVacuum_kPa >= rAlmVac_H_kPa THEN
    bAlmVac_H_Active := TRUE;
ELSIF rVotedNozzleVacuum_kPa < (rAlmVac_H_kPa - rAlmVac_Deadband_kPa) THEN
    bAlmVac_H_Active := FALSE;
END_IF;

(* 3. Machine Frame Dynamic Vibration Accelerometer Alarms *)
IF rVotedFrameVib_mps2 >= rAlmVib_HH_mps2 THEN
    bAlmVib_HH_Active := TRUE;
    bFastInterruptBrakeTrip := TRUE; (* Severe collision impact dynamic brake firing *)
    IF dwFirstOutWord = 16#00000000 THEN
        dwFirstOutWord := 16#00000008; (* First-Out Root Cause 8: High Frame Shock / Collision *)
    END_IF;
ELSIF rVotedFrameVib_mps2 < (rAlmVib_HH_mps2 - rAlmVib_Deadband_mps2) THEN
    IF bAlarmAcknowledge THEN
        bAlmVib_HH_Active := FALSE;
    END_IF;
END_IF;

IF rVotedFrameVib_mps2 >= rAlmVib_H_mps2 THEN
    bAlmVib_H_Active := TRUE;
ELSIF rVotedFrameVib_mps2 < (rAlmVib_H_mps2 - rAlmVib_Deadband_mps2) THEN
    bAlmVib_H_Active := FALSE;
END_IF;

(* 4. Gantry Position Tracking Error Alarms *)
IF (ABS(vec_x[1]) >= rAlmTrack_HH_um) OR (ABS(vec_x[2]) >= rAlmTrack_HH_um) THEN
    bAlmTrack_HH_Active := TRUE;
    bFastInterruptBrakeTrip := TRUE; (* High-speed tracking divergence trip *)
    IF dwFirstOutWord = 16#00000000 THEN
        dwFirstOutWord := 16#00000010; (* First-Out Root Cause 16: Linear Motor Tracking Deviation HH *)
    END_IF;
ELSIF (ABS(vec_x[1]) < (rAlmTrack_HH_um - rAlmTrack_Deadband_um)) AND (ABS(vec_x[2]) < (rAlmTrack_HH_um - rAlmTrack_Deadband_um)) THEN
    IF bAlarmAcknowledge THEN
        bAlmTrack_HH_Active := FALSE;
    END_IF;
END_IF;

IF (ABS(vec_x[1]) >= rAlmTrack_H_um) OR (ABS(vec_x[2]) >= rAlmTrack_H_um) THEN
    bAlmTrack_H_Active := TRUE;
ELSIF (ABS(vec_x[1]) < (rAlmTrack_H_um - rAlmTrack_Deadband_um)) AND (ABS(vec_x[2]) < (rAlmTrack_H_um - rAlmTrack_Deadband_um)) THEN
    bAlmTrack_H_Active := FALSE;
END_IF;

(* 5. Angular Theta Misalignment Alarms *)
IF ABS(vec_x[5]) >= rAlmTheta_HH_mrad THEN
    bAlmTheta_HH_Active := TRUE;
    IF dwFirstOutWord = 16#00000000 THEN
        dwFirstOutWord := 16#00000020; (* First-Out Root Cause 32: Rotary Theta Misalignment Exceeded *)
    END_IF;
ELSIF ABS(vec_x[5]) < (rAlmTheta_HH_mrad - rAlmTheta_Deadband_mrad) THEN
    IF bAlarmAcknowledge THEN
        bAlmTheta_HH_Active := FALSE;
    END_IF;
END_IF;

IF ABS(vec_x[5]) >= rAlmTheta_H_mrad THEN
    bAlmTheta_H_Active := TRUE;
ELSIF ABS(vec_x[5]) < (rAlmTheta_H_mrad - rAlmTheta_Deadband_mrad) THEN
    bAlmTheta_H_Active := FALSE;
END_IF;

(* Clear First-Out Alarm Register on Master Reset *)
IF bAlarmReset THEN
    dwFirstOutWord := 16#00000000;
END_IF;

(* Master Emergency Trip Active Status Flag *)
bEmergencyTripActive := NOT bEmergencyStopHealthy OR bFastInterruptBrakeTrip OR 
                        bAlmForce_HH_Active OR bAlmVib_HH_Active OR bAlmTrack_HH_Active;

(* Output Manipulated Actuator Commands to Hardware Interfaces *)
rLinearMotorCurrentCmdX_pct   := vec_u[1];
rLinearMotorCurrentCmdY_pct   := vec_u[2];
rVoiceCoilZForceCmd_pct       := vec_u[3];
rVacuumVenturiSolenoidCmd_pct := vec_u[4];
rPositiveBlowOffPuffCmd_pct   := vec_u[5];
nProductionState              := nFsmState;
nComponentsPlacedTotal        := nPlacementsCountInternal;

(* Store Actuator Command History for Slew Rate Optimization *)
FOR idx_m := 1 TO 5 DO
    vec_u_prev[idx_m] := vec_u[idx_m];
END_FOR;

(* ============================================================================================== *)
(* 32-BIT BIT-PACKED STATUS & DIAGNOSTIC TELEMETRY DWORDS                                        *)
(* ============================================================================================== *)
(* dwStatusWord1: Operational State, Interlocks & Tooling Bitmask *)
dwStatusWord1 := 16#00000000;
IF bSystemEnable THEN dwStatusWord1 := dwStatusWord1 OR 16#00000001; END_IF;
IF bProductionRunCmd THEN dwStatusWord1 := dwStatusWord1 OR 16#00000002; END_IF;
IF bEmergencyStopHealthy THEN dwStatusWord1 := dwStatusWord1 OR 16#00000004; END_IF;
IF bSystemReady THEN dwStatusWord1 := dwStatusWord1 OR 16#00000008; END_IF;
IF bPickAndPlaceActive THEN dwStatusWord1 := dwStatusWord1 OR 16#00000010; END_IF;
IF bSafetyDoorInterlockLocked THEN dwStatusWord1 := dwStatusWord1 OR 16#00000020; END_IF;
IF bPneumaticPressureMainOK THEN dwStatusWord1 := dwStatusWord1 OR 16#00000040; END_IF;
IF bMainVacuumSupplyOK THEN dwStatusWord1 := dwStatusWord1 OR 16#00000080; END_IF;
IF bLane1PcbClamped THEN dwStatusWord1 := dwStatusWord1 OR 16#00000100; END_IF;
IF bLane2PcbClamped THEN dwStatusWord1 := dwStatusWord1 OR 16#00000200; END_IF;
IF bSupportPinsEngagedFeedback THEN dwStatusWord1 := dwStatusWord1 OR 16#00000400; END_IF;
IF bVisionStrobeTrigger THEN dwStatusWord1 := dwStatusWord1 OR 16#00000800; END_IF;
IF bVisionInspectionPassed THEN dwStatusWord1 := dwStatusWord1 OR 16#00001000; END_IF;
IF bNozzleSealConforming THEN dwStatusWord1 := dwStatusWord1 OR 16#00002000; END_IF;
IF bComponentTombstoneDetected THEN dwStatusWord1 := dwStatusWord1 OR 16#00004000; END_IF;
IF bWarpageMapValid THEN dwStatusWord1 := dwStatusWord1 OR 16#00008000; END_IF;
dwStatusWord1 := dwStatusWord1 OR SHL(INT_TO_DWORD(nFsmState), 16);
dwStatusWord1 := dwStatusWord1 OR SHL(INT_TO_DWORD(nActiveLaneUnderPlacement), 28);

(* dwStatusWord2: Sensor TMR Health & Voting Mode Bitmask *)
dwStatusWord2 := 16#00000000;
IF bScaleX_ChanA_Healthy THEN dwStatusWord2 := dwStatusWord2 OR 16#00000001; END_IF;
IF bScaleX_ChanB_Healthy THEN dwStatusWord2 := dwStatusWord2 OR 16#00000002; END_IF;
IF bScaleX_ChanC_Healthy THEN dwStatusWord2 := dwStatusWord2 OR 16#00000004; END_IF;
IF bScaleY_ChanA_Healthy THEN dwStatusWord2 := dwStatusWord2 OR 16#00000008; END_IF;
IF bScaleY_ChanB_Healthy THEN dwStatusWord2 := dwStatusWord2 OR 16#00000010; END_IF;
IF bScaleY_ChanC_Healthy THEN dwStatusWord2 := dwStatusWord2 OR 16#00000020; END_IF;
IF bVac_ChanA_Healthy THEN dwStatusWord2 := dwStatusWord2 OR 16#00000040; END_IF;
IF bVac_ChanB_Healthy THEN dwStatusWord2 := dwStatusWord2 OR 16#00000080; END_IF;
IF bVac_ChanC_Healthy THEN dwStatusWord2 := dwStatusWord2 OR 16#00000100; END_IF;
IF bForce_ChanA_Healthy THEN dwStatusWord2 := dwStatusWord2 OR 16#00000200; END_IF;
IF bForce_ChanB_Healthy THEN dwStatusWord2 := dwStatusWord2 OR 16#00000400; END_IF;
IF bForce_ChanC_Healthy THEN dwStatusWord2 := dwStatusWord2 OR 16#00000800; END_IF;
IF bVib_ChanA_Healthy THEN dwStatusWord2 := dwStatusWord2 OR 16#00001000; END_IF;
IF bVib_ChanB_Healthy THEN dwStatusWord2 := dwStatusWord2 OR 16#00002000; END_IF;
IF bVib_ChanC_Healthy THEN dwStatusWord2 := dwStatusWord2 OR 16#00004000; END_IF;
dwStatusWord2 := dwStatusWord2 OR SHL(INT_TO_DWORD(nScaleX_VotingMode), 16);
dwStatusWord2 := dwStatusWord2 OR SHL(INT_TO_DWORD(nScaleY_VotingMode), 20);
dwStatusWord2 := dwStatusWord2 OR SHL(INT_TO_DWORD(nVac_VotingMode), 24);
dwStatusWord2 := dwStatusWord2 OR SHL(INT_TO_DWORD(nForce_VotingMode), 28);

(* dwAlarmWord1: High-High & Low-Low Safety Critical Trips *)
dwAlarmWord1 := 16#00000000;
IF bAlmForce_HH_Active THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000001; END_IF;
IF bAlmForce_LL_Active THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000002; END_IF;
IF bAlmVac_HH_Active THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000004; END_IF;
IF bAlmVib_HH_Active THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000008; END_IF;
IF bAlmTrack_HH_Active THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000010; END_IF;
IF bAlmTheta_HH_Active THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000020; END_IF;
IF bFastInterruptBrakeTrip THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000040; END_IF;
IF NOT bEmergencyStopHealthy THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000080; END_IF;

(* dwAlarmWord2: Process Warnings & Non-Critical Degradations *)
dwAlarmWord2 := 16#00000000;
IF bAlmForce_H_Active THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000001; END_IF;
IF bAlmForce_L_Active THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000002; END_IF;
IF bAlmVac_H_Active THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000004; END_IF;
IF bAlmVib_H_Active THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000008; END_IF;
IF bAlmTrack_H_Active THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000010; END_IF;
IF bAlmTheta_H_Active THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000020; END_IF;
IF bComponentTombstoneDetected THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000040; END_IF;

END_FUNCTION_BLOCK