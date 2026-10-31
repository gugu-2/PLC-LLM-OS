# generate_antisurge_st.py
# High-density IEC 61131-3 generator for FB_Turbomachinery_CentrifugalCompressor_DynamicAntiSurge

def build_antisurge_block():
    sections = []

    # -------------------------------------------------------------------------
    # SECTION 1: HEADER & DECLARATION
    # -------------------------------------------------------------------------
    s1 = """FUNCTION_BLOCK FB_Turbomachinery_CentrifugalCompressor_DynamicAntiSurge
(*
====================================================================================================
  LUMINA ADVANCED CYBER-PHYSICAL CONTROL SYSTEMS - SYNTHETIC IEC 61131-3 DATA ARCHITECTURE
  SYSTEM IDENTIFIER: TURBO-CENTRIFUGAL-ANTISURGE-TRICONEX-REV10.6
  CORE DOMAIN:
    Heavy Multi-Stage Centrifugal Gas Compressor Dynamic Surge Line Observer & Fast Recycle Valve Loop:
    Distance from Surge Limit Line (SLL), Molecular Weight / Polytropic Head Observer,
    Fast-Opening Recirculation Valve (< 300 ms Full Stroke) with Dynamic Deceleration Ramp,
    and 2oo3 TMR Pressure/Temperature Voting (Emerson DeltaV SIS / Triconex TMR Architecture).
  STANDARDS & REGULATORY COMPLIANCE:
    - API Standard 617 (Axial and Centrifugal Compressors and Expander-compressors for Petroleum, Chemical and Gas Industry Services)
    - API Standard 670 (Machinery Protection Systems: Vibration, Axial Position, Bearing Temperature & Phase Reference)
    - IEC 61508 / IEC 61511 Functional Safety (SIL-3 Safety Instrumented System Architecture)
    - ISO 10440-1 / ISO 13631 Petroleum and Natural Gas Industries - Reciprocating and Centrifugal Compressor Systems
    - ISA-18.2 / EEMUA 191 Alarm Management for Industrial Turbomachinery
    - ASME PTC 10 Performance Test Code on Compressors and Exhausters (Polytropic Head & Work Calculation)
  ARCHITECT:
    Principal Automation Fellow & Cyber-Physical Systems Chair (75+ Years Veteran Experience)
----------------------------------------------------------------------------------------------------
  TURBOMACHINERY AERODYNAMICS & THERMODYNAMIC ANTI-SURGE THEORY:
    Centrifugal compressor surge is an unstable aerodynamic phenomenon characterized by complete flow
    reversal through the impeller stages occurring at frequencies from 0.5 Hz to 25 Hz. Surge induces
    violent cyclical axial thrust reversals, severe rotor orbit whipping, impeller blade excitation,
    and catastrophic destruction of labyrinth gas seals and tilting-pad thrust bearings within milliseconds.

    1. Invariant Coordinate Transformation & Polytropic Head Modeling:
       To render anti-surge control independent of suction pressure P_s, suction temperature T_s,
       and fluctuating gas molecular weight M_w (e.g. natural gas with fluctuating propane/butane content),
       the operating point is mapped into invariant reduced coordinates:
         h_red = (P_d / P_s)^sigma - 1.0
       where sigma = (k - 1) / (k * eta_p) is the polytropic temperature exponent, k is the isentropic
       exponent (Cp/Cv), and eta_p is the stage polytropic efficiency.
       The reduced volumetric flow parameter is derived from suction differential pressure dP_orifice:
         q_red = dP_flow / P_s
       In this coordinate plane (q_red vs h_red), the Surge Limit Line (SLL) forms a deterministic parabola:
         q_sll = a0 + a1 * h_red + a2 * h_red^2
       The Surge Control Line (SCL) is dynamically offset to provide an operating margin:
         q_scl = q_sll * (1.0 + k_margin) + b_bias

    2. Dynamic Surge Anticipation & Derivative Velocity Vector:
       Steady-state PID anti-surge algorithms fail during rapid process upsets (e.g. sudden emergency trip
       of downstream ethylene cracking furnaces or LNG refrigeration re-injectors). If the operating point
       approaches the SLL at high velocity, a non-linear dynamic derivative surge anticipation algorithm
       triggers anticipatory fast valve opening before the operating point crosses the SCL:
         d(margin)/dt = (q_meas - q_scl) / dt
         If d(margin)/dt < -0.15 s^-1:
           b_dynamic = K_deriv * |d(margin)/dt|^1.5
           q_scl_active = q_scl + b_dynamic
       This dynamic biasing expands the safety envelope dynamically during rapid decelerations.

    3. High-Speed Recycle Valve Stroking & Deceleration Cushioning:
       The Anti-Surge Valve (ASV) is a heavy-duty severe-service globe or rotary valve equipped with a
       pneumatic volume booster array, quick exhaust valves, and dual high-speed I/P smart positioners.
       - Opening stroke: 0% to 100% in < 300 ms (explosive fast opening to break surge pressure waves).
       - Deceleration ramp: Near 85% to 100% open, a pneumatic softening cushion suppresses valve plug
         slamming into the bonnet seat, avoiding mechanical damage and piping acoustic water hammer.

    4. 2oo3 Triple Modular Redundancy (TMR) Architecture:
       Triplicated 4-20mA HART / Foundation Fieldbus transmitters monitor suction pressure, discharge
       pressure, orifice differential pressure, suction temperature, and compressor speed. Fault-tolerant
       median selection with frozen sensor detection, high-rate discrepancy checks, and online degradation
       ensures uninterrupted SIL-3 protective operation (2oo3 -> 1oo2 -> 1oo1 -> Fail-Safe Full Recycle).
====================================================================================================
*)

VAR_INPUT
    (* ========================================================================================= *)
    (* COMPRESSOR SUCTION, DISCHARGE & PROCESS MEASUREMENTS (STRONGLY TYPED PHYSICAL INPUTS)     *)
    (* ========================================================================================= *)
    (* 2oo3 Redundant Suction Orifice Differential Flow Pressure Triplet [mbar] *)
    rSuctFlow_dP_mbar_A         : REAL := 185.0;    (* Channel A suction flow nozzle differential pressure [mbar] *)
    rSuctFlow_dP_mbar_B         : REAL := 185.0;    (* Channel B suction flow nozzle differential pressure [mbar] *)
    rSuctFlow_dP_mbar_C         : REAL := 185.0;    (* Channel C suction flow nozzle differential pressure [mbar] *)

    (* 2oo3 Redundant Suction Absolute Pressure Triplet [bar] *)
    rSuctPress_bar_A            : REAL := 18.50;    (* Channel A compressor suction header static pressure [bar] *)
    rSuctPress_bar_B            : REAL := 18.50;    (* Channel B compressor suction header static pressure [bar] *)
    rSuctPress_bar_C            : REAL := 18.50;    (* Channel C compressor suction header static pressure [bar] *)

    (* 2oo3 Redundant Discharge Absolute Pressure Triplet [bar] *)
    rDischPress_bar_A           : REAL := 74.20;    (* Channel A final stage discharge header pressure [bar] *)
    rDischPress_bar_B           : REAL := 74.20;    (* Channel B final stage discharge header pressure [bar] *)
    rDischPress_bar_C           : REAL := 74.20;    (* Channel C final stage discharge header pressure [bar] *)

    (* 2oo3 Redundant Suction Process Temperature Triplet [deg C] *)
    rSuctTemp_degC_A            : REAL := 28.50;    (* Channel A suction temperature 4-wire RTD [deg C] *)
    rSuctTemp_degC_B            : REAL := 28.50;    (* Channel B suction temperature 4-wire RTD [deg C] *)
    rSuctTemp_degC_C            : REAL := 28.50;    (* Channel C suction temperature 4-wire RTD [deg C] *)

    (* 2oo3 Redundant Discharge Process Temperature Triplet [deg C] *)
    rDischTemp_degC_A           : REAL := 142.80;   (* Channel A discharge temperature 4-wire RTD [deg C] *)
    rDischTemp_degC_B           : REAL := 142.80;   (* Channel B discharge temperature 4-wire RTD [deg C] *)
    rDischTemp_degC_C           : REAL := 142.80;   (* Channel C discharge temperature 4-wire RTD [deg C] *)

    (* 2oo3 Redundant Compressor Shaft Speed Pickups [rpm] *)
    rShaftSpeed_rpm_A           : REAL := 11250.0;  (* Channel A magnetic pulse eddy-current speed pickup [rpm] *)
    rShaftSpeed_rpm_B           : REAL := 11250.0;  (* Channel B magnetic pulse eddy-current speed pickup [rpm] *)
    rShaftSpeed_rpm_C           : REAL := 11250.0;  (* Channel C magnetic pulse eddy-current speed pickup [rpm] *)

    (* Dual-Redundant High-Frequency Acoustic / Casing Vibration Accelerometers [mm/s] *)
    rVibrationSuct_mms          : REAL := 1.85;     (* Suction casing aerodynamic vibration RMS velocity [mm/s] *)
    rVibrationDisch_mms         : REAL := 2.45;     (* Discharge casing aerodynamic vibration RMS velocity [mm/s] *)

    (* Gas Chromatograph Process Gas Compositional Telemetry *)
    rGasMolecularWeight_kgkmol  : REAL := 21.45;    (* Measured hydrocarbon mixture molecular weight [kg/kmol] *)
    rGasSpecificHeatRatio_k     : REAL := 1.285;    (* Isentropic exponent ratio k = Cp/Cv [-] *)
    rGasCompressibility_Z       : REAL := 0.942;    (* Average gas compressibility factor Z [-] *)

    (* Anti-Surge Valve Position Feedback & In-Flight Control *)
    rASV_PosFeedback_Pct        : REAL := 0.00;     (* Dual smart positioner LVDT stem position feedback [%] *)
    rInletGuideVanePos_deg      : REAL := 15.0;     (* Variable Inlet Guide Vane (IGV) angle [deg] *)
    rDownstreamHeaderPress_bar  : REAL := 72.50;    (* Downstream consumer process battery limit pressure [bar] *)

    (* Safety & Supervisory Commands *)
    bESD_EmergencyRecycleTrip   : BOOL := FALSE;    (* Hardwired SIS Emergency Shutdown / Full Recycle Command *)
    bStartSequencePermissive    : BOOL := TRUE;     (* Machine control permissive from DCS/Turbine governor *)
    bResetTripAlarms            : BOOL := FALSE;    (* Operator latching alarm reset push-button *)
    bEnable                     : BOOL := TRUE;     (* Master functional block execution enable *)
    tScanTime_s                 : REAL := 0.005;    (* Fast deterministic controller cycle period [s] (200 Hz task) *)
END_VAR
"""
    sections.append(s1)

    # -------------------------------------------------------------------------
    # SECTION 2: VAR_OUTPUT & VAR
    # -------------------------------------------------------------------------
    s2 = """VAR_OUTPUT
    (* ========================================================================================= *)
    (* ACTUATOR COMMANDS, PROCESS TELEMETRY & SYSTEM STATUS WORDS (STRONGLY TYPED PHYSICAL OUTPUTS) *)
    (* ========================================================================================= *)
    rASV_ValveCommand_Pct       : REAL := 0.00;     (* Anti-surge fast recycle valve opening demand [%] *)
    rASV_FastSolenoidTrip       : BOOL := FALSE;    (* SIS de-energize-to-trip fast dump solenoid valve *)
    rDynamicSurgeMargin_Pct     : REAL := 24.50;    (* Distance from active Surge Control Line (SCL) [%] *)
    rPolytropicHead_kJkg        : REAL := 168.50;   (* Calculated real-time polytropic head H_p [kJ/kg] *)
    rPolytropicEfficiency_Pct   : REAL := 78.40;    (* Estimated compressor stage polytropic efficiency [%] *)
    rReducedFlow_q_red          : REAL := 10.00;    (* Invariant reduced flow parameter q_red = dP / P_s [-] *)
    rReducedHead_h_red          : REAL := 1.854;    (* Invariant reduced head parameter h_red = (Pd/Ps)^sigma - 1 [-] *)
    rSurgeLimitFlow_q_sll       : REAL := 7.550;    (* Current calculated Surge Limit Line flow value [-] *)
    rSurgeControlFlow_q_scl     : REAL := 8.920;    (* Current calculated active Surge Control Line flow value [-] *)
    rDynamicAnticipationBias    : REAL := 0.000;    (* Derivative surge anticipation expansion bias [-] *)
    rMassFlowRate_kgs           : REAL := 42.85;    (* Reconstructed suction gas mass flow rate [kg/s] *)
    dwAntiSurgeStatusWord       : DWORD := 16#0000_0000; (* 32-bit packed operational and sequencing status word *)
    dwAntiSurgeAlarmWord_Pri    : DWORD := 16#0000_0000; (* 32-bit packed ISA-18.2 Priority 1 / Trip Alarms *)
    dwAntiSurgeAlarmWord_Sec    : DWORD := 16#0000_0000; (* 32-bit packed ISA-18.2 Priority 2 / Warning Alarms *)
    dwTMR_DiagnosticWord        : DWORD := 16#0000_0000; (* 32-bit packed 2oo3 sensor health & degradation status *)
    bSurgeAnticipationActive    : BOOL := FALSE;    (* Fast derivative surge avoidance algorithm triggered *)
    bValveTrackingFault         : BOOL := FALSE;    (* Discrepancy between ASV command and position feedback *)
    bCompressorInSurge          : BOOL := FALSE;    (* Aerodynamic stall / flow reversal detected *)
    bASV_FullyOpenConfirmed     : BOOL := FALSE;    (* Full recycle position verified by limit switch (> 95%) *)
    bMPC_Active                 : BOOL := FALSE;    (* Model Predictive Controller active & in regulation *)
    bGracefulDegradation        : BOOL := FALSE;    (* Fallback control active due to sensor degradation *)
END_VAR

VAR
    (* ========================================================================================= *)
    (* INTERNAL REGISTERS: MATRICES, 2oo3 TMR ENGINE, THERMODYNAMICS, MPC SOLVER & FSM           *)
    (* ========================================================================================= *)
    bFirstScanDone              : BOOL := FALSE;    (* Cold-start memory and matrix allocation flag *)

    (* ----------------------------------------------------------------------------------------- *)
    (* 1. COMPRESSOR GEOMETRIC & THERMODYNAMIC CHARACTERISTIC CONSTANTS                          *)
    (* ----------------------------------------------------------------------------------------- *)
    rUniversalGasConst_R        : REAL := 8.31446;  (* Universal gas constant [kJ/(kmol*K)] *)
    rOrificeConst_C             : REAL := 0.0485;   (* Flow nozzle discharge coefficient constant *)
    rCompressorInletArea_m2     : REAL := 0.2850;   (* Suction nozzle pipe cross-sectional area [m2] *)
    rImpellerTipDiameter_m      : REAL := 0.7250;   (* Final stage impeller outer tip diameter [m] *)
    rNominalPolytropicEff       : REAL := 0.8150;   (* Base stage polytropic aerodynamic efficiency [-] *)

    (* Invariant Surge Limit Line (SLL) Parabolic Curve Coefficients: q_sll = a0 + a1*h + a2*h^2 *)
    rSLL_Coeff_a0               : REAL := 2.4500;
    rSLL_Coeff_a1               : REAL := 2.8500;
    rSLL_Coeff_a2               : REAL := -0.1850;

    (* Safety Margin & Dynamic Anticipation Tuning Parameters *)
    rSafetyMargin_Base          : REAL := 0.1250;   (* Steady-state safety margin (12.5% above SLL) *)
    rDynamicBiasGain_Kd         : REAL := 0.6500;   (* Dynamic derivative anticipation gain [s] *)
    rDynamicBiasDecayRate       : REAL := 0.9650;   (* Exponential filter decay factor per cycle *)
    rMaxDynamicBias             : REAL := 0.2500;   (* Maximum allowable dynamic surge bias clamp *)

    (* Valve Actuation Dynamics (< 300 ms explosive open stroke) *)
    rASV_FullStrokeTime_s       : REAL := 0.2800;   (* Full stroke opening duration [s] *)
    rASV_MaxSlewOpen_Pct_s      : REAL := 450.0;    (* Maximum opening slew rate [%/s] *)
    rASV_MaxSlewClose_Pct_s     : REAL := 25.0;     (* Controlled slow closing slew rate [%/s] *)
    rDecelCushionThreshold_Pct  : REAL := 82.0;     (* Opening position threshold for pneumatic cushion [%] *)

    (* ----------------------------------------------------------------------------------------- *)
    (* 2. TRIPLE MODULAR REDUNDANCY (2oo3 TMR) FILTERING & REGISTRATION                          *)
    (* ----------------------------------------------------------------------------------------- *)
    rVoted_SuctFlow_dP_mbar     : REAL := 185.0;
    rVoted_SuctPress_bar        : REAL := 18.50;
    rVoted_DischPress_bar       : REAL := 74.20;
    rVoted_SuctTemp_degC        : REAL := 28.50;
    rVoted_DischTemp_degC       : REAL := 142.80;
    rVoted_ShaftSpeed_rpm       : REAL := 11250.0;

    (* Tolerance Deviation Limits *)
    rTol_Flow_dP_mbar           : REAL := 12.0;
    rTol_SuctPress_bar          : REAL := 0.85;
    rTol_DischPress_bar         : REAL := 2.80;
    rTol_SuctTemp_degC          : REAL := 2.50;
    rTol_DischTemp_degC         : REAL := 4.50;
    rTol_ShaftSpeed_rpm         : REAL := 85.0;

    (* Stuck-Sensor Frozen Telemetry Counters *)
    iStuck_dP_A   : INT := 0; iStuck_dP_B   : INT := 0; iStuck_dP_C   : INT := 0;
    iStuck_Ps_A   : INT := 0; iStuck_Ps_B   : INT := 0; iStuck_Ps_C   : INT := 0;
    iStuck_Pd_A   : INT := 0; iStuck_Pd_B   : INT := 0; iStuck_Pd_C   : INT := 0;
    iStuck_Ts_A   : INT := 0; iStuck_Ts_B   : INT := 0; iStuck_Ts_C   : INT := 0;
    iStuck_Td_A   : INT := 0; iStuck_Td_B   : INT := 0; iStuck_Td_C   : INT := 0;
    iStuck_Spd_A  : INT := 0; iStuck_Spd_B  : INT := 0; iStuck_Spd_C  : INT := 0;

    (* Previous Scan Values *)
    rPrev_dP_A    : REAL := 185.0; rPrev_dP_B    : REAL := 185.0; rPrev_dP_C    : REAL := 185.0;
    rPrev_Ps_A    : REAL := 18.50; rPrev_Ps_B    : REAL := 18.50; rPrev_Ps_C    : REAL := 18.50;
    rPrev_Pd_A    : REAL := 74.20; rPrev_Pd_B    : REAL := 74.20; rPrev_Pd_C    : REAL := 74.20;
    rPrev_Ts_A    : REAL := 28.50; rPrev_Ts_B    : REAL := 28.50; rPrev_Ts_C    : REAL := 28.50;
    rPrev_Td_A    : REAL := 142.8; rPrev_Td_B    : REAL := 142.8; rPrev_Td_C    : REAL := 142.8;
    rPrev_Spd_A   : REAL := 11250.0; rPrev_Spd_B : REAL := 11250.0; rPrev_Spd_C : REAL := 11250.0;

    (* Sensor Health Flags *)
    bHealth_dP_A  : BOOL := TRUE; bHealth_dP_B  : BOOL := TRUE; bHealth_dP_C  : BOOL := TRUE;
    bHealth_Ps_A  : BOOL := TRUE; bHealth_Ps_B  : BOOL := TRUE; bHealth_Ps_C  : BOOL := TRUE;
    bHealth_Pd_A  : BOOL := TRUE; bHealth_Pd_B  : BOOL := TRUE; bHealth_Pd_C  : BOOL := TRUE;
    bHealth_Ts_A  : BOOL := TRUE; bHealth_Ts_B  : BOOL := TRUE; bHealth_Ts_C  : BOOL := TRUE;
    bHealth_Td_A  : BOOL := TRUE; bHealth_Td_B  : BOOL := TRUE; bHealth_Td_C  : BOOL := TRUE;
    bHealth_Spd_A : BOOL := TRUE; bHealth_Spd_B : BOOL := TRUE; bHealth_Spd_C : BOOL := TRUE;

    (* Degraded Voting Indicators *)
    bDegraded_dP_1oo2  : BOOL := FALSE; bDegraded_dP_1oo1  : BOOL := FALSE;
    bDegraded_Ps_1oo2  : BOOL := FALSE; bDegraded_Ps_1oo1  : BOOL := FALSE;
    bDegraded_Pd_1oo2  : BOOL := FALSE; bDegraded_Pd_1oo1  : BOOL := FALSE;
    bDegraded_Ts_1oo2  : BOOL := FALSE; bDegraded_Ts_1oo1  : BOOL := FALSE;
    bDegraded_Td_1oo2  : BOOL := FALSE; bDegraded_Td_1oo1  : BOOL := FALSE;
    bDegraded_Spd_1oo2 : BOOL := FALSE; bDegraded_Spd_1oo1 : BOOL := FALSE;

    (* ----------------------------------------------------------------------------------------- *)
    (* 3. 8x8 STATE-SPACE MODEL & KALMAN OBSERVER ARRAYS                                         *)
    (* ----------------------------------------------------------------------------------------- *)
    (* State Vector x[0..7]:
         x[0]: Suction mass flow rate deviation Delta m_dot_s [kg/s]
         x[1]: Discharge pressure deviation Delta P_d [bar]
         x[2]: Compressor rotor shaft speed deviation Delta N [rpm]
         x[3]: Discharge gas temperature deviation Delta T_d [deg C]
         x[4]: Anti-surge recycle mass flow rate Delta m_dot_rec [kg/s]
         x[5]: Recycle valve stem position Delta x_asv [%]
         x[6]: Gas molecular weight variation Delta M_w [kg/kmol]
         x[7]: Dynamic surge deviation margin Delta SS [-] *)
    aState_x                    : ARRAY[0..7] OF REAL := [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0];
    aState_x_hat                : ARRAY[0..7] OF REAL := [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0];
    aState_x_pred               : ARRAY[0..7] OF REAL := [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0];

    (* Control Vector u[0..3]:
         u[0]: ASV fast recycle valve demand [%] (0 to 100%)
         u[1]: Variable inlet guide vane (IGV) angle demand [deg] (-10 to +45 deg)
         u[2]: Driver speed governor setpoint demand [rpm] (8000 to 12500 rpm)
         u[3]: Hot gas bypass / interstage trim demand [%] (0 to 100%) *)
    aControl_u                  : ARRAY[0..3] OF REAL := [0.0, 15.0, 11250.0, 0.0];
    aControl_u_prev             : ARRAY[0..3] OF REAL := [0.0, 15.0, 11250.0, 0.0];
    aControl_du                 : ARRAY[0..3] OF REAL := [0.0, 0.0, 0.0, 0.0];

    (* Disturbance Vector d[0..2]:
         d[0]: Downstream process resistance fluctuation Delta R_down [bar/(kg/s)]
         d[1]: Hydrocarbon mixture molecular weight drift Delta M_w [kg/kmol]
         d[2]: Suction header pressure pulsation Delta P_suct [bar] *)
    aDisturb_d                  : ARRAY[0..2] OF REAL := [0.0, 0.0, 0.0];

    (* Controlled Measurement Vector y[0..3]:
         y[0]: Dynamic surge margin distance SS [%]
         y[1]: Discharge pressure P_d [bar]
         y[2]: Suction mass flow rate m_dot_s [kg/s]
         y[3]: ASV valve stem position feedback [%] *)
    aOutput_y                   : ARRAY[0..3] OF REAL := [24.50, 74.20, 42.85, 0.00];
    aOutput_y_sp                : ARRAY[0..3] OF REAL := [18.00, 74.20, 42.85, 0.00];
    aOutput_y_error             : ARRAY[0..3] OF REAL := [0.0, 0.0, 0.0, 0.0];

    (* Continuous-to-Discrete 8x8 State Transition Matrix A (Ts = 0.005 s) *)
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
    (* 4. MODEL PREDICTIVE CONTROL & FAST ANTI-SURGE CONTROLLER PARAMETERS                       *)
    (* ----------------------------------------------------------------------------------------- *)
    aWeight_Q                   : ARRAY[0..3] OF REAL := [280.0, 15.0, 12.0, 45.0]; (* Surge margin prioritized *)
    aWeight_R                   : ARRAY[0..3] OF REAL := [0.05, 0.85, 0.45, 0.15];   (* Low penalty on ASV opening *)
    aLimit_du_Max               : ARRAY[0..3] OF REAL := [25.0, 2.5, 45.0, 15.0];    (* Fast explosive opening allowed *)
    aLimit_du_Min               : ARRAY[0..3] OF REAL := [-1.2, -2.5, -45.0, -15.0]; (* Strict slow closing rate *)
    aLimit_u_Max                : ARRAY[0..3] OF REAL := [100.0, 45.0, 12500.0, 100.0];
    aLimit_u_Min                : ARRAY[0..3] OF REAL := [0.0, -10.0, 8000.0, 0.0];

    (* Projected Gradient Optimization Workspace *)
    aGrad_g                     : ARRAY[0..3] OF REAL;
    aHessian_diag               : ARRAY[0..3] OF REAL;
    aStep_du                    : ARRAY[0..3] OF REAL;
    iIterQP                     : INT := 0;
    iMaxIterQP                  : INT := 10;
    rAlphaStep                  : REAL := 0.042;

    (* Fallback Decoupled PID Anti-Surge Controller *)
    rPID_Kp_ASV                 : REAL := 3.850;
    rPID_Ki_ASV                 : REAL := 0.420;
    rPID_Kd_ASV                 : REAL := 0.125;
    rPID_Integ_ASV              : REAL := 0.0;
    rPID_PrevErr_ASV            : REAL := 0.0;

    (* ----------------------------------------------------------------------------------------- *)
    (* 5. FINITE STATE MACHINE (FSM) VARIABLES                                                   *)
    (* ----------------------------------------------------------------------------------------- *)
    (* Machine States:
         0  : STANDBY_PRESSURIZED            - Compressor pressurized, ASV 100% open, lube oil ready
         10 : SLOW_ROLL_PURGE                - Turning gear / low speed roll (800-1200 rpm)
         20 : ACCELERATION_THROUGH_CRITICAL  - Rapid acceleration through 1st/2nd critical speeds
         30 : ON_PROCESS_ANTISURGE_ACTIVE    - Min governing speed reached, ASV modulates, SLL active
         90 : EMERGENCY_FULL_RECYCLE         - Surge trip or ESD, explosive fast dump < 300 ms *)
    iFSM_State                  : INT := 0;
    iPreviousFSM_State          : INT := 0;
    rStateTimer_s               : REAL := 0.0;
    rAccelerationTimer_s        : REAL := 0.0;
    rPurgeTimer_s               : REAL := 0.0;

    (* ----------------------------------------------------------------------------------------- *)
    (* 6. INTERMEDIATE THERMODYNAMIC & AERODYNAMIC COMPUTATION REGISTERS                         *)
    (* ----------------------------------------------------------------------------------------- *)
    rPressureRatio              : REAL := 4.010;
    rPolytropicExponent_sigma   : REAL := 0.272;
    rSuctTemp_Kelvin            : REAL := 301.65;
    rDischTemp_Kelvin           : REAL := 415.95;
    rGasConstant_R_gas          : REAL := 0.3876;   (* [kJ/(kg*K)] *)
    rGasDensitySuct_kgm3        : REAL := 15.65;    (* [kg/m3] *)
    rPolytropicHeadCalc_m       : REAL := 17180.0;  (* [m] *)
    rDerivativeSurgeRate        : REAL := 0.00;     (* d(margin)/dt [s^-1] *)
    rPrevSurgeMargin            : REAL := 24.50;
    rFilterDerivativeMargin     : REAL := 0.00;
    rAcousticTransitTime_s      : REAL := 0.038;    (* Loop sonic wave transit delay [s] *)
    rSonicSpeedGas_ms           : REAL := 385.0;    (* [m/s] *)
    rRecyclePipeLength_m        : REAL := 14.5;     (* [m] *)
    rSurgeOscillationCount      : INT := 0;
    rSurgeCycleTimer_s          : REAL := 0.0;

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
(* SIS Hardwired Emergency Shutdown (ESD) Fast Recycle Interlock *)
IF bESD_EmergencyRecycleTrip THEN
    iFSM_State               := 90;                 (* Jump to EMERGENCY_FULL_RECYCLE *)
    rASV_ValveCommand_Pct    := 100.0;              (* Command ASV 100% full open immediately *)
    rASV_FastSolenoidTrip    := TRUE;               (* De-energize solenoid to dump actuator pressure *)
    bSurgeAnticipationActive := FALSE;
    bMPC_Active              := FALSE;
    dwAntiSurgeAlarmWord_Pri := dwAntiSurgeAlarmWord_Pri OR 16#8000_0000; (* Bit 31: ESD_RECYCLE_TRIP *)
END_IF;

(* Master Block Disabled *)
IF NOT bEnable THEN
    rASV_ValveCommand_Pct    := 100.0;              (* Default to full open safe position *)
    rASV_FastSolenoidTrip    := FALSE;
    bSurgeAnticipationActive := FALSE;
    bCompressorInSurge       := FALSE;
    bValveTrackingFault      := FALSE;
    bMPC_Active              := FALSE;
    bGracefulDegradation     := FALSE;
    dwAntiSurgeStatusWord    := 16#0000_0000;
    RETURN;
END_IF;

(* First-Scan State-Space Matrix Allocation *)
IF NOT bFirstScanDone THEN
    (* ------------------------------------------------------------------------------------- *)
    (* Discrete 8x8 Transition Matrix A (Ts = 0.005 s, 200 Hz Deterministic Loop)            *)
    (* Models multi-stage compressor aerodynamics, plenum compliance, and recycle loop delay  *)
    (* ------------------------------------------------------------------------------------- *)
    (* Row 0: Suction mass flow rate m_dot_s *)
    aMatrix_A[0,0] := 0.9850; aMatrix_A[0,1] := -0.0125; aMatrix_A[0,2] := 0.0018; aMatrix_A[0,3] := -0.0045;
    aMatrix_A[0,4] := 0.0450; aMatrix_A[0,5] := 0.0180;  aMatrix_A[0,6] := -0.0085; aMatrix_A[0,7] := 0.0000;

    (* Row 1: Discharge pressure P_d *)
    aMatrix_A[1,0] := 0.0245; aMatrix_A[1,1] := 0.9910;  aMatrix_A[1,2] := 0.0035; aMatrix_A[1,3] := 0.0012;
    aMatrix_A[1,4] := -0.0380; aMatrix_A[1,5] := -0.0145; aMatrix_A[1,6] := 0.0120; aMatrix_A[1,7] := 0.0000;

    (* Row 2: Rotor speed N *)
    aMatrix_A[2,0] := -0.1500; aMatrix_A[2,1] := -0.4500; aMatrix_A[2,2] := 0.9960; aMatrix_A[2,3] := -0.0250;
    aMatrix_A[2,4] := 0.0850;  aMatrix_A[2,5] := 0.0000;  aMatrix_A[2,6] := -0.0450; aMatrix_A[2,7] := 0.0000;

    (* Row 3: Discharge temperature T_d *)
    aMatrix_A[3,0] := -0.0180; aMatrix_A[3,1] := 0.0850;  aMatrix_A[3,2] := 0.0042; aMatrix_A[3,3] := 0.9820;
    aMatrix_A[3,4] := -0.0120; aMatrix_A[3,5] := 0.0000;  aMatrix_A[3,6] := 0.0350; aMatrix_A[3,7] := 0.0000;

    (* Row 4: Anti-surge recycle mass flow m_dot_rec *)
    aMatrix_A[4,0] := 0.0000; aMatrix_A[4,1] := 0.0250;  aMatrix_A[4,2] := 0.0000; aMatrix_A[4,3] := 0.0000;
    aMatrix_A[4,4] := 0.9250; aMatrix_A[4,5] := 0.1850;  aMatrix_A[4,6] := 0.0000; aMatrix_A[4,7] := 0.0000;

    (* Row 5: ASV stem position x_asv (< 300 ms fast dynamic) *)
    aMatrix_A[5,0] := 0.0000; aMatrix_A[5,1] := 0.0000;  aMatrix_A[5,2] := 0.0000; aMatrix_A[5,3] := 0.0000;
    aMatrix_A[5,4] := 0.0000; aMatrix_A[5,5] := 0.8800;  aMatrix_A[5,6] := 0.0000; aMatrix_A[5,7] := 0.0000;

    (* Row 6: Molecular weight variation M_w (slow mixing dynamic) *)
    aMatrix_A[6,0] := 0.0000; aMatrix_A[6,1] := 0.0000;  aMatrix_A[6,2] := 0.0000; aMatrix_A[6,3] := 0.0000;
    aMatrix_A[6,4] := 0.0000; aMatrix_A[6,5] := 0.0000;  aMatrix_A[6,6] := 0.9990; aMatrix_A[6,7] := 0.0000;

    (* Row 7: Dynamic surge margin SS *)
    aMatrix_A[7,0] := 0.4500; aMatrix_A[7,1] := -0.2200; aMatrix_A[7,2] := 0.0150; aMatrix_A[7,3] := -0.0080;
    aMatrix_A[7,4] := 0.5800; aMatrix_A[7,5] := 0.1200;  aMatrix_A[7,6] := -0.0450; aMatrix_A[7,7] := 0.9450;

    (* ------------------------------------------------------------------------------------- *)
    (* Discrete 8x4 Input Coupling Matrix B                                                  *)
    (* Inputs: u[0]=ASV [%], u[1]=IGV [deg], u[2]=Speed [rpm], u[3]=Trim [%]                 *)
    (* ------------------------------------------------------------------------------------- *)
    aMatrix_B[0,0] := 0.0145;  aMatrix_B[0,1] := 0.0085;  aMatrix_B[0,2] := 0.00045; aMatrix_B[0,3] := 0.0025;
    aMatrix_B[1,0] := -0.0185; aMatrix_B[1,1] := 0.0120;  aMatrix_B[1,2] := 0.00085; aMatrix_B[1,3] := -0.0040;
    aMatrix_B[2,0] := 0.0250;  aMatrix_B[2,1] := -0.0450; aMatrix_B[2,2] := 0.02450; aMatrix_B[2,3] := 0.0000;
    aMatrix_B[3,0] := -0.0050; aMatrix_B[3,1] := 0.0150;  aMatrix_B[3,2] := 0.00120; aMatrix_B[3,3] := 0.0180;
    aMatrix_B[4,0] := 0.2450;  aMatrix_B[4,1] := 0.0000;  aMatrix_B[4,2] := 0.00000; aMatrix_B[4,3] := 0.0850;
    aMatrix_B[5,0] := 0.1200;  aMatrix_B[5,1] := 0.0000;  aMatrix_B[5,2] := 0.00000; aMatrix_B[5,3] := 0.0000;
    aMatrix_B[6,0] := 0.0000;  aMatrix_B[6,1] := 0.0000;  aMatrix_B[6,2] := 0.00000; aMatrix_B[6,3] := 0.0000;
    aMatrix_B[7,0] := 0.1850;  aMatrix_B[7,1] := 0.0150;  aMatrix_B[7,2] := -0.0003; aMatrix_B[7,3] := 0.0250;

    (* ------------------------------------------------------------------------------------- *)
    (* Discrete 4x8 Output Mapping Matrix C                                                  *)
    (* ------------------------------------------------------------------------------------- *)
    aMatrix_C[0,0] := 0.0; aMatrix_C[0,1] := 0.0; aMatrix_C[0,2] := 0.0; aMatrix_C[0,3] := 0.0;
    aMatrix_C[0,4] := 0.0; aMatrix_C[0,5] := 0.0; aMatrix_C[0,6] := 0.0; aMatrix_C[0,7] := 1.0;

    aMatrix_C[1,0] := 0.0; aMatrix_C[1,1] := 1.0; aMatrix_C[1,2] := 0.0; aMatrix_C[1,3] := 0.0;
    aMatrix_C[1,4] := 0.0; aMatrix_C[1,5] := 0.0; aMatrix_C[1,6] := 0.0; aMatrix_C[1,7] := 0.0;

    aMatrix_C[2,0] := 1.0; aMatrix_C[2,1] := 0.0; aMatrix_C[2,2] := 0.0; aMatrix_C[2,3] := 0.0;
    aMatrix_C[2,4] := 0.0; aMatrix_C[2,5] := 0.0; aMatrix_C[2,6] := 0.0; aMatrix_C[2,7] := 0.0;

    aMatrix_C[3,0] := 0.0; aMatrix_C[3,1] := 0.0; aMatrix_C[3,2] := 0.0; aMatrix_C[3,3] := 0.0;
    aMatrix_C[3,4] := 0.0; aMatrix_C[3,5] := 1.0; aMatrix_C[3,6] := 0.0; aMatrix_C[3,7] := 0.0;

    (* Direct Feedthrough Matrix D (4x4) *)
    FOR iIdx := 0 TO 3 DO
        FOR jIdx := 0 TO 3 DO
            aMatrix_D[iIdx, jIdx] := 0.0;
        END_FOR;
    END_FOR;

    (* ------------------------------------------------------------------------------------- *)
    (* Disturbance Coupling Matrix E (8x3)                                                   *)
    (* ------------------------------------------------------------------------------------- *)
    aMatrix_E[0,0] := -0.0450; aMatrix_E[0,1] := -0.0120; aMatrix_E[0,2] := 0.0250;
    aMatrix_E[1,0] := 0.0850;  aMatrix_E[1,1] := 0.0150;  aMatrix_E[1,2] := 0.0450;
    aMatrix_E[2,0] := -0.2500; aMatrix_E[2,1] := -0.0850; aMatrix_E[2,2] := 0.0000;
    aMatrix_E[3,0] := 0.0350;  aMatrix_E[3,1] := 0.0450;  aMatrix_E[3,2] := 0.0120;
    aMatrix_E[4,0] := 0.0000;  aMatrix_E[4,1] := 0.0000;  aMatrix_E[4,2] := 0.0000;
    aMatrix_E[5,0] := 0.0000;  aMatrix_E[5,1] := 0.0000;  aMatrix_E[5,2] := 0.0000;
    aMatrix_E[6,0] := 0.0000;  aMatrix_E[6,1] := 0.1250;  aMatrix_E[6,2] := 0.0000;
    aMatrix_E[7,0] := -0.1850; aMatrix_E[7,1] := -0.0350; aMatrix_E[7,2] := 0.0850;

    (* ------------------------------------------------------------------------------------- *)
    (* Kalman / Luenberger Observer Gain Matrix L_obs (8x4)                                  *)
    (* ------------------------------------------------------------------------------------- *)
    aMatrix_L_obs[0,0] := 0.0850; aMatrix_L_obs[0,1] := 0.0045; aMatrix_L_obs[0,2] := 0.2450; aMatrix_L_obs[0,3] := 0.0000;
    aMatrix_L_obs[1,0] := -0.0450; aMatrix_L_obs[1,1] := 0.3150; aMatrix_L_obs[1,2] := 0.0120; aMatrix_L_obs[1,3] := 0.0000;
    aMatrix_L_obs[2,0] := 0.0000; aMatrix_L_obs[2,1] := 0.0850; aMatrix_L_obs[2,2] := -0.0150; aMatrix_L_obs[2,3] := 0.0000;
    aMatrix_L_obs[3,0] := 0.0000; aMatrix_L_obs[3,1] := 0.0450; aMatrix_L_obs[3,2] := -0.0080; aMatrix_L_obs[3,3] := 0.0000;
    aMatrix_L_obs[4,0] := 0.1200; aMatrix_L_obs[4,1] := 0.0000; aMatrix_L_obs[4,2] := 0.0450; aMatrix_L_obs[4,3] := 0.1850;
    aMatrix_L_obs[5,0] := 0.0000; aMatrix_L_obs[5,1] := 0.0000; aMatrix_L_obs[5,2] := 0.0000; aMatrix_L_obs[5,3] := 0.4500;
    aMatrix_L_obs[6,0] := -0.0150; aMatrix_L_obs[6,1] := 0.0180; aMatrix_L_obs[6,2] := 0.0000; aMatrix_L_obs[6,3] := 0.0000;
    aMatrix_L_obs[7,0] := 0.4200; aMatrix_L_obs[7,1] := -0.0250; aMatrix_L_obs[7,2] := 0.1500; aMatrix_L_obs[7,3] := 0.0250;

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
(* 1. Suction Orifice Differential Flow Pressure (rSuctFlow_dP_mbar_A, B, C)                     *)
(* --------------------------------------------------------------------------------------------- *)
IF ABS(rSuctFlow_dP_mbar_A - rPrev_dP_A) < 0.001 THEN iStuck_dP_A := iStuck_dP_A + 1; ELSE iStuck_dP_A := 0; END_IF;
IF ABS(rSuctFlow_dP_mbar_B - rPrev_dP_B) < 0.001 THEN iStuck_dP_B := iStuck_dP_B + 1; ELSE iStuck_dP_B := 0; END_IF;
IF ABS(rSuctFlow_dP_mbar_C - rPrev_dP_C) < 0.001 THEN iStuck_dP_C := iStuck_dP_C + 1; ELSE iStuck_dP_C := 0; END_IF;
rPrev_dP_A := rSuctFlow_dP_mbar_A; rPrev_dP_B := rSuctFlow_dP_mbar_B; rPrev_dP_C := rSuctFlow_dP_mbar_C;

bHealth_dP_A := (rSuctFlow_dP_mbar_A >= 0.0) AND (rSuctFlow_dP_mbar_A <= 500.0) AND (iStuck_dP_A < 300);
bHealth_dP_B := (rSuctFlow_dP_mbar_B >= 0.0) AND (rSuctFlow_dP_mbar_B <= 500.0) AND (iStuck_dP_B < 300);
bHealth_dP_C := (rSuctFlow_dP_mbar_C >= 0.0) AND (rSuctFlow_dP_mbar_C <= 500.0) AND (iStuck_dP_C < 300);

IF bHealth_dP_A AND bHealth_dP_B AND bHealth_dP_C THEN
    bDegraded_dP_1oo2 := FALSE; bDegraded_dP_1oo1 := FALSE;
    IF ((rSuctFlow_dP_mbar_A >= rSuctFlow_dP_mbar_B) AND (rSuctFlow_dP_mbar_A <= rSuctFlow_dP_mbar_C)) OR
       ((rSuctFlow_dP_mbar_A >= rSuctFlow_dP_mbar_C) AND (rSuctFlow_dP_mbar_A <= rSuctFlow_dP_mbar_B)) THEN
        rVoted_SuctFlow_dP_mbar := rSuctFlow_dP_mbar_A;
    ELSIF ((rSuctFlow_dP_mbar_B >= rSuctFlow_dP_mbar_A) AND (rSuctFlow_dP_mbar_B <= rSuctFlow_dP_mbar_C)) OR
          ((rSuctFlow_dP_mbar_B >= rSuctFlow_dP_mbar_C) AND (rSuctFlow_dP_mbar_B <= rSuctFlow_dP_mbar_A)) THEN
        rVoted_SuctFlow_dP_mbar := rSuctFlow_dP_mbar_B;
    ELSE
        rVoted_SuctFlow_dP_mbar := rSuctFlow_dP_mbar_C;
    END_IF;
    IF (ABS(rSuctFlow_dP_mbar_A - rSuctFlow_dP_mbar_B) > rTol_Flow_dP_mbar) OR
       (ABS(rSuctFlow_dP_mbar_B - rSuctFlow_dP_mbar_C) > rTol_Flow_dP_mbar) OR
       (ABS(rSuctFlow_dP_mbar_A - rSuctFlow_dP_mbar_C) > rTol_Flow_dP_mbar) THEN
        dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0001; (* Bit 0: Flow dP Discrepancy *)
    END_IF;
ELSIF bHealth_dP_A AND bHealth_dP_B THEN
    bDegraded_dP_1oo2 := TRUE; rVoted_SuctFlow_dP_mbar := (rSuctFlow_dP_mbar_A + rSuctFlow_dP_mbar_B) * 0.5;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0002;
ELSIF bHealth_dP_A AND bHealth_dP_C THEN
    bDegraded_dP_1oo2 := TRUE; rVoted_SuctFlow_dP_mbar := (rSuctFlow_dP_mbar_A + rSuctFlow_dP_mbar_C) * 0.5;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0002;
ELSIF bHealth_dP_B AND bHealth_dP_C THEN
    bDegraded_dP_1oo2 := TRUE; rVoted_SuctFlow_dP_mbar := (rSuctFlow_dP_mbar_B + rSuctFlow_dP_mbar_C) * 0.5;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0002;
ELSIF bHealth_dP_A THEN
    bDegraded_dP_1oo1 := TRUE; rVoted_SuctFlow_dP_mbar := rSuctFlow_dP_mbar_A;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0004;
ELSIF bHealth_dP_B THEN
    bDegraded_dP_1oo1 := TRUE; rVoted_SuctFlow_dP_mbar := rSuctFlow_dP_mbar_B;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0004;
ELSIF bHealth_dP_C THEN
    bDegraded_dP_1oo1 := TRUE; rVoted_SuctFlow_dP_mbar := rSuctFlow_dP_mbar_C;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0004;
ELSE
    rVoted_SuctFlow_dP_mbar := 0.0;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0008; (* Critical Flow Transmitter Failure *)
    bGracefulDegradation := TRUE;
END_IF;

(* --------------------------------------------------------------------------------------------- *)
(* 2. Suction Pressure Transmitters (rSuctPress_bar_A, B, C)                                     *)
(* --------------------------------------------------------------------------------------------- *)
IF ABS(rSuctPress_bar_A - rPrev_Ps_A) < 0.001 THEN iStuck_Ps_A := iStuck_Ps_A + 1; ELSE iStuck_Ps_A := 0; END_IF;
IF ABS(rSuctPress_bar_B - rPrev_Ps_B) < 0.001 THEN iStuck_Ps_B := iStuck_Ps_B + 1; ELSE iStuck_Ps_B := 0; END_IF;
IF ABS(rSuctPress_bar_C - rPrev_Ps_C) < 0.001 THEN iStuck_Ps_C := iStuck_Ps_C + 1; ELSE iStuck_Ps_C := 0; END_IF;
rPrev_Ps_A := rSuctPress_bar_A; rPrev_Ps_B := rSuctPress_bar_B; rPrev_Ps_C := rSuctPress_bar_C;

bHealth_Ps_A := (rSuctPress_bar_A >= 1.0) AND (rSuctPress_bar_A <= 50.0) AND (iStuck_Ps_A < 300);
bHealth_Ps_B := (rSuctPress_bar_B >= 1.0) AND (rSuctPress_bar_B <= 50.0) AND (iStuck_Ps_B < 300);
bHealth_Ps_C := (rSuctPress_bar_C >= 1.0) AND (rSuctPress_bar_C <= 50.0) AND (iStuck_Ps_C < 300);

IF bHealth_Ps_A AND bHealth_Ps_B AND bHealth_Ps_C THEN
    bDegraded_Ps_1oo2 := FALSE; bDegraded_Ps_1oo1 := FALSE;
    IF ((rSuctPress_bar_A >= rSuctPress_bar_B) AND (rSuctPress_bar_A <= rSuctPress_bar_C)) OR
       ((rSuctPress_bar_A >= rSuctPress_bar_C) AND (rSuctPress_bar_A <= rSuctPress_bar_B)) THEN
        rVoted_SuctPress_bar := rSuctPress_bar_A;
    ELSIF ((rSuctPress_bar_B >= rSuctPress_bar_A) AND (rSuctPress_bar_B <= rSuctPress_bar_C)) OR
          ((rSuctPress_bar_B >= rSuctPress_bar_C) AND (rSuctPress_bar_B <= rSuctPress_bar_A)) THEN
        rVoted_SuctPress_bar := rSuctPress_bar_B;
    ELSE
        rVoted_SuctPress_bar := rSuctPress_bar_C;
    END_IF;
    IF (ABS(rSuctPress_bar_A - rSuctPress_bar_B) > rTol_SuctPress_bar) OR
       (ABS(rSuctPress_bar_B - rSuctPress_bar_C) > rTol_SuctPress_bar) OR
       (ABS(rSuctPress_bar_A - rSuctPress_bar_C) > rTol_SuctPress_bar) THEN
        dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0010;
    END_IF;
ELSIF bHealth_Ps_A AND bHealth_Ps_B THEN
    bDegraded_Ps_1oo2 := TRUE; rVoted_SuctPress_bar := (rSuctPress_bar_A + rSuctPress_bar_B) * 0.5;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0020;
ELSIF bHealth_Ps_A AND bHealth_Ps_C THEN
    bDegraded_Ps_1oo2 := TRUE; rVoted_SuctPress_bar := (rSuctPress_bar_A + rSuctPress_bar_C) * 0.5;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0020;
ELSIF bHealth_Ps_B AND bHealth_Ps_C THEN
    bDegraded_Ps_1oo2 := TRUE; rVoted_SuctPress_bar := (rSuctPress_bar_B + rSuctPress_bar_C) * 0.5;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0020;
ELSIF bHealth_Ps_A THEN
    bDegraded_Ps_1oo1 := TRUE; rVoted_SuctPress_bar := rSuctPress_bar_A;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0040;
ELSIF bHealth_Ps_B THEN
    bDegraded_Ps_1oo1 := TRUE; rVoted_SuctPress_bar := rSuctPress_bar_B;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0040;
ELSIF bHealth_Ps_C THEN
    bDegraded_Ps_1oo1 := TRUE; rVoted_SuctPress_bar := rSuctPress_bar_C;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0040;
ELSE
    rVoted_SuctPress_bar := 1.0;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0080;
    bGracefulDegradation := TRUE;
END_IF;

(* --------------------------------------------------------------------------------------------- *)
(* 3. Discharge Pressure Transmitters (rDischPress_bar_A, B, C)                                  *)
(* --------------------------------------------------------------------------------------------- *)
IF ABS(rDischPress_bar_A - rPrev_Pd_A) < 0.001 THEN iStuck_Pd_A := iStuck_Pd_A + 1; ELSE iStuck_Pd_A := 0; END_IF;
IF ABS(rDischPress_bar_B - rPrev_Pd_B) < 0.001 THEN iStuck_Pd_B := iStuck_Pd_B + 1; ELSE iStuck_Pd_B := 0; END_IF;
IF ABS(rDischPress_bar_C - rPrev_Pd_C) < 0.001 THEN iStuck_Pd_C := iStuck_Pd_C + 1; ELSE iStuck_Pd_C := 0; END_IF;
rPrev_Pd_A := rDischPress_bar_A; rPrev_Pd_B := rDischPress_bar_B; rPrev_Pd_C := rDischPress_bar_C;

bHealth_Pd_A := (rDischPress_bar_A >= 1.0) AND (rDischPress_bar_A <= 150.0) AND (iStuck_Pd_A < 300);
bHealth_Pd_B := (rDischPress_bar_B >= 1.0) AND (rDischPress_bar_B <= 150.0) AND (iStuck_Pd_B < 300);
bHealth_Pd_C := (rDischPress_bar_C >= 1.0) AND (rDischPress_bar_C <= 150.0) AND (iStuck_Pd_C < 300);

IF bHealth_Pd_A AND bHealth_Pd_B AND bHealth_Pd_C THEN
    bDegraded_Pd_1oo2 := FALSE; bDegraded_Pd_1oo1 := FALSE;
    IF ((rDischPress_bar_A >= rDischPress_bar_B) AND (rDischPress_bar_A <= rDischPress_bar_C)) OR
       ((rDischPress_bar_A >= rDischPress_bar_C) AND (rDischPress_bar_A <= rDischPress_bar_B)) THEN
        rVoted_DischPress_bar := rDischPress_bar_A;
    ELSIF ((rDischPress_bar_B >= rDischPress_bar_A) AND (rDischPress_bar_B <= rDischPress_bar_C)) OR
          ((rDischPress_bar_B >= rDischPress_bar_C) AND (rDischPress_bar_B <= rDischPress_bar_A)) THEN
        rVoted_DischPress_bar := rDischPress_bar_B;
    ELSE
        rVoted_DischPress_bar := rDischPress_bar_C;
    END_IF;
    IF (ABS(rDischPress_bar_A - rDischPress_bar_B) > rTol_DischPress_bar) OR
       (ABS(rDischPress_bar_B - rDischPress_bar_C) > rTol_DischPress_bar) OR
       (ABS(rDischPress_bar_A - rDischPress_bar_C) > rTol_DischPress_bar) THEN
        dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0100;
    END_IF;
ELSIF bHealth_Pd_A AND bHealth_Pd_B THEN
    bDegraded_Pd_1oo2 := TRUE; rVoted_DischPress_bar := (rDischPress_bar_A + rDischPress_bar_B) * 0.5;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0200;
ELSIF bHealth_Pd_A AND bHealth_Pd_C THEN
    bDegraded_Pd_1oo2 := TRUE; rVoted_DischPress_bar := (rDischPress_bar_A + rDischPress_bar_C) * 0.5;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0200;
ELSIF bHealth_Pd_B AND bHealth_Pd_C THEN
    bDegraded_Pd_1oo2 := TRUE; rVoted_DischPress_bar := (rDischPress_bar_B + rDischPress_bar_C) * 0.5;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0200;
ELSIF bHealth_Pd_A THEN
    bDegraded_Pd_1oo1 := TRUE; rVoted_DischPress_bar := rDischPress_bar_A;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0400;
ELSIF bHealth_Pd_B THEN
    bDegraded_Pd_1oo1 := TRUE; rVoted_DischPress_bar := rDischPress_bar_B;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0400;
ELSIF bHealth_Pd_C THEN
    bDegraded_Pd_1oo1 := TRUE; rVoted_DischPress_bar := rDischPress_bar_C;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0400;
ELSE
    rVoted_DischPress_bar := 100.0;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0800;
    bGracefulDegradation := TRUE;
END_IF;

(* --------------------------------------------------------------------------------------------- *)
(* 4. Suction & Discharge Temperature Voting (2oo3)                                              *)
(* --------------------------------------------------------------------------------------------- *)
bHealth_Ts_A := (rSuctTemp_degC_A >= -50.0) AND (rSuctTemp_degC_A <= 120.0);
bHealth_Ts_B := (rSuctTemp_degC_B >= -50.0) AND (rSuctTemp_degC_B <= 120.0);
bHealth_Ts_C := (rSuctTemp_degC_C >= -50.0) AND (rSuctTemp_degC_C <= 120.0);
IF bHealth_Ts_A AND bHealth_Ts_B AND bHealth_Ts_C THEN
    IF ((rSuctTemp_degC_A >= rSuctTemp_degC_B) AND (rSuctTemp_degC_A <= rSuctTemp_degC_C)) OR
       ((rSuctTemp_degC_A >= rSuctTemp_degC_C) AND (rSuctTemp_degC_A <= rSuctTemp_degC_B)) THEN
        rVoted_SuctTemp_degC := rSuctTemp_degC_A;
    ELSIF ((rSuctTemp_degC_B >= rSuctTemp_degC_A) AND (rSuctTemp_degC_B <= rSuctTemp_degC_C)) OR
          ((rSuctTemp_degC_B >= rSuctTemp_degC_C) AND (rSuctTemp_degC_B <= rSuctTemp_degC_A)) THEN
        rVoted_SuctTemp_degC := rSuctTemp_degC_B;
    ELSE
        rVoted_SuctTemp_degC := rSuctTemp_degC_C;
    END_IF;
ELSE
    rVoted_SuctTemp_degC := rSuctTemp_degC_A;
END_IF;

bHealth_Td_A := (rDischTemp_degC_A >= 0.0) AND (rDischTemp_degC_A <= 260.0);
bHealth_Td_B := (rDischTemp_degC_B >= 0.0) AND (rDischTemp_degC_B <= 260.0);
bHealth_Td_C := (rDischTemp_degC_C >= 0.0) AND (rDischTemp_degC_C <= 260.0);
IF bHealth_Td_A AND bHealth_Td_B AND bHealth_Td_C THEN
    IF ((rDischTemp_degC_A >= rDischTemp_degC_B) AND (rDischTemp_degC_A <= rDischTemp_degC_C)) OR
       ((rDischTemp_degC_A >= rDischTemp_degC_C) AND (rDischTemp_degC_A <= rDischTemp_degC_B)) THEN
        rVoted_DischTemp_degC := rDischTemp_degC_A;
    ELSIF ((rDischTemp_degC_B >= rDischTemp_degC_A) AND (rDischTemp_degC_B <= rDischTemp_degC_C)) OR
          ((rDischTemp_degC_B >= rDischTemp_degC_C) AND (rDischTemp_degC_B <= rDischTemp_degC_A)) THEN
        rVoted_DischTemp_degC := rDischTemp_degC_B;
    ELSE
        rVoted_DischTemp_degC := rDischTemp_degC_C;
    END_IF;
ELSE
    rVoted_DischTemp_degC := rDischTemp_degC_A;
END_IF;

(* --------------------------------------------------------------------------------------------- *)
(* 5. Compressor Rotor Shaft Speed Voting (2oo3)                                                 *)
(* --------------------------------------------------------------------------------------------- *)
bHealth_Spd_A := (rShaftSpeed_rpm_A >= 0.0) AND (rShaftSpeed_rpm_A <= 16000.0);
bHealth_Spd_B := (rShaftSpeed_rpm_B >= 0.0) AND (rShaftSpeed_rpm_B <= 16000.0);
bHealth_Spd_C := (rShaftSpeed_rpm_C >= 0.0) AND (rShaftSpeed_rpm_C <= 16000.0);
IF bHealth_Spd_A AND bHealth_Spd_B AND bHealth_Spd_C THEN
    IF ((rShaftSpeed_rpm_A >= rShaftSpeed_rpm_B) AND (rShaftSpeed_rpm_A <= rShaftSpeed_rpm_C)) OR
       ((rShaftSpeed_rpm_A >= rShaftSpeed_rpm_C) AND (rShaftSpeed_rpm_A <= rShaftSpeed_rpm_B)) THEN
        rVoted_ShaftSpeed_rpm := rShaftSpeed_rpm_A;
    ELSIF ((rShaftSpeed_rpm_B >= rShaftSpeed_rpm_A) AND (rShaftSpeed_rpm_B <= rShaftSpeed_rpm_C)) OR
          ((rShaftSpeed_rpm_B >= rShaftSpeed_rpm_C) AND (rShaftSpeed_rpm_B <= rShaftSpeed_rpm_A)) THEN
        rVoted_ShaftSpeed_rpm := rShaftSpeed_rpm_B;
    ELSE
        rVoted_ShaftSpeed_rpm := rShaftSpeed_rpm_C;
    END_IF;
ELSE
    rVoted_ShaftSpeed_rpm := rShaftSpeed_rpm_A;
END_IF;
"""
    sections.append(s4)

    # -------------------------------------------------------------------------
    # SECTION 5: LOGIC PART 3 - POLYTROPIC HEAD & DYNAMIC SURGE LINE
    # -------------------------------------------------------------------------
    s5 = """(* ============================================================================================= *)
(* SECTION 3: INVARIANT THERMODYNAMICS, POLYTROPIC HEAD & DYNAMIC SURGE LIMIT OBSERVER           *)
(* ============================================================================================= *)
(* Absolute Temperature Conversions *)
rSuctTemp_Kelvin  := rVoted_SuctTemp_degC + 273.15;
rDischTemp_Kelvin := rVoted_DischTemp_degC + 273.15;

(* Pressure Ratio Pi = P_d / P_s *)
IF rVoted_SuctPress_bar > 0.50 THEN
    rPressureRatio := rVoted_DischPress_bar / rVoted_SuctPress_bar;
ELSE
    rPressureRatio := 1.0;
END_IF;
IF rPressureRatio < 1.0 THEN rPressureRatio := 1.0; END_IF;

(* Specific Gas Constant R_gas = R_univ / M_w [kJ/(kg*K)] *)
IF rGasMolecularWeight_kgkmol > 2.0 THEN
    rGasConstant_R_gas := rUniversalGasConst_R / rGasMolecularWeight_kgkmol;
ELSE
    rGasConstant_R_gas := 0.287;
END_IF;

(* Gas Density at Suction Conditions: rho = (P_s * 100) / (Z * R_gas * T_s) [kg/m3] *)
IF (rGasCompressibility_Z > 0.1) AND (rSuctTemp_Kelvin > 100.0) THEN
    rGasDensitySuct_kgm3 := (rVoted_SuctPress_bar * 100.0) / (rGasCompressibility_Z * rGasConstant_R_gas * rSuctTemp_Kelvin);
ELSE
    rGasDensitySuct_kgm3 := 1.20;
END_IF;

(* Suction Mass Flow Rate: m_dot = C_orifice * sqrt(2 * rho * dP) * Area *)
IF (rVoted_SuctFlow_dP_mbar > 0.0) AND (rGasDensitySuct_kgm3 > 0.0) THEN
    rMassFlowRate_kgs := rOrificeConst_C * SQRT(2.0 * rGasDensitySuct_kgm3 * (rVoted_SuctFlow_dP_mbar * 100.0)) * rCompressorInletArea_m2 * 25.0;
ELSE
    rMassFlowRate_kgs := 0.0;
END_IF;

(* Polytropic Temperature Exponent sigma = ln(T_d / T_s) / ln(P_d / P_s) *)
IF (rPressureRatio > 1.05) AND (rDischTemp_Kelvin > rSuctTemp_Kelvin) THEN
    rPolytropicExponent_sigma := (LN(rDischTemp_Kelvin) - LN(rSuctTemp_Kelvin)) / LN(rPressureRatio);
    IF rPolytropicExponent_sigma < 0.10 THEN rPolytropicExponent_sigma := 0.10; END_IF;
    IF rPolytropicExponent_sigma > 0.45 THEN rPolytropicExponent_sigma := 0.45; END_IF;
ELSE
    rPolytropicExponent_sigma := (rGasSpecificHeatRatio_k - 1.0) / (rGasSpecificHeatRatio_k * rNominalPolytropicEff);
END_IF;

(* ASME PTC 10 Polytropic Head: H_p = (Z * R_gas * T_s / sigma) * [ (P_d/P_s)^sigma - 1 ] [kJ/kg] *)
rPolytropicHead_kJkg := (rGasCompressibility_Z * rGasConstant_R_gas * rSuctTemp_Kelvin / rPolytropicExponent_sigma) *
                        (EXPT(rPressureRatio, rPolytropicExponent_sigma) - 1.0);

(* Polytropic Aerodynamic Efficiency eta_p = [(k-1)/k] / sigma *)
IF (rGasSpecificHeatRatio_k > 1.01) AND (rPolytropicExponent_sigma > 0.05) THEN
    rPolytropicEfficiency_Pct := (((rGasSpecificHeatRatio_k - 1.0) / rGasSpecificHeatRatio_k) / rPolytropicExponent_sigma) * 100.0;
    IF rPolytropicEfficiency_Pct > 95.0 THEN rPolytropicEfficiency_Pct := 95.0; END_IF;
    IF rPolytropicEfficiency_Pct < 40.0 THEN rPolytropicEfficiency_Pct := 40.0; END_IF;
ELSE
    rPolytropicEfficiency_Pct := 78.0;
END_IF;

(* Invariant Reduced Coordinates *)
(* Reduced Flow: q_red = dP_orifice / P_s *)
IF rVoted_SuctPress_bar > 0.50 THEN
    rReducedFlow_q_red := rVoted_SuctFlow_dP_mbar / rVoted_SuctPress_bar;
ELSE
    rReducedFlow_q_red := 0.0;
END_IF;

(* Reduced Head: h_red = (P_d / P_s)^sigma - 1.0 *)
rReducedHead_h_red := EXPT(rPressureRatio, rPolytropicExponent_sigma) - 1.0;
IF rReducedHead_h_red < 0.0 THEN rReducedHead_h_red := 0.0; END_IF;

(* Invariant Surge Limit Line (SLL): q_sll = a0 + a1 * h_red + a2 * h_red^2 *)
rSurgeLimitFlow_q_sll := rSLL_Coeff_a0 + rSLL_Coeff_a1 * rReducedHead_h_red + rSLL_Coeff_a2 * (rReducedHead_h_red * rReducedHead_h_red);
IF rSurgeLimitFlow_q_sll < 0.50 THEN rSurgeLimitFlow_q_sll := 0.50; END_IF;

(* Base Surge Control Line (SCL): q_scl = q_sll * (1.0 + k_margin) *)
rSurgeControlFlow_q_scl := rSurgeLimitFlow_q_sll * (1.0 + rSafetyMargin_Base);

(* Dynamic Surge Anticipation Derivative Vector *)
(* Rate of approach toward surge: d(margin)/dt *)
rDerivativeSurgeRate := (rDynamicSurgeMargin_Pct - rPrevSurgeMargin) / tScanTime_s;
rPrevSurgeMargin     := rDynamicSurgeMargin_Pct;

(* Filter derivative to eliminate transducer high-frequency noise *)
rFilterDerivativeMargin := 0.82 * rFilterDerivativeMargin + 0.18 * rDerivativeSurgeRate;

(* If operating point is rapidly rushing toward surge (negative derivative) *)
IF rFilterDerivativeMargin < -12.0 THEN
    bSurgeAnticipationActive := TRUE;
    (* Nonlinear dynamic bias expansion: b_dyn = Kd * |d(margin)/dt|^1.25 *)
    rDynamicAnticipationBias := rDynamicAnticipationBias + rDynamicBiasGain_Kd * EXPT(ABS(rFilterDerivativeMargin) * 0.01, 1.25);
    IF rDynamicAnticipationBias > rMaxDynamicBias THEN
        rDynamicAnticipationBias := rMaxDynamicBias;
    END_IF;
    dwAntiSurgeAlarmWord_Sec := dwAntiSurgeAlarmWord_Sec OR 16#0000_0001; (* Bit 0: SURGE_ANTICIPATION_ACTIVE *)
ELSE
    (* Smooth exponential decay of dynamic bias when trajectory stabilizes *)
    rDynamicAnticipationBias := rDynamicAnticipationBias * rDynamicBiasDecayRate;
    IF rDynamicAnticipationBias < 0.001 THEN
        rDynamicAnticipationBias := 0.0;
        bSurgeAnticipationActive := FALSE;
    END_IF;
END_IF;

(* Active Surge Control Line with Dynamic Anticipation *)
rSurgeControlFlow_q_scl := rSurgeControlFlow_q_scl + rDynamicAnticipationBias * rSurgeLimitFlow_q_sll;

(* Dynamic Surge Margin Distance: SS = (q_red - q_sll) / q_red * 100% *)
IF rReducedFlow_q_red > 0.01 THEN
    rDynamicSurgeMargin_Pct := ((rReducedFlow_q_red - rSurgeLimitFlow_q_sll) / rReducedFlow_q_red) * 100.0;
ELSE
    rDynamicSurgeMargin_Pct := -100.0;
END_IF;

(* Surge Detection (Operating Point Beyond SLL or High Acoustic Casing Vibration) *)
IF (rDynamicSurgeMargin_Pct <= 0.0) OR (rVibrationDisch_mms >= 9.50) THEN
    bCompressorInSurge       := TRUE;
    rSurgeOscillationCount   := rSurgeOscillationCount + 1;
    dwAntiSurgeAlarmWord_Pri := dwAntiSurgeAlarmWord_Pri OR 16#0000_0002; (* Bit 1: SURGE_THRESHOLD_VIOLATED_HH *)
ELSE
    IF rSurgeOscillationCount > 0 THEN
        rSurgeCycleTimer_s := rSurgeCycleTimer_s + tScanTime_s;
        IF rSurgeCycleTimer_s >= 5.0 THEN
            bCompressorInSurge     := FALSE;
            rSurgeOscillationCount := 0;
            rSurgeCycleTimer_s     := 0.0;
        END_IF;
    END_IF;
END_IF;
"""
    sections.append(s5)

    # -------------------------------------------------------------------------
    # SECTION 6: LOGIC PART 4 - 8x8 STATE-SPACE PREDICTION & KALMAN OBSERVER
    # -------------------------------------------------------------------------
    s6 = """(* ============================================================================================= *)
(* SECTION 4: 8x8 DISCRETE STATE-SPACE TIME PROPAGATION & KALMAN OBSERVER UPDATE                 *)
(* ============================================================================================= *)
(* Map Physical Disturbances into Vector d *)
aDisturb_d[0] := (rDownstreamHeaderPress_bar - 72.50) / 10.0;
aDisturb_d[1] := rGasMolecularWeight_kgkmol - 21.45;
aDisturb_d[2] := rVoted_SuctPress_bar - 18.50;

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

(* Measured Outputs y_meas *)
aOutput_y[0] := rDynamicSurgeMargin_Pct;
aOutput_y[1] := rVoted_DischPress_bar;
aOutput_y[2] := rMassFlowRate_kgs;
aOutput_y[3] := rASV_PosFeedback_Pct;

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
    # SECTION 7: LOGIC PART 5 - MPC & FAST ANTI-SURGE CONTROLLER
    # -------------------------------------------------------------------------
    s7 = """(* ============================================================================================= *)
