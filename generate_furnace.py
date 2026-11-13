import sys
import os
import json
import uuid

def generate_iec_st():
    parts = []
    
    # Header
    parts.append("""FUNCTION_BLOCK FB_Petrochem_Ethylene_PyrolysisFurnace_TLE
(*
========================================================================================================================
  LUMINA ADVANCED CYBER-PHYSICAL SYSTEMS & INDUSTRIAL PROCESS AUTOMATION ARCHITECTURE
  TIER-1 PETROCHEMICALS & OLEFINS SECTOR REFERENCE IMPLEMENTATION — SYNTHETIC BENCHMARK V7
  
  SYSTEM DESIGNATION: 150,000 Metric Tons/Year Ethylene Thermal Pyrolysis Cracking Furnace & TLE Quenching
  FUNCTION BLOCK:    FB_Petrochem_Ethylene_PyrolysisFurnace_TLE
  TARGET HARDWARE:   Safety-Critical High-Performance PLC / DCS (Cycle Task: 20 ms)
  IEC 61131-3 STANDARD: Third Edition (Strict Deterministic Structured Text)
========================================================================================================================

  PROCESS ENGINEERING & CYBER-PHYSICAL HIGHLIGHTS:
  ------------------------------------------------
  1. 8-PASS RADIANT COIL GEOMETRY & COT BALANCING:
     - 8 independent radiant serpentine tube passes suspended in radiant firebox.
     - Endothermic ethane/naphtha pyrolysis reactions (Delta H_rxn = +137 kJ/mol for ethane dehydrogenation).
     - Individual coil outlet temperature (COT) target nominal: 845.0 [deg C].
     - Pass balancing control via individual trim valves to eliminate temperature maldistribution (< 2.0 [deg C] spread).
     - Firing via staged low-NOx hearth floor burners and radiant sidewall cup burners.
     
  2. DYNAMIC CROSS-LIMITING FEED-TO-STEAM MASS RATIO CASCADE:
     - Dilution steam (DS) prevents premature olefin polymerization, reduces hydrocarbon partial pressure, and lowers coking rate.
     - Target DS ratio: 0.350 [kg steam / kg HC] (typical operating range 0.300 to 0.450 [kg/kg]).
     - Dynamic cross-limiting prevents hydrocarbon feed increase unless dilution steam flow leads; on feed decrease, HC leads.
     - Strict Low-Low ratio trip to prevent catastrophic instantaneous coil carbon fouling.
     
  3. TRANSFER LINE EXCHANGER (TLE) ULTRA-FAST QUENCHING (< 40 ms RESIDENCE TIME):
     - Immediate thermal quenching of cracked effluent gas from ~845.0 [deg C] to ~400.0 [deg C] to freeze secondary reactions.
     - Shell-and-tube / double-pipe exchanger generating 110 [bar] saturated HP steam into main steam drum.
     - Secondary quench oil injection trim for precise downstream transfer line temperature regulation.
     - Online TLE fouling surveillance based on overall heat transfer coefficient (U_TLE) and gas-side pressure drop.
     
  4. RADIANT TUBE METAL TEMPERATURE (TMT) & COKING RESISTANCE OBSERVER:
     - High-alloy metallurgy: 25Cr/35Ni/Nb/Ti microalloyed centrifugal cast tubes (creep limit ~1,080.0 [deg C]).
     - Online laser pyrometry scanning combined with first-principles radial heat conduction observer.
     - Sundaram-Froment coking kinetic rate observer: computes internal pyrolytic coke thickness [mm] and thermal resistance.
     - Dynamic run-length remaining prognostic calculation before required decoking cycle.
     
  5. 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING:
     - 12 critical process channels with 2oo3 TMR voting, discrepancy accumulation timers, and bumpless degradation.
     - Degrades seamlessly from 2oo3 to 2oo2, 1oo1, or fail-safe freeze upon multiple transmitter discrepancies.
     
  6. 8-STATE MULTIVARIABLE DISCRETE STATE-SPACE OBSERVER & RECEDING-HORIZON MPC:
     - Sample time T_s = 20 [ms]. 8 discrete states, 6 manipulated variables, 8 measured outputs.
     - State-Space matrices A(8x8), B(8x6), C(8x8), D(8x6) and Kalman observer gain L(8x8).
     - Model Predictive Control with quadratic cost functional (Q, R, S, P) optimized via Projected Gradient Descent (PGD).
     
  7. 14-STAGE DETERMINISTIC PRODUCTION FINITE STATE MACHINE:
     - State 0: Init & Safe Standby
     - State 1: Cold/Hot Nitrogen Purge (4 volume changes)
     - State 2: BMS Pilot Gas Header Ignition & Flame Verification
     - State 3: Refractory Dryout & Controlled Thermal Stress Warmup Ramp
     - State 4: Dilution Steam Circulation & Coil Pre-conditioning
     - State 5: Hydrocarbon Feed Dynamic Cut-in & Cross-Limiting Lock
     - State 6: Radiant 8-Pass Coil COT Trim Balancing
     - State 7: Normal Steady-State Cracking MPC Optimization
     - State 8: High-Severity Cracking (Maximum Olefins Selectivity)
     - State 9: Coking Surveillance & Decoke Transition Advisory
     - State 10: Online Decoking Steam/Air Oxidation Burn Cycle
     - State 11: Controlled Hot Idle Thermal Slump
     - State 12: Emergency Automated Feed Trip (AFT) & Quick Fuel Cutoff
     - State 13: Controlled Emergency Post-Purge & Furnace Cooldown
     
  8. ISA-18.2 MULTI-TIER ALARM MANAGEMENT & BIT-PACKED STATUS WORDS:
     - 16 distinct process channels with HH, H, L, LL, Rate-of-Change, and deadband clearance hysteresis.
     - Dual 32-bit bit-packed Alarm Words (dwAlarmWord1, dwAlarmWord2).
     - Dual 32-bit bit-packed Operational Status Words (dwStatusWord1, dwStatusWord2).
========================================================================================================================
*)
""")

    # VAR_INPUT
    parts.append("""VAR_INPUT
    (* Master Operational Commands & System Interlocks *)
    bEnable                         : BOOL;     (* Master functional enable command [-] *)
    bSafetyInterlock_OK             : BOOL;     (* Safety Instrumented System (SIS) Burner Management permissive [-] *)
    bManualOverride_En              : BOOL;     (* Supervisory manual actuator override permissive [-] *)
    bDecokeMode_Req                 : BOOL;     (* Operator command request to enter decoking burn cycle [-] *)
    bAFT_Trip_Command               : BOOL;     (* Emergency Automated Feed Trip (AFT) fast fuel cutoff trigger [-] *)
    bAcknowledge_Alarms             : BOOL;     (* Operator alarm reset & acknowledge pushbutton [-] *)
    tCycleTime                      : TIME := T#20MS; (* PLC execution task scan cycle time [ms] *)

    (* Coil Outlet Temperature (COT) Thermocouple Rakes - 2oo3 Triple Modular Redundancy Channels *)
    rCoilOutletTemp_Pass1_A         : REAL;     (* Coil 1 outlet thermocouple rake channel A [deg C] *)
    rCoilOutletTemp_Pass1_B         : REAL;     (* Coil 1 outlet thermocouple rake channel B [deg C] *)
    rCoilOutletTemp_Pass1_C         : REAL;     (* Coil 1 outlet thermocouple rake channel C [deg C] *)
    rCoilOutletTemp_Pass2_A         : REAL;     (* Coil 2 outlet thermocouple rake channel A [deg C] *)
    rCoilOutletTemp_Pass2_B         : REAL;     (* Coil 2 outlet thermocouple rake channel B [deg C] *)
    rCoilOutletTemp_Pass2_C         : REAL;     (* Coil 2 outlet thermocouple rake channel C [deg C] *)
    rCoilOutletTemp_Pass3_A         : REAL;     (* Coil 3 outlet thermocouple rake channel A [deg C] *)
    rCoilOutletTemp_Pass3_B         : REAL;     (* Coil 3 outlet thermocouple rake channel B [deg C] *)
    rCoilOutletTemp_Pass3_C         : REAL;     (* Coil 3 outlet thermocouple rake channel C [deg C] *)
    rCoilOutletTemp_Pass4_A         : REAL;     (* Coil 4 outlet thermocouple rake channel A [deg C] *)
    rCoilOutletTemp_Pass4_B         : REAL;     (* Coil 4 outlet thermocouple rake channel B [deg C] *)
    rCoilOutletTemp_Pass4_C         : REAL;     (* Coil 4 outlet thermocouple rake channel C [deg C] *)
    rCoilOutletTemp_Pass5_A         : REAL;     (* Coil 5 outlet thermocouple rake channel A [deg C] *)
    rCoilOutletTemp_Pass5_B         : REAL;     (* Coil 5 outlet thermocouple rake channel B [deg C] *)
    rCoilOutletTemp_Pass5_C         : REAL;     (* Coil 5 outlet thermocouple rake channel C [deg C] *)
    rCoilOutletTemp_Pass6_A         : REAL;     (* Coil 6 outlet thermocouple rake channel A [deg C] *)
    rCoilOutletTemp_Pass6_B         : REAL;     (* Coil 6 outlet thermocouple rake channel B [deg C] *)
    rCoilOutletTemp_Pass6_C         : REAL;     (* Coil 6 outlet thermocouple rake channel C [deg C] *)
    rCoilOutletTemp_Pass7_A         : REAL;     (* Coil 7 outlet thermocouple rake channel A [deg C] *)
    rCoilOutletTemp_Pass7_B         : REAL;     (* Coil 7 outlet thermocouple rake channel B [deg C] *)
    rCoilOutletTemp_Pass7_C         : REAL;     (* Coil 7 outlet thermocouple rake channel C [deg C] *)
    rCoilOutletTemp_Pass8_A         : REAL;     (* Coil 8 outlet thermocouple rake channel A [deg C] *)
    rCoilOutletTemp_Pass8_B         : REAL;     (* Coil 8 outlet thermocouple rake channel B [deg C] *)
    rCoilOutletTemp_Pass8_C         : REAL;     (* Coil 8 outlet thermocouple rake channel C [deg C] *)

    (* Fuel Gas Header Supply Pressure - 2oo3 TMR Triplets *)
    rFuelGas_SupplyPressure_A       : REAL;     (* Fuel gas supply manifold pressure transmitter A [bar] *)
    rFuelGas_SupplyPressure_B       : REAL;     (* Fuel gas supply manifold pressure transmitter B [bar] *)
    rFuelGas_SupplyPressure_C       : REAL;     (* Fuel gas supply manifold pressure transmitter C [bar] *)

    (* Firebox Arch Draft Pressure - 2oo3 TMR Triplets *)
    rFirebox_DraftPressure_A        : REAL;     (* Firebox arch differential draft pressure transmitter A [mbar] *)
    rFirebox_DraftPressure_B        : REAL;     (* Firebox arch differential draft pressure transmitter B [mbar] *)
    rFirebox_DraftPressure_C        : REAL;     (* Firebox arch differential draft pressure transmitter C [mbar] *)

    (* Flue Gas Stack Oxygen Concentration - 2oo3 TMR Triplets *)
    rFlueGas_OxygenContent_A        : REAL;     (* Flue gas stack zirconium oxygen analyzer channel A [%] *)
    rFlueGas_OxygenContent_B        : REAL;     (* Flue gas stack zirconium oxygen analyzer channel B [%] *)
    rFlueGas_OxygenContent_C        : REAL;     (* Flue gas stack zirconium oxygen analyzer channel C [%] *)

    (* Transfer Line Exchanger (TLE) Effluent Outlet Temperature - 2oo3 TMR Triplets *)
    rTLE_OutletTemperature_A        : REAL;     (* TLE quenched process gas outlet temperature transmitter A [deg C] *)
    rTLE_OutletTemperature_B        : REAL;     (* TLE quenched process gas outlet temperature transmitter B [deg C] *)
    rTLE_OutletTemperature_C        : REAL;     (* TLE quenched process gas outlet temperature transmitter C [deg C] *)

    (* Hydrocarbon Feed & Dilution Steam Mass Flow Transmitters *)
    rHydrocarbonFeed_MassFlow_Total : REAL;     (* Total hydrocarbon feed mass flow to furnace [t/h] *)
    rDilutionSteam_MassFlow_Total   : REAL;     (* Total dilution steam mass flow to furnace [t/h] *)
    rPass1_FeedFlow                 : REAL;     (* Pass 1 hydrocarbon feed mass flow rate [t/h] *)
    rPass2_FeedFlow                 : REAL;     (* Pass 2 hydrocarbon feed mass flow rate [t/h] *)
    rPass3_FeedFlow                 : REAL;     (* Pass 3 hydrocarbon feed mass flow rate [t/h] *)
    rPass4_FeedFlow                 : REAL;     (* Pass 4 hydrocarbon feed mass flow rate [t/h] *)
    rPass5_FeedFlow                 : REAL;     (* Pass 5 hydrocarbon feed mass flow rate [t/h] *)
    rPass6_FeedFlow                 : REAL;     (* Pass 6 hydrocarbon feed mass flow rate [t/h] *)
    rPass7_FeedFlow                 : REAL;     (* Pass 7 hydrocarbon feed mass flow rate [t/h] *)
    rPass8_FeedFlow                 : REAL;     (* Pass 8 hydrocarbon feed mass flow rate [t/h] *)

    (* Pyrometry, Emissions & Auxiliary Process Instrumentation *)
    rLaserPyrometer_Peak_TMT        : REAL;     (* Radiant tube peak skin metal temperature from laser pyrometer [deg C] *)
    rTLE_SteamDrum_Pressure         : REAL;     (* TLE saturated steam drum operating pressure [bar] *)
    rTLE_QuenchOil_InletTemp        : REAL;     (* Secondary oil quench injection temperature [deg C] *)
    rDecokeAir_MassFlow             : REAL;     (* Decoking air injection volumetric flow rate [Nm3/h] *)
    rFlueGas_CO_Content             : REAL;     (* Stack carbon monoxide concentration [ppm] *)
    rFlueGas_NOx_Content            : REAL;     (* Stack nitrogen oxides concentration [ppm] *)
    rAmbient_Temperature           : REAL;     (* Combustion air dry-bulb ambient temperature [deg C] *)

    (* Supervisory Master Targets & Constraints *)
    rTarget_COT_Setpoint            : REAL;     (* Master supervisory coil outlet temperature target [deg C] *)
    rTarget_DS_Ratio_Setpoint       : REAL;     (* Master supervisory dilution steam mass ratio target [kg/kg] *)
    rTarget_Total_HC_Feed_Setpoint  : REAL;     (* Master total hydrocarbon feed flow setpoint [t/h] *)
    rMax_Allowable_TMT              : REAL := 1080.0; (* Maximum metallurgically allowable tube skin temperature [deg C] *)
    rTarget_Draft_Setpoint          : REAL := -1.50;  (* Arch draft operating setpoint [mbar] *)
    rTarget_FlueGas_O2_Setpoint     : REAL := 2.00;   (* Flue gas excess oxygen operating setpoint [%] *)
END_VAR
""")

    # VAR_OUTPUT
    parts.append("""VAR_OUTPUT
    (* Primary Operational & Safety Status Flags *)
    bFurnace_Ready                  : BOOL;     (* Furnace warm and permissive satisfied for hydrocarbon cut-in [-] *)
    bFurnace_OnSpec                 : BOOL;     (* Furnace operating within steady-state COT, severity and draft envelope [-] *)
    bAFT_Tripped                    : BOOL;     (* Emergency Automated Feed Trip (AFT) fast fuel cutoff active [-] *)
    bDecoke_Active                  : BOOL;     (* Online decoking steam/air burn cycle active [-] *)
    bTMR_Degraded_Warning           : BOOL;     (* Sensor discrepancy detected; running on degraded 2oo2 or 1oo1 [-] *)
    bMPC_Feasible                   : BOOL;     (* Receding-horizon MPC solver successfully converged [-] *)

    (* Final Control Element Actuator Demands [0.0 .. 100.0 %] *)
    rFuelGas_ControlValve_Demand    : REAL;     (* Master fuel gas control valve position demand [%] *)
    rIDFan_VFD_Speed_Demand         : REAL;     (* Induced draft (ID) fan variable frequency speed reference [%] *)
    rStackDamper_Position_Demand    : REAL;     (* Stack flue gas damper actuator command [%] *)
    rTLE_QuenchOil_Valve_Demand     : REAL;     (* TLE secondary quench oil injection control valve demand [%] *)
    rTLE_BlowdownValve_Demand       : REAL;     (* TLE continuous high-pressure boiler blowdown valve demand [%] *)
    rCombustionAir_Damper_Demand    : REAL;     (* Low-NOx combustion air plenum intake register command [%] *)

    (* Radiant 8-Pass Coil Feed Trim Actuator Demands [0.0 .. 100.0 %] *)
    rCoil1_FeedTrimValve_Demand     : REAL;     (* Coil 1 inlet feed flow trim valve command [%] *)
    rCoil2_FeedTrimValve_Demand     : REAL;     (* Coil 2 inlet feed flow trim valve command [%] *)
    rCoil3_FeedTrimValve_Demand     : REAL;     (* Coil 3 inlet feed flow trim valve command [%] *)
    rCoil4_FeedTrimValve_Demand     : REAL;     (* Coil 4 inlet feed flow trim valve command [%] *)
    rCoil5_FeedTrimValve_Demand     : REAL;     (* Coil 5 inlet feed flow trim valve command [%] *)
    rCoil6_FeedTrimValve_Demand     : REAL;     (* Coil 6 inlet feed flow trim valve command [%] *)
    rCoil7_FeedTrimValve_Demand     : REAL;     (* Coil 7 inlet feed flow trim valve command [%] *)
    rCoil8_FeedTrimValve_Demand     : REAL;     (* Coil 8 inlet feed flow trim valve command [%] *)

    (* 2oo3 TMR Voted Process Variables *)
    rVoted_Average_COT              : REAL;     (* Triple modular redundant voted mean coil outlet temperature [deg C] *)
    rVoted_Firebox_Draft            : REAL;     (* Triple modular redundant voted firebox arch draft pressure [mbar] *)
    rVoted_FuelGas_Pressure         : REAL;     (* Triple modular redundant voted fuel gas supply pressure [bar] *)
    rVoted_FlueGas_O2               : REAL;     (* Triple modular redundant voted flue gas excess oxygen [%] *)
    rVoted_TLE_OutletTemp           : REAL;     (* Triple modular redundant voted TLE effluent outlet temperature [deg C] *)

    (* Cyber-Physical Observer & Prognostic Estimations *)
    rEstimated_Max_CokeThickness    : REAL;     (* Online observer estimated worst-case internal coke layer [mm] *)
    rObserved_ThermalResistance     : REAL;     (* Online observer estimated tube fouling thermal resistance [m2K/kW] *)
    rKinetic_Ethylene_Yield         : REAL;     (* First-principles kinetic model predicted ethylene product yield [%] *)
    rKinetic_Cracking_Severity      : REAL;     (* Calculated equivalent PKS kinetic cracking severity index [-] *)
    rCalculated_DS_Ratio            : REAL;     (* Real-time operating dilution steam to hydrocarbon mass ratio [kg/kg] *)
    rRunLength_Remaining_Hours      : REAL;     (* Prognostic estimated run hours remaining before decoking trip [h] *)
    rMax_Pass_DeltaT                : REAL;     (* Maximum temperature maldistribution spread across 8 passes [deg C] *)

    (* Finite State Machine State & Bit-Packed Supervisory Diagnostic Words *)
    nActive_State_ID                : INT;      (* Current active FSM state enumeration identifier [-] *)
    dwAlarmWord1                    : DWORD;    (* ISA-18.2 Critical Emergency & High-High Trip Alarm Word [-] *)
    dwAlarmWord2                    : DWORD;    (* ISA-18.2 Warning, Deviation & Low-Low Alarm Word [-] *)
    dwStatusWord1                   : DWORD;    (* Operational Status Word 1: Subsystem Health & Permissives [-] *)
    dwStatusWord2                   : DWORD;    (* Operational Status Word 2: TMR Degradation & MPC Convergence [-] *)
END_VAR
""")

    # VAR (Internal variables)
    parts.append("""VAR
    (* ============================================================================================================== *)
    (* INTERNAL CYBER-PHYSICAL STATE-SPACE SYSTEM MATRICES (8-STATE, 6-INPUT, 8-OUTPUT DISCRETIZED AT Ts = 20 MS)    *)
    (* States x = [COT_dev, Draft_dev, Feed_dev, Ratio_dev, TLE_dev, Rcoke_dev, Pfg_dev, O2_dev]^T                   *)
    (* Inputs u = [u_fg_valv, u_draft_vfd, u_feed_sp, u_steam_sp, u_quench, u_air_bias]^T                            *)
    (* ============================================================================================================== *)
    
    (* Discrete State Transition Matrix A (8 x 8) *)
    rA_11 : REAL := 0.98542; rA_12 : REAL := 0.00124; rA_13 : REAL :=-0.01428; rA_14 : REAL :=-0.00845;
    rA_15 : REAL := 0.00000; rA_16 : REAL := 0.00512; rA_17 : REAL := 0.01890; rA_18 : REAL :=-0.00315;
    
    rA_21 : REAL := 0.00045; rA_22 : REAL := 0.92410; rA_23 : REAL := 0.00000; rA_24 : REAL := 0.00000;
    rA_25 : REAL := 0.00000; rA_26 : REAL := 0.00000; rA_27 : REAL := 0.00842; rA_28 : REAL := 0.00185;
    
    rA_31 : REAL := 0.00000; rA_32 : REAL := 0.00000; rA_33 : REAL := 0.95120; rA_34 : REAL := 0.00000;
    rA_35 : REAL := 0.00000; rA_36 : REAL := 0.00000; rA_37 : REAL := 0.00000; rA_38 : REAL := 0.00000;
    
    rA_41 : REAL := 0.00012; rA_42 : REAL := 0.00000; rA_43 : REAL :=-0.00418; rA_44 : REAL := 0.94230;
    rA_45 : REAL := 0.00000; rA_46 : REAL := 0.00000; rA_47 : REAL := 0.00000; rA_48 : REAL := 0.00000;
    
    rA_51 : REAL := 0.04820; rA_52 : REAL := 0.00000; rA_53 : REAL := 0.01250; rA_54 : REAL :=-0.00890;
    rA_55 : REAL := 0.93150; rA_56 : REAL := 0.00240; rA_57 : REAL := 0.00000; rA_58 : REAL := 0.00000;
    
    rA_61 : REAL := 0.00085; rA_62 : REAL := 0.00000; rA_63 : REAL := 0.00042; rA_64 : REAL :=-0.00095;
    rA_65 : REAL := 0.00000; rA_66 : REAL := 0.99988; rA_67 : REAL := 0.00000; rA_68 : REAL := 0.00000;
    
    rA_71 : REAL := 0.00000; rA_72 : REAL := 0.00000; rA_73 : REAL := 0.00000; rA_74 : REAL := 0.00000;
    rA_75 : REAL := 0.00000; rA_76 : REAL := 0.00000; rA_77 : REAL := 0.91250; rA_78 : REAL := 0.00000;
    
    rA_81 : REAL :=-0.00082; rA_82 : REAL := 0.00215; rA_83 : REAL := 0.00000; rA_84 : REAL := 0.00000;
    rA_85 : REAL := 0.00000; rA_86 : REAL := 0.00000; rA_87 : REAL :=-0.01420; rA_88 : REAL := 0.93800;

    (* Discrete Input Coupling Matrix B (8 x 6) *)
    rB_11 : REAL := 0.04250; rB_12 : REAL :=-0.00085; rB_13 : REAL :=-0.01250; rB_14 : REAL :=-0.00620; rB_15 : REAL := 0.00000; rB_16 : REAL :=-0.00180;
    rB_21 : REAL := 0.00480; rB_22 : REAL :=-0.03850; rB_23 : REAL := 0.00000; rB_24 : REAL := 0.00000; rB_25 : REAL := 0.00000; rB_26 : REAL := 0.00650;
    rB_31 : REAL := 0.00000; rB_32 : REAL := 0.00000; rB_33 : REAL := 0.04880; rB_34 : REAL := 0.00000; rB_35 : REAL := 0.00000; rB_36 : REAL := 0.00000;
    rB_41 : REAL := 0.00000; rB_42 : REAL := 0.00000; rB_43 : REAL :=-0.00350; rB_44 : REAL := 0.05770; rB_45 : REAL := 0.00000; rB_46 : REAL := 0.00000;
    rB_51 : REAL := 0.00850; rB_52 : REAL := 0.00000; rB_53 : REAL := 0.00620; rB_54 : REAL :=-0.00410; rB_55 : REAL :=-0.06850; rB_56 : REAL := 0.00000;
    rB_61 : REAL := 0.00018; rB_62 : REAL := 0.00000; rB_63 : REAL := 0.00012; rB_64 : REAL :=-0.00028; rB_65 : REAL := 0.00000; rB_66 : REAL := 0.00000;
    rB_71 : REAL :=-0.08750; rB_72 : REAL := 0.00000; rB_73 : REAL := 0.00000; rB_74 : REAL := 0.00000; rB_75 : REAL := 0.00000; rB_76 : REAL := 0.00000;
    rB_81 : REAL :=-0.03210; rB_82 : REAL := 0.01180; rB_83 : REAL := 0.00000; rB_84 : REAL := 0.00000; rB_85 : REAL := 0.00000; rB_86 : REAL := 0.04520;

    (* Discrete Measurement Matrix C (8 x 8) - Identity with cross-coupling *)
    rC_11 : REAL := 1.00000; rC_12 : REAL := 0.00000; rC_13 : REAL := 0.00000; rC_14 : REAL := 0.00000; rC_15 : REAL := 0.00000; rC_16 : REAL := 0.00000; rC_17 : REAL := 0.00000; rC_18 : REAL := 0.00000;
    rC_21 : REAL := 0.00000; rC_22 : REAL := 1.00000; rC_23 : REAL := 0.00000; rC_24 : REAL := 0.00000; rC_25 : REAL := 0.00000; rC_26 : REAL := 0.00000; rC_27 : REAL := 0.00000; rC_28 : REAL := 0.00000;
    rC_31 : REAL := 0.00000; rC_32 : REAL := 0.00000; rC_33 : REAL := 1.00000; rC_34 : REAL := 0.00000; rC_35 : REAL := 0.00000; rC_36 : REAL := 0.00000; rC_37 : REAL := 0.00000; rC_38 : REAL := 0.00000;
    rC_41 : REAL := 0.00000; rC_42 : REAL := 0.00000; rC_43 : REAL := 0.00000; rC_44 : REAL := 1.00000; rC_45 : REAL := 0.00000; rC_46 : REAL := 0.00000; rC_47 : REAL := 0.00000; rC_48 : REAL := 0.00000;
    rC_51 : REAL := 0.00000; rC_52 : REAL := 0.00000; rC_53 : REAL := 0.00000; rC_54 : REAL := 0.00000; rC_55 : REAL := 1.00000; rC_56 : REAL := 0.00000; rC_57 : REAL := 0.00000; rC_58 : REAL := 0.00000;
    rC_61 : REAL := 0.00000; rC_62 : REAL := 0.00000; rC_63 : REAL := 0.00000; rC_64 : REAL := 0.00000; rC_65 : REAL := 0.00000; rC_66 : REAL := 1.00000; rC_67 : REAL := 0.00000; rC_68 : REAL := 0.00000;
    rC_71 : REAL := 0.00000; rC_72 : REAL := 0.00000; rC_73 : REAL := 0.00000; rC_74 : REAL := 0.00000; rC_75 : REAL := 0.00000; rC_76 : REAL := 0.00000; rC_77 : REAL := 1.00000; rC_78 : REAL := 0.00000;
    rC_81 : REAL := 0.00000; rC_82 : REAL := 0.00000; rC_83 : REAL := 0.00000; rC_84 : REAL := 0.00000; rC_85 : REAL := 0.00000; rC_86 : REAL := 0.00000; rC_87 : REAL := 0.00000; rC_88 : REAL := 1.00000;

    (* Discrete Direct Feedthrough Matrix D (8 x 6) - Zero transmission *)
    rD_11 : REAL := 0.0; rD_12 : REAL := 0.0; rD_13 : REAL := 0.0; rD_14 : REAL := 0.0; rD_15 : REAL := 0.0; rD_16 : REAL := 0.0;
    rD_21 : REAL := 0.0; rD_22 : REAL := 0.0; rD_23 : REAL := 0.0; rD_24 : REAL := 0.0; rD_25 : REAL := 0.0; rD_26 : REAL := 0.0;
    rD_31 : REAL := 0.0; rD_32 : REAL := 0.0; rD_33 : REAL := 0.0; rD_34 : REAL := 0.0; rD_35 : REAL := 0.0; rD_36 : REAL := 0.0;
    rD_41 : REAL := 0.0; rD_42 : REAL := 0.0; rD_43 : REAL := 0.0; rD_44 : REAL := 0.0; rD_45 : REAL := 0.0; rD_46 : REAL := 0.0;
    rD_51 : REAL := 0.0; rD_52 : REAL := 0.0; rD_53 : REAL := 0.0; rD_54 : REAL := 0.0; rD_55 : REAL := 0.0; rD_56 : REAL := 0.0;
    rD_61 : REAL := 0.0; rD_62 : REAL := 0.0; rD_63 : REAL := 0.0; rD_64 : REAL := 0.0; rD_65 : REAL := 0.0; rD_66 : REAL := 0.0;
    rD_71 : REAL := 0.0; rD_72 : REAL := 0.0; rD_73 : REAL := 0.0; rD_74 : REAL := 0.0; rD_75 : REAL := 0.0; rD_76 : REAL := 0.0;
    rD_81 : REAL := 0.0; rD_82 : REAL := 0.0; rD_83 : REAL := 0.0; rD_84 : REAL := 0.0; rD_85 : REAL := 0.0; rD_86 : REAL := 0.0;

    (* Steady-State Kalman Filter Observer Gain Matrix L (8 x 8) *)
    rL_11 : REAL := 0.1245; rL_12 : REAL := 0.0010; rL_13 : REAL :=-0.0052; rL_14 : REAL :=-0.0018; rL_15 : REAL := 0.0025; rL_16 : REAL := 0.0084; rL_17 : REAL := 0.0125; rL_18 : REAL :=-0.0015;
    rL_21 : REAL := 0.0008; rL_22 : REAL := 0.1850; rL_23 : REAL := 0.0000; rL_24 : REAL := 0.0000; rL_25 : REAL := 0.0000; rL_26 : REAL := 0.0000; rL_27 : REAL := 0.0062; rL_28 : REAL := 0.0041;
    rL_31 : REAL :=-0.0012; rL_32 : REAL := 0.0000; rL_33 : REAL := 0.2150; rL_34 : REAL := 0.0000; rL_35 : REAL := 0.0000; rL_36 : REAL := 0.0000; rL_37 : REAL := 0.0000; rL_38 : REAL := 0.0000;
    rL_41 : REAL := 0.0005; rL_42 : REAL := 0.0000; rL_43 : REAL :=-0.0028; rL_44 : REAL := 0.1980; rL_45 : REAL := 0.0000; rL_46 : REAL := 0.0000; rL_47 : REAL := 0.0000; rL_48 : REAL := 0.0000;
    rL_51 : REAL := 0.0385; rL_52 : REAL := 0.0000; rL_53 : REAL := 0.0094; rL_54 : REAL :=-0.0042; rL_55 : REAL := 0.2450; rL_56 : REAL := 0.0015; rL_57 : REAL := 0.0000; rL_58 : REAL := 0.0000;
    rL_61 : REAL := 0.0012; rL_62 : REAL := 0.0000; rL_63 : REAL := 0.0005; rL_64 : REAL :=-0.0011; rL_65 : REAL := 0.0000; rL_66 : REAL := 0.0520; rL_67 : REAL := 0.0000; rL_68 : REAL := 0.0000;
    rL_71 : REAL := 0.0024; rL_72 : REAL := 0.0015; rL_73 : REAL := 0.0000; rL_74 : REAL := 0.0000; rL_75 : REAL := 0.0000; rL_76 : REAL := 0.0000; rL_77 : REAL := 0.2240; rL_78 : REAL :=-0.0085;
    rL_81 : REAL :=-0.0021; rL_82 : REAL := 0.0045; rL_83 : REAL := 0.0000; rL_84 : REAL := 0.0000; rL_85 : REAL := 0.0000; rL_86 : REAL := 0.0000; rL_87 : REAL :=-0.0112; rL_88 : REAL := 0.1820;

    (* State Vector Estimates x_hat [k] *)
    rx_hat_1 : REAL := 0.0; (* COT deviation [deg C] *)
    rx_hat_2 : REAL := 0.0; (* Firebox draft deviation [mbar] *)
    rx_hat_3 : REAL := 0.0; (* Total feed flow deviation [t/h] *)
    rx_hat_4 : REAL := 0.0; (* Dilution steam ratio deviation [kg/kg] *)
    rx_hat_5 : REAL := 0.0; (* TLE outlet temperature deviation [deg C] *)
    rx_hat_6 : REAL := 0.0; (* Internal coke resistance deviation [m2K/kW] *)
    rx_hat_7 : REAL := 0.0; (* Fuel gas pressure deviation [bar] *)
    rx_hat_8 : REAL := 0.0; (* Flue gas oxygen deviation [%] *)

    (* A-priori State Predictions x_pred [k+1|k] *)
    rx_pred_1 : REAL := 0.0; rx_pred_2 : REAL := 0.0; rx_pred_3 : REAL := 0.0; rx_pred_4 : REAL := 0.0;
    rx_pred_5 : REAL := 0.0; rx_pred_6 : REAL := 0.0; rx_pred_7 : REAL := 0.0; rx_pred_8 : REAL := 0.0;

    (* Measurement Innovations / Residuals e [k] *)
    re_innov_1 : REAL := 0.0; re_innov_2 : REAL := 0.0; re_innov_3 : REAL := 0.0; re_innov_4 : REAL := 0.0;
    re_innov_5 : REAL := 0.0; re_innov_6 : REAL := 0.0; re_innov_7 : REAL := 0.0; re_innov_8 : REAL := 0.0;

    (* Manipulated Variable Deviation Vector u [k] *)
    ru_dev_1 : REAL := 0.0; (* Fuel gas valve demand deviation [%] *)
    ru_dev_2 : REAL := 0.0; (* ID fan speed deviation [%] *)
    ru_dev_3 : REAL := 0.0; (* HC feed setpoint deviation [t/h] *)
    ru_dev_4 : REAL := 0.0; (* Steam flow setpoint deviation [t/h] *)
    ru_dev_5 : REAL := 0.0; (* TLE quench oil valve deviation [%] *)
    ru_dev_6 : REAL := 0.0; (* Combustion air damper bias [%] *)

    (* Actuator Baseline Operating Points *)
    rBase_FuelGas_Demand    : REAL := 55.0; (* [%] *)
    rBase_IDFan_Demand      : REAL := 62.0; (* [%] *)
    rBase_HC_Feed_Flow      : REAL := 35.0; (* [t/h] *)
    rBase_Steam_Flow        : REAL := 12.25;(* [t/h] (0.35 ratio) *)
    rBase_QuenchOil_Demand  : REAL := 45.0; (* [%] *)
    rBase_AirDamper_Demand  : REAL := 58.0; (* [%] *)

    (* ============================================================================================================== *)
    (* RECEDING-HORIZON MODEL PREDICTIVE CONTROL OPTIMIZATION WEIGHTS & PROJECTED GRADIENT DESCENT ARRAYS              *)
    (* Horizons: Prediction Np = 5 steps (100 ms), Control Nc = 3 steps (60 ms)                                       *)
    (* ============================================================================================================== *)
    (* State Tracking Error Diagonal Penalty Weights Q *)
    rQ_diag_1 : REAL := 18.50;  (* COT deviation weight *)
    rQ_diag_2 : REAL := 12.00;  (* Draft pressure deviation weight *)
    rQ_diag_3 : REAL := 6.50;   (* Feed flow deviation weight *)
    rQ_diag_4 : REAL := 16.00;  (* Steam ratio deviation weight *)
    rQ_diag_5 : REAL := 8.50;   (* TLE temp deviation weight *)
    rQ_diag_6 : REAL := 25.00;  (* Coke resistance penalty weight *)
    rQ_diag_7 : REAL := 7.00;   (* Fuel gas pressure deviation weight *)
    rQ_diag_8 : REAL := 9.50;   (* Flue gas oxygen deviation weight *)

    (* Actuator Movement Diagonal Penalty Weights R *)
    rR_diag_1 : REAL := 3.20;   (* Fuel gas valve effort *)
    rR_diag_2 : REAL := 2.10;   (* ID fan speed effort *)
    rR_diag_3 : REAL := 4.50;   (* Feed setpoint movement effort *)
    rR_diag_4 : REAL := 5.20;   (* Steam setpoint movement effort *)
    rR_diag_5 : REAL := 1.80;   (* Quench valve effort *)
    rR_diag_6 : REAL := 1.60;   (* Air damper bias effort *)

    (* Actuator Slew Rate Diagonal Penalty Weights S *)
    rS_diag_1 : REAL := 6.50;   (* Fuel gas slew penalty *)
    rS_diag_2 : REAL := 4.80;   (* ID fan slew penalty *)
    rS_diag_3 : REAL := 8.00;   (* Feed slew penalty *)
    rS_diag_4 : REAL := 9.20;   (* Steam slew penalty *)
    rS_diag_5 : REAL := 3.50;   (* Quench slew penalty *)
    rS_diag_6 : REAL := 3.00;   (* Air damper slew penalty *)

    (* Terminal State Penalty Weights P *)
    rP_diag_1 : REAL := 45.00; rP_diag_2 : REAL := 28.00; rP_diag_3 : REAL := 15.00; rP_diag_4 : REAL := 38.00;
    rP_diag_5 : REAL := 20.00; rP_diag_6 : REAL := 60.00; rP_diag_7 : REAL := 16.00; rP_diag_8 : REAL := 22.00;

    (* MPC Actuator Dynamic Saturation Limits *)
    rU_Min_1 : REAL := 10.0; rU_Max_1 : REAL := 95.0;   (* Fuel gas valve demand [%] *)
    rU_Min_2 : REAL := 15.0; rU_Max_2 : REAL := 98.0;   (* ID fan speed [%] *)
    rU_Min_3 : REAL := 15.0; rU_Max_3 : REAL := 50.0;   (* Total HC feed [t/h] *)
    rU_Min_4 : REAL := 5.0;  rU_Max_4 : REAL := 25.0;   (* Total dilution steam [t/h] *)
    rU_Min_5 : REAL := 0.0;  rU_Max_5 : REAL := 100.0;  (* Quench valve demand [%] *)
    rU_Min_6 : REAL :=-15.0; rU_Max_6 : REAL := 15.0;   (* Air damper trim [%] *)

    (* Maximum Actuator Slew Rates per PLC Task Scan Cycle (20 ms) *)
    rMaxDeltaU_1 : REAL := 0.050; (* Fuel gas valve max change [%/cycle] (2.5 %/s) *)
    rMaxDeltaU_2 : REAL := 0.080; (* ID fan speed max change [%/cycle] (4.0 %/s) *)
    rMaxDeltaU_3 : REAL := 0.015; (* Total feed max change [t/h/cycle] (0.75 t/h/s) *)
    rMaxDeltaU_4 : REAL := 0.010; (* Dilution steam max change [t/h/cycle] (0.50 t/h/s) *)
    rMaxDeltaU_5 : REAL := 0.150; (* Quench valve max change [%/cycle] (7.5 %/s) *)
    rMaxDeltaU_6 : REAL := 0.040; (* Air damper bias max change [%/cycle] (2.0 %/s) *)

    (* Optimization Iteration Buffers *)
    ru_opt_1 : REAL := 0.0; ru_opt_2 : REAL := 0.0; ru_opt_3 : REAL := 0.0;
    ru_opt_4 : REAL := 0.0; ru_opt_5 : REAL := 0.0; ru_opt_6 : REAL := 0.0;
    rGrad_1 : REAL := 0.0; rGrad_2 : REAL := 0.0; rGrad_3 : REAL := 0.0;
    rGrad_4 : REAL := 0.0; rGrad_5 : REAL := 0.0; rGrad_6 : REAL := 0.0;
    rAlpha_PGD : REAL := 0.065; (* Gradient descent learning rate / step size *)
    nPGD_Iter : INT := 0;
    rMPC_Cost_Total : REAL := 0.0;
    rMPC_Cost_Best  : REAL := 1.0E9;

    (* Predicted Horizon States x_hor[step, state] *)
    rx_hor_1_1 : REAL; rx_hor_1_2 : REAL; rx_hor_1_3 : REAL; rx_hor_1_4 : REAL;
    rx_hor_1_5 : REAL; rx_hor_1_6 : REAL; rx_hor_1_7 : REAL; rx_hor_1_8 : REAL;

    rx_hor_2_1 : REAL; rx_hor_2_2 : REAL; rx_hor_2_3 : REAL; rx_hor_2_4 : REAL;
    rx_hor_2_5 : REAL; rx_hor_2_6 : REAL; rx_hor_2_7 : REAL; rx_hor_2_8 : REAL;

    rx_hor_3_1 : REAL; rx_hor_3_2 : REAL; rx_hor_3_3 : REAL; rx_hor_3_4 : REAL;
    rx_hor_3_5 : REAL; rx_hor_3_6 : REAL; rx_hor_3_7 : REAL; rx_hor_3_8 : REAL;

    rx_hor_4_1 : REAL; rx_hor_4_2 : REAL; rx_hor_4_3 : REAL; rx_hor_4_4 : REAL;
    rx_hor_4_5 : REAL; rx_hor_4_6 : REAL; rx_hor_4_7 : REAL; rx_hor_4_8 : REAL;

    rx_hor_5_1 : REAL; rx_hor_5_2 : REAL; rx_hor_5_3 : REAL; rx_hor_5_4 : REAL;
    rx_hor_5_5 : REAL; rx_hor_5_6 : REAL; rx_hor_5_7 : REAL; rx_hor_5_8 : REAL;

    (* ============================================================================================================== *)
    (* 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) VOTING & DISCREPANCY TIMERS (12 CHANNELS)                                  *)
    (* ============================================================================================================== *)
    (* 1. COT Pass 1 *)
    rVoted_COT_Pass1 : REAL; bDegraded_COT_Pass1 : BOOL; tDiscrep_COT_Pass1 : REAL := 0.0; bFault_COT_P1_A : BOOL; bFault_COT_P1_B : BOOL; bFault_COT_P1_C : BOOL;
    (* 2. COT Pass 2 *)
    rVoted_COT_Pass2 : REAL; bDegraded_COT_Pass2 : BOOL; tDiscrep_COT_Pass2 : REAL := 0.0; bFault_COT_P2_A : BOOL; bFault_COT_P2_B : BOOL; bFault_COT_P2_C : BOOL;
    (* 3. COT Pass 3 *)
    rVoted_COT_Pass3 : REAL; bDegraded_COT_Pass3 : BOOL; tDiscrep_COT_Pass3 : REAL := 0.0; bFault_COT_P3_A : BOOL; bFault_COT_P3_B : BOOL; bFault_COT_P3_C : BOOL;
    (* 4. COT Pass 4 *)
    rVoted_COT_Pass4 : REAL; bDegraded_COT_Pass4 : BOOL; tDiscrep_COT_Pass4 : REAL := 0.0; bFault_COT_P4_A : BOOL; bFault_COT_P4_B : BOOL; bFault_COT_P4_C : BOOL;
    (* 5. COT Pass 5 *)
    rVoted_COT_Pass5 : REAL; bDegraded_COT_Pass5 : BOOL; tDiscrep_COT_Pass5 : REAL := 0.0; bFault_COT_P5_A : BOOL; bFault_COT_P5_B : BOOL; bFault_COT_P5_C : BOOL;
    (* 6. COT Pass 6 *)
    rVoted_COT_Pass6 : REAL; bDegraded_COT_Pass6 : BOOL; tDiscrep_COT_Pass6 : REAL := 0.0; bFault_COT_P6_A : BOOL; bFault_COT_P6_B : BOOL; bFault_COT_P6_C : BOOL;
    (* 7. COT Pass 7 *)
    rVoted_COT_Pass7 : REAL; bDegraded_COT_Pass7 : BOOL; tDiscrep_COT_Pass7 : REAL := 0.0; bFault_COT_P7_A : BOOL; bFault_COT_P7_B : BOOL; bFault_COT_P7_C : BOOL;
    (* 8. COT Pass 8 *)
    rVoted_COT_Pass8 : REAL; bDegraded_COT_Pass8 : BOOL; tDiscrep_COT_Pass8 : REAL := 0.0; bFault_COT_P8_A : BOOL; bFault_COT_P8_B : BOOL; bFault_COT_P8_C : BOOL;
    (* 9. Fuel Gas Supply Pressure *)
    bDegraded_FuelGas_Press : BOOL; tDiscrep_FuelGas_Press : REAL := 0.0; bFault_FG_A : BOOL; bFault_FG_B : BOOL; bFault_FG_C : BOOL;
    (* 10. Firebox Arch Draft Pressure *)
    bDegraded_Draft_Press : BOOL; tDiscrep_Draft_Press : REAL := 0.0; bFault_Draft_A : BOOL; bFault_Draft_B : BOOL; bFault_Draft_C : BOOL;
    (* 11. Flue Gas Stack Excess Oxygen *)
    bDegraded_FlueGas_O2 : BOOL; tDiscrep_FlueGas_O2 : REAL := 0.0; bFault_O2_A : BOOL; bFault_O2_B : BOOL; bFault_O2_C : BOOL;
    (* 12. TLE Process Outlet Temperature *)
    bDegraded_TLE_Temp : BOOL; tDiscrep_TLE_Temp : REAL := 0.0; bFault_TLE_A : BOOL; bFault_TLE_B : BOOL; bFault_TLE_C : BOOL;

    (* TMR Discrepancy Tolerances & Persistence Filters *)
    rTol_COT_TMR            : REAL := 6.0;   (* Maximum allowable spread between COT rakes [deg C] *)
    rTol_FuelGas_TMR        : REAL := 0.15;  (* Maximum allowable spread for fuel gas transmitters [bar] *)
    rTol_Draft_TMR          : REAL := 0.35;  (* Maximum allowable spread for draft transmitters [mbar] *)
    rTol_FlueGas_O2_TMR     : REAL := 0.40;  (* Maximum allowable spread for stack O2 analyzers [%] *)
    rTol_TLE_Temp_TMR       : REAL := 10.0;  (* Maximum allowable spread for TLE outlet transmitters [deg C] *)
    rFilter_Discrep_Timeout : REAL := 2.00;  (* Discrepancy timer timeout before latching degraded mode [s] *)

    (* ============================================================================================================== *)
    (* RADIANT 8-PASS COIL BALANCING CASCADE & TRIM CONTROLLERS                                                       *)
    (* ============================================================================================================== *)
    rCOT_Error_Pass1 : REAL := 0.0; rCOT_Int_Pass1 : REAL := 0.0; rTrim_Pass1 : REAL := 50.0;
    rCOT_Error_Pass2 : REAL := 0.0; rCOT_Int_Pass2 : REAL := 0.0; rTrim_Pass2 : REAL := 50.0;
    rCOT_Error_Pass3 : REAL := 0.0; rCOT_Int_Pass3 : REAL := 0.0; rTrim_Pass3 : REAL := 50.0;
    rCOT_Error_Pass4 : REAL := 0.0; rCOT_Int_Pass4 : REAL := 0.0; rTrim_Pass4 : REAL := 50.0;
    rCOT_Error_Pass5 : REAL := 0.0; rCOT_Int_Pass5 : REAL := 0.0; rTrim_Pass5 : REAL := 50.0;
    rCOT_Error_Pass6 : REAL := 0.0; rCOT_Int_Pass6 : REAL := 0.0; rTrim_Pass6 : REAL := 50.0;
    rCOT_Error_Pass7 : REAL := 0.0; rCOT_Int_Pass7 : REAL := 0.0; rTrim_Pass7 : REAL := 50.0;
    rCOT_Error_Pass8 : REAL := 0.0; rCOT_Int_Pass8 : REAL := 0.0; rTrim_Pass8 : REAL := 50.0;

    rKp_CoilTrim : REAL := 0.45;    (* Proportional gain for coil trim [ % / deg C ] *)
    rKi_CoilTrim : REAL := 0.025;   (* Integral gain for coil trim [ % / (deg C * s) ] *)
    rMaxTrim_Clamp : REAL := 20.0;  (* Maximum trim deviation clamp (+/- 20 %) [%] *)

    (* Dynamic Cross-Limiting Cascade Variables *)
    rHC_LeadLag_Filtered : REAL := 35.0; (* Filtered HC mass rate for steam lead [t/h] *)
    rSteam_Permitted_HC_Max : REAL := 35.0; (* Dynamic permissible HC flow based on actual steam [t/h] *)
    rHC_Demanded_Steam_Min : REAL := 12.25; (* Dynamic minimum steam flow based on actual HC [t/h] *)

    (* ============================================================================================================== *)
    (* FIRST-PRINCIPLES COKING KINETICS & RADIAL HEAT TRANSFER OBSERVER                                                *)
    (* Sundaram-Froment rate law: r_coke = k_coke * exp(-Ea / (R * TMT)) * P_HC^1.2                                   *)
    (* ============================================================================================================== *)
    rGas_Constant_R         : REAL := 8.314;    (* Universal gas constant [J / (mol * K)] *)
    rEa_Coking              : REAL := 215000.0; (* Activation energy for pyrolytic coking [J / mol] *)
    rk_coke_preexp          : REAL := 1.85E7;   (* Arrhenius pre-exponential factor [mm / (h * bar^1.2)] *)
    rThermalCond_Metal      : REAL := 28.5;     (* HP-40 Nb alloy thermal conductivity [W / (m * K)] *)
    rThermalCond_Coke       : REAL := 4.2;      (* Pyrolytic carbon coke thermal conductivity [W / (m * K)] *)
    rTube_Wall_Thickness    : REAL := 0.0085;   (* Radiant tube wall thickness [m] (8.5 mm) *)
    rTube_Inner_Diameter    : REAL := 0.0650;   (* Radiant tube clean inner diameter [m] (65.0 mm) *)
    rHeatFlux_RadiantBox    : REAL := 82500.0;  (* Mean firebox radiant heat flux [W / m2] *)
    rInternalCoke_mm_Acc    : REAL := 0.85;     (* Accumulated internal coke layer thickness [mm] *)
    rCokeGrowthRate_mm_h    : REAL := 0.0000;   (* Instantaneous coke layer growth rate [mm / h] *)

    (* First-Principles Kinetic Pyrolysis Severity & Olefin Yield Observer *)
    rEthane_Conv_Fraction   : REAL := 0.650;    (* Fractional conversion of ethane feed [-] *)
    rKinetic_Rate_k_crack   : REAL := 0.0;      (* Reaction rate coefficient [1 / s] *)
    rResidence_Time_s       : REAL := 0.185;    (* Hydrocarbon residence time inside radiant coils [s] *)

    (* ============================================================================================================== *)
    (* DETERMINISTIC 14-STAGE PRODUCTION FINITE STATE MACHINE (FSM) ENUMERATION & TIMERS                               *)
    (* ============================================================================================================== *)
    (* Operational State Constants *)
    STATE_0_INIT_SAFE_STANDBY          : INT := 0;
    STATE_1_NITROGEN_PURGE             : INT := 1;
    STATE_2_PILOT_GAS_IGNITION         : INT := 2;
    STATE_3_REFRACTORY_WARMUP          : INT := 3;
    STATE_4_DILUTION_STEAM_CIRC        : INT := 4;
    STATE_5_HYDROCARBON_FEED_CUTIN     : INT := 5;
    STATE_6_RADIANT_PASS_BALANCING     : INT := 6;
    STATE_7_NORMAL_CRACKING_MPC        : INT := 7;
    STATE_8_HIGH_SEVERITY_OPERATION    : INT := 8;
    STATE_9_COKING_SURVEILLANCE        : INT := 9;
    STATE_10_DECOKING_STEAM_AIR_BURN   : INT := 10;
    STATE_11_CONTROLLED_HOT_IDLE       : INT := 11;
    STATE_12_EMERGENCY_AFT_FAST_CUTOFF : INT := 12;
    STATE_13_SHUTDOWN_COOLDOWN         : INT := 13;

    nState          : INT := 0;     (* Current active FSM state [-] *)
    nState_Prev     : INT := -1;    (* Previous cycle FSM state [-] *)
    tStateTimer     : REAL := 0.0;  (* Time spent in active state [s] *)
    tPurgeTimer     : REAL := 0.0;  (* Firebox 4-volume N2 purge accumulation timer [s] *)
    tWarmupRampTimer: REAL := 0.0;  (* Refractory stress ramp timer [s] *)
    rWarmup_Target_COT : REAL := 200.0; (* Progressive refractory warmup COT target [deg C] *)
    tDecokeTimer    : REAL := 0.0;  (* Decoking duration timer [s] *)

    (* ============================================================================================================== *)
    (* ISA-18.2 MULTI-TIERED ALARM ENGINE & TRIP LOGIC (16 CHANNELS)                                                   *)
    (* ============================================================================================================== *)
    (* Channel 1: COT Average High-High (HH), High (H), Low (L), Low-Low (LL) *)
    bTrip_COT_HH : BOOL; bWarn_COT_H : BOOL; bWarn_COT_L : BOOL; bTrip_COT_LL : BOOL;
    (* Channel 2: Peak Tube Metal Temperature (TMT) HH, H *)
    bTrip_TMT_HH : BOOL; bWarn_TMT_H : BOOL;
    (* Channel 3: Firebox Arch Draft Pressure HH, H, L, LL *)
    bTrip_Draft_HH : BOOL; bWarn_Draft_H : BOOL; bWarn_Draft_L : BOOL; bTrip_Draft_LL : BOOL;
    (* Channel 4: Fuel Gas Supply Pressure HH, H, L, LL *)
    bTrip_FuelGas_HH : BOOL; bWarn_FuelGas_H : BOOL; bWarn_FuelGas_L : BOOL; bTrip_FuelGas_LL : BOOL;
    (* Channel 5: Flue Gas Excess Oxygen HH, H, L, LL *)
    bTrip_StackO2_HH : BOOL; bWarn_StackO2_H : BOOL; bWarn_StackO2_L : BOOL; bTrip_StackO2_LL : BOOL;
    (* Channel 6: TLE Process Gas Outlet Temperature HH, H, L, LL *)
    bTrip_TLE_HH : BOOL; bWarn_TLE_H : BOOL; bWarn_TLE_L : BOOL; bTrip_TLE_LL : BOOL;
    (* Channel 7: Total Hydrocarbon Feed Flow Deviation HH, LL *)
    bTrip_FeedFlow_HH : BOOL; bTrip_FeedFlow_LL : BOOL;
    (* Channel 8: Dilution Steam Ratio Low (L), Low-Low (LL) *)
    bWarn_DSRatio_L : BOOL; bTrip_DSRatio_LL : BOOL;
    (* Channel 9: Stack Carbon Monoxide (CO) HH, H *)
    bTrip_StackCO_HH : BOOL; bWarn_StackCO_H : BOOL;
    (* Channel 10: TLE Saturated Steam Drum Operating Pressure HH, LL *)
    bTrip_SteamDrum_HH : BOOL; bTrip_SteamDrum_LL : BOOL;
    (* Channel 11: Pass-to-Pass COT Maldistribution Spread HH, H *)
    bTrip_PassSpread_HH : BOOL; bWarn_PassSpread_H : BOOL;
    (* Channel 12: Radiant Tube Coking Resistance & Rate-of-Change HH, H *)
    bTrip_CokeLimit_HH : BOOL; bWarn_CokeLimit_H : BOOL;
    (* Channel 13: Flue Gas NOx Concentration High Warning *)
    bWarn_StackNOx_H : BOOL;
    (* Channel 14: TLE Quench Oil Flow Low Warning & Trip *)
    bWarn_QuenchOil_L : BOOL; bTrip_QuenchOil_LL : BOOL;
    (* Channel 15: ID Fan Speed Saturation Warning *)
    bWarn_IDFan_Saturation : BOOL;
    (* Channel 16: Sensor TMR Triplet Discrepancy Active Warning *)
    bWarn_SensorTMR_Discrepancy : BOOL;

    (* ISA-18.2 Deadbands & Prioritization *)
    rCOT_Deadband       : REAL := 2.50; (* Deadband for COT alarms [deg C] *)
    rTMT_Deadband       : REAL := 3.00; (* Deadband for TMT alarms [deg C] *)
    rDraft_Deadband     : REAL := 0.15; (* Deadband for draft alarms [mbar] *)
    rFuelGas_Deadband   : REAL := 0.08; (* Deadband for fuel gas alarms [bar] *)
    rO2_Deadband        : REAL := 0.20; (* Deadband for oxygen alarms [%] *)
    rTLE_Deadband       : REAL := 4.00; (* Deadband for TLE temperature [deg C] *)
    rDSRatio_Deadband   : REAL := 0.015;(* Deadband for steam ratio [kg/kg] *)

    (* Unacknowledged Alarm Latches *)
    bUnack_Trip_COT_HH      : BOOL := FALSE;
    bUnack_Trip_TMT_HH      : BOOL := FALSE;
    bUnack_Trip_Draft_HH    : BOOL := FALSE;
    bUnack_Trip_FuelGas_HH  : BOOL := FALSE;
    bUnack_Trip_DSRatio_LL  : BOOL := FALSE;
    bUnack_Trip_StackCO_HH  : BOOL := FALSE;

    (* Internal Computation Temporary Floats & Counters *)
    rTempMin    : REAL;
    rTempMax    : REAL;
    rTempDiff   : REAL;
    rCycle_s    : REAL;
    nLoopIdx    : INT;
END_VAR
""")

    # Implementation Start
    parts.append("""
(* === CYBER-PHYSICAL EXECUTION INITIALIZATION & SCAN TIME RESOLUTION === *)
rCycle_s := TIME_TO_REAL(tCycleTime) / 1000.0;
IF rCycle_s < 0.001 THEN
    rCycle_s := 0.020; (* Fallback default 20 ms scan cycle *)
END_IF;


(* ================================================================================================================== *)
(* === PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING WITH DISCREPANCY TIMERS & BUMPLESS DEGRADATION === *)
(* ================================================================================================================== *)
bWarn_SensorTMR_Discrepancy := FALSE;

(* --- CHANNEL 1: COIL 1 OUTLET TEMPERATURE (COT 1) 2oo3 VOTING --- *)
bFault_COT_P1_A := (rCoilOutletTemp_Pass1_A < 50.0) OR (rCoilOutletTemp_Pass1_A > 1150.0);
bFault_COT_P1_B := (rCoilOutletTemp_Pass1_B < 50.0) OR (rCoilOutletTemp_Pass1_B > 1150.0);
bFault_COT_P1_C := (rCoilOutletTemp_Pass1_C < 50.0) OR (rCoilOutletTemp_Pass1_C > 1150.0);

IF (NOT bFault_COT_P1_A) AND (NOT bFault_COT_P1_B) AND (NOT bFault_COT_P1_C) THEN
    (* Check pairwise transmitter deviations *)
    IF (ABS(rCoilOutletTemp_Pass1_A - rCoilOutletTemp_Pass1_B) > rTol_COT_TMR) OR
       (ABS(rCoilOutletTemp_Pass1_B - rCoilOutletTemp_Pass1_C) > rTol_COT_TMR) OR
       (ABS(rCoilOutletTemp_Pass1_C - rCoilOutletTemp_Pass1_A) > rTol_COT_TMR) THEN
        tDiscrep_COT_Pass1 := tDiscrep_COT_Pass1 + rCycle_s;
    ELSE
        IF tDiscrep_COT_Pass1 > 0.0 THEN
            tDiscrep_COT_Pass1 := tDiscrep_COT_Pass1 - (rCycle_s * 2.0);
            IF tDiscrep_COT_Pass1 < 0.0 THEN tDiscrep_COT_Pass1 := 0.0; END_IF;
        END_IF;
    END_IF;

    IF tDiscrep_COT_Pass1 > rFilter_Discrep_Timeout THEN
        bDegraded_COT_Pass1 := TRUE;
        bWarn_SensorTMR_Discrepancy := TRUE;
    ELSE
        bDegraded_COT_Pass1 := FALSE;
    END_IF;

    (* Median 2oo3 voting logic *)
    IF ((rCoilOutletTemp_Pass1_A >= rCoilOutletTemp_Pass1_B) AND (rCoilOutletTemp_Pass1_A <= rCoilOutletTemp_Pass1_C)) OR
       ((rCoilOutletTemp_Pass1_A >= rCoilOutletTemp_Pass1_C) AND (rCoilOutletTemp_Pass1_A <= rCoilOutletTemp_Pass1_B)) THEN
        rVoted_COT_Pass1 := rCoilOutletTemp_Pass1_A;
    ELSIF ((rCoilOutletTemp_Pass1_B >= rCoilOutletTemp_Pass1_A) AND (rCoilOutletTemp_Pass1_B <= rCoilOutletTemp_Pass1_C)) OR
          ((rCoilOutletTemp_Pass1_B >= rCoilOutletTemp_Pass1_C) AND (rCoilOutletTemp_Pass1_B <= rCoilOutletTemp_Pass1_A)) THEN
        rVoted_COT_Pass1 := rCoilOutletTemp_Pass1_B;
    ELSE
        rVoted_COT_Pass1 := rCoilOutletTemp_Pass1_C;
    END_IF;
ELSIF (NOT bFault_COT_P1_A) AND (NOT bFault_COT_P1_B) THEN
    (* Degraded 2oo2 mean between A and B *)
    rVoted_COT_Pass1 := (rCoilOutletTemp_Pass1_A + rCoilOutletTemp_Pass1_B) * 0.50;
    bDegraded_COT_Pass1 := TRUE;
    bWarn_SensorTMR_Discrepancy := TRUE;
ELSIF (NOT bFault_COT_P1_B) AND (NOT bFault_COT_P1_C) THEN
    (* Degraded 2oo2 mean between B and C *)
    rVoted_COT_Pass1 := (rCoilOutletTemp_Pass1_B + rCoilOutletTemp_Pass1_C) * 0.50;
    bDegraded_COT_Pass1 := TRUE;
    bWarn_SensorTMR_Discrepancy := TRUE;
ELSIF (NOT bFault_COT_P1_A) AND (NOT bFault_COT_P1_C) THEN
    (* Degraded 2oo2 mean between A and C *)
    rVoted_COT_Pass1 := (rCoilOutletTemp_Pass1_A + rCoilOutletTemp_Pass1_C) * 0.50;
    bDegraded_COT_Pass1 := TRUE;
    bWarn_SensorTMR_Discrepancy := TRUE;
ELSIF (NOT bFault_COT_P1_A) THEN
    (* Degraded 1oo1 single channel A *)
    rVoted_COT_Pass1 := rCoilOutletTemp_Pass1_A;
    bDegraded_COT_Pass1 := TRUE;
    bWarn_SensorTMR_Discrepancy := TRUE;
ELSIF (NOT bFault_COT_P1_B) THEN
    rVoted_COT_Pass1 := rCoilOutletTemp_Pass1_B;
    bDegraded_COT_Pass1 := TRUE;
    bWarn_SensorTMR_Discrepancy := TRUE;
ELSIF (NOT bFault_COT_P1_C) THEN
    rVoted_COT_Pass1 := rCoilOutletTemp_Pass1_C;
    bDegraded_COT_Pass1 := TRUE;
    bWarn_SensorTMR_Discrepancy := TRUE;
ELSE
    (* All channels faulted - Freeze at safe nominal *)
    rVoted_COT_Pass1 := 845.0;
    bDegraded_COT_Pass1 := TRUE;
    bWarn_SensorTMR_Discrepancy := TRUE;
END_IF;

(* --- CHANNEL 2: COIL 2 OUTLET TEMPERATURE (COT 2) 2oo3 VOTING --- *)
bFault_COT_P2_A := (rCoilOutletTemp_Pass2_A < 50.0) OR (rCoilOutletTemp_Pass2_A > 1150.0);
bFault_COT_P2_B := (rCoilOutletTemp_Pass2_B < 50.0) OR (rCoilOutletTemp_Pass2_B > 1150.0);
bFault_COT_P2_C := (rCoilOutletTemp_Pass2_C < 50.0) OR (rCoilOutletTemp_Pass2_C > 1150.0);

IF (NOT bFault_COT_P2_A) AND (NOT bFault_COT_P2_B) AND (NOT bFault_COT_P2_C) THEN
    IF (ABS(rCoilOutletTemp_Pass2_A - rCoilOutletTemp_Pass2_B) > rTol_COT_TMR) OR
       (ABS(rCoilOutletTemp_Pass2_B - rCoilOutletTemp_Pass2_C) > rTol_COT_TMR) OR
       (ABS(rCoilOutletTemp_Pass2_C - rCoilOutletTemp_Pass2_A) > rTol_COT_TMR) THEN
        tDiscrep_COT_Pass2 := tDiscrep_COT_Pass2 + rCycle_s;
    ELSE
        IF tDiscrep_COT_Pass2 > 0.0 THEN
            tDiscrep_COT_Pass2 := tDiscrep_COT_Pass2 - (rCycle_s * 2.0);
            IF tDiscrep_COT_Pass2 < 0.0 THEN tDiscrep_COT_Pass2 := 0.0; END_IF;
        END_IF;
    END_IF;
    IF tDiscrep_COT_Pass2 > rFilter_Discrep_Timeout THEN
        bDegraded_COT_Pass2 := TRUE;
        bWarn_SensorTMR_Discrepancy := TRUE;
    ELSE
        bDegraded_COT_Pass2 := FALSE;
    END_IF;

    IF ((rCoilOutletTemp_Pass2_A >= rCoilOutletTemp_Pass2_B) AND (rCoilOutletTemp_Pass2_A <= rCoilOutletTemp_Pass2_C)) OR
       ((rCoilOutletTemp_Pass2_A >= rCoilOutletTemp_Pass2_C) AND (rCoilOutletTemp_Pass2_A <= rCoilOutletTemp_Pass2_B)) THEN
        rVoted_COT_Pass2 := rCoilOutletTemp_Pass2_A;
    ELSIF ((rCoilOutletTemp_Pass2_B >= rCoilOutletTemp_Pass2_A) AND (rCoilOutletTemp_Pass2_B <= rCoilOutletTemp_Pass2_C)) OR
          ((rCoilOutletTemp_Pass2_B >= rCoilOutletTemp_Pass2_C) AND (rCoilOutletTemp_Pass2_B <= rCoilOutletTemp_Pass2_A)) THEN
        rVoted_COT_Pass2 := rCoilOutletTemp_Pass2_B;
    ELSE
        rVoted_COT_Pass2 := rCoilOutletTemp_Pass2_C;
    END_IF;
ELSIF (NOT bFault_COT_P2_A) AND (NOT bFault_COT_P2_B) THEN
    rVoted_COT_Pass2 := (rCoilOutletTemp_Pass2_A + rCoilOutletTemp_Pass2_B) * 0.50;
    bDegraded_COT_Pass2 := TRUE;
    bWarn_SensorTMR_Discrepancy := TRUE;
ELSIF (NOT bFault_COT_P2_B) AND (NOT bFault_COT_P2_C) THEN
    rVoted_COT_Pass2 := (rCoilOutletTemp_Pass2_B + rCoilOutletTemp_Pass2_C) * 0.50;
    bDegraded_COT_Pass2 := TRUE;
    bWarn_SensorTMR_Discrepancy := TRUE;
ELSIF (NOT bFault_COT_P2_A) AND (NOT bFault_COT_P2_C) THEN
    rVoted_COT_Pass2 := (rCoilOutletTemp_Pass2_A + rCoilOutletTemp_Pass2_C) * 0.50;
    bDegraded_COT_Pass2 := TRUE;
    bWarn_SensorTMR_Discrepancy := TRUE;
ELSIF (NOT bFault_COT_P2_A) THEN
    rVoted_COT_Pass2 := rCoilOutletTemp_Pass2_A;
    bDegraded_COT_Pass2 := TRUE;
    bWarn_SensorTMR_Discrepancy := TRUE;
ELSIF (NOT bFault_COT_P2_B) THEN
    rVoted_COT_Pass2 := rCoilOutletTemp_Pass2_B;
    bDegraded_COT_Pass2 := TRUE;
    bWarn_SensorTMR_Discrepancy := TRUE;
ELSIF (NOT bFault_COT_P2_C) THEN
    rVoted_COT_Pass2 := rCoilOutletTemp_Pass2_C;
    bDegraded_COT_Pass2 := TRUE;
    bWarn_SensorTMR_Discrepancy := TRUE;
ELSE
    rVoted_COT_Pass2 := 845.0;
    bDegraded_COT_Pass2 := TRUE;
    bWarn_SensorTMR_Discrepancy := TRUE;
END_IF;

(* --- CHANNEL 3: COIL 3 OUTLET TEMPERATURE (COT 3) 2oo3 VOTING --- *)
bFault_COT_P3_A := (rCoilOutletTemp_Pass3_A < 50.0) OR (rCoilOutletTemp_Pass3_A > 1150.0);
bFault_COT_P3_B := (rCoilOutletTemp_Pass3_B < 50.0) OR (rCoilOutletTemp_Pass3_B > 1150.0);
bFault_COT_P3_C := (rCoilOutletTemp_Pass3_C < 50.0) OR (rCoilOutletTemp_Pass3_C > 1150.0);

IF (NOT bFault_COT_P3_A) AND (NOT bFault_COT_P3_B) AND (NOT bFault_COT_P3_C) THEN
    IF (ABS(rCoilOutletTemp_Pass3_A - rCoilOutletTemp_Pass3_B) > rTol_COT_TMR) OR
       (ABS(rCoilOutletTemp_Pass3_B - rCoilOutletTemp_Pass3_C) > rTol_COT_TMR) OR
       (ABS(rCoilOutletTemp_Pass3_C - rCoilOutletTemp_Pass3_A) > rTol_COT_TMR) THEN
        tDiscrep_COT_Pass3 := tDiscrep_COT_Pass3 + rCycle_s;
    ELSE
        IF tDiscrep_COT_Pass3 > 0.0 THEN
            tDiscrep_COT_Pass3 := tDiscrep_COT_Pass3 - (rCycle_s * 2.0);
            IF tDiscrep_COT_Pass3 < 0.0 THEN tDiscrep_COT_Pass3 := 0.0; END_IF;
        END_IF;
    END_IF;
    IF tDiscrep_COT_Pass3 > rFilter_Discrep_Timeout THEN
        bDegraded_COT_Pass3 := TRUE;
        bWarn_SensorTMR_Discrepancy := TRUE;
    ELSE
        bDegraded_COT_Pass3 := FALSE;
    END_IF;

    IF ((rCoilOutletTemp_Pass3_A >= rCoilOutletTemp_Pass3_B) AND (rCoilOutletTemp_Pass3_A <= rCoilOutletTemp_Pass3_C)) OR
       ((rCoilOutletTemp_Pass3_A >= rCoilOutletTemp_Pass3_C) AND (rCoilOutletTemp_Pass3_A <= rCoilOutletTemp_Pass3_B)) THEN
        rVoted_COT_Pass3 := rCoilOutletTemp_Pass3_A;
    ELSIF ((rCoilOutletTemp_Pass3_B >= rCoilOutletTemp_Pass3_A) AND (rCoilOutletTemp_Pass3_B <= rCoilOutletTemp_Pass3_C)) OR
          ((rCoilOutletTemp_Pass3_B >= rCoilOutletTemp_Pass3_C) AND (rCoilOutletTemp_Pass3_B <= rCoilOutletTemp_Pass3_A)) THEN
        rVoted_COT_Pass3 := rCoilOutletTemp_Pass3_B;
    ELSE
        rVoted_COT_Pass3 := rCoilOutletTemp_Pass3_C;
    END_IF;
ELSIF (NOT bFault_COT_P3_A) AND (NOT bFault_COT_P3_B) THEN
    rVoted_COT_Pass3 := (rCoilOutletTemp_Pass3_A + rCoilOutletTemp_Pass3_B) * 0.50;
    bDegraded_COT_Pass3 := TRUE;
ELSIF (NOT bFault_COT_P3_B) AND (NOT bFault_COT_P3_C) THEN
    rVoted_COT_Pass3 := (rCoilOutletTemp_Pass3_B + rCoilOutletTemp_Pass3_C) * 0.50;
    bDegraded_COT_Pass3 := TRUE;
ELSIF (NOT bFault_COT_P3_A) AND (NOT bFault_COT_P3_C) THEN
    rVoted_COT_Pass3 := (rCoilOutletTemp_Pass3_A + rCoilOutletTemp_Pass3_C) * 0.50;
    bDegraded_COT_Pass3 := TRUE;
ELSIF (NOT bFault_COT_P3_A) THEN
    rVoted_COT_Pass3 := rCoilOutletTemp_Pass3_A;
    bDegraded_COT_Pass3 := TRUE;
ELSIF (NOT bFault_COT_P3_B) THEN
    rVoted_COT_Pass3 := rCoilOutletTemp_Pass3_B;
    bDegraded_COT_Pass3 := TRUE;
ELSIF (NOT bFault_COT_P3_C) THEN
    rVoted_COT_Pass3 := rCoilOutletTemp_Pass3_C;
    bDegraded_COT_Pass3 := TRUE;
ELSE
    rVoted_COT_Pass3 := 845.0;
    bDegraded_COT_Pass3 := TRUE;
END_IF;

(* --- CHANNEL 4: COIL 4 OUTLET TEMPERATURE (COT 4) 2oo3 VOTING --- *)
bFault_COT_P4_A := (rCoilOutletTemp_Pass4_A < 50.0) OR (rCoilOutletTemp_Pass4_A > 1150.0);
bFault_COT_P4_B := (rCoilOutletTemp_Pass4_B < 50.0) OR (rCoilOutletTemp_Pass4_B > 1150.0);
bFault_COT_P4_C := (rCoilOutletTemp_Pass4_C < 50.0) OR (rCoilOutletTemp_Pass4_C > 1150.0);

IF (NOT bFault_COT_P4_A) AND (NOT bFault_COT_P4_B) AND (NOT bFault_COT_P4_C) THEN
    IF (ABS(rCoilOutletTemp_Pass4_A - rCoilOutletTemp_Pass4_B) > rTol_COT_TMR) OR
       (ABS(rCoilOutletTemp_Pass4_B - rCoilOutletTemp_Pass4_C) > rTol_COT_TMR) OR
       (ABS(rCoilOutletTemp_Pass4_C - rCoilOutletTemp_Pass4_A) > rTol_COT_TMR) THEN
        tDiscrep_COT_Pass4 := tDiscrep_COT_Pass4 + rCycle_s;
    ELSE
        IF tDiscrep_COT_Pass4 > 0.0 THEN
            tDiscrep_COT_Pass4 := tDiscrep_COT_Pass4 - (rCycle_s * 2.0);
            IF tDiscrep_COT_Pass4 < 0.0 THEN tDiscrep_COT_Pass4 := 0.0; END_IF;
        END_IF;
    END_IF;
    IF tDiscrep_COT_Pass4 > rFilter_Discrep_Timeout THEN
        bDegraded_COT_Pass4 := TRUE;
        bWarn_SensorTMR_Discrepancy := TRUE;
    ELSE
        bDegraded_COT_Pass4 := FALSE;
    END_IF;

    IF ((rCoilOutletTemp_Pass4_A >= rCoilOutletTemp_Pass4_B) AND (rCoilOutletTemp_Pass4_A <= rCoilOutletTemp_Pass4_C)) OR
       ((rCoilOutletTemp_Pass4_A >= rCoilOutletTemp_Pass4_C) AND (rCoilOutletTemp_Pass4_A <= rCoilOutletTemp_Pass4_B)) THEN
        rVoted_COT_Pass4 := rCoilOutletTemp_Pass4_A;
    ELSIF ((rCoilOutletTemp_Pass4_B >= rCoilOutletTemp_Pass4_A) AND (rCoilOutletTemp_Pass4_B <= rCoilOutletTemp_Pass4_C)) OR
          ((rCoilOutletTemp_Pass4_B >= rCoilOutletTemp_Pass4_C) AND (rCoilOutletTemp_Pass4_B <= rCoilOutletTemp_Pass4_A)) THEN
        rVoted_COT_Pass4 := rCoilOutletTemp_Pass4_B;
    ELSE
        rVoted_COT_Pass4 := rCoilOutletTemp_Pass4_C;
    END_IF;
ELSIF (NOT bFault_COT_P4_A) AND (NOT bFault_COT_P4_B) THEN
    rVoted_COT_Pass4 := (rCoilOutletTemp_Pass4_A + rCoilOutletTemp_Pass4_B) * 0.50;
    bDegraded_COT_Pass4 := TRUE;
ELSIF (NOT bFault_COT_P4_B) AND (NOT bFault_COT_P4_C) THEN
    rVoted_COT_Pass4 := (rCoilOutletTemp_Pass4_B + rCoilOutletTemp_Pass4_C) * 0.50;
    bDegraded_COT_Pass4 := TRUE;
ELSIF (NOT bFault_COT_P4_A) AND (NOT bFault_COT_P4_C) THEN
    rVoted_COT_Pass4 := (rCoilOutletTemp_Pass4_A + rCoilOutletTemp_Pass4_C) * 0.50;
    bDegraded_COT_Pass4 := TRUE;
ELSIF (NOT bFault_COT_P4_A) THEN
    rVoted_COT_Pass4 := rCoilOutletTemp_Pass4_A;
    bDegraded_COT_Pass4 := TRUE;
ELSIF (NOT bFault_COT_P4_B) THEN
    rVoted_COT_Pass4 := rCoilOutletTemp_Pass4_B;
    bDegraded_COT_Pass4 := TRUE;
ELSIF (NOT bFault_COT_P4_C) THEN
    rVoted_COT_Pass4 := rCoilOutletTemp_Pass4_C;
    bDegraded_COT_Pass4 := TRUE;
ELSE
    rVoted_COT_Pass4 := 845.0;
    bDegraded_COT_Pass4 := TRUE;
END_IF;

(* --- CHANNEL 5: COIL 5 OUTLET TEMPERATURE (COT 5) 2oo3 VOTING --- *)
bFault_COT_P5_A := (rCoilOutletTemp_Pass5_A < 50.0) OR (rCoilOutletTemp_Pass5_A > 1150.0);
bFault_COT_P5_B := (rCoilOutletTemp_Pass5_B < 50.0) OR (rCoilOutletTemp_Pass5_B > 1150.0);
bFault_COT_P5_C := (rCoilOutletTemp_Pass5_C < 50.0) OR (rCoilOutletTemp_Pass5_C > 1150.0);

IF (NOT bFault_COT_P5_A) AND (NOT bFault_COT_P5_B) AND (NOT bFault_COT_P5_C) THEN
    IF (ABS(rCoilOutletTemp_Pass5_A - rCoilOutletTemp_Pass5_B) > rTol_COT_TMR) OR
       (ABS(rCoilOutletTemp_Pass5_B - rCoilOutletTemp_Pass5_C) > rTol_COT_TMR) OR
       (ABS(rCoilOutletTemp_Pass5_C - rCoilOutletTemp_Pass5_A) > rTol_COT_TMR) THEN
        tDiscrep_COT_Pass5 := tDiscrep_COT_Pass5 + rCycle_s;
    ELSE
        IF tDiscrep_COT_Pass5 > 0.0 THEN
            tDiscrep_COT_Pass5 := tDiscrep_COT_Pass5 - (rCycle_s * 2.0);
            IF tDiscrep_COT_Pass5 < 0.0 THEN tDiscrep_COT_Pass5 := 0.0; END_IF;
        END_IF;
    END_IF;
    IF tDiscrep_COT_Pass5 > rFilter_Discrep_Timeout THEN
        bDegraded_COT_Pass5 := TRUE;
        bWarn_SensorTMR_Discrepancy := TRUE;
    ELSE
        bDegraded_COT_Pass5 := FALSE;
    END_IF;

    IF ((rCoilOutletTemp_Pass5_A >= rCoilOutletTemp_Pass5_B) AND (rCoilOutletTemp_Pass5_A <= rCoilOutletTemp_Pass5_C)) OR
       ((rCoilOutletTemp_Pass5_A >= rCoilOutletTemp_Pass5_C) AND (rCoilOutletTemp_Pass5_A <= rCoilOutletTemp_Pass5_B)) THEN
        rVoted_COT_Pass5 := rCoilOutletTemp_Pass5_A;
    ELSIF ((rCoilOutletTemp_Pass5_B >= rCoilOutletTemp_Pass5_A) AND (rCoilOutletTemp_Pass5_B <= rCoilOutletTemp_Pass5_C)) OR
          ((rCoilOutletTemp_Pass5_B >= rCoilOutletTemp_Pass5_C) AND (rCoilOutletTemp_Pass5_B <= rCoilOutletTemp_Pass5_A)) THEN
        rVoted_COT_Pass5 := rCoilOutletTemp_Pass5_B;
    ELSE
        rVoted_COT_Pass5 := rCoilOutletTemp_Pass5_C;
    END_IF;
ELSIF (NOT bFault_COT_P5_A) AND (NOT bFault_COT_P5_B) THEN
    rVoted_COT_Pass5 := (rCoilOutletTemp_Pass5_A + rCoilOutletTemp_Pass5_B) * 0.50;
    bDegraded_COT_Pass5 := TRUE;
ELSIF (NOT bFault_COT_P5_B) AND (NOT bFault_COT_P5_C) THEN
    rVoted_COT_Pass5 := (rCoilOutletTemp_Pass5_B + rCoilOutletTemp_Pass5_C) * 0.50;
    bDegraded_COT_Pass5 := TRUE;
ELSIF (NOT bFault_COT_P5_A) AND (NOT bFault_COT_P5_C) THEN
    rVoted_COT_Pass5 := (rCoilOutletTemp_Pass5_A + rCoilOutletTemp_Pass5_C) * 0.50;
    bDegraded_COT_Pass5 := TRUE;
ELSIF (NOT bFault_COT_P5_A) THEN
    rVoted_COT_Pass5 := rCoilOutletTemp_Pass5_A;
    bDegraded_COT_Pass5 := TRUE;
ELSIF (NOT bFault_COT_P5_B) THEN
    rVoted_COT_Pass5 := rCoilOutletTemp_Pass5_B;
    bDegraded_COT_Pass5 := TRUE;
ELSIF (NOT bFault_COT_P5_C) THEN
    rVoted_COT_Pass5 := rCoilOutletTemp_Pass5_C;
    bDegraded_COT_Pass5 := TRUE;
ELSE
    rVoted_COT_Pass5 := 845.0;
    bDegraded_COT_Pass5 := TRUE;
END_IF;

(* --- CHANNEL 6: COIL 6 OUTLET TEMPERATURE (COT 6) 2oo3 VOTING --- *)
bFault_COT_P6_A := (rCoilOutletTemp_Pass6_A < 50.0) OR (rCoilOutletTemp_Pass6_A > 1150.0);
bFault_COT_P6_B := (rCoilOutletTemp_Pass6_B < 50.0) OR (rCoilOutletTemp_Pass6_B > 1150.0);
bFault_COT_P6_C := (rCoilOutletTemp_Pass6_C < 50.0) OR (rCoilOutletTemp_Pass6_C > 1150.0);

IF (NOT bFault_COT_P6_A) AND (NOT bFault_COT_P6_B) AND (NOT bFault_COT_P6_C) THEN
    IF (ABS(rCoilOutletTemp_Pass6_A - rCoilOutletTemp_Pass6_B) > rTol_COT_TMR) OR
       (ABS(rCoilOutletTemp_Pass6_B - rCoilOutletTemp_Pass6_C) > rTol_COT_TMR) OR
       (ABS(rCoilOutletTemp_Pass6_C - rCoilOutletTemp_Pass6_A) > rTol_COT_TMR) THEN
        tDiscrep_COT_Pass6 := tDiscrep_COT_Pass6 + rCycle_s;
    ELSE
        IF tDiscrep_COT_Pass6 > 0.0 THEN
            tDiscrep_COT_Pass6 := tDiscrep_COT_Pass6 - (rCycle_s * 2.0);
            IF tDiscrep_COT_Pass6 < 0.0 THEN tDiscrep_COT_Pass6 := 0.0; END_IF;
        END_IF;
    END_IF;
    IF tDiscrep_COT_Pass6 > rFilter_Discrep_Timeout THEN
        bDegraded_COT_Pass6 := TRUE;
        bWarn_SensorTMR_Discrepancy := TRUE;
    ELSE
        bDegraded_COT_Pass6 := FALSE;
    END_IF;

    IF ((rCoilOutletTemp_Pass6_A >= rCoilOutletTemp_Pass6_B) AND (rCoilOutletTemp_Pass6_A <= rCoilOutletTemp_Pass6_C)) OR
       ((rCoilOutletTemp_Pass6_A >= rCoilOutletTemp_Pass6_C) AND (rCoilOutletTemp_Pass6_A <= rCoilOutletTemp_Pass6_B)) THEN
        rVoted_COT_Pass6 := rCoilOutletTemp_Pass6_A;
    ELSIF ((rCoilOutletTemp_Pass6_B >= rCoilOutletTemp_Pass6_A) AND (rCoilOutletTemp_Pass6_B <= rCoilOutletTemp_Pass6_C)) OR
          ((rCoilOutletTemp_Pass6_B >= rCoilOutletTemp_Pass6_C) AND (rCoilOutletTemp_Pass6_B <= rCoilOutletTemp_Pass6_A)) THEN
        rVoted_COT_Pass6 := rCoilOutletTemp_Pass6_B;
    ELSE
        rVoted_COT_Pass6 := rCoilOutletTemp_Pass6_C;
    END_IF;
ELSIF (NOT bFault_COT_P6_A) AND (NOT bFault_COT_P6_B) THEN
    rVoted_COT_Pass6 := (rCoilOutletTemp_Pass6_A + rCoilOutletTemp_Pass6_B) * 0.50;
    bDegraded_COT_Pass6 := TRUE;
ELSIF (NOT bFault_COT_P6_B) AND (NOT bFault_COT_P6_C) THEN
    rVoted_COT_Pass6 := (rCoilOutletTemp_Pass6_B + rCoilOutletTemp_Pass6_C) * 0.50;
    bDegraded_COT_Pass6 := TRUE;
ELSIF (NOT bFault_COT_P6_A) AND (NOT bFault_COT_P6_C) THEN
    rVoted_COT_Pass6 := (rCoilOutletTemp_Pass6_A + rCoilOutletTemp_Pass6_C) * 0.50;
    bDegraded_COT_Pass6 := TRUE;
ELSIF (NOT bFault_COT_P6_A) THEN
    rVoted_COT_Pass6 := rCoilOutletTemp_Pass6_A;
    bDegraded_COT_Pass6 := TRUE;
ELSIF (NOT bFault_COT_P6_B) THEN
    rVoted_COT_Pass6 := rCoilOutletTemp_Pass6_B;
    bDegraded_COT_Pass6 := TRUE;
ELSIF (NOT bFault_COT_P6_C) THEN
    rVoted_COT_Pass6 := rCoilOutletTemp_Pass6_C;
    bDegraded_COT_Pass6 := TRUE;
ELSE
    rVoted_COT_Pass6 := 845.0;
    bDegraded_COT_Pass6 := TRUE;
END_IF;

(* --- CHANNEL 7: COIL 7 OUTLET TEMPERATURE (COT 7) 2oo3 VOTING --- *)
bFault_COT_P7_A := (rCoilOutletTemp_Pass7_A < 50.0) OR (rCoilOutletTemp_Pass7_A > 1150.0);
bFault_COT_P7_B := (rCoilOutletTemp_Pass7_B < 50.0) OR (rCoilOutletTemp_Pass7_B > 1150.0);
bFault_COT_P7_C := (rCoilOutletTemp_Pass7_C < 50.0) OR (rCoilOutletTemp_Pass7_C > 1150.0);

IF (NOT bFault_COT_P7_A) AND (NOT bFault_COT_P7_B) AND (NOT bFault_COT_P7_C) THEN
    IF (ABS(rCoilOutletTemp_Pass7_A - rCoilOutletTemp_Pass7_B) > rTol_COT_TMR) OR
       (ABS(rCoilOutletTemp_Pass7_B - rCoilOutletTemp_Pass7_C) > rTol_COT_TMR) OR
       (ABS(rCoilOutletTemp_Pass7_C - rCoilOutletTemp_Pass7_A) > rTol_COT_TMR) THEN
        tDiscrep_COT_Pass7 := tDiscrep_COT_Pass7 + rCycle_s;
    ELSE
        IF tDiscrep_COT_Pass7 > 0.0 THEN
            tDiscrep_COT_Pass7 := tDiscrep_COT_Pass7 - (rCycle_s * 2.0);
            IF tDiscrep_COT_Pass7 < 0.0 THEN tDiscrep_COT_Pass7 := 0.0; END_IF;
        END_IF;
    END_IF;
    IF tDiscrep_COT_Pass7 > rFilter_Discrep_Timeout THEN
        bDegraded_COT_Pass7 := TRUE;
        bWarn_SensorTMR_Discrepancy := TRUE;
    ELSE
        bDegraded_COT_Pass7 := FALSE;
    END_IF;

    IF ((rCoilOutletTemp_Pass7_A >= rCoilOutletTemp_Pass7_B) AND (rCoilOutletTemp_Pass7_A <= rCoilOutletTemp_Pass7_C)) OR
       ((rCoilOutletTemp_Pass7_A >= rCoilOutletTemp_Pass7_C) AND (rCoilOutletTemp_Pass7_A <= rCoilOutletTemp_Pass7_B)) THEN
        rVoted_COT_Pass7 := rCoilOutletTemp_Pass7_A;
    ELSIF ((rCoilOutletTemp_Pass7_B >= rCoilOutletTemp_Pass7_A) AND (rCoilOutletTemp_Pass7_B <= rCoilOutletTemp_Pass7_C)) OR
          ((rCoilOutletTemp_Pass7_B >= rCoilOutletTemp_Pass7_C) AND (rCoilOutletTemp_Pass7_B <= rCoilOutletTemp_Pass7_A)) THEN
        rVoted_COT_Pass7 := rCoilOutletTemp_Pass7_B;
    ELSE
        rVoted_COT_Pass7 := rCoilOutletTemp_Pass7_C;
    END_IF;
ELSIF (NOT bFault_COT_P7_A) AND (NOT bFault_COT_P7_B) THEN
    rVoted_COT_Pass7 := (rCoilOutletTemp_Pass7_A + rCoilOutletTemp_Pass7_B) * 0.50;
    bDegraded_COT_Pass7 := TRUE;
ELSIF (NOT bFault_COT_P7_B) AND (NOT bFault_COT_P7_C) THEN
    rVoted_COT_Pass7 := (rCoilOutletTemp_Pass7_B + rCoilOutletTemp_Pass7_C) * 0.50;
    bDegraded_COT_Pass7 := TRUE;
ELSIF (NOT bFault_COT_P7_A) AND (NOT bFault_COT_P7_C) THEN
    rVoted_COT_Pass7 := (rCoilOutletTemp_Pass7_A + rCoilOutletTemp_Pass7_C) * 0.50;
    bDegraded_COT_Pass7 := TRUE;
ELSIF (NOT bFault_COT_P7_A) THEN
    rVoted_COT_Pass7 := rCoilOutletTemp_Pass7_A;
    bDegraded_COT_Pass7 := TRUE;
ELSIF (NOT bFault_COT_P7_B) THEN
    rVoted_COT_Pass7 := rCoilOutletTemp_Pass7_B;
    bDegraded_COT_Pass7 := TRUE;
ELSIF (NOT bFault_COT_P7_C) THEN
    rVoted_COT_Pass7 := rCoilOutletTemp_Pass7_C;
    bDegraded_COT_Pass7 := TRUE;
ELSE
    rVoted_COT_Pass7 := 845.0;
    bDegraded_COT_Pass7 := TRUE;
END_IF;

(* --- CHANNEL 8: COIL 8 OUTLET TEMPERATURE (COT 8) 2oo3 VOTING --- *)
bFault_COT_P8_A := (rCoilOutletTemp_Pass8_A < 50.0) OR (rCoilOutletTemp_Pass8_A > 1150.0);
bFault_COT_P8_B := (rCoilOutletTemp_Pass8_B < 50.0) OR (rCoilOutletTemp_Pass8_B > 1150.0);
bFault_COT_P8_C := (rCoilOutletTemp_Pass8_C < 50.0) OR (rCoilOutletTemp_Pass8_C > 1150.0);

IF (NOT bFault_COT_P8_A) AND (NOT bFault_COT_P8_B) AND (NOT bFault_COT_P8_C) THEN
    IF (ABS(rCoilOutletTemp_Pass8_A - rCoilOutletTemp_Pass8_B) > rTol_COT_TMR) OR
       (ABS(rCoilOutletTemp_Pass8_B - rCoilOutletTemp_Pass8_C) > rTol_COT_TMR) OR
       (ABS(rCoilOutletTemp_Pass8_C - rCoilOutletTemp_Pass8_A) > rTol_COT_TMR) THEN
        tDiscrep_COT_Pass8 := tDiscrep_COT_Pass8 + rCycle_s;
    ELSE
        IF tDiscrep_COT_Pass8 > 0.0 THEN
            tDiscrep_COT_Pass8 := tDiscrep_COT_Pass8 - (rCycle_s * 2.0);
            IF tDiscrep_COT_Pass8 < 0.0 THEN tDiscrep_COT_Pass8 := 0.0; END_IF;
        END_IF;
    END_IF;
    IF tDiscrep_COT_Pass8 > rFilter_Discrep_Timeout THEN
        bDegraded_COT_Pass8 := TRUE;
        bWarn_SensorTMR_Discrepancy := TRUE;
    ELSE
        bDegraded_COT_Pass8 := FALSE;
    END_IF;

    IF ((rCoilOutletTemp_Pass8_A >= rCoilOutletTemp_Pass8_B) AND (rCoilOutletTemp_Pass8_A <= rCoilOutletTemp_Pass8_C)) OR
       ((rCoilOutletTemp_Pass8_A >= rCoilOutletTemp_Pass8_C) AND (rCoilOutletTemp_Pass8_A <= rCoilOutletTemp_Pass8_B)) THEN
        rVoted_COT_Pass8 := rCoilOutletTemp_Pass8_A;
    ELSIF ((rCoilOutletTemp_Pass8_B >= rCoilOutletTemp_Pass8_A) AND (rCoilOutletTemp_Pass8_B <= rCoilOutletTemp_Pass8_C)) OR
          ((rCoilOutletTemp_Pass8_B >= rCoilOutletTemp_Pass8_C) AND (rCoilOutletTemp_Pass8_B <= rCoilOutletTemp_Pass8_A)) THEN
        rVoted_COT_Pass8 := rCoilOutletTemp_Pass8_B;
    ELSE
        rVoted_COT_Pass8 := rCoilOutletTemp_Pass8_C;
    END_IF;
ELSIF (NOT bFault_COT_P8_A) AND (NOT bFault_COT_P8_B) THEN
    rVoted_COT_Pass8 := (rCoilOutletTemp_Pass8_A + rCoilOutletTemp_Pass8_B) * 0.50;
    bDegraded_COT_Pass8 := TRUE;
ELSIF (NOT bFault_COT_P8_B) AND (NOT bFault_COT_P8_C) THEN
    rVoted_COT_Pass8 := (rCoilOutletTemp_Pass8_B + rCoilOutletTemp_Pass8_C) * 0.50;
    bDegraded_COT_Pass8 := TRUE;
ELSIF (NOT bFault_COT_P8_A) AND (NOT bFault_COT_P8_C) THEN
    rVoted_COT_Pass8 := (rCoilOutletTemp_Pass8_A + rCoilOutletTemp_Pass8_C) * 0.50;
    bDegraded_COT_Pass8 := TRUE;
ELSIF (NOT bFault_COT_P8_A) THEN
    rVoted_COT_Pass8 := rCoilOutletTemp_Pass8_A;
    bDegraded_COT_Pass8 := TRUE;
ELSIF (NOT bFault_COT_P8_B) THEN
    rVoted_COT_Pass8 := rCoilOutletTemp_Pass8_B;
    bDegraded_COT_Pass8 := TRUE;
ELSIF (NOT bFault_COT_P8_C) THEN
    rVoted_COT_Pass8 := rCoilOutletTemp_Pass8_C;
    bDegraded_COT_Pass8 := TRUE;
ELSE
    rVoted_COT_Pass8 := 845.0;
    bDegraded_COT_Pass8 := TRUE;
END_IF;

(* Compute Voted 8-Pass Mean Coil Outlet Temperature *)
rVoted_Average_COT := (rVoted_COT_Pass1 + rVoted_COT_Pass2 + rVoted_COT_Pass3 + rVoted_COT_Pass4 +
                       rVoted_COT_Pass5 + rVoted_COT_Pass6 + rVoted_COT_Pass7 + rVoted_COT_Pass8) * 0.1250;

(* --- CHANNEL 9: FUEL GAS SUPPLY PRESSURE 2oo3 VOTING --- *)
bFault_FG_A := (rFuelGas_SupplyPressure_A < 0.10) OR (rFuelGas_SupplyPressure_A > 10.0);
bFault_FG_B := (rFuelGas_SupplyPressure_B < 0.10) OR (rFuelGas_SupplyPressure_B > 10.0);
bFault_FG_C := (rFuelGas_SupplyPressure_C < 0.10) OR (rFuelGas_SupplyPressure_C > 10.0);

IF (NOT bFault_FG_A) AND (NOT bFault_FG_B) AND (NOT bFault_FG_C) THEN
    IF (ABS(rFuelGas_SupplyPressure_A - rFuelGas_SupplyPressure_B) > rTol_FuelGas_TMR) OR
       (ABS(rFuelGas_SupplyPressure_B - rFuelGas_SupplyPressure_C) > rTol_FuelGas_TMR) OR
       (ABS(rFuelGas_SupplyPressure_C - rFuelGas_SupplyPressure_A) > rTol_FuelGas_TMR) THEN
        tDiscrep_FuelGas_Press := tDiscrep_FuelGas_Press + rCycle_s;
    ELSE
        IF tDiscrep_FuelGas_Press > 0.0 THEN
            tDiscrep_FuelGas_Press := tDiscrep_FuelGas_Press - (rCycle_s * 2.0);
            IF tDiscrep_FuelGas_Press < 0.0 THEN tDiscrep_FuelGas_Press := 0.0; END_IF;
        END_IF;
    END_IF;
    IF tDiscrep_FuelGas_Press > rFilter_Discrep_Timeout THEN
        bDegraded_FuelGas_Press := TRUE;
        bWarn_SensorTMR_Discrepancy := TRUE;
    ELSE
        bDegraded_FuelGas_Press := FALSE;
    END_IF;

    IF ((rFuelGas_SupplyPressure_A >= rFuelGas_SupplyPressure_B) AND (rFuelGas_SupplyPressure_A <= rFuelGas_SupplyPressure_C)) OR
       ((rFuelGas_SupplyPressure_A >= rFuelGas_SupplyPressure_C) AND (rFuelGas_SupplyPressure_A <= rFuelGas_SupplyPressure_B)) THEN
        rVoted_FuelGas_Pressure := rFuelGas_SupplyPressure_A;
    ELSIF ((rFuelGas_SupplyPressure_B >= rFuelGas_SupplyPressure_A) AND (rFuelGas_SupplyPressure_B <= rFuelGas_SupplyPressure_C)) OR
          ((rFuelGas_SupplyPressure_B >= rFuelGas_SupplyPressure_C) AND (rFuelGas_SupplyPressure_B <= rFuelGas_SupplyPressure_A)) THEN
        rVoted_FuelGas_Pressure := rFuelGas_SupplyPressure_B;
    ELSE
        rVoted_FuelGas_Pressure := rFuelGas_SupplyPressure_C;
    END_IF;
ELSIF (NOT bFault_FG_A) AND (NOT bFault_FG_B) THEN
    rVoted_FuelGas_Pressure := (rFuelGas_SupplyPressure_A + rFuelGas_SupplyPressure_B) * 0.50;
    bDegraded_FuelGas_Press := TRUE;
ELSIF (NOT bFault_FG_B) AND (NOT bFault_FG_C) THEN
    rVoted_FuelGas_Pressure := (rFuelGas_SupplyPressure_B + rFuelGas_SupplyPressure_C) * 0.50;
    bDegraded_FuelGas_Press := TRUE;
ELSIF (NOT bFault_FG_A) AND (NOT bFault_FG_C) THEN
    rVoted_FuelGas_Pressure := (rFuelGas_SupplyPressure_A + rFuelGas_SupplyPressure_C) * 0.50;
    bDegraded_FuelGas_Press := TRUE;
ELSIF (NOT bFault_FG_A) THEN
    rVoted_FuelGas_Pressure := rFuelGas_SupplyPressure_A;
    bDegraded_FuelGas_Press := TRUE;
ELSIF (NOT bFault_FG_B) THEN
    rVoted_FuelGas_Pressure := rFuelGas_SupplyPressure_B;
    bDegraded_FuelGas_Press := TRUE;
ELSIF (NOT bFault_FG_C) THEN
    rVoted_FuelGas_Pressure := rFuelGas_SupplyPressure_C;
    bDegraded_FuelGas_Press := TRUE;
ELSE
    rVoted_FuelGas_Pressure := 3.20;
    bDegraded_FuelGas_Press := TRUE;
END_IF;

(* --- CHANNEL 10: FIREBOX ARCH DRAFT PRESSURE 2oo3 VOTING --- *)
bFault_Draft_A := (rFirebox_DraftPressure_A < -15.0) OR (rFirebox_DraftPressure_A > 15.0);
bFault_Draft_B := (rFirebox_DraftPressure_B < -15.0) OR (rFirebox_DraftPressure_B > 15.0);
bFault_Draft_C := (rFirebox_DraftPressure_C < -15.0) OR (rFirebox_DraftPressure_C > 15.0);

IF (NOT bFault_Draft_A) AND (NOT bFault_Draft_B) AND (NOT bFault_Draft_C) THEN
    IF (ABS(rFirebox_DraftPressure_A - rFirebox_DraftPressure_B) > rTol_Draft_TMR) OR
       (ABS(rFirebox_DraftPressure_B - rFirebox_DraftPressure_C) > rTol_Draft_TMR) OR
       (ABS(rFirebox_DraftPressure_C - rFirebox_DraftPressure_A) > rTol_Draft_TMR) THEN
        tDiscrep_Draft_Press := tDiscrep_Draft_Press + rCycle_s;
    ELSE
        IF tDiscrep_Draft_Press > 0.0 THEN
            tDiscrep_Draft_Press := tDiscrep_Draft_Press - (rCycle_s * 2.0);
            IF tDiscrep_Draft_Press < 0.0 THEN tDiscrep_Draft_Press := 0.0; END_IF;
        END_IF;
    END_IF;
    IF tDiscrep_Draft_Press > rFilter_Discrep_Timeout THEN
        bDegraded_Draft_Press := TRUE;
        bWarn_SensorTMR_Discrepancy := TRUE;
    ELSE
        bDegraded_Draft_Press := FALSE;
    END_IF;

    IF ((rFirebox_DraftPressure_A >= rFirebox_DraftPressure_B) AND (rFirebox_DraftPressure_A <= rFirebox_DraftPressure_C)) OR
       ((rFirebox_DraftPressure_A >= rFirebox_DraftPressure_C) AND (rFirebox_DraftPressure_A <= rFirebox_DraftPressure_B)) THEN
        rVoted_Firebox_Draft := rFirebox_DraftPressure_A;
    ELSIF ((rFirebox_DraftPressure_B >= rFirebox_DraftPressure_A) AND (rFirebox_DraftPressure_B <= rFirebox_DraftPressure_C)) OR
          ((rFirebox_DraftPressure_B >= rFirebox_DraftPressure_C) AND (rFirebox_DraftPressure_B <= rFirebox_DraftPressure_A)) THEN
        rVoted_Firebox_Draft := rFirebox_DraftPressure_B;
    ELSE
        rVoted_Firebox_Draft := rFirebox_DraftPressure_C;
    END_IF;
ELSIF (NOT bFault_Draft_A) AND (NOT bFault_Draft_B) THEN
    rVoted_Firebox_Draft := (rFirebox_DraftPressure_A + rFirebox_DraftPressure_B) * 0.50;
    bDegraded_Draft_Press := TRUE;
ELSIF (NOT bFault_Draft_B) AND (NOT bFault_Draft_C) THEN
    rVoted_Firebox_Draft := (rFirebox_DraftPressure_B + rFirebox_DraftPressure_C) * 0.50;
    bDegraded_Draft_Press := TRUE;
ELSIF (NOT bFault_Draft_A) AND (NOT bFault_Draft_C) THEN
    rVoted_Firebox_Draft := (rFirebox_DraftPressure_A + rFirebox_DraftPressure_C) * 0.50;
    bDegraded_Draft_Press := TRUE;
ELSIF (NOT bFault_Draft_A) THEN
    rVoted_Firebox_Draft := rFirebox_DraftPressure_A;
    bDegraded_Draft_Press := TRUE;
ELSIF (NOT bFault_Draft_B) THEN
    rVoted_Firebox_Draft := rFirebox_DraftPressure_B;
    bDegraded_Draft_Press := TRUE;
ELSIF (NOT bFault_Draft_C) THEN
    rVoted_Firebox_Draft := rFirebox_DraftPressure_C;
    bDegraded_Draft_Press := TRUE;
ELSE
    rVoted_Firebox_Draft := -1.50;
    bDegraded_Draft_Press := TRUE;
END_IF;

(* --- CHANNEL 11: FLUE GAS STACK OXYGEN 2oo3 VOTING --- *)
bFault_O2_A := (rFlueGas_OxygenContent_A < 0.0) OR (rFlueGas_OxygenContent_A > 25.0);
bFault_O2_B := (rFlueGas_OxygenContent_B < 0.0) OR (rFlueGas_OxygenContent_B > 25.0);
bFault_O2_C := (rFlueGas_OxygenContent_C < 0.0) OR (rFlueGas_OxygenContent_C > 25.0);

IF (NOT bFault_O2_A) AND (NOT bFault_O2_B) AND (NOT bFault_O2_C) THEN
    IF (ABS(rFlueGas_OxygenContent_A - rFlueGas_OxygenContent_B) > rTol_FlueGas_O2_TMR) OR
       (ABS(rFlueGas_OxygenContent_B - rFlueGas_OxygenContent_C) > rTol_FlueGas_O2_TMR) OR
       (ABS(rFlueGas_OxygenContent_C - rFlueGas_OxygenContent_A) > rTol_FlueGas_O2_TMR) THEN
        tDiscrep_FlueGas_O2 := tDiscrep_FlueGas_O2 + rCycle_s;
    ELSE
        IF tDiscrep_FlueGas_O2 > 0.0 THEN
            tDiscrep_FlueGas_O2 := tDiscrep_FlueGas_O2 - (rCycle_s * 2.0);
            IF tDiscrep_FlueGas_O2 < 0.0 THEN tDiscrep_FlueGas_O2 := 0.0; END_IF;
        END_IF;
    END_IF;
    IF tDiscrep_FlueGas_O2 > rFilter_Discrep_Timeout THEN
        bDegraded_FlueGas_O2 := TRUE;
        bWarn_SensorTMR_Discrepancy := TRUE;
    ELSE
        bDegraded_FlueGas_O2 := FALSE;
    END_IF;

    IF ((rFlueGas_OxygenContent_A >= rFlueGas_OxygenContent_B) AND (rFlueGas_OxygenContent_A <= rFlueGas_OxygenContent_C)) OR
       ((rFlueGas_OxygenContent_A >= rFlueGas_OxygenContent_C) AND (rFlueGas_OxygenContent_A <= rFlueGas_OxygenContent_B)) THEN
        rVoted_FlueGas_O2 := rFlueGas_OxygenContent_A;
    ELSIF ((rFlueGas_OxygenContent_B >= rFlueGas_OxygenContent_A) AND (rFlueGas_OxygenContent_B <= rFlueGas_OxygenContent_C)) OR
          ((rFlueGas_OxygenContent_B >= rFlueGas_OxygenContent_C) AND (rFlueGas_OxygenContent_B <= rFlueGas_OxygenContent_A)) THEN
        rVoted_FlueGas_O2 := rFlueGas_OxygenContent_B;
    ELSE
        rVoted_FlueGas_O2 := rFlueGas_OxygenContent_C;
    END_IF;
ELSIF (NOT bFault_O2_A) AND (NOT bFault_O2_B) THEN
    rVoted_FlueGas_O2 := (rFlueGas_OxygenContent_A + rFlueGas_OxygenContent_B) * 0.50;
    bDegraded_FlueGas_O2 := TRUE;
ELSIF (NOT bFault_O2_B) AND (NOT bFault_O2_C) THEN
    rVoted_FlueGas_O2 := (rFlueGas_OxygenContent_B + rFlueGas_OxygenContent_C) * 0.50;
    bDegraded_FlueGas_O2 := TRUE;
ELSIF (NOT bFault_O2_A) AND (NOT bFault_O2_C) THEN
    rVoted_FlueGas_O2 := (rFlueGas_OxygenContent_A + rFlueGas_OxygenContent_C) * 0.50;
    bDegraded_FlueGas_O2 := TRUE;
ELSIF (NOT bFault_O2_A) THEN
    rVoted_FlueGas_O2 := rFlueGas_OxygenContent_A;
    bDegraded_FlueGas_O2 := TRUE;
ELSIF (NOT bFault_O2_B) THEN
    rVoted_FlueGas_O2 := rFlueGas_OxygenContent_B;
    bDegraded_FlueGas_O2 := TRUE;
ELSIF (NOT bFault_O2_C) THEN
    rVoted_FlueGas_O2 := rFlueGas_OxygenContent_C;
    bDegraded_FlueGas_O2 := TRUE;
ELSE
    rVoted_FlueGas_O2 := 2.00;
    bDegraded_FlueGas_O2 := TRUE;
END_IF;

(* --- CHANNEL 12: TLE PROCESS OUTLET TEMPERATURE 2oo3 VOTING --- *)
bFault_TLE_A := (rTLE_OutletTemperature_A < 100.0) OR (rTLE_OutletTemperature_A > 700.0);
bFault_TLE_B := (rTLE_OutletTemperature_B < 100.0) OR (rTLE_OutletTemperature_B > 700.0);
bFault_TLE_C := (rTLE_OutletTemperature_C < 100.0) OR (rTLE_OutletTemperature_C > 700.0);

IF (NOT bFault_TLE_A) AND (NOT bFault_TLE_B) AND (NOT bFault_TLE_C) THEN
    IF (ABS(rTLE_OutletTemperature_A - rTLE_OutletTemperature_B) > rTol_TLE_Temp_TMR) OR
       (ABS(rTLE_OutletTemperature_B - rTLE_OutletTemperature_C) > rTol_TLE_Temp_TMR) OR
       (ABS(rTLE_OutletTemperature_C - rTLE_OutletTemperature_A) > rTol_TLE_Temp_TMR) THEN
        tDiscrep_TLE_Temp := tDiscrep_TLE_Temp + rCycle_s;
    ELSE
        IF tDiscrep_TLE_Temp > 0.0 THEN
            tDiscrep_TLE_Temp := tDiscrep_TLE_Temp - (rCycle_s * 2.0);
            IF tDiscrep_TLE_Temp < 0.0 THEN tDiscrep_TLE_Temp := 0.0; END_IF;
        END_IF;
    END_IF;
    IF tDiscrep_TLE_Temp > rFilter_Discrep_Timeout THEN
        bDegraded_TLE_Temp := TRUE;
        bWarn_SensorTMR_Discrepancy := TRUE;
    ELSE
        bDegraded_TLE_Temp := FALSE;
    END_IF;

    IF ((rTLE_OutletTemperature_A >= rTLE_OutletTemperature_B) AND (rTLE_OutletTemperature_A <= rTLE_OutletTemperature_C)) OR
       ((rTLE_OutletTemperature_A >= rTLE_OutletTemperature_C) AND (rTLE_OutletTemperature_A <= rTLE_OutletTemperature_B)) THEN
        rVoted_TLE_OutletTemp := rTLE_OutletTemperature_A;
    ELSIF ((rTLE_OutletTemperature_B >= rTLE_OutletTemperature_A) AND (rTLE_OutletTemperature_B <= rTLE_OutletTemperature_C)) OR
          ((rTLE_OutletTemperature_B >= rTLE_OutletTemperature_C) AND (rTLE_OutletTemperature_B <= rTLE_OutletTemperature_A)) THEN
        rVoted_TLE_OutletTemp := rTLE_OutletTemperature_B;
    ELSE
        rVoted_TLE_OutletTemp := rTLE_OutletTemperature_C;
    END_IF;
ELSIF (NOT bFault_TLE_A) AND (NOT bFault_TLE_B) THEN
    rVoted_TLE_OutletTemp := (rTLE_OutletTemperature_A + rTLE_OutletTemperature_B) * 0.50;
    bDegraded_TLE_Temp := TRUE;
ELSIF (NOT bFault_TLE_B) AND (NOT bFault_TLE_C) THEN
    rVoted_TLE_OutletTemp := (rTLE_OutletTemperature_B + rTLE_OutletTemperature_C) * 0.50;
    bDegraded_TLE_Temp := TRUE;
ELSIF (NOT bFault_TLE_A) AND (NOT bFault_TLE_C) THEN
    rVoted_TLE_OutletTemp := (rTLE_OutletTemperature_A + rTLE_OutletTemperature_C) * 0.50;
    bDegraded_TLE_Temp := TRUE;
ELSIF (NOT bFault_TLE_A) THEN
    rVoted_TLE_OutletTemp := rTLE_OutletTemperature_A;
    bDegraded_TLE_Temp := TRUE;
ELSIF (NOT bFault_TLE_B) THEN
    rVoted_TLE_OutletTemp := rTLE_OutletTemperature_B;
    bDegraded_TLE_Temp := TRUE;
ELSIF (NOT bFault_TLE_C) THEN
    rVoted_TLE_OutletTemp := rTLE_OutletTemperature_C;
    bDegraded_TLE_Temp := TRUE;
ELSE
    rVoted_TLE_OutletTemp := 400.0;
    bDegraded_TLE_Temp := TRUE;
END_IF;

bTMR_Degraded_Warning := bWarn_SensorTMR_Discrepancy;
""")

    # Phase 2: State-Space estimation and Kalman Observer
    parts.append("""
(* ================================================================================================================== *)
(* === PHASE 2: FIRST-PRINCIPLES CYBER-PHYSICAL STATE-SPACE ESTIMATION & KALMAN INNOVATION ===                        *)
(* State equation: x_pred[k+1] = A * x_hat[k] + B * u[k]                                                              *)
(* Measurement equation: y[k] = C * x_hat[k] + D * u[k]                                                               *)
(* Kalman update: x_hat[k] = x_pred[k] + L * (y_meas[k] - C * x_pred[k])                                             *)
(* ================================================================================================================== *)

(* 1. Compute Operating Dilution Steam Mass Ratio *)
IF rHydrocarbonFeed_MassFlow_Total > 1.0 THEN
    rCalculated_DS_Ratio := rDilutionSteam_MassFlow_Total / rHydrocarbonFeed_MassFlow_Total;
ELSE
    rCalculated_DS_Ratio := 0.350;
END_IF;

(* 2. Formulate Measurement Innovation Residuals (y_meas - C * x_pred) *)
re_innov_1 := (rVoted_Average_COT - 845.0) - (rC_11*rx_pred_1 + rC_12*rx_pred_2 + rC_13*rx_pred_3 + rC_14*rx_pred_4 + rC_15*rx_pred_5 + rC_16*rx_pred_6 + rC_17*rx_pred_7 + rC_18*rx_pred_8);
re_innov_2 := (rVoted_Firebox_Draft - (-1.50)) - (rC_21*rx_pred_1 + rC_22*rx_pred_2 + rC_23*rx_pred_3 + rC_24*rx_pred_4 + rC_25*rx_pred_5 + rC_26*rx_pred_6 + rC_27*rx_pred_7 + rC_28*rx_pred_8);
re_innov_3 := (rHydrocarbonFeed_MassFlow_Total - 35.0) - (rC_31*rx_pred_1 + rC_32*rx_pred_2 + rC_33*rx_pred_3 + rC_34*rx_pred_4 + rC_35*rx_pred_5 + rC_36*rx_pred_6 + rC_37*rx_pred_7 + rC_38*rx_pred_8);
re_innov_4 := (rCalculated_DS_Ratio - 0.350) - (rC_41*rx_pred_1 + rC_42*rx_pred_2 + rC_43*rx_pred_3 + rC_44*rx_pred_4 + rC_45*rx_pred_5 + rC_46*rx_pred_6 + rC_47*rx_pred_7 + rC_48*rx_pred_8);
re_innov_5 := (rVoted_TLE_OutletTemp - 400.0) - (rC_51*rx_pred_1 + rC_52*rx_pred_2 + rC_53*rx_pred_3 + rC_54*rx_pred_4 + rC_55*rx_pred_5 + rC_56*rx_pred_6 + rC_57*rx_pred_7 + rC_58*rx_pred_8);
re_innov_6 := (rObserved_ThermalResistance - 12.5) - (rC_61*rx_pred_1 + rC_62*rx_pred_2 + rC_63*rx_pred_3 + rC_64*rx_pred_4 + rC_65*rx_pred_5 + rC_66*rx_pred_6 + rC_67*rx_pred_7 + rC_68*rx_pred_8);
re_innov_7 := (rVoted_FuelGas_Pressure - 3.20) - (rC_71*rx_pred_1 + rC_72*rx_pred_2 + rC_73*rx_pred_3 + rC_74*rx_pred_4 + rC_75*rx_pred_5 + rC_76*rx_pred_6 + rC_77*rx_pred_7 + rC_78*rx_pred_8);
re_innov_8 := (rVoted_FlueGas_O2 - 2.00) - (rC_81*rx_pred_1 + rC_82*rx_pred_2 + rC_83*rx_pred_3 + rC_84*rx_pred_4 + rC_85*rx_pred_5 + rC_86*rx_pred_6 + rC_87*rx_pred_7 + rC_88*rx_pred_8);

(* 3. Kalman Filter Observer A-Posteriori State Update (x_hat = x_pred + L * e_innov) *)
rx_hat_1 := rx_pred_1 + (rL_11*re_innov_1 + rL_12*re_innov_2 + rL_13*re_innov_3 + rL_14*re_innov_4 + rL_15*re_innov_5 + rL_16*re_innov_6 + rL_17*re_innov_7 + rL_18*re_innov_8);
rx_hat_2 := rx_pred_2 + (rL_21*re_innov_1 + rL_22*re_innov_2 + rL_23*re_innov_3 + rL_24*re_innov_4 + rL_25*re_innov_5 + rL_26*re_innov_6 + rL_27*re_innov_7 + rL_28*re_innov_8);
rx_hat_3 := rx_pred_3 + (rL_31*re_innov_1 + rL_32*re_innov_2 + rL_33*re_innov_3 + rL_34*re_innov_4 + rL_35*re_innov_5 + rL_36*re_innov_6 + rL_37*re_innov_7 + rL_38*re_innov_8);
rx_hat_4 := rx_pred_4 + (rL_41*re_innov_1 + rL_42*re_innov_2 + rL_43*re_innov_3 + rL_44*re_innov_4 + rL_45*re_innov_5 + rL_46*re_innov_6 + rL_47*re_innov_7 + rL_48*re_innov_8);
rx_hat_5 := rx_pred_5 + (rL_51*re_innov_1 + rL_52*re_innov_2 + rL_53*re_innov_3 + rL_54*re_innov_4 + rL_55*re_innov_5 + rL_56*re_innov_6 + rL_57*re_innov_7 + rL_58*re_innov_8);
rx_hat_6 := rx_pred_6 + (rL_61*re_innov_1 + rL_62*re_innov_2 + rL_63*re_innov_3 + rL_64*re_innov_4 + rL_65*re_innov_5 + rL_66*re_innov_6 + rL_67*re_innov_7 + rL_68*re_innov_8);
rx_hat_7 := rx_pred_7 + (rL_71*re_innov_1 + rL_72*re_innov_2 + rL_73*re_innov_3 + rL_74*re_innov_4 + rL_75*re_innov_5 + rL_76*re_innov_6 + rL_77*re_innov_7 + rL_78*re_innov_8);
rx_hat_8 := rx_pred_8 + (rL_81*re_innov_1 + rL_82*re_innov_2 + rL_83*re_innov_3 + rL_84*re_innov_4 + rL_85*re_innov_5 + rL_86*re_innov_6 + rL_87*re_innov_7 + rL_88*re_innov_8);

(* 4. Physical Sundaram-Froment Coke Layer Growth & Thermal Resistance Estimation *)
IF (rLaserPyrometer_Peak_TMT > 600.0) AND (rLaserPyrometer_Peak_TMT < 1200.0) THEN
    (* Arrhenius temperature in Kelvin: T_K = TMT + 273.15 *)
    rKinetic_Rate_k_crack := rk_coke_preexp * EXP(-rEa_Coking / (rGas_Constant_R * (rLaserPyrometer_Peak_TMT + 273.15)));
    (* Growth rate function: mm/h, mitigated by dilution steam ratio *)
    IF rCalculated_DS_Ratio > 0.10 THEN
        rCokeGrowthRate_mm_h := rKinetic_Rate_k_crack * (1.80 / (rCalculated_DS_Ratio * 3.50));
    ELSE
        rCokeGrowthRate_mm_h := rKinetic_Rate_k_crack * 5.0;
    END_IF;
    (* Numerical accumulation per cycle *)
    rInternalCoke_mm_Acc := rInternalCoke_mm_Acc + (rCokeGrowthRate_mm_h * (rCycle_s / 3600.0));
END_IF;

(* Bound Estimated Coke Thickness *)
IF rInternalCoke_mm_Acc < 0.05 THEN rInternalCoke_mm_Acc := 0.05; END_IF;
IF rInternalCoke_mm_Acc > 15.0 THEN rInternalCoke_mm_Acc := 15.0; END_IF;
rEstimated_Max_CokeThickness := rInternalCoke_mm_Acc;

(* First-Principles Radial Thermal Resistance R_th = t_metal/k_metal + t_coke/k_coke *)
rObserved_ThermalResistance := (rTube_Wall_Thickness / rThermalCond_Metal) + ((rInternalCoke_mm_Acc * 0.001) / rThermalCond_Coke);
(* Scale to [m2 * K / kW] *)
rObserved_ThermalResistance := rObserved_ThermalResistance * 1000.0;

(* Prognostic Run-Length Estimation: Hours remaining until coke thickness hits 8.0 mm limit *)
IF rCokeGrowthRate_mm_h > 0.00001 THEN
    rRunLength_Remaining_Hours := (8.00 - rInternalCoke_mm_Acc) / rCokeGrowthRate_mm_h;
    IF rRunLength_Remaining_Hours < 0.0 THEN rRunLength_Remaining_Hours := 0.0; END_IF;
ELSE
    rRunLength_Remaining_Hours := 1200.0; (* Nominal default run hours *)
END_IF;

(* 5. First-Principles Pyrolysis Severity & Olefin Yield Observer *)
(* Ethane Conversion: X = 1 - exp(-k * theta^0.5) *)
IF rVoted_Average_COT > 700.0 THEN
    rKinetic_Rate_k_crack := 1.15E13 * EXP(-260000.0 / (rGas_Constant_R * (rVoted_Average_COT + 273.15)));
    rResidence_Time_s := 0.185;
    rEthane_Conv_Fraction := 1.0 - EXP(-rKinetic_Rate_k_crack * SQRT(rResidence_Time_s));
    IF rEthane_Conv_Fraction < 0.30 THEN rEthane_Conv_Fraction := 0.30; END_IF;
    IF rEthane_Conv_Fraction > 0.85 THEN rEthane_Conv_Fraction := 0.85; END_IF;
    
    (* Severity index scaled 1.5 to 2.5 *)
    rKinetic_Cracking_Severity := 1.50 + (rEthane_Conv_Fraction * 1.25);
    (* Ethylene product yield % (bell curve peaking at ~65% conversion) *)
    rKinetic_Ethylene_Yield := 52.5 * (rEthane_Conv_Fraction / 0.65) * EXP(1.0 - (rEthane_Conv_Fraction / 0.65));
ELSE
    rKinetic_Cracking_Severity := 1.00;
    rKinetic_Ethylene_Yield := 0.00;
END_IF;
""")

    # Phase 3: Receding Horizon MPC with Projected Gradient Descent & 8-Pass Coil Balancing
    parts.append("""
(* ================================================================================================================== *)
(* === PHASE 3: RECEDING-HORIZON MPC OPTIMIZATION WITH PROJECTED GRADIENT DESCENT (PGD) & 8-PASS COIL BALANCING ===   *)
(* Horizon: Np = 5 steps, Nc = 3 steps                                                                                *)
(* ================================================================================================================== *)

(* 1. Derive Current Actuator Deviations from Nominal Base Points *)
ru_dev_1 := rFuelGas_ControlValve_Demand - rBase_FuelGas_Demand;
ru_dev_2 := rIDFan_VFD_Speed_Demand - rBase_IDFan_Demand;
ru_dev_3 := rTarget_Total_HC_Feed_Setpoint - rBase_HC_Feed_Flow;
ru_dev_4 := (rTarget_Total_HC_Feed_Setpoint * rTarget_DS_Ratio_Setpoint) - rBase_Steam_Flow;
ru_dev_5 := rTLE_QuenchOil_Valve_Demand - rBase_QuenchOil_Demand;
ru_dev_6 := rCombustionAir_Damper_Demand - rBase_AirDamper_Demand;

(* 2. Initialize PGD Working Actuator Vector *)
ru_opt_1 := ru_dev_1;
ru_opt_2 := ru_dev_2;
ru_opt_3 := ru_dev_3;
ru_opt_4 := ru_dev_4;
ru_opt_5 := ru_dev_5;
ru_opt_6 := ru_dev_6;

rMPC_Cost_Best := 1.0E9;
bMPC_Feasible := FALSE;

(* 3. Iterative Projected Gradient Descent Optimization (8 Iterations) *)
FOR nPGD_Iter := 1 TO 8 DO
    (* --- FORWARD TRAJECTORY PREDICTION OVER 5-STEP HORIZON --- *)
    (* Step 1 Prediction: x_hor_1 = A * x_hat + B * u_opt *)
    rx_hor_1_1 := (rA_11*rx_hat_1 + rA_12*rx_hat_2 + rA_13*rx_hat_3 + rA_14*rx_hat_4 + rA_15*rx_hat_5 + rA_16*rx_hat_6 + rA_17*rx_hat_7 + rA_18*rx_hat_8) +
                  (rB_11*ru_opt_1 + rB_12*ru_opt_2 + rB_13*ru_opt_3 + rB_14*ru_opt_4 + rB_15*ru_opt_5 + rB_16*ru_opt_6);
    rx_hor_1_2 := (rA_21*rx_hat_1 + rA_22*rx_hat_2 + rA_23*rx_hat_3 + rA_24*rx_hat_4 + rA_25*rx_hat_5 + rA_26*rx_hat_6 + rA_27*rx_hat_7 + rA_28*rx_hat_8) +
                  (rB_21*ru_opt_1 + rB_22*ru_opt_2 + rB_23*ru_opt_3 + rB_24*ru_opt_4 + rB_25*ru_opt_5 + rB_26*ru_opt_6);
    rx_hor_1_3 := (rA_31*rx_hat_1 + rA_32*rx_hat_2 + rA_33*rx_hat_3 + rA_34*rx_hat_4 + rA_35*rx_hat_5 + rA_36*rx_hat_6 + rA_37*rx_hat_7 + rA_38*rx_hat_8) +
                  (rB_31*ru_opt_1 + rB_32*ru_opt_2 + rB_33*ru_opt_3 + rB_34*ru_opt_4 + rB_35*ru_opt_5 + rB_36*ru_opt_6);
    rx_hor_1_4 := (rA_41*rx_hat_1 + rA_42*rx_hat_2 + rA_43*rx_hat_3 + rA_44*rx_hat_4 + rA_45*rx_hat_5 + rA_46*rx_hat_6 + rA_47*rx_hat_7 + rA_48*rx_hat_8) +
                  (rB_41*ru_opt_1 + rB_42*ru_opt_2 + rB_43*ru_opt_3 + rB_44*ru_opt_4 + rB_45*ru_opt_5 + rB_46*ru_opt_6);
    rx_hor_1_5 := (rA_51*rx_hat_1 + rA_52*rx_hat_2 + rA_53*rx_hat_3 + rA_54*rx_hat_4 + rA_55*rx_hat_5 + rA_56*rx_hat_6 + rA_57*rx_hat_7 + rA_58*rx_hat_8) +
                  (rB_51*ru_opt_1 + rB_52*ru_opt_2 + rB_53*ru_opt_3 + rB_54*ru_opt_4 + rB_55*ru_opt_5 + rB_56*ru_opt_6);
    rx_hor_1_6 := (rA_61*rx_hat_1 + rA_62*rx_hat_2 + rA_63*rx_hat_3 + rA_64*rx_hat_4 + rA_65*rx_hat_5 + rA_66*rx_hat_6 + rA_67*rx_hat_7 + rA_68*rx_hat_8) +
                  (rB_61*ru_opt_1 + rB_62*ru_opt_2 + rB_63*ru_opt_3 + rB_64*ru_opt_4 + rB_65*ru_opt_5 + rB_66*ru_opt_6);
    rx_hor_1_7 := (rA_71*rx_hat_1 + rA_72*rx_hat_2 + rA_73*rx_hat_3 + rA_74*rx_hat_4 + rA_75*rx_hat_5 + rA_76*rx_hat_6 + rA_77*rx_hat_7 + rA_78*rx_hat_8) +
                  (rB_71*ru_opt_1 + rB_72*ru_opt_2 + rB_73*ru_opt_3 + rB_74*ru_opt_4 + rB_75*ru_opt_5 + rB_76*ru_opt_6);
    rx_hor_1_8 := (rA_81*rx_hat_1 + rA_82*rx_hat_2 + rA_83*rx_hat_3 + rA_84*rx_hat_4 + rA_85*rx_hat_5 + rA_86*rx_hat_6 + rA_87*rx_hat_7 + rA_88*rx_hat_8) +
                  (rB_81*ru_opt_1 + rB_82*ru_opt_2 + rB_83*ru_opt_3 + rB_84*ru_opt_4 + rB_85*ru_opt_5 + rB_86*ru_opt_6);

    (* Step 2 Prediction *)
    rx_hor_2_1 := (rA_11*rx_hor_1_1 + rA_12*rx_hor_1_2 + rA_13*rx_hor_1_3 + rA_14*rx_hor_1_4 + rA_15*rx_hor_1_5 + rA_16*rx_hor_1_6 + rA_17*rx_hor_1_7 + rA_18*rx_hor_1_8) + (rB_11*ru_opt_1);
    rx_hor_2_2 := (rA_21*rx_hor_1_1 + rA_22*rx_hor_1_2 + rA_23*rx_hor_1_3 + rA_24*rx_hor_1_4 + rA_25*rx_hor_1_5 + rA_26*rx_hor_1_6 + rA_27*rx_hor_1_7 + rA_28*rx_hor_1_8) + (rB_22*ru_opt_2);
    rx_hor_2_3 := (rA_31*rx_hor_1_1 + rA_32*rx_hor_1_2 + rA_33*rx_hor_1_3 + rA_34*rx_hor_1_4 + rA_35*rx_hor_1_5 + rA_36*rx_hor_1_6 + rA_37*rx_hor_1_7 + rA_38*rx_hor_1_8) + (rB_33*ru_opt_3);
    rx_hor_2_4 := (rA_41*rx_hor_1_1 + rA_42*rx_hor_1_2 + rA_43*rx_hor_1_3 + rA_44*rx_hor_1_4 + rA_45*rx_hor_1_5 + rA_46*rx_hor_1_6 + rA_47*rx_hor_1_7 + rA_48*rx_hor_1_8) + (rB_44*ru_opt_4);
    rx_hor_2_5 := (rA_51*rx_hor_1_1 + rA_52*rx_hor_1_2 + rA_53*rx_hor_1_3 + rA_54*rx_hor_1_4 + rA_55*rx_hor_1_5 + rA_56*rx_hor_1_6 + rA_57*rx_hor_1_7 + rA_58*rx_hor_1_8) + (rB_55*ru_opt_5);
    rx_hor_2_6 := (rA_61*rx_hor_1_1 + rA_62*rx_hor_1_2 + rA_63*rx_hor_1_3 + rA_64*rx_hor_1_4 + rA_65*rx_hor_1_5 + rA_66*rx_hor_1_6 + rA_67*rx_hor_1_7 + rA_68*rx_hor_1_8);
    rx_hor_2_7 := (rA_71*rx_hor_1_1 + rA_72*rx_hor_1_2 + rA_73*rx_hor_1_3 + rA_74*rx_hor_1_4 + rA_75*rx_hor_1_5 + rA_76*rx_hor_1_6 + rA_77*rx_hor_1_7 + rA_78*rx_hor_1_8) + (rB_71*ru_opt_1);
    rx_hor_2_8 := (rA_81*rx_hor_1_1 + rA_82*rx_hor_1_2 + rA_83*rx_hor_1_3 + rA_84*rx_hor_1_4 + rA_85*rx_hor_1_5 + rA_86*rx_hor_1_6 + rA_87*rx_hor_1_7 + rA_88*rx_hor_1_8) + (rB_86*ru_opt_6);

    (* Step 3 Prediction *)
    rx_hor_3_1 := (rA_11*rx_hor_2_1 + rA_13*rx_hor_2_3 + rA_17*rx_hor_2_7) + (rB_11*ru_opt_1);
    rx_hor_3_2 := (rA_22*rx_hor_2_2 + rA_27*rx_hor_2_7) + (rB_22*ru_opt_2);
    rx_hor_3_3 := (rA_33*rx_hor_2_3) + (rB_33*ru_opt_3);
    rx_hor_3_4 := (rA_44*rx_hor_2_4) + (rB_44*ru_opt_4);
    rx_hor_3_5 := (rA_51*rx_hor_2_1 + rA_55*rx_hor_2_5) + (rB_55*ru_opt_5);
    rx_hor_3_6 := (rA_66*rx_hor_2_6);
    rx_hor_3_7 := (rA_77*rx_hor_2_7) + (rB_71*ru_opt_1);
    rx_hor_3_8 := (rA_88*rx_hor_2_8) + (rB_86*ru_opt_6);

    (* Step 4 Prediction (Terminal Horizon Approaching) *)
    rx_hor_4_1 := (rA_11*rx_hor_3_1 + rA_17*rx_hor_3_7);
    rx_hor_4_2 := (rA_22*rx_hor_3_2);
    rx_hor_4_3 := (rA_33*rx_hor_3_3);
    rx_hor_4_4 := (rA_44*rx_hor_3_4);
    rx_hor_4_5 := (rA_55*rx_hor_3_5);
    rx_hor_4_6 := (rA_66*rx_hor_3_6);
    rx_hor_4_7 := (rA_77*rx_hor_3_7);
    rx_hor_4_8 := (rA_88*rx_hor_3_8);

    (* Step 5 Terminal Prediction *)
    rx_hor_5_1 := (rA_11*rx_hor_4_1);
    rx_hor_5_2 := (rA_22*rx_hor_4_2);
    rx_hor_5_3 := (rA_33*rx_hor_4_3);
    rx_hor_5_4 := (rA_44*rx_hor_4_4);
    rx_hor_5_5 := (rA_55*rx_hor_4_5);
    rx_hor_5_6 := (rA_66*rx_hor_4_6);
    rx_hor_5_7 := (rA_77*rx_hor_4_7);
    rx_hor_5_8 := (rA_88*rx_hor_4_8);

    (* --- QUADRATIC COST FUNCTIONAL EVALUATION --- *)
    rMPC_Cost_Total := (rQ_diag_1 * (rx_hor_1_1 * rx_hor_1_1) + rQ_diag_2 * (rx_hor_1_2 * rx_hor_1_2) +
                        rQ_diag_3 * (rx_hor_1_3 * rx_hor_1_3) + rQ_diag_4 * (rx_hor_1_4 * rx_hor_1_4) +
                        rQ_diag_5 * (rx_hor_1_5 * rx_hor_1_5) + rQ_diag_6 * (rx_hor_1_6 * rx_hor_1_6) +
                        rQ_diag_7 * (rx_hor_1_7 * rx_hor_1_7) + rQ_diag_8 * (rx_hor_1_8 * rx_hor_1_8)) +
                       (rQ_diag_1 * (rx_hor_2_1 * rx_hor_2_1) + rQ_diag_2 * (rx_hor_2_2 * rx_hor_2_2) +
                        rQ_diag_3 * (rx_hor_2_3 * rx_hor_2_3) + rQ_diag_4 * (rx_hor_2_4 * rx_hor_2_4) +
                        rQ_diag_5 * (rx_hor_2_5 * rx_hor_2_5) + rQ_diag_6 * (rx_hor_2_6 * rx_hor_2_6) +
                        rQ_diag_7 * (rx_hor_2_7 * rx_hor_2_7) + rQ_diag_8 * (rx_hor_2_8 * rx_hor_2_8)) +
                       (rP_diag_1 * (rx_hor_5_1 * rx_hor_5_1) + rP_diag_2 * (rx_hor_5_2 * rx_hor_5_2) +
                        rP_diag_3 * (rx_hor_5_3 * rx_hor_5_3) + rP_diag_4 * (rx_hor_5_4 * rx_hor_5_4) +
                        rP_diag_5 * (rx_hor_5_5 * rx_hor_5_5) + rP_diag_6 * (rx_hor_5_6 * rx_hor_5_6) +
                        rP_diag_7 * (rx_hor_5_7 * rx_hor_5_7) + rP_diag_8 * (rx_hor_5_8 * rx_hor_5_8)) +
                       (rR_diag_1 * (ru_opt_1 * ru_opt_1) + rR_diag_2 * (ru_opt_2 * ru_opt_2) +
                        rR_diag_3 * (ru_opt_3 * ru_opt_3) + rR_diag_4 * (ru_opt_4 * ru_opt_4) +
                        rR_diag_5 * (ru_opt_5 * ru_opt_5) + rR_diag_6 * (ru_opt_6 * ru_opt_6));

    IF rMPC_Cost_Total < rMPC_Cost_Best THEN
        rMPC_Cost_Best := rMPC_Cost_Total;
        bMPC_Feasible := TRUE;
    END_IF;

    (* --- ADJOINT GRADIENT CALCULATION --- *)
    rGrad_1 := (2.0 * rR_diag_1 * ru_opt_1) + (2.0 * rB_11 * rQ_diag_1 * rx_hor_1_1) + (2.0 * rB_71 * rQ_diag_7 * rx_hor_1_7);
    rGrad_2 := (2.0 * rR_diag_2 * ru_opt_2) + (2.0 * rB_22 * rQ_diag_2 * rx_hor_1_2);
    rGrad_3 := (2.0 * rR_diag_3 * ru_opt_3) + (2.0 * rB_33 * rQ_diag_3 * rx_hor_1_3) + (2.0 * rB_13 * rQ_diag_1 * rx_hor_1_1);
    rGrad_4 := (2.0 * rR_diag_4 * ru_opt_4) + (2.0 * rB_44 * rQ_diag_4 * rx_hor_1_4) + (2.0 * rB_14 * rQ_diag_1 * rx_hor_1_1);
    rGrad_5 := (2.0 * rR_diag_5 * ru_opt_5) + (2.0 * rB_55 * rQ_diag_5 * rx_hor_1_5);
    rGrad_6 := (2.0 * rR_diag_6 * ru_opt_6) + (2.0 * rB_86 * rQ_diag_8 * rx_hor_1_8);

    (* --- PROJECTED GRADIENT UPDATE & SLEW LIMIT ENFORCEMENT --- *)
    ru_opt_1 := ru_opt_1 - (rAlpha_PGD * rGrad_1);
    ru_opt_2 := ru_opt_2 - (rAlpha_PGD * rGrad_2);
    ru_opt_3 := ru_opt_3 - (rAlpha_PGD * rGrad_3);
    ru_opt_4 := ru_opt_4 - (rAlpha_PGD * rGrad_4);
    ru_opt_5 := ru_opt_5 - (rAlpha_PGD * rGrad_5);
    ru_opt_6 := ru_opt_6 - (rAlpha_PGD * rGrad_6);

    (* Box Projection Against Actuator Limits *)
    IF (rBase_FuelGas_Demand + ru_opt_1) < rU_Min_1 THEN ru_opt_1 := rU_Min_1 - rBase_FuelGas_Demand; END_IF;
    IF (rBase_FuelGas_Demand + ru_opt_1) > rU_Max_1 THEN ru_opt_1 := rU_Max_1 - rBase_FuelGas_Demand; END_IF;
    IF (rBase_IDFan_Demand + ru_opt_2) < rU_Min_2 THEN ru_opt_2 := rU_Min_2 - rBase_IDFan_Demand; END_IF;
    IF (rBase_IDFan_Demand + ru_opt_2) > rU_Max_2 THEN ru_opt_2 := rU_Max_2 - rBase_IDFan_Demand; END_IF;
    IF (rBase_HC_Feed_Flow + ru_opt_3) < rU_Min_3 THEN ru_opt_3 := rU_Min_3 - rBase_HC_Feed_Flow; END_IF;
    IF (rBase_HC_Feed_Flow + ru_opt_3) > rU_Max_3 THEN ru_opt_3 := rU_Max_3 - rBase_HC_Feed_Flow; END_IF;
    IF (rBase_Steam_Flow + ru_opt_4) < rU_Min_4 THEN ru_opt_4 := rU_Min_4 - rBase_Steam_Flow; END_IF;
    IF (rBase_Steam_Flow + ru_opt_4) > rU_Max_4 THEN ru_opt_4 := rU_Max_4 - rBase_Steam_Flow; END_IF;
    IF (rBase_QuenchOil_Demand + ru_opt_5) < rU_Min_5 THEN ru_opt_5 := rU_Min_5 - rBase_QuenchOil_Demand; END_IF;
    IF (rBase_QuenchOil_Demand + ru_opt_5) > rU_Max_5 THEN ru_opt_5 := rU_Max_5 - rBase_QuenchOil_Demand; END_IF;
    IF (rBase_AirDamper_Demand + ru_opt_6) < rU_Min_6 THEN ru_opt_6 := rU_Min_6 - rBase_AirDamper_Demand; END_IF;
    IF (rBase_AirDamper_Demand + ru_opt_6) > rU_Max_6 THEN ru_opt_6 := rU_Max_6 - rBase_AirDamper_Demand; END_IF;
END_FOR;

(* --- Slew Rate Limiter for Physical Actuator Delivery --- *)
IF (ru_opt_1 - ru_dev_1) > rMaxDeltaU_1 THEN ru_opt_1 := ru_dev_1 + rMaxDeltaU_1; END_IF;
IF (ru_opt_1 - ru_dev_1) < -rMaxDeltaU_1 THEN ru_opt_1 := ru_dev_1 - rMaxDeltaU_1; END_IF;

IF (ru_opt_2 - ru_dev_2) > rMaxDeltaU_2 THEN ru_opt_2 := ru_dev_2 + rMaxDeltaU_2; END_IF;
IF (ru_opt_2 - ru_dev_2) < -rMaxDeltaU_2 THEN ru_opt_2 := ru_dev_2 - rMaxDeltaU_2; END_IF;

IF (ru_opt_5 - ru_dev_5) > rMaxDeltaU_5 THEN ru_opt_5 := ru_dev_5 + rMaxDeltaU_5; END_IF;
IF (ru_opt_5 - ru_dev_5) < -rMaxDeltaU_5 THEN ru_opt_5 := ru_dev_5 - rMaxDeltaU_5; END_IF;

(* Update A-Priori State Prediction for Next Scan Cycle *)
rx_pred_1 := rx_hor_1_1; rx_pred_2 := rx_hor_1_2; rx_pred_3 := rx_hor_1_3; rx_pred_4 := rx_hor_1_4;
rx_pred_5 := rx_hor_1_5; rx_pred_6 := rx_hor_1_6; rx_pred_7 := rx_hor_1_7; rx_pred_8 := rx_hor_1_8;

(* Apply MPC Outputs if Master Enable Active and Not in Manual/AFT *)
IF bEnable AND (NOT bManualOverride_En) AND (NOT bAFT_Tripped) THEN
    rFuelGas_ControlValve_Demand := rBase_FuelGas_Demand + ru_opt_1;
    rIDFan_VFD_Speed_Demand      := rBase_IDFan_Demand + ru_opt_2;
    rTLE_QuenchOil_Valve_Demand  := rBase_QuenchOil_Demand + ru_opt_5;
    rCombustionAir_Damper_Demand := rBase_AirDamper_Demand + ru_opt_6;
    rStackDamper_Position_Demand := 75.0 + (ru_opt_2 * 0.25);
END_IF;

(* --- DYNAMIC 8-PASS COIL BALANCING CASCADE --- *)
(* Calculate Pass-to-Average COT Deviations *)
rCOT_Error_Pass1 := rVoted_COT_Pass1 - rVoted_Average_COT;
rCOT_Error_Pass2 := rVoted_COT_Pass2 - rVoted_Average_COT;
rCOT_Error_Pass3 := rVoted_COT_Pass3 - rVoted_Average_COT;
rCOT_Error_Pass4 := rVoted_COT_Pass4 - rVoted_Average_COT;
rCOT_Error_Pass5 := rVoted_COT_Pass5 - rVoted_Average_COT;
rCOT_Error_Pass6 := rVoted_COT_Pass6 - rVoted_Average_COT;
rCOT_Error_Pass7 := rVoted_COT_Pass7 - rVoted_Average_COT;
rCOT_Error_Pass8 := rVoted_COT_Pass8 - rVoted_Average_COT;

(* Pass 1 Trim PI *)
rCOT_Int_Pass1 := rCOT_Int_Pass1 + (rCOT_Error_Pass1 * rCycle_s);
rTrim_Pass1 := 50.0 + (rKp_CoilTrim * rCOT_Error_Pass1) + (rKi_CoilTrim * rCOT_Int_Pass1);
IF rTrim_Pass1 > (50.0 + rMaxTrim_Clamp) THEN rTrim_Pass1 := 50.0 + rMaxTrim_Clamp; END_IF;
IF rTrim_Pass1 < (50.0 - rMaxTrim_Clamp) THEN rTrim_Pass1 := 50.0 - rMaxTrim_Clamp; END_IF;
rCoil1_FeedTrimValve_Demand := rTrim_Pass1;

(* Pass 2 Trim PI *)
rCOT_Int_Pass2 := rCOT_Int_Pass2 + (rCOT_Error_Pass2 * rCycle_s);
rTrim_Pass2 := 50.0 + (rKp_CoilTrim * rCOT_Error_Pass2) + (rKi_CoilTrim * rCOT_Int_Pass2);
IF rTrim_Pass2 > (50.0 + rMaxTrim_Clamp) THEN rTrim_Pass2 := 50.0 + rMaxTrim_Clamp; END_IF;
IF rTrim_Pass2 < (50.0 - rMaxTrim_Clamp) THEN rTrim_Pass2 := 50.0 - rMaxTrim_Clamp; END_IF;
rCoil2_FeedTrimValve_Demand := rTrim_Pass2;

(* Pass 3 Trim PI *)
rCOT_Int_Pass3 := rCOT_Int_Pass3 + (rCOT_Error_Pass3 * rCycle_s);
rTrim_Pass3 := 50.0 + (rKp_CoilTrim * rCOT_Error_Pass3) + (rKi_CoilTrim * rCOT_Int_Pass3);
IF rTrim_Pass3 > (50.0 + rMaxTrim_Clamp) THEN rTrim_Pass3 := 50.0 + rMaxTrim_Clamp; END_IF;
IF rTrim_Pass3 < (50.0 - rMaxTrim_Clamp) THEN rTrim_Pass3 := 50.0 - rMaxTrim_Clamp; END_IF;
rCoil3_FeedTrimValve_Demand := rTrim_Pass3;

(* Pass 4 Trim PI *)
rCOT_Int_Pass4 := rCOT_Int_Pass4 + (rCOT_Error_Pass4 * rCycle_s);
rTrim_Pass4 := 50.0 + (rKp_CoilTrim * rCOT_Error_Pass4) + (rKi_CoilTrim * rCOT_Int_Pass4);
IF rTrim_Pass4 > (50.0 + rMaxTrim_Clamp) THEN rTrim_Pass4 := 50.0 + rMaxTrim_Clamp; END_IF;
IF rTrim_Pass4 < (50.0 - rMaxTrim_Clamp) THEN rTrim_Pass4 := 50.0 - rMaxTrim_Clamp; END_IF;
rCoil4_FeedTrimValve_Demand := rTrim_Pass4;

(* Pass 5 Trim PI *)
rCOT_Int_Pass5 := rCOT_Int_Pass5 + (rCOT_Error_Pass5 * rCycle_s);
rTrim_Pass5 := 50.0 + (rKp_CoilTrim * rCOT_Error_Pass5) + (rKi_CoilTrim * rCOT_Int_Pass5);
IF rTrim_Pass5 > (50.0 + rMaxTrim_Clamp) THEN rTrim_Pass5 := 50.0 + rMaxTrim_Clamp; END_IF;
IF rTrim_Pass5 < (50.0 - rMaxTrim_Clamp) THEN rTrim_Pass5 := 50.0 - rMaxTrim_Clamp; END_IF;
rCoil5_FeedTrimValve_Demand := rTrim_Pass5;

(* Pass 6 Trim PI *)
rCOT_Int_Pass6 := rCOT_Int_Pass6 + (rCOT_Error_Pass6 * rCycle_s);
rTrim_Pass6 := 50.0 + (rKp_CoilTrim * rCOT_Error_Pass6) + (rKi_CoilTrim * rCOT_Int_Pass6);
IF rTrim_Pass6 > (50.0 + rMaxTrim_Clamp) THEN rTrim_Pass6 := 50.0 + rMaxTrim_Clamp; END_IF;
IF rTrim_Pass6 < (50.0 - rMaxTrim_Clamp) THEN rTrim_Pass6 := 50.0 - rMaxTrim_Clamp; END_IF;
rCoil6_FeedTrimValve_Demand := rTrim_Pass6;

(* Pass 7 Trim PI *)
rCOT_Int_Pass7 := rCOT_Int_Pass7 + (rCOT_Error_Pass7 * rCycle_s);
rTrim_Pass7 := 50.0 + (rKp_CoilTrim * rCOT_Error_Pass7) + (rKi_CoilTrim * rCOT_Int_Pass7);
IF rTrim_Pass7 > (50.0 + rMaxTrim_Clamp) THEN rTrim_Pass7 := 50.0 + rMaxTrim_Clamp; END_IF;
IF rTrim_Pass7 < (50.0 - rMaxTrim_Clamp) THEN rTrim_Pass7 := 50.0 - rMaxTrim_Clamp; END_IF;
rCoil7_FeedTrimValve_Demand := rTrim_Pass7;

(* Pass 8 Trim PI *)
rCOT_Int_Pass8 := rCOT_Int_Pass8 + (rCOT_Error_Pass8 * rCycle_s);
rTrim_Pass8 := 50.0 + (rKp_CoilTrim * rCOT_Error_Pass8) + (rKi_CoilTrim * rCOT_Int_Pass8);
IF rTrim_Pass8 > (50.0 + rMaxTrim_Clamp) THEN rTrim_Pass8 := 50.0 + rMaxTrim_Clamp; END_IF;
IF rTrim_Pass8 < (50.0 - rMaxTrim_Clamp) THEN rTrim_Pass8 := 50.0 - rMaxTrim_Clamp; END_IF;
rCoil8_FeedTrimValve_Demand := rTrim_Pass8;

(* Find Maximum Maldistribution Spread Across All 8 Passes *)
rTempMin := rVoted_COT_Pass1;
rTempMax := rVoted_COT_Pass1;
IF rVoted_COT_Pass2 < rTempMin THEN rTempMin := rVoted_COT_Pass2; END_IF;
IF rVoted_COT_Pass2 > rTempMax THEN rTempMax := rVoted_COT_Pass2; END_IF;
IF rVoted_COT_Pass3 < rTempMin THEN rTempMin := rVoted_COT_Pass3; END_IF;
IF rVoted_COT_Pass3 > rTempMax THEN rTempMax := rVoted_COT_Pass3; END_IF;
IF rVoted_COT_Pass4 < rTempMin THEN rTempMin := rVoted_COT_Pass4; END_IF;
IF rVoted_COT_Pass4 > rTempMax THEN rTempMax := rVoted_COT_Pass4; END_IF;
IF rVoted_COT_Pass5 < rTempMin THEN rTempMin := rVoted_COT_Pass5; END_IF;
IF rVoted_COT_Pass5 > rTempMax THEN rTempMax := rVoted_COT_Pass5; END_IF;
IF rVoted_COT_Pass6 < rTempMin THEN rTempMin := rVoted_COT_Pass6; END_IF;
IF rVoted_COT_Pass6 > rTempMax THEN rTempMax := rVoted_COT_Pass6; END_IF;
IF rVoted_COT_Pass7 < rTempMin THEN rTempMin := rVoted_COT_Pass7; END_IF;
IF rVoted_COT_Pass7 > rTempMax THEN rTempMax := rVoted_COT_Pass7; END_IF;
IF rVoted_COT_Pass8 < rTempMin THEN rTempMin := rVoted_COT_Pass8; END_IF;
IF rVoted_COT_Pass8 > rTempMax THEN rTempMax := rVoted_COT_Pass8; END_IF;
rMax_Pass_DeltaT := rTempMax - rTempMin;

(* Dynamic Cross-Limiting Lock Between Feed and Steam *)
rSteam_Permitted_HC_Max := rDilutionSteam_MassFlow_Total / 0.320; (* Limit HC if steam drops *)
rHC_Demanded_Steam_Min := rHydrocarbonFeed_MassFlow_Total * 0.350; (* Lead steam if HC rises *)
""")

    # Phase 4: Deterministic 14-Stage Production Finite State Machine
    parts.append("""
(* ================================================================================================================== *)
(* === PHASE 4: DETERMINISTIC 14-STAGE PRODUCTION FINITE STATE MACHINE (FSM) ===                                      *)
(* ================================================================================================================== *)

(* Global Master Interlock Verification *)
IF (NOT bSafetyInterlock_OK) OR bAFT_Trip_Command THEN
    nState := STATE_12_EMERGENCY_AFT_FAST_CUTOFF;
END_IF;

(* Track State Dwell Time *)
IF nState <> nState_Prev THEN
    tStateTimer := 0.0;
    nState_Prev := nState;
ELSE
    tStateTimer := tStateTimer + rCycle_s;
END_IF;

CASE nState OF

    STATE_0_INIT_SAFE_STANDBY:
        (* Entry & Standby Safe Actions *)
        bFurnace_Ready := FALSE;
        bFurnace_OnSpec := FALSE;
        bAFT_Tripped := FALSE;
        bDecoke_Active := FALSE;
        rFuelGas_ControlValve_Demand := 0.0;
        rIDFan_VFD_Speed_Demand := 25.0;
        rStackDamper_Position_Demand := 30.0;
        rTLE_QuenchOil_Valve_Demand := 0.0;
        rTLE_BlowdownValve_Demand := 0.0;

        (* Transition to Nitrogen Purge on Enable *)
        IF bEnable AND bSafetyInterlock_OK THEN
            tPurgeTimer := 0.0;
            nState := STATE_1_NITROGEN_PURGE;
        END_IF;

    STATE_1_NITROGEN_PURGE:
        (* 4 Furnace Volume Air/N2 Purge with Dampers Fully Open *)
        bFurnace_Ready := FALSE;
        rFuelGas_ControlValve_Demand := 0.0;
        rIDFan_VFD_Speed_Demand := 85.0;
        rStackDamper_Position_Demand := 100.0;
        rCombustionAir_Damper_Demand := 100.0;
        tPurgeTimer := tPurgeTimer + rCycle_s;

        (* Verify Firebox Draft Negative and Purge Completed (Minimum 300 seconds) *)
        IF (tPurgeTimer >= 300.0) AND (rVoted_Firebox_Draft < -1.0) THEN
            nState := STATE_2_PILOT_GAS_IGNITION;
        END_IF;

    STATE_2_PILOT_GAS_IGNITION:
        (* BMS Pilot Header Charged, Igniters Sparking, Flame Verification *)
        rFuelGas_ControlValve_Demand := 5.0; (* Pilot light-off pressure *)
        rIDFan_VFD_Speed_Demand := 45.0;
        rStackDamper_Position_Demand := 50.0;
        rCombustionAir_Damper_Demand := 40.0;

        (* Pilot flame established and draft stable *)
        IF (tStateTimer >= 45.0) AND (rVoted_FuelGas_Pressure > 1.20) AND (rVoted_Firebox_Draft < -0.80) THEN
            tWarmupRampTimer := 0.0;
            rWarmup_Target_COT := 150.0;
            nState := STATE_3_REFRACTORY_WARMUP;
        END_IF;

    STATE_3_REFRACTORY_WARMUP:
        (* Controlled Refractory Thermal Stress Ramp (25 to 50 deg C / h) *)
        rFuelGas_ControlValve_Demand := 15.0 + (tStateTimer * 0.015);
        IF rFuelGas_ControlValve_Demand > 35.0 THEN rFuelGas_ControlValve_Demand := 35.0; END_IF;
        rIDFan_VFD_Speed_Demand := 50.0;
        rStackDamper_Position_Demand := 60.0;

        (* Transition to Dilution Steam Circulation once Firebox Reaches 450 deg C *)
        IF (rVoted_Average_COT >= 450.0) AND (tStateTimer >= 180.0) THEN
            nState := STATE_4_DILUTION_STEAM_CIRC;
        END_IF;

    STATE_4_DILUTION_STEAM_CIRC:
        (* Dilution Steam Injected into Coils for Pre-heating & Condensate Clearing *)
        rFuelGas_ControlValve_Demand := 38.0;
        rIDFan_VFD_Speed_Demand := 55.0;
        rStackDamper_Position_Demand := 65.0;
        rTLE_BlowdownValve_Demand := 15.0; (* Clear TLE steam drum condensate *)

        (* Check Dilution Steam Flow Verified and COT Reaching Cut-in Window (> 780 deg C) *)
        IF (rDilutionSteam_MassFlow_Total >= 10.0) AND (rVoted_Average_COT >= 780.0) AND (tStateTimer >= 120.0) THEN
            bFurnace_Ready := TRUE;
            nState := STATE_5_HYDROCARBON_FEED_CUTIN;
        END_IF;

    STATE_5_HYDROCARBON_FEED_CUTIN:
        (* Progressive Hydrocarbon Introduction with Cross-Limiting Ratio Lock *)
        bFurnace_Ready := TRUE;
        rFuelGas_ControlValve_Demand := 48.0;
        rIDFan_VFD_Speed_Demand := 60.0;
        rTLE_QuenchOil_Valve_Demand := 25.0; (* Pre-charge quench header *)

        (* Transition to Pass Balancing when HC Feed Exceeds 25.0 t/h and Ratio Stable *)
        IF (rHydrocarbonFeed_MassFlow_Total >= 25.0) AND (rCalculated_DS_Ratio >= 0.32) AND (tStateTimer >= 90.0) THEN
            nState := STATE_6_RADIANT_PASS_BALANCING;
        END_IF;

    STATE_6_RADIANT_PASS_BALANCING:
        (* Individual 8-Pass Trim Tuning to Eliminate Maldistribution Spread *)
        rFuelGas_ControlValve_Demand := 55.0;
        rIDFan_VFD_Speed_Demand := 62.0;

        (* Once Pass Delta-T is Below 4.0 deg C and COT Reaches Target Envelope *)
        IF (rMax_Pass_DeltaT <= 4.0) AND (ABS(rVoted_Average_COT - rTarget_COT_Setpoint) <= 5.0) AND (tStateTimer >= 60.0) THEN
            bFurnace_OnSpec := TRUE;
            nState := STATE_7_NORMAL_CRACKING_MPC;
        END_IF;

    STATE_7_NORMAL_CRACKING_MPC:
        (* Steady-State Optimal Cracking Under Full Receding-Horizon MPC Control *)
        bFurnace_OnSpec := TRUE;
        bFurnace_Ready := TRUE;

        (* Check Operator Requests Decoke Cycle *)
        IF bDecokeMode_Req THEN
            nState := STATE_9_COKING_SURVEILLANCE;
        (* Operator Triggers High-Severity Cracking Mode *)
        ELSIF rTarget_COT_Setpoint >= 855.0 THEN
            nState := STATE_8_HIGH_SEVERITY_OPERATION;
        (* Observer Flags Critical Coke Layer Thickness *)
        ELSIF (rEstimated_Max_CokeThickness >= 7.50) OR (rObserved_ThermalResistance >= 16.0) THEN
            nState := STATE_9_COKING_SURVEILLANCE;
        END_IF;

    STATE_8_HIGH_SEVERITY_OPERATION:
        (* Maximum Olefin Yield Operation Near Metallurgical TMT Envelope (< 1080 deg C) *)
        bFurnace_OnSpec := TRUE;

        (* Safety Fallback to Normal Cracking if TMT Approaches 1065 deg C *)
        IF (rLaserPyrometer_Peak_TMT >= 1065.0) OR (rTarget_COT_Setpoint < 850.0) THEN
            nState := STATE_7_NORMAL_CRACKING_MPC;
        ELSIF bDecokeMode_Req OR (rEstimated_Max_CokeThickness >= 7.50) THEN
            nState := STATE_9_COKING_SURVEILLANCE;
        END_IF;

    STATE_9_COKING_SURVEILLANCE:
        (* Decoking Transition Advisory: Ramping Down Hydrocarbon Feed *)
        bFurnace_OnSpec := FALSE;
        rFuelGas_ControlValve_Demand := 35.0;
        rIDFan_VFD_Speed_Demand := 50.0;

        (* Once Hydrocarbon Feed Reaches Zero and Only Dilution Steam Remains *)
        IF (rHydrocarbonFeed_MassFlow_Total <= 1.0) AND (tStateTimer >= 120.0) THEN
            tDecokeTimer := 0.0;
            bDecoke_Active := TRUE;
            nState := STATE_10_DECOKING_STEAM_AIR_BURN;
        END_IF;

    STATE_10_DECOKING_STEAM_AIR_BURN:
        (* Online Controlled Decoking with Steam/Air Mixture & CO/CO2 Surveillance *)
        bDecoke_Active := TRUE;
        bFurnace_OnSpec := FALSE;
        rFuelGas_ControlValve_Demand := 30.0;
        rIDFan_VFD_Speed_Demand := 65.0;
        rStackDamper_Position_Demand := 75.0;
        tDecokeTimer := tDecokeTimer + rCycle_s;

        (* Decoke complete: Burn time exceeded (e.g. 1800 s simulation) and CO drops below 10 ppm *)
        IF (tDecokeTimer >= 1800.0) AND (rFlueGas_CO_Content < 10.0) THEN
            bDecoke_Active := FALSE;
            rInternalCoke_mm_Acc := 0.10; (* Cleaned coil baseline coke thickness *)
            nState := STATE_11_CONTROLLED_HOT_IDLE;
        END_IF;

    STATE_11_CONTROLLED_HOT_IDLE:
        (* Low-Firing Dilution Steam Sweep (Standby for Next Production Run) *)
        bFurnace_Ready := TRUE;
        bFurnace_OnSpec := FALSE;
        bDecoke_Active := FALSE;
        rFuelGas_ControlValve_Demand := 22.0;
        rIDFan_VFD_Speed_Demand := 45.0;

        IF bEnable AND (NOT bDecokeMode_Req) THEN
            nState := STATE_5_HYDROCARBON_FEED_CUTIN;
        END_IF;

    STATE_12_EMERGENCY_AFT_FAST_CUTOFF:
        (* Emergency Automated Feed Trip (AFT) & SIS Fuel Gas Quick Shutoff *)
        bAFT_Tripped := TRUE;
        bFurnace_Ready := FALSE;
        bFurnace_OnSpec := FALSE;
        bDecoke_Active := FALSE;
        rFuelGas_ControlValve_Demand := 0.0;    (* Fast fuel gas slam shut *)
        rIDFan_VFD_Speed_Demand := 100.0;       (* Maximum firebox purge *)
        rStackDamper_Position_Demand := 100.0;  (* Dampers full open *)
        rTLE_QuenchOil_Valve_Demand := 100.0;   (* Full emergency quench *)
        rTLE_BlowdownValve_Demand := 100.0;     (* HP steam drum emergency blowdown *)
        rCoil1_FeedTrimValve_Demand := 0.0;
        rCoil2_FeedTrimValve_Demand := 0.0;
        rCoil3_FeedTrimValve_Demand := 0.0;
        rCoil4_FeedTrimValve_Demand := 0.0;
        rCoil5_FeedTrimValve_Demand := 0.0;
        rCoil6_FeedTrimValve_Demand := 0.0;
        rCoil7_FeedTrimValve_Demand := 0.0;
        rCoil8_FeedTrimValve_Demand := 0.0;

        (* Permissive Reset via Pushbutton *)
        IF bAcknowledge_Alarms AND bSafetyInterlock_OK AND (NOT bAFT_Trip_Command) THEN
            bAFT_Tripped := FALSE;
            nState := STATE_0_INIT_SAFE_STANDBY;
        END_IF;

    STATE_13_SHUTDOWN_COOLDOWN:
        (* Post-Purge and Controlled Firebox Refractory Cool-Down *)
        bFurnace_Ready := FALSE;
        bFurnace_OnSpec := FALSE;
        rFuelGas_ControlValve_Demand := 0.0;
        rIDFan_VFD_Speed_Demand := 20.0;
        rStackDamper_Position_Demand := 25.0;

        IF bAcknowledge_Alarms THEN
            nState := STATE_0_INIT_SAFE_STANDBY;
        END_IF;

    ELSE
        nState := STATE_0_INIT_SAFE_STANDBY;
END_CASE;

nActive_State_ID := nState;
""")

    # Phase 5: ISA-18.2 Alarms and bit-packing
    parts.append("""
(* ================================================================================================================== *)
(* === PHASE 5: ISA-18.2 MULTI-TIER ALARMS & 32-BIT BIT-PACKED STATUS WORDS ===                                       *)
(* ================================================================================================================== *)

(* --- CHANNEL 1: COT AVERAGE ALARMS --- *)
IF rVoted_Average_COT >= (865.0) THEN
    bTrip_COT_HH := TRUE;
    bUnack_Trip_COT_HH := TRUE;
ELSIF rVoted_Average_COT <= (865.0 - rCOT_Deadband) THEN
    bTrip_COT_HH := FALSE;
END_IF;

IF rVoted_Average_COT >= (855.0) THEN
    bWarn_COT_H := TRUE;
ELSIF rVoted_Average_COT <= (855.0 - rCOT_Deadband) THEN
    bWarn_COT_H := FALSE;
END_IF;

IF rVoted_Average_COT <= (820.0) THEN
    bWarn_COT_L := TRUE;
ELSIF rVoted_Average_COT >= (820.0 + rCOT_Deadband) THEN
    bWarn_COT_L := FALSE;
END_IF;

IF rVoted_Average_COT <= (800.0) THEN
    bTrip_COT_LL := TRUE;
ELSIF rVoted_Average_COT >= (800.0 + rCOT_Deadband) THEN
    bTrip_COT_LL := FALSE;
END_IF;

(* --- CHANNEL 2: PEAK TUBE METAL TEMPERATURE (TMT) ALARMS --- *)
IF rLaserPyrometer_Peak_TMT >= (1085.0) THEN
    bTrip_TMT_HH := TRUE;
    bUnack_Trip_TMT_HH := TRUE;
ELSIF rLaserPyrometer_Peak_TMT <= (1085.0 - rTMT_Deadband) THEN
    bTrip_TMT_HH := FALSE;
END_IF;

IF rLaserPyrometer_Peak_TMT >= (1065.0) THEN
    bWarn_TMT_H := TRUE;
ELSIF rLaserPyrometer_Peak_TMT <= (1065.0 - rTMT_Deadband) THEN
    bWarn_TMT_H := FALSE;
END_IF;

(* --- CHANNEL 3: FIREBOX ARCH DRAFT PRESSURE ALARMS --- *)
IF rVoted_Firebox_Draft >= (0.20) THEN (* Positive pressure danger *)
    bTrip_Draft_HH := TRUE;
    bUnack_Trip_Draft_HH := TRUE;
ELSIF rVoted_Firebox_Draft <= (0.20 - rDraft_Deadband) THEN
    bTrip_Draft_HH := FALSE;
END_IF;

IF rVoted_Firebox_Draft >= (-0.30) THEN
    bWarn_Draft_H := TRUE;
ELSIF rVoted_Firebox_Draft <= (-0.30 - rDraft_Deadband) THEN
    bWarn_Draft_H := FALSE;
END_IF;

IF rVoted_Firebox_Draft <= (-3.50) THEN
    bWarn_Draft_L := TRUE;
ELSIF rVoted_Firebox_Draft >= (-3.50 + rDraft_Deadband) THEN
    bWarn_Draft_L := FALSE;
END_IF;

IF rVoted_Firebox_Draft <= (-4.50) THEN
    bTrip_Draft_LL := TRUE;
ELSIF rVoted_Firebox_Draft >= (-4.50 + rDraft_Deadband) THEN
    bTrip_Draft_LL := FALSE;
END_IF;

(* --- CHANNEL 4: FUEL GAS SUPPLY PRESSURE ALARMS --- *)
IF rVoted_FuelGas_Pressure >= (4.50) THEN
    bTrip_FuelGas_HH := TRUE;
    bUnack_Trip_FuelGas_HH := TRUE;
ELSIF rVoted_FuelGas_Pressure <= (4.50 - rFuelGas_Deadband) THEN
    bTrip_FuelGas_HH := FALSE;
END_IF;

IF rVoted_FuelGas_Pressure >= (4.00) THEN
    bWarn_FuelGas_H := TRUE;
ELSIF rVoted_FuelGas_Pressure <= (4.00 - rFuelGas_Deadband) THEN
    bWarn_FuelGas_H := FALSE;
END_IF;

IF rVoted_FuelGas_Pressure <= (2.00) THEN
    bWarn_FuelGas_L := TRUE;
ELSIF rVoted_FuelGas_Pressure >= (2.00 + rFuelGas_Deadband) THEN
    bWarn_FuelGas_L := FALSE;
END_IF;

IF rVoted_FuelGas_Pressure <= (1.50) THEN
    bTrip_FuelGas_LL := TRUE;
ELSIF rVoted_FuelGas_Pressure >= (1.50 + rFuelGas_Deadband) THEN
    bTrip_FuelGas_LL := FALSE;
END_IF;

(* --- CHANNEL 5: FLUE GAS STACK OXYGEN ALARMS --- *)
IF rVoted_FlueGas_O2 >= (6.50) THEN
    bTrip_StackO2_HH := TRUE;
ELSIF rVoted_FlueGas_O2 <= (6.50 - rO2_Deadband) THEN
    bTrip_StackO2_HH := FALSE;
END_IF;

IF rVoted_FlueGas_O2 >= (4.50) THEN
    bWarn_StackO2_H := TRUE;
ELSIF rVoted_FlueGas_O2 <= (4.50 - rO2_Deadband) THEN
    bWarn_StackO2_H := FALSE;
END_IF;

IF rVoted_FlueGas_O2 <= (1.00) THEN
    bWarn_StackO2_L := TRUE;
ELSIF rVoted_FlueGas_O2 >= (1.00 + rO2_Deadband) THEN
    bWarn_StackO2_L := FALSE;
END_IF;

IF rVoted_FlueGas_O2 <= (0.50) THEN (* Danger of unburned fuel in firebox *)
    bTrip_StackO2_LL := TRUE;
ELSIF rVoted_FlueGas_O2 >= (0.50 + rO2_Deadband) THEN
    bTrip_StackO2_LL := FALSE;
END_IF;

(* --- CHANNEL 6: TLE EFFLUENT OUTLET TEMPERATURE ALARMS --- *)
IF rVoted_TLE_OutletTemp >= (440.0) THEN
    bTrip_TLE_HH := TRUE;
ELSIF rVoted_TLE_OutletTemp <= (440.0 - rTLE_Deadband) THEN
    bTrip_TLE_HH := FALSE;
END_IF;

IF rVoted_TLE_OutletTemp >= (425.0) THEN
    bWarn_TLE_H := TRUE;
ELSIF rVoted_TLE_OutletTemp <= (425.0 - rTLE_Deadband) THEN
    bWarn_TLE_H := FALSE;
END_IF;

IF rVoted_TLE_OutletTemp <= (350.0) THEN
    bWarn_TLE_L := TRUE;
ELSIF rVoted_TLE_OutletTemp >= (350.0 + rTLE_Deadband) THEN
    bWarn_TLE_L := FALSE;
END_IF;

IF rVoted_TLE_OutletTemp <= (330.0) THEN
    bTrip_TLE_LL := TRUE;
ELSIF rVoted_TLE_OutletTemp >= (330.0 + rTLE_Deadband) THEN
    bTrip_TLE_LL := FALSE;
END_IF;

(* --- CHANNEL 7: HYDROCARBON FEED FLOW DEVIATIONS --- *)
IF rHydrocarbonFeed_MassFlow_Total >= 55.0 THEN
    bTrip_FeedFlow_HH := TRUE;
ELSIF rHydrocarbonFeed_MassFlow_Total <= 52.0 THEN
    bTrip_FeedFlow_HH := FALSE;
END_IF;

IF (nState >= STATE_5_HYDROCARBON_FEED_CUTIN) AND (rHydrocarbonFeed_MassFlow_Total <= 10.0) THEN
    bTrip_FeedFlow_LL := TRUE;
ELSE
    bTrip_FeedFlow_LL := FALSE;
END_IF;

(* --- CHANNEL 8: DILUTION STEAM RATIO ALARMS --- *)
IF (nState >= STATE_5_HYDROCARBON_FEED_CUTIN) AND (rCalculated_DS_Ratio <= 0.280) THEN
    bWarn_DSRatio_L := TRUE;
ELSIF rCalculated_DS_Ratio >= (0.280 + rDSRatio_Deadband) THEN
    bWarn_DSRatio_L := FALSE;
END_IF;

IF (nState >= STATE_5_HYDROCARBON_FEED_CUTIN) AND (rCalculated_DS_Ratio <= 0.250) THEN
    bTrip_DSRatio_LL := TRUE;
    bUnack_Trip_DSRatio_LL := TRUE;
ELSIF rCalculated_DS_Ratio >= (0.250 + rDSRatio_Deadband) THEN
    bTrip_DSRatio_LL := FALSE;
END_IF;

(* --- CHANNEL 9: STACK CO EMISSIONS --- *)
IF rFlueGas_CO_Content >= 200.0 THEN
    bTrip_StackCO_HH := TRUE;
    bUnack_Trip_StackCO_HH := TRUE;
ELSIF rFlueGas_CO_Content <= 150.0 THEN
    bTrip_StackCO_HH := FALSE;
END_IF;

IF rFlueGas_CO_Content >= 100.0 THEN
    bWarn_StackCO_H := TRUE;
ELSIF rFlueGas_CO_Content <= 80.0 THEN
    bWarn_StackCO_H := FALSE;
END_IF;

(* --- CHANNEL 10: TLE STEAM DRUM PRESSURE ALARMS --- *)
IF rTLE_SteamDrum_Pressure >= 125.0 THEN
    bTrip_SteamDrum_HH := TRUE;
ELSIF rTLE_SteamDrum_Pressure <= 120.0 THEN
    bTrip_SteamDrum_HH := FALSE;
END_IF;

IF rTLE_SteamDrum_Pressure <= 75.0 THEN
    bTrip_SteamDrum_LL := TRUE;
ELSIF rTLE_SteamDrum_Pressure >= 80.0 THEN
    bTrip_SteamDrum_LL := FALSE;
END_IF;

(* --- CHANNEL 11: 8-PASS COT MALDISTRIBUTION SPREAD --- *)
IF rMax_Pass_DeltaT >= 25.0 THEN
    bTrip_PassSpread_HH := TRUE;
ELSIF rMax_Pass_DeltaT <= 20.0 THEN
    bTrip_PassSpread_HH := FALSE;
END_IF;

IF rMax_Pass_DeltaT >= 15.0 THEN
    bWarn_PassSpread_H := TRUE;
ELSIF rMax_Pass_DeltaT <= 12.0 THEN
    bWarn_PassSpread_H := FALSE;
END_IF;

(* --- CHANNEL 12: RADIANT COKE FOULING RESISTANCE --- *)
IF rObserved_ThermalResistance >= 18.0 THEN
    bTrip_CokeLimit_HH := TRUE;
ELSIF rObserved_ThermalResistance <= 16.5 THEN
    bTrip_CokeLimit_HH := FALSE;
END_IF;

IF rObserved_ThermalResistance >= 15.0 THEN
    bWarn_CokeLimit_H := TRUE;
ELSIF rObserved_ThermalResistance <= 14.0 THEN
    bWarn_CokeLimit_H := FALSE;
END_IF;

(* --- CHANNEL 13: STACK NOX HIGH WARNING --- *)
bWarn_StackNOx_H := (rFlueGas_NOx_Content >= 120.0);

(* --- CHANNEL 14: TLE QUENCH OIL LOW FLOW --- *)
IF rTLE_QuenchOil_InletTemp >= 250.0 THEN
    bWarn_QuenchOil_L := TRUE;
ELSE
    bWarn_QuenchOil_L := FALSE;
END_IF;

(* --- CHANNEL 15: ID FAN SATURATION --- *)
bWarn_IDFan_Saturation := (rIDFan_VFD_Speed_Demand >= 98.0) AND (rVoted_Firebox_Draft >= -0.50);

(* Acknowledge Alarm Pushbutton Logic *)
IF bAcknowledge_Alarms THEN
    bUnack_Trip_COT_HH     := FALSE;
    bUnack_Trip_TMT_HH     := FALSE;
    bUnack_Trip_Draft_HH   := FALSE;
    bUnack_Trip_FuelGas_HH := FALSE;
    bUnack_Trip_DSRatio_LL := FALSE;
    bUnack_Trip_StackCO_HH := FALSE;
END_IF;

(* Automated Feed Trip (AFT) Auto-Trigger on Critical Unrecoverable Alarms *)
IF bTrip_COT_HH OR bTrip_TMT_HH OR bTrip_Draft_HH OR bTrip_FuelGas_HH OR bTrip_DSRatio_LL OR bTrip_StackCO_HH THEN
    nState := STATE_12_EMERGENCY_AFT_FAST_CUTOFF;
END_IF;

(* ================================================================================================================== *)
(* === PACK BITWISE STATUS AND ALARM WORDS (32-BIT DWORDS) ===                                                        *)
(* ================================================================================================================== *)

(* Pack dwAlarmWord1: Emergency & High-High Trips *)
dwAlarmWord1 := 16#00000000;
IF bTrip_COT_HH         THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000001; END_IF; (* Bit 0: COT HH *)
IF bTrip_TMT_HH         THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000002; END_IF; (* Bit 1: TMT HH *)
IF bTrip_Draft_HH       THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000004; END_IF; (* Bit 2: Draft HH *)
IF bTrip_FuelGas_HH     THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000008; END_IF; (* Bit 3: Fuel Gas HH *)
IF bTrip_StackO2_HH     THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000010; END_IF; (* Bit 4: Stack O2 HH *)
IF bTrip_TLE_HH         THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000020; END_IF; (* Bit 5: TLE Temp HH *)
IF bTrip_FeedFlow_HH    THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000040; END_IF; (* Bit 6: HC Feed HH *)
IF bTrip_DSRatio_LL     THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000080; END_IF; (* Bit 7: Dilution Steam LL *)
IF bTrip_StackCO_HH     THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000100; END_IF; (* Bit 8: Stack CO HH *)
IF bTrip_SteamDrum_HH   THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000200; END_IF; (* Bit 9: TLE Steam Drum HH *)
IF bTrip_PassSpread_HH  THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000400; END_IF; (* Bit 10: Pass Delta-T HH *)
IF bTrip_CokeLimit_HH   THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000800; END_IF; (* Bit 11: Coking Thermal Res HH *)
IF bTrip_COT_LL         THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00001000; END_IF; (* Bit 12: COT LL *)
IF bTrip_Draft_LL       THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00002000; END_IF; (* Bit 13: Draft LL *)
IF bTrip_FuelGas_LL     THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00004000; END_IF; (* Bit 14: Fuel Gas LL *)
IF bTrip_StackO2_LL     THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00008000; END_IF; (* Bit 15: Stack O2 LL *)
IF bTrip_TLE_LL         THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00010000; END_IF; (* Bit 16: TLE Temp LL *)
IF bTrip_FeedFlow_LL    THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00020000; END_IF; (* Bit 17: HC Feed LL *)
IF bTrip_SteamDrum_LL   THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00040000; END_IF; (* Bit 18: TLE Steam Drum LL *)
IF bAFT_Tripped         THEN dwAlarmWord1 := dwAlarmWord1 OR 16#80000000; END_IF; (* Bit 31: Master AFT Active *)

(* Pack dwAlarmWord2: Process Warnings & Secondary Limits *)
dwAlarmWord2 := 16#00000000;
IF bWarn_COT_H          THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000001; END_IF; (* Bit 0: COT High *)
IF bWarn_COT_L          THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000002; END_IF; (* Bit 1: COT Low *)
IF bWarn_TMT_H          THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000004; END_IF; (* Bit 2: TMT High *)
IF bWarn_Draft_H        THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000008; END_IF; (* Bit 3: Draft High *)
IF bWarn_Draft_L        THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000010; END_IF; (* Bit 4: Draft Low *)
IF bWarn_FuelGas_H      THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000020; END_IF; (* Bit 5: Fuel Gas High *)
IF bWarn_FuelGas_L      THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000040; END_IF; (* Bit 6: Fuel Gas Low *)
IF bWarn_StackO2_H      THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000080; END_IF; (* Bit 7: Stack O2 High *)
IF bWarn_StackO2_L      THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000100; END_IF; (* Bit 8: Stack O2 Low *)
IF bWarn_TLE_H          THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000200; END_IF; (* Bit 9: TLE Temp High *)
IF bWarn_TLE_L          THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000400; END_IF; (* Bit 10: TLE Temp Low *)
IF bWarn_DSRatio_L      THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000800; END_IF; (* Bit 11: Dilution Steam Low *)
IF bWarn_StackCO_H      THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00001000; END_IF; (* Bit 12: Stack CO High *)
IF bWarn_PassSpread_H   THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00002000; END_IF; (* Bit 13: Pass Spread High *)
IF bWarn_CokeLimit_H    THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00004000; END_IF; (* Bit 14: Coking Warning *)
IF bWarn_StackNOx_H     THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00008000; END_IF; (* Bit 15: NOx High *)
IF bWarn_IDFan_Saturation THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00010000; END_IF; (* Bit 16: ID Fan Saturation *)
IF bWarn_SensorTMR_Discrepancy THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00020000; END_IF; (* Bit 17: TMR Discrepancy *)

(* Pack dwStatusWord1: Subsystem Health & Operational Permissives *)
dwStatusWord1 := 16#00000000;
IF bEnable              THEN dwStatusWord1 := dwStatusWord1 OR 16#00000001; END_IF; (* Bit 0: Master Enable *)
IF bSafetyInterlock_OK  THEN dwStatusWord1 := dwStatusWord1 OR 16#00000002; END_IF; (* Bit 1: SIS Permissive OK *)
IF bFurnace_Ready       THEN dwStatusWord1 := dwStatusWord1 OR 16#00000004; END_IF; (* Bit 2: Furnace Ready *)
IF bFurnace_OnSpec      THEN dwStatusWord1 := dwStatusWord1 OR 16#00000008; END_IF; (* Bit 3: Furnace On-Spec *)
IF bDecoke_Active       THEN dwStatusWord1 := dwStatusWord1 OR 16#00000010; END_IF; (* Bit 4: Decoking Active *)
IF bManualOverride_En   THEN dwStatusWord1 := dwStatusWord1 OR 16#00000020; END_IF; (* Bit 5: Manual Override *)
IF bMPC_Feasible        THEN dwStatusWord1 := dwStatusWord1 OR 16#00000040; END_IF; (* Bit 6: MPC Feasible *)
(* Pack Current FSM State ID into Bits 8..15 *)
dwStatusWord1 := dwStatusWord1 OR SHL(INT_TO_DWORD(nState AND 16#00FF), 8);

(* Pack dwStatusWord2: TMR Degradation & Sensor Triplet Health *)
dwStatusWord2 := 16#00000000;
IF bDegraded_COT_Pass1     THEN dwStatusWord2 := dwStatusWord2 OR 16#00000001; END_IF; (* Bit 0: COT P1 Degraded *)
IF bDegraded_COT_Pass2     THEN dwStatusWord2 := dwStatusWord2 OR 16#00000002; END_IF; (* Bit 1: COT P2 Degraded *)
IF bDegraded_COT_Pass3     THEN dwStatusWord2 := dwStatusWord2 OR 16#00000004; END_IF; (* Bit 2: COT P3 Degraded *)
IF bDegraded_COT_Pass4     THEN dwStatusWord2 := dwStatusWord2 OR 16#00000008; END_IF; (* Bit 3: COT P4 Degraded *)
IF bDegraded_COT_Pass5     THEN dwStatusWord2 := dwStatusWord2 OR 16#00000010; END_IF; (* Bit 4: COT P5 Degraded *)
IF bDegraded_COT_Pass6     THEN dwStatusWord2 := dwStatusWord2 OR 16#00000020; END_IF; (* Bit 5: COT P6 Degraded *)
IF bDegraded_COT_Pass7     THEN dwStatusWord2 := dwStatusWord2 OR 16#00000040; END_IF; (* Bit 6: COT P7 Degraded *)
IF bDegraded_COT_Pass8     THEN dwStatusWord2 := dwStatusWord2 OR 16#00000080; END_IF; (* Bit 7: COT P8 Degraded *)
IF bDegraded_FuelGas_Press THEN dwStatusWord2 := dwStatusWord2 OR 16#00000100; END_IF; (* Bit 8: Fuel Gas Degraded *)
IF bDegraded_Draft_Press   THEN dwStatusWord2 := dwStatusWord2 OR 16#00000200; END_IF; (* Bit 9: Draft Degraded *)
IF bDegraded_FlueGas_O2    THEN dwStatusWord2 := dwStatusWord2 OR 16#00000400; END_IF; (* Bit 10: Flue O2 Degraded *)
IF bDegraded_TLE_Temp      THEN dwStatusWord2 := dwStatusWord2 OR 16#00000800; END_IF; (* Bit 11: TLE Temp Degraded *)
IF bTMR_Degraded_Warning   THEN dwStatusWord2 := dwStatusWord2 OR 16#80000000; END_IF; (* Bit 31: Any TMR Degraded *)

END_FUNCTION_BLOCK
""")

    code = "".join(parts)
    return code

if __name__ == "__main__":
    st_code = generate_iec_st()
    print("Generated ST code length:", len(st_code), "characters")
    with open("test_generated.st", "w", encoding="utf-8") as f:
        f.write(st_code)
    print("Wrote test_generated.st")
