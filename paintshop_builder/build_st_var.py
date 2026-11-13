# paintshop_builder/build_st_var.py

def get_var_declarations():
    return """VAR
    (* Execution Scheduling & Time Base *)
    bFirstScanDone                  : BOOL := FALSE;    (* One-Shot System Power-On Initialization Flag [-] *)
    rTs_s                           : REAL := 0.010;    (* Discrete Task Execution Period: 10 [ms] *)
    rScanCounter                    : DINT := 0;        (* Cyclic Continuous Scan Accumulator [-] *)

    (* Cyber-Physical Discrete State-Space Model Dimension Constants (8-State, 6-Input, 6-Output, 3-Disturbance) *)
    (* States x:
         x[1] = Bell turbine rotational speed deviation [rpm]
         x[2] = Electrostatic tip high voltage potential deviation [kV]
         x[3] = Paint delivery hydraulic line pressure deviation [bar]
         x[4] = Paint volumetric dosing flow rate deviation [mL/min]
         x[5] = Inner shaping shroud air pressure deviation [bar]
         x[6] = Outer shaping shroud air pressure deviation [bar]
         x[7] = Cleanroom booth downdraft static pressure drop deviation [Pa]
         x[8] = Exhaust solvent VOC flammability concentration deviation [%LEL]
       Controls u:
         u[1] = Turbine drive air proportional valve command [0..100 %]
         u[2] = High voltage cascade PWM voltage command [0..100 %]
         u[3] = Micro-gear dosing pump servo rotational speed [0..250 rpm]
         u[4] = Inner shaping air electronic proportional regulator setpoint [0..6.0 bar]
         u[5] = Outer shaping air electronic proportional regulator setpoint [0..6.0 bar]
         u[6] = Recirculation & exhaust plenum VAV air balancing damper command [0..100 %]
       Disturbances w:
         w[1] = Robot TCP linear acceleration / centrifugal fluid head surge [m/s2]
         w[2] = Inline paint fluid viscosity / temperature batch variance [mPa.s]
         w[3] = Cleanroom airlock door transient convective thermal draft [m/s]
       Outputs y:
         y[1] = Bell turbine speed [rpm]
         y[2] = High voltage [kV]
         y[3] = Paint mass flow rate [mL/min]
         y[4] = Inner shaping air pressure [bar]
         y[5] = Outer shaping air pressure [bar]
         y[6] = Downdraft differential pressure [Pa]
    *)

    (* Discrete System Matrices at Ts = 0.010 s *)
    A                               : ARRAY[1..8, 1..8] OF REAL;    (* State Transition Matrix (8x8) *)
    B                               : ARRAY[1..8, 1..6] OF REAL;    (* Input Coupling Matrix (8x6) *)
    C_mat                           : ARRAY[1..6, 1..8] OF REAL;    (* Output Observation Matrix (6x8) *)
    D_mat                           : ARRAY[1..6, 1..6] OF REAL;    (* Direct Feedthrough Matrix (6x6) *)
    E_w                             : ARRAY[1..8, 1..3] OF REAL;    (* Disturbance Coupling Matrix (8x3) *)
    K_obs                           : ARRAY[1..8, 1..6] OF REAL;    (* Steady-State Kalman Filter Innovation Gain Matrix (8x6) *)

    (* State-Space Dynamic Vectors *)
    x_state                         : ARRAY[1..8] OF REAL;          (* True Plant Physical State Deviation Vector *)
    x_hat                           : ARRAY[1..8] OF REAL;          (* A Posteriori Kalman Estimated State Vector *)
    x_pred                          : ARRAY[1..8] OF REAL;          (* A Priori Projected State Vector *)
    u_ctrl                          : ARRAY[1..6] OF REAL;          (* Active Control Vector Applied to Actuators *)
    u_prev                          : ARRAY[1..6] OF REAL;          (* Preceding Scan Cycle Actuator Vector *)
    w_dist                          : ARRAY[1..3] OF REAL;          (* Real-Time Cyber-Physical Disturbance Vector *)
    y_meas                          : ARRAY[1..6] OF REAL;          (* Plant Validated Sensor Measurement Vector *)
    y_est                           : ARRAY[1..6] OF REAL;          (* Estimated Model Measurement Vector *)
    e_innov                         : ARRAY[1..6] OF REAL;          (* Measurement Residual Innovation Vector *)
    r_ref                           : ARRAY[1..8] OF REAL;          (* Dynamic State Tracking Reference Targets *)

    (* Model Predictive Control (MPC) Cost Weighting Matrices & Arrays *)
    Q_cost                          : ARRAY[1..8, 1..8] OF REAL;    (* State Tracking Error Penalty Diagonal Matrix *)
    R_cost                          : ARRAY[1..6, 1..6] OF REAL;    (* Control Energy Penalty Diagonal Matrix *)
    P_term                          : ARRAY[1..8, 1..8] OF REAL;    (* Receding-Horizon Terminal Cost Matrix *)
    S_slew                          : ARRAY[1..6, 1..6] OF REAL;    (* Actuator Slew-Rate Penalty Diagonal Matrix *)

    (* Receding Horizon Prediction Arrays (Horizon N = 5 Steps) *)
    x_traj                          : ARRAY[0..5, 1..8] OF REAL;    (* Projected State Trajectory Across Horizon *)
    u_traj                          : ARRAY[0..4, 1..6] OF REAL;    (* Unrolled Actuator Control Sequence Horizon *)
    grad_u                          : ARRAY[0..4, 1..6] OF REAL;    (* Projected Gradient Descent Cost Gradient *)
    lambda_adj                      : ARRAY[0..5, 1..8] OF REAL;    (* Adjoint Costate Backpropagation Vector *)

    (* Actuator Box Bounds & Rate-of-Change Hard Limits *)
    u_min                           : ARRAY[1..6] OF REAL;          (* Actuator Lower Box Constraints *)
    u_max                           : ARRAY[1..6] OF REAL;          (* Actuator Upper Box Constraints *)
    du_max                          : ARRAY[1..6] OF REAL;          (* Maximum Permissible Slew Rate per 10 ms *)

    (* MPC Projected Gradient Descent Solver Variables *)
    rAlpha_pgd                      : REAL := 0.045;    (* Projected Gradient Descent Adaptation Step Size [-] *)
    nMaxPgdIters                    : INT := 6;         (* Fixed Deterministic Iteration Limit for Scan Parity [-] *)
    rCostCurrent                    : REAL := 0.0;      (* Real-Time Computed Objective Functional Evaluation *)
    rCostPrev                       : REAL := 0.0;      (* Preceding Iteration Cost for Convergence Monitoring *)
    rGradNorm                       : REAL := 0.0;      (* Euclidean Norm of Control Sequence Gradient *)

    (* 2oo3 Triple Modular Redundancy (TMR) Data Structures *)
    (* Channel Group 1: Turbine Speed Optical Transmitters (ST-101A/B/C) *)
    rST_ChA_Speed_rpm               : REAL := 0.0;
    rST_ChB_Speed_rpm               : REAL := 0.0;
    rST_ChC_Speed_rpm               : REAL := 0.0;
    bST_ChA_Healthy                 : BOOL := TRUE;
    bST_ChB_Healthy                 : BOOL := TRUE;
    bST_ChC_Healthy                 : BOOL := TRUE;
    rST_ChA_Dev_rpm                 : REAL := 0.0;
    rST_ChB_Dev_rpm                 : REAL := 0.0;
    rST_ChC_Dev_rpm                 : REAL := 0.0;
    rST_TmrA_s                      : REAL := 0.0;
    rST_TmrB_s                      : REAL := 0.0;
    rST_TmrC_s                      : REAL := 0.0;
    nST_DegradedMode                : INT := 3;         (* 3 = 2oo3 Normal, 2 = 1oo2 Degraded, 1 = 1oo1 Warning, 0 = Fail *)

    (* Channel Group 2: High Voltage Cascade Potential Transmitters (VT-201A/B/C) *)
    rVT_ChA_HV_kV                   : REAL := 0.0;
    rVT_ChB_HV_kV                   : REAL := 0.0;
    rVT_ChC_HV_kV                   : REAL := 0.0;
    bVT_ChA_Healthy                 : BOOL := TRUE;
    bVT_ChB_Healthy                 : BOOL := TRUE;
    bVT_ChC_Healthy                 : BOOL := TRUE;
    rVT_ChA_Dev_kV                  : REAL := 0.0;
    rVT_ChB_Dev_kV                  : REAL := 0.0;
    rVT_ChC_Dev_kV                  : REAL := 0.0;
    rVT_TmrA_s                      : REAL := 0.0;
    rVT_TmrB_s                      : REAL := 0.0;
    rVT_TmrC_s                      : REAL := 0.0;
    nVT_DegradedMode                : INT := 3;

    (* Channel Group 3: Coriolis Micro-Flow Paint Dosing Transmitters (FT-301A/B/C) *)
    rFT_ChA_Flow_mlpm               : REAL := 0.0;
    rFT_ChB_Flow_mlpm               : REAL := 0.0;
    rFT_ChC_Flow_mlpm               : REAL := 0.0;
    bFT_ChA_Healthy                 : BOOL := TRUE;
    bFT_ChB_Healthy                 : BOOL := TRUE;
    bFT_ChC_Healthy                 : BOOL := TRUE;
    rFT_ChA_Dev_mlpm                : REAL := 0.0;
    rFT_ChB_Dev_mlpm                : REAL := 0.0;
    rFT_ChC_Dev_mlpm                : REAL := 0.0;
    rFT_TmrA_s                      : REAL := 0.0;
    rFT_TmrB_s                      : REAL := 0.0;
    rFT_TmrC_s                      : REAL := 0.0;
    nFT_DegradedMode                : INT := 3;

    (* Channel Group 4: Downdraft Static Pressure Drop Transmitters (PT-401A/B/C) *)
    rPT_ChA_Press_Pa                : REAL := 0.0;
    rPT_ChB_Press_Pa                : REAL := 0.0;
    rPT_ChC_Press_Pa                : REAL := 0.0;
    bPT_ChA_Healthy                 : BOOL := TRUE;
    bPT_ChB_Healthy                 : BOOL := TRUE;
    bPT_ChC_Healthy                 : BOOL := TRUE;
    rPT_ChA_Dev_Pa                  : REAL := 0.0;
    rPT_ChB_Dev_Pa                  : REAL := 0.0;
    rPT_ChC_Dev_Pa                  : REAL := 0.0;
    rPT_TmrA_s                      : REAL := 0.0;
    rPT_TmrB_s                      : REAL := 0.0;
    rPT_TmrC_s                      : REAL := 0.0;
    nPT_DegradedMode                : INT := 3;

    (* TMR Discrepancy & Plausibility Tolerances *)
    rST_DiscrepancyLimit_rpm        : REAL := 2500.0;   (* Turbine Speed Divergence Trip Level [rpm] *)
    rVT_DiscrepancyLimit_kV         : REAL := 4.50;     (* High Voltage Divider Divergence Trip Level [kV] *)
    rFT_DiscrepancyLimit_mlpm       : REAL := 22.0;     (* Dosing Flowmeter Divergence Trip Level [mL/min] *)
    rPT_DiscrepancyLimit_Pa         : REAL := 2.20;     (* Static Pressure Divergence Trip Level [Pa] *)
    rTMR_DiscrepancyTimeout_s       : REAL := 0.250;    (* Discrepancy Persistence Trip Threshold: 250 [ms] *)

    (* Sub-5 ms Fast Electrostatic Arc Flash Detection & Quench Architecture *)
    rPrevHVCurrent_uA               : REAL := 0.0;      (* Historical Current for Rate-of-Rise Computation [uA] *)
    rdIdt_uA_per_ms                 : REAL := 0.0;      (* Real-Time Current Time Derivative [uA/ms] *)
    rdIdt_TripThreshold             : REAL := 120.0;    (* Flashover Corona Ionization Arc Rate Limit [uA/ms] *)
    rCurrentPeakLimit_uA            : REAL := 380.0;    (* Hard Overcurrent Cascade Ground Fault Limit [uA] *)
    rArcQuenchTimer_s               : REAL := 0.0;      (* Quench Hold & Bleed Solenoid Assert Timer [s] *)
    bArcQuenchLatched               : BOOL := FALSE;    (* Sub-Millisecond Arc Detection Trip Interlock Flag [-] *)

    (* Deterministic 14-Stage Production Finite State Machine (FSM) Engine *)
    (* FSM State Definitions:
         0 = FSM_BOOT_IDLE                   : Safe Booth Idle Standby & Diagnostics
         1 = FSM_PREPURGE_VENTILATION        : 4-Volume Air Exchange Fresh Cleanroom Purge
         2 = FSM_DOWNDRAFT_AIR_BALANCE_LOCK  : Laminar Air Balance Lock (0.35 m/s +/- 0.02 m/s)
         3 = FSM_HV_CASCADE_DIAGNOSTICS      : High-Voltage Cascade Bleed & Isolation Check
         4 = FSM_COLOR_BLOCK_SOLVENT_FLUSH   : Rapid Color-Change Valve Block Solvent Flush (< 12 s)
         5 = FSM_HIGH_VELOCITY_AIR_DRY       : High-Velocity Air Dry & Blow-Down
         6 = FSM_PAINT_FLUID_FAST_PREFILL    : Paint Fluid Line Fast Pre-Fill to Tip Valve
         7 = FSM_BELL_TURBINE_RAMPUP         : Bell Turbine Soft-Start & Ramp to 65,000 rpm
         8 = FSM_HV_CHARGE_ENABLE            : -90 kV Electrostatic Charge Soft Ramp & Corona Form
         9 = FSM_CAR_BODY_ROBOT_SPRAY        : Body-in-White Contouring Trajectory Spray Active
        10 = FSM_EDGE_WRAP_RECESS_COMPENSATION: Dynamic Shaping Air & Voltage Recess Shaping
        11 = FSM_BELL_CUP_TIP_WASH           : Bell Cup Rim External Solvent Wash & Spin Dry
        12 = FSM_RTO_VOC_BURNER_MODULATION   : RTO VOC Abatement Bed Temperature Tracking
        13 = FSM_SPARK_ARC_QUENCH_TRIP       : High-Speed Quench Trip & Emergency Depressurize
    *)
    nState                          : INT := 0;         (* Active FSM State Number [0..13] *)
    nStatePrev                      : INT := 0;         (* State Memory for Transition One-Shots *)
    rStateTimer_s                   : REAL := 0.0;      (* Duration Clock in Active State [s] *)
    rStateTimeout_s                 : REAL := 300.0;    (* Safety Watchdog Timeout Limit for State [s] *)
    bStateFirstCycle                : BOOL := TRUE;     (* One-Shot State Entry Trigger *)

    (* Rapid Color-Change Valve Block (CCV) Chop-Chop Sequencer Variables *)
    nChopSubPhase                   : INT := 0;         (* 0=Idle, 1=SolventPrePurge, 2=AirPush, 3=ChopChop, 4=AirDry, 5=PreFill *)
    rChopTimer_s                    : REAL := 0.0;      (* Micro-Sequencer Phase Timer [s] *)
    nChopCyclesCount                : INT := 0;         (* Alternating Solvent/Air Pulse Counter [-] *)
    nChopCyclesTarget               : INT := 5;         (* Total Solvent/Air Pulsing Cycles [-] *)

    (* Tip Wash Sequencer Variables *)
    nTipWashSubPhase                : INT := 0;         (* 0=Idle, 1=SolventSpray, 2=HighSpeedSpinDry, 3=AirWipe *)
    rTipWashTimer_s                 : REAL := 0.0;      (* Tip Wash Phase Elapsed Timer [s] *)

    (* Booth Pre-Purge Cleanroom Ventilation Counter *)
    rPurgeElapsedTimer_s            : REAL := 0.0;      (* Continuous Purge Run Timer [s] *)
    rPurgeRequiredDuration_s        : REAL := 180.0;    (* 4 Booth Volume Turnovers at 120,000 m3/h [s] *)

    (* Cyber-Physical Hydrodynamics & Electrostatic Observers *)
    rDropletWeberNumber             : REAL := 0.0;      (* Aerodynamic Weber Number for Droplet Breakup [-] *)
    rChargeToMassRatio_C_per_kg     : REAL := 0.0;      (* Specific Electrostatic Charge Density [C/kg] *)
    rElectricFieldStrength_kV_per_m : REAL := 0.0;      (* Electrostatic Tip-to-Body Field Gradient [kV/m] *)
    rDryFilmThickness_um            : REAL := 0.0;      (* Continuous Dry Film Thickness Integration [um] *)
    rTransferEff_Instant_pct        : REAL := 0.0;      (* Instantaneous Electrostatic Deposition Fraction [%] *)
    rVOCMassRate_g_per_s            : REAL := 0.0;      (* Vaporized Solvent Mass Flow to Exhaust [g/s] *)

    (* Totalizers & Consumption Metrics *)
    rPaintAccumulator_g             : REAL := 0.0;      (* Integrated Clearcoat Applied Mass [g] *)
    rSolventAccumulator_mL          : REAL := 0.0;      (* Integrated Flush Solvent Consumed [mL] *)
    rAirVolumeAccumulator_m3        : REAL := 0.0;      (* Integrated Purge Air Consumed [m3] *)

    (* ISA-18.2 Process Alarm Trip Points, Deadbands & Timers *)
    (* Parameter 1: Bell Turbine Speed ST-101 *)
    rST_Trip_HH_rpm                 : REAL := 68000.0;  (* Turbine Critical Overspeed Limit [rpm] *)
    rST_Trip_H_rpm                  : REAL := 66000.0;  (* High Speed Warning [rpm] *)
    rST_Trip_L_rpm                  : REAL := 8000.0;   (* Low Atomization Speed Warning [rpm] *)
    rST_Trip_LL_rpm                 : REAL := 5000.0;   (* Turbine Stall / Bearing Seizure Shutdown [rpm] *)
    rST_Deadband_rpm                : REAL := 500.0;    (* Clearance Hysteresis Deadband [rpm] *)
    rST_TmrHH                       : REAL := 0.0;
    rST_TmrH                        : REAL := 0.0;
    rST_TmrL                        : REAL := 0.0;
    rST_TmrLL                       : REAL := 0.0;

    (* Parameter 2: Electrostatic High Voltage VT-201 *)
    rVT_Trip_HH_kV                  : REAL := -95.0;    (* Dielectric Flashover Danger Potential [kV] *)
    rVT_Trip_H_kV                   : REAL := -92.0;    (* High Voltage Operating Ceiling [kV] *)
    rVT_Trip_L_kV                   : REAL := -25.0;    (* Low Electrostatic Efficiency Warning [kV] *)
    rVT_Trip_LL_kV                  : REAL := -10.0;    (* Electrostatic Charge Collapse Trip [kV] *)
    rVT_Deadband_kV                 : REAL := 1.5;      (* Clearance Hysteresis Deadband [kV] *)
    rVT_TmrHH                       : REAL := 0.0;
    rVT_TmrH                        : REAL := 0.0;
    rVT_TmrL                        : REAL := 0.0;
    rVT_TmrLL                       : REAL := 0.0;

    (* Parameter 3: Micro-Gear Pump Paint Flow FT-301 *)
    rFT_Trip_HH_mlpm                : REAL := 650.0;    (* High Fluid Delivery Runaway [mL/min] *)
    rFT_Trip_H_mlpm                 : REAL := 620.0;    (* High Dosing Warning [mL/min] *)
    rFT_Trip_L_mlpm                 : REAL := 40.0;     (* Low Paint Dosing Warning [mL/min] *)
    rFT_Trip_LL_mlpm                : REAL := 20.0;     (* Paint Starvation / Dry Running Pump Trip [mL/min] *)
    rFT_Deadband_mlpm               : REAL := 5.0;      (* Clearance Hysteresis Deadband [mL/min] *)
    rFT_TmrHH                       : REAL := 0.0;
    rFT_TmrH                        : REAL := 0.0;
    rFT_TmrL                        : REAL := 0.0;
    rFT_TmrLL                       : REAL := 0.0;

    (* Parameter 4: Hydraulic Line Pressure PT-302 *)
    rPT_Line_Trip_HH_bar            : REAL := 20.0;     (* Line Overpressure Burst Disk Hazard [bar] *)
    rPT_Line_Trip_H_bar             : REAL := 16.0;     (* High Fluid Line Pressure Warning [bar] *)
    rPT_Line_Trip_L_bar             : REAL := 1.2;      (* Low Feed Line Pressure Warning [bar] *)
    rPT_Line_Trip_LL_bar            : REAL := 0.5;      (* Line Rupture / Cavitation Feed Trip [bar] *)
    rPT_Line_Deadband_bar           : REAL := 0.3;      (* Clearance Hysteresis Deadband [bar] *)
    rPT_Line_TmrHH                  : REAL := 0.0;
    rPT_Line_TmrH                   : REAL := 0.0;
    rPT_Line_TmrL                   : REAL := 0.0;
    rPT_Line_TmrLL                  : REAL := 0.0;

    (* Parameter 5: Downdraft Static Differential Pressure PT-401 *)
    rPT_Down_Trip_HH_Pa             : REAL := 22.0;     (* High Differential Overspray Grating Clog [Pa] *)
    rPT_Down_Trip_H_Pa              : REAL := 18.0;     (* High Delta-P Warning [Pa] *)
    rPT_Down_Trip_L_Pa              : REAL := 7.0;      (* Low Laminar Flow Degradation Warning [Pa] *)
    rPT_Down_Trip_LL_Pa             : REAL := 4.0;      (* Downdraft Flow Failure / Air Collapse Trip [Pa] *)
    rPT_Down_Deadband_Pa            : REAL := 0.8;      (* Clearance Hysteresis Deadband [Pa] *)
    rPT_Down_TmrHH                  : REAL := 0.0;
    rPT_Down_TmrH                   : REAL := 0.0;
    rPT_Down_TmrL                   : REAL := 0.0;
    rPT_Down_TmrLL                  : REAL := 0.0;

    (* Parameter 6: Exhaust Duct Solvent Concentration AT-601 *)
    rAT_Trip_HH_LEL_pct             : REAL := 40.0;     (* NFPA 33 Emergency Explosion Interlock Trip [%LEL] *)
    rAT_Trip_H_LEL_pct              : REAL := 25.0;     (* High Solvent Concentration Warning [%LEL] *)
    rAT_Deadband_LEL_pct            : REAL := 2.0;      (* Clearance Hysteresis Deadband [%LEL] *)
    rAT_TmrHH                       : REAL := 0.0;
    rAT_TmrH                        : REAL := 0.0;

    (* Parameter 7: RTO Core Combustion Temperature *)
    rRTO_Trip_HH_degC               : REAL := 980.0;    (* Ceramic Bed Thermal Runaway Trip [deg C] *)
    rRTO_Trip_H_degC                : REAL := 920.0;    (* Bed High Temperature Warning [deg C] *)
    rRTO_Trip_L_degC                : REAL := 760.0;    (* VOC Incomplete Destruction Warning [deg C] *)
    rRTO_Trip_LL_degC               : REAL := 720.0;    (* RTO Flame Flameout / Cold Bed Trip [deg C] *)
    rRTO_Deadband_degC              : REAL := 10.0;     (* Clearance Hysteresis Deadband [deg C] *)
    rRTO_TmrHH                      : REAL := 0.0;
    rRTO_TmrH                       : REAL := 0.0;
    rRTO_TmrL                       : REAL := 0.0;
    rRTO_TmrLL                      : REAL := 0.0;

    (* Alarm Debounce Duration Constant *)
    rAlarmDebounce_s                : REAL := 0.200;    (* 200 ms Filter Debounce for Process Alarms *)

    (* First-Out Latching Engine Variables *)
    nFirstOutCode                   : DINT := 0;        (* Latched Root Cause Diagnostic Index *)
    bFirstOutLatched                : BOOL := FALSE;    (* Single First-Out Latch Lockout Flag *)

    (* General Purpose Loop & Mathematical Iteration Indices *)
    i_idx                           : INT := 1;
    j_idx                           : INT := 1;
    k_idx                           : INT := 1;
    m_idx                           : INT := 1;
    n_iter                          : INT := 1;
    tau_step                        : INT := 0;

    (* Temporary Mathematical Real Work Registers *)
    rWork1                          : REAL := 0.0;
    rWork2                          : REAL := 0.0;
    rWork3                          : REAL := 0.0;
    rWork4                          : REAL := 0.0;
    rSum                            : REAL := 0.0;
    rSlewDelta                      : REAL := 0.0;
    rGradStep                       : REAL := 0.0;
END_VAR
"""