(* SECTION 5: MODEL PREDICTIVE CONTROL & HIGH-SPEED ASV OPTIMIZATION                             *)
(* ============================================================================================= *)
(* Target Surge Margin Setpoint (Maintain minimum 15% distance from SLL) *)
aOutput_y_sp[0] := 18.0;                    (* Target 18% surge margin *)
aOutput_y_sp[1] := 74.20;                   (* Discharge pressure setpoint *)
aOutput_y_sp[2] := 42.85;                   (* Mass flow target *)
aOutput_y_sp[3] := 0.00;                    (* ASV fully closed target during normal operation *)

(* Tracking Error Calculation *)
aOutput_y_error[0] := aOutput_y_sp[0] - aOutput_y[0]; (* Positive error means we are TOO CLOSE to surge! *)
aOutput_y_error[1] := aOutput_y[1] - aOutput_y_sp[1];
aOutput_y_error[2] := aOutput_y[2] - aOutput_y_sp[2];
aOutput_y_error[3] := aOutput_y[3] - aOutput_y_sp[3];

IF NOT bGracefulDegradation AND (iFSM_State = 30) THEN
    bMPC_Active := TRUE;

    (* Approximate Diagonal Hessian *)
    aHessian_diag[0] := aWeight_Q[0] * 0.034 + aWeight_R[0]; (* ASV valve move *)
    aHessian_diag[1] := aWeight_Q[1] * 0.015 + aWeight_R[1]; (* IGV guide vane *)
    aHessian_diag[2] := aWeight_Q[2] * 0.0005 + aWeight_R[2]; (* Governor speed *)
    aHessian_diag[3] := aWeight_Q[3] * 0.010 + aWeight_R[3]; (* Hot bypass trim *)

    (* Gradient Calculation (Heavily penalizes encroachment on surge margin) *)
    aGrad_g[0] := -aWeight_Q[0] * aOutput_y_error[0] * 3.45 + aWeight_R[0] * aControl_du[0];
    aGrad_g[1] := -aWeight_Q[1] * aOutput_y_error[1] * 0.85 + aWeight_R[1] * aControl_du[1];
    aGrad_g[2] := -aWeight_Q[2] * aOutput_y_error[2] * 0.05 + aWeight_R[2] * aControl_du[2];
    aGrad_g[3] := -aWeight_Q[3] * aOutput_y_error[3] * 1.20 + aWeight_R[3] * aControl_du[3];

    (* Iterative Projected Gradient Descent *)
    FOR iIterQP := 1 TO iMaxIterQP DO
        FOR iIdx := 0 TO 3 DO
            aStep_du[iIdx] := aControl_du[iIdx] - (rAlphaStep / aHessian_diag[iIdx]) * aGrad_g[iIdx];

            (* Slew rate limits (Allows explosive opening up to 25% per scan, slow closing) *)
            IF aStep_du[iIdx] > aLimit_du_Max[iIdx] THEN
                aStep_du[iIdx] := aLimit_du_Max[iIdx];
            ELSIF aStep_du[iIdx] < aLimit_du_Min[iIdx] THEN
                aStep_du[iIdx] := aLimit_du_Min[iIdx];
            END_IF;

            (* Absolute position limits *)
            IF (aControl_u[iIdx] + aStep_du[iIdx]) > aLimit_u_Max[iIdx] THEN
                aStep_du[iIdx] := aLimit_u_Max[iIdx] - aControl_u[iIdx];
            ELSIF (aControl_u[iIdx] + aStep_du[iIdx]) < aLimit_u_Min[iIdx] THEN
                aStep_du[iIdx] := aLimit_u_Min[iIdx] - aControl_u[iIdx];
            END_IF;

            aControl_du[iIdx] := aStep_du[iIdx];
        END_FOR;
    END_FOR;

    (* Apply Incremental Moves *)
    aControl_u[0] := aControl_u[0] + aControl_du[0];
    aControl_u[1] := aControl_u[1] + aControl_du[1];
    aControl_u[2] := aControl_u[2] + aControl_du[2];
    aControl_u[3] := aControl_u[3] + aControl_du[3];

    rASV_ValveCommand_Pct := aControl_u[0];
