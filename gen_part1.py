# gen_part1.py
part1 = """FUNCTION_BLOCK FB_Chemical_ChlorAlkali_MembraneElectrolyzer_DPControl
(*
====================================================================================================
LUMINA CYBER-PHYSICAL AUTOMATION KERNEL - IEC 61131-3 STRUCTURED TEXT
DOMAIN: CHEMICAL & PETROCHEMICAL / CHLOR-ALKALI INDUSTRIAL PROCESS AUTOMATION
SYSTEM: BIPOLAR MEMBRANE CELL ELECTROLYZER DIFFERENTIAL PRESSURE (DP) & GAS HEADER BALANCING
PLANT CAPACITY: 2.5 kA/m2 CURRENT DENSITY, 27 BIPOLAR CELLS, DUAL Cl2 / H2 HEADERS, 32-35 wt% NaOH
CORE FOCUS:
  - STRICT DP REGULATION (+/- 3.0 [mbar]) BETWEEN CATHOLYTE (H2) AND ANOLYTE (Cl2) COMPARTMENTS
  - FIRST-PRINCIPLES ELECTRO-CHEMO-HYDRODYNAMIC DISCRETE STATE-SPACE OBSERVER (Ts = 0.020 [s])
  - RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) WITH PROJECTED GRADIENT DESCENT (10 ITERATIONS)
  - 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) VOTING SUITE ACROSS 6 CRITICAL SENSOR CHANNELS
  - DETERMINISTIC 14-STAGE ELECTROLYZER PRODUCTION FINITE STATE MACHINE (FSM STATES 0 TO 13)
  - ISA-18.2 MULTI-TIER PROCESS ALARM ENGINE (HH, H, L, LL) WITH FIRST-OUT LATCHING TELEMETRY
====================================================================================================
*)

VAR_INPUT
    (* Master System Commands & Plant Permissives *)
    bEnable                         : BOOL;         (* Master Function Block Execution Enable [-] *)
    bAutoCycleStart                 : BOOL;         (* Automatic Chlor-Alkali Electrolyzer Start Command [-] *)
    bPlantStop                      : BOOL;         (* Orderly Plant Turndown and Shutdown Sequence Command [-] *)
    bEmergencyStop                  : BOOL;         (* Hardwired Cat-4 Safety Emergency Stop Pushbutton [-] *)
    bFaultReset                     : BOOL;         (* Master Safety Trip & Alarm Fault Latch Reset Pushbutton [-] *)
    bAlarmAck                       : BOOL;         (* ISA-18.2 Audible & Visual Alarm Acknowledge Command [-] *)
    bMpcManualOverride              : BOOL;         (* Model Predictive Control Manual Actuator Override Permissive [-] *)
    bNitrogenPurgePermissive        : BOOL;         (* High-Pressure Inert Nitrogen Header Supply Pressure Permissive [-] *)
    bCausticRecircPumpRunning       : BOOL;         (* Catholyte Loop Caustic Recirculation Pump Running Status [-] *)
    bAnolyteRecircPumpRunning       : BOOL;         (* Anolyte Loop Brine Recirculation Pump Running Status [-] *)
    bChlorineAbsorptionReady        : BOOL;         (* Downstream Emergency Chlorine Scrubber System Ready Permissive [-] *)
    bHydrogenVentStackReady         : BOOL;         (* Downstream Hydrogen Flare / Vent Stack Water Seal Permissive [-] *)
    bDeminWaterSupplyPermissive     : BOOL;         (* Demineralized / Soft Water Dilution Supply Header Ready [-] *)
    bRectifierOnlineFeedback        : BOOL;         (* High-Current DC Rectifier Interlock & Operational Ready Feedback [-] *)

    (* Channel Group 1: Cell Differential Pressure Transmitters (Catholyte minus Anolyte) (2oo3 TMR) *)
    rPDT_Cell_DP_1A_mbar            : REAL;         (* Cell Differential Pressure Transmitter Channel 1A [mbar] *)
    rPDT_Cell_DP_1B_mbar            : REAL;         (* Cell Differential Pressure Transmitter Channel 1B [mbar] *)
    rPDT_Cell_DP_1C_mbar            : REAL;         (* Cell Differential Pressure Transmitter Channel 1C [mbar] *)

    (* Channel Group 2: Chlorine Header Pressure Transmitters (2oo3 TMR) *)
    rPT_Cl2_Header_2A_bar           : REAL;         (* Chlorine Gas Collector Header Pressure Channel 2A [bar] *)
    rPT_Cl2_Header_2B_bar           : REAL;         (* Chlorine Gas Collector Header Pressure Channel 2B [bar] *)
    rPT_Cl2_Header_2C_bar           : REAL;         (* Chlorine Gas Collector Header Pressure Channel 2C [bar] *)

    (* Channel Group 3: Hydrogen Header Pressure Transmitters (2oo3 TMR) *)
    rPT_H2_Header_3A_bar            : REAL;         (* Hydrogen Gas Collector Header Pressure Channel 3A [bar] *)
    rPT_H2_Header_3B_bar            : REAL;         (* Hydrogen Gas Collector Header Pressure Channel 3B [bar] *)
    rPT_H2_Header_3C_bar            : REAL;         (* Hydrogen Gas Collector Header Pressure Channel 3C [bar] *)

    (* Channel Group 4: Inline Hydrogen-in-Chlorine Photometer Analyzers (2oo3 TMR) *)
    rAT_H2_in_Cl2_4A_pct            : REAL;         (* Inline Chlorine Gas H2 Purity Photometer Channel 4A [% vol] *)
    rAT_H2_in_Cl2_4B_pct            : REAL;         (* Inline Chlorine Gas H2 Purity Photometer Channel 4B [% vol] *)
    rAT_H2_in_Cl2_4C_pct            : REAL;         (* Inline Chlorine Gas H2 Purity Photometer Channel 4C [% vol] *)

    (* Channel Group 5: Anolyte Depleted Brine Concentration Analyzers (2oo3 TMR) *)
    rAT_Anolyte_NaCl_5A_gL          : REAL;         (* Anolyte Overflow Depleted Brine Concentration Channel 5A [g/L] *)
    rAT_Anolyte_NaCl_5B_gL          : REAL;         (* Anolyte Overflow Depleted Brine Concentration Channel 5B [g/L] *)
    rAT_Anolyte_NaCl_5C_gL          : REAL;         (* Anolyte Overflow Depleted Brine Concentration Channel 5C [g/L] *)

    (* Channel Group 6: Catholyte Caustic Soda Concentration Analyzers (2oo3 TMR) *)
    rAT_Catholyte_NaOH_6A_pct       : REAL;         (* Catholyte Overflow Caustic Soda Concentration Channel 6A [wt%] *)
    rAT_Catholyte_NaOH_6B_pct       : REAL;         (* Catholyte Overflow Caustic Soda Concentration Channel 6B [wt%] *)
    rAT_Catholyte_NaOH_6C_pct       : REAL;         (* Catholyte Overflow Caustic Soda Concentration Channel 6C [wt%] *)

    (* Process Thermodynamics, Feed Flows & Electrical Telemetry *)
    rCell_Temperature_degC          : REAL;         (* Electrolyzer Cell Stack Bulk Electrolyte Temperature [deg C] *)
    rCell_AverageVoltage_V          : REAL;         (* Individual Average Single-Cell Polarization Voltage [V] *)
    rCell_TotalStackVoltage_V       : REAL;         (* Total Bipolar Electrolyzer Stack Terminal Voltage [V] *)
    rRectifier_CurrentFb_kA         : REAL;         (* DC Rectifier High-Current Busbar Actual Feedback [kA] *)
    rFeedBrine_Flow_m3h             : REAL;         (* Saturated Primary Brine Inflow Feed Rate [m3/h] *)
    rFeedBrine_Concentration_gL     : REAL;         (* Saturated Primary Brine Inflow Feed Concentration [g/L] *)
    rFeedBrine_Temperature_degC     : REAL;         (* Primary Brine Inflow Feed Temperature [deg C] *)
    rDilutionWater_FlowFb_m3h       : REAL;         (* Demineralized Water Caustic Dilution Inflow Rate [m3/h] *)
    rAnolyte_CirculationFlow_m3h    : REAL;         (* Anolyte Compartment Brine Recirculation Rate [m3/h] *)
    rCatholyte_CirculationFlow_m3h  : REAL;         (* Catholyte Compartment Caustic Recirculation Rate [m3/h] *)

    (* Actuator Position Feedback Signals *)
    rValve_H2_BackPress_Fb_pct      : REAL;         (* H2 Header Backpressure Fast Control Valve Position Feedback [%] *)
    rValve_Cl2_Vent_Fb_pct          : REAL;         (* Cl2 Header Pressure / Scrubber Vent Valve Position Feedback [%] *)
    rValve_WaterDilution_Fb_pct     : REAL;         (* Soft Water Catholyte Dilution Control Valve Position Feedback [%] *)
    rValve_BrineTrim_Fb_pct         : REAL;         (* Anolyte Feed Saturated Brine Trim Valve Position Feedback [%] *)
END_VAR

VAR_OUTPUT
    (* Modulating Control Actuator Outputs *)
    rValve_H2_BackPress_Cmd_pct     : REAL;         (* H2 Header Backpressure Fast Modulating Valve Command [%] *)
    rValve_Cl2_Vent_Cmd_pct         : REAL;         (* Cl2 Header Pressure / Scrubber Modulating Valve Command [%] *)
    rValve_WaterDilution_Cmd_pct    : REAL;         (* Soft Water Catholyte Dilution Modulating Valve Command [%] *)
    rValve_BrineTrim_Cmd_pct        : REAL;         (* Anolyte Feed Saturated Brine Trim Modulating Valve Command [%] *)
    rRectifier_Current_Cmd_kA       : REAL;         (* DC High-Current Rectifier Load Setpoint Command [kA] *)

    (* Fast Discrete Safety Valves & Emergency Solenoids *)
    bValve_EmergencyScrubberVent    : BOOL;         (* Cl2 Header Emergency Dump Solenoid to Caustic Scrubber [-] *)
    bValve_EmergencyH2VentStack     : BOOL;         (* H2 Header Emergency Fast Depressurization Vent Solenoid [-] *)
    bValve_N2_AnolytePurge          : BOOL;         (* Nitrogen Inert Fast Blanket Purge Solenoid to Anolyte Header [-] *)
    bValve_N2_CatholytePurge        : BOOL;         (* Nitrogen Inert Fast Blanket Purge Solenoid to Catholyte Header [-] *)
    bRectifier_TripInterlock        : BOOL;         (* Immediate Hardwired Emergency Trip Interlock to DC Rectifier [-] *)
    bElectrolyzerIsolateValves      : BOOL;         (* Double Block & Bleed Skid Isolation Valves Command [-] *)
    bBrinePreheaterSteamValve       : BOOL;         (* Anolyte Brine Warmup Shell-and-Tube Steam Supply Valve [-] *)
    bCausticCoolerWaterValve        : BOOL;         (* Catholyte Caustic Plate Heat Exchanger Cooling Water Valve [-] *)

    (* First-Principles Cyber-Physical Observer Estimated States *)
    rEst_Cell_DP_mbar               : REAL;         (* Observer Estimated Cell Differential Pressure (Cathode - Anode) [mbar] *)
    rEst_P_Cl2_bar                  : REAL;         (* Observer Estimated Chlorine Header Absolute Pressure [bar] *)
    rEst_P_H2_bar                   : REAL;         (* Observer Estimated Hydrogen Header Absolute Pressure [bar] *)
    rEst_Anolyte_NaCl_gL            : REAL;         (* Observer Estimated Anolyte Depleted Brine Concentration [g/L] *)
    rEst_Catholyte_NaOH_pct         : REAL;         (* Observer Estimated Catholyte Caustic Soda Concentration [wt%] *)
    rEst_Cell_Temperature_degC      : REAL;         (* Observer Estimated Cell Stack Core Electrolyte Temperature [deg C] *)

    (* Electrochemical Kinetics, Thermodynamics & Quality Metrics *)
    rCalc_CurrentDensity_kAm2       : REAL;         (* Calculated Operational Current Density [kA/m2] *)
    rCalc_FaradayEfficiency_pct     : REAL;         (* Calculated Electrochemical Faraday Current Efficiency [%] *)
    rCalc_SpecificPower_kWh_tCl2    : REAL;         (* Specific DC Electrical Power Consumption per Ton of Cl2 [kWh/t] *)
    rCalc_MembraneAreaResist_mOhm   : REAL;         (* Ion-Exchange Membrane Specific Area Resistance [mOhm.cm2] *)
    rCalc_Cl2_ProductionRate_Nm3h   : REAL;         (* Calculated Instantaneous Chlorine Gas Production Rate [Nm3/h] *)
    rCalc_H2_ProductionRate_Nm3h    : REAL;         (* Calculated Instantaneous Hydrogen Gas Production Rate [Nm3/h] *)
    rCalc_NaOH_ProductionRate_kgh   : REAL;         (* Calculated 100% Equivalent Caustic Soda Production Rate [kg/h] *)
    rCalc_ThermalHeatGen_kW         : REAL;         (* Calculated Joule & Overpotential Thermal Dissipation [kW] *)
    rCalc_CoolingRequirement_kW     : REAL;         (* Required Electrolyzer Cooling Duty to Maintain 88 deg C [kW] *)
    rMpc_CostFunction_Val           : REAL;         (* Model Predictive Control Quadratic Cost Objective Metric [-] *)
    iActiveFsmState                 : INT;          (* Deterministic Electrolyzer Finite State Machine Active State [0..13] *)

    (* 32-Bit Bit-Packed Telemetry & Diagnostic Status Words *)
    dwStatusWord1                   : DWORD;        (* Electrolyzer Operational State & Actuator Subsystem Status Bits [-] *)
    dwStatusWord2                   : DWORD;        (* 2oo3 TMR Sensor Health & Observer Convergence Telemetry Bits [-] *)
    dwAlarmWord1                    : DWORD;        (* ISA-18.2 Critical Emergency Trips & Interlocks (HH/LL) [-] *)
    dwAlarmWord2                    : DWORD;        (* ISA-18.2 Warning Deviations & Sensor Discrepancies (H/L) [-] *)
    dwFirstOutWord                  : DWORD;        (* Latched First-Out Fault Root Cause Diagnostic Code [-] *)
END_VAR

VAR
    (* Execution Control, Scan Timing & Initialization Flags *)
    bFirstScanDone                  : BOOL := FALSE;    (* First Scan Initialization Completed Flag [-] *)
    tScanCycleTime_s                : REAL := 0.020;    (* Discrete Task Execution Sample Period [s] *)
    iCycleCounter                   : DINT := 0;        (* Rolling Execution Scan Counter [-] *)

    (* Discrete State-Space Cyber-Physical Matrices (6 States x 5 Control Inputs) *)
    matA                            : ARRAY[0..5, 0..5] OF REAL; (* State Transition Dynamic Matrix A (6x6) [-] *)
    matB                            : ARRAY[0..5, 0..4] OF REAL; (* Actuator Input Mapping Matrix B (6x5) [-] *)
    matC                            : ARRAY[0..5, 0..5] OF REAL; (* Sensor Measurement Mapping Matrix C (6x6) [-] *)
    matD                            : ARRAY[0..5, 0..4] OF REAL; (* Direct Feedthrough Matrix D (6x5) [-] *)
    matL                            : ARRAY[0..5, 0..5] OF REAL; (* Steady-State Luenberger Observer Innovation Gain L (6x6) [-] *)

    (* Cyber-Physical State & Control Vectors *)
    vecX                            : ARRAY[0..5] OF REAL; (* Internal Physical State Vector [-] *)
    vecX_hat                        : ARRAY[0..5] OF REAL; (* Filtered State Estimate Vector [-] *)
    vecX_pred                       : ARRAY[0..5] OF REAL; (* One-Step-Ahead Observer State Prediction Vector [-] *)
    vecY_meas                       : ARRAY[0..5] OF REAL; (* 2oo3 Voted Sensor Measurement Vector [-] *)
    vecY_hat                        : ARRAY[0..5] OF REAL; (* Estimated Measurement Vector [-] *)
    vecInnov                        : ARRAY[0..5] OF REAL; (* Innovation Residual Vector (Y_meas - Y_hat) [-] *)
    vecU                            : ARRAY[0..4] OF REAL; (* Current Optimal Actuator Output Vector [-] *)
    vecU_prev                       : ARRAY[0..4] OF REAL; (* Previous Execution Cycle Actuator Vector [-] *)
    vecU_rate                       : ARRAY[0..4] OF REAL; (* Actuator Instantaneous Slew Rate Vector [%/s] *)
    vecX_target                     : ARRAY[0..5] OF REAL; (* Dynamic State Trajectory Setpoint Vector [-] *)
    vecU_target                     : ARRAY[0..4] OF REAL; (* Actuator Nominal Steady-State Setpoint Vector [-] *)

    (* Model Predictive Control (MPC) Cost Weighting & Constraint Vectors *)
    vecQ_weight                     : ARRAY[0..5] OF REAL; (* Quadratic State Tracking Penalty Diagonal Weights [-] *)
    vecR_weight                     : ARRAY[0..4] OF REAL; (* Actuator Effort Penalty Diagonal Weights [-] *)
    vecR_delta_weight               : ARRAY[0..4] OF REAL; (* Actuator Rate-of-Change Penalty Diagonal Weights [-] *)
    vecP_terminal                   : ARRAY[0..5] OF REAL; (* Terminal Horizon State Penalty Diagonal Weights [-] *)
    vecU_min                        : ARRAY[0..4] OF REAL; (* Physical Lower Saturation Bounds [%, kA] *)
    vecU_max                        : ARRAY[0..4] OF REAL; (* Physical Upper Saturation Bounds [%, kA] *)
    vecU_slewMax                    : ARRAY[0..4] OF REAL; (* Maximum Slew Rate Per Execution Scan [%, kA] *)

    (* Receding-Horizon Workspace (Horizon N = 5 Steps, 10 Unrolled PGD Iterations) *)
    trajX_mpc                       : ARRAY[0..5, 0..5] OF REAL; (* Horizon State Trajectory Predictions [-] *)
    trajU_mpc                       : ARRAY[0..4, 0..4] OF REAL; (* Horizon Actuator Control Sequences [-] *)
    trajU_cand                      : ARRAY[0..4, 0..4] OF REAL; (* Projected Candidate Control Updates [-] *)
    trajGrad_J                      : ARRAY[0..4, 0..4] OF REAL; (* Analytical Gradient of Quadratic Cost w.r.t U [-] *)
    trajLambda                      : ARRAY[0..5, 0..5] OF REAL; (* Adjoint Costate Backpropagation Vectors [-] *)
    rPgd_StepSize                   : REAL := 0.015;    (* Projected Gradient Descent Learning Step Size Gamma [-] *)
    rMpc_AccumulatedCost            : REAL := 0.0;      (* Evaluated Quadratic Cost Objective Value [-] *)

    (* 2oo3 Triple Modular Redundancy (TMR) Sensor Channels *)
    (* Channel Group 1: Cell Differential Pressure (Catholyte - Anolyte) [mbar] *)
    rPDT_Cell_DP_Voted              : REAL := 30.0;     (* 2oo3 Voted Differential Pressure [mbar] *)
    bPDT_Cell_DP_HealthA            : BOOL := TRUE;     (* DP Transmitter 1A Healthy Status [-] *)
    bPDT_Cell_DP_HealthB            : BOOL := TRUE;     (* DP Transmitter 1B Healthy Status [-] *)
    bPDT_Cell_DP_HealthC            : BOOL := TRUE;     (* DP Transmitter 1C Healthy Status [-] *)
    rPDT_Cell_DP_Disc_AB_ms         : REAL := 0.0;      (* DP Transmitter 1A vs 1B Discrepancy Timer [ms] *)
    rPDT_Cell_DP_Disc_BC_ms         : REAL := 0.0;      (* DP Transmitter 1B vs 1C Discrepancy Timer [ms] *)
    rPDT_Cell_DP_Disc_CA_ms         : REAL := 0.0;      (* DP Transmitter 1C vs 1A Discrepancy Timer [ms] *)
    bPDT_Cell_DP_Degraded           : BOOL := FALSE;    (* DP Channel Operating in Degraded 2oo2 Voting [-] *)
    bPDT_Cell_DP_SingleFallback     : BOOL := FALSE;    (* DP Channel Operating on Single Channel 1oo1 [-] *)
    bPDT_Cell_DP_Trip               : BOOL := FALSE;    (* Complete DP Sensor Triplication Failure Trip [-] *)

    (* Channel Group 2: Chlorine Header Pressure [bar] *)
    rPT_Cl2_Header_Voted            : REAL := 0.250;    (* 2oo3 Voted Chlorine Header Pressure [bar] *)
    bPT_Cl2_Header_HealthA          : BOOL := TRUE;     (* Cl2 Transmitter 2A Healthy Status [-] *)
    bPT_Cl2_Header_HealthB          : BOOL := TRUE;     (* Cl2 Transmitter 2B Healthy Status [-] *)
    bPT_Cl2_Header_HealthC          : BOOL := TRUE;     (* Cl2 Transmitter 2C Healthy Status [-] *)
    rPT_Cl2_Header_Disc_AB_ms       : REAL := 0.0;      (* Cl2 Transmitter 2A vs 2B Discrepancy Timer [ms] *)
    rPT_Cl2_Header_Disc_BC_ms       : REAL := 0.0;      (* Cl2 Transmitter 2B vs 2C Discrepancy Timer [ms] *)
    rPT_Cl2_Header_Disc_CA_ms       : REAL := 0.0;      (* Cl2 Transmitter 2C vs 2A Discrepancy Timer [ms] *)
    bPT_Cl2_Header_Degraded         : BOOL := FALSE;    (* Cl2 Pressure Operating in Degraded 2oo2 Voting [-] *)
    bPT_Cl2_Header_SingleFallback   : BOOL := FALSE;    (* Cl2 Pressure Operating on Single Channel 1oo1 [-] *)
    bPT_Cl2_Header_Trip             : BOOL := FALSE;    (* Complete Cl2 Sensor Triplication Failure Trip [-] *)

    (* Channel Group 3: Hydrogen Header Pressure [bar] *)
    rPT_H2_Header_Voted             : REAL := 0.280;    (* 2oo3 Voted Hydrogen Header Pressure [bar] *)
    bPT_H2_Header_HealthA           : BOOL := TRUE;     (* H2 Transmitter 3A Healthy Status [-] *)
    bPT_H2_Header_HealthB           : BOOL := TRUE;     (* H2 Transmitter 3B Healthy Status [-] *)
    bPT_H2_Header_HealthC           : BOOL := TRUE;     (* H2 Transmitter 3C Healthy Status [-] *)
    rPT_H2_Header_Disc_AB_ms        : REAL := 0.0;      (* H2 Transmitter 3A vs 3B Discrepancy Timer [ms] *)
    rPT_H2_Header_Disc_BC_ms        : REAL := 0.0;      (* H2 Transmitter 3B vs 3C Discrepancy Timer [ms] *)
    rPT_H2_Header_Disc_CA_ms        : REAL := 0.0;      (* H2 Transmitter 3C vs 3A Discrepancy Timer [ms] *)
    bPT_H2_Header_Degraded          : BOOL := FALSE;    (* H2 Pressure Operating in Degraded 2oo2 Voting [-] *)
    bPT_H2_Header_SingleFallback    : BOOL := FALSE;    (* H2 Pressure Operating on Single Channel 1oo1 [-] *)
    bPT_H2_Header_Trip              : BOOL := FALSE;    (* Complete H2 Sensor Triplication Failure Trip [-] *)

    (* Channel Group 4: Inline Hydrogen-in-Chlorine Photometer Analyzers [% vol] *)
    rAT_H2_in_Cl2_Voted             : REAL := 0.12;     (* 2oo3 Voted H2 in Cl2 Impurity Concentration [% vol] *)
    bAT_H2_in_Cl2_HealthA           : BOOL := TRUE;     (* Photometer Analyzer 4A Healthy Status [-] *)
    bAT_H2_in_Cl2_HealthB           : BOOL := TRUE;     (* Photometer Analyzer 4B Healthy Status [-] *)
    bAT_H2_in_Cl2_HealthC           : BOOL := TRUE;     (* Photometer Analyzer 4C Healthy Status [-] *)
    rAT_H2_in_Cl2_Disc_AB_ms        : REAL := 0.0;      (* Photometer 4A vs 4B Discrepancy Timer [ms] *)
    rAT_H2_in_Cl2_Disc_BC_ms        : REAL := 0.0;      (* Photometer 4B vs 4C Discrepancy Timer [ms] *)
    rAT_H2_in_Cl2_Disc_CA_ms        : REAL := 0.0;      (* Photometer 4C vs 4A Discrepancy Timer [ms] *)
    bAT_H2_in_Cl2_Degraded          : BOOL := FALSE;    (* Photometer Operating in Degraded 2oo2 Voting [-] *)
    bAT_H2_in_Cl2_SingleFallback    : BOOL := FALSE;    (* Photometer Operating on Single Channel 1oo1 [-] *)
    bAT_H2_in_Cl2_Trip              : BOOL := FALSE;    (* Complete Photometer Triplication Failure Trip [-] *)

    (* Channel Group 5: Anolyte Depleted Brine Concentration Analyzers [g/L] *)
    rAT_Anolyte_NaCl_Voted          : REAL := 205.0;    (* 2oo3 Voted Depleted Brine Concentration [g/L] *)
    bAT_Anolyte_NaCl_HealthA        : BOOL := TRUE;     (* Brine Analyzer 5A Healthy Status [-] *)
    bAT_Anolyte_NaCl_HealthB        : BOOL := TRUE;     (* Brine Analyzer 5B Healthy Status [-] *)
    bAT_Anolyte_NaCl_HealthC        : BOOL := TRUE;     (* Brine Analyzer 5C Healthy Status [-] *)
    rAT_Anolyte_NaCl_Disc_AB_ms     : REAL := 0.0;      (* Brine Analyzer 5A vs 5B Discrepancy Timer [ms] *)
    rAT_Anolyte_NaCl_Disc_BC_ms     : REAL := 0.0;      (* Brine Analyzer 5B vs 5C Discrepancy Timer [ms] *)
    rAT_Anolyte_NaCl_Disc_CA_ms     : REAL := 0.0;      (* Brine Analyzer 5C vs 5A Discrepancy Timer [ms] *)
    bAT_Anolyte_NaCl_Degraded       : BOOL := FALSE;    (* Brine Analyzer Operating in Degraded 2oo2 Voting [-] *)
    bAT_Anolyte_NaCl_SingleFallback : BOOL := FALSE;    (* Brine Analyzer Operating on Single Channel 1oo1 [-] *)
    bAT_Anolyte_NaCl_Trip           : BOOL := FALSE;    (* Complete Brine Analyzer Triplication Failure Trip [-] *)

    (* Channel Group 6: Catholyte Caustic Soda Concentration Analyzers [wt%] *)
    rAT_Catholyte_NaOH_Voted        : REAL := 32.5;     (* 2oo3 Voted Caustic Soda Concentration [wt%] *)
    bAT_Catholyte_NaOH_HealthA      : BOOL := TRUE;     (* Caustic Analyzer 6A Healthy Status [-] *)
    bAT_Catholyte_NaOH_HealthB      : BOOL := TRUE;     (* Caustic Analyzer 6B Healthy Status [-] *)
    bAT_Catholyte_NaOH_HealthC      : BOOL := TRUE;     (* Caustic Analyzer 6C Healthy Status [-] *)
    rAT_Catholyte_NaOH_Disc_AB_ms   : REAL := 0.0;      (* Caustic Analyzer 6A vs 6B Discrepancy Timer [ms] *)
    rAT_Catholyte_NaOH_Disc_BC_ms   : REAL := 0.0;      (* Caustic Analyzer 6B vs 6C Discrepancy Timer [ms] *)
    rAT_Catholyte_NaOH_Disc_CA_ms   : REAL := 0.0;      (* Caustic Analyzer 6C vs 6A Discrepancy Timer [ms] *)
    bAT_Catholyte_NaOH_Degraded     : BOOL := FALSE;    (* Caustic Analyzer Operating in Degraded 2oo2 Voting [-] *)
    bAT_Catholyte_NaOH_SingleFallback: BOOL := FALSE;   (* Caustic Analyzer Operating on Single Channel 1oo1 [-] *)
    bAT_Catholyte_NaOH_Trip         : BOOL := FALSE;    (* Complete Caustic Analyzer Triplication Failure Trip [-] *)

    (* Electrochemical Constants & Physical System Properties *)
    rFaradayConst_C_mol             : REAL := 96485.332;(* Faraday Constant [C/mol] *)
    rGasConst_J_molK                : REAL := 8.31446;  (* Universal Gas Constant [J/(mol.K)] *)
    rMolarVol_Nm3_kmol              : REAL := 22.414;   (* Standard Ideal Gas Molar Volume [Nm3/kmol] *)
    rNumberCellsInBipolarStack      : REAL := 27.0;     (* Total Number of Series Connected Cells in Stack [-] *)
    rMembraneAreaPerCell_m2         : REAL := 2.67;     (* Active Ion-Exchange Membrane Area Per Cell [m2] *)
    rTotalActiveMembraneArea_m2     : REAL := 72.09;    (* Total Active Area = 27 cells * 2.67 m2 [m2] *)
    rMolarMass_Cl2_kg_kmol          : REAL := 70.906;   (* Molecular Weight of Chlorine Gas [kg/kmol] *)
    rMolarMass_H2_kg_kmol           : REAL := 2.016;    (* Molecular Weight of Hydrogen Gas [kg/kmol] *)
    rMolarMass_NaOH_kg_kmol         : REAL := 39.997;   (* Molecular Weight of Sodium Hydroxide [kg/kmol] *)
    rStandardElectrodePotential_V   : REAL := 2.195;    (* Standard Reversible Cell Potential E0 at 25 deg C [V] *)
    rReactionEnthalpy_kJ_mol        : REAL := 283.0;    (* Standard Thermoneutral Enthalpy of Reaction [kJ/mol] *)

    (* Calculated Electrochemical Intermediate Variables *)
    rNernstPotential_V              : REAL := 2.180;    (* Temperature and Activity Corrected Nernst Potential [V] *)
    rAnodeOverpotential_V           : REAL := 0.085;    (* Chlorine Evolution Kinetic Overpotential on DSA [V] *)
    rCathodeOverpotential_V         : REAL := 0.115;    (* Hydrogen Evolution Kinetic Overpotential on Nickel [V] *)
    rMembraneOhmicDrop_V            : REAL := 0.380;    (* Nafion/Flemion Bilayer Membrane IR Drop [V] *)
    rElectrolyteOhmicDrop_V         : REAL := 0.160;    (* Brine and Caustic Bulk Solution IR Voltage Drop [V] *)
    rTheoreticalCellVoltage_V       : REAL := 2.920;    (* Theoretical Sum of Reversible, Overpotentials and IR [V] *)
    rCellVoltageDeviation_V         : REAL := 0.0;      (* Actual vs Model Theoretical Cell Voltage Deviation [V] *)
    rFaradayCurrentEfficiency       : REAL := 0.965;    (* Fractional Faraday Current Efficiency (0.95 to 0.98) [-] *)

    (* Deterministic 14-Stage Production Finite State Machine (FSM) Engine *)
    eState                          : INT := 0;         (* Active Operational State Index [0..13] [-] *)
    ePrevState                      : INT := 0;         (* Previous Cycle Operational State Index [0..13] [-] *)
    rStateTimer_s                   : REAL := 0.0;      (* Dwell Time Elapsed in Active State [s] *)
    rSubStateTimer_s                : REAL := 0.0;      (* Auxiliary Internal Sub-State Dwell Timer [s] *)
    iFsmStepIndex                   : INT := 0;         (* Sequential Step Index Within Active State [-] *)
    bFsmTransitionTrigger           : BOOL := FALSE;    (* Inter-State Transition Permissive Trigger [-] *)

    (* Sequence, Purge & Ramp Specific Timers *)
    rPurgeTimer_s                   : REAL := 0.0;      (* Nitrogen Header Inert Purge Duration Timer [s] *)
    rLeakCheckTimer_s               : REAL := 0.0;      (* Header Pressure Hold Leak Decay Check Timer [s] *)
    rBrineWarmupTimer_s             : REAL := 0.0;      (* Brine Thermal Circulation Warmup Timer [s] *)
    rPolarizationInitTimer_s        : REAL := 0.0;      (* Rectifier Minimum Polarization Stabilization Timer [s] *)
    rLowLoadRampTimer_s             : REAL := 0.0;      (* Rectifier Ramp to 25% Low Load Current Timer [s] *)
    rPressureEquilibrationTimer_s   : REAL := 0.0;      (* Differential Pressure Zero-Balancing Dwell Timer [s] *)
    rTurndownRampTimer_s            : REAL := 0.0;      (* Rectifier Orderly Load Turndown Timer [s] *)
    rShutdownPolarizationTimer_s    : REAL := 0.0;      (* Post-Turndown Polarization Hold Timer [s] *)
    rEmergencyTripTimer_s           : REAL := 0.0;      (* Emergency Fast Vent Scrubber Evacuation Timer [s] *)
    rPostTripBlanketTimer_s         : REAL := 0.0;      (* Post-Trip Nitrogen Sweeping and Inert Blanket Timer [s] *)

    (* ISA-18.2 Multi-Tier Process Alarm Limits, Deadbands & Active Latch Bits *)
    (* Cell Differential Pressure Alarms [mbar] *)
    rDP_HH_Limit_mbar               : REAL := 6.0;      (* Cell DP High-High Membrane Rupture Danger Trip [mbar] *)
    rDP_H_Limit_mbar                : REAL := 3.0;      (* Cell DP High Deviation Warning [mbar] *)
    rDP_L_Limit_mbar                : REAL := -3.0;     (* Cell DP Low Deviation Warning [mbar] *)
    rDP_LL_Limit_mbar               : REAL := -6.0;     (* Cell DP Low-Low Reverse Pinch Rupture Trip [mbar] *)
    rDP_Deadband_mbar               : REAL := 0.40;     (* Cell DP Alarm Clearance Hysteresis [mbar] *)

    (* Chlorine Header Pressure Alarms [bar] *)
    rP_Cl2_HH_Limit_bar             : REAL := 0.60;     (* Chlorine Header Overpressure Trip [bar] *)
    rP_Cl2_H_Limit_bar              : REAL := 0.40;     (* Chlorine Header High Pressure Warning [bar] *)
    rP_Cl2_L_Limit_bar              : REAL := 0.05;     (* Chlorine Header Low Pressure Warning [bar] *)
    rP_Cl2_LL_Limit_bar             : REAL := -0.02;    (* Chlorine Header Vacuum Ingress Explosion Trip [bar] *)
    rP_Cl2_Deadband_bar             : REAL := 0.020;    (* Chlorine Pressure Alarm Clearance Hysteresis [bar] *)

    (* Hydrogen Header Pressure Alarms [bar] *)
    rP_H2_HH_Limit_bar              : REAL := 0.62;     (* Hydrogen Header Overpressure Trip [bar] *)
    rP_H2_H_Limit_bar               : REAL := 0.42;     (* Hydrogen Header High Pressure Warning [bar] *)
    rP_H2_L_Limit_bar               : REAL := 0.06;     (* Hydrogen Header Low Pressure Warning [bar] *)
    rP_H2_LL_Limit_bar              : REAL := -0.01;    (* Hydrogen Header Vacuum Ingress Explosion Trip [bar] *)
    rP_H2_Deadband_bar              : REAL := 0.020;    (* Hydrogen Pressure Alarm Clearance Hysteresis [bar] *)

    (* Inline Hydrogen-in-Chlorine Purity Alarms [% vol] *)
    rH2_in_Cl2_HH_Limit_pct         : REAL := 1.20;     (* H2 in Cl2 Explosive Detonation Risk Hard Trip [% vol] *)
    rH2_in_Cl2_H_Limit_pct          : REAL := 0.60;     (* H2 in Cl2 High Contamination Advisory Warning [% vol] *)
    rH2_in_Cl2_L_Limit_pct          : REAL := 0.05;     (* H2 in Cl2 Low Baseline Operating Sanity [% vol] *)
    rH2_in_Cl2_LL_Limit_pct         : REAL := 0.00;     (* Photometer Zero Calibration Drift Failure [% vol] *)
    rH2_in_Cl2_Deadband_pct         : REAL := 0.050;    (* H2 in Cl2 Alarm Clearance Hysteresis [% vol] *)

    (* Anolyte Depleted Brine Concentration Alarms [g/L] *)
    rBrine_HH_Limit_gL              : REAL := 240.0;    (* Depleted Brine High Concentration Inefficient Feed [g/L] *)
    rBrine_H_Limit_gL               : REAL := 225.0;    (* Depleted Brine High Concentration Advisory [g/L] *)
    rBrine_L_Limit_gL               : REAL := 190.0;    (* Depleted Brine Low Salt Under-Saturation Warning [g/L] *)
    rBrine_LL_Limit_gL              : REAL := 175.0;    (* Depleted Brine Severe Oxygen Evolution Anode Rupture Trip [g/L] *)
    rBrine_Deadband_gL              : REAL := 3.0;      (* Brine Concentration Alarm Clearance Hysteresis [g/L] *)

    (* Catholyte Caustic Soda Concentration Alarms [wt%] *)
    rCaustic_HH_Limit_pct           : REAL := 36.0;     (* Caustic High-High Precipitation & Scaling Trip [wt%] *)
    rCaustic_H_Limit_pct            : REAL := 34.5;     (* Caustic High Concentration Deviation Warning [wt%] *)
    rCaustic_L_Limit_pct            : REAL := 31.0;     (* Caustic Low Concentration Deviation Warning [wt%] *)
    rCaustic_LL_Limit_pct           : REAL := 28.0;     (* Caustic Low-Low Water Back-Migration Efficiency Trip [wt%] *)
    rCaustic_Deadband_pct           : REAL := 0.40;     (* Caustic Concentration Alarm Clearance Hysteresis [wt%] *)

    (* Cell Stack Temperature Alarms [deg C] *)
    rTemp_HH_Limit_degC             : REAL := 93.0;     (* Bulk Temperature Boiling & Localized Steam Pocket Trip [deg C] *)
    rTemp_H_Limit_degC              : REAL := 90.0;     (* Bulk Temperature High Thermal Warning [deg C] *)
    rTemp_L_Limit_degC              : REAL := 80.0;     (* Bulk Temperature Low Operating Warning [deg C] *)
    rTemp_LL_Limit_degC             : REAL := 70.0;     (* Bulk Temperature Low Cold Membrane High Resistance Trip [deg C] *)
    rTemp_Deadband_degC             : REAL := 1.0;      (* Cell Temperature Alarm Clearance Hysteresis [deg C] *)

    (* Single-Cell Polarization Voltage Alarms [V] *)
    rVolt_HH_Limit_V                : REAL := 3.55;     (* Cell Polarization High-High Blistering / Passivation Trip [V] *)
    rVolt_H_Limit_V                 : REAL := 3.35;     (* Cell Polarization High Voltage Efficiency Warning [V] *)
    rVolt_L_Limit_V                 : REAL := 2.85;     (* Cell Polarization Low Voltage Efficiency Advisory [V] *)
    rVolt_LL_Limit_V                : REAL := 2.10;     (* Cell Polarization Low-Low Reverse Current Short Trip [V] *)
    rVolt_Deadband_V                : REAL := 0.050;    (* Cell Voltage Alarm Clearance Hysteresis [V] *)

    (* Active Alarm Condition Latch Booleans *)
    bAlarm_DP_HH                    : BOOL := FALSE;
    bAlarm_DP_H                     : BOOL := FALSE;
    bAlarm_DP_L                     : BOOL := FALSE;
    bAlarm_DP_LL                    : BOOL := FALSE;
    bAlarm_P_Cl2_HH                 : BOOL := FALSE;
    bAlarm_P_Cl2_H                  : BOOL := FALSE;
    bAlarm_P_Cl2_L                  : BOOL := FALSE;
    bAlarm_P_Cl2_LL                 : BOOL := FALSE;
    bAlarm_P_H2_HH                  : BOOL := FALSE;
    bAlarm_P_H2_H                   : BOOL := FALSE;
    bAlarm_P_H2_L                   : BOOL := FALSE;
    bAlarm_P_H2_LL                  : BOOL := FALSE;
    bAlarm_H2_in_Cl2_HH             : BOOL := FALSE;
    bAlarm_H2_in_Cl2_H              : BOOL := FALSE;
    bAlarm_H2_in_Cl2_L              : BOOL := FALSE;
    bAlarm_H2_in_Cl2_LL             : BOOL := FALSE;
    bAlarm_Brine_HH                 : BOOL := FALSE;
    bAlarm_Brine_H                  : BOOL := FALSE;
    bAlarm_Brine_L                  : BOOL := FALSE;
    bAlarm_Brine_LL                 : BOOL := FALSE;
    bAlarm_Caustic_HH               : BOOL := FALSE;
    bAlarm_Caustic_H                : BOOL := FALSE;
    bAlarm_Caustic_L                : BOOL := FALSE;
    bAlarm_Caustic_LL               : BOOL := FALSE;
    bAlarm_Temp_HH                  : BOOL := FALSE;
    bAlarm_Temp_H                   : BOOL := FALSE;
    bAlarm_Temp_L                   : BOOL := FALSE;
    bAlarm_Temp_LL                  : BOOL := FALSE;
    bAlarm_Volt_HH                  : BOOL := FALSE;
    bAlarm_Volt_H                   : BOOL := FALSE;
    bAlarm_Volt_L                   : BOOL := FALSE;
    bAlarm_Volt_LL                  : BOOL := FALSE;

    (* First-Out Latching Internal Architecture *)
    bFirstOutLatched                : BOOL := FALSE;    (* First-Out Root Cause Trip Code Latched [-] *)
    dwFirstOutCapturedCode          : DWORD := 16#00000000; (* Latched Initial Hardware Root Cause Code [-] *)

    (* Scratch Loop Counters & Temporary Math Computation Workspace *)
    iIdx                            : INT := 0;         (* Primary State Index Loop Counter [-] *)
    jIdx                            : INT := 0;         (* Matrix Column Loop Counter [-] *)
    mIdx                            : INT := 0;         (* Actuator Dimension Loop Counter [-] *)
    kStep                           : INT := 0;         (* Receding Horizon Step Counter [-] *)
    iIter                           : INT := 0;         (* PGD Optimization Unrolled Iteration Counter [-] *)
    rTempSum                        : REAL := 0.0;      (* Dot Product Matrix Multiply Accumulator [-] *)
    rTempDiff                       : REAL := 0.0;      (* Scalar Difference Intermediate Real [-] *)
    rTempCandidate                  : REAL := 0.0;      (* Actuator Gradient Candidate Intermediate Real [-] *)
    rTempDeltaU                     : REAL := 0.0;      (* Actuator Slew Rate Intermediate Step [-] *)
    rTempMaxDev                     : REAL := 0.0;      (* Maximum State Vector Deviation Diagnostic [-] *)
    rTempGasMols                    : REAL := 0.0;      (* Molar Gas Reaction Rate Intermediate Real [-] *)
END_VAR
"""

with open("dataset_parts/part1_vars.txt", "w", encoding="utf-8") as f:
    f.write(part1)

print("Part 1 written successfully.")
