# -*- coding: utf-8 -*-
"""
Builder script for FB_Refining_FluidCatalyticCracking_RegeneratorMPC
Commercial Sector: Commercial Petrochemicals & Refining: Fluid Catalytic Cracking Unit (FCCU) Catalyst Regenerator & Riser Reactor
Target File: data/swarm_raw/agent_3d91b07c.json
"""

import os
import json
import re
import subprocess
import sys

def build_fccu_st():
    parts = []
    
    # -------------------------------------------------------------------------
    # PART 1: FUNCTION BLOCK DECLARATION & CYBER-PHYSICAL SPECIFICATION HEADER
    # -------------------------------------------------------------------------
    parts.append("FUNCTION_BLOCK FB_Refining_FluidCatalyticCracking_RegeneratorMPC\n")
    
    header = """(*
========================================================================================================================
LUMINA CYBER-PHYSICAL PROCESS AUTOMATION ENGINE - SYNTHETIC DATASET V7 MAX-PERSONA
COMMERCIAL PETROCHEMICALS & REFINING DIVISION - FLUID CATALYTIC CRACKING UNIT (FCCU)
CATALYST REGENERATOR & RISER REACTOR WITH SLIDE VALVE DIFFERENTIAL PRESSURE & RECEDING-HORIZON MPC
========================================================================================================================
SYSTEM SPECIFICATION & ENGINEERING PHENOMENOLOGY:
  Author: Principal Automation Fellow & Cyber-Physical Systems Chair
  Standard: IEC 61131-3 3rd Edition (Ed. 3.0 / TR 61131-8)
  Target SIL Integrity: SIL-3 Execution Architecture (IEC 61508 / IEC 61511 / ISA-84)
  Industrial Domain: Continuous Heavy Petroleum Refining - 120,000 BPD Fluid Catalytic Cracking Unit (FCCU)
  Real-Time Execution Task Periodicity: Ts = 0.050 s (50.0 ms deterministic periodic scan cycle)

1. CYBER-PHYSICAL PROCESS TOPOLOGY & HYDRODYNAMIC COUPLING:
  The Fluid Catalytic Cracking Unit (FCCU) represents the core chemical conversion complex of a modern oil refinery,
  converting low-value heavy atmospheric and vacuum gas oil (VGO/HGO, API gravity 18.0 - 26.0 deg API, CCR 0.5 - 6.5 wt%)
  into high-octane gasoline blending stock, liquefied petroleum gas (LPG olefins: C3=/C4=), light cycle oil (LCO),
  and dry fuel gas. The unit operates as a continuous, tightly coupled circulating fluidized bed (CFB) consisting of
  three primary reaction and regeneration vessels:

  A. RISER CRACKING REACTOR:
     Preheated heavy hydrocarbon feedstock (180 - 320 deg C) is injected through specialized atomizing feed nozzles
     into the base of a vertical riser reactor (diameter 1.8 - 2.4 m, height 35 - 45 m), where it makes instantaneous
     contact with hot regenerated equilibrium catalyst (E-Cat, zeolite Y / USY matrix, particle diameter dp ~ 75 um,
     inflow temperature 680 - 740 deg C). High-pressure dispersion steam (2,000 - 8,000 kg/h) atomizes the oil into
     fine droplet mists (< 50 um), accelerating instantaneous vaporization and endothermic catalytic cracking.
     Riser Outlet Temperature (ROT) must be held strictly between 520.0 and 550.0 deg C (+/- 0.5 deg C precision)
     to maintain targeted conversion without thermal overcracking to dry gas (C1/C2) or excessive heavy coking.
     Catalyst-to-oil mass ratio (CTO) ranges from 5.0 to 8.5 kg catalyst per kg feed, with short contact time (1.5 - 3.0 s).

  B. DISENGAGER-STRIPPER & CATALYST STRIPPING:
     At the riser top, cracked hydrocarbon vapors and spent catalyst are separated via high-efficiency closed cyclones.
     Spent catalyst falls into a counter-current baffle stripper, where superheated steam (1.5 - 3.0 kg steam per ton cat)
     strips volatile and interstitial hydrocarbons from the catalyst pore structures. Inadequate stripping severely
     increases hydrocarbon carryover into the regenerator, producing severe thermal afterburning and oxygen depletion.

  C. CATALYST REGENERATOR (COMBUSTION & FLUIDIZED BED DYNAMICS):
     Spent catalyst bearing 0.85 - 1.45 wt% deposited carbonaceous coke flows into the dense fluidized bed of the
     regenerator (diameter 8.5 - 12.0 m, dense-bed inventory 200 - 300 metric tons, operating pressure 2.0 - 3.5 bar).
     The main combustion air blower (axial/centrifugal compressor, 45,000 - 95,000 Nm3/h) delivers combustion air through
     a multi-nozzle air distribution grid. Coke is combusted at 680 - 740 deg C according to parallel heterogeneous
     reaction kinetics:
         C + O2        --> CO2                (Delta H = -393.5 kJ/mol)
         2 C + O2      --> 2 CO               (Delta H = -221.0 kJ/mol)
         2 H2 + O2     --> 2 H2O              (Delta H = -483.6 kJ/mol)
     Residual carbon on regenerated catalyst (CRC) is reduced to 0.05 - 0.20 wt%. Hot flue gas disengages in the dilute
     freeboard phase and passes through two stages of cyclones before exiting through the flue gas power recovery expander.

2. SLIDE VALVE HYDRAULIC CONTROL & CATASTROPHIC REVERSE FLOW PREVENTION:
  Catalyst circulation between the low-pressure disengager stripper (2.1 bar) and higher-pressure regenerator dense bed
  (2.8 bar), and from the regenerator back to the riser foot, is regulated by two mission-critical electrohydraulic
  slide valves:
     - Regenerated Catalyst Slide Valve (RCSV): regulates hot regenerated catalyst flow to riser foot.
     - Spent Catalyst Slide Valve (SCSV): regulates spent catalyst return flow to regenerator dense bed.
  Each slide valve is driven by a dual-redundant electrohydraulic servo actuator capable of full stroke within 4.5 s
  during modulating control, and fast SIL-3 fail-safe closure within < 850 ms upon emergency de-inventory trip.
  DIFFERENTIAL PRESSURE INTEGRITY (Delta P):
  To guarantee positive hydrodynamic catalyst sealing, the differential pressure across both slide valves must be
  maintained strictly between 0.35 bar (35 kPa) and 0.85 bar (85 kPa).
  HAZARD PHENOMENON:
  If slide valve Delta P drops below 0.25 bar, hydrodynamic head collapses, creating catastrophic REVERSE FLOW:
  Hydrocarbon vapors from the stripper/riser backflow into the oxygen-rich regenerator, triggering instantaneous
  internal vapor-cloud detonation, severe vessel rupture, and catastrophic refinery loss. Conversely, if reverse flow
  drives air into the riser, violent in-situ coke fire and riser metallurgical destruction result.

3. REGENERATOR AFTERBURNING KINETICS & EXPANDER COUPLING:
  In the dilute phase and cyclone plenum, unreacted carbon monoxide can react with residual oxygen:
         2 CO + O2 --> 2 CO2                  (Delta H = -566.0 kJ/mol)
  Because the dilute phase contains low catalyst heat capacity (solids loading < 1.0 kg/m3 vs > 500 kg/m3 in dense bed),
  this exothermic oxidation causes violent thermal afterburning. If plenum temperature exceeds dense bed temperature
  by > 25.0 deg C (warning) or > 45.0 deg C (SIL-3 trip), cyclone structural failure occurs via metal creep.
  Flue gas energy is recovered via an axial power recovery expander turbine driving an electrical generator / motor
  coupled to the main combustion air blower train, requiring precise pressure and bypass valve modulation.

4. MULTIVARIABLE MODEL PREDICTIVE CONTROL (MPC) MATHEMATICAL FORMULATION:
  A 16th-order discrete-time state-space model represents the multivariable interactions of the FCCU:
      x(k+1) = matA * x(k) + matB * delta_u(k)
      y(k)   = matC * x(k) + matD * u(k)
  States x:
      x1: Regenerator dense-bed temperature T_bed [deg C]
      x2: Regenerator dilute-phase cyclone plenum temperature T_cyc [deg C]
      x3: Carbon on regenerated catalyst CRC [wt%]
      x4: Flue gas oxygen concentration [O2] [% vol]
      x5: Flue gas carbon monoxide concentration [CO] [ppm]
      x6: Flue gas carbon dioxide concentration [CO2] [% vol]
      x7: Dense-bed catalyst inventory differential pressure Delta P_bed [kPa]
      x8: Regenerated catalyst slide valve differential pressure Delta P_rcsv [bar]
      x9: Spent catalyst slide valve differential pressure Delta P_scsv [bar]
      x10: Catalyst circulation mass flow rate W_cat [t/min]
      x11: Riser outlet temperature ROT [deg C]
      x12: Riser cracking conversion severity index [%]
      x13: Disengager stripper bed catalyst level L_strip [%]
      x14: Stripper hydrocarbon vapor entrainment index [g/kg]
      x15: Main air blower delivery pressure P_air [bar]
      x16: Wet gas compressor suction pressure P_wgc [bar]
  Manipulated Inputs u:
      u1: Regenerated catalyst slide valve position MV_rcsv [%]
      u2: Spent catalyst slide valve position MV_scsv [%]
      u3: Combustion air blower inlet guide vanes MV_blower [%]
      u4: Feed preheat furnace firing duty MV_furnace [%]
      u5: Feed mass flow rate feedforward DV_feed [t/h]
      u6: Feed nozzle dispersion steam trim valve MV_disp [%]
      u7: Stripper superheated steam valve MV_steam [%]
      u8: Feed Conradson Carbon Residue disturbance DV_ccr [wt%]
  The receding-horizon MPC executes Projected Gradient Descent (PGD) with quadratic cost weights Q and R,
  augmented with nonlinear barrier penalty functions guarding against slide valve reverse flow, cyclone afterburning,
  blower surge boundary violation, and riser thermal over-shoot.

5. TRIPLE MODULAR REDUNDANCY (2oo3) VOTING ARCHITECTURE:
  Triplicated sensor arrays are deployed across 4 mission-critical measurement nodes:
     1) Regenerated Catalyst Slide Valve Delta P Transmitters (2oo3);
     2) Spent Catalyst Slide Valve Delta P Transmitters (2oo3);
     3) Regenerator Dense-Bed Thermocouples at 120-degree orientation (2oo3);
     4) Flue Gas Oxygen Zirconia Electrochemical Analyzers (2oo3).
  The voting engine executes cyclic median bubble sorting, discrepancy debounce timers, and bumpless
  dynamic degradation across 4 health levels: 3 healthy (2oo3 median) -> 2 healthy (1oo2 mean) ->
  1 healthy (1oo1 fallback with high-priority warning) -> 0 healthy (SIL-3 trip to safe fallback state).
========================================================================================================================
*)
"""
    parts.append(header)
    
    # -------------------------------------------------------------------------
    # PART 2: VAR_INPUT DECLARATIONS
    # -------------------------------------------------------------------------
    var_input = """VAR_INPUT
    (* === SUPERVISORY PERMISSIVES & HARDWIRED SIL-3 SAFETY CIRCUITS === *)
    bEnableMasterFCCU               : BOOL;     (* Master FCCU automation supervisory permissive [TRUE=Arm, FALSE=Disarm] *)
    bEmergencyTripCircuit           : BOOL;     (* SIL-3 hardwired emergency de-inventory manual trip switch (Active Low: FALSE=Trip) *)
    bAcknowledgeAlarms              : BOOL;     (* Operator pushbutton for ISA-18.2 alarm acknowledge and trip reset *)
    bManualModePermissive           : BOOL;     (* Authorized maintenance manual override permissive switch *)
    bExpanderCoupledPermissive      : BOOL;     (* Flue gas power recovery expander turbine clutch engaged permissive *)

    (* === TRIPLICATED 2oo3 REGENERATED CATALYST SLIDE VALVE DELTA P TRANSMITTERS === *)
    rRCSV_DeltaP_Transmitters       : ARRAY[1..3] OF REAL; (* Regenerated catalyst slide valve differential pressure [bar] *)

    (* === TRIPLICATED 2oo3 SPENT CATALYST SLIDE VALVE DELTA P TRANSMITTERS === *)
    rSCSV_DeltaP_Transmitters       : ARRAY[1..3] OF REAL; (* Spent catalyst slide valve differential pressure [bar] *)

    (* === TRIPLICATED 2oo3 REGENERATOR DENSE-BED THERMOCOUPLES === *)
    rRegenBedTemp_Transmitters      : ARRAY[1..3] OF REAL; (* Regenerator dense-bed thermocouples at 120-deg orientation [deg C] *)

    (* === TRIPLICATED 2oo3 FLUE GAS OXYGEN ZIRCONIA ANALYZERS === *)
    rFlueGasO2_Transmitters         : ARRAY[1..3] OF REAL; (* Regenerator dilute-phase flue gas oxygen zirconia analyzers [%] *)

    (* === RISER REACTOR & FEED SYSTEM PROCESS FEEDBACKS === *)
    rRiserOutletTemp_Actual         : REAL;     (* Riser reactor top cyclone outlet vapor temperature (ROT) [deg C] *)
    rRiserInletFeedTemp_Actual      : REAL;     (* Heavy gas oil feed preheat furnace outlet temperature [deg C] *)
    rFeedMassFlowRate_Actual        : REAL;     (* Total heavy gas oil (HGO/VGO) feed mass flow rate to feed nozzles [t/h] *)
    rDispersionSteamFlow_Actual     : REAL;     (* Feed nozzle high-pressure atomization dispersion steam flow rate [kg/h] *)
    rStrippingSteamFlow_Actual      : REAL;     (* Disengager stripper bed steam mass flow rate [kg/h] *)
    rFeedSpecificGravityAPI         : REAL;     (* On-line near-IR analyzer heavy gas oil feed density [deg API] *)
    rFeedConradsonCarbonRes         : REAL;     (* Heavy gas oil feed Conradson Carbon Residue (CCR) content [wt%] *)

    (* === REGENERATOR & COMBUSTION AIR SYSTEM FEEDBACKS === *)
    rMainAirBlowerFlow_Actual       : REAL;     (* Combustion air blower delivered mass flow rate to regenerator grid [Nm3/h] *)
    rAirBlowerDischargePress        : REAL;     (* Main air blower discharge air header pressure [bar] *)
    rRegenDilutePhaseTemp           : REAL;     (* Regenerator cyclone dilute-phase freeboard gas temperature [deg C] *)
    rRegenCyclonePlenumTemp         : REAL;     (* Regenerator primary cyclone outlet plenum gas temperature [deg C] *)
    rRegenBedDifferentialPress      : REAL;     (* Dense-bed catalyst inventory differential pressure transmitter [kPa] *)
    rFlueGasCO_Concentration        : REAL;     (* Flue gas carbon monoxide infrared analyzer [ppm] *)
    rFlueGasCO2_Concentration       : REAL;     (* Flue gas carbon dioxide analyzer [%] *)

    (* === FRACTIONATOR & EXPANDER COUPLING FEEDBACKS === *)
    rWetGasCompSuctionPress         : REAL;     (* Wet gas compressor (WGC) suction drum vapor pressure [bar] *)
    rRiserPressureActual            : REAL;     (* Riser disengager vapor dome pressure [bar] *)
    rExpanderInletFlueGasPress      : REAL;     (* Flue gas power recovery expander turbine inlet pressure [bar] *)
    rExpanderPowerGeneration        : REAL;     (* Flue gas power recovery expander electrical output [kW] *)
END_VAR
"""
    parts.append(var_input)
    
    # -------------------------------------------------------------------------
    # PART 3: VAR_OUTPUT DECLARATIONS
    # -------------------------------------------------------------------------
    var_output = """VAR_OUTPUT
    (* === SUPERVISORY AUTOMATION STATUS & SYSTEM INTERLOCK WORDS === *)
    bFCCU_SystemReady               : BOOL;     (* FCCU cyber-physical automation subsystem online and calibrated *)
    bMPC_OptimizationActive         : BOOL;     (* 16-state multivariable receding horizon MPC active and healthy *)
    bFeedInflowPermissive           : BOOL;     (* Permissive signal to open heavy gas oil feed isolation valves *)
    bExpanderCoupled                : BOOL;     (* Flue gas power recovery expander coupled to motor/blower train *)
    bSlideValveReverseFlowWarning   : BOOL;     (* Low slide valve differential pressure reverse flow warning *)
    bSlideValveFastTripActive       : BOOL;     (* SIL-3 emergency hydraulic fast-close actuator triggered *)
    bAfterburningDetected           : BOOL;     (* Dilute-phase cyclone afterburning thermal runaway detected *)
    bSensorTMR_Degraded             : BOOL;     (* TMR voting engine operating under degraded 1oo2 or 1oo1 logic *)
    bEmergencySnuffingActive        : BOOL;     (* Emergency steam snuffing active into regenerator dilute phase *)

    (* === STATUS & ISA-18.2 TELEMETRY BITMASKS === *)
    wFCCU_OperationalStatus         : WORD;     (* 16-bit packed machine operational state word *)
    dwISA182_AlarmWord_1            : DWORD;    (* ISA-18.2 primary safety and critical trip alarm bitmask *)
    dwISA182_AlarmWord_2            : DWORD;    (* ISA-18.2 secondary process advisory and deviation alarm bitmask *)

    (* === MODULATING ACTUATOR COMMAND SETPOINTS === *)
    rRCSV_PositionSetpointCmd       : REAL;     (* Regenerated catalyst slide valve hydraulic servo command [%] *)
    rSCSV_PositionSetpointCmd       : REAL;     (* Spent catalyst slide valve hydraulic servo command [%] *)
    rAirBlowerGuideVanesCmd         : REAL;     (* Main combustion air blower inlet guide vane (IGV) pitch command [%] *)
    rPreheatFurnaceFuelDutyCmd      : REAL;     (* Feed preheat furnace fuel gas firing duty command [%] *)
    rStrippingSteamValveCmd         : REAL;     (* Stripper superheated steam control valve position [%] *)
    rDispersionSteamValveCmd        : REAL;     (* Feed nozzle dispersion steam trim valve position [%] *)
    rSnuffingSteamDumpValveCmd      : REAL;     (* Regenerator dilute-phase emergency snuffing steam valve [%] *)

    (* === ESTIMATED CYBER-PHYSICAL OBSERVABLES & REACTION METRICS === *)
    rEstimatedRiserOutletTemp       : REAL;     (* Observer estimated riser outlet temperature (ROT) [deg C] *)
    rEstimatedRegenBedTemp          : REAL;     (* Observer estimated regenerator dense-bed temperature [deg C] *)
    rEstimatedCatCirculationRate    : REAL;     (* Observer calculated catalyst circulation rate [t/min] *)
    rEstimatedCokeOnRegenCat        : REAL;     (* Observer estimated carbon on regenerated catalyst (CRC) [wt%] *)
    rEstimatedCokeBurnRate          : REAL;     (* Observer calculated coke combustion reaction rate [kg/h] *)
    rEstimatedCatToOilRatio         : REAL;     (* Observer calculated catalyst-to-oil mass ratio (CTO) [-] *)
    rCycloneDeltaT_Actual           : REAL;     (* Temperature difference across cyclone plenum [deg C] *)
    rBlowerSurgeMarginPct           : REAL;     (* Main combustion air blower distance to surge line [%] *)
    iActiveFSMStateIndex            : INT;      (* Currently active 12-stage operational state index *)
END_VAR
"""
    parts.append(var_output)
    
    # -------------------------------------------------------------------------
    # PART 4: VAR INTERNAL DECLARATIONS
    # -------------------------------------------------------------------------
    var_block = """VAR
    (* === SEQUENTIAL EXECUTION REGISTERS === *)
    iStateStep                      : INT := 0; (* Current operational state machine step index *)
    iPreviousState                  : INT := 0; (* Preceding state index for edge transition logging *)
    bFirstExecutionScan             : BOOL := TRUE; (* Cold boot initialization flag *)
    dwScanCycleCounter              : DWORD := 0; (* 50ms periodic cyclic scan counter *)

    (* === 2oo3 TMR VOTING ENGINE: REGENERATED CATALYST SLIDE VALVE DELTA P === *)
    rVoted_RCSV_DeltaP              : REAL := 0.55; (* 2oo3 voted RCSV differential pressure [bar] *)
    bHealthy_RCSV_Sensors           : ARRAY[1..3] OF BOOL := [TRUE, TRUE, TRUE]; (* Sensor health array *)
    rDiscrepancyTimer_RCSV          : ARRAY[1..3] OF REAL := [0.0, 0.0, 0.0]; (* Debounce accumulation timers [s] *)
    iHealthyCount_RCSV              : INT := 3; (* Count of operational RCSV Delta P transmitters *)
    rThreshold_RCSV_DeltaP          : REAL := 0.075; (* Maximum channel divergence threshold [bar] *)

    (* === 2oo3 TMR VOTING ENGINE: SPENT CATALYST SLIDE VALVE DELTA P === *)
    rVoted_SCSV_DeltaP              : REAL := 0.52; (* 2oo3 voted SCSV differential pressure [bar] *)
    bHealthy_SCSV_Sensors           : ARRAY[1..3] OF BOOL := [TRUE, TRUE, TRUE]; (* Sensor health array *)
    rDiscrepancyTimer_SCSV          : ARRAY[1..3] OF REAL := [0.0, 0.0, 0.0]; (* Debounce accumulation timers [s] *)
    iHealthyCount_SCSV              : INT := 3; (* Count of operational SCSV Delta P transmitters *)
    rThreshold_SCSV_DeltaP          : REAL := 0.075; (* Maximum channel divergence threshold [bar] *)

    (* === 2oo3 TMR VOTING ENGINE: REGENERATOR DENSE-BED TEMPERATURE === *)
    rVoted_RegenBedTemp             : REAL := 710.0; (* 2oo3 voted regenerator dense-bed temperature [deg C] *)
    bHealthy_RegenTempSensors       : ARRAY[1..3] OF BOOL := [TRUE, TRUE, TRUE]; (* Sensor health array *)
    rDiscrepancyTimer_RegenTemp     : ARRAY[1..3] OF REAL := [0.0, 0.0, 0.0]; (* Debounce accumulation timers [s] *)
    iHealthyCount_RegenTemp         : INT := 3; (* Count of operational bed thermocouples *)
    rThreshold_RegenBedTemp         : REAL := 15.0; (* Maximum channel divergence threshold [deg C] *)

    (* === 2oo3 TMR VOTING ENGINE: FLUE GAS OXYGEN CONCENTRATION === *)
    rVoted_FlueGasO2                : REAL := 1.85; (* 2oo3 voted flue gas oxygen concentration [%] *)
    bHealthy_FlueGasO2Sensors       : ARRAY[1..3] OF BOOL := [TRUE, TRUE, TRUE]; (* Sensor health array *)
    rDiscrepancyTimer_FlueGasO2     : ARRAY[1..3] OF REAL := [0.0, 0.0, 0.0]; (* Debounce accumulation timers [s] *)
    iHealthyCount_FlueGasO2         : INT := 3; (* Count of operational flue gas O2 analyzers *)
    rThreshold_FlueGasO2            : REAL := 0.45; (* Maximum channel divergence threshold [%] *)

    (* === PHYSICAL, CHEMICAL KINETIC & HYDRODYNAMIC CONSTANTS === *)
    rCatSpecificHeat                : REAL := 1.15;  (* Equilibrium catalyst specific heat capacity [kJ/(kg*K)] *)
    rAirSpecificHeat                : REAL := 1.08;  (* Combustion air specific heat capacity [kJ/(kg*K)] *)
    rFlueGasSpecificHeat            : REAL := 1.12;  (* Regenerator flue gas specific heat capacity [kJ/(kg*K)] *)
    rFeedSpecificHeat               : REAL := 2.55;  (* Heavy gas oil liquid feed specific heat capacity [kJ/(kg*K)] *)
    rVaporSpecificHeat              : REAL := 3.10;  (* Cracked hydrocarbon vapor specific heat [kJ/(kg*K)] *)
    rDeltaH_CokeCombustion          : REAL := 32500.0; (* Heat of coke combustion reaction [kJ/kg coke] *)
    rDeltaH_RiserCracking           : REAL := 450.0;   (* Endothermic heat of catalytic cracking [kJ/kg feed] *)
    rDeltaH_CO_Oxidation            : REAL := 10100.0; (* Exothermic heat of carbon monoxide afterburning [kJ/kg CO] *)
    rArrheniusA_Coke                : REAL := 24500.0; (* Coke combustion Arrhenius pre-exponential factor [1/(bar*s)] *)
    rActivationEnergy_Coke          : REAL := 85500.0; (* Coke combustion activation energy [J/mol] *)
    rGasConstant_R                  : REAL := 8.314;   (* Universal gas constant [J/(mol*K)] *)
    rValveCd_RCSV                   : REAL := 0.68;    (* Discharge coefficient of regenerated catalyst slide valve *)
    rValveCd_SCSV                   : REAL := 0.65;    (* Discharge coefficient of spent catalyst slide valve *)
    rCatDensity_Aerated             : REAL := 780.0;   (* Aerated fluidized catalyst density in standpipes [kg/m3] *)
    rCatDensity_Settled             : REAL := 950.0;   (* Settled catalyst density [kg/m3] *)
    rValvePortAreaMax               : REAL := 0.42;    (* Maximum slide valve full-bore orifice throat area [m2] *)
    rRegenCatalystInventory_Tons    : REAL := 245.0;   (* Total regenerator dense-bed catalyst inventory [metric tons] *)
    rStripperCatInventory_Tons      : REAL := 68.0;    (* Total disengager stripper catalyst inventory [metric tons] *)

    (* === PROCESS SETPOINTS & ISA-18.2 OPERATIONAL SAFETY BOUNDARIES === *)
    rTargetRiserOutletTemp          : REAL := 535.0; (* Target Riser Outlet Temperature setpoint [deg C] *)
    rMaxAllowableROT                : REAL := 550.0; (* High-High trip threshold for riser outlet temperature [deg C] *)
    rMinAllowableROT                : REAL := 515.0; (* Low-Low trip threshold for riser outlet temperature [deg C] *)
    rTargetRegenBedTemp             : REAL := 715.0; (* Target regenerator dense-bed temperature [deg C] *)
    rMaxAllowableRegenTemp          : REAL := 750.0; (* High-High thermal trip for regenerator dense bed [deg C] *)
    rMaxCycloneDeltaT_Trip          : REAL := 45.0;  (* High-High afterburning trip across cyclone plenum [deg C] *)
    rMaxCycloneDeltaT_Warn          : REAL := 25.0;  (* High warning afterburning across cyclone plenum [deg C] *)
    rMinSlideValveDeltaP_Trip       : REAL := 0.25;  (* Reverse flow SIL-3 fast-close Delta P trip limit [bar] *)
    rMinSlideValveDeltaP_Warn       : REAL := 0.35;  (* Reverse flow advisory alarm Delta P limit [bar] *)
    rTargetSlideValveDeltaP         : REAL := 0.55;  (* Normal target slide valve differential pressure [bar] *)
    rMinCombustionAirFlow_Trip      : REAL := 28000.0; (* Low-Low combustion air trip limit [Nm3/h] *)

    (* === 16x16 DISCRETE-TIME STATE-SPACE SYSTEM MATRICES (Ts = 0.050 s) === *)
    matA : ARRAY[1..16, 1..16] OF REAL := [
        (* Row 1: T_bed *)
        [0.9650, 0.0080, 0.0450, 0.0180, 0.0000, 0.0000, 0.0012, 0.0000, 0.0000,-0.0085, 0.0000, 0.0000, 0.0000, 0.0000, 0.0045, 0.0000],
        (* Row 2: T_cyc *)
        [0.0150, 0.9420, 0.0000, 0.0380, 0.0240, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0120, 0.0035, 0.0000],
        (* Row 3: CRC *)
        [-0.0008, 0.0000, 0.9250,-0.0045, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000,-0.0012, 0.0000, 0.0028, 0.0000, 0.0000,-0.0025, 0.0000],
        (* Row 4: [O2] *)
        [-0.0015,-0.0010,-0.0850, 0.8850,-0.0120, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000,-0.0045, 0.0420, 0.0000],
        (* Row 5: [CO] *)
        [0.0250, 0.0180, 0.1250,-0.0650, 0.8650,-0.0150, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0350,-0.0220, 0.0000],
        (* Row 6: [CO2] *)
        [0.0045, 0.0020, 0.0950, 0.0450, 0.0320, 0.9100, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0080, 0.0180, 0.0000],
        (* Row 7: Delta P_bed *)
        [0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.9750, 0.0000, 0.0000,-0.0055, 0.0000, 0.0000, 0.0042, 0.0000, 0.0065, 0.0000],
        (* Row 8: Delta P_rcsv *)
        [0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0025, 0.9150, 0.0000,-0.0120, 0.0000, 0.0000, 0.0000, 0.0000, 0.0015,-0.0045],
        (* Row 9: Delta P_scsv *)
        [0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000,-0.0018, 0.0000, 0.9120,-0.0115, 0.0000, 0.0000, 0.0035, 0.0000,-0.0020, 0.0050],
        (* Row 10: W_cat *)
        [0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0045, 0.0550, 0.0480, 0.8950, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
        (* Row 11: ROT *)
        [0.0185, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0420, 0.8450,-0.0280, 0.0000, 0.0000, 0.0000, 0.0000],
        (* Row 12: X_crack *)
        [0.0012, 0.0000,-0.0150, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0085, 0.0350, 0.8800, 0.0000, 0.0000, 0.0000, 0.0000],
        (* Row 13: L_strip *)
        [0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0150, 0.0000, 0.0000, 0.9650, 0.0000, 0.0000, 0.0000],
        (* Row 14: H_strip *)
        [0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0045, 0.0000, 0.0085, 0.0120, 0.8750, 0.0000, 0.0000],
        (* Row 15: P_air *)
        [0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0008, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.8900, 0.0000],
        (* Row 16: P_wgc *)
        [0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0045, 0.0080, 0.0000, 0.0000, 0.0000, 0.8650]
    ];

    (* === 16x8 INPUT COUPLING MATRIX matB === *)
    matB : ARRAY[1..16, 1..8] OF REAL := [
        (* State 1: T_bed *)
        [-0.0120,  0.0185,  0.0650,  0.0000, -0.0045,  0.0000,  0.0000,  0.0240],
        (* State 2: T_cyc *)
        [ 0.0000,  0.0000,  0.0250,  0.0000,  0.0000,  0.0000, -0.0150,  0.0180],
        (* State 3: CRC *)
        [-0.0018,  0.0042, -0.0085,  0.0000,  0.0025,  0.0000,  0.0000,  0.0095],
        (* State 4: [O2] *)
        [ 0.0000, -0.0055,  0.0850,  0.0000, -0.0120,  0.0000,  0.0000, -0.0140],
        (* State 5: [CO] *)
        [ 0.0000,  0.0120, -0.0450,  0.0000,  0.0180,  0.0000, -0.0080,  0.0350],
        (* State 6: [CO2] *)
        [ 0.0000,  0.0085,  0.0380,  0.0000,  0.0065,  0.0000,  0.0000,  0.0120],
        (* State 7: Delta P_bed *)
        [-0.0085,  0.0140,  0.0045,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000],
        (* State 8: Delta P_rcsv *)
        [-0.0240,  0.0000,  0.0035,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000],
        (* State 9: Delta P_scsv *)
        [ 0.0000, -0.0220, -0.0025,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000],
        (* State 10: W_cat *)
        [ 0.0750,  0.0680,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000],
        (* State 11: ROT *)
        [ 0.0520,  0.0000,  0.0000,  0.0280, -0.0450, -0.0065,  0.0000,  0.0000],
        (* State 12: X_crack *)
        [ 0.0180,  0.0000,  0.0000,  0.0120, -0.0220,  0.0085,  0.0000, -0.0045],
        (* State 13: L_strip *)
        [ 0.0000, -0.0250,  0.0000,  0.0000,  0.0180,  0.0000,  0.0000,  0.0000],
        (* State 14: H_strip *)
        [ 0.0000,  0.0000,  0.0000,  0.0000,  0.0140,  0.0000, -0.0380,  0.0065],
        (* State 15: P_air *)
        [ 0.0000,  0.0000,  0.0480,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000],
        (* State 16: P_wgc *)
        [ 0.0000,  0.0000,  0.0000,  0.0000,  0.0320,  0.0000,  0.0000,  0.0000]
    ];

    (* === 8x16 OUTPUT OBSERVATION MATRIX matC === *)
    matC : ARRAY[1..8, 1..16] OF REAL := [
        (* y1: T_bed *)
        [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        (* y2: ROT *)
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        (* y3: Delta P_rcsv *)
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        (* y4: Delta P_scsv *)
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        (* y5: [O2] *)
        [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        (* y6: Cyclone Delta T = T_cyc - T_bed *)
        [-1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        (* y7: Delta P_bed *)
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        (* y8: CRC *)
        [0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    ];

    (* === 8x8 FEEDFORWARD DIRECT TRANSMISSION MATRIX matD === *)
    matD : ARRAY[1..8, 1..8] OF REAL := [
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    ];

    (* === 16x8 OBSERVER KALMAN/LUENBERGER GAIN MATRIX matL === *)
    matL : ARRAY[1..16, 1..8] OF REAL := [
        [0.2450, 0.0000, 0.0000, 0.0000, 0.0120,-0.0850, 0.0050, 0.0000],
        [0.0150, 0.0000, 0.0000, 0.0000, 0.0240, 0.3150, 0.0000, 0.0000],
        [-0.0012, 0.0000, 0.0000, 0.0000,-0.0085, 0.0000, 0.0000, 0.2850],
        [0.0000, 0.0000, 0.0000, 0.0000, 0.3450, 0.0120, 0.0000,-0.0150],
        [0.0050, 0.0000, 0.0000, 0.0000,-0.0450, 0.0180, 0.0000, 0.0240],
        [0.0020, 0.0000, 0.0000, 0.0000, 0.0180, 0.0050, 0.0000, 0.0120],
        [0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.3200, 0.0000],
        [0.0000, 0.0000, 0.3100, 0.0000, 0.0000, 0.0000, 0.0080, 0.0000],
        [0.0000, 0.0000, 0.0000, 0.2950, 0.0000, 0.0000,-0.0065, 0.0000],
        [0.0000, 0.0150, 0.0250, 0.0220, 0.0000, 0.0000, 0.0120, 0.0000],
        [0.0000, 0.3850, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
        [0.0000, 0.0450, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0180],
        [0.0000, 0.0000, 0.0000,-0.0180, 0.0000, 0.0000, 0.0250, 0.0000],
        [0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0150, 0.0000, 0.0080],
        [0.0000, 0.0000, 0.0000, 0.0000, 0.0120, 0.0000, 0.0000, 0.0000],
        [0.0000, 0.0085, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000]
    ];

    (* === MODEL PREDICTIVE CONTROL STATE & VECTOR REGISTERS === *)
    vecStateEstimate                : ARRAY[1..16] OF REAL := [710.0, 718.0, 0.12, 1.85, 120.0, 16.5, 62.0, 0.55, 0.52, 34.5, 535.0, 74.5, 52.0, 1.25, 3.45, 1.85];
    vecStatePredicted               : ARRAY[1..16] OF REAL := [710.0, 718.0, 0.12, 1.85, 120.0, 16.5, 62.0, 0.55, 0.52, 34.5, 535.0, 74.5, 52.0, 1.25, 3.45, 1.85];
    vecMeasuredOutputs              : ARRAY[1..8] OF REAL := [710.0, 535.0, 0.55, 0.52, 1.85, 8.0, 62.0, 0.12];
    vecOutputReference              : ARRAY[1..8] OF REAL := [715.0, 535.0, 0.55, 0.52, 1.75, 10.0, 62.0, 0.10];
    vecInnovationResidual           : ARRAY[1..8] OF REAL := [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0];

    vecControlCurrent               : ARRAY[1..8] OF REAL := [48.5, 51.2, 68.5, 55.0, 280.0, 35.0, 42.0, 3.2];
    vecControlPrevious              : ARRAY[1..8] OF REAL := [48.5, 51.2, 68.5, 55.0, 280.0, 35.0, 42.0, 3.2];
    vecDeltaU                       : ARRAY[1..8] OF REAL := [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0];
    vecControlMinLimits             : ARRAY[1..8] OF REAL := [10.0, 10.0, 25.0, 10.0, 50.0, 10.0, 15.0, 0.5];
    vecControlMaxLimits             : ARRAY[1..8] OF REAL := [90.0, 90.0, 98.0, 95.0, 420.0, 90.0, 90.0, 8.0];
    vecMaxSlewRatePerScan           : ARRAY[1..8] OF REAL := [0.35, 0.35, 0.50, 0.40, 1.20, 0.50, 0.60, 0.10];

    (* MPC Quadratic Weights & Barrier Penalties *)
    vecOutputWeight_Q               : ARRAY[1..8] OF REAL := [0.085, 45.0, 850.0, 850.0, 12.0, 8.5, 0.25, 120.0];
    vecInputRateWeight_R            : ARRAY[1..8] OF REAL := [0.150, 0.150, 0.080, 0.050, 0.000, 0.025, 0.035, 0.000];
    rReverseFlowPenaltyWeight       : REAL := 45000.0; (* Soft barrier weight for slide valve Delta P < 0.40 bar *)
    rAfterburningPenaltyWeight      : REAL := 18500.0; (* Soft barrier weight for cyclone Delta T > 25.0 deg C *)
    rRotExcursionPenaltyWeight      : REAL := 22000.0; (* Soft barrier weight for ROT deviation > 1.5 deg C *)
    rBlowerSurgePenaltyWeight       : REAL := 35000.0; (* Soft barrier weight for combustion air near surge line *)
    rPGD_StepSize                   : REAL := 0.00045; (* Projected gradient descent convergence step size *)
    iMPC_MaxIterations              : INT := 8;        (* Maximum PGD iterations per cyclic task *)

    (* === TIMERS FOR 12-STAGE FINITE STATE MACHINE === *)
    tStateTimer                     : TON; (* General dwell timer for operational transitions *)
    tAirPurgeTimer                  : TON; (* Timer for refractory purge & air blower soak *)
    tRefractoryWarmupTimer          : TON; (* Timer for initial refractory curing thermal ramp *)
    tTorchingOilTimer               : TON; (* Timer for torching oil ignition burn-in *)
    tCatCirculationBalancingTimer   : TON; (* Timer for slide valve hydraulic balance verification *)
    tFeedCutInRampTimer             : TON; (* Timer for heavy gas oil feed ramp-up *)
    tSnuffingSteamTimer             : TON; (* Emergency snuffing steam injection timer *)
    tEmergencyNitrogenTimer         : TON; (* Emergency N2 inerting timer *)
    tHeartbeatOscillator            : TON; (* Cyclic toggle timer for PLC alive watchdog *)
    bHeartbeatPulse                 : BOOL := FALSE; (* Alive heartbeat toggle bit *)

    (* === EVENT & DIAGNOSTIC REGISTERS === *)
    dwTotalCrackingHours            : DWORD := 0; (* Cumulative hours of active cracking *)
    dwSlideValveMoveEvents          : DWORD := 0; (* Slide valve stroke modulation counter *)
    rPeakRegenCycloneTemp           : REAL := 0.0; (* Historical maximum recorded cyclone temperature [deg C] *)
END_VAR
"""
    parts.append(var_block)
    
    # -------------------------------------------------------------------------
    # PART 5: VAR_TEMP DECLARATIONS
    # -------------------------------------------------------------------------
    var_temp = """VAR_TEMP
    iLoopI                          : INT;      (* Matrix & vector loop index i *)
    jLoopJ                          : INT;      (* Matrix & vector loop index j *)
    kIterK                          : INT;      (* PGD optimization iteration index k *)
    rTempSum                        : REAL;     (* General-purpose accumulator *)
    rMedianBuffer                   : ARRAY[1..3] OF REAL; (* Temporary sorting buffer for 2oo3 median voting *)
    rSwapBuffer                     : REAL;     (* Bubble sort exchange register *)
    rBarrierGradient_RCSV           : REAL;     (* Reverse flow barrier penalty gradient for RCSV Delta P *)
    rBarrierGradient_SCSV           : REAL;     (* Reverse flow barrier penalty gradient for SCSV Delta P *)
    rBarrierGradient_Afterburn      : REAL;     (* Cyclone afterburning barrier penalty gradient *)
    rBarrierGradient_ROT            : REAL;     (* Riser outlet temperature barrier penalty gradient *)
    rBarrierGradient_Surge          : REAL;     (* Air blower compressor surge barrier penalty gradient *)
    rGradientVector                 : ARRAY[1..8] OF REAL; (* Multivariable cost function gradient vector *)
    rCandidateU                     : REAL;     (* Temporary bounded control actuator value *)
    rCalculatedDeltaT               : REAL;     (* Calculated cyclone plenum temperature differential *)
    rSurgeLimitFlow                 : REAL;     (* Calculated air blower minimum surge flow at current pressure *)
    rCatalystFlow_kg_s              : REAL;     (* Computed catalyst circulation rate [kg/s] *)
    rCokeCombustionKineticK         : REAL;     (* Arrhenius reaction rate constant [1/(bar*s)] *)
END_VAR
"""
    parts.append(var_temp)
    
    # -------------------------------------------------------------------------
    # PART 6: PHASE 1 - SAFETY INTERLOCKS & WATCHDOG
    # -------------------------------------------------------------------------
    phase1 = """(*
========================================================================================================================
  PHASE 1: SIL-3 SAFETY INTERLOCKS, HEARTBEAT WATCHDOG & PERMISSIVES
========================================================================================================================
*)
dwScanCycleCounter := dwScanCycleCounter + 1;

(* Cyclic Heartbeat Watchdog Pulse (0.5 Hz Square Wave) *)
tHeartbeatOscillator(IN := NOT tHeartbeatOscillator.Q, PT := T#1000MS);
IF tHeartbeatOscillator.Q THEN
    bHeartbeatPulse := NOT bHeartbeatPulse;
END_IF;

(* Master Hardwired SIL-3 Emergency De-Inventory Safety Circuit (Active Low Trip) *)
IF NOT bEmergencyTripCircuit THEN
    iStateStep := 120; (* Immediate transition to SIL-3 Fast Close Safe State *)
    bSlideValveFastTripActive := TRUE;
    bFeedInflowPermissive := FALSE;
    bMPC_OptimizationActive := FALSE;
    bFCCU_SystemReady := FALSE;
    dwISA182_AlarmWord_1.0 := TRUE; (* SIL-3 Emergency De-Inventory Trip Activated *)

    (* Immediate Actuator Dump Commands *)
    rRCSV_PositionSetpointCmd := 0.0;
    rSCSV_PositionSetpointCmd := 0.0;
    rPreheatFurnaceFuelDutyCmd := 0.0;
    rSnuffingSteamDumpValveCmd := 100.0; (* Full open emergency snuffing steam *)
    rAirBlowerGuideVanesCmd := 25.0;     (* Minimum blower flow / anti-surge open *)
    iActiveFSMStateIndex := iStateStep;
    RETURN;
END_IF;

(* Master Supervisory Enable Check *)
IF NOT bEnableMasterFCCU AND (iStateStep > 0) AND (iStateStep < 100) THEN
    iStateStep := 100; (* Controlled shutdown to Catalyst Purge & Inactive Circulation *)
    bMPC_OptimizationActive := FALSE;
    bFeedInflowPermissive := FALSE;
END_IF;

(* Operator Pushbutton Alarm Acknowledgment & Trip Reset *)
IF bAcknowledgeAlarms THEN
    dwISA182_AlarmWord_1.1 := FALSE;
    dwISA182_AlarmWord_1.2 := FALSE;
    dwISA182_AlarmWord_1.3 := FALSE;
    dwISA182_AlarmWord_1.4 := FALSE;
    dwISA182_AlarmWord_1.5 := FALSE;
    dwISA182_AlarmWord_1.6 := FALSE;
    dwISA182_AlarmWord_1.7 := FALSE;
    dwISA182_AlarmWord_1.8 := FALSE;
    dwISA182_AlarmWord_1.9 := FALSE;
    dwISA182_AlarmWord_1.10 := FALSE;
    dwISA182_AlarmWord_2.0 := FALSE;
    dwISA182_AlarmWord_2.1 := FALSE;
    dwISA182_AlarmWord_2.2 := FALSE;
    dwISA182_AlarmWord_2.3 := FALSE;
    dwISA182_AlarmWord_2.4 := FALSE;
    dwISA182_AlarmWord_2.5 := FALSE;
    dwISA182_AlarmWord_2.6 := FALSE;
    dwISA182_AlarmWord_2.7 := FALSE;
    dwISA182_AlarmWord_2.8 := FALSE;

    (* Reset from Safe Lockout if safety circuit restored *)
    IF (iStateStep = 120) AND bEmergencyTripCircuit THEN
        iStateStep := 0; (* Cold Standby *)
        bSlideValveFastTripActive := FALSE;
        dwISA182_AlarmWord_1.0 := FALSE;
    END_IF;
END_IF;
"""
    parts.append(phase1)
    
    # -------------------------------------------------------------------------
    # PART 7: PHASE 2 - FOUR 2oo3 TMR SENSOR VOTING ENGINES
    # -------------------------------------------------------------------------
    phase2 = """(*
========================================================================================================================
  PHASE 2: TRIPLE MODULAR REDUNDANCY (2oo3) SENSOR VOTING ENGINES WITH DEGRADATION
========================================================================================================================
*)
(* -------------------------------------------------------------------------------------------------- *)
(* ENGINE 2A: REGENERATED CATALYST SLIDE VALVE DELTA P (2oo3 MEDIAN VOTING)                           *)
(* -------------------------------------------------------------------------------------------------- *)
rMedianBuffer[1] := rRCSV_DeltaP_Transmitters[1];
rMedianBuffer[2] := rRCSV_DeltaP_Transmitters[2];
rMedianBuffer[3] := rRCSV_DeltaP_Transmitters[3];

(* 3-Element Bubble Sort *)
FOR iLoopI := 1 TO 2 DO
    FOR jLoopJ := 1 TO 3 - iLoopI DO
        IF rMedianBuffer[jLoopJ] > rMedianBuffer[jLoopJ + 1] THEN
            rSwapBuffer := rMedianBuffer[jLoopJ];
            rMedianBuffer[jLoopJ] := rMedianBuffer[jLoopJ + 1];
            rMedianBuffer[jLoopJ + 1] := rSwapBuffer;
        END_IF;
    END_FOR;
END_FOR;

iHealthyCount_RCSV := 0;
FOR iLoopI := 1 TO 3 DO
    IF ABS(rRCSV_DeltaP_Transmitters[iLoopI] - rMedianBuffer[2]) > rThreshold_RCSV_DeltaP THEN
        rDiscrepancyTimer_RCSV[iLoopI] := rDiscrepancyTimer_RCSV[iLoopI] + 0.050;
        IF rDiscrepancyTimer_RCSV[iLoopI] > 1.500 THEN
            bHealthy_RCSV_Sensors[iLoopI] := FALSE;
        END_IF;
    ELSE
        rDiscrepancyTimer_RCSV[iLoopI] := 0.0;
        bHealthy_RCSV_Sensors[iLoopI] := TRUE;
    END_IF;
    IF bHealthy_RCSV_Sensors[iLoopI] THEN
        iHealthyCount_RCSV := iHealthyCount_RCSV + 1;
    END_IF;
END_FOR;

IF iHealthyCount_RCSV = 3 THEN
    rVoted_RCSV_DeltaP := rMedianBuffer[2];
    dwISA182_AlarmWord_2.10 := FALSE;
    dwISA182_AlarmWord_2.11 := FALSE;
ELSIF iHealthyCount_RCSV = 2 THEN
    rTempSum := 0.0;
    FOR iLoopI := 1 TO 3 DO
        IF bHealthy_RCSV_Sensors[iLoopI] THEN
            rTempSum := rTempSum + rRCSV_DeltaP_Transmitters[iLoopI];
        END_IF;
    END_FOR;
    rVoted_RCSV_DeltaP := rTempSum / 2.0;
    bSensorTMR_Degraded := TRUE;
    dwISA182_AlarmWord_2.10 := TRUE; (* RCSV Delta P TMR 1oo2 Degraded Mode Active *)
ELSIF iHealthyCount_RCSV = 1 THEN
    FOR iLoopI := 1 TO 3 DO
        IF bHealthy_RCSV_Sensors[iLoopI] THEN
            rVoted_RCSV_DeltaP := rRCSV_DeltaP_Transmitters[iLoopI];
        END_IF;
    END_FOR;
    bSensorTMR_Degraded := TRUE;
    dwISA182_AlarmWord_2.11 := TRUE; (* RCSV Delta P TMR 1oo1 Standby Depleted Warning *)
ELSE
    dwISA182_AlarmWord_1.15 := TRUE; (* All RCSV Delta P Sensors Failed - Emergency SIL-3 Trip *)
    iStateStep := 120;
END_IF;

(* -------------------------------------------------------------------------------------------------- *)
(* ENGINE 2B: SPENT CATALYST SLIDE VALVE DELTA P (2oo3 MEDIAN VOTING)                                 *)
(* -------------------------------------------------------------------------------------------------- *)
rMedianBuffer[1] := rSCSV_DeltaP_Transmitters[1];
rMedianBuffer[2] := rSCSV_DeltaP_Transmitters[2];
rMedianBuffer[3] := rSCSV_DeltaP_Transmitters[3];

FOR iLoopI := 1 TO 2 DO
    FOR jLoopJ := 1 TO 3 - iLoopI DO
        IF rMedianBuffer[jLoopJ] > rMedianBuffer[jLoopJ + 1] THEN
            rSwapBuffer := rMedianBuffer[jLoopJ];
            rMedianBuffer[jLoopJ] := rMedianBuffer[jLoopJ + 1];
            rMedianBuffer[jLoopJ + 1] := rSwapBuffer;
        END_IF;
    END_FOR;
END_FOR;

iHealthyCount_SCSV := 0;
FOR iLoopI := 1 TO 3 DO
    IF ABS(rSCSV_DeltaP_Transmitters[iLoopI] - rMedianBuffer[2]) > rThreshold_SCSV_DeltaP THEN
        rDiscrepancyTimer_SCSV[iLoopI] := rDiscrepancyTimer_SCSV[iLoopI] + 0.050;
        IF rDiscrepancyTimer_SCSV[iLoopI] > 1.500 THEN
            bHealthy_SCSV_Sensors[iLoopI] := FALSE;
        END_IF;
    ELSE
        rDiscrepancyTimer_SCSV[iLoopI] := 0.0;
        bHealthy_SCSV_Sensors[iLoopI] := TRUE;
    END_IF;
    IF bHealthy_SCSV_Sensors[iLoopI] THEN
        iHealthyCount_SCSV := iHealthyCount_SCSV + 1;
    END_IF;
END_FOR;

IF iHealthyCount_SCSV = 3 THEN
    rVoted_SCSV_DeltaP := rMedianBuffer[2];
    dwISA182_AlarmWord_2.12 := FALSE;
    dwISA182_AlarmWord_2.13 := FALSE;
ELSIF iHealthyCount_SCSV = 2 THEN
    rTempSum := 0.0;
    FOR iLoopI := 1 TO 3 DO
        IF bHealthy_SCSV_Sensors[iLoopI] THEN
            rTempSum := rTempSum + rSCSV_DeltaP_Transmitters[iLoopI];
        END_IF;
    END_FOR;
    rVoted_SCSV_DeltaP := rTempSum / 2.0;
    bSensorTMR_Degraded := TRUE;
    dwISA182_AlarmWord_2.12 := TRUE; (* SCSV Delta P TMR 1oo2 Degraded Mode Active *)
ELSIF iHealthyCount_SCSV = 1 THEN
    FOR iLoopI := 1 TO 3 DO
        IF bHealthy_SCSV_Sensors[iLoopI] THEN
            rVoted_SCSV_DeltaP := rSCSV_DeltaP_Transmitters[iLoopI];
        END_IF;
    END_FOR;
    bSensorTMR_Degraded := TRUE;
    dwISA182_AlarmWord_2.13 := TRUE; (* SCSV Delta P TMR 1oo1 Standby Depleted Warning *)
ELSE
    dwISA182_AlarmWord_1.16 := TRUE; (* All SCSV Delta P Sensors Failed - Emergency SIL-3 Trip *)
    iStateStep := 120;
END_IF;

(* -------------------------------------------------------------------------------------------------- *)
(* ENGINE 2C: REGENERATOR DENSE-BED THERMOCOUPLES (2oo3 MEDIAN VOTING)                                *)
(* -------------------------------------------------------------------------------------------------- *)
rMedianBuffer[1] := rRegenBedTemp_Transmitters[1];
rMedianBuffer[2] := rRegenBedTemp_Transmitters[2];
rMedianBuffer[3] := rRegenBedTemp_Transmitters[3];

FOR iLoopI := 1 TO 2 DO
    FOR jLoopJ := 1 TO 3 - iLoopI DO
        IF rMedianBuffer[jLoopJ] > rMedianBuffer[jLoopJ + 1] THEN
            rSwapBuffer := rMedianBuffer[jLoopJ];
            rMedianBuffer[jLoopJ] := rMedianBuffer[jLoopJ + 1];
            rMedianBuffer[jLoopJ + 1] := rSwapBuffer;
        END_IF;
    END_FOR;
END_FOR;

iHealthyCount_RegenTemp := 0;
FOR iLoopI := 1 TO 3 DO
    IF ABS(rRegenBedTemp_Transmitters[iLoopI] - rMedianBuffer[2]) > rThreshold_RegenBedTemp THEN
        rDiscrepancyTimer_RegenTemp[iLoopI] := rDiscrepancyTimer_RegenTemp[iLoopI] + 0.050;
        IF rDiscrepancyTimer_RegenTemp[iLoopI] > 2.000 THEN
            bHealthy_RegenTempSensors[iLoopI] := FALSE;
        END_IF;
    ELSE
        rDiscrepancyTimer_RegenTemp[iLoopI] := 0.0;
        bHealthy_RegenTempSensors[iLoopI] := TRUE;
    END_IF;
    IF bHealthy_RegenTempSensors[iLoopI] THEN
        iHealthyCount_RegenTemp := iHealthyCount_RegenTemp + 1;
    END_IF;
END_FOR;

IF iHealthyCount_RegenTemp = 3 THEN
    rVoted_RegenBedTemp := rMedianBuffer[2];
    dwISA182_AlarmWord_2.14 := FALSE;
    dwISA182_AlarmWord_2.15 := FALSE;
ELSIF iHealthyCount_RegenTemp = 2 THEN
    rTempSum := 0.0;
    FOR iLoopI := 1 TO 3 DO
        IF bHealthy_RegenTempSensors[iLoopI] THEN
            rTempSum := rTempSum + rRegenBedTemp_Transmitters[iLoopI];
        END_IF;
    END_FOR;
    rVoted_RegenBedTemp := rTempSum / 2.0;
    bSensorTMR_Degraded := TRUE;
    dwISA182_AlarmWord_2.14 := TRUE; (* Bed Temp TMR 1oo2 Degraded Mode Active *)
ELSIF iHealthyCount_RegenTemp = 1 THEN
    FOR iLoopI := 1 TO 3 DO
        IF bHealthy_RegenTempSensors[iLoopI] THEN
            rVoted_RegenBedTemp := rRegenBedTemp_Transmitters[iLoopI];
        END_IF;
    END_FOR;
    bSensorTMR_Degraded := TRUE;
    dwISA182_AlarmWord_2.15 := TRUE; (* Bed Temp TMR 1oo1 Standby Depleted Warning *)
ELSE
    dwISA182_AlarmWord_1.17 := TRUE; (* All Regen Bed Thermocouples Failed - Safe Abort *)
    iStateStep := 110;
END_IF;

(* -------------------------------------------------------------------------------------------------- *)
(* ENGINE 2D: REGENERATOR FLUE GAS OXYGEN ZIRCONIA ANALYZERS (2oo3 MEDIAN VOTING)                     *)
(* -------------------------------------------------------------------------------------------------- *)
rMedianBuffer[1] := rFlueGasO2_Transmitters[1];
rMedianBuffer[2] := rFlueGasO2_Transmitters[2];
rMedianBuffer[3] := rFlueGasO2_Transmitters[3];

FOR iLoopI := 1 TO 2 DO
    FOR jLoopJ := 1 TO 3 - iLoopI DO
        IF rMedianBuffer[jLoopJ] > rMedianBuffer[jLoopJ + 1] THEN
            rSwapBuffer := rMedianBuffer[jLoopJ];
            rMedianBuffer[jLoopJ] := rMedianBuffer[jLoopJ + 1];
            rMedianBuffer[jLoopJ + 1] := rSwapBuffer;
        END_IF;
    END_FOR;
END_FOR;

iHealthyCount_FlueGasO2 := 0;
FOR iLoopI := 1 TO 3 DO
    IF ABS(rFlueGasO2_Transmitters[iLoopI] - rMedianBuffer[2]) > rThreshold_FlueGasO2 THEN
        rDiscrepancyTimer_FlueGasO2[iLoopI] := rDiscrepancyTimer_FlueGasO2[iLoopI] + 0.050;
        IF rDiscrepancyTimer_FlueGasO2[iLoopI] > 2.500 THEN
            bHealthy_FlueGasO2Sensors[iLoopI] := FALSE;
        END_IF;
    ELSE
        rDiscrepancyTimer_FlueGasO2[iLoopI] := 0.0;
        bHealthy_FlueGasO2Sensors[iLoopI] := TRUE;
    END_IF;
    IF bHealthy_FlueGasO2Sensors[iLoopI] THEN
        iHealthyCount_FlueGasO2 := iHealthyCount_FlueGasO2 + 1;
    END_IF;
END_FOR;

IF iHealthyCount_FlueGasO2 = 3 THEN
    rVoted_FlueGasO2 := rMedianBuffer[2];
    dwISA182_AlarmWord_2.16 := FALSE;
    dwISA182_AlarmWord_2.17 := FALSE;
ELSIF iHealthyCount_FlueGasO2 = 2 THEN
    rTempSum := 0.0;
    FOR iLoopI := 1 TO 3 DO
        IF bHealthy_FlueGasO2Sensors[iLoopI] THEN
            rTempSum := rTempSum + rFlueGasO2_Transmitters[iLoopI];
        END_IF;
    END_FOR;
    rVoted_FlueGasO2 := rTempSum / 2.0;
    bSensorTMR_Degraded := TRUE;
    dwISA182_AlarmWord_2.16 := TRUE; (* Flue Gas O2 TMR 1oo2 Degraded Mode Active *)
ELSIF iHealthyCount_FlueGasO2 = 1 THEN
    FOR iLoopI := 1 TO 3 DO
        IF bHealthy_FlueGasO2Sensors[iLoopI] THEN
            rVoted_FlueGasO2 := rFlueGasO2_Transmitters[iLoopI];
        END_IF;
    END_FOR;
    bSensorTMR_Degraded := TRUE;
    dwISA182_AlarmWord_2.17 := TRUE; (* Flue Gas O2 TMR 1oo1 Standby Depleted Warning *)
ELSE
    dwISA182_AlarmWord_1.18 := TRUE; (* All Flue Gas O2 Analyzers Failed *)
    iStateStep := 100;
END_IF;
"""
    parts.append(phase2)
    
    # -------------------------------------------------------------------------
    # PART 8: PHASE 3 - PROCESS ESTIMATORS & PHENOMENOLOGICAL KINETICS
    # -------------------------------------------------------------------------
    phase3 = """(*
========================================================================================================================
  PHASE 3: CYBER-PHYSICAL PROCESS ESTIMATORS & PHENOMENOLOGICAL KINETICS
========================================================================================================================
*)
(* 1. Hydrodynamic Catalyst Circulation Rate from Slide Valve Orifice Law:                       *)
(*    W_cat = C_d * A_valve * SQRT(2 * rho_aerated * Delta_P * 100000.0)                         *)
IF (rVoted_RCSV_DeltaP > 0.05) AND (rRCSV_PositionSetpointCmd > 5.0) THEN
    rCatalystFlow_kg_s := rValveCd_RCSV * (rValvePortAreaMax * (rRCSV_PositionSetpointCmd / 100.0))
                          * SQRT(2.0 * rCatDensity_Aerated * (rVoted_RCSV_DeltaP * 100000.0));
    rEstimatedCatCirculationRate := (rCatalystFlow_kg_s * 60.0) / 1000.0; (* Converted to [t/min] *)
ELSE
    rEstimatedCatCirculationRate := 0.0;
END_IF;

(* 2. Catalyst-to-Oil Mass Ratio (CTO):                                                          *)
(*    CTO = (W_cat [t/min] * 60.0) / (W_feed [t/h])                                             *)
IF rFeedMassFlowRate_Actual > 15.0 THEN
    rEstimatedCatToOilRatio := (rEstimatedCatCirculationRate * 60.0) / rFeedMassFlowRate_Actual;
ELSE
    rEstimatedCatToOilRatio := 0.0;
END_IF;

(* 3. Arrhenius Heterogeneous Coke Combustion Kinetics:                                          *)
(*    r_coke = A_c * EXP(-E_a / (R * (T_bed + 273.15))) * P_O2 * C_coke                          *)
rCokeCombustionKineticK := rArrheniusA_Coke * EXP(-rActivationEnergy_Coke / (rGasConstant_R * (rVoted_RegenBedTemp + 273.15)));
IF (rVoted_FlueGasO2 > 0.10) AND (rRegenCatalystInventory_Tons > 50.0) THEN
    rEstimatedCokeBurnRate := rCokeCombustionKineticK * ((rVoted_FlueGasO2 / 100.0) * (rAirBlowerDischargePress + 1.013))
                              * (vecStateEstimate[3] / 100.0) * (rRegenCatalystInventory_Tons * 1000.0) * 0.125;
    IF rEstimatedCokeBurnRate < 500.0 THEN
        rEstimatedCokeBurnRate := 500.0;
    ELSIF rEstimatedCokeBurnRate > 25000.0 THEN
        rEstimatedCokeBurnRate := 25000.0;
    END_IF;
ELSE
    rEstimatedCokeBurnRate := 0.0;
END_IF;

(* 4. Cyclone Afterburning Temperature Differential (Delta T):                                  *)
(*    Delta T = T_cyclone_plenum - T_dense_bed                                                   *)
rCalculatedDeltaT := rRegenCyclonePlenumTemp - rVoted_RegenBedTemp;
rCycloneDeltaT_Actual := rCalculatedDeltaT;

IF rCalculatedDeltaT > rMaxCycloneDeltaT_Trip THEN
    bAfterburningDetected := TRUE;
    dwISA182_AlarmWord_1.3 := TRUE; (* Cyclone Afterburning HH Trip Activated *)
    IF (iStateStep >= 40) AND (iStateStep <= 80) THEN
        iStateStep := 110; (* Emergency Snuffing / Feed Abort *)
    END_IF;
ELSIF rCalculatedDeltaT > rMaxCycloneDeltaT_Warn THEN
    bAfterburningDetected := TRUE;
    dwISA182_AlarmWord_2.2 := TRUE; (* Cyclone Afterburning Warning (Delta T > 25 C) *)
ELSE
    bAfterburningDetected := FALSE;
    dwISA182_AlarmWord_2.2 := FALSE;
END_IF;

(* 5. Main Combustion Air Blower Surge Margin Calculation:                                      *)
(*    Surge Line Model: Flow_surge = 12000.0 * SQRT(P_discharge)                                 *)
rSurgeLimitFlow := 14500.0 * SQRT(MAX(1.0, rAirBlowerDischargePress));
IF rMainAirBlowerFlow_Actual > 1000.0 THEN
    rBlowerSurgeMarginPct := ((rMainAirBlowerFlow_Actual - rSurgeLimitFlow) / rMainAirBlowerFlow_Actual) * 100.0;
ELSE
    rBlowerSurgeMarginPct := 0.0;
END_IF;

IF rBlowerSurgeMarginPct < 8.0 THEN
    dwISA182_AlarmWord_1.5 := TRUE; (* Blower Surge Critical Trip Activated *)
    IF iStateStep >= 30 THEN
        iStateStep := 110;
    END_IF;
ELSIF rBlowerSurgeMarginPct < 15.0 THEN
    dwISA182_AlarmWord_2.7 := TRUE; (* Blower Near Surge Margin Warning *)
ELSE
    dwISA182_AlarmWord_2.7 := FALSE;
END_IF;

(* Update Process Output Observables *)
rEstimatedRiserOutletTemp := vecStateEstimate[11];
rEstimatedRegenBedTemp := vecStateEstimate[1];
rEstimatedCokeOnRegenCat := vecStateEstimate[3];
"""
    parts.append(phase3)
    
    # -------------------------------------------------------------------------
    # PART 9: PHASE 4 - 16-STATE DISCRETE-TIME STATE OBSERVER
    # -------------------------------------------------------------------------
    phase4 = """(*
========================================================================================================================
  PHASE 4: 16-STATE DISCRETE-TIME STATE-SPACE OBSERVER (KALMAN/LUENBERGER)
========================================================================================================================
*)
(* Assemble Measured Output Vector y(k) *)
vecMeasuredOutputs[1] := rVoted_RegenBedTemp;
vecMeasuredOutputs[2] := rRiserOutletTemp_Actual;
vecMeasuredOutputs[3] := rVoted_RCSV_DeltaP;
vecMeasuredOutputs[4] := rVoted_SCSV_DeltaP;
vecMeasuredOutputs[5] := rVoted_FlueGasO2;
vecMeasuredOutputs[6] := rCycloneDeltaT_Actual;
vecMeasuredOutputs[7] := rRegenBedDifferentialPress;
vecMeasuredOutputs[8] := vecStateEstimate[3]; (* Carbon on regen cat observer fallback *)

(* 1. Compute Innovation Residual Vector: e(k) = y(k) - (matC * x(k) + matD * u(k)) *)
FOR iLoopI := 1 TO 8 DO
    rTempSum := 0.0;
    FOR jLoopJ := 1 TO 16 DO
        rTempSum := rTempSum + (matC[iLoopI, jLoopJ] * vecStateEstimate[jLoopJ]);
    END_FOR;
    FOR jLoopJ := 1 TO 8 DO
        rTempSum := rTempSum + (matD[iLoopI, jLoopJ] * vecControlCurrent[jLoopJ]);
    END_FOR;
    vecInnovationResidual[iLoopI] := vecMeasuredOutputs[iLoopI] - rTempSum;
END_FOR;

(* 2. State Propagation: x_pred(k+1) = matA * x(k) + matB * delta_u(k) *)
FOR iLoopI := 1 TO 16 DO
    rTempSum := 0.0;
    FOR jLoopJ := 1 TO 16 DO
        rTempSum := rTempSum + (matA[iLoopI, jLoopJ] * vecStateEstimate[jLoopJ]);
    END_FOR;
    FOR jLoopJ := 1 TO 8 DO
        rTempSum := rTempSum + (matB[iLoopI, jLoopJ] * (vecControlCurrent[jLoopJ] - vecControlPrevious[jLoopJ]));
    END_FOR;
    vecStatePredicted[iLoopI] := rTempSum;
END_FOR;

(* 3. State Correction Update: x_est(k+1) = x_pred(k+1) + matL * e(k) *)
FOR iLoopI := 1 TO 16 DO
    rTempSum := 0.0;
    FOR jLoopJ := 1 TO 8 DO
        rTempSum := rTempSum + (matL[iLoopI, jLoopJ] * vecInnovationResidual[jLoopJ]);
    END_FOR;
    vecStateEstimate[iLoopI] := vecStatePredicted[iLoopI] + rTempSum;
END_FOR;

(* Physical Plausibility Sanity Bounds on Estimated States *)
IF vecStateEstimate[1] < 450.0 THEN vecStateEstimate[1] := 450.0; ELSIF vecStateEstimate[1] > 850.0 THEN vecStateEstimate[1] := 850.0; END_IF;
IF vecStateEstimate[3] < 0.01 THEN vecStateEstimate[3] := 0.01; ELSIF vecStateEstimate[3] > 2.50 THEN vecStateEstimate[3] := 2.50; END_IF;
IF vecStateEstimate[4] < 0.00 THEN vecStateEstimate[4] := 0.00; ELSIF vecStateEstimate[4] > 12.00 THEN vecStateEstimate[4] := 12.00; END_IF;
IF vecStateEstimate[8] < 0.00 THEN vecStateEstimate[8] := 0.00; ELSIF vecStateEstimate[8] > 2.50 THEN vecStateEstimate[8] := 2.50; END_IF;
IF vecStateEstimate[9] < 0.00 THEN vecStateEstimate[9] := 0.00; ELSIF vecStateEstimate[9] > 2.50 THEN vecStateEstimate[9] := 2.50; END_IF;
IF vecStateEstimate[11] < 350.0 THEN vecStateEstimate[11] := 350.0; ELSIF vecStateEstimate[11] > 650.0 THEN vecStateEstimate[11] := 650.0; END_IF;
"""
    parts.append(phase4)
    
    # -------------------------------------------------------------------------
    # PART 10: PHASE 5 - RECEDING-HORIZON MPC OPTIMIZER WITH BARRIER PENALTIES
    # -------------------------------------------------------------------------
    phase5 = """(*
========================================================================================================================
  PHASE 5: RECEDING-HORIZON MULTIVARIABLE MODEL PREDICTIVE CONTROL (MPC)
  PROJECTED GRADIENT DESCENT (PGD) WITH NONLINEAR SOFT BARRIER CONSTRAINTS
========================================================================================================================
*)
IF ((iStateStep = 60) OR (iStateStep = 70)) AND NOT bManualModePermissive THEN
    bMPC_OptimizationActive := TRUE;

    (* Target Output References *)
    vecOutputReference[1] := rTargetRegenBedTemp;
    vecOutputReference[2] := rTargetRiserOutletTemp;
    vecOutputReference[3] := rTargetSlideValveDeltaP;
    vecOutputReference[4] := rTargetSlideValveDeltaP;
    vecOutputReference[5] := 1.75; (* Target Flue Gas O2 [%] *)
    vecOutputReference[6] := 8.0;  (* Target cyclone Delta T [deg C] *)
    vecOutputReference[7] := 62.0; (* Target bed inventory Delta P [kPa] *)
    vecOutputReference[8] := 0.08; (* Target CRC [wt%] *)

    (* Initialize Control Increment Candidate *)
    FOR iLoopI := 1 TO 8 DO
        vecDeltaU[iLoopI] := 0.0;
    END_FOR;

    (* Evaluate Nonlinear Soft-Barrier Penalty Gradients *)
    (* 1. RCSV Reverse Flow Barrier Gradient: penalize Delta P < 0.40 bar *)
    IF vecStateEstimate[8] < 0.40 THEN
        rBarrierGradient_RCSV := rReverseFlowPenaltyWeight * (vecStateEstimate[8] - 0.40);
    ELSE
        rBarrierGradient_RCSV := 0.0;
    END_IF;

    (* 2. SCSV Reverse Flow Barrier Gradient: penalize Delta P < 0.40 bar *)
    IF vecStateEstimate[9] < 0.40 THEN
        rBarrierGradient_SCSV := rReverseFlowPenaltyWeight * (vecStateEstimate[9] - 0.40);
    ELSE
        rBarrierGradient_SCSV := 0.0;
    END_IF;

    (* 3. Cyclone Afterburning Thermal Gradient: penalize Delta T > 22.0 deg C *)
    IF (vecStateEstimate[2] - vecStateEstimate[1]) > 22.0 THEN
        rBarrierGradient_Afterburn := rAfterburningPenaltyWeight * ((vecStateEstimate[2] - vecStateEstimate[1]) - 22.0);
    ELSE
        rBarrierGradient_Afterburn := 0.0;
    END_IF;

    (* 4. Riser Outlet Temperature Excursion Gradient: penalize |ROT - 535.0| > 1.2 deg C *)
    IF ABS(vecStateEstimate[11] - rTargetRiserOutletTemp) > 1.20 THEN
        rBarrierGradient_ROT := rRotExcursionPenaltyWeight * (vecStateEstimate[11] - rTargetRiserOutletTemp);
    ELSE
        rBarrierGradient_ROT := 0.0;
    END_IF;

    (* 5. Main Air Blower Surge Margin Gradient: penalize margin < 18.0 % *)
    IF rBlowerSurgeMarginPct < 18.0 THEN
        rBarrierGradient_Surge := rBlowerSurgePenaltyWeight * (18.0 - rBlowerSurgeMarginPct);
    ELSE
        rBarrierGradient_Surge := 0.0;
    END_IF;

    (* Projected Gradient Descent Optimization Loop (Unrolled across iMPC_MaxIterations) *)
    FOR kIterK := 1 TO iMPC_MaxIterations DO
        (* Gradient with respect to u1 (Regenerated Catalyst Slide Valve Position) *)
        rGradientVector[1] := (vecOutputWeight_Q[2] * (vecMeasuredOutputs[2] - vecOutputReference[2]) * 0.0520)
                            + (vecOutputWeight_Q[3] * (vecMeasuredOutputs[3] - vecOutputReference[3]) * (-0.0240))
                            + (vecInputRateWeight_R[1] * vecDeltaU[1])
                            + (rBarrierGradient_ROT * 0.0520)
                            - (rBarrierGradient_RCSV * 0.0240);

        (* Gradient with respect to u2 (Spent Catalyst Slide Valve Position) *)
        rGradientVector[2] := (vecOutputWeight_Q[1] * (vecMeasuredOutputs[1] - vecOutputReference[1]) * 0.0185)
                            + (vecOutputWeight_Q[4] * (vecMeasuredOutputs[4] - vecOutputReference[4]) * (-0.0220))
                            + (vecInputRateWeight_R[2] * vecDeltaU[2])
                            - (rBarrierGradient_SCSV * 0.0220);

        (* Gradient with respect to u3 (Combustion Air Blower Guide Vanes) *)
        rGradientVector[3] := (vecOutputWeight_Q[1] * (vecMeasuredOutputs[1] - vecOutputReference[1]) * 0.0650)
                            + (vecOutputWeight_Q[5] * (vecMeasuredOutputs[5] - vecOutputReference[5]) * 0.0850)
                            + (vecInputRateWeight_R[3] * vecDeltaU[3])
                            + (rBarrierGradient_Afterburn * 0.0250)
                            - (rBarrierGradient_Surge * 0.0480);

        (* Gradient with respect to u4 (Feed Preheat Furnace Duty) *)
        rGradientVector[4] := (vecOutputWeight_Q[2] * (vecMeasuredOutputs[2] - vecOutputReference[2]) * 0.0280)
                            + (vecInputRateWeight_R[4] * vecDeltaU[4])
                            + (rBarrierGradient_ROT * 0.0280);

        (* Gradient with respect to u5 (Feed Flow Rate - Feedforward only, zero direct gradient) *)
        rGradientVector[5] := 0.0;

        (* Gradient with respect to u6 (Dispersion Steam Trim Valve) *)
        rGradientVector[6] := (vecOutputWeight_Q[2] * (vecMeasuredOutputs[2] - vecOutputReference[2]) * (-0.0065))
                            + (vecInputRateWeight_R[6] * vecDeltaU[6]);

        (* Gradient with respect to u7 (Stripper Superheated Steam Valve) *)
        rGradientVector[7] := (vecOutputWeight_Q[6] * (vecMeasuredOutputs[6] - vecOutputReference[6]) * (-0.0150))
                            + (vecInputRateWeight_R[7] * vecDeltaU[7])
                            - (rBarrierGradient_Afterburn * 0.0150);

        (* Gradient with respect to u8 (Feed CCR Disturbance - feedforward only) *)
        rGradientVector[8] := 0.0;

        (* Gradient Descent Step & Slew Rate Projection *)
        FOR iLoopI := 1 TO 8 DO
            vecDeltaU[iLoopI] := vecDeltaU[iLoopI] - (rPGD_StepSize * rGradientVector[iLoopI]);
            IF vecDeltaU[iLoopI] > vecMaxSlewRatePerScan[iLoopI] THEN
                vecDeltaU[iLoopI] := vecMaxSlewRatePerScan[iLoopI];
            ELSIF vecDeltaU[iLoopI] < -vecMaxSlewRatePerScan[iLoopI] THEN
                vecDeltaU[iLoopI] := -vecMaxSlewRatePerScan[iLoopI];
            END_IF;
        END_FOR;
    END_FOR;

    (* Apply Increments to Modulating Actuator Commands subject to Box Limits *)
    FOR iLoopI := 1 TO 8 DO
        rCandidateU := vecControlPrevious[iLoopI] + vecDeltaU[iLoopI];
        IF rCandidateU > vecControlMaxLimits[iLoopI] THEN
            vecControlCurrent[iLoopI] := vecControlMaxLimits[iLoopI];
        ELSIF rCandidateU < vecControlMinLimits[iLoopI] THEN
            vecControlCurrent[iLoopI] := vecControlMinLimits[iLoopI];
        ELSE
            vecControlCurrent[iLoopI] := rCandidateU;
        END_IF;
    END_FOR;

    (* Bind Optimized Outputs to Actuator Setpoint Registers *)
    rRCSV_PositionSetpointCmd := vecControlCurrent[1];
    rSCSV_PositionSetpointCmd := vecControlCurrent[2];
    rAirBlowerGuideVanesCmd := vecControlCurrent[3];
    rPreheatFurnaceFuelDutyCmd := vecControlCurrent[4];
    rDispersionSteamValveCmd := vecControlCurrent[6];
    rStrippingSteamValveCmd := vecControlCurrent[7];

    (* Store previous control vector for next scan cycle *)
    FOR iLoopI := 1 TO 8 DO
        vecControlPrevious[iLoopI] := vecControlCurrent[iLoopI];
    END_FOR;
ELSE
    bMPC_OptimizationActive := FALSE;
END_IF;
"""
    parts.append(phase5)
    
    # -------------------------------------------------------------------------
    # PART 11: PHASE 6 - 12-STAGE OPERATIONAL FINITE STATE MACHINE (FSM)
    # -------------------------------------------------------------------------
    phase6 = """(*
========================================================================================================================
  PHASE 6: 12-STAGE OPERATIONAL FINITE STATE MACHINE (FSM)
========================================================================================================================
*)
tStateTimer(IN := (iStateStep = iPreviousState), PT := T#86400S);
iPreviousState := iStateStep;

CASE iStateStep OF
    0: (* === STATE 0: SYSTEM IDLE & PRE-FLIGHT DIAGNOSTICS === *)
        bFCCU_SystemReady := FALSE;
        bFeedInflowPermissive := FALSE;
        bMPC_OptimizationActive := FALSE;
        bExpanderCoupled := FALSE;
        bSlideValveReverseFlowWarning := FALSE;
        bSlideValveFastTripActive := FALSE;
        bEmergencySnuffingActive := FALSE;

        rRCSV_PositionSetpointCmd := 0.0;
        rSCSV_PositionSetpointCmd := 0.0;
        rAirBlowerGuideVanesCmd := 15.0; (* Minimum idle purge *)
        rPreheatFurnaceFuelDutyCmd := 0.0;
        rStrippingSteamValveCmd := 10.0;
        rDispersionSteamValveCmd := 0.0;
        rSnuffingSteamDumpValveCmd := 0.0;

        IF bEnableMasterFCCU AND bEmergencyTripCircuit AND (dwISA182_AlarmWord_1 = 16#00000000) THEN
            iStateStep := 10; (* Transition to Regenerator Air Purge & Refractory Dryout *)
        END_IF;

    10: (* === STATE 10: REGENERATOR AIR PURGE & REFRACTORY DRYOUT === *)
        bFCCU_SystemReady := FALSE;
        bFeedInflowPermissive := FALSE;
        rAirBlowerGuideVanesCmd := 35.0; (* Moderate air blower purge velocity *)
        rStrippingSteamValveCmd := 20.0;
        rPreheatFurnaceFuelDutyCmd := 0.0;
        rSnuffingSteamDumpValveCmd := 0.0;

        tAirPurgeTimer(IN := TRUE, PT := T#1800S); (* 30 minutes soak time *)
        IF tAirPurgeTimer.Q AND (rMainAirBlowerFlow_Actual > 32000.0) AND (rAirBlowerDischargePress > 1.85) THEN
            tAirPurgeTimer(IN := FALSE);
            iStateStep := 20; (* Advance to Torching Oil Ignition & Thermal Ramp *)
        END_IF;

    20: (* === STATE 20: TORCHING OIL IGNITION & THERMAL RAMP === *)
        bFCCU_SystemReady := FALSE;
        bFeedInflowPermissive := FALSE;
        rAirBlowerGuideVanesCmd := 45.0;
        rStrippingSteamValveCmd := 25.0;
        rPreheatFurnaceFuelDutyCmd := 25.0; (* Initial furnace pilot light-off *)

        tTorchingOilTimer(IN := TRUE, PT := T#3600S); (* Controlled thermal ramp *)
        (* Controlled dense-bed heating ramp: target 650+ deg C before catalyst circulation *)
        IF (rVoted_RegenBedTemp >= 640.0) AND (rVoted_FlueGasO2 > 2.0) THEN
            tTorchingOilTimer(IN := FALSE);
            iStateStep := 30; (* Advance to Catalyst Circulation Balancing *)
        END_IF;

    30: (* === STATE 30: CATALYST CIRCULATION HYDRODYNAMIC BALANCING === *)
        bFCCU_SystemReady := FALSE;
        bFeedInflowPermissive := FALSE;
        rAirBlowerGuideVanesCmd := 55.0;
        rStrippingSteamValveCmd := 45.0; (* Establish riser and stripper fluidization *)
        rDispersionSteamValveCmd := 35.0;

        (* Ramp slide valves slowly to establish positive catalyst circulation head *)
        IF rRCSV_PositionSetpointCmd < 28.0 THEN
            rRCSV_PositionSetpointCmd := rRCSV_PositionSetpointCmd + 0.05;
        END_IF;
        IF rSCSV_PositionSetpointCmd < 30.0 THEN
            rSCSV_PositionSetpointCmd := rSCSV_PositionSetpointCmd + 0.05;
        END_IF;

        tCatCirculationBalancingTimer(IN := TRUE, PT := T#600S);
        IF tCatCirculationBalancingTimer.Q AND (rVoted_RCSV_DeltaP >= 0.45) AND (rVoted_SCSV_DeltaP >= 0.45)
           AND (rEstimatedCatCirculationRate > 15.0) THEN
            tCatCirculationBalancingTimer(IN := FALSE);
            iStateStep := 40; (* Advance to Heavy Gas Oil Feed Inflow Cut-In *)
        END_IF;

    40: (* === STATE 40: HEAVY GAS OIL FEED INFLOW CUT-IN === *)
        bFCCU_SystemReady := TRUE;
        bFeedInflowPermissive := TRUE; (* Open main feed emergency shut-off valves *)
        rDispersionSteamValveCmd := 55.0;
        rStrippingSteamValveCmd := 50.0;
        rPreheatFurnaceFuelDutyCmd := 45.0;

        tFeedCutInRampTimer(IN := TRUE, PT := T#1200S);
        (* Verify feed cut-in without dropping slide valve Delta P *)
        IF (rFeedMassFlowRate_Actual > 80.0) AND (rRiserOutletTemp_Actual > 505.0)
           AND (rVoted_RCSV_DeltaP >= 0.42) AND (rVoted_SCSV_DeltaP >= 0.42) THEN
            tFeedCutInRampTimer(IN := FALSE);
            iStateStep := 50; (* Advance to Riser Temperature Closed-Loop Stabilization *)
        END_IF;

    50: (* === STATE 50: RISER TEMPERATURE CLOSED-LOOP STABILIZATION === *)
        bFCCU_SystemReady := TRUE;
        bFeedInflowPermissive := TRUE;
        rDispersionSteamValveCmd := 65.0;
        rStrippingSteamValveCmd := 55.0;

        (* Classical feedback trim on RCSV position to drive ROT toward 535 C *)
        IF rRiserOutletTemp_Actual < (rTargetRiserOutletTemp - 1.0) THEN
            IF rRCSV_PositionSetpointCmd < 65.0 THEN
                rRCSV_PositionSetpointCmd := rRCSV_PositionSetpointCmd + 0.04;
            END_IF;
        ELSIF rRiserOutletTemp_Actual > (rTargetRiserOutletTemp + 1.0) THEN
            IF rRCSV_PositionSetpointCmd > 25.0 THEN
                rRCSV_PositionSetpointCmd := rRCSV_PositionSetpointCmd - 0.04;
            END_IF;
        END_IF;

        (* Spent cat slide valve tracks stripper bed inventory *)
        IF vecStateEstimate[13] > 60.0 THEN
            IF rSCSV_PositionSetpointCmd < 70.0 THEN
                rSCSV_PositionSetpointCmd := rSCSV_PositionSetpointCmd + 0.04;
            END_IF;
        ELSIF vecStateEstimate[13] < 45.0 THEN
            IF rSCSV_PositionSetpointCmd > 25.0 THEN
                rSCSV_PositionSetpointCmd := rSCSV_PositionSetpointCmd - 0.04;
            END_IF;
        END_IF;

        IF (ABS(rRiserOutletTemp_Actual - rTargetRiserOutletTemp) < 2.5) AND (tStateTimer.ET > T#300S) THEN
            iStateStep := 60; (* Engage Steady-State MPC Cracking Optimization *)
        END_IF;

    60: (* === STATE 60: STEADY-STATE MPC CRACKING OPTIMIZATION === *)
        bFCCU_SystemReady := TRUE;
        bFeedInflowPermissive := TRUE;
        bMPC_OptimizationActive := TRUE;

        (* MPC handles all modulating setpoints: RCSV, SCSV, Air Blower, Furnace, Dispersion, Stripping *)
        IF bExpanderCoupledPermissive AND (rExpanderInletFlueGasPress > 2.20) AND NOT bExpanderCoupled THEN
            iStateStep := 80; (* Transition to Expander Coupling *)
        ELSIF vecStateEstimate[14] > 2.20 THEN
            iStateStep := 70; (* Transition to Stripping Steam Optimization *)
        END_IF;

    70: (* === STATE 70: STEAM STRIPPING STEAM RATIO ADJUSTMENT === *)
        bFCCU_SystemReady := TRUE;
        bFeedInflowPermissive := TRUE;
        bMPC_OptimizationActive := TRUE;

        (* Adaptive trim on stripping steam to suppress volatile hydrocarbon carryover *)
        IF vecStateEstimate[14] > 1.80 THEN
            IF rStrippingSteamValveCmd < 85.0 THEN
                rStrippingSteamValveCmd := rStrippingSteamValveCmd + 0.10;
            END_IF;
        ELSIF vecStateEstimate[14] < 0.95 THEN
            IF rStrippingSteamValveCmd > 35.0 THEN
                rStrippingSteamValveCmd := rStrippingSteamValveCmd - 0.05;
            END_IF;
        END_IF;

        IF (vecStateEstimate[14] <= 1.25) AND (tStateTimer.ET > T#180S) THEN
            iStateStep := 60; (* Return to Standard MPC Optimization *)
        END_IF;

    80: (* === STATE 80: FLUE GAS POWER RECOVERY EXPANDER COUPLING === *)
        bFCCU_SystemReady := TRUE;
        bFeedInflowPermissive := TRUE;
        bMPC_OptimizationActive := TRUE;

        IF bExpanderCoupledPermissive AND (rExpanderInletFlueGasPress >= 2.15) THEN
            bExpanderCoupled := TRUE;
            dwISA182_AlarmWord_2.23 := FALSE;
        ELSE
            bExpanderCoupled := FALSE;
            dwISA182_AlarmWord_2.23 := TRUE; (* Flue Gas Expander Delta P Low Warning *)
        END_IF;

        IF tStateTimer.ET > T#120S THEN
            iStateStep := 60; (* Return to Standard MPC Optimization *)
        END_IF;

    90: (* === STATE 90: PARTIAL FEED SHEDDING MANEUVER === *)
        bFCCU_SystemReady := TRUE;
        bFeedInflowPermissive := TRUE;
        bMPC_OptimizationActive := FALSE; (* Disengage MPC during rapid rate shedding *)

        (* Slew down feed and trim air blower to maintain Delta P stability *)
        IF rFeedMassFlowRate_Actual > 120.0 THEN
            rRCSV_PositionSetpointCmd := rRCSV_PositionSetpointCmd - 0.25;
            rSCSV_PositionSetpointCmd := rSCSV_PositionSetpointCmd - 0.25;
            rAirBlowerGuideVanesCmd := rAirBlowerGuideVanesCmd - 0.15;
            rPreheatFurnaceFuelDutyCmd := rPreheatFurnaceFuelDutyCmd - 0.10;
        END_IF;

        IF (rVoted_RCSV_DeltaP >= 0.45) AND (rVoted_SCSV_DeltaP >= 0.45) AND (tStateTimer.ET > T#240S) THEN
            iStateStep := 50; (* Restabilize at lower feed rate *)
        END_IF;

    100: (* === STATE 100: CATALYST PURGE & INACTIVE CIRCULATION === *)
        bFCCU_SystemReady := FALSE;
        bFeedInflowPermissive := FALSE; (* Fast cut heavy gas oil feed *)
        bMPC_OptimizationActive := FALSE;
        bExpanderCoupled := FALSE;

        rPreheatFurnaceFuelDutyCmd := 0.0;
        rDispersionSteamValveCmd := 40.0; (* Maintain riser sweep steam *)
        rStrippingSteamValveCmd := 40.0;  (* Purge disengager stripper *)
        rAirBlowerGuideVanesCmd := 45.0;

        (* Maintain low gentle catalyst circulation to preserve thermal bed *)
        rRCSV_PositionSetpointCmd := 22.0;
        rSCSV_PositionSetpointCmd := 24.0;

        IF NOT bEnableMasterFCCU AND (tStateTimer.ET > T#600S) THEN
            iStateStep := 0; (* Cold Standby *)
        END_IF;

    110: (* === STATE 110: EMERGENCY NITROGEN DE-INVENTORY SNUFFING === *)
        bFCCU_SystemReady := FALSE;
        bFeedInflowPermissive := FALSE;
        bMPC_OptimizationActive := FALSE;
        bExpanderCoupled := FALSE;
        bEmergencySnuffingActive := TRUE;

        rSnuffingSteamDumpValveCmd := 100.0; (* Full blast steam snuffing to quench afterburning *)
        rDispersionSteamValveCmd := 80.0;   (* Sweep riser with steam *)
        rStrippingSteamValveCmd := 80.0;
        rPreheatFurnaceFuelDutyCmd := 0.0;
        rAirBlowerGuideVanesCmd := 25.0;     (* Reduce combustion air *)

        (* Lower slide valve openings to prevent violent bed transfer *)
        rRCSV_PositionSetpointCmd := 10.0;
        rSCSV_PositionSetpointCmd := 10.0;

        tSnuffingSteamTimer(IN := TRUE, PT := T#300S);
        IF tSnuffingSteamTimer.Q THEN
            tSnuffingSteamTimer(IN := FALSE);
            bEmergencySnuffingActive := FALSE;
            rSnuffingSteamDumpValveCmd := 0.0;
            iStateStep := 120; (* Transition to SIL-3 Fast Close *)
        END_IF;

    120: (* === STATE 120: EMERGENCY SLIDE VALVE SIL-3 FAST CLOSE === *)
        bFCCU_SystemReady := FALSE;
        bFeedInflowPermissive := FALSE;
        bMPC_OptimizationActive := FALSE;
        bExpanderCoupled := FALSE;
        bSlideValveFastTripActive := TRUE;

        (* SIL-3 Fast Hydraulic Dump of Both Slide Valves (< 850 ms) *)
        rRCSV_PositionSetpointCmd := 0.0;
        rSCSV_PositionSetpointCmd := 0.0;
        rPreheatFurnaceFuelDutyCmd := 0.0;
        rAirBlowerGuideVanesCmd := 20.0;
        rDispersionSteamValveCmd := 25.0;
        rStrippingSteamValveCmd := 25.0;

        dwISA182_AlarmWord_1.0 := TRUE; (* Lockout in Safe State *)
END_CASE;

iActiveFSMStateIndex := iStateStep;
"""
    parts.append(phase6)
    
    # -------------------------------------------------------------------------
    # PART 12: PHASE 7 - ISA-18.2 ALARMS & BIT-PACKED STATUS WORDS
    # -------------------------------------------------------------------------
    phase7 = """(*
========================================================================================================================
  PHASE 7: ISA-18.2 MULTI-TIERED ALARM MATRIX & STATUS WORD BIT-PACKING
========================================================================================================================
*)
(* -------------------------------------------------------------------------------------------------- *)
(* ISA-18.2 PRIMARY SAFETY & CRITICAL TRIP ALARMS (dwISA182_AlarmWord_1)                              *)
(* -------------------------------------------------------------------------------------------------- *)
(* Bit 1: RCSV Reverse Flow Critical Delta P Low-Low Trip (< 0.25 bar) *)
IF (rVoted_RCSV_DeltaP < rMinSlideValveDeltaP_Trip) AND (iStateStep >= 30) AND (iStateStep <= 80) THEN
    dwISA182_AlarmWord_1.1 := TRUE;
    iStateStep := 120; (* SIL-3 Fast Close *)
END_IF;

(* Bit 2: SCSV Reverse Flow Critical Delta P Low-Low Trip (< 0.25 bar) *)
IF (rVoted_SCSV_DeltaP < rMinSlideValveDeltaP_Trip) AND (iStateStep >= 30) AND (iStateStep <= 80) THEN
    dwISA182_AlarmWord_1.2 := TRUE;
    iStateStep := 120;
END_IF;

(* Bit 4: Regenerator Bed Temperature High-High Trip (> 750 deg C) *)
IF rVoted_RegenBedTemp > rMaxAllowableRegenTemp THEN
    dwISA182_AlarmWord_1.4 := TRUE;
    IF (iStateStep >= 40) AND (iStateStep <= 80) THEN
        iStateStep := 110; (* Snuffing & Feed Cut *)
    END_IF;
END_IF;

(* Bit 6: Wet Gas Compressor Suction Low-Pressure Trip (< 1.20 bar) *)
IF (rWetGasCompSuctionPress < 1.20) AND (iStateStep >= 40) THEN
    dwISA182_AlarmWord_1.6 := TRUE;
    IF iStateStep = 60 THEN
        iStateStep := 90; (* Partial Feed Shedding *)
    END_IF;
END_IF;

(* Bit 7: Riser Outlet Temperature High-High Trip (> 550 deg C) *)
IF (rRiserOutletTemp_Actual > rMaxAllowableROT) AND (iStateStep >= 40) THEN
    dwISA182_AlarmWord_1.7 := TRUE;
    IF iStateStep = 60 THEN
        iStateStep := 90;
    END_IF;
END_IF;

(* Bit 8: Riser Outlet Temperature Low-Low Trip (< 515 deg C) *)
IF (rRiserOutletTemp_Actual < rMinAllowableROT) AND (iStateStep >= 50) THEN
    dwISA182_AlarmWord_1.8 := TRUE;
END_IF;

(* Bit 9: Flue Gas Oxygen Low-Low Trip (< 0.20 % vol - Explosive Combustible Flue Gas Hazard) *)
IF (rVoted_FlueGasO2 < 0.20) AND (iStateStep >= 30) THEN
    dwISA182_AlarmWord_1.9 := TRUE;
END_IF;

(* Bit 10: Flue Gas CO High-High Alarm (> 2500 ppm) *)
IF rFlueGasCO_Concentration > 2500.0 THEN
    dwISA182_AlarmWord_1.10 := TRUE;
END_IF;

(* Bit 11: Main Combustion Air Flow Low-Low Trip (< 28,000 Nm3/h) *)
IF (rMainAirBlowerFlow_Actual < rMinCombustionAirFlow_Trip) AND (iStateStep >= 30) THEN
    dwISA182_AlarmWord_1.11 := TRUE;
    IF iStateStep < 100 THEN
        iStateStep := 110;
    END_IF;
END_IF;

(* Bit 12: Feed Dispersion Steam Low-Low Trip (< 1200 kg/h) *)
IF (rDispersionSteamFlow_Actual < 1200.0) AND (iStateStep >= 40) THEN
    dwISA182_AlarmWord_1.12 := TRUE;
END_IF;

(* Bit 13: Stripper Steam Low-Low Warning (< 1500 kg/h) *)
IF (rStrippingSteamFlow_Actual < 1500.0) AND (iStateStep >= 30) THEN
    dwISA182_AlarmWord_1.13 := TRUE;
END_IF;

(* Bit 21: Catalyst Bed Level / Inventory High-High (> 90 kPa) *)
IF rRegenBedDifferentialPress > 90.0 THEN
    dwISA182_AlarmWord_1.21 := TRUE;
ELSIF rRegenBedDifferentialPress < 30.0 THEN
    dwISA182_AlarmWord_1.22 := TRUE; (* Bed Level Low-Low (< 30 kPa) *)
ELSE
    dwISA182_AlarmWord_1.21 := FALSE;
    dwISA182_AlarmWord_1.22 := FALSE;
END_IF;

(* -------------------------------------------------------------------------------------------------- *)
(* ISA-18.2 SECONDARY PROCESS ADVISORY & WARNING ALARMS (dwISA182_AlarmWord_2)                        *)
(* -------------------------------------------------------------------------------------------------- *)
(* Bit 0: RCSV Delta P Low Warning (< 0.35 bar) *)
IF rVoted_RCSV_DeltaP < rMinSlideValveDeltaP_Warn THEN
    dwISA182_AlarmWord_2.0 := TRUE;
    bSlideValveReverseFlowWarning := TRUE;
ELSE
    dwISA182_AlarmWord_2.0 := FALSE;
    bSlideValveReverseFlowWarning := FALSE;
END_IF;

(* Bit 1: SCSV Delta P Low Warning (< 0.35 bar) *)
IF rVoted_SCSV_DeltaP < rMinSlideValveDeltaP_Warn THEN
    dwISA182_AlarmWord_2.1 := TRUE;
    bSlideValveReverseFlowWarning := TRUE;
ELSE
    dwISA182_AlarmWord_2.1 := FALSE;
END_IF;

(* Bit 3: Regenerator Bed Temperature High Warning (> 735 deg C) *)
IF rVoted_RegenBedTemp > 735.0 THEN
    dwISA182_AlarmWord_2.3 := TRUE;
ELSIF rVoted_RegenBedTemp < 680.0 THEN
    dwISA182_AlarmWord_2.4 := TRUE; (* Bed Temperature Low Warning (< 680 deg C) *)
ELSE
    dwISA182_AlarmWord_2.3 := FALSE;
    dwISA182_AlarmWord_2.4 := FALSE;
END_IF;

(* Bit 5: Flue Gas O2 High Warning (> 3.5 % vol) *)
IF rVoted_FlueGasO2 > 3.50 THEN
    dwISA182_AlarmWord_2.5 := TRUE;
ELSIF rVoted_FlueGasO2 < 0.80 THEN
    dwISA182_AlarmWord_2.6 := TRUE; (* Flue Gas O2 Low Warning (< 0.80 % vol) *)
ELSE
    dwISA182_AlarmWord_2.5 := FALSE;
    dwISA182_AlarmWord_2.6 := FALSE;
END_IF;

(* Bit 8: Riser Outlet Temperature Deviation Warning (> +/- 2.5 deg C) *)
IF ABS(rRiserOutletTemp_Actual - rTargetRiserOutletTemp) > 2.50 THEN
    dwISA182_AlarmWord_2.8 := TRUE;
ELSE
    dwISA182_AlarmWord_2.8 := FALSE;
END_IF;

(* Bit 9: Heavy Gas Oil Feed CCR Influx High Warning (> 5.5 wt%) *)
IF rFeedConradsonCarbonRes > 5.50 THEN
    dwISA182_AlarmWord_2.9 := TRUE;
ELSE
    dwISA182_AlarmWord_2.9 := FALSE;
END_IF;

(* Bit 18: Stripper Bed Level High (> 75 %) *)
IF vecStateEstimate[13] > 75.0 THEN
    dwISA182_AlarmWord_2.18 := TRUE;
ELSIF vecStateEstimate[13] < 35.0 THEN
    dwISA182_AlarmWord_2.19 := TRUE; (* Stripper Bed Level Low (< 35 %) *)
ELSE
    dwISA182_AlarmWord_2.18 := FALSE;
    dwISA182_AlarmWord_2.19 := FALSE;
END_IF;

(* Bit 20: Wet Gas Compressor Suction High Warning (> 2.60 bar) *)
IF rWetGasCompSuctionPress > 2.60 THEN
    dwISA182_AlarmWord_2.20 := TRUE;
ELSE
    dwISA182_AlarmWord_2.20 := FALSE;
END_IF;

(* Bit 21: Feed Preheat Furnace Duty High Warning (> 90 %) *)
IF rPreheatFurnaceFuelDutyCmd > 90.0 THEN
    dwISA182_AlarmWord_2.21 := TRUE;
ELSE
    dwISA182_AlarmWord_2.21 := FALSE;
END_IF;

(* Bit 22: Catalyst Circulation Rate Exceeded Warning (> 42 t/min) *)
IF rEstimatedCatCirculationRate > 42.0 THEN
    dwISA182_AlarmWord_2.22 := TRUE;
ELSE
    dwISA182_AlarmWord_2.22 := FALSE;
END_IF;

(* -------------------------------------------------------------------------------------------------- *)
(* 16-BIT PACKED OPERATIONAL STATUS WORD (wFCCU_OperationalStatus)                                    *)
(* -------------------------------------------------------------------------------------------------- *)
wFCCU_OperationalStatus.0 := bFCCU_SystemReady;
wFCCU_OperationalStatus.1 := bMPC_OptimizationActive;
wFCCU_OperationalStatus.2 := bFeedInflowPermissive;
wFCCU_OperationalStatus.3 := bExpanderCoupled;
wFCCU_OperationalStatus.4 := bSlideValveReverseFlowWarning;
wFCCU_OperationalStatus.5 := bSlideValveFastTripActive;
wFCCU_OperationalStatus.6 := bAfterburningDetected;
wFCCU_OperationalStatus.7 := bSensorTMR_Degraded;
wFCCU_OperationalStatus.8 := (rMainAirBlowerFlow_Actual > 30000.0);
wFCCU_OperationalStatus.9 := (rPreheatFurnaceFuelDutyCmd > 10.0);
wFCCU_OperationalStatus.10 := (rEstimatedCatCirculationRate > 10.0);
wFCCU_OperationalStatus.11 := bEmergencySnuffingActive;
wFCCU_OperationalStatus.12 := (iStateStep = 90);
wFCCU_OperationalStatus.13 := (iStateStep = 110) OR (iStateStep = 120);
wFCCU_OperationalStatus.14 := bManualModePermissive;
wFCCU_OperationalStatus.15 := bHeartbeatPulse;
"""
    parts.append(phase7)
    
    # -------------------------------------------------------------------------
    # PART 13: CLOSING DECLARATION
    # -------------------------------------------------------------------------
    parts.append("\nEND_FUNCTION_BLOCK\n")
    
    return "".join(parts)

