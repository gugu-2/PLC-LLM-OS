# ccgt_builder/st_var.py

def get_var_declarations():
    return """VAR
    (* =================================================================================================================
     * SECTION 3.1: FUNDAMENTAL CYCLE TIME, SIMULATION CONSTANTS & THERMODYNAMIC COEFFICIENTS
     * ================================================================================================================= *)
    rScan_Period_Ts                 : REAL := 0.020;      (* Real-Time Sampling Execution Period [s] (20.0 ms / 50 Hz) *)
    bInitialized                    : BOOL := FALSE;      (* Master First-Scan Cold Initialization Latch *)
    rGT_Rated_Base_Power_MW         : REAL := 250.0;      (* Gas Turbine Base Load ISO Electrical Capacity [MW] *)
    rCCGT_Total_Rated_Power_MW      : REAL := 350.0;      (* Combined Cycle Power Block Total Generating Capacity [MW] *)
    rNominal_Turbine_Speed_RPM      : REAL := 3000.0;     (* Rated Turbomachinery Synchronous Speed (50 Hz Grid) [rpm] *)
    rNominal_EGT_degC               : REAL := 620.0;      (* Base Load Combustor Exhaust Gas Temperature [deg C] *)
    rNominal_MainSteam_Temp_degC    : REAL := 565.0;      (* Superheater Final Outlet Main Steam Temperature [deg C] *)
    rNominal_MainSteam_Flow_kgs     : REAL := 180.0;      (* HP Superheater Rated Steam Mass Flow Rate [kg/s] *)
    rNominal_HP_Drum_Press_bar      : REAL := 125.0;      (* High-Pressure Evaporator Drum Operating Pressure [bar] *)
    rSpecific_Heat_ExhaustGas_Cp    : REAL := 1.150;      (* Combustion Flue Gas Specific Heat Capacity [kJ/(kg*K)] *)
    rSpecific_Heat_Steam_Cp         : REAL := 2.450;      (* Superheated HP Steam Specific Heat Capacity [kJ/(kg*K)] *)
    rSpecific_Heat_Water_Cp         : REAL := 4.280;      (* Subcooled Boiler Feedwater Specific Heat Capacity [kJ/(kg*K)] *)
    rEnthalpy_Evaporation_hfg       : REAL := 1150.0;     (* Latent Heat of Steam Evaporation at 125 bar [kJ/kg] *)

    (* =================================================================================================================
     * SECTION 3.2: DISCRETE STATE-SPACE MATRICES (8 STATES x 6 INPUTS x 6 OUTPUTS)
     * Discretized at Ts = 0.020 s (20 ms) from Continuous Governing Equations:
     *   x[1] = Gas Turbine Active Electrical Power Output [MW]
     *   x[2] = Combustor Exhaust Gas Temperature (EGT) [deg C]
     *   x[3] = Compressor Variable Guide Vane (VGV) Position [deg]
     *   x[4] = HRSG High-Pressure Drum Narrow-Range Water Level [mm] (shrink/swell dynamics)
     *   x[5] = HP Steam Header Mass Flow Rate [kg/s]
     *   x[6] = Final Superheater Main Steam Exit Temperature [deg C]
     *   x[7] = Attemperator Desuperheater Inter-Stage Temperature [deg C]
     *   x[8] = Boiler Feedwater Regulating Valve Effective Hydrodynamic Position [%]
     * ================================================================================================================= *)
    A_mat                           : ARRAY[1..8, 1..8] OF REAL; (* Discrete System Dynamics Matrix A (8x8) [-] *)
    B_mat                           : ARRAY[1..8, 1..6] OF REAL; (* Discrete Actuator/Disturbance Input Matrix B (8x6) [-] *)
    C_mat                           : ARRAY[1..6, 1..8] OF REAL; (* Discrete Observation Matrix C (6x8) [-] *)
    D_mat                           : ARRAY[1..6, 1..6] OF REAL; (* Discrete Direct Feedthrough Matrix D (6x6) [-] *)
    L_mat                           : ARRAY[1..8, 1..6] OF REAL; (* Discrete Kalman/Luenberger Innovation Observer Gain L (8x6) [-] *)

    (* Model Predictive Control Quadratic Cost Weighting Matrices *)
    Q_mat                           : ARRAY[1..8, 1..8] OF REAL; (* State Error Quadratic Cost Penalty Matrix Q (8x8) [-] *)
    R_mat                           : ARRAY[1..6, 1..6] OF REAL; (* Control Actuation Effort Penalty Matrix R (6x6) [-] *)
    R_delta                         : ARRAY[1..6, 1..6] OF REAL; (* Actuator Slew Rate Variation Penalty Matrix R_delta (6x6) [-] *)
    P_mat                           : ARRAY[1..8, 1..8] OF REAL; (* Terminal Horizon State Error Penalty Matrix P (8x8) [-] *)

    (* State, Control, Measurement & Innovation Vectors *)
    x_hat                           : ARRAY[1..8] OF REAL;       (* Filtered a-posteriori Cyber-Physical State Vector Estimate [-] *)
    x_pred                          : ARRAY[1..8] OF REAL;       (* One-Step Ahead a-priori State Prediction Vector [-] *)
    x_ref                           : ARRAY[1..8] OF REAL;       (* Coordinated Target Reference State Setpoint Vector [-] *)
    x_corr                          : ARRAY[1..8] OF REAL;       (* Innovation-Corrected State Vector Before Time Update [-] *)
    u_vec                           : ARRAY[1..6] OF REAL;       (* Coordinated Actuator Command Vector [Fuel %, VGV deg, FW %, Spray %, Bypass %, Duct %] *)
    u_prev                          : ARRAY[1..6] OF REAL;       (* Previous Execution Scan Actuator Vector [-] *)
    u_ref                           : ARRAY[1..6] OF REAL;       (* Reference Baseline Actuator Equilibrium Vector [-] *)
    u_min                           : ARRAY[1..6] OF REAL;       (* Physical Lower Saturation Bounds on Actuators [-] *)
    u_max                           : ARRAY[1..6] OF REAL;       (* Physical Upper Saturation Bounds on Actuators [-] *)
    du_max                          : ARRAY[1..6] OF REAL;       (* Maximum Allowable Actuator Rate of Change per Scan [units/scan] *)
    y_meas                          : ARRAY[1..6] OF REAL;       (* High-Reliability 2oo3 Voted Process Measurement Vector [-] *)
    y_est                           : ARRAY[1..6] OF REAL;       (* Estimated Output Vector from Observer: y_est = C * x_hat [-] *)
    innov_err                       : ARRAY[1..6] OF REAL;       (* Innovation Residual Error Vector: innov_err = y_meas - y_est [-] *)

    (* =================================================================================================================
     * SECTION 3.3: RECEDING HORIZON MPC OPTIMIZER BUFFERS (Np=5, Nu=6)
     * ================================================================================================================= *)
    u_traj                          : ARRAY[1..5, 1..6] OF REAL; (* Forward Actuator Prediction Horizon Trajectory [step, input] *)
    x_traj                          : ARRAY[1..5, 1..8] OF REAL; (* Forward State Prediction Horizon Trajectory [step, state] *)
    lambda_vec                      : ARRAY[1..5, 1..8] OF REAL; (* Backward Costate Adjoint Multiplier Trajectory [step, state] *)
    grad_u                          : ARRAY[1..5, 1..6] OF REAL; (* Projected Gradient of Quadratic Cost Functional [step, input] *)
    rPGD_Alpha_Step                 : REAL := 0.0125;     (* Projected Gradient Descent Learning Rate Step Size [-] *)

    (* Iteration & Coordinate Scratch Indices *)
    i_idx                           : INT;                (* General Row / State Index 1..8 *)
    j_idx                           : INT;                (* General Column / Input Index 1..6 *)
    k_idx                           : INT;                (* Time Step Horizon Index 1..5 *)
    m_idx                           : INT;                (* Output Measurement Index 1..6 *)
    iter_idx                        : INT;                (* PGD Optimization Unrolled Loop Iteration Counter 1..6 *)
    rTemp_Sum                       : REAL;               (* High-Precision Floating-Point Matrix Accumulator *)
    rCandidate_U                    : REAL;               (* Projected Gradient Actuator Trial Value *)
    rDelta_U                        : REAL;               (* Slew Rate Clamping Increment *)

    (* =================================================================================================================
     * SECTION 3.4: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING STRUCTURES
     * Channel Groups:
     *   1: EGT Rakes (A, B, C) [deg C]
     *   2: HP Drum Narrow-Range Level (A, B, C) [mm]
     *   3: Main Steam Temperature (A, B, C) [deg C]
     *   4: HP Steam Coriolis Mass Flow (A, B, C) [kg/s]
     *   5: Generator Active Power Transducers (A, B, C) [MW]
     * ================================================================================================================= *)
    (* Channel Group 1: EGT *)
    rEGT_Previous_A                 : REAL := 0.0;
    rEGT_Previous_B                 : REAL := 0.0;
    rEGT_Previous_C                 : REAL := 0.0;
    bEGT_Healthy_A                  : BOOL := TRUE;
    bEGT_Healthy_B                  : BOOL := TRUE;
    bEGT_Healthy_C                  : BOOL := TRUE;
    rTimer_EGT_Discrep_AB           : REAL := 0.0;
    rTimer_EGT_Discrep_BC           : REAL := 0.0;
    rTimer_EGT_Discrep_CA           : REAL := 0.0;
    bAlarm_EGT_Discrepancy          : BOOL := FALSE;
    nMode_EGT_TMR                   : INT := 3;           (* 3=2oo3 Normal, 2=1oo2 Degraded, 1=1oo1 Critical, 0=Fail *)
    rVoted_EGT_Raw                  : REAL := 0.0;

    (* Channel Group 2: HP Drum Level *)
    rDrumL_Previous_A               : REAL := 0.0;
    rDrumL_Previous_B               : REAL := 0.0;
    rDrumL_Previous_C               : REAL := 0.0;
    bDrumL_Healthy_A                : BOOL := TRUE;
    bDrumL_Healthy_B                : BOOL := TRUE;
    bDrumL_Healthy_C                : BOOL := TRUE;
    rTimer_DrumL_Discrep_AB         : REAL := 0.0;
    rTimer_DrumL_Discrep_BC         : REAL := 0.0;
    rTimer_DrumL_Discrep_CA         : REAL := 0.0;
    bAlarm_DrumL_Discrepancy        : BOOL := FALSE;
    nMode_DrumL_TMR                 : INT := 3;
    rVoted_DrumL_Raw                : REAL := 0.0;

    (* Channel Group 3: Main Steam Temperature *)
    rSteamT_Previous_A              : REAL := 0.0;
    rSteamT_Previous_B              : REAL := 0.0;
    rSteamT_Previous_C              : REAL := 0.0;
    bSteamT_Healthy_A               : BOOL := TRUE;
    bSteamT_Healthy_B               : BOOL := TRUE;
    bSteamT_Healthy_C               : BOOL := TRUE;
    rTimer_SteamT_Discrep_AB        : REAL := 0.0;
    rTimer_SteamT_Discrep_BC        : REAL := 0.0;
    rTimer_SteamT_Discrep_CA        : REAL := 0.0;
    bAlarm_SteamT_Discrepancy       : BOOL := FALSE;
    nMode_SteamT_TMR                : INT := 3;
    rVoted_SteamT_Raw               : REAL := 0.0;

    (* Channel Group 4: HP Steam Flow *)
    rSteamF_Previous_A              : REAL := 0.0;
    rSteamF_Previous_B              : REAL := 0.0;
    rSteamF_Previous_C              : REAL := 0.0;
    bSteamF_Healthy_A               : BOOL := TRUE;
    bSteamF_Healthy_B               : BOOL := TRUE;
    bSteamF_Healthy_C               : BOOL := TRUE;
    rTimer_SteamF_Discrep_AB        : REAL := 0.0;
    rTimer_SteamF_Discrep_BC        : REAL := 0.0;
    rTimer_SteamF_Discrep_CA        : REAL := 0.0;
    bAlarm_SteamF_Discrepancy       : BOOL := FALSE;
    nMode_SteamF_TMR                : INT := 3;
    rVoted_SteamF_Raw               : REAL := 0.0;

    (* Channel Group 5: Generator Active Power *)
    rPower_Previous_A               : REAL := 0.0;
    rPower_Previous_B               : REAL := 0.0;
    rPower_Previous_C               : REAL := 0.0;
    bPower_Healthy_A                : BOOL := TRUE;
    bPower_Healthy_B                : BOOL := TRUE;
    bPower_Healthy_C                : BOOL := TRUE;
    rTimer_Power_Discrep_AB         : REAL := 0.0;
    rTimer_Power_Discrep_BC         : REAL := 0.0;
    rTimer_Power_Discrep_CA         : REAL := 0.0;
    bAlarm_Power_Discrepancy        : BOOL := FALSE;
    nMode_Power_TMR                 : INT := 3;
    rVoted_Power_Raw                : REAL := 0.0;

    (* TMR Discrepancy Tolerances & Maximum Rates of Change *)
    rTol_EGT_Discrep_degC           : REAL := 25.0;       (* Combustor Radial Temperature Spread Tolerance [deg C] *)
    rTol_DrumL_Discrep_mm           : REAL := 30.0;       (* Drum Differential Pressure Transducer Tolerance [mm] *)
    rTol_SteamT_Discrep_degC        : REAL := 15.0;       (* Main Steam Superheater Tolerance [deg C] *)
    rTol_SteamF_Discrep_kgs         : REAL := 12.0;       (* Coriolis Mass Flow Tolerance [kg/s] *)
    rTol_Power_Discrep_MW           : REAL := 10.0;       (* Grid Active Power Transducer Tolerance [MW] *)

    rMax_ROC_EGT_degC_s             : REAL := 80.0;       (* Maximum Physical Plausible EGT Rate of Change [deg C/s] *)
    rMax_ROC_DrumL_mm_s             : REAL := 60.0;       (* Maximum Plausible Drum Level Displacement Velocity [mm/s] *)
    rMax_ROC_SteamT_degC_s          : REAL := 30.0;       (* Maximum Thermal Shock Gradient [deg C/s] *)
    rMax_ROC_SteamF_kgs_s           : REAL := 50.0;       (* Maximum Steam Flow Dynamic Spike [kg/s/s] *)
    rMax_ROC_Power_MW_s             : REAL := 100.0;      (* Maximum Electrical Inrush Gradient [MW/s] *)

    (* =================================================================================================================
     * SECTION 3.5: DETERMINISTIC 14-STAGE FINITE STATE MACHINE (FSM) VARIABLES
     * ================================================================================================================= *)
    eCurrentState                   : INT := 0;           (* Active Power Plant Operational State [0..13] *)
    ePreviousState                  : INT := 0;           (* Previous Scan Operational State [0..13] *)
    rState_Dwell_Timer              : REAL := 0.0;        (* Time Elapsed in Current State [s] *)
    bState_Entry_Flag               : BOOL := TRUE;       (* One-Shot Pulse on State Entry *)

    (* State Transition Sub-Timers & Sequence Integrators *)
    rTimer_Purge_Elapsed_s          : REAL := 0.0;        (* NFPA 85 Combustion Chamber Air Purge Timer [s] *)
    rTimer_Crank_Spinup_s           : REAL := 0.0;        (* Starter Motor Ignition Acceleration Timer [s] *)
    rTimer_Warmup_Idle_s            : REAL := 0.0;        (* Turbomachinery Rotor Thermal Soak Timer [s] *)
    rTimer_Sync_Window_s            : REAL := 0.0;        (* Auto-Synchronizer Phase Matching Time [s] *)
    rTimer_DLN_Transfer_s           : REAL := 0.0;        (* Dry Low NOx Fuel Gas Staging Transition Timer [s] *)
    rTimer_Drum_Swell_Lock_s        : REAL := 0.0;        (* HRSG Evaporator Boiling Void Stabilization Window [s] *)
    rTimer_Duct_Burner_Ramp_s       : REAL := 0.0;        (* Supplemental Peaking Duct Firing Heat Ramp Timer [s] *)
    rTimer_Turndown_Cooldown_s      : REAL := 0.0;        (* Coordinated Thermal Stress Turndown Timer [s] *)
    rTimer_Trip_Lockout_s           : REAL := 0.0;        (* Master Fuel Trip Solenoid De-Energize Lockout Timer [s] *)

    (* Coordinated Setpoint Profilers & Feedforward Ramps *)
    rTarget_Power_MW                : REAL := 0.0;        (* Intermediate Governor Power Setpoint [MW] *)
    rRamped_Power_MW                : REAL := 0.0;        (* Rate-Limited Active Power Trajectory [MW] *)
    rTarget_DrumLevel_mm            : REAL := 0.0;        (* Drum Working Level Centerline Setpoint [mm] *)
    rTarget_SteamTemp_degC          : REAL := 565.0;      (* Main Steam Regulated Enthalpy Temperature [deg C] *)
    rTarget_VGV_Position_deg        : REAL := 0.0;        (* Compressor Air Induction Guide Vane Setpoint [deg] *)
    rDynamic_Decoupling_Spray_FF    : REAL := 0.0;        (* Anticipatory Attemperator Spray Feedforward Compensation [%] *)
    rDynamic_Decoupling_FW_FF       : REAL := 0.0;        (* 3-Element Boiler Feedwater Shrink/Swell Balance Bias [%] *)
    rPrimary_Freq_Delta_MW          : REAL := 0.0;        (* Grid Frequency Disturbance Proportional Response [MW] *)

    (* =================================================================================================================
     * SECTION 3.6: ISA-18.2 PROCESS ALARM SETPOINTS, TRIP THRESHOLDS & DEBOUNCE TIMERS
     * ================================================================================================================= *)
    (* Trip Thresholds & Pre-Warnings *)
    rTrip_EGT_HighHigh_HH           : REAL := 660.0;      (* SIL-3 Combustor Exhaust Gas High-High Trip [deg C] *)
    rWarn_EGT_High_H                : REAL := 645.0;      (* Combustor Exhaust Gas Temperature High Alarm [deg C] *)
    rDeadband_EGT_degC              : REAL := 6.0;        (* Exhaust Gas Alarm Clearance Hysteresis Deadband [deg C] *)

    rTrip_Drum_LowLow_LL            : REAL := -250.0;     (* SIL-3 Evaporator Dry-Out Tube Rupture Protection Trip [mm] *)
    rTrip_Drum_HighHigh_HH          : REAL := 200.0;      (* SIL-3 Steam Turbine Water Induction Protection Trip [mm] *)
    rWarn_Drum_Low_L                : REAL := -120.0;     (* HP Drum Water Level Low Warning [mm] *)
    rWarn_Drum_High_H               : REAL := 120.0;      (* HP Drum Water Level High Warning [mm] *)
    rDeadband_Drum_mm               : REAL := 10.0;       (* Drum Level Alarm Clearance Hysteresis Deadband [mm] *)

    rTrip_SteamTemp_HighHigh_HH     : REAL := 595.0;      (* Final Superheater Creep Stress Safety Trip [deg C] *)
    rWarn_SteamTemp_High_H          : REAL := 580.0;      (* Superheater Temperature High Pre-Alarm [deg C] *)
    rWarn_SteamTemp_Low_L           : REAL := 480.0;      (* Superheater Temperature Low Droop Warning [deg C] *)
    rDeadband_SteamTemp_degC        : REAL := 4.0;        (* Steam Temperature Clearance Deadband [deg C] *)

    rTrip_Overspeed_HH_RPM          : REAL := 3300.0;     (* 110% Over-Speed Turbomachinery Rotor Safety Trip [rpm] *)
    rWarn_Overspeed_H_RPM           : REAL := 3150.0;     (* 105% Over-Speed Governor Alarm Threshold [rpm] *)
    rTrip_FlameLoss_Threshold_Pct   : REAL := 15.0;       (* Minimum Permissible Flame Scanner Persistence [%] *)

    (* Hard Debounce Accumulation Timers *)
    rTimer_Alarm_EGT_HH             : REAL := 0.0;
    rTimer_Alarm_EGT_H              : REAL := 0.0;
    rTimer_Alarm_Drum_LL            : REAL := 0.0;
    rTimer_Alarm_Drum_HH            : REAL := 0.0;
    rTimer_Alarm_Drum_L             : REAL := 0.0;
    rTimer_Alarm_Drum_H             : REAL := 0.0;
    rTimer_Alarm_SteamT_HH          : REAL := 0.0;
    rTimer_Alarm_SteamT_H           : REAL := 0.0;
    rTimer_Alarm_SteamT_L           : REAL := 0.0;
    rTimer_Alarm_FlameLoss          : REAL := 0.0;
    rTimer_Alarm_Overspeed          : REAL := 0.0;

    (* Active Alarm Condition Flags *)
    bActive_EGT_HH                  : BOOL := FALSE;
    bActive_EGT_H                   : BOOL := FALSE;
    bActive_Drum_LL                 : BOOL := FALSE;
    bActive_Drum_HH                 : BOOL := FALSE;
    bActive_Drum_L                  : BOOL := FALSE;
    bActive_Drum_H                  : BOOL := FALSE;
    bActive_SteamT_HH               : BOOL := FALSE;
    bActive_SteamT_H                : BOOL := FALSE;
    bActive_SteamT_L                : BOOL := FALSE;
    bActive_FlameLoss               : BOOL := FALSE;
    bActive_Overspeed               : BOOL := FALSE;
    bMFT_Latched                    : BOOL := FALSE;
END_VAR
"""
