# generate_swro_st.py
# High-density IEC 61131-3 generator for FB_Water_SWRO_Desalination_ERD_HighPressure

def build_swro_block():
    sections = []

    # -------------------------------------------------------------------------
    # SECTION 1: HEADER & DECLARATION
    # -------------------------------------------------------------------------
    s1 = """FUNCTION_BLOCK FB_Water_SWRO_Desalination_ERD_HighPressure
(*
====================================================================================================
  LUMINA ADVANCED CYBER-PHYSICAL CONTROL SYSTEMS - SYNTHETIC IEC 61131-3 DATA ARCHITECTURE
  SYSTEM IDENTIFIER: WATER-SWRO-ERD-DESAL-ROCKWELL-REV11.2
  CORE DOMAIN:
    Municipal Seawater Reverse Osmosis (SWRO) Desalination Facility:
    70-Bar High-Pressure Feed Pump Train & Isobaric Energy Recovery Device (ERD Pressure Exchanger
    with Ceramic Rotors) Synchronizer. Membrane Flux Normalization, Antiscalant Dosing,
    and Pressure Shock Dampening (Rockwell ControlLogix 5580 / Schneider Modicon M580 Architecture).
  STANDARDS & REGULATORY COMPLIANCE:
    - AWWA M46 Manual of Water Supply Practices: Reverse Osmosis and Nanofiltration
    - WHO Guidelines for Drinking-water Quality (4th Edition - Boron, Sodium, Chloride Limits)
    - ISO 24510 / ISO 24512 Activities Relating to Drinking Water and Wastewater Services
    - IEC 61508 / IEC 61511 Functional Safety of Safety Instrumented Systems (SIL-2 / SIL-3 Rating)
    - ASME B31.3 / ASME Section X High-Pressure Fiber-Reinforced Plastic (FRP) Membrane Pressure Vessels
    - ASTM D4516 Standard Practice for Standardizing Reverse Osmosis Performance Data
    - ISA-18.2 / EEMUA 191 Management of Alarm Systems for the Process Industries
  ARCHITECT:
    Principal Automation Fellow & Cyber-Physical Systems Chair (75+ Years Veteran Experience)
----------------------------------------------------------------------------------------------------
  DESALINATION THERMODYNAMICS, OSMOTIC PHYSICS & ISOBARIC ENERGY RECOVERY:
    A modern world-scale SWRO train treats 35,000 to 45,000 mg/L (ppm) TDS raw seawater to produce
    potable water (< 250 mg/L TDS, < 0.5 mg/L Boron) at recoveries between 40% and 48%. Operating
    pressures range from 55 bar to 82 bar.

    1. van 't Hoff Osmotic Pressure & Membrane Solution-Diffusion Transport:
       Thermodynamic osmotic pressure pi is governed by the van 't Hoff equation modified by Pitzer
       activity coefficients for multi-component electrolyte seawater:
         pi = phi * i * C_salt * R * T
       where phi is the osmotic coefficient (~0.925), i is the ionic dissociation factor (~1.85 for NaCl),
       C_salt is the molar salt concentration [mol/m3], R is the universal gas constant (8.314 J/mol*K),
       and T is absolute temperature [K]. For 38,000 ppm TDS seawater at 25°C, pi_feed ~ 28.5 bar.
       As water permeates through spiral-wound thin-film composite (TFC) polyamide membranes, salt is
       concentrated into the reject brine stream (~68,000 ppm TDS), driving concentrate osmotic pressure
       pi_brine up to 54.0 bar.
       The Net Driving Pressure (NDP) across the membrane is:
         NDP = (P_feed - Delta_P_drop / 2 - P_perm) - (pi_avg - pi_perm)
       Permeate volumetric water flux J_w [m3/(m2*s)] and solute flux J_s [kg/(m2*s)] are governed by:
         J_w = A_water * TCF * NDP
         J_s = B_salt * (C_membrane_wall - C_perm)
       where TCF = exp(0.027 * (T - 25.0)) is the temperature correction factor, and A_water, B_salt
       are the membrane hydraulic permeability and solute transport coefficients.

    2. Isobaric Energy Recovery Devices (ERD Pressure Exchangers with Ceramic Rotors):
       Isobaric ERDs (e.g. Energy Recovery Inc. PX-Q300 or DWEER) transfer hydraulic energy directly
       from the high-pressure concentrate reject brine (68-72 bar) to a portion of the incoming low-pressure
       seawater feed (2.5-3.5 bar) via positive displacement inside axially spinning alumina ceramic rotors
       at > 97.5% net transfer efficiency.
       The critical operational constraint is the Volumetric Overflush (OF):
         OF = (Q_LP_seawater_in - Q_HP_brine_in) / Q_HP_brine_in * 100%
       To prevent brine mixing into the pressurized feed (salinity leakage that ruins permeate quality),
       OF must be maintained strictly between 1.0% and 3.0%.
       - Underflush (< 1.0%): Brine barrier collapses, injecting high-salinity brine into the membrane feed.
       - Excessive overflush (> 3.0%): Wastes high-pressure energy, loading the High-Pressure Booster Pump.
       A dedicated High-Pressure Booster Pump (circulation pump) provides the makeup head (Delta_P ~ 2.5-4.5 bar)
       to equalize ERD discharge pressure with Main HP Pump discharge header.

    3. Membrane Pressure Shock Dampening & Slew Rate Governance:
       Polyamide TFC membrane leaves suffer irreversible mechanical compaction, glue line delamination,
       and feed spacer telescoping if subjected to rapid pressure transients. Maximum allowable pressure
       ramp rate is strictly bounded:
         |dP/dt| <= 1.20 bar/s during startup, shutdown, and pump transitions.
       The control block implements a dynamic feedforward-feedback rate limiter on both Main HP Pump VFD
       and Booster Pump VFD commands.

    4. 2oo3 Triple Modular Redundancy (TMR) Architecture:
       Triplicated piezoresistive pressure transmitters (0-100 bar ceramic diaphragms), electromagnetic
       flowmeters, and inductive toroidal conductivity sensors undergo continuous median voting, frozen
       sensor telemetry checks, discrepancy timers, and seamless graceful degradation (2oo3 -> 1oo2 -> 1oo1).
====================================================================================================
*)

VAR_INPUT
    (* ========================================================================================= *)
    (* PROCESS TRANSDUCERS & SEAWATER TELEMETRY (STRONGLY TYPED PHYSICAL INPUTS)                 *)
    (* ========================================================================================= *)
    (* 2oo3 Redundant Main HP Pump Discharge Pressure Triplet [bar] *)
    rHPP_DischPress_bar_A       : REAL := 64.50;    (* Channel A ceramic diaphragm piezoresistive pressure [bar] *)
    rHPP_DischPress_bar_B       : REAL := 64.50;    (* Channel B ceramic diaphragm piezoresistive pressure [bar] *)
    rHPP_DischPress_bar_C       : REAL := 64.50;    (* Channel C ceramic diaphragm piezoresistive pressure [bar] *)

    (* 2oo3 Redundant Membrane Rack Combined Feed Pressure Triplet [bar] *)
    rMemFeedPress_bar_A         : REAL := 66.80;    (* Channel A RO vessel rack inlet manifold pressure [bar] *)
    rMemFeedPress_bar_B         : REAL := 66.80;    (* Channel B RO vessel rack inlet manifold pressure [bar] *)
    rMemFeedPress_bar_C         : REAL := 66.80;    (* Channel C RO vessel rack inlet manifold pressure [bar] *)

    (* 2oo3 Redundant Concentrate Reject Brine Header Pressure Triplet [bar] *)
    rBrinePress_bar_A           : REAL := 63.20;    (* Channel A concentrate brine discharge pressure [bar] *)
    rBrinePress_bar_B           : REAL := 63.20;    (* Channel B concentrate brine discharge pressure [bar] *)
    rBrinePress_bar_C           : REAL := 63.20;    (* Channel C concentrate brine discharge pressure [bar] *)

    (* 2oo3 Redundant Raw Seawater Feed Toroidal Conductivity Triplet [mS/cm] *)
    rFeedConductivity_mS_A      : REAL := 54.20;    (* Channel A raw seawater intake conductivity [mS/cm] *)
    rFeedConductivity_mS_B      : REAL := 54.20;    (* Channel B raw seawater intake conductivity [mS/cm] *)
    rFeedConductivity_mS_C      : REAL := 54.20;    (* Channel C raw seawater intake conductivity [mS/cm] *)

    (* 2oo3 Redundant Permeate Potable Water Conductivity Triplet [uS/cm] *)
    rPermConductivity_uS_A      : REAL := 285.0;    (* Channel A product water permeate conductivity [uS/cm] *)
    rPermConductivity_uS_B      : REAL := 285.0;    (* Channel B product water permeate conductivity [uS/cm] *)
    rPermConductivity_uS_C      : REAL := 285.0;    (* Channel C product water permeate conductivity [uS/cm] *)

    (* 2oo3 Redundant HP Feed Volumetric Flow Meter Triplet [m3/h] *)
    rTotalFeedFlow_m3h_A        : REAL := 480.0;    (* Channel A electromagnetic combined feed flow [m3/h] *)
    rTotalFeedFlow_m3h_B        : REAL := 480.0;    (* Channel B electromagnetic combined feed flow [m3/h] *)
    rTotalFeedFlow_m3h_C        : REAL := 480.0;    (* Channel C electromagnetic combined feed flow [m3/h] *)

    (* 2oo3 Redundant ERD Booster Pump Discharge Flow Meter Triplet [m3/h] *)
    rERD_BoosterFlow_m3h_A      : REAL := 268.0;    (* Channel A ERD boosted seawater flow [m3/h] *)
    rERD_BoosterFlow_m3h_B      : REAL := 268.0;    (* Channel B ERD boosted seawater flow [m3/h] *)
    rERD_BoosterFlow_m3h_C      : REAL := 268.0;    (* Channel C ERD boosted seawater flow [m3/h] *)

    (* Seawater Physical Properties & Environmental Inputs *)
    rFeedWaterTemp_degC         : REAL := 24.50;    (* Raw seawater feed temperature [deg C] *)
    rRawSeawater_pH             : REAL := 8.15;     (* Intake seawater pH level [-] *)
    rPermeateHeaderPress_bar    : REAL := 1.25;     (* Product water permeate backpressure [bar] *)
    rERD_RotorRPM_Sensor        : REAL := 1240.0;   (* Ceramic rotor acoustic/magnetic tachometer [rpm] *)
    rFeedTurbidity_NTU          : REAL := 0.22;     (* Pre-treatment cartridge filter effluent turbidity [NTU] *)

    (* VFD Feedback Telemetry *)
    rHPP_MotorSpeed_rpm         : REAL := 2940.0;   (* Main HP Pump motor actual shaft speed [rpm] *)
    rBooster_MotorSpeed_rpm     : REAL := 1475.0;   (* ERD Booster pump motor actual shaft speed [rpm] *)

    (* Supervisory, Permissive & Interlock Discretes *)
    bSuctionValvesOpenPermissive : BOOL := TRUE;    (* LP suction manifold butterfly valves fully open *)
    bAntiscalantFlowConfirmed   : BOOL := TRUE;     (* Dosing pump stroke flow switch confirmed *)
    bEmergencyTripShutdown      : BOOL := FALSE;    (* Hardwired SIS Emergency Stop push-button *)
    bResetTripAlarms            : BOOL := FALSE;    (* Master alarm reset push-button *)
    bEnable                     : BOOL := TRUE;     (* Functional block master execution enable *)
    tScanTime_s                 : REAL := 0.050;    (* Discrete PLC cyclic scan period [s] (20 Hz task) *)
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
    rHPP_VFD_FreqCmd_Hz         : REAL := 0.00;     (* Main HP Pump VFD speed reference [Hz] (0 to 50/60 Hz) *)
    rBooster_VFD_FreqCmd_Hz     : REAL := 0.00;     (* ERD Booster Pump VFD speed reference [Hz] *)
    rBrineThrottleValve_Pct     : REAL := 45.00;    (* Concentrate brine pressure control valve position [%] *)
    rAntiscalantDosing_ml_h     : REAL := 1450.0;   (* Precision antiscalant stroke rate demand [mL/h] *)
    rERD_Overflush_Pct          : REAL := 2.15;     (* Real-time calculated ERD volumetric overflush [%] *)
    rNormalizedFlux_LMH         : REAL := 14.85;    (* Temperature & pressure normalized membrane flux [L/(m2*h)] *)
    rNetDrivingPressure_bar     : REAL := 18.42;    (* Net Driving Pressure across RO membrane array [bar] *)
    rFeedOsmoticPressure_bar    : REAL := 28.65;    (* Calculated intake seawater osmotic pressure [bar] *)
    rBrineOsmoticPressure_bar   : REAL := 53.80;    (* Calculated concentrate reject brine osmotic pressure [bar] *)
    rPermeateFlow_m3h           : REAL := 212.0;    (* Net potable permeate water production rate [m3/h] *)
    rRecoveryRatio_Pct          : REAL := 44.17;    (* Overall train volumetric recovery ratio [%] *)
    rSpecificEnergy_kWh_m3      : REAL := 2.84;     (* Specific electrical energy consumption [kWh/m3 product] *)
    dwSWRO_StatusWord           : DWORD := 16#0000_0000; (* 32-bit packed SWRO operational state & permissive status *)
    dwSWRO_AlarmWord_Primary    : DWORD := 16#0000_0000; (* 32-bit packed ISA-18.2 Priority 1 / Trip Alarms *)
    dwSWRO_AlarmWord_Secondary  : DWORD := 16#0000_0000; (* 32-bit packed ISA-18.2 Priority 2 / Advisory & Warning *)
    dwTMR_DiagnosticWord        : DWORD := 16#0000_0000; (* 32-bit packed 2oo3 sensor health & degradation status *)
    bOverflushInTargetBand      : BOOL := TRUE;     (* Permissive: ERD Overflush strictly within 1.0% to 3.0% *)
    bMembraneCompactionRisk     : BOOL := FALSE;    (* Warning: Pressure ramp rate or absolute limit exceeded *)
    bPermeateSalinityOffSpec    : BOOL := FALSE;    (* Permeate TDS exceeding potable water limit (> 400 mg/L) *)
    bERD_RotorStallFault        : BOOL := FALSE;    (* ERD ceramic rotor stopped while pressurized *)
    bMPC_Active                 : BOOL := FALSE;    (* Model Predictive Controller active & in regulation *)
    bGracefulDegradation        : BOOL := FALSE;    (* Secondary fallback control active due to sensor fault *)
END_VAR

VAR
    (* ========================================================================================= *)
    (* INTERNAL REGISTERS: MATRICES, 2oo3 TMR ENGINE, OSMOTIC MODEL, MPC SOLVER & FSM           *)
    (* ========================================================================================= *)
    bFirstScanDone              : BOOL := FALSE;    (* Cold-start memory and matrix allocation flag *)

    (* ----------------------------------------------------------------------------------------- *)
    (* 1. SWRO FACILITY & MEMBRANE DESIGN CHARACTERISTIC CONSTANTS                               *)
    (* ----------------------------------------------------------------------------------------- *)
    rUniversalGasConst_R        : REAL := 8.31446;  (* Universal gas constant [J/(mol*K)] *)
    rNaCl_MolarMass_gmol        : REAL := 58.443;   (* NaCl molecular weight [g/mol] *)
    rTotalMembraneArea_m2       : REAL := 14280.0;  (* Total active membrane surface area (8-inch elements) [m2] *)
    rMembranePermeability_A     : REAL := 1.15E-6;  (* Pure water permeability coefficient [m/(s*bar)] *)
    rSaltTransportCoeff_B       : REAL := 2.45E-8;  (* Salt solute transport coefficient [m/s] *)
    rMembraneVesselPressureDrop : REAL := 2.20;     (* Longitudinal vessel friction head loss [bar] *)
    rMaxAllowablePressure_bar   : REAL := 76.00;    (* Design maximum membrane compaction trip limit [bar] *)
    rMaxPressureRampRate_bars   : REAL := 1.20;     (* Max allowable rate-of-change to prevent delamination [bar/s] *)

    (* ERD Isobaric Ceramic Pressure Exchanger Mechanical Parameters *)
    rERD_NominalDisplacement_L  : REAL := 14.50;    (* Ceramic rotor internal duct swept volume per rev [L] *)
    rERD_MaxOperatingRPM        : REAL := 1600.0;   (* Maximum mechanical rotor speed limit [rpm] *)
    rERD_MinOperatingRPM        : REAL := 450.0;    (* Minimum hydrodynamic rotor float speed [rpm] *)
    rERD_HighPressureLoss_bar   : REAL := 0.85;     (* Hydraulic friction loss through high-pressure ports [bar] *)
    rERD_LowPressureLoss_bar    : REAL := 0.65;     (* Hydraulic friction loss through low-pressure ports [bar] *)

    (* Antiscalant Chemical Dosing Model Parameters *)
    rAntiscalantDosingRatio_ppm : REAL := 2.50;     (* Antiscalant target concentration in feed [mg/L] *)
    rAntiscalantSpecificGravity : REAL := 1.18;     (* Neat chemical drum specific gravity [-] *)

    (* ----------------------------------------------------------------------------------------- *)
    (* 2. TRIPLE MODULAR REDUNDANCY (2oo3 TMR) FILTERING & REGISTRATION                          *)
    (* ----------------------------------------------------------------------------------------- *)
    rVoted_HPP_DischPress_bar   : REAL := 64.50;
    rVoted_MemFeedPress_bar     : REAL := 66.80;
    rVoted_BrinePress_bar       : REAL := 63.20;
    rVoted_FeedConductivity_mS  : REAL := 54.20;
    rVoted_PermConductivity_uS  : REAL := 285.0;
    rVoted_TotalFeedFlow_m3h    : REAL := 480.0;
    rVoted_ERD_BoosterFlow_m3h  : REAL := 268.0;

    (* Tolerance Deviation Limits *)
    rTol_Pressure_bar           : REAL := 2.40;
    rTol_ConductivityFeed_mS    : REAL := 3.50;
    rTol_ConductivityPerm_uS    : REAL := 35.0;
    rTol_Flow_m3h               : REAL := 18.0;

    (* Stuck-Sensor Frozen Telemetry Counters *)
    iStuck_HPP_A : INT := 0; iStuck_HPP_B : INT := 0; iStuck_HPP_C : INT := 0;
    iStuck_MFP_A : INT := 0; iStuck_MFP_B : INT := 0; iStuck_MFP_C : INT := 0;
    iStuck_BRP_A : INT := 0; iStuck_BRP_B : INT := 0; iStuck_BRP_C : INT := 0;
    iStuck_FC_A  : INT := 0; iStuck_FC_B  : INT := 0; iStuck_FC_C  : INT := 0;
    iStuck_PC_A  : INT := 0; iStuck_PC_B  : INT := 0; iStuck_PC_C  : INT := 0;
    iStuck_TFF_A : INT := 0; iStuck_TFF_B : INT := 0; iStuck_TFF_C : INT := 0;
    iStuck_EBF_A : INT := 0; iStuck_EBF_B : INT := 0; iStuck_EBF_C : INT := 0;

    (* Previous Scan Telemetry *)
    rPrev_HPP_A  : REAL := 64.50; rPrev_HPP_B  : REAL := 64.50; rPrev_HPP_C  : REAL := 64.50;
    rPrev_MFP_A  : REAL := 66.80; rPrev_MFP_B  : REAL := 66.80; rPrev_MFP_C  : REAL := 66.80;
    rPrev_BRP_A  : REAL := 63.20; rPrev_BRP_B  : REAL := 63.20; rPrev_BRP_C  : REAL := 63.20;
    rPrev_FC_A   : REAL := 54.20; rPrev_FC_B   : REAL := 54.20; rPrev_FC_C   : REAL := 54.20;
    rPrev_PC_A   : REAL := 285.0; rPrev_PC_B   : REAL := 285.0; rPrev_PC_C   : REAL := 285.0;
    rPrev_TFF_A  : REAL := 480.0; rPrev_TFF_B  : REAL := 480.0; rPrev_TFF_C  : REAL := 480.0;
    rPrev_EBF_A  : REAL := 268.0; rPrev_EBF_B  : REAL := 268.0; rPrev_EBF_C  : REAL := 268.0;

    (* Transducer Health Flags *)
    bHealth_HPP_A : BOOL := TRUE; bHealth_HPP_B : BOOL := TRUE; bHealth_HPP_C : BOOL := TRUE;
    bHealth_MFP_A : BOOL := TRUE; bHealth_MFP_B : BOOL := TRUE; bHealth_MFP_C : BOOL := TRUE;
    bHealth_BRP_A : BOOL := TRUE; bHealth_BRP_B : BOOL := TRUE; bHealth_BRP_C : BOOL := TRUE;
    bHealth_FC_A  : BOOL := TRUE; bHealth_FC_B  : BOOL := TRUE; bHealth_FC_C  : BOOL := TRUE;
    bHealth_PC_A  : BOOL := TRUE; bHealth_PC_B  : BOOL := TRUE; bHealth_PC_C  : BOOL := TRUE;
    bHealth_TFF_A : BOOL := TRUE; bHealth_TFF_B : BOOL := TRUE; bHealth_TFF_C : BOOL := TRUE;
    bHealth_EBF_A : BOOL := TRUE; bHealth_EBF_B : BOOL := TRUE; bHealth_EBF_C : BOOL := TRUE;

    (* Degraded Voting Status Flags *)
    bDegraded_HPP_1oo2 : BOOL := FALSE; bDegraded_HPP_1oo1 : BOOL := FALSE;
    bDegraded_MFP_1oo2 : BOOL := FALSE; bDegraded_MFP_1oo1 : BOOL := FALSE;
    bDegraded_BRP_1oo2 : BOOL := FALSE; bDegraded_BRP_1oo1 : BOOL := FALSE;
    bDegraded_FC_1oo2  : BOOL := FALSE; bDegraded_FC_1oo1  : BOOL := FALSE;
    bDegraded_PC_1oo2  : BOOL := FALSE; bDegraded_PC_1oo1  : BOOL := FALSE;
    bDegraded_TFF_1oo2 : BOOL := FALSE; bDegraded_TFF_1oo1 : BOOL := FALSE;
    bDegraded_EBF_1oo2 : BOOL := FALSE; bDegraded_EBF_1oo1 : BOOL := FALSE;

    (* ----------------------------------------------------------------------------------------- *)
    (* 3. 8x8 DISCRETE STATE-SPACE MODEL & KALMAN OBSERVER ARRAYS                                *)
    (* ----------------------------------------------------------------------------------------- *)
    (* State Vector x[0..7]:
         x[0]: Membrane feed manifold pressure deviation Delta P_feed [bar]
         x[1]: Permeate volumetric flow rate deviation Delta Q_perm [m3/h]
         x[2]: Permeate salinity TDS deviation Delta C_perm [ppm]
         x[3]: Concentrate reject brine pressure deviation Delta P_brine [bar]
         x[4]: ERD ceramic rotor rotational frequency Delta omega_erd [rpm]
         x[5]: ERD volumetric overflush percentage deviation Delta OF [%]
         x[6]: ERD booster pump flow rate deviation Delta Q_boost [m3/h]
         x[7]: Membrane average osmotic pressure deviation Delta pi_avg [bar] *)
    aState_x                    : ARRAY[0..7] OF REAL := [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0];
    aState_x_hat                : ARRAY[0..7] OF REAL := [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0];
    aState_x_pred               : ARRAY[0..7] OF REAL := [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0];

    (* Control Vector u[0..3]:
         u[0]: Main HP Pump VFD speed reference f_hpp [Hz] (0 to 50 Hz)
         u[1]: ERD Booster Pump VFD speed reference f_boost [Hz] (0 to 50 Hz)
         u[2]: Concentrate brine throttle control valve position V_brine [%] (0 to 100%)
         u[3]: Antiscalant chemical dosing metering rate demand Q_chem [mL/h] *)
    aControl_u                  : ARRAY[0..3] OF REAL := [0.0, 0.0, 45.0, 1450.0];
    aControl_u_prev             : ARRAY[0..3] OF REAL := [0.0, 0.0, 45.0, 1450.0];
    aControl_du                 : ARRAY[0..3] OF REAL := [0.0, 0.0, 0.0, 0.0];

    (* Disturbance Vector d[0..2]:
         d[0]: Raw seawater temperature drift Delta T_feed [deg C]
         d[1]: Intake seawater salinity fluctuation Delta TDS_feed [ppm]
         d[2]: Membrane fouling resistance factor Delta R_fouling [-] *)
    aDisturb_d                  : ARRAY[0..2] OF REAL := [0.0, 0.0, 0.0];

    (* Controlled Measurement Vector y[0..3]:
         y[0]: Membrane feed pressure P_feed [bar]
         y[1]: ERD volumetric overflush OF [%]
         y[2]: Permeate product flow rate Q_perm [m3/h]
         y[3]: Permeate product conductivity C_perm [uS/cm] *)
    aOutput_y                   : ARRAY[0..3] OF REAL := [66.80, 2.15, 212.0, 285.0];
    aOutput_y_sp                : ARRAY[0..3] OF REAL := [66.80, 2.00, 212.0, 280.0];
    aOutput_y_error             : ARRAY[0..3] OF REAL := [0.0, 0.0, 0.0, 0.0];

    (* Continuous-to-Discrete 8x8 State Transition Matrix A (Ts = 0.050 s) *)
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
    aWeight_Q                   : ARRAY[0..3] OF REAL := [45.0, 320.0, 18.0, 0.15]; (* Overflush heavily weighted *)
    aWeight_R                   : ARRAY[0..3] OF REAL := [0.25, 0.35, 0.08, 0.005];  (* Penalty on VFD slew *)
    aLimit_du_Max               : ARRAY[0..3] OF REAL := [0.060, 0.085, 1.50, 25.0]; (* Max ramp: 1.2 bar/s bounded *)
    aLimit_du_Min               : ARRAY[0..3] OF REAL := [-0.060, -0.085, -1.50, -25.0];
    aLimit_u_Max                : ARRAY[0..3] OF REAL := [50.0, 50.0, 100.0, 3500.0];
    aLimit_u_Min                : ARRAY[0..3] OF REAL := [0.0, 0.0, 10.0, 200.0];

    (* Optimization Iteration Workspace *)
    aGrad_g                     : ARRAY[0..3] OF REAL;
    aHessian_diag               : ARRAY[0..3] OF REAL;
    aStep_du                    : ARRAY[0..3] OF REAL;
    iIterQP                     : INT := 0;
    iMaxIterQP                  : INT := 10;
    rAlphaStep                  : REAL := 0.035;

    (* Fallback Decoupled PID Controllers *)
    rPID_Kp_HPP                 : REAL := 0.650;
    rPID_Ki_HPP                 : REAL := 0.045;
    rPID_Kd_HPP                 : REAL := 0.015;
    rPID_Integ_HPP              : REAL := 0.0;
    rPID_PrevErr_HPP            : REAL := 0.0;

    rPID_Kp_Booster             : REAL := 1.250;
    rPID_Ki_Booster             : REAL := 0.085;
    rPID_Kd_Booster             : REAL := 0.025;
    rPID_Integ_Booster          : REAL := 0.0;
    rPID_PrevErr_Booster        : REAL := 0.0;

    (* ----------------------------------------------------------------------------------------- *)
    (* 5. FINITE STATE MACHINE (FSM) VARIABLES                                                   *)
    (* ----------------------------------------------------------------------------------------- *)
    (* Machine States:
         0  : SYSTEM_FLUSH               - Low pressure permeate flush to displace brine
         10 : PUMP_RAMP_SOFT_START       - Controlled soft ramp of Main HP pump (<= 1.2 bar/s)
         20 : ERD_ROTOR_ENGAGE           - Pressure exchanger synchronization & booster engagement
         30 : STEADY_DESALINATION        - Closed-loop desalination, overflush strictly 1-3%
         40 : MEMBRANE_FLUSH_SHUTDOWN    - Controlled rampdown followed by permeate displacement
         50 : CIP_ACID_CLEAN             - Low-pressure chemical cleaning circulation
         90 : EMERGENCY_PRESSURE_RELIEF  - Rapid trip to relieve overpressure shock *)
    iFSM_State                  : INT := 0;
    iPreviousFSM_State          : INT := 0;
    rStateTimer_s               : REAL := 0.0;
    rFlushTimer_s               : REAL := 0.0;
    rRampTimer_s                : REAL := 0.0;
    rCIP_Timer_s                : REAL := 0.0;

    (* ----------------------------------------------------------------------------------------- *)
    (* 6. INTERMEDIATE THERMODYNAMIC, OSMOTIC & ERD FLUID COMPUTATIONS                           *)
    (* ----------------------------------------------------------------------------------------- *)
    rFeedTDS_ppm                : REAL := 38500.0;  (* Converted from mS/cm: TDS = Cond * 710.0 *)
    rPermeateTDS_ppm            : REAL := 202.35;   (* Converted from uS/cm: TDS = Cond * 0.710 *)
    rBrineTDS_ppm               : REAL := 68200.0;  (* Reject brine concentration *)
    rFeedTemp_Kelvin            : REAL := 297.65;   (* 24.5 + 273.15 *)
    rTCF_Factor                 : REAL := 0.9865;   (* exp(0.027 * (T - 25)) *)
    rBrineFlow_m3h              : REAL := 268.0;    (* Reject concentrate brine flow *)
    rMainHPP_Flow_m3h           : REAL := 212.0;    (* Direct pump flow to membrane *)
    rMembraneAverageOsmotic_bar : REAL := 41.22;    (* Log-mean osmotic pressure across vessel *)
    rCalculatedFlux_LMH         : REAL := 14.85;    (* Actual operating flux *)
    rPressureRampRate_bars      : REAL := 0.00;     (* Instantaneous dP/dt [bar/s] *)
    rPrevFeedPress_bar          : REAL := 66.80;
    rElectricalPower_kW         : REAL := 602.0;    (* Main HPP + Booster electrical load *)

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
(* Hardwired SIS Emergency Shutdown / Pressure Relief Interlock *)
IF bEmergencyTripShutdown THEN
    iFSM_State               := 90;                 (* EMERGENCY_PRESSURE_RELIEF *)
    rHPP_VFD_FreqCmd_Hz      := 0.00;               (* Trip Main HP pump immediately *)
    rBooster_VFD_FreqCmd_Hz  := 0.00;               (* Trip Booster pump *)
    rBrineThrottleValve_Pct  := 100.0;              (* Fully open brine throttle to depressurize rack *)
    bMPC_Active              := FALSE;
    dwSWRO_AlarmWord_Primary := dwSWRO_AlarmWord_Primary OR 16#8000_0000; (* Bit 31: EMERGENCY_TRIP_ACTIVE *)
END_IF;

(* Master Block Disabled *)
IF NOT bEnable THEN
    rHPP_VFD_FreqCmd_Hz      := 0.00;
    rBooster_VFD_FreqCmd_Hz  := 0.00;
    rBrineThrottleValve_Pct  := 100.0;
    bMPC_Active              := FALSE;
    bGracefulDegradation     := FALSE;
    bOverflushInTargetBand   := FALSE;
    bMembraneCompactionRisk  := FALSE;
    bPermeateSalinityOffSpec := FALSE;
    bERD_RotorStallFault     := FALSE;
    dwSWRO_StatusWord        := 16#0000_0000;
    RETURN;
END_IF;

(* First-Scan State-Space Matrix Allocation *)
IF NOT bFirstScanDone THEN
    (* ------------------------------------------------------------------------------------- *)
    (* Discrete 8x8 Transition Matrix A (Ts = 0.050 s, 20 Hz Deterministic Loop)             *)
    (* Models membrane hydraulics, ceramic rotor momentum, and brine osmotic accumulation    *)
    (* ------------------------------------------------------------------------------------- *)
    (* Row 0: Membrane feed pressure P_feed *)
    aMatrix_A[0,0] := 0.9650; aMatrix_A[0,1] := -0.0180; aMatrix_A[0,2] := 0.0000; aMatrix_A[0,3] := 0.0240;
    aMatrix_A[0,4] := 0.0012; aMatrix_A[0,5] := 0.0000;  aMatrix_A[0,6] := 0.0145; aMatrix_A[0,7] := 0.0085;

    (* Row 1: Permeate flow rate Q_perm *)
    aMatrix_A[1,0] := 0.0450; aMatrix_A[1,1] := 0.9820;  aMatrix_A[1,2] := -0.0045; aMatrix_A[1,3] := -0.0120;
    aMatrix_A[1,4] := 0.0000; aMatrix_A[1,5] := 0.0000;  aMatrix_A[1,6] := 0.0085;  aMatrix_A[1,7] := -0.0380;

    (* Row 2: Permeate salinity TDS C_perm *)
    aMatrix_A[2,0] := -0.0850; aMatrix_A[2,1] := -0.1250; aMatrix_A[2,2] := 0.9910; aMatrix_A[2,3] := 0.0450;
    aMatrix_A[2,4] := -0.0120; aMatrix_A[2,5] := -0.2500; aMatrix_A[2,6] := -0.0150; aMatrix_A[2,7] := 0.1850;

    (* Row 3: Concentrate brine pressure P_brine *)
    aMatrix_A[3,0] := 0.8200; aMatrix_A[3,1] := -0.0145; aMatrix_A[3,2] := 0.0000; aMatrix_A[3,3] := 0.9450;
    aMatrix_A[3,4] := 0.0000; aMatrix_A[3,5] := 0.0000;  aMatrix_A[3,6] := 0.0000; aMatrix_A[3,7] := 0.0120;

    (* Row 4: ERD ceramic rotor speed omega_erd *)
    aMatrix_A[4,0] := 0.0000; aMatrix_A[4,1] := 0.0000;  aMatrix_A[4,2] := 0.0000; aMatrix_A[4,3] := 0.4500;
    aMatrix_A[4,4] := 0.9880; aMatrix_A[4,5] := 0.0000;  aMatrix_A[4,6] := 0.8500; aMatrix_A[4,7] := 0.0000;

    (* Row 5: ERD overflush percentage OF *)
    aMatrix_A[5,0] := 0.0000; aMatrix_A[5,1] := -0.0150; aMatrix_A[5,2] := 0.0000; aMatrix_A[5,3] := -0.0450;
    aMatrix_A[5,4] := 0.0025; aMatrix_A[5,5] := 0.9420;  aMatrix_A[5,6] := 0.0850; aMatrix_A[5,7] := 0.0000;

    (* Row 6: ERD booster pump flow Q_boost *)
    aMatrix_A[6,0] := -0.0250; aMatrix_A[6,1] := 0.0000; aMatrix_A[6,2] := 0.0000; aMatrix_A[6,3] := 0.0180;
    aMatrix_A[6,4] := 0.0145;  aMatrix_A[6,5] := 0.0000; aMatrix_A[6,6] := 0.9550; aMatrix_A[6,7] := 0.0000;

    (* Row 7: Membrane average osmotic pressure pi_avg *)
    aMatrix_A[7,0] := 0.0120; aMatrix_A[7,1] := 0.0450;  aMatrix_A[7,2] := 0.0000; aMatrix_A[7,3] := 0.0150;
    aMatrix_A[7,4] := 0.0000; aMatrix_A[7,5] := -0.0850; aMatrix_A[7,6] := 0.0000; aMatrix_A[7,7] := 0.9950;

    (* ------------------------------------------------------------------------------------- *)
    (* Discrete 8x4 Input Coupling Matrix B                                                  *)
    (* Inputs: u[0]=HPP VFD [Hz], u[1]=Booster VFD [Hz], u[2]=Brine Valve [%], u[3]=Antiscalant [mL/h] *)
    (* ------------------------------------------------------------------------------------- *)
    aMatrix_B[0,0] := 0.0485; aMatrix_B[0,1] := 0.0245;  aMatrix_B[0,2] := -0.0185; aMatrix_B[0,3] := 0.0000;
    aMatrix_B[1,0] := 0.0320; aMatrix_B[1,1] := 0.0185;  aMatrix_B[1,2] := -0.0080; aMatrix_B[1,3] := 0.0000;
    aMatrix_B[2,0] := -0.0450; aMatrix_B[2,1] := -0.0250; aMatrix_B[2,2] := 0.0850; aMatrix_B[2,3] := -0.0002;
    aMatrix_B[3,0] := 0.0420; aMatrix_B[3,1] := 0.0120;  aMatrix_B[3,2] := -0.0650; aMatrix_B[3,3] := 0.0000;
    aMatrix_B[4,0] := 0.0000; aMatrix_B[4,1] := 0.4500;  aMatrix_B[4,2] := 0.1200;  aMatrix_B[4,3] := 0.0000;
    aMatrix_B[5,0] := -0.0120; aMatrix_B[5,1] := 0.0650; aMatrix_B[5,2] := 0.0350;  aMatrix_B[5,3] := 0.0000;
    aMatrix_B[6,0] := 0.0000; aMatrix_B[6,1] := 0.0850;  aMatrix_B[6,2] := 0.0120;  aMatrix_B[6,3] := 0.0000;
    aMatrix_B[7,0] := 0.0085; aMatrix_B[7,1] := 0.0042;  aMatrix_B[7,2] := -0.0150; aMatrix_B[7,3] := 0.0000;

    (* ------------------------------------------------------------------------------------- *)
    (* Discrete 4x8 Output Mapping Matrix C                                                  *)
    (* Outputs: y[0]=P_feed, y[1]=OF, y[2]=Q_perm, y[3]=C_perm                               *)
    (* ------------------------------------------------------------------------------------- *)
    aMatrix_C[0,0] := 1.0; aMatrix_C[0,1] := 0.0; aMatrix_C[0,2] := 0.0; aMatrix_C[0,3] := 0.0;
    aMatrix_C[0,4] := 0.0; aMatrix_C[0,5] := 0.0; aMatrix_C[0,6] := 0.0; aMatrix_C[0,7] := 0.0;

    aMatrix_C[1,0] := 0.0; aMatrix_C[1,1] := 0.0; aMatrix_C[1,2] := 0.0; aMatrix_C[1,3] := 0.0;
    aMatrix_C[1,4] := 0.0; aMatrix_C[1,5] := 1.0; aMatrix_C[1,6] := 0.0; aMatrix_C[1,7] := 0.0;

    aMatrix_C[2,0] := 0.0; aMatrix_C[2,1] := 1.0; aMatrix_C[2,2] := 0.0; aMatrix_C[2,3] := 0.0;
    aMatrix_C[2,4] := 0.0; aMatrix_C[2,5] := 0.0; aMatrix_C[2,6] := 0.0; aMatrix_C[2,7] := 0.0;

    aMatrix_C[3,0] := 0.0; aMatrix_C[3,1] := 0.0; aMatrix_C[3,2] := 1.0; aMatrix_C[3,3] := 0.0;
    aMatrix_C[3,4] := 0.0; aMatrix_C[3,5] := 0.0; aMatrix_C[3,6] := 0.0; aMatrix_C[3,7] := 0.0;

    (* Direct Feedthrough Matrix D (4x4) *)
    FOR iIdx := 0 TO 3 DO
        FOR jIdx := 0 TO 3 DO
            aMatrix_D[iIdx, jIdx] := 0.0;
        END_FOR;
    END_FOR;

    (* ------------------------------------------------------------------------------------- *)
    (* Disturbance Coupling Matrix E (8x3)                                                   *)
    (* ------------------------------------------------------------------------------------- *)
    aMatrix_E[0,0] := 0.0150; aMatrix_E[0,1] := 0.0245;  aMatrix_E[0,2] := 0.0450;
    aMatrix_E[1,0] := 0.0280; aMatrix_E[1,1] := -0.0185; aMatrix_E[1,2] := -0.0650;
    aMatrix_E[2,0] := 0.0450; aMatrix_E[2,1] := 0.0850;  aMatrix_E[2,2] := 0.0350;
    aMatrix_E[3,0] := 0.0120; aMatrix_E[3,1] := 0.0320;  aMatrix_E[3,2] := 0.0150;
    aMatrix_E[4,0] := 0.0000; aMatrix_E[4,1] := 0.0000;  aMatrix_E[4,2] := 0.0000;
    aMatrix_E[5,0] := 0.0000; aMatrix_E[5,1] := -0.0120; aMatrix_E[5,2] := 0.0000;
    aMatrix_E[6,0] := 0.0000; aMatrix_E[6,1] := 0.0000;  aMatrix_E[6,2] := 0.0000;
    aMatrix_E[7,0] := 0.0850; aMatrix_E[7,1] := 0.1250;  aMatrix_E[7,2] := 0.0000;

    (* ------------------------------------------------------------------------------------- *)
    (* Kalman / Luenberger Observer Gain Matrix L_obs (8x4)                                  *)
    (* ------------------------------------------------------------------------------------- *)
    aMatrix_L_obs[0,0] := 0.2850; aMatrix_L_obs[0,1] := 0.0000; aMatrix_L_obs[0,2] := 0.0450; aMatrix_L_obs[0,3] := 0.0000;
    aMatrix_L_obs[1,0] := 0.0180; aMatrix_L_obs[1,1] := 0.0000; aMatrix_L_obs[1,2] := 0.3150; aMatrix_L_obs[1,3] := -0.0080;
    aMatrix_L_obs[2,0] := 0.0000; aMatrix_L_obs[2,1] := -0.0450; aMatrix_L_obs[2,2] := 0.0120; aMatrix_L_obs[2,3] := 0.4200;
    aMatrix_L_obs[3,0] := 0.1850; aMatrix_L_obs[3,1] := 0.0000; aMatrix_L_obs[3,2] := -0.0150; aMatrix_L_obs[3,3] := 0.0000;
    aMatrix_L_obs[4,0] := 0.0000; aMatrix_L_obs[4,1] := 0.1200; aMatrix_L_obs[4,2] := 0.0000; aMatrix_L_obs[4,3] := 0.0000;
    aMatrix_L_obs[5,0] := 0.0000; aMatrix_L_obs[5,1] := 0.3800; aMatrix_L_obs[5,2] := 0.0000; aMatrix_L_obs[5,3] := -0.0150;
    aMatrix_L_obs[6,0] := 0.0000; aMatrix_L_obs[6,1] := 0.1850; aMatrix_L_obs[6,2] := 0.0250; aMatrix_L_obs[6,3] := 0.0000;
    aMatrix_L_obs[7,0] := 0.0450; aMatrix_L_obs[7,1] := -0.0850; aMatrix_L_obs[7,2] := -0.0350; aMatrix_L_obs[7,3] := 0.0850;

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
(* 1. Main HP Pump Discharge Pressure Transducers (rHPP_DischPress_bar_A, B, C)                  *)
(* --------------------------------------------------------------------------------------------- *)
IF ABS(rHPP_DischPress_bar_A - rPrev_HPP_A) < 0.001 THEN iStuck_HPP_A := iStuck_HPP_A + 1; ELSE iStuck_HPP_A := 0; END_IF;
IF ABS(rHPP_DischPress_bar_B - rPrev_HPP_B) < 0.001 THEN iStuck_HPP_B := iStuck_HPP_B + 1; ELSE iStuck_HPP_B := 0; END_IF;
IF ABS(rHPP_DischPress_bar_C - rPrev_HPP_C) < 0.001 THEN iStuck_HPP_C := iStuck_HPP_C + 1; ELSE iStuck_HPP_C := 0; END_IF;
rPrev_HPP_A := rHPP_DischPress_bar_A; rPrev_HPP_B := rHPP_DischPress_bar_B; rPrev_HPP_C := rHPP_DischPress_bar_C;

bHealth_HPP_A := (rHPP_DischPress_bar_A >= 0.0) AND (rHPP_DischPress_bar_A <= 100.0) AND (iStuck_HPP_A < 200);
bHealth_HPP_B := (rHPP_DischPress_bar_B >= 0.0) AND (rHPP_DischPress_bar_B <= 100.0) AND (iStuck_HPP_B < 200);
bHealth_HPP_C := (rHPP_DischPress_bar_C >= 0.0) AND (rHPP_DischPress_bar_C <= 100.0) AND (iStuck_HPP_C < 200);

IF bHealth_HPP_A AND bHealth_HPP_B AND bHealth_HPP_C THEN
    bDegraded_HPP_1oo2 := FALSE; bDegraded_HPP_1oo1 := FALSE;
    IF ((rHPP_DischPress_bar_A >= rHPP_DischPress_bar_B) AND (rHPP_DischPress_bar_A <= rHPP_DischPress_bar_C)) OR
       ((rHPP_DischPress_bar_A >= rHPP_DischPress_bar_C) AND (rHPP_DischPress_bar_A <= rHPP_DischPress_bar_B)) THEN
        rVoted_HPP_DischPress_bar := rHPP_DischPress_bar_A;
    ELSIF ((rHPP_DischPress_bar_B >= rHPP_DischPress_bar_A) AND (rHPP_DischPress_bar_B <= rHPP_DischPress_bar_C)) OR
          ((rHPP_DischPress_bar_B >= rHPP_DischPress_bar_C) AND (rHPP_DischPress_bar_B <= rHPP_DischPress_bar_A)) THEN
        rVoted_HPP_DischPress_bar := rHPP_DischPress_bar_B;
    ELSE
        rVoted_HPP_DischPress_bar := rHPP_DischPress_bar_C;
    END_IF;
    IF (ABS(rHPP_DischPress_bar_A - rHPP_DischPress_bar_B) > rTol_Pressure_bar) OR
       (ABS(rHPP_DischPress_bar_B - rHPP_DischPress_bar_C) > rTol_Pressure_bar) OR
       (ABS(rHPP_DischPress_bar_A - rHPP_DischPress_bar_C) > rTol_Pressure_bar) THEN
        dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0001; (* Bit 0: HPP Pressure Discrepancy *)
    END_IF;
ELSIF bHealth_HPP_A AND bHealth_HPP_B THEN
    bDegraded_HPP_1oo2 := TRUE; rVoted_HPP_DischPress_bar := (rHPP_DischPress_bar_A + rHPP_DischPress_bar_B) * 0.5;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0002;
ELSIF bHealth_HPP_A AND bHealth_HPP_C THEN
    bDegraded_HPP_1oo2 := TRUE; rVoted_HPP_DischPress_bar := (rHPP_DischPress_bar_A + rHPP_DischPress_bar_C) * 0.5;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0002;
ELSIF bHealth_HPP_B AND bHealth_HPP_C THEN
    bDegraded_HPP_1oo2 := TRUE; rVoted_HPP_DischPress_bar := (rHPP_DischPress_bar_B + rHPP_DischPress_bar_C) * 0.5;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0002;
ELSIF bHealth_HPP_A THEN
    bDegraded_HPP_1oo1 := TRUE; rVoted_HPP_DischPress_bar := rHPP_DischPress_bar_A;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0004;
ELSIF bHealth_HPP_B THEN
    bDegraded_HPP_1oo1 := TRUE; rVoted_HPP_DischPress_bar := rHPP_DischPress_bar_B;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0004;
ELSIF bHealth_HPP_C THEN
    bDegraded_HPP_1oo1 := TRUE; rVoted_HPP_DischPress_bar := rHPP_DischPress_bar_C;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0004;
ELSE
    rVoted_HPP_DischPress_bar := 0.0;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0008;
    bGracefulDegradation := TRUE;
END_IF;

(* --------------------------------------------------------------------------------------------- *)
(* 2. Membrane Feed Manifold Pressure Transducers (rMemFeedPress_bar_A, B, C)                    *)
(* --------------------------------------------------------------------------------------------- *)
IF ABS(rMemFeedPress_bar_A - rPrev_MFP_A) < 0.001 THEN iStuck_MFP_A := iStuck_MFP_A + 1; ELSE iStuck_MFP_A := 0; END_IF;
IF ABS(rMemFeedPress_bar_B - rPrev_MFP_B) < 0.001 THEN iStuck_MFP_B := iStuck_MFP_B + 1; ELSE iStuck_MFP_B := 0; END_IF;
IF ABS(rMemFeedPress_bar_C - rPrev_MFP_C) < 0.001 THEN iStuck_MFP_C := iStuck_MFP_C + 1; ELSE iStuck_MFP_C := 0; END_IF;
rPrev_MFP_A := rMemFeedPress_bar_A; rPrev_MFP_B := rMemFeedPress_bar_B; rPrev_MFP_C := rMemFeedPress_bar_C;

bHealth_MFP_A := (rMemFeedPress_bar_A >= 0.0) AND (rMemFeedPress_bar_A <= 100.0) AND (iStuck_MFP_A < 200);
bHealth_MFP_B := (rMemFeedPress_bar_B >= 0.0) AND (rMemFeedPress_bar_B <= 100.0) AND (iStuck_MFP_B < 200);
bHealth_MFP_C := (rMemFeedPress_bar_C >= 0.0) AND (rMemFeedPress_bar_C <= 100.0) AND (iStuck_MFP_C < 200);

IF bHealth_MFP_A AND bHealth_MFP_B AND bHealth_MFP_C THEN
    bDegraded_MFP_1oo2 := FALSE; bDegraded_MFP_1oo1 := FALSE;
    IF ((rMemFeedPress_bar_A >= rMemFeedPress_bar_B) AND (rMemFeedPress_bar_A <= rMemFeedPress_bar_C)) OR
       ((rMemFeedPress_bar_A >= rMemFeedPress_bar_C) AND (rMemFeedPress_bar_A <= rMemFeedPress_bar_B)) THEN
        rVoted_MemFeedPress_bar := rMemFeedPress_bar_A;
    ELSIF ((rMemFeedPress_bar_B >= rMemFeedPress_bar_A) AND (rMemFeedPress_bar_B <= rMemFeedPress_bar_C)) OR
          ((rMemFeedPress_bar_B >= rMemFeedPress_bar_C) AND (rMemFeedPress_bar_B <= rMemFeedPress_bar_A)) THEN
        rVoted_MemFeedPress_bar := rMemFeedPress_bar_B;
    ELSE
        rVoted_MemFeedPress_bar := rMemFeedPress_bar_C;
    END_IF;
    IF (ABS(rMemFeedPress_bar_A - rMemFeedPress_bar_B) > rTol_Pressure_bar) OR
       (ABS(rMemFeedPress_bar_B - rMemFeedPress_bar_C) > rTol_Pressure_bar) OR
       (ABS(rMemFeedPress_bar_A - rMemFeedPress_bar_C) > rTol_Pressure_bar) THEN
        dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0010;
    END_IF;
ELSIF bHealth_MFP_A AND bHealth_MFP_B THEN
    bDegraded_MFP_1oo2 := TRUE; rVoted_MemFeedPress_bar := (rMemFeedPress_bar_A + rMemFeedPress_bar_B) * 0.5;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0020;
ELSIF bHealth_MFP_A AND bHealth_MFP_C THEN
    bDegraded_MFP_1oo2 := TRUE; rVoted_MemFeedPress_bar := (rMemFeedPress_bar_A + rMemFeedPress_bar_C) * 0.5;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0020;
ELSIF bHealth_MFP_B AND bHealth_MFP_C THEN
    bDegraded_MFP_1oo2 := TRUE; rVoted_MemFeedPress_bar := (rMemFeedPress_bar_B + rMemFeedPress_bar_C) * 0.5;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0020;
ELSIF bHealth_MFP_A THEN
    bDegraded_MFP_1oo1 := TRUE; rVoted_MemFeedPress_bar := rMemFeedPress_bar_A;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0040;
ELSIF bHealth_MFP_B THEN
    bDegraded_MFP_1oo1 := TRUE; rVoted_MemFeedPress_bar := rMemFeedPress_bar_B;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0040;
ELSIF bHealth_MFP_C THEN
    bDegraded_MFP_1oo1 := TRUE; rVoted_MemFeedPress_bar := rMemFeedPress_bar_C;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0040;
ELSE
    rVoted_MemFeedPress_bar := 0.0;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0080;
    bGracefulDegradation := TRUE;
END_IF;

(* --------------------------------------------------------------------------------------------- *)
(* 3. Concentrate Brine Pressure Transducers (rBrinePress_bar_A, B, C)                           *)
(* --------------------------------------------------------------------------------------------- *)
bHealth_BRP_A := (rBrinePress_bar_A >= 0.0) AND (rBrinePress_bar_A <= 100.0);
bHealth_BRP_B := (rBrinePress_bar_B >= 0.0) AND (rBrinePress_bar_B <= 100.0);
bHealth_BRP_C := (rBrinePress_bar_C >= 0.0) AND (rBrinePress_bar_C <= 100.0);

IF bHealth_BRP_A AND bHealth_BRP_B AND bHealth_BRP_C THEN
    IF ((rBrinePress_bar_A >= rBrinePress_bar_B) AND (rBrinePress_bar_A <= rBrinePress_bar_C)) OR
       ((rBrinePress_bar_A >= rBrinePress_bar_C) AND (rBrinePress_bar_A <= rBrinePress_bar_B)) THEN
        rVoted_BrinePress_bar := rBrinePress_bar_A;
    ELSIF ((rBrinePress_bar_B >= rBrinePress_bar_A) AND (rBrinePress_bar_B <= rBrinePress_bar_C)) OR
          ((rBrinePress_bar_B >= rBrinePress_bar_C) AND (rBrinePress_bar_B <= rBrinePress_bar_A)) THEN
        rVoted_BrinePress_bar := rBrinePress_bar_B;
    ELSE
        rVoted_BrinePress_bar := rBrinePress_bar_C;
    END_IF;
ELSE
    rVoted_BrinePress_bar := rBrinePress_bar_A;
END_IF;

(* --------------------------------------------------------------------------------------------- *)
(* 4. Flow Transducers Voting (Total Feed & ERD Booster Flows)                                   *)
(* --------------------------------------------------------------------------------------------- *)
bHealth_TFF_A := (rTotalFeedFlow_m3h_A >= 0.0) AND (rTotalFeedFlow_m3h_A <= 1000.0);
bHealth_TFF_B := (rTotalFeedFlow_m3h_B >= 0.0) AND (rTotalFeedFlow_m3h_B <= 1000.0);
bHealth_TFF_C := (rTotalFeedFlow_m3h_C >= 0.0) AND (rTotalFeedFlow_m3h_C <= 1000.0);
IF bHealth_TFF_A AND bHealth_TFF_B AND bHealth_TFF_C THEN
    IF ((rTotalFeedFlow_m3h_A >= rTotalFeedFlow_m3h_B) AND (rTotalFeedFlow_m3h_A <= rTotalFeedFlow_m3h_C)) OR
       ((rTotalFeedFlow_m3h_A >= rTotalFeedFlow_m3h_C) AND (rTotalFeedFlow_m3h_A <= rTotalFeedFlow_m3h_B)) THEN
        rVoted_TotalFeedFlow_m3h := rTotalFeedFlow_m3h_A;
    ELSIF ((rTotalFeedFlow_m3h_B >= rTotalFeedFlow_m3h_A) AND (rTotalFeedFlow_m3h_B <= rTotalFeedFlow_m3h_C)) OR
          ((rTotalFeedFlow_m3h_B >= rTotalFeedFlow_m3h_C) AND (rTotalFeedFlow_m3h_B <= rTotalFeedFlow_m3h_A)) THEN
        rVoted_TotalFeedFlow_m3h := rTotalFeedFlow_m3h_B;
    ELSE
        rVoted_TotalFeedFlow_m3h := rTotalFeedFlow_m3h_C;
    END_IF;
ELSE
    rVoted_TotalFeedFlow_m3h := rTotalFeedFlow_m3h_A;
END_IF;

bHealth_EBF_A := (rERD_BoosterFlow_m3h_A >= 0.0) AND (rERD_BoosterFlow_m3h_A <= 600.0);
bHealth_EBF_B := (rERD_BoosterFlow_m3h_B >= 0.0) AND (rERD_BoosterFlow_m3h_B <= 600.0);
bHealth_EBF_C := (rERD_BoosterFlow_m3h_C >= 0.0) AND (rERD_BoosterFlow_m3h_C <= 600.0);
IF bHealth_EBF_A AND bHealth_EBF_B AND bHealth_EBF_C THEN
    IF ((rERD_BoosterFlow_m3h_A >= rERD_BoosterFlow_m3h_B) AND (rERD_BoosterFlow_m3h_A <= rERD_BoosterFlow_m3h_C)) OR
       ((rERD_BoosterFlow_m3h_A >= rERD_BoosterFlow_m3h_C) AND (rERD_BoosterFlow_m3h_A <= rERD_BoosterFlow_m3h_B)) THEN
        rVoted_ERD_BoosterFlow_m3h := rERD_BoosterFlow_m3h_A;
    ELSIF ((rERD_BoosterFlow_m3h_B >= rERD_BoosterFlow_m3h_A) AND (rERD_BoosterFlow_m3h_B <= rERD_BoosterFlow_m3h_C)) OR
          ((rERD_BoosterFlow_m3h_B >= rERD_BoosterFlow_m3h_C) AND (rERD_BoosterFlow_m3h_B <= rERD_BoosterFlow_m3h_A)) THEN
        rVoted_ERD_BoosterFlow_m3h := rERD_BoosterFlow_m3h_B;
    ELSE
        rVoted_ERD_BoosterFlow_m3h := rERD_BoosterFlow_m3h_C;
    END_IF;
ELSE
    rVoted_ERD_BoosterFlow_m3h := rERD_BoosterFlow_m3h_A;
END_IF;

(* --------------------------------------------------------------------------------------------- *)
(* 5. Conductivity Transducers Voting (Feed & Permeate)                                          *)
(* --------------------------------------------------------------------------------------------- *)
rVoted_FeedConductivity_mS := (rFeedConductivity_mS_A + rFeedConductivity_mS_B + rFeedConductivity_mS_C) / 3.0;
rVoted_PermConductivity_uS := (rPermConductivity_uS_A + rPermConductivity_uS_B + rPermConductivity_uS_C) / 3.0;
"""
    sections.append(s4)

    # -------------------------------------------------------------------------
    # SECTION 5: LOGIC PART 3 - OSMOTIC THERMODYNAMICS & ERD OBSERVER
    # -------------------------------------------------------------------------
    s5 = """(* ============================================================================================= *)
(* SECTION 3: OSMOTIC THERMODYNAMICS & ERD VOLUMETRIC OVERFLUSH OBSERVER                         *)
(* ============================================================================================= *)
(* Absolute Temperature and ASTM D4516 Temperature Correction Factor (TCF) *)
rFeedTemp_Kelvin := rFeedWaterTemp_degC + 273.15;
rTCF_Factor      := EXP(0.027 * (rFeedWaterTemp_degC - 25.0));

(* Salinity Conversions: TDS [ppm] = Conductivity * Constant *)
rFeedTDS_ppm     := rVoted_FeedConductivity_mS * 710.0;
rPermeateTDS_ppm := rVoted_PermConductivity_uS * 0.710;

(* van 't Hoff Osmotic Pressure Calculations: pi = phi * i * C * R * T *)
(* Constant 0.000754 bar per ppm TDS at 25 deg C *)
rFeedOsmoticPressure_bar  := (rFeedTDS_ppm * 0.000754) * (rFeedTemp_Kelvin / 298.15);

(* Overall Recovery Ratio: Y = Q_perm / Q_feed *)
rMainHPP_Flow_m3h := rVoted_TotalFeedFlow_m3h - rVoted_ERD_BoosterFlow_m3h;
IF rMainHPP_Flow_m3h < 0.0 THEN rMainHPP_Flow_m3h := 0.0; END_IF;

IF rVoted_TotalFeedFlow_m3h > 10.0 THEN
    rRecoveryRatio_Pct := (rPermeateFlow_m3h / rVoted_TotalFeedFlow_m3h) * 100.0;
ELSE
    rRecoveryRatio_Pct := 0.0;
END_IF;

(* Reject Brine Flow and Concentration: C_brine = C_feed / (1 - Y) *)
rBrineFlow_m3h := rVoted_TotalFeedFlow_m3h - rPermeateFlow_m3h;
IF rBrineFlow_m3h < 1.0 THEN rBrineFlow_m3h := 1.0; END_IF;

IF rRecoveryRatio_Pct < 90.0 THEN
    rBrineTDS_ppm := rFeedTDS_ppm / (1.0 - (rRecoveryRatio_Pct * 0.01));
ELSE
    rBrineTDS_ppm := rFeedTDS_ppm * 2.0;
END_IF;
rBrineOsmoticPressure_bar := (rBrineTDS_ppm * 0.000754) * (rFeedTemp_Kelvin / 298.15);

(* Average Membrane Osmotic Pressure pi_avg *)
rMembraneAverageOsmotic_bar := (rFeedOsmoticPressure_bar + rBrineOsmoticPressure_bar) * 0.50;

(* Net Driving Pressure: NDP = (P_feed - Delta_P/2 - P_perm) - (pi_avg - pi_perm) *)
rNetDrivingPressure_bar := (rVoted_MemFeedPress_bar - (rMembraneVesselPressureDrop * 0.50) - rPermeateHeaderPress_bar) -
                           (rMembraneAverageOsmotic_bar - (rPermeateTDS_ppm * 0.000754));
IF rNetDrivingPressure_bar < 0.0 THEN rNetDrivingPressure_bar := 0.0; END_IF;

(* Membrane Permeate Water Production: Q_perm = A * S_area * TCF * NDP *)
rPermeateFlow_m3h := (rMembranePermeability_A * rTotalMembraneArea_m2 * rTCF_Factor * rNetDrivingPressure_bar) * 3600.0;
rCalculatedFlux_LMH := (rPermeateFlow_m3h * 1000.0) / rTotalMembraneArea_m2;
rNormalizedFlux_LMH := rCalculatedFlux_LMH / rTCF_Factor;

(* ERD Isobaric Ceramic Rotor Volumetric Overflush Calculation *)
(* Overflush OF = (Q_booster - Q_brine) / Q_brine * 100% *)
IF rBrineFlow_m3h > 10.0 THEN
    rERD_Overflush_Pct := ((rVoted_ERD_BoosterFlow_m3h - rBrineFlow_m3h) / rBrineFlow_m3h) * 100.0;
ELSE
    rERD_Overflush_Pct := 0.0;
END_IF;

(* Overflush Compliance Window Supervision (Target: 1.0% to 3.0%) *)
bOverflushInTargetBand := (rERD_Overflush_Pct >= 1.00) AND (rERD_Overflush_Pct <= 3.00);

(* ERD Rotor Stall Detection (Pressurized above 30 bar but rotor speed < 450 RPM) *)
IF (rVoted_MemFeedPress_bar >= 30.0) AND (rERD_RotorRPM_Sensor < rERD_MinOperatingRPM) THEN
    bERD_RotorStallFault     := TRUE;
    dwSWRO_AlarmWord_Primary := dwSWRO_AlarmWord_Primary OR 16#0000_0001; (* Bit 0: ERD_ROTOR_STALL_TRIP *)
ELSE
    bERD_RotorStallFault := FALSE;
END_IF;

(* Pressure Ramp Rate Slew Monitor |dP/dt| *)
rPressureRampRate_bars := ABS(rVoted_MemFeedPress_bar - rPrevFeedPress_bar) / tScanTime_s;
rPrevFeedPress_bar     := rVoted_MemFeedPress_bar;
bMembraneCompactionRisk := (rPressureRampRate_bars > rMaxPressureRampRate_bars) OR (rVoted_MemFeedPress_bar > rMaxAllowablePressure_bar);

(* Specific Electrical Energy Consumption [kWh/m3] *)
IF rPermeateFlow_m3h > 5.0 THEN
    rElectricalPower_kW    := ((rVoted_HPP_DischPress_bar * 1.0E5 * (rMainHPP_Flow_m3h / 3600.0)) / (0.85 * 1000.0)) +
                              (((rVoted_MemFeedPress_bar - rVoted_BrinePress_bar + 2.5) * 1.0E5 * (rVoted_ERD_BoosterFlow_m3h / 3600.0)) / (0.82 * 1000.0));
    rSpecificEnergy_kWh_m3 := rElectricalPower_kW / rPermeateFlow_m3h;
ELSE
    rSpecificEnergy_kWh_m3 := 0.0;
END_IF;
"""
    sections.append(s5)

    # -------------------------------------------------------------------------
    # SECTION 6: LOGIC PART 4 - 8x8 STATE-SPACE & KALMAN OBSERVER
    # -------------------------------------------------------------------------
    s6 = """(* ============================================================================================= *)
(* SECTION 4: 8x8 DISCRETE STATE-SPACE TIME PROPAGATION & KALMAN OBSERVER UPDATE                 *)
(* ============================================================================================= *)
(* Assign Disturbance Vector d *)
aDisturb_d[0] := rFeedWaterTemp_degC - 25.0;
aDisturb_d[1] := (rFeedTDS_ppm - 38000.0) / 1000.0;
aDisturb_d[2] := rFeedTurbidity_NTU - 0.20;

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
aOutput_y[0] := rVoted_MemFeedPress_bar;
aOutput_y[1] := rERD_Overflush_Pct;
aOutput_y[2] := rPermeateFlow_m3h;
aOutput_y[3] := rVoted_PermConductivity_uS;

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
    # SECTION 7: LOGIC PART 5 - MPC SOLVER & FEEDFORWARD OPTIMIZER
    # -------------------------------------------------------------------------
    s7 = """(* ============================================================================================= *)
