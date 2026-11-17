FUNCTION_BLOCK FB_Automotive_Gigacasting_4500Ton_HPDC_RealTimeShot
(*
 * ====================================================================================================
 * LUMINA CYBER-PHYSICAL INDUSTRIAL AUTOMATION SYSTEMS ARCHITECTURE -- V7 MAX-PERSONA
 * DOMAIN: CAR MECHANICS & AUTOMOTIVE MASS PRODUCTION -- MEGA-CASTING / GIGACASTING CELL
 * SYSTEM: 4,500-TON HIGH-PRESSURE ALUMINUM DIE CASTING (HPDC) REAL-TIME SHOT INJECTION & VACUUM CELL
 * ====================================================================================================
 * Mathematical Foundations and Cyber-Physical Control Architecture:
 *   1. 4,500-Ton (44,145 kN) Clamping Unit with Acoustic Strain-Gage Tie-Bar Elongation Feedback
 *      and Hydraulic Toggle/Wedge Locking Dynamics.
 *   2. Closed-Loop Three-Stage Hydraulic Shot Injection Cylinder:
 *      - Stage 1: Wave-avoidance slow shot (0.15 - 0.45 m/s) with dynamic liquid meniscus stabilization
 *        and shot-sleeve wave height resonance suppression.
 *      - Stage 2: Ultra-high dynamic fast shot acceleration (up to 9.0 m/s in < 22 ms, 45 m/s2 acceleration)
 *        controlled via high-response servo-proportional 4-way cartridge valve with LVDT feedback.
 *      - Stage 3: Closed-loop hydraulic intensification squeeze (up to 1,200 bar hydraulic / 120 MPa metal pressure)
 *        with < 12 ms rise time and active biscuit solidification shrinkage compensation.
 *   3. Ultra-High Vacuum Real-Time Cavity Evacuation Skid:
 *      - Dual high-speed chill-vent poppet valves evacuating cavity to < 25 mbar absolute before fast-shot fill.
 *   4. Mathematical Cyber-Physical Discrete State-Space Model (6x6, Ts = 0.002s):
 *      - State Vector x[k] = [e_pos [mm], e_vel [m/s], P_head [bar], P_rod [bar], P_vac [mbar], P_metal [bar]]^T
 *      - Input Vector u[k] = [u_head [%], u_rod [%], u_accu [%], u_intens [%], u_vac [%]]^T
 *      - Output Vector y[k] = [y_pos [mm], y_head [bar], y_vac [mbar], y_clamp [kN]]^T
 *      - Innovation-corrected by 6x4 Steady-State Kalman Filter Gain Matrix L.
 *   5. Receding-Horizon Model Predictive Control (MPC):
 *      - 10 Unrolled Projected Gradient Descent (PGD) optimization iterations.
 *      - Cost function with Q (state tracking), R (actuator effort), P (terminal penalty), S (slew rate penalty).
 *      - Analytical adjoint costate backpropagation: lambda_k = A^T * lambda_{k+1} + Q * (x_k - x_ref).
 *      - Hard box limits [u_min, u_max] and maximum slew rate clamping [|du/dt| <= du_max].
 *   6. 4-Channel 2oo3 Triple Modular Redundancy (TMR) Sensor Architecture:
 *      - Channel 1: Plunger Linear Position [mm] (Sensors A, B, C)
 *      - Channel 2: Hydraulic Head Pressure [bar] (Sensors A, B, C)
 *      - Channel 3: Cavity Vacuum Pressure [mbar] (Sensors A, B, C)
 *      - Channel 4: Clamping Tie-Bar Force [kN] (Sensors A, B, C)
 *      - Pairwise discrepancy comparison, 50 ms debouncing persistence timers, and automatic bumpless
 *        fallback degradation (2oo3 -> 1oo2 -> 1oo1 -> Kalman Observer prediction fallback).
 *   7. 14-Stage Deterministic Production Finite State Machine (FSM):
 *      - Stage 0: FSM_IDLE_SAFE_DISARMED
 *      - Stage 1: FSM_DIE_LUBRICATION_AND_BLOW_CLEAN
 *      - Stage 2: FSM_DIE_CLOSE_AND_4500T_TOGGLE_LOCK
 *      - Stage 3: FSM_TIE_BAR_PRESTRESS_AND_SAFETY_LATCH
 *      - Stage 4: FSM_DOSING_FURNACE_LADLE_ALUMINUM_POUR
 *      - Stage 5: FSM_CAVITY_HIGH_VACUUM_EVACUATION
 *      - Stage 6: FSM_STAGE1_SLOW_SHOT_WAVE_AVOIDANCE
 *      - Stage 7: FSM_STAGE2_HIGH_SPEED_DYNAMIC_CAVITY_FILL
 *      - Stage 8: FSM_VP_TRANSITION_AND_DECELERATION
 *      - Stage 9: FSM_STAGE3_HYDRAULIC_INTENSIFICATION_HOLD
 *      - Stage 10: FSM_SOLIDIFICATION_COOLING_MONITOR
 *      - Stage 11: FSM_DIE_OPEN_AND_CORE_PULL_RETRACT
 *      - Stage 12: FSM_ROBOTIC_EJECTION_AND_PART_EXTRACTION
 *      - Stage 13: FSM_EMERGENCY_ABORT_AND_SAFE_PRESSURE_DUMP
 *   8. ANSI/ISA-18.2 Multi-Tier Alarms (HH, H, L, LL, hysteresis) & 32-Bit Bit-Packed Fieldbus Telemetry.
 * ====================================================================================================
 *)
VAR_INPUT
    (* --- Cell Master Control & Hardware Supervisory Signals --- *)
    bEnable : BOOL := FALSE; (* Master execution enable flag *)
    bReset : BOOL := FALSE; (* Master alarm and trip latch reset command *)
    bAutoMode : BOOL := FALSE; (* Automatic production cycle sequencing mode *)
    bStartCycle : BOOL := FALSE; (* External rising-edge pulse to initiate casting cycle *)
    bEmergencyStop_NC : BOOL := TRUE; (* Dual-channel safety loop monitor (Normally Closed: 1=OK, 0=Tripped) *)
    rCycleTime_s : REAL := 0.002; (* Deterministic PLC controller scan execution period [s] *)

    (* --- 2oo3 TMR Channel 1: Shot Plunger Linear Position Magnetostrictive Transducers --- *)
    rPlungerPos_SensorA_mm : REAL := 0.0; (* Plunger position measurement Sensor A [mm] *)
    rPlungerPos_SensorB_mm : REAL := 0.0; (* Plunger position measurement Sensor B [mm] *)
    rPlungerPos_SensorC_mm : REAL := 0.0; (* Plunger position measurement Sensor C [mm] *)

    (* --- 2oo3 TMR Channel 2: Hydraulic Injection Cylinder Head Chamber Pressure Transducers --- *)
    rHeadPress_SensorA_bar : REAL := 0.0; (* Cylinder head hydraulic pressure Sensor A [bar] *)
    rHeadPress_SensorB_bar : REAL := 0.0; (* Cylinder head hydraulic pressure Sensor B [bar] *)
    rHeadPress_SensorC_bar : REAL := 0.0; (* Cylinder head hydraulic pressure Sensor C [bar] *)

    (* --- 2oo3 TMR Channel 3: Die Cavity Absolute Vacuum Pressure Transducers --- *)
    rCavityVacuum_SensorA_mbar : REAL := 1013.25; (* Cavity vacuum absolute pressure Sensor A [mbar] *)
    rCavityVacuum_SensorB_mbar : REAL := 1013.25; (* Cavity vacuum absolute pressure Sensor B [mbar] *)
    rCavityVacuum_SensorC_mbar : REAL := 1013.25; (* Cavity vacuum absolute pressure Sensor C [mbar] *)

    (* --- 2oo3 TMR Channel 4: 4,500-Ton Clamping Mechanism Tie-Bar Acoustic Strain Transducers --- *)
    rClampForce_SensorA_kN : REAL := 0.0; (* Total tie-bar locking strain force Sensor A [kN] *)
    rClampForce_SensorB_kN : REAL := 0.0; (* Total tie-bar locking strain force Sensor B [kN] *)
    rClampForce_SensorC_kN : REAL := 0.0; (* Total tie-bar locking strain force Sensor C [kN] *)

    (* --- Hydraulic Power Unit (HPU) & Auxiliary Transducers --- *)
    rRodPress_Sensor_bar : REAL := 15.0; (* Injection cylinder rod chamber hydraulic backpressure [bar] *)
    rAccumulatorPress_bar : REAL := 295.0; (* High-pressure nitrogen piston accumulator storage bank [bar] *)
    rIntensifierPress_bar : REAL := 310.0; (* Hydraulic intensification multiplier input supply circuit [bar] *)
    rDieTemp_Fixed_degC : REAL := 210.0; (* Cover fixed die insert multi-point thermocouple average [deg C] *)
    rDieTemp_Moving_degC : REAL := 205.0; (* Ejector moving die insert multi-point thermocouple average [deg C] *)
    rHydraulicOilTemp_degC : REAL := 42.5; (* Main hydraulic reservoir mineral oil temperature [deg C] *)
    rCoolingWaterFlow_lpm : REAL := 145.0; (* Die thermal conditioning conformal channel water flow [l/min] *)
    rCoolingWaterTemp_degC : REAL := 28.0; (* Die thermal conditioning water supply temperature [deg C] *)
    rMoltenMetalTemp_degC : REAL := 695.0; (* Holding furnace molten AlSi10MnMg alloy pouring temperature [deg C] *)
    rDosingLadleWeight_kg : REAL := 38.5; (* Automated robotic dosing ladle molten aluminum charge mass [kg] *)
    rBiscuitThickness_mm : REAL := 35.0; (* Residual injection solidified biscuit thickness sensor [mm] *)

    (* --- Cell Safety, Interlock & External Automation Status --- *)
    bSafetyGateClosed : BOOL := TRUE; (* Safety perimeter perimeter light-curtains and safety door locked *)
    bRobotExtractorReady : BOOL := TRUE; (* 6-Axis heavy part extraction robot in home waiting position *)
    bDieSprayComplete : BOOL := TRUE; (* Robotic servo electrostatic mold lube spray cycle finished *)
    bVacuumPumpRunning : BOOL := TRUE; (* Vacuum skid dual roots booster and rotary vane pumps energized *)
    bHydraulicPumpsRunning : BOOL := TRUE; (* Main variable-displacement axial piston pumps energized *)
    bNitrogenBottleBankOK : BOOL := TRUE; (* Nitrogen pre-charge accumulator bottle pressure healthy *)

    (* --- Motion & Process Dynamic Trajectory Setpoints --- *)
    rStage1_TargetVel_mps : REAL := 0.28; (* Stage 1 slow-shot wave avoidance velocity setpoint [m/s] *)
    rStage2_TargetVel_mps : REAL := 7.50; (* Stage 2 fast-shot dynamic cavity fill velocity setpoint [m/s] *)
    rStage3_TargetPress_bar : REAL := 1150.0; (* Stage 3 intensification final metal squeeze pressure setpoint [bar] *)
    rV_P_TransferPos_mm : REAL := 820.0; (* Velocity-to-pressure (V/P) transition switchover position [mm] *)
    rVacuumTarget_mbar : REAL := 25.0; (* Minimum required cavity vacuum level to permit fast-shot trigger [mbar] *)
    rClampForce_Setpoint_kN : REAL := 44145.0; (* Nominal 4,500-metric-ton locking clamp force setpoint [kN] *)
    rSleeveFillPercentage_pct : REAL := 65.0; (* Volumetric molten aluminum shot-sleeve filling ratio [%] *)
    rTMR_Discrepancy_Limit_s : REAL := 0.050; (* Maximum persistence time for 2oo3 sensor discrepancy [s] *)
    rAlpha_PGD_StepSize : REAL := 0.015; (* Projected Gradient Descent optimization descent step size *)
END_VAR

VAR_OUTPUT
    (* --- Cell Supervisory & Cycle State Outputs --- *)
    bSystemReady : BOOL := FALSE; (* Gigacasting cell primed, locked and armed for cycle initiation *)
    bCycleActive : BOOL := FALSE; (* Real-time die casting injection shot cycle actively executing *)
    bCycleComplete : BOOL := FALSE; (* Gigacasting sequence fully executed and parts ejected *)
    bGeneralFault : BOOL := FALSE; (* Master fault latch indicating critical cell trip *)
    bEmergencyStopActive : BOOL := FALSE; (* Emergency stop circuit tripped state *)
    iCurrentState : INT := 0; (* Active 14-stage FSM state index (0 to 13) *)
    iPreviousState : INT := 0; (* Prior 14-stage FSM state index *)

    (* --- Hydraulic & Vacuum Actuator Physical Command Outputs --- *)
    rServoValve_HeadSpool_cmd : REAL := 0.0; (* High-dynamic fast-shot proportional valve spool command [%] (-100..+100) *)
    rServoValve_RodSpool_cmd : REAL := 0.0; (* Rod backpressure proportional servo-valve command [%] (0..100) *)
    rAccuBoosterValve_cmd : REAL := 0.0; (* High-flow accumulator booster discharge poppet valve [%] (0..100) *)
    rIntensifierValve_cmd : REAL := 0.0; (* Hydraulic intensification multiplier cartridge pilot [%] (0..100) *)
    rVacuumPoppetValve_cmd : REAL := 0.0; (* Chill-vent high-vacuum cavity isolation poppet command [%] (0..100) *)
    rDieClampValve_cmd : REAL := 0.0; (* 4,500-ton toggle lockup proportional hydraulic valve command [%] (0..100) *)
    bEjectorForward_cmd : BOOL := FALSE; (* Hydraulic part ejector pin cylinder forward actuation *)
    bEjectorRetract_cmd : BOOL := FALSE; (* Hydraulic part ejector pin cylinder retract actuation *)
    bCorePull1_Extend_cmd : BOOL := FALSE; (* Heavy hydraulic side-core slide 1 extend command *)
    bCorePull1_Retract_cmd : BOOL := FALSE; (* Heavy hydraulic side-core slide 1 retract command *)
    bCorePull2_Extend_cmd : BOOL := FALSE; (* Heavy hydraulic side-core slide 2 extend command *)
    bCorePull2_Retract_cmd : BOOL := FALSE; (* Heavy hydraulic side-core slide 2 retract command *)
    bVacuumDumpValve_cmd : BOOL := FALSE; (* Vacuum vent break atmospheric release valve solenoid command *)

    (* --- Validated & Filtered Voted Physical Feedback Signals --- *)
    rVoted_PlungerPos_mm : REAL := 0.0; (* 2oo3 TMR validated shot plunger linear position [mm] *)
    rVoted_PlungerVel_mps : REAL := 0.0; (* Validated and filtered shot plunger velocity [m/s] *)
    rVoted_HeadPress_bar : REAL := 0.0; (* 2oo3 TMR validated cylinder head injection hydraulic pressure [bar] *)
    rVoted_CavityVacuum_mbar : REAL := 1013.25; (* 2oo3 TMR validated die cavity absolute vacuum pressure [mbar] *)
    rVoted_ClampForce_kN : REAL := 0.0; (* 2oo3 TMR validated 4,500-ton tie-bar total clamping force [kN] *)
    rEstimated_MetalPress_bar : REAL := 0.0; (* Cyber-physical Kalman observer estimated molten metal pressure [bar] *)
    rEstimated_CavityResistance_bar : REAL := 0.0; (* Observer estimated flow front solidification dynamic drag [bar] *)

    (* --- Gigacasting Cycle Diagnostic & Quality Metrics --- *)
    rFillTime_ms : REAL := 0.0; (* Measured Stage 2 high-speed cavity fill duration [ms] *)
    rIntensificationRiseTime_ms : REAL := 0.0; (* Measured Stage 3 hydraulic pressure build rise time [ms] *)
    rPeakIntensificationPress_bar : REAL := 0.0; (* Maximum dynamic squeeze pressure recorded during holding [bar] *)
    rCycleDuration_s : REAL := 0.0; (* Total elapsed execution time of the active gigacasting cycle [s] *)
    rMaxPlungerVel_mps : REAL := 0.0; (* Maximum plunger speed attained during fast-shot injection [m/s] *)
    rFinalBiscuitThickness_mm : REAL := 0.0; (* Measured residual solidified aluminum biscuit thickness [mm] *)

    (* --- Bit-Packed Telemetry & ISA-18.2 Fieldbus Registers --- *)
    udiStatusWord1 : DWORD := 16#00000000; (* Cell state, operating modes, and safety interlocks status word *)
    udiStatusWord2 : DWORD := 16#00000000; (* Hydraulic valves, accumulators, and vacuum physical hardware status word *)
    udiStatusWord3 : DWORD := 16#00000000; (* TMR sensor health, discrepancy states, and observer fallback status word *)
    udiAlarmWord_ISA_HH : DWORD := 16#00000000; (* ANSI/ISA-18.2 High-High Emergency Alarm Bit Register *)
    udiAlarmWord_ISA_H : DWORD := 16#00000000; (* ANSI/ISA-18.2 High Warning Alarm Bit Register *)
    udiAlarmWord_ISA_L : DWORD := 16#00000000; (* ANSI/ISA-18.2 Low Warning Alarm Bit Register *)
    udiAlarmWord_ISA_LL : DWORD := 16#00000000; (* ANSI/ISA-18.2 Low-Low Emergency Alarm Bit Register *)
END_VAR

VAR
    (* ==================================================================================================== *)
    (* INTERNAL DISCRETE STATE-SPACE CYBER-PHYSICAL MATRICES (6x6 Model, Ts = 0.002s)                       *)
    (* States x: [1: e_pos [mm], 2: e_vel [m/s], 3: P_head [bar], 4: P_rod [bar], 5: P_vac [mbar], 6: P_met [bar]] *)
    (* Inputs u: [1: u_head [%], 2: u_rod [%], 3: u_accu [%], 4: u_intens [%], 5: u_vac [%]]                *)
    (* Meas   y: [1: y_pos [mm], 2: y_head [bar], 3: y_vac [mbar], 4: y_clamp [kN]]                       *)
    (* ==================================================================================================== *)
    rA_Mat : ARRAY[1..6, 1..6] OF REAL := [
        (* Row 1: e_pos dynamic propagation *)
        0.984250, 0.001968, 0.000142, -0.000098, 0.000000, -0.000185,
        (* Row 2: e_vel acceleration and hydraulic balance *)
        -0.015240, 0.968500, 0.048210, -0.034520, 0.000000, -0.052140,
        (* Row 3: P_head hydraulic bulk modulus and valve flow dynamics *)
        0.000000, -0.428500, 0.912400, 0.000000, 0.000000, -0.018500,
        (* Row 4: P_rod backpressure hydraulic damping dynamics *)
        0.000000, 0.285400, 0.000000, 0.924500, 0.000000, 0.000000,
        (* Row 5: P_vac cavity vacuum conductance and leakage *)
        0.000000, 0.000000, 0.000000, 0.000000, 0.941200, 0.000000,
        (* Row 6: P_met molten alloy solidification dynamic resistance *)
        0.000000, 0.354100, 0.012400, 0.000000, 0.000000, 0.887500
    ];

    rB_Mat : ARRAY[1..6, 1..5] OF REAL := [
        (* Row 1: e_pos control sensitivity *)
        0.000215, -0.000142, 0.000184, 0.000000, 0.000000,
        (* Row 2: e_vel acceleration sensitivity *)
        0.084520, -0.054210, 0.068410, 0.000000, 0.000000,
        (* Row 3: P_head pressure buildup sensitivity *)
        1.245800, 0.000000, 0.845200, 1.845000, 0.000000,
        (* Row 4: P_rod backpressure throttling sensitivity *)
        0.000000, 0.942100, 0.000000, 0.000000, 0.000000,
        (* Row 5: P_vac vacuum evacuation pumping sensitivity *)
        0.000000, 0.000000, 0.000000, 0.000000, -2.485000,
        (* Row 6: P_met intensification pressure sensitivity *)
        0.185200, 0.000000, 0.124500, 2.458000, 0.000000
    ];

    rC_Mat : ARRAY[1..4, 1..6] OF REAL := [
        (* Output 1: y_pos measurement map *)
        1.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000,
        (* Output 2: y_head pressure measurement map *)
        0.000000, 0.000000, 1.000000, 0.000000, 0.000000, 0.000000,
        (* Output 3: y_vac vacuum measurement map *)
        0.000000, 0.000000, 0.000000, 0.000000, 1.000000, 0.000000,
        (* Output 4: y_clamp force reaction map *)
        0.000000, 0.000000, 12.450000, 0.000000, 0.000000, 24.850000
    ];

    rD_Mat : ARRAY[1..4, 1..5] OF REAL := [
        0.000000, 0.000000, 0.000000, 0.000000, 0.000000,
        0.000000, 0.000000, 0.000000, 0.000000, 0.000000,
        0.000000, 0.000000, 0.000000, 0.000000, 0.000000,
        0.000000, 0.000000, 0.000000, 0.000000, 0.000000
    ];

    rL_Mat : ARRAY[1..6, 1..4] OF REAL := [
        (* Luenberger / Steady-State Kalman Filter Innovation Gain Matrix L (6x4) *)
        (* Row 1: Correction to e_pos *)
        0.245800, 0.000124, 0.000000, 0.000015,
        (* Row 2: Correction to e_vel *)
        0.185400, 0.001452, 0.000000, 0.000084,
        (* Row 3: Correction to P_head *)
        0.002450, 0.312500, 0.000000, 0.004210,
        (* Row 4: Correction to P_rod *)
        -0.001240, 0.048500, 0.000000, -0.000840,
        (* Row 5: Correction to P_vac *)
        0.000000, 0.000000, 0.428500, 0.000000,
        (* Row 6: Correction to P_met *)
        0.004850, 0.084500, 0.000000, 0.018500
    ];

    (* --- Kalman Observer Dynamic State Vectors --- *)
    a_x_hat : ARRAY[1..6] OF REAL := [6(0.0)]; (* Posterior state estimate vector x_hat[k|k] *)
    a_x_pred : ARRAY[1..6] OF REAL := [6(0.0)]; (* Prior predicted state vector x_hat[k|k-1] *)
    a_y_pred : ARRAY[1..4] OF REAL := [4(0.0)]; (* Predicted measurement vector y_hat[k] *)
    a_y_meas : ARRAY[1..4] OF REAL := [4(0.0)]; (* Voted physical measurement vector y[k] *)
    a_innov : ARRAY[1..4] OF REAL := [4(0.0)]; (* Innovation residual vector y - y_hat *)
    a_u_act : ARRAY[1..5] OF REAL := [5(0.0)]; (* Current cycle actuator command vector u[k] *)
    a_u_prev : ARRAY[1..5] OF REAL := [5(0.0)]; (* Previous cycle actuator command vector u[k-1] *)
    bObserverInitialized : BOOL := FALSE; (* Observer warm-start initialization flag *)

    (* ==================================================================================================== *)
    (* RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) MATRICES & BUFFER STRUCTURES                        *)
    (* Horizons: Prediction Hp = 5 steps (10 ms), Control Hu = 3 steps (6 ms), PGD Iterations = 10         *)
    (* ==================================================================================================== *)
    rQ_Diag : ARRAY[1..6] OF REAL := [
        (* Penalty weights on state errors: e_pos, e_vel, P_head, P_rod, P_vac, P_met *)
        45.0, 120.0, 0.85, 0.45, 2.50, 1.80
    ];
    rR_Diag : ARRAY[1..5] OF REAL := [
        (* Penalty weights on actuator commands: u_head, u_rod, u_accu, u_intens, u_vac *)
        0.12, 0.08, 0.15, 0.22, 0.05
    ];
    rP_Diag : ARRAY[1..6] OF REAL := [
        (* Terminal penalty weights on final prediction horizon state *)
        95.0, 240.0, 1.50, 0.90, 5.00, 3.60
    ];
    rS_Diag : ARRAY[1..5] OF REAL := [
        (* Penalty weights on actuator slew rates (du/dt) *)
        0.85, 0.50, 1.20, 1.50, 0.25
    ];
    rU_BoxMin : ARRAY[1..5] OF REAL := [-100.0, 0.0, 0.0, 0.0, 0.0]; (* Lower actuator box limits *)
    rU_BoxMax : ARRAY[1..5] OF REAL := [100.0, 100.0, 100.0, 100.0, 100.0]; (* Upper actuator box limits *)
    rDeltaU_Max : ARRAY[1..5] OF REAL := [18.0, 15.0, 25.0, 30.0, 50.0]; (* Maximum slew limit per cycle [%] *)

    rX_Pred_Horizon : ARRAY[1..5, 1..6] OF REAL; (* Forward predicted state trajectory across Hp=5 *)
    rLambda_Costate : ARRAY[1..5, 1..6] OF REAL; (* Adjoint backward costate trajectory across Hp=5 *)
    rU_Opt_Seq : ARRAY[1..3, 1..5] OF REAL; (* Control input trajectory across Hu=3 *)
    rGrad_J : ARRAY[1..3, 1..5] OF REAL; (* Analytical gradient trajectory w.r.t. control inputs *)
    rX_Target : ARRAY[1..5, 1..6] OF REAL; (* Time-varying state reference trajectory across Hp=5 *)

    (* --- MPC Iteration & Convergence Tracking Registers --- *)
    iPGD_IterCount : INT := 0; (* Active PGD iteration loop counter *)
    rMPC_Cost_J : REAL := 0.0; (* Evaluated quadratic objective cost J *)
    rMPC_Cost_J_Prev : REAL := 0.0; (* Cost J evaluated at previous PGD iteration *)
    rMPC_GradNormSq : REAL := 0.0; (* Squared Euclidean norm of analytical gradient *)
    rMPC_SlewResidual : REAL := 0.0; (* Total slew constraint projection residual *)
    bMPC_Converged : BOOL := FALSE; (* Convergence flag for PGD optimization *)

    (* ==================================================================================================== *)
    (* 4-CHANNEL 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) INTERNAL STRUCTURES & TIMERS                          *)
    (* Channels: 1=Plunger Position [mm], 2=Head Pressure [bar], 3=Cavity Vac [mbar], 4=Clamp Force [kN]   *)
    (* ==================================================================================================== *)
    (* --- TMR Channel 1 Variables (Plunger Position [mm]) --- *)
    rTMR_Ch1_ValA : REAL := 0.0;
    rTMR_Ch1_ValB : REAL := 0.0;
    rTMR_Ch1_ValC : REAL := 0.0;
    rTMR_Ch1_DiffAB : REAL := 0.0;
    rTMR_Ch1_DiffBC : REAL := 0.0;
    rTMR_Ch1_DiffCA : REAL := 0.0;
    rTMR_Ch1_Tol : REAL := 0.85; (* Discrepancy threshold [mm] *)
    bTMR_Ch1_DiscAB : BOOL := FALSE;
    bTMR_Ch1_DiscBC : BOOL := FALSE;
    bTMR_Ch1_DiscCA : BOOL := FALSE;
    rTMR_Ch1_TimerAB_s : REAL := 0.0;
    rTMR_Ch1_TimerBC_s : REAL := 0.0;
    rTMR_Ch1_TimerCA_s : REAL := 0.0;
    bTMR_Ch1_FaultA : BOOL := FALSE;
    bTMR_Ch1_FaultB : BOOL := FALSE;
    bTMR_Ch1_FaultC : BOOL := FALSE;
    iTMR_Ch1_DegradationState : INT := 3; (* 3=2oo3, 2=1oo2, 1=1oo1, 0=Observer Fallback *)
    rTMR_Ch1_VotedRaw : REAL := 0.0;
    rTMR_Ch1_VotedFilt : REAL := 0.0;
    rTMR_Ch1_VotedPrev : REAL := 0.0;

    (* --- TMR Channel 2 Variables (Head Injection Pressure [bar]) --- *)
    rTMR_Ch2_ValA : REAL := 0.0;
    rTMR_Ch2_ValB : REAL := 0.0;
    rTMR_Ch2_ValC : REAL := 0.0;
    rTMR_Ch2_DiffAB : REAL := 0.0;
    rTMR_Ch2_DiffBC : REAL := 0.0;
    rTMR_Ch2_DiffCA : REAL := 0.0;
    rTMR_Ch2_Tol : REAL := 15.0; (* Discrepancy threshold [bar] *)
    bTMR_Ch2_DiscAB : BOOL := FALSE;
    bTMR_Ch2_DiscBC : BOOL := FALSE;
    bTMR_Ch2_DiscCA : BOOL := FALSE;
    rTMR_Ch2_TimerAB_s : REAL := 0.0;
    rTMR_Ch2_TimerBC_s : REAL := 0.0;
    rTMR_Ch2_TimerCA_s : REAL := 0.0;
    bTMR_Ch2_FaultA : BOOL := FALSE;
    bTMR_Ch2_FaultB : BOOL := FALSE;
    bTMR_Ch2_FaultC : BOOL := FALSE;
    iTMR_Ch2_DegradationState : INT := 3; (* 3=2oo3, 2=1oo2, 1=1oo1, 0=Observer Fallback *)
    rTMR_Ch2_VotedRaw : REAL := 0.0;
    rTMR_Ch2_VotedFilt : REAL := 0.0;
    rTMR_Ch2_VotedPrev : REAL := 0.0;

    (* --- TMR Channel 3 Variables (Cavity Vacuum Pressure [mbar]) --- *)
    rTMR_Ch3_ValA : REAL := 1013.25;
    rTMR_Ch3_ValB : REAL := 1013.25;
    rTMR_Ch3_ValC : REAL := 1013.25;
    rTMR_Ch3_DiffAB : REAL := 0.0;
    rTMR_Ch3_DiffBC : REAL := 0.0;
    rTMR_Ch3_DiffCA : REAL := 0.0;
    rTMR_Ch3_Tol : REAL := 5.0; (* Discrepancy threshold [mbar] *)
    bTMR_Ch3_DiscAB : BOOL := FALSE;
    bTMR_Ch3_DiscBC : BOOL := FALSE;
    bTMR_Ch3_DiscCA : BOOL := FALSE;
    rTMR_Ch3_TimerAB_s : REAL := 0.0;
    rTMR_Ch3_TimerBC_s : REAL := 0.0;
    rTMR_Ch3_TimerCA_s : REAL := 0.0;
    bTMR_Ch3_FaultA : BOOL := FALSE;
    bTMR_Ch3_FaultB : BOOL := FALSE;
    bTMR_Ch3_FaultC : BOOL := FALSE;
    iTMR_Ch3_DegradationState : INT := 3; (* 3=2oo3, 2=1oo2, 1=1oo1, 0=Observer Fallback *)
    rTMR_Ch3_VotedRaw : REAL := 1013.25;
    rTMR_Ch3_VotedFilt : REAL := 1013.25;
    rTMR_Ch3_VotedPrev : REAL := 1013.25;

    (* --- TMR Channel 4 Variables (Tie-Bar Clamping Force [kN]) --- *)
    rTMR_Ch4_ValA : REAL := 0.0;
    rTMR_Ch4_ValB : REAL := 0.0;
    rTMR_Ch4_ValC : REAL := 0.0;
    rTMR_Ch4_DiffAB : REAL := 0.0;
    rTMR_Ch4_DiffBC : REAL := 0.0;
    rTMR_Ch4_DiffCA : REAL := 0.0;
    rTMR_Ch4_Tol : REAL := 450.0; (* Discrepancy threshold [kN] *)
    bTMR_Ch4_DiscAB : BOOL := FALSE;
    bTMR_Ch4_DiscBC : BOOL := FALSE;
    bTMR_Ch4_DiscCA : BOOL := FALSE;
    rTMR_Ch4_TimerAB_s : REAL := 0.0;
    rTMR_Ch4_TimerBC_s : REAL := 0.0;
    rTMR_Ch4_TimerCA_s : REAL := 0.0;
    bTMR_Ch4_FaultA : BOOL := FALSE;
    bTMR_Ch4_FaultB : BOOL := FALSE;
    bTMR_Ch4_FaultC : BOOL := FALSE;
    iTMR_Ch4_DegradationState : INT := 3; (* 3=2oo3, 2=1oo2, 1=1oo1, 0=Observer Fallback *)
    rTMR_Ch4_VotedRaw : REAL := 0.0;
    rTMR_Ch4_VotedFilt : REAL := 0.0;
    rTMR_Ch4_VotedPrev : REAL := 0.0;

    (* ==================================================================================================== *)
    (* 14-STAGE DETERMINISTIC PRODUCTION FINITE STATE MACHINE (FSM) INTERNAL REGISTERS                    *)
    (* ==================================================================================================== *)
    iState : INT := 0; (* Current state index (0 to 13) *)
    iPrevState : INT := 0; (* Previous scan cycle state index *)
    bStateFirstScan : BOOL := TRUE; (* One-shot pulse active during first scan of new state *)
    rStateTimer_s : REAL := 0.0; (* Elapsed dwell timer in active state [s] *)
    rCycleTimer_s : REAL := 0.0; (* Total continuous casting cycle timer [s] *)
    rStageTimeout_s : REAL := 25.0; (* Watchdog safety timeout for current stage [s] *)
    rShotStartTime_s : REAL := 0.0; (* System timestamp at shot initiation [s] *)
    rFillStartTime_s : REAL := 0.0; (* System timestamp at Stage 2 fast-shot start [s] *)
    rIntensifyStartTime_s : REAL := 0.0; (* System timestamp at Stage 3 intensification start [s] *)
    bIntensificationLatching : BOOL := FALSE; (* Latching flag for Stage 3 intensification trigger *)
    bBiscuitDetected : BOOL := FALSE; (* Solidified biscuit position threshold detected *)
    rBiscuitCutoffPos_mm : REAL := 0.0; (* Measured stroke position at solidification cutoff [mm] *)
    bEjectionComplete : BOOL := FALSE; (* Part ejection stroke and robot confirmation flag *)
    rSolidificationDwellTimer_s : REAL := 0.0; (* In-mold metal freezing dwell timer [s] *)
    rSolidificationRequired_s : REAL := 12.5; (* Nominal solidification freeze time required [s] *)

    (* ==================================================================================================== *)
    (* ANSI/ISA-18.2 MULTI-TIER ALARM MANAGEMENT INTERNAL DATA STRUCTURES (10 Process Variables)           *)
    (* PVs: 1:Speed, 2:HeadP, 3:Vac, 4:ClampF, 5:DieTemp, 6:OilTemp, 7:WaterFlow, 8:MetalP, 9:PourTemp, 10:CycleT *)
    (* ==================================================================================================== *)
    rPV_Val : ARRAY[1..10] OF REAL; (* Process Variable current values *)
    rPV_HH_Limit : ARRAY[1..10] OF REAL := [9.50, 320.0, 150.0, 48000.0, 280.0, 65.0, 250.0, 1400.0, 750.0, 95.0];
    rPV_H_Limit  : ARRAY[1..10] OF REAL := [8.80, 280.0, 60.0,  46000.0, 250.0, 55.0, 200.0, 1250.0, 725.0, 75.0];
    rPV_L_Limit  : ARRAY[1..10] OF REAL := [0.10, 50.0,  0.0,   40000.0, 160.0, 30.0, 80.0,  950.0,  660.0, 0.0];
    rPV_LL_Limit : ARRAY[1..10] OF REAL := [0.05, 20.0,  0.0,   36000.0, 130.0, 20.0, 50.0,  800.0,  635.0, 0.0];
    rPV_Hysteresis : ARRAY[1..10] OF REAL := [0.15, 8.0, 3.0, 300.0, 5.0, 2.0, 8.0, 25.0, 5.0, 1.0];
    rAlarmDelay_Timer_HH : ARRAY[1..10] OF REAL := [10(0.0)];
    rAlarmDelay_Timer_H  : ARRAY[1..10] OF REAL := [10(0.0)];
    rAlarmDelay_Timer_L  : ARRAY[1..10] OF REAL := [10(0.0)];
    rAlarmDelay_Timer_LL : ARRAY[1..10] OF REAL := [10(0.0)];
    rAlarmDelay_Limit_s  : ARRAY[1..10] OF REAL := [0.010, 0.020, 0.050, 0.050, 0.500, 1.000, 0.500, 0.015, 0.500, 0.500];
    bAlarmActive_HH : ARRAY[1..10] OF BOOL := [10(FALSE)];
    bAlarmActive_H  : ARRAY[1..10] OF BOOL := [10(FALSE)];
    bAlarmActive_L  : ARRAY[1..10] OF BOOL := [10(FALSE)];
    bAlarmActive_LL : ARRAY[1..10] OF BOOL := [10(FALSE)];
    bAlarmLatched_HH : ARRAY[1..10] OF BOOL := [10(FALSE)];
    bAlarmLatched_H  : ARRAY[1..10] OF BOOL := [10(FALSE)];
    bAlarmLatched_L  : ARRAY[1..10] OF BOOL := [10(FALSE)];
    bAlarmLatched_LL : ARRAY[1..10] OF BOOL := [10(FALSE)];
    bAlarmAck : ARRAY[1..10] OF BOOL := [10(FALSE)];

    (* --- General Scratchpad, Iteration & Mathematical Helper Variables --- *)
    i_idx : INT := 1; (* Primary loop iterator *)
    j_idx : INT := 1; (* Secondary loop iterator *)
    k_idx : INT := 1; (* Tertiary loop iterator *)
    m_iter : INT := 1; (* Optimization iteration iterator *)
    h_step : INT := 1; (* MPC horizon prediction step iterator *)
    rSum_Acc : REAL := 0.0; (* Mathematical accumulator register *)
    rTemp_Val : REAL := 0.0; (* Scratchpad floating-point register *)
    rDiff_Temp : REAL := 0.0; (* Scratchpad difference register *)
    rFilter_Alpha : REAL := 0.15; (* Exponential moving average smoothing factor *)
    rDifferentiated_Vel_Raw : REAL := 0.0; (* Finite-difference raw velocity *)
    bFirstScan : BOOL := TRUE; (* Block first-scan initialization pulse *)
END_VAR


(* ==================================================================================================== *)
(* PHASE 0: REAL-TIME TASK SUPERVISION, INITIALIZATION & FIRST SCAN ARMED PREPARATION                  *)
(* ==================================================================================================== *)
IF bFirstScan THEN
    (* Initialize filter memory and previous states *)
    rTMR_Ch1_VotedPrev := rPlungerPos_SensorA_mm;
    rTMR_Ch2_VotedPrev := rHeadPress_SensorA_bar;
    rTMR_Ch3_VotedPrev := rCavityVacuum_SensorA_mbar;
    rTMR_Ch4_VotedPrev := rClampForce_SensorA_kN;
    rVoted_PlungerPos_mm := rPlungerPos_SensorA_mm;
    rVoted_HeadPress_bar := rHeadPress_SensorA_bar;
    rVoted_CavityVacuum_mbar := rCavityVacuum_SensorA_mbar;
    rVoted_ClampForce_kN := rClampForce_SensorA_kN;
    rVoted_PlungerVel_mps := 0.0;
    a_x_hat[1] := 0.0; (* Plunger position error initialized to zero *)
    a_x_hat[2] := 0.0; (* Plunger velocity error initialized to zero *)
    a_x_hat[3] := rHeadPress_SensorA_bar;
    a_x_hat[4] := rRodPress_Sensor_bar;
    a_x_hat[5] := rCavityVacuum_SensorA_mbar;
    a_x_hat[6] := 0.0; (* Molten metal initial counter-pressure *)
    bObserverInitialized := TRUE;
    bFirstScan := FALSE;
END_IF;

(* Reset logic for sensor fault latches *)
IF bReset THEN
    bTMR_Ch1_FaultA := FALSE;
    bTMR_Ch1_FaultB := FALSE;
    bTMR_Ch1_FaultC := FALSE;
    rTMR_Ch1_TimerAB_s := 0.0;
    rTMR_Ch1_TimerBC_s := 0.0;
    rTMR_Ch1_TimerCA_s := 0.0;
    bTMR_Ch2_FaultA := FALSE;
    bTMR_Ch2_FaultB := FALSE;
    bTMR_Ch2_FaultC := FALSE;
    rTMR_Ch2_TimerAB_s := 0.0;
    rTMR_Ch2_TimerBC_s := 0.0;
    rTMR_Ch2_TimerCA_s := 0.0;
    bTMR_Ch3_FaultA := FALSE;
    bTMR_Ch3_FaultB := FALSE;
    bTMR_Ch3_FaultC := FALSE;
    rTMR_Ch3_TimerAB_s := 0.0;
    rTMR_Ch3_TimerBC_s := 0.0;
    rTMR_Ch3_TimerCA_s := 0.0;
    bTMR_Ch4_FaultA := FALSE;
    bTMR_Ch4_FaultB := FALSE;
    bTMR_Ch4_FaultC := FALSE;
    rTMR_Ch4_TimerAB_s := 0.0;
    rTMR_Ch4_TimerBC_s := 0.0;
    rTMR_Ch4_TimerCA_s := 0.0;
    bGeneralFault := FALSE;
END_IF;

(* ==================================================================================================== *)
(* PHASE 1: 4-CHANNEL 2oo3 TMR SENSOR VOTING WITH DISCREPANCY TIMERS & BUMPLESS DEGRADATION            *)
(* ==================================================================================================== *)
(* -------------------------------------------------------------------------------------------------- *)
(* TMR CHANNEL Ch1: Plunger Linear Position Transducers [mm] *)
(* -------------------------------------------------------------------------------------------------- *)
rTMR_Ch1_ValA := rPlungerPos_SensorA_mm;
rTMR_Ch1_ValB := rPlungerPos_SensorB_mm;
rTMR_Ch1_ValC := rPlungerPos_SensorC_mm;

(* Calculate pairwise absolute deviation deltas *)
rTMR_Ch1_DiffAB := ABS(rTMR_Ch1_ValA - rTMR_Ch1_ValB);
rTMR_Ch1_DiffBC := ABS(rTMR_Ch1_ValB - rTMR_Ch1_ValC);
rTMR_Ch1_DiffCA := ABS(rTMR_Ch1_ValC - rTMR_Ch1_ValA);

(* Instantaneous discrepancy evaluation *)
rTMR_Ch1_DiscAB := (rTMR_Ch1_DiffAB > rTMR_Ch1_Tol);
rTMR_Ch1_DiscBC := (rTMR_Ch1_DiffBC > rTMR_Ch1_Tol);
rTMR_Ch1_DiscCA := (rTMR_Ch1_DiffCA > rTMR_Ch1_Tol);

(* Discrepancy integration debounce timer for Pair A-B *)
IF rTMR_Ch1_DiscAB THEN
    rTMR_Ch1_TimerAB_s := rTMR_Ch1_TimerAB_s + rCycleTime_s;
    IF rTMR_Ch1_TimerAB_s >= rTMR_Discrepancy_Limit_s THEN
        rTMR_Ch1_TimerAB_s := rTMR_Discrepancy_Limit_s;
    END_IF;
ELSE
    IF rTMR_Ch1_TimerAB_s > 0.0 THEN
        rTMR_Ch1_TimerAB_s := rTMR_Ch1_TimerAB_s - (rCycleTime_s * 2.0);
        IF rTMR_Ch1_TimerAB_s < 0.0 THEN
            rTMR_Ch1_TimerAB_s := 0.0;
        END_IF;
    END_IF;
END_IF;

(* Discrepancy integration debounce timer for Pair B-C *)
IF rTMR_Ch1_DiscBC THEN
    rTMR_Ch1_TimerBC_s := rTMR_Ch1_TimerBC_s + rCycleTime_s;
    IF rTMR_Ch1_TimerBC_s >= rTMR_Discrepancy_Limit_s THEN
        rTMR_Ch1_TimerBC_s := rTMR_Discrepancy_Limit_s;
    END_IF;
ELSE
    IF rTMR_Ch1_TimerBC_s > 0.0 THEN
        rTMR_Ch1_TimerBC_s := rTMR_Ch1_TimerBC_s - (rCycleTime_s * 2.0);
        IF rTMR_Ch1_TimerBC_s < 0.0 THEN
            rTMR_Ch1_TimerBC_s := 0.0;
        END_IF;
    END_IF;
END_IF;

(* Discrepancy integration debounce timer for Pair C-A *)
IF rTMR_Ch1_DiscCA THEN
    rTMR_Ch1_TimerCA_s := rTMR_Ch1_TimerCA_s + rCycleTime_s;
    IF rTMR_Ch1_TimerCA_s >= rTMR_Discrepancy_Limit_s THEN
        rTMR_Ch1_TimerCA_s := rTMR_Discrepancy_Limit_s;
    END_IF;
ELSE
    IF rTMR_Ch1_TimerCA_s > 0.0 THEN
        rTMR_Ch1_TimerCA_s := rTMR_Ch1_TimerCA_s - (rCycleTime_s * 2.0);
        IF rTMR_Ch1_TimerCA_s < 0.0 THEN
            rTMR_Ch1_TimerCA_s := 0.0;
        END_IF;
    END_IF;
END_IF;

(* Sensor Isolation: A sensor is faulted if both of its pairs persist in discrepancy *)
IF (rTMR_Ch1_TimerAB_s >= rTMR_Discrepancy_Limit_s) AND (rTMR_Ch1_TimerCA_s >= rTMR_Discrepancy_Limit_s) THEN
    rTMR_Ch1_FaultA := TRUE;
END_IF;
IF (rTMR_Ch1_TimerAB_s >= rTMR_Discrepancy_Limit_s) AND (rTMR_Ch1_TimerBC_s >= rTMR_Discrepancy_Limit_s) THEN
    rTMR_Ch1_FaultB := TRUE;
END_IF;
IF (rTMR_Ch1_TimerBC_s >= rTMR_Discrepancy_Limit_s) AND (rTMR_Ch1_TimerCA_s >= rTMR_Discrepancy_Limit_s) THEN
    rTMR_Ch1_FaultC := TRUE;
END_IF;

(* Degradation Logic & Voted Value Selection *)
IF (NOT rTMR_Ch1_FaultA) AND (NOT rTMR_Ch1_FaultB) AND (NOT rTMR_Ch1_FaultC) THEN
    (* Nominal 2oo3 State: All 3 sensors healthy -> Median Selection *)
    rTMR_Ch1_DegradationState := 3;
    IF ((rTMR_Ch1_ValA >= rTMR_Ch1_ValB) AND (rTMR_Ch1_ValA <= rTMR_Ch1_ValC)) OR ((rTMR_Ch1_ValA >= rTMR_Ch1_ValC) AND (rTMR_Ch1_ValA <= rTMR_Ch1_ValB)) THEN
        rTMR_Ch1_VotedRaw := rTMR_Ch1_ValA;
    ELSIF ((rTMR_Ch1_ValB >= rTMR_Ch1_ValA) AND (rTMR_Ch1_ValB <= rTMR_Ch1_ValC)) OR ((rTMR_Ch1_ValB >= rTMR_Ch1_ValC) AND (rTMR_Ch1_ValB <= rTMR_Ch1_ValA)) THEN
        rTMR_Ch1_VotedRaw := rTMR_Ch1_ValB;
    ELSE
        rTMR_Ch1_VotedRaw := rTMR_Ch1_ValC;
    END_IF;
ELSIF rTMR_Ch1_FaultA AND (NOT rTMR_Ch1_FaultB) AND (NOT rTMR_Ch1_FaultC) THEN
    (* 1oo2 Degraded State: Sensor A faulted -> Mean of B and C *)
    rTMR_Ch1_DegradationState := 2;
    rTMR_Ch1_VotedRaw := (rTMR_Ch1_ValB + rTMR_Ch1_ValC) * 0.5;
ELSIF rTMR_Ch1_FaultB AND (NOT rTMR_Ch1_FaultA) AND (NOT rTMR_Ch1_FaultC) THEN
    (* 1oo2 Degraded State: Sensor B faulted -> Mean of A and C *)
    rTMR_Ch1_DegradationState := 2;
    rTMR_Ch1_VotedRaw := (rTMR_Ch1_ValA + rTMR_Ch1_ValC) * 0.5;
ELSIF rTMR_Ch1_FaultC AND (NOT rTMR_Ch1_FaultA) AND (NOT rTMR_Ch1_FaultB) THEN
    (* 1oo2 Degraded State: Sensor C faulted -> Mean of A and B *)
    rTMR_Ch1_DegradationState := 2;
    rTMR_Ch1_VotedRaw := (rTMR_Ch1_ValA + rTMR_Ch1_ValB) * 0.5;
ELSIF (NOT rTMR_Ch1_FaultA) AND rTMR_Ch1_FaultB AND rTMR_Ch1_FaultC THEN
    (* 1oo1 Degraded State: Only Sensor A healthy *)
    rTMR_Ch1_DegradationState := 1;
    rTMR_Ch1_VotedRaw := rTMR_Ch1_ValA;
ELSIF (NOT rTMR_Ch1_FaultB) AND rTMR_Ch1_FaultA AND rTMR_Ch1_FaultC THEN
    (* 1oo1 Degraded State: Only Sensor B healthy *)
    rTMR_Ch1_DegradationState := 1;
    rTMR_Ch1_VotedRaw := rTMR_Ch1_ValB;
ELSIF (NOT rTMR_Ch1_FaultC) AND rTMR_Ch1_FaultA AND rTMR_Ch1_FaultB THEN
    (* 1oo1 Degraded State: Only Sensor C healthy *)
    rTMR_Ch1_DegradationState := 1;
    rTMR_Ch1_VotedRaw := rTMR_Ch1_ValC;
ELSE
    (* Total TMR Failure: Fallback to Cyber-Physical Observer prediction *)
    rTMR_Ch1_DegradationState := 0;
    rTMR_Ch1_VotedRaw := a_x_pred[1];
END_IF;

(* First-Order Exponential Low-Pass Bumpless Transfer Filter *)
rTMR_Ch1_VotedFilt := (rFilter_Alpha * rTMR_Ch1_VotedRaw) + ((1.0 - rFilter_Alpha) * rTMR_Ch1_VotedPrev);
rTMR_Ch1_VotedPrev := rTMR_Ch1_VotedFilt;

(* -------------------------------------------------------------------------------------------------- *)
(* TMR CHANNEL Ch2: Head Injection Cylinder Hydraulic Pressure [bar] *)
(* -------------------------------------------------------------------------------------------------- *)
rTMR_Ch2_ValA := rHeadPress_SensorA_bar;
rTMR_Ch2_ValB := rHeadPress_SensorB_bar;
rTMR_Ch2_ValC := rHeadPress_SensorC_bar;

(* Calculate pairwise absolute deviation deltas *)
rTMR_Ch2_DiffAB := ABS(rTMR_Ch2_ValA - rTMR_Ch2_ValB);
rTMR_Ch2_DiffBC := ABS(rTMR_Ch2_ValB - rTMR_Ch2_ValC);
rTMR_Ch2_DiffCA := ABS(rTMR_Ch2_ValC - rTMR_Ch2_ValA);

(* Instantaneous discrepancy evaluation *)
rTMR_Ch2_DiscAB := (rTMR_Ch2_DiffAB > rTMR_Ch2_Tol);
rTMR_Ch2_DiscBC := (rTMR_Ch2_DiffBC > rTMR_Ch2_Tol);
rTMR_Ch2_DiscCA := (rTMR_Ch2_DiffCA > rTMR_Ch2_Tol);

(* Discrepancy integration debounce timer for Pair A-B *)
IF rTMR_Ch2_DiscAB THEN
    rTMR_Ch2_TimerAB_s := rTMR_Ch2_TimerAB_s + rCycleTime_s;
    IF rTMR_Ch2_TimerAB_s >= rTMR_Discrepancy_Limit_s THEN
        rTMR_Ch2_TimerAB_s := rTMR_Discrepancy_Limit_s;
    END_IF;
ELSE
    IF rTMR_Ch2_TimerAB_s > 0.0 THEN
        rTMR_Ch2_TimerAB_s := rTMR_Ch2_TimerAB_s - (rCycleTime_s * 2.0);
        IF rTMR_Ch2_TimerAB_s < 0.0 THEN
            rTMR_Ch2_TimerAB_s := 0.0;
        END_IF;
    END_IF;
END_IF;

(* Discrepancy integration debounce timer for Pair B-C *)
IF rTMR_Ch2_DiscBC THEN
    rTMR_Ch2_TimerBC_s := rTMR_Ch2_TimerBC_s + rCycleTime_s;
    IF rTMR_Ch2_TimerBC_s >= rTMR_Discrepancy_Limit_s THEN
        rTMR_Ch2_TimerBC_s := rTMR_Discrepancy_Limit_s;
    END_IF;
ELSE
    IF rTMR_Ch2_TimerBC_s > 0.0 THEN
        rTMR_Ch2_TimerBC_s := rTMR_Ch2_TimerBC_s - (rCycleTime_s * 2.0);
        IF rTMR_Ch2_TimerBC_s < 0.0 THEN
            rTMR_Ch2_TimerBC_s := 0.0;
        END_IF;
    END_IF;
END_IF;

(* Discrepancy integration debounce timer for Pair C-A *)
IF rTMR_Ch2_DiscCA THEN
    rTMR_Ch2_TimerCA_s := rTMR_Ch2_TimerCA_s + rCycleTime_s;
    IF rTMR_Ch2_TimerCA_s >= rTMR_Discrepancy_Limit_s THEN
        rTMR_Ch2_TimerCA_s := rTMR_Discrepancy_Limit_s;
    END_IF;
ELSE
    IF rTMR_Ch2_TimerCA_s > 0.0 THEN
        rTMR_Ch2_TimerCA_s := rTMR_Ch2_TimerCA_s - (rCycleTime_s * 2.0);
        IF rTMR_Ch2_TimerCA_s < 0.0 THEN
            rTMR_Ch2_TimerCA_s := 0.0;
        END_IF;
    END_IF;
END_IF;

(* Sensor Isolation: A sensor is faulted if both of its pairs persist in discrepancy *)
IF (rTMR_Ch2_TimerAB_s >= rTMR_Discrepancy_Limit_s) AND (rTMR_Ch2_TimerCA_s >= rTMR_Discrepancy_Limit_s) THEN
    rTMR_Ch2_FaultA := TRUE;
END_IF;
IF (rTMR_Ch2_TimerAB_s >= rTMR_Discrepancy_Limit_s) AND (rTMR_Ch2_TimerBC_s >= rTMR_Discrepancy_Limit_s) THEN
    rTMR_Ch2_FaultB := TRUE;
END_IF;
IF (rTMR_Ch2_TimerBC_s >= rTMR_Discrepancy_Limit_s) AND (rTMR_Ch2_TimerCA_s >= rTMR_Discrepancy_Limit_s) THEN
    rTMR_Ch2_FaultC := TRUE;
END_IF;

(* Degradation Logic & Voted Value Selection *)
IF (NOT rTMR_Ch2_FaultA) AND (NOT rTMR_Ch2_FaultB) AND (NOT rTMR_Ch2_FaultC) THEN
    (* Nominal 2oo3 State: All 3 sensors healthy -> Median Selection *)
    rTMR_Ch2_DegradationState := 3;
    IF ((rTMR_Ch2_ValA >= rTMR_Ch2_ValB) AND (rTMR_Ch2_ValA <= rTMR_Ch2_ValC)) OR ((rTMR_Ch2_ValA >= rTMR_Ch2_ValC) AND (rTMR_Ch2_ValA <= rTMR_Ch2_ValB)) THEN
        rTMR_Ch2_VotedRaw := rTMR_Ch2_ValA;
    ELSIF ((rTMR_Ch2_ValB >= rTMR_Ch2_ValA) AND (rTMR_Ch2_ValB <= rTMR_Ch2_ValC)) OR ((rTMR_Ch2_ValB >= rTMR_Ch2_ValC) AND (rTMR_Ch2_ValB <= rTMR_Ch2_ValA)) THEN
        rTMR_Ch2_VotedRaw := rTMR_Ch2_ValB;
    ELSE
        rTMR_Ch2_VotedRaw := rTMR_Ch2_ValC;
    END_IF;
ELSIF rTMR_Ch2_FaultA AND (NOT rTMR_Ch2_FaultB) AND (NOT rTMR_Ch2_FaultC) THEN
    (* 1oo2 Degraded State: Sensor A faulted -> Mean of B and C *)
    rTMR_Ch2_DegradationState := 2;
    rTMR_Ch2_VotedRaw := (rTMR_Ch2_ValB + rTMR_Ch2_ValC) * 0.5;
ELSIF rTMR_Ch2_FaultB AND (NOT rTMR_Ch2_FaultA) AND (NOT rTMR_Ch2_FaultC) THEN
    (* 1oo2 Degraded State: Sensor B faulted -> Mean of A and C *)
    rTMR_Ch2_DegradationState := 2;
    rTMR_Ch2_VotedRaw := (rTMR_Ch2_ValA + rTMR_Ch2_ValC) * 0.5;
ELSIF rTMR_Ch2_FaultC AND (NOT rTMR_Ch2_FaultA) AND (NOT rTMR_Ch2_FaultB) THEN
    (* 1oo2 Degraded State: Sensor C faulted -> Mean of A and B *)
    rTMR_Ch2_DegradationState := 2;
    rTMR_Ch2_VotedRaw := (rTMR_Ch2_ValA + rTMR_Ch2_ValB) * 0.5;
ELSIF (NOT rTMR_Ch2_FaultA) AND rTMR_Ch2_FaultB AND rTMR_Ch2_FaultC THEN
    (* 1oo1 Degraded State: Only Sensor A healthy *)
    rTMR_Ch2_DegradationState := 1;
    rTMR_Ch2_VotedRaw := rTMR_Ch2_ValA;
ELSIF (NOT rTMR_Ch2_FaultB) AND rTMR_Ch2_FaultA AND rTMR_Ch2_FaultC THEN
    (* 1oo1 Degraded State: Only Sensor B healthy *)
    rTMR_Ch2_DegradationState := 1;
    rTMR_Ch2_VotedRaw := rTMR_Ch2_ValB;
ELSIF (NOT rTMR_Ch2_FaultC) AND rTMR_Ch2_FaultA AND rTMR_Ch2_FaultB THEN
    (* 1oo1 Degraded State: Only Sensor C healthy *)
    rTMR_Ch2_DegradationState := 1;
    rTMR_Ch2_VotedRaw := rTMR_Ch2_ValC;
ELSE
    (* Total TMR Failure: Fallback to Cyber-Physical Observer prediction *)
    rTMR_Ch2_DegradationState := 0;
    rTMR_Ch2_VotedRaw := a_x_pred[3];
END_IF;

(* First-Order Exponential Low-Pass Bumpless Transfer Filter *)
rTMR_Ch2_VotedFilt := (rFilter_Alpha * rTMR_Ch2_VotedRaw) + ((1.0 - rFilter_Alpha) * rTMR_Ch2_VotedPrev);
rTMR_Ch2_VotedPrev := rTMR_Ch2_VotedFilt;

(* -------------------------------------------------------------------------------------------------- *)
(* TMR CHANNEL Ch3: Die Cavity Absolute Vacuum Transducers [mbar] *)
(* -------------------------------------------------------------------------------------------------- *)
rTMR_Ch3_ValA := rCavityVacuum_SensorA_mbar;
rTMR_Ch3_ValB := rCavityVacuum_SensorB_mbar;
rTMR_Ch3_ValC := rCavityVacuum_SensorC_mbar;

(* Calculate pairwise absolute deviation deltas *)
rTMR_Ch3_DiffAB := ABS(rTMR_Ch3_ValA - rTMR_Ch3_ValB);
rTMR_Ch3_DiffBC := ABS(rTMR_Ch3_ValB - rTMR_Ch3_ValC);
rTMR_Ch3_DiffCA := ABS(rTMR_Ch3_ValC - rTMR_Ch3_ValA);

(* Instantaneous discrepancy evaluation *)
rTMR_Ch3_DiscAB := (rTMR_Ch3_DiffAB > rTMR_Ch3_Tol);
rTMR_Ch3_DiscBC := (rTMR_Ch3_DiffBC > rTMR_Ch3_Tol);
rTMR_Ch3_DiscCA := (rTMR_Ch3_DiffCA > rTMR_Ch3_Tol);

(* Discrepancy integration debounce timer for Pair A-B *)
IF rTMR_Ch3_DiscAB THEN
    rTMR_Ch3_TimerAB_s := rTMR_Ch3_TimerAB_s + rCycleTime_s;
    IF rTMR_Ch3_TimerAB_s >= rTMR_Discrepancy_Limit_s THEN
        rTMR_Ch3_TimerAB_s := rTMR_Discrepancy_Limit_s;
    END_IF;
ELSE
    IF rTMR_Ch3_TimerAB_s > 0.0 THEN
        rTMR_Ch3_TimerAB_s := rTMR_Ch3_TimerAB_s - (rCycleTime_s * 2.0);
        IF rTMR_Ch3_TimerAB_s < 0.0 THEN
            rTMR_Ch3_TimerAB_s := 0.0;
        END_IF;
    END_IF;
END_IF;

(* Discrepancy integration debounce timer for Pair B-C *)
IF rTMR_Ch3_DiscBC THEN
    rTMR_Ch3_TimerBC_s := rTMR_Ch3_TimerBC_s + rCycleTime_s;
    IF rTMR_Ch3_TimerBC_s >= rTMR_Discrepancy_Limit_s THEN
        rTMR_Ch3_TimerBC_s := rTMR_Discrepancy_Limit_s;
    END_IF;
ELSE
    IF rTMR_Ch3_TimerBC_s > 0.0 THEN
        rTMR_Ch3_TimerBC_s := rTMR_Ch3_TimerBC_s - (rCycleTime_s * 2.0);
        IF rTMR_Ch3_TimerBC_s < 0.0 THEN
            rTMR_Ch3_TimerBC_s := 0.0;
        END_IF;
    END_IF;
END_IF;

(* Discrepancy integration debounce timer for Pair C-A *)
IF rTMR_Ch3_DiscCA THEN
    rTMR_Ch3_TimerCA_s := rTMR_Ch3_TimerCA_s + rCycleTime_s;
    IF rTMR_Ch3_TimerCA_s >= rTMR_Discrepancy_Limit_s THEN
        rTMR_Ch3_TimerCA_s := rTMR_Discrepancy_Limit_s;
    END_IF;
ELSE
    IF rTMR_Ch3_TimerCA_s > 0.0 THEN
        rTMR_Ch3_TimerCA_s := rTMR_Ch3_TimerCA_s - (rCycleTime_s * 2.0);
        IF rTMR_Ch3_TimerCA_s < 0.0 THEN
            rTMR_Ch3_TimerCA_s := 0.0;
        END_IF;
    END_IF;
END_IF;

(* Sensor Isolation: A sensor is faulted if both of its pairs persist in discrepancy *)
IF (rTMR_Ch3_TimerAB_s >= rTMR_Discrepancy_Limit_s) AND (rTMR_Ch3_TimerCA_s >= rTMR_Discrepancy_Limit_s) THEN
    rTMR_Ch3_FaultA := TRUE;
END_IF;
IF (rTMR_Ch3_TimerAB_s >= rTMR_Discrepancy_Limit_s) AND (rTMR_Ch3_TimerBC_s >= rTMR_Discrepancy_Limit_s) THEN
    rTMR_Ch3_FaultB := TRUE;
END_IF;
IF (rTMR_Ch3_TimerBC_s >= rTMR_Discrepancy_Limit_s) AND (rTMR_Ch3_TimerCA_s >= rTMR_Discrepancy_Limit_s) THEN
    rTMR_Ch3_FaultC := TRUE;
END_IF;

(* Degradation Logic & Voted Value Selection *)
IF (NOT rTMR_Ch3_FaultA) AND (NOT rTMR_Ch3_FaultB) AND (NOT rTMR_Ch3_FaultC) THEN
    (* Nominal 2oo3 State: All 3 sensors healthy -> Median Selection *)
    rTMR_Ch3_DegradationState := 3;
    IF ((rTMR_Ch3_ValA >= rTMR_Ch3_ValB) AND (rTMR_Ch3_ValA <= rTMR_Ch3_ValC)) OR ((rTMR_Ch3_ValA >= rTMR_Ch3_ValC) AND (rTMR_Ch3_ValA <= rTMR_Ch3_ValB)) THEN
        rTMR_Ch3_VotedRaw := rTMR_Ch3_ValA;
    ELSIF ((rTMR_Ch3_ValB >= rTMR_Ch3_ValA) AND (rTMR_Ch3_ValB <= rTMR_Ch3_ValC)) OR ((rTMR_Ch3_ValB >= rTMR_Ch3_ValC) AND (rTMR_Ch3_ValB <= rTMR_Ch3_ValA)) THEN
        rTMR_Ch3_VotedRaw := rTMR_Ch3_ValB;
    ELSE
        rTMR_Ch3_VotedRaw := rTMR_Ch3_ValC;
    END_IF;
ELSIF rTMR_Ch3_FaultA AND (NOT rTMR_Ch3_FaultB) AND (NOT rTMR_Ch3_FaultC) THEN
    (* 1oo2 Degraded State: Sensor A faulted -> Mean of B and C *)
    rTMR_Ch3_DegradationState := 2;
    rTMR_Ch3_VotedRaw := (rTMR_Ch3_ValB + rTMR_Ch3_ValC) * 0.5;
ELSIF rTMR_Ch3_FaultB AND (NOT rTMR_Ch3_FaultA) AND (NOT rTMR_Ch3_FaultC) THEN
    (* 1oo2 Degraded State: Sensor B faulted -> Mean of A and C *)
    rTMR_Ch3_DegradationState := 2;
    rTMR_Ch3_VotedRaw := (rTMR_Ch3_ValA + rTMR_Ch3_ValC) * 0.5;
ELSIF rTMR_Ch3_FaultC AND (NOT rTMR_Ch3_FaultA) AND (NOT rTMR_Ch3_FaultB) THEN
    (* 1oo2 Degraded State: Sensor C faulted -> Mean of A and B *)
    rTMR_Ch3_DegradationState := 2;
    rTMR_Ch3_VotedRaw := (rTMR_Ch3_ValA + rTMR_Ch3_ValB) * 0.5;
ELSIF (NOT rTMR_Ch3_FaultA) AND rTMR_Ch3_FaultB AND rTMR_Ch3_FaultC THEN
    (* 1oo1 Degraded State: Only Sensor A healthy *)
    rTMR_Ch3_DegradationState := 1;
    rTMR_Ch3_VotedRaw := rTMR_Ch3_ValA;
ELSIF (NOT rTMR_Ch3_FaultB) AND rTMR_Ch3_FaultA AND rTMR_Ch3_FaultC THEN
    (* 1oo1 Degraded State: Only Sensor B healthy *)
    rTMR_Ch3_DegradationState := 1;
    rTMR_Ch3_VotedRaw := rTMR_Ch3_ValB;
ELSIF (NOT rTMR_Ch3_FaultC) AND rTMR_Ch3_FaultA AND rTMR_Ch3_FaultB THEN
    (* 1oo1 Degraded State: Only Sensor C healthy *)
    rTMR_Ch3_DegradationState := 1;
    rTMR_Ch3_VotedRaw := rTMR_Ch3_ValC;
ELSE
    (* Total TMR Failure: Fallback to Cyber-Physical Observer prediction *)
    rTMR_Ch3_DegradationState := 0;
    rTMR_Ch3_VotedRaw := a_x_pred[5];
END_IF;

(* First-Order Exponential Low-Pass Bumpless Transfer Filter *)
rTMR_Ch3_VotedFilt := (rFilter_Alpha * rTMR_Ch3_VotedRaw) + ((1.0 - rFilter_Alpha) * rTMR_Ch3_VotedPrev);
rTMR_Ch3_VotedPrev := rTMR_Ch3_VotedFilt;

(* -------------------------------------------------------------------------------------------------- *)
(* TMR CHANNEL Ch4: 4,500-Ton Clamping Mechanism Tie-Bar Total Force [kN] *)
(* -------------------------------------------------------------------------------------------------- *)
rTMR_Ch4_ValA := rClampForce_SensorA_kN;
rTMR_Ch4_ValB := rClampForce_SensorB_kN;
rTMR_Ch4_ValC := rClampForce_SensorC_kN;

(* Calculate pairwise absolute deviation deltas *)
rTMR_Ch4_DiffAB := ABS(rTMR_Ch4_ValA - rTMR_Ch4_ValB);
rTMR_Ch4_DiffBC := ABS(rTMR_Ch4_ValB - rTMR_Ch4_ValC);
rTMR_Ch4_DiffCA := ABS(rTMR_Ch4_ValC - rTMR_Ch4_ValA);

(* Instantaneous discrepancy evaluation *)
rTMR_Ch4_DiscAB := (rTMR_Ch4_DiffAB > rTMR_Ch4_Tol);
rTMR_Ch4_DiscBC := (rTMR_Ch4_DiffBC > rTMR_Ch4_Tol);
rTMR_Ch4_DiscCA := (rTMR_Ch4_DiffCA > rTMR_Ch4_Tol);

(* Discrepancy integration debounce timer for Pair A-B *)
IF rTMR_Ch4_DiscAB THEN
    rTMR_Ch4_TimerAB_s := rTMR_Ch4_TimerAB_s + rCycleTime_s;
    IF rTMR_Ch4_TimerAB_s >= rTMR_Discrepancy_Limit_s THEN
        rTMR_Ch4_TimerAB_s := rTMR_Discrepancy_Limit_s;
    END_IF;
ELSE
    IF rTMR_Ch4_TimerAB_s > 0.0 THEN
        rTMR_Ch4_TimerAB_s := rTMR_Ch4_TimerAB_s - (rCycleTime_s * 2.0);
        IF rTMR_Ch4_TimerAB_s < 0.0 THEN
            rTMR_Ch4_TimerAB_s := 0.0;
        END_IF;
    END_IF;
END_IF;

(* Discrepancy integration debounce timer for Pair B-C *)
IF rTMR_Ch4_DiscBC THEN
    rTMR_Ch4_TimerBC_s := rTMR_Ch4_TimerBC_s + rCycleTime_s;
    IF rTMR_Ch4_TimerBC_s >= rTMR_Discrepancy_Limit_s THEN
        rTMR_Ch4_TimerBC_s := rTMR_Discrepancy_Limit_s;
    END_IF;
ELSE
    IF rTMR_Ch4_TimerBC_s > 0.0 THEN
        rTMR_Ch4_TimerBC_s := rTMR_Ch4_TimerBC_s - (rCycleTime_s * 2.0);
        IF rTMR_Ch4_TimerBC_s < 0.0 THEN
            rTMR_Ch4_TimerBC_s := 0.0;
        END_IF;
    END_IF;
END_IF;

(* Discrepancy integration debounce timer for Pair C-A *)
IF rTMR_Ch4_DiscCA THEN
    rTMR_Ch4_TimerCA_s := rTMR_Ch4_TimerCA_s + rCycleTime_s;
    IF rTMR_Ch4_TimerCA_s >= rTMR_Discrepancy_Limit_s THEN
        rTMR_Ch4_TimerCA_s := rTMR_Discrepancy_Limit_s;
    END_IF;
ELSE
    IF rTMR_Ch4_TimerCA_s > 0.0 THEN
        rTMR_Ch4_TimerCA_s := rTMR_Ch4_TimerCA_s - (rCycleTime_s * 2.0);
        IF rTMR_Ch4_TimerCA_s < 0.0 THEN
            rTMR_Ch4_TimerCA_s := 0.0;
        END_IF;
    END_IF;
END_IF;

(* Sensor Isolation: A sensor is faulted if both of its pairs persist in discrepancy *)
IF (rTMR_Ch4_TimerAB_s >= rTMR_Discrepancy_Limit_s) AND (rTMR_Ch4_TimerCA_s >= rTMR_Discrepancy_Limit_s) THEN
    rTMR_Ch4_FaultA := TRUE;
END_IF;
IF (rTMR_Ch4_TimerAB_s >= rTMR_Discrepancy_Limit_s) AND (rTMR_Ch4_TimerBC_s >= rTMR_Discrepancy_Limit_s) THEN
    rTMR_Ch4_FaultB := TRUE;
END_IF;
IF (rTMR_Ch4_TimerBC_s >= rTMR_Discrepancy_Limit_s) AND (rTMR_Ch4_TimerCA_s >= rTMR_Discrepancy_Limit_s) THEN
    rTMR_Ch4_FaultC := TRUE;
END_IF;

(* Degradation Logic & Voted Value Selection *)
IF (NOT rTMR_Ch4_FaultA) AND (NOT rTMR_Ch4_FaultB) AND (NOT rTMR_Ch4_FaultC) THEN
    (* Nominal 2oo3 State: All 3 sensors healthy -> Median Selection *)
    rTMR_Ch4_DegradationState := 3;
    IF ((rTMR_Ch4_ValA >= rTMR_Ch4_ValB) AND (rTMR_Ch4_ValA <= rTMR_Ch4_ValC)) OR ((rTMR_Ch4_ValA >= rTMR_Ch4_ValC) AND (rTMR_Ch4_ValA <= rTMR_Ch4_ValB)) THEN
        rTMR_Ch4_VotedRaw := rTMR_Ch4_ValA;
    ELSIF ((rTMR_Ch4_ValB >= rTMR_Ch4_ValA) AND (rTMR_Ch4_ValB <= rTMR_Ch4_ValC)) OR ((rTMR_Ch4_ValB >= rTMR_Ch4_ValC) AND (rTMR_Ch4_ValB <= rTMR_Ch4_ValA)) THEN
        rTMR_Ch4_VotedRaw := rTMR_Ch4_ValB;
    ELSE
        rTMR_Ch4_VotedRaw := rTMR_Ch4_ValC;
    END_IF;
ELSIF rTMR_Ch4_FaultA AND (NOT rTMR_Ch4_FaultB) AND (NOT rTMR_Ch4_FaultC) THEN
    (* 1oo2 Degraded State: Sensor A faulted -> Mean of B and C *)
    rTMR_Ch4_DegradationState := 2;
    rTMR_Ch4_VotedRaw := (rTMR_Ch4_ValB + rTMR_Ch4_ValC) * 0.5;
ELSIF rTMR_Ch4_FaultB AND (NOT rTMR_Ch4_FaultA) AND (NOT rTMR_Ch4_FaultC) THEN
    (* 1oo2 Degraded State: Sensor B faulted -> Mean of A and C *)
    rTMR_Ch4_DegradationState := 2;
    rTMR_Ch4_VotedRaw := (rTMR_Ch4_ValA + rTMR_Ch4_ValC) * 0.5;
ELSIF rTMR_Ch4_FaultC AND (NOT rTMR_Ch4_FaultA) AND (NOT rTMR_Ch4_FaultB) THEN
    (* 1oo2 Degraded State: Sensor C faulted -> Mean of A and B *)
    rTMR_Ch4_DegradationState := 2;
    rTMR_Ch4_VotedRaw := (rTMR_Ch4_ValA + rTMR_Ch4_ValB) * 0.5;
ELSIF (NOT rTMR_Ch4_FaultA) AND rTMR_Ch4_FaultB AND rTMR_Ch4_FaultC THEN
    (* 1oo1 Degraded State: Only Sensor A healthy *)
    rTMR_Ch4_DegradationState := 1;
    rTMR_Ch4_VotedRaw := rTMR_Ch4_ValA;
ELSIF (NOT rTMR_Ch4_FaultB) AND rTMR_Ch4_FaultA AND rTMR_Ch4_FaultC THEN
    (* 1oo1 Degraded State: Only Sensor B healthy *)
    rTMR_Ch4_DegradationState := 1;
    rTMR_Ch4_VotedRaw := rTMR_Ch4_ValB;
ELSIF (NOT rTMR_Ch4_FaultC) AND rTMR_Ch4_FaultA AND rTMR_Ch4_FaultB THEN
    (* 1oo1 Degraded State: Only Sensor C healthy *)
    rTMR_Ch4_DegradationState := 1;
    rTMR_Ch4_VotedRaw := rTMR_Ch4_ValC;
ELSE
    (* Total TMR Failure: Fallback to Cyber-Physical Observer prediction *)
    rTMR_Ch4_DegradationState := 0;
    rTMR_Ch4_VotedRaw := (a_x_pred[3]*12.45 + a_x_pred[6]*24.85);
END_IF;

(* First-Order Exponential Low-Pass Bumpless Transfer Filter *)
rTMR_Ch4_VotedFilt := (rFilter_Alpha * rTMR_Ch4_VotedRaw) + ((1.0 - rFilter_Alpha) * rTMR_Ch4_VotedPrev);
rTMR_Ch4_VotedPrev := rTMR_Ch4_VotedFilt;

(* Physical Feedback Signal Assignment & Numerical Differentiation *)
rDifferentiated_Vel_Raw := (rTMR_Ch1_VotedFilt - rVoted_PlungerPos_mm) / (rCycleTime_s * 1000.0);
(* Apply 2nd-order dynamic smoothing filter to differentiated velocity *)
rVoted_PlungerVel_mps := (0.35 * rDifferentiated_Vel_Raw) + (0.65 * rVoted_PlungerVel_mps);
rVoted_PlungerPos_mm := rTMR_Ch1_VotedFilt;
rVoted_HeadPress_bar := rTMR_Ch2_VotedFilt;
rVoted_CavityVacuum_mbar := rTMR_Ch3_VotedFilt;
rVoted_ClampForce_kN := rTMR_Ch4_VotedFilt;


(* ==================================================================================================== *)
(* PHASE 2: FIRST-PRINCIPLES CYBER-PHYSICAL DISCRETE STATE-SPACE MODEL & KALMAN OBSERVER                *)
(* Discrete Sampling Period Ts = 0.002s (2000 us). Real-Time Matrix Propagation                         *)
(* Dynamic States x:                                                                                    *)
(*   x[1]: Plunger Position Tracking Error e_pos = (x_meas - x_ref) [mm]                                *)
(*   x[2]: Plunger Velocity Tracking Error e_vel = (v_meas - v_ref) [m/s]                               *)
(*   x[3]: Hydraulic Cylinder Head Chamber Injection Pressure P_head [bar]                              *)
(*   x[4]: Hydraulic Cylinder Rod Chamber Backpressure P_rod [bar]                                      *)
(*   x[5]: Die Cavity Absolute Vacuum Pressure P_vac [mbar]                                             *)
(*   x[6]: Molten Metal Flow Resistance & Solidification Counter-Pressure P_met [bar]                   *)
(* Control Inputs u:                                                                                    *)
(*   u[1]: Head Proportional Fast-Shot Servo-Valve Spool Command [%] (-100..+100)                      *)
(*   u[2]: Rod Proportional Backpressure Valve Spool Command [%] (0..100)                              *)
(*   u[3]: Accumulator Discharge Booster Poppet Valve Command [%] (0..100)                              *)
(*   u[4]: Squeeze Intensifier Multiplier High-Pressure Pilot [%] (0..100)                              *)
(*   u[5]: Cavity Chill-Vent High-Vacuum Solenoid Poppet Command [%] (0..100)                           *)
(* Measurements y:                                                                                      *)
(*   y[1]: Plunger Voted Linear Position [mm]                                                           *)
(*   y[2]: Head Chamber Voted Hydraulic Pressure [bar]                                                  *)
(*   y[3]: Cavity Voted Absolute Vacuum Level [mbar]                                                    *)
(*   y[4]: Tie-Bar 4,500-Ton Total Locking Force Reaction [kN]                                          *)
(* ==================================================================================================== *)

(* Step 2.1: Actuator Vector & Measurement Vector Mapping *)
a_u_act[1] := rServoValve_HeadSpool_cmd;
a_u_act[2] := rServoValve_RodSpool_cmd;
a_u_act[3] := rAccuBoosterValve_cmd;
a_u_act[4] := rIntensifierValve_cmd;
a_u_act[5] := rVacuumPoppetValve_cmd;

a_y_meas[1] := rVoted_PlungerPos_mm;
a_y_meas[2] := rVoted_HeadPress_bar;
a_y_meas[3] := rVoted_CavityVacuum_mbar;
a_y_meas[4] := rVoted_ClampForce_kN;

(* Step 2.2: Prior State Estimate Propagation: x_hat[k|k-1] = A * x_hat[k-1|k-1] + B * u[k-1] *)
(* State 1: Plunger Position Tracking Error e_pos [mm] *)
a_x_pred[1] := (rA_Mat[1,1] * a_x_hat[1]) + (rA_Mat[1,2] * a_x_hat[2]) + (rA_Mat[1,3] * a_x_hat[3])
             + (rA_Mat[1,4] * a_x_hat[4]) + (rA_Mat[1,5] * a_x_hat[5]) + (rA_Mat[1,6] * a_x_hat[6])
             + (rB_Mat[1,1] * a_u_prev[1]) + (rB_Mat[1,2] * a_u_prev[2]) + (rB_Mat[1,3] * a_u_prev[3])
             + (rB_Mat[1,4] * a_u_prev[4]) + (rB_Mat[1,5] * a_u_prev[5]);

(* State 2: Plunger Velocity Tracking Error e_vel [m/s] *)
a_x_pred[2] := (rA_Mat[2,1] * a_x_hat[1]) + (rA_Mat[2,2] * a_x_hat[2]) + (rA_Mat[2,3] * a_x_hat[3])
             + (rA_Mat[2,4] * a_x_hat[4]) + (rA_Mat[2,5] * a_x_hat[5]) + (rA_Mat[2,6] * a_x_hat[6])
             + (rB_Mat[2,1] * a_u_prev[1]) + (rB_Mat[2,2] * a_u_prev[2]) + (rB_Mat[2,3] * a_u_prev[3])
             + (rB_Mat[2,4] * a_u_prev[4]) + (rB_Mat[2,5] * a_u_prev[5]);

(* State 3: Hydraulic Head Chamber Pressure P_head [bar] *)
a_x_pred[3] := (rA_Mat[3,1] * a_x_hat[1]) + (rA_Mat[3,2] * a_x_hat[2]) + (rA_Mat[3,3] * a_x_hat[3])
             + (rA_Mat[3,4] * a_x_hat[4]) + (rA_Mat[3,5] * a_x_hat[5]) + (rA_Mat[3,6] * a_x_hat[6])
             + (rB_Mat[3,1] * a_u_prev[1]) + (rB_Mat[3,2] * a_u_prev[2]) + (rB_Mat[3,3] * a_u_prev[3])
             + (rB_Mat[3,4] * a_u_prev[4]) + (rB_Mat[3,5] * a_u_prev[5]);

(* State 4: Hydraulic Rod Chamber Backpressure P_rod [bar] *)
a_x_pred[4] := (rA_Mat[4,1] * a_x_hat[1]) + (rA_Mat[4,2] * a_x_hat[2]) + (rA_Mat[4,3] * a_x_hat[3])
             + (rA_Mat[4,4] * a_x_hat[4]) + (rA_Mat[4,5] * a_x_hat[5]) + (rA_Mat[4,6] * a_x_hat[6])
             + (rB_Mat[4,1] * a_u_prev[1]) + (rB_Mat[4,2] * a_u_prev[2]) + (rB_Mat[4,3] * a_u_prev[3])
             + (rB_Mat[4,4] * a_u_prev[4]) + (rB_Mat[4,5] * a_u_prev[5]);

(* State 5: Cavity Absolute Vacuum Level P_vac [mbar] *)
a_x_pred[5] := (rA_Mat[5,1] * a_x_hat[1]) + (rA_Mat[5,2] * a_x_hat[2]) + (rA_Mat[5,3] * a_x_hat[3])
             + (rA_Mat[5,4] * a_x_hat[4]) + (rA_Mat[5,5] * a_x_hat[5]) + (rA_Mat[5,6] * a_x_hat[6])
             + (rB_Mat[5,1] * a_u_prev[1]) + (rB_Mat[5,2] * a_u_prev[2]) + (rB_Mat[5,3] * a_u_prev[3])
             + (rB_Mat[5,4] * a_u_prev[4]) + (rB_Mat[5,5] * a_u_prev[5]);

(* State 6: Molten Metal Flow Front Resistance P_met [bar] *)
a_x_pred[6] := (rA_Mat[6,1] * a_x_hat[1]) + (rA_Mat[6,2] * a_x_hat[2]) + (rA_Mat[6,3] * a_x_hat[3])
             + (rA_Mat[6,4] * a_x_hat[4]) + (rA_Mat[6,5] * a_x_hat[5]) + (rA_Mat[6,6] * a_x_hat[6])
             + (rB_Mat[6,1] * a_u_prev[1]) + (rB_Mat[6,2] * a_u_prev[2]) + (rB_Mat[6,3] * a_u_prev[3])
             + (rB_Mat[6,4] * a_u_prev[4]) + (rB_Mat[6,5] * a_u_prev[5]);

(* Step 2.3: Predicted Measurement Synthesis: y_hat[k] = C * x_hat[k|k-1] + D * u[k] *)
a_y_pred[1] := (rC_Mat[1,1] * a_x_pred[1]) + (rC_Mat[1,2] * a_x_pred[2]) + (rC_Mat[1,3] * a_x_pred[3])
             + (rC_Mat[1,4] * a_x_pred[4]) + (rC_Mat[1,5] * a_x_pred[5]) + (rC_Mat[1,6] * a_x_pred[6]);

a_y_pred[2] := (rC_Mat[2,1] * a_x_pred[1]) + (rC_Mat[2,2] * a_x_pred[2]) + (rC_Mat[2,3] * a_x_pred[3])
             + (rC_Mat[2,4] * a_x_pred[4]) + (rC_Mat[2,5] * a_x_pred[5]) + (rC_Mat[2,6] * a_x_pred[6]);

a_y_pred[3] := (rC_Mat[3,1] * a_x_pred[1]) + (rC_Mat[3,2] * a_x_pred[2]) + (rC_Mat[3,3] * a_x_pred[3])
             + (rC_Mat[3,4] * a_x_pred[4]) + (rC_Mat[3,5] * a_x_pred[5]) + (rC_Mat[3,6] * a_x_pred[6]);

a_y_pred[4] := (rC_Mat[4,1] * a_x_pred[1]) + (rC_Mat[4,2] * a_x_pred[2]) + (rC_Mat[4,3] * a_x_pred[3])
             + (rC_Mat[4,4] * a_x_pred[4]) + (rC_Mat[4,5] * a_x_pred[5]) + (rC_Mat[4,6] * a_x_pred[6]);

(* Step 2.4: Innovation Residual Vector Calculation: innov = (y_meas - y_pred) *)
a_innov[1] := a_y_meas[1] - a_y_pred[1]; (* Position residual [mm] *)
a_innov[2] := a_y_meas[2] - a_y_pred[2]; (* Head pressure residual [bar] *)
a_innov[3] := a_y_meas[3] - a_y_pred[3]; (* Cavity vacuum residual [mbar] *)
a_innov[4] := a_y_meas[4] - a_y_pred[4]; (* Clamping force residual [kN] *)

(* Nonlinear Outlier Suppression Clamping on Innovation Residuals *)
IF a_innov[1] > 25.0 THEN a_innov[1] := 25.0; ELSIF a_innov[1] < -25.0 THEN a_innov[1] := -25.0; END_IF;
IF a_innov[2] > 60.0 THEN a_innov[2] := 60.0; ELSIF a_innov[2] < -60.0 THEN a_innov[2] := -60.0; END_IF;
IF a_innov[3] > 100.0 THEN a_innov[3] := 100.0; ELSIF a_innov[3] < -100.0 THEN a_innov[3] := -100.0; END_IF;
IF a_innov[4] > 2500.0 THEN a_innov[4] := 2500.0; ELSIF a_innov[4] < -2500.0 THEN a_innov[4] := -2500.0; END_IF;

(* Step 2.5: Posterior Kalman State Correction: x_hat[k|k] = x_hat[k|k-1] + L * innov *)
a_x_hat[1] := a_x_pred[1] + (rL_Mat[1,1] * a_innov[1]) + (rL_Mat[1,2] * a_innov[2])
                          + (rL_Mat[1,3] * a_innov[3]) + (rL_Mat[1,4] * a_innov[4]);

a_x_hat[2] := a_x_pred[2] + (rL_Mat[2,1] * a_innov[1]) + (rL_Mat[2,2] * a_innov[2])
                          + (rL_Mat[2,3] * a_innov[3]) + (rL_Mat[2,4] * a_innov[4]);

a_x_hat[3] := a_x_pred[3] + (rL_Mat[3,1] * a_innov[1]) + (rL_Mat[3,2] * a_innov[2])
                          + (rL_Mat[3,3] * a_innov[3]) + (rL_Mat[3,4] * a_innov[4]);

a_x_hat[4] := a_x_pred[4] + (rL_Mat[4,1] * a_innov[1]) + (rL_Mat[4,2] * a_innov[2])
                          + (rL_Mat[4,3] * a_innov[3]) + (rL_Mat[4,4] * a_innov[4]);

a_x_hat[5] := a_x_pred[5] + (rL_Mat[5,1] * a_innov[1]) + (rL_Mat[5,2] * a_innov[2])
                          + (rL_Mat[5,3] * a_innov[3]) + (rL_Mat[5,4] * a_innov[4]);

a_x_hat[6] := a_x_pred[6] + (rL_Mat[6,1] * a_innov[1]) + (rL_Mat[6,2] * a_innov[2])
                          + (rL_Mat[6,3] * a_innov[3]) + (rL_Mat[6,4] * a_innov[4]);

(* Step 2.6: Cyber-Physical Observer Output Mapping *)
rEstimated_MetalPress_bar := a_x_hat[6];
rEstimated_CavityResistance_bar := (a_x_hat[6] * 0.82) + (ABS(a_x_hat[2]) * 8.45);

(* Store actuator commands for next cycle propagation *)
a_u_prev[1] := a_u_act[1];
a_u_prev[2] := a_u_act[2];
a_u_prev[3] := a_u_act[3];
a_u_prev[4] := a_u_act[4];
a_u_prev[5] := a_u_act[5];


(* ==================================================================================================== *)
(* PHASE 3: RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) WITH 10 UNROLLED PGD ITERATIONS             *)
(* Mathematical Formulation:                                                                            *)
(*   Prediction Horizon Hp = 5 steps (10 ms)                                                            *)
(*   Control Horizon    Hu = 3 steps (6 ms)                                                             *)
(*   PGD Iterations     N_iter = 10 fully unrolled descent steps                                        *)
(*   Quadratic Objective:                                                                               *)
(*     min J = 1/2 * sum_{h=1..5} (x_h - x_ref)^T * Q * (x_h - x_ref)                                   *)
(*           + 1/2 * sum_{h=1..3} u_h^T * R * u_h                                                       *)
(*           + 1/2 * sum_{h=1..3} (u_h - u_{h-1})^T * S * (u_h - u_{h-1})                               *)
(*           + 1/2 * (x_5 - x_ref)^T * P * (x_5 - x_ref)                                                *)
(*   Subject to:                                                                                        *)
(*     x_{h+1} = A * x_h + B * u_h                                                                      *)
(*     u_min <= u_h <= u_max                                                                            *)
(*     |u_h - u_{h-1}| <= Delta_u_max                                                                   *)
(* ==================================================================================================== *)

(* Step 3.1: Construct Time-Varying Target Reference Trajectory x_ref across Prediction Horizon Hp=5 *)
FOR h_step := 1 TO 5 DO
    (* Plunger position error target = 0.0 *)
    rX_Target[h_step, 1] := 0.0;
    (* Plunger velocity error target = 0.0 *)
    rX_Target[h_step, 2] := 0.0;
    (* Head pressure setpoint depends on active casting stage *)
    IF iState = 9 THEN
        (* Stage 3 Intensification holding pressure *)
        rX_Target[h_step, 3] := rStage3_TargetPress_bar;
    ELSIF iState = 7 THEN
        (* Stage 2 Fast shot dynamic pressure requirement *)
        rX_Target[h_step, 3] := 210.0;
    ELSE
        (* Slow shot and pre-fill pressure *)
        rX_Target[h_step, 3] := 65.0;
    END_IF;
    (* Rod backpressure target *)
    rX_Target[h_step, 4] := 25.0;
    (* Cavity vacuum target *)
    rX_Target[h_step, 5] := rVacuumTarget_mbar;
    (* Metal counter-pressure reference *)
    IF iState = 9 THEN
        rX_Target[h_step, 6] := rStage3_TargetPress_bar * 0.95;
    ELSE
        rX_Target[h_step, 6] := 10.0;
    END_IF;
END_FOR;

(* Step 3.2: Warm-Start Control Trajectory Initialization from Previous Solution *)
FOR j_idx := 1 TO 5 DO
    rU_Opt_Seq[1, j_idx] := a_u_prev[j_idx];
    rU_Opt_Seq[2, j_idx] := a_u_prev[j_idx];
    rU_Opt_Seq[3, j_idx] := a_u_prev[j_idx];
END_FOR;

(* ================================================================================================== *)
(* MPC PROJECTED GRADIENT DESCENT -- UNROLLED ITERATION 1 OF 10                                 *)
(* ================================================================================================== *)
iPGD_IterCount := 1;

(* Iteration 1 - Forward State Prediction Step 1 (h=1): x_1 = A * x_hat + B * u_1 *)
rX_Pred_Horizon[1, 1] := (rA_Mat[1,1] * a_x_hat[1]) + (rA_Mat[1,2] * a_x_hat[2]) + (rA_Mat[1,3] * a_x_hat[3]) + (rA_Mat[1,4] * a_x_hat[4]) + (rA_Mat[1,5] * a_x_hat[5]) + (rA_Mat[1,6] * a_x_hat[6]) + (rB_Mat[1,1] * rU_Opt_Seq[1,1]) + (rB_Mat[1,2] * rU_Opt_Seq[1,2]) + (rB_Mat[1,3] * rU_Opt_Seq[1,3]) + (rB_Mat[1,4] * rU_Opt_Seq[1,4]) + (rB_Mat[1,5] * rU_Opt_Seq[1,5]);
rX_Pred_Horizon[1, 2] := (rA_Mat[2,1] * a_x_hat[1]) + (rA_Mat[2,2] * a_x_hat[2]) + (rA_Mat[2,3] * a_x_hat[3]) + (rA_Mat[2,4] * a_x_hat[4]) + (rA_Mat[2,5] * a_x_hat[5]) + (rA_Mat[2,6] * a_x_hat[6]) + (rB_Mat[2,1] * rU_Opt_Seq[1,1]) + (rB_Mat[2,2] * rU_Opt_Seq[1,2]) + (rB_Mat[2,3] * rU_Opt_Seq[1,3]) + (rB_Mat[2,4] * rU_Opt_Seq[1,4]) + (rB_Mat[2,5] * rU_Opt_Seq[1,5]);
rX_Pred_Horizon[1, 3] := (rA_Mat[3,1] * a_x_hat[1]) + (rA_Mat[3,2] * a_x_hat[2]) + (rA_Mat[3,3] * a_x_hat[3]) + (rA_Mat[3,4] * a_x_hat[4]) + (rA_Mat[3,5] * a_x_hat[5]) + (rA_Mat[3,6] * a_x_hat[6]) + (rB_Mat[3,1] * rU_Opt_Seq[1,1]) + (rB_Mat[3,2] * rU_Opt_Seq[1,2]) + (rB_Mat[3,3] * rU_Opt_Seq[1,3]) + (rB_Mat[3,4] * rU_Opt_Seq[1,4]) + (rB_Mat[3,5] * rU_Opt_Seq[1,5]);
rX_Pred_Horizon[1, 4] := (rA_Mat[4,1] * a_x_hat[1]) + (rA_Mat[4,2] * a_x_hat[2]) + (rA_Mat[4,3] * a_x_hat[3]) + (rA_Mat[4,4] * a_x_hat[4]) + (rA_Mat[4,5] * a_x_hat[5]) + (rA_Mat[4,6] * a_x_hat[6]) + (rB_Mat[4,1] * rU_Opt_Seq[1,1]) + (rB_Mat[4,2] * rU_Opt_Seq[1,2]) + (rB_Mat[4,3] * rU_Opt_Seq[1,3]) + (rB_Mat[4,4] * rU_Opt_Seq[1,4]) + (rB_Mat[4,5] * rU_Opt_Seq[1,5]);
rX_Pred_Horizon[1, 5] := (rA_Mat[5,1] * a_x_hat[1]) + (rA_Mat[5,2] * a_x_hat[2]) + (rA_Mat[5,3] * a_x_hat[3]) + (rA_Mat[5,4] * a_x_hat[4]) + (rA_Mat[5,5] * a_x_hat[5]) + (rA_Mat[5,6] * a_x_hat[6]) + (rB_Mat[5,1] * rU_Opt_Seq[1,1]) + (rB_Mat[5,2] * rU_Opt_Seq[1,2]) + (rB_Mat[5,3] * rU_Opt_Seq[1,3]) + (rB_Mat[5,4] * rU_Opt_Seq[1,4]) + (rB_Mat[5,5] * rU_Opt_Seq[1,5]);
rX_Pred_Horizon[1, 6] := (rA_Mat[6,1] * a_x_hat[1]) + (rA_Mat[6,2] * a_x_hat[2]) + (rA_Mat[6,3] * a_x_hat[3]) + (rA_Mat[6,4] * a_x_hat[4]) + (rA_Mat[6,5] * a_x_hat[5]) + (rA_Mat[6,6] * a_x_hat[6]) + (rB_Mat[6,1] * rU_Opt_Seq[1,1]) + (rB_Mat[6,2] * rU_Opt_Seq[1,2]) + (rB_Mat[6,3] * rU_Opt_Seq[1,3]) + (rB_Mat[6,4] * rU_Opt_Seq[1,4]) + (rB_Mat[6,5] * rU_Opt_Seq[1,5]);

(* Iteration 1 - Forward State Prediction Step 2 (h=2): x_2 = A * x_1 + B * u_2 *)
rX_Pred_Horizon[2, 1] := (rA_Mat[1,1] * rX_Pred_Horizon[1,1]) + (rA_Mat[1,2] * rX_Pred_Horizon[1,2]) + (rA_Mat[1,3] * rX_Pred_Horizon[1,3]) + (rA_Mat[1,4] * rX_Pred_Horizon[1,4]) + (rA_Mat[1,5] * rX_Pred_Horizon[1,5]) + (rA_Mat[1,6] * rX_Pred_Horizon[1,6]) + (rB_Mat[1,1] * rU_Opt_Seq[2,1]) + (rB_Mat[1,2] * rU_Opt_Seq[2,2]) + (rB_Mat[1,3] * rU_Opt_Seq[2,3]) + (rB_Mat[1,4] * rU_Opt_Seq[2,4]) + (rB_Mat[1,5] * rU_Opt_Seq[2,5]);
rX_Pred_Horizon[2, 2] := (rA_Mat[2,1] * rX_Pred_Horizon[1,1]) + (rA_Mat[2,2] * rX_Pred_Horizon[1,2]) + (rA_Mat[2,3] * rX_Pred_Horizon[1,3]) + (rA_Mat[2,4] * rX_Pred_Horizon[1,4]) + (rA_Mat[2,5] * rX_Pred_Horizon[1,5]) + (rA_Mat[2,6] * rX_Pred_Horizon[1,6]) + (rB_Mat[2,1] * rU_Opt_Seq[2,1]) + (rB_Mat[2,2] * rU_Opt_Seq[2,2]) + (rB_Mat[2,3] * rU_Opt_Seq[2,3]) + (rB_Mat[2,4] * rU_Opt_Seq[2,4]) + (rB_Mat[2,5] * rU_Opt_Seq[2,5]);
rX_Pred_Horizon[2, 3] := (rA_Mat[3,1] * rX_Pred_Horizon[1,1]) + (rA_Mat[3,2] * rX_Pred_Horizon[1,2]) + (rA_Mat[3,3] * rX_Pred_Horizon[1,3]) + (rA_Mat[3,4] * rX_Pred_Horizon[1,4]) + (rA_Mat[3,5] * rX_Pred_Horizon[1,5]) + (rA_Mat[3,6] * rX_Pred_Horizon[1,6]) + (rB_Mat[3,1] * rU_Opt_Seq[2,1]) + (rB_Mat[3,2] * rU_Opt_Seq[2,2]) + (rB_Mat[3,3] * rU_Opt_Seq[2,3]) + (rB_Mat[3,4] * rU_Opt_Seq[2,4]) + (rB_Mat[3,5] * rU_Opt_Seq[2,5]);
rX_Pred_Horizon[2, 4] := (rA_Mat[4,1] * rX_Pred_Horizon[1,1]) + (rA_Mat[4,2] * rX_Pred_Horizon[1,2]) + (rA_Mat[4,3] * rX_Pred_Horizon[1,3]) + (rA_Mat[4,4] * rX_Pred_Horizon[1,4]) + (rA_Mat[4,5] * rX_Pred_Horizon[1,5]) + (rA_Mat[4,6] * rX_Pred_Horizon[1,6]) + (rB_Mat[4,1] * rU_Opt_Seq[2,1]) + (rB_Mat[4,2] * rU_Opt_Seq[2,2]) + (rB_Mat[4,3] * rU_Opt_Seq[2,3]) + (rB_Mat[4,4] * rU_Opt_Seq[2,4]) + (rB_Mat[4,5] * rU_Opt_Seq[2,5]);
rX_Pred_Horizon[2, 5] := (rA_Mat[5,1] * rX_Pred_Horizon[1,1]) + (rA_Mat[5,2] * rX_Pred_Horizon[1,2]) + (rA_Mat[5,3] * rX_Pred_Horizon[1,3]) + (rA_Mat[5,4] * rX_Pred_Horizon[1,4]) + (rA_Mat[5,5] * rX_Pred_Horizon[1,5]) + (rA_Mat[5,6] * rX_Pred_Horizon[1,6]) + (rB_Mat[5,1] * rU_Opt_Seq[2,1]) + (rB_Mat[5,2] * rU_Opt_Seq[2,2]) + (rB_Mat[5,3] * rU_Opt_Seq[2,3]) + (rB_Mat[5,4] * rU_Opt_Seq[2,4]) + (rB_Mat[5,5] * rU_Opt_Seq[2,5]);
rX_Pred_Horizon[2, 6] := (rA_Mat[6,1] * rX_Pred_Horizon[1,1]) + (rA_Mat[6,2] * rX_Pred_Horizon[1,2]) + (rA_Mat[6,3] * rX_Pred_Horizon[1,3]) + (rA_Mat[6,4] * rX_Pred_Horizon[1,4]) + (rA_Mat[6,5] * rX_Pred_Horizon[1,5]) + (rA_Mat[6,6] * rX_Pred_Horizon[1,6]) + (rB_Mat[6,1] * rU_Opt_Seq[2,1]) + (rB_Mat[6,2] * rU_Opt_Seq[2,2]) + (rB_Mat[6,3] * rU_Opt_Seq[2,3]) + (rB_Mat[6,4] * rU_Opt_Seq[2,4]) + (rB_Mat[6,5] * rU_Opt_Seq[2,5]);

(* Iteration 1 - Forward State Prediction Step 3 (h=3): x_3 = A * x_2 + B * u_3 *)
rX_Pred_Horizon[3, 1] := (rA_Mat[1,1] * rX_Pred_Horizon[2,1]) + (rA_Mat[1,2] * rX_Pred_Horizon[2,2]) + (rA_Mat[1,3] * rX_Pred_Horizon[2,3]) + (rA_Mat[1,4] * rX_Pred_Horizon[2,4]) + (rA_Mat[1,5] * rX_Pred_Horizon[2,5]) + (rA_Mat[1,6] * rX_Pred_Horizon[2,6]) + (rB_Mat[1,1] * rU_Opt_Seq[3,1]) + (rB_Mat[1,2] * rU_Opt_Seq[3,2]) + (rB_Mat[1,3] * rU_Opt_Seq[3,3]) + (rB_Mat[1,4] * rU_Opt_Seq[3,4]) + (rB_Mat[1,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[3, 2] := (rA_Mat[2,1] * rX_Pred_Horizon[2,1]) + (rA_Mat[2,2] * rX_Pred_Horizon[2,2]) + (rA_Mat[2,3] * rX_Pred_Horizon[2,3]) + (rA_Mat[2,4] * rX_Pred_Horizon[2,4]) + (rA_Mat[2,5] * rX_Pred_Horizon[2,5]) + (rA_Mat[2,6] * rX_Pred_Horizon[2,6]) + (rB_Mat[2,1] * rU_Opt_Seq[3,1]) + (rB_Mat[2,2] * rU_Opt_Seq[3,2]) + (rB_Mat[2,3] * rU_Opt_Seq[3,3]) + (rB_Mat[2,4] * rU_Opt_Seq[3,4]) + (rB_Mat[2,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[3, 3] := (rA_Mat[3,1] * rX_Pred_Horizon[2,1]) + (rA_Mat[3,2] * rX_Pred_Horizon[2,2]) + (rA_Mat[3,3] * rX_Pred_Horizon[2,3]) + (rA_Mat[3,4] * rX_Pred_Horizon[2,4]) + (rA_Mat[3,5] * rX_Pred_Horizon[2,5]) + (rA_Mat[3,6] * rX_Pred_Horizon[2,6]) + (rB_Mat[3,1] * rU_Opt_Seq[3,1]) + (rB_Mat[3,2] * rU_Opt_Seq[3,2]) + (rB_Mat[3,3] * rU_Opt_Seq[3,3]) + (rB_Mat[3,4] * rU_Opt_Seq[3,4]) + (rB_Mat[3,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[3, 4] := (rA_Mat[4,1] * rX_Pred_Horizon[2,1]) + (rA_Mat[4,2] * rX_Pred_Horizon[2,2]) + (rA_Mat[4,3] * rX_Pred_Horizon[2,3]) + (rA_Mat[4,4] * rX_Pred_Horizon[2,4]) + (rA_Mat[4,5] * rX_Pred_Horizon[2,5]) + (rA_Mat[4,6] * rX_Pred_Horizon[2,6]) + (rB_Mat[4,1] * rU_Opt_Seq[3,1]) + (rB_Mat[4,2] * rU_Opt_Seq[3,2]) + (rB_Mat[4,3] * rU_Opt_Seq[3,3]) + (rB_Mat[4,4] * rU_Opt_Seq[3,4]) + (rB_Mat[4,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[3, 5] := (rA_Mat[5,1] * rX_Pred_Horizon[2,1]) + (rA_Mat[5,2] * rX_Pred_Horizon[2,2]) + (rA_Mat[5,3] * rX_Pred_Horizon[2,3]) + (rA_Mat[5,4] * rX_Pred_Horizon[2,4]) + (rA_Mat[5,5] * rX_Pred_Horizon[2,5]) + (rA_Mat[5,6] * rX_Pred_Horizon[2,6]) + (rB_Mat[5,1] * rU_Opt_Seq[3,1]) + (rB_Mat[5,2] * rU_Opt_Seq[3,2]) + (rB_Mat[5,3] * rU_Opt_Seq[3,3]) + (rB_Mat[5,4] * rU_Opt_Seq[3,4]) + (rB_Mat[5,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[3, 6] := (rA_Mat[6,1] * rX_Pred_Horizon[2,1]) + (rA_Mat[6,2] * rX_Pred_Horizon[2,2]) + (rA_Mat[6,3] * rX_Pred_Horizon[2,3]) + (rA_Mat[6,4] * rX_Pred_Horizon[2,4]) + (rA_Mat[6,5] * rX_Pred_Horizon[2,5]) + (rA_Mat[6,6] * rX_Pred_Horizon[2,6]) + (rB_Mat[6,1] * rU_Opt_Seq[3,1]) + (rB_Mat[6,2] * rU_Opt_Seq[3,2]) + (rB_Mat[6,3] * rU_Opt_Seq[3,3]) + (rB_Mat[6,4] * rU_Opt_Seq[3,4]) + (rB_Mat[6,5] * rU_Opt_Seq[3,5]);

(* Iteration 1 - Forward State Prediction Step 4 (h=4): x_4 = A * x_3 + B * u_3 (held beyond Hu) *)
rX_Pred_Horizon[4, 1] := (rA_Mat[1,1] * rX_Pred_Horizon[3,1]) + (rA_Mat[1,2] * rX_Pred_Horizon[3,2]) + (rA_Mat[1,3] * rX_Pred_Horizon[3,3]) + (rA_Mat[1,4] * rX_Pred_Horizon[3,4]) + (rA_Mat[1,5] * rX_Pred_Horizon[3,5]) + (rA_Mat[1,6] * rX_Pred_Horizon[3,6]) + (rB_Mat[1,1] * rU_Opt_Seq[3,1]) + (rB_Mat[1,2] * rU_Opt_Seq[3,2]) + (rB_Mat[1,3] * rU_Opt_Seq[3,3]) + (rB_Mat[1,4] * rU_Opt_Seq[3,4]) + (rB_Mat[1,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[4, 2] := (rA_Mat[2,1] * rX_Pred_Horizon[3,1]) + (rA_Mat[2,2] * rX_Pred_Horizon[3,2]) + (rA_Mat[2,3] * rX_Pred_Horizon[3,3]) + (rA_Mat[2,4] * rX_Pred_Horizon[3,4]) + (rA_Mat[2,5] * rX_Pred_Horizon[3,5]) + (rA_Mat[2,6] * rX_Pred_Horizon[3,6]) + (rB_Mat[2,1] * rU_Opt_Seq[3,1]) + (rB_Mat[2,2] * rU_Opt_Seq[3,2]) + (rB_Mat[2,3] * rU_Opt_Seq[3,3]) + (rB_Mat[2,4] * rU_Opt_Seq[3,4]) + (rB_Mat[2,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[4, 3] := (rA_Mat[3,1] * rX_Pred_Horizon[3,1]) + (rA_Mat[3,2] * rX_Pred_Horizon[3,2]) + (rA_Mat[3,3] * rX_Pred_Horizon[3,3]) + (rA_Mat[3,4] * rX_Pred_Horizon[3,4]) + (rA_Mat[3,5] * rX_Pred_Horizon[3,5]) + (rA_Mat[3,6] * rX_Pred_Horizon[3,6]) + (rB_Mat[3,1] * rU_Opt_Seq[3,1]) + (rB_Mat[3,2] * rU_Opt_Seq[3,2]) + (rB_Mat[3,3] * rU_Opt_Seq[3,3]) + (rB_Mat[3,4] * rU_Opt_Seq[3,4]) + (rB_Mat[3,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[4, 4] := (rA_Mat[4,1] * rX_Pred_Horizon[3,1]) + (rA_Mat[4,2] * rX_Pred_Horizon[3,2]) + (rA_Mat[4,3] * rX_Pred_Horizon[3,3]) + (rA_Mat[4,4] * rX_Pred_Horizon[3,4]) + (rA_Mat[4,5] * rX_Pred_Horizon[3,5]) + (rA_Mat[4,6] * rX_Pred_Horizon[3,6]) + (rB_Mat[4,1] * rU_Opt_Seq[3,1]) + (rB_Mat[4,2] * rU_Opt_Seq[3,2]) + (rB_Mat[4,3] * rU_Opt_Seq[3,3]) + (rB_Mat[4,4] * rU_Opt_Seq[3,4]) + (rB_Mat[4,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[4, 5] := (rA_Mat[5,1] * rX_Pred_Horizon[3,1]) + (rA_Mat[5,2] * rX_Pred_Horizon[3,2]) + (rA_Mat[5,3] * rX_Pred_Horizon[3,3]) + (rA_Mat[5,4] * rX_Pred_Horizon[3,4]) + (rA_Mat[5,5] * rX_Pred_Horizon[3,5]) + (rA_Mat[5,6] * rX_Pred_Horizon[3,6]) + (rB_Mat[5,1] * rU_Opt_Seq[3,1]) + (rB_Mat[5,2] * rU_Opt_Seq[3,2]) + (rB_Mat[5,3] * rU_Opt_Seq[3,3]) + (rB_Mat[5,4] * rU_Opt_Seq[3,4]) + (rB_Mat[5,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[4, 6] := (rA_Mat[6,1] * rX_Pred_Horizon[3,1]) + (rA_Mat[6,2] * rX_Pred_Horizon[3,2]) + (rA_Mat[6,3] * rX_Pred_Horizon[3,3]) + (rA_Mat[6,4] * rX_Pred_Horizon[3,4]) + (rA_Mat[6,5] * rX_Pred_Horizon[3,5]) + (rA_Mat[6,6] * rX_Pred_Horizon[3,6]) + (rB_Mat[6,1] * rU_Opt_Seq[3,1]) + (rB_Mat[6,2] * rU_Opt_Seq[3,2]) + (rB_Mat[6,3] * rU_Opt_Seq[3,3]) + (rB_Mat[6,4] * rU_Opt_Seq[3,4]) + (rB_Mat[6,5] * rU_Opt_Seq[3,5]);

(* Iteration 1 - Forward State Prediction Step 5 (h=5): x_5 = A * x_4 + B * u_3 (held beyond Hu) *)
rX_Pred_Horizon[5, 1] := (rA_Mat[1,1] * rX_Pred_Horizon[4,1]) + (rA_Mat[1,2] * rX_Pred_Horizon[4,2]) + (rA_Mat[1,3] * rX_Pred_Horizon[4,3]) + (rA_Mat[1,4] * rX_Pred_Horizon[4,4]) + (rA_Mat[1,5] * rX_Pred_Horizon[4,5]) + (rA_Mat[1,6] * rX_Pred_Horizon[4,6]) + (rB_Mat[1,1] * rU_Opt_Seq[3,1]) + (rB_Mat[1,2] * rU_Opt_Seq[3,2]) + (rB_Mat[1,3] * rU_Opt_Seq[3,3]) + (rB_Mat[1,4] * rU_Opt_Seq[3,4]) + (rB_Mat[1,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[5, 2] := (rA_Mat[2,1] * rX_Pred_Horizon[4,1]) + (rA_Mat[2,2] * rX_Pred_Horizon[4,2]) + (rA_Mat[2,3] * rX_Pred_Horizon[4,3]) + (rA_Mat[2,4] * rX_Pred_Horizon[4,4]) + (rA_Mat[2,5] * rX_Pred_Horizon[4,5]) + (rA_Mat[2,6] * rX_Pred_Horizon[4,6]) + (rB_Mat[2,1] * rU_Opt_Seq[3,1]) + (rB_Mat[2,2] * rU_Opt_Seq[3,2]) + (rB_Mat[2,3] * rU_Opt_Seq[3,3]) + (rB_Mat[2,4] * rU_Opt_Seq[3,4]) + (rB_Mat[2,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[5, 3] := (rA_Mat[3,1] * rX_Pred_Horizon[4,1]) + (rA_Mat[3,2] * rX_Pred_Horizon[4,2]) + (rA_Mat[3,3] * rX_Pred_Horizon[4,3]) + (rA_Mat[3,4] * rX_Pred_Horizon[4,4]) + (rA_Mat[3,5] * rX_Pred_Horizon[4,5]) + (rA_Mat[3,6] * rX_Pred_Horizon[4,6]) + (rB_Mat[3,1] * rU_Opt_Seq[3,1]) + (rB_Mat[3,2] * rU_Opt_Seq[3,2]) + (rB_Mat[3,3] * rU_Opt_Seq[3,3]) + (rB_Mat[3,4] * rU_Opt_Seq[3,4]) + (rB_Mat[3,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[5, 4] := (rA_Mat[4,1] * rX_Pred_Horizon[4,1]) + (rA_Mat[4,2] * rX_Pred_Horizon[4,2]) + (rA_Mat[4,3] * rX_Pred_Horizon[4,3]) + (rA_Mat[4,4] * rX_Pred_Horizon[4,4]) + (rA_Mat[4,5] * rX_Pred_Horizon[4,5]) + (rA_Mat[4,6] * rX_Pred_Horizon[4,6]) + (rB_Mat[4,1] * rU_Opt_Seq[3,1]) + (rB_Mat[4,2] * rU_Opt_Seq[3,2]) + (rB_Mat[4,3] * rU_Opt_Seq[3,3]) + (rB_Mat[4,4] * rU_Opt_Seq[3,4]) + (rB_Mat[4,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[5, 5] := (rA_Mat[5,1] * rX_Pred_Horizon[4,1]) + (rA_Mat[5,2] * rX_Pred_Horizon[4,2]) + (rA_Mat[5,3] * rX_Pred_Horizon[4,3]) + (rA_Mat[5,4] * rX_Pred_Horizon[4,4]) + (rA_Mat[5,5] * rX_Pred_Horizon[4,5]) + (rA_Mat[5,6] * rX_Pred_Horizon[4,6]) + (rB_Mat[5,1] * rU_Opt_Seq[3,1]) + (rB_Mat[5,2] * rU_Opt_Seq[3,2]) + (rB_Mat[5,3] * rU_Opt_Seq[3,3]) + (rB_Mat[5,4] * rU_Opt_Seq[3,4]) + (rB_Mat[5,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[5, 6] := (rA_Mat[6,1] * rX_Pred_Horizon[4,1]) + (rA_Mat[6,2] * rX_Pred_Horizon[4,2]) + (rA_Mat[6,3] * rX_Pred_Horizon[4,3]) + (rA_Mat[6,4] * rX_Pred_Horizon[4,4]) + (rA_Mat[6,5] * rX_Pred_Horizon[4,5]) + (rA_Mat[6,6] * rX_Pred_Horizon[4,6]) + (rB_Mat[6,1] * rU_Opt_Seq[3,1]) + (rB_Mat[6,2] * rU_Opt_Seq[3,2]) + (rB_Mat[6,3] * rU_Opt_Seq[3,3]) + (rB_Mat[6,4] * rU_Opt_Seq[3,4]) + (rB_Mat[6,5] * rU_Opt_Seq[3,5]);

(* Iteration 1 - Evaluate Objective Function Cost J *)
rMPC_Cost_J := 0.0;
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[1] * (rX_Pred_Horizon[1,1] - rX_Target[1,1]) * (rX_Pred_Horizon[1,1] - rX_Target[1,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[2] * (rX_Pred_Horizon[1,2] - rX_Target[1,2]) * (rX_Pred_Horizon[1,2] - rX_Target[1,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[3] * (rX_Pred_Horizon[1,3] - rX_Target[1,3]) * (rX_Pred_Horizon[1,3] - rX_Target[1,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[4] * (rX_Pred_Horizon[1,4] - rX_Target[1,4]) * (rX_Pred_Horizon[1,4] - rX_Target[1,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[5] * (rX_Pred_Horizon[1,5] - rX_Target[1,5]) * (rX_Pred_Horizon[1,5] - rX_Target[1,5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[6] * (rX_Pred_Horizon[1,6] - rX_Target[1,6]) * (rX_Pred_Horizon[1,6] - rX_Target[1,6]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[1] * (rX_Pred_Horizon[2,1] - rX_Target[2,1]) * (rX_Pred_Horizon[2,1] - rX_Target[2,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[2] * (rX_Pred_Horizon[2,2] - rX_Target[2,2]) * (rX_Pred_Horizon[2,2] - rX_Target[2,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[3] * (rX_Pred_Horizon[2,3] - rX_Target[2,3]) * (rX_Pred_Horizon[2,3] - rX_Target[2,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[4] * (rX_Pred_Horizon[2,4] - rX_Target[2,4]) * (rX_Pred_Horizon[2,4] - rX_Target[2,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[5] * (rX_Pred_Horizon[2,5] - rX_Target[2,5]) * (rX_Pred_Horizon[2,5] - rX_Target[2,5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[6] * (rX_Pred_Horizon[2,6] - rX_Target[2,6]) * (rX_Pred_Horizon[2,6] - rX_Target[2,6]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[1] * (rX_Pred_Horizon[3,1] - rX_Target[3,1]) * (rX_Pred_Horizon[3,1] - rX_Target[3,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[2] * (rX_Pred_Horizon[3,2] - rX_Target[3,2]) * (rX_Pred_Horizon[3,2] - rX_Target[3,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[3] * (rX_Pred_Horizon[3,3] - rX_Target[3,3]) * (rX_Pred_Horizon[3,3] - rX_Target[3,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[4] * (rX_Pred_Horizon[3,4] - rX_Target[3,4]) * (rX_Pred_Horizon[3,4] - rX_Target[3,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[5] * (rX_Pred_Horizon[3,5] - rX_Target[3,5]) * (rX_Pred_Horizon[3,5] - rX_Target[3,5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[6] * (rX_Pred_Horizon[3,6] - rX_Target[3,6]) * (rX_Pred_Horizon[3,6] - rX_Target[3,6]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[1] * (rX_Pred_Horizon[4,1] - rX_Target[4,1]) * (rX_Pred_Horizon[4,1] - rX_Target[4,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[2] * (rX_Pred_Horizon[4,2] - rX_Target[4,2]) * (rX_Pred_Horizon[4,2] - rX_Target[4,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[3] * (rX_Pred_Horizon[4,3] - rX_Target[4,3]) * (rX_Pred_Horizon[4,3] - rX_Target[4,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[4] * (rX_Pred_Horizon[4,4] - rX_Target[4,4]) * (rX_Pred_Horizon[4,4] - rX_Target[4,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[5] * (rX_Pred_Horizon[4,5] - rX_Target[4,5]) * (rX_Pred_Horizon[4,5] - rX_Target[4,5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[6] * (rX_Pred_Horizon[4,6] - rX_Target[4,6]) * (rX_Pred_Horizon[4,6] - rX_Target[4,6]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[1] * (rX_Pred_Horizon[5,1] - rX_Target[5,1]) * (rX_Pred_Horizon[5,1] - rX_Target[5,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[2] * (rX_Pred_Horizon[5,2] - rX_Target[5,2]) * (rX_Pred_Horizon[5,2] - rX_Target[5,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[3] * (rX_Pred_Horizon[5,3] - rX_Target[5,3]) * (rX_Pred_Horizon[5,3] - rX_Target[5,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[4] * (rX_Pred_Horizon[5,4] - rX_Target[5,4]) * (rX_Pred_Horizon[5,4] - rX_Target[5,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[5] * (rX_Pred_Horizon[5,5] - rX_Target[5,5]) * (rX_Pred_Horizon[5,5] - rX_Target[5,5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[6] * (rX_Pred_Horizon[5,6] - rX_Target[5,6]) * (rX_Pred_Horizon[5,6] - rX_Target[5,6]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rP_Diag[1] * (rX_Pred_Horizon[5,1] - rX_Target[5,1]) * (rX_Pred_Horizon[5,1] - rX_Target[5,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rP_Diag[2] * (rX_Pred_Horizon[5,2] - rX_Target[5,2]) * (rX_Pred_Horizon[5,2] - rX_Target[5,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rP_Diag[3] * (rX_Pred_Horizon[5,3] - rX_Target[5,3]) * (rX_Pred_Horizon[5,3] - rX_Target[5,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rP_Diag[4] * (rX_Pred_Horizon[5,4] - rX_Target[5,4]) * (rX_Pred_Horizon[5,4] - rX_Target[5,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rP_Diag[5] * (rX_Pred_Horizon[5,5] - rX_Target[5,5]) * (rX_Pred_Horizon[5,5] - rX_Target[5,5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rP_Diag[6] * (rX_Pred_Horizon[5,6] - rX_Target[5,6]) * (rX_Pred_Horizon[5,6] - rX_Target[5,6]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[1] * rU_Opt_Seq[1,1] * rU_Opt_Seq[1,1]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[2] * rU_Opt_Seq[1,2] * rU_Opt_Seq[1,2]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[3] * rU_Opt_Seq[1,3] * rU_Opt_Seq[1,3]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[4] * rU_Opt_Seq[1,4] * rU_Opt_Seq[1,4]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[5] * rU_Opt_Seq[1,5] * rU_Opt_Seq[1,5]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[1] * rU_Opt_Seq[2,1] * rU_Opt_Seq[2,1]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[2] * rU_Opt_Seq[2,2] * rU_Opt_Seq[2,2]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[3] * rU_Opt_Seq[2,3] * rU_Opt_Seq[2,3]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[4] * rU_Opt_Seq[2,4] * rU_Opt_Seq[2,4]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[5] * rU_Opt_Seq[2,5] * rU_Opt_Seq[2,5]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[1] * rU_Opt_Seq[3,1] * rU_Opt_Seq[3,1]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[2] * rU_Opt_Seq[3,2] * rU_Opt_Seq[3,2]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[3] * rU_Opt_Seq[3,3] * rU_Opt_Seq[3,3]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[4] * rU_Opt_Seq[3,4] * rU_Opt_Seq[3,4]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[5] * rU_Opt_Seq[3,5] * rU_Opt_Seq[3,5]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[1] * (rU_Opt_Seq[1,1] - a_u_prev[1]) * (rU_Opt_Seq[1,1] - a_u_prev[1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[1] * (rU_Opt_Seq[2,1] - rU_Opt_Seq[1,1]) * (rU_Opt_Seq[2,1] - rU_Opt_Seq[1,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[1] * (rU_Opt_Seq[3,1] - rU_Opt_Seq[2,1]) * (rU_Opt_Seq[3,1] - rU_Opt_Seq[2,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[2] * (rU_Opt_Seq[1,2] - a_u_prev[2]) * (rU_Opt_Seq[1,2] - a_u_prev[2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[2] * (rU_Opt_Seq[2,2] - rU_Opt_Seq[1,2]) * (rU_Opt_Seq[2,2] - rU_Opt_Seq[1,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[2] * (rU_Opt_Seq[3,2] - rU_Opt_Seq[2,2]) * (rU_Opt_Seq[3,2] - rU_Opt_Seq[2,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[3] * (rU_Opt_Seq[1,3] - a_u_prev[3]) * (rU_Opt_Seq[1,3] - a_u_prev[3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[3] * (rU_Opt_Seq[2,3] - rU_Opt_Seq[1,3]) * (rU_Opt_Seq[2,3] - rU_Opt_Seq[1,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[3] * (rU_Opt_Seq[3,3] - rU_Opt_Seq[2,3]) * (rU_Opt_Seq[3,3] - rU_Opt_Seq[2,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[4] * (rU_Opt_Seq[1,4] - a_u_prev[4]) * (rU_Opt_Seq[1,4] - a_u_prev[4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[4] * (rU_Opt_Seq[2,4] - rU_Opt_Seq[1,4]) * (rU_Opt_Seq[2,4] - rU_Opt_Seq[1,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[4] * (rU_Opt_Seq[3,4] - rU_Opt_Seq[2,4]) * (rU_Opt_Seq[3,4] - rU_Opt_Seq[2,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[5] * (rU_Opt_Seq[1,5] - a_u_prev[5]) * (rU_Opt_Seq[1,5] - a_u_prev[5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[5] * (rU_Opt_Seq[2,5] - rU_Opt_Seq[1,5]) * (rU_Opt_Seq[2,5] - rU_Opt_Seq[1,5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[5] * (rU_Opt_Seq[3,5] - rU_Opt_Seq[2,5]) * (rU_Opt_Seq[3,5] - rU_Opt_Seq[2,5]));

(* Iteration 1 - Backward Adjoint Costate Propagation: lambda_h = A^T * lambda_{h+1} + Q * (x_h - x_ref) *)
(* Terminal Costate at h=5: lambda_5 = (P + Q) * (x_5 - x_target_5) *)
rLambda_Costate[5, 1] := (rP_Diag[1] + rQ_Diag[1]) * (rX_Pred_Horizon[5,1] - rX_Target[5,1]);
rLambda_Costate[5, 2] := (rP_Diag[2] + rQ_Diag[2]) * (rX_Pred_Horizon[5,2] - rX_Target[5,2]);
rLambda_Costate[5, 3] := (rP_Diag[3] + rQ_Diag[3]) * (rX_Pred_Horizon[5,3] - rX_Target[5,3]);
rLambda_Costate[5, 4] := (rP_Diag[4] + rQ_Diag[4]) * (rX_Pred_Horizon[5,4] - rX_Target[5,4]);
rLambda_Costate[5, 5] := (rP_Diag[5] + rQ_Diag[5]) * (rX_Pred_Horizon[5,5] - rX_Target[5,5]);
rLambda_Costate[5, 6] := (rP_Diag[6] + rQ_Diag[6]) * (rX_Pred_Horizon[5,6] - rX_Target[5,6]);

(* Adjoint Costate at h=4: lambda_4 = A^T * lambda_5 + Q * (x_4 - x_target_4) *)
rLambda_Costate[4, 1] := (rA_Mat[1,1] * rLambda_Costate[5,1]) + (rA_Mat[2,1] * rLambda_Costate[5,2]) + (rA_Mat[3,1] * rLambda_Costate[5,3]) + (rA_Mat[4,1] * rLambda_Costate[5,4]) + (rA_Mat[5,1] * rLambda_Costate[5,5]) + (rA_Mat[6,1] * rLambda_Costate[5,6]) + (rQ_Diag[1] * (rX_Pred_Horizon[4,1] - rX_Target[4,1]));
rLambda_Costate[4, 2] := (rA_Mat[1,2] * rLambda_Costate[5,1]) + (rA_Mat[2,2] * rLambda_Costate[5,2]) + (rA_Mat[3,2] * rLambda_Costate[5,3]) + (rA_Mat[4,2] * rLambda_Costate[5,4]) + (rA_Mat[5,2] * rLambda_Costate[5,5]) + (rA_Mat[6,2] * rLambda_Costate[5,6]) + (rQ_Diag[2] * (rX_Pred_Horizon[4,2] - rX_Target[4,2]));
rLambda_Costate[4, 3] := (rA_Mat[1,3] * rLambda_Costate[5,1]) + (rA_Mat[2,3] * rLambda_Costate[5,2]) + (rA_Mat[3,3] * rLambda_Costate[5,3]) + (rA_Mat[4,3] * rLambda_Costate[5,4]) + (rA_Mat[5,3] * rLambda_Costate[5,5]) + (rA_Mat[6,3] * rLambda_Costate[5,6]) + (rQ_Diag[3] * (rX_Pred_Horizon[4,3] - rX_Target[4,3]));
rLambda_Costate[4, 4] := (rA_Mat[1,4] * rLambda_Costate[5,1]) + (rA_Mat[2,4] * rLambda_Costate[5,2]) + (rA_Mat[3,4] * rLambda_Costate[5,3]) + (rA_Mat[4,4] * rLambda_Costate[5,4]) + (rA_Mat[5,4] * rLambda_Costate[5,5]) + (rA_Mat[6,4] * rLambda_Costate[5,6]) + (rQ_Diag[4] * (rX_Pred_Horizon[4,4] - rX_Target[4,4]));
rLambda_Costate[4, 5] := (rA_Mat[1,5] * rLambda_Costate[5,1]) + (rA_Mat[2,5] * rLambda_Costate[5,2]) + (rA_Mat[3,5] * rLambda_Costate[5,3]) + (rA_Mat[4,5] * rLambda_Costate[5,4]) + (rA_Mat[5,5] * rLambda_Costate[5,5]) + (rA_Mat[6,5] * rLambda_Costate[5,6]) + (rQ_Diag[5] * (rX_Pred_Horizon[4,5] - rX_Target[4,5]));
rLambda_Costate[4, 6] := (rA_Mat[1,6] * rLambda_Costate[5,1]) + (rA_Mat[2,6] * rLambda_Costate[5,2]) + (rA_Mat[3,6] * rLambda_Costate[5,3]) + (rA_Mat[4,6] * rLambda_Costate[5,4]) + (rA_Mat[5,6] * rLambda_Costate[5,5]) + (rA_Mat[6,6] * rLambda_Costate[5,6]) + (rQ_Diag[6] * (rX_Pred_Horizon[4,6] - rX_Target[4,6]));

(* Adjoint Costate at h=3: lambda_3 = A^T * lambda_4 + Q * (x_3 - x_target_3) *)
rLambda_Costate[3, 1] := (rA_Mat[1,1] * rLambda_Costate[4,1]) + (rA_Mat[2,1] * rLambda_Costate[4,2]) + (rA_Mat[3,1] * rLambda_Costate[4,3]) + (rA_Mat[4,1] * rLambda_Costate[4,4]) + (rA_Mat[5,1] * rLambda_Costate[4,5]) + (rA_Mat[6,1] * rLambda_Costate[4,6]) + (rQ_Diag[1] * (rX_Pred_Horizon[3,1] - rX_Target[3,1]));
rLambda_Costate[3, 2] := (rA_Mat[1,2] * rLambda_Costate[4,1]) + (rA_Mat[2,2] * rLambda_Costate[4,2]) + (rA_Mat[3,2] * rLambda_Costate[4,3]) + (rA_Mat[4,2] * rLambda_Costate[4,4]) + (rA_Mat[5,2] * rLambda_Costate[4,5]) + (rA_Mat[6,2] * rLambda_Costate[4,6]) + (rQ_Diag[2] * (rX_Pred_Horizon[3,2] - rX_Target[3,2]));
rLambda_Costate[3, 3] := (rA_Mat[1,3] * rLambda_Costate[4,1]) + (rA_Mat[2,3] * rLambda_Costate[4,2]) + (rA_Mat[3,3] * rLambda_Costate[4,3]) + (rA_Mat[4,3] * rLambda_Costate[4,4]) + (rA_Mat[5,3] * rLambda_Costate[4,5]) + (rA_Mat[6,3] * rLambda_Costate[4,6]) + (rQ_Diag[3] * (rX_Pred_Horizon[3,3] - rX_Target[3,3]));
rLambda_Costate[3, 4] := (rA_Mat[1,4] * rLambda_Costate[4,1]) + (rA_Mat[2,4] * rLambda_Costate[4,2]) + (rA_Mat[3,4] * rLambda_Costate[4,3]) + (rA_Mat[4,4] * rLambda_Costate[4,4]) + (rA_Mat[5,4] * rLambda_Costate[4,5]) + (rA_Mat[6,4] * rLambda_Costate[4,6]) + (rQ_Diag[4] * (rX_Pred_Horizon[3,4] - rX_Target[3,4]));
rLambda_Costate[3, 5] := (rA_Mat[1,5] * rLambda_Costate[4,1]) + (rA_Mat[2,5] * rLambda_Costate[4,2]) + (rA_Mat[3,5] * rLambda_Costate[4,3]) + (rA_Mat[4,5] * rLambda_Costate[4,4]) + (rA_Mat[5,5] * rLambda_Costate[4,5]) + (rA_Mat[6,5] * rLambda_Costate[4,6]) + (rQ_Diag[5] * (rX_Pred_Horizon[3,5] - rX_Target[3,5]));
rLambda_Costate[3, 6] := (rA_Mat[1,6] * rLambda_Costate[4,1]) + (rA_Mat[2,6] * rLambda_Costate[4,2]) + (rA_Mat[3,6] * rLambda_Costate[4,3]) + (rA_Mat[4,6] * rLambda_Costate[4,4]) + (rA_Mat[5,6] * rLambda_Costate[4,5]) + (rA_Mat[6,6] * rLambda_Costate[4,6]) + (rQ_Diag[6] * (rX_Pred_Horizon[3,6] - rX_Target[3,6]));

(* Adjoint Costate at h=2: lambda_2 = A^T * lambda_3 + Q * (x_2 - x_target_2) *)
rLambda_Costate[2, 1] := (rA_Mat[1,1] * rLambda_Costate[3,1]) + (rA_Mat[2,1] * rLambda_Costate[3,2]) + (rA_Mat[3,1] * rLambda_Costate[3,3]) + (rA_Mat[4,1] * rLambda_Costate[3,4]) + (rA_Mat[5,1] * rLambda_Costate[3,5]) + (rA_Mat[6,1] * rLambda_Costate[3,6]) + (rQ_Diag[1] * (rX_Pred_Horizon[2,1] - rX_Target[2,1]));
rLambda_Costate[2, 2] := (rA_Mat[1,2] * rLambda_Costate[3,1]) + (rA_Mat[2,2] * rLambda_Costate[3,2]) + (rA_Mat[3,2] * rLambda_Costate[3,3]) + (rA_Mat[4,2] * rLambda_Costate[3,4]) + (rA_Mat[5,2] * rLambda_Costate[3,5]) + (rA_Mat[6,2] * rLambda_Costate[3,6]) + (rQ_Diag[2] * (rX_Pred_Horizon[2,2] - rX_Target[2,2]));
rLambda_Costate[2, 3] := (rA_Mat[1,3] * rLambda_Costate[3,1]) + (rA_Mat[2,3] * rLambda_Costate[3,2]) + (rA_Mat[3,3] * rLambda_Costate[3,3]) + (rA_Mat[4,3] * rLambda_Costate[3,4]) + (rA_Mat[5,3] * rLambda_Costate[3,5]) + (rA_Mat[6,3] * rLambda_Costate[3,6]) + (rQ_Diag[3] * (rX_Pred_Horizon[2,3] - rX_Target[2,3]));
rLambda_Costate[2, 4] := (rA_Mat[1,4] * rLambda_Costate[3,1]) + (rA_Mat[2,4] * rLambda_Costate[3,2]) + (rA_Mat[3,4] * rLambda_Costate[3,3]) + (rA_Mat[4,4] * rLambda_Costate[3,4]) + (rA_Mat[5,4] * rLambda_Costate[3,5]) + (rA_Mat[6,4] * rLambda_Costate[3,6]) + (rQ_Diag[4] * (rX_Pred_Horizon[2,4] - rX_Target[2,4]));
rLambda_Costate[2, 5] := (rA_Mat[1,5] * rLambda_Costate[3,1]) + (rA_Mat[2,5] * rLambda_Costate[3,2]) + (rA_Mat[3,5] * rLambda_Costate[3,3]) + (rA_Mat[4,5] * rLambda_Costate[3,4]) + (rA_Mat[5,5] * rLambda_Costate[3,5]) + (rA_Mat[6,5] * rLambda_Costate[3,6]) + (rQ_Diag[5] * (rX_Pred_Horizon[2,5] - rX_Target[2,5]));
rLambda_Costate[2, 6] := (rA_Mat[1,6] * rLambda_Costate[3,1]) + (rA_Mat[2,6] * rLambda_Costate[3,2]) + (rA_Mat[3,6] * rLambda_Costate[3,3]) + (rA_Mat[4,6] * rLambda_Costate[3,4]) + (rA_Mat[5,6] * rLambda_Costate[3,5]) + (rA_Mat[6,6] * rLambda_Costate[3,6]) + (rQ_Diag[6] * (rX_Pred_Horizon[2,6] - rX_Target[2,6]));

(* Adjoint Costate at h=1: lambda_1 = A^T * lambda_2 + Q * (x_1 - x_target_1) *)
rLambda_Costate[1, 1] := (rA_Mat[1,1] * rLambda_Costate[2,1]) + (rA_Mat[2,1] * rLambda_Costate[2,2]) + (rA_Mat[3,1] * rLambda_Costate[2,3]) + (rA_Mat[4,1] * rLambda_Costate[2,4]) + (rA_Mat[5,1] * rLambda_Costate[2,5]) + (rA_Mat[6,1] * rLambda_Costate[2,6]) + (rQ_Diag[1] * (rX_Pred_Horizon[1,1] - rX_Target[1,1]));
rLambda_Costate[1, 2] := (rA_Mat[1,2] * rLambda_Costate[2,1]) + (rA_Mat[2,2] * rLambda_Costate[2,2]) + (rA_Mat[3,2] * rLambda_Costate[2,3]) + (rA_Mat[4,2] * rLambda_Costate[2,4]) + (rA_Mat[5,2] * rLambda_Costate[2,5]) + (rA_Mat[6,2] * rLambda_Costate[2,6]) + (rQ_Diag[2] * (rX_Pred_Horizon[1,2] - rX_Target[1,2]));
rLambda_Costate[1, 3] := (rA_Mat[1,3] * rLambda_Costate[2,1]) + (rA_Mat[2,3] * rLambda_Costate[2,2]) + (rA_Mat[3,3] * rLambda_Costate[2,3]) + (rA_Mat[4,3] * rLambda_Costate[2,4]) + (rA_Mat[5,3] * rLambda_Costate[2,5]) + (rA_Mat[6,3] * rLambda_Costate[2,6]) + (rQ_Diag[3] * (rX_Pred_Horizon[1,3] - rX_Target[1,3]));
rLambda_Costate[1, 4] := (rA_Mat[1,4] * rLambda_Costate[2,1]) + (rA_Mat[2,4] * rLambda_Costate[2,2]) + (rA_Mat[3,4] * rLambda_Costate[2,3]) + (rA_Mat[4,4] * rLambda_Costate[2,4]) + (rA_Mat[5,4] * rLambda_Costate[2,5]) + (rA_Mat[6,4] * rLambda_Costate[2,6]) + (rQ_Diag[4] * (rX_Pred_Horizon[1,4] - rX_Target[1,4]));
rLambda_Costate[1, 5] := (rA_Mat[1,5] * rLambda_Costate[2,1]) + (rA_Mat[2,5] * rLambda_Costate[2,2]) + (rA_Mat[3,5] * rLambda_Costate[2,3]) + (rA_Mat[4,5] * rLambda_Costate[2,4]) + (rA_Mat[5,5] * rLambda_Costate[2,5]) + (rA_Mat[6,5] * rLambda_Costate[2,6]) + (rQ_Diag[5] * (rX_Pred_Horizon[1,5] - rX_Target[1,5]));
rLambda_Costate[1, 6] := (rA_Mat[1,6] * rLambda_Costate[2,1]) + (rA_Mat[2,6] * rLambda_Costate[2,2]) + (rA_Mat[3,6] * rLambda_Costate[2,3]) + (rA_Mat[4,6] * rLambda_Costate[2,4]) + (rA_Mat[5,6] * rLambda_Costate[2,5]) + (rA_Mat[6,6] * rLambda_Costate[2,6]) + (rQ_Diag[6] * (rX_Pred_Horizon[1,6] - rX_Target[1,6]));

(* Iteration 1 - Analytical Gradient Computation w.r.t. Control Inputs u_h *)
rMPC_GradNormSq := 0.0;
(* Gradient for u_1 (h=1) *)
rGrad_J[1, 1] := (rB_Mat[1,1] * rLambda_Costate[1,1]) + (rB_Mat[2,1] * rLambda_Costate[1,2]) + (rB_Mat[3,1] * rLambda_Costate[1,3]) + (rB_Mat[4,1] * rLambda_Costate[1,4]) + (rB_Mat[5,1] * rLambda_Costate[1,5]) + (rB_Mat[6,1] * rLambda_Costate[1,6]) + (rR_Diag[1] * rU_Opt_Seq[1,1]) + (rS_Diag[1] * (rU_Opt_Seq[1,1] - a_u_prev[1])) - (rS_Diag[1] * (rU_Opt_Seq[2,1] - rU_Opt_Seq[1,1]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[1, 1] * rGrad_J[1, 1]);
rGrad_J[1, 2] := (rB_Mat[1,2] * rLambda_Costate[1,1]) + (rB_Mat[2,2] * rLambda_Costate[1,2]) + (rB_Mat[3,2] * rLambda_Costate[1,3]) + (rB_Mat[4,2] * rLambda_Costate[1,4]) + (rB_Mat[5,2] * rLambda_Costate[1,5]) + (rB_Mat[6,2] * rLambda_Costate[1,6]) + (rR_Diag[2] * rU_Opt_Seq[1,2]) + (rS_Diag[2] * (rU_Opt_Seq[1,2] - a_u_prev[2])) - (rS_Diag[2] * (rU_Opt_Seq[2,2] - rU_Opt_Seq[1,2]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[1, 2] * rGrad_J[1, 2]);
rGrad_J[1, 3] := (rB_Mat[1,3] * rLambda_Costate[1,1]) + (rB_Mat[2,3] * rLambda_Costate[1,2]) + (rB_Mat[3,3] * rLambda_Costate[1,3]) + (rB_Mat[4,3] * rLambda_Costate[1,4]) + (rB_Mat[5,3] * rLambda_Costate[1,5]) + (rB_Mat[6,3] * rLambda_Costate[1,6]) + (rR_Diag[3] * rU_Opt_Seq[1,3]) + (rS_Diag[3] * (rU_Opt_Seq[1,3] - a_u_prev[3])) - (rS_Diag[3] * (rU_Opt_Seq[2,3] - rU_Opt_Seq[1,3]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[1, 3] * rGrad_J[1, 3]);
rGrad_J[1, 4] := (rB_Mat[1,4] * rLambda_Costate[1,1]) + (rB_Mat[2,4] * rLambda_Costate[1,2]) + (rB_Mat[3,4] * rLambda_Costate[1,3]) + (rB_Mat[4,4] * rLambda_Costate[1,4]) + (rB_Mat[5,4] * rLambda_Costate[1,5]) + (rB_Mat[6,4] * rLambda_Costate[1,6]) + (rR_Diag[4] * rU_Opt_Seq[1,4]) + (rS_Diag[4] * (rU_Opt_Seq[1,4] - a_u_prev[4])) - (rS_Diag[4] * (rU_Opt_Seq[2,4] - rU_Opt_Seq[1,4]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[1, 4] * rGrad_J[1, 4]);
rGrad_J[1, 5] := (rB_Mat[1,5] * rLambda_Costate[1,1]) + (rB_Mat[2,5] * rLambda_Costate[1,2]) + (rB_Mat[3,5] * rLambda_Costate[1,3]) + (rB_Mat[4,5] * rLambda_Costate[1,4]) + (rB_Mat[5,5] * rLambda_Costate[1,5]) + (rB_Mat[6,5] * rLambda_Costate[1,6]) + (rR_Diag[5] * rU_Opt_Seq[1,5]) + (rS_Diag[5] * (rU_Opt_Seq[1,5] - a_u_prev[5])) - (rS_Diag[5] * (rU_Opt_Seq[2,5] - rU_Opt_Seq[1,5]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[1, 5] * rGrad_J[1, 5]);

(* Gradient for u_2 (h=2) *)
rGrad_J[2, 1] := (rB_Mat[1,1] * rLambda_Costate[2,1]) + (rB_Mat[2,1] * rLambda_Costate[2,2]) + (rB_Mat[3,1] * rLambda_Costate[2,3]) + (rB_Mat[4,1] * rLambda_Costate[2,4]) + (rB_Mat[5,1] * rLambda_Costate[2,5]) + (rB_Mat[6,1] * rLambda_Costate[2,6]) + (rR_Diag[1] * rU_Opt_Seq[2,1]) + (rS_Diag[1] * (rU_Opt_Seq[2,1] - rU_Opt_Seq[1,1])) - (rS_Diag[1] * (rU_Opt_Seq[3,1] - rU_Opt_Seq[2,1]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[2, 1] * rGrad_J[2, 1]);
rGrad_J[2, 2] := (rB_Mat[1,2] * rLambda_Costate[2,1]) + (rB_Mat[2,2] * rLambda_Costate[2,2]) + (rB_Mat[3,2] * rLambda_Costate[2,3]) + (rB_Mat[4,2] * rLambda_Costate[2,4]) + (rB_Mat[5,2] * rLambda_Costate[2,5]) + (rB_Mat[6,2] * rLambda_Costate[2,6]) + (rR_Diag[2] * rU_Opt_Seq[2,2]) + (rS_Diag[2] * (rU_Opt_Seq[2,2] - rU_Opt_Seq[1,2])) - (rS_Diag[2] * (rU_Opt_Seq[3,2] - rU_Opt_Seq[2,2]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[2, 2] * rGrad_J[2, 2]);
rGrad_J[2, 3] := (rB_Mat[1,3] * rLambda_Costate[2,1]) + (rB_Mat[2,3] * rLambda_Costate[2,2]) + (rB_Mat[3,3] * rLambda_Costate[2,3]) + (rB_Mat[4,3] * rLambda_Costate[2,4]) + (rB_Mat[5,3] * rLambda_Costate[2,5]) + (rB_Mat[6,3] * rLambda_Costate[2,6]) + (rR_Diag[3] * rU_Opt_Seq[2,3]) + (rS_Diag[3] * (rU_Opt_Seq[2,3] - rU_Opt_Seq[1,3])) - (rS_Diag[3] * (rU_Opt_Seq[3,3] - rU_Opt_Seq[2,3]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[2, 3] * rGrad_J[2, 3]);
rGrad_J[2, 4] := (rB_Mat[1,4] * rLambda_Costate[2,1]) + (rB_Mat[2,4] * rLambda_Costate[2,2]) + (rB_Mat[3,4] * rLambda_Costate[2,3]) + (rB_Mat[4,4] * rLambda_Costate[2,4]) + (rB_Mat[5,4] * rLambda_Costate[2,5]) + (rB_Mat[6,4] * rLambda_Costate[2,6]) + (rR_Diag[4] * rU_Opt_Seq[2,4]) + (rS_Diag[4] * (rU_Opt_Seq[2,4] - rU_Opt_Seq[1,4])) - (rS_Diag[4] * (rU_Opt_Seq[3,4] - rU_Opt_Seq[2,4]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[2, 4] * rGrad_J[2, 4]);
rGrad_J[2, 5] := (rB_Mat[1,5] * rLambda_Costate[2,1]) + (rB_Mat[2,5] * rLambda_Costate[2,2]) + (rB_Mat[3,5] * rLambda_Costate[2,3]) + (rB_Mat[4,5] * rLambda_Costate[2,4]) + (rB_Mat[5,5] * rLambda_Costate[2,5]) + (rB_Mat[6,5] * rLambda_Costate[2,6]) + (rR_Diag[5] * rU_Opt_Seq[2,5]) + (rS_Diag[5] * (rU_Opt_Seq[2,5] - rU_Opt_Seq[1,5])) - (rS_Diag[5] * (rU_Opt_Seq[3,5] - rU_Opt_Seq[2,5]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[2, 5] * rGrad_J[2, 5]);

(* Gradient for u_3 (h=3, held through h=4, 5) *)
rGrad_J[3, 1] := (rB_Mat[1,1] * (rLambda_Costate[3,1] + rLambda_Costate[4,1] + rLambda_Costate[5,1])) + (rB_Mat[2,1] * (rLambda_Costate[3,2] + rLambda_Costate[4,2] + rLambda_Costate[5,2])) + (rB_Mat[3,1] * (rLambda_Costate[3,3] + rLambda_Costate[4,3] + rLambda_Costate[5,3])) + (rB_Mat[4,1] * (rLambda_Costate[3,4] + rLambda_Costate[4,4] + rLambda_Costate[5,4])) + (rB_Mat[5,1] * (rLambda_Costate[3,5] + rLambda_Costate[4,5] + rLambda_Costate[5,5])) + (rB_Mat[6,1] * (rLambda_Costate[3,6] + rLambda_Costate[4,6] + rLambda_Costate[5,6])) + (rR_Diag[1] * rU_Opt_Seq[3,1]) + (rS_Diag[1] * (rU_Opt_Seq[3,1] - rU_Opt_Seq[2,1]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[3, 1] * rGrad_J[3, 1]);
rGrad_J[3, 2] := (rB_Mat[1,2] * (rLambda_Costate[3,1] + rLambda_Costate[4,1] + rLambda_Costate[5,1])) + (rB_Mat[2,2] * (rLambda_Costate[3,2] + rLambda_Costate[4,2] + rLambda_Costate[5,2])) + (rB_Mat[3,2] * (rLambda_Costate[3,3] + rLambda_Costate[4,3] + rLambda_Costate[5,3])) + (rB_Mat[4,2] * (rLambda_Costate[3,4] + rLambda_Costate[4,4] + rLambda_Costate[5,4])) + (rB_Mat[5,2] * (rLambda_Costate[3,5] + rLambda_Costate[4,5] + rLambda_Costate[5,5])) + (rB_Mat[6,2] * (rLambda_Costate[3,6] + rLambda_Costate[4,6] + rLambda_Costate[5,6])) + (rR_Diag[2] * rU_Opt_Seq[3,2]) + (rS_Diag[2] * (rU_Opt_Seq[3,2] - rU_Opt_Seq[2,2]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[3, 2] * rGrad_J[3, 2]);
rGrad_J[3, 3] := (rB_Mat[1,3] * (rLambda_Costate[3,1] + rLambda_Costate[4,1] + rLambda_Costate[5,1])) + (rB_Mat[2,3] * (rLambda_Costate[3,2] + rLambda_Costate[4,2] + rLambda_Costate[5,2])) + (rB_Mat[3,3] * (rLambda_Costate[3,3] + rLambda_Costate[4,3] + rLambda_Costate[5,3])) + (rB_Mat[4,3] * (rLambda_Costate[3,4] + rLambda_Costate[4,4] + rLambda_Costate[5,4])) + (rB_Mat[5,3] * (rLambda_Costate[3,5] + rLambda_Costate[4,5] + rLambda_Costate[5,5])) + (rB_Mat[6,3] * (rLambda_Costate[3,6] + rLambda_Costate[4,6] + rLambda_Costate[5,6])) + (rR_Diag[3] * rU_Opt_Seq[3,3]) + (rS_Diag[3] * (rU_Opt_Seq[3,3] - rU_Opt_Seq[2,3]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[3, 3] * rGrad_J[3, 3]);
rGrad_J[3, 4] := (rB_Mat[1,4] * (rLambda_Costate[3,1] + rLambda_Costate[4,1] + rLambda_Costate[5,1])) + (rB_Mat[2,4] * (rLambda_Costate[3,2] + rLambda_Costate[4,2] + rLambda_Costate[5,2])) + (rB_Mat[3,4] * (rLambda_Costate[3,3] + rLambda_Costate[4,3] + rLambda_Costate[5,3])) + (rB_Mat[4,4] * (rLambda_Costate[3,4] + rLambda_Costate[4,4] + rLambda_Costate[5,4])) + (rB_Mat[5,4] * (rLambda_Costate[3,5] + rLambda_Costate[4,5] + rLambda_Costate[5,5])) + (rB_Mat[6,4] * (rLambda_Costate[3,6] + rLambda_Costate[4,6] + rLambda_Costate[5,6])) + (rR_Diag[4] * rU_Opt_Seq[3,4]) + (rS_Diag[4] * (rU_Opt_Seq[3,4] - rU_Opt_Seq[2,4]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[3, 4] * rGrad_J[3, 4]);
rGrad_J[3, 5] := (rB_Mat[1,5] * (rLambda_Costate[3,1] + rLambda_Costate[4,1] + rLambda_Costate[5,1])) + (rB_Mat[2,5] * (rLambda_Costate[3,2] + rLambda_Costate[4,2] + rLambda_Costate[5,2])) + (rB_Mat[3,5] * (rLambda_Costate[3,3] + rLambda_Costate[4,3] + rLambda_Costate[5,3])) + (rB_Mat[4,5] * (rLambda_Costate[3,4] + rLambda_Costate[4,4] + rLambda_Costate[5,4])) + (rB_Mat[5,5] * (rLambda_Costate[3,5] + rLambda_Costate[4,5] + rLambda_Costate[5,5])) + (rB_Mat[6,5] * (rLambda_Costate[3,6] + rLambda_Costate[4,6] + rLambda_Costate[5,6])) + (rR_Diag[5] * rU_Opt_Seq[3,5]) + (rS_Diag[5] * (rU_Opt_Seq[3,5] - rU_Opt_Seq[2,5]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[3, 5] * rGrad_J[3, 5]);

(* Iteration 1 - Projected Gradient Step with Hard Box & Dynamic Slew Limits *)
rTemp_Val := rU_Opt_Seq[1, 1] - (rAlpha_PGD_StepSize * rGrad_J[1, 1]);
(* Slew limit against prior actuator output *)
IF rTemp_Val > (a_u_prev[1] + rDeltaU_Max[1]) THEN
    rTemp_Val := a_u_prev[1] + rDeltaU_Max[1];
ELSIF rTemp_Val < (a_u_prev[1] - rDeltaU_Max[1]) THEN
    rTemp_Val := a_u_prev[1] - rDeltaU_Max[1];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[1] THEN
    rTemp_Val := rU_BoxMax[1];
ELSIF rTemp_Val < rU_BoxMin[1] THEN
    rTemp_Val := rU_BoxMin[1];
END_IF;
rU_Opt_Seq[1, 1] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[1, 2] - (rAlpha_PGD_StepSize * rGrad_J[1, 2]);
(* Slew limit against prior actuator output *)
IF rTemp_Val > (a_u_prev[2] + rDeltaU_Max[2]) THEN
    rTemp_Val := a_u_prev[2] + rDeltaU_Max[2];
ELSIF rTemp_Val < (a_u_prev[2] - rDeltaU_Max[2]) THEN
    rTemp_Val := a_u_prev[2] - rDeltaU_Max[2];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[2] THEN
    rTemp_Val := rU_BoxMax[2];
ELSIF rTemp_Val < rU_BoxMin[2] THEN
    rTemp_Val := rU_BoxMin[2];
END_IF;
rU_Opt_Seq[1, 2] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[1, 3] - (rAlpha_PGD_StepSize * rGrad_J[1, 3]);
(* Slew limit against prior actuator output *)
IF rTemp_Val > (a_u_prev[3] + rDeltaU_Max[3]) THEN
    rTemp_Val := a_u_prev[3] + rDeltaU_Max[3];
ELSIF rTemp_Val < (a_u_prev[3] - rDeltaU_Max[3]) THEN
    rTemp_Val := a_u_prev[3] - rDeltaU_Max[3];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[3] THEN
    rTemp_Val := rU_BoxMax[3];
ELSIF rTemp_Val < rU_BoxMin[3] THEN
    rTemp_Val := rU_BoxMin[3];
END_IF;
rU_Opt_Seq[1, 3] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[1, 4] - (rAlpha_PGD_StepSize * rGrad_J[1, 4]);
(* Slew limit against prior actuator output *)
IF rTemp_Val > (a_u_prev[4] + rDeltaU_Max[4]) THEN
    rTemp_Val := a_u_prev[4] + rDeltaU_Max[4];
ELSIF rTemp_Val < (a_u_prev[4] - rDeltaU_Max[4]) THEN
    rTemp_Val := a_u_prev[4] - rDeltaU_Max[4];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[4] THEN
    rTemp_Val := rU_BoxMax[4];
ELSIF rTemp_Val < rU_BoxMin[4] THEN
    rTemp_Val := rU_BoxMin[4];
END_IF;
rU_Opt_Seq[1, 4] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[1, 5] - (rAlpha_PGD_StepSize * rGrad_J[1, 5]);
(* Slew limit against prior actuator output *)
IF rTemp_Val > (a_u_prev[5] + rDeltaU_Max[5]) THEN
    rTemp_Val := a_u_prev[5] + rDeltaU_Max[5];
ELSIF rTemp_Val < (a_u_prev[5] - rDeltaU_Max[5]) THEN
    rTemp_Val := a_u_prev[5] - rDeltaU_Max[5];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[5] THEN
    rTemp_Val := rU_BoxMax[5];
ELSIF rTemp_Val < rU_BoxMin[5] THEN
    rTemp_Val := rU_BoxMin[5];
END_IF;
rU_Opt_Seq[1, 5] := rTemp_Val;

rTemp_Val := rU_Opt_Seq[2, 1] - (rAlpha_PGD_StepSize * rGrad_J[2, 1]);
(* Slew limit against step 1 *)
IF rTemp_Val > (rU_Opt_Seq[1, 1] + rDeltaU_Max[1]) THEN
    rTemp_Val := rU_Opt_Seq[1, 1] + rDeltaU_Max[1];
ELSIF rTemp_Val < (rU_Opt_Seq[1, 1] - rDeltaU_Max[1]) THEN
    rTemp_Val := rU_Opt_Seq[1, 1] - rDeltaU_Max[1];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[1] THEN
    rTemp_Val := rU_BoxMax[1];
ELSIF rTemp_Val < rU_BoxMin[1] THEN
    rTemp_Val := rU_BoxMin[1];
END_IF;
rU_Opt_Seq[2, 1] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[2, 2] - (rAlpha_PGD_StepSize * rGrad_J[2, 2]);
(* Slew limit against step 1 *)
IF rTemp_Val > (rU_Opt_Seq[1, 2] + rDeltaU_Max[2]) THEN
    rTemp_Val := rU_Opt_Seq[1, 2] + rDeltaU_Max[2];
ELSIF rTemp_Val < (rU_Opt_Seq[1, 2] - rDeltaU_Max[2]) THEN
    rTemp_Val := rU_Opt_Seq[1, 2] - rDeltaU_Max[2];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[2] THEN
    rTemp_Val := rU_BoxMax[2];
ELSIF rTemp_Val < rU_BoxMin[2] THEN
    rTemp_Val := rU_BoxMin[2];
END_IF;
rU_Opt_Seq[2, 2] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[2, 3] - (rAlpha_PGD_StepSize * rGrad_J[2, 3]);
(* Slew limit against step 1 *)
IF rTemp_Val > (rU_Opt_Seq[1, 3] + rDeltaU_Max[3]) THEN
    rTemp_Val := rU_Opt_Seq[1, 3] + rDeltaU_Max[3];
ELSIF rTemp_Val < (rU_Opt_Seq[1, 3] - rDeltaU_Max[3]) THEN
    rTemp_Val := rU_Opt_Seq[1, 3] - rDeltaU_Max[3];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[3] THEN
    rTemp_Val := rU_BoxMax[3];
ELSIF rTemp_Val < rU_BoxMin[3] THEN
    rTemp_Val := rU_BoxMin[3];
END_IF;
rU_Opt_Seq[2, 3] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[2, 4] - (rAlpha_PGD_StepSize * rGrad_J[2, 4]);
(* Slew limit against step 1 *)
IF rTemp_Val > (rU_Opt_Seq[1, 4] + rDeltaU_Max[4]) THEN
    rTemp_Val := rU_Opt_Seq[1, 4] + rDeltaU_Max[4];
ELSIF rTemp_Val < (rU_Opt_Seq[1, 4] - rDeltaU_Max[4]) THEN
    rTemp_Val := rU_Opt_Seq[1, 4] - rDeltaU_Max[4];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[4] THEN
    rTemp_Val := rU_BoxMax[4];
ELSIF rTemp_Val < rU_BoxMin[4] THEN
    rTemp_Val := rU_BoxMin[4];
END_IF;
rU_Opt_Seq[2, 4] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[2, 5] - (rAlpha_PGD_StepSize * rGrad_J[2, 5]);
(* Slew limit against step 1 *)
IF rTemp_Val > (rU_Opt_Seq[1, 5] + rDeltaU_Max[5]) THEN
    rTemp_Val := rU_Opt_Seq[1, 5] + rDeltaU_Max[5];
ELSIF rTemp_Val < (rU_Opt_Seq[1, 5] - rDeltaU_Max[5]) THEN
    rTemp_Val := rU_Opt_Seq[1, 5] - rDeltaU_Max[5];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[5] THEN
    rTemp_Val := rU_BoxMax[5];
ELSIF rTemp_Val < rU_BoxMin[5] THEN
    rTemp_Val := rU_BoxMin[5];
END_IF;
rU_Opt_Seq[2, 5] := rTemp_Val;

rTemp_Val := rU_Opt_Seq[3, 1] - (rAlpha_PGD_StepSize * rGrad_J[3, 1]);
(* Slew limit against step 2 *)
IF rTemp_Val > (rU_Opt_Seq[2, 1] + rDeltaU_Max[1]) THEN
    rTemp_Val := rU_Opt_Seq[2, 1] + rDeltaU_Max[1];
ELSIF rTemp_Val < (rU_Opt_Seq[2, 1] - rDeltaU_Max[1]) THEN
    rTemp_Val := rU_Opt_Seq[2, 1] - rDeltaU_Max[1];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[1] THEN
    rTemp_Val := rU_BoxMax[1];
ELSIF rTemp_Val < rU_BoxMin[1] THEN
    rTemp_Val := rU_BoxMin[1];
END_IF;
rU_Opt_Seq[3, 1] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[3, 2] - (rAlpha_PGD_StepSize * rGrad_J[3, 2]);
(* Slew limit against step 2 *)
IF rTemp_Val > (rU_Opt_Seq[2, 2] + rDeltaU_Max[2]) THEN
    rTemp_Val := rU_Opt_Seq[2, 2] + rDeltaU_Max[2];
ELSIF rTemp_Val < (rU_Opt_Seq[2, 2] - rDeltaU_Max[2]) THEN
    rTemp_Val := rU_Opt_Seq[2, 2] - rDeltaU_Max[2];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[2] THEN
    rTemp_Val := rU_BoxMax[2];
ELSIF rTemp_Val < rU_BoxMin[2] THEN
    rTemp_Val := rU_BoxMin[2];
END_IF;
rU_Opt_Seq[3, 2] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[3, 3] - (rAlpha_PGD_StepSize * rGrad_J[3, 3]);
(* Slew limit against step 2 *)
IF rTemp_Val > (rU_Opt_Seq[2, 3] + rDeltaU_Max[3]) THEN
    rTemp_Val := rU_Opt_Seq[2, 3] + rDeltaU_Max[3];
ELSIF rTemp_Val < (rU_Opt_Seq[2, 3] - rDeltaU_Max[3]) THEN
    rTemp_Val := rU_Opt_Seq[2, 3] - rDeltaU_Max[3];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[3] THEN
    rTemp_Val := rU_BoxMax[3];
ELSIF rTemp_Val < rU_BoxMin[3] THEN
    rTemp_Val := rU_BoxMin[3];
END_IF;
rU_Opt_Seq[3, 3] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[3, 4] - (rAlpha_PGD_StepSize * rGrad_J[3, 4]);
(* Slew limit against step 2 *)
IF rTemp_Val > (rU_Opt_Seq[2, 4] + rDeltaU_Max[4]) THEN
    rTemp_Val := rU_Opt_Seq[2, 4] + rDeltaU_Max[4];
ELSIF rTemp_Val < (rU_Opt_Seq[2, 4] - rDeltaU_Max[4]) THEN
    rTemp_Val := rU_Opt_Seq[2, 4] - rDeltaU_Max[4];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[4] THEN
    rTemp_Val := rU_BoxMax[4];
ELSIF rTemp_Val < rU_BoxMin[4] THEN
    rTemp_Val := rU_BoxMin[4];
END_IF;
rU_Opt_Seq[3, 4] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[3, 5] - (rAlpha_PGD_StepSize * rGrad_J[3, 5]);
(* Slew limit against step 2 *)
IF rTemp_Val > (rU_Opt_Seq[2, 5] + rDeltaU_Max[5]) THEN
    rTemp_Val := rU_Opt_Seq[2, 5] + rDeltaU_Max[5];
ELSIF rTemp_Val < (rU_Opt_Seq[2, 5] - rDeltaU_Max[5]) THEN
    rTemp_Val := rU_Opt_Seq[2, 5] - rDeltaU_Max[5];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[5] THEN
    rTemp_Val := rU_BoxMax[5];
ELSIF rTemp_Val < rU_BoxMin[5] THEN
    rTemp_Val := rU_BoxMin[5];
END_IF;
rU_Opt_Seq[3, 5] := rTemp_Val;

(* ================================================================================================== *)
(* MPC PROJECTED GRADIENT DESCENT -- UNROLLED ITERATION 2 OF 10                                 *)
(* ================================================================================================== *)
iPGD_IterCount := 2;

(* Iteration 2 - Forward State Prediction Step 1 (h=1): x_1 = A * x_hat + B * u_1 *)
rX_Pred_Horizon[1, 1] := (rA_Mat[1,1] * a_x_hat[1]) + (rA_Mat[1,2] * a_x_hat[2]) + (rA_Mat[1,3] * a_x_hat[3]) + (rA_Mat[1,4] * a_x_hat[4]) + (rA_Mat[1,5] * a_x_hat[5]) + (rA_Mat[1,6] * a_x_hat[6]) + (rB_Mat[1,1] * rU_Opt_Seq[1,1]) + (rB_Mat[1,2] * rU_Opt_Seq[1,2]) + (rB_Mat[1,3] * rU_Opt_Seq[1,3]) + (rB_Mat[1,4] * rU_Opt_Seq[1,4]) + (rB_Mat[1,5] * rU_Opt_Seq[1,5]);
rX_Pred_Horizon[1, 2] := (rA_Mat[2,1] * a_x_hat[1]) + (rA_Mat[2,2] * a_x_hat[2]) + (rA_Mat[2,3] * a_x_hat[3]) + (rA_Mat[2,4] * a_x_hat[4]) + (rA_Mat[2,5] * a_x_hat[5]) + (rA_Mat[2,6] * a_x_hat[6]) + (rB_Mat[2,1] * rU_Opt_Seq[1,1]) + (rB_Mat[2,2] * rU_Opt_Seq[1,2]) + (rB_Mat[2,3] * rU_Opt_Seq[1,3]) + (rB_Mat[2,4] * rU_Opt_Seq[1,4]) + (rB_Mat[2,5] * rU_Opt_Seq[1,5]);
rX_Pred_Horizon[1, 3] := (rA_Mat[3,1] * a_x_hat[1]) + (rA_Mat[3,2] * a_x_hat[2]) + (rA_Mat[3,3] * a_x_hat[3]) + (rA_Mat[3,4] * a_x_hat[4]) + (rA_Mat[3,5] * a_x_hat[5]) + (rA_Mat[3,6] * a_x_hat[6]) + (rB_Mat[3,1] * rU_Opt_Seq[1,1]) + (rB_Mat[3,2] * rU_Opt_Seq[1,2]) + (rB_Mat[3,3] * rU_Opt_Seq[1,3]) + (rB_Mat[3,4] * rU_Opt_Seq[1,4]) + (rB_Mat[3,5] * rU_Opt_Seq[1,5]);
rX_Pred_Horizon[1, 4] := (rA_Mat[4,1] * a_x_hat[1]) + (rA_Mat[4,2] * a_x_hat[2]) + (rA_Mat[4,3] * a_x_hat[3]) + (rA_Mat[4,4] * a_x_hat[4]) + (rA_Mat[4,5] * a_x_hat[5]) + (rA_Mat[4,6] * a_x_hat[6]) + (rB_Mat[4,1] * rU_Opt_Seq[1,1]) + (rB_Mat[4,2] * rU_Opt_Seq[1,2]) + (rB_Mat[4,3] * rU_Opt_Seq[1,3]) + (rB_Mat[4,4] * rU_Opt_Seq[1,4]) + (rB_Mat[4,5] * rU_Opt_Seq[1,5]);
rX_Pred_Horizon[1, 5] := (rA_Mat[5,1] * a_x_hat[1]) + (rA_Mat[5,2] * a_x_hat[2]) + (rA_Mat[5,3] * a_x_hat[3]) + (rA_Mat[5,4] * a_x_hat[4]) + (rA_Mat[5,5] * a_x_hat[5]) + (rA_Mat[5,6] * a_x_hat[6]) + (rB_Mat[5,1] * rU_Opt_Seq[1,1]) + (rB_Mat[5,2] * rU_Opt_Seq[1,2]) + (rB_Mat[5,3] * rU_Opt_Seq[1,3]) + (rB_Mat[5,4] * rU_Opt_Seq[1,4]) + (rB_Mat[5,5] * rU_Opt_Seq[1,5]);
rX_Pred_Horizon[1, 6] := (rA_Mat[6,1] * a_x_hat[1]) + (rA_Mat[6,2] * a_x_hat[2]) + (rA_Mat[6,3] * a_x_hat[3]) + (rA_Mat[6,4] * a_x_hat[4]) + (rA_Mat[6,5] * a_x_hat[5]) + (rA_Mat[6,6] * a_x_hat[6]) + (rB_Mat[6,1] * rU_Opt_Seq[1,1]) + (rB_Mat[6,2] * rU_Opt_Seq[1,2]) + (rB_Mat[6,3] * rU_Opt_Seq[1,3]) + (rB_Mat[6,4] * rU_Opt_Seq[1,4]) + (rB_Mat[6,5] * rU_Opt_Seq[1,5]);

(* Iteration 2 - Forward State Prediction Step 2 (h=2): x_2 = A * x_1 + B * u_2 *)
rX_Pred_Horizon[2, 1] := (rA_Mat[1,1] * rX_Pred_Horizon[1,1]) + (rA_Mat[1,2] * rX_Pred_Horizon[1,2]) + (rA_Mat[1,3] * rX_Pred_Horizon[1,3]) + (rA_Mat[1,4] * rX_Pred_Horizon[1,4]) + (rA_Mat[1,5] * rX_Pred_Horizon[1,5]) + (rA_Mat[1,6] * rX_Pred_Horizon[1,6]) + (rB_Mat[1,1] * rU_Opt_Seq[2,1]) + (rB_Mat[1,2] * rU_Opt_Seq[2,2]) + (rB_Mat[1,3] * rU_Opt_Seq[2,3]) + (rB_Mat[1,4] * rU_Opt_Seq[2,4]) + (rB_Mat[1,5] * rU_Opt_Seq[2,5]);
rX_Pred_Horizon[2, 2] := (rA_Mat[2,1] * rX_Pred_Horizon[1,1]) + (rA_Mat[2,2] * rX_Pred_Horizon[1,2]) + (rA_Mat[2,3] * rX_Pred_Horizon[1,3]) + (rA_Mat[2,4] * rX_Pred_Horizon[1,4]) + (rA_Mat[2,5] * rX_Pred_Horizon[1,5]) + (rA_Mat[2,6] * rX_Pred_Horizon[1,6]) + (rB_Mat[2,1] * rU_Opt_Seq[2,1]) + (rB_Mat[2,2] * rU_Opt_Seq[2,2]) + (rB_Mat[2,3] * rU_Opt_Seq[2,3]) + (rB_Mat[2,4] * rU_Opt_Seq[2,4]) + (rB_Mat[2,5] * rU_Opt_Seq[2,5]);
rX_Pred_Horizon[2, 3] := (rA_Mat[3,1] * rX_Pred_Horizon[1,1]) + (rA_Mat[3,2] * rX_Pred_Horizon[1,2]) + (rA_Mat[3,3] * rX_Pred_Horizon[1,3]) + (rA_Mat[3,4] * rX_Pred_Horizon[1,4]) + (rA_Mat[3,5] * rX_Pred_Horizon[1,5]) + (rA_Mat[3,6] * rX_Pred_Horizon[1,6]) + (rB_Mat[3,1] * rU_Opt_Seq[2,1]) + (rB_Mat[3,2] * rU_Opt_Seq[2,2]) + (rB_Mat[3,3] * rU_Opt_Seq[2,3]) + (rB_Mat[3,4] * rU_Opt_Seq[2,4]) + (rB_Mat[3,5] * rU_Opt_Seq[2,5]);
rX_Pred_Horizon[2, 4] := (rA_Mat[4,1] * rX_Pred_Horizon[1,1]) + (rA_Mat[4,2] * rX_Pred_Horizon[1,2]) + (rA_Mat[4,3] * rX_Pred_Horizon[1,3]) + (rA_Mat[4,4] * rX_Pred_Horizon[1,4]) + (rA_Mat[4,5] * rX_Pred_Horizon[1,5]) + (rA_Mat[4,6] * rX_Pred_Horizon[1,6]) + (rB_Mat[4,1] * rU_Opt_Seq[2,1]) + (rB_Mat[4,2] * rU_Opt_Seq[2,2]) + (rB_Mat[4,3] * rU_Opt_Seq[2,3]) + (rB_Mat[4,4] * rU_Opt_Seq[2,4]) + (rB_Mat[4,5] * rU_Opt_Seq[2,5]);
rX_Pred_Horizon[2, 5] := (rA_Mat[5,1] * rX_Pred_Horizon[1,1]) + (rA_Mat[5,2] * rX_Pred_Horizon[1,2]) + (rA_Mat[5,3] * rX_Pred_Horizon[1,3]) + (rA_Mat[5,4] * rX_Pred_Horizon[1,4]) + (rA_Mat[5,5] * rX_Pred_Horizon[1,5]) + (rA_Mat[5,6] * rX_Pred_Horizon[1,6]) + (rB_Mat[5,1] * rU_Opt_Seq[2,1]) + (rB_Mat[5,2] * rU_Opt_Seq[2,2]) + (rB_Mat[5,3] * rU_Opt_Seq[2,3]) + (rB_Mat[5,4] * rU_Opt_Seq[2,4]) + (rB_Mat[5,5] * rU_Opt_Seq[2,5]);
rX_Pred_Horizon[2, 6] := (rA_Mat[6,1] * rX_Pred_Horizon[1,1]) + (rA_Mat[6,2] * rX_Pred_Horizon[1,2]) + (rA_Mat[6,3] * rX_Pred_Horizon[1,3]) + (rA_Mat[6,4] * rX_Pred_Horizon[1,4]) + (rA_Mat[6,5] * rX_Pred_Horizon[1,5]) + (rA_Mat[6,6] * rX_Pred_Horizon[1,6]) + (rB_Mat[6,1] * rU_Opt_Seq[2,1]) + (rB_Mat[6,2] * rU_Opt_Seq[2,2]) + (rB_Mat[6,3] * rU_Opt_Seq[2,3]) + (rB_Mat[6,4] * rU_Opt_Seq[2,4]) + (rB_Mat[6,5] * rU_Opt_Seq[2,5]);

(* Iteration 2 - Forward State Prediction Step 3 (h=3): x_3 = A * x_2 + B * u_3 *)
rX_Pred_Horizon[3, 1] := (rA_Mat[1,1] * rX_Pred_Horizon[2,1]) + (rA_Mat[1,2] * rX_Pred_Horizon[2,2]) + (rA_Mat[1,3] * rX_Pred_Horizon[2,3]) + (rA_Mat[1,4] * rX_Pred_Horizon[2,4]) + (rA_Mat[1,5] * rX_Pred_Horizon[2,5]) + (rA_Mat[1,6] * rX_Pred_Horizon[2,6]) + (rB_Mat[1,1] * rU_Opt_Seq[3,1]) + (rB_Mat[1,2] * rU_Opt_Seq[3,2]) + (rB_Mat[1,3] * rU_Opt_Seq[3,3]) + (rB_Mat[1,4] * rU_Opt_Seq[3,4]) + (rB_Mat[1,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[3, 2] := (rA_Mat[2,1] * rX_Pred_Horizon[2,1]) + (rA_Mat[2,2] * rX_Pred_Horizon[2,2]) + (rA_Mat[2,3] * rX_Pred_Horizon[2,3]) + (rA_Mat[2,4] * rX_Pred_Horizon[2,4]) + (rA_Mat[2,5] * rX_Pred_Horizon[2,5]) + (rA_Mat[2,6] * rX_Pred_Horizon[2,6]) + (rB_Mat[2,1] * rU_Opt_Seq[3,1]) + (rB_Mat[2,2] * rU_Opt_Seq[3,2]) + (rB_Mat[2,3] * rU_Opt_Seq[3,3]) + (rB_Mat[2,4] * rU_Opt_Seq[3,4]) + (rB_Mat[2,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[3, 3] := (rA_Mat[3,1] * rX_Pred_Horizon[2,1]) + (rA_Mat[3,2] * rX_Pred_Horizon[2,2]) + (rA_Mat[3,3] * rX_Pred_Horizon[2,3]) + (rA_Mat[3,4] * rX_Pred_Horizon[2,4]) + (rA_Mat[3,5] * rX_Pred_Horizon[2,5]) + (rA_Mat[3,6] * rX_Pred_Horizon[2,6]) + (rB_Mat[3,1] * rU_Opt_Seq[3,1]) + (rB_Mat[3,2] * rU_Opt_Seq[3,2]) + (rB_Mat[3,3] * rU_Opt_Seq[3,3]) + (rB_Mat[3,4] * rU_Opt_Seq[3,4]) + (rB_Mat[3,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[3, 4] := (rA_Mat[4,1] * rX_Pred_Horizon[2,1]) + (rA_Mat[4,2] * rX_Pred_Horizon[2,2]) + (rA_Mat[4,3] * rX_Pred_Horizon[2,3]) + (rA_Mat[4,4] * rX_Pred_Horizon[2,4]) + (rA_Mat[4,5] * rX_Pred_Horizon[2,5]) + (rA_Mat[4,6] * rX_Pred_Horizon[2,6]) + (rB_Mat[4,1] * rU_Opt_Seq[3,1]) + (rB_Mat[4,2] * rU_Opt_Seq[3,2]) + (rB_Mat[4,3] * rU_Opt_Seq[3,3]) + (rB_Mat[4,4] * rU_Opt_Seq[3,4]) + (rB_Mat[4,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[3, 5] := (rA_Mat[5,1] * rX_Pred_Horizon[2,1]) + (rA_Mat[5,2] * rX_Pred_Horizon[2,2]) + (rA_Mat[5,3] * rX_Pred_Horizon[2,3]) + (rA_Mat[5,4] * rX_Pred_Horizon[2,4]) + (rA_Mat[5,5] * rX_Pred_Horizon[2,5]) + (rA_Mat[5,6] * rX_Pred_Horizon[2,6]) + (rB_Mat[5,1] * rU_Opt_Seq[3,1]) + (rB_Mat[5,2] * rU_Opt_Seq[3,2]) + (rB_Mat[5,3] * rU_Opt_Seq[3,3]) + (rB_Mat[5,4] * rU_Opt_Seq[3,4]) + (rB_Mat[5,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[3, 6] := (rA_Mat[6,1] * rX_Pred_Horizon[2,1]) + (rA_Mat[6,2] * rX_Pred_Horizon[2,2]) + (rA_Mat[6,3] * rX_Pred_Horizon[2,3]) + (rA_Mat[6,4] * rX_Pred_Horizon[2,4]) + (rA_Mat[6,5] * rX_Pred_Horizon[2,5]) + (rA_Mat[6,6] * rX_Pred_Horizon[2,6]) + (rB_Mat[6,1] * rU_Opt_Seq[3,1]) + (rB_Mat[6,2] * rU_Opt_Seq[3,2]) + (rB_Mat[6,3] * rU_Opt_Seq[3,3]) + (rB_Mat[6,4] * rU_Opt_Seq[3,4]) + (rB_Mat[6,5] * rU_Opt_Seq[3,5]);

(* Iteration 2 - Forward State Prediction Step 4 (h=4): x_4 = A * x_3 + B * u_3 (held beyond Hu) *)
rX_Pred_Horizon[4, 1] := (rA_Mat[1,1] * rX_Pred_Horizon[3,1]) + (rA_Mat[1,2] * rX_Pred_Horizon[3,2]) + (rA_Mat[1,3] * rX_Pred_Horizon[3,3]) + (rA_Mat[1,4] * rX_Pred_Horizon[3,4]) + (rA_Mat[1,5] * rX_Pred_Horizon[3,5]) + (rA_Mat[1,6] * rX_Pred_Horizon[3,6]) + (rB_Mat[1,1] * rU_Opt_Seq[3,1]) + (rB_Mat[1,2] * rU_Opt_Seq[3,2]) + (rB_Mat[1,3] * rU_Opt_Seq[3,3]) + (rB_Mat[1,4] * rU_Opt_Seq[3,4]) + (rB_Mat[1,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[4, 2] := (rA_Mat[2,1] * rX_Pred_Horizon[3,1]) + (rA_Mat[2,2] * rX_Pred_Horizon[3,2]) + (rA_Mat[2,3] * rX_Pred_Horizon[3,3]) + (rA_Mat[2,4] * rX_Pred_Horizon[3,4]) + (rA_Mat[2,5] * rX_Pred_Horizon[3,5]) + (rA_Mat[2,6] * rX_Pred_Horizon[3,6]) + (rB_Mat[2,1] * rU_Opt_Seq[3,1]) + (rB_Mat[2,2] * rU_Opt_Seq[3,2]) + (rB_Mat[2,3] * rU_Opt_Seq[3,3]) + (rB_Mat[2,4] * rU_Opt_Seq[3,4]) + (rB_Mat[2,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[4, 3] := (rA_Mat[3,1] * rX_Pred_Horizon[3,1]) + (rA_Mat[3,2] * rX_Pred_Horizon[3,2]) + (rA_Mat[3,3] * rX_Pred_Horizon[3,3]) + (rA_Mat[3,4] * rX_Pred_Horizon[3,4]) + (rA_Mat[3,5] * rX_Pred_Horizon[3,5]) + (rA_Mat[3,6] * rX_Pred_Horizon[3,6]) + (rB_Mat[3,1] * rU_Opt_Seq[3,1]) + (rB_Mat[3,2] * rU_Opt_Seq[3,2]) + (rB_Mat[3,3] * rU_Opt_Seq[3,3]) + (rB_Mat[3,4] * rU_Opt_Seq[3,4]) + (rB_Mat[3,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[4, 4] := (rA_Mat[4,1] * rX_Pred_Horizon[3,1]) + (rA_Mat[4,2] * rX_Pred_Horizon[3,2]) + (rA_Mat[4,3] * rX_Pred_Horizon[3,3]) + (rA_Mat[4,4] * rX_Pred_Horizon[3,4]) + (rA_Mat[4,5] * rX_Pred_Horizon[3,5]) + (rA_Mat[4,6] * rX_Pred_Horizon[3,6]) + (rB_Mat[4,1] * rU_Opt_Seq[3,1]) + (rB_Mat[4,2] * rU_Opt_Seq[3,2]) + (rB_Mat[4,3] * rU_Opt_Seq[3,3]) + (rB_Mat[4,4] * rU_Opt_Seq[3,4]) + (rB_Mat[4,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[4, 5] := (rA_Mat[5,1] * rX_Pred_Horizon[3,1]) + (rA_Mat[5,2] * rX_Pred_Horizon[3,2]) + (rA_Mat[5,3] * rX_Pred_Horizon[3,3]) + (rA_Mat[5,4] * rX_Pred_Horizon[3,4]) + (rA_Mat[5,5] * rX_Pred_Horizon[3,5]) + (rA_Mat[5,6] * rX_Pred_Horizon[3,6]) + (rB_Mat[5,1] * rU_Opt_Seq[3,1]) + (rB_Mat[5,2] * rU_Opt_Seq[3,2]) + (rB_Mat[5,3] * rU_Opt_Seq[3,3]) + (rB_Mat[5,4] * rU_Opt_Seq[3,4]) + (rB_Mat[5,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[4, 6] := (rA_Mat[6,1] * rX_Pred_Horizon[3,1]) + (rA_Mat[6,2] * rX_Pred_Horizon[3,2]) + (rA_Mat[6,3] * rX_Pred_Horizon[3,3]) + (rA_Mat[6,4] * rX_Pred_Horizon[3,4]) + (rA_Mat[6,5] * rX_Pred_Horizon[3,5]) + (rA_Mat[6,6] * rX_Pred_Horizon[3,6]) + (rB_Mat[6,1] * rU_Opt_Seq[3,1]) + (rB_Mat[6,2] * rU_Opt_Seq[3,2]) + (rB_Mat[6,3] * rU_Opt_Seq[3,3]) + (rB_Mat[6,4] * rU_Opt_Seq[3,4]) + (rB_Mat[6,5] * rU_Opt_Seq[3,5]);

(* Iteration 2 - Forward State Prediction Step 5 (h=5): x_5 = A * x_4 + B * u_3 (held beyond Hu) *)
rX_Pred_Horizon[5, 1] := (rA_Mat[1,1] * rX_Pred_Horizon[4,1]) + (rA_Mat[1,2] * rX_Pred_Horizon[4,2]) + (rA_Mat[1,3] * rX_Pred_Horizon[4,3]) + (rA_Mat[1,4] * rX_Pred_Horizon[4,4]) + (rA_Mat[1,5] * rX_Pred_Horizon[4,5]) + (rA_Mat[1,6] * rX_Pred_Horizon[4,6]) + (rB_Mat[1,1] * rU_Opt_Seq[3,1]) + (rB_Mat[1,2] * rU_Opt_Seq[3,2]) + (rB_Mat[1,3] * rU_Opt_Seq[3,3]) + (rB_Mat[1,4] * rU_Opt_Seq[3,4]) + (rB_Mat[1,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[5, 2] := (rA_Mat[2,1] * rX_Pred_Horizon[4,1]) + (rA_Mat[2,2] * rX_Pred_Horizon[4,2]) + (rA_Mat[2,3] * rX_Pred_Horizon[4,3]) + (rA_Mat[2,4] * rX_Pred_Horizon[4,4]) + (rA_Mat[2,5] * rX_Pred_Horizon[4,5]) + (rA_Mat[2,6] * rX_Pred_Horizon[4,6]) + (rB_Mat[2,1] * rU_Opt_Seq[3,1]) + (rB_Mat[2,2] * rU_Opt_Seq[3,2]) + (rB_Mat[2,3] * rU_Opt_Seq[3,3]) + (rB_Mat[2,4] * rU_Opt_Seq[3,4]) + (rB_Mat[2,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[5, 3] := (rA_Mat[3,1] * rX_Pred_Horizon[4,1]) + (rA_Mat[3,2] * rX_Pred_Horizon[4,2]) + (rA_Mat[3,3] * rX_Pred_Horizon[4,3]) + (rA_Mat[3,4] * rX_Pred_Horizon[4,4]) + (rA_Mat[3,5] * rX_Pred_Horizon[4,5]) + (rA_Mat[3,6] * rX_Pred_Horizon[4,6]) + (rB_Mat[3,1] * rU_Opt_Seq[3,1]) + (rB_Mat[3,2] * rU_Opt_Seq[3,2]) + (rB_Mat[3,3] * rU_Opt_Seq[3,3]) + (rB_Mat[3,4] * rU_Opt_Seq[3,4]) + (rB_Mat[3,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[5, 4] := (rA_Mat[4,1] * rX_Pred_Horizon[4,1]) + (rA_Mat[4,2] * rX_Pred_Horizon[4,2]) + (rA_Mat[4,3] * rX_Pred_Horizon[4,3]) + (rA_Mat[4,4] * rX_Pred_Horizon[4,4]) + (rA_Mat[4,5] * rX_Pred_Horizon[4,5]) + (rA_Mat[4,6] * rX_Pred_Horizon[4,6]) + (rB_Mat[4,1] * rU_Opt_Seq[3,1]) + (rB_Mat[4,2] * rU_Opt_Seq[3,2]) + (rB_Mat[4,3] * rU_Opt_Seq[3,3]) + (rB_Mat[4,4] * rU_Opt_Seq[3,4]) + (rB_Mat[4,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[5, 5] := (rA_Mat[5,1] * rX_Pred_Horizon[4,1]) + (rA_Mat[5,2] * rX_Pred_Horizon[4,2]) + (rA_Mat[5,3] * rX_Pred_Horizon[4,3]) + (rA_Mat[5,4] * rX_Pred_Horizon[4,4]) + (rA_Mat[5,5] * rX_Pred_Horizon[4,5]) + (rA_Mat[5,6] * rX_Pred_Horizon[4,6]) + (rB_Mat[5,1] * rU_Opt_Seq[3,1]) + (rB_Mat[5,2] * rU_Opt_Seq[3,2]) + (rB_Mat[5,3] * rU_Opt_Seq[3,3]) + (rB_Mat[5,4] * rU_Opt_Seq[3,4]) + (rB_Mat[5,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[5, 6] := (rA_Mat[6,1] * rX_Pred_Horizon[4,1]) + (rA_Mat[6,2] * rX_Pred_Horizon[4,2]) + (rA_Mat[6,3] * rX_Pred_Horizon[4,3]) + (rA_Mat[6,4] * rX_Pred_Horizon[4,4]) + (rA_Mat[6,5] * rX_Pred_Horizon[4,5]) + (rA_Mat[6,6] * rX_Pred_Horizon[4,6]) + (rB_Mat[6,1] * rU_Opt_Seq[3,1]) + (rB_Mat[6,2] * rU_Opt_Seq[3,2]) + (rB_Mat[6,3] * rU_Opt_Seq[3,3]) + (rB_Mat[6,4] * rU_Opt_Seq[3,4]) + (rB_Mat[6,5] * rU_Opt_Seq[3,5]);

(* Iteration 2 - Evaluate Objective Function Cost J *)
rMPC_Cost_J := 0.0;
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[1] * (rX_Pred_Horizon[1,1] - rX_Target[1,1]) * (rX_Pred_Horizon[1,1] - rX_Target[1,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[2] * (rX_Pred_Horizon[1,2] - rX_Target[1,2]) * (rX_Pred_Horizon[1,2] - rX_Target[1,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[3] * (rX_Pred_Horizon[1,3] - rX_Target[1,3]) * (rX_Pred_Horizon[1,3] - rX_Target[1,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[4] * (rX_Pred_Horizon[1,4] - rX_Target[1,4]) * (rX_Pred_Horizon[1,4] - rX_Target[1,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[5] * (rX_Pred_Horizon[1,5] - rX_Target[1,5]) * (rX_Pred_Horizon[1,5] - rX_Target[1,5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[6] * (rX_Pred_Horizon[1,6] - rX_Target[1,6]) * (rX_Pred_Horizon[1,6] - rX_Target[1,6]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[1] * (rX_Pred_Horizon[2,1] - rX_Target[2,1]) * (rX_Pred_Horizon[2,1] - rX_Target[2,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[2] * (rX_Pred_Horizon[2,2] - rX_Target[2,2]) * (rX_Pred_Horizon[2,2] - rX_Target[2,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[3] * (rX_Pred_Horizon[2,3] - rX_Target[2,3]) * (rX_Pred_Horizon[2,3] - rX_Target[2,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[4] * (rX_Pred_Horizon[2,4] - rX_Target[2,4]) * (rX_Pred_Horizon[2,4] - rX_Target[2,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[5] * (rX_Pred_Horizon[2,5] - rX_Target[2,5]) * (rX_Pred_Horizon[2,5] - rX_Target[2,5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[6] * (rX_Pred_Horizon[2,6] - rX_Target[2,6]) * (rX_Pred_Horizon[2,6] - rX_Target[2,6]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[1] * (rX_Pred_Horizon[3,1] - rX_Target[3,1]) * (rX_Pred_Horizon[3,1] - rX_Target[3,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[2] * (rX_Pred_Horizon[3,2] - rX_Target[3,2]) * (rX_Pred_Horizon[3,2] - rX_Target[3,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[3] * (rX_Pred_Horizon[3,3] - rX_Target[3,3]) * (rX_Pred_Horizon[3,3] - rX_Target[3,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[4] * (rX_Pred_Horizon[3,4] - rX_Target[3,4]) * (rX_Pred_Horizon[3,4] - rX_Target[3,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[5] * (rX_Pred_Horizon[3,5] - rX_Target[3,5]) * (rX_Pred_Horizon[3,5] - rX_Target[3,5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[6] * (rX_Pred_Horizon[3,6] - rX_Target[3,6]) * (rX_Pred_Horizon[3,6] - rX_Target[3,6]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[1] * (rX_Pred_Horizon[4,1] - rX_Target[4,1]) * (rX_Pred_Horizon[4,1] - rX_Target[4,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[2] * (rX_Pred_Horizon[4,2] - rX_Target[4,2]) * (rX_Pred_Horizon[4,2] - rX_Target[4,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[3] * (rX_Pred_Horizon[4,3] - rX_Target[4,3]) * (rX_Pred_Horizon[4,3] - rX_Target[4,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[4] * (rX_Pred_Horizon[4,4] - rX_Target[4,4]) * (rX_Pred_Horizon[4,4] - rX_Target[4,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[5] * (rX_Pred_Horizon[4,5] - rX_Target[4,5]) * (rX_Pred_Horizon[4,5] - rX_Target[4,5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[6] * (rX_Pred_Horizon[4,6] - rX_Target[4,6]) * (rX_Pred_Horizon[4,6] - rX_Target[4,6]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[1] * (rX_Pred_Horizon[5,1] - rX_Target[5,1]) * (rX_Pred_Horizon[5,1] - rX_Target[5,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[2] * (rX_Pred_Horizon[5,2] - rX_Target[5,2]) * (rX_Pred_Horizon[5,2] - rX_Target[5,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[3] * (rX_Pred_Horizon[5,3] - rX_Target[5,3]) * (rX_Pred_Horizon[5,3] - rX_Target[5,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[4] * (rX_Pred_Horizon[5,4] - rX_Target[5,4]) * (rX_Pred_Horizon[5,4] - rX_Target[5,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[5] * (rX_Pred_Horizon[5,5] - rX_Target[5,5]) * (rX_Pred_Horizon[5,5] - rX_Target[5,5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[6] * (rX_Pred_Horizon[5,6] - rX_Target[5,6]) * (rX_Pred_Horizon[5,6] - rX_Target[5,6]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rP_Diag[1] * (rX_Pred_Horizon[5,1] - rX_Target[5,1]) * (rX_Pred_Horizon[5,1] - rX_Target[5,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rP_Diag[2] * (rX_Pred_Horizon[5,2] - rX_Target[5,2]) * (rX_Pred_Horizon[5,2] - rX_Target[5,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rP_Diag[3] * (rX_Pred_Horizon[5,3] - rX_Target[5,3]) * (rX_Pred_Horizon[5,3] - rX_Target[5,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rP_Diag[4] * (rX_Pred_Horizon[5,4] - rX_Target[5,4]) * (rX_Pred_Horizon[5,4] - rX_Target[5,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rP_Diag[5] * (rX_Pred_Horizon[5,5] - rX_Target[5,5]) * (rX_Pred_Horizon[5,5] - rX_Target[5,5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rP_Diag[6] * (rX_Pred_Horizon[5,6] - rX_Target[5,6]) * (rX_Pred_Horizon[5,6] - rX_Target[5,6]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[1] * rU_Opt_Seq[1,1] * rU_Opt_Seq[1,1]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[2] * rU_Opt_Seq[1,2] * rU_Opt_Seq[1,2]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[3] * rU_Opt_Seq[1,3] * rU_Opt_Seq[1,3]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[4] * rU_Opt_Seq[1,4] * rU_Opt_Seq[1,4]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[5] * rU_Opt_Seq[1,5] * rU_Opt_Seq[1,5]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[1] * rU_Opt_Seq[2,1] * rU_Opt_Seq[2,1]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[2] * rU_Opt_Seq[2,2] * rU_Opt_Seq[2,2]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[3] * rU_Opt_Seq[2,3] * rU_Opt_Seq[2,3]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[4] * rU_Opt_Seq[2,4] * rU_Opt_Seq[2,4]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[5] * rU_Opt_Seq[2,5] * rU_Opt_Seq[2,5]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[1] * rU_Opt_Seq[3,1] * rU_Opt_Seq[3,1]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[2] * rU_Opt_Seq[3,2] * rU_Opt_Seq[3,2]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[3] * rU_Opt_Seq[3,3] * rU_Opt_Seq[3,3]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[4] * rU_Opt_Seq[3,4] * rU_Opt_Seq[3,4]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[5] * rU_Opt_Seq[3,5] * rU_Opt_Seq[3,5]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[1] * (rU_Opt_Seq[1,1] - a_u_prev[1]) * (rU_Opt_Seq[1,1] - a_u_prev[1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[1] * (rU_Opt_Seq[2,1] - rU_Opt_Seq[1,1]) * (rU_Opt_Seq[2,1] - rU_Opt_Seq[1,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[1] * (rU_Opt_Seq[3,1] - rU_Opt_Seq[2,1]) * (rU_Opt_Seq[3,1] - rU_Opt_Seq[2,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[2] * (rU_Opt_Seq[1,2] - a_u_prev[2]) * (rU_Opt_Seq[1,2] - a_u_prev[2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[2] * (rU_Opt_Seq[2,2] - rU_Opt_Seq[1,2]) * (rU_Opt_Seq[2,2] - rU_Opt_Seq[1,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[2] * (rU_Opt_Seq[3,2] - rU_Opt_Seq[2,2]) * (rU_Opt_Seq[3,2] - rU_Opt_Seq[2,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[3] * (rU_Opt_Seq[1,3] - a_u_prev[3]) * (rU_Opt_Seq[1,3] - a_u_prev[3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[3] * (rU_Opt_Seq[2,3] - rU_Opt_Seq[1,3]) * (rU_Opt_Seq[2,3] - rU_Opt_Seq[1,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[3] * (rU_Opt_Seq[3,3] - rU_Opt_Seq[2,3]) * (rU_Opt_Seq[3,3] - rU_Opt_Seq[2,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[4] * (rU_Opt_Seq[1,4] - a_u_prev[4]) * (rU_Opt_Seq[1,4] - a_u_prev[4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[4] * (rU_Opt_Seq[2,4] - rU_Opt_Seq[1,4]) * (rU_Opt_Seq[2,4] - rU_Opt_Seq[1,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[4] * (rU_Opt_Seq[3,4] - rU_Opt_Seq[2,4]) * (rU_Opt_Seq[3,4] - rU_Opt_Seq[2,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[5] * (rU_Opt_Seq[1,5] - a_u_prev[5]) * (rU_Opt_Seq[1,5] - a_u_prev[5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[5] * (rU_Opt_Seq[2,5] - rU_Opt_Seq[1,5]) * (rU_Opt_Seq[2,5] - rU_Opt_Seq[1,5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[5] * (rU_Opt_Seq[3,5] - rU_Opt_Seq[2,5]) * (rU_Opt_Seq[3,5] - rU_Opt_Seq[2,5]));

(* Iteration 2 - Backward Adjoint Costate Propagation: lambda_h = A^T * lambda_{h+1} + Q * (x_h - x_ref) *)
(* Terminal Costate at h=5: lambda_5 = (P + Q) * (x_5 - x_target_5) *)
rLambda_Costate[5, 1] := (rP_Diag[1] + rQ_Diag[1]) * (rX_Pred_Horizon[5,1] - rX_Target[5,1]);
rLambda_Costate[5, 2] := (rP_Diag[2] + rQ_Diag[2]) * (rX_Pred_Horizon[5,2] - rX_Target[5,2]);
rLambda_Costate[5, 3] := (rP_Diag[3] + rQ_Diag[3]) * (rX_Pred_Horizon[5,3] - rX_Target[5,3]);
rLambda_Costate[5, 4] := (rP_Diag[4] + rQ_Diag[4]) * (rX_Pred_Horizon[5,4] - rX_Target[5,4]);
rLambda_Costate[5, 5] := (rP_Diag[5] + rQ_Diag[5]) * (rX_Pred_Horizon[5,5] - rX_Target[5,5]);
rLambda_Costate[5, 6] := (rP_Diag[6] + rQ_Diag[6]) * (rX_Pred_Horizon[5,6] - rX_Target[5,6]);

(* Adjoint Costate at h=4: lambda_4 = A^T * lambda_5 + Q * (x_4 - x_target_4) *)
rLambda_Costate[4, 1] := (rA_Mat[1,1] * rLambda_Costate[5,1]) + (rA_Mat[2,1] * rLambda_Costate[5,2]) + (rA_Mat[3,1] * rLambda_Costate[5,3]) + (rA_Mat[4,1] * rLambda_Costate[5,4]) + (rA_Mat[5,1] * rLambda_Costate[5,5]) + (rA_Mat[6,1] * rLambda_Costate[5,6]) + (rQ_Diag[1] * (rX_Pred_Horizon[4,1] - rX_Target[4,1]));
rLambda_Costate[4, 2] := (rA_Mat[1,2] * rLambda_Costate[5,1]) + (rA_Mat[2,2] * rLambda_Costate[5,2]) + (rA_Mat[3,2] * rLambda_Costate[5,3]) + (rA_Mat[4,2] * rLambda_Costate[5,4]) + (rA_Mat[5,2] * rLambda_Costate[5,5]) + (rA_Mat[6,2] * rLambda_Costate[5,6]) + (rQ_Diag[2] * (rX_Pred_Horizon[4,2] - rX_Target[4,2]));
rLambda_Costate[4, 3] := (rA_Mat[1,3] * rLambda_Costate[5,1]) + (rA_Mat[2,3] * rLambda_Costate[5,2]) + (rA_Mat[3,3] * rLambda_Costate[5,3]) + (rA_Mat[4,3] * rLambda_Costate[5,4]) + (rA_Mat[5,3] * rLambda_Costate[5,5]) + (rA_Mat[6,3] * rLambda_Costate[5,6]) + (rQ_Diag[3] * (rX_Pred_Horizon[4,3] - rX_Target[4,3]));
rLambda_Costate[4, 4] := (rA_Mat[1,4] * rLambda_Costate[5,1]) + (rA_Mat[2,4] * rLambda_Costate[5,2]) + (rA_Mat[3,4] * rLambda_Costate[5,3]) + (rA_Mat[4,4] * rLambda_Costate[5,4]) + (rA_Mat[5,4] * rLambda_Costate[5,5]) + (rA_Mat[6,4] * rLambda_Costate[5,6]) + (rQ_Diag[4] * (rX_Pred_Horizon[4,4] - rX_Target[4,4]));
rLambda_Costate[4, 5] := (rA_Mat[1,5] * rLambda_Costate[5,1]) + (rA_Mat[2,5] * rLambda_Costate[5,2]) + (rA_Mat[3,5] * rLambda_Costate[5,3]) + (rA_Mat[4,5] * rLambda_Costate[5,4]) + (rA_Mat[5,5] * rLambda_Costate[5,5]) + (rA_Mat[6,5] * rLambda_Costate[5,6]) + (rQ_Diag[5] * (rX_Pred_Horizon[4,5] - rX_Target[4,5]));
rLambda_Costate[4, 6] := (rA_Mat[1,6] * rLambda_Costate[5,1]) + (rA_Mat[2,6] * rLambda_Costate[5,2]) + (rA_Mat[3,6] * rLambda_Costate[5,3]) + (rA_Mat[4,6] * rLambda_Costate[5,4]) + (rA_Mat[5,6] * rLambda_Costate[5,5]) + (rA_Mat[6,6] * rLambda_Costate[5,6]) + (rQ_Diag[6] * (rX_Pred_Horizon[4,6] - rX_Target[4,6]));

(* Adjoint Costate at h=3: lambda_3 = A^T * lambda_4 + Q * (x_3 - x_target_3) *)
rLambda_Costate[3, 1] := (rA_Mat[1,1] * rLambda_Costate[4,1]) + (rA_Mat[2,1] * rLambda_Costate[4,2]) + (rA_Mat[3,1] * rLambda_Costate[4,3]) + (rA_Mat[4,1] * rLambda_Costate[4,4]) + (rA_Mat[5,1] * rLambda_Costate[4,5]) + (rA_Mat[6,1] * rLambda_Costate[4,6]) + (rQ_Diag[1] * (rX_Pred_Horizon[3,1] - rX_Target[3,1]));
rLambda_Costate[3, 2] := (rA_Mat[1,2] * rLambda_Costate[4,1]) + (rA_Mat[2,2] * rLambda_Costate[4,2]) + (rA_Mat[3,2] * rLambda_Costate[4,3]) + (rA_Mat[4,2] * rLambda_Costate[4,4]) + (rA_Mat[5,2] * rLambda_Costate[4,5]) + (rA_Mat[6,2] * rLambda_Costate[4,6]) + (rQ_Diag[2] * (rX_Pred_Horizon[3,2] - rX_Target[3,2]));
rLambda_Costate[3, 3] := (rA_Mat[1,3] * rLambda_Costate[4,1]) + (rA_Mat[2,3] * rLambda_Costate[4,2]) + (rA_Mat[3,3] * rLambda_Costate[4,3]) + (rA_Mat[4,3] * rLambda_Costate[4,4]) + (rA_Mat[5,3] * rLambda_Costate[4,5]) + (rA_Mat[6,3] * rLambda_Costate[4,6]) + (rQ_Diag[3] * (rX_Pred_Horizon[3,3] - rX_Target[3,3]));
rLambda_Costate[3, 4] := (rA_Mat[1,4] * rLambda_Costate[4,1]) + (rA_Mat[2,4] * rLambda_Costate[4,2]) + (rA_Mat[3,4] * rLambda_Costate[4,3]) + (rA_Mat[4,4] * rLambda_Costate[4,4]) + (rA_Mat[5,4] * rLambda_Costate[4,5]) + (rA_Mat[6,4] * rLambda_Costate[4,6]) + (rQ_Diag[4] * (rX_Pred_Horizon[3,4] - rX_Target[3,4]));
rLambda_Costate[3, 5] := (rA_Mat[1,5] * rLambda_Costate[4,1]) + (rA_Mat[2,5] * rLambda_Costate[4,2]) + (rA_Mat[3,5] * rLambda_Costate[4,3]) + (rA_Mat[4,5] * rLambda_Costate[4,4]) + (rA_Mat[5,5] * rLambda_Costate[4,5]) + (rA_Mat[6,5] * rLambda_Costate[4,6]) + (rQ_Diag[5] * (rX_Pred_Horizon[3,5] - rX_Target[3,5]));
rLambda_Costate[3, 6] := (rA_Mat[1,6] * rLambda_Costate[4,1]) + (rA_Mat[2,6] * rLambda_Costate[4,2]) + (rA_Mat[3,6] * rLambda_Costate[4,3]) + (rA_Mat[4,6] * rLambda_Costate[4,4]) + (rA_Mat[5,6] * rLambda_Costate[4,5]) + (rA_Mat[6,6] * rLambda_Costate[4,6]) + (rQ_Diag[6] * (rX_Pred_Horizon[3,6] - rX_Target[3,6]));

(* Adjoint Costate at h=2: lambda_2 = A^T * lambda_3 + Q * (x_2 - x_target_2) *)
rLambda_Costate[2, 1] := (rA_Mat[1,1] * rLambda_Costate[3,1]) + (rA_Mat[2,1] * rLambda_Costate[3,2]) + (rA_Mat[3,1] * rLambda_Costate[3,3]) + (rA_Mat[4,1] * rLambda_Costate[3,4]) + (rA_Mat[5,1] * rLambda_Costate[3,5]) + (rA_Mat[6,1] * rLambda_Costate[3,6]) + (rQ_Diag[1] * (rX_Pred_Horizon[2,1] - rX_Target[2,1]));
rLambda_Costate[2, 2] := (rA_Mat[1,2] * rLambda_Costate[3,1]) + (rA_Mat[2,2] * rLambda_Costate[3,2]) + (rA_Mat[3,2] * rLambda_Costate[3,3]) + (rA_Mat[4,2] * rLambda_Costate[3,4]) + (rA_Mat[5,2] * rLambda_Costate[3,5]) + (rA_Mat[6,2] * rLambda_Costate[3,6]) + (rQ_Diag[2] * (rX_Pred_Horizon[2,2] - rX_Target[2,2]));
rLambda_Costate[2, 3] := (rA_Mat[1,3] * rLambda_Costate[3,1]) + (rA_Mat[2,3] * rLambda_Costate[3,2]) + (rA_Mat[3,3] * rLambda_Costate[3,3]) + (rA_Mat[4,3] * rLambda_Costate[3,4]) + (rA_Mat[5,3] * rLambda_Costate[3,5]) + (rA_Mat[6,3] * rLambda_Costate[3,6]) + (rQ_Diag[3] * (rX_Pred_Horizon[2,3] - rX_Target[2,3]));
rLambda_Costate[2, 4] := (rA_Mat[1,4] * rLambda_Costate[3,1]) + (rA_Mat[2,4] * rLambda_Costate[3,2]) + (rA_Mat[3,4] * rLambda_Costate[3,3]) + (rA_Mat[4,4] * rLambda_Costate[3,4]) + (rA_Mat[5,4] * rLambda_Costate[3,5]) + (rA_Mat[6,4] * rLambda_Costate[3,6]) + (rQ_Diag[4] * (rX_Pred_Horizon[2,4] - rX_Target[2,4]));
rLambda_Costate[2, 5] := (rA_Mat[1,5] * rLambda_Costate[3,1]) + (rA_Mat[2,5] * rLambda_Costate[3,2]) + (rA_Mat[3,5] * rLambda_Costate[3,3]) + (rA_Mat[4,5] * rLambda_Costate[3,4]) + (rA_Mat[5,5] * rLambda_Costate[3,5]) + (rA_Mat[6,5] * rLambda_Costate[3,6]) + (rQ_Diag[5] * (rX_Pred_Horizon[2,5] - rX_Target[2,5]));
rLambda_Costate[2, 6] := (rA_Mat[1,6] * rLambda_Costate[3,1]) + (rA_Mat[2,6] * rLambda_Costate[3,2]) + (rA_Mat[3,6] * rLambda_Costate[3,3]) + (rA_Mat[4,6] * rLambda_Costate[3,4]) + (rA_Mat[5,6] * rLambda_Costate[3,5]) + (rA_Mat[6,6] * rLambda_Costate[3,6]) + (rQ_Diag[6] * (rX_Pred_Horizon[2,6] - rX_Target[2,6]));

(* Adjoint Costate at h=1: lambda_1 = A^T * lambda_2 + Q * (x_1 - x_target_1) *)
rLambda_Costate[1, 1] := (rA_Mat[1,1] * rLambda_Costate[2,1]) + (rA_Mat[2,1] * rLambda_Costate[2,2]) + (rA_Mat[3,1] * rLambda_Costate[2,3]) + (rA_Mat[4,1] * rLambda_Costate[2,4]) + (rA_Mat[5,1] * rLambda_Costate[2,5]) + (rA_Mat[6,1] * rLambda_Costate[2,6]) + (rQ_Diag[1] * (rX_Pred_Horizon[1,1] - rX_Target[1,1]));
rLambda_Costate[1, 2] := (rA_Mat[1,2] * rLambda_Costate[2,1]) + (rA_Mat[2,2] * rLambda_Costate[2,2]) + (rA_Mat[3,2] * rLambda_Costate[2,3]) + (rA_Mat[4,2] * rLambda_Costate[2,4]) + (rA_Mat[5,2] * rLambda_Costate[2,5]) + (rA_Mat[6,2] * rLambda_Costate[2,6]) + (rQ_Diag[2] * (rX_Pred_Horizon[1,2] - rX_Target[1,2]));
rLambda_Costate[1, 3] := (rA_Mat[1,3] * rLambda_Costate[2,1]) + (rA_Mat[2,3] * rLambda_Costate[2,2]) + (rA_Mat[3,3] * rLambda_Costate[2,3]) + (rA_Mat[4,3] * rLambda_Costate[2,4]) + (rA_Mat[5,3] * rLambda_Costate[2,5]) + (rA_Mat[6,3] * rLambda_Costate[2,6]) + (rQ_Diag[3] * (rX_Pred_Horizon[1,3] - rX_Target[1,3]));
rLambda_Costate[1, 4] := (rA_Mat[1,4] * rLambda_Costate[2,1]) + (rA_Mat[2,4] * rLambda_Costate[2,2]) + (rA_Mat[3,4] * rLambda_Costate[2,3]) + (rA_Mat[4,4] * rLambda_Costate[2,4]) + (rA_Mat[5,4] * rLambda_Costate[2,5]) + (rA_Mat[6,4] * rLambda_Costate[2,6]) + (rQ_Diag[4] * (rX_Pred_Horizon[1,4] - rX_Target[1,4]));
rLambda_Costate[1, 5] := (rA_Mat[1,5] * rLambda_Costate[2,1]) + (rA_Mat[2,5] * rLambda_Costate[2,2]) + (rA_Mat[3,5] * rLambda_Costate[2,3]) + (rA_Mat[4,5] * rLambda_Costate[2,4]) + (rA_Mat[5,5] * rLambda_Costate[2,5]) + (rA_Mat[6,5] * rLambda_Costate[2,6]) + (rQ_Diag[5] * (rX_Pred_Horizon[1,5] - rX_Target[1,5]));
rLambda_Costate[1, 6] := (rA_Mat[1,6] * rLambda_Costate[2,1]) + (rA_Mat[2,6] * rLambda_Costate[2,2]) + (rA_Mat[3,6] * rLambda_Costate[2,3]) + (rA_Mat[4,6] * rLambda_Costate[2,4]) + (rA_Mat[5,6] * rLambda_Costate[2,5]) + (rA_Mat[6,6] * rLambda_Costate[2,6]) + (rQ_Diag[6] * (rX_Pred_Horizon[1,6] - rX_Target[1,6]));

(* Iteration 2 - Analytical Gradient Computation w.r.t. Control Inputs u_h *)
rMPC_GradNormSq := 0.0;
(* Gradient for u_1 (h=1) *)
rGrad_J[1, 1] := (rB_Mat[1,1] * rLambda_Costate[1,1]) + (rB_Mat[2,1] * rLambda_Costate[1,2]) + (rB_Mat[3,1] * rLambda_Costate[1,3]) + (rB_Mat[4,1] * rLambda_Costate[1,4]) + (rB_Mat[5,1] * rLambda_Costate[1,5]) + (rB_Mat[6,1] * rLambda_Costate[1,6]) + (rR_Diag[1] * rU_Opt_Seq[1,1]) + (rS_Diag[1] * (rU_Opt_Seq[1,1] - a_u_prev[1])) - (rS_Diag[1] * (rU_Opt_Seq[2,1] - rU_Opt_Seq[1,1]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[1, 1] * rGrad_J[1, 1]);
rGrad_J[1, 2] := (rB_Mat[1,2] * rLambda_Costate[1,1]) + (rB_Mat[2,2] * rLambda_Costate[1,2]) + (rB_Mat[3,2] * rLambda_Costate[1,3]) + (rB_Mat[4,2] * rLambda_Costate[1,4]) + (rB_Mat[5,2] * rLambda_Costate[1,5]) + (rB_Mat[6,2] * rLambda_Costate[1,6]) + (rR_Diag[2] * rU_Opt_Seq[1,2]) + (rS_Diag[2] * (rU_Opt_Seq[1,2] - a_u_prev[2])) - (rS_Diag[2] * (rU_Opt_Seq[2,2] - rU_Opt_Seq[1,2]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[1, 2] * rGrad_J[1, 2]);
rGrad_J[1, 3] := (rB_Mat[1,3] * rLambda_Costate[1,1]) + (rB_Mat[2,3] * rLambda_Costate[1,2]) + (rB_Mat[3,3] * rLambda_Costate[1,3]) + (rB_Mat[4,3] * rLambda_Costate[1,4]) + (rB_Mat[5,3] * rLambda_Costate[1,5]) + (rB_Mat[6,3] * rLambda_Costate[1,6]) + (rR_Diag[3] * rU_Opt_Seq[1,3]) + (rS_Diag[3] * (rU_Opt_Seq[1,3] - a_u_prev[3])) - (rS_Diag[3] * (rU_Opt_Seq[2,3] - rU_Opt_Seq[1,3]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[1, 3] * rGrad_J[1, 3]);
rGrad_J[1, 4] := (rB_Mat[1,4] * rLambda_Costate[1,1]) + (rB_Mat[2,4] * rLambda_Costate[1,2]) + (rB_Mat[3,4] * rLambda_Costate[1,3]) + (rB_Mat[4,4] * rLambda_Costate[1,4]) + (rB_Mat[5,4] * rLambda_Costate[1,5]) + (rB_Mat[6,4] * rLambda_Costate[1,6]) + (rR_Diag[4] * rU_Opt_Seq[1,4]) + (rS_Diag[4] * (rU_Opt_Seq[1,4] - a_u_prev[4])) - (rS_Diag[4] * (rU_Opt_Seq[2,4] - rU_Opt_Seq[1,4]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[1, 4] * rGrad_J[1, 4]);
rGrad_J[1, 5] := (rB_Mat[1,5] * rLambda_Costate[1,1]) + (rB_Mat[2,5] * rLambda_Costate[1,2]) + (rB_Mat[3,5] * rLambda_Costate[1,3]) + (rB_Mat[4,5] * rLambda_Costate[1,4]) + (rB_Mat[5,5] * rLambda_Costate[1,5]) + (rB_Mat[6,5] * rLambda_Costate[1,6]) + (rR_Diag[5] * rU_Opt_Seq[1,5]) + (rS_Diag[5] * (rU_Opt_Seq[1,5] - a_u_prev[5])) - (rS_Diag[5] * (rU_Opt_Seq[2,5] - rU_Opt_Seq[1,5]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[1, 5] * rGrad_J[1, 5]);

(* Gradient for u_2 (h=2) *)
rGrad_J[2, 1] := (rB_Mat[1,1] * rLambda_Costate[2,1]) + (rB_Mat[2,1] * rLambda_Costate[2,2]) + (rB_Mat[3,1] * rLambda_Costate[2,3]) + (rB_Mat[4,1] * rLambda_Costate[2,4]) + (rB_Mat[5,1] * rLambda_Costate[2,5]) + (rB_Mat[6,1] * rLambda_Costate[2,6]) + (rR_Diag[1] * rU_Opt_Seq[2,1]) + (rS_Diag[1] * (rU_Opt_Seq[2,1] - rU_Opt_Seq[1,1])) - (rS_Diag[1] * (rU_Opt_Seq[3,1] - rU_Opt_Seq[2,1]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[2, 1] * rGrad_J[2, 1]);
rGrad_J[2, 2] := (rB_Mat[1,2] * rLambda_Costate[2,1]) + (rB_Mat[2,2] * rLambda_Costate[2,2]) + (rB_Mat[3,2] * rLambda_Costate[2,3]) + (rB_Mat[4,2] * rLambda_Costate[2,4]) + (rB_Mat[5,2] * rLambda_Costate[2,5]) + (rB_Mat[6,2] * rLambda_Costate[2,6]) + (rR_Diag[2] * rU_Opt_Seq[2,2]) + (rS_Diag[2] * (rU_Opt_Seq[2,2] - rU_Opt_Seq[1,2])) - (rS_Diag[2] * (rU_Opt_Seq[3,2] - rU_Opt_Seq[2,2]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[2, 2] * rGrad_J[2, 2]);
rGrad_J[2, 3] := (rB_Mat[1,3] * rLambda_Costate[2,1]) + (rB_Mat[2,3] * rLambda_Costate[2,2]) + (rB_Mat[3,3] * rLambda_Costate[2,3]) + (rB_Mat[4,3] * rLambda_Costate[2,4]) + (rB_Mat[5,3] * rLambda_Costate[2,5]) + (rB_Mat[6,3] * rLambda_Costate[2,6]) + (rR_Diag[3] * rU_Opt_Seq[2,3]) + (rS_Diag[3] * (rU_Opt_Seq[2,3] - rU_Opt_Seq[1,3])) - (rS_Diag[3] * (rU_Opt_Seq[3,3] - rU_Opt_Seq[2,3]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[2, 3] * rGrad_J[2, 3]);
rGrad_J[2, 4] := (rB_Mat[1,4] * rLambda_Costate[2,1]) + (rB_Mat[2,4] * rLambda_Costate[2,2]) + (rB_Mat[3,4] * rLambda_Costate[2,3]) + (rB_Mat[4,4] * rLambda_Costate[2,4]) + (rB_Mat[5,4] * rLambda_Costate[2,5]) + (rB_Mat[6,4] * rLambda_Costate[2,6]) + (rR_Diag[4] * rU_Opt_Seq[2,4]) + (rS_Diag[4] * (rU_Opt_Seq[2,4] - rU_Opt_Seq[1,4])) - (rS_Diag[4] * (rU_Opt_Seq[3,4] - rU_Opt_Seq[2,4]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[2, 4] * rGrad_J[2, 4]);
rGrad_J[2, 5] := (rB_Mat[1,5] * rLambda_Costate[2,1]) + (rB_Mat[2,5] * rLambda_Costate[2,2]) + (rB_Mat[3,5] * rLambda_Costate[2,3]) + (rB_Mat[4,5] * rLambda_Costate[2,4]) + (rB_Mat[5,5] * rLambda_Costate[2,5]) + (rB_Mat[6,5] * rLambda_Costate[2,6]) + (rR_Diag[5] * rU_Opt_Seq[2,5]) + (rS_Diag[5] * (rU_Opt_Seq[2,5] - rU_Opt_Seq[1,5])) - (rS_Diag[5] * (rU_Opt_Seq[3,5] - rU_Opt_Seq[2,5]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[2, 5] * rGrad_J[2, 5]);

(* Gradient for u_3 (h=3, held through h=4, 5) *)
rGrad_J[3, 1] := (rB_Mat[1,1] * (rLambda_Costate[3,1] + rLambda_Costate[4,1] + rLambda_Costate[5,1])) + (rB_Mat[2,1] * (rLambda_Costate[3,2] + rLambda_Costate[4,2] + rLambda_Costate[5,2])) + (rB_Mat[3,1] * (rLambda_Costate[3,3] + rLambda_Costate[4,3] + rLambda_Costate[5,3])) + (rB_Mat[4,1] * (rLambda_Costate[3,4] + rLambda_Costate[4,4] + rLambda_Costate[5,4])) + (rB_Mat[5,1] * (rLambda_Costate[3,5] + rLambda_Costate[4,5] + rLambda_Costate[5,5])) + (rB_Mat[6,1] * (rLambda_Costate[3,6] + rLambda_Costate[4,6] + rLambda_Costate[5,6])) + (rR_Diag[1] * rU_Opt_Seq[3,1]) + (rS_Diag[1] * (rU_Opt_Seq[3,1] - rU_Opt_Seq[2,1]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[3, 1] * rGrad_J[3, 1]);
rGrad_J[3, 2] := (rB_Mat[1,2] * (rLambda_Costate[3,1] + rLambda_Costate[4,1] + rLambda_Costate[5,1])) + (rB_Mat[2,2] * (rLambda_Costate[3,2] + rLambda_Costate[4,2] + rLambda_Costate[5,2])) + (rB_Mat[3,2] * (rLambda_Costate[3,3] + rLambda_Costate[4,3] + rLambda_Costate[5,3])) + (rB_Mat[4,2] * (rLambda_Costate[3,4] + rLambda_Costate[4,4] + rLambda_Costate[5,4])) + (rB_Mat[5,2] * (rLambda_Costate[3,5] + rLambda_Costate[4,5] + rLambda_Costate[5,5])) + (rB_Mat[6,2] * (rLambda_Costate[3,6] + rLambda_Costate[4,6] + rLambda_Costate[5,6])) + (rR_Diag[2] * rU_Opt_Seq[3,2]) + (rS_Diag[2] * (rU_Opt_Seq[3,2] - rU_Opt_Seq[2,2]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[3, 2] * rGrad_J[3, 2]);
rGrad_J[3, 3] := (rB_Mat[1,3] * (rLambda_Costate[3,1] + rLambda_Costate[4,1] + rLambda_Costate[5,1])) + (rB_Mat[2,3] * (rLambda_Costate[3,2] + rLambda_Costate[4,2] + rLambda_Costate[5,2])) + (rB_Mat[3,3] * (rLambda_Costate[3,3] + rLambda_Costate[4,3] + rLambda_Costate[5,3])) + (rB_Mat[4,3] * (rLambda_Costate[3,4] + rLambda_Costate[4,4] + rLambda_Costate[5,4])) + (rB_Mat[5,3] * (rLambda_Costate[3,5] + rLambda_Costate[4,5] + rLambda_Costate[5,5])) + (rB_Mat[6,3] * (rLambda_Costate[3,6] + rLambda_Costate[4,6] + rLambda_Costate[5,6])) + (rR_Diag[3] * rU_Opt_Seq[3,3]) + (rS_Diag[3] * (rU_Opt_Seq[3,3] - rU_Opt_Seq[2,3]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[3, 3] * rGrad_J[3, 3]);
rGrad_J[3, 4] := (rB_Mat[1,4] * (rLambda_Costate[3,1] + rLambda_Costate[4,1] + rLambda_Costate[5,1])) + (rB_Mat[2,4] * (rLambda_Costate[3,2] + rLambda_Costate[4,2] + rLambda_Costate[5,2])) + (rB_Mat[3,4] * (rLambda_Costate[3,3] + rLambda_Costate[4,3] + rLambda_Costate[5,3])) + (rB_Mat[4,4] * (rLambda_Costate[3,4] + rLambda_Costate[4,4] + rLambda_Costate[5,4])) + (rB_Mat[5,4] * (rLambda_Costate[3,5] + rLambda_Costate[4,5] + rLambda_Costate[5,5])) + (rB_Mat[6,4] * (rLambda_Costate[3,6] + rLambda_Costate[4,6] + rLambda_Costate[5,6])) + (rR_Diag[4] * rU_Opt_Seq[3,4]) + (rS_Diag[4] * (rU_Opt_Seq[3,4] - rU_Opt_Seq[2,4]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[3, 4] * rGrad_J[3, 4]);
rGrad_J[3, 5] := (rB_Mat[1,5] * (rLambda_Costate[3,1] + rLambda_Costate[4,1] + rLambda_Costate[5,1])) + (rB_Mat[2,5] * (rLambda_Costate[3,2] + rLambda_Costate[4,2] + rLambda_Costate[5,2])) + (rB_Mat[3,5] * (rLambda_Costate[3,3] + rLambda_Costate[4,3] + rLambda_Costate[5,3])) + (rB_Mat[4,5] * (rLambda_Costate[3,4] + rLambda_Costate[4,4] + rLambda_Costate[5,4])) + (rB_Mat[5,5] * (rLambda_Costate[3,5] + rLambda_Costate[4,5] + rLambda_Costate[5,5])) + (rB_Mat[6,5] * (rLambda_Costate[3,6] + rLambda_Costate[4,6] + rLambda_Costate[5,6])) + (rR_Diag[5] * rU_Opt_Seq[3,5]) + (rS_Diag[5] * (rU_Opt_Seq[3,5] - rU_Opt_Seq[2,5]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[3, 5] * rGrad_J[3, 5]);

(* Iteration 2 - Projected Gradient Step with Hard Box & Dynamic Slew Limits *)
rTemp_Val := rU_Opt_Seq[1, 1] - (rAlpha_PGD_StepSize * rGrad_J[1, 1]);
(* Slew limit against prior actuator output *)
IF rTemp_Val > (a_u_prev[1] + rDeltaU_Max[1]) THEN
    rTemp_Val := a_u_prev[1] + rDeltaU_Max[1];
ELSIF rTemp_Val < (a_u_prev[1] - rDeltaU_Max[1]) THEN
    rTemp_Val := a_u_prev[1] - rDeltaU_Max[1];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[1] THEN
    rTemp_Val := rU_BoxMax[1];
ELSIF rTemp_Val < rU_BoxMin[1] THEN
    rTemp_Val := rU_BoxMin[1];
END_IF;
rU_Opt_Seq[1, 1] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[1, 2] - (rAlpha_PGD_StepSize * rGrad_J[1, 2]);
(* Slew limit against prior actuator output *)
IF rTemp_Val > (a_u_prev[2] + rDeltaU_Max[2]) THEN
    rTemp_Val := a_u_prev[2] + rDeltaU_Max[2];
ELSIF rTemp_Val < (a_u_prev[2] - rDeltaU_Max[2]) THEN
    rTemp_Val := a_u_prev[2] - rDeltaU_Max[2];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[2] THEN
    rTemp_Val := rU_BoxMax[2];
ELSIF rTemp_Val < rU_BoxMin[2] THEN
    rTemp_Val := rU_BoxMin[2];
END_IF;
rU_Opt_Seq[1, 2] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[1, 3] - (rAlpha_PGD_StepSize * rGrad_J[1, 3]);
(* Slew limit against prior actuator output *)
IF rTemp_Val > (a_u_prev[3] + rDeltaU_Max[3]) THEN
    rTemp_Val := a_u_prev[3] + rDeltaU_Max[3];
ELSIF rTemp_Val < (a_u_prev[3] - rDeltaU_Max[3]) THEN
    rTemp_Val := a_u_prev[3] - rDeltaU_Max[3];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[3] THEN
    rTemp_Val := rU_BoxMax[3];
ELSIF rTemp_Val < rU_BoxMin[3] THEN
    rTemp_Val := rU_BoxMin[3];
END_IF;
rU_Opt_Seq[1, 3] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[1, 4] - (rAlpha_PGD_StepSize * rGrad_J[1, 4]);
(* Slew limit against prior actuator output *)
IF rTemp_Val > (a_u_prev[4] + rDeltaU_Max[4]) THEN
    rTemp_Val := a_u_prev[4] + rDeltaU_Max[4];
ELSIF rTemp_Val < (a_u_prev[4] - rDeltaU_Max[4]) THEN
    rTemp_Val := a_u_prev[4] - rDeltaU_Max[4];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[4] THEN
    rTemp_Val := rU_BoxMax[4];
ELSIF rTemp_Val < rU_BoxMin[4] THEN
    rTemp_Val := rU_BoxMin[4];
END_IF;
rU_Opt_Seq[1, 4] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[1, 5] - (rAlpha_PGD_StepSize * rGrad_J[1, 5]);
(* Slew limit against prior actuator output *)
IF rTemp_Val > (a_u_prev[5] + rDeltaU_Max[5]) THEN
    rTemp_Val := a_u_prev[5] + rDeltaU_Max[5];
ELSIF rTemp_Val < (a_u_prev[5] - rDeltaU_Max[5]) THEN
    rTemp_Val := a_u_prev[5] - rDeltaU_Max[5];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[5] THEN
    rTemp_Val := rU_BoxMax[5];
ELSIF rTemp_Val < rU_BoxMin[5] THEN
    rTemp_Val := rU_BoxMin[5];
END_IF;
rU_Opt_Seq[1, 5] := rTemp_Val;

rTemp_Val := rU_Opt_Seq[2, 1] - (rAlpha_PGD_StepSize * rGrad_J[2, 1]);
(* Slew limit against step 1 *)
IF rTemp_Val > (rU_Opt_Seq[1, 1] + rDeltaU_Max[1]) THEN
    rTemp_Val := rU_Opt_Seq[1, 1] + rDeltaU_Max[1];
ELSIF rTemp_Val < (rU_Opt_Seq[1, 1] - rDeltaU_Max[1]) THEN
    rTemp_Val := rU_Opt_Seq[1, 1] - rDeltaU_Max[1];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[1] THEN
    rTemp_Val := rU_BoxMax[1];
ELSIF rTemp_Val < rU_BoxMin[1] THEN
    rTemp_Val := rU_BoxMin[1];
END_IF;
rU_Opt_Seq[2, 1] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[2, 2] - (rAlpha_PGD_StepSize * rGrad_J[2, 2]);
(* Slew limit against step 1 *)
IF rTemp_Val > (rU_Opt_Seq[1, 2] + rDeltaU_Max[2]) THEN
    rTemp_Val := rU_Opt_Seq[1, 2] + rDeltaU_Max[2];
ELSIF rTemp_Val < (rU_Opt_Seq[1, 2] - rDeltaU_Max[2]) THEN
    rTemp_Val := rU_Opt_Seq[1, 2] - rDeltaU_Max[2];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[2] THEN
    rTemp_Val := rU_BoxMax[2];
ELSIF rTemp_Val < rU_BoxMin[2] THEN
    rTemp_Val := rU_BoxMin[2];
END_IF;
rU_Opt_Seq[2, 2] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[2, 3] - (rAlpha_PGD_StepSize * rGrad_J[2, 3]);
(* Slew limit against step 1 *)
IF rTemp_Val > (rU_Opt_Seq[1, 3] + rDeltaU_Max[3]) THEN
    rTemp_Val := rU_Opt_Seq[1, 3] + rDeltaU_Max[3];
ELSIF rTemp_Val < (rU_Opt_Seq[1, 3] - rDeltaU_Max[3]) THEN
    rTemp_Val := rU_Opt_Seq[1, 3] - rDeltaU_Max[3];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[3] THEN
    rTemp_Val := rU_BoxMax[3];
ELSIF rTemp_Val < rU_BoxMin[3] THEN
    rTemp_Val := rU_BoxMin[3];
END_IF;
rU_Opt_Seq[2, 3] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[2, 4] - (rAlpha_PGD_StepSize * rGrad_J[2, 4]);
(* Slew limit against step 1 *)
IF rTemp_Val > (rU_Opt_Seq[1, 4] + rDeltaU_Max[4]) THEN
    rTemp_Val := rU_Opt_Seq[1, 4] + rDeltaU_Max[4];
ELSIF rTemp_Val < (rU_Opt_Seq[1, 4] - rDeltaU_Max[4]) THEN
    rTemp_Val := rU_Opt_Seq[1, 4] - rDeltaU_Max[4];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[4] THEN
    rTemp_Val := rU_BoxMax[4];
ELSIF rTemp_Val < rU_BoxMin[4] THEN
    rTemp_Val := rU_BoxMin[4];
END_IF;
rU_Opt_Seq[2, 4] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[2, 5] - (rAlpha_PGD_StepSize * rGrad_J[2, 5]);
(* Slew limit against step 1 *)
IF rTemp_Val > (rU_Opt_Seq[1, 5] + rDeltaU_Max[5]) THEN
    rTemp_Val := rU_Opt_Seq[1, 5] + rDeltaU_Max[5];
ELSIF rTemp_Val < (rU_Opt_Seq[1, 5] - rDeltaU_Max[5]) THEN
    rTemp_Val := rU_Opt_Seq[1, 5] - rDeltaU_Max[5];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[5] THEN
    rTemp_Val := rU_BoxMax[5];
ELSIF rTemp_Val < rU_BoxMin[5] THEN
    rTemp_Val := rU_BoxMin[5];
END_IF;
rU_Opt_Seq[2, 5] := rTemp_Val;

rTemp_Val := rU_Opt_Seq[3, 1] - (rAlpha_PGD_StepSize * rGrad_J[3, 1]);
(* Slew limit against step 2 *)
IF rTemp_Val > (rU_Opt_Seq[2, 1] + rDeltaU_Max[1]) THEN
    rTemp_Val := rU_Opt_Seq[2, 1] + rDeltaU_Max[1];
ELSIF rTemp_Val < (rU_Opt_Seq[2, 1] - rDeltaU_Max[1]) THEN
    rTemp_Val := rU_Opt_Seq[2, 1] - rDeltaU_Max[1];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[1] THEN
    rTemp_Val := rU_BoxMax[1];
ELSIF rTemp_Val < rU_BoxMin[1] THEN
    rTemp_Val := rU_BoxMin[1];
END_IF;
rU_Opt_Seq[3, 1] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[3, 2] - (rAlpha_PGD_StepSize * rGrad_J[3, 2]);
(* Slew limit against step 2 *)
IF rTemp_Val > (rU_Opt_Seq[2, 2] + rDeltaU_Max[2]) THEN
    rTemp_Val := rU_Opt_Seq[2, 2] + rDeltaU_Max[2];
ELSIF rTemp_Val < (rU_Opt_Seq[2, 2] - rDeltaU_Max[2]) THEN
    rTemp_Val := rU_Opt_Seq[2, 2] - rDeltaU_Max[2];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[2] THEN
    rTemp_Val := rU_BoxMax[2];
ELSIF rTemp_Val < rU_BoxMin[2] THEN
    rTemp_Val := rU_BoxMin[2];
END_IF;
rU_Opt_Seq[3, 2] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[3, 3] - (rAlpha_PGD_StepSize * rGrad_J[3, 3]);
(* Slew limit against step 2 *)
IF rTemp_Val > (rU_Opt_Seq[2, 3] + rDeltaU_Max[3]) THEN
    rTemp_Val := rU_Opt_Seq[2, 3] + rDeltaU_Max[3];
ELSIF rTemp_Val < (rU_Opt_Seq[2, 3] - rDeltaU_Max[3]) THEN
    rTemp_Val := rU_Opt_Seq[2, 3] - rDeltaU_Max[3];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[3] THEN
    rTemp_Val := rU_BoxMax[3];
ELSIF rTemp_Val < rU_BoxMin[3] THEN
    rTemp_Val := rU_BoxMin[3];
END_IF;
rU_Opt_Seq[3, 3] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[3, 4] - (rAlpha_PGD_StepSize * rGrad_J[3, 4]);
(* Slew limit against step 2 *)
IF rTemp_Val > (rU_Opt_Seq[2, 4] + rDeltaU_Max[4]) THEN
    rTemp_Val := rU_Opt_Seq[2, 4] + rDeltaU_Max[4];
ELSIF rTemp_Val < (rU_Opt_Seq[2, 4] - rDeltaU_Max[4]) THEN
    rTemp_Val := rU_Opt_Seq[2, 4] - rDeltaU_Max[4];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[4] THEN
    rTemp_Val := rU_BoxMax[4];
ELSIF rTemp_Val < rU_BoxMin[4] THEN
    rTemp_Val := rU_BoxMin[4];
END_IF;
rU_Opt_Seq[3, 4] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[3, 5] - (rAlpha_PGD_StepSize * rGrad_J[3, 5]);
(* Slew limit against step 2 *)
IF rTemp_Val > (rU_Opt_Seq[2, 5] + rDeltaU_Max[5]) THEN
    rTemp_Val := rU_Opt_Seq[2, 5] + rDeltaU_Max[5];
ELSIF rTemp_Val < (rU_Opt_Seq[2, 5] - rDeltaU_Max[5]) THEN
    rTemp_Val := rU_Opt_Seq[2, 5] - rDeltaU_Max[5];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[5] THEN
    rTemp_Val := rU_BoxMax[5];
ELSIF rTemp_Val < rU_BoxMin[5] THEN
    rTemp_Val := rU_BoxMin[5];
END_IF;
rU_Opt_Seq[3, 5] := rTemp_Val;

(* ================================================================================================== *)
(* MPC PROJECTED GRADIENT DESCENT -- UNROLLED ITERATION 3 OF 10                                 *)
(* ================================================================================================== *)
iPGD_IterCount := 3;

(* Iteration 3 - Forward State Prediction Step 1 (h=1): x_1 = A * x_hat + B * u_1 *)
rX_Pred_Horizon[1, 1] := (rA_Mat[1,1] * a_x_hat[1]) + (rA_Mat[1,2] * a_x_hat[2]) + (rA_Mat[1,3] * a_x_hat[3]) + (rA_Mat[1,4] * a_x_hat[4]) + (rA_Mat[1,5] * a_x_hat[5]) + (rA_Mat[1,6] * a_x_hat[6]) + (rB_Mat[1,1] * rU_Opt_Seq[1,1]) + (rB_Mat[1,2] * rU_Opt_Seq[1,2]) + (rB_Mat[1,3] * rU_Opt_Seq[1,3]) + (rB_Mat[1,4] * rU_Opt_Seq[1,4]) + (rB_Mat[1,5] * rU_Opt_Seq[1,5]);
rX_Pred_Horizon[1, 2] := (rA_Mat[2,1] * a_x_hat[1]) + (rA_Mat[2,2] * a_x_hat[2]) + (rA_Mat[2,3] * a_x_hat[3]) + (rA_Mat[2,4] * a_x_hat[4]) + (rA_Mat[2,5] * a_x_hat[5]) + (rA_Mat[2,6] * a_x_hat[6]) + (rB_Mat[2,1] * rU_Opt_Seq[1,1]) + (rB_Mat[2,2] * rU_Opt_Seq[1,2]) + (rB_Mat[2,3] * rU_Opt_Seq[1,3]) + (rB_Mat[2,4] * rU_Opt_Seq[1,4]) + (rB_Mat[2,5] * rU_Opt_Seq[1,5]);
rX_Pred_Horizon[1, 3] := (rA_Mat[3,1] * a_x_hat[1]) + (rA_Mat[3,2] * a_x_hat[2]) + (rA_Mat[3,3] * a_x_hat[3]) + (rA_Mat[3,4] * a_x_hat[4]) + (rA_Mat[3,5] * a_x_hat[5]) + (rA_Mat[3,6] * a_x_hat[6]) + (rB_Mat[3,1] * rU_Opt_Seq[1,1]) + (rB_Mat[3,2] * rU_Opt_Seq[1,2]) + (rB_Mat[3,3] * rU_Opt_Seq[1,3]) + (rB_Mat[3,4] * rU_Opt_Seq[1,4]) + (rB_Mat[3,5] * rU_Opt_Seq[1,5]);
rX_Pred_Horizon[1, 4] := (rA_Mat[4,1] * a_x_hat[1]) + (rA_Mat[4,2] * a_x_hat[2]) + (rA_Mat[4,3] * a_x_hat[3]) + (rA_Mat[4,4] * a_x_hat[4]) + (rA_Mat[4,5] * a_x_hat[5]) + (rA_Mat[4,6] * a_x_hat[6]) + (rB_Mat[4,1] * rU_Opt_Seq[1,1]) + (rB_Mat[4,2] * rU_Opt_Seq[1,2]) + (rB_Mat[4,3] * rU_Opt_Seq[1,3]) + (rB_Mat[4,4] * rU_Opt_Seq[1,4]) + (rB_Mat[4,5] * rU_Opt_Seq[1,5]);
rX_Pred_Horizon[1, 5] := (rA_Mat[5,1] * a_x_hat[1]) + (rA_Mat[5,2] * a_x_hat[2]) + (rA_Mat[5,3] * a_x_hat[3]) + (rA_Mat[5,4] * a_x_hat[4]) + (rA_Mat[5,5] * a_x_hat[5]) + (rA_Mat[5,6] * a_x_hat[6]) + (rB_Mat[5,1] * rU_Opt_Seq[1,1]) + (rB_Mat[5,2] * rU_Opt_Seq[1,2]) + (rB_Mat[5,3] * rU_Opt_Seq[1,3]) + (rB_Mat[5,4] * rU_Opt_Seq[1,4]) + (rB_Mat[5,5] * rU_Opt_Seq[1,5]);
rX_Pred_Horizon[1, 6] := (rA_Mat[6,1] * a_x_hat[1]) + (rA_Mat[6,2] * a_x_hat[2]) + (rA_Mat[6,3] * a_x_hat[3]) + (rA_Mat[6,4] * a_x_hat[4]) + (rA_Mat[6,5] * a_x_hat[5]) + (rA_Mat[6,6] * a_x_hat[6]) + (rB_Mat[6,1] * rU_Opt_Seq[1,1]) + (rB_Mat[6,2] * rU_Opt_Seq[1,2]) + (rB_Mat[6,3] * rU_Opt_Seq[1,3]) + (rB_Mat[6,4] * rU_Opt_Seq[1,4]) + (rB_Mat[6,5] * rU_Opt_Seq[1,5]);

(* Iteration 3 - Forward State Prediction Step 2 (h=2): x_2 = A * x_1 + B * u_2 *)
rX_Pred_Horizon[2, 1] := (rA_Mat[1,1] * rX_Pred_Horizon[1,1]) + (rA_Mat[1,2] * rX_Pred_Horizon[1,2]) + (rA_Mat[1,3] * rX_Pred_Horizon[1,3]) + (rA_Mat[1,4] * rX_Pred_Horizon[1,4]) + (rA_Mat[1,5] * rX_Pred_Horizon[1,5]) + (rA_Mat[1,6] * rX_Pred_Horizon[1,6]) + (rB_Mat[1,1] * rU_Opt_Seq[2,1]) + (rB_Mat[1,2] * rU_Opt_Seq[2,2]) + (rB_Mat[1,3] * rU_Opt_Seq[2,3]) + (rB_Mat[1,4] * rU_Opt_Seq[2,4]) + (rB_Mat[1,5] * rU_Opt_Seq[2,5]);
rX_Pred_Horizon[2, 2] := (rA_Mat[2,1] * rX_Pred_Horizon[1,1]) + (rA_Mat[2,2] * rX_Pred_Horizon[1,2]) + (rA_Mat[2,3] * rX_Pred_Horizon[1,3]) + (rA_Mat[2,4] * rX_Pred_Horizon[1,4]) + (rA_Mat[2,5] * rX_Pred_Horizon[1,5]) + (rA_Mat[2,6] * rX_Pred_Horizon[1,6]) + (rB_Mat[2,1] * rU_Opt_Seq[2,1]) + (rB_Mat[2,2] * rU_Opt_Seq[2,2]) + (rB_Mat[2,3] * rU_Opt_Seq[2,3]) + (rB_Mat[2,4] * rU_Opt_Seq[2,4]) + (rB_Mat[2,5] * rU_Opt_Seq[2,5]);
rX_Pred_Horizon[2, 3] := (rA_Mat[3,1] * rX_Pred_Horizon[1,1]) + (rA_Mat[3,2] * rX_Pred_Horizon[1,2]) + (rA_Mat[3,3] * rX_Pred_Horizon[1,3]) + (rA_Mat[3,4] * rX_Pred_Horizon[1,4]) + (rA_Mat[3,5] * rX_Pred_Horizon[1,5]) + (rA_Mat[3,6] * rX_Pred_Horizon[1,6]) + (rB_Mat[3,1] * rU_Opt_Seq[2,1]) + (rB_Mat[3,2] * rU_Opt_Seq[2,2]) + (rB_Mat[3,3] * rU_Opt_Seq[2,3]) + (rB_Mat[3,4] * rU_Opt_Seq[2,4]) + (rB_Mat[3,5] * rU_Opt_Seq[2,5]);
rX_Pred_Horizon[2, 4] := (rA_Mat[4,1] * rX_Pred_Horizon[1,1]) + (rA_Mat[4,2] * rX_Pred_Horizon[1,2]) + (rA_Mat[4,3] * rX_Pred_Horizon[1,3]) + (rA_Mat[4,4] * rX_Pred_Horizon[1,4]) + (rA_Mat[4,5] * rX_Pred_Horizon[1,5]) + (rA_Mat[4,6] * rX_Pred_Horizon[1,6]) + (rB_Mat[4,1] * rU_Opt_Seq[2,1]) + (rB_Mat[4,2] * rU_Opt_Seq[2,2]) + (rB_Mat[4,3] * rU_Opt_Seq[2,3]) + (rB_Mat[4,4] * rU_Opt_Seq[2,4]) + (rB_Mat[4,5] * rU_Opt_Seq[2,5]);
rX_Pred_Horizon[2, 5] := (rA_Mat[5,1] * rX_Pred_Horizon[1,1]) + (rA_Mat[5,2] * rX_Pred_Horizon[1,2]) + (rA_Mat[5,3] * rX_Pred_Horizon[1,3]) + (rA_Mat[5,4] * rX_Pred_Horizon[1,4]) + (rA_Mat[5,5] * rX_Pred_Horizon[1,5]) + (rA_Mat[5,6] * rX_Pred_Horizon[1,6]) + (rB_Mat[5,1] * rU_Opt_Seq[2,1]) + (rB_Mat[5,2] * rU_Opt_Seq[2,2]) + (rB_Mat[5,3] * rU_Opt_Seq[2,3]) + (rB_Mat[5,4] * rU_Opt_Seq[2,4]) + (rB_Mat[5,5] * rU_Opt_Seq[2,5]);
rX_Pred_Horizon[2, 6] := (rA_Mat[6,1] * rX_Pred_Horizon[1,1]) + (rA_Mat[6,2] * rX_Pred_Horizon[1,2]) + (rA_Mat[6,3] * rX_Pred_Horizon[1,3]) + (rA_Mat[6,4] * rX_Pred_Horizon[1,4]) + (rA_Mat[6,5] * rX_Pred_Horizon[1,5]) + (rA_Mat[6,6] * rX_Pred_Horizon[1,6]) + (rB_Mat[6,1] * rU_Opt_Seq[2,1]) + (rB_Mat[6,2] * rU_Opt_Seq[2,2]) + (rB_Mat[6,3] * rU_Opt_Seq[2,3]) + (rB_Mat[6,4] * rU_Opt_Seq[2,4]) + (rB_Mat[6,5] * rU_Opt_Seq[2,5]);

(* Iteration 3 - Forward State Prediction Step 3 (h=3): x_3 = A * x_2 + B * u_3 *)
rX_Pred_Horizon[3, 1] := (rA_Mat[1,1] * rX_Pred_Horizon[2,1]) + (rA_Mat[1,2] * rX_Pred_Horizon[2,2]) + (rA_Mat[1,3] * rX_Pred_Horizon[2,3]) + (rA_Mat[1,4] * rX_Pred_Horizon[2,4]) + (rA_Mat[1,5] * rX_Pred_Horizon[2,5]) + (rA_Mat[1,6] * rX_Pred_Horizon[2,6]) + (rB_Mat[1,1] * rU_Opt_Seq[3,1]) + (rB_Mat[1,2] * rU_Opt_Seq[3,2]) + (rB_Mat[1,3] * rU_Opt_Seq[3,3]) + (rB_Mat[1,4] * rU_Opt_Seq[3,4]) + (rB_Mat[1,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[3, 2] := (rA_Mat[2,1] * rX_Pred_Horizon[2,1]) + (rA_Mat[2,2] * rX_Pred_Horizon[2,2]) + (rA_Mat[2,3] * rX_Pred_Horizon[2,3]) + (rA_Mat[2,4] * rX_Pred_Horizon[2,4]) + (rA_Mat[2,5] * rX_Pred_Horizon[2,5]) + (rA_Mat[2,6] * rX_Pred_Horizon[2,6]) + (rB_Mat[2,1] * rU_Opt_Seq[3,1]) + (rB_Mat[2,2] * rU_Opt_Seq[3,2]) + (rB_Mat[2,3] * rU_Opt_Seq[3,3]) + (rB_Mat[2,4] * rU_Opt_Seq[3,4]) + (rB_Mat[2,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[3, 3] := (rA_Mat[3,1] * rX_Pred_Horizon[2,1]) + (rA_Mat[3,2] * rX_Pred_Horizon[2,2]) + (rA_Mat[3,3] * rX_Pred_Horizon[2,3]) + (rA_Mat[3,4] * rX_Pred_Horizon[2,4]) + (rA_Mat[3,5] * rX_Pred_Horizon[2,5]) + (rA_Mat[3,6] * rX_Pred_Horizon[2,6]) + (rB_Mat[3,1] * rU_Opt_Seq[3,1]) + (rB_Mat[3,2] * rU_Opt_Seq[3,2]) + (rB_Mat[3,3] * rU_Opt_Seq[3,3]) + (rB_Mat[3,4] * rU_Opt_Seq[3,4]) + (rB_Mat[3,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[3, 4] := (rA_Mat[4,1] * rX_Pred_Horizon[2,1]) + (rA_Mat[4,2] * rX_Pred_Horizon[2,2]) + (rA_Mat[4,3] * rX_Pred_Horizon[2,3]) + (rA_Mat[4,4] * rX_Pred_Horizon[2,4]) + (rA_Mat[4,5] * rX_Pred_Horizon[2,5]) + (rA_Mat[4,6] * rX_Pred_Horizon[2,6]) + (rB_Mat[4,1] * rU_Opt_Seq[3,1]) + (rB_Mat[4,2] * rU_Opt_Seq[3,2]) + (rB_Mat[4,3] * rU_Opt_Seq[3,3]) + (rB_Mat[4,4] * rU_Opt_Seq[3,4]) + (rB_Mat[4,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[3, 5] := (rA_Mat[5,1] * rX_Pred_Horizon[2,1]) + (rA_Mat[5,2] * rX_Pred_Horizon[2,2]) + (rA_Mat[5,3] * rX_Pred_Horizon[2,3]) + (rA_Mat[5,4] * rX_Pred_Horizon[2,4]) + (rA_Mat[5,5] * rX_Pred_Horizon[2,5]) + (rA_Mat[5,6] * rX_Pred_Horizon[2,6]) + (rB_Mat[5,1] * rU_Opt_Seq[3,1]) + (rB_Mat[5,2] * rU_Opt_Seq[3,2]) + (rB_Mat[5,3] * rU_Opt_Seq[3,3]) + (rB_Mat[5,4] * rU_Opt_Seq[3,4]) + (rB_Mat[5,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[3, 6] := (rA_Mat[6,1] * rX_Pred_Horizon[2,1]) + (rA_Mat[6,2] * rX_Pred_Horizon[2,2]) + (rA_Mat[6,3] * rX_Pred_Horizon[2,3]) + (rA_Mat[6,4] * rX_Pred_Horizon[2,4]) + (rA_Mat[6,5] * rX_Pred_Horizon[2,5]) + (rA_Mat[6,6] * rX_Pred_Horizon[2,6]) + (rB_Mat[6,1] * rU_Opt_Seq[3,1]) + (rB_Mat[6,2] * rU_Opt_Seq[3,2]) + (rB_Mat[6,3] * rU_Opt_Seq[3,3]) + (rB_Mat[6,4] * rU_Opt_Seq[3,4]) + (rB_Mat[6,5] * rU_Opt_Seq[3,5]);

(* Iteration 3 - Forward State Prediction Step 4 (h=4): x_4 = A * x_3 + B * u_3 (held beyond Hu) *)
rX_Pred_Horizon[4, 1] := (rA_Mat[1,1] * rX_Pred_Horizon[3,1]) + (rA_Mat[1,2] * rX_Pred_Horizon[3,2]) + (rA_Mat[1,3] * rX_Pred_Horizon[3,3]) + (rA_Mat[1,4] * rX_Pred_Horizon[3,4]) + (rA_Mat[1,5] * rX_Pred_Horizon[3,5]) + (rA_Mat[1,6] * rX_Pred_Horizon[3,6]) + (rB_Mat[1,1] * rU_Opt_Seq[3,1]) + (rB_Mat[1,2] * rU_Opt_Seq[3,2]) + (rB_Mat[1,3] * rU_Opt_Seq[3,3]) + (rB_Mat[1,4] * rU_Opt_Seq[3,4]) + (rB_Mat[1,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[4, 2] := (rA_Mat[2,1] * rX_Pred_Horizon[3,1]) + (rA_Mat[2,2] * rX_Pred_Horizon[3,2]) + (rA_Mat[2,3] * rX_Pred_Horizon[3,3]) + (rA_Mat[2,4] * rX_Pred_Horizon[3,4]) + (rA_Mat[2,5] * rX_Pred_Horizon[3,5]) + (rA_Mat[2,6] * rX_Pred_Horizon[3,6]) + (rB_Mat[2,1] * rU_Opt_Seq[3,1]) + (rB_Mat[2,2] * rU_Opt_Seq[3,2]) + (rB_Mat[2,3] * rU_Opt_Seq[3,3]) + (rB_Mat[2,4] * rU_Opt_Seq[3,4]) + (rB_Mat[2,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[4, 3] := (rA_Mat[3,1] * rX_Pred_Horizon[3,1]) + (rA_Mat[3,2] * rX_Pred_Horizon[3,2]) + (rA_Mat[3,3] * rX_Pred_Horizon[3,3]) + (rA_Mat[3,4] * rX_Pred_Horizon[3,4]) + (rA_Mat[3,5] * rX_Pred_Horizon[3,5]) + (rA_Mat[3,6] * rX_Pred_Horizon[3,6]) + (rB_Mat[3,1] * rU_Opt_Seq[3,1]) + (rB_Mat[3,2] * rU_Opt_Seq[3,2]) + (rB_Mat[3,3] * rU_Opt_Seq[3,3]) + (rB_Mat[3,4] * rU_Opt_Seq[3,4]) + (rB_Mat[3,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[4, 4] := (rA_Mat[4,1] * rX_Pred_Horizon[3,1]) + (rA_Mat[4,2] * rX_Pred_Horizon[3,2]) + (rA_Mat[4,3] * rX_Pred_Horizon[3,3]) + (rA_Mat[4,4] * rX_Pred_Horizon[3,4]) + (rA_Mat[4,5] * rX_Pred_Horizon[3,5]) + (rA_Mat[4,6] * rX_Pred_Horizon[3,6]) + (rB_Mat[4,1] * rU_Opt_Seq[3,1]) + (rB_Mat[4,2] * rU_Opt_Seq[3,2]) + (rB_Mat[4,3] * rU_Opt_Seq[3,3]) + (rB_Mat[4,4] * rU_Opt_Seq[3,4]) + (rB_Mat[4,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[4, 5] := (rA_Mat[5,1] * rX_Pred_Horizon[3,1]) + (rA_Mat[5,2] * rX_Pred_Horizon[3,2]) + (rA_Mat[5,3] * rX_Pred_Horizon[3,3]) + (rA_Mat[5,4] * rX_Pred_Horizon[3,4]) + (rA_Mat[5,5] * rX_Pred_Horizon[3,5]) + (rA_Mat[5,6] * rX_Pred_Horizon[3,6]) + (rB_Mat[5,1] * rU_Opt_Seq[3,1]) + (rB_Mat[5,2] * rU_Opt_Seq[3,2]) + (rB_Mat[5,3] * rU_Opt_Seq[3,3]) + (rB_Mat[5,4] * rU_Opt_Seq[3,4]) + (rB_Mat[5,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[4, 6] := (rA_Mat[6,1] * rX_Pred_Horizon[3,1]) + (rA_Mat[6,2] * rX_Pred_Horizon[3,2]) + (rA_Mat[6,3] * rX_Pred_Horizon[3,3]) + (rA_Mat[6,4] * rX_Pred_Horizon[3,4]) + (rA_Mat[6,5] * rX_Pred_Horizon[3,5]) + (rA_Mat[6,6] * rX_Pred_Horizon[3,6]) + (rB_Mat[6,1] * rU_Opt_Seq[3,1]) + (rB_Mat[6,2] * rU_Opt_Seq[3,2]) + (rB_Mat[6,3] * rU_Opt_Seq[3,3]) + (rB_Mat[6,4] * rU_Opt_Seq[3,4]) + (rB_Mat[6,5] * rU_Opt_Seq[3,5]);

(* Iteration 3 - Forward State Prediction Step 5 (h=5): x_5 = A * x_4 + B * u_3 (held beyond Hu) *)
rX_Pred_Horizon[5, 1] := (rA_Mat[1,1] * rX_Pred_Horizon[4,1]) + (rA_Mat[1,2] * rX_Pred_Horizon[4,2]) + (rA_Mat[1,3] * rX_Pred_Horizon[4,3]) + (rA_Mat[1,4] * rX_Pred_Horizon[4,4]) + (rA_Mat[1,5] * rX_Pred_Horizon[4,5]) + (rA_Mat[1,6] * rX_Pred_Horizon[4,6]) + (rB_Mat[1,1] * rU_Opt_Seq[3,1]) + (rB_Mat[1,2] * rU_Opt_Seq[3,2]) + (rB_Mat[1,3] * rU_Opt_Seq[3,3]) + (rB_Mat[1,4] * rU_Opt_Seq[3,4]) + (rB_Mat[1,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[5, 2] := (rA_Mat[2,1] * rX_Pred_Horizon[4,1]) + (rA_Mat[2,2] * rX_Pred_Horizon[4,2]) + (rA_Mat[2,3] * rX_Pred_Horizon[4,3]) + (rA_Mat[2,4] * rX_Pred_Horizon[4,4]) + (rA_Mat[2,5] * rX_Pred_Horizon[4,5]) + (rA_Mat[2,6] * rX_Pred_Horizon[4,6]) + (rB_Mat[2,1] * rU_Opt_Seq[3,1]) + (rB_Mat[2,2] * rU_Opt_Seq[3,2]) + (rB_Mat[2,3] * rU_Opt_Seq[3,3]) + (rB_Mat[2,4] * rU_Opt_Seq[3,4]) + (rB_Mat[2,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[5, 3] := (rA_Mat[3,1] * rX_Pred_Horizon[4,1]) + (rA_Mat[3,2] * rX_Pred_Horizon[4,2]) + (rA_Mat[3,3] * rX_Pred_Horizon[4,3]) + (rA_Mat[3,4] * rX_Pred_Horizon[4,4]) + (rA_Mat[3,5] * rX_Pred_Horizon[4,5]) + (rA_Mat[3,6] * rX_Pred_Horizon[4,6]) + (rB_Mat[3,1] * rU_Opt_Seq[3,1]) + (rB_Mat[3,2] * rU_Opt_Seq[3,2]) + (rB_Mat[3,3] * rU_Opt_Seq[3,3]) + (rB_Mat[3,4] * rU_Opt_Seq[3,4]) + (rB_Mat[3,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[5, 4] := (rA_Mat[4,1] * rX_Pred_Horizon[4,1]) + (rA_Mat[4,2] * rX_Pred_Horizon[4,2]) + (rA_Mat[4,3] * rX_Pred_Horizon[4,3]) + (rA_Mat[4,4] * rX_Pred_Horizon[4,4]) + (rA_Mat[4,5] * rX_Pred_Horizon[4,5]) + (rA_Mat[4,6] * rX_Pred_Horizon[4,6]) + (rB_Mat[4,1] * rU_Opt_Seq[3,1]) + (rB_Mat[4,2] * rU_Opt_Seq[3,2]) + (rB_Mat[4,3] * rU_Opt_Seq[3,3]) + (rB_Mat[4,4] * rU_Opt_Seq[3,4]) + (rB_Mat[4,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[5, 5] := (rA_Mat[5,1] * rX_Pred_Horizon[4,1]) + (rA_Mat[5,2] * rX_Pred_Horizon[4,2]) + (rA_Mat[5,3] * rX_Pred_Horizon[4,3]) + (rA_Mat[5,4] * rX_Pred_Horizon[4,4]) + (rA_Mat[5,5] * rX_Pred_Horizon[4,5]) + (rA_Mat[5,6] * rX_Pred_Horizon[4,6]) + (rB_Mat[5,1] * rU_Opt_Seq[3,1]) + (rB_Mat[5,2] * rU_Opt_Seq[3,2]) + (rB_Mat[5,3] * rU_Opt_Seq[3,3]) + (rB_Mat[5,4] * rU_Opt_Seq[3,4]) + (rB_Mat[5,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[5, 6] := (rA_Mat[6,1] * rX_Pred_Horizon[4,1]) + (rA_Mat[6,2] * rX_Pred_Horizon[4,2]) + (rA_Mat[6,3] * rX_Pred_Horizon[4,3]) + (rA_Mat[6,4] * rX_Pred_Horizon[4,4]) + (rA_Mat[6,5] * rX_Pred_Horizon[4,5]) + (rA_Mat[6,6] * rX_Pred_Horizon[4,6]) + (rB_Mat[6,1] * rU_Opt_Seq[3,1]) + (rB_Mat[6,2] * rU_Opt_Seq[3,2]) + (rB_Mat[6,3] * rU_Opt_Seq[3,3]) + (rB_Mat[6,4] * rU_Opt_Seq[3,4]) + (rB_Mat[6,5] * rU_Opt_Seq[3,5]);

(* Iteration 3 - Evaluate Objective Function Cost J *)
rMPC_Cost_J := 0.0;
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[1] * (rX_Pred_Horizon[1,1] - rX_Target[1,1]) * (rX_Pred_Horizon[1,1] - rX_Target[1,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[2] * (rX_Pred_Horizon[1,2] - rX_Target[1,2]) * (rX_Pred_Horizon[1,2] - rX_Target[1,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[3] * (rX_Pred_Horizon[1,3] - rX_Target[1,3]) * (rX_Pred_Horizon[1,3] - rX_Target[1,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[4] * (rX_Pred_Horizon[1,4] - rX_Target[1,4]) * (rX_Pred_Horizon[1,4] - rX_Target[1,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[5] * (rX_Pred_Horizon[1,5] - rX_Target[1,5]) * (rX_Pred_Horizon[1,5] - rX_Target[1,5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[6] * (rX_Pred_Horizon[1,6] - rX_Target[1,6]) * (rX_Pred_Horizon[1,6] - rX_Target[1,6]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[1] * (rX_Pred_Horizon[2,1] - rX_Target[2,1]) * (rX_Pred_Horizon[2,1] - rX_Target[2,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[2] * (rX_Pred_Horizon[2,2] - rX_Target[2,2]) * (rX_Pred_Horizon[2,2] - rX_Target[2,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[3] * (rX_Pred_Horizon[2,3] - rX_Target[2,3]) * (rX_Pred_Horizon[2,3] - rX_Target[2,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[4] * (rX_Pred_Horizon[2,4] - rX_Target[2,4]) * (rX_Pred_Horizon[2,4] - rX_Target[2,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[5] * (rX_Pred_Horizon[2,5] - rX_Target[2,5]) * (rX_Pred_Horizon[2,5] - rX_Target[2,5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[6] * (rX_Pred_Horizon[2,6] - rX_Target[2,6]) * (rX_Pred_Horizon[2,6] - rX_Target[2,6]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[1] * (rX_Pred_Horizon[3,1] - rX_Target[3,1]) * (rX_Pred_Horizon[3,1] - rX_Target[3,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[2] * (rX_Pred_Horizon[3,2] - rX_Target[3,2]) * (rX_Pred_Horizon[3,2] - rX_Target[3,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[3] * (rX_Pred_Horizon[3,3] - rX_Target[3,3]) * (rX_Pred_Horizon[3,3] - rX_Target[3,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[4] * (rX_Pred_Horizon[3,4] - rX_Target[3,4]) * (rX_Pred_Horizon[3,4] - rX_Target[3,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[5] * (rX_Pred_Horizon[3,5] - rX_Target[3,5]) * (rX_Pred_Horizon[3,5] - rX_Target[3,5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[6] * (rX_Pred_Horizon[3,6] - rX_Target[3,6]) * (rX_Pred_Horizon[3,6] - rX_Target[3,6]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[1] * (rX_Pred_Horizon[4,1] - rX_Target[4,1]) * (rX_Pred_Horizon[4,1] - rX_Target[4,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[2] * (rX_Pred_Horizon[4,2] - rX_Target[4,2]) * (rX_Pred_Horizon[4,2] - rX_Target[4,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[3] * (rX_Pred_Horizon[4,3] - rX_Target[4,3]) * (rX_Pred_Horizon[4,3] - rX_Target[4,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[4] * (rX_Pred_Horizon[4,4] - rX_Target[4,4]) * (rX_Pred_Horizon[4,4] - rX_Target[4,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[5] * (rX_Pred_Horizon[4,5] - rX_Target[4,5]) * (rX_Pred_Horizon[4,5] - rX_Target[4,5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[6] * (rX_Pred_Horizon[4,6] - rX_Target[4,6]) * (rX_Pred_Horizon[4,6] - rX_Target[4,6]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[1] * (rX_Pred_Horizon[5,1] - rX_Target[5,1]) * (rX_Pred_Horizon[5,1] - rX_Target[5,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[2] * (rX_Pred_Horizon[5,2] - rX_Target[5,2]) * (rX_Pred_Horizon[5,2] - rX_Target[5,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[3] * (rX_Pred_Horizon[5,3] - rX_Target[5,3]) * (rX_Pred_Horizon[5,3] - rX_Target[5,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[4] * (rX_Pred_Horizon[5,4] - rX_Target[5,4]) * (rX_Pred_Horizon[5,4] - rX_Target[5,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[5] * (rX_Pred_Horizon[5,5] - rX_Target[5,5]) * (rX_Pred_Horizon[5,5] - rX_Target[5,5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[6] * (rX_Pred_Horizon[5,6] - rX_Target[5,6]) * (rX_Pred_Horizon[5,6] - rX_Target[5,6]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rP_Diag[1] * (rX_Pred_Horizon[5,1] - rX_Target[5,1]) * (rX_Pred_Horizon[5,1] - rX_Target[5,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rP_Diag[2] * (rX_Pred_Horizon[5,2] - rX_Target[5,2]) * (rX_Pred_Horizon[5,2] - rX_Target[5,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rP_Diag[3] * (rX_Pred_Horizon[5,3] - rX_Target[5,3]) * (rX_Pred_Horizon[5,3] - rX_Target[5,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rP_Diag[4] * (rX_Pred_Horizon[5,4] - rX_Target[5,4]) * (rX_Pred_Horizon[5,4] - rX_Target[5,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rP_Diag[5] * (rX_Pred_Horizon[5,5] - rX_Target[5,5]) * (rX_Pred_Horizon[5,5] - rX_Target[5,5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rP_Diag[6] * (rX_Pred_Horizon[5,6] - rX_Target[5,6]) * (rX_Pred_Horizon[5,6] - rX_Target[5,6]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[1] * rU_Opt_Seq[1,1] * rU_Opt_Seq[1,1]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[2] * rU_Opt_Seq[1,2] * rU_Opt_Seq[1,2]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[3] * rU_Opt_Seq[1,3] * rU_Opt_Seq[1,3]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[4] * rU_Opt_Seq[1,4] * rU_Opt_Seq[1,4]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[5] * rU_Opt_Seq[1,5] * rU_Opt_Seq[1,5]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[1] * rU_Opt_Seq[2,1] * rU_Opt_Seq[2,1]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[2] * rU_Opt_Seq[2,2] * rU_Opt_Seq[2,2]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[3] * rU_Opt_Seq[2,3] * rU_Opt_Seq[2,3]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[4] * rU_Opt_Seq[2,4] * rU_Opt_Seq[2,4]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[5] * rU_Opt_Seq[2,5] * rU_Opt_Seq[2,5]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[1] * rU_Opt_Seq[3,1] * rU_Opt_Seq[3,1]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[2] * rU_Opt_Seq[3,2] * rU_Opt_Seq[3,2]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[3] * rU_Opt_Seq[3,3] * rU_Opt_Seq[3,3]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[4] * rU_Opt_Seq[3,4] * rU_Opt_Seq[3,4]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[5] * rU_Opt_Seq[3,5] * rU_Opt_Seq[3,5]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[1] * (rU_Opt_Seq[1,1] - a_u_prev[1]) * (rU_Opt_Seq[1,1] - a_u_prev[1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[1] * (rU_Opt_Seq[2,1] - rU_Opt_Seq[1,1]) * (rU_Opt_Seq[2,1] - rU_Opt_Seq[1,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[1] * (rU_Opt_Seq[3,1] - rU_Opt_Seq[2,1]) * (rU_Opt_Seq[3,1] - rU_Opt_Seq[2,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[2] * (rU_Opt_Seq[1,2] - a_u_prev[2]) * (rU_Opt_Seq[1,2] - a_u_prev[2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[2] * (rU_Opt_Seq[2,2] - rU_Opt_Seq[1,2]) * (rU_Opt_Seq[2,2] - rU_Opt_Seq[1,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[2] * (rU_Opt_Seq[3,2] - rU_Opt_Seq[2,2]) * (rU_Opt_Seq[3,2] - rU_Opt_Seq[2,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[3] * (rU_Opt_Seq[1,3] - a_u_prev[3]) * (rU_Opt_Seq[1,3] - a_u_prev[3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[3] * (rU_Opt_Seq[2,3] - rU_Opt_Seq[1,3]) * (rU_Opt_Seq[2,3] - rU_Opt_Seq[1,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[3] * (rU_Opt_Seq[3,3] - rU_Opt_Seq[2,3]) * (rU_Opt_Seq[3,3] - rU_Opt_Seq[2,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[4] * (rU_Opt_Seq[1,4] - a_u_prev[4]) * (rU_Opt_Seq[1,4] - a_u_prev[4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[4] * (rU_Opt_Seq[2,4] - rU_Opt_Seq[1,4]) * (rU_Opt_Seq[2,4] - rU_Opt_Seq[1,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[4] * (rU_Opt_Seq[3,4] - rU_Opt_Seq[2,4]) * (rU_Opt_Seq[3,4] - rU_Opt_Seq[2,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[5] * (rU_Opt_Seq[1,5] - a_u_prev[5]) * (rU_Opt_Seq[1,5] - a_u_prev[5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[5] * (rU_Opt_Seq[2,5] - rU_Opt_Seq[1,5]) * (rU_Opt_Seq[2,5] - rU_Opt_Seq[1,5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[5] * (rU_Opt_Seq[3,5] - rU_Opt_Seq[2,5]) * (rU_Opt_Seq[3,5] - rU_Opt_Seq[2,5]));

(* Iteration 3 - Backward Adjoint Costate Propagation: lambda_h = A^T * lambda_{h+1} + Q * (x_h - x_ref) *)
(* Terminal Costate at h=5: lambda_5 = (P + Q) * (x_5 - x_target_5) *)
rLambda_Costate[5, 1] := (rP_Diag[1] + rQ_Diag[1]) * (rX_Pred_Horizon[5,1] - rX_Target[5,1]);
rLambda_Costate[5, 2] := (rP_Diag[2] + rQ_Diag[2]) * (rX_Pred_Horizon[5,2] - rX_Target[5,2]);
rLambda_Costate[5, 3] := (rP_Diag[3] + rQ_Diag[3]) * (rX_Pred_Horizon[5,3] - rX_Target[5,3]);
rLambda_Costate[5, 4] := (rP_Diag[4] + rQ_Diag[4]) * (rX_Pred_Horizon[5,4] - rX_Target[5,4]);
rLambda_Costate[5, 5] := (rP_Diag[5] + rQ_Diag[5]) * (rX_Pred_Horizon[5,5] - rX_Target[5,5]);
rLambda_Costate[5, 6] := (rP_Diag[6] + rQ_Diag[6]) * (rX_Pred_Horizon[5,6] - rX_Target[5,6]);

(* Adjoint Costate at h=4: lambda_4 = A^T * lambda_5 + Q * (x_4 - x_target_4) *)
rLambda_Costate[4, 1] := (rA_Mat[1,1] * rLambda_Costate[5,1]) + (rA_Mat[2,1] * rLambda_Costate[5,2]) + (rA_Mat[3,1] * rLambda_Costate[5,3]) + (rA_Mat[4,1] * rLambda_Costate[5,4]) + (rA_Mat[5,1] * rLambda_Costate[5,5]) + (rA_Mat[6,1] * rLambda_Costate[5,6]) + (rQ_Diag[1] * (rX_Pred_Horizon[4,1] - rX_Target[4,1]));
rLambda_Costate[4, 2] := (rA_Mat[1,2] * rLambda_Costate[5,1]) + (rA_Mat[2,2] * rLambda_Costate[5,2]) + (rA_Mat[3,2] * rLambda_Costate[5,3]) + (rA_Mat[4,2] * rLambda_Costate[5,4]) + (rA_Mat[5,2] * rLambda_Costate[5,5]) + (rA_Mat[6,2] * rLambda_Costate[5,6]) + (rQ_Diag[2] * (rX_Pred_Horizon[4,2] - rX_Target[4,2]));
rLambda_Costate[4, 3] := (rA_Mat[1,3] * rLambda_Costate[5,1]) + (rA_Mat[2,3] * rLambda_Costate[5,2]) + (rA_Mat[3,3] * rLambda_Costate[5,3]) + (rA_Mat[4,3] * rLambda_Costate[5,4]) + (rA_Mat[5,3] * rLambda_Costate[5,5]) + (rA_Mat[6,3] * rLambda_Costate[5,6]) + (rQ_Diag[3] * (rX_Pred_Horizon[4,3] - rX_Target[4,3]));
rLambda_Costate[4, 4] := (rA_Mat[1,4] * rLambda_Costate[5,1]) + (rA_Mat[2,4] * rLambda_Costate[5,2]) + (rA_Mat[3,4] * rLambda_Costate[5,3]) + (rA_Mat[4,4] * rLambda_Costate[5,4]) + (rA_Mat[5,4] * rLambda_Costate[5,5]) + (rA_Mat[6,4] * rLambda_Costate[5,6]) + (rQ_Diag[4] * (rX_Pred_Horizon[4,4] - rX_Target[4,4]));
rLambda_Costate[4, 5] := (rA_Mat[1,5] * rLambda_Costate[5,1]) + (rA_Mat[2,5] * rLambda_Costate[5,2]) + (rA_Mat[3,5] * rLambda_Costate[5,3]) + (rA_Mat[4,5] * rLambda_Costate[5,4]) + (rA_Mat[5,5] * rLambda_Costate[5,5]) + (rA_Mat[6,5] * rLambda_Costate[5,6]) + (rQ_Diag[5] * (rX_Pred_Horizon[4,5] - rX_Target[4,5]));
rLambda_Costate[4, 6] := (rA_Mat[1,6] * rLambda_Costate[5,1]) + (rA_Mat[2,6] * rLambda_Costate[5,2]) + (rA_Mat[3,6] * rLambda_Costate[5,3]) + (rA_Mat[4,6] * rLambda_Costate[5,4]) + (rA_Mat[5,6] * rLambda_Costate[5,5]) + (rA_Mat[6,6] * rLambda_Costate[5,6]) + (rQ_Diag[6] * (rX_Pred_Horizon[4,6] - rX_Target[4,6]));

(* Adjoint Costate at h=3: lambda_3 = A^T * lambda_4 + Q * (x_3 - x_target_3) *)
rLambda_Costate[3, 1] := (rA_Mat[1,1] * rLambda_Costate[4,1]) + (rA_Mat[2,1] * rLambda_Costate[4,2]) + (rA_Mat[3,1] * rLambda_Costate[4,3]) + (rA_Mat[4,1] * rLambda_Costate[4,4]) + (rA_Mat[5,1] * rLambda_Costate[4,5]) + (rA_Mat[6,1] * rLambda_Costate[4,6]) + (rQ_Diag[1] * (rX_Pred_Horizon[3,1] - rX_Target[3,1]));
rLambda_Costate[3, 2] := (rA_Mat[1,2] * rLambda_Costate[4,1]) + (rA_Mat[2,2] * rLambda_Costate[4,2]) + (rA_Mat[3,2] * rLambda_Costate[4,3]) + (rA_Mat[4,2] * rLambda_Costate[4,4]) + (rA_Mat[5,2] * rLambda_Costate[4,5]) + (rA_Mat[6,2] * rLambda_Costate[4,6]) + (rQ_Diag[2] * (rX_Pred_Horizon[3,2] - rX_Target[3,2]));
rLambda_Costate[3, 3] := (rA_Mat[1,3] * rLambda_Costate[4,1]) + (rA_Mat[2,3] * rLambda_Costate[4,2]) + (rA_Mat[3,3] * rLambda_Costate[4,3]) + (rA_Mat[4,3] * rLambda_Costate[4,4]) + (rA_Mat[5,3] * rLambda_Costate[4,5]) + (rA_Mat[6,3] * rLambda_Costate[4,6]) + (rQ_Diag[3] * (rX_Pred_Horizon[3,3] - rX_Target[3,3]));
rLambda_Costate[3, 4] := (rA_Mat[1,4] * rLambda_Costate[4,1]) + (rA_Mat[2,4] * rLambda_Costate[4,2]) + (rA_Mat[3,4] * rLambda_Costate[4,3]) + (rA_Mat[4,4] * rLambda_Costate[4,4]) + (rA_Mat[5,4] * rLambda_Costate[4,5]) + (rA_Mat[6,4] * rLambda_Costate[4,6]) + (rQ_Diag[4] * (rX_Pred_Horizon[3,4] - rX_Target[3,4]));
rLambda_Costate[3, 5] := (rA_Mat[1,5] * rLambda_Costate[4,1]) + (rA_Mat[2,5] * rLambda_Costate[4,2]) + (rA_Mat[3,5] * rLambda_Costate[4,3]) + (rA_Mat[4,5] * rLambda_Costate[4,4]) + (rA_Mat[5,5] * rLambda_Costate[4,5]) + (rA_Mat[6,5] * rLambda_Costate[4,6]) + (rQ_Diag[5] * (rX_Pred_Horizon[3,5] - rX_Target[3,5]));
rLambda_Costate[3, 6] := (rA_Mat[1,6] * rLambda_Costate[4,1]) + (rA_Mat[2,6] * rLambda_Costate[4,2]) + (rA_Mat[3,6] * rLambda_Costate[4,3]) + (rA_Mat[4,6] * rLambda_Costate[4,4]) + (rA_Mat[5,6] * rLambda_Costate[4,5]) + (rA_Mat[6,6] * rLambda_Costate[4,6]) + (rQ_Diag[6] * (rX_Pred_Horizon[3,6] - rX_Target[3,6]));

(* Adjoint Costate at h=2: lambda_2 = A^T * lambda_3 + Q * (x_2 - x_target_2) *)
rLambda_Costate[2, 1] := (rA_Mat[1,1] * rLambda_Costate[3,1]) + (rA_Mat[2,1] * rLambda_Costate[3,2]) + (rA_Mat[3,1] * rLambda_Costate[3,3]) + (rA_Mat[4,1] * rLambda_Costate[3,4]) + (rA_Mat[5,1] * rLambda_Costate[3,5]) + (rA_Mat[6,1] * rLambda_Costate[3,6]) + (rQ_Diag[1] * (rX_Pred_Horizon[2,1] - rX_Target[2,1]));
rLambda_Costate[2, 2] := (rA_Mat[1,2] * rLambda_Costate[3,1]) + (rA_Mat[2,2] * rLambda_Costate[3,2]) + (rA_Mat[3,2] * rLambda_Costate[3,3]) + (rA_Mat[4,2] * rLambda_Costate[3,4]) + (rA_Mat[5,2] * rLambda_Costate[3,5]) + (rA_Mat[6,2] * rLambda_Costate[3,6]) + (rQ_Diag[2] * (rX_Pred_Horizon[2,2] - rX_Target[2,2]));
rLambda_Costate[2, 3] := (rA_Mat[1,3] * rLambda_Costate[3,1]) + (rA_Mat[2,3] * rLambda_Costate[3,2]) + (rA_Mat[3,3] * rLambda_Costate[3,3]) + (rA_Mat[4,3] * rLambda_Costate[3,4]) + (rA_Mat[5,3] * rLambda_Costate[3,5]) + (rA_Mat[6,3] * rLambda_Costate[3,6]) + (rQ_Diag[3] * (rX_Pred_Horizon[2,3] - rX_Target[2,3]));
rLambda_Costate[2, 4] := (rA_Mat[1,4] * rLambda_Costate[3,1]) + (rA_Mat[2,4] * rLambda_Costate[3,2]) + (rA_Mat[3,4] * rLambda_Costate[3,3]) + (rA_Mat[4,4] * rLambda_Costate[3,4]) + (rA_Mat[5,4] * rLambda_Costate[3,5]) + (rA_Mat[6,4] * rLambda_Costate[3,6]) + (rQ_Diag[4] * (rX_Pred_Horizon[2,4] - rX_Target[2,4]));
rLambda_Costate[2, 5] := (rA_Mat[1,5] * rLambda_Costate[3,1]) + (rA_Mat[2,5] * rLambda_Costate[3,2]) + (rA_Mat[3,5] * rLambda_Costate[3,3]) + (rA_Mat[4,5] * rLambda_Costate[3,4]) + (rA_Mat[5,5] * rLambda_Costate[3,5]) + (rA_Mat[6,5] * rLambda_Costate[3,6]) + (rQ_Diag[5] * (rX_Pred_Horizon[2,5] - rX_Target[2,5]));
rLambda_Costate[2, 6] := (rA_Mat[1,6] * rLambda_Costate[3,1]) + (rA_Mat[2,6] * rLambda_Costate[3,2]) + (rA_Mat[3,6] * rLambda_Costate[3,3]) + (rA_Mat[4,6] * rLambda_Costate[3,4]) + (rA_Mat[5,6] * rLambda_Costate[3,5]) + (rA_Mat[6,6] * rLambda_Costate[3,6]) + (rQ_Diag[6] * (rX_Pred_Horizon[2,6] - rX_Target[2,6]));

(* Adjoint Costate at h=1: lambda_1 = A^T * lambda_2 + Q * (x_1 - x_target_1) *)
rLambda_Costate[1, 1] := (rA_Mat[1,1] * rLambda_Costate[2,1]) + (rA_Mat[2,1] * rLambda_Costate[2,2]) + (rA_Mat[3,1] * rLambda_Costate[2,3]) + (rA_Mat[4,1] * rLambda_Costate[2,4]) + (rA_Mat[5,1] * rLambda_Costate[2,5]) + (rA_Mat[6,1] * rLambda_Costate[2,6]) + (rQ_Diag[1] * (rX_Pred_Horizon[1,1] - rX_Target[1,1]));
rLambda_Costate[1, 2] := (rA_Mat[1,2] * rLambda_Costate[2,1]) + (rA_Mat[2,2] * rLambda_Costate[2,2]) + (rA_Mat[3,2] * rLambda_Costate[2,3]) + (rA_Mat[4,2] * rLambda_Costate[2,4]) + (rA_Mat[5,2] * rLambda_Costate[2,5]) + (rA_Mat[6,2] * rLambda_Costate[2,6]) + (rQ_Diag[2] * (rX_Pred_Horizon[1,2] - rX_Target[1,2]));
rLambda_Costate[1, 3] := (rA_Mat[1,3] * rLambda_Costate[2,1]) + (rA_Mat[2,3] * rLambda_Costate[2,2]) + (rA_Mat[3,3] * rLambda_Costate[2,3]) + (rA_Mat[4,3] * rLambda_Costate[2,4]) + (rA_Mat[5,3] * rLambda_Costate[2,5]) + (rA_Mat[6,3] * rLambda_Costate[2,6]) + (rQ_Diag[3] * (rX_Pred_Horizon[1,3] - rX_Target[1,3]));
rLambda_Costate[1, 4] := (rA_Mat[1,4] * rLambda_Costate[2,1]) + (rA_Mat[2,4] * rLambda_Costate[2,2]) + (rA_Mat[3,4] * rLambda_Costate[2,3]) + (rA_Mat[4,4] * rLambda_Costate[2,4]) + (rA_Mat[5,4] * rLambda_Costate[2,5]) + (rA_Mat[6,4] * rLambda_Costate[2,6]) + (rQ_Diag[4] * (rX_Pred_Horizon[1,4] - rX_Target[1,4]));
rLambda_Costate[1, 5] := (rA_Mat[1,5] * rLambda_Costate[2,1]) + (rA_Mat[2,5] * rLambda_Costate[2,2]) + (rA_Mat[3,5] * rLambda_Costate[2,3]) + (rA_Mat[4,5] * rLambda_Costate[2,4]) + (rA_Mat[5,5] * rLambda_Costate[2,5]) + (rA_Mat[6,5] * rLambda_Costate[2,6]) + (rQ_Diag[5] * (rX_Pred_Horizon[1,5] - rX_Target[1,5]));
rLambda_Costate[1, 6] := (rA_Mat[1,6] * rLambda_Costate[2,1]) + (rA_Mat[2,6] * rLambda_Costate[2,2]) + (rA_Mat[3,6] * rLambda_Costate[2,3]) + (rA_Mat[4,6] * rLambda_Costate[2,4]) + (rA_Mat[5,6] * rLambda_Costate[2,5]) + (rA_Mat[6,6] * rLambda_Costate[2,6]) + (rQ_Diag[6] * (rX_Pred_Horizon[1,6] - rX_Target[1,6]));

(* Iteration 3 - Analytical Gradient Computation w.r.t. Control Inputs u_h *)
rMPC_GradNormSq := 0.0;
(* Gradient for u_1 (h=1) *)
rGrad_J[1, 1] := (rB_Mat[1,1] * rLambda_Costate[1,1]) + (rB_Mat[2,1] * rLambda_Costate[1,2]) + (rB_Mat[3,1] * rLambda_Costate[1,3]) + (rB_Mat[4,1] * rLambda_Costate[1,4]) + (rB_Mat[5,1] * rLambda_Costate[1,5]) + (rB_Mat[6,1] * rLambda_Costate[1,6]) + (rR_Diag[1] * rU_Opt_Seq[1,1]) + (rS_Diag[1] * (rU_Opt_Seq[1,1] - a_u_prev[1])) - (rS_Diag[1] * (rU_Opt_Seq[2,1] - rU_Opt_Seq[1,1]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[1, 1] * rGrad_J[1, 1]);
rGrad_J[1, 2] := (rB_Mat[1,2] * rLambda_Costate[1,1]) + (rB_Mat[2,2] * rLambda_Costate[1,2]) + (rB_Mat[3,2] * rLambda_Costate[1,3]) + (rB_Mat[4,2] * rLambda_Costate[1,4]) + (rB_Mat[5,2] * rLambda_Costate[1,5]) + (rB_Mat[6,2] * rLambda_Costate[1,6]) + (rR_Diag[2] * rU_Opt_Seq[1,2]) + (rS_Diag[2] * (rU_Opt_Seq[1,2] - a_u_prev[2])) - (rS_Diag[2] * (rU_Opt_Seq[2,2] - rU_Opt_Seq[1,2]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[1, 2] * rGrad_J[1, 2]);
rGrad_J[1, 3] := (rB_Mat[1,3] * rLambda_Costate[1,1]) + (rB_Mat[2,3] * rLambda_Costate[1,2]) + (rB_Mat[3,3] * rLambda_Costate[1,3]) + (rB_Mat[4,3] * rLambda_Costate[1,4]) + (rB_Mat[5,3] * rLambda_Costate[1,5]) + (rB_Mat[6,3] * rLambda_Costate[1,6]) + (rR_Diag[3] * rU_Opt_Seq[1,3]) + (rS_Diag[3] * (rU_Opt_Seq[1,3] - a_u_prev[3])) - (rS_Diag[3] * (rU_Opt_Seq[2,3] - rU_Opt_Seq[1,3]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[1, 3] * rGrad_J[1, 3]);
rGrad_J[1, 4] := (rB_Mat[1,4] * rLambda_Costate[1,1]) + (rB_Mat[2,4] * rLambda_Costate[1,2]) + (rB_Mat[3,4] * rLambda_Costate[1,3]) + (rB_Mat[4,4] * rLambda_Costate[1,4]) + (rB_Mat[5,4] * rLambda_Costate[1,5]) + (rB_Mat[6,4] * rLambda_Costate[1,6]) + (rR_Diag[4] * rU_Opt_Seq[1,4]) + (rS_Diag[4] * (rU_Opt_Seq[1,4] - a_u_prev[4])) - (rS_Diag[4] * (rU_Opt_Seq[2,4] - rU_Opt_Seq[1,4]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[1, 4] * rGrad_J[1, 4]);
rGrad_J[1, 5] := (rB_Mat[1,5] * rLambda_Costate[1,1]) + (rB_Mat[2,5] * rLambda_Costate[1,2]) + (rB_Mat[3,5] * rLambda_Costate[1,3]) + (rB_Mat[4,5] * rLambda_Costate[1,4]) + (rB_Mat[5,5] * rLambda_Costate[1,5]) + (rB_Mat[6,5] * rLambda_Costate[1,6]) + (rR_Diag[5] * rU_Opt_Seq[1,5]) + (rS_Diag[5] * (rU_Opt_Seq[1,5] - a_u_prev[5])) - (rS_Diag[5] * (rU_Opt_Seq[2,5] - rU_Opt_Seq[1,5]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[1, 5] * rGrad_J[1, 5]);

(* Gradient for u_2 (h=2) *)
rGrad_J[2, 1] := (rB_Mat[1,1] * rLambda_Costate[2,1]) + (rB_Mat[2,1] * rLambda_Costate[2,2]) + (rB_Mat[3,1] * rLambda_Costate[2,3]) + (rB_Mat[4,1] * rLambda_Costate[2,4]) + (rB_Mat[5,1] * rLambda_Costate[2,5]) + (rB_Mat[6,1] * rLambda_Costate[2,6]) + (rR_Diag[1] * rU_Opt_Seq[2,1]) + (rS_Diag[1] * (rU_Opt_Seq[2,1] - rU_Opt_Seq[1,1])) - (rS_Diag[1] * (rU_Opt_Seq[3,1] - rU_Opt_Seq[2,1]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[2, 1] * rGrad_J[2, 1]);
rGrad_J[2, 2] := (rB_Mat[1,2] * rLambda_Costate[2,1]) + (rB_Mat[2,2] * rLambda_Costate[2,2]) + (rB_Mat[3,2] * rLambda_Costate[2,3]) + (rB_Mat[4,2] * rLambda_Costate[2,4]) + (rB_Mat[5,2] * rLambda_Costate[2,5]) + (rB_Mat[6,2] * rLambda_Costate[2,6]) + (rR_Diag[2] * rU_Opt_Seq[2,2]) + (rS_Diag[2] * (rU_Opt_Seq[2,2] - rU_Opt_Seq[1,2])) - (rS_Diag[2] * (rU_Opt_Seq[3,2] - rU_Opt_Seq[2,2]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[2, 2] * rGrad_J[2, 2]);
rGrad_J[2, 3] := (rB_Mat[1,3] * rLambda_Costate[2,1]) + (rB_Mat[2,3] * rLambda_Costate[2,2]) + (rB_Mat[3,3] * rLambda_Costate[2,3]) + (rB_Mat[4,3] * rLambda_Costate[2,4]) + (rB_Mat[5,3] * rLambda_Costate[2,5]) + (rB_Mat[6,3] * rLambda_Costate[2,6]) + (rR_Diag[3] * rU_Opt_Seq[2,3]) + (rS_Diag[3] * (rU_Opt_Seq[2,3] - rU_Opt_Seq[1,3])) - (rS_Diag[3] * (rU_Opt_Seq[3,3] - rU_Opt_Seq[2,3]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[2, 3] * rGrad_J[2, 3]);
rGrad_J[2, 4] := (rB_Mat[1,4] * rLambda_Costate[2,1]) + (rB_Mat[2,4] * rLambda_Costate[2,2]) + (rB_Mat[3,4] * rLambda_Costate[2,3]) + (rB_Mat[4,4] * rLambda_Costate[2,4]) + (rB_Mat[5,4] * rLambda_Costate[2,5]) + (rB_Mat[6,4] * rLambda_Costate[2,6]) + (rR_Diag[4] * rU_Opt_Seq[2,4]) + (rS_Diag[4] * (rU_Opt_Seq[2,4] - rU_Opt_Seq[1,4])) - (rS_Diag[4] * (rU_Opt_Seq[3,4] - rU_Opt_Seq[2,4]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[2, 4] * rGrad_J[2, 4]);
rGrad_J[2, 5] := (rB_Mat[1,5] * rLambda_Costate[2,1]) + (rB_Mat[2,5] * rLambda_Costate[2,2]) + (rB_Mat[3,5] * rLambda_Costate[2,3]) + (rB_Mat[4,5] * rLambda_Costate[2,4]) + (rB_Mat[5,5] * rLambda_Costate[2,5]) + (rB_Mat[6,5] * rLambda_Costate[2,6]) + (rR_Diag[5] * rU_Opt_Seq[2,5]) + (rS_Diag[5] * (rU_Opt_Seq[2,5] - rU_Opt_Seq[1,5])) - (rS_Diag[5] * (rU_Opt_Seq[3,5] - rU_Opt_Seq[2,5]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[2, 5] * rGrad_J[2, 5]);

(* Gradient for u_3 (h=3, held through h=4, 5) *)
rGrad_J[3, 1] := (rB_Mat[1,1] * (rLambda_Costate[3,1] + rLambda_Costate[4,1] + rLambda_Costate[5,1])) + (rB_Mat[2,1] * (rLambda_Costate[3,2] + rLambda_Costate[4,2] + rLambda_Costate[5,2])) + (rB_Mat[3,1] * (rLambda_Costate[3,3] + rLambda_Costate[4,3] + rLambda_Costate[5,3])) + (rB_Mat[4,1] * (rLambda_Costate[3,4] + rLambda_Costate[4,4] + rLambda_Costate[5,4])) + (rB_Mat[5,1] * (rLambda_Costate[3,5] + rLambda_Costate[4,5] + rLambda_Costate[5,5])) + (rB_Mat[6,1] * (rLambda_Costate[3,6] + rLambda_Costate[4,6] + rLambda_Costate[5,6])) + (rR_Diag[1] * rU_Opt_Seq[3,1]) + (rS_Diag[1] * (rU_Opt_Seq[3,1] - rU_Opt_Seq[2,1]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[3, 1] * rGrad_J[3, 1]);
rGrad_J[3, 2] := (rB_Mat[1,2] * (rLambda_Costate[3,1] + rLambda_Costate[4,1] + rLambda_Costate[5,1])) + (rB_Mat[2,2] * (rLambda_Costate[3,2] + rLambda_Costate[4,2] + rLambda_Costate[5,2])) + (rB_Mat[3,2] * (rLambda_Costate[3,3] + rLambda_Costate[4,3] + rLambda_Costate[5,3])) + (rB_Mat[4,2] * (rLambda_Costate[3,4] + rLambda_Costate[4,4] + rLambda_Costate[5,4])) + (rB_Mat[5,2] * (rLambda_Costate[3,5] + rLambda_Costate[4,5] + rLambda_Costate[5,5])) + (rB_Mat[6,2] * (rLambda_Costate[3,6] + rLambda_Costate[4,6] + rLambda_Costate[5,6])) + (rR_Diag[2] * rU_Opt_Seq[3,2]) + (rS_Diag[2] * (rU_Opt_Seq[3,2] - rU_Opt_Seq[2,2]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[3, 2] * rGrad_J[3, 2]);
rGrad_J[3, 3] := (rB_Mat[1,3] * (rLambda_Costate[3,1] + rLambda_Costate[4,1] + rLambda_Costate[5,1])) + (rB_Mat[2,3] * (rLambda_Costate[3,2] + rLambda_Costate[4,2] + rLambda_Costate[5,2])) + (rB_Mat[3,3] * (rLambda_Costate[3,3] + rLambda_Costate[4,3] + rLambda_Costate[5,3])) + (rB_Mat[4,3] * (rLambda_Costate[3,4] + rLambda_Costate[4,4] + rLambda_Costate[5,4])) + (rB_Mat[5,3] * (rLambda_Costate[3,5] + rLambda_Costate[4,5] + rLambda_Costate[5,5])) + (rB_Mat[6,3] * (rLambda_Costate[3,6] + rLambda_Costate[4,6] + rLambda_Costate[5,6])) + (rR_Diag[3] * rU_Opt_Seq[3,3]) + (rS_Diag[3] * (rU_Opt_Seq[3,3] - rU_Opt_Seq[2,3]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[3, 3] * rGrad_J[3, 3]);
rGrad_J[3, 4] := (rB_Mat[1,4] * (rLambda_Costate[3,1] + rLambda_Costate[4,1] + rLambda_Costate[5,1])) + (rB_Mat[2,4] * (rLambda_Costate[3,2] + rLambda_Costate[4,2] + rLambda_Costate[5,2])) + (rB_Mat[3,4] * (rLambda_Costate[3,3] + rLambda_Costate[4,3] + rLambda_Costate[5,3])) + (rB_Mat[4,4] * (rLambda_Costate[3,4] + rLambda_Costate[4,4] + rLambda_Costate[5,4])) + (rB_Mat[5,4] * (rLambda_Costate[3,5] + rLambda_Costate[4,5] + rLambda_Costate[5,5])) + (rB_Mat[6,4] * (rLambda_Costate[3,6] + rLambda_Costate[4,6] + rLambda_Costate[5,6])) + (rR_Diag[4] * rU_Opt_Seq[3,4]) + (rS_Diag[4] * (rU_Opt_Seq[3,4] - rU_Opt_Seq[2,4]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[3, 4] * rGrad_J[3, 4]);
rGrad_J[3, 5] := (rB_Mat[1,5] * (rLambda_Costate[3,1] + rLambda_Costate[4,1] + rLambda_Costate[5,1])) + (rB_Mat[2,5] * (rLambda_Costate[3,2] + rLambda_Costate[4,2] + rLambda_Costate[5,2])) + (rB_Mat[3,5] * (rLambda_Costate[3,3] + rLambda_Costate[4,3] + rLambda_Costate[5,3])) + (rB_Mat[4,5] * (rLambda_Costate[3,4] + rLambda_Costate[4,4] + rLambda_Costate[5,4])) + (rB_Mat[5,5] * (rLambda_Costate[3,5] + rLambda_Costate[4,5] + rLambda_Costate[5,5])) + (rB_Mat[6,5] * (rLambda_Costate[3,6] + rLambda_Costate[4,6] + rLambda_Costate[5,6])) + (rR_Diag[5] * rU_Opt_Seq[3,5]) + (rS_Diag[5] * (rU_Opt_Seq[3,5] - rU_Opt_Seq[2,5]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[3, 5] * rGrad_J[3, 5]);

(* Iteration 3 - Projected Gradient Step with Hard Box & Dynamic Slew Limits *)
rTemp_Val := rU_Opt_Seq[1, 1] - (rAlpha_PGD_StepSize * rGrad_J[1, 1]);
(* Slew limit against prior actuator output *)
IF rTemp_Val > (a_u_prev[1] + rDeltaU_Max[1]) THEN
    rTemp_Val := a_u_prev[1] + rDeltaU_Max[1];
ELSIF rTemp_Val < (a_u_prev[1] - rDeltaU_Max[1]) THEN
    rTemp_Val := a_u_prev[1] - rDeltaU_Max[1];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[1] THEN
    rTemp_Val := rU_BoxMax[1];
ELSIF rTemp_Val < rU_BoxMin[1] THEN
    rTemp_Val := rU_BoxMin[1];
END_IF;
rU_Opt_Seq[1, 1] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[1, 2] - (rAlpha_PGD_StepSize * rGrad_J[1, 2]);
(* Slew limit against prior actuator output *)
IF rTemp_Val > (a_u_prev[2] + rDeltaU_Max[2]) THEN
    rTemp_Val := a_u_prev[2] + rDeltaU_Max[2];
ELSIF rTemp_Val < (a_u_prev[2] - rDeltaU_Max[2]) THEN
    rTemp_Val := a_u_prev[2] - rDeltaU_Max[2];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[2] THEN
    rTemp_Val := rU_BoxMax[2];
ELSIF rTemp_Val < rU_BoxMin[2] THEN
    rTemp_Val := rU_BoxMin[2];
END_IF;
rU_Opt_Seq[1, 2] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[1, 3] - (rAlpha_PGD_StepSize * rGrad_J[1, 3]);
(* Slew limit against prior actuator output *)
IF rTemp_Val > (a_u_prev[3] + rDeltaU_Max[3]) THEN
    rTemp_Val := a_u_prev[3] + rDeltaU_Max[3];
ELSIF rTemp_Val < (a_u_prev[3] - rDeltaU_Max[3]) THEN
    rTemp_Val := a_u_prev[3] - rDeltaU_Max[3];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[3] THEN
    rTemp_Val := rU_BoxMax[3];
ELSIF rTemp_Val < rU_BoxMin[3] THEN
    rTemp_Val := rU_BoxMin[3];
END_IF;
rU_Opt_Seq[1, 3] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[1, 4] - (rAlpha_PGD_StepSize * rGrad_J[1, 4]);
(* Slew limit against prior actuator output *)
IF rTemp_Val > (a_u_prev[4] + rDeltaU_Max[4]) THEN
    rTemp_Val := a_u_prev[4] + rDeltaU_Max[4];
ELSIF rTemp_Val < (a_u_prev[4] - rDeltaU_Max[4]) THEN
    rTemp_Val := a_u_prev[4] - rDeltaU_Max[4];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[4] THEN
    rTemp_Val := rU_BoxMax[4];
ELSIF rTemp_Val < rU_BoxMin[4] THEN
    rTemp_Val := rU_BoxMin[4];
END_IF;
rU_Opt_Seq[1, 4] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[1, 5] - (rAlpha_PGD_StepSize * rGrad_J[1, 5]);
(* Slew limit against prior actuator output *)
IF rTemp_Val > (a_u_prev[5] + rDeltaU_Max[5]) THEN
    rTemp_Val := a_u_prev[5] + rDeltaU_Max[5];
ELSIF rTemp_Val < (a_u_prev[5] - rDeltaU_Max[5]) THEN
    rTemp_Val := a_u_prev[5] - rDeltaU_Max[5];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[5] THEN
    rTemp_Val := rU_BoxMax[5];
ELSIF rTemp_Val < rU_BoxMin[5] THEN
    rTemp_Val := rU_BoxMin[5];
END_IF;
rU_Opt_Seq[1, 5] := rTemp_Val;

rTemp_Val := rU_Opt_Seq[2, 1] - (rAlpha_PGD_StepSize * rGrad_J[2, 1]);
(* Slew limit against step 1 *)
IF rTemp_Val > (rU_Opt_Seq[1, 1] + rDeltaU_Max[1]) THEN
    rTemp_Val := rU_Opt_Seq[1, 1] + rDeltaU_Max[1];
ELSIF rTemp_Val < (rU_Opt_Seq[1, 1] - rDeltaU_Max[1]) THEN
    rTemp_Val := rU_Opt_Seq[1, 1] - rDeltaU_Max[1];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[1] THEN
    rTemp_Val := rU_BoxMax[1];
ELSIF rTemp_Val < rU_BoxMin[1] THEN
    rTemp_Val := rU_BoxMin[1];
END_IF;
rU_Opt_Seq[2, 1] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[2, 2] - (rAlpha_PGD_StepSize * rGrad_J[2, 2]);
(* Slew limit against step 1 *)
IF rTemp_Val > (rU_Opt_Seq[1, 2] + rDeltaU_Max[2]) THEN
    rTemp_Val := rU_Opt_Seq[1, 2] + rDeltaU_Max[2];
ELSIF rTemp_Val < (rU_Opt_Seq[1, 2] - rDeltaU_Max[2]) THEN
    rTemp_Val := rU_Opt_Seq[1, 2] - rDeltaU_Max[2];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[2] THEN
    rTemp_Val := rU_BoxMax[2];
ELSIF rTemp_Val < rU_BoxMin[2] THEN
    rTemp_Val := rU_BoxMin[2];
END_IF;
rU_Opt_Seq[2, 2] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[2, 3] - (rAlpha_PGD_StepSize * rGrad_J[2, 3]);
(* Slew limit against step 1 *)
IF rTemp_Val > (rU_Opt_Seq[1, 3] + rDeltaU_Max[3]) THEN
    rTemp_Val := rU_Opt_Seq[1, 3] + rDeltaU_Max[3];
ELSIF rTemp_Val < (rU_Opt_Seq[1, 3] - rDeltaU_Max[3]) THEN
    rTemp_Val := rU_Opt_Seq[1, 3] - rDeltaU_Max[3];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[3] THEN
    rTemp_Val := rU_BoxMax[3];
ELSIF rTemp_Val < rU_BoxMin[3] THEN
    rTemp_Val := rU_BoxMin[3];
END_IF;
rU_Opt_Seq[2, 3] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[2, 4] - (rAlpha_PGD_StepSize * rGrad_J[2, 4]);
(* Slew limit against step 1 *)
IF rTemp_Val > (rU_Opt_Seq[1, 4] + rDeltaU_Max[4]) THEN
    rTemp_Val := rU_Opt_Seq[1, 4] + rDeltaU_Max[4];
ELSIF rTemp_Val < (rU_Opt_Seq[1, 4] - rDeltaU_Max[4]) THEN
    rTemp_Val := rU_Opt_Seq[1, 4] - rDeltaU_Max[4];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[4] THEN
    rTemp_Val := rU_BoxMax[4];
ELSIF rTemp_Val < rU_BoxMin[4] THEN
    rTemp_Val := rU_BoxMin[4];
END_IF;
rU_Opt_Seq[2, 4] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[2, 5] - (rAlpha_PGD_StepSize * rGrad_J[2, 5]);
(* Slew limit against step 1 *)
IF rTemp_Val > (rU_Opt_Seq[1, 5] + rDeltaU_Max[5]) THEN
    rTemp_Val := rU_Opt_Seq[1, 5] + rDeltaU_Max[5];
ELSIF rTemp_Val < (rU_Opt_Seq[1, 5] - rDeltaU_Max[5]) THEN
    rTemp_Val := rU_Opt_Seq[1, 5] - rDeltaU_Max[5];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[5] THEN
    rTemp_Val := rU_BoxMax[5];
ELSIF rTemp_Val < rU_BoxMin[5] THEN
    rTemp_Val := rU_BoxMin[5];
END_IF;
rU_Opt_Seq[2, 5] := rTemp_Val;

rTemp_Val := rU_Opt_Seq[3, 1] - (rAlpha_PGD_StepSize * rGrad_J[3, 1]);
(* Slew limit against step 2 *)
IF rTemp_Val > (rU_Opt_Seq[2, 1] + rDeltaU_Max[1]) THEN
    rTemp_Val := rU_Opt_Seq[2, 1] + rDeltaU_Max[1];
ELSIF rTemp_Val < (rU_Opt_Seq[2, 1] - rDeltaU_Max[1]) THEN
    rTemp_Val := rU_Opt_Seq[2, 1] - rDeltaU_Max[1];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[1] THEN
    rTemp_Val := rU_BoxMax[1];
ELSIF rTemp_Val < rU_BoxMin[1] THEN
    rTemp_Val := rU_BoxMin[1];
END_IF;
rU_Opt_Seq[3, 1] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[3, 2] - (rAlpha_PGD_StepSize * rGrad_J[3, 2]);
(* Slew limit against step 2 *)
IF rTemp_Val > (rU_Opt_Seq[2, 2] + rDeltaU_Max[2]) THEN
    rTemp_Val := rU_Opt_Seq[2, 2] + rDeltaU_Max[2];
ELSIF rTemp_Val < (rU_Opt_Seq[2, 2] - rDeltaU_Max[2]) THEN
    rTemp_Val := rU_Opt_Seq[2, 2] - rDeltaU_Max[2];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[2] THEN
    rTemp_Val := rU_BoxMax[2];
ELSIF rTemp_Val < rU_BoxMin[2] THEN
    rTemp_Val := rU_BoxMin[2];
END_IF;
rU_Opt_Seq[3, 2] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[3, 3] - (rAlpha_PGD_StepSize * rGrad_J[3, 3]);
(* Slew limit against step 2 *)
IF rTemp_Val > (rU_Opt_Seq[2, 3] + rDeltaU_Max[3]) THEN
    rTemp_Val := rU_Opt_Seq[2, 3] + rDeltaU_Max[3];
ELSIF rTemp_Val < (rU_Opt_Seq[2, 3] - rDeltaU_Max[3]) THEN
    rTemp_Val := rU_Opt_Seq[2, 3] - rDeltaU_Max[3];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[3] THEN
    rTemp_Val := rU_BoxMax[3];
ELSIF rTemp_Val < rU_BoxMin[3] THEN
    rTemp_Val := rU_BoxMin[3];
END_IF;
rU_Opt_Seq[3, 3] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[3, 4] - (rAlpha_PGD_StepSize * rGrad_J[3, 4]);
(* Slew limit against step 2 *)
IF rTemp_Val > (rU_Opt_Seq[2, 4] + rDeltaU_Max[4]) THEN
    rTemp_Val := rU_Opt_Seq[2, 4] + rDeltaU_Max[4];
ELSIF rTemp_Val < (rU_Opt_Seq[2, 4] - rDeltaU_Max[4]) THEN
    rTemp_Val := rU_Opt_Seq[2, 4] - rDeltaU_Max[4];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[4] THEN
    rTemp_Val := rU_BoxMax[4];
ELSIF rTemp_Val < rU_BoxMin[4] THEN
    rTemp_Val := rU_BoxMin[4];
END_IF;
rU_Opt_Seq[3, 4] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[3, 5] - (rAlpha_PGD_StepSize * rGrad_J[3, 5]);
(* Slew limit against step 2 *)
IF rTemp_Val > (rU_Opt_Seq[2, 5] + rDeltaU_Max[5]) THEN
    rTemp_Val := rU_Opt_Seq[2, 5] + rDeltaU_Max[5];
ELSIF rTemp_Val < (rU_Opt_Seq[2, 5] - rDeltaU_Max[5]) THEN
    rTemp_Val := rU_Opt_Seq[2, 5] - rDeltaU_Max[5];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[5] THEN
    rTemp_Val := rU_BoxMax[5];
ELSIF rTemp_Val < rU_BoxMin[5] THEN
    rTemp_Val := rU_BoxMin[5];
END_IF;
rU_Opt_Seq[3, 5] := rTemp_Val;

(* ================================================================================================== *)
(* MPC PROJECTED GRADIENT DESCENT -- UNROLLED ITERATION 4 OF 10                                 *)
(* ================================================================================================== *)
iPGD_IterCount := 4;

(* Iteration 4 - Forward State Prediction Step 1 (h=1): x_1 = A * x_hat + B * u_1 *)
rX_Pred_Horizon[1, 1] := (rA_Mat[1,1] * a_x_hat[1]) + (rA_Mat[1,2] * a_x_hat[2]) + (rA_Mat[1,3] * a_x_hat[3]) + (rA_Mat[1,4] * a_x_hat[4]) + (rA_Mat[1,5] * a_x_hat[5]) + (rA_Mat[1,6] * a_x_hat[6]) + (rB_Mat[1,1] * rU_Opt_Seq[1,1]) + (rB_Mat[1,2] * rU_Opt_Seq[1,2]) + (rB_Mat[1,3] * rU_Opt_Seq[1,3]) + (rB_Mat[1,4] * rU_Opt_Seq[1,4]) + (rB_Mat[1,5] * rU_Opt_Seq[1,5]);
rX_Pred_Horizon[1, 2] := (rA_Mat[2,1] * a_x_hat[1]) + (rA_Mat[2,2] * a_x_hat[2]) + (rA_Mat[2,3] * a_x_hat[3]) + (rA_Mat[2,4] * a_x_hat[4]) + (rA_Mat[2,5] * a_x_hat[5]) + (rA_Mat[2,6] * a_x_hat[6]) + (rB_Mat[2,1] * rU_Opt_Seq[1,1]) + (rB_Mat[2,2] * rU_Opt_Seq[1,2]) + (rB_Mat[2,3] * rU_Opt_Seq[1,3]) + (rB_Mat[2,4] * rU_Opt_Seq[1,4]) + (rB_Mat[2,5] * rU_Opt_Seq[1,5]);
rX_Pred_Horizon[1, 3] := (rA_Mat[3,1] * a_x_hat[1]) + (rA_Mat[3,2] * a_x_hat[2]) + (rA_Mat[3,3] * a_x_hat[3]) + (rA_Mat[3,4] * a_x_hat[4]) + (rA_Mat[3,5] * a_x_hat[5]) + (rA_Mat[3,6] * a_x_hat[6]) + (rB_Mat[3,1] * rU_Opt_Seq[1,1]) + (rB_Mat[3,2] * rU_Opt_Seq[1,2]) + (rB_Mat[3,3] * rU_Opt_Seq[1,3]) + (rB_Mat[3,4] * rU_Opt_Seq[1,4]) + (rB_Mat[3,5] * rU_Opt_Seq[1,5]);
rX_Pred_Horizon[1, 4] := (rA_Mat[4,1] * a_x_hat[1]) + (rA_Mat[4,2] * a_x_hat[2]) + (rA_Mat[4,3] * a_x_hat[3]) + (rA_Mat[4,4] * a_x_hat[4]) + (rA_Mat[4,5] * a_x_hat[5]) + (rA_Mat[4,6] * a_x_hat[6]) + (rB_Mat[4,1] * rU_Opt_Seq[1,1]) + (rB_Mat[4,2] * rU_Opt_Seq[1,2]) + (rB_Mat[4,3] * rU_Opt_Seq[1,3]) + (rB_Mat[4,4] * rU_Opt_Seq[1,4]) + (rB_Mat[4,5] * rU_Opt_Seq[1,5]);
rX_Pred_Horizon[1, 5] := (rA_Mat[5,1] * a_x_hat[1]) + (rA_Mat[5,2] * a_x_hat[2]) + (rA_Mat[5,3] * a_x_hat[3]) + (rA_Mat[5,4] * a_x_hat[4]) + (rA_Mat[5,5] * a_x_hat[5]) + (rA_Mat[5,6] * a_x_hat[6]) + (rB_Mat[5,1] * rU_Opt_Seq[1,1]) + (rB_Mat[5,2] * rU_Opt_Seq[1,2]) + (rB_Mat[5,3] * rU_Opt_Seq[1,3]) + (rB_Mat[5,4] * rU_Opt_Seq[1,4]) + (rB_Mat[5,5] * rU_Opt_Seq[1,5]);
rX_Pred_Horizon[1, 6] := (rA_Mat[6,1] * a_x_hat[1]) + (rA_Mat[6,2] * a_x_hat[2]) + (rA_Mat[6,3] * a_x_hat[3]) + (rA_Mat[6,4] * a_x_hat[4]) + (rA_Mat[6,5] * a_x_hat[5]) + (rA_Mat[6,6] * a_x_hat[6]) + (rB_Mat[6,1] * rU_Opt_Seq[1,1]) + (rB_Mat[6,2] * rU_Opt_Seq[1,2]) + (rB_Mat[6,3] * rU_Opt_Seq[1,3]) + (rB_Mat[6,4] * rU_Opt_Seq[1,4]) + (rB_Mat[6,5] * rU_Opt_Seq[1,5]);

(* Iteration 4 - Forward State Prediction Step 2 (h=2): x_2 = A * x_1 + B * u_2 *)
rX_Pred_Horizon[2, 1] := (rA_Mat[1,1] * rX_Pred_Horizon[1,1]) + (rA_Mat[1,2] * rX_Pred_Horizon[1,2]) + (rA_Mat[1,3] * rX_Pred_Horizon[1,3]) + (rA_Mat[1,4] * rX_Pred_Horizon[1,4]) + (rA_Mat[1,5] * rX_Pred_Horizon[1,5]) + (rA_Mat[1,6] * rX_Pred_Horizon[1,6]) + (rB_Mat[1,1] * rU_Opt_Seq[2,1]) + (rB_Mat[1,2] * rU_Opt_Seq[2,2]) + (rB_Mat[1,3] * rU_Opt_Seq[2,3]) + (rB_Mat[1,4] * rU_Opt_Seq[2,4]) + (rB_Mat[1,5] * rU_Opt_Seq[2,5]);
rX_Pred_Horizon[2, 2] := (rA_Mat[2,1] * rX_Pred_Horizon[1,1]) + (rA_Mat[2,2] * rX_Pred_Horizon[1,2]) + (rA_Mat[2,3] * rX_Pred_Horizon[1,3]) + (rA_Mat[2,4] * rX_Pred_Horizon[1,4]) + (rA_Mat[2,5] * rX_Pred_Horizon[1,5]) + (rA_Mat[2,6] * rX_Pred_Horizon[1,6]) + (rB_Mat[2,1] * rU_Opt_Seq[2,1]) + (rB_Mat[2,2] * rU_Opt_Seq[2,2]) + (rB_Mat[2,3] * rU_Opt_Seq[2,3]) + (rB_Mat[2,4] * rU_Opt_Seq[2,4]) + (rB_Mat[2,5] * rU_Opt_Seq[2,5]);
rX_Pred_Horizon[2, 3] := (rA_Mat[3,1] * rX_Pred_Horizon[1,1]) + (rA_Mat[3,2] * rX_Pred_Horizon[1,2]) + (rA_Mat[3,3] * rX_Pred_Horizon[1,3]) + (rA_Mat[3,4] * rX_Pred_Horizon[1,4]) + (rA_Mat[3,5] * rX_Pred_Horizon[1,5]) + (rA_Mat[3,6] * rX_Pred_Horizon[1,6]) + (rB_Mat[3,1] * rU_Opt_Seq[2,1]) + (rB_Mat[3,2] * rU_Opt_Seq[2,2]) + (rB_Mat[3,3] * rU_Opt_Seq[2,3]) + (rB_Mat[3,4] * rU_Opt_Seq[2,4]) + (rB_Mat[3,5] * rU_Opt_Seq[2,5]);
rX_Pred_Horizon[2, 4] := (rA_Mat[4,1] * rX_Pred_Horizon[1,1]) + (rA_Mat[4,2] * rX_Pred_Horizon[1,2]) + (rA_Mat[4,3] * rX_Pred_Horizon[1,3]) + (rA_Mat[4,4] * rX_Pred_Horizon[1,4]) + (rA_Mat[4,5] * rX_Pred_Horizon[1,5]) + (rA_Mat[4,6] * rX_Pred_Horizon[1,6]) + (rB_Mat[4,1] * rU_Opt_Seq[2,1]) + (rB_Mat[4,2] * rU_Opt_Seq[2,2]) + (rB_Mat[4,3] * rU_Opt_Seq[2,3]) + (rB_Mat[4,4] * rU_Opt_Seq[2,4]) + (rB_Mat[4,5] * rU_Opt_Seq[2,5]);
rX_Pred_Horizon[2, 5] := (rA_Mat[5,1] * rX_Pred_Horizon[1,1]) + (rA_Mat[5,2] * rX_Pred_Horizon[1,2]) + (rA_Mat[5,3] * rX_Pred_Horizon[1,3]) + (rA_Mat[5,4] * rX_Pred_Horizon[1,4]) + (rA_Mat[5,5] * rX_Pred_Horizon[1,5]) + (rA_Mat[5,6] * rX_Pred_Horizon[1,6]) + (rB_Mat[5,1] * rU_Opt_Seq[2,1]) + (rB_Mat[5,2] * rU_Opt_Seq[2,2]) + (rB_Mat[5,3] * rU_Opt_Seq[2,3]) + (rB_Mat[5,4] * rU_Opt_Seq[2,4]) + (rB_Mat[5,5] * rU_Opt_Seq[2,5]);
rX_Pred_Horizon[2, 6] := (rA_Mat[6,1] * rX_Pred_Horizon[1,1]) + (rA_Mat[6,2] * rX_Pred_Horizon[1,2]) + (rA_Mat[6,3] * rX_Pred_Horizon[1,3]) + (rA_Mat[6,4] * rX_Pred_Horizon[1,4]) + (rA_Mat[6,5] * rX_Pred_Horizon[1,5]) + (rA_Mat[6,6] * rX_Pred_Horizon[1,6]) + (rB_Mat[6,1] * rU_Opt_Seq[2,1]) + (rB_Mat[6,2] * rU_Opt_Seq[2,2]) + (rB_Mat[6,3] * rU_Opt_Seq[2,3]) + (rB_Mat[6,4] * rU_Opt_Seq[2,4]) + (rB_Mat[6,5] * rU_Opt_Seq[2,5]);

(* Iteration 4 - Forward State Prediction Step 3 (h=3): x_3 = A * x_2 + B * u_3 *)
rX_Pred_Horizon[3, 1] := (rA_Mat[1,1] * rX_Pred_Horizon[2,1]) + (rA_Mat[1,2] * rX_Pred_Horizon[2,2]) + (rA_Mat[1,3] * rX_Pred_Horizon[2,3]) + (rA_Mat[1,4] * rX_Pred_Horizon[2,4]) + (rA_Mat[1,5] * rX_Pred_Horizon[2,5]) + (rA_Mat[1,6] * rX_Pred_Horizon[2,6]) + (rB_Mat[1,1] * rU_Opt_Seq[3,1]) + (rB_Mat[1,2] * rU_Opt_Seq[3,2]) + (rB_Mat[1,3] * rU_Opt_Seq[3,3]) + (rB_Mat[1,4] * rU_Opt_Seq[3,4]) + (rB_Mat[1,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[3, 2] := (rA_Mat[2,1] * rX_Pred_Horizon[2,1]) + (rA_Mat[2,2] * rX_Pred_Horizon[2,2]) + (rA_Mat[2,3] * rX_Pred_Horizon[2,3]) + (rA_Mat[2,4] * rX_Pred_Horizon[2,4]) + (rA_Mat[2,5] * rX_Pred_Horizon[2,5]) + (rA_Mat[2,6] * rX_Pred_Horizon[2,6]) + (rB_Mat[2,1] * rU_Opt_Seq[3,1]) + (rB_Mat[2,2] * rU_Opt_Seq[3,2]) + (rB_Mat[2,3] * rU_Opt_Seq[3,3]) + (rB_Mat[2,4] * rU_Opt_Seq[3,4]) + (rB_Mat[2,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[3, 3] := (rA_Mat[3,1] * rX_Pred_Horizon[2,1]) + (rA_Mat[3,2] * rX_Pred_Horizon[2,2]) + (rA_Mat[3,3] * rX_Pred_Horizon[2,3]) + (rA_Mat[3,4] * rX_Pred_Horizon[2,4]) + (rA_Mat[3,5] * rX_Pred_Horizon[2,5]) + (rA_Mat[3,6] * rX_Pred_Horizon[2,6]) + (rB_Mat[3,1] * rU_Opt_Seq[3,1]) + (rB_Mat[3,2] * rU_Opt_Seq[3,2]) + (rB_Mat[3,3] * rU_Opt_Seq[3,3]) + (rB_Mat[3,4] * rU_Opt_Seq[3,4]) + (rB_Mat[3,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[3, 4] := (rA_Mat[4,1] * rX_Pred_Horizon[2,1]) + (rA_Mat[4,2] * rX_Pred_Horizon[2,2]) + (rA_Mat[4,3] * rX_Pred_Horizon[2,3]) + (rA_Mat[4,4] * rX_Pred_Horizon[2,4]) + (rA_Mat[4,5] * rX_Pred_Horizon[2,5]) + (rA_Mat[4,6] * rX_Pred_Horizon[2,6]) + (rB_Mat[4,1] * rU_Opt_Seq[3,1]) + (rB_Mat[4,2] * rU_Opt_Seq[3,2]) + (rB_Mat[4,3] * rU_Opt_Seq[3,3]) + (rB_Mat[4,4] * rU_Opt_Seq[3,4]) + (rB_Mat[4,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[3, 5] := (rA_Mat[5,1] * rX_Pred_Horizon[2,1]) + (rA_Mat[5,2] * rX_Pred_Horizon[2,2]) + (rA_Mat[5,3] * rX_Pred_Horizon[2,3]) + (rA_Mat[5,4] * rX_Pred_Horizon[2,4]) + (rA_Mat[5,5] * rX_Pred_Horizon[2,5]) + (rA_Mat[5,6] * rX_Pred_Horizon[2,6]) + (rB_Mat[5,1] * rU_Opt_Seq[3,1]) + (rB_Mat[5,2] * rU_Opt_Seq[3,2]) + (rB_Mat[5,3] * rU_Opt_Seq[3,3]) + (rB_Mat[5,4] * rU_Opt_Seq[3,4]) + (rB_Mat[5,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[3, 6] := (rA_Mat[6,1] * rX_Pred_Horizon[2,1]) + (rA_Mat[6,2] * rX_Pred_Horizon[2,2]) + (rA_Mat[6,3] * rX_Pred_Horizon[2,3]) + (rA_Mat[6,4] * rX_Pred_Horizon[2,4]) + (rA_Mat[6,5] * rX_Pred_Horizon[2,5]) + (rA_Mat[6,6] * rX_Pred_Horizon[2,6]) + (rB_Mat[6,1] * rU_Opt_Seq[3,1]) + (rB_Mat[6,2] * rU_Opt_Seq[3,2]) + (rB_Mat[6,3] * rU_Opt_Seq[3,3]) + (rB_Mat[6,4] * rU_Opt_Seq[3,4]) + (rB_Mat[6,5] * rU_Opt_Seq[3,5]);

(* Iteration 4 - Forward State Prediction Step 4 (h=4): x_4 = A * x_3 + B * u_3 (held beyond Hu) *)
rX_Pred_Horizon[4, 1] := (rA_Mat[1,1] * rX_Pred_Horizon[3,1]) + (rA_Mat[1,2] * rX_Pred_Horizon[3,2]) + (rA_Mat[1,3] * rX_Pred_Horizon[3,3]) + (rA_Mat[1,4] * rX_Pred_Horizon[3,4]) + (rA_Mat[1,5] * rX_Pred_Horizon[3,5]) + (rA_Mat[1,6] * rX_Pred_Horizon[3,6]) + (rB_Mat[1,1] * rU_Opt_Seq[3,1]) + (rB_Mat[1,2] * rU_Opt_Seq[3,2]) + (rB_Mat[1,3] * rU_Opt_Seq[3,3]) + (rB_Mat[1,4] * rU_Opt_Seq[3,4]) + (rB_Mat[1,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[4, 2] := (rA_Mat[2,1] * rX_Pred_Horizon[3,1]) + (rA_Mat[2,2] * rX_Pred_Horizon[3,2]) + (rA_Mat[2,3] * rX_Pred_Horizon[3,3]) + (rA_Mat[2,4] * rX_Pred_Horizon[3,4]) + (rA_Mat[2,5] * rX_Pred_Horizon[3,5]) + (rA_Mat[2,6] * rX_Pred_Horizon[3,6]) + (rB_Mat[2,1] * rU_Opt_Seq[3,1]) + (rB_Mat[2,2] * rU_Opt_Seq[3,2]) + (rB_Mat[2,3] * rU_Opt_Seq[3,3]) + (rB_Mat[2,4] * rU_Opt_Seq[3,4]) + (rB_Mat[2,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[4, 3] := (rA_Mat[3,1] * rX_Pred_Horizon[3,1]) + (rA_Mat[3,2] * rX_Pred_Horizon[3,2]) + (rA_Mat[3,3] * rX_Pred_Horizon[3,3]) + (rA_Mat[3,4] * rX_Pred_Horizon[3,4]) + (rA_Mat[3,5] * rX_Pred_Horizon[3,5]) + (rA_Mat[3,6] * rX_Pred_Horizon[3,6]) + (rB_Mat[3,1] * rU_Opt_Seq[3,1]) + (rB_Mat[3,2] * rU_Opt_Seq[3,2]) + (rB_Mat[3,3] * rU_Opt_Seq[3,3]) + (rB_Mat[3,4] * rU_Opt_Seq[3,4]) + (rB_Mat[3,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[4, 4] := (rA_Mat[4,1] * rX_Pred_Horizon[3,1]) + (rA_Mat[4,2] * rX_Pred_Horizon[3,2]) + (rA_Mat[4,3] * rX_Pred_Horizon[3,3]) + (rA_Mat[4,4] * rX_Pred_Horizon[3,4]) + (rA_Mat[4,5] * rX_Pred_Horizon[3,5]) + (rA_Mat[4,6] * rX_Pred_Horizon[3,6]) + (rB_Mat[4,1] * rU_Opt_Seq[3,1]) + (rB_Mat[4,2] * rU_Opt_Seq[3,2]) + (rB_Mat[4,3] * rU_Opt_Seq[3,3]) + (rB_Mat[4,4] * rU_Opt_Seq[3,4]) + (rB_Mat[4,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[4, 5] := (rA_Mat[5,1] * rX_Pred_Horizon[3,1]) + (rA_Mat[5,2] * rX_Pred_Horizon[3,2]) + (rA_Mat[5,3] * rX_Pred_Horizon[3,3]) + (rA_Mat[5,4] * rX_Pred_Horizon[3,4]) + (rA_Mat[5,5] * rX_Pred_Horizon[3,5]) + (rA_Mat[5,6] * rX_Pred_Horizon[3,6]) + (rB_Mat[5,1] * rU_Opt_Seq[3,1]) + (rB_Mat[5,2] * rU_Opt_Seq[3,2]) + (rB_Mat[5,3] * rU_Opt_Seq[3,3]) + (rB_Mat[5,4] * rU_Opt_Seq[3,4]) + (rB_Mat[5,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[4, 6] := (rA_Mat[6,1] * rX_Pred_Horizon[3,1]) + (rA_Mat[6,2] * rX_Pred_Horizon[3,2]) + (rA_Mat[6,3] * rX_Pred_Horizon[3,3]) + (rA_Mat[6,4] * rX_Pred_Horizon[3,4]) + (rA_Mat[6,5] * rX_Pred_Horizon[3,5]) + (rA_Mat[6,6] * rX_Pred_Horizon[3,6]) + (rB_Mat[6,1] * rU_Opt_Seq[3,1]) + (rB_Mat[6,2] * rU_Opt_Seq[3,2]) + (rB_Mat[6,3] * rU_Opt_Seq[3,3]) + (rB_Mat[6,4] * rU_Opt_Seq[3,4]) + (rB_Mat[6,5] * rU_Opt_Seq[3,5]);

(* Iteration 4 - Forward State Prediction Step 5 (h=5): x_5 = A * x_4 + B * u_3 (held beyond Hu) *)
rX_Pred_Horizon[5, 1] := (rA_Mat[1,1] * rX_Pred_Horizon[4,1]) + (rA_Mat[1,2] * rX_Pred_Horizon[4,2]) + (rA_Mat[1,3] * rX_Pred_Horizon[4,3]) + (rA_Mat[1,4] * rX_Pred_Horizon[4,4]) + (rA_Mat[1,5] * rX_Pred_Horizon[4,5]) + (rA_Mat[1,6] * rX_Pred_Horizon[4,6]) + (rB_Mat[1,1] * rU_Opt_Seq[3,1]) + (rB_Mat[1,2] * rU_Opt_Seq[3,2]) + (rB_Mat[1,3] * rU_Opt_Seq[3,3]) + (rB_Mat[1,4] * rU_Opt_Seq[3,4]) + (rB_Mat[1,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[5, 2] := (rA_Mat[2,1] * rX_Pred_Horizon[4,1]) + (rA_Mat[2,2] * rX_Pred_Horizon[4,2]) + (rA_Mat[2,3] * rX_Pred_Horizon[4,3]) + (rA_Mat[2,4] * rX_Pred_Horizon[4,4]) + (rA_Mat[2,5] * rX_Pred_Horizon[4,5]) + (rA_Mat[2,6] * rX_Pred_Horizon[4,6]) + (rB_Mat[2,1] * rU_Opt_Seq[3,1]) + (rB_Mat[2,2] * rU_Opt_Seq[3,2]) + (rB_Mat[2,3] * rU_Opt_Seq[3,3]) + (rB_Mat[2,4] * rU_Opt_Seq[3,4]) + (rB_Mat[2,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[5, 3] := (rA_Mat[3,1] * rX_Pred_Horizon[4,1]) + (rA_Mat[3,2] * rX_Pred_Horizon[4,2]) + (rA_Mat[3,3] * rX_Pred_Horizon[4,3]) + (rA_Mat[3,4] * rX_Pred_Horizon[4,4]) + (rA_Mat[3,5] * rX_Pred_Horizon[4,5]) + (rA_Mat[3,6] * rX_Pred_Horizon[4,6]) + (rB_Mat[3,1] * rU_Opt_Seq[3,1]) + (rB_Mat[3,2] * rU_Opt_Seq[3,2]) + (rB_Mat[3,3] * rU_Opt_Seq[3,3]) + (rB_Mat[3,4] * rU_Opt_Seq[3,4]) + (rB_Mat[3,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[5, 4] := (rA_Mat[4,1] * rX_Pred_Horizon[4,1]) + (rA_Mat[4,2] * rX_Pred_Horizon[4,2]) + (rA_Mat[4,3] * rX_Pred_Horizon[4,3]) + (rA_Mat[4,4] * rX_Pred_Horizon[4,4]) + (rA_Mat[4,5] * rX_Pred_Horizon[4,5]) + (rA_Mat[4,6] * rX_Pred_Horizon[4,6]) + (rB_Mat[4,1] * rU_Opt_Seq[3,1]) + (rB_Mat[4,2] * rU_Opt_Seq[3,2]) + (rB_Mat[4,3] * rU_Opt_Seq[3,3]) + (rB_Mat[4,4] * rU_Opt_Seq[3,4]) + (rB_Mat[4,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[5, 5] := (rA_Mat[5,1] * rX_Pred_Horizon[4,1]) + (rA_Mat[5,2] * rX_Pred_Horizon[4,2]) + (rA_Mat[5,3] * rX_Pred_Horizon[4,3]) + (rA_Mat[5,4] * rX_Pred_Horizon[4,4]) + (rA_Mat[5,5] * rX_Pred_Horizon[4,5]) + (rA_Mat[5,6] * rX_Pred_Horizon[4,6]) + (rB_Mat[5,1] * rU_Opt_Seq[3,1]) + (rB_Mat[5,2] * rU_Opt_Seq[3,2]) + (rB_Mat[5,3] * rU_Opt_Seq[3,3]) + (rB_Mat[5,4] * rU_Opt_Seq[3,4]) + (rB_Mat[5,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[5, 6] := (rA_Mat[6,1] * rX_Pred_Horizon[4,1]) + (rA_Mat[6,2] * rX_Pred_Horizon[4,2]) + (rA_Mat[6,3] * rX_Pred_Horizon[4,3]) + (rA_Mat[6,4] * rX_Pred_Horizon[4,4]) + (rA_Mat[6,5] * rX_Pred_Horizon[4,5]) + (rA_Mat[6,6] * rX_Pred_Horizon[4,6]) + (rB_Mat[6,1] * rU_Opt_Seq[3,1]) + (rB_Mat[6,2] * rU_Opt_Seq[3,2]) + (rB_Mat[6,3] * rU_Opt_Seq[3,3]) + (rB_Mat[6,4] * rU_Opt_Seq[3,4]) + (rB_Mat[6,5] * rU_Opt_Seq[3,5]);

(* Iteration 4 - Evaluate Objective Function Cost J *)
rMPC_Cost_J := 0.0;
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[1] * (rX_Pred_Horizon[1,1] - rX_Target[1,1]) * (rX_Pred_Horizon[1,1] - rX_Target[1,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[2] * (rX_Pred_Horizon[1,2] - rX_Target[1,2]) * (rX_Pred_Horizon[1,2] - rX_Target[1,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[3] * (rX_Pred_Horizon[1,3] - rX_Target[1,3]) * (rX_Pred_Horizon[1,3] - rX_Target[1,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[4] * (rX_Pred_Horizon[1,4] - rX_Target[1,4]) * (rX_Pred_Horizon[1,4] - rX_Target[1,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[5] * (rX_Pred_Horizon[1,5] - rX_Target[1,5]) * (rX_Pred_Horizon[1,5] - rX_Target[1,5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[6] * (rX_Pred_Horizon[1,6] - rX_Target[1,6]) * (rX_Pred_Horizon[1,6] - rX_Target[1,6]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[1] * (rX_Pred_Horizon[2,1] - rX_Target[2,1]) * (rX_Pred_Horizon[2,1] - rX_Target[2,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[2] * (rX_Pred_Horizon[2,2] - rX_Target[2,2]) * (rX_Pred_Horizon[2,2] - rX_Target[2,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[3] * (rX_Pred_Horizon[2,3] - rX_Target[2,3]) * (rX_Pred_Horizon[2,3] - rX_Target[2,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[4] * (rX_Pred_Horizon[2,4] - rX_Target[2,4]) * (rX_Pred_Horizon[2,4] - rX_Target[2,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[5] * (rX_Pred_Horizon[2,5] - rX_Target[2,5]) * (rX_Pred_Horizon[2,5] - rX_Target[2,5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[6] * (rX_Pred_Horizon[2,6] - rX_Target[2,6]) * (rX_Pred_Horizon[2,6] - rX_Target[2,6]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[1] * (rX_Pred_Horizon[3,1] - rX_Target[3,1]) * (rX_Pred_Horizon[3,1] - rX_Target[3,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[2] * (rX_Pred_Horizon[3,2] - rX_Target[3,2]) * (rX_Pred_Horizon[3,2] - rX_Target[3,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[3] * (rX_Pred_Horizon[3,3] - rX_Target[3,3]) * (rX_Pred_Horizon[3,3] - rX_Target[3,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[4] * (rX_Pred_Horizon[3,4] - rX_Target[3,4]) * (rX_Pred_Horizon[3,4] - rX_Target[3,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[5] * (rX_Pred_Horizon[3,5] - rX_Target[3,5]) * (rX_Pred_Horizon[3,5] - rX_Target[3,5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[6] * (rX_Pred_Horizon[3,6] - rX_Target[3,6]) * (rX_Pred_Horizon[3,6] - rX_Target[3,6]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[1] * (rX_Pred_Horizon[4,1] - rX_Target[4,1]) * (rX_Pred_Horizon[4,1] - rX_Target[4,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[2] * (rX_Pred_Horizon[4,2] - rX_Target[4,2]) * (rX_Pred_Horizon[4,2] - rX_Target[4,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[3] * (rX_Pred_Horizon[4,3] - rX_Target[4,3]) * (rX_Pred_Horizon[4,3] - rX_Target[4,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[4] * (rX_Pred_Horizon[4,4] - rX_Target[4,4]) * (rX_Pred_Horizon[4,4] - rX_Target[4,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[5] * (rX_Pred_Horizon[4,5] - rX_Target[4,5]) * (rX_Pred_Horizon[4,5] - rX_Target[4,5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[6] * (rX_Pred_Horizon[4,6] - rX_Target[4,6]) * (rX_Pred_Horizon[4,6] - rX_Target[4,6]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[1] * (rX_Pred_Horizon[5,1] - rX_Target[5,1]) * (rX_Pred_Horizon[5,1] - rX_Target[5,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[2] * (rX_Pred_Horizon[5,2] - rX_Target[5,2]) * (rX_Pred_Horizon[5,2] - rX_Target[5,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[3] * (rX_Pred_Horizon[5,3] - rX_Target[5,3]) * (rX_Pred_Horizon[5,3] - rX_Target[5,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[4] * (rX_Pred_Horizon[5,4] - rX_Target[5,4]) * (rX_Pred_Horizon[5,4] - rX_Target[5,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[5] * (rX_Pred_Horizon[5,5] - rX_Target[5,5]) * (rX_Pred_Horizon[5,5] - rX_Target[5,5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[6] * (rX_Pred_Horizon[5,6] - rX_Target[5,6]) * (rX_Pred_Horizon[5,6] - rX_Target[5,6]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rP_Diag[1] * (rX_Pred_Horizon[5,1] - rX_Target[5,1]) * (rX_Pred_Horizon[5,1] - rX_Target[5,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rP_Diag[2] * (rX_Pred_Horizon[5,2] - rX_Target[5,2]) * (rX_Pred_Horizon[5,2] - rX_Target[5,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rP_Diag[3] * (rX_Pred_Horizon[5,3] - rX_Target[5,3]) * (rX_Pred_Horizon[5,3] - rX_Target[5,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rP_Diag[4] * (rX_Pred_Horizon[5,4] - rX_Target[5,4]) * (rX_Pred_Horizon[5,4] - rX_Target[5,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rP_Diag[5] * (rX_Pred_Horizon[5,5] - rX_Target[5,5]) * (rX_Pred_Horizon[5,5] - rX_Target[5,5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rP_Diag[6] * (rX_Pred_Horizon[5,6] - rX_Target[5,6]) * (rX_Pred_Horizon[5,6] - rX_Target[5,6]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[1] * rU_Opt_Seq[1,1] * rU_Opt_Seq[1,1]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[2] * rU_Opt_Seq[1,2] * rU_Opt_Seq[1,2]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[3] * rU_Opt_Seq[1,3] * rU_Opt_Seq[1,3]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[4] * rU_Opt_Seq[1,4] * rU_Opt_Seq[1,4]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[5] * rU_Opt_Seq[1,5] * rU_Opt_Seq[1,5]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[1] * rU_Opt_Seq[2,1] * rU_Opt_Seq[2,1]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[2] * rU_Opt_Seq[2,2] * rU_Opt_Seq[2,2]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[3] * rU_Opt_Seq[2,3] * rU_Opt_Seq[2,3]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[4] * rU_Opt_Seq[2,4] * rU_Opt_Seq[2,4]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[5] * rU_Opt_Seq[2,5] * rU_Opt_Seq[2,5]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[1] * rU_Opt_Seq[3,1] * rU_Opt_Seq[3,1]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[2] * rU_Opt_Seq[3,2] * rU_Opt_Seq[3,2]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[3] * rU_Opt_Seq[3,3] * rU_Opt_Seq[3,3]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[4] * rU_Opt_Seq[3,4] * rU_Opt_Seq[3,4]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[5] * rU_Opt_Seq[3,5] * rU_Opt_Seq[3,5]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[1] * (rU_Opt_Seq[1,1] - a_u_prev[1]) * (rU_Opt_Seq[1,1] - a_u_prev[1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[1] * (rU_Opt_Seq[2,1] - rU_Opt_Seq[1,1]) * (rU_Opt_Seq[2,1] - rU_Opt_Seq[1,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[1] * (rU_Opt_Seq[3,1] - rU_Opt_Seq[2,1]) * (rU_Opt_Seq[3,1] - rU_Opt_Seq[2,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[2] * (rU_Opt_Seq[1,2] - a_u_prev[2]) * (rU_Opt_Seq[1,2] - a_u_prev[2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[2] * (rU_Opt_Seq[2,2] - rU_Opt_Seq[1,2]) * (rU_Opt_Seq[2,2] - rU_Opt_Seq[1,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[2] * (rU_Opt_Seq[3,2] - rU_Opt_Seq[2,2]) * (rU_Opt_Seq[3,2] - rU_Opt_Seq[2,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[3] * (rU_Opt_Seq[1,3] - a_u_prev[3]) * (rU_Opt_Seq[1,3] - a_u_prev[3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[3] * (rU_Opt_Seq[2,3] - rU_Opt_Seq[1,3]) * (rU_Opt_Seq[2,3] - rU_Opt_Seq[1,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[3] * (rU_Opt_Seq[3,3] - rU_Opt_Seq[2,3]) * (rU_Opt_Seq[3,3] - rU_Opt_Seq[2,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[4] * (rU_Opt_Seq[1,4] - a_u_prev[4]) * (rU_Opt_Seq[1,4] - a_u_prev[4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[4] * (rU_Opt_Seq[2,4] - rU_Opt_Seq[1,4]) * (rU_Opt_Seq[2,4] - rU_Opt_Seq[1,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[4] * (rU_Opt_Seq[3,4] - rU_Opt_Seq[2,4]) * (rU_Opt_Seq[3,4] - rU_Opt_Seq[2,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[5] * (rU_Opt_Seq[1,5] - a_u_prev[5]) * (rU_Opt_Seq[1,5] - a_u_prev[5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[5] * (rU_Opt_Seq[2,5] - rU_Opt_Seq[1,5]) * (rU_Opt_Seq[2,5] - rU_Opt_Seq[1,5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[5] * (rU_Opt_Seq[3,5] - rU_Opt_Seq[2,5]) * (rU_Opt_Seq[3,5] - rU_Opt_Seq[2,5]));

(* Iteration 4 - Backward Adjoint Costate Propagation: lambda_h = A^T * lambda_{h+1} + Q * (x_h - x_ref) *)
(* Terminal Costate at h=5: lambda_5 = (P + Q) * (x_5 - x_target_5) *)
rLambda_Costate[5, 1] := (rP_Diag[1] + rQ_Diag[1]) * (rX_Pred_Horizon[5,1] - rX_Target[5,1]);
rLambda_Costate[5, 2] := (rP_Diag[2] + rQ_Diag[2]) * (rX_Pred_Horizon[5,2] - rX_Target[5,2]);
rLambda_Costate[5, 3] := (rP_Diag[3] + rQ_Diag[3]) * (rX_Pred_Horizon[5,3] - rX_Target[5,3]);
rLambda_Costate[5, 4] := (rP_Diag[4] + rQ_Diag[4]) * (rX_Pred_Horizon[5,4] - rX_Target[5,4]);
rLambda_Costate[5, 5] := (rP_Diag[5] + rQ_Diag[5]) * (rX_Pred_Horizon[5,5] - rX_Target[5,5]);
rLambda_Costate[5, 6] := (rP_Diag[6] + rQ_Diag[6]) * (rX_Pred_Horizon[5,6] - rX_Target[5,6]);

(* Adjoint Costate at h=4: lambda_4 = A^T * lambda_5 + Q * (x_4 - x_target_4) *)
rLambda_Costate[4, 1] := (rA_Mat[1,1] * rLambda_Costate[5,1]) + (rA_Mat[2,1] * rLambda_Costate[5,2]) + (rA_Mat[3,1] * rLambda_Costate[5,3]) + (rA_Mat[4,1] * rLambda_Costate[5,4]) + (rA_Mat[5,1] * rLambda_Costate[5,5]) + (rA_Mat[6,1] * rLambda_Costate[5,6]) + (rQ_Diag[1] * (rX_Pred_Horizon[4,1] - rX_Target[4,1]));
rLambda_Costate[4, 2] := (rA_Mat[1,2] * rLambda_Costate[5,1]) + (rA_Mat[2,2] * rLambda_Costate[5,2]) + (rA_Mat[3,2] * rLambda_Costate[5,3]) + (rA_Mat[4,2] * rLambda_Costate[5,4]) + (rA_Mat[5,2] * rLambda_Costate[5,5]) + (rA_Mat[6,2] * rLambda_Costate[5,6]) + (rQ_Diag[2] * (rX_Pred_Horizon[4,2] - rX_Target[4,2]));
rLambda_Costate[4, 3] := (rA_Mat[1,3] * rLambda_Costate[5,1]) + (rA_Mat[2,3] * rLambda_Costate[5,2]) + (rA_Mat[3,3] * rLambda_Costate[5,3]) + (rA_Mat[4,3] * rLambda_Costate[5,4]) + (rA_Mat[5,3] * rLambda_Costate[5,5]) + (rA_Mat[6,3] * rLambda_Costate[5,6]) + (rQ_Diag[3] * (rX_Pred_Horizon[4,3] - rX_Target[4,3]));
rLambda_Costate[4, 4] := (rA_Mat[1,4] * rLambda_Costate[5,1]) + (rA_Mat[2,4] * rLambda_Costate[5,2]) + (rA_Mat[3,4] * rLambda_Costate[5,3]) + (rA_Mat[4,4] * rLambda_Costate[5,4]) + (rA_Mat[5,4] * rLambda_Costate[5,5]) + (rA_Mat[6,4] * rLambda_Costate[5,6]) + (rQ_Diag[4] * (rX_Pred_Horizon[4,4] - rX_Target[4,4]));
rLambda_Costate[4, 5] := (rA_Mat[1,5] * rLambda_Costate[5,1]) + (rA_Mat[2,5] * rLambda_Costate[5,2]) + (rA_Mat[3,5] * rLambda_Costate[5,3]) + (rA_Mat[4,5] * rLambda_Costate[5,4]) + (rA_Mat[5,5] * rLambda_Costate[5,5]) + (rA_Mat[6,5] * rLambda_Costate[5,6]) + (rQ_Diag[5] * (rX_Pred_Horizon[4,5] - rX_Target[4,5]));
rLambda_Costate[4, 6] := (rA_Mat[1,6] * rLambda_Costate[5,1]) + (rA_Mat[2,6] * rLambda_Costate[5,2]) + (rA_Mat[3,6] * rLambda_Costate[5,3]) + (rA_Mat[4,6] * rLambda_Costate[5,4]) + (rA_Mat[5,6] * rLambda_Costate[5,5]) + (rA_Mat[6,6] * rLambda_Costate[5,6]) + (rQ_Diag[6] * (rX_Pred_Horizon[4,6] - rX_Target[4,6]));

(* Adjoint Costate at h=3: lambda_3 = A^T * lambda_4 + Q * (x_3 - x_target_3) *)
rLambda_Costate[3, 1] := (rA_Mat[1,1] * rLambda_Costate[4,1]) + (rA_Mat[2,1] * rLambda_Costate[4,2]) + (rA_Mat[3,1] * rLambda_Costate[4,3]) + (rA_Mat[4,1] * rLambda_Costate[4,4]) + (rA_Mat[5,1] * rLambda_Costate[4,5]) + (rA_Mat[6,1] * rLambda_Costate[4,6]) + (rQ_Diag[1] * (rX_Pred_Horizon[3,1] - rX_Target[3,1]));
rLambda_Costate[3, 2] := (rA_Mat[1,2] * rLambda_Costate[4,1]) + (rA_Mat[2,2] * rLambda_Costate[4,2]) + (rA_Mat[3,2] * rLambda_Costate[4,3]) + (rA_Mat[4,2] * rLambda_Costate[4,4]) + (rA_Mat[5,2] * rLambda_Costate[4,5]) + (rA_Mat[6,2] * rLambda_Costate[4,6]) + (rQ_Diag[2] * (rX_Pred_Horizon[3,2] - rX_Target[3,2]));
rLambda_Costate[3, 3] := (rA_Mat[1,3] * rLambda_Costate[4,1]) + (rA_Mat[2,3] * rLambda_Costate[4,2]) + (rA_Mat[3,3] * rLambda_Costate[4,3]) + (rA_Mat[4,3] * rLambda_Costate[4,4]) + (rA_Mat[5,3] * rLambda_Costate[4,5]) + (rA_Mat[6,3] * rLambda_Costate[4,6]) + (rQ_Diag[3] * (rX_Pred_Horizon[3,3] - rX_Target[3,3]));
rLambda_Costate[3, 4] := (rA_Mat[1,4] * rLambda_Costate[4,1]) + (rA_Mat[2,4] * rLambda_Costate[4,2]) + (rA_Mat[3,4] * rLambda_Costate[4,3]) + (rA_Mat[4,4] * rLambda_Costate[4,4]) + (rA_Mat[5,4] * rLambda_Costate[4,5]) + (rA_Mat[6,4] * rLambda_Costate[4,6]) + (rQ_Diag[4] * (rX_Pred_Horizon[3,4] - rX_Target[3,4]));
rLambda_Costate[3, 5] := (rA_Mat[1,5] * rLambda_Costate[4,1]) + (rA_Mat[2,5] * rLambda_Costate[4,2]) + (rA_Mat[3,5] * rLambda_Costate[4,3]) + (rA_Mat[4,5] * rLambda_Costate[4,4]) + (rA_Mat[5,5] * rLambda_Costate[4,5]) + (rA_Mat[6,5] * rLambda_Costate[4,6]) + (rQ_Diag[5] * (rX_Pred_Horizon[3,5] - rX_Target[3,5]));
rLambda_Costate[3, 6] := (rA_Mat[1,6] * rLambda_Costate[4,1]) + (rA_Mat[2,6] * rLambda_Costate[4,2]) + (rA_Mat[3,6] * rLambda_Costate[4,3]) + (rA_Mat[4,6] * rLambda_Costate[4,4]) + (rA_Mat[5,6] * rLambda_Costate[4,5]) + (rA_Mat[6,6] * rLambda_Costate[4,6]) + (rQ_Diag[6] * (rX_Pred_Horizon[3,6] - rX_Target[3,6]));

(* Adjoint Costate at h=2: lambda_2 = A^T * lambda_3 + Q * (x_2 - x_target_2) *)
rLambda_Costate[2, 1] := (rA_Mat[1,1] * rLambda_Costate[3,1]) + (rA_Mat[2,1] * rLambda_Costate[3,2]) + (rA_Mat[3,1] * rLambda_Costate[3,3]) + (rA_Mat[4,1] * rLambda_Costate[3,4]) + (rA_Mat[5,1] * rLambda_Costate[3,5]) + (rA_Mat[6,1] * rLambda_Costate[3,6]) + (rQ_Diag[1] * (rX_Pred_Horizon[2,1] - rX_Target[2,1]));
rLambda_Costate[2, 2] := (rA_Mat[1,2] * rLambda_Costate[3,1]) + (rA_Mat[2,2] * rLambda_Costate[3,2]) + (rA_Mat[3,2] * rLambda_Costate[3,3]) + (rA_Mat[4,2] * rLambda_Costate[3,4]) + (rA_Mat[5,2] * rLambda_Costate[3,5]) + (rA_Mat[6,2] * rLambda_Costate[3,6]) + (rQ_Diag[2] * (rX_Pred_Horizon[2,2] - rX_Target[2,2]));
rLambda_Costate[2, 3] := (rA_Mat[1,3] * rLambda_Costate[3,1]) + (rA_Mat[2,3] * rLambda_Costate[3,2]) + (rA_Mat[3,3] * rLambda_Costate[3,3]) + (rA_Mat[4,3] * rLambda_Costate[3,4]) + (rA_Mat[5,3] * rLambda_Costate[3,5]) + (rA_Mat[6,3] * rLambda_Costate[3,6]) + (rQ_Diag[3] * (rX_Pred_Horizon[2,3] - rX_Target[2,3]));
rLambda_Costate[2, 4] := (rA_Mat[1,4] * rLambda_Costate[3,1]) + (rA_Mat[2,4] * rLambda_Costate[3,2]) + (rA_Mat[3,4] * rLambda_Costate[3,3]) + (rA_Mat[4,4] * rLambda_Costate[3,4]) + (rA_Mat[5,4] * rLambda_Costate[3,5]) + (rA_Mat[6,4] * rLambda_Costate[3,6]) + (rQ_Diag[4] * (rX_Pred_Horizon[2,4] - rX_Target[2,4]));
rLambda_Costate[2, 5] := (rA_Mat[1,5] * rLambda_Costate[3,1]) + (rA_Mat[2,5] * rLambda_Costate[3,2]) + (rA_Mat[3,5] * rLambda_Costate[3,3]) + (rA_Mat[4,5] * rLambda_Costate[3,4]) + (rA_Mat[5,5] * rLambda_Costate[3,5]) + (rA_Mat[6,5] * rLambda_Costate[3,6]) + (rQ_Diag[5] * (rX_Pred_Horizon[2,5] - rX_Target[2,5]));
rLambda_Costate[2, 6] := (rA_Mat[1,6] * rLambda_Costate[3,1]) + (rA_Mat[2,6] * rLambda_Costate[3,2]) + (rA_Mat[3,6] * rLambda_Costate[3,3]) + (rA_Mat[4,6] * rLambda_Costate[3,4]) + (rA_Mat[5,6] * rLambda_Costate[3,5]) + (rA_Mat[6,6] * rLambda_Costate[3,6]) + (rQ_Diag[6] * (rX_Pred_Horizon[2,6] - rX_Target[2,6]));

(* Adjoint Costate at h=1: lambda_1 = A^T * lambda_2 + Q * (x_1 - x_target_1) *)
rLambda_Costate[1, 1] := (rA_Mat[1,1] * rLambda_Costate[2,1]) + (rA_Mat[2,1] * rLambda_Costate[2,2]) + (rA_Mat[3,1] * rLambda_Costate[2,3]) + (rA_Mat[4,1] * rLambda_Costate[2,4]) + (rA_Mat[5,1] * rLambda_Costate[2,5]) + (rA_Mat[6,1] * rLambda_Costate[2,6]) + (rQ_Diag[1] * (rX_Pred_Horizon[1,1] - rX_Target[1,1]));
rLambda_Costate[1, 2] := (rA_Mat[1,2] * rLambda_Costate[2,1]) + (rA_Mat[2,2] * rLambda_Costate[2,2]) + (rA_Mat[3,2] * rLambda_Costate[2,3]) + (rA_Mat[4,2] * rLambda_Costate[2,4]) + (rA_Mat[5,2] * rLambda_Costate[2,5]) + (rA_Mat[6,2] * rLambda_Costate[2,6]) + (rQ_Diag[2] * (rX_Pred_Horizon[1,2] - rX_Target[1,2]));
rLambda_Costate[1, 3] := (rA_Mat[1,3] * rLambda_Costate[2,1]) + (rA_Mat[2,3] * rLambda_Costate[2,2]) + (rA_Mat[3,3] * rLambda_Costate[2,3]) + (rA_Mat[4,3] * rLambda_Costate[2,4]) + (rA_Mat[5,3] * rLambda_Costate[2,5]) + (rA_Mat[6,3] * rLambda_Costate[2,6]) + (rQ_Diag[3] * (rX_Pred_Horizon[1,3] - rX_Target[1,3]));
rLambda_Costate[1, 4] := (rA_Mat[1,4] * rLambda_Costate[2,1]) + (rA_Mat[2,4] * rLambda_Costate[2,2]) + (rA_Mat[3,4] * rLambda_Costate[2,3]) + (rA_Mat[4,4] * rLambda_Costate[2,4]) + (rA_Mat[5,4] * rLambda_Costate[2,5]) + (rA_Mat[6,4] * rLambda_Costate[2,6]) + (rQ_Diag[4] * (rX_Pred_Horizon[1,4] - rX_Target[1,4]));
rLambda_Costate[1, 5] := (rA_Mat[1,5] * rLambda_Costate[2,1]) + (rA_Mat[2,5] * rLambda_Costate[2,2]) + (rA_Mat[3,5] * rLambda_Costate[2,3]) + (rA_Mat[4,5] * rLambda_Costate[2,4]) + (rA_Mat[5,5] * rLambda_Costate[2,5]) + (rA_Mat[6,5] * rLambda_Costate[2,6]) + (rQ_Diag[5] * (rX_Pred_Horizon[1,5] - rX_Target[1,5]));
rLambda_Costate[1, 6] := (rA_Mat[1,6] * rLambda_Costate[2,1]) + (rA_Mat[2,6] * rLambda_Costate[2,2]) + (rA_Mat[3,6] * rLambda_Costate[2,3]) + (rA_Mat[4,6] * rLambda_Costate[2,4]) + (rA_Mat[5,6] * rLambda_Costate[2,5]) + (rA_Mat[6,6] * rLambda_Costate[2,6]) + (rQ_Diag[6] * (rX_Pred_Horizon[1,6] - rX_Target[1,6]));

(* Iteration 4 - Analytical Gradient Computation w.r.t. Control Inputs u_h *)
rMPC_GradNormSq := 0.0;
(* Gradient for u_1 (h=1) *)
rGrad_J[1, 1] := (rB_Mat[1,1] * rLambda_Costate[1,1]) + (rB_Mat[2,1] * rLambda_Costate[1,2]) + (rB_Mat[3,1] * rLambda_Costate[1,3]) + (rB_Mat[4,1] * rLambda_Costate[1,4]) + (rB_Mat[5,1] * rLambda_Costate[1,5]) + (rB_Mat[6,1] * rLambda_Costate[1,6]) + (rR_Diag[1] * rU_Opt_Seq[1,1]) + (rS_Diag[1] * (rU_Opt_Seq[1,1] - a_u_prev[1])) - (rS_Diag[1] * (rU_Opt_Seq[2,1] - rU_Opt_Seq[1,1]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[1, 1] * rGrad_J[1, 1]);
rGrad_J[1, 2] := (rB_Mat[1,2] * rLambda_Costate[1,1]) + (rB_Mat[2,2] * rLambda_Costate[1,2]) + (rB_Mat[3,2] * rLambda_Costate[1,3]) + (rB_Mat[4,2] * rLambda_Costate[1,4]) + (rB_Mat[5,2] * rLambda_Costate[1,5]) + (rB_Mat[6,2] * rLambda_Costate[1,6]) + (rR_Diag[2] * rU_Opt_Seq[1,2]) + (rS_Diag[2] * (rU_Opt_Seq[1,2] - a_u_prev[2])) - (rS_Diag[2] * (rU_Opt_Seq[2,2] - rU_Opt_Seq[1,2]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[1, 2] * rGrad_J[1, 2]);
rGrad_J[1, 3] := (rB_Mat[1,3] * rLambda_Costate[1,1]) + (rB_Mat[2,3] * rLambda_Costate[1,2]) + (rB_Mat[3,3] * rLambda_Costate[1,3]) + (rB_Mat[4,3] * rLambda_Costate[1,4]) + (rB_Mat[5,3] * rLambda_Costate[1,5]) + (rB_Mat[6,3] * rLambda_Costate[1,6]) + (rR_Diag[3] * rU_Opt_Seq[1,3]) + (rS_Diag[3] * (rU_Opt_Seq[1,3] - a_u_prev[3])) - (rS_Diag[3] * (rU_Opt_Seq[2,3] - rU_Opt_Seq[1,3]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[1, 3] * rGrad_J[1, 3]);
rGrad_J[1, 4] := (rB_Mat[1,4] * rLambda_Costate[1,1]) + (rB_Mat[2,4] * rLambda_Costate[1,2]) + (rB_Mat[3,4] * rLambda_Costate[1,3]) + (rB_Mat[4,4] * rLambda_Costate[1,4]) + (rB_Mat[5,4] * rLambda_Costate[1,5]) + (rB_Mat[6,4] * rLambda_Costate[1,6]) + (rR_Diag[4] * rU_Opt_Seq[1,4]) + (rS_Diag[4] * (rU_Opt_Seq[1,4] - a_u_prev[4])) - (rS_Diag[4] * (rU_Opt_Seq[2,4] - rU_Opt_Seq[1,4]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[1, 4] * rGrad_J[1, 4]);
rGrad_J[1, 5] := (rB_Mat[1,5] * rLambda_Costate[1,1]) + (rB_Mat[2,5] * rLambda_Costate[1,2]) + (rB_Mat[3,5] * rLambda_Costate[1,3]) + (rB_Mat[4,5] * rLambda_Costate[1,4]) + (rB_Mat[5,5] * rLambda_Costate[1,5]) + (rB_Mat[6,5] * rLambda_Costate[1,6]) + (rR_Diag[5] * rU_Opt_Seq[1,5]) + (rS_Diag[5] * (rU_Opt_Seq[1,5] - a_u_prev[5])) - (rS_Diag[5] * (rU_Opt_Seq[2,5] - rU_Opt_Seq[1,5]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[1, 5] * rGrad_J[1, 5]);

(* Gradient for u_2 (h=2) *)
rGrad_J[2, 1] := (rB_Mat[1,1] * rLambda_Costate[2,1]) + (rB_Mat[2,1] * rLambda_Costate[2,2]) + (rB_Mat[3,1] * rLambda_Costate[2,3]) + (rB_Mat[4,1] * rLambda_Costate[2,4]) + (rB_Mat[5,1] * rLambda_Costate[2,5]) + (rB_Mat[6,1] * rLambda_Costate[2,6]) + (rR_Diag[1] * rU_Opt_Seq[2,1]) + (rS_Diag[1] * (rU_Opt_Seq[2,1] - rU_Opt_Seq[1,1])) - (rS_Diag[1] * (rU_Opt_Seq[3,1] - rU_Opt_Seq[2,1]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[2, 1] * rGrad_J[2, 1]);
rGrad_J[2, 2] := (rB_Mat[1,2] * rLambda_Costate[2,1]) + (rB_Mat[2,2] * rLambda_Costate[2,2]) + (rB_Mat[3,2] * rLambda_Costate[2,3]) + (rB_Mat[4,2] * rLambda_Costate[2,4]) + (rB_Mat[5,2] * rLambda_Costate[2,5]) + (rB_Mat[6,2] * rLambda_Costate[2,6]) + (rR_Diag[2] * rU_Opt_Seq[2,2]) + (rS_Diag[2] * (rU_Opt_Seq[2,2] - rU_Opt_Seq[1,2])) - (rS_Diag[2] * (rU_Opt_Seq[3,2] - rU_Opt_Seq[2,2]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[2, 2] * rGrad_J[2, 2]);
rGrad_J[2, 3] := (rB_Mat[1,3] * rLambda_Costate[2,1]) + (rB_Mat[2,3] * rLambda_Costate[2,2]) + (rB_Mat[3,3] * rLambda_Costate[2,3]) + (rB_Mat[4,3] * rLambda_Costate[2,4]) + (rB_Mat[5,3] * rLambda_Costate[2,5]) + (rB_Mat[6,3] * rLambda_Costate[2,6]) + (rR_Diag[3] * rU_Opt_Seq[2,3]) + (rS_Diag[3] * (rU_Opt_Seq[2,3] - rU_Opt_Seq[1,3])) - (rS_Diag[3] * (rU_Opt_Seq[3,3] - rU_Opt_Seq[2,3]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[2, 3] * rGrad_J[2, 3]);
rGrad_J[2, 4] := (rB_Mat[1,4] * rLambda_Costate[2,1]) + (rB_Mat[2,4] * rLambda_Costate[2,2]) + (rB_Mat[3,4] * rLambda_Costate[2,3]) + (rB_Mat[4,4] * rLambda_Costate[2,4]) + (rB_Mat[5,4] * rLambda_Costate[2,5]) + (rB_Mat[6,4] * rLambda_Costate[2,6]) + (rR_Diag[4] * rU_Opt_Seq[2,4]) + (rS_Diag[4] * (rU_Opt_Seq[2,4] - rU_Opt_Seq[1,4])) - (rS_Diag[4] * (rU_Opt_Seq[3,4] - rU_Opt_Seq[2,4]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[2, 4] * rGrad_J[2, 4]);
rGrad_J[2, 5] := (rB_Mat[1,5] * rLambda_Costate[2,1]) + (rB_Mat[2,5] * rLambda_Costate[2,2]) + (rB_Mat[3,5] * rLambda_Costate[2,3]) + (rB_Mat[4,5] * rLambda_Costate[2,4]) + (rB_Mat[5,5] * rLambda_Costate[2,5]) + (rB_Mat[6,5] * rLambda_Costate[2,6]) + (rR_Diag[5] * rU_Opt_Seq[2,5]) + (rS_Diag[5] * (rU_Opt_Seq[2,5] - rU_Opt_Seq[1,5])) - (rS_Diag[5] * (rU_Opt_Seq[3,5] - rU_Opt_Seq[2,5]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[2, 5] * rGrad_J[2, 5]);

(* Gradient for u_3 (h=3, held through h=4, 5) *)
rGrad_J[3, 1] := (rB_Mat[1,1] * (rLambda_Costate[3,1] + rLambda_Costate[4,1] + rLambda_Costate[5,1])) + (rB_Mat[2,1] * (rLambda_Costate[3,2] + rLambda_Costate[4,2] + rLambda_Costate[5,2])) + (rB_Mat[3,1] * (rLambda_Costate[3,3] + rLambda_Costate[4,3] + rLambda_Costate[5,3])) + (rB_Mat[4,1] * (rLambda_Costate[3,4] + rLambda_Costate[4,4] + rLambda_Costate[5,4])) + (rB_Mat[5,1] * (rLambda_Costate[3,5] + rLambda_Costate[4,5] + rLambda_Costate[5,5])) + (rB_Mat[6,1] * (rLambda_Costate[3,6] + rLambda_Costate[4,6] + rLambda_Costate[5,6])) + (rR_Diag[1] * rU_Opt_Seq[3,1]) + (rS_Diag[1] * (rU_Opt_Seq[3,1] - rU_Opt_Seq[2,1]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[3, 1] * rGrad_J[3, 1]);
rGrad_J[3, 2] := (rB_Mat[1,2] * (rLambda_Costate[3,1] + rLambda_Costate[4,1] + rLambda_Costate[5,1])) + (rB_Mat[2,2] * (rLambda_Costate[3,2] + rLambda_Costate[4,2] + rLambda_Costate[5,2])) + (rB_Mat[3,2] * (rLambda_Costate[3,3] + rLambda_Costate[4,3] + rLambda_Costate[5,3])) + (rB_Mat[4,2] * (rLambda_Costate[3,4] + rLambda_Costate[4,4] + rLambda_Costate[5,4])) + (rB_Mat[5,2] * (rLambda_Costate[3,5] + rLambda_Costate[4,5] + rLambda_Costate[5,5])) + (rB_Mat[6,2] * (rLambda_Costate[3,6] + rLambda_Costate[4,6] + rLambda_Costate[5,6])) + (rR_Diag[2] * rU_Opt_Seq[3,2]) + (rS_Diag[2] * (rU_Opt_Seq[3,2] - rU_Opt_Seq[2,2]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[3, 2] * rGrad_J[3, 2]);
rGrad_J[3, 3] := (rB_Mat[1,3] * (rLambda_Costate[3,1] + rLambda_Costate[4,1] + rLambda_Costate[5,1])) + (rB_Mat[2,3] * (rLambda_Costate[3,2] + rLambda_Costate[4,2] + rLambda_Costate[5,2])) + (rB_Mat[3,3] * (rLambda_Costate[3,3] + rLambda_Costate[4,3] + rLambda_Costate[5,3])) + (rB_Mat[4,3] * (rLambda_Costate[3,4] + rLambda_Costate[4,4] + rLambda_Costate[5,4])) + (rB_Mat[5,3] * (rLambda_Costate[3,5] + rLambda_Costate[4,5] + rLambda_Costate[5,5])) + (rB_Mat[6,3] * (rLambda_Costate[3,6] + rLambda_Costate[4,6] + rLambda_Costate[5,6])) + (rR_Diag[3] * rU_Opt_Seq[3,3]) + (rS_Diag[3] * (rU_Opt_Seq[3,3] - rU_Opt_Seq[2,3]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[3, 3] * rGrad_J[3, 3]);
rGrad_J[3, 4] := (rB_Mat[1,4] * (rLambda_Costate[3,1] + rLambda_Costate[4,1] + rLambda_Costate[5,1])) + (rB_Mat[2,4] * (rLambda_Costate[3,2] + rLambda_Costate[4,2] + rLambda_Costate[5,2])) + (rB_Mat[3,4] * (rLambda_Costate[3,3] + rLambda_Costate[4,3] + rLambda_Costate[5,3])) + (rB_Mat[4,4] * (rLambda_Costate[3,4] + rLambda_Costate[4,4] + rLambda_Costate[5,4])) + (rB_Mat[5,4] * (rLambda_Costate[3,5] + rLambda_Costate[4,5] + rLambda_Costate[5,5])) + (rB_Mat[6,4] * (rLambda_Costate[3,6] + rLambda_Costate[4,6] + rLambda_Costate[5,6])) + (rR_Diag[4] * rU_Opt_Seq[3,4]) + (rS_Diag[4] * (rU_Opt_Seq[3,4] - rU_Opt_Seq[2,4]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[3, 4] * rGrad_J[3, 4]);
rGrad_J[3, 5] := (rB_Mat[1,5] * (rLambda_Costate[3,1] + rLambda_Costate[4,1] + rLambda_Costate[5,1])) + (rB_Mat[2,5] * (rLambda_Costate[3,2] + rLambda_Costate[4,2] + rLambda_Costate[5,2])) + (rB_Mat[3,5] * (rLambda_Costate[3,3] + rLambda_Costate[4,3] + rLambda_Costate[5,3])) + (rB_Mat[4,5] * (rLambda_Costate[3,4] + rLambda_Costate[4,4] + rLambda_Costate[5,4])) + (rB_Mat[5,5] * (rLambda_Costate[3,5] + rLambda_Costate[4,5] + rLambda_Costate[5,5])) + (rB_Mat[6,5] * (rLambda_Costate[3,6] + rLambda_Costate[4,6] + rLambda_Costate[5,6])) + (rR_Diag[5] * rU_Opt_Seq[3,5]) + (rS_Diag[5] * (rU_Opt_Seq[3,5] - rU_Opt_Seq[2,5]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[3, 5] * rGrad_J[3, 5]);

(* Iteration 4 - Projected Gradient Step with Hard Box & Dynamic Slew Limits *)
rTemp_Val := rU_Opt_Seq[1, 1] - (rAlpha_PGD_StepSize * rGrad_J[1, 1]);
(* Slew limit against prior actuator output *)
IF rTemp_Val > (a_u_prev[1] + rDeltaU_Max[1]) THEN
    rTemp_Val := a_u_prev[1] + rDeltaU_Max[1];
ELSIF rTemp_Val < (a_u_prev[1] - rDeltaU_Max[1]) THEN
    rTemp_Val := a_u_prev[1] - rDeltaU_Max[1];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[1] THEN
    rTemp_Val := rU_BoxMax[1];
ELSIF rTemp_Val < rU_BoxMin[1] THEN
    rTemp_Val := rU_BoxMin[1];
END_IF;
rU_Opt_Seq[1, 1] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[1, 2] - (rAlpha_PGD_StepSize * rGrad_J[1, 2]);
(* Slew limit against prior actuator output *)
IF rTemp_Val > (a_u_prev[2] + rDeltaU_Max[2]) THEN
    rTemp_Val := a_u_prev[2] + rDeltaU_Max[2];
ELSIF rTemp_Val < (a_u_prev[2] - rDeltaU_Max[2]) THEN
    rTemp_Val := a_u_prev[2] - rDeltaU_Max[2];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[2] THEN
    rTemp_Val := rU_BoxMax[2];
ELSIF rTemp_Val < rU_BoxMin[2] THEN
    rTemp_Val := rU_BoxMin[2];
END_IF;
rU_Opt_Seq[1, 2] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[1, 3] - (rAlpha_PGD_StepSize * rGrad_J[1, 3]);
(* Slew limit against prior actuator output *)
IF rTemp_Val > (a_u_prev[3] + rDeltaU_Max[3]) THEN
    rTemp_Val := a_u_prev[3] + rDeltaU_Max[3];
ELSIF rTemp_Val < (a_u_prev[3] - rDeltaU_Max[3]) THEN
    rTemp_Val := a_u_prev[3] - rDeltaU_Max[3];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[3] THEN
    rTemp_Val := rU_BoxMax[3];
ELSIF rTemp_Val < rU_BoxMin[3] THEN
    rTemp_Val := rU_BoxMin[3];
END_IF;
rU_Opt_Seq[1, 3] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[1, 4] - (rAlpha_PGD_StepSize * rGrad_J[1, 4]);
(* Slew limit against prior actuator output *)
IF rTemp_Val > (a_u_prev[4] + rDeltaU_Max[4]) THEN
    rTemp_Val := a_u_prev[4] + rDeltaU_Max[4];
ELSIF rTemp_Val < (a_u_prev[4] - rDeltaU_Max[4]) THEN
    rTemp_Val := a_u_prev[4] - rDeltaU_Max[4];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[4] THEN
    rTemp_Val := rU_BoxMax[4];
ELSIF rTemp_Val < rU_BoxMin[4] THEN
    rTemp_Val := rU_BoxMin[4];
END_IF;
rU_Opt_Seq[1, 4] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[1, 5] - (rAlpha_PGD_StepSize * rGrad_J[1, 5]);
(* Slew limit against prior actuator output *)
IF rTemp_Val > (a_u_prev[5] + rDeltaU_Max[5]) THEN
    rTemp_Val := a_u_prev[5] + rDeltaU_Max[5];
ELSIF rTemp_Val < (a_u_prev[5] - rDeltaU_Max[5]) THEN
    rTemp_Val := a_u_prev[5] - rDeltaU_Max[5];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[5] THEN
    rTemp_Val := rU_BoxMax[5];
ELSIF rTemp_Val < rU_BoxMin[5] THEN
    rTemp_Val := rU_BoxMin[5];
END_IF;
rU_Opt_Seq[1, 5] := rTemp_Val;

rTemp_Val := rU_Opt_Seq[2, 1] - (rAlpha_PGD_StepSize * rGrad_J[2, 1]);
(* Slew limit against step 1 *)
IF rTemp_Val > (rU_Opt_Seq[1, 1] + rDeltaU_Max[1]) THEN
    rTemp_Val := rU_Opt_Seq[1, 1] + rDeltaU_Max[1];
ELSIF rTemp_Val < (rU_Opt_Seq[1, 1] - rDeltaU_Max[1]) THEN
    rTemp_Val := rU_Opt_Seq[1, 1] - rDeltaU_Max[1];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[1] THEN
    rTemp_Val := rU_BoxMax[1];
ELSIF rTemp_Val < rU_BoxMin[1] THEN
    rTemp_Val := rU_BoxMin[1];
END_IF;
rU_Opt_Seq[2, 1] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[2, 2] - (rAlpha_PGD_StepSize * rGrad_J[2, 2]);
(* Slew limit against step 1 *)
IF rTemp_Val > (rU_Opt_Seq[1, 2] + rDeltaU_Max[2]) THEN
    rTemp_Val := rU_Opt_Seq[1, 2] + rDeltaU_Max[2];
ELSIF rTemp_Val < (rU_Opt_Seq[1, 2] - rDeltaU_Max[2]) THEN
    rTemp_Val := rU_Opt_Seq[1, 2] - rDeltaU_Max[2];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[2] THEN
    rTemp_Val := rU_BoxMax[2];
ELSIF rTemp_Val < rU_BoxMin[2] THEN
    rTemp_Val := rU_BoxMin[2];
END_IF;
rU_Opt_Seq[2, 2] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[2, 3] - (rAlpha_PGD_StepSize * rGrad_J[2, 3]);
(* Slew limit against step 1 *)
IF rTemp_Val > (rU_Opt_Seq[1, 3] + rDeltaU_Max[3]) THEN
    rTemp_Val := rU_Opt_Seq[1, 3] + rDeltaU_Max[3];
ELSIF rTemp_Val < (rU_Opt_Seq[1, 3] - rDeltaU_Max[3]) THEN
    rTemp_Val := rU_Opt_Seq[1, 3] - rDeltaU_Max[3];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[3] THEN
    rTemp_Val := rU_BoxMax[3];
ELSIF rTemp_Val < rU_BoxMin[3] THEN
    rTemp_Val := rU_BoxMin[3];
END_IF;
rU_Opt_Seq[2, 3] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[2, 4] - (rAlpha_PGD_StepSize * rGrad_J[2, 4]);
(* Slew limit against step 1 *)
IF rTemp_Val > (rU_Opt_Seq[1, 4] + rDeltaU_Max[4]) THEN
    rTemp_Val := rU_Opt_Seq[1, 4] + rDeltaU_Max[4];
ELSIF rTemp_Val < (rU_Opt_Seq[1, 4] - rDeltaU_Max[4]) THEN
    rTemp_Val := rU_Opt_Seq[1, 4] - rDeltaU_Max[4];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[4] THEN
    rTemp_Val := rU_BoxMax[4];
ELSIF rTemp_Val < rU_BoxMin[4] THEN
    rTemp_Val := rU_BoxMin[4];
END_IF;
rU_Opt_Seq[2, 4] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[2, 5] - (rAlpha_PGD_StepSize * rGrad_J[2, 5]);
(* Slew limit against step 1 *)
IF rTemp_Val > (rU_Opt_Seq[1, 5] + rDeltaU_Max[5]) THEN
    rTemp_Val := rU_Opt_Seq[1, 5] + rDeltaU_Max[5];
ELSIF rTemp_Val < (rU_Opt_Seq[1, 5] - rDeltaU_Max[5]) THEN
    rTemp_Val := rU_Opt_Seq[1, 5] - rDeltaU_Max[5];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[5] THEN
    rTemp_Val := rU_BoxMax[5];
ELSIF rTemp_Val < rU_BoxMin[5] THEN
    rTemp_Val := rU_BoxMin[5];
END_IF;
rU_Opt_Seq[2, 5] := rTemp_Val;

rTemp_Val := rU_Opt_Seq[3, 1] - (rAlpha_PGD_StepSize * rGrad_J[3, 1]);
(* Slew limit against step 2 *)
IF rTemp_Val > (rU_Opt_Seq[2, 1] + rDeltaU_Max[1]) THEN
    rTemp_Val := rU_Opt_Seq[2, 1] + rDeltaU_Max[1];
ELSIF rTemp_Val < (rU_Opt_Seq[2, 1] - rDeltaU_Max[1]) THEN
    rTemp_Val := rU_Opt_Seq[2, 1] - rDeltaU_Max[1];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[1] THEN
    rTemp_Val := rU_BoxMax[1];
ELSIF rTemp_Val < rU_BoxMin[1] THEN
    rTemp_Val := rU_BoxMin[1];
END_IF;
rU_Opt_Seq[3, 1] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[3, 2] - (rAlpha_PGD_StepSize * rGrad_J[3, 2]);
(* Slew limit against step 2 *)
IF rTemp_Val > (rU_Opt_Seq[2, 2] + rDeltaU_Max[2]) THEN
    rTemp_Val := rU_Opt_Seq[2, 2] + rDeltaU_Max[2];
ELSIF rTemp_Val < (rU_Opt_Seq[2, 2] - rDeltaU_Max[2]) THEN
    rTemp_Val := rU_Opt_Seq[2, 2] - rDeltaU_Max[2];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[2] THEN
    rTemp_Val := rU_BoxMax[2];
ELSIF rTemp_Val < rU_BoxMin[2] THEN
    rTemp_Val := rU_BoxMin[2];
END_IF;
rU_Opt_Seq[3, 2] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[3, 3] - (rAlpha_PGD_StepSize * rGrad_J[3, 3]);
(* Slew limit against step 2 *)
IF rTemp_Val > (rU_Opt_Seq[2, 3] + rDeltaU_Max[3]) THEN
    rTemp_Val := rU_Opt_Seq[2, 3] + rDeltaU_Max[3];
ELSIF rTemp_Val < (rU_Opt_Seq[2, 3] - rDeltaU_Max[3]) THEN
    rTemp_Val := rU_Opt_Seq[2, 3] - rDeltaU_Max[3];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[3] THEN
    rTemp_Val := rU_BoxMax[3];
ELSIF rTemp_Val < rU_BoxMin[3] THEN
    rTemp_Val := rU_BoxMin[3];
END_IF;
rU_Opt_Seq[3, 3] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[3, 4] - (rAlpha_PGD_StepSize * rGrad_J[3, 4]);
(* Slew limit against step 2 *)
IF rTemp_Val > (rU_Opt_Seq[2, 4] + rDeltaU_Max[4]) THEN
    rTemp_Val := rU_Opt_Seq[2, 4] + rDeltaU_Max[4];
ELSIF rTemp_Val < (rU_Opt_Seq[2, 4] - rDeltaU_Max[4]) THEN
    rTemp_Val := rU_Opt_Seq[2, 4] - rDeltaU_Max[4];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[4] THEN
    rTemp_Val := rU_BoxMax[4];
ELSIF rTemp_Val < rU_BoxMin[4] THEN
    rTemp_Val := rU_BoxMin[4];
END_IF;
rU_Opt_Seq[3, 4] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[3, 5] - (rAlpha_PGD_StepSize * rGrad_J[3, 5]);
(* Slew limit against step 2 *)
IF rTemp_Val > (rU_Opt_Seq[2, 5] + rDeltaU_Max[5]) THEN
    rTemp_Val := rU_Opt_Seq[2, 5] + rDeltaU_Max[5];
ELSIF rTemp_Val < (rU_Opt_Seq[2, 5] - rDeltaU_Max[5]) THEN
    rTemp_Val := rU_Opt_Seq[2, 5] - rDeltaU_Max[5];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[5] THEN
    rTemp_Val := rU_BoxMax[5];
ELSIF rTemp_Val < rU_BoxMin[5] THEN
    rTemp_Val := rU_BoxMin[5];
END_IF;
rU_Opt_Seq[3, 5] := rTemp_Val;

(* ================================================================================================== *)
(* MPC PROJECTED GRADIENT DESCENT -- UNROLLED ITERATION 5 OF 10                                 *)
(* ================================================================================================== *)
iPGD_IterCount := 5;

(* Iteration 5 - Forward State Prediction Step 1 (h=1): x_1 = A * x_hat + B * u_1 *)
rX_Pred_Horizon[1, 1] := (rA_Mat[1,1] * a_x_hat[1]) + (rA_Mat[1,2] * a_x_hat[2]) + (rA_Mat[1,3] * a_x_hat[3]) + (rA_Mat[1,4] * a_x_hat[4]) + (rA_Mat[1,5] * a_x_hat[5]) + (rA_Mat[1,6] * a_x_hat[6]) + (rB_Mat[1,1] * rU_Opt_Seq[1,1]) + (rB_Mat[1,2] * rU_Opt_Seq[1,2]) + (rB_Mat[1,3] * rU_Opt_Seq[1,3]) + (rB_Mat[1,4] * rU_Opt_Seq[1,4]) + (rB_Mat[1,5] * rU_Opt_Seq[1,5]);
rX_Pred_Horizon[1, 2] := (rA_Mat[2,1] * a_x_hat[1]) + (rA_Mat[2,2] * a_x_hat[2]) + (rA_Mat[2,3] * a_x_hat[3]) + (rA_Mat[2,4] * a_x_hat[4]) + (rA_Mat[2,5] * a_x_hat[5]) + (rA_Mat[2,6] * a_x_hat[6]) + (rB_Mat[2,1] * rU_Opt_Seq[1,1]) + (rB_Mat[2,2] * rU_Opt_Seq[1,2]) + (rB_Mat[2,3] * rU_Opt_Seq[1,3]) + (rB_Mat[2,4] * rU_Opt_Seq[1,4]) + (rB_Mat[2,5] * rU_Opt_Seq[1,5]);
rX_Pred_Horizon[1, 3] := (rA_Mat[3,1] * a_x_hat[1]) + (rA_Mat[3,2] * a_x_hat[2]) + (rA_Mat[3,3] * a_x_hat[3]) + (rA_Mat[3,4] * a_x_hat[4]) + (rA_Mat[3,5] * a_x_hat[5]) + (rA_Mat[3,6] * a_x_hat[6]) + (rB_Mat[3,1] * rU_Opt_Seq[1,1]) + (rB_Mat[3,2] * rU_Opt_Seq[1,2]) + (rB_Mat[3,3] * rU_Opt_Seq[1,3]) + (rB_Mat[3,4] * rU_Opt_Seq[1,4]) + (rB_Mat[3,5] * rU_Opt_Seq[1,5]);
rX_Pred_Horizon[1, 4] := (rA_Mat[4,1] * a_x_hat[1]) + (rA_Mat[4,2] * a_x_hat[2]) + (rA_Mat[4,3] * a_x_hat[3]) + (rA_Mat[4,4] * a_x_hat[4]) + (rA_Mat[4,5] * a_x_hat[5]) + (rA_Mat[4,6] * a_x_hat[6]) + (rB_Mat[4,1] * rU_Opt_Seq[1,1]) + (rB_Mat[4,2] * rU_Opt_Seq[1,2]) + (rB_Mat[4,3] * rU_Opt_Seq[1,3]) + (rB_Mat[4,4] * rU_Opt_Seq[1,4]) + (rB_Mat[4,5] * rU_Opt_Seq[1,5]);
rX_Pred_Horizon[1, 5] := (rA_Mat[5,1] * a_x_hat[1]) + (rA_Mat[5,2] * a_x_hat[2]) + (rA_Mat[5,3] * a_x_hat[3]) + (rA_Mat[5,4] * a_x_hat[4]) + (rA_Mat[5,5] * a_x_hat[5]) + (rA_Mat[5,6] * a_x_hat[6]) + (rB_Mat[5,1] * rU_Opt_Seq[1,1]) + (rB_Mat[5,2] * rU_Opt_Seq[1,2]) + (rB_Mat[5,3] * rU_Opt_Seq[1,3]) + (rB_Mat[5,4] * rU_Opt_Seq[1,4]) + (rB_Mat[5,5] * rU_Opt_Seq[1,5]);
rX_Pred_Horizon[1, 6] := (rA_Mat[6,1] * a_x_hat[1]) + (rA_Mat[6,2] * a_x_hat[2]) + (rA_Mat[6,3] * a_x_hat[3]) + (rA_Mat[6,4] * a_x_hat[4]) + (rA_Mat[6,5] * a_x_hat[5]) + (rA_Mat[6,6] * a_x_hat[6]) + (rB_Mat[6,1] * rU_Opt_Seq[1,1]) + (rB_Mat[6,2] * rU_Opt_Seq[1,2]) + (rB_Mat[6,3] * rU_Opt_Seq[1,3]) + (rB_Mat[6,4] * rU_Opt_Seq[1,4]) + (rB_Mat[6,5] * rU_Opt_Seq[1,5]);

(* Iteration 5 - Forward State Prediction Step 2 (h=2): x_2 = A * x_1 + B * u_2 *)
rX_Pred_Horizon[2, 1] := (rA_Mat[1,1] * rX_Pred_Horizon[1,1]) + (rA_Mat[1,2] * rX_Pred_Horizon[1,2]) + (rA_Mat[1,3] * rX_Pred_Horizon[1,3]) + (rA_Mat[1,4] * rX_Pred_Horizon[1,4]) + (rA_Mat[1,5] * rX_Pred_Horizon[1,5]) + (rA_Mat[1,6] * rX_Pred_Horizon[1,6]) + (rB_Mat[1,1] * rU_Opt_Seq[2,1]) + (rB_Mat[1,2] * rU_Opt_Seq[2,2]) + (rB_Mat[1,3] * rU_Opt_Seq[2,3]) + (rB_Mat[1,4] * rU_Opt_Seq[2,4]) + (rB_Mat[1,5] * rU_Opt_Seq[2,5]);
rX_Pred_Horizon[2, 2] := (rA_Mat[2,1] * rX_Pred_Horizon[1,1]) + (rA_Mat[2,2] * rX_Pred_Horizon[1,2]) + (rA_Mat[2,3] * rX_Pred_Horizon[1,3]) + (rA_Mat[2,4] * rX_Pred_Horizon[1,4]) + (rA_Mat[2,5] * rX_Pred_Horizon[1,5]) + (rA_Mat[2,6] * rX_Pred_Horizon[1,6]) + (rB_Mat[2,1] * rU_Opt_Seq[2,1]) + (rB_Mat[2,2] * rU_Opt_Seq[2,2]) + (rB_Mat[2,3] * rU_Opt_Seq[2,3]) + (rB_Mat[2,4] * rU_Opt_Seq[2,4]) + (rB_Mat[2,5] * rU_Opt_Seq[2,5]);
rX_Pred_Horizon[2, 3] := (rA_Mat[3,1] * rX_Pred_Horizon[1,1]) + (rA_Mat[3,2] * rX_Pred_Horizon[1,2]) + (rA_Mat[3,3] * rX_Pred_Horizon[1,3]) + (rA_Mat[3,4] * rX_Pred_Horizon[1,4]) + (rA_Mat[3,5] * rX_Pred_Horizon[1,5]) + (rA_Mat[3,6] * rX_Pred_Horizon[1,6]) + (rB_Mat[3,1] * rU_Opt_Seq[2,1]) + (rB_Mat[3,2] * rU_Opt_Seq[2,2]) + (rB_Mat[3,3] * rU_Opt_Seq[2,3]) + (rB_Mat[3,4] * rU_Opt_Seq[2,4]) + (rB_Mat[3,5] * rU_Opt_Seq[2,5]);
rX_Pred_Horizon[2, 4] := (rA_Mat[4,1] * rX_Pred_Horizon[1,1]) + (rA_Mat[4,2] * rX_Pred_Horizon[1,2]) + (rA_Mat[4,3] * rX_Pred_Horizon[1,3]) + (rA_Mat[4,4] * rX_Pred_Horizon[1,4]) + (rA_Mat[4,5] * rX_Pred_Horizon[1,5]) + (rA_Mat[4,6] * rX_Pred_Horizon[1,6]) + (rB_Mat[4,1] * rU_Opt_Seq[2,1]) + (rB_Mat[4,2] * rU_Opt_Seq[2,2]) + (rB_Mat[4,3] * rU_Opt_Seq[2,3]) + (rB_Mat[4,4] * rU_Opt_Seq[2,4]) + (rB_Mat[4,5] * rU_Opt_Seq[2,5]);
rX_Pred_Horizon[2, 5] := (rA_Mat[5,1] * rX_Pred_Horizon[1,1]) + (rA_Mat[5,2] * rX_Pred_Horizon[1,2]) + (rA_Mat[5,3] * rX_Pred_Horizon[1,3]) + (rA_Mat[5,4] * rX_Pred_Horizon[1,4]) + (rA_Mat[5,5] * rX_Pred_Horizon[1,5]) + (rA_Mat[5,6] * rX_Pred_Horizon[1,6]) + (rB_Mat[5,1] * rU_Opt_Seq[2,1]) + (rB_Mat[5,2] * rU_Opt_Seq[2,2]) + (rB_Mat[5,3] * rU_Opt_Seq[2,3]) + (rB_Mat[5,4] * rU_Opt_Seq[2,4]) + (rB_Mat[5,5] * rU_Opt_Seq[2,5]);
rX_Pred_Horizon[2, 6] := (rA_Mat[6,1] * rX_Pred_Horizon[1,1]) + (rA_Mat[6,2] * rX_Pred_Horizon[1,2]) + (rA_Mat[6,3] * rX_Pred_Horizon[1,3]) + (rA_Mat[6,4] * rX_Pred_Horizon[1,4]) + (rA_Mat[6,5] * rX_Pred_Horizon[1,5]) + (rA_Mat[6,6] * rX_Pred_Horizon[1,6]) + (rB_Mat[6,1] * rU_Opt_Seq[2,1]) + (rB_Mat[6,2] * rU_Opt_Seq[2,2]) + (rB_Mat[6,3] * rU_Opt_Seq[2,3]) + (rB_Mat[6,4] * rU_Opt_Seq[2,4]) + (rB_Mat[6,5] * rU_Opt_Seq[2,5]);

(* Iteration 5 - Forward State Prediction Step 3 (h=3): x_3 = A * x_2 + B * u_3 *)
rX_Pred_Horizon[3, 1] := (rA_Mat[1,1] * rX_Pred_Horizon[2,1]) + (rA_Mat[1,2] * rX_Pred_Horizon[2,2]) + (rA_Mat[1,3] * rX_Pred_Horizon[2,3]) + (rA_Mat[1,4] * rX_Pred_Horizon[2,4]) + (rA_Mat[1,5] * rX_Pred_Horizon[2,5]) + (rA_Mat[1,6] * rX_Pred_Horizon[2,6]) + (rB_Mat[1,1] * rU_Opt_Seq[3,1]) + (rB_Mat[1,2] * rU_Opt_Seq[3,2]) + (rB_Mat[1,3] * rU_Opt_Seq[3,3]) + (rB_Mat[1,4] * rU_Opt_Seq[3,4]) + (rB_Mat[1,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[3, 2] := (rA_Mat[2,1] * rX_Pred_Horizon[2,1]) + (rA_Mat[2,2] * rX_Pred_Horizon[2,2]) + (rA_Mat[2,3] * rX_Pred_Horizon[2,3]) + (rA_Mat[2,4] * rX_Pred_Horizon[2,4]) + (rA_Mat[2,5] * rX_Pred_Horizon[2,5]) + (rA_Mat[2,6] * rX_Pred_Horizon[2,6]) + (rB_Mat[2,1] * rU_Opt_Seq[3,1]) + (rB_Mat[2,2] * rU_Opt_Seq[3,2]) + (rB_Mat[2,3] * rU_Opt_Seq[3,3]) + (rB_Mat[2,4] * rU_Opt_Seq[3,4]) + (rB_Mat[2,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[3, 3] := (rA_Mat[3,1] * rX_Pred_Horizon[2,1]) + (rA_Mat[3,2] * rX_Pred_Horizon[2,2]) + (rA_Mat[3,3] * rX_Pred_Horizon[2,3]) + (rA_Mat[3,4] * rX_Pred_Horizon[2,4]) + (rA_Mat[3,5] * rX_Pred_Horizon[2,5]) + (rA_Mat[3,6] * rX_Pred_Horizon[2,6]) + (rB_Mat[3,1] * rU_Opt_Seq[3,1]) + (rB_Mat[3,2] * rU_Opt_Seq[3,2]) + (rB_Mat[3,3] * rU_Opt_Seq[3,3]) + (rB_Mat[3,4] * rU_Opt_Seq[3,4]) + (rB_Mat[3,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[3, 4] := (rA_Mat[4,1] * rX_Pred_Horizon[2,1]) + (rA_Mat[4,2] * rX_Pred_Horizon[2,2]) + (rA_Mat[4,3] * rX_Pred_Horizon[2,3]) + (rA_Mat[4,4] * rX_Pred_Horizon[2,4]) + (rA_Mat[4,5] * rX_Pred_Horizon[2,5]) + (rA_Mat[4,6] * rX_Pred_Horizon[2,6]) + (rB_Mat[4,1] * rU_Opt_Seq[3,1]) + (rB_Mat[4,2] * rU_Opt_Seq[3,2]) + (rB_Mat[4,3] * rU_Opt_Seq[3,3]) + (rB_Mat[4,4] * rU_Opt_Seq[3,4]) + (rB_Mat[4,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[3, 5] := (rA_Mat[5,1] * rX_Pred_Horizon[2,1]) + (rA_Mat[5,2] * rX_Pred_Horizon[2,2]) + (rA_Mat[5,3] * rX_Pred_Horizon[2,3]) + (rA_Mat[5,4] * rX_Pred_Horizon[2,4]) + (rA_Mat[5,5] * rX_Pred_Horizon[2,5]) + (rA_Mat[5,6] * rX_Pred_Horizon[2,6]) + (rB_Mat[5,1] * rU_Opt_Seq[3,1]) + (rB_Mat[5,2] * rU_Opt_Seq[3,2]) + (rB_Mat[5,3] * rU_Opt_Seq[3,3]) + (rB_Mat[5,4] * rU_Opt_Seq[3,4]) + (rB_Mat[5,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[3, 6] := (rA_Mat[6,1] * rX_Pred_Horizon[2,1]) + (rA_Mat[6,2] * rX_Pred_Horizon[2,2]) + (rA_Mat[6,3] * rX_Pred_Horizon[2,3]) + (rA_Mat[6,4] * rX_Pred_Horizon[2,4]) + (rA_Mat[6,5] * rX_Pred_Horizon[2,5]) + (rA_Mat[6,6] * rX_Pred_Horizon[2,6]) + (rB_Mat[6,1] * rU_Opt_Seq[3,1]) + (rB_Mat[6,2] * rU_Opt_Seq[3,2]) + (rB_Mat[6,3] * rU_Opt_Seq[3,3]) + (rB_Mat[6,4] * rU_Opt_Seq[3,4]) + (rB_Mat[6,5] * rU_Opt_Seq[3,5]);

(* Iteration 5 - Forward State Prediction Step 4 (h=4): x_4 = A * x_3 + B * u_3 (held beyond Hu) *)
rX_Pred_Horizon[4, 1] := (rA_Mat[1,1] * rX_Pred_Horizon[3,1]) + (rA_Mat[1,2] * rX_Pred_Horizon[3,2]) + (rA_Mat[1,3] * rX_Pred_Horizon[3,3]) + (rA_Mat[1,4] * rX_Pred_Horizon[3,4]) + (rA_Mat[1,5] * rX_Pred_Horizon[3,5]) + (rA_Mat[1,6] * rX_Pred_Horizon[3,6]) + (rB_Mat[1,1] * rU_Opt_Seq[3,1]) + (rB_Mat[1,2] * rU_Opt_Seq[3,2]) + (rB_Mat[1,3] * rU_Opt_Seq[3,3]) + (rB_Mat[1,4] * rU_Opt_Seq[3,4]) + (rB_Mat[1,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[4, 2] := (rA_Mat[2,1] * rX_Pred_Horizon[3,1]) + (rA_Mat[2,2] * rX_Pred_Horizon[3,2]) + (rA_Mat[2,3] * rX_Pred_Horizon[3,3]) + (rA_Mat[2,4] * rX_Pred_Horizon[3,4]) + (rA_Mat[2,5] * rX_Pred_Horizon[3,5]) + (rA_Mat[2,6] * rX_Pred_Horizon[3,6]) + (rB_Mat[2,1] * rU_Opt_Seq[3,1]) + (rB_Mat[2,2] * rU_Opt_Seq[3,2]) + (rB_Mat[2,3] * rU_Opt_Seq[3,3]) + (rB_Mat[2,4] * rU_Opt_Seq[3,4]) + (rB_Mat[2,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[4, 3] := (rA_Mat[3,1] * rX_Pred_Horizon[3,1]) + (rA_Mat[3,2] * rX_Pred_Horizon[3,2]) + (rA_Mat[3,3] * rX_Pred_Horizon[3,3]) + (rA_Mat[3,4] * rX_Pred_Horizon[3,4]) + (rA_Mat[3,5] * rX_Pred_Horizon[3,5]) + (rA_Mat[3,6] * rX_Pred_Horizon[3,6]) + (rB_Mat[3,1] * rU_Opt_Seq[3,1]) + (rB_Mat[3,2] * rU_Opt_Seq[3,2]) + (rB_Mat[3,3] * rU_Opt_Seq[3,3]) + (rB_Mat[3,4] * rU_Opt_Seq[3,4]) + (rB_Mat[3,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[4, 4] := (rA_Mat[4,1] * rX_Pred_Horizon[3,1]) + (rA_Mat[4,2] * rX_Pred_Horizon[3,2]) + (rA_Mat[4,3] * rX_Pred_Horizon[3,3]) + (rA_Mat[4,4] * rX_Pred_Horizon[3,4]) + (rA_Mat[4,5] * rX_Pred_Horizon[3,5]) + (rA_Mat[4,6] * rX_Pred_Horizon[3,6]) + (rB_Mat[4,1] * rU_Opt_Seq[3,1]) + (rB_Mat[4,2] * rU_Opt_Seq[3,2]) + (rB_Mat[4,3] * rU_Opt_Seq[3,3]) + (rB_Mat[4,4] * rU_Opt_Seq[3,4]) + (rB_Mat[4,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[4, 5] := (rA_Mat[5,1] * rX_Pred_Horizon[3,1]) + (rA_Mat[5,2] * rX_Pred_Horizon[3,2]) + (rA_Mat[5,3] * rX_Pred_Horizon[3,3]) + (rA_Mat[5,4] * rX_Pred_Horizon[3,4]) + (rA_Mat[5,5] * rX_Pred_Horizon[3,5]) + (rA_Mat[5,6] * rX_Pred_Horizon[3,6]) + (rB_Mat[5,1] * rU_Opt_Seq[3,1]) + (rB_Mat[5,2] * rU_Opt_Seq[3,2]) + (rB_Mat[5,3] * rU_Opt_Seq[3,3]) + (rB_Mat[5,4] * rU_Opt_Seq[3,4]) + (rB_Mat[5,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[4, 6] := (rA_Mat[6,1] * rX_Pred_Horizon[3,1]) + (rA_Mat[6,2] * rX_Pred_Horizon[3,2]) + (rA_Mat[6,3] * rX_Pred_Horizon[3,3]) + (rA_Mat[6,4] * rX_Pred_Horizon[3,4]) + (rA_Mat[6,5] * rX_Pred_Horizon[3,5]) + (rA_Mat[6,6] * rX_Pred_Horizon[3,6]) + (rB_Mat[6,1] * rU_Opt_Seq[3,1]) + (rB_Mat[6,2] * rU_Opt_Seq[3,2]) + (rB_Mat[6,3] * rU_Opt_Seq[3,3]) + (rB_Mat[6,4] * rU_Opt_Seq[3,4]) + (rB_Mat[6,5] * rU_Opt_Seq[3,5]);

(* Iteration 5 - Forward State Prediction Step 5 (h=5): x_5 = A * x_4 + B * u_3 (held beyond Hu) *)
rX_Pred_Horizon[5, 1] := (rA_Mat[1,1] * rX_Pred_Horizon[4,1]) + (rA_Mat[1,2] * rX_Pred_Horizon[4,2]) + (rA_Mat[1,3] * rX_Pred_Horizon[4,3]) + (rA_Mat[1,4] * rX_Pred_Horizon[4,4]) + (rA_Mat[1,5] * rX_Pred_Horizon[4,5]) + (rA_Mat[1,6] * rX_Pred_Horizon[4,6]) + (rB_Mat[1,1] * rU_Opt_Seq[3,1]) + (rB_Mat[1,2] * rU_Opt_Seq[3,2]) + (rB_Mat[1,3] * rU_Opt_Seq[3,3]) + (rB_Mat[1,4] * rU_Opt_Seq[3,4]) + (rB_Mat[1,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[5, 2] := (rA_Mat[2,1] * rX_Pred_Horizon[4,1]) + (rA_Mat[2,2] * rX_Pred_Horizon[4,2]) + (rA_Mat[2,3] * rX_Pred_Horizon[4,3]) + (rA_Mat[2,4] * rX_Pred_Horizon[4,4]) + (rA_Mat[2,5] * rX_Pred_Horizon[4,5]) + (rA_Mat[2,6] * rX_Pred_Horizon[4,6]) + (rB_Mat[2,1] * rU_Opt_Seq[3,1]) + (rB_Mat[2,2] * rU_Opt_Seq[3,2]) + (rB_Mat[2,3] * rU_Opt_Seq[3,3]) + (rB_Mat[2,4] * rU_Opt_Seq[3,4]) + (rB_Mat[2,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[5, 3] := (rA_Mat[3,1] * rX_Pred_Horizon[4,1]) + (rA_Mat[3,2] * rX_Pred_Horizon[4,2]) + (rA_Mat[3,3] * rX_Pred_Horizon[4,3]) + (rA_Mat[3,4] * rX_Pred_Horizon[4,4]) + (rA_Mat[3,5] * rX_Pred_Horizon[4,5]) + (rA_Mat[3,6] * rX_Pred_Horizon[4,6]) + (rB_Mat[3,1] * rU_Opt_Seq[3,1]) + (rB_Mat[3,2] * rU_Opt_Seq[3,2]) + (rB_Mat[3,3] * rU_Opt_Seq[3,3]) + (rB_Mat[3,4] * rU_Opt_Seq[3,4]) + (rB_Mat[3,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[5, 4] := (rA_Mat[4,1] * rX_Pred_Horizon[4,1]) + (rA_Mat[4,2] * rX_Pred_Horizon[4,2]) + (rA_Mat[4,3] * rX_Pred_Horizon[4,3]) + (rA_Mat[4,4] * rX_Pred_Horizon[4,4]) + (rA_Mat[4,5] * rX_Pred_Horizon[4,5]) + (rA_Mat[4,6] * rX_Pred_Horizon[4,6]) + (rB_Mat[4,1] * rU_Opt_Seq[3,1]) + (rB_Mat[4,2] * rU_Opt_Seq[3,2]) + (rB_Mat[4,3] * rU_Opt_Seq[3,3]) + (rB_Mat[4,4] * rU_Opt_Seq[3,4]) + (rB_Mat[4,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[5, 5] := (rA_Mat[5,1] * rX_Pred_Horizon[4,1]) + (rA_Mat[5,2] * rX_Pred_Horizon[4,2]) + (rA_Mat[5,3] * rX_Pred_Horizon[4,3]) + (rA_Mat[5,4] * rX_Pred_Horizon[4,4]) + (rA_Mat[5,5] * rX_Pred_Horizon[4,5]) + (rA_Mat[5,6] * rX_Pred_Horizon[4,6]) + (rB_Mat[5,1] * rU_Opt_Seq[3,1]) + (rB_Mat[5,2] * rU_Opt_Seq[3,2]) + (rB_Mat[5,3] * rU_Opt_Seq[3,3]) + (rB_Mat[5,4] * rU_Opt_Seq[3,4]) + (rB_Mat[5,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[5, 6] := (rA_Mat[6,1] * rX_Pred_Horizon[4,1]) + (rA_Mat[6,2] * rX_Pred_Horizon[4,2]) + (rA_Mat[6,3] * rX_Pred_Horizon[4,3]) + (rA_Mat[6,4] * rX_Pred_Horizon[4,4]) + (rA_Mat[6,5] * rX_Pred_Horizon[4,5]) + (rA_Mat[6,6] * rX_Pred_Horizon[4,6]) + (rB_Mat[6,1] * rU_Opt_Seq[3,1]) + (rB_Mat[6,2] * rU_Opt_Seq[3,2]) + (rB_Mat[6,3] * rU_Opt_Seq[3,3]) + (rB_Mat[6,4] * rU_Opt_Seq[3,4]) + (rB_Mat[6,5] * rU_Opt_Seq[3,5]);

(* Iteration 5 - Evaluate Objective Function Cost J *)
rMPC_Cost_J := 0.0;
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[1] * (rX_Pred_Horizon[1,1] - rX_Target[1,1]) * (rX_Pred_Horizon[1,1] - rX_Target[1,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[2] * (rX_Pred_Horizon[1,2] - rX_Target[1,2]) * (rX_Pred_Horizon[1,2] - rX_Target[1,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[3] * (rX_Pred_Horizon[1,3] - rX_Target[1,3]) * (rX_Pred_Horizon[1,3] - rX_Target[1,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[4] * (rX_Pred_Horizon[1,4] - rX_Target[1,4]) * (rX_Pred_Horizon[1,4] - rX_Target[1,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[5] * (rX_Pred_Horizon[1,5] - rX_Target[1,5]) * (rX_Pred_Horizon[1,5] - rX_Target[1,5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[6] * (rX_Pred_Horizon[1,6] - rX_Target[1,6]) * (rX_Pred_Horizon[1,6] - rX_Target[1,6]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[1] * (rX_Pred_Horizon[2,1] - rX_Target[2,1]) * (rX_Pred_Horizon[2,1] - rX_Target[2,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[2] * (rX_Pred_Horizon[2,2] - rX_Target[2,2]) * (rX_Pred_Horizon[2,2] - rX_Target[2,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[3] * (rX_Pred_Horizon[2,3] - rX_Target[2,3]) * (rX_Pred_Horizon[2,3] - rX_Target[2,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[4] * (rX_Pred_Horizon[2,4] - rX_Target[2,4]) * (rX_Pred_Horizon[2,4] - rX_Target[2,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[5] * (rX_Pred_Horizon[2,5] - rX_Target[2,5]) * (rX_Pred_Horizon[2,5] - rX_Target[2,5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[6] * (rX_Pred_Horizon[2,6] - rX_Target[2,6]) * (rX_Pred_Horizon[2,6] - rX_Target[2,6]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[1] * (rX_Pred_Horizon[3,1] - rX_Target[3,1]) * (rX_Pred_Horizon[3,1] - rX_Target[3,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[2] * (rX_Pred_Horizon[3,2] - rX_Target[3,2]) * (rX_Pred_Horizon[3,2] - rX_Target[3,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[3] * (rX_Pred_Horizon[3,3] - rX_Target[3,3]) * (rX_Pred_Horizon[3,3] - rX_Target[3,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[4] * (rX_Pred_Horizon[3,4] - rX_Target[3,4]) * (rX_Pred_Horizon[3,4] - rX_Target[3,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[5] * (rX_Pred_Horizon[3,5] - rX_Target[3,5]) * (rX_Pred_Horizon[3,5] - rX_Target[3,5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[6] * (rX_Pred_Horizon[3,6] - rX_Target[3,6]) * (rX_Pred_Horizon[3,6] - rX_Target[3,6]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[1] * (rX_Pred_Horizon[4,1] - rX_Target[4,1]) * (rX_Pred_Horizon[4,1] - rX_Target[4,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[2] * (rX_Pred_Horizon[4,2] - rX_Target[4,2]) * (rX_Pred_Horizon[4,2] - rX_Target[4,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[3] * (rX_Pred_Horizon[4,3] - rX_Target[4,3]) * (rX_Pred_Horizon[4,3] - rX_Target[4,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[4] * (rX_Pred_Horizon[4,4] - rX_Target[4,4]) * (rX_Pred_Horizon[4,4] - rX_Target[4,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[5] * (rX_Pred_Horizon[4,5] - rX_Target[4,5]) * (rX_Pred_Horizon[4,5] - rX_Target[4,5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[6] * (rX_Pred_Horizon[4,6] - rX_Target[4,6]) * (rX_Pred_Horizon[4,6] - rX_Target[4,6]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[1] * (rX_Pred_Horizon[5,1] - rX_Target[5,1]) * (rX_Pred_Horizon[5,1] - rX_Target[5,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[2] * (rX_Pred_Horizon[5,2] - rX_Target[5,2]) * (rX_Pred_Horizon[5,2] - rX_Target[5,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[3] * (rX_Pred_Horizon[5,3] - rX_Target[5,3]) * (rX_Pred_Horizon[5,3] - rX_Target[5,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[4] * (rX_Pred_Horizon[5,4] - rX_Target[5,4]) * (rX_Pred_Horizon[5,4] - rX_Target[5,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[5] * (rX_Pred_Horizon[5,5] - rX_Target[5,5]) * (rX_Pred_Horizon[5,5] - rX_Target[5,5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[6] * (rX_Pred_Horizon[5,6] - rX_Target[5,6]) * (rX_Pred_Horizon[5,6] - rX_Target[5,6]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rP_Diag[1] * (rX_Pred_Horizon[5,1] - rX_Target[5,1]) * (rX_Pred_Horizon[5,1] - rX_Target[5,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rP_Diag[2] * (rX_Pred_Horizon[5,2] - rX_Target[5,2]) * (rX_Pred_Horizon[5,2] - rX_Target[5,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rP_Diag[3] * (rX_Pred_Horizon[5,3] - rX_Target[5,3]) * (rX_Pred_Horizon[5,3] - rX_Target[5,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rP_Diag[4] * (rX_Pred_Horizon[5,4] - rX_Target[5,4]) * (rX_Pred_Horizon[5,4] - rX_Target[5,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rP_Diag[5] * (rX_Pred_Horizon[5,5] - rX_Target[5,5]) * (rX_Pred_Horizon[5,5] - rX_Target[5,5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rP_Diag[6] * (rX_Pred_Horizon[5,6] - rX_Target[5,6]) * (rX_Pred_Horizon[5,6] - rX_Target[5,6]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[1] * rU_Opt_Seq[1,1] * rU_Opt_Seq[1,1]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[2] * rU_Opt_Seq[1,2] * rU_Opt_Seq[1,2]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[3] * rU_Opt_Seq[1,3] * rU_Opt_Seq[1,3]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[4] * rU_Opt_Seq[1,4] * rU_Opt_Seq[1,4]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[5] * rU_Opt_Seq[1,5] * rU_Opt_Seq[1,5]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[1] * rU_Opt_Seq[2,1] * rU_Opt_Seq[2,1]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[2] * rU_Opt_Seq[2,2] * rU_Opt_Seq[2,2]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[3] * rU_Opt_Seq[2,3] * rU_Opt_Seq[2,3]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[4] * rU_Opt_Seq[2,4] * rU_Opt_Seq[2,4]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[5] * rU_Opt_Seq[2,5] * rU_Opt_Seq[2,5]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[1] * rU_Opt_Seq[3,1] * rU_Opt_Seq[3,1]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[2] * rU_Opt_Seq[3,2] * rU_Opt_Seq[3,2]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[3] * rU_Opt_Seq[3,3] * rU_Opt_Seq[3,3]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[4] * rU_Opt_Seq[3,4] * rU_Opt_Seq[3,4]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[5] * rU_Opt_Seq[3,5] * rU_Opt_Seq[3,5]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[1] * (rU_Opt_Seq[1,1] - a_u_prev[1]) * (rU_Opt_Seq[1,1] - a_u_prev[1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[1] * (rU_Opt_Seq[2,1] - rU_Opt_Seq[1,1]) * (rU_Opt_Seq[2,1] - rU_Opt_Seq[1,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[1] * (rU_Opt_Seq[3,1] - rU_Opt_Seq[2,1]) * (rU_Opt_Seq[3,1] - rU_Opt_Seq[2,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[2] * (rU_Opt_Seq[1,2] - a_u_prev[2]) * (rU_Opt_Seq[1,2] - a_u_prev[2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[2] * (rU_Opt_Seq[2,2] - rU_Opt_Seq[1,2]) * (rU_Opt_Seq[2,2] - rU_Opt_Seq[1,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[2] * (rU_Opt_Seq[3,2] - rU_Opt_Seq[2,2]) * (rU_Opt_Seq[3,2] - rU_Opt_Seq[2,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[3] * (rU_Opt_Seq[1,3] - a_u_prev[3]) * (rU_Opt_Seq[1,3] - a_u_prev[3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[3] * (rU_Opt_Seq[2,3] - rU_Opt_Seq[1,3]) * (rU_Opt_Seq[2,3] - rU_Opt_Seq[1,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[3] * (rU_Opt_Seq[3,3] - rU_Opt_Seq[2,3]) * (rU_Opt_Seq[3,3] - rU_Opt_Seq[2,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[4] * (rU_Opt_Seq[1,4] - a_u_prev[4]) * (rU_Opt_Seq[1,4] - a_u_prev[4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[4] * (rU_Opt_Seq[2,4] - rU_Opt_Seq[1,4]) * (rU_Opt_Seq[2,4] - rU_Opt_Seq[1,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[4] * (rU_Opt_Seq[3,4] - rU_Opt_Seq[2,4]) * (rU_Opt_Seq[3,4] - rU_Opt_Seq[2,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[5] * (rU_Opt_Seq[1,5] - a_u_prev[5]) * (rU_Opt_Seq[1,5] - a_u_prev[5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[5] * (rU_Opt_Seq[2,5] - rU_Opt_Seq[1,5]) * (rU_Opt_Seq[2,5] - rU_Opt_Seq[1,5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[5] * (rU_Opt_Seq[3,5] - rU_Opt_Seq[2,5]) * (rU_Opt_Seq[3,5] - rU_Opt_Seq[2,5]));

(* Iteration 5 - Backward Adjoint Costate Propagation: lambda_h = A^T * lambda_{h+1} + Q * (x_h - x_ref) *)
(* Terminal Costate at h=5: lambda_5 = (P + Q) * (x_5 - x_target_5) *)
rLambda_Costate[5, 1] := (rP_Diag[1] + rQ_Diag[1]) * (rX_Pred_Horizon[5,1] - rX_Target[5,1]);
rLambda_Costate[5, 2] := (rP_Diag[2] + rQ_Diag[2]) * (rX_Pred_Horizon[5,2] - rX_Target[5,2]);
rLambda_Costate[5, 3] := (rP_Diag[3] + rQ_Diag[3]) * (rX_Pred_Horizon[5,3] - rX_Target[5,3]);
rLambda_Costate[5, 4] := (rP_Diag[4] + rQ_Diag[4]) * (rX_Pred_Horizon[5,4] - rX_Target[5,4]);
rLambda_Costate[5, 5] := (rP_Diag[5] + rQ_Diag[5]) * (rX_Pred_Horizon[5,5] - rX_Target[5,5]);
rLambda_Costate[5, 6] := (rP_Diag[6] + rQ_Diag[6]) * (rX_Pred_Horizon[5,6] - rX_Target[5,6]);

(* Adjoint Costate at h=4: lambda_4 = A^T * lambda_5 + Q * (x_4 - x_target_4) *)
rLambda_Costate[4, 1] := (rA_Mat[1,1] * rLambda_Costate[5,1]) + (rA_Mat[2,1] * rLambda_Costate[5,2]) + (rA_Mat[3,1] * rLambda_Costate[5,3]) + (rA_Mat[4,1] * rLambda_Costate[5,4]) + (rA_Mat[5,1] * rLambda_Costate[5,5]) + (rA_Mat[6,1] * rLambda_Costate[5,6]) + (rQ_Diag[1] * (rX_Pred_Horizon[4,1] - rX_Target[4,1]));
rLambda_Costate[4, 2] := (rA_Mat[1,2] * rLambda_Costate[5,1]) + (rA_Mat[2,2] * rLambda_Costate[5,2]) + (rA_Mat[3,2] * rLambda_Costate[5,3]) + (rA_Mat[4,2] * rLambda_Costate[5,4]) + (rA_Mat[5,2] * rLambda_Costate[5,5]) + (rA_Mat[6,2] * rLambda_Costate[5,6]) + (rQ_Diag[2] * (rX_Pred_Horizon[4,2] - rX_Target[4,2]));
rLambda_Costate[4, 3] := (rA_Mat[1,3] * rLambda_Costate[5,1]) + (rA_Mat[2,3] * rLambda_Costate[5,2]) + (rA_Mat[3,3] * rLambda_Costate[5,3]) + (rA_Mat[4,3] * rLambda_Costate[5,4]) + (rA_Mat[5,3] * rLambda_Costate[5,5]) + (rA_Mat[6,3] * rLambda_Costate[5,6]) + (rQ_Diag[3] * (rX_Pred_Horizon[4,3] - rX_Target[4,3]));
rLambda_Costate[4, 4] := (rA_Mat[1,4] * rLambda_Costate[5,1]) + (rA_Mat[2,4] * rLambda_Costate[5,2]) + (rA_Mat[3,4] * rLambda_Costate[5,3]) + (rA_Mat[4,4] * rLambda_Costate[5,4]) + (rA_Mat[5,4] * rLambda_Costate[5,5]) + (rA_Mat[6,4] * rLambda_Costate[5,6]) + (rQ_Diag[4] * (rX_Pred_Horizon[4,4] - rX_Target[4,4]));
rLambda_Costate[4, 5] := (rA_Mat[1,5] * rLambda_Costate[5,1]) + (rA_Mat[2,5] * rLambda_Costate[5,2]) + (rA_Mat[3,5] * rLambda_Costate[5,3]) + (rA_Mat[4,5] * rLambda_Costate[5,4]) + (rA_Mat[5,5] * rLambda_Costate[5,5]) + (rA_Mat[6,5] * rLambda_Costate[5,6]) + (rQ_Diag[5] * (rX_Pred_Horizon[4,5] - rX_Target[4,5]));
rLambda_Costate[4, 6] := (rA_Mat[1,6] * rLambda_Costate[5,1]) + (rA_Mat[2,6] * rLambda_Costate[5,2]) + (rA_Mat[3,6] * rLambda_Costate[5,3]) + (rA_Mat[4,6] * rLambda_Costate[5,4]) + (rA_Mat[5,6] * rLambda_Costate[5,5]) + (rA_Mat[6,6] * rLambda_Costate[5,6]) + (rQ_Diag[6] * (rX_Pred_Horizon[4,6] - rX_Target[4,6]));

(* Adjoint Costate at h=3: lambda_3 = A^T * lambda_4 + Q * (x_3 - x_target_3) *)
rLambda_Costate[3, 1] := (rA_Mat[1,1] * rLambda_Costate[4,1]) + (rA_Mat[2,1] * rLambda_Costate[4,2]) + (rA_Mat[3,1] * rLambda_Costate[4,3]) + (rA_Mat[4,1] * rLambda_Costate[4,4]) + (rA_Mat[5,1] * rLambda_Costate[4,5]) + (rA_Mat[6,1] * rLambda_Costate[4,6]) + (rQ_Diag[1] * (rX_Pred_Horizon[3,1] - rX_Target[3,1]));
rLambda_Costate[3, 2] := (rA_Mat[1,2] * rLambda_Costate[4,1]) + (rA_Mat[2,2] * rLambda_Costate[4,2]) + (rA_Mat[3,2] * rLambda_Costate[4,3]) + (rA_Mat[4,2] * rLambda_Costate[4,4]) + (rA_Mat[5,2] * rLambda_Costate[4,5]) + (rA_Mat[6,2] * rLambda_Costate[4,6]) + (rQ_Diag[2] * (rX_Pred_Horizon[3,2] - rX_Target[3,2]));
rLambda_Costate[3, 3] := (rA_Mat[1,3] * rLambda_Costate[4,1]) + (rA_Mat[2,3] * rLambda_Costate[4,2]) + (rA_Mat[3,3] * rLambda_Costate[4,3]) + (rA_Mat[4,3] * rLambda_Costate[4,4]) + (rA_Mat[5,3] * rLambda_Costate[4,5]) + (rA_Mat[6,3] * rLambda_Costate[4,6]) + (rQ_Diag[3] * (rX_Pred_Horizon[3,3] - rX_Target[3,3]));
rLambda_Costate[3, 4] := (rA_Mat[1,4] * rLambda_Costate[4,1]) + (rA_Mat[2,4] * rLambda_Costate[4,2]) + (rA_Mat[3,4] * rLambda_Costate[4,3]) + (rA_Mat[4,4] * rLambda_Costate[4,4]) + (rA_Mat[5,4] * rLambda_Costate[4,5]) + (rA_Mat[6,4] * rLambda_Costate[4,6]) + (rQ_Diag[4] * (rX_Pred_Horizon[3,4] - rX_Target[3,4]));
rLambda_Costate[3, 5] := (rA_Mat[1,5] * rLambda_Costate[4,1]) + (rA_Mat[2,5] * rLambda_Costate[4,2]) + (rA_Mat[3,5] * rLambda_Costate[4,3]) + (rA_Mat[4,5] * rLambda_Costate[4,4]) + (rA_Mat[5,5] * rLambda_Costate[4,5]) + (rA_Mat[6,5] * rLambda_Costate[4,6]) + (rQ_Diag[5] * (rX_Pred_Horizon[3,5] - rX_Target[3,5]));
rLambda_Costate[3, 6] := (rA_Mat[1,6] * rLambda_Costate[4,1]) + (rA_Mat[2,6] * rLambda_Costate[4,2]) + (rA_Mat[3,6] * rLambda_Costate[4,3]) + (rA_Mat[4,6] * rLambda_Costate[4,4]) + (rA_Mat[5,6] * rLambda_Costate[4,5]) + (rA_Mat[6,6] * rLambda_Costate[4,6]) + (rQ_Diag[6] * (rX_Pred_Horizon[3,6] - rX_Target[3,6]));

(* Adjoint Costate at h=2: lambda_2 = A^T * lambda_3 + Q * (x_2 - x_target_2) *)
rLambda_Costate[2, 1] := (rA_Mat[1,1] * rLambda_Costate[3,1]) + (rA_Mat[2,1] * rLambda_Costate[3,2]) + (rA_Mat[3,1] * rLambda_Costate[3,3]) + (rA_Mat[4,1] * rLambda_Costate[3,4]) + (rA_Mat[5,1] * rLambda_Costate[3,5]) + (rA_Mat[6,1] * rLambda_Costate[3,6]) + (rQ_Diag[1] * (rX_Pred_Horizon[2,1] - rX_Target[2,1]));
rLambda_Costate[2, 2] := (rA_Mat[1,2] * rLambda_Costate[3,1]) + (rA_Mat[2,2] * rLambda_Costate[3,2]) + (rA_Mat[3,2] * rLambda_Costate[3,3]) + (rA_Mat[4,2] * rLambda_Costate[3,4]) + (rA_Mat[5,2] * rLambda_Costate[3,5]) + (rA_Mat[6,2] * rLambda_Costate[3,6]) + (rQ_Diag[2] * (rX_Pred_Horizon[2,2] - rX_Target[2,2]));
rLambda_Costate[2, 3] := (rA_Mat[1,3] * rLambda_Costate[3,1]) + (rA_Mat[2,3] * rLambda_Costate[3,2]) + (rA_Mat[3,3] * rLambda_Costate[3,3]) + (rA_Mat[4,3] * rLambda_Costate[3,4]) + (rA_Mat[5,3] * rLambda_Costate[3,5]) + (rA_Mat[6,3] * rLambda_Costate[3,6]) + (rQ_Diag[3] * (rX_Pred_Horizon[2,3] - rX_Target[2,3]));
rLambda_Costate[2, 4] := (rA_Mat[1,4] * rLambda_Costate[3,1]) + (rA_Mat[2,4] * rLambda_Costate[3,2]) + (rA_Mat[3,4] * rLambda_Costate[3,3]) + (rA_Mat[4,4] * rLambda_Costate[3,4]) + (rA_Mat[5,4] * rLambda_Costate[3,5]) + (rA_Mat[6,4] * rLambda_Costate[3,6]) + (rQ_Diag[4] * (rX_Pred_Horizon[2,4] - rX_Target[2,4]));
rLambda_Costate[2, 5] := (rA_Mat[1,5] * rLambda_Costate[3,1]) + (rA_Mat[2,5] * rLambda_Costate[3,2]) + (rA_Mat[3,5] * rLambda_Costate[3,3]) + (rA_Mat[4,5] * rLambda_Costate[3,4]) + (rA_Mat[5,5] * rLambda_Costate[3,5]) + (rA_Mat[6,5] * rLambda_Costate[3,6]) + (rQ_Diag[5] * (rX_Pred_Horizon[2,5] - rX_Target[2,5]));
rLambda_Costate[2, 6] := (rA_Mat[1,6] * rLambda_Costate[3,1]) + (rA_Mat[2,6] * rLambda_Costate[3,2]) + (rA_Mat[3,6] * rLambda_Costate[3,3]) + (rA_Mat[4,6] * rLambda_Costate[3,4]) + (rA_Mat[5,6] * rLambda_Costate[3,5]) + (rA_Mat[6,6] * rLambda_Costate[3,6]) + (rQ_Diag[6] * (rX_Pred_Horizon[2,6] - rX_Target[2,6]));

(* Adjoint Costate at h=1: lambda_1 = A^T * lambda_2 + Q * (x_1 - x_target_1) *)
rLambda_Costate[1, 1] := (rA_Mat[1,1] * rLambda_Costate[2,1]) + (rA_Mat[2,1] * rLambda_Costate[2,2]) + (rA_Mat[3,1] * rLambda_Costate[2,3]) + (rA_Mat[4,1] * rLambda_Costate[2,4]) + (rA_Mat[5,1] * rLambda_Costate[2,5]) + (rA_Mat[6,1] * rLambda_Costate[2,6]) + (rQ_Diag[1] * (rX_Pred_Horizon[1,1] - rX_Target[1,1]));
rLambda_Costate[1, 2] := (rA_Mat[1,2] * rLambda_Costate[2,1]) + (rA_Mat[2,2] * rLambda_Costate[2,2]) + (rA_Mat[3,2] * rLambda_Costate[2,3]) + (rA_Mat[4,2] * rLambda_Costate[2,4]) + (rA_Mat[5,2] * rLambda_Costate[2,5]) + (rA_Mat[6,2] * rLambda_Costate[2,6]) + (rQ_Diag[2] * (rX_Pred_Horizon[1,2] - rX_Target[1,2]));
rLambda_Costate[1, 3] := (rA_Mat[1,3] * rLambda_Costate[2,1]) + (rA_Mat[2,3] * rLambda_Costate[2,2]) + (rA_Mat[3,3] * rLambda_Costate[2,3]) + (rA_Mat[4,3] * rLambda_Costate[2,4]) + (rA_Mat[5,3] * rLambda_Costate[2,5]) + (rA_Mat[6,3] * rLambda_Costate[2,6]) + (rQ_Diag[3] * (rX_Pred_Horizon[1,3] - rX_Target[1,3]));
rLambda_Costate[1, 4] := (rA_Mat[1,4] * rLambda_Costate[2,1]) + (rA_Mat[2,4] * rLambda_Costate[2,2]) + (rA_Mat[3,4] * rLambda_Costate[2,3]) + (rA_Mat[4,4] * rLambda_Costate[2,4]) + (rA_Mat[5,4] * rLambda_Costate[2,5]) + (rA_Mat[6,4] * rLambda_Costate[2,6]) + (rQ_Diag[4] * (rX_Pred_Horizon[1,4] - rX_Target[1,4]));
rLambda_Costate[1, 5] := (rA_Mat[1,5] * rLambda_Costate[2,1]) + (rA_Mat[2,5] * rLambda_Costate[2,2]) + (rA_Mat[3,5] * rLambda_Costate[2,3]) + (rA_Mat[4,5] * rLambda_Costate[2,4]) + (rA_Mat[5,5] * rLambda_Costate[2,5]) + (rA_Mat[6,5] * rLambda_Costate[2,6]) + (rQ_Diag[5] * (rX_Pred_Horizon[1,5] - rX_Target[1,5]));
rLambda_Costate[1, 6] := (rA_Mat[1,6] * rLambda_Costate[2,1]) + (rA_Mat[2,6] * rLambda_Costate[2,2]) + (rA_Mat[3,6] * rLambda_Costate[2,3]) + (rA_Mat[4,6] * rLambda_Costate[2,4]) + (rA_Mat[5,6] * rLambda_Costate[2,5]) + (rA_Mat[6,6] * rLambda_Costate[2,6]) + (rQ_Diag[6] * (rX_Pred_Horizon[1,6] - rX_Target[1,6]));

(* Iteration 5 - Analytical Gradient Computation w.r.t. Control Inputs u_h *)
rMPC_GradNormSq := 0.0;
(* Gradient for u_1 (h=1) *)
rGrad_J[1, 1] := (rB_Mat[1,1] * rLambda_Costate[1,1]) + (rB_Mat[2,1] * rLambda_Costate[1,2]) + (rB_Mat[3,1] * rLambda_Costate[1,3]) + (rB_Mat[4,1] * rLambda_Costate[1,4]) + (rB_Mat[5,1] * rLambda_Costate[1,5]) + (rB_Mat[6,1] * rLambda_Costate[1,6]) + (rR_Diag[1] * rU_Opt_Seq[1,1]) + (rS_Diag[1] * (rU_Opt_Seq[1,1] - a_u_prev[1])) - (rS_Diag[1] * (rU_Opt_Seq[2,1] - rU_Opt_Seq[1,1]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[1, 1] * rGrad_J[1, 1]);
rGrad_J[1, 2] := (rB_Mat[1,2] * rLambda_Costate[1,1]) + (rB_Mat[2,2] * rLambda_Costate[1,2]) + (rB_Mat[3,2] * rLambda_Costate[1,3]) + (rB_Mat[4,2] * rLambda_Costate[1,4]) + (rB_Mat[5,2] * rLambda_Costate[1,5]) + (rB_Mat[6,2] * rLambda_Costate[1,6]) + (rR_Diag[2] * rU_Opt_Seq[1,2]) + (rS_Diag[2] * (rU_Opt_Seq[1,2] - a_u_prev[2])) - (rS_Diag[2] * (rU_Opt_Seq[2,2] - rU_Opt_Seq[1,2]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[1, 2] * rGrad_J[1, 2]);
rGrad_J[1, 3] := (rB_Mat[1,3] * rLambda_Costate[1,1]) + (rB_Mat[2,3] * rLambda_Costate[1,2]) + (rB_Mat[3,3] * rLambda_Costate[1,3]) + (rB_Mat[4,3] * rLambda_Costate[1,4]) + (rB_Mat[5,3] * rLambda_Costate[1,5]) + (rB_Mat[6,3] * rLambda_Costate[1,6]) + (rR_Diag[3] * rU_Opt_Seq[1,3]) + (rS_Diag[3] * (rU_Opt_Seq[1,3] - a_u_prev[3])) - (rS_Diag[3] * (rU_Opt_Seq[2,3] - rU_Opt_Seq[1,3]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[1, 3] * rGrad_J[1, 3]);
rGrad_J[1, 4] := (rB_Mat[1,4] * rLambda_Costate[1,1]) + (rB_Mat[2,4] * rLambda_Costate[1,2]) + (rB_Mat[3,4] * rLambda_Costate[1,3]) + (rB_Mat[4,4] * rLambda_Costate[1,4]) + (rB_Mat[5,4] * rLambda_Costate[1,5]) + (rB_Mat[6,4] * rLambda_Costate[1,6]) + (rR_Diag[4] * rU_Opt_Seq[1,4]) + (rS_Diag[4] * (rU_Opt_Seq[1,4] - a_u_prev[4])) - (rS_Diag[4] * (rU_Opt_Seq[2,4] - rU_Opt_Seq[1,4]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[1, 4] * rGrad_J[1, 4]);
rGrad_J[1, 5] := (rB_Mat[1,5] * rLambda_Costate[1,1]) + (rB_Mat[2,5] * rLambda_Costate[1,2]) + (rB_Mat[3,5] * rLambda_Costate[1,3]) + (rB_Mat[4,5] * rLambda_Costate[1,4]) + (rB_Mat[5,5] * rLambda_Costate[1,5]) + (rB_Mat[6,5] * rLambda_Costate[1,6]) + (rR_Diag[5] * rU_Opt_Seq[1,5]) + (rS_Diag[5] * (rU_Opt_Seq[1,5] - a_u_prev[5])) - (rS_Diag[5] * (rU_Opt_Seq[2,5] - rU_Opt_Seq[1,5]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[1, 5] * rGrad_J[1, 5]);

(* Gradient for u_2 (h=2) *)
rGrad_J[2, 1] := (rB_Mat[1,1] * rLambda_Costate[2,1]) + (rB_Mat[2,1] * rLambda_Costate[2,2]) + (rB_Mat[3,1] * rLambda_Costate[2,3]) + (rB_Mat[4,1] * rLambda_Costate[2,4]) + (rB_Mat[5,1] * rLambda_Costate[2,5]) + (rB_Mat[6,1] * rLambda_Costate[2,6]) + (rR_Diag[1] * rU_Opt_Seq[2,1]) + (rS_Diag[1] * (rU_Opt_Seq[2,1] - rU_Opt_Seq[1,1])) - (rS_Diag[1] * (rU_Opt_Seq[3,1] - rU_Opt_Seq[2,1]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[2, 1] * rGrad_J[2, 1]);
rGrad_J[2, 2] := (rB_Mat[1,2] * rLambda_Costate[2,1]) + (rB_Mat[2,2] * rLambda_Costate[2,2]) + (rB_Mat[3,2] * rLambda_Costate[2,3]) + (rB_Mat[4,2] * rLambda_Costate[2,4]) + (rB_Mat[5,2] * rLambda_Costate[2,5]) + (rB_Mat[6,2] * rLambda_Costate[2,6]) + (rR_Diag[2] * rU_Opt_Seq[2,2]) + (rS_Diag[2] * (rU_Opt_Seq[2,2] - rU_Opt_Seq[1,2])) - (rS_Diag[2] * (rU_Opt_Seq[3,2] - rU_Opt_Seq[2,2]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[2, 2] * rGrad_J[2, 2]);
rGrad_J[2, 3] := (rB_Mat[1,3] * rLambda_Costate[2,1]) + (rB_Mat[2,3] * rLambda_Costate[2,2]) + (rB_Mat[3,3] * rLambda_Costate[2,3]) + (rB_Mat[4,3] * rLambda_Costate[2,4]) + (rB_Mat[5,3] * rLambda_Costate[2,5]) + (rB_Mat[6,3] * rLambda_Costate[2,6]) + (rR_Diag[3] * rU_Opt_Seq[2,3]) + (rS_Diag[3] * (rU_Opt_Seq[2,3] - rU_Opt_Seq[1,3])) - (rS_Diag[3] * (rU_Opt_Seq[3,3] - rU_Opt_Seq[2,3]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[2, 3] * rGrad_J[2, 3]);
rGrad_J[2, 4] := (rB_Mat[1,4] * rLambda_Costate[2,1]) + (rB_Mat[2,4] * rLambda_Costate[2,2]) + (rB_Mat[3,4] * rLambda_Costate[2,3]) + (rB_Mat[4,4] * rLambda_Costate[2,4]) + (rB_Mat[5,4] * rLambda_Costate[2,5]) + (rB_Mat[6,4] * rLambda_Costate[2,6]) + (rR_Diag[4] * rU_Opt_Seq[2,4]) + (rS_Diag[4] * (rU_Opt_Seq[2,4] - rU_Opt_Seq[1,4])) - (rS_Diag[4] * (rU_Opt_Seq[3,4] - rU_Opt_Seq[2,4]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[2, 4] * rGrad_J[2, 4]);
rGrad_J[2, 5] := (rB_Mat[1,5] * rLambda_Costate[2,1]) + (rB_Mat[2,5] * rLambda_Costate[2,2]) + (rB_Mat[3,5] * rLambda_Costate[2,3]) + (rB_Mat[4,5] * rLambda_Costate[2,4]) + (rB_Mat[5,5] * rLambda_Costate[2,5]) + (rB_Mat[6,5] * rLambda_Costate[2,6]) + (rR_Diag[5] * rU_Opt_Seq[2,5]) + (rS_Diag[5] * (rU_Opt_Seq[2,5] - rU_Opt_Seq[1,5])) - (rS_Diag[5] * (rU_Opt_Seq[3,5] - rU_Opt_Seq[2,5]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[2, 5] * rGrad_J[2, 5]);

(* Gradient for u_3 (h=3, held through h=4, 5) *)
rGrad_J[3, 1] := (rB_Mat[1,1] * (rLambda_Costate[3,1] + rLambda_Costate[4,1] + rLambda_Costate[5,1])) + (rB_Mat[2,1] * (rLambda_Costate[3,2] + rLambda_Costate[4,2] + rLambda_Costate[5,2])) + (rB_Mat[3,1] * (rLambda_Costate[3,3] + rLambda_Costate[4,3] + rLambda_Costate[5,3])) + (rB_Mat[4,1] * (rLambda_Costate[3,4] + rLambda_Costate[4,4] + rLambda_Costate[5,4])) + (rB_Mat[5,1] * (rLambda_Costate[3,5] + rLambda_Costate[4,5] + rLambda_Costate[5,5])) + (rB_Mat[6,1] * (rLambda_Costate[3,6] + rLambda_Costate[4,6] + rLambda_Costate[5,6])) + (rR_Diag[1] * rU_Opt_Seq[3,1]) + (rS_Diag[1] * (rU_Opt_Seq[3,1] - rU_Opt_Seq[2,1]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[3, 1] * rGrad_J[3, 1]);
rGrad_J[3, 2] := (rB_Mat[1,2] * (rLambda_Costate[3,1] + rLambda_Costate[4,1] + rLambda_Costate[5,1])) + (rB_Mat[2,2] * (rLambda_Costate[3,2] + rLambda_Costate[4,2] + rLambda_Costate[5,2])) + (rB_Mat[3,2] * (rLambda_Costate[3,3] + rLambda_Costate[4,3] + rLambda_Costate[5,3])) + (rB_Mat[4,2] * (rLambda_Costate[3,4] + rLambda_Costate[4,4] + rLambda_Costate[5,4])) + (rB_Mat[5,2] * (rLambda_Costate[3,5] + rLambda_Costate[4,5] + rLambda_Costate[5,5])) + (rB_Mat[6,2] * (rLambda_Costate[3,6] + rLambda_Costate[4,6] + rLambda_Costate[5,6])) + (rR_Diag[2] * rU_Opt_Seq[3,2]) + (rS_Diag[2] * (rU_Opt_Seq[3,2] - rU_Opt_Seq[2,2]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[3, 2] * rGrad_J[3, 2]);
rGrad_J[3, 3] := (rB_Mat[1,3] * (rLambda_Costate[3,1] + rLambda_Costate[4,1] + rLambda_Costate[5,1])) + (rB_Mat[2,3] * (rLambda_Costate[3,2] + rLambda_Costate[4,2] + rLambda_Costate[5,2])) + (rB_Mat[3,3] * (rLambda_Costate[3,3] + rLambda_Costate[4,3] + rLambda_Costate[5,3])) + (rB_Mat[4,3] * (rLambda_Costate[3,4] + rLambda_Costate[4,4] + rLambda_Costate[5,4])) + (rB_Mat[5,3] * (rLambda_Costate[3,5] + rLambda_Costate[4,5] + rLambda_Costate[5,5])) + (rB_Mat[6,3] * (rLambda_Costate[3,6] + rLambda_Costate[4,6] + rLambda_Costate[5,6])) + (rR_Diag[3] * rU_Opt_Seq[3,3]) + (rS_Diag[3] * (rU_Opt_Seq[3,3] - rU_Opt_Seq[2,3]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[3, 3] * rGrad_J[3, 3]);
rGrad_J[3, 4] := (rB_Mat[1,4] * (rLambda_Costate[3,1] + rLambda_Costate[4,1] + rLambda_Costate[5,1])) + (rB_Mat[2,4] * (rLambda_Costate[3,2] + rLambda_Costate[4,2] + rLambda_Costate[5,2])) + (rB_Mat[3,4] * (rLambda_Costate[3,3] + rLambda_Costate[4,3] + rLambda_Costate[5,3])) + (rB_Mat[4,4] * (rLambda_Costate[3,4] + rLambda_Costate[4,4] + rLambda_Costate[5,4])) + (rB_Mat[5,4] * (rLambda_Costate[3,5] + rLambda_Costate[4,5] + rLambda_Costate[5,5])) + (rB_Mat[6,4] * (rLambda_Costate[3,6] + rLambda_Costate[4,6] + rLambda_Costate[5,6])) + (rR_Diag[4] * rU_Opt_Seq[3,4]) + (rS_Diag[4] * (rU_Opt_Seq[3,4] - rU_Opt_Seq[2,4]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[3, 4] * rGrad_J[3, 4]);
rGrad_J[3, 5] := (rB_Mat[1,5] * (rLambda_Costate[3,1] + rLambda_Costate[4,1] + rLambda_Costate[5,1])) + (rB_Mat[2,5] * (rLambda_Costate[3,2] + rLambda_Costate[4,2] + rLambda_Costate[5,2])) + (rB_Mat[3,5] * (rLambda_Costate[3,3] + rLambda_Costate[4,3] + rLambda_Costate[5,3])) + (rB_Mat[4,5] * (rLambda_Costate[3,4] + rLambda_Costate[4,4] + rLambda_Costate[5,4])) + (rB_Mat[5,5] * (rLambda_Costate[3,5] + rLambda_Costate[4,5] + rLambda_Costate[5,5])) + (rB_Mat[6,5] * (rLambda_Costate[3,6] + rLambda_Costate[4,6] + rLambda_Costate[5,6])) + (rR_Diag[5] * rU_Opt_Seq[3,5]) + (rS_Diag[5] * (rU_Opt_Seq[3,5] - rU_Opt_Seq[2,5]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[3, 5] * rGrad_J[3, 5]);

(* Iteration 5 - Projected Gradient Step with Hard Box & Dynamic Slew Limits *)
rTemp_Val := rU_Opt_Seq[1, 1] - (rAlpha_PGD_StepSize * rGrad_J[1, 1]);
(* Slew limit against prior actuator output *)
IF rTemp_Val > (a_u_prev[1] + rDeltaU_Max[1]) THEN
    rTemp_Val := a_u_prev[1] + rDeltaU_Max[1];
ELSIF rTemp_Val < (a_u_prev[1] - rDeltaU_Max[1]) THEN
    rTemp_Val := a_u_prev[1] - rDeltaU_Max[1];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[1] THEN
    rTemp_Val := rU_BoxMax[1];
ELSIF rTemp_Val < rU_BoxMin[1] THEN
    rTemp_Val := rU_BoxMin[1];
END_IF;
rU_Opt_Seq[1, 1] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[1, 2] - (rAlpha_PGD_StepSize * rGrad_J[1, 2]);
(* Slew limit against prior actuator output *)
IF rTemp_Val > (a_u_prev[2] + rDeltaU_Max[2]) THEN
    rTemp_Val := a_u_prev[2] + rDeltaU_Max[2];
ELSIF rTemp_Val < (a_u_prev[2] - rDeltaU_Max[2]) THEN
    rTemp_Val := a_u_prev[2] - rDeltaU_Max[2];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[2] THEN
    rTemp_Val := rU_BoxMax[2];
ELSIF rTemp_Val < rU_BoxMin[2] THEN
    rTemp_Val := rU_BoxMin[2];
END_IF;
rU_Opt_Seq[1, 2] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[1, 3] - (rAlpha_PGD_StepSize * rGrad_J[1, 3]);
(* Slew limit against prior actuator output *)
IF rTemp_Val > (a_u_prev[3] + rDeltaU_Max[3]) THEN
    rTemp_Val := a_u_prev[3] + rDeltaU_Max[3];
ELSIF rTemp_Val < (a_u_prev[3] - rDeltaU_Max[3]) THEN
    rTemp_Val := a_u_prev[3] - rDeltaU_Max[3];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[3] THEN
    rTemp_Val := rU_BoxMax[3];
ELSIF rTemp_Val < rU_BoxMin[3] THEN
    rTemp_Val := rU_BoxMin[3];
END_IF;
rU_Opt_Seq[1, 3] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[1, 4] - (rAlpha_PGD_StepSize * rGrad_J[1, 4]);
(* Slew limit against prior actuator output *)
IF rTemp_Val > (a_u_prev[4] + rDeltaU_Max[4]) THEN
    rTemp_Val := a_u_prev[4] + rDeltaU_Max[4];
ELSIF rTemp_Val < (a_u_prev[4] - rDeltaU_Max[4]) THEN
    rTemp_Val := a_u_prev[4] - rDeltaU_Max[4];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[4] THEN
    rTemp_Val := rU_BoxMax[4];
ELSIF rTemp_Val < rU_BoxMin[4] THEN
    rTemp_Val := rU_BoxMin[4];
END_IF;
rU_Opt_Seq[1, 4] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[1, 5] - (rAlpha_PGD_StepSize * rGrad_J[1, 5]);
(* Slew limit against prior actuator output *)
IF rTemp_Val > (a_u_prev[5] + rDeltaU_Max[5]) THEN
    rTemp_Val := a_u_prev[5] + rDeltaU_Max[5];
ELSIF rTemp_Val < (a_u_prev[5] - rDeltaU_Max[5]) THEN
    rTemp_Val := a_u_prev[5] - rDeltaU_Max[5];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[5] THEN
    rTemp_Val := rU_BoxMax[5];
ELSIF rTemp_Val < rU_BoxMin[5] THEN
    rTemp_Val := rU_BoxMin[5];
END_IF;
rU_Opt_Seq[1, 5] := rTemp_Val;

rTemp_Val := rU_Opt_Seq[2, 1] - (rAlpha_PGD_StepSize * rGrad_J[2, 1]);
(* Slew limit against step 1 *)
IF rTemp_Val > (rU_Opt_Seq[1, 1] + rDeltaU_Max[1]) THEN
    rTemp_Val := rU_Opt_Seq[1, 1] + rDeltaU_Max[1];
ELSIF rTemp_Val < (rU_Opt_Seq[1, 1] - rDeltaU_Max[1]) THEN
    rTemp_Val := rU_Opt_Seq[1, 1] - rDeltaU_Max[1];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[1] THEN
    rTemp_Val := rU_BoxMax[1];
ELSIF rTemp_Val < rU_BoxMin[1] THEN
    rTemp_Val := rU_BoxMin[1];
END_IF;
rU_Opt_Seq[2, 1] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[2, 2] - (rAlpha_PGD_StepSize * rGrad_J[2, 2]);
(* Slew limit against step 1 *)
IF rTemp_Val > (rU_Opt_Seq[1, 2] + rDeltaU_Max[2]) THEN
    rTemp_Val := rU_Opt_Seq[1, 2] + rDeltaU_Max[2];
ELSIF rTemp_Val < (rU_Opt_Seq[1, 2] - rDeltaU_Max[2]) THEN
    rTemp_Val := rU_Opt_Seq[1, 2] - rDeltaU_Max[2];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[2] THEN
    rTemp_Val := rU_BoxMax[2];
ELSIF rTemp_Val < rU_BoxMin[2] THEN
    rTemp_Val := rU_BoxMin[2];
END_IF;
rU_Opt_Seq[2, 2] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[2, 3] - (rAlpha_PGD_StepSize * rGrad_J[2, 3]);
(* Slew limit against step 1 *)
IF rTemp_Val > (rU_Opt_Seq[1, 3] + rDeltaU_Max[3]) THEN
    rTemp_Val := rU_Opt_Seq[1, 3] + rDeltaU_Max[3];
ELSIF rTemp_Val < (rU_Opt_Seq[1, 3] - rDeltaU_Max[3]) THEN
    rTemp_Val := rU_Opt_Seq[1, 3] - rDeltaU_Max[3];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[3] THEN
    rTemp_Val := rU_BoxMax[3];
ELSIF rTemp_Val < rU_BoxMin[3] THEN
    rTemp_Val := rU_BoxMin[3];
END_IF;
rU_Opt_Seq[2, 3] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[2, 4] - (rAlpha_PGD_StepSize * rGrad_J[2, 4]);
(* Slew limit against step 1 *)
IF rTemp_Val > (rU_Opt_Seq[1, 4] + rDeltaU_Max[4]) THEN
    rTemp_Val := rU_Opt_Seq[1, 4] + rDeltaU_Max[4];
ELSIF rTemp_Val < (rU_Opt_Seq[1, 4] - rDeltaU_Max[4]) THEN
    rTemp_Val := rU_Opt_Seq[1, 4] - rDeltaU_Max[4];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[4] THEN
    rTemp_Val := rU_BoxMax[4];
ELSIF rTemp_Val < rU_BoxMin[4] THEN
    rTemp_Val := rU_BoxMin[4];
END_IF;
rU_Opt_Seq[2, 4] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[2, 5] - (rAlpha_PGD_StepSize * rGrad_J[2, 5]);
(* Slew limit against step 1 *)
IF rTemp_Val > (rU_Opt_Seq[1, 5] + rDeltaU_Max[5]) THEN
    rTemp_Val := rU_Opt_Seq[1, 5] + rDeltaU_Max[5];
ELSIF rTemp_Val < (rU_Opt_Seq[1, 5] - rDeltaU_Max[5]) THEN
    rTemp_Val := rU_Opt_Seq[1, 5] - rDeltaU_Max[5];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[5] THEN
    rTemp_Val := rU_BoxMax[5];
ELSIF rTemp_Val < rU_BoxMin[5] THEN
    rTemp_Val := rU_BoxMin[5];
END_IF;
rU_Opt_Seq[2, 5] := rTemp_Val;

rTemp_Val := rU_Opt_Seq[3, 1] - (rAlpha_PGD_StepSize * rGrad_J[3, 1]);
(* Slew limit against step 2 *)
IF rTemp_Val > (rU_Opt_Seq[2, 1] + rDeltaU_Max[1]) THEN
    rTemp_Val := rU_Opt_Seq[2, 1] + rDeltaU_Max[1];
ELSIF rTemp_Val < (rU_Opt_Seq[2, 1] - rDeltaU_Max[1]) THEN
    rTemp_Val := rU_Opt_Seq[2, 1] - rDeltaU_Max[1];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[1] THEN
    rTemp_Val := rU_BoxMax[1];
ELSIF rTemp_Val < rU_BoxMin[1] THEN
    rTemp_Val := rU_BoxMin[1];
END_IF;
rU_Opt_Seq[3, 1] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[3, 2] - (rAlpha_PGD_StepSize * rGrad_J[3, 2]);
(* Slew limit against step 2 *)
IF rTemp_Val > (rU_Opt_Seq[2, 2] + rDeltaU_Max[2]) THEN
    rTemp_Val := rU_Opt_Seq[2, 2] + rDeltaU_Max[2];
ELSIF rTemp_Val < (rU_Opt_Seq[2, 2] - rDeltaU_Max[2]) THEN
    rTemp_Val := rU_Opt_Seq[2, 2] - rDeltaU_Max[2];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[2] THEN
    rTemp_Val := rU_BoxMax[2];
ELSIF rTemp_Val < rU_BoxMin[2] THEN
    rTemp_Val := rU_BoxMin[2];
END_IF;
rU_Opt_Seq[3, 2] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[3, 3] - (rAlpha_PGD_StepSize * rGrad_J[3, 3]);
(* Slew limit against step 2 *)
IF rTemp_Val > (rU_Opt_Seq[2, 3] + rDeltaU_Max[3]) THEN
    rTemp_Val := rU_Opt_Seq[2, 3] + rDeltaU_Max[3];
ELSIF rTemp_Val < (rU_Opt_Seq[2, 3] - rDeltaU_Max[3]) THEN
    rTemp_Val := rU_Opt_Seq[2, 3] - rDeltaU_Max[3];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[3] THEN
    rTemp_Val := rU_BoxMax[3];
ELSIF rTemp_Val < rU_BoxMin[3] THEN
    rTemp_Val := rU_BoxMin[3];
END_IF;
rU_Opt_Seq[3, 3] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[3, 4] - (rAlpha_PGD_StepSize * rGrad_J[3, 4]);
(* Slew limit against step 2 *)
IF rTemp_Val > (rU_Opt_Seq[2, 4] + rDeltaU_Max[4]) THEN
    rTemp_Val := rU_Opt_Seq[2, 4] + rDeltaU_Max[4];
ELSIF rTemp_Val < (rU_Opt_Seq[2, 4] - rDeltaU_Max[4]) THEN
    rTemp_Val := rU_Opt_Seq[2, 4] - rDeltaU_Max[4];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[4] THEN
    rTemp_Val := rU_BoxMax[4];
ELSIF rTemp_Val < rU_BoxMin[4] THEN
    rTemp_Val := rU_BoxMin[4];
END_IF;
rU_Opt_Seq[3, 4] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[3, 5] - (rAlpha_PGD_StepSize * rGrad_J[3, 5]);
(* Slew limit against step 2 *)
IF rTemp_Val > (rU_Opt_Seq[2, 5] + rDeltaU_Max[5]) THEN
    rTemp_Val := rU_Opt_Seq[2, 5] + rDeltaU_Max[5];
ELSIF rTemp_Val < (rU_Opt_Seq[2, 5] - rDeltaU_Max[5]) THEN
    rTemp_Val := rU_Opt_Seq[2, 5] - rDeltaU_Max[5];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[5] THEN
    rTemp_Val := rU_BoxMax[5];
ELSIF rTemp_Val < rU_BoxMin[5] THEN
    rTemp_Val := rU_BoxMin[5];
END_IF;
rU_Opt_Seq[3, 5] := rTemp_Val;

(* ================================================================================================== *)
(* MPC PROJECTED GRADIENT DESCENT -- UNROLLED ITERATION 6 OF 10                                 *)
(* ================================================================================================== *)
iPGD_IterCount := 6;

(* Iteration 6 - Forward State Prediction Step 1 (h=1): x_1 = A * x_hat + B * u_1 *)
rX_Pred_Horizon[1, 1] := (rA_Mat[1,1] * a_x_hat[1]) + (rA_Mat[1,2] * a_x_hat[2]) + (rA_Mat[1,3] * a_x_hat[3]) + (rA_Mat[1,4] * a_x_hat[4]) + (rA_Mat[1,5] * a_x_hat[5]) + (rA_Mat[1,6] * a_x_hat[6]) + (rB_Mat[1,1] * rU_Opt_Seq[1,1]) + (rB_Mat[1,2] * rU_Opt_Seq[1,2]) + (rB_Mat[1,3] * rU_Opt_Seq[1,3]) + (rB_Mat[1,4] * rU_Opt_Seq[1,4]) + (rB_Mat[1,5] * rU_Opt_Seq[1,5]);
rX_Pred_Horizon[1, 2] := (rA_Mat[2,1] * a_x_hat[1]) + (rA_Mat[2,2] * a_x_hat[2]) + (rA_Mat[2,3] * a_x_hat[3]) + (rA_Mat[2,4] * a_x_hat[4]) + (rA_Mat[2,5] * a_x_hat[5]) + (rA_Mat[2,6] * a_x_hat[6]) + (rB_Mat[2,1] * rU_Opt_Seq[1,1]) + (rB_Mat[2,2] * rU_Opt_Seq[1,2]) + (rB_Mat[2,3] * rU_Opt_Seq[1,3]) + (rB_Mat[2,4] * rU_Opt_Seq[1,4]) + (rB_Mat[2,5] * rU_Opt_Seq[1,5]);
rX_Pred_Horizon[1, 3] := (rA_Mat[3,1] * a_x_hat[1]) + (rA_Mat[3,2] * a_x_hat[2]) + (rA_Mat[3,3] * a_x_hat[3]) + (rA_Mat[3,4] * a_x_hat[4]) + (rA_Mat[3,5] * a_x_hat[5]) + (rA_Mat[3,6] * a_x_hat[6]) + (rB_Mat[3,1] * rU_Opt_Seq[1,1]) + (rB_Mat[3,2] * rU_Opt_Seq[1,2]) + (rB_Mat[3,3] * rU_Opt_Seq[1,3]) + (rB_Mat[3,4] * rU_Opt_Seq[1,4]) + (rB_Mat[3,5] * rU_Opt_Seq[1,5]);
rX_Pred_Horizon[1, 4] := (rA_Mat[4,1] * a_x_hat[1]) + (rA_Mat[4,2] * a_x_hat[2]) + (rA_Mat[4,3] * a_x_hat[3]) + (rA_Mat[4,4] * a_x_hat[4]) + (rA_Mat[4,5] * a_x_hat[5]) + (rA_Mat[4,6] * a_x_hat[6]) + (rB_Mat[4,1] * rU_Opt_Seq[1,1]) + (rB_Mat[4,2] * rU_Opt_Seq[1,2]) + (rB_Mat[4,3] * rU_Opt_Seq[1,3]) + (rB_Mat[4,4] * rU_Opt_Seq[1,4]) + (rB_Mat[4,5] * rU_Opt_Seq[1,5]);
rX_Pred_Horizon[1, 5] := (rA_Mat[5,1] * a_x_hat[1]) + (rA_Mat[5,2] * a_x_hat[2]) + (rA_Mat[5,3] * a_x_hat[3]) + (rA_Mat[5,4] * a_x_hat[4]) + (rA_Mat[5,5] * a_x_hat[5]) + (rA_Mat[5,6] * a_x_hat[6]) + (rB_Mat[5,1] * rU_Opt_Seq[1,1]) + (rB_Mat[5,2] * rU_Opt_Seq[1,2]) + (rB_Mat[5,3] * rU_Opt_Seq[1,3]) + (rB_Mat[5,4] * rU_Opt_Seq[1,4]) + (rB_Mat[5,5] * rU_Opt_Seq[1,5]);
rX_Pred_Horizon[1, 6] := (rA_Mat[6,1] * a_x_hat[1]) + (rA_Mat[6,2] * a_x_hat[2]) + (rA_Mat[6,3] * a_x_hat[3]) + (rA_Mat[6,4] * a_x_hat[4]) + (rA_Mat[6,5] * a_x_hat[5]) + (rA_Mat[6,6] * a_x_hat[6]) + (rB_Mat[6,1] * rU_Opt_Seq[1,1]) + (rB_Mat[6,2] * rU_Opt_Seq[1,2]) + (rB_Mat[6,3] * rU_Opt_Seq[1,3]) + (rB_Mat[6,4] * rU_Opt_Seq[1,4]) + (rB_Mat[6,5] * rU_Opt_Seq[1,5]);

(* Iteration 6 - Forward State Prediction Step 2 (h=2): x_2 = A * x_1 + B * u_2 *)
rX_Pred_Horizon[2, 1] := (rA_Mat[1,1] * rX_Pred_Horizon[1,1]) + (rA_Mat[1,2] * rX_Pred_Horizon[1,2]) + (rA_Mat[1,3] * rX_Pred_Horizon[1,3]) + (rA_Mat[1,4] * rX_Pred_Horizon[1,4]) + (rA_Mat[1,5] * rX_Pred_Horizon[1,5]) + (rA_Mat[1,6] * rX_Pred_Horizon[1,6]) + (rB_Mat[1,1] * rU_Opt_Seq[2,1]) + (rB_Mat[1,2] * rU_Opt_Seq[2,2]) + (rB_Mat[1,3] * rU_Opt_Seq[2,3]) + (rB_Mat[1,4] * rU_Opt_Seq[2,4]) + (rB_Mat[1,5] * rU_Opt_Seq[2,5]);
rX_Pred_Horizon[2, 2] := (rA_Mat[2,1] * rX_Pred_Horizon[1,1]) + (rA_Mat[2,2] * rX_Pred_Horizon[1,2]) + (rA_Mat[2,3] * rX_Pred_Horizon[1,3]) + (rA_Mat[2,4] * rX_Pred_Horizon[1,4]) + (rA_Mat[2,5] * rX_Pred_Horizon[1,5]) + (rA_Mat[2,6] * rX_Pred_Horizon[1,6]) + (rB_Mat[2,1] * rU_Opt_Seq[2,1]) + (rB_Mat[2,2] * rU_Opt_Seq[2,2]) + (rB_Mat[2,3] * rU_Opt_Seq[2,3]) + (rB_Mat[2,4] * rU_Opt_Seq[2,4]) + (rB_Mat[2,5] * rU_Opt_Seq[2,5]);
rX_Pred_Horizon[2, 3] := (rA_Mat[3,1] * rX_Pred_Horizon[1,1]) + (rA_Mat[3,2] * rX_Pred_Horizon[1,2]) + (rA_Mat[3,3] * rX_Pred_Horizon[1,3]) + (rA_Mat[3,4] * rX_Pred_Horizon[1,4]) + (rA_Mat[3,5] * rX_Pred_Horizon[1,5]) + (rA_Mat[3,6] * rX_Pred_Horizon[1,6]) + (rB_Mat[3,1] * rU_Opt_Seq[2,1]) + (rB_Mat[3,2] * rU_Opt_Seq[2,2]) + (rB_Mat[3,3] * rU_Opt_Seq[2,3]) + (rB_Mat[3,4] * rU_Opt_Seq[2,4]) + (rB_Mat[3,5] * rU_Opt_Seq[2,5]);
rX_Pred_Horizon[2, 4] := (rA_Mat[4,1] * rX_Pred_Horizon[1,1]) + (rA_Mat[4,2] * rX_Pred_Horizon[1,2]) + (rA_Mat[4,3] * rX_Pred_Horizon[1,3]) + (rA_Mat[4,4] * rX_Pred_Horizon[1,4]) + (rA_Mat[4,5] * rX_Pred_Horizon[1,5]) + (rA_Mat[4,6] * rX_Pred_Horizon[1,6]) + (rB_Mat[4,1] * rU_Opt_Seq[2,1]) + (rB_Mat[4,2] * rU_Opt_Seq[2,2]) + (rB_Mat[4,3] * rU_Opt_Seq[2,3]) + (rB_Mat[4,4] * rU_Opt_Seq[2,4]) + (rB_Mat[4,5] * rU_Opt_Seq[2,5]);
rX_Pred_Horizon[2, 5] := (rA_Mat[5,1] * rX_Pred_Horizon[1,1]) + (rA_Mat[5,2] * rX_Pred_Horizon[1,2]) + (rA_Mat[5,3] * rX_Pred_Horizon[1,3]) + (rA_Mat[5,4] * rX_Pred_Horizon[1,4]) + (rA_Mat[5,5] * rX_Pred_Horizon[1,5]) + (rA_Mat[5,6] * rX_Pred_Horizon[1,6]) + (rB_Mat[5,1] * rU_Opt_Seq[2,1]) + (rB_Mat[5,2] * rU_Opt_Seq[2,2]) + (rB_Mat[5,3] * rU_Opt_Seq[2,3]) + (rB_Mat[5,4] * rU_Opt_Seq[2,4]) + (rB_Mat[5,5] * rU_Opt_Seq[2,5]);
rX_Pred_Horizon[2, 6] := (rA_Mat[6,1] * rX_Pred_Horizon[1,1]) + (rA_Mat[6,2] * rX_Pred_Horizon[1,2]) + (rA_Mat[6,3] * rX_Pred_Horizon[1,3]) + (rA_Mat[6,4] * rX_Pred_Horizon[1,4]) + (rA_Mat[6,5] * rX_Pred_Horizon[1,5]) + (rA_Mat[6,6] * rX_Pred_Horizon[1,6]) + (rB_Mat[6,1] * rU_Opt_Seq[2,1]) + (rB_Mat[6,2] * rU_Opt_Seq[2,2]) + (rB_Mat[6,3] * rU_Opt_Seq[2,3]) + (rB_Mat[6,4] * rU_Opt_Seq[2,4]) + (rB_Mat[6,5] * rU_Opt_Seq[2,5]);

(* Iteration 6 - Forward State Prediction Step 3 (h=3): x_3 = A * x_2 + B * u_3 *)
rX_Pred_Horizon[3, 1] := (rA_Mat[1,1] * rX_Pred_Horizon[2,1]) + (rA_Mat[1,2] * rX_Pred_Horizon[2,2]) + (rA_Mat[1,3] * rX_Pred_Horizon[2,3]) + (rA_Mat[1,4] * rX_Pred_Horizon[2,4]) + (rA_Mat[1,5] * rX_Pred_Horizon[2,5]) + (rA_Mat[1,6] * rX_Pred_Horizon[2,6]) + (rB_Mat[1,1] * rU_Opt_Seq[3,1]) + (rB_Mat[1,2] * rU_Opt_Seq[3,2]) + (rB_Mat[1,3] * rU_Opt_Seq[3,3]) + (rB_Mat[1,4] * rU_Opt_Seq[3,4]) + (rB_Mat[1,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[3, 2] := (rA_Mat[2,1] * rX_Pred_Horizon[2,1]) + (rA_Mat[2,2] * rX_Pred_Horizon[2,2]) + (rA_Mat[2,3] * rX_Pred_Horizon[2,3]) + (rA_Mat[2,4] * rX_Pred_Horizon[2,4]) + (rA_Mat[2,5] * rX_Pred_Horizon[2,5]) + (rA_Mat[2,6] * rX_Pred_Horizon[2,6]) + (rB_Mat[2,1] * rU_Opt_Seq[3,1]) + (rB_Mat[2,2] * rU_Opt_Seq[3,2]) + (rB_Mat[2,3] * rU_Opt_Seq[3,3]) + (rB_Mat[2,4] * rU_Opt_Seq[3,4]) + (rB_Mat[2,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[3, 3] := (rA_Mat[3,1] * rX_Pred_Horizon[2,1]) + (rA_Mat[3,2] * rX_Pred_Horizon[2,2]) + (rA_Mat[3,3] * rX_Pred_Horizon[2,3]) + (rA_Mat[3,4] * rX_Pred_Horizon[2,4]) + (rA_Mat[3,5] * rX_Pred_Horizon[2,5]) + (rA_Mat[3,6] * rX_Pred_Horizon[2,6]) + (rB_Mat[3,1] * rU_Opt_Seq[3,1]) + (rB_Mat[3,2] * rU_Opt_Seq[3,2]) + (rB_Mat[3,3] * rU_Opt_Seq[3,3]) + (rB_Mat[3,4] * rU_Opt_Seq[3,4]) + (rB_Mat[3,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[3, 4] := (rA_Mat[4,1] * rX_Pred_Horizon[2,1]) + (rA_Mat[4,2] * rX_Pred_Horizon[2,2]) + (rA_Mat[4,3] * rX_Pred_Horizon[2,3]) + (rA_Mat[4,4] * rX_Pred_Horizon[2,4]) + (rA_Mat[4,5] * rX_Pred_Horizon[2,5]) + (rA_Mat[4,6] * rX_Pred_Horizon[2,6]) + (rB_Mat[4,1] * rU_Opt_Seq[3,1]) + (rB_Mat[4,2] * rU_Opt_Seq[3,2]) + (rB_Mat[4,3] * rU_Opt_Seq[3,3]) + (rB_Mat[4,4] * rU_Opt_Seq[3,4]) + (rB_Mat[4,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[3, 5] := (rA_Mat[5,1] * rX_Pred_Horizon[2,1]) + (rA_Mat[5,2] * rX_Pred_Horizon[2,2]) + (rA_Mat[5,3] * rX_Pred_Horizon[2,3]) + (rA_Mat[5,4] * rX_Pred_Horizon[2,4]) + (rA_Mat[5,5] * rX_Pred_Horizon[2,5]) + (rA_Mat[5,6] * rX_Pred_Horizon[2,6]) + (rB_Mat[5,1] * rU_Opt_Seq[3,1]) + (rB_Mat[5,2] * rU_Opt_Seq[3,2]) + (rB_Mat[5,3] * rU_Opt_Seq[3,3]) + (rB_Mat[5,4] * rU_Opt_Seq[3,4]) + (rB_Mat[5,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[3, 6] := (rA_Mat[6,1] * rX_Pred_Horizon[2,1]) + (rA_Mat[6,2] * rX_Pred_Horizon[2,2]) + (rA_Mat[6,3] * rX_Pred_Horizon[2,3]) + (rA_Mat[6,4] * rX_Pred_Horizon[2,4]) + (rA_Mat[6,5] * rX_Pred_Horizon[2,5]) + (rA_Mat[6,6] * rX_Pred_Horizon[2,6]) + (rB_Mat[6,1] * rU_Opt_Seq[3,1]) + (rB_Mat[6,2] * rU_Opt_Seq[3,2]) + (rB_Mat[6,3] * rU_Opt_Seq[3,3]) + (rB_Mat[6,4] * rU_Opt_Seq[3,4]) + (rB_Mat[6,5] * rU_Opt_Seq[3,5]);

(* Iteration 6 - Forward State Prediction Step 4 (h=4): x_4 = A * x_3 + B * u_3 (held beyond Hu) *)
rX_Pred_Horizon[4, 1] := (rA_Mat[1,1] * rX_Pred_Horizon[3,1]) + (rA_Mat[1,2] * rX_Pred_Horizon[3,2]) + (rA_Mat[1,3] * rX_Pred_Horizon[3,3]) + (rA_Mat[1,4] * rX_Pred_Horizon[3,4]) + (rA_Mat[1,5] * rX_Pred_Horizon[3,5]) + (rA_Mat[1,6] * rX_Pred_Horizon[3,6]) + (rB_Mat[1,1] * rU_Opt_Seq[3,1]) + (rB_Mat[1,2] * rU_Opt_Seq[3,2]) + (rB_Mat[1,3] * rU_Opt_Seq[3,3]) + (rB_Mat[1,4] * rU_Opt_Seq[3,4]) + (rB_Mat[1,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[4, 2] := (rA_Mat[2,1] * rX_Pred_Horizon[3,1]) + (rA_Mat[2,2] * rX_Pred_Horizon[3,2]) + (rA_Mat[2,3] * rX_Pred_Horizon[3,3]) + (rA_Mat[2,4] * rX_Pred_Horizon[3,4]) + (rA_Mat[2,5] * rX_Pred_Horizon[3,5]) + (rA_Mat[2,6] * rX_Pred_Horizon[3,6]) + (rB_Mat[2,1] * rU_Opt_Seq[3,1]) + (rB_Mat[2,2] * rU_Opt_Seq[3,2]) + (rB_Mat[2,3] * rU_Opt_Seq[3,3]) + (rB_Mat[2,4] * rU_Opt_Seq[3,4]) + (rB_Mat[2,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[4, 3] := (rA_Mat[3,1] * rX_Pred_Horizon[3,1]) + (rA_Mat[3,2] * rX_Pred_Horizon[3,2]) + (rA_Mat[3,3] * rX_Pred_Horizon[3,3]) + (rA_Mat[3,4] * rX_Pred_Horizon[3,4]) + (rA_Mat[3,5] * rX_Pred_Horizon[3,5]) + (rA_Mat[3,6] * rX_Pred_Horizon[3,6]) + (rB_Mat[3,1] * rU_Opt_Seq[3,1]) + (rB_Mat[3,2] * rU_Opt_Seq[3,2]) + (rB_Mat[3,3] * rU_Opt_Seq[3,3]) + (rB_Mat[3,4] * rU_Opt_Seq[3,4]) + (rB_Mat[3,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[4, 4] := (rA_Mat[4,1] * rX_Pred_Horizon[3,1]) + (rA_Mat[4,2] * rX_Pred_Horizon[3,2]) + (rA_Mat[4,3] * rX_Pred_Horizon[3,3]) + (rA_Mat[4,4] * rX_Pred_Horizon[3,4]) + (rA_Mat[4,5] * rX_Pred_Horizon[3,5]) + (rA_Mat[4,6] * rX_Pred_Horizon[3,6]) + (rB_Mat[4,1] * rU_Opt_Seq[3,1]) + (rB_Mat[4,2] * rU_Opt_Seq[3,2]) + (rB_Mat[4,3] * rU_Opt_Seq[3,3]) + (rB_Mat[4,4] * rU_Opt_Seq[3,4]) + (rB_Mat[4,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[4, 5] := (rA_Mat[5,1] * rX_Pred_Horizon[3,1]) + (rA_Mat[5,2] * rX_Pred_Horizon[3,2]) + (rA_Mat[5,3] * rX_Pred_Horizon[3,3]) + (rA_Mat[5,4] * rX_Pred_Horizon[3,4]) + (rA_Mat[5,5] * rX_Pred_Horizon[3,5]) + (rA_Mat[5,6] * rX_Pred_Horizon[3,6]) + (rB_Mat[5,1] * rU_Opt_Seq[3,1]) + (rB_Mat[5,2] * rU_Opt_Seq[3,2]) + (rB_Mat[5,3] * rU_Opt_Seq[3,3]) + (rB_Mat[5,4] * rU_Opt_Seq[3,4]) + (rB_Mat[5,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[4, 6] := (rA_Mat[6,1] * rX_Pred_Horizon[3,1]) + (rA_Mat[6,2] * rX_Pred_Horizon[3,2]) + (rA_Mat[6,3] * rX_Pred_Horizon[3,3]) + (rA_Mat[6,4] * rX_Pred_Horizon[3,4]) + (rA_Mat[6,5] * rX_Pred_Horizon[3,5]) + (rA_Mat[6,6] * rX_Pred_Horizon[3,6]) + (rB_Mat[6,1] * rU_Opt_Seq[3,1]) + (rB_Mat[6,2] * rU_Opt_Seq[3,2]) + (rB_Mat[6,3] * rU_Opt_Seq[3,3]) + (rB_Mat[6,4] * rU_Opt_Seq[3,4]) + (rB_Mat[6,5] * rU_Opt_Seq[3,5]);

(* Iteration 6 - Forward State Prediction Step 5 (h=5): x_5 = A * x_4 + B * u_3 (held beyond Hu) *)
rX_Pred_Horizon[5, 1] := (rA_Mat[1,1] * rX_Pred_Horizon[4,1]) + (rA_Mat[1,2] * rX_Pred_Horizon[4,2]) + (rA_Mat[1,3] * rX_Pred_Horizon[4,3]) + (rA_Mat[1,4] * rX_Pred_Horizon[4,4]) + (rA_Mat[1,5] * rX_Pred_Horizon[4,5]) + (rA_Mat[1,6] * rX_Pred_Horizon[4,6]) + (rB_Mat[1,1] * rU_Opt_Seq[3,1]) + (rB_Mat[1,2] * rU_Opt_Seq[3,2]) + (rB_Mat[1,3] * rU_Opt_Seq[3,3]) + (rB_Mat[1,4] * rU_Opt_Seq[3,4]) + (rB_Mat[1,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[5, 2] := (rA_Mat[2,1] * rX_Pred_Horizon[4,1]) + (rA_Mat[2,2] * rX_Pred_Horizon[4,2]) + (rA_Mat[2,3] * rX_Pred_Horizon[4,3]) + (rA_Mat[2,4] * rX_Pred_Horizon[4,4]) + (rA_Mat[2,5] * rX_Pred_Horizon[4,5]) + (rA_Mat[2,6] * rX_Pred_Horizon[4,6]) + (rB_Mat[2,1] * rU_Opt_Seq[3,1]) + (rB_Mat[2,2] * rU_Opt_Seq[3,2]) + (rB_Mat[2,3] * rU_Opt_Seq[3,3]) + (rB_Mat[2,4] * rU_Opt_Seq[3,4]) + (rB_Mat[2,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[5, 3] := (rA_Mat[3,1] * rX_Pred_Horizon[4,1]) + (rA_Mat[3,2] * rX_Pred_Horizon[4,2]) + (rA_Mat[3,3] * rX_Pred_Horizon[4,3]) + (rA_Mat[3,4] * rX_Pred_Horizon[4,4]) + (rA_Mat[3,5] * rX_Pred_Horizon[4,5]) + (rA_Mat[3,6] * rX_Pred_Horizon[4,6]) + (rB_Mat[3,1] * rU_Opt_Seq[3,1]) + (rB_Mat[3,2] * rU_Opt_Seq[3,2]) + (rB_Mat[3,3] * rU_Opt_Seq[3,3]) + (rB_Mat[3,4] * rU_Opt_Seq[3,4]) + (rB_Mat[3,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[5, 4] := (rA_Mat[4,1] * rX_Pred_Horizon[4,1]) + (rA_Mat[4,2] * rX_Pred_Horizon[4,2]) + (rA_Mat[4,3] * rX_Pred_Horizon[4,3]) + (rA_Mat[4,4] * rX_Pred_Horizon[4,4]) + (rA_Mat[4,5] * rX_Pred_Horizon[4,5]) + (rA_Mat[4,6] * rX_Pred_Horizon[4,6]) + (rB_Mat[4,1] * rU_Opt_Seq[3,1]) + (rB_Mat[4,2] * rU_Opt_Seq[3,2]) + (rB_Mat[4,3] * rU_Opt_Seq[3,3]) + (rB_Mat[4,4] * rU_Opt_Seq[3,4]) + (rB_Mat[4,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[5, 5] := (rA_Mat[5,1] * rX_Pred_Horizon[4,1]) + (rA_Mat[5,2] * rX_Pred_Horizon[4,2]) + (rA_Mat[5,3] * rX_Pred_Horizon[4,3]) + (rA_Mat[5,4] * rX_Pred_Horizon[4,4]) + (rA_Mat[5,5] * rX_Pred_Horizon[4,5]) + (rA_Mat[5,6] * rX_Pred_Horizon[4,6]) + (rB_Mat[5,1] * rU_Opt_Seq[3,1]) + (rB_Mat[5,2] * rU_Opt_Seq[3,2]) + (rB_Mat[5,3] * rU_Opt_Seq[3,3]) + (rB_Mat[5,4] * rU_Opt_Seq[3,4]) + (rB_Mat[5,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[5, 6] := (rA_Mat[6,1] * rX_Pred_Horizon[4,1]) + (rA_Mat[6,2] * rX_Pred_Horizon[4,2]) + (rA_Mat[6,3] * rX_Pred_Horizon[4,3]) + (rA_Mat[6,4] * rX_Pred_Horizon[4,4]) + (rA_Mat[6,5] * rX_Pred_Horizon[4,5]) + (rA_Mat[6,6] * rX_Pred_Horizon[4,6]) + (rB_Mat[6,1] * rU_Opt_Seq[3,1]) + (rB_Mat[6,2] * rU_Opt_Seq[3,2]) + (rB_Mat[6,3] * rU_Opt_Seq[3,3]) + (rB_Mat[6,4] * rU_Opt_Seq[3,4]) + (rB_Mat[6,5] * rU_Opt_Seq[3,5]);

(* Iteration 6 - Evaluate Objective Function Cost J *)
rMPC_Cost_J := 0.0;
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[1] * (rX_Pred_Horizon[1,1] - rX_Target[1,1]) * (rX_Pred_Horizon[1,1] - rX_Target[1,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[2] * (rX_Pred_Horizon[1,2] - rX_Target[1,2]) * (rX_Pred_Horizon[1,2] - rX_Target[1,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[3] * (rX_Pred_Horizon[1,3] - rX_Target[1,3]) * (rX_Pred_Horizon[1,3] - rX_Target[1,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[4] * (rX_Pred_Horizon[1,4] - rX_Target[1,4]) * (rX_Pred_Horizon[1,4] - rX_Target[1,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[5] * (rX_Pred_Horizon[1,5] - rX_Target[1,5]) * (rX_Pred_Horizon[1,5] - rX_Target[1,5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[6] * (rX_Pred_Horizon[1,6] - rX_Target[1,6]) * (rX_Pred_Horizon[1,6] - rX_Target[1,6]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[1] * (rX_Pred_Horizon[2,1] - rX_Target[2,1]) * (rX_Pred_Horizon[2,1] - rX_Target[2,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[2] * (rX_Pred_Horizon[2,2] - rX_Target[2,2]) * (rX_Pred_Horizon[2,2] - rX_Target[2,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[3] * (rX_Pred_Horizon[2,3] - rX_Target[2,3]) * (rX_Pred_Horizon[2,3] - rX_Target[2,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[4] * (rX_Pred_Horizon[2,4] - rX_Target[2,4]) * (rX_Pred_Horizon[2,4] - rX_Target[2,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[5] * (rX_Pred_Horizon[2,5] - rX_Target[2,5]) * (rX_Pred_Horizon[2,5] - rX_Target[2,5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[6] * (rX_Pred_Horizon[2,6] - rX_Target[2,6]) * (rX_Pred_Horizon[2,6] - rX_Target[2,6]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[1] * (rX_Pred_Horizon[3,1] - rX_Target[3,1]) * (rX_Pred_Horizon[3,1] - rX_Target[3,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[2] * (rX_Pred_Horizon[3,2] - rX_Target[3,2]) * (rX_Pred_Horizon[3,2] - rX_Target[3,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[3] * (rX_Pred_Horizon[3,3] - rX_Target[3,3]) * (rX_Pred_Horizon[3,3] - rX_Target[3,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[4] * (rX_Pred_Horizon[3,4] - rX_Target[3,4]) * (rX_Pred_Horizon[3,4] - rX_Target[3,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[5] * (rX_Pred_Horizon[3,5] - rX_Target[3,5]) * (rX_Pred_Horizon[3,5] - rX_Target[3,5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[6] * (rX_Pred_Horizon[3,6] - rX_Target[3,6]) * (rX_Pred_Horizon[3,6] - rX_Target[3,6]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[1] * (rX_Pred_Horizon[4,1] - rX_Target[4,1]) * (rX_Pred_Horizon[4,1] - rX_Target[4,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[2] * (rX_Pred_Horizon[4,2] - rX_Target[4,2]) * (rX_Pred_Horizon[4,2] - rX_Target[4,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[3] * (rX_Pred_Horizon[4,3] - rX_Target[4,3]) * (rX_Pred_Horizon[4,3] - rX_Target[4,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[4] * (rX_Pred_Horizon[4,4] - rX_Target[4,4]) * (rX_Pred_Horizon[4,4] - rX_Target[4,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[5] * (rX_Pred_Horizon[4,5] - rX_Target[4,5]) * (rX_Pred_Horizon[4,5] - rX_Target[4,5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[6] * (rX_Pred_Horizon[4,6] - rX_Target[4,6]) * (rX_Pred_Horizon[4,6] - rX_Target[4,6]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[1] * (rX_Pred_Horizon[5,1] - rX_Target[5,1]) * (rX_Pred_Horizon[5,1] - rX_Target[5,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[2] * (rX_Pred_Horizon[5,2] - rX_Target[5,2]) * (rX_Pred_Horizon[5,2] - rX_Target[5,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[3] * (rX_Pred_Horizon[5,3] - rX_Target[5,3]) * (rX_Pred_Horizon[5,3] - rX_Target[5,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[4] * (rX_Pred_Horizon[5,4] - rX_Target[5,4]) * (rX_Pred_Horizon[5,4] - rX_Target[5,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[5] * (rX_Pred_Horizon[5,5] - rX_Target[5,5]) * (rX_Pred_Horizon[5,5] - rX_Target[5,5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[6] * (rX_Pred_Horizon[5,6] - rX_Target[5,6]) * (rX_Pred_Horizon[5,6] - rX_Target[5,6]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rP_Diag[1] * (rX_Pred_Horizon[5,1] - rX_Target[5,1]) * (rX_Pred_Horizon[5,1] - rX_Target[5,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rP_Diag[2] * (rX_Pred_Horizon[5,2] - rX_Target[5,2]) * (rX_Pred_Horizon[5,2] - rX_Target[5,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rP_Diag[3] * (rX_Pred_Horizon[5,3] - rX_Target[5,3]) * (rX_Pred_Horizon[5,3] - rX_Target[5,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rP_Diag[4] * (rX_Pred_Horizon[5,4] - rX_Target[5,4]) * (rX_Pred_Horizon[5,4] - rX_Target[5,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rP_Diag[5] * (rX_Pred_Horizon[5,5] - rX_Target[5,5]) * (rX_Pred_Horizon[5,5] - rX_Target[5,5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rP_Diag[6] * (rX_Pred_Horizon[5,6] - rX_Target[5,6]) * (rX_Pred_Horizon[5,6] - rX_Target[5,6]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[1] * rU_Opt_Seq[1,1] * rU_Opt_Seq[1,1]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[2] * rU_Opt_Seq[1,2] * rU_Opt_Seq[1,2]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[3] * rU_Opt_Seq[1,3] * rU_Opt_Seq[1,3]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[4] * rU_Opt_Seq[1,4] * rU_Opt_Seq[1,4]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[5] * rU_Opt_Seq[1,5] * rU_Opt_Seq[1,5]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[1] * rU_Opt_Seq[2,1] * rU_Opt_Seq[2,1]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[2] * rU_Opt_Seq[2,2] * rU_Opt_Seq[2,2]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[3] * rU_Opt_Seq[2,3] * rU_Opt_Seq[2,3]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[4] * rU_Opt_Seq[2,4] * rU_Opt_Seq[2,4]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[5] * rU_Opt_Seq[2,5] * rU_Opt_Seq[2,5]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[1] * rU_Opt_Seq[3,1] * rU_Opt_Seq[3,1]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[2] * rU_Opt_Seq[3,2] * rU_Opt_Seq[3,2]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[3] * rU_Opt_Seq[3,3] * rU_Opt_Seq[3,3]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[4] * rU_Opt_Seq[3,4] * rU_Opt_Seq[3,4]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[5] * rU_Opt_Seq[3,5] * rU_Opt_Seq[3,5]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[1] * (rU_Opt_Seq[1,1] - a_u_prev[1]) * (rU_Opt_Seq[1,1] - a_u_prev[1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[1] * (rU_Opt_Seq[2,1] - rU_Opt_Seq[1,1]) * (rU_Opt_Seq[2,1] - rU_Opt_Seq[1,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[1] * (rU_Opt_Seq[3,1] - rU_Opt_Seq[2,1]) * (rU_Opt_Seq[3,1] - rU_Opt_Seq[2,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[2] * (rU_Opt_Seq[1,2] - a_u_prev[2]) * (rU_Opt_Seq[1,2] - a_u_prev[2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[2] * (rU_Opt_Seq[2,2] - rU_Opt_Seq[1,2]) * (rU_Opt_Seq[2,2] - rU_Opt_Seq[1,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[2] * (rU_Opt_Seq[3,2] - rU_Opt_Seq[2,2]) * (rU_Opt_Seq[3,2] - rU_Opt_Seq[2,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[3] * (rU_Opt_Seq[1,3] - a_u_prev[3]) * (rU_Opt_Seq[1,3] - a_u_prev[3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[3] * (rU_Opt_Seq[2,3] - rU_Opt_Seq[1,3]) * (rU_Opt_Seq[2,3] - rU_Opt_Seq[1,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[3] * (rU_Opt_Seq[3,3] - rU_Opt_Seq[2,3]) * (rU_Opt_Seq[3,3] - rU_Opt_Seq[2,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[4] * (rU_Opt_Seq[1,4] - a_u_prev[4]) * (rU_Opt_Seq[1,4] - a_u_prev[4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[4] * (rU_Opt_Seq[2,4] - rU_Opt_Seq[1,4]) * (rU_Opt_Seq[2,4] - rU_Opt_Seq[1,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[4] * (rU_Opt_Seq[3,4] - rU_Opt_Seq[2,4]) * (rU_Opt_Seq[3,4] - rU_Opt_Seq[2,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[5] * (rU_Opt_Seq[1,5] - a_u_prev[5]) * (rU_Opt_Seq[1,5] - a_u_prev[5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[5] * (rU_Opt_Seq[2,5] - rU_Opt_Seq[1,5]) * (rU_Opt_Seq[2,5] - rU_Opt_Seq[1,5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[5] * (rU_Opt_Seq[3,5] - rU_Opt_Seq[2,5]) * (rU_Opt_Seq[3,5] - rU_Opt_Seq[2,5]));

(* Iteration 6 - Backward Adjoint Costate Propagation: lambda_h = A^T * lambda_{h+1} + Q * (x_h - x_ref) *)
(* Terminal Costate at h=5: lambda_5 = (P + Q) * (x_5 - x_target_5) *)
rLambda_Costate[5, 1] := (rP_Diag[1] + rQ_Diag[1]) * (rX_Pred_Horizon[5,1] - rX_Target[5,1]);
rLambda_Costate[5, 2] := (rP_Diag[2] + rQ_Diag[2]) * (rX_Pred_Horizon[5,2] - rX_Target[5,2]);
rLambda_Costate[5, 3] := (rP_Diag[3] + rQ_Diag[3]) * (rX_Pred_Horizon[5,3] - rX_Target[5,3]);
rLambda_Costate[5, 4] := (rP_Diag[4] + rQ_Diag[4]) * (rX_Pred_Horizon[5,4] - rX_Target[5,4]);
rLambda_Costate[5, 5] := (rP_Diag[5] + rQ_Diag[5]) * (rX_Pred_Horizon[5,5] - rX_Target[5,5]);
rLambda_Costate[5, 6] := (rP_Diag[6] + rQ_Diag[6]) * (rX_Pred_Horizon[5,6] - rX_Target[5,6]);

(* Adjoint Costate at h=4: lambda_4 = A^T * lambda_5 + Q * (x_4 - x_target_4) *)
rLambda_Costate[4, 1] := (rA_Mat[1,1] * rLambda_Costate[5,1]) + (rA_Mat[2,1] * rLambda_Costate[5,2]) + (rA_Mat[3,1] * rLambda_Costate[5,3]) + (rA_Mat[4,1] * rLambda_Costate[5,4]) + (rA_Mat[5,1] * rLambda_Costate[5,5]) + (rA_Mat[6,1] * rLambda_Costate[5,6]) + (rQ_Diag[1] * (rX_Pred_Horizon[4,1] - rX_Target[4,1]));
rLambda_Costate[4, 2] := (rA_Mat[1,2] * rLambda_Costate[5,1]) + (rA_Mat[2,2] * rLambda_Costate[5,2]) + (rA_Mat[3,2] * rLambda_Costate[5,3]) + (rA_Mat[4,2] * rLambda_Costate[5,4]) + (rA_Mat[5,2] * rLambda_Costate[5,5]) + (rA_Mat[6,2] * rLambda_Costate[5,6]) + (rQ_Diag[2] * (rX_Pred_Horizon[4,2] - rX_Target[4,2]));
rLambda_Costate[4, 3] := (rA_Mat[1,3] * rLambda_Costate[5,1]) + (rA_Mat[2,3] * rLambda_Costate[5,2]) + (rA_Mat[3,3] * rLambda_Costate[5,3]) + (rA_Mat[4,3] * rLambda_Costate[5,4]) + (rA_Mat[5,3] * rLambda_Costate[5,5]) + (rA_Mat[6,3] * rLambda_Costate[5,6]) + (rQ_Diag[3] * (rX_Pred_Horizon[4,3] - rX_Target[4,3]));
rLambda_Costate[4, 4] := (rA_Mat[1,4] * rLambda_Costate[5,1]) + (rA_Mat[2,4] * rLambda_Costate[5,2]) + (rA_Mat[3,4] * rLambda_Costate[5,3]) + (rA_Mat[4,4] * rLambda_Costate[5,4]) + (rA_Mat[5,4] * rLambda_Costate[5,5]) + (rA_Mat[6,4] * rLambda_Costate[5,6]) + (rQ_Diag[4] * (rX_Pred_Horizon[4,4] - rX_Target[4,4]));
rLambda_Costate[4, 5] := (rA_Mat[1,5] * rLambda_Costate[5,1]) + (rA_Mat[2,5] * rLambda_Costate[5,2]) + (rA_Mat[3,5] * rLambda_Costate[5,3]) + (rA_Mat[4,5] * rLambda_Costate[5,4]) + (rA_Mat[5,5] * rLambda_Costate[5,5]) + (rA_Mat[6,5] * rLambda_Costate[5,6]) + (rQ_Diag[5] * (rX_Pred_Horizon[4,5] - rX_Target[4,5]));
rLambda_Costate[4, 6] := (rA_Mat[1,6] * rLambda_Costate[5,1]) + (rA_Mat[2,6] * rLambda_Costate[5,2]) + (rA_Mat[3,6] * rLambda_Costate[5,3]) + (rA_Mat[4,6] * rLambda_Costate[5,4]) + (rA_Mat[5,6] * rLambda_Costate[5,5]) + (rA_Mat[6,6] * rLambda_Costate[5,6]) + (rQ_Diag[6] * (rX_Pred_Horizon[4,6] - rX_Target[4,6]));

(* Adjoint Costate at h=3: lambda_3 = A^T * lambda_4 + Q * (x_3 - x_target_3) *)
rLambda_Costate[3, 1] := (rA_Mat[1,1] * rLambda_Costate[4,1]) + (rA_Mat[2,1] * rLambda_Costate[4,2]) + (rA_Mat[3,1] * rLambda_Costate[4,3]) + (rA_Mat[4,1] * rLambda_Costate[4,4]) + (rA_Mat[5,1] * rLambda_Costate[4,5]) + (rA_Mat[6,1] * rLambda_Costate[4,6]) + (rQ_Diag[1] * (rX_Pred_Horizon[3,1] - rX_Target[3,1]));
rLambda_Costate[3, 2] := (rA_Mat[1,2] * rLambda_Costate[4,1]) + (rA_Mat[2,2] * rLambda_Costate[4,2]) + (rA_Mat[3,2] * rLambda_Costate[4,3]) + (rA_Mat[4,2] * rLambda_Costate[4,4]) + (rA_Mat[5,2] * rLambda_Costate[4,5]) + (rA_Mat[6,2] * rLambda_Costate[4,6]) + (rQ_Diag[2] * (rX_Pred_Horizon[3,2] - rX_Target[3,2]));
rLambda_Costate[3, 3] := (rA_Mat[1,3] * rLambda_Costate[4,1]) + (rA_Mat[2,3] * rLambda_Costate[4,2]) + (rA_Mat[3,3] * rLambda_Costate[4,3]) + (rA_Mat[4,3] * rLambda_Costate[4,4]) + (rA_Mat[5,3] * rLambda_Costate[4,5]) + (rA_Mat[6,3] * rLambda_Costate[4,6]) + (rQ_Diag[3] * (rX_Pred_Horizon[3,3] - rX_Target[3,3]));
rLambda_Costate[3, 4] := (rA_Mat[1,4] * rLambda_Costate[4,1]) + (rA_Mat[2,4] * rLambda_Costate[4,2]) + (rA_Mat[3,4] * rLambda_Costate[4,3]) + (rA_Mat[4,4] * rLambda_Costate[4,4]) + (rA_Mat[5,4] * rLambda_Costate[4,5]) + (rA_Mat[6,4] * rLambda_Costate[4,6]) + (rQ_Diag[4] * (rX_Pred_Horizon[3,4] - rX_Target[3,4]));
rLambda_Costate[3, 5] := (rA_Mat[1,5] * rLambda_Costate[4,1]) + (rA_Mat[2,5] * rLambda_Costate[4,2]) + (rA_Mat[3,5] * rLambda_Costate[4,3]) + (rA_Mat[4,5] * rLambda_Costate[4,4]) + (rA_Mat[5,5] * rLambda_Costate[4,5]) + (rA_Mat[6,5] * rLambda_Costate[4,6]) + (rQ_Diag[5] * (rX_Pred_Horizon[3,5] - rX_Target[3,5]));
rLambda_Costate[3, 6] := (rA_Mat[1,6] * rLambda_Costate[4,1]) + (rA_Mat[2,6] * rLambda_Costate[4,2]) + (rA_Mat[3,6] * rLambda_Costate[4,3]) + (rA_Mat[4,6] * rLambda_Costate[4,4]) + (rA_Mat[5,6] * rLambda_Costate[4,5]) + (rA_Mat[6,6] * rLambda_Costate[4,6]) + (rQ_Diag[6] * (rX_Pred_Horizon[3,6] - rX_Target[3,6]));

(* Adjoint Costate at h=2: lambda_2 = A^T * lambda_3 + Q * (x_2 - x_target_2) *)
rLambda_Costate[2, 1] := (rA_Mat[1,1] * rLambda_Costate[3,1]) + (rA_Mat[2,1] * rLambda_Costate[3,2]) + (rA_Mat[3,1] * rLambda_Costate[3,3]) + (rA_Mat[4,1] * rLambda_Costate[3,4]) + (rA_Mat[5,1] * rLambda_Costate[3,5]) + (rA_Mat[6,1] * rLambda_Costate[3,6]) + (rQ_Diag[1] * (rX_Pred_Horizon[2,1] - rX_Target[2,1]));
rLambda_Costate[2, 2] := (rA_Mat[1,2] * rLambda_Costate[3,1]) + (rA_Mat[2,2] * rLambda_Costate[3,2]) + (rA_Mat[3,2] * rLambda_Costate[3,3]) + (rA_Mat[4,2] * rLambda_Costate[3,4]) + (rA_Mat[5,2] * rLambda_Costate[3,5]) + (rA_Mat[6,2] * rLambda_Costate[3,6]) + (rQ_Diag[2] * (rX_Pred_Horizon[2,2] - rX_Target[2,2]));
rLambda_Costate[2, 3] := (rA_Mat[1,3] * rLambda_Costate[3,1]) + (rA_Mat[2,3] * rLambda_Costate[3,2]) + (rA_Mat[3,3] * rLambda_Costate[3,3]) + (rA_Mat[4,3] * rLambda_Costate[3,4]) + (rA_Mat[5,3] * rLambda_Costate[3,5]) + (rA_Mat[6,3] * rLambda_Costate[3,6]) + (rQ_Diag[3] * (rX_Pred_Horizon[2,3] - rX_Target[2,3]));
rLambda_Costate[2, 4] := (rA_Mat[1,4] * rLambda_Costate[3,1]) + (rA_Mat[2,4] * rLambda_Costate[3,2]) + (rA_Mat[3,4] * rLambda_Costate[3,3]) + (rA_Mat[4,4] * rLambda_Costate[3,4]) + (rA_Mat[5,4] * rLambda_Costate[3,5]) + (rA_Mat[6,4] * rLambda_Costate[3,6]) + (rQ_Diag[4] * (rX_Pred_Horizon[2,4] - rX_Target[2,4]));
rLambda_Costate[2, 5] := (rA_Mat[1,5] * rLambda_Costate[3,1]) + (rA_Mat[2,5] * rLambda_Costate[3,2]) + (rA_Mat[3,5] * rLambda_Costate[3,3]) + (rA_Mat[4,5] * rLambda_Costate[3,4]) + (rA_Mat[5,5] * rLambda_Costate[3,5]) + (rA_Mat[6,5] * rLambda_Costate[3,6]) + (rQ_Diag[5] * (rX_Pred_Horizon[2,5] - rX_Target[2,5]));
rLambda_Costate[2, 6] := (rA_Mat[1,6] * rLambda_Costate[3,1]) + (rA_Mat[2,6] * rLambda_Costate[3,2]) + (rA_Mat[3,6] * rLambda_Costate[3,3]) + (rA_Mat[4,6] * rLambda_Costate[3,4]) + (rA_Mat[5,6] * rLambda_Costate[3,5]) + (rA_Mat[6,6] * rLambda_Costate[3,6]) + (rQ_Diag[6] * (rX_Pred_Horizon[2,6] - rX_Target[2,6]));

(* Adjoint Costate at h=1: lambda_1 = A^T * lambda_2 + Q * (x_1 - x_target_1) *)
rLambda_Costate[1, 1] := (rA_Mat[1,1] * rLambda_Costate[2,1]) + (rA_Mat[2,1] * rLambda_Costate[2,2]) + (rA_Mat[3,1] * rLambda_Costate[2,3]) + (rA_Mat[4,1] * rLambda_Costate[2,4]) + (rA_Mat[5,1] * rLambda_Costate[2,5]) + (rA_Mat[6,1] * rLambda_Costate[2,6]) + (rQ_Diag[1] * (rX_Pred_Horizon[1,1] - rX_Target[1,1]));
rLambda_Costate[1, 2] := (rA_Mat[1,2] * rLambda_Costate[2,1]) + (rA_Mat[2,2] * rLambda_Costate[2,2]) + (rA_Mat[3,2] * rLambda_Costate[2,3]) + (rA_Mat[4,2] * rLambda_Costate[2,4]) + (rA_Mat[5,2] * rLambda_Costate[2,5]) + (rA_Mat[6,2] * rLambda_Costate[2,6]) + (rQ_Diag[2] * (rX_Pred_Horizon[1,2] - rX_Target[1,2]));
rLambda_Costate[1, 3] := (rA_Mat[1,3] * rLambda_Costate[2,1]) + (rA_Mat[2,3] * rLambda_Costate[2,2]) + (rA_Mat[3,3] * rLambda_Costate[2,3]) + (rA_Mat[4,3] * rLambda_Costate[2,4]) + (rA_Mat[5,3] * rLambda_Costate[2,5]) + (rA_Mat[6,3] * rLambda_Costate[2,6]) + (rQ_Diag[3] * (rX_Pred_Horizon[1,3] - rX_Target[1,3]));
rLambda_Costate[1, 4] := (rA_Mat[1,4] * rLambda_Costate[2,1]) + (rA_Mat[2,4] * rLambda_Costate[2,2]) + (rA_Mat[3,4] * rLambda_Costate[2,3]) + (rA_Mat[4,4] * rLambda_Costate[2,4]) + (rA_Mat[5,4] * rLambda_Costate[2,5]) + (rA_Mat[6,4] * rLambda_Costate[2,6]) + (rQ_Diag[4] * (rX_Pred_Horizon[1,4] - rX_Target[1,4]));
rLambda_Costate[1, 5] := (rA_Mat[1,5] * rLambda_Costate[2,1]) + (rA_Mat[2,5] * rLambda_Costate[2,2]) + (rA_Mat[3,5] * rLambda_Costate[2,3]) + (rA_Mat[4,5] * rLambda_Costate[2,4]) + (rA_Mat[5,5] * rLambda_Costate[2,5]) + (rA_Mat[6,5] * rLambda_Costate[2,6]) + (rQ_Diag[5] * (rX_Pred_Horizon[1,5] - rX_Target[1,5]));
rLambda_Costate[1, 6] := (rA_Mat[1,6] * rLambda_Costate[2,1]) + (rA_Mat[2,6] * rLambda_Costate[2,2]) + (rA_Mat[3,6] * rLambda_Costate[2,3]) + (rA_Mat[4,6] * rLambda_Costate[2,4]) + (rA_Mat[5,6] * rLambda_Costate[2,5]) + (rA_Mat[6,6] * rLambda_Costate[2,6]) + (rQ_Diag[6] * (rX_Pred_Horizon[1,6] - rX_Target[1,6]));

(* Iteration 6 - Analytical Gradient Computation w.r.t. Control Inputs u_h *)
rMPC_GradNormSq := 0.0;
(* Gradient for u_1 (h=1) *)
rGrad_J[1, 1] := (rB_Mat[1,1] * rLambda_Costate[1,1]) + (rB_Mat[2,1] * rLambda_Costate[1,2]) + (rB_Mat[3,1] * rLambda_Costate[1,3]) + (rB_Mat[4,1] * rLambda_Costate[1,4]) + (rB_Mat[5,1] * rLambda_Costate[1,5]) + (rB_Mat[6,1] * rLambda_Costate[1,6]) + (rR_Diag[1] * rU_Opt_Seq[1,1]) + (rS_Diag[1] * (rU_Opt_Seq[1,1] - a_u_prev[1])) - (rS_Diag[1] * (rU_Opt_Seq[2,1] - rU_Opt_Seq[1,1]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[1, 1] * rGrad_J[1, 1]);
rGrad_J[1, 2] := (rB_Mat[1,2] * rLambda_Costate[1,1]) + (rB_Mat[2,2] * rLambda_Costate[1,2]) + (rB_Mat[3,2] * rLambda_Costate[1,3]) + (rB_Mat[4,2] * rLambda_Costate[1,4]) + (rB_Mat[5,2] * rLambda_Costate[1,5]) + (rB_Mat[6,2] * rLambda_Costate[1,6]) + (rR_Diag[2] * rU_Opt_Seq[1,2]) + (rS_Diag[2] * (rU_Opt_Seq[1,2] - a_u_prev[2])) - (rS_Diag[2] * (rU_Opt_Seq[2,2] - rU_Opt_Seq[1,2]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[1, 2] * rGrad_J[1, 2]);
rGrad_J[1, 3] := (rB_Mat[1,3] * rLambda_Costate[1,1]) + (rB_Mat[2,3] * rLambda_Costate[1,2]) + (rB_Mat[3,3] * rLambda_Costate[1,3]) + (rB_Mat[4,3] * rLambda_Costate[1,4]) + (rB_Mat[5,3] * rLambda_Costate[1,5]) + (rB_Mat[6,3] * rLambda_Costate[1,6]) + (rR_Diag[3] * rU_Opt_Seq[1,3]) + (rS_Diag[3] * (rU_Opt_Seq[1,3] - a_u_prev[3])) - (rS_Diag[3] * (rU_Opt_Seq[2,3] - rU_Opt_Seq[1,3]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[1, 3] * rGrad_J[1, 3]);
rGrad_J[1, 4] := (rB_Mat[1,4] * rLambda_Costate[1,1]) + (rB_Mat[2,4] * rLambda_Costate[1,2]) + (rB_Mat[3,4] * rLambda_Costate[1,3]) + (rB_Mat[4,4] * rLambda_Costate[1,4]) + (rB_Mat[5,4] * rLambda_Costate[1,5]) + (rB_Mat[6,4] * rLambda_Costate[1,6]) + (rR_Diag[4] * rU_Opt_Seq[1,4]) + (rS_Diag[4] * (rU_Opt_Seq[1,4] - a_u_prev[4])) - (rS_Diag[4] * (rU_Opt_Seq[2,4] - rU_Opt_Seq[1,4]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[1, 4] * rGrad_J[1, 4]);
rGrad_J[1, 5] := (rB_Mat[1,5] * rLambda_Costate[1,1]) + (rB_Mat[2,5] * rLambda_Costate[1,2]) + (rB_Mat[3,5] * rLambda_Costate[1,3]) + (rB_Mat[4,5] * rLambda_Costate[1,4]) + (rB_Mat[5,5] * rLambda_Costate[1,5]) + (rB_Mat[6,5] * rLambda_Costate[1,6]) + (rR_Diag[5] * rU_Opt_Seq[1,5]) + (rS_Diag[5] * (rU_Opt_Seq[1,5] - a_u_prev[5])) - (rS_Diag[5] * (rU_Opt_Seq[2,5] - rU_Opt_Seq[1,5]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[1, 5] * rGrad_J[1, 5]);

(* Gradient for u_2 (h=2) *)
rGrad_J[2, 1] := (rB_Mat[1,1] * rLambda_Costate[2,1]) + (rB_Mat[2,1] * rLambda_Costate[2,2]) + (rB_Mat[3,1] * rLambda_Costate[2,3]) + (rB_Mat[4,1] * rLambda_Costate[2,4]) + (rB_Mat[5,1] * rLambda_Costate[2,5]) + (rB_Mat[6,1] * rLambda_Costate[2,6]) + (rR_Diag[1] * rU_Opt_Seq[2,1]) + (rS_Diag[1] * (rU_Opt_Seq[2,1] - rU_Opt_Seq[1,1])) - (rS_Diag[1] * (rU_Opt_Seq[3,1] - rU_Opt_Seq[2,1]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[2, 1] * rGrad_J[2, 1]);
rGrad_J[2, 2] := (rB_Mat[1,2] * rLambda_Costate[2,1]) + (rB_Mat[2,2] * rLambda_Costate[2,2]) + (rB_Mat[3,2] * rLambda_Costate[2,3]) + (rB_Mat[4,2] * rLambda_Costate[2,4]) + (rB_Mat[5,2] * rLambda_Costate[2,5]) + (rB_Mat[6,2] * rLambda_Costate[2,6]) + (rR_Diag[2] * rU_Opt_Seq[2,2]) + (rS_Diag[2] * (rU_Opt_Seq[2,2] - rU_Opt_Seq[1,2])) - (rS_Diag[2] * (rU_Opt_Seq[3,2] - rU_Opt_Seq[2,2]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[2, 2] * rGrad_J[2, 2]);
rGrad_J[2, 3] := (rB_Mat[1,3] * rLambda_Costate[2,1]) + (rB_Mat[2,3] * rLambda_Costate[2,2]) + (rB_Mat[3,3] * rLambda_Costate[2,3]) + (rB_Mat[4,3] * rLambda_Costate[2,4]) + (rB_Mat[5,3] * rLambda_Costate[2,5]) + (rB_Mat[6,3] * rLambda_Costate[2,6]) + (rR_Diag[3] * rU_Opt_Seq[2,3]) + (rS_Diag[3] * (rU_Opt_Seq[2,3] - rU_Opt_Seq[1,3])) - (rS_Diag[3] * (rU_Opt_Seq[3,3] - rU_Opt_Seq[2,3]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[2, 3] * rGrad_J[2, 3]);
rGrad_J[2, 4] := (rB_Mat[1,4] * rLambda_Costate[2,1]) + (rB_Mat[2,4] * rLambda_Costate[2,2]) + (rB_Mat[3,4] * rLambda_Costate[2,3]) + (rB_Mat[4,4] * rLambda_Costate[2,4]) + (rB_Mat[5,4] * rLambda_Costate[2,5]) + (rB_Mat[6,4] * rLambda_Costate[2,6]) + (rR_Diag[4] * rU_Opt_Seq[2,4]) + (rS_Diag[4] * (rU_Opt_Seq[2,4] - rU_Opt_Seq[1,4])) - (rS_Diag[4] * (rU_Opt_Seq[3,4] - rU_Opt_Seq[2,4]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[2, 4] * rGrad_J[2, 4]);
rGrad_J[2, 5] := (rB_Mat[1,5] * rLambda_Costate[2,1]) + (rB_Mat[2,5] * rLambda_Costate[2,2]) + (rB_Mat[3,5] * rLambda_Costate[2,3]) + (rB_Mat[4,5] * rLambda_Costate[2,4]) + (rB_Mat[5,5] * rLambda_Costate[2,5]) + (rB_Mat[6,5] * rLambda_Costate[2,6]) + (rR_Diag[5] * rU_Opt_Seq[2,5]) + (rS_Diag[5] * (rU_Opt_Seq[2,5] - rU_Opt_Seq[1,5])) - (rS_Diag[5] * (rU_Opt_Seq[3,5] - rU_Opt_Seq[2,5]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[2, 5] * rGrad_J[2, 5]);

(* Gradient for u_3 (h=3, held through h=4, 5) *)
rGrad_J[3, 1] := (rB_Mat[1,1] * (rLambda_Costate[3,1] + rLambda_Costate[4,1] + rLambda_Costate[5,1])) + (rB_Mat[2,1] * (rLambda_Costate[3,2] + rLambda_Costate[4,2] + rLambda_Costate[5,2])) + (rB_Mat[3,1] * (rLambda_Costate[3,3] + rLambda_Costate[4,3] + rLambda_Costate[5,3])) + (rB_Mat[4,1] * (rLambda_Costate[3,4] + rLambda_Costate[4,4] + rLambda_Costate[5,4])) + (rB_Mat[5,1] * (rLambda_Costate[3,5] + rLambda_Costate[4,5] + rLambda_Costate[5,5])) + (rB_Mat[6,1] * (rLambda_Costate[3,6] + rLambda_Costate[4,6] + rLambda_Costate[5,6])) + (rR_Diag[1] * rU_Opt_Seq[3,1]) + (rS_Diag[1] * (rU_Opt_Seq[3,1] - rU_Opt_Seq[2,1]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[3, 1] * rGrad_J[3, 1]);
rGrad_J[3, 2] := (rB_Mat[1,2] * (rLambda_Costate[3,1] + rLambda_Costate[4,1] + rLambda_Costate[5,1])) + (rB_Mat[2,2] * (rLambda_Costate[3,2] + rLambda_Costate[4,2] + rLambda_Costate[5,2])) + (rB_Mat[3,2] * (rLambda_Costate[3,3] + rLambda_Costate[4,3] + rLambda_Costate[5,3])) + (rB_Mat[4,2] * (rLambda_Costate[3,4] + rLambda_Costate[4,4] + rLambda_Costate[5,4])) + (rB_Mat[5,2] * (rLambda_Costate[3,5] + rLambda_Costate[4,5] + rLambda_Costate[5,5])) + (rB_Mat[6,2] * (rLambda_Costate[3,6] + rLambda_Costate[4,6] + rLambda_Costate[5,6])) + (rR_Diag[2] * rU_Opt_Seq[3,2]) + (rS_Diag[2] * (rU_Opt_Seq[3,2] - rU_Opt_Seq[2,2]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[3, 2] * rGrad_J[3, 2]);
rGrad_J[3, 3] := (rB_Mat[1,3] * (rLambda_Costate[3,1] + rLambda_Costate[4,1] + rLambda_Costate[5,1])) + (rB_Mat[2,3] * (rLambda_Costate[3,2] + rLambda_Costate[4,2] + rLambda_Costate[5,2])) + (rB_Mat[3,3] * (rLambda_Costate[3,3] + rLambda_Costate[4,3] + rLambda_Costate[5,3])) + (rB_Mat[4,3] * (rLambda_Costate[3,4] + rLambda_Costate[4,4] + rLambda_Costate[5,4])) + (rB_Mat[5,3] * (rLambda_Costate[3,5] + rLambda_Costate[4,5] + rLambda_Costate[5,5])) + (rB_Mat[6,3] * (rLambda_Costate[3,6] + rLambda_Costate[4,6] + rLambda_Costate[5,6])) + (rR_Diag[3] * rU_Opt_Seq[3,3]) + (rS_Diag[3] * (rU_Opt_Seq[3,3] - rU_Opt_Seq[2,3]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[3, 3] * rGrad_J[3, 3]);
rGrad_J[3, 4] := (rB_Mat[1,4] * (rLambda_Costate[3,1] + rLambda_Costate[4,1] + rLambda_Costate[5,1])) + (rB_Mat[2,4] * (rLambda_Costate[3,2] + rLambda_Costate[4,2] + rLambda_Costate[5,2])) + (rB_Mat[3,4] * (rLambda_Costate[3,3] + rLambda_Costate[4,3] + rLambda_Costate[5,3])) + (rB_Mat[4,4] * (rLambda_Costate[3,4] + rLambda_Costate[4,4] + rLambda_Costate[5,4])) + (rB_Mat[5,4] * (rLambda_Costate[3,5] + rLambda_Costate[4,5] + rLambda_Costate[5,5])) + (rB_Mat[6,4] * (rLambda_Costate[3,6] + rLambda_Costate[4,6] + rLambda_Costate[5,6])) + (rR_Diag[4] * rU_Opt_Seq[3,4]) + (rS_Diag[4] * (rU_Opt_Seq[3,4] - rU_Opt_Seq[2,4]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[3, 4] * rGrad_J[3, 4]);
rGrad_J[3, 5] := (rB_Mat[1,5] * (rLambda_Costate[3,1] + rLambda_Costate[4,1] + rLambda_Costate[5,1])) + (rB_Mat[2,5] * (rLambda_Costate[3,2] + rLambda_Costate[4,2] + rLambda_Costate[5,2])) + (rB_Mat[3,5] * (rLambda_Costate[3,3] + rLambda_Costate[4,3] + rLambda_Costate[5,3])) + (rB_Mat[4,5] * (rLambda_Costate[3,4] + rLambda_Costate[4,4] + rLambda_Costate[5,4])) + (rB_Mat[5,5] * (rLambda_Costate[3,5] + rLambda_Costate[4,5] + rLambda_Costate[5,5])) + (rB_Mat[6,5] * (rLambda_Costate[3,6] + rLambda_Costate[4,6] + rLambda_Costate[5,6])) + (rR_Diag[5] * rU_Opt_Seq[3,5]) + (rS_Diag[5] * (rU_Opt_Seq[3,5] - rU_Opt_Seq[2,5]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[3, 5] * rGrad_J[3, 5]);

(* Iteration 6 - Projected Gradient Step with Hard Box & Dynamic Slew Limits *)
rTemp_Val := rU_Opt_Seq[1, 1] - (rAlpha_PGD_StepSize * rGrad_J[1, 1]);
(* Slew limit against prior actuator output *)
IF rTemp_Val > (a_u_prev[1] + rDeltaU_Max[1]) THEN
    rTemp_Val := a_u_prev[1] + rDeltaU_Max[1];
ELSIF rTemp_Val < (a_u_prev[1] - rDeltaU_Max[1]) THEN
    rTemp_Val := a_u_prev[1] - rDeltaU_Max[1];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[1] THEN
    rTemp_Val := rU_BoxMax[1];
ELSIF rTemp_Val < rU_BoxMin[1] THEN
    rTemp_Val := rU_BoxMin[1];
END_IF;
rU_Opt_Seq[1, 1] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[1, 2] - (rAlpha_PGD_StepSize * rGrad_J[1, 2]);
(* Slew limit against prior actuator output *)
IF rTemp_Val > (a_u_prev[2] + rDeltaU_Max[2]) THEN
    rTemp_Val := a_u_prev[2] + rDeltaU_Max[2];
ELSIF rTemp_Val < (a_u_prev[2] - rDeltaU_Max[2]) THEN
    rTemp_Val := a_u_prev[2] - rDeltaU_Max[2];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[2] THEN
    rTemp_Val := rU_BoxMax[2];
ELSIF rTemp_Val < rU_BoxMin[2] THEN
    rTemp_Val := rU_BoxMin[2];
END_IF;
rU_Opt_Seq[1, 2] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[1, 3] - (rAlpha_PGD_StepSize * rGrad_J[1, 3]);
(* Slew limit against prior actuator output *)
IF rTemp_Val > (a_u_prev[3] + rDeltaU_Max[3]) THEN
    rTemp_Val := a_u_prev[3] + rDeltaU_Max[3];
ELSIF rTemp_Val < (a_u_prev[3] - rDeltaU_Max[3]) THEN
    rTemp_Val := a_u_prev[3] - rDeltaU_Max[3];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[3] THEN
    rTemp_Val := rU_BoxMax[3];
ELSIF rTemp_Val < rU_BoxMin[3] THEN
    rTemp_Val := rU_BoxMin[3];
END_IF;
rU_Opt_Seq[1, 3] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[1, 4] - (rAlpha_PGD_StepSize * rGrad_J[1, 4]);
(* Slew limit against prior actuator output *)
IF rTemp_Val > (a_u_prev[4] + rDeltaU_Max[4]) THEN
    rTemp_Val := a_u_prev[4] + rDeltaU_Max[4];
ELSIF rTemp_Val < (a_u_prev[4] - rDeltaU_Max[4]) THEN
    rTemp_Val := a_u_prev[4] - rDeltaU_Max[4];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[4] THEN
    rTemp_Val := rU_BoxMax[4];
ELSIF rTemp_Val < rU_BoxMin[4] THEN
    rTemp_Val := rU_BoxMin[4];
END_IF;
rU_Opt_Seq[1, 4] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[1, 5] - (rAlpha_PGD_StepSize * rGrad_J[1, 5]);
(* Slew limit against prior actuator output *)
IF rTemp_Val > (a_u_prev[5] + rDeltaU_Max[5]) THEN
    rTemp_Val := a_u_prev[5] + rDeltaU_Max[5];
ELSIF rTemp_Val < (a_u_prev[5] - rDeltaU_Max[5]) THEN
    rTemp_Val := a_u_prev[5] - rDeltaU_Max[5];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[5] THEN
    rTemp_Val := rU_BoxMax[5];
ELSIF rTemp_Val < rU_BoxMin[5] THEN
    rTemp_Val := rU_BoxMin[5];
END_IF;
rU_Opt_Seq[1, 5] := rTemp_Val;

rTemp_Val := rU_Opt_Seq[2, 1] - (rAlpha_PGD_StepSize * rGrad_J[2, 1]);
(* Slew limit against step 1 *)
IF rTemp_Val > (rU_Opt_Seq[1, 1] + rDeltaU_Max[1]) THEN
    rTemp_Val := rU_Opt_Seq[1, 1] + rDeltaU_Max[1];
ELSIF rTemp_Val < (rU_Opt_Seq[1, 1] - rDeltaU_Max[1]) THEN
    rTemp_Val := rU_Opt_Seq[1, 1] - rDeltaU_Max[1];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[1] THEN
    rTemp_Val := rU_BoxMax[1];
ELSIF rTemp_Val < rU_BoxMin[1] THEN
    rTemp_Val := rU_BoxMin[1];
END_IF;
rU_Opt_Seq[2, 1] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[2, 2] - (rAlpha_PGD_StepSize * rGrad_J[2, 2]);
(* Slew limit against step 1 *)
IF rTemp_Val > (rU_Opt_Seq[1, 2] + rDeltaU_Max[2]) THEN
    rTemp_Val := rU_Opt_Seq[1, 2] + rDeltaU_Max[2];
ELSIF rTemp_Val < (rU_Opt_Seq[1, 2] - rDeltaU_Max[2]) THEN
    rTemp_Val := rU_Opt_Seq[1, 2] - rDeltaU_Max[2];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[2] THEN
    rTemp_Val := rU_BoxMax[2];
ELSIF rTemp_Val < rU_BoxMin[2] THEN
    rTemp_Val := rU_BoxMin[2];
END_IF;
rU_Opt_Seq[2, 2] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[2, 3] - (rAlpha_PGD_StepSize * rGrad_J[2, 3]);
(* Slew limit against step 1 *)
IF rTemp_Val > (rU_Opt_Seq[1, 3] + rDeltaU_Max[3]) THEN
    rTemp_Val := rU_Opt_Seq[1, 3] + rDeltaU_Max[3];
ELSIF rTemp_Val < (rU_Opt_Seq[1, 3] - rDeltaU_Max[3]) THEN
    rTemp_Val := rU_Opt_Seq[1, 3] - rDeltaU_Max[3];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[3] THEN
    rTemp_Val := rU_BoxMax[3];
ELSIF rTemp_Val < rU_BoxMin[3] THEN
    rTemp_Val := rU_BoxMin[3];
END_IF;
rU_Opt_Seq[2, 3] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[2, 4] - (rAlpha_PGD_StepSize * rGrad_J[2, 4]);
(* Slew limit against step 1 *)
IF rTemp_Val > (rU_Opt_Seq[1, 4] + rDeltaU_Max[4]) THEN
    rTemp_Val := rU_Opt_Seq[1, 4] + rDeltaU_Max[4];
ELSIF rTemp_Val < (rU_Opt_Seq[1, 4] - rDeltaU_Max[4]) THEN
    rTemp_Val := rU_Opt_Seq[1, 4] - rDeltaU_Max[4];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[4] THEN
    rTemp_Val := rU_BoxMax[4];
ELSIF rTemp_Val < rU_BoxMin[4] THEN
    rTemp_Val := rU_BoxMin[4];
END_IF;
rU_Opt_Seq[2, 4] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[2, 5] - (rAlpha_PGD_StepSize * rGrad_J[2, 5]);
(* Slew limit against step 1 *)
IF rTemp_Val > (rU_Opt_Seq[1, 5] + rDeltaU_Max[5]) THEN
    rTemp_Val := rU_Opt_Seq[1, 5] + rDeltaU_Max[5];
ELSIF rTemp_Val < (rU_Opt_Seq[1, 5] - rDeltaU_Max[5]) THEN
    rTemp_Val := rU_Opt_Seq[1, 5] - rDeltaU_Max[5];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[5] THEN
    rTemp_Val := rU_BoxMax[5];
ELSIF rTemp_Val < rU_BoxMin[5] THEN
    rTemp_Val := rU_BoxMin[5];
END_IF;
rU_Opt_Seq[2, 5] := rTemp_Val;

rTemp_Val := rU_Opt_Seq[3, 1] - (rAlpha_PGD_StepSize * rGrad_J[3, 1]);
(* Slew limit against step 2 *)
IF rTemp_Val > (rU_Opt_Seq[2, 1] + rDeltaU_Max[1]) THEN
    rTemp_Val := rU_Opt_Seq[2, 1] + rDeltaU_Max[1];
ELSIF rTemp_Val < (rU_Opt_Seq[2, 1] - rDeltaU_Max[1]) THEN
    rTemp_Val := rU_Opt_Seq[2, 1] - rDeltaU_Max[1];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[1] THEN
    rTemp_Val := rU_BoxMax[1];
ELSIF rTemp_Val < rU_BoxMin[1] THEN
    rTemp_Val := rU_BoxMin[1];
END_IF;
rU_Opt_Seq[3, 1] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[3, 2] - (rAlpha_PGD_StepSize * rGrad_J[3, 2]);
(* Slew limit against step 2 *)
IF rTemp_Val > (rU_Opt_Seq[2, 2] + rDeltaU_Max[2]) THEN
    rTemp_Val := rU_Opt_Seq[2, 2] + rDeltaU_Max[2];
ELSIF rTemp_Val < (rU_Opt_Seq[2, 2] - rDeltaU_Max[2]) THEN
    rTemp_Val := rU_Opt_Seq[2, 2] - rDeltaU_Max[2];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[2] THEN
    rTemp_Val := rU_BoxMax[2];
ELSIF rTemp_Val < rU_BoxMin[2] THEN
    rTemp_Val := rU_BoxMin[2];
END_IF;
rU_Opt_Seq[3, 2] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[3, 3] - (rAlpha_PGD_StepSize * rGrad_J[3, 3]);
(* Slew limit against step 2 *)
IF rTemp_Val > (rU_Opt_Seq[2, 3] + rDeltaU_Max[3]) THEN
    rTemp_Val := rU_Opt_Seq[2, 3] + rDeltaU_Max[3];
ELSIF rTemp_Val < (rU_Opt_Seq[2, 3] - rDeltaU_Max[3]) THEN
    rTemp_Val := rU_Opt_Seq[2, 3] - rDeltaU_Max[3];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[3] THEN
    rTemp_Val := rU_BoxMax[3];
ELSIF rTemp_Val < rU_BoxMin[3] THEN
    rTemp_Val := rU_BoxMin[3];
END_IF;
rU_Opt_Seq[3, 3] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[3, 4] - (rAlpha_PGD_StepSize * rGrad_J[3, 4]);
(* Slew limit against step 2 *)
IF rTemp_Val > (rU_Opt_Seq[2, 4] + rDeltaU_Max[4]) THEN
    rTemp_Val := rU_Opt_Seq[2, 4] + rDeltaU_Max[4];
ELSIF rTemp_Val < (rU_Opt_Seq[2, 4] - rDeltaU_Max[4]) THEN
    rTemp_Val := rU_Opt_Seq[2, 4] - rDeltaU_Max[4];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[4] THEN
    rTemp_Val := rU_BoxMax[4];
ELSIF rTemp_Val < rU_BoxMin[4] THEN
    rTemp_Val := rU_BoxMin[4];
END_IF;
rU_Opt_Seq[3, 4] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[3, 5] - (rAlpha_PGD_StepSize * rGrad_J[3, 5]);
(* Slew limit against step 2 *)
IF rTemp_Val > (rU_Opt_Seq[2, 5] + rDeltaU_Max[5]) THEN
    rTemp_Val := rU_Opt_Seq[2, 5] + rDeltaU_Max[5];
ELSIF rTemp_Val < (rU_Opt_Seq[2, 5] - rDeltaU_Max[5]) THEN
    rTemp_Val := rU_Opt_Seq[2, 5] - rDeltaU_Max[5];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[5] THEN
    rTemp_Val := rU_BoxMax[5];
ELSIF rTemp_Val < rU_BoxMin[5] THEN
    rTemp_Val := rU_BoxMin[5];
END_IF;
rU_Opt_Seq[3, 5] := rTemp_Val;

(* ================================================================================================== *)
(* MPC PROJECTED GRADIENT DESCENT -- UNROLLED ITERATION 7 OF 10                                 *)
(* ================================================================================================== *)
iPGD_IterCount := 7;

(* Iteration 7 - Forward State Prediction Step 1 (h=1): x_1 = A * x_hat + B * u_1 *)
rX_Pred_Horizon[1, 1] := (rA_Mat[1,1] * a_x_hat[1]) + (rA_Mat[1,2] * a_x_hat[2]) + (rA_Mat[1,3] * a_x_hat[3]) + (rA_Mat[1,4] * a_x_hat[4]) + (rA_Mat[1,5] * a_x_hat[5]) + (rA_Mat[1,6] * a_x_hat[6]) + (rB_Mat[1,1] * rU_Opt_Seq[1,1]) + (rB_Mat[1,2] * rU_Opt_Seq[1,2]) + (rB_Mat[1,3] * rU_Opt_Seq[1,3]) + (rB_Mat[1,4] * rU_Opt_Seq[1,4]) + (rB_Mat[1,5] * rU_Opt_Seq[1,5]);
rX_Pred_Horizon[1, 2] := (rA_Mat[2,1] * a_x_hat[1]) + (rA_Mat[2,2] * a_x_hat[2]) + (rA_Mat[2,3] * a_x_hat[3]) + (rA_Mat[2,4] * a_x_hat[4]) + (rA_Mat[2,5] * a_x_hat[5]) + (rA_Mat[2,6] * a_x_hat[6]) + (rB_Mat[2,1] * rU_Opt_Seq[1,1]) + (rB_Mat[2,2] * rU_Opt_Seq[1,2]) + (rB_Mat[2,3] * rU_Opt_Seq[1,3]) + (rB_Mat[2,4] * rU_Opt_Seq[1,4]) + (rB_Mat[2,5] * rU_Opt_Seq[1,5]);
rX_Pred_Horizon[1, 3] := (rA_Mat[3,1] * a_x_hat[1]) + (rA_Mat[3,2] * a_x_hat[2]) + (rA_Mat[3,3] * a_x_hat[3]) + (rA_Mat[3,4] * a_x_hat[4]) + (rA_Mat[3,5] * a_x_hat[5]) + (rA_Mat[3,6] * a_x_hat[6]) + (rB_Mat[3,1] * rU_Opt_Seq[1,1]) + (rB_Mat[3,2] * rU_Opt_Seq[1,2]) + (rB_Mat[3,3] * rU_Opt_Seq[1,3]) + (rB_Mat[3,4] * rU_Opt_Seq[1,4]) + (rB_Mat[3,5] * rU_Opt_Seq[1,5]);
rX_Pred_Horizon[1, 4] := (rA_Mat[4,1] * a_x_hat[1]) + (rA_Mat[4,2] * a_x_hat[2]) + (rA_Mat[4,3] * a_x_hat[3]) + (rA_Mat[4,4] * a_x_hat[4]) + (rA_Mat[4,5] * a_x_hat[5]) + (rA_Mat[4,6] * a_x_hat[6]) + (rB_Mat[4,1] * rU_Opt_Seq[1,1]) + (rB_Mat[4,2] * rU_Opt_Seq[1,2]) + (rB_Mat[4,3] * rU_Opt_Seq[1,3]) + (rB_Mat[4,4] * rU_Opt_Seq[1,4]) + (rB_Mat[4,5] * rU_Opt_Seq[1,5]);
rX_Pred_Horizon[1, 5] := (rA_Mat[5,1] * a_x_hat[1]) + (rA_Mat[5,2] * a_x_hat[2]) + (rA_Mat[5,3] * a_x_hat[3]) + (rA_Mat[5,4] * a_x_hat[4]) + (rA_Mat[5,5] * a_x_hat[5]) + (rA_Mat[5,6] * a_x_hat[6]) + (rB_Mat[5,1] * rU_Opt_Seq[1,1]) + (rB_Mat[5,2] * rU_Opt_Seq[1,2]) + (rB_Mat[5,3] * rU_Opt_Seq[1,3]) + (rB_Mat[5,4] * rU_Opt_Seq[1,4]) + (rB_Mat[5,5] * rU_Opt_Seq[1,5]);
rX_Pred_Horizon[1, 6] := (rA_Mat[6,1] * a_x_hat[1]) + (rA_Mat[6,2] * a_x_hat[2]) + (rA_Mat[6,3] * a_x_hat[3]) + (rA_Mat[6,4] * a_x_hat[4]) + (rA_Mat[6,5] * a_x_hat[5]) + (rA_Mat[6,6] * a_x_hat[6]) + (rB_Mat[6,1] * rU_Opt_Seq[1,1]) + (rB_Mat[6,2] * rU_Opt_Seq[1,2]) + (rB_Mat[6,3] * rU_Opt_Seq[1,3]) + (rB_Mat[6,4] * rU_Opt_Seq[1,4]) + (rB_Mat[6,5] * rU_Opt_Seq[1,5]);

(* Iteration 7 - Forward State Prediction Step 2 (h=2): x_2 = A * x_1 + B * u_2 *)
rX_Pred_Horizon[2, 1] := (rA_Mat[1,1] * rX_Pred_Horizon[1,1]) + (rA_Mat[1,2] * rX_Pred_Horizon[1,2]) + (rA_Mat[1,3] * rX_Pred_Horizon[1,3]) + (rA_Mat[1,4] * rX_Pred_Horizon[1,4]) + (rA_Mat[1,5] * rX_Pred_Horizon[1,5]) + (rA_Mat[1,6] * rX_Pred_Horizon[1,6]) + (rB_Mat[1,1] * rU_Opt_Seq[2,1]) + (rB_Mat[1,2] * rU_Opt_Seq[2,2]) + (rB_Mat[1,3] * rU_Opt_Seq[2,3]) + (rB_Mat[1,4] * rU_Opt_Seq[2,4]) + (rB_Mat[1,5] * rU_Opt_Seq[2,5]);
rX_Pred_Horizon[2, 2] := (rA_Mat[2,1] * rX_Pred_Horizon[1,1]) + (rA_Mat[2,2] * rX_Pred_Horizon[1,2]) + (rA_Mat[2,3] * rX_Pred_Horizon[1,3]) + (rA_Mat[2,4] * rX_Pred_Horizon[1,4]) + (rA_Mat[2,5] * rX_Pred_Horizon[1,5]) + (rA_Mat[2,6] * rX_Pred_Horizon[1,6]) + (rB_Mat[2,1] * rU_Opt_Seq[2,1]) + (rB_Mat[2,2] * rU_Opt_Seq[2,2]) + (rB_Mat[2,3] * rU_Opt_Seq[2,3]) + (rB_Mat[2,4] * rU_Opt_Seq[2,4]) + (rB_Mat[2,5] * rU_Opt_Seq[2,5]);
rX_Pred_Horizon[2, 3] := (rA_Mat[3,1] * rX_Pred_Horizon[1,1]) + (rA_Mat[3,2] * rX_Pred_Horizon[1,2]) + (rA_Mat[3,3] * rX_Pred_Horizon[1,3]) + (rA_Mat[3,4] * rX_Pred_Horizon[1,4]) + (rA_Mat[3,5] * rX_Pred_Horizon[1,5]) + (rA_Mat[3,6] * rX_Pred_Horizon[1,6]) + (rB_Mat[3,1] * rU_Opt_Seq[2,1]) + (rB_Mat[3,2] * rU_Opt_Seq[2,2]) + (rB_Mat[3,3] * rU_Opt_Seq[2,3]) + (rB_Mat[3,4] * rU_Opt_Seq[2,4]) + (rB_Mat[3,5] * rU_Opt_Seq[2,5]);
rX_Pred_Horizon[2, 4] := (rA_Mat[4,1] * rX_Pred_Horizon[1,1]) + (rA_Mat[4,2] * rX_Pred_Horizon[1,2]) + (rA_Mat[4,3] * rX_Pred_Horizon[1,3]) + (rA_Mat[4,4] * rX_Pred_Horizon[1,4]) + (rA_Mat[4,5] * rX_Pred_Horizon[1,5]) + (rA_Mat[4,6] * rX_Pred_Horizon[1,6]) + (rB_Mat[4,1] * rU_Opt_Seq[2,1]) + (rB_Mat[4,2] * rU_Opt_Seq[2,2]) + (rB_Mat[4,3] * rU_Opt_Seq[2,3]) + (rB_Mat[4,4] * rU_Opt_Seq[2,4]) + (rB_Mat[4,5] * rU_Opt_Seq[2,5]);
rX_Pred_Horizon[2, 5] := (rA_Mat[5,1] * rX_Pred_Horizon[1,1]) + (rA_Mat[5,2] * rX_Pred_Horizon[1,2]) + (rA_Mat[5,3] * rX_Pred_Horizon[1,3]) + (rA_Mat[5,4] * rX_Pred_Horizon[1,4]) + (rA_Mat[5,5] * rX_Pred_Horizon[1,5]) + (rA_Mat[5,6] * rX_Pred_Horizon[1,6]) + (rB_Mat[5,1] * rU_Opt_Seq[2,1]) + (rB_Mat[5,2] * rU_Opt_Seq[2,2]) + (rB_Mat[5,3] * rU_Opt_Seq[2,3]) + (rB_Mat[5,4] * rU_Opt_Seq[2,4]) + (rB_Mat[5,5] * rU_Opt_Seq[2,5]);
rX_Pred_Horizon[2, 6] := (rA_Mat[6,1] * rX_Pred_Horizon[1,1]) + (rA_Mat[6,2] * rX_Pred_Horizon[1,2]) + (rA_Mat[6,3] * rX_Pred_Horizon[1,3]) + (rA_Mat[6,4] * rX_Pred_Horizon[1,4]) + (rA_Mat[6,5] * rX_Pred_Horizon[1,5]) + (rA_Mat[6,6] * rX_Pred_Horizon[1,6]) + (rB_Mat[6,1] * rU_Opt_Seq[2,1]) + (rB_Mat[6,2] * rU_Opt_Seq[2,2]) + (rB_Mat[6,3] * rU_Opt_Seq[2,3]) + (rB_Mat[6,4] * rU_Opt_Seq[2,4]) + (rB_Mat[6,5] * rU_Opt_Seq[2,5]);

(* Iteration 7 - Forward State Prediction Step 3 (h=3): x_3 = A * x_2 + B * u_3 *)
rX_Pred_Horizon[3, 1] := (rA_Mat[1,1] * rX_Pred_Horizon[2,1]) + (rA_Mat[1,2] * rX_Pred_Horizon[2,2]) + (rA_Mat[1,3] * rX_Pred_Horizon[2,3]) + (rA_Mat[1,4] * rX_Pred_Horizon[2,4]) + (rA_Mat[1,5] * rX_Pred_Horizon[2,5]) + (rA_Mat[1,6] * rX_Pred_Horizon[2,6]) + (rB_Mat[1,1] * rU_Opt_Seq[3,1]) + (rB_Mat[1,2] * rU_Opt_Seq[3,2]) + (rB_Mat[1,3] * rU_Opt_Seq[3,3]) + (rB_Mat[1,4] * rU_Opt_Seq[3,4]) + (rB_Mat[1,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[3, 2] := (rA_Mat[2,1] * rX_Pred_Horizon[2,1]) + (rA_Mat[2,2] * rX_Pred_Horizon[2,2]) + (rA_Mat[2,3] * rX_Pred_Horizon[2,3]) + (rA_Mat[2,4] * rX_Pred_Horizon[2,4]) + (rA_Mat[2,5] * rX_Pred_Horizon[2,5]) + (rA_Mat[2,6] * rX_Pred_Horizon[2,6]) + (rB_Mat[2,1] * rU_Opt_Seq[3,1]) + (rB_Mat[2,2] * rU_Opt_Seq[3,2]) + (rB_Mat[2,3] * rU_Opt_Seq[3,3]) + (rB_Mat[2,4] * rU_Opt_Seq[3,4]) + (rB_Mat[2,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[3, 3] := (rA_Mat[3,1] * rX_Pred_Horizon[2,1]) + (rA_Mat[3,2] * rX_Pred_Horizon[2,2]) + (rA_Mat[3,3] * rX_Pred_Horizon[2,3]) + (rA_Mat[3,4] * rX_Pred_Horizon[2,4]) + (rA_Mat[3,5] * rX_Pred_Horizon[2,5]) + (rA_Mat[3,6] * rX_Pred_Horizon[2,6]) + (rB_Mat[3,1] * rU_Opt_Seq[3,1]) + (rB_Mat[3,2] * rU_Opt_Seq[3,2]) + (rB_Mat[3,3] * rU_Opt_Seq[3,3]) + (rB_Mat[3,4] * rU_Opt_Seq[3,4]) + (rB_Mat[3,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[3, 4] := (rA_Mat[4,1] * rX_Pred_Horizon[2,1]) + (rA_Mat[4,2] * rX_Pred_Horizon[2,2]) + (rA_Mat[4,3] * rX_Pred_Horizon[2,3]) + (rA_Mat[4,4] * rX_Pred_Horizon[2,4]) + (rA_Mat[4,5] * rX_Pred_Horizon[2,5]) + (rA_Mat[4,6] * rX_Pred_Horizon[2,6]) + (rB_Mat[4,1] * rU_Opt_Seq[3,1]) + (rB_Mat[4,2] * rU_Opt_Seq[3,2]) + (rB_Mat[4,3] * rU_Opt_Seq[3,3]) + (rB_Mat[4,4] * rU_Opt_Seq[3,4]) + (rB_Mat[4,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[3, 5] := (rA_Mat[5,1] * rX_Pred_Horizon[2,1]) + (rA_Mat[5,2] * rX_Pred_Horizon[2,2]) + (rA_Mat[5,3] * rX_Pred_Horizon[2,3]) + (rA_Mat[5,4] * rX_Pred_Horizon[2,4]) + (rA_Mat[5,5] * rX_Pred_Horizon[2,5]) + (rA_Mat[5,6] * rX_Pred_Horizon[2,6]) + (rB_Mat[5,1] * rU_Opt_Seq[3,1]) + (rB_Mat[5,2] * rU_Opt_Seq[3,2]) + (rB_Mat[5,3] * rU_Opt_Seq[3,3]) + (rB_Mat[5,4] * rU_Opt_Seq[3,4]) + (rB_Mat[5,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[3, 6] := (rA_Mat[6,1] * rX_Pred_Horizon[2,1]) + (rA_Mat[6,2] * rX_Pred_Horizon[2,2]) + (rA_Mat[6,3] * rX_Pred_Horizon[2,3]) + (rA_Mat[6,4] * rX_Pred_Horizon[2,4]) + (rA_Mat[6,5] * rX_Pred_Horizon[2,5]) + (rA_Mat[6,6] * rX_Pred_Horizon[2,6]) + (rB_Mat[6,1] * rU_Opt_Seq[3,1]) + (rB_Mat[6,2] * rU_Opt_Seq[3,2]) + (rB_Mat[6,3] * rU_Opt_Seq[3,3]) + (rB_Mat[6,4] * rU_Opt_Seq[3,4]) + (rB_Mat[6,5] * rU_Opt_Seq[3,5]);

(* Iteration 7 - Forward State Prediction Step 4 (h=4): x_4 = A * x_3 + B * u_3 (held beyond Hu) *)
rX_Pred_Horizon[4, 1] := (rA_Mat[1,1] * rX_Pred_Horizon[3,1]) + (rA_Mat[1,2] * rX_Pred_Horizon[3,2]) + (rA_Mat[1,3] * rX_Pred_Horizon[3,3]) + (rA_Mat[1,4] * rX_Pred_Horizon[3,4]) + (rA_Mat[1,5] * rX_Pred_Horizon[3,5]) + (rA_Mat[1,6] * rX_Pred_Horizon[3,6]) + (rB_Mat[1,1] * rU_Opt_Seq[3,1]) + (rB_Mat[1,2] * rU_Opt_Seq[3,2]) + (rB_Mat[1,3] * rU_Opt_Seq[3,3]) + (rB_Mat[1,4] * rU_Opt_Seq[3,4]) + (rB_Mat[1,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[4, 2] := (rA_Mat[2,1] * rX_Pred_Horizon[3,1]) + (rA_Mat[2,2] * rX_Pred_Horizon[3,2]) + (rA_Mat[2,3] * rX_Pred_Horizon[3,3]) + (rA_Mat[2,4] * rX_Pred_Horizon[3,4]) + (rA_Mat[2,5] * rX_Pred_Horizon[3,5]) + (rA_Mat[2,6] * rX_Pred_Horizon[3,6]) + (rB_Mat[2,1] * rU_Opt_Seq[3,1]) + (rB_Mat[2,2] * rU_Opt_Seq[3,2]) + (rB_Mat[2,3] * rU_Opt_Seq[3,3]) + (rB_Mat[2,4] * rU_Opt_Seq[3,4]) + (rB_Mat[2,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[4, 3] := (rA_Mat[3,1] * rX_Pred_Horizon[3,1]) + (rA_Mat[3,2] * rX_Pred_Horizon[3,2]) + (rA_Mat[3,3] * rX_Pred_Horizon[3,3]) + (rA_Mat[3,4] * rX_Pred_Horizon[3,4]) + (rA_Mat[3,5] * rX_Pred_Horizon[3,5]) + (rA_Mat[3,6] * rX_Pred_Horizon[3,6]) + (rB_Mat[3,1] * rU_Opt_Seq[3,1]) + (rB_Mat[3,2] * rU_Opt_Seq[3,2]) + (rB_Mat[3,3] * rU_Opt_Seq[3,3]) + (rB_Mat[3,4] * rU_Opt_Seq[3,4]) + (rB_Mat[3,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[4, 4] := (rA_Mat[4,1] * rX_Pred_Horizon[3,1]) + (rA_Mat[4,2] * rX_Pred_Horizon[3,2]) + (rA_Mat[4,3] * rX_Pred_Horizon[3,3]) + (rA_Mat[4,4] * rX_Pred_Horizon[3,4]) + (rA_Mat[4,5] * rX_Pred_Horizon[3,5]) + (rA_Mat[4,6] * rX_Pred_Horizon[3,6]) + (rB_Mat[4,1] * rU_Opt_Seq[3,1]) + (rB_Mat[4,2] * rU_Opt_Seq[3,2]) + (rB_Mat[4,3] * rU_Opt_Seq[3,3]) + (rB_Mat[4,4] * rU_Opt_Seq[3,4]) + (rB_Mat[4,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[4, 5] := (rA_Mat[5,1] * rX_Pred_Horizon[3,1]) + (rA_Mat[5,2] * rX_Pred_Horizon[3,2]) + (rA_Mat[5,3] * rX_Pred_Horizon[3,3]) + (rA_Mat[5,4] * rX_Pred_Horizon[3,4]) + (rA_Mat[5,5] * rX_Pred_Horizon[3,5]) + (rA_Mat[5,6] * rX_Pred_Horizon[3,6]) + (rB_Mat[5,1] * rU_Opt_Seq[3,1]) + (rB_Mat[5,2] * rU_Opt_Seq[3,2]) + (rB_Mat[5,3] * rU_Opt_Seq[3,3]) + (rB_Mat[5,4] * rU_Opt_Seq[3,4]) + (rB_Mat[5,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[4, 6] := (rA_Mat[6,1] * rX_Pred_Horizon[3,1]) + (rA_Mat[6,2] * rX_Pred_Horizon[3,2]) + (rA_Mat[6,3] * rX_Pred_Horizon[3,3]) + (rA_Mat[6,4] * rX_Pred_Horizon[3,4]) + (rA_Mat[6,5] * rX_Pred_Horizon[3,5]) + (rA_Mat[6,6] * rX_Pred_Horizon[3,6]) + (rB_Mat[6,1] * rU_Opt_Seq[3,1]) + (rB_Mat[6,2] * rU_Opt_Seq[3,2]) + (rB_Mat[6,3] * rU_Opt_Seq[3,3]) + (rB_Mat[6,4] * rU_Opt_Seq[3,4]) + (rB_Mat[6,5] * rU_Opt_Seq[3,5]);

(* Iteration 7 - Forward State Prediction Step 5 (h=5): x_5 = A * x_4 + B * u_3 (held beyond Hu) *)
rX_Pred_Horizon[5, 1] := (rA_Mat[1,1] * rX_Pred_Horizon[4,1]) + (rA_Mat[1,2] * rX_Pred_Horizon[4,2]) + (rA_Mat[1,3] * rX_Pred_Horizon[4,3]) + (rA_Mat[1,4] * rX_Pred_Horizon[4,4]) + (rA_Mat[1,5] * rX_Pred_Horizon[4,5]) + (rA_Mat[1,6] * rX_Pred_Horizon[4,6]) + (rB_Mat[1,1] * rU_Opt_Seq[3,1]) + (rB_Mat[1,2] * rU_Opt_Seq[3,2]) + (rB_Mat[1,3] * rU_Opt_Seq[3,3]) + (rB_Mat[1,4] * rU_Opt_Seq[3,4]) + (rB_Mat[1,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[5, 2] := (rA_Mat[2,1] * rX_Pred_Horizon[4,1]) + (rA_Mat[2,2] * rX_Pred_Horizon[4,2]) + (rA_Mat[2,3] * rX_Pred_Horizon[4,3]) + (rA_Mat[2,4] * rX_Pred_Horizon[4,4]) + (rA_Mat[2,5] * rX_Pred_Horizon[4,5]) + (rA_Mat[2,6] * rX_Pred_Horizon[4,6]) + (rB_Mat[2,1] * rU_Opt_Seq[3,1]) + (rB_Mat[2,2] * rU_Opt_Seq[3,2]) + (rB_Mat[2,3] * rU_Opt_Seq[3,3]) + (rB_Mat[2,4] * rU_Opt_Seq[3,4]) + (rB_Mat[2,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[5, 3] := (rA_Mat[3,1] * rX_Pred_Horizon[4,1]) + (rA_Mat[3,2] * rX_Pred_Horizon[4,2]) + (rA_Mat[3,3] * rX_Pred_Horizon[4,3]) + (rA_Mat[3,4] * rX_Pred_Horizon[4,4]) + (rA_Mat[3,5] * rX_Pred_Horizon[4,5]) + (rA_Mat[3,6] * rX_Pred_Horizon[4,6]) + (rB_Mat[3,1] * rU_Opt_Seq[3,1]) + (rB_Mat[3,2] * rU_Opt_Seq[3,2]) + (rB_Mat[3,3] * rU_Opt_Seq[3,3]) + (rB_Mat[3,4] * rU_Opt_Seq[3,4]) + (rB_Mat[3,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[5, 4] := (rA_Mat[4,1] * rX_Pred_Horizon[4,1]) + (rA_Mat[4,2] * rX_Pred_Horizon[4,2]) + (rA_Mat[4,3] * rX_Pred_Horizon[4,3]) + (rA_Mat[4,4] * rX_Pred_Horizon[4,4]) + (rA_Mat[4,5] * rX_Pred_Horizon[4,5]) + (rA_Mat[4,6] * rX_Pred_Horizon[4,6]) + (rB_Mat[4,1] * rU_Opt_Seq[3,1]) + (rB_Mat[4,2] * rU_Opt_Seq[3,2]) + (rB_Mat[4,3] * rU_Opt_Seq[3,3]) + (rB_Mat[4,4] * rU_Opt_Seq[3,4]) + (rB_Mat[4,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[5, 5] := (rA_Mat[5,1] * rX_Pred_Horizon[4,1]) + (rA_Mat[5,2] * rX_Pred_Horizon[4,2]) + (rA_Mat[5,3] * rX_Pred_Horizon[4,3]) + (rA_Mat[5,4] * rX_Pred_Horizon[4,4]) + (rA_Mat[5,5] * rX_Pred_Horizon[4,5]) + (rA_Mat[5,6] * rX_Pred_Horizon[4,6]) + (rB_Mat[5,1] * rU_Opt_Seq[3,1]) + (rB_Mat[5,2] * rU_Opt_Seq[3,2]) + (rB_Mat[5,3] * rU_Opt_Seq[3,3]) + (rB_Mat[5,4] * rU_Opt_Seq[3,4]) + (rB_Mat[5,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[5, 6] := (rA_Mat[6,1] * rX_Pred_Horizon[4,1]) + (rA_Mat[6,2] * rX_Pred_Horizon[4,2]) + (rA_Mat[6,3] * rX_Pred_Horizon[4,3]) + (rA_Mat[6,4] * rX_Pred_Horizon[4,4]) + (rA_Mat[6,5] * rX_Pred_Horizon[4,5]) + (rA_Mat[6,6] * rX_Pred_Horizon[4,6]) + (rB_Mat[6,1] * rU_Opt_Seq[3,1]) + (rB_Mat[6,2] * rU_Opt_Seq[3,2]) + (rB_Mat[6,3] * rU_Opt_Seq[3,3]) + (rB_Mat[6,4] * rU_Opt_Seq[3,4]) + (rB_Mat[6,5] * rU_Opt_Seq[3,5]);

(* Iteration 7 - Evaluate Objective Function Cost J *)
rMPC_Cost_J := 0.0;
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[1] * (rX_Pred_Horizon[1,1] - rX_Target[1,1]) * (rX_Pred_Horizon[1,1] - rX_Target[1,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[2] * (rX_Pred_Horizon[1,2] - rX_Target[1,2]) * (rX_Pred_Horizon[1,2] - rX_Target[1,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[3] * (rX_Pred_Horizon[1,3] - rX_Target[1,3]) * (rX_Pred_Horizon[1,3] - rX_Target[1,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[4] * (rX_Pred_Horizon[1,4] - rX_Target[1,4]) * (rX_Pred_Horizon[1,4] - rX_Target[1,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[5] * (rX_Pred_Horizon[1,5] - rX_Target[1,5]) * (rX_Pred_Horizon[1,5] - rX_Target[1,5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[6] * (rX_Pred_Horizon[1,6] - rX_Target[1,6]) * (rX_Pred_Horizon[1,6] - rX_Target[1,6]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[1] * (rX_Pred_Horizon[2,1] - rX_Target[2,1]) * (rX_Pred_Horizon[2,1] - rX_Target[2,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[2] * (rX_Pred_Horizon[2,2] - rX_Target[2,2]) * (rX_Pred_Horizon[2,2] - rX_Target[2,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[3] * (rX_Pred_Horizon[2,3] - rX_Target[2,3]) * (rX_Pred_Horizon[2,3] - rX_Target[2,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[4] * (rX_Pred_Horizon[2,4] - rX_Target[2,4]) * (rX_Pred_Horizon[2,4] - rX_Target[2,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[5] * (rX_Pred_Horizon[2,5] - rX_Target[2,5]) * (rX_Pred_Horizon[2,5] - rX_Target[2,5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[6] * (rX_Pred_Horizon[2,6] - rX_Target[2,6]) * (rX_Pred_Horizon[2,6] - rX_Target[2,6]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[1] * (rX_Pred_Horizon[3,1] - rX_Target[3,1]) * (rX_Pred_Horizon[3,1] - rX_Target[3,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[2] * (rX_Pred_Horizon[3,2] - rX_Target[3,2]) * (rX_Pred_Horizon[3,2] - rX_Target[3,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[3] * (rX_Pred_Horizon[3,3] - rX_Target[3,3]) * (rX_Pred_Horizon[3,3] - rX_Target[3,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[4] * (rX_Pred_Horizon[3,4] - rX_Target[3,4]) * (rX_Pred_Horizon[3,4] - rX_Target[3,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[5] * (rX_Pred_Horizon[3,5] - rX_Target[3,5]) * (rX_Pred_Horizon[3,5] - rX_Target[3,5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[6] * (rX_Pred_Horizon[3,6] - rX_Target[3,6]) * (rX_Pred_Horizon[3,6] - rX_Target[3,6]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[1] * (rX_Pred_Horizon[4,1] - rX_Target[4,1]) * (rX_Pred_Horizon[4,1] - rX_Target[4,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[2] * (rX_Pred_Horizon[4,2] - rX_Target[4,2]) * (rX_Pred_Horizon[4,2] - rX_Target[4,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[3] * (rX_Pred_Horizon[4,3] - rX_Target[4,3]) * (rX_Pred_Horizon[4,3] - rX_Target[4,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[4] * (rX_Pred_Horizon[4,4] - rX_Target[4,4]) * (rX_Pred_Horizon[4,4] - rX_Target[4,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[5] * (rX_Pred_Horizon[4,5] - rX_Target[4,5]) * (rX_Pred_Horizon[4,5] - rX_Target[4,5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[6] * (rX_Pred_Horizon[4,6] - rX_Target[4,6]) * (rX_Pred_Horizon[4,6] - rX_Target[4,6]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[1] * (rX_Pred_Horizon[5,1] - rX_Target[5,1]) * (rX_Pred_Horizon[5,1] - rX_Target[5,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[2] * (rX_Pred_Horizon[5,2] - rX_Target[5,2]) * (rX_Pred_Horizon[5,2] - rX_Target[5,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[3] * (rX_Pred_Horizon[5,3] - rX_Target[5,3]) * (rX_Pred_Horizon[5,3] - rX_Target[5,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[4] * (rX_Pred_Horizon[5,4] - rX_Target[5,4]) * (rX_Pred_Horizon[5,4] - rX_Target[5,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[5] * (rX_Pred_Horizon[5,5] - rX_Target[5,5]) * (rX_Pred_Horizon[5,5] - rX_Target[5,5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[6] * (rX_Pred_Horizon[5,6] - rX_Target[5,6]) * (rX_Pred_Horizon[5,6] - rX_Target[5,6]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rP_Diag[1] * (rX_Pred_Horizon[5,1] - rX_Target[5,1]) * (rX_Pred_Horizon[5,1] - rX_Target[5,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rP_Diag[2] * (rX_Pred_Horizon[5,2] - rX_Target[5,2]) * (rX_Pred_Horizon[5,2] - rX_Target[5,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rP_Diag[3] * (rX_Pred_Horizon[5,3] - rX_Target[5,3]) * (rX_Pred_Horizon[5,3] - rX_Target[5,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rP_Diag[4] * (rX_Pred_Horizon[5,4] - rX_Target[5,4]) * (rX_Pred_Horizon[5,4] - rX_Target[5,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rP_Diag[5] * (rX_Pred_Horizon[5,5] - rX_Target[5,5]) * (rX_Pred_Horizon[5,5] - rX_Target[5,5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rP_Diag[6] * (rX_Pred_Horizon[5,6] - rX_Target[5,6]) * (rX_Pred_Horizon[5,6] - rX_Target[5,6]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[1] * rU_Opt_Seq[1,1] * rU_Opt_Seq[1,1]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[2] * rU_Opt_Seq[1,2] * rU_Opt_Seq[1,2]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[3] * rU_Opt_Seq[1,3] * rU_Opt_Seq[1,3]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[4] * rU_Opt_Seq[1,4] * rU_Opt_Seq[1,4]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[5] * rU_Opt_Seq[1,5] * rU_Opt_Seq[1,5]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[1] * rU_Opt_Seq[2,1] * rU_Opt_Seq[2,1]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[2] * rU_Opt_Seq[2,2] * rU_Opt_Seq[2,2]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[3] * rU_Opt_Seq[2,3] * rU_Opt_Seq[2,3]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[4] * rU_Opt_Seq[2,4] * rU_Opt_Seq[2,4]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[5] * rU_Opt_Seq[2,5] * rU_Opt_Seq[2,5]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[1] * rU_Opt_Seq[3,1] * rU_Opt_Seq[3,1]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[2] * rU_Opt_Seq[3,2] * rU_Opt_Seq[3,2]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[3] * rU_Opt_Seq[3,3] * rU_Opt_Seq[3,3]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[4] * rU_Opt_Seq[3,4] * rU_Opt_Seq[3,4]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[5] * rU_Opt_Seq[3,5] * rU_Opt_Seq[3,5]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[1] * (rU_Opt_Seq[1,1] - a_u_prev[1]) * (rU_Opt_Seq[1,1] - a_u_prev[1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[1] * (rU_Opt_Seq[2,1] - rU_Opt_Seq[1,1]) * (rU_Opt_Seq[2,1] - rU_Opt_Seq[1,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[1] * (rU_Opt_Seq[3,1] - rU_Opt_Seq[2,1]) * (rU_Opt_Seq[3,1] - rU_Opt_Seq[2,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[2] * (rU_Opt_Seq[1,2] - a_u_prev[2]) * (rU_Opt_Seq[1,2] - a_u_prev[2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[2] * (rU_Opt_Seq[2,2] - rU_Opt_Seq[1,2]) * (rU_Opt_Seq[2,2] - rU_Opt_Seq[1,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[2] * (rU_Opt_Seq[3,2] - rU_Opt_Seq[2,2]) * (rU_Opt_Seq[3,2] - rU_Opt_Seq[2,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[3] * (rU_Opt_Seq[1,3] - a_u_prev[3]) * (rU_Opt_Seq[1,3] - a_u_prev[3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[3] * (rU_Opt_Seq[2,3] - rU_Opt_Seq[1,3]) * (rU_Opt_Seq[2,3] - rU_Opt_Seq[1,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[3] * (rU_Opt_Seq[3,3] - rU_Opt_Seq[2,3]) * (rU_Opt_Seq[3,3] - rU_Opt_Seq[2,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[4] * (rU_Opt_Seq[1,4] - a_u_prev[4]) * (rU_Opt_Seq[1,4] - a_u_prev[4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[4] * (rU_Opt_Seq[2,4] - rU_Opt_Seq[1,4]) * (rU_Opt_Seq[2,4] - rU_Opt_Seq[1,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[4] * (rU_Opt_Seq[3,4] - rU_Opt_Seq[2,4]) * (rU_Opt_Seq[3,4] - rU_Opt_Seq[2,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[5] * (rU_Opt_Seq[1,5] - a_u_prev[5]) * (rU_Opt_Seq[1,5] - a_u_prev[5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[5] * (rU_Opt_Seq[2,5] - rU_Opt_Seq[1,5]) * (rU_Opt_Seq[2,5] - rU_Opt_Seq[1,5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[5] * (rU_Opt_Seq[3,5] - rU_Opt_Seq[2,5]) * (rU_Opt_Seq[3,5] - rU_Opt_Seq[2,5]));

(* Iteration 7 - Backward Adjoint Costate Propagation: lambda_h = A^T * lambda_{h+1} + Q * (x_h - x_ref) *)
(* Terminal Costate at h=5: lambda_5 = (P + Q) * (x_5 - x_target_5) *)
rLambda_Costate[5, 1] := (rP_Diag[1] + rQ_Diag[1]) * (rX_Pred_Horizon[5,1] - rX_Target[5,1]);
rLambda_Costate[5, 2] := (rP_Diag[2] + rQ_Diag[2]) * (rX_Pred_Horizon[5,2] - rX_Target[5,2]);
rLambda_Costate[5, 3] := (rP_Diag[3] + rQ_Diag[3]) * (rX_Pred_Horizon[5,3] - rX_Target[5,3]);
rLambda_Costate[5, 4] := (rP_Diag[4] + rQ_Diag[4]) * (rX_Pred_Horizon[5,4] - rX_Target[5,4]);
rLambda_Costate[5, 5] := (rP_Diag[5] + rQ_Diag[5]) * (rX_Pred_Horizon[5,5] - rX_Target[5,5]);
rLambda_Costate[5, 6] := (rP_Diag[6] + rQ_Diag[6]) * (rX_Pred_Horizon[5,6] - rX_Target[5,6]);

(* Adjoint Costate at h=4: lambda_4 = A^T * lambda_5 + Q * (x_4 - x_target_4) *)
rLambda_Costate[4, 1] := (rA_Mat[1,1] * rLambda_Costate[5,1]) + (rA_Mat[2,1] * rLambda_Costate[5,2]) + (rA_Mat[3,1] * rLambda_Costate[5,3]) + (rA_Mat[4,1] * rLambda_Costate[5,4]) + (rA_Mat[5,1] * rLambda_Costate[5,5]) + (rA_Mat[6,1] * rLambda_Costate[5,6]) + (rQ_Diag[1] * (rX_Pred_Horizon[4,1] - rX_Target[4,1]));
rLambda_Costate[4, 2] := (rA_Mat[1,2] * rLambda_Costate[5,1]) + (rA_Mat[2,2] * rLambda_Costate[5,2]) + (rA_Mat[3,2] * rLambda_Costate[5,3]) + (rA_Mat[4,2] * rLambda_Costate[5,4]) + (rA_Mat[5,2] * rLambda_Costate[5,5]) + (rA_Mat[6,2] * rLambda_Costate[5,6]) + (rQ_Diag[2] * (rX_Pred_Horizon[4,2] - rX_Target[4,2]));
rLambda_Costate[4, 3] := (rA_Mat[1,3] * rLambda_Costate[5,1]) + (rA_Mat[2,3] * rLambda_Costate[5,2]) + (rA_Mat[3,3] * rLambda_Costate[5,3]) + (rA_Mat[4,3] * rLambda_Costate[5,4]) + (rA_Mat[5,3] * rLambda_Costate[5,5]) + (rA_Mat[6,3] * rLambda_Costate[5,6]) + (rQ_Diag[3] * (rX_Pred_Horizon[4,3] - rX_Target[4,3]));
rLambda_Costate[4, 4] := (rA_Mat[1,4] * rLambda_Costate[5,1]) + (rA_Mat[2,4] * rLambda_Costate[5,2]) + (rA_Mat[3,4] * rLambda_Costate[5,3]) + (rA_Mat[4,4] * rLambda_Costate[5,4]) + (rA_Mat[5,4] * rLambda_Costate[5,5]) + (rA_Mat[6,4] * rLambda_Costate[5,6]) + (rQ_Diag[4] * (rX_Pred_Horizon[4,4] - rX_Target[4,4]));
rLambda_Costate[4, 5] := (rA_Mat[1,5] * rLambda_Costate[5,1]) + (rA_Mat[2,5] * rLambda_Costate[5,2]) + (rA_Mat[3,5] * rLambda_Costate[5,3]) + (rA_Mat[4,5] * rLambda_Costate[5,4]) + (rA_Mat[5,5] * rLambda_Costate[5,5]) + (rA_Mat[6,5] * rLambda_Costate[5,6]) + (rQ_Diag[5] * (rX_Pred_Horizon[4,5] - rX_Target[4,5]));
rLambda_Costate[4, 6] := (rA_Mat[1,6] * rLambda_Costate[5,1]) + (rA_Mat[2,6] * rLambda_Costate[5,2]) + (rA_Mat[3,6] * rLambda_Costate[5,3]) + (rA_Mat[4,6] * rLambda_Costate[5,4]) + (rA_Mat[5,6] * rLambda_Costate[5,5]) + (rA_Mat[6,6] * rLambda_Costate[5,6]) + (rQ_Diag[6] * (rX_Pred_Horizon[4,6] - rX_Target[4,6]));

(* Adjoint Costate at h=3: lambda_3 = A^T * lambda_4 + Q * (x_3 - x_target_3) *)
rLambda_Costate[3, 1] := (rA_Mat[1,1] * rLambda_Costate[4,1]) + (rA_Mat[2,1] * rLambda_Costate[4,2]) + (rA_Mat[3,1] * rLambda_Costate[4,3]) + (rA_Mat[4,1] * rLambda_Costate[4,4]) + (rA_Mat[5,1] * rLambda_Costate[4,5]) + (rA_Mat[6,1] * rLambda_Costate[4,6]) + (rQ_Diag[1] * (rX_Pred_Horizon[3,1] - rX_Target[3,1]));
rLambda_Costate[3, 2] := (rA_Mat[1,2] * rLambda_Costate[4,1]) + (rA_Mat[2,2] * rLambda_Costate[4,2]) + (rA_Mat[3,2] * rLambda_Costate[4,3]) + (rA_Mat[4,2] * rLambda_Costate[4,4]) + (rA_Mat[5,2] * rLambda_Costate[4,5]) + (rA_Mat[6,2] * rLambda_Costate[4,6]) + (rQ_Diag[2] * (rX_Pred_Horizon[3,2] - rX_Target[3,2]));
rLambda_Costate[3, 3] := (rA_Mat[1,3] * rLambda_Costate[4,1]) + (rA_Mat[2,3] * rLambda_Costate[4,2]) + (rA_Mat[3,3] * rLambda_Costate[4,3]) + (rA_Mat[4,3] * rLambda_Costate[4,4]) + (rA_Mat[5,3] * rLambda_Costate[4,5]) + (rA_Mat[6,3] * rLambda_Costate[4,6]) + (rQ_Diag[3] * (rX_Pred_Horizon[3,3] - rX_Target[3,3]));
rLambda_Costate[3, 4] := (rA_Mat[1,4] * rLambda_Costate[4,1]) + (rA_Mat[2,4] * rLambda_Costate[4,2]) + (rA_Mat[3,4] * rLambda_Costate[4,3]) + (rA_Mat[4,4] * rLambda_Costate[4,4]) + (rA_Mat[5,4] * rLambda_Costate[4,5]) + (rA_Mat[6,4] * rLambda_Costate[4,6]) + (rQ_Diag[4] * (rX_Pred_Horizon[3,4] - rX_Target[3,4]));
rLambda_Costate[3, 5] := (rA_Mat[1,5] * rLambda_Costate[4,1]) + (rA_Mat[2,5] * rLambda_Costate[4,2]) + (rA_Mat[3,5] * rLambda_Costate[4,3]) + (rA_Mat[4,5] * rLambda_Costate[4,4]) + (rA_Mat[5,5] * rLambda_Costate[4,5]) + (rA_Mat[6,5] * rLambda_Costate[4,6]) + (rQ_Diag[5] * (rX_Pred_Horizon[3,5] - rX_Target[3,5]));
rLambda_Costate[3, 6] := (rA_Mat[1,6] * rLambda_Costate[4,1]) + (rA_Mat[2,6] * rLambda_Costate[4,2]) + (rA_Mat[3,6] * rLambda_Costate[4,3]) + (rA_Mat[4,6] * rLambda_Costate[4,4]) + (rA_Mat[5,6] * rLambda_Costate[4,5]) + (rA_Mat[6,6] * rLambda_Costate[4,6]) + (rQ_Diag[6] * (rX_Pred_Horizon[3,6] - rX_Target[3,6]));

(* Adjoint Costate at h=2: lambda_2 = A^T * lambda_3 + Q * (x_2 - x_target_2) *)
rLambda_Costate[2, 1] := (rA_Mat[1,1] * rLambda_Costate[3,1]) + (rA_Mat[2,1] * rLambda_Costate[3,2]) + (rA_Mat[3,1] * rLambda_Costate[3,3]) + (rA_Mat[4,1] * rLambda_Costate[3,4]) + (rA_Mat[5,1] * rLambda_Costate[3,5]) + (rA_Mat[6,1] * rLambda_Costate[3,6]) + (rQ_Diag[1] * (rX_Pred_Horizon[2,1] - rX_Target[2,1]));
rLambda_Costate[2, 2] := (rA_Mat[1,2] * rLambda_Costate[3,1]) + (rA_Mat[2,2] * rLambda_Costate[3,2]) + (rA_Mat[3,2] * rLambda_Costate[3,3]) + (rA_Mat[4,2] * rLambda_Costate[3,4]) + (rA_Mat[5,2] * rLambda_Costate[3,5]) + (rA_Mat[6,2] * rLambda_Costate[3,6]) + (rQ_Diag[2] * (rX_Pred_Horizon[2,2] - rX_Target[2,2]));
rLambda_Costate[2, 3] := (rA_Mat[1,3] * rLambda_Costate[3,1]) + (rA_Mat[2,3] * rLambda_Costate[3,2]) + (rA_Mat[3,3] * rLambda_Costate[3,3]) + (rA_Mat[4,3] * rLambda_Costate[3,4]) + (rA_Mat[5,3] * rLambda_Costate[3,5]) + (rA_Mat[6,3] * rLambda_Costate[3,6]) + (rQ_Diag[3] * (rX_Pred_Horizon[2,3] - rX_Target[2,3]));
rLambda_Costate[2, 4] := (rA_Mat[1,4] * rLambda_Costate[3,1]) + (rA_Mat[2,4] * rLambda_Costate[3,2]) + (rA_Mat[3,4] * rLambda_Costate[3,3]) + (rA_Mat[4,4] * rLambda_Costate[3,4]) + (rA_Mat[5,4] * rLambda_Costate[3,5]) + (rA_Mat[6,4] * rLambda_Costate[3,6]) + (rQ_Diag[4] * (rX_Pred_Horizon[2,4] - rX_Target[2,4]));
rLambda_Costate[2, 5] := (rA_Mat[1,5] * rLambda_Costate[3,1]) + (rA_Mat[2,5] * rLambda_Costate[3,2]) + (rA_Mat[3,5] * rLambda_Costate[3,3]) + (rA_Mat[4,5] * rLambda_Costate[3,4]) + (rA_Mat[5,5] * rLambda_Costate[3,5]) + (rA_Mat[6,5] * rLambda_Costate[3,6]) + (rQ_Diag[5] * (rX_Pred_Horizon[2,5] - rX_Target[2,5]));
rLambda_Costate[2, 6] := (rA_Mat[1,6] * rLambda_Costate[3,1]) + (rA_Mat[2,6] * rLambda_Costate[3,2]) + (rA_Mat[3,6] * rLambda_Costate[3,3]) + (rA_Mat[4,6] * rLambda_Costate[3,4]) + (rA_Mat[5,6] * rLambda_Costate[3,5]) + (rA_Mat[6,6] * rLambda_Costate[3,6]) + (rQ_Diag[6] * (rX_Pred_Horizon[2,6] - rX_Target[2,6]));

(* Adjoint Costate at h=1: lambda_1 = A^T * lambda_2 + Q * (x_1 - x_target_1) *)
rLambda_Costate[1, 1] := (rA_Mat[1,1] * rLambda_Costate[2,1]) + (rA_Mat[2,1] * rLambda_Costate[2,2]) + (rA_Mat[3,1] * rLambda_Costate[2,3]) + (rA_Mat[4,1] * rLambda_Costate[2,4]) + (rA_Mat[5,1] * rLambda_Costate[2,5]) + (rA_Mat[6,1] * rLambda_Costate[2,6]) + (rQ_Diag[1] * (rX_Pred_Horizon[1,1] - rX_Target[1,1]));
rLambda_Costate[1, 2] := (rA_Mat[1,2] * rLambda_Costate[2,1]) + (rA_Mat[2,2] * rLambda_Costate[2,2]) + (rA_Mat[3,2] * rLambda_Costate[2,3]) + (rA_Mat[4,2] * rLambda_Costate[2,4]) + (rA_Mat[5,2] * rLambda_Costate[2,5]) + (rA_Mat[6,2] * rLambda_Costate[2,6]) + (rQ_Diag[2] * (rX_Pred_Horizon[1,2] - rX_Target[1,2]));
rLambda_Costate[1, 3] := (rA_Mat[1,3] * rLambda_Costate[2,1]) + (rA_Mat[2,3] * rLambda_Costate[2,2]) + (rA_Mat[3,3] * rLambda_Costate[2,3]) + (rA_Mat[4,3] * rLambda_Costate[2,4]) + (rA_Mat[5,3] * rLambda_Costate[2,5]) + (rA_Mat[6,3] * rLambda_Costate[2,6]) + (rQ_Diag[3] * (rX_Pred_Horizon[1,3] - rX_Target[1,3]));
rLambda_Costate[1, 4] := (rA_Mat[1,4] * rLambda_Costate[2,1]) + (rA_Mat[2,4] * rLambda_Costate[2,2]) + (rA_Mat[3,4] * rLambda_Costate[2,3]) + (rA_Mat[4,4] * rLambda_Costate[2,4]) + (rA_Mat[5,4] * rLambda_Costate[2,5]) + (rA_Mat[6,4] * rLambda_Costate[2,6]) + (rQ_Diag[4] * (rX_Pred_Horizon[1,4] - rX_Target[1,4]));
rLambda_Costate[1, 5] := (rA_Mat[1,5] * rLambda_Costate[2,1]) + (rA_Mat[2,5] * rLambda_Costate[2,2]) + (rA_Mat[3,5] * rLambda_Costate[2,3]) + (rA_Mat[4,5] * rLambda_Costate[2,4]) + (rA_Mat[5,5] * rLambda_Costate[2,5]) + (rA_Mat[6,5] * rLambda_Costate[2,6]) + (rQ_Diag[5] * (rX_Pred_Horizon[1,5] - rX_Target[1,5]));
rLambda_Costate[1, 6] := (rA_Mat[1,6] * rLambda_Costate[2,1]) + (rA_Mat[2,6] * rLambda_Costate[2,2]) + (rA_Mat[3,6] * rLambda_Costate[2,3]) + (rA_Mat[4,6] * rLambda_Costate[2,4]) + (rA_Mat[5,6] * rLambda_Costate[2,5]) + (rA_Mat[6,6] * rLambda_Costate[2,6]) + (rQ_Diag[6] * (rX_Pred_Horizon[1,6] - rX_Target[1,6]));

(* Iteration 7 - Analytical Gradient Computation w.r.t. Control Inputs u_h *)
rMPC_GradNormSq := 0.0;
(* Gradient for u_1 (h=1) *)
rGrad_J[1, 1] := (rB_Mat[1,1] * rLambda_Costate[1,1]) + (rB_Mat[2,1] * rLambda_Costate[1,2]) + (rB_Mat[3,1] * rLambda_Costate[1,3]) + (rB_Mat[4,1] * rLambda_Costate[1,4]) + (rB_Mat[5,1] * rLambda_Costate[1,5]) + (rB_Mat[6,1] * rLambda_Costate[1,6]) + (rR_Diag[1] * rU_Opt_Seq[1,1]) + (rS_Diag[1] * (rU_Opt_Seq[1,1] - a_u_prev[1])) - (rS_Diag[1] * (rU_Opt_Seq[2,1] - rU_Opt_Seq[1,1]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[1, 1] * rGrad_J[1, 1]);
rGrad_J[1, 2] := (rB_Mat[1,2] * rLambda_Costate[1,1]) + (rB_Mat[2,2] * rLambda_Costate[1,2]) + (rB_Mat[3,2] * rLambda_Costate[1,3]) + (rB_Mat[4,2] * rLambda_Costate[1,4]) + (rB_Mat[5,2] * rLambda_Costate[1,5]) + (rB_Mat[6,2] * rLambda_Costate[1,6]) + (rR_Diag[2] * rU_Opt_Seq[1,2]) + (rS_Diag[2] * (rU_Opt_Seq[1,2] - a_u_prev[2])) - (rS_Diag[2] * (rU_Opt_Seq[2,2] - rU_Opt_Seq[1,2]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[1, 2] * rGrad_J[1, 2]);
rGrad_J[1, 3] := (rB_Mat[1,3] * rLambda_Costate[1,1]) + (rB_Mat[2,3] * rLambda_Costate[1,2]) + (rB_Mat[3,3] * rLambda_Costate[1,3]) + (rB_Mat[4,3] * rLambda_Costate[1,4]) + (rB_Mat[5,3] * rLambda_Costate[1,5]) + (rB_Mat[6,3] * rLambda_Costate[1,6]) + (rR_Diag[3] * rU_Opt_Seq[1,3]) + (rS_Diag[3] * (rU_Opt_Seq[1,3] - a_u_prev[3])) - (rS_Diag[3] * (rU_Opt_Seq[2,3] - rU_Opt_Seq[1,3]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[1, 3] * rGrad_J[1, 3]);
rGrad_J[1, 4] := (rB_Mat[1,4] * rLambda_Costate[1,1]) + (rB_Mat[2,4] * rLambda_Costate[1,2]) + (rB_Mat[3,4] * rLambda_Costate[1,3]) + (rB_Mat[4,4] * rLambda_Costate[1,4]) + (rB_Mat[5,4] * rLambda_Costate[1,5]) + (rB_Mat[6,4] * rLambda_Costate[1,6]) + (rR_Diag[4] * rU_Opt_Seq[1,4]) + (rS_Diag[4] * (rU_Opt_Seq[1,4] - a_u_prev[4])) - (rS_Diag[4] * (rU_Opt_Seq[2,4] - rU_Opt_Seq[1,4]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[1, 4] * rGrad_J[1, 4]);
rGrad_J[1, 5] := (rB_Mat[1,5] * rLambda_Costate[1,1]) + (rB_Mat[2,5] * rLambda_Costate[1,2]) + (rB_Mat[3,5] * rLambda_Costate[1,3]) + (rB_Mat[4,5] * rLambda_Costate[1,4]) + (rB_Mat[5,5] * rLambda_Costate[1,5]) + (rB_Mat[6,5] * rLambda_Costate[1,6]) + (rR_Diag[5] * rU_Opt_Seq[1,5]) + (rS_Diag[5] * (rU_Opt_Seq[1,5] - a_u_prev[5])) - (rS_Diag[5] * (rU_Opt_Seq[2,5] - rU_Opt_Seq[1,5]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[1, 5] * rGrad_J[1, 5]);

(* Gradient for u_2 (h=2) *)
rGrad_J[2, 1] := (rB_Mat[1,1] * rLambda_Costate[2,1]) + (rB_Mat[2,1] * rLambda_Costate[2,2]) + (rB_Mat[3,1] * rLambda_Costate[2,3]) + (rB_Mat[4,1] * rLambda_Costate[2,4]) + (rB_Mat[5,1] * rLambda_Costate[2,5]) + (rB_Mat[6,1] * rLambda_Costate[2,6]) + (rR_Diag[1] * rU_Opt_Seq[2,1]) + (rS_Diag[1] * (rU_Opt_Seq[2,1] - rU_Opt_Seq[1,1])) - (rS_Diag[1] * (rU_Opt_Seq[3,1] - rU_Opt_Seq[2,1]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[2, 1] * rGrad_J[2, 1]);
rGrad_J[2, 2] := (rB_Mat[1,2] * rLambda_Costate[2,1]) + (rB_Mat[2,2] * rLambda_Costate[2,2]) + (rB_Mat[3,2] * rLambda_Costate[2,3]) + (rB_Mat[4,2] * rLambda_Costate[2,4]) + (rB_Mat[5,2] * rLambda_Costate[2,5]) + (rB_Mat[6,2] * rLambda_Costate[2,6]) + (rR_Diag[2] * rU_Opt_Seq[2,2]) + (rS_Diag[2] * (rU_Opt_Seq[2,2] - rU_Opt_Seq[1,2])) - (rS_Diag[2] * (rU_Opt_Seq[3,2] - rU_Opt_Seq[2,2]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[2, 2] * rGrad_J[2, 2]);
rGrad_J[2, 3] := (rB_Mat[1,3] * rLambda_Costate[2,1]) + (rB_Mat[2,3] * rLambda_Costate[2,2]) + (rB_Mat[3,3] * rLambda_Costate[2,3]) + (rB_Mat[4,3] * rLambda_Costate[2,4]) + (rB_Mat[5,3] * rLambda_Costate[2,5]) + (rB_Mat[6,3] * rLambda_Costate[2,6]) + (rR_Diag[3] * rU_Opt_Seq[2,3]) + (rS_Diag[3] * (rU_Opt_Seq[2,3] - rU_Opt_Seq[1,3])) - (rS_Diag[3] * (rU_Opt_Seq[3,3] - rU_Opt_Seq[2,3]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[2, 3] * rGrad_J[2, 3]);
rGrad_J[2, 4] := (rB_Mat[1,4] * rLambda_Costate[2,1]) + (rB_Mat[2,4] * rLambda_Costate[2,2]) + (rB_Mat[3,4] * rLambda_Costate[2,3]) + (rB_Mat[4,4] * rLambda_Costate[2,4]) + (rB_Mat[5,4] * rLambda_Costate[2,5]) + (rB_Mat[6,4] * rLambda_Costate[2,6]) + (rR_Diag[4] * rU_Opt_Seq[2,4]) + (rS_Diag[4] * (rU_Opt_Seq[2,4] - rU_Opt_Seq[1,4])) - (rS_Diag[4] * (rU_Opt_Seq[3,4] - rU_Opt_Seq[2,4]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[2, 4] * rGrad_J[2, 4]);
rGrad_J[2, 5] := (rB_Mat[1,5] * rLambda_Costate[2,1]) + (rB_Mat[2,5] * rLambda_Costate[2,2]) + (rB_Mat[3,5] * rLambda_Costate[2,3]) + (rB_Mat[4,5] * rLambda_Costate[2,4]) + (rB_Mat[5,5] * rLambda_Costate[2,5]) + (rB_Mat[6,5] * rLambda_Costate[2,6]) + (rR_Diag[5] * rU_Opt_Seq[2,5]) + (rS_Diag[5] * (rU_Opt_Seq[2,5] - rU_Opt_Seq[1,5])) - (rS_Diag[5] * (rU_Opt_Seq[3,5] - rU_Opt_Seq[2,5]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[2, 5] * rGrad_J[2, 5]);

(* Gradient for u_3 (h=3, held through h=4, 5) *)
rGrad_J[3, 1] := (rB_Mat[1,1] * (rLambda_Costate[3,1] + rLambda_Costate[4,1] + rLambda_Costate[5,1])) + (rB_Mat[2,1] * (rLambda_Costate[3,2] + rLambda_Costate[4,2] + rLambda_Costate[5,2])) + (rB_Mat[3,1] * (rLambda_Costate[3,3] + rLambda_Costate[4,3] + rLambda_Costate[5,3])) + (rB_Mat[4,1] * (rLambda_Costate[3,4] + rLambda_Costate[4,4] + rLambda_Costate[5,4])) + (rB_Mat[5,1] * (rLambda_Costate[3,5] + rLambda_Costate[4,5] + rLambda_Costate[5,5])) + (rB_Mat[6,1] * (rLambda_Costate[3,6] + rLambda_Costate[4,6] + rLambda_Costate[5,6])) + (rR_Diag[1] * rU_Opt_Seq[3,1]) + (rS_Diag[1] * (rU_Opt_Seq[3,1] - rU_Opt_Seq[2,1]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[3, 1] * rGrad_J[3, 1]);
rGrad_J[3, 2] := (rB_Mat[1,2] * (rLambda_Costate[3,1] + rLambda_Costate[4,1] + rLambda_Costate[5,1])) + (rB_Mat[2,2] * (rLambda_Costate[3,2] + rLambda_Costate[4,2] + rLambda_Costate[5,2])) + (rB_Mat[3,2] * (rLambda_Costate[3,3] + rLambda_Costate[4,3] + rLambda_Costate[5,3])) + (rB_Mat[4,2] * (rLambda_Costate[3,4] + rLambda_Costate[4,4] + rLambda_Costate[5,4])) + (rB_Mat[5,2] * (rLambda_Costate[3,5] + rLambda_Costate[4,5] + rLambda_Costate[5,5])) + (rB_Mat[6,2] * (rLambda_Costate[3,6] + rLambda_Costate[4,6] + rLambda_Costate[5,6])) + (rR_Diag[2] * rU_Opt_Seq[3,2]) + (rS_Diag[2] * (rU_Opt_Seq[3,2] - rU_Opt_Seq[2,2]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[3, 2] * rGrad_J[3, 2]);
rGrad_J[3, 3] := (rB_Mat[1,3] * (rLambda_Costate[3,1] + rLambda_Costate[4,1] + rLambda_Costate[5,1])) + (rB_Mat[2,3] * (rLambda_Costate[3,2] + rLambda_Costate[4,2] + rLambda_Costate[5,2])) + (rB_Mat[3,3] * (rLambda_Costate[3,3] + rLambda_Costate[4,3] + rLambda_Costate[5,3])) + (rB_Mat[4,3] * (rLambda_Costate[3,4] + rLambda_Costate[4,4] + rLambda_Costate[5,4])) + (rB_Mat[5,3] * (rLambda_Costate[3,5] + rLambda_Costate[4,5] + rLambda_Costate[5,5])) + (rB_Mat[6,3] * (rLambda_Costate[3,6] + rLambda_Costate[4,6] + rLambda_Costate[5,6])) + (rR_Diag[3] * rU_Opt_Seq[3,3]) + (rS_Diag[3] * (rU_Opt_Seq[3,3] - rU_Opt_Seq[2,3]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[3, 3] * rGrad_J[3, 3]);
rGrad_J[3, 4] := (rB_Mat[1,4] * (rLambda_Costate[3,1] + rLambda_Costate[4,1] + rLambda_Costate[5,1])) + (rB_Mat[2,4] * (rLambda_Costate[3,2] + rLambda_Costate[4,2] + rLambda_Costate[5,2])) + (rB_Mat[3,4] * (rLambda_Costate[3,3] + rLambda_Costate[4,3] + rLambda_Costate[5,3])) + (rB_Mat[4,4] * (rLambda_Costate[3,4] + rLambda_Costate[4,4] + rLambda_Costate[5,4])) + (rB_Mat[5,4] * (rLambda_Costate[3,5] + rLambda_Costate[4,5] + rLambda_Costate[5,5])) + (rB_Mat[6,4] * (rLambda_Costate[3,6] + rLambda_Costate[4,6] + rLambda_Costate[5,6])) + (rR_Diag[4] * rU_Opt_Seq[3,4]) + (rS_Diag[4] * (rU_Opt_Seq[3,4] - rU_Opt_Seq[2,4]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[3, 4] * rGrad_J[3, 4]);
rGrad_J[3, 5] := (rB_Mat[1,5] * (rLambda_Costate[3,1] + rLambda_Costate[4,1] + rLambda_Costate[5,1])) + (rB_Mat[2,5] * (rLambda_Costate[3,2] + rLambda_Costate[4,2] + rLambda_Costate[5,2])) + (rB_Mat[3,5] * (rLambda_Costate[3,3] + rLambda_Costate[4,3] + rLambda_Costate[5,3])) + (rB_Mat[4,5] * (rLambda_Costate[3,4] + rLambda_Costate[4,4] + rLambda_Costate[5,4])) + (rB_Mat[5,5] * (rLambda_Costate[3,5] + rLambda_Costate[4,5] + rLambda_Costate[5,5])) + (rB_Mat[6,5] * (rLambda_Costate[3,6] + rLambda_Costate[4,6] + rLambda_Costate[5,6])) + (rR_Diag[5] * rU_Opt_Seq[3,5]) + (rS_Diag[5] * (rU_Opt_Seq[3,5] - rU_Opt_Seq[2,5]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[3, 5] * rGrad_J[3, 5]);

(* Iteration 7 - Projected Gradient Step with Hard Box & Dynamic Slew Limits *)
rTemp_Val := rU_Opt_Seq[1, 1] - (rAlpha_PGD_StepSize * rGrad_J[1, 1]);
(* Slew limit against prior actuator output *)
IF rTemp_Val > (a_u_prev[1] + rDeltaU_Max[1]) THEN
    rTemp_Val := a_u_prev[1] + rDeltaU_Max[1];
ELSIF rTemp_Val < (a_u_prev[1] - rDeltaU_Max[1]) THEN
    rTemp_Val := a_u_prev[1] - rDeltaU_Max[1];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[1] THEN
    rTemp_Val := rU_BoxMax[1];
ELSIF rTemp_Val < rU_BoxMin[1] THEN
    rTemp_Val := rU_BoxMin[1];
END_IF;
rU_Opt_Seq[1, 1] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[1, 2] - (rAlpha_PGD_StepSize * rGrad_J[1, 2]);
(* Slew limit against prior actuator output *)
IF rTemp_Val > (a_u_prev[2] + rDeltaU_Max[2]) THEN
    rTemp_Val := a_u_prev[2] + rDeltaU_Max[2];
ELSIF rTemp_Val < (a_u_prev[2] - rDeltaU_Max[2]) THEN
    rTemp_Val := a_u_prev[2] - rDeltaU_Max[2];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[2] THEN
    rTemp_Val := rU_BoxMax[2];
ELSIF rTemp_Val < rU_BoxMin[2] THEN
    rTemp_Val := rU_BoxMin[2];
END_IF;
rU_Opt_Seq[1, 2] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[1, 3] - (rAlpha_PGD_StepSize * rGrad_J[1, 3]);
(* Slew limit against prior actuator output *)
IF rTemp_Val > (a_u_prev[3] + rDeltaU_Max[3]) THEN
    rTemp_Val := a_u_prev[3] + rDeltaU_Max[3];
ELSIF rTemp_Val < (a_u_prev[3] - rDeltaU_Max[3]) THEN
    rTemp_Val := a_u_prev[3] - rDeltaU_Max[3];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[3] THEN
    rTemp_Val := rU_BoxMax[3];
ELSIF rTemp_Val < rU_BoxMin[3] THEN
    rTemp_Val := rU_BoxMin[3];
END_IF;
rU_Opt_Seq[1, 3] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[1, 4] - (rAlpha_PGD_StepSize * rGrad_J[1, 4]);
(* Slew limit against prior actuator output *)
IF rTemp_Val > (a_u_prev[4] + rDeltaU_Max[4]) THEN
    rTemp_Val := a_u_prev[4] + rDeltaU_Max[4];
ELSIF rTemp_Val < (a_u_prev[4] - rDeltaU_Max[4]) THEN
    rTemp_Val := a_u_prev[4] - rDeltaU_Max[4];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[4] THEN
    rTemp_Val := rU_BoxMax[4];
ELSIF rTemp_Val < rU_BoxMin[4] THEN
    rTemp_Val := rU_BoxMin[4];
END_IF;
rU_Opt_Seq[1, 4] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[1, 5] - (rAlpha_PGD_StepSize * rGrad_J[1, 5]);
(* Slew limit against prior actuator output *)
IF rTemp_Val > (a_u_prev[5] + rDeltaU_Max[5]) THEN
    rTemp_Val := a_u_prev[5] + rDeltaU_Max[5];
ELSIF rTemp_Val < (a_u_prev[5] - rDeltaU_Max[5]) THEN
    rTemp_Val := a_u_prev[5] - rDeltaU_Max[5];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[5] THEN
    rTemp_Val := rU_BoxMax[5];
ELSIF rTemp_Val < rU_BoxMin[5] THEN
    rTemp_Val := rU_BoxMin[5];
END_IF;
rU_Opt_Seq[1, 5] := rTemp_Val;

rTemp_Val := rU_Opt_Seq[2, 1] - (rAlpha_PGD_StepSize * rGrad_J[2, 1]);
(* Slew limit against step 1 *)
IF rTemp_Val > (rU_Opt_Seq[1, 1] + rDeltaU_Max[1]) THEN
    rTemp_Val := rU_Opt_Seq[1, 1] + rDeltaU_Max[1];
ELSIF rTemp_Val < (rU_Opt_Seq[1, 1] - rDeltaU_Max[1]) THEN
    rTemp_Val := rU_Opt_Seq[1, 1] - rDeltaU_Max[1];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[1] THEN
    rTemp_Val := rU_BoxMax[1];
ELSIF rTemp_Val < rU_BoxMin[1] THEN
    rTemp_Val := rU_BoxMin[1];
END_IF;
rU_Opt_Seq[2, 1] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[2, 2] - (rAlpha_PGD_StepSize * rGrad_J[2, 2]);
(* Slew limit against step 1 *)
IF rTemp_Val > (rU_Opt_Seq[1, 2] + rDeltaU_Max[2]) THEN
    rTemp_Val := rU_Opt_Seq[1, 2] + rDeltaU_Max[2];
ELSIF rTemp_Val < (rU_Opt_Seq[1, 2] - rDeltaU_Max[2]) THEN
    rTemp_Val := rU_Opt_Seq[1, 2] - rDeltaU_Max[2];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[2] THEN
    rTemp_Val := rU_BoxMax[2];
ELSIF rTemp_Val < rU_BoxMin[2] THEN
    rTemp_Val := rU_BoxMin[2];
END_IF;
rU_Opt_Seq[2, 2] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[2, 3] - (rAlpha_PGD_StepSize * rGrad_J[2, 3]);
(* Slew limit against step 1 *)
IF rTemp_Val > (rU_Opt_Seq[1, 3] + rDeltaU_Max[3]) THEN
    rTemp_Val := rU_Opt_Seq[1, 3] + rDeltaU_Max[3];
ELSIF rTemp_Val < (rU_Opt_Seq[1, 3] - rDeltaU_Max[3]) THEN
    rTemp_Val := rU_Opt_Seq[1, 3] - rDeltaU_Max[3];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[3] THEN
    rTemp_Val := rU_BoxMax[3];
ELSIF rTemp_Val < rU_BoxMin[3] THEN
    rTemp_Val := rU_BoxMin[3];
END_IF;
rU_Opt_Seq[2, 3] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[2, 4] - (rAlpha_PGD_StepSize * rGrad_J[2, 4]);
(* Slew limit against step 1 *)
IF rTemp_Val > (rU_Opt_Seq[1, 4] + rDeltaU_Max[4]) THEN
    rTemp_Val := rU_Opt_Seq[1, 4] + rDeltaU_Max[4];
ELSIF rTemp_Val < (rU_Opt_Seq[1, 4] - rDeltaU_Max[4]) THEN
    rTemp_Val := rU_Opt_Seq[1, 4] - rDeltaU_Max[4];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[4] THEN
    rTemp_Val := rU_BoxMax[4];
ELSIF rTemp_Val < rU_BoxMin[4] THEN
    rTemp_Val := rU_BoxMin[4];
END_IF;
rU_Opt_Seq[2, 4] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[2, 5] - (rAlpha_PGD_StepSize * rGrad_J[2, 5]);
(* Slew limit against step 1 *)
IF rTemp_Val > (rU_Opt_Seq[1, 5] + rDeltaU_Max[5]) THEN
    rTemp_Val := rU_Opt_Seq[1, 5] + rDeltaU_Max[5];
ELSIF rTemp_Val < (rU_Opt_Seq[1, 5] - rDeltaU_Max[5]) THEN
    rTemp_Val := rU_Opt_Seq[1, 5] - rDeltaU_Max[5];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[5] THEN
    rTemp_Val := rU_BoxMax[5];
ELSIF rTemp_Val < rU_BoxMin[5] THEN
    rTemp_Val := rU_BoxMin[5];
END_IF;
rU_Opt_Seq[2, 5] := rTemp_Val;

rTemp_Val := rU_Opt_Seq[3, 1] - (rAlpha_PGD_StepSize * rGrad_J[3, 1]);
(* Slew limit against step 2 *)
IF rTemp_Val > (rU_Opt_Seq[2, 1] + rDeltaU_Max[1]) THEN
    rTemp_Val := rU_Opt_Seq[2, 1] + rDeltaU_Max[1];
ELSIF rTemp_Val < (rU_Opt_Seq[2, 1] - rDeltaU_Max[1]) THEN
    rTemp_Val := rU_Opt_Seq[2, 1] - rDeltaU_Max[1];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[1] THEN
    rTemp_Val := rU_BoxMax[1];
ELSIF rTemp_Val < rU_BoxMin[1] THEN
    rTemp_Val := rU_BoxMin[1];
END_IF;
rU_Opt_Seq[3, 1] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[3, 2] - (rAlpha_PGD_StepSize * rGrad_J[3, 2]);
(* Slew limit against step 2 *)
IF rTemp_Val > (rU_Opt_Seq[2, 2] + rDeltaU_Max[2]) THEN
    rTemp_Val := rU_Opt_Seq[2, 2] + rDeltaU_Max[2];
ELSIF rTemp_Val < (rU_Opt_Seq[2, 2] - rDeltaU_Max[2]) THEN
    rTemp_Val := rU_Opt_Seq[2, 2] - rDeltaU_Max[2];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[2] THEN
    rTemp_Val := rU_BoxMax[2];
ELSIF rTemp_Val < rU_BoxMin[2] THEN
    rTemp_Val := rU_BoxMin[2];
END_IF;
rU_Opt_Seq[3, 2] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[3, 3] - (rAlpha_PGD_StepSize * rGrad_J[3, 3]);
(* Slew limit against step 2 *)
IF rTemp_Val > (rU_Opt_Seq[2, 3] + rDeltaU_Max[3]) THEN
    rTemp_Val := rU_Opt_Seq[2, 3] + rDeltaU_Max[3];
ELSIF rTemp_Val < (rU_Opt_Seq[2, 3] - rDeltaU_Max[3]) THEN
    rTemp_Val := rU_Opt_Seq[2, 3] - rDeltaU_Max[3];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[3] THEN
    rTemp_Val := rU_BoxMax[3];
ELSIF rTemp_Val < rU_BoxMin[3] THEN
    rTemp_Val := rU_BoxMin[3];
END_IF;
rU_Opt_Seq[3, 3] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[3, 4] - (rAlpha_PGD_StepSize * rGrad_J[3, 4]);
(* Slew limit against step 2 *)
IF rTemp_Val > (rU_Opt_Seq[2, 4] + rDeltaU_Max[4]) THEN
    rTemp_Val := rU_Opt_Seq[2, 4] + rDeltaU_Max[4];
ELSIF rTemp_Val < (rU_Opt_Seq[2, 4] - rDeltaU_Max[4]) THEN
    rTemp_Val := rU_Opt_Seq[2, 4] - rDeltaU_Max[4];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[4] THEN
    rTemp_Val := rU_BoxMax[4];
ELSIF rTemp_Val < rU_BoxMin[4] THEN
    rTemp_Val := rU_BoxMin[4];
END_IF;
rU_Opt_Seq[3, 4] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[3, 5] - (rAlpha_PGD_StepSize * rGrad_J[3, 5]);
(* Slew limit against step 2 *)
IF rTemp_Val > (rU_Opt_Seq[2, 5] + rDeltaU_Max[5]) THEN
    rTemp_Val := rU_Opt_Seq[2, 5] + rDeltaU_Max[5];
ELSIF rTemp_Val < (rU_Opt_Seq[2, 5] - rDeltaU_Max[5]) THEN
    rTemp_Val := rU_Opt_Seq[2, 5] - rDeltaU_Max[5];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[5] THEN
    rTemp_Val := rU_BoxMax[5];
ELSIF rTemp_Val < rU_BoxMin[5] THEN
    rTemp_Val := rU_BoxMin[5];
END_IF;
rU_Opt_Seq[3, 5] := rTemp_Val;

(* ================================================================================================== *)
(* MPC PROJECTED GRADIENT DESCENT -- UNROLLED ITERATION 8 OF 10                                 *)
(* ================================================================================================== *)
iPGD_IterCount := 8;

(* Iteration 8 - Forward State Prediction Step 1 (h=1): x_1 = A * x_hat + B * u_1 *)
rX_Pred_Horizon[1, 1] := (rA_Mat[1,1] * a_x_hat[1]) + (rA_Mat[1,2] * a_x_hat[2]) + (rA_Mat[1,3] * a_x_hat[3]) + (rA_Mat[1,4] * a_x_hat[4]) + (rA_Mat[1,5] * a_x_hat[5]) + (rA_Mat[1,6] * a_x_hat[6]) + (rB_Mat[1,1] * rU_Opt_Seq[1,1]) + (rB_Mat[1,2] * rU_Opt_Seq[1,2]) + (rB_Mat[1,3] * rU_Opt_Seq[1,3]) + (rB_Mat[1,4] * rU_Opt_Seq[1,4]) + (rB_Mat[1,5] * rU_Opt_Seq[1,5]);
rX_Pred_Horizon[1, 2] := (rA_Mat[2,1] * a_x_hat[1]) + (rA_Mat[2,2] * a_x_hat[2]) + (rA_Mat[2,3] * a_x_hat[3]) + (rA_Mat[2,4] * a_x_hat[4]) + (rA_Mat[2,5] * a_x_hat[5]) + (rA_Mat[2,6] * a_x_hat[6]) + (rB_Mat[2,1] * rU_Opt_Seq[1,1]) + (rB_Mat[2,2] * rU_Opt_Seq[1,2]) + (rB_Mat[2,3] * rU_Opt_Seq[1,3]) + (rB_Mat[2,4] * rU_Opt_Seq[1,4]) + (rB_Mat[2,5] * rU_Opt_Seq[1,5]);
rX_Pred_Horizon[1, 3] := (rA_Mat[3,1] * a_x_hat[1]) + (rA_Mat[3,2] * a_x_hat[2]) + (rA_Mat[3,3] * a_x_hat[3]) + (rA_Mat[3,4] * a_x_hat[4]) + (rA_Mat[3,5] * a_x_hat[5]) + (rA_Mat[3,6] * a_x_hat[6]) + (rB_Mat[3,1] * rU_Opt_Seq[1,1]) + (rB_Mat[3,2] * rU_Opt_Seq[1,2]) + (rB_Mat[3,3] * rU_Opt_Seq[1,3]) + (rB_Mat[3,4] * rU_Opt_Seq[1,4]) + (rB_Mat[3,5] * rU_Opt_Seq[1,5]);
rX_Pred_Horizon[1, 4] := (rA_Mat[4,1] * a_x_hat[1]) + (rA_Mat[4,2] * a_x_hat[2]) + (rA_Mat[4,3] * a_x_hat[3]) + (rA_Mat[4,4] * a_x_hat[4]) + (rA_Mat[4,5] * a_x_hat[5]) + (rA_Mat[4,6] * a_x_hat[6]) + (rB_Mat[4,1] * rU_Opt_Seq[1,1]) + (rB_Mat[4,2] * rU_Opt_Seq[1,2]) + (rB_Mat[4,3] * rU_Opt_Seq[1,3]) + (rB_Mat[4,4] * rU_Opt_Seq[1,4]) + (rB_Mat[4,5] * rU_Opt_Seq[1,5]);
rX_Pred_Horizon[1, 5] := (rA_Mat[5,1] * a_x_hat[1]) + (rA_Mat[5,2] * a_x_hat[2]) + (rA_Mat[5,3] * a_x_hat[3]) + (rA_Mat[5,4] * a_x_hat[4]) + (rA_Mat[5,5] * a_x_hat[5]) + (rA_Mat[5,6] * a_x_hat[6]) + (rB_Mat[5,1] * rU_Opt_Seq[1,1]) + (rB_Mat[5,2] * rU_Opt_Seq[1,2]) + (rB_Mat[5,3] * rU_Opt_Seq[1,3]) + (rB_Mat[5,4] * rU_Opt_Seq[1,4]) + (rB_Mat[5,5] * rU_Opt_Seq[1,5]);
rX_Pred_Horizon[1, 6] := (rA_Mat[6,1] * a_x_hat[1]) + (rA_Mat[6,2] * a_x_hat[2]) + (rA_Mat[6,3] * a_x_hat[3]) + (rA_Mat[6,4] * a_x_hat[4]) + (rA_Mat[6,5] * a_x_hat[5]) + (rA_Mat[6,6] * a_x_hat[6]) + (rB_Mat[6,1] * rU_Opt_Seq[1,1]) + (rB_Mat[6,2] * rU_Opt_Seq[1,2]) + (rB_Mat[6,3] * rU_Opt_Seq[1,3]) + (rB_Mat[6,4] * rU_Opt_Seq[1,4]) + (rB_Mat[6,5] * rU_Opt_Seq[1,5]);

(* Iteration 8 - Forward State Prediction Step 2 (h=2): x_2 = A * x_1 + B * u_2 *)
rX_Pred_Horizon[2, 1] := (rA_Mat[1,1] * rX_Pred_Horizon[1,1]) + (rA_Mat[1,2] * rX_Pred_Horizon[1,2]) + (rA_Mat[1,3] * rX_Pred_Horizon[1,3]) + (rA_Mat[1,4] * rX_Pred_Horizon[1,4]) + (rA_Mat[1,5] * rX_Pred_Horizon[1,5]) + (rA_Mat[1,6] * rX_Pred_Horizon[1,6]) + (rB_Mat[1,1] * rU_Opt_Seq[2,1]) + (rB_Mat[1,2] * rU_Opt_Seq[2,2]) + (rB_Mat[1,3] * rU_Opt_Seq[2,3]) + (rB_Mat[1,4] * rU_Opt_Seq[2,4]) + (rB_Mat[1,5] * rU_Opt_Seq[2,5]);
rX_Pred_Horizon[2, 2] := (rA_Mat[2,1] * rX_Pred_Horizon[1,1]) + (rA_Mat[2,2] * rX_Pred_Horizon[1,2]) + (rA_Mat[2,3] * rX_Pred_Horizon[1,3]) + (rA_Mat[2,4] * rX_Pred_Horizon[1,4]) + (rA_Mat[2,5] * rX_Pred_Horizon[1,5]) + (rA_Mat[2,6] * rX_Pred_Horizon[1,6]) + (rB_Mat[2,1] * rU_Opt_Seq[2,1]) + (rB_Mat[2,2] * rU_Opt_Seq[2,2]) + (rB_Mat[2,3] * rU_Opt_Seq[2,3]) + (rB_Mat[2,4] * rU_Opt_Seq[2,4]) + (rB_Mat[2,5] * rU_Opt_Seq[2,5]);
rX_Pred_Horizon[2, 3] := (rA_Mat[3,1] * rX_Pred_Horizon[1,1]) + (rA_Mat[3,2] * rX_Pred_Horizon[1,2]) + (rA_Mat[3,3] * rX_Pred_Horizon[1,3]) + (rA_Mat[3,4] * rX_Pred_Horizon[1,4]) + (rA_Mat[3,5] * rX_Pred_Horizon[1,5]) + (rA_Mat[3,6] * rX_Pred_Horizon[1,6]) + (rB_Mat[3,1] * rU_Opt_Seq[2,1]) + (rB_Mat[3,2] * rU_Opt_Seq[2,2]) + (rB_Mat[3,3] * rU_Opt_Seq[2,3]) + (rB_Mat[3,4] * rU_Opt_Seq[2,4]) + (rB_Mat[3,5] * rU_Opt_Seq[2,5]);
rX_Pred_Horizon[2, 4] := (rA_Mat[4,1] * rX_Pred_Horizon[1,1]) + (rA_Mat[4,2] * rX_Pred_Horizon[1,2]) + (rA_Mat[4,3] * rX_Pred_Horizon[1,3]) + (rA_Mat[4,4] * rX_Pred_Horizon[1,4]) + (rA_Mat[4,5] * rX_Pred_Horizon[1,5]) + (rA_Mat[4,6] * rX_Pred_Horizon[1,6]) + (rB_Mat[4,1] * rU_Opt_Seq[2,1]) + (rB_Mat[4,2] * rU_Opt_Seq[2,2]) + (rB_Mat[4,3] * rU_Opt_Seq[2,3]) + (rB_Mat[4,4] * rU_Opt_Seq[2,4]) + (rB_Mat[4,5] * rU_Opt_Seq[2,5]);
rX_Pred_Horizon[2, 5] := (rA_Mat[5,1] * rX_Pred_Horizon[1,1]) + (rA_Mat[5,2] * rX_Pred_Horizon[1,2]) + (rA_Mat[5,3] * rX_Pred_Horizon[1,3]) + (rA_Mat[5,4] * rX_Pred_Horizon[1,4]) + (rA_Mat[5,5] * rX_Pred_Horizon[1,5]) + (rA_Mat[5,6] * rX_Pred_Horizon[1,6]) + (rB_Mat[5,1] * rU_Opt_Seq[2,1]) + (rB_Mat[5,2] * rU_Opt_Seq[2,2]) + (rB_Mat[5,3] * rU_Opt_Seq[2,3]) + (rB_Mat[5,4] * rU_Opt_Seq[2,4]) + (rB_Mat[5,5] * rU_Opt_Seq[2,5]);
rX_Pred_Horizon[2, 6] := (rA_Mat[6,1] * rX_Pred_Horizon[1,1]) + (rA_Mat[6,2] * rX_Pred_Horizon[1,2]) + (rA_Mat[6,3] * rX_Pred_Horizon[1,3]) + (rA_Mat[6,4] * rX_Pred_Horizon[1,4]) + (rA_Mat[6,5] * rX_Pred_Horizon[1,5]) + (rA_Mat[6,6] * rX_Pred_Horizon[1,6]) + (rB_Mat[6,1] * rU_Opt_Seq[2,1]) + (rB_Mat[6,2] * rU_Opt_Seq[2,2]) + (rB_Mat[6,3] * rU_Opt_Seq[2,3]) + (rB_Mat[6,4] * rU_Opt_Seq[2,4]) + (rB_Mat[6,5] * rU_Opt_Seq[2,5]);

(* Iteration 8 - Forward State Prediction Step 3 (h=3): x_3 = A * x_2 + B * u_3 *)
rX_Pred_Horizon[3, 1] := (rA_Mat[1,1] * rX_Pred_Horizon[2,1]) + (rA_Mat[1,2] * rX_Pred_Horizon[2,2]) + (rA_Mat[1,3] * rX_Pred_Horizon[2,3]) + (rA_Mat[1,4] * rX_Pred_Horizon[2,4]) + (rA_Mat[1,5] * rX_Pred_Horizon[2,5]) + (rA_Mat[1,6] * rX_Pred_Horizon[2,6]) + (rB_Mat[1,1] * rU_Opt_Seq[3,1]) + (rB_Mat[1,2] * rU_Opt_Seq[3,2]) + (rB_Mat[1,3] * rU_Opt_Seq[3,3]) + (rB_Mat[1,4] * rU_Opt_Seq[3,4]) + (rB_Mat[1,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[3, 2] := (rA_Mat[2,1] * rX_Pred_Horizon[2,1]) + (rA_Mat[2,2] * rX_Pred_Horizon[2,2]) + (rA_Mat[2,3] * rX_Pred_Horizon[2,3]) + (rA_Mat[2,4] * rX_Pred_Horizon[2,4]) + (rA_Mat[2,5] * rX_Pred_Horizon[2,5]) + (rA_Mat[2,6] * rX_Pred_Horizon[2,6]) + (rB_Mat[2,1] * rU_Opt_Seq[3,1]) + (rB_Mat[2,2] * rU_Opt_Seq[3,2]) + (rB_Mat[2,3] * rU_Opt_Seq[3,3]) + (rB_Mat[2,4] * rU_Opt_Seq[3,4]) + (rB_Mat[2,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[3, 3] := (rA_Mat[3,1] * rX_Pred_Horizon[2,1]) + (rA_Mat[3,2] * rX_Pred_Horizon[2,2]) + (rA_Mat[3,3] * rX_Pred_Horizon[2,3]) + (rA_Mat[3,4] * rX_Pred_Horizon[2,4]) + (rA_Mat[3,5] * rX_Pred_Horizon[2,5]) + (rA_Mat[3,6] * rX_Pred_Horizon[2,6]) + (rB_Mat[3,1] * rU_Opt_Seq[3,1]) + (rB_Mat[3,2] * rU_Opt_Seq[3,2]) + (rB_Mat[3,3] * rU_Opt_Seq[3,3]) + (rB_Mat[3,4] * rU_Opt_Seq[3,4]) + (rB_Mat[3,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[3, 4] := (rA_Mat[4,1] * rX_Pred_Horizon[2,1]) + (rA_Mat[4,2] * rX_Pred_Horizon[2,2]) + (rA_Mat[4,3] * rX_Pred_Horizon[2,3]) + (rA_Mat[4,4] * rX_Pred_Horizon[2,4]) + (rA_Mat[4,5] * rX_Pred_Horizon[2,5]) + (rA_Mat[4,6] * rX_Pred_Horizon[2,6]) + (rB_Mat[4,1] * rU_Opt_Seq[3,1]) + (rB_Mat[4,2] * rU_Opt_Seq[3,2]) + (rB_Mat[4,3] * rU_Opt_Seq[3,3]) + (rB_Mat[4,4] * rU_Opt_Seq[3,4]) + (rB_Mat[4,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[3, 5] := (rA_Mat[5,1] * rX_Pred_Horizon[2,1]) + (rA_Mat[5,2] * rX_Pred_Horizon[2,2]) + (rA_Mat[5,3] * rX_Pred_Horizon[2,3]) + (rA_Mat[5,4] * rX_Pred_Horizon[2,4]) + (rA_Mat[5,5] * rX_Pred_Horizon[2,5]) + (rA_Mat[5,6] * rX_Pred_Horizon[2,6]) + (rB_Mat[5,1] * rU_Opt_Seq[3,1]) + (rB_Mat[5,2] * rU_Opt_Seq[3,2]) + (rB_Mat[5,3] * rU_Opt_Seq[3,3]) + (rB_Mat[5,4] * rU_Opt_Seq[3,4]) + (rB_Mat[5,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[3, 6] := (rA_Mat[6,1] * rX_Pred_Horizon[2,1]) + (rA_Mat[6,2] * rX_Pred_Horizon[2,2]) + (rA_Mat[6,3] * rX_Pred_Horizon[2,3]) + (rA_Mat[6,4] * rX_Pred_Horizon[2,4]) + (rA_Mat[6,5] * rX_Pred_Horizon[2,5]) + (rA_Mat[6,6] * rX_Pred_Horizon[2,6]) + (rB_Mat[6,1] * rU_Opt_Seq[3,1]) + (rB_Mat[6,2] * rU_Opt_Seq[3,2]) + (rB_Mat[6,3] * rU_Opt_Seq[3,3]) + (rB_Mat[6,4] * rU_Opt_Seq[3,4]) + (rB_Mat[6,5] * rU_Opt_Seq[3,5]);

(* Iteration 8 - Forward State Prediction Step 4 (h=4): x_4 = A * x_3 + B * u_3 (held beyond Hu) *)
rX_Pred_Horizon[4, 1] := (rA_Mat[1,1] * rX_Pred_Horizon[3,1]) + (rA_Mat[1,2] * rX_Pred_Horizon[3,2]) + (rA_Mat[1,3] * rX_Pred_Horizon[3,3]) + (rA_Mat[1,4] * rX_Pred_Horizon[3,4]) + (rA_Mat[1,5] * rX_Pred_Horizon[3,5]) + (rA_Mat[1,6] * rX_Pred_Horizon[3,6]) + (rB_Mat[1,1] * rU_Opt_Seq[3,1]) + (rB_Mat[1,2] * rU_Opt_Seq[3,2]) + (rB_Mat[1,3] * rU_Opt_Seq[3,3]) + (rB_Mat[1,4] * rU_Opt_Seq[3,4]) + (rB_Mat[1,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[4, 2] := (rA_Mat[2,1] * rX_Pred_Horizon[3,1]) + (rA_Mat[2,2] * rX_Pred_Horizon[3,2]) + (rA_Mat[2,3] * rX_Pred_Horizon[3,3]) + (rA_Mat[2,4] * rX_Pred_Horizon[3,4]) + (rA_Mat[2,5] * rX_Pred_Horizon[3,5]) + (rA_Mat[2,6] * rX_Pred_Horizon[3,6]) + (rB_Mat[2,1] * rU_Opt_Seq[3,1]) + (rB_Mat[2,2] * rU_Opt_Seq[3,2]) + (rB_Mat[2,3] * rU_Opt_Seq[3,3]) + (rB_Mat[2,4] * rU_Opt_Seq[3,4]) + (rB_Mat[2,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[4, 3] := (rA_Mat[3,1] * rX_Pred_Horizon[3,1]) + (rA_Mat[3,2] * rX_Pred_Horizon[3,2]) + (rA_Mat[3,3] * rX_Pred_Horizon[3,3]) + (rA_Mat[3,4] * rX_Pred_Horizon[3,4]) + (rA_Mat[3,5] * rX_Pred_Horizon[3,5]) + (rA_Mat[3,6] * rX_Pred_Horizon[3,6]) + (rB_Mat[3,1] * rU_Opt_Seq[3,1]) + (rB_Mat[3,2] * rU_Opt_Seq[3,2]) + (rB_Mat[3,3] * rU_Opt_Seq[3,3]) + (rB_Mat[3,4] * rU_Opt_Seq[3,4]) + (rB_Mat[3,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[4, 4] := (rA_Mat[4,1] * rX_Pred_Horizon[3,1]) + (rA_Mat[4,2] * rX_Pred_Horizon[3,2]) + (rA_Mat[4,3] * rX_Pred_Horizon[3,3]) + (rA_Mat[4,4] * rX_Pred_Horizon[3,4]) + (rA_Mat[4,5] * rX_Pred_Horizon[3,5]) + (rA_Mat[4,6] * rX_Pred_Horizon[3,6]) + (rB_Mat[4,1] * rU_Opt_Seq[3,1]) + (rB_Mat[4,2] * rU_Opt_Seq[3,2]) + (rB_Mat[4,3] * rU_Opt_Seq[3,3]) + (rB_Mat[4,4] * rU_Opt_Seq[3,4]) + (rB_Mat[4,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[4, 5] := (rA_Mat[5,1] * rX_Pred_Horizon[3,1]) + (rA_Mat[5,2] * rX_Pred_Horizon[3,2]) + (rA_Mat[5,3] * rX_Pred_Horizon[3,3]) + (rA_Mat[5,4] * rX_Pred_Horizon[3,4]) + (rA_Mat[5,5] * rX_Pred_Horizon[3,5]) + (rA_Mat[5,6] * rX_Pred_Horizon[3,6]) + (rB_Mat[5,1] * rU_Opt_Seq[3,1]) + (rB_Mat[5,2] * rU_Opt_Seq[3,2]) + (rB_Mat[5,3] * rU_Opt_Seq[3,3]) + (rB_Mat[5,4] * rU_Opt_Seq[3,4]) + (rB_Mat[5,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[4, 6] := (rA_Mat[6,1] * rX_Pred_Horizon[3,1]) + (rA_Mat[6,2] * rX_Pred_Horizon[3,2]) + (rA_Mat[6,3] * rX_Pred_Horizon[3,3]) + (rA_Mat[6,4] * rX_Pred_Horizon[3,4]) + (rA_Mat[6,5] * rX_Pred_Horizon[3,5]) + (rA_Mat[6,6] * rX_Pred_Horizon[3,6]) + (rB_Mat[6,1] * rU_Opt_Seq[3,1]) + (rB_Mat[6,2] * rU_Opt_Seq[3,2]) + (rB_Mat[6,3] * rU_Opt_Seq[3,3]) + (rB_Mat[6,4] * rU_Opt_Seq[3,4]) + (rB_Mat[6,5] * rU_Opt_Seq[3,5]);

(* Iteration 8 - Forward State Prediction Step 5 (h=5): x_5 = A * x_4 + B * u_3 (held beyond Hu) *)
rX_Pred_Horizon[5, 1] := (rA_Mat[1,1] * rX_Pred_Horizon[4,1]) + (rA_Mat[1,2] * rX_Pred_Horizon[4,2]) + (rA_Mat[1,3] * rX_Pred_Horizon[4,3]) + (rA_Mat[1,4] * rX_Pred_Horizon[4,4]) + (rA_Mat[1,5] * rX_Pred_Horizon[4,5]) + (rA_Mat[1,6] * rX_Pred_Horizon[4,6]) + (rB_Mat[1,1] * rU_Opt_Seq[3,1]) + (rB_Mat[1,2] * rU_Opt_Seq[3,2]) + (rB_Mat[1,3] * rU_Opt_Seq[3,3]) + (rB_Mat[1,4] * rU_Opt_Seq[3,4]) + (rB_Mat[1,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[5, 2] := (rA_Mat[2,1] * rX_Pred_Horizon[4,1]) + (rA_Mat[2,2] * rX_Pred_Horizon[4,2]) + (rA_Mat[2,3] * rX_Pred_Horizon[4,3]) + (rA_Mat[2,4] * rX_Pred_Horizon[4,4]) + (rA_Mat[2,5] * rX_Pred_Horizon[4,5]) + (rA_Mat[2,6] * rX_Pred_Horizon[4,6]) + (rB_Mat[2,1] * rU_Opt_Seq[3,1]) + (rB_Mat[2,2] * rU_Opt_Seq[3,2]) + (rB_Mat[2,3] * rU_Opt_Seq[3,3]) + (rB_Mat[2,4] * rU_Opt_Seq[3,4]) + (rB_Mat[2,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[5, 3] := (rA_Mat[3,1] * rX_Pred_Horizon[4,1]) + (rA_Mat[3,2] * rX_Pred_Horizon[4,2]) + (rA_Mat[3,3] * rX_Pred_Horizon[4,3]) + (rA_Mat[3,4] * rX_Pred_Horizon[4,4]) + (rA_Mat[3,5] * rX_Pred_Horizon[4,5]) + (rA_Mat[3,6] * rX_Pred_Horizon[4,6]) + (rB_Mat[3,1] * rU_Opt_Seq[3,1]) + (rB_Mat[3,2] * rU_Opt_Seq[3,2]) + (rB_Mat[3,3] * rU_Opt_Seq[3,3]) + (rB_Mat[3,4] * rU_Opt_Seq[3,4]) + (rB_Mat[3,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[5, 4] := (rA_Mat[4,1] * rX_Pred_Horizon[4,1]) + (rA_Mat[4,2] * rX_Pred_Horizon[4,2]) + (rA_Mat[4,3] * rX_Pred_Horizon[4,3]) + (rA_Mat[4,4] * rX_Pred_Horizon[4,4]) + (rA_Mat[4,5] * rX_Pred_Horizon[4,5]) + (rA_Mat[4,6] * rX_Pred_Horizon[4,6]) + (rB_Mat[4,1] * rU_Opt_Seq[3,1]) + (rB_Mat[4,2] * rU_Opt_Seq[3,2]) + (rB_Mat[4,3] * rU_Opt_Seq[3,3]) + (rB_Mat[4,4] * rU_Opt_Seq[3,4]) + (rB_Mat[4,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[5, 5] := (rA_Mat[5,1] * rX_Pred_Horizon[4,1]) + (rA_Mat[5,2] * rX_Pred_Horizon[4,2]) + (rA_Mat[5,3] * rX_Pred_Horizon[4,3]) + (rA_Mat[5,4] * rX_Pred_Horizon[4,4]) + (rA_Mat[5,5] * rX_Pred_Horizon[4,5]) + (rA_Mat[5,6] * rX_Pred_Horizon[4,6]) + (rB_Mat[5,1] * rU_Opt_Seq[3,1]) + (rB_Mat[5,2] * rU_Opt_Seq[3,2]) + (rB_Mat[5,3] * rU_Opt_Seq[3,3]) + (rB_Mat[5,4] * rU_Opt_Seq[3,4]) + (rB_Mat[5,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[5, 6] := (rA_Mat[6,1] * rX_Pred_Horizon[4,1]) + (rA_Mat[6,2] * rX_Pred_Horizon[4,2]) + (rA_Mat[6,3] * rX_Pred_Horizon[4,3]) + (rA_Mat[6,4] * rX_Pred_Horizon[4,4]) + (rA_Mat[6,5] * rX_Pred_Horizon[4,5]) + (rA_Mat[6,6] * rX_Pred_Horizon[4,6]) + (rB_Mat[6,1] * rU_Opt_Seq[3,1]) + (rB_Mat[6,2] * rU_Opt_Seq[3,2]) + (rB_Mat[6,3] * rU_Opt_Seq[3,3]) + (rB_Mat[6,4] * rU_Opt_Seq[3,4]) + (rB_Mat[6,5] * rU_Opt_Seq[3,5]);

(* Iteration 8 - Evaluate Objective Function Cost J *)
rMPC_Cost_J := 0.0;
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[1] * (rX_Pred_Horizon[1,1] - rX_Target[1,1]) * (rX_Pred_Horizon[1,1] - rX_Target[1,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[2] * (rX_Pred_Horizon[1,2] - rX_Target[1,2]) * (rX_Pred_Horizon[1,2] - rX_Target[1,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[3] * (rX_Pred_Horizon[1,3] - rX_Target[1,3]) * (rX_Pred_Horizon[1,3] - rX_Target[1,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[4] * (rX_Pred_Horizon[1,4] - rX_Target[1,4]) * (rX_Pred_Horizon[1,4] - rX_Target[1,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[5] * (rX_Pred_Horizon[1,5] - rX_Target[1,5]) * (rX_Pred_Horizon[1,5] - rX_Target[1,5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[6] * (rX_Pred_Horizon[1,6] - rX_Target[1,6]) * (rX_Pred_Horizon[1,6] - rX_Target[1,6]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[1] * (rX_Pred_Horizon[2,1] - rX_Target[2,1]) * (rX_Pred_Horizon[2,1] - rX_Target[2,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[2] * (rX_Pred_Horizon[2,2] - rX_Target[2,2]) * (rX_Pred_Horizon[2,2] - rX_Target[2,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[3] * (rX_Pred_Horizon[2,3] - rX_Target[2,3]) * (rX_Pred_Horizon[2,3] - rX_Target[2,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[4] * (rX_Pred_Horizon[2,4] - rX_Target[2,4]) * (rX_Pred_Horizon[2,4] - rX_Target[2,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[5] * (rX_Pred_Horizon[2,5] - rX_Target[2,5]) * (rX_Pred_Horizon[2,5] - rX_Target[2,5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[6] * (rX_Pred_Horizon[2,6] - rX_Target[2,6]) * (rX_Pred_Horizon[2,6] - rX_Target[2,6]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[1] * (rX_Pred_Horizon[3,1] - rX_Target[3,1]) * (rX_Pred_Horizon[3,1] - rX_Target[3,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[2] * (rX_Pred_Horizon[3,2] - rX_Target[3,2]) * (rX_Pred_Horizon[3,2] - rX_Target[3,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[3] * (rX_Pred_Horizon[3,3] - rX_Target[3,3]) * (rX_Pred_Horizon[3,3] - rX_Target[3,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[4] * (rX_Pred_Horizon[3,4] - rX_Target[3,4]) * (rX_Pred_Horizon[3,4] - rX_Target[3,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[5] * (rX_Pred_Horizon[3,5] - rX_Target[3,5]) * (rX_Pred_Horizon[3,5] - rX_Target[3,5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[6] * (rX_Pred_Horizon[3,6] - rX_Target[3,6]) * (rX_Pred_Horizon[3,6] - rX_Target[3,6]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[1] * (rX_Pred_Horizon[4,1] - rX_Target[4,1]) * (rX_Pred_Horizon[4,1] - rX_Target[4,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[2] * (rX_Pred_Horizon[4,2] - rX_Target[4,2]) * (rX_Pred_Horizon[4,2] - rX_Target[4,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[3] * (rX_Pred_Horizon[4,3] - rX_Target[4,3]) * (rX_Pred_Horizon[4,3] - rX_Target[4,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[4] * (rX_Pred_Horizon[4,4] - rX_Target[4,4]) * (rX_Pred_Horizon[4,4] - rX_Target[4,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[5] * (rX_Pred_Horizon[4,5] - rX_Target[4,5]) * (rX_Pred_Horizon[4,5] - rX_Target[4,5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[6] * (rX_Pred_Horizon[4,6] - rX_Target[4,6]) * (rX_Pred_Horizon[4,6] - rX_Target[4,6]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[1] * (rX_Pred_Horizon[5,1] - rX_Target[5,1]) * (rX_Pred_Horizon[5,1] - rX_Target[5,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[2] * (rX_Pred_Horizon[5,2] - rX_Target[5,2]) * (rX_Pred_Horizon[5,2] - rX_Target[5,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[3] * (rX_Pred_Horizon[5,3] - rX_Target[5,3]) * (rX_Pred_Horizon[5,3] - rX_Target[5,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[4] * (rX_Pred_Horizon[5,4] - rX_Target[5,4]) * (rX_Pred_Horizon[5,4] - rX_Target[5,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[5] * (rX_Pred_Horizon[5,5] - rX_Target[5,5]) * (rX_Pred_Horizon[5,5] - rX_Target[5,5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[6] * (rX_Pred_Horizon[5,6] - rX_Target[5,6]) * (rX_Pred_Horizon[5,6] - rX_Target[5,6]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rP_Diag[1] * (rX_Pred_Horizon[5,1] - rX_Target[5,1]) * (rX_Pred_Horizon[5,1] - rX_Target[5,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rP_Diag[2] * (rX_Pred_Horizon[5,2] - rX_Target[5,2]) * (rX_Pred_Horizon[5,2] - rX_Target[5,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rP_Diag[3] * (rX_Pred_Horizon[5,3] - rX_Target[5,3]) * (rX_Pred_Horizon[5,3] - rX_Target[5,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rP_Diag[4] * (rX_Pred_Horizon[5,4] - rX_Target[5,4]) * (rX_Pred_Horizon[5,4] - rX_Target[5,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rP_Diag[5] * (rX_Pred_Horizon[5,5] - rX_Target[5,5]) * (rX_Pred_Horizon[5,5] - rX_Target[5,5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rP_Diag[6] * (rX_Pred_Horizon[5,6] - rX_Target[5,6]) * (rX_Pred_Horizon[5,6] - rX_Target[5,6]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[1] * rU_Opt_Seq[1,1] * rU_Opt_Seq[1,1]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[2] * rU_Opt_Seq[1,2] * rU_Opt_Seq[1,2]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[3] * rU_Opt_Seq[1,3] * rU_Opt_Seq[1,3]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[4] * rU_Opt_Seq[1,4] * rU_Opt_Seq[1,4]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[5] * rU_Opt_Seq[1,5] * rU_Opt_Seq[1,5]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[1] * rU_Opt_Seq[2,1] * rU_Opt_Seq[2,1]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[2] * rU_Opt_Seq[2,2] * rU_Opt_Seq[2,2]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[3] * rU_Opt_Seq[2,3] * rU_Opt_Seq[2,3]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[4] * rU_Opt_Seq[2,4] * rU_Opt_Seq[2,4]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[5] * rU_Opt_Seq[2,5] * rU_Opt_Seq[2,5]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[1] * rU_Opt_Seq[3,1] * rU_Opt_Seq[3,1]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[2] * rU_Opt_Seq[3,2] * rU_Opt_Seq[3,2]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[3] * rU_Opt_Seq[3,3] * rU_Opt_Seq[3,3]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[4] * rU_Opt_Seq[3,4] * rU_Opt_Seq[3,4]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[5] * rU_Opt_Seq[3,5] * rU_Opt_Seq[3,5]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[1] * (rU_Opt_Seq[1,1] - a_u_prev[1]) * (rU_Opt_Seq[1,1] - a_u_prev[1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[1] * (rU_Opt_Seq[2,1] - rU_Opt_Seq[1,1]) * (rU_Opt_Seq[2,1] - rU_Opt_Seq[1,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[1] * (rU_Opt_Seq[3,1] - rU_Opt_Seq[2,1]) * (rU_Opt_Seq[3,1] - rU_Opt_Seq[2,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[2] * (rU_Opt_Seq[1,2] - a_u_prev[2]) * (rU_Opt_Seq[1,2] - a_u_prev[2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[2] * (rU_Opt_Seq[2,2] - rU_Opt_Seq[1,2]) * (rU_Opt_Seq[2,2] - rU_Opt_Seq[1,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[2] * (rU_Opt_Seq[3,2] - rU_Opt_Seq[2,2]) * (rU_Opt_Seq[3,2] - rU_Opt_Seq[2,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[3] * (rU_Opt_Seq[1,3] - a_u_prev[3]) * (rU_Opt_Seq[1,3] - a_u_prev[3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[3] * (rU_Opt_Seq[2,3] - rU_Opt_Seq[1,3]) * (rU_Opt_Seq[2,3] - rU_Opt_Seq[1,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[3] * (rU_Opt_Seq[3,3] - rU_Opt_Seq[2,3]) * (rU_Opt_Seq[3,3] - rU_Opt_Seq[2,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[4] * (rU_Opt_Seq[1,4] - a_u_prev[4]) * (rU_Opt_Seq[1,4] - a_u_prev[4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[4] * (rU_Opt_Seq[2,4] - rU_Opt_Seq[1,4]) * (rU_Opt_Seq[2,4] - rU_Opt_Seq[1,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[4] * (rU_Opt_Seq[3,4] - rU_Opt_Seq[2,4]) * (rU_Opt_Seq[3,4] - rU_Opt_Seq[2,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[5] * (rU_Opt_Seq[1,5] - a_u_prev[5]) * (rU_Opt_Seq[1,5] - a_u_prev[5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[5] * (rU_Opt_Seq[2,5] - rU_Opt_Seq[1,5]) * (rU_Opt_Seq[2,5] - rU_Opt_Seq[1,5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[5] * (rU_Opt_Seq[3,5] - rU_Opt_Seq[2,5]) * (rU_Opt_Seq[3,5] - rU_Opt_Seq[2,5]));

(* Iteration 8 - Backward Adjoint Costate Propagation: lambda_h = A^T * lambda_{h+1} + Q * (x_h - x_ref) *)
(* Terminal Costate at h=5: lambda_5 = (P + Q) * (x_5 - x_target_5) *)
rLambda_Costate[5, 1] := (rP_Diag[1] + rQ_Diag[1]) * (rX_Pred_Horizon[5,1] - rX_Target[5,1]);
rLambda_Costate[5, 2] := (rP_Diag[2] + rQ_Diag[2]) * (rX_Pred_Horizon[5,2] - rX_Target[5,2]);
rLambda_Costate[5, 3] := (rP_Diag[3] + rQ_Diag[3]) * (rX_Pred_Horizon[5,3] - rX_Target[5,3]);
rLambda_Costate[5, 4] := (rP_Diag[4] + rQ_Diag[4]) * (rX_Pred_Horizon[5,4] - rX_Target[5,4]);
rLambda_Costate[5, 5] := (rP_Diag[5] + rQ_Diag[5]) * (rX_Pred_Horizon[5,5] - rX_Target[5,5]);
rLambda_Costate[5, 6] := (rP_Diag[6] + rQ_Diag[6]) * (rX_Pred_Horizon[5,6] - rX_Target[5,6]);

(* Adjoint Costate at h=4: lambda_4 = A^T * lambda_5 + Q * (x_4 - x_target_4) *)
rLambda_Costate[4, 1] := (rA_Mat[1,1] * rLambda_Costate[5,1]) + (rA_Mat[2,1] * rLambda_Costate[5,2]) + (rA_Mat[3,1] * rLambda_Costate[5,3]) + (rA_Mat[4,1] * rLambda_Costate[5,4]) + (rA_Mat[5,1] * rLambda_Costate[5,5]) + (rA_Mat[6,1] * rLambda_Costate[5,6]) + (rQ_Diag[1] * (rX_Pred_Horizon[4,1] - rX_Target[4,1]));
rLambda_Costate[4, 2] := (rA_Mat[1,2] * rLambda_Costate[5,1]) + (rA_Mat[2,2] * rLambda_Costate[5,2]) + (rA_Mat[3,2] * rLambda_Costate[5,3]) + (rA_Mat[4,2] * rLambda_Costate[5,4]) + (rA_Mat[5,2] * rLambda_Costate[5,5]) + (rA_Mat[6,2] * rLambda_Costate[5,6]) + (rQ_Diag[2] * (rX_Pred_Horizon[4,2] - rX_Target[4,2]));
rLambda_Costate[4, 3] := (rA_Mat[1,3] * rLambda_Costate[5,1]) + (rA_Mat[2,3] * rLambda_Costate[5,2]) + (rA_Mat[3,3] * rLambda_Costate[5,3]) + (rA_Mat[4,3] * rLambda_Costate[5,4]) + (rA_Mat[5,3] * rLambda_Costate[5,5]) + (rA_Mat[6,3] * rLambda_Costate[5,6]) + (rQ_Diag[3] * (rX_Pred_Horizon[4,3] - rX_Target[4,3]));
rLambda_Costate[4, 4] := (rA_Mat[1,4] * rLambda_Costate[5,1]) + (rA_Mat[2,4] * rLambda_Costate[5,2]) + (rA_Mat[3,4] * rLambda_Costate[5,3]) + (rA_Mat[4,4] * rLambda_Costate[5,4]) + (rA_Mat[5,4] * rLambda_Costate[5,5]) + (rA_Mat[6,4] * rLambda_Costate[5,6]) + (rQ_Diag[4] * (rX_Pred_Horizon[4,4] - rX_Target[4,4]));
rLambda_Costate[4, 5] := (rA_Mat[1,5] * rLambda_Costate[5,1]) + (rA_Mat[2,5] * rLambda_Costate[5,2]) + (rA_Mat[3,5] * rLambda_Costate[5,3]) + (rA_Mat[4,5] * rLambda_Costate[5,4]) + (rA_Mat[5,5] * rLambda_Costate[5,5]) + (rA_Mat[6,5] * rLambda_Costate[5,6]) + (rQ_Diag[5] * (rX_Pred_Horizon[4,5] - rX_Target[4,5]));
rLambda_Costate[4, 6] := (rA_Mat[1,6] * rLambda_Costate[5,1]) + (rA_Mat[2,6] * rLambda_Costate[5,2]) + (rA_Mat[3,6] * rLambda_Costate[5,3]) + (rA_Mat[4,6] * rLambda_Costate[5,4]) + (rA_Mat[5,6] * rLambda_Costate[5,5]) + (rA_Mat[6,6] * rLambda_Costate[5,6]) + (rQ_Diag[6] * (rX_Pred_Horizon[4,6] - rX_Target[4,6]));

(* Adjoint Costate at h=3: lambda_3 = A^T * lambda_4 + Q * (x_3 - x_target_3) *)
rLambda_Costate[3, 1] := (rA_Mat[1,1] * rLambda_Costate[4,1]) + (rA_Mat[2,1] * rLambda_Costate[4,2]) + (rA_Mat[3,1] * rLambda_Costate[4,3]) + (rA_Mat[4,1] * rLambda_Costate[4,4]) + (rA_Mat[5,1] * rLambda_Costate[4,5]) + (rA_Mat[6,1] * rLambda_Costate[4,6]) + (rQ_Diag[1] * (rX_Pred_Horizon[3,1] - rX_Target[3,1]));
rLambda_Costate[3, 2] := (rA_Mat[1,2] * rLambda_Costate[4,1]) + (rA_Mat[2,2] * rLambda_Costate[4,2]) + (rA_Mat[3,2] * rLambda_Costate[4,3]) + (rA_Mat[4,2] * rLambda_Costate[4,4]) + (rA_Mat[5,2] * rLambda_Costate[4,5]) + (rA_Mat[6,2] * rLambda_Costate[4,6]) + (rQ_Diag[2] * (rX_Pred_Horizon[3,2] - rX_Target[3,2]));
rLambda_Costate[3, 3] := (rA_Mat[1,3] * rLambda_Costate[4,1]) + (rA_Mat[2,3] * rLambda_Costate[4,2]) + (rA_Mat[3,3] * rLambda_Costate[4,3]) + (rA_Mat[4,3] * rLambda_Costate[4,4]) + (rA_Mat[5,3] * rLambda_Costate[4,5]) + (rA_Mat[6,3] * rLambda_Costate[4,6]) + (rQ_Diag[3] * (rX_Pred_Horizon[3,3] - rX_Target[3,3]));
rLambda_Costate[3, 4] := (rA_Mat[1,4] * rLambda_Costate[4,1]) + (rA_Mat[2,4] * rLambda_Costate[4,2]) + (rA_Mat[3,4] * rLambda_Costate[4,3]) + (rA_Mat[4,4] * rLambda_Costate[4,4]) + (rA_Mat[5,4] * rLambda_Costate[4,5]) + (rA_Mat[6,4] * rLambda_Costate[4,6]) + (rQ_Diag[4] * (rX_Pred_Horizon[3,4] - rX_Target[3,4]));
rLambda_Costate[3, 5] := (rA_Mat[1,5] * rLambda_Costate[4,1]) + (rA_Mat[2,5] * rLambda_Costate[4,2]) + (rA_Mat[3,5] * rLambda_Costate[4,3]) + (rA_Mat[4,5] * rLambda_Costate[4,4]) + (rA_Mat[5,5] * rLambda_Costate[4,5]) + (rA_Mat[6,5] * rLambda_Costate[4,6]) + (rQ_Diag[5] * (rX_Pred_Horizon[3,5] - rX_Target[3,5]));
rLambda_Costate[3, 6] := (rA_Mat[1,6] * rLambda_Costate[4,1]) + (rA_Mat[2,6] * rLambda_Costate[4,2]) + (rA_Mat[3,6] * rLambda_Costate[4,3]) + (rA_Mat[4,6] * rLambda_Costate[4,4]) + (rA_Mat[5,6] * rLambda_Costate[4,5]) + (rA_Mat[6,6] * rLambda_Costate[4,6]) + (rQ_Diag[6] * (rX_Pred_Horizon[3,6] - rX_Target[3,6]));

(* Adjoint Costate at h=2: lambda_2 = A^T * lambda_3 + Q * (x_2 - x_target_2) *)
rLambda_Costate[2, 1] := (rA_Mat[1,1] * rLambda_Costate[3,1]) + (rA_Mat[2,1] * rLambda_Costate[3,2]) + (rA_Mat[3,1] * rLambda_Costate[3,3]) + (rA_Mat[4,1] * rLambda_Costate[3,4]) + (rA_Mat[5,1] * rLambda_Costate[3,5]) + (rA_Mat[6,1] * rLambda_Costate[3,6]) + (rQ_Diag[1] * (rX_Pred_Horizon[2,1] - rX_Target[2,1]));
rLambda_Costate[2, 2] := (rA_Mat[1,2] * rLambda_Costate[3,1]) + (rA_Mat[2,2] * rLambda_Costate[3,2]) + (rA_Mat[3,2] * rLambda_Costate[3,3]) + (rA_Mat[4,2] * rLambda_Costate[3,4]) + (rA_Mat[5,2] * rLambda_Costate[3,5]) + (rA_Mat[6,2] * rLambda_Costate[3,6]) + (rQ_Diag[2] * (rX_Pred_Horizon[2,2] - rX_Target[2,2]));
rLambda_Costate[2, 3] := (rA_Mat[1,3] * rLambda_Costate[3,1]) + (rA_Mat[2,3] * rLambda_Costate[3,2]) + (rA_Mat[3,3] * rLambda_Costate[3,3]) + (rA_Mat[4,3] * rLambda_Costate[3,4]) + (rA_Mat[5,3] * rLambda_Costate[3,5]) + (rA_Mat[6,3] * rLambda_Costate[3,6]) + (rQ_Diag[3] * (rX_Pred_Horizon[2,3] - rX_Target[2,3]));
rLambda_Costate[2, 4] := (rA_Mat[1,4] * rLambda_Costate[3,1]) + (rA_Mat[2,4] * rLambda_Costate[3,2]) + (rA_Mat[3,4] * rLambda_Costate[3,3]) + (rA_Mat[4,4] * rLambda_Costate[3,4]) + (rA_Mat[5,4] * rLambda_Costate[3,5]) + (rA_Mat[6,4] * rLambda_Costate[3,6]) + (rQ_Diag[4] * (rX_Pred_Horizon[2,4] - rX_Target[2,4]));
rLambda_Costate[2, 5] := (rA_Mat[1,5] * rLambda_Costate[3,1]) + (rA_Mat[2,5] * rLambda_Costate[3,2]) + (rA_Mat[3,5] * rLambda_Costate[3,3]) + (rA_Mat[4,5] * rLambda_Costate[3,4]) + (rA_Mat[5,5] * rLambda_Costate[3,5]) + (rA_Mat[6,5] * rLambda_Costate[3,6]) + (rQ_Diag[5] * (rX_Pred_Horizon[2,5] - rX_Target[2,5]));
rLambda_Costate[2, 6] := (rA_Mat[1,6] * rLambda_Costate[3,1]) + (rA_Mat[2,6] * rLambda_Costate[3,2]) + (rA_Mat[3,6] * rLambda_Costate[3,3]) + (rA_Mat[4,6] * rLambda_Costate[3,4]) + (rA_Mat[5,6] * rLambda_Costate[3,5]) + (rA_Mat[6,6] * rLambda_Costate[3,6]) + (rQ_Diag[6] * (rX_Pred_Horizon[2,6] - rX_Target[2,6]));

(* Adjoint Costate at h=1: lambda_1 = A^T * lambda_2 + Q * (x_1 - x_target_1) *)
rLambda_Costate[1, 1] := (rA_Mat[1,1] * rLambda_Costate[2,1]) + (rA_Mat[2,1] * rLambda_Costate[2,2]) + (rA_Mat[3,1] * rLambda_Costate[2,3]) + (rA_Mat[4,1] * rLambda_Costate[2,4]) + (rA_Mat[5,1] * rLambda_Costate[2,5]) + (rA_Mat[6,1] * rLambda_Costate[2,6]) + (rQ_Diag[1] * (rX_Pred_Horizon[1,1] - rX_Target[1,1]));
rLambda_Costate[1, 2] := (rA_Mat[1,2] * rLambda_Costate[2,1]) + (rA_Mat[2,2] * rLambda_Costate[2,2]) + (rA_Mat[3,2] * rLambda_Costate[2,3]) + (rA_Mat[4,2] * rLambda_Costate[2,4]) + (rA_Mat[5,2] * rLambda_Costate[2,5]) + (rA_Mat[6,2] * rLambda_Costate[2,6]) + (rQ_Diag[2] * (rX_Pred_Horizon[1,2] - rX_Target[1,2]));
rLambda_Costate[1, 3] := (rA_Mat[1,3] * rLambda_Costate[2,1]) + (rA_Mat[2,3] * rLambda_Costate[2,2]) + (rA_Mat[3,3] * rLambda_Costate[2,3]) + (rA_Mat[4,3] * rLambda_Costate[2,4]) + (rA_Mat[5,3] * rLambda_Costate[2,5]) + (rA_Mat[6,3] * rLambda_Costate[2,6]) + (rQ_Diag[3] * (rX_Pred_Horizon[1,3] - rX_Target[1,3]));
rLambda_Costate[1, 4] := (rA_Mat[1,4] * rLambda_Costate[2,1]) + (rA_Mat[2,4] * rLambda_Costate[2,2]) + (rA_Mat[3,4] * rLambda_Costate[2,3]) + (rA_Mat[4,4] * rLambda_Costate[2,4]) + (rA_Mat[5,4] * rLambda_Costate[2,5]) + (rA_Mat[6,4] * rLambda_Costate[2,6]) + (rQ_Diag[4] * (rX_Pred_Horizon[1,4] - rX_Target[1,4]));
rLambda_Costate[1, 5] := (rA_Mat[1,5] * rLambda_Costate[2,1]) + (rA_Mat[2,5] * rLambda_Costate[2,2]) + (rA_Mat[3,5] * rLambda_Costate[2,3]) + (rA_Mat[4,5] * rLambda_Costate[2,4]) + (rA_Mat[5,5] * rLambda_Costate[2,5]) + (rA_Mat[6,5] * rLambda_Costate[2,6]) + (rQ_Diag[5] * (rX_Pred_Horizon[1,5] - rX_Target[1,5]));
rLambda_Costate[1, 6] := (rA_Mat[1,6] * rLambda_Costate[2,1]) + (rA_Mat[2,6] * rLambda_Costate[2,2]) + (rA_Mat[3,6] * rLambda_Costate[2,3]) + (rA_Mat[4,6] * rLambda_Costate[2,4]) + (rA_Mat[5,6] * rLambda_Costate[2,5]) + (rA_Mat[6,6] * rLambda_Costate[2,6]) + (rQ_Diag[6] * (rX_Pred_Horizon[1,6] - rX_Target[1,6]));

(* Iteration 8 - Analytical Gradient Computation w.r.t. Control Inputs u_h *)
rMPC_GradNormSq := 0.0;
(* Gradient for u_1 (h=1) *)
rGrad_J[1, 1] := (rB_Mat[1,1] * rLambda_Costate[1,1]) + (rB_Mat[2,1] * rLambda_Costate[1,2]) + (rB_Mat[3,1] * rLambda_Costate[1,3]) + (rB_Mat[4,1] * rLambda_Costate[1,4]) + (rB_Mat[5,1] * rLambda_Costate[1,5]) + (rB_Mat[6,1] * rLambda_Costate[1,6]) + (rR_Diag[1] * rU_Opt_Seq[1,1]) + (rS_Diag[1] * (rU_Opt_Seq[1,1] - a_u_prev[1])) - (rS_Diag[1] * (rU_Opt_Seq[2,1] - rU_Opt_Seq[1,1]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[1, 1] * rGrad_J[1, 1]);
rGrad_J[1, 2] := (rB_Mat[1,2] * rLambda_Costate[1,1]) + (rB_Mat[2,2] * rLambda_Costate[1,2]) + (rB_Mat[3,2] * rLambda_Costate[1,3]) + (rB_Mat[4,2] * rLambda_Costate[1,4]) + (rB_Mat[5,2] * rLambda_Costate[1,5]) + (rB_Mat[6,2] * rLambda_Costate[1,6]) + (rR_Diag[2] * rU_Opt_Seq[1,2]) + (rS_Diag[2] * (rU_Opt_Seq[1,2] - a_u_prev[2])) - (rS_Diag[2] * (rU_Opt_Seq[2,2] - rU_Opt_Seq[1,2]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[1, 2] * rGrad_J[1, 2]);
rGrad_J[1, 3] := (rB_Mat[1,3] * rLambda_Costate[1,1]) + (rB_Mat[2,3] * rLambda_Costate[1,2]) + (rB_Mat[3,3] * rLambda_Costate[1,3]) + (rB_Mat[4,3] * rLambda_Costate[1,4]) + (rB_Mat[5,3] * rLambda_Costate[1,5]) + (rB_Mat[6,3] * rLambda_Costate[1,6]) + (rR_Diag[3] * rU_Opt_Seq[1,3]) + (rS_Diag[3] * (rU_Opt_Seq[1,3] - a_u_prev[3])) - (rS_Diag[3] * (rU_Opt_Seq[2,3] - rU_Opt_Seq[1,3]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[1, 3] * rGrad_J[1, 3]);
rGrad_J[1, 4] := (rB_Mat[1,4] * rLambda_Costate[1,1]) + (rB_Mat[2,4] * rLambda_Costate[1,2]) + (rB_Mat[3,4] * rLambda_Costate[1,3]) + (rB_Mat[4,4] * rLambda_Costate[1,4]) + (rB_Mat[5,4] * rLambda_Costate[1,5]) + (rB_Mat[6,4] * rLambda_Costate[1,6]) + (rR_Diag[4] * rU_Opt_Seq[1,4]) + (rS_Diag[4] * (rU_Opt_Seq[1,4] - a_u_prev[4])) - (rS_Diag[4] * (rU_Opt_Seq[2,4] - rU_Opt_Seq[1,4]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[1, 4] * rGrad_J[1, 4]);
rGrad_J[1, 5] := (rB_Mat[1,5] * rLambda_Costate[1,1]) + (rB_Mat[2,5] * rLambda_Costate[1,2]) + (rB_Mat[3,5] * rLambda_Costate[1,3]) + (rB_Mat[4,5] * rLambda_Costate[1,4]) + (rB_Mat[5,5] * rLambda_Costate[1,5]) + (rB_Mat[6,5] * rLambda_Costate[1,6]) + (rR_Diag[5] * rU_Opt_Seq[1,5]) + (rS_Diag[5] * (rU_Opt_Seq[1,5] - a_u_prev[5])) - (rS_Diag[5] * (rU_Opt_Seq[2,5] - rU_Opt_Seq[1,5]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[1, 5] * rGrad_J[1, 5]);

(* Gradient for u_2 (h=2) *)
rGrad_J[2, 1] := (rB_Mat[1,1] * rLambda_Costate[2,1]) + (rB_Mat[2,1] * rLambda_Costate[2,2]) + (rB_Mat[3,1] * rLambda_Costate[2,3]) + (rB_Mat[4,1] * rLambda_Costate[2,4]) + (rB_Mat[5,1] * rLambda_Costate[2,5]) + (rB_Mat[6,1] * rLambda_Costate[2,6]) + (rR_Diag[1] * rU_Opt_Seq[2,1]) + (rS_Diag[1] * (rU_Opt_Seq[2,1] - rU_Opt_Seq[1,1])) - (rS_Diag[1] * (rU_Opt_Seq[3,1] - rU_Opt_Seq[2,1]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[2, 1] * rGrad_J[2, 1]);
rGrad_J[2, 2] := (rB_Mat[1,2] * rLambda_Costate[2,1]) + (rB_Mat[2,2] * rLambda_Costate[2,2]) + (rB_Mat[3,2] * rLambda_Costate[2,3]) + (rB_Mat[4,2] * rLambda_Costate[2,4]) + (rB_Mat[5,2] * rLambda_Costate[2,5]) + (rB_Mat[6,2] * rLambda_Costate[2,6]) + (rR_Diag[2] * rU_Opt_Seq[2,2]) + (rS_Diag[2] * (rU_Opt_Seq[2,2] - rU_Opt_Seq[1,2])) - (rS_Diag[2] * (rU_Opt_Seq[3,2] - rU_Opt_Seq[2,2]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[2, 2] * rGrad_J[2, 2]);
rGrad_J[2, 3] := (rB_Mat[1,3] * rLambda_Costate[2,1]) + (rB_Mat[2,3] * rLambda_Costate[2,2]) + (rB_Mat[3,3] * rLambda_Costate[2,3]) + (rB_Mat[4,3] * rLambda_Costate[2,4]) + (rB_Mat[5,3] * rLambda_Costate[2,5]) + (rB_Mat[6,3] * rLambda_Costate[2,6]) + (rR_Diag[3] * rU_Opt_Seq[2,3]) + (rS_Diag[3] * (rU_Opt_Seq[2,3] - rU_Opt_Seq[1,3])) - (rS_Diag[3] * (rU_Opt_Seq[3,3] - rU_Opt_Seq[2,3]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[2, 3] * rGrad_J[2, 3]);
rGrad_J[2, 4] := (rB_Mat[1,4] * rLambda_Costate[2,1]) + (rB_Mat[2,4] * rLambda_Costate[2,2]) + (rB_Mat[3,4] * rLambda_Costate[2,3]) + (rB_Mat[4,4] * rLambda_Costate[2,4]) + (rB_Mat[5,4] * rLambda_Costate[2,5]) + (rB_Mat[6,4] * rLambda_Costate[2,6]) + (rR_Diag[4] * rU_Opt_Seq[2,4]) + (rS_Diag[4] * (rU_Opt_Seq[2,4] - rU_Opt_Seq[1,4])) - (rS_Diag[4] * (rU_Opt_Seq[3,4] - rU_Opt_Seq[2,4]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[2, 4] * rGrad_J[2, 4]);
rGrad_J[2, 5] := (rB_Mat[1,5] * rLambda_Costate[2,1]) + (rB_Mat[2,5] * rLambda_Costate[2,2]) + (rB_Mat[3,5] * rLambda_Costate[2,3]) + (rB_Mat[4,5] * rLambda_Costate[2,4]) + (rB_Mat[5,5] * rLambda_Costate[2,5]) + (rB_Mat[6,5] * rLambda_Costate[2,6]) + (rR_Diag[5] * rU_Opt_Seq[2,5]) + (rS_Diag[5] * (rU_Opt_Seq[2,5] - rU_Opt_Seq[1,5])) - (rS_Diag[5] * (rU_Opt_Seq[3,5] - rU_Opt_Seq[2,5]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[2, 5] * rGrad_J[2, 5]);

(* Gradient for u_3 (h=3, held through h=4, 5) *)
rGrad_J[3, 1] := (rB_Mat[1,1] * (rLambda_Costate[3,1] + rLambda_Costate[4,1] + rLambda_Costate[5,1])) + (rB_Mat[2,1] * (rLambda_Costate[3,2] + rLambda_Costate[4,2] + rLambda_Costate[5,2])) + (rB_Mat[3,1] * (rLambda_Costate[3,3] + rLambda_Costate[4,3] + rLambda_Costate[5,3])) + (rB_Mat[4,1] * (rLambda_Costate[3,4] + rLambda_Costate[4,4] + rLambda_Costate[5,4])) + (rB_Mat[5,1] * (rLambda_Costate[3,5] + rLambda_Costate[4,5] + rLambda_Costate[5,5])) + (rB_Mat[6,1] * (rLambda_Costate[3,6] + rLambda_Costate[4,6] + rLambda_Costate[5,6])) + (rR_Diag[1] * rU_Opt_Seq[3,1]) + (rS_Diag[1] * (rU_Opt_Seq[3,1] - rU_Opt_Seq[2,1]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[3, 1] * rGrad_J[3, 1]);
rGrad_J[3, 2] := (rB_Mat[1,2] * (rLambda_Costate[3,1] + rLambda_Costate[4,1] + rLambda_Costate[5,1])) + (rB_Mat[2,2] * (rLambda_Costate[3,2] + rLambda_Costate[4,2] + rLambda_Costate[5,2])) + (rB_Mat[3,2] * (rLambda_Costate[3,3] + rLambda_Costate[4,3] + rLambda_Costate[5,3])) + (rB_Mat[4,2] * (rLambda_Costate[3,4] + rLambda_Costate[4,4] + rLambda_Costate[5,4])) + (rB_Mat[5,2] * (rLambda_Costate[3,5] + rLambda_Costate[4,5] + rLambda_Costate[5,5])) + (rB_Mat[6,2] * (rLambda_Costate[3,6] + rLambda_Costate[4,6] + rLambda_Costate[5,6])) + (rR_Diag[2] * rU_Opt_Seq[3,2]) + (rS_Diag[2] * (rU_Opt_Seq[3,2] - rU_Opt_Seq[2,2]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[3, 2] * rGrad_J[3, 2]);
rGrad_J[3, 3] := (rB_Mat[1,3] * (rLambda_Costate[3,1] + rLambda_Costate[4,1] + rLambda_Costate[5,1])) + (rB_Mat[2,3] * (rLambda_Costate[3,2] + rLambda_Costate[4,2] + rLambda_Costate[5,2])) + (rB_Mat[3,3] * (rLambda_Costate[3,3] + rLambda_Costate[4,3] + rLambda_Costate[5,3])) + (rB_Mat[4,3] * (rLambda_Costate[3,4] + rLambda_Costate[4,4] + rLambda_Costate[5,4])) + (rB_Mat[5,3] * (rLambda_Costate[3,5] + rLambda_Costate[4,5] + rLambda_Costate[5,5])) + (rB_Mat[6,3] * (rLambda_Costate[3,6] + rLambda_Costate[4,6] + rLambda_Costate[5,6])) + (rR_Diag[3] * rU_Opt_Seq[3,3]) + (rS_Diag[3] * (rU_Opt_Seq[3,3] - rU_Opt_Seq[2,3]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[3, 3] * rGrad_J[3, 3]);
rGrad_J[3, 4] := (rB_Mat[1,4] * (rLambda_Costate[3,1] + rLambda_Costate[4,1] + rLambda_Costate[5,1])) + (rB_Mat[2,4] * (rLambda_Costate[3,2] + rLambda_Costate[4,2] + rLambda_Costate[5,2])) + (rB_Mat[3,4] * (rLambda_Costate[3,3] + rLambda_Costate[4,3] + rLambda_Costate[5,3])) + (rB_Mat[4,4] * (rLambda_Costate[3,4] + rLambda_Costate[4,4] + rLambda_Costate[5,4])) + (rB_Mat[5,4] * (rLambda_Costate[3,5] + rLambda_Costate[4,5] + rLambda_Costate[5,5])) + (rB_Mat[6,4] * (rLambda_Costate[3,6] + rLambda_Costate[4,6] + rLambda_Costate[5,6])) + (rR_Diag[4] * rU_Opt_Seq[3,4]) + (rS_Diag[4] * (rU_Opt_Seq[3,4] - rU_Opt_Seq[2,4]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[3, 4] * rGrad_J[3, 4]);
rGrad_J[3, 5] := (rB_Mat[1,5] * (rLambda_Costate[3,1] + rLambda_Costate[4,1] + rLambda_Costate[5,1])) + (rB_Mat[2,5] * (rLambda_Costate[3,2] + rLambda_Costate[4,2] + rLambda_Costate[5,2])) + (rB_Mat[3,5] * (rLambda_Costate[3,3] + rLambda_Costate[4,3] + rLambda_Costate[5,3])) + (rB_Mat[4,5] * (rLambda_Costate[3,4] + rLambda_Costate[4,4] + rLambda_Costate[5,4])) + (rB_Mat[5,5] * (rLambda_Costate[3,5] + rLambda_Costate[4,5] + rLambda_Costate[5,5])) + (rB_Mat[6,5] * (rLambda_Costate[3,6] + rLambda_Costate[4,6] + rLambda_Costate[5,6])) + (rR_Diag[5] * rU_Opt_Seq[3,5]) + (rS_Diag[5] * (rU_Opt_Seq[3,5] - rU_Opt_Seq[2,5]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[3, 5] * rGrad_J[3, 5]);

(* Iteration 8 - Projected Gradient Step with Hard Box & Dynamic Slew Limits *)
rTemp_Val := rU_Opt_Seq[1, 1] - (rAlpha_PGD_StepSize * rGrad_J[1, 1]);
(* Slew limit against prior actuator output *)
IF rTemp_Val > (a_u_prev[1] + rDeltaU_Max[1]) THEN
    rTemp_Val := a_u_prev[1] + rDeltaU_Max[1];
ELSIF rTemp_Val < (a_u_prev[1] - rDeltaU_Max[1]) THEN
    rTemp_Val := a_u_prev[1] - rDeltaU_Max[1];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[1] THEN
    rTemp_Val := rU_BoxMax[1];
ELSIF rTemp_Val < rU_BoxMin[1] THEN
    rTemp_Val := rU_BoxMin[1];
END_IF;
rU_Opt_Seq[1, 1] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[1, 2] - (rAlpha_PGD_StepSize * rGrad_J[1, 2]);
(* Slew limit against prior actuator output *)
IF rTemp_Val > (a_u_prev[2] + rDeltaU_Max[2]) THEN
    rTemp_Val := a_u_prev[2] + rDeltaU_Max[2];
ELSIF rTemp_Val < (a_u_prev[2] - rDeltaU_Max[2]) THEN
    rTemp_Val := a_u_prev[2] - rDeltaU_Max[2];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[2] THEN
    rTemp_Val := rU_BoxMax[2];
ELSIF rTemp_Val < rU_BoxMin[2] THEN
    rTemp_Val := rU_BoxMin[2];
END_IF;
rU_Opt_Seq[1, 2] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[1, 3] - (rAlpha_PGD_StepSize * rGrad_J[1, 3]);
(* Slew limit against prior actuator output *)
IF rTemp_Val > (a_u_prev[3] + rDeltaU_Max[3]) THEN
    rTemp_Val := a_u_prev[3] + rDeltaU_Max[3];
ELSIF rTemp_Val < (a_u_prev[3] - rDeltaU_Max[3]) THEN
    rTemp_Val := a_u_prev[3] - rDeltaU_Max[3];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[3] THEN
    rTemp_Val := rU_BoxMax[3];
ELSIF rTemp_Val < rU_BoxMin[3] THEN
    rTemp_Val := rU_BoxMin[3];
END_IF;
rU_Opt_Seq[1, 3] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[1, 4] - (rAlpha_PGD_StepSize * rGrad_J[1, 4]);
(* Slew limit against prior actuator output *)
IF rTemp_Val > (a_u_prev[4] + rDeltaU_Max[4]) THEN
    rTemp_Val := a_u_prev[4] + rDeltaU_Max[4];
ELSIF rTemp_Val < (a_u_prev[4] - rDeltaU_Max[4]) THEN
    rTemp_Val := a_u_prev[4] - rDeltaU_Max[4];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[4] THEN
    rTemp_Val := rU_BoxMax[4];
ELSIF rTemp_Val < rU_BoxMin[4] THEN
    rTemp_Val := rU_BoxMin[4];
END_IF;
rU_Opt_Seq[1, 4] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[1, 5] - (rAlpha_PGD_StepSize * rGrad_J[1, 5]);
(* Slew limit against prior actuator output *)
IF rTemp_Val > (a_u_prev[5] + rDeltaU_Max[5]) THEN
    rTemp_Val := a_u_prev[5] + rDeltaU_Max[5];
ELSIF rTemp_Val < (a_u_prev[5] - rDeltaU_Max[5]) THEN
    rTemp_Val := a_u_prev[5] - rDeltaU_Max[5];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[5] THEN
    rTemp_Val := rU_BoxMax[5];
ELSIF rTemp_Val < rU_BoxMin[5] THEN
    rTemp_Val := rU_BoxMin[5];
END_IF;
rU_Opt_Seq[1, 5] := rTemp_Val;

rTemp_Val := rU_Opt_Seq[2, 1] - (rAlpha_PGD_StepSize * rGrad_J[2, 1]);
(* Slew limit against step 1 *)
IF rTemp_Val > (rU_Opt_Seq[1, 1] + rDeltaU_Max[1]) THEN
    rTemp_Val := rU_Opt_Seq[1, 1] + rDeltaU_Max[1];
ELSIF rTemp_Val < (rU_Opt_Seq[1, 1] - rDeltaU_Max[1]) THEN
    rTemp_Val := rU_Opt_Seq[1, 1] - rDeltaU_Max[1];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[1] THEN
    rTemp_Val := rU_BoxMax[1];
ELSIF rTemp_Val < rU_BoxMin[1] THEN
    rTemp_Val := rU_BoxMin[1];
END_IF;
rU_Opt_Seq[2, 1] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[2, 2] - (rAlpha_PGD_StepSize * rGrad_J[2, 2]);
(* Slew limit against step 1 *)
IF rTemp_Val > (rU_Opt_Seq[1, 2] + rDeltaU_Max[2]) THEN
    rTemp_Val := rU_Opt_Seq[1, 2] + rDeltaU_Max[2];
ELSIF rTemp_Val < (rU_Opt_Seq[1, 2] - rDeltaU_Max[2]) THEN
    rTemp_Val := rU_Opt_Seq[1, 2] - rDeltaU_Max[2];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[2] THEN
    rTemp_Val := rU_BoxMax[2];
ELSIF rTemp_Val < rU_BoxMin[2] THEN
    rTemp_Val := rU_BoxMin[2];
END_IF;
rU_Opt_Seq[2, 2] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[2, 3] - (rAlpha_PGD_StepSize * rGrad_J[2, 3]);
(* Slew limit against step 1 *)
IF rTemp_Val > (rU_Opt_Seq[1, 3] + rDeltaU_Max[3]) THEN
    rTemp_Val := rU_Opt_Seq[1, 3] + rDeltaU_Max[3];
ELSIF rTemp_Val < (rU_Opt_Seq[1, 3] - rDeltaU_Max[3]) THEN
    rTemp_Val := rU_Opt_Seq[1, 3] - rDeltaU_Max[3];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[3] THEN
    rTemp_Val := rU_BoxMax[3];
ELSIF rTemp_Val < rU_BoxMin[3] THEN
    rTemp_Val := rU_BoxMin[3];
END_IF;
rU_Opt_Seq[2, 3] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[2, 4] - (rAlpha_PGD_StepSize * rGrad_J[2, 4]);
(* Slew limit against step 1 *)
IF rTemp_Val > (rU_Opt_Seq[1, 4] + rDeltaU_Max[4]) THEN
    rTemp_Val := rU_Opt_Seq[1, 4] + rDeltaU_Max[4];
ELSIF rTemp_Val < (rU_Opt_Seq[1, 4] - rDeltaU_Max[4]) THEN
    rTemp_Val := rU_Opt_Seq[1, 4] - rDeltaU_Max[4];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[4] THEN
    rTemp_Val := rU_BoxMax[4];
ELSIF rTemp_Val < rU_BoxMin[4] THEN
    rTemp_Val := rU_BoxMin[4];
END_IF;
rU_Opt_Seq[2, 4] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[2, 5] - (rAlpha_PGD_StepSize * rGrad_J[2, 5]);
(* Slew limit against step 1 *)
IF rTemp_Val > (rU_Opt_Seq[1, 5] + rDeltaU_Max[5]) THEN
    rTemp_Val := rU_Opt_Seq[1, 5] + rDeltaU_Max[5];
ELSIF rTemp_Val < (rU_Opt_Seq[1, 5] - rDeltaU_Max[5]) THEN
    rTemp_Val := rU_Opt_Seq[1, 5] - rDeltaU_Max[5];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[5] THEN
    rTemp_Val := rU_BoxMax[5];
ELSIF rTemp_Val < rU_BoxMin[5] THEN
    rTemp_Val := rU_BoxMin[5];
END_IF;
rU_Opt_Seq[2, 5] := rTemp_Val;

rTemp_Val := rU_Opt_Seq[3, 1] - (rAlpha_PGD_StepSize * rGrad_J[3, 1]);
(* Slew limit against step 2 *)
IF rTemp_Val > (rU_Opt_Seq[2, 1] + rDeltaU_Max[1]) THEN
    rTemp_Val := rU_Opt_Seq[2, 1] + rDeltaU_Max[1];
ELSIF rTemp_Val < (rU_Opt_Seq[2, 1] - rDeltaU_Max[1]) THEN
    rTemp_Val := rU_Opt_Seq[2, 1] - rDeltaU_Max[1];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[1] THEN
    rTemp_Val := rU_BoxMax[1];
ELSIF rTemp_Val < rU_BoxMin[1] THEN
    rTemp_Val := rU_BoxMin[1];
END_IF;
rU_Opt_Seq[3, 1] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[3, 2] - (rAlpha_PGD_StepSize * rGrad_J[3, 2]);
(* Slew limit against step 2 *)
IF rTemp_Val > (rU_Opt_Seq[2, 2] + rDeltaU_Max[2]) THEN
    rTemp_Val := rU_Opt_Seq[2, 2] + rDeltaU_Max[2];
ELSIF rTemp_Val < (rU_Opt_Seq[2, 2] - rDeltaU_Max[2]) THEN
    rTemp_Val := rU_Opt_Seq[2, 2] - rDeltaU_Max[2];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[2] THEN
    rTemp_Val := rU_BoxMax[2];
ELSIF rTemp_Val < rU_BoxMin[2] THEN
    rTemp_Val := rU_BoxMin[2];
END_IF;
rU_Opt_Seq[3, 2] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[3, 3] - (rAlpha_PGD_StepSize * rGrad_J[3, 3]);
(* Slew limit against step 2 *)
IF rTemp_Val > (rU_Opt_Seq[2, 3] + rDeltaU_Max[3]) THEN
    rTemp_Val := rU_Opt_Seq[2, 3] + rDeltaU_Max[3];
ELSIF rTemp_Val < (rU_Opt_Seq[2, 3] - rDeltaU_Max[3]) THEN
    rTemp_Val := rU_Opt_Seq[2, 3] - rDeltaU_Max[3];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[3] THEN
    rTemp_Val := rU_BoxMax[3];
ELSIF rTemp_Val < rU_BoxMin[3] THEN
    rTemp_Val := rU_BoxMin[3];
END_IF;
rU_Opt_Seq[3, 3] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[3, 4] - (rAlpha_PGD_StepSize * rGrad_J[3, 4]);
(* Slew limit against step 2 *)
IF rTemp_Val > (rU_Opt_Seq[2, 4] + rDeltaU_Max[4]) THEN
    rTemp_Val := rU_Opt_Seq[2, 4] + rDeltaU_Max[4];
ELSIF rTemp_Val < (rU_Opt_Seq[2, 4] - rDeltaU_Max[4]) THEN
    rTemp_Val := rU_Opt_Seq[2, 4] - rDeltaU_Max[4];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[4] THEN
    rTemp_Val := rU_BoxMax[4];
ELSIF rTemp_Val < rU_BoxMin[4] THEN
    rTemp_Val := rU_BoxMin[4];
END_IF;
rU_Opt_Seq[3, 4] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[3, 5] - (rAlpha_PGD_StepSize * rGrad_J[3, 5]);
(* Slew limit against step 2 *)
IF rTemp_Val > (rU_Opt_Seq[2, 5] + rDeltaU_Max[5]) THEN
    rTemp_Val := rU_Opt_Seq[2, 5] + rDeltaU_Max[5];
ELSIF rTemp_Val < (rU_Opt_Seq[2, 5] - rDeltaU_Max[5]) THEN
    rTemp_Val := rU_Opt_Seq[2, 5] - rDeltaU_Max[5];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[5] THEN
    rTemp_Val := rU_BoxMax[5];
ELSIF rTemp_Val < rU_BoxMin[5] THEN
    rTemp_Val := rU_BoxMin[5];
END_IF;
rU_Opt_Seq[3, 5] := rTemp_Val;

(* ================================================================================================== *)
(* MPC PROJECTED GRADIENT DESCENT -- UNROLLED ITERATION 9 OF 10                                 *)
(* ================================================================================================== *)
iPGD_IterCount := 9;

(* Iteration 9 - Forward State Prediction Step 1 (h=1): x_1 = A * x_hat + B * u_1 *)
rX_Pred_Horizon[1, 1] := (rA_Mat[1,1] * a_x_hat[1]) + (rA_Mat[1,2] * a_x_hat[2]) + (rA_Mat[1,3] * a_x_hat[3]) + (rA_Mat[1,4] * a_x_hat[4]) + (rA_Mat[1,5] * a_x_hat[5]) + (rA_Mat[1,6] * a_x_hat[6]) + (rB_Mat[1,1] * rU_Opt_Seq[1,1]) + (rB_Mat[1,2] * rU_Opt_Seq[1,2]) + (rB_Mat[1,3] * rU_Opt_Seq[1,3]) + (rB_Mat[1,4] * rU_Opt_Seq[1,4]) + (rB_Mat[1,5] * rU_Opt_Seq[1,5]);
rX_Pred_Horizon[1, 2] := (rA_Mat[2,1] * a_x_hat[1]) + (rA_Mat[2,2] * a_x_hat[2]) + (rA_Mat[2,3] * a_x_hat[3]) + (rA_Mat[2,4] * a_x_hat[4]) + (rA_Mat[2,5] * a_x_hat[5]) + (rA_Mat[2,6] * a_x_hat[6]) + (rB_Mat[2,1] * rU_Opt_Seq[1,1]) + (rB_Mat[2,2] * rU_Opt_Seq[1,2]) + (rB_Mat[2,3] * rU_Opt_Seq[1,3]) + (rB_Mat[2,4] * rU_Opt_Seq[1,4]) + (rB_Mat[2,5] * rU_Opt_Seq[1,5]);
rX_Pred_Horizon[1, 3] := (rA_Mat[3,1] * a_x_hat[1]) + (rA_Mat[3,2] * a_x_hat[2]) + (rA_Mat[3,3] * a_x_hat[3]) + (rA_Mat[3,4] * a_x_hat[4]) + (rA_Mat[3,5] * a_x_hat[5]) + (rA_Mat[3,6] * a_x_hat[6]) + (rB_Mat[3,1] * rU_Opt_Seq[1,1]) + (rB_Mat[3,2] * rU_Opt_Seq[1,2]) + (rB_Mat[3,3] * rU_Opt_Seq[1,3]) + (rB_Mat[3,4] * rU_Opt_Seq[1,4]) + (rB_Mat[3,5] * rU_Opt_Seq[1,5]);
rX_Pred_Horizon[1, 4] := (rA_Mat[4,1] * a_x_hat[1]) + (rA_Mat[4,2] * a_x_hat[2]) + (rA_Mat[4,3] * a_x_hat[3]) + (rA_Mat[4,4] * a_x_hat[4]) + (rA_Mat[4,5] * a_x_hat[5]) + (rA_Mat[4,6] * a_x_hat[6]) + (rB_Mat[4,1] * rU_Opt_Seq[1,1]) + (rB_Mat[4,2] * rU_Opt_Seq[1,2]) + (rB_Mat[4,3] * rU_Opt_Seq[1,3]) + (rB_Mat[4,4] * rU_Opt_Seq[1,4]) + (rB_Mat[4,5] * rU_Opt_Seq[1,5]);
rX_Pred_Horizon[1, 5] := (rA_Mat[5,1] * a_x_hat[1]) + (rA_Mat[5,2] * a_x_hat[2]) + (rA_Mat[5,3] * a_x_hat[3]) + (rA_Mat[5,4] * a_x_hat[4]) + (rA_Mat[5,5] * a_x_hat[5]) + (rA_Mat[5,6] * a_x_hat[6]) + (rB_Mat[5,1] * rU_Opt_Seq[1,1]) + (rB_Mat[5,2] * rU_Opt_Seq[1,2]) + (rB_Mat[5,3] * rU_Opt_Seq[1,3]) + (rB_Mat[5,4] * rU_Opt_Seq[1,4]) + (rB_Mat[5,5] * rU_Opt_Seq[1,5]);
rX_Pred_Horizon[1, 6] := (rA_Mat[6,1] * a_x_hat[1]) + (rA_Mat[6,2] * a_x_hat[2]) + (rA_Mat[6,3] * a_x_hat[3]) + (rA_Mat[6,4] * a_x_hat[4]) + (rA_Mat[6,5] * a_x_hat[5]) + (rA_Mat[6,6] * a_x_hat[6]) + (rB_Mat[6,1] * rU_Opt_Seq[1,1]) + (rB_Mat[6,2] * rU_Opt_Seq[1,2]) + (rB_Mat[6,3] * rU_Opt_Seq[1,3]) + (rB_Mat[6,4] * rU_Opt_Seq[1,4]) + (rB_Mat[6,5] * rU_Opt_Seq[1,5]);

(* Iteration 9 - Forward State Prediction Step 2 (h=2): x_2 = A * x_1 + B * u_2 *)
rX_Pred_Horizon[2, 1] := (rA_Mat[1,1] * rX_Pred_Horizon[1,1]) + (rA_Mat[1,2] * rX_Pred_Horizon[1,2]) + (rA_Mat[1,3] * rX_Pred_Horizon[1,3]) + (rA_Mat[1,4] * rX_Pred_Horizon[1,4]) + (rA_Mat[1,5] * rX_Pred_Horizon[1,5]) + (rA_Mat[1,6] * rX_Pred_Horizon[1,6]) + (rB_Mat[1,1] * rU_Opt_Seq[2,1]) + (rB_Mat[1,2] * rU_Opt_Seq[2,2]) + (rB_Mat[1,3] * rU_Opt_Seq[2,3]) + (rB_Mat[1,4] * rU_Opt_Seq[2,4]) + (rB_Mat[1,5] * rU_Opt_Seq[2,5]);
rX_Pred_Horizon[2, 2] := (rA_Mat[2,1] * rX_Pred_Horizon[1,1]) + (rA_Mat[2,2] * rX_Pred_Horizon[1,2]) + (rA_Mat[2,3] * rX_Pred_Horizon[1,3]) + (rA_Mat[2,4] * rX_Pred_Horizon[1,4]) + (rA_Mat[2,5] * rX_Pred_Horizon[1,5]) + (rA_Mat[2,6] * rX_Pred_Horizon[1,6]) + (rB_Mat[2,1] * rU_Opt_Seq[2,1]) + (rB_Mat[2,2] * rU_Opt_Seq[2,2]) + (rB_Mat[2,3] * rU_Opt_Seq[2,3]) + (rB_Mat[2,4] * rU_Opt_Seq[2,4]) + (rB_Mat[2,5] * rU_Opt_Seq[2,5]);
rX_Pred_Horizon[2, 3] := (rA_Mat[3,1] * rX_Pred_Horizon[1,1]) + (rA_Mat[3,2] * rX_Pred_Horizon[1,2]) + (rA_Mat[3,3] * rX_Pred_Horizon[1,3]) + (rA_Mat[3,4] * rX_Pred_Horizon[1,4]) + (rA_Mat[3,5] * rX_Pred_Horizon[1,5]) + (rA_Mat[3,6] * rX_Pred_Horizon[1,6]) + (rB_Mat[3,1] * rU_Opt_Seq[2,1]) + (rB_Mat[3,2] * rU_Opt_Seq[2,2]) + (rB_Mat[3,3] * rU_Opt_Seq[2,3]) + (rB_Mat[3,4] * rU_Opt_Seq[2,4]) + (rB_Mat[3,5] * rU_Opt_Seq[2,5]);
rX_Pred_Horizon[2, 4] := (rA_Mat[4,1] * rX_Pred_Horizon[1,1]) + (rA_Mat[4,2] * rX_Pred_Horizon[1,2]) + (rA_Mat[4,3] * rX_Pred_Horizon[1,3]) + (rA_Mat[4,4] * rX_Pred_Horizon[1,4]) + (rA_Mat[4,5] * rX_Pred_Horizon[1,5]) + (rA_Mat[4,6] * rX_Pred_Horizon[1,6]) + (rB_Mat[4,1] * rU_Opt_Seq[2,1]) + (rB_Mat[4,2] * rU_Opt_Seq[2,2]) + (rB_Mat[4,3] * rU_Opt_Seq[2,3]) + (rB_Mat[4,4] * rU_Opt_Seq[2,4]) + (rB_Mat[4,5] * rU_Opt_Seq[2,5]);
rX_Pred_Horizon[2, 5] := (rA_Mat[5,1] * rX_Pred_Horizon[1,1]) + (rA_Mat[5,2] * rX_Pred_Horizon[1,2]) + (rA_Mat[5,3] * rX_Pred_Horizon[1,3]) + (rA_Mat[5,4] * rX_Pred_Horizon[1,4]) + (rA_Mat[5,5] * rX_Pred_Horizon[1,5]) + (rA_Mat[5,6] * rX_Pred_Horizon[1,6]) + (rB_Mat[5,1] * rU_Opt_Seq[2,1]) + (rB_Mat[5,2] * rU_Opt_Seq[2,2]) + (rB_Mat[5,3] * rU_Opt_Seq[2,3]) + (rB_Mat[5,4] * rU_Opt_Seq[2,4]) + (rB_Mat[5,5] * rU_Opt_Seq[2,5]);
rX_Pred_Horizon[2, 6] := (rA_Mat[6,1] * rX_Pred_Horizon[1,1]) + (rA_Mat[6,2] * rX_Pred_Horizon[1,2]) + (rA_Mat[6,3] * rX_Pred_Horizon[1,3]) + (rA_Mat[6,4] * rX_Pred_Horizon[1,4]) + (rA_Mat[6,5] * rX_Pred_Horizon[1,5]) + (rA_Mat[6,6] * rX_Pred_Horizon[1,6]) + (rB_Mat[6,1] * rU_Opt_Seq[2,1]) + (rB_Mat[6,2] * rU_Opt_Seq[2,2]) + (rB_Mat[6,3] * rU_Opt_Seq[2,3]) + (rB_Mat[6,4] * rU_Opt_Seq[2,4]) + (rB_Mat[6,5] * rU_Opt_Seq[2,5]);

(* Iteration 9 - Forward State Prediction Step 3 (h=3): x_3 = A * x_2 + B * u_3 *)
rX_Pred_Horizon[3, 1] := (rA_Mat[1,1] * rX_Pred_Horizon[2,1]) + (rA_Mat[1,2] * rX_Pred_Horizon[2,2]) + (rA_Mat[1,3] * rX_Pred_Horizon[2,3]) + (rA_Mat[1,4] * rX_Pred_Horizon[2,4]) + (rA_Mat[1,5] * rX_Pred_Horizon[2,5]) + (rA_Mat[1,6] * rX_Pred_Horizon[2,6]) + (rB_Mat[1,1] * rU_Opt_Seq[3,1]) + (rB_Mat[1,2] * rU_Opt_Seq[3,2]) + (rB_Mat[1,3] * rU_Opt_Seq[3,3]) + (rB_Mat[1,4] * rU_Opt_Seq[3,4]) + (rB_Mat[1,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[3, 2] := (rA_Mat[2,1] * rX_Pred_Horizon[2,1]) + (rA_Mat[2,2] * rX_Pred_Horizon[2,2]) + (rA_Mat[2,3] * rX_Pred_Horizon[2,3]) + (rA_Mat[2,4] * rX_Pred_Horizon[2,4]) + (rA_Mat[2,5] * rX_Pred_Horizon[2,5]) + (rA_Mat[2,6] * rX_Pred_Horizon[2,6]) + (rB_Mat[2,1] * rU_Opt_Seq[3,1]) + (rB_Mat[2,2] * rU_Opt_Seq[3,2]) + (rB_Mat[2,3] * rU_Opt_Seq[3,3]) + (rB_Mat[2,4] * rU_Opt_Seq[3,4]) + (rB_Mat[2,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[3, 3] := (rA_Mat[3,1] * rX_Pred_Horizon[2,1]) + (rA_Mat[3,2] * rX_Pred_Horizon[2,2]) + (rA_Mat[3,3] * rX_Pred_Horizon[2,3]) + (rA_Mat[3,4] * rX_Pred_Horizon[2,4]) + (rA_Mat[3,5] * rX_Pred_Horizon[2,5]) + (rA_Mat[3,6] * rX_Pred_Horizon[2,6]) + (rB_Mat[3,1] * rU_Opt_Seq[3,1]) + (rB_Mat[3,2] * rU_Opt_Seq[3,2]) + (rB_Mat[3,3] * rU_Opt_Seq[3,3]) + (rB_Mat[3,4] * rU_Opt_Seq[3,4]) + (rB_Mat[3,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[3, 4] := (rA_Mat[4,1] * rX_Pred_Horizon[2,1]) + (rA_Mat[4,2] * rX_Pred_Horizon[2,2]) + (rA_Mat[4,3] * rX_Pred_Horizon[2,3]) + (rA_Mat[4,4] * rX_Pred_Horizon[2,4]) + (rA_Mat[4,5] * rX_Pred_Horizon[2,5]) + (rA_Mat[4,6] * rX_Pred_Horizon[2,6]) + (rB_Mat[4,1] * rU_Opt_Seq[3,1]) + (rB_Mat[4,2] * rU_Opt_Seq[3,2]) + (rB_Mat[4,3] * rU_Opt_Seq[3,3]) + (rB_Mat[4,4] * rU_Opt_Seq[3,4]) + (rB_Mat[4,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[3, 5] := (rA_Mat[5,1] * rX_Pred_Horizon[2,1]) + (rA_Mat[5,2] * rX_Pred_Horizon[2,2]) + (rA_Mat[5,3] * rX_Pred_Horizon[2,3]) + (rA_Mat[5,4] * rX_Pred_Horizon[2,4]) + (rA_Mat[5,5] * rX_Pred_Horizon[2,5]) + (rA_Mat[5,6] * rX_Pred_Horizon[2,6]) + (rB_Mat[5,1] * rU_Opt_Seq[3,1]) + (rB_Mat[5,2] * rU_Opt_Seq[3,2]) + (rB_Mat[5,3] * rU_Opt_Seq[3,3]) + (rB_Mat[5,4] * rU_Opt_Seq[3,4]) + (rB_Mat[5,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[3, 6] := (rA_Mat[6,1] * rX_Pred_Horizon[2,1]) + (rA_Mat[6,2] * rX_Pred_Horizon[2,2]) + (rA_Mat[6,3] * rX_Pred_Horizon[2,3]) + (rA_Mat[6,4] * rX_Pred_Horizon[2,4]) + (rA_Mat[6,5] * rX_Pred_Horizon[2,5]) + (rA_Mat[6,6] * rX_Pred_Horizon[2,6]) + (rB_Mat[6,1] * rU_Opt_Seq[3,1]) + (rB_Mat[6,2] * rU_Opt_Seq[3,2]) + (rB_Mat[6,3] * rU_Opt_Seq[3,3]) + (rB_Mat[6,4] * rU_Opt_Seq[3,4]) + (rB_Mat[6,5] * rU_Opt_Seq[3,5]);

(* Iteration 9 - Forward State Prediction Step 4 (h=4): x_4 = A * x_3 + B * u_3 (held beyond Hu) *)
rX_Pred_Horizon[4, 1] := (rA_Mat[1,1] * rX_Pred_Horizon[3,1]) + (rA_Mat[1,2] * rX_Pred_Horizon[3,2]) + (rA_Mat[1,3] * rX_Pred_Horizon[3,3]) + (rA_Mat[1,4] * rX_Pred_Horizon[3,4]) + (rA_Mat[1,5] * rX_Pred_Horizon[3,5]) + (rA_Mat[1,6] * rX_Pred_Horizon[3,6]) + (rB_Mat[1,1] * rU_Opt_Seq[3,1]) + (rB_Mat[1,2] * rU_Opt_Seq[3,2]) + (rB_Mat[1,3] * rU_Opt_Seq[3,3]) + (rB_Mat[1,4] * rU_Opt_Seq[3,4]) + (rB_Mat[1,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[4, 2] := (rA_Mat[2,1] * rX_Pred_Horizon[3,1]) + (rA_Mat[2,2] * rX_Pred_Horizon[3,2]) + (rA_Mat[2,3] * rX_Pred_Horizon[3,3]) + (rA_Mat[2,4] * rX_Pred_Horizon[3,4]) + (rA_Mat[2,5] * rX_Pred_Horizon[3,5]) + (rA_Mat[2,6] * rX_Pred_Horizon[3,6]) + (rB_Mat[2,1] * rU_Opt_Seq[3,1]) + (rB_Mat[2,2] * rU_Opt_Seq[3,2]) + (rB_Mat[2,3] * rU_Opt_Seq[3,3]) + (rB_Mat[2,4] * rU_Opt_Seq[3,4]) + (rB_Mat[2,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[4, 3] := (rA_Mat[3,1] * rX_Pred_Horizon[3,1]) + (rA_Mat[3,2] * rX_Pred_Horizon[3,2]) + (rA_Mat[3,3] * rX_Pred_Horizon[3,3]) + (rA_Mat[3,4] * rX_Pred_Horizon[3,4]) + (rA_Mat[3,5] * rX_Pred_Horizon[3,5]) + (rA_Mat[3,6] * rX_Pred_Horizon[3,6]) + (rB_Mat[3,1] * rU_Opt_Seq[3,1]) + (rB_Mat[3,2] * rU_Opt_Seq[3,2]) + (rB_Mat[3,3] * rU_Opt_Seq[3,3]) + (rB_Mat[3,4] * rU_Opt_Seq[3,4]) + (rB_Mat[3,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[4, 4] := (rA_Mat[4,1] * rX_Pred_Horizon[3,1]) + (rA_Mat[4,2] * rX_Pred_Horizon[3,2]) + (rA_Mat[4,3] * rX_Pred_Horizon[3,3]) + (rA_Mat[4,4] * rX_Pred_Horizon[3,4]) + (rA_Mat[4,5] * rX_Pred_Horizon[3,5]) + (rA_Mat[4,6] * rX_Pred_Horizon[3,6]) + (rB_Mat[4,1] * rU_Opt_Seq[3,1]) + (rB_Mat[4,2] * rU_Opt_Seq[3,2]) + (rB_Mat[4,3] * rU_Opt_Seq[3,3]) + (rB_Mat[4,4] * rU_Opt_Seq[3,4]) + (rB_Mat[4,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[4, 5] := (rA_Mat[5,1] * rX_Pred_Horizon[3,1]) + (rA_Mat[5,2] * rX_Pred_Horizon[3,2]) + (rA_Mat[5,3] * rX_Pred_Horizon[3,3]) + (rA_Mat[5,4] * rX_Pred_Horizon[3,4]) + (rA_Mat[5,5] * rX_Pred_Horizon[3,5]) + (rA_Mat[5,6] * rX_Pred_Horizon[3,6]) + (rB_Mat[5,1] * rU_Opt_Seq[3,1]) + (rB_Mat[5,2] * rU_Opt_Seq[3,2]) + (rB_Mat[5,3] * rU_Opt_Seq[3,3]) + (rB_Mat[5,4] * rU_Opt_Seq[3,4]) + (rB_Mat[5,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[4, 6] := (rA_Mat[6,1] * rX_Pred_Horizon[3,1]) + (rA_Mat[6,2] * rX_Pred_Horizon[3,2]) + (rA_Mat[6,3] * rX_Pred_Horizon[3,3]) + (rA_Mat[6,4] * rX_Pred_Horizon[3,4]) + (rA_Mat[6,5] * rX_Pred_Horizon[3,5]) + (rA_Mat[6,6] * rX_Pred_Horizon[3,6]) + (rB_Mat[6,1] * rU_Opt_Seq[3,1]) + (rB_Mat[6,2] * rU_Opt_Seq[3,2]) + (rB_Mat[6,3] * rU_Opt_Seq[3,3]) + (rB_Mat[6,4] * rU_Opt_Seq[3,4]) + (rB_Mat[6,5] * rU_Opt_Seq[3,5]);

(* Iteration 9 - Forward State Prediction Step 5 (h=5): x_5 = A * x_4 + B * u_3 (held beyond Hu) *)
rX_Pred_Horizon[5, 1] := (rA_Mat[1,1] * rX_Pred_Horizon[4,1]) + (rA_Mat[1,2] * rX_Pred_Horizon[4,2]) + (rA_Mat[1,3] * rX_Pred_Horizon[4,3]) + (rA_Mat[1,4] * rX_Pred_Horizon[4,4]) + (rA_Mat[1,5] * rX_Pred_Horizon[4,5]) + (rA_Mat[1,6] * rX_Pred_Horizon[4,6]) + (rB_Mat[1,1] * rU_Opt_Seq[3,1]) + (rB_Mat[1,2] * rU_Opt_Seq[3,2]) + (rB_Mat[1,3] * rU_Opt_Seq[3,3]) + (rB_Mat[1,4] * rU_Opt_Seq[3,4]) + (rB_Mat[1,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[5, 2] := (rA_Mat[2,1] * rX_Pred_Horizon[4,1]) + (rA_Mat[2,2] * rX_Pred_Horizon[4,2]) + (rA_Mat[2,3] * rX_Pred_Horizon[4,3]) + (rA_Mat[2,4] * rX_Pred_Horizon[4,4]) + (rA_Mat[2,5] * rX_Pred_Horizon[4,5]) + (rA_Mat[2,6] * rX_Pred_Horizon[4,6]) + (rB_Mat[2,1] * rU_Opt_Seq[3,1]) + (rB_Mat[2,2] * rU_Opt_Seq[3,2]) + (rB_Mat[2,3] * rU_Opt_Seq[3,3]) + (rB_Mat[2,4] * rU_Opt_Seq[3,4]) + (rB_Mat[2,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[5, 3] := (rA_Mat[3,1] * rX_Pred_Horizon[4,1]) + (rA_Mat[3,2] * rX_Pred_Horizon[4,2]) + (rA_Mat[3,3] * rX_Pred_Horizon[4,3]) + (rA_Mat[3,4] * rX_Pred_Horizon[4,4]) + (rA_Mat[3,5] * rX_Pred_Horizon[4,5]) + (rA_Mat[3,6] * rX_Pred_Horizon[4,6]) + (rB_Mat[3,1] * rU_Opt_Seq[3,1]) + (rB_Mat[3,2] * rU_Opt_Seq[3,2]) + (rB_Mat[3,3] * rU_Opt_Seq[3,3]) + (rB_Mat[3,4] * rU_Opt_Seq[3,4]) + (rB_Mat[3,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[5, 4] := (rA_Mat[4,1] * rX_Pred_Horizon[4,1]) + (rA_Mat[4,2] * rX_Pred_Horizon[4,2]) + (rA_Mat[4,3] * rX_Pred_Horizon[4,3]) + (rA_Mat[4,4] * rX_Pred_Horizon[4,4]) + (rA_Mat[4,5] * rX_Pred_Horizon[4,5]) + (rA_Mat[4,6] * rX_Pred_Horizon[4,6]) + (rB_Mat[4,1] * rU_Opt_Seq[3,1]) + (rB_Mat[4,2] * rU_Opt_Seq[3,2]) + (rB_Mat[4,3] * rU_Opt_Seq[3,3]) + (rB_Mat[4,4] * rU_Opt_Seq[3,4]) + (rB_Mat[4,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[5, 5] := (rA_Mat[5,1] * rX_Pred_Horizon[4,1]) + (rA_Mat[5,2] * rX_Pred_Horizon[4,2]) + (rA_Mat[5,3] * rX_Pred_Horizon[4,3]) + (rA_Mat[5,4] * rX_Pred_Horizon[4,4]) + (rA_Mat[5,5] * rX_Pred_Horizon[4,5]) + (rA_Mat[5,6] * rX_Pred_Horizon[4,6]) + (rB_Mat[5,1] * rU_Opt_Seq[3,1]) + (rB_Mat[5,2] * rU_Opt_Seq[3,2]) + (rB_Mat[5,3] * rU_Opt_Seq[3,3]) + (rB_Mat[5,4] * rU_Opt_Seq[3,4]) + (rB_Mat[5,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[5, 6] := (rA_Mat[6,1] * rX_Pred_Horizon[4,1]) + (rA_Mat[6,2] * rX_Pred_Horizon[4,2]) + (rA_Mat[6,3] * rX_Pred_Horizon[4,3]) + (rA_Mat[6,4] * rX_Pred_Horizon[4,4]) + (rA_Mat[6,5] * rX_Pred_Horizon[4,5]) + (rA_Mat[6,6] * rX_Pred_Horizon[4,6]) + (rB_Mat[6,1] * rU_Opt_Seq[3,1]) + (rB_Mat[6,2] * rU_Opt_Seq[3,2]) + (rB_Mat[6,3] * rU_Opt_Seq[3,3]) + (rB_Mat[6,4] * rU_Opt_Seq[3,4]) + (rB_Mat[6,5] * rU_Opt_Seq[3,5]);

(* Iteration 9 - Evaluate Objective Function Cost J *)
rMPC_Cost_J := 0.0;
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[1] * (rX_Pred_Horizon[1,1] - rX_Target[1,1]) * (rX_Pred_Horizon[1,1] - rX_Target[1,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[2] * (rX_Pred_Horizon[1,2] - rX_Target[1,2]) * (rX_Pred_Horizon[1,2] - rX_Target[1,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[3] * (rX_Pred_Horizon[1,3] - rX_Target[1,3]) * (rX_Pred_Horizon[1,3] - rX_Target[1,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[4] * (rX_Pred_Horizon[1,4] - rX_Target[1,4]) * (rX_Pred_Horizon[1,4] - rX_Target[1,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[5] * (rX_Pred_Horizon[1,5] - rX_Target[1,5]) * (rX_Pred_Horizon[1,5] - rX_Target[1,5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[6] * (rX_Pred_Horizon[1,6] - rX_Target[1,6]) * (rX_Pred_Horizon[1,6] - rX_Target[1,6]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[1] * (rX_Pred_Horizon[2,1] - rX_Target[2,1]) * (rX_Pred_Horizon[2,1] - rX_Target[2,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[2] * (rX_Pred_Horizon[2,2] - rX_Target[2,2]) * (rX_Pred_Horizon[2,2] - rX_Target[2,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[3] * (rX_Pred_Horizon[2,3] - rX_Target[2,3]) * (rX_Pred_Horizon[2,3] - rX_Target[2,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[4] * (rX_Pred_Horizon[2,4] - rX_Target[2,4]) * (rX_Pred_Horizon[2,4] - rX_Target[2,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[5] * (rX_Pred_Horizon[2,5] - rX_Target[2,5]) * (rX_Pred_Horizon[2,5] - rX_Target[2,5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[6] * (rX_Pred_Horizon[2,6] - rX_Target[2,6]) * (rX_Pred_Horizon[2,6] - rX_Target[2,6]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[1] * (rX_Pred_Horizon[3,1] - rX_Target[3,1]) * (rX_Pred_Horizon[3,1] - rX_Target[3,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[2] * (rX_Pred_Horizon[3,2] - rX_Target[3,2]) * (rX_Pred_Horizon[3,2] - rX_Target[3,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[3] * (rX_Pred_Horizon[3,3] - rX_Target[3,3]) * (rX_Pred_Horizon[3,3] - rX_Target[3,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[4] * (rX_Pred_Horizon[3,4] - rX_Target[3,4]) * (rX_Pred_Horizon[3,4] - rX_Target[3,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[5] * (rX_Pred_Horizon[3,5] - rX_Target[3,5]) * (rX_Pred_Horizon[3,5] - rX_Target[3,5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[6] * (rX_Pred_Horizon[3,6] - rX_Target[3,6]) * (rX_Pred_Horizon[3,6] - rX_Target[3,6]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[1] * (rX_Pred_Horizon[4,1] - rX_Target[4,1]) * (rX_Pred_Horizon[4,1] - rX_Target[4,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[2] * (rX_Pred_Horizon[4,2] - rX_Target[4,2]) * (rX_Pred_Horizon[4,2] - rX_Target[4,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[3] * (rX_Pred_Horizon[4,3] - rX_Target[4,3]) * (rX_Pred_Horizon[4,3] - rX_Target[4,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[4] * (rX_Pred_Horizon[4,4] - rX_Target[4,4]) * (rX_Pred_Horizon[4,4] - rX_Target[4,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[5] * (rX_Pred_Horizon[4,5] - rX_Target[4,5]) * (rX_Pred_Horizon[4,5] - rX_Target[4,5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[6] * (rX_Pred_Horizon[4,6] - rX_Target[4,6]) * (rX_Pred_Horizon[4,6] - rX_Target[4,6]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[1] * (rX_Pred_Horizon[5,1] - rX_Target[5,1]) * (rX_Pred_Horizon[5,1] - rX_Target[5,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[2] * (rX_Pred_Horizon[5,2] - rX_Target[5,2]) * (rX_Pred_Horizon[5,2] - rX_Target[5,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[3] * (rX_Pred_Horizon[5,3] - rX_Target[5,3]) * (rX_Pred_Horizon[5,3] - rX_Target[5,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[4] * (rX_Pred_Horizon[5,4] - rX_Target[5,4]) * (rX_Pred_Horizon[5,4] - rX_Target[5,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[5] * (rX_Pred_Horizon[5,5] - rX_Target[5,5]) * (rX_Pred_Horizon[5,5] - rX_Target[5,5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[6] * (rX_Pred_Horizon[5,6] - rX_Target[5,6]) * (rX_Pred_Horizon[5,6] - rX_Target[5,6]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rP_Diag[1] * (rX_Pred_Horizon[5,1] - rX_Target[5,1]) * (rX_Pred_Horizon[5,1] - rX_Target[5,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rP_Diag[2] * (rX_Pred_Horizon[5,2] - rX_Target[5,2]) * (rX_Pred_Horizon[5,2] - rX_Target[5,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rP_Diag[3] * (rX_Pred_Horizon[5,3] - rX_Target[5,3]) * (rX_Pred_Horizon[5,3] - rX_Target[5,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rP_Diag[4] * (rX_Pred_Horizon[5,4] - rX_Target[5,4]) * (rX_Pred_Horizon[5,4] - rX_Target[5,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rP_Diag[5] * (rX_Pred_Horizon[5,5] - rX_Target[5,5]) * (rX_Pred_Horizon[5,5] - rX_Target[5,5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rP_Diag[6] * (rX_Pred_Horizon[5,6] - rX_Target[5,6]) * (rX_Pred_Horizon[5,6] - rX_Target[5,6]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[1] * rU_Opt_Seq[1,1] * rU_Opt_Seq[1,1]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[2] * rU_Opt_Seq[1,2] * rU_Opt_Seq[1,2]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[3] * rU_Opt_Seq[1,3] * rU_Opt_Seq[1,3]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[4] * rU_Opt_Seq[1,4] * rU_Opt_Seq[1,4]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[5] * rU_Opt_Seq[1,5] * rU_Opt_Seq[1,5]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[1] * rU_Opt_Seq[2,1] * rU_Opt_Seq[2,1]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[2] * rU_Opt_Seq[2,2] * rU_Opt_Seq[2,2]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[3] * rU_Opt_Seq[2,3] * rU_Opt_Seq[2,3]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[4] * rU_Opt_Seq[2,4] * rU_Opt_Seq[2,4]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[5] * rU_Opt_Seq[2,5] * rU_Opt_Seq[2,5]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[1] * rU_Opt_Seq[3,1] * rU_Opt_Seq[3,1]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[2] * rU_Opt_Seq[3,2] * rU_Opt_Seq[3,2]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[3] * rU_Opt_Seq[3,3] * rU_Opt_Seq[3,3]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[4] * rU_Opt_Seq[3,4] * rU_Opt_Seq[3,4]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[5] * rU_Opt_Seq[3,5] * rU_Opt_Seq[3,5]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[1] * (rU_Opt_Seq[1,1] - a_u_prev[1]) * (rU_Opt_Seq[1,1] - a_u_prev[1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[1] * (rU_Opt_Seq[2,1] - rU_Opt_Seq[1,1]) * (rU_Opt_Seq[2,1] - rU_Opt_Seq[1,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[1] * (rU_Opt_Seq[3,1] - rU_Opt_Seq[2,1]) * (rU_Opt_Seq[3,1] - rU_Opt_Seq[2,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[2] * (rU_Opt_Seq[1,2] - a_u_prev[2]) * (rU_Opt_Seq[1,2] - a_u_prev[2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[2] * (rU_Opt_Seq[2,2] - rU_Opt_Seq[1,2]) * (rU_Opt_Seq[2,2] - rU_Opt_Seq[1,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[2] * (rU_Opt_Seq[3,2] - rU_Opt_Seq[2,2]) * (rU_Opt_Seq[3,2] - rU_Opt_Seq[2,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[3] * (rU_Opt_Seq[1,3] - a_u_prev[3]) * (rU_Opt_Seq[1,3] - a_u_prev[3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[3] * (rU_Opt_Seq[2,3] - rU_Opt_Seq[1,3]) * (rU_Opt_Seq[2,3] - rU_Opt_Seq[1,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[3] * (rU_Opt_Seq[3,3] - rU_Opt_Seq[2,3]) * (rU_Opt_Seq[3,3] - rU_Opt_Seq[2,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[4] * (rU_Opt_Seq[1,4] - a_u_prev[4]) * (rU_Opt_Seq[1,4] - a_u_prev[4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[4] * (rU_Opt_Seq[2,4] - rU_Opt_Seq[1,4]) * (rU_Opt_Seq[2,4] - rU_Opt_Seq[1,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[4] * (rU_Opt_Seq[3,4] - rU_Opt_Seq[2,4]) * (rU_Opt_Seq[3,4] - rU_Opt_Seq[2,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[5] * (rU_Opt_Seq[1,5] - a_u_prev[5]) * (rU_Opt_Seq[1,5] - a_u_prev[5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[5] * (rU_Opt_Seq[2,5] - rU_Opt_Seq[1,5]) * (rU_Opt_Seq[2,5] - rU_Opt_Seq[1,5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[5] * (rU_Opt_Seq[3,5] - rU_Opt_Seq[2,5]) * (rU_Opt_Seq[3,5] - rU_Opt_Seq[2,5]));

(* Iteration 9 - Backward Adjoint Costate Propagation: lambda_h = A^T * lambda_{h+1} + Q * (x_h - x_ref) *)
(* Terminal Costate at h=5: lambda_5 = (P + Q) * (x_5 - x_target_5) *)
rLambda_Costate[5, 1] := (rP_Diag[1] + rQ_Diag[1]) * (rX_Pred_Horizon[5,1] - rX_Target[5,1]);
rLambda_Costate[5, 2] := (rP_Diag[2] + rQ_Diag[2]) * (rX_Pred_Horizon[5,2] - rX_Target[5,2]);
rLambda_Costate[5, 3] := (rP_Diag[3] + rQ_Diag[3]) * (rX_Pred_Horizon[5,3] - rX_Target[5,3]);
rLambda_Costate[5, 4] := (rP_Diag[4] + rQ_Diag[4]) * (rX_Pred_Horizon[5,4] - rX_Target[5,4]);
rLambda_Costate[5, 5] := (rP_Diag[5] + rQ_Diag[5]) * (rX_Pred_Horizon[5,5] - rX_Target[5,5]);
rLambda_Costate[5, 6] := (rP_Diag[6] + rQ_Diag[6]) * (rX_Pred_Horizon[5,6] - rX_Target[5,6]);

(* Adjoint Costate at h=4: lambda_4 = A^T * lambda_5 + Q * (x_4 - x_target_4) *)
rLambda_Costate[4, 1] := (rA_Mat[1,1] * rLambda_Costate[5,1]) + (rA_Mat[2,1] * rLambda_Costate[5,2]) + (rA_Mat[3,1] * rLambda_Costate[5,3]) + (rA_Mat[4,1] * rLambda_Costate[5,4]) + (rA_Mat[5,1] * rLambda_Costate[5,5]) + (rA_Mat[6,1] * rLambda_Costate[5,6]) + (rQ_Diag[1] * (rX_Pred_Horizon[4,1] - rX_Target[4,1]));
rLambda_Costate[4, 2] := (rA_Mat[1,2] * rLambda_Costate[5,1]) + (rA_Mat[2,2] * rLambda_Costate[5,2]) + (rA_Mat[3,2] * rLambda_Costate[5,3]) + (rA_Mat[4,2] * rLambda_Costate[5,4]) + (rA_Mat[5,2] * rLambda_Costate[5,5]) + (rA_Mat[6,2] * rLambda_Costate[5,6]) + (rQ_Diag[2] * (rX_Pred_Horizon[4,2] - rX_Target[4,2]));
rLambda_Costate[4, 3] := (rA_Mat[1,3] * rLambda_Costate[5,1]) + (rA_Mat[2,3] * rLambda_Costate[5,2]) + (rA_Mat[3,3] * rLambda_Costate[5,3]) + (rA_Mat[4,3] * rLambda_Costate[5,4]) + (rA_Mat[5,3] * rLambda_Costate[5,5]) + (rA_Mat[6,3] * rLambda_Costate[5,6]) + (rQ_Diag[3] * (rX_Pred_Horizon[4,3] - rX_Target[4,3]));
rLambda_Costate[4, 4] := (rA_Mat[1,4] * rLambda_Costate[5,1]) + (rA_Mat[2,4] * rLambda_Costate[5,2]) + (rA_Mat[3,4] * rLambda_Costate[5,3]) + (rA_Mat[4,4] * rLambda_Costate[5,4]) + (rA_Mat[5,4] * rLambda_Costate[5,5]) + (rA_Mat[6,4] * rLambda_Costate[5,6]) + (rQ_Diag[4] * (rX_Pred_Horizon[4,4] - rX_Target[4,4]));
rLambda_Costate[4, 5] := (rA_Mat[1,5] * rLambda_Costate[5,1]) + (rA_Mat[2,5] * rLambda_Costate[5,2]) + (rA_Mat[3,5] * rLambda_Costate[5,3]) + (rA_Mat[4,5] * rLambda_Costate[5,4]) + (rA_Mat[5,5] * rLambda_Costate[5,5]) + (rA_Mat[6,5] * rLambda_Costate[5,6]) + (rQ_Diag[5] * (rX_Pred_Horizon[4,5] - rX_Target[4,5]));
rLambda_Costate[4, 6] := (rA_Mat[1,6] * rLambda_Costate[5,1]) + (rA_Mat[2,6] * rLambda_Costate[5,2]) + (rA_Mat[3,6] * rLambda_Costate[5,3]) + (rA_Mat[4,6] * rLambda_Costate[5,4]) + (rA_Mat[5,6] * rLambda_Costate[5,5]) + (rA_Mat[6,6] * rLambda_Costate[5,6]) + (rQ_Diag[6] * (rX_Pred_Horizon[4,6] - rX_Target[4,6]));

(* Adjoint Costate at h=3: lambda_3 = A^T * lambda_4 + Q * (x_3 - x_target_3) *)
rLambda_Costate[3, 1] := (rA_Mat[1,1] * rLambda_Costate[4,1]) + (rA_Mat[2,1] * rLambda_Costate[4,2]) + (rA_Mat[3,1] * rLambda_Costate[4,3]) + (rA_Mat[4,1] * rLambda_Costate[4,4]) + (rA_Mat[5,1] * rLambda_Costate[4,5]) + (rA_Mat[6,1] * rLambda_Costate[4,6]) + (rQ_Diag[1] * (rX_Pred_Horizon[3,1] - rX_Target[3,1]));
rLambda_Costate[3, 2] := (rA_Mat[1,2] * rLambda_Costate[4,1]) + (rA_Mat[2,2] * rLambda_Costate[4,2]) + (rA_Mat[3,2] * rLambda_Costate[4,3]) + (rA_Mat[4,2] * rLambda_Costate[4,4]) + (rA_Mat[5,2] * rLambda_Costate[4,5]) + (rA_Mat[6,2] * rLambda_Costate[4,6]) + (rQ_Diag[2] * (rX_Pred_Horizon[3,2] - rX_Target[3,2]));
rLambda_Costate[3, 3] := (rA_Mat[1,3] * rLambda_Costate[4,1]) + (rA_Mat[2,3] * rLambda_Costate[4,2]) + (rA_Mat[3,3] * rLambda_Costate[4,3]) + (rA_Mat[4,3] * rLambda_Costate[4,4]) + (rA_Mat[5,3] * rLambda_Costate[4,5]) + (rA_Mat[6,3] * rLambda_Costate[4,6]) + (rQ_Diag[3] * (rX_Pred_Horizon[3,3] - rX_Target[3,3]));
rLambda_Costate[3, 4] := (rA_Mat[1,4] * rLambda_Costate[4,1]) + (rA_Mat[2,4] * rLambda_Costate[4,2]) + (rA_Mat[3,4] * rLambda_Costate[4,3]) + (rA_Mat[4,4] * rLambda_Costate[4,4]) + (rA_Mat[5,4] * rLambda_Costate[4,5]) + (rA_Mat[6,4] * rLambda_Costate[4,6]) + (rQ_Diag[4] * (rX_Pred_Horizon[3,4] - rX_Target[3,4]));
rLambda_Costate[3, 5] := (rA_Mat[1,5] * rLambda_Costate[4,1]) + (rA_Mat[2,5] * rLambda_Costate[4,2]) + (rA_Mat[3,5] * rLambda_Costate[4,3]) + (rA_Mat[4,5] * rLambda_Costate[4,4]) + (rA_Mat[5,5] * rLambda_Costate[4,5]) + (rA_Mat[6,5] * rLambda_Costate[4,6]) + (rQ_Diag[5] * (rX_Pred_Horizon[3,5] - rX_Target[3,5]));
rLambda_Costate[3, 6] := (rA_Mat[1,6] * rLambda_Costate[4,1]) + (rA_Mat[2,6] * rLambda_Costate[4,2]) + (rA_Mat[3,6] * rLambda_Costate[4,3]) + (rA_Mat[4,6] * rLambda_Costate[4,4]) + (rA_Mat[5,6] * rLambda_Costate[4,5]) + (rA_Mat[6,6] * rLambda_Costate[4,6]) + (rQ_Diag[6] * (rX_Pred_Horizon[3,6] - rX_Target[3,6]));

(* Adjoint Costate at h=2: lambda_2 = A^T * lambda_3 + Q * (x_2 - x_target_2) *)
rLambda_Costate[2, 1] := (rA_Mat[1,1] * rLambda_Costate[3,1]) + (rA_Mat[2,1] * rLambda_Costate[3,2]) + (rA_Mat[3,1] * rLambda_Costate[3,3]) + (rA_Mat[4,1] * rLambda_Costate[3,4]) + (rA_Mat[5,1] * rLambda_Costate[3,5]) + (rA_Mat[6,1] * rLambda_Costate[3,6]) + (rQ_Diag[1] * (rX_Pred_Horizon[2,1] - rX_Target[2,1]));
rLambda_Costate[2, 2] := (rA_Mat[1,2] * rLambda_Costate[3,1]) + (rA_Mat[2,2] * rLambda_Costate[3,2]) + (rA_Mat[3,2] * rLambda_Costate[3,3]) + (rA_Mat[4,2] * rLambda_Costate[3,4]) + (rA_Mat[5,2] * rLambda_Costate[3,5]) + (rA_Mat[6,2] * rLambda_Costate[3,6]) + (rQ_Diag[2] * (rX_Pred_Horizon[2,2] - rX_Target[2,2]));
rLambda_Costate[2, 3] := (rA_Mat[1,3] * rLambda_Costate[3,1]) + (rA_Mat[2,3] * rLambda_Costate[3,2]) + (rA_Mat[3,3] * rLambda_Costate[3,3]) + (rA_Mat[4,3] * rLambda_Costate[3,4]) + (rA_Mat[5,3] * rLambda_Costate[3,5]) + (rA_Mat[6,3] * rLambda_Costate[3,6]) + (rQ_Diag[3] * (rX_Pred_Horizon[2,3] - rX_Target[2,3]));
rLambda_Costate[2, 4] := (rA_Mat[1,4] * rLambda_Costate[3,1]) + (rA_Mat[2,4] * rLambda_Costate[3,2]) + (rA_Mat[3,4] * rLambda_Costate[3,3]) + (rA_Mat[4,4] * rLambda_Costate[3,4]) + (rA_Mat[5,4] * rLambda_Costate[3,5]) + (rA_Mat[6,4] * rLambda_Costate[3,6]) + (rQ_Diag[4] * (rX_Pred_Horizon[2,4] - rX_Target[2,4]));
rLambda_Costate[2, 5] := (rA_Mat[1,5] * rLambda_Costate[3,1]) + (rA_Mat[2,5] * rLambda_Costate[3,2]) + (rA_Mat[3,5] * rLambda_Costate[3,3]) + (rA_Mat[4,5] * rLambda_Costate[3,4]) + (rA_Mat[5,5] * rLambda_Costate[3,5]) + (rA_Mat[6,5] * rLambda_Costate[3,6]) + (rQ_Diag[5] * (rX_Pred_Horizon[2,5] - rX_Target[2,5]));
rLambda_Costate[2, 6] := (rA_Mat[1,6] * rLambda_Costate[3,1]) + (rA_Mat[2,6] * rLambda_Costate[3,2]) + (rA_Mat[3,6] * rLambda_Costate[3,3]) + (rA_Mat[4,6] * rLambda_Costate[3,4]) + (rA_Mat[5,6] * rLambda_Costate[3,5]) + (rA_Mat[6,6] * rLambda_Costate[3,6]) + (rQ_Diag[6] * (rX_Pred_Horizon[2,6] - rX_Target[2,6]));

(* Adjoint Costate at h=1: lambda_1 = A^T * lambda_2 + Q * (x_1 - x_target_1) *)
rLambda_Costate[1, 1] := (rA_Mat[1,1] * rLambda_Costate[2,1]) + (rA_Mat[2,1] * rLambda_Costate[2,2]) + (rA_Mat[3,1] * rLambda_Costate[2,3]) + (rA_Mat[4,1] * rLambda_Costate[2,4]) + (rA_Mat[5,1] * rLambda_Costate[2,5]) + (rA_Mat[6,1] * rLambda_Costate[2,6]) + (rQ_Diag[1] * (rX_Pred_Horizon[1,1] - rX_Target[1,1]));
rLambda_Costate[1, 2] := (rA_Mat[1,2] * rLambda_Costate[2,1]) + (rA_Mat[2,2] * rLambda_Costate[2,2]) + (rA_Mat[3,2] * rLambda_Costate[2,3]) + (rA_Mat[4,2] * rLambda_Costate[2,4]) + (rA_Mat[5,2] * rLambda_Costate[2,5]) + (rA_Mat[6,2] * rLambda_Costate[2,6]) + (rQ_Diag[2] * (rX_Pred_Horizon[1,2] - rX_Target[1,2]));
rLambda_Costate[1, 3] := (rA_Mat[1,3] * rLambda_Costate[2,1]) + (rA_Mat[2,3] * rLambda_Costate[2,2]) + (rA_Mat[3,3] * rLambda_Costate[2,3]) + (rA_Mat[4,3] * rLambda_Costate[2,4]) + (rA_Mat[5,3] * rLambda_Costate[2,5]) + (rA_Mat[6,3] * rLambda_Costate[2,6]) + (rQ_Diag[3] * (rX_Pred_Horizon[1,3] - rX_Target[1,3]));
rLambda_Costate[1, 4] := (rA_Mat[1,4] * rLambda_Costate[2,1]) + (rA_Mat[2,4] * rLambda_Costate[2,2]) + (rA_Mat[3,4] * rLambda_Costate[2,3]) + (rA_Mat[4,4] * rLambda_Costate[2,4]) + (rA_Mat[5,4] * rLambda_Costate[2,5]) + (rA_Mat[6,4] * rLambda_Costate[2,6]) + (rQ_Diag[4] * (rX_Pred_Horizon[1,4] - rX_Target[1,4]));
rLambda_Costate[1, 5] := (rA_Mat[1,5] * rLambda_Costate[2,1]) + (rA_Mat[2,5] * rLambda_Costate[2,2]) + (rA_Mat[3,5] * rLambda_Costate[2,3]) + (rA_Mat[4,5] * rLambda_Costate[2,4]) + (rA_Mat[5,5] * rLambda_Costate[2,5]) + (rA_Mat[6,5] * rLambda_Costate[2,6]) + (rQ_Diag[5] * (rX_Pred_Horizon[1,5] - rX_Target[1,5]));
rLambda_Costate[1, 6] := (rA_Mat[1,6] * rLambda_Costate[2,1]) + (rA_Mat[2,6] * rLambda_Costate[2,2]) + (rA_Mat[3,6] * rLambda_Costate[2,3]) + (rA_Mat[4,6] * rLambda_Costate[2,4]) + (rA_Mat[5,6] * rLambda_Costate[2,5]) + (rA_Mat[6,6] * rLambda_Costate[2,6]) + (rQ_Diag[6] * (rX_Pred_Horizon[1,6] - rX_Target[1,6]));

(* Iteration 9 - Analytical Gradient Computation w.r.t. Control Inputs u_h *)
rMPC_GradNormSq := 0.0;
(* Gradient for u_1 (h=1) *)
rGrad_J[1, 1] := (rB_Mat[1,1] * rLambda_Costate[1,1]) + (rB_Mat[2,1] * rLambda_Costate[1,2]) + (rB_Mat[3,1] * rLambda_Costate[1,3]) + (rB_Mat[4,1] * rLambda_Costate[1,4]) + (rB_Mat[5,1] * rLambda_Costate[1,5]) + (rB_Mat[6,1] * rLambda_Costate[1,6]) + (rR_Diag[1] * rU_Opt_Seq[1,1]) + (rS_Diag[1] * (rU_Opt_Seq[1,1] - a_u_prev[1])) - (rS_Diag[1] * (rU_Opt_Seq[2,1] - rU_Opt_Seq[1,1]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[1, 1] * rGrad_J[1, 1]);
rGrad_J[1, 2] := (rB_Mat[1,2] * rLambda_Costate[1,1]) + (rB_Mat[2,2] * rLambda_Costate[1,2]) + (rB_Mat[3,2] * rLambda_Costate[1,3]) + (rB_Mat[4,2] * rLambda_Costate[1,4]) + (rB_Mat[5,2] * rLambda_Costate[1,5]) + (rB_Mat[6,2] * rLambda_Costate[1,6]) + (rR_Diag[2] * rU_Opt_Seq[1,2]) + (rS_Diag[2] * (rU_Opt_Seq[1,2] - a_u_prev[2])) - (rS_Diag[2] * (rU_Opt_Seq[2,2] - rU_Opt_Seq[1,2]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[1, 2] * rGrad_J[1, 2]);
rGrad_J[1, 3] := (rB_Mat[1,3] * rLambda_Costate[1,1]) + (rB_Mat[2,3] * rLambda_Costate[1,2]) + (rB_Mat[3,3] * rLambda_Costate[1,3]) + (rB_Mat[4,3] * rLambda_Costate[1,4]) + (rB_Mat[5,3] * rLambda_Costate[1,5]) + (rB_Mat[6,3] * rLambda_Costate[1,6]) + (rR_Diag[3] * rU_Opt_Seq[1,3]) + (rS_Diag[3] * (rU_Opt_Seq[1,3] - a_u_prev[3])) - (rS_Diag[3] * (rU_Opt_Seq[2,3] - rU_Opt_Seq[1,3]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[1, 3] * rGrad_J[1, 3]);
rGrad_J[1, 4] := (rB_Mat[1,4] * rLambda_Costate[1,1]) + (rB_Mat[2,4] * rLambda_Costate[1,2]) + (rB_Mat[3,4] * rLambda_Costate[1,3]) + (rB_Mat[4,4] * rLambda_Costate[1,4]) + (rB_Mat[5,4] * rLambda_Costate[1,5]) + (rB_Mat[6,4] * rLambda_Costate[1,6]) + (rR_Diag[4] * rU_Opt_Seq[1,4]) + (rS_Diag[4] * (rU_Opt_Seq[1,4] - a_u_prev[4])) - (rS_Diag[4] * (rU_Opt_Seq[2,4] - rU_Opt_Seq[1,4]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[1, 4] * rGrad_J[1, 4]);
rGrad_J[1, 5] := (rB_Mat[1,5] * rLambda_Costate[1,1]) + (rB_Mat[2,5] * rLambda_Costate[1,2]) + (rB_Mat[3,5] * rLambda_Costate[1,3]) + (rB_Mat[4,5] * rLambda_Costate[1,4]) + (rB_Mat[5,5] * rLambda_Costate[1,5]) + (rB_Mat[6,5] * rLambda_Costate[1,6]) + (rR_Diag[5] * rU_Opt_Seq[1,5]) + (rS_Diag[5] * (rU_Opt_Seq[1,5] - a_u_prev[5])) - (rS_Diag[5] * (rU_Opt_Seq[2,5] - rU_Opt_Seq[1,5]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[1, 5] * rGrad_J[1, 5]);

(* Gradient for u_2 (h=2) *)
rGrad_J[2, 1] := (rB_Mat[1,1] * rLambda_Costate[2,1]) + (rB_Mat[2,1] * rLambda_Costate[2,2]) + (rB_Mat[3,1] * rLambda_Costate[2,3]) + (rB_Mat[4,1] * rLambda_Costate[2,4]) + (rB_Mat[5,1] * rLambda_Costate[2,5]) + (rB_Mat[6,1] * rLambda_Costate[2,6]) + (rR_Diag[1] * rU_Opt_Seq[2,1]) + (rS_Diag[1] * (rU_Opt_Seq[2,1] - rU_Opt_Seq[1,1])) - (rS_Diag[1] * (rU_Opt_Seq[3,1] - rU_Opt_Seq[2,1]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[2, 1] * rGrad_J[2, 1]);
rGrad_J[2, 2] := (rB_Mat[1,2] * rLambda_Costate[2,1]) + (rB_Mat[2,2] * rLambda_Costate[2,2]) + (rB_Mat[3,2] * rLambda_Costate[2,3]) + (rB_Mat[4,2] * rLambda_Costate[2,4]) + (rB_Mat[5,2] * rLambda_Costate[2,5]) + (rB_Mat[6,2] * rLambda_Costate[2,6]) + (rR_Diag[2] * rU_Opt_Seq[2,2]) + (rS_Diag[2] * (rU_Opt_Seq[2,2] - rU_Opt_Seq[1,2])) - (rS_Diag[2] * (rU_Opt_Seq[3,2] - rU_Opt_Seq[2,2]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[2, 2] * rGrad_J[2, 2]);
rGrad_J[2, 3] := (rB_Mat[1,3] * rLambda_Costate[2,1]) + (rB_Mat[2,3] * rLambda_Costate[2,2]) + (rB_Mat[3,3] * rLambda_Costate[2,3]) + (rB_Mat[4,3] * rLambda_Costate[2,4]) + (rB_Mat[5,3] * rLambda_Costate[2,5]) + (rB_Mat[6,3] * rLambda_Costate[2,6]) + (rR_Diag[3] * rU_Opt_Seq[2,3]) + (rS_Diag[3] * (rU_Opt_Seq[2,3] - rU_Opt_Seq[1,3])) - (rS_Diag[3] * (rU_Opt_Seq[3,3] - rU_Opt_Seq[2,3]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[2, 3] * rGrad_J[2, 3]);
rGrad_J[2, 4] := (rB_Mat[1,4] * rLambda_Costate[2,1]) + (rB_Mat[2,4] * rLambda_Costate[2,2]) + (rB_Mat[3,4] * rLambda_Costate[2,3]) + (rB_Mat[4,4] * rLambda_Costate[2,4]) + (rB_Mat[5,4] * rLambda_Costate[2,5]) + (rB_Mat[6,4] * rLambda_Costate[2,6]) + (rR_Diag[4] * rU_Opt_Seq[2,4]) + (rS_Diag[4] * (rU_Opt_Seq[2,4] - rU_Opt_Seq[1,4])) - (rS_Diag[4] * (rU_Opt_Seq[3,4] - rU_Opt_Seq[2,4]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[2, 4] * rGrad_J[2, 4]);
rGrad_J[2, 5] := (rB_Mat[1,5] * rLambda_Costate[2,1]) + (rB_Mat[2,5] * rLambda_Costate[2,2]) + (rB_Mat[3,5] * rLambda_Costate[2,3]) + (rB_Mat[4,5] * rLambda_Costate[2,4]) + (rB_Mat[5,5] * rLambda_Costate[2,5]) + (rB_Mat[6,5] * rLambda_Costate[2,6]) + (rR_Diag[5] * rU_Opt_Seq[2,5]) + (rS_Diag[5] * (rU_Opt_Seq[2,5] - rU_Opt_Seq[1,5])) - (rS_Diag[5] * (rU_Opt_Seq[3,5] - rU_Opt_Seq[2,5]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[2, 5] * rGrad_J[2, 5]);

(* Gradient for u_3 (h=3, held through h=4, 5) *)
rGrad_J[3, 1] := (rB_Mat[1,1] * (rLambda_Costate[3,1] + rLambda_Costate[4,1] + rLambda_Costate[5,1])) + (rB_Mat[2,1] * (rLambda_Costate[3,2] + rLambda_Costate[4,2] + rLambda_Costate[5,2])) + (rB_Mat[3,1] * (rLambda_Costate[3,3] + rLambda_Costate[4,3] + rLambda_Costate[5,3])) + (rB_Mat[4,1] * (rLambda_Costate[3,4] + rLambda_Costate[4,4] + rLambda_Costate[5,4])) + (rB_Mat[5,1] * (rLambda_Costate[3,5] + rLambda_Costate[4,5] + rLambda_Costate[5,5])) + (rB_Mat[6,1] * (rLambda_Costate[3,6] + rLambda_Costate[4,6] + rLambda_Costate[5,6])) + (rR_Diag[1] * rU_Opt_Seq[3,1]) + (rS_Diag[1] * (rU_Opt_Seq[3,1] - rU_Opt_Seq[2,1]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[3, 1] * rGrad_J[3, 1]);
rGrad_J[3, 2] := (rB_Mat[1,2] * (rLambda_Costate[3,1] + rLambda_Costate[4,1] + rLambda_Costate[5,1])) + (rB_Mat[2,2] * (rLambda_Costate[3,2] + rLambda_Costate[4,2] + rLambda_Costate[5,2])) + (rB_Mat[3,2] * (rLambda_Costate[3,3] + rLambda_Costate[4,3] + rLambda_Costate[5,3])) + (rB_Mat[4,2] * (rLambda_Costate[3,4] + rLambda_Costate[4,4] + rLambda_Costate[5,4])) + (rB_Mat[5,2] * (rLambda_Costate[3,5] + rLambda_Costate[4,5] + rLambda_Costate[5,5])) + (rB_Mat[6,2] * (rLambda_Costate[3,6] + rLambda_Costate[4,6] + rLambda_Costate[5,6])) + (rR_Diag[2] * rU_Opt_Seq[3,2]) + (rS_Diag[2] * (rU_Opt_Seq[3,2] - rU_Opt_Seq[2,2]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[3, 2] * rGrad_J[3, 2]);
rGrad_J[3, 3] := (rB_Mat[1,3] * (rLambda_Costate[3,1] + rLambda_Costate[4,1] + rLambda_Costate[5,1])) + (rB_Mat[2,3] * (rLambda_Costate[3,2] + rLambda_Costate[4,2] + rLambda_Costate[5,2])) + (rB_Mat[3,3] * (rLambda_Costate[3,3] + rLambda_Costate[4,3] + rLambda_Costate[5,3])) + (rB_Mat[4,3] * (rLambda_Costate[3,4] + rLambda_Costate[4,4] + rLambda_Costate[5,4])) + (rB_Mat[5,3] * (rLambda_Costate[3,5] + rLambda_Costate[4,5] + rLambda_Costate[5,5])) + (rB_Mat[6,3] * (rLambda_Costate[3,6] + rLambda_Costate[4,6] + rLambda_Costate[5,6])) + (rR_Diag[3] * rU_Opt_Seq[3,3]) + (rS_Diag[3] * (rU_Opt_Seq[3,3] - rU_Opt_Seq[2,3]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[3, 3] * rGrad_J[3, 3]);
rGrad_J[3, 4] := (rB_Mat[1,4] * (rLambda_Costate[3,1] + rLambda_Costate[4,1] + rLambda_Costate[5,1])) + (rB_Mat[2,4] * (rLambda_Costate[3,2] + rLambda_Costate[4,2] + rLambda_Costate[5,2])) + (rB_Mat[3,4] * (rLambda_Costate[3,3] + rLambda_Costate[4,3] + rLambda_Costate[5,3])) + (rB_Mat[4,4] * (rLambda_Costate[3,4] + rLambda_Costate[4,4] + rLambda_Costate[5,4])) + (rB_Mat[5,4] * (rLambda_Costate[3,5] + rLambda_Costate[4,5] + rLambda_Costate[5,5])) + (rB_Mat[6,4] * (rLambda_Costate[3,6] + rLambda_Costate[4,6] + rLambda_Costate[5,6])) + (rR_Diag[4] * rU_Opt_Seq[3,4]) + (rS_Diag[4] * (rU_Opt_Seq[3,4] - rU_Opt_Seq[2,4]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[3, 4] * rGrad_J[3, 4]);
rGrad_J[3, 5] := (rB_Mat[1,5] * (rLambda_Costate[3,1] + rLambda_Costate[4,1] + rLambda_Costate[5,1])) + (rB_Mat[2,5] * (rLambda_Costate[3,2] + rLambda_Costate[4,2] + rLambda_Costate[5,2])) + (rB_Mat[3,5] * (rLambda_Costate[3,3] + rLambda_Costate[4,3] + rLambda_Costate[5,3])) + (rB_Mat[4,5] * (rLambda_Costate[3,4] + rLambda_Costate[4,4] + rLambda_Costate[5,4])) + (rB_Mat[5,5] * (rLambda_Costate[3,5] + rLambda_Costate[4,5] + rLambda_Costate[5,5])) + (rB_Mat[6,5] * (rLambda_Costate[3,6] + rLambda_Costate[4,6] + rLambda_Costate[5,6])) + (rR_Diag[5] * rU_Opt_Seq[3,5]) + (rS_Diag[5] * (rU_Opt_Seq[3,5] - rU_Opt_Seq[2,5]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[3, 5] * rGrad_J[3, 5]);

(* Iteration 9 - Projected Gradient Step with Hard Box & Dynamic Slew Limits *)
rTemp_Val := rU_Opt_Seq[1, 1] - (rAlpha_PGD_StepSize * rGrad_J[1, 1]);
(* Slew limit against prior actuator output *)
IF rTemp_Val > (a_u_prev[1] + rDeltaU_Max[1]) THEN
    rTemp_Val := a_u_prev[1] + rDeltaU_Max[1];
ELSIF rTemp_Val < (a_u_prev[1] - rDeltaU_Max[1]) THEN
    rTemp_Val := a_u_prev[1] - rDeltaU_Max[1];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[1] THEN
    rTemp_Val := rU_BoxMax[1];
ELSIF rTemp_Val < rU_BoxMin[1] THEN
    rTemp_Val := rU_BoxMin[1];
END_IF;
rU_Opt_Seq[1, 1] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[1, 2] - (rAlpha_PGD_StepSize * rGrad_J[1, 2]);
(* Slew limit against prior actuator output *)
IF rTemp_Val > (a_u_prev[2] + rDeltaU_Max[2]) THEN
    rTemp_Val := a_u_prev[2] + rDeltaU_Max[2];
ELSIF rTemp_Val < (a_u_prev[2] - rDeltaU_Max[2]) THEN
    rTemp_Val := a_u_prev[2] - rDeltaU_Max[2];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[2] THEN
    rTemp_Val := rU_BoxMax[2];
ELSIF rTemp_Val < rU_BoxMin[2] THEN
    rTemp_Val := rU_BoxMin[2];
END_IF;
rU_Opt_Seq[1, 2] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[1, 3] - (rAlpha_PGD_StepSize * rGrad_J[1, 3]);
(* Slew limit against prior actuator output *)
IF rTemp_Val > (a_u_prev[3] + rDeltaU_Max[3]) THEN
    rTemp_Val := a_u_prev[3] + rDeltaU_Max[3];
ELSIF rTemp_Val < (a_u_prev[3] - rDeltaU_Max[3]) THEN
    rTemp_Val := a_u_prev[3] - rDeltaU_Max[3];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[3] THEN
    rTemp_Val := rU_BoxMax[3];
ELSIF rTemp_Val < rU_BoxMin[3] THEN
    rTemp_Val := rU_BoxMin[3];
END_IF;
rU_Opt_Seq[1, 3] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[1, 4] - (rAlpha_PGD_StepSize * rGrad_J[1, 4]);
(* Slew limit against prior actuator output *)
IF rTemp_Val > (a_u_prev[4] + rDeltaU_Max[4]) THEN
    rTemp_Val := a_u_prev[4] + rDeltaU_Max[4];
ELSIF rTemp_Val < (a_u_prev[4] - rDeltaU_Max[4]) THEN
    rTemp_Val := a_u_prev[4] - rDeltaU_Max[4];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[4] THEN
    rTemp_Val := rU_BoxMax[4];
ELSIF rTemp_Val < rU_BoxMin[4] THEN
    rTemp_Val := rU_BoxMin[4];
END_IF;
rU_Opt_Seq[1, 4] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[1, 5] - (rAlpha_PGD_StepSize * rGrad_J[1, 5]);
(* Slew limit against prior actuator output *)
IF rTemp_Val > (a_u_prev[5] + rDeltaU_Max[5]) THEN
    rTemp_Val := a_u_prev[5] + rDeltaU_Max[5];
ELSIF rTemp_Val < (a_u_prev[5] - rDeltaU_Max[5]) THEN
    rTemp_Val := a_u_prev[5] - rDeltaU_Max[5];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[5] THEN
    rTemp_Val := rU_BoxMax[5];
ELSIF rTemp_Val < rU_BoxMin[5] THEN
    rTemp_Val := rU_BoxMin[5];
END_IF;
rU_Opt_Seq[1, 5] := rTemp_Val;

rTemp_Val := rU_Opt_Seq[2, 1] - (rAlpha_PGD_StepSize * rGrad_J[2, 1]);
(* Slew limit against step 1 *)
IF rTemp_Val > (rU_Opt_Seq[1, 1] + rDeltaU_Max[1]) THEN
    rTemp_Val := rU_Opt_Seq[1, 1] + rDeltaU_Max[1];
ELSIF rTemp_Val < (rU_Opt_Seq[1, 1] - rDeltaU_Max[1]) THEN
    rTemp_Val := rU_Opt_Seq[1, 1] - rDeltaU_Max[1];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[1] THEN
    rTemp_Val := rU_BoxMax[1];
ELSIF rTemp_Val < rU_BoxMin[1] THEN
    rTemp_Val := rU_BoxMin[1];
END_IF;
rU_Opt_Seq[2, 1] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[2, 2] - (rAlpha_PGD_StepSize * rGrad_J[2, 2]);
(* Slew limit against step 1 *)
IF rTemp_Val > (rU_Opt_Seq[1, 2] + rDeltaU_Max[2]) THEN
    rTemp_Val := rU_Opt_Seq[1, 2] + rDeltaU_Max[2];
ELSIF rTemp_Val < (rU_Opt_Seq[1, 2] - rDeltaU_Max[2]) THEN
    rTemp_Val := rU_Opt_Seq[1, 2] - rDeltaU_Max[2];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[2] THEN
    rTemp_Val := rU_BoxMax[2];
ELSIF rTemp_Val < rU_BoxMin[2] THEN
    rTemp_Val := rU_BoxMin[2];
END_IF;
rU_Opt_Seq[2, 2] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[2, 3] - (rAlpha_PGD_StepSize * rGrad_J[2, 3]);
(* Slew limit against step 1 *)
IF rTemp_Val > (rU_Opt_Seq[1, 3] + rDeltaU_Max[3]) THEN
    rTemp_Val := rU_Opt_Seq[1, 3] + rDeltaU_Max[3];
ELSIF rTemp_Val < (rU_Opt_Seq[1, 3] - rDeltaU_Max[3]) THEN
    rTemp_Val := rU_Opt_Seq[1, 3] - rDeltaU_Max[3];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[3] THEN
    rTemp_Val := rU_BoxMax[3];
ELSIF rTemp_Val < rU_BoxMin[3] THEN
    rTemp_Val := rU_BoxMin[3];
END_IF;
rU_Opt_Seq[2, 3] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[2, 4] - (rAlpha_PGD_StepSize * rGrad_J[2, 4]);
(* Slew limit against step 1 *)
IF rTemp_Val > (rU_Opt_Seq[1, 4] + rDeltaU_Max[4]) THEN
    rTemp_Val := rU_Opt_Seq[1, 4] + rDeltaU_Max[4];
ELSIF rTemp_Val < (rU_Opt_Seq[1, 4] - rDeltaU_Max[4]) THEN
    rTemp_Val := rU_Opt_Seq[1, 4] - rDeltaU_Max[4];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[4] THEN
    rTemp_Val := rU_BoxMax[4];
ELSIF rTemp_Val < rU_BoxMin[4] THEN
    rTemp_Val := rU_BoxMin[4];
END_IF;
rU_Opt_Seq[2, 4] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[2, 5] - (rAlpha_PGD_StepSize * rGrad_J[2, 5]);
(* Slew limit against step 1 *)
IF rTemp_Val > (rU_Opt_Seq[1, 5] + rDeltaU_Max[5]) THEN
    rTemp_Val := rU_Opt_Seq[1, 5] + rDeltaU_Max[5];
ELSIF rTemp_Val < (rU_Opt_Seq[1, 5] - rDeltaU_Max[5]) THEN
    rTemp_Val := rU_Opt_Seq[1, 5] - rDeltaU_Max[5];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[5] THEN
    rTemp_Val := rU_BoxMax[5];
ELSIF rTemp_Val < rU_BoxMin[5] THEN
    rTemp_Val := rU_BoxMin[5];
END_IF;
rU_Opt_Seq[2, 5] := rTemp_Val;

rTemp_Val := rU_Opt_Seq[3, 1] - (rAlpha_PGD_StepSize * rGrad_J[3, 1]);
(* Slew limit against step 2 *)
IF rTemp_Val > (rU_Opt_Seq[2, 1] + rDeltaU_Max[1]) THEN
    rTemp_Val := rU_Opt_Seq[2, 1] + rDeltaU_Max[1];
ELSIF rTemp_Val < (rU_Opt_Seq[2, 1] - rDeltaU_Max[1]) THEN
    rTemp_Val := rU_Opt_Seq[2, 1] - rDeltaU_Max[1];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[1] THEN
    rTemp_Val := rU_BoxMax[1];
ELSIF rTemp_Val < rU_BoxMin[1] THEN
    rTemp_Val := rU_BoxMin[1];
END_IF;
rU_Opt_Seq[3, 1] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[3, 2] - (rAlpha_PGD_StepSize * rGrad_J[3, 2]);
(* Slew limit against step 2 *)
IF rTemp_Val > (rU_Opt_Seq[2, 2] + rDeltaU_Max[2]) THEN
    rTemp_Val := rU_Opt_Seq[2, 2] + rDeltaU_Max[2];
ELSIF rTemp_Val < (rU_Opt_Seq[2, 2] - rDeltaU_Max[2]) THEN
    rTemp_Val := rU_Opt_Seq[2, 2] - rDeltaU_Max[2];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[2] THEN
    rTemp_Val := rU_BoxMax[2];
ELSIF rTemp_Val < rU_BoxMin[2] THEN
    rTemp_Val := rU_BoxMin[2];
END_IF;
rU_Opt_Seq[3, 2] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[3, 3] - (rAlpha_PGD_StepSize * rGrad_J[3, 3]);
(* Slew limit against step 2 *)
IF rTemp_Val > (rU_Opt_Seq[2, 3] + rDeltaU_Max[3]) THEN
    rTemp_Val := rU_Opt_Seq[2, 3] + rDeltaU_Max[3];
ELSIF rTemp_Val < (rU_Opt_Seq[2, 3] - rDeltaU_Max[3]) THEN
    rTemp_Val := rU_Opt_Seq[2, 3] - rDeltaU_Max[3];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[3] THEN
    rTemp_Val := rU_BoxMax[3];
ELSIF rTemp_Val < rU_BoxMin[3] THEN
    rTemp_Val := rU_BoxMin[3];
END_IF;
rU_Opt_Seq[3, 3] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[3, 4] - (rAlpha_PGD_StepSize * rGrad_J[3, 4]);
(* Slew limit against step 2 *)
IF rTemp_Val > (rU_Opt_Seq[2, 4] + rDeltaU_Max[4]) THEN
    rTemp_Val := rU_Opt_Seq[2, 4] + rDeltaU_Max[4];
ELSIF rTemp_Val < (rU_Opt_Seq[2, 4] - rDeltaU_Max[4]) THEN
    rTemp_Val := rU_Opt_Seq[2, 4] - rDeltaU_Max[4];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[4] THEN
    rTemp_Val := rU_BoxMax[4];
ELSIF rTemp_Val < rU_BoxMin[4] THEN
    rTemp_Val := rU_BoxMin[4];
END_IF;
rU_Opt_Seq[3, 4] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[3, 5] - (rAlpha_PGD_StepSize * rGrad_J[3, 5]);
(* Slew limit against step 2 *)
IF rTemp_Val > (rU_Opt_Seq[2, 5] + rDeltaU_Max[5]) THEN
    rTemp_Val := rU_Opt_Seq[2, 5] + rDeltaU_Max[5];
ELSIF rTemp_Val < (rU_Opt_Seq[2, 5] - rDeltaU_Max[5]) THEN
    rTemp_Val := rU_Opt_Seq[2, 5] - rDeltaU_Max[5];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[5] THEN
    rTemp_Val := rU_BoxMax[5];
ELSIF rTemp_Val < rU_BoxMin[5] THEN
    rTemp_Val := rU_BoxMin[5];
END_IF;
rU_Opt_Seq[3, 5] := rTemp_Val;

(* ================================================================================================== *)
(* MPC PROJECTED GRADIENT DESCENT -- UNROLLED ITERATION 10 OF 10                                 *)
(* ================================================================================================== *)
iPGD_IterCount := 10;

(* Iteration 10 - Forward State Prediction Step 1 (h=1): x_1 = A * x_hat + B * u_1 *)
rX_Pred_Horizon[1, 1] := (rA_Mat[1,1] * a_x_hat[1]) + (rA_Mat[1,2] * a_x_hat[2]) + (rA_Mat[1,3] * a_x_hat[3]) + (rA_Mat[1,4] * a_x_hat[4]) + (rA_Mat[1,5] * a_x_hat[5]) + (rA_Mat[1,6] * a_x_hat[6]) + (rB_Mat[1,1] * rU_Opt_Seq[1,1]) + (rB_Mat[1,2] * rU_Opt_Seq[1,2]) + (rB_Mat[1,3] * rU_Opt_Seq[1,3]) + (rB_Mat[1,4] * rU_Opt_Seq[1,4]) + (rB_Mat[1,5] * rU_Opt_Seq[1,5]);
rX_Pred_Horizon[1, 2] := (rA_Mat[2,1] * a_x_hat[1]) + (rA_Mat[2,2] * a_x_hat[2]) + (rA_Mat[2,3] * a_x_hat[3]) + (rA_Mat[2,4] * a_x_hat[4]) + (rA_Mat[2,5] * a_x_hat[5]) + (rA_Mat[2,6] * a_x_hat[6]) + (rB_Mat[2,1] * rU_Opt_Seq[1,1]) + (rB_Mat[2,2] * rU_Opt_Seq[1,2]) + (rB_Mat[2,3] * rU_Opt_Seq[1,3]) + (rB_Mat[2,4] * rU_Opt_Seq[1,4]) + (rB_Mat[2,5] * rU_Opt_Seq[1,5]);
rX_Pred_Horizon[1, 3] := (rA_Mat[3,1] * a_x_hat[1]) + (rA_Mat[3,2] * a_x_hat[2]) + (rA_Mat[3,3] * a_x_hat[3]) + (rA_Mat[3,4] * a_x_hat[4]) + (rA_Mat[3,5] * a_x_hat[5]) + (rA_Mat[3,6] * a_x_hat[6]) + (rB_Mat[3,1] * rU_Opt_Seq[1,1]) + (rB_Mat[3,2] * rU_Opt_Seq[1,2]) + (rB_Mat[3,3] * rU_Opt_Seq[1,3]) + (rB_Mat[3,4] * rU_Opt_Seq[1,4]) + (rB_Mat[3,5] * rU_Opt_Seq[1,5]);
rX_Pred_Horizon[1, 4] := (rA_Mat[4,1] * a_x_hat[1]) + (rA_Mat[4,2] * a_x_hat[2]) + (rA_Mat[4,3] * a_x_hat[3]) + (rA_Mat[4,4] * a_x_hat[4]) + (rA_Mat[4,5] * a_x_hat[5]) + (rA_Mat[4,6] * a_x_hat[6]) + (rB_Mat[4,1] * rU_Opt_Seq[1,1]) + (rB_Mat[4,2] * rU_Opt_Seq[1,2]) + (rB_Mat[4,3] * rU_Opt_Seq[1,3]) + (rB_Mat[4,4] * rU_Opt_Seq[1,4]) + (rB_Mat[4,5] * rU_Opt_Seq[1,5]);
rX_Pred_Horizon[1, 5] := (rA_Mat[5,1] * a_x_hat[1]) + (rA_Mat[5,2] * a_x_hat[2]) + (rA_Mat[5,3] * a_x_hat[3]) + (rA_Mat[5,4] * a_x_hat[4]) + (rA_Mat[5,5] * a_x_hat[5]) + (rA_Mat[5,6] * a_x_hat[6]) + (rB_Mat[5,1] * rU_Opt_Seq[1,1]) + (rB_Mat[5,2] * rU_Opt_Seq[1,2]) + (rB_Mat[5,3] * rU_Opt_Seq[1,3]) + (rB_Mat[5,4] * rU_Opt_Seq[1,4]) + (rB_Mat[5,5] * rU_Opt_Seq[1,5]);
rX_Pred_Horizon[1, 6] := (rA_Mat[6,1] * a_x_hat[1]) + (rA_Mat[6,2] * a_x_hat[2]) + (rA_Mat[6,3] * a_x_hat[3]) + (rA_Mat[6,4] * a_x_hat[4]) + (rA_Mat[6,5] * a_x_hat[5]) + (rA_Mat[6,6] * a_x_hat[6]) + (rB_Mat[6,1] * rU_Opt_Seq[1,1]) + (rB_Mat[6,2] * rU_Opt_Seq[1,2]) + (rB_Mat[6,3] * rU_Opt_Seq[1,3]) + (rB_Mat[6,4] * rU_Opt_Seq[1,4]) + (rB_Mat[6,5] * rU_Opt_Seq[1,5]);

(* Iteration 10 - Forward State Prediction Step 2 (h=2): x_2 = A * x_1 + B * u_2 *)
rX_Pred_Horizon[2, 1] := (rA_Mat[1,1] * rX_Pred_Horizon[1,1]) + (rA_Mat[1,2] * rX_Pred_Horizon[1,2]) + (rA_Mat[1,3] * rX_Pred_Horizon[1,3]) + (rA_Mat[1,4] * rX_Pred_Horizon[1,4]) + (rA_Mat[1,5] * rX_Pred_Horizon[1,5]) + (rA_Mat[1,6] * rX_Pred_Horizon[1,6]) + (rB_Mat[1,1] * rU_Opt_Seq[2,1]) + (rB_Mat[1,2] * rU_Opt_Seq[2,2]) + (rB_Mat[1,3] * rU_Opt_Seq[2,3]) + (rB_Mat[1,4] * rU_Opt_Seq[2,4]) + (rB_Mat[1,5] * rU_Opt_Seq[2,5]);
rX_Pred_Horizon[2, 2] := (rA_Mat[2,1] * rX_Pred_Horizon[1,1]) + (rA_Mat[2,2] * rX_Pred_Horizon[1,2]) + (rA_Mat[2,3] * rX_Pred_Horizon[1,3]) + (rA_Mat[2,4] * rX_Pred_Horizon[1,4]) + (rA_Mat[2,5] * rX_Pred_Horizon[1,5]) + (rA_Mat[2,6] * rX_Pred_Horizon[1,6]) + (rB_Mat[2,1] * rU_Opt_Seq[2,1]) + (rB_Mat[2,2] * rU_Opt_Seq[2,2]) + (rB_Mat[2,3] * rU_Opt_Seq[2,3]) + (rB_Mat[2,4] * rU_Opt_Seq[2,4]) + (rB_Mat[2,5] * rU_Opt_Seq[2,5]);
rX_Pred_Horizon[2, 3] := (rA_Mat[3,1] * rX_Pred_Horizon[1,1]) + (rA_Mat[3,2] * rX_Pred_Horizon[1,2]) + (rA_Mat[3,3] * rX_Pred_Horizon[1,3]) + (rA_Mat[3,4] * rX_Pred_Horizon[1,4]) + (rA_Mat[3,5] * rX_Pred_Horizon[1,5]) + (rA_Mat[3,6] * rX_Pred_Horizon[1,6]) + (rB_Mat[3,1] * rU_Opt_Seq[2,1]) + (rB_Mat[3,2] * rU_Opt_Seq[2,2]) + (rB_Mat[3,3] * rU_Opt_Seq[2,3]) + (rB_Mat[3,4] * rU_Opt_Seq[2,4]) + (rB_Mat[3,5] * rU_Opt_Seq[2,5]);
rX_Pred_Horizon[2, 4] := (rA_Mat[4,1] * rX_Pred_Horizon[1,1]) + (rA_Mat[4,2] * rX_Pred_Horizon[1,2]) + (rA_Mat[4,3] * rX_Pred_Horizon[1,3]) + (rA_Mat[4,4] * rX_Pred_Horizon[1,4]) + (rA_Mat[4,5] * rX_Pred_Horizon[1,5]) + (rA_Mat[4,6] * rX_Pred_Horizon[1,6]) + (rB_Mat[4,1] * rU_Opt_Seq[2,1]) + (rB_Mat[4,2] * rU_Opt_Seq[2,2]) + (rB_Mat[4,3] * rU_Opt_Seq[2,3]) + (rB_Mat[4,4] * rU_Opt_Seq[2,4]) + (rB_Mat[4,5] * rU_Opt_Seq[2,5]);
rX_Pred_Horizon[2, 5] := (rA_Mat[5,1] * rX_Pred_Horizon[1,1]) + (rA_Mat[5,2] * rX_Pred_Horizon[1,2]) + (rA_Mat[5,3] * rX_Pred_Horizon[1,3]) + (rA_Mat[5,4] * rX_Pred_Horizon[1,4]) + (rA_Mat[5,5] * rX_Pred_Horizon[1,5]) + (rA_Mat[5,6] * rX_Pred_Horizon[1,6]) + (rB_Mat[5,1] * rU_Opt_Seq[2,1]) + (rB_Mat[5,2] * rU_Opt_Seq[2,2]) + (rB_Mat[5,3] * rU_Opt_Seq[2,3]) + (rB_Mat[5,4] * rU_Opt_Seq[2,4]) + (rB_Mat[5,5] * rU_Opt_Seq[2,5]);
rX_Pred_Horizon[2, 6] := (rA_Mat[6,1] * rX_Pred_Horizon[1,1]) + (rA_Mat[6,2] * rX_Pred_Horizon[1,2]) + (rA_Mat[6,3] * rX_Pred_Horizon[1,3]) + (rA_Mat[6,4] * rX_Pred_Horizon[1,4]) + (rA_Mat[6,5] * rX_Pred_Horizon[1,5]) + (rA_Mat[6,6] * rX_Pred_Horizon[1,6]) + (rB_Mat[6,1] * rU_Opt_Seq[2,1]) + (rB_Mat[6,2] * rU_Opt_Seq[2,2]) + (rB_Mat[6,3] * rU_Opt_Seq[2,3]) + (rB_Mat[6,4] * rU_Opt_Seq[2,4]) + (rB_Mat[6,5] * rU_Opt_Seq[2,5]);

(* Iteration 10 - Forward State Prediction Step 3 (h=3): x_3 = A * x_2 + B * u_3 *)
rX_Pred_Horizon[3, 1] := (rA_Mat[1,1] * rX_Pred_Horizon[2,1]) + (rA_Mat[1,2] * rX_Pred_Horizon[2,2]) + (rA_Mat[1,3] * rX_Pred_Horizon[2,3]) + (rA_Mat[1,4] * rX_Pred_Horizon[2,4]) + (rA_Mat[1,5] * rX_Pred_Horizon[2,5]) + (rA_Mat[1,6] * rX_Pred_Horizon[2,6]) + (rB_Mat[1,1] * rU_Opt_Seq[3,1]) + (rB_Mat[1,2] * rU_Opt_Seq[3,2]) + (rB_Mat[1,3] * rU_Opt_Seq[3,3]) + (rB_Mat[1,4] * rU_Opt_Seq[3,4]) + (rB_Mat[1,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[3, 2] := (rA_Mat[2,1] * rX_Pred_Horizon[2,1]) + (rA_Mat[2,2] * rX_Pred_Horizon[2,2]) + (rA_Mat[2,3] * rX_Pred_Horizon[2,3]) + (rA_Mat[2,4] * rX_Pred_Horizon[2,4]) + (rA_Mat[2,5] * rX_Pred_Horizon[2,5]) + (rA_Mat[2,6] * rX_Pred_Horizon[2,6]) + (rB_Mat[2,1] * rU_Opt_Seq[3,1]) + (rB_Mat[2,2] * rU_Opt_Seq[3,2]) + (rB_Mat[2,3] * rU_Opt_Seq[3,3]) + (rB_Mat[2,4] * rU_Opt_Seq[3,4]) + (rB_Mat[2,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[3, 3] := (rA_Mat[3,1] * rX_Pred_Horizon[2,1]) + (rA_Mat[3,2] * rX_Pred_Horizon[2,2]) + (rA_Mat[3,3] * rX_Pred_Horizon[2,3]) + (rA_Mat[3,4] * rX_Pred_Horizon[2,4]) + (rA_Mat[3,5] * rX_Pred_Horizon[2,5]) + (rA_Mat[3,6] * rX_Pred_Horizon[2,6]) + (rB_Mat[3,1] * rU_Opt_Seq[3,1]) + (rB_Mat[3,2] * rU_Opt_Seq[3,2]) + (rB_Mat[3,3] * rU_Opt_Seq[3,3]) + (rB_Mat[3,4] * rU_Opt_Seq[3,4]) + (rB_Mat[3,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[3, 4] := (rA_Mat[4,1] * rX_Pred_Horizon[2,1]) + (rA_Mat[4,2] * rX_Pred_Horizon[2,2]) + (rA_Mat[4,3] * rX_Pred_Horizon[2,3]) + (rA_Mat[4,4] * rX_Pred_Horizon[2,4]) + (rA_Mat[4,5] * rX_Pred_Horizon[2,5]) + (rA_Mat[4,6] * rX_Pred_Horizon[2,6]) + (rB_Mat[4,1] * rU_Opt_Seq[3,1]) + (rB_Mat[4,2] * rU_Opt_Seq[3,2]) + (rB_Mat[4,3] * rU_Opt_Seq[3,3]) + (rB_Mat[4,4] * rU_Opt_Seq[3,4]) + (rB_Mat[4,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[3, 5] := (rA_Mat[5,1] * rX_Pred_Horizon[2,1]) + (rA_Mat[5,2] * rX_Pred_Horizon[2,2]) + (rA_Mat[5,3] * rX_Pred_Horizon[2,3]) + (rA_Mat[5,4] * rX_Pred_Horizon[2,4]) + (rA_Mat[5,5] * rX_Pred_Horizon[2,5]) + (rA_Mat[5,6] * rX_Pred_Horizon[2,6]) + (rB_Mat[5,1] * rU_Opt_Seq[3,1]) + (rB_Mat[5,2] * rU_Opt_Seq[3,2]) + (rB_Mat[5,3] * rU_Opt_Seq[3,3]) + (rB_Mat[5,4] * rU_Opt_Seq[3,4]) + (rB_Mat[5,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[3, 6] := (rA_Mat[6,1] * rX_Pred_Horizon[2,1]) + (rA_Mat[6,2] * rX_Pred_Horizon[2,2]) + (rA_Mat[6,3] * rX_Pred_Horizon[2,3]) + (rA_Mat[6,4] * rX_Pred_Horizon[2,4]) + (rA_Mat[6,5] * rX_Pred_Horizon[2,5]) + (rA_Mat[6,6] * rX_Pred_Horizon[2,6]) + (rB_Mat[6,1] * rU_Opt_Seq[3,1]) + (rB_Mat[6,2] * rU_Opt_Seq[3,2]) + (rB_Mat[6,3] * rU_Opt_Seq[3,3]) + (rB_Mat[6,4] * rU_Opt_Seq[3,4]) + (rB_Mat[6,5] * rU_Opt_Seq[3,5]);

(* Iteration 10 - Forward State Prediction Step 4 (h=4): x_4 = A * x_3 + B * u_3 (held beyond Hu) *)
rX_Pred_Horizon[4, 1] := (rA_Mat[1,1] * rX_Pred_Horizon[3,1]) + (rA_Mat[1,2] * rX_Pred_Horizon[3,2]) + (rA_Mat[1,3] * rX_Pred_Horizon[3,3]) + (rA_Mat[1,4] * rX_Pred_Horizon[3,4]) + (rA_Mat[1,5] * rX_Pred_Horizon[3,5]) + (rA_Mat[1,6] * rX_Pred_Horizon[3,6]) + (rB_Mat[1,1] * rU_Opt_Seq[3,1]) + (rB_Mat[1,2] * rU_Opt_Seq[3,2]) + (rB_Mat[1,3] * rU_Opt_Seq[3,3]) + (rB_Mat[1,4] * rU_Opt_Seq[3,4]) + (rB_Mat[1,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[4, 2] := (rA_Mat[2,1] * rX_Pred_Horizon[3,1]) + (rA_Mat[2,2] * rX_Pred_Horizon[3,2]) + (rA_Mat[2,3] * rX_Pred_Horizon[3,3]) + (rA_Mat[2,4] * rX_Pred_Horizon[3,4]) + (rA_Mat[2,5] * rX_Pred_Horizon[3,5]) + (rA_Mat[2,6] * rX_Pred_Horizon[3,6]) + (rB_Mat[2,1] * rU_Opt_Seq[3,1]) + (rB_Mat[2,2] * rU_Opt_Seq[3,2]) + (rB_Mat[2,3] * rU_Opt_Seq[3,3]) + (rB_Mat[2,4] * rU_Opt_Seq[3,4]) + (rB_Mat[2,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[4, 3] := (rA_Mat[3,1] * rX_Pred_Horizon[3,1]) + (rA_Mat[3,2] * rX_Pred_Horizon[3,2]) + (rA_Mat[3,3] * rX_Pred_Horizon[3,3]) + (rA_Mat[3,4] * rX_Pred_Horizon[3,4]) + (rA_Mat[3,5] * rX_Pred_Horizon[3,5]) + (rA_Mat[3,6] * rX_Pred_Horizon[3,6]) + (rB_Mat[3,1] * rU_Opt_Seq[3,1]) + (rB_Mat[3,2] * rU_Opt_Seq[3,2]) + (rB_Mat[3,3] * rU_Opt_Seq[3,3]) + (rB_Mat[3,4] * rU_Opt_Seq[3,4]) + (rB_Mat[3,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[4, 4] := (rA_Mat[4,1] * rX_Pred_Horizon[3,1]) + (rA_Mat[4,2] * rX_Pred_Horizon[3,2]) + (rA_Mat[4,3] * rX_Pred_Horizon[3,3]) + (rA_Mat[4,4] * rX_Pred_Horizon[3,4]) + (rA_Mat[4,5] * rX_Pred_Horizon[3,5]) + (rA_Mat[4,6] * rX_Pred_Horizon[3,6]) + (rB_Mat[4,1] * rU_Opt_Seq[3,1]) + (rB_Mat[4,2] * rU_Opt_Seq[3,2]) + (rB_Mat[4,3] * rU_Opt_Seq[3,3]) + (rB_Mat[4,4] * rU_Opt_Seq[3,4]) + (rB_Mat[4,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[4, 5] := (rA_Mat[5,1] * rX_Pred_Horizon[3,1]) + (rA_Mat[5,2] * rX_Pred_Horizon[3,2]) + (rA_Mat[5,3] * rX_Pred_Horizon[3,3]) + (rA_Mat[5,4] * rX_Pred_Horizon[3,4]) + (rA_Mat[5,5] * rX_Pred_Horizon[3,5]) + (rA_Mat[5,6] * rX_Pred_Horizon[3,6]) + (rB_Mat[5,1] * rU_Opt_Seq[3,1]) + (rB_Mat[5,2] * rU_Opt_Seq[3,2]) + (rB_Mat[5,3] * rU_Opt_Seq[3,3]) + (rB_Mat[5,4] * rU_Opt_Seq[3,4]) + (rB_Mat[5,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[4, 6] := (rA_Mat[6,1] * rX_Pred_Horizon[3,1]) + (rA_Mat[6,2] * rX_Pred_Horizon[3,2]) + (rA_Mat[6,3] * rX_Pred_Horizon[3,3]) + (rA_Mat[6,4] * rX_Pred_Horizon[3,4]) + (rA_Mat[6,5] * rX_Pred_Horizon[3,5]) + (rA_Mat[6,6] * rX_Pred_Horizon[3,6]) + (rB_Mat[6,1] * rU_Opt_Seq[3,1]) + (rB_Mat[6,2] * rU_Opt_Seq[3,2]) + (rB_Mat[6,3] * rU_Opt_Seq[3,3]) + (rB_Mat[6,4] * rU_Opt_Seq[3,4]) + (rB_Mat[6,5] * rU_Opt_Seq[3,5]);

(* Iteration 10 - Forward State Prediction Step 5 (h=5): x_5 = A * x_4 + B * u_3 (held beyond Hu) *)
rX_Pred_Horizon[5, 1] := (rA_Mat[1,1] * rX_Pred_Horizon[4,1]) + (rA_Mat[1,2] * rX_Pred_Horizon[4,2]) + (rA_Mat[1,3] * rX_Pred_Horizon[4,3]) + (rA_Mat[1,4] * rX_Pred_Horizon[4,4]) + (rA_Mat[1,5] * rX_Pred_Horizon[4,5]) + (rA_Mat[1,6] * rX_Pred_Horizon[4,6]) + (rB_Mat[1,1] * rU_Opt_Seq[3,1]) + (rB_Mat[1,2] * rU_Opt_Seq[3,2]) + (rB_Mat[1,3] * rU_Opt_Seq[3,3]) + (rB_Mat[1,4] * rU_Opt_Seq[3,4]) + (rB_Mat[1,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[5, 2] := (rA_Mat[2,1] * rX_Pred_Horizon[4,1]) + (rA_Mat[2,2] * rX_Pred_Horizon[4,2]) + (rA_Mat[2,3] * rX_Pred_Horizon[4,3]) + (rA_Mat[2,4] * rX_Pred_Horizon[4,4]) + (rA_Mat[2,5] * rX_Pred_Horizon[4,5]) + (rA_Mat[2,6] * rX_Pred_Horizon[4,6]) + (rB_Mat[2,1] * rU_Opt_Seq[3,1]) + (rB_Mat[2,2] * rU_Opt_Seq[3,2]) + (rB_Mat[2,3] * rU_Opt_Seq[3,3]) + (rB_Mat[2,4] * rU_Opt_Seq[3,4]) + (rB_Mat[2,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[5, 3] := (rA_Mat[3,1] * rX_Pred_Horizon[4,1]) + (rA_Mat[3,2] * rX_Pred_Horizon[4,2]) + (rA_Mat[3,3] * rX_Pred_Horizon[4,3]) + (rA_Mat[3,4] * rX_Pred_Horizon[4,4]) + (rA_Mat[3,5] * rX_Pred_Horizon[4,5]) + (rA_Mat[3,6] * rX_Pred_Horizon[4,6]) + (rB_Mat[3,1] * rU_Opt_Seq[3,1]) + (rB_Mat[3,2] * rU_Opt_Seq[3,2]) + (rB_Mat[3,3] * rU_Opt_Seq[3,3]) + (rB_Mat[3,4] * rU_Opt_Seq[3,4]) + (rB_Mat[3,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[5, 4] := (rA_Mat[4,1] * rX_Pred_Horizon[4,1]) + (rA_Mat[4,2] * rX_Pred_Horizon[4,2]) + (rA_Mat[4,3] * rX_Pred_Horizon[4,3]) + (rA_Mat[4,4] * rX_Pred_Horizon[4,4]) + (rA_Mat[4,5] * rX_Pred_Horizon[4,5]) + (rA_Mat[4,6] * rX_Pred_Horizon[4,6]) + (rB_Mat[4,1] * rU_Opt_Seq[3,1]) + (rB_Mat[4,2] * rU_Opt_Seq[3,2]) + (rB_Mat[4,3] * rU_Opt_Seq[3,3]) + (rB_Mat[4,4] * rU_Opt_Seq[3,4]) + (rB_Mat[4,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[5, 5] := (rA_Mat[5,1] * rX_Pred_Horizon[4,1]) + (rA_Mat[5,2] * rX_Pred_Horizon[4,2]) + (rA_Mat[5,3] * rX_Pred_Horizon[4,3]) + (rA_Mat[5,4] * rX_Pred_Horizon[4,4]) + (rA_Mat[5,5] * rX_Pred_Horizon[4,5]) + (rA_Mat[5,6] * rX_Pred_Horizon[4,6]) + (rB_Mat[5,1] * rU_Opt_Seq[3,1]) + (rB_Mat[5,2] * rU_Opt_Seq[3,2]) + (rB_Mat[5,3] * rU_Opt_Seq[3,3]) + (rB_Mat[5,4] * rU_Opt_Seq[3,4]) + (rB_Mat[5,5] * rU_Opt_Seq[3,5]);
rX_Pred_Horizon[5, 6] := (rA_Mat[6,1] * rX_Pred_Horizon[4,1]) + (rA_Mat[6,2] * rX_Pred_Horizon[4,2]) + (rA_Mat[6,3] * rX_Pred_Horizon[4,3]) + (rA_Mat[6,4] * rX_Pred_Horizon[4,4]) + (rA_Mat[6,5] * rX_Pred_Horizon[4,5]) + (rA_Mat[6,6] * rX_Pred_Horizon[4,6]) + (rB_Mat[6,1] * rU_Opt_Seq[3,1]) + (rB_Mat[6,2] * rU_Opt_Seq[3,2]) + (rB_Mat[6,3] * rU_Opt_Seq[3,3]) + (rB_Mat[6,4] * rU_Opt_Seq[3,4]) + (rB_Mat[6,5] * rU_Opt_Seq[3,5]);

(* Iteration 10 - Evaluate Objective Function Cost J *)
rMPC_Cost_J := 0.0;
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[1] * (rX_Pred_Horizon[1,1] - rX_Target[1,1]) * (rX_Pred_Horizon[1,1] - rX_Target[1,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[2] * (rX_Pred_Horizon[1,2] - rX_Target[1,2]) * (rX_Pred_Horizon[1,2] - rX_Target[1,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[3] * (rX_Pred_Horizon[1,3] - rX_Target[1,3]) * (rX_Pred_Horizon[1,3] - rX_Target[1,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[4] * (rX_Pred_Horizon[1,4] - rX_Target[1,4]) * (rX_Pred_Horizon[1,4] - rX_Target[1,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[5] * (rX_Pred_Horizon[1,5] - rX_Target[1,5]) * (rX_Pred_Horizon[1,5] - rX_Target[1,5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[6] * (rX_Pred_Horizon[1,6] - rX_Target[1,6]) * (rX_Pred_Horizon[1,6] - rX_Target[1,6]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[1] * (rX_Pred_Horizon[2,1] - rX_Target[2,1]) * (rX_Pred_Horizon[2,1] - rX_Target[2,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[2] * (rX_Pred_Horizon[2,2] - rX_Target[2,2]) * (rX_Pred_Horizon[2,2] - rX_Target[2,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[3] * (rX_Pred_Horizon[2,3] - rX_Target[2,3]) * (rX_Pred_Horizon[2,3] - rX_Target[2,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[4] * (rX_Pred_Horizon[2,4] - rX_Target[2,4]) * (rX_Pred_Horizon[2,4] - rX_Target[2,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[5] * (rX_Pred_Horizon[2,5] - rX_Target[2,5]) * (rX_Pred_Horizon[2,5] - rX_Target[2,5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[6] * (rX_Pred_Horizon[2,6] - rX_Target[2,6]) * (rX_Pred_Horizon[2,6] - rX_Target[2,6]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[1] * (rX_Pred_Horizon[3,1] - rX_Target[3,1]) * (rX_Pred_Horizon[3,1] - rX_Target[3,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[2] * (rX_Pred_Horizon[3,2] - rX_Target[3,2]) * (rX_Pred_Horizon[3,2] - rX_Target[3,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[3] * (rX_Pred_Horizon[3,3] - rX_Target[3,3]) * (rX_Pred_Horizon[3,3] - rX_Target[3,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[4] * (rX_Pred_Horizon[3,4] - rX_Target[3,4]) * (rX_Pred_Horizon[3,4] - rX_Target[3,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[5] * (rX_Pred_Horizon[3,5] - rX_Target[3,5]) * (rX_Pred_Horizon[3,5] - rX_Target[3,5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[6] * (rX_Pred_Horizon[3,6] - rX_Target[3,6]) * (rX_Pred_Horizon[3,6] - rX_Target[3,6]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[1] * (rX_Pred_Horizon[4,1] - rX_Target[4,1]) * (rX_Pred_Horizon[4,1] - rX_Target[4,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[2] * (rX_Pred_Horizon[4,2] - rX_Target[4,2]) * (rX_Pred_Horizon[4,2] - rX_Target[4,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[3] * (rX_Pred_Horizon[4,3] - rX_Target[4,3]) * (rX_Pred_Horizon[4,3] - rX_Target[4,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[4] * (rX_Pred_Horizon[4,4] - rX_Target[4,4]) * (rX_Pred_Horizon[4,4] - rX_Target[4,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[5] * (rX_Pred_Horizon[4,5] - rX_Target[4,5]) * (rX_Pred_Horizon[4,5] - rX_Target[4,5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[6] * (rX_Pred_Horizon[4,6] - rX_Target[4,6]) * (rX_Pred_Horizon[4,6] - rX_Target[4,6]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[1] * (rX_Pred_Horizon[5,1] - rX_Target[5,1]) * (rX_Pred_Horizon[5,1] - rX_Target[5,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[2] * (rX_Pred_Horizon[5,2] - rX_Target[5,2]) * (rX_Pred_Horizon[5,2] - rX_Target[5,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[3] * (rX_Pred_Horizon[5,3] - rX_Target[5,3]) * (rX_Pred_Horizon[5,3] - rX_Target[5,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[4] * (rX_Pred_Horizon[5,4] - rX_Target[5,4]) * (rX_Pred_Horizon[5,4] - rX_Target[5,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[5] * (rX_Pred_Horizon[5,5] - rX_Target[5,5]) * (rX_Pred_Horizon[5,5] - rX_Target[5,5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rQ_Diag[6] * (rX_Pred_Horizon[5,6] - rX_Target[5,6]) * (rX_Pred_Horizon[5,6] - rX_Target[5,6]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rP_Diag[1] * (rX_Pred_Horizon[5,1] - rX_Target[5,1]) * (rX_Pred_Horizon[5,1] - rX_Target[5,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rP_Diag[2] * (rX_Pred_Horizon[5,2] - rX_Target[5,2]) * (rX_Pred_Horizon[5,2] - rX_Target[5,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rP_Diag[3] * (rX_Pred_Horizon[5,3] - rX_Target[5,3]) * (rX_Pred_Horizon[5,3] - rX_Target[5,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rP_Diag[4] * (rX_Pred_Horizon[5,4] - rX_Target[5,4]) * (rX_Pred_Horizon[5,4] - rX_Target[5,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rP_Diag[5] * (rX_Pred_Horizon[5,5] - rX_Target[5,5]) * (rX_Pred_Horizon[5,5] - rX_Target[5,5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rP_Diag[6] * (rX_Pred_Horizon[5,6] - rX_Target[5,6]) * (rX_Pred_Horizon[5,6] - rX_Target[5,6]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[1] * rU_Opt_Seq[1,1] * rU_Opt_Seq[1,1]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[2] * rU_Opt_Seq[1,2] * rU_Opt_Seq[1,2]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[3] * rU_Opt_Seq[1,3] * rU_Opt_Seq[1,3]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[4] * rU_Opt_Seq[1,4] * rU_Opt_Seq[1,4]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[5] * rU_Opt_Seq[1,5] * rU_Opt_Seq[1,5]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[1] * rU_Opt_Seq[2,1] * rU_Opt_Seq[2,1]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[2] * rU_Opt_Seq[2,2] * rU_Opt_Seq[2,2]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[3] * rU_Opt_Seq[2,3] * rU_Opt_Seq[2,3]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[4] * rU_Opt_Seq[2,4] * rU_Opt_Seq[2,4]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[5] * rU_Opt_Seq[2,5] * rU_Opt_Seq[2,5]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[1] * rU_Opt_Seq[3,1] * rU_Opt_Seq[3,1]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[2] * rU_Opt_Seq[3,2] * rU_Opt_Seq[3,2]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[3] * rU_Opt_Seq[3,3] * rU_Opt_Seq[3,3]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[4] * rU_Opt_Seq[3,4] * rU_Opt_Seq[3,4]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rR_Diag[5] * rU_Opt_Seq[3,5] * rU_Opt_Seq[3,5]);
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[1] * (rU_Opt_Seq[1,1] - a_u_prev[1]) * (rU_Opt_Seq[1,1] - a_u_prev[1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[1] * (rU_Opt_Seq[2,1] - rU_Opt_Seq[1,1]) * (rU_Opt_Seq[2,1] - rU_Opt_Seq[1,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[1] * (rU_Opt_Seq[3,1] - rU_Opt_Seq[2,1]) * (rU_Opt_Seq[3,1] - rU_Opt_Seq[2,1]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[2] * (rU_Opt_Seq[1,2] - a_u_prev[2]) * (rU_Opt_Seq[1,2] - a_u_prev[2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[2] * (rU_Opt_Seq[2,2] - rU_Opt_Seq[1,2]) * (rU_Opt_Seq[2,2] - rU_Opt_Seq[1,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[2] * (rU_Opt_Seq[3,2] - rU_Opt_Seq[2,2]) * (rU_Opt_Seq[3,2] - rU_Opt_Seq[2,2]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[3] * (rU_Opt_Seq[1,3] - a_u_prev[3]) * (rU_Opt_Seq[1,3] - a_u_prev[3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[3] * (rU_Opt_Seq[2,3] - rU_Opt_Seq[1,3]) * (rU_Opt_Seq[2,3] - rU_Opt_Seq[1,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[3] * (rU_Opt_Seq[3,3] - rU_Opt_Seq[2,3]) * (rU_Opt_Seq[3,3] - rU_Opt_Seq[2,3]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[4] * (rU_Opt_Seq[1,4] - a_u_prev[4]) * (rU_Opt_Seq[1,4] - a_u_prev[4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[4] * (rU_Opt_Seq[2,4] - rU_Opt_Seq[1,4]) * (rU_Opt_Seq[2,4] - rU_Opt_Seq[1,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[4] * (rU_Opt_Seq[3,4] - rU_Opt_Seq[2,4]) * (rU_Opt_Seq[3,4] - rU_Opt_Seq[2,4]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[5] * (rU_Opt_Seq[1,5] - a_u_prev[5]) * (rU_Opt_Seq[1,5] - a_u_prev[5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[5] * (rU_Opt_Seq[2,5] - rU_Opt_Seq[1,5]) * (rU_Opt_Seq[2,5] - rU_Opt_Seq[1,5]));
rMPC_Cost_J := rMPC_Cost_J + (0.5 * rS_Diag[5] * (rU_Opt_Seq[3,5] - rU_Opt_Seq[2,5]) * (rU_Opt_Seq[3,5] - rU_Opt_Seq[2,5]));

(* Iteration 10 - Backward Adjoint Costate Propagation: lambda_h = A^T * lambda_{h+1} + Q * (x_h - x_ref) *)
(* Terminal Costate at h=5: lambda_5 = (P + Q) * (x_5 - x_target_5) *)
rLambda_Costate[5, 1] := (rP_Diag[1] + rQ_Diag[1]) * (rX_Pred_Horizon[5,1] - rX_Target[5,1]);
rLambda_Costate[5, 2] := (rP_Diag[2] + rQ_Diag[2]) * (rX_Pred_Horizon[5,2] - rX_Target[5,2]);
rLambda_Costate[5, 3] := (rP_Diag[3] + rQ_Diag[3]) * (rX_Pred_Horizon[5,3] - rX_Target[5,3]);
rLambda_Costate[5, 4] := (rP_Diag[4] + rQ_Diag[4]) * (rX_Pred_Horizon[5,4] - rX_Target[5,4]);
rLambda_Costate[5, 5] := (rP_Diag[5] + rQ_Diag[5]) * (rX_Pred_Horizon[5,5] - rX_Target[5,5]);
rLambda_Costate[5, 6] := (rP_Diag[6] + rQ_Diag[6]) * (rX_Pred_Horizon[5,6] - rX_Target[5,6]);

(* Adjoint Costate at h=4: lambda_4 = A^T * lambda_5 + Q * (x_4 - x_target_4) *)
rLambda_Costate[4, 1] := (rA_Mat[1,1] * rLambda_Costate[5,1]) + (rA_Mat[2,1] * rLambda_Costate[5,2]) + (rA_Mat[3,1] * rLambda_Costate[5,3]) + (rA_Mat[4,1] * rLambda_Costate[5,4]) + (rA_Mat[5,1] * rLambda_Costate[5,5]) + (rA_Mat[6,1] * rLambda_Costate[5,6]) + (rQ_Diag[1] * (rX_Pred_Horizon[4,1] - rX_Target[4,1]));
rLambda_Costate[4, 2] := (rA_Mat[1,2] * rLambda_Costate[5,1]) + (rA_Mat[2,2] * rLambda_Costate[5,2]) + (rA_Mat[3,2] * rLambda_Costate[5,3]) + (rA_Mat[4,2] * rLambda_Costate[5,4]) + (rA_Mat[5,2] * rLambda_Costate[5,5]) + (rA_Mat[6,2] * rLambda_Costate[5,6]) + (rQ_Diag[2] * (rX_Pred_Horizon[4,2] - rX_Target[4,2]));
rLambda_Costate[4, 3] := (rA_Mat[1,3] * rLambda_Costate[5,1]) + (rA_Mat[2,3] * rLambda_Costate[5,2]) + (rA_Mat[3,3] * rLambda_Costate[5,3]) + (rA_Mat[4,3] * rLambda_Costate[5,4]) + (rA_Mat[5,3] * rLambda_Costate[5,5]) + (rA_Mat[6,3] * rLambda_Costate[5,6]) + (rQ_Diag[3] * (rX_Pred_Horizon[4,3] - rX_Target[4,3]));
rLambda_Costate[4, 4] := (rA_Mat[1,4] * rLambda_Costate[5,1]) + (rA_Mat[2,4] * rLambda_Costate[5,2]) + (rA_Mat[3,4] * rLambda_Costate[5,3]) + (rA_Mat[4,4] * rLambda_Costate[5,4]) + (rA_Mat[5,4] * rLambda_Costate[5,5]) + (rA_Mat[6,4] * rLambda_Costate[5,6]) + (rQ_Diag[4] * (rX_Pred_Horizon[4,4] - rX_Target[4,4]));
rLambda_Costate[4, 5] := (rA_Mat[1,5] * rLambda_Costate[5,1]) + (rA_Mat[2,5] * rLambda_Costate[5,2]) + (rA_Mat[3,5] * rLambda_Costate[5,3]) + (rA_Mat[4,5] * rLambda_Costate[5,4]) + (rA_Mat[5,5] * rLambda_Costate[5,5]) + (rA_Mat[6,5] * rLambda_Costate[5,6]) + (rQ_Diag[5] * (rX_Pred_Horizon[4,5] - rX_Target[4,5]));
rLambda_Costate[4, 6] := (rA_Mat[1,6] * rLambda_Costate[5,1]) + (rA_Mat[2,6] * rLambda_Costate[5,2]) + (rA_Mat[3,6] * rLambda_Costate[5,3]) + (rA_Mat[4,6] * rLambda_Costate[5,4]) + (rA_Mat[5,6] * rLambda_Costate[5,5]) + (rA_Mat[6,6] * rLambda_Costate[5,6]) + (rQ_Diag[6] * (rX_Pred_Horizon[4,6] - rX_Target[4,6]));

(* Adjoint Costate at h=3: lambda_3 = A^T * lambda_4 + Q * (x_3 - x_target_3) *)
rLambda_Costate[3, 1] := (rA_Mat[1,1] * rLambda_Costate[4,1]) + (rA_Mat[2,1] * rLambda_Costate[4,2]) + (rA_Mat[3,1] * rLambda_Costate[4,3]) + (rA_Mat[4,1] * rLambda_Costate[4,4]) + (rA_Mat[5,1] * rLambda_Costate[4,5]) + (rA_Mat[6,1] * rLambda_Costate[4,6]) + (rQ_Diag[1] * (rX_Pred_Horizon[3,1] - rX_Target[3,1]));
rLambda_Costate[3, 2] := (rA_Mat[1,2] * rLambda_Costate[4,1]) + (rA_Mat[2,2] * rLambda_Costate[4,2]) + (rA_Mat[3,2] * rLambda_Costate[4,3]) + (rA_Mat[4,2] * rLambda_Costate[4,4]) + (rA_Mat[5,2] * rLambda_Costate[4,5]) + (rA_Mat[6,2] * rLambda_Costate[4,6]) + (rQ_Diag[2] * (rX_Pred_Horizon[3,2] - rX_Target[3,2]));
rLambda_Costate[3, 3] := (rA_Mat[1,3] * rLambda_Costate[4,1]) + (rA_Mat[2,3] * rLambda_Costate[4,2]) + (rA_Mat[3,3] * rLambda_Costate[4,3]) + (rA_Mat[4,3] * rLambda_Costate[4,4]) + (rA_Mat[5,3] * rLambda_Costate[4,5]) + (rA_Mat[6,3] * rLambda_Costate[4,6]) + (rQ_Diag[3] * (rX_Pred_Horizon[3,3] - rX_Target[3,3]));
rLambda_Costate[3, 4] := (rA_Mat[1,4] * rLambda_Costate[4,1]) + (rA_Mat[2,4] * rLambda_Costate[4,2]) + (rA_Mat[3,4] * rLambda_Costate[4,3]) + (rA_Mat[4,4] * rLambda_Costate[4,4]) + (rA_Mat[5,4] * rLambda_Costate[4,5]) + (rA_Mat[6,4] * rLambda_Costate[4,6]) + (rQ_Diag[4] * (rX_Pred_Horizon[3,4] - rX_Target[3,4]));
rLambda_Costate[3, 5] := (rA_Mat[1,5] * rLambda_Costate[4,1]) + (rA_Mat[2,5] * rLambda_Costate[4,2]) + (rA_Mat[3,5] * rLambda_Costate[4,3]) + (rA_Mat[4,5] * rLambda_Costate[4,4]) + (rA_Mat[5,5] * rLambda_Costate[4,5]) + (rA_Mat[6,5] * rLambda_Costate[4,6]) + (rQ_Diag[5] * (rX_Pred_Horizon[3,5] - rX_Target[3,5]));
rLambda_Costate[3, 6] := (rA_Mat[1,6] * rLambda_Costate[4,1]) + (rA_Mat[2,6] * rLambda_Costate[4,2]) + (rA_Mat[3,6] * rLambda_Costate[4,3]) + (rA_Mat[4,6] * rLambda_Costate[4,4]) + (rA_Mat[5,6] * rLambda_Costate[4,5]) + (rA_Mat[6,6] * rLambda_Costate[4,6]) + (rQ_Diag[6] * (rX_Pred_Horizon[3,6] - rX_Target[3,6]));

(* Adjoint Costate at h=2: lambda_2 = A^T * lambda_3 + Q * (x_2 - x_target_2) *)
rLambda_Costate[2, 1] := (rA_Mat[1,1] * rLambda_Costate[3,1]) + (rA_Mat[2,1] * rLambda_Costate[3,2]) + (rA_Mat[3,1] * rLambda_Costate[3,3]) + (rA_Mat[4,1] * rLambda_Costate[3,4]) + (rA_Mat[5,1] * rLambda_Costate[3,5]) + (rA_Mat[6,1] * rLambda_Costate[3,6]) + (rQ_Diag[1] * (rX_Pred_Horizon[2,1] - rX_Target[2,1]));
rLambda_Costate[2, 2] := (rA_Mat[1,2] * rLambda_Costate[3,1]) + (rA_Mat[2,2] * rLambda_Costate[3,2]) + (rA_Mat[3,2] * rLambda_Costate[3,3]) + (rA_Mat[4,2] * rLambda_Costate[3,4]) + (rA_Mat[5,2] * rLambda_Costate[3,5]) + (rA_Mat[6,2] * rLambda_Costate[3,6]) + (rQ_Diag[2] * (rX_Pred_Horizon[2,2] - rX_Target[2,2]));
rLambda_Costate[2, 3] := (rA_Mat[1,3] * rLambda_Costate[3,1]) + (rA_Mat[2,3] * rLambda_Costate[3,2]) + (rA_Mat[3,3] * rLambda_Costate[3,3]) + (rA_Mat[4,3] * rLambda_Costate[3,4]) + (rA_Mat[5,3] * rLambda_Costate[3,5]) + (rA_Mat[6,3] * rLambda_Costate[3,6]) + (rQ_Diag[3] * (rX_Pred_Horizon[2,3] - rX_Target[2,3]));
rLambda_Costate[2, 4] := (rA_Mat[1,4] * rLambda_Costate[3,1]) + (rA_Mat[2,4] * rLambda_Costate[3,2]) + (rA_Mat[3,4] * rLambda_Costate[3,3]) + (rA_Mat[4,4] * rLambda_Costate[3,4]) + (rA_Mat[5,4] * rLambda_Costate[3,5]) + (rA_Mat[6,4] * rLambda_Costate[3,6]) + (rQ_Diag[4] * (rX_Pred_Horizon[2,4] - rX_Target[2,4]));
rLambda_Costate[2, 5] := (rA_Mat[1,5] * rLambda_Costate[3,1]) + (rA_Mat[2,5] * rLambda_Costate[3,2]) + (rA_Mat[3,5] * rLambda_Costate[3,3]) + (rA_Mat[4,5] * rLambda_Costate[3,4]) + (rA_Mat[5,5] * rLambda_Costate[3,5]) + (rA_Mat[6,5] * rLambda_Costate[3,6]) + (rQ_Diag[5] * (rX_Pred_Horizon[2,5] - rX_Target[2,5]));
rLambda_Costate[2, 6] := (rA_Mat[1,6] * rLambda_Costate[3,1]) + (rA_Mat[2,6] * rLambda_Costate[3,2]) + (rA_Mat[3,6] * rLambda_Costate[3,3]) + (rA_Mat[4,6] * rLambda_Costate[3,4]) + (rA_Mat[5,6] * rLambda_Costate[3,5]) + (rA_Mat[6,6] * rLambda_Costate[3,6]) + (rQ_Diag[6] * (rX_Pred_Horizon[2,6] - rX_Target[2,6]));

(* Adjoint Costate at h=1: lambda_1 = A^T * lambda_2 + Q * (x_1 - x_target_1) *)
rLambda_Costate[1, 1] := (rA_Mat[1,1] * rLambda_Costate[2,1]) + (rA_Mat[2,1] * rLambda_Costate[2,2]) + (rA_Mat[3,1] * rLambda_Costate[2,3]) + (rA_Mat[4,1] * rLambda_Costate[2,4]) + (rA_Mat[5,1] * rLambda_Costate[2,5]) + (rA_Mat[6,1] * rLambda_Costate[2,6]) + (rQ_Diag[1] * (rX_Pred_Horizon[1,1] - rX_Target[1,1]));
rLambda_Costate[1, 2] := (rA_Mat[1,2] * rLambda_Costate[2,1]) + (rA_Mat[2,2] * rLambda_Costate[2,2]) + (rA_Mat[3,2] * rLambda_Costate[2,3]) + (rA_Mat[4,2] * rLambda_Costate[2,4]) + (rA_Mat[5,2] * rLambda_Costate[2,5]) + (rA_Mat[6,2] * rLambda_Costate[2,6]) + (rQ_Diag[2] * (rX_Pred_Horizon[1,2] - rX_Target[1,2]));
rLambda_Costate[1, 3] := (rA_Mat[1,3] * rLambda_Costate[2,1]) + (rA_Mat[2,3] * rLambda_Costate[2,2]) + (rA_Mat[3,3] * rLambda_Costate[2,3]) + (rA_Mat[4,3] * rLambda_Costate[2,4]) + (rA_Mat[5,3] * rLambda_Costate[2,5]) + (rA_Mat[6,3] * rLambda_Costate[2,6]) + (rQ_Diag[3] * (rX_Pred_Horizon[1,3] - rX_Target[1,3]));
rLambda_Costate[1, 4] := (rA_Mat[1,4] * rLambda_Costate[2,1]) + (rA_Mat[2,4] * rLambda_Costate[2,2]) + (rA_Mat[3,4] * rLambda_Costate[2,3]) + (rA_Mat[4,4] * rLambda_Costate[2,4]) + (rA_Mat[5,4] * rLambda_Costate[2,5]) + (rA_Mat[6,4] * rLambda_Costate[2,6]) + (rQ_Diag[4] * (rX_Pred_Horizon[1,4] - rX_Target[1,4]));
rLambda_Costate[1, 5] := (rA_Mat[1,5] * rLambda_Costate[2,1]) + (rA_Mat[2,5] * rLambda_Costate[2,2]) + (rA_Mat[3,5] * rLambda_Costate[2,3]) + (rA_Mat[4,5] * rLambda_Costate[2,4]) + (rA_Mat[5,5] * rLambda_Costate[2,5]) + (rA_Mat[6,5] * rLambda_Costate[2,6]) + (rQ_Diag[5] * (rX_Pred_Horizon[1,5] - rX_Target[1,5]));
rLambda_Costate[1, 6] := (rA_Mat[1,6] * rLambda_Costate[2,1]) + (rA_Mat[2,6] * rLambda_Costate[2,2]) + (rA_Mat[3,6] * rLambda_Costate[2,3]) + (rA_Mat[4,6] * rLambda_Costate[2,4]) + (rA_Mat[5,6] * rLambda_Costate[2,5]) + (rA_Mat[6,6] * rLambda_Costate[2,6]) + (rQ_Diag[6] * (rX_Pred_Horizon[1,6] - rX_Target[1,6]));

(* Iteration 10 - Analytical Gradient Computation w.r.t. Control Inputs u_h *)
rMPC_GradNormSq := 0.0;
(* Gradient for u_1 (h=1) *)
rGrad_J[1, 1] := (rB_Mat[1,1] * rLambda_Costate[1,1]) + (rB_Mat[2,1] * rLambda_Costate[1,2]) + (rB_Mat[3,1] * rLambda_Costate[1,3]) + (rB_Mat[4,1] * rLambda_Costate[1,4]) + (rB_Mat[5,1] * rLambda_Costate[1,5]) + (rB_Mat[6,1] * rLambda_Costate[1,6]) + (rR_Diag[1] * rU_Opt_Seq[1,1]) + (rS_Diag[1] * (rU_Opt_Seq[1,1] - a_u_prev[1])) - (rS_Diag[1] * (rU_Opt_Seq[2,1] - rU_Opt_Seq[1,1]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[1, 1] * rGrad_J[1, 1]);
rGrad_J[1, 2] := (rB_Mat[1,2] * rLambda_Costate[1,1]) + (rB_Mat[2,2] * rLambda_Costate[1,2]) + (rB_Mat[3,2] * rLambda_Costate[1,3]) + (rB_Mat[4,2] * rLambda_Costate[1,4]) + (rB_Mat[5,2] * rLambda_Costate[1,5]) + (rB_Mat[6,2] * rLambda_Costate[1,6]) + (rR_Diag[2] * rU_Opt_Seq[1,2]) + (rS_Diag[2] * (rU_Opt_Seq[1,2] - a_u_prev[2])) - (rS_Diag[2] * (rU_Opt_Seq[2,2] - rU_Opt_Seq[1,2]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[1, 2] * rGrad_J[1, 2]);
rGrad_J[1, 3] := (rB_Mat[1,3] * rLambda_Costate[1,1]) + (rB_Mat[2,3] * rLambda_Costate[1,2]) + (rB_Mat[3,3] * rLambda_Costate[1,3]) + (rB_Mat[4,3] * rLambda_Costate[1,4]) + (rB_Mat[5,3] * rLambda_Costate[1,5]) + (rB_Mat[6,3] * rLambda_Costate[1,6]) + (rR_Diag[3] * rU_Opt_Seq[1,3]) + (rS_Diag[3] * (rU_Opt_Seq[1,3] - a_u_prev[3])) - (rS_Diag[3] * (rU_Opt_Seq[2,3] - rU_Opt_Seq[1,3]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[1, 3] * rGrad_J[1, 3]);
rGrad_J[1, 4] := (rB_Mat[1,4] * rLambda_Costate[1,1]) + (rB_Mat[2,4] * rLambda_Costate[1,2]) + (rB_Mat[3,4] * rLambda_Costate[1,3]) + (rB_Mat[4,4] * rLambda_Costate[1,4]) + (rB_Mat[5,4] * rLambda_Costate[1,5]) + (rB_Mat[6,4] * rLambda_Costate[1,6]) + (rR_Diag[4] * rU_Opt_Seq[1,4]) + (rS_Diag[4] * (rU_Opt_Seq[1,4] - a_u_prev[4])) - (rS_Diag[4] * (rU_Opt_Seq[2,4] - rU_Opt_Seq[1,4]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[1, 4] * rGrad_J[1, 4]);
rGrad_J[1, 5] := (rB_Mat[1,5] * rLambda_Costate[1,1]) + (rB_Mat[2,5] * rLambda_Costate[1,2]) + (rB_Mat[3,5] * rLambda_Costate[1,3]) + (rB_Mat[4,5] * rLambda_Costate[1,4]) + (rB_Mat[5,5] * rLambda_Costate[1,5]) + (rB_Mat[6,5] * rLambda_Costate[1,6]) + (rR_Diag[5] * rU_Opt_Seq[1,5]) + (rS_Diag[5] * (rU_Opt_Seq[1,5] - a_u_prev[5])) - (rS_Diag[5] * (rU_Opt_Seq[2,5] - rU_Opt_Seq[1,5]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[1, 5] * rGrad_J[1, 5]);

(* Gradient for u_2 (h=2) *)
rGrad_J[2, 1] := (rB_Mat[1,1] * rLambda_Costate[2,1]) + (rB_Mat[2,1] * rLambda_Costate[2,2]) + (rB_Mat[3,1] * rLambda_Costate[2,3]) + (rB_Mat[4,1] * rLambda_Costate[2,4]) + (rB_Mat[5,1] * rLambda_Costate[2,5]) + (rB_Mat[6,1] * rLambda_Costate[2,6]) + (rR_Diag[1] * rU_Opt_Seq[2,1]) + (rS_Diag[1] * (rU_Opt_Seq[2,1] - rU_Opt_Seq[1,1])) - (rS_Diag[1] * (rU_Opt_Seq[3,1] - rU_Opt_Seq[2,1]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[2, 1] * rGrad_J[2, 1]);
rGrad_J[2, 2] := (rB_Mat[1,2] * rLambda_Costate[2,1]) + (rB_Mat[2,2] * rLambda_Costate[2,2]) + (rB_Mat[3,2] * rLambda_Costate[2,3]) + (rB_Mat[4,2] * rLambda_Costate[2,4]) + (rB_Mat[5,2] * rLambda_Costate[2,5]) + (rB_Mat[6,2] * rLambda_Costate[2,6]) + (rR_Diag[2] * rU_Opt_Seq[2,2]) + (rS_Diag[2] * (rU_Opt_Seq[2,2] - rU_Opt_Seq[1,2])) - (rS_Diag[2] * (rU_Opt_Seq[3,2] - rU_Opt_Seq[2,2]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[2, 2] * rGrad_J[2, 2]);
rGrad_J[2, 3] := (rB_Mat[1,3] * rLambda_Costate[2,1]) + (rB_Mat[2,3] * rLambda_Costate[2,2]) + (rB_Mat[3,3] * rLambda_Costate[2,3]) + (rB_Mat[4,3] * rLambda_Costate[2,4]) + (rB_Mat[5,3] * rLambda_Costate[2,5]) + (rB_Mat[6,3] * rLambda_Costate[2,6]) + (rR_Diag[3] * rU_Opt_Seq[2,3]) + (rS_Diag[3] * (rU_Opt_Seq[2,3] - rU_Opt_Seq[1,3])) - (rS_Diag[3] * (rU_Opt_Seq[3,3] - rU_Opt_Seq[2,3]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[2, 3] * rGrad_J[2, 3]);
rGrad_J[2, 4] := (rB_Mat[1,4] * rLambda_Costate[2,1]) + (rB_Mat[2,4] * rLambda_Costate[2,2]) + (rB_Mat[3,4] * rLambda_Costate[2,3]) + (rB_Mat[4,4] * rLambda_Costate[2,4]) + (rB_Mat[5,4] * rLambda_Costate[2,5]) + (rB_Mat[6,4] * rLambda_Costate[2,6]) + (rR_Diag[4] * rU_Opt_Seq[2,4]) + (rS_Diag[4] * (rU_Opt_Seq[2,4] - rU_Opt_Seq[1,4])) - (rS_Diag[4] * (rU_Opt_Seq[3,4] - rU_Opt_Seq[2,4]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[2, 4] * rGrad_J[2, 4]);
rGrad_J[2, 5] := (rB_Mat[1,5] * rLambda_Costate[2,1]) + (rB_Mat[2,5] * rLambda_Costate[2,2]) + (rB_Mat[3,5] * rLambda_Costate[2,3]) + (rB_Mat[4,5] * rLambda_Costate[2,4]) + (rB_Mat[5,5] * rLambda_Costate[2,5]) + (rB_Mat[6,5] * rLambda_Costate[2,6]) + (rR_Diag[5] * rU_Opt_Seq[2,5]) + (rS_Diag[5] * (rU_Opt_Seq[2,5] - rU_Opt_Seq[1,5])) - (rS_Diag[5] * (rU_Opt_Seq[3,5] - rU_Opt_Seq[2,5]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[2, 5] * rGrad_J[2, 5]);

(* Gradient for u_3 (h=3, held through h=4, 5) *)
rGrad_J[3, 1] := (rB_Mat[1,1] * (rLambda_Costate[3,1] + rLambda_Costate[4,1] + rLambda_Costate[5,1])) + (rB_Mat[2,1] * (rLambda_Costate[3,2] + rLambda_Costate[4,2] + rLambda_Costate[5,2])) + (rB_Mat[3,1] * (rLambda_Costate[3,3] + rLambda_Costate[4,3] + rLambda_Costate[5,3])) + (rB_Mat[4,1] * (rLambda_Costate[3,4] + rLambda_Costate[4,4] + rLambda_Costate[5,4])) + (rB_Mat[5,1] * (rLambda_Costate[3,5] + rLambda_Costate[4,5] + rLambda_Costate[5,5])) + (rB_Mat[6,1] * (rLambda_Costate[3,6] + rLambda_Costate[4,6] + rLambda_Costate[5,6])) + (rR_Diag[1] * rU_Opt_Seq[3,1]) + (rS_Diag[1] * (rU_Opt_Seq[3,1] - rU_Opt_Seq[2,1]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[3, 1] * rGrad_J[3, 1]);
rGrad_J[3, 2] := (rB_Mat[1,2] * (rLambda_Costate[3,1] + rLambda_Costate[4,1] + rLambda_Costate[5,1])) + (rB_Mat[2,2] * (rLambda_Costate[3,2] + rLambda_Costate[4,2] + rLambda_Costate[5,2])) + (rB_Mat[3,2] * (rLambda_Costate[3,3] + rLambda_Costate[4,3] + rLambda_Costate[5,3])) + (rB_Mat[4,2] * (rLambda_Costate[3,4] + rLambda_Costate[4,4] + rLambda_Costate[5,4])) + (rB_Mat[5,2] * (rLambda_Costate[3,5] + rLambda_Costate[4,5] + rLambda_Costate[5,5])) + (rB_Mat[6,2] * (rLambda_Costate[3,6] + rLambda_Costate[4,6] + rLambda_Costate[5,6])) + (rR_Diag[2] * rU_Opt_Seq[3,2]) + (rS_Diag[2] * (rU_Opt_Seq[3,2] - rU_Opt_Seq[2,2]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[3, 2] * rGrad_J[3, 2]);
rGrad_J[3, 3] := (rB_Mat[1,3] * (rLambda_Costate[3,1] + rLambda_Costate[4,1] + rLambda_Costate[5,1])) + (rB_Mat[2,3] * (rLambda_Costate[3,2] + rLambda_Costate[4,2] + rLambda_Costate[5,2])) + (rB_Mat[3,3] * (rLambda_Costate[3,3] + rLambda_Costate[4,3] + rLambda_Costate[5,3])) + (rB_Mat[4,3] * (rLambda_Costate[3,4] + rLambda_Costate[4,4] + rLambda_Costate[5,4])) + (rB_Mat[5,3] * (rLambda_Costate[3,5] + rLambda_Costate[4,5] + rLambda_Costate[5,5])) + (rB_Mat[6,3] * (rLambda_Costate[3,6] + rLambda_Costate[4,6] + rLambda_Costate[5,6])) + (rR_Diag[3] * rU_Opt_Seq[3,3]) + (rS_Diag[3] * (rU_Opt_Seq[3,3] - rU_Opt_Seq[2,3]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[3, 3] * rGrad_J[3, 3]);
rGrad_J[3, 4] := (rB_Mat[1,4] * (rLambda_Costate[3,1] + rLambda_Costate[4,1] + rLambda_Costate[5,1])) + (rB_Mat[2,4] * (rLambda_Costate[3,2] + rLambda_Costate[4,2] + rLambda_Costate[5,2])) + (rB_Mat[3,4] * (rLambda_Costate[3,3] + rLambda_Costate[4,3] + rLambda_Costate[5,3])) + (rB_Mat[4,4] * (rLambda_Costate[3,4] + rLambda_Costate[4,4] + rLambda_Costate[5,4])) + (rB_Mat[5,4] * (rLambda_Costate[3,5] + rLambda_Costate[4,5] + rLambda_Costate[5,5])) + (rB_Mat[6,4] * (rLambda_Costate[3,6] + rLambda_Costate[4,6] + rLambda_Costate[5,6])) + (rR_Diag[4] * rU_Opt_Seq[3,4]) + (rS_Diag[4] * (rU_Opt_Seq[3,4] - rU_Opt_Seq[2,4]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[3, 4] * rGrad_J[3, 4]);
rGrad_J[3, 5] := (rB_Mat[1,5] * (rLambda_Costate[3,1] + rLambda_Costate[4,1] + rLambda_Costate[5,1])) + (rB_Mat[2,5] * (rLambda_Costate[3,2] + rLambda_Costate[4,2] + rLambda_Costate[5,2])) + (rB_Mat[3,5] * (rLambda_Costate[3,3] + rLambda_Costate[4,3] + rLambda_Costate[5,3])) + (rB_Mat[4,5] * (rLambda_Costate[3,4] + rLambda_Costate[4,4] + rLambda_Costate[5,4])) + (rB_Mat[5,5] * (rLambda_Costate[3,5] + rLambda_Costate[4,5] + rLambda_Costate[5,5])) + (rB_Mat[6,5] * (rLambda_Costate[3,6] + rLambda_Costate[4,6] + rLambda_Costate[5,6])) + (rR_Diag[5] * rU_Opt_Seq[3,5]) + (rS_Diag[5] * (rU_Opt_Seq[3,5] - rU_Opt_Seq[2,5]));
rMPC_GradNormSq := rMPC_GradNormSq + (rGrad_J[3, 5] * rGrad_J[3, 5]);

(* Iteration 10 - Projected Gradient Step with Hard Box & Dynamic Slew Limits *)
rTemp_Val := rU_Opt_Seq[1, 1] - (rAlpha_PGD_StepSize * rGrad_J[1, 1]);
(* Slew limit against prior actuator output *)
IF rTemp_Val > (a_u_prev[1] + rDeltaU_Max[1]) THEN
    rTemp_Val := a_u_prev[1] + rDeltaU_Max[1];
ELSIF rTemp_Val < (a_u_prev[1] - rDeltaU_Max[1]) THEN
    rTemp_Val := a_u_prev[1] - rDeltaU_Max[1];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[1] THEN
    rTemp_Val := rU_BoxMax[1];
ELSIF rTemp_Val < rU_BoxMin[1] THEN
    rTemp_Val := rU_BoxMin[1];
END_IF;
rU_Opt_Seq[1, 1] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[1, 2] - (rAlpha_PGD_StepSize * rGrad_J[1, 2]);
(* Slew limit against prior actuator output *)
IF rTemp_Val > (a_u_prev[2] + rDeltaU_Max[2]) THEN
    rTemp_Val := a_u_prev[2] + rDeltaU_Max[2];
ELSIF rTemp_Val < (a_u_prev[2] - rDeltaU_Max[2]) THEN
    rTemp_Val := a_u_prev[2] - rDeltaU_Max[2];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[2] THEN
    rTemp_Val := rU_BoxMax[2];
ELSIF rTemp_Val < rU_BoxMin[2] THEN
    rTemp_Val := rU_BoxMin[2];
END_IF;
rU_Opt_Seq[1, 2] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[1, 3] - (rAlpha_PGD_StepSize * rGrad_J[1, 3]);
(* Slew limit against prior actuator output *)
IF rTemp_Val > (a_u_prev[3] + rDeltaU_Max[3]) THEN
    rTemp_Val := a_u_prev[3] + rDeltaU_Max[3];
ELSIF rTemp_Val < (a_u_prev[3] - rDeltaU_Max[3]) THEN
    rTemp_Val := a_u_prev[3] - rDeltaU_Max[3];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[3] THEN
    rTemp_Val := rU_BoxMax[3];
ELSIF rTemp_Val < rU_BoxMin[3] THEN
    rTemp_Val := rU_BoxMin[3];
END_IF;
rU_Opt_Seq[1, 3] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[1, 4] - (rAlpha_PGD_StepSize * rGrad_J[1, 4]);
(* Slew limit against prior actuator output *)
IF rTemp_Val > (a_u_prev[4] + rDeltaU_Max[4]) THEN
    rTemp_Val := a_u_prev[4] + rDeltaU_Max[4];
ELSIF rTemp_Val < (a_u_prev[4] - rDeltaU_Max[4]) THEN
    rTemp_Val := a_u_prev[4] - rDeltaU_Max[4];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[4] THEN
    rTemp_Val := rU_BoxMax[4];
ELSIF rTemp_Val < rU_BoxMin[4] THEN
    rTemp_Val := rU_BoxMin[4];
END_IF;
rU_Opt_Seq[1, 4] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[1, 5] - (rAlpha_PGD_StepSize * rGrad_J[1, 5]);
(* Slew limit against prior actuator output *)
IF rTemp_Val > (a_u_prev[5] + rDeltaU_Max[5]) THEN
    rTemp_Val := a_u_prev[5] + rDeltaU_Max[5];
ELSIF rTemp_Val < (a_u_prev[5] - rDeltaU_Max[5]) THEN
    rTemp_Val := a_u_prev[5] - rDeltaU_Max[5];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[5] THEN
    rTemp_Val := rU_BoxMax[5];
ELSIF rTemp_Val < rU_BoxMin[5] THEN
    rTemp_Val := rU_BoxMin[5];
END_IF;
rU_Opt_Seq[1, 5] := rTemp_Val;

rTemp_Val := rU_Opt_Seq[2, 1] - (rAlpha_PGD_StepSize * rGrad_J[2, 1]);
(* Slew limit against step 1 *)
IF rTemp_Val > (rU_Opt_Seq[1, 1] + rDeltaU_Max[1]) THEN
    rTemp_Val := rU_Opt_Seq[1, 1] + rDeltaU_Max[1];
ELSIF rTemp_Val < (rU_Opt_Seq[1, 1] - rDeltaU_Max[1]) THEN
    rTemp_Val := rU_Opt_Seq[1, 1] - rDeltaU_Max[1];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[1] THEN
    rTemp_Val := rU_BoxMax[1];
ELSIF rTemp_Val < rU_BoxMin[1] THEN
    rTemp_Val := rU_BoxMin[1];
END_IF;
rU_Opt_Seq[2, 1] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[2, 2] - (rAlpha_PGD_StepSize * rGrad_J[2, 2]);
(* Slew limit against step 1 *)
IF rTemp_Val > (rU_Opt_Seq[1, 2] + rDeltaU_Max[2]) THEN
    rTemp_Val := rU_Opt_Seq[1, 2] + rDeltaU_Max[2];
ELSIF rTemp_Val < (rU_Opt_Seq[1, 2] - rDeltaU_Max[2]) THEN
    rTemp_Val := rU_Opt_Seq[1, 2] - rDeltaU_Max[2];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[2] THEN
    rTemp_Val := rU_BoxMax[2];
ELSIF rTemp_Val < rU_BoxMin[2] THEN
    rTemp_Val := rU_BoxMin[2];
END_IF;
rU_Opt_Seq[2, 2] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[2, 3] - (rAlpha_PGD_StepSize * rGrad_J[2, 3]);
(* Slew limit against step 1 *)
IF rTemp_Val > (rU_Opt_Seq[1, 3] + rDeltaU_Max[3]) THEN
    rTemp_Val := rU_Opt_Seq[1, 3] + rDeltaU_Max[3];
ELSIF rTemp_Val < (rU_Opt_Seq[1, 3] - rDeltaU_Max[3]) THEN
    rTemp_Val := rU_Opt_Seq[1, 3] - rDeltaU_Max[3];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[3] THEN
    rTemp_Val := rU_BoxMax[3];
ELSIF rTemp_Val < rU_BoxMin[3] THEN
    rTemp_Val := rU_BoxMin[3];
END_IF;
rU_Opt_Seq[2, 3] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[2, 4] - (rAlpha_PGD_StepSize * rGrad_J[2, 4]);
(* Slew limit against step 1 *)
IF rTemp_Val > (rU_Opt_Seq[1, 4] + rDeltaU_Max[4]) THEN
    rTemp_Val := rU_Opt_Seq[1, 4] + rDeltaU_Max[4];
ELSIF rTemp_Val < (rU_Opt_Seq[1, 4] - rDeltaU_Max[4]) THEN
    rTemp_Val := rU_Opt_Seq[1, 4] - rDeltaU_Max[4];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[4] THEN
    rTemp_Val := rU_BoxMax[4];
ELSIF rTemp_Val < rU_BoxMin[4] THEN
    rTemp_Val := rU_BoxMin[4];
END_IF;
rU_Opt_Seq[2, 4] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[2, 5] - (rAlpha_PGD_StepSize * rGrad_J[2, 5]);
(* Slew limit against step 1 *)
IF rTemp_Val > (rU_Opt_Seq[1, 5] + rDeltaU_Max[5]) THEN
    rTemp_Val := rU_Opt_Seq[1, 5] + rDeltaU_Max[5];
ELSIF rTemp_Val < (rU_Opt_Seq[1, 5] - rDeltaU_Max[5]) THEN
    rTemp_Val := rU_Opt_Seq[1, 5] - rDeltaU_Max[5];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[5] THEN
    rTemp_Val := rU_BoxMax[5];
ELSIF rTemp_Val < rU_BoxMin[5] THEN
    rTemp_Val := rU_BoxMin[5];
END_IF;
rU_Opt_Seq[2, 5] := rTemp_Val;

rTemp_Val := rU_Opt_Seq[3, 1] - (rAlpha_PGD_StepSize * rGrad_J[3, 1]);
(* Slew limit against step 2 *)
IF rTemp_Val > (rU_Opt_Seq[2, 1] + rDeltaU_Max[1]) THEN
    rTemp_Val := rU_Opt_Seq[2, 1] + rDeltaU_Max[1];
ELSIF rTemp_Val < (rU_Opt_Seq[2, 1] - rDeltaU_Max[1]) THEN
    rTemp_Val := rU_Opt_Seq[2, 1] - rDeltaU_Max[1];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[1] THEN
    rTemp_Val := rU_BoxMax[1];
ELSIF rTemp_Val < rU_BoxMin[1] THEN
    rTemp_Val := rU_BoxMin[1];
END_IF;
rU_Opt_Seq[3, 1] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[3, 2] - (rAlpha_PGD_StepSize * rGrad_J[3, 2]);
(* Slew limit against step 2 *)
IF rTemp_Val > (rU_Opt_Seq[2, 2] + rDeltaU_Max[2]) THEN
    rTemp_Val := rU_Opt_Seq[2, 2] + rDeltaU_Max[2];
ELSIF rTemp_Val < (rU_Opt_Seq[2, 2] - rDeltaU_Max[2]) THEN
    rTemp_Val := rU_Opt_Seq[2, 2] - rDeltaU_Max[2];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[2] THEN
    rTemp_Val := rU_BoxMax[2];
ELSIF rTemp_Val < rU_BoxMin[2] THEN
    rTemp_Val := rU_BoxMin[2];
END_IF;
rU_Opt_Seq[3, 2] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[3, 3] - (rAlpha_PGD_StepSize * rGrad_J[3, 3]);
(* Slew limit against step 2 *)
IF rTemp_Val > (rU_Opt_Seq[2, 3] + rDeltaU_Max[3]) THEN
    rTemp_Val := rU_Opt_Seq[2, 3] + rDeltaU_Max[3];
ELSIF rTemp_Val < (rU_Opt_Seq[2, 3] - rDeltaU_Max[3]) THEN
    rTemp_Val := rU_Opt_Seq[2, 3] - rDeltaU_Max[3];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[3] THEN
    rTemp_Val := rU_BoxMax[3];
ELSIF rTemp_Val < rU_BoxMin[3] THEN
    rTemp_Val := rU_BoxMin[3];
END_IF;
rU_Opt_Seq[3, 3] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[3, 4] - (rAlpha_PGD_StepSize * rGrad_J[3, 4]);
(* Slew limit against step 2 *)
IF rTemp_Val > (rU_Opt_Seq[2, 4] + rDeltaU_Max[4]) THEN
    rTemp_Val := rU_Opt_Seq[2, 4] + rDeltaU_Max[4];
ELSIF rTemp_Val < (rU_Opt_Seq[2, 4] - rDeltaU_Max[4]) THEN
    rTemp_Val := rU_Opt_Seq[2, 4] - rDeltaU_Max[4];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[4] THEN
    rTemp_Val := rU_BoxMax[4];
ELSIF rTemp_Val < rU_BoxMin[4] THEN
    rTemp_Val := rU_BoxMin[4];
END_IF;
rU_Opt_Seq[3, 4] := rTemp_Val;
rTemp_Val := rU_Opt_Seq[3, 5] - (rAlpha_PGD_StepSize * rGrad_J[3, 5]);
(* Slew limit against step 2 *)
IF rTemp_Val > (rU_Opt_Seq[2, 5] + rDeltaU_Max[5]) THEN
    rTemp_Val := rU_Opt_Seq[2, 5] + rDeltaU_Max[5];
ELSIF rTemp_Val < (rU_Opt_Seq[2, 5] - rDeltaU_Max[5]) THEN
    rTemp_Val := rU_Opt_Seq[2, 5] - rDeltaU_Max[5];
END_IF;
(* Box constraints *)
IF rTemp_Val > rU_BoxMax[5] THEN
    rTemp_Val := rU_BoxMax[5];
ELSIF rTemp_Val < rU_BoxMin[5] THEN
    rTemp_Val := rU_BoxMin[5];
END_IF;
rU_Opt_Seq[3, 5] := rTemp_Val;

(* Step 3.3: Extract Optimal First Control Step u_opt[1] for Actuator Deployment *)
rServoValve_HeadSpool_cmd := rU_Opt_Seq[1, 1];
rServoValve_RodSpool_cmd := rU_Opt_Seq[1, 2];
rAccuBoosterValve_cmd := rU_Opt_Seq[1, 3];
rIntensifierValve_cmd := rU_Opt_Seq[1, 4];
rVacuumPoppetValve_cmd := rU_Opt_Seq[1, 5];


(* ==================================================================================================== *)
(* PHASE 4: 14-STAGE DETERMINISTIC PRODUCTION FINITE STATE MACHINE (FSM)                                *)
(* Controls the complete cyber-physical operational lifecycle of the 4,500-Ton HPDC Gigacasting Cell:   *)
(*   State 0:  FSM_IDLE_SAFE_DISARMED                                                                   *)
(*   State 1:  FSM_DIE_LUBRICATION_AND_BLOW_CLEAN                                                        *)
(*   State 2:  FSM_DIE_CLOSE_AND_4500T_TOGGLE_LOCK                                                      *)
(*   State 3:  FSM_TIE_BAR_PRESTRESS_AND_SAFETY_LATCH                                                     *)
(*   State 4:  FSM_DOSING_FURNACE_LADLE_ALUMINUM_POUR                                                    *)
(*   State 5:  FSM_CAVITY_HIGH_VACUUM_EVACUATION                                                         *)
(*   State 6:  FSM_STAGE1_SLOW_SHOT_WAVE_AVOIDANCE                                                        *)
(*   State 7:  FSM_STAGE2_HIGH_SPEED_DYNAMIC_CAVITY_FILL                                                 *)
(*   State 8:  FSM_VP_TRANSITION_AND_DECELERATION                                                        *)
(*   State 9:  FSM_STAGE3_HYDRAULIC_INTENSIFICATION_HOLD                                                 *)
(*   State 10: FSM_SOLIDIFICATION_COOLING_MONITOR                                                        *)
(*   State 11: FSM_DIE_OPEN_AND_CORE_PULL_RETRACT                                                        *)
(*   State 12: FSM_ROBOTIC_EJECTION_AND_PART_EXTRACTION                                                  *)
(*   State 13: FSM_EMERGENCY_ABORT_AND_SAFE_PRESSURE_DUMP                                                *)
(* ==================================================================================================== *)

(* Master Safety & Emergency Interlock Evaluation *)
IF (NOT bEmergencyStop_NC) OR (NOT bSafetyGateClosed) THEN
    bEmergencyStopActive := TRUE;
    bGeneralFault := TRUE;
    iState := 13; (* Immediate transition to Safe Emergency Abort *)
ELSE
    bEmergencyStopActive := FALSE;
END_IF;

(* State Transition Supervisory Bookkeeping *)
IF iState <> iPrevState THEN
    bStateFirstScan := TRUE;
    rStateTimer_s := 0.0;
    iPreviousState := iPrevState;
    iPrevState := iState;
ELSE
    bStateFirstScan := FALSE;
    rStateTimer_s := rStateTimer_s + rCycleTime_s;
END_IF;
iCurrentState := iState;

(* Total Casting Cycle Execution Timer *)
IF (iState > 0) AND (iState < 13) THEN
    bCycleActive := TRUE;
    rCycleTimer_s := rCycleTimer_s + rCycleTime_s;
    rCycleDuration_s := rCycleTimer_s;
ELSE
    bCycleActive := FALSE;
    IF iState = 0 THEN
        rCycleTimer_s := 0.0;
    END_IF;
END_IF;

(* 14-Stage Deterministic Production FSM Execution Block *)
CASE iState OF

    0: (* FSM_IDLE_SAFE_DISARMED *)
        IF bStateFirstScan THEN
            rServoValve_HeadSpool_cmd := 0.0;
            rServoValve_RodSpool_cmd := 0.0;
            rAccuBoosterValve_cmd := 0.0;
            rIntensifierValve_cmd := 0.0;
            rVacuumPoppetValve_cmd := 0.0;
            rDieClampValve_cmd := 0.0;
            bEjectorForward_cmd := FALSE;
            bEjectorRetract_cmd := TRUE;
            bCorePull1_Extend_cmd := FALSE;
            bCorePull1_Retract_cmd := TRUE;
            bCorePull2_Extend_cmd := FALSE;
            bCorePull2_Retract_cmd := TRUE;
            bVacuumDumpValve_cmd := TRUE;
            bCycleComplete := FALSE;
        END_IF;
        (* Ready condition verification *)
        bSystemReady := bEnable AND bAutoMode AND bSafetyGateClosed AND bEmergencyStop_NC
                        AND bHydraulicPumpsRunning AND bVacuumPumpRunning AND bNitrogenBottleBankOK
                        AND (NOT bGeneralFault) AND bRobotExtractorReady;
        (* Cycle Start Trigger *)
        IF bSystemReady AND bStartCycle THEN
            bCycleComplete := FALSE;
            iState := 1; (* Proceed to Die Lubrication *)
        END_IF;

    1: (* FSM_DIE_LUBRICATION_AND_BLOW_CLEAN *)
        IF bStateFirstScan THEN
            rStageTimeout_s := 15.0;
        END_IF;
        (* Robotic lube spray arm actively coating die inserts with electrostatic micro-spray *)
        IF bDieSprayComplete AND (rStateTimer_s >= 3.5) THEN
            iState := 2; (* Proceed to Die Close & Lock *)
        ELSIF rStateTimer_s > rStageTimeout_s THEN
            bGeneralFault := TRUE;
            iState := 13; (* Timeout fault *)
        END_IF;

    2: (* FSM_DIE_CLOSE_AND_4500T_TOGGLE_LOCK *)
        IF bStateFirstScan THEN
            rStageTimeout_s := 12.0;
            rDieClampValve_cmd := 45.0; (* Proportional close advance *)
        END_IF;
        (* Ramp clamping hydraulic force as toggle linkage moves over-center *)
        IF rStateTimer_s > 2.0 THEN
            rDieClampValve_cmd := 95.0; (* Full high-pressure wedge toggle lock *)
        END_IF;
        (* Check 2oo3 TMR voted clamping force reaches 96% of 44,145 kN rating *)
        IF rVoted_ClampForce_kN >= (rClampForce_Setpoint_kN * 0.96) THEN
            iState := 3; (* Proceed to Tie-Bar Prestress *)
        ELSIF rStateTimer_s > rStageTimeout_s THEN
            bGeneralFault := TRUE;
            iState := 13;
        END_IF;

    3: (* FSM_TIE_BAR_PRESTRESS_AND_SAFETY_LATCH *)
        IF bStateFirstScan THEN
            rStageTimeout_s := 8.0;
            bCorePull1_Extend_cmd := TRUE;
            bCorePull1_Retract_cmd := FALSE;
            bCorePull2_Extend_cmd := TRUE;
            bCorePull2_Retract_cmd := FALSE;
        END_IF;
        (* Side cores locked and acoustic tie-bar strain verified *)
        IF (rStateTimer_s >= 2.5) AND (rVoted_ClampForce_kN >= (rClampForce_Setpoint_kN * 0.98)) THEN
            iState := 4; (* Proceed to Molten Aluminum Pour *)
        ELSIF rStateTimer_s > rStageTimeout_s THEN
            bGeneralFault := TRUE;
            iState := 13;
        END_IF;

    4: (* FSM_DOSING_FURNACE_LADLE_ALUMINUM_POUR *)
        IF bStateFirstScan THEN
            rStageTimeout_s := 10.0;
            bVacuumDumpValve_cmd := FALSE; (* Close vacuum vent to prepare for evacuation *)
        END_IF;
        (* Verify molten alloy temperature & dosing ladle poured weight *)
        IF (rStateTimer_s >= 4.0) THEN
            IF (rMoltenMetalTemp_degC >= 660.0) AND (rMoltenMetalTemp_degC <= 735.0)
               AND (rDosingLadleWeight_kg >= 35.0) AND (rDosingLadleWeight_kg <= 42.0) THEN
                iState := 5; (* Proceed to High Vacuum Evacuation *)
            ELSE
                bGeneralFault := TRUE;
                iState := 13; (* Ladle dosing thermal/mass violation *)
            END_IF;
        ELSIF rStateTimer_s > rStageTimeout_s THEN
            bGeneralFault := TRUE;
            iState := 13;
        END_IF;

    5: (* FSM_CAVITY_HIGH_VACUUM_EVACUATION *)
        IF bStateFirstScan THEN
            rStageTimeout_s := 1.8;
            rVacuumPoppetValve_cmd := 100.0; (* Open high-speed chill-vent vacuum valves *)
        END_IF;
        (* Check 2oo3 TMR voted cavity vacuum pressure reaches < 25 mbar threshold *)
        IF rVoted_CavityVacuum_mbar <= rVacuumTarget_mbar THEN
            rShotStartTime_s := rCycleTimer_s;
            iState := 6; (* Trigger Stage 1 Slow Shot *)
        ELSIF rStateTimer_s > rStageTimeout_s THEN
            (* Vacuum seal integrity failure - abort before molten alloy is injected *)
            bGeneralFault := TRUE;
            iState := 13;
        END_IF;

    6: (* FSM_STAGE1_SLOW_SHOT_WAVE_AVOIDANCE *)
        IF bStateFirstScan THEN
            rStageTimeout_s := 3.5;
        END_IF;
        (* Plunger advances slowly at 0.28 m/s controlled by MPC to prevent turbulent wave folding *)
        (* Switchover to Stage 2 Fast Shot when plunger reaches 450 mm *)
        IF rVoted_PlungerPos_mm >= 450.0 THEN
            rFillStartTime_s := rCycleTimer_s;
            iState := 7; (* Trigger Stage 2 Fast Shot *)
        ELSIF rStateTimer_s > rStageTimeout_s THEN
            bGeneralFault := TRUE;
            iState := 13; (* Slow shot jam timeout *)
        END_IF;

    7: (* FSM_STAGE2_HIGH_SPEED_DYNAMIC_CAVITY_FILL *)
        IF bStateFirstScan THEN
            rStageTimeout_s := 0.250; (* Fast fill must complete within 250 ms *)
            rAccuBoosterValve_cmd := 100.0; (* Fire high-speed nitrogen accumulator discharge *)
        END_IF;
        (* Track maximum plunger velocity attained *)
        IF rVoted_PlungerVel_mps > rMaxPlungerVel_mps THEN
            rMaxPlungerVel_mps := rVoted_PlungerVel_mps;
        END_IF;
        (* V/P Transfer Point Detection: Plunger reaches 820 mm or hydraulic head pressure spikes *)
        IF (rVoted_PlungerPos_mm >= rV_P_TransferPos_mm) OR (rVoted_HeadPress_bar >= 175.0) THEN
            rFillTime_ms := (rCycleTimer_s - rFillStartTime_s) * 1000.0;
            iState := 8; (* Velocity-to-Pressure Transition *)
        ELSIF rStateTimer_s > rStageTimeout_s THEN
            bGeneralFault := TRUE;
            iState := 13; (* Cavity filling obstruction timeout *)
        END_IF;

    8: (* FSM_VP_TRANSITION_AND_DECELERATION *)
        IF bStateFirstScan THEN
            rStageTimeout_s := 0.050; (* 50 ms transition window *)
            rVacuumPoppetValve_cmd := 0.0; (* Mechanical chill-vent shut-off closed before alloy impacts vent *)
            rServoValve_RodSpool_cmd := 55.0; (* Rod backpressure cushioning *)
        END_IF;
        (* Once kinetic deceleration occurs and pressure front forms *)
        IF (rVoted_HeadPress_bar >= 195.0) OR (rStateTimer_s >= 0.018) THEN
            rIntensifyStartTime_s := rCycleTimer_s;
            iState := 9; (* Trigger Stage 3 Intensification *)
        END_IF;

    9: (* FSM_STAGE3_HYDRAULIC_INTENSIFICATION_HOLD *)
        IF bStateFirstScan THEN
            rStageTimeout_s := 5.0;
            rIntensifierValve_cmd := 100.0; (* Fire high-pressure multiplication cartridge *)
            bIntensificationLatching := TRUE;
        END_IF;
        (* Measure intensification pressure rise time *)
        IF (rVoted_HeadPress_bar >= (rStage3_TargetPress_bar * 0.90)) AND (rIntensificationRiseTime_ms = 0.0) THEN
            rIntensificationRiseTime_ms := (rCycleTimer_s - rIntensifyStartTime_s) * 1000.0;
        END_IF;
        (* Track peak intensification pressure *)
        IF rVoted_HeadPress_bar > rPeakIntensificationPress_bar THEN
            rPeakIntensificationPress_bar := rVoted_HeadPress_bar;
        END_IF;
        (* Measure residual biscuit thickness *)
        rFinalBiscuitThickness_mm := rBiscuitThickness_mm;
        (* Hold high pressure for 2.8s to feed solidification shrinkage *)
        IF rStateTimer_s >= 2.8 THEN
            rIntensifierValve_cmd := 0.0; (* Decompress multiplier *)
            iState := 10; (* Proceed to Solidification Cooling Monitor *)
        ELSIF rStateTimer_s > rStageTimeout_s THEN
            bGeneralFault := TRUE;
            iState := 13;
        END_IF;

    10: (* FSM_SOLIDIFICATION_COOLING_MONITOR *)
        IF bStateFirstScan THEN
            rStageTimeout_s := 25.0;
            rAccuBoosterValve_cmd := 0.0;
            rServoValve_HeadSpool_cmd := 0.0;
        END_IF;
        (* Conformal cooling circuit dwell to ensure solidus transition across heavy node sections *)
        IF (rStateTimer_s >= rSolidificationRequired_s) AND (rDieTemp_Fixed_degC <= 230.0) AND (rDieTemp_Moving_degC <= 225.0) THEN
            iState := 11; (* Proceed to Die Open & Core Pull *)
        ELSIF rStateTimer_s > rStageTimeout_s THEN
            bGeneralFault := TRUE;
            iState := 13; (* Cooling circuit fault *)
        END_IF;

    11: (* FSM_DIE_OPEN_AND_CORE_PULL_RETRACT *)
        IF bStateFirstScan THEN
            rStageTimeout_s := 15.0;
            bCorePull1_Retract_cmd := TRUE;
            bCorePull1_Extend_cmd := FALSE;
            bCorePull2_Retract_cmd := TRUE;
            bCorePull2_Extend_cmd := FALSE;
            rDieClampValve_cmd := 0.0; (* Unlock 4,500T toggle *)
        END_IF;
        (* Cores retracted and die platen opened to part extraction position *)
        IF rStateTimer_s >= 4.5 THEN
            iState := 12; (* Proceed to Part Ejection *)
        ELSIF rStateTimer_s > rStageTimeout_s THEN
            bGeneralFault := TRUE;
            iState := 13;
        END_IF;

    12: (* FSM_ROBOTIC_EJECTION_AND_PART_EXTRACTION *)
        IF bStateFirstScan THEN
            rStageTimeout_s := 18.0;
            bEjectorForward_cmd := TRUE;
            bEjectorRetract_cmd := FALSE;
        END_IF;
        (* Robot grips part and removes from die space *)
        IF rStateTimer_s >= 3.0 THEN
            bEjectorForward_cmd := FALSE;
            bEjectorRetract_cmd := TRUE;
        END_IF;
        IF (rStateTimer_s >= 6.5) AND bRobotExtractorReady THEN
            bCycleComplete := TRUE;
            iState := 0; (* Cycle successful -> return to Idle *)
        ELSIF rStateTimer_s > rStageTimeout_s THEN
            bGeneralFault := TRUE;
            iState := 13;
        END_IF;

    13: (* FSM_EMERGENCY_ABORT_AND_SAFE_PRESSURE_DUMP *)
        IF bStateFirstScan THEN
            rServoValve_HeadSpool_cmd := 0.0;
            rServoValve_RodSpool_cmd := 0.0;
            rAccuBoosterValve_cmd := 0.0;
            rIntensifierValve_cmd := 0.0;
            rVacuumPoppetValve_cmd := 0.0;
            bVacuumDumpValve_cmd := TRUE; (* Vent vacuum lines *)
            bEjectorForward_cmd := FALSE;
            bGeneralFault := TRUE;
        END_IF;
        (* Await Operator Reset Command *)
        IF bReset AND bEmergencyStop_NC AND bSafetyGateClosed THEN
            bGeneralFault := FALSE;
            bEmergencyStopActive := FALSE;
            iState := 0; (* Return to Idle Safe Disarmed *)
        END_IF;

END_CASE;


(* ==================================================================================================== *)
(* PHASE 5: ANSI/ISA-18.2 MULTI-TIER ALARMS & 32-BIT BIT-PACKED FIELDBUS TELEMETRY REGISTERS            *)
(* 10 Critical Process Variables Monitored:                                                             *)
(*   PV 1:  Shot Plunger Speed [m/s]                                                                    *)
(*   PV 2:  Head Chamber Injection Hydraulic Pressure [bar]                                             *)
(*   PV 3:  Die Cavity Absolute Vacuum Level [mbar]                                                     *)
(*   PV 4:  4,500-Ton Clamping Mechanism Total Locking Force [kN]                                       *)
(*   PV 5:  Cover Die Cavity Insert Thermocouple Average [deg C]                                        *)
(*   PV 6:  Hydraulic Power Unit Reservoir Oil Temperature [deg C]                                      *)
(*   PV 7:  Die Internal Conformal Cooling Water Flow Rate [l/min]                                      *)
(*   PV 8:  Molten Metal Solidification Intensification Pressure [bar]                                 *)
(*   PV 9:  Dosing Holding Furnace Molten Aluminum Pouring Temperature [deg C]                          *)
(*   PV 10: Total Gigacasting Cycle Execution Duration [s]                                              *)
(* ==================================================================================================== *)

(* Step 5.1: Process Variable Feedback Assignment *)
rPV_Val[1] := ABS(rVoted_PlungerVel_mps);
rPV_Val[2] := rVoted_HeadPress_bar;
rPV_Val[3] := rVoted_CavityVacuum_mbar;
rPV_Val[4] := rVoted_ClampForce_kN;
rPV_Val[5] := rDieTemp_Fixed_degC;
rPV_Val[6] := rHydraulicOilTemp_degC;
rPV_Val[7] := rCoolingWaterFlow_lpm;
rPV_Val[8] := rEstimated_MetalPress_bar;
rPV_Val[9] := rMoltenMetalTemp_degC;
rPV_Val[10] := rCycleDuration_s;

(* Step 5.2: ANSI/ISA-18.2 Multi-Tier Trip, Persistence Timing & Deadband Hysteresis Engine *)
(* -------------------------------------------------------------------------------------------------- *)
(* PV 1: Shot Plunger Speed [m/s] *)
(* -------------------------------------------------------------------------------------------------- *)
(* High-High (HH) Alarm Evaluation *)
IF rPV_Val[1] >= rPV_HH_Limit[1] THEN
    rAlarmDelay_Timer_HH[1] := rAlarmDelay_Timer_HH[1] + rCycleTime_s;
    IF rAlarmDelay_Timer_HH[1] >= rAlarmDelay_Limit_s[1] THEN
        bAlarmActive_HH[1] := TRUE;
        bAlarmLatched_HH[1] := TRUE;
        bGeneralFault := TRUE; (* HH Alarms cause emergency escalation *)
    END_IF;
ELSIF rPV_Val[1] < (rPV_HH_Limit[1] - rPV_Hysteresis[1]) THEN
    rAlarmDelay_Timer_HH[1] := 0.0;
    bAlarmActive_HH[1] := FALSE;
END_IF;

(* High (H) Warning Alarm Evaluation *)
IF rPV_Val[1] >= rPV_H_Limit[1] THEN
    rAlarmDelay_Timer_H[1] := rAlarmDelay_Timer_H[1] + rCycleTime_s;
    IF rAlarmDelay_Timer_H[1] >= rAlarmDelay_Limit_s[1] THEN
        bAlarmActive_H[1] := TRUE;
        bAlarmLatched_H[1] := TRUE;
    END_IF;
ELSIF rPV_Val[1] < (rPV_H_Limit[1] - rPV_Hysteresis[1]) THEN
    rAlarmDelay_Timer_H[1] := 0.0;
    bAlarmActive_H[1] := FALSE;
END_IF;

(* Low (L) Warning Alarm Evaluation *)
IF (rPV_L_Limit[1] > 0.0) AND (rPV_Val[1] <= rPV_L_Limit[1]) THEN
    rAlarmDelay_Timer_L[1] := rAlarmDelay_Timer_L[1] + rCycleTime_s;
    IF rAlarmDelay_Timer_L[1] >= rAlarmDelay_Limit_s[1] THEN
        bAlarmActive_L[1] := TRUE;
        bAlarmLatched_L[1] := TRUE;
    END_IF;
ELSIF rPV_Val[1] > (rPV_L_Limit[1] + rPV_Hysteresis[1]) THEN
    rAlarmDelay_Timer_L[1] := 0.0;
    bAlarmActive_L[1] := FALSE;
END_IF;

(* Low-Low (LL) Alarm Evaluation *)
IF (rPV_LL_Limit[1] > 0.0) AND (rPV_Val[1] <= rPV_LL_Limit[1]) THEN
    rAlarmDelay_Timer_LL[1] := rAlarmDelay_Timer_LL[1] + rCycleTime_s;
    IF rAlarmDelay_Timer_LL[1] >= rAlarmDelay_Limit_s[1] THEN
        bAlarmActive_LL[1] := TRUE;
        bAlarmLatched_LL[1] := TRUE;
        bGeneralFault := TRUE; (* LL Alarms cause emergency escalation *)
    END_IF;
ELSIF rPV_Val[1] > (rPV_LL_Limit[1] + rPV_Hysteresis[1]) THEN
    rAlarmDelay_Timer_LL[1] := 0.0;
    bAlarmActive_LL[1] := FALSE;
END_IF;

IF bReset THEN
    bAlarmLatched_HH[1] := FALSE;
    bAlarmLatched_H[1] := FALSE;
    bAlarmLatched_L[1] := FALSE;
    bAlarmLatched_LL[1] := FALSE;
END_IF;

(* -------------------------------------------------------------------------------------------------- *)
(* PV 2: Head Injection Hydraulic Pressure [bar] *)
(* -------------------------------------------------------------------------------------------------- *)
(* High-High (HH) Alarm Evaluation *)
IF rPV_Val[2] >= rPV_HH_Limit[2] THEN
    rAlarmDelay_Timer_HH[2] := rAlarmDelay_Timer_HH[2] + rCycleTime_s;
    IF rAlarmDelay_Timer_HH[2] >= rAlarmDelay_Limit_s[2] THEN
        bAlarmActive_HH[2] := TRUE;
        bAlarmLatched_HH[2] := TRUE;
        bGeneralFault := TRUE; (* HH Alarms cause emergency escalation *)
    END_IF;
ELSIF rPV_Val[2] < (rPV_HH_Limit[2] - rPV_Hysteresis[2]) THEN
    rAlarmDelay_Timer_HH[2] := 0.0;
    bAlarmActive_HH[2] := FALSE;
END_IF;

(* High (H) Warning Alarm Evaluation *)
IF rPV_Val[2] >= rPV_H_Limit[2] THEN
    rAlarmDelay_Timer_H[2] := rAlarmDelay_Timer_H[2] + rCycleTime_s;
    IF rAlarmDelay_Timer_H[2] >= rAlarmDelay_Limit_s[2] THEN
        bAlarmActive_H[2] := TRUE;
        bAlarmLatched_H[2] := TRUE;
    END_IF;
ELSIF rPV_Val[2] < (rPV_H_Limit[2] - rPV_Hysteresis[2]) THEN
    rAlarmDelay_Timer_H[2] := 0.0;
    bAlarmActive_H[2] := FALSE;
END_IF;

(* Low (L) Warning Alarm Evaluation *)
IF (rPV_L_Limit[2] > 0.0) AND (rPV_Val[2] <= rPV_L_Limit[2]) THEN
    rAlarmDelay_Timer_L[2] := rAlarmDelay_Timer_L[2] + rCycleTime_s;
    IF rAlarmDelay_Timer_L[2] >= rAlarmDelay_Limit_s[2] THEN
        bAlarmActive_L[2] := TRUE;
        bAlarmLatched_L[2] := TRUE;
    END_IF;
ELSIF rPV_Val[2] > (rPV_L_Limit[2] + rPV_Hysteresis[2]) THEN
    rAlarmDelay_Timer_L[2] := 0.0;
    bAlarmActive_L[2] := FALSE;
END_IF;

(* Low-Low (LL) Alarm Evaluation *)
IF (rPV_LL_Limit[2] > 0.0) AND (rPV_Val[2] <= rPV_LL_Limit[2]) THEN
    rAlarmDelay_Timer_LL[2] := rAlarmDelay_Timer_LL[2] + rCycleTime_s;
    IF rAlarmDelay_Timer_LL[2] >= rAlarmDelay_Limit_s[2] THEN
        bAlarmActive_LL[2] := TRUE;
        bAlarmLatched_LL[2] := TRUE;
        bGeneralFault := TRUE; (* LL Alarms cause emergency escalation *)
    END_IF;
ELSIF rPV_Val[2] > (rPV_LL_Limit[2] + rPV_Hysteresis[2]) THEN
    rAlarmDelay_Timer_LL[2] := 0.0;
    bAlarmActive_LL[2] := FALSE;
END_IF;

IF bReset THEN
    bAlarmLatched_HH[2] := FALSE;
    bAlarmLatched_H[2] := FALSE;
    bAlarmLatched_L[2] := FALSE;
    bAlarmLatched_LL[2] := FALSE;
END_IF;

(* -------------------------------------------------------------------------------------------------- *)
(* PV 3: Die Cavity Absolute Vacuum [mbar] *)
(* -------------------------------------------------------------------------------------------------- *)
(* High-High (HH) Alarm Evaluation *)
IF rPV_Val[3] >= rPV_HH_Limit[3] THEN
    rAlarmDelay_Timer_HH[3] := rAlarmDelay_Timer_HH[3] + rCycleTime_s;
    IF rAlarmDelay_Timer_HH[3] >= rAlarmDelay_Limit_s[3] THEN
        bAlarmActive_HH[3] := TRUE;
        bAlarmLatched_HH[3] := TRUE;
        bGeneralFault := TRUE; (* HH Alarms cause emergency escalation *)
    END_IF;
ELSIF rPV_Val[3] < (rPV_HH_Limit[3] - rPV_Hysteresis[3]) THEN
    rAlarmDelay_Timer_HH[3] := 0.0;
    bAlarmActive_HH[3] := FALSE;
END_IF;

(* High (H) Warning Alarm Evaluation *)
IF rPV_Val[3] >= rPV_H_Limit[3] THEN
    rAlarmDelay_Timer_H[3] := rAlarmDelay_Timer_H[3] + rCycleTime_s;
    IF rAlarmDelay_Timer_H[3] >= rAlarmDelay_Limit_s[3] THEN
        bAlarmActive_H[3] := TRUE;
        bAlarmLatched_H[3] := TRUE;
    END_IF;
ELSIF rPV_Val[3] < (rPV_H_Limit[3] - rPV_Hysteresis[3]) THEN
    rAlarmDelay_Timer_H[3] := 0.0;
    bAlarmActive_H[3] := FALSE;
END_IF;

(* Low (L) Warning Alarm Evaluation *)
IF (rPV_L_Limit[3] > 0.0) AND (rPV_Val[3] <= rPV_L_Limit[3]) THEN
    rAlarmDelay_Timer_L[3] := rAlarmDelay_Timer_L[3] + rCycleTime_s;
    IF rAlarmDelay_Timer_L[3] >= rAlarmDelay_Limit_s[3] THEN
        bAlarmActive_L[3] := TRUE;
        bAlarmLatched_L[3] := TRUE;
    END_IF;
ELSIF rPV_Val[3] > (rPV_L_Limit[3] + rPV_Hysteresis[3]) THEN
    rAlarmDelay_Timer_L[3] := 0.0;
    bAlarmActive_L[3] := FALSE;
END_IF;

(* Low-Low (LL) Alarm Evaluation *)
IF (rPV_LL_Limit[3] > 0.0) AND (rPV_Val[3] <= rPV_LL_Limit[3]) THEN
    rAlarmDelay_Timer_LL[3] := rAlarmDelay_Timer_LL[3] + rCycleTime_s;
    IF rAlarmDelay_Timer_LL[3] >= rAlarmDelay_Limit_s[3] THEN
        bAlarmActive_LL[3] := TRUE;
        bAlarmLatched_LL[3] := TRUE;
        bGeneralFault := TRUE; (* LL Alarms cause emergency escalation *)
    END_IF;
ELSIF rPV_Val[3] > (rPV_LL_Limit[3] + rPV_Hysteresis[3]) THEN
    rAlarmDelay_Timer_LL[3] := 0.0;
    bAlarmActive_LL[3] := FALSE;
END_IF;

IF bReset THEN
    bAlarmLatched_HH[3] := FALSE;
    bAlarmLatched_H[3] := FALSE;
    bAlarmLatched_L[3] := FALSE;
    bAlarmLatched_LL[3] := FALSE;
END_IF;

(* -------------------------------------------------------------------------------------------------- *)
(* PV 4: 4,500-Ton Clamping Force [kN] *)
(* -------------------------------------------------------------------------------------------------- *)
(* High-High (HH) Alarm Evaluation *)
IF rPV_Val[4] >= rPV_HH_Limit[4] THEN
    rAlarmDelay_Timer_HH[4] := rAlarmDelay_Timer_HH[4] + rCycleTime_s;
    IF rAlarmDelay_Timer_HH[4] >= rAlarmDelay_Limit_s[4] THEN
        bAlarmActive_HH[4] := TRUE;
        bAlarmLatched_HH[4] := TRUE;
        bGeneralFault := TRUE; (* HH Alarms cause emergency escalation *)
    END_IF;
ELSIF rPV_Val[4] < (rPV_HH_Limit[4] - rPV_Hysteresis[4]) THEN
    rAlarmDelay_Timer_HH[4] := 0.0;
    bAlarmActive_HH[4] := FALSE;
END_IF;

(* High (H) Warning Alarm Evaluation *)
IF rPV_Val[4] >= rPV_H_Limit[4] THEN
    rAlarmDelay_Timer_H[4] := rAlarmDelay_Timer_H[4] + rCycleTime_s;
    IF rAlarmDelay_Timer_H[4] >= rAlarmDelay_Limit_s[4] THEN
        bAlarmActive_H[4] := TRUE;
        bAlarmLatched_H[4] := TRUE;
    END_IF;
ELSIF rPV_Val[4] < (rPV_H_Limit[4] - rPV_Hysteresis[4]) THEN
    rAlarmDelay_Timer_H[4] := 0.0;
    bAlarmActive_H[4] := FALSE;
END_IF;

(* Low (L) Warning Alarm Evaluation *)
IF (rPV_L_Limit[4] > 0.0) AND (rPV_Val[4] <= rPV_L_Limit[4]) THEN
    rAlarmDelay_Timer_L[4] := rAlarmDelay_Timer_L[4] + rCycleTime_s;
    IF rAlarmDelay_Timer_L[4] >= rAlarmDelay_Limit_s[4] THEN
        bAlarmActive_L[4] := TRUE;
        bAlarmLatched_L[4] := TRUE;
    END_IF;
ELSIF rPV_Val[4] > (rPV_L_Limit[4] + rPV_Hysteresis[4]) THEN
    rAlarmDelay_Timer_L[4] := 0.0;
    bAlarmActive_L[4] := FALSE;
END_IF;

(* Low-Low (LL) Alarm Evaluation *)
IF (rPV_LL_Limit[4] > 0.0) AND (rPV_Val[4] <= rPV_LL_Limit[4]) THEN
    rAlarmDelay_Timer_LL[4] := rAlarmDelay_Timer_LL[4] + rCycleTime_s;
    IF rAlarmDelay_Timer_LL[4] >= rAlarmDelay_Limit_s[4] THEN
        bAlarmActive_LL[4] := TRUE;
        bAlarmLatched_LL[4] := TRUE;
        bGeneralFault := TRUE; (* LL Alarms cause emergency escalation *)
    END_IF;
ELSIF rPV_Val[4] > (rPV_LL_Limit[4] + rPV_Hysteresis[4]) THEN
    rAlarmDelay_Timer_LL[4] := 0.0;
    bAlarmActive_LL[4] := FALSE;
END_IF;

IF bReset THEN
    bAlarmLatched_HH[4] := FALSE;
    bAlarmLatched_H[4] := FALSE;
    bAlarmLatched_L[4] := FALSE;
    bAlarmLatched_LL[4] := FALSE;
END_IF;

(* -------------------------------------------------------------------------------------------------- *)
(* PV 5: Die Cover Cavity Temperature [deg C] *)
(* -------------------------------------------------------------------------------------------------- *)
(* High-High (HH) Alarm Evaluation *)
IF rPV_Val[5] >= rPV_HH_Limit[5] THEN
    rAlarmDelay_Timer_HH[5] := rAlarmDelay_Timer_HH[5] + rCycleTime_s;
    IF rAlarmDelay_Timer_HH[5] >= rAlarmDelay_Limit_s[5] THEN
        bAlarmActive_HH[5] := TRUE;
        bAlarmLatched_HH[5] := TRUE;
        bGeneralFault := TRUE; (* HH Alarms cause emergency escalation *)
    END_IF;
ELSIF rPV_Val[5] < (rPV_HH_Limit[5] - rPV_Hysteresis[5]) THEN
    rAlarmDelay_Timer_HH[5] := 0.0;
    bAlarmActive_HH[5] := FALSE;
END_IF;

(* High (H) Warning Alarm Evaluation *)
IF rPV_Val[5] >= rPV_H_Limit[5] THEN
    rAlarmDelay_Timer_H[5] := rAlarmDelay_Timer_H[5] + rCycleTime_s;
    IF rAlarmDelay_Timer_H[5] >= rAlarmDelay_Limit_s[5] THEN
        bAlarmActive_H[5] := TRUE;
        bAlarmLatched_H[5] := TRUE;
    END_IF;
ELSIF rPV_Val[5] < (rPV_H_Limit[5] - rPV_Hysteresis[5]) THEN
    rAlarmDelay_Timer_H[5] := 0.0;
    bAlarmActive_H[5] := FALSE;
END_IF;

(* Low (L) Warning Alarm Evaluation *)
IF (rPV_L_Limit[5] > 0.0) AND (rPV_Val[5] <= rPV_L_Limit[5]) THEN
    rAlarmDelay_Timer_L[5] := rAlarmDelay_Timer_L[5] + rCycleTime_s;
    IF rAlarmDelay_Timer_L[5] >= rAlarmDelay_Limit_s[5] THEN
        bAlarmActive_L[5] := TRUE;
        bAlarmLatched_L[5] := TRUE;
    END_IF;
ELSIF rPV_Val[5] > (rPV_L_Limit[5] + rPV_Hysteresis[5]) THEN
    rAlarmDelay_Timer_L[5] := 0.0;
    bAlarmActive_L[5] := FALSE;
END_IF;

(* Low-Low (LL) Alarm Evaluation *)
IF (rPV_LL_Limit[5] > 0.0) AND (rPV_Val[5] <= rPV_LL_Limit[5]) THEN
    rAlarmDelay_Timer_LL[5] := rAlarmDelay_Timer_LL[5] + rCycleTime_s;
    IF rAlarmDelay_Timer_LL[5] >= rAlarmDelay_Limit_s[5] THEN
        bAlarmActive_LL[5] := TRUE;
        bAlarmLatched_LL[5] := TRUE;
        bGeneralFault := TRUE; (* LL Alarms cause emergency escalation *)
    END_IF;
ELSIF rPV_Val[5] > (rPV_LL_Limit[5] + rPV_Hysteresis[5]) THEN
    rAlarmDelay_Timer_LL[5] := 0.0;
    bAlarmActive_LL[5] := FALSE;
END_IF;

IF bReset THEN
    bAlarmLatched_HH[5] := FALSE;
    bAlarmLatched_H[5] := FALSE;
    bAlarmLatched_L[5] := FALSE;
    bAlarmLatched_LL[5] := FALSE;
END_IF;

(* -------------------------------------------------------------------------------------------------- *)
(* PV 6: Hydraulic Reservoir Oil Temperature [deg C] *)
(* -------------------------------------------------------------------------------------------------- *)
(* High-High (HH) Alarm Evaluation *)
IF rPV_Val[6] >= rPV_HH_Limit[6] THEN
    rAlarmDelay_Timer_HH[6] := rAlarmDelay_Timer_HH[6] + rCycleTime_s;
    IF rAlarmDelay_Timer_HH[6] >= rAlarmDelay_Limit_s[6] THEN
        bAlarmActive_HH[6] := TRUE;
        bAlarmLatched_HH[6] := TRUE;
        bGeneralFault := TRUE; (* HH Alarms cause emergency escalation *)
    END_IF;
ELSIF rPV_Val[6] < (rPV_HH_Limit[6] - rPV_Hysteresis[6]) THEN
    rAlarmDelay_Timer_HH[6] := 0.0;
    bAlarmActive_HH[6] := FALSE;
END_IF;

(* High (H) Warning Alarm Evaluation *)
IF rPV_Val[6] >= rPV_H_Limit[6] THEN
    rAlarmDelay_Timer_H[6] := rAlarmDelay_Timer_H[6] + rCycleTime_s;
    IF rAlarmDelay_Timer_H[6] >= rAlarmDelay_Limit_s[6] THEN
        bAlarmActive_H[6] := TRUE;
        bAlarmLatched_H[6] := TRUE;
    END_IF;
ELSIF rPV_Val[6] < (rPV_H_Limit[6] - rPV_Hysteresis[6]) THEN
    rAlarmDelay_Timer_H[6] := 0.0;
    bAlarmActive_H[6] := FALSE;
END_IF;

(* Low (L) Warning Alarm Evaluation *)
IF (rPV_L_Limit[6] > 0.0) AND (rPV_Val[6] <= rPV_L_Limit[6]) THEN
    rAlarmDelay_Timer_L[6] := rAlarmDelay_Timer_L[6] + rCycleTime_s;
    IF rAlarmDelay_Timer_L[6] >= rAlarmDelay_Limit_s[6] THEN
        bAlarmActive_L[6] := TRUE;
        bAlarmLatched_L[6] := TRUE;
    END_IF;
ELSIF rPV_Val[6] > (rPV_L_Limit[6] + rPV_Hysteresis[6]) THEN
    rAlarmDelay_Timer_L[6] := 0.0;
    bAlarmActive_L[6] := FALSE;
END_IF;

(* Low-Low (LL) Alarm Evaluation *)
IF (rPV_LL_Limit[6] > 0.0) AND (rPV_Val[6] <= rPV_LL_Limit[6]) THEN
    rAlarmDelay_Timer_LL[6] := rAlarmDelay_Timer_LL[6] + rCycleTime_s;
    IF rAlarmDelay_Timer_LL[6] >= rAlarmDelay_Limit_s[6] THEN
        bAlarmActive_LL[6] := TRUE;
        bAlarmLatched_LL[6] := TRUE;
        bGeneralFault := TRUE; (* LL Alarms cause emergency escalation *)
    END_IF;
ELSIF rPV_Val[6] > (rPV_LL_Limit[6] + rPV_Hysteresis[6]) THEN
    rAlarmDelay_Timer_LL[6] := 0.0;
    bAlarmActive_LL[6] := FALSE;
END_IF;

IF bReset THEN
    bAlarmLatched_HH[6] := FALSE;
    bAlarmLatched_H[6] := FALSE;
    bAlarmLatched_L[6] := FALSE;
    bAlarmLatched_LL[6] := FALSE;
END_IF;

(* -------------------------------------------------------------------------------------------------- *)
(* PV 7: Conformal Cooling Water Flow Rate [l/min] *)
(* -------------------------------------------------------------------------------------------------- *)
(* High-High (HH) Alarm Evaluation *)
IF rPV_Val[7] >= rPV_HH_Limit[7] THEN
    rAlarmDelay_Timer_HH[7] := rAlarmDelay_Timer_HH[7] + rCycleTime_s;
    IF rAlarmDelay_Timer_HH[7] >= rAlarmDelay_Limit_s[7] THEN
        bAlarmActive_HH[7] := TRUE;
        bAlarmLatched_HH[7] := TRUE;
        bGeneralFault := TRUE; (* HH Alarms cause emergency escalation *)
    END_IF;
ELSIF rPV_Val[7] < (rPV_HH_Limit[7] - rPV_Hysteresis[7]) THEN
    rAlarmDelay_Timer_HH[7] := 0.0;
    bAlarmActive_HH[7] := FALSE;
END_IF;

(* High (H) Warning Alarm Evaluation *)
IF rPV_Val[7] >= rPV_H_Limit[7] THEN
    rAlarmDelay_Timer_H[7] := rAlarmDelay_Timer_H[7] + rCycleTime_s;
    IF rAlarmDelay_Timer_H[7] >= rAlarmDelay_Limit_s[7] THEN
        bAlarmActive_H[7] := TRUE;
        bAlarmLatched_H[7] := TRUE;
    END_IF;
ELSIF rPV_Val[7] < (rPV_H_Limit[7] - rPV_Hysteresis[7]) THEN
    rAlarmDelay_Timer_H[7] := 0.0;
    bAlarmActive_H[7] := FALSE;
END_IF;

(* Low (L) Warning Alarm Evaluation *)
IF (rPV_L_Limit[7] > 0.0) AND (rPV_Val[7] <= rPV_L_Limit[7]) THEN
    rAlarmDelay_Timer_L[7] := rAlarmDelay_Timer_L[7] + rCycleTime_s;
    IF rAlarmDelay_Timer_L[7] >= rAlarmDelay_Limit_s[7] THEN
        bAlarmActive_L[7] := TRUE;
        bAlarmLatched_L[7] := TRUE;
    END_IF;
ELSIF rPV_Val[7] > (rPV_L_Limit[7] + rPV_Hysteresis[7]) THEN
    rAlarmDelay_Timer_L[7] := 0.0;
    bAlarmActive_L[7] := FALSE;
END_IF;

(* Low-Low (LL) Alarm Evaluation *)
IF (rPV_LL_Limit[7] > 0.0) AND (rPV_Val[7] <= rPV_LL_Limit[7]) THEN
    rAlarmDelay_Timer_LL[7] := rAlarmDelay_Timer_LL[7] + rCycleTime_s;
    IF rAlarmDelay_Timer_LL[7] >= rAlarmDelay_Limit_s[7] THEN
        bAlarmActive_LL[7] := TRUE;
        bAlarmLatched_LL[7] := TRUE;
        bGeneralFault := TRUE; (* LL Alarms cause emergency escalation *)
    END_IF;
ELSIF rPV_Val[7] > (rPV_LL_Limit[7] + rPV_Hysteresis[7]) THEN
    rAlarmDelay_Timer_LL[7] := 0.0;
    bAlarmActive_LL[7] := FALSE;
END_IF;

IF bReset THEN
    bAlarmLatched_HH[7] := FALSE;
    bAlarmLatched_H[7] := FALSE;
    bAlarmLatched_L[7] := FALSE;
    bAlarmLatched_LL[7] := FALSE;
END_IF;

(* -------------------------------------------------------------------------------------------------- *)
(* PV 8: Molten Metal Squeeze Intensification Pressure [bar] *)
(* -------------------------------------------------------------------------------------------------- *)
(* High-High (HH) Alarm Evaluation *)
IF rPV_Val[8] >= rPV_HH_Limit[8] THEN
    rAlarmDelay_Timer_HH[8] := rAlarmDelay_Timer_HH[8] + rCycleTime_s;
    IF rAlarmDelay_Timer_HH[8] >= rAlarmDelay_Limit_s[8] THEN
        bAlarmActive_HH[8] := TRUE;
        bAlarmLatched_HH[8] := TRUE;
        bGeneralFault := TRUE; (* HH Alarms cause emergency escalation *)
    END_IF;
ELSIF rPV_Val[8] < (rPV_HH_Limit[8] - rPV_Hysteresis[8]) THEN
    rAlarmDelay_Timer_HH[8] := 0.0;
    bAlarmActive_HH[8] := FALSE;
END_IF;

(* High (H) Warning Alarm Evaluation *)
IF rPV_Val[8] >= rPV_H_Limit[8] THEN
    rAlarmDelay_Timer_H[8] := rAlarmDelay_Timer_H[8] + rCycleTime_s;
    IF rAlarmDelay_Timer_H[8] >= rAlarmDelay_Limit_s[8] THEN
        bAlarmActive_H[8] := TRUE;
        bAlarmLatched_H[8] := TRUE;
    END_IF;
ELSIF rPV_Val[8] < (rPV_H_Limit[8] - rPV_Hysteresis[8]) THEN
    rAlarmDelay_Timer_H[8] := 0.0;
    bAlarmActive_H[8] := FALSE;
END_IF;

(* Low (L) Warning Alarm Evaluation *)
IF (rPV_L_Limit[8] > 0.0) AND (rPV_Val[8] <= rPV_L_Limit[8]) THEN
    rAlarmDelay_Timer_L[8] := rAlarmDelay_Timer_L[8] + rCycleTime_s;
    IF rAlarmDelay_Timer_L[8] >= rAlarmDelay_Limit_s[8] THEN
        bAlarmActive_L[8] := TRUE;
        bAlarmLatched_L[8] := TRUE;
    END_IF;
ELSIF rPV_Val[8] > (rPV_L_Limit[8] + rPV_Hysteresis[8]) THEN
    rAlarmDelay_Timer_L[8] := 0.0;
    bAlarmActive_L[8] := FALSE;
END_IF;

(* Low-Low (LL) Alarm Evaluation *)
IF (rPV_LL_Limit[8] > 0.0) AND (rPV_Val[8] <= rPV_LL_Limit[8]) THEN
    rAlarmDelay_Timer_LL[8] := rAlarmDelay_Timer_LL[8] + rCycleTime_s;
    IF rAlarmDelay_Timer_LL[8] >= rAlarmDelay_Limit_s[8] THEN
        bAlarmActive_LL[8] := TRUE;
        bAlarmLatched_LL[8] := TRUE;
        bGeneralFault := TRUE; (* LL Alarms cause emergency escalation *)
    END_IF;
ELSIF rPV_Val[8] > (rPV_LL_Limit[8] + rPV_Hysteresis[8]) THEN
    rAlarmDelay_Timer_LL[8] := 0.0;
    bAlarmActive_LL[8] := FALSE;
END_IF;

IF bReset THEN
    bAlarmLatched_HH[8] := FALSE;
    bAlarmLatched_H[8] := FALSE;
    bAlarmLatched_L[8] := FALSE;
    bAlarmLatched_LL[8] := FALSE;
END_IF;

(* -------------------------------------------------------------------------------------------------- *)
(* PV 9: Holding Furnace Molten Aluminum Temperature [deg C] *)
(* -------------------------------------------------------------------------------------------------- *)
(* High-High (HH) Alarm Evaluation *)
IF rPV_Val[9] >= rPV_HH_Limit[9] THEN
    rAlarmDelay_Timer_HH[9] := rAlarmDelay_Timer_HH[9] + rCycleTime_s;
    IF rAlarmDelay_Timer_HH[9] >= rAlarmDelay_Limit_s[9] THEN
        bAlarmActive_HH[9] := TRUE;
        bAlarmLatched_HH[9] := TRUE;
        bGeneralFault := TRUE; (* HH Alarms cause emergency escalation *)
    END_IF;
ELSIF rPV_Val[9] < (rPV_HH_Limit[9] - rPV_Hysteresis[9]) THEN
    rAlarmDelay_Timer_HH[9] := 0.0;
    bAlarmActive_HH[9] := FALSE;
END_IF;

(* High (H) Warning Alarm Evaluation *)
IF rPV_Val[9] >= rPV_H_Limit[9] THEN
    rAlarmDelay_Timer_H[9] := rAlarmDelay_Timer_H[9] + rCycleTime_s;
    IF rAlarmDelay_Timer_H[9] >= rAlarmDelay_Limit_s[9] THEN
        bAlarmActive_H[9] := TRUE;
        bAlarmLatched_H[9] := TRUE;
    END_IF;
ELSIF rPV_Val[9] < (rPV_H_Limit[9] - rPV_Hysteresis[9]) THEN
    rAlarmDelay_Timer_H[9] := 0.0;
    bAlarmActive_H[9] := FALSE;
END_IF;

(* Low (L) Warning Alarm Evaluation *)
IF (rPV_L_Limit[9] > 0.0) AND (rPV_Val[9] <= rPV_L_Limit[9]) THEN
    rAlarmDelay_Timer_L[9] := rAlarmDelay_Timer_L[9] + rCycleTime_s;
    IF rAlarmDelay_Timer_L[9] >= rAlarmDelay_Limit_s[9] THEN
        bAlarmActive_L[9] := TRUE;
        bAlarmLatched_L[9] := TRUE;
    END_IF;
ELSIF rPV_Val[9] > (rPV_L_Limit[9] + rPV_Hysteresis[9]) THEN
    rAlarmDelay_Timer_L[9] := 0.0;
    bAlarmActive_L[9] := FALSE;
END_IF;

(* Low-Low (LL) Alarm Evaluation *)
IF (rPV_LL_Limit[9] > 0.0) AND (rPV_Val[9] <= rPV_LL_Limit[9]) THEN
    rAlarmDelay_Timer_LL[9] := rAlarmDelay_Timer_LL[9] + rCycleTime_s;
    IF rAlarmDelay_Timer_LL[9] >= rAlarmDelay_Limit_s[9] THEN
        bAlarmActive_LL[9] := TRUE;
        bAlarmLatched_LL[9] := TRUE;
        bGeneralFault := TRUE; (* LL Alarms cause emergency escalation *)
    END_IF;
ELSIF rPV_Val[9] > (rPV_LL_Limit[9] + rPV_Hysteresis[9]) THEN
    rAlarmDelay_Timer_LL[9] := 0.0;
    bAlarmActive_LL[9] := FALSE;
END_IF;

IF bReset THEN
    bAlarmLatched_HH[9] := FALSE;
    bAlarmLatched_H[9] := FALSE;
    bAlarmLatched_L[9] := FALSE;
    bAlarmLatched_LL[9] := FALSE;
END_IF;

(* -------------------------------------------------------------------------------------------------- *)
(* PV 10: Total Gigacasting Cycle Execution Time [s] *)
(* -------------------------------------------------------------------------------------------------- *)
(* High-High (HH) Alarm Evaluation *)
IF rPV_Val[10] >= rPV_HH_Limit[10] THEN
    rAlarmDelay_Timer_HH[10] := rAlarmDelay_Timer_HH[10] + rCycleTime_s;
    IF rAlarmDelay_Timer_HH[10] >= rAlarmDelay_Limit_s[10] THEN
        bAlarmActive_HH[10] := TRUE;
        bAlarmLatched_HH[10] := TRUE;
        bGeneralFault := TRUE; (* HH Alarms cause emergency escalation *)
    END_IF;
ELSIF rPV_Val[10] < (rPV_HH_Limit[10] - rPV_Hysteresis[10]) THEN
    rAlarmDelay_Timer_HH[10] := 0.0;
    bAlarmActive_HH[10] := FALSE;
END_IF;

(* High (H) Warning Alarm Evaluation *)
IF rPV_Val[10] >= rPV_H_Limit[10] THEN
    rAlarmDelay_Timer_H[10] := rAlarmDelay_Timer_H[10] + rCycleTime_s;
    IF rAlarmDelay_Timer_H[10] >= rAlarmDelay_Limit_s[10] THEN
        bAlarmActive_H[10] := TRUE;
        bAlarmLatched_H[10] := TRUE;
    END_IF;
ELSIF rPV_Val[10] < (rPV_H_Limit[10] - rPV_Hysteresis[10]) THEN
    rAlarmDelay_Timer_H[10] := 0.0;
    bAlarmActive_H[10] := FALSE;
END_IF;

(* Low (L) Warning Alarm Evaluation *)
IF (rPV_L_Limit[10] > 0.0) AND (rPV_Val[10] <= rPV_L_Limit[10]) THEN
    rAlarmDelay_Timer_L[10] := rAlarmDelay_Timer_L[10] + rCycleTime_s;
    IF rAlarmDelay_Timer_L[10] >= rAlarmDelay_Limit_s[10] THEN
        bAlarmActive_L[10] := TRUE;
        bAlarmLatched_L[10] := TRUE;
    END_IF;
ELSIF rPV_Val[10] > (rPV_L_Limit[10] + rPV_Hysteresis[10]) THEN
    rAlarmDelay_Timer_L[10] := 0.0;
    bAlarmActive_L[10] := FALSE;
END_IF;

(* Low-Low (LL) Alarm Evaluation *)
IF (rPV_LL_Limit[10] > 0.0) AND (rPV_Val[10] <= rPV_LL_Limit[10]) THEN
    rAlarmDelay_Timer_LL[10] := rAlarmDelay_Timer_LL[10] + rCycleTime_s;
    IF rAlarmDelay_Timer_LL[10] >= rAlarmDelay_Limit_s[10] THEN
        bAlarmActive_LL[10] := TRUE;
        bAlarmLatched_LL[10] := TRUE;
        bGeneralFault := TRUE; (* LL Alarms cause emergency escalation *)
    END_IF;
ELSIF rPV_Val[10] > (rPV_LL_Limit[10] + rPV_Hysteresis[10]) THEN
    rAlarmDelay_Timer_LL[10] := 0.0;
    bAlarmActive_LL[10] := FALSE;
END_IF;

IF bReset THEN
    bAlarmLatched_HH[10] := FALSE;
    bAlarmLatched_H[10] := FALSE;
    bAlarmLatched_L[10] := FALSE;
    bAlarmLatched_LL[10] := FALSE;
END_IF;

(* Step 5.3: Fieldbus Bit-Packed Status Words Telemetry Encoding *)
(* Status Word 1: Cell Master Operating Interlocks & FSM Stage *)
udiStatusWord1 := 16#00000000;
IF bEnable THEN udiStatusWord1 := udiStatusWord1 OR 16#00000001; END_IF;
IF bAutoMode THEN udiStatusWord1 := udiStatusWord1 OR 16#00000002; END_IF;
IF bSystemReady THEN udiStatusWord1 := udiStatusWord1 OR 16#00000004; END_IF;
IF bCycleActive THEN udiStatusWord1 := udiStatusWord1 OR 16#00000008; END_IF;
IF bCycleComplete THEN udiStatusWord1 := udiStatusWord1 OR 16#00000010; END_IF;
IF bGeneralFault THEN udiStatusWord1 := udiStatusWord1 OR 16#00000020; END_IF;
IF bEmergencyStopActive THEN udiStatusWord1 := udiStatusWord1 OR 16#00000040; END_IF;
IF bSafetyGateClosed THEN udiStatusWord1 := udiStatusWord1 OR 16#00000080; END_IF;
udiStatusWord1 := udiStatusWord1 OR SHL(INT_TO_DWORD(iState AND 16#0F), 8);
IF bObserverInitialized THEN udiStatusWord1 := udiStatusWord1 OR 16#00001000; END_IF;
IF bIntensificationLatching THEN udiStatusWord1 := udiStatusWord1 OR 16#00002000; END_IF;
IF bBiscuitDetected THEN udiStatusWord1 := udiStatusWord1 OR 16#00004000; END_IF;
IF bEjectionComplete THEN udiStatusWord1 := udiStatusWord1 OR 16#00008000; END_IF;
IF bVacuumPumpRunning THEN udiStatusWord1 := udiStatusWord1 OR 16#00010000; END_IF;
IF bHydraulicPumpsRunning THEN udiStatusWord1 := udiStatusWord1 OR 16#00020000; END_IF;
IF bNitrogenBottleBankOK THEN udiStatusWord1 := udiStatusWord1 OR 16#00040000; END_IF;
IF bRobotExtractorReady THEN udiStatusWord1 := udiStatusWord1 OR 16#00080000; END_IF;
IF bDieSprayComplete THEN udiStatusWord1 := udiStatusWord1 OR 16#00100000; END_IF;

(* Status Word 2: Actuator Command & Physical Valve Deployments *)
udiStatusWord2 := 16#00000000;
IF ABS(rServoValve_HeadSpool_cmd) > 1.0 THEN udiStatusWord2 := udiStatusWord2 OR 16#00000001; END_IF;
IF rServoValve_RodSpool_cmd > 1.0 THEN udiStatusWord2 := udiStatusWord2 OR 16#00000002; END_IF;
IF rAccuBoosterValve_cmd > 50.0 THEN udiStatusWord2 := udiStatusWord2 OR 16#00000004; END_IF;
IF rIntensifierValve_cmd > 50.0 THEN udiStatusWord2 := udiStatusWord2 OR 16#00000008; END_IF;
IF rVacuumPoppetValve_cmd > 50.0 THEN udiStatusWord2 := udiStatusWord2 OR 16#00000010; END_IF;
IF rDieClampValve_cmd > 50.0 THEN udiStatusWord2 := udiStatusWord2 OR 16#00000020; END_IF;
IF bEjectorForward_cmd THEN udiStatusWord2 := udiStatusWord2 OR 16#00000040; END_IF;
IF bEjectorRetract_cmd THEN udiStatusWord2 := udiStatusWord2 OR 16#00000080; END_IF;
IF bCorePull1_Extend_cmd THEN udiStatusWord2 := udiStatusWord2 OR 16#00000100; END_IF;
IF bCorePull1_Retract_cmd THEN udiStatusWord2 := udiStatusWord2 OR 16#00000200; END_IF;
IF bCorePull2_Extend_cmd THEN udiStatusWord2 := udiStatusWord2 OR 16#00000400; END_IF;
IF bCorePull2_Retract_cmd THEN udiStatusWord2 := udiStatusWord2 OR 16#00000800; END_IF;
IF bVacuumDumpValve_cmd THEN udiStatusWord2 := udiStatusWord2 OR 16#00001000; END_IF;

(* Status Word 3: 4-Channel 2oo3 TMR Health & Degradation States *)
udiStatusWord3 := 16#00000000;
udiStatusWord3 := udiStatusWord3 OR INT_TO_DWORD(iTMR_Ch1_DegradationState AND 16#03);
IF bTMR_Ch1_FaultA THEN udiStatusWord3 := udiStatusWord3 OR 16#00000004; END_IF;
IF bTMR_Ch1_FaultB THEN udiStatusWord3 := udiStatusWord3 OR 16#00000008; END_IF;
IF bTMR_Ch1_FaultC THEN udiStatusWord3 := udiStatusWord3 OR 16#00000010; END_IF;
IF bTMR_Ch1_DiscAB OR bTMR_Ch1_DiscBC OR bTMR_Ch1_DiscCA THEN udiStatusWord3 := udiStatusWord3 OR 16#00000020; END_IF;
udiStatusWord3 := udiStatusWord3 OR SHL(INT_TO_DWORD(iTMR_Ch2_DegradationState AND 16#03), 6);
IF bTMR_Ch2_FaultA THEN udiStatusWord3 := udiStatusWord3 OR 16#00000100; END_IF;
IF bTMR_Ch2_FaultB THEN udiStatusWord3 := udiStatusWord3 OR 16#00000200; END_IF;
IF bTMR_Ch2_FaultC THEN udiStatusWord3 := udiStatusWord3 OR 16#00000400; END_IF;
IF bTMR_Ch2_DiscAB OR bTMR_Ch2_DiscBC OR bTMR_Ch2_DiscCA THEN udiStatusWord3 := udiStatusWord3 OR 16#00000800; END_IF;
udiStatusWord3 := udiStatusWord3 OR SHL(INT_TO_DWORD(iTMR_Ch3_DegradationState AND 16#03), 12);
IF bTMR_Ch3_FaultA THEN udiStatusWord3 := udiStatusWord3 OR 16#00004000; END_IF;
IF bTMR_Ch3_FaultB THEN udiStatusWord3 := udiStatusWord3 OR 16#00008000; END_IF;
IF bTMR_Ch3_FaultC THEN udiStatusWord3 := udiStatusWord3 OR 16#00010000; END_IF;
IF bTMR_Ch3_DiscAB OR bTMR_Ch3_DiscBC OR bTMR_Ch3_DiscCA THEN udiStatusWord3 := udiStatusWord3 OR 16#00020000; END_IF;
udiStatusWord3 := udiStatusWord3 OR SHL(INT_TO_DWORD(iTMR_Ch4_DegradationState AND 16#03), 18);
IF bTMR_Ch4_FaultA THEN udiStatusWord3 := udiStatusWord3 OR 16#00100000; END_IF;
IF bTMR_Ch4_FaultB THEN udiStatusWord3 := udiStatusWord3 OR 16#00200000; END_IF;
IF bTMR_Ch4_FaultC THEN udiStatusWord3 := udiStatusWord3 OR 16#00400000; END_IF;
IF bTMR_Ch4_DiscAB OR bTMR_Ch4_DiscBC OR bTMR_Ch4_DiscCA THEN udiStatusWord3 := udiStatusWord3 OR 16#00800000; END_IF;

(* Step 5.4: ANSI/ISA-18.2 Bit-Packed Alarm Registers Encoding *)
udiAlarmWord_ISA_HH := 16#00000000;
udiAlarmWord_ISA_H  := 16#00000000;
udiAlarmWord_ISA_L  := 16#00000000;
udiAlarmWord_ISA_LL := 16#00000000;
IF bAlarmLatched_HH[1] THEN udiAlarmWord_ISA_HH := udiAlarmWord_ISA_HH OR SHL(DWORD#1, 0); END_IF;
IF bAlarmLatched_H[1]  THEN udiAlarmWord_ISA_H  := udiAlarmWord_ISA_H  OR SHL(DWORD#1, 0); END_IF;
IF bAlarmLatched_L[1]  THEN udiAlarmWord_ISA_L  := udiAlarmWord_ISA_L  OR SHL(DWORD#1, 0); END_IF;
IF bAlarmLatched_LL[1] THEN udiAlarmWord_ISA_LL := udiAlarmWord_ISA_LL OR SHL(DWORD#1, 0); END_IF;
IF bAlarmLatched_HH[2] THEN udiAlarmWord_ISA_HH := udiAlarmWord_ISA_HH OR SHL(DWORD#1, 1); END_IF;
IF bAlarmLatched_H[2]  THEN udiAlarmWord_ISA_H  := udiAlarmWord_ISA_H  OR SHL(DWORD#1, 1); END_IF;
IF bAlarmLatched_L[2]  THEN udiAlarmWord_ISA_L  := udiAlarmWord_ISA_L  OR SHL(DWORD#1, 1); END_IF;
IF bAlarmLatched_LL[2] THEN udiAlarmWord_ISA_LL := udiAlarmWord_ISA_LL OR SHL(DWORD#1, 1); END_IF;
IF bAlarmLatched_HH[3] THEN udiAlarmWord_ISA_HH := udiAlarmWord_ISA_HH OR SHL(DWORD#1, 2); END_IF;
IF bAlarmLatched_H[3]  THEN udiAlarmWord_ISA_H  := udiAlarmWord_ISA_H  OR SHL(DWORD#1, 2); END_IF;
IF bAlarmLatched_L[3]  THEN udiAlarmWord_ISA_L  := udiAlarmWord_ISA_L  OR SHL(DWORD#1, 2); END_IF;
IF bAlarmLatched_LL[3] THEN udiAlarmWord_ISA_LL := udiAlarmWord_ISA_LL OR SHL(DWORD#1, 2); END_IF;
IF bAlarmLatched_HH[4] THEN udiAlarmWord_ISA_HH := udiAlarmWord_ISA_HH OR SHL(DWORD#1, 3); END_IF;
IF bAlarmLatched_H[4]  THEN udiAlarmWord_ISA_H  := udiAlarmWord_ISA_H  OR SHL(DWORD#1, 3); END_IF;
IF bAlarmLatched_L[4]  THEN udiAlarmWord_ISA_L  := udiAlarmWord_ISA_L  OR SHL(DWORD#1, 3); END_IF;
IF bAlarmLatched_LL[4] THEN udiAlarmWord_ISA_LL := udiAlarmWord_ISA_LL OR SHL(DWORD#1, 3); END_IF;
IF bAlarmLatched_HH[5] THEN udiAlarmWord_ISA_HH := udiAlarmWord_ISA_HH OR SHL(DWORD#1, 4); END_IF;
IF bAlarmLatched_H[5]  THEN udiAlarmWord_ISA_H  := udiAlarmWord_ISA_H  OR SHL(DWORD#1, 4); END_IF;
IF bAlarmLatched_L[5]  THEN udiAlarmWord_ISA_L  := udiAlarmWord_ISA_L  OR SHL(DWORD#1, 4); END_IF;
IF bAlarmLatched_LL[5] THEN udiAlarmWord_ISA_LL := udiAlarmWord_ISA_LL OR SHL(DWORD#1, 4); END_IF;
IF bAlarmLatched_HH[6] THEN udiAlarmWord_ISA_HH := udiAlarmWord_ISA_HH OR SHL(DWORD#1, 5); END_IF;
IF bAlarmLatched_H[6]  THEN udiAlarmWord_ISA_H  := udiAlarmWord_ISA_H  OR SHL(DWORD#1, 5); END_IF;
IF bAlarmLatched_L[6]  THEN udiAlarmWord_ISA_L  := udiAlarmWord_ISA_L  OR SHL(DWORD#1, 5); END_IF;
IF bAlarmLatched_LL[6] THEN udiAlarmWord_ISA_LL := udiAlarmWord_ISA_LL OR SHL(DWORD#1, 5); END_IF;
IF bAlarmLatched_HH[7] THEN udiAlarmWord_ISA_HH := udiAlarmWord_ISA_HH OR SHL(DWORD#1, 6); END_IF;
IF bAlarmLatched_H[7]  THEN udiAlarmWord_ISA_H  := udiAlarmWord_ISA_H  OR SHL(DWORD#1, 6); END_IF;
IF bAlarmLatched_L[7]  THEN udiAlarmWord_ISA_L  := udiAlarmWord_ISA_L  OR SHL(DWORD#1, 6); END_IF;
IF bAlarmLatched_LL[7] THEN udiAlarmWord_ISA_LL := udiAlarmWord_ISA_LL OR SHL(DWORD#1, 6); END_IF;
IF bAlarmLatched_HH[8] THEN udiAlarmWord_ISA_HH := udiAlarmWord_ISA_HH OR SHL(DWORD#1, 7); END_IF;
IF bAlarmLatched_H[8]  THEN udiAlarmWord_ISA_H  := udiAlarmWord_ISA_H  OR SHL(DWORD#1, 7); END_IF;
IF bAlarmLatched_L[8]  THEN udiAlarmWord_ISA_L  := udiAlarmWord_ISA_L  OR SHL(DWORD#1, 7); END_IF;
IF bAlarmLatched_LL[8] THEN udiAlarmWord_ISA_LL := udiAlarmWord_ISA_LL OR SHL(DWORD#1, 7); END_IF;
IF bAlarmLatched_HH[9] THEN udiAlarmWord_ISA_HH := udiAlarmWord_ISA_HH OR SHL(DWORD#1, 8); END_IF;
IF bAlarmLatched_H[9]  THEN udiAlarmWord_ISA_H  := udiAlarmWord_ISA_H  OR SHL(DWORD#1, 8); END_IF;
IF bAlarmLatched_L[9]  THEN udiAlarmWord_ISA_L  := udiAlarmWord_ISA_L  OR SHL(DWORD#1, 8); END_IF;
IF bAlarmLatched_LL[9] THEN udiAlarmWord_ISA_LL := udiAlarmWord_ISA_LL OR SHL(DWORD#1, 8); END_IF;
IF bAlarmLatched_HH[10] THEN udiAlarmWord_ISA_HH := udiAlarmWord_ISA_HH OR SHL(DWORD#1, 9); END_IF;
IF bAlarmLatched_H[10]  THEN udiAlarmWord_ISA_H  := udiAlarmWord_ISA_H  OR SHL(DWORD#1, 9); END_IF;
IF bAlarmLatched_L[10]  THEN udiAlarmWord_ISA_L  := udiAlarmWord_ISA_L  OR SHL(DWORD#1, 9); END_IF;
IF bAlarmLatched_LL[10] THEN udiAlarmWord_ISA_LL := udiAlarmWord_ISA_LL OR SHL(DWORD#1, 9); END_IF;

END_FUNCTION_BLOCK