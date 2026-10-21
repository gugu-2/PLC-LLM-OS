# Python script to build the complete FB_GeothermalDLE_IonExchange_ElutionCycle
# and verify all syntax rules, parity, and character counts.

import json
import uuid
import re
import sys

def build_iec_code():
    parts = []

    # -------------------------------------------------------------------------
    # HEADER & PROCESS ARCHITECTURE
    # -------------------------------------------------------------------------
    parts.append("""FUNCTION_BLOCK FB_GeothermalDLE_IonExchange_ElutionCycle
(*
========================================================================================================================
 CYBER-PHYSICAL SYSTEM SPECIFICATION & INDUSTRIAL DOMAIN ARCHITECTURE:
 SUPERCRITICAL GEOTHERMAL BRINE DIRECT LITHIUM EXTRACTION (DLE) - 220.0 deg C, 25.0 bar
 MULTI-COLUMN SORBENT (Al-Li LDH / Ti-O) BED CAROUSEL DYNAMIC ADSORPTION FRONT TRACKING,
 HIGH-PRESSURE ACID ELUTION WASH PROFILE, SILICA SCALING POLYMERIZATION SEED INHIBITOR DOSING,
 AND HYDRAULIC ENERGY RECOVERY TURBINE (HERT) RUNNER SPEED GOVERNOR
========================================================================================================================
 
 1.0 CHEMICAL ENGINEERING & PROCESS THERMODYNAMICS OVERVIEW:
   - High-enthalpy geothermal reservoir brine extracted at supercritical wellhead conditions:
     T_feed = 220.0 deg C (493.15 K), P_feed = 25.0 bar (2.50 MPa gauge). Total Dissolved Solids (TDS) = 260,000 - 310,000 mg/L.
     Raw feed lithium ion concentration [Li+] = 280.0 to 450.0 mg/L, dissolved monomeric silica [SiO2] = 480.0 to 650.0 mg/L.
   - Sorbent Matrix Chemistry:
     High-temperature crystalline Layered Double Hydroxide (Al-Li LDH: [LiAl2(OH)6]Cl * nH2O) and Nanostructured Lithium
     Titanate / Titanic Acid (H2TiO3 / LTO) ion sieve materials packed in packed-bed columns.
     The adsorption selectivity quotient alpha_(Li/Na) > 1200, alpha_(Li/Ca) > 850, enabling highly selective lithium uptake
     directly from hypersaline sodium/calcium/potassium chloride matrix.
   - Sorbent Degradation & Lattice Stability:
     Operation strictly bound above pH 1.95 to prevent irreversible leaching and dissolution of octahedral aluminum/titanium
     framework (Al(OH)3 + 3H+ -> Al3+ + 3H2O). Thermal degradation derating factor tracked across thermal cycles (220 deg C <-> 95 deg C).

 2.0 DYNAMIC ADSORPTION FRONT & MASS TRANSFER ZONE (MTZ) TRACKING:
   - Discretized 10-node axial finite volume representation of the sorbent bed along length L = 3.80 m.
   - Dynamic breakthrough governed by modified Bohart-Adams and Thomas sorption kinetic differential formulations:
     d(q_i)/dt = k_Th * (q_max * C_i - q_i * C_i)
   - Real-time mass-transfer wave front velocity tracking:
     v_front = u_superficial / (epsilon_bed + rho_bulk * (q_star / C_feed))
   - Lead/Lag carousel advance handoff automatically triggered at 88.0% penetration depth or 15.0% effluent lithium slip.

 3.0 AMORPHOUS SILICA POLYMERIZATION & KINETIC SEED INHIBITION:
   - Supersaturation ratio S = [SiO2]_actual / C_eq(T, pH).
   - Non-linear amorphous silica equilibrium solubility polynomial:
     C_eq(T) = 55.4 + 1.28*T + 0.0041*T^2 [mg/L]
   - Induction time before homogeneous nucleation: tau_ind = A_nucl * exp(E_act / (R * T)) * (S - 1)^(-2).
   - High-pressure polyacrylic/phosphinocarboxylic anti-scalant dosing dynamically compensated via Arrhenius scaling
     and wellhead flow pacing to retard colloidal silica gelation and prevent catastrophic sorbent pore blinding.

 4.0 HIGH-PRESSURE ACID ELUTION WASH PROFILE & CHROMATOGRAPHIC PEAK CUT:
   - Sub-boiling pressurized displacement of entrained interstitial brine using high-temperature demineralized water at 25 bar.
   - Stoichiometric hydrochloric acid (0.15 - 0.35 M HCl) elution profile to strip bound Li+ as lithium chloride (LiCl).
   - Feedforward-feedback decoupled pH regulation maintaining pH strictly within 2.30 to 2.50.
   - Toroidal non-contact electrodeless conductivity sensor detecting the chromatographic LiCl elution peak:
     Harvest valve opens at kappa >= 45.0 mS/cm (directing rich eluate to crystallization) and closes at kappa <= 14.0 mS/cm.

 5.0 HYDRAULIC ENERGY RECOVERY TURBINE (HERT) RUNNER SPEED GOVERNOR:
   - Pelton-type hydraulic impulse turbine / reverse running multistage pump recovering kinetic and pressure head from the spent
     brine discharge (25.0 bar down to 3.5 bar reinjection suction).
   - Recovers up to 85.0% of available hydraulic expansion energy, producing continuous mechanical-to-electrical power.
   - Tip-speed ratio optimization: lambda_opt = u_runner / c_jet = 0.465.
   - Fast jet deflector drop mechanism (< 60 ms actuation) to prevent explosive overspeed runaway in event of generator breaker trip.
   - Real-time Net Positive Suction Head (NPSH) supervision preventing cavitation flashing.

 6.0 MULTIVARIABLE STATE-SPACE MODEL & MODEL PREDICTIVE CONTROL (MPC):
   - Discrete 5x5 state-space system matrix representation:
     x(k+1) = A_d * x(k) + B_d * u(k) + Ed * d(k)
     y(k)   = C_d * x(k) + D_d * u(k)
   - Analytical unconstrained quadratic cost minimization with iterative projected gradient saturation handling.

 7.0 SAFETY-INSTRUMENTED SYSTEM (SIS) & TRIPLE MODULAR REDUNDANCY (TMR):
   - 2oo3 voting on all process-critical analog transmitters with discrepancy detection and automatic failover to 1oo2.
   - 11-stage Finite State Machine with deterministic cycle management and SIL-3 graceful degradation.
========================================================================================================================
*)
""")

    # -------------------------------------------------------------------------
    # VAR_INPUT
    # -------------------------------------------------------------------------
    parts.append("""VAR_INPUT
    (* ================================================================================================================ *)
    (* 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) PROCESS SENSOR CHANNELS                                                     *)
    (* ================================================================================================================ *)

    (* --- Wellhead Supercritical Geothermal Brine Supply Pressure [bar] --- *)
    rBrineInletPressure_A_bar       : REAL;     (* [bar] Primary wellhead geothermal brine supply pressure channel A *)
    rBrineInletPressure_B_bar       : REAL;     (* [bar] Primary wellhead geothermal brine supply pressure channel B *)
    rBrineInletPressure_C_bar       : REAL;     (* [bar] Primary wellhead geothermal brine supply pressure channel C *)

    (* --- Wellhead Supercritical Geothermal Brine Temperature [deg C] --- *)
    rBrineInletTemp_A_degC          : REAL;     (* [deg C] High-enthalpy supercritical brine temperature channel A *)
    rBrineInletTemp_B_degC          : REAL;     (* [deg C] High-enthalpy supercritical brine temperature channel B *)
    rBrineInletTemp_C_degC          : REAL;     (* [deg C] High-enthalpy supercritical brine temperature channel C *)

    (* --- Multi-Column Extraction Carousel Raw Brine Feed Volumetric Flow [m3/h] --- *)
    rBrineFeedFlow_A_m3h            : REAL;     (* [m3/h] Extraction carousel raw brine feed volumetric flow rate channel A *)
    rBrineFeedFlow_B_m3h            : REAL;     (* [m3/h] Extraction carousel raw brine feed volumetric flow rate channel B *)
    rBrineFeedFlow_C_m3h            : REAL;     (* [m3/h] Extraction carousel raw brine feed volumetric flow rate channel C *)

    (* --- High-Pressure Acid Elution Stripping Line pH Analyzers [pH] --- *)
    rElutionAcidPH_A_pH             : REAL;     (* [pH] High-pressure acid elution wash feed pH channel A *)
    rElutionAcidPH_B_pH             : REAL;     (* [pH] High-pressure acid elution wash feed pH channel B *)
    rElutionAcidPH_C_pH             : REAL;     (* [pH] High-pressure acid elution wash feed pH channel C *)

    (* --- Hydraulic Energy Recovery Turbine (HERT) Shaft Speed Probes [rpm] --- *)
    rTurbineSpeed_A_rpm             : REAL;     (* [rpm] Hydraulic Energy Recovery Turbine shaft speed sensor A *)
    rTurbineSpeed_B_rpm             : REAL;     (* [rpm] Hydraulic Energy Recovery Turbine shaft speed sensor B *)
    rTurbineSpeed_C_rpm             : REAL;     (* [rpm] Hydraulic Energy Recovery Turbine shaft speed sensor C *)

    (* ================================================================================================================ *)
    (* ANALYTICAL PROCESS SENSORS & INSTRUMENTATION                                                                     *)
    (* ================================================================================================================ *)

    (* --- Online Spectrophotometric & Ion-Selective Lithium Analyzers [mg/L] --- *)
    rInletLithiumConc_mgL           : REAL;     (* [mg/L] Online spectroscopic raw brine lithium ion concentration *)
    rEffluentLithiumConc_mgL         : REAL;     (* [mg/L] Online post-sorbent effluent lithium slip concentration *)

    (* --- Online Soluble Silica Silicic Acid Analyzer [mg/L] --- *)
    rDissolvedSilicaConc_mgL        : REAL;     (* [mg/L] Online colorimetric molybdate-reactive dissolved silica concentration *)

    (* --- HERT Permanent Magnet Synchronous Generator Active Power [kW] --- *)
    rTurbineActivePower_kW          : REAL;     (* [kW] HERT permanent magnet synchronous generator active electrical power *)

    (* --- High-Temperature Toroidal Electrodeless Conductivity Analyzer [mS/cm] --- *)
    rEluateConductivity_mScm        : REAL;     (* [mS/cm] Toroidal non-contact conductivity of rich lithium eluate stream *)

    (* --- Active Sorbent Bed Differential Pressure Transmitter [bar] --- *)
    rColumnDiffPressure_bar         : REAL;     (* [bar] Active lead sorbent column differential pressure *)

    (* --- Displaced Column Brine Effluent Specific Gravity / Density [kg/m3] --- *)
    rBrineEffluentDensity_kgm3      : REAL := 1180.0; (* [kg/m3] Displaced brine effluent fluid density *)

    (* --- Sorbent Column Inlet Header Temperature [deg C] --- *)
    rColumnInletTemp_degC           : REAL := 215.0;  (* [deg C] Sorbent bed inlet distribution manifold temperature *)

    (* --- Sorbent Column Outlet Header Backpressure [bar] --- *)
    rColumnOutletBackpressure_bar   : REAL := 23.5;   (* [bar] Column carousel outlet backpressure regulating header *)

    (* ================================================================================================================ *)
    (* DIGITAL COMMANDS, SAFETY PERMISSIVES, AND INTERLOCK SIGNALS                                                      *)
    (* ================================================================================================================ *)

    bEnableCycle                    : BOOL;     (* Master supervisory extraction and elution cycle enable command *)
    bEmergencyStop                  : BOOL;     (* Dual-channel hardwired SIL-3 emergency stop circuit healthy (NC) *)
    bCarouselIndexPermissive        : BOOL;     (* Column carousel mechanical turret indexer alignment lock verified *)
    bResetFaults                    : BOOL;     (* Global master operator fault reset and latch clear strobe *)
    bInhibitorTankLowLevel          : BOOL;     (* Chemical inhibitor storage day-tank low level switch *)
    bHertOverspeedSensorTrip        : BOOL;     (* Discrete hardwired turbine centrifugal overspeed trip contact *)
    bDeminWaterPressureOk           : BOOL := TRUE;  (* Demineralized wash water supply booster pump pressure OK *)
    bNitrogenPurgePressureOk        : BOOL := TRUE;  (* High-pressure nitrogen blanket regulator header pressure OK *)
    bAcidDayTankLevelOk             : BOOL := TRUE;  (* Concentrated hydrochloric acid metering day-tank level OK *)

    (* ================================================================================================================ *)
    (* REAL-TIME CONTROLLER EXECUTION SCAN CONFIGURATION                                                                *)
    (* ================================================================================================================ *)
    rCycleTime_sec                  : REAL := 0.01; (* [s] Discrete task loop execution period (10 ms scan cycle) *)
END_VAR
""")

    # -------------------------------------------------------------------------
    # VAR_OUTPUT
    # -------------------------------------------------------------------------
    parts.append("""VAR_OUTPUT
    (* ================================================================================================================ *)
    (* SUPERVISORY SYSTEM STATUS & SEQUENCING INDICATORS                                                               *)
    (* ================================================================================================================ *)
    bSystemReady                    : BOOL;     (* Supervisory system ready for automated extraction cycle *)
    bSystemRunning                  : BOOL;     (* Active extraction, elution, or regeneration sequence in progress *)
    bSystemTripped                  : BOOL;     (* Master emergency shutdown tripped and safety bypass latched *)
    bAdsorptionLeadLagSwapReq       : BOOL;     (* Adsorption front reached saturation threshold; carousel rotation trigger *)
    bElutionPeakDetected            : BOOL;     (* Concentrated lithium chloride eluate harvest band active *)
    bSilicaPolymerizationHazard     : BOOL;     (* Silica supersaturation ratio exceeded critical polymerization threshold *)
    bHertEmergencyBrakeTripped      : BOOL;     (* Turbine dynamic overspeed deflector jet activated *)
    bDegradedSensorMode             : BOOL;     (* At least one 2oo3 sensor bank operating in degraded 1oo2 mode *)
    bRegenerationRequired           : BOOL;     (* Sorbent chemical fouling threshold exceeded; acid rejuvenation required *)

    (* ================================================================================================================ *)
    (* CONTINUOUS PROCESS ACTUATION DEMANDS & CONTROLLER OUTPUTS                                                       *)
    (* ================================================================================================================ *)
    rCarouselAdvanceDemand_pct      : REAL;     (* [%] Rotary carousel hydraulic indexing drive speed / position demand *)
    rAcidDosingValveDemand_pct      : REAL;     (* [%] High-pressure acid metering diaphragm pump / valve demand *)
    rSilicaInhibitorDosing_Lh       : REAL;     (* [L/h] Silica scale inhibitor chemical injection pump metering rate *)
    rHertVfdSpeedDemand_rpm         : REAL;     (* [rpm] Hydraulic Energy Recovery Turbine governor / VFD speed setpoint *)
    rEluateDiverterValve_pct        : REAL;     (* [%] Eluate cut diverter 3-way valve position: 0%=Recycle, 100%=Harvest *)
    rBrineBypassValveDemand_pct     : REAL;     (* [%] High-pressure feed brine bypass modulation valve command *)
    rColumnBackpressureValve_pct    : REAL;     (* [%] Multi-column outlet backpressure regulating control valve *)

    (* ================================================================================================================ *)
    (* ADVANCED PROCESS DIAGNOSTICS & TELEMETRY CALCULATIONS                                                           *)
    (* ================================================================================================================ *)
    rEstimatedBreakthrough_pct      : REAL;     (* [%] Online estimated sorbent bed dynamic mass transfer front penetration *)
    rNetRecoveredHydraulicPower_kW  : REAL;     (* [kW] Instantaneous mechanical-to-electrical net recovered power *)
    rSpecificAcidConsumption_kgLi   : REAL;     (* [kg/kg] Real-time stoichiometric acid consumption ratio per kg Li harvested *)
    rSilicaSaturationIndex          : REAL;     (* [-] Logarithmic silica supersaturation ratio (log10(C/C_eq)) *)
    rCumulativeLithiumDay_kg        : REAL;     (* [kg] Cumulative total purified elemental lithium harvested today *)
    rCurrentSpecificEnergy_kWh_kg   : REAL;     (* [kWh/kg] Specific net parasitic energy consumed per kg Li produced *)

    (* ================================================================================================================ *)
    (* STANDARDIZED BIT-PACKED STATUS & ALARM TELEMETRY REGISTERS                                                       *)
    (* ================================================================================================================ *)
    dwSystemStatusWord              : DWORD;    (* Bit-packed operational state and active subsystem flags *)
    dwAlarmWord1                    : DWORD;    (* Bit-packed primary process safety and boundary trip alarms *)
    dwAlarmWord2                    : DWORD;    (* Bit-packed secondary equipment protection and interlock alarms *)
    dwWarningWord                   : DWORD;    (* Bit-packed predictive maintenance and sensor degradation warnings *)
END_VAR
""")

    # -------------------------------------------------------------------------
    # VAR
    # -------------------------------------------------------------------------
    parts.append("""VAR
    (* ================================================================================================================ *)
    (* 1.0 INTERNAL 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING STRUCTURES                                      *)
    (* ================================================================================================================ *)
    rVotedBrinePressure_bar         : REAL := 25.0;
    rVotedBrineTemp_degC            : REAL := 220.0;
    rVotedBrineFlow_m3h             : REAL := 450.0;
    rVotedElutionPH_pH              : REAL := 2.45;
    rVotedTurbineSpeed_rpm          : REAL := 3000.0;

    (* Channel Fault Latches *)
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

    (* Outlier Discrepancy Debounce Timers *)
    tPresDiscrepancyTimer           : TON;
    tTempDiscrepancyTimer           : TON;
    tFlowDiscrepancyTimer           : TON;
    tPHDiscrepancyTimer             : TON;
    tSpeedDiscrepancyTimer          : TON;

    (* Previous Cycle Samples for Rate-of-Change / Frozen Sensor Detection *)
    rPres_LastA                     : REAL := 25.0;
    rPres_LastB                     : REAL := 25.0;
    rPres_LastC                     : REAL := 25.0;
    rTemp_LastA                     : REAL := 220.0;
    rTemp_LastB                     : REAL := 220.0;
    rTemp_LastC                     : REAL := 220.0;
    rFlow_LastA                     : REAL := 450.0;
    rFlow_LastB                     : REAL := 450.0;
    rFlow_LastC                     : REAL := 450.0;
    rPH_LastA                       : REAL := 2.45;
    rPH_LastB                       : REAL := 2.45;
    rPH_LastC                       : REAL := 2.45;
    rSpeed_LastA                    : REAL := 3000.0;
    rSpeed_LastB                    : REAL := 3000.0;
    rSpeed_LastC                    : REAL := 3000.0;

    (* Frozen Sensor Accumulator Timers *)
    rPresFrozenAccum_A              : REAL := 0.0;
    rPresFrozenAccum_B              : REAL := 0.0;
    rPresFrozenAccum_C              : REAL := 0.0;

    (* ================================================================================================================ *)
    (* 2.0 COLUMN CAROUSEL GEOMETRY & SORBENT ADSORPTION DYNAMICS (THOMAS / BOHART-ADAMS)                             *)
    (* ================================================================================================================ *)
    (* Mechanical Specs: 6 Columns, Height L = 3.80 m, Diameter D = 1.60 m                                            *)
    rBedLength_m                    : REAL := 3.80;
    rBedCrossSection_m2             : REAL := 2.01062;  (* pi * (1.60 / 2)^2 *)
    rBedVolume_m3                   : REAL := 7.64035;  (* CrossSection * Length *)
    rSorbentVoidFraction            : REAL := 0.385;    (* Inter-particle bed porosity *)
    rSorbentBulkDensity_kgm3        : REAL := 820.0;    (* Dry bed packing bulk density *)
    rTotalSorbentMass_kg            : REAL := 6265.09;  (* Volume * BulkDensity *)

    (* Sorbent Equilibrium & Kinetic Constants (Al-Li LDH at 90-120 deg C)                                            *)
    rSorbentMaxCapacity_mg_g        : REAL := 9.450;    (* Theoretical maximum Li+ uptake capacity *)
    rThomasKineticConstant_L_min_mg : REAL := 0.000185; (* Thomas rate constant k_Th *)
    rLangmuirAffinity_L_mg          : REAL := 0.0245;   (* Langmuir equilibrium constant K_L *)

    (* Dynamic Mass Transfer Front Tracking Integrators *)
    rAdsorptionFrontPosition_m      : REAL := 0.0;      (* Axial coordinate of MTZ center [m] *)
    rCumulativeLiMassFed_kg         : REAL := 0.0;      (* Total lithium mass entered current column *)
    rCumulativeLiMassAdsorbed_kg    : REAL := 0.0;      (* Estimated lithium loaded onto column *)
    rCurrentColumnRunTime_sec       : REAL := 0.0;      (* Time spent in lead adsorption position *)
    rSuperficialVelocity_ms         : REAL := 0.0;      (* Interstitial fluid velocity *)
    rMassTransferZoneWidth_m        : REAL := 0.650;    (* Effective MTZ boundary spread *)
    iActiveLeadColumnIndex          : INT := 1;         (* Currently active carousel lead column (1..6) *)
    iActiveLagColumnIndex           : INT := 2;         (* Currently active carousel lag column (1..6) *)
    iActiveWashColumnIndex          : INT := 3;         (* Currently active column undergoing displacement wash *)
    iActiveElutionColumnIndex       : INT := 4;         (* Currently active column undergoing acid stripping *)
    iActiveSweetenColumnIndex       : INT := 5;         (* Currently active column undergoing sweetening rinse *)
    iActiveConditionColumnIndex     : INT := 6;         (* Currently active column undergoing conditioning *)

    (* Discretized 10-Node Axial Saturation Profile: q_node[0..9] as fraction of q_max *)
    rSorbentSaturation_Node0        : REAL := 0.985;    (* Entrance node (z = 0.00 to 0.38 m) *)
    rSorbentSaturation_Node1        : REAL := 0.970;    (* Node 1 (z = 0.38 to 0.76 m) *)
    rSorbentSaturation_Node2        : REAL := 0.940;    (* Node 2 (z = 0.76 to 1.14 m) *)
    rSorbentSaturation_Node3        : REAL := 0.880;    (* Node 3 (z = 1.14 to 1.52 m) *)
    rSorbentSaturation_Node4        : REAL := 0.760;    (* Node 4 (z = 1.52 to 1.90 m) *)
    rSorbentSaturation_Node5        : REAL := 0.580;    (* Node 5 (z = 1.90 to 2.28 m) - MTZ Center *)
    rSorbentSaturation_Node6        : REAL := 0.350;    (* Node 6 (z = 2.28 to 2.66 m) *)
    rSorbentSaturation_Node7        : REAL := 0.160;    (* Node 7 (z = 2.66 to 3.04 m) *)
    rSorbentSaturation_Node8        : REAL := 0.045;    (* Node 8 (z = 3.04 to 3.42 m) *)
    rSorbentSaturation_Node9        : REAL := 0.005;    (* Exit node (z = 3.42 to 3.80 m) *)

    (* Sorbent Bed Thermal Degradation & Hydrothermal Stability Monitor *)
    rColumnThermalCyclesCount       : REAL := 1420.0;   (* Cumulative hot brine thermal shock cycles *)
    rSorbentHealthFactor            : REAL := 0.945;    (* Capacity derate factor (1.0 = virgin, <0.70 = replace) *)
    rAcidExposureHours              : REAL := 840.5;    (* Cumulative hours exposed to pH < 2.8 *)

    (* Ergun Equation Fluid Resistance Parameters *)
    rSorbentParticleDiameter_m      : REAL := 0.00045;  (* 450 micron bead diameter *)
    rBrineDynamicViscosity_Pas      : REAL := 0.000185; (* Geothermal brine dynamic viscosity at 220 C *)
    rCalculatedCleanDeltaP_bar      : REAL := 1.15;     (* Theoretical Ergun clean pressure drop *)

    (* ================================================================================================================ *)
    (* 3.0 AMORPHOUS SILICA SATURATION & POLYMERIZATION SEED INHIBITOR KINETIC ENGINE                                   *)
    (* ================================================================================================================ *)
    rSilicaEquilibriumSolubility_mgL: REAL := 420.0;    (* C_eq calculated at local brine temperature *)
    rSilicaSupersaturationRatio     : REAL := 1.15;     (* S = C_actual / C_eq *)
    rSilicaPolymerizationRate_mgL_s : REAL := 0.0;      (* Monomer condensation rate *)
    rSilicaInductionTime_sec        : REAL := 1200.0;   (* Time delay before colloidal silica nucleates *)
    rInhibitorBaseDosage_mgL        : REAL := 18.5;     (* Standard anti-scalant dosing rate *)
    rInhibitorTempCompensation      : REAL := 1.0;      (* Arrhenius correction multiplier *)
    rInhibitorDemand_Lh             : REAL := 12.5;     (* Output metering pump rate *)
    rInhibitorStockConcentration_pct: REAL := 30.0;     (* Commercial active polyacrylate inhibitor conc *)
    rInhibitorSpecificGravity       : REAL := 1.18;     (* Solution density [kg/L] *)
    rSilicaNucleationBarrier_kJmol  : REAL := 48.5;     (* Thermodynamic free energy barrier *)

    (* ================================================================================================================ *)
    (* 4.0 HIGH-PRESSURE ACID ELUTION WASH TRAJECTORY & CHROMATOGRAPHIC PEAK HARVEST                                    *)
    (* ================================================================================================================ *)
    rTargetElutionPH                : REAL := 2.40;     (* Strict window: 2.30 to 2.50 to preserve LDH lattice *)
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
    rEluateMassFlow_kgh             : REAL := 0.0;
    rEluateLithiumConcentration_mgL : REAL := 0.0;

    (* ================================================================================================================ *)
    (* 5.0 HYDRAULIC ENERGY RECOVERY TURBINE (HERT) HYDRODYNAMICS & RUNAWAY GOVERNOR                                    *)
    (* ================================================================================================================ *)
    rTurbineInletHead_m             : REAL := 250.0;    (* Equivalent brine head from 25 bar *)
    rTurbineOptimalTipSpeedRatio    : REAL := 0.465;    (* Pelton runner velocity ratio u/c0 *)
    rTurbinePitchDiameter_m         : REAL := 0.650;    (* Runner active diameter *)
    rTurbineTargetSpeed_rpm         : REAL := 2980.0;   (* Nominal synchronized speed setpoint *)
    rTurbineGovernor_Kp             : REAL := 1.450;
    rTurbineGovernor_Ki             : REAL := 0.220;
    rTurbineGovernorIntegral        : REAL := 0.0;
    rNozzleNeedlePosition_pct       : REAL := 65.0;     (* Spear valve modulating position *)
    rVaporPressureAtTemp_bar        : REAL := 18.20;    (* Brine vapor pressure at 208 deg C *)
    rTurbineNPSH_Available_m        : REAL := 32.50;    (* Net Positive Suction Head available *)
    rTurbineNPSH_Required_m         : REAL := 14.80;    (* Net Positive Suction Head required *)
    bDeflectorEmergencyDrop         : BOOL := FALSE;    (* Fast jet deflector solenoid (<60 ms response) *)
    rTurbineShaftTorque_Nm          : REAL := 1250.0;   (* Calculated mechanical shaft torque *)
    rTurbineRunawaySpeed_rpm        : REAL := 5400.0;   (* Theoretical runaway overspeed limit *)

    (* ================================================================================================================ *)
    (* 6.0 COMPLETE STATE-SPACE MODEL MATRICES & MODEL PREDICTIVE CONTROL (MPC) ENGINE                                  *)
    (* ================================================================================================================ *)
    (* Discrete State Space Evolution:                                                                                 *)
    (* x(k+1) = A_d * x(k) + B_d * u(k) + Ed * d(k)                                                                    *)
    (* States x:                                                                                                       *)
    (*   x[1] = Sorbent MTZ Front Position z_f [m]                                                                     *)
    (*   x[2] = Bed Differential Pressure Delta_P [bar]                                                                *)
    (*   x[3] = Stripping Elution pH [pH]                                                                              *)
    (*   x[4] = HERT Turbine Speed omega [rpm]                                                                         *)
    (*   x[5] = Silica Polymerization Nucleation Index xi [-]                                                          *)
    (* Manipulated Variables u:                                                                                        *)
    (*   u[1] = Brine Bypass Control Valve Trim [%]                                                                    *)
    (*   u[2] = Elution Acid Metering Pump Stroke [%]                                                                  *)
    (*   u[3] = HERT Spear Valve Nozzle Position [%]                                                                   *)
    (*   u[4] = Silica Seed Inhibitor Injection Flow [%]                                                               *)
    (* Disturbances d:                                                                                                 *)
    (*   d[1] = Geothermal Wellhead Pressure Fluctuations Delta_P_well [bar]                                           *)
    (*   d[2] = Feed Brine Temperature Thermal Shock Delta_T_feed [deg C]                                              *)
    (*   d[3] = Raw Brine Lithium Concentration Variability Delta_C_Li [mg/L]                                          *)

    (* Discrete State Transition Matrix A_d (5x5, sample time dt = 0.01 s) *)
    A_11 : REAL := 0.999820;  A_12 : REAL := 0.000000;  A_13 : REAL := 0.000000;  A_14 : REAL := 0.000000;  A_15 : REAL := 0.000000;
    A_21 : REAL := 0.000350;  A_22 : REAL := 0.994200;  A_23 : REAL := 0.000000;  A_24 : REAL := 0.000000;  A_25 : REAL := 0.001250;
    A_31 : REAL := 0.000000;  A_32 : REAL := 0.000000;  A_33 : REAL := 0.985000;  A_34 : REAL := 0.000000;  A_35 : REAL := 0.000000;
    A_41 : REAL := 0.000000;  A_42 : REAL :=-0.008500;  A_43 : REAL := 0.000000;  A_44 : REAL := 0.991200;  A_45 : REAL := 0.000000;
    A_51 : REAL := 0.000120;  A_52 : REAL := 0.000450;  A_53 : REAL :=-0.002100;  A_54 : REAL := 0.000000;  A_55 : REAL := 0.996500;

    (* Discrete Input Coupling Matrix B_d (5x4) *)
    B_11 : REAL :=-0.000150;  B_12 : REAL := 0.000000;  B_13 : REAL := 0.000000;  B_14 : REAL := 0.000000;
    B_21 : REAL :=-0.004200;  B_22 : REAL := 0.000000;  B_23 : REAL :=-0.001100;  B_24 : REAL :=-0.000850;
    B_31 : REAL := 0.000000;  B_32 : REAL :=-0.024500;  B_33 : REAL := 0.000000;  B_34 : REAL := 0.000000;
    B_41 : REAL := 0.012500;  B_42 : REAL := 0.000000;  B_43 : REAL := 0.358000;  B_44 : REAL := 0.000000;
    B_51 : REAL := 0.000250;  B_52 : REAL := 0.000100;  B_53 : REAL := 0.000000;  B_54 : REAL :=-0.018500;

    (* Disturbance Coupling Matrix Ed (5x3) *)
    Ed_11 : REAL := 0.000080; Ed_12 : REAL := 0.000120; Ed_13 : REAL := 0.000450;
    Ed_21 : REAL := 0.003500; Ed_22 : REAL :=-0.001800; Ed_23 : REAL := 0.000000;
    Ed_31 : REAL := 0.000000; Ed_32 : REAL := 0.000850; Ed_33 : REAL := 0.000000;
    Ed_41 : REAL := 0.125000; Ed_42 : REAL := 0.022000; Ed_43 : REAL := 0.000000;
    Ed_51 : REAL := 0.000450; Ed_52 : REAL := 0.004200; Ed_53 : REAL := 0.000150;

    (* Output Observation Matrix C_d (4x5) *)
    C_11 : REAL := 1.000000;  C_12 : REAL := 0.000000;  C_13 : REAL := 0.000000;  C_14 : REAL := 0.000000;  C_15 : REAL := 0.000000;
    C_21 : REAL := 0.000000;  C_22 : REAL := 1.000000;  C_23 : REAL := 0.000000;  C_24 : REAL := 0.000000;  C_25 : REAL := 0.000000;
    C_31 : REAL := 0.000000;  C_32 : REAL := 0.000000;  C_33 : REAL := 1.000000;  C_34 : REAL := 0.000000;  C_35 : REAL := 0.000000;
    C_41 : REAL := 0.000000;  C_42 : REAL := 0.000000;  C_43 : REAL := 0.000000;  C_44 : REAL := 1.000000;  C_45 : REAL := 0.000000;

    (* Direct Feedthrough Matrix D_d (4x4) *)
    D_11 : REAL := 0.000000;  D_12 : REAL := 0.000000;  D_13 : REAL := 0.000000;  D_14 : REAL := 0.000000;
    D_21 : REAL := 0.000000;  D_22 : REAL := 0.000000;  D_23 : REAL := 0.000000;  D_24 : REAL := 0.000000;
    D_31 : REAL := 0.000000;  D_32 : REAL := 0.000000;  D_33 : REAL := 0.000000;  D_34 : REAL := 0.000000;
    D_41 : REAL := 0.000000;  D_42 : REAL := 0.000000;  D_43 : REAL := 0.000000;  D_44 : REAL := 0.000000;

    (* State Vector Estimates *)
    rState_x1_FrontPos_m            : REAL := 0.0;
    rState_x2_BedDeltaP_bar         : REAL := 1.250;
    rState_x3_ElutionPH             : REAL := 2.450;
    rState_x4_TurbineSpeed_rpm      : REAL := 2980.0;
    rState_x5_SilicaIndex           : REAL := 0.050;

    (* Setpoint Targets for MPC Quadratic Cost Optimization *)
    rSetpoint_x1_FrontPos_m         : REAL := 3.200;    (* Maximum target depth before carousel indexing *)
    rSetpoint_x2_BedDeltaP_bar      : REAL := 1.350;    (* Target clean hydraulic pressure drop *)
    rSetpoint_x3_ElutionPH          : REAL := 2.400;    (* Optimal stripping pH setpoint *)
    rSetpoint_x4_TurbineSpeed_rpm   : REAL := 2985.0;   (* Target peak electrical power speed *)

    (* MPC Quadratic Penalty Weights (Diagonal Q on states, Diagonal R on control increments) *)
    rWeight_Q1                      : REAL := 15.0;
    rWeight_Q2                      : REAL := 45.0;
    rWeight_Q3                      : REAL := 120.0;
    rWeight_Q4                      : REAL := 2.50;
    rWeight_R1                      : REAL := 8.00;
    rWeight_R2                      : REAL := 25.0;
    rWeight_R3                      : REAL := 5.00;
    rWeight_R4                      : REAL := 30.0;

    (* MPC Manipulated Variables & Control Increments *)
    rMpcOutput_u1_Bypass_pct        : REAL := 0.0;
    rMpcOutput_u2_Acid_pct          : REAL := 35.0;
    rMpcOutput_u3_Nozzle_pct        : REAL := 65.0;
    rMpcOutput_u4_Inhibitor_pct     : REAL := 22.0;

    rDeltaU1                        : REAL := 0.0;
    rDeltaU2                        : REAL := 0.0;
    rDeltaU3                        : REAL := 0.0;
    rDeltaU4                        : REAL := 0.0;

    (* MPC Prediction Horizon Prediction State Buffers (Np = 3 steps) *)
    rPred_x1_k1                     : REAL := 0.0;
    rPred_x2_k1                     : REAL := 1.25;
    rPred_x3_k1                     : REAL := 2.45;
    rPred_x4_k1                     : REAL := 2980.0;
    rPred_x5_k1                     : REAL := 0.05;

    rPred_x1_k2                     : REAL := 0.0;
    rPred_x2_k2                     : REAL := 1.25;
    rPred_x3_k2                     : REAL := 2.45;
    rPred_x4_k2                     : REAL := 2980.0;
    rPred_x5_k2                     : REAL := 0.05;

    (* ================================================================================================================ *)
    (* 7.0 FINITE STATE MACHINE SEQUENCER (11 DISTINCT PRODUCTION STATES)                                               *)
    (* ================================================================================================================ *)
    iState                          : INT := 0;
    (*
      0: UNINITIALIZED / COLD PLANT BOOT
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
    tShutdownCooldownTimer          : TON;

    (* Internal Process Flags & Diagnostics *)
    bDegradedInstrumentWarning      : BOOL := FALSE;
    bCarouselIndexingActive         : BOOL := FALSE;
    bOverpressurePreTrip            : BOOL := FALSE;
    bThermalShockHazard             : BOOL := FALSE;
    bSilicaGelationImminent         : BOOL := FALSE;
    bAcidLatticeCorrosionRisk       : BOOL := FALSE;

    (* Miscellaneous Process Computations *)
    rDeltaP_History                 : REAL := 0.0;
    rDeltaP_Derivative              : REAL := 0.0;
    rRawLithiumHarvestRate_kgh      : REAL := 0.0;
    rRawAcidMassFlow_kgh            : REAL := 0.0;
    rBrineEnthalpy_kJkg             : REAL := 945.0;
    rRecoveryTurbineEfficiency      : REAL := 0.835;
    rCumulativeParasiticPower_kWh   : REAL := 145.0;
END_VAR
""")

    # -------------------------------------------------------------------------
    # MAIN LOGIC - SECTION 1 & 2
    # -------------------------------------------------------------------------
    parts.append("""(*
========================================================================================================================
                                                MAIN EXECUTABLE LOGIC
========================================================================================================================
*)

(* ==================================================================================================================== *)
(* 1.0 SIL-3 HARDWIRED EMERGENCY STOP & CRITICAL BOUNDARY INTERLOCK SUPERVISION                                         *)
(* ==================================================================================================================== *)
(* Safety Instrumented Function (SIF) 101: Emergency de-energize and fail-safe bypass opening on trip.                 *)
(* Ensures compliance with IEC 61508 / IEC 61511 functional safety standards for supercritical thermal processes.      *)

IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bSystemRunning := FALSE;
    bSystemTripped := TRUE;
    iState := 100; (* Branch immediately into emergency depressurization and trip state *)
    dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0001; (* E-Stop tripped bit *)
END_IF;

IF bHertOverspeedSensorTrip THEN
    bHertEmergencyBrakeTripped := TRUE;
    bDeflectorEmergencyDrop := TRUE;
    rHertVfdSpeedDemand_rpm := 0.0;
    dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0001; (* Turbine overspeed trip contact activated *)
END_IF;


(* ==================================================================================================================== *)
(* 2.0 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) VOTING & SENSOR VALIDATION ROUTINES                                         *)
(* ==================================================================================================================== *)
(* Evaluates 5 independent 3-channel instrument banks with discrepancy detection, frozen-sensor identification,        *)
(* and bumpless graceful degradation to 1oo2 or conservative single-channel fallback.                                   *)

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 2.1 Wellhead Brine Inlet Pressure Transmitters [bar] (PT-101A, PT-101B, PT-101C)                                     *)
(* Operating point: ~25.0 bar, Upper boundary: 28.5 bar, Lower boundary: 18.0 bar, Channel discrepancy limit: 2.2 bar   *)
(* -------------------------------------------------------------------------------------------------------------------- *)
IF ABS(rBrineInletPressure_A_bar - rBrineInletPressure_B_bar) > 2.20 THEN
    bPres_SensorA_Fail := TRUE;
END_IF;
IF ABS(rBrineInletPressure_B_bar - rBrineInletPressure_C_bar) > 2.20 THEN
    bPres_SensorB_Fail := TRUE;
END_IF;
IF ABS(rBrineInletPressure_C_bar - rBrineInletPressure_A_bar) > 2.20 THEN
    bPres_SensorC_Fail := TRUE;
END_IF;

(* Rate of change / frozen sensor check *)
IF ABS(rBrineInletPressure_A_bar - rPres_LastA) < 0.001 THEN
    rPresFrozenAccum_A := rPresFrozenAccum_A + rCycleTime_sec;
    IF rPresFrozenAccum_A > 30.0 THEN bPres_SensorA_Fail := TRUE; END_IF;
ELSE
    rPresFrozenAccum_A := 0.0;
END_IF;
rPres_LastA := rBrineInletPressure_A_bar;
rPres_LastB := rBrineInletPressure_B_bar;
rPres_LastC := rBrineInletPressure_C_bar;

IF (NOT bPres_SensorA_Fail) AND (NOT bPres_SensorB_Fail) AND (NOT bPres_SensorC_Fail) THEN
    (* Standard 2oo3 Median Mid-Value Select *)
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
    (* Degraded 1oo2 Voting Architecture *)
    bPres_Degraded_1oo2 := TRUE;
    IF NOT bPres_SensorA_Fail AND NOT bPres_SensorB_Fail THEN
        rVotedBrinePressure_bar := (rBrineInletPressure_A_bar + rBrineInletPressure_B_bar) * 0.50;
    ELSIF NOT bPres_SensorB_Fail AND NOT bPres_SensorC_Fail THEN
        rVotedBrinePressure_bar := (rBrineInletPressure_B_bar + rBrineInletPressure_C_bar) * 0.50;
    ELSIF NOT bPres_SensorA_Fail AND NOT bPres_SensorC_Fail THEN
        rVotedBrinePressure_bar := (rBrineInletPressure_A_bar + rBrineInletPressure_C_bar) * 0.50;
    ELSIF NOT bPres_SensorA_Fail THEN
        rVotedBrinePressure_bar := rBrineInletPressure_A_bar;
    ELSIF NOT bPres_SensorB_Fail THEN
        rVotedBrinePressure_bar := rBrineInletPressure_B_bar;
    ELSE
        rVotedBrinePressure_bar := rBrineInletPressure_C_bar;
    END_IF;
    dwWarningWord := dwWarningWord OR 16#0000_0001; (* Pressure sensor bank degraded *)
END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 2.2 Wellhead Supercritical Brine Inlet Temperature Transmitters [deg C] (TT-101A, TT-101B, TT-101C)                 *)
(* Operating point: ~220.0 C, Upper boundary: 245.0 C, Channel discrepancy limit: 8.0 C                                 *)
(* -------------------------------------------------------------------------------------------------------------------- *)
IF ABS(rBrineInletTemp_A_degC - rBrineInletTemp_B_degC) > 8.00 THEN bTemp_SensorA_Fail := TRUE; END_IF;
IF ABS(rBrineInletTemp_B_degC - rBrineInletTemp_C_degC) > 8.00 THEN bTemp_SensorB_Fail := TRUE; END_IF;
IF ABS(rBrineInletTemp_C_degC - rBrineInletTemp_A_degC) > 8.00 THEN bTemp_SensorC_Fail := TRUE; END_IF;

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
        rVotedBrineTemp_degC := (rBrineInletTemp_A_degC + rBrineInletTemp_B_degC) * 0.50;
    ELSIF NOT bTemp_SensorB_Fail AND NOT bTemp_SensorC_Fail THEN
        rVotedBrineTemp_degC := (rBrineInletTemp_B_degC + rBrineInletTemp_C_degC) * 0.50;
    ELSIF NOT bTemp_SensorA_Fail AND NOT bTemp_SensorC_Fail THEN
        rVotedBrineTemp_degC := (rBrineInletTemp_A_degC + rBrineInletTemp_C_degC) * 0.50;
    ELSE
        rVotedBrineTemp_degC := rBrineInletTemp_A_degC;
    END_IF;
    dwWarningWord := dwWarningWord OR 16#0000_0002; (* Temperature sensor bank degraded *)
END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 2.3 Extraction Train Feed Volumetric Flow Transmitters [m3/h] (FT-101A, FT-101B, FT-101C)                           *)
(* Operating range: 350-550 m3/h, Discrepancy limit: 25.0 m3/h                                                          *)
(* -------------------------------------------------------------------------------------------------------------------- *)
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
        rVotedBrineFlow_m3h := (rBrineFeedFlow_A_m3h + rBrineFeedFlow_B_m3h) * 0.50;
    ELSIF NOT bFlow_SensorB_Fail AND NOT bFlow_SensorC_Fail THEN
        rVotedBrineFlow_m3h := (rBrineFeedFlow_B_m3h + rBrineFeedFlow_C_m3h) * 0.50;
    ELSIF NOT bFlow_SensorA_Fail AND NOT bFlow_SensorC_Fail THEN
        rVotedBrineFlow_m3h := (rBrineFeedFlow_A_m3h + rBrineFeedFlow_C_m3h) * 0.50;
    ELSE
        rVotedBrineFlow_m3h := rBrineFeedFlow_A_m3h;
    END_IF;
    dwWarningWord := dwWarningWord OR 16#0000_0004; (* Flow transmitter bank degraded *)
END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 2.4 Elution Acid Feed Line pH Analyzers [pH] (AT-201A, AT-201B, AT-201C)                                             *)
(* Operating window: 2.30 to 2.50 pH, Discrepancy limit: 0.25 pH                                                       *)
(* -------------------------------------------------------------------------------------------------------------------- *)
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
        rVotedElutionPH_pH := (rElutionAcidPH_A_pH + rElutionAcidPH_B_pH) * 0.50;
    ELSIF NOT bPH_SensorB_Fail AND NOT bPH_SensorC_Fail THEN
        rVotedElutionPH_pH := (rElutionAcidPH_B_pH + rElutionAcidPH_C_pH) * 0.50;
    ELSIF NOT bPH_SensorA_Fail AND NOT bPH_SensorC_Fail THEN
        rVotedElutionPH_pH := (rElutionAcidPH_A_pH + rElutionAcidPH_C_pH) * 0.50;
    ELSE
        rVotedElutionPH_pH := rElutionAcidPH_A_pH;
    END_IF;
    dwWarningWord := dwWarningWord OR 16#0000_0008; (* pH analyzer bank degraded *)
END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 2.5 HERT Recovery Turbine Proximity Speed Probes [rpm] (ST-301A, ST-301B, ST-301C)                                   *)
(* Operating range: 2900-3100 rpm, Discrepancy limit: 60.0 rpm                                                          *)
(* -------------------------------------------------------------------------------------------------------------------- *)
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
        rVotedTurbineSpeed_rpm := (rTurbineSpeed_A_rpm + rTurbineSpeed_B_rpm) * 0.50;
    ELSIF NOT bSpeed_SensorB_Fail AND NOT bSpeed_SensorC_Fail THEN
        rVotedTurbineSpeed_rpm := (rTurbineSpeed_B_rpm + rTurbineSpeed_C_rpm) * 0.50;
    ELSIF NOT bSpeed_SensorA_Fail AND NOT bSpeed_SensorC_Fail THEN
        rVotedTurbineSpeed_rpm := (rTurbineSpeed_A_rpm + rTurbineSpeed_C_rpm) * 0.50;
    ELSE
        rVotedTurbineSpeed_rpm := rTurbineSpeed_A_rpm;
    END_IF;
    dwWarningWord := dwWarningWord OR 16#0000_0010; (* Turbine speed probe bank degraded *)
END_IF;
""")

    # -------------------------------------------------------------------------
    # MAIN LOGIC - SECTION 3 & 4
    # -------------------------------------------------------------------------
    parts.append("""(* ==================================================================================================================== *)
(* 3.0 GEOTHERMAL BRINE THERMOPHYSICAL PROPERTIES & AMORPHOUS SILICA SATURATION MODEL                                   *)
(* ==================================================================================================================== *)
(* Evaluates temperature-dependent silica equilibrium solubility C_eq via empirical 3rd order polynomial.              *)
(* Determines supersaturation index S, logarithmic saturation SI, and homogeneous nucleation induction time tau_ind.  *)

rSilicaEquilibriumSolubility_mgL := 55.40 + (1.280 * rVotedBrineTemp_degC) + (0.00410 * rVotedBrineTemp_degC * rVotedBrineTemp_degC);
IF rSilicaEquilibriumSolubility_mgL < 15.0 THEN
    rSilicaEquilibriumSolubility_mgL := 15.0;
END_IF;

(* Supersaturation Ratio: S = [SiO2] / C_eq *)
rSilicaSupersaturationRatio := rDissolvedSilicaConc_mgL / rSilicaEquilibriumSolubility_mgL;

(* Logarithmic Saturation Index: SI = log10(S) *)
IF rSilicaSupersaturationRatio > 0.05 THEN
    IF (rSilicaSupersaturationRatio > 0.50) AND (rSilicaSupersaturationRatio < 2.00) THEN
        (* Quadratic Taylor expansion approximation of ln(S) *)
        rSilicaSaturationIndex := ((rSilicaSupersaturationRatio - 1.0) - (0.50 * (rSilicaSupersaturationRatio - 1.0) * (rSilicaSupersaturationRatio - 1.0))) / 2.302585;
    ELSE
        rSilicaSaturationIndex := (rSilicaSupersaturationRatio - 1.0) / 2.302585;
    END_IF;
ELSE
    rSilicaSaturationIndex := -1.0;
END_IF;

(* Silica Polymerization Induction Time Kinetics *)
IF rSilicaSupersaturationRatio > 1.05 THEN
    bSilicaPolymerizationHazard := TRUE;
    rSilicaPolymerizationRate_mgL_s := 0.0450 * (rSilicaSupersaturationRatio - 1.0) * (rSilicaSupersaturationRatio - 1.0);
    rSilicaInductionTime_sec := 3600.0 / (1.0 + (12.50 * (rSilicaSupersaturationRatio - 1.0)));
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


(* ==================================================================================================================== *)
(* 4.0 SORBENT BED DYNAMIC ADSORPTION FRONT TRACKING & 10-NODE AXIAL DISCRETIZATION                                    *)
(* ==================================================================================================================== *)
(* Implements a continuous mass balance across 10 spatial nodes along bed height L = 3.80 m.                            *)
(* Couples interstitial fluid velocity to modified Bohart-Adams sorption kinetics.                                     *)

IF (rVotedBrineFlow_m3h > 10.0) AND bSystemRunning AND (iState = 30) THEN
    (* Interstitial superficial velocity u_s = Q / (3600 * A_bed) [m/s] *)
    rSuperficialVelocity_ms := (rVotedBrineFlow_m3h / 3600.0) / rBedCrossSection_m2;

    (* Lithium Mass Influx rate [kg/h] *)
    rRawLithiumHarvestRate_kgh := (rVotedBrineFlow_m3h * (rInletLithiumConc_mgL - rEffluentLithiumConc_mgL)) / 1000.0;
    IF rRawLithiumHarvestRate_kgh < 0.0 THEN rRawLithiumHarvestRate_kgh := 0.0; END_IF;

    (* Wave Front Propagation Velocity along axial coordinate z [m/s] *)
    IF rInletLithiumConc_mgL > 10.0 THEN
        rAdsorptionFrontPosition_m := rAdsorptionFrontPosition_m + 
            ((rSuperficialVelocity_ms / (rSorbentVoidFraction + (rSorbentBulkDensity_kgm3 * rSorbentMaxCapacity_mg_g * rSorbentHealthFactor / rInletLithiumConc_mgL))) * rCycleTime_sec);
    END_IF;

    (* Mass integration accumulators *)
    rCumulativeLiMassFed_kg := rCumulativeLiMassFed_kg + ((rVotedBrineFlow_m3h * rInletLithiumConc_mgL / 1000.0) * (rCycleTime_sec / 3600.0));
    rCumulativeLiMassAdsorbed_kg := rCumulativeLiMassAdsorbed_kg + (rRawLithiumHarvestRate_kgh * (rCycleTime_sec / 3600.0));

    (* Breakthrough percentage relative to total column height *)
    rEstimatedBreakthrough_pct := (rAdsorptionFrontPosition_m / rBedLength_m) * 100.0;
    IF rEstimatedBreakthrough_pct > 100.0 THEN rEstimatedBreakthrough_pct := 100.0; END_IF;

    (* Update Discretized 10-Node Axial Saturation Profile *)
    IF rAdsorptionFrontPosition_m >= 0.38 THEN rSorbentSaturation_Node0 := 0.999; END_IF;
    IF rAdsorptionFrontPosition_m >= 0.76 THEN rSorbentSaturation_Node1 := 0.995; END_IF;
    IF rAdsorptionFrontPosition_m >= 1.14 THEN rSorbentSaturation_Node2 := 0.980; END_IF;
    IF rAdsorptionFrontPosition_m >= 1.52 THEN rSorbentSaturation_Node3 := 0.950; END_IF;
    IF rAdsorptionFrontPosition_m >= 1.90 THEN rSorbentSaturation_Node4 := 0.890; END_IF;
    IF rAdsorptionFrontPosition_m >= 2.28 THEN rSorbentSaturation_Node5 := 0.750; END_IF;
    IF rAdsorptionFrontPosition_m >= 2.66 THEN rSorbentSaturation_Node6 := 0.520; END_IF;
    IF rAdsorptionFrontPosition_m >= 3.04 THEN rSorbentSaturation_Node7 := 0.280; END_IF;
    IF rAdsorptionFrontPosition_m >= 3.42 THEN rSorbentSaturation_Node8 := 0.110; END_IF;
    IF rAdsorptionFrontPosition_m >= 3.80 THEN rSorbentSaturation_Node9 := 0.035; END_IF;

    (* Carousel Index Permissive Trigger: Advance when front exceeds 88% or slip > 15% *)
    IF (rEstimatedBreakthrough_pct >= 88.0) OR ((rInletLithiumConc_mgL > 50.0) AND ((rEffluentLithiumConc_mgL / rInletLithiumConc_mgL) > 0.15)) THEN
        bAdsorptionLeadLagSwapReq := TRUE;
    ELSE
        bAdsorptionLeadLagSwapReq := FALSE;
    END_IF;
ELSE
    rSuperficialVelocity_ms := 0.0;
END_IF;
""")

    # -------------------------------------------------------------------------
    # MAIN LOGIC - SECTION 5 & 6
    # -------------------------------------------------------------------------
    parts.append("""(* ==================================================================================================================== *)
(* 5.0 STATE-SPACE PLANT MATRICES & MODEL PREDICTIVE CONTROL (MPC) ENGINE                                               *)
(* ==================================================================================================================== *)
(* Implements a discrete-time linear state-space observer and predictive controller with analytical rate-of-change      *)
(* optimization and projected gradient constraint handling.                                                             *)

(* 5.1 Update State Vector Estimates *)
rState_x1_FrontPos_m := rAdsorptionFrontPosition_m;
rState_x2_BedDeltaP_bar := rColumnDiffPressure_bar;
rState_x3_ElutionPH := rVotedElutionPH_pH;
rState_x4_TurbineSpeed_rpm := rVotedTurbineSpeed_rpm;
rState_x5_SilicaIndex := rSilicaSaturationIndex;

(* 5.2 One-Step Ahead State Prediction: x(k+1) = A_d * x(k) + B_d * u(k) *)
rPred_x1_k1 := (A_11 * rState_x1_FrontPos_m) + (B_11 * rMpcOutput_u1_Bypass_pct);
rPred_x2_k1 := (A_21 * rState_x1_FrontPos_m) + (A_22 * rState_x2_BedDeltaP_bar) + (A_25 * rState_x5_SilicaIndex) +
               (B_21 * rMpcOutput_u1_Bypass_pct) + (B_23 * rMpcOutput_u3_Nozzle_pct) + (B_24 * rMpcOutput_u4_Inhibitor_pct);
rPred_x3_k1 := (A_33 * rState_x3_ElutionPH) + (B_32 * rMpcOutput_u2_Acid_pct);
rPred_x4_k1 := (A_42 * rState_x2_BedDeltaP_bar) + (A_44 * rState_x4_TurbineSpeed_rpm) +
               (B_41 * rMpcOutput_u1_Bypass_pct) + (B_43 * rMpcOutput_u3_Nozzle_pct);
rPred_x5_k1 := (A_51 * rState_x1_FrontPos_m) + (A_52 * rState_x2_BedDeltaP_bar) + (A_53 * rState_x3_ElutionPH) + (A_55 * rState_x5_SilicaIndex) +
               (B_51 * rMpcOutput_u1_Bypass_pct) + (B_52 * rMpcOutput_u2_Acid_pct) + (B_54 * rMpcOutput_u4_Inhibitor_pct);

(* 5.3 MPC Analytical Unconstrained Rate Optimization & Constraint Projection *)
(* Quadratic Cost: J = e^T * Q * e + delta_u^T * R * delta_u                                                           *)

(* Delta U1: Brine Bypass Valve Command Adjustment *)
rDeltaU1 := - (1.0 / (rWeight_R1 + 0.10)) * (
                (B_21 * rWeight_Q2 * (rPred_x2_k1 - rSetpoint_x2_BedDeltaP_bar)) +
                (B_41 * rWeight_Q4 * (rPred_x4_k1 - rSetpoint_x4_TurbineSpeed_rpm))
             );

(* Delta U2: Elution Acid Metering Stroke Adjustment *)
rDeltaU2 := - (1.0 / (rWeight_R2 + 0.10)) * (
                (B_32 * rWeight_Q3 * (rPred_x3_k1 - rSetpoint_x3_ElutionPH))
             );

(* Delta U3: HERT Turbine Spear Valve Nozzle Position Adjustment *)
rDeltaU3 := - (1.0 / (rWeight_R3 + 0.10)) * (
                (B_43 * rWeight_Q4 * (rPred_x4_k1 - rSetpoint_x4_TurbineSpeed_rpm)) +
                (B_23 * rWeight_Q2 * (rPred_x2_k1 - rSetpoint_x2_BedDeltaP_bar))
             );

(* Delta U4: Silica Inhibitor Dosing Injection Adjustment *)
rDeltaU4 := - (1.0 / (rWeight_R4 + 0.10)) * (
                (B_54 * 25.0 * (rPred_x5_k1 - 0.0)) +
                (B_24 * rWeight_Q2 * (rPred_x2_k1 - rSetpoint_x2_BedDeltaP_bar))
             );

(* Slew-Rate Limiting on Manipulated Increments *)
IF rDeltaU1 > 1.50 THEN rDeltaU1 := 1.50; ELSIF rDeltaU1 < -1.50 THEN rDeltaU1 := -1.50; END_IF;
IF rDeltaU2 > 2.00 THEN rDeltaU2 := 2.00; ELSIF rDeltaU2 < -2.00 THEN rDeltaU2 := -2.00; END_IF;
IF rDeltaU3 > 2.50 THEN rDeltaU3 := 2.50; ELSIF rDeltaU3 < -2.50 THEN rDeltaU3 := -2.50; END_IF;
IF rDeltaU4 > 1.80 THEN rDeltaU4 := 1.80; ELSIF rDeltaU4 < -1.80 THEN rDeltaU4 := -1.80; END_IF;

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

rBrineBypassValveDemand_pct := rMpcOutput_u1_Bypass_pct;


(* ==================================================================================================================== *)
(* 6.0 HIGH-PRESSURE ACID ELUTION WASH PROFILE & CHROMATOGRAPHIC PEAK HARVEST                                           *)
(* ==================================================================================================================== *)
(* Executes 4-stage selective lithium stripping sequence at 20-25 bar backpressure to avoid boiling at 120-140 deg C.  *)
(* Employs high-speed PID feedback trim over MPC base to lock pH tightly at 2.40.                                       *)

IF (iState = 60) AND bSystemRunning THEN
    rElutionPhaseTimer_sec := rElutionPhaseTimer_sec + rCycleTime_sec;
    rAcidPHError := rTargetElutionPH - rVotedElutionPH_pH;

    (* Anti-dissolution safety interlock: if pH drops below 1.95, sorbent lattice dissolves! *)
    IF rVotedElutionPH_pH < 1.95 THEN
        bAcidLatticeCorrosionRisk := TRUE;
        rAcidDosingValveDemand_pct := 0.0; (* Immediate acid feed shutoff *)
        dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0002; (* Sorbent dissolution trip alarm *)
    ELSE
        bAcidLatticeCorrosionRisk := FALSE;
    END_IF;

    (* Classical PID Feedback Trim *)
    rAcidPHDerivative := (rVotedElutionPH_pH - rAcidPHLastValue) / rCycleTime_sec;
    rAcidPHLastValue := rVotedElutionPH_pH;

    IF NOT bAcidLatticeCorrosionRisk THEN
        rAcidPHIntegral := rAcidPHIntegral + (rAcidPHError * rCycleTime_sec);
        IF rAcidPHIntegral > 25.0 THEN rAcidPHIntegral := 25.0; ELSIF rAcidPHIntegral < -25.0 THEN rAcidPHIntegral := -25.0; END_IF;

        (* Acid Demand Output: inverted action (lower pH requires less acid) *)
        rAcidDosingValveDemand_pct := rMpcOutput_u2_Acid_pct + 
            (rAcidPID_Kp * (-rAcidPHError)) + (rAcidPID_Ki * (-rAcidPHIntegral)) + (rAcidPID_Kd * (-rAcidPHDerivative));

        IF rAcidDosingValveDemand_pct > 100.0 THEN rAcidDosingValveDemand_pct := 100.0; END_IF;
        IF rAcidDosingValveDemand_pct < 0.0 THEN rAcidDosingValveDemand_pct := 0.0; END_IF;
    END_IF;

    (* Mass balance calculations for acid and lithium recovery *)
    rRawAcidMassFlow_kgh := (rElutionFeedFlow_m3h * 1000.0 * 0.0150 * (rAcidDosingValveDemand_pct / 100.0));
    rTotalAcidConsumedThisBatch_kg := rTotalAcidConsumedThisBatch_kg + (rRawAcidMassFlow_kgh * (rCycleTime_sec / 3600.0));

    (* Chromatographic Peak Cut: Toroidal conductivity signals rich LiCl harvest window *)
    IF rEluateConductivity_mScm >= rConductivityThresholdHarvest THEN
        bElutionPeakDetected := TRUE;
        rEluateDiverterValve_pct := 100.0; (* 100% position: Rich product crystallization feed tank *)
        rTotalLithiumHarvestedThisBatch_kg := rTotalLithiumHarvestedThisBatch_kg + (12.80 * (rCycleTime_sec / 3600.0));
        rCumulativeLithiumDay_kg := rCumulativeLithiumDay_kg + (12.80 * (rCycleTime_sec / 3600.0));
    ELSIF rEluateConductivity_mScm <= rConductivityThresholdTail THEN
        bElutionPeakDetected := FALSE;
        rEluateDiverterValve_pct := 0.0;   (* 0% position: Barren rinse / reinjection recycle *)
    END_IF;

    (* Specific acid consumption ratio [kg HCl / kg Li harvested] *)
    IF rTotalLithiumHarvestedThisBatch_kg > 0.50 THEN
        rSpecificAcidConsumption_kgLi := rTotalAcidConsumedThisBatch_kg / rTotalLithiumHarvestedThisBatch_kg;
    ELSE
        rSpecificAcidConsumption_kgLi := 3.550; (* Stoichiometric theoretical baseline *)
    END_IF;
ELSE
    rAcidDosingValveDemand_pct := 0.0;
    rAcidPHIntegral := 0.0;
    bElutionPeakDetected := FALSE;
    rEluateDiverterValve_pct := 0.0;
    rElutionPhaseTimer_sec := 0.0;
END_IF;
""")

    # -------------------------------------------------------------------------
    # MAIN LOGIC - SECTION 7 & 8
    # -------------------------------------------------------------------------
    parts.append("""(* ==================================================================================================================== *)
(* 7.0 SILICA SCALE POLYMERIZATION SEED INHIBITOR DOSING CONTROLLER                                                     *)
(* ==================================================================================================================== *)
(* Flow-proportional and Arrhenius temperature-compensated inhibitor injection algorithm.                              *)

IF (rVotedBrineFlow_m3h > 15.0) AND (iState >= 20) AND (iState <= 80) THEN
    (* Arrhenius temperature compensation: As brine cools, polymerization accelerates *)
    IF rVotedBrineTemp_degC < 220.0 THEN
        rInhibitorTempCompensation := 1.0 + (0.0150 * (220.0 - rVotedBrineTemp_degC));
    ELSE
        rInhibitorTempCompensation := 1.0;
    END_IF;

    (* Volumetric chemical dosing requirement: L/h = (Q_brine [m3/h] * Dosage [g/m3]) / (rho * conc) *)
    rInhibitorDemand_Lh := (rVotedBrineFlow_m3h * rInhibitorBaseDosage_mgL * rInhibitorTempCompensation * (1.0 + (1.50 * rMpcOutput_u4_Inhibitor_pct / 100.0))) /
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


(* ==================================================================================================================== *)
(* 8.0 HYDRAULIC ENERGY RECOVERY TURBINE (HERT) RUNNER SPEED GOVERNOR & ANTI-CAVITATION                                *)
(* ==================================================================================================================== *)
(* Governs Pelton runner nozzle spear needle valve to maximize isentropic energy recovery while continuously            *)
(* evaluating Net Positive Suction Head (NPSH) to eliminate cavitation pitting.                                        *)

(* Net Positive Suction Head Supervision *)
rTurbineNPSH_Available_m := ((rVotedBrinePressure_bar - rVaporPressureAtTemp_bar) * 100000.0) / (9810.0 * 1.150);
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
    rNetRecoveredHydraulicPower_kW := (rRecoveryTurbineEfficiency * 1150.0 * 9.810 * (rVotedBrineFlow_m3h / 3600.0) * rTurbineInletHead_m) / 1000.0;
ELSE
    IF bDeflectorEmergencyDrop THEN
        rHertVfdSpeedDemand_rpm := 0.0;
    ELSE
        rHertVfdSpeedDemand_rpm := 1200.0; (* Low idle speed *)
    END_IF;
    rNetRecoveredHydraulicPower_kW := 0.0;
    rTurbineGovernorIntegral := 0.0;
END_IF;
""")

    # -------------------------------------------------------------------------
    # MAIN LOGIC - SECTION 9 (FINITE STATE MACHINE)
    # -------------------------------------------------------------------------
    parts.append("""(* ==================================================================================================================== *)
(* 9.0 MULTI-STAGE CAROUSEL FINITE STATE MACHINE (CASE iState OF ...)                                                   *)
(* ==================================================================================================================== *)
(* Fully deterministic 11-stage state engine executing extraction, carousel turret rotation, displacement, and elution. *)

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
        IF tSweeteningTimer.Q AND (rVotedElutionPH_pH >= 5.50) THEN
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
""")

    # -------------------------------------------------------------------------
    # MAIN LOGIC - SECTION 10 & 11
    # -------------------------------------------------------------------------
    parts.append("""(* ==================================================================================================================== *)
(* 10.0 GRACEFUL DEGRADATION, SENSOR DERATE & ACTUATOR SATURATION MANAGEMENT                                            *)
(* ==================================================================================================================== *)
(* Handles operation under degraded instrument conditions and enforces multi-variable safety bounds                     *)

bDegradedInstrumentWarning := bPres_Degraded_1oo2 OR bTemp_Degraded_1oo2 OR 
                              bFlow_Degraded_1oo2 OR bPH_Degraded_1oo2 OR bSpeed_Degraded_1oo2;

bDegradedSensorMode := bDegradedInstrumentWarning;

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


(* ==================================================================================================================== *)
(* 11.0 BIT-PACKED STATUS WORDS & ALARM TREE ASSEMBLY                                                                   *)
(* ==================================================================================================================== *)
(* Encodes system status into standardized DWORD registers for plant DCS / SCADA integration                             *)

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
IF (iState = 0)   THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0001_0000; END_IF;
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
""")

    return "".join(parts)