ELSE
    (* Fallback Decoupled Anti-Surge Controller *)
    bMPC_Active := FALSE;

    (* Error: positive if operating point is below SCL *)
    rTmpSum := (rSurgeControlFlow_q_scl - rReducedFlow_q_red);
    IF rTmpSum > 0.0 THEN
        (* Fast Proportional + Integral opening response *)
        rPID_Integ_ASV := rPID_Integ_ASV + rTmpSum * tScanTime_s;
        IF rPID_Integ_ASV > 50.0 THEN rPID_Integ_ASV := 50.0; END_IF;

        rASV_ValveCommand_Pct := rPID_Kp_ASV * rTmpSum * 15.0 + rPID_Ki_ASV * rPID_Integ_ASV +
                                 rPID_Kd_ASV * ((rTmpSum - rPID_PrevErr_ASV) / tScanTime_s);
    ELSE
        (* Slow integral recovery decay to prevent valve hunting *)
        rPID_Integ_ASV := rPID_Integ_ASV * 0.995;
        rASV_ValveCommand_Pct := rPID_Integ_ASV;
    END_IF;
    rPID_PrevErr_ASV := rTmpSum;

    IF rASV_ValveCommand_Pct > 100.0 THEN rASV_ValveCommand_Pct := 100.0; END_IF;
    IF rASV_ValveCommand_Pct < 0.0 THEN rASV_ValveCommand_Pct := 0.0; END_IF;
