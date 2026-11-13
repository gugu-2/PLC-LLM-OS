FUNCTION_BLOCK FB_Chemical_ChlorAlkali_MembraneElectrolyzer_DPControl
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

(* ==================================================================================================== *)
(* PHASE 0: FIRST SCAN INITIALIZATION & DISCRETE CYBER-PHYSICAL STATE-SPACE MATRIX CONFIGURATION        *)
(* Sampling Period Ts = 0.020 [s] (20 [ms] Hard Real-Time Deterministic Cyclic Scan)                    *)
(* States: x[0]=DP [mbar], x[1]=P_Cl2 [bar], x[2]=P_H2 [bar], x[3]=C_NaCl [g/L], x[4]=C_NaOH [wt%],     *)
(*         x[5]=T_cell [deg C]                                                                          *)
(* Inputs: u[0]=CV_H2 [%], u[1]=CV_Cl2 [%], u[2]=CV_Water [%], u[3]=CV_Brine [%], u[4]=I_rect [kA]      *)
(* ==================================================================================================== *)
IF NOT bFirstScanDone THEN
    (* ------------------------------------------------------------------------------------------------ *)
    (* 6x6 Discrete State Transition Dynamic Matrix A                                                  *)
    (* Reflects Gas Compressibility, Membrane Cross-Migration, Electrochemical Reactions & Joule Heat   *)
    (* ------------------------------------------------------------------------------------------------ *)
    matA[0, 0] := 0.98520; (* DP Autoregressive Pole (Cathode/Anode Compartment Compliance) [-] *)
    matA[0, 1] := -0.01250; (* Cl2 Header Pressure Cross-Coupling on Differential Pressure [-] *)
    matA[0, 2] := 0.01420; (* H2 Header Pressure Cross-Coupling on Differential Pressure [-] *)
    matA[0, 3] := 0.00015; (* Anolyte Density & Static Head Drift on Cell Differential Pressure [-] *)
    matA[0, 4] := -0.00028; (* Catholyte Density & Dynamic Viscosity Drift on Cell DP [-] *)
    matA[0, 5] := 0.00350; (* Thermal Expansion and Gas Expansion Molar Flow Rate on Cell DP [-] *)

    matA[1, 0] := -0.00180; (* Differential Pressure Feedback onto Cl2 Collector Header [-] *)
    matA[1, 1] := 0.99120; (* Cl2 Header Gas Volume Hold-Up and Acoustic Flow Decay [-] *)
    matA[1, 2] := 0.00045; (* Hydraulic Inter-Header Pressure Cross-Talk via Acid Seal [-] *)
    matA[1, 3] := 0.00008; (* Brine Saturation Influence on Cl2 Gas Desorption Rate [-] *)
    matA[1, 4] := 0.00000; (* Catholyte Caustic Decoupled from Chlorine Header [-] *)
    matA[1, 5] := 0.00115; (* Thermal Influence on Wet Chlorine Header Vapor Pressure [-] *)

    matA[2, 0] := 0.00210; (* Differential Pressure Feedback onto H2 Collector Header [-] *)
    matA[2, 1] := 0.00050; (* Cl2 to H2 Acoustic Wave Cross-Coupling via Cell Frames [-] *)
    matA[2, 2] := 0.99080; (* H2 Header Gas Volume Hold-Up and Compressor Suction Decay [-] *)
    matA[2, 3] := 0.00000; (* Anolyte Brine Decoupled from Hydrogen Header [-] *)
    matA[2, 4] := -0.00012; (* Caustic Concentration Effect on Hydrogen Water Vapor Evaporation [-] *)
    matA[2, 5] := 0.00135; (* Thermal Influence on Saturated Hydrogen Gas Header Pressure [-] *)

    matA[3, 0] := 0.00005; (* Differential Pressure Membrane Flexing on Anolyte Retention [-] *)
    matA[3, 1] := 0.00010; (* Chlorine Gas Evolution Gas-Lift Circulation Rate on Brine Mixing [-] *)
    matA[3, 2] := 0.00000; (* Hydrogen Header Decoupled from Anolyte NaCl [-] *)
    matA[3, 3] := 0.99780; (* Anolyte Saturated Brine Hydraulic Residence Time Decay [-] *)
    matA[3, 4] := -0.00040; (* Osmotic Water Transport Across Membrane from Anolyte to Catholyte [-] *)
    matA[3, 5] := -0.00185; (* Temperature Acceleration of Electrochemical Consumption of NaCl [-] *)

    matA[4, 0] := -0.00008; (* Differential Pressure Membrane Piezoresistive Deformation on Water Flow [-] *)
    matA[4, 1] := 0.00000; (* Chlorine Header Decoupled from Caustic Concentration [-] *)
    matA[4, 2] := 0.00012; (* Hydrogen Gas-Lift Mixing Kinetics in Catholyte Compartment [-] *)
    matA[4, 3] := 0.00025; (* Hydration Sphere Electro-Osmotic Drag Coupling (3.5 H2O / Na+) [-] *)
    matA[4, 4] := 0.99810; (* Catholyte Tank Caustic Inventory Dynamic Residence Pole [-] *)
    matA[4, 5] := 0.00095; (* Evaporative Loss of Water Elevating Caustic Concentration [-] *)

    matA[5, 0] := 0.00010; (* Pressure Fluctuation Joule Heat Redistribution [-] *)
    matA[5, 1] := 0.00020; (* Cl2 Vaporization Heat Removal Coupling [-] *)
    matA[5, 2] := 0.00025; (* H2 Vaporization Latent Heat Removal Coupling [-] *)
    matA[5, 3] := -0.00050; (* Brine Inflow Sensible Heat Advection Rate [-] *)
    matA[5, 4] := -0.00065; (* Soft Water Dilution Sensible Heat Advection Rate [-] *)
    matA[5, 5] := 0.99890; (* Electrolyzer Cell Stack Bulk Thermal Inertia Time Constant [-] *)

    (* ------------------------------------------------------------------------------------------------ *)
    (* 6x5 Discrete Input Mapping Matrix B: Fast Valves, Water Dilution, Brine Trim & DC Current       *)
    (* Inputs: u[0]=CV_H2 [%], u[1]=CV_Cl2 [%], u[2]=CV_Water [%], u[3]=CV_Brine [%], u[4]=I_rect [kA]  *)
    (* ------------------------------------------------------------------------------------------------ *)
    matB[0, 0] := -0.1850; (* Opening H2 Backpressure Valve Drops H2 Pressure, Decreasing DP [mbar/%] *)
    matB[0, 1] := 0.1920;  (* Opening Cl2 Scrubber Vent Drops Cl2 Pressure, Increasing DP [mbar/%] *)
    matB[0, 2] := -0.0045; (* Soft Water Inflow Slightly Increases Catholyte Liquid Head [mbar/%] *)
    matB[0, 3] := 0.0035;  (* Fresh Saturated Brine Feed Increases Anolyte Hydrostatic Head [mbar/%] *)
    matB[0, 4] := 0.0450;  (* Fast Rectifier Current Step Generates Transient Molar Gas Delta [mbar/kA] *)

    matB[1, 0] := 0.0008;  (* H2 Backpressure Minor Cross-Talk to Cl2 Header via Pressure Transducers [bar/%] *)
    matB[1, 1] := -0.0145; (* Opening Cl2 Scrubber Valve Directly Depressurizes Cl2 Header [bar/%] *)
    matB[1, 2] := 0.0000;  (* Soft Water Dilution Decoupled from Chlorine Header [bar/%] *)
    matB[1, 3] := 0.0001;  (* Brine Infeed Entrained Gas Displacement [bar/%] *)
    matB[1, 4] := 0.0085;  (* Faradaic Chlorine Gas Generation Rate: 1 kA -> 0.0085 bar/scan [bar/kA] *)

    matB[2, 0] := -0.0152; (* Opening H2 Backpressure Valve Directly Depressurizes H2 Header [bar/%] *)
    matB[2, 1] := 0.0007;  (* Cl2 Scrubber Vent Valve Acoustic Reflection on H2 Header [bar/%] *)
    matB[2, 2] := 0.0002;  (* Water Addition Minor Vapor Space Compression [bar/%] *)
    matB[2, 3] := 0.0000;  (* Brine Feed Decoupled from Hydrogen Gas Header [bar/%] *)
    matB[2, 4] := 0.0088;  (* Faradaic Hydrogen Gas Generation Rate: 1 kA -> 0.0088 bar/scan [bar/kA] *)

    matB[3, 0] := 0.0000;  (* H2 Valve Decoupled from Brine Concentration [g/L/%] *)
    matB[3, 1] := 0.0000;  (* Cl2 Valve Decoupled from Brine Concentration [g/L/%] *)
    matB[3, 2] := -0.0015; (* Catholyte Dilution Slight Water Osmosis Shift on Brine [g/L/%] *)
    matB[3, 3] := 0.0850;  (* Saturated Feed Brine Trim Valve Increases Salt Concentration [g/L/%] *)
    matB[3, 4] := -0.1250; (* Faradaic Consumption of NaCl: -0.125 g/L per kA per scan [g/L/kA] *)

    matB[4, 0] := 0.0000;  (* H2 Valve Decoupled from Caustic Concentration [wt%/%] *)
    matB[4, 1] := 0.0000;  (* Cl2 Valve Decoupled from Caustic Concentration [wt%/%] *)
    matB[4, 2] := -0.0480; (* Soft Demin Water Dilution Valve Lowers Caustic Concentration [wt%/%] *)
    matB[4, 3] := 0.0005;  (* Saturated Brine Trace Water Cross-Transport [wt%/%] *)
    matB[4, 4] := 0.0385;  (* Faradaic Generation of NaOH: +0.0385 wt% per kA per scan [wt%/kA] *)

    matB[5, 0] := -0.0005; (* H2 Depressurization Flash Cooling [deg C/%] *)
    matB[5, 1] := -0.0005; (* Cl2 Depressurization Flash Cooling [deg C/%] *)
    matB[5, 2] := -0.0120; (* Cold Demin Water Inflow Thermal Quenching [deg C/%] *)
    matB[5, 3] := 0.0080;  (* Warm Saturated Brine Inflow Sensible Heating [deg C/%] *)
    matB[5, 4] := 0.0650;  (* Rectifier Ohmic & Kinetic Overpotential Joule Dissipation [deg C/kA] *)

    (* ------------------------------------------------------------------------------------------------ *)
    (* 6x6 Discrete Measurement Mapping Matrix C: Direct Voted Sensor Projections                      *)
    (* ------------------------------------------------------------------------------------------------ *)
    matC[0, 0] := 1.0000; (* y[0] = Voted Cell Differential Pressure [mbar] *)
    matC[0, 1] := 0.0000;
    matC[0, 2] := 0.0000;
    matC[0, 3] := 0.0000;
    matC[0, 4] := 0.0000;
    matC[0, 5] := 0.0000;

    matC[1, 0] := 0.0000;
    matC[1, 1] := 1.0000; (* y[1] = Voted Chlorine Header Pressure [bar] *)
    matC[1, 2] := 0.0000;
    matC[1, 3] := 0.0000;
    matC[1, 4] := 0.0000;
    matC[1, 5] := 0.0000;

    matC[2, 0] := 0.0000;
    matC[2, 1] := 0.0000;
    matC[2, 2] := 1.0000; (* y[2] = Voted Hydrogen Header Pressure [bar] *)
    matC[2, 3] := 0.0000;
    matC[2, 4] := 0.0000;
    matC[2, 5] := 0.0000;

    matC[3, 0] := 0.0000;
    matC[3, 1] := 0.0000;
    matC[3, 2] := 0.0000;
    matC[3, 3] := 1.0000; (* y[3] = Voted Anolyte Depleted Brine Concentration [g/L] *)
    matC[3, 4] := 0.0000;
    matC[3, 5] := 0.0000;

    matC[4, 0] := 0.0000;
    matC[4, 1] := 0.0000;
    matC[4, 2] := 0.0000;
    matC[4, 3] := 0.0000;
    matC[4, 4] := 1.0000; (* y[4] = Voted Catholyte Caustic Concentration [wt%] *)
    matC[4, 5] := 0.0000;

    matC[5, 0] := 0.0000;
    matC[5, 1] := 0.0000;
    matC[5, 2] := 0.0000;
    matC[5, 3] := 0.0000;
    matC[5, 4] := 0.0000;
    matC[5, 5] := 1.0000; (* y[5] = Electrolyzer Cell Bulk Temperature [deg C] *)

    (* ------------------------------------------------------------------------------------------------ *)
    (* 6x5 Direct Feedthrough Matrix D: Transient Pneumatic Acoustic Shock Feedthrough                 *)
    (* ------------------------------------------------------------------------------------------------ *)
    matD[0, 0] := -0.0150; (* High-Speed Acoustic Delta Pressure Pulse from H2 Valve Quick-Opening [-] *)
    matD[0, 1] := 0.0160;  (* High-Speed Acoustic Delta Pressure Pulse from Cl2 Valve Quick-Opening [-] *)
    matD[0, 2] := 0.0000;
    matD[0, 3] := 0.0000;
    matD[0, 4] := 0.0050;  (* Rectifier Rapid Commutation Inductive Kickback [-] *)

    matD[1, 0] := 0.0000;
    matD[1, 1] := -0.0025; (* Cl2 Valve Throat Pneumatic Choke Transient [-] *)
    matD[1, 2] := 0.0000;
    matD[1, 3] := 0.0000;
    matD[1, 4] := 0.0010;  (* Immediate Faradaic Gas Bubble Nucleation Displacement [-] *)

    matD[2, 0] := -0.0028; (* H2 Valve Throat Sonic Choke Transient [-] *)
    matD[2, 1] := 0.0000;
    matD[2, 2] := 0.0000;
    matD[2, 3] := 0.0000;
    matD[2, 4] := 0.0012;  (* Immediate Cathode Gas Bubble Nucleation Displacement [-] *)

    matD[3, 0] := 0.0000;
    matD[3, 1] := 0.0000;
    matD[3, 2] := 0.0000;
    matD[3, 3] := 0.0050;  (* Brine Inflow Manifold Header Local Conductivity Spike [-] *)
    matD[3, 4] := 0.0000;

    matD[4, 0] := 0.0000;
    matD[4, 1] := 0.0000;
    matD[4, 2] := -0.0040; (* Dilution Water Quench Injection Manifold Local Dilution [-] *)
    matD[4, 3] := 0.0000;
    matD[4, 4] := 0.0000;

    matD[5, 0] := 0.0000;
    matD[5, 1] := 0.0000;
    matD[5, 2] := 0.0000;
    matD[5, 3] := 0.0000;
    matD[5, 4] := 0.0020;  (* Fast Busbar Resistive Ohmic Dissipation Sensor Radiance [-] *)

    (* ------------------------------------------------------------------------------------------------ *)
    (* 6x6 Steady-State Luenberger Observer Innovation Gain Matrix L (Discrete Kalman Filter Solution) *)
    (* Eliminates Sensor Noise While Retaining High-Bandwidth Response to DP Deviations                *)
    (* ------------------------------------------------------------------------------------------------ *)
    matL[0, 0] := 0.3250; (* Primary DP Innovation Gain on Differential Pressure Estimate [-] *)
    matL[0, 1] := -0.0450; (* Cl2 Pressure Error Correction on Differential Pressure [-] *)
    matL[0, 2] := 0.0480; (* H2 Pressure Error Correction on Differential Pressure [-] *)
    matL[0, 3] := 0.0015; (* Brine Measurement Innovation on Differential Pressure [-] *)
    matL[0, 4] := -0.0020; (* Caustic Innovation on Differential Pressure [-] *)
    matL[0, 5] := 0.0085; (* Temperature Innovation on Differential Pressure [-] *)

    matL[1, 0] := -0.0250; (* DP Residual on Cl2 Header Pressure Estimate [-] *)
    matL[1, 1] := 0.2850; (* Cl2 Pressure Innovation Gain on Cl2 Header Estimate [-] *)
    matL[1, 2] := 0.0120; (* H2 Residual Cross-Correction on Cl2 Header [-] *)
    matL[1, 3] := 0.0010; (* Brine Concentration Correction [-] *)
    matL[1, 4] := 0.0000;
    matL[1, 5] := 0.0045; (* Temperature Residual Correction on Cl2 Header [-] *)

    matL[2, 0] := 0.0280; (* DP Residual on H2 Header Pressure Estimate [-] *)
    matL[2, 1] := 0.0110; (* Cl2 Residual Cross-Correction on H2 Header [-] *)
    matL[2, 2] := 0.2920; (* H2 Pressure Innovation Gain on H2 Header Estimate [-] *)
    matL[2, 3] := 0.0000;
    matL[2, 4] := -0.0015; (* Caustic Concentration Correction [-] *)
    matL[2, 5] := 0.0050; (* Temperature Residual Correction on H2 Header [-] *)

    matL[3, 0] := 0.0020; (* DP Residual on Anolyte Brine Concentration [-] *)
    matL[3, 1] := 0.0035; (* Cl2 Header Residual on Brine [-] *)
    matL[3, 2] := 0.0000;
    matL[3, 3] := 0.2150; (* Brine Innovation Gain on Anolyte NaCl Estimate [-] *)
    matL[3, 4] := -0.0080; (* Caustic Residual on Brine [-] *)
    matL[3, 5] := -0.0120; (* Temperature Residual on Brine Estimate [-] *)

    matL[4, 0] := -0.0030; (* DP Residual on Catholyte Caustic Concentration [-] *)
    matL[4, 1] := 0.0000;
    matL[4, 2] := 0.0040; (* H2 Header Residual on Caustic [-] *)
    matL[4, 3] := 0.0065; (* Brine Residual on Caustic [-] *)
    matL[4, 4] := 0.2280; (* Caustic Innovation Gain on Catholyte NaOH Estimate [-] *)
    matL[4, 5] := 0.0145; (* Temperature Residual on Caustic Estimate [-] *)

    matL[5, 0] := 0.0050; (* DP Residual on Cell Temperature [-] *)
    matL[5, 1] := 0.0080; (* Cl2 Header Residual on Cell Temperature [-] *)
    matL[5, 2] := 0.0090; (* H2 Header Residual on Cell Temperature [-] *)
    matL[5, 3] := -0.0150; (* Brine Residual on Temperature [-] *)
    matL[5, 4] := -0.0180; (* Caustic Residual on Temperature [-] *)
    matL[5, 5] := 0.1950; (* Temperature Innovation Gain on Bulk Cell Temperature [-] *)

    (* ------------------------------------------------------------------------------------------------ *)
    (* Model Predictive Control (MPC) Quadratic Weighting Tuning Matrices                              *)
    (* Q: State Tracking Penalty (Diagonal), R: Actuator Effort, R_delta: Slew Rate, P: Terminal Cost    *)
    (* ------------------------------------------------------------------------------------------------ *)
    vecQ_weight[0] := 75.0;  (* Very High Penalty on Differential Pressure Tracking Error [mbar] *)
    vecQ_weight[1] := 25.0;  (* Chlorine Header Pressure Tracking Penalty [bar] *)
    vecQ_weight[2] := 25.0;  (* Hydrogen Header Pressure Tracking Penalty [bar] *)
    vecQ_weight[3] := 3.5;   (* Anolyte Brine Concentration Tracking Penalty [g/L] *)
    vecQ_weight[4] := 5.0;   (* Catholyte Caustic Concentration Tracking Penalty [wt%] *)
    vecQ_weight[5] := 2.0;   (* Bulk Cell Electrolyte Temperature Tracking Penalty [deg C] *)

    vecR_weight[0] := 0.18;  (* H2 Backpressure Valve Position Deviation Penalty [-] *)
    vecR_weight[1] := 0.18;  (* Cl2 Scrubber Vent Valve Position Deviation Penalty [-] *)
    vecR_weight[2] := 0.12;  (* Demin Water Dilution Valve Position Penalty [-] *)
    vecR_weight[3] := 0.12;  (* Primary Brine Feed Trim Valve Position Penalty [-] *)
    vecR_weight[4] := 0.04;  (* DC Rectifier Load Current Setpoint Penalty [-] *)

    vecR_delta_weight[0] := 1.85; (* Strict Penalty on H2 Valve High-Frequency Chattering [-] *)
    vecR_delta_weight[1] := 1.85; (* Strict Penalty on Cl2 Valve Rapid Movement [-] *)
    vecR_delta_weight[2] := 0.65; (* Soft Water Slew Rate Penalty [-] *)
    vecR_delta_weight[3] := 0.65; (* Brine Trim Valve Slew Rate Penalty [-] *)
    vecR_delta_weight[4] := 4.50; (* Severe Slew Rate Penalty on Rectifier Current Commutation [-] *)

    vecP_terminal[0] := 180.0; (* Receding Terminal Horizon State Penalty on DP Balance [-] *)
    vecP_terminal[1] := 60.0;  (* Terminal Penalty on Cl2 Header Pressure [-] *)
    vecP_terminal[2] := 60.0;  (* Terminal Penalty on H2 Header Pressure [-] *)
    vecP_terminal[3] := 8.0;   (* Terminal Penalty on Brine Depletion [-] *)
    vecP_terminal[4] := 12.0;  (* Terminal Penalty on Caustic Concentration [-] *)
    vecP_terminal[5] := 5.0;   (* Terminal Penalty on Cell Temperature [-] *)

    (* Actuator Physical Saturation Limits & Maximum Permissible Slew Rates *)
    vecU_min[0] := 0.0;     (* H2 Backpressure Valve Minimum Position [%] *)
    vecU_max[0] := 100.0;   (* H2 Backpressure Valve Maximum Position [%] *)
    vecU_slewMax[0] := 5.0; (* H2 Valve Max Slew: 5.0% per 20 ms scan (250 %/s) [%] *)

    vecU_min[1] := 0.0;     (* Cl2 Vent Scrubber Valve Minimum Position [%] *)
    vecU_max[1] := 100.0;   (* Cl2 Vent Scrubber Valve Maximum Position [%] *)
    vecU_slewMax[1] := 5.0; (* Cl2 Valve Max Slew: 5.0% per 20 ms scan (250 %/s) [%] *)

    vecU_min[2] := 0.0;     (* Soft Water Dilution Valve Minimum Position [%] *)
    vecU_max[2] := 100.0;   (* Soft Water Dilution Valve Maximum Position [%] *)
    vecU_slewMax[2] := 1.5; (* Soft Water Slew: 1.5% per 20 ms scan (75 %/s) [%] *)

    vecU_min[3] := 0.0;     (* Brine Feed Trim Valve Minimum Position [%] *)
    vecU_max[3] := 100.0;   (* Brine Feed Trim Valve Maximum Position [%] *)
    vecU_slewMax[3] := 1.5; (* Brine Trim Slew: 1.5% per 20 ms scan (75 %/s) [%] *)

    vecU_min[4] := 0.0;     (* Rectifier Load Current Minimum: 0.0 kA [kA] *)
    vecU_max[4] := 75.0;    (* Rectifier Load Current Maximum: 75.0 kA (2.8 kA/m2) [kA] *)
    vecU_slewMax[4] := 0.15;(* Rectifier Max Slew: 0.15 kA per scan (7.5 kA/s max ramp) [kA] *)

    (* Initialize State Estimates and Target Vectors to Safe Cold Standby Defaults *)
    vecX_hat[0] := 0.0;     (* Baseline Zero Differential Pressure [mbar] *)
    vecX_hat[1] := 0.0;     (* Atmospheric Starting Cl2 Header Pressure [bar] *)
    vecX_hat[2] := 0.0;     (* Atmospheric Starting H2 Header Pressure [bar] *)
    vecX_hat[3] := 305.0;   (* Fresh Saturated Brine Feed Salt Concentration [g/L] *)
    vecX_hat[4] := 30.0;    (* Starting Weak Caustic Soda Concentration [wt%] *)
    vecX_hat[5] := 25.0;    (* Ambient Starting Cell Temperature [deg C] *)

    vecX_target[0] := 30.0;  (* Design Baseload Differential Pressure Setpoint [mbar] *)
    vecX_target[1] := 0.250; (* Design Baseload Cl2 Header Pressure [bar] *)
    vecX_target[2] := 0.280; (* Design Baseload H2 Header Pressure [bar] *)
    vecX_target[3] := 205.0; (* Optimal Anolyte Depleted Brine Outlet Concentration [g/L] *)
    vecX_target[4] := 32.5;  (* Optimal Commercial Product Caustic Concentration [wt%] *)
    vecX_target[5] := 88.0;  (* Optimal Electrochemical Operating Temperature [deg C] *)

    vecU_prev[0] := 0.0;
    vecU_prev[1] := 0.0;
    vecU_prev[2] := 0.0;
    vecU_prev[3] := 0.0;
    vecU_prev[4] := 0.0;

    vecU[0] := 0.0;
    vecU[1] := 0.0;
    vecU[2] := 0.0;
    vecU[3] := 0.0;
    vecU[4] := 0.0;

    bFirstScanDone := TRUE;
