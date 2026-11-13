# -*- coding: utf-8 -*-
"""
smt_builder/var_declarations.py
Generates the comprehensive VAR block with all state-space matrices, MPC weights,
TMR voting structures, 16-spindle records, FSM variables, and ISA-18.2 alarm declarations.
"""

def get_var_declarations():
    return """VAR
    (* ============================================================================================== *)
    (* INTERNAL DISCRETE STATE-SPACE CYBER-PHYSICAL MODEL (10 STATES, 4 INPUTS, 6 OUTPUTS, Ts = 1 ms) *)
    (* ============================================================================================== *)
    (* State Vector x[k]:
       x[1]  : Gantry primary carriage position x_car [mm]
       x[2]  : Gantry carriage velocity v_car [mm/s]
       x[3]  : Tool-center-point (TCP) flexure displacement delta_tcp [mm]
       x[4]  : Tool-center-point flexure velocity d(delta_tcp)/dt [mm/s]
       x[5]  : Spindle rotation angle theta_sp [mrad]
       x[6]  : Spindle angular velocity omega_sp [rad/s]
       x[7]  : Vacuum nozzle chamber pressure P_vac [kPa]
       x[8]  : Vacuum chamber acoustic volumetric flow Q_vac [L/min]
       x[9]  : Dual-gantry crossbeam yaw skew angle phi_yaw [mrad]
       x[10] : Thermal structural strain expansion offset epsilon_th [um] *)
    a_mat                           : ARRAY[1..10, 1..10] OF REAL; (* Discrete state transition matrix A (10x10) *)
    b_mat                           : ARRAY[1..10, 1..4] OF REAL;  (* Discrete input influence matrix B (10x4) *)
    c_mat                           : ARRAY[1..6, 1..10] OF REAL;  (* Discrete output observation matrix C (6x10) *)
    d_mat                           : ARRAY[1..6, 1..4] OF REAL;   (* Discrete feedthrough matrix D (6x4) *)
    l_obs                           : ARRAY[1..10, 1..6] OF REAL;  (* Luenberger observer innovation gain matrix L (10x6) *)

    x_state                         : ARRAY[1..10] OF REAL;        (* Current estimated cyber-physical state x[k] *)
    x_next                          : ARRAY[1..10] OF REAL;        (* Propagated next state prediction x[k+1] *)
    x_ref                           : ARRAY[1..10] OF REAL;        (* Dynamic reference trajectory state target x_ref[k] *)
    y_est                           : ARRAY[1..6] OF REAL;         (* Predicted measurement output y_hat[k] = C*x + D*u *)
    y_meas                          : ARRAY[1..6] OF REAL;         (* Sensor feedback vector from 2oo3 TMR voting *)
    e_innov                         : ARRAY[1..6] OF REAL;         (* Innovation error residual e[k] = y_meas - y_hat *)

    u_ctrl                          : ARRAY[1..4] OF REAL;         (* Optimal control demand u[k] *)
    u_prev                          : ARRAY[1..4] OF REAL;         (* Prior control command u[k-1] for slew rate limits *)
    delta_u                         : ARRAY[1..4] OF REAL;         (* Control command rate-of-change delta_u = u[k] - u[k-1] *)
    bStateSpace_Initialized         : BOOL := FALSE;               (* One-shot initialization latch for state-space matrices *)

    (* Model Predictive Control (MPC) Cost Matrices & Optimization Buffers *)
    q_mat                           : ARRAY[1..10, 1..10] OF REAL; (* State error penalty diagonal matrix Q (10x10) *)
    r_mat                           : ARRAY[1..4, 1..4] OF REAL;   (* Actuator effort penalty diagonal matrix R (4x4) *)
    s_mat                           : ARRAY[1..4, 1..4] OF REAL;   (* Actuator rate-of-change penalty matrix S (4x4) *)
    p_mat                           : ARRAY[1..10, 1..10] OF REAL; (* Terminal state penalty matrix P (10x10) *)

    (* Horizon Prediction Buffers (Np = 5, Nc = 3) *)
    x_pred_h0                       : ARRAY[1..10] OF REAL;
    x_pred_h1                       : ARRAY[1..10] OF REAL;
    x_pred_h2                       : ARRAY[1..10] OF REAL;
    x_pred_h3                       : ARRAY[1..10] OF REAL;
    x_pred_h4                       : ARRAY[1..10] OF REAL;
    x_pred_h5                       : ARRAY[1..10] OF REAL;

    u_cand_h0                       : ARRAY[1..4] OF REAL;
    u_cand_h1                       : ARRAY[1..4] OF REAL;
    u_cand_h2                       : ARRAY[1..4] OF REAL;

    grad_u_h0                       : ARRAY[1..4] OF REAL;
    grad_u_h1                       : ARRAY[1..4] OF REAL;
    grad_u_h2                       : ARRAY[1..4] OF REAL;

    rPGD_StepSize                   : REAL := 0.00042;             (* Projected Gradient Descent descent step size alpha *)
    rMPC_TotalCost                  : REAL;                        (* Evaluated quadratic performance index J *)
    iPGD_IterCount                  : INT;                         (* Iteration counter for unrolled optimization *)

    (* Actuator Physical Saturation & Slew Limits *)
    rLimit_ForceX_Max               : REAL := 250.0;               (* Maximum Gantry X linear motor thrust force [N] *)
    rLimit_ForceX_Min               : REAL := -250.0;              (* Minimum Gantry X linear motor thrust force [N] *)
    rLimit_ForceY_Max               : REAL := 180.0;               (* Maximum Gantry Y linear motor thrust force [N] *)
    rLimit_ForceY_Min               : REAL := -180.0;              (* Minimum Gantry Y linear motor thrust force [N] *)
    rLimit_ThetaTorque_Max          : REAL := 120.0;               (* Maximum Spindle Theta torque limit [mN*m] *)
    rLimit_ThetaTorque_Min          : REAL := -120.0;              (* Minimum Spindle Theta torque limit [mN*m] *)
    rLimit_VacuumPWM_Max            : REAL := 100.0;               (* Maximum vacuum valve duty cycle [%] *)
    rLimit_VacuumPWM_Min            : REAL := 0.0;                 (* Minimum vacuum valve duty cycle [%] *)
    rLimit_SlewRate_Force_Max       : REAL := 45.0;                (* Maximum force slew rate per ms [N/ms] *)
    rLimit_SlewRate_Torque_Max      : REAL := 25.0;                (* Maximum torque slew rate per ms [mN*m/ms] *)

    (* ============================================================================================== *)
    (* 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) ARCHITECTURE FOR 5 CRITICAL SENSOR TRIPLETS               *)
    (* ============================================================================================== *)
    (* Triplet 1: Gantry X-Axis Linear Encoders *)
    rTMR_X_ChA                      : REAL;
    rTMR_X_ChB                      : REAL;
    rTMR_X_ChC                      : REAL;
    rTMR_X_Dev_AB                   : REAL;
    rTMR_X_Dev_BC                   : REAL;
    rTMR_X_Dev_CA                   : REAL;
    rTMR_X_Voted                    : REAL;
    bTMR_X_Discrep_AB               : BOOL;
    bTMR_X_Discrep_BC               : BOOL;
    bTMR_X_Discrep_CA               : BOOL;
    udiTMR_X_Timer_AB               : UDINT;
    udiTMR_X_Timer_BC               : UDINT;
    udiTMR_X_Timer_CA               : UDINT;
    iTMR_X_DegradationState         : INT := 0;                    (* 0=3-Ch Normal, 1=2-Ch Degraded, 2=Single, 3=Fault *)
    bTMR_X_MajorDiscrepancyTrip     : BOOL;

    (* Triplet 2: Gantry Y-Axis Crossbeam Encoders *)
    rTMR_Y_ChA                      : REAL;
    rTMR_Y_ChB                      : REAL;
    rTMR_Y_ChC                      : REAL;
    rTMR_Y_Dev_AB                   : REAL;
    rTMR_Y_Dev_BC                   : REAL;
    rTMR_Y_Dev_CA                   : REAL;
    rTMR_Y_Voted                    : REAL;
    bTMR_Y_Discrep_AB               : BOOL;
    bTMR_Y_Discrep_BC               : BOOL;
    bTMR_Y_Discrep_CA               : BOOL;
    udiTMR_Y_Timer_AB               : UDINT;
    udiTMR_Y_Timer_BC               : UDINT;
    udiTMR_Y_Timer_CA               : UDINT;
    iTMR_Y_DegradationState         : INT := 0;
    bTMR_Y_MajorDiscrepancyTrip     : BOOL;

    (* Triplet 3: Spindle Turret Theta Encoders *)
    rTMR_Theta_ChA                  : REAL;
    rTMR_Theta_ChB                  : REAL;
    rTMR_Theta_ChC                  : REAL;
    rTMR_Theta_Dev_AB               : REAL;
    rTMR_Theta_Dev_BC               : REAL;
    rTMR_Theta_Dev_CA               : REAL;
    rTMR_Theta_Voted                : REAL;
    bTMR_Theta_Discrep_AB           : BOOL;
    bTMR_Theta_Discrep_BC           : BOOL;
    bTMR_Theta_Discrep_CA           : BOOL;
    udiTMR_Theta_Timer_AB           : UDINT;
    udiTMR_Theta_Timer_BC           : UDINT;
    udiTMR_Theta_Timer_CA           : UDINT;
    iTMR_Theta_DegradationState     : INT := 0;
    bTMR_Theta_MajorDiscrepancyTrip : BOOL;

    (* Triplet 4: Vacuum Manifold Pressure Transducers *)
    rTMR_Vac_ChA                    : REAL;
    rTMR_Vac_ChB                    : REAL;
    rTMR_Vac_ChC                    : REAL;
    rTMR_Vac_Dev_AB                 : REAL;
    rTMR_Vac_Dev_BC                 : REAL;
    rTMR_Vac_Dev_CA                 : REAL;
    rTMR_Vac_Voted                  : REAL;
    bTMR_Vac_Discrep_AB             : BOOL;
    bTMR_Vac_Discrep_BC             : BOOL;
    bTMR_Vac_Discrep_CA             : BOOL;
    udiTMR_Vac_Timer_AB             : UDINT;
    udiTMR_Vac_Timer_BC             : UDINT;
    udiTMR_Vac_Timer_CA             : UDINT;
    iTMR_Vac_DegradationState       : INT := 0;
    bTMR_Vac_MajorDiscrepancyTrip   : BOOL;

    (* Triplet 5: Laser PCB Warpage Gauges *)
    rTMR_Laser_ChA                  : REAL;
    rTMR_Laser_ChB                  : REAL;
    rTMR_Laser_ChC                  : REAL;
    rTMR_Laser_Dev_AB               : REAL;
    rTMR_Laser_Dev_BC               : REAL;
    rTMR_Laser_Dev_CA               : REAL;
    rTMR_Laser_Voted                : REAL;
    bTMR_Laser_Discrep_AB           : BOOL;
    bTMR_Laser_Discrep_BC           : BOOL;
    bTMR_Laser_Discrep_CA           : BOOL;
    udiTMR_Laser_Timer_AB           : UDINT;
    udiTMR_Laser_Timer_BC           : UDINT;
    udiTMR_Laser_Timer_CA           : UDINT;
    iTMR_Laser_DegradationState     : INT := 0;
    bTMR_Laser_MajorDiscrepancyTrip : BOOL;

    (* Discrepancy Tolerance Limits & Persistence Thresholds *)
    rTol_Discrep_X_mm               : REAL := 0.045;               (* Maximum allowable X-axis encoder divergence [mm] *)
    rTol_Discrep_Y_mm               : REAL := 0.045;               (* Maximum allowable Y-axis encoder divergence [mm] *)
    rTol_Discrep_Theta_deg          : REAL := 0.080;               (* Maximum allowable Theta encoder divergence [deg] *)
    rTol_Discrep_Vac_kPa            : REAL := 6.50;                (* Maximum allowable Vacuum transducer divergence [kPa] *)
    rTol_Discrep_Laser_mm           : REAL := 0.085;               (* Maximum allowable Laser warpage divergence [mm] *)
    udiTMR_DiscrepancyLimit_ms      : UDINT := 25;                 (* Persistence timeout before degradation escalation [ms] *)

    (* ============================================================================================== *)
    (* 16-SPINDLE STAR TURRET TRACKING & MANAGEMENT DATA STRUCTURES                                    *)
    (* ============================================================================================== *)
    arrSpindle_HasComponent         : ARRAY[1..16] OF BOOL;        (* True if spindle nozzle holds picked component *)
    arrSpindle_ComponentID          : ARRAY[1..16] OF INT;         (* Part ID assigned to spindle nozzle *)
    arrSpindle_PickVacuum_kPa       : ARRAY[1..16] OF REAL;        (* Peak vacuum recorded after pick touchdown [kPa] *)
    arrSpindle_CurrentVacuum_kPa    : ARRAY[1..16] OF REAL;        (* Instantaneous dynamic vacuum pressure [kPa] *)
    arrSpindle_LandingForce_N       : ARRAY[1..16] OF REAL;        (* Measured voice coil landing impact force [N] *)
    arrSpindle_VisionOffset_X       : ARRAY[1..16] OF REAL;        (* Vision calculated offset dX for spindle [mm] *)
    arrSpindle_VisionOffset_Y       : ARRAY[1..16] OF REAL;        (* Vision calculated offset dY for spindle [mm] *)
    arrSpindle_VisionOffset_Theta   : ARRAY[1..16] OF REAL;        (* Vision calculated offset dTheta for spindle [deg] *)
    arrSpindle_VisionPassed         : ARRAY[1..16] OF BOOL;        (* Optical inspection verification passed *)
    arrSpindle_RejectFlag           : ARRAY[1..16] OF BOOL;        (* Flagged for ejection into defect purge bin *)
    arrSpindle_ConsecutiveErrors    : ARRAY[1..16] OF INT;         (* Mispick / drop error count per spindle *)
    arrSpindle_Z_Stroke_mm          : ARRAY[1..16] OF REAL;        (* Voice-coil displacement position [mm] *)
    arrSpindle_BlowOffActive        : ARRAY[1..16] OF BOOL;        (* Active positive-pressure blow-off pulse flag *)
    arrSpindle_BlowOffTimer_ms      : ARRAY[1..16] OF UDINT;       (* Micro-blow-off pulse elapsed duration [ms] *)

    iInternalSpindlePointer         : INT := 1;                    (* Internal sequence pointer index (1 to 16) *)
    iTotalComponentsOnHead          : INT := 0;                    (* Number of valid components currently held on head *)

    (* ============================================================================================== *)
    (* THERMAL LINEAR SCALE GRADIENT EXPANSION COMPENSATION PARAMETERS                                *)
    (* ============================================================================================== *)
    rRefTemp_Baseline               : REAL := 20.0;                (* Reference calibration temperature [deg C] *)
    rScaleCTE_Invar                 : REAL := 1.15E-6;             (* Invar optical scale linear thermal coefficient [1/K] *)
    rScaleCTE_Ceramic               : REAL := 0.85E-6;             (* Zerodur ceramic crossbeam coefficient [1/K] *)
    rThermalGradientGain_X          : REAL := 0.00035;             (* Differential expansion gain between X1 and X2 rails *)
    rTurretDrumExpansionGain        : REAL := 0.00062;             (* Radial drum expansion coefficient with spindle temp *)
    rLength_Gantry_X_mm             : REAL := 1800.0;              (* Total active measurement travel length X [mm] *)
    rLength_Gantry_Y_mm             : REAL := 950.0;               (* Total active measurement travel length Y [mm] *)

    (* Real-time thermal expansion offsets calculated *)
    rComp_X_Total_mm                : REAL := 0.0;
    rComp_Y_Total_mm                : REAL := 0.0;
    rComp_Theta_Drum_deg            : REAL := 0.0;

    (* ============================================================================================== *)
    (* 7-SEGMENT S-CURVE TRAJECTORY GENERATOR & VIBRATION-FREE PROFILE BUFFERS                        *)
    (* ============================================================================================== *)
    rProfile_Pos_Target_X           : REAL;
    rProfile_Pos_Target_Y           : REAL;
    rProfile_Pos_Actual_X           : REAL;
    rProfile_Pos_Actual_Y           : REAL;
    rProfile_Vel_Actual_X           : REAL;
    rProfile_Vel_Actual_Y           : REAL;
    rProfile_Acc_Actual_X           : REAL;
    rProfile_Acc_Actual_Y           : REAL;

    rSCurve_MaxJerk                 : REAL := 450.0;               (* Maximum jerk constraint [m/s^3] *)
    rSCurve_MaxAcc                  : REAL := 45.0;                (* Maximum acceleration constraint [m/s^2] *)
    rSCurve_MaxVel                  : REAL := 3.20;                (* Maximum cruising velocity constraint [m/s] *)
    rSCurve_TrajectoryDistance      : REAL;
    rSCurve_ProgressRatio           : REAL;
    iSCurve_SegmentPhase            : INT := 0;                    (* 0=Idle, 1=Jerk+, 2=ConstAcc, 3=Jerk-, 4=Cruising, 5=JerkDec+, 6=ConstDec, 7=JerkDec- *)
    bTrajectoryCompleted            : BOOL := TRUE;

    (* ============================================================================================== *)
    (* DETERMINISTIC 14-STAGE FINITE STATE MACHINE (FSM) CONTROL REGISTERS                            *)
    (* ============================================================================================== *)
    iFSM_State                      : INT := 0;                    (* Current active operational state identifier *)
    iFSM_PrevState                  : INT := -1;                   (* Previous state for transition edge detection *)
    udiFSM_SubStep                  : UDINT := 0;                  (* Step sequence index within active state *)
    udiFSM_StateDwell_ms            : UDINT := 0;                  (* Continuous dwell time in current state [ms] *)
    bFSM_StateFirstScan             : BOOL := TRUE;                (* Rising edge strobe on entering new state *)
    iFSM_ReturnStateAfterRecovery   : INT := 0;                    (* Stored state pointer during safe recovery *)

    (* State Enumeration Constants *)
    STATE_00_INIT_HOMING_SELFTEST   : INT := 0;
    STATE_01_PCB_CONVEYOR_INDEX     : INT := 1;
    STATE_02_GLOBAL_OPTICAL_ALIGN   : INT := 2;
    STATE_03_LASER_WARPAGE_SURFACE  : INT := 3;
    STATE_04_FEEDER_BANK_APPROACH   : INT := 4;
    STATE_05_NOZZLE_TOUCH_PICK      : INT := 5;
    STATE_06_PICK_PRESSURE_VERIFY   : INT := 6;
    STATE_07_FLYBY_VISION_STROBE    : INT := 7;
    STATE_08_VISION_OFFSET_APPLY    : INT := 8;
    STATE_09_HIGH_SPEED_FLIGHT      : INT := 9;
    STATE_10_PRECISION_Z_LANDING    : INT := 10;
    STATE_11_BLOWOFF_RELEASE        : INT := 11;
    STATE_12_REJECT_BIN_DISCHARGE   : INT := 12;
    STATE_13_NOZZLE_AUTO_EXCHANGE   : INT := 13;
    STATE_14_ESTOP_CONTROLLED_STOP  : INT := 14;

    (* FSM Timeout Watchdogs *)
    udiTimeout_Homing_ms            : UDINT := 8000;
    udiTimeout_ConveyorIndex_ms     : UDINT := 3500;
    udiTimeout_VisionStrobe_ms      : UDINT := 1500;
    udiTimeout_PickTouch_ms         : UDINT := 200;
    udiTimeout_LandingRelease_ms    : UDINT := 250;
    udiTimeout_NozzleExchange_ms    : UDINT := 6000;

    (* ============================================================================================== *)
    (* ISA-18.2 MULTI-TIER ALARM SYSTEM & STATUS WORD PACKING REGISTERS                               *)
    (* ============================================================================================== *)
    (* Alarm Thresholds & Hysteresis Deadbands *)
    rAlarmLimit_FollowError_HH_mm   : REAL := 0.120;               (* High-High Gantry Following Error [mm] *)
    rAlarmLimit_FollowError_H_mm    : REAL := 0.065;               (* High Gantry Following Error warning [mm] *)
    rAlarmDeadband_FollowError_mm   : REAL := 0.015;

    rAlarmLimit_VacLeak_LL_kPa      : REAL := -35.0;               (* Low-Low Vacuum Seal (Severe Leak/Drop) [kPa] *)
    rAlarmLimit_VacLow_L_kPa        : REAL := -52.0;               (* Low Vacuum Warning (Partial Seal) [kPa] *)
    rAlarmDeadband_Vac_kPa          : REAL := 3.0;

    rAlarmLimit_LandingForce_HH_N   : REAL := 12.0;                (* High-High Touchdown Impact Force (Die Crack Risk) [N] *)
    rAlarmLimit_LandingForce_H_N    : REAL := 9.0;                 (* High Touchdown Impact Force warning [N] *)
    rAlarmDeadband_LandingForce_N   : REAL := 0.5;

    rAlarmLimit_ScaleTemp_HH_degC   : REAL := 42.0;                (* High-High Invar Scale Overtemperature [deg C] *)
    rAlarmLimit_ScaleTemp_H_degC    : REAL := 35.0;                (* High Invar Scale Temperature warning [deg C] *)
    rAlarmDeadband_ScaleTemp_degC   : REAL := 1.5;

    rAlarmLimit_SupplyAir_LL_kPa    : REAL := 450.0;               (* Low-Low Main Pneumatic Supply Pressure [kPa] *)
    rAlarmLimit_SupplyAir_L_kPa     : REAL := 520.0;               (* Low Main Pneumatic Supply Pressure warning [kPa] *)
    rAlarmDeadband_SupplyAir_kPa    : REAL := 15.0;

    rAlarmLimit_VisionOffset_HH_mm  : REAL := 1.250;               (* High-High Component Translation Offset [mm] *)
    rAlarmLimit_VisionOffset_H_mm   : REAL := 0.850;               (* High Component Translation Offset warning [mm] *)
    rAlarmDeadband_VisionOffset_mm  : REAL := 0.050;

    rAlarmLimit_ConsecutiveFails_HH : INT := 5;                    (* High-High Consecutive Mispick Trip Limit [count] *)
    rAlarmLimit_ConsecutiveFails_H  : INT := 3;                    (* High Consecutive Mispick Warning Limit [count] *)

    (* Active Alarm State Latches *)
    bAlarm_FollowError_X_HH         : BOOL := FALSE;
    bAlarm_FollowError_X_H          : BOOL := FALSE;
    bAlarm_FollowError_Y_HH         : BOOL := FALSE;
    bAlarm_FollowError_Y_H          : BOOL := FALSE;
    bAlarm_VacuumLeak_LL            : BOOL := FALSE;
    bAlarm_VacuumLow_L              : BOOL := FALSE;
    bAlarm_LandingForce_HH          : BOOL := FALSE;
    bAlarm_LandingForce_H           : BOOL := FALSE;
    bAlarm_ScaleTemp_HH             : BOOL := FALSE;
    bAlarm_ScaleTemp_H              : BOOL := FALSE;
    bAlarm_SupplyAir_LL             : BOOL := FALSE;
    bAlarm_SupplyAir_L              : BOOL := FALSE;
    bAlarm_VisionOffset_HH          : BOOL := FALSE;
    bAlarm_VisionOffset_H           : BOOL := FALSE;
    bAlarm_ConsecutiveMispick_HH    : BOOL := FALSE;
    bAlarm_ConsecutiveMispick_H     : BOOL := FALSE;

    (* Diagnostic Feeder Health Registers *)
    bFeeder_TapeJamDetected         : BOOL := FALSE;
    bFeeder_CoverTapePeelError      : BOOL := FALSE;
    bFeeder_SprocketDriveSlip       : BOOL := FALSE;

    (* General Calculation Working Variables *)
    rCalc_X_Dev                     : REAL;
    rCalc_Y_Dev                     : REAL;
    rCalc_FollowError_X             : REAL;
    rCalc_FollowError_Y             : REAL;
    rVoted_X_Raw                    : REAL;
    rVoted_Y_Raw                    : REAL;
    rVoted_Theta_Raw                : REAL;
    rVoted_Vac_Raw                  : REAL;
    rVoted_Laser_Raw                : REAL;

    iIdxSpindle                     : INT;
    iIterPGD                        : INT;
    iRow                            : INT;
    iCol                            : INT;
    rAccumTerm                      : REAL;

    (* Placement Rate Computation Moving Window *)
    udiCycleCounter                 : UDINT := 0;
    udiPlacementIntervalTimer_ms    : UDINT := 0;
    rPlacementRateSmoothed          : REAL := 0.0;
END_VAR
"""