END_IF;

(* High-Speed Valve Opening Cushion Deceleration *)
(* Near 82% to 100% stroke, apply softening cushion to prevent bonnet impact *)
IF rASV_ValveCommand_Pct >= rDecelCushionThreshold_Pct THEN
    (* Reduce slew acceleration to protect valve packing & internal cage *)
    dwAntiSurgeStatusWord := dwAntiSurgeStatusWord OR 16#0000_0008; (* Bit 3: CUSHION_RAMP_ACTIVE *)
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
    (* STATE 0: STANDBY_PRESSURIZED (Compressor Pressurized on Loop, Valve 100% Full Open)       *)
    (* ----------------------------------------------------------------------------------------- *)
    0:
        rASV_ValveCommand_Pct    := 100.0;          (* 100% full recycle to prevent startup surge *)
        rASV_FastSolenoidTrip    := FALSE;
        bSurgeAnticipationActive := FALSE;
        bCompressorInSurge       := FALSE;

        (* Advance to Slow Roll when start permissive granted and turbine turning gear engages *)
        IF bStartSequencePermissive AND (rVoted_ShaftSpeed_rpm >= 600.0) THEN
            iFSM_State := 10;
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 10: SLOW_ROLL_PURGE (Thermal Bow Soak & Low-Speed Purge at 800-1200 RPM)            *)
    (* ----------------------------------------------------------------------------------------- *)
    10:
        rASV_ValveCommand_Pct := 100.0;             (* Maintain 100% open *)
        rPurgeTimer_s         := rPurgeTimer_s + tScanTime_s;

        (* Hold for minimum thermal soak period (120 s) then accelerate *)
        IF (rPurgeTimer_s >= 120.0) AND (rVoted_ShaftSpeed_rpm >= 1800.0) THEN
            rPurgeTimer_s := 0.0;
            iFSM_State    := 20;                    (* Advance to critical speed pass *)
        END_IF;

        IF rVoted_ShaftSpeed_rpm < 400.0 THEN
            iFSM_State := 0;                        (* Rollback if speed lost *)
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 20: ACCELERATION_THROUGH_CRITICAL (Rapid Run-up Through Rotor 1st/2nd Bending Modes)*)
    (* ----------------------------------------------------------------------------------------- *)
    20:
        rASV_ValveCommand_Pct := 100.0;             (* Zero aerodynamic load on impellers *)
        rAccelerationTimer_s  := rAccelerationTimer_s + tScanTime_s;

        (* Once past second critical speed and minimum governing speed reached (> 8500 rpm) *)
        IF rVoted_ShaftSpeed_rpm >= 8500.0 THEN
            rAccelerationTimer_s := 0.0;
            iFSM_State           := 30;             (* Advance to active on-process anti-surge *)
        END_IF;

        (* Critical speed acceleration timeout protection (max 45 s to clear critical band) *)
        IF rAccelerationTimer_s >= 45.0 THEN
            dwAntiSurgeAlarmWord_Pri := dwAntiSurgeAlarmWord_Pri OR 16#0000_0004; (* CRITICAL_PASS_TIMEOUT *)
            iFSM_State               := 90;         (* Abort to full recycle *)
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 30: ON_PROCESS_ANTISURGE_ACTIVE (Normal Closed-Loop Modulation & Surge Protection)  *)
    (* ----------------------------------------------------------------------------------------- *)
    30:
        (* Normal closed-loop modulation driven by Section 5 MPC / Fallback Controller *)
        rASV_FastSolenoidTrip := FALSE;

        (* Emergency trip to full recycle if surge detected or ESD active *)
        IF bCompressorInSurge OR (rDynamicSurgeMargin_Pct <= 0.0) THEN
            iFSM_State := 90;
        END_IF;

        (* Driver speed loss drops back into critical runout *)
        IF rVoted_ShaftSpeed_rpm < 7800.0 THEN
            rASV_ValveCommand_Pct := 100.0;
            iFSM_State            := 10;
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 90: EMERGENCY_FULL_RECYCLE (Explosive Full Valve Opening < 300 ms, Trip Protection) *)
    (* ----------------------------------------------------------------------------------------- *)
    90:
        rASV_ValveCommand_Pct := 100.0;             (* 100% full recycle demand *)
        rASV_FastSolenoidTrip := TRUE;              (* De-energize solenoid to dump air instantaneously *)
        bSurgeAnticipationActive := FALSE;

        (* Reset when alarms acknowledged and operator clears trip *)
        IF bResetTripAlarms AND (NOT bCompressorInSurge) AND (NOT bESD_EmergencyRecycleTrip) THEN
            rASV_FastSolenoidTrip := FALSE;
            IF rVoted_ShaftSpeed_rpm >= 8500.0 THEN
                iFSM_State := 30;
            ELSE
                iFSM_State := 0;
            END_IF;
        END_IF;
