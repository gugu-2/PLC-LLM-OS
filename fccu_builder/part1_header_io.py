# fccu_builder/part1_header_io.py

def get_part1_header_io():
    return """FUNCTION_BLOCK FB_Petrochem_FCC_RiserRegenerator_SlideValve_PressureBalance
(*
========================================================================================================================
  LUMINA CYBER-PHYSICAL AUTOMATION KERNEL - PETROCHEMICAL & ADVANCED REFINING SYSTEMS GROUP
  HIGH-DEMAND TIER 1 PRIORITY SECTOR: HEAVY HYDROCARBON CONVERSION & FLUID CATALYTIC CRACKING (FCCU)
  
  SYSTEM DESIGNATION : INDUSTRIAL FLUID CATALYTIC CRACKING RISER-REGENERATOR REACTION-REGENERATION SUITE
  NOMINAL CAPACITY   : 85,000 BPD (BARRELS PER STREAM DAY) VACUUM GAS OIL (VGO) & RESID HYDROCRACKING
  PRIMARY SUBSYSTEMS :
    - SHORT-CONTACT-TIME (SCT) RISER REACTOR WITH MULTI-POINT DISPERSION FEED NOZZLE ATOMIZATION
    - HIGH-EFFICIENCY CLOSED PRIMARY CYCLONES & VORTEX QUICK-DISENGAGING STRIPPING SECTION
    - TWO-STAGE FLUIDIZED-BED CATALYST REGENERATOR WITH COMPLETE/PARTIAL COKE COMBUSTION REGIMES
    - HYDRAULIC CATALYST CIRCULATION LOOP: SPENT CATALYST STANDPIPE & REGENERATED CATALYST STANDPIPE
    - DUAL REGENERATED & SPENT CATALYST HYDRAULIC SLIDE VALVES (RCSV & SCSV) WITH FLUID DELTA-P SEAL
    - COMBUSTION AIR BLOWER WITH AXIAL VARIABLE GUIDE VANES & ANTI-SURGE RECIRCULATION CASCADE
    - HIGH-PRESSURE HEAVY TORCH OIL AUXILIARY DIRECT BED COMBUSTION & LIGHT-OFF SYSTEM
    - FLUE GAS DOUBLE-DISC ORIFICE EXPANDER SLIDE VALVE & WET GAS COMPRESSOR BACKPRESSURE DECOUPLING
    - 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) CRITICAL SAFETY SENSOR SUITE WITH REAL-TIME DISCREPANCY TIMERS
    - 8-STATE DISCRETE CYBER-PHYSICAL STATE-SPACE ESTIMATOR & LUENBERGER OBSERVER (Ts = 25 ms)
    - RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) WITH PROJECTED GRADIENT DESCENT (PGD)
    - ANTI-REVERSAL CATALYTIC DEFLAGRATION HYDRAULIC INTERLOCK (<50 ms FAST ACTUATION CUTOFF)
    - DETERMINISTIC 14-STAGE REFINERY PRODUCTION, EQUILIBRATION & EMERGENCY QUENCH FINITE STATE MACHINE (FSM)
    - ISA-18.2 / IEC 62682 PROCESS ALARM MATRIX WITH 32-BIT BIT-PACKED TELEMETRY WORDS
    
  APPLICABLE REFINING CODES & INDUSTRY STANDARDS:
    - API RP 554 Part 1/2/3: Process Control Systems for Refining and Petrochemical Facilities
    - API Standard 537: Flare Details for Petroleum, Petrochemical, and Natural Gas Industries
    - API 560 / ASME Section VIII Div 1 & 2: Petrochemical Fired Heaters and High-Pressure Vessel Integrity
    - NFPA 85: Boiler and Combustion Systems Hazards Code (FCCU CO Boilers & Regenerator Light-off)
    - ISA-84 / IEC 61511: Functional Safety - Safety Instrumented Systems for the Process Industry Sector (SIL-3)
    - ISA-18.2 / IEC 62682: Management of Alarm Systems for the Process Industries
    - IEC 61131-3 Programmable Controllers - Part 3: Programming Languages (Structured Text Standard)

  AUTHOR: 75+ YEARS VETERAN PRINCIPAL AUTOMATION FELLOW & CYBER-PHYSICAL SYSTEMS CHAIR
========================================================================================================================

  THEORETICAL CHEMICAL ENGINEERING FOUNDATIONS & REACTION HYDRODYNAMICS:
  ----------------------------------------------------------------------------------------------------------------------
  1. RISER REACTOR HYDRODYNAMICS & SLIP-FLOW PHENOMENOLOGY:
     - The FCC riser reactor is an ultra-short-residence-time (1.5 - 3.5 seconds) co-current vertical pneumatic transport
       line wherein preheated atomized hydrocarbon feed (Vacuum Gas Oil, VGO, atmospheric residue) is contacted with hot
       solid regenerated zeolitic catalyst (USY / RE-Y zeolite, micro-spherical particles, d_p approx 65-75 microns,
       apparent particle density rho_p approx 1400 kg/m3).
     - Catalyst-to-Oil Ratio (C/O):
           C/O = F_cat_circ [t/h] / F_oil_feed [t/h]  (typical industrial range: 5.5 to 9.5 kg cat / kg feed)
     - Gas-Solid Slip Velocity & Voidage Profile:
       Gas superficial velocity increases rapidly up the riser from u_g,inlet approx 6-8 m/s to u_g,outlet approx 18-24 m/s
       due to molar volumetric expansion from catalytic cracking (1 mole heavy gasoil cracked into 4 to 6 moles lighter
       paraffins, olefins, and aromatics).
       Particle slip velocity is governed by Richardson-Zaki fluidization correlation and drag force balance:
           u_slip = u_g - u_p = u_t * epsilon_g^(n_rz - 1)
       where u_t is terminal settling velocity, epsilon_g is local cross-sectional gas void fraction (0.85 to 0.98),
       and n_rz is the Richardson-Zaki expansion index (approx 2.4 for FCC Geldart Group A powders).
     - Pressure Drop along the Riser Height (H_riser approx 35-45 m):
           Delta_P_riser = Delta_P_hydrostatic + Delta_P_acceleration + Delta_P_friction
           Delta_P_hydrostatic = integral_0^H ( (1 - epsilon_g) * rho_p + epsilon_g * rho_g ) * g * dz
       Hydrostatic solid hold-up accounts for >85% of total riser differential pressure.

  2. LUMPED REACTION KINETICS & ENDOTHERMIC THERMODYNAMICS:
     - Catalytic cracking occurs through carbenium ion chain mechanisms on acidic Bronsted/Lewis sites of the zeolite:
           Gasoil (F) ---> Gasoline (G) + LPG / Distillate (L) + Dry Gas (D) + Coke (C)
     - The overall cracking reaction is strongly endothermic, absorbing approximately 350 to 520 kJ/kg of vaporized feed.
       The thermal energy required to vaporize the incoming feed (at 180-260 deg C) and drive the cracking reactions
       to completion (riser outlet target 510-545 deg C) is supplied entirely by the sensible heat of the circulating
       regenerated catalyst arriving from the regenerator at 680 to 740 deg C.
     - Heat Balance across Riser Mixing Zone:
           F_feed * [ Delta_H_vap + C_p,oil * (T_mix - T_feed) + Delta_H_crack * X_feed ] =
           F_cat_circ * C_p,cat * (T_regen - T_mix) + F_steam * C_p,steam * (T_mix - T_steam)
       where C_p,cat approx 1.15 kJ/(kg*K), C_p,oil_vapor approx 2.85 kJ/(kg*K).
     - Dynamic Coke Deposition on Catalyst Surface:
           Coke weight percent on spent catalyst (C_sc) increases from C_rc (regenerated catalyst coke: 0.05 - 0.15 wt%)
           to C_sc (spent catalyst coke: 0.85 - 1.45 wt%) through catalytic cracking, heavy aromatic condensation,
           and metal-catalyzed dehydrogenation (Ni, V active sites).
           C_sc = C_rc + k_coke * (t_contact)^m_coke * exp( -E_coke / (R_gas * T_riser) )

  3. TWO-STAGE FLUIDIZED REGENERATOR COMBUSTION KINETICS:
     - Deactivated spent catalyst passes through the steam stripping section (displacing interstitial hydrocarbons)
       and enters the Fluidized Bed Regenerator where coke is burned off with compressed atmospheric air at 670-745 deg C.
     - Heterogeneous Coke Combustion Chemical Reactions:
           1) Carbon partial oxidation : C_(coke) + 0.5 O2 ----> CO             (Delta_H = -110.5 kJ/mol C)
           2) Carbon full oxidation    : C_(coke) + O2       ----> CO2            (Delta_H = -393.5 kJ/mol C)
           3) Homogeneous / catalysed  : CO + 0.5 O2         ----> CO2            (Delta_H = -283.0 kJ/mol C)
           4) Hydrogen combustion      : 2 H_(coke) + 0.5 O2 ----> H2O            (Delta_H = -241.8 kJ/mol H2)
     - Carbon Monoxide Combustion Ratio (CO2 / CO) in dense bed is controlled by combustion air blower mass flow,
       bed temperature, and combustion promoter additives (Pt/Al2O3 micro-particles, 0.5-2.0 ppmw Pt in inventory).
     - Complete Combustion vs Partial Combustion Regimes:
       * Complete Combustion Mode: Excess oxygen (1.0 to 2.5 vol% O2 in flue gas) converts virtually all carbon to CO2.
         Dense bed temperatures operate higher (700-750 deg C), eliminating need for external CO boiler.
       * Afterburning Phenomenon: If unburned CO escapes into the dilute phase or cyclone disengaging space and meets
         residual oxygen, gas-phase CO combustion occurs in the absence of solid catalyst heat sink, causing catastrophic
         temperature excursions (>820 deg C) that can structurally destroy cyclone barrels and refractory liners.
         The algorithm detects Afterburning Delta-T = (T_cyclone - T_dense_bed) > 25 deg C and deploys quench steam/water.

  4. CATALYST SLIDE VALVE HYDRAULIC PRESSURE BALANCE & ANTI-REVERSAL LOCK:
     - Catalyst circulation between reactor and regenerator is driven by the gravitational hydrostatic head of fluidized
       solids in the vertical standpipes minus the pressure drop across the respective catalyst slide valves.
     - Standpipe Hydrostatic Head:
           Delta_P_standpipe = rho_aerated * g * H_standpipe  [kPa]
       Aeration gas (steam in spent standpipe, dry instrument air or nitrogen in regenerated standpipe) is injected
       via multi-tap aeration nozzles to maintain Geldart Group A powder in minimum fluidization state (voidage approx 0.45).
     - Catalyst Slide Valve Differential Pressure (dP_SCSV and dP_RCSV):
           dP_valve = Delta_P_standpipe - Delta_P_vessel_delta
           where:
             dP_SCSV = P_stripper_bottom - P_regen_dense_bed - Delta_P_spent_transport
             dP_RCSV = P_regen_bottom - P_riser_inlet - Delta_P_regen_transport
     - CRITICAL SAFETY INTERLOCK (ANTI-REVERSAL DEFLAGRATION):
       Hydrocarbon vapors in the reactor/stripper MUST NEVER flow backward into the oxygen-containing regenerator,
       as direct mixing of 500 deg C flammable hydrocarbon gas with hot air creates a catastrophic internal explosion.
       Similarly, hot oxygen-rich flue gas must never enter the hydrocarbon reactor.
       A positive pressure seal across both slide valves is an absolute refinery safety imperative:
           Mandatory Stable Window: 35.0 kPa <= dP_valve <= 70.0 kPa
           Warning Threshold (Low): dP_valve < 30.0 kPa
           SIL-3 Emergency Reverse Flow Fast Trip: dP_valve < 20.0 kPa
       Upon detecting dP < 20.0 kPa on either slide valve, the hydraulic actuator is driven to full mechanical seat
       closure (<50 milliseconds) via double-acting hydraulic accumulator dump valves, cutting feed instantaneously.

  5. 8-STATE DISCRETE CYBER-PHYSICAL MODEL (Ts = 25 ms):
     State Vector x[k] in R^8:
       x1 : Riser Outlet Temperature [deg C]
       x2 : Riser Top Differential Pressure [kPa]
       x3 : Regenerator 1st Stage Dense Bed Temperature [deg C]
       x4 : Regenerator 2nd Stage Dense Bed Temperature [deg C]
       x5 : Spent Catalyst Slide Valve Differential Pressure (dP_SCSV) [kPa]
       x6 : Regenerated Catalyst Slide Valve Differential Pressure (dP_RCSV) [kPa]
       x7 : Regenerator Flue Gas Excess Oxygen Content [% O2]
       x8 : Combustion Flue Gas Carbon Monoxide Concentration [ppmv]

     Manipulated Input Vector u[k] in R^6:
       u1 : Regenerated Catalyst Slide Valve Position Command (RCSV) [0.0 .. 100.0 %]
       u2 : Spent Catalyst Slide Valve Position Command (SCSV) [0.0 .. 100.0 %]
       u3 : Combustion Air Blower VFD Guide Vane Command [0.0 .. 100.0 %]
       u4 : Torch Oil Injection Control Valve Command [0.0 .. 100.0 %]
       u5 : Riser Lift Steam Control Valve Command [0.0 .. 100.0 %]
       u6 : Flue Gas Double-Disc Slide Valve Backpressure Command [0.0 .. 100.0 %]
========================================================================================================================
*)
VAR_INPUT
    (* Master Execution & Safety Permissive Commands *)
    bSystemEnable                       : BOOL;         (* Master Function Block Supervisory Run Enable [-] *)
    bEmergencyStop                      : BOOL;         (* SIL-3 Hardwired Hard Emergency Stop Pushbutton [-] *)
    bAlarmReset                         : BOOL;         (* Master Safety Alarm Latch Acknowledge & Reset [-] *)
    bAutoModeRequest                    : BOOL;         (* Automatic Multivariable MPC Control Request [-] *)
    bFeedCutPermissive                  : BOOL;         (* Refinery Feed Header Safety Interlock Permissive [-] *)
    bTorchOilPermissive                 : BOOL;         (* Torch Oil Burner Combustion Safety Permissive [-] *)
    bAirBlowerTripFeedback              : BOOL;         (* Combustion Air Blower Motor Overload / Surge Trip [-] *)
    bSlideValveHydraulicOk              : BOOL;         (* Slide Valve High-Pressure Hydraulic Power Unit Health [-] *)

    (* 2oo3 Triple Modular Redundancy (TMR) Primary Sensor Channels *)
    rTT_RISER_101A_degC                 : REAL;         (* Riser Outlet Temp Transmitter Channel A [deg C] *)
    rTT_RISER_101B_degC                 : REAL;         (* Riser Outlet Temp Transmitter Channel B [deg C] *)
    rTT_RISER_101C_degC                 : REAL;         (* Riser Outlet Temp Transmitter Channel C [deg C] *)

    rTT_REGEN_201A_degC                 : REAL;         (* Regenerator 1st Bed Temp Transmitter Channel A [deg C] *)
    rTT_REGEN_201B_degC                 : REAL;         (* Regenerator 1st Bed Temp Transmitter Channel B [deg C] *)
    rTT_REGEN_201C_degC                 : REAL;         (* Regenerator 1st Bed Temp Transmitter Channel C [deg C] *)

    rPDT_SCSV_301A_kPa                  : REAL;         (* Spent Catalyst Slide Valve DP Channel A [kPa] *)
    rPDT_SCSV_301B_kPa                  : REAL;         (* Spent Catalyst Slide Valve DP Channel B [kPa] *)
    rPDT_SCSV_301C_kPa                  : REAL;         (* Spent Catalyst Slide Valve DP Channel C [kPa] *)

    rPDT_RCSV_401A_kPa                  : REAL;         (* Regenerated Catalyst Slide Valve DP Channel A [kPa] *)
    rPDT_RCSV_401B_kPa                  : REAL;         (* Regenerated Catalyst Slide Valve DP Channel B [kPa] *)
    rPDT_RCSV_401C_kPa                  : REAL;         (* Regenerated Catalyst Slide Valve DP Channel C [kPa] *)

    rAT_O2_501A_pct                     : REAL;         (* Flue Gas Zirconia Excess O2 Analyzer Channel A [% O2] *)
    rAT_O2_501B_pct                     : REAL;         (* Flue Gas Zirconia Excess O2 Analyzer Channel B [% O2] *)
    rAT_O2_501C_pct                     : REAL;         (* Flue Gas Zirconia Excess O2 Analyzer Channel C [% O2] *)

    (* Additional Critical Process Transmitters & Exogenous Feedbacks *)
    rTT_REGEN_STAGE2_degC               : REAL;         (* Regenerator 2nd Stage Dense Bed Temp [deg C] *)
    rTT_REGEN_CYCLONE_degC              : REAL;         (* Regenerator Dilute Phase / Cyclone Inlet Temp [deg C] *)
    rPDT_RISER_TOTAL_kPa                : REAL;         (* Total Riser Bottom-to-Top Differential Pressure [kPa] *)
    rAT_CO_FLUEGAS_ppmv                 : REAL;         (* Flue Gas Infrared Carbon Monoxide Analyzer [ppmv] *)
    rPT_REGEN_TOP_kPa                   : REAL;         (* Regenerator Vessel Top Flue Gas Pressure [kPa] *)
    rPT_REACTOR_TOP_kPa                 : REAL;         (* Reactor Disengager Vessel Top Vapor Pressure [kPa] *)
    rFT_OIL_FEED_th                     : REAL;         (* Total Combined Fresh Gasoil Feed Mass Flow [t/h] *)
    rTT_FEED_PREHEAT_degC               : REAL;         (* Heavy Oil Feed Fired Heater Outlet Temp [deg C] *)
    rFT_LIFT_STEAM_th                   : REAL;         (* Riser Base Total Lift Steam Mass Flow Rate [t/h] *)
    rFT_DISPERSION_STEAM_th             : REAL;         (* Feed Nozzle Steam Atomization Total Rate [t/h] *)
    rFT_COMBUSTION_AIR_kgs              : REAL;         (* Main Air Blower Blast Air Mass Flow Rate [kg/s] *)
    rPT_AIR_BLAST_kPa                   : REAL;         (* Air Blower Discharge Blast Header Pressure [kPa] *)
    rFT_TORCH_OIL_kgh                   : REAL;         (* Auxiliary Torch Oil Injection Mass Flow Rate [kg/h] *)
    rFT_QUENCH_WATER_th                 : REAL;         (* Regenerator Dilute Phase Quench Water Flow [t/h] *)
    rLT_STRIPPER_BED_m                  : REAL;         (* Spent Catalyst Stripper Bed Level [m] *)
    rLT_REGEN_STAGE1_m                  : REAL;         (* Regenerator Stage 1 Fluidized Bed Level [m] *)
    rLT_REGEN_STAGE2_m                  : REAL;         (* Regenerator Stage 2 Fluidized Bed Level [m] *)
    rDensity_Feed_kgm3                  : REAL;         (* Fresh Gasoil Feed Packed Liquid Density [kg/m3] *)
    rAPI_Gravity_Feed                   : REAL;         (* Hydrocarbon Feed API Specific Gravity Index [deg API] *)

    (* Setpoint Targets & Operational Constraints *)
    rTargetRiserTemp_degC               : REAL;         (* Operator Riser Outlet Temp Target (515.0 - 540.0) [deg C] *)
    rTargetSlideValveDP_kPa             : REAL;         (* Target Equalized Slide Valve Differential Pressure [kPa] *)
    rTargetRegenTemp_degC               : REAL;         (* Target Regenerator 1st Bed Temp (680.0 - 735.0) [deg C] *)
    rTargetFlueGasO2_pct                : REAL;         (* Target Regenerator Flue Gas Excess Oxygen (1.0 - 2.5) [% O2] *)
    rTargetFeedRate_th                  : REAL;         (* Target Production Unit Feed Mass Throughput [t/h] *)
    rMaxAllowableRiserTemp_degC         : REAL;         (* Safety Maximum Upper Riser Temperature Limit [deg C] *)
    rMinAllowableSlideValveDP_kPa       : REAL;         (* Absolute Minimum Slide Valve Seal Differential [kPa] *)
    rMaxAllowableRegenTemp_degC         : REAL          (* Structural Maximum Regenerator Vessel Temp Limit [deg C] *)
END_VAR
VAR_OUTPUT
    (* Primary Manipulated Actuator Command Outputs *)
    rActuator_RCSV_Pos_pct              : REAL;         (* Regenerated Catalyst Slide Valve Position Command [0..100%] *)
    rActuator_SCSV_Pos_pct              : REAL;         (* Spent Catalyst Slide Valve Position Command [0..100%] *)
    rActuator_AirBlower_pct             : REAL;         (* Combustion Air Blower VFD / Guide Vane Command [0..100%] *)
    rActuator_TorchOil_pct              : REAL;         (* Torch Oil Injection Fuel Control Valve Command [0..100%] *)
    rActuator_LiftSteam_pct             : REAL;         (* Riser Base Lift Steam Control Valve Command [0..100%] *)
    rActuator_FlueGasValve_pct          : REAL;         (* Flue Gas Double-Disc Slide Valve Backpressure [0..100%] *)
    rActuator_QuenchWater_pct           : REAL;         (* Regenerator Afterburn Quench Water Valve Command [0..100%] *)
    rActuator_FeedCutoff_pct            : REAL;         (* Main Hydrocarbon Feed Safety Emergency Cutoff [0..100%] *)

    (* Master Operational States & Discrete Safety Interlocks *)
    bSystemReady                        : BOOL;         (* Riser-Regenerator Loop Ready for Operation [-] *)
    bProductionActive                   : BOOL;         (* Full Cracking Steady-State Production Run Active [-] *)
    bEmergencyTripActive                : BOOL;         (* SIL-3 Master Emergency Trip Latched Active [-] *)
    bAntiReversalLockActive             : BOOL;         (* Catalyst Slide Valve Reverse DP Fast Lock Engaged [-] *)
    bAfterburnQuenchActive              : BOOL;         (* Regenerator Dilute Phase Thermal Afterburning Active [-] *)
    bBlowerSurgeAlert                   : BOOL;         (* Combustion Air Blower Impending Surge Alert Active [-] *)
    bTorchOilActive                     : BOOL;         (* Direct Bed Torch Oil Combustion Currently Active [-] *)
    nOperationalState                   : INT;          (* Deterministic Refinery FSM State Code [0..13] [-] *)

    (* Bit-Packed Telemetry Words (ISA-18.2 Compliant) *)
    dwStatusWord1                       : DWORD;        (* Primary Operational Status Bitfield 1 [-] *)
    dwStatusWord2                       : DWORD;        (* Secondary Operational Status Bitfield 2 [-] *)
    dwAlarmWord1                        : DWORD;        (* Critical Process Alarm Bitfield 1 (HH/LL Trips) [-] *)
    dwAlarmWord2                        : DWORD;        (* Warning & Maintenance Alarm Bitfield 2 (H/L Warnings) [-] *)
    dwFirstOutWord                      : DWORD;        (* SIL-3 Fast First-Out Safety Trip Diagnostic Code [-] *)

    (* 2oo3 TMR Voted Sensor Process Variables *)
    rVoted_RiserTemp_degC               : REAL;         (* 2oo3 TMR Voted Riser Outlet Temperature [deg C] *)
    rVoted_RegenBedTemp_degC            : REAL;         (* 2oo3 TMR Voted Regenerator Dense Bed Temp [deg C] *)
    rVoted_SCSV_dP_kPa                  : REAL;         (* 2oo3 TMR Voted Spent Slide Valve Delta-P [kPa] *)
    rVoted_RCSV_dP_kPa                  : REAL;         (* 2oo3 TMR Voted Regenerated Slide Valve Delta-P [kPa] *)
    rVoted_FlueGasO2_pct                : REAL;         (* 2oo3 TMR Voted Flue Gas Excess Oxygen [% O2] *)

    (* Cyber-Physical Observer States & Diagnostics *)
    rObs_RiserTemp_degC                 : REAL;         (* Estimated Riser Outlet Temperature x1 [deg C] *)
    rObs_RiserTopDP_kPa                 : REAL;         (* Estimated Riser Top Differential Pressure x2 [kPa] *)
    rObs_RegenStage1Temp_degC           : REAL;         (* Estimated Regenerator Stage 1 Bed Temp x3 [deg C] *)
    rObs_RegenStage2Temp_degC           : REAL;         (* Estimated Regenerator Stage 2 Bed Temp x4 [deg C] *)
    rObs_SCSV_dP_kPa                    : REAL;         (* Estimated Spent Slide Valve Delta-P x5 [kPa] *)
    rObs_RCSV_dP_kPa                    : REAL;         (* Estimated Regenerated Slide Valve Delta-P x6 [kPa] *)
    rObs_ExcessO2_pct                   : REAL;         (* Estimated Flue Gas Excess Oxygen x7 [% O2] *)
    rObs_CO_ppmv                        : REAL;         (* Estimated Flue Gas Carbon Monoxide x8 [ppmv] *)
    rMPC_CostFunctionJ                  : REAL;         (* Receding-Horizon MPC Quadratic Cost Index [-] *)
    rMPC_OptimizationError              : REAL;         (* PGD Convergence Residual Norm Infinity [-] *)
    rSlideValveMinMargin_kPa            : REAL          (* Minimum Operating Hydraulic Seal Margin over 35 kPa [kPa] *)
END_VAR
"""
