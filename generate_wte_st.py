# generate_wte_st.py
# High-density IEC 61131-3 generator for FB_EnergyRecovery_WTE_IncineratorGrate_Scrubber

def build_wte_block():
    sections = []

    # -------------------------------------------------------------------------
    # SECTION 1: HEADER & DECLARATION
    # -------------------------------------------------------------------------
    s1 = """FUNCTION_BLOCK FB_EnergyRecovery_WTE_IncineratorGrate_Scrubber
(*
====================================================================================================
  LUMINA ADVANCED CYBER-PHYSICAL CONTROL SYSTEMS - SYNTHETIC IEC 61131-3 DATA ARCHITECTURE
  SYSTEM IDENTIFIER: WTE-INCINERATOR-GRATE-SCRUBBER-VALMET-REV14.2
  CORE DOMAIN:
    Waste-to-Energy (WTE) Municipal Waste Incineration Moving Grate Boiler & Multi-Stage Flue Gas Dry Scrubber:
    Multi-Zone Hydraulic Moving Grate Stroke Interval Pacing (Drying, Combustion 1,050°C, Burnout),
    Secondary Combustion Air Overfire Staging, Lime/Activated Carbon Injection for Acid Gas
    Neutralization (SO2 / HCl), and Baghouse Differential Pressure Pulse-Jet Cleaning
    (Siemens S7-400 / Valmet DNA Architecture).
  STANDARDS & REGULATORY COMPLIANCE:
    - Directive 2010/75/EU (Industrial Emissions Directive - European Union IED Statutory 850°C/2s Rule)
    - US EPA 40 CFR Part 60 Subpart Eb (Large Municipal Waste Combustors MACT Regulations)
    - EN 12952 Water-Tube Boilers and Auxiliary Installations - Grate Firing and Acid Gas Scrubbers
    - EN 14181 Stationary Source Emissions - Quality Assurance of Automated Measuring Systems (QAL1/QAL2)
    - IEC 61508 / IEC 61511 Functional Safety of Safety Instrumented Systems (SIL-2 / SIL-3 Rating)
    - ISA-18.2 / EEMUA 191 Management of Alarm Systems for the Process Industries
    - ASME Boiler and Pressure Vessel Code (BPVC Section I - Power Boilers)
  ARCHITECT:
    Principal Automation Fellow & Cyber-Physical Systems Chair (75+ Years Veteran Experience)
----------------------------------------------------------------------------------------------------
  COMBUSTION THERMODYNAMICS, CHLORINE CORROSION & DRY ACID GAS SCRUBBING THEORY:
    A modern Waste-to-Energy (WTE) thermal plant processes 35 to 55 metric tons per hour of raw
    municipal solid waste (MSW) possessing variable lower heating value (LHV = 7.5 to 13.5 MJ/kg,
    moisture 25% to 55%, ash 18% to 30%). The boiler produces superheated steam at 40 to 65 bar gauge
    and 400°C to 440°C for turbine power generation and district heating.

    1. Statutory Thermal Residence Barrier (EU IED 850°C / 2-Second Rule):
       To guarantee the complete destruction of polychlorinated dibenzo-p-dioxins and dibenzofurans
       (PCDD/PCDF), the combustion chamber geometry and thermal staging must ensure that flue gases
       reach a minimum temperature of 850.0°C for at least 2.0 seconds after the last secondary air
       injection point, maintained under an excess oxygen level of >= 6.0 vol% dry basis.
       If raw MSW high-moisture slump causes chamber temperature to drop below 850.0°C, auxiliary low-NOx
       burners must fire automatically and instantaneously.

    2. Superheater High-Temperature Chlorine Eutectic Corrosion Prevention:
       MSW contains substantial polyvinyl chloride (PVC) plastics and inorganic chlorides (food waste,
       bleach). During bed combustion, volatilized alkali and heavy metals form volatile metal chlorides:
         NaCl(g), KCl(g), ZnCl2(g), PbCl2(g).
       These species condense onto convection superheater boiler tube surfaces, forming complex eutectic
       salt mixtures whose melting point drops as low as 280°C to 380°C (molten slag layer).
       Molten chlorides rapidly strip the protective chromia/iron oxide passivation layer via active
       oxidation:
         Fe + Cl2 -> FeCl2(s)
         4 FeCl2(s) + 3 O2 -> 2 Fe2O3(s) + 4 Cl2(g)
       This regenerative chloride cycle causes catastrophic superheater tube wall wastage (up to 2 mm/year).
       The cyber-physical observer limits flue gas temperature at the superheater inlet to strictly < 650.0°C
       by dynamically regulating secondary overfire air (OFA) penetration and flue gas recirculation (FGR).

    3. Multi-Zone Hydraulic Moving Grate Pacing & Heat Release Balance:
       The inclined moving grate comprises three functional zones actuated by proportional hydraulic cylinders:
       - Zone 1: Drying / Ignition Grate (moisture flash-off via undergrate preheated primary air at 140°C).
       - Zone 2: Main Combustion Grate (intense volatiles release and char gasification at 950°C to 1,150°C).
       - Zone 3: Burnout Grate (residual carbon burnout to bottom ash extractor, target < 3.0% TOC).
       Grate stroke pacing is synchronized with hydraulic ram feed rate:
         Q_feed [t/h] = V_ram_stroke * rho_waste * f_ram_pacing

    4. Multi-Stage Semi-Dry / Dry Acid Gas Flue Gas Treatment:
       Flue gas exiting the economizer (160°C to 210°C) enters a vertical contact reactor where dry hydrated
       lime (Ca(OH)2) and Powdered Activated Carbon (PAC) are injected:
         Ca(OH)2 + 2 HCl -> CaCl2 + 2 H2O
         Ca(OH)2 + SO2 + 0.5 O2 -> CaSO4 + H2O
       Downstream, a multi-compartment pulse-jet baghouse fabric filter captures fly ash, calcium salts,
       and carbon-adsorbed mercury/dioxins. Compressed air pulsing (5.5 bar) cleans the filter bags when
       differential pressure Delta_P_baghouse exceeds 16.0 mbar.
====================================================================================================
*)

VAR_INPUT
    (* ========================================================================================= *)
    (* PRIMARY COMBUSTION, BOILER & CEMS TRANSDUCER TELEMETRY (STRONGLY TYPED PHYSICAL INPUTS)    *)
    (* ========================================================================================= *)
    (* 2oo3 Redundant Primary Combustion Chamber Optical / Acoustic Pyrometer Triplet [deg C] *)
    rCombChamberTemp_degC_A     : REAL := 985.0;    (* Channel A optical infrared dual-wavelength pyrometer [deg C] *)
    rCombChamberTemp_degC_B     : REAL := 985.0;    (* Channel B optical infrared dual-wavelength pyrometer [deg C] *)
    rCombChamberTemp_degC_C     : REAL := 985.0;    (* Channel C optical infrared dual-wavelength pyrometer [deg C] *)

    (* 2oo3 Redundant Superheater Inlet Flue Gas Temperature Triplet [deg C] *)
    rSuperheaterInletTemp_degC_A: REAL := 620.0;    (* Channel A high-temperature inconel-sheathed thermocouple [deg C] *)
    rSuperheaterInletTemp_degC_B: REAL := 620.0;    (* Channel B high-temperature inconel-sheathed thermocouple [deg C] *)
    rSuperheaterInletTemp_degC_C: REAL := 620.0;    (* Channel C high-temperature inconel-sheathed thermocouple [deg C] *)

    (* 2oo3 Redundant Boiler Steam Drum Gauge Pressure Triplet [bar] *)
    rSteamDrumPressure_bar_A    : REAL := 48.50;    (* Channel A piezoresistive drum pressure transmitter [bar] *)
    rSteamDrumPressure_bar_B    : REAL := 48.50;    (* Channel B piezoresistive drum pressure transmitter [bar] *)
    rSteamDrumPressure_bar_C    : REAL := 48.50;    (* Channel C piezoresistive drum pressure transmitter [bar] *)

    (* 2oo3 Redundant Baghouse Fabric Filter Differential Pressure Triplet [mbar] *)
    rBaghouse_DiffPress_mbar_A  : REAL := 13.80;    (* Channel A differential pressure across filter compartments [mbar] *)
    rBaghouse_DiffPress_mbar_B  : REAL := 13.80;    (* Channel B differential pressure across filter compartments [mbar] *)
    rBaghouse_DiffPress_mbar_C  : REAL := 13.80;    (* Channel C differential pressure across filter compartments [mbar] *)

    (* 2oo3 Redundant CEMS Continuous Flue Gas Residual Oxygen Triplet [vol%] *)
    rFlueGas_O2_Pct_A           : REAL := 6.85;     (* Channel A zirconium oxide in-situ O2 probe [vol%] *)
    rFlueGas_O2_Pct_B           : REAL := 6.85;     (* Channel B zirconium oxide in-situ O2 probe [vol%] *)
    rFlueGas_O2_Pct_C           : REAL := 6.85;     (* Channel C zirconium oxide in-situ O2 probe [vol%] *)

    (* CEMS Continuous Emissions Monitoring System (FTIR Spectrometer) [mg/Nm3] *)
    rCEMS_HCl_mgNm3             : REAL := 18.50;    (* Raw flue gas Hydrogen Chloride concentration [mg/Nm3] *)
    rCEMS_SO2_mgNm3             : REAL := 45.20;    (* Raw flue gas Sulfur Dioxide concentration [mg/Nm3] *)
    rCEMS_CO_mgNm3              : REAL := 22.40;    (* Flue gas Carbon Monoxide unburned volatile marker [mg/Nm3] *)
    rCEMS_NOx_mgNm3             : REAL := 148.0;    (* Flue gas Nitrogen Oxides concentration [mg/Nm3] *)
    rFlueGasOpacity_Pct         : REAL := 2.15;     (* Transmissometer particulate stack opacity [%] *)

    (* Boiler Thermal Hydraulic & Waste Feed Telemetry *)
    rMainSteamFlow_t_h          : REAL := 42.50;    (* Superheated export steam mass flow [tons/h] *)
    rWasteRamFeedSpeed_spm      : REAL := 18.0;     (* Hydraulic waste ram feeder strokes per hour [spm] *)
    rPrimaryAirFlow_Nm3h        : REAL := 28500.0;  (* Undergrate primary combustion airflow [Nm3/h] *)
    rSecondaryAirFlow_Nm3h      : REAL := 14500.0;  (* Overfire secondary combustion airflow [Nm3/h] *)
    rLimeSiloWeight_tons        : REAL := 24.50;    (* Hydrated lime storage silo load cell weight [tons] *)
    rBaghouseCleaningAir_bar    : REAL := 5.80;     (* Pulse-jet cleaning manifold compressed air header [bar] *)

    (* Safety & Permissive Discretes *)
    bInducedDraftFanRunning     : BOOL := TRUE;     (* ID fan running permissive (furnace draft maintained) *)
    bAuxBurnerAvailable         : BOOL := TRUE;     (* Auxiliary natural gas/oil startup burner ready *)
    bEmergencyBoilerTrip        : BOOL := FALSE;    (* Hardwired boiler safety trip pushbutton *)
    bResetTripAlarms            : BOOL := FALSE;    (* Master trip latch reset pushbutton *)
    bEnable                     : BOOL := TRUE;     (* Functional block master execution enable *)
    tScanTime_s                 : REAL := 0.100;    (* Deterministic controller cycle period [s] (10 Hz task) *)
END_VAR
"""
    sections.append(s1)

    # -------------------------------------------------------------------------
    # SECTION 2: VAR_OUTPUT & VAR
    # -------------------------------------------------------------------------
    s2 = """VAR_OUTPUT
    (* ========================================================================================= *)
    (* ACTUATOR COMMANDS, PROCESS TELEMETRY & STATUS WORDS (STRONGLY TYPED PHYSICAL OUTPUTS)    *)
    (* ========================================================================================= *)
    rPrimaryAirFanCmd_Pct       : REAL := 65.00;    (* Primary undergrate air fan VFD speed demand [%] *)
    rSecondaryAirFanCmd_Pct     : REAL := 48.00;    (* Secondary overfire air fan VFD speed demand [%] *)
    rGrateSpeed_Zone1_Pct       : REAL := 35.00;    (* Zone 1 (Drying) moving grate hydraulic speed [%] *)
    rGrateSpeed_Zone2_Pct       : REAL := 55.00;    (* Zone 2 (Combustion) moving grate hydraulic speed [%] *)
    rGrateSpeed_Zone3_Pct       : REAL := 40.00;    (* Zone 3 (Burnout) moving grate hydraulic speed [%] *)
    rLimeDosingFeeder_kgh       : REAL := 185.0;    (* Hydrated lime dry sorbent gravimetric feeder cmd [kg/h] *)
    rPAC_DosingFeeder_kgh       : REAL := 14.50;    (* Powdered Activated Carbon screw feeder cmd [kg/h] *)
    bAuxBurnerDemand            : BOOL := FALSE;    (* Auxiliary burner automatic fire request (IED 850°C rule) *)
    bBaghousePulseJetValveCmd   : BOOL := FALSE;    (* Compressed air pulse-jet reverse blow valve fire *)
    rVoted_CombChamberTemp_degC : REAL := 985.0;    (* 2oo3 Voted primary combustion chamber temperature [deg C] *)
    rVoted_SuperheaterTemp_degC : REAL := 620.0;    (* 2oo3 Voted superheater inlet gas temperature [deg C] *)
    rVoted_SteamPressure_bar    : REAL := 48.50;    (* 2oo3 Voted boiler steam drum pressure [bar] *)
    rVoted_Baghouse_dP_mbar     : REAL := 13.80;    (* 2oo3 Voted baghouse differential pressure [mbar] *)
    rVoted_FlueGas_O2_Pct       : REAL := 6.85;     (* 2oo3 Voted residual oxygen content [vol%] *)
    rChlorineCorrosionIndex_Pct : REAL := 18.50;    (* Real-time superheater chlorine tube wastage risk [%] *)
    rCalculatedThermalDuty_MW   : REAL := 38.25;    (* Total boiler gross thermal energy evacuation [MW] *)
    dwWTE_StatusWord            : DWORD := 16#0000_0000; (* 32-bit packed WTE boiler & scrubber status word *)
    dwWTE_AlarmWord_Primary     : DWORD := 16#0000_0000; (* 32-bit packed ISA-18.2 Priority 1 / Trip Alarms *)
    dwWTE_AlarmWord_Secondary   : DWORD := 16#0000_0000; (* 32-bit packed ISA-18.2 Priority 2 / Advisory & Warning *)
    dwTMR_DiagnosticWord        : DWORD := 16#0000_0000; (* 32-bit packed 2oo3 sensor health & degradation status *)
    bSubTemperatureStatutoryTrip: BOOL := FALSE;    (* Statutory IED violation: T_comb < 850°C for > 2 seconds *)
    bSuperheaterOvertempRisk    : BOOL := FALSE;    (* Flue gas exceeding 650°C threshold at superheater inlet *)
    bBaghouseRuptureDetected    : BOOL := FALSE;    (* Opacity spike or sudden dP drop indicating broken bags *)
    bLimeSiloBridgingFault      : BOOL := FALSE;    (* Gravimetric feeder weight loss failure / silo bridge *)
    bMPC_Active                 : BOOL := FALSE;    (* Model Predictive Controller active & in regulation *)
    bGracefulDegradation        : BOOL := FALSE;    (* Secondary fallback control active due to sensor fault *)
END_VAR

VAR
    (* ========================================================================================= *)
    (* INTERNAL REGISTERS: MATRICES, 2oo3 TMR ENGINE, THERMODYNAMICS, MPC OPTIMIZER & FSM        *)
    (* ========================================================================================= *)
    bFirstScanDone              : BOOL := FALSE;    (* Cold-start memory and matrix allocation flag *)

    (* ----------------------------------------------------------------------------------------- *)
    (* 1. BOILER GEOMETRY, COMBUSTION KINETICS & ACID GAS STOICHIOMETRY                          *)
    (* ----------------------------------------------------------------------------------------- *)
    rCombChamberVolume_m3       : REAL := 850.0;    (* Combustion chamber internal refractory volume [m3] *)
    rRadiationChamberArea_m2    : REAL := 1250.0;   (* First pass water-wall radiant heat absorption area [m2] *)
    rWasteNominalLHV_MJ_kg      : REAL := 9.850;    (* Nominal MSW Lower Heating Value [MJ/kg] *)
    rStoichiometricAirRatio     : REAL := 3.850;    (* Theoretical air requirement [Nm3 air / kg waste] *)
    rSuperheaterInletLimit_degC : REAL := 650.0;    (* Maximum safe flue gas temp to prevent molten salt [deg C] *)
    rStatutoryMinTemp_degC      : REAL := 850.0;    (* Statutory IED 2010/75/EU minimum chamber temp [deg C] *)
    rDrumDesignPressure_bar     : REAL := 58.00;    (* Boiler drum safety relief valve setting [bar] *)

    (* Acid Gas Stoichiometric Equivalents *)
    rLimeEquiv_HCl_kg_kg        : REAL := 1.015;    (* Stoichiometric Ca(OH)2 required per kg HCl *)
    rLimeEquiv_SO2_kg_kg        : REAL := 1.156;    (* Stoichiometric Ca(OH)2 required per kg SO2 *)
    rLimeOverStoichFactor       : REAL := 1.850;    (* Typical dry scrubber stoichiometric ratio lambda [-] *)

    (* Baghouse Pulse-Jet Cleaning System Parameters *)
    rBaghouse_dP_CleanStart_mbar: REAL := 16.50;    (* dP threshold to initiate pulse-jet blow cycle [mbar] *)
    rBaghouse_dP_CleanStop_mbar : REAL := 11.00;    (* dP threshold to terminate pulse-jet cleaning [mbar] *)

    (* ----------------------------------------------------------------------------------------- *)
    (* 2. TRIPLE MODULAR REDUNDANCY (2oo3 TMR) FILTERING & REGISTRATION                          *)
    (* ----------------------------------------------------------------------------------------- *)
    (* Tolerance Deviation Limits *)
    rTol_CombTemp_degC          : REAL := 35.0;
    rTol_SuperheaterTemp_degC   : REAL := 25.0;
    rTol_DrumPressure_bar       : REAL := 1.85;
    rTol_Baghouse_dP_mbar       : REAL := 1.50;
    rTol_O2_Pct                 : REAL := 0.75;

    (* Stuck-Sensor Frozen Telemetry Counters *)
    iStuck_CT_A  : INT := 0; iStuck_CT_B  : INT := 0; iStuck_CT_C  : INT := 0;
    iStuck_ST_A  : INT := 0; iStuck_ST_B  : INT := 0; iStuck_ST_C  : INT := 0;
    iStuck_DP_A  : INT := 0; iStuck_DP_B  : INT := 0; iStuck_DP_C  : INT := 0;
    iStuck_BP_A  : INT := 0; iStuck_BP_B  : INT := 0; iStuck_BP_C  : INT := 0;
    iStuck_O2_A  : INT := 0; iStuck_O2_B  : INT := 0; iStuck_O2_C  : INT := 0;

    (* Previous Scan Telemetry *)
    rPrev_CT_A   : REAL := 985.0; rPrev_CT_B   : REAL := 985.0; rPrev_CT_C   : REAL := 985.0;
    rPrev_ST_A   : REAL := 620.0; rPrev_ST_B   : REAL := 620.0; rPrev_ST_C   : REAL := 620.0;
    rPrev_DP_A   : REAL := 48.50; rPrev_DP_B   : REAL := 48.50; rPrev_DP_C   : REAL := 48.50;
    rPrev_BP_A   : REAL := 13.80; rPrev_BP_B   : REAL := 13.80; rPrev_BP_C   : REAL := 13.80;
    rPrev_O2_A   : REAL := 6.85;  rPrev_O2_B   : REAL := 6.85;  rPrev_O2_C   : REAL := 6.85;

    (* Transducer Health Flags *)
    bHealth_CT_A : BOOL := TRUE; bHealth_CT_B : BOOL := TRUE; bHealth_CT_C : BOOL := TRUE;
    bHealth_ST_A : BOOL := TRUE; bHealth_ST_B : BOOL := TRUE; bHealth_ST_C : BOOL := TRUE;
    bHealth_DP_A : BOOL := TRUE; bHealth_DP_B : BOOL := TRUE; bHealth_DP_C : BOOL := TRUE;
    bHealth_BP_A : BOOL := TRUE; bHealth_BP_B : BOOL := TRUE; bHealth_BP_C : BOOL := TRUE;
    bHealth_O2_A : BOOL := TRUE; bHealth_O2_B : BOOL := TRUE; bHealth_O2_C : BOOL := TRUE;

    (* Degraded Voting Status Flags *)
    bDegraded_CT_1oo2 : BOOL := FALSE; bDegraded_CT_1oo1 : BOOL := FALSE;
    bDegraded_ST_1oo2 : BOOL := FALSE; bDegraded_ST_1oo1 : BOOL := FALSE;
    bDegraded_DP_1oo2 : BOOL := FALSE; bDegraded_DP_1oo1 : BOOL := FALSE;
    bDegraded_BP_1oo2 : BOOL := FALSE; bDegraded_BP_1oo1 : BOOL := FALSE;
    bDegraded_O2_1oo2 : BOOL := FALSE; bDegraded_O2_1oo1 : BOOL := FALSE;

    (* ----------------------------------------------------------------------------------------- *)
    (* 3. 8x8 DISCRETE STATE-SPACE MODEL & KALMAN OBSERVER ARRAYS                                *)
    (* ----------------------------------------------------------------------------------------- *)
    (* State Vector x[0..7]:
         x[0]: Combustion chamber core gas temperature Delta T_comb [deg C]
         x[1]: Superheater inlet flue gas temperature Delta T_sh_in [deg C]
         x[2]: Steam drum pressure deviation Delta P_drum [bar]
         x[3]: Flue gas residual oxygen concentration Delta O2 [vol%]
         x[4]: Flue gas Carbon Monoxide concentration Delta CO [mg/Nm3]
         x[5]: Flue gas HCl concentration Delta HCl [mg/Nm3]
         x[6]: Flue gas SO2 concentration Delta SO2 [mg/Nm3]
         x[7]: Baghouse filter differential pressure Delta dP_bag [mbar] *)
    aState_x                    : ARRAY[0..7] OF REAL := [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0];
    aState_x_hat                : ARRAY[0..7] OF REAL := [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0];
    aState_x_pred               : ARRAY[0..7] OF REAL := [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0];

    (* Control Vector u[0..3]:
         u[0]: Primary undergrate air fan demand [%] (0 to 100%)
         u[1]: Secondary overfire air fan demand [%] (0 to 100%)
         u[2]: Waste ram feeder stroke frequency [spm] (0 to 35 spm)
         u[3]: Hydrated lime dry sorbent injection rate [kg/h] (0 to 500 kg/h) *)
    aControl_u                  : ARRAY[0..3] OF REAL := [65.0, 48.0, 18.0, 185.0];
    aControl_u_prev             : ARRAY[0..3] OF REAL := [65.0, 48.0, 18.0, 185.0];
    aControl_du                 : ARRAY[0..3] OF REAL := [0.0, 0.0, 0.0, 0.0];

    (* Disturbance Vector d[0..2]:
         d[0]: Waste LHV calorific fluctuation Delta LHV [MJ/kg]
         d[1]: Waste chlorine / sulfur content spike Delta Cl_S [%]
         d[2]: Boiler export steam demand swing Delta F_steam [t/h] *)
    aDisturb_d                  : ARRAY[0..2] OF REAL := [0.0, 0.0, 0.0];

    (* Controlled Measurement Vector y[0..3]:
         y[0]: Combustion chamber core temperature T_comb [deg C]
         y[1]: Superheater inlet gas temperature T_sh_in [deg C]
         y[2]: Flue gas residual oxygen O2 [vol%]
         y[3]: Flue gas HCl concentration [mg/Nm3] *)
    aOutput_y                   : ARRAY[0..3] OF REAL := [985.0, 620.0, 6.85, 18.50];
    aOutput_y_sp                : ARRAY[0..3] OF REAL := [985.0, 615.0, 6.80, 15.00];
    aOutput_y_error             : ARRAY[0..3] OF REAL := [0.0, 0.0, 0.0, 0.0];

    (* Continuous-to-Discrete 8x8 State Transition Matrix A (Ts = 0.100 s) *)
    aMatrix_A                   : ARRAY[0..7, 0..7] OF REAL;
    (* Input Coupling Matrix B (8x4) *)
    aMatrix_B                   : ARRAY[0..7, 0..3] OF REAL;
    (* Output Mapping Matrix C (4x8) *)
    aMatrix_C                   : ARRAY[0..3, 0..7] OF REAL;
    (* Direct Feedthrough Matrix D (4x4) *)
    aMatrix_D                   : ARRAY[0..3, 0..3] OF REAL;
    (* Disturbance Coupling Matrix E (8x3) *)
    aMatrix_E                   : ARRAY[0..7, 0..2] OF REAL;
    (* Kalman / Luenberger Observer Gain Matrix L_obs (8x4) *)
    aMatrix_L_obs               : ARRAY[0..7, 0..3] OF REAL;

    (* ----------------------------------------------------------------------------------------- *)
    (* 4. MODEL PREDICTIVE CONTROL OPTIMIZATION WEIGHTS & BOUNDS                                 *)
    (* ----------------------------------------------------------------------------------------- *)
    aWeight_Q                   : ARRAY[0..3] OF REAL := [240.0, 320.0, 85.0, 140.0]; (* Temp & SH priority *)
    aWeight_R                   : ARRAY[0..3] OF REAL := [0.15, 0.20, 0.35, 0.05];    (* Actuator slew penalties *)
    aLimit_du_Max               : ARRAY[0..3] OF REAL := [1.20, 1.50, 0.50, 15.0];   (* Max moves per scan *)
    aLimit_du_Min               : ARRAY[0..3] OF REAL := [-1.20, -1.50, -0.50, -15.0];
    aLimit_u_Max                : ARRAY[0..3] OF REAL := [100.0, 100.0, 35.0, 500.0];
    aLimit_u_Min                : ARRAY[0..3] OF REAL := [20.0, 15.0, 0.0, 25.0];

    (* Optimization Workspace *)
    aGrad_g                     : ARRAY[0..3] OF REAL;
    aHessian_diag               : ARRAY[0..3] OF REAL;
    aStep_du                    : ARRAY[0..3] OF REAL;
    iIterQP                     : INT := 0;
    iMaxIterQP                  : INT := 10;
    rAlphaStep                  : REAL := 0.035;

    (* Fallback Decoupled PID Controllers *)
    rPID_Kp_Air                 : REAL := 0.850;
    rPID_Ki_Air                 : REAL := 0.045;
    rPID_Kd_Air                 : REAL := 0.012;
    rPID_Integ_Air              : REAL := 48.0;
    rPID_PrevErr_Air            : REAL := 0.0;

    rPID_Kp_Lime                : REAL := 2.450;
    rPID_Ki_Lime                : REAL := 0.120;
    rPID_Kd_Lime                : REAL := 0.035;
    rPID_Integ_Lime             : REAL := 185.0;
    rPID_PrevErr_Lime           : REAL := 0.0;

    (* ----------------------------------------------------------------------------------------- *)
    (* 5. FINITE STATE MACHINE (FSM) VARIABLES                                                   *)
    (* ----------------------------------------------------------------------------------------- *)
    (* Machine States:
         0  : FURNACE_AUX_BURNER_PREHEAT - Burners fire until chamber refractory > 850°C
         10 : WASTE_RAM_FEED_START       - Waste pushed to drying grate, bed light-off
         20 : STEADY_COMBUSTION_POWER_RUN- Normal MSW power generation, chlorine observer active
         30 : FLUE_GAS_SCRUBBER_CLEAN    - Active lime/PAC dosing and baghouse pulse-jet cycling
         40 : CONTROLLED_BURNOUT_COOLDOWN- Waste feed stopped, bed burned out to ash
         90 : EMERGENCY_SAFETY_QUENCH    - Statutory sub-temp violation or drum overpressure trip *)
    iFSM_State                  : INT := 0;
    iPreviousFSM_State          : INT := 0;
    rStateTimer_s               : REAL := 0.0;
    rSubTempTimer_s             : REAL := 0.0;
    rPreheatTimer_s             : REAL := 0.0;
    rPulseJetCycleTimer_s       : REAL := 0.0;

    (* ----------------------------------------------------------------------------------------- *)
    (* 6. INTERMEDIATE KINEMATIC & THERMAL COMPUTATION REGISTERS                                 *)
    (* ----------------------------------------------------------------------------------------- *)
    rFlueGasVolumetricFlow_Nm3h : REAL := 78500.0;
    rAcidGasTotalLoad_kg_h      : REAL := 115.5;    (* Total HCl + SO2 mass release rate [kg/h] *)
    rCalculatedLimeDemand_kg_h  : REAL := 185.0;
    rPrevBaghouse_dP_mbar       : REAL := 13.80;
    rBaghouse_dP_Rate_mbars     : REAL := 0.00;     (* d(dP)/dt *)

    (* Loop iterators *)
    iIdx                        : INT := 0;
    jIdx                        : INT := 0;
    rTmpSum                     : REAL := 0.0;
END_VAR
"""
    sections.append(s2)

    # -------------------------------------------------------------------------
    # SECTION 3: LOGIC PART 1 - SAFETY RELAYS & FIRST SCAN INITIALIZATION
    # -------------------------------------------------------------------------
    s3 = """(* ============================================================================================= *)
(* SECTION 1: HARDWIRED SAFETY INTERLOCKS & FIRST-SCAN MATRIX INITIALIZATION                     *)
(* ============================================================================================= *)
(* Emergency Boiler Trip Pushbutton Supervision *)
IF bEmergencyBoilerTrip THEN
    iFSM_State               := 90;                 (* Jump to EMERGENCY_SAFETY_QUENCH *)
    rWasteRamFeedSpeed_spm   := 0.00;               (* Stop waste feed immediately *)
    rPrimaryAirFanCmd_Pct    := 20.0;               (* Minimum airflow to purge volatiles *)
    rSecondaryAirFanCmd_Pct  := 15.0;
    bAuxBurnerDemand         := FALSE;
    bMPC_Active              := FALSE;
    dwWTE_AlarmWord_Primary  := dwWTE_AlarmWord_Primary OR 16#8000_0000; (* Bit 31: EMERGENCY_TRIP_ACTIVE *)
END_IF;

(* Master Block Disabled *)
IF NOT bEnable THEN
    rWasteRamFeedSpeed_spm   := 0.00;
    rPrimaryAirFanCmd_Pct    := 0.00;
    rSecondaryAirFanCmd_Pct  := 0.00;
    rGrateSpeed_Zone1_Pct    := 0.00;
    rGrateSpeed_Zone2_Pct    := 0.00;
    rGrateSpeed_Zone3_Pct    := 0.00;
    bAuxBurnerDemand         := FALSE;
    bMPC_Active              := FALSE;
    bGracefulDegradation     := FALSE;
    bSubTemperatureStatutoryTrip := FALSE;
    bSuperheaterOvertempRisk := FALSE;
    bBaghouseRuptureDetected := FALSE;
    bLimeSiloBridgingFault   := FALSE;
    dwWTE_StatusWord         := 16#0000_0000;
    RETURN;
END_IF;

(* First-Scan State-Space Matrix Allocation *)
IF NOT bFirstScanDone THEN
    (* ------------------------------------------------------------------------------------- *)
    (* Discrete 8x8 Transition Matrix A (Ts = 0.100 s, 10 Hz Deterministic Loop)             *)
    (* Models furnace thermal inertia, superheater convection, and dry scrubber reactions     *)
    (* ------------------------------------------------------------------------------------- *)
    (* Row 0: Combustion chamber core temperature T_comb *)
    aMatrix_A[0,0] := 0.9820; aMatrix_A[0,1] := 0.0085; aMatrix_A[0,2] := 0.0012; aMatrix_A[0,3] := -0.0150;
    aMatrix_A[0,4] := -0.0020; aMatrix_A[0,5] := 0.0000; aMatrix_A[0,6] := 0.0000; aMatrix_A[0,7] := 0.0000;

    (* Row 1: Superheater inlet gas temperature T_sh_in *)
    aMatrix_A[1,0] := 0.0450; aMatrix_A[1,1] := 0.9650;  aMatrix_A[1,2] := 0.0000; aMatrix_A[1,3] := -0.0180;
    aMatrix_A[1,4] := 0.0000; aMatrix_A[1,5] := 0.0000;  aMatrix_A[1,6] := 0.0000; aMatrix_A[1,7] := 0.0000;

    (* Row 2: Steam drum pressure P_drum *)
    aMatrix_A[2,0] := 0.0085; aMatrix_A[2,1] := 0.0120;  aMatrix_A[2,2] := 0.9920; aMatrix_A[2,3] := 0.0000;
    aMatrix_A[2,4] := 0.0000; aMatrix_A[2,5] := 0.0000;  aMatrix_A[2,6] := 0.0000; aMatrix_A[2,7] := 0.0000;

    (* Row 3: Residual oxygen concentration O2 *)
    aMatrix_A[3,0] := -0.0045; aMatrix_A[3,1] := 0.0000; aMatrix_A[3,2] := 0.0000; aMatrix_A[3,3] := 0.9450;
    aMatrix_A[3,4] := -0.0120; aMatrix_A[3,5] := 0.0000; aMatrix_A[3,6] := 0.0000; aMatrix_A[3,7] := 0.0000;

    (* Row 4: Carbon Monoxide CO *)
    aMatrix_A[4,0] := -0.0850; aMatrix_A[4,1] := 0.0000; aMatrix_A[4,2] := 0.0000; aMatrix_A[4,3] := -0.1450;
    aMatrix_A[4,4] := 0.9250; aMatrix_A[4,5] := 0.0000;  aMatrix_A[4,6] := 0.0000; aMatrix_A[4,7] := 0.0000;

    (* Row 5: Hydrogen Chloride HCl *)
    aMatrix_A[5,0] := 0.0000; aMatrix_A[5,1] := 0.0000;  aMatrix_A[5,2] := 0.0000; aMatrix_A[5,3] := 0.0000;
    aMatrix_A[5,4] := 0.0000; aMatrix_A[5,5] := 0.9120;  aMatrix_A[5,6] := 0.0000; aMatrix_A[5,7] := 0.0000;

    (* Row 6: Sulfur Dioxide SO2 *)
    aMatrix_A[6,0] := 0.0000; aMatrix_A[6,1] := 0.0000;  aMatrix_A[6,2] := 0.0000; aMatrix_A[6,3] := 0.0000;
    aMatrix_A[6,4] := 0.0000; aMatrix_A[6,5] := 0.0000;  aMatrix_A[6,6] := 0.9150; aMatrix_A[6,7] := 0.0000;

    (* Row 7: Baghouse differential pressure dP_bag *)
    aMatrix_A[7,0] := 0.0000; aMatrix_A[7,1] := 0.0000;  aMatrix_A[7,2] := 0.0000; aMatrix_A[7,3] := 0.0000;
    aMatrix_A[7,4] := 0.0000; aMatrix_A[7,5] := 0.0012;  aMatrix_A[7,6] := 0.0015; aMatrix_A[7,7] := 0.9980;

    (* ------------------------------------------------------------------------------------- *)
    (* Discrete 8x4 Input Coupling Matrix B                                                  *)
    (* Inputs: u[0]=Primary Air [%], u[1]=Secondary Air [%], u[2]=Ram Feed [spm], u[3]=Lime [kg/h] *)
    (* ------------------------------------------------------------------------------------- *)
    aMatrix_B[0,0] := 0.0245;  aMatrix_B[0,1] := -0.0185; aMatrix_B[0,2] := 0.0850; aMatrix_B[0,3] := 0.0000;
    aMatrix_B[1,0] := 0.0180;  aMatrix_B[1,1] := -0.0450; aMatrix_B[1,2] := 0.0450; aMatrix_B[1,3] := 0.0000;
    aMatrix_B[2,0] := 0.0045;  aMatrix_B[2,1] := 0.0012;  aMatrix_B[2,2] := 0.0185; aMatrix_B[2,3] := 0.0000;
    aMatrix_B[3,0] := 0.0385;  aMatrix_B[3,1] := 0.0450;  aMatrix_B[3,2] := -0.0150; aMatrix_B[3,3] := 0.0000;
    aMatrix_B[4,0] := -0.0850; aMatrix_B[4,1] := -0.1850; aMatrix_B[4,2] := 0.1250; aMatrix_B[4,3] := 0.0000;
    aMatrix_B[5,0] := 0.0000;  aMatrix_B[5,1] := 0.0000;  aMatrix_B[5,2] := 0.0450; aMatrix_B[5,3] := -0.0420;
    aMatrix_B[6,0] := 0.0000;  aMatrix_B[6,1] := 0.0000;  aMatrix_B[6,2] := 0.0350; aMatrix_B[6,3] := -0.0380;
    aMatrix_B[7,0] := 0.0015;  aMatrix_B[7,1] := 0.0010;  aMatrix_B[7,2] := 0.0045; aMatrix_B[7,3] := 0.0085;

    (* ------------------------------------------------------------------------------------- *)
    (* Discrete 4x8 Output Mapping Matrix C                                                  *)
    (* Outputs: y[0]=T_comb, y[1]=T_sh_in, y[2]=O2, y[3]=HCl                                 *)
    (* ------------------------------------------------------------------------------------- *)
    aMatrix_C[0,0] := 1.0; aMatrix_C[0,1] := 0.0; aMatrix_C[0,2] := 0.0; aMatrix_C[0,3] := 0.0;
    aMatrix_C[0,4] := 0.0; aMatrix_C[0,5] := 0.0; aMatrix_C[0,6] := 0.0; aMatrix_C[0,7] := 0.0;

    aMatrix_C[1,0] := 0.0; aMatrix_C[1,1] := 1.0; aMatrix_C[1,2] := 0.0; aMatrix_C[1,3] := 0.0;
    aMatrix_C[1,4] := 0.0; aMatrix_C[1,5] := 0.0; aMatrix_C[1,6] := 0.0; aMatrix_C[1,7] := 0.0;

    aMatrix_C[2,0] := 0.0; aMatrix_C[2,1] := 0.0; aMatrix_C[2,2] := 0.0; aMatrix_C[2,3] := 1.0;
    aMatrix_C[2,4] := 0.0; aMatrix_C[2,5] := 0.0; aMatrix_C[2,6] := 0.0; aMatrix_C[2,7] := 0.0;

    aMatrix_C[3,0] := 0.0; aMatrix_C[3,1] := 0.0; aMatrix_C[3,2] := 0.0; aMatrix_C[3,3] := 0.0;
    aMatrix_C[3,4] := 0.0; aMatrix_C[3,5] := 1.0; aMatrix_C[3,6] := 0.0; aMatrix_C[3,7] := 0.0;

    (* Direct Feedthrough Matrix D (4x4) *)
    FOR iIdx := 0 TO 3 DO
        FOR jIdx := 0 TO 3 DO
            aMatrix_D[iIdx, jIdx] := 0.0;
        END_FOR;
    END_FOR;

    (* ------------------------------------------------------------------------------------- *)
    (* Disturbance Coupling Matrix E (8x3)                                                   *)
    (* ------------------------------------------------------------------------------------- *)
    aMatrix_E[0,0] := 0.1450; aMatrix_E[0,1] := 0.0000; aMatrix_E[0,2] := 0.0000;
    aMatrix_E[1,0] := 0.0850; aMatrix_E[1,1] := 0.0000; aMatrix_E[1,2] := -0.0120;
    aMatrix_E[2,0] := 0.0450; aMatrix_E[2,1] := 0.0000; aMatrix_E[2,2] := -0.0450;
    aMatrix_E[3,0] := -0.0250; aMatrix_E[3,1] := 0.0000; aMatrix_E[3,2] := 0.0000;
    aMatrix_E[4,0] := -0.0450; aMatrix_E[4,1] := 0.0000; aMatrix_E[4,2] := 0.0000;
    aMatrix_E[5,0] := 0.0000; aMatrix_E[5,1] := 0.2450; aMatrix_E[5,2] := 0.0000;
    aMatrix_E[6,0] := 0.0000; aMatrix_E[6,1] := 0.1850; aMatrix_E[6,2] := 0.0000;
    aMatrix_E[7,0] := 0.0000; aMatrix_E[7,1] := 0.0120; aMatrix_E[7,2] := 0.0000;

    (* ------------------------------------------------------------------------------------- *)
    (* Kalman / Luenberger Observer Gain Matrix L_obs (8x4)                                  *)
    (* ------------------------------------------------------------------------------------- *)
    aMatrix_L_obs[0,0] := 0.3450; aMatrix_L_obs[0,1] := 0.0150; aMatrix_L_obs[0,2] := 0.0000; aMatrix_L_obs[0,3] := 0.0000;
    aMatrix_L_obs[1,0] := 0.0450; aMatrix_L_obs[1,1] := 0.3850; aMatrix_L_obs[1,2] := 0.0000; aMatrix_L_obs[1,3] := 0.0000;
    aMatrix_L_obs[2,0] := 0.0120; aMatrix_L_obs[2,1] := 0.0000; aMatrix_L_obs[2,2] := 0.0000; aMatrix_L_obs[2,3] := 0.0000;
    aMatrix_L_obs[3,0] := -0.0080; aMatrix_L_obs[3,1] := 0.0000; aMatrix_L_obs[3,2] := 0.4200; aMatrix_L_obs[3,3] := 0.0000;
    aMatrix_L_obs[4,0] := -0.0250; aMatrix_L_obs[4,1] := 0.0000; aMatrix_L_obs[4,2] := -0.0850; aMatrix_L_obs[4,3] := 0.0000;
    aMatrix_L_obs[5,0] := 0.0000; aMatrix_L_obs[5,1] := 0.0000; aMatrix_L_obs[5,2] := 0.0000; aMatrix_L_obs[5,3] := 0.3850;
    aMatrix_L_obs[6,0] := 0.0000; aMatrix_L_obs[6,1] := 0.0000; aMatrix_L_obs[6,2] := 0.0000; aMatrix_L_obs[6,3] := 0.1850;
    aMatrix_L_obs[7,0] := 0.0000; aMatrix_L_obs[7,1] := 0.0000; aMatrix_L_obs[7,2] := 0.0000; aMatrix_L_obs[7,3] := 0.0120;

    bFirstScanDone := TRUE;
END_IF;
"""
    sections.append(s3)

    # -------------------------------------------------------------------------
    # SECTION 4: LOGIC PART 2 - 2oo3 TMR VOTING
    # -------------------------------------------------------------------------
    s4 = """(* ============================================================================================= *)
(* SECTION 2: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) VOTING & FAULT DEGRADATION ENGINE            *)
(* ============================================================================================= *)
(* --------------------------------------------------------------------------------------------- *)
(* 1. Combustion Chamber Optical Pyrometer Transducers (rCombChamberTemp_degC_A, B, C)           *)
(* --------------------------------------------------------------------------------------------- *)
IF ABS(rCombChamberTemp_degC_A - rPrev_CT_A) < 0.001 THEN iStuck_CT_A := iStuck_CT_A + 1; ELSE iStuck_CT_A := 0; END_IF;
IF ABS(rCombChamberTemp_degC_B - rPrev_CT_B) < 0.001 THEN iStuck_CT_B := iStuck_CT_B + 1; ELSE iStuck_CT_B := 0; END_IF;
IF ABS(rCombChamberTemp_degC_C - rPrev_CT_C) < 0.001 THEN iStuck_CT_C := iStuck_CT_C + 1; ELSE iStuck_CT_C := 0; END_IF;
rPrev_CT_A := rCombChamberTemp_degC_A; rPrev_CT_B := rCombChamberTemp_degC_B; rPrev_CT_C := rCombChamberTemp_degC_C;

bHealth_CT_A := (rCombChamberTemp_degC_A >= 100.0) AND (rCombChamberTemp_degC_A <= 1350.0) AND (iStuck_CT_A < 250);
bHealth_CT_B := (rCombChamberTemp_degC_B >= 100.0) AND (rCombChamberTemp_degC_B <= 1350.0) AND (iStuck_CT_B < 250);
bHealth_CT_C := (rCombChamberTemp_degC_C >= 100.0) AND (rCombChamberTemp_degC_C <= 1350.0) AND (iStuck_CT_C < 250);

IF bHealth_CT_A AND bHealth_CT_B AND bHealth_CT_C THEN
    bDegraded_CT_1oo2 := FALSE; bDegraded_CT_1oo1 := FALSE;
    IF ((rCombChamberTemp_degC_A >= rCombChamberTemp_degC_B) AND (rCombChamberTemp_degC_A <= rCombChamberTemp_degC_C)) OR
       ((rCombChamberTemp_degC_A >= rCombChamberTemp_degC_C) AND (rCombChamberTemp_degC_A <= rCombChamberTemp_degC_B)) THEN
        rVoted_CombChamberTemp_degC := rCombChamberTemp_degC_A;
    ELSIF ((rCombChamberTemp_degC_B >= rCombChamberTemp_degC_A) AND (rCombChamberTemp_degC_B <= rCombChamberTemp_degC_C)) OR
          ((rCombChamberTemp_degC_B >= rCombChamberTemp_degC_C) AND (rCombChamberTemp_degC_B <= rCombChamberTemp_degC_A)) THEN
        rVoted_CombChamberTemp_degC := rCombChamberTemp_degC_B;
    ELSE
        rVoted_CombChamberTemp_degC := rCombChamberTemp_degC_C;
    END_IF;
    IF (ABS(rCombChamberTemp_degC_A - rCombChamberTemp_degC_B) > rTol_CombTemp_degC) OR
       (ABS(rCombChamberTemp_degC_B - rCombChamberTemp_degC_C) > rTol_CombTemp_degC) OR
       (ABS(rCombChamberTemp_degC_A - rCombChamberTemp_degC_C) > rTol_CombTemp_degC) THEN
        dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0001; (* Bit 0: Comb Temp Discrepancy *)
    END_IF;
ELSIF bHealth_CT_A AND bHealth_CT_B THEN
    bDegraded_CT_1oo2 := TRUE; rVoted_CombChamberTemp_degC := (rCombChamberTemp_degC_A + rCombChamberTemp_degC_B) * 0.5;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0002;
ELSIF bHealth_CT_A AND bHealth_CT_C THEN
    bDegraded_CT_1oo2 := TRUE; rVoted_CombChamberTemp_degC := (rCombChamberTemp_degC_A + rCombChamberTemp_degC_C) * 0.5;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0002;
ELSIF bHealth_CT_B AND bHealth_CT_C THEN
    bDegraded_CT_1oo2 := TRUE; rVoted_CombChamberTemp_degC := (rCombChamberTemp_degC_B + rCombChamberTemp_degC_C) * 0.5;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0002;
ELSIF bHealth_CT_A THEN
    bDegraded_CT_1oo1 := TRUE; rVoted_CombChamberTemp_degC := rCombChamberTemp_degC_A;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0004;
ELSIF bHealth_CT_B THEN
    bDegraded_CT_1oo1 := TRUE; rVoted_CombChamberTemp_degC := rCombChamberTemp_degC_B;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0004;
ELSIF bHealth_CT_C THEN
    bDegraded_CT_1oo1 := TRUE; rVoted_CombChamberTemp_degC := rCombChamberTemp_degC_C;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0004;
ELSE
    rVoted_CombChamberTemp_degC := 800.0; (* Fail-safe sub-temperature triggers aux burner *)
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0008;
    bGracefulDegradation := TRUE;
END_IF;

(* --------------------------------------------------------------------------------------------- *)
(* 2. Superheater Inlet Flue Gas Temperature Transducers (rSuperheaterInletTemp_degC_A, B, C)    *)
(* --------------------------------------------------------------------------------------------- *)
IF ABS(rSuperheaterInletTemp_degC_A - rPrev_ST_A) < 0.001 THEN iStuck_ST_A := iStuck_ST_A + 1; ELSE iStuck_ST_A := 0; END_IF;
IF ABS(rSuperheaterInletTemp_degC_B - rPrev_ST_B) < 0.001 THEN iStuck_ST_B := iStuck_ST_B + 1; ELSE iStuck_ST_B := 0; END_IF;
IF ABS(rSuperheaterInletTemp_degC_C - rPrev_ST_C) < 0.001 THEN iStuck_ST_C := iStuck_ST_C + 1; ELSE iStuck_ST_C := 0; END_IF;
rPrev_ST_A := rSuperheaterInletTemp_degC_A; rPrev_ST_B := rSuperheaterInletTemp_degC_B; rPrev_ST_C := rSuperheaterInletTemp_degC_C;

bHealth_ST_A := (rSuperheaterInletTemp_degC_A >= 100.0) AND (rSuperheaterInletTemp_degC_A <= 950.0) AND (iStuck_ST_A < 250);
bHealth_ST_B := (rSuperheaterInletTemp_degC_B >= 100.0) AND (rSuperheaterInletTemp_degC_B <= 950.0) AND (iStuck_ST_B < 250);
bHealth_ST_C := (rSuperheaterInletTemp_degC_C >= 100.0) AND (rSuperheaterInletTemp_degC_C <= 950.0) AND (iStuck_ST_C < 250);

IF bHealth_ST_A AND bHealth_ST_B AND bHealth_ST_C THEN
    bDegraded_ST_1oo2 := FALSE; bDegraded_ST_1oo1 := FALSE;
    IF ((rSuperheaterInletTemp_degC_A >= rSuperheaterInletTemp_degC_B) AND (rSuperheaterInletTemp_degC_A <= rSuperheaterInletTemp_degC_C)) OR
       ((rSuperheaterInletTemp_degC_A >= rSuperheaterInletTemp_degC_C) AND (rSuperheaterInletTemp_degC_A <= rSuperheaterInletTemp_degC_B)) THEN
        rVoted_SuperheaterTemp_degC := rSuperheaterInletTemp_degC_A;
    ELSIF ((rSuperheaterInletTemp_degC_B >= rSuperheaterInletTemp_degC_A) AND (rSuperheaterInletTemp_degC_B <= rSuperheaterInletTemp_degC_C)) OR
          ((rSuperheaterInletTemp_degC_B >= rSuperheaterInletTemp_degC_C) AND (rSuperheaterInletTemp_degC_B <= rSuperheaterInletTemp_degC_A)) THEN
        rVoted_SuperheaterTemp_degC := rSuperheaterInletTemp_degC_B;
    ELSE
        rVoted_SuperheaterTemp_degC := rSuperheaterInletTemp_degC_C;
    END_IF;
    IF (ABS(rSuperheaterInletTemp_degC_A - rSuperheaterInletTemp_degC_B) > rTol_SuperheaterTemp_degC) OR
       (ABS(rSuperheaterInletTemp_degC_B - rSuperheaterInletTemp_degC_C) > rTol_SuperheaterTemp_degC) OR
       (ABS(rSuperheaterInletTemp_degC_A - rSuperheaterInletTemp_degC_C) > rTol_SuperheaterTemp_degC) THEN
        dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0010;
    END_IF;
ELSIF bHealth_ST_A AND bHealth_ST_B THEN
    bDegraded_ST_1oo2 := TRUE; rVoted_SuperheaterTemp_degC := (rSuperheaterInletTemp_degC_A + rSuperheaterInletTemp_degC_B) * 0.5;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0020;
ELSIF bHealth_ST_A AND bHealth_ST_C THEN
    bDegraded_ST_1oo2 := TRUE; rVoted_SuperheaterTemp_degC := (rSuperheaterInletTemp_degC_A + rSuperheaterInletTemp_degC_C) * 0.5;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0020;
ELSIF bHealth_ST_B AND bHealth_ST_C THEN
    bDegraded_ST_1oo2 := TRUE; rVoted_SuperheaterTemp_degC := (rSuperheaterInletTemp_degC_B + rSuperheaterInletTemp_degC_C) * 0.5;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0020;
ELSIF bHealth_ST_A THEN
    bDegraded_ST_1oo1 := TRUE; rVoted_SuperheaterTemp_degC := rSuperheaterInletTemp_degC_A;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0040;
ELSIF bHealth_ST_B THEN
    bDegraded_ST_1oo1 := TRUE; rVoted_SuperheaterTemp_degC := rSuperheaterInletTemp_degC_B;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0040;
ELSIF bHealth_ST_C THEN
    bDegraded_ST_1oo1 := TRUE; rVoted_SuperheaterTemp_degC := rSuperheaterInletTemp_degC_C;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0040;
ELSE
    rVoted_SuperheaterTemp_degC := 680.0; (* Trip safe on total loss *)
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0080;
    bGracefulDegradation := TRUE;
END_IF;

(* --------------------------------------------------------------------------------------------- *)
(* 3. Boiler Steam Drum Pressure Transducers (rSteamDrumPressure_bar_A, B, C)                    *)
(* --------------------------------------------------------------------------------------------- *)
bHealth_DP_A := (rSteamDrumPressure_bar_A >= 0.0) AND (rSteamDrumPressure_bar_A <= 80.0);
bHealth_DP_B := (rSteamDrumPressure_bar_B >= 0.0) AND (rSteamDrumPressure_bar_B <= 80.0);
bHealth_DP_C := (rSteamDrumPressure_bar_C >= 0.0) AND (rSteamDrumPressure_bar_C <= 80.0);

IF bHealth_DP_A AND bHealth_DP_B AND bHealth_DP_C THEN
    IF ((rSteamDrumPressure_bar_A >= rSteamDrumPressure_bar_B) AND (rSteamDrumPressure_bar_A <= rSteamDrumPressure_bar_C)) OR
       ((rSteamDrumPressure_bar_A >= rSteamDrumPressure_bar_C) AND (rSteamDrumPressure_bar_A <= rSteamDrumPressure_bar_B)) THEN
        rVoted_SteamPressure_bar := rSteamDrumPressure_bar_A;
    ELSIF ((rSteamDrumPressure_bar_B >= rSteamDrumPressure_bar_A) AND (rSteamDrumPressure_bar_B <= rSteamDrumPressure_bar_C)) OR
          ((rSteamDrumPressure_bar_B >= rSteamDrumPressure_bar_C) AND (rSteamDrumPressure_bar_B <= rSteamDrumPressure_bar_A)) THEN
        rVoted_SteamPressure_bar := rSteamDrumPressure_bar_B;
    ELSE
        rVoted_SteamPressure_bar := rSteamDrumPressure_bar_C;
    END_IF;
ELSE
    rVoted_SteamPressure_bar := rSteamDrumPressure_bar_A;
END_IF;

(* --------------------------------------------------------------------------------------------- *)
(* 4. Baghouse Differential Pressure Transducers (rBaghouse_DiffPress_mbar_A, B, C)              *)
(* --------------------------------------------------------------------------------------------- *)
bHealth_BP_A := (rBaghouse_DiffPress_mbar_A >= 0.0) AND (rBaghouse_DiffPress_mbar_A <= 50.0);
bHealth_BP_B := (rBaghouse_DiffPress_mbar_B >= 0.0) AND (rBaghouse_DiffPress_mbar_B <= 50.0);
bHealth_BP_C := (rBaghouse_DiffPress_mbar_C >= 0.0) AND (rBaghouse_DiffPress_mbar_C <= 50.0);

IF bHealth_BP_A AND bHealth_BP_B AND bHealth_BP_C THEN
    IF ((rBaghouse_DiffPress_mbar_A >= rBaghouse_DiffPress_mbar_B) AND (rBaghouse_DiffPress_mbar_A <= rBaghouse_DiffPress_mbar_C)) OR
       ((rBaghouse_DiffPress_mbar_A >= rBaghouse_DiffPress_mbar_C) AND (rBaghouse_DiffPress_mbar_A <= rBaghouse_DiffPress_mbar_B)) THEN
        rVoted_Baghouse_dP_mbar := rBaghouse_DiffPress_mbar_A;
    ELSIF ((rBaghouse_DiffPress_mbar_B >= rBaghouse_DiffPress_mbar_A) AND (rBaghouse_DiffPress_mbar_B <= rBaghouse_DiffPress_mbar_C)) OR
          ((rBaghouse_DiffPress_mbar_B >= rBaghouse_DiffPress_mbar_C) AND (rBaghouse_DiffPress_mbar_B <= rBaghouse_DiffPress_mbar_A)) THEN
        rVoted_Baghouse_dP_mbar := rBaghouse_DiffPress_mbar_B;
    ELSE
        rVoted_Baghouse_dP_mbar := rBaghouse_DiffPress_mbar_C;
    END_IF;
ELSE
    rVoted_Baghouse_dP_mbar := rBaghouse_DiffPress_mbar_A;
END_IF;

(* --------------------------------------------------------------------------------------------- *)
(* 5. Flue Gas Residual Oxygen Voting (rFlueGas_O2_Pct_A, B, C)                                  *)
(* --------------------------------------------------------------------------------------------- *)
rVoted_FlueGas_O2_Pct := (rFlueGas_O2_Pct_A + rFlueGas_O2_Pct_B + rFlueGas_O2_Pct_C) / 3.0;
"""
    sections.append(s4)

    # -------------------------------------------------------------------------
    # SECTION 5: LOGIC PART 3 - CORROSION OBSERVER & DRY SCRUBBER DOSING
    # -------------------------------------------------------------------------
    s5 = """(* ============================================================================================= *)
(* SECTION 3: SUPERHEATER CHLORINE CORROSION OBSERVER & DRY LIME SCRUBBER DOSING                *)
(* ============================================================================================= *)
(* Superheater High-Temperature Chlorine Eutectic Corrosion Risk Index *)
(* If flue gas entering superheater exceeds 625°C, molten eutectic salts accelerate rapidly *)
IF rVoted_SuperheaterTemp_degC >= 650.0 THEN
    rChlorineCorrosionIndex_Pct := 100.0;
    bSuperheaterOvertempRisk    := TRUE;
    dwWTE_AlarmWord_Pri         := dwWTE_AlarmWord_Pri OR 16#0000_0001; (* Bit 0: SUPERHEATER_OVERTEMP_HH *)
ELSIF rVoted_SuperheaterTemp_degC >= 625.0 THEN
    rChlorineCorrosionIndex_Pct := 50.0 + ((rVoted_SuperheaterTemp_degC - 625.0) / 25.0) * 50.0;
    bSuperheaterOvertempRisk    := FALSE;
    dwWTE_AlarmWord_Sec         := dwWTE_AlarmWord_Sec OR 16#0000_0001; (* Bit 0: SUPERHEATER_TEMP_H_WARN *)
ELSE
    rChlorineCorrosionIndex_Pct := ((rVoted_SuperheaterTemp_degC - 550.0) / 75.0) * 50.0;
    IF rChlorineCorrosionIndex_Pct < 0.0 THEN rChlorineCorrosionIndex_Pct := 0.0; END_IF;
    bSuperheaterOvertempRisk    := FALSE;
END_IF;

(* Statutory 850°C / 2-Second Residence Timer Supervision (EU IED 2010/75/EU) *)
IF rVoted_CombChamberTemp_degC < rStatutoryMinTemp_degC THEN
    rSubTempTimer_s  := rSubTempTimer_s + tScanTime_s;
    bAuxBurnerDemand := TRUE;                   (* Demand auxiliary low-NOx burner firing *)

    IF rSubTempTimer_s >= 2.00 THEN
        bSubTemperatureStatutoryTrip := TRUE;
        dwWTE_AlarmWord_Pri          := dwWTE_AlarmWord_Pri OR 16#0000_0002; (* Bit 1: SUB_850C_STATUTORY_VIOLATION_HH *)
        iFSM_State                   := 90;     (* Immediate shutdown sequence *)
    END_IF;
ELSE
    rSubTempTimer_s              := 0.0;
    bSubTemperatureStatutoryTrip := FALSE;
    bAuxBurnerDemand             := FALSE;
END_IF;

(* Total Acid Gas Load Calculation (HCl + SO2 mass flux into scrubber) *)
(* Flue gas volume in Nm3/h reconstructed from primary and secondary air flows *)
rFlueGasVolumetricFlow_Nm3h := (rPrimaryAirFlow_Nm3h + rSecondaryAirFlow_Nm3h) * 1.25;

(* Acid gas mass flow rates [kg/h] *)
rAcidGasTotalLoad_kg_h := (rFlueGasVolumetricFlow_Nm3h * (rCEMS_HCl_mgNm3 + rCEMS_SO2_mgNm3) * 1.0E-6);

(* Stoichiometric Hydrated Lime Ca(OH)2 Dosing Requirement *)
rCalculatedLimeDemand_kg_h := (rFlueGasVolumetricFlow_Nm3h * 1.0E-6) *
                              (rCEMS_HCl_mgNm3 * rLimeEquiv_HCl_kg_kg + rCEMS_SO2_mgNm3 * rLimeEquiv_SO2_kg_kg) * rLimeOverStoichFactor;
IF rCalculatedLimeDemand_kg_h < 45.0 THEN rCalculatedLimeDemand_kg_h := 45.0; END_IF;
IF rCalculatedLimeDemand_kg_h > 480.0 THEN rCalculatedLimeDemand_kg_h := 480.0; END_IF;

(* Baghouse Fabric Filter Pulse-Jet Cleaning Sequencer *)
IF rVoted_Baghouse_dP_mbar >= rBaghouse_dP_CleanStart_mbar THEN
    bBaghousePulseJetValveCmd := TRUE;          (* Fire reverse compressed air blow *)
    dwWTE_StatusWord          := dwWTE_StatusWord OR 16#0000_0008; (* Bit 3: PULSE_JET_ACTIVE *)
ELSIF rVoted_Baghouse_dP_mbar <= rBaghouse_dP_CleanStop_mbar THEN
    bBaghousePulseJetValveCmd := FALSE;
END_IF;

(* Baghouse Broken Bag / Rupture Detection (Sudden opacity spike > 8.0% or dP collapse) *)
rBaghouse_dP_Rate_mbars := (rVoted_Baghouse_dP_mbar - rPrevBaghouse_dP_mbar) / tScanTime_s;
rPrevBaghouse_dP_mbar   := rVoted_Baghouse_dP_mbar;

IF (rFlueGasOpacity_Pct >= 8.50) OR ((rBaghouse_dP_Rate_mbars <= -5.0) AND (rVoted_Baghouse_dP_mbar <= 4.0)) THEN
    bBaghouseRuptureDetected := TRUE;
    dwWTE_AlarmWord_Pri      := dwWTE_AlarmWord_Pri OR 16#0000_0004; (* Bit 2: BAGHOUSE_BAG_RUPTURE_HH *)
ELSE
    bBaghouseRuptureDetected := FALSE;
END_IF;

(* Hydrated Lime Silo Bridging / Loss of Feed Fault *)
IF rLimeSiloWeight_tons <= 2.50 THEN
    bLimeSiloBridgingFault   := TRUE;
    dwWTE_AlarmWord_Sec      := dwWTE_AlarmWord_Sec OR 16#0000_0002; (* Bit 1: LIME_SILO_LOW_WARN *)
ELSE
    bLimeSiloBridgingFault   := FALSE;
END_IF;

(* Gross Boiler Thermal Energy Output [MW] *)
rCalculatedThermalDuty_MW := (rMainSteamFlow_t_h * (2780.0 - 450.0) / 3600.0);
"""
    sections.append(s5)

    # -------------------------------------------------------------------------
    # SECTION 6: LOGIC PART 4 - 8x8 STATE-SPACE & KALMAN OBSERVER
    # -------------------------------------------------------------------------
    s6 = """(* ============================================================================================= *)
(* SECTION 4: 8x8 DISCRETE STATE-SPACE TIME PROPAGATION & KALMAN OBSERVER UPDATE                 *)
(* ============================================================================================= *)
(* Map Disturbance Vector d *)
aDisturb_d[0] := 0.0;
aDisturb_d[1] := (rCEMS_HCl_mgNm3 - 18.50) * 0.10;
aDisturb_d[2] := rMainSteamFlow_t_h - 42.50;

(* State Propagation: x_pred = A * x_hat + B * u + E * d *)
FOR iIdx := 0 TO 7 DO
    rTmpSum := 0.0;
    FOR jIdx := 0 TO 7 DO
        rTmpSum := rTmpSum + aMatrix_A[iIdx, jIdx] * aState_x_hat[jIdx];
    END_FOR;
    FOR jIdx := 0 TO 3 DO
        rTmpSum := rTmpSum + aMatrix_B[iIdx, jIdx] * aControl_u[jIdx];
    END_FOR;
    FOR jIdx := 0 TO 2 DO
        rTmpSum := rTmpSum + aMatrix_E[iIdx, jIdx] * aDisturb_d[jIdx];
    END_FOR;
    aState_x_pred[iIdx] := rTmpSum;
END_FOR;

(* Measured Physical Outputs y_meas *)
aOutput_y[0] := rVoted_CombChamberTemp_degC;
aOutput_y[1] := rVoted_SuperheaterTemp_degC;
aOutput_y[2] := rVoted_FlueGas_O2_Pct;
aOutput_y[3] := rCEMS_HCl_mgNm3;

(* Observer Innovation Correction: x_hat = x_pred + L_obs * (y_meas - C * x_pred) *)
FOR iIdx := 0 TO 7 DO
    rTmpSum := aState_x_pred[iIdx];
    FOR jIdx := 0 TO 3 DO
        rTmpSum := rTmpSum + aMatrix_L_obs[iIdx, jIdx] * (aOutput_y[jIdx] -
            (aMatrix_C[jIdx, 0]*aState_x_pred[0] + aMatrix_C[jIdx, 1]*aState_x_pred[1] +
             aMatrix_C[jIdx, 2]*aState_x_pred[2] + aMatrix_C[jIdx, 3]*aState_x_pred[3] +
             aMatrix_C[jIdx, 4]*aState_x_pred[4] + aMatrix_C[jIdx, 5]*aState_x_pred[5] +
             aMatrix_C[jIdx, 6]*aState_x_pred[6] + aMatrix_C[jIdx, 7]*aState_x_pred[7]));
    END_FOR;
    aState_x_hat[iIdx] := rTmpSum;
END_FOR;
"""
    sections.append(s6)

    # -------------------------------------------------------------------------
    # SECTION 7: LOGIC PART 5 - MPC SOLVER & COMBUSTION STAGING
    # -------------------------------------------------------------------------
    s7 = """(* ============================================================================================= *)
(* SECTION 5: MODEL PREDICTIVE CONTROL & AIR STAGING OPTIMIZATION                                *)
(* ============================================================================================= *)
(* Target Setpoints *)
aOutput_y_sp[0] := 985.0;                   (* Core combustion temp target [deg C] *)
aOutput_y_sp[1] := 615.0;                   (* Superheater inlet temp target (< 650°C strictly) *)
aOutput_y_sp[2] := 6.80;                    (* Residual oxygen setpoint [vol%] *)
aOutput_y_sp[3] := 15.00;                   (* HCl target emission [mg/Nm3] *)

(* Tracking Error *)
aOutput_y_error[0] := aOutput_y[0] - aOutput_y_sp[0];
aOutput_y_error[1] := aOutput_y[1] - aOutput_y_sp[1];
aOutput_y_error[2] := aOutput_y[2] - aOutput_y_sp[2];
aOutput_y_error[3] := aOutput_y[3] - aOutput_y_sp[3];

IF NOT bGracefulDegradation AND (iFSM_State = 20) THEN
    bMPC_Active := TRUE;

    (* Approximate Diagonal Hessian *)
    aHessian_diag[0] := aWeight_Q[0] * 0.0012 + aWeight_R[0]; (* Primary air *)
    aHessian_diag[1] := aWeight_Q[1] * 0.0025 + aWeight_R[1]; (* Secondary overfire air *)
    aHessian_diag[2] := aWeight_Q[0] * 0.0045 + aWeight_R[2]; (* Waste ram feed rate *)
    aHessian_diag[3] := aWeight_Q[3] * 0.0018 + aWeight_R[3]; (* Lime sorbent feed *)

    (* Gradient Calculation *)
    aGrad_g[0] := aWeight_Q[0] * aOutput_y_error[0] * 0.0245 + aWeight_R[0] * aControl_du[0];
    aGrad_g[1] := aWeight_Q[1] * aOutput_y_error[1] * (-0.0450) + aWeight_R[1] * aControl_du[1];
    aGrad_g[2] := aWeight_Q[0] * aOutput_y_error[0] * 0.0850 + aWeight_R[2] * aControl_du[2];
    aGrad_g[3] := aWeight_Q[3] * aOutput_y_error[3] * (-0.0420) + aWeight_R[3] * aControl_du[3];

    (* Iterative Projected Gradient Descent *)
    FOR iIterQP := 1 TO iMaxIterQP DO
        FOR iIdx := 0 TO 3 DO
            aStep_du[iIdx] := aControl_du[iIdx] - (rAlphaStep / aHessian_diag[iIdx]) * aGrad_g[iIdx];

            (* Slew rate constraints *)
            IF aStep_du[iIdx] > aLimit_du_Max[iIdx] THEN
                aStep_du[iIdx] := aLimit_du_Max[iIdx];
            ELSIF aStep_du[iIdx] < aLimit_du_Min[iIdx] THEN
                aStep_du[iIdx] := aLimit_du_Min[iIdx];
            END_IF;

            (* Actuator limits *)
            IF (aControl_u[iIdx] + aStep_du[iIdx]) > aLimit_u_Max[iIdx] THEN
                aStep_du[iIdx] := aLimit_u_Max[iIdx] - aControl_u[iIdx];
            ELSIF (aControl_u[iIdx] + aStep_du[iIdx]) < aLimit_u_Min[iIdx] THEN
                aStep_du[iIdx] := aLimit_u_Min[iIdx] - aControl_u[iIdx];
            END_IF;

            aControl_du[iIdx] := aStep_du[iIdx];
        END_FOR;
    END_FOR;

    (* Apply Moves *)
    aControl_u[0] := aControl_u[0] + aControl_du[0];
    aControl_u[1] := aControl_u[1] + aControl_du[1];
    aControl_u[2] := aControl_u[2] + aControl_du[2];
    aControl_u[3] := aControl_u[3] + aControl_du[3];

    rPrimaryAirFanCmd_Pct   := aControl_u[0];
    rSecondaryAirFanCmd_Pct := aControl_u[1];
    rWasteRamFeedSpeed_spm  := aControl_u[2];
    rLimeDosingFeeder_kgh   := aControl_u[3];
ELSE
    (* Fallback Decoupled Control *)
    bMPC_Active := FALSE;

    (* Secondary Overfire Air PID on Superheater Inlet Temperature *)
    rTmpSum := (rVoted_SuperheaterTemp_degC - 615.0);
    rPID_Integ_Air := rPID_Integ_Air + rTmpSum * tScanTime_s;
    IF rPID_Integ_Air > 25.0 THEN rPID_Integ_Air := 25.0; END_IF;
    IF rPID_Integ_Air < -25.0 THEN rPID_Integ_Air := -25.0; END_IF;
    rSecondaryAirFanCmd_Pct := 48.0 + rPID_Kp_Air * rTmpSum + rPID_Ki_Air * rPID_Integ_Air;

    IF rSecondaryAirFanCmd_Pct > 100.0 THEN rSecondaryAirFanCmd_Pct := 100.0; END_IF;
    IF rSecondaryAirFanCmd_Pct < 15.0 THEN rSecondaryAirFanCmd_Pct := 15.0; END_IF;

    (* Lime Feeder Feedforward + PID *)
    rLimeDosingFeeder_kgh := rCalculatedLimeDemand_kg_h;
END_IF;

(* Automatic Lime Feed Boost on HCl / SO2 Spike *)
IF rCEMS_HCl_mgNm3 >= 35.0 THEN
    rLimeDosingFeeder_kgh := rLimeDosingFeeder_kgh * 1.35;
END_IF;

(* Grate Speed Zone Proportional Pacing *)
rGrateSpeed_Zone1_Pct := rWasteRamFeedSpeed_spm * 2.10;
rGrateSpeed_Zone2_Pct := rWasteRamFeedSpeed_spm * 2.85;
rGrateSpeed_Zone3_Pct := rWasteRamFeedSpeed_spm * 2.25;
"""
    sections.append(s7)

    # -------------------------------------------------------------------------
    # SECTION 8: LOGIC PART 6 - FSM MACHINE SEQUENCER
    # -------------------------------------------------------------------------
    s8 = """(* ============================================================================================= *)
(* SECTION 6: MULTI-STAGE FINITE STATE MACHINE (FSM) SEQUENCING                                  *)
(* ============================================================================================= *)
IF iFSM_State = iPreviousFSM_State THEN
    rStateTimer_s := rStateTimer_s + tScanTime_s;
ELSE
    rStateTimer_s      := 0.0;
    iPreviousFSM_State := iFSM_State;
END_IF;

CASE iFSM_State OF
    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 0: FURNACE_AUX_BURNER_PREHEAT (Aux Burners Preheating Refractory to > 850°C)        *)
    (* ----------------------------------------------------------------------------------------- *)
    0:
        rWasteRamFeedSpeed_spm  := 0.00;            (* Waste ram feed locked *)
        rPrimaryAirFanCmd_Pct   := 35.0;            (* Light purge *)
        rSecondaryAirFanCmd_Pct := 25.0;
        bAuxBurnerDemand        := TRUE;            (* Fire startup auxiliary burners *)
        rPreheatTimer_s         := rPreheatTimer_s + tScanTime_s;

        (* Advance to Waste Feed Start when refractory reaches statutory 850°C and ID fan running *)
        IF bInducedDraftFanRunning AND (rVoted_CombChamberTemp_degC >= 865.0) AND (rPreheatTimer_s >= 60.0) THEN
            rPreheatTimer_s := 0.0;
            iFSM_State      := 10;                  (* Advance to WASTE_RAM_FEED_START *)
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 10: WASTE_RAM_FEED_START (Waste Pushed to Drying Grate, Bed Ignition Observed)      *)
    (* ----------------------------------------------------------------------------------------- *)
    10:
        rWasteRamFeedSpeed_spm  := 10.0;            (* Slow initial ram feed *)
        rPrimaryAirFanCmd_Pct   := 50.0;            (* Preheated undergrate air to dry waste *)
        bAuxBurnerDemand        := TRUE;            (* Maintain aux burners until MSW self-sustains *)

        (* Detect solid bed light-off: Chamber temp > 920°C and steam production starts *)
        IF (rVoted_CombChamberTemp_degC >= 920.0) AND (rMainSteamFlow_t_h >= 15.0) THEN
            bAuxBurnerDemand := FALSE;              (* Disengage aux burners *)
            iFSM_State       := 20;                 (* Advance to STEADY_COMBUSTION_POWER_RUN *)
        END_IF;

        (* Ignition failure *)
        IF rStateTimer_s >= 2400.0 THEN
            dwWTE_AlarmWord_Pri := dwWTE_AlarmWord_Pri OR 16#0000_0008; (* IGNITION_TIMEOUT_FAIL *)
            iFSM_State          := 0;
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 20: STEADY_COMBUSTION_POWER_RUN (Continuous Power Generation & MPC Superheater Trim)*)
    (* ----------------------------------------------------------------------------------------- *)
    20:
        (* Normal closed-loop modulation driven by Section 5 MPC / Fallback Controller *)
        (* Trip to emergency quench if statutory sub-temp or drum overpressure *)
        IF bSubTemperatureStatutoryTrip OR (rVoted_SteamPressure_bar >= rDrumDesignPressure_bar) THEN
            iFSM_State := 90;
        END_IF;

        (* ID Fan failure interlock *)
        IF NOT bInducedDraftFanRunning THEN
            dwWTE_AlarmWord_Pri := dwWTE_AlarmWord_Pri OR 16#0000_0010; (* ID_FAN_TRIP_INTERLOCK *)
            iFSM_State          := 90;
        END_IF;

        (* Controlled operator stop *)
        IF NOT bEnable THEN
            iFSM_State := 40;                       (* Advance to CONTROLLED_BURNOUT_COOLDOWN *)
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 30: FLUE_GAS_SCRUBBER_CLEAN (Dedicated Baghouse Reverse Pulse-Jet Cleaning Routine) *)
    (* ----------------------------------------------------------------------------------------- *)
    30:
        bBaghousePulseJetValveCmd := TRUE;
        rPulseJetCycleTimer_s     := rPulseJetCycleTimer_s + tScanTime_s;

        IF rPulseJetCycleTimer_s >= 60.0 THEN
            bBaghousePulseJetValveCmd := FALSE;
            rPulseJetCycleTimer_s     := 0.0;
            iFSM_State                := 20;        (* Return to steady run *)
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 40: CONTROLLED_BURNOUT_COOLDOWN (Waste Feed Halted, Grate Running to Extinguish Bed)*)
    (* ----------------------------------------------------------------------------------------- *)
    40:
        rWasteRamFeedSpeed_spm  := 0.00;            (* No more raw waste *)
        rPrimaryAirFanCmd_Pct   := 45.0;            (* Air to burn out residual char on Zone 3 *)
        rGrateSpeed_Zone1_Pct   := 30.0;
        rGrateSpeed_Zone2_Pct   := 45.0;
        rGrateSpeed_Zone3_Pct   := 60.0;            (* Evacuate ash to discharger *)

        IF (rVoted_CombChamberTemp_degC <= 350.0) AND (rMainSteamFlow_t_h <= 2.0) THEN
            rPrimaryAirFanCmd_Pct   := 0.00;
            rSecondaryAirFanCmd_Pct := 0.00;
            iFSM_State              := 0;           (* Safe cold standby *)
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 90: EMERGENCY_SAFETY_QUENCH (Immediate Air Cut, Aux Burner Lock, Vent Relief)      *)
    (* ----------------------------------------------------------------------------------------- *)
    90:
        rWasteRamFeedSpeed_spm  := 0.00;
        rPrimaryAirFanCmd_Pct   := 15.0;            (* Emergency minimum draft *)
        rSecondaryAirFanCmd_Pct := 10.0;
        bAuxBurnerDemand        := FALSE;

        (* Reset when alarms cleared and operator reset acknowledged *)
        IF bResetTripAlarms AND (rVoted_SteamPressure_bar <= 40.0) AND (NOT bEmergencyBoilerTrip) THEN
            iFSM_State := 0;
        END_IF;
END_CASE;
"""
    sections.append(s8)

    # -------------------------------------------------------------------------
    # SECTION 9: LOGIC PART 7 - ISA-18.2 ALARMS & DIAGNOSTIC PACKING
    # -------------------------------------------------------------------------
    s9 = """(* ============================================================================================= *)
(* SECTION 7: ISA-18.2 ALARM MATRIX, LATCHING & STATUS WORD BIT-PACKING                          *)
(* ============================================================================================= *)
(* 1. Steam Drum Pressure Alarms *)
IF rVoted_SteamPressure_bar >= rDrumDesignPressure_bar THEN
    dwWTE_AlarmWord_Pri := dwWTE_AlarmWord_Pri OR 16#0000_0020; (* Bit 5: DRUM_PRESSURE_HH_TRIP *)
ELSIF rVoted_SteamPressure_bar >= 54.00 THEN
    dwWTE_AlarmWord_Sec := dwWTE_AlarmWord_Sec OR 16#0000_0004; (* Bit 2: DRUM_PRESSURE_H_WARN *)
END_IF;

(* 2. Baghouse Differential Pressure Alarms *)
IF rVoted_Baghouse_dP_mbar >= 22.0 THEN
    dwWTE_AlarmWord_Pri := dwWTE_AlarmWord_Pri OR 16#0000_0040; (* Bit 6: BAGHOUSE_DP_HH_TRIP *)
ELSIF rVoted_Baghouse_dP_mbar >= 18.0 THEN
    dwWTE_AlarmWord_Sec := dwWTE_AlarmWord_Sec OR 16#0000_0008; (* Bit 3: BAGHOUSE_DP_H_WARN *)
END_IF;

(* 3. Flue Gas CEMS Emission Warnings *)
IF rCEMS_HCl_mgNm3 >= 45.0 THEN
    dwWTE_AlarmWord_Sec := dwWTE_AlarmWord_Sec OR 16#0000_0010; (* Bit 4: HCL_EMISSION_HIGH_WARN *)
END_IF;

IF rCEMS_SO2_mgNm3 >= 85.0 THEN
    dwWTE_AlarmWord_Sec := dwWTE_AlarmWord_Sec OR 16#0000_0020; (* Bit 5: SO2_EMISSION_HIGH_WARN *)
END_IF;

(* Master Reset *)
IF bResetTripAlarms THEN
    dwWTE_AlarmWord_Pri := 16#0000_0000;
    dwWTE_AlarmWord_Sec := 16#0000_0000;
END_IF;

(* --------------------------------------------------------------------------------------------- *)
(* 4. 32-Bit Waste-to-Energy Status Word Packing (dwWTE_StatusWord)                              *)
(* --------------------------------------------------------------------------------------------- *)
(* Bits 0..7  : Current FSM State Integer [0..90] *)
(* Bit 8      : bAuxBurnerDemand *)
(* Bit 9      : bSubTemperatureStatutoryTrip *)
(* Bit 10     : bSuperheaterOvertempRisk *)
(* Bit 11     : bBaghouseRuptureDetected *)
(* Bit 12     : bMPC_Active *)
(* Bit 13     : bGracefulDegradation *)
(* Bit 14     : bInducedDraftFanRunning *)
(* Bit 15     : bBaghousePulseJetValveCmd *)
(* Bit 31     : Master Emergency Trip Flag *)
dwWTE_StatusWord := INT_TO_DWORD(iFSM_State);
IF bAuxBurnerDemand              THEN dwWTE_StatusWord := dwWTE_StatusWord OR 16#0000_0100; END_IF;
IF bSubTemperatureStatutoryTrip  THEN dwWTE_StatusWord := dwWTE_StatusWord OR 16#0000_0200; END_IF;
IF bSuperheaterOvertempRisk      THEN dwWTE_StatusWord := dwWTE_StatusWord OR 16#0000_0400; END_IF;
IF bBaghouseRuptureDetected      THEN dwWTE_StatusWord := dwWTE_StatusWord OR 16#0000_0800; END_IF;
IF bMPC_Active                   THEN dwWTE_StatusWord := dwWTE_StatusWord OR 16#0000_1000; END_IF;
IF bGracefulDegradation          THEN dwWTE_StatusWord := dwWTE_StatusWord OR 16#0000_2000; END_IF;
IF bInducedDraftFanRunning       THEN dwWTE_StatusWord := dwWTE_StatusWord OR 16#0000_4000; END_IF;
IF bBaghousePulseJetValveCmd     THEN dwWTE_StatusWord := dwWTE_StatusWord OR 16#0000_8000; END_IF;
IF (iFSM_State = 90)             THEN dwWTE_StatusWord := dwWTE_StatusWord OR 16#8000_0000; END_IF;

END_FUNCTION_BLOCK
"""
    sections.append(s9)

    return "".join(sections)

if __name__ == "__main__":
    code = build_wte_block()
    print(f"Total ST code length: {len(code)} characters")