END_IF;

(* ==================================================================================================== *)
(* PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING WITH DISCREPANCY TIMERS                 *)
(* Channels: 1. Cell Differential Pressure (PDT-101A/B/C) [mbar]                                         *)
(*           2. Chlorine Header Pressure (PT-201A/B/C) [bar]                                             *)
(*           3. Hydrogen Header Pressure (PT-301A/B/C) [bar]                                             *)
(*           4. Inline Hydrogen-in-Chlorine Photometer (AT-401A/B/C) [% vol]                             *)
(*           5. Anolyte Depleted Brine Concentration (AT-501A/B/C) [g/L]                                 *)
(*           6. Catholyte Caustic Concentration (AT-601A/B/C) [wt%]                                      *)
(* Fault Handling: Pairwise Discrepancy -> Timer Accumulation -> Disqualification -> Bumpless Degraded   *)
(* ==================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------- *)
(* Channel Group 1: Cell Differential Pressure (Catholyte minus Anolyte) [mbar]                         *)
(* Physical Safe Tolerance: +/- 3.0 mbar; Sensor Range: -50.0 to 100.0 mbar                              *)
(* ---------------------------------------------------------------------------------------------------- *)
(* Sensor Channel Range Sanity Verification *)
IF rPDT_Cell_DP_1A_mbar < -50.0 OR rPDT_Cell_DP_1A_mbar > 100.0 THEN
    bPDT_Cell_DP_HealthA := FALSE;
END_IF;
IF rPDT_Cell_DP_1B_mbar < -50.0 OR rPDT_Cell_DP_1B_mbar > 100.0 THEN
    bPDT_Cell_DP_HealthB := FALSE;
END_IF;
IF rPDT_Cell_DP_1C_mbar < -50.0 OR rPDT_Cell_DP_1C_mbar > 100.0 THEN
    bPDT_Cell_DP_HealthC := FALSE;
END_IF;

(* Pairwise Discrepancy Timers (Threshold: 1.50 mbar deviation for > 300 ms) *)
IF ABS(rPDT_Cell_DP_1A_mbar - rPDT_Cell_DP_1B_mbar) > 1.50 THEN
    rPDT_Cell_DP_Disc_AB_ms := rPDT_Cell_DP_Disc_AB_ms + (tScanCycleTime_s * 1000.0);
ELSE
    rPDT_Cell_DP_Disc_AB_ms := MAX(0.0, rPDT_Cell_DP_Disc_AB_ms - (tScanCycleTime_s * 500.0));
END_IF;

IF ABS(rPDT_Cell_DP_1B_mbar - rPDT_Cell_DP_1C_mbar) > 1.50 THEN
    rPDT_Cell_DP_Disc_BC_ms := rPDT_Cell_DP_Disc_BC_ms + (tScanCycleTime_s * 1000.0);
ELSE
    rPDT_Cell_DP_Disc_BC_ms := MAX(0.0, rPDT_Cell_DP_Disc_BC_ms - (tScanCycleTime_s * 500.0));
END_IF;

IF ABS(rPDT_Cell_DP_1C_mbar - rPDT_Cell_DP_1A_mbar) > 1.50 THEN
    rPDT_Cell_DP_Disc_CA_ms := rPDT_Cell_DP_Disc_CA_ms + (tScanCycleTime_s * 1000.0);
ELSE
    rPDT_Cell_DP_Disc_CA_ms := MAX(0.0, rPDT_Cell_DP_Disc_CA_ms - (tScanCycleTime_s * 500.0));
END_IF;

(* Identify Discordant Channel Beyond 300 ms Integration Limit *)
IF rPDT_Cell_DP_Disc_AB_ms > 300.0 AND rPDT_Cell_DP_Disc_CA_ms > 300.0 THEN
    bPDT_Cell_DP_HealthA := FALSE;
END_IF;
IF rPDT_Cell_DP_Disc_AB_ms > 300.0 AND rPDT_Cell_DP_Disc_BC_ms > 300.0 THEN
    bPDT_Cell_DP_HealthB := FALSE;
END_IF;
IF rPDT_Cell_DP_Disc_BC_ms > 300.0 AND rPDT_Cell_DP_Disc_CA_ms > 300.0 THEN
    bPDT_Cell_DP_HealthC := FALSE;
END_IF;

(* Recovery of Channel Health on Fault Reset Pushbutton *)
IF bFaultReset THEN
    IF rPDT_Cell_DP_1A_mbar >= -50.0 AND rPDT_Cell_DP_1A_mbar <= 100.0 AND rPDT_Cell_DP_Disc_AB_ms < 50.0 AND rPDT_Cell_DP_Disc_CA_ms < 50.0 THEN
        bPDT_Cell_DP_HealthA := TRUE;
    END_IF;
    IF rPDT_Cell_DP_1B_mbar >= -50.0 AND rPDT_Cell_DP_1B_mbar <= 100.0 AND rPDT_Cell_DP_Disc_AB_ms < 50.0 AND rPDT_Cell_DP_Disc_BC_ms < 50.0 THEN
        bPDT_Cell_DP_HealthB := TRUE;
    END_IF;
    IF rPDT_Cell_DP_1C_mbar >= -50.0 AND rPDT_Cell_DP_1C_mbar <= 100.0 AND rPDT_Cell_DP_Disc_BC_ms < 50.0 AND rPDT_Cell_DP_Disc_CA_ms < 50.0 THEN
        bPDT_Cell_DP_HealthC := TRUE;
    END_IF;
END_IF;

(* 2oo3 TMR Voting & Bumpless Degradation Logic for Cell Differential Pressure *)
IF bPDT_Cell_DP_HealthA AND bPDT_Cell_DP_HealthB AND bPDT_Cell_DP_HealthC THEN
    (* All 3 Channels Healthy: Median Selection *)
    IF (rPDT_Cell_DP_1A_mbar >= rPDT_Cell_DP_1B_mbar AND rPDT_Cell_DP_1A_mbar <= rPDT_Cell_DP_1C_mbar) OR
       (rPDT_Cell_DP_1A_mbar >= rPDT_Cell_DP_1C_mbar AND rPDT_Cell_DP_1A_mbar <= rPDT_Cell_DP_1B_mbar) THEN
        rPDT_Cell_DP_Voted := rPDT_Cell_DP_1A_mbar;
    ELSIF (rPDT_Cell_DP_1B_mbar >= rPDT_Cell_DP_1A_mbar AND rPDT_Cell_DP_1B_mbar <= rPDT_Cell_DP_1C_mbar) OR
          (rPDT_Cell_DP_1B_mbar >= rPDT_Cell_DP_1C_mbar AND rPDT_Cell_DP_1B_mbar <= rPDT_Cell_DP_1A_mbar) THEN
        rPDT_Cell_DP_Voted := rPDT_Cell_DP_1B_mbar;
    ELSE
        rPDT_Cell_DP_Voted := rPDT_Cell_DP_1C_mbar;
    END_IF;
    bPDT_Cell_DP_Degraded := FALSE;
    bPDT_Cell_DP_SingleFallback := FALSE;
    bPDT_Cell_DP_Trip := FALSE;
ELSIF (bPDT_Cell_DP_HealthA AND bPDT_Cell_DP_HealthB) OR
      (bPDT_Cell_DP_HealthB AND bPDT_Cell_DP_HealthC) OR
      (bPDT_Cell_DP_HealthC AND bPDT_Cell_DP_HealthA) THEN
    (* 2 Channels Healthy: Degraded 2oo2 Averaging *)
    IF bPDT_Cell_DP_HealthA AND bPDT_Cell_DP_HealthB THEN
        rPDT_Cell_DP_Voted := (rPDT_Cell_DP_1A_mbar + rPDT_Cell_DP_1B_mbar) * 0.50;
    ELSIF bPDT_Cell_DP_HealthB AND bPDT_Cell_DP_HealthC THEN
        rPDT_Cell_DP_Voted := (rPDT_Cell_DP_1B_mbar + rPDT_Cell_DP_1C_mbar) * 0.50;
    ELSE
        rPDT_Cell_DP_Voted := (rPDT_Cell_DP_1C_mbar + rPDT_Cell_DP_1A_mbar) * 0.50;
    END_IF;
    bPDT_Cell_DP_Degraded := TRUE;
    bPDT_Cell_DP_SingleFallback := FALSE;
    bPDT_Cell_DP_Trip := FALSE;
ELSIF bPDT_Cell_DP_HealthA OR bPDT_Cell_DP_HealthB OR bPDT_Cell_DP_HealthC THEN
    (* 1 Channel Healthy: Single Fallback 1oo1 Operation *)
    IF bPDT_Cell_DP_HealthA THEN
        rPDT_Cell_DP_Voted := rPDT_Cell_DP_1A_mbar;
    ELSIF bPDT_Cell_DP_HealthB THEN
        rPDT_Cell_DP_Voted := rPDT_Cell_DP_1B_mbar;
    ELSE
        rPDT_Cell_DP_Voted := rPDT_Cell_DP_1C_mbar;
    END_IF;
    bPDT_Cell_DP_Degraded := TRUE;
    bPDT_Cell_DP_SingleFallback := TRUE;
    bPDT_Cell_DP_Trip := FALSE;
ELSE
    (* All 3 Channels Failed: Critical Hardware Interlock Trip Latch *)
    bPDT_Cell_DP_Degraded := TRUE;
    bPDT_Cell_DP_SingleFallback := TRUE;
    bPDT_Cell_DP_Trip := TRUE;
    (* Hold previous safe voted value *)
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* Channel Group 2: Chlorine Header Pressure Transmitters [bar]                                         *)
(* Operational Range: 0.150 to 0.450 bar; Transmitter Span: -0.100 to 1.500 bar                         *)
(* ---------------------------------------------------------------------------------------------------- *)
IF rPT_Cl2_Header_2A_bar < -0.10 OR rPT_Cl2_Header_2A_bar > 1.50 THEN
    bPT_Cl2_Header_HealthA := FALSE;
END_IF;
IF rPT_Cl2_Header_2B_bar < -0.10 OR rPT_Cl2_Header_2B_bar > 1.50 THEN
    bPT_Cl2_Header_HealthB := FALSE;
END_IF;
IF rPT_Cl2_Header_2C_bar < -0.10 OR rPT_Cl2_Header_2C_bar > 1.50 THEN
    bPT_Cl2_Header_HealthC := FALSE;
END_IF;

IF ABS(rPT_Cl2_Header_2A_bar - rPT_Cl2_Header_2B_bar) > 0.035 THEN
    rPT_Cl2_Header_Disc_AB_ms := rPT_Cl2_Header_Disc_AB_ms + (tScanCycleTime_s * 1000.0);
ELSE
    rPT_Cl2_Header_Disc_AB_ms := MAX(0.0, rPT_Cl2_Header_Disc_AB_ms - (tScanCycleTime_s * 500.0));
END_IF;

IF ABS(rPT_Cl2_Header_2B_bar - rPT_Cl2_Header_2C_bar) > 0.035 THEN
    rPT_Cl2_Header_Disc_BC_ms := rPT_Cl2_Header_Disc_BC_ms + (tScanCycleTime_s * 1000.0);
ELSE
    rPT_Cl2_Header_Disc_BC_ms := MAX(0.0, rPT_Cl2_Header_Disc_BC_ms - (tScanCycleTime_s * 500.0));
END_IF;

IF ABS(rPT_Cl2_Header_2C_bar - rPT_Cl2_Header_2A_bar) > 0.035 THEN
    rPT_Cl2_Header_Disc_CA_ms := rPT_Cl2_Header_Disc_CA_ms + (tScanCycleTime_s * 1000.0);
ELSE
    rPT_Cl2_Header_Disc_CA_ms := MAX(0.0, rPT_Cl2_Header_Disc_CA_ms - (tScanCycleTime_s * 500.0));
END_IF;

IF rPT_Cl2_Header_Disc_AB_ms > 300.0 AND rPT_Cl2_Header_Disc_CA_ms > 300.0 THEN
    bPT_Cl2_Header_HealthA := FALSE;
END_IF;
IF rPT_Cl2_Header_Disc_AB_ms > 300.0 AND rPT_Cl2_Header_Disc_BC_ms > 300.0 THEN
    bPT_Cl2_Header_HealthB := FALSE;
END_IF;
IF rPT_Cl2_Header_Disc_BC_ms > 300.0 AND rPT_Cl2_Header_Disc_CA_ms > 300.0 THEN
    bPT_Cl2_Header_HealthC := FALSE;
END_IF;

IF bFaultReset THEN
    IF rPT_Cl2_Header_2A_bar >= -0.10 AND rPT_Cl2_Header_2A_bar <= 1.50 AND rPT_Cl2_Header_Disc_AB_ms < 50.0 AND rPT_Cl2_Header_Disc_CA_ms < 50.0 THEN
        bPT_Cl2_Header_HealthA := TRUE;
    END_IF;
    IF rPT_Cl2_Header_2B_bar >= -0.10 AND rPT_Cl2_Header_2B_bar <= 1.50 AND rPT_Cl2_Header_Disc_AB_ms < 50.0 AND rPT_Cl2_Header_Disc_BC_ms < 50.0 THEN
        bPT_Cl2_Header_HealthB := TRUE;
    END_IF;
    IF rPT_Cl2_Header_2C_bar >= -0.10 AND rPT_Cl2_Header_2C_bar <= 1.50 AND rPT_Cl2_Header_Disc_BC_ms < 50.0 AND rPT_Cl2_Header_Disc_CA_ms < 50.0 THEN
        bPT_Cl2_Header_HealthC := TRUE;
    END_IF;
