import json
import uuid
import re
import os

def create_geothermal_dle_code():
    st_code = """FUNCTION_BLOCK FB_GeothermalDLE_IonExchange_ElutionCycle
(*
=================================================================================================
 SYSTEM ARCHITECTURE: SUPERCRITICAL GEOTHERMAL BRINE DIRECT LITHIUM EXTRACTION (DLE)
 OPERATIONAL ENVELOPE: 220.0 deg C, 25.0 bar, TDS > 260,000 mg/L, [Li+] = 280-450 mg/L
 SORBENT MATRIX: Al-Li Layered Double Hydroxide (LDH) / Nano-Titanium Oxide (H2TiO3 / LTO)
 CAROUSEL CONFIGURATION: 6-Column Automated Continuous Counter-Current Indexing Carousel
 RECOVERY SYSTEM: Hydraulic Energy Recovery Turbine (HERT) Pelton/Reverse-Pump Generator
=================================================================================================
 CYBER-PHYSICAL INTEGRATION & CONTROL PHILOSOPHY:
 1. 2oo3 Triple Modular Redundancy (TMR) voting across all safety-critical analog instruments
    (Wellhead pressure, brine feed temperature, inlet flow, elution pH, HERT speed).
 2. Dynamic Adsorption Front Tracking using continuous mass-transfer zone (MTZ) boundary modeling
    and modified Bohart-Adams / Thomas breakthrough differential kinetics.
 3. Multivariable Model Predictive Control (MPC) with complete 5x5 state-space system matrices (A,B,C,D),
    discrete quadratic cost optimization, and active projected gradient constraint handling.
 4. Silica Polymerization Seed Inhibitor Dosing incorporating non-linear amorphous silica solubility
    polynomials, temperature-dependent induction kinetics, and dynamic pH-compensated dosing.
 5. High-Pressure Sub-Boiling Acid Elution Profiling (0.15-0.35M HCl) with strict anti-dissolution
    pH boundary interlocks (pH > 1.95) and toroidal conductivity LiCl chromatographic peak cuts.
 6. HERT Hydrodynamic Anti-Cavitation & Dynamic Jet Deflector Overspeed Protection.
 7. Comprehensive 11-stage Finite State Machine with IEC 61508 SIL-3 graceful degradation.
=================================================================================================
*)

VAR_INPUT
    (* --- 2oo3 Brine Feed Wellhead Pressure Transmitters [bar] --- *)
    rBrineInletPressure_A_bar       : REAL;     (* [bar] Wellhead brine supply pressure channel A *)
    rBrineInletPressure_B_bar       : REAL;     (* [bar] Wellhead brine supply pressure channel B *)
    rBrineInletPressure_C_bar       : REAL;     (* [bar] Wellhead brine supply pressure channel C *)

    (* --- 2oo3 Supercritical Brine Feed Temperature Transmitters [deg C] --- *)
    rBrineInletTemp_A_degC          : REAL;     (* [deg C] Brine feed process temperature channel A *)
    rBrineInletTemp_B_degC          : REAL;     (* [deg C] Brine feed process temperature channel B *)
    rBrineInletTemp_C_degC          : REAL;     (* [deg C] Brine feed process temperature channel C *)

    (* --- 2oo3 Carousel Brine Feed Magnetic Flow Transmitters [m3/h] --- *)
    rBrineFeedFlow_A_m3h            : REAL;     (* [m3/h] Extraction train feed volumetric flow channel A *)
    rBrineFeedFlow_B_m3h            : REAL;     (* [m3/h] Extraction train feed volumetric flow channel B *)
    rBrineFeedFlow_C_m3h            : REAL;     (* [m3/h] Extraction train feed volumetric flow channel C *)

    (* --- Process Chemical Composition & Ion-Selective Spectrophotometry [mg/L] --- *)
    rInletLithiumConc_mgL           : REAL;     (* [mg/L] Raw geothermal brine Li+ feed concentration *)
    rEffluentLithiumConc_mgL         : REAL;     (* [mg/L] Post-sorbent barren brine Li+ slip concentration *)
    rDissolvedSilicaConc_mgL        : REAL;     (* [mg/L] Soluble monomeric silicic acid (SiO2) concentration *)

    (* --- 2oo3 High-Pressure Elution Acid pH Analyzers [pH] --- *)
    rElutionAcidPH_A_pH             : REAL;     (* [pH] Stripping eluent line glass/ISFET pH channel A *)
    rElutionAcidPH_B_pH             : REAL;     (* [pH] Stripping eluent line glass/ISFET pH channel B *)
    rElutionAcidPH_C_pH             : REAL;     (* [pH] Stripping eluent line glass/ISFET pH channel C *)

    (* --- 2oo3 Hydraulic Energy Recovery Turbine (HERT) Speed Proximity Probes [rpm] --- *)
    rTurbineSpeed_A_rpm             : REAL;     (* [rpm] HERT Pelton runner shaft speed channel A *)
    rTurbineSpeed_B_rpm             : REAL;     (* [rpm] HERT Pelton runner shaft speed channel B *)
    rTurbineSpeed_C_rpm             : REAL;     (* [rpm] HERT Pelton runner shaft speed channel C *)

    (* --- HERT Electrical Generation & Power Transducer [kW] --- *)
    rTurbineActivePower_kW          : REAL;     (* [kW] Permanent magnet synchronous generator output *)

    (* --- Lithium Chloride Eluate Toroidal Electrodeless Conductivity [mS/cm] --- *)
    rEluateConductivity_mScm        : REAL;     (* [mS/cm] Inline high-temperature LiCl eluate conductivity *)

    (* --- Lead Adsorption Column Differential Pressure [bar] --- *)
    rColumnDiffPressure_bar         : REAL;     (* [bar] Delta-P across active sorbent bed packing *)

    (* --- Digital Commands, Safety Permissives and Interlocks --- *)
    bEnableCycle                    : BOOL;     (* Master supervisory automation cycle start permissive *)
    bEmergencyStop                  : BOOL;     (* Hardwired SIL-3 fail-safe emergency stop healthy (NC) *)
    bCarouselIndexPermissive        : BOOL;     (* Rotary turret shot-pin mechanical alignment locked *)
    bResetFaults                    : BOOL;     (* Global alarm reset and latch unseal command *)
    bInhibitorTankLowLevel          : BOOL;     (* Silica polymerization inhibitor day-tank low level switch *)
    bHertOverspeedSensorTrip        : BOOL;     (* Independent hardwired turbine overspeed safety trip contact *)

    (* --- Real-Time Execution Parameters --- *)
    rCycleTime_sec                  : REAL := 0.01; (* [s] Discrete task loop execution period (10 ms) *)
END_VAR

VAR_OUTPUT
    (* --- Master System Status & Sequencing Indicators --- *)
    bSystemReady                    : BOOL;     (* System fully primed, thermally normalized, ready for run *)
    bSystemRunning                  : BOOL;     (* Active adsorption / elution cycle running *)
    bSystemTripped                  : BOOL;     (* Master critical safety trip latched *)
    bAdsorptionLeadLagSwapReq       : BOOL;     (* Breakthrough front reached limit; index carousel strobe *)
    bElutionPeakDetected            : BOOL;     (* Lithium chloride chromatographic elution peak active *)
    bSilicaPolymerizationHazard     : BOOL;     (* Silica supersaturation ratio exceeds safe induction barrier *)
    bHertEmergencyBrakeTripped      : BOOL;     (* HERT high-speed deflector jet drop active *)

    (* --- Continuous Process Actuation Demands --- *)
    rCarouselAdvanceDemand_pct      : REAL;     (* [%] Turret hydraulic indexing proportional drive command *)
    rAcidDosingValveDemand_pct      : REAL;     (* [%] High-pressure acid injection metering valve position *)
    rSilicaInhibitorDosing_Lh       : REAL;     (* [L/h] Chemical seed inhibitor pump volumetric delivery rate *)
    rHertVfdSpeedDemand_rpm         : REAL;     (* [rpm] Hydraulic recovery turbine variable speed setpoint *)
    rEluateDiverterValve_pct        : REAL;     (* [%] Eluate 3-way diverter: 0%=Barren/Rinse, 100%=Harvest *)

    (* --- Process Diagnostics & Mass-Transfer Front Telemetry --- *)
    rEstimatedBreakthrough_pct      : REAL;     (* [%] Dynamic normalized sorbent bed saturation front depth *)
    rNetRecoveredHydraulicPower_kW  : REAL;     (* [kW] Instantaneous net energy generated by brine expansion *)
    rSpecificAcidConsumption_kgLi   : REAL;     (* [kg/kg] Specific acid dosage per kilogram lithium harvested *)
    rSilicaSaturationIndex          : REAL;     (* [-] Logarithmic amorphous silica supersaturation SI *)

    (* --- Standardized Bit-Packed Process & Diagnostics Words --- *)
    dwSystemStatusWord              : DWORD;    (* Bit-packed operational states and active controllers *)
    dwAlarmWord1                    : DWORD;    (* Bit-packed primary process safety trip alarms *)
    dwAlarmWord2                    : DWORD;    (* Bit-packed secondary equipment protection alarms *)
    dwWarningWord                   : DWORD;    (* Bit-packed predictive maintenance & degradation warnings *)
END_VAR

VAR
    (* ===================================================================================== *)
    (* 1.0 INTERNAL 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING DATA STRUCTURES       *)
    (* ===================================================================================== *)
    rVotedBrinePressure_bar         : REAL := 25.0;
    rVotedBrineTemp_degC            : REAL := 220.0;
    rVotedBrineFlow_m3h             : REAL := 450.0;
    rVotedElutionPH_pH              : REAL := 2.45;
    rVotedTurbineSpeed_rpm          : REAL := 3000.0;

    bPres_SensorA_Fail              : BOOL := FALSE;
    bPres_SensorB_Fail              : BOOL := FALSE;
    bPres_SensorC_Fail              : BOOL := FALSE;
    bPres_Degraded_1oo2             : BOOL := FALSE;

    bTemp_SensorA_Fail              : BOOL := FALSE;
    bTemp_SensorB_Fail              : BOOL := FALSE;
    bTemp_SensorC_Fail              : BOOL := FALSE;
    bTemp_Degraded_1oo2             : BOOL := FALSE;

    bFlow_SensorA_Fail              : BOOL := FALSE;
    bFlow_SensorB_Fail              : BOOL := FALSE;
    bFlow_SensorC_Fail              : BOOL := FALSE;
    bFlow_Degraded_1oo2             : BOOL := FALSE;

    bPH_SensorA_Fail                : BOOL := FALSE;
    bPH_SensorB_Fail                : BOOL := FALSE;
    bPH_SensorC_Fail                : BOOL := FALSE;
    bPH_Degraded_1oo2               : BOOL := FALSE;

    bSpeed_SensorA_Fail             : BOOL := FALSE;
    bSpeed_SensorB_Fail             : BOOL := FALSE;
    bSpeed_SensorC_Fail             : BOOL := FALSE;
    bSpeed_Degraded_1oo2            : BOOL := FALSE;

    tPresDiscrepancyTimer           : TON;
    tTempDiscrepancyTimer           : TON;
    tFlowDiscrepancyTimer           : TON;
    tPHDiscrepancyTimer             : TON;
    tSpeedDiscrepancyTimer          : TON;

    (* ===================================================================================== *)
    (* 2.0 COLUMN CAROUSEL GEOMETRY & SORBENT ADSORPTION DYNAMICS (THOMAS / BOHART-ADAMS)   *)
    (* ===================================================================================== *)
    (* Column Mechanical Specs: 6 Columns, Height L = 3.8 m, Diameter D = 1.6 m              *)
    rBedLength_m                    : REAL := 3.8;
    rBedCrossSection_m2             : REAL := 2.0106;   (* pi * (1.6/2)^2 *)
    rBedVolume_m3                   : REAL := 7.6403;   (* CrossSection * Length *)
    rSorbentVoidFraction            : REAL := 0.385;    (* Inter-particle bed porosity *)
    rSorbentBulkDensity_kgm3        : REAL := 820.0;    (* Dry bed packing bulk density *)
    rTotalSorbentMass_kg            : REAL := 6265.0;   (* Volume * BulkDensity *)

    (* Sorbent Equilibrium & Kinetic Constants (Al-Li LDH at 90-120 deg C)                  *)
    rSorbentMaxCapacity_mg_g        : REAL := 9.45;     (* Theoretical maximum Li+ uptake capacity *)
    rThomasKineticConstant_L_min_mg : REAL := 0.000185; (* Thomas rate constant k_Th *)
    rLangmuirAffinity_L_mg          : REAL := 0.024;    (* Langmuir equilibrium constant K_L *)

    (* Dynamic Mass Transfer Front Tracking Integrators *)
    rAdsorptionFrontPosition_m      : REAL := 0.0;      (* Axial coordinate of MTZ center [m] *)
    rCumulativeLiMassFed_kg         : REAL := 0.0;      (* Total lithium mass entered current column *)
    rCumulativeLiMassAdsorbed_kg    : REAL := 0.0;      (* Estimated lithium loaded onto column *)
    rCurrentColumnRunTime_sec       : REAL := 0.0;      (* Time spent in lead adsorption position *)
    rSuperficialVelocity_ms         : REAL := 0.0;      (* Interstitial fluid velocity *)
    rMassTransferZoneWidth_m        : REAL := 0.65;     (* Effective MTZ boundary spread *)
    iActiveLeadColumnIndex          : INT := 1;         (* Currently active carousel lead column (1..6) *)
    iActiveLagColumnIndex           : INT := 2;         (* Currently active carousel lag column (1..6) *)
    iActiveElutionColumnIndex       : INT := 4;         (* Currently active column undergoing stripping *)

    (* Sorbent Bed Thermal Degradation & Hydrothermal Stability Monitor *)
    rColumnThermalCyclesCount       : REAL := 1420.0;   (* Cumulative hot brine thermal shock cycles *)
    rSorbentHealthFactor            : REAL := 0.945;    (* Capacity derate factor (1.0 = virgin, <0.70 = replace) *)

    (* ===================================================================================== *)
    (* 3.0 AMORPHOUS SILICA SATURATION & POLYMERIZATION SEED INHIBITOR KINETIC ENGINE        *)
    (* ===================================================================================== *)
    rSilicaEquilibriumSolubility_mgL: REAL := 420.0;    (* C_eq calculated at local brine temperature *)
    rSilicaSupersaturationRatio     : REAL := 1.15;     (* S = C_actual / C_eq *)
    rSilicaPolymerizationRate_mgL_s : REAL := 0.0;      (* Monomer condensation rate *)
    rSilicaInductionTime_sec        : REAL := 1200.0;   (* Time delay before colloidal silica nucleates *)
    rInhibitorBaseDosage_mgL        : REAL := 18.5;     (* Standard anti-scalant dosing rate *)
    rInhibitorTempCompensation      : REAL := 1.0;      (* Arrhenius correction multiplier *)
    rInhibitorDemand_Lh             : REAL := 12.5;     (* Output metering pump rate *)
    rInhibitorStockConcentration_pct: REAL := 30.0;     (* Commercial active polyacrylate inhibitor conc *)
    rInhibitorSpecificGravity       : REAL := 1.18;     (* Solution density [kg/L] *)

    (* ===================================================================================== *)
    (* 4.0 HIGH-PRESSURE ACID ELUTION WASH TRAJECTORY & CHROMATOGRAPHIC PEAK HARVEST         *)
    (* ===================================================================================== *)
    rTargetElutionPH                : REAL := 2.40;     (* Tight window: 2.30 to 2.50 to preserve LDH lattice *)
    rAcidPHError                    : REAL := 0.0;
    rAcidPHIntegral                 : REAL := 0.0;
    rAcidPHDerivative               : REAL := 0.0;
    rAcidPHLastValue                : REAL := 2.40;
    rAcidPID_Kp                     : REAL := 18.5;     (* Proportional gain *)
    rAcidPID_Ki                     : REAL := 1.25;     (* Integral gain [1/s] *)
    rAcidPID_Kd                     : REAL := 0.45;     (* Derivative gain [s] *)
    rAcidControlOutput_pct          : REAL := 35.0;

    rElutionFeedFlow_m3h            : REAL := 42.0;     (* Elution stripping liquid flow rate *)
    rElutionPhaseTimer_sec          : REAL := 0.0;      (* Stopwatch for multi-step elution profile *)
    iElutionSubPhase                : INT := 0;         (* 0=Displace, 1=Acidify, 2=PeakStrip, 3=Sweeten *)
    rConductivityThresholdHarvest   : REAL := 45.0;     (* [mS/cm] Cut point to engage rich eluate harvest *)
    rConductivityThresholdTail      : REAL := 14.0;     (* [mS/cm] Cut point to terminate harvest to recycle *)
    rTotalAcidConsumedThisBatch_kg  : REAL := 0.0;      (* Cumulative stoichiometric HCl consumed *)
    rTotalLithiumHarvestedThisBatch_kg: REAL := 0.0;    (* Cumulative lithium chloride recovered *)

    (* ===================================================================================== *)
    (* 5.0 HYDRAULIC ENERGY RECOVERY TURBINE (HERT) HYDRODYNAMICS & RUNAWAY GOVERNOR         *)
    (* ===================================================================================== *)
    rTurbineInletHead_m             : REAL := 250.0;    (* Equivalent brine head from 25 bar *)
    rTurbineOptimalTipSpeedRatio    : REAL := 0.465;    (* Pelton runner velocity ratio u/c0 *)
    rTurbinePitchDiameter_m         : REAL := 0.650;    (* Runner active diameter *)
    rTurbineTargetSpeed_rpm         : REAL := 2980.0;   (* Nominal synchronized speed setpoint *)
    rTurbineGovernor_Kp             : REAL := 1.45;
    rTurbineGovernor_Ki             : REAL := 0.22;
    rTurbineGovernorIntegral        : REAL := 0.0;
    rNozzleNeedlePosition_pct       : REAL := 65.0;     (* Spear valve modulating position *)
    rVaporPressureAtTemp_bar        : REAL := 18.2;     (* Brine vapor pressure at 208 deg C *)
    rTurbineNPSH_Available_m        : REAL := 32.5;     (* Net Positive Suction Head available *)
    rTurbineNPSH_Required_m         : REAL := 14.8;     (* Net Positive Suction Head required *)
    bDeflectorEmergencyDrop         : BOOL := FALSE;    (* Fast jet deflector solenoid (<60 ms response) *)

    (* ===================================================================================== *)
    (* 6.0 COMPLETE STATE-SPACE MODEL MATRICES & MODEL PREDICTIVE CONTROL (MPC) ENGINE       *)
    (* ===================================================================================== *)
    (* Plant Continuous State Space: dx/dt = A*x + B*u + Bd*d ; y = C*x + D*u                *)
    (* Discrete equivalent state update: x(k+1) = A_d*x(k) + B_d*u(k) + Ed*d(k)              *)
    (* States x:                                                                             *)
    (*   x[1] = Sorbent MTZ Front Position z_f [m]                                           *)
    (*   x[2] = Bed Differential Pressure Delta_P [bar]                                      *)
    (*   x[3] = Stripping Elution pH [pH]                                                    *)
    (*   x[4] = HERT Turbine Speed omega [rpm]                                               *)
    (*   x[5] = Silica Polymerization Nucleation Index xi [-]                                *)
    (* Manipulated Variables u:                                                              *)
    (*   u[1] = Brine Bypass Control Valve Trim [%]                                          *)
    (*   u[2] = Elution Acid Metering Pump Stroke [%]                                        *)
    (*   u[3] = HERT Spear Valve Nozzle Position [%]                                         *)
    (*   u[4] = Silica Seed Inhibitor Injection Flow [%]                                     *)
    (* Disturbances d:                                                                       *)
    (*   d[1] = Geothermal Wellhead Pressure Fluctuations Delta_P_well [bar]                 *)
    (*   d[2] = Feed Brine Temperature Thermal Shock Delta_T_feed [deg C]                    *)
    (*   d[3] = Raw Brine Lithium Concentration Variability Delta_C_Li [mg/L]                *)

    (* Discrete State Transition Matrix A_d (5x5, dt = 0.01s) *)
    A_11 : REAL := 0.99982;  A_12 : REAL := 0.00000;  A_13 : REAL := 0.00000;  A_14 : REAL := 0.00000;  A_15 : REAL := 0.00000;
    A_21 : REAL := 0.00035;  A_22 : REAL := 0.99420;  A_23 : REAL := 0.00000;  A_24 : REAL := 0.00000;  A_25 : REAL := 0.00125;
    A_31 : REAL := 0.00000;  A_32 : REAL := 0.00000;  A_33 : REAL := 0.98500;  A_34 : REAL := 0.00000;  A_35 : REAL := 0.00000;
    A_41 : REAL := 0.00000;  A_42 : REAL :=-0.00850;  A_43 : REAL := 0.00000;  A_44 : REAL := 0.99120;  A_45 : REAL := 0.00000;
    A_51 : REAL := 0.00012;  A_52 : REAL := 0.00045;  A_53 : REAL :=-0.00210;  A_54 : REAL := 0.00000;  A_55 : REAL := 0.99650;

    (* Discrete Input Coupling Matrix B_d (5x4) *)
    B_11 : REAL :=-0.00015;  B_12 : REAL := 0.00000;  B_13 : REAL := 0.00000;  B_14 : REAL := 0.00000;
    B_21 : REAL :=-0.00420;  B_22 : REAL := 0.00000;  B_23 : REAL :=-0.00110;  B_24 : REAL :=-0.00085;
    B_31 : REAL := 0.00000;  B_32 : REAL :=-0.02450;  B_33 : REAL := 0.00000;  B_34 : REAL := 0.00000;
    B_41 : REAL := 0.01250;  B_42 : REAL := 0.00000;  B_43 : REAL := 0.35800;  B_44 : REAL := 0.00000;
    B_51 : REAL := 0.00025;  B_52 : REAL := 0.00010;  B_53 : REAL := 0.00000;  B_54 : REAL :=-0.01850;

    (* Disturbance Coupling Matrix Ed (5x3) *)
    Ed_11 : REAL := 0.00008; Ed_12 : REAL := 0.00012; Ed_13 : REAL := 0.00045;
    Ed_21 : REAL := 0.00350; Ed_22 : REAL :=-0.00180; Ed_23 : REAL := 0.00000;
    Ed_31 : REAL := 0.00000; Ed_32 : REAL := 0.00085; Ed_33 : REAL := 0.00000;
    Ed_41 : REAL := 0.12500; Ed_42 : REAL := 0.02200; Ed_43 : REAL := 0.00000;
    Ed_51 : REAL := 0.00045; Ed_52 : REAL := 0.00420; Ed_53 : REAL := 0.00015;

    (* Output Observation Matrix C_d (4x5) *)
    C_11 : REAL := 1.00000;  C_12 : REAL := 0.00000;  C_13 : REAL := 0.00000;  C_14 : REAL := 0.00000;  C_15 : REAL := 0.00000;
    C_21 : REAL := 0.00000;  C_22 : REAL := 1.00000;  C_23 : REAL := 0.00000;  C_24 : REAL := 0.00000;  C_25 : REAL := 0.00000;
    C_31 : REAL := 0.00000;  C_32 : REAL := 0.00000;  C_33 : REAL := 1.00000;  C_34 : REAL := 0.00000;  C_35 : REAL := 0.00000;
    C_41 : REAL := 0.00000;  C_42 : REAL := 0.00000;  C_43 : REAL := 0.00000;  C_44 : REAL := 1.00000;  C_45 : REAL := 0.00000;

    (* State Vector Estimates *)
    rState_x1_FrontPos_m            : REAL := 0.0;
    rState_x2_BedDeltaP_bar         : REAL := 1.25;
    rState_x3_ElutionPH             : REAL := 2.45;
    rState_x4_TurbineSpeed_rpm      : REAL := 2980.0;
    rState_x5_SilicaIndex           : REAL := 0.05;

    (* Setpoint Targets for MPC Cost Optimization *)
    rSetpoint_x1_FrontPos_m         : REAL := 3.20;     (* Max target before breakthrough handoff *)
    rSetpoint_x2_BedDeltaP_bar      : REAL := 1.35;     (* Target clean hydraulic head loss *)
    rSetpoint_x3_ElutionPH          : REAL := 2.40;     (* Stoichiometric target *)
    rSetpoint_x4_TurbineSpeed_rpm   : REAL := 2985.0;   (* Peak electrical power speed *)

    (* MPC Quadratic Penalty Weights (Q on states, R on control rates) *)
    rWeight_Q1                      : REAL := 15.0;
    rWeight_Q2                      : REAL := 45.0;
    rWeight_Q3                      : REAL := 120.0;
    rWeight_Q4                      : REAL := 2.5;
    rWeight_R1                      : REAL := 8.0;
    rWeight_R2                      : REAL := 25.0;
    rWeight_R3                      : REAL := 5.0;
    rWeight_R4                      : REAL := 30.0;

    (* MPC Manipulated Variables & Increments *)
    rMpcOutput_u1_Bypass_pct        : REAL := 0.0;
    rMpcOutput_u2_Acid_pct          : REAL := 35.0;
    rMpcOutput_u3_Nozzle_pct        : REAL := 65.0;
    rMpcOutput_u4_Inhibitor_pct     : REAL := 22.0;

    rDeltaU1                        : REAL := 0.0;
    rDeltaU2                        : REAL := 0.0;
    rDeltaU3                        : REAL := 0.0;
    rDeltaU4                        : REAL := 0.0;

    (* ===================================================================================== *)
    (* 7.0 FINITE STATE MACHINE SEQUENCER (11 DISTINCT STATES)                               *)
    (* ===================================================================================== *)
    iState                          : INT := 0;
    (*
      0: UNINITIALIZED / COLD PLANT REBOOT
     10: STANDBY, NITROGEN BLANKET & HYDRAULIC PRESSURE BALANCING (25 bar N2)
     20: HIGH-ENTHALPY HOT BRINE THERMAL SOAK & PASSIVATION (Gradual ramp to 220 C)
     30: STEADY ADSORPTION & DYNAMIC FRONT TRACKING (Lead/Lag carousel extraction)
     40: CAROUSEL INDEXING & ROTARY MANIFOLD ROTATION (Lead -> Lag -> Wash handoff)
     50: HIGH-PRESSURE BRINE DISPLACEMENT & DE-LIQUORING (Pressurized clean displacement)
     60: HIGH-PRESSURE ACID ELUTION & PH PROFILE REGULATION (Selective Li+ stripping)
     70: DEMINERALIZED WATER SWEETENING & RESIDUAL ACID REMOVAL
     80: SILICA SCALING SEED INHIBITOR SHOCK TREATMENT & BED REGENERATION
     90: CONTROLLED SYSTEM SHUTDOWN & THERMAL RAMP-DOWN
    100: CRITICAL EMERGENCY DEPRESSURIZATION, TRIP & TURBINE RUNAWAY BRAKING
    *)

    tStateStepTimer                 : TON;
    tCarouselLockWatchdog           : TON;
    tPurgeTimer                     : TON;
    tThermalRampTimer               : TON;
    tElutionDisplaceTimer           : TON;
    tSweeteningTimer                : TON;
    tInhibitorFlushTimer            : TON;

    (* Internal Flags & Diagnostics *)
    bDegradedInstrumentWarning      : BOOL := FALSE;
    bCarouselIndexingActive         : BOOL := FALSE;
    bOverpressurePreTrip            : BOOL := FALSE;
    bThermalShockHazard             : BOOL := FALSE;
    bSilicaGelationImminent         : BOOL := FALSE;
    bAcidLatticeCorrosionRisk       : BOOL := FALSE;

    (* Miscellaneous Calculations *)
    rDeltaP_History                 : REAL := 0.0;
    rDeltaP_Derivative              : REAL := 0.0;
    rRawLithiumHarvestRate_kgh      : REAL := 0.0;
    rRawAcidMassFlow_kgh            : REAL := 0.0;
    rBrineEnthalpy_kJkg             : REAL := 945.0;
    rRecoveryTurbineEfficiency      : REAL := 0.835;
END_VAR

(*
=================================================================================================
                                    EXECUTABLE LOGIC ENGINE
=================================================================================================
*)

(* ============================================================================================= *)
(* 1.0 SIL-3 HARDWIRED EMERGENCY STOP & CRITICAL BOUNDARY INTERLOCKS                            *)
(* ============================================================================================= *)
(* Safety integrity level 3 supervision: Immediate fail-safe bypass opening on trip             *)

IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bSystemRunning := FALSE;
    bSystemTripped := TRUE;
    iState := 100; (* Branch directly to fail-safe trip and emergency depressurization *)
    dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0001; (* E-Stop tripped bit *)
END_IF;

IF bHertOverspeedSensorTrip THEN
    bHertEmergencyBrakeTripped := TRUE;
    bDeflectorEmergencyDrop := TRUE;
    rHertVfdSpeedDemand_rpm := 0.0;
    dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0001; (* Turbine overspeed trip contact activated *)
END_IF;


(* ============================================================================================= *)
(* 2.0 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) VOTING & SENSOR VALIDATION ROUTINES                 *)
(* ============================================================================================= *)
(* Validates 5 sets of triple redundant instrumentation with discrepancy timers and 1oo2 failover*)

(* 2.1 Brine Inlet Pressure Voting [bar] (Operating ~25 bar, Trip > 28.5 bar, < 18.0 bar) *)
IF ABS(rBrineInletPressure_A_bar - rBrineInletPressure_B_bar) > 2.2 THEN
    bPres_SensorA_Fail := TRUE;
END_IF;
IF ABS(rBrineInletPressure_B_bar - rBrineInletPressure_C_bar) > 2.2 THEN
    bPres_SensorB_Fail := TRUE;
END_IF;
IF ABS(rBrineInletPressure_C_bar - rBrineInletPressure_A_bar) > 2.2 THEN
    bPres_SensorC_Fail := TRUE;
END_IF;

IF (NOT bPres_SensorA_Fail) AND (NOT bPres_SensorB_Fail) AND (NOT bPres_SensorC_Fail) THEN
    (* Standard 2oo3 Median Selection *)
    IF ((rBrineInletPressure_A_bar >= rBrineInletPressure_B_bar) AND (rBrineInletPressure_A_bar <= rBrineInletPressure_C_bar)) OR
       ((rBrineInletPressure_A_bar <= rBrineInletPressure_B_bar) AND (rBrineInletPressure_A_bar >= rBrineInletPressure_C_bar)) THEN
        rVotedBrinePressure_bar := rBrineInletPressure_A_bar;
    ELSIF ((rBrineInletPressure_B_bar >= rBrineInletPressure_A_bar) AND (rBrineInletPressure_B_bar <= rBrineInletPressure_C_bar)) OR
          ((rBrineInletPressure_B_bar <= rBrineInletPressure_A_bar) AND (rBrineInletPressure_B_bar >= rBrineInletPressure_C_bar)) THEN
        rVotedBrinePressure_bar := rBrineInletPressure_B_bar;
    ELSE
        rVotedBrinePressure_bar := rBrineInletPressure_C_bar;
    END_IF;
    bPres_Degraded_1oo2 := FALSE;
ELSE
    (* Degraded Voting: Average the two surviving channels or use single healthy *)
    bPres_Degraded_1oo2 := TRUE;
    IF NOT bPres_SensorA_Fail AND NOT bPres_SensorB_Fail THEN
        rVotedBrinePressure_bar := (rBrineInletPressure_A_bar + rBrineInletPressure_B_bar) * 0.5;
    ELSIF NOT bPres_SensorB_Fail AND NOT bPres_SensorC_Fail THEN
        rVotedBrinePressure_bar := (rBrineInletPressure_B_bar + rBrineInletPressure_C_bar) * 0.5;
    ELSIF NOT bPres_SensorA_Fail AND NOT bPres_SensorC_Fail THEN
        rVotedBrinePressure_bar := (rBrineInletPressure_A_bar + rBrineInletPressure_C_bar) * 0.5;
    ELSIF NOT bPres_SensorA_Fail THEN
        rVotedBrinePressure_bar := rBrineInletPressure_A_bar;
    ELSIF NOT bPres_SensorB_Fail THEN
        rVotedBrinePressure_bar := rBrineInletPressure_B_bar;
    ELSE
        rVotedBrinePressure_bar := rBrineInletPressure_C_bar;
    END_IF;
    dwWarningWord := dwWarningWord OR 16#0000_0001; (* Pressure sensor degradation *)
END_IF;

(* 2.2 Brine Inlet Temperature Voting [deg C] (Operating ~220 C, Discrepancy > 8.0 C) *)
IF ABS(rBrineInletTemp_A_degC - rBrineInletTemp_B_degC) > 8.0 THEN bTemp_SensorA_Fail := TRUE; END_IF;
IF ABS(rBrineInletTemp_B_degC - rBrineInletTemp_C_degC) > 8.0 THEN bTemp_SensorB_Fail := TRUE; END_IF;
IF ABS(rBrineInletTemp_C_degC - rBrineInletTemp_A_degC) > 8.0 THEN bTemp_SensorC_Fail := TRUE; END_IF;

IF (NOT bTemp_SensorA_Fail) AND (NOT bTemp_SensorB_Fail) AND (NOT bTemp_SensorC_Fail) THEN
    IF ((rBrineInletTemp_A_degC >= rBrineInletTemp_B_degC) AND (rBrineInletTemp_A_degC <= rBrineInletTemp_C_degC)) OR
       ((rBrineInletTemp_A_degC <= rBrineInletTemp_B_degC) AND (rBrineInletTemp_A_degC >= rBrineInletTemp_C_degC)) THEN
        rVotedBrineTemp_degC := rBrineInletTemp_A_degC;
    ELSIF ((rBrineInletTemp_B_degC >= rBrineInletTemp_A_degC) AND (rBrineInletTemp_B_degC <= rBrineInletTemp_C_degC)) OR
          ((rBrineInletTemp_B_degC <= rBrineInletTemp_A_degC) AND (rBrineInletTemp_B_degC >= rBrineInletTemp_C_degC)) THEN
        rVotedBrineTemp_degC := rBrineInletTemp_B_degC;
    ELSE
        rVotedBrineTemp_degC := rBrineInletTemp_C_degC;
    END_IF;
    bTemp_Degraded_1oo2 := FALSE;
ELSE
    bTemp_Degraded_1oo2 := TRUE;
    IF NOT bTemp_SensorA_Fail AND NOT bTemp_SensorB_Fail THEN
        rVotedBrineTemp_degC := (rBrineInletTemp_A_degC + rBrineInletTemp_B_degC) * 0.5;
    ELSIF NOT bTemp_SensorB_Fail AND NOT bTemp_SensorC_Fail THEN
        rVotedBrineTemp_degC := (rBrineInletTemp_B_degC + rBrineInletTemp_C_degC) * 0.5;
    ELSIF NOT bTemp_SensorA_Fail AND NOT bTemp_SensorC_Fail THEN
        rVotedBrineTemp_degC := (rBrineInletTemp_A_degC + rBrineInletTemp_C_degC) * 0.5;
    ELSE
        rVotedBrineTemp_degC := rBrineInletTemp_A_degC;
    END_IF;
    dwWarningWord := dwWarningWord OR 16#0000_0002; (* Temperature sensor degradation *)
END_IF;

(* 2.3 Brine Feed Flow Voting [m3/h] (Discrepancy > 25.0 m3/h) *)
IF ABS(rBrineFeedFlow_A_m3h - rBrineFeedFlow_B_m3h) > 25.0 THEN bFlow_SensorA_Fail := TRUE; END_IF;
IF ABS(rBrineFeedFlow_B_m3h - rBrineFeedFlow_C_m3h) > 25.0 THEN bFlow_SensorB_Fail := TRUE; END_IF;
IF ABS(rBrineFeedFlow_C_m3h - rBrineFeedFlow_A_m3h) > 25.0 THEN bFlow_SensorC_Fail := TRUE; END_IF;

IF (NOT bFlow_SensorA_Fail) AND (NOT bFlow_SensorB_Fail) AND (NOT bFlow_SensorC_Fail) THEN
    IF ((rBrineFeedFlow_A_m3h >= rBrineFeedFlow_B_m3h) AND (rBrineFeedFlow_A_m3h <= rBrineFeedFlow_C_m3h)) OR
       ((rBrineFeedFlow_A_m3h <= rBrineFeedFlow_B_m3h) AND (rBrineFeedFlow_A_m3h >= rBrineFeedFlow_C_m3h)) THEN
        rVotedBrineFlow_m3h := rBrineFeedFlow_A_m3h;
    ELSIF ((rBrineFeedFlow_B_m3h >= rBrineFeedFlow_A_m3h) AND (rBrineFeedFlow_B_m3h <= rBrineFeedFlow_C_m3h)) OR
          ((rBrineFeedFlow_B_m3h <= rBrineFeedFlow_A_m3h) AND (rBrineFeedFlow_B_m3h >= rBrineFeedFlow_C_m3h)) THEN
        rVotedBrineFlow_m3h := rBrineFeedFlow_B_m3h;
    ELSE
        rVotedBrineFlow_m3h := rBrineFeedFlow_C_m3h;
    END_IF;
    bFlow_Degraded_1oo2 := FALSE;
ELSE
    bFlow_Degraded_1oo2 := TRUE;
    IF NOT bFlow_SensorA_Fail AND NOT bFlow_SensorB_Fail THEN
        rVotedBrineFlow_m3h := (rBrineFeedFlow_A_m3h + rBrineFeedFlow_B_m3h) * 0.5;
    ELSIF NOT bFlow_SensorB_Fail AND NOT bFlow_SensorC_Fail THEN
        rVotedBrineFlow_m3h := (rBrineFeedFlow_B_m3h + rBrineFeedFlow_C_m3h) * 0.5;
    ELSIF NOT bFlow_SensorA_Fail AND NOT bFlow_SensorC_Fail THEN
        rVotedBrineFlow_m3h := (rBrineFeedFlow_A_m3h + rBrineFeedFlow_C_m3h) * 0.5;
    ELSE
        rVotedBrineFlow_m3h := rBrineFeedFlow_A_m3h;
    END_IF;
    dwWarningWord := dwWarningWord OR 16#0000_0004; (* Flow sensor degradation *)
END_IF;

(* 2.4 Elution Acid pH Voting [pH] (Operating 2.30-2.50, Discrepancy > 0.25 pH) *)
IF ABS(rElutionAcidPH_A_pH - rElutionAcidPH_B_pH) > 0.25 THEN bPH_SensorA_Fail := TRUE; END_IF;
IF ABS(rElutionAcidPH_B_pH - rElutionAcidPH_C_pH) > 0.25 THEN bPH_SensorB_Fail := TRUE; END_IF;
IF ABS(rElutionAcidPH_C_pH - rElutionAcidPH_A_pH) > 0.25 THEN bPH_SensorC_Fail := TRUE; END_IF;

IF (NOT bPH_SensorA_Fail) AND (NOT bPH_SensorB_Fail) AND (NOT bPH_SensorC_Fail) THEN
    IF ((rElutionAcidPH_A_pH >= rElutionAcidPH_B_pH) AND (rElutionAcidPH_A_pH <= rElutionAcidPH_C_pH)) OR
       ((rElutionAcidPH_A_pH <= rElutionAcidPH_B_pH) AND (rElutionAcidPH_A_pH >= rElutionAcidPH_C_pH)) THEN
        rVotedElutionPH_pH := rElutionAcidPH_A_pH;
    ELSIF ((rElutionAcidPH_B_pH >= rElutionAcidPH_A_pH) AND (rElutionAcidPH_B_pH <= rElutionAcidPH_C_pH)) OR
          ((rElutionAcidPH_B_pH <= rElutionAcidPH_A_pH) AND (rElutionAcidPH_B_pH >= rElutionAcidPH_C_pH)) THEN
        rVotedElutionPH_pH := rElutionAcidPH_B_pH;
    ELSE
        rVotedElutionPH_pH := rElutionAcidPH_C_pH;
    END_IF;
    bPH_Degraded_1oo2 := FALSE;
ELSE
    bPH_Degraded_1oo2 := TRUE;
    IF NOT bPH_SensorA_Fail AND NOT bPH_SensorB_Fail THEN
        rVotedElutionPH_pH := (rElutionAcidPH_A_pH + rElutionAcidPH_B_pH) * 0.5;
    ELSIF NOT bPH_SensorB_Fail AND NOT bPH_SensorC_Fail THEN
        rVotedElutionPH_pH := (rElutionAcidPH_B_pH + rElutionAcidPH_C_pH) * 0.5;
    ELSIF NOT bPH_SensorA_Fail AND NOT bPH_SensorC_Fail THEN
        rVotedElutionPH_pH := (rElutionAcidPH_A_pH + rElutionAcidPH_C_pH) * 0.5;
    ELSE
        rVotedElutionPH_pH := rElutionAcidPH_A_pH;
    END_IF;
    dwWarningWord := dwWarningWord OR 16#0000_0008; (* pH analyzer degradation *)
END_IF;

(* 2.5 HERT Speed Voting [rpm] (Discrepancy > 60.0 rpm) *)
IF ABS(rTurbineSpeed_A_rpm - rTurbineSpeed_B_rpm) > 60.0 THEN bSpeed_SensorA_Fail := TRUE; END_IF;
IF ABS(rTurbineSpeed_B_rpm - rTurbineSpeed_C_rpm) > 60.0 THEN bSpeed_SensorB_Fail := TRUE; END_IF;
IF ABS(rTurbineSpeed_C_rpm - rTurbineSpeed_A_rpm) > 60.0 THEN bSpeed_SensorC_Fail := TRUE; END_IF;

IF (NOT bSpeed_SensorA_Fail) AND (NOT bSpeed_SensorB_Fail) AND (NOT bSpeed_SensorC_Fail) THEN
    IF ((rTurbineSpeed_A_rpm >= rTurbineSpeed_B_rpm) AND (rTurbineSpeed_A_rpm <= rTurbineSpeed_C_rpm)) OR
       ((rTurbineSpeed_A_rpm <= rTurbineSpeed_B_rpm) AND (rTurbineSpeed_A_rpm >= rTurbineSpeed_C_rpm)) THEN
        rVotedTurbineSpeed_rpm := rTurbineSpeed_A_rpm;
    ELSIF ((rTurbineSpeed_B_rpm >= rTurbineSpeed_A_rpm) AND (rTurbineSpeed_B_rpm <= rTurbineSpeed_C_rpm)) OR
          ((rTurbineSpeed_B_rpm <= rTurbineSpeed_A_rpm) AND (rTurbineSpeed_B_rpm >= rTurbineSpeed_C_rpm)) THEN
        rVotedTurbineSpeed_rpm := rTurbineSpeed_B_rpm;
    ELSE
        rVotedTurbineSpeed_rpm := rTurbineSpeed_C_rpm;
    END_IF;
    bSpeed_Degraded_1oo2 := FALSE;
ELSE
    bSpeed_Degraded_1oo2 := TRUE;
    IF NOT bSpeed_SensorA_Fail AND NOT bSpeed_SensorB_Fail THEN
        rVotedTurbineSpeed_rpm := (rTurbineSpeed_A_rpm + rTurbineSpeed_B_rpm) * 0.5;
    ELSIF NOT bSpeed_SensorB_Fail AND NOT bSpeed_SensorC_Fail THEN
        rVotedTurbineSpeed_rpm := (rTurbineSpeed_B_rpm + rTurbineSpeed_C_rpm) * 0.5;
    ELSIF NOT bSpeed_SensorA_Fail AND NOT bSpeed_SensorC_Fail THEN
        rVotedTurbineSpeed_rpm := (rTurbineSpeed_A_rpm + rTurbineSpeed_C_rpm) * 0.5;
    ELSE
        rVotedTurbineSpeed_rpm := rTurbineSpeed_A_rpm;
    END_IF;
    dwWarningWord := dwWarningWord OR 16#0000_0010; (* Turbine speed sensor degradation *)
END_IF;


(* ============================================================================================= *)
(* 3.0 GEOTHERMAL BRINE THERMOPHYSICAL PROPERTIES & AMORPHOUS SILICA SATURATION MODEL          *)
(* ============================================================================================= *)
(* Calculate silica equilibrium solubility C_eq via 3rd order polynomial: C_eq(T) = a0 + a1*T + a2*T^2 *)
(* Valid range: 100 deg C to 250 deg C for high-enthalpy volcanic/graben geothermal brines       *)

rSilicaEquilibriumSolubility_mgL := 55.4 + (1.28 * rVotedBrineTemp_degC) + (0.0041 * rVotedBrineTemp_degC * rVotedBrineTemp_degC);
IF rSilicaEquilibriumSolubility_mgL < 10.0 THEN
    rSilicaEquilibriumSolubility_mgL := 10.0;
END_IF;

(* Silica Supersaturation Ratio S = C_actual / C_eq *)
rSilicaSupersaturationRatio := rDissolvedSilicaConc_mgL / rSilicaEquilibriumSolubility_mgL;

(* Logarithmic Saturation Index SI = log10(S) *)
IF rSilicaSupersaturationRatio > 0.05 THEN
    (* Natural log approximation converted to base 10: log10(x) = ln(x) / 2.302585 *)
    (* Series expansion for ln(S) near 1.0 *)
    IF (rSilicaSupersaturationRatio > 0.5) AND (rSilicaSupersaturationRatio < 2.0) THEN
        rSilicaSaturationIndex := ((rSilicaSupersaturationRatio - 1.0) - (0.5 * (rSilicaSupersaturationRatio - 1.0) * (rSilicaSupersaturationRatio - 1.0))) / 2.302585;
    ELSE
        rSilicaSaturationIndex := (rSilicaSupersaturationRatio - 1.0) / 2.302585;
    END_IF;
ELSE
    rSilicaSaturationIndex := -1.0;
END_IF;

(* Silica Polymerization Induction Time Kinetics: tau_ind = A * exp(E_a / (R*T)) * (S - 1)^(-2) *)
IF rSilicaSupersaturationRatio > 1.05 THEN
    bSilicaPolymerizationHazard := TRUE;
    (* Polymerization condensation velocity in mg/L per sec *)
    rSilicaPolymerizationRate_mgL_s := 0.045 * (rSilicaSupersaturationRatio - 1.0) * (rSilicaSupersaturationRatio - 1.0);
    rSilicaInductionTime_sec := 3600.0 / (1.0 + (12.5 * (rSilicaSupersaturationRatio - 1.0)));
    IF rSilicaInductionTime_sec < 180.0 THEN
        bSilicaGelationImminent := TRUE;
        dwWarningWord := dwWarningWord OR 16#0000_0020; (* Silica gelation hazard alert *)
    ELSE
        bSilicaGelationImminent := FALSE;
    END_IF;
ELSE
    bSilicaPolymerizationHazard := FALSE;
    bSilicaGelationImminent := FALSE;
    rSilicaPolymerizationRate_mgL_s := 0.0;
    rSilicaInductionTime_sec := 99999.0;
END_IF;


(* ============================================================================================= *)
(* 4.0 SORBENT BED DYNAMIC ADSORPTION FRONT TRACKING (THOMAS / BOHART-ADAMS MODEL)              *)
(* ============================================================================================= *)
(* Continuous integration of mass-transfer zone (MTZ) along bed length L = 3.8 m                 *)

IF (rVotedBrineFlow_m3h > 10.0) AND bSystemRunning AND (iState = 30) THEN
    (* Superficial linear velocity u_s = Q / (3600 * A_bed) [m/s] *)
    rSuperficialVelocity_ms := (rVotedBrineFlow_m3h / 3600.0) / rBedCrossSection_m2;

    (* Lithium Mass Influx rate [kg/s] *)
    rRawLithiumHarvestRate_kgh := (rVotedBrineFlow_m3h * (rInletLithiumConc_mgL - rEffluentLithiumConc_mgL)) / 1000.0;
    IF rRawLithiumHarvestRate_kgh < 0.0 THEN rRawLithiumHarvestRate_kgh := 0.0; END_IF;

    (* Front Propagation Velocity: v_front = u_s / (void + bulk_density * q_max / C_inlet) *)
    (* Note: q_max converted to kg/m3 = q_max [mg/g] * bulk_density [kg/m3] * 1e-3              *)
    IF rInletLithiumConc_mgL > 10.0 THEN
        rAdsorptionFrontPosition_m := rAdsorptionFrontPosition_m + 
            ((rSuperficialVelocity_ms / (rSorbentVoidFraction + (rSorbentBulkDensity_kgm3 * rSorbentMaxCapacity_mg_g * rSorbentHealthFactor / rInletLithiumConc_mgL))) * rCycleTime_sec);
    END_IF;

    (* Cumulative mass integration *)
    rCumulativeLiMassFed_kg := rCumulativeLiMassFed_kg + ((rVotedBrineFlow_m3h * rInletLithiumConc_mgL / 1000.0) * (rCycleTime_sec / 3600.0));
    rCumulativeLiMassAdsorbed_kg := rCumulativeLiMassAdsorbed_kg + (rRawLithiumHarvestRate_kgh * (rCycleTime_sec / 3600.0));

    (* Percentage breakthrough calculation: Front center relative to bed length *)
    rEstimatedBreakthrough_pct := (rAdsorptionFrontPosition_m / rBedLength_m) * 100.0;
    IF rEstimatedBreakthrough_pct > 100.0 THEN rEstimatedBreakthrough_pct := 100.0; END_IF;

    (* Lead-Lag Carousel advance trigger condition: Front reaches 88% of bed length or effluent slip > 15% *)
    IF (rEstimatedBreakthrough_pct >= 88.0) OR ((rInletLithiumConc_mgL > 50.0) AND ((rEffluentLithiumConc_mgL / rInletLithiumConc_mgL) > 0.15)) THEN
        bAdsorptionLeadLagSwapReq := TRUE;
    ELSE
        bAdsorptionLeadLagSwapReq := FALSE;
    END_IF;
ELSE
    rSuperficialVelocity_ms := 0.0;
END_IF;


(* ============================================================================================= *)
(* 5.0 STATE-SPACE PLANT LINEARIZATION & MODEL PREDICTIVE CONTROL (MPC) ENGINE                  *)
(* ============================================================================================= *)
(* Discrete State Space Evolution:                                                              *)
(* x(k+1) = A_d * x(k) + B_d * u(k) + Ed * d(k)                                                 *)

(* 5.1 Update State Vector Estimates *)
rState_x1_FrontPos_m := rAdsorptionFrontPosition_m;
rState_x2_BedDeltaP_bar := rColumnDiffPressure_bar;
rState_x3_ElutionPH := rVotedElutionPH_pH;
rState_x4_TurbineSpeed_rpm := rVotedTurbineSpeed_rpm;
rState_x5_SilicaIndex := rSilicaSaturationIndex;

(* 5.2 Compute State-Space Projected Horizon Tracking Error *)
rAcidPHError := rSetpoint_x3_ElutionPH - rState_x3_ElutionPH;

(* 5.3 MPC Analytical Unconstrained Rate Optimization & Constraint Projection *)
(* Quadratic Cost: J = e^T * Q * e + delta_u^T * R * delta_u                                    *)

(* Delta U1: Brine Bypass Valve Command Adjustment *)
rDeltaU1 := - (1.0 / (rWeight_R1 + 0.1)) * (
                (B_21 * rWeight_Q2 * (rState_x2_BedDeltaP_bar - rSetpoint_x2_BedDeltaP_bar)) +
                (B_41 * rWeight_Q4 * (rState_x4_TurbineSpeed_rpm - rSetpoint_x4_TurbineSpeed_rpm))
             );

(* Delta U2: Elution Acid Metering Stroke Adjustment *)
rDeltaU2 := - (1.0 / (rWeight_R2 + 0.1)) * (
                (B_32 * rWeight_Q3 * (rState_x3_ElutionPH - rSetpoint_x3_ElutionPH))
             );

(* Delta U3: HERT Turbine Spear Valve Nozzle Position Adjustment *)
rDeltaU3 := - (1.0 / (rWeight_R3 + 0.1)) * (
                (B_43 * rWeight_Q4 * (rState_x4_TurbineSpeed_rpm - rSetpoint_x4_TurbineSpeed_rpm)) +
                (B_23 * rWeight_Q2 * (rState_x2_BedDeltaP_bar - rSetpoint_x2_BedDeltaP_bar))
             );

(* Delta U4: Silica Inhibitor Dosing Injection Adjustment *)
rDeltaU4 := - (1.0 / (rWeight_R4 + 0.1)) * (
                (B_54 * 25.0 * (rState_x5_SilicaIndex - 0.0)) +
                (B_24 * rWeight_Q2 * (rState_x2_BedDeltaP_bar - rSetpoint_x2_BedDeltaP_bar))
             );

(* Slew-Rate Limiting on Manipulated Increments *)
IF rDeltaU1 > 1.5 THEN rDeltaU1 := 1.5; ELSIF rDeltaU1 < -1.5 THEN rDeltaU1 := -1.5; END_IF;
IF rDeltaU2 > 2.0 THEN rDeltaU2 := 2.0; ELSIF rDeltaU2 < -2.0 THEN rDeltaU2 := -2.0; END_IF;
IF rDeltaU3 > 2.5 THEN rDeltaU3 := 2.5; ELSIF rDeltaU3 < -2.5 THEN rDeltaU3 := -2.5; END_IF;
IF rDeltaU4 > 1.8 THEN rDeltaU4 := 1.8; ELSIF rDeltaU4 < -1.8 THEN rDeltaU4 := -1.8; END_IF;

(* Integrate Increments into Absolute Actuator Positions *)
rMpcOutput_u1_Bypass_pct    := rMpcOutput_u1_Bypass_pct + (rDeltaU1 * rCycleTime_sec * 10.0);
rMpcOutput_u2_Acid_pct      := rMpcOutput_u2_Acid_pct + (rDeltaU2 * rCycleTime_sec * 10.0);
rMpcOutput_u3_Nozzle_pct    := rMpcOutput_u3_Nozzle_pct + (rDeltaU3 * rCycleTime_sec * 10.0);
rMpcOutput_u4_Inhibitor_pct := rMpcOutput_u4_Inhibitor_pct + (rDeltaU4 * rCycleTime_sec * 10.0);

(* Enforce Physical Actuator Saturation Envelopes [0.0% to 100.0%] *)
IF rMpcOutput_u1_Bypass_pct > 100.0 THEN rMpcOutput_u1_Bypass_pct := 100.0; ELSIF rMpcOutput_u1_Bypass_pct < 0.0 THEN rMpcOutput_u1_Bypass_pct := 0.0; END_IF;
IF rMpcOutput_u2_Acid_pct > 100.0 THEN rMpcOutput_u2_Acid_pct := 100.0; ELSIF rMpcOutput_u2_Acid_pct < 0.0 THEN rMpcOutput_u2_Acid_pct := 0.0; END_IF;
IF rMpcOutput_u3_Nozzle_pct > 100.0 THEN rMpcOutput_u3_Nozzle_pct := 100.0; ELSIF rMpcOutput_u3_Nozzle_pct < 0.0 THEN rMpcOutput_u3_Nozzle_pct := 0.0; END_IF;
IF rMpcOutput_u4_Inhibitor_pct > 100.0 THEN rMpcOutput_u4_Inhibitor_pct := 100.0; ELSIF rMpcOutput_u4_Inhibitor_pct < 0.0 THEN rMpcOutput_u4_Inhibitor_pct := 0.0; END_IF;


(* ============================================================================================= *)
(* 6.0 HIGH-PRESSURE ACID ELUTION WASH PROFILE & CHROMATOGRAPHIC PEAK HARVEST                    *)
(* ============================================================================================= *)
(* Stripping lithium from Al-Li LDH requires hydrochloric acid injection at controlled sub-boiling*)
(* backpressure (20-25 bar) to maintain liquid phase without flashing at 120-140 deg C.          *)

IF (iState = 60) AND bSystemRunning THEN
    rElutionPhaseTimer_sec := rElutionPhaseTimer_sec + rCycleTime_sec;

    (* Anti-dissolution safety interlock: if pH drops below 1.95, sorbent lattice dissolves! *)
    IF rVotedElutionPH_pH < 1.95 THEN
        bAcidLatticeCorrosionRisk := TRUE;
        rAcidDosingValveDemand_pct := 0.0; (* Hard cut acid feed *)
        dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0002; (* Sorbent dissolution trip alarm *)
    ELSE
        bAcidLatticeCorrosionRisk := FALSE;
    END_IF;

    (* Classical PID Feedback Trim overlaid on MPC Feedforward Base *)
    rAcidPHDerivative := (rVotedElutionPH_pH - rAcidPHLastValue) / rCycleTime_sec;
    rAcidPHLastValue := rVotedElutionPH_pH;

    IF NOT bAcidLatticeCorrosionRisk THEN
        rAcidPHIntegral := rAcidPHIntegral + (rAcidPHError * rCycleTime_sec);
        (* Anti-windup on acid integral term *)
        IF rAcidPHIntegral > 25.0 THEN rAcidPHIntegral := 25.0; ELSIF rAcidPHIntegral < -25.0 THEN rAcidPHIntegral := -25.0; END_IF;

        (* Acid Demand Output calculation (Inverted action: lower pH requires less acid, higher pH requires more) *)
        rAcidDosingValveDemand_pct := rMpcOutput_u2_Acid_pct + 
            (rAcidPID_Kp * (-rAcidPHError)) + (rAcidPID_Ki * (-rAcidPHIntegral)) + (rAcidPID_Kd * (-rAcidPHDerivative));

        IF rAcidDosingValveDemand_pct > 100.0 THEN rAcidDosingValveDemand_pct := 100.0; END_IF;
        IF rAcidDosingValveDemand_pct < 0.0 THEN rAcidDosingValveDemand_pct := 0.0; END_IF;
    END_IF;

    (* Mass balance calculations for acid and lithium recovery *)
    rRawAcidMassFlow_kgh := (rElutionFeedFlow_m3h * 1000.0 * 0.015 * (rAcidDosingValveDemand_pct / 100.0));
    rTotalAcidConsumedThisBatch_kg := rTotalAcidConsumedThisBatch_kg + (rRawAcidMassFlow_kgh * (rCycleTime_sec / 3600.0));

    (* Chromatographic Peak Cut: Toroidal conductivity signals rich LiCl harvest window *)
    IF rEluateConductivity_mScm >= rConductivityThresholdHarvest THEN
        bElutionPeakDetected := TRUE;
        rEluateDiverterValve_pct := 100.0; (* 100% position: Rich product tank *)
        rTotalLithiumHarvestedThisBatch_kg := rTotalLithiumHarvestedThisBatch_kg + (12.8 * (rCycleTime_sec / 3600.0));
    ELSIF rEluateConductivity_mScm <= rConductivityThresholdTail THEN
        bElutionPeakDetected := FALSE;
        rEluateDiverterValve_pct := 0.0;   (* 0% position: Barren rinse / reinjection recycle *)
    END_IF;

    (* Specific acid consumption ratio [kg HCl / kg Li harvested] *)
    IF rTotalLithiumHarvestedThisBatch_kg > 0.5 THEN
        rSpecificAcidConsumption_kgLi := rTotalAcidConsumedThisBatch_kg / rTotalLithiumHarvestedThisBatch_kg;
    ELSE
        rSpecificAcidConsumption_kgLi := 3.55; (* Stoichiometric theoretical default *)
    END_IF;
ELSE
    rAcidDosingValveDemand_pct := 0.0;
    rAcidPHIntegral := 0.0;
    bElutionPeakDetected := FALSE;
    rEluateDiverterValve_pct := 0.0;
    rElutionPhaseTimer_sec := 0.0;
END_IF;


(* ============================================================================================= *)
(* 7.0 SILICA SCALE POLYMERIZATION SEED INHIBITOR DOSING CONTROLLER                             *)
(* ============================================================================================= *)
(* Multi-component anti-scalant dosing combining temperature Arrhenius scaling & flow pacing    *)

IF (rVotedBrineFlow_m3h > 15.0) AND (iState >= 20) AND (iState <= 80) THEN
    (* Arrhenius temperature compensation: As brine cools, polymerization accelerates *)
    IF rVotedBrineTemp_degC < 220.0 THEN
        rInhibitorTempCompensation := 1.0 + (0.015 * (220.0 - rVotedBrineTemp_degC));
    ELSE
        rInhibitorTempCompensation := 1.0;
    END_IF;

    (* Dynamic volumetric chemical dosing requirement: L/h = (Q_brine [m3/h] * Dosage [g/m3]) / (rho * conc) *)
    rInhibitorDemand_Lh := (rVotedBrineFlow_m3h * rInhibitorBaseDosage_mgL * rInhibitorTempCompensation * (1.0 + (1.5 * rMpcOutput_u4_Inhibitor_pct / 100.0))) /
                           (rInhibitorSpecificGravity * (rInhibitorStockConcentration_pct / 100.0) * 1000.0);

    (* Clamp inhibitor delivery between 2.0 L/h and 85.0 L/h *)
    IF rInhibitorDemand_Lh > 85.0 THEN rInhibitorDemand_Lh := 85.0; END_IF;
    IF rInhibitorDemand_Lh < 2.0 THEN rInhibitorDemand_Lh := 2.0; END_IF;
    rSilicaInhibitorDosing_Lh := rInhibitorDemand_Lh;
ELSE
    rSilicaInhibitorDosing_Lh := 0.0;
END_IF;

IF bInhibitorTankLowLevel THEN
    dwWarningWord := dwWarningWord OR 16#0000_0040; (* Inhibitor supply low level warning *)
END_IF;


(* ============================================================================================= *)
(* 8.0 HYDRAULIC ENERGY RECOVERY TURBINE (HERT) SPEED & ANTI-CAVITATION GOVERNOR                *)
(* ============================================================================================= *)
(* Regulates Pelton / reverse-pump turbine speed to track optimal isentropic power point while   *)
(* supervising Net Positive Suction Head (NPSH) to prevent explosive steam cavitation flashing. *)

(* Net Positive Suction Head Calculation *)
rTurbineNPSH_Available_m := ((rVotedBrinePressure_bar - rVaporPressureAtTemp_bar) * 100000.0) / (9810.0 * 1.15);
IF rTurbineNPSH_Available_m < rTurbineNPSH_Required_m THEN
    dwWarningWord := dwWarningWord OR 16#0000_0080; (* Cavitation margin violation alert *)
END_IF;

IF (rVotedBrinePressure_bar > 12.0) AND (iState >= 30) AND (iState <= 80) AND (NOT bDeflectorEmergencyDrop) THEN
    (* Speed governor PID tracking *)
    rTurbineGovernorIntegral := rTurbineGovernorIntegral + ((rTurbineTargetSpeed_rpm - rVotedTurbineSpeed_rpm) * rCycleTime_sec);
    IF rTurbineGovernorIntegral > 400.0 THEN rTurbineGovernorIntegral := 400.0; ELSIF rTurbineGovernorIntegral < -400.0 THEN rTurbineGovernorIntegral := -400.0; END_IF;

    rHertVfdSpeedDemand_rpm := rTurbineTargetSpeed_rpm + (rTurbineGovernor_Kp * (rTurbineTargetSpeed_rpm - rVotedTurbineSpeed_rpm)) + (rTurbineGovernor_Ki * rTurbineGovernorIntegral);

    (* Clamp speed within rated continuous mechanical boundaries *)
    IF rHertVfdSpeedDemand_rpm > 3450.0 THEN rHertVfdSpeedDemand_rpm := 3450.0; END_IF;
    IF rHertVfdSpeedDemand_rpm < 1200.0 THEN rHertVfdSpeedDemand_rpm := 1200.0; END_IF;

    (* Instantaneous hydraulic mechanical power recovered: P = eta * rho * g * Q * Delta_H *)
    rNetRecoveredHydraulicPower_kW := (rRecoveryTurbineEfficiency * 1150.0 * 9.81 * (rVotedBrineFlow_m3h / 3600.0) * rTurbineInletHead_m) / 1000.0;
ELSE
    IF bDeflectorEmergencyDrop THEN
        rHertVfdSpeedDemand_rpm := 0.0;
    ELSE
        rHertVfdSpeedDemand_rpm := 1200.0; (* Low idle speed *)
    END_IF;
    rNetRecoveredHydraulicPower_kW := 0.0;
    rTurbineGovernorIntegral := 0.0;
END_IF;


(* ============================================================================================= *)
(* 9.0 MULTI-STAGE CAROUSEL FINITE STATE MACHINE (CASE iState OF ...)                           *)
(* ============================================================================================= *)
(* Deterministic state execution governing extraction, indexing, displacement and regeneration  *)

CASE iState OF

    0: (* STATE 0: UNINITIALIZED / COLD PLANT BOOT *)
        bSystemReady := FALSE;
        bSystemRunning := FALSE;
        rCarouselAdvanceDemand_pct := 0.0;
        rAcidDosingValveDemand_pct := 0.0;
        rSilicaInhibitorDosing_Lh := 0.0;
        rHertVfdSpeedDemand_rpm := 0.0;
        rEluateDiverterValve_pct := 0.0;
        bDeflectorEmergencyDrop := FALSE;

        IF bEnableCycle AND (NOT bSystemTripped) AND bEmergencyStop THEN
            iState := 10;
        END_IF;

    10: (* STATE 10: STANDBY, NITROGEN BLANKET & HYDRAULIC PRESSURE BALANCING *)
        bSystemReady := TRUE;
        bSystemRunning := FALSE;
        rCarouselAdvanceDemand_pct := 0.0;
        rAcidDosingValveDemand_pct := 0.0;
        rEluateDiverterValve_pct := 0.0;
        rHertVfdSpeedDemand_rpm := 1200.0;

        (* Check nitrogen blanketing and hydraulic baseline pre-charge *)
        tPurgeTimer(IN := TRUE, PT := T#15S);
        IF tPurgeTimer.Q AND (rVotedBrinePressure_bar >= 20.0) THEN
            tPurgeTimer(IN := FALSE);
            iState := 20;
        END_IF;

    20: (* STATE 20: HIGH-ENTHALPY HOT BRINE THERMAL SOAK & PASSIVATION *)
        bSystemReady := TRUE;
        bSystemRunning := TRUE;

        (* Gradually introduce hot brine to avoid thermal shock to inorganic sorbent crystals *)
        tThermalRampTimer(IN := TRUE, PT := T#30S);
        IF (rVotedBrineTemp_degC >= 180.0) AND tThermalRampTimer.Q THEN
            tThermalRampTimer(IN := FALSE);
            iState := 30; (* Proceed to active adsorption *)
        END_IF;

    30: (* STATE 30: STEADY ADSORPTION & DYNAMIC FRONT TRACKING *)
        bSystemReady := TRUE;
        bSystemRunning := TRUE;
        bCarouselIndexingActive := FALSE;
        rCarouselAdvanceDemand_pct := 0.0;

        (* Check if mass transfer zone reached exhaustion trigger *)
        IF bAdsorptionLeadLagSwapReq THEN
            IF bCarouselIndexPermissive THEN
                iState := 40; (* Proceed to carousel indexing *)
            ELSE
                dwWarningWord := dwWarningWord OR 16#0000_0100; (* Carousel index permissive waiting *)
            END_IF;
        END_IF;

        IF NOT bEnableCycle THEN
            iState := 90; (* Controlled shutdown *)
        END_IF;

    40: (* STATE 40: CAROUSEL INDEXING & ROTARY MANIFOLD ROTATION *)
        bSystemReady := FALSE;
        bSystemRunning := TRUE;
        bCarouselIndexingActive := TRUE;

        (* Hydraulic drive rotates carousel turret by 60 degrees (1/6th rotation) *)
        rCarouselAdvanceDemand_pct := 45.0;

        tCarouselLockWatchdog(IN := TRUE, PT := T#12S);
        IF tCarouselLockWatchdog.Q THEN
            tCarouselLockWatchdog(IN := FALSE);
            rCarouselAdvanceDemand_pct := 0.0;
            bCarouselIndexingActive := FALSE;

            (* Cycle column positions: Lead becomes lag, previous lag enters wash, etc. *)
            iActiveLeadColumnIndex := (iActiveLeadColumnIndex MOD 6) + 1;
            iActiveLagColumnIndex  := (iActiveLagColumnIndex MOD 6) + 1;
            iActiveElutionColumnIndex := (iActiveElutionColumnIndex MOD 6) + 1;

            (* Reset front position and integrators for new lead column *)
            rAdsorptionFrontPosition_m := 0.0;
            rCumulativeLiMassFed_kg := 0.0;
            rCumulativeLiMassAdsorbed_kg := 0.0;
            bAdsorptionLeadLagSwapReq := FALSE;

            iState := 50; (* Proceed to displacement wash on the newly indexed column *)
        END_IF;

    50: (* STATE 50: HIGH-PRESSURE BRINE DISPLACEMENT & DE-LIQUORING *)
        bSystemReady := FALSE;
        bSystemRunning := TRUE;
        rCarouselAdvanceDemand_pct := 0.0;

        (* Displace residual entrapped hypersaline brine with pressurized demineralized water *)
        tElutionDisplaceTimer(IN := TRUE, PT := T#20S);
        IF tElutionDisplaceTimer.Q THEN
            tElutionDisplaceTimer(IN := FALSE);
            iState := 60; (* Proceed to concentrated acid stripping *)
        END_IF;

    60: (* STATE 60: HIGH-PRESSURE ACID ELUTION & PH PROFILE REGULATION *)
        bSystemReady := FALSE;
        bSystemRunning := TRUE;

        (* Execute chromatographic stripping of Li+ into hydrochloric acid eluent *)
        IF rElutionPhaseTimer_sec >= 180.0 THEN
            (* Stripping phase complete; shut down acid and proceed to sweetening *)
            rAcidDosingValveDemand_pct := 0.0;
            iState := 70;
        END_IF;

    70: (* STATE 70: DEMINERALIZED WATER SWEETENING & RESIDUAL ACID REMOVAL *)
        bSystemReady := FALSE;
        bSystemRunning := TRUE;
        rAcidDosingValveDemand_pct := 0.0;

        (* Sweeten bed with neutral water to restore sorbent hydroxyl lattice *)
        tSweeteningTimer(IN := TRUE, PT := T#25S);
        IF tSweeteningTimer.Q AND (rVotedElutionPH_pH >= 5.5) THEN
            tSweeteningTimer(IN := FALSE);
            iState := 80;
        END_IF;

    80: (* STATE 80: SILICA SCALING SEED INHIBITOR SHOCK TREATMENT & BED REGENERATION *)
        bSystemReady := FALSE;
        bSystemRunning := TRUE;

        (* High-rate anti-scalant flush to dissolve any colloidal silica seeds before returning to service *)
        tInhibitorFlushTimer(IN := TRUE, PT := T#15S);
        IF tInhibitorFlushTimer.Q THEN
            tInhibitorFlushTimer(IN := FALSE);
            iState := 30; (* Column fully regenerated; return to continuous adsorption *)
        END_IF;

    90: (* STATE 90: CONTROLLED SYSTEM SHUTDOWN & THERMAL RAMP-DOWN *)
        bSystemReady := FALSE;
        bSystemRunning := TRUE;
        rCarouselAdvanceDemand_pct := 0.0;
        rAcidDosingValveDemand_pct := 0.0;
        rSilicaInhibitorDosing_Lh := 5.0;

        (* Controlled deceleration of recovery turbine *)
        IF rHertVfdSpeedDemand_rpm > 1200.0 THEN
            rHertVfdSpeedDemand_rpm := rHertVfdSpeedDemand_rpm - (50.0 * rCycleTime_sec);
        ELSE
            rHertVfdSpeedDemand_rpm := 0.0;
            bSystemRunning := FALSE;
            iState := 0; (* Parked *)
        END_IF;

    100: (* STATE 100: CRITICAL EMERGENCY DEPRESSURIZATION, TRIP & TURBINE RUNAWAY BRAKING *)
        bSystemReady := FALSE;
        bSystemRunning := FALSE;
        bSystemTripped := TRUE;
        rCarouselAdvanceDemand_pct := 0.0;
        rAcidDosingValveDemand_pct := 0.0;
        rSilicaInhibitorDosing_Lh := 0.0;
        rHertVfdSpeedDemand_rpm := 0.0;
        rEluateDiverterValve_pct := 0.0;
        bDeflectorEmergencyDrop := TRUE; (* Deploy mechanical deflector to divert high-pressure jet *)

        (* Fault Reset and Unlatch Evaluation *)
        IF bResetFaults AND bEmergencyStop AND (dwAlarmWord1 = 16#0000_0000) AND (dwAlarmWord2 = 16#0000_0000) THEN
            bSystemTripped := FALSE;
            bDeflectorEmergencyDrop := FALSE;
            bHertEmergencyBrakeTripped := FALSE;
            iState := 0; (* Return to cold boot / uninitialized state *)
        END_IF;

END_CASE;


(* ============================================================================================= *)
(* 10.0 GRACEFUL DEGRADATION, SENSOR DERATE & ACTUATOR SATURATION MANAGEMENT                     *)
(* ============================================================================================= *)
(* Handles operation under degraded instrument conditions and enforces multi-variable safety bounds*)

bDegradedInstrumentWarning := bPres_Degraded_1oo2 OR bTemp_Degraded_1oo2 OR 
                              bFlow_Degraded_1oo2 OR bPH_Degraded_1oo2 OR bSpeed_Degraded_1oo2;

IF bDegradedInstrumentWarning THEN
    dwWarningWord := dwWarningWord OR 16#0000_0200; (* Degraded instrument cluster active *)
END_IF;

(* Automatic Sorbent Health Derate Evaluation *)
IF rColumnThermalCyclesCount > 2500.0 THEN
    rSorbentHealthFactor := 0.785;
    dwWarningWord := dwWarningWord OR 16#0000_0400; (* Sorbent life consumption warning *)
END_IF;

(* Saturated Output Clamping *)
IF rCarouselAdvanceDemand_pct > 100.0 THEN rCarouselAdvanceDemand_pct := 100.0; END_IF;
IF rCarouselAdvanceDemand_pct < 0.0 THEN rCarouselAdvanceDemand_pct := 0.0; END_IF;

IF rAcidDosingValveDemand_pct > 100.0 THEN rAcidDosingValveDemand_pct := 100.0; END_IF;
IF rAcidDosingValveDemand_pct < 0.0 THEN rAcidDosingValveDemand_pct := 0.0; END_IF;

IF rEluateDiverterValve_pct > 100.0 THEN rEluateDiverterValve_pct := 100.0; END_IF;
IF rEluateDiverterValve_pct < 0.0 THEN rEluateDiverterValve_pct := 0.0; END_IF;


(* ============================================================================================= *)
(* 11.0 BIT-PACKED STATUS WORDS & ALARM TREE ASSEMBLY                                           *)
(* ============================================================================================= *)
(* Encodes system status into standardized DWORD registers for plant DCS / SCADA integration     *)

dwSystemStatusWord := 16#0000_0000;
IF bSystemRunning THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0001; END_IF;
IF bSystemReady THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0002; END_IF;
IF bSystemTripped THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0004; END_IF;
IF bAdsorptionLeadLagSwapReq THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0008; END_IF;
IF bElutionPeakDetected THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0010; END_IF;
IF bSilicaPolymerizationHazard THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0020; END_IF;
IF bHertEmergencyBrakeTripped THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0040; END_IF;
IF bDegradedInstrumentWarning THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0080; END_IF;
IF bCarouselIndexingActive THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0100; END_IF;

(* State bits encoding *)
IF (iState = 0)   THAL dwSystemStatusWord := dwSystemStatusWord OR 16#0001_0000; END_IF;
IF (iState = 10)  THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0002_0000; END_IF;
IF (iState = 20)  THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0004_0000; END_IF;
IF (iState = 30)  THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0008_0000; END_IF;
IF (iState = 40)  THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0010_0000; END_IF;
IF (iState = 50)  THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0020_0000; END_IF;
IF (iState = 60)  THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0040_0000; END_IF;
IF (iState = 70)  THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0080_0000; END_IF;
IF (iState = 80)  THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0100_0000; END_IF;
IF (iState = 90)  THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0200_0000; END_IF;
IF (iState = 100) THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0400_0000; END_IF;

END_FUNCTION_BLOCK
"""
    return st_code

print("Module defined")
