# brain_scratch/can_seamer_builder/part1_decl.py

PART1_DECL = """FUNCTION_BLOCK FB_FoodBev_RotaryCanSeamer_DoubleSeam_InertN2
(* ==========================================================================================
 * LUMINA CYBER-PHYSICAL AUTOMATION ENGINE - IEC 61131-3 HIGH-PERFORMANCE STRUCTURED TEXT
 * ARCHITECTURE: ULTRA-HIGH-SPEED CONTINUOUS ROTARY ASEPTIC BEVERAGE CAN SEAMER
 * CAPACITY: 1,200 CANS/MINUTE (20 CANS/SECOND, 18-HEAD ROTARY SEAMING TURRET)
 * TARGET PROCESS: ASEPTIC BEVERAGE CANNING (ALUMINUM BEVERAGE CAN 202/204/211 FORMATS)
 * 
 * CORE SUBSYSTEMS INTEGRATED:
 *  1. Dynamic Double-Seam Mechanical Profiling:
 *     - Multi-axis electronic cam synchronization between 1st operation curl roll and
 *       2nd operation flattening roll servos.
 *     - Real-time seaming chuck axial load strain-gauge monitoring (3.5 kN to 8.0 kN).
 *     - Individual 18-head statistical variance tracking and predictive wear modeling.
 *  2. Liquid Nitrogen (LN2) Headspace Micro-Dosing Injection:
 *     - Cryogenic micro-solenoid valve pulsed injection at -196.0 deg C.
 *     - Precise millisecond pulse width modulation proportional to turret line speed.
 *     - Internal headspace pressurization (1.2 to 2.8 bar) and residual O2 purge (< 0.8%).
 *  3. Acoustic Impulse Sound Pressure Resonance Can Leak & Pressure Inspection:
 *     - Non-destructive piezoelectric impulse strike and sound pressure resonance spectrum.
 *     - Resonant frequency tracking (2.4 to 3.8 kHz) for micro-leaks, bulged/dented cans.
 *  4. Sterile Steam Barrier Turret Enclosure:
 *     - Continuous 125.0 deg C saturated steam labyrinth seal preventing microbial ingress.
 *     - Real-time accumulated sterilization lethality F0 thermal death time integration.
 *  5. Synchronous Rotary Infeed Worm Screw & Starwheel Transfer:
 *     - Electronic gearing and dynamic phase trimming to eliminate container jamming.
 *  6. 8-State Discrete State-Space Model (A, B, C, D) & Luenberger State Estimator.
 *  7. Receding-Horizon Model Predictive Control (MPC) Quadratic Cost Optimization.
 *  8. 2oo3 Triple Modular Redundancy (TMR) on Load Cells, LN2 Pressure, Steam RTDs, Acoustic Pings.
 *  9. Deterministic 12-Stage Finite State Machine (FSM).
 * 10. ISA-18.2 Multi-Tiered Alarm Hierarchy & Diagnostic Bitmask Packing.
 * ========================================================================================== *)

VAR_INPUT
    (* Supervisory Permissives & Safety Commands *)
    bEnable                         : BOOL;     (* System Master Automation Enable [bool] *)
    bEStop_Ok                       : BOOL;     (* Dual-channel Emergency Stop circuit healthy [bool] *)
    bSterileSteam_Permissive        : BOOL;     (* Steam barrier supply pressure & quality permissive [bool] *)
    bLN2_Dosing_Permissive          : BOOL;     (* Liquid Nitrogen cryogenic manifold supply permissive [bool] *)
    bCIP_Wash_Request               : BOOL;     (* Operator / supervisory CIP sanitization cycle request [bool] *)
    bReset_Faults                   : BOOL;     (* Master Alarm and Interlock Reset Pushbutton [bool] *)

    (* Turret Kinematics & Multi-Axis Servo Position / Speed Feedback *)
    rTurret_Speed_Actual_RPM        : REAL;     (* Rotary seamer main turret actual speed [rpm], nominal 66.67 rpm (1200 cpm) *)
    rTurret_Angular_Pos_Deg         : REAL;     (* Master rotary turret absolute position [deg], 0.0 to 360.0 *)
    rInfeed_WormScrew_Phase_Deg     : REAL;     (* Infeed timing worm screw electronic cam phase [deg], 0.0 to 360.0 *)
    rInfeed_Starwheel_Phase_Deg     : REAL;     (* Infeed transfer starwheel pocket phase [deg], 0.0 to 360.0 *)
    rDriveMotor_Torque_Nm           : REAL;     (* Main turret electric servo drive feedback torque [Nm], 0.0 to 500.0 Nm *)

    (* Station Tracking & Proximity Sensors *)
    iActive_Head_ID                 : INT;      (* Active seaming station head index currently at seaming station [1..18] *)
    bCan_Present_Infeed             : BOOL;     (* High-speed optical sensor: container present at infeed worm screw [bool] *)
    bEnd_Present_Chute              : BOOL;     (* Proximity sensor: can lid / end stack present in downstack chute [bool] *)
    bCan_Lid_Separated              : BOOL;     (* Rotary knife vacuum lid singulation confirmation [bool] *)
    bDischarge_Jam_Sensor           : BOOL;     (* Discharge starwheel / conveyor photoelectric anti-jam sensor [bool] *)

    (* 2oo3 TMR Triplets: Seaming Chuck Axial Load Transducers (Active Head Preload Strain Gauges) *)
    rChuck_AxialLoad_ChA            : REAL;     (* Seaming station lifter chuck axial strain gauge Channel A [kN], 0.0 to 12.0 kN *)
    rChuck_AxialLoad_ChB            : REAL;     (* Seaming station lifter chuck axial strain gauge Channel B [kN], 0.0 to 12.0 kN *)
    rChuck_AxialLoad_ChC            : REAL;     (* Seaming station lifter chuck axial strain gauge Channel C [kN], 0.0 to 12.0 kN *)

    (* 2oo3 TMR Triplets: Cryogenic Liquid Nitrogen (LN2) Supply Manifold Pressure *)
    rLN2_SupplyPressure_ChA         : REAL;     (* Cryogenic LN2 supply manifold pressure transmitter ChA [bar], 0.0 to 6.0 bar *)
    rLN2_SupplyPressure_ChB         : REAL;     (* Cryogenic LN2 supply manifold pressure transmitter ChB [bar], 0.0 to 6.0 bar *)
    rLN2_SupplyPressure_ChC         : REAL;     (* Cryogenic LN2 supply manifold pressure transmitter ChC [bar], 0.0 to 6.0 bar *)
    rLN2_ManifoldTemp_degC          : REAL;     (* Cryogenic LN2 dosing manifold sub-cooling RTD [deg C], nominal -196.0 deg C *)

    (* 2oo3 TMR Triplets: Aseptic Turret Steam Barrier Temperature RTDs (Labyrinth Seal Enclosure) *)
    rSteamBarrier_Temp_ChA          : REAL;     (* Aseptic steam seal enclosure PT100 RTD Channel A [deg C], 20.0 to 150.0 deg C *)
    rSteamBarrier_Temp_ChB          : REAL;     (* Aseptic steam seal enclosure PT100 RTD Channel B [deg C], 20.0 to 150.0 deg C *)
    rSteamBarrier_Temp_ChC          : REAL;     (* Aseptic steam seal enclosure PT100 RTD Channel C [deg C], 20.0 to 150.0 deg C *)
    rSteamBarrier_Pressure_bar      : REAL;     (* Saturated steam barrier labyrinth header pressure [bar], 0.0 to 4.0 bar *)

    (* 2oo3 TMR Triplets: Non-Destructive Acoustic Sound Resonance Can Inspection Array *)
    rAcoustic_ResonanceFreq_ChA     : REAL;     (* Acoustic sound pressure sensor ChA resonance frequency peak [kHz], 1.5 to 5.0 kHz *)
    rAcoustic_ResonanceFreq_ChB     : REAL;     (* Acoustic sound pressure sensor ChB resonance frequency peak [kHz], 1.5 to 5.0 kHz *)
    rAcoustic_ResonanceFreq_ChC     : REAL;     (* Acoustic sound pressure sensor ChC resonance frequency peak [kHz], 1.5 to 5.0 kHz *)
    rAcoustic_ImpulseDecay_ms       : REAL;     (* Acoustic ping impulse sound pressure ring-down decay [ms], 2.0 to 60.0 ms *)

    (* Online Optical & Laser Seam Quality Triangulation Transducers *)
    rLaser_SeamThickness_mm         : REAL;     (* High-speed laser triangulation seam thickness gauge [mm], 0.80 to 1.60 mm *)
    rLaser_SeamHeight_mm            : REAL;     (* High-speed laser triangulation seam height gauge [mm], 2.40 to 3.60 mm *)
    rLaser_CountersinkDepth_mm      : REAL;     (* High-speed laser triangulation countersink depth gauge [mm], 2.60 to 3.80 mm *)
    rCan_HeadspaceDeflection_mm     : REAL;     (* Laser dome elastic deflection under internal can pressure [mm], 0.10 to 1.50 mm *)

    (* Discrete Scan Delta Time *)
    tCycle_DeltaTime_s              : REAL;     (* Real-time PLC task scan cycle delta time [s], nominal 0.001 to 0.010 s *)
END_VAR

VAR_OUTPUT
    (* Supervisory Status & Machine Operational Flags *)
    bSystem_Ready                   : BOOL;     (* Seamer ready for high-speed synchronized production [bool] *)
    bIn_Production                  : BOOL;     (* Seamer actively running at steady-state 1200 cpm production [bool] *)
    bEStop_Tripped                  : BOOL;     (* Emergency Stop active or critical safety jam tripped [bool] *)
    iCurrent_FSM_State              : INT;      (* Active 12-stage operational Finite State Machine state code [1..12] *)

    (* Motion Servo References & Dynamic Gearing Trim Commands *)
    rTurret_Speed_Command_RPM       : REAL;     (* Main rotary turret servo master speed setpoint [rpm], 0.0 to 75.0 rpm *)
    rInfeed_Phase_Trim_Deg          : REAL;     (* Infeed worm screw electronic cam dynamic phase trim [deg], +/- 15.0 deg *)
    rInfeed_Starwheel_Phase_Trim_Deg: REAL;     (* Infeed starwheel pocket dynamic electronic cam phase trim [deg], +/- 10.0 deg *)
    rSeamingRoll_1stOp_CamTrim_mm   : REAL;     (* 1st operation curl roll dynamic servo cam depth trim [mm], +/- 0.50 mm *)
    rSeamingRoll_2ndOp_CamTrim_mm   : REAL;     (* 2nd operation ironing roll dynamic servo cam depth trim [mm], +/- 0.35 mm *)

    (* Cryogenic Nitrogen & Aseptic Steam Actuation Outputs *)
    rLN2_InjectorPulse_ms           : REAL;     (* Cryogenic LN2 micro-valve injection pulse width [ms], 2.0 to 35.0 ms *)
    bLN2_Dosing_Valve_Trigger       : BOOL;     (* High-speed solid-state digital output trigger for cryogenic micro-valve [bool] *)
    rSteamBarrier_Valve_Position_Pct: REAL;     (* Aseptic steam regulation valve modulating position command [%], 0.0 to 100.0% *)

    (* High-Speed Pneumatics & Defect Rejection Actuation *)
    bCan_Lifter_ChamberPneumatic_Up : BOOL;     (* Can lifter table pneumatic boost cylinder engage command [bool] *)
    bLid_Separator_Release_Solenoid : BOOL;     (* Rotary end feeder vacuum/knife separator solenoid trigger [bool] *)
    bAcoustic_Ping_Exciter_Trigger  : BOOL;     (* Piezoelectric acoustic striker impulse excitation pulse [bool] *)
    bReject_Gate_Actuator_Pulse     : BOOL;     (* High-speed pneumatic reject diverter gate pulse for defective cans [bool] *)

    (* Cyber-Physical Quality & Diagnostic Observables *)
    rSeam_TheoreticalOverlap_Pct    : REAL;     (* Estimated double-seam overlap percentage [%], nominal 65.0 to 85.0% *)
    rCan_InternalPressure_bar       : REAL;     (* Estimated internal can headspace gauge pressure [bar], nominal 1.85 bar *)
    rResidual_Oxygen_Pct            : REAL;     (* Estimated can headspace residual oxygen concentration [%], target < 0.8% *)
    rThermalBarrier_F0_Accum        : REAL;     (* Accumulated aseptic steam enclosure F0 lethality equivalent [minutes] *)
    rVoted_Chuck_AxialLoad_kN       : REAL;     (* 2oo3 TMR voted active chuck axial load force [kN], nominal 5.5 kN *)
    rVoted_LN2_Pressure_bar         : REAL;     (* 2oo3 TMR voted cryogenic LN2 supply manifold pressure [bar] *)
    rVoted_SteamBarrier_Temp_degC   : REAL;     (* 2oo3 TMR voted aseptic steam enclosure barrier temperature [deg C] *)
    rVoted_AcousticResonance_kHz    : REAL;     (* 2oo3 TMR voted acoustic ping sound resonance frequency [kHz] *)

    (* ISA-18.2 Diagnostic Packed Alarm Words & Defect Head Bitmasks *)
    dwAlarm_Critical_Safety         : DWORD;    (* Priority 1 Critical Safety & Emergency Abort Alarm Word [dword] *)
    dwAlarm_Process_Quality         : DWORD;    (* Priority 2 Process Out-of-Spec & Quality Rejection Word [dword] *)
    dwAlarm_Diagnostic_Wear         : DWORD;    (* Priority 3 Maintenance Advisory & Predictive Wear Word [dword] *)
    dwSystem_Status_Word            : DWORD;    (* Master Operational Diagnostic & Interlock Bitmask [dword] *)
    dwHead_Defect_Mask              : DWORD;    (* Bitmask of seaming heads exhibiting out-of-spec defects (bits 1..18) [dword] *)
    diTotal_Cans_Processed          : DINT;     (* Cumulative production can counter [cans] *)
    diTotal_Cans_Rejected           : DINT;     (* Cumulative defective rejected can counter [cans] *)
END_VAR

VAR
    (* ======================================================================================
     * INTERNAL CONSTANTS & OPERATIONAL BOUNDS
     * ====================================================================================== *)
    bInitialized                    : BOOL := FALSE;    (* Cold boot initialization flag [bool] *)
    rDeltaT                         : REAL;             (* Bounded PLC cycle scan execution time [s] *)
    
    (* Nominal Setpoints *)
    rSP_Turret_Speed_RPM            : REAL := 66.6667;  (* 1,200 cans/min / 18 heads = 66.6667 RPM [rpm] *)
    rSP_Chuck_AxialLoad_kN          : REAL := 5.50;     (* Nominal seaming chuck lifter axial load [kN] *)
    rSP_LN2_DosingPulse_ms          : REAL := 14.50;    (* Nominal cryogenic LN2 dosing pulse duration [ms] *)
    rSP_HeadspacePressure_bar       : REAL := 1.85;     (* Nominal target internal can pressure [bar] *)
    rSP_AcousticResonance_kHz       : REAL := 3.15;     (* Nominal acoustic ping resonance frequency [kHz] *)
    rSP_SteamBarrier_Temp_degC      : REAL := 125.0;    (* Nominal aseptic steam seal enclosure temperature [deg C] *)
    rSP_Infeed_Phase_Deg            : REAL := 0.0;      (* Synchronous infeed electronic cam phase setpoint [deg] *)

    (* ======================================================================================
     * 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) VOTING INTERNAL STRUCTURES
     * ====================================================================================== *)
    (* Channel A/B/C Discrepancy Timers [s] *)
    rTMR_AxialLoad_Discrep_Timer    : REAL := 0.0;
    rTMR_LN2Press_Discrep_Timer     : REAL := 0.0;
    rTMR_SteamTemp_Discrep_Timer    : REAL := 0.0;
    rTMR_Acoustic_Discrep_Timer     : REAL := 0.0;
    rTMR_Deflection_Discrep_Timer   : REAL := 0.0;

    (* Healthy Channel Flags *)
    bTMR_AxialLoad_ChA_Healthy      : BOOL := TRUE;
    bTMR_AxialLoad_ChB_Healthy      : BOOL := TRUE;
    bTMR_AxialLoad_ChC_Healthy      : BOOL := TRUE;
    bTMR_LN2Press_ChA_Healthy       : BOOL := TRUE;
    bTMR_LN2Press_ChB_Healthy       : BOOL := TRUE;
    bTMR_LN2Press_ChC_Healthy       : BOOL := TRUE;
    bTMR_SteamTemp_ChA_Healthy      : BOOL := TRUE;
    bTMR_SteamTemp_ChB_Healthy      : BOOL := TRUE;
    bTMR_SteamTemp_ChC_Healthy      : BOOL := TRUE;
    bTMR_Acoustic_ChA_Healthy       : BOOL := TRUE;
    bTMR_Acoustic_ChB_Healthy       : BOOL := TRUE;
    bTMR_Acoustic_ChC_Healthy       : BOOL := TRUE;

    (* TMR Discrepancy Trip Limits *)
    rTMR_Tol_AxialLoad_kN           : REAL := 0.75;     (* 0.75 kN max allowed inter-sensor discrepancy [kN] *)
    rTMR_Tol_LN2Press_bar           : REAL := 0.35;     (* 0.35 bar max allowed inter-sensor discrepancy [bar] *)
    rTMR_Tol_SteamTemp_degC         : REAL := 2.50;     (* 2.50 deg C max allowed inter-sensor discrepancy [deg C] *)
    rTMR_Tol_Acoustic_kHz           : REAL := 0.25;     (* 0.25 kHz max allowed acoustic peak discrepancy [kHz] *)
    rTMR_Discrepancy_Timeout_s      : REAL := 0.150;    (* Discrepancy persistence time before channel alarm [s] *)

    (* ======================================================================================
     * 8-STATE DISCRETE STATE-SPACE INTERNAL MATRICES (A, B, C, D) & LUENBERGER OBSERVER (L)
     * State Vector x[8]:
     *   x[1] = Delta Turret Speed Error [rpm]
     *   x[2] = Seaming Chuck Axial Load Force [kN]
     *   x[3] = LN2 Dosing Injection Pulse Width [ms]
     *   x[4] = Internal Can Headspace Pressure [bar]
     *   x[5] = Acoustic Resonance Frequency Peak [kHz]
     *   x[6] = Aseptic Steam Barrier Enclosure Temp [deg C]
     *   x[7] = Infeed Starwheel Phase Sync Error [mrad]
     *   x[8] = Seamer Main Drive Motor Torque Ripple [Nm]
     * ====================================================================================== *)
    aA_Matrix                       : ARRAY[1..8, 1..8] OF REAL; (* Discrete State Transition Matrix A [8x8] *)
    aB_Matrix                       : ARRAY[1..8, 1..6] OF REAL; (* Discrete Input Coupling Matrix B [8x6] *)
    aC_Matrix                       : ARRAY[1..6, 1..8] OF REAL; (* Discrete Output Measurement Matrix C [6x8] *)
    aD_Matrix                       : ARRAY[1..6, 1..6] OF REAL; (* Discrete Direct Feedthrough Matrix D [6x6] *)
    aL_ObserverGain                 : ARRAY[1..8, 1..6] OF REAL; (* Luenberger Kalman Filter Observer Gain L [8x6] *)

    (* State Vector, Estimated State Vector & Model Predictions *)
    ax_State                        : ARRAY[1..8] OF REAL; (* Actual / Filtered State Vector x[k] *)
    ax_Hat                          : ARRAY[1..8] OF REAL; (* Observer Estimated State Vector x_hat[k] *)
    ax_Pred                         : ARRAY[1..8] OF REAL; (* One-step ahead model predicted state x_hat[k+1] *)
    ay_Meas                         : ARRAY[1..6] OF REAL; (* Process Measurement Vector y[k] *)
    ay_Hat                          : ARRAY[1..6] OF REAL; (* Observer Estimated Measurement Vector y_hat[k] *)
    ay_Residual                     : ARRAY[1..6] OF REAL; (* Innovation Residual y[k] - y_hat[k] *)

    (* Control Input Vector u[6]:
     *   u[1] = Turret Speed Command Bias [rpm]
     *   u[2] = Lifter Axial Preload Bias [kN]
     *   u[3] = LN2 Micro-Valve Injection Trim [ms]
     *   u[4] = Steam Barrier Valve Modulation Position [%]
     *   u[5] = Infeed Worm Screw Phase Offset [mrad]
     *   u[6] = Dynamic Seaming Roll Cam Depth Bias [mm] *)
    au_Control                      : ARRAY[1..6] OF REAL; (* Saturated Applied Control Vector u[k] *)
    au_Unconstrained                : ARRAY[1..6] OF REAL; (* Raw Unconstrained MPC Control Vector u_raw[k] *)

    (* ======================================================================================
     * MODEL PREDICTIVE CONTROL (MPC) RECEDING-HORIZON MATRICES (Np=5, Nc=3)
     * ====================================================================================== *)
    aQ_StateWeight                  : ARRAY[1..8, 1..8] OF REAL; (* State Error Penalty Matrix Q [8x8] *)
    aR_ControlWeight                : ARRAY[1..6, 1..6] OF REAL; (* Actuator Effort Penalty Matrix R [6x6] *)
    aP_TerminalWeight               : ARRAY[1..8, 1..8] OF REAL; (* Terminal State Penalty Matrix P [8x8] *)
    ax_Reference                    : ARRAY[1..8] OF REAL;       (* State Setpoint Reference Vector x_ref *)
    
    (* MPC Horizons & Iteration Temp Storage *)
    ax_Horizon                      : ARRAY[1..5, 1..8] OF REAL; (* Predicted State Horizon x[k+h|k] *)
    au_Horizon                      : ARRAY[1..3, 1..6] OF REAL; (* Control Sequence Horizon u[k+j|k] *)
    rMPC_Cost_J                     : REAL := 0.0;               (* Evaluated Quadratic Cost Function Value J *)
    rMPC_Gradient_Step              : REAL := 0.0125;            (* Projected Gradient Descent Learning Rate *)

    (* Actuator Slew Rate Limiters & Bounds *)
    rMaxRate_TurretSpeed_RPM_s      : REAL := 15.0;     (* Max turret acceleration rate [rpm/s] *)
    rMaxRate_SteamValve_Pct_s       : REAL := 8.0;      (* Max steam valve stroke rate [%/s] *)
    rMaxRate_LN2Pulse_ms_s          : REAL := 25.0;     (* Max cryogenic pulse modulation slew rate [ms/s] *)
    rMaxRate_CamDepth_mm_s          : REAL := 1.20;     (* Max servo roll cam depth trim slew rate [mm/s] *)

    (* Prior Actuator Values for Slew Rate Calculation *)
    rLast_Turret_Speed_Cmd          : REAL := 0.0;
    rLast_SteamValve_Cmd            : REAL := 0.0;
    rLast_LN2Pulse_Cmd              : REAL := 0.0;
    rLast_1stOp_CamTrim             : REAL := 0.0;
    rLast_2ndOp_CamTrim             : REAL := 0.0;

    (* ======================================================================================
     * 18-HEAD INDIVIDUAL STATISTICAL PROFILING & PREDICTIVE WEAR MATRICES
     * ====================================================================================== *)
    aHead_AxialLoad_Mean            : ARRAY[1..18] OF REAL; (* Exponential moving average axial load [kN] *)
    aHead_AxialLoad_Peak            : ARRAY[1..18] OF REAL; (* Running peak seaming load [kN] *)
    aHead_AxialLoad_Min             : ARRAY[1..18] OF REAL; (* Running minimum chuck preload [kN] *)
    aHead_AxialLoad_Variance        : ARRAY[1..18] OF REAL; (* Running sample variance of axial load [kN^2] *)
    aHead_SeamThickness_Hist        : ARRAY[1..18] OF REAL; (* Historical moving average seam thickness [mm] *)
    aHead_SeamHeight_Hist           : ARRAY[1..18] OF REAL; (* Historical moving average seam height [mm] *)
    aHead_Countersink_Hist          : ARRAY[1..18] OF REAL; (* Historical moving average countersink [mm] *)
    aHead_ResonanceFreq_Hist        : ARRAY[1..18] OF REAL; (* Historical moving average acoustic frequency [kHz] *)
    aHead_RejectCount               : ARRAY[1..18] OF DINT; (* Number of rejected cans produced by head [cans] *)
    aHead_TotalCycles               : ARRAY[1..18] OF DINT; (* Total can cycles performed by head [cans] *)
    aHead_WearIndex_Pct             : ARRAY[1..18] OF REAL; (* Dynamic mechanical wear index [0.0 to 100.0%] *)
    aHead_CalibOffset_1stOp_mm      : ARRAY[1..18] OF REAL; (* Individual head 1st op roll eccentric offset [mm] *)
    aHead_CalibOffset_2ndOp_mm      : ARRAY[1..18] OF REAL; (* Individual head 2nd op roll eccentric offset [mm] *)

    (* Active Head Cycle Temporary Variables *)
    iHeadIdx                        : INT := 1;         (* General loop iterator for heads [1..18] *)
    iMatrixRow                      : INT := 1;         (* Matrix row index iterator *)
    iMatrixCol                      : INT := 1;         (* Matrix column index iterator *)
    iHorizonIdx                     : INT := 1;         (* MPC prediction horizon loop index *)
    iOptStep                        : INT := 1;         (* MPC gradient descent optimization step *)

    (* ======================================================================================
     * CYBER-PHYSICAL OBSERVER INTERNAL VARIABLES
     * ====================================================================================== *)
    (* Double-Seam Dimensions & Metal Sheet Specifications *)
    rSheetThick_Body_tb_mm          : REAL := 0.208;    (* Body sheet metal thickness (aluminum 3104-H19) [mm] *)
    rSheetThick_End_te_mm           : REAL := 0.224;    (* Can end / lid sheet thickness (aluminum 5182-H48) [mm] *)
    rSeam_CoverHook_CH_mm           : REAL := 1.95;     (* Estimated cover hook length [mm] *)
    rSeam_BodyHook_BH_mm            : REAL := 1.92;     (* Estimated body hook length [mm] *)
    rSeam_SeamLength_SL_mm          : REAL := 2.98;     (* Estimated seam height / length [mm] *)
    rSeam_TightnessRating_Pct       : REAL := 82.5;     (* Seam tightness index (% wrinkle-free) [%] *)

    (* Cryogenic LN2 Vaporization & Headspace Thermodynamics *)
    rHeadspace_Volume_mL            : REAL := 12.5;     (* Nominal open headspace volume above liquid [mL] *)
    rLN2_Density_kg_m3              : REAL := 808.4;    (* Liquid nitrogen density at -196 deg C [kg/m^3] *)
    rLN2_DoseMass_mg                : REAL := 85.0;     (* Vaporized nitrogen mass per injection [mg] *)
    rLN2_VaporExpansionRatio        : REAL := 694.0;    (* Volume expansion ratio liquid to gas at 20 deg C *)
    rN2_GasVolume_STP_mL            : REAL := 72.8;     (* Standard gas volume produced by dose [mL] *)
    rHeadspace_InitialO2_Pct        : REAL := 20.95;    (* Initial atmospheric oxygen concentration [%] *)
    rVaporization_RateConstant_s    : REAL := 45.0;     (* Flash boiling kinetics rate constant [1/s] *)

    (* Acoustic Dome Membrane Vibration Physics *)
    rCan_Lid_Radius_m               : REAL := 0.0265;   (* Can end dome effective diaphragm radius [m] *)
    rCan_Lid_SurfaceDensity_kg_m2   : REAL := 0.605;    (* Diaphragm area surface mass density [kg/m^2] *)
    rAcoustic_Model_Freq_kHz        : REAL := 3.15;     (* Theoretically predicted acoustic resonance [kHz] *)
    rAcoustic_Freq_Deviation_kHz    : REAL := 0.0;      (* Measured vs model resonance frequency error [kHz] *)
    bAcoustic_Defect_Detected       : BOOL := FALSE;    (* Acoustic ping failure flag [bool] *)

    (* Turret 18th-Order Spatially Periodic Torque Ripple Estimator *)
    rSpatial_Angle_Rad              : REAL := 0.0;      (* Turret angular position in radians [rad] *)
    rTorqueRipple_Harmonic1_Nm      : REAL := 0.0;      (* Fundamental 18th harmonic torque component [Nm] *)
    rTorqueRipple_Harmonic2_Nm      : REAL := 0.0;      (* 36th harmonic torque component [Nm] *)
    rTorqueRipple_Harmonic3_Nm      : REAL := 0.0;      (* 54th harmonic torque component [Nm] *)
    rTorqueRipple_Comp_Nm           : REAL := 0.0;      (* Active harmonic cancellation feedforward command [Nm] *)

    (* Aseptic Steam Barrier Heat Balance & F0 Accumulation *)
    rSteam_Enclosure_Temp_K         : REAL := 398.15;   (* Steam temperature in Kelvin [K] *)
    rSteam_Enclosure_Target_K       : REAL := 398.15;   (* Target 125 deg C in Kelvin [K] *)
    rF0_Lethality_Rate_min_s        : REAL := 0.0;      (* Instantaneous equivalent lethality rate [min/s] *)
    rSteam_Condensate_Flow_kg_h     : REAL := 4.2;      (* Steam condensation mass rate [kg/h] *)

    (* ======================================================================================
     * 12-STAGE FINITE STATE MACHINE (FSM) INTERNAL SEQUENCING
     * States:
     *   1:  STATE_STEAM_BARRIER_PURGE_125C
     *   2:  STATE_LN2_CHILLDOWN_MINUS196C
     *   3:  STATE_INFEED_TURRET_SYNC_INCHING
     *   4:  STATE_CAN_INFEED_LID_FEED_GATE
     *   5:  STATE_LN2_HEADSPACE_MICRODOSING
     *   6:  STATE_1ST_OP_CURL_ROLL_ENGAGE
     *   7:  STATE_2ND_OP_FLATTENING_IRON_DWELL
     *   8:  STATE_LASER_SEAM_GAUGING_ONLINE
     *   9:  STATE_ACOUSTIC_PING_LEAK_INSPECT
     *   10: STATE_REJECTION_GATE_ACTUATION
     *   11: STATE_ROTARY_CIP_SIP_SANITIZATION
     *   12: STATE_JAM_ESTOP_CLAMP_RETRACT
     * ====================================================================================== *)
    iState                          : INT := 1;         (* Current machine operating state [1..12] *)
    iNextState                      : INT := 1;         (* Desired next state for synchronous transition *)
    rState_Timer_s                  : REAL := 0.0;      (* Continuous state dwell timer [s] *)
    bState_First_Scan               : BOOL := TRUE;     (* Edge flag for state entry initialization *)

    (* State Transition Dwell Durations [s] *)
    tDwell_SteamPurge_Target_s      : REAL := 180.0;    (* 3-minute pre-sterilization steam dwell [s] *)
    tDwell_LN2Chill_Target_s        : REAL := 60.0;     (* 1-minute cryogenic vacuum line chill-down [s] *)
    tDwell_SyncInching_Target_s     : REAL := 5.0;      (* Turret phase synchronization inching dwell [s] *)
    tDwell_CIP_Target_s             : REAL := 300.0;    (* 5-minute rotary CIP chemical / steam flush [s] *)

    (* Dynamic Cam Generator Variables *)
    rCamAngle_1stOp_Deg             : REAL := 0.0;      (* 1st operation roll engagement cam angle [deg] *)
    rCamAngle_2ndOp_Deg             : REAL := 0.0;      (* 2nd operation roll engagement cam angle [deg] *)
    rCamProfile_1stOp_Pos_mm        : REAL := 0.0;      (* Theoretical 1st operation roll radial position [mm] *)
    rCamProfile_2ndOp_Pos_mm        : REAL := 0.0;      (* Theoretical 2nd operation roll radial position [mm] *)

    (* High-Speed Quality Tracking Shift Register (18 Turret Pockets + 12 Infeed/Discharge Pockets) *)
    abPocket_HasCan                 : ARRAY[1..36] OF BOOL; (* Container tracking shift register [bool] *)
    abPocket_HasEnd                 : ARRAY[1..36] OF BOOL; (* Lid present tracking shift register [bool] *)
    abPocket_DosedLN2               : ARRAY[1..36] OF BOOL; (* Nitrogen dosed confirmation [bool] *)
    abPocket_SeamedOK               : ARRAY[1..36] OF BOOL; (* Double seam mechanical integrity OK [bool] *)
    abPocket_AcousticPass           : ARRAY[1..36] OF BOOL; (* Acoustic resonance leak inspection PASS [bool] *)
    abPocket_RejectPending          : ARRAY[1..36] OF BOOL; (* Reject flag scheduled for discharge gate [bool] *)
    aiPocket_HeadOrigin             : ARRAY[1..36] OF INT;  (* Originating seaming head index [1..18] *)

    (* Rejection Actuation Pulse Timer *)
    rReject_Pulse_Timer_s           : REAL := 0.0;      (* Rejection pneumatic gate solenoid timer [s] *)
    rAcoustic_Pulse_Timer_s         : REAL := 0.0;      (* Acoustic striker hammer pulse timer [s] *)
    rLN2_Pulse_Timer_s              : REAL := 0.0;      (* Cryogenic dosing micro-valve timer [s] *)

    (* ======================================================================================
     * ISA-18.2 ALARM ENGINE TRIP POINTS, DEAD-BANDS & DEVIATION MONITORS
     * ====================================================================================== *)
    (* Axial Chuck Load Limits [kN] *)
    rTrip_AxialLoad_HH_kN           : REAL := 8.50;     (* High-High Chuck Mechanical Overload [kN] *)
    rTrip_AxialLoad_H_kN            : REAL := 7.20;     (* High Chuck Seaming Force Warning [kN] *)
    rTrip_AxialLoad_L_kN            : REAL := 4.00;     (* Low Chuck Lifter Preload Warning [kN] *)
    rTrip_AxialLoad_LL_kN           : REAL := 3.00;     (* Low-Low Chuck Collapse / Can Crushed [kN] *)
    rDeadband_AxialLoad_kN          : REAL := 0.20;     (* Axial load trip deadband hysteresis [kN] *)

    (* Cryogenic LN2 Supply Pressure Limits [bar] *)
    rTrip_LN2Press_HH_bar           : REAL := 3.80;     (* High-High Cryogenic Overpressure [bar] *)
    rTrip_LN2Press_H_bar            : REAL := 3.20;     (* High Cryogenic Pressure Warning [bar] *)
    rTrip_LN2Press_L_bar            : REAL := 1.80;     (* Low Cryogenic Pressure Warning [bar] *)
    rTrip_LN2Press_LL_bar           : REAL := 1.20;     (* Low-Low Cryogenic Cavitation / Depleted [bar] *)
    rDeadband_LN2Press_bar          : REAL := 0.10;     (* Pressure deadband hysteresis [bar] *)

    (* Aseptic Steam Barrier Temperature Limits [deg C] *)
    rTrip_SteamTemp_HH_degC         : REAL := 138.0;    (* High-High Steam Seal Overheat [deg C] *)
    rTrip_SteamTemp_H_degC          : REAL := 132.0;    (* High Steam Seal Temp Warning [deg C] *)
    rTrip_SteamTemp_L_degC          : REAL := 122.0;    (* Low Steam Seal Temp Warning [deg C] *)
    rTrip_SteamTemp_LL_degC         : REAL := 118.0;    (* Low-Low Aseptic Barrier Compromised [deg C] *)
    rDeadband_SteamTemp_degC        : REAL := 1.00;     (* Steam temperature deadband hysteresis [deg C] *)

    (* Seam Thickness Laser Inspection Limits [mm] *)
    rTrip_Thickness_HH_mm           : REAL := 1.40;     (* Loose Seam / Insufficient Compression [mm] *)
    rTrip_Thickness_LL_mm           : REAL := 0.98;     (* Over-rolled Seam / Metal Extrusion [mm] *)

    (* Headspace Residual Oxygen Limits [%] *)
    rTrip_ResidualO2_HH_Pct         : REAL := 1.50;     (* High-High Oxidative Flavor Spoilage [%] *)
    rTrip_ResidualO2_H_Pct          : REAL := 0.80;     (* High Residual Oxygen Target Threshold [%] *)

    (* Acoustic Ping Resonance Limits [kHz] *)
    rTrip_Acoustic_LL_kHz           : REAL := 2.20;     (* Low-Low Pressure Leak / Missing N2 Dose [kHz] *)
    rTrip_Acoustic_HH_kHz           : REAL := 4.10;     (* High-High Hydraulic Overfill Hydrostatic Lock [kHz] *)

    (* Internal Latching & Diagnostic Alarm Flags *)
    bAlarm_AxialLoad_HH             : BOOL := FALSE;
    bAlarm_AxialLoad_H              : BOOL := FALSE;
    bAlarm_AxialLoad_L              : BOOL := FALSE;
    bAlarm_AxialLoad_LL             : BOOL := FALSE;
    bAlarm_LN2Press_HH              : BOOL := FALSE;
    bAlarm_LN2Press_LL              : BOOL := FALSE;
    bAlarm_SteamTemp_LL             : BOOL := FALSE;
    bAlarm_InfeedSync_Fault         : BOOL := FALSE;
    bAlarm_TurretJam_Fault          : BOOL := FALSE;
    bAlarm_SeamThickness_Fault      : BOOL := FALSE;
    bAlarm_Oxygen_Elevated          : BOOL := FALSE;
    bAlarm_Acoustic_Leak_Fault      : BOOL := FALSE;
    bAlarm_Discharge_Jam            : BOOL := FALSE;
    bAlarm_TMR_Axial_Discrep        : BOOL := FALSE;
    bAlarm_TMR_LN2_Discrep          : BOOL := FALSE;
    bAlarm_TMR_Steam_Discrep        : BOOL := FALSE;
    bAlarm_TMR_Acoustic_Discrep     : BOOL := FALSE;
    bAlarm_IndividualHead_WearWarn  : BOOL := FALSE;
END_VAR
"""