END_IF;

IF bPT_Cl2_Header_HealthA AND bPT_Cl2_Header_HealthB AND bPT_Cl2_Header_HealthC THEN
    IF (rPT_Cl2_Header_2A_bar >= rPT_Cl2_Header_2B_bar AND rPT_Cl2_Header_2A_bar <= rPT_Cl2_Header_2C_bar) OR
       (rPT_Cl2_Header_2A_bar >= rPT_Cl2_Header_2C_bar AND rPT_Cl2_Header_2A_bar <= rPT_Cl2_Header_2B_bar) THEN
        rPT_Cl2_Header_Voted := rPT_Cl2_Header_2A_bar;
    ELSIF (rPT_Cl2_Header_2B_bar >= rPT_Cl2_Header_2A_bar AND rPT_Cl2_Header_2B_bar <= rPT_Cl2_Header_2C_bar) OR
          (rPT_Cl2_Header_2B_bar >= rPT_Cl2_Header_2C_bar AND rPT_Cl2_Header_2B_bar <= rPT_Cl2_Header_2A_bar) THEN
        rPT_Cl2_Header_Voted := rPT_Cl2_Header_2B_bar;
    ELSE
        rPT_Cl2_Header_Voted := rPT_Cl2_Header_2C_bar;
    END_IF;
    bPT_Cl2_Header_Degraded := FALSE;
    bPT_Cl2_Header_SingleFallback := FALSE;
    bPT_Cl2_Header_Trip := FALSE;
ELSIF (bPT_Cl2_Header_HealthA AND bPT_Cl2_Header_HealthB) OR
      (bPT_Cl2_Header_HealthB AND bPT_Cl2_Header_HealthC) OR
      (bPT_Cl2_Header_HealthC AND bPT_Cl2_Header_HealthA) THEN
    IF bPT_Cl2_Header_HealthA AND bPT_Cl2_Header_HealthB THEN
        rPT_Cl2_Header_Voted := (rPT_Cl2_Header_2A_bar + rPT_Cl2_Header_2B_bar) * 0.50;
    ELSIF bPT_Cl2_Header_HealthB AND bPT_Cl2_Header_HealthC THEN
        rPT_Cl2_Header_Voted := (rPT_Cl2_Header_2B_bar + rPT_Cl2_Header_2C_bar) * 0.50;
    ELSE
        rPT_Cl2_Header_Voted := (rPT_Cl2_Header_2C_bar + rPT_Cl2_Header_2A_bar) * 0.50;
    END_IF;
    bPT_Cl2_Header_Degraded := TRUE;
    bPT_Cl2_Header_SingleFallback := FALSE;
    bPT_Cl2_Header_Trip := FALSE;
ELSIF bPT_Cl2_Header_HealthA OR bPT_Cl2_Header_HealthB OR bPT_Cl2_Header_HealthC THEN
    IF bPT_Cl2_Header_HealthA THEN
        rPT_Cl2_Header_Voted := rPT_Cl2_Header_2A_bar;
    ELSIF bPT_Cl2_Header_HealthB THEN
        rPT_Cl2_Header_Voted := rPT_Cl2_Header_2B_bar;
    ELSE
        rPT_Cl2_Header_Voted := rPT_Cl2_Header_2C_bar;
    END_IF;
    bPT_Cl2_Header_Degraded := TRUE;
    bPT_Cl2_Header_SingleFallback := TRUE;
    bPT_Cl2_Header_Trip := FALSE;
ELSE
    bPT_Cl2_Header_Degraded := TRUE;
    bPT_Cl2_Header_SingleFallback := TRUE;
    bPT_Cl2_Header_Trip := TRUE;
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* Channel Group 3: Hydrogen Header Pressure Transmitters [bar]                                         *)
(* Operational Range: 0.180 to 0.480 bar; Transmitter Span: -0.100 to 1.500 bar                         *)
(* ---------------------------------------------------------------------------------------------------- *)
IF rPT_H2_Header_3A_bar < -0.10 OR rPT_H2_Header_3A_bar > 1.50 THEN
    bPT_H2_Header_HealthA := FALSE;
END_IF;
IF rPT_H2_Header_3B_bar < -0.10 OR rPT_H2_Header_3B_bar > 1.50 THEN
    bPT_H2_Header_HealthB := FALSE;
END_IF;
IF rPT_H2_Header_3C_bar < -0.10 OR rPT_H2_Header_3C_bar > 1.50 THEN
    bPT_H2_Header_HealthC := FALSE;
END_IF;

IF ABS(rPT_H2_Header_3A_bar - rPT_H2_Header_3B_bar) > 0.035 THEN
    rPT_H2_Header_Disc_AB_ms := rPT_H2_Header_Disc_AB_ms + (tScanCycleTime_s * 1000.0);
ELSE
    rPT_H2_Header_Disc_AB_ms := MAX(0.0, rPT_H2_Header_Disc_AB_ms - (tScanCycleTime_s * 500.0));
END_IF;

IF ABS(rPT_H2_Header_3B_bar - rPT_H2_Header_3C_bar) > 0.035 THEN
    rPT_H2_Header_Disc_BC_ms := rPT_H2_Header_Disc_BC_ms + (tScanCycleTime_s * 1000.0);
ELSE
    rPT_H2_Header_Disc_BC_ms := MAX(0.0, rPT_H2_Header_Disc_BC_ms - (tScanCycleTime_s * 500.0));
END_IF;

IF ABS(rPT_H2_Header_3C_bar - rPT_H2_Header_3A_bar) > 0.035 THEN
    rPT_H2_Header_Disc_CA_ms := rPT_H2_Header_Disc_CA_ms + (tScanCycleTime_s * 1000.0);
ELSE
    rPT_H2_Header_Disc_CA_ms := MAX(0.0, rPT_H2_Header_Disc_CA_ms - (tScanCycleTime_s * 500.0));
END_IF;

IF rPT_H2_Header_Disc_AB_ms > 300.0 AND rPT_H2_Header_Disc_CA_ms > 300.0 THEN
    bPT_H2_Header_HealthA := FALSE;
END_IF;
IF rPT_H2_Header_Disc_AB_ms > 300.0 AND rPT_H2_Header_Disc_BC_ms > 300.0 THEN
    bPT_H2_Header_HealthB := FALSE;
END_IF;
IF rPT_H2_Header_Disc_BC_ms > 300.0 AND rPT_H2_Header_Disc_CA_ms > 300.0 THEN
    bPT_H2_Header_HealthC := FALSE;
END_IF;

IF bFaultReset THEN
    IF rPT_H2_Header_3A_bar >= -0.10 AND rPT_H2_Header_3A_bar <= 1.50 AND rPT_H2_Header_Disc_AB_ms < 50.0 AND rPT_H2_Header_Disc_CA_ms < 50.0 THEN
        bPT_H2_Header_HealthA := TRUE;
    END_IF;
    IF rPT_H2_Header_3B_bar >= -0.10 AND rPT_H2_Header_3B_bar <= 1.50 AND rPT_H2_Header_Disc_AB_ms < 50.0 AND rPT_H2_Header_Disc_BC_ms < 50.0 THEN
        bPT_H2_Header_HealthB := TRUE;
    END_IF;
    IF rPT_H2_Header_3C_bar >= -0.10 AND rPT_H2_Header_3C_bar <= 1.50 AND rPT_H2_Header_Disc_BC_ms < 50.0 AND rPT_H2_Header_Disc_CA_ms < 50.0 THEN
        bPT_H2_Header_HealthC := TRUE;
    END_IF;
END_IF;

IF bPT_H2_Header_HealthA AND bPT_H2_Header_HealthB AND bPT_H2_Header_HealthC THEN
    IF (rPT_H2_Header_3A_bar >= rPT_H2_Header_3B_bar AND rPT_H2_Header_3A_bar <= rPT_H2_Header_3C_bar) OR
       (rPT_H2_Header_3A_bar >= rPT_H2_Header_3C_bar AND rPT_H2_Header_3A_bar <= rPT_H2_Header_3B_bar) THEN
        rPT_H2_Header_Voted := rPT_H2_Header_3A_bar;
    ELSIF (rPT_H2_Header_3B_bar >= rPT_H2_Header_3A_bar AND rPT_H2_Header_3B_bar <= rPT_H2_Header_3C_bar) OR
          (rPT_H2_Header_3B_bar >= rPT_H2_Header_3C_bar AND rPT_H2_Header_3B_bar <= rPT_H2_Header_3A_bar) THEN
        rPT_H2_Header_Voted := rPT_H2_Header_3B_bar;
    ELSE
        rPT_H2_Header_Voted := rPT_H2_Header_3C_bar;
    END_IF;
    bPT_H2_Header_Degraded := FALSE;
    bPT_H2_Header_SingleFallback := FALSE;
    bPT_H2_Header_Trip := FALSE;
ELSIF (bPT_H2_Header_HealthA AND bPT_H2_Header_HealthB) OR
      (bPT_H2_Header_HealthB AND bPT_H2_Header_HealthC) OR
      (bPT_H2_Header_HealthC AND bPT_H2_Header_HealthA) THEN
    IF bPT_H2_Header_HealthA AND bPT_H2_Header_HealthB THEN
        rPT_H2_Header_Voted := (rPT_H2_Header_3A_bar + rPT_H2_Header_3B_bar) * 0.50;
    ELSIF bPT_H2_Header_HealthB AND bPT_H2_Header_HealthC THEN
        rPT_H2_Header_Voted := (rPT_H2_Header_3B_bar + rPT_H2_Header_3C_bar) * 0.50;
    ELSE
        rPT_H2_Header_Voted := (rPT_H2_Header_3C_bar + rPT_H2_Header_3A_bar) * 0.50;
    END_IF;
    bPT_H2_Header_Degraded := TRUE;
    bPT_H2_Header_SingleFallback := FALSE;
    bPT_H2_Header_Trip := FALSE;
ELSIF bPT_H2_Header_HealthA OR bPT_H2_Header_HealthB OR bPT_H2_Header_HealthC THEN
    IF bPT_H2_Header_HealthA THEN
        rPT_H2_Header_Voted := rPT_H2_Header_3A_bar;
    ELSIF bPT_H2_Header_HealthB THEN
        rPT_H2_Header_Voted := rPT_H2_Header_3B_bar;
    ELSE
        rPT_H2_Header_Voted := rPT_H2_Header_3C_bar;
    END_IF;
    bPT_H2_Header_Degraded := TRUE;
    bPT_H2_Header_SingleFallback := TRUE;
    bPT_H2_Header_Trip := FALSE;
ELSE
    bPT_H2_Header_Degraded := TRUE;
    bPT_H2_Header_SingleFallback := TRUE;
    bPT_H2_Header_Trip := TRUE;
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* Channel Group 4: Inline Hydrogen-in-Chlorine Gas Photometer Analyzers [% vol]                        *)
(* Safety Critical Detonation Threshold: 1.20 % vol; Nominal Baseline: < 0.20 % vol                     *)
(* ---------------------------------------------------------------------------------------------------- *)
IF rAT_H2_in_Cl2_4A_pct < 0.0 OR rAT_H2_in_Cl2_4A_pct > 5.00 THEN
    bAT_H2_in_Cl2_HealthA := FALSE;
END_IF;
IF rAT_H2_in_Cl2_4B_pct < 0.0 OR rAT_H2_in_Cl2_4B_pct > 5.00 THEN
    bAT_H2_in_Cl2_HealthB := FALSE;
END_IF;
IF rAT_H2_in_Cl2_4C_pct < 0.0 OR rAT_H2_in_Cl2_4C_pct > 5.00 THEN
    bAT_H2_in_Cl2_HealthC := FALSE;
END_IF;

IF ABS(rAT_H2_in_Cl2_4A_pct - rAT_H2_in_Cl2_4B_pct) > 0.15 THEN
    rAT_H2_in_Cl2_Disc_AB_ms := rAT_H2_in_Cl2_Disc_AB_ms + (tScanCycleTime_s * 1000.0);
ELSE
    rAT_H2_in_Cl2_Disc_AB_ms := MAX(0.0, rAT_H2_in_Cl2_Disc_AB_ms - (tScanCycleTime_s * 500.0));
END_IF;

IF ABS(rAT_H2_in_Cl2_4B_pct - rAT_H2_in_Cl2_4C_pct) > 0.15 THEN
    rAT_H2_in_Cl2_Disc_BC_ms := rAT_H2_in_Cl2_Disc_BC_ms + (tScanCycleTime_s * 1000.0);
ELSE
    rAT_H2_in_Cl2_Disc_BC_ms := MAX(0.0, rAT_H2_in_Cl2_Disc_BC_ms - (tScanCycleTime_s * 500.0));
END_IF;

IF ABS(rAT_H2_in_Cl2_4C_pct - rAT_H2_in_Cl2_4A_pct) > 0.15 THEN
    rAT_H2_in_Cl2_Disc_CA_ms := rAT_H2_in_Cl2_Disc_CA_ms + (tScanCycleTime_s * 1000.0);
ELSE
    rAT_H2_in_Cl2_Disc_CA_ms := MAX(0.0, rAT_H2_in_Cl2_Disc_CA_ms - (tScanCycleTime_s * 500.0));
END_IF;

IF rAT_H2_in_Cl2_Disc_AB_ms > 250.0 AND rAT_H2_in_Cl2_Disc_CA_ms > 250.0 THEN
    bAT_H2_in_Cl2_HealthA := FALSE;
END_IF;
IF rAT_H2_in_Cl2_Disc_AB_ms > 250.0 AND rAT_H2_in_Cl2_Disc_BC_ms > 250.0 THEN
    bAT_H2_in_Cl2_HealthB := FALSE;
END_IF;
IF rAT_H2_in_Cl2_Disc_BC_ms > 250.0 AND rAT_H2_in_Cl2_Disc_CA_ms > 250.0 THEN
    bAT_H2_in_Cl2_HealthC := FALSE;
END_IF;

IF bFaultReset THEN
    IF rAT_H2_in_Cl2_4A_pct >= 0.0 AND rAT_H2_in_Cl2_4A_pct <= 5.00 AND rAT_H2_in_Cl2_Disc_AB_ms < 50.0 AND rAT_H2_in_Cl2_Disc_CA_ms < 50.0 THEN
        bAT_H2_in_Cl2_HealthA := TRUE;
    END_IF;
    IF rAT_H2_in_Cl2_4B_pct >= 0.0 AND rAT_H2_in_Cl2_4B_pct <= 5.00 AND rAT_H2_in_Cl2_Disc_AB_ms < 50.0 AND rAT_H2_in_Cl2_Disc_BC_ms < 50.0 THEN
        bAT_H2_in_Cl2_HealthB := TRUE;
    END_IF;
    IF rAT_H2_in_Cl2_4C_pct >= 0.0 AND rAT_H2_in_Cl2_4C_pct <= 5.00 AND rAT_H2_in_Cl2_Disc_BC_ms < 50.0 AND rAT_H2_in_Cl2_Disc_CA_ms < 50.0 THEN
        bAT_H2_in_Cl2_HealthC := TRUE;
    END_IF;
END_IF;

IF bAT_H2_in_Cl2_HealthA AND bAT_H2_in_Cl2_HealthB AND bAT_H2_in_Cl2_HealthC THEN
    (* 3 Healthy: High-Purity Median Selection *)
    IF (rAT_H2_in_Cl2_4A_pct >= rAT_H2_in_Cl2_4B_pct AND rAT_H2_in_Cl2_4A_pct <= rAT_H2_in_Cl2_4C_pct) OR
       (rAT_H2_in_Cl2_4A_pct >= rAT_H2_in_Cl2_4C_pct AND rAT_H2_in_Cl2_4A_pct <= rAT_H2_in_Cl2_4B_pct) THEN
        rAT_H2_in_Cl2_Voted := rAT_H2_in_Cl2_4A_pct;
    ELSIF (rAT_H2_in_Cl2_4B_pct >= rAT_H2_in_Cl2_4A_pct AND rAT_H2_in_Cl2_4B_pct <= rAT_H2_in_Cl2_4C_pct) OR
          (rAT_H2_in_Cl2_4B_pct >= rAT_H2_in_Cl2_4C_pct AND rAT_H2_in_Cl2_4B_pct <= rAT_H2_in_Cl2_4A_pct) THEN
        rAT_H2_in_Cl2_Voted := rAT_H2_in_Cl2_4B_pct;
    ELSE
        rAT_H2_in_Cl2_Voted := rAT_H2_in_Cl2_4C_pct;
    END_IF;
    bAT_H2_in_Cl2_Degraded := FALSE;
    bAT_H2_in_Cl2_SingleFallback := FALSE;
    bAT_H2_in_Cl2_Trip := FALSE;
ELSIF (bAT_H2_in_Cl2_HealthA AND bAT_H2_in_Cl2_HealthB) OR
      (bAT_H2_in_Cl2_HealthB AND bAT_H2_in_Cl2_HealthC) OR
      (bAT_H2_in_Cl2_HealthC AND bAT_H2_in_Cl2_HealthA) THEN
    (* 2 Healthy: Conservative High-Select Voting for Safety *)
    IF bAT_H2_in_Cl2_HealthA AND bAT_H2_in_Cl2_HealthB THEN
        rAT_H2_in_Cl2_Voted := MAX(rAT_H2_in_Cl2_4A_pct, rAT_H2_in_Cl2_4B_pct);
    ELSIF bAT_H2_in_Cl2_HealthB AND bAT_H2_in_Cl2_HealthC THEN
        rAT_H2_in_Cl2_Voted := MAX(rAT_H2_in_Cl2_4B_pct, rAT_H2_in_Cl2_4C_pct);
    ELSE
        rAT_H2_in_Cl2_Voted := MAX(rAT_H2_in_Cl2_4C_pct, rAT_H2_in_Cl2_4A_pct);
    END_IF;
    bAT_H2_in_Cl2_Degraded := TRUE;
    bAT_H2_in_Cl2_SingleFallback := FALSE;
    bAT_H2_in_Cl2_Trip := FALSE;
ELSIF bAT_H2_in_Cl2_HealthA OR bAT_H2_in_Cl2_HealthB OR bAT_H2_in_Cl2_HealthC THEN
    IF bAT_H2_in_Cl2_HealthA THEN
        rAT_H2_in_Cl2_Voted := rAT_H2_in_Cl2_4A_pct;
    ELSIF bAT_H2_in_Cl2_HealthB THEN
        rAT_H2_in_Cl2_Voted := rAT_H2_in_Cl2_4B_pct;
    ELSE
        rAT_H2_in_Cl2_Voted := rAT_H2_in_Cl2_4C_pct;
    END_IF;
    bAT_H2_in_Cl2_Degraded := TRUE;
    bAT_H2_in_Cl2_SingleFallback := TRUE;
    bAT_H2_in_Cl2_Trip := FALSE;