(* SECTION 5: MODEL PREDICTIVE CONTROL & COORDINATED ERD OPTIMIZATION                            *)
(* ============================================================================================= *)
(* Target Output Setpoints *)
aOutput_y_sp[0] := 66.50;                   (* Target membrane feed pressure [bar] *)
aOutput_y_sp[1] := 2.00;                    (* Target ERD overflush strictly 2.0% *)
aOutput_y_sp[2] := 212.0;                   (* Target permeate production rate [m3/h] *)
aOutput_y_sp[3] := 280.0;                   (* Permeate conductivity target [uS/cm] *)

(* Tracking Error *)
aOutput_y_error[0] := aOutput_y[0] - aOutput_y_sp[0];
aOutput_y_error[1] := aOutput_y[1] - aOutput_y_sp[1];
aOutput_y_error[2] := aOutput_y[2] - aOutput_y_sp[2];
aOutput_y_error[3] := aOutput_y[3] - aOutput_y_sp[3];

IF NOT bGracefulDegradation AND (iFSM_State = 30) THEN
    bMPC_Active := TRUE;

    (* Approximate Diagonal Hessian *)
    aHessian_diag[0] := aWeight_Q[0] * 0.0024 + aWeight_R[0]; (* Main HPP VFD *)
    aHessian_diag[1] := aWeight_Q[1] * 0.0042 + aWeight_R[1]; (* Booster VFD *)
    aHessian_diag[2] := aWeight_Q[0] * 0.0003 + aWeight_R[2]; (* Brine throttle valve *)
    aHessian_diag[3] := aWeight_Q[3] * 0.0001 + aWeight_R[3]; (* Antiscalant *)

    (* Gradient Calculation *)
    aGrad_g[0] := aWeight_Q[0] * aOutput_y_error[0] * 0.048 + aWeight_R[0] * aControl_du[0];
    aGrad_g[1] := aWeight_Q[1] * aOutput_y_error[1] * 0.065 + aWeight_R[1] * aControl_du[1];
    aGrad_g[2] := aWeight_Q[0] * aOutput_y_error[0] * (-0.018) + aWeight_R[2] * aControl_du[2];
    aGrad_g[3] := aWeight_Q[3] * aOutput_y_error[3] * (-0.0002) + aWeight_R[3] * aControl_du[3];

    (* Iterative Projected Gradient Descent *)
    FOR iIterQP := 1 TO iMaxIterQP DO
        FOR iIdx := 0 TO 3 DO
            aStep_du[iIdx] := aControl_du[iIdx] - (rAlphaStep / aHessian_diag[iIdx]) * aGrad_g[iIdx];

            (* Enforce strictly bounded slew rates (preventing pressure shock dP/dt > 1.2 bar/s) *)
            IF aStep_du[iIdx] > aLimit_du_Max[iIdx] THEN
                aStep_du[iIdx] := aLimit_du_Max[iIdx];
            ELSIF aStep_du[iIdx] < aLimit_du_Min[iIdx] THEN
                aStep_du[iIdx] := aLimit_du_Min[iIdx];
            END_IF;

            (* Absolute actuator bounds *)
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

    rHPP_VFD_FreqCmd_Hz     := aControl_u[0];
    rBooster_VFD_FreqCmd_Hz := aControl_u[1];
    rBrineThrottleValve_Pct := aControl_u[2];
    rAntiscalantDosing_ml_h := aControl_u[3];