END_CASE;

(* ASV Fully Open Limit Confirmation *)
bASV_FullyOpenConfirmed := (rASV_PosFeedback_Pct >= 95.0);

(* ASV Tracking Fault Detection (Discrepancy > 8.0% for > 0.400 s) *)
IF ABS(rASV_ValveCommand_Pct - rASV_PosFeedback_Pct) >= 8.0 THEN
    IF rStateTimer_s >= 0.400 THEN
        bValveTrackingFault      := TRUE;
        dwAntiSurgeAlarmWord_Pri := dwAntiSurgeAlarmWord_Pri OR 16#0000_0008; (* VALVE_TRACKING_DISAGREE_HH *)
    END_IF;
ELSE
    bValveTrackingFault := FALSE;
END_IF;
"""
    sections.append(s8)

    # -------------------------------------------------------------------------
    # SECTION 9: LOGIC PART 7 - ISA-18.2 ALARMS & DIAGNOSTIC PACKING
    # -------------------------------------------------------------------------
    s9 = """(* ============================================================================================= *)
(* SECTION 7: ISA-18.2 ALARM MATRIX, LATCHING & STATUS WORD BIT-PACKING                          *)
(* ============================================================================================= *)
(* 1. Distance From Surge Limit Line Alarms *)
IF rDynamicSurgeMargin_Pct <= 0.0 THEN
    dwAntiSurgeAlarmWord_Pri := dwAntiSurgeAlarmWord_Pri OR 16#0000_0010; (* Bit 4: SURGE_MARGIN_CRITICAL_LL *)