ELSE
    bAT_H2_in_Cl2_Degraded := TRUE;
    bAT_H2_in_Cl2_SingleFallback := TRUE;
    bAT_H2_in_Cl2_Trip := TRUE;
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* Channel Group 5: Anolyte Depleted Brine Concentration Analyzers [g/L]                                *)
(* Nominal Operational Range: 195.0 to 225.0 g/L; Feed Brine: ~305.0 g/L                                 *)
(* ---------------------------------------------------------------------------------------------------- *)
IF rAT_Anolyte_NaCl_5A_gL < 140.0 OR rAT_Anolyte_NaCl_5A_gL > 340.0 THEN
    bAT_Anolyte_NaCl_HealthA := FALSE;
END_IF;
IF rAT_Anolyte_NaCl_5B_gL < 140.0 OR rAT_Anolyte_NaCl_5B_gL > 340.0 THEN
    bAT_Anolyte_NaCl_HealthB := FALSE;
END_IF;
IF rAT_Anolyte_NaCl_5C_gL < 140.0 OR rAT_Anolyte_NaCl_5C_gL > 340.0 THEN
    bAT_Anolyte_NaCl_HealthC := FALSE;
END_IF;

IF ABS(rAT_Anolyte_NaCl_5A_gL - rAT_Anolyte_NaCl_5B_gL) > 8.00 THEN
    rAT_Anolyte_NaCl_Disc_AB_ms := rAT_Anolyte_NaCl_Disc_AB_ms + (tScanCycleTime_s * 1000.0);
ELSE
    rAT_Anolyte_NaCl_Disc_AB_ms := MAX(0.0, rAT_Anolyte_NaCl_Disc_AB_ms - (tScanCycleTime_s * 500.0));
END_IF;

IF ABS(rAT_Anolyte_NaCl_5B_gL - rAT_Anolyte_NaCl_5C_gL) > 8.00 THEN
    rAT_Anolyte_NaCl_Disc_BC_ms := rAT_Anolyte_NaCl_Disc_BC_ms + (tScanCycleTime_s * 1000.0);
ELSE
    rAT_Anolyte_NaCl_Disc_BC_ms := MAX(0.0, rAT_Anolyte_NaCl_Disc_BC_ms - (tScanCycleTime_s * 500.0));
END_IF;

IF ABS(rAT_Anolyte_NaCl_5C_gL - rAT_Anolyte_NaCl_5A_gL) > 8.00 THEN
    rAT_Anolyte_NaCl_Disc_CA_ms := rAT_Anolyte_NaCl_Disc_CA_ms + (tScanCycleTime_s * 1000.0);
ELSE
    rAT_Anolyte_NaCl_Disc_CA_ms := MAX(0.0, rAT_Anolyte_NaCl_Disc_CA_ms - (tScanCycleTime_s * 500.0));
END_IF;

IF rAT_Anolyte_NaCl_Disc_AB_ms > 400.0 AND rAT_Anolyte_NaCl_Disc_CA_ms > 400.0 THEN
    bAT_Anolyte_NaCl_HealthA := FALSE;
END_IF;
IF rAT_Anolyte_NaCl_Disc_AB_ms > 400.0 AND rAT_Anolyte_NaCl_Disc_BC_ms > 400.0 THEN
    bAT_Anolyte_NaCl_HealthB := FALSE;
END_IF;
IF rAT_Anolyte_NaCl_Disc_BC_ms > 400.0 AND rAT_Anolyte_NaCl_Disc_CA_ms > 400.0 THEN
    bAT_Anolyte_NaCl_HealthC := FALSE;
END_IF;

IF bFaultReset THEN
    IF rAT_Anolyte_NaCl_5A_gL >= 140.0 AND rAT_Anolyte_NaCl_5A_gL <= 340.0 AND rAT_Anolyte_NaCl_Disc_AB_ms < 50.0 AND rAT_Anolyte_NaCl_Disc_CA_ms < 50.0 THEN
        bAT_Anolyte_NaCl_HealthA := TRUE;
    END_IF;
    IF rAT_Anolyte_NaCl_5B_gL >= 140.0 AND rAT_Anolyte_NaCl_5B_gL <= 340.0 AND rAT_Anolyte_NaCl_Disc_AB_ms < 50.0 AND rAT_Anolyte_NaCl_Disc_BC_ms < 50.0 THEN
        bAT_Anolyte_NaCl_HealthB := TRUE;
    END_IF;
    IF rAT_Anolyte_NaCl_5C_gL >= 140.0 AND rAT_Anolyte_NaCl_5C_gL <= 340.0 AND rAT_Anolyte_NaCl_Disc_BC_ms < 50.0 AND rAT_Anolyte_NaCl_Disc_CA_ms < 50.0 THEN
        bAT_Anolyte_NaCl_HealthC := TRUE;
    END_IF;
END_IF;

IF bAT_Anolyte_NaCl_HealthA AND bAT_Anolyte_NaCl_HealthB AND bAT_Anolyte_NaCl_HealthC THEN
    IF (rAT_Anolyte_NaCl_5A_gL >= rAT_Anolyte_NaCl_5B_gL AND rAT_Anolyte_NaCl_5A_gL <= rAT_Anolyte_NaCl_5C_gL) OR
       (rAT_Anolyte_NaCl_5A_gL >= rAT_Anolyte_NaCl_5C_gL AND rAT_Anolyte_NaCl_5A_gL <= rAT_Anolyte_NaCl_5B_gL) THEN
        rAT_Anolyte_NaCl_Voted := rAT_Anolyte_NaCl_5A_gL;
    ELSIF (rAT_Anolyte_NaCl_5B_gL >= rAT_Anolyte_NaCl_5A_gL AND rAT_Anolyte_NaCl_5B_gL <= rAT_Anolyte_NaCl_5C_gL) OR
          (rAT_Anolyte_NaCl_5B_gL >= rAT_Anolyte_NaCl_5C_gL AND rAT_Anolyte_NaCl_5B_gL <= rAT_Anolyte_NaCl_5A_gL) THEN
        rAT_Anolyte_NaCl_Voted := rAT_Anolyte_NaCl_5B_gL;
    ELSE
        rAT_Anolyte_NaCl_Voted := rAT_Anolyte_NaCl_5C_gL;
    END_IF;
    bAT_Anolyte_NaCl_Degraded := FALSE;
    bAT_Anolyte_NaCl_SingleFallback := FALSE;
    bAT_Anolyte_NaCl_Trip := FALSE;
ELSIF (bAT_Anolyte_NaCl_HealthA AND bAT_Anolyte_NaCl_HealthB) OR
      (bAT_Anolyte_NaCl_HealthB AND bAT_Anolyte_NaCl_HealthC) OR
      (bAT_Anolyte_NaCl_HealthC AND bAT_Anolyte_NaCl_HealthA) THEN
    IF bAT_Anolyte_NaCl_HealthA AND bAT_Anolyte_NaCl_HealthB THEN
        rAT_Anolyte_NaCl_Voted := (rAT_Anolyte_NaCl_5A_gL + rAT_Anolyte_NaCl_5B_gL) * 0.50;
    ELSIF bAT_Anolyte_NaCl_HealthB AND bAT_Anolyte_NaCl_HealthC THEN
        rAT_Anolyte_NaCl_Voted := (rAT_Anolyte_NaCl_5B_gL + rAT_Anolyte_NaCl_5C_gL) * 0.50;
    ELSE
        rAT_Anolyte_NaCl_Voted := (rAT_Anolyte_NaCl_5C_gL + rAT_Anolyte_NaCl_5A_gL) * 0.50;
    END_IF;
    bAT_Anolyte_NaCl_Degraded := TRUE;
    bAT_Anolyte_NaCl_SingleFallback := FALSE;
    bAT_Anolyte_NaCl_Trip := FALSE;
ELSIF bAT_Anolyte_NaCl_HealthA OR bAT_Anolyte_NaCl_HealthB OR bAT_Anolyte_NaCl_HealthC THEN
    IF bAT_Anolyte_NaCl_HealthA THEN
        rAT_Anolyte_NaCl_Voted := rAT_Anolyte_NaCl_5A_gL;
    ELSIF bAT_Anolyte_NaCl_HealthB THEN
        rAT_Anolyte_NaCl_Voted := rAT_Anolyte_NaCl_5B_gL;
    ELSE
        rAT_Anolyte_NaCl_Voted := rAT_Anolyte_NaCl_5C_gL;
    END_IF;
    bAT_Anolyte_NaCl_Degraded := TRUE;
    bAT_Anolyte_NaCl_SingleFallback := TRUE;
    bAT_Anolyte_NaCl_Trip := FALSE;
ELSE
    bAT_Anolyte_NaCl_Degraded := TRUE;
    bAT_Anolyte_NaCl_SingleFallback := TRUE;
    bAT_Anolyte_NaCl_Trip := TRUE;
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* Channel Group 6: Catholyte Caustic Soda Concentration Analyzers [wt%]                                *)
(* Nominal Commercial Target: 32.0 to 35.0 wt% NaOH; High-Viscosity Crystallization Hazard: > 36.0 wt%    *)
(* ---------------------------------------------------------------------------------------------------- *)
IF rAT_Catholyte_NaOH_6A_pct < 20.0 OR rAT_Catholyte_NaOH_6A_pct > 50.0 THEN
    bAT_Catholyte_NaOH_HealthA := FALSE;
END_IF;
IF rAT_Catholyte_NaOH_6B_pct < 20.0 OR rAT_Catholyte_NaOH_6B_pct > 50.0 THEN
    bAT_Catholyte_NaOH_HealthB := FALSE;
END_IF;
IF rAT_Catholyte_NaOH_6C_pct < 20.0 OR rAT_Catholyte_NaOH_6C_pct > 50.0 THEN
    bAT_Catholyte_NaOH_HealthC := FALSE;
END_IF;

IF ABS(rAT_Catholyte_NaOH_6A_pct - rAT_Catholyte_NaOH_6B_pct) > 0.75 THEN
    rAT_Catholyte_NaOH_Disc_AB_ms := rAT_Catholyte_NaOH_Disc_AB_ms + (tScanCycleTime_s * 1000.0);
ELSE
    rAT_Catholyte_NaOH_Disc_AB_ms := MAX(0.0, rAT_Catholyte_NaOH_Disc_AB_ms - (tScanCycleTime_s * 500.0));
END_IF;

IF ABS(rAT_Catholyte_NaOH_6B_pct - rAT_Catholyte_NaOH_6C_pct) > 0.75 THEN
    rAT_Catholyte_NaOH_Disc_BC_ms := rAT_Catholyte_NaOH_Disc_BC_ms + (tScanCycleTime_s * 1000.0);
ELSE
    rAT_Catholyte_NaOH_Disc_BC_ms := MAX(0.0, rAT_Catholyte_NaOH_Disc_BC_ms - (tScanCycleTime_s * 500.0));
END_IF;

IF ABS(rAT_Catholyte_NaOH_6C_pct - rAT_Catholyte_NaOH_6A_pct) > 0.75 THEN
    rAT_Catholyte_NaOH_Disc_CA_ms := rAT_Catholyte_NaOH_Disc_CA_ms + (tScanCycleTime_s * 1000.0);
ELSE
    rAT_Catholyte_NaOH_Disc_CA_ms := MAX(0.0, rAT_Catholyte_NaOH_Disc_CA_ms - (tScanCycleTime_s * 500.0));
END_IF;

IF rAT_Catholyte_NaOH_Disc_AB_ms > 400.0 AND rAT_Catholyte_NaOH_Disc_CA_ms > 400.0 THEN
    bAT_Catholyte_NaOH_HealthA := FALSE;
END_IF;
IF rAT_Catholyte_NaOH_Disc_AB_ms > 400.0 AND rAT_Catholyte_NaOH_Disc_BC_ms > 400.0 THEN
    bAT_Catholyte_NaOH_HealthB := FALSE;
END_IF;
IF rAT_Catholyte_NaOH_Disc_BC_ms > 400.0 AND rAT_Catholyte_NaOH_Disc_CA_ms > 400.0 THEN
    bAT_Catholyte_NaOH_HealthC := FALSE;
END_IF;

IF bFaultReset THEN
    IF rAT_Catholyte_NaOH_6A_pct >= 20.0 AND rAT_Catholyte_NaOH_6A_pct <= 50.0 AND rAT_Catholyte_NaOH_Disc_AB_ms < 50.0 AND rAT_Catholyte_NaOH_Disc_CA_ms < 50.0 THEN
        bAT_Catholyte_NaOH_HealthA := TRUE;
    END_IF;
    IF rAT_Catholyte_NaOH_6B_pct >= 20.0 AND rAT_Catholyte_NaOH_6B_pct <= 50.0 AND rAT_Catholyte_NaOH_Disc_AB_ms < 50.0 AND rAT_Catholyte_NaOH_Disc_BC_ms < 50.0 THEN
        bAT_Catholyte_NaOH_HealthB := TRUE;
    END_IF;
    IF rAT_Catholyte_NaOH_6C_pct >= 20.0 AND rAT_Catholyte_NaOH_6C_pct <= 50.0 AND rAT_Catholyte_NaOH_Disc_BC_ms < 50.0 AND rAT_Catholyte_NaOH_Disc_CA_ms < 50.0 THEN
        bAT_Catholyte_NaOH_HealthC := TRUE;
    END_IF;
END_IF;

IF bAT_Catholyte_NaOH_HealthA AND bAT_Catholyte_NaOH_HealthB AND bAT_Catholyte_NaOH_HealthC THEN
    IF (rAT_Catholyte_NaOH_6A_pct >= rAT_Catholyte_NaOH_6B_pct AND rAT_Catholyte_NaOH_6A_pct <= rAT_Catholyte_NaOH_6C_pct) OR
       (rAT_Catholyte_NaOH_6A_pct >= rAT_Catholyte_NaOH_6C_pct AND rAT_Catholyte_NaOH_6A_pct <= rAT_Catholyte_NaOH_6B_pct) THEN
        rAT_Catholyte_NaOH_Voted := rAT_Catholyte_NaOH_6A_pct;
    ELSIF (rAT_Catholyte_NaOH_6B_pct >= rAT_Catholyte_NaOH_6A_pct AND rAT_Catholyte_NaOH_6B_pct <= rAT_Catholyte_NaOH_6C_pct) OR
          (rAT_Catholyte_NaOH_6B_pct >= rAT_Catholyte_NaOH_6C_pct AND rAT_Catholyte_NaOH_6B_pct <= rAT_Catholyte_NaOH_6A_pct) THEN
        rAT_Catholyte_NaOH_Voted := rAT_Catholyte_NaOH_6B_pct;
    ELSE
        rAT_Catholyte_NaOH_Voted := rAT_Catholyte_NaOH_6C_pct;
    END_IF;
    bAT_Catholyte_NaOH_Degraded := FALSE;
    bAT_Catholyte_NaOH_SingleFallback := FALSE;
    bAT_Catholyte_NaOH_Trip := FALSE;
ELSIF (bAT_Catholyte_NaOH_HealthA AND bAT_Catholyte_NaOH_HealthB) OR
      (bAT_Catholyte_NaOH_HealthB AND bAT_Catholyte_NaOH_HealthC) OR
      (bAT_Catholyte_NaOH_HealthC AND bAT_Catholyte_NaOH_HealthA) THEN
    IF bAT_Catholyte_NaOH_HealthA AND bAT_Catholyte_NaOH_HealthB THEN
        rAT_Catholyte_NaOH_Voted := (rAT_Catholyte_NaOH_6A_pct + rAT_Catholyte_NaOH_6B_pct) * 0.50;
    ELSIF bAT_Catholyte_NaOH_HealthB AND bAT_Catholyte_NaOH_HealthC THEN
        rAT_Catholyte_NaOH_Voted := (rAT_Catholyte_NaOH_6B_pct + rAT_Catholyte_NaOH_6C_pct) * 0.50;
    ELSE
        rAT_Catholyte_NaOH_Voted := (rAT_Catholyte_NaOH_6C_pct + rAT_Catholyte_NaOH_6A_pct) * 0.50;
    END_IF;
    bAT_Catholyte_NaOH_Degraded := TRUE;
    bAT_Catholyte_NaOH_SingleFallback := FALSE;
    bAT_Catholyte_NaOH_Trip := FALSE;
ELSIF bAT_Catholyte_NaOH_HealthA OR bAT_Catholyte_NaOH_HealthB OR bAT_Catholyte_NaOH_HealthC THEN
    IF bAT_Catholyte_NaOH_HealthA THEN
        rAT_Catholyte_NaOH_Voted := rAT_Catholyte_NaOH_6A_pct;
    ELSIF bAT_Catholyte_NaOH_HealthB THEN
        rAT_Catholyte_NaOH_Voted := rAT_Catholyte_NaOH_6B_pct;
    ELSE
        rAT_Catholyte_NaOH_Voted := rAT_Catholyte_NaOH_6C_pct;
    END_IF;
    bAT_Catholyte_NaOH_Degraded := TRUE;
    bAT_Catholyte_NaOH_SingleFallback := TRUE;
    bAT_Catholyte_NaOH_Trip := FALSE;
ELSE
    bAT_Catholyte_NaOH_Degraded := TRUE;
    bAT_Catholyte_NaOH_SingleFallback := TRUE;
    bAT_Catholyte_NaOH_Trip := TRUE;
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* Assemble Voted Measurements into Observer Cyber-Physical Input Vector Y_meas                         *)
(* ---------------------------------------------------------------------------------------------------- *)
vecY_meas[0] := rPDT_Cell_DP_Voted;
vecY_meas[1] := rPT_Cl2_Header_Voted;
vecY_meas[2] := rPT_H2_Header_Voted;
vecY_meas[3] := rAT_Anolyte_NaCl_Voted;
vecY_meas[4] := rAT_Catholyte_NaOH_Voted;
vecY_meas[5] := rCell_Temperature_degC;

(* ==================================================================================================== *)
(* PHASE 2: FIRST-PRINCIPLES CYBER-PHYSICAL STATE-SPACE ESTIMATION & ELECTROCHEMICAL KINETICS           *)
(* Architecture: Luenberger Observer (Prediction -> Measurement -> Innovation -> Filtered Estimate)     *)
(* Electrochemical Kinetics: Faraday Production, Nernst Reversible Potential, Butler-Volmer/Tafel,     *)
(*                           Membrane Area Resistance, Specific Energy & Thermal Balance                *)
(* ==================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------- *)
(* Step 1: One-Step-Ahead Cyber-Physical State Prediction (x_pred = A * x_hat + B * u)                  *)
(* ---------------------------------------------------------------------------------------------------- *)
FOR iIdx := 0 TO 5 DO
    rTempSum := 0.0;
    FOR jIdx := 0 TO 5 DO
        rTempSum := rTempSum + (matA[iIdx, jIdx] * vecX_hat[jIdx]);
    END_FOR;
    FOR mIdx := 0 TO 4 DO
        rTempSum := rTempSum + (matB[iIdx, mIdx] * vecU[mIdx]);
    END_FOR;
    vecX_pred[iIdx] := rTempSum;