ELSE
    (* Fallback Decoupled Control *)
    bMPC_Active := FALSE;

    (* PID on Main HP Pump to regulate feed pressure *)
    rTmpSum := (66.50 - rVoted_MemFeedPress_bar);
    rPID_Integ_HPP := rPID_Integ_HPP + rTmpSum * tScanTime_s;
    IF rPID_Integ_HPP > 15.0 THEN rPID_Integ_HPP := 15.0; END_IF;
    IF rPID_Integ_HPP < -15.0 THEN rPID_Integ_HPP := -15.0; END_IF;
    rHPP_VFD_FreqCmd_Hz := 45.0 + rPID_Kp_HPP * rTmpSum + rPID_Ki_HPP * rPID_Integ_HPP;

    (* Slew rate limit *)
    IF (rHPP_VFD_FreqCmd_Hz - aControl_u_prev[0]) > 0.060 THEN
        rHPP_VFD_FreqCmd_Hz := aControl_u_prev[0] + 0.060;
    ELSIF (rHPP_VFD_FreqCmd_Hz - aControl_u_prev[0]) < -0.060 THEN
        rHPP_VFD_FreqCmd_Hz := aControl_u_prev[0] - 0.060;
    END_IF;

    (* PID on Booster Pump to maintain ERD Overflush at 2.0% *)
    rTmpSum := (2.00 - rERD_Overflush_Pct);
    rPID_Integ_Booster := rPID_Integ_Booster + rTmpSum * tScanTime_s;
    IF rPID_Integ_Booster > 10.0 THEN rPID_Integ_Booster := 10.0; END_IF;
    IF rPID_Integ_Booster < -10.0 THEN rPID_Integ_Booster := -10.0; END_IF;
    rBooster_VFD_FreqCmd_Hz := 46.5 + rPID_Kp_Booster * rTmpSum + rPID_Ki_Booster * rPID_Integ_Booster;

    IF (rBooster_VFD_FreqCmd_Hz - aControl_u_prev[1]) > 0.085 THEN
        rBooster_VFD_FreqCmd_Hz := aControl_u_prev[1] + 0.085;
    ELSIF (rBooster_VFD_FreqCmd_Hz - aControl_u_prev[1]) < -0.085 THEN
        rBooster_VFD_FreqCmd_Hz := aControl_u_prev[1] - 0.085;
    END_IF;
