# trt_builder/st_var.py
"""
VAR internal declarations for FB_Steel_BlastFurnace_TopGas_TRT_PowerRecovery
"""

def get_var_declarations():
    return """VAR
    (* Initialization & First Scan Control *)
    bInitialized                    : BOOL := FALSE;    (* Power-On Cold Start Initialization Complete Flag *)
    bFirstScanDone                  : BOOL := FALSE;    (* One-Shot First Scan Logic Completion Bit *)
    nCycleCounter                   : UDINT := 0;       (* Execution Cycle Heartbeat Counter (Ts = 10 ms) *)
    rSamplingTime_s                 : REAL := 0.010;    (* Discrete Base PLC Scan Time Delta [s] *)

    (* Finite State Machine Operational Stage Definitions *)
    eFsmCurrentState                : INT := 0;         (* Active Operational State Register (0 to 13) *)
    eFsmPreviousState               : INT := 0;         (* Previous Cycle Execution State Register *)
    nFsmStateStep                   : INT := 0;         (* Sub-State Sequence Step Index *)
    nFsmStateTimer_ms               : UDINT := 0;       (* Monotonic Dwell Timer for Current State [ms] *)
    nPurgeTimer_ms                  : UDINT := 0;       (* Nitrogen Casing Inert Purge Accumulator [ms] *)
    nWarmupTimer_ms                 : UDINT := 0;       (* Turbine Casing Pre-Heating Warmup Timer [ms] *)
    nCriticalBandTimer_ms           : UDINT := 0;       (* Critical Resonance Speed Acceleration Watchdog [ms] *)
    nSyncWatchdog_ms                : UDINT := 0;       (* Grid Synchronization Dwell Watchdog [ms] *)
    nBreakerCloseTimer_ms           : UDINT := 0;       (* 52G Breaker Close Acknowledge Timer [ms] *)
    nScouringCycleTimer_ms          : UDINT := 0;       (* Blade Washing Solvent/Water Injection Timer [ms] *)
    nScouringInterval_s             : UDINT := 28800;   (* 8-Hour Interval Between Scouring Cycles [s] *)
    nScouringAccumulator_s          : UDINT := 0;       (* Run-Time Clock Accumulator for Blade Washing [s] *)
    nUnloadingRampTimer_ms          : UDINT := 0;       (* Controlled Shutdown Desynchronization Timer [ms] *)
    nTripClearTimer_ms              : UDINT := 0;       (* Trip Latch Hardware Reset Holdoff Timer [ms] *)

    (* ========================================================================= *)
    (* CYBER-PHYSICAL DISCRETE STATE-SPACE ARRAYS & MATRICES (Ts = 10 ms)        *)
    (* States x[8]:                                                              *)
    (*   x[1] = Top gas plenum pressure deviation delta_Ptop [kPa]               *)
    (*   x[2] = Turbine inlet nozzle box pressure deviation delta_Pnoz [kPa]     *)
    (*   x[3] = Turbine mass flow rate mdot_trt [kg/s]                           *)
    (*   x[4] = Septum valve bank total mass flow rate mdot_septum [kg/s]        *)
    (*   x[5] = Rotor mechanical rotational speed deviation delta_omega [rad/s]  *)
    (*   x[6] = Generator active electrical power output P_elec [MW]             *)
    (*   x[7] = Dry bag filter differential pressure delta_Pbf [kPa]             *)
    (*   x[8] = Shaft journal radial vibration displacement V_shaft [um]         *)
    (* Control Inputs u[5]:                                                      *)
    (*   u[1] = TRT Variable Stator Vane (VSV) angular demand [%]                *)
    (*   u[2] = Septum Valve 1 (Coarse Throttling Bypass) position demand [%]   *)
    (*   u[3] = Septum Valve 2 (Intermediate Throttling) position demand [%]    *)
    (*   u[4] = Septum Valve 3 (High-Speed Fine Pressure Trim) position [%]     *)
    (*   u[5] = Generator excitation torque / load demand trim [%]               *)
    (* Measurements y[6]:                                                        *)
    (*   y[1] = Voted Top Gas Pressure PT-101 [kPa]                              *)
    (*   y[2] = Voted Turbine Inlet Pressure PT-201 [kPa]                        *)
    (*   y[3] = Voted Top Gas Mass Flow FT-301 [kg/s]                            *)
    (*   y[4] = Voted Generator Active Power WT-401 [MW]                         *)
    (*   y[5] = Voted Shaft Radial Vibration VT-501 [um]                         *)
    (*   y[6] = Voted Bag Filter Differential Pressure DPT-601 [kPa]             *)
    (* ========================================================================= *)
    aStateEst                       : ARRAY[1..8] OF REAL;  (* Luenberger Observed State Vector x_hat[k] *)
    aStatePred                      : ARRAY[1..8] OF REAL;  (* Propagated Prior State Prediction x_hat[k+1|k] *)
    aStateMeas                      : ARRAY[1..6] OF REAL;  (* Filtered Process Sensor Observation Vector y[k] *)
    aObsInnovation                  : ARRAY[1..6] OF REAL;  (* Observer Innovation Residual Error e_y = y - C*x_hat *)
    aControlDemand                  : ARRAY[1..5] OF REAL;  (* Final Actuator Control Output Vector u[k] *)
    aControlPrev                    : ARRAY[1..5] OF REAL;  (* Previous Cycle Actuator Vector u[k-1] *)
    aDisturbanceEst                 : ARRAY[1..4] OF REAL;  (* Exogenous Disturbance Estimator Vector w[k] *)

    (* State-Space Model Parameter Matrices *)
    mA                              : ARRAY[1..8, 1..8] OF REAL; (* Discrete System Dynamics Matrix A (8x8) *)
    mB                              : ARRAY[1..8, 1..5] OF REAL; (* Discrete Actuator Control Input Matrix B (8x5) *)
    mC                              : ARRAY[1..6, 1..8] OF REAL; (* Sensor Output Observation Matrix C (6x8) *)
    mD                              : ARRAY[1..6, 1..5] OF REAL; (* Direct Feedthrough Matrix D (6x5) *)
    mK                              : ARRAY[1..8, 1..6] OF REAL; (* Steady-State Luenberger Observer Gain K (8x6) *)

    (* Model Predictive Control (MPC) Cost Weighting & Sensitivity Matrices *)
    mQ                              : ARRAY[1..8, 1..8] OF REAL; (* MPC State Tracking Quadratic Penalty Matrix Q (8x8) *)
    mR                              : ARRAY[1..5, 1..5] OF REAL; (* MPC Actuator Rate Quadratic Penalty Matrix R (5x5) *)
    mP                              : ARRAY[1..8, 1..8] OF REAL; (* Terminal Horizon Penalty Matrix P (8x8) *)

    (* Receding-Horizon MPC Rolling Prediction Buffers (Np = 5, Nc = 3) *)
    aMpcPredState                   : ARRAY[1..5, 1..8] OF REAL; (* Predicted Trajectory Over Np Steps *)
    aMpcDeltaU                      : ARRAY[1..3, 1..5] OF REAL; (* Candidate Actuator Adjustments Over Nc Steps *)
    aMpcGradU                       : ARRAY[1..3, 1..5] OF REAL; (* Unrolled Projected Gradient Descent Gradients *)
    aMpcStepSize                    : ARRAY[1..5] OF REAL;       (* PGD Iterative Gradient Learning Rates *)
    rMpcObjectiveCost               : REAL := 0.0;               (* Evaluated Multi-Variable Cost Functional J *)
    rMpcStateCost                   : REAL := 0.0;               (* Instantaneous Tracking Quadratic Cost Component *)
    rMpcInputCost                   : REAL := 0.0;               (* Actuator Movement Quadratic Cost Component *)
    rMpcTerminalCost                : REAL := 0.0;               (* Terminal Boundary Cost Component *)

    (* Actuator Physical Saturation & Slew Limits *)
    aActuatorMinLimit               : ARRAY[1..5] OF REAL; (* Actuator Lower Stroke Clamping Limits [%] *)
    aActuatorMaxLimit               : ARRAY[1..5] OF REAL; (* Actuator Upper Stroke Clamping Limits [%] *)
    aActuatorMaxSlewRate            : ARRAY[1..5] OF REAL; (* Actuator Maximum Velocity Bound [% per 10 ms] *)

    (* ========================================================================= *)
    (* 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING SUITE DATA STRUCTURES  *)
    (* ========================================================================= *)
    (* Channel 1: Top Gas Pressure PT-101 (kPa) *)
    rCh1_ValA                       : REAL := 250.0;
    rCh1_ValB                       : REAL := 250.0;
    rCh1_ValC                       : REAL := 250.0;
    bCh1_HealthA                    : BOOL := TRUE;
    bCh1_HealthB                    : BOOL := TRUE;
    bCh1_HealthC                    : BOOL := TRUE;
    nCh1_TimerA                     : UDINT := 0;
    nCh1_TimerB                     : UDINT := 0;
    nCh1_TimerC                     : UDINT := 0;
    nCh1_HealthyCount               : INT := 3;
    rCh1_Voted                      : REAL := 250.0;
    rCh1_PrevVoted                  : REAL := 250.0;
    rCh1_FilteredROC                : REAL := 0.0;
    bCh1_DegradedLatch              : BOOL := FALSE;
    bCh1_TotalFailureLatch          : BOOL := FALSE;

    (* Channel 2: Turbine Inlet Pressure PT-201 (kPa) *)
    rCh2_ValA                       : REAL := 245.0;
    rCh2_ValB                       : REAL := 245.0;
    rCh2_ValC                       : REAL := 245.0;
    bCh2_HealthA                    : BOOL := TRUE;
    bCh2_HealthB                    : BOOL := TRUE;
    bCh2_HealthC                    : BOOL := TRUE;
    nCh2_TimerA                     : UDINT := 0;
    nCh2_TimerB                     : UDINT := 0;
    nCh2_TimerC                     : UDINT := 0;
    nCh2_HealthyCount               : INT := 3;
    rCh2_Voted                      : REAL := 245.0;
    rCh2_PrevVoted                  : REAL := 245.0;
    bCh2_DegradedLatch              : BOOL := FALSE;
    bCh2_TotalFailureLatch          : BOOL := FALSE;

    (* Channel 3: Top Gas Mass Flow FT-301 (kg/s) *)
    rCh3_ValA                       : REAL := 210.0;
    rCh3_ValB                       : REAL := 210.0;
    rCh3_ValC                       : REAL := 210.0;
    bCh3_HealthA                    : BOOL := TRUE;
    bCh3_HealthB                    : BOOL := TRUE;
    bCh3_HealthC                    : BOOL := TRUE;
    nCh3_TimerA                     : UDINT := 0;
    nCh3_TimerB                     : UDINT := 0;
    nCh3_TimerC                     : UDINT := 0;
    nCh3_HealthyCount               : INT := 3;
    rCh3_Voted                      : REAL := 210.0;
    rCh3_PrevVoted                  : REAL := 210.0;
    bCh3_DegradedLatch              : BOOL := FALSE;
    bCh3_TotalFailureLatch          : BOOL := FALSE;

    (* Channel 4: Generator Active Power WT-401 (MW) *)
    rCh4_ValA                       : REAL := 0.0;
    rCh4_ValB                       : REAL := 0.0;
    rCh4_ValC                       : REAL := 0.0;
    bCh4_HealthA                    : BOOL := TRUE;
    bCh4_HealthB                    : BOOL := TRUE;
    bCh4_HealthC                    : BOOL := TRUE;
    nCh4_TimerA                     : UDINT := 0;
    nCh4_TimerB                     : UDINT := 0;
    nCh4_TimerC                     : UDINT := 0;
    nCh4_HealthyCount               : INT := 3;
    rCh4_Voted                      : REAL := 0.0;
    rCh4_PrevVoted                  : REAL := 0.0;
    bCh4_DegradedLatch              : BOOL := FALSE;
    bCh4_TotalFailureLatch          : BOOL := FALSE;

    (* Channel 5: Turbine Radial Vibration VT-501 (um) *)
    rCh5_ValA                       : REAL := 12.0;
    rCh5_ValB                       : REAL := 12.0;
    rCh5_ValC                       : REAL := 12.0;
    bCh5_HealthA                    : BOOL := TRUE;
    bCh5_HealthB                    : BOOL := TRUE;
    bCh5_HealthC                    : BOOL := TRUE;
    nCh5_TimerA                     : UDINT := 0;
    nCh5_TimerB                     : UDINT := 0;
    nCh5_TimerC                     : UDINT := 0;
    nCh5_HealthyCount               : INT := 3;
    rCh5_Voted                      : REAL := 12.0;
    rCh5_PrevVoted                  : REAL := 12.0;
    bCh5_DegradedLatch              : BOOL := FALSE;
    bCh5_TotalFailureLatch          : BOOL := FALSE;

    (* Channel 6: Bag Filter Differential Pressure DPT-601 (kPa) *)
    rCh6_ValA                       : REAL := 5.2;
    rCh6_ValB                       : REAL := 5.2;
    rCh6_ValC                       : REAL := 5.2;
    bCh6_HealthA                    : BOOL := TRUE;
    bCh6_HealthB                    : BOOL := TRUE;
    bCh6_HealthC                    : BOOL := TRUE;
    nCh6_TimerA                     : UDINT := 0;
    nCh6_TimerB                     : UDINT := 0;
    nCh6_TimerC                     : UDINT := 0;
    nCh6_HealthyCount               : INT := 3;
    rCh6_Voted                      : REAL := 5.2;
    rCh6_PrevVoted                  : REAL := 5.2;
    bCh6_DegradedLatch              : BOOL := FALSE;
    bCh6_TotalFailureLatch          : BOOL := FALSE;

    (* Dual Redundant Turbine Speed Transmitters ST-101A/B (rpm) *)
    rSpeed_RawA                     : REAL := 0.0;
    rSpeed_RawB                     : REAL := 0.0;
    rSpeed_Voted                    : REAL := 0.0;
    rSpeed_Prev                     : REAL := 0.0;
    rSpeed_ROC                      : REAL := 0.0;
    bSpeed_SensorA_Healthy          : BOOL := TRUE;
    bSpeed_SensorB_Healthy          : BOOL := TRUE;
    nSpeed_DiscrepancyTimer_ms      : UDINT := 0;

    (* TMR Discrepancy Debounce Threshold Limits *)
    rTMR_TolPressTop                : REAL := 6.0;      (* Permissible PT-101 Inter-Channel Delta [kPa] *)
    rTMR_TolPressNozzle             : REAL := 6.0;      (* Permissible PT-201 Inter-Channel Delta [kPa] *)
    rTMR_TolFlow                    : REAL := 15.0;     (* Permissible FT-301 Inter-Channel Delta [kg/s] *)
    rTMR_TolPower                   : REAL := 1.2;      (* Permissible WT-401 Inter-Channel Delta [MW] *)
    rTMR_TolVib                     : REAL := 5.0;      (* Permissible VT-501 Inter-Channel Delta [um] *)
    rTMR_TolDiffPress               : REAL := 1.2;      (* Permissible DPT-601 Inter-Channel Delta [kPa] *)
    rTMR_TolSpeed                   : REAL := 45.0;     (* Permissible ST-101 Inter-Channel Delta [rpm] *)
    nDiscrepancyTripDelay_ms        : UDINT := 1500;    (* Discrepancy Fault Debounce Duration (1.5 s) [ms] *)

    (* ========================================================================= *)
    (* FIRST-PRINCIPLES THERMODYNAMIC & CYBER-PHYSICAL MODEL REGISTERS           *)
    (* ========================================================================= *)
    rGasConstantUniversal           : REAL := 8314.46;  (* Universal Molar Gas Constant Ru [J/(kmol*K)] *)
    rTopGasMolarMass                : REAL := 29.85;    (* Average Blast Furnace Top Gas Molar Mass [kg/kmol] *)
    rGasConstantSpecific            : REAL := 278.54;   (* Top Gas Specific Constant R_spec [J/(kg*K)] *)
    rGasSpecificHeat_Cp             : REAL := 1045.0;   (* Top Gas Isobaric Heat Capacity Cp [J/(kg*K)] *)
    rGasSpecificHeat_Cv             : REAL := 766.46;   (* Top Gas Isochoric Heat Capacity Cv [J/(kg*K)] *)
    rIsentropicExponent             : REAL := 1.363;    (* Isentropic Expansion Index Kappa (Cp/Cv) *)
    rGasCompressibilityZ            : REAL := 0.992;    (* Supercompressibility Deviation Factor Z(P,T) *)
    rGasDensity_Inlet               : REAL := 2.65;     (* Upstream Turbine Expansion Gas Density [kg/m3] *)
    rGasAbsoluteTempInlet_K         : REAL := 438.15;   (* Absolute Gas Inlet Temperature [K] (165 deg C) *)
    rGasAbsolutePressInlet_Pa       : REAL := 351325.0; (* Absolute Inlet Pressure P_abs = P_gauge + P_atm [Pa] *)
    rGasAbsolutePressBack_Pa        : REAL := 116325.0; (* Absolute Network Backpressure P_clean + P_atm [Pa] *)
    rAtmosphericPressure_Pa         : REAL := 101325.0; (* Standard Barometric Reference Pressure [Pa] *)
    rPressureRatio_Total            : REAL := 3.02;     (* Overall Turbine Pressure Expansion Ratio Pi *)
    rIsentropicEnthalpyDrop         : REAL := 115200.0; (* Theoretical Isentropic Enthalpy Drop delta_hs [J/kg] *)
    rPolytropicEnthalpyDrop         : REAL := 99072.0;  (* Actual Polytropic Enthalpy Drop delta_h [J/kg] *)
    rAerodynamicTorque_Nm           : REAL := 66250.0;  (* Internal Rotor Gas Kinetic Torque [N*m] *)
    rGeneratorOpposingTorque_Nm     : REAL := 0.0;      (* Generator Electromagnetic Braking Torque [N*m] *)
    rTurbineRotorInertia_J          : REAL := 4250.0;   (* Combined Turbine-Gearbox-Generator Inertia [kg*m2] *)
    rPlenumEffectiveVolume_m3       : REAL := 5500.0;   (* Blast Furnace Hearth & Top Gas Plenum Volume [m3] *)
    rSeptumV1_MaxFlowCap_kgs        : REAL := 125.0;    (* Septum Valve 1 Max Choked Capacity [kg/s] *)
    rSeptumV2_MaxFlowCap_kgs        : REAL := 85.0;     (* Septum Valve 2 Max Choked Capacity [kg/s] *)
    rSeptumV3_MaxFlowCap_kgs        : REAL := 40.0;     (* Septum Valve 3 Max Choked Capacity [kg/s] *)
    rTRT_MaxFlowCap_kgs             : REAL := 195.0;    (* TRT Variable Stator Full Open Capacity [kg/s] *)
    rCalculated_SeptumFlow_kgs      : REAL := 0.0;      (* Combined Bypass Flow Yield across Septum Bank [kg/s] *)
    rCalculated_TRTFlow_kgs         : REAL := 0.0;      (* Current Calculated TRT Throughput [kg/s] *)

    (* Slew-Rate Clamping & Actuator Output Conditioning *)
    rVSV_Demand_Unclamped           : REAL := 0.0;
    rSeptumV1_Demand_Unclamped      : REAL := 35.0;
    rSeptumV2_Demand_Unclamped      : REAL := 25.0;
    rSeptumV3_Demand_Unclamped      : REAL := 15.0;
    rVSV_Demand_RateClamped         : REAL := 0.0;
    rSeptumV1_Demand_RateClamped    : REAL := 35.0;
    rSeptumV2_Demand_RateClamped    : REAL := 25.0;
    rSeptumV3_Demand_RateClamped    : REAL := 15.0;

    (* ========================================================================= *)
    (* ISA-18.2 ALARM ENGINE TRIP POINTS, DEADBANDS & STATUS LATCHES             *)
    (* ========================================================================= *)
    (* Process Alarm Threshold Constants *)
    cTopGasPress_TripHH             : REAL := 280.0;    (* Catastrophic Top Pressure Trip (SIL-3 Bleeder Vent) [kPa] *)
    cTopGasPress_AlarmH             : REAL := 265.0;    (* High Top Gas Operating Pressure Warning [kPa] *)
    cTopGasPress_AlarmL             : REAL := 235.0;    (* Low Top Gas Operating Pressure Warning [kPa] *)
    cTopGasPress_TripLL             : REAL := 210.0;    (* Dangerous Low Top Gas Pressure Trip [kPa] *)
    cTopGasPress_Hysteresis         : REAL := 2.5;      (* Alarm Clearing Deadband Hysteresis [kPa] *)
    cTopGasPress_SlipROC_Threshold  : REAL := 25.0;     (* Blast Furnace Burden Slip Surge ROC [kPa/s] *)

    cTurbineOverspeed_TripHH        : REAL := 3300.0;   (* 110% Turbine Overspeed Hardware Trip [rpm] *)
    cTurbineOverspeed_AlarmH        : REAL := 3150.0;   (* 105% High Rotor Speed Warning [rpm] *)
    cTurbineOverspeed_Hysteresis    : REAL := 25.0;     (* Overspeed Alarm Clearing Deadband [rpm] *)

    cTurbineVib_TripHH              : REAL := 65.0;     (* ISO 10816 Zone D Catastrophic Vibration Trip [um] *)
    cTurbineVib_AlarmH              : REAL := 45.0;     (* ISO 10816 Zone C Abnormal Vibration Warning [um] *)
    cTurbineVib_Hysteresis          : REAL := 3.0;      (* Vibration Clearing Deadband [um] *)

    cBagFilter_dPTripHH             : REAL := 9.0;      (* Bag Filter Blinded Clogging Differential Trip [kPa] *)
    cBagFilter_dPAlarmH             : REAL := 7.8;      (* Bag Filter High Differential Warning [kPa] *)
    cBagFilter_dPTripLL             : REAL := 1.8;      (* Bag Filter Membrane Rupture Trip [kPa] *)
    cBagFilter_dPHysteresis         : REAL := 0.4;      (* Bag Filter dP Clearing Deadband [kPa] *)

    cBagFilterTemp_TripHH           : REAL := 245.0;    (* Bag Filter High-Temperature Scorch Trip [deg C] *)
    cBagFilterTemp_AlarmH           : REAL := 220.0;    (* Bag Filter High-Temperature Warning [deg C] *)
    cBagFilterTemp_AlarmL           : REAL := 120.0;    (* Bag Filter Acid Dewpoint Condensation Warning [deg C] *)
    cBagFilterTemp_TripLL           : REAL := 105.0;    (* Bag Filter Acid Dewpoint Corrosion Trip [deg C] *)

    cBearingTemp_TripHH             : REAL := 95.0;     (* Journal/Thrust Bearing Metal High Trip [deg C] *)
    cBearingTemp_AlarmH             : REAL := 82.0;     (* Journal/Thrust Bearing Metal Warning [deg C] *)

    cLubeOilPress_TripLL            : REAL := 1.8;      (* Lube Oil Header Pressure Collapse Trip [bar] *)
    cLubeOilPress_AlarmL            : REAL := 2.3;      (* Lube Oil Header Pressure Warning [bar] *)

    cN2SealDiffPress_TripLL         : REAL := 10.0;     (* Nitrogen Shaft Seal Loss Toxic Trip [kPa] *)
    cN2SealDiffPress_AlarmL         : REAL := 15.0;     (* Nitrogen Shaft Seal Low Warning [kPa] *)

    cOxygenConc_TripHH              : REAL := 1.0;      (* Top Gas Flammable Oxygen Infiltration Trip [vol %] *)

    (* Alarm State Latches *)
    bAlarm_TopPress_HH              : BOOL := FALSE;
    bAlarm_TopPress_H               : BOOL := FALSE;
    bAlarm_TopPress_L               : BOOL := FALSE;
    bAlarm_TopPress_LL              : BOOL := FALSE;
    bAlarm_TopPress_SlipROC         : BOOL := FALSE;
    bAlarm_TurbineSpeed_HH          : BOOL := FALSE;
    bAlarm_TurbineSpeed_H           : BOOL := FALSE;
    bAlarm_TurbineVib_HH            : BOOL := FALSE;
    bAlarm_TurbineVib_H             : BOOL := FALSE;
    bAlarm_BagFilter_dPHH           : BOOL := FALSE;
    bAlarm_BagFilter_dPH            : BOOL := FALSE;
    bAlarm_BagFilter_dPLL           : BOOL := FALSE;
    bAlarm_BagFilter_TempHH         : BOOL := FALSE;
    bAlarm_BagFilter_TempLL         : BOOL := FALSE;
    bAlarm_BearingTemp_HH           : BOOL := FALSE;
    bAlarm_BearingTemp_H            : BOOL := FALSE;
    bAlarm_LubeOil_LL               : BOOL := FALSE;
    bAlarm_LubeOil_L                : BOOL := FALSE;
    bAlarm_N2Seal_LL                : BOOL := FALSE;
    bAlarm_N2Seal_L                 : BOOL := FALSE;
    bAlarm_Oxygen_HH                : BOOL := FALSE;
    bAlarm_FastBypassHydraulic_Low  : BOOL := FALSE;
    bAlarm_GeneratorReversePower    : BOOL := FALSE;
    bAlarm_TMR_MajorSensorFailure   : BOOL := FALSE;

    (* Hardware Trip Memory & First-Out Registration *)
    bHardwareMasterTripEngaged      : BOOL := FALSE;
    nFirstOutTripReasonCode         : INT := 0;

    (* Temporary Calculation & Loop Iteration Variables *)
    iIdx                            : INT := 1;
    jIdx                            : INT := 1;
    kIdx                            : INT := 1;
    pIdx                            : INT := 1;
    nIter                           : INT := 1;
    rTempSum                        : REAL := 0.0;
    rTempDiff                       : REAL := 0.0;
    rTempGrad                       : REAL := 0.0;
    rTempMin                        : REAL := 0.0;
    rTempMax                        : REAL := 0.0;
    rTempMed                        : REAL := 0.0;
    rTempA                          : REAL := 0.0;
    rTempB                          : REAL := 0.0;
    rTempC                          : REAL := 0.0;
    rTempRatio                      : REAL := 0.0;
    rTempTerm                       : REAL := 0.0;
END_VAR
"""