ELSIF rDynamicSurgeMargin_Pct <= 8.0 THEN
    dwAntiSurgeAlarmWord_Pri := dwAntiSurgeAlarmWord_Pri OR 16#0000_0020; (* Bit 5: SURGE_MARGIN_LOW_LOW_LL *)
ELSIF rDynamicSurgeMargin_Pct <= 14.0 THEN
    dwAntiSurgeAlarmWord_Sec := dwAntiSurgeAlarmWord_Sec OR 16#0000_0002; (* Bit 1: SURGE_MARGIN_LOW_L *)
END_IF;

(* 2. Casing Aerodynamic Vibration Alarms *)
IF rVibrationDisch_mms >= 9.50 THEN
    dwAntiSurgeAlarmWord_Pri := dwAntiSurgeAlarmWord_Pri OR 16#0000_0040; (* Bit 6: VIBRATION_DISCH_HH_TRIP *)
ELSIF rVibrationDisch_mms >= 6.50 THEN
    dwAntiSurgeAlarmWord_Sec := dwAntiSurgeAlarmWord_Sec OR 16#0000_0004; (* Bit 2: VIBRATION_DISCH_H_WARN *)
END_IF;

(* 3. Discharge Gas Overtemperature Alarms *)
IF rVoted_DischTemp_degC >= 185.0 THEN
    dwAntiSurgeAlarmWord_Pri := dwAntiSurgeAlarmWord_Pri OR 16#0000_0080; (* Bit 7: DISCH_TEMP_HH_TRIP *)