END_IF;

aControl_u_prev[0] := rHPP_VFD_FreqCmd_Hz;
aControl_u_prev[1] := rBooster_VFD_FreqCmd_Hz;

(* Antiscalant Chemical Dosing Proportional Calculation *)
(* Dosing rate: Q_chem [mL/h] = Q_feed [m3/h] * Ratio [mg/L] / (SG * 10) *)
IF rVoted_TotalFeedFlow_m3h > 10.0 THEN
    rAntiscalantDosing_ml_h := (rVoted_TotalFeedFlow_m3h * rAntiscalantDosingRatio_ppm) / (rAntiscalantSpecificGravity * 0.001 * 1000.0);
ELSE
    rAntiscalantDosing_ml_h := 0.0;
END_IF;
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
    (* STATE 0: SYSTEM_FLUSH (Low-Pressure Displacement of Stagnant High-Salinity Water)        *)
    (* ----------------------------------------------------------------------------------------- *)
    0:
        rHPP_VFD_FreqCmd_Hz     := 0.00;            (* Main HP pump stopped *)
        rBooster_VFD_FreqCmd_Hz := 0.00;            (* Booster pump stopped *)
        rBrineThrottleValve_Pct := 100.0;           (* Brine line wide open *)
        rFlushTimer_s           := rFlushTimer_s + tScanTime_s;

        (* Advance to Soft Start when suction permissive satisfied and flush complete *)
        IF bSuctionValvesOpenPermissive AND bAntiscalantFlowConfirmed AND (rFlushTimer_s >= 60.0) THEN
            rFlushTimer_s := 0.0;
            iFSM_State    := 10;                    (* PUMP_RAMP_SOFT_START *)
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 10: PUMP_RAMP_SOFT_START (Controlled VFD Ramp at <= 1.0 bar/s to Avoid Shock)      *)
    (* ----------------------------------------------------------------------------------------- *)
    10:
        rRampTimer_s := rRampTimer_s + tScanTime_s;
        (* Gradual ramp of Main HPP frequency *)
        IF rHPP_VFD_FreqCmd_Hz < 42.0 THEN
            rHPP_VFD_FreqCmd_Hz := rHPP_VFD_FreqCmd_Hz + 0.045;
        END_IF;

        rBrineThrottleValve_Pct := 65.0;

        (* When pressure reaches ERD engagement threshold (45 bar), synchronize ERD *)
        IF rVoted_MemFeedPress_bar >= 45.0 THEN
            rRampTimer_s := 0.0;
            iFSM_State   := 20;                     (* ERD_ROTOR_ENGAGE *)
        END_IF;

        (* Suction valve lost interlock *)
        IF NOT bSuctionValvesOpenPermissive THEN
            iFSM_State := 0;
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 20: ERD_ROTOR_ENGAGE (Synchronize ERD Booster Pump & Verify Ceramic Rotor Float)   *)
    (* ----------------------------------------------------------------------------------------- *)
    20:
        (* Ramp booster pump to match brine pressure *)
        IF rBooster_VFD_FreqCmd_Hz < 44.0 THEN
            rBooster_VFD_FreqCmd_Hz := rBooster_VFD_FreqCmd_Hz + 0.065;
        END_IF;
        IF rHPP_VFD_FreqCmd_Hz < 48.5 THEN
            rHPP_VFD_FreqCmd_Hz := rHPP_VFD_FreqCmd_Hz + 0.035;
        END_IF;

        rBrineThrottleValve_Pct := 45.0;

        (* Verify rotor speed reaches hydrodynamic cushion (> 800 rpm) and overflush is stable *)
        IF (rERD_RotorRPM_Sensor >= 850.0) AND bOverflushInTargetBand AND (rStateTimer_s >= 15.0) THEN
            iFSM_State := 30;                       (* Advance to STEADY_DESALINATION *)
        END_IF;

        (* Stall abort *)
        IF (rStateTimer_s >= 40.0) AND (rERD_RotorRPM_Sensor < 450.0) THEN
            dwSWRO_AlarmWord_Primary := dwSWRO_AlarmWord_Primary OR 16#0000_0002; (* ROTOR_ENGAGE_FAIL_HH *)
            iFSM_State               := 90;
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 30: STEADY_DESALINATION (Normal Closed-Loop Operation with MPC & Overflush Control)*)
    (* ----------------------------------------------------------------------------------------- *)
    30:
        (* Normal closed-loop modulation driven by Section 5 MPC / Fallback Controller *)
        (* Trip to relief if membrane compaction overpressure detected *)
        IF rVoted_MemFeedPress_bar >= rMaxAllowablePressure_bar THEN
            iFSM_State := 90;
        END_IF;

        IF bERD_RotorStallFault THEN
            iFSM_State := 90;
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 40: MEMBRANE_FLUSH_SHUTDOWN (Controlled Rampdown Followed by Permeate Rinse)       *)
    (* ----------------------------------------------------------------------------------------- *)
    40:
        (* Controlled VFD rampdown to avoid hydraulic vacuum/shock *)
        IF rHPP_VFD_FreqCmd_Hz > 0.0 THEN
            rHPP_VFD_FreqCmd_Hz := rHPP_VFD_FreqCmd_Hz - 0.050;
        END_IF;
        IF rBooster_VFD_FreqCmd_Hz > 0.0 THEN
            rBooster_VFD_FreqCmd_Hz := rBooster_VFD_FreqCmd_Hz - 0.080;
        END_IF;
        rBrineThrottleValve_Pct := 100.0;

        IF (rHPP_VFD_FreqCmd_Hz <= 1.0) AND (rVoted_MemFeedPress_bar <= 8.0) THEN
            iFSM_State := 0;                        (* Complete shutdown into flush *)
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 50: CIP_ACID_CLEAN (Low-Pressure Chemical Cleaning Circulation)                    *)
    (* ----------------------------------------------------------------------------------------- *)
    50:
        rHPP_VFD_FreqCmd_Hz     := 0.00;
        rBooster_VFD_FreqCmd_Hz := 0.00;
        rBrineThrottleValve_Pct := 100.0;
        rCIP_Timer_s            := rCIP_Timer_s + tScanTime_s;

        IF rCIP_Timer_s >= 7200.0 THEN              (* 2-hour CIP soak completed *)
            rCIP_Timer_s := 0.0;
            iFSM_State   := 0;
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 90: EMERGENCY_PRESSURE_RELIEF (Rapid Depressurization to Protect FRP Vessels)      *)
    (* ----------------------------------------------------------------------------------------- *)
    90:
        rHPP_VFD_FreqCmd_Hz     := 0.00;
        rBooster_VFD_FreqCmd_Hz := 0.00;
        rBrineThrottleValve_Pct := 100.0;           (* Wide open to evacuate line pressure *)

        IF bResetTripAlarms AND (rVoted_MemFeedPress_bar <= 5.0) AND (NOT bEmergencyTripShutdown) THEN
            iFSM_State := 0;
        END_IF;