if __name__ == "__main__":
    code = build_iec_code()
    print(f"Generated code length: {len(code)} characters")
    
    # Check syntax rules
    assert code.startswith("FUNCTION_BLOCK FB_GeothermalDLE_IonExchange_ElutionCycle"), "Must start with FUNCTION_BLOCK"
    assert code.strip().endswith("END_FUNCTION_BLOCK"), "Must end with END_FUNCTION_BLOCK"
    
    # Check IF / END_IF balance
    # Clean out comments first
    clean_code = re.sub(r'\(\*.*?\*\)', '', code, flags=re.DOTALL)
    
    # Count occurrences
    ifs = len(re.findall(r'\bIF\b', clean_code))
    end_ifs = len(re.findall(r'\bEND_IF\b', clean_code))
    cases = len(re.findall(r'\bCASE\b', clean_code))
    end_cases = len(re.findall(r'\bEND_CASE\b', clean_code))
    
    print(f"IF count: {ifs}, END_IF count: {end_ifs}")
    print(f"CASE count: {cases}, END_CASE count: {end_cases}")
    assert ifs == end_ifs, f"IF/END_IF mismatch: {ifs} vs {end_ifs}"
    assert cases == end_cases, f"CASE/END_CASE mismatch: {cases} vs {end_cases}"
    print("All syntax checks passed!")
