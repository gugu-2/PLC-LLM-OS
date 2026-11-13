# ldpe_reactor_builder/st_var_declarations.py

def get_var_declarations():
    return """VAR
    (* ============================================================================================== *)
    (* SECTION 1: DISCRETE STATE-SPACE MODEL & KALMAN/LUMENBERGER OBSERVER MATRICES (6X6 SYSTEM)      *)
    (* States x = [T_peak (deg C), Z_peak (m), P_inlet (bar), P_outlet (bar), X_conv (%), MFI (g/10min)]*)
    (* Inputs u = [Q_comp_trim (%), S_perox_trim (%), u_HPLDV_trim (%), u_jkt_trim (%)]               *)
    (* Outputs y = [T_peak_meas, Z_peak_meas, P_inlet_meas, P_outlet_meas, X_conv_meas, MFI_meas]     *)
    (* Discrete Sample Time Ts = 5 ms (0.005 s)                                                      *)
    (* ============================================================================================== *)
    bMatricesInitialized            : BOOL := FALSE;(* State-Space and MPC Matrices Initialized Flag *)
    
    (* System Transition Matrix A (6x6) *)
    matA                            : ARRAY[1..6, 1..6] OF REAL;
    (* Input Coupling Matrix B (6x4) *)
    matB                            : ARRAY[1..6, 1..4] OF REAL;
    (* Output State Measurement Matrix C (6x6) *)
    matC                            : ARRAY[1..6, 1..6] OF REAL;
    (* Direct Transmission Matrix D (6x4) *)
    matD                            : ARRAY[1..6, 1..4] OF REAL;
    (* Observer Innovation Feedback Gain Matrix L_obs (6x6) *)
    matL_Obs                        : ARRAY[1..6, 1..6] OF REAL;

    (* Discrete State Space Vectors *)
    vecX_Est                        : ARRAY[1..6] OF REAL;  (* Current Filtered Estimated State Vector *)
    vecX_Pred                       : ARRAY[1..6] OF REAL;  (* One-Step Ahead A Priori State Prediction *)
    vecX_Ref                        : ARRAY[1..6] OF REAL;  (* State Trajectory Reference Setpoint Vector *)
    vecY_Meas                       : ARRAY[1..6] OF REAL;  (* Reconstructed Measurement Observation Vector *)
    vecY_Pred                       : ARRAY[1..6] OF REAL;  (* Output Vector Predicted from State *)
    vecY_Err                        : ARRAY[1..6] OF REAL;  (* Innovation Residual Error (y_meas - y_pred) *)
    vecU_Prev                       : ARRAY[1..4] OF REAL;  (* Previous Scan Actuator Command Vector *)
    vecU_Cmd                        : ARRAY[1..4] OF REAL;  (* Current Scan Optimized Actuator Command Vector *)

    (* State Vector Index Aliases *)
    iState_Tpeak                    : INT := 1; (* Index 1: Peak Exotherm Temperature [deg C] *)
    iState_Zpeak                    : INT := 2; (* Index 2: Axial Spatial Exotherm Location [m] *)
    iState_Pinlet                   : INT := 3; (* Index 3: Inlet Header Hyper-Compressor Pressure [bar] *)
    iState_Poutlet                  : INT := 4; (* Index 4: Outlet Header Pressure Before HPLDV [bar] *)
    iState_Xconv                    : INT := 5; (* Index 5: Single-Pass Monomer Conversion Rate [%] *)
    iState_MFI                      : INT := 6; (* Index 6: Polyethylene Melt Flow Index [g/10min] *)

    (* Actuator Vector Index Aliases *)
    iInput_HyperCompTrim            : INT := 1; (* Input 1: Hyper-Compressor Throughput Trim [%] *)
    iInput_PeroxMasterTrim          : INT := 2; (* Input 2: Peroxide Master Dosing Stroke Trim [%] *)
    iInput_HPLDVBaseTrim            : INT := 3; (* Input 3: High-Pressure Letdown Baseline Trim [%] *)
    iInput_JacketWaterTrim          : INT := 4; (* Input 4: Pressurized Jacket Cooling Trim [%] *)

    (* Cyber-Physical Physical Properties & Tube Wall Boundary Layer Variables *)
    rTube_Length_Total_m            : REAL := 1500.0;       (* Total Unrolled Reactor Tube Length [m] *)
    rTube_InnerDiameter_m           : REAL := 0.052;        (* High-Alloy Inner Bore Diameter [m] *)
    rSupercritical_EthyleneDensity_kgm3 : REAL := 540.0;    (* Supercritical Ethylene Density at 3,000 bar [kg/m3] *)
    rHeatOfReaction_kJ_kg           : REAL := 3550.0;       (* Specific Exothermic Heat of Polymerization [kJ/kg] *)
    rEthylene_SpecificHeat_kJ_kgK   : REAL := 2.65;         (* Specific Heat Capacity of Supercritical Gas [kJ/kg K] *)
    rPolymer_ThermalConductivity_W_mK : REAL := 0.22;       (* Stagnant LDPE Wall Gel Thermal Conductivity [W/m K] *)
    rClean_HeatTransferCoeff_W_m2K  : REAL := 850.0;        (* Clean Tube Overall Heat Transfer Coefficient [W/m2 K] *)
    rCurrent_FoulingResistance_m2K_kW : REAL := 0.42;       (* Current Estimated Boundary Gel Thermal Resistance [m2 K/kW] *)
    rCurrent_WallGelThickness_um    : REAL := 88.5;         (* Current Stagnant Polymer Gel Layer Thickness [um] *)
    rDepositionRate_um_per_s        : REAL := 0.12;         (* Rate of Gel Layer Thickening Due to Laminar Drag [um/s] *)
    rScourShearStress_Critical_Pa   : REAL := 125000.0;     (* Minimum Wall Shear Required for Gel Erosion [Pa] *)

    (* ============================================================================================== *)
    (* SECTION 2: RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) & PGD VARIABLES                     *)
    (* ============================================================================================== *)
    (* Cost Function Weights *)
    matQ                            : ARRAY[1..6, 1..6] OF REAL;  (* State Tracking Penalty Matrix Q *)
    matR                            : ARRAY[1..4, 1..4] OF REAL;  (* Actuator Effort Penalty Matrix R *)
    matP_Term                       : ARRAY[1..6, 1..6] OF REAL;  (* Terminal State Cost Penalty Matrix P *)
    matS_Slew                       : ARRAY[1..4, 1..4] OF REAL;  (* Actuator Slew Rate Penalty Matrix S *)

    (* MPC Trajectory and Iteration Buffers *)
    arrX_HorizonPred                : ARRAY[1..10, 1..6] OF REAL; (* State Prediction Over 10-Step Horizon *)
    arrU_HorizonPlan                : ARRAY[1..10, 1..4] OF REAL; (* Actuator Plan Over 10-Step Horizon *)
    arrGrad_U                       : ARRAY[1..10, 1..4] OF REAL; (* Unrolled Gradient with Respect to Controls *)
    vecGrad_CurrentStep             : ARRAY[1..4] OF REAL;        (* Consolidated Gradient for Current Actuation *)

    (* Projected Gradient Descent Parameters *)
    iPGD_MaxIterations              : INT := 10;            (* Number of Unrolled PGD Iterations [-] *)
    rPGD_StepSizeAlpha              : REAL := 0.0125;       (* Gradient Descent Learning Rate Step Size [-] *)
    rMPC_ObjectiveCost              : REAL := 0.0;          (* Total Evaluated Cost J(x, u) [-] *)
    rMPC_TerminalCost               : REAL := 0.0;          (* Terminal Cost Component J_term [-] *)

    (* Actuator Hard Saturation & Slew Constraints *)
    vecU_Min                        : ARRAY[1..4] OF REAL;  (* Lower Bound on Control Inputs [%] *)
    vecU_Max                        : ARRAY[1..4] OF REAL;  (* Upper Bound on Control Inputs [%] *)
    vecDeltaU_Max                   : ARRAY[1..4] OF REAL;  (* Maximum Permissible Slew Rate Per Scan [%/scan] *)

    (* Multi-Zone Initiator Pump Dosing Splits *)
    rPeroxide_Zone1_Ratio           : REAL := 0.22; (* Zone 1 Initiator Flow Split Ratio [-] *)
    rPeroxide_Zone2_Ratio           : REAL := 0.38; (* Zone 2 Initiator Flow Split Ratio [-] *)
    rPeroxide_Zone3_Ratio           : REAL := 0.25; (* Zone 3 Initiator Flow Split Ratio [-] *)
    rPeroxide_Zone4_Ratio           : REAL := 0.15; (* Zone 4 Initiator Flow Split Ratio [-] *)

    (* Arrhenius Kinetic Rate Parameters for Peroxide Decomposition *)
    rEa_LowTempPeroxide_J_mol       : REAL := 125000.0; (* Activation Energy for Low-T Initiator [J/mol] *)
    rA0_LowTempPeroxide_s_inv       : REAL := 1.8E15;   (* Frequency Factor for Low-T Initiator [1/s] *)
    rEa_MedTempPeroxide_J_mol       : REAL := 138000.0; (* Activation Energy for Mid-T Initiator [J/mol] *)
    rA0_MedTempPeroxide_s_inv       : REAL := 4.2E15;   (* Frequency Factor for Mid-T Initiator [1/s] *)
    rEa_HighTempPeroxide_J_mol      : REAL := 152000.0; (* Activation Energy for High-T Initiator [J/mol] *)
    rA0_HighTempPeroxide_s_inv      : REAL := 9.5E15;   (* Frequency Factor for High-T Initiator [1/s] *)
    rGasConstant_R_J_molK           : REAL := 8.31446;  (* Universal Ideal Gas Constant [J/mol K] *)

    (* ============================================================================================== *)
    (* SECTION 3: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING STRUCTURES                       *)
    (* ============================================================================================== *)
    (* Channel Group 1: 4,000-Bar Quartz Pressure Transducers *)
    rTMR_Press_Tol_bar              : REAL := 45.0;     (* Permissible Inter-Channel Pressure Deviation [bar] *)
    tTMR_Press_DiscTimer_s          : REAL := 0.0;      (* Channel Discrepancy Timer Accumulator [s] *)
    tTMR_Press_TripDelay_s          : REAL := 0.200;    (* Discrepancy Trip Qualification Time [s] *)
    bFault_Press_Ch1                : BOOL := FALSE;    (* Pressure Channel 1 Fault Latched Flag *)
    bFault_Press_Ch2                : BOOL := FALSE;    (* Pressure Channel 2 Fault Latched Flag *)
    bFault_Press_Ch3                : BOOL := FALSE;    (* Pressure Channel 3 Fault Latched Flag *)
    rHealth_Press_Ch1_pct           : REAL := 100.0;    (* Sensor Ch1 Integrity Health Metric [%] *)
    rHealth_Press_Ch2_pct           : REAL := 100.0;    (* Sensor Ch2 Integrity Health Metric [%] *)
    rHealth_Press_Ch3_pct           : REAL := 100.0;    (* Sensor Ch3 Integrity Health Metric [%] *)
    rVoted_Press_Prev_bar           : REAL := 3050.0;   (* Previous Scan Voted Pressure for Derivative [bar] *)

    (* Channel Group 2: Thick-Walled Fast Type K Thermocouples *)
    rTMR_Temp_Tol_degC              : REAL := 6.5;      (* Permissible Inter-Channel Temperature Deviation [deg C] *)
    tTMR_Temp_DiscTimer_s           : REAL := 0.0;      (* Temperature Discrepancy Timer Accumulator [s] *)
    tTMR_Temp_TripDelay_s           : REAL := 0.250;    (* Temperature Discrepancy Qualification Time [s] *)
    bFault_Temp_Ch1                 : BOOL := FALSE;    (* Thermocouple Channel 1 Fault Latched Flag *)
    bFault_Temp_Ch2                 : BOOL := FALSE;    (* Thermocouple Channel 2 Fault Latched Flag *)
    bFault_Temp_Ch3                 : BOOL := FALSE;    (* Thermocouple Channel 3 Fault Latched Flag *)
    rHealth_Temp_Ch1_pct            : REAL := 100.0;    (* Thermocouple Ch1 Integrity Health Metric [%] *)
    rHealth_Temp_Ch2_pct            : REAL := 100.0;    (* Thermocouple Ch2 Integrity Health Metric [%] *)
    rHealth_Temp_Ch3_pct            : REAL := 100.0;    (* Thermocouple Ch3 Integrity Health Metric [%] *)
    rVoted_Temp_Prev_degC           : REAL := 302.0;    (* Previous Scan Voted Temp for Derivative [deg C] *)

    (* Channel Group 3: Coriolis Peroxide Dosing Flowmeters *)
    rTMR_Flow_Tol_kgh               : REAL := 2.5;      (* Permissible Inter-Channel Flow Deviation [kg/h] *)
    tTMR_Flow_DiscTimer_s           : REAL := 0.0;      (* Flowmeter Discrepancy Timer Accumulator [s] *)
    tTMR_Flow_TripDelay_s           : REAL := 0.350;    (* Flow Discrepancy Qualification Time [s] *)
    bFault_Flow_Ch1                 : BOOL := FALSE;    (* Flowmeter Channel 1 Fault Latched Flag *)
    bFault_Flow_Ch2                 : BOOL := FALSE;    (* Flowmeter Channel 2 Fault Latched Flag *)
    bFault_Flow_Ch3                 : BOOL := FALSE;    (* Flowmeter Channel 3 Fault Latched Flag *)
    rHealth_Flow_Ch1_pct            : REAL := 100.0;    (* Flowmeter Ch1 Integrity Health Metric [%] *)
    rHealth_Flow_Ch2_pct            : REAL := 100.0;    (* Flowmeter Ch2 Integrity Health Metric [%] *)
    rHealth_Flow_Ch3_pct            : REAL := 100.0;    (* Flowmeter Ch3 Integrity Health Metric [%] *)
    rVoted_Flow_Prev_kgh            : REAL := 48.0;     (* Previous Scan Voted Flow for Derivative [kg/h] *)

    (* Channel Group 4: Acoustic Emission Decomposition Precursor Sensors *)
    rTMR_Acoustic_Tol_dB            : REAL := 8.0;      (* Permissible Inter-Channel Acoustic Deviation [dB] *)
    tTMR_Acoustic_DiscTimer_s       : REAL := 0.0;      (* Acoustic Discrepancy Timer Accumulator [s] *)
    tTMR_Acoustic_TripDelay_s       : REAL := 0.100;    (* Acoustic Discrepancy Qualification Time [s] *)
    bFault_Acoustic_Ch1             : BOOL := FALSE;    (* Acoustic Sensor Channel 1 Fault Latched Flag *)
    bFault_Acoustic_Ch2             : BOOL := FALSE;    (* Acoustic Sensor Channel 2 Fault Latched Flag *)
    bFault_Acoustic_Ch3             : BOOL := FALSE;    (* Acoustic Sensor Channel 3 Fault Latched Flag *)
    rHealth_Acoustic_Ch1_pct        : REAL := 100.0;    (* Acoustic Sensor Ch1 Integrity Health Metric [%] *)
    rHealth_Acoustic_Ch2_pct        : REAL := 100.0;    (* Acoustic Sensor Ch2 Integrity Health Metric [%] *)
    rHealth_Acoustic_Ch3_pct        : REAL := 100.0;    (* Acoustic Sensor Ch3 Integrity Health Metric [%] *)

    (* ============================================================================================== *)
    (* SECTION 4: HPLDV PULSE DEPRESSURIZATION ENGINE & ACOUSTIC SCOURING WAVE DYNAMICS               *)
    (* ============================================================================================== *)
    tHPLDV_PulseCycleTimer_s        : REAL := 0.0;      (* Master Cyclic Pulsation Timer (0 to 20 s) [s] *)
    tHPLDV_PulsePhaseTimer_s        : REAL := 0.0;      (* Active Step-Open Expansion Wave Timer [s] *)
    bHPLDV_InPulseExecution         : BOOL := FALSE;    (* Active Scouring Pulse In-Flight Flag *)
    rHPLDV_PulseBaselineStroke_pct  : REAL := 28.5;     (* Normal Modulating Letdown Stroke [%] *)
    rHPLDV_PulseStepStroke_pct      : REAL := 42.0;     (* Transient Stepped-Open Letdown Stroke [%] *)
    rMeasured_PrePulsePress_bar     : REAL := 3050.0;   (* Stored Inlet Pressure Prior to Pulse [bar] *)
    rMeasured_MinPulsePress_bar     : REAL := 2800.0;   (* Minimum Trough Pressure During Pulse [bar] *)
    rHPLDV_PulseRampRate_pct_s      : REAL := 180.0;    (* High-Speed Hydraulic Stroke Slew Rate [%/s] *)
    rAcoustic_WaveSpeed_m_s         : REAL := 1920.0;   (* Supercritical Ethylene Acoustic Velocity [m/s] *)
    rWave_TransitTime_Total_s       : REAL := 0.781;    (* Round-Trip Sound Propagation Time [s] *)
    iTotalPulseCyclesCompleted      : DINT := 0;        (* Lifetime Cyclic Pulsations Counter [-] *)

    (* ============================================================================================== *)
    (* SECTION 5: FAST EXPLOSIVE DECOMPOSITION (DECOMP) PROTECTION & HYDRAULIC SNORT DUMP             *)
    (* ============================================================================================== *)
    rFast_dP_dt_bar_s               : REAL := 0.0;      (* Sub-5ms Pressure Rise Rate dP/dt [bar/s] *)
    rFast_dT_dt_K_s                 : REAL := 0.0;      (* Sub-5ms Temperature Rise Rate dT/dt [K/s] *)
    rThreshold_Decomp_dP_dt_bar_s   : REAL := 1500.0;   (* Critical Rate-of-Pressure Rise Limit [bar/s] *)
    rThreshold_Decomp_dT_dt_K_s     : REAL := 50.0;     (* Critical Rate-of-Temperature Rise Limit [K/s] *)
    rThreshold_Decomp_Acoustic_dB   : REAL := 115.0;    (* Critical Explosive Acoustic Crack Limit [dB] *)
    rThreshold_Decomp_AbsPress_bar  : REAL := 3450.0;   (* Ultimate Mechanical Overpressure Trip [bar] *)
    rThreshold_Decomp_AbsTemp_degC  : REAL := 325.0;    (* Extreme Thermal Runaway Temperature [deg C] *)
    bDecomp_TripQualified           : BOOL := FALSE;    (* Fast Sub-5ms Decomposition Trip Qualified Flag *)
    bSnortSolValve1_Actuated        : BOOL := FALSE;    (* Pilot Solenoid 1 for Snort Valve Actuated *)
    bSnortSolValve2_Actuated        : BOOL := FALSE;    (* Pilot Solenoid 2 for Snort Valve Actuated *)
    tSnortDumpActiveTimer_s         : REAL := 0.0;      (* Snort Dump Valve Open Duration Accumulator [s] *)

    (* ============================================================================================== *)
    (* SECTION 6: 14-STAGE DETERMINISTIC PRODUCTION FINITE STATE MACHINE (FSM)                        *)
    (* ============================================================================================== *)
    iState                          : INT := 0;         (* Active Operational State (0..13) [-] *)
    iPreviousState                  : INT := 0;         (* Previous Operational State [-] *)
    tStateTimer_s                   : REAL := 0.0;      (* Continuous Elapsed Time in Active State [s] *)
    rStateProgress_pct              : REAL := 0.0;      (* Active State Milestone Progress Metric [%] *)
    bStateFirstScan                 : BOOL := TRUE;     (* First Execution Scan of Current State Flag *)

    (* State Number Enumerations *)
    STATE_IDLE                      : INT := 0;  (* Standby Cold Pressurization Permissive Check *)
    STATE_JACKET_WATER_PREHEAT      : INT := 1;  (* Pressurized Hot Water Circulation Preheat 180 C *)
    STATE_ETHYLENE_GAS_PRESS_1000   : INT := 2;  (* Primary Compressor Pressurization Ramp to 1,000 bar *)
    STATE_HYPER_COMPRESSOR_SPINUP   : INT := 3;  (* Secondary Hyper-Compressor Spinup to 3,000 bar *)
    STATE_INITIATOR_PRIME_AIR_EXPUL : INT := 4;  (* Micro-Metering Peroxide Diaphragm Lines De-Air *)
    STATE_FIRST_ZONE_PEROXIDE_IGNIT : INT := 5;  (* Zone 1 Low-T Peroxide Light-Off & Exotherm Ignition *)
    STATE_NOMINAL_EXOTHERMIC_RUN    : INT := 6;  (* Multi-Zone Polymerization Steady Production *)
    STATE_CYCLIC_LETDOWN_PULSE_RUN  : INT := 7;  (* Synchronized 20s HPLDV Wall Gel Scour Pulsation *)
    STATE_DYNAMIC_GRADE_TRANSITION  : INT := 8;  (* Dynamic MFI & Density Polymer Grade Transition *)
    STATE_PEAK_TEMP_LIMITING_TRIM   : INT := 9;  (* Exotherm Protection Automatic Peroxide Throttle *)
    STATE_CONTROLLED_TURNDOWN_FLUSH : INT := 10; (* Safe Production Rampdown & Hydrocarbon Solvent Flush *)
    STATE_ETHYLENE_RECYCLE_DEPRESS  : INT := 11; (* Controlled Monomer Recycle & Depressurization *)
    STATE_REACTOR_POST_WASH_NITRO   : INT := 12; (* Hot Solvent Tube Wash & Nitrogen Blanket Seal *)
    STATE_EMERGENCY_DECOMP_SNORT    : INT := 13; (* Explosive Decomp Fast Snort Dump to Quench Silo *)

    (* ============================================================================================== *)
    (* SECTION 7: ISA-18.2 MULTI-TIER PROCESS ALARM THRESHOLDS & HYSTERESIS DEADBANDS                 *)
    (* ============================================================================================== *)
    (* Trip & Warning Limits *)
    rAlarm_Press_HH_bar             : REAL := 3280.0;   (* Trip High-High Operating Pressure [bar] *)
    rAlarm_Press_H_bar              : REAL := 3150.0;   (* Warning High Operating Pressure [bar] *)
    rAlarm_Press_L_bar              : REAL := 2750.0;   (* Warning Low Operating Pressure [bar] *)
    rAlarm_Press_LL_bar             : REAL := 2450.0;   (* Trip Low-Low Operating Pressure [bar] *)
    rAlarm_Press_Deadband_bar       : REAL := 15.0;     (* Pressure Hysteresis Clear Deadband [bar] *)

    rAlarm_Temp_HH_degC             : REAL := 316.0;    (* Trip High-High Exotherm Temperature [deg C] *)
    rAlarm_Temp_H_degC              : REAL := 308.0;    (* Warning High Exotherm Temperature [deg C] *)
    rAlarm_Temp_L_degC              : REAL := 220.0;    (* Warning Low Reaction Temperature [deg C] *)
    rAlarm_Temp_LL_degC             : REAL := 170.0;    (* Trip Low-Low Flameout/Extinction Temp [deg C] *)
    rAlarm_Temp_Deadband_degC       : REAL := 2.5;      (* Temperature Hysteresis Clear Deadband [deg C] *)

    rAlarm_Flow_H_kgh               : REAL := 65.0;     (* Warning High Peroxide Dosing Flow [kg/h] *)
    rAlarm_Flow_L_kgh               : REAL := 25.0;     (* Warning Low Peroxide Dosing Flow [kg/h] *)
    rAlarm_Flow_Deadband_kgh        : REAL := 1.0;      (* Flowmeter Hysteresis Clear Deadband [kg/h] *)

    rAlarm_Acoustic_H_dB            : REAL := 85.0;     (* Warning High Acoustic Stress Level [dB] *)
    rAlarm_Acoustic_HH_dB           : REAL := 112.0;    (* Trip High-High Explosive Acoustic Crack [dB] *)

    (* Alarm Qualification Delay Timers *)
    tAlarm_Press_HH_Timer_s         : REAL := 0.0;
    tAlarm_Press_H_Timer_s          : REAL := 0.0;
    tAlarm_Press_L_Timer_s          : REAL := 0.0;
    tAlarm_Press_LL_Timer_s         : REAL := 0.0;
    tAlarm_Temp_HH_Timer_s          : REAL := 0.0;
    tAlarm_Temp_H_Timer_s           : REAL := 0.0;
    tAlarm_Temp_L_Timer_s           : REAL := 0.0;
    tAlarm_Temp_LL_Timer_s          : REAL := 0.0;

    (* Latched Alarm Status Bits *)
    bLatched_Press_HH               : BOOL := FALSE;
    bLatched_Press_H                : BOOL := FALSE;
    bLatched_Press_L                : BOOL := FALSE;
    bLatched_Press_LL               : BOOL := FALSE;
    bLatched_Temp_HH                : BOOL := FALSE;
    bLatched_Temp_H                 : BOOL := FALSE;
    bLatched_Temp_L                 : BOOL := FALSE;
    bLatched_Temp_LL                : BOOL := FALSE;
    bLatched_Flow_H                 : BOOL := FALSE;
    bLatched_Flow_L                 : BOOL := FALSE;
    bLatched_Acoustic_H             : BOOL := FALSE;
    bLatched_Acoustic_HH            : BOOL := FALSE;
    bLatched_RatePress_HH           : BOOL := FALSE;
    bLatched_RateTemp_HH            : BOOL := FALSE;

    (* Loop Counters and Temporary Computation Registers *)
    idx_i                           : INT := 1;
    idx_j                           : INT := 1;
    idx_k                           : INT := 1;
    idx_m                           : INT := 1;
    rTempCalc1                      : REAL := 0.0;
    rTempCalc2                      : REAL := 0.0;
    rTempCalc3                      : REAL := 0.0;
    rTempCalc4                      : REAL := 0.0;
END_VAR
"""