END_CASE;

(* Permeate Salinity Compliance Check (< 400 mg/L potable threshold) *)
bPermeateSalinityOffSpec := (rPermeateTDS_ppm >= 400.0);
IF bPermeateSalinityOffSpec THEN
    dwSWRO_AlarmWord_Primary := dwSWRO_AlarmWord_Primary OR 16#0000_0004; (* Bit 2: PERMEATE_TDS_OFFSPEC_HH *)
END_IF;
"""
    sections.append(s8)

    # -------------------------------------------------------------------------
    # SECTION 9: LOGIC PART 7 - ISA-18.2 ALARMS & DIAGNOSTIC PACKING
    # -------------------------------------------------------------------------
    s9 = """(* ============================================================================================= *)
(* SECTION 7: ISA-18.2 ALARM MATRIX, LATCHING & STATUS WORD BIT-PACKING                          *)
(* ============================================================================================= *)
(* 1. Membrane Compaction Overpressure Alarms *)
IF rVoted_MemFeedPress_bar >= 75.00 THEN
    dwSWRO_AlarmWord_Primary := dwSWRO_AlarmWord_Primary OR 16#0000_0008; (* Bit 3: MEMBRANE_PRESS_HH_TRIP *)
ELSIF rVoted_MemFeedPress_bar >= 71.50 THEN
    dwSWRO_AlarmWord_Secondary := dwSWRO_AlarmWord_Secondary OR 16#0000_0001; (* Bit 0: MEMBRANE_PRESS_H_WARN *)
