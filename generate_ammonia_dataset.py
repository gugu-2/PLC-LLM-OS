# Complete generator for FB_Chemical_AmmoniaSynthesis_HaberBosch_200Bar
import os
import json
import uuid

def generate_iec_st():
    parts = []

    # 1. Header
    parts.append("""FUNCTION_BLOCK FB_Chemical_AmmoniaSynthesis_HaberBosch_200Bar
(*
 ==========================================================================================
  PROJECT:       WORLD-SCALE COMMERCIAL CHEMICALS & FERTILIZER COMPLEX
  SUBSYSTEM:     3,000 MTPD AMMONIA SYNTHESIS LOOP (HABER-BOSCH, 200 BAR)
  DISCIPLINE:    THERMOCHEMICAL CATALYSIS / CENTRIFUGAL COMPRESSORS / MPC / TMR SAFETY
  IEC STANDARD:  IEC 61131-3 STRUCTURED TEXT 3RD EDITION (DETERMINISTIC EMBEDDED EXECUTION)
  AUTHOR:        LUMINA AI CLOUD SWARM - PRINCIPAL AUTOMATION FELLOW & CPS CHAIR (V7 MAX)
  FACILITY CAP:  3,000 METRIC TONS PER DAY ANHYDROUS LIQUID NH3 (125,000 KG/H | 34.72 KG/S)
  LOOP PRESSURE: 180.0 TO 220.0 BAR GAUGE (NOMINAL 200.0 BAR | DESIGN 245.0 BAR)
  CATALYST:      MULTIPROMOTED MAGNETITE / WUSTITE Fe-K2O-Al2O3-CaO (ACTIVE FRACTION > 99%)
  COMPRESSOR:    35 MW STEAM TURBINE DRIVEN 2-CASING LP/HP CENTRIFUGAL SYNGAS TRAIN
  SAFETY CLASS:  SIL-3 ARCHITECTURE (IEC 61508 / IEC 61511) WITH 2oo3 TMR INSTRUMENTATION

  PROCESS ARCHITECTURE & CYBER-PHYSICAL GOVERNING EQUATIONS:

  1. HETEROGENEOUS REACTION KINETICS (TEMKIN-PYZHEV FORMULATION):
     Reversible ammonia synthesis across promoted iron catalyst:
         N2(g) + 3 H2(g) <===> 2 NH3(g)   [Delta H_rxn = -46.22 kJ/mol NH3 at 298 K]
     Intrinsic kinetics rate equation per unit catalyst volume:
         r_NH3 = k1 * P_N2 * (P_H2^3 / P_NH3^2)^alpha - k2 * (P_NH3^2 / P_H2^3)^(1 - alpha)
     where alpha = 0.5 (Temkin parameter), partial pressures P_i = y_i * P_loop * phi_i,
     phi_i = fugacity coefficients calculated via Redlich-Kwong-Soave / Peng-Robinson EOS.
     Arrhenius rate constants:
         k1(T) = k10 * EXP(-E1 / (R * (T_bed + 273.15)))
         k2(T) = k20 * EXP(-E2 / (R * (T_bed + 273.15)))
     Equilibrium Constant K_eq(T, P):
         LOG10(K_p) = -2.691122 * LOG10(T) - 5.519265E-5 * T + 1.848863E-7 * T^2
                      + 2001.6 / T + 2.6899 - 0.000105 * P_bar

  2. MULTI-BED AXIAL-RADIAL QUENCH CONVERTER HEAT & MASS INTEGRATION:
     4-Bed insulated catalytic basket with direct inter-bed cold syngas quench injection:
         Bed 1 (Top):     Inlet 385 C, Exotherm Peak 505 C -> Quench 1 Injection -> 410 C
         Bed 2 (Upper):   Inlet 410 C, Exotherm Peak 475 C -> Quench 2 Injection -> 400 C
         Bed 3 (Lower):   Inlet 400 C, Exotherm Peak 450 C -> Quench 3 Injection -> 395 C
         Bed 4 (Bottom):  Inlet 395 C, Effluent 432 C (Cumulative NH3 Conversion = 18.5 mol%)
     Thermal runaway sintering limit: T_bed_peak > 520.0 C activates emergency quench & trip.
     Quench mass & thermal balance per mixing zone j:
         m_in(j+1) * H(T_in,j+1) = m_eff(j) * H(T_eff,j) + m_quench(j) * H(T_cold_quench)

  3. SYNGAS COMPRESSOR AERODYNAMICS & ANTI-SURGE DYNAMICS:
     Multi-stage centrifugal syngas compressor driven by 35 MW extraction-condensing turbine:
         Polytropic Head: H_poly = (Z_avg * R * T_in / M_avg) * (n/(n-1)) * [(P_out/P_in)^((n-1)/n) - 1]
         Surge Limit Line (SLL): dP_surge = K_surge * dP_orifice_inlet
         Dynamic Surge Margin: S_margin = (dP_orifice - dP_surge) / dP_surge * 100 [%]
         Derivative Surge Kick: u_kick = K_deriv * d(S_margin)/dt (when rate of approach < -5%/s)
     Active thrust bearing eddy-current proximity monitoring:
         Axial displacement alarm at +0.35 mm / -0.35 mm; trip at +0.50 mm / -0.50 mm.

  4. CLOSED-LOOP STOICHIOMETRY & INERT PURGE GAS CRYOGENIC RECOVERY:
     Circulating gas H2:N2 stoichiometric ratio held rigorously at 2.95 : 1.00 (deadband 2.85-3.05).
     In-line dual gas chromatograph + quadrupole mass spectrometer feedforward trim on makeup gas.
     Continuous purge gas bleed (regulating inerts CH4 + Ar < 10.5 vol% in loop):
         High-pressure purge sent to Cryogenic Hydrogen Recovery Unit (HRU).
         Cold box recovers 92% pure H2 returned to HP compressor recycle suction;
         Reject fuel gas (CH4 + Ar) dispatched to primary steam reformer burners.

  5. AMMONIA REFRIGERATION CONDENSATION TRAIN:
     Multi-stage flash refrigeration chillers condense gaseous NH3 from loop effluent:
         Stages: Gas-Gas Exchanger (280 C) -> Water Cooler (38 C) ->
                 Chiller 1 (+12 C) -> Chiller 2 (+2 C) -> Chiller 3 (-10 C) -> Catch Separator (-25 C).
         Liquid NH3 yield: 34.72 kg/s at 99.8 wt% purity pumped to atmospheric cryogenic tank (-33 C).
 ==========================================================================================
*)
""")

    # 2. VAR_INPUT
    parts.append("""VAR_INPUT
    (* ===================================================================================== *)
    (* 1. SYSTEM MASTER DIGITAL PERMISSIVES & SUPERVISORY RUN COMMANDS                       *)
    (* ===================================================================================== *)
    bMasterEnable                   : BOOL;     (* Plant master supervisory loop enable permissive *)
    bEmergencyStop                  : BOOL;     (* SIL-3 hardwired emergency loop trip [active-low] *)
    bResetFaults                    : BOOL;     (* Master alarm unlatch and safety shutdown reset *)
    bCompressorPermissive           : BOOL;     (* Syngas compressor lube/seal oil & turning gear ready *)
    bTurbineSteamPermissive         : BOOL;     (* 110 bar HP superheated steam supply header ready *)
    bCryoHruOnlinePermissive        : BOOL;     (* Cryogenic Hydrogen Recovery Unit ready for purge feed *)
    bRefrigerationLoopPermissive    : BOOL;     (* Ammonia mechanical refrigeration chiller compressor online *)
    bFeedGasSkidPermissive          : BOOL;     (* Purified fresh makeup syngas skid pressurized & online *)
    bManualOverride                 : BOOL;     (* Manual engineering override permissive *)

    (* ===================================================================================== *)
    (* 2. CONVERTER CATALYST BED TEMPERATURE TRANSMITTERS (2oo3 TMR) [deg C]                 *)
    (* ===================================================================================== *)
    rBed1_Temp_DegC_Ch1             : REAL;     (* Catalyst Bed 1 inlet/core thermocouple Ch1 [deg C] *)
    rBed1_Temp_DegC_Ch2             : REAL;     (* Catalyst Bed 1 inlet/core thermocouple Ch2 [deg C] *)
    rBed1_Temp_DegC_Ch3             : REAL;     (* Catalyst Bed 1 inlet/core thermocouple Ch3 [deg C] *)
    rBed2_Temp_DegC_Ch1             : REAL;     (* Catalyst Bed 2 inlet/core thermocouple Ch1 [deg C] *)
    rBed2_Temp_DegC_Ch2             : REAL;     (* Catalyst Bed 2 inlet/core thermocouple Ch2 [deg C] *)
    rBed2_Temp_DegC_Ch3             : REAL;     (* Catalyst Bed 2 inlet/core thermocouple Ch3 [deg C] *)
    rBed3_Temp_DegC_Ch1             : REAL;     (* Catalyst Bed 3 inlet/core thermocouple Ch1 [deg C] *)
    rBed3_Temp_DegC_Ch2             : REAL;     (* Catalyst Bed 3 inlet/core thermocouple Ch2 [deg C] *)
    rBed3_Temp_DegC_Ch3             : REAL;     (* Catalyst Bed 3 inlet/core thermocouple Ch3 [deg C] *)
    rBed4_Temp_DegC_Ch1             : REAL;     (* Catalyst Bed 4 effluent thermocouple Ch1 [deg C] *)
    rBed4_Temp_DegC_Ch2             : REAL;     (* Catalyst Bed 4 effluent thermocouple Ch2 [deg C] *)
    rBed4_Temp_DegC_Ch3             : REAL;     (* Catalyst Bed 4 effluent thermocouple Ch3 [deg C] *)
    rConverterShell_Temp_DegC       : REAL;     (* Converter high-pressure outer pressure shell [deg C] *)
    rStartupHeater_Temp_DegC        : REAL;     (* Electric startup preheater core temperature [deg C] *)

    (* ===================================================================================== *)
    (* 3. LOOP PRESSURES & DIFFERENTIAL TRANSMITTERS (2oo3 TMR) [bar], [mbar]                *)
    (* ===================================================================================== *)
    rLoopPressure_bar_Ch1           : REAL;     (* Synthesis loop discharge pressure Ch1 [bar] *)
    rLoopPressure_bar_Ch2           : REAL;     (* Synthesis loop discharge pressure Ch2 [bar] *)
    rLoopPressure_bar_Ch3           : REAL;     (* Synthesis loop discharge pressure Ch3 [bar] *)
    rConverterDiffPress_bar         : REAL;     (* Converter catalyst basket differential pressure [bar] *)
    rLoopRecycleDiffPress_mbar      : REAL;     (* Loop circulating differential pressure [mbar] *)
    rCompressorSuctionPress_bar     : REAL;     (* Syngas compressor 1st stage suction pressure [bar] *)
    rCompressorInterstagePress_bar  : REAL;     (* Syngas compressor LP-HP interstage pressure [bar] *)

    (* ===================================================================================== *)
    (* 4. SYNGAS COMPRESSOR & TURBINE DYNAMICS (2oo3 TMR) [rpm], [mbar], [MW], [mm/s], [mm]  *)
    (* ===================================================================================== *)
    rCompressorSpeed_rpm_Ch1        : REAL;     (* Syngas compressor shaft speed Ch1 [rpm] *)
    rCompressorSpeed_rpm_Ch2        : REAL;     (* Syngas compressor shaft speed Ch2 [rpm] *)
    rCompressorSpeed_rpm_Ch3        : REAL;     (* Syngas compressor shaft speed Ch3 [rpm] *)
    rSurgeDiffPress_mbar_Ch1        : REAL;     (* Anti-surge orifice differential pressure Ch1 [mbar] *)
    rSurgeDiffPress_mbar_Ch2        : REAL;     (* Anti-surge orifice differential pressure Ch2 [mbar] *)
    rSurgeDiffPress_mbar_Ch3        : REAL;     (* Anti-surge orifice differential pressure Ch3 [mbar] *)
    rTurbinePower_MW                : REAL;     (* Steam turbine instantaneous mechanical shaft power [MW] *)
    rTurbineSteamFlow_th            : REAL;     (* 110 bar HP steam consumption rate [t/h] *)
    rTurbineVibration_mms           : REAL;     (* Turbine radial shaft vibration velocity RMS [mm/s] *)
    rThrustBearingDisplace_mm       : REAL;     (* Compressor axial thrust bearing displacement [mm] *)
    rLubeOilPressure_bar            : REAL;     (* Compressor lubrication oil manifold pressure [bar] *)

    (* ===================================================================================== *)
    (* 5. GAS COMPOSITIONS & LOOP STOICHIOMETRY (2oo3 TMR) [mol/mol]                         *)
    (* ===================================================================================== *)
    rLoopH2_N2_Ratio_Ch1            : REAL;     (* Circulating loop H2:N2 molar ratio Ch1 [mol/mol] *)
    rLoopH2_N2_Ratio_Ch2            : REAL;     (* Circulating loop H2:N2 molar ratio Ch2 [mol/mol] *)
    rLoopH2_N2_Ratio_Ch3            : REAL;     (* Circulating loop H2:N2 molar ratio Ch3 [mol/mol] *)
    rConverterEffluentNH3_Ch1       : REAL;     (* Converter exit NH3 mole fraction Ch1 [mol/mol] *)
    rConverterEffluentNH3_Ch2       : REAL;     (* Converter exit NH3 mole fraction Ch2 [mol/mol] *)
    rConverterEffluentNH3_Ch3       : REAL;     (* Converter exit NH3 mole fraction Ch3 [mol/mol] *)
    rLoopInerts_Methane_molmol      : REAL;     (* Circulating loop methane (CH4) mole fraction [mol/mol] *)
    rLoopInerts_Argon_molmol        : REAL;     (* Circulating loop argon (Ar) mole fraction [mol/mol] *)
    rMakeupSyngasH2_molmol          : REAL;     (* Fresh makeup syngas H2 fraction [mol/mol] *)
    rCryoHruReturnH2_molmol         : REAL;     (* Cryogenic recovery return gas H2 fraction [mol/mol] *)

    (* ===================================================================================== *)
    (* 6. FLOW RATES & LIQUID PRODUCTION METRICS [Nm3/h], [kg/s], [t/day], [%]               *)
    (* ===================================================================================== *)
    rMakeupSyngasFlow_Nm3h          : REAL;     (* Fresh makeup syngas mass flow [Nm3/h] *)
    rLoopCirculationFlow_Nm3h       : REAL;     (* Total loop gas circulation rate [Nm3/h] *)
    rPurgeGasFlow_Nm3h              : REAL;     (* Loop continuous purge gas bleed flow [Nm3/h] *)
    rLiquidAmmoniaYield_kgs         : REAL;     (* Net anhydrous liquid NH3 production [kg/s] *)
    rAmmoniaChillerTemp_DegC        : REAL;     (* Cold catch separator refrigeration temperature [deg C] *)
    rColdCatchDrumLevel_pct         : REAL;     (* Final ammonia liquid separator vessel level [%] *)
    rSuctionDrumLevel_pct           : REAL;     (* Compressor suction KO drum condensate level [%] *)

    (* ===================================================================================== *)
    (* 7. SUPERVISORY SETPOINTS & SYSTEM TIMING [bar], [deg C], [t/day], [s]                 *)
    (* ===================================================================================== *)
    rTargetLoopPressure_bar         : REAL;     (* Supervisory target loop operating pressure [bar] *)
    rTargetProductionRate_tday      : REAL;     (* Target anhydrous ammonia production setpoint [t/day] *)
    rTargetH2_N2_Ratio              : REAL;     (* Target loop stoichiometric ratio (nom 2.95) [mol/mol] *)
    rTargetBed1InletTemp_DegC       : REAL;     (* Bed 1 inlet setpoint (nom 385.0) [deg C] *)
    rMaxAllowableBedTemp_DegC       : REAL;     (* Absolute catalyst protection ceiling [deg C] *)
    rCycleTime_sec                  : REAL;     (* Deterministic PLC scan cycle time [s] *)
END_VAR
""")

    # 3. VAR_OUTPUT
    parts.append("""VAR_OUTPUT
    (* ===================================================================================== *)
    (* 1. DISCRETE OPERATIONAL FLAGS & SUPERVISORY STATUS                                    *)
    (* ===================================================================================== *)
    bSystemRunning                  : BOOL;     (* Ammonia synthesis plant active running status *)
    bSystemReady                    : BOOL;     (* Loop pressurized, converter warmed, ready for full load *)
    bSystemTripped                  : BOOL;     (* Latched SIL-3 safety shutdown condition active *)
    bMpcControllerActive            : BOOL;     (* Receding-horizon multivariable MPC in closed-loop control *)
    bTmrDegradedMode                : BOOL;     (* Operating under single sensor failure degradation *)
    bAutothermalReactionIgnited     : BOOL;     (* Exothermic Haber-Bosch reaction autothermal light-off confirmed *)
    bCryoHruActive                  : BOOL;     (* Cryogenic Hydrogen Recovery Unit operational and recovering H2 *)
    bAntiSurgeActive                : BOOL;     (* Compressor anti-surge valve active or surge kick triggered *)
    bCatalystThermalRunawayWarning  : BOOL;     (* Rapid Bed exotherm approaching sintering ceiling (> 510 C) *)

    (* ===================================================================================== *)
    (* 2. CONVERTER INTER-BED QUENCH VALVE COMMANDS [%]                                      *)
    (* ===================================================================================== *)
    rQuenchValve1_Cmd_pct           : REAL;     (* Bed 1-2 inter-bed cold syngas quench valve command [%] *)
    rQuenchValve2_Cmd_pct           : REAL;     (* Bed 2-3 inter-bed cold syngas quench valve command [%] *)
    rQuenchValve3_Cmd_pct           : REAL;     (* Bed 3-4 inter-bed cold syngas quench valve command [%] *)
    rStartupHeaterThyristor_pct     : REAL;     (* Electric startup preheater thyristor power demand [%] *)

    (* ===================================================================================== *)
    (* 3. SYNGAS COMPRESSOR & TURBINE ACTUATION [%], [rpm]                                   *)
    (* ===================================================================================== *)
    rTurbineGovernorDemand_rpm      : REAL;     (* Steam turbine governor speed setpoint command [rpm] *)
    rAntiSurgeValve_Cmd_pct         : REAL;     (* Syngas compressor anti-surge recycle valve command [%] *)
    rMakeupSyngasValve_Cmd_pct      : REAL;     (* Fresh makeup syngas master inlet control valve [%] *)
    rMakeupH2_TrimValve_Cmd_pct     : REAL;     (* Stoichiometric H2 makeup fine trim valve command [%] *)

    (* ===================================================================================== *)
    (* 4. PURGE BLEED & REFRIGERATION CHILLER ACTUATION [%], [Nm3/h]                         *)
    (* ===================================================================================== *)
    rPurgeBleedValve_Cmd_pct        : REAL;     (* Continuous loop inert gas purge bleed valve command [%] *)
    rChillerRefrigerationDemand_pct : REAL;     (* Ammonia refrigeration compressor capacity demand [%] *)
    rLiquidAmmoniaDrawValve_pct     : REAL;     (* Anhydrous liquid NH3 letdown valve to storage tank [%] *)
    rCryoHruH2ReturnRate_Nm3h       : REAL;     (* Calculated pure H2 return flow rate from cryo unit [Nm3/h] *)

    (* ===================================================================================== *)
    (* 5. SYNTHESIS EFFICIENCY & THERMODYNAMIC PERFORMANCE METRICS [%], [mol/mol], [t/day]   *)
    (* ===================================================================================== *)
    rCurrentAmmoniaDailyRate_tday   : REAL;     (* Normalized 24-hour anhydrous ammonia production [t/day] *)
    rSinglePassConversion_pct       : REAL;     (* Converter single-pass nitrogen conversion efficiency [%] *)
    rTotalInertsConcentration_pct   : REAL;     (* Total loop circulating inerts (CH4 + Ar) concentration [%] *)
    rCalculatedSurgeMargin_pct      : REAL;     (* Instantaneous compressor aerodynamic surge margin [%] *)
    rCatalystActivityFactor         : REAL;     (* Estimated catalyst deactivation / health index [0.0 - 1.0] *)
    rReactionHeatGenerated_MW       : REAL;     (* Total thermochemical Haber-Bosch heat release [MW] *)

    (* ===================================================================================== *)
    (* 6. BIT-PACKED STATUS & DIAGNOSTIC REGISTERS (DWORD)                                   *)
    (* ===================================================================================== *)
    dwStatusWord                    : DWORD;    (* Bit-packed plant status and operational FSM state *)
    dwAlarmWord1                    : DWORD;    (* SIL-3 critical process and compressor safety trips *)
    dwAlarmWord2                    : DWORD;    (* Thermal runaway, stoichiometry, and environmental trips *)
    dwWarningWord                   : DWORD;    (* Maintenance alerts, sensor degradation, and surge warnings *)
END_VAR
""")

    # 4. VAR
    parts.append("""VAR
    (* ===================================================================================== *)
    (* 1. THERMODYNAMIC & CHEMICAL CONSTANTS                                                 *)
    (* ===================================================================================== *)
    rConst_GasConst_R               : REAL := 8.31446;      (* Universal gas constant [J/(mol*K)] *)
    rConst_MolarMass_NH3            : REAL := 17.0305;      (* Molecular weight of NH3 [g/mol] *)
    rConst_MolarMass_N2             : REAL := 28.0134;      (* Molecular weight of N2 [g/mol] *)
    rConst_MolarMass_H2             : REAL := 2.01588;      (* Molecular weight of H2 [g/mol] *)
    rConst_MolarMass_CH4            : REAL := 16.0425;      (* Molecular weight of CH4 [g/mol] *)
    rConst_MolarMass_Ar             : REAL := 39.9480;      (* Molecular weight of Ar [g/mol] *)
    rConst_StandardMolarVol         : REAL := 22.414;       (* Standard molar volume [Nm3/kmol] *)
    rConst_DeltaH_Rxn_Jmol          : REAL := -46220.0;     (* Standard reaction enthalpy [J/mol NH3] *)
    rConst_SpecificHeat_Gas_JkgK    : REAL := 3250.0;       (* Average syngas specific heat [J/(kg*K)] *)
    rConst_LatentHeat_NH3_Jkg       : REAL := 1371200.0;    (* Latent heat of vaporization of NH3 [J/kg] *)

    (* ===================================================================================== *)
    (* 2. TEMKIN-PYZHEV KINETIC PARAMETERS & REACTOR BED GEOMETRY                            *)
    (* ===================================================================================== *)
    rKinetic_k10                    : REAL := 1.79E+04;     (* Forward reaction pre-exponential factor *)
    rKinetic_E1                     : REAL := 87400.0;      (* Forward activation energy [J/mol] *)
    rKinetic_k20                    : REAL := 2.57E+14;     (* Reverse reaction pre-exponential factor *)
    rKinetic_E2                     : REAL := 166500.0;     (* Reverse activation energy [J/mol] *)
    rKinetic_Alpha                  : REAL := 0.500;        (* Temkin kinetics transfer coefficient *)
    rBed1_CatalystVolume_m3         : REAL := 18.5;         (* Catalyst volume Bed 1 [m3] *)
    rBed2_CatalystVolume_m3         : REAL := 26.2;         (* Catalyst volume Bed 2 [m3] *)
    rBed3_CatalystVolume_m3         : REAL := 34.8;         (* Catalyst volume Bed 3 [m3] *)
    rBed4_CatalystVolume_m3         : REAL := 42.5;         (* Catalyst volume Bed 4 [m3] *)
    rTotalCatalystVolume_m3         : REAL := 122.0;        (* Total converter catalyst inventory [m3] *)

    (* ===================================================================================== *)
    (* 3. 2oo3 TRIPLE MODULAR REDUNDANCY VOTED INTERNAL REGISTERS                            *)
    (* ===================================================================================== *)
    rVotedBed1Temp_DegC             : REAL := 385.0;
    rVotedBed2Temp_DegC             : REAL := 410.0;
    rVotedBed3Temp_DegC             : REAL := 400.0;
    rVotedBed4Temp_DegC             : REAL := 432.0;
    rVotedLoopPressure_bar          : REAL := 200.0;
    rVotedCompressorSpeed_rpm       : REAL := 10500.0;
    rVotedSurgeDiffPress_mbar       : REAL := 185.0;
    rVotedH2_N2_Ratio               : REAL := 2.95;
    rVotedConverterEffluentNH3      : REAL := 0.185;

    (* 2oo3 Discrepancy & Health Flags *)
    bBed1Temp_Ch1_Fault             : BOOL := FALSE;
    bBed1Temp_Ch2_Fault             : BOOL := FALSE;
    bBed1Temp_Ch3_Fault             : BOOL := FALSE;
    bBed1Temp_Degraded              : BOOL := FALSE;
    bBed2Temp_Ch1_Fault             : BOOL := FALSE;
    bBed2Temp_Ch2_Fault             : BOOL := FALSE;
    bBed2Temp_Ch3_Fault             : BOOL := FALSE;
    bBed2Temp_Degraded              : BOOL := FALSE;
    bBed3Temp_Ch1_Fault             : BOOL := FALSE;
    bBed3Temp_Ch2_Fault             : BOOL := FALSE;
    bBed3Temp_Ch3_Fault             : BOOL := FALSE;
    bBed3Temp_Degraded              : BOOL := FALSE;
    bBed4Temp_Ch1_Fault             : BOOL := FALSE;
    bBed4Temp_Ch2_Fault             : BOOL := FALSE;
    bBed4Temp_Ch3_Fault             : BOOL := FALSE;
    bBed4Temp_Degraded              : BOOL := FALSE;
    bLoopPress_Ch1_Fault            : BOOL := FALSE;
    bLoopPress_Ch2_Fault            : BOOL := FALSE;
    bLoopPress_Ch3_Fault            : BOOL := FALSE;
    bLoopPress_Degraded             : BOOL := FALSE;
    bCompSpeed_Ch1_Fault            : BOOL := FALSE;
    bCompSpeed_Ch2_Fault            : BOOL := FALSE;
    bCompSpeed_Ch3_Fault            : BOOL := FALSE;
    bCompSpeed_Degraded             : BOOL := FALSE;
    bSurgeDiff_Ch1_Fault            : BOOL := FALSE;
    bSurgeDiff_Ch2_Fault            : BOOL := FALSE;
    bSurgeDiff_Ch3_Fault            : BOOL := FALSE;
    bSurgeDiff_Degraded             : BOOL := FALSE;
    bRatio_Ch1_Fault                : BOOL := FALSE;
    bRatio_Ch2_Fault                : BOOL := FALSE;
    bRatio_Ch3_Fault                : BOOL := FALSE;
    bRatio_Degraded                 : BOOL := FALSE;
    bEffluentNH3_Ch1_Fault          : BOOL := FALSE;
    bEffluentNH3_Ch2_Fault          : BOOL := FALSE;
    bEffluentNH3_Ch3_Fault          : BOOL := FALSE;
    bEffluentNH3_Degraded           : BOOL := FALSE;

    (* 2oo3 Discrepancy Accumulator Timers *)
    rTimer_Bed1_Discrepancy         : REAL := 0.0;
    rTimer_Bed2_Discrepancy         : REAL := 0.0;
    rTimer_Bed3_Discrepancy         : REAL := 0.0;
    rTimer_Bed4_Discrepancy         : REAL := 0.0;
    rTimer_LoopPress_Discrepancy    : REAL := 0.0;
    rTimer_CompSpeed_Discrepancy    : REAL := 0.0;
    rTimer_SurgeDiff_Discrepancy    : REAL := 0.0;
    rTimer_Ratio_Discrepancy        : REAL := 0.0;
    rTimer_EffluentNH3_Discrepancy  : REAL := 0.0;

    (* ===================================================================================== *)
    (* 4. 16x16 DISCRETE STATE-SPACE MODEL MATRICES & TRAJECTORY VECTORS                    *)
    (* States x[1..16]:                                                                      *)
    (*  x1:  T_Bed1 [C],               x2:  T_Bed2 [C],                                      *)
    (*  x3:  T_Bed3 [C],               x4:  T_Bed4 [C],                                      *)
    (*  x5:  P_Loop [bar],             x6:  y_NH3_effluent [mol/mol],                        *)
    (*  x7:  y_H2_loop [mol/mol],      x8:  y_N2_loop [mol/mol],                             *)
    (*  x9:  y_Inerts_loop [mol/mol],  x10: m_NH3_liq_rate [kg/s],                           *)
    (*  x11: N_Compressor [rpm],       x12: Margin_Surge [%],                                *)
    (*  x13: T_Chiller [C],            x14: L_SuctionDrum [%],                               *)
    (*  x15: Flow_Purge_Cryo [Nm3/h],  x16: P_Turbine [MW]                                   *)
    (* Control Inputs u[1..8]:                                                               *)
    (*  u1: Quench 1 [%],              u2: Quench 2 [%],                                     *)
    (*  u3: Quench 3 [%],              u4: Turbine Speed Gov [rpm],                          *)
    (*  u5: AntiSurge Valve [%],       u6: Purge Bleed Valve [%],                            *)
    (*  u7: Makeup Trim Valve [%],     u8: Chiller Duty [%]                                  *)
    (* ===================================================================================== *)
    aMatrix_A                       : ARRAY[1..16, 1..16] OF REAL;
    aMatrix_B                       : ARRAY[1..16, 1..8] OF REAL;
    aMatrix_C                       : ARRAY[1..16, 1..16] OF REAL;
    aMatrix_D                       : ARRAY[1..16, 1..8] OF REAL;

    aState_x                        : ARRAY[1..16] OF REAL;
    aState_x_next                   : ARRAY[1..16] OF REAL;
    aState_x_err                    : ARRAY[1..16] OF REAL;
    aState_y_pred                   : ARRAY[1..16] OF REAL;
    aControl_u                      : ARRAY[1..8] OF REAL;
    aControl_u_prev                 : ARRAY[1..8] OF REAL;
    aControl_u_delta                : ARRAY[1..8] OF REAL;
    aState_x_target                 : ARRAY[1..16] OF REAL;

    (* MPC Quadratic Weights *)
    aWeight_Q                       : ARRAY[1..16] OF REAL;
    aWeight_R                       : ARRAY[1..8] OF REAL;
    aWeight_P                       : ARRAY[1..16] OF REAL;
    aWeight_S_slew                  : ARRAY[1..8] OF REAL;

    (* MPC Solver Optimization Workspaces *)
    aGrad_J                         : ARRAY[1..8] OF REAL;
    aStep_u                         : ARRAY[1..8] OF REAL;
    rMpcObjectiveValue              : REAL := 0.0;
    iMpcIter                        : INT := 0;
    iStateIdx                       : INT := 1;
    jInputIdx                       : INT := 1;
    kColIdx                         : INT := 1;
    bMpcConverged                   : BOOL := FALSE;

    (* ===================================================================================== *)
    (* 5. COMPRESSOR ANTI-SURGE & AERODYNAMIC HEAD VARIABLES                                 *)
    (* ===================================================================================== *)
    rComp_PolytropicHead_kJkg       : REAL := 0.0;
    rComp_InletVolFlow_m3h          : REAL := 0.0;
    rComp_PressureRatio             : REAL := 1.0;
    rComp_SurgeDpLimit_mbar         : REAL := 100.0;
    rComp_SurgeDev_pct              : REAL := 15.0;
    rSurgeDerivativeRate            : REAL := 0.0;
    rPrevSurgeMargin_pct            : REAL := 15.0;
    rSurgeKickCommand_pct           : REAL := 0.0;
    rAntiSurgePidOutput_pct         : REAL := 0.0;
    rAntiSurgeIntegral              : REAL := 0.0;

    (* ===================================================================================== *)
    (* 6. TEMKIN-PYZHEV KINETIC EVALUATION WORKSPACE                                         *)
    (* ===================================================================================== *)
    rBed1_Rate_kmols                : REAL := 0.0;
    rBed2_Rate_kmols                : REAL := 0.0;
    rBed3_Rate_kmols                : REAL := 0.0;
    rBed4_Rate_kmols                : REAL := 0.0;
    rEquilConstant_Kp               : REAL := 0.0;
    rPartialPress_N2_bar            : REAL := 0.0;
    rPartialPress_H2_bar            : REAL := 0.0;
    rPartialPress_NH3_bar           : REAL := 0.0;
    rArrhenius_k1                   : REAL := 0.0;
    rArrhenius_k2                   : REAL := 0.0;
    rReactionQuotient               : REAL := 0.0;
    rBed1_Exotherm_C                : REAL := 0.0;
    rBed2_Exotherm_C                : REAL := 0.0;
    rBed3_Exotherm_C                : REAL := 0.0;
    rBed4_Exotherm_C                : REAL := 0.0;

    (* ===================================================================================== *)
    (* 7. CLOSED-LOOP STOICHIOMETRY & RATIO TRIM INTEGRATORS                                 *)
    (* ===================================================================================== *)
    rRatioError                     : REAL := 0.0;
    rRatioIntegral                  : REAL := 0.0;
    rRatioDerivative                : REAL := 0.0;
    rRatioPrevError                 : REAL := 0.0;
    rRatioTrimOutput_pct            : REAL := 0.0;

    (* ===================================================================================== *)
    (* 8. CRYOGENIC PURGE RECOVERY & CHILLER FLASH INTEGRATORS                               *)
    (* ===================================================================================== *)
    rCryoHruPurgeFeed_kgs           : REAL := 0.0;
    rCryoHruSeparationFactor        : REAL := 0.920;
    rChillerCondenserDuty_MW        : REAL := 0.0;
    rLiquidAmmoniaCondensation_kgs  : REAL := 0.0;
    rLetdownValveInternal_pct       : REAL := 45.0;

    (* ===================================================================================== *)
    (* 9. 12-STAGE FINITE STATE MACHINE (FSM) & OPERATIONAL TIMERS                           *)
    (* ===================================================================================== *)
    iState                          : INT := 10;
    iPreviousState                  : INT := 10;
    rStateTimer_sec                 : REAL := 0.0;
    rPressurizationRampRate_barmin  : REAL := 2.5;
    rConverterWarmupRate_DegCh      : REAL := 20.0;
    rShutdownCooldownRate_DegCh     : REAL := 25.0;
    rCompressorWarmupTimer_sec      : REAL := 0.0;
    bLightoffConfirmed              : BOOL := FALSE;
    bCryoPermissiveActive           : BOOL := FALSE;

    (* ===================================================================================== *)
    (* 10. ALARM HYSTERESIS, SIL-3 TRIP LATCHES & TELEMETRY REGISTERS                        *)
    (* ===================================================================================== *)
    bAlarmHighBed1_Active           : BOOL := FALSE;
    bAlarmHighBed2_Active           : BOOL := FALSE;
    bAlarmHighBed3_Active           : BOOL := FALSE;
    bAlarmHighBed4_Active           : BOOL := FALSE;
    bAlarmHighLoopPress_Active      : BOOL := FALSE;
    bAlarmLowSurgeMargin_Active     : BOOL := FALSE;
    bAlarmHighInerts_Active         : BOOL := FALSE;
    bAlarmRatioExcursion_Active     : BOOL := FALSE;
    bThrustDisplacementTrip_Active  : BOOL := FALSE;
    bVibrationTrip_Active           : BOOL := FALSE;
    bCatalystRunawayTrip_Active     : BOOL := FALSE;
    bOverpressureTrip_Active        : BOOL := FALSE;
    bCompressorSurgeTrip_Active     : BOOL := FALSE;
    bSuctionDrumHighLevelTrip_Active: BOOL := FALSE;
    bAmmoniaReleaseTrip_Active      : BOOL := FALSE;
END_VAR
""")

    # 5. Logic: Phase 1: 2oo3 TMR Voting
    parts.append("""(* ========================================================================================= *)
(* === PHASE 1: TRIPLE MODULAR REDUNDANCY (2oo3) SENSOR VOTING & DISCREPANCY TIMERS       === *)
(* ========================================================================================= *)
(* Evaluates 8 critical instrument triplets with cross-channel discrepancy monitoring,       *)
(* 2.5-second persistence timers, and bumpless failover to 1oo2 averaging and single channel *)

(* --- 1.1 Converter Bed 1 Temperature (Tolerance: 15.0 deg C) --- *)
IF ABS(rBed1_Temp_DegC_Ch1 - rBed1_Temp_DegC_Ch2) > 15.0 OR
   ABS(rBed1_Temp_DegC_Ch2 - rBed1_Temp_DegC_Ch3) > 15.0 OR
   ABS(rBed1_Temp_DegC_Ch1 - rBed1_Temp_DegC_Ch3) > 15.0 THEN
    rTimer_Bed1_Discrepancy := rTimer_Bed1_Discrepancy + rCycleTime_sec;
    IF rTimer_Bed1_Discrepancy >= 2.5 THEN
        IF ABS(rBed1_Temp_DegC_Ch1 - rBed1_Temp_DegC_Ch2) > 15.0 AND ABS(rBed1_Temp_DegC_Ch1 - rBed1_Temp_DegC_Ch3) > 15.0 THEN
            bBed1Temp_Ch1_Fault := TRUE;
        END_IF;
        IF ABS(rBed1_Temp_DegC_Ch2 - rBed1_Temp_DegC_Ch1) > 15.0 AND ABS(rBed1_Temp_DegC_Ch2 - rBed1_Temp_DegC_Ch3) > 15.0 THEN
            bBed1Temp_Ch2_Fault := TRUE;
        END_IF;
        IF ABS(rBed1_Temp_DegC_Ch3 - rBed1_Temp_DegC_Ch1) > 15.0 AND ABS(rBed1_Temp_DegC_Ch3 - rBed1_Temp_DegC_Ch2) > 15.0 THEN
            bBed1Temp_Ch3_Fault := TRUE;
        END_IF;
    END_IF;
ELSE
    rTimer_Bed1_Discrepancy := 0.0;
END_IF;

bBed1Temp_Degraded := bBed1Temp_Ch1_Fault OR bBed1Temp_Ch2_Fault OR bBed1Temp_Ch3_Fault;

IF NOT bBed1Temp_Degraded THEN
    IF (rBed1_Temp_DegC_Ch1 >= rBed1_Temp_DegC_Ch2 AND rBed1_Temp_DegC_Ch1 <= rBed1_Temp_DegC_Ch3) OR
       (rBed1_Temp_DegC_Ch1 <= rBed1_Temp_DegC_Ch2 AND rBed1_Temp_DegC_Ch1 >= rBed1_Temp_DegC_Ch3) THEN
        rVotedBed1Temp_DegC := rBed1_Temp_DegC_Ch1;
    ELSIF (rBed1_Temp_DegC_Ch2 >= rBed1_Temp_DegC_Ch1 AND rBed1_Temp_DegC_Ch2 <= rBed1_Temp_DegC_Ch3) OR
          (rBed1_Temp_DegC_Ch2 <= rBed1_Temp_DegC_Ch1 AND rBed1_Temp_DegC_Ch2 >= rBed1_Temp_DegC_Ch3) THEN
        rVotedBed1Temp_DegC := rBed1_Temp_DegC_Ch2;
    ELSE
        rVotedBed1Temp_DegC := rBed1_Temp_DegC_Ch3;
    END_IF;
ELSIF bBed1Temp_Ch1_Fault AND NOT bBed1Temp_Ch2_Fault AND NOT bBed1Temp_Ch3_Fault THEN
    rVotedBed1Temp_DegC := (rBed1_Temp_DegC_Ch2 + rBed1_Temp_DegC_Ch3) * 0.50;
ELSIF bBed1Temp_Ch2_Fault AND NOT bBed1Temp_Ch1_Fault AND NOT bBed1Temp_Ch3_Fault THEN
    rVotedBed1Temp_DegC := (rBed1_Temp_DegC_Ch1 + rBed1_Temp_DegC_Ch3) * 0.50;
ELSIF bBed1Temp_Ch3_Fault AND NOT bBed1Temp_Ch1_Fault AND NOT bBed1Temp_Ch2_Fault THEN
    rVotedBed1Temp_DegC := (rBed1_Temp_DegC_Ch1 + rBed1_Temp_DegC_Ch2) * 0.50;
ELSE
    IF NOT bBed1Temp_Ch1_Fault THEN
        rVotedBed1Temp_DegC := rBed1_Temp_DegC_Ch1;
    ELSIF NOT bBed1Temp_Ch2_Fault THEN
        rVotedBed1Temp_DegC := rBed1_Temp_DegC_Ch2;
    ELSE
        rVotedBed1Temp_DegC := rBed1_Temp_DegC_Ch3;
    END_IF;
END_IF;

(* --- 1.2 Converter Bed 2 Temperature (Tolerance: 15.0 deg C) --- *)
IF ABS(rBed2_Temp_DegC_Ch1 - rBed2_Temp_DegC_Ch2) > 15.0 OR
   ABS(rBed2_Temp_DegC_Ch2 - rBed2_Temp_DegC_Ch3) > 15.0 OR
   ABS(rBed2_Temp_DegC_Ch1 - rBed2_Temp_DegC_Ch3) > 15.0 THEN
    rTimer_Bed2_Discrepancy := rTimer_Bed2_Discrepancy + rCycleTime_sec;
    IF rTimer_Bed2_Discrepancy >= 2.5 THEN
        IF ABS(rBed2_Temp_DegC_Ch1 - rBed2_Temp_DegC_Ch2) > 15.0 AND ABS(rBed2_Temp_DegC_Ch1 - rBed2_Temp_DegC_Ch3) > 15.0 THEN
            bBed2Temp_Ch1_Fault := TRUE;
        END_IF;
        IF ABS(rBed2_Temp_DegC_Ch2 - rBed2_Temp_DegC_Ch1) > 15.0 AND ABS(rBed2_Temp_DegC_Ch2 - rBed2_Temp_DegC_Ch3) > 15.0 THEN
            bBed2Temp_Ch2_Fault := TRUE;
        END_IF;
        IF ABS(rBed2_Temp_DegC_Ch3 - rBed2_Temp_DegC_Ch1) > 15.0 AND ABS(rBed2_Temp_DegC_Ch3 - rBed2_Temp_DegC_Ch2) > 15.0 THEN
            bBed2Temp_Ch3_Fault := TRUE;
        END_IF;
    END_IF;
ELSE
    rTimer_Bed2_Discrepancy := 0.0;
END_IF;

bBed2Temp_Degraded := bBed2Temp_Ch1_Fault OR bBed2Temp_Ch2_Fault OR bBed2Temp_Ch3_Fault;

IF NOT bBed2Temp_Degraded THEN
    IF (rBed2_Temp_DegC_Ch1 >= rBed2_Temp_DegC_Ch2 AND rBed2_Temp_DegC_Ch1 <= rBed2_Temp_DegC_Ch3) OR
       (rBed2_Temp_DegC_Ch1 <= rBed2_Temp_DegC_Ch2 AND rBed2_Temp_DegC_Ch1 >= rBed2_Temp_DegC_Ch3) THEN
        rVotedBed2Temp_DegC := rBed2_Temp_DegC_Ch1;
    ELSIF (rBed2_Temp_DegC_Ch2 >= rBed2_Temp_DegC_Ch1 AND rBed2_Temp_DegC_Ch2 <= rBed2_Temp_DegC_Ch3) OR
          (rBed2_Temp_DegC_Ch2 <= rBed2_Temp_DegC_Ch1 AND rBed2_Temp_DegC_Ch2 >= rBed2_Temp_DegC_Ch3) THEN
        rVotedBed2Temp_DegC := rBed2_Temp_DegC_Ch2;
    ELSE
        rVotedBed2Temp_DegC := rBed2_Temp_DegC_Ch3;
    END_IF;
ELSIF bBed2Temp_Ch1_Fault AND NOT bBed2Temp_Ch2_Fault AND NOT bBed2Temp_Ch3_Fault THEN
    rVotedBed2Temp_DegC := (rBed2_Temp_DegC_Ch2 + rBed2_Temp_DegC_Ch3) * 0.50;
ELSIF bBed2Temp_Ch2_Fault AND NOT bBed2Temp_Ch1_Fault AND NOT bBed2Temp_Ch3_Fault THEN
    rVotedBed2Temp_DegC := (rBed2_Temp_DegC_Ch1 + rBed2_Temp_DegC_Ch3) * 0.50;
ELSIF bBed2Temp_Ch3_Fault AND NOT bBed2Temp_Ch1_Fault AND NOT bBed2Temp_Ch2_Fault THEN
    rVotedBed2Temp_DegC := (rBed2_Temp_DegC_Ch1 + rBed2_Temp_DegC_Ch2) * 0.50;
ELSE
    IF NOT bBed2Temp_Ch1_Fault THEN
        rVotedBed2Temp_DegC := rBed2_Temp_DegC_Ch1;
    ELSIF NOT bBed2Temp_Ch2_Fault THEN
        rVotedBed2Temp_DegC := rBed2_Temp_DegC_Ch2;
    ELSE
        rVotedBed2Temp_DegC := rBed2_Temp_DegC_Ch3;
    END_IF;
END_IF;

(* --- 1.3 Converter Bed 3 Temperature (Tolerance: 15.0 deg C) --- *)
IF ABS(rBed3_Temp_DegC_Ch1 - rBed3_Temp_DegC_Ch2) > 15.0 OR
   ABS(rBed3_Temp_DegC_Ch2 - rBed3_Temp_DegC_Ch3) > 15.0 OR
   ABS(rBed3_Temp_DegC_Ch1 - rBed3_Temp_DegC_Ch3) > 15.0 THEN
    rTimer_Bed3_Discrepancy := rTimer_Bed3_Discrepancy + rCycleTime_sec;
    IF rTimer_Bed3_Discrepancy >= 2.5 THEN
        IF ABS(rBed3_Temp_DegC_Ch1 - rBed3_Temp_DegC_Ch2) > 15.0 AND ABS(rBed3_Temp_DegC_Ch1 - rBed3_Temp_DegC_Ch3) > 15.0 THEN
            bBed3Temp_Ch1_Fault := TRUE;
        END_IF;
        IF ABS(rBed3_Temp_DegC_Ch2 - rBed3_Temp_DegC_Ch1) > 15.0 AND ABS(rBed3_Temp_DegC_Ch2 - rBed3_Temp_DegC_Ch3) > 15.0 THEN
            bBed3Temp_Ch2_Fault := TRUE;
        END_IF;
        IF ABS(rBed3_Temp_DegC_Ch3 - rBed3_Temp_DegC_Ch1) > 15.0 AND ABS(rBed3_Temp_DegC_Ch3 - rBed3_Temp_DegC_Ch2) > 15.0 THEN
            bBed3Temp_Ch3_Fault := TRUE;
        END_IF;
    END_IF;
ELSE
    rTimer_Bed3_Discrepancy := 0.0;
END_IF;

bBed3Temp_Degraded := bBed3Temp_Ch1_Fault OR bBed3Temp_Ch2_Fault OR bBed3Temp_Ch3_Fault;

IF NOT bBed3Temp_Degraded THEN
    IF (rBed3_Temp_DegC_Ch1 >= rBed3_Temp_DegC_Ch2 AND rBed3_Temp_DegC_Ch1 <= rBed3_Temp_DegC_Ch3) OR
       (rBed3_Temp_DegC_Ch1 <= rBed3_Temp_DegC_Ch2 AND rBed3_Temp_DegC_Ch1 >= rBed3_Temp_DegC_Ch3) THEN
        rVotedBed3Temp_DegC := rBed3_Temp_DegC_Ch1;
    ELSIF (rBed3_Temp_DegC_Ch2 >= rBed3_Temp_DegC_Ch1 AND rBed3_Temp_DegC_Ch2 <= rBed3_Temp_DegC_Ch3) OR
          (rBed3_Temp_DegC_Ch2 <= rBed3_Temp_DegC_Ch1 AND rBed3_Temp_DegC_Ch2 >= rBed3_Temp_DegC_Ch3) THEN
        rVotedBed3Temp_DegC := rBed3_Temp_DegC_Ch2;
    ELSE
        rVotedBed3Temp_DegC := rBed3_Temp_DegC_Ch3;
    END_IF;
ELSIF bBed3Temp_Ch1_Fault AND NOT bBed3Temp_Ch2_Fault AND NOT bBed3Temp_Ch3_Fault THEN
    rVotedBed3Temp_DegC := (rBed3_Temp_DegC_Ch2 + rBed3_Temp_DegC_Ch3) * 0.50;
ELSIF bBed3Temp_Ch2_Fault AND NOT bBed3Temp_Ch1_Fault AND NOT bBed3Temp_Ch3_Fault THEN
    rVotedBed3Temp_DegC := (rBed3_Temp_DegC_Ch1 + rBed3_Temp_DegC_Ch3) * 0.50;
ELSIF bBed3Temp_Ch3_Fault AND NOT bBed3Temp_Ch1_Fault AND NOT bBed3Temp_Ch2_Fault THEN
    rVotedBed3Temp_DegC := (rBed3_Temp_DegC_Ch1 + rBed3_Temp_DegC_Ch2) * 0.50;
ELSE
    IF NOT bBed3Temp_Ch1_Fault THEN
        rVotedBed3Temp_DegC := rBed3_Temp_DegC_Ch1;
    ELSIF NOT bBed3Temp_Ch2_Fault THEN
        rVotedBed3Temp_DegC := rBed3_Temp_DegC_Ch2;
    ELSE
        rVotedBed3Temp_DegC := rBed3_Temp_DegC_Ch3;
    END_IF;
END_IF;

(* --- 1.4 Converter Bed 4 Temperature (Tolerance: 15.0 deg C) --- *)
IF ABS(rBed4_Temp_DegC_Ch1 - rBed4_Temp_DegC_Ch2) > 15.0 OR
   ABS(rBed4_Temp_DegC_Ch2 - rBed4_Temp_DegC_Ch3) > 15.0 OR
   ABS(rBed4_Temp_DegC_Ch1 - rBed4_Temp_DegC_Ch3) > 15.0 THEN
    rTimer_Bed4_Discrepancy := rTimer_Bed4_Discrepancy + rCycleTime_sec;
    IF rTimer_Bed4_Discrepancy >= 2.5 THEN
        IF ABS(rBed4_Temp_DegC_Ch1 - rBed4_Temp_DegC_Ch2) > 15.0 AND ABS(rBed4_Temp_DegC_Ch1 - rBed4_Temp_DegC_Ch3) > 15.0 THEN
            bBed4Temp_Ch1_Fault := TRUE;
        END_IF;
        IF ABS(rBed4_Temp_DegC_Ch2 - rBed4_Temp_DegC_Ch1) > 15.0 AND ABS(rBed4_Temp_DegC_Ch2 - rBed4_Temp_DegC_Ch3) > 15.0 THEN
            bBed4Temp_Ch2_Fault := TRUE;
        END_IF;
        IF ABS(rBed4_Temp_DegC_Ch3 - rBed4_Temp_DegC_Ch1) > 15.0 AND ABS(rBed4_Temp_DegC_Ch3 - rBed4_Temp_DegC_Ch2) > 15.0 THEN
            bBed4Temp_Ch3_Fault := TRUE;
        END_IF;
    END_IF;
ELSE
    rTimer_Bed4_Discrepancy := 0.0;
END_IF;

bBed4Temp_Degraded := bBed4Temp_Ch1_Fault OR bBed4Temp_Ch2_Fault OR bBed4Temp_Ch3_Fault;

IF NOT bBed4Temp_Degraded THEN
    IF (rBed4_Temp_DegC_Ch1 >= rBed4_Temp_DegC_Ch2 AND rBed4_Temp_DegC_Ch1 <= rBed4_Temp_DegC_Ch3) OR
       (rBed4_Temp_DegC_Ch1 <= rBed4_Temp_DegC_Ch2 AND rBed4_Temp_DegC_Ch1 >= rBed4_Temp_DegC_Ch3) THEN
        rVotedBed4Temp_DegC := rBed4_Temp_DegC_Ch1;
    ELSIF (rBed4_Temp_DegC_Ch2 >= rBed4_Temp_DegC_Ch1 AND rBed4_Temp_DegC_Ch2 <= rBed4_Temp_DegC_Ch3) OR
          (rBed4_Temp_DegC_Ch2 <= rBed4_Temp_DegC_Ch1 AND rBed4_Temp_DegC_Ch2 >= rBed4_Temp_DegC_Ch3) THEN
        rVotedBed4Temp_DegC := rBed4_Temp_DegC_Ch2;
    ELSE
        rVotedBed4Temp_DegC := rBed4_Temp_DegC_Ch3;
    END_IF;
ELSIF bBed4Temp_Ch1_Fault AND NOT bBed4Temp_Ch2_Fault AND NOT bBed4Temp_Ch3_Fault THEN
    rVotedBed4Temp_DegC := (rBed4_Temp_DegC_Ch2 + rBed4_Temp_DegC_Ch3) * 0.50;
ELSIF bBed4Temp_Ch2_Fault AND NOT bBed4Temp_Ch1_Fault AND NOT bBed4Temp_Ch3_Fault THEN
    rVotedBed4Temp_DegC := (rBed4_Temp_DegC_Ch1 + rBed4_Temp_DegC_Ch3) * 0.50;
ELSIF bBed4Temp_Ch3_Fault AND NOT bBed4Temp_Ch1_Fault AND NOT bBed4Temp_Ch2_Fault THEN
    rVotedBed4Temp_DegC := (rBed4_Temp_DegC_Ch1 + rBed4_Temp_DegC_Ch2) * 0.50;
ELSE
    IF NOT bBed4Temp_Ch1_Fault THEN
        rVotedBed4Temp_DegC := rBed4_Temp_DegC_Ch1;
    ELSIF NOT bBed4Temp_Ch2_Fault THEN
        rVotedBed4Temp_DegC := rBed4_Temp_DegC_Ch2;
    ELSE
        rVotedBed4Temp_DegC := rBed4_Temp_DegC_Ch3;
    END_IF;
END_IF;

(* --- 1.5 Loop Operating Pressure (Tolerance: 5.0 bar) --- *)
IF ABS(rLoopPressure_bar_Ch1 - rLoopPressure_bar_Ch2) > 5.0 OR
   ABS(rLoopPressure_bar_Ch2 - rLoopPressure_bar_Ch3) > 5.0 OR
   ABS(rLoopPressure_bar_Ch1 - rLoopPressure_bar_Ch3) > 5.0 THEN
    rTimer_LoopPress_Discrepancy := rTimer_LoopPress_Discrepancy + rCycleTime_sec;
    IF rTimer_LoopPress_Discrepancy >= 2.5 THEN
        IF ABS(rLoopPressure_bar_Ch1 - rLoopPressure_bar_Ch2) > 5.0 AND ABS(rLoopPressure_bar_Ch1 - rLoopPressure_bar_Ch3) > 5.0 THEN
            bLoopPress_Ch1_Fault := TRUE;
        END_IF;
        IF ABS(rLoopPressure_bar_Ch2 - rLoopPressure_bar_Ch1) > 5.0 AND ABS(rLoopPressure_bar_Ch2 - rLoopPressure_bar_Ch3) > 5.0 THEN
            bLoopPress_Ch2_Fault := TRUE;
        END_IF;
        IF ABS(rLoopPressure_bar_Ch3 - rLoopPressure_bar_Ch1) > 5.0 AND ABS(rLoopPressure_bar_Ch3 - rLoopPressure_bar_Ch2) > 5.0 THEN
            bLoopPress_Ch3_Fault := TRUE;
        END_IF;
    END_IF;
ELSE
    rTimer_LoopPress_Discrepancy := 0.0;
END_IF;

bLoopPress_Degraded := bLoopPress_Ch1_Fault OR bLoopPress_Ch2_Fault OR bLoopPress_Ch3_Fault;

IF NOT bLoopPress_Degraded THEN
    IF (rLoopPressure_bar_Ch1 >= rLoopPressure_bar_Ch2 AND rLoopPressure_bar_Ch1 <= rLoopPressure_bar_Ch3) OR
       (rLoopPressure_bar_Ch1 <= rLoopPressure_bar_Ch2 AND rLoopPressure_bar_Ch1 >= rLoopPressure_bar_Ch3) THEN
        rVotedLoopPressure_bar := rLoopPressure_bar_Ch1;
    ELSIF (rLoopPressure_bar_Ch2 >= rLoopPressure_bar_Ch1 AND rLoopPressure_bar_Ch2 <= rLoopPressure_bar_Ch3) OR
          (rLoopPressure_bar_Ch2 <= rLoopPressure_bar_Ch1 AND rLoopPressure_bar_Ch2 >= rLoopPressure_bar_Ch3) THEN
        rVotedLoopPressure_bar := rLoopPressure_bar_Ch2;
    ELSE
        rVotedLoopPressure_bar := rLoopPressure_bar_Ch3;
    END_IF;
ELSIF bLoopPress_Ch1_Fault AND NOT bLoopPress_Ch2_Fault AND NOT bLoopPress_Ch3_Fault THEN
    rVotedLoopPressure_bar := (rLoopPressure_bar_Ch2 + rLoopPressure_bar_Ch3) * 0.50;
ELSIF bLoopPress_Ch2_Fault AND NOT bLoopPress_Ch1_Fault AND NOT bLoopPress_Ch3_Fault THEN
    rVotedLoopPressure_bar := (rLoopPressure_bar_Ch1 + rLoopPressure_bar_Ch3) * 0.50;
ELSIF bLoopPress_Ch3_Fault AND NOT bLoopPress_Ch1_Fault AND NOT bLoopPress_Ch2_Fault THEN
    rVotedLoopPressure_bar := (rLoopPressure_bar_Ch1 + rLoopPressure_bar_Ch2) * 0.50;
ELSE
    IF NOT bLoopPress_Ch1_Fault THEN
        rVotedLoopPressure_bar := rLoopPressure_bar_Ch1;
    ELSIF NOT bLoopPress_Ch2_Fault THEN
        rVotedLoopPressure_bar := rLoopPressure_bar_Ch2;
    ELSE
        rVotedLoopPressure_bar := rLoopPressure_bar_Ch3;
    END_IF;
END_IF;

(* --- 1.6 Syngas Compressor Shaft Speed (Tolerance: 120.0 rpm) --- *)
IF ABS(rCompressorSpeed_rpm_Ch1 - rCompressorSpeed_rpm_Ch2) > 120.0 OR
   ABS(rCompressorSpeed_rpm_Ch2 - rCompressorSpeed_rpm_Ch3) > 120.0 OR
   ABS(rCompressorSpeed_rpm_Ch1 - rCompressorSpeed_rpm_Ch3) > 120.0 THEN
    rTimer_CompSpeed_Discrepancy := rTimer_CompSpeed_Discrepancy + rCycleTime_sec;
    IF rTimer_CompSpeed_Discrepancy >= 2.5 THEN
        IF ABS(rCompressorSpeed_rpm_Ch1 - rCompressorSpeed_rpm_Ch2) > 120.0 AND ABS(rCompressorSpeed_rpm_Ch1 - rCompressorSpeed_rpm_Ch3) > 120.0 THEN
            bCompSpeed_Ch1_Fault := TRUE;
        END_IF;
        IF ABS(rCompressorSpeed_rpm_Ch2 - rCompressorSpeed_rpm_Ch1) > 120.0 AND ABS(rCompressorSpeed_rpm_Ch2 - rCompressorSpeed_rpm_Ch3) > 120.0 THEN
            bCompSpeed_Ch2_Fault := TRUE;
        END_IF;
        IF ABS(rCompressorSpeed_rpm_Ch3 - rCompressorSpeed_rpm_Ch1) > 120.0 AND ABS(rCompressorSpeed_rpm_Ch3 - rCompressorSpeed_rpm_Ch2) > 120.0 THEN
            bCompSpeed_Ch3_Fault := TRUE;
        END_IF;
    END_IF;
ELSE
    rTimer_CompSpeed_Discrepancy := 0.0;
END_IF;

bCompSpeed_Degraded := bCompSpeed_Ch1_Fault OR bCompSpeed_Ch2_Fault OR bCompSpeed_Ch3_Fault;

IF NOT bCompSpeed_Degraded THEN
    IF (rCompressorSpeed_rpm_Ch1 >= rCompressorSpeed_rpm_Ch2 AND rCompressorSpeed_rpm_Ch1 <= rCompressorSpeed_rpm_Ch3) OR
       (rCompressorSpeed_rpm_Ch1 <= rCompressorSpeed_rpm_Ch2 AND rCompressorSpeed_rpm_Ch1 >= rCompressorSpeed_rpm_Ch3) THEN
        rVotedCompressorSpeed_rpm := rCompressorSpeed_rpm_Ch1;
    ELSIF (rCompressorSpeed_rpm_Ch2 >= rCompressorSpeed_rpm_Ch1 AND rCompressorSpeed_rpm_Ch2 <= rCompressorSpeed_rpm_Ch3) OR
          (rCompressorSpeed_rpm_Ch2 <= rCompressorSpeed_rpm_Ch1 AND rCompressorSpeed_rpm_Ch2 >= rCompressorSpeed_rpm_Ch3) THEN
        rVotedCompressorSpeed_rpm := rCompressorSpeed_rpm_Ch2;
    ELSE
        rVotedCompressorSpeed_rpm := rCompressorSpeed_rpm_Ch3;
    END_IF;
ELSIF bCompSpeed_Ch1_Fault AND NOT bCompSpeed_Ch2_Fault AND NOT bCompSpeed_Ch3_Fault THEN
    rVotedCompressorSpeed_rpm := (rCompressorSpeed_rpm_Ch2 + rCompressorSpeed_rpm_Ch3) * 0.50;
ELSIF bCompSpeed_Ch2_Fault AND NOT bCompSpeed_Ch1_Fault AND NOT bCompSpeed_Ch3_Fault THEN
    rVotedCompressorSpeed_rpm := (rCompressorSpeed_rpm_Ch1 + rCompressorSpeed_rpm_Ch3) * 0.50;
ELSIF bCompSpeed_Ch3_Fault AND NOT bCompSpeed_Ch1_Fault AND NOT bCompSpeed_Ch2_Fault THEN
    rVotedCompressorSpeed_rpm := (rCompressorSpeed_rpm_Ch1 + rCompressorSpeed_rpm_Ch2) * 0.50;
ELSE
    IF NOT bCompSpeed_Ch1_Fault THEN
        rVotedCompressorSpeed_rpm := rCompressorSpeed_rpm_Ch1;
    ELSIF NOT bCompSpeed_Ch2_Fault THEN
        rVotedCompressorSpeed_rpm := rCompressorSpeed_rpm_Ch2;
    ELSE
        rVotedCompressorSpeed_rpm := rCompressorSpeed_rpm_Ch3;
    END_IF;
END_IF;

(* --- 1.7 Anti-Surge Differential Pressure (Tolerance: 8.0 mbar) --- *)
IF ABS(rSurgeDiffPress_mbar_Ch1 - rSurgeDiffPress_mbar_Ch2) > 8.0 OR
   ABS(rSurgeDiffPress_mbar_Ch2 - rSurgeDiffPress_mbar_Ch3) > 8.0 OR
   ABS(rSurgeDiffPress_mbar_Ch1 - rSurgeDiffPress_mbar_Ch3) > 8.0 THEN
    rTimer_SurgeDiff_Discrepancy := rTimer_SurgeDiff_Discrepancy + rCycleTime_sec;
    IF rTimer_SurgeDiff_Discrepancy >= 2.5 THEN
        IF ABS(rSurgeDiffPress_mbar_Ch1 - rSurgeDiffPress_mbar_Ch2) > 8.0 AND ABS(rSurgeDiffPress_mbar_Ch1 - rSurgeDiffPress_mbar_Ch3) > 8.0 THEN
            bSurgeDiff_Ch1_Fault := TRUE;
        END_IF;
        IF ABS(rSurgeDiffPress_mbar_Ch2 - rSurgeDiffPress_mbar_Ch1) > 8.0 AND ABS(rSurgeDiffPress_mbar_Ch2 - rSurgeDiffPress_mbar_Ch3) > 8.0 THEN
            bSurgeDiff_Ch2_Fault := TRUE;
        END_IF;
        IF ABS(rSurgeDiffPress_mbar_Ch3 - rSurgeDiffPress_mbar_Ch1) > 8.0 AND ABS(rSurgeDiffPress_mbar_Ch3 - rSurgeDiffPress_mbar_Ch2) > 8.0 THEN
            bSurgeDiff_Ch3_Fault := TRUE;
        END_IF;
    END_IF;
ELSE
    rTimer_SurgeDiff_Discrepancy := 0.0;
END_IF;

bSurgeDiff_Degraded := bSurgeDiff_Ch1_Fault OR bSurgeDiff_Ch2_Fault OR bSurgeDiff_Ch3_Fault;

IF NOT bSurgeDiff_Degraded THEN
    IF (rSurgeDiffPress_mbar_Ch1 >= rSurgeDiffPress_mbar_Ch2 AND rSurgeDiffPress_mbar_Ch1 <= rSurgeDiffPress_mbar_Ch3) OR
       (rSurgeDiffPress_mbar_Ch1 <= rSurgeDiffPress_mbar_Ch2 AND rSurgeDiffPress_mbar_Ch1 >= rSurgeDiffPress_mbar_Ch3) THEN
        rVotedSurgeDiffPress_mbar := rSurgeDiffPress_mbar_Ch1;
    ELSIF (rSurgeDiffPress_mbar_Ch2 >= rSurgeDiffPress_mbar_Ch1 AND rSurgeDiffPress_mbar_Ch2 <= rSurgeDiffPress_mbar_Ch3) OR
          (rSurgeDiffPress_mbar_Ch2 <= rSurgeDiffPress_mbar_Ch1 AND rSurgeDiffPress_mbar_Ch2 >= rSurgeDiffPress_mbar_Ch3) THEN
        rVotedSurgeDiffPress_mbar := rSurgeDiffPress_mbar_Ch2;
    ELSE
        rVotedSurgeDiffPress_mbar := rSurgeDiffPress_mbar_Ch3;
    END_IF;
ELSIF bSurgeDiff_Ch1_Fault AND NOT bSurgeDiff_Ch2_Fault AND NOT bSurgeDiff_Ch3_Fault THEN
    rVotedSurgeDiffPress_mbar := (rSurgeDiffPress_mbar_Ch2 + rSurgeDiffPress_mbar_Ch3) * 0.50;
ELSIF bSurgeDiff_Ch2_Fault AND NOT bSurgeDiff_Ch1_Fault AND NOT bSurgeDiff_Ch3_Fault THEN
    rVotedSurgeDiffPress_mbar := (rSurgeDiffPress_mbar_Ch1 + rSurgeDiffPress_mbar_Ch3) * 0.50;
ELSIF bSurgeDiff_Ch3_Fault AND NOT bSurgeDiff_Ch1_Fault AND NOT bSurgeDiff_Ch2_Fault THEN
    rVotedSurgeDiffPress_mbar := (rSurgeDiffPress_mbar_Ch1 + rSurgeDiffPress_mbar_Ch2) * 0.50;
ELSE
    IF NOT bSurgeDiff_Ch1_Fault THEN
        rVotedSurgeDiffPress_mbar := rSurgeDiffPress_mbar_Ch1;
    ELSIF NOT bSurgeDiff_Ch2_Fault THEN
        rVotedSurgeDiffPress_mbar := rSurgeDiffPress_mbar_Ch2;
    ELSE
        rVotedSurgeDiffPress_mbar := rSurgeDiffPress_mbar_Ch3;
    END_IF;
END_IF;

(* --- 1.8 Loop H2:N2 Stoichiometric Ratio (Tolerance: 0.080 mol/mol) --- *)
IF ABS(rLoopH2_N2_Ratio_Ch1 - rLoopH2_N2_Ratio_Ch2) > 0.080 OR
   ABS(rLoopH2_N2_Ratio_Ch2 - rLoopH2_N2_Ratio_Ch3) > 0.080 OR
   ABS(rLoopH2_N2_Ratio_Ch1 - rLoopH2_N2_Ratio_Ch3) > 0.080 THEN
    rTimer_Ratio_Discrepancy := rTimer_Ratio_Discrepancy + rCycleTime_sec;
    IF rTimer_Ratio_Discrepancy >= 2.5 THEN
        IF ABS(rLoopH2_N2_Ratio_Ch1 - rLoopH2_N2_Ratio_Ch2) > 0.080 AND ABS(rLoopH2_N2_Ratio_Ch1 - rLoopH2_N2_Ratio_Ch3) > 0.080 THEN
            bRatio_Ch1_Fault := TRUE;
        END_IF;
        IF ABS(rLoopH2_N2_Ratio_Ch2 - rLoopH2_N2_Ratio_Ch1) > 0.080 AND ABS(rLoopH2_N2_Ratio_Ch2 - rLoopH2_N2_Ratio_Ch3) > 0.080 THEN
            bRatio_Ch2_Fault := TRUE;
        END_IF;
        IF ABS(rLoopH2_N2_Ratio_Ch3 - rLoopH2_N2_Ratio_Ch1) > 0.080 AND ABS(rLoopH2_N2_Ratio_Ch3 - rLoopH2_N2_Ratio_Ch2) > 0.080 THEN
            bRatio_Ch3_Fault := TRUE;
        END_IF;
    END_IF;
ELSE
    rTimer_Ratio_Discrepancy := 0.0;
END_IF;

bRatio_Degraded := bRatio_Ch1_Fault OR bRatio_Ch2_Fault OR bRatio_Ch3_Fault;

IF NOT bRatio_Degraded THEN
    IF (rLoopH2_N2_Ratio_Ch1 >= rLoopH2_N2_Ratio_Ch2 AND rLoopH2_N2_Ratio_Ch1 <= rLoopH2_N2_Ratio_Ch3) OR
       (rLoopH2_N2_Ratio_Ch1 <= rLoopH2_N2_Ratio_Ch2 AND rLoopH2_N2_Ratio_Ch1 >= rLoopH2_N2_Ratio_Ch3) THEN
        rVotedH2_N2_Ratio := rLoopH2_N2_Ratio_Ch1;
    ELSIF (rLoopH2_N2_Ratio_Ch2 >= rLoopH2_N2_Ratio_Ch1 AND rLoopH2_N2_Ratio_Ch2 <= rLoopH2_N2_Ratio_Ch3) OR
          (rLoopH2_N2_Ratio_Ch2 <= rLoopH2_N2_Ratio_Ch1 AND rLoopH2_N2_Ratio_Ch2 >= rLoopH2_N2_Ratio_Ch3) THEN
        rVotedH2_N2_Ratio := rLoopH2_N2_Ratio_Ch2;
    ELSE
        rVotedH2_N2_Ratio := rLoopH2_N2_Ratio_Ch3;
    END_IF;
ELSIF bRatio_Ch1_Fault AND NOT bRatio_Ch2_Fault AND NOT bRatio_Ch3_Fault THEN
    rVotedH2_N2_Ratio := (rLoopH2_N2_Ratio_Ch2 + rLoopH2_N2_Ratio_Ch3) * 0.50;
ELSIF bRatio_Ch2_Fault AND NOT bRatio_Ch1_Fault AND NOT bRatio_Ch3_Fault THEN
    rVotedH2_N2_Ratio := (rLoopH2_N2_Ratio_Ch1 + rLoopH2_N2_Ratio_Ch3) * 0.50;
ELSIF bRatio_Ch3_Fault AND NOT bRatio_Ch1_Fault AND NOT bRatio_Ch2_Fault THEN
    rVotedH2_N2_Ratio := (rLoopH2_N2_Ratio_Ch1 + rLoopH2_N2_Ratio_Ch2) * 0.50;
ELSE
    IF NOT bRatio_Ch1_Fault THEN
        rVotedH2_N2_Ratio := rLoopH2_N2_Ratio_Ch1;
    ELSIF NOT bRatio_Ch2_Fault THEN
        rVotedH2_N2_Ratio := rLoopH2_N2_Ratio_Ch2;
    ELSE
        rVotedH2_N2_Ratio := rLoopH2_N2_Ratio_Ch3;
    END_IF;
END_IF;

(* Cumulative Sensor Degraded Mode Flag *)
bTmrDegradedMode := bBed1Temp_Degraded OR bBed2Temp_Degraded OR bBed3Temp_Degraded OR
                    bBed4Temp_Degraded OR bLoopPress_Degraded OR bCompSpeed_Degraded OR
                    bSurgeDiff_Degraded OR bRatio_Degraded;
""")

    # 6. Logic: Phase 2: Complete Discrete State-Space Matrices (16x16 A, 16x8 B, 16x16 C, 16x8 D)
    # We will generate unrolled assignments for all entries of A, B, C, D!
    parts.append("""(* ========================================================================================= *)
(* === PHASE 2: DISCRETE STATE-SPACE INITIALIZATION (16x16 A, 16x8 B, C, D) & PREDICTION   === *)
(* ========================================================================================= *)
(* Complete unrolled mathematical linearization around 3,000 MTPD nominal Haber-Bosch point *)
(* Discretization step Ts = 0.5 s with complete thermal, pneumatic and kinetic cross-terms  *)
""")
    # Matrix A: 16x16
    a_lines = []
    a_lines.append("(* Matrix A [16x16] Discrete State Transition Matrix *)")
    # Base coefficients
    # diagonal values for each of the 16 states:
    diag_vals = [
        0.9150, 0.9080, 0.9020, 0.8950, # x1..x4: Bed temps
        0.9650,                         # x5: Loop Pressure
        0.9200,                         # x6: NH3 mole fraction
        0.9420,                         # x7: H2 mole fraction
        0.9420,                         # x8: N2 mole fraction
        0.9880,                         # x9: Inerts mole fraction
        0.8750,                         # x10: NH3 liquid rate
        0.9100,                         # x11: Compressor speed
        0.8850,                         # x12: Surge margin
        0.9250,                         # x13: Chiller temperature
        0.9400,                         # x14: Suction drum level
        0.9120,                         # x15: Purge flow
        0.8920                          # x16: Turbine power
    ]
    for r in range(1, 17):
        row_str = []
        for c in range(1, 17):
            val = 0.0000
            if r == c:
                val = diag_vals[r-1]
            elif r == 2 and c == 1:
                val = 0.0540 # Bed 1 exotherm warms Bed 2
            elif r == 3 and c == 2:
                val = 0.0480 # Bed 2 exotherm warms Bed 3
            elif r == 4 and c == 3:
                val = 0.0420 # Bed 3 exotherm warms Bed 4
            elif r == 5 and c == 11:
                val = 0.0035 # Compressor speed pressurizes loop
            elif r == 5 and c == 10:
                val = -0.0125 # Ammonia condensation relieves gas pressure
            elif r == 6 and c == 4:
                val = 0.00085 # Bed 4 reaction increases NH3 fraction
            elif r == 6 and c == 5:
                val = 0.00045 # Higher pressure increases equilibrium NH3
            elif r == 7 and c == 6:
                val = -0.0012 # NH3 synthesis consumes H2
            elif r == 8 and c == 6:
                val = -0.0004 # NH3 synthesis consumes N2
            elif r == 9 and c == 15:
                val = -0.0022 # Purge flow reduces loop inerts
            elif r == 10 and c == 6:
                val = 14.500  # Higher effluent NH3 drives condensation rate
            elif r == 10 and c == 13:
                val = -0.650  # Lower chiller temp increases condensation
            elif r == 11 and c == 16:
                val = 48.500  # Turbine power drives compressor shaft speed
            elif r == 12 and c == 11:
                val = 0.0042  # Higher speed shifts away from surge line
            elif r == 16 and c == 11:
                val = 0.0028  # Speed back-EMF / load torque coupling
            row_str.append(f"aMatrix_A[{r:2d}, {c:2d}] := {val:7.4f};")
        a_lines.append(" ".join(row_str[:4]))
        a_lines.append(" ".join(row_str[4:8]))
        a_lines.append(" ".join(row_str[8:12]))
        a_lines.append(" ".join(row_str[12:16]))

    parts.append("\n".join(a_lines))

    # Matrix B: 16x8
    b_lines = []
    b_lines.append("\n(* Matrix B [16x8] Discrete Actuator Input Gain Matrix *)")
    # Inputs:
    # u1: Quench 1 [%], u2: Quench 2 [%], u3: Quench 3 [%], u4: Turbine speed gov [rpm]
    # u5: Anti-surge [%], u6: Purge bleed [%], u7: Makeup trim [%], u8: Chiller duty [%]
    for r in range(1, 17):
        row_str = []
        for c in range(1, 9):
            val = 0.0000
            if r == 2 and c == 1:
                val = -0.3450 # Quench 1 cools Bed 2 inlet
            elif r == 3 and c == 2:
                val = -0.3120 # Quench 2 cools Bed 3 inlet
            elif r == 4 and c == 3:
                val = -0.2850 # Quench 3 cools Bed 4 inlet
            elif r == 5 and c == 4:
                val = 0.0022  # Compressor speed increases loop pressure
            elif r == 5 and c == 5:
                val = -0.0850 # Anti-surge opening reduces discharge pressure
            elif r == 5 and c == 6:
                val = -0.0450 # Purge bleed reduces loop pressure
            elif r == 7 and c == 7:
                val = 0.0045  # Makeup H2 trim increases H2 fraction
            elif r == 8 and c == 7:
                val = -0.0015 # Makeup H2 trim offsets N2 fraction
            elif r == 9 and c == 6:
                val = -0.0068 # Purge bleed lowers inerts
            elif r == 11 and c == 4:
                val = 0.1250  # Turbine governor increases shaft speed
            elif r == 12 and c == 5:
                val = 0.4500  # Anti-surge opening increases surge margin
            elif r == 13 and c == 8:
                val = -0.2450 # Chiller duty lowers flash temperature
            elif r == 15 and c == 6:
                val = 225.00  # Purge valve opening increases purge Nm3/h
            elif r == 16 and c == 4:
                val = 0.0150  # Governor valve lift increases turbine MW
            row_str.append(f"aMatrix_B[{r:2d}, {c:2d}] := {val:7.4f};")
        b_lines.append(" ".join(row_str[:4]))
        b_lines.append(" ".join(row_str[4:8]))

    parts.append("\n".join(b_lines))

    # Matrix C: 16x16
    c_lines = []
    c_lines.append("\n(* Matrix C [16x16] Discrete Observation Output Matrix *)")
    for r in range(1, 17):
        row_str = []
        for c in range(1, 17):
            val = 1.0000 if r == c else 0.0000
            row_str.append(f"aMatrix_C[{r:2d}, {c:2d}] := {val:7.4f};")
        c_lines.append(" ".join(row_str[:4]))
        c_lines.append(" ".join(row_str[4:8]))
        c_lines.append(" ".join(row_str[8:12]))
        c_lines.append(" ".join(row_str[12:16]))

    parts.append("\n".join(c_lines))

    # Matrix D: 16x8
    d_lines = []
    d_lines.append("\n(* Matrix D [16x8] Discrete Direct Feedthrough Matrix *)")
    for r in range(1, 17):
        row_str = []
        for c in range(1, 9):
            val = 0.0000
            if r == 12 and c == 5:
                val = 0.0500 # Direct anti-surge valve displacement feedthrough
            elif r == 15 and c == 6:
                val = 15.000 # Direct purge bleed valve displacement feedthrough
            row_str.append(f"aMatrix_D[{r:2d}, {c:2d}] := {val:7.4f};")
        d_lines.append(" ".join(row_str[:4]))
        d_lines.append(" ".join(row_str[4:8]))

    parts.append("\n".join(d_lines))

    # State vector population & propagation loop
    parts.append("""
(* Assign Current Plant Voted States into State Vector aState_x *)
aState_x[1]  := rVotedBed1Temp_DegC;
aState_x[2]  := rVotedBed2Temp_DegC;
aState_x[3]  := rVotedBed3Temp_DegC;
aState_x[4]  := rVotedBed4Temp_DegC;
aState_x[5]  := rVotedLoopPressure_bar;
aState_x[6]  := rVotedConverterEffluentNH3;
aState_x[7]  := (rVotedH2_N2_Ratio / (1.0 + rVotedH2_N2_Ratio)) * (1.0 - rLoopInerts_Methane_molmol - rLoopInerts_Argon_molmol);
aState_x[8]  := (1.0 / (1.0 + rVotedH2_N2_Ratio)) * (1.0 - rLoopInerts_Methane_molmol - rLoopInerts_Argon_molmol);
aState_x[9]  := rLoopInerts_Methane_molmol + rLoopInerts_Argon_molmol;
aState_x[10] := rLiquidAmmoniaYield_kgs;
aState_x[11] := rVotedCompressorSpeed_rpm;
aState_x[12] := rCalculatedSurgeMargin_pct;
aState_x[13] := rAmmoniaChillerTemp_DegC;
aState_x[14] := rSuctionDrumLevel_pct;
aState_x[15] := rPurgeGasFlow_Nm3h;
aState_x[16] := rTurbinePower_MW;

(* State-Space Time-Domain Forward Propagation: x[k+1] = A * x[k] + B * u[k] *)
FOR iStateIdx := 1 TO 16 DO
    aState_x_next[iStateIdx] := 0.0;
    FOR kColIdx := 1 TO 16 DO
        aState_x_next[iStateIdx] := aState_x_next[iStateIdx] + aMatrix_A[iStateIdx, kColIdx] * aState_x[kColIdx];
    END_FOR;
    FOR jInputIdx := 1 TO 8 DO
        aState_x_next[iStateIdx] := aState_x_next[iStateIdx] + aMatrix_B[iStateIdx, jInputIdx] * aControl_u[jInputIdx];
    END_FOR;
END_FOR;

(* Output Observation Estimation: y_pred[k] = C * x[k] + D * u[k] *)
FOR iStateIdx := 1 TO 16 DO
    aState_y_pred[iStateIdx] := 0.0;
    FOR kColIdx := 1 TO 16 DO
        aState_y_pred[iStateIdx] := aState_y_pred[iStateIdx] + aMatrix_C[iStateIdx, kColIdx] * aState_x[kColIdx];
    END_FOR;
    FOR jInputIdx := 1 TO 8 DO
        aState_y_pred[iStateIdx] := aState_y_pred[iStateIdx] + aMatrix_D[iStateIdx, jInputIdx] * aControl_u[jInputIdx];
    END_FOR;
END_FOR;
""")

    # 7. Logic: Phase 3: Temkin-Pyzhev Kinetics & Compressor Head
    parts.append("""(* ========================================================================================= *)
(* === PHASE 3: TEMKIN-PYZHEV KINETICS, COMPRESSOR AERODYNAMICS & ANTI-SURGE CONTROLLER   === *)
(* ========================================================================================= *)
(* Real-time calculation of partial pressures, Arrhenius rates, reaction enthalpies,        *)
(* centrifugal compressor polytropic head, dynamic surge line and derivative kick.          *)

(* --- 3.1 Partial Pressures & Fugacity Corrections [bar] --- *)
rPartialPress_N2_bar  := aState_x[8] * rVotedLoopPressure_bar * 0.985;
rPartialPress_H2_bar  := aState_x[7] * rVotedLoopPressure_bar * 1.015;
rPartialPress_NH3_bar := aState_x[6] * rVotedLoopPressure_bar * 0.960;

IF rPartialPress_NH3_bar < 0.10 THEN
    rPartialPress_NH3_bar := 0.10; (* Prevent numerical division by zero *)
END_IF;

(* --- 3.2 Temkin-Pyzhev Equilibrium & Reaction Kinetics for Bed 1 --- *)
(* Arrhenius Forward & Reverse Reaction Constants *)
rArrhenius_k1 := rKinetic_k10 * EXP(-rKinetic_E1 / (rConst_GasConst_R * (rVotedBed1Temp_DegC + 273.15)));
rArrhenius_k2 := rKinetic_k20 * EXP(-rKinetic_E2 / (rConst_GasConst_R * (rVotedBed1Temp_DegC + 273.15)));

(* Reaction Quotient & Net Intrinsic Volumetric Rate *)
rReactionQuotient := (rPartialPress_H2_bar * rPartialPress_H2_bar * rPartialPress_H2_bar) /
                     (rPartialPress_NH3_bar * rPartialPress_NH3_bar);
IF rReactionQuotient > 1.0E-06 THEN
    rBed1_Rate_kmols := (rArrhenius_k1 * rPartialPress_N2_bar * SQRT(rReactionQuotient) -
                         rArrhenius_k2 / SQRT(rReactionQuotient)) * rBed1_CatalystVolume_m3 * 0.001;
ELSE
    rBed1_Rate_kmols := 0.0;
END_IF;

IF rBed1_Rate_kmols < 0.0 THEN
    rBed1_Rate_kmols := 0.0;
END_IF;

(* Exothermic Heat Liberation [MW] & Adiabatic Exotherm Rise [deg C] *)
rBed1_Exotherm_C := (rBed1_Rate_kmols * 1000.0 * ABS(rConst_DeltaH_Rxn_Jmol)) /
                    (rLoopCirculationFlow_Nm3h * (1.0 / rConst_StandardMolarVol) * 1000.0 * 29.1);
IF rBed1_Exotherm_C > 140.0 THEN
    rBed1_Exotherm_C := 140.0;
END_IF;

(* --- 3.3 Bed 2, Bed 3, Bed 4 Inter-Bed Quench & Cascaded Kinetics --- *)
(* Bed 2 inlet after Quench 1 mixing *)
rArrhenius_k1 := rKinetic_k10 * EXP(-rKinetic_E1 / (rConst_GasConst_R * (rVotedBed2Temp_DegC + 273.15)));
rArrhenius_k2 := rKinetic_k20 * EXP(-rKinetic_E2 / (rConst_GasConst_R * (rVotedBed2Temp_DegC + 273.15)));
rBed2_Rate_kmols := (rArrhenius_k1 * rPartialPress_N2_bar * SQRT(rReactionQuotient) -
                     rArrhenius_k2 / SQRT(rReactionQuotient)) * rBed2_CatalystVolume_m3 * 0.00085;
IF rBed2_Rate_kmols < 0.0 THEN rBed2_Rate_kmols := 0.0; END_IF;

(* Bed 3 inlet after Quench 2 mixing *)
rArrhenius_k1 := rKinetic_k10 * EXP(-rKinetic_E1 / (rConst_GasConst_R * (rVotedBed3Temp_DegC + 273.15)));
rArrhenius_k2 := rKinetic_k20 * EXP(-rKinetic_E2 / (rConst_GasConst_R * (rVotedBed3Temp_DegC + 273.15)));
rBed3_Rate_kmols := (rArrhenius_k1 * rPartialPress_N2_bar * SQRT(rReactionQuotient) -
                     rArrhenius_k2 / SQRT(rReactionQuotient)) * rBed3_CatalystVolume_m3 * 0.00072;
IF rBed3_Rate_kmols < 0.0 THEN rBed3_Rate_kmols := 0.0; END_IF;

(* Bed 4 bottom layer kinetics *)
rArrhenius_k1 := rKinetic_k10 * EXP(-rKinetic_E1 / (rConst_GasConst_R * (rVotedBed4Temp_DegC + 273.15)));
rArrhenius_k2 := rKinetic_k20 * EXP(-rKinetic_E2 / (rConst_GasConst_R * (rVotedBed4Temp_DegC + 273.15)));
rBed4_Rate_kmols := (rArrhenius_k1 * rPartialPress_N2_bar * SQRT(rReactionQuotient) -
                     rArrhenius_k2 / SQRT(rReactionQuotient)) * rBed4_CatalystVolume_m3 * 0.00061;
IF rBed4_Rate_kmols < 0.0 THEN rBed4_Rate_kmols := 0.0; END_IF;

(* Total Thermochemical Synthesis Heat Release [MW] *)
rReactionHeatGenerated_MW := (rBed1_Rate_kmols + rBed2_Rate_kmols + rBed3_Rate_kmols + rBed4_Rate_kmols) *
                             ABS(rConst_DeltaH_Rxn_Jmol) * 0.001;

(* Total Anhydrous Liquid Ammonia Production Rate [kg/s] & [t/day] *)
rLiquidAmmoniaYield_kgs := (rBed1_Rate_kmols + rBed2_Rate_kmols + rBed3_Rate_kmols + rBed4_Rate_kmols) *
                           rConst_MolarMass_NH3;
IF rLiquidAmmoniaYield_kgs > 45.0 THEN
    rLiquidAmmoniaYield_kgs := 45.0;
END_IF;
rCurrentAmmoniaDailyRate_tday := (rLiquidAmmoniaYield_kgs * 86400.0) / 1000.0;

(* Converter Single-Pass Nitrogen Conversion [%] *)
IF (aState_x[8] > 0.01) AND (rLoopCirculationFlow_Nm3h > 1000.0) THEN
    rSinglePassConversion_pct := ((rBed1_Rate_kmols + rBed2_Rate_kmols + rBed3_Rate_kmols + rBed4_Rate_kmols) * 0.50 * 22.414 * 3600.0) /
                                 (rLoopCirculationFlow_Nm3h * aState_x[8]) * 100.0;
ELSE
    rSinglePassConversion_pct := 0.0;
END_IF;

(* Total Inerts Accumulation in Recycle Loop [%] *)
rTotalInertsConcentration_pct := (rLoopInerts_Methane_molmol + rLoopInerts_Argon_molmol) * 100.0;

(* --- 3.4 Syngas Compressor Aerodynamic Head & Anti-Surge Control --- *)
(* Polytropic Compression Head & Dynamic Surge Limit Line *)
IF rCompressorSuctionPress_bar > 1.0 THEN
    rComp_PressureRatio := rVotedLoopPressure_bar / rCompressorSuctionPress_bar;
ELSE
    rComp_PressureRatio := 1.0;
END_IF;

(* Polytropic Head [kJ/kg] for Syngas Molecular Weight ~8.5 g/mol *)
rComp_PolytropicHead_kJkg := (0.95 * rConst_GasConst_R * (45.0 + 273.15) / 0.0085) *
                             (1.39 / (1.39 - 1.0)) * 0.76 *
                             (EXP(((1.39 - 1.0) / 1.39) * LN(rComp_PressureRatio)) - 1.0) * 0.001;

(* Dynamic Surge Limit Line Orifice dP Limit [mbar] *)
rComp_SurgeDpLimit_mbar := 0.0042 * (rVotedCompressorSpeed_rpm * rVotedCompressorSpeed_rpm) / 10000.0 +
                           0.45 * rComp_PressureRatio * 10.0;

(* Instantaneous Compressor Aerodynamic Surge Margin [%] *)
IF rComp_SurgeDpLimit_mbar > 5.0 THEN
    rCalculatedSurgeMargin_pct := ((rVotedSurgeDiffPress_mbar - rComp_SurgeDpLimit_mbar) / rComp_SurgeDpLimit_mbar) * 100.0;
ELSE
    rCalculatedSurgeMargin_pct := 25.0;
END_IF;

(* Fast Derivative Surge Kick Detector *)
rSurgeDerivativeRate := (rCalculatedSurgeMargin_pct - rPrevSurgeMargin_pct) / rCycleTime_sec;
rPrevSurgeMargin_pct := rCalculatedSurgeMargin_pct;

IF (rCalculatedSurgeMargin_pct < 10.0) OR (rSurgeDerivativeRate < -4.0) THEN
    rSurgeKickCommand_pct := 35.0 + (10.0 - rCalculatedSurgeMargin_pct) * 2.5;
    IF rSurgeKickCommand_pct > 100.0 THEN rSurgeKickCommand_pct := 100.0; END_IF;
    bAntiSurgeActive := TRUE;
ELSE
    rSurgeKickCommand_pct := 0.0;
    bAntiSurgeActive := (rAntiSurgePidOutput_pct > 2.0);
END_IF;

(* Anti-Surge PI Closed-Loop Control with Anti-Windup *)
rComp_SurgeDev_pct := 12.0 - rCalculatedSurgeMargin_pct; (* Setpoint = 12% surge margin bias *)
IF rComp_SurgeDev_pct > 0.0 THEN
    rAntiSurgeIntegral := rAntiSurgeIntegral + (rComp_SurgeDev_pct * 1.8 * rCycleTime_sec);
    IF rAntiSurgeIntegral > 100.0 THEN rAntiSurgeIntegral := 100.0; END_IF;
ELSE
    rAntiSurgeIntegral := rAntiSurgeIntegral - (ABS(rComp_SurgeDev_pct) * 0.5 * rCycleTime_sec);
    IF rAntiSurgeIntegral < 0.0 THEN rAntiSurgeIntegral := 0.0; END_IF;
END_IF;

rAntiSurgePidOutput_pct := (rComp_SurgeDev_pct * 2.5) + rAntiSurgeIntegral + rSurgeKickCommand_pct;
IF rAntiSurgePidOutput_pct > 100.0 THEN rAntiSurgePidOutput_pct := 100.0; END_IF;
IF rAntiSurgePidOutput_pct < 0.0 THEN rAntiSurgePidOutput_pct := 0.0; END_IF;
""")

    # 8. Logic: Phase 4: Receding-Horizon MPC Optimization Solver
    parts.append("""(* ========================================================================================= *)
(* === PHASE 4: RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) OPTIMIZATION SOLVER        === *)
(* ========================================================================================= *)
(* Multi-variable quadratic cost optimization over 16 plant states and 8 actuator channels.  *)
(* Computes constrained projected gradient descent steps with rate-of-change clamping.      *)

(* Setup Target Reference Trajectory Vector aState_x_target *)
aState_x_target[1]  := rTargetBed1InletTemp_DegC;
aState_x_target[2]  := 410.0;                   (* Bed 2 inlet setpoint [deg C] *)
aState_x_target[3]  := 400.0;                   (* Bed 3 inlet setpoint [deg C] *)
aState_x_target[4]  := 395.0;                   (* Bed 4 inlet setpoint [deg C] *)
aState_x_target[5]  := rTargetLoopPressure_bar;
aState_x_target[6]  := 0.185;                   (* Target NH3 mole fraction [mol/mol] *)
aState_x_target[7]  := 0.7425;                  (* Nominal H2 fraction *)
aState_x_target[8]  := 0.2475;                  (* Nominal N2 fraction *)
aState_x_target[9]  := 0.0950;                  (* Target inerts < 10 vol% *)
aState_x_target[10] := 34.722;                  (* 3,000 MTPD NH3 yield [kg/s] *)
aState_x_target[11] := 10500.0;                 (* Nominal turbine compressor speed [rpm] *)
aState_x_target[12] := 15.0;                    (* Operating surge margin [%] *)
aState_x_target[13] := -25.0;                   (* Ammonia chiller flash temp [deg C] *)
aState_x_target[14] := 45.0;                    (* Suction drum level [%] *)
aState_x_target[15] := 18500.0;                 (* Purge feed to Cryo HRU [Nm3/h] *)
aState_x_target[16] := 32.5;                    (* Steam turbine load [MW] *)

(* Setup Quadratic Penalty Weights Q, R, P, S *)
aWeight_Q[1]  := 2.50;  aWeight_Q[2]  := 2.80;  aWeight_Q[3]  := 2.80;  aWeight_Q[4]  := 3.20;
aWeight_Q[5]  := 5.00;  aWeight_Q[6]  := 8.50;  aWeight_Q[7]  := 4.00;  aWeight_Q[8]  := 4.00;
aWeight_Q[9]  := 6.00;  aWeight_Q[10] := 12.00; aWeight_Q[11] := 0.85;  aWeight_Q[12] := 7.50;
aWeight_Q[13] := 3.50;  aWeight_Q[14] := 1.50;  aWeight_Q[15] := 2.00;  aWeight_Q[16] := 0.50;

aWeight_R[1]  := 0.25;  aWeight_R[2]  := 0.25;  aWeight_R[3]  := 0.25;  aWeight_R[4]  := 0.05;
aWeight_R[5]  := 1.20;  aWeight_R[6]  := 0.80;  aWeight_R[7]  := 0.45;  aWeight_R[8]  := 0.35;

aWeight_S_slew[1] := 1.50; aWeight_S_slew[2] := 1.50; aWeight_S_slew[3] := 1.50; aWeight_S_slew[4] := 0.80;
aWeight_S_slew[5] := 3.00; aWeight_S_slew[6] := 1.20; aWeight_S_slew[7] := 1.80; aWeight_S_slew[8] := 1.00;

(* Calculate State Prediction Tracking Errors *)
FOR iStateIdx := 1 TO 16 DO
    aState_x_err[iStateIdx] := aState_x_next[iStateIdx] - aState_x_target[iStateIdx];
END_FOR;

(* Projected Gradient Descent Solver (8 Inner Iterations) *)
FOR iMpcIter := 1 TO 8 DO
    (* Compute Cost Gradient w.r.t each Control Actuator u[j] *)
    FOR jInputIdx := 1 TO 8 DO
        aGrad_J[jInputIdx] := aWeight_R[jInputIdx] * aControl_u[jInputIdx] +
                              aWeight_S_slew[jInputIdx] * (aControl_u[jInputIdx] - aControl_u_prev[jInputIdx]);
        FOR iStateIdx := 1 TO 16 DO
            aGrad_J[jInputIdx] := aGrad_J[jInputIdx] +
                                  aMatrix_B[iStateIdx, jInputIdx] * aWeight_Q[iStateIdx] * aState_x_err[iStateIdx];
        END_FOR;
    END_FOR;

    (* Apply Projected Gradient Step: u = u - alpha * grad_J *)
    aControl_u[1] := aControl_u[1] - 0.0035 * aGrad_J[1]; (* Quench 1 *)
    aControl_u[2] := aControl_u[2] - 0.0035 * aGrad_J[2]; (* Quench 2 *)
    aControl_u[3] := aControl_u[3] - 0.0035 * aGrad_J[3]; (* Quench 3 *)
    aControl_u[4] := aControl_u[4] - 0.0085 * aGrad_J[4]; (* Turbine speed governor *)
    aControl_u[5] := aControl_u[5] - 0.0025 * aGrad_J[5]; (* Anti-surge valve *)
    aControl_u[6] := aControl_u[6] - 0.0040 * aGrad_J[6]; (* Purge bleed valve *)
    aControl_u[7] := aControl_u[7] - 0.0050 * aGrad_J[7]; (* Makeup trim valve *)
    aControl_u[8] := aControl_u[8] - 0.0045 * aGrad_J[8]; (* Chiller duty *)

    (* Actuator Hard Saturation Bounds Projection *)
    IF aControl_u[1] > 100.0 THEN aControl_u[1] := 100.0; END_IF;
    IF aControl_u[1] < 0.0   THEN aControl_u[1] := 0.0;   END_IF;
    IF aControl_u[2] > 100.0 THEN aControl_u[2] := 100.0; END_IF;
    IF aControl_u[2] < 0.0   THEN aControl_u[2] := 0.0;   END_IF;
    IF aControl_u[3] > 100.0 THEN aControl_u[3] := 100.0; END_IF;
    IF aControl_u[3] < 0.0   THEN aControl_u[3] := 0.0;   END_IF;

    IF aControl_u[4] > 11500.0 THEN aControl_u[4] := 11500.0; END_IF;
    IF aControl_u[4] < 4500.0  THEN aControl_u[4] := 4500.0;  END_IF;

    IF aControl_u[5] > 100.0 THEN aControl_u[5] := 100.0; END_IF;
    IF aControl_u[5] < 0.0   THEN aControl_u[5] := 0.0;   END_IF;

    IF aControl_u[6] > 100.0 THEN aControl_u[6] := 100.0; END_IF;
    IF aControl_u[6] < 0.0   THEN aControl_u[6] := 0.0;   END_IF;

    IF aControl_u[7] > 20.0  THEN aControl_u[7] := 20.0;  END_IF;
    IF aControl_u[7] < -20.0 THEN aControl_u[7] := -20.0; END_IF;

    IF aControl_u[8] > 100.0 THEN aControl_u[8] := 100.0; END_IF;
    IF aControl_u[8] < 0.0   THEN aControl_u[8] := 0.0;   END_IF;
END_FOR;

(* Actuator Rate-of-Change Slew Limiting per PLC Cycle *)
FOR jInputIdx := 1 TO 8 DO
    aControl_u_delta[jInputIdx] := aControl_u[jInputIdx] - aControl_u_prev[jInputIdx];
END_FOR;

(* Clamping individual slew rates *)
IF ABS(aControl_u_delta[1]) > (2.5 * rCycleTime_sec) THEN
    IF aControl_u_delta[1] > 0.0 THEN aControl_u[1] := aControl_u_prev[1] + (2.5 * rCycleTime_sec);
    ELSE aControl_u[1] := aControl_u_prev[1] - (2.5 * rCycleTime_sec); END_IF;
END_IF;
IF ABS(aControl_u_delta[2]) > (2.5 * rCycleTime_sec) THEN
    IF aControl_u_delta[2] > 0.0 THEN aControl_u[2] := aControl_u_prev[2] + (2.5 * rCycleTime_sec);
    ELSE aControl_u[2] := aControl_u_prev[2] - (2.5 * rCycleTime_sec); END_IF;
END_IF;
IF ABS(aControl_u_delta[3]) > (2.5 * rCycleTime_sec) THEN
    IF aControl_u_delta[3] > 0.0 THEN aControl_u[3] := aControl_u_prev[3] + (2.5 * rCycleTime_sec);
    ELSE aControl_u[3] := aControl_u_prev[3] - (2.5 * rCycleTime_sec); END_IF;
END_IF;
IF ABS(aControl_u_delta[4]) > (50.0 * rCycleTime_sec) THEN
    IF aControl_u_delta[4] > 0.0 THEN aControl_u[4] := aControl_u_prev[4] + (50.0 * rCycleTime_sec);
    ELSE aControl_u[4] := aControl_u_prev[4] - (50.0 * rCycleTime_sec); END_IF;
END_IF;

(* Store Previous Controls for Slew Penalty on Next Scan *)
FOR jInputIdx := 1 TO 8 DO
    aControl_u_prev[jInputIdx] := aControl_u[jInputIdx];
END_FOR;
""")

    # 9. Logic: Phase 5: Closed-Loop Stoichiometry Trim & Cryo Purge Balance
    parts.append("""(* ========================================================================================= *)
(* === PHASE 5: CLOSED-LOOP STOICHIOMETRY TRIM & CRYOGENIC PURGE BALANCE                    === *)
(* ========================================================================================= *)
(* Precision H2:N2 ratio feedback with mass spectrometer feedforward and Cryogenic HRU loop  *)

(* --- 5.1 Stoichiometry Ratio PID Controller --- *)
rRatioError := rTargetH2_N2_Ratio - rVotedH2_N2_Ratio;

(* Trapezoidal Anti-Windup Integration *)
IF (rRatioError > -0.25) AND (rRatioError < 0.25) THEN
    rRatioIntegral := rRatioIntegral + (rRatioError * 0.085 * rCycleTime_sec);
    IF rRatioIntegral > 15.0 THEN rRatioIntegral := 15.0; END_IF;
    IF rRatioIntegral < -15.0 THEN rRatioIntegral := -15.0; END_IF;
END_IF;

rRatioDerivative := (rRatioError - rRatioPrevError) / rCycleTime_sec;
rRatioPrevError := rRatioError;

(* Fine Makeup Gas H2 Trim Output [%] *)
rRatioTrimOutput_pct := (rRatioError * 18.5) + rRatioIntegral + (rRatioDerivative * 1.25) +
                        ((rMakeupSyngasH2_molmol - 0.750) * -12.0); (* Feedforward analyzer compensation *)

IF rRatioTrimOutput_pct > 20.0 THEN rRatioTrimOutput_pct := 20.0; END_IF;
IF rRatioTrimOutput_pct < -20.0 THEN rRatioTrimOutput_pct := -20.0; END_IF;
rMakeupH2_TrimValve_Cmd_pct := rRatioTrimOutput_pct;

(* --- 5.2 Cryogenic Purge Gas Recovery Unit Mass Balance --- *)
IF bCryoHruOnlinePermissive AND (rPurgeGasFlow_Nm3h > 5000.0) THEN
    bCryoHruActive := TRUE;
    (* 92% pure H2 return stream back to compressor suction *)
    rCryoHruH2ReturnRate_Nm3h := rPurgeGasFlow_Nm3h * (aState_x[7] * 0.98) * rCryoHruSeparationFactor;
ELSE
    bCryoHruActive := FALSE;
    rCryoHruH2ReturnRate_Nm3h := 0.0;
END_IF;

(* --- 5.3 Ammonia Condensation & Letdown Vessel Level Controller --- *)
IF rColdCatchDrumLevel_pct > 55.0 THEN
    rLetdownValveInternal_pct := 45.0 + (rColdCatchDrumLevel_pct - 50.0) * 1.8;
ELSIF rColdCatchDrumLevel_pct < 45.0 THEN
    rLetdownValveInternal_pct := 45.0 - (50.0 - rColdCatchDrumLevel_pct) * 1.8;
ELSE
    rLetdownValveInternal_pct := 45.0;
END_IF;
IF rLetdownValveInternal_pct > 100.0 THEN rLetdownValveInternal_pct := 100.0; END_IF;
IF rLetdownValveInternal_pct < 5.0 THEN rLetdownValveInternal_pct := 5.0; END_IF;
rLiquidAmmoniaDrawValve_pct := rLetdownValveInternal_pct;
""")

    # 10. Logic: Phase 6: 12-Stage Operational Finite State Machine
    parts.append("""(* ========================================================================================= *)
(* === PHASE 6: 12-STAGE OPERATIONAL FINITE STATE MACHINE (FSM)                            === *)
(* ========================================================================================= *)
(* Deterministic life-cycle supervision from nitrogen purge through 3,000 MTPD production   *)
(* to controlled shutdown and SIL-3 emergency flare depressurization.                       *)

(* Master Run Permissive Check *)
IF NOT bMasterEnable OR NOT bEmergencyStop THEN
    iState := 120; (* Force direct transition to Emergency Flare Depressurization *)
END_IF;

(* Advance State Elapsed Timer *)
IF iState = iPreviousState THEN
    rStateTimer_sec := rStateTimer_sec + rCycleTime_sec;
ELSE
    rStateTimer_sec := 0.0;
    iPreviousState := iState;
END_IF;

CASE iState OF

    10: (* STATE_01_NITROGEN_PURGE_REDUCTION *)
        bSystemRunning := TRUE;
        bSystemReady := FALSE;
        bMpcControllerActive := FALSE;
        rStartupHeaterThyristor_pct := 0.0;
        rQuenchValve1_Cmd_pct := 0.0;
        rQuenchValve2_Cmd_pct := 0.0;
        rQuenchValve3_Cmd_pct := 0.0;
        rTurbineGovernorDemand_rpm := 600.0; (* Turning gear barring speed *)
        rAntiSurgeValve_Cmd_pct := 100.0;    (* Full bypass *)
        rMakeupSyngasValve_Cmd_pct := 0.0;
        rPurgeBleedValve_Cmd_pct := 15.0;    (* Purging inert sweep *)
        rChillerRefrigerationDemand_pct := 0.0;

        (* Transition: Loop sweep complete, O2 analyzer < 0.1%, ready for compressor roll *)
        IF bCompressorPermissive AND (rStateTimer_sec >= 120.0) THEN
            iState := 20;
        END_IF;

    20: (* STATE_02_COMPRESSOR_SLOW_ROLL_WARMUP *)
        bSystemRunning := TRUE;
        bSystemReady := FALSE;
        bMpcControllerActive := FALSE;
        rStartupHeaterThyristor_pct := 0.0;
        rQuenchValve1_Cmd_pct := 0.0;
        rQuenchValve2_Cmd_pct := 0.0;
        rQuenchValve3_Cmd_pct := 0.0;
        rAntiSurgeValve_Cmd_pct := 100.0;
        rMakeupSyngasValve_Cmd_pct := 0.0;
        rPurgeBleedValve_Cmd_pct := 5.0;
        rChillerRefrigerationDemand_pct := 0.0;

        (* Turbine slow roll & thermal soaking: ramp from 600 rpm to minimum governor 4,500 rpm *)
        IF rTurbineSteamPermissive AND (rStateTimer_sec >= 300.0) THEN
            rTurbineGovernorDemand_rpm := 4500.0;
            IF (rVotedCompressorSpeed_rpm >= 4400.0) AND (rTurbineVibration_mms < 4.5) THEN
                iState := 30;
            END_IF;
        ELSE
            rTurbineGovernorDemand_rpm := 1200.0;
        END_IF;

    30: (* STATE_03_LOOP_PRESSURIZATION_150BAR *)
        bSystemRunning := TRUE;
        bSystemReady := FALSE;
        bMpcControllerActive := FALSE;
        rStartupHeaterThyristor_pct := 0.0;
        rQuenchValve1_Cmd_pct := 0.0;
        rQuenchValve2_Cmd_pct := 0.0;
        rQuenchValve3_Cmd_pct := 0.0;
        rTurbineGovernorDemand_rpm := 6500.0;
        rAntiSurgeValve_Cmd_pct := 65.0;
        rPurgeBleedValve_Cmd_pct := 2.0;
        rChillerRefrigerationDemand_pct := 0.0;

        (* Staged pressurization via makeup syngas feed valve at 2.5 bar/min *)
        rMakeupSyngasValve_Cmd_pct := 25.0;
        IF rVotedLoopPressure_bar >= 150.0 THEN
            iState := 40;
        END_IF;

    40: (* STATE_04_ELECTRIC_STARTUP_HEATER_LIGHTOFF *)
        bSystemRunning := TRUE;
        bSystemReady := FALSE;
        bMpcControllerActive := FALSE;
        rQuenchValve1_Cmd_pct := 0.0;
        rQuenchValve2_Cmd_pct := 0.0;
        rQuenchValve3_Cmd_pct := 0.0;
        rTurbineGovernorDemand_rpm := 8000.0;
        rAntiSurgeValve_Cmd_pct := 40.0;
        rMakeupSyngasValve_Cmd_pct := 40.0;
        rPurgeBleedValve_Cmd_pct := 5.0;
        rChillerRefrigerationDemand_pct := 20.0;

        (* Energize electric preheater to achieve autothermal initiation at 380 C *)
        rStartupHeaterThyristor_pct := 85.0;
        IF rVotedBed1Temp_DegC >= 380.0 THEN
            bLightoffConfirmed := TRUE;
            iState := 50;
        END_IF;

    50: (* STATE_05_AUTOTHERMAL_LIGHTOFF_QUENCH_ACT *)
        bSystemRunning := TRUE;
        bSystemReady := TRUE;
        bMpcControllerActive := FALSE;
        bAutothermalReactionIgnited := TRUE;
        rTurbineGovernorDemand_rpm := 9500.0;
        rAntiSurgeValve_Cmd_pct := 15.0;
        rMakeupSyngasValve_Cmd_pct := 65.0;
        rPurgeBleedValve_Cmd_pct := 8.0;
        rChillerRefrigerationDemand_pct := 60.0;

        (* Ramp down electric startup heater as Haber-Bosch exotherm takes over *)
        rStartupHeaterThyristor_pct := 0.0;
        rQuenchValve1_Cmd_pct := 18.0;
        rQuenchValve2_Cmd_pct := 22.0;
        rQuenchValve3_Cmd_pct := 20.0;

        IF (rBed1_Exotherm_C > 45.0) AND (rVotedConverterEffluentNH3 > 0.12) THEN
            iState := 60;
        END_IF;

    60: (* STATE_06_STEADY_STATE_PRODUCTION_200BAR *)
        bSystemRunning := TRUE;
        bSystemReady := TRUE;
        bMpcControllerActive := TRUE;
        rStartupHeaterThyristor_pct := 0.0;

        (* Hand over actuator dispatches to Receding-Horizon MPC *)
        rQuenchValve1_Cmd_pct := aControl_u[1];
        rQuenchValve2_Cmd_pct := aControl_u[2];
        rQuenchValve3_Cmd_pct := aControl_u[3];
        rTurbineGovernorDemand_rpm := aControl_u[4];
        rAntiSurgeValve_Cmd_pct := rAntiSurgePidOutput_pct;
        rPurgeBleedValve_Cmd_pct := aControl_u[6];
        rChillerRefrigerationDemand_pct := aControl_u[8];
        rMakeupSyngasValve_Cmd_pct := 88.0;

        IF (rVotedLoopPressure_bar >= 195.0) AND (rCurrentAmmoniaDailyRate_tday >= 2600.0) THEN
            iState := 70;
        END_IF;

    70: (* STATE_07_STOICHIOMETRIC_RATIO_TRIMMING *)
        bSystemRunning := TRUE;
        bSystemReady := TRUE;
        bMpcControllerActive := TRUE;
        rStartupHeaterThyristor_pct := 0.0;

        rQuenchValve1_Cmd_pct := aControl_u[1];
        rQuenchValve2_Cmd_pct := aControl_u[2];
        rQuenchValve3_Cmd_pct := aControl_u[3];
        rTurbineGovernorDemand_rpm := aControl_u[4];
        rAntiSurgeValve_Cmd_pct := rAntiSurgePidOutput_pct;
        rPurgeBleedValve_Cmd_pct := aControl_u[6];
        rChillerRefrigerationDemand_pct := aControl_u[8];
        rMakeupSyngasValve_Cmd_pct := 94.0;

        IF (ABS(rVotedH2_N2_Ratio - 2.95) < 0.05) AND (rStateTimer_sec >= 180.0) THEN
            iState := 80;
        END_IF;

    80: (* STATE_08_CRYOGENIC_PURGE_RECOVERY_ONLINE *)
        bSystemRunning := TRUE;
        bSystemReady := TRUE;
        bMpcControllerActive := TRUE;
        rStartupHeaterThyristor_pct := 0.0;

        rQuenchValve1_Cmd_pct := aControl_u[1];
        rQuenchValve2_Cmd_pct := aControl_u[2];
        rQuenchValve3_Cmd_pct := aControl_u[3];
        rTurbineGovernorDemand_rpm := aControl_u[4];
        rAntiSurgeValve_Cmd_pct := rAntiSurgePidOutput_pct;
        rPurgeBleedValve_Cmd_pct := aControl_u[6];
        rChillerRefrigerationDemand_pct := aControl_u[8];
        rMakeupSyngasValve_Cmd_pct := 98.0;

        IF bCryoHruActive AND (rTotalInertsConcentration_pct < 10.5) THEN
            iState := 90;
        END_IF;

    90: (* STATE_09_CHILLER_REFRIGERATION_PACING *)
        bSystemRunning := TRUE;
        bSystemReady := TRUE;
        bMpcControllerActive := TRUE;
        rStartupHeaterThyristor_pct := 0.0;

        (* Full capacity baseload 3,000 MTPD ammonia production dispatch *)
        rQuenchValve1_Cmd_pct := aControl_u[1];
        rQuenchValve2_Cmd_pct := aControl_u[2];
        rQuenchValve3_Cmd_pct := aControl_u[3];
        rTurbineGovernorDemand_rpm := aControl_u[4];
        rAntiSurgeValve_Cmd_pct := rAntiSurgePidOutput_pct;
        rPurgeBleedValve_Cmd_pct := aControl_u[6];
        rChillerRefrigerationDemand_pct := aControl_u[8];
        rMakeupSyngasValve_Cmd_pct := 100.0;

        (* Normal state stays at 90 during baseload manufacture *)

    100: (* STATE_10_MAKEUP_RATE_TURNDOWN *)
        bSystemRunning := TRUE;
        bSystemReady := TRUE;
        bMpcControllerActive := TRUE;
        rStartupHeaterThyristor_pct := 0.0;

        (* Turn down to 65% minimum technical load (1,950 MTPD) *)
        rMakeupSyngasValve_Cmd_pct := 65.0;
        rTurbineGovernorDemand_rpm := 8200.0;
        rQuenchValve1_Cmd_pct := aControl_u[1] * 0.75;
        rQuenchValve2_Cmd_pct := aControl_u[2] * 0.75;
        rQuenchValve3_Cmd_pct := aControl_u[3] * 0.75;
        rAntiSurgeValve_Cmd_pct := rAntiSurgePidOutput_pct + 8.0; (* Added safety bias *)
        rPurgeBleedValve_Cmd_pct := 6.0;
        rChillerRefrigerationDemand_pct := 65.0;

    110: (* STATE_11_CONTROLLED_COOLDOWN_DEPRESSURIZE *)
        bSystemRunning := TRUE;
        bSystemReady := FALSE;
        bMpcControllerActive := FALSE;
        rStartupHeaterThyristor_pct := 0.0;
        rMakeupSyngasValve_Cmd_pct := 0.0; (* Isolate fresh syngas *)

        (* Controlled circulation cooldown (< 25 deg C/h) with anti-surge full recycle *)
        rTurbineGovernorDemand_rpm := 6000.0;
        rAntiSurgeValve_Cmd_pct := 80.0;
        rQuenchValve1_Cmd_pct := 100.0;
        rQuenchValve2_Cmd_pct := 100.0;
        rQuenchValve3_Cmd_pct := 100.0;
        rPurgeBleedValve_Cmd_pct := 35.0; (* Controlled depressurization *)
        rChillerRefrigerationDemand_pct := 0.0;

        IF (rVotedBed1Temp_DegC < 150.0) AND (rVotedLoopPressure_bar < 25.0) THEN
            iState := 10; (* Return to cold nitrogen purge *)
        END_IF;

    120: (* STATE_12_EMERGENCY_SIL3_DEPRESSURIZE_FLARE *)
        bSystemRunning := FALSE;
        bSystemReady := FALSE;
        bSystemTripped := TRUE;
        bMpcControllerActive := FALSE;
        bAutothermalReactionIgnited := FALSE;

        (* SIL-3 failsafe trip actuation: isolate feed, trip turbine, open flare blowdown *)
        rStartupHeaterThyristor_pct := 0.0;
        rMakeupSyngasValve_Cmd_pct := 0.0;
        rMakeupH2_TrimValve_Cmd_pct := 0.0;
        rQuenchValve1_Cmd_pct := 0.0;
        rQuenchValve2_Cmd_pct := 0.0;
        rQuenchValve3_Cmd_pct := 0.0;
        rTurbineGovernorDemand_rpm := 0.0;  (* Turbine quick trip closed *)
        rAntiSurgeValve_Cmd_pct := 100.0;   (* Full open *)
        rPurgeBleedValve_Cmd_pct := 100.0;  (* Fast depressurization to flare *)
        rChillerRefrigerationDemand_pct := 0.0;
        rLiquidAmmoniaDrawValve_pct := 0.0; (* Isolate liquid storage *)

        (* Latch until master unlatch and reset *)
        IF bResetFaults AND bMasterEnable AND bEmergencyStop THEN
            bSystemTripped := FALSE;
            iState := 10;
        END_IF;

END_CASE;
""")

    # 11. Logic: Phase 7: ISA-18.2 Alarms & Bit-Packed Telemetry
    parts.append("""(* ========================================================================================= *)
(* === PHASE 7: ISA-18.2 ALARMS & BIT-PACKED TELEMETRY REGISTERS                           === *)
(* ========================================================================================= *)
(* Real-time deadband monitoring, trip condition evaluation and diagnostic DWORD packing.    *)

(* --- 7.1 Catastrophic Trips (SIL-3 Priority 1: dwAlarmWord1) --- *)
(* Catalyst runaway sintering limit > 520.0 deg C *)
bCatalystRunawayTrip_Active := (rVotedBed1Temp_DegC > 520.0) OR (rVotedBed2Temp_DegC > 520.0) OR
                               (rVotedBed3Temp_DegC > 520.0) OR (rVotedBed4Temp_DegC > 520.0);
IF bCatalystRunawayTrip_Active THEN
    bCatalystThermalRunawayWarning := TRUE;
    iState := 120;
ELSE
    bCatalystThermalRunawayWarning := (rVotedBed1Temp_DegC > 505.0) OR (rVotedBed2Temp_DegC > 490.0);
END_IF;

(* Loop overpressure HH > 230.0 bar *)
bOverpressureTrip_Active := (rVotedLoopPressure_bar > 230.0);
IF bOverpressureTrip_Active THEN
    iState := 120;
END_IF;

(* Compressor surge margin critical trip < 4.0 % *)
bCompressorSurgeTrip_Active := (rCalculatedSurgeMargin_pct < 4.0);
IF bCompressorSurgeTrip_Active THEN
    iState := 120;
END_IF;

(* Turbine axial displacement trip > +0.50 mm or < -0.50 mm *)
bThrustDisplacementTrip_Active := (rThrustBearingDisplace_mm > 0.50) OR (rThrustBearingDisplace_mm < -0.50);
IF bThrustDisplacementTrip_Active THEN
    iState := 120;
END_IF;

(* Turbine radial vibration trip > 18.0 mm/s *)
bVibrationTrip_Active := (rTurbineVibration_mms > 18.0);
IF bVibrationTrip_Active THEN
    iState := 120;
END_IF;

(* Suction KO drum level high-high > 85.0 % *)
bSuctionDrumHighLevelTrip_Active := (rSuctionDrumLevel_pct > 85.0);
IF bSuctionDrumHighLevelTrip_Active THEN
    iState := 120;
END_IF;

(* Pack dwAlarmWord1 *)
dwAlarmWord1 := 16#0000_0000;
IF NOT bEmergencyStop THEN dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0001; END_IF;
IF rVotedBed1Temp_DegC > 520.0 THEN dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0002; END_IF;
IF rVotedBed2Temp_DegC > 520.0 THEN dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0004; END_IF;
IF rVotedBed3Temp_DegC > 520.0 THEN dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0008; END_IF;
IF rVotedBed4Temp_DegC > 520.0 THEN dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0010; END_IF;
IF bOverpressureTrip_Active    THEN dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0020; END_IF;
IF bCompressorSurgeTrip_Active THEN dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0040; END_IF;
IF bThrustDisplacementTrip_Active THEN dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0080; END_IF;
IF bVibrationTrip_Active       THEN dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0100; END_IF;
IF bSuctionDrumHighLevelTrip_Active THEN dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0200; END_IF;
IF rLubeOilPressure_bar < 1.8  THEN dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0400; END_IF;

(* --- 7.2 Process & Stoichiometric Trips (Priority 2: dwAlarmWord2) --- *)
dwAlarmWord2 := 16#0000_0000;
IF rVotedH2_N2_Ratio < 2.50 THEN dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0001; END_IF;
IF rVotedH2_N2_Ratio > 3.50 THEN dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0002; END_IF;
IF (rVotedBed1Temp_DegC < 340.0) AND (iState >= 60) THEN dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0004; END_IF;
IF rConverterShell_Temp_DegC > 280.0 THEN dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0008; END_IF;
IF rConverterDiffPress_bar > 8.5 THEN dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0010; END_IF;
IF rTotalInertsConcentration_pct > 13.5 THEN dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0020; END_IF;
IF rStartupHeater_Temp_DegC > 580.0 THEN dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0040; END_IF;

(* --- 7.3 Diagnostic & Sensor Degradation Warnings (Priority 3: dwWarningWord) --- *)
dwWarningWord := 16#0000_0000;
IF bBed1Temp_Degraded THEN dwWarningWord := dwWarningWord OR 16#0000_0001; END_IF;
IF bBed2Temp_Degraded THEN dwWarningWord := dwWarningWord OR 16#0000_0002; END_IF;
IF bBed3Temp_Degraded THEN dwWarningWord := dwWarningWord OR 16#0000_0004; END_IF;
IF bBed4Temp_Degraded THEN dwWarningWord := dwWarningWord OR 16#0000_0008; END_IF;
IF bLoopPress_Degraded THEN dwWarningWord := dwWarningWord OR 16#0000_0010; END_IF;
IF bCompSpeed_Degraded THEN dwWarningWord := dwWarningWord OR 16#0000_0020; END_IF;
IF bSurgeDiff_Degraded THEN dwWarningWord := dwWarningWord OR 16#0000_0040; END_IF;
IF bRatio_Degraded     THEN dwWarningWord := dwWarningWord OR 16#0000_0080; END_IF;
IF bAntiSurgeActive    THEN dwWarningWord := dwWarningWord OR 16#0000_0100; END_IF;
IF rTotalInertsConcentration_pct > 10.5 THEN dwWarningWord := dwWarningWord OR 16#0000_0200; END_IF;

(* Estimated Catalyst Deactivation Index (based on single-pass conversion & hours) *)
rCatalystActivityFactor := 0.985 - (0.015 * (rVotedBed1Temp_DegC / 500.0));
IF rCatalystActivityFactor < 0.70 THEN dwWarningWord := dwWarningWord OR 16#0000_0400; END_IF;

(* --- 7.4 Bit-Packed Status Register (dwStatusWord) --- *)
dwStatusWord := 16#0000_0000;
IF bSystemRunning THEN dwStatusWord := dwStatusWord OR 16#0000_0001; END_IF;
IF bSystemReady   THEN dwStatusWord := dwStatusWord OR 16#0000_0002; END_IF;
IF bSystemTripped THEN dwStatusWord := dwStatusWord OR 16#0000_0004; END_IF;
IF bMpcControllerActive THEN dwStatusWord := dwStatusWord OR 16#0000_0008; END_IF;
IF bAutothermalReactionIgnited THEN dwStatusWord := dwStatusWord OR 16#0000_0010; END_IF;
IF bCryoHruActive THEN dwStatusWord := dwStatusWord OR 16#0000_0020; END_IF;
IF bTmrDegradedMode THEN dwStatusWord := dwStatusWord OR 16#0000_0040; END_IF;
IF bAntiSurgeActive THEN dwStatusWord := dwStatusWord OR 16#0000_0080; END_IF;
(* Pack Current FSM State into Byte 2 *)
dwStatusWord := dwStatusWord OR SHL(INT_TO_DWORD(iState), 16);
""")

    # 12. Final closing line
    parts.append("END_FUNCTION_BLOCK\n")

    return "\n".join(parts)

