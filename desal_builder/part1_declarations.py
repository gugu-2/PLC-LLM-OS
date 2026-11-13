# desal_builder/part1_declarations.py
# Declarations for FB_Water_Desalination_SWRO_EnergyRecoveryDevice

def get_part1_declarations():
    return """FUNCTION_BLOCK FB_Water_Desalination_SWRO_EnergyRecoveryDevice
(*
====================================================================================================
LUMINA CYBER-PHYSICAL AUTOMATION KERNEL - IEC 61131-3 STRUCTURED TEXT
SYSTEM: 50,000 m3/day SEAWATER REVERSE OSMOSIS (SWRO) INDUSTRIAL DESALINATION TRAIN
SUBSYSTEMS:
  - MULTI-STAGE HIGH PRESSURE CENTRIFUGAL FEED PUMP (HPP) SYSTEM (65 - 82 [bar])
  - ISOBARIC CERAMIC ROTARY ENERGY RECOVERY DEVICE (ERD / ERI PRESSURE EXCHANGER PX-300 ARRAY)
  - PX BOOSTER PUMP DIFFERENTIAL PRESSURE BALANCING (2.0 - 5.0 [bar])
  - POLARIZATION CONCENTRATION & DARCY-VAN 'T HOFF MEMBRANE FLUX OBSERVER
  - MODEL PREDICTIVE CONTROL (MPC) FOR SPECIFIC ENERGY CONSUMPTION (SEC [kWh/m3]) MINIMIZATION
  - 2oo3 TRIPLE MODULAR REDUNDANT (TMR) SENSOR VOTING SUITE WITH DEBOUNCE TIMERS
  - CONTINUOUS ORP REDOX / SODIUM BISULFITE (SBS) CHLORINE BREAKTHROUGH PROTECTION TRIP
  - DYNAMIC SCALING INDEX & STIFF-DAVIS / LANGELIER ANTISCALANT STOICHIOMETRIC DOSING
  - DETERMINISTIC 14-STAGE PRODUCTION, CIP CHEMICAL CLEANING & EMERGENCY DEPRESSURIZATION FSM
  - ISA-18.2 MULTI-TIER PROCESS ALARM HIERARCHY WITH BIT-PACKED STATUS WORDS
====================================================================================================
*)

VAR_INPUT
    (* Digital Control Commands & Master Permissives *)
    bEnable                         : BOOL;         (* System Master Execution Enable / Auto Mode Select [-] *)
    bStartCommand                   : BOOL;         (* Sequence Start Command from Central SCADA / DCS [-] *)
    bStopCommand                    : BOOL;         (* Controlled Sequence Stop & LP Permeate Flush Request [-] *)
    bEmergencyDepressurize          : BOOL;         (* Fast Emergency Depressurization (FED) Hardwired Pushbutton [-] *)
    bResetFault                     : BOOL;         (* Master Fault & Latch Reset Command [-] *)
    bAckAlarm                       : BOOL;         (* ISA-18.2 Process Alarm Acknowledge Pushbutton [-] *)
    bCipInitiate                    : BOOL;         (* Clean-In-Place (CIP) Membrane Chemical Soak Initiate [-] *)
    bCipTypeCaustic                 : BOOL;         (* CIP Chemistry Select: FALSE = Acid Soak, TRUE = Caustic/Alkaline [-] *)
    
    (* Primary 2oo3 TMR Channel A/B/C Raw Analog Transmitters *)
    (* Channel Group 1: Raw Seawater Intake Pressure PT-101A/B/C *)
    rPT_101A_IntakePressure_bar     : REAL;         (* LP Feed Intake Pressure Transmitter PT-101A [bar] *)
    rPT_101B_IntakePressure_bar     : REAL;         (* LP Feed Intake Pressure Transmitter PT-101B [bar] *)
    rPT_101C_IntakePressure_bar     : REAL;         (* LP Feed Intake Pressure Transmitter PT-101C [bar] *)
    
    (* Channel Group 2: HP Membrane Header Feed Pressure PT-201A/B/C *)
    rPT_201A_HpFeedPressure_bar     : REAL;         (* High Pressure Membrane Feed Header PT-201A [bar] *)
    rPT_201B_HpFeedPressure_bar     : REAL;         (* High Pressure Membrane Feed Header PT-201B [bar] *)
    rPT_201C_HpFeedPressure_bar     : REAL;         (* High Pressure Membrane Feed Header PT-201C [bar] *)
    
    (* Channel Group 3: Permeate Product Water Conductivity AT-301A/B/C *)
    rAT_301A_PermConductivity_uS    : REAL;         (* Combined Permeate Conductivity Analyzer AT-301A [uS/cm] *)
    rAT_301B_PermConductivity_uS    : REAL;         (* Combined Permeate Conductivity Analyzer AT-301B [uS/cm] *)
    rAT_301C_PermConductivity_uS    : REAL;         (* Combined Permeate Conductivity Analyzer AT-301C [uS/cm] *)
    
    (* Channel Group 4: Isobaric ERD High-Pressure Brine Flow FT-401A/B/C *)
    rFT_401A_ErdBrineFlow_m3h       : REAL;         (* HP Brine Reject to ERD PX Array FT-401A [m3/h] *)
    rFT_401B_ErdBrineFlow_m3h       : REAL;         (* HP Brine Reject to ERD PX Array FT-401B [m3/h] *)
    rFT_401C_ErdBrineFlow_m3h       : REAL;         (* HP Brine Reject to ERD PX Array FT-401C [m3/h] *)
    
    (* Channel Group 5: Feed Dechlorination ORP Analyzer AT-102A/B/C *)
    rAT_102A_FeedOrp_mV             : REAL;         (* Raw Water Redox ORP Chlorine Protection AT-102A [mV] *)
    rAT_102B_FeedOrp_mV             : REAL;         (* Raw Water Redox ORP Chlorine Protection AT-102B [mV] *)
    rAT_102C_FeedOrp_mV             : REAL;         (* Raw Water Redox ORP Chlorine Protection AT-102C [mV] *)
    
    (* Channel Group 6: ERD PX Booster Pump Discharge Pressure PT-501A/B/C *)
    rPT_501A_PxDischargePress_bar   : REAL;         (* ERD Booster Pump Discharge Manifold PT-501A [bar] *)
    rPT_501B_PxDischargePress_bar   : REAL;         (* ERD Booster Pump Discharge Manifold PT-501B [bar] *)
    rPT_501C_PxDischargePress_bar   : REAL;         (* ERD Booster Pump Discharge Manifold PT-501C [bar] *)

    (* Exogenous Seawater Quality & Hydraulic Disturbances *)
    rRawSeawaterTds_ppm             : REAL;         (* Raw Intake Seawater Total Dissolved Solids [ppm] *)
    rRawSeawaterTemp_degC           : REAL;         (* Raw Seawater Feed Temperature [deg C] *)
    rRawSeawaterPh                  : REAL;         (* Raw Seawater pH Level [pH] *)
    rRawSeawaterSdi15               : REAL;         (* 15-Minute Silt Density Index SDI-15 [-] *)
    rCartridgeFilterDp_bar          : REAL;         (* Micron Cartridge Pre-Filter Differential Pressure [bar] *)
    rErdLpBrineOutPress_bar         : REAL;         (* Low Pressure Brine Outfall Backpressure PT-402 [bar] *)
    rPermeateBackPressure_bar       : REAL;         (* Permeate Collector Header Backpressure PT-302 [bar] *)
    
    (* Actuator & Motor Electrical Power Telemetry Feedback *)
    rHppVfdOutputFreq_Hz            : REAL;         (* HP Feed Pump VFD Output Frequency Feedback [Hz] *)
    rHppMotorPower_kW               : REAL;         (* HP Feed Pump Motor Active Power Consumption [kW] *)
    rPxBpVfdOutputFreq_Hz           : REAL;         (* ERD Booster Pump VFD Output Frequency Feedback [Hz] *)
    rPxBpMotorPower_kW              : REAL;         (* ERD Booster Pump Motor Active Power Consumption [kW] *)
    rLpFeedPumpPower_kW             : REAL;         (* Raw Seawater Intake Low-Pressure Pump Active Power [kW] *)
    
    (* Mechanical Vibration & Bearing Temperature Safety Sensors *)
    rHppBearingTempDe_degC          : REAL;         (* HPP Drive-End Bearing RTD Temperature [deg C] *)
    rHppBearingTempNde_degC         : REAL;         (* HPP Non-Drive-End Bearing RTD Temperature [deg C] *)
    rHppVibrationRms_mms            : REAL;         (* HPP Radial Vibration Velocity Overall [mm/s] *)
    rPxBpVibrationRms_mms           : REAL;         (* PX Booster Pump Radial Vibration RMS [mm/s] *)
    
    (* Chemical Dosing Reagent Tank Levels *)
    rSbsDayTankLevel_pct            : REAL;         (* Sodium Bisulfite Solution Storage Level [%] *)
    rAntiscalantDayTankLevel_pct    : REAL;         (* Polyacrylic Antiscalant Reagent Storage Level [%] *)
    rCipChemicalTankLevel_pct       : REAL;         (* CIP Circulation Skid Neutralization Tank Level [%] *)
    rCipSolutionTemp_degC           : REAL;         (* CIP Cleaning Solution Bulk Temperature [deg C] *)
    rCipSolutionPh                  : REAL;         (* CIP Skid In-Line Recirculation pH Sensor [pH] *)
    
    (* Operational Setpoint Adjustments & Targets *)
    rTargetPermeateFlow_m3h         : REAL;         (* Target Permeate Production Rate Setpoint [m3/h] *)
    rTargetRecoveryRatio_pct        : REAL;         (* Target Volumetric System Recovery (38.0 - 45.0) [%] *)
    rMaxAllowableHpPress_bar        : REAL;         (* Maximum High-Pressure Interlock Limit [bar] *)
    rMaxPermeateConductivity_uS     : REAL          (* Maximum Allowable Permeate Salinity Threshold [uS/cm] *)
END_VAR

VAR_OUTPUT
    (* Actuator Frequency & Position Command References *)
    rHppVfdSpeedReference_Hz        : REAL;         (* High-Pressure Pump VFD Speed Reference Command [Hz] *)
    rPxBpVfdSpeedReference_Hz       : REAL;         (* ERD Booster Pump VFD Speed Reference Command [Hz] *)
    rBrineThrottleValveCmd_pct      : REAL;         (* High-Pressure Brine Backpressure Control Valve [%] *)
    rSbsDosingPumpStroke_pct        : REAL;         (* Sodium Bisulfite Metering Pump Speed/Stroke [%] *)
    rAntiscalantDosingStroke_pct    : REAL;         (* Antiscalant Chemical Metering Pump Speed/Stroke [%] *)
    rPermeateDivertValveCmd_pct     : REAL;         (* Permeate Dump-to-Outfall Divert Valve Command [%] *)
    rLpPermeateFlushPumpCmd_pct     : REAL;         (* Automatic LP Permeate Flush Pump VFD Command [%] *)
    rCipCirculationPumpCmd_pct      : REAL;         (* CIP Skid Chemical Recirculation Pump Speed [%] *)
    
    (* Discrete Motorized Isolation & Sequence Solenoid Valves *)
    bOpenLpFeedInletValve           : BOOL;         (* Low Pressure Intake Raw Seawater Isolation Valve [-] *)
    bOpenHpFeedHeaderValve          : BOOL;         (* HP Membrane Header Fast Isolation Block Valve [-] *)
    bOpenErdHpBrineValve            : BOOL;         (* ERD Isobaric PX HP Brine Reject Isolation Valve [-] *)
    bOpenErdLpSeawaterValve         : BOOL;         (* ERD LP Seawater Supply Flow Control Valve [-] *)
    bOpenFastDepressurizeDumpValve  : BOOL;         (* Emergency Fast Depressurization Rupture Dump Valve [-] *)
    bOpenPermeateProductValve       : BOOL;         (* Permeate Forward Delivery to Potable Storage [-] *)
    bOpenCipSuctionValve            : BOOL;         (* CIP Cleaning Skid Supply Isolation Valve [-] *)
    bOpenCipReturnValve             : BOOL;         (* CIP Cleaning Skid Return Recirculation Valve [-] *)
    
    (* Cyber-Physical Process Observers & Efficiency Telemetry *)
    rObservedNetDrivingPress_bar    : REAL;         (* Computed Membrane Net Driving Pressure (NDP) [bar] *)
    rObservedOsmoticPress_bar       : REAL;         (* Calculated Average Membrane Surface Osmotic Pressure [bar] *)
    rObservedMembraneFlux_LMH       : REAL;         (* Calculated Normalized Membrane Permeate Flux [LMH] *)
    rObservedPermeateFlow_m3h       : REAL;         (* Total Clean Permeate Production Rate [m3/h] *)
    rObservedBrineFlow_m3h          : REAL;         (* Total High Salinity Concentrate Reject Rate [m3/h] *)
    rObservedRecoveryRatio_pct      : REAL;         (* True Operating Volumetric Recovery Ratio [%] *)
    rObservedSpecificEnergy_kWh_m3  : REAL;         (* Real-Time Specific Energy Consumption SEC [kWh/m3] *)
    rObservedErdEnergyRecovery_pct  : REAL;         (* Isobaric ERD Hydraulic Pressure Transfer Efficiency [%] *)
    rObservedErdMixingRatio_pct     : REAL;         (* PX Volumetric Overflush / Internal Salinity Leak [%] *)
    rObservedMembranePermeability   : REAL;         (* Normalized Specific Permeability Kw [LMH/bar] *)
    rObservedScalingIndex_Lsi       : REAL;         (* Langelier / Stiff-Davis Concentrate Scaling Index [-] *)
    rObservedSaltRejection_pct      : REAL;         (* Overall Polyamide Membrane Salt Rejection Ratio [%] *)

    (* 2oo3 TMR Synthesized Voted Values for Control & Historian *)
    rVoted_PT101_IntakePress_bar    : REAL;         (* 2oo3 Voted Feed Intake Pressure [bar] *)
    rVoted_PT201_HpFeedPress_bar    : REAL;         (* 2oo3 Voted HP Membrane Feed Pressure [bar] *)
    rVoted_AT301_PermConduct_uS     : REAL;         (* 2oo3 Voted Permeate Conductivity [uS/cm] *)
    rVoted_FT401_ErdBrineFlow_m3h   : REAL;         (* 2oo3 Voted ERD Brine Reject Flow [m3/h] *)
    rVoted_AT102_FeedOrp_mV         : REAL;         (* 2oo3 Voted Feed Dechlorination ORP [mV] *)
    rVoted_PT501_PxDischPress_bar   : REAL;         (* 2oo3 Voted PX Booster Discharge Pressure [bar] *)

    (* Deterministic FSM Sequencer State & Timers *)
    nFsmCurrentState                : INT;          (* Active Deterministic Operational State (0 - 13) [-] *)
    sFsmStateName                   : STRING(32);   (* Descriptive ASCII State Identifier [-] *)
    rFsmStateElapsedTime_sec        : REAL;         (* Elapsed Time within Current Operating Stage [s] *)
    bSequenceComplete               : BOOL;         (* Operational Sequence Ready / Steady State Reached [-] *)
    bSystemRunning                  : BOOL;         (* SWRO Train Operating in Full Production Mode [-] *)
    bPermeateOffSpecDiverted        : BOOL;         (* Permeate Conductivity High -> Dump Valve Active [-] *)
    bCipCycleActive                 : BOOL;         (* Automated Membrane Chemical CIP Running [-] *)

    (* ISA-18.2 Bit-Packed Status & Diagnostic Words *)
    dwStatusWord                    : DWORD;        (* 32-Bit System Operational Mode & Subsystem Status *)
    dwAlarmWord1                    : DWORD;        (* 32-Bit High-High & Critical Safety Emergency Alarms *)
    dwAlarmWord2                    : DWORD;        (* 32-Bit Process Warnings, TMR Discordance & Fouling *)
    dwTripWord                      : DWORD;        (* 32-Bit First-Out Safety Trip Lockout Reason *)
    bCriticalTripActive             : BOOL;         (* Global Emergency Safety Trip Lockout Active [-] *)
    bWarningAlarmActive             : BOOL          (* Process Warning Condition Requiring Attention [-] *)
END_VAR

VAR
    (* Internal Initialization & System Execution Flags *)
    bInitialized                    : BOOL := FALSE;(* One-Shot System Memory & Matrix Initialized Flag *)
    nScanCounter                    : DINT := 0;    (* Execution Cycle Counter *)
    rCycleTime_sec                  : REAL := 0.01; (* Fixed Internal Scan Interval Ts = 10 [ms] *)
    
    (* -------------------------------------------------------------------------
       CYBER-PHYSICAL 8-STATE DISCRETE STATE-SPACE INTERNAL MATRICES
       State Vector x[k]:
         x[1]: HP Feed Pressure P_feed [bar] (60.0 - 82.0)
         x[2]: Membrane Net Driving Pressure NDP [bar] (10.0 - 28.0)
         x[3]: Membrane Permeate Flux J_v [LMH] (10.0 - 25.0)
         x[4]: Membrane Surface Osmotic Pressure Pi_bar [bar] (30.0 - 55.0)
         x[5]: ERD HP Brine Inlet Pressure P_erd [bar] (58.0 - 80.0)
         x[6]: ERD Rotor Mixing Salinity Delta_C_mix [ppm] (0.0 - 1500.0)
         x[7]: Permeate Product Conductivity C_perm [uS/cm] (100.0 - 600.0)
         x[8]: Membrane Specific Permeability Kw [LMH/bar] (0.8 - 2.2)
       Control Vector u[k]:
         u[1]: HPP VFD Output Frequency f_hpp [Hz] (30.0 - 60.0)
         u[2]: PX Booster VFD Frequency f_bp [Hz] (25.0 - 60.0)
         u[3]: Brine Reject Throttle Valve Pos V_brine [%] (10.0 - 100.0)
         u[4]: Antiscalant Pump Stroke f_as [%] (0.0 - 100.0)
         u[5]: Sodium Bisulfite Pump Stroke f_sbs [%] (0.0 - 100.0)
         u[6]: Permeate Flush Valve Pos V_flush [%] (0.0 - 100.0)
       Disturbance Vector d[k]:
         d[1]: Seawater TDS C_sea [ppm] (32000 - 45000)
         d[2]: Seawater Temperature T_sea [deg C] (12.0 - 35.0)
         d[3]: Intake Low Pressure P_intake [bar] (2.0 - 4.5)
         d[4]: Oxidation-Reduction Potential ORP [mV] (-50 to +600)
         d[5]: Silt Density Index SDI-15 [-] (0.5 - 5.0)
         d[6]: Seawater pH Level [-] (7.2 - 8.4)
       Output Vector y[k]:
         y[1]: HP Feed Pressure P_feed [bar]
         y[2]: Permeate Flow Q_perm [m3/h]
         y[3]: Brine Reject Flow Q_brine [m3/h]
         y[4]: Permeate Conductivity Cond_perm [uS/cm]
         y[5]: ERD Differential Pressure Delta_P_erd [bar]
         y[6]: Specific Energy Consumption SEC [kWh/m3]
       ------------------------------------------------------------------------- *)
    x_state                         : ARRAY[1..8] OF REAL;      (* Current Estimated State Vector *)
    x_hat                           : ARRAY[1..8] OF REAL;      (* Luenberger Corrected State Vector *)
    x_pred                          : ARRAY[1..8] OF REAL;      (* Prior Predicted State Vector *)
    x_ref                           : ARRAY[1..8] OF REAL;      (* Target State Reference Vector *)
    u_ctrl                          : ARRAY[1..6] OF REAL;      (* Current Applied Control Vector *)
    u_prev                          : ARRAY[1..6] OF REAL;      (* Previous Scan Control Vector *)
    u_mpc_opt                       : ARRAY[1..6] OF REAL;      (* MPC Optimal Unconstrained Vector *)
    d_dist                          : ARRAY[1..6] OF REAL;      (* Measured Exogenous Disturbance Vector *)
    y_meas                          : ARRAY[1..6] OF REAL;      (* Voted Sensor Measurement Vector *)
    y_est                           : ARRAY[1..6] OF REAL;      (* Estimated Physical Output Vector *)
    e_innov                         : ARRAY[1..6] OF REAL;      (* Luenberger Innovation Residual Vector *)

    (* State-Space Matrix Arrays *)
    matA                            : ARRAY[1..8, 1..8] OF REAL;(* Discrete System Transition Matrix (8x8) *)
    matB                            : ARRAY[1..8, 1..6] OF REAL;(* Control Input Distribution Matrix (8x6) *)
    matBd                           : ARRAY[1..8, 1..6] OF REAL;(* Exogenous Disturbance Matrix (8x6) *)
    matC                            : ARRAY[1..6, 1..8] OF REAL;(* Measurement Observation Matrix (6x8) *)
    matD                            : ARRAY[1..6, 1..6] OF REAL;(* Direct Feedthrough Matrix (6x6) *)
    matL                            : ARRAY[1..8, 1..6] OF REAL;(* Luenberger Observer Kalman Gain Matrix (8x6) *)

    (* Model Predictive Control (MPC) Cost Weighting & Horizon Arrays *)
    matQ                            : ARRAY[1..8, 1..8] OF REAL;(* State Tracking Quadratic Penalty Matrix *)
    matR                            : ARRAY[1..6, 1..6] OF REAL;(* Actuator Energy Quadratic Penalty Matrix *)
    matS                            : ARRAY[1..6, 1..6] OF REAL;(* Actuator Slew Rate Quadratic Penalty Matrix *)
    matP                            : ARRAY[1..8, 1..8] OF REAL;(* Terminal State Riccati Quadratic Penalty Matrix *)
    u_min                           : ARRAY[1..6] OF REAL;      (* Actuator Lower Box Constraints *)
    u_max                           : ARRAY[1..6] OF REAL;      (* Actuator Upper Box Constraints *)
    du_max                          : ARRAY[1..6] OF REAL;      (* Actuator Maximum Slew Rate Per Scan *)
    
    (* MPC Unrolled Trajectory Rollout Arrays (Np = 5, Nc = 3) *)
    x_rollout                       : ARRAY[1..5, 1..8] OF REAL;(* State Prediction Trajectory across Horizon *)
    u_horizon                       : ARRAY[1..3, 1..6] OF REAL;(* Planned Control Moves across Horizon *)
    grad_J                          : ARRAY[1..6] OF REAL;      (* Projected Gradient of Quadratic Cost Functional *)

    (* -------------------------------------------------------------------------
       2oo3 TRIPLE MODULAR REDUNDANCY (TMR) VOTING INTERNAL STRUCTURES
       ------------------------------------------------------------------------- *)
    (* Channel Group 1: PT-101 Feed Intake Pressure *)
    bHealthy_PT101A                 : BOOL;
    bHealthy_PT101B                 : BOOL;
    bHealthy_PT101C                 : BOOL;
    rTimer_PT101_AB_sec             : REAL := 0.0;
    rTimer_PT101_BC_sec             : REAL := 0.0;
    rTimer_PT101_CA_sec             : REAL := 0.0;
    bDiscrepancy_PT101              : BOOL := FALSE;
    bDegraded_PT101                 : BOOL := FALSE;
    rVoted_PT101_Prev               : REAL := 3.2;

    (* Channel Group 2: PT-201 HP Membrane Header Pressure *)
    bHealthy_PT201A                 : BOOL;
    bHealthy_PT201B                 : BOOL;
    bHealthy_PT201C                 : BOOL;
    rTimer_PT201_AB_sec             : REAL := 0.0;
    rTimer_PT201_BC_sec             : REAL := 0.0;
    rTimer_PT201_CA_sec             : REAL := 0.0;
    bDiscrepancy_PT201              : BOOL := FALSE;
    bDegraded_PT201                 : BOOL := FALSE;
    rVoted_PT201_Prev               : REAL := 65.0;

    (* Channel Group 3: AT-301 Permeate Conductivity *)
    bHealthy_AT301A                 : BOOL;
    bHealthy_AT301B                 : BOOL;
    bHealthy_AT301C                 : BOOL;
    rTimer_AT301_AB_sec             : REAL := 0.0;
    rTimer_AT301_BC_sec             : REAL := 0.0;
    rTimer_AT301_CA_sec             : REAL := 0.0;
    bDiscrepancy_AT301              : BOOL := FALSE;
    bDegraded_AT301                 : BOOL := FALSE;
    rVoted_AT301_Prev               : REAL := 250.0;

    (* Channel Group 4: FT-401 ERD HP Brine Reject Flow *)
    bHealthy_FT401A                 : BOOL;
    bHealthy_FT401B                 : BOOL;
    bHealthy_FT401C                 : BOOL;
    rTimer_FT401_AB_sec             : REAL := 0.0;
    rTimer_FT401_BC_sec             : REAL := 0.0;
    rTimer_FT401_CA_sec             : REAL := 0.0;
    bDiscrepancy_FT401              : BOOL := FALSE;
    bDegraded_FT401                 : BOOL := FALSE;
    rVoted_FT401_Prev               : REAL := 2500.0;

    (* Channel Group 5: AT-102 Raw Water ORP Chlorine Breakthrough *)
    bHealthy_AT102A                 : BOOL;
    bHealthy_AT102B                 : BOOL;
    bHealthy_AT102C                 : BOOL;
    rTimer_AT102_AB_sec             : REAL := 0.0;
    rTimer_AT102_BC_sec             : REAL := 0.0;
    rTimer_AT102_CA_sec             : REAL := 0.0;
    bDiscrepancy_AT102              : BOOL := FALSE;
    bDegraded_AT102                 : BOOL := FALSE;
    rVoted_AT102_Prev               : REAL := 150.0;

    (* Channel Group 6: PT-501 PX Booster Discharge Pressure *)
    bHealthy_PT501A                 : BOOL;
    bHealthy_PT501B                 : BOOL;
    bHealthy_PT501C                 : BOOL;
    rTimer_PT501_AB_sec             : REAL := 0.0;
    rTimer_PT501_BC_sec             : REAL := 0.0;
    rTimer_PT501_CA_sec             : REAL := 0.0;
    bDiscrepancy_PT501              : BOOL := FALSE;
    bDegraded_PT501                 : BOOL := FALSE;
    rVoted_PT501_Prev               : REAL := 68.0;

    (* -------------------------------------------------------------------------
       THERMODYNAMIC, HYDRAULIC & CHEMICAL MASS BALANCE CONSTANTS
       ------------------------------------------------------------------------- *)
    rTotalMembraneArea_m2           : REAL := 125000.0; (* 50,000 m3/day Nominal Membrane Active Surface Area [m2] *)
    rGasConstant_R_bar_L_mol_K      : REAL := 0.083144; (* Universal Gas Constant [bar.L/(mol.K)] *)
    rNaclMolecularWeight_g_mol      : REAL := 58.44;    (* Equivalent Monovalent Salt MW [g/mol] *)
    rCleanMembranePermeability_Kw0  : REAL := 1.85;     (* Baseline Clean Normalized Permeability [LMH/bar] *)
    rMembraneSaltPassingCoeff_B0    : REAL := 0.012;    (* Solute Mass Transfer Diffusion Constant [LMH] *)
    rArrheniusEnergyWater_K         : REAL := 2640.0;   (* Water Viscosity Arrhenius Temperature Factor [K] *)
    rArrheniusEnergySalt_K          : REAL := 1850.0;   (* Salt Diffusion Arrhenius Temperature Factor [K] *)
    rStandardTemp_K                 : REAL := 298.15;   (* Reference Calibration Temperature (25.0 C) [K] *)
    rConcentrationPolarizationConst : REAL := 0.68;     (* Mass Transfer Film Boundary Layer Coefficient *)

    (* Dynamic Process Intermediate Variables *)
    rFeedWaterTemp_K                : REAL;
    rWaterViscosityCorrectionFactor : REAL;
    rSaltDiffusionCorrectionFactor  : REAL;
    rOsmoticCoeff_phi               : REAL;
    rFeedOsmoticPressure_bar        : REAL;
    rConcentrateOsmoticPress_bar    : REAL;
    rAverageMembraneOsmotic_bar     : REAL;
    rConcentrationPolarizationBeta  : REAL;
    rDynamicNetDrivingPressure_bar  : REAL;
    rDynamicMembraneFlux_LMH        : REAL;
    rTotalPermeateVolumetricFlow    : REAL;
    rTotalBrineVolumetricFlow       : REAL;
    rVolumetricRecoveryRatio_calc   : REAL;
    rSaltPassageRatio_calc          : REAL;
    rDynamicPermeateTds_ppm         : REAL;
    rDynamicPermeateConductivity    : REAL;
    rErdHpPressureTransferCoeff     : REAL;
    rErdVolumetricOverflushRatio    : REAL;
    rErdMixingSalinityLeak_ppm      : REAL;
    rTotalHydraulicPower_kW         : REAL;
    rDynamicSpecificEnergy_kWh_m3   : REAL;
    rScalingIndex_S_DSI             : REAL;

    (* -------------------------------------------------------------------------
       DETERMINISTIC 14-STAGE PRODUCTION & CIP SEQUENCER REGISTERS
       ------------------------------------------------------------------------- *)
    nFsmState                       : INT := 0;     (* 0: STANDBY, 1: LP PRIME, 2: CHEM PRECOND, 3: LP FLUSH,
                                                       4: HP SOFT RAMP, 5: ERD ENGAGE, 6: ERD BP SYNC,
                                                       7: PERM PROD, 8: SALINITY FLUX TRIM, 9: ANTISCALANT AUTOTUNE,
                                                       10: SCHED LP FLUSH, 11: CIP ACID, 12: CIP CAUSTIC, 13: FED TRIP *)
    nFsmNextState                   : INT := 0;
    rFsmTimer_sec                   : REAL := 0.0;
    rFsmStepTimer_sec               : REAL := 0.0;
    nCipSubStep                     : INT := 0;
    rCipSubStepTimer_sec            : REAL := 0.0;
    bStateFirstScan                 : BOOL := TRUE;
    
    (* Controlled Slew & Soft-Ramp Integrators *)
    rHppRampTarget_Hz               : REAL := 0.0;
    rPxBpRampTarget_Hz              : REAL := 0.0;
    rBrineValveRampTarget_pct       : REAL := 100.0;
    rSbsDosingRampTarget_pct        : REAL := 0.0;
    rAntiscalantRampTarget_pct      : REAL := 0.0;

    (* -------------------------------------------------------------------------
       ISA-18.2 MULTI-TIER PROCESS ALARM LOGIC ENGINE REGISTERS & TIMERS
       ------------------------------------------------------------------------- *)
    (* Safety Trip Setpoints & Hysteresis *)
    rSp_PT201_Trip_HH_bar           : REAL := 83.5; (* High-High Membrane Feed Pressure Instant Trip [bar] *)
    rSp_PT201_Alarm_H_bar           : REAL := 78.5; (* High HP Feed Pressure Warning [bar] *)
    rSp_PT101_Trip_LL_bar           : REAL := 1.2;  (* Low-Low Intake Pressure Pump Cavitation Trip [bar] *)
    rSp_PT101_Alarm_L_bar           : REAL := 2.0;  (* Low Feed Intake Pressure Warning [bar] *)
    rSp_AT102_Trip_HH_mV            : REAL := 280.0;(* Chlorine Redox Breakthrough Hard Stop Trip [mV] *)
    rSp_AT102_Alarm_H_mV            : REAL := 220.0;(* Chlorine Redox Breakthrough Warning [mV] *)
    rSp_AT301_Alarm_HH_uS           : REAL := 550.0;(* High-High Permeate Salinity Divert Trip [uS/cm] *)
    rSp_AT301_Alarm_H_uS            : REAL := 420.0;(* High Permeate Salinity Warning [uS/cm] *)
    rSp_DP_Erd_Trip_HH_bar          : REAL := 4.8;  (* ERD Differential Pressure Rotor Stalling Trip [bar] *)
    rSp_HppBearingTemp_Trip_HH_degC : REAL := 95.0; (* HPP Bearing Temperature Hard Trip [deg C] *)
    rSp_HppVibration_Trip_HH_mms    : REAL := 7.5;  (* HPP Mechanical Vibration Hard Trip [mm/s] *)
    rAlarmHysteresis_bar            : REAL := 0.5;  (* Standard Deadband Hysteresis [bar] *)
    rAlarmHysteresis_mV             : REAL := 10.0; (* Standard Deadband Hysteresis [mV] *)
    rAlarmHysteresis_uS             : REAL := 15.0; (* Standard Deadband Hysteresis [uS/cm] *)

    (* Alarm Qualification Delay Timers *)
    rTimer_Trip_PT201_HH_sec        : REAL := 0.0;
    rTimer_Alarm_PT201_H_sec        : REAL := 0.0;
    rTimer_Trip_PT101_LL_sec        : REAL := 0.0;
    rTimer_Alarm_PT101_L_sec        : REAL := 0.0;
    rTimer_Trip_AT102_HH_sec        : REAL := 0.0;
    rTimer_Alarm_AT102_H_sec        : REAL := 0.0;
    rTimer_Alarm_AT301_HH_sec       : REAL := 0.0;
    rTimer_Alarm_AT301_H_sec        : REAL := 0.0;
    rTimer_Trip_DPErd_HH_sec        : REAL := 0.0;
    rTimer_Trip_BearingTemp_sec     : REAL := 0.0;
    rTimer_Trip_Vibration_sec       : REAL := 0.0;
    
    (* General Calculation Loop Iterators *)
    i                               : INT;
    j                               : INT;
    k                               : INT;
    m                               : INT;
    n                               : INT;
    rTempSum                        : REAL;
    rAlpha_pgd                      : REAL := 0.0025; (* PGD Optimization Step Size *)
    rCost_J                         : REAL;
    rDelta_u                        : REAL
END_VAR
"""