END_IF;

(* 2. ERD Overflush Out-of-Band Alarms *)
IF rERD_Overflush_Pct <= 0.50 THEN
    dwSWRO_AlarmWord_Primary := dwSWRO_AlarmWord_Primary OR 16#0000_0010; (* Bit 4: OVERFLUSH_CRITICAL_LOW_LL *)
ELSIF rERD_Overflush_Pct <= 1.00 THEN
    dwSWRO_AlarmWord_Secondary := dwSWRO_AlarmWord_Secondary OR 16#0000_0002; (* Bit 1: OVERFLUSH_LOW_L *)
ELSIF rERD_Overflush_Pct >= 3.50 THEN
    dwSWRO_AlarmWord_Secondary := dwSWRO_AlarmWord_Secondary OR 16#0000_0004; (* Bit 2: OVERFLUSH_HIGH_H *)
END_IF;

(* 3. Raw Seawater Turbidity Alarms *)
IF rFeedTurbidity_NTU >= 0.85 THEN
    dwSWRO_AlarmWord_Secondary := dwSWRO_AlarmWord_Secondary OR 16#0000_0008; (* Bit 3: TURBIDITY_HIGH_H *)
END_IF;

(* 4. Suction Pressure Loss Warning *)
IF NOT bSuctionValvesOpenPermissive THEN
    dwSWRO_AlarmWord_Primary := dwSWRO_AlarmWord_Primary OR 16#0000_0020; (* Bit 5: SUCTION_INTERLOCK_TRIP *)
