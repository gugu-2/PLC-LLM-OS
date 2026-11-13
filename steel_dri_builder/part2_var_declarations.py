# steel_dri_builder/part2_var_declarations.py
"""
Part 2: Comprehensive internal VAR declarations
"""

def get_var_declarations():
    return """VAR
    (* Execution Heartbeat and Scan Tracking *)
    bInitialized                        : BOOL := FALSE;       (* System State-Space & Parameter Initialization Complete Flag *)
    udiScanCounter                      : UDINT := 0;          (* Monotonic Discrete PLC Scan Execution Cycle Counter *)
    udiHeartbeatCounter                 : UDINT := 0;          (* Diagnostic Flasher Heartbeat Accumulator *)
    bHeartbeatBit                       : BOOL := FALSE;       (* Alternating Diagnostic Heartbeat Telemetry Bit *)
    rTs_Seconds                         : REAL := 0.025;       (* Execution Period Converted to Float Seconds [s] *)

    (* Cyber-Physical State-Space Dynamic Vectors (8 States, 6 Inputs, 6 Outputs) *)
    (* x1: Bustle Gas Inlet Temp [deg C]                                          *)
    (* x2: Mid-Shaft Reduction Zone Metallization Degree [% Fe]                   *)
    (* x3: Shaft Upper-to-Lower Differential Pressure [kPa]                       *)
    (* x4: Top Gas H2/CO Molar Ratio [ratio]                                      *)
    (* x5: Top Gas CO2 Concentration [% vol]                                      *)
    (* x6: Discharged DRI Carbon Content [wt% C]                                  *)
    (* x7: Cooling Zone Bottom Gas Discharge Temperature [deg C]                  *)
    (* x8: Discharge Screw Feeder Linear Mass Extraction Rate [t/h]               *)
    x_State                             : ARRAY[1..8] OF REAL; (* Discrete System Physical State Vector x[k] *)
    x_Hat                               : ARRAY[1..8] OF REAL; (* Luenberger Full-State Observer Estimated Vector x_hat[k] *)
    x_Pred                              : ARRAY[1..8] OF REAL; (* Open-Loop One-Step Ahead State Prediction Vector x_pred[k+1] *)
    x_Ref                               : ARRAY[1..8] OF REAL; (* Target Operating Trajectory Equilibrium Setpoint Vector x_ref *)
    y_Meas                              : ARRAY[1..6] OF REAL; (* Process Sensor Robustly Voted Measurement Vector y[k] *)
    y_Hat                               : ARRAY[1..6] OF REAL; (* Estimated Observer Measurement Output Vector y_hat[k] *)
    y_Innov                             : ARRAY[1..6] OF REAL; (* Innovation / Estimation Error Residual Vector (y - y_hat) *)
    u_Act                               : ARRAY[1..6] OF REAL; (* Synthesized Actuator Command Vector u[k] [0..100%] *)
    u_Prev                              : ARRAY[1..6] OF REAL; (* Previous Execution Cycle Actuator Output Vector u[k-1] *)
    du_Act                              : ARRAY[1..6] OF REAL; (* First-Difference Actuator Slew Rate Vector du[k] = u[k] - u[k-1] *)
    u_Ref                               : ARRAY[1..6] OF REAL; (* Nominal Stationary Feedforward Operating Inputs *)

    (* Discrete Cyber-Physical State-Space Non-Zero Transition Matrices *)
    matA                                : ARRAY[1..8, 1..8] OF REAL; (* System Dynamic Evolution Matrix A (8x8) *)
    matB                                : ARRAY[1..8, 1..6] OF REAL; (* Actuator Input Control Gain Coupling Matrix B (8x6) *)
    matC                                : ARRAY[1..6, 1..8] OF REAL; (* Sensor State Output Measurement Matrix C (6x8) *)
    matD                                : ARRAY[1..6, 1..6] OF REAL; (* Feedthrough Direct Transmission Matrix D (6x6) *)
    matL                                : ARRAY[1..8, 1..6] OF REAL; (* Steady-State Luenberger Observer Gain Matrix L (8x6) *)

    (* Model Predictive Control (MPC) Cost Weight Matrices & Variables *)
    matQ                                : ARRAY[1..8, 1..8] OF REAL; (* State Trajectory Tracking Penalty Weight Matrix Q (8x8) *)
    matR                                : ARRAY[1..6, 1..6] OF REAL; (* Actuator Slew and Control Effort Penalty Matrix R (6x6) *)
    matP                                : ARRAY[1..8, 1..8] OF REAL; (* Terminal Horizon Penalty Matrix P (8x8) *)

    (* Receding Horizon MPC Optimization Workspace (Horizon N=5, Iterations=6) *)
    u_MPC_Trajectory                    : ARRAY[1..5, 1..6] OF REAL; (* Receding Control Horizon Sequences u[k+n|k] *)
    grad_MPC                            : ARRAY[1..5, 1..6] OF REAL; (* Objective Function Projected Gradient Vectors *)
    x_MPC_Predict                       : ARRAY[1..5, 1..8] OF REAL; (* Forward State Trajectory Predictions over Horizon *)
    u_Min                               : ARRAY[1..6] OF REAL;       (* Actuator Hard Saturation Lower Bounds [%] *)
    u_Max                               : ARRAY[1..6] OF REAL;       (* Actuator Hard Saturation Upper Bounds [%] *)
    du_MaxSlew                          : ARRAY[1..6] OF REAL;       (* Actuator Maximum Allowable Slew Rates [% / cycle] *)
    rPGD_StepSize                       : REAL := 0.0150;            (* Projected Gradient Descent Learning Rate Step Alpha *)
    rMPC_Lambda_H2Syngas                : REAL := 0.4200;            (* Dynamic H2 / Syngas Gas Mix Decoupling Cross-Weight *)
    rMPC_Lambda_CarbDep                 : REAL := 0.3150;            (* Natural Gas Carburization vs Thermal Penalty Cross-Weight *)

    (* 2oo3 TMR Sensor Voting Suite Data Records *)
    (* Channel 1: Bustle Pipe Temperature *)
    rTMR_Bustle_DevAB                   : REAL := 0.0;
    rTMR_Bustle_DevBC                   : REAL := 0.0;
    rTMR_Bustle_DevAC                   : REAL := 0.0;
    bTMR_Bustle_DiscAB                  : BOOL := FALSE;
    bTMR_Bustle_DiscBC                  : BOOL := FALSE;
    bTMR_Bustle_DiscAC                  : BOOL := FALSE;
    tTMR_Bustle_TimerAB                 : TIME := T#0ms;
    tTMR_Bustle_TimerBC                 : TIME := T#0ms;
    tTMR_Bustle_TimerAC                 : TIME := T#0ms;
    bTMR_Bustle_FaultA                  : BOOL := FALSE;
    bTMR_Bustle_FaultB                  : BOOL := FALSE;
    bTMR_Bustle_FaultC                  : BOOL := FALSE;
    bTMR_Bustle_Degraded                : BOOL := FALSE;
    bTMR_Bustle_Critical                : BOOL := FALSE;
    rTMR_Bustle_LastGood                : REAL := 950.0;

    (* Channel 2: Shaft Differential Pressure *)
    rTMR_ShaftDP_DevAB                  : REAL := 0.0;
    rTMR_ShaftDP_DevBC                  : REAL := 0.0;
    rTMR_ShaftDP_DevAC                  : REAL := 0.0;
    bTMR_ShaftDP_DiscAB                 : BOOL := FALSE;
    bTMR_ShaftDP_DiscBC                 : BOOL := FALSE;
    bTMR_ShaftDP_DiscAC                 : BOOL := FALSE;
    tTMR_ShaftDP_TimerAB                : TIME := T#0ms;
    tTMR_ShaftDP_TimerBC                : TIME := T#0ms;
    tTMR_ShaftDP_TimerAC                : TIME := T#0ms;
    bTMR_ShaftDP_FaultA                 : BOOL := FALSE;
    bTMR_ShaftDP_FaultB                 : BOOL := FALSE;
    bTMR_ShaftDP_FaultC                 : BOOL := FALSE;
    bTMR_ShaftDP_Degraded               : BOOL := FALSE;
    bTMR_ShaftDP_Critical               : BOOL := FALSE;
    rTMR_ShaftDP_LastGood               : REAL := 52.0;

    (* Channel 3: Top Gas H2/CO Ratio *)
    rTMR_GasH2CO_DevAB                  : REAL := 0.0;
    rTMR_GasH2CO_DevBC                  : REAL := 0.0;
    rTMR_GasH2CO_DevAC                  : REAL := 0.0;
    bTMR_GasH2CO_DiscAB                 : BOOL := FALSE;
    bTMR_GasH2CO_DiscBC                 : BOOL := FALSE;
    bTMR_GasH2CO_DiscAC                 : BOOL := FALSE;
    tTMR_GasH2CO_TimerAB                : TIME := T#0ms;
    tTMR_GasH2CO_TimerBC                : TIME := T#0ms;
    tTMR_GasH2CO_TimerAC                : TIME := T#0ms;
    bTMR_GasH2CO_FaultA                 : BOOL := FALSE;
    bTMR_GasH2CO_FaultB                 : BOOL := FALSE;
    bTMR_GasH2CO_FaultC                 : BOOL := FALSE;
    bTMR_GasH2CO_Degraded               : BOOL := FALSE;
    bTMR_GasH2CO_Critical               : BOOL := FALSE;
    rTMR_GasH2CO_LastGood               : REAL := 2.85;

    (* Channel 4: Top Gas CO2 Fraction *)
    rTMR_GasCO2_DevAB                   : REAL := 0.0;
    rTMR_GasCO2_DevBC                   : REAL := 0.0;
    rTMR_GasCO2_DevAC                   : REAL := 0.0;
    bTMR_GasCO2_DiscAB                  : BOOL := FALSE;
    bTMR_GasCO2_DiscBC                  : BOOL := FALSE;
    bTMR_GasCO2_DiscAC                  : BOOL := FALSE;
    tTMR_GasCO2_TimerAB                 : TIME := T#0ms;
    tTMR_GasCO2_TimerBC                 : TIME := T#0ms;
    tTMR_GasCO2_TimerAC                 : TIME := T#0ms;
    bTMR_GasCO2_FaultA                  : BOOL := FALSE;
    bTMR_GasCO2_FaultB                  : BOOL := FALSE;
    bTMR_GasCO2_FaultC                  : BOOL := FALSE;
    bTMR_GasCO2_Degraded                : BOOL := FALSE;
    bTMR_GasCO2_Critical                : BOOL := FALSE;
    rTMR_GasCO2_LastGood                : REAL := 15.2;

    (* Channel 5: Burden Level Profiler *)
    rTMR_Burden_DevAB                   : REAL := 0.0;
    rTMR_Burden_DevBC                   : REAL := 0.0;
    rTMR_Burden_DevAC                   : REAL := 0.0;
    bTMR_Burden_DiscAB                  : BOOL := FALSE;
    bTMR_Burden_DiscBC                  : BOOL := FALSE;
    bTMR_Burden_DiscAC                  : BOOL := FALSE;
    tTMR_Burden_TimerAB                 : TIME := T#0ms;
    tTMR_Burden_TimerBC                 : TIME := T#0ms;
    tTMR_Burden_TimerAC                 : TIME := T#0ms;
    bTMR_Burden_FaultA                  : BOOL := FALSE;
    bTMR_Burden_FaultB                  : BOOL := FALSE;
    bTMR_Burden_FaultC                  : BOOL := FALSE;
    bTMR_Burden_Degraded                : BOOL := FALSE;
    bTMR_Burden_Critical                : BOOL := FALSE;
    rTMR_Burden_LastGood                : REAL := 18.5;

    (* Channel 6: Discharged DRI Pyrometer *)
    rTMR_DRITemp_DevAB                  : REAL := 0.0;
    rTMR_DRITemp_DevBC                  : REAL := 0.0;
    rTMR_DRITemp_DevAC                  : REAL := 0.0;
    bTMR_DRITemp_DiscAB                 : BOOL := FALSE;
    bTMR_DRITemp_DiscBC                 : BOOL := FALSE;
    bTMR_DRITemp_DiscAC                 : BOOL := FALSE;
    tTMR_DRITemp_TimerAB                : TIME := T#0ms;
    tTMR_DRITemp_TimerBC                : TIME := T#0ms;
    tTMR_DRITemp_TimerAC                : TIME := T#0ms;
    bTMR_DRITemp_FaultA                 : BOOL := FALSE;
    bTMR_DRITemp_FaultB                 : BOOL := FALSE;
    bTMR_DRITemp_FaultC                 : BOOL := FALSE;
    bTMR_DRITemp_Degraded               : BOOL := FALSE;
    bTMR_DRITemp_Critical               : BOOL := FALSE;
    rTMR_DRITemp_LastGood               : REAL := 680.0;

    (* Deterministic 14-Stage Steelmaking Finite State Machine Variables *)
    iState                              : INT := 0;            (* Internal Active State Machine Register *)
    iPrevState                          : INT := -1;           (* Previous Scan State Machine Register *)
    tCurrentStateDwell                  : TIME := T#0ms;       (* Total Time Elapsed in Current FSM State *)
    iFSM_SubPhase                       : INT := 0;            (* Internal Sub-Phase Step within Active State *)
    rFSM_RampGenerator                  : REAL := 0.0;         (* Dynamic Trajectory Linear Ramp Variable *)
    rFSM_HeaterRampSP                   : REAL := 25.0;        (* Warmup Ramp Bustle Temperature Setpoint [deg C] *)
    rFSM_H2FractionRamp                 : REAL := 0.0;         (* Hydrogen Enrichment Ramp Fraction [0..100%] *)
    bClusterPulseActive                 : BOOL := FALSE;       (* Sticking Cluster Breaker Pulsing State Flag *)
    tClusterPulseTimer                  : TIME := T#0ms;       (* Duration Timer for Cluster Breaker Shock Blast *)
    udiClusterPulseCounter              : UDINT := 0;          (* Number of Blasts Dispatched to Shake Burden *)
    rCluster_DeltaP_Baseline            : REAL := 50.0;        (* Baseline DP for Hang Detection Reference [kPa] *)
    tSnortDumpDuration                  : TIME := T#0ms;       (* Elapsed Duration in Snort Depressurization Dump *)
    tDoubleBlockBleedTimer              : TIME := T#0ms;       (* SIL-3 Double Block and Bleed Execution Latency Timer *)

    (* ISA-18.2 Multi-Tier Process Alarm Configuration & Dynamic State *)
    (* Bustle Temperature Alarm Boundaries *)
    rLimit_Bustle_HH                    : REAL := 1050.0;      (* Bustle Pipe High-High Refractory Protection [deg C] *)
    rLimit_Bustle_H                     : REAL := 1000.0;      (* Bustle Pipe High Warning [deg C] *)
    rLimit_Bustle_L                     : REAL := 890.0;       (* Bustle Pipe Low Warning [deg C] *)
    rLimit_Bustle_LL                    : REAL := 830.0;       (* Bustle Pipe Low-Low Metallization Collapse [deg C] *)
    rHyst_Bustle                        : REAL := 8.0;         (* Bustle Pipe Temperature Alarm Deadband [deg C] *)
    bAlarm_Bustle_HH                    : BOOL := FALSE;
    bAlarm_Bustle_H                     : BOOL := FALSE;
    bAlarm_Bustle_L                     : BOOL := FALSE;
    bAlarm_Bustle_LL                    : BOOL := FALSE;

    (* Shaft Differential Pressure Alarm Boundaries *)
    rLimit_ShaftDP_HH                   : REAL := 82.0;        (* Shaft DP High-High Severe Hang / Clinker [kPa] *)
    rLimit_ShaftDP_H                    : REAL := 72.0;        (* Shaft DP High Early Sticking Warning [kPa] *)
    rLimit_ShaftDP_L                    : REAL := 30.0;        (* Shaft DP Low Gas Channeling / Void Warning [kPa] *)
    rLimit_ShaftDP_LL                   : REAL := 18.0;        (* Shaft DP Low-Low Gas Blow-Through [kPa] *)
    rHyst_ShaftDP                       : REAL := 3.0;         (* Shaft DP Deadband [kPa] *)
    bAlarm_ShaftDP_HH                   : BOOL := FALSE;
    bAlarm_ShaftDP_H                    : BOOL := FALSE;
    bAlarm_ShaftDP_L                    : BOOL := FALSE;
    bAlarm_ShaftDP_LL                   : BOOL := FALSE;

    (* Top Gas H2/CO Ratio Alarm Boundaries *)
    rLimit_GasH2CO_HH                   : REAL := 5.20;        (* Top Gas H2/CO Ratio High-High Syngas Starvation [ratio] *)
    rLimit_GasH2CO_H                    : REAL := 4.20;        (* Top Gas H2/CO Ratio High [ratio] *)
    rLimit_GasH2CO_L                    : REAL := 1.80;        (* Top Gas H2/CO Ratio Low H2 Starvation [ratio] *)
    rLimit_GasH2CO_LL                   : REAL := 1.20;        (* Top Gas H2/CO Ratio Low-Low Inadequate Reduction [ratio] *)
    rHyst_GasH2CO                       : REAL := 0.15;        (* Top Gas H2/CO Deadband [ratio] *)
    bAlarm_GasH2CO_HH                   : BOOL := FALSE;
    bAlarm_GasH2CO_H                    : BOOL := FALSE;
    bAlarm_GasH2CO_L                    : BOOL := FALSE;
    bAlarm_GasH2CO_LL                   : BOOL := FALSE;

    (* Discharged DRI Carbon Alarm Boundaries *)
    rLimit_Carbon_HH                    : REAL := 3.60;        (* DRI Product Carbon High-High Sooting Hazard [wt% C] *)
    rLimit_Carbon_H                     : REAL := 3.00;        (* DRI Product Carbon High Warning [wt% C] *)
    rLimit_Carbon_L                     : REAL := 1.50;        (* DRI Product Carbon Low EAF Penalty [wt% C] *)
    rLimit_Carbon_LL                    : REAL := 1.00;        (* DRI Product Carbon Low-Low Re-Oxidation Hazard [wt% C] *)
    rHyst_Carbon                        : REAL := 0.10;        (* Product Carbon Deadband [wt% C] *)
    bAlarm_Carbon_HH                    : BOOL := FALSE;
    bAlarm_Carbon_H                     : BOOL := FALSE;
    bAlarm_Carbon_L                     : BOOL := FALSE;
    bAlarm_Carbon_LL                    : BOOL := FALSE;

    (* SIL-3 Fast Oxygen Ingress Protection Variables *)
    rO2_Max_Safety_Trip                 : REAL := 0.12;        (* Strict Upper Oxygen Ingress Deflagration Trip Limit [% vol] *)
    rO2_Max_RateOfRise                  : REAL := 0.04;        (* Maximum Allowable Rate of O2 Increase [% vol / s] *)
    rO2_Prev_Inlet                      : REAL := 0.02;        (* Previous Cycle O2 Measurement for Rate Derivation [% vol] *)
    rO2_Inlet_Rate                      : REAL := 0.0;         (* Instantaneous O2 Concentration Rate of Rise [% vol / s] *)
    bO2_Ingress_InterlockTripped        : BOOL := FALSE;       (* Latched Oxygen Ingress Fast SIS Interlock *)

    (* Anti-Stiction Dither & Linearization Variables *)
    rDither_Frequency                   : REAL := 2.5;         (* Micro-Dither Frequency for Valve Packing Anti-Stiction [Hz] *)
    rDither_Amplitude                   : REAL := 0.45;        (* Micro-Dither Stroke Modulation Amplitude [%] *)
    rDither_Phase                       : REAL := 0.0;         (* Dither Angle Oscillator Phase Radians *)
    rDither_Signal                      : REAL := 0.0;         (* Instantaneous High-Frequency Dither Waveform [%] *)

    (* Historical Rolling Buffers for Kinetic Estimation *)
    arrHist_Metallization               : ARRAY[1..16] OF REAL;(* Rolling History of Estimated Metallization [% Fe] *)
    arrHist_ShaftDP                     : ARRAY[1..16] OF REAL;(* Rolling History of Shaft Differential Pressure [kPa] *)
    iHistIndex                          : INT := 1;            (* Rolling Circular History Ring Index *)
    rFilter_Metallization_SMA           : REAL := 95.0;        (* Moving Average Smoothed Metallization [% Fe] *)
    rFilter_ShaftDP_SMA                 : REAL := 52.0;        (* Moving Average Smoothed Shaft DP [kPa] *)

    (* Loop Counters and Optimization Workspace Indexers *)
    idx_i                               : INT := 1;
    idx_j                               : INT := 1;
    idx_k                               : INT := 1;
    idx_n                               : INT := 1;
    idx_iter                            : INT := 1;
    idx_h                               : INT := 1;
    rTempSum                            : REAL := 0.0;
    rGradSum                            : REAL := 0.0;
    rPGD_ProjVal                        : REAL := 0.0;
    rSlewDelta                          : REAL := 0.0;
END_VAR
"""