END_FOR;

(* ---------------------------------------------------------------------------------------------------- *)
(* Step 2: Predicted Measurement Projection (y_hat = C * x_pred + D * u)                                *)
(* ---------------------------------------------------------------------------------------------------- *)
FOR iIdx := 0 TO 5 DO
    rTempSum := 0.0;
    FOR jIdx := 0 TO 5 DO
        rTempSum := rTempSum + (matC[iIdx, jIdx] * vecX_pred[jIdx]);
    END_FOR;
    FOR mIdx := 0 TO 4 DO
        rTempSum := rTempSum + (matD[iIdx, mIdx] * vecU[mIdx]);
    END_FOR;
    vecY_hat[iIdx] := rTempSum;
END_FOR;

(* ---------------------------------------------------------------------------------------------------- *)
(* Step 3: Innovation Residual Vector Computation (vecInnov = vecY_meas - vecY_hat)                    *)
(* ---------------------------------------------------------------------------------------------------- *)
FOR iIdx := 0 TO 5 DO
    vecInnov[iIdx] := vecY_meas[iIdx] - vecY_hat[iIdx];
END_FOR;

(* ---------------------------------------------------------------------------------------------------- *)
(* Step 4: Luenberger Innovation Correction Update (x_hat = x_pred + L * innov)                         *)
(* ---------------------------------------------------------------------------------------------------- *)
FOR iIdx := 0 TO 5 DO
    rTempSum := 0.0;
    FOR jIdx := 0 TO 5 DO
        rTempSum := rTempSum + (matL[iIdx, jIdx] * vecInnov[jIdx]);
    END_FOR;
    vecX_hat[iIdx] := vecX_pred[iIdx] + rTempSum;
END_FOR;

(* Assign Filtered Estimates to Dedicated Physical Telemetry Outputs *)
rEst_Cell_DP_mbar          := vecX_hat[0];
rEst_P_Cl2_bar             := vecX_hat[1];
rEst_P_H2_bar              := vecX_hat[2];
rEst_Anolyte_NaCl_gL       := vecX_hat[3];
rEst_Catholyte_NaOH_pct    := vecX_hat[4];
rEst_Cell_Temperature_degC := vecX_hat[5];

(* ---------------------------------------------------------------------------------------------------- *)
(* Step 5: Advanced Electrochemical Reaction Kinetics & Real-Time Performance Analytics                 *)
(* ---------------------------------------------------------------------------------------------------- *)
(* 1. Operating Current Density J [kA/m2] across Active Membrane Area *)
IF rTotalActiveMembraneArea_m2 > 1.0 THEN
    rCalc_CurrentDensity_kAm2 := (rRectifier_CurrentFb_kA * rNumberCellsInBipolarStack) / rTotalActiveMembraneArea_m2;
ELSE
    rCalc_CurrentDensity_kAm2 := 0.0;
END_IF;

(* 2. Faraday Current Efficiency Model (Sensitive to Caustic Concentration & Electrolyte Temp) *)
rFaradayCurrentEfficiency := 0.9850 - (0.0035 * ABS(rEst_Catholyte_NaOH_pct - 32.5)) - (0.00045 * MAX(0.0, rEst_Cell_Temperature_degC - 85.0));
IF rFaradayCurrentEfficiency > 0.9850 THEN
    rFaradayCurrentEfficiency := 0.9850;
ELSIF rFaradayCurrentEfficiency < 0.8800 THEN
    rFaradayCurrentEfficiency := 0.8800;
END_IF;
rCalc_FaradayEfficiency_pct := rFaradayCurrentEfficiency * 100.0;

(* 3. Faraday Law Gas Production Rates: Chlorine Cl2 and Hydrogen H2 in Standard [Nm3/h] *)
(* n_mols/s = (I * N_cells * eta) / (z * F), where z = 2 electrons per molecule *)
rTempGasMols := (rRectifier_CurrentFb_kA * 1000.0 * rNumberCellsInBipolarStack * rFaradayCurrentEfficiency) / (2.0 * rFaradayConst_C_mol);
rCalc_Cl2_ProductionRate_Nm3h := rTempGasMols * 3600.0 * (rMolarVol_Nm3_kmol / 1000.0);
rCalc_H2_ProductionRate_Nm3h  := rCalc_Cl2_ProductionRate_Nm3h;

(* 4. 100% Equivalent Caustic Soda (NaOH) Production Rate in [kg/h] (z = 1 electron per NaOH) *)
rCalc_NaOH_ProductionRate_kgh := (rRectifier_CurrentFb_kA * 1000.0 * rNumberCellsInBipolarStack * rFaradayCurrentEfficiency / rFaradayConst_C_mol) * 3600.0 * (rMolarMass_NaOH_kg_kmol / 1000.0);

(* 5. Reversible Nernst Potential E_rev [V] as function of Bulk Temperature & Activities *)
rNernstPotential_V := rStandardElectrodePotential_V - (0.00085 * (rEst_Cell_Temperature_degC - 25.0)) +
                      (((rGasConst_J_molK * (rEst_Cell_Temperature_degC + 273.15)) / (2.0 * rFaradayConst_C_mol)) * 0.045);

(* 6. Anode Kinetic Overpotential (RuO2-TiO2 DSA Coating Tafel Equation) *)
IF rCalc_CurrentDensity_kAm2 > 0.01 THEN
    rAnodeOverpotential_V := 0.042 + (0.032 * (rCalc_CurrentDensity_kAm2 / 2.50));
ELSE
    rAnodeOverpotential_V := 0.005;
END_IF;

(* 7. Cathode Kinetic Overpotential (Nickel Mesh Cathode Tafel Equation) *)
IF rCalc_CurrentDensity_kAm2 > 0.01 THEN
    rCathodeOverpotential_V := 0.065 + (0.048 * (rCalc_CurrentDensity_kAm2 / 2.50));
ELSE
    rCathodeOverpotential_V := 0.010;
END_IF;

(* 8. Membrane Specific Ohmic Resistance [mOhm.cm2] with Arrhenius Temperature Correction *)
(* Nafion/Flemion Perfluorosulfonic Carboxylic Bilayer Area Resistance *)
rCalc_MembraneAreaResist_mOhm := 210.0 * (1.0 + (0.045 * (rEst_Catholyte_NaOH_pct - 32.0))) *
                                 (1.0 - (0.011 * (rEst_Cell_Temperature_degC - 85.0)));
IF rCalc_MembraneAreaResist_mOhm < 120.0 THEN
    rCalc_MembraneAreaResist_mOhm := 120.0;
ELSIF rCalc_MembraneAreaResist_mOhm > 450.0 THEN
    rCalc_MembraneAreaResist_mOhm := 450.0;
END_IF;

(* Membrane IR Voltage Drop [V] *)
rMembraneOhmicDrop_V := (rCalc_CurrentDensity_kAm2 * 1000.0 / 10000.0) * (rCalc_MembraneAreaResist_mOhm / 1000.0);

(* 9. Electrolyte Brine & Caustic Solution IR Voltage Drop [V] *)
rElectrolyteOhmicDrop_V := (rCalc_CurrentDensity_kAm2 * 0.055) * (1.0 + (0.002 * MAX(0.0, 220.0 - rEst_Anolyte_NaCl_gL)));

(* 10. Theoretical Sum of Cell Voltage & Discrepancy Diagnostics *)
rTheoreticalCellVoltage_V := rNernstPotential_V + rAnodeOverpotential_V + rCathodeOverpotential_V +
                             rMembraneOhmicDrop_V + rElectrolyteOhmicDrop_V + 0.075;
rCellVoltageDeviation_V   := rCell_AverageVoltage_V - rTheoreticalCellVoltage_V;

(* 11. Specific DC Electrical Energy Consumption [kWh / Metric Ton Cl2] *)
IF rCalc_Cl2_ProductionRate_Nm3h > 0.1 AND rFaradayCurrentEfficiency > 0.50 THEN
    rCalc_SpecificPower_kWh_tCl2 := (rCell_AverageVoltage_V * 2.0 * rFaradayConst_C_mol) /
                                    (rFaradayCurrentEfficiency * rMolarMass_Cl2_kg_kmol * 3.60);
ELSE
    rCalc_SpecificPower_kWh_tCl2 := 0.0;
END_IF;

(* 12. Cell Stack Thermal Dissipation & Required Heat Exchanger Duty [kW] *)
(* Thermoneutral potential E_th = 1.48 V. Heat gen = I * (V_cell - 1.48) * N_cells *)
IF rRectifier_CurrentFb_kA > 0.5 THEN
    rCalc_ThermalHeatGen_kW := rRectifier_CurrentFb_kA * MAX(0.0, rCell_AverageVoltage_V - 1.480) * rNumberCellsInBipolarStack;
    (* Cooling requirement to maintain setpoint temperature *)
    rCalc_CoolingRequirement_kW := MAX(0.0, rCalc_ThermalHeatGen_kW - (0.45 * (rEst_Cell_Temperature_degC - 25.0)));
ELSE
    rCalc_ThermalHeatGen_kW     := 0.0;
    rCalc_CoolingRequirement_kW := 0.0;
END_IF;

(* ==================================================================================================== *)
(* PHASE 3: RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) WITH PROJECTED GRADIENT DESCENT (PGD)       *)
(* Configuration: Horizon N = 5 Steps (100 [ms]), 10 Unrolled PGD Iterations, Slew & Physical Bounds    *)
(* Actuators: u[0]=CV_H2 [%], u[1]=CV_Cl2 [%], u[2]=CV_Water [%], u[3]=CV_Brine [%], u[4]=I_rect [kA]     *)
(* Adjoint Sensitivity Backpropagation: Costates lambda[k] & Analytical Gradient w.r.t Control Action   *)
(* ==================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------- *)
(* Step 1: Dynamic State Trajectory Setpoint Adaptation Based on FSM State & Electrolyzer Regime        *)
(* ---------------------------------------------------------------------------------------------------- *)
IF eState = 1 THEN
    (* State 1: Nitrogen Purge & Leak Check - Depressurized Balanced State *)
    vecX_target[0] := 0.0;     (* Target DP: 0.0 mbar *)
    vecX_target[1] := 0.100;   (* Target Cl2 Purge Pressure: 0.10 bar *)
    vecX_target[2] := 0.100;   (* Target H2 Purge Pressure: 0.10 bar *)
    vecX_target[3] := 305.0;   (* Saturated Inflow Baseline [g/L] *)
    vecX_target[4] := 30.0;    (* Weak Caustic Inventory [wt%] *)
    vecX_target[5] := 25.0;    (* Cold Purge Temperature [deg C] *)
ELSIF eState = 2 THEN
    (* State 2: Brine Warmup Circulation - Elevating Stack Temperature Without Current *)
    vecX_target[0] := 0.0;     (* Balanced Hydraulic Head *)
    vecX_target[1] := 0.020;   (* Open Manifolds *)
    vecX_target[2] := 0.020;   (* Open Manifolds *)
    vecX_target[3] := 300.0;   (* Fresh Brine Saturation [g/L] *)
    vecX_target[4] := 30.5;    (* Caustic [wt%] *)
    vecX_target[5] := 82.0;    (* Pre-Energization Target Temperature [deg C] *)
ELSIF eState = 3 THEN
    (* State 3: Rectifier Polarization Current Initialization (5% Load, 3.5 kA) *)
    vecX_target[0] := 5.0;     (* Establish Positive Differential Pressure [mbar] *)
    vecX_target[1] := 0.080;   (* Initial Cl2 Blanket [bar] *)
    vecX_target[2] := 0.085;   (* Initial H2 Blanket [bar] *)
    vecX_target[3] := 285.0;   (* Slight Depletion [g/L] *)
    vecX_target[4] := 31.0;    (* Caustic Beginning to Form [wt%] *)
    vecX_target[5] := 84.0;    (* Warm Electrolyte [deg C] *)
ELSIF eState = 4 THEN
    (* State 4: Ramp Current to 25% Low Load (~17.5 kA) *)
    vecX_target[0] := 18.0;    (* Transitional Differential Pressure [mbar] *)
    vecX_target[1] := 0.160;   (* Cl2 Header Pressure [bar] *)
    vecX_target[2] := 0.178;   (* H2 Header Pressure [bar] *)
    vecX_target[3] := 240.0;   (* Depleted Brine Transition [g/L] *)
    vecX_target[4] := 32.0;    (* Caustic Product [wt%] *)
    vecX_target[5] := 86.0;    (* Approaching Operating Temp [deg C] *)
ELSIF eState = 5 THEN
    (* State 5: Pressure Equilibration Transition - Locking Tight +/- 1.5 mbar DP *)
    vecX_target[0] := 30.0;    (* Nominal Baseload DP Setpoint [mbar] *)
    vecX_target[1] := 0.220;   (* Cl2 Header Pressure [bar] *)
    vecX_target[2] := 0.250;   (* H2 Header Pressure [bar] *)
    vecX_target[3] := 215.0;   (* Depleted Brine [g/L] *)
    vecX_target[4] := 32.2;    (* Caustic [wt%] *)
    vecX_target[5] := 87.5;    (* Near Steady State [deg C] *)
ELSIF eState = 6 THEN
    (* State 6: Nominal Baseload Production (Full Load, 2.5 kA/m2, 67.5 kA) *)
    vecX_target[0] := 30.0;    (* Strict DP Setpoint: 30.0 mbar *)
    vecX_target[1] := 0.250;   (* Cl2 Header Steady Pressure: 0.250 bar *)
    vecX_target[2] := 0.280;   (* H2 Header Steady Pressure: 0.280 bar *)
    vecX_target[3] := 205.0;   (* Optimal Anolyte Outlet Brine: 205.0 g/L *)
    vecX_target[4] := 32.5;    (* Commercial High-Purity Caustic: 32.5 wt% *)
    vecX_target[5] := 88.0;    (* Optimal Cell Thermal Equilibrium: 88.0 deg C *)
ELSIF eState = 7 THEN
    (* State 7: Dedicated Caustic Concentration Control Loop Tuning *)
    vecX_target[0] := 30.0;    (* Maintain Strict DP *)
    vecX_target[1] := 0.250;
    vecX_target[2] := 0.280;
    vecX_target[3] := 205.0;
    vecX_target[4] := 32.5;    (* High Priority Focus on 32.5 wt% NaOH *)
    vecX_target[5] := 88.0;
ELSIF eState = 8 THEN
    (* State 8: Dedicated Brine Depletion Feed Control Loop Tuning *)
    vecX_target[0] := 30.0;
    vecX_target[1] := 0.250;
    vecX_target[2] := 0.280;
    vecX_target[3] := 205.0;   (* High Priority Focus on 205.0 g/L NaCl *)
    vecX_target[4] := 32.5;
    vecX_target[5] := 88.0;
ELSIF eState = 9 THEN
    (* State 9: Membrane Health & Specific Resistance Diagnostic Sweep *)
    vecX_target[0] := 30.0;
    vecX_target[1] := 0.250;
    vecX_target[2] := 0.280;
    vecX_target[3] := 215.0;   (* Slightly Richer Brine to Reduce Membrane IR *)
    vecX_target[4] := 32.0;    (* Optimal Hydration Caustic Concentration *)
    vecX_target[5] := 88.5;    (* Elevated Temp to Lower Membrane Resistance *)
ELSIF eState = 10 THEN
    (* State 10: Controlled Ramp-Down Turndown Sequence *)
    vecX_target[0] := 15.0;    (* Decreasing DP to Match Lower Gas Flow Rates *)
    vecX_target[1] := 0.150;
    vecX_target[2] := 0.165;
    vecX_target[3] := 240.0;
    vecX_target[4] := 31.5;
    vecX_target[5] := 82.0;
ELSIF eState = 11 THEN
    (* State 11: Automated Shutdown Polarization Hold (5% Current, 3.5 kA) *)
    vecX_target[0] := 5.0;
    vecX_target[1] := 0.050;
    vecX_target[2] := 0.055;
    vecX_target[3] := 280.0;
    vecX_target[4] := 30.5;
    vecX_target[5] := 75.0;
ELSIF eState = 12 OR eState = 13 THEN
    (* State 12 & 13: Emergency Trip & Post-Trip Inert Blanket *)
    vecX_target[0] := 0.0;     (* Zero Differential Pressure to Relieve Stress *)
    vecX_target[1] := 0.020;   (* Low Inert Nitrogen Header Pressure *)
    vecX_target[2] := 0.020;   (* Low Inert Nitrogen Header Pressure *)
    vecX_target[3] := 290.0;
    vecX_target[4] := 30.0;
    vecX_target[5] := 50.0;    (* Cooling Stack *)
ELSE
    (* Default Baseline Setpoint *)
    vecX_target[0] := 30.0;
    vecX_target[1] := 0.250;
    vecX_target[2] := 0.280;
    vecX_target[3] := 205.0;
    vecX_target[4] := 32.5;
    vecX_target[5] := 88.0;
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* Step 2: Initialize Receding Horizon Trajectory: State Seed & Actuator Warm Start                     *)
(* ---------------------------------------------------------------------------------------------------- *)
FOR iIdx := 0 TO 5 DO
    trajX_mpc[0, iIdx] := vecX_hat[iIdx];
END_FOR;

FOR kStep := 0 TO 4 DO
    FOR mIdx := 0 TO 4 DO
        trajU_mpc[kStep, mIdx] := vecU[mIdx];
    END_FOR;
END_FOR;