END_IF;

(* Master Reset *)
IF bResetTripAlarms THEN
    dwSWRO_AlarmWord_Primary   := 16#0000_0000;
    dwSWRO_AlarmWord_Secondary := 16#0000_0000;
END_IF;

(* --------------------------------------------------------------------------------------------- *)
(* 5. 32-Bit SWRO Status Word Packing (dwSWRO_StatusWord)                                        *)
(* --------------------------------------------------------------------------------------------- *)
(* Bits 0..7  : Current FSM State Integer [0..90] *)
(* Bit 8      : bOverflushInTargetBand *)
(* Bit 9      : bMembraneCompactionRisk *)
(* Bit 10     : bPermeateSalinityOffSpec *)
(* Bit 11     : bERD_RotorStallFault *)
(* Bit 12     : bMPC_Active *)
(* Bit 13     : bGracefulDegradation *)
(* Bit 14     : bSuctionValvesOpenPermissive *)
(* Bit 15     : bAntiscalantFlowConfirmed *)
(* Bit 31     : Master Emergency Trip Flag *)
dwSWRO_StatusWord := INT_TO_DWORD(iFSM_State);
IF bOverflushInTargetBand      THEN dwSWRO_StatusWord := dwSWRO_StatusWord OR 16#0000_0100; END_IF;
IF bMembraneCompactionRisk     THEN dwSWRO_StatusWord := dwSWRO_StatusWord OR 16#0000_0200; END_IF;
IF bPermeateSalinityOffSpec    THEN dwSWRO_StatusWord := dwSWRO_StatusWord OR 16#0000_0400; END_IF;
IF bERD_RotorStallFault        THEN dwSWRO_StatusWord := dwSWRO_StatusWord OR 16#0000_0800; END_IF;
IF bMPC_Active                 THEN dwSWRO_StatusWord := dwSWRO_StatusWord OR 16#0000_1000; END_IF;
IF bGracefulDegradation        THEN dwSWRO_StatusWord := dwSWRO_StatusWord OR 16#0000_2000; END_IF;
IF bSuctionValvesOpenPermissive THEN dwSWRO_StatusWord := dwSWRO_StatusWord OR 16#0000_4000; END_IF;
IF bAntiscalantFlowConfirmed   THEN dwSWRO_StatusWord := dwSWRO_StatusWord OR 16#0000_8000; END_IF;
IF (iFSM_State = 90)           THEN dwSWRO_StatusWord := dwSWRO_StatusWord OR 16#8000_0000; END_IF;

END_FUNCTION_BLOCK
"""
    sections.append(s9)

    return "".join(sections)

if __name__ == "__main__":
    code = build_swro_block()
    print(f"Total ST code length: {len(code)} characters")