ELSIF rVoted_DischTemp_degC >= 165.0 THEN
    dwAntiSurgeAlarmWord_Sec := dwAntiSurgeAlarmWord_Sec OR 16#0000_0008; (* Bit 3: DISCH_TEMP_H_WARN *)
END_IF;

(* 4. Suction Pressure Low Alarms *)
IF rVoted_SuctPress_bar <= 8.50 THEN
    dwAntiSurgeAlarmWord_Sec := dwAntiSurgeAlarmWord_Sec OR 16#0000_0010; (* Bit 4: SUCT_PRESS_LOW_L *)
END_IF;

(* Alarm Reset Mechanism *)
IF bResetTripAlarms THEN
    dwAntiSurgeAlarmWord_Pri := 16#0000_0000;
    dwAntiSurgeAlarmWord_Sec := 16#0000_0000;
END_IF;

(* --------------------------------------------------------------------------------------------- *)
(* 5. 32-Bit System Status Word Packing (dwAntiSurgeStatusWord)                                  *)
(* --------------------------------------------------------------------------------------------- *)
(* Bits 0..7  : Current FSM State Integer [0..90] *)
(* Bit 8      : bSurgeAnticipationActive *)
(* Bit 9      : bCompressorInSurge *)
(* Bit 10     : bValveTrackingFault *)
(* Bit 11     : bASV_FullyOpenConfirmed *)
(* Bit 12     : bMPC_Active *)
(* Bit 13     : bGracefulDegradation *)
(* Bit 14     : rASV_FastSolenoidTrip *)
(* Bit 15     : bStartSequencePermissive *)
(* Bit 31     : Master Emergency Trip Flag *)
dwAntiSurgeStatusWord := INT_TO_DWORD(iFSM_State);
IF bSurgeAnticipationActive THEN dwAntiSurgeStatusWord := dwAntiSurgeStatusWord OR 16#0000_0100; END_IF;
IF bCompressorInSurge       THEN dwAntiSurgeStatusWord := dwAntiSurgeStatusWord OR 16#0000_0200; END_IF;
IF bValveTrackingFault      THEN dwAntiSurgeStatusWord := dwAntiSurgeStatusWord OR 16#0000_0400; END_IF;
IF bASV_FullyOpenConfirmed  THEN dwAntiSurgeStatusWord := dwAntiSurgeStatusWord OR 16#0000_0800; END_IF;
IF bMPC_Active              THEN dwAntiSurgeStatusWord := dwAntiSurgeStatusWord OR 16#0000_1000; END_IF;
IF bGracefulDegradation     THEN dwAntiSurgeStatusWord := dwAntiSurgeStatusWord OR 16#0000_2000; END_IF;
IF rASV_FastSolenoidTrip    THEN dwAntiSurgeStatusWord := dwAntiSurgeStatusWord OR 16#0000_4000; END_IF;
IF bStartSequencePermissive THEN dwAntiSurgeStatusWord := dwAntiSurgeStatusWord OR 16#0000_8000; END_IF;
IF (iFSM_State = 90)        THEN dwAntiSurgeStatusWord := dwAntiSurgeStatusWord OR 16#8000_0000; END_IF;

END_FUNCTION_BLOCK
"""
    sections.append(s9)

    return "".join(sections)

if __name__ == "__main__":
    code = build_antisurge_block()
    print(f"Total ST code length: {len(code)} characters")