(* ---------------------------------------------------------------------------------------------------- *)
(* Step 3: Unrolled Projected Gradient Descent (PGD) Solver Core (10 Full Unrolled Iterations)          *)
(* Solves Quadratic Program: min 1/2 sum(e^T Q e + u^T R u + du^T R_delta du) + 1/2 e_N^T P e_N         *)
(* ---------------------------------------------------------------------------------------------------- *)
FOR iIter := 0 TO 9 DO
    (* 3a. Forward Simulation Across Receding Horizon Steps k = 0 to 4 *)
    FOR kStep := 0 TO 4 DO
        FOR iIdx := 0 TO 5 DO
            rTempSum := 0.0;
            FOR jIdx := 0 TO 5 DO
                rTempSum := rTempSum + (matA[iIdx, jIdx] * trajX_mpc[kStep, jIdx]);
            END_FOR;
            FOR mIdx := 0 TO 4 DO
                rTempSum := rTempSum + (matB[iIdx, mIdx] * trajU_mpc[kStep, mIdx]);
            END_FOR;
            trajX_mpc[kStep + 1, iIdx] := rTempSum;
        END_FOR;
    END_FOR;

    (* 3b. Evaluate Objective Function Quadratic Cost *)
    rMpc_AccumulatedCost := 0.0;
    FOR kStep := 0 TO 4 DO
        (* State Tracking Cost Term *)
        FOR iIdx := 0 TO 5 DO
            rTempDiff := trajX_mpc[kStep, iIdx] - vecX_target[iIdx];
            rMpc_AccumulatedCost := rMpc_AccumulatedCost + (vecQ_weight[iIdx] * rTempDiff * rTempDiff);
        END_FOR;
        (* Actuator Effort & Slew Rate Cost Terms *)
        FOR mIdx := 0 TO 4 DO
            rTempDiff := trajU_mpc[kStep, mIdx];
            rMpc_AccumulatedCost := rMpc_AccumulatedCost + (vecR_weight[mIdx] * rTempDiff * rTempDiff);
            rTempDeltaU := trajU_mpc[kStep, mIdx] - vecU_prev[mIdx];
            rMpc_AccumulatedCost := rMpc_AccumulatedCost + (vecR_delta_weight[mIdx] * rTempDeltaU * rTempDeltaU);
        END_FOR;
    END_FOR;
    (* Terminal Horizon Penalty Cost Term *)
    FOR iIdx := 0 TO 5 DO
        rTempDiff := trajX_mpc[5, iIdx] - vecX_target[iIdx];
        rMpc_AccumulatedCost := rMpc_AccumulatedCost + (vecP_terminal[iIdx] * rTempDiff * rTempDiff);
    END_FOR;

    (* 3c. Terminal Adjoint Costate Vector Initialization: lambda[N] = 2 * P * (x[N] - x_target) *)
    FOR iIdx := 0 TO 5 DO
        trajLambda[5, iIdx] := 2.0 * vecP_terminal[iIdx] * (trajX_mpc[5, iIdx] - vecX_target[iIdx]);
    END_FOR;

    (* 3d. Backward Adjoint Sensitivity Propagation & Control Gradient Extraction *)
    FOR kStep := 4 TO 0 BY -1 DO
        (* Costate Backpropagation: lambda[k] = A^T * lambda[k+1] + 2 * Q * (x[k] - x_target) *)
        FOR iIdx := 0 TO 5 DO
            rTempSum := 0.0;
            FOR jIdx := 0 TO 5 DO
                rTempSum := rTempSum + (matA[jIdx, iIdx] * trajLambda[kStep + 1, jIdx]);
            END_FOR;
            trajLambda[kStep, iIdx] := rTempSum + (2.0 * vecQ_weight[iIdx] * (trajX_mpc[kStep, iIdx] - vecX_target[iIdx]));
        END_FOR;

        (* Control Gradient: grad_J[k] = B^T * lambda[k+1] + 2 * R * u[k] + 2 * R_delta * (u[k] - u_prev) *)
        FOR mIdx := 0 TO 4 DO
            rTempSum := 0.0;
            FOR iIdx := 0 TO 5 DO
                rTempSum := rTempSum + (matB[iIdx, mIdx] * trajLambda[kStep + 1, iIdx]);
            END_FOR;
            trajGrad_J[kStep, mIdx] := rTempSum +
                                      (2.0 * vecR_weight[mIdx] * trajU_mpc[kStep, mIdx]) +
                                      (2.0 * vecR_delta_weight[mIdx] * (trajU_mpc[kStep, mIdx] - vecU_prev[mIdx]));
        END_FOR;
    END_FOR;

    (* 3e. Projected Gradient Descent Update Step & Constraint Projection *)
    FOR kStep := 0 TO 4 DO
        FOR mIdx := 0 TO 4 DO
            (* Gradient Descent Step: u_cand = u - gamma * grad_J *)
            rTempCandidate := trajU_mpc[kStep, mIdx] - (rPgd_StepSize * trajGrad_J[kStep, mIdx]);

            (* Projection 1: Slew Rate Limit Clamping w.r.t Previous Plant Command *)
            rTempDeltaU := rTempCandidate - vecU_prev[mIdx];
            IF rTempDeltaU > vecU_slewMax[mIdx] THEN
                rTempDeltaU := vecU_slewMax[mIdx];
            ELSIF rTempDeltaU < -vecU_slewMax[mIdx] THEN
                rTempDeltaU := -vecU_slewMax[mIdx];
            END_IF;
            rTempCandidate := vecU_prev[mIdx] + rTempDeltaU;

            (* Projection 2: Physical Lower & Upper Actuator Saturation Box Clamping *)
            IF rTempCandidate > vecU_max[mIdx] THEN
                trajU_mpc[kStep, mIdx] := vecU_max[mIdx];
            ELSIF rTempCandidate < vecU_min[mIdx] THEN
                trajU_mpc[kStep, mIdx] := vecU_min[mIdx];
            ELSE
                trajU_mpc[kStep, mIdx] := rTempCandidate;
            END_IF;
        END_FOR;
    END_FOR;
END_FOR;

(* ---------------------------------------------------------------------------------------------------- *)
(* Step 4: Apply Optimal Control Action from Horizon Step 0 to Physical Actuator Outputs                *)
(* ---------------------------------------------------------------------------------------------------- *)
IF NOT bMpcManualOverride AND eState <> 12 AND eState <> 0 THEN
    FOR mIdx := 0 TO 4 DO
        vecU[mIdx] := trajU_mpc[0, mIdx];
        vecU_rate[mIdx] := (vecU[mIdx] - vecU_prev[mIdx]) / tScanCycleTime_s;
        vecU_prev[mIdx] := vecU[mIdx];
    END_FOR;

    rValve_H2_BackPress_Cmd_pct  := vecU[0];
    rValve_Cl2_Vent_Cmd_pct      := vecU[1];
    rValve_WaterDilution_Cmd_pct := vecU[2];
    rValve_BrineTrim_Cmd_pct     := vecU[3];
    rRectifier_Current_Cmd_kA    := vecU[4];
END_IF;

rMpc_CostFunction_Val := rMpc_AccumulatedCost;

(* ==================================================================================================== *)
(* PHASE 4: DETERMINISTIC 14-STAGE PRODUCTION FINITE STATE MACHINE (FSM) ENGINE                          *)
(* States: 0: STATE_IDLE                                                                                 *)
(*         1: STATE_NITROGEN_PURGE_AND_LEAK_CHECK                                                        *)
(*         2: STATE_BRINE_WARMUP_CIRCULATION                                                             *)
(*         3: STATE_RECTIFIER_POLARIZATION_CURRENT_INIT                                                  *)
(*         4: STATE_RAMP_CURRENT_LOW_LOAD_25PCT                                                          *)
(*         5: STATE_PRESSURE_EQUILIBRATION_TRANSITION                                                    *)
(*         6: STATE_NOMINAL_BASELOAD_PRODUCTION                                                          *)
(*         7: STATE_CAUSTIC_CONCENTRATION_CONTROL_LOOP                                                   *)
(*         8: STATE_BRINE_DEPLETION_FEED_CONTROL                                                         *)
(*         9: STATE_MEMBRANE_HEALTH_VOLTAGE_MONITORING                                                   *)
(*         10: STATE_CONTROLLED_RAMP_DOWN_TURNDOWN                                                       *)
(*         11: STATE_AUTOMATED_SHUTDOWN_POLARIZATION_HOLD                                                *)
(*         12: STATE_EMERGENCY_DEPRESSURIZATION_SCRUBBER_TRIP                                            *)
(*         13: STATE_POST_TRIP_NITROGEN_INERT_BLANKET                                                    *)
(* ==================================================================================================== *)

(* Universal State Dwell Timer Accumulation *)
rStateTimer_s := rStateTimer_s + tScanCycleTime_s;

(* Universal Safety Critical Emergency Trip Interlock *)
IF (bEmergencyStop OR bAlarm_DP_HH OR bAlarm_DP_LL OR bAlarm_H2_in_Cl2_HH OR bPDT_Cell_DP_Trip OR
    bAlarm_P_Cl2_HH OR bAlarm_P_Cl2_LL OR bAlarm_P_H2_HH OR bAlarm_P_H2_LL OR
    (NOT bRectifierOnlineFeedback AND eState >= 3 AND eState <= 11)) AND eState <> 12 AND eState <> 13 THEN
    ePrevState := eState;
    eState := 12; (* Fast Divert to Emergency Depressurization Scrubber Trip *)
    rStateTimer_s := 0.0;
    rEmergencyTripTimer_s := 0.0;
END_IF;

CASE eState OF
    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 0: IDLE / STANDBY                                                                          *)
    (* Plant De-Energized, Cold Standby, Awaiting Process Permissives & Operator Start Command          *)
    (* ------------------------------------------------------------------------------------------------ *)
    0:
        (* De-energize Actuator Commands *)
        rValve_H2_BackPress_Cmd_pct  := 0.0;
        rValve_Cl2_Vent_Cmd_pct      := 0.0;
        rValve_WaterDilution_Cmd_pct := 0.0;
        rValve_BrineTrim_Cmd_pct     := 0.0;
        rRectifier_Current_Cmd_kA    := 0.0;

        (* Discrete Solenoids in Safe Parked State *)
        bValve_EmergencyScrubberVent := FALSE;
        bValve_EmergencyH2VentStack  := FALSE;
        bValve_N2_AnolytePurge       := FALSE;
        bValve_N2_CatholytePurge     := FALSE;
        bRectifier_TripInterlock     := FALSE;
        bElectrolyzerIsolateValves   := FALSE;
        bBrinePreheaterSteamValve    := FALSE;
        bCausticCoolerWaterValve     := FALSE;

        (* Transition Condition: All Permissives Active & Start Command Rising Edge *)
        IF bEnable AND bAutoCycleStart AND NOT bEmergencyStop AND
           bNitrogenPurgePermissive AND bChlorineAbsorptionReady AND
           bHydrogenVentStackReady AND bDeminWaterSupplyPermissive THEN
            ePrevState := 0;
            eState := 1; (* Advance to Nitrogen Purge & Leak Check *)
            rStateTimer_s := 0.0;
            rPurgeTimer_s := 0.0;
            rLeakCheckTimer_s := 0.0;
            iFsmStepIndex := 0;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 1: NITROGEN PURGE AND LEAK CHECK                                                           *)
    (* Displace Atmospheric Air / Oxygen from Cell Boxes & Conduct 60-Second Pressure Decay Leak Check  *)
    (* ------------------------------------------------------------------------------------------------ *)
    1:
        IF iFsmStepIndex = 0 THEN
            (* Step 0: Open N2 Purge Solenoids & Open Gas Vent Valves to Sweep Residual Gases *)
            bValve_N2_AnolytePurge      := TRUE;
            bValve_N2_CatholytePurge    := TRUE;
            rValve_Cl2_Vent_Cmd_pct     := 20.0;
            rValve_H2_BackPress_Cmd_pct := 20.0;
            rPurgeTimer_s := rPurgeTimer_s + tScanCycleTime_s;

            (* Dwell 45 Seconds for Complete Header Sweeping *)
            IF rPurgeTimer_s >= 45.0 THEN
                iFsmStepIndex := 1;
                rLeakCheckTimer_s := 0.0;
            END_IF;
        ELSIF iFsmStepIndex = 1 THEN
            (* Step 1: Pressure Hold Leak Decay Check at 0.10 bar (100 mbar) *)
            bValve_N2_AnolytePurge      := FALSE;
            bValve_N2_CatholytePurge    := FALSE;
            rValve_Cl2_Vent_Cmd_pct     := 0.0;
            rValve_H2_BackPress_Cmd_pct := 0.0;
            rLeakCheckTimer_s := rLeakCheckTimer_s + tScanCycleTime_s;

            (* Verify Leak Decay Rate < 0.005 bar (5 mbar) over 60 seconds *)
            IF rLeakCheckTimer_s >= 60.0 THEN
                IF rPT_Cl2_Header_Voted >= 0.080 AND rPT_H2_Header_Voted >= 0.080 AND
                   ABS(rPDT_Cell_DP_Voted) <= 2.50 THEN
                    (* Leak Check Passed Successfully *)
                    ePrevState := 1;
                    eState := 2; (* Advance to Brine Warmup Circulation *)
                    rStateTimer_s := 0.0;
                    rBrineWarmupTimer_s := 0.0;
                    iFsmStepIndex := 0;
                ELSE
                    (* Leak Check Failed: Abort to IDLE *)
                    ePrevState := 1;
                    eState := 0;
                    rStateTimer_s := 0.0;
                END_IF;
            END_IF;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 2: BRINE WARMUP CIRCULATION                                                                *)
    (* Circulate Saturated Brine & Weak Caustic; Pre-Heat Electrolyzer to >= 80 deg C Before Powering   *)
    (* ------------------------------------------------------------------------------------------------ *)
    2:
        (* Modulate Brine Trim Valve to 35% & Activate Warmup Steam Exchanger *)
        rValve_BrineTrim_Cmd_pct  := 35.0;
        bBrinePreheaterSteamValve := TRUE;
        rBrineWarmupTimer_s       := rBrineWarmupTimer_s + tScanCycleTime_s;

        (* Check Circulation Pumps are Running *)
        IF bAnolyteRecircPumpRunning AND bCausticRecircPumpRunning THEN
            (* Confirm Cell Stack Bulk Temperature Reached Safe 80.0 deg C Activation Point *)
            IF rCell_Temperature_degC >= 80.0 AND rBrineWarmupTimer_s >= 30.0 THEN
                bBrinePreheaterSteamValve := FALSE;
                ePrevState := 2;
                eState := 3; (* Advance to Rectifier Polarization Current Init *)
                rStateTimer_s := 0.0;
                rPolarizationInitTimer_s := 0.0;
                iFsmStepIndex := 0;
            END_IF;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 3: RECTIFIER POLARIZATION CURRENT INITIALIZATION                                           *)
    (* Energize DC Rectifier to Minimum Polarization Current (5% Load, 3.50 kA) to Protect DSA Coating  *)
    (* ------------------------------------------------------------------------------------------------ *)
    3:
        bRectifier_TripInterlock  := FALSE;
        rRectifier_Current_Cmd_kA := 3.50; (* 5% of 70 kA *)
        rPolarizationInitTimer_s  := rPolarizationInitTimer_s + tScanCycleTime_s;

        (* Verify Rectifier Interlock Closed & Polarization Current Flowing *)
        IF rPolarizationInitTimer_s >= 30.0 AND rRectifier_CurrentFb_kA >= 3.0 AND
           rCell_AverageVoltage_V >= 2.10 AND rCell_AverageVoltage_V <= 2.45 THEN
            (* Polarization Established Safely *)
            ePrevState := 3;
            eState := 4; (* Advance to Ramp Current Low Load 25% *)
            rStateTimer_s := 0.0;
            rLowLoadRampTimer_s := 0.0;
            iFsmStepIndex := 0;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 4: RAMP CURRENT TO LOW LOAD (25% BASELOAD, ~17.5 kA)                                       *)
    (* Smoothly Ramp Rectifier Current at 1.0 kA/10s; Initiate Gas Header Pressure Regulation           *)
    (* ------------------------------------------------------------------------------------------------ *)
    4:
        rLowLoadRampTimer_s := rLowLoadRampTimer_s + tScanCycleTime_s;

        (* Controlled Rectifier Current Ramp from 3.50 kA to 17.50 kA *)
        IF rRectifier_Current_Cmd_kA < 17.50 THEN
            rRectifier_Current_Cmd_kA := MIN(17.50, rRectifier_Current_Cmd_kA + (0.10 * tScanCycleTime_s));
        END_IF;

        (* Check Transition Conditions: Current Reached 17.5 kA and DP within +/- 2.5 mbar *)
        IF rRectifier_CurrentFb_kA >= 17.0 AND ABS(rEst_Cell_DP_mbar - 18.0) <= 2.50 AND
           rLowLoadRampTimer_s >= 60.0 THEN
            ePrevState := 4;
            eState := 5; (* Advance to Pressure Equilibration Transition *)
            rStateTimer_s := 0.0;
            rPressureEquilibrationTimer_s := 0.0;
            iFsmStepIndex := 0;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 5: PRESSURE EQUILIBRATION TRANSITION                                                       *)
    (* Lock Differential Pressure Within +/- 1.5 mbar at +30.0 mbar Setpoint; Gas Purity Verification   *)
    (* ------------------------------------------------------------------------------------------------ *)
    5:
        rPressureEquilibrationTimer_s := rPressureEquilibrationTimer_s + tScanCycleTime_s;

        (* Hold at 25% Load While MPC Locks In Header Pressures and Differential Pressure *)
        IF rPressureEquilibrationTimer_s >= 60.0 AND ABS(rEst_Cell_DP_mbar - 30.0) <= 1.50 AND
           rAT_H2_in_Cl2_Voted <= 0.25 AND rPT_Cl2_Header_Voted >= 0.180 AND rPT_H2_Header_Voted >= 0.200 THEN
            ePrevState := 5;
            eState := 6; (* Advance to Nominal Baseload Production *)
            rStateTimer_s := 0.0;
            iFsmStepIndex := 0;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 6: NOMINAL BASELOAD PRODUCTION                                                             *)
    (* Full Current Density (2.5 kA/m2, 67.5 kA); Multi-Variable Receding Horizon MPC Balancing         *)
    (* ------------------------------------------------------------------------------------------------ *)
    6:
        (* Rectifier Allowed to Ramp Up to Baseload Current (up to 67.5 kA) *)
        IF rRectifier_Current_Cmd_kA < 67.50 THEN
            rRectifier_Current_Cmd_kA := MIN(67.50, rRectifier_Current_Cmd_kA + (0.25 * tScanCycleTime_s));
        END_IF;

        (* Thermal Cooling Regulation to Maintain 88 deg C *)
        IF rEst_Cell_Temperature_degC > 88.5 THEN
            bCausticCoolerWaterValve := TRUE;
        ELSIF rEst_Cell_Temperature_degC < 87.0 THEN
            bCausticCoolerWaterValve := FALSE;
        END_IF;

        (* Dynamic Transitions to Specialized Sub-Loops Based on Process Deviations *)
        IF ABS(rEst_Catholyte_NaOH_pct - 32.5) > 0.80 AND rStateTimer_s >= 30.0 THEN
            ePrevState := 6;
            eState := 7; (* Caustic Concentration Control Loop Tuning *)
            rStateTimer_s := 0.0;
        ELSIF rEst_Anolyte_NaCl_gL < 195.0 AND rStateTimer_s >= 30.0 THEN
            ePrevState := 6;
            eState := 8; (* Brine Depletion Feed Control Loop Tuning *)
            rStateTimer_s := 0.0;
        ELSIF rCellVoltageDeviation_V > 0.150 AND rStateTimer_s >= 60.0 THEN
            ePrevState := 6;
            eState := 9; (* Membrane Health & Specific Resistance Monitoring *)
            rStateTimer_s := 0.0;
        ELSIF bPlantStop THEN
            ePrevState := 6;
            eState := 10; (* Orderly Ramp-Down Turndown Sequence *)
            rStateTimer_s := 0.0;
            rTurndownRampTimer_s := 0.0;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 7: CAUSTIC CONCENTRATION CONTROL LOOP                                                      *)
    (* High-Precision Feedforward & Feedback Regulation of Demin Water Catholyte Dilution               *)
    (* ------------------------------------------------------------------------------------------------ *)
    7:
        (* Priority Trim on Soft Water Dilution Valve *)
        IF rEst_Catholyte_NaOH_pct > 32.7 THEN
            rValve_WaterDilution_Cmd_pct := MIN(100.0, rValve_WaterDilution_Cmd_pct + (0.15 * tScanCycleTime_s));
        ELSIF rEst_Catholyte_NaOH_pct < 32.3 THEN
            rValve_WaterDilution_Cmd_pct := MAX(0.0, rValve_WaterDilution_Cmd_pct - (0.15 * tScanCycleTime_s));
        END_IF;

        (* Return to Nominal Baseload when Caustic Concentration Returns to +/- 0.15 wt% Band *)
        IF ABS(rEst_Catholyte_NaOH_pct - 32.5) <= 0.15 AND rStateTimer_s >= 30.0 THEN
            ePrevState := 7;
            eState := 6; (* Return to Baseload Production *)
            rStateTimer_s := 0.0;
        ELSIF bPlantStop THEN
            ePrevState := 7;
            eState := 10;
            rStateTimer_s := 0.0;
            rTurndownRampTimer_s := 0.0;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 8: BRINE DEPLETION FEED CONTROL                                                            *)
    (* Adjust Saturated Brine Feed Trim to Rebalance Anolyte Salt Concentration to 205.0 g/L            *)
    (* ------------------------------------------------------------------------------------------------ *)
    8:
        (* Boost Fresh Saturated Brine Inflow Feed *)
        IF rEst_Anolyte_NaCl_gL < 205.0 THEN
            rValve_BrineTrim_Cmd_pct := MIN(100.0, rValve_BrineTrim_Cmd_pct + (0.20 * tScanCycleTime_s));
        ELSIF rEst_Anolyte_NaCl_gL > 215.0 THEN
            rValve_BrineTrim_Cmd_pct := MAX(10.0, rValve_BrineTrim_Cmd_pct - (0.20 * tScanCycleTime_s));
        END_IF;

        (* Return to Nominal Baseload when Anolyte Salt Restored *)
        IF rEst_Anolyte_NaCl_gL >= 203.0 AND rStateTimer_s >= 30.0 THEN
            ePrevState := 8;
            eState := 6; (* Return to Baseload Production *)
            rStateTimer_s := 0.0;
        ELSIF bPlantStop THEN
            ePrevState := 8;
            eState := 10;
            rStateTimer_s := 0.0;
            rTurndownRampTimer_s := 0.0;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 9: MEMBRANE HEALTH VOLTAGE MONITORING                                                      *)
    (* Evaluate Membrane Specific Ohmic Resistance, Gas Bubble Stagnation & Micro-Deformation           *)
    (* ------------------------------------------------------------------------------------------------ *)
    9:
        (* Boost Circulation to Sweep Stagnant Bubbles from Membrane Surface *)
        IF rCalc_MembraneAreaResist_mOhm > 300.0 THEN
            rValve_BrineTrim_Cmd_pct := MIN(100.0, rValve_BrineTrim_Cmd_pct + 5.0);
        END_IF;

        (* Dwell 60 Seconds to Gather Frequency Response & Resistance Data *)
        IF rStateTimer_s >= 60.0 THEN
            ePrevState := 9;
            eState := 6; (* Return to Baseload Production *)
            rStateTimer_s := 0.0;
        ELSIF bPlantStop THEN
            ePrevState := 9;
            eState := 10;
            rStateTimer_s := 0.0;
            rTurndownRampTimer_s := 0.0;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 10: CONTROLLED RAMP-DOWN TURNDOWN                                                          *)
    (* Orderly Rectifier Turndown at -1.5 kA/5s Down to Polarization Current (3.50 kA)                  *)
    (* ------------------------------------------------------------------------------------------------ *)
    10:
        rTurndownRampTimer_s := rTurndownRampTimer_s + tScanCycleTime_s;

        (* Smoothly Turndown Current *)
        IF rRectifier_Current_Cmd_kA > 3.50 THEN
            rRectifier_Current_Cmd_kA := MAX(3.50, rRectifier_Current_Cmd_kA - (0.30 * tScanCycleTime_s));
        END_IF;

        (* Throttle Gas Valves Concurrently to Avoid DP Divergence *)
        IF rRectifier_CurrentFb_kA <= 4.0 AND rTurndownRampTimer_s >= 60.0 THEN
            ePrevState := 10;
            eState := 11; (* Advance to Automated Shutdown Polarization Hold *)
            rStateTimer_s := 0.0;
            rShutdownPolarizationTimer_s := 0.0;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 11: AUTOMATED SHUTDOWN POLARIZATION HOLD                                                   *)
    (* Hold at 5% Current (3.50 kA) to Prevent Reverse Galvanic Current While Preparing Depressurization *)
    (* ------------------------------------------------------------------------------------------------ *)
    11:
        rRectifier_Current_Cmd_kA    := 3.50;
        rShutdownPolarizationTimer_s := rShutdownPolarizationTimer_s + tScanCycleTime_s;

        (* Confirm Complete Shutdown Command *)
        IF rShutdownPolarizationTimer_s >= 60.0 AND NOT bAutoCycleStart THEN
            (* De-energize Rectifier and Transition to Nitrogen Purge / Standby *)
            rRectifier_Current_Cmd_kA := 0.0;
            bRectifier_TripInterlock  := TRUE;
            ePrevState := 11;
            eState := 0; (* Return to Standby IDLE *)
            rStateTimer_s := 0.0;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 12: EMERGENCY DEPRESSURIZATION SCRUBBER TRIP                                               *)
    (* Immediate Interlock: Rectifier Trip, Open Chlorine Scrubber Solenoid, Open H2 Flare Vent, Purge  *)
    (* ------------------------------------------------------------------------------------------------ *)
    12:
        rEmergencyTripTimer_s := rEmergencyTripTimer_s + tScanCycleTime_s;

        (* 1. Fast Rectifier Hardware Interlock Trip *)
        bRectifier_TripInterlock  := TRUE;
        rRectifier_Current_Cmd_kA := 0.0;

        (* 2. Fast Emergency Vent Solenoids Actuation *)
        bValve_EmergencyScrubberVent := TRUE; (* Dump Cl2 to Caustic Neutralization Scrubber *)
        bValve_EmergencyH2VentStack  := TRUE; (* Dump H2 to Atmosphere Flare Stack *)

        (* 3. High-Pressure Inert Nitrogen Purge Ingress *)
        bValve_N2_AnolytePurge       := TRUE;
        bValve_N2_CatholytePurge     := TRUE;

        (* 4. Double Block & Bleed Skid Isolation *)
        bElectrolyzerIsolateValves   := TRUE;
        bBrinePreheaterSteamValve    := FALSE;
        bCausticCoolerWaterValve     := FALSE;

        (* 5. Modulating Valves Forced Safe *)
        rValve_H2_BackPress_Cmd_pct  := 100.0;
        rValve_Cl2_Vent_Cmd_pct      := 100.0;
        rValve_WaterDilution_Cmd_pct := 0.0;
        rValve_BrineTrim_Cmd_pct     := 0.0;

        (* Dwell 60 Seconds to Evacuate All Hazardous Gases *)
        IF rEmergencyTripTimer_s >= 60.0 THEN
            ePrevState := 12;
            eState := 13; (* Transition to Post-Trip Nitrogen Inert Blanket *)
            rStateTimer_s := 0.0;
            rPostTripBlanketTimer_s := 0.0;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 13: POST-TRIP NITROGEN INERT BLANKET                                                       *)
    (* Maintain Positive Inert Blanket (0.02 bar) to Inhibit Atmospheric Oxygen or Hydrogen Cross-Leak  *)
    (* ------------------------------------------------------------------------------------------------ *)
    13:
        rPostTripBlanketTimer_s := rPostTripBlanketTimer_s + tScanCycleTime_s;

        (* Maintain Low Continuous Inert Blanket *)
        bValve_EmergencyScrubberVent := FALSE;
        bValve_EmergencyH2VentStack  := FALSE;
        bValve_N2_AnolytePurge       := TRUE;
        bValve_N2_CatholytePurge     := TRUE;
        rValve_H2_BackPress_Cmd_pct  := 5.0;
        rValve_Cl2_Vent_Cmd_pct      := 5.0;

        (* Operator Reset & Acknowledge Sequence to Clear Trip *)
        IF bFaultReset AND bAlarmAck AND NOT bEmergencyStop AND
           NOT bAlarm_DP_HH AND NOT bAlarm_DP_LL AND NOT bAlarm_H2_in_Cl2_HH AND
           rPostTripBlanketTimer_s >= 30.0 THEN
            ePrevState := 13;
            eState := 0; (* Return to IDLE *)
            rStateTimer_s := 0.0;
        END_IF;