if __name__ == "__main__":
    st_code = build_fccu_st()
    print(f"Generated IEC ST Code Length: {len(st_code)} characters")
    
    # Check parity and essential structure
    errors = []
    lines = [l.strip() for l in st_code.strip().splitlines() if l.strip()]
    if not lines[0].startswith("FUNCTION_BLOCK FB_"):
        errors.append("First line does not start with FUNCTION_BLOCK FB_")
    if lines[-1] != "END_FUNCTION_BLOCK":
        errors.append(f"Last line is '{lines[-1]}', expected 'END_FUNCTION_BLOCK'")
        
    open_c = st_code.count("(*")
    close_c = st_code.count("*)")
    if open_c != close_c:
        errors.append(f"Comment mismatch: (* count ({open_c}) != *) count ({close_c})")
        
    no_comments = re.sub(r'\(\*[\s\S]*?\*\)', '', st_code)
    clean_code = re.sub(r'\'[^\']*\'', '', no_comments)
    
    ifs = len(re.findall(r'\b(?<!END_)(?<!ELS)IF\b', clean_code, re.IGNORECASE))
    end_ifs = len(re.findall(r'\bEND_IF\b', clean_code, re.IGNORECASE))
    cases = len(re.findall(r'\b(?<!END_)CASE\b', clean_code, re.IGNORECASE))
    end_cases = len(re.findall(r'\bEND_CASE\b', clean_code, re.IGNORECASE))
    fors = len(re.findall(r'\b(?<!END_)FOR\b', clean_code, re.IGNORECASE))
    end_fors = len(re.findall(r'\bEND_FOR\b', clean_code, re.IGNORECASE))
    whiles = len(re.findall(r'\b(?<!END_)WHILE\b', clean_code, re.IGNORECASE))
    end_whiles = len(re.findall(r'\bEND_WHILE\b', clean_code, re.IGNORECASE))
    fb_starts = len(re.findall(r'\b(?<!END_)FUNCTION_BLOCK\b', clean_code, re.IGNORECASE))
    fb_ends = len(re.findall(r'\bEND_FUNCTION_BLOCK\b', clean_code, re.IGNORECASE))
    
    print("Internal Parity Audit:")
    print(f"  IF: {ifs} | END_IF: {end_ifs} (Match: {ifs == end_ifs})")
    print(f"  CASE: {cases} | END_CASE: {end_cases} (Match: {cases == end_cases})")
    print(f"  FOR: {fors} | END_FOR: {end_fors} (Match: {fors == end_fors})")
    print(f"  WHILE: {whiles} | END_WHILE: {end_whiles} (Match: {whiles == end_whiles})")
    print(f"  FUNCTION_BLOCK: {fb_starts} | END_FUNCTION_BLOCK: {fb_ends} (Match: {fb_starts == fb_ends})")
    
    if ifs != end_ifs: errors.append(f"IF mismatch: {ifs} vs {end_ifs}")
    if cases != end_cases: errors.append(f"CASE mismatch: {cases} vs {end_cases}")
    if fors != end_fors: errors.append(f"FOR mismatch: {fors} vs {end_fors}")
    if whiles != end_whiles: errors.append(f"WHILE mismatch: {whiles} vs {end_whiles}")
    if fb_starts != fb_ends: errors.append(f"FB mismatch: {fb_starts} vs {fb_ends}")
    
    if errors:
        print("INTERNAL PRE-CHECK FAILED:")
        for err in errors:
            print(" -", err)
        sys.exit(1)
        
    print("ALL INTERNAL PRE-CHECKS PASSED!")
    
    # Target dataset file
    user_prompt = """You are a veteran Principal Automation Fellow & Cyber-Physical Systems Chair (V7 Max-Persona) specializing in commercial oil refining, fluidized catalytic cracking, and heavy petrochemical cyber-physical automation.

YOUR MISSION:
Synthesize an ultra-dense, mathematically complete, production-grade IEC 61131-3 Structured Text dataset row for:
**Commercial Petrochemicals & Refining: Fluid Catalytic Cracking Unit (FCCU) Catalyst Regenerator & Riser Reactor with Slide Valve Differential Pressure & Multi-Variable MPC**
Function Block Name: `FB_Refining_FluidCatalyticCracking_RegeneratorMPC`
Target File: `data/swarm_raw/agent_3d91b07c.json`

SPECIFICATIONS & REQUIREMENTS:
1. Target Character Length: 55,000 to 85,000+ characters for the IEC 61131-3 ST output. Zero placeholders, zero summaries, zero truncation comments like '// ... rest of code'. Every single state, matrix, loop, and formula must be completely unrolled and coded.
2. Technical Cyber-Physical Depth:
   - High-temperature fluidized catalytic cracking system (Riser reactor at 520–550 deg C, Regenerator fluidized bed at 680–740 deg C, system pressure 2.0–3.5 bar).
   - Precision electrohydraulic slide valves regulating spent catalyst from disengager stripper to regenerator, and regenerated catalyst from regenerator back to riser foot.
   - Critical differential pressure closed-loop control across slide valves (Delta P kept strictly between 0.35 and 0.85 bar) to prevent catastrophic hydrocarbon reverse flow into the oxygen-rich regenerator.
   - Main combustion air blower (axial/centrifugal compressor driven by steam turbine/electric motor) regulating air mass flow rate to maintain complete coke combustion while preventing thermal runaway in regenerator cyclones (afterburning detection via flue gas CO/CO2/O2 analyzers).
   - Discrete State-Space Model (16x16 state matrix A, 16x8 B, C, D) incorporating catalyst fluidization bed hydrodynamics, coke combustion reaction kinetics, riser cracking endothermic enthalpy absorption, and stripper steam stripping balance.
   - Receding-horizon MPC for multivariable control of regenerated catalyst slide valve position, feed preheat furnace duty, and combustion air rate to hold riser outlet temperature (ROT) within +/- 0.5 deg C under fluctuating heavy gas oil (HGO) feed properties.
   - 2oo3 Triple Modular Redundancy (TMR) voting across slide valve differential pressure transmitters, regenerator bed dense-phase thermocouples, and flue gas oxygen analyzers with bumpless degradation.
   - 12-Stage Operational FSM (Regenerator Air Purge & Refractory Dryout, Torching Oil Ignition & Thermal Ramp, Catalyst Circulation Hydrodynamic Balancing, Heavy Gas Oil Feed Inflow Cut-In, Riser Temperature Closed-Loop Stabilization, Steady-State MPC Cracking Optimization, Steam Stripping Steam Ratio Adjustment, Flue Gas Power Recovery Expander Coupling, Partial Feed Shedding Maneuver, Catalyst Purge & Inactive Circulation, Emergency Nitrogen De-Inventory Snuffing, Emergency Slide Valve SIL-3 Fast Close).
   - ISA-18.2 multi-tiered alarm matrix (Slide valve Delta P reverse flow HH trip, regenerator cyclone thermal afterburning trip, blower surge warning, wet gas compressor suction low-pressure trip) with bit-packed telemetry DWORDs.
3. Strict Syntax & AST Parity:
   - Enclose the Structured Text in TRIPLE BACKTICKS with iec-st:
   ```iec-st
   FUNCTION_BLOCK FB_Refining_FluidCatalyticCracking_RegeneratorMPC
   ...
   END_FUNCTION_BLOCK
   ```
   - 100% exact matching parity: every IF has END_IF;, every CASE has END_CASE;, every FOR has END_FOR;, every WHILE has END_WHILE;.
   - Ensure comments do not accidentally close prematurely (do not use `*)` inside comments; write `tau_star` instead of `tau*`).
4. Dataset File Format:
   Save to `data/swarm_raw/agent_3d91b07c.json` in JSON format:
   {"instruction": "...", "input": "...", "output": "```iec-st\\n...\\n```"}"""

    content_with_fence = "```iec-st\n" + st_code + "\n```"
    record = {
        "messages": [
            {"role": "user", "content": user_prompt},
            {"role": "assistant", "content": content_with_fence}
        ],
        "instruction": user_prompt,
        "input": "",
        "output": content_with_fence
    }
    
    os.makedirs("data/swarm_raw", exist_ok=True)
    target_path = "data/swarm_raw/agent_3d91b07c.json"
    with open(target_path, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)
    print(f"Successfully saved to {target_path}")
