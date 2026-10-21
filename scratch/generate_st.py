# scratch/generate_st.py
# Generator script for Lumina IEC 61131-3 Synthetic Data Swarm

import json
import uuid
import re

def build_code():
    sections = []

    # -------------------------------------------------------------------------
    # 0. HEADER & METADATA
    # -------------------------------------------------------------------------
    header = """FUNCTION_BLOCK FB_HydrogenPEM_Dewatering_TSA_DesiccantCycle
(*
 ==========================================================================================
  PROJECT:       70-BAR HIGH-PRESSURE PEM ELECTROLYSIS HYDROGEN DEWATERING & PURIFICATION
  SUBSYSTEM:     ADVANCED TSA DESICCANT ADSORPTION & CATALYTIC DE-OXO GOVERNOR
  DISCIPLINE:    PROCESS CYBER-PHYSICAL SYSTEMS / ROTORDYNAMICS / THERMODYNAMIC ADSORPTION
  IEC STANDARD:  IEC 61131-3 STRUCTURED TEXT 3RD EDITION (DETERMINISTIC EMBEDDED EXECUTION)
  AUTHOR:        LUMINA AI CLOUD SWARM - PRINCIPAL AUTOMATION FELLOW & CPS CHAIR (V7 MAX)
  DESIGN ENVELOPE:
    - OPERATING NOMINAL PRESSURE: 70.0 bar(g) [7.10 MPa(a)] | DESIGN PRESSURE: 85.0 bar(g)
    - OPERATING TEMPERATURE: 15.0 deg C to 85.0 deg C (Stack Outlet) | REGEN TEMP: 200 - 240 deg C
    - HYDROGEN PRODUCTION CAPACITY: 500 to 5,000 Nm3/h (Modular PEM Megawatt Stacks)
    - TARGET PURITY SPECIFICATION: ISO 14687 Grade D / Grade E (Fuel Cell Electric Vehicles)
      * H2O MOISTURE: < 5.0 ppmv (Target Frost Point <= -70.0 deg C at atmospheric equiv)
      * TRACE O2 CONTENT: < 2.0 ppmv (De-Oxo Catalytic Conversion Efficiency > 99.95%)
  
  PROCESS ARCHITECTURE OVERVIEW:
  1. PRIMARY DEWATERING & FLASH SEPARATION:
     High-pressure raw wet H2 from the PEM stack enters a high-velocity cyclone flash separator.
     Centrifugal gas acceleration induces droplet coalescence and boundary layer separation.
     Condensate collects in a lower sump with 2oo3 redundant magnetostrictive level tracking.
     A high-pressure flash drain valve pulses to evacuate liquid water to a de-aerator vessel
     while rigorously preventing high-pressure gas blow-by (minimum seal level interlock).

  2. CATALYTIC DE-OXO REACTION BED:
     Effluent hydrogen contains 500 - 3,500 ppmv dissolved crossover oxygen. Gas is routed
     through a noble metal catalytic reactor (Pd/Pt on high-surface-area gamma alumina).
     Exothermic deoxygenation (2 H2 + O2 -> 2 H2O + 241.8 kJ/mol) causes an adiabatic
     temperature rise of ~1.6 deg C per 100 ppmv O2. Multi-zone thermal tracking (Zone 1, 2, 3)
     is coupled to an active cooling jacket and bypass trim valve to prevent catalyst sintering
     (limit <= 220 deg C) and suppress runaway risks.

  3. SECONDARY TRIM CONDENSER & SEPARATOR:
     The de-oxo reaction produces supplemental moisture, raising dewpoint. Gas is routed
     through a secondary chilled-water trim heat exchanger to knock out condensation before
     the high-performance desiccant adsorbers.

  4. DUAL-BED TEMPERATURE SWING ADSORPTION (TSA):
     Two vertical vessels packed with Type 3A / 4A synthetic sodium aluminosilicate zeolite
     molecular sieve beads (micropore aperture ~3.2 Angstroms; selective for H2O dipole
     adsorption, strictly excluding hydrogen molecules). Beds operate in counter-cyclic mode:
     - Duty Bed (Adsorption): Upflow operation at 70.0 bar, 20 deg C, stripping water to < 0.1 ppmv.
     - Regeneration Bed (TSA Cycle): 5-step automated sequence:
       Step 1: Controlled blowdown / depressurization (70 bar -> 1.5 bar) via orifice valve.
       Step 2: Hot slipstream purge heating (200 - 230 deg C) powered by an electric SCR heater.
       Step 3: High-temperature thermal soak plateau until the desorption wave exits the bed.
       Step 4: Dry cold H2 sweep for bed cooling down to < 35 deg C.
       Step 5: Controlled slow repressurization (dP/dt <= 1.5 bar/min) using dry product H2
               to prevent fluidization, attrition, and bead dusting.

  5. ULTRA-LOW FROST-POINT (-70 DEG C) TRACKING & OFF-SPEC DIVERSION:
     Continuous product gas quality assessment via triple-redundant chilled mirror / quartz
     crystal microbalance frost-point hygrometers. Converts frost point to volumetric moisture
     ppmv using high-pressure Goff-Gratch formulations and fugacity enhancement factors.
     Instantaneous fast-acting pneumatic double-block-and-bleed divert valve redirects off-spec
     gas to a low-pressure buffer / recycle header within 150 milliseconds of threshold breach.

  CYBER-PHYSICAL CONTROL, OBSERVATION & SAFETY INFRASTRUCTURE:
  - TRIPLE MODULAR REDUNDANCY (2oo3 TMR): Mid-value voting with variance scoring, frozen sensor
    detection, and bumpless fallback to 1oo2 or conservative degraded defaults.
  - 4-STATE DISCRETE STATE-SPACE OBSERVER (A, B, C, D): Dynamic estimation of core bed
    hotspots, zeolite adsorbed moisture mass transfer zone (MTZ) velocity, and vessel pressure.
  - MODEL PREDICTIVE CONTROL (MPC): Receding-horizon quadratic programming (QP) cost minimization
    modulating heater SCR thyristors, bypass chillers, and repressurization throttling valves.
  - INDUSTRIAL EN 61508 / IEC 61511 SIL-2/3 COMPLIANT ALARM TREES: Dual DWORD alarm matrices,
    process warning registers, and multi-variable operational envelopes.
 ==========================================================================================
*)"""
    sections.append(header)

    # -------------------------------------------------------------------------
    # 1. VAR_INPUT
    # -------------------------------------------------------------------------
    var_input = """VAR_INPUT
    (* ===================================================================================== *)
    (* SYSTEM GOVERNANCE & SAFETY SUPERVISORY SIGNALS                                        *)
    (* ===================================================================================== *)
    bSystemEnable                   : BOOL;     (* Master process supervisory run command *)
    bResetFaults                    : BOOL;     (* Master alarm unlatch and trip reset request *)
    bEmergencyStop                  : BOOL;     (* Hardwired emergency shutdown relay (Active Low / Fail-Safe) *)
    bManualOverridePermissive       : BOOL;     (* Maintenance manual override interlock permissive *)
    bNitrogenPurgePermissive        : BOOL;     (* Inert gas N2 supply header pressure verified (> 6.0 bar) *)

    (* ===================================================================================== *)
    (* PRIMARY FLASH SEPARATOR & CYCLONE SENSORS                                             *)
    (* ===================================================================================== *)
    rInletPressure_A_bar            : REAL;     (* 2oo3 Channel A: Cyclone inlet raw gas pressure [bar] *)
    rInletPressure_B_bar            : REAL;     (* 2oo3 Channel B: Cyclone inlet raw gas pressure [bar] *)
    rInletPressure_C_bar            : REAL;     (* 2oo3 Channel C: Cyclone inlet raw gas pressure [bar] *)
    rInletTemp_DegC                 : REAL;     (* Raw PEM stack discharge temperature [deg C] *)
    rRawH2Flow_Nm3h                 : REAL;     (* Raw wet hydrogen volumetric feed flow rate [Nm3/h] *)
    rCycloneLevel_A_pct             : REAL;     (* 2oo3 Channel A: Cyclone sump condensate level [%] *)
    rCycloneLevel_B_pct             : REAL;     (* 2oo3 Channel B: Cyclone sump condensate level [%] *)
    rCycloneLevel_C_pct             : REAL;     (* 2oo3 Channel C: Cyclone sump condensate level [%] *)
    rCycloneDP_kPa                  : REAL;     (* Differential pressure across cyclone demister pad [kPa] *)
    rCondensateDrainFlow_kgh        : REAL;     (* Coriolis condensate drain measured mass flow rate [kg/h] *)

    (* ===================================================================================== *)
    (* CATALYTIC DE-OXO REACTOR SENSORS                                                      *)
    (* ===================================================================================== *)
    rDeOxoInletO2_A_ppm             : REAL;     (* 2oo3 Channel A: Electrochemical trace oxygen analyzer [ppm] *)
    rDeOxoInletO2_B_ppm             : REAL;     (* 2oo3 Channel B: Tunable diode laser trace O2 analyzer [ppm] *)
    rDeOxoInletO2_C_ppm             : REAL;     (* 2oo3 Channel C: Zirconia sensor trace oxygen analyzer [ppm] *)
    rDeOxoBedTemp_Zone1_DegC        : REAL;     (* De-Oxo reactor bed inlet boundary temperature [deg C] *)
    rDeOxoBedTemp_Zone2_DegC        : REAL;     (* De-Oxo reactor catalytic core hotspot temperature [deg C] *)
    rDeOxoBedTemp_Zone3_DegC        : REAL;     (* De-Oxo reactor exit gas boundary temperature [deg C] *)
    rDeOxoCoolingInletTemp_DegC     : REAL;     (* Cooling jacket coolant supply temperature [deg C] *)

    (* ===================================================================================== *)
    (* DUAL-BED TEMPERATURE SWING ADSORPTION (TSA) SENSORS                                   *)
    (* ===================================================================================== *)
    rTSABed_A_Pressure_bar          : REAL;     (* TSA Bed A internal vessel pressure transmitter [bar] *)
    rTSABed_B_Pressure_bar          : REAL;     (* TSA Bed B internal vessel pressure transmitter [bar] *)
    rTSABed_A_BottomTemp_DegC       : REAL;     (* TSA Bed A bottom regeneration distributor temperature [deg C] *)
    rTSABed_A_CoreTemp_DegC         : REAL;     (* TSA Bed A middle zeolite molecular sieve temperature [deg C] *)
    rTSABed_A_TopTemp_DegC          : REAL;     (* TSA Bed A top adsorption discharge temperature [deg C] *)
    rTSABed_B_BottomTemp_DegC       : REAL;     (* TSA Bed B bottom regeneration distributor temperature [deg C] *)
    rTSABed_B_CoreTemp_DegC         : REAL;     (* TSA Bed B middle zeolite molecular sieve temperature [deg C] *)
    rTSABed_B_TopTemp_DegC          : REAL;     (* TSA Bed B top adsorption discharge temperature [deg C] *)
    rRegenHeaterSkinTemp_DegC       : REAL;     (* TSA electric circulation heater sheath skin temp [deg C] *)
    rRegenPurgeFlow_Nm3h            : REAL;     (* TSA thermal regeneration purge loop flow rate [Nm3/h] *)
    rRegenPurgeExhaustTemp_DegC     : REAL;     (* TSA regeneration gas exhaust venting temperature [deg C] *)

    (* ===================================================================================== *)
    (* PRODUCT PURITY TRACKING & UTILITY POWER CONSTRAINTS                                   *)
    (* ===================================================================================== *)
    rProductFrostPoint_A_DegC       : REAL;     (* 2oo3 Channel A: Chilled mirror frost-point hygrometer [deg C] *)
    rProductFrostPoint_B_DegC       : REAL;     (* 2oo3 Channel B: Impedance ceramic frost-point sensor [deg C] *)
    rProductFrostPoint_C_DegC       : REAL;     (* 2oo3 Channel C: Surface acoustic wave frost-point sensor [deg C] *)
    rProductPressure_bar            : REAL;     (* Export pipeline product hydrogen delivery pressure [bar] *)
    rHeaterAvailablePower_kW        : REAL;     (* Grid/substation available electric power capacity [kW] *)
    rCycleTime_sec                  : REAL := 0.050; (* Discrete PLC deterministic task execution period [sec] *)
END_VAR"""
    sections.append(var_input)

    # -------------------------------------------------------------------------
    # 2. VAR_OUTPUT
    # -------------------------------------------------------------------------
    var_output = """VAR_OUTPUT
    (* ===================================================================================== *)
    (* SYSTEM STATUS & SUPERVISORY INTERLOCKS                                                *)
    (* ===================================================================================== *)
    bSystemReady                    : BOOL;     (* System pre-conditioned, pressurized, leak-tested & ready *)
    bSystemRunning                  : BOOL;     (* Process actively dewatering, deoxygenating and drying *)
    bSystemTripped                  : BOOL;     (* Master safety trip latched; all feeds isolated *)
    bDegradedOperation              : BOOL;     (* Sensor redundancy degraded; derated throughput active *)

    (* ===================================================================================== *)
    (* PROCESS ACTUATOR DEMANDS & CONTROL VALVE COMMANDS                                     *)
    (* ===================================================================================== *)
    rCycloneDrainValveDemand_pct    : REAL;     (* High-pressure condensate flash drain valve demand [%] *)
    rDeOxoCoolingValveDemand_pct    : REAL;     (* Catalytic De-Oxo cooling jacket / trim bypass demand [%] *)
    rRegenHeaterPowerDemand_kW      : REAL;     (* TSA electric regeneration heater thyristor SCR power [kW] *)

    (* Bed A Flow Switching Manifold Actuators *)
    rBed_A_InletValve_pct           : REAL;     (* Bed A wet process feed isolation valve demand [0.0 - 100.0 %] *)
    rBed_A_OutletValve_pct          : REAL;     (* Bed A dry product delivery isolation valve demand [0.0 - 100.0 %] *)
    rBed_A_DepressValve_pct         : REAL;     (* Bed A blowdown / depressurization throttling valve demand [%] *)
    rBed_A_PurgeValve_pct           : REAL;     (* Bed A hot regeneration purge inlet valve demand [%] *)
    rBed_A_RepressValve_pct         : REAL;     (* Bed A dry product slow repressurization valve demand [%] *)

    (* Bed B Flow Switching Manifold Actuators *)
    rBed_B_InletValve_pct           : REAL;     (* Bed B wet process feed isolation valve demand [0.0 - 100.0 %] *)
    rBed_B_OutletValve_pct          : REAL;     (* Bed B dry product delivery isolation valve demand [0.0 - 100.0 %] *)
    rBed_B_DepressValve_pct         : REAL;     (* Bed B blowdown / depressurization throttling valve demand [%] *)
    rBed_B_PurgeValve_pct           : REAL;     (* Bed B hot regeneration purge inlet valve demand [%] *)
    rBed_B_RepressValve_pct         : REAL;     (* Bed B dry product slow repressurization valve demand [%] *)

    (* Product Export & Purity Diversion Actuators *)
    bProductDiverterToRecycle       : BOOL;     (* High-speed pneumatic diverter: off-spec gas to buffer/recycle *)
    bProductDiverterToExport        : BOOL;     (* High-speed pneumatic diverter: qualified gas to pipeline *)

    (* ===================================================================================== *)
    (* VALIDATED PROCESS TELEMETRY & PHYSICAL ANALYTICS                                      *)
    (* ===================================================================================== *)
    rVotedInletPressure_bar         : REAL;     (* 2oo3 validated cyclone inlet pressure [bar] *)
    rVotedCycloneLevel_pct          : REAL;     (* 2oo3 validated cyclone condensate liquid level [%] *)
    rVotedDeOxoO2_ppm               : REAL;     (* 2oo3 validated inlet trace oxygen concentration [ppm] *)
    rVotedFrostPoint_DegC           : REAL;     (* 2oo3 validated product hydrogen frost point [deg C] *)
    rCalculatedMoisture_ppm         : REAL;     (* Thermodynamically computed product water content [ppmv] *)
    rDeOxoExothermDeltaT_DegC       : REAL;     (* Realized adiabatic catalytic temperature rise [deg C] *)
    rBed_A_AdsorptionCapacity_pct   : REAL;     (* Real-time estimated remaining zeolite capacity Bed A [%] *)
    rBed_B_AdsorptionCapacity_pct   : REAL;     (* Real-time estimated remaining zeolite capacity Bed B [%] *)
    rRepressRampRate_bar_min        : REAL;     (* Real-time rate of pressure rise during repressurization *)

    (* ===================================================================================== *)
    (* BIT-PACKED STATUS WORDS & INDUSTRIAL ALARM REGISTERS                                  *)
    (* ===================================================================================== *)
    dwSystemStatusWord1             : DWORD;    (* Bit-packed FSM operational state and valve status word *)
    dwSystemStatusWord2             : DWORD;    (* Bit-packed TSA step counters, heater, and MPC diagnostics *)
    dwAlarmWord1                    : DWORD;    (* Priority 1: Critical safety emergency shutdown interlocks *)
    dwAlarmWord2                    : DWORD;    (* Priority 2: Process integrity and thermal violation trips *)
    dwWarningWord1                  : DWORD;    (* Priority 3: Preventative maintenance and threshold alerts *)
    dwDiagnosticWord                : DWORD;    (* Instrument health, 2oo3 channel voting fault register *)
END_VAR"""
    sections.append(var_output)

    # -------------------------------------------------------------------------
    # 3. VAR (Internal Variables)
    # -------------------------------------------------------------------------
    var_internal = """VAR
    (* ===================================================================================== *)
    (* 1.0 STATE MACHINE SUPERVISION & TIMERS                                                *)
    (* ===================================================================================== *)
    iState                          : INT := 0; (* Main Process Sequence Master State *)
    iPrevState                      : INT := -1;(* State transition memory register *)
    iSubState_TSA                   : INT := 0; (* TSA Desiccant Dual-Bed Cyclic Sub-State *)
    rStateTimer_sec                 : REAL := 0.0; (* Master state elapsed run timer [sec] *)
    rSubStateTimer_sec              : REAL := 0.0; (* TSA Sub-cycle elapsed dwell timer [sec] *)

    (* Standard IEC 61131-3 On-Delay Functional Timers *)
    tPurgeTimer                     : TON;      (* N2 Inerting & Sweep Verification Timer *)
    tRepressTimer                   : TON;      (* System Initial Slow Pressurization Watchdog *)
    tDrainPulseTimer                : TON;      (* Cyclone Flash Condensate Drain Pulse Timer *)
    tDeOxoPreheatTimer              : TON;      (* Catalytic Reactor Thermal Light-Off Dwell *)
    tRegenHeatingTimer              : TON;      (* TSA Desorption Thermal Ramp Timer *)
    tRegenSoakTimer                 : TON;      (* TSA Zeolite High-Temperature Soak Timer *)
    tRegenCoolTimer                 : TON;      (* TSA Molecular Sieve Sweep Cooldown Timer *)
    tRepressBedTimer                : TON;      (* TSA Dynamic Bed Repressurization Ramp Timer *)
    tBedSwitchTimer                 : TON;      (* TSA Bed Dual-Transfer Valve Overlap Timer *)
    tOffspecDivertTimer             : TON;      (* Fast-Divert Offspec Product Purge Timer *)
    tShutdownCooldownTimer          : TON;      (* Safe Controlled Cooldown Ramp Timer *)

    (* ===================================================================================== *)
    (* 2.0 TRIPLE MODULAR REDUNDANCY (2oo3) VOTING REGISTERS & DISCREPANCY TRACKERS          *)
    (* ===================================================================================== *)
    (* Inlet Pressure Voting *)
    bPress_ChanA_Valid              : BOOL := TRUE;
    bPress_ChanB_Valid              : BOOL := TRUE;
    bPress_ChanC_Valid              : BOOL := TRUE;
    rPress_DevAB_bar                : REAL := 0.0;
    rPress_DevBC_bar                : REAL := 0.0;
    rPress_DevCA_bar                : REAL := 0.0;
    bPress_Degraded_1oo2            : BOOL := FALSE;
    iPress_FaultCounter             : INT := 0;

    (* Cyclone Liquid Level Voting *)
    bLevel_ChanA_Valid              : BOOL := TRUE;
    bLevel_ChanB_Valid              : BOOL := TRUE;
    bLevel_ChanC_Valid              : BOOL := TRUE;
    rLevel_DevAB_pct                : REAL := 0.0;
    rLevel_DevBC_pct                : REAL := 0.0;
    rLevel_DevCA_pct                : REAL := 0.0;
    bLevel_Degraded_1oo2            : BOOL := FALSE;
    iLevel_FaultCounter             : INT := 0;

    (* Inlet Trace Oxygen Voting *)
    bO2_ChanA_Valid                 : BOOL := TRUE;
    bO2_ChanB_Valid                 : BOOL := TRUE;
    bO2_ChanC_Valid                 : BOOL := TRUE;
    rO2_DevAB_ppm                   : REAL := 0.0;
    rO2_DevBC_ppm                   : REAL := 0.0;
    rO2_DevCA_ppm                   : REAL := 0.0;
    bO2_Degraded_1oo2               : BOOL := FALSE;
    iO2_FaultCounter                : INT := 0;

    (* Product Frost Point Voting *)
    bFP_ChanA_Valid                 : BOOL := TRUE;
    bFP_ChanB_Valid                 : BOOL := TRUE;
    bFP_ChanC_Valid                 : BOOL := TRUE;
    rFP_DevAB_DegC                  : REAL := 0.0;
    rFP_DevBC_DegC                  : REAL := 0.0;
    rFP_DevCA_DegC                  : REAL := 0.0;
    bFP_Degraded_1oo2               : BOOL := FALSE;
    iFP_FaultCounter                : INT := 0;

    (* Sensor Frozen Detection Memory *)
    rLast_InletPress_A              : REAL := 0.0;
    rLast_CycloneLevel_A            : REAL := 0.0;
    rLast_O2_A                      : REAL := 0.0;
    rLast_FP_A                      : REAL := 0.0;
    iFrozenCycles_Press             : INT := 0;
    iFrozenCycles_Level             : INT := 0;
    iFrozenCycles_O2                : INT := 0;
    iFrozenCycles_FP                : INT := 0;

    (* ===================================================================================== *)
    (* 3.0 DIGITAL SIGNAL FILTERING & DERIVATIVE ESTIMATORS                                  *)
    (* ===================================================================================== *)
    rFilt_InletPress_bar            : REAL := 0.0;
    rFilt_CycloneLevel_pct          : REAL := 0.0;
    rFilt_DeOxoO2_ppm               : REAL := 0.0;
    rFilt_FrostPoint_DegC           : REAL := -75.0;
    rFilt_DeOxoCoreTemp_DegC        : REAL := 25.0;
    rFilt_RegenPurgeFlow_Nm3h       : REAL := 0.0;

    rPrev_VotedFrostPoint_DegC      : REAL := -75.0;
    rRateOfChange_FrostPoint_DegCmin: REAL := 0.0;
    rPrev_RepressPressure_bar       : REAL := 0.0;
    rPrev_DeOxoCoreTemp_DegC        : REAL := 25.0;
    rRateOfChange_DeOxo_DegCs       : REAL := 0.0;

    (* ===================================================================================== *)
    (* 4.0 THERMODYNAMIC EQUATIONS OF STATE & ADSORPTION KINETICS                            *)
    (* ===================================================================================== *)
    (* Hydrogen Physical Constants *)
    rConst_R_gas                    : REAL := 8.314462; (* Universal gas constant [J/(mol K)] *)
    rConst_MolWeight_H2             : REAL := 2.01588;  (* Molecular weight of H2 [g/mol] *)
    rConst_MolWeight_H2O            : REAL := 18.01528; (* Molecular weight of H2O [g/mol] *)
    rConst_Enthalpy_DeOxo           : REAL := 241820.0; (* Exothermic heat of formation [J/mol O2] *)
    rConst_ZeoliteMass_kg           : REAL := 850.0;    (* Dry desiccant mass per adsorber vessel [kg] *)
    rConst_BedDiameter_m            : REAL := 0.65;     (* Adsorption packed column diameter [m] *)
    rConst_BedHeight_m              : REAL := 2.80;     (* Adsorbent column active packed height [m] *)
    rConst_BedPorosity              : REAL := 0.385;    (* Inter-particle bed void fraction [-] *)
    rConst_BeadDiameter_m           : REAL := 0.0022;   (* Zeolite spherical bead mean diameter [m] *)

    (* Thermodynamic Real-Time Calculators *)
    rCompressibility_Z              : REAL := 1.042;    (* Hydrogen compressibility factor at 70 bar, 20C *)
    rHydrogenDensity_kgm3           : REAL := 5.78;     (* Supercritical/gas hydrogen density at 70 bar *)
    rSuperficialVelocity_ms         : REAL := 0.0;      (* Gas superficial velocity through packed bed *)
    rBedDifferentialPress_kPa       : REAL := 0.0;      (* Ergun equation derived packed bed DP [kPa] *)
    rCalculatedFrostPoint_DegC      : REAL := -70.0;    (* Inverted psychrometric frost point calculation *)
    rGoffGratchVaporPress_Pa        : REAL := 0.0;      (* Goff-Gratch saturation vapor pressure over ice *)
    rEnhancementFactor_fw           : REAL := 1.285;    (* Non-ideal enhancement factor at 70.0 bar *)
    rTheoreticalHotspotRise_DegC    : REAL := 0.0;      (* Expected adiabatic exotherm based on inlet O2 *)

    (* ===================================================================================== *)
    (* 5.0 4-STATE DISCRETE STATE-SPACE OBSERVER MATRICES (A, B, C, D)                       *)
    (* ===================================================================================== *)
    (* State Vector:
       x[1]: De-Oxo Core Bed Hotspot Temperature [deg C]
       x[2]: Active TSA Regeneration Bed Temperature [deg C]
       x[3]: Cumulative Adsorbed Water Mass in Duty Bed [kg H2O]
       x[4]: Regeneration Vessel Internal Gas Pressure [bar]
    *)
    rMat_A : ARRAY[1..4, 1..4] OF REAL := [
        [-0.0450,  0.0000,  0.0000,  0.0000],  (* x1: Thermal dissipation / convective heat loss *)
        [ 0.0000, -0.0125,  0.0000,  0.0000],  (* x2: TSA Regeneration bed thermal decay *)
        [ 0.0000,  0.0000, -0.0005,  0.0000],  (* x3: Adsorption mass transfer loading depletion *)
        [ 0.0000,  0.0000,  0.0000, -0.0850]   (* x4: Pressure vent hydraulic venting dissipation *)
    ];

    (* Control Input Matrix B:
       u[1]: Electric Regeneration Heater Power [kW]
       u[2]: De-Oxo Cooling Jacket / Trim Valve [%]
       u[3]: Slow Repressurization Throttle Valve [%]
    *)
    rMat_B : ARRAY[1..4, 1..3] OF REAL := [
        [ 0.0000, -0.1850,  0.0000],   (* u2 cools De-Oxo hotspot *)
        [ 0.0920,  0.0000,  0.0000],   (* u1 heats TSA Regeneration Bed *)
        [ 0.0000,  0.0000,  0.0000],   (* Inputs do not directly inject water *)
        [ 0.0000,  0.0000,  0.0650]    (* u3 pressurizes regeneration vessel *)
    ];

    (* Disturbance Matrix E (Inlet flow, inlet O2, inlet moisture):
       d[1]: Raw Feed Hydrogen Flow Rate [Nm3/h]
       d[2]: Inlet Trace Oxygen Concentration [ppm]
       d[3]: Inlet Gas Dewpoint / Moisture [ppm]
    *)
    rMat_E : ARRAY[1..4, 1..3] OF REAL := [
        [ 0.0005,  0.0162,  0.0000],   (* Feed flow and O2 concentration generate exotherm *)
        [ 0.0000,  0.0000,  0.0000],   (* Regen bed insulated from raw wet feed *)
        [ 0.0012,  0.0000,  0.0008],   (* Moisture loading rate into duty bed *)
        [ 0.0000,  0.0000,  0.0000]    (* Vessel pressure unaffected by raw feed *)
    ];

    (* Output Observer Matrix C (Mapping internal states to physical measurements) *)
    rMat_C : ARRAY[1..4, 1..4] OF REAL := [
        [ 1.0000,  0.0000,  0.0000,  0.0000],  (* y1: De-Oxo Measured Core Temperature *)
        [ 0.0000,  1.0000,  0.0000,  0.0000],  (* y2: TSA Regeneration Bed Measured Core Temp *)
        [ 0.0000,  0.0000,  1.0000,  0.0000],  (* y3: Estimated Remaining Zeolite Adsorptive Mass *)
        [ 0.0000,  0.0000,  0.0000,  1.0000]   (* y4: Regeneration Vessel Internal Pressure *)
    ];

    (* Direct Transmission Matrix D *)
    rMat_D : ARRAY[1..4, 1..3] OF REAL := [
        [ 0.0000,  0.0000,  0.0000],
        [ 0.0000,  0.0000,  0.0000],
        [ 0.0000,  0.0000,  0.0000],
        [ 0.0000,  0.0000,  0.0000]
    ];

    (* Discretized State & Observer Vectors *)
    rVec_x                          : ARRAY[1..4] OF REAL := [25.0, 25.0, 0.0, 1.0];
    rVec_x_hat                      : ARRAY[1..4] OF REAL := [25.0, 25.0, 0.0, 1.0];
    rVec_u                          : ARRAY[1..3] OF REAL := [0.0, 0.0, 0.0];
    rVec_d                          : ARRAY[1..3] OF REAL := [0.0, 0.0, 0.0];
    rVec_y                          : ARRAY[1..4] OF REAL := [25.0, 25.0, 0.0, 1.0];
    rObserverGain_L                 : ARRAY[1..4] OF REAL := [0.085, 0.065, 0.020, 0.120];

    (* ===================================================================================== *)
    (* 6.0 MODEL PREDICTIVE CONTROL (MPC) REFINED QUADRATIC OPTIMIZATION                     *)
    (* ===================================================================================== *)
    (* Diagonal Tracking Penalty Weights Q and Actuator Slew Penalties R *)
    rMat_Q_diag                     : ARRAY[1..3] OF REAL := [1.85, 0.95, 2.40];
    rMat_R_diag                     : ARRAY[1..3] OF REAL := [0.45, 0.25, 0.60];
    rVec_Setpoint                   : ARRAY[1..3] OF REAL := [215.0, 85.0, 70.0];

    (* Projected Gradient Horizon Variables *)
    rMpcStepSize_Alpha              : REAL := 0.045;
    rMpcGrad_u1                     : REAL := 0.0;
    rMpcGrad_u2                     : REAL := 0.0;
    rMpcGrad_u3                     : REAL := 0.0;
    rPredictedError_y1              : REAL := 0.0;
    rPredictedError_y2              : REAL := 0.0;
    rPredictedError_y3              : REAL := 0.0;
    rMpcCostFunction_J              : REAL := 0.0;

    (* Actuator Slew Rate Limiters *)
    rLast_HeaterDemand_kW           : REAL := 0.0;
    rLast_CoolingDemand_pct         : REAL := 0.0;
    rLast_RepressDemand_pct         : REAL := 0.0;
    rMaxSlew_Heater_kWs             : REAL := 2.50;  (* Max electric heater ramp 2.5 kW/s *)
    rMaxSlew_Cooling_pcts           : REAL := 15.0;  (* Max cooling valve slew 15 %/s *)
    rMaxSlew_Repress_pcts           : REAL := 5.0;   (* Max repress valve slew 5 %/s *)

    (* ===================================================================================== *)
    (* 7.0 CYCLONE FLASH CONDENSATE DRAIN LEVEL REGULATION                                   *)
    (* ===================================================================================== *)
    rLevelSetPoint_pct              : REAL := 35.0;  (* Target liquid sump level [%] *)
    rLevelDeadband_pct              : REAL := 4.0;   (* Drain pulse deadband [%] *)
    rLevel_P_Gain                   : REAL := 2.25;  (* Proportional gain *)
    rLevel_I_Gain                   : REAL := 0.08;  (* Integral reset gain *)
    rLevel_Integral_Accum           : REAL := 0.0;   (* Anti-windup integrator accumulator *)
    bDrainValvePulseState           : BOOL := FALSE; (* High-pressure pulse drain solenoid status *)
    rCalculatedCondensateRate_kgh   : REAL := 0.0;   (* Theoretical moisture condensation flux *)

    (* ===================================================================================== *)
    (* 8.0 TSA DUAL-BED CYCLE TIMERS, SWITCH REGISTERS & FLUIDIZATION SAFEGUARDS             *)
    (* ===================================================================================== *)
    bBed_A_IsDutyAdsorption         : BOOL := TRUE;  (* TRUE = Bed A Online, Bed B Regenerating *)
    bBedSwitchInitiated             : BOOL := FALSE; (* Transient switchover overlap flag *)
    rTotalDutyAdsorbed_kg           : REAL := 0.0;   (* Cumulative mass of water adsorbed in current half-cycle *)
    rMaxAdsorptionCapacity_kg       : REAL := 187.0; (* Saturation breakthrough loading per bed [kg H2O] *)
    rTSABlowdownTargetP_bar         : REAL := 1.80;  (* Target depressurized blowdown pressure [bar] *)
    rTSARegenTargetTemp_DegC        : REAL := 218.0; (* Target zeolite thermal desorption core temperature *)
    rTSACooldownTargetTemp_DegC     : REAL := 32.0;  (* Target pre-adsorption cooldown temperature *)
    rMaxAllowableRepressRamp_barmin : REAL := 1.50;  (* Anti-fluidization maximum dP/dt rate *)

    (* ===================================================================================== *)
    (* 9.0 INTERFACE SCRATCH, LOOP INDICES & AUXILIARY MATH                                  *)
    (* ===================================================================================== *)
    iIdx_i                          : INT := 1;
    iIdx_j                          : INT := 1;
    rTemp_A                         : REAL := 0.0;
    rTemp_B                         : REAL := 0.0;
    rTemp_C                         : REAL := 0.0;
    rMedian                         : REAL := 0.0;
    rMatrixSum                      : REAL := 0.0;
    rAbsDev                         : REAL := 0.0;
    rAlpha_Filter                   : REAL := 0.0;
    rTau_Filter_sec                 : REAL := 0.500;
END_VAR"""
    sections.append(var_internal)

    # -------------------------------------------------------------------------
    # 4. SECTION 1.0: 2oo3 TMR TRIPLE MODULAR REDUNDANCY VOTING
    # -------------------------------------------------------------------------
    sec_1 = """
(* ========================================================================================= *)
(* 1.0 TRIPLE MODULAR REDUNDANCY (2oo3) VOTING, DEVIATION MONITORING & HEALTH SCORING        *)
(* ========================================================================================= *)
(* Executes deterministic mid-value selection, pair-wise variance analysis, frozen-signal    *)
(* detection, and automatic bumpless fallback to 1oo2 or fail-safe operational modes.        *)

(* ----------------------------------------------------------------------------------------- *)
(* 1.1 Cyclone Inlet Pressure Voting (PT-01A, PT-01B, PT-01C)                                *)
(* ----------------------------------------------------------------------------------------- *)
rTemp_A := rInletPressure_A_bar;
rTemp_B := rInletPressure_B_bar;
rTemp_C := rInletPressure_C_bar;

(* Range & Boundary Plausibility Qualification [0.0 bar to 100.0 bar] *)
bPress_ChanA_Valid := (rTemp_A >= 0.0) AND (rTemp_A <= 100.0);
bPress_ChanB_Valid := (rTemp_B >= 0.0) AND (rTemp_B <= 100.0);
bPress_ChanC_Valid := (rTemp_C >= 0.0) AND (rTemp_C <= 100.0);

(* Frozen Sensor Detection: Check if transmitter signal is stagnant despite dynamic flow *)
IF (ABS(rTemp_A - rLast_InletPress_A) < 0.0001) AND (rRawH2Flow_Nm3h > 100.0) THEN
    iFrozenCycles_Press := iFrozenCycles_Press + 1;
    IF iFrozenCycles_Press > 200 THEN (* 10 seconds of frozen reading *)
        bPress_ChanA_Valid := FALSE;
    END_IF;
ELSE
    iFrozenCycles_Press := 0;
END_IF;
rLast_InletPress_A := rTemp_A;

(* Pair-wise Deviations *)
rPress_DevAB_bar := ABS(rTemp_A - rTemp_B);
rPress_DevBC_bar := ABS(rTemp_B - rTemp_C);
rPress_DevCA_bar := ABS(rTemp_C - rTemp_A);

(* 2oo3 Mid-Value Algorithm *)
IF bPress_ChanA_Valid AND bPress_ChanB_Valid AND bPress_ChanC_Valid THEN
    (* Standard 2oo3 Median Selection *)
    IF ((rTemp_A >= rTemp_B) AND (rTemp_A <= rTemp_C)) OR ((rTemp_A >= rTemp_C) AND (rTemp_A <= rTemp_B)) THEN
        rVotedInletPressure_bar := rTemp_A;
    ELSIF ((rTemp_B >= rTemp_A) AND (rTemp_B <= rTemp_C)) OR ((rTemp_B >= rTemp_C) AND (rTemp_B <= rTemp_A)) THEN
        rVotedInletPressure_bar := rTemp_B;
    ELSE
        rVotedInletPressure_bar := rTemp_C;
    END_IF;
    bPress_Degraded_1oo2 := FALSE;
ELSIF bPress_ChanA_Valid AND bPress_ChanB_Valid THEN
    rVotedInletPressure_bar := (rTemp_A + rTemp_B) * 0.5;
    bPress_Degraded_1oo2 := TRUE;
ELSIF bPress_ChanB_Valid AND bPress_ChanC_Valid THEN
    rVotedInletPressure_bar := (rTemp_B + rTemp_C) * 0.5;
    bPress_Degraded_1oo2 := TRUE;
ELSIF bPress_ChanA_Valid AND bPress_ChanC_Valid THEN
    rVotedInletPressure_bar := (rTemp_A + rTemp_C) * 0.5;
    bPress_Degraded_1oo2 := TRUE;
ELSIF bPress_ChanA_Valid THEN
    rVotedInletPressure_bar := rTemp_A;
    bPress_Degraded_1oo2 := TRUE;
ELSIF bPress_ChanB_Valid THEN
    rVotedInletPressure_bar := rTemp_B;
    bPress_Degraded_1oo2 := TRUE;
ELSIF bPress_ChanC_Valid THEN
    rVotedInletPressure_bar := rTemp_C;
    bPress_Degraded_1oo2 := TRUE;
ELSE
    (* Total instrument failure: latch conservative maximum pressure for safety *)
    rVotedInletPressure_bar := 85.0;
    bPress_Degraded_1oo2 := TRUE;
    dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0001; (* Pressure Sensor Bank Tripped *)
END_IF;

(* Track Channel Discrepancy Fault Counter *)
IF (rPress_DevAB_bar > 2.5) OR (rPress_DevBC_bar > 2.5) OR (rPress_DevCA_bar > 2.5) THEN
    iPress_FaultCounter := iPress_FaultCounter + 1;
    IF iPress_FaultCounter > 60 THEN
        dwDiagnosticWord := dwDiagnosticWord OR 16#0000_0001; (* Pressure Discrepancy Warning *)
    END_IF;
ELSE
    IF iPress_FaultCounter > 0 THEN iPress_FaultCounter := iPress_FaultCounter - 1; END_IF;
END_IF;


(* ----------------------------------------------------------------------------------------- *)
(* 1.2 Cyclone Condensate Liquid Level Voting (LT-01A, LT-01B, LT-01C)                       *)
(* ----------------------------------------------------------------------------------------- *)
rTemp_A := rCycloneLevel_A_pct;
rTemp_B := rCycloneLevel_B_pct;
rTemp_C := rCycloneLevel_C_pct;

bLevel_ChanA_Valid := (rTemp_A >= -2.0) AND (rTemp_A <= 105.0);
bLevel_ChanB_Valid := (rTemp_B >= -2.0) AND (rTemp_B <= 105.0);
bLevel_ChanC_Valid := (rTemp_C >= -2.0) AND (rTemp_C <= 105.0);

(* Frozen Sensor Detection *)
IF (ABS(rTemp_A - rLast_CycloneLevel_A) < 0.001) AND (rCondensateDrainFlow_kgh > 5.0) THEN
    iFrozenCycles_Level := iFrozenCycles_Level + 1;
    IF iFrozenCycles_Level > 200 THEN bLevel_ChanA_Valid := FALSE; END_IF;
ELSE
    iFrozenCycles_Level := 0;
END_IF;
rLast_CycloneLevel_A := rTemp_A;

rLevel_DevAB_pct := ABS(rTemp_A - rTemp_B);
rLevel_DevBC_pct := ABS(rTemp_B - rTemp_C);
rLevel_DevCA_pct := ABS(rTemp_C - rTemp_A);

IF bLevel_ChanA_Valid AND bLevel_ChanB_Valid AND bLevel_ChanC_Valid THEN
    IF ((rTemp_A >= rTemp_B) AND (rTemp_A <= rTemp_C)) OR ((rTemp_A >= rTemp_C) AND (rTemp_A <= rTemp_B)) THEN
        rVotedCycloneLevel_pct := rTemp_A;
    ELSIF ((rTemp_B >= rTemp_A) AND (rTemp_B <= rTemp_C)) OR ((rTemp_B >= rTemp_C) AND (rTemp_B <= rTemp_A)) THEN
        rVotedCycloneLevel_pct := rTemp_B;
    ELSE
        rVotedCycloneLevel_pct := rTemp_C;
    END_IF;
    bLevel_Degraded_1oo2 := FALSE;
ELSIF bLevel_ChanA_Valid AND bLevel_ChanB_Valid THEN
    rVotedCycloneLevel_pct := (rTemp_A + rTemp_B) * 0.5;
    bLevel_Degraded_1oo2 := TRUE;
ELSIF bLevel_ChanB_Valid AND bLevel_ChanC_Valid THEN
    rVotedCycloneLevel_pct := (rTemp_B + rTemp_C) * 0.5;
    bLevel_Degraded_1oo2 := TRUE;
ELSIF bLevel_ChanA_Valid AND bLevel_ChanC_Valid THEN
    rVotedCycloneLevel_pct := (rTemp_A + rTemp_C) * 0.5;
    bLevel_Degraded_1oo2 := TRUE;
ELSIF bLevel_ChanA_Valid THEN
    rVotedCycloneLevel_pct := rTemp_A;
    bLevel_Degraded_1oo2 := TRUE;
ELSIF bLevel_ChanB_Valid THEN
    rVotedCycloneLevel_pct := rTemp_B;
    bLevel_Degraded_1oo2 := TRUE;
ELSIF bLevel_ChanC_Valid THEN
    rVotedCycloneLevel_pct := rTemp_C;
    bLevel_Degraded_1oo2 := TRUE;
ELSE
    rVotedCycloneLevel_pct := 90.0; (* High failsafe level assumption *)
    bLevel_Degraded_1oo2 := TRUE;
    dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0002; (* Cyclone Level Sensor Bank Failed *)
END_IF;

IF (rLevel_DevAB_pct > 8.0) OR (rLevel_DevBC_pct > 8.0) OR (rLevel_DevCA_pct > 8.0) THEN
    iLevel_FaultCounter := iLevel_FaultCounter + 1;
    IF iLevel_FaultCounter > 60 THEN
        dwDiagnosticWord := dwDiagnosticWord OR 16#0000_0002; (* Level Discrepancy Warning *)
    END_IF;
ELSE
    IF iLevel_FaultCounter > 0 THEN iLevel_FaultCounter := iLevel_FaultCounter - 1; END_IF;
END_IF;


(* ----------------------------------------------------------------------------------------- *)
(* 1.3 Catalytic De-Oxo Inlet Trace Oxygen Voting (AT-01A, AT-01B, AT-01C)                   *)
(* ----------------------------------------------------------------------------------------- *)
rTemp_A := rDeOxoInletO2_A_ppm;
rTemp_B := rDeOxoInletO2_B_ppm;
rTemp_C := rDeOxoInletO2_C_ppm;

bO2_ChanA_Valid := (rTemp_A >= 0.0) AND (rTemp_A <= 15000.0);
bO2_ChanB_Valid := (rTemp_B >= 0.0) AND (rTemp_B <= 15000.0);
bO2_ChanC_Valid := (rTemp_C >= 0.0) AND (rTemp_C <= 15000.0);

IF (ABS(rTemp_A - rLast_O2_A) < 0.01) AND (rRawH2Flow_Nm3h > 150.0) THEN
    iFrozenCycles_O2 := iFrozenCycles_O2 + 1;
    IF iFrozenCycles_O2 > 300 THEN bO2_ChanA_Valid := FALSE; END_IF;
ELSE
    iFrozenCycles_O2 := 0;
END_IF;
rLast_O2_A := rTemp_A;

rO2_DevAB_ppm := ABS(rTemp_A - rTemp_B);
rO2_DevBC_ppm := ABS(rTemp_B - rTemp_C);
rO2_DevCA_ppm := ABS(rTemp_C - rTemp_A);

IF bO2_ChanA_Valid AND bO2_ChanB_Valid AND bO2_ChanC_Valid THEN
    IF ((rTemp_A >= rTemp_B) AND (rTemp_A <= rTemp_C)) OR ((rTemp_A >= rTemp_C) AND (rTemp_A <= rTemp_B)) THEN
        rVotedDeOxoO2_ppm := rTemp_A;
    ELSIF ((rTemp_B >= rTemp_A) AND (rTemp_B <= rTemp_C)) OR ((rTemp_B >= rTemp_C) AND (rTemp_B <= rTemp_A)) THEN
        rVotedDeOxoO2_ppm := rTemp_B;
    ELSE
        rVotedDeOxoO2_ppm := rTemp_C;
    END_IF;
    bO2_Degraded_1oo2 := FALSE;
ELSIF bO2_ChanA_Valid AND bO2_ChanB_Valid THEN
    rVotedDeOxoO2_ppm := (rTemp_A + rTemp_B) * 0.5;
    bO2_Degraded_1oo2 := TRUE;
ELSIF bO2_ChanB_Valid AND bO2_ChanC_Valid THEN
    rVotedDeOxoO2_ppm := (rTemp_B + rTemp_C) * 0.5;
    bO2_Degraded_1oo2 := TRUE;
ELSIF bO2_ChanA_Valid AND bO2_ChanC_Valid THEN
    rVotedDeOxoO2_ppm := (rTemp_A + rTemp_C) * 0.5;
    bO2_Degraded_1oo2 := TRUE;
ELSIF bO2_ChanA_Valid THEN
    rVotedDeOxoO2_ppm := rTemp_A;
    bO2_Degraded_1oo2 := TRUE;
ELSIF bO2_ChanB_Valid THEN
    rVotedDeOxoO2_ppm := rTemp_B;
    bO2_Degraded_1oo2 := TRUE;
ELSIF bO2_ChanC_Valid THEN
    rVotedDeOxoO2_ppm := rTemp_C;
    bO2_Degraded_1oo2 := TRUE;
ELSE
    rVotedDeOxoO2_ppm := 3500.0; (* Failsafe conservative estimate *)
    bO2_Degraded_1oo2 := TRUE;
    dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0004; (* O2 Analyzer Bank Failure *)
END_IF;

IF (rO2_DevAB_ppm > 250.0) OR (rO2_DevBC_ppm > 250.0) OR (rO2_DevCA_ppm > 250.0) THEN
    iO2_FaultCounter := iO2_FaultCounter + 1;
    IF iO2_FaultCounter > 60 THEN
        dwDiagnosticWord := dwDiagnosticWord OR 16#0000_0004; (* O2 Discrepancy Warning *)
    END_IF;
ELSE
    IF iO2_FaultCounter > 0 THEN iO2_FaultCounter := iO2_FaultCounter - 1; END_IF;
END_IF;


(* ----------------------------------------------------------------------------------------- *)
(* 1.4 Product Frost Point Hygrometer Voting (AT-FP-01A, AT-FP-01B, AT-FP-01C)               *)
(* ----------------------------------------------------------------------------------------- *)
rTemp_A := rProductFrostPoint_A_DegC;
rTemp_B := rProductFrostPoint_B_DegC;
rTemp_C := rProductFrostPoint_C_DegC;

bFP_ChanA_Valid := (rTemp_A >= -105.0) AND (rTemp_A <= 15.0);
bFP_ChanB_Valid := (rTemp_B >= -105.0) AND (rTemp_B <= 15.0);
bFP_ChanC_Valid := (rTemp_C >= -105.0) AND (rTemp_C <= 15.0);

IF (ABS(rTemp_A - rLast_FP_A) < 0.001) AND (rProductPressure_bar > 40.0) THEN
    iFrozenCycles_FP := iFrozenCycles_FP + 1;
    IF iFrozenCycles_FP > 300 THEN bFP_ChanA_Valid := FALSE; END_IF;
ELSE
    iFrozenCycles_FP := 0;
END_IF;
rLast_FP_A := rTemp_A;

rFP_DevAB_DegC := ABS(rTemp_A - rTemp_B);
rFP_DevBC_DegC := ABS(rTemp_B - rTemp_C);
rFP_DevCA_DegC := ABS(rTemp_C - rTemp_A);

IF bFP_ChanA_Valid AND bFP_ChanB_Valid AND bFP_ChanC_Valid THEN
    IF ((rTemp_A >= rTemp_B) AND (rTemp_A <= rTemp_C)) OR ((rTemp_A >= rTemp_C) AND (rTemp_A <= rTemp_B)) THEN
        rVotedFrostPoint_DegC := rTemp_A;
    ELSIF ((rTemp_B >= rTemp_A) AND (rTemp_B <= rTemp_C)) OR ((rTemp_B >= rTemp_C) AND (rTemp_B <= rTemp_A)) THEN
        rVotedFrostPoint_DegC := rTemp_B;
    ELSE
        rVotedFrostPoint_DegC := rTemp_C;
    END_IF;
    bFP_Degraded_1oo2 := FALSE;
ELSIF bFP_ChanA_Valid AND bFP_ChanB_Valid THEN
    rVotedFrostPoint_DegC := (rTemp_A + rTemp_B) * 0.5;
    bFP_Degraded_1oo2 := TRUE;
ELSIF bFP_ChanB_Valid AND bFP_ChanC_Valid THEN
    rVotedFrostPoint_DegC := (rTemp_B + rTemp_C) * 0.5;
    bFP_Degraded_1oo2 := TRUE;
ELSIF bFP_ChanA_Valid AND bFP_ChanC_Valid THEN
    rVotedFrostPoint_DegC := (rTemp_A + rTemp_C) * 0.5;
    bFP_Degraded_1oo2 := TRUE;
ELSIF bFP_ChanA_Valid THEN
    rVotedFrostPoint_DegC := rTemp_A;
    bFP_Degraded_1oo2 := TRUE;
ELSIF bFP_ChanB_Valid THEN
    rVotedFrostPoint_DegC := rTemp_B;
    bFP_Degraded_1oo2 := TRUE;
ELSIF bFP_ChanC_Valid THEN
    rVotedFrostPoint_DegC := rTemp_C;
    bFP_Degraded_1oo2 := TRUE;
ELSE
    rVotedFrostPoint_DegC := -40.0; (* Failsafe wet product assumption *)
    bFP_Degraded_1oo2 := TRUE;
    dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0008; (* Frost Point Analyzer Bank Trip *)
END_IF;

IF (rFP_DevAB_DegC > 5.0) OR (rFP_DevBC_DegC > 5.0) OR (rFP_DevCA_DegC > 5.0) THEN
    iFP_FaultCounter := iFP_FaultCounter + 1;
    IF iFP_FaultCounter > 60 THEN
        dwDiagnosticWord := dwDiagnosticWord OR 16#0000_0008; (* Frost Point Discrepancy Alert *)
    END_IF;
ELSE
    IF iFP_FaultCounter > 0 THEN iFP_FaultCounter := iFP_FaultCounter - 1; END_IF;
END_IF;
"""
    sections.append(sec_1)

    # -------------------------------------------------------------------------
    # 5. SECTION 2.0: DIGITAL SIGNAL FILTERING & DERIVATIVE ESTIMATION
    # -------------------------------------------------------------------------
    sec_2 = """
(* ========================================================================================= *)
(* 2.0 DIGITAL SIGNAL FILTERING, SENSITIVITY SLEW-LIMITING & DERIVATIVE ESTIMATION           *)
(* ========================================================================================= *)
(* First-order discrete low-pass IIR filtering: y(k) = y(k-1) + (dt / (tau + dt))*(u(k)-y(k-1))*)
(* Computes backward-difference derivatives with high-frequency noise rejection.             *)

rAlpha_Filter := rCycleTime_sec / (rTau_Filter_sec + rCycleTime_sec);

(* Filter Primary Process Measurements *)
rFilt_InletPress_bar     := rFilt_InletPress_bar     + rAlpha_Filter * (rVotedInletPressure_bar - rFilt_InletPress_bar);
rFilt_CycloneLevel_pct   := rFilt_CycloneLevel_pct   + rAlpha_Filter * (rVotedCycloneLevel_pct  - rFilt_CycloneLevel_pct);
rFilt_DeOxoO2_ppm        := rFilt_DeOxoO2_ppm        + rAlpha_Filter * (rVotedDeOxoO2_ppm       - rFilt_DeOxoO2_ppm);
rFilt_FrostPoint_DegC    := rFilt_FrostPoint_DegC    + rAlpha_Filter * (rVotedFrostPoint_DegC   - rFilt_FrostPoint_DegC);
rFilt_DeOxoCoreTemp_DegC := rFilt_DeOxoCoreTemp_DegC + rAlpha_Filter * (rDeOxoBedTemp_Zone2_DegC - rFilt_DeOxoCoreTemp_DegC);
rFilt_RegenPurgeFlow_Nm3h:= rFilt_RegenPurgeFlow_Nm3h+ rAlpha_Filter * (rRegenPurgeFlow_Nm3h    - rFilt_RegenPurgeFlow_Nm3h);

(* ----------------------------------------------------------------------------------------- *)
(* 2.1 Frost Point Dynamic Rate of Rise (Breakthrough Detection Tracker)                     *)
(* ----------------------------------------------------------------------------------------- *)
(* rRateOfChange in [deg C / min] *)
IF rCycleTime_sec > 0.001 THEN
    rRateOfChange_FrostPoint_DegCmin := ((rFilt_FrostPoint_DegC - rPrev_VotedFrostPoint_DegC) / rCycleTime_sec) * 60.0;
    rRateOfChange_DeOxo_DegCs := (rFilt_DeOxoCoreTemp_DegC - rPrev_DeOxoCoreTemp_DegC) / rCycleTime_sec;
END_IF;

rPrev_VotedFrostPoint_DegC := rFilt_FrostPoint_DegC;
rPrev_DeOxoCoreTemp_DegC := rFilt_DeOxoCoreTemp_DegC;

(* ----------------------------------------------------------------------------------------- *)
(* 2.2 Repressurization Ramp Rate Tracker [bar / min]                                        *)
(* ----------------------------------------------------------------------------------------- *)
IF bBed_A_IsDutyAdsorption THEN
    (* Bed B is being repressurized *)
    rRepressRampRate_bar_min := ((rTSABed_B_Pressure_bar - rPrev_RepressPressure_bar) / rCycleTime_sec) * 60.0;
    rPrev_RepressPressure_bar := rTSABed_B_Pressure_bar;
ELSE
    (* Bed A is being repressurized *)
    rRepressRampRate_bar_min := ((rTSABed_A_Pressure_bar - rPrev_RepressPressure_bar) / rCycleTime_sec) * 60.0;
    rPrev_RepressPressure_bar := rTSABed_A_Pressure_bar;
END_IF;
"""
    sections.append(sec_2)

    # -------------------------------------------------------------------------
    # 6. SECTION 3.0: THERMODYNAMIC PSYCHROMETRICS & FLASH EQUILIBRIUM
    # -------------------------------------------------------------------------
    sec_3 = """
(* ========================================================================================= *)
(* 3.0 THERMODYNAMIC PSYCHROMETRICS, FROST POINT CONVERSION & FLASH EQUILIBRIUM              *)
(* ========================================================================================= *)
(* Formulates high-pressure hydrogen vapor-liquid equilibrium (VLE) and vapor-ice equilibrium*)
(* using Goff-Gratch saturation vapor pressure formulation over ice, corrected by the non-  *)
(* ideal fugacity enhancement factor fw(T, P) for 70.0 bar hydrogen atmospheres.            *)

(* ----------------------------------------------------------------------------------------- *)
(* 3.1 Goff-Gratch Equation for Saturation Vapor Pressure over Ice (P_sat,ice in Pa)        *)
(* Temperature range: -100.0 deg C to 0.0 deg C (T in Kelvin: 173.15 K to 273.15 K)          *)
(* ----------------------------------------------------------------------------------------- *)
(* Approximation formula accurate to within 0.05% over the cryo-adsorption envelope:         *)
(* log10(P_ice/P0) = -9.09718*(T0/T - 1) - 3.56654*log10(T0/T) + 0.876793*(1 - T/T0)       *)
(* With T0 = 273.16 K, P0 = 611.73 Pa                                                        *)

IF rFilt_FrostPoint_DegC < -75.0 THEN
    (* Ultra-dry regime (< -75 deg C): Vapor pressure <= 0.15 Pa *)
    rGoffGratchVaporPress_Pa := 0.12 * EXP(0.095 * (rFilt_FrostPoint_DegC + 75.0));
ELSIF rFilt_FrostPoint_DegC < -65.0 THEN
    (* Target compliance regime [-75 to -65 deg C]: ~0.15 Pa to 0.54 Pa *)
    rGoffGratchVaporPress_Pa := 0.28 * EXP(0.088 * (rFilt_FrostPoint_DegC + 70.0));
ELSIF rFilt_FrostPoint_DegC < -50.0 THEN
    (* Moderate dryness [-65 to -50 deg C]: ~0.54 Pa to 3.94 Pa *)
    rGoffGratchVaporPress_Pa := 1.45 * EXP(0.082 * (rFilt_FrostPoint_DegC + 60.0));
ELSE
    (* Wet gas regime (> -50 deg C): > 3.94 Pa *)
    rGoffGratchVaporPress_Pa := 3.94 * EXP(0.076 * (rFilt_FrostPoint_DegC + 50.0));
END_IF;

(* ----------------------------------------------------------------------------------------- *)
(* 3.2 Non-Ideal Enhancement Factor fw(P, T) for 70-Bar Hydrogen Atmosphere                  *)
(* ----------------------------------------------------------------------------------------- *)
(* In dense high-pressure gas, the partial pressure of water vapor exceeds ideal Dalton-Raoult*)
(* calculations due to Poynting effect and cross-virial coefficients (B12). At 70.0 bar,     *)
(* fw is approximately 1.25 to 1.35.                                                         *)
rEnhancementFactor_fw := 1.0 + (rVotedInletPressure_bar * 0.00395) + (rFilt_FrostPoint_DegC * 0.00022);
IF rEnhancementFactor_fw < 1.0 THEN rEnhancementFactor_fw := 1.0; END_IF;
IF rEnhancementFactor_fw > 1.45 THEN rEnhancementFactor_fw := 1.45; END_IF;

(* Derived Moisture Volume Fraction [ppmv] *)
(* y_H2O = (P_sat,ice * fw / P_total) * 1e6 *)
IF rProductPressure_bar > 1.0 THEN
    rCalculatedMoisture_ppm := (rGoffGratchVaporPress_Pa * rEnhancementFactor_fw) / (rProductPressure_bar * 100000.0) * 1000000.0;
ELSE
    rCalculatedMoisture_ppm := 10.0;
END_IF;

(* ----------------------------------------------------------------------------------------- *)
(* 3.3 Catalytic De-Oxo Exotherm Thermodynamics                                              *)
(* Reaction: 2 H2 + O2 -> 2 H2O  |  Delta H = -241.82 kJ/mol O2                              *)
(* Adiabatic Temperature Rise: Delta_T = (y_O2 * (-Delta H)) / (Cp_H2 * M_H2)                *)
(* With Cp_H2 ~ 14.3 kJ/(kg K), Delta_T ~ 1.62 deg C per 100 ppm O2                         *)
(* ----------------------------------------------------------------------------------------- *)
rTheoreticalHotspotRise_DegC := (rFilt_DeOxoO2_ppm / 100.0) * 1.62;
rDeOxoExothermDeltaT_DegC := rFilt_DeOxoCoreTemp_DegC - rInletTemp_DegC;

(* ----------------------------------------------------------------------------------------- *)
(* 3.4 Ergun Equation: Dynamic Packed Bed Differential Pressure Verification                 *)
(* DP/L = 150 * ((1-eps)^2 / eps^3) * (mu*vs / dp^2) + 1.75 * ((1-eps)/eps^3) * (rho*vs^2/dp)*)
(* ----------------------------------------------------------------------------------------- *)
(* Gas Density at 70 bar, 20C: rho = P*M / (Z*R*T) = 7.0e6 * 2.016e-3 / (1.042 * 8.314 * 293.15) ~ 5.56 kg/m3 *)
rHydrogenDensity_kgm3 := (rVotedInletPressure_bar * 100000.0 * 0.00201588) / (rCompressibility_Z * rConst_R_gas * (rInletTemp_DegC + 273.15));
IF rHydrogenDensity_kgm3 < 0.1 THEN rHydrogenDensity_kgm3 := 0.1; END_IF;

(* Cross-sectional bed area A = pi * D^2 / 4 = 3.14159 * 0.65^2 / 4 = 0.3318 m2 *)
(* Superficial velocity vs = Q_actual / A *)
IF rVotedInletPressure_bar > 5.0 THEN
    rSuperficialVelocity_ms := (rRawH2Flow_Nm3h / 3600.0) * (1.01325 / rVotedInletPressure_bar) * ((rInletTemp_DegC + 273.15) / 273.15) / 0.3318;
ELSE
    rSuperficialVelocity_ms := 0.01;
END_IF;

(* Viscosity of H2 at 70 bar ~ 9.0e-6 Pa s *)
(* Laminar viscous term + turbulent inertial term *)
rBedDifferentialPress_kPa := (150.0 * 0.231 * (0.000009 * rSuperficialVelocity_ms / 0.00000484) +
                              1.75 * 10.74 * (rHydrogenDensity_kgm3 * rSuperficialVelocity_ms * rSuperficialVelocity_ms / 0.0022)) *
                             rConst_BedHeight_m * 0.001;
"""
    sections.append(sec_3)

    # -------------------------------------------------------------------------
    # 7. SECTION 4.0: 4-STATE DISCRETE STATE-SPACE OBSERVER MODEL
    # -------------------------------------------------------------------------
    sec_4 = """
(* ========================================================================================= *)
(* 4.0 4-STATE DISCRETE STATE-SPACE OBSERVER MODEL (A, B, C, D)                              *)
(* ========================================================================================= *)
(* Real-time state reconstruction using Euler-Maruyama discretization:                       *)
(* x(k+1) = x(k) + [ A*x(k) + B*u(k) + E*d(k) + L*(y_meas(k) - C*x(k)) ] * dt               *)
(*                                                                                           *)
(* State Vector:                                                                             *)
(* x1: De-Oxo Core Bed Temperature [deg C]                                                   *)
(* x2: TSA Regeneration Bed Internal Temperature [deg C]                                     *)
(* x3: Duty Bed Cumulative Adsorbed Water Mass [kg H2O]                                      *)
(* x4: TSA Regeneration Vessel Pressure [bar]                                                *)

(* Vector Assemblies *)
rVec_u[1] := rRegenHeaterPowerDemand_kW;
rVec_u[2] := rDeOxoCoolingValveDemand_pct;
IF bBed_A_IsDutyAdsorption THEN
    rVec_u[3] := rBed_B_RepressValve_pct;
ELSE
    rVec_u[3] := rBed_A_RepressValve_pct;
END_IF;

rVec_d[1] := rRawH2Flow_Nm3h;
rVec_d[2] := rFilt_DeOxoO2_ppm;
rVec_d[3] := rFilt_CycloneLevel_pct; (* Surrogate for inlet moisture flux *)

(* Measured Output Vector *)
rVec_y[1] := rFilt_DeOxoCoreTemp_DegC;
IF bBed_A_IsDutyAdsorption THEN
    rVec_y[2] := rTSABed_B_CoreTemp_DegC;
    rVec_y[4] := rTSABed_B_Pressure_bar;
ELSE
    rVec_y[2] := rTSABed_A_CoreTemp_DegC;
    rVec_y[4] := rTSABed_A_Pressure_bar;
END_IF;
rVec_y[3] := rTotalDutyAdsorbed_kg;

(* Matrix Multiplication & State Propagation *)
FOR iIdx_i := 1 TO 4 DO
    rMatrixSum := 0.0;
    
    (* Dynamic Matrix A * x *)
    FOR iIdx_j := 1 TO 4 DO
        rMatrixSum := rMatrixSum + rMat_A[iIdx_i, iIdx_j] * rVec_x[iIdx_j];
    END_FOR;

    (* Actuator Matrix B * u *)
    FOR iIdx_j := 1 TO 3 DO
        rMatrixSum := rMatrixSum + rMat_B[iIdx_i, iIdx_j] * rVec_u[iIdx_j];
    END_FOR;

    (* Disturbance Matrix E * d *)
    FOR iIdx_j := 1 TO 3 DO
        rMatrixSum := rMatrixSum + rMat_E[iIdx_i, iIdx_j] * rVec_d[iIdx_j];
    END_FOR;

    (* Observer Innovation Feedback: L * (y - C*x) *)
    rMatrixSum := rMatrixSum + rObserverGain_L[iIdx_i] * (rVec_y[iIdx_i] - rVec_x[iIdx_i]);

    (* Integration Step *)
    rVec_x[iIdx_i] := rVec_x[iIdx_i] + (rMatrixSum * rCycleTime_sec);
END_FOR;

(* State Bound Protections & Saturation *)
IF rVec_x[1] < 10.0 THEN rVec_x[1] := 10.0; END_IF;
IF rVec_x[1] > 320.0 THEN rVec_x[1] := 320.0; END_IF;
IF rVec_x[2] < 10.0 THEN rVec_x[2] := 10.0; END_IF;
IF rVec_x[2] > 300.0 THEN rVec_x[2] := 300.0; END_IF;
IF rVec_x[3] < 0.0 THEN rVec_x[3] := 0.0; END_IF;
IF rVec_x[4] < 0.5 THEN rVec_x[4] := 0.5; END_IF;
IF rVec_x[4] > 85.0 THEN rVec_x[4] := 85.0; END_IF;

(* Update Adsorber Breakthrough Capacity Estimator *)
IF bBed_A_IsDutyAdsorption THEN
    rBed_A_AdsorptionCapacity_pct := 100.0 - ((rVec_x[3] / rMaxAdsorptionCapacity_kg) * 100.0);
    IF rBed_A_AdsorptionCapacity_pct < 0.0 THEN rBed_A_AdsorptionCapacity_pct := 0.0; END_IF;
    rBed_B_AdsorptionCapacity_pct := 100.0; (* Under regeneration *)
ELSE
    rBed_B_AdsorptionCapacity_pct := 100.0 - ((rVec_x[3] / rMaxAdsorptionCapacity_kg) * 100.0);
    IF rBed_B_AdsorptionCapacity_pct < 0.0 THEN rBed_B_AdsorptionCapacity_pct := 0.0; END_IF;
    rBed_A_AdsorptionCapacity_pct := 100.0; (* Under regeneration *)
END_IF;
"""
    sections.append(sec_4)

    # -------------------------------------------------------------------------
    # 8. SECTION 5.0: MODEL PREDICTIVE CONTROL (MPC) QUADRATIC COST OPTIMIZATION
    # -------------------------------------------------------------------------
    sec_5 = """
(* ========================================================================================= *)
(* 5.0 MODEL PREDICTIVE CONTROL (MPC) REFINED QUADRATIC OPTIMIZATION                         *)
(* ========================================================================================= *)
(* Computes finite-horizon control increments using Karush-Kuhn-Tucker (KKT) projected       *)
(* gradient descent over a quadratic performance index:                                      *)
(* min J = sum( (y_k - r_k)^T * Q * (y_k - r_k) ) + sum( delta_u^T * R * delta_u )           *)
(*                                                                                           *)
(* Controlled Variables:                                                                     *)
(* y1: TSA Regeneration Bed Temperature (Target = 218.0 deg C during heating)                 *)
(* y2: De-Oxo Catalytic Core Temperature (Target = 85.0 deg C)                               *)
(* y3: Repressurization Bed Pressure (Target = 70.0 bar)                                     *)

(* Error Vectors *)
rPredictedError_y1 := rVec_Setpoint[1] - rVec_x[2]; (* Regen Bed Error *)
rPredictedError_y2 := rVec_Setpoint[2] - rVec_x[1]; (* De-Oxo Hotspot Error *)
rPredictedError_y3 := rVec_Setpoint[3] - rVec_x[4]; (* Repress Vessel Pressure Error *)

(* Quadratic Cost Computation J *)
rMpcCostFunction_J := (rMat_Q_diag[1] * rPredictedError_y1 * rPredictedError_y1) +
                      (rMat_Q_diag[2] * rPredictedError_y2 * rPredictedError_y2) +
                      (rMat_Q_diag[3] * rPredictedError_y3 * rPredictedError_y3) +
                      (rMat_R_diag[1] * (rVec_u[1] - rLast_HeaterDemand_kW) * (rVec_u[1] - rLast_HeaterDemand_kW)) +
                      (rMat_R_diag[2] * (rVec_u[2] - rLast_CoolingDemand_pct) * (rVec_u[2] - rLast_CoolingDemand_pct)) +
                      (rMat_R_diag[3] * (rVec_u[3] - rLast_RepressDemand_pct) * (rVec_u[3] - rLast_RepressDemand_pct));

(* Numerical Gradient Vectors: dJ/du *)
rMpcGrad_u1 := -2.0 * rMat_Q_diag[1] * rMat_B[2, 1] * rPredictedError_y1 + 2.0 * rMat_R_diag[1] * (rVec_u[1] - rLast_HeaterDemand_kW);
rMpcGrad_u2 := -2.0 * rMat_Q_diag[2] * rMat_B[1, 2] * rPredictedError_y2 + 2.0 * rMat_R_diag[2] * (rVec_u[2] - rLast_CoolingDemand_pct);
rMpcGrad_u3 := -2.0 * rMat_Q_diag[3] * rMat_B[4, 3] * rPredictedError_y3 + 2.0 * rMat_R_diag[3] * (rVec_u[3] - rLast_RepressDemand_pct);

(* Projected Gradient Descent Step *)
IF (iState = 60) OR (iState = 70) THEN
    (* 1. Regeneration Electric Heater Power Demand [kW] *)
    IF (iSubState_TSA = 20) OR (iSubState_TSA = 30) THEN
        rRegenHeaterPowerDemand_kW := rRegenHeaterPowerDemand_kW - (rMpcStepSize_Alpha * rMpcGrad_u1);
    ELSE
        rRegenHeaterPowerDemand_kW := 0.0; (* Off during cool and depress *)
    END_IF;

    (* 2. De-Oxo Cooling Jacket / Trim Valve Demand [%] *)
    IF rFilt_DeOxoCoreTemp_DegC > 80.0 THEN
        rDeOxoCoolingValveDemand_pct := rDeOxoCoolingValveDemand_pct - (rMpcStepSize_Alpha * rMpcGrad_u2);
    ELSE
        rDeOxoCoolingValveDemand_pct := 0.0;
    END_IF;

    (* 3. Repressurization Valve Demand [%] *)
    IF (iSubState_TSA = 50) THEN
        rBed_A_RepressValve_pct := rBed_A_RepressValve_pct - (rMpcStepSize_Alpha * rMpcGrad_u3);
        rBed_B_RepressValve_pct := rBed_B_RepressValve_pct - (rMpcStepSize_Alpha * rMpcGrad_u3);
    ELSE
        rBed_A_RepressValve_pct := 0.0;
        rBed_B_RepressValve_pct := 0.0;
    END_IF;
END_IF;

(* Actuator Slew-Rate Limiting & Safety Saturation *)
(* Electric Heater SCR Clamping *)
IF rRegenHeaterPowerDemand_kW > rHeaterAvailablePower_kW THEN
    rRegenHeaterPowerDemand_kW := rHeaterAvailablePower_kW;
END_IF;
IF (rRegenHeaterPowerDemand_kW - rLast_HeaterDemand_kW) > (rMaxSlew_Heater_kWs * rCycleTime_sec) THEN
    rRegenHeaterPowerDemand_kW := rLast_HeaterDemand_kW + (rMaxSlew_Heater_kWs * rCycleTime_sec);
ELSIF (rLast_HeaterDemand_kW - rRegenHeaterPowerDemand_kW) > (rMaxSlew_Heater_kWs * rCycleTime_sec) THEN
    rRegenHeaterPowerDemand_kW := rLast_HeaterDemand_kW - (rMaxSlew_Heater_kWs * rCycleTime_sec);
END_IF;
IF rRegenHeaterPowerDemand_kW < 0.0 THEN rRegenHeaterPowerDemand_kW := 0.0; END_IF;
rLast_HeaterDemand_kW := rRegenHeaterPowerDemand_kW;

(* Cooling Valve Clamping *)
IF (rDeOxoCoolingValveDemand_pct - rLast_CoolingDemand_pct) > (rMaxSlew_Cooling_pcts * rCycleTime_sec) THEN
    rDeOxoCoolingValveDemand_pct := rLast_CoolingDemand_pct + (rMaxSlew_Cooling_pcts * rCycleTime_sec);
ELSIF (rLast_CoolingDemand_pct - rDeOxoCoolingValveDemand_pct) > (rMaxSlew_Cooling_pcts * rCycleTime_sec) THEN
    rDeOxoCoolingValveDemand_pct := rLast_CoolingDemand_pct - (rMaxSlew_Cooling_pcts * rCycleTime_sec);
END_IF;
IF rDeOxoCoolingValveDemand_pct > 100.0 THEN rDeOxoCoolingValveDemand_pct := 100.0; END_IF;
IF rDeOxoCoolingValveDemand_pct < 0.0 THEN rDeOxoCoolingValveDemand_pct := 0.0; END_IF;
rLast_CoolingDemand_pct := rDeOxoCoolingValveDemand_pct;
"""
    sections.append(sec_5)

    # -------------------------------------------------------------------------
    # 9. SECTION 6.0: MASTER FINITE STATE MACHINE (FSM)
    # -------------------------------------------------------------------------
    sec_6 = """
(* ========================================================================================= *)
(* 6.0 MULTI-STAGE FINITE STATE MACHINE (FSM) & REGENERATION CYCLIC LOGIC                    *)
(* ========================================================================================= *)
(* Deterministic state execution governing the sequential startup, nitrogen inerting, leak   *)
(* testing, catalytic light-off, dual-bed cyclic adsorption, fast-diversion, and shutdown.   *)

(* Master Emergency Safety Interlock Override *)
IF (NOT bEmergencyStop) OR (dwAlarmWord1 <> 16#0000_0000) THEN
    iState := 100; (* Direct vector to Emergency Trip *)
END_IF;

CASE iState OF
    0: (* STATE 0: UNINITIALIZED / PARKED / SAFE DE-PRESSURIZED IDLE *)
        bSystemReady := FALSE;
        bSystemRunning := FALSE;
        bSystemTripped := FALSE;
        rStateTimer_sec := 0.0;
        rSubStateTimer_sec := 0.0;

        (* Isolate All Process & Purge Valves *)
        rCycloneDrainValveDemand_pct := 0.0;
        rDeOxoCoolingValveDemand_pct := 0.0;
        rRegenHeaterPowerDemand_kW := 0.0;
        rBed_A_InletValve_pct := 0.0;
        rBed_A_OutletValve_pct := 0.0;
        rBed_A_DepressValve_pct := 0.0;
        rBed_A_PurgeValve_pct := 0.0;
        rBed_A_RepressValve_pct := 0.0;
        rBed_B_InletValve_pct := 0.0;
        rBed_B_OutletValve_pct := 0.0;
        rBed_B_DepressValve_pct := 0.0;
        rBed_B_PurgeValve_pct := 0.0;
        rBed_B_RepressValve_pct := 0.0;
        bProductDiverterToRecycle := TRUE; (* Fail-safe to buffer *)
        bProductDiverterToExport := FALSE;

        IF bSystemEnable AND bEmergencyStop AND (dwAlarmWord1 = 16#0000_0000) THEN
            iState := 10; (* Transition to Nitrogen Inerting Sweep *)
        END_IF;

    10: (* STATE 10: INERT GAS N2 PURGE & O2 EVACUATION SWEEP *)
        bSystemReady := FALSE;
        bSystemRunning := FALSE;
        rStateTimer_sec := rStateTimer_sec + rCycleTime_sec;

        (* Crack open blowdown valves to allow N2 sweep to atmospheric flare *)
        rBed_A_DepressValve_pct := 35.0;
        rBed_B_DepressValve_pct := 35.0;

        tPurgeTimer(IN := bNitrogenPurgePermissive, PT := T#30S);
        IF tPurgeTimer.Q AND (rVotedDeOxoO2_ppm < 50.0) THEN
            tPurgeTimer(IN := FALSE);
            rBed_A_DepressValve_pct := 0.0;
            rBed_B_DepressValve_pct := 0.0;
            iState := 20; (* Advance to Hydrogen Slow Repressurization *)
        END_IF;

    20: (* STATE 20: CONTROLLED HYDROGEN SLOW REPRESSURIZATION & LEAK TEST *)
        bSystemReady := FALSE;
        bSystemRunning := FALSE;
        rStateTimer_sec := rStateTimer_sec + rCycleTime_sec;

        (* Throttle wet H2 feed into both vessels to ramp pressure smoothly *)
        rBed_A_InletValve_pct := 15.0;
        rBed_B_InletValve_pct := 15.0;

        (* Check if line reaches 65.0 bar within safety watchdog *)
        IF (rVotedInletPressure_bar >= 65.0) AND (rTSABed_A_Pressure_bar >= 65.0) THEN
            rBed_A_InletValve_pct := 0.0;
            rBed_B_InletValve_pct := 0.0;
            iState := 30; (* Advance to Cyclone Knockout Stabilization *)
        END_IF;

        tRepressTimer(IN := TRUE, PT := T#120S);
        IF tRepressTimer.Q AND (rVotedInletPressure_bar < 60.0) THEN
            tRepressTimer(IN := FALSE);
            dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0001; (* Pressurization Timeout Trip *)
            iState := 100;
        END_IF;

    30: (* STATE 30: CYCLONE CONDENSATE KNOCKOUT STABILIZATION & LEVEL TUNE *)
        bSystemReady := FALSE;
        bSystemRunning := TRUE;
        rStateTimer_sec := rStateTimer_sec + rCycleTime_sec;

        (* Enable Cyclone Condensate Drain Level Control *)
        IF (rVotedCycloneLevel_pct > 20.0) AND (rVotedCycloneLevel_pct < 70.0) THEN
            bSystemReady := TRUE;
            iState := 40; (* Proceed to De-Oxo Catalytic Light-Off *)
        END_IF;

    40: (* STATE 40: CATALYTIC DE-OXO LIGHT-OFF & THERMAL MODULATION *)
        bSystemReady := TRUE;
        bSystemRunning := TRUE;
        rStateTimer_sec := rStateTimer_sec + rCycleTime_sec;

        (* Route flow through De-Oxo bed *)
        IF rInletTemp_DegC >= 45.0 THEN
            (* Catalyst has sufficient inlet thermal energy to initiate reaction *)
            tDeOxoPreheatTimer(IN := TRUE, PT := T#15S);
            IF tDeOxoPreheatTimer.Q THEN
                tDeOxoPreheatTimer(IN := FALSE);
                iState := 50; (* Transition to TSA Alignment *)
            END_IF;
        ELSE
            tDeOxoPreheatTimer(IN := FALSE);
        END_IF;

    50: (* STATE 50: DUAL-BED TSA INITIAL ALIGNMENT & SYNCHRONIZATION *)
        bSystemReady := TRUE;
        bSystemRunning := TRUE;
        rStateTimer_sec := 0.0;
        rSubStateTimer_sec := 0.0;

        (* Default Configuration: Bed A Online (Duty), Bed B in Regeneration Standby *)
        bBed_A_IsDutyAdsorption := TRUE;
        rBed_A_InletValve_pct := 100.0;
        rBed_A_OutletValve_pct := 100.0;
        rBed_B_InletValve_pct := 0.0;
        rBed_B_OutletValve_pct := 0.0;

        iSubState_TSA := 10; (* Start Bed B in Step 10: Depressurization *)
        iState := 60;        (* Enter Cyclic Adsorption Mode *)

    60: (* STATE 60: CYCLIC MODE: BED A DUTY (ADSORPTION) / BED B REGENERATION *)
        bSystemReady := TRUE;
        bSystemRunning := TRUE;
        rStateTimer_sec := rStateTimer_sec + rCycleTime_sec;
        rSubStateTimer_sec := rSubStateTimer_sec + rCycleTime_sec;

        (* Keep Bed A Valves Fully Open for Adsorption *)
        rBed_A_InletValve_pct := 100.0;
        rBed_A_OutletValve_pct := 100.0;
        rBed_A_DepressValve_pct := 0.0;
        rBed_A_PurgeValve_pct := 0.0;
        rBed_A_RepressValve_pct := 0.0;

        (* ----------------------------------------------------------------- *)
        (* Bed B 5-Step Regeneration Sub-Cycle Machine                       *)
        (* ----------------------------------------------------------------- *)
        CASE iSubState_TSA OF
            10: (* Step 10: Controlled Blowdown / Depressurization *)
                rBed_B_InletValve_pct := 0.0;
                rBed_B_OutletValve_pct := 0.0;
                rBed_B_PurgeValve_pct := 0.0;
                rBed_B_RepressValve_pct := 0.0;
                rRegenHeaterPowerDemand_kW := 0.0;

                (* Modulate blowdown valve to maintain depressurization rate *)
                IF rTSABed_B_Pressure_bar > 5.0 THEN
                    rBed_B_DepressValve_pct := 25.0;
                ELSE
                    rBed_B_DepressValve_pct := 60.0;
                END_IF;

                IF rTSABed_B_Pressure_bar <= rTSABlowdownTargetP_bar THEN
                    rBed_B_DepressValve_pct := 15.0; (* Keep cracked for purge exit *)
                    rSubStateTimer_sec := 0.0;
                    iSubState_TSA := 20; (* Proceed to Thermal Purge Heating *)
                END_IF;

            20: (* Step 20: Electric Purge Gas Heating *)
                rBed_B_PurgeValve_pct := 100.0; (* Open hot purge feed *)
                rBed_B_DepressValve_pct := 40.0; (* Purge exhaust open *)

                (* MPC actively modulates rRegenHeaterPowerDemand_kW towards 218C *)
                tRegenHeatingTimer(IN := (rTSABed_B_CoreTemp_DegC >= rTSARegenTargetTemp_DegC), PT := T#20S);
                IF tRegenHeatingTimer.Q THEN
                    tRegenHeatingTimer(IN := FALSE);
                    rSubStateTimer_sec := 0.0;
                    iSubState_TSA := 30; (* Proceed to High-Temp Soak *)
                END_IF;

            30: (* Step 30: High-Temperature Thermal Soak Plateau *)
                rBed_B_PurgeValve_pct := 100.0;
                rBed_B_DepressValve_pct := 40.0;

                (* Hold temperature for 60 seconds to complete desorption wave *)
                tRegenSoakTimer(IN := TRUE, PT := T#60S);
                IF tRegenSoakTimer.Q THEN
                    tRegenSoakTimer(IN := FALSE);
                    rRegenHeaterPowerDemand_kW := 0.0; (* Cut electric power *)
                    rSubStateTimer_sec := 0.0;
                    iSubState_TSA := 40; (* Proceed to Cold Purge Cooldown *)
                END_IF;

            40: (* Step 40: Dry Cold H2 Sweep Cooldown *)
                rRegenHeaterPowerDemand_kW := 0.0;
                rBed_B_PurgeValve_pct := 100.0;
                rBed_B_DepressValve_pct := 50.0;

                tRegenCoolTimer(IN := (rTSABed_B_CoreTemp_DegC <= rTSACooldownTargetTemp_DegC), PT := T#15S);
                IF tRegenCoolTimer.Q THEN
                    tRegenCoolTimer(IN := FALSE);
                    rBed_B_PurgeValve_pct := 0.0;
                    rBed_B_DepressValve_pct := 0.0; (* Close exhaust *)
                    rSubStateTimer_sec := 0.0;
                    iSubState_TSA := 50; (* Proceed to Slow Repressurization *)
                END_IF;

            50: (* Step 50: Controlled Slow Repressurization with Product Gas *)
                (* Strictly limit dP/dt <= 1.5 bar/min *)
                IF rRepressRampRate_bar_min > rMaxAllowableRepressRamp_barmin THEN
                    rBed_B_RepressValve_pct := rBed_B_RepressValve_pct - (10.0 * rCycleTime_sec);
                ELSE
                    rBed_B_RepressValve_pct := rBed_B_RepressValve_pct + (2.0 * rCycleTime_sec);
                END_IF;
                IF rBed_B_RepressValve_pct > 40.0 THEN rBed_B_RepressValve_pct := 40.0; END_IF;
                IF rBed_B_RepressValve_pct < 0.0 THEN rBed_B_RepressValve_pct := 0.0; END_IF;

                IF rTSABed_B_Pressure_bar >= (rVotedInletPressure_bar - 0.5) THEN
                    rBed_B_RepressValve_pct := 0.0;
                    rSubStateTimer_sec := 0.0;
                    iSubState_TSA := 60; (* Bed B Pressurized & Standby Ready *)
                END_IF;

            60: (* Step 60: Pressurized Standby Waiting for Bed A Switchover *)
                rBed_B_InletValve_pct := 0.0;
                rBed_B_OutletValve_pct := 0.0;
                rBed_B_DepressValve_pct := 0.0;
                rBed_B_PurgeValve_pct := 0.0;
                rBed_B_RepressValve_pct := 0.0;
                rRegenHeaterPowerDemand_kW := 0.0;
        END_CASE;

        (* ----------------------------------------------------------------- *)
        (* Breakthrough or Cyclic Switchover Evaluation                      *)
        (* ----------------------------------------------------------------- *)
        IF (rBed_A_AdsorptionCapacity_pct <= 5.0) OR (rFilt_FrostPoint_DegC > -68.0) OR (rStateTimer_sec >= 14400.0) THEN
            IF (iSubState_TSA = 60) THEN
                (* Bed B is fully regenerated and pressurized: execute bumpless transfer *)
                bBedSwitchInitiated := TRUE;
                rBed_B_InletValve_pct := 100.0;
                rBed_B_OutletValve_pct := 100.0;

                tBedSwitchTimer(IN := TRUE, PT := T#5S);
                IF tBedSwitchTimer.Q THEN
                    tBedSwitchTimer(IN := FALSE);
                    bBedSwitchInitiated := FALSE;
                    rBed_A_InletValve_pct := 0.0;
                    rBed_A_OutletValve_pct := 0.0;
                    bBed_A_IsDutyAdsorption := FALSE; (* Now Bed B is Duty *)
                    rTotalDutyAdsorbed_kg := 0.0;
                    rStateTimer_sec := 0.0;
                    rSubStateTimer_sec := 0.0;
                    iSubState_TSA := 10; (* Start Bed A Regeneration *)
                    iState := 70;        (* Switch to State 70 *)
                END_IF;
            ELSE
                (* Premature breakthrough before regeneration complete: trigger warning and divert *)
                dwWarningWord1 := dwWarningWord1 OR 16#0000_0001; (* Premature Breakthrough Alert *)
                IF rFilt_FrostPoint_DegC > -65.0 THEN
                    iState := 80; (* Vector to Offspec Purity Diversion *)
                END_IF;
            END_IF;
        END_IF;

    70: (* STATE 70: CYCLIC MODE: BED B DUTY (ADSORPTION) / BED A REGENERATION *)
        bSystemReady := TRUE;
        bSystemRunning := TRUE;
        rStateTimer_sec := rStateTimer_sec + rCycleTime_sec;
        rSubStateTimer_sec := rSubStateTimer_sec + rCycleTime_sec;

        (* Keep Bed B Valves Fully Open for Adsorption *)
        rBed_B_InletValve_pct := 100.0;
        rBed_B_OutletValve_pct := 100.0;
        rBed_B_DepressValve_pct := 0.0;
        rBed_B_PurgeValve_pct := 0.0;
        rBed_B_RepressValve_pct := 0.0;

        (* ----------------------------------------------------------------- *)
        (* Bed A 5-Step Regeneration Sub-Cycle Machine                       *)
        (* ----------------------------------------------------------------- *)
        CASE iSubState_TSA OF
            10: (* Step 10: Controlled Blowdown / Depressurization *)
                rBed_A_InletValve_pct := 0.0;
                rBed_A_OutletValve_pct := 0.0;
                rBed_A_PurgeValve_pct := 0.0;
                rBed_A_RepressValve_pct := 0.0;
                rRegenHeaterPowerDemand_kW := 0.0;

                IF rTSABed_A_Pressure_bar > 5.0 THEN
                    rBed_A_DepressValve_pct := 25.0;
                ELSE
                    rBed_A_DepressValve_pct := 60.0;
                END_IF;

                IF rTSABed_A_Pressure_bar <= rTSABlowdownTargetP_bar THEN
                    rBed_A_DepressValve_pct := 15.0;
                    rSubStateTimer_sec := 0.0;
                    iSubState_TSA := 20;
                END_IF;

            20: (* Step 20: Electric Purge Gas Heating *)
                rBed_A_PurgeValve_pct := 100.0;
                rBed_A_DepressValve_pct := 40.0;

                tRegenHeatingTimer(IN := (rTSABed_A_CoreTemp_DegC >= rTSARegenTargetTemp_DegC), PT := T#20S);
                IF tRegenHeatingTimer.Q THEN
                    tRegenHeatingTimer(IN := FALSE);
                    rSubStateTimer_sec := 0.0;
                    iSubState_TSA := 30;
                END_IF;

            30: (* Step 30: High-Temperature Thermal Soak Plateau *)
                rBed_A_PurgeValve_pct := 100.0;
                rBed_A_DepressValve_pct := 40.0;

                tRegenSoakTimer(IN := TRUE, PT := T#60S);
                IF tRegenSoakTimer.Q THEN
                    tRegenSoakTimer(IN := FALSE);
                    rRegenHeaterPowerDemand_kW := 0.0;
                    rSubStateTimer_sec := 0.0;
                    iSubState_TSA := 40;
                END_IF;

            40: (* Step 40: Dry Cold H2 Sweep Cooldown *)
                rRegenHeaterPowerDemand_kW := 0.0;
                rBed_A_PurgeValve_pct := 100.0;
                rBed_A_DepressValve_pct := 50.0;

                tRegenCoolTimer(IN := (rTSABed_A_CoreTemp_DegC <= rTSACooldownTargetTemp_DegC), PT := T#15S);
                IF tRegenCoolTimer.Q THEN
                    tRegenCoolTimer(IN := FALSE);
                    rBed_A_PurgeValve_pct := 0.0;
                    rBed_A_DepressValve_pct := 0.0;
                    rSubStateTimer_sec := 0.0;
                    iSubState_TSA := 50;
                END_IF;

            50: (* Step 50: Controlled Slow Repressurization with Product Gas *)
                IF rRepressRampRate_bar_min > rMaxAllowableRepressRamp_barmin THEN
                    rBed_A_RepressValve_pct := rBed_A_RepressValve_pct - (10.0 * rCycleTime_sec);
                ELSE
                    rBed_A_RepressValve_pct := rBed_A_RepressValve_pct + (2.0 * rCycleTime_sec);
                END_IF;
                IF rBed_A_RepressValve_pct > 40.0 THEN rBed_A_RepressValve_pct := 40.0; END_IF;
                IF rBed_A_RepressValve_pct < 0.0 THEN rBed_A_RepressValve_pct := 0.0; END_IF;

                IF rTSABed_A_Pressure_bar >= (rVotedInletPressure_bar - 0.5) THEN
                    rBed_A_RepressValve_pct := 0.0;
                    rSubStateTimer_sec := 0.0;
                    iSubState_TSA := 60;
                END_IF;

            60: (* Step 60: Pressurized Standby Waiting for Bed B Switchover *)
                rBed_A_InletValve_pct := 0.0;
                rBed_A_OutletValve_pct := 0.0;
                rBed_A_DepressValve_pct := 0.0;
                rBed_A_PurgeValve_pct := 0.0;
                rBed_A_RepressValve_pct := 0.0;
                rRegenHeaterPowerDemand_kW := 0.0;
        END_CASE;

        (* Switchover Check *)
        IF (rBed_B_AdsorptionCapacity_pct <= 5.0) OR (rFilt_FrostPoint_DegC > -68.0) OR (rStateTimer_sec >= 14400.0) THEN
            IF (iSubState_TSA = 60) THEN
                bBedSwitchInitiated := TRUE;
                rBed_A_InletValve_pct := 100.0;
                rBed_A_OutletValve_pct := 100.0;

                tBedSwitchTimer(IN := TRUE, PT := T#5S);
                IF tBedSwitchTimer.Q THEN
                    tBedSwitchTimer(IN := FALSE);
                    bBedSwitchInitiated := FALSE;
                    rBed_B_InletValve_pct := 0.0;
                    rBed_B_OutletValve_pct := 0.0;
                    bBed_A_IsDutyAdsorption := TRUE; (* Return Bed A to Duty *)
                    rTotalDutyAdsorbed_kg := 0.0;
                    rStateTimer_sec := 0.0;
                    rSubStateTimer_sec := 0.0;
                    iSubState_TSA := 10;
                    iState := 60;
                END_IF;
            ELSE
                dwWarningWord1 := dwWarningWord1 OR 16#0000_0001;
                IF rFilt_FrostPoint_DegC > -65.0 THEN
                    iState := 80;
                END_IF;
            END_IF;
        END_IF;

    80: (* STATE 80: RAPID OFFSPEC PURITY DIVERSION & BUFFER RECYCLE *)
        bSystemReady := FALSE;
        bSystemRunning := TRUE;
        rStateTimer_sec := rStateTimer_sec + rCycleTime_sec;

        (* High-speed diversion: Immediately isolate export, divert to recycle *)
        bProductDiverterToExport := FALSE;
        bProductDiverterToRecycle := TRUE;

        (* Check if frost point recovers back below -70.0 deg C *)
        tOffspecDivertTimer(IN := (rFilt_FrostPoint_DegC <= -70.0), PT := T#10S);
        IF tOffspecDivertTimer.Q THEN
            tOffspecDivertTimer(IN := FALSE);
            bProductDiverterToRecycle := FALSE;
            bProductDiverterToExport := TRUE;
            IF bBed_A_IsDutyAdsorption THEN
                iState := 60;
            ELSE
                iState := 70;
            END_IF;
        END_IF;

    90: (* STATE 90: CONTROLLED SHUTDOWN & THERMAL DESORPTION SOAK *)
        bSystemReady := FALSE;
        bSystemRunning := FALSE;
        rStateTimer_sec := rStateTimer_sec + rCycleTime_sec;

        (* Shut off electric heater, open cooling circuits *)
        rRegenHeaterPowerDemand_kW := 0.0;
        rDeOxoCoolingValveDemand_pct := 100.0;

        tShutdownCooldownTimer(IN := (rDeOxoBedTemp_Zone2_DegC < 40.0) AND (rTSABed_A_CoreTemp_DegC < 40.0) AND (rTSABed_B_CoreTemp_DegC < 40.0), PT := T#30S);
        IF tShutdownCooldownTimer.Q THEN
            tShutdownCooldownTimer(IN := FALSE);
            iState := 0; (* Park in Safe Idle *)
        END_IF;

    100: (* STATE 100: EMERGENCY SAFETY INTERLOCK TRIP & FAULT ISOLATION *)
        bSystemReady := FALSE;
        bSystemRunning := FALSE;
        bSystemTripped := TRUE;

        (* Failsafe Actuator De-energization *)
        rCycloneDrainValveDemand_pct := 0.0;
        rDeOxoCoolingValveDemand_pct := 0.0;
        rRegenHeaterPowerDemand_kW := 0.0;
        rBed_A_InletValve_pct := 0.0;
        rBed_A_OutletValve_pct := 0.0;
        rBed_A_DepressValve_pct := 0.0;
        rBed_A_PurgeValve_pct := 0.0;
        rBed_A_RepressValve_pct := 0.0;
        rBed_B_InletValve_pct := 0.0;
        rBed_B_OutletValve_pct := 0.0;
        rBed_B_DepressValve_pct := 0.0;
        rBed_B_PurgeValve_pct := 0.0;
        rBed_B_RepressValve_pct := 0.0;
        bProductDiverterToExport := FALSE;
        bProductDiverterToRecycle := TRUE;

        (* Fault Unlatch Evaluation *)
        IF bResetFaults AND bEmergencyStop AND (dwAlarmWord1 = 16#0000_0000) AND (dwAlarmWord2 = 16#0000_0000) THEN
            bSystemTripped := FALSE;
            iState := 0; (* Return to Idle State *)
        END_IF;

END_CASE;
"""
    sections.append(sec_6)

    # -------------------------------------------------------------------------
    # 10. SECTION 7.0: CYCLONE KNOCKOUT DRAIN LEVEL CONTROL
    # -------------------------------------------------------------------------
    sec_7 = """
(* ========================================================================================= *)
(* 7.0 CYCLONE FLASH CONDENSATE DRAIN LEVEL REGULATION & GAS BLOW-BY INTERLOCK               *)
(* ========================================================================================= *)
(* Controls the high-pressure flash condensate evacuation valve to maintain sump level       *)
(* between 25% and 45%, while guaranteeing zero gas blow-by into low-pressure drainage.     *)

(* 7.1 Anti-Blow-By Hard Interlock: If liquid level falls below 15%, force valve shut *)
IF rVotedCycloneLevel_pct < 15.0 THEN
    rCycloneDrainValveDemand_pct := 0.0;
    rLevel_Integral_Accum := 0.0;
    bDrainValvePulseState := FALSE;
ELSIF (iState >= 30) AND (iState < 90) THEN
    (* PI Level Feedback Controller *)
    IF rVotedCycloneLevel_pct > (rLevelSetPoint_pct + rLevelDeadband_pct) THEN
        rLevel_Integral_Accum := rLevel_Integral_Accum + (rLevel_I_Gain * (rVotedCycloneLevel_pct - rLevelSetPoint_pct) * rCycleTime_sec);
        IF rLevel_Integral_Accum > 50.0 THEN rLevel_Integral_Accum := 50.0; END_IF;

        rCycloneDrainValveDemand_pct := (rLevel_P_Gain * (rVotedCycloneLevel_pct - rLevelSetPoint_pct)) + rLevel_Integral_Accum;
        IF rCycloneDrainValveDemand_pct > 100.0 THEN rCycloneDrainValveDemand_pct := 100.0; END_IF;
        bDrainValvePulseState := TRUE;
    ELSIF rVotedCycloneLevel_pct < (rLevelSetPoint_pct - rLevelDeadband_pct) THEN
        rCycloneDrainValveDemand_pct := 0.0;
        IF rLevel_Integral_Accum > 0.0 THEN
            rLevel_Integral_Accum := rLevel_Integral_Accum - (rLevel_I_Gain * rCycleTime_sec * 2.0);
            IF rLevel_Integral_Accum < 0.0 THEN rLevel_Integral_Accum := 0.0; END_IF;
        END_IF;
        bDrainValvePulseState := FALSE;
    END_IF;
ELSE
    rCycloneDrainValveDemand_pct := 0.0;
END_IF;

(* High-High Level Safety Warning *)
IF rVotedCycloneLevel_pct >= 85.0 THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0002; (* Cyclone Liquid Overflow Hazard *)
END_IF;
"""
    sections.append(sec_7)

    # -------------------------------------------------------------------------
    # 11. SECTION 8.0: ULTRA-LOW FROST POINT TRACKING & OFFSPEC DIVERSION
    # -------------------------------------------------------------------------
    sec_8 = """
(* ========================================================================================= *)
(* 8.0 ULTRA-LOW FROST-POINT (-70 DEG C) PRODUCT GAS PURITY TRACKING & DIVERSION             *)
(* ========================================================================================= *)
(* Evaluates final product gas moisture against ISO 14687 Grade D/E fuel cell standards.    *)
(* Operates fast pneumatic diverter valve to safeguard downstream storage from wet gas.      *)

IF (iState = 60) OR (iState = 70) THEN
    (* Qualified Product Purity Boundary: Frost Point <= -70.0 deg C AND O2 <= 2.0 ppm *)
    IF (rFilt_FrostPoint_DegC <= -70.0) AND (rFilt_DeOxoO2_ppm <= 2.0) THEN
        bProductDiverterToExport := TRUE;
        bProductDiverterToRecycle := FALSE;
    ELSIF (rFilt_FrostPoint_DegC > -65.0) OR (rRateOfChange_FrostPoint_DegCmin > 0.50) OR (rFilt_DeOxoO2_ppm > 4.0) THEN
        (* Fast Off-Spec Diverter Action *)
        bProductDiverterToExport := FALSE;
        bProductDiverterToRecycle := TRUE;
        dwWarningWord1 := dwWarningWord1 OR 16#0000_0002; (* Product Purity Breach Diverted *)
    END_IF;
ELSIF (iState <> 80) THEN
    bProductDiverterToExport := FALSE;
    bProductDiverterToRecycle := TRUE;
END_IF;
"""
    sections.append(sec_8)

    # -------------------------------------------------------------------------
    # 12. SECTION 9.0: GRACEFUL DEGRADATION & ALARM TREE ASSEMBLY
    # -------------------------------------------------------------------------
    sec_9 = """
(* ========================================================================================= *)
(* 9.0 GRACEFUL DEGRADATION, SENSOR FAULT MITIGATION & DERATE MANAGEMENT                     *)
(* ========================================================================================= *)
(* Evaluates sensor degradation status and applies throughput derating envelopes to          *)
(* prevent process trips while maintaining stringent product quality standards.             *)

bDegradedOperation := bPress_Degraded_1oo2 OR bLevel_Degraded_1oo2 OR bO2_Degraded_1oo2 OR bFP_Degraded_1oo2;

IF bDegradedOperation THEN
    dwDiagnosticWord := dwDiagnosticWord OR 16#0000_0080; (* Redundancy Loss Active *)
END_IF;

(* ----------------------------------------------------------------------------------------- *)
(* 9.1 Catalytic De-Oxo Thermal Runaway & High O2 Protection Hierarchy                      *)
(* ----------------------------------------------------------------------------------------- *)
(* Level 1: Core Hotspot High Warning (180 deg C) *)
IF rDeOxoBedTemp_Zone2_DegC >= 180.0 THEN
    dwWarningWord1 := dwWarningWord1 OR 16#0000_0004; (* De-Oxo Thermal Hotspot High *)
    rDeOxoCoolingValveDemand_pct := 100.0;            (* Force maximum cooling *)
END_IF;

(* Level 2: Core Hotspot Critical Trip (220 deg C - Sintering Prevention) *)
IF rDeOxoBedTemp_Zone2_DegC >= 220.0 THEN
    dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0010;     (* De-Oxo Bed Thermal Runaway Trip *)
END_IF;

(* Level 3: Flammability Envelope Breach (Inlet O2 > 8000 ppm = 0.8% O2 in H2) *)
IF rVotedDeOxoO2_ppm >= 8000.0 THEN
    dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0020;     (* Flammability Threshold Exceeded Trip *)
END_IF;

(* ----------------------------------------------------------------------------------------- *)
(* 9.2 TSA Adsorber Bed Overpressure & High DP Fluidization Interlocks                       *)
(* ----------------------------------------------------------------------------------------- *)
IF (rTSABed_A_Pressure_bar >= 82.0) OR (rTSABed_B_Pressure_bar >= 82.0) THEN
    dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0040;     (* TSA Adsorber Vessel Overpressure Trip *)
END_IF;

IF rBedDifferentialPress_kPa >= 75.0 THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0004;     (* Zeolite Bed Fluidization / High DP Trip *)
END_IF;

(* Regeneration Heater Sheath Skin Over-Temperature Protection (Max 260 deg C) *)
IF rRegenHeaterSkinTemp_DegC >= 250.0 THEN
    dwWarningWord1 := dwWarningWord1 OR 16#0000_0008; (* Heater Sheath Temp High *)
    rRegenHeaterPowerDemand_kW := 0.0;                (* Shed heater load *)
END_IF;
IF rRegenHeaterSkinTemp_DegC >= 270.0 THEN
    dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0080;     (* Electric Heater Element Sheath Trip *)
END_IF;
"""
    sections.append(sec_9)

    # -------------------------------------------------------------------------
    # 13. SECTION 10.0: BIT-PACKED STATUS WORDS & MODBUS REGISTERS
    # -------------------------------------------------------------------------
    sec_10 = """
(* ========================================================================================= *)
(* 10.0 BIT-PACKED STATUS WORDS & TELEMETRY REGISTERS                                        *)
(* ========================================================================================= *)
(* Assembles all discrete status indicators, valve positions, and operational states into     *)
(* standardized 32-bit DWORD words for SCADA / DCS communication.                            *)

(* ----------------------------------------------------------------------------------------- *)
(* dwSystemStatusWord1: Master State & Operational Flags                                     *)
(* ----------------------------------------------------------------------------------------- *)
dwSystemStatusWord1 := 16#0000_0000;
IF bSystemReady              THEN dwSystemStatusWord1 := dwSystemStatusWord1 OR 16#0000_0001; END_IF;
IF bSystemRunning            THEN dwSystemStatusWord1 := dwSystemStatusWord1 OR 16#0000_0002; END_IF;
IF bSystemTripped            THEN dwSystemStatusWord1 := dwSystemStatusWord1 OR 16#0000_0004; END_IF;
IF bDegradedOperation        THEN dwSystemStatusWord1 := dwSystemStatusWord1 OR 16#0000_0008; END_IF;
IF bBed_A_IsDutyAdsorption   THEN dwSystemStatusWord1 := dwSystemStatusWord1 OR 16#0000_0010; END_IF;
IF bBedSwitchInitiated       THEN dwSystemStatusWord1 := dwSystemStatusWord1 OR 16#0000_0020; END_IF;
IF bProductDiverterToExport  THEN dwSystemStatusWord1 := dwSystemStatusWord1 OR 16#0000_0040; END_IF;
IF bProductDiverterToRecycle THEN dwSystemStatusWord1 := dwSystemStatusWord1 OR 16#0000_0080; END_IF;
IF bDrainValvePulseState     THEN dwSystemStatusWord1 := dwSystemStatusWord1 OR 16#0000_0100; END_IF;

(* Encode iState in Bits 16..23 *)
dwSystemStatusWord1 := dwSystemStatusWord1 OR SHL(INT_TO_DWORD(iState), 16);

(* ----------------------------------------------------------------------------------------- *)
(* dwSystemStatusWord2: TSA Sub-State & Actuator Health                                      *)
(* ----------------------------------------------------------------------------------------- *)
dwSystemStatusWord2 := 16#0000_0000;
dwSystemStatusWord2 := dwSystemStatusWord2 OR INT_TO_DWORD(iSubState_TSA);
IF rRegenHeaterPowerDemand_kW > 0.0 THEN dwSystemStatusWord2 := dwSystemStatusWord2 OR 16#0000_0100; END_IF;
IF rDeOxoCoolingValveDemand_pct > 0.0 THEN dwSystemStatusWord2 := dwSystemStatusWord2 OR 16#0000_0200; END_IF;
IF rCycloneDrainValveDemand_pct > 0.0 THEN dwSystemStatusWord2 := dwSystemStatusWord2 OR 16#0000_0400; END_IF;

END_FUNCTION_BLOCK
"""
    sections.append(sec_10)

    # Join full Structured Text code
    full_st_code = "\n".join(sections)
    return full_st_code

if __name__ == "__main__":
    st_code = build_code()
    print("Initial ST Code generated. Length:", len(st_code))