END_CASE;

iActiveFsmState := eState;

(* ==================================================================================================== *)
(* PHASE 5: ISA-18.2 MULTI-TIER PROCESS ALARMS, DIAGNOSTICS & 32-BIT BIT-PACKED TELEMETRY               *)
(* Alarms: 4-Tier Matrix (HH, H, L, LL) with Clearance Hysteresis Deadbands                              *)
(* Features: First-Out Latching Architecture, 32-Bit Packed Status, Diagnostic & Alarm Words             *)
(* ==================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------- *)
(* Tier 1: Cell Differential Pressure Alarms [mbar] (Catholyte minus Anolyte)                           *)
(* HH = 6.0 mbar (Membrane Rupture), H = 3.0 mbar, L = -3.0 mbar, LL = -6.0 mbar (Reverse Pinch)       *)
(* ---------------------------------------------------------------------------------------------------- *)
IF rPDT_Cell_DP_Voted >= rDP_HH_Limit_mbar THEN
    bAlarm_DP_HH := TRUE;
ELSIF rPDT_Cell_DP_Voted <= (rDP_HH_Limit_mbar - rDP_Deadband_mbar) THEN
    bAlarm_DP_HH := FALSE;
END_IF;

IF rPDT_Cell_DP_Voted >= rDP_H_Limit_mbar THEN
    bAlarm_DP_H := TRUE;
ELSIF rPDT_Cell_DP_Voted <= (rDP_H_Limit_mbar - rDP_Deadband_mbar) THEN
    bAlarm_DP_H := FALSE;
END_IF;

IF rPDT_Cell_DP_Voted <= rDP_L_Limit_mbar THEN
    bAlarm_DP_L := TRUE;
ELSIF rPDT_Cell_DP_Voted >= (rDP_L_Limit_mbar + rDP_Deadband_mbar) THEN
    bAlarm_DP_L := FALSE;
END_IF;

IF rPDT_Cell_DP_Voted <= rDP_LL_Limit_mbar THEN
    bAlarm_DP_LL := TRUE;
ELSIF rPDT_Cell_DP_Voted >= (rDP_LL_Limit_mbar + rDP_Deadband_mbar) THEN
    bAlarm_DP_LL := FALSE;
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* Tier 2: Chlorine Header Pressure Alarms [bar]                                                        *)
(* HH = 0.60 bar (Overpressure Trip), H = 0.40 bar, L = 0.05 bar, LL = -0.02 bar (Vacuum Ingress Trip)  *)
(* ---------------------------------------------------------------------------------------------------- *)
IF rPT_Cl2_Header_Voted >= rP_Cl2_HH_Limit_bar THEN
    bAlarm_P_Cl2_HH := TRUE;
ELSIF rPT_Cl2_Header_Voted <= (rP_Cl2_HH_Limit_bar - rP_Cl2_Deadband_bar) THEN
    bAlarm_P_Cl2_HH := FALSE;
END_IF;

IF rPT_Cl2_Header_Voted >= rP_Cl2_H_Limit_bar THEN
    bAlarm_P_Cl2_H := TRUE;
ELSIF rPT_Cl2_Header_Voted <= (rP_Cl2_H_Limit_bar - rP_Cl2_Deadband_bar) THEN
    bAlarm_P_Cl2_H := FALSE;
END_IF;

IF rPT_Cl2_Header_Voted <= rP_Cl2_L_Limit_bar THEN
    bAlarm_P_Cl2_L := TRUE;
ELSIF rPT_Cl2_Header_Voted >= (rP_Cl2_L_Limit_bar + rP_Cl2_Deadband_bar) THEN
    bAlarm_P_Cl2_L := FALSE;
END_IF;

IF rPT_Cl2_Header_Voted <= rP_Cl2_LL_Limit_bar THEN
    bAlarm_P_Cl2_LL := TRUE;
ELSIF rPT_Cl2_Header_Voted >= (rP_Cl2_LL_Limit_bar + rP_Cl2_Deadband_bar) THEN
    bAlarm_P_Cl2_LL := FALSE;
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* Tier 3: Hydrogen Header Pressure Alarms [bar]                                                        *)
(* HH = 0.62 bar, H = 0.42 bar, L = 0.06 bar, LL = -0.01 bar (Air Ingress Detonation Hazard)           *)
(* ---------------------------------------------------------------------------------------------------- *)
IF rPT_H2_Header_Voted >= rP_H2_HH_Limit_bar THEN
    bAlarm_P_H2_HH := TRUE;
ELSIF rPT_H2_Header_Voted <= (rP_H2_HH_Limit_bar - rP_H2_Deadband_bar) THEN
    bAlarm_P_H2_HH := FALSE;
END_IF;

IF rPT_H2_Header_Voted >= rP_H2_H_Limit_bar THEN
    bAlarm_P_H2_H := TRUE;
ELSIF rPT_H2_Header_Voted <= (rP_H2_H_Limit_bar - rP_H2_Deadband_bar) THEN
    bAlarm_P_H2_H := FALSE;
END_IF;

IF rPT_H2_Header_Voted <= rP_H2_L_Limit_bar THEN
    bAlarm_P_H2_L := TRUE;
ELSIF rPT_H2_Header_Voted >= (rP_H2_L_Limit_bar + rP_H2_Deadband_bar) THEN
    bAlarm_P_H2_L := FALSE;
END_IF;

IF rPT_H2_Header_Voted <= rP_H2_LL_Limit_bar THEN
    bAlarm_P_H2_LL := TRUE;
ELSIF rPT_H2_Header_Voted >= (rP_H2_LL_Limit_bar + rP_H2_Deadband_bar) THEN
    bAlarm_P_H2_LL := FALSE;
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* Tier 4: Inline Hydrogen-in-Chlorine Gas Purity Alarms [% vol]                                        *)
(* HH = 1.20 % vol (Immediate Emergency Scrubber Trip), H = 0.60 % vol (High Advisory Warning)         *)
(* ---------------------------------------------------------------------------------------------------- *)
IF rAT_H2_in_Cl2_Voted >= rH2_in_Cl2_HH_Limit_pct THEN
    bAlarm_H2_in_Cl2_HH := TRUE;
ELSIF rAT_H2_in_Cl2_Voted <= (rH2_in_Cl2_HH_Limit_pct - rH2_in_Cl2_Deadband_pct) THEN
    bAlarm_H2_in_Cl2_HH := FALSE;
END_IF;

IF rAT_H2_in_Cl2_Voted >= rH2_in_Cl2_H_Limit_pct THEN
    bAlarm_H2_in_Cl2_H := TRUE;
ELSIF rAT_H2_in_Cl2_Voted <= (rH2_in_Cl2_H_Limit_pct - rH2_in_Cl2_Deadband_pct) THEN
    bAlarm_H2_in_Cl2_H := FALSE;
END_IF;

IF rAT_H2_in_Cl2_Voted <= rH2_in_Cl2_L_Limit_pct THEN
    bAlarm_H2_in_Cl2_L := TRUE;
ELSIF rAT_H2_in_Cl2_Voted >= (rH2_in_Cl2_L_Limit_pct + rH2_in_Cl2_Deadband_pct) THEN
    bAlarm_H2_in_Cl2_L := FALSE;
END_IF;

IF rAT_H2_in_Cl2_Voted <= rH2_in_Cl2_LL_Limit_pct THEN
    bAlarm_H2_in_Cl2_LL := TRUE;
ELSIF rAT_H2_in_Cl2_Voted >= (rH2_in_Cl2_LL_Limit_pct + rH2_in_Cl2_Deadband_pct) THEN
    bAlarm_H2_in_Cl2_LL := FALSE;
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* Tier 5: Anolyte Depleted Brine Concentration Alarms [g/L]                                            *)
(* LL = 175.0 g/L (Severe O2 Evolution / DSA Coating Destruction), L = 190.0 g/L, H = 225.0, HH = 240.0 *)
(* ---------------------------------------------------------------------------------------------------- *)
IF rAT_Anolyte_NaCl_Voted >= rBrine_HH_Limit_gL THEN
    bAlarm_Brine_HH := TRUE;
ELSIF rAT_Anolyte_NaCl_Voted <= (rBrine_HH_Limit_gL - rBrine_Deadband_gL) THEN
    bAlarm_Brine_HH := FALSE;
END_IF;

IF rAT_Anolyte_NaCl_Voted >= rBrine_H_Limit_gL THEN
    bAlarm_Brine_H := TRUE;
ELSIF rAT_Anolyte_NaCl_Voted <= (rBrine_H_Limit_gL - rBrine_Deadband_gL) THEN
    bAlarm_Brine_H := FALSE;
END_IF;

IF rAT_Anolyte_NaCl_Voted <= rBrine_L_Limit_gL THEN
    bAlarm_Brine_L := TRUE;
ELSIF rAT_Anolyte_NaCl_Voted >= (rBrine_L_Limit_gL + rBrine_Deadband_gL) THEN
    bAlarm_Brine_L := FALSE;
END_IF;

IF rAT_Anolyte_NaCl_Voted <= rBrine_LL_Limit_gL THEN
    bAlarm_Brine_LL := TRUE;
ELSIF rAT_Anolyte_NaCl_Voted >= (rBrine_LL_Limit_gL + rBrine_Deadband_gL) THEN
    bAlarm_Brine_LL := FALSE;
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* Tier 6: Catholyte Caustic Soda Concentration Alarms [wt%]                                            *)
(* HH = 36.0 wt% (Precipitation / Membrane Damage), H = 34.5 wt%, L = 31.0 wt%, LL = 28.0 wt%           *)
(* ---------------------------------------------------------------------------------------------------- *)
IF rAT_Catholyte_NaOH_Voted >= rCaustic_HH_Limit_pct THEN
    bAlarm_Caustic_HH := TRUE;
ELSIF rAT_Catholyte_NaOH_Voted <= (rCaustic_HH_Limit_pct - rCaustic_Deadband_pct) THEN
    bAlarm_Caustic_HH := FALSE;
END_IF;

IF rAT_Catholyte_NaOH_Voted >= rCaustic_H_Limit_pct THEN
    bAlarm_Caustic_H := TRUE;
ELSIF rAT_Catholyte_NaOH_Voted <= (rCaustic_H_Limit_pct - rCaustic_Deadband_pct) THEN
    bAlarm_Caustic_H := FALSE;