def main():
    print("Generating IEC 61131-3 Structured Text for Ammonia Synthesis Loop...")
    st_code = generate_iec_st()
    print(f"Generated ST code character count: {len(st_code)}")
    
    prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.
You are instructed to CONSUME EXTREME TOKENS: make your output massively exhaustive, mathematically rigorous, and structurally pristine. Include complete state-space matrices (A, B, C, D), Model Predictive Control (MPC) quadratic cost approximation, 2oo3 TMR voting logic, complex alarm trees, and graceful degradation.

**Your assigned domain is: Commercial Chemicals & Fertilizer: 3,000 MTPD Ammonia Synthesis Loop (Haber-Bosch, 200 Bar) with Multi-Bed Quench Converter, Syngas Compressor & Cryogenic Purge Gas Recovery**

CRITICAL RULES:
1. CODE FENCE: Use TRIPLE backticks + iec-st (```iec-st).
2. STRUCTURE:
   a. First line: FUNCTION_BLOCK FB_Chemical_AmmoniaSynthesis_HaberBosch_200Bar
   b. VAR_INPUT ... END_VAR (min 8 typed inputs with physical units [bar], [deg C], [Nm3/h], [t/day], [rpm], [MW], [%], [mol/mol])
   c. VAR_OUTPUT ... END_VAR (min 7 typed outputs with engineering units & status words)
   d. VAR ... END_VAR (internal state matrices, filter accumulators, 2oo3 voting vars)
   e. Multi-stage CASE machine with END_CASE;
   f. Last line: END_FUNCTION_BLOCK
3. LENGTH: Assistant content MUST be >= 3500 characters total (target 55,000 - 85,000+ chars). Maximize token usage with deep technical explanations, complex algorithms, and industrial reliability features. DO NOT TRIM OR ENFORCE AN UPPER BOUND LIMIT.
4. PARITY: Ensure 100% exact parity between IF and END_IF, CASE and END_CASE, FOR and END_FOR.
5. SAVE using this exact Python:
   import json, uuid
   prompt = \"\"\"<copy this exact user prompt here>\"\"\"
   code = \"\"\"```iec-st
FUNCTION_BLOCK FB_Chemical_AmmoniaSynthesis_HaberBosch_200Bar
//...
END_FUNCTION_BLOCK
```\"\"\"
   record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
   with open("data/swarm_raw/agent_5f1902ab.json", "w", encoding="utf-8") as f:
       json.dump(record, f, ensure_ascii=False)
6. REPLY with: EVOLUTION COMPLETE: Commercial Chemicals & Fertilizer: 3,000 MTPD Ammonia Synthesis Loop (Haber-Bosch, 200 Bar) with Multi-Bed Quench Converter, Syngas Compressor & Cryogenic Purge Gas Recovery"""

    assistant_content = f"```iec-st\n{st_code}```"
    print(f"Total assistant content characters: {len(assistant_content)}")
    
    record = {
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": assistant_content}
        ]
    }
    
    target_path = "data/swarm_raw/agent_5f1902ab.json"
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    with open(target_path, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    print(f"Successfully saved dataset to {target_path}")

if __name__ == "__main__":
    main()
