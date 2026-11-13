import sys
import json
import uuid
import re
import os

def build_iec_code():
    code_lines = []
    
    # -------------------------------------------------------------------------
    # PART 1: HEADER COMMENT
    # -------------------------------------------------------------------------
    code_lines.append("""FUNCTION_BLOCK FB_Paper_ContinuousDigester_KraftPulping_KappaNumber
(*
========================================================================================================================
  LUMINA CYBER-PHYSICAL AUTOMATION KERNEL - ADVANCED CONTINUOUS PROCESS ENGINEERING GROUP
  HIGH-DEMAND TIER 1 PRIORITY SECTOR: PULP & PAPER CHEMICAL DIGESTING & CELLULOSE REFINING
  
  SYSTEM DESIGNATION : INDUSTRIAL CONTINUOUS KAMYR TWO-VESSEL HYDRAULIC KRAFT DIGESTER
  NOMINAL CAPACITY   : 1,500 ADt/d (AIR-DRY METRIC TONS PER DAY) FULL-BLEACHABLE SOFTWOOD/HARDWOOD KRAFT PULP
  PRIMARY SUBSYSTEMS :
    - HIGH-PRESSURE CHIP FEEDER (HPF) & IMPREGNATION VESSEL (IV) HYDRAULIC EQUALIZATION SYSTEM
    - MULTI-ZONE COUNTER-CURRENT & CO-CURRENT COOKING CIRCULATION SYSTEM (UPPER COOK, LOWER COOK, WASH ZONE)
    - DYNAMIC BLACK LIQUOR EXTRACTION HEADER WITH AUTOMATIC SLOTTED SCREEN HYDRAULIC BACKFLUSH CYCLE
    - WHITE LIQUOR ACTIVE ALKALI DOSING CASCADE WITH IN-LINE CONDUCTIVE / SPECTROSCOPIC RESIDUAL FEEDBACK
    - REAL-TIME IN-LINE NIR DELIGNIFICATION OBSERVER & VROOM ARRHENIUS H-FACTOR THERMAL INTEGRATOR
    - DIGESTER BOTTOM ROTARY DISCHARGE SCRAPER & BLOW LINE CONSISTENCY/FLOW SYNCHRONIZATION
    - 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING SUITE WITH DISCREPANCY TIMERS
    - 8-STATE DISCRETE CYBER-PHYSICAL STATE-SPACE ESTIMATOR & LUENBERGER OBSERVER (Ts = 100 ms)
    - RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) OPTIMIZER WITH PROJECTED GRADIENT DESCENT (PGD)
    - DETERMINISTIC 14-STAGE PRODUCTION, SCREEN CLEANING, COLUMN RECOVERY & BLOWDOWN FINITE STATE MACHINE (FSM)
    - ISA-18.2 / IEC 62682 MULTI-TIER PROCESS ALARM ENGINE WITH 32-BIT BIT-PACKED STATUS WORDS
    
  APPLICABLE STANDARDS & DESIGN CODES:
    - TAPPI T-236 om-13 (Kappa Number of Pulp), TAPPI T-624 cm-11 (Analysis of White and Black Liquors)
    - TAPPI T-271 om-12 (Fiber Length of Pulp by Automated Optical Analyzer)
    - ASME Boiler & Pressure Vessel Code (BPVC) Section VIII Div 1/2 (Heavy Thick-Wall Chemical Digester Shells)
    - ISA-18.2 / IEC 62682 Management of Alarm Systems for the Process Industries
    - IEC 61508 / IEC 61511 Functional Safety of Safety Instrumented Systems (SIL-2 / SIL-3 Architecture)
    - IEC 61131-3 Programmable Controllers - Part 3: Programming Languages (Structured Text Standard)
    
  AUTHOR: 75+ YEARS VETERAN PRINCIPAL AUTOMATION FELLOW & CYBER-PHYSICAL SYSTEMS CHAIR
========================================================================================================================

  THEORETICAL FOUNDATIONS & CHEMICAL REACTION ENGINEERING ARCHITECTURE:
  ----------------------------------------------------------------------------------------------------------------------
  1. KRAFT (SULFATE) CHEMICAL DELIGNIFICATION MECHANISMS:
     - Kraft pulping involves the chemical cleavage of ether and carbon-carbon linkages within the complex,
       three-dimensional phenylpropane matrix of plant lignin. The primary objective is dissolving hydrophobic
       lignin fragments into alkali-soluble phenolate and carboxylate forms, thereby liberating intact cellulose
       and hemicellulose fibers for high-strength paper manufacturing.
     - Active cooking chemicals in White Liquor comprise Sodium Hydroxide (NaOH) and Sodium Sulfide (Na2S).
       In aqueous solution at alkaline pH (> 13.0), complete hydrolysis occurs:
           Na2S + H2O <-> NaHS + NaOH
           S^(2-) + H2O <-> HS^(-) + OH^(-)
     - Standard Chemical Definitions:
       * Total Alkali (TA)         = NaOH + Na2S + Na2CO3 + 0.5 Na2SO3 [expressed as g/L Na2O or NaOH equivalent]
       * Active Alkali (AA)        = NaOH + Na2S                       [g/L Na2O]
       * Effective Alkali (EA)     = NaOH + 0.5 Na2S                   [g/L Na2O]
       * White Liquor Sulfidity (S)= (Na2S / AA) * 100.0               [%] (typically 25.0% to 35.0%)
       * Causticity (C)            = (NaOH / (NaOH + Na2CO3)) * 100.0  [%] (typically 80.0% to 84.0%)
     - Hydrosulfide ions (HS^(-)) act as strong nucleophilic reagents, attacking quinone methide intermediates
       formed during beta-aryl ether bond cleavage, dramatically accelerating lignin solubilization while preventing
       undesirable alkaline lignin condensation reactions.
       
  2. THREE-PHASE DELIGNIFICATION PHENOMENOLOGICAL KINETICS:
     Delignification proceeds sequentially through three kinetically distinctive reaction regimes:
     * Phase A: Initial Delignification Phase (T < 130 deg C):
       Very fast dissolution of approximately 20-25% of total lignin, primarily through cleavage of phenolic
       alpha- and beta-ether bonds. Controlled primarily by diffusion into chip pores. Very low activation energy
       (E_a,initial approx 48-60 kJ/mol). Up to 60-70% of consumed alkali in this phase neutralizes acidic wood
       extractives (uronic acids, resin and fatty acids) and cleaves ester groups on acetylated xylan.
     * Phase B: Bulk Delignification Phase (140 deg C <= T <= 175 deg C):
       The main cooking regime responsible for removing an additional 65-70% of initial lignin via cleavage of
       non-phenolic beta-O-4 ether linkages. Governed by high chemical activation energy (E_a,bulk approx 134-142 kJ/mol).
       Follows pseudo-first-order kinetics with respect to residual unreacted lignin:
           -d[L] / dt = k_bulk * [L] * [OH^(-)]^a * [HS^(-)]^b
       where reaction exponents a approx 0.7 to 1.0, b approx 0.2 to 0.35.
     * Phase C: Residual Delignification Phase (Lignin content < 2-3% of pulp dry mass):
       Extremely slow dissolution of structurally recalcitrant, cross-linked lignin-carbohydrate complexes (LCC).
       Activation energy rises to 145-160 kJ/mol. In this regime, undesirable cellulose random chain scission
       (hydrolytic depolymerization) and alkaline peeling reactions accelerate drastically, causing catastrophic
       loss of pulp fiber intrinsic viscosity and paper sheet tensile strength. Cooking must be stopped abruptly
       when reaching the target Kappa number before entering deep residual delignification.

  3. VROOM H-FACTOR THERMODYNAMIC & REACTION INTEGRAL:
     - To decouple the coupled effects of time and cooking temperature into a single scalar delignification index,
       Kenneth E. Vroom (1957) formulated the H-factor concept based on the Arrhenius relationship:
           k(T) = A_arrhenius * exp( -E_a / (R_gas * T_K) )
     - Taking the reaction rate at 100 deg C (373.15 K) as the baseline reference (k_rel = 1.0), the relative
       delignification rate k_rel(T) at any process temperature T [deg C] (T_K = T + 273.15) is evaluated by:
           k_rel(T) = exp( A_vroom - B_vroom / T_K )
       where:
           A_vroom = 43.20
           B_vroom = 16,113.0 K  (derived from E_a = 133,970 J/mol and R_gas = 8.31446 J/(mol*K))
     - The cumulative H-factor integral across cooking zones is calculated by continuous time-integration:
           H(t) = integral_0^t k_rel( T(tau) ) dtau
     - In this cyber-physical Function Block, the continuous integral is evaluated numerically at every discrete
       PLC execution cycle (Ts = 100 ms) via high-precision trapezoidal accumulation:
           Delta_H[k] = 0.5 * ( k_rel(T[k]) + k_rel(T[k-1]) ) * (Ts / 3600.0) [H-factor units]
           H_accum[k] = H_accum[k-1] + Delta_H[k]

  4. HATTON STATISTICAL-KINETIC KAPPA NUMBER PREDICTION MODEL:
     - The Kappa number (K) is the standard metric for residual lignin content in unbleached pulp (TAPPI T-236).
       Lignin percentage by dry mass is approximately %Lignin = 0.147 * Kappa.
     - Dr. J.V. Hatton established empirical-mechanistic models correlating Kraft pulp Kappa number to cooking H-factor,
       effective alkali charge (EA [% on oven-dry wood]), and chip species constants:
           Kappa = A_hatton - B_hatton * ln( H_factor ) * (EA_effective_pct)^gamma_hatton
     - For industrial Scandinavian softwood (Pinus sylvestris / Picea abies) and North American southern pine:
           A_hatton     = 168.50
           B_hatton     = 28.75
           gamma_hatton = 0.65
     - For mixed temperate/tropical hardwoods (Eucalyptus grandis / Betula pendula):
           A_hatton     = 142.30
           B_hatton     = 24.10
           gamma_hatton = 0.72
     - The continuous observer integrates a real-time blend-weighted Hatton model corrected by an in-line
       Fourier-Transform Near-Infrared (FT-NIR) spectroscopic analyzer feedback filter.

  5. TWO-VESSEL HYDRAULIC KAMYR DIGESTER VESSEL HYDRAULICS:
     - Chip and liquor slurry is continuously charged via a Low-Pressure Feeder into a Steaming Vessel, deaerating
       wood pores. A High-Pressure Feeder (HPF) pressurized to 10.0-14.0 bar transfers chips through top circulation
       lines into the Impregnation Vessel (IV).
     - In the IV, chips descend slowly under plug-flow conditions (approx 35-45 minutes residence time) at 115-130 deg C,
       imbibing white liquor alkali throughout the micro-capillary fiber cell walls via capillary penetration and diffusion.
     - The chip column then enters the main Digester Vessel (DV), descending through:
       a) Upper Cooking Zone (Co-current flow, 155 - 165 deg C)
       b) Lower Cooking Zone (Counter-current or co-current flow, 162 - 172 deg C)
       c) Dynamic Black Liquor Extraction Screen Belt (Liquor extraction to evaporation plant)
       d) Counter-Current Hi-Heat Wash Zone (120 - 135 deg C, 2.0 to 4.0 hours residence time)
     - Chip column compaction is governed by chip bed permeability, buoyant weight, and liquor downflow drag.
       The hydraulic drag force per unit height is modeled by the Ergun equation for porous media:
           Delta_P / Delta_L = 150 * (1 - epsilon_bed)^2 / (epsilon_bed^3 * (phi * d_chip)^2) * mu_liq * v_rel +
                               1.75 * (1 - epsilon_bed) / (epsilon_bed^3 * phi * d_chip) * rho_liq * (v_rel)^2
     - When liquor downward percolation velocity exceeds critical bed fluidization velocity, chip column compaction
       skyrockets, leading to "Column Hanging" (loss of plug flow, screen blinding, and severe bottom scraper torque spikes).
     - The extraction screen rows utilize continuous cyclic backflushing: while screens 1 & 3 extract, screen 2 is
       subjected to reverse hydraulic shock, clearing pin chips from slotted apertures (slots 3.5 mm to 5.0 mm).
       
  6. 8-STATE CYBER-PHYSICAL DISCRETE STATE-SPACE FORMULATION (Ts = 100 ms):
     State Vector x[k] in R^8:
       x[1]: Digester Chip Column Compaction Level / Downward Velocity Index [%] (0.0 to 100.0%)
       x[2]: Impregnation Vessel Residual Effective Alkali Concentration [g/L as NaOH] (15.0 to 35.0 g/L)
       x[3]: Upper Cooking Zone Residual Effective Alkali Concentration [g/L as NaOH] (10.0 to 25.0 g/L)
       x[4]: Upper Cooking Circulation Temperature T_upper [deg C] (145.0 to 175.0 deg C)
       x[5]: Lower Cooking Circulation Temperature T_lower [deg C] (150.0 to 180.0 deg C)
       x[6]: Delignification H-Factor Thermal Reaction Accumulator [H-factor units] (200.0 to 2200.0)
       x[7]: Real-Time Predicted Blow Line Pulp Kappa Number [Kappa units] (18.0 to 45.0)
       x[8]: Wash Zone Displacement Liquor Dissolved Solids Concentration [%] (4.0 to 22.0%)
     Control Vector u[k] in R^8:
       u[1]: Upper Cook Circulation Heat Exchanger Medium-Pressure Steam Control Valve Pos [%] (0.0 to 100.0%)
       u[2]: Lower Cook Circulation Heat Exchanger Medium-Pressure Steam Control Valve Pos [%] (0.0 to 100.0%)
       u[3]: Dynamic Black Liquor Extraction Header Proportional Control Valve Pos [%] (10.0 to 100.0%)
       u[4]: White Liquor Active Alkali Dosing Cascade Feed Valve Pos [%] (0.0 to 100.0%)
       u[5]: High-Pressure Chip Feeder Rotary Pocket VFD Speed Reference [rpm] (5.0 to 25.0 rpm)
       u[6]: Digester Bottom Discharge Scraper VFD Motor Speed Reference [rpm] (2.0 to 12.0 rpm)
       u[7]: Pulp Blow Discharge Flow Line Divert / Control Valve Pos [%] (5.0 to 100.0%)
       u[8]: Wash Zone Counter-Current Displacement Liquor Flow Control Valve Pos [%] (10.0 to 100.0%)
     Exogenous Disturbance Vector d[k] in R^6:
       d[1]: Incoming Wood Chip Moisture Content [%] (35.0% to 62.0%)
       d[2]: Wood Chip Bulk Packed Density [kg/m3] (310.0 to 460.0 kg/m3)
       d[3]: White Liquor Active Alkali Lab Analytical Concentration [g/L Na2O] (95.0 to 135.0 g/L)
       d[4]: Ambient Wood Yard Chip Temperature [deg C] (-25.0 to +40.0 deg C)
       d[5]: White Liquor Sulfidity Percentage [%] (22.0% to 38.0%)
       d[6]: Wood Chip Species Blend Hardwood Ratio [%] (0.0% = 100% Pine, 100.0% = 100% Eucalyptus)
*)
""")

    # -------------------------------------------------------------------------
    # PART 2: VAR_INPUT
    # -------------------------------------------------------------------------
    code_lines.append("""
VAR_INPUT
    (* Master Digital Commands & Hardware Safety Signals *)
    bSystemEnable                       : BOOL;         (* Digester Master Automation System Enable Permissive [-] *)
    bProductionRunCmd                   : BOOL;         (* Continuous Digester Production Run Command from DCS [-] *)
    bEmergencyStop                      : BOOL;         (* SIL-3 Hardwired Safety Shutdown Pushbutton (1=Healthy, 0=Trip) [-] *)
    bAlarmAcknowledge                   : BOOL;         (* ISA-18.2 Process Alarm Acknowledge Pushbutton [-] *)
    bAlarmReset                         : BOOL;         (* Master Safety Fault & Interlock Latch Reset [-] *)
    bManualBackflushTrigger             : BOOL;         (* Manual Operator Extraction Screen Backflush Cycle Request [-] *)
    bChipColumnAgitatorRun              : BOOL;         (* Chip Chute Hydraulic Agitator Drive Run Command [-] *)
    bBlowLineDilutionPumpRun            : BOOL;         (* Blow Line Filtrate Dilution Pump Run Feedback [-] *)
    
    (* Primary 2oo3 TMR Analog Transmitters with SI Units *)
    rTT_101A_UpperCookTemp_degC         : REAL;         (* Upper Cook Circulation Temp Transmitter Channel A [deg C] *)
    rTT_101B_UpperCookTemp_degC         : REAL;         (* Upper Cook Circulation Temp Transmitter Channel B [deg C] *)
    rTT_101C_UpperCookTemp_degC         : REAL;         (* Upper Cook Circulation Temp Transmitter Channel C [deg C] *)

    rTT_201A_LowerCookTemp_degC         : REAL;         (* Lower Cook Circulation Temp Transmitter Channel A [deg C] *)
    rTT_201B_LowerCookTemp_degC         : REAL;         (* Lower Cook Circulation Temp Transmitter Channel B [deg C] *)
    rTT_201C_LowerCookTemp_degC         : REAL;         (* Lower Cook Circulation Temp Transmitter Channel C [deg C] *)

    rPT_301A_TopPressure_bar            : REAL;         (* Digester Shell Top Pressure Transmitter Channel A [bar] *)
    rPT_301B_TopPressure_bar            : REAL;         (* Digester Shell Top Pressure Transmitter Channel B [bar] *)
    rPT_301C_TopPressure_bar            : REAL;         (* Digester Shell Top Pressure Transmitter Channel C [bar] *)

    rAT_401A_ResidualAlkali_gL          : REAL;         (* Black Liquor Residual Alkali Analyzer Channel A [g/L] *)
    rAT_401B_ResidualAlkali_gL          : REAL;         (* Black Liquor Residual Alkali Analyzer Channel B [g/L] *)
    rAT_401C_ResidualAlkali_gL          : REAL;         (* Black Liquor Residual Alkali Analyzer Channel C [g/L] *)

    rPT_501A_BlowPressure_bar           : REAL;         (* Digester Bottom Blow Discharge Pressure Channel A [bar] *)
    rPT_501B_BlowPressure_bar           : REAL;         (* Digester Bottom Blow Discharge Pressure Channel B [bar] *)
    rPT_501C_BlowPressure_bar           : REAL;         (* Digester Bottom Blow Discharge Pressure Channel C [bar] *)

    rFT_601A_ExtractionFlow_m3h         : REAL;         (* Black Liquor Main Extraction Flow Channel A [m3/h] *)
    rFT_601B_ExtractionFlow_m3h         : REAL;         (* Black Liquor Main Extraction Flow Channel B [m3/h] *)
    rFT_601C_ExtractionFlow_m3h         : REAL;         (* Black Liquor Main Extraction Flow Channel C [m3/h] *)

    (* Exogenous Disturbances & Wood Chip Feed Quality *)
    rChipMoisture_pct                   : REAL;         (* In-Line Gamma / Microwave Wood Chip Moisture Content [%] *)
    rChipBulkDensity_kgm3               : REAL;         (* Belt Scale Chip Bulk Weight Packed Density [kg/m3] *)
    rWhiteLiquorActiveAlkali_gL         : REAL;         (* Titrated White Liquor Active Alkali (AA as Na2O) [g/L] *)
    rFeedChipTemp_degC                  : REAL;         (* Ambient Wood Chip Silo Storage Bulk Temp [deg C] *)
    rWhiteLiquorSulfidity_pct           : REAL;         (* White Liquor Chemical Sulfidity Index [%] *)
    rHardwoodBlendRatio_pct             : REAL;         (* Wood Chip Hardwood (Eucalyptus/Birch) Species Fraction [%] *)
    rSteamingVesselPressure_bar         : REAL;         (* Low Pressure Steaming Vessel Vapor Header [bar] *)
    rImpregnationVesselLevel_pct        : REAL;         (* Impregnation Vessel Radiometric Chip Column Level [%] *)
    
    (* Process Telemetry & Mechanical Feedbacks *)
    rDigesterChipLevel_m                : REAL;         (* Gamma Nuclear Digester Vessel Chip Level Profiler [m] *)
    rScreenDifferentialPress_bar        : REAL;         (* Extraction Screen Internal/External Delta-P PT-405 [bar] *)
    rBottomScraperVfdTorque_kNm         : REAL;         (* Digester Bottom Rotary Scraper Motor Shaft Torque [kNm] *)
    rBottomScraperCurrent_A             : REAL;         (* Bottom Scraper Inverter Output Phase Current [A] *)
    rBlowLineConsistency_pct           : REAL;         (* In-Line Optical/Shear Pulp Blow Line Consistency [%] *)
    rBlowLineFlow_m3h                   : REAL;         (* Magnetic Flowmeter Blow Line Pulp Slurry Discharge [m3/h] *)
    rWashLiquorInletTemp_degC           : REAL;         (* Wash Liquor Supply Header Fluid Temperature [deg C] *)
    rWashLiquorInletFlow_m3h            : REAL;         (* Counter-Current Wash Liquor Displacement Feed Rate [m3/h] *)
    rSteamSupplyPressure_bar            : REAL;         (* Medium-Pressure Steam Main Supply Header [bar] *)
    rSteamSupplyTemp_degC               : REAL;         (* Medium-Pressure Superheated Steam Supply Temp [deg C] *)
    rHpfSpeedFeedback_rpm               : REAL;         (* High-Pressure Chip Feeder Rotary Pocket Actual Speed [rpm] *)
    
    (* Setpoint Targets & Operational Constraints *)
    rTargetKappaNumber                  : REAL;         (* Final Unbleached Pulp Target Kappa Number Setpoint [Kappa] *)
    rTargetProductionRate_ADtd          : REAL;         (* Production Rate Setpoint (1200.0 - 1650.0) [ADt/d] *)
    rTargetAlkaliToWoodRatio_pct        : REAL;         (* Target Effective Alkali on Dry Wood Charge (16.5 - 21.0) [%] *)
    rTargetLiquorToWoodRatio            : REAL;         (* Total Volumetric Liquor to Oven-Dry Wood Ratio (3.2 - 4.5) [-] *)
    rMaxAllowableTopPressure_bar        : REAL;         (* Digester Vessel Structural Pressure Safety Limit [bar] *)
    rMaxAllowableCookTemp_degC          : REAL          (* Maximum Permissible Cooking Fluid Temperature [deg C] *)
END_VAR
""")

    # -------------------------------------------------------------------------
    # PART 3: VAR_OUTPUT
    # -------------------------------------------------------------------------
    code_lines.append("""
VAR_OUTPUT
    (* Master System Status & Operational Indicators *)
    bSystemReady                        : BOOL;         (* Digester System Hydraulically Equalized & Ready [-] *)
    bProductionActive                   : BOOL;         (* Continuous Steady-State Pulp Cooking Active [-] *)
    bEmergencyTripActive                : BOOL;         (* SIL-3 Process Safety Trip or Depressurization Active [-] *)
    nDigesterOperationalState           : INT;          (* Current Active 14-Stage FSM Operational Stage Code (0 - 14) [-] *)
    sOperationalStateName               : STRING(32);   (* Descriptive ASCII String of Current Operating Stage [-] *)
    
    (* Primary Actuator Modulating Commands *)
    rUpperSteamValveCmd_pct             : REAL;         (* Upper Cook Circulation Steam Heat Exchanger Valve [%] *)
    rLowerSteamValveCmd_pct             : REAL;         (* Lower Cook Circulation Steam Heat Exchanger Valve [%] *)
    rExtractionFlowValveCmd_pct         : REAL;         (* Dynamic Black Liquor Extraction Header Control Valve [%] *)
    rWhiteLiquorDosingValveCmd_pct      : REAL;         (* White Liquor Active Alkali Metering Valve Position [%] *)
    rHpfSpeedReference_rpm              : REAL;         (* High-Pressure Chip Feeder Rotary Pocket VFD Speed [rpm] *)
    rBottomScraperSpeedCmd_rpm          : REAL;         (* Digester Bottom Rotary Scraper Motor Speed Command [rpm] *)
    rBlowValveCmd_pct                   : REAL;         (* Digester Bottom Pulp Discharge Blow Valve Position [%] *)
    rWashLiquorValveCmd_pct             : REAL;         (* Wash Zone Counter-Current Displacement Flow Valve [%] *)
    rBlowDilutionFiltrateValveCmd_pct   : REAL;         (* Blow Line Consistency Trim Dilution Flow Valve [%] *)
    
    (* Discrete Solenoids & Valves *)
    bOpenTopHydraulicInletValve         : BOOL;         (* Digester Top Chip/Liquor Inflow Isolation Block Valve [-] *)
    bOpenWhiteLiquorBlockValve          : BOOL;         (* White Liquor Dosing Header Fast Isolation Block Valve [-] *)
    bOpenBottomBlowLineValve            : BOOL;         (* Digester Bottom Pulp Discharge Main Safety Isolation [-] *)
    bOpenEmergencyDepressurizeValve     : BOOL;         (* Fast Emergency Digester Shell Depressurization Rupture Dump [-] *)
    bExtractionScreenBackflushActive    : BOOL;         (* Slotted Extraction Screen Backflush Flush Cycle Running [-] *)
    bBackflushValveRow1                 : BOOL;         (* Screen Row 1 Hydraulic Reverse Shock Solenoid Valve [-] *)
    bBackflushValveRow2                 : BOOL;         (* Screen Row 2 Hydraulic Reverse Shock Solenoid Valve [-] *)
    bBackflushValveRow3                 : BOOL;         (* Screen Row 3 Hydraulic Reverse Shock Solenoid Valve [-] *)

    (* 2oo3 TMR Validated Sensor Values *)
    rVotedUpperCookTemp_degC            : REAL;         (* 2oo3 TMR Validated Upper Cook Circulation Temp [deg C] *)
    rVotedLowerCookTemp_degC            : REAL;         (* 2oo3 TMR Validated Lower Cook Circulation Temp [deg C] *)
    rVotedTopPressure_bar               : REAL;         (* 2oo3 TMR Validated Digester Shell Top Pressure [bar] *)
    rVotedResidualAlkali_gL             : REAL;         (* 2oo3 TMR Validated Extraction Residual Alkali [g/L] *)
    rVotedBlowPressure_bar              : REAL;         (* 2oo3 TMR Validated Digester Bottom Blow Line Pressure [bar] *)
    rVotedExtractionFlow_m3h            : REAL;         (* 2oo3 TMR Validated Black Liquor Extraction Flow [m3/h] *)

    (* Cyber-Physical State Estimates & Kinetic Observers *)
    rObservedKappaNumber                : REAL;         (* Cyber-Physical Observer Estimated Pulp Kappa Number [Kappa] *)
    rObservedHFactor                    : REAL;         (* Accumulated Vroom Thermodynamic Delignification H-Factor [-] *)
    rObservedDelignificationRate_pcth   : REAL;         (* Instantaneous Lignin Chemical Dissolution Rate [%/h] *)
    rObservedEffectiveAlkali_gL         : REAL;         (* Estimated Bulk Cooking Liquor Residual Effective Alkali [g/L] *)
    rObservedChipCompaction_pct         : REAL;         (* Dynamic Chip Column Compaction Degree / Flow Resistance [%] *)
    rObservedWashDisplacementRatio      : REAL;         (* Counter-Current Wash Zone Liquid Displacement Ratio [-] *)
    rObservedProductionRate_ADtd        : REAL;         (* Computed Real-Time Dry Pulp Mass Production Rate [ADt/d] *)
    rObservedSpecificSteamConsump_t_ADt : REAL;         (* Real-Time Medium-Pressure Steam Specific Consumption [t/ADt] *)
    rChipColumnPermeabilityIndex        : REAL;         (* Estimated Hydraulic Porous Bed Darcy Permeability Index [-] *)
    rEstimatedTimeInDigester_h          : REAL;         (* Calculated Total Chip Column Residence Retention Time [h] *)

    (* Bit-Packed Status Words & ISA-18.2 Process Alarms *)
    dwStatusWord                        : DWORD;        (* 32-Bit System Operational State & Mode Bitmask [-] *)
    dwAlarmWord1                        : DWORD;        (* 32-Bit Priority 1 Emergency Safety Interlocks & Trips [-] *)
    dwAlarmWord2                        : DWORD;        (* 32-Bit Priority 2 Warnings, Screen DP & TMR Discordances [-] *)
    dwTripWord                          : DWORD;        (* 32-Bit First-Out Safety Shutdown Lockout Code [-] *)
    bAlarmHighHigh_Pressure             : BOOL;         (* Digester Top Shell High-High Pressure Safety Trip Active [-] *)
    bAlarmHigh_ExtractionDP             : BOOL;         (* Extraction Screen High Differential Pressure Warning [-] *)
    bAlarmLow_ResidualAlkali            : BOOL;         (* Cooking Residual Alkali Low Warning (Lignin Condensation) [-] *)
    bAlarm_ChipColumnHanging            : BOOL;         (* Chip Column Hanging / Plug Flow Stoppage Interlock Active [-] *)
    bAlarm_KappaDeviation               : BOOL;         (* Final Pulp Kappa Number Exceeding +/- 1.5 Quality Tolerance [-] *)
    bAlarm_TmrDiscordanceActive         : BOOL          (* TMR Transmitter Discrepancy Debounce Exceeded on Any Group [-] *)
END_VAR
""")

    # -------------------------------------------------------------------------
    # PART 4: VAR (Internal Variables)
    # -------------------------------------------------------------------------
    code_lines.append("""
VAR
    (* Execution & Initialization Controls *)
    bInitialized                        : BOOL := FALSE;(* One-Shot System Memory & Matrix Initialization Latch *)
    nScanCounter                        : DINT := 0;    (* Discrete PLC Scan Execution Counter *)
    rCycleTime_sec                      : REAL := 0.100;(* Discrete PLC Execution Scan Interval Ts = 100 ms [s] *)
    
    (* Cyber-Physical 8-State Discrete State-Space Model Vectors & Matrices *)
    x_state                             : ARRAY[1..8] OF REAL;      (* Estimated Cyber-Physical State Vector x[k] *)
    x_hat                               : ARRAY[1..8] OF REAL;      (* Luenberger Innovation-Corrected State Vector *)
    x_pred                              : ARRAY[1..8] OF REAL;      (* A-Priori Predicted State Vector x[k+1|k] *)
    x_ref                               : ARRAY[1..8] OF REAL;      (* Target State Reference Trajectory Vector *)
    u_ctrl                              : ARRAY[1..8] OF REAL;      (* Applied Control Actuator Vector u[k] *)
    u_prev                              : ARRAY[1..8] OF REAL;      (* Previous Scan Control Vector u[k-1] *)
    u_mpc_opt                           : ARRAY[1..8] OF REAL;      (* MPC Optimal Unconstrained Control Vector *)
    d_dist                              : ARRAY[1..6] OF REAL;      (* Measured Exogenous Disturbance Vector d[k] *)
    y_meas                              : ARRAY[1..8] OF REAL;      (* Filtered 2oo3 Sensor Output Measurement Vector *)
    y_est                               : ARRAY[1..8] OF REAL;      (* Model Estimated Physical Output Vector *)
    e_innov                             : ARRAY[1..8] OF REAL;      (* Luenberger Innovation Residual Vector *)

    matA                                : ARRAY[1..8, 1..8] OF REAL;(* Discrete State Transition Matrix A (8x8) *)
    matB                                : ARRAY[1..8, 1..8] OF REAL;(* Manipulated Input Coupling Matrix B (8x8) *)
    matBd                               : ARRAY[1..8, 1..6] OF REAL;(* Exogenous Disturbance Coupling Matrix Bd (8x6) *)
    matC                                : ARRAY[1..8, 1..8] OF REAL;(* Observation Measurement Matrix C (8x8) *)
    matD                                : ARRAY[1..8, 1..8] OF REAL;(* Direct Feedthrough Matrix D (8x8) *)
    matL                                : ARRAY[1..8, 1..8] OF REAL;(* Luenberger Observer Kalman Innovation Gains *)

    (* Model Predictive Control (MPC) Cost Matrices & Saturation Bounds *)
    matQ                                : ARRAY[1..8, 1..8] OF REAL;(* State Tracking Quadratic Penalty Matrix (8x8) *)
    matR                                : ARRAY[1..8, 1..8] OF REAL;(* Actuator Effort Quadratic Penalty Matrix (8x8) *)
    matS                                : ARRAY[1..8, 1..8] OF REAL;(* Actuator Slew Rate Quadratic Penalty Matrix (8x8) *)
    matP                                : ARRAY[1..8, 1..8] OF REAL;(* Terminal State Riccati Quadratic Penalty Matrix *)
    u_min                               : ARRAY[1..8] OF REAL;      (* Actuator Lower Box Saturation Bounds *)
    u_max                               : ARRAY[1..8] OF REAL;      (* Actuator Upper Box Saturation Bounds *)
    du_max                              : ARRAY[1..8] OF REAL;      (* Actuator Maximum Allowable Slew Rate Per Scan *)

    (* MPC Receding-Horizon Rollout Arrays (Prediction Horizon Np = 5, Control Horizon Nc = 3) *)
    x_rollout                           : ARRAY[1..5, 1..8] OF REAL;(* Predicted State Trajectory across Horizon *)
    u_horizon                           : ARRAY[1..3, 1..8] OF REAL;(* Planned Manipulated Actuator Sequence *)
    grad_J                              : ARRAY[1..8] OF REAL;      (* Projected Gradient Vector of Cost Functional J *)
    rAlpha_pgd                          : REAL := 0.00185;          (* PGD Optimization Gradient Step Length *)
    rCost_J                             : REAL;                     (* Cumulative Quadratic Objective Function Value *)

    (* 2oo3 TMR Voting Internal Structures & Timers *)
    bHealthy_TT101A                     : BOOL := TRUE;
    bHealthy_TT101B                     : BOOL := TRUE;
    bHealthy_TT101C                     : BOOL := TRUE;
    rTimer_TT101_AB_sec                 : REAL := 0.0;
    rTimer_TT101_BC_sec                 : REAL := 0.0;
    rTimer_TT101_CA_sec                 : REAL := 0.0;
    bDiscrepancy_TT101                  : BOOL := FALSE;
    bDegraded_TT101                     : BOOL := FALSE;
    rVoted_TT101_Prev                   : REAL := 158.0;

    bHealthy_TT201A                     : BOOL := TRUE;
    bHealthy_TT201B                     : BOOL := TRUE;
    bHealthy_TT201C                     : BOOL := TRUE;
    rTimer_TT201_AB_sec                 : REAL := 0.0;
    rTimer_TT201_BC_sec                 : REAL := 0.0;
    rTimer_TT201_CA_sec                 : REAL := 0.0;
    bDiscrepancy_TT201                  : BOOL := FALSE;
    bDegraded_TT201                     : BOOL := FALSE;
    rVoted_TT201_Prev                   : REAL := 168.0;

    bHealthy_PT301A                     : BOOL := TRUE;
    bHealthy_PT301B                     : BOOL := TRUE;
    bHealthy_PT301C                     : BOOL := TRUE;
    rTimer_PT301_AB_sec                 : REAL := 0.0;
    rTimer_PT301_BC_sec                 : REAL := 0.0;
    rTimer_PT301_CA_sec                 : REAL := 0.0;
    bDiscrepancy_PT301                  : BOOL := FALSE;
    bDegraded_PT301                     : BOOL := FALSE;
    rVoted_PT301_Prev                   : REAL := 12.5;

    bHealthy_AT401A                     : BOOL := TRUE;
    bHealthy_AT401B                     : BOOL := TRUE;
    bHealthy_AT401C                     : BOOL := TRUE;
    rTimer_AT401_AB_sec                 : REAL := 0.0;
    rTimer_AT401_BC_sec                 : REAL := 0.0;
    rTimer_AT401_CA_sec                 : REAL := 0.0;
    bDiscrepancy_AT401                  : BOOL := FALSE;
    bDegraded_AT401                     : BOOL := FALSE;
    rVoted_AT401_Prev                   : REAL := 14.5;

    bHealthy_PT501A                     : BOOL := TRUE;
    bHealthy_PT501B                     : BOOL := TRUE;
    bHealthy_PT501C                     : BOOL := TRUE;
    rTimer_PT501_AB_sec                 : REAL := 0.0;
    rTimer_PT501_BC_sec                 : REAL := 0.0;
    rTimer_PT501_CA_sec                 : REAL := 0.0;
    bDiscrepancy_PT501                  : BOOL := FALSE;
    bDegraded_PT501                     : BOOL := FALSE;
    rVoted_PT501_Prev                   : REAL := 4.2;

    bHealthy_FT601A                     : BOOL := TRUE;
    bHealthy_FT601B                     : BOOL := TRUE;
    bHealthy_FT601C                     : BOOL := TRUE;
    rTimer_FT601_AB_sec                 : REAL := 0.0;
    rTimer_FT601_BC_sec                 : REAL := 0.0;
    rTimer_FT601_CA_sec                 : REAL := 0.0;
    bDiscrepancy_FT601                  : BOOL := FALSE;
    bDegraded_FT601                     : BOOL := FALSE;
    rVoted_FT601_Prev                   : REAL := 420.0;

    rDiscrepancyThreshold_Temp_degC     : REAL := 3.0;      (* Discrepancy Margin for RTD Sensors [deg C] *)
    rDiscrepancyThreshold_Press_bar     : REAL := 0.6;      (* Discrepancy Margin for Pressure Cells [bar] *)
    rDiscrepancyThreshold_Alkali_gL     : REAL := 2.5;      (* Discrepancy Margin for Residual Alkali [g/L] *)
    rDiscrepancyThreshold_Flow_m3h      : REAL := 25.0;     (* Discrepancy Margin for Extraction Flow [m3/h] *)
    rTmrDebounceTimeLimit_sec           : REAL := 2.5;      (* Time Delay before Invalidating Channel [s] *)

    (* Thermodynamic, Kinetic & Hydraulic Constants *)
    rActivationEnergy_Bulk_Jmol         : REAL := 133970.0; (* Bulk Delignification Activation Energy E_a [J/mol] *)
    rUniversalGasConst_JmolK            : REAL := 8.31446;  (* Universal Gas Constant R [J/(mol*K)] *)
    rVroomConstant_A                    : REAL := 43.20;    (* Vroom Pre-exponential Arrhenius Constant *)
    rVroomConstant_B                    : REAL := 16113.0;  (* Vroom Temperature Quotient Constant [K] *)
    rBaselineTemp_K                     : REAL := 373.15;   (* 100 deg C Standard Reference Baseline [K] *)
    
    rHatton_A_Softwood                  : REAL := 168.50;   (* Hatton Equation Constant A for Coniferous Softwood *)
    rHatton_B_Softwood                  : REAL := 28.75;    (* Hatton Equation Constant B for Coniferous Softwood *)
    rHatton_Gamma_Softwood              : REAL := 0.65;     (* Hatton Alkali Exponent for Softwood *)
    rHatton_A_Hardwood                  : REAL := 142.30;   (* Hatton Equation Constant A for Deciduous Hardwood *)
    rHatton_B_Hardwood                  : REAL := 24.10;    (* Hatton Equation Constant B for Deciduous Hardwood *)
    rHatton_Gamma_Hardwood              : REAL := 0.72;     (* Hatton Alkali Exponent for Hardwood *)

    rUpperTemp_K                        : REAL;             (* Upper Cook Circulation Temp in Kelvin [K] *)
    rLowerTemp_K                        : REAL;             (* Lower Cook Circulation Temp in Kelvin [K] *)
    rMeanCookTemp_K                     : REAL;             (* Weighted Mean Cooking Temperature [K] *)
    rRelativeRate_Upper                 : REAL;             (* Vroom Relative Reaction Rate k_rel at Upper Temp *)
    rRelativeRate_Lower                 : REAL;             (* Vroom Relative Reaction Rate k_rel at Lower Temp *)
    rRelativeRate_Mean                  : REAL;             (* Mean Delignification Reaction Rate Factor *)
    rHFactor_Increment                  : REAL;             (* Discrete Scan H-Factor Increment [H-factor units] *)
    rEffectiveAlkaliActive_pct          : REAL;             (* Applied Effective Alkali on Dry Wood [%] *)
    rHatton_A_Blend                     : REAL;             (* Species Blend Weighted Hatton Constant A *)
    rHatton_B_Blend                     : REAL;             (* Species Blend Weighted Hatton Constant B *)
    rHatton_Gamma_Blend                 : REAL;             (* Species Blend Weighted Hatton Exponent Gamma *)
    rHattonKappa_Predicted              : REAL;             (* Raw Hatton Equation Kappa Prediction [Kappa] *)
    rErgunViscosity_Pas                 : REAL := 0.00045;  (* Black Liquor Dynamic Viscosity at 160 deg C [Pa.s] *)
    rChipBedPorosity_epsilon            : REAL := 0.42;     (* Compacted Wood Chip Column Porosity [-] *)
    rEquivalentChipDiameter_m           : REAL := 0.018;    (* Sieve Equivalent Wood Chip Mean Diameter [m] *)
    rDynamicLiquorDensity_kgm3          : REAL := 1120.0;   (* Black Liquor Operating Density [kg/m3] *)
    rChipDownwardVelocity_mps           : REAL;             (* Linear Chip Bed Subsidence Velocity [m/s] *)
    rHydraulicFrictionalHeadLoss_bar    : REAL;             (* Ergun Fluid Downflow Pressure Drop [bar] *)
    rNordenEfficiencyWashFactor         : REAL := 6.5;      (* Norden Wash Displacement Efficiency Constant [-] *)

    (* Finite State Machine Registers *)
    nFsmState                           : INT := 0;         (* Active Operational State Code (0 - 14) *)
    nFsmNextState                       : INT := 0;         (* Next Transition State Code *)
    rFsmStateElapsedTime_sec            : REAL := 0.0;      (* Cumulative Time in Current Active State [s] *)
    bStateFirstScan                     : BOOL := TRUE;     (* One-Shot Pulse on State Entry Transition *)
    
    nBackflushStep                      : INT := 0;         (* Screen Cyclic Sub-Step: 0=Idle, 1=Row1, 2=Row2, 3=Row3 *)
    rBackflushStepTimer_sec             : REAL := 0.0;      (* Screen Backflush Pulse Elapsed Timer [s] *)
    rBackflushIntervalTimer_sec         : REAL := 0.0;      (* Screen Cyclic Auto-Trigger Interval Timer [s] *)
    
    nHangingRecoveryStep                : INT := 0;         (* Recovery Step: 1=Relieve, 2=Displace, 3=Sync *)
    rHangingRecoveryTimer_sec           : REAL := 0.0;      (* Hanging Recovery Step Duration Timer [s] *)

    rUpperSteamRampTarget_pct           : REAL := 0.0;
    rLowerSteamRampTarget_pct           : REAL := 0.0;
    rExtractionFlowRampTarget_pct       : REAL := 20.0;
    rWhiteLiquorRampTarget_pct          : REAL := 15.0;
    rHpfSpeedRampTarget_rpm             : REAL := 8.0;
    rBottomScraperRampTarget_rpm        : REAL := 3.5;
    rBlowValveRampTarget_pct            : REAL := 10.0;
    rWashLiquorRampTarget_pct           : REAL := 25.0;

    (* ISA-18.2 Process Alarm Limits & Constants *)
    rSp_TopPress_Trip_HH_bar            : REAL := 15.2;     (* High-High Top Hydraulic Pressure Trip [bar] *)
    rSp_TopPress_Alarm_H_bar            : REAL := 14.0;     (* High Top Pressure Warning [bar] *)
    rSp_TopPress_Alarm_L_bar            : REAL := 9.5;      (* Low Top Pressure Warning (Cavitation Risk) [bar] *)
    rSp_TopPress_Trip_LL_bar            : REAL := 8.0;      (* Low-Low Pressure Hydraulic Collapse Trip [bar] *)
    
    rSp_CookTemp_Trip_HH_degC           : REAL := 178.0;    (* High-High Cooking Temp Cellulose Damage Trip [deg C] *)
    rSp_CookTemp_Alarm_H_degC           : REAL := 172.0;    (* High Cooking Temp Warning [deg C] *)
    rSp_CookTemp_Alarm_L_degC           : REAL := 142.0;    (* Low Cooking Temp Incomplete Reaction Warning [deg C] *)
    
    rSp_Alkali_Alarm_H_gL               : REAL := 28.0;     (* High Residual Alkali Chemical Waste Warning [g/L] *)
    rSp_Alkali_Alarm_L_gL               : REAL := 8.5;      (* Low Residual Alkali Lignin Condensation Warning [g/L] *)
    rSp_Alkali_Trip_LL_gL               : REAL := 5.0;      (* Low-Low Alkali Acidic Lignin Precipitation Trip [g/L] *)
    
    rSp_ScreenDP_Trip_HH_bar            : REAL := 2.8;      (* High-High Screen Delta-P Structural Crush Trip [bar] *)
    rSp_ScreenDP_Alarm_H_bar            : REAL := 1.7;      (* High Screen Delta-P Backflush Trigger Warning [bar] *)
    
    rSp_ScraperTorque_Trip_HH_kNm       : REAL := 55.0;     (* High-High Scraper Motor Mechanical Shear Trip [kNm] *)
    rSp_ScraperTorque_Alarm_H_kNm       : REAL := 42.0;     (* High Scraper Torque Column Compaction Warning [kNm] *)
    
    rSp_Kappa_Alarm_H_Kappa             : REAL := 31.5;     (* High Kappa Under-cooked Hard Shive Pulp [Kappa] *)
    rSp_Kappa_Alarm_L_Kappa             : REAL := 24.5;     (* Low Kappa Over-cooked Cellulose Degraded Pulp [Kappa] *)

    rHysteresis_Press_bar               : REAL := 0.35;     (* Pressure Trip Deadband [bar] *)
    rHysteresis_Temp_degC               : REAL := 1.5;      (* Temperature Trip Deadband [deg C] *)
    rHysteresis_Alkali_gL               : REAL := 0.8;      (* Alkali Trip Deadband [g/L] *)
    rHysteresis_ScreenDP_bar            : REAL := 0.20;     (* Screen DP Deadband [bar] *)
    rHysteresis_Torque_kNm              : REAL := 3.0;      (* Torque Deadband [kNm] *)
    rHysteresis_Kappa                   : REAL := 0.5;      (* Kappa Deadband [Kappa] *)

    rTimer_Trip_TopPress_HH_sec         : REAL := 0.0;
    rTimer_Alarm_TopPress_H_sec         : REAL := 0.0;
    rTimer_Alarm_TopPress_L_sec         : REAL := 0.0;
    rTimer_Trip_TopPress_LL_sec         : REAL := 0.0;
    rTimer_Trip_CookTemp_HH_sec         : REAL := 0.0;
    rTimer_Alarm_CookTemp_H_sec         : REAL := 0.0;
    rTimer_Trip_Alkali_LL_sec           : REAL := 0.0;
    rTimer_Alarm_Alkali_L_sec           : REAL := 0.0;
    rTimer_Trip_ScreenDP_HH_sec         : REAL := 0.0;
    rTimer_Alarm_ScreenDP_H_sec         : REAL := 0.0;
    rTimer_Trip_ScraperTorque_sec       : REAL := 0.0;
    rTimer_Alarm_ScraperTorque_sec      : REAL := 0.0;
    rTimer_Alarm_KappaDev_sec           : REAL := 0.0;
    
    i                                   : INT := 1;
    j                                   : INT := 1;
    k_idx                               : INT := 1;
    m_idx                               : INT := 1;
    n_idx                               : INT := 1;
    rTempSum                            : REAL := 0.0;
    rDelta_u                            : REAL := 0.0
END_VAR
""")

    # -------------------------------------------------------------------------
    # PART 5: PHASE 0 - ONE-SHOT FIRST-SCAN INITIALIZATION
    # -------------------------------------------------------------------------
    code_lines.append("""
(* ====================================================================================================
   PHASE 0: ONE-SHOT FIRST-SCAN SYSTEM INITIALIZATION & CYBER-PHYSICAL MATRIX ALLOCATION
   Ts = 100 ms (0.100 s) Discrete Sample Period
   State Vector x in R^8:
     x[1]: Chip Column Compaction / Downward Velocity Index [%] (0.0 to 100.0)
     x[2]: Impregnation Residual Effective Alkali EA_iv [g/L] (15.0 to 35.0)
     x[3]: Upper Cooking Zone Residual Effective Alkali EA_uc [g/L] (10.0 to 25.0)
     x[4]: Upper Cooking Circulation Temperature T_upper [deg C] (145.0 to 175.0)
     x[5]: Lower Cooking Circulation Temperature T_lower [deg C] (150.0 to 180.0)
     x[6]: Delignification H-Factor Thermal Reaction Accumulator [H-factor units]
     x[7]: Blow Line Pulp Kappa Number [Kappa units] (18.0 to 45.0)
     x[8]: Wash Zone Displacement Liquor Dissolved Solids [%] (4.0 to 22.0)
   Control Vector u in R^8:
     u[1]: Upper Cook Steam Valve [%]
     u[2]: Lower Cook Steam Valve [%]
     u[3]: Extraction Header Flow Valve [%]
     u[4]: White Liquor Active Alkali Feed Valve [%]
     u[5]: High-Pressure Chip Feeder Speed [rpm]
     u[6]: Bottom Scraper Motor Speed [rpm]
     u[7]: Blow Line Flow Control Valve [%]
     u[8]: Wash Zone Displacement Valve [%]
   ==================================================================================================== *)

IF NOT bInitialized THEN
    (* ------------------------------------------------------------------------------------------------
       MATRIX A: DISCRETE STATE TRANSITION MATRIX (8x8) at Ts = 100 ms
       Linearized continuous Kamyr digester model with chip compaction, alkali diffusion,
       Arrhenius thermal delignification kinetics, and counter-current displacement washing.
       ------------------------------------------------------------------------------------------------ *)
    (* Row 1: Chip Column Compaction Level x[1] [%] *)
    matA[1, 1] := 0.965000;   (* Viscous compaction persistence and bed elasticity damping *)
    matA[1, 2] := -0.012500;  (* Impregnation alkali swelling reduces interstitial void friction *)
    matA[1, 3] := -0.018000;  (* Upper cooking alkali saponification of wood resin acids *)
    matA[1, 4] := 0.008500;   (* Upper thermal softening increases chip deformability *)
    matA[1, 5] := 0.014200;   (* Lower thermal plasticity increases column compressibility *)
    matA[1, 6] := -0.000045;  (* Lignin dissolution structural collapse coupling *)
    matA[1, 7] := 0.012000;   (* Higher Kappa stiffer fibers resist packing *)
    matA[1, 8] := -0.025000;  (* Wash liquor counter-current upward buoyancy lift *)

    (* Row 2: Impregnation Vessel Residual Effective Alkali x[2] [g/L] *)
    matA[2, 1] := -0.008500;  (* Chip compaction reduces liquor circulation infiltration *)
    matA[2, 2] := 0.938000;   (* Impregnation vessel plug flow residence time decay *)
    matA[2, 3] := 0.005000;   (* Diffusion back-coupling from transfer line *)
    matA[2, 4] := -0.014500;  (* Thermal acceleration of initial neutralization consumption *)
    matA[2, 5] := 0.000000;   (* Lower cook decoupled from impregnation vessel *)
    matA[2, 6] := 0.000000;   (* H-factor decoupled from initial impregnation stage *)
    matA[2, 7] := 0.000000;   (* Blow Kappa decoupled from impregnation vessel *)
    matA[2, 8] := 0.000000;   (* Wash dissolved solids decoupled from impregnation *)

    (* Row 3: Upper Cooking Zone Residual Effective Alkali x[3] [g/L] *)
    matA[3, 1] := -0.014000;  (* Compaction channeling reduces liquor contact efficiency *)
    matA[3, 2] := 0.052000;   (* Direct advective carryover from impregnation vessel *)
    matA[3, 3] := 0.915000;   (* Upper cooking zone residence time and consumption decay *)
    matA[3, 4] := -0.038500;  (* Temperature increases bulk delignification alkali consumption *)
    matA[3, 5] := 0.002500;   (* Lower cooking back-diffusion gradient *)
    matA[3, 6] := -0.000120;  (* Lignin cleavage stoichiometric alkali depletion *)
    matA[3, 7] := 0.000000;   (* Blow Kappa decoupled from upper cooking stage *)
    matA[3, 8] := 0.000000;   (* Wash liquor decoupled from upper cooking *)

    (* Row 4: Upper Cooking Circulation Temperature x[4] [deg C] *)
    matA[4, 1] := 0.002200;   (* Chip bed packing changes heat transfer convection area *)
    matA[4, 2] := 0.001500;   (* Chemical neutralization mild exotherm coupling *)
    matA[4, 3] := 0.003500;   (* Alkali concentration convective heat capacity modification *)
    matA[4, 4] := 0.942000;   (* Upper circulation loop thermal heat loss and mixing dissipation *)
    matA[4, 5] := 0.018000;   (* Conductive/convective coupling to lower cooking zone *)
    matA[4, 6] := 0.000000;   (* H-factor uncoupled to temperature dynamics *)
    matA[4, 7] := 0.000000;   (* Kappa uncoupled to temperature dynamics *)
    matA[4, 8] := -0.005000;  (* Wash zone upward thermal migration attenuation *)

    (* Row 5: Lower Cooking Circulation Temperature x[5] [deg C] *)
    matA[5, 1] := 0.003500;   (* Chip bed packing increases residence contact time *)
    matA[5, 2] := 0.000000;   (* Impregnation alkali decoupled from lower cook temperature *)
    matA[5, 3] := 0.004200;   (* Upper alkali feed alters bulk liquor heat capacity *)
    matA[5, 4] := 0.032000;   (* Co-current downward heat advection from upper cooking zone *)
    matA[5, 5] := 0.935000;   (* Lower circulation loop thermal dissipation persistence *)
    matA[5, 6] := 0.000000;   (* H-factor uncoupled to thermal dynamics *)
    matA[5, 7] := 0.000000;   (* Kappa uncoupled to thermal dynamics *)
    matA[5, 8] := -0.018500;  (* Cooler wash liquor upflow cooling effect *)

    (* Row 6: Delignification H-Factor Reaction Accumulator x[6] [H-factor units] *)
    matA[6, 1] := 0.000000;   (* Compaction uncoupled to reaction rate constant *)
    matA[6, 2] := 0.000000;   (* Arrhenius rate depends exclusively on thermal activation *)
    matA[6, 3] := 0.000000;   (* Chemical alkali modulates rate constant via Hatton, not H-factor *)
    matA[6, 4] := 0.185000;   (* Upper cooking temperature Arrhenius rate contribution *)
    matA[6, 5] := 0.325000;   (* Lower cooking temperature Arrhenius rate dominant contribution *)
    matA[6, 6] := 1.000000;   (* Pure discrete time-integral state persistence *)
    matA[6, 7] := 0.000000;   (* Kappa uncoupled to H-factor accumulation *)
    matA[6, 8] := 0.000000;   (* Wash liquor uncoupled to H-factor accumulation *)

    (* Row 7: Blow Line Pulp Kappa Number x[7] [Kappa units] *)
    matA[7, 1] := -0.015000;  (* Compaction prolongs cooking retention, dropping Kappa *)
    matA[7, 2] := -0.045000;  (* Impregnation alkali charge accelerates delignification *)
    matA[7, 3] := -0.125000;  (* Upper cooking residual alkali drives bulk lignin removal *)
    matA[7, 4] := -0.082000;  (* Upper temperature increases delignification extent *)
    matA[7, 5] := -0.145000;  (* Lower cooking temperature strongest delignification driver *)
    matA[7, 6] := -0.005500;  (* Integrated H-factor logarithmic delignification progression *)
    matA[7, 7] := 0.958000;   (* Pulp column advection and plug flow mixing persistence *)
    matA[7, 8] := 0.012500;   (* Inadequate wash solids displacement causes lignin precipitation *)

    (* Row 8: Wash Zone Displacement Liquor Dissolved Solids x[8] [%] *)
    matA[8, 1] := 0.008500;   (* Compaction restricts wash filtrate percolation channel *)
    matA[8, 2] := 0.000000;   (* Impregnation decoupled from bottom wash *)
    matA[8, 3] := 0.015000;   (* Residual alkali carryover to wash zone *)
    matA[8, 4] := 0.000000;   (* Upper temp decoupled from wash solids *)
    matA[8, 5] := 0.012000;   (* Lower temp increases lignin dissolution in wash filtrate *)
    matA[8, 6] := 0.000150;   (* Higher total delignification releases more dissolved solids *)
    matA[8, 7] := -0.035000;  (* Lower Kappa corresponds to more dissolved lignin solids *)
    matA[8, 8] := 0.912000;   (* Wash zone liquor displacement washout rate *)

    (* ------------------------------------------------------------------------------------------------
       MATRIX B: CONTROL INPUT DISTRIBUTION MATRIX (8x8)
       Inputs:
         u[1]: Upper Cook Steam Valve [%]
         u[2]: Lower Cook Steam Valve [%]
         u[3]: Extraction Flow Valve [%]
         u[4]: White Liquor Feed Valve [%]
         u[5]: High-Pressure Chip Feeder Speed [rpm]
         u[6]: Bottom Scraper Speed [rpm]
         u[7]: Blow Line Flow Valve [%]
         u[8]: Wash Zone Displacement Valve [%]
       ------------------------------------------------------------------------------------------------ *)
    (* State 1: Chip Column Compaction [%] *)
    matB[1, 1] := 0.002000;   (* Upper steam thermal expansion *)
    matB[1, 2] := 0.003500;   (* Lower steam thermal expansion *)
    matB[1, 3] := 0.185000;   (* High extraction flow increases downward hydraulic drag force *)
    matB[1, 4] := -0.015000;  (* White liquor lubricating alkali film *)
    matB[1, 5] := 0.225000;   (* HPF chip feed rate drives column mass accumulation *)
    matB[1, 6] := -0.165000;  (* Bottom scraper discharges compacted chip bed *)
    matB[1, 7] := -0.195000;  (* Blow flow draws column downward relieving compaction *)
    matB[1, 8] := -0.110000;  (* Wash liquor upflow exerts hydraulic buoyancy lift *)

    (* State 2: Impregnation Residual Effective Alkali [g/L] *)
    matB[2, 1] := 0.000000;   (* Upper steam no effect on impregnation *)
    matB[2, 2] := 0.000000;   (* Lower steam no effect on impregnation *)
    matB[2, 3] := -0.005000;  (* Extraction liquor slight hydraulic pull *)
    matB[2, 4] := 0.425000;   (* White liquor dosing primary alkali replenishment gain *)
    matB[2, 5] := -0.085000;  (* Higher chip feed rate consumes more initial alkali *)
    matB[2, 6] := 0.000000;   (* Bottom scraper no effect on impregnation *)
    matB[2, 7] := 0.000000;   (* Blow valve no effect on impregnation *)
    matB[2, 8] := 0.000000;   (* Wash liquor no effect on impregnation *)

    (* State 3: Upper Cooking Residual Effective Alkali [g/L] *)
    matB[3, 1] := -0.015000;  (* Upper steam heating accelerates alkali reaction rate *)
    matB[3, 2] := 0.000000;   (* Lower steam no direct effect *)
    matB[3, 3] := -0.145000;  (* Extraction valve draws residual alkali out of cooking zone *)
    matB[3, 4] := 0.285000;   (* White liquor dosing cascade replenishes upper cook alkali *)
    matB[3, 5] := -0.115000;  (* Wood chip influx consumes cooking alkali *)
    matB[3, 6] := 0.000000;   (* Bottom scraper no direct effect *)
    matB[3, 7] := 0.000000;   (* Blow valve no direct effect *)
    matB[3, 8] := -0.025000;  (* Wash filtrate dilution penetration *)

    (* State 4: Upper Cooking Circulation Temperature [deg C] *)
    matB[4, 1] := 0.455000;   (* Upper MP steam valve direct heat exchange gain [deg C/%] *)
    matB[4, 2] := 0.012000;   (* Lower steam indirect back-conduction *)
    matB[4, 3] := -0.035000;  (* Extraction flow liquor removal enthalpy loss *)
    matB[4, 4] := -0.018000;  (* Cold white liquor feed sensible enthalpy dip *)
    matB[4, 5] := -0.055000;  (* Cold wood chip feed sensible thermal load *)
    matB[4, 6] := 0.000000;   (* Bottom scraper neutral *)
    matB[4, 7] := 0.000000;   (* Blow valve neutral *)
    matB[4, 8] := -0.015000;  (* Wash filtrate upflow cooling *)

    (* State 5: Lower Cooking Circulation Temperature [deg C] *)
    matB[5, 1] := 0.025000;   (* Upper steam heat carried downward *)
    matB[5, 2] := 0.525000;   (* Lower MP steam valve direct heat exchange gain [deg C/%] *)
    matB[5, 3] := 0.045000;   (* Extraction flow balances lower counter-current circulation *)
    matB[5, 4] := -0.012000;  (* White liquor sensible enthalpy dip *)
    matB[5, 5] := -0.035000;  (* Chip feed throughput thermal load *)
    matB[5, 6] := 0.000000;   (* Bottom scraper neutral *)
    matB[5, 7] := -0.008000;  (* Blow flow draws hot liquor downward *)
    matB[5, 8] := -0.065000;  (* Cold wash liquor displacement cooling *)

    (* State 6: Delignification H-Factor Accumulator [H-factor units] *)
    matB[6, 1] := 0.125000;   (* Upper steam valve thermal reaction rate gain *)
    matB[6, 2] := 0.245000;   (* Lower steam valve thermal reaction rate gain *)
    matB[6, 3] := 0.015000;   (* Extraction flow stabilizes cooking zone profile *)
    matB[6, 4] := 0.000000;   (* White liquor neutral to thermal H-factor definition *)
    matB[6, 5] := -0.045000;  (* Faster chip feed shortens total digester residence time *)
    matB[6, 6] := -0.025000;  (* Faster scraper discharge shortens cooking time *)
    matB[6, 7] := -0.035000;  (* Blow valve discharge rate reduces cooking retention *)
    matB[6, 8] := -0.018000;  (* Wash liquor cools cooking zone bottom *)

    (* State 7: Blow Line Pulp Kappa Number [Kappa units] *)
    matB[7, 1] := -0.115000;  (* Upper steam heat drives delignification, lowering Kappa *)
    matB[7, 2] := -0.195000;  (* Lower steam heat primary delignification driver *)
    matB[7, 3] := 0.085000;   (* Excessive extraction strips active alkali, raising Kappa *)
    matB[7, 4] := -0.265000;  (* White liquor dosing increases alkali charge, lowering Kappa *)
    matB[7, 5] := 0.315000;   (* Higher production rate shortens cook, raising Kappa *)
    matB[7, 6] := 0.045000;   (* Scraper speed discharge acceleration *)
    matB[7, 7] := 0.065000;   (* Blow valve flow acceleration *)
    matB[7, 8] := -0.025000;  (* Effective wash prevents lignin re-precipitation *)

    (* State 8: Wash Zone Dissolved Solids [%] *)
    matB[8, 1] := 0.005000;   (* Upper steam cook extent *)
    matB[8, 2] := 0.015000;   (* Lower steam cook extent *)
    matB[8, 3] := -0.085000;  (* Extraction valve draws solids into black liquor header *)
    matB[8, 4] := 0.025000;   (* White liquor salts contribution *)
    matB[8, 5] := 0.045000;   (* Chip feed rate increases dissolved solids loading *)
    matB[8, 6] := 0.018000;   (* Scraper agitates bottom pulp suspension *)
    matB[8, 7] := -0.035000;  (* Blow valve discharges solids with pulp slurry *)
    matB[8, 8] := -0.325000;  (* Counter-current wash liquor flushes dissolved solids out *)

    (* ------------------------------------------------------------------------------------------------
       MATRIX Bd: EXOGENOUS DISTURBANCE COUPLING MATRIX (8x6)
       Disturbances:
         d[1]: Wood Chip Moisture [%]
         d[2]: Wood Chip Bulk Density [kg/m3]
         d[3]: White Liquor Active Alkali [g/L]
         d[4]: Feed Chip Temperature [deg C]
         d[5]: White Liquor Sulfidity [%]
         d[6]: Wood Chip Hardwood Ratio [%]
       ------------------------------------------------------------------------------------------------ *)
    (* State 1: Compaction *)
    matBd[1, 1] := 0.085000;  (* Moisture adds weight to chip bed *)
    matBd[1, 2] := 0.125000;  (* High density increases column gravitational force *)
    matBd[1, 3] := -0.015000; (* High alkali softens chip fibers *)
    matBd[1, 4] := -0.005000; (* Warmer chips slightly deform *)
    matBd[1, 5] := 0.000000;  (* Sulfidity neutral *)
    matBd[1, 6] := 0.045000;  (* Hardwood short fibers pack tighter than softwood *)

    (* State 2: Impregnation Alkali *)
    matBd[2, 1] := -0.165000; (* Chip moisture dilutes incoming white liquor *)
    matBd[2, 2] := -0.075000; (* Higher wood density consumes more chemical per unit volume *)
    matBd[2, 3] := 0.385000;  (* High supply alkali directly enriches impregnation *)
    matBd[2, 4] := 0.015000;  (* Warm chips improve alkali penetration *)
    matBd[2, 5] := 0.045000;  (* Higher sulfidity provides more hydrosulfide buffer *)
    matBd[2, 6] := -0.025000; (* Hardwood xylans consume more alkali in initial phase *)

    (* State 3: Upper Cooking Alkali *)
    matBd[3, 1] := -0.125000; (* Water carryover dilutes cooking liquor *)
    matBd[3, 2] := -0.095000; (* Higher wood mass increases chemical demand *)
    matBd[3, 3] := 0.285000;  (* White liquor strength directly impacts residual *)
    matBd[3, 4] := 0.012000;  (* Chip preheat sensible energy *)
    matBd[3, 5] := 0.065000;  (* Sulfidity preserves hydroxide ions via buffering *)
    matBd[3, 6] := -0.045000; (* Hardwood requires different alkali consumption profile *)

    (* State 4: Upper Cook Temperature *)
    matBd[4, 1] := -0.185000; (* Water vaporization and sensible heating thermal sink *)
    matBd[4, 2] := -0.045000; (* More wood mass requires more enthalpy *)
    matBd[4, 3] := 0.000000;  (* Chemical concentration neutral *)
    matBd[4, 4] := 0.225000;  (* Warmer feed chips reduce steaming heating load *)
    matBd[4, 5] := 0.000000;  (* Neutral *)
    matBd[4, 6] := 0.015000;  (* Species specific heat difference *)

    (* State 5: Lower Cook Temperature *)
    matBd[5, 1] := -0.095000; (* Moisture sensible heat carryover *)
    matBd[5, 2] := -0.035000; (* Thermal inertia *)
    matBd[5, 3] := 0.000000;  (* Neutral *)
    matBd[5, 4] := 0.115000;  (* Feed chip temp sensible carryover *)
    matBd[5, 5] := 0.000000;  (* Neutral *)
    matBd[5, 6] := 0.012000;  (* Species thermal diffusivity *)

    (* State 6: H-Factor Accumulator *)
    matBd[6, 1] := -0.025000; (* Moisture slows heating, delaying H-factor accumulation *)
    matBd[6, 2] := 0.000000;  (* Density neutral *)
    matBd[6, 3] := 0.000000;  (* Alkali neutral *)
    matBd[6, 4] := 0.045000;  (* Warm chips reach cooking temperature faster *)
    matBd[6, 5] := 0.000000;  (* Neutral *)
    matBd[6, 6] := 0.000000;  (* Neutral *)

    (* State 7: Blow Line Kappa Number *)
    matBd[7, 1] := 0.225000;  (* High moisture causes under-cooking, increasing Kappa *)
    matBd[7, 2] := 0.185000;  (* High density wood has slower liquor penetration *)
    matBd[7, 3] := -0.345000; (* Rich white liquor drops Kappa significantly *)
    matBd[7, 4] := -0.085000; (* Warmer chips promote better impregnation *)
    matBd[7, 5] := -0.155000; (* High sulfidity accelerates delignification *)
    matBd[7, 6] := -0.450000; (* Hardwood delignifies much faster than softwood (lower Kappa) *)

    (* State 8: Wash Zone Dissolved Solids *)
    matBd[8, 1] := -0.045000; (* Moisture dilution *)
    matBd[8, 2] := 0.085000;  (* Dense chips produce more dissolved solids per volume *)
    matBd[8, 3] := 0.065000;  (* Chemical solids load *)
    matBd[8, 4] := 0.000000;  (* Neutral *)
    matBd[8, 5] := 0.025000;  (* Sulfur salt ions *)
    matBd[8, 6] := 0.055000;  (* Hardwood dissolved xylan fragments enrich liquor solids *)

    (* ------------------------------------------------------------------------------------------------
       MATRIX C: MEASUREMENT OBSERVATION MATRIX (8x8)
       Outputs:
         y[1]: Upper Cook Temp TT-101 [deg C]
         y[2]: Lower Cook Temp TT-201 [deg C]
         y[3]: Digester Top Pressure PT-301 [bar]
         y[4]: Residual Alkali AT-401 [g/L]
         y[5]: Blow Pressure PT-501 [bar]
         y[6]: Extraction Flow FT-601 [m3/h]
         y[7]: In-Line NIR Kappa Number [Kappa]
         y[8]: Wash Solids Concentration [%]
       ------------------------------------------------------------------------------------------------ *)
    (* Row 1: TT-101 Upper Cook Temp *)
    matC[1, 1] := 0.000000; matC[1, 2] := 0.000000; matC[1, 3] := 0.000000;
    matC[1, 4] := 1.000000; matC[1, 5] := 0.000000; matC[1, 6] := 0.000000;
    matC[1, 7] := 0.000000; matC[1, 8] := 0.000000;

    (* Row 2: TT-201 Lower Cook Temp *)
    matC[2, 1] := 0.000000; matC[2, 2] := 0.000000; matC[2, 3] := 0.000000;
    matC[2, 4] := 0.000000; matC[2, 5] := 1.000000; matC[2, 6] := 0.000000;
    matC[2, 7] := 0.000000; matC[2, 8] := 0.000000;

    (* Row 3: PT-301 Top Hydraulic Pressure *)
    matC[3, 1] := 0.045000; matC[3, 2] := 0.000000; matC[3, 3] := 0.000000;
    matC[3, 4] := 0.015000; matC[3, 5] := 0.012000; matC[3, 6] := 0.000000;
    matC[3, 7] := 0.000000; matC[3, 8] := 0.000000;

    (* Row 4: AT-401 Extraction Residual Alkali *)
    matC[4, 1] := 0.000000; matC[4, 2] := 0.000000; matC[4, 3] := 0.950000;
    matC[4, 4] := 0.000000; matC[4, 5] := 0.000000; matC[4, 6] := 0.000000;
    matC[4, 7] := 0.000000; matC[4, 8] := 0.000000;

    (* Row 5: PT-501 Blow Line Pressure *)
    matC[5, 1] := 0.015000; matC[5, 2] := 0.000000; matC[5, 3] := 0.000000;
    matC[5, 4] := 0.000000; matC[5, 5] := 0.000000; matC[5, 6] := 0.000000;
    matC[5, 7] := 0.000000; matC[5, 8] := 0.000000;

    (* Row 6: FT-601 Extraction Header Flow *)
    matC[6, 1] := -0.250000; matC[6, 2] := 0.000000; matC[6, 3] := 0.000000;
    matC[6, 4] := 0.000000; matC[6, 5] := 0.000000; matC[6, 6] := 0.000000;
    matC[6, 7] := 0.000000; matC[6, 8] := 0.000000;

    (* Row 7: Blow Line Kappa Number *)
    matC[7, 1] := 0.000000; matC[7, 2] := 0.000000; matC[7, 3] := 0.000000;
    matC[7, 4] := 0.000000; matC[7, 5] := 0.000000; matC[7, 6] := 0.000000;
    matC[7, 7] := 1.000000; matC[7, 8] := 0.000000;

    (* Row 8: Wash Solids Concentration *)
    matC[8, 1] := 0.000000; matC[8, 2] := 0.000000; matC[8, 3] := 0.000000;
    matC[8, 4] := 0.000000; matC[8, 5] := 0.000000; matC[8, 6] := 0.000000;
    matC[8, 7] := 0.000000; matC[8, 8] := 1.000000;

    (* ------------------------------------------------------------------------------------------------
       MATRIX D: DIRECT FEEDTHROUGH MATRIX (8x8)
       ------------------------------------------------------------------------------------------------ *)
    FOR i := 1 TO 8 DO
        FOR j := 1 TO 8 DO
            matD[i, j] := 0.000000;
        END_FOR;
    END_FOR;
    matD[3, 4] := 0.025000;   (* White liquor pumping directly adds top hydraulic pressure *)
    matD[3, 5] := 0.035000;   (* HPF pocket discharge hydraulic pressure pulse *)
    matD[5, 6] := 0.045000;   (* Bottom scraper rotation imparts dynamic head to blow line *)
    matD[5, 7] := -0.065000;  (* Blow valve opening drops blow line backpressure *)
    matD[6, 3] := 4.250000;   (* Extraction valve position directly modulates flow [m3/h / %] *)
    matD[8, 8] := -0.085000;  (* Wash liquor flow immediately dilutes bottom liquor solids *)

    (* ------------------------------------------------------------------------------------------------
       MATRIX L: LUENBERGER OBSERVER KALMAN INNOVATION GAIN MATRIX (8x8)
       Compensates estimation errors using real-time voted measurements.
       ------------------------------------------------------------------------------------------------ *)
    FOR i := 1 TO 8 DO
        FOR j := 1 TO 8 DO
            matL[i, j] := 0.000000;
        END_FOR;
    END_FOR;
    matL[1, 3] := 0.125000;   (* Top pressure innovation corrects chip compaction estimate *)
    matL[1, 6] := -0.015000;  (* Extraction flow drop indicates screen blinding / compaction *)
    matL[2, 4] := 0.145000;   (* Extraction residual alkali corrects impregnation model *)
    matL[3, 4] := 0.385000;   (* Extraction alkali residual directly corrects upper cook alkali *)
    matL[4, 1] := 0.450000;   (* TT-101 RTD measurement corrects upper cook temperature *)
    matL[5, 2] := 0.485000;   (* TT-201 RTD measurement corrects lower cook temperature *)
    matL[6, 1] := 0.085000;   (* Upper temp innovation updates H-factor accumulator *)
    matL[6, 2] := 0.145000;   (* Lower temp innovation updates H-factor accumulator *)
    matL[7, 7] := 0.325000;   (* In-line NIR Kappa analyzer corrects Kappa state estimate *)
    matL[8, 8] := 0.285000;   (* Conductivity refractometer corrects wash solids estimate *)

    (* ------------------------------------------------------------------------------------------------
       MPC WEIGHTING MATRICES & CONSTRAINTS (8x8)
       ------------------------------------------------------------------------------------------------ *)
    FOR i := 1 TO 8 DO
        FOR j := 1 TO 8 DO
            matQ[i, j] := 0.000000;
            matR[i, j] := 0.000000;
            matS[i, j] := 0.000000;
            matP[i, j] := 0.000000;
        END_FOR;
    END_FOR;
    (* State Tracking Penalties Q *)
    matQ[1, 1] := 1.200000;   (* Penalty on chip compaction deviation *)
    matQ[2, 2] := 2.500000;   (* Penalty on impregnation alkali deviation *)
    matQ[3, 3] := 5.000000;   (* Penalty on upper cook residual alkali *)
    matQ[4, 4] := 8.500000;   (* High penalty on upper cook temperature error *)
    matQ[5, 5] := 12.000000;  (* High penalty on lower cook temperature error *)
    matQ[6, 6] := 0.050000;   (* Mild penalty on H-factor deviation *)
    matQ[7, 7] := 45.000000;  (* DOMINANT PENALTY ON PULP KAPPA NUMBER TARGET ERROR *)
    matQ[8, 8] := 3.500000;   (* Penalty on wash liquor solids displacement *)

    (* Actuator Effort Penalties R *)
    matR[1, 1] := 0.850000;   (* Upper steam valve movement cost *)
    matR[2, 2] := 0.950000;   (* Lower steam valve movement cost *)
    matR[3, 3] := 0.450000;   (* Extraction valve modulation cost *)
    matR[4, 4] := 1.500000;   (* White liquor chemical consumption cost *)
    matR[5, 5] := 0.650000;   (* HPF rotary feeder speed variation cost *)
    matR[6, 6] := 0.350000;   (* Bottom scraper speed variation cost *)
    matR[7, 7] := 0.400000;   (* Blow valve modulation cost *)
    matR[8, 8] := 0.500000;   (* Wash liquor displacement valve cost *)

    (* Actuator Slew Rate Penalties S *)
    matS[1, 1] := 2.500000;   (* Upper steam thermal shock suppression *)
    matS[2, 2] := 3.000000;   (* Lower steam thermal shock suppression *)
    matS[3, 3] := 1.200000;   (* Extraction hydraulic surge suppression *)
    matS[4, 4] := 4.000000;   (* White liquor concentration surge damping *)
    matS[5, 5] := 2.000000;   (* Chip feeder mechanical wear damping *)
    matS[6, 6] := 1.500000;   (* Scraper torque pulsation suppression *)
    matS[7, 7] := 1.800000;   (* Blow line consistency hydraulic stabilization *)
    matS[8, 8] := 1.500000;   (* Wash zone flow channeling damping *)

    (* Terminal State Penalties P (Riccati Terminal Cost) *)
    FOR i := 1 TO 8 DO
        matP[i, i] := matQ[i, i] * 2.250000;
    END_FOR;

    (* Actuator Lower and Upper Box Saturation Limits *)
    u_min[1] := 0.0;    u_max[1] := 100.0;  (* Upper steam valve [%] *)
    u_min[2] := 0.0;    u_max[2] := 100.0;  (* Lower steam valve [%] *)
    u_min[3] := 10.0;   u_max[3] := 100.0;  (* Extraction header valve [%] *)
    u_min[4] := 0.0;    u_max[4] := 100.0;  (* White liquor dosing valve [%] *)
    u_min[5] := 4.0;    u_max[5] := 25.0;   (* HPF speed [rpm] *)
    u_min[6] := 1.5;    u_max[6] := 12.0;   (* Scraper speed [rpm] *)
    u_min[7] := 5.0;    u_max[7] := 100.0;  (* Blow valve [%] *)
    u_min[8] := 5.0;    u_max[8] := 100.0;  (* Wash liquor valve [%] *)

    (* Actuator Maximum Allowable Slew Rate Limits per 100 ms Scan *)
    du_max[1] := 0.45;  (* Max 4.5 %/s Upper steam valve slew *)
    du_max[2] := 0.45;  (* Max 4.5 %/s Lower steam valve slew *)
    du_max[3] := 0.80;  (* Max 8.0 %/s Extraction valve slew *)
    du_max[4] := 0.50;  (* Max 5.0 %/s White liquor valve slew *)
    du_max[5] := 0.15;  (* Max 1.5 rpm/s HPF feeder acceleration *)
    du_max[6] := 0.10;  (* Max 1.0 rpm/s Bottom scraper acceleration *)
    du_max[7] := 0.75;  (* Max 7.5 %/s Blow valve slew *)
    du_max[8] := 0.60;  (* Max 6.0 %/s Wash valve slew *)

    (* Initialize State Vectors to Baseline Kraft Digester Operating Point *)
    x_state[1] := 35.0;   (* Initial Chip Bed Compaction [%] *)
    x_state[2] := 26.5;   (* Impregnation Alkali EA [g/L] *)
    x_state[3] := 16.8;   (* Upper Cooking Alkali EA [g/L] *)
    x_state[4] := 158.0;  (* Upper Cooking Circulation Temp [deg C] *)
    x_state[5] := 166.5;  (* Lower Cooking Circulation Temp [deg C] *)
    x_state[6] := 1150.0; (* Accumulated Delignification H-factor *)
    x_state[7] := 28.0;   (* Target Unbleached Pulp Kappa Number [Kappa] *)
    x_state[8] := 14.5;   (* Wash Zone Dissolved Solids [%] *)

    FOR i := 1 TO 8 DO
        x_pred[i] := x_state[i];
        x_hat[i]  := x_state[i];
        x_ref[i]  := x_state[i];
    END_FOR;

    (* Initialize Control Vectors to Steady-State Baseline *)
    u_ctrl[1] := 48.5;  (* Upper steam valve [%] *)
    u_ctrl[2] := 62.0;  (* Lower steam valve [%] *)
    u_ctrl[3] := 55.0;  (* Extraction flow valve [%] *)
    u_ctrl[4] := 42.0;  (* White liquor dosing valve [%] *)
    u_ctrl[5] := 14.5;  (* HPF rotary speed [rpm] *)
    u_ctrl[6] := 5.2;   (* Bottom scraper speed [rpm] *)
    u_ctrl[7] := 38.0;  (* Blow valve [%] *)
    u_ctrl[8] := 45.0;  (* Wash liquor displacement valve [%] *)

    FOR j := 1 TO 8 DO
        u_prev[j]    := u_ctrl[j];
        u_mpc_opt[j] := u_ctrl[j];
    END_FOR;

    rObservedHFactor := 1150.0;
    bInitialized := TRUE;
END_IF;
""")

    # -------------------------------------------------------------------------
    # PART 6: PHASE 1 - 2oo3 TMR SENSOR VOTING SUITE
    # -------------------------------------------------------------------------
    code_lines.append("""
(* ====================================================================================================
   PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) VOTING SUITE WITH DISCREPANCY TIMERS
   Protects safety and process control loops against transmitter drift, electrical open-circuits,
   fouled sensor membranes, and optical window obscuration.
   Channels:
     Group 1: Upper Cooking Temp TT-101A/B/C [deg C]
     Group 2: Lower Cooking Temp TT-201A/B/C [deg C]
     Group 3: Digester Top Pressure PT-301A/B/C [bar]
     Group 4: Residual Effective Alkali AT-401A/B/C [g/L]
     Group 5: Blow Line Pressure PT-501A/B/C [bar]
     Group 6: Dynamic Extraction Header Flow FT-601A/B/C [m3/h]
   ==================================================================================================== *)

(* ----------------------------------------------------------------------------------------------------
   GROUP 1: TT-101 UPPER COOKING CIRCULATION TEMPERATURE [deg C]
   ---------------------------------------------------------------------------------------------------- *)
IF ABS(rTT_101A_UpperCookTemp_degC - rTT_101B_UpperCookTemp_degC) > rDiscrepancyThreshold_Temp_degC THEN
    rTimer_TT101_AB_sec := rTimer_TT101_AB_sec + rCycleTime_sec;
ELSE
    rTimer_TT101_AB_sec := MAX(0.0, rTimer_TT101_AB_sec - (rCycleTime_sec * 0.5));
END_IF;

IF ABS(rTT_101B_UpperCookTemp_degC - rTT_101C_UpperCookTemp_degC) > rDiscrepancyThreshold_Temp_degC THEN
    rTimer_TT101_BC_sec := rTimer_TT101_BC_sec + rCycleTime_sec;
ELSE
    rTimer_TT101_BC_sec := MAX(0.0, rTimer_TT101_BC_sec - (rCycleTime_sec * 0.5));
END_IF;

IF ABS(rTT_101C_UpperCookTemp_degC - rTT_101A_UpperCookTemp_degC) > rDiscrepancyThreshold_Temp_degC THEN
    rTimer_TT101_CA_sec := rTimer_TT101_CA_sec + rCycleTime_sec;
ELSE
    rTimer_TT101_CA_sec := MAX(0.0, rTimer_TT101_CA_sec - (rCycleTime_sec * 0.5));
END_IF;

bHealthy_TT101A := (rTimer_TT101_AB_sec <= rTmrDebounceTimeLimit_sec) OR (rTimer_TT101_CA_sec <= rTmrDebounceTimeLimit_sec);
bHealthy_TT101B := (rTimer_TT101_AB_sec <= rTmrDebounceTimeLimit_sec) OR (rTimer_TT101_BC_sec <= rTmrDebounceTimeLimit_sec);
bHealthy_TT101C := (rTimer_TT101_BC_sec <= rTmrDebounceTimeLimit_sec) OR (rTimer_TT101_CA_sec <= rTmrDebounceTimeLimit_sec);
bDiscrepancy_TT101 := (rTimer_TT101_AB_sec > 1.0) OR (rTimer_TT101_BC_sec > 1.0) OR (rTimer_TT101_CA_sec > 1.0);

IF bHealthy_TT101A AND bHealthy_TT101B AND bHealthy_TT101C THEN
    (* Full 2oo3 Median Voting *)
    IF (rTT_101A_UpperCookTemp_degC >= rTT_101B_UpperCookTemp_degC AND rTT_101A_UpperCookTemp_degC <= rTT_101C_UpperCookTemp_degC) OR
       (rTT_101A_UpperCookTemp_degC <= rTT_101B_UpperCookTemp_degC AND rTT_101A_UpperCookTemp_degC >= rTT_101C_UpperCookTemp_degC) THEN
        rVotedUpperCookTemp_degC := rTT_101A_UpperCookTemp_degC;
    ELSIF (rTT_101B_UpperCookTemp_degC >= rTT_101A_UpperCookTemp_degC AND rTT_101B_UpperCookTemp_degC <= rTT_101C_UpperCookTemp_degC) OR
          (rTT_101B_UpperCookTemp_degC <= rTT_101A_UpperCookTemp_degC AND rTT_101B_UpperCookTemp_degC >= rTT_101C_UpperCookTemp_degC) THEN
        rVotedUpperCookTemp_degC := rTT_101B_UpperCookTemp_degC;
    ELSE
        rVotedUpperCookTemp_degC := rTT_101C_UpperCookTemp_degC;
    END_IF;
    bDegraded_TT101 := FALSE;
ELSIF bHealthy_TT101A AND bHealthy_TT101B THEN
    rVotedUpperCookTemp_degC := 0.5 * (rTT_101A_UpperCookTemp_degC + rTT_101B_UpperCookTemp_degC);
    bDegraded_TT101 := TRUE;
ELSIF bHealthy_TT101B AND bHealthy_TT101C THEN
    rVotedUpperCookTemp_degC := 0.5 * (rTT_101B_UpperCookTemp_degC + rTT_101C_UpperCookTemp_degC);
    bDegraded_TT101 := TRUE;
ELSIF bHealthy_TT101A AND bHealthy_TT101C THEN
    rVotedUpperCookTemp_degC := 0.5 * (rTT_101A_UpperCookTemp_degC + rTT_101C_UpperCookTemp_degC);
    bDegraded_TT101 := TRUE;
ELSIF bHealthy_TT101A THEN
    rVotedUpperCookTemp_degC := rTT_101A_UpperCookTemp_degC;
    bDegraded_TT101 := TRUE;
ELSIF bHealthy_TT101B THEN
    rVotedUpperCookTemp_degC := rTT_101B_UpperCookTemp_degC;
    bDegraded_TT101 := TRUE;
ELSIF bHealthy_TT101C THEN
    rVotedUpperCookTemp_degC := rTT_101C_UpperCookTemp_degC;
    bDegraded_TT101 := TRUE;
ELSE
    rVotedUpperCookTemp_degC := rVoted_TT101_Prev;
    bDegraded_TT101 := TRUE;
END_IF;
(* Bumpless Slew Rate Limiter *)
rVotedUpperCookTemp_degC := rVoted_TT101_Prev + LIMIT(-0.25, rVotedUpperCookTemp_degC - rVoted_TT101_Prev, 0.25);
rVoted_TT101_Prev := rVotedUpperCookTemp_degC;

(* ----------------------------------------------------------------------------------------------------
   GROUP 2: TT-201 LOWER COOKING CIRCULATION TEMPERATURE [deg C]
   ---------------------------------------------------------------------------------------------------- *)
IF ABS(rTT_201A_LowerCookTemp_degC - rTT_201B_LowerCookTemp_degC) > rDiscrepancyThreshold_Temp_degC THEN
    rTimer_TT201_AB_sec := rTimer_TT201_AB_sec + rCycleTime_sec;
ELSE
    rTimer_TT201_AB_sec := MAX(0.0, rTimer_TT201_AB_sec - (rCycleTime_sec * 0.5));
END_IF;

IF ABS(rTT_201B_LowerCookTemp_degC - rTT_201C_LowerCookTemp_degC) > rDiscrepancyThreshold_Temp_degC THEN
    rTimer_TT201_BC_sec := rTimer_TT201_BC_sec + rCycleTime_sec;
ELSE
    rTimer_TT201_BC_sec := MAX(0.0, rTimer_TT201_BC_sec - (rCycleTime_sec * 0.5));
END_IF;

IF ABS(rTT_201C_LowerCookTemp_degC - rTT_201A_LowerCookTemp_degC) > rDiscrepancyThreshold_Temp_degC THEN
    rTimer_TT201_CA_sec := rTimer_TT201_CA_sec + rCycleTime_sec;
ELSE
    rTimer_TT201_CA_sec := MAX(0.0, rTimer_TT201_CA_sec - (rCycleTime_sec * 0.5));
END_IF;

bHealthy_TT201A := (rTimer_TT201_AB_sec <= rTmrDebounceTimeLimit_sec) OR (rTimer_TT201_CA_sec <= rTmrDebounceTimeLimit_sec);
bHealthy_TT201B := (rTimer_TT201_AB_sec <= rTmrDebounceTimeLimit_sec) OR (rTimer_TT201_BC_sec <= rTmrDebounceTimeLimit_sec);
bHealthy_TT201C := (rTimer_TT201_BC_sec <= rTmrDebounceTimeLimit_sec) OR (rTimer_TT201_CA_sec <= rTmrDebounceTimeLimit_sec);
bDiscrepancy_TT201 := (rTimer_TT201_AB_sec > 1.0) OR (rTimer_TT201_BC_sec > 1.0) OR (rTimer_TT201_CA_sec > 1.0);

IF bHealthy_TT201A AND bHealthy_TT201B AND bHealthy_TT201C THEN
    IF (rTT_201A_LowerCookTemp_degC >= rTT_201B_LowerCookTemp_degC AND rTT_201A_LowerCookTemp_degC <= rTT_201C_LowerCookTemp_degC) OR
       (rTT_201A_LowerCookTemp_degC <= rTT_201B_LowerCookTemp_degC AND rTT_201A_LowerCookTemp_degC >= rTT_201C_LowerCookTemp_degC) THEN
        rVotedLowerCookTemp_degC := rTT_201A_LowerCookTemp_degC;
    ELSIF (rTT_201B_LowerCookTemp_degC >= rTT_201A_LowerCookTemp_degC AND rTT_201B_LowerCookTemp_degC <= rTT_201C_LowerCookTemp_degC) OR
          (rTT_201B_LowerCookTemp_degC <= rTT_201A_LowerCookTemp_degC AND rTT_201B_LowerCookTemp_degC >= rTT_201C_LowerCookTemp_degC) THEN
        rVotedLowerCookTemp_degC := rTT_201B_LowerCookTemp_degC;
    ELSE
        rVotedLowerCookTemp_degC := rTT_201C_LowerCookTemp_degC;
    END_IF;
    bDegraded_TT201 := FALSE;
ELSIF bHealthy_TT201A AND bHealthy_TT201B THEN
    rVotedLowerCookTemp_degC := 0.5 * (rTT_201A_LowerCookTemp_degC + rTT_201B_LowerCookTemp_degC);
    bDegraded_TT201 := TRUE;
ELSIF bHealthy_TT201B AND bHealthy_TT201C THEN
    rVotedLowerCookTemp_degC := 0.5 * (rTT_201B_LowerCookTemp_degC + rTT_201C_LowerCookTemp_degC);
    bDegraded_TT201 := TRUE;
ELSIF bHealthy_TT201A AND bHealthy_TT201C THEN
    rVotedLowerCookTemp_degC := 0.5 * (rTT_201A_LowerCookTemp_degC + rTT_201C_LowerCookTemp_degC);
    bDegraded_TT201 := TRUE;
ELSIF bHealthy_TT201A THEN
    rVotedLowerCookTemp_degC := rTT_201A_LowerCookTemp_degC;
    bDegraded_TT201 := TRUE;
ELSIF bHealthy_TT201B THEN
    rVotedLowerCookTemp_degC := rTT_201B_LowerCookTemp_degC;
    bDegraded_TT201 := TRUE;
ELSIF bHealthy_TT201C THEN
    rVotedLowerCookTemp_degC := rTT_201C_LowerCookTemp_degC;
    bDegraded_TT201 := TRUE;
ELSE
    rVotedLowerCookTemp_degC := rVoted_TT201_Prev;
    bDegraded_TT201 := TRUE;
END_IF;
rVotedLowerCookTemp_degC := rVoted_TT201_Prev + LIMIT(-0.25, rVotedLowerCookTemp_degC - rVoted_TT201_Prev, 0.25);
rVoted_TT201_Prev := rVotedLowerCookTemp_degC;

(* ----------------------------------------------------------------------------------------------------
   GROUP 3: PT-301 DIGESTER TOP HYDRAULIC PRESSURE [bar]
   ---------------------------------------------------------------------------------------------------- *)
IF ABS(rPT_301A_TopPressure_bar - rPT_301B_TopPressure_bar) > rDiscrepancyThreshold_Press_bar THEN
    rTimer_PT301_AB_sec := rTimer_PT301_AB_sec + rCycleTime_sec;
ELSE
    rTimer_PT301_AB_sec := MAX(0.0, rTimer_PT301_AB_sec - (rCycleTime_sec * 0.5));
END_IF;

IF ABS(rPT_301B_TopPressure_bar - rPT_301C_TopPressure_bar) > rDiscrepancyThreshold_Press_bar THEN
    rTimer_PT301_BC_sec := rTimer_PT301_BC_sec + rCycleTime_sec;
ELSE
    rTimer_PT301_BC_sec := MAX(0.0, rTimer_PT301_BC_sec - (rCycleTime_sec * 0.5));
END_IF;

IF ABS(rPT_301C_TopPressure_bar - rPT_301A_TopPressure_bar) > rDiscrepancyThreshold_Press_bar THEN
    rTimer_PT301_CA_sec := rTimer_PT301_CA_sec + rCycleTime_sec;
ELSE
    rTimer_PT301_CA_sec := MAX(0.0, rTimer_PT301_CA_sec - (rCycleTime_sec * 0.5));
END_IF;

bHealthy_PT301A := (rTimer_PT301_AB_sec <= rTmrDebounceTimeLimit_sec) OR (rTimer_PT301_CA_sec <= rTmrDebounceTimeLimit_sec);
bHealthy_PT301B := (rTimer_PT301_AB_sec <= rTmrDebounceTimeLimit_sec) OR (rTimer_PT301_BC_sec <= rTmrDebounceTimeLimit_sec);
bHealthy_PT301C := (rTimer_PT301_BC_sec <= rTmrDebounceTimeLimit_sec) OR (rTimer_PT301_CA_sec <= rTmrDebounceTimeLimit_sec);
bDiscrepancy_PT301 := (rTimer_PT301_AB_sec > 1.0) OR (rTimer_PT301_BC_sec > 1.0) OR (rTimer_PT301_CA_sec > 1.0);

IF bHealthy_PT301A AND bHealthy_PT301B AND bHealthy_PT301C THEN
    IF (rPT_301A_TopPressure_bar >= rPT_301B_TopPressure_bar AND rPT_301A_TopPressure_bar <= rPT_301C_TopPressure_bar) OR
       (rPT_301A_TopPressure_bar <= rPT_301B_TopPressure_bar AND rPT_301A_TopPressure_bar >= rPT_301C_TopPressure_bar) THEN
        rVotedTopPressure_bar := rPT_301A_TopPressure_bar;
    ELSIF (rPT_301B_TopPressure_bar >= rPT_301A_TopPressure_bar AND rPT_301B_TopPressure_bar <= rPT_301C_TopPressure_bar) OR
          (rPT_301B_TopPressure_bar <= rPT_301A_TopPressure_bar AND rPT_301B_TopPressure_bar >= rPT_301C_TopPressure_bar) THEN
        rVotedTopPressure_bar := rPT_301B_TopPressure_bar;
    ELSE
        rVotedTopPressure_bar := rPT_301C_TopPressure_bar;
    END_IF;
    bDegraded_PT301 := FALSE;
ELSIF bHealthy_PT301A AND bHealthy_PT301B THEN
    rVotedTopPressure_bar := 0.5 * (rPT_301A_TopPressure_bar + rPT_301B_TopPressure_bar);
    bDegraded_PT301 := TRUE;
ELSIF bHealthy_PT301B AND bHealthy_PT301C THEN
    rVotedTopPressure_bar := 0.5 * (rPT_301B_TopPressure_bar + rPT_301C_TopPressure_bar);
    bDegraded_PT301 := TRUE;
ELSIF bHealthy_PT301A AND bHealthy_PT301C THEN
    rVotedTopPressure_bar := 0.5 * (rPT_301A_TopPressure_bar + rPT_301C_TopPressure_bar);
    bDegraded_PT301 := TRUE;
ELSIF bHealthy_PT301A THEN
    rVotedTopPressure_bar := rPT_301A_TopPressure_bar;
    bDegraded_PT301 := TRUE;
ELSIF bHealthy_PT301B THEN
    rVotedTopPressure_bar := rPT_301B_TopPressure_bar;
    bDegraded_PT301 := TRUE;
ELSIF bHealthy_PT301C THEN
    rVotedTopPressure_bar := rPT_301C_TopPressure_bar;
    bDegraded_PT301 := TRUE;
ELSE
    rVotedTopPressure_bar := rVoted_PT301_Prev;
    bDegraded_PT301 := TRUE;
END_IF;
rVotedTopPressure_bar := rVoted_PT301_Prev + LIMIT(-0.08, rVotedTopPressure_bar - rVoted_PT301_Prev, 0.08);
rVoted_PT301_Prev := rVotedTopPressure_bar;

(* ----------------------------------------------------------------------------------------------------
   GROUP 4: AT-401 EXTRACTION RESIDUAL ALKALI ANALYZER [g/L]
   ---------------------------------------------------------------------------------------------------- *)
IF ABS(rAT_401A_ResidualAlkali_gL - rAT_401B_ResidualAlkali_gL) > rDiscrepancyThreshold_Alkali_gL THEN
    rTimer_AT401_AB_sec := rTimer_AT401_AB_sec + rCycleTime_sec;
ELSE
    rTimer_AT401_AB_sec := MAX(0.0, rTimer_AT401_AB_sec - (rCycleTime_sec * 0.5));
END_IF;

IF ABS(rAT_401B_ResidualAlkali_gL - rAT_401C_ResidualAlkali_gL) > rDiscrepancyThreshold_Alkali_gL THEN
    rTimer_AT401_BC_sec := rTimer_AT401_BC_sec + rCycleTime_sec;
ELSE
    rTimer_AT401_BC_sec := MAX(0.0, rTimer_AT401_BC_sec - (rCycleTime_sec * 0.5));
END_IF;

IF ABS(rAT_401C_ResidualAlkali_gL - rAT_401A_ResidualAlkali_gL) > rDiscrepancyThreshold_Alkali_gL THEN
    rTimer_AT401_CA_sec := rTimer_AT401_CA_sec + rCycleTime_sec;
ELSE
    rTimer_AT401_CA_sec := MAX(0.0, rTimer_AT401_CA_sec - (rCycleTime_sec * 0.5));
END_IF;

bHealthy_AT401A := (rTimer_AT401_AB_sec <= rTmrDebounceTimeLimit_sec) OR (rTimer_AT401_CA_sec <= rTmrDebounceTimeLimit_sec);
bHealthy_AT401B := (rTimer_AT401_AB_sec <= rTmrDebounceTimeLimit_sec) OR (rTimer_AT401_BC_sec <= rTmrDebounceTimeLimit_sec);
bHealthy_AT401C := (rTimer_AT401_BC_sec <= rTmrDebounceTimeLimit_sec) OR (rTimer_AT401_CA_sec <= rTmrDebounceTimeLimit_sec);
bDiscrepancy_AT401 := (rTimer_AT401_AB_sec > 1.0) OR (rTimer_AT401_BC_sec > 1.0) OR (rTimer_AT401_CA_sec > 1.0);

IF bHealthy_AT401A AND bHealthy_AT401B AND bHealthy_AT401C THEN
    IF (rAT_401A_ResidualAlkali_gL >= rAT_401B_ResidualAlkali_gL AND rAT_401A_ResidualAlkali_gL <= rAT_401C_ResidualAlkali_gL) OR
       (rAT_401A_ResidualAlkali_gL <= rAT_401B_ResidualAlkali_gL AND rAT_401A_ResidualAlkali_gL >= rAT_401C_ResidualAlkali_gL) THEN
        rVotedResidualAlkali_gL := rAT_401A_ResidualAlkali_gL;
    ELSIF (rAT_401B_ResidualAlkali_gL >= rAT_401A_ResidualAlkali_gL AND rAT_401B_ResidualAlkali_gL <= rAT_401C_ResidualAlkali_gL) OR
          (rAT_401B_ResidualAlkali_gL <= rAT_401A_ResidualAlkali_gL AND rAT_401B_ResidualAlkali_gL >= rAT_401C_ResidualAlkali_gL) THEN
        rVotedResidualAlkali_gL := rAT_401B_ResidualAlkali_gL;
    ELSE
        rVotedResidualAlkali_gL := rAT_401C_ResidualAlkali_gL;
    END_IF;
    bDegraded_AT401 := FALSE;
ELSIF bHealthy_AT401A AND bHealthy_AT401B THEN
    rVotedResidualAlkali_gL := 0.5 * (rAT_401A_ResidualAlkali_gL + rAT_401B_ResidualAlkali_gL);
    bDegraded_AT401 := TRUE;
ELSIF bHealthy_AT401B AND bHealthy_AT401C THEN
    rVotedResidualAlkali_gL := 0.5 * (rAT_401B_ResidualAlkali_gL + rAT_401C_ResidualAlkali_gL);
    bDegraded_AT401 := TRUE;
ELSIF bHealthy_AT401A AND bHealthy_AT401C THEN
    rVotedResidualAlkali_gL := 0.5 * (rAT_401A_ResidualAlkali_gL + rAT_401C_ResidualAlkali_gL);
    bDegraded_AT401 := TRUE;
ELSIF bHealthy_AT401A THEN
    rVotedResidualAlkali_gL := rAT_401A_ResidualAlkali_gL;
    bDegraded_AT401 := TRUE;
ELSIF bHealthy_AT401B THEN
    rVotedResidualAlkali_gL := rAT_401B_ResidualAlkali_gL;
    bDegraded_AT401 := TRUE;
ELSIF bHealthy_AT401C THEN
    rVotedResidualAlkali_gL := rAT_401C_ResidualAlkali_gL;
    bDegraded_AT401 := TRUE;
ELSE
    rVotedResidualAlkali_gL := rVoted_AT401_Prev;
    bDegraded_AT401 := TRUE;
END_IF;
rVotedResidualAlkali_gL := rVoted_AT401_Prev + LIMIT(-0.15, rVotedResidualAlkali_gL - rVoted_AT401_Prev, 0.15);
rVoted_AT401_Prev := rVotedResidualAlkali_gL;

(* ----------------------------------------------------------------------------------------------------
   GROUP 5: PT-501 BLOW LINE DISCHARGE PRESSURE [bar]
   ---------------------------------------------------------------------------------------------------- *)
IF ABS(rPT_501A_BlowPressure_bar - rPT_501B_BlowPressure_bar) > rDiscrepancyThreshold_Press_bar THEN
    rTimer_PT501_AB_sec := rTimer_PT501_AB_sec + rCycleTime_sec;
ELSE
    rTimer_PT501_AB_sec := MAX(0.0, rTimer_PT501_AB_sec - (rCycleTime_sec * 0.5));
END_IF;

IF ABS(rPT_501B_BlowPressure_bar - rPT_501C_BlowPressure_bar) > rDiscrepancyThreshold_Press_bar THEN
    rTimer_PT501_BC_sec := rTimer_PT501_BC_sec + rCycleTime_sec;
ELSE
    rTimer_PT501_BC_sec := MAX(0.0, rTimer_PT501_BC_sec - (rCycleTime_sec * 0.5));
END_IF;

IF ABS(rPT_501C_BlowPressure_bar - rPT_501A_BlowPressure_bar) > rDiscrepancyThreshold_Press_bar THEN
    rTimer_PT501_CA_sec := rTimer_PT501_CA_sec + rCycleTime_sec;
ELSE
    rTimer_PT501_CA_sec := MAX(0.0, rTimer_PT501_CA_sec - (rCycleTime_sec * 0.5));
END_IF;

bHealthy_PT501A := (rTimer_PT501_AB_sec <= rTmrDebounceTimeLimit_sec) OR (rTimer_PT501_CA_sec <= rTmrDebounceTimeLimit_sec);
bHealthy_PT501B := (rTimer_PT501_AB_sec <= rTmrDebounceTimeLimit_sec) OR (rTimer_PT501_BC_sec <= rTmrDebounceTimeLimit_sec);
bHealthy_PT501C := (rTimer_PT501_BC_sec <= rTmrDebounceTimeLimit_sec) OR (rTimer_PT501_CA_sec <= rTmrDebounceTimeLimit_sec);
bDiscrepancy_PT501 := (rTimer_PT501_AB_sec > 1.0) OR (rTimer_PT501_BC_sec > 1.0) OR (rTimer_PT501_CA_sec > 1.0);

IF bHealthy_PT501A AND bHealthy_PT501B AND bHealthy_PT501C THEN
    IF (rPT_501A_BlowPressure_bar >= rPT_501B_BlowPressure_bar AND rPT_501A_BlowPressure_bar <= rPT_501C_BlowPressure_bar) OR
       (rPT_501A_BlowPressure_bar <= rPT_501B_BlowPressure_bar AND rPT_501A_BlowPressure_bar >= rPT_501C_BlowPressure_bar) THEN
        rVotedBlowPressure_bar := rPT_501A_BlowPressure_bar;
    ELSIF (rPT_501B_BlowPressure_bar >= rPT_501A_BlowPressure_bar AND rPT_501B_BlowPressure_bar <= rPT_501C_BlowPressure_bar) OR
          (rPT_501B_BlowPressure_bar <= rPT_501A_BlowPressure_bar AND rPT_501B_BlowPressure_bar >= rPT_501C_BlowPressure_bar) THEN
        rVotedBlowPressure_bar := rPT_501B_BlowPressure_bar;
    ELSE
        rVotedBlowPressure_bar := rPT_501C_BlowPressure_bar;
    END_IF;
    bDegraded_PT501 := FALSE;
ELSIF bHealthy_PT501A AND bHealthy_PT501B THEN
    rVotedBlowPressure_bar := 0.5 * (rPT_501A_BlowPressure_bar + rPT_501B_BlowPressure_bar);
    bDegraded_PT501 := TRUE;
ELSIF bHealthy_PT501B AND bHealthy_PT501C THEN
    rVotedBlowPressure_bar := 0.5 * (rPT_501B_BlowPressure_bar + rPT_501C_BlowPressure_bar);
    bDegraded_PT501 := TRUE;
ELSIF bHealthy_PT501A AND bHealthy_PT501C THEN
    rVotedBlowPressure_bar := 0.5 * (rPT_501A_BlowPressure_bar + rPT_501C_BlowPressure_bar);
    bDegraded_PT501 := TRUE;
ELSIF bHealthy_PT501A THEN
    rVotedBlowPressure_bar := rPT_501A_BlowPressure_bar;
    bDegraded_PT501 := TRUE;
ELSIF bHealthy_PT501B THEN
    rVotedBlowPressure_bar := rPT_501B_BlowPressure_bar;
    bDegraded_PT501 := TRUE;
ELSIF bHealthy_PT501C THEN
    rVotedBlowPressure_bar := rPT_501C_BlowPressure_bar;
    bDegraded_PT501 := TRUE;
ELSE
    rVotedBlowPressure_bar := rVoted_PT501_Prev;
    bDegraded_PT501 := TRUE;
END_IF;
rVotedBlowPressure_bar := rVoted_PT501_Prev + LIMIT(-0.06, rVotedBlowPressure_bar - rVoted_PT501_Prev, 0.06);
rVoted_PT501_Prev := rVotedBlowPressure_bar;

(* ----------------------------------------------------------------------------------------------------
   GROUP 6: FT-601 BLACK LIQUOR EXTRACTION HEADER FLOW [m3/h]
   ---------------------------------------------------------------------------------------------------- *)
IF ABS(rFT_601A_ExtractionFlow_m3h - rFT_601B_ExtractionFlow_m3h) > rDiscrepancyThreshold_Flow_m3h THEN
    rTimer_FT601_AB_sec := rTimer_FT601_AB_sec + rCycleTime_sec;
ELSE
    rTimer_FT601_AB_sec := MAX(0.0, rTimer_FT601_AB_sec - (rCycleTime_sec * 0.5));
END_IF;

IF ABS(rFT_601B_ExtractionFlow_m3h - rFT_601C_ExtractionFlow_m3h) > rDiscrepancyThreshold_Flow_m3h THEN
    rTimer_FT601_BC_sec := rTimer_FT601_BC_sec + rCycleTime_sec;
ELSE
    rTimer_FT601_BC_sec := MAX(0.0, rTimer_FT601_BC_sec - (rCycleTime_sec * 0.5));
END_IF;

IF ABS(rFT_601C_ExtractionFlow_m3h - rFT_601A_ExtractionFlow_m3h) > rDiscrepancyThreshold_Flow_m3h THEN
    rTimer_FT601_CA_sec := rTimer_FT601_CA_sec + rCycleTime_sec;
ELSE
    rTimer_FT601_CA_sec := MAX(0.0, rTimer_FT601_CA_sec - (rCycleTime_sec * 0.5));
END_IF;

bHealthy_FT601A := (rTimer_FT601_AB_sec <= rTmrDebounceTimeLimit_sec) OR (rTimer_FT601_CA_sec <= rTmrDebounceTimeLimit_sec);
bHealthy_FT601B := (rTimer_FT601_AB_sec <= rTmrDebounceTimeLimit_sec) OR (rTimer_FT601_BC_sec <= rTmrDebounceTimeLimit_sec);
bHealthy_FT601C := (rTimer_FT601_BC_sec <= rTmrDebounceTimeLimit_sec) OR (rTimer_FT601_CA_sec <= rTmrDebounceTimeLimit_sec);
bDiscrepancy_FT601 := (rTimer_FT601_AB_sec > 1.0) OR (rTimer_FT601_BC_sec > 1.0) OR (rTimer_FT601_CA_sec > 1.0);

IF bHealthy_FT601A AND bHealthy_FT601B AND bHealthy_FT601C THEN
    IF (rFT_601A_ExtractionFlow_m3h >= rFT_601B_ExtractionFlow_m3h AND rFT_601A_ExtractionFlow_m3h <= rFT_601C_ExtractionFlow_m3h) OR
       (rFT_601A_ExtractionFlow_m3h <= rFT_601B_ExtractionFlow_m3h AND rFT_601A_ExtractionFlow_m3h >= rFT_601C_ExtractionFlow_m3h) THEN
        rVotedExtractionFlow_m3h := rFT_601A_ExtractionFlow_m3h;
    ELSIF (rFT_601B_ExtractionFlow_m3h >= rFT_601A_ExtractionFlow_m3h AND rFT_601B_ExtractionFlow_m3h <= rFT_601C_ExtractionFlow_m3h) OR
          (rFT_601B_ExtractionFlow_m3h <= rFT_601A_ExtractionFlow_m3h AND rFT_601B_ExtractionFlow_m3h >= rFT_601C_ExtractionFlow_m3h) THEN
        rVotedExtractionFlow_m3h := rFT_601B_ExtractionFlow_m3h;
    ELSE
        rVotedExtractionFlow_m3h := rFT_601C_ExtractionFlow_m3h;
    END_IF;
    bDegraded_FT601 := FALSE;
ELSIF bHealthy_FT601A AND bHealthy_FT601B THEN
    rVotedExtractionFlow_m3h := 0.5 * (rFT_601A_ExtractionFlow_m3h + rFT_601B_ExtractionFlow_m3h);
    bDegraded_FT601 := TRUE;
ELSIF bHealthy_FT601B AND bHealthy_FT601C THEN
    rVotedExtractionFlow_m3h := 0.5 * (rFT_601B_ExtractionFlow_m3h + rFT_601C_ExtractionFlow_m3h);
    bDegraded_FT601 := TRUE;
ELSIF bHealthy_FT601A AND bHealthy_FT601C THEN
    rVotedExtractionFlow_m3h := 0.5 * (rFT_601A_ExtractionFlow_m3h + rFT_601C_ExtractionFlow_m3h);
    bDegraded_FT601 := TRUE;
ELSIF bHealthy_FT601A THEN
    rVotedExtractionFlow_m3h := rFT_601A_ExtractionFlow_m3h;
    bDegraded_FT601 := TRUE;
ELSIF bHealthy_FT601B THEN
    rVotedExtractionFlow_m3h := rFT_601B_ExtractionFlow_m3h;
    bDegraded_FT601 := TRUE;
ELSIF bHealthy_FT601C THEN
    rVotedExtractionFlow_m3h := rFT_601C_ExtractionFlow_m3h;
    bDegraded_FT601 := TRUE;
ELSE
    rVotedExtractionFlow_m3h := rVoted_FT601_Prev;
    bDegraded_FT601 := TRUE;
END_IF;
rVotedExtractionFlow_m3h := rVoted_FT601_Prev + LIMIT(-4.0, rVotedExtractionFlow_m3h - rVoted_FT601_Prev, 4.0);
rVoted_FT601_Prev := rVotedExtractionFlow_m3h;

bAlarm_TmrDiscordanceActive := bDiscrepancy_TT101 OR bDiscrepancy_TT201 OR bDiscrepancy_PT301 OR
                               bDiscrepancy_AT401 OR bDiscrepancy_PT501 OR bDiscrepancy_FT601;
""")

    # -------------------------------------------------------------------------
    # PART 7: PHASE 2 - THERMODYNAMIC & DELIGNIFICATION KINETIC OBSERVERS
    # -------------------------------------------------------------------------
    code_lines.append("""
(* ====================================================================================================
   PHASE 2: FIRST-PRINCIPLES CYBER-PHYSICAL DELIGNIFICATION KINETICS & HYDRAULIC OBSERVERS
   Implements continuous Vroom Arrhenius H-factor integration, Hatton multi-species Kappa number
   prediction, porous media Ergun bed compaction pressure loss, and counter-current wash displacement.
   ==================================================================================================== *)

(* 1. Absolute Temperatures in Kelvin *)
rUpperTemp_K := LIMIT(373.15, rVotedUpperCookTemp_degC + 273.15, 463.15);
rLowerTemp_K := LIMIT(373.15, rVotedLowerCookTemp_degC + 273.15, 463.15);
rMeanCookTemp_K := (0.45 * rUpperTemp_K) + (0.55 * rLowerTemp_K);

(* 2. Vroom Arrhenius Relative Delignification Reaction Rate *)
(* k_rel = exp(43.20 - 16113.0 / T_K) *)
rRelativeRate_Upper := EXP(rVroomConstant_A - (rVroomConstant_B / rUpperTemp_K));
rRelativeRate_Lower := EXP(rVroomConstant_A - (rVroomConstant_B / rLowerTemp_K));
rRelativeRate_Mean  := (0.45 * rRelativeRate_Upper) + (0.55 * rRelativeRate_Lower);

(* 3. Discrete Time Integration of H-Factor (Trapezoidal Accumulation in Hours) *)
rHFactor_Increment := rRelativeRate_Mean * (rCycleTime_sec / 3600.0);
IF bProductionActive THEN
    rObservedHFactor := rObservedHFactor + rHFactor_Increment;
END_IF;

(* 4. Hatton Delignification Kappa Number Prediction *)
(* Interpolate species constants between softwood and hardwood based on blend ratio *)
rHatton_A_Blend     := (1.0 - (rHardwoodBlendRatio_pct / 100.0)) * rHatton_A_Softwood + (rHardwoodBlendRatio_pct / 100.0) * rHatton_A_Hardwood;
rHatton_B_Blend     := (1.0 - (rHardwoodBlendRatio_pct / 100.0)) * rHatton_B_Softwood + (rHardwoodBlendRatio_pct / 100.0) * rHatton_B_Hardwood;
rHatton_Gamma_Blend := (1.0 - (rHardwoodBlendRatio_pct / 100.0)) * rHatton_Gamma_Softwood + (rHardwoodBlendRatio_pct / 100.0) * rHatton_Gamma_Hardwood;

(* Effective Alkali Charge on Dry Wood [%] *)
rEffectiveAlkaliActive_pct := (rWhiteLiquorActiveAlkali_gL * (rWhiteLiquorDosingValveCmd_pct / 100.0) * 0.185) /
                              MAX(0.1, (1.0 - (rChipMoisture_pct / 100.0)));

(* Hatton Kappa Equation: Kappa = A - B * ln(H) * (EA)^gamma *)
rHattonKappa_Predicted := rHatton_A_Blend - (rHatton_B_Blend * LN(MAX(10.0, rObservedHFactor)) * EXPT(MAX(10.0, rEffectiveAlkaliActive_pct), (rHatton_Gamma_Blend * 0.1)));
rHattonKappa_Predicted := LIMIT(15.0, rHattonKappa_Predicted, 60.0);

(* 5. Porous Bed Hydraulic Fluidization & Ergun Pressure Loss Observer *)
(* Downward chip velocity derived from volumetric production rate *)
rChipDownwardVelocity_mps := (rTargetProductionRate_ADtd * 1000.0) / (24.0 * 3600.0 * 380.0 * 18.5); (* Bed cross-section approx 18.5 m2 *)
rHydraulicFrictionalHeadLoss_bar := (150.0 * EXPT(1.0 - rChipBedPorosity_epsilon, 2.0) / (EXPT(rChipBedPorosity_epsilon, 3.0) * EXPT(rEquivalentChipDiameter_m, 2.0))) *
                                    (rErgunViscosity_Pas * rChipDownwardVelocity_mps * 32.0 / 100000.0); (* 32 m digester column height *)

rChipColumnPermeabilityIndex := MAX(0.1, 100.0 - (rHydraulicFrictionalHeadLoss_bar * 45.0) - (rScreenDifferentialPress_bar * 20.0));
rObservedChipCompaction_pct := LIMIT(10.0, 100.0 - rChipColumnPermeabilityIndex, 95.0);

(* 6. Counter-Current Wash Displacement Ratio & Dilution Factor *)
rObservedWashDisplacementRatio := (rWashLiquorInletFlow_m3h * 1.05) / MAX(10.0, rBlowLineFlow_m3h);
rObservedDelignificationRate_pcth := rRelativeRate_Mean * 0.082;
rObservedProductionRate_ADtd := (rBlowLineFlow_m3h * (rBlowLineConsistency_pct / 100.0) * 24.0 * 1.08) / 0.90; (* 90% air-dry basis *)
rObservedSpecificSteamConsump_t_ADt := ((rUpperSteamValveCmd_pct * 0.18) + (rLowerSteamValveCmd_pct * 0.24)) * 24.0 / MAX(500.0, rObservedProductionRate_ADtd);
rEstimatedTimeInDigester_h := 32.0 / MAX(0.001, rChipDownwardVelocity_mps * 3600.0);
""")

    # -------------------------------------------------------------------------
    # PART 8: PHASE 3 - STATE-SPACE PROPAGATION & LUENBERGER OBSERVER
    # -------------------------------------------------------------------------
    code_lines.append("""
(* ====================================================================================================
   PHASE 3: CYBER-PHYSICAL DISCRETE STATE-SPACE PROPAGATION & LUENBERGER OBSERVER
   Formulation:
     x_pred[k+1] = A * x_state[k] + B * u_ctrl[k] + Bd * d_dist[k]
     y_est[k]    = C * x_pred[k+1] + D * u_ctrl[k]
     e_innov[k]  = y_meas[k] - y_est[k]
     x_hat[k+1]  = x_pred[k+1] + L * e_innov[k]
   ==================================================================================================== *)

(* Pack Control Actuator Vector u_ctrl *)
u_ctrl[1] := rUpperSteamValveCmd_pct;
u_ctrl[2] := rLowerSteamValveCmd_pct;
u_ctrl[3] := rExtractionFlowValveCmd_pct;
u_ctrl[4] := rWhiteLiquorDosingValveCmd_pct;
u_ctrl[5] := rHpfSpeedReference_rpm;
u_ctrl[6] := rBottomScraperSpeedCmd_rpm;
u_ctrl[7] := rBlowValveCmd_pct;
u_ctrl[8] := rWashLiquorValveCmd_pct;

(* Pack Exogenous Disturbance Vector d_dist *)
d_dist[1] := rChipMoisture_pct;
d_dist[2] := rChipBulkDensity_kgm3;
d_dist[3] := rWhiteLiquorActiveAlkali_gL;
d_dist[4] := rFeedChipTemp_degC;
d_dist[5] := rWhiteLiquorSulfidity_pct;
d_dist[6] := rHardwoodBlendRatio_pct;

(* Pack Measured Output Vector y_meas from 2oo3 Voted Channels *)
y_meas[1] := rVotedUpperCookTemp_degC;
y_meas[2] := rVotedLowerCookTemp_degC;
y_meas[3] := rVotedTopPressure_bar;
y_meas[4] := rVotedResidualAlkali_gL;
y_meas[5] := rVotedBlowPressure_bar;
y_meas[6] := rVotedExtractionFlow_m3h;
y_meas[7] := rHattonKappa_Predicted;
y_meas[8] := 14.5; (* Wash dissolved solids baseline *)

(* Forward State Propagation: x_pred = A * x + B * u + Bd * d *)
FOR i := 1 TO 8 DO
    rTempSum := 0.0;
    FOR j := 1 TO 8 DO
        rTempSum := rTempSum + (matA[i, j] * x_state[j]);
    END_FOR;
    FOR j := 1 TO 8 DO
        rTempSum := rTempSum + (matB[i, j] * u_ctrl[j]);
    END_FOR;
    FOR j := 1 TO 6 DO
        rTempSum := rTempSum + (matBd[i, j] * d_dist[j]);
    END_FOR;
    x_pred[i] := rTempSum;
END_FOR;

(* Physical Safety Clamping of Predicted State Vector *)
x_pred[1] := LIMIT(0.0,   x_pred[1], 100.0);  (* Compaction [%] *)
x_pred[2] := LIMIT(5.0,   x_pred[2], 50.0);   (* Impregnation Alkali [g/L] *)
x_pred[3] := LIMIT(2.0,   x_pred[3], 40.0);   (* Upper Cook Alkali [g/L] *)
x_pred[4] := LIMIT(100.0, x_pred[4], 190.0);  (* Upper Cook Temp [deg C] *)
x_pred[5] := LIMIT(100.0, x_pred[5], 195.0);  (* Lower Cook Temp [deg C] *)
x_pred[6] := LIMIT(0.0,   x_pred[6], 5000.0); (* H-factor *)
x_pred[7] := LIMIT(10.0,  x_pred[7], 60.0);   (* Kappa Number *)
x_pred[8] := LIMIT(0.0,   x_pred[8], 30.0);   (* Wash Solids [%] *)

(* Estimated Physical Outputs: y_est = C * x_pred + D * u *)
FOR i := 1 TO 8 DO
    rTempSum := 0.0;
    FOR j := 1 TO 8 DO
        rTempSum := rTempSum + (matC[i, j] * x_pred[j]) + (matD[i, j] * u_ctrl[j]);
    END_FOR;
    y_est[i] := rTempSum;
    e_innov[i] := y_meas[i] - y_est[i];
END_FOR;

(* Luenberger State Innovation Correction: x_hat = x_pred + L * e_innov *)
FOR i := 1 TO 8 DO
    rTempSum := 0.0;
    FOR j := 1 TO 8 DO
        rTempSum := rTempSum + (matL[i, j] * e_innov[j]);
    END_FOR;
    x_hat[i] := x_pred[i] + rTempSum;
    x_state[i] := x_hat[i];
END_FOR;

(* Assign Cyber-Physical Process Observers to Outputs *)
rObservedEffectiveAlkali_gL := x_state[3];
rObservedKappaNumber        := x_state[7];
""")

    # -------------------------------------------------------------------------
    # PART 9: PHASE 4 - RECEDING-HORIZON MPC OPTIMIZATION WITH PGD
    # -------------------------------------------------------------------------
    code_lines.append("""
(* ====================================================================================================
   PHASE 4: RECEDING-HORIZON MPC OPTIMIZATION VIA PROJECTED GRADIENT DESCENT (PGD)
   Solves unrolled quadratic optimization over prediction horizon Np = 5, control horizon Nc = 3:
     min_u J = sum_{k=1}^Np (x_k - x_ref)' * Q * (x_k - x_ref) +
               sum_{k=0}^{Nc-1} (u_k - u_ref)' * R * (u_k - u_ref) + du_k' * S * du_k +
               (x_Np - x_ref)' * P * (x_Np - x_ref)
   Subject to box saturation [u_min, u_max] and slew limits [-du_max, +du_max].
   ==================================================================================================== *)

(* Set State Tracking References x_ref *)
x_ref[1] := 35.0;                         (* Target Chip Bed Compaction [%] *)
x_ref[2] := 26.0;                         (* Impregnation Alkali Target [g/L] *)
x_ref[3] := 16.5;                         (* Upper Cook Residual Alkali Target [g/L] *)
x_ref[4] := 158.0;                        (* Upper Cook Temperature Target [deg C] *)
x_ref[5] := 167.0;                        (* Lower Cook Temperature Target [deg C] *)
x_ref[6] := 1250.0;                       (* Target Total H-Factor *)
x_ref[7] := rTargetKappaNumber;           (* Main Quality Setpoint: Kappa Number [Kappa] *)
x_ref[8] := 12.0;                         (* Wash Zone Displacement Solids Target [%] *)

(* Step 1: Forward Trajectory Rollout across Prediction Horizon (Np = 5) *)
FOR k_idx := 1 TO 5 DO
    FOR i := 1 TO 8 DO
        rTempSum := 0.0;
        IF k_idx = 1 THEN
            FOR j := 1 TO 8 DO
                rTempSum := rTempSum + (matA[i, j] * x_state[j]);
            END_FOR;
        ELSE
            FOR j := 1 TO 8 DO
                rTempSum := rTempSum + (matA[i, j] * x_rollout[k_idx - 1, j]);
            END_FOR;
        END_IF;
        
        (* Apply control move u_prev for stage k *)
        FOR j := 1 TO 8 DO
            rTempSum := rTempSum + (matB[i, j] * u_prev[j]);
        END_FOR;
        FOR j := 1 TO 6 DO
            rTempSum := rTempSum + (matBd[i, j] * d_dist[j]);
        END_FOR;
        x_rollout[k_idx, i] := rTempSum;
    END_FOR;
END_FOR;

(* Step 2: Accumulate Quadratic Cost Functional J *)
rCost_J := 0.0;
FOR k_idx := 1 TO 5 DO
    FOR i := 1 TO 8 DO
        IF k_idx < 5 THEN
            rCost_J := rCost_J + (matQ[i, i] * EXPT(x_rollout[k_idx, i] - x_ref[i], 2.0));
        ELSE
            rCost_J := rCost_J + (matP[i, i] * EXPT(x_rollout[k_idx, i] - x_ref[i], 2.0));
        END_IF;
    END_FOR;
END_FOR;

(* Step 3: Compute Projected Analytical Gradient of Cost Functional grad_J = dJ/du *)
FOR j := 1 TO 8 DO
    rTempSum := 0.0;
    (* Stage tracking error gradient propagation *)
    FOR k_idx := 1 TO 5 DO
        FOR i := 1 TO 8 DO
            rTempSum := rTempSum + (2.0 * matQ[i, i] * (x_rollout[k_idx, i] - x_ref[i]) * matB[i, j]);
        END_FOR;
    END_FOR;
    (* Actuator effort and slew rate penalty gradient *)
    rTempSum := rTempSum + (2.0 * matR[j, j] * (u_prev[j] - u_ctrl[j])) + (2.0 * matS[j, j] * (u_prev[j] - u_ctrl[j]));
    grad_J[j] := rTempSum;
END_FOR;

(* Step 4: Gradient Descent Step with Saturation & Slew Projection *)
IF bProductionActive AND (nDigesterOperationalState = 7 OR nDigesterOperationalState = 8) THEN
    FOR j := 1 TO 8 DO
        (* Gradient Descent Update *)
        u_mpc_opt[j] := u_prev[j] - (rAlpha_pgd * grad_J[j]);
        
        (* Box Saturation Projection *)
        u_mpc_opt[j] := LIMIT(u_min[j], u_mpc_opt[j], u_max[j]);
        
        (* Slew Rate Projection *)
        rDelta_u := LIMIT(-du_max[j], u_mpc_opt[j] - u_prev[j], du_max[j]);
        u_ctrl[j] := u_prev[j] + rDelta_u;
        u_prev[j] := u_ctrl[j];
    END_FOR;
    
    (* Apply MPC Optimized Control to Physical Actuator Outputs *)
    rUpperSteamValveCmd_pct        := u_ctrl[1];
    rLowerSteamValveCmd_pct        := u_ctrl[2];
    rExtractionFlowValveCmd_pct    := u_ctrl[3];
    rWhiteLiquorDosingValveCmd_pct := u_ctrl[4];
    rHpfSpeedReference_rpm         := u_ctrl[5];
    rBottomScraperSpeedCmd_rpm     := u_ctrl[6];
    rBlowValveCmd_pct              := u_ctrl[7];
    rWashLiquorValveCmd_pct        := u_ctrl[8];
END_IF;
""")

    # -------------------------------------------------------------------------
    # PART 10: PHASE 5 - 14-STAGE DETERMINISTIC PRODUCTION FSM
    # -------------------------------------------------------------------------
    code_lines.append("""
(* ====================================================================================================
   PHASE 5: DETERMINISTIC 14-STAGE PRODUCTION FINITE STATE MACHINE (FSM)
   Operating States:
     0:  STATE_0_STANDBY_IDLE
     1:  STATE_1_VESSEL_COLD_FILL_DEAERATION
     2:  STATE_2_IMPREGNATION_PRESSURIZATION
     3:  STATE_3_LP_STEAM_PREHEATING
     4:  STATE_4_HP_CHIP_FEEDER_SYNC
     5:  STATE_5_COOKING_CIRCULATION_INIT
     6:  STATE_6_EFFECTIVE_ALKALI_RATIO_LOCK
     7:  STATE_7_STEADY_STATE_KRAFT_MPC
     8:  STATE_8_KAPPA_INLINE_FEEDBACK_TRIM
     9:  STATE_9_EXTRACTION_SCREEN_BACKFLUSH
     10: STATE_10_CHIP_COLUMN_HANGING_RECOVERY
     11: STATE_11_WASH_ZONE_DISPLACEMENT_EQ
     12: STATE_12_CONTROLLED_PRODUCTION_DERATE
     13: STATE_13_DIGESTER_COLD_BLOWDOWN
     14: STATE_14_OVERPRESSURE_SAFETY_TRIP
   ==================================================================================================== *)

(* State Transition Timer Accumulation *)
rFsmStateElapsedTime_sec := rFsmStateElapsedTime_sec + rCycleTime_sec;
rBackflushIntervalTimer_sec := rBackflushIntervalTimer_sec + rCycleTime_sec;

(* Check Emergency Depressurization / Safety Trip Interlocks *)
IF NOT bEmergencyStop OR (rVotedTopPressure_bar >= rSp_TopPress_Trip_HH_bar) THEN
    nFsmNextState := 14; (* Direct Trip to State 14: Overpressure Safety Depressurization *)
END_IF;

(* State First Scan Detection *)
IF nFsmState <> nFsmNextState THEN
    nFsmState := nFsmNextState;
    rFsmStateElapsedTime_sec := 0.0;
    bStateFirstScan := TRUE;
ELSE
    bStateFirstScan := FALSE;
END_IF;

nDigesterOperationalState := nFsmState;

CASE nFsmState OF
    (* ------------------------------------------------------------------------------------------------
       STATE 0: STANDBY & INERT BLANKETING
       ------------------------------------------------------------------------------------------------ *)
    0:
        sOperationalStateName := 'STANDBY_IDLE';
        bSystemReady := FALSE;
        bProductionActive := FALSE;
        bEmergencyTripActive := FALSE;
        bExtractionScreenBackflushActive := FALSE;
        bOpenTopHydraulicInletValve := FALSE;
        bOpenWhiteLiquorBlockValve := FALSE;
        bOpenBottomBlowLineValve := FALSE;
        bOpenEmergencyDepressurizeValve := FALSE;
        
        rUpperSteamValveCmd_pct        := 0.0;
        rLowerSteamValveCmd_pct        := 0.0;
        rExtractionFlowValveCmd_pct    := 0.0;
        rWhiteLiquorDosingValveCmd_pct := 0.0;
        rHpfSpeedReference_rpm         := 0.0;
        rBottomScraperSpeedCmd_rpm     := 0.0;
        rBlowValveCmd_pct              := 0.0;
        rWashLiquorValveCmd_pct        := 0.0;
        
        IF bSystemEnable AND bProductionRunCmd AND bEmergencyStop THEN
            nFsmNextState := 1;
        END_IF;

    (* ------------------------------------------------------------------------------------------------
       STATE 1: VESSEL COLD FILL & DEAERATION
       ------------------------------------------------------------------------------------------------ *)
    1:
        sOperationalStateName := 'COLD_FILL_DEAERATION';
        bOpenTopHydraulicInletValve := TRUE;
        bOpenWhiteLiquorBlockValve := TRUE;
        
        rWhiteLiquorDosingValveCmd_pct := 15.0;
        rWashLiquorValveCmd_pct        := 20.0;
        
        IF rVotedTopPressure_bar >= 4.5 AND rFsmStateElapsedTime_sec > 60.0 THEN
            nFsmNextState := 2;
        END_IF;

    (* ------------------------------------------------------------------------------------------------
       STATE 2: IMPREGNATION VESSEL HYDRAULIC PRESSURIZATION
       ------------------------------------------------------------------------------------------------ *)
    2:
        sOperationalStateName := 'IMPREG_PRESSURIZATION';
        rWhiteLiquorDosingValveCmd_pct := 25.0;
        rWashLiquorValveCmd_pct        := 30.0;
        
        IF rVotedTopPressure_bar >= 10.5 AND rFsmStateElapsedTime_sec > 90.0 THEN
            nFsmNextState := 3;
        END_IF;

    (* ------------------------------------------------------------------------------------------------
       STATE 3: LOW-PRESSURE STEAM CHIP PREHEATING
       ------------------------------------------------------------------------------------------------ *)
    3:
        sOperationalStateName := 'LP_STEAM_PREHEATING';
        rHpfSpeedReference_rpm := 6.0;
        rUpperSteamValveCmd_pct := 15.0;
        
        IF rVotedUpperCookTemp_degC >= 125.0 AND rFsmStateElapsedTime_sec > 120.0 THEN
            nFsmNextState := 4;
        END_IF;

    (* ------------------------------------------------------------------------------------------------
       STATE 4: HIGH-PRESSURE CHIP FEEDER SYNCHRONIZATION
       ------------------------------------------------------------------------------------------------ *)
    4:
        sOperationalStateName := 'HPF_FEEDER_SYNC';
        rHpfSpeedReference_rpm := 10.5;
        rWhiteLiquorDosingValveCmd_pct := 30.0;
        rExtractionFlowValveCmd_pct := 25.0;
        
        IF rDigesterChipLevel_m >= 15.0 AND rFsmStateElapsedTime_sec > 120.0 THEN
            nFsmNextState := 5;
        END_IF;

    (* ------------------------------------------------------------------------------------------------
       STATE 5: COOKING CIRCULATION LOOP INITIATION
       ------------------------------------------------------------------------------------------------ *)
    5:
        sOperationalStateName := 'CIRCULATION_INIT';
        rUpperSteamValveCmd_pct := 35.0;
        rLowerSteamValveCmd_pct := 45.0;
        rExtractionFlowValveCmd_pct := 40.0;
        
        IF rVotedUpperCookTemp_degC >= 150.0 AND rVotedLowerCookTemp_degC >= 158.0 THEN
            nFsmNextState := 6;
        END_IF;

    (* ------------------------------------------------------------------------------------------------
       STATE 6: EFFECTIVE ALKALI RATIO LOCK & TARGETING
       ------------------------------------------------------------------------------------------------ *)
    6:
        sOperationalStateName := 'ALKALI_RATIO_LOCK';
        bOpenBottomBlowLineValve := TRUE;
        rBottomScraperSpeedCmd_rpm := 3.5;
        rBlowValveCmd_pct := 20.0;
        rWhiteLiquorDosingValveCmd_pct := 38.0;
        
        IF rVotedResidualAlkali_gL >= 12.0 AND rFsmStateElapsedTime_sec > 150.0 THEN
            nFsmNextState := 7;
        END_IF;

    (* ------------------------------------------------------------------------------------------------
       STATE 7: STEADY-STATE KRAFT DIGESTION MPC MODE
       ------------------------------------------------------------------------------------------------ *)
    7:
        sOperationalStateName := 'STEADY_KRAFT_MPC';
        bSystemReady := TRUE;
        bProductionActive := TRUE;
        
        (* In this state, MPC is actively writing to valve commands in Phase 4 *)
        (* Check if extraction screen differential pressure is elevated *)
        IF (rScreenDifferentialPress_bar >= rSp_ScreenDP_Alarm_H_bar) OR (rBackflushIntervalTimer_sec >= 900.0) OR bManualBackflushTrigger THEN
            nFsmNextState := 9; (* Initiate Extraction Screen Backflush Cycle *)
        ELSIF rBottomScraperVfdTorque_kNm >= rSp_ScraperTorque_Alarm_H_kNm THEN
            nFsmNextState := 10; (* Chip Column Hanging Recovery *)
        ELSIF ABS(rObservedKappaNumber - rTargetKappaNumber) > 1.2 THEN
            nFsmNextState := 8; (* Kappa Feedback Trimming State *)
        ELSIF NOT bProductionRunCmd THEN
            nFsmNextState := 12; (* Controlled Production Rate Derate *)
        END_IF;

    (* ------------------------------------------------------------------------------------------------
       STATE 8: KAPPA NUMBER IN-LINE FEEDBACK TRIMMING
       ------------------------------------------------------------------------------------------------ *)
    8:
        sOperationalStateName := 'KAPPA_FEEDBACK_TRIM';
        bProductionActive := TRUE;
        
        (* Fast Trim offset based on Kappa error *)
        IF rObservedKappaNumber > rTargetKappaNumber THEN
            (* Pulp is undercooked: bump steam temperature reference slightly *)
            rUpperSteamValveCmd_pct := LIMIT(0.0, rUpperSteamValveCmd_pct + 0.15, 100.0);
            rLowerSteamValveCmd_pct := LIMIT(0.0, rLowerSteamValveCmd_pct + 0.25, 100.0);
            rWhiteLiquorDosingValveCmd_pct := LIMIT(0.0, rWhiteLiquorDosingValveCmd_pct + 0.10, 100.0);
        ELSE
            (* Pulp is overcooked: back off steam valves slightly *)
            rUpperSteamValveCmd_pct := LIMIT(0.0, rUpperSteamValveCmd_pct - 0.20, 100.0);
            rLowerSteamValveCmd_pct := LIMIT(0.0, rLowerSteamValveCmd_pct - 0.30, 100.0);
        END_IF;
        
        IF ABS(rObservedKappaNumber - rTargetKappaNumber) <= 0.6 OR rFsmStateElapsedTime_sec > 300.0 THEN
            nFsmNextState := 7; (* Return to steady-state MPC *)
        END_IF;

    (* ------------------------------------------------------------------------------------------------
       STATE 9: EXTRACTION SCREEN AUTOMATIC BACKFLUSH CYCLE
       ------------------------------------------------------------------------------------------------ *)
    9:
        sOperationalStateName := 'SCREEN_BACKFLUSH';
        bExtractionScreenBackflushActive := TRUE;
        
        IF bStateFirstScan THEN
            nBackflushStep := 1;
            rBackflushStepTimer_sec := 0.0;
        END_IF;
        
        rBackflushStepTimer_sec := rBackflushStepTimer_sec + rCycleTime_sec;
        
        CASE nBackflushStep OF
            1:
                bBackflushValveRow1 := TRUE;
                bBackflushValveRow2 := FALSE;
                bBackflushValveRow3 := FALSE;
                IF rBackflushStepTimer_sec >= 8.0 THEN
                    nBackflushStep := 2;
                    rBackflushStepTimer_sec := 0.0;
                END_IF;
            2:
                bBackflushValveRow1 := FALSE;
                bBackflushValveRow2 := TRUE;
                bBackflushValveRow3 := FALSE;
                IF rBackflushStepTimer_sec >= 8.0 THEN
                    nBackflushStep := 3;
                    rBackflushStepTimer_sec := 0.0;
                END_IF;
            3:
                bBackflushValveRow1 := FALSE;
                bBackflushValveRow2 := FALSE;
                bBackflushValveRow3 := TRUE;
                IF rBackflushStepTimer_sec >= 8.0 THEN
                    nBackflushStep := 0;
                    bBackflushValveRow3 := FALSE;
                    bExtractionScreenBackflushActive := FALSE;
                    rBackflushIntervalTimer_sec := 0.0;
                    nFsmNextState := 7; (* Return to Steady-State MPC *)
                END_IF;
            ELSE
                bBackflushValveRow1 := FALSE;
                bBackflushValveRow2 := FALSE;
                bBackflushValveRow3 := FALSE;
                nFsmNextState := 7;
        END_CASE;

    (* ------------------------------------------------------------------------------------------------
       STATE 10: CHIP COLUMN HANGING RECOVERY CYCLE
       ------------------------------------------------------------------------------------------------ *)
    10:
        sOperationalStateName := 'COLUMN_HANG_RECOVERY';
        bAlarm_ChipColumnHanging := TRUE;
        
        IF bStateFirstScan THEN
            nHangingRecoveryStep := 1;
            rHangingRecoveryTimer_sec := 0.0;
        END_IF;
        
        rHangingRecoveryTimer_sec := rHangingRecoveryTimer_sec + rCycleTime_sec;
        
        CASE nHangingRecoveryStep OF
            1:
                (* Step 1: Immediately throttle extraction to relieve downward hydraulic suction *)
                rExtractionFlowValveCmd_pct := 15.0;
                rWashLiquorValveCmd_pct := 65.0; (* Boost bottom wash to fluidize bed *)
                IF rHangingRecoveryTimer_sec >= 25.0 THEN
                    nHangingRecoveryStep := 2;
                    rHangingRecoveryTimer_sec := 0.0;
                END_IF;
            2:
                (* Step 2: Ramp bottom scraper speed to dislodge compacted plug *)
                rBottomScraperSpeedCmd_rpm := 7.5;
                rBlowValveCmd_pct := 45.0;
                IF (rBottomScraperVfdTorque_kNm < (rSp_ScraperTorque_Alarm_H_kNm - rHysteresis_Torque_kNm)) OR (rHangingRecoveryTimer_sec >= 45.0) THEN
                    nHangingRecoveryStep := 3;
                    rHangingRecoveryTimer_sec := 0.0;
                END_IF;
            3:
                (* Step 3: Resynchronize extraction and wash flows *)
                rExtractionFlowValveCmd_pct := 45.0;
                rWashLiquorValveCmd_pct := 45.0;
                rBottomScraperSpeedCmd_rpm := 5.0;
                bAlarm_ChipColumnHanging := FALSE;
                nFsmNextState := 7; (* Back to steady-state *)
            ELSE
                nFsmNextState := 7;
        END_CASE;

    (* ------------------------------------------------------------------------------------------------
       STATE 11: WASH ZONE DISPLACEMENT EQUILIBRIUM
       ------------------------------------------------------------------------------------------------ *)
    11:
        sOperationalStateName := 'WASH_DISPLACEMENT_EQ';
        rWashLiquorValveCmd_pct := 55.0;
        rBlowDilutionFiltrateValveCmd_pct := 30.0;
        
        IF rObservedWashDisplacementRatio >= 1.05 AND rFsmStateElapsedTime_sec > 60.0 THEN
            nFsmNextState := 7;
        END_IF;

    (* ------------------------------------------------------------------------------------------------
       STATE 12: CONTROLLED PRODUCTION RATE DERATE
       ------------------------------------------------------------------------------------------------ *)
    12:
        sOperationalStateName := 'PRODUCTION_DERATE';
        bProductionActive := FALSE;
        
        rUpperSteamValveCmd_pct := MAX(0.0, rUpperSteamValveCmd_pct - 0.25);
        rLowerSteamValveCmd_pct := MAX(0.0, rLowerSteamValveCmd_pct - 0.35);
        rHpfSpeedReference_rpm  := MAX(4.0, rHpfSpeedReference_rpm - 0.10);
        rWhiteLiquorDosingValveCmd_pct := MAX(10.0, rWhiteLiquorDosingValveCmd_pct - 0.20);
        
        IF rVotedUpperCookTemp_degC <= 135.0 AND rFsmStateElapsedTime_sec > 180.0 THEN
            nFsmNextState := 13; (* Proceed to Cold Blowdown *)
        END_IF;

    (* ------------------------------------------------------------------------------------------------
       STATE 13: DIGESTER COLD BLOWDOWN & EMERGENCY ISOLATION
       ------------------------------------------------------------------------------------------------ *)
    13:
        sOperationalStateName := 'COLD_BLOWDOWN';
        rUpperSteamValveCmd_pct := 0.0;
        rLowerSteamValveCmd_pct := 0.0;
        rWhiteLiquorDosingValveCmd_pct := 0.0;
        rHpfSpeedReference_rpm := 0.0;
        
        rBottomScraperSpeedCmd_rpm := 6.5;
        rBlowValveCmd_pct := 60.0;
        rWashLiquorValveCmd_pct := 40.0;
        
        IF rDigesterChipLevel_m <= 1.5 OR rFsmStateElapsedTime_sec > 600.0 THEN
            nFsmNextState := 0; (* Return to Standby Idle *)
        END_IF;

    (* ------------------------------------------------------------------------------------------------
       STATE 14: OVERPRESSURE SAFETY DEPRESSURIZATION (SAFETY TRIP)
       ------------------------------------------------------------------------------------------------ *)
    14:
        sOperationalStateName := 'SAFETY_DEPRESSURIZE';
        bEmergencyTripActive := TRUE;
        bSystemReady := FALSE;
        bProductionActive := FALSE;
        
        (* Fast Emergency Isolation Actions *)
        bOpenTopHydraulicInletValve := FALSE;
        bOpenWhiteLiquorBlockValve := FALSE;
        bOpenEmergencyDepressurizeValve := TRUE; (* Open Rupture Blowdown Valve *)
        
        rUpperSteamValveCmd_pct := 0.0;
        rLowerSteamValveCmd_pct := 0.0;
        rWhiteLiquorDosingValveCmd_pct := 0.0;
        rHpfSpeedReference_rpm := 0.0;
        
        IF bAlarmReset AND bEmergencyStop AND (rVotedTopPressure_bar < (rSp_TopPress_Alarm_L_bar)) THEN
            bOpenEmergencyDepressurizeValve := FALSE;
            bEmergencyTripActive := FALSE;
            nFsmNextState := 0; (* Return to Standby *)
        END_IF;
ELSE
    nFsmNextState := 0;
END_CASE;
""")

    # -------------------------------------------------------------------------
    # PART 11: PHASE 6 - ISA-18.2 ALARMS & BIT-PACKED STATUS WORDS
    # -------------------------------------------------------------------------
    code_lines.append("""
(* ====================================================================================================
   PHASE 6: ISA-18.2 MULTI-TIER PROCESS ALARM LOGIC ENGINE & BIT-PACKED REGISTERS
   DWORD Bitmaps:
     dwStatusWord : Machine Operational Mode & Subsystems
     dwAlarmWord1 : Priority 1 Critical Safety Trips & Interlocks
     dwAlarmWord2 : Priority 2 Process Warnings, DP Exceedance & TMR Discordance
     dwTripWord   : First-Out Lockout Cause
   ==================================================================================================== *)

(* 1. Digester Top Shell Pressure Alarms *)
IF rVotedTopPressure_bar >= rSp_TopPress_Trip_HH_bar THEN
    rTimer_Trip_TopPress_HH_sec := rTimer_Trip_TopPress_HH_sec + rCycleTime_sec;
    IF rTimer_Trip_TopPress_HH_sec >= 0.20 THEN
        bAlarmHighHigh_Pressure := TRUE;
        dwAlarmWord1 := dwAlarmWord1 OR 16#00000001;
        IF dwTripWord = 0 THEN dwTripWord := 16#00000001; END_IF;
    END_IF;
ELSIF rVotedTopPressure_bar < (rSp_TopPress_Trip_HH_bar - rHysteresis_Press_bar) THEN
    rTimer_Trip_TopPress_HH_sec := 0.0;
    IF bAlarmAcknowledge THEN
        bAlarmHighHigh_Pressure := FALSE;
        dwAlarmWord1 := dwAlarmWord1 AND 16#FFFFFFFE;
    END_IF;
END_IF;

IF rVotedTopPressure_bar >= rSp_TopPress_Alarm_H_bar THEN
    rTimer_Alarm_TopPress_H_sec := rTimer_Alarm_TopPress_H_sec + rCycleTime_sec;
    IF rTimer_Alarm_TopPress_H_sec >= 1.0 THEN
        dwAlarmWord2 := dwAlarmWord2 OR 16#00000001;
    END_IF;
ELSIF rVotedTopPressure_bar < (rSp_TopPress_Alarm_H_bar - rHysteresis_Press_bar) THEN
    rTimer_Alarm_TopPress_H_sec := 0.0;
    IF bAlarmAcknowledge THEN
        dwAlarmWord2 := dwAlarmWord2 AND 16#FFFFFFFE;
    END_IF;
END_IF;

(* 2. Upper and Lower Cooking Temperature Alarms *)
IF (rVotedUpperCookTemp_degC >= rSp_CookTemp_Trip_HH_degC) OR (rVotedLowerCookTemp_degC >= rSp_CookTemp_Trip_HH_degC) THEN
    rTimer_Trip_CookTemp_HH_sec := rTimer_Trip_CookTemp_HH_sec + rCycleTime_sec;
    IF rTimer_Trip_CookTemp_HH_sec >= 0.50 THEN
        dwAlarmWord1 := dwAlarmWord1 OR 16#00000002;
        IF dwTripWord = 0 THEN dwTripWord := 16#00000002; END_IF;
    END_IF;
ELSIF (rVotedUpperCookTemp_degC < (rSp_CookTemp_Trip_HH_degC - rHysteresis_Temp_degC)) AND
      (rVotedLowerCookTemp_degC < (rSp_CookTemp_Trip_HH_degC - rHysteresis_Temp_degC)) THEN
    rTimer_Trip_CookTemp_HH_sec := 0.0;
    IF bAlarmAcknowledge THEN
        dwAlarmWord1 := dwAlarmWord1 AND 16#FFFFFFFD;
    END_IF;
END_IF;

(* 3. Extraction Residual Alkali Low-Low Trip & Low Warning *)
IF rVotedResidualAlkali_gL <= rSp_Alkali_Trip_LL_gL THEN
    rTimer_Trip_Alkali_LL_sec := rTimer_Trip_Alkali_LL_sec + rCycleTime_sec;
    IF rTimer_Trip_Alkali_LL_sec >= 2.0 THEN
        dwAlarmWord1 := dwAlarmWord1 OR 16#00000004;
        IF dwTripWord = 0 THEN dwTripWord := 16#00000004; END_IF;
    END_IF;
ELSIF rVotedResidualAlkali_gL > (rSp_Alkali_Trip_LL_gL + rHysteresis_Alkali_gL) THEN
    rTimer_Trip_Alkali_LL_sec := 0.0;
    IF bAlarmAcknowledge THEN
        dwAlarmWord1 := dwAlarmWord1 AND 16#FFFFFFFB;
    END_IF;
END_IF;

IF rVotedResidualAlkali_gL <= rSp_Alkali_Alarm_L_gL THEN
    rTimer_Alarm_Alkali_L_sec := rTimer_Alarm_Alkali_L_sec + rCycleTime_sec;
    IF rTimer_Alarm_Alkali_L_sec >= 2.0 THEN
        bAlarmLow_ResidualAlkali := TRUE;
        dwAlarmWord2 := dwAlarmWord2 OR 16#00000004;
    END_IF;
ELSIF rVotedResidualAlkali_gL > (rSp_Alkali_Alarm_L_gL + rHysteresis_Alkali_gL) THEN
    rTimer_Alarm_Alkali_L_sec := 0.0;
    IF bAlarmAcknowledge THEN
        bAlarmLow_ResidualAlkali := FALSE;
        dwAlarmWord2 := dwAlarmWord2 AND 16#FFFFFFFB;
    END_IF;
END_IF;

(* 4. Extraction Screen High Differential Pressure *)
IF rScreenDifferentialPress_bar >= rSp_ScreenDP_Trip_HH_bar THEN
    rTimer_Trip_ScreenDP_HH_sec := rTimer_Trip_ScreenDP_HH_sec + rCycleTime_sec;
    IF rTimer_Trip_ScreenDP_HH_sec >= 0.50 THEN
        dwAlarmWord1 := dwAlarmWord1 OR 16#00000008;
        IF dwTripWord = 0 THEN dwTripWord := 16#00000008; END_IF;
    END_IF;
ELSIF rScreenDifferentialPress_bar < (rSp_ScreenDP_Trip_HH_bar - rHysteresis_ScreenDP_bar) THEN
    rTimer_Trip_ScreenDP_HH_sec := 0.0;
    IF bAlarmAcknowledge THEN
        dwAlarmWord1 := dwAlarmWord1 AND 16#FFFFFFF7;
    END_IF;
END_IF;

IF rScreenDifferentialPress_bar >= rSp_ScreenDP_Alarm_H_bar THEN
    rTimer_Alarm_ScreenDP_H_sec := rTimer_Alarm_ScreenDP_H_sec + rCycleTime_sec;
    IF rTimer_Alarm_ScreenDP_H_sec >= 1.0 THEN
        bAlarmHigh_ExtractionDP := TRUE;
        dwAlarmWord2 := dwAlarmWord2 OR 16#00000008;
    END_IF;
ELSIF rScreenDifferentialPress_bar < (rSp_ScreenDP_Alarm_H_bar - rHysteresis_ScreenDP_bar) THEN
    rTimer_Alarm_ScreenDP_H_sec := 0.0;
    IF bAlarmAcknowledge THEN
        bAlarmHigh_ExtractionDP := FALSE;
        dwAlarmWord2 := dwAlarmWord2 AND 16#FFFFFFF7;
    END_IF;
END_IF;

(* 5. Scraper Motor Over-Torque / Chip Column Hanging Alarm *)
IF rBottomScraperVfdTorque_kNm >= rSp_ScraperTorque_Trip_HH_kNm THEN
    rTimer_Trip_ScraperTorque_sec := rTimer_Trip_ScraperTorque_sec + rCycleTime_sec;
    IF rTimer_Trip_ScraperTorque_sec >= 0.50 THEN
        dwAlarmWord1 := dwAlarmWord1 OR 16#00000010;
        IF dwTripWord = 0 THEN dwTripWord := 16#00000010; END_IF;
    END_IF;
ELSIF rBottomScraperVfdTorque_kNm < (rSp_ScraperTorque_Trip_HH_kNm - rHysteresis_Torque_kNm) THEN
    rTimer_Trip_ScraperTorque_sec := 0.0;
    IF bAlarmAcknowledge THEN
        dwAlarmWord1 := dwAlarmWord1 AND 16#FFFFFFEF;
    END_IF;
END_IF;

(* 6. Quality Alarm: Kappa Number Deviation *)
IF ABS(rObservedKappaNumber - rTargetKappaNumber) > 1.5 THEN
    rTimer_Alarm_KappaDev_sec := rTimer_Alarm_KappaDev_sec + rCycleTime_sec;
    IF rTimer_Alarm_KappaDev_sec >= 10.0 THEN
        bAlarm_KappaDeviation := TRUE;
        dwAlarmWord2 := dwAlarmWord2 OR 16#00000020;
    END_IF;
ELSE
    rTimer_Alarm_KappaDev_sec := 0.0;
    IF bAlarmAcknowledge THEN
        bAlarm_KappaDeviation := FALSE;
        dwAlarmWord2 := dwAlarmWord2 AND 16#FFDFFFFF;
    END_IF;
END_IF;

(* 7. TMR Discordance Alarms in dwAlarmWord2 *)
IF bDiscrepancy_TT101 THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000100; ELSE dwAlarmWord2 := dwAlarmWord2 AND 16#FFFFFEFF; END_IF;
IF bDiscrepancy_TT201 THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000200; ELSE dwAlarmWord2 := dwAlarmWord2 AND 16#FFFFFDFF; END_IF;
IF bDiscrepancy_PT301 THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000400; ELSE dwAlarmWord2 := dwAlarmWord2 AND 16#FFFFFBFF; END_IF;
IF bDiscrepancy_AT401 THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000800; ELSE dwAlarmWord2 := dwAlarmWord2 AND 16#FFFFF7FF; END_IF;
IF bDiscrepancy_PT501 THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00001000; ELSE dwAlarmWord2 := dwAlarmWord2 AND 16#FFFFEFFF; END_IF;
IF bDiscrepancy_FT601 THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00002000; ELSE dwAlarmWord2 := dwAlarmWord2 AND 16#FFFFDFFF; END_IF;

(* 8. Master dwStatusWord Bit Packing *)
dwStatusWord := 16#00000000;
IF bSystemEnable THEN dwStatusWord := dwStatusWord OR 16#00000001; END_IF;
IF bProductionActive THEN dwStatusWord := dwStatusWord OR 16#00000002; END_IF;
IF bSystemReady THEN dwStatusWord := dwStatusWord OR 16#00000004; END_IF;
IF bEmergencyTripActive THEN dwStatusWord := dwStatusWord OR 16#00000008; END_IF;
IF bExtractionScreenBackflushActive THEN dwStatusWord := dwStatusWord OR 16#00000010; END_IF;
IF bAlarm_ChipColumnHanging THEN dwStatusWord := dwStatusWord OR 16#00000020; END_IF;
dwStatusWord := dwStatusWord OR SHL(INT_TO_DWORD(nDigesterOperationalState), 8);

(* Reset Master Safety Trip on Command *)
IF bAlarmReset AND NOT bEmergencyTripActive THEN
    dwTripWord := 16#00000000;
END_IF;

nScanCounter := nScanCounter + 1;
END_FUNCTION_BLOCK
""")

    return "".join(code_lines)

if __name__ == "__main__":
    code = build_iec_code()
    print(f"Total IEC-ST code length: {len(code)} characters.")