END_IF;

IF rAT_Catholyte_NaOH_Voted <= rCaustic_L_Limit_pct THEN
    bAlarm_Caustic_L := TRUE;
ELSIF rAT_Catholyte_NaOH_Voted >= (rCaustic_L_Limit_pct + rCaustic_Deadband_pct) THEN
    bAlarm_Caustic_L := FALSE;
END_IF;

IF rAT_Catholyte_NaOH_Voted <= rCaustic_LL_Limit_pct THEN
    bAlarm_Caustic_LL := TRUE;
ELSIF rAT_Catholyte_NaOH_Voted >= (rCaustic_LL_Limit_pct + rCaustic_Deadband_pct) THEN
    bAlarm_Caustic_LL := FALSE;
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* Tier 7: Electrolyzer Cell Stack Temperature Alarms [deg C]                                           *)
(* HH = 93.0 deg C (Boiling Hazard), H = 90.0 deg C, L = 80.0 deg C, LL = 70.0 deg C                   *)
(* ---------------------------------------------------------------------------------------------------- *)
IF rCell_Temperature_degC >= rTemp_HH_Limit_degC THEN
    bAlarm_Temp_HH := TRUE;
ELSIF rCell_Temperature_degC <= (rTemp_HH_Limit_degC - rTemp_Deadband_degC) THEN
    bAlarm_Temp_HH := FALSE;
END_IF;

IF rCell_Temperature_degC >= rTemp_H_Limit_degC THEN
    bAlarm_Temp_H := TRUE;
ELSIF rCell_Temperature_degC <= (rTemp_H_Limit_degC - rTemp_Deadband_degC) THEN
    bAlarm_Temp_H := FALSE;
END_IF;

IF rCell_Temperature_degC <= rTemp_L_Limit_degC THEN
    bAlarm_Temp_L := TRUE;
ELSIF rCell_Temperature_degC >= (rTemp_L_Limit_degC + rTemp_Deadband_degC) THEN
    bAlarm_Temp_L := FALSE;
END_IF;

IF rCell_Temperature_degC <= rTemp_LL_Limit_degC THEN
    bAlarm_Temp_LL := TRUE;
ELSIF rCell_Temperature_degC >= (rTemp_LL_Limit_degC + rTemp_Deadband_degC) THEN
    bAlarm_Temp_LL := FALSE;
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* Tier 8: Single-Cell Polarization Voltage Alarms [V]                                                  *)
(* HH = 3.55 V (Passivation / Membrane Blistering), H = 3.35 V, L = 2.85 V, LL = 2.10 V (Short Circuit) *)
(* ---------------------------------------------------------------------------------------------------- *)
IF rCell_AverageVoltage_V >= rVolt_HH_Limit_V THEN
    bAlarm_Volt_HH := TRUE;
ELSIF rCell_AverageVoltage_V <= (rVolt_HH_Limit_V - rVolt_Deadband_V) THEN
    bAlarm_Volt_HH := FALSE;
END_IF;

IF rCell_AverageVoltage_V >= rVolt_H_Limit_V THEN
    bAlarm_Volt_H := TRUE;
ELSIF rCell_AverageVoltage_V <= (rVolt_H_Limit_V - rVolt_Deadband_V) THEN
    bAlarm_Volt_H := FALSE;
END_IF;

IF rCell_AverageVoltage_V <= rVolt_L_Limit_V THEN
    bAlarm_Volt_L := TRUE;
ELSIF rCell_AverageVoltage_V >= (rVolt_L_Limit_V + rVolt_Deadband_V) THEN
    bAlarm_Volt_L := FALSE;
END_IF;

IF rCell_AverageVoltage_V <= rVolt_LL_Limit_V THEN
    bAlarm_Volt_LL := TRUE;
ELSIF rCell_AverageVoltage_V >= (rVolt_LL_Limit_V + rVolt_Deadband_V) THEN
    bAlarm_Volt_LL := FALSE;
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* First-Out Latching Diagnostic Architecture                                                           *)
(* Freezes and Preserves the First Hardware Fault Triggering an Emergency Plant Trip                   *)
(* ---------------------------------------------------------------------------------------------------- *)
IF NOT bFirstOutLatched THEN
    IF bAlarm_DP_HH THEN
        dwFirstOutCapturedCode := 16#00000001; (* Code 1: Cell Differential Pressure High-High *)
        bFirstOutLatched := TRUE;
    ELSIF bAlarm_DP_LL THEN
        dwFirstOutCapturedCode := 16#00000002; (* Code 2: Cell Differential Pressure Low-Low *)
        bFirstOutLatched := TRUE;
    ELSIF bAlarm_P_Cl2_HH THEN
        dwFirstOutCapturedCode := 16#00000004; (* Code 4: Chlorine Header Overpressure HH *)
        bFirstOutLatched := TRUE;
    ELSIF bAlarm_P_Cl2_LL THEN
        dwFirstOutCapturedCode := 16#00000008; (* Code 8: Chlorine Header Vacuum Ingress LL *)
        bFirstOutLatched := TRUE;
    ELSIF bAlarm_P_H2_HH THEN
        dwFirstOutCapturedCode := 16#00000010; (* Code 16: Hydrogen Header Overpressure HH *)
        bFirstOutLatched := TRUE;
    ELSIF bAlarm_P_H2_LL THEN
        dwFirstOutCapturedCode := 16#00000020; (* Code 32: Hydrogen Header Vacuum Ingress LL *)
        bFirstOutLatched := TRUE;
    ELSIF bAlarm_H2_in_Cl2_HH THEN
        dwFirstOutCapturedCode := 16#00000040; (* Code 64: H2 in Cl2 Detonation Risk HH *)
        bFirstOutLatched := TRUE;
    ELSIF bAlarm_Brine_LL THEN
        dwFirstOutCapturedCode := 16#00000080; (* Code 128: Brine Concentration Under-Saturation LL *)
        bFirstOutLatched := TRUE;
    ELSIF bAlarm_Caustic_HH THEN
        dwFirstOutCapturedCode := 16#00000100; (* Code 256: Caustic High Precipitation HH *)
        bFirstOutLatched := TRUE;
    ELSIF bAlarm_Temp_HH THEN
        dwFirstOutCapturedCode := 16#00000200; (* Code 512: Cell Temperature Boiling HH *)
        bFirstOutLatched := TRUE;
    ELSIF bAlarm_Volt_HH THEN
        dwFirstOutCapturedCode := 16#00000400; (* Code 1024: Cell Voltage High Passivation HH *)
        bFirstOutLatched := TRUE;
    ELSIF bAlarm_Volt_LL THEN
        dwFirstOutCapturedCode := 16#00000800; (* Code 2048: Cell Voltage Low Short Circuit LL *)
        bFirstOutLatched := TRUE;
    ELSIF bPDT_Cell_DP_Trip THEN
        dwFirstOutCapturedCode := 16#00001000; (* Code 4096: Cell DP Complete TMR Sensor Failure *)
        bFirstOutLatched := TRUE;
    ELSIF bEmergencyStop THEN
        dwFirstOutCapturedCode := 16#00010000; (* Code 65536: Master Emergency Stop Pushbutton *)
        bFirstOutLatched := TRUE;
    END_IF;
END_IF;

(* Clear First-Out Latch on Authorized Operator Reset *)
IF bFaultReset AND bAlarmAck THEN
    IF NOT bAlarm_DP_HH AND NOT bAlarm_DP_LL AND NOT bAlarm_P_Cl2_HH AND NOT bAlarm_P_Cl2_LL AND
       NOT bAlarm_P_H2_HH AND NOT bAlarm_P_H2_LL AND NOT bAlarm_H2_in_Cl2_HH AND NOT bEmergencyStop THEN
        bFirstOutLatched := FALSE;
        dwFirstOutCapturedCode := 16#00000000;
    END_IF;
END_IF;

dwFirstOutWord := dwFirstOutCapturedCode;

(* ---------------------------------------------------------------------------------------------------- *)
(* Assemble 32-Bit Bit-Packed Telemetry & Diagnostic Status Words                                       *)
(* ---------------------------------------------------------------------------------------------------- *)
(* 1. Status Word 1: Operational States, Interlocks & Actuator Discretes *)
dwStatusWord1 := 16#00000000;
dwStatusWord1 := dwStatusWord1 OR INT_TO_DWORD(eState); (* Bits 0..3: Active State *)
IF bEnable THEN dwStatusWord1 := dwStatusWord1 OR 16#00000010; END_IF; (* Bit 4: Enable *)
IF bAutoCycleStart THEN dwStatusWord1 := dwStatusWord1 OR 16#00000020; END_IF; (* Bit 5: Auto Start *)
IF bRectifierOnlineFeedback THEN dwStatusWord1 := dwStatusWord1 OR 16#00000040; END_IF; (* Bit 6: Rectifier Online *)
IF bAnolyteRecircPumpRunning THEN dwStatusWord1 := dwStatusWord1 OR 16#00000080; END_IF; (* Bit 7: Anolyte Pump *)
IF bCausticRecircPumpRunning THEN dwStatusWord1 := dwStatusWord1 OR 16#00000100; END_IF; (* Bit 8: Caustic Pump *)
IF bValve_EmergencyScrubberVent THEN dwStatusWord1 := dwStatusWord1 OR 16#00000200; END_IF; (* Bit 9: Scrubber Vent *)
IF bValve_EmergencyH2VentStack THEN dwStatusWord1 := dwStatusWord1 OR 16#00000400; END_IF; (* Bit 10: H2 Vent *)
IF bValve_N2_AnolytePurge THEN dwStatusWord1 := dwStatusWord1 OR 16#00000800; END_IF; (* Bit 11: N2 Anolyte Purge *)
IF bValve_N2_CatholytePurge THEN dwStatusWord1 := dwStatusWord1 OR 16#00001000; END_IF; (* Bit 12: N2 Catholyte Purge *)
IF bRectifier_TripInterlock THEN dwStatusWord1 := dwStatusWord1 OR 16#00002000; END_IF; (* Bit 13: Rectifier Interlock *)
IF bElectrolyzerIsolateValves THEN dwStatusWord1 := dwStatusWord1 OR 16#00004000; END_IF; (* Bit 14: Skid Isolate *)
IF bBrinePreheaterSteamValve THEN dwStatusWord1 := dwStatusWord1 OR 16#00008000; END_IF; (* Bit 15: Steam Preheater *)
IF bCausticCoolerWaterValve THEN dwStatusWord1 := dwStatusWord1 OR 16#00010000; END_IF; (* Bit 16: Caustic Cooler *)
IF bMpcManualOverride THEN dwStatusWord1 := dwStatusWord1 OR 16#00020000; END_IF; (* Bit 17: MPC Manual *)
IF bNitrogenPurgePermissive THEN dwStatusWord1 := dwStatusWord1 OR 16#00040000; END_IF; (* Bit 18: N2 Permissive *)
IF bChlorineAbsorptionReady THEN dwStatusWord1 := dwStatusWord1 OR 16#00080000; END_IF; (* Bit 19: Scrubber Ready *)
IF bHydrogenVentStackReady THEN dwStatusWord1 := dwStatusWord1 OR 16#00100000; END_IF; (* Bit 20: Flare Ready *)
IF bDeminWaterSupplyPermissive THEN dwStatusWord1 := dwStatusWord1 OR 16#00200000; END_IF; (* Bit 21: Demin Ready *)

(* 2. Status Word 2: 2oo3 TMR Sensor Health, Degraded Modes & Cyber-Physical Diagnostics *)
dwStatusWord2 := 16#00000000;
IF bPDT_Cell_DP_HealthA THEN dwStatusWord2 := dwStatusWord2 OR 16#00000001; END_IF; (* Bit 0: DP 1A Health *)
IF bPDT_Cell_DP_HealthB THEN dwStatusWord2 := dwStatusWord2 OR 16#00000002; END_IF; (* Bit 1: DP 1B Health *)
IF bPDT_Cell_DP_HealthC THEN dwStatusWord2 := dwStatusWord2 OR 16#00000004; END_IF; (* Bit 2: DP 1C Health *)
IF bPDT_Cell_DP_Degraded THEN dwStatusWord2 := dwStatusWord2 OR 16#00000008; END_IF; (* Bit 3: DP Degraded 2oo2 *)
IF bPDT_Cell_DP_SingleFallback THEN dwStatusWord2 := dwStatusWord2 OR 16#00000010; END_IF; (* Bit 4: DP Single Fallback *)
IF bPT_Cl2_Header_Degraded THEN dwStatusWord2 := dwStatusWord2 OR 16#00000020; END_IF; (* Bit 5: Cl2 Degraded *)
IF bPT_Cl2_Header_SingleFallback THEN dwStatusWord2 := dwStatusWord2 OR 16#00000040; END_IF; (* Bit 6: Cl2 Fallback *)
IF bPT_H2_Header_Degraded THEN dwStatusWord2 := dwStatusWord2 OR 16#00000080; END_IF; (* Bit 7: H2 Degraded *)
IF bPT_H2_Header_SingleFallback THEN dwStatusWord2 := dwStatusWord2 OR 16#00000100; END_IF; (* Bit 8: H2 Fallback *)
IF bAT_H2_in_Cl2_Degraded THEN dwStatusWord2 := dwStatusWord2 OR 16#00000200; END_IF; (* Bit 9: Photometer Degraded *)
IF bAT_H2_in_Cl2_SingleFallback THEN dwStatusWord2 := dwStatusWord2 OR 16#00000400; END_IF; (* Bit 10: Photometer Fallback *)
IF bAT_Anolyte_NaCl_Degraded THEN dwStatusWord2 := dwStatusWord2 OR 16#00000800; END_IF; (* Bit 11: Brine Degraded *)
IF bAT_Catholyte_NaOH_Degraded THEN dwStatusWord2 := dwStatusWord2 OR 16#00001000; END_IF; (* Bit 12: Caustic Degraded *)
IF ABS(vecInnov[0]) < 1.00 AND ABS(vecInnov[1]) < 0.020 THEN dwStatusWord2 := dwStatusWord2 OR 16#00002000; END_IF; (* Bit 13: Observer Converged *)
IF rMpc_CostFunction_Val < 500.0 THEN dwStatusWord2 := dwStatusWord2 OR 16#00004000; END_IF; (* Bit 14: MPC Converged *)

(* 3. Alarm Word 1: ISA-18.2 Critical Emergency Trips & Safety Interlocks (HH/LL) *)
dwAlarmWord1 := 16#00000000;
IF bAlarm_DP_HH THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000001; END_IF; (* Bit 0: DP HH Trip *)
IF bAlarm_DP_LL THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000002; END_IF; (* Bit 1: DP LL Trip *)
IF bAlarm_P_Cl2_HH THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000004; END_IF; (* Bit 2: Cl2 HH Trip *)
IF bAlarm_P_Cl2_LL THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000008; END_IF; (* Bit 3: Cl2 LL Trip *)
IF bAlarm_P_H2_HH THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000010; END_IF; (* Bit 4: H2 HH Trip *)
IF bAlarm_P_H2_LL THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000020; END_IF; (* Bit 5: H2 LL Trip *)
IF bAlarm_H2_in_Cl2_HH THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000040; END_IF; (* Bit 6: H2 in Cl2 HH Trip *)
IF bAlarm_Brine_LL THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000080; END_IF; (* Bit 7: Brine LL Trip *)
IF bAlarm_Caustic_HH THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000100; END_IF; (* Bit 8: Caustic HH Trip *)
IF bAlarm_Temp_HH THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000200; END_IF; (* Bit 9: Temp HH Trip *)
IF bAlarm_Volt_HH THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000400; END_IF; (* Bit 10: Volt HH Trip *)
IF bAlarm_Volt_LL THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000800; END_IF; (* Bit 11: Volt LL Trip *)
IF bPDT_Cell_DP_Trip THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00001000; END_IF; (* Bit 12: DP TMR Sensor Trip *)
IF bPT_Cl2_Header_Trip THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00002000; END_IF; (* Bit 13: Cl2 TMR Sensor Trip *)
IF bPT_H2_Header_Trip THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00004000; END_IF; (* Bit 14: H2 TMR Sensor Trip *)
IF bAT_H2_in_Cl2_Trip THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00008000; END_IF; (* Bit 15: Photometer Sensor Trip *)
IF bEmergencyStop THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00010000; END_IF; (* Bit 16: E-Stop Trip *)

(* 4. Alarm Word 2: ISA-18.2 Warning Deviations & Sensor Discrepancies (H/L) *)
dwAlarmWord2 := 16#00000000;
IF bAlarm_DP_H THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000001; END_IF; (* Bit 0: DP High Warning *)
IF bAlarm_DP_L THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000002; END_IF; (* Bit 1: DP Low Warning *)
IF bAlarm_P_Cl2_H THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000004; END_IF; (* Bit 2: Cl2 High Warning *)
IF bAlarm_P_Cl2_L THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000008; END_IF; (* Bit 3: Cl2 Low Warning *)
IF bAlarm_P_H2_H THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000010; END_IF; (* Bit 4: H2 High Warning *)
IF bAlarm_P_H2_L THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000020; END_IF; (* Bit 5: H2 Low Warning *)
IF bAlarm_H2_in_Cl2_H THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000040; END_IF; (* Bit 6: H2 in Cl2 Warning *)
IF bAlarm_Brine_HH THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000080; END_IF; (* Bit 7: Brine High-High *)
IF bAlarm_Brine_H THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000100; END_IF; (* Bit 8: Brine High Advisory *)
IF bAlarm_Brine_L THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000200; END_IF; (* Bit 9: Brine Low Warning *)
IF bAlarm_Caustic_H THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000400; END_IF; (* Bit 10: Caustic High Warning *)
IF bAlarm_Caustic_L THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000800; END_IF; (* Bit 11: Caustic Low Warning *)
IF bAlarm_Caustic_LL THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00001000; END_IF; (* Bit 12: Caustic Low-Low *)
IF bAlarm_Temp_H THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00002000; END_IF; (* Bit 13: Temp High Warning *)
IF bAlarm_Temp_L THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00004000; END_IF; (* Bit 14: Temp Low Warning *)
IF bAlarm_Volt_H THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00008000; END_IF; (* Bit 15: Volt High Warning *)
IF bAlarm_Volt_L THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00010000; END_IF; (* Bit 16: Volt Low Advisory *)
IF rPDT_Cell_DP_Disc_AB_ms > 200.0 THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00020000; END_IF; (* Bit 17: DP AB Discrepancy *)
IF rPDT_Cell_DP_Disc_BC_ms > 200.0 THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00040000; END_IF; (* Bit 18: DP BC Discrepancy *)
IF rPDT_Cell_DP_Disc_CA_ms > 200.0 THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00080000; END_IF; (* Bit 19: DP CA Discrepancy *)

(* Cyclic Execution Scan Counter Increment *)
iCycleCounter := iCycleCounter + 1;

END_FUNCTION_BLOCK
