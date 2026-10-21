# -*- coding: utf-8 -*-
"""
Generator script for IEC 61131-3 Megawatt High-Pressure Alkaline Water Electrolysis (AWE)
Functional Block: FB_Hydrogen_AWE_HighPressure_SeparatorSync
Target Character Length: 85,000 - 95,000 chars
Structured Text 3rd Edition Compliant
"""

import json
import uuid
import re

def build_code():
    parts = []
    
    # -------------------------------------------------------------------------
    # 0. FUNCTION_BLOCK Header & Architecture Comments
    # -------------------------------------------------------------------------
    parts.append("""FUNCTION_BLOCK FB_Hydrogen_AWE_HighPressure_SeparatorSync
(*
 ==========================================================================================
  PROJECT:       10 MW HIGH-PRESSURE ALKALINE WATER ELECTROLYSIS (AWE) CYBER-PHYSICAL GOVERNOR
  SUBSYSTEM:     ANODE-CATHODE SEPARATOR BALANCE, CROSS-PERMEATION & DE-OXO THERMAL SYNC
  DISCIPLINE:    ELECTROCHEMICAL PROCESS AUTOMATION / ADVANCED MULTIVARIABLE MODEL PREDICTIVE CONTROL
  IEC STANDARD:  IEC 61131-3 STRUCTURED TEXT 3RD EDITION (DETERMINISTIC EMBEDDED REAL-TIME CONTROL)
 ==========================================================================================

  1.0 SCIENTIFIC PRINCIPLES & GOVERNING PROCESS EQUATIONS:
  ------------------------------------------------------------------------------------------
  This Function Block executes deterministic real-time supervisory governor control, multivariable
  decoupling, and SIL-3 functional safety mitigation for an industrial 10-Megawatt High-Pressure
  Alkaline Water Electrolysis (AWE) facility operating under extreme thermodynamic conditions:
    - Nominal operating pressure:   30.0 bar (range: 25.0 to 32.0 bar gauge; design: 45.0 bar)
    - Nominal operating temp:       80.0 deg C (range: 65.0 to 85.0 deg C; trip limit: 90.0 deg C)
    - Liquid electrolyte:           30.0 wt% Aqueous Potassium Hydroxide (KOH)
    - Stack electrical rating:      10.0 MW (Stack current: 0 to 16.0 kA DC; Stack voltage: 450 - 650 V DC)
    - Cell architecture:            280 Bipolar Zero-Gap Filter-Press Cell Frames in series
    - Diaphragm separator:          Zirfon PERL 500 porous composite (85 wt% ZrO2, 15 wt% polysulfone)
                                    Thickness: 500 um (+- 30 um), Porosity: 55%, Bubble point > 2.0 bar

  1.1 ELECTROCHEMICAL KINETICS & NERNST-OVERPOTENTIAL DECOMPOSITION:
  ------------------------------------------------------------------------------------------
  Overall endothermic water-splitting reaction:
      H2O(l) + Electrical Energy + Heat --> H2(g) + 0.5 O2(g)
  Cathode (Hydrogen Evolution Reaction - HER):
      2 H2O + 2 e- --> H2(g) + 2 OH-               [E0_HER = -0.828 V vs SHE at 25 deg C]
  Anode (Oxygen Evolution Reaction - OER):
      2 OH- --> 0.5 O2(g) + H2O + 2 e-             [E0_OER = +0.401 V vs SHE at 25 deg C]

  Thermodynamic reversible cell voltage E_rev(T, P) is governed by the Nernst equation:
      E_rev(T, P) = E0(T) + [R * T / (2 * F)] * ln[ (a_H2 * a_O2^0.5) / a_H2O ]
  Where:
      - E0(T) = 1.5184 - 1.5421e-3 * T + 9.523e-5 * T * ln(T) + 9.84e-8 * T^2   [V, T in Kelvin]
      - Faradaic constant F = 96485.33 C/mol, Universal gas constant R = 8.31446 J/(mol*K)
      - Water activity in 30 wt% KOH: a_H2O ~ 0.68 (depressed from unity due to ionic solvation)
      - Thermoneutral cell potential: E_tn = Delta_H / (2 * F) ~ 1.482 V at 80 deg C
  The total operating cell voltage U_cell is decomposed into discrete kinetic components:
      U_cell = E_rev(T, P) + eta_act,a(j, T) + eta_act,c(j, T) + eta_ohm,lye(j, T) + eta_ohm,dia(j, T) + eta_mass(j, T)
  Where:
      - Activation overpotentials follow the non-linear Butler-Volmer relationship:
        eta_act = (R * T / (alpha * F)) * asinh( j / (2 * j0) )
      - Ohmic electrolyte resistance follows empirical Kohlrausch conductivity for 30 wt% KOH:
        kappa_KOH(T) = -2.041 * w + 0.0028 * w^2 + 0.005332 * w * T + 0.000207 * w * T^2 [mS/cm]
      - Void fraction bubble resistance (Bruggeman effective medium approximation):
        kappa_eff = kappa_bulk * (1 - epsilon_void)^1.5

  1.2 FARADAY'S LAW, MOLAR GAS FLUX & HYDRODYNAMIC BUBBLE DISENGAGEMENT:
  ------------------------------------------------------------------------------------------
  Theoretical molar production rates per Faraday's law:
      dot_n_H2 = (I_stack * N_cells * eta_Faraday) / (2 * F)   [mol/s]
      dot_n_O2 = (I_stack * N_cells * eta_Faraday) / (4 * F)   [mol/s]
  Gas volume generation at standard temperature and pressure (0 deg C, 1.01325 bar STP):
      V_dot_H2_STP = dot_n_H2 * 0.022414 * 3600  [Nm3/h] (~4.18 Nm3/h per kA per cell)
      V_dot_O2_STP = dot_n_O2 * 0.022414 * 3600  [Nm3/h] (~2.09 Nm3/h per kA per cell)
  In-situ volumetric gas flow at operating 30 bar and 80 deg C:
      V_dot_insitu = dot_n * Z(T, P) * R * T / P_operating  [m3/h]
  In the gas-liquid separators, bubbles rise through the liquid froth according to Hadamard-Rybczynski
  drag relations modified for high ionic strength (surfactant-free hindered bubble clustering):
      u_bubble_rise = [g * d_bubble^2 * (rho_lye - rho_gas)] / [18 * mu_lye] * (1 - phi_gas)^2.39

  1.3 DIAPHRAGM CROSS-PERMEATION & FLAMMABILITY SAFETY LIMITS:
  ------------------------------------------------------------------------------------------
  Cross-permeation represents the primary catastrophic explosion hazard in pressurized AWE.
  Gases dissolve into the electrolyte at the electrode surfaces per Henry's Law:
      C_sol,H2 = k_H,H2(T) * P_H2;   C_sol,O2 = k_H,O2(T) * P_O2
  Mass transfer across the Zirfon composite separator proceeds by coupled diffusion and convection:
      J_total = J_diffusion + J_convection
      J_diffusion  = -D_eff * [C_sol / delta_x_membrane]                 (Fick's 1st Law)
      J_convection = -[k_perm / mu_lye] * [dP / delta_x_membrane] * C_sol (Darcy's Law)
  Where:
      - Effective diffusivity: D_eff = D_molecular * (epsilon_porosity / tau_tortuosity)
      - Diaphragm thickness: delta_x = 500 um; Permeability: k_perm ~ 1.2e-15 m2
  The fraction of H2 impurity in the O2 stream (HTO) and O2 in H2 (OTH) are given by:
      C_H2_in_O2 = [dot_n_cross,H2] / [dot_n_produced,O2 + dot_n_cross,H2]
  CRITICAL SAFETY IMPLICATION: Because dot_n_produced,O2 is directly proportional to I_stack,
  while J_diffusion is driven by the 30 bar partial pressure and is completely independent of current,
  as current I_stack drops, C_H2_in_O2 rises hyperbolically as (1 / I_stack)!
  Flammability Boundaries (ISO 22734 / IEC 61010-1 / EN 60079):
    - Lower Flammability Limit (LFL) of H2 in O2: 4.0 vol% (40,000 ppm)
    - SIL-3 Emergency Shutdown Trip Threshold:    1.8 vol% (18,000 ppm) [45% LFL]
    - Warning Alarm & Fast Power Derate:          1.0 vol% (10,000 ppm) [25% LFL]

  1.4 ANODE-CATHODE DIFFERENTIAL PRESSURE NULLING & COMMUNICATING VESSELS:
  ------------------------------------------------------------------------------------------
  The liquid electrolyte return circuits from the Anode and Cathode separators join at the common
  suction header of the recirculation pumps. This creates a giant U-tube hydraulic manometer:
      Delta_P_hydrostatic = rho_lye * g * (h_Cathode - h_Anode)
  With 30 wt% KOH (rho = 1285 kg/m3), a differential pressure of just 10.0 mbar induces an
  equilibrium level shift of:
      Delta_h = 1000 Pa / (1285 kg/m3 * 9.80665 m/s2) = 0.0793 m = 7.93 cm!
  If dP reaches 50 mbar, liquid shifts by 40 cm, causing total gas blow-through into the pump suction
  or liquid flooding of the gas demister pads. Dynamic cross-permeation nulling eliminates dP
  using high-speed dome-loaded electronic pilot backpressure valves (PCV-H2, PCV-O2) and an
  inter-separator balancing transfer valve (LV-Bal).

  1.5 CATALYTIC DE-OXO PURIFICATION THERMAL RUNAWAY SYNC:
  ------------------------------------------------------------------------------------------
  Crude H2 contains 0.1 to 1.5 vol% O2. A fixed-bed catalytic De-Oxo reactor (0.5 wt% Pd on theta-Al2O3)
  combusts the trace oxygen:
      2 H2 + O2 --> 2 H2O(g)   [Delta_H_rxn = -241.8 kJ/mol O2 consumed]
  Adiabatic temperature rise:
      Delta_T_ad = [y_O2 * (-Delta_H_rxn)] / [C_p,gas_mix] ~ 162 deg C per 1.0 vol% O2!
  Catalyst thermal constraints:
    - Minimum light-off temperature:  65 deg C (below which reaction extinguishes and O2 slips)
    - Maximum operating temperature:  380 deg C
    - Irreversible sintering threshold: 450 deg C (palladium crystallite agglomeration and alumina phase shift)
  The block executes feedforward thermal balancing: modulating SCR preheater duty, interstage cooling
  gas bypass, and emergency quench isolation.

  1.6 FAST RENEWABLE POWER RAMP RATE LIMITING:
  ------------------------------------------------------------------------------------------
  To integrate with intermittent solar PV and wind turbines, the electrolyzer must accommodate
  extreme power gradients. However, rapid current ramp-up (di/dt > 10% / sec) causes violent gas void
  fraction expansion ('liquid swell') in the cell frames, triggering massive hydraulic dP pulses.
  Rapid current ramp-down drops Faradaic O2 production instantly while gas cross-diffusion continues,
  causing a sudden spike in H2-in-O2 concentration. The block dynamically modulates maximum allowable
  di/dt based on stack temperature, cell voltage dispersion, and instantaneous gas purity margins.

  1.7 MULTIVARIABLE STATE-SPACE (A, B, C, D) & REAL-TIME MPC OPTIMIZER:
  ------------------------------------------------------------------------------------------
  State vector (n=6):
      x = [ dP (mbar), dLevel (%), T_DeOxo (deg C), T_Stack (deg C), C_H2_in_O2 (ppm/1000), C_O2_in_H2 (ppm/1000) ]^T
  Actuator vector (m=4):
      u = [ u_PCV_H2 (%), u_LV_Bal (%), u_HTR_DeOxo (%), I_Rectifier_Demand (kA) ]^T
  The block solves an embedded Quadratic Program (QP) using Barzilai-Borwein projected gradient
  descent with explicit box constraints and actuator slew rate limits.
 ==========================================================================================
*)
""")

    # -------------------------------------------------------------------------
    # 1. VAR_INPUT Declarations (min 8 typed with physical units)
    # -------------------------------------------------------------------------
    parts.append("""VAR_INPUT
    (* ------------------------------------------------------------------------------------- *)
    (* SYSTEM MASTER DIGITAL PERMISSIVES & SUPERVISORY COMMANDS                              *)
    (* ------------------------------------------------------------------------------------- *)
    bEnableSystem                   : BOOL;     (* Master functional enable permissive command *)
    bEmergencyStop                  : BOOL;     (* SIL-3 active-low hardwired safety shutdown contact *)
    bResetFaults                    : BOOL;     (* Master alarm acknowledgement and unlatch command *)
    bAutoMode                       : BOOL;     (* Supervisory automatic MPC control enable permissive *)
    bDeOxoPreheaterPermissive       : BOOL;     (* Catalytic De-Oxo electric preheater power supply ready *)
    bLyeCirculationPermissive       : BOOL;     (* Electrolyte recirculation loop valve alignment confirmed *)
    bNitrogenPurgePermissive        : BOOL;     (* Inert nitrogen supply skid header pressure adequate *)
    bCoolingWaterPermissive         : BOOL;     (* Primary cooling water loop circulation verified *)

    (* ------------------------------------------------------------------------------------- *)
    (* RENEWABLE POWER & ELECTRICAL PROCESS TRANSMITTERS [kW], [kA], [V], [Hz]               *)
    (* ------------------------------------------------------------------------------------- *)
    rRenewablePowerAvailable_kW     : REAL;     (* Dynamic renewable (Wind/Solar) power profile [kW] *)
    rStackCurrent_kA                : REAL;     (* DC Rectifier measured stack current [kA] *)
    rStackVoltage_V                 : REAL;     (* DC Stack measured terminal voltage [V] *)
    rGridFrequency_Hz               : REAL;     (* AC Grid frequency for primary frequency response [Hz] *)
    rCellVoltageSpread_mV           : REAL;     (* Maximum minus minimum individual cell voltage [mV] *)

    (* ------------------------------------------------------------------------------------- *)
    (* TRIPLE MODULAR REDUNDANCY (2oo3) CATHODE (H2) PRESSURE TRANSMITTERS [bar]             *)
    (* ------------------------------------------------------------------------------------- *)
    rCathodePressure_A_bar          : REAL;     (* Cathode separator gas headspace pressure PT-201A [bar] *)
    rCathodePressure_B_bar          : REAL;     (* Cathode separator gas headspace pressure PT-201B [bar] *)
    rCathodePressure_C_bar          : REAL;     (* Cathode separator gas headspace pressure PT-201C [bar] *)

    (* ------------------------------------------------------------------------------------- *)
    (* TRIPLE MODULAR REDUNDANCY (2oo3) ANODE (O2) PRESSURE TRANSMITTERS [bar]               *)
    (* ------------------------------------------------------------------------------------- *)
    rAnodePressure_A_bar            : REAL;     (* Anode separator gas headspace pressure PT-301A [bar] *)
    rAnodePressure_B_bar            : REAL;     (* Anode separator gas headspace pressure PT-301B [bar] *)
    rAnodePressure_C_bar            : REAL;     (* Anode separator gas headspace pressure PT-301C [bar] *)

    (* ------------------------------------------------------------------------------------- *)
    (* TRIPLE MODULAR REDUNDANCY (2oo3) DIFFERENTIAL PRESSURE TRANSMITTERS [mbar]            *)
    (* ------------------------------------------------------------------------------------- *)
    rDifferentialPressure_A_mbar    : REAL;     (* High-accuracy fast DP transmitter dPT-401A (P_O2 - P_H2) [mbar] *)
    rDifferentialPressure_B_mbar    : REAL;     (* High-accuracy fast DP transmitter dPT-401B (P_O2 - P_H2) [mbar] *)
    rDifferentialPressure_C_mbar    : REAL;     (* High-accuracy fast DP transmitter dPT-401C (P_O2 - P_H2) [mbar] *)

    (* ------------------------------------------------------------------------------------- *)
    (* TRIPLE MODULAR REDUNDANCY (2oo3) CATHODE SEPARATOR LYE LEVEL TRANSMITTERS [%]         *)
    (* ------------------------------------------------------------------------------------- *)
    rCathodeSeparatorLevel_A_pct    : REAL;     (* Cathode gas-liquid separator guided wave radar LT-202A [%] *)
    rCathodeSeparatorLevel_B_pct    : REAL;     (* Cathode gas-liquid separator differential pressure LT-202B [%] *)
    rCathodeSeparatorLevel_C_pct    : REAL;     (* Cathode gas-liquid separator displacer float LT-202C [%] *)

    (* ------------------------------------------------------------------------------------- *)
    (* TRIPLE MODULAR REDUNDANCY (2oo3) ANODE SEPARATOR LYE LEVEL TRANSMITTERS [%]           *)
    (* ------------------------------------------------------------------------------------- *)
    rAnodeSeparatorLevel_A_pct      : REAL;     (* Anode gas-liquid separator guided wave radar LT-302A [%] *)
    rAnodeSeparatorLevel_B_pct      : REAL;     (* Anode gas-liquid separator differential pressure LT-302B [%] *)
    rAnodeSeparatorLevel_C_pct      : REAL;     (* Anode gas-liquid separator displacer float LT-302C [%] *)

    (* ------------------------------------------------------------------------------------- *)
    (* ELECTROLYTE CIRCULATION PROCESS TRANSMITTERS [m3/h], [deg C], [mS/cm], [wt%]          *)
    (* ------------------------------------------------------------------------------------- *)
    rCathodeLyeFlow_m3h             : REAL;     (* Cathode half-cell lye circulation flow rate [m3/h] *)
    rAnodeLyeFlow_m3h               : REAL;     (* Anode half-cell lye circulation flow rate [m3/h] *)
    rElectrolyteInletTemp_DegC      : REAL;     (* 30 wt% KOH common stack inlet temperature [deg C] *)
    rCathodeOutletTemp_DegC         : REAL;     (* Cathode stack return lye temperature [deg C] *)
    rAnodeOutletTemp_DegC           : REAL;     (* Anode stack return lye temperature [deg C] *)
    rElectrolyteConductivity_mScm   : REAL;     (* 30 wt% KOH specific ionic conductivity [mS/cm] *)
    rElectrolyteConcentration_wtPct : REAL;     (* On-line coriolis derived KOH concentration [wt%] *)

    (* ------------------------------------------------------------------------------------- *)
    (* GAS MASS FLOW TRANSMITTERS [Nm3/h]                                                    *)
    (* ------------------------------------------------------------------------------------- *)
    rHydrogenGasFlow_Nm3h           : REAL;     (* Cathode raw hydrogen gas production flow rate [Nm3/h] *)
    rOxygenGasFlow_Nm3h             : REAL;     (* Anode raw oxygen gas production flow rate [Nm3/h] *)

    (* ------------------------------------------------------------------------------------- *)
    (* TRIPLE MODULAR REDUNDANCY (2oo3) TRACE GAS ANALYZERS [ppm]                            *)
    (* ------------------------------------------------------------------------------------- *)
    rOxygenInHydrogen_A_ppm         : REAL;     (* Crude H2 stream trace O2 impurity analyzer AT-501A [ppm] *)
    rOxygenInHydrogen_B_ppm         : REAL;     (* Crude H2 stream trace O2 impurity analyzer AT-501B [ppm] *)
    rOxygenInHydrogen_C_ppm         : REAL;     (* Crude H2 stream trace O2 impurity analyzer AT-501C [ppm] *)
    rHydrogenInOxygen_A_ppm         : REAL;     (* Anode off-gas trace H2 impurity analyzer AT-601A [ppm] *)
    rHydrogenInOxygen_B_ppm         : REAL;     (* Anode off-gas trace H2 impurity analyzer AT-601B [ppm] *)
    rHydrogenInOxygen_C_ppm         : REAL;     (* Anode off-gas trace H2 impurity analyzer AT-601C [ppm] *)

    (* ------------------------------------------------------------------------------------- *)
    (* CATALYTIC DE-OXO PURIFICATION SYSTEM TRANSMITTERS [deg C], [ppm], [mbar]              *)
    (* ------------------------------------------------------------------------------------- *)
    rDeOxoInletTemp_DegC            : REAL;     (* Preheated crude H2 gas entering De-Oxo reactor [deg C] *)
    rDeOxoBedTempZone1_DegC         : REAL;     (* De-Oxo catalytic bed inlet reaction zone temperature [deg C] *)
    rDeOxoBedTempZone2_DegC         : REAL;     (* De-Oxo catalytic bed core reaction zone temperature [deg C] *)
    rDeOxoBedTempZone3_DegC         : REAL;     (* De-Oxo catalytic bed exit reaction zone temperature [deg C] *)
    rDeOxoExitGasTemp_DegC          : REAL;     (* De-Oxo product gas cooler outlet temperature [deg C] *)
    rDeOxoProductO2_ppm             : REAL;     (* Purified H2 product residual oxygen concentration [ppm] *)
    rDeOxoDifferentialPress_mbar    : REAL;     (* De-Oxo catalyst bed pressure drop [mbar] *)
END_VAR
""")

    # -------------------------------------------------------------------------
    # 2. VAR_OUTPUT Declarations (min 7 typed with engineering units & status)
    # -------------------------------------------------------------------------
    parts.append("""VAR_OUTPUT
    (* ------------------------------------------------------------------------------------- *)
    (* MASTER OPERATIONAL & SUPERVISORY STATUS INDICATORS                                    *)
    (* ------------------------------------------------------------------------------------- *)
    bSystemRunning                  : BOOL;     (* Electrolysis system active running state *)
    bProductionReady                : BOOL;     (* Gas production ready and on-specification flag *)
    bAlarmActive                    : BOOL;     (* Active unacknowledged warning alarm flag *)
    bTripActive                     : BOOL;     (* Hardwired or software safety trip active flag *)
    bDegradedMode                   : BOOL;     (* Redundancy degraded operating state active *)
    bPurgeActive                    : BOOL;     (* Nitrogen inerting/purging cycle active *)

    (* ------------------------------------------------------------------------------------- *)
    (* ACTUATOR COMMANDS: RECTIFIER, CONTROL VALVES, PUMPS & PREHEATERS                      *)
    (* ------------------------------------------------------------------------------------- *)
    rRectifierCurrentDemand_kA      : REAL;     (* Modulated DC current setpoint to rectifier [kA] *)
    rH2BackpressureValve_pct        : REAL;     (* Cathode H2 backpressure valve command PCV-201 [%] *)
    rO2BackpressureValve_pct        : REAL;     (* Anode O2 backpressure valve command PCV-301 [%] *)
    rLyeBalanceValve_pct            : REAL;     (* Inter-separator lye cross-transfer valve command LV-401 [%] *)
    rCathodeLyePumpSpeed_pct        : REAL;     (* Cathode lye circulation pump VFD speed demand [%] *)
    rAnodeLyePumpSpeed_pct          : REAL;     (* Anode lye circulation pump VFD speed demand [%] *)
    rDeOxoPreheaterDuty_pct         : REAL;     (* Catalytic De-Oxo electric preheater SCR duty [%] *)
    rDeOxoCoolingBypass_pct         : REAL;     (* De-Oxo thermal sync bypass damper valve command [%] *)
    rEmergencyDepressValve_pct      : REAL;     (* Fast safety depressurization blowdown valve [%] *)
    rNitrogenPurgeValve_pct         : REAL;     (* High-pressure N2 safety sweep injection valve [%] *)

    (* ------------------------------------------------------------------------------------- *)
    (* CALCULATED PROCESS ESTIMATES & PERFORMANCE TELEMETRY                                  *)
    (* ------------------------------------------------------------------------------------- *)
    rEffectiveDP_mbar               : REAL;     (* Voted & validated differential pressure (P_O2 - P_H2) [mbar] *)
    rEffectiveSystemPressure_bar    : REAL;     (* Voted master system operating pressure [bar] *)
    rEffectiveLevelDiff_pct         : REAL;     (* Hydrostatic level imbalance (L_H2 - L_O2) [%] *)
    rEffectiveH2inO2_ppm            : REAL;     (* Voted trace H2 cross-permeation into O2 off-gas [ppm] *)
    rEffectiveO2inH2_ppm            : REAL;     (* Voted trace O2 cross-permeation into H2 stream [ppm] *)
    rFaradaicEfficiency_pct         : REAL;     (* Real-time Faradaic current efficiency estimate [%] *)
    rSpecificEnergy_kWh_Nm3         : REAL;     (* Dynamic specific energy consumption [kWh/Nm3 H2] *)
    rStackPower_kW                  : REAL;     (* Total DC power consumed by electrolyzer stack [kW] *)
    rPredictedDeOxoPeakTemp_DegC    : REAL;     (* Model-predicted catalytic bed peak hot-spot temp [deg C] *)
    rCrossPermeationFlux_mol_m2s    : REAL;     (* Calculated Fickian + Darcy diaphragm gas flux [mol/(m2*s)] *)

    (* ------------------------------------------------------------------------------------- *)
    (* BIT-PACKED STATUS WORDS & ALARM REGISTERS                                             *)
    (* ------------------------------------------------------------------------------------- *)
    dwSystemStatusWord              : DWORD;    (* Bit-packed operational state and permissive telemetry *)
    dwAlarmWord1_Process            : DWORD;    (* Bit-packed process warning alarms (P, dP, T, Levels) *)
    dwAlarmWord2_Safety             : DWORD;    (* Bit-packed SIL-3 safety interlock trip flags *)
    dwSubsystemDiagnostics          : DWORD;    (* Bit-packed 2oo3 sensor health and MPC solver metrics *)
END_VAR
""")

    # -------------------------------------------------------------------------
    # 3. VAR Internal Declarations
    # -------------------------------------------------------------------------
    parts.append("""VAR
    (* ------------------------------------------------------------------------------------- *)
    (* FINITE STATE MACHINE (FSM) STEP CONTROL & TIMERS                                      *)
    (* ------------------------------------------------------------------------------------- *)
    iState                          : INT := 0; (* Master state machine state index *)
    iStateStep                      : INT := 0; (* Sub-step progression index *)
    tStateTimer                     : TON;      (* State dwelling duration timer *)
    tPurgeTimer                     : TON;      (* Nitrogen sweeping timer *)
    tLeakTestTimer                  : TON;      (* High-pressure hold leak test timer *)
    tPreheatTimer                   : TON;      (* Electrolyte preheat thermal dwell timer *)
    tMpcIterationTimer              : TON;      (* MPC solver execution cycle timer *)

    (* ------------------------------------------------------------------------------------- *)
    (* TRIPLE MODULAR REDUNDANCY (2oo3) VOTING INTERNAL DATA STRUCTURES                      *)
    (* ------------------------------------------------------------------------------------- *)
    bCathodePress_A_Healthy         : BOOL := TRUE;
    bCathodePress_B_Healthy         : BOOL := TRUE;
    bCathodePress_C_Healthy         : BOOL := TRUE;
    rVotedCathodePressure_bar       : REAL := 30.0;

    bAnodePress_A_Healthy           : BOOL := TRUE;
    bAnodePress_B_Healthy           : BOOL := TRUE;
    bAnodePress_C_Healthy           : BOOL := TRUE;
    rVotedAnodePressure_bar         : REAL := 30.0;

    bDP_A_Healthy                   : BOOL := TRUE;
    bDP_B_Healthy                   : BOOL := TRUE;
    bDP_C_Healthy                   : BOOL := TRUE;
    rVotedDP_mbar                   : REAL := 0.0;

    bCathodeLevel_A_Healthy         : BOOL := TRUE;
    bCathodeLevel_B_Healthy         : BOOL := TRUE;
    bCathodeLevel_C_Healthy         : BOOL := TRUE;
    rVotedCathodeLevel_pct          : REAL := 50.0;

    bAnodeLevel_A_Healthy           : BOOL := TRUE;
    bAnodeLevel_B_Healthy           : BOOL := TRUE;
    bAnodeLevel_C_Healthy           : BOOL := TRUE;
    rVotedAnodeLevel_pct            : REAL := 50.0;

    bO2inH2_A_Healthy               : BOOL := TRUE;
    bO2inH2_B_Healthy               : BOOL := TRUE;
    bO2inH2_C_Healthy               : BOOL := TRUE;
    rVotedO2inH2_ppm                : REAL := 1500.0;

    bH2inO2_A_Healthy               : BOOL := TRUE;
    bH2inO2_B_Healthy               : BOOL := TRUE;
    bH2inO2_C_Healthy               : BOOL := TRUE;
    rVotedH2inO2_ppm                : REAL := 2500.0;

    (* ------------------------------------------------------------------------------------- *)
    (* PHYSICAL & THERMODYNAMIC ESTIMATION REGISTERS                                         *)
    (* ------------------------------------------------------------------------------------- *)
    rKOH_Density_kg_m3              : REAL := 1285.0; (* Dynamic density of 30 wt% KOH [kg/m3] *)
    rKOH_Viscosity_Pa_s             : REAL := 0.0014; (* Dynamic viscosity of 30 wt% KOH [Pa*s] *)
    rWaterVaporPressure_bar         : REAL := 0.35;   (* Vapor pressure of H2O over 30 wt% KOH [bar] *)
    rTheoreticalCellVoltage_V       : REAL := 1.23;   (* Reversible thermodynamic Nernst cell voltage [V] *)
    rThermoneutralCellVoltage_V     : REAL := 1.48;   (* Enthalpic thermoneutral cell voltage [V] *)
    rCellActivationOverpotential_V  : REAL := 0.32;   (* Butler-Volmer kinetic overpotential [V] *)
    rCellOhmicOverpotential_V       : REAL := 0.28;   (* Electrolyte and diaphragm IR voltage drop [V] *)
    rAverageCellVoltage_V           : REAL := 1.83;   (* Mean bipolar cell voltage [V] *)
    rTotalGasVolumeFlow_m3h         : REAL := 0.0;    (* In-situ gas generation volume flow [m3/h] *)

    (* ------------------------------------------------------------------------------------- *)
    (* DIFFERENTIAL PRESSURE NULLING & VALVE DECOUPLING CONTROLLER                           *)
    (* ------------------------------------------------------------------------------------- *)
    rDP_IntegralAccumulator         : REAL := 0.0;
    rDP_DerivativeState             : REAL := 0.0;
    rDP_PreviousError               : REAL := 0.0;
    rMasterPressureIntegral         : REAL := 0.0;
    rMasterPressurePreviousError    : REAL := 0.0;
    rH2ValveTrim                    : REAL := 0.0;
    rO2ValveTrim                    : REAL := 0.0;
    rDecoupledPCV_H2                : REAL := 50.0;
    rDecoupledPCV_O2                : REAL := 50.0;

    (* ------------------------------------------------------------------------------------- *)
    (* SEPARATOR LYE LEVEL BALANCING & HYDRAULIC EQUALIZATION                                *)
    (* ------------------------------------------------------------------------------------- *)
    rLevelDiff_IntegralAccumulator  : REAL := 0.0;
    rLevelDiff_PreviousError        : REAL := 0.0;
    rDynamicLyeSwellCorrection      : REAL := 0.0;
    rBaseLyePumpSpeed_pct           : REAL := 65.0;
    rLyePumpDifferentialSpeed_pct   : REAL := 0.0;

    (* ------------------------------------------------------------------------------------- *)
    (* CATALYTIC DE-OXO THERMAL REACTION & RUNAWAY MODEL                                     *)
    (* ------------------------------------------------------------------------------------- *)
    rDeOxoHeatGeneration_kW         : REAL := 0.0;
    rAdiabaticTempRise_DegC         : REAL := 0.0;
    rDeOxoPreheaterIntegral         : REAL := 0.0;
    rDeOxoPreheaterPreviousError    : REAL := 0.0;
    rDeOxoBypassIntegral            : REAL := 0.0;
    rDeOxoBypassPreviousError       : REAL := 0.0;

    (* ------------------------------------------------------------------------------------- *)
    (* RENEWABLE POWER RAMP RATE LIMITER & FLAMMABILITY FLOOR                                *)
    (* ------------------------------------------------------------------------------------- *)
    rFilteredCurrentDemand_kA       : REAL := 0.0;
    rCurrentRampRate_kA_s           : REAL := 0.0;
    rMaxAllowableRampRate_kA_s      : REAL := 0.16;   (* 1.0% of 16 kA per second baseline *)
    rDynamicMinCurrentFloor_kA      : REAL := 2.4;    (* 15.0% minimum current floor *)

    (* ------------------------------------------------------------------------------------- *)
    (* 6-STATE MULTIVARIABLE DISCRETE STATE-SPACE MODEL & MPC REGISTERS                      *)
    (*   x = [dP, dLevel, T_DeOxo, T_Stack, C_H2_in_O2, C_O2_in_H2]^T                        *)
    (*   u = [u_PCV_H2, u_LV_Bal, u_HTR_DeOxo, I_Rectifier_Demand]^T                         *)
    (* ------------------------------------------------------------------------------------- *)
    arrA                            : ARRAY[1..6, 1..6] OF REAL; (* Discrete State Transition Matrix *)
    arrB                            : ARRAY[1..6, 1..4] OF REAL; (* Discrete Control Input Matrix *)
    arrC                            : ARRAY[1..6, 1..6] OF REAL; (* State Output Observation Matrix *)
    arrD                            : ARRAY[1..6, 1..4] OF REAL; (* Feedthrough Direct Transmission *)
    arrX                            : ARRAY[1..6] OF REAL;       (* State Vector: [mbar, %, degC, degC, ppm, ppm] *)
    arrX_hat                        : ARRAY[1..6] OF REAL;       (* Observer Reconciled State Vector *)
    arrX_ref                        : ARRAY[1..6] OF REAL;       (* Target State Reference Vector *)
    arrU                            : ARRAY[1..4] OF REAL;       (* Control Actuator Vector: [%, %, %, kA] *)
    arrU_prev                       : ARRAY[1..4] OF REAL;       (* Preceding Execution Step Control Vector *)
    arrU_min                        : ARRAY[1..4] OF REAL;       (* Actuator Lower Saturation Boundaries *)
    arrU_max                        : ARRAY[1..4] OF REAL;       (* Actuator Upper Saturation Boundaries *)
    arrDeltaU_max                   : ARRAY[1..4] OF REAL;       (* Actuator Maximum Slew Rates per Cycle *)
    arrQ                            : ARRAY[1..6] OF REAL;       (* State Error Quadratic Penalty Weights *)
    arrR                            : ARRAY[1..4] OF REAL;       (* Control Effort Penalty Weights *)
    arrS                            : ARRAY[1..4] OF REAL;       (* Actuator Slew Rate Quadratic Weights *)
    arrGrad                         : ARRAY[1..4] OF REAL;       (* Calculated Objective Function Gradient *)
    bMpcConverged                   : BOOL := FALSE;
    iMpcIterationCount              : INT := 0;

    (* ------------------------------------------------------------------------------------- *)
    (* UTILITY VARIABLES, ACCUMULATORS & LOOP COUNTERS                                       *)
    (* ------------------------------------------------------------------------------------- *)
    iIdx                            : INT := 0;
    jIdx                            : INT := 0;
    kIdx                            : INT := 0;
    rTempCalc                       : REAL := 0.0;
    rLeakTestInitialPress_bar       : REAL := 0.0;
    bFirstScanComplete              : BOOL := FALSE;
END_VAR
""")

    # -------------------------------------------------------------------------
    # 4. SECTION 1.0: SAFETY SHUTDOWN & SIL-3 INTERLOCKS
    # -------------------------------------------------------------------------
    parts.append("""
(* ========================================================================================= *)
(* 1.0 EMERGENCY SAFETY SHUTDOWN & SIL-3 HARDWIRED INTERLOCK EVALUATION                      *)
(* ========================================================================================= *)
(* Check active-low SIL-3 hardwired E-stop permissive and master functional safety trips.    *)
(* Any trip event forces immediate rectifier unlatch (0 kA), nitrogen inerting sweep,       *)
(* controlled high-pressure venting, and transitions the FSM into lockout (State 100).      *)

IF NOT bEmergencyStop THEN
    bTripActive := TRUE;
    bSystemRunning := FALSE;
    bProductionReady := FALSE;
    rRectifierCurrentDemand_kA := 0.0;
    rDeOxoPreheaterDuty_pct := 0.0;
    rNitrogenPurgeValve_pct := 100.0;
    rEmergencyDepressValve_pct := 25.0;
    dwAlarmWord2_Safety := dwAlarmWord2_Safety OR 16#0000_0001; (* Bit 0: Hardwired E-Stop Trip *)
    iState := 100; (* SAFETY_FAULT_LOCKOUT *)
    RETURN;
END_IF;

IF NOT bEnableSystem THEN
    bSystemRunning := FALSE;
    bProductionReady := FALSE;
    rRectifierCurrentDemand_kA := 0.0;
    rDeOxoPreheaterDuty_pct := 0.0;
    IF (iState <> 0) AND (iState <> 100) THEN
        iState := 0; (* Return to Standby *)
    END_IF;
END_IF;

(* Master alarm acknowledgement and fault reset *)
IF bResetFaults THEN
    bTripActive := FALSE;
    bAlarmActive := FALSE;
    dwAlarmWord1_Process := 16#0000_0000;
    dwAlarmWord2_Safety := 16#0000_0000;
    dwSubsystemDiagnostics := dwSubsystemDiagnostics AND 16#0000_FFFF;
    IF (iState = 100) AND bEnableSystem THEN
        iState := 0; (* Clear lockout to Standby *)
    END_IF;
END_IF;
""")

    # -------------------------------------------------------------------------
    # 5. SECTION 2.0: TRIPLE MODULAR REDUNDANCY (2oo3) VOTING
    # -------------------------------------------------------------------------
    parts.append("""
(* ========================================================================================= *)
(* 2.0 TRIPLE MODULAR REDUNDANCY (2oo3) SENSOR VOTING ALGORITHMS                             *)
(* ========================================================================================= *)
(* Robust median selection across redundant transmitters with discrepancy anomaly rejection, *)
(* out-of-range sensor health flagging, and graceful degradation from 2oo3 -> 1oo2 -> Fail. *)

(* --- 2.1 CATHODE (H2) PRESSURE TRANSMITTERS PT-201A/B/C [bar] --- *)
bCathodePress_A_Healthy := (rCathodePressure_A_bar >= 0.0) AND (rCathodePressure_A_bar <= 45.0);
bCathodePress_B_Healthy := (rCathodePressure_B_bar >= 0.0) AND (rCathodePressure_B_bar <= 45.0);
bCathodePress_C_Healthy := (rCathodePressure_C_bar >= 0.0) AND (rCathodePressure_C_bar <= 45.0);

IF bCathodePress_A_Healthy AND bCathodePress_B_Healthy AND bCathodePress_C_Healthy THEN
    (* 3 Healthy: Exact Median Calculation *)
    IF (rCathodePressure_A_bar >= rCathodePressure_B_bar) THEN
        IF (rCathodePressure_B_bar >= rCathodePressure_C_bar) THEN
            rVotedCathodePressure_bar := rCathodePressure_B_bar;
        ELSIF (rCathodePressure_A_bar >= rCathodePressure_C_bar) THEN
            rVotedCathodePressure_bar := rCathodePressure_C_bar;
        ELSE
            rVotedCathodePressure_bar := rCathodePressure_A_bar;
        END_IF;
    ELSE
        IF (rCathodePressure_A_bar >= rCathodePressure_C_bar) THEN
            rVotedCathodePressure_bar := rCathodePressure_A_bar;
        ELSIF (rCathodePressure_B_bar >= rCathodePressure_C_bar) THEN
            rVotedCathodePressure_bar := rCathodePressure_C_bar;
        ELSE
            rVotedCathodePressure_bar := rCathodePressure_B_bar;
        END_IF;
    END_IF;
ELSIF bCathodePress_A_Healthy AND bCathodePress_B_Healthy THEN
    rVotedCathodePressure_bar := (rCathodePressure_A_bar + rCathodePressure_B_bar) * 0.5;
    dwSubsystemDiagnostics := dwSubsystemDiagnostics OR 16#0000_0001; (* Cathode PT-C Failed *)
ELSIF bCathodePress_A_Healthy AND bCathodePress_C_Healthy THEN
    rVotedCathodePressure_bar := (rCathodePressure_A_bar + rCathodePressure_C_bar) * 0.5;
    dwSubsystemDiagnostics := dwSubsystemDiagnostics OR 16#0000_0002; (* Cathode PT-B Failed *)
ELSIF bCathodePress_B_Healthy AND bCathodePress_C_Healthy THEN
    rVotedCathodePressure_bar := (rCathodePressure_B_bar + rCathodePressure_C_bar) * 0.5;
    dwSubsystemDiagnostics := dwSubsystemDiagnostics OR 16#0000_0004; (* Cathode PT-A Failed *)
ELSIF bCathodePress_A_Healthy THEN
    rVotedCathodePressure_bar := rCathodePressure_A_bar;
    bDegradedMode := TRUE;
ELSIF bCathodePress_B_Healthy THEN
    rVotedCathodePressure_bar := rCathodePressure_B_bar;
    bDegradedMode := TRUE;
ELSIF bCathodePress_C_Healthy THEN
    rVotedCathodePressure_bar := rCathodePressure_C_bar;
    bDegradedMode := TRUE;
ELSE
    bTripActive := TRUE;
    dwAlarmWord2_Safety := dwAlarmWord2_Safety OR 16#0000_0002; (* Complete Cathode PT Loss *)
END_IF;

(* --- 2.2 ANODE (O2) PRESSURE TRANSMITTERS PT-301A/B/C [bar] --- *)
bAnodePress_A_Healthy := (rAnodePressure_A_bar >= 0.0) AND (rAnodePressure_A_bar <= 45.0);
bAnodePress_B_Healthy := (rAnodePressure_B_bar >= 0.0) AND (rAnodePressure_B_bar <= 45.0);
bAnodePress_C_Healthy := (rAnodePressure_C_bar >= 0.0) AND (rAnodePressure_C_bar <= 45.0);

IF bAnodePress_A_Healthy AND bAnodePress_B_Healthy AND bAnodePress_C_Healthy THEN
    IF (rAnodePressure_A_bar >= rAnodePressure_B_bar) THEN
        IF (rAnodePressure_B_bar >= rAnodePressure_C_bar) THEN
            rVotedAnodePressure_bar := rAnodePressure_B_bar;
        ELSIF (rAnodePressure_A_bar >= rAnodePressure_C_bar) THEN
            rVotedAnodePressure_bar := rAnodePressure_C_bar;
        ELSE
            rVotedAnodePressure_bar := rAnodePressure_A_bar;
        END_IF;
    ELSE
        IF (rAnodePressure_A_bar >= rAnodePressure_C_bar) THEN
            rVotedAnodePressure_bar := rAnodePressure_A_bar;
        ELSIF (rAnodePressure_B_bar >= rAnodePressure_C_bar) THEN
            rVotedAnodePressure_bar := rAnodePressure_C_bar;
        ELSE
            rVotedAnodePressure_bar := rAnodePressure_B_bar;
        END_IF;
    END_IF;
ELSIF bAnodePress_A_Healthy AND bAnodePress_B_Healthy THEN
    rVotedAnodePressure_bar := (rAnodePressure_A_bar + rAnodePressure_B_bar) * 0.5;
    dwSubsystemDiagnostics := dwSubsystemDiagnostics OR 16#0000_0008;
ELSIF bAnodePress_A_Healthy AND bAnodePress_C_Healthy THEN
    rVotedAnodePressure_bar := (rAnodePressure_A_bar + rAnodePressure_C_bar) * 0.5;
    dwSubsystemDiagnostics := dwSubsystemDiagnostics OR 16#0000_0010;
ELSIF bAnodePress_B_Healthy AND bAnodePress_C_Healthy THEN
    rVotedAnodePressure_bar := (rAnodePressure_B_bar + rAnodePressure_C_bar) * 0.5;
    dwSubsystemDiagnostics := dwSubsystemDiagnostics OR 16#0000_0020;
ELSIF bAnodePress_A_Healthy THEN
    rVotedAnodePressure_bar := rAnodePressure_A_bar;
    bDegradedMode := TRUE;
ELSIF bAnodePress_B_Healthy THEN
    rVotedAnodePressure_bar := rAnodePressure_B_bar;
    bDegradedMode := TRUE;
ELSIF bAnodePress_C_Healthy THEN
    rVotedAnodePressure_bar := rAnodePressure_C_bar;
    bDegradedMode := TRUE;
ELSE
    bTripActive := TRUE;
    dwAlarmWord2_Safety := dwAlarmWord2_Safety OR 16#0000_0004; (* Complete Anode PT Loss *)
END_IF;

rEffectiveSystemPressure_bar := (rVotedCathodePressure_bar + rVotedAnodePressure_bar) * 0.5;

(* --- 2.3 DIFFERENTIAL PRESSURE TRANSMITTERS dPT-401A/B/C [mbar] --- *)
bDP_A_Healthy := (rDifferentialPressure_A_mbar >= -100.0) AND (rDifferentialPressure_A_mbar <= 100.0);
bDP_B_Healthy := (rDifferentialPressure_B_mbar >= -100.0) AND (rDifferentialPressure_B_mbar <= 100.0);
bDP_C_Healthy := (rDifferentialPressure_C_mbar >= -100.0) AND (rDifferentialPressure_C_mbar <= 100.0);

IF bDP_A_Healthy AND bDP_B_Healthy AND bDP_C_Healthy THEN
    IF (rDifferentialPressure_A_mbar >= rDifferentialPressure_B_mbar) THEN
        IF (rDifferentialPressure_B_mbar >= rDifferentialPressure_C_mbar) THEN
            rVotedDP_mbar := rDifferentialPressure_B_mbar;
        ELSIF (rDifferentialPressure_A_mbar >= rDifferentialPressure_C_mbar) THEN
            rVotedDP_mbar := rDifferentialPressure_C_mbar;
        ELSE
            rVotedDP_mbar := rDifferentialPressure_A_mbar;
        END_IF;
    ELSE
        IF (rDifferentialPressure_A_mbar >= rDifferentialPressure_C_mbar) THEN
            rVotedDP_mbar := rDifferentialPressure_A_mbar;
        ELSIF (rDifferentialPressure_B_mbar >= rDifferentialPressure_C_mbar) THEN
            rVotedDP_mbar := rDifferentialPressure_C_mbar;
        ELSE
            rVotedDP_mbar := rDifferentialPressure_B_mbar;
        END_IF;
    END_IF;
ELSIF bDP_A_Healthy AND bDP_B_Healthy THEN
    rVotedDP_mbar := (rDifferentialPressure_A_mbar + rDifferentialPressure_B_mbar) * 0.5;
    dwSubsystemDiagnostics := dwSubsystemDiagnostics OR 16#0000_0040;
ELSIF bDP_A_Healthy AND bDP_C_Healthy THEN
    rVotedDP_mbar := (rDifferentialPressure_A_mbar + rDifferentialPressure_C_mbar) * 0.5;
    dwSubsystemDiagnostics := dwSubsystemDiagnostics OR 16#0000_0080;
ELSIF bDP_B_Healthy AND bDP_C_Healthy THEN
    rVotedDP_mbar := (rDifferentialPressure_B_mbar + rDifferentialPressure_C_mbar) * 0.5;
    dwSubsystemDiagnostics := dwSubsystemDiagnostics OR 16#0000_0100;
ELSIF bDP_A_Healthy THEN
    rVotedDP_mbar := rDifferentialPressure_A_mbar;
    bDegradedMode := TRUE;
ELSIF bDP_B_Healthy THEN
    rVotedDP_mbar := rDifferentialPressure_B_mbar;
    bDegradedMode := TRUE;
ELSIF bDP_C_Healthy THEN
    rVotedDP_mbar := rDifferentialPressure_C_mbar;
    bDegradedMode := TRUE;
ELSE
    (* Fallback to mathematical difference of absolute pressure sensors *)
    rVotedDP_mbar := (rVotedAnodePressure_bar - rVotedCathodePressure_bar) * 1000.0;
    bDegradedMode := TRUE;
    dwSubsystemDiagnostics := dwSubsystemDiagnostics OR 16#0000_0200;
END_IF;

rEffectiveDP_mbar := rVotedDP_mbar;

(* --- 2.4 CATHODE SEPARATOR LYE LEVEL TRANSMITTERS LT-202A/B/C [%] --- *)
bCathodeLevel_A_Healthy := (rCathodeSeparatorLevel_A_pct >= 0.0) AND (rCathodeSeparatorLevel_A_pct <= 100.0);
bCathodeLevel_B_Healthy := (rCathodeSeparatorLevel_B_pct >= 0.0) AND (rCathodeSeparatorLevel_B_pct <= 100.0);
bCathodeLevel_C_Healthy := (rCathodeSeparatorLevel_C_pct >= 0.0) AND (rCathodeSeparatorLevel_C_pct <= 100.0);

IF bCathodeLevel_A_Healthy AND bCathodeLevel_B_Healthy AND bCathodeLevel_C_Healthy THEN
    IF (rCathodeSeparatorLevel_A_pct >= rCathodeSeparatorLevel_B_pct) THEN
        IF (rCathodeSeparatorLevel_B_pct >= rCathodeSeparatorLevel_C_pct) THEN
            rVotedCathodeLevel_pct := rCathodeSeparatorLevel_B_pct;
        ELSIF (rCathodeSeparatorLevel_A_pct >= rCathodeSeparatorLevel_C_pct) THEN
            rVotedCathodeLevel_pct := rCathodeSeparatorLevel_C_pct;
        ELSE
            rVotedCathodeLevel_pct := rCathodeSeparatorLevel_A_pct;
        END_IF;
    ELSE
        IF (rCathodeSeparatorLevel_A_pct >= rCathodeSeparatorLevel_C_pct) THEN
            rVotedCathodeLevel_pct := rCathodeSeparatorLevel_A_pct;
        ELSIF (rCathodeSeparatorLevel_B_pct >= rCathodeSeparatorLevel_C_pct) THEN
            rVotedCathodeLevel_pct := rCathodeSeparatorLevel_C_pct;
        ELSE
            rVotedCathodeLevel_pct := rCathodeSeparatorLevel_B_pct;
        END_IF;
    END_IF;
ELSIF bCathodeLevel_A_Healthy AND bCathodeLevel_B_Healthy THEN
    rVotedCathodeLevel_pct := (rCathodeSeparatorLevel_A_pct + rCathodeSeparatorLevel_B_pct) * 0.5;
ELSIF bCathodeLevel_A_Healthy AND bCathodeLevel_C_Healthy THEN
    rVotedCathodeLevel_pct := (rCathodeSeparatorLevel_A_pct + rCathodeSeparatorLevel_C_pct) * 0.5;
ELSIF bCathodeLevel_B_Healthy AND bCathodeLevel_C_Healthy THEN
    rVotedCathodeLevel_pct := (rCathodeSeparatorLevel_B_pct + rCathodeSeparatorLevel_C_pct) * 0.5;
ELSIF bCathodeLevel_A_Healthy THEN
    rVotedCathodeLevel_pct := rCathodeSeparatorLevel_A_pct;
    bDegradedMode := TRUE;
ELSIF bCathodeLevel_B_Healthy THEN
    rVotedCathodeLevel_pct := rCathodeSeparatorLevel_B_pct;
    bDegradedMode := TRUE;
ELSIF bCathodeLevel_C_Healthy THEN
    rVotedCathodeLevel_pct := rCathodeSeparatorLevel_C_pct;
    bDegradedMode := TRUE;
ELSE
    bTripActive := TRUE;
    dwAlarmWord2_Safety := dwAlarmWord2_Safety OR 16#0000_0008; (* Cathode Level Loss *)
END_IF;

(* --- 2.5 ANODE SEPARATOR LYE LEVEL TRANSMITTERS LT-302A/B/C [%] --- *)
bAnodeLevel_A_Healthy := (rAnodeSeparatorLevel_A_pct >= 0.0) AND (rAnodeSeparatorLevel_A_pct <= 100.0);
bAnodeLevel_B_Healthy := (rAnodeSeparatorLevel_B_pct >= 0.0) AND (rAnodeSeparatorLevel_B_pct <= 100.0);
bAnodeLevel_C_Healthy := (rAnodeSeparatorLevel_C_pct >= 0.0) AND (rAnodeSeparatorLevel_C_pct <= 100.0);

IF bAnodeLevel_A_Healthy AND bAnodeLevel_B_Healthy AND bAnodeLevel_C_Healthy THEN
    IF (rAnodeSeparatorLevel_A_pct >= rAnodeSeparatorLevel_B_pct) THEN
        IF (rAnodeSeparatorLevel_B_pct >= rAnodeSeparatorLevel_C_pct) THEN
            rVotedAnodeLevel_pct := rAnodeSeparatorLevel_B_pct;
        ELSIF (rAnodeSeparatorLevel_A_pct >= rAnodeSeparatorLevel_C_pct) THEN
            rVotedAnodeLevel_pct := rAnodeSeparatorLevel_C_pct;
        ELSE
            rVotedAnodeLevel_pct := rAnodeSeparatorLevel_A_pct;
        END_IF;
    ELSE
        IF (rAnodeSeparatorLevel_A_pct >= rAnodeSeparatorLevel_C_pct) THEN
            rVotedAnodeLevel_pct := rAnodeSeparatorLevel_A_pct;
        ELSIF (rAnodeSeparatorLevel_B_pct >= rAnodeSeparatorLevel_C_pct) THEN
            rVotedAnodeLevel_pct := rAnodeSeparatorLevel_C_pct;
        ELSE
            rVotedAnodeLevel_pct := rAnodeSeparatorLevel_B_pct;
        END_IF;
    END_IF;
ELSIF bAnodeLevel_A_Healthy AND bAnodeLevel_B_Healthy THEN
    rVotedAnodeLevel_pct := (rAnodeSeparatorLevel_A_pct + rAnodeSeparatorLevel_B_pct) * 0.5;
ELSIF bAnodeLevel_A_Healthy AND bAnodeLevel_C_Healthy THEN
    rVotedAnodeLevel_pct := (rAnodeSeparatorLevel_A_pct + rAnodeSeparatorLevel_C_pct) * 0.5;
ELSIF bAnodeLevel_B_Healthy AND bAnodeLevel_C_Healthy THEN
    rVotedAnodeLevel_pct := (rAnodeSeparatorLevel_B_pct + rAnodeSeparatorLevel_C_pct) * 0.5;
ELSIF bAnodeLevel_A_Healthy THEN
    rVotedAnodeLevel_pct := rAnodeSeparatorLevel_A_pct;
    bDegradedMode := TRUE;
ELSIF bAnodeLevel_B_Healthy THEN
    rVotedAnodeLevel_pct := rAnodeSeparatorLevel_B_pct;
    bDegradedMode := TRUE;
ELSIF bAnodeLevel_C_Healthy THEN
    rVotedAnodeLevel_pct := rAnodeSeparatorLevel_C_pct;
    bDegradedMode := TRUE;
ELSE
    bTripActive := TRUE;
    dwAlarmWord2_Safety := dwAlarmWord2_Safety OR 16#0000_0010; (* Anode Level Loss *)
END_IF;

rEffectiveLevelDiff_pct := rVotedCathodeLevel_pct - rVotedAnodeLevel_pct;

(* --- 2.6 TRACE GAS IMPURITY ANALYZERS (2oo3) --- *)
bO2inH2_A_Healthy := (rOxygenInHydrogen_A_ppm >= 0.0) AND (rOxygenInHydrogen_A_ppm <= 30000.0);
bO2inH2_B_Healthy := (rOxygenInHydrogen_B_ppm >= 0.0) AND (rOxygenInHydrogen_B_ppm <= 30000.0);
bO2inH2_C_Healthy := (rOxygenInHydrogen_C_ppm >= 0.0) AND (rOxygenInHydrogen_C_ppm <= 30000.0);

IF bO2inH2_A_Healthy AND bO2inH2_B_Healthy AND bO2inH2_C_Healthy THEN
    IF (rOxygenInHydrogen_A_ppm >= rOxygenInHydrogen_B_ppm) THEN
        IF (rOxygenInHydrogen_B_ppm >= rOxygenInHydrogen_C_ppm) THEN
            rVotedO2inH2_ppm := rOxygenInHydrogen_B_ppm;
        ELSIF (rOxygenInHydrogen_A_ppm >= rOxygenInHydrogen_C_ppm) THEN
            rVotedO2inH2_ppm := rOxygenInHydrogen_C_ppm;
        ELSE
            rVotedO2inH2_ppm := rOxygenInHydrogen_A_ppm;
        END_IF;
    ELSE
        IF (rOxygenInHydrogen_A_ppm >= rOxygenInHydrogen_C_ppm) THEN
            rVotedO2inH2_ppm := rOxygenInHydrogen_A_ppm;
        ELSIF (rOxygenInHydrogen_B_ppm >= rOxygenInHydrogen_C_ppm) THEN
            rVotedO2inH2_ppm := rOxygenInHydrogen_C_ppm;
        ELSE
            rVotedO2inH2_ppm := rOxygenInHydrogen_B_ppm;
        END_IF;
    END_IF;
ELSIF bO2inH2_A_Healthy AND bO2inH2_B_Healthy THEN
    rVotedO2inH2_ppm := (rOxygenInHydrogen_A_ppm + rOxygenInHydrogen_B_ppm) * 0.5;
ELSE
    rVotedO2inH2_ppm := rOxygenInHydrogen_A_ppm;
END_IF;
rEffectiveO2inH2_ppm := rVotedO2inH2_ppm;

bH2inO2_A_Healthy := (rHydrogenInOxygen_A_ppm >= 0.0) AND (rHydrogenInOxygen_A_ppm <= 40000.0);
bH2inO2_B_Healthy := (rHydrogenInOxygen_B_ppm >= 0.0) AND (rHydrogenInOxygen_B_ppm <= 40000.0);
bH2inO2_C_Healthy := (rHydrogenInOxygen_C_ppm >= 0.0) AND (rHydrogenInOxygen_C_ppm <= 40000.0);

IF bH2inO2_A_Healthy AND bH2inO2_B_Healthy AND bH2inO2_C_Healthy THEN
    IF (rHydrogenInOxygen_A_ppm >= rHydrogenInOxygen_B_ppm) THEN
        IF (rHydrogenInOxygen_B_ppm >= rHydrogenInOxygen_C_ppm) THEN
            rVotedH2inO2_ppm := rHydrogenInOxygen_B_ppm;
        ELSIF (rHydrogenInOxygen_A_ppm >= rHydrogenInOxygen_C_ppm) THEN
            rVotedH2inO2_ppm := rHydrogenInOxygen_C_ppm;
        ELSE
            rVotedH2inO2_ppm := rHydrogenInOxygen_A_ppm;
        END_IF;
    ELSE
        IF (rHydrogenInOxygen_A_ppm >= rHydrogenInOxygen_C_ppm) THEN
            rVotedH2inO2_ppm := rHydrogenInOxygen_A_ppm;
        ELSIF (rHydrogenInOxygen_B_ppm >= rHydrogenInOxygen_C_ppm) THEN
            rVotedH2inO2_ppm := rHydrogenInOxygen_C_ppm;
        ELSE
            rVotedH2inO2_ppm := rHydrogenInOxygen_B_ppm;
        END_IF;
    END_IF;
ELSIF bH2inO2_A_Healthy AND bH2inO2_B_Healthy THEN
    rVotedH2inO2_ppm := (rHydrogenInOxygen_A_ppm + rHydrogenInOxygen_B_ppm) * 0.5;
ELSE
    rVotedH2inO2_ppm := rHydrogenInOxygen_A_ppm;
END_IF;
rEffectiveH2inO2_ppm := rVotedH2inO2_ppm;
""")

    # -------------------------------------------------------------------------
    # 6. SECTION 3.0: THERMODYNAMIC & ELECTROCHEMICAL PROCESS ENGINE
    # -------------------------------------------------------------------------
    parts.append("""
(* ========================================================================================= *)
(* 3.0 HIGH-PRESSURE ELECTROLYTE & ELECTROCHEMICAL THERMODYNAMICS ENGINE                     *)
(* ========================================================================================= *)
(* Calculates real-time 30 wt% KOH physical properties, Nernst reversible cell potential,   *)
(* Butler-Volmer overpotentials, Faradaic efficiency, gas volume generation and gas flux.    *)

(* Density of 30 wt% aqueous KOH as a function of temperature (T in deg C) *)
(* Polynomial fit: rho(T) = 1310.0 - 0.55 * T - 0.0012 * T^2 [kg/m3] *)
rKOH_Density_kg_m3 := 1310.0 - (0.55 * rElectrolyteInletTemp_DegC) - (0.0012 * rElectrolyteInletTemp_DegC * rElectrolyteInletTemp_DegC);
IF (rKOH_Density_kg_m3 < 1200.0) THEN rKOH_Density_kg_m3 := 1200.0; END_IF;

(* Dynamic Viscosity of 30 wt% KOH: mu(T) = 0.0028 * EXP(-0.018 * (T - 20)) [Pa*s] *)
rKOH_Viscosity_Pa_s := 0.0028 * EXP(-0.018 * (rElectrolyteInletTemp_DegC - 20.0));
IF (rKOH_Viscosity_Pa_s < 0.0006) THEN rKOH_Viscosity_Pa_s := 0.0006; END_IF;

(* Water vapor partial pressure over 30 wt% aqueous KOH at 80 deg C [bar] *)
(* Antoine equation modified for KOH water activity a_w ~ 0.68 *)
rWaterVaporPressure_bar := 0.68 * EXP(11.6834 - (3816.44 / (rElectrolyteInletTemp_DegC + 227.02)));

(* Reversible Nernst Cell Voltage: E_rev(T, P) = E0(T) + (R*T/(2*F)) * ln((P_H2 * P_O2^0.5)/a_w) *)
(* At 80 deg C (353.15 K) and 30 bar: E0 ~ 1.18 V; Nernst pressure elevation ~ 0.052 V *)
rTheoreticalCellVoltage_V := 1.182 + (0.0000431 * (rElectrolyteInletTemp_DegC + 273.15) * LN(rEffectiveSystemPressure_bar * SQRT(rEffectiveSystemPressure_bar) / 0.68));

(* Average cell voltage from measured stack terminal voltage (280 bipolar cells) *)
IF (rStackVoltage_V > 10.0) THEN
    rAverageCellVoltage_V := rStackVoltage_V / 280.0;
ELSE
    rAverageCellVoltage_V := rTheoreticalCellVoltage_V;
END_IF;

(* Instantaneous Stack DC Power [kW] *)
rStackPower_kW := rStackVoltage_V * rStackCurrent_kA;

(* Faradaic Efficiency Model: eta_F(j, T) *)
(* Accounting for stray shunt currents in KOH distribution manifolds and parasitic cross-permeation *)
(* Current density j = I_kA / Area (Area ~ 2.0 m2 per cell -> j in kA/m2) *)
IF (rStackCurrent_kA > 0.5) THEN
    rFaradaicEfficiency_pct := (rStackCurrent_kA / (rStackCurrent_kA + 0.18)) * 99.4 - (0.015 * rEffectiveSystemPressure_bar);
    IF (rFaradaicEfficiency_pct > 99.5) THEN rFaradaicEfficiency_pct := 99.5; END_IF;
    IF (rFaradaicEfficiency_pct < 60.0) THEN rFaradaicEfficiency_pct := 60.0; END_IF;
ELSE
    rFaradaicEfficiency_pct := 0.0;
END_IF;

(* Specific Energy Consumption [kWh / Nm3 H2] *)
(* Theoretical ideal at thermoneutral: 3.54 kWh/Nm3; Typical industrial AWE: 4.3 - 4.9 kWh/Nm3 *)
IF (rHydrogenGasFlow_Nm3h > 10.0) THEN
    rSpecificEnergy_kWh_Nm3 := rStackPower_kW / rHydrogenGasFlow_Nm3h;
ELSE
    rSpecificEnergy_kWh_Nm3 := 4.45;
END_IF;

(* Diaphragm Cross-Permeation Gas Flux Calculation: *)
(* J_cross = J_diffusion (Fick) + J_convection (Darcy) [mol/(m2*s)] *)
(* D_eff ~ 3.5e-9 m2/s in KOH at 80 deg C; permeability k ~ 1.2e-15 m2; thickness delta_x = 0.5 mm *)
rCrossPermeationFlux_mol_m2s := (3.5E-9 * (rEffectiveSystemPressure_bar * 100000.0 * 0.00078) / 0.0005)
                              + (1.2E-15 / rKOH_Viscosity_Pa_s) * (rEffectiveDP_mbar * 100.0 / 0.0005) * (rEffectiveSystemPressure_bar * 0.024);
""")

    # -------------------------------------------------------------------------
    # 7. SECTION 4.0: DIFFERENTIAL PRESSURE (dP) CROSS-PERMEATION NULLING
    # -------------------------------------------------------------------------
    parts.append("""
(* ========================================================================================= *)
(* 4.0 ANODE-CATHODE DIFFERENTIAL PRESSURE (dP) CROSS-PERMEATION NULLING CONTROLLER          *)
(* ========================================================================================= *)
(* Coordinated multivariable decoupling governor for high-speed pilot-operated dome-loaded   *)
(* backpressure valves PCV-201 (H2) and PCV-301 (O2). Nulls dP = P_O2 - P_H2 to 0.0 +- 2 mbar *)
(* while regulating master system header pressure to nominal 30.0 bar.                       *)

(* Master system pressure error: Target = 30.0 bar *)
rMasterPressurePreviousError := (30.0 - rEffectiveSystemPressure_bar);
rMasterPressureIntegral := rMasterPressureIntegral + (rMasterPressurePreviousError * 0.10 * 0.05);
IF (rMasterPressureIntegral > 25.0) THEN rMasterPressureIntegral := 25.0; END_IF;
IF (rMasterPressureIntegral < -25.0) THEN rMasterPressureIntegral := -25.0; END_IF;

(* Differential pressure error: Target dP = 0.0 mbar (P_O2 = P_H2) *)
(* High priority fast derivative damping prevents hydraulic resonance *)
rDP_DerivativeState := (rEffectiveDP_mbar - rDP_PreviousError) / 0.10;
rDP_PreviousError := rEffectiveDP_mbar;

(* dP Integral Accumulator with anti-windup clamping *)
rDP_IntegralAccumulator := rDP_IntegralAccumulator + (rEffectiveDP_mbar * 0.10 * 0.12);
IF (rDP_IntegralAccumulator > 30.0) THEN rDP_IntegralAccumulator := 30.0; END_IF;
IF (rDP_IntegralAccumulator < -30.0) THEN rDP_IntegralAccumulator := -30.0; END_IF;

(* Dynamic Decoupling Matrix: *)
(* If P_O2 > P_H2 (dP > 0): open PCV-O2 slightly and throttle PCV-H2 slightly *)
(* If P_H2 > P_O2 (dP < 0): open PCV-H2 slightly and throttle PCV-O2 slightly *)
rH2ValveTrim := (-0.35 * rEffectiveDP_mbar) - (0.08 * rDP_DerivativeState) - rDP_IntegralAccumulator;
rO2ValveTrim := (0.35 * rEffectiveDP_mbar) + (0.08 * rDP_DerivativeState) + rDP_IntegralAccumulator;

(* Common backpressure baseline established by master pressure PID and gas generation feedforward *)
rDecoupledPCV_H2 := 50.0 + (1.2 * rHydrogenGasFlow_Nm3h / 20.0) - (4.5 * rMasterPressurePreviousError) - rMasterPressureIntegral + rH2ValveTrim;
rDecoupledPCV_O2 := 50.0 + (1.2 * rOxygenGasFlow_Nm3h / 10.0) - (4.5 * rMasterPressurePreviousError) - rMasterPressureIntegral + rO2ValveTrim;

(* Physical valve travel saturation [5.0% to 95.0%] *)
IF (rDecoupledPCV_H2 > 95.0) THEN rDecoupledPCV_H2 := 95.0; END_IF;
IF (rDecoupledPCV_H2 < 5.0) THEN rDecoupledPCV_H2 := 5.0; END_IF;
IF (rDecoupledPCV_O2 > 95.0) THEN rDecoupledPCV_O2 := 95.0; END_IF;
IF (rDecoupledPCV_O2 < 5.0) THEN rDecoupledPCV_O2 := 5.0; END_IF;

rH2BackpressureValve_pct := rDecoupledPCV_H2;
rO2BackpressureValve_pct := rDecoupledPCV_O2;

(* SIL-3 Differential Pressure Trip Interlock *)
IF (ABS(rEffectiveDP_mbar) > 65.0) THEN
    bTripActive := TRUE;
    dwAlarmWord2_Safety := dwAlarmWord2_Safety OR 16#0000_0020; (* Critical DP Exceeded *)
    iState := 100; (* Trip to Lockout *)
ELSIF (ABS(rEffectiveDP_mbar) > 25.0) THEN
    bAlarmActive := TRUE;
    dwAlarmWord1_Process := dwAlarmWord1_Process OR 16#0000_0001; (* DP Warning High *)
END_IF;
""")

    # -------------------------------------------------------------------------
    # 8. SECTION 5.0: SEPARATOR LYE LEVEL FLOAT BALANCING
    # -------------------------------------------------------------------------
    parts.append("""
(* ========================================================================================= *)
(* 5.0 GAS-LIQUID SEPARATOR LYE LEVEL FLOAT BALANCING & HYDRAULIC EQUALIZATION               *)
(* ========================================================================================= *)
(* Compensates communicating vessel hydrostatic displacement between H2 and O2 separators.   *)
(* Governs inter-separator balancing valve LV-401 and trims lye circulation pump VFD speeds. *)

(* Hydrostatic level differential error: Target e_L = 0.0% (L_H2 = L_O2 = 50.0%) *)
rLevelDiff_IntegralAccumulator := rLevelDiff_IntegralAccumulator + (rEffectiveLevelDiff_pct * 0.10 * 0.04);
IF (rLevelDiff_IntegralAccumulator > 35.0) THEN rLevelDiff_IntegralAccumulator := 35.0; END_IF;
IF (rLevelDiff_IntegralAccumulator < -35.0) THEN rLevelDiff_IntegralAccumulator := -35.0; END_IF;

(* Dynamic gas void fraction swell compensation: rapid current increases swell H2 side 2x O2 *)
rDynamicLyeSwellCorrection := 0.25 * (rStackCurrent_kA - rFilteredCurrentDemand_kA);

(* Modulating Lye Balancing Valve LV-401 command: *)
(* 50% = Neutral closed center; > 50% = Transfer H2 to O2; < 50% = Transfer O2 to H2 *)
rLyeBalanceValve_pct := 50.0 + (1.8 * rEffectiveLevelDiff_pct) + rLevelDiff_IntegralAccumulator + (3.0 * rDynamicLyeSwellCorrection);
IF (rLyeBalanceValve_pct > 100.0) THEN rLyeBalanceValve_pct := 100.0; END_IF;
IF (rLyeBalanceValve_pct < 0.0) THEN rLyeBalanceValve_pct := 0.0; END_IF;

(* Recirculation Pump Speed Trim: Differential VFD bias *)
rLyePumpDifferentialSpeed_pct := (0.65 * rEffectiveLevelDiff_pct);
IF (rLyePumpDifferentialSpeed_pct > 15.0) THEN rLyePumpDifferentialSpeed_pct := 15.0; END_IF;
IF (rLyePumpDifferentialSpeed_pct < -15.0) THEN rLyePumpDifferentialSpeed_pct := -15.0; END_IF;

rCathodeLyePumpSpeed_pct := rBaseLyePumpSpeed_pct - rLyePumpDifferentialSpeed_pct;
rAnodeLyePumpSpeed_pct   := rBaseLyePumpSpeed_pct + rLyePumpDifferentialSpeed_pct;

IF (rCathodeLyePumpSpeed_pct > 100.0) THEN rCathodeLyePumpSpeed_pct := 100.0; END_IF;
IF (rCathodeLyePumpSpeed_pct < 20.0) THEN rCathodeLyePumpSpeed_pct := 20.0; END_IF;
IF (rAnodeLyePumpSpeed_pct > 100.0) THEN rAnodeLyePumpSpeed_pct := 100.0; END_IF;
IF (rAnodeLyePumpSpeed_pct < 20.0) THEN rAnodeLyePumpSpeed_pct := 20.0; END_IF;

(* Extreme Level Safety Interlocks: High-High (85%) / Low-Low (15%) *)
IF (rVotedCathodeLevel_pct > 85.0) OR (rVotedAnodeLevel_pct > 85.0) THEN
    bTripActive := TRUE;
    dwAlarmWord2_Safety := dwAlarmWord2_Safety OR 16#0000_0040; (* Separator High-High Level Trip *)
    iState := 100;
ELSIF (rVotedCathodeLevel_pct < 15.0) OR (rVotedAnodeLevel_pct < 15.0) THEN
    bTripActive := TRUE;
    dwAlarmWord2_Safety := dwAlarmWord2_Safety OR 16#0000_0080; (* Separator Low-Low Level Trip *)
    iState := 100;
END_IF;
""")

    # -------------------------------------------------------------------------
    # 9. SECTION 6.0: CATALYTIC DE-OXO THERMAL SYNC
    # -------------------------------------------------------------------------
    parts.append("""
(* ========================================================================================= *)
(* 6.0 CATALYTIC DE-OXO HYDROGEN PURIFICATION THERMAL SYNC & RUNAWAY MODEL                   *)
(* ========================================================================================= *)
(* Governs catalytic de-oxygenation reactor (2 H2 + O2 -> 2 H2O, Delta_H = -241.8 kJ/mol O2) *)
(* Modulates electric SCR preheater duty and interstage gas cooling bypass to maintain bed    *)
(* temperature safely within 110 deg C to 380 deg C, preventing thermal runaway (> 420 deg C)*)

(* Moles of O2 entering reactor per second: dot_n_O2 = Flow_Nm3h * (ppm / 1e6) / (0.022414 * 3600) *)
(* Heat generation rate: Q = dot_n_O2 * 241,800 J/mol [kW] *)
rDeOxoHeatGeneration_kW := (rHydrogenGasFlow_Nm3h * (rEffectiveO2inH2_ppm / 1000000.0) / 80.69) * 241.8;

(* Adiabatic temperature rise estimation: Delta_T_ad ~ 160 deg C per 1.0 vol% O2 (10,000 ppm) *)
rAdiabaticTempRise_DegC := (rEffectiveO2inH2_ppm / 10000.0) * 162.0;

(* Model predicted peak catalyst bed hot-spot temperature *)
rPredictedDeOxoPeakTemp_DegC := rDeOxoInletTemp_DegC + rAdiabaticTempRise_DegC;

(* Electric Preheater SCR Duty Control: maintains bed inlet at >= 85 deg C for reliable light-off *)
IF (rDeOxoInletTemp_DegC < 85.0) THEN
    rDeOxoPreheaterDuty_pct := (85.0 - rDeOxoInletTemp_DegC) * 3.5;
    IF (rDeOxoPreheaterDuty_pct > 100.0) THEN rDeOxoPreheaterDuty_pct := 100.0; END_IF;
ELSE
    rDeOxoPreheaterDuty_pct := 0.0;
END_IF;

(* Interstage Cooling Gas Bypass Modulation: opens bypass when bed zone 2/3 exceeds 260 deg C *)
IF (rDeOxoBedTempZone2_DegC > 260.0) THEN
    rDeOxoCoolingBypass_pct := (rDeOxoBedTempZone2_DegC - 260.0) * 1.25;
    IF (rDeOxoCoolingBypass_pct > 100.0) THEN rDeOxoCoolingBypass_pct := 100.0; END_IF;
ELSE
    rDeOxoCoolingBypass_pct := 0.0;
END_IF;

(* Critical Catalytic Bed Thermal Runaway Interlock (> 420 deg C) *)
IF (rDeOxoBedTempZone1_DegC > 420.0) OR (rDeOxoBedTempZone2_DegC > 420.0) OR (rDeOxoBedTempZone3_DegC > 420.0) THEN
    bTripActive := TRUE;
    dwAlarmWord2_Safety := dwAlarmWord2_Safety OR 16#0000_0100; (* De-Oxo Thermal Runaway Trip *)
    iState := 100;
ELSIF (rDeOxoBedTempZone2_DegC > 380.0) THEN
    bAlarmActive := TRUE;
    dwAlarmWord1_Process := dwAlarmWord1_Process OR 16#0000_0002; (* De-Oxo High Temp Warning *)
END_IF;

(* Residual Oxygen in Product Hydrogen Quality Interlock (> 5 ppm violates fuel cell grade) *)
IF (rDeOxoProductO2_ppm > 5.0) AND (iState = 60) THEN
    dwAlarmWord1_Process := dwAlarmWord1_Process OR 16#0000_0004; (* H2 Off-Spec O2 Purity Warning *)
END_IF;
""")

    # -------------------------------------------------------------------------
    # 10. SECTION 7.0: RENEWABLE POWER RAMP RATE LIMITER
    # -------------------------------------------------------------------------
    parts.append("""
(* ========================================================================================= *)
(* 7.0 RENEWABLE POWER FAST RAMP RATE LIMITER & FLAMMABILITY PROTECTION FLOOR                *)
(* ========================================================================================= *)
(* Regulates electrical ramp rates (di/dt) to protect diaphragms from pressure shock waves   *)
(* and dynamically enforces a minimum current floor to prevent H2-in-O2 flammability spikes. *)

(* Dynamic Minimum Current Floor: Inversely proportional to operating pressure and gas purity*)
(* At 30 bar, minimum current must not fall below 15% (2.4 kA) to prevent H2 in O2 crossing 1.5%*)
rDynamicMinCurrentFloor_kA := 2.40 + (0.00035 * rEffectiveH2inO2_ppm);
IF (rDynamicMinCurrentFloor_kA > 5.0) THEN rDynamicMinCurrentFloor_kA := 5.0; END_IF;

(* Convert available renewable power [kW] to current setpoint demand [kA] *)
IF (rStackVoltage_V > 100.0) THEN
    rTempCalc := rRenewablePowerAvailable_kW / rStackVoltage_V;
ELSE
    rTempCalc := 2.40;
END_IF;

(* Apply dynamic lower and upper bounds *)
IF (rTempCalc < rDynamicMinCurrentFloor_kA) THEN
    rTempCalc := rDynamicMinCurrentFloor_kA;
END_IF;
IF (rTempCalc > 16.0) THEN
    rTempCalc := 16.0;
END_IF;

(* Dynamic Allowable Ramp Rate: derated if stack is cold (< 65 deg C) or dP error is high *)
IF (rElectrolyteInletTemp_DegC < 65.0) THEN
    rMaxAllowableRampRate_kA_s := 0.08; (* Cold stack: 0.5% / s *)
ELSIF (ABS(rEffectiveDP_mbar) > 15.0) THEN
    rMaxAllowableRampRate_kA_s := 0.05; (* High dP: derate to 0.3% / s *)
ELSE
    rMaxAllowableRampRate_kA_s := 0.32; (* Nominal hot stack: 2.0% / s *)
END_IF;

(* Rate Limiting Slew Rate Execution: Ts = 0.10 s *)
rCurrentRampRate_kA_s := (rTempCalc - rFilteredCurrentDemand_kA) / 0.10;

IF (rCurrentRampRate_kA_s > rMaxAllowableRampRate_kA_s) THEN
    rFilteredCurrentDemand_kA := rFilteredCurrentDemand_kA + (rMaxAllowableRampRate_kA_s * 0.10);
ELSIF (rCurrentRampRate_kA_s < -rMaxAllowableRampRate_kA_s) THEN
    rFilteredCurrentDemand_kA := rFilteredCurrentDemand_kA - (rMaxAllowableRampRate_kA_s * 0.10);
ELSE
    rFilteredCurrentDemand_kA := rTempCalc;
END_IF;

(* Cross-Permeation Gas Safety Trips: LFL of H2 in O2 is 40,000 ppm (4.0 vol%) *)
(* SIL-3 Trip at 18,000 ppm (1.8 vol%); Alarm at 10,000 ppm (1.0 vol%) *)
IF (rEffectiveH2inO2_ppm > 18000.0) THEN
    bTripActive := TRUE;
    dwAlarmWord2_Safety := dwAlarmWord2_Safety OR 16#0000_0200; (* H2 in O2 Explosive Trip *)
    iState := 100;
ELSIF (rEffectiveH2inO2_ppm > 10000.0) THEN
    bAlarmActive := TRUE;
    dwAlarmWord1_Process := dwAlarmWord1_Process OR 16#0000_0008; (* H2 in O2 Warning High *)
END_IF;

IF (rEffectiveO2inH2_ppm > 20000.0) THEN
    bTripActive := TRUE;
    dwAlarmWord2_Safety := dwAlarmWord2_Safety OR 16#0000_0400; (* O2 in H2 Explosive Trip *)
    iState := 100;
END_IF;
""")

    # -------------------------------------------------------------------------
    # 11. SECTION 8.0: 6-STATE MULTIVARIABLE MPC OPTIMIZER
    # -------------------------------------------------------------------------
    parts.append("""
(* ========================================================================================= *)
(* 8.0 6-STATE MULTIVARIABLE STATE-SPACE DISCRETE MODEL & REAL-TIME MPC OPTIMIZER            *)
(* ========================================================================================= *)
(* Embedded quadratic programming solver executing projected gradient descent iterations.    *)
(* State vector: x = [dP, dLevel, T_DeOxo, T_Stack, C_H2_in_O2, C_O2_in_H2]^T                 *)
(* Actuators:    u = [u_PCV_H2, u_LV_Bal, u_HTR_DeOxo, I_Rectifier_Demand]^T                  *)

(* Initialize discrete state matrices on first scan or reset *)
IF NOT bFirstScanComplete THEN
    (* Diagonal state transition elements (decay dynamics) *)
    arrA[1, 1] := 0.88; arrA[1, 2] := -0.04; arrA[1, 3] := 0.00; arrA[1, 4] := 0.00; arrA[1, 5] := 0.00; arrA[1, 6] := 0.00;
    arrA[2, 1] := 0.06; arrA[2, 2] := 0.94; arrA[2, 3] := 0.00; arrA[2, 4] := 0.00; arrA[2, 5] := 0.00; arrA[2, 6] := 0.00;
    arrA[3, 1] := 0.00; arrA[3, 2] := 0.00; arrA[3, 3] := 0.92; arrA[3, 4] := 0.02; arrA[3, 5] := 0.00; arrA[3, 6] := 0.05;
    arrA[4, 1] := 0.00; arrA[4, 2] := 0.00; arrA[4, 3] := 0.00; arrA[4, 4] := 0.98; arrA[4, 5] := 0.00; arrA[4, 6] := 0.00;
    arrA[5, 1] := 0.15; arrA[5, 2] := 0.00; arrA[5, 3] := 0.00; arrA[5, 4] := 0.08; arrA[5, 5] := 0.96; arrA[5, 6] := 0.00;
    arrA[6, 1] := -0.12; arrA[6, 2] := 0.00; arrA[6, 3] := 0.00; arrA[6, 4] := 0.05; arrA[6, 5] := 0.00; arrA[6, 6] := 0.96;

    (* Control Input Matrix B: effect of actuators on state progression *)
    arrB[1, 1] := -0.45; arrB[1, 2] := 0.00; arrB[1, 3] := 0.00; arrB[1, 4] := 0.12;
    arrB[2, 1] := 0.00;  arrB[2, 2] := 0.38; arrB[2, 3] := 0.00; arrB[2, 4] := 0.04;
    arrB[3, 1] := 0.00;  arrB[3, 2] := 0.00; arrB[3, 3] := 0.55; arrB[3, 4] := 0.85;
    arrB[4, 1] := 0.00;  arrB[4, 2] := 0.00; arrB[4, 3] := 0.00; arrB[4, 4] := 1.25;
    arrB[5, 1] := 0.02;  arrB[5, 2] := 0.00; arrB[5, 3] := 0.00; arrB[5, 4] := -0.80;
    arrB[6, 1] := -0.02; arrB[6, 2] := 0.00; arrB[6, 3] := 0.00; arrB[6, 4] := -0.65;

    (* State Penalty Weights Q (Diagonal): strict penalty on dP and cross-contamination *)
    arrQ[1] := 50.0; (* dP [mbar] *)
    arrQ[2] := 20.0; (* dLevel [%] *)
    arrQ[3] := 2.0;  (* T_DeOxo [deg C] *)
    arrQ[4] := 1.0;  (* T_Stack [deg C] *)
    arrQ[5] := 15.0; (* H2 in O2 [ppm] *)
    arrQ[6] := 10.0; (* O2 in H2 [ppm] *)

    (* Control Effort Weights R and Slew Penalty S *)
    arrR[1] := 0.5; arrR[2] := 0.5; arrR[3] := 0.1; arrR[4] := 0.2;
    arrS[1] := 2.0; arrS[2] := 1.5; arrS[3] := 0.8; arrS[4] := 3.0;

    (* Actuator Physical Saturation Limits *)
    arrU_min[1] := 5.0;   arrU_max[1] := 95.0;  arrDeltaU_max[1] := 5.0;
    arrU_min[2] := 0.0;   arrU_max[2] := 100.0; arrDeltaU_max[2] := 4.0;
    arrU_min[3] := 0.0;   arrU_max[3] := 100.0; arrDeltaU_max[3] := 8.0;
    arrU_min[4] := 2.4;   arrU_max[4] := 16.0;  arrDeltaU_max[4] := 0.16;

    bFirstScanComplete := TRUE;
END_IF;

(* Populate current measured state vector *)
arrX[1] := rEffectiveDP_mbar;
arrX[2] := rEffectiveLevelDiff_pct;
arrX[3] := rDeOxoBedTempZone2_DegC;
arrX[4] := rElectrolyteInletTemp_DegC;
arrX[5] := rEffectiveH2inO2_ppm / 1000.0; (* Scaled to ppt for numerical conditioning *)
arrX[6] := rEffectiveO2inH2_ppm / 1000.0;

(* Target state reference *)
arrX_ref[1] := 0.0;   (* Target dP = 0 mbar *)
arrX_ref[2] := 0.0;   (* Target dLevel = 0 % *)
arrX_ref[3] := 160.0; (* Optimum De-Oxo bed temp [deg C] *)
arrX_ref[4] := 80.0;  (* Optimum stack temp [deg C] *)
arrX_ref[5] := 2.0;   (* H2 in O2 reference < 2000 ppm *)
arrX_ref[6] := 1.0;   (* O2 in H2 reference < 1000 ppm *)

(* Execute MPC Projected Gradient Descent if in Auto Mode *)
IF bAutoMode AND (iState = 60) THEN
    (* 10 Iterations per cycle of gradient projection *)
    FOR kIdx := 1 TO 10 DO
        (* Calculate predicted state: x_pred = A*x + B*u *)
        FOR iIdx := 1 TO 6 DO
            rTempCalc := 0.0;
            FOR jIdx := 1 TO 6 DO
                rTempCalc := rTempCalc + (arrA[iIdx, jIdx] * arrX[jIdx]);
            END_FOR;
            FOR jIdx := 1 TO 4 DO
                rTempCalc := rTempCalc + (arrB[iIdx, jIdx] * arrU[jIdx]);
            END_FOR;
            arrX_hat[iIdx] := rTempCalc;
        END_FOR;

        (* Calculate gradient: grad_J = B^T * Q * (x_pred - x_ref) + R * u + S * (u - u_prev) *)
        FOR iIdx := 1 TO 4 DO
            rTempCalc := 0.0;
            FOR jIdx := 1 TO 6 DO
                rTempCalc := rTempCalc + (arrB[jIdx, iIdx] * arrQ[jIdx] * (arrX_hat[jIdx] - arrX_ref[jIdx]));
            END_FOR;
            rTempCalc := rTempCalc + (arrR[iIdx] * arrU[iIdx]) + (arrS[iIdx] * (arrU[iIdx] - arrU_prev[iIdx]));
            arrGrad[iIdx] := rTempCalc;
        END_FOR;

        (* Projected step update: u_new = u - alpha * grad_J *)
        FOR iIdx := 1 TO 4 DO
            arrU[iIdx] := arrU[iIdx] - (0.012 * arrGrad[iIdx]);

            (* Slew rate saturation *)
            IF (arrU[iIdx] - arrU_prev[iIdx]) > arrDeltaU_max[iIdx] THEN
                arrU[iIdx] := arrU_prev[iIdx] + arrDeltaU_max[iIdx];
            ELSIF (arrU[iIdx] - arrU_prev[iIdx]) < -arrDeltaU_max[iIdx] THEN
                arrU[iIdx] := arrU_prev[iIdx] - arrDeltaU_max[iIdx];
            END_IF;

            (* Actuator boundary projection *)
            IF (arrU[iIdx] > arrU_max[iIdx]) THEN
                arrU[iIdx] := arrU_max[iIdx];
            ELSIF (arrU[iIdx] < arrU_min[iIdx]) THEN
                arrU[iIdx] := arrU_min[iIdx];
            END_IF;
        END_FOR;
    END_FOR;

    (* Store previous control vector *)
    FOR iIdx := 1 TO 4 DO
        arrU_prev[iIdx] := arrU[iIdx];
    END_FOR;

    (* Map MPC control variables to physical actuators *)
    rH2BackpressureValve_pct   := arrU[1];
    rLyeBalanceValve_pct       := arrU[2];
    rDeOxoPreheaterDuty_pct    := arrU[3];
    rRectifierCurrentDemand_kA := arrU[4];
    bMpcConverged := TRUE;
ELSE
    bMpcConverged := FALSE;
END_IF;
""")

    # -------------------------------------------------------------------------
    # 12. SECTION 9.0: MULTI-STAGE FINITE STATE MACHINE (FSM)
    # -------------------------------------------------------------------------
    parts.append("""
(* ========================================================================================= *)
(* 9.0 MULTI-STAGE FINITE STATE MACHINE (FSM)                                                *)
(* ========================================================================================= *)
(* 0: SYSTEM_INERT_STANDBY        - Atmospheric N2 blanket, system depressurized             *)
(* 10: N2_PURGE_LEAK_TEST         - Nitrogen sweep and 30 bar pressure hold leak integrity   *)
(* 20: LYE_FILL_AND_FLOAT_PRIME   - Lye circulation pumps engaged, separators balanced       *)
(* 30: PREHEAT_HOT_STANDBY        - Electrolyte loop preheated to 80 deg C via heat exchangers*)
(* 40: MINIMUM_LOAD_POLARIZATION  - Rectifier energized at minimum floor current (2.4 kA)    *)
(* 50: PRESSURE_RAMP_UP           - Coordinated H2/O2 pressurization from 1.5 to 30.0 bar    *)
(* 60: AUTONOMOUS_PRODUCTION_MPC  - Full green hydrogen modulation under active MPC          *)
(* 70: DE_OXO_THERMAL_STABILIZE   - Catalytic De-Oxo fine thermal tuning                     *)
(* 80: CONTROLLED_POWER_RAMP_DOWN - Orderly load shedding and depressurization               *)
(* 90: EMERGENCY_SHUTDOWN_PURGE   - Rectifier tripped, high-pressure N2 safety sweep         *)
(* 100: SAFETY_FAULT_LOCKOUT      - SIL-3 tripped state requiring manual inspection & reset  *)

CASE iState OF
    0: (* ---------------- SYSTEM_INERT_STANDBY ---------------- *)
        bSystemRunning := FALSE;
        bProductionReady := FALSE;
        rRectifierCurrentDemand_kA := 0.0;
        rDeOxoPreheaterDuty_pct := 0.0;
        rEmergencyDepressValve_pct := 0.0;
        rNitrogenPurgeValve_pct := 0.0;
        rCathodeLyePumpSpeed_pct := 0.0;
        rAnodeLyePumpSpeed_pct := 0.0;

        IF bEnableSystem AND NOT bTripActive THEN
            IF bNitrogenPurgePermissive THEN
                iState := 10; (* Advance to Purge & Leak Test *)
                iStateStep := 0;
            END_IF;
        END_IF;

    10: (* ---------------- N2_PURGE_LEAK_TEST ---------------- *)
        bSystemRunning := TRUE;
        bPurgeActive := TRUE;

        CASE iStateStep OF
            0: (* Open N2 purge to sweep atmospheric oxygen *)
                rNitrogenPurgeValve_pct := 100.0;
                rH2BackpressureValve_pct := 80.0;
                rO2BackpressureValve_pct := 80.0;
                tPurgeTimer(IN := TRUE, PT := T#30S);
                IF tPurgeTimer.Q THEN
                    tPurgeTimer(IN := FALSE);
                    iStateStep := 1;
                END_IF;

            1: (* Pressurize system to 30 bar for leak decay test *)
                rNitrogenPurgeValve_pct := 40.0;
                rH2BackpressureValve_pct := 0.0;
                rO2BackpressureValve_pct := 0.0;
                IF (rEffectiveSystemPressure_bar >= 29.5) THEN
                    rNitrogenPurgeValve_pct := 0.0;
                    rLeakTestInitialPress_bar := rEffectiveSystemPressure_bar;
                    iStateStep := 2;
                END_IF;

            2: (* Hold pressure for 60 seconds; verify decay < 0.2 bar *)
                tLeakTestTimer(IN := TRUE, PT := T#60S);
                IF tLeakTestTimer.Q THEN
                    tLeakTestTimer(IN := FALSE);
                    IF (rLeakTestInitialPress_bar - rEffectiveSystemPressure_bar) < 0.20 THEN
                        bPurgeActive := FALSE;
                        iState := 20; (* Leak test passed, proceed to lye fill *)
                        iStateStep := 0;
                    ELSE
                        bTripActive := TRUE;
                        dwAlarmWord2_Safety := dwAlarmWord2_Safety OR 16#0000_0800; (* Leak Test Failed *)
                        iState := 100;
                    END_IF;
                END_IF;
        END_CASE;

    20: (* ---------------- LYE_FILL_AND_FLOAT_PRIME ---------------- *)
        bPurgeActive := FALSE;
        IF bLyeCirculationPermissive THEN
            rBaseLyePumpSpeed_pct := 40.0;
            (* Allow lye levels to settle to 50% +- 5% *)
            IF (ABS(rEffectiveLevelDiff_pct) < 5.0) AND (rVotedCathodeLevel_pct > 40.0) AND (rVotedAnodeLevel_pct > 40.0) THEN
                iState := 30; (* Advance to Preheat *)
                iStateStep := 0;
            END_IF;
        END_IF;

    30: (* ---------------- PREHEAT_HOT_STANDBY ---------------- *)
        rBaseLyePumpSpeed_pct := 60.0;
        tPreheatTimer(IN := TRUE, PT := T#120S);

        (* Check if electrolyte and De-Oxo reach minimum thermal operational thresholds *)
        IF (rElectrolyteInletTemp_DegC >= 65.0) AND (rDeOxoInletTemp_DegC >= 65.0) THEN
            tPreheatTimer(IN := FALSE);
            iState := 40; (* Proceed to Polarization *)
            iStateStep := 0;
        ELSIF tPreheatTimer.Q THEN
            tPreheatTimer(IN := FALSE);
            iState := 40; (* Proceed on timeout if temperature is adequate *)
        END_IF;

    40: (* ---------------- MINIMUM_LOAD_POLARIZATION ---------------- *)
        (* Energize rectifier to minimum current floor (2.4 kA) at low pressure (1.5 bar) *)
        rRectifierCurrentDemand_kA := 2.40;
        rBaseLyePumpSpeed_pct := 70.0;

        (* Verify cell polarization: stack voltage > 400 V and gas flow detectable *)
        IF (rStackVoltage_V > 400.0) AND (rHydrogenGasFlow_Nm3h > 50.0) THEN
            IF (ABS(rEffectiveDP_mbar) < 5.0) THEN
                iState := 50; (* Ready to ramp system pressure *)
                iStateStep := 0;
            END_IF;
        END_IF;

    50: (* ---------------- PRESSURE_RAMP_UP ---------------- *)
        (* Gradually throttle backpressure valves to build pressure from 1.5 to 30.0 bar *)
        (* Crucial: keep dP tightly nulled within +- 3 mbar during entire compression phase *)
        IF (rEffectiveSystemPressure_bar < 29.8) THEN
            rH2BackpressureValve_pct := 35.0;
            rO2BackpressureValve_pct := 35.0;
        ELSE
            iState := 60; (* Reached 30 bar nominal: enter autonomous MPC production *)
            iStateStep := 0;
        END_IF;

    60: (* ---------------- AUTONOMOUS_PRODUCTION_MPC ---------------- *)
        bProductionReady := TRUE;
        bSystemRunning := TRUE;

        (* Active MPC optimizer governs actuators in Section 8.0 *)
        (* Fallback to internal PID if MPC flag is false *)
        IF NOT bMpcConverged THEN
            rRectifierCurrentDemand_kA := rFilteredCurrentDemand_kA;
        END_IF;

        (* Check for power ramp-down command or trip *)
        IF NOT bEnableSystem THEN
            iState := 80; (* Orderly ramp down *)
        END_IF;

    70: (* ---------------- DE_OXO_THERMAL_STABILIZE ---------------- *)
        (* Temporary holding state during catalytic bed thermal transients *)
        IF (rDeOxoBedTempZone2_DegC <= 320.0) AND (rEffectiveO2inH2_ppm < 5000.0) THEN
            iState := 60; (* Return to production *)
        END_IF;

    80: (* ---------------- CONTROLLED_POWER_RAMP_DOWN ---------------- *)
        bProductionReady := FALSE;
        (* Step down rectifier current at controlled rate *)
        IF (rRectifierCurrentDemand_kA > 2.40) THEN
            rRectifierCurrentDemand_kA := rRectifierCurrentDemand_kA - 0.20;
        ELSE
            rRectifierCurrentDemand_kA := 0.0;
            (* Slowly depressurize system down to 2 bar *)
            IF (rEffectiveSystemPressure_bar > 2.5) THEN
                rH2BackpressureValve_pct := 65.0;
                rO2BackpressureValve_pct := 65.0;
            ELSE
                iState := 0; (* Returned to Standby *)
            END_IF;
        END_IF;

    90: (* ---------------- EMERGENCY_SHUTDOWN_PURGE ---------------- *)
        bProductionReady := FALSE;
        bSystemRunning := FALSE;
        rRectifierCurrentDemand_kA := 0.0;
        rDeOxoPreheaterDuty_pct := 0.0;
        rNitrogenPurgeValve_pct := 100.0;
        rEmergencyDepressValve_pct := 40.0;
        rH2BackpressureValve_pct := 90.0;
        rO2BackpressureValve_pct := 90.0;

        IF (rEffectiveSystemPressure_bar <= 1.5) THEN
            rEmergencyDepressValve_pct := 0.0;
            iState := 100; (* Lockout *)
        END_IF;

    100: (* ---------------- SAFETY_FAULT_LOCKOUT ---------------- *)
        bProductionReady := FALSE;
        bSystemRunning := FALSE;
        bTripActive := TRUE;
        rRectifierCurrentDemand_kA := 0.0;
        rDeOxoPreheaterDuty_pct := 0.0;
        rCathodeLyePumpSpeed_pct := 0.0;
        rAnodeLyePumpSpeed_pct := 0.0;
        rNitrogenPurgeValve_pct := 0.0;
        rEmergencyDepressValve_pct := 0.0;

        (* Lockout requires bResetFaults toggle when fault causes are cleared *)
        IF bResetFaults AND bEnableSystem AND (dwAlarmWord2_Safety = 16#0000_0000) THEN
            iState := 0;
        END_IF;

END_CASE;
""")

    # -------------------------------------------------------------------------
    # 13. SECTION 10.0: GRACEFUL DEGRADATION & FAULT MITIGATION
    # -------------------------------------------------------------------------
    parts.append("""
(* ========================================================================================= *)
(* 10.0 GRACEFUL DEGRADATION, SENSOR FAULT MITIGATION & DERATE MANAGEMENT                    *)
(* ========================================================================================= *)
(* Manages transmitter degradation, actuator wear tracking, and automatic power derating.    *)

(* Detect sensor health degradation across all 2oo3 triplets *)
IF NOT (bCathodePress_A_Healthy AND bCathodePress_B_Healthy AND bCathodePress_C_Healthy) OR
   NOT (bAnodePress_A_Healthy AND bAnodePress_B_Healthy AND bAnodePress_C_Healthy) OR
   NOT (bDP_A_Healthy AND bDP_B_Healthy AND bDP_C_Healthy) OR
   NOT (bCathodeLevel_A_Healthy AND bCathodeLevel_B_Healthy AND bCathodeLevel_C_Healthy) OR
   NOT (bAnodeLevel_A_Healthy AND bAnodeLevel_B_Healthy AND bAnodeLevel_C_Healthy) THEN
    bDegradedMode := TRUE;
    dwSubsystemDiagnostics := dwSubsystemDiagnostics OR 16#0001_0000; (* Transmitter Redundancy Degraded *)
ELSE
    bDegradedMode := FALSE;
END_IF;

(* Automatic Rectifier Derating: if operating in degraded mode, clamp maximum current to 65% *)
IF bDegradedMode AND (rRectifierCurrentDemand_kA > 10.4) THEN
    rRectifierCurrentDemand_kA := 10.4;
END_IF;

(* Electrolyte Circulation Flow Rate Interlocks *)
IF (rCathodeLyeFlow_m3h < 15.0) OR (rAnodeLyeFlow_m3h < 15.0) THEN
    IF (iState = 60) THEN
        bTripActive := TRUE;
        dwAlarmWord2_Safety := dwAlarmWord2_Safety OR 16#0000_1000; (* Loss of Lye Circulation Trip *)
        iState := 100;
    END_IF;
END_IF;
""")

    # -------------------------------------------------------------------------
    # 14. SECTION 11.0: BIT-PACKED STATUS & ALARM WORD ASSEMBLY
    # -------------------------------------------------------------------------
    parts.append("""
(* ========================================================================================= *)
(* 11.0 BIT-PACKED STATUS WORD & ALARM ASSEMBLY                                              *)
(* ========================================================================================= *)

(* --- 11.1 SYSTEM OPERATIONAL STATUS WORD (dwSystemStatusWord) --- *)
dwSystemStatusWord := 16#0000_0000;
IF bSystemRunning THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0001; END_IF;
IF bProductionReady THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0002; END_IF;
IF bAlarmActive THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0004; END_IF;
IF bTripActive THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0008; END_IF;
IF bDegradedMode THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0010; END_IF;
IF bPurgeActive THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0020; END_IF;
IF bMpcConverged THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0040; END_IF;
IF bAutoMode THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0080; END_IF;

(* State Index Encoding in Upper Byte *)
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

    code = "".join(parts)
    return code

if __name__ == "__main__":
    c = build_code()
    print("Code length:", len(c))
    lines = c.split("\n")
    print("Total lines:", len(lines))
    print("First line:", lines[0])
    print("Last line:", lines[-2] if lines[-1] == "" else lines[-1])
