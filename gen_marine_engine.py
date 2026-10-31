# -*- coding: utf-8 -*-
"""
Generator script for FB_Marine_TwoStroke_DualFuel_LNG_SCR
IEC 61131-3 Structured Text dataset.
Target size: 65,000 - 85,000 characters.
Target file: data/swarm_raw/agent_7b1940ca.json
"""

import os
import sys
import json
import re

def generate_marine_engine_st():
    parts = []

    # =========================================================================
    # 1. FUNCTION BLOCK DECLARATION & COMPREHENSIVE CYBER-PHYSICAL HEADER
    # =========================================================================
    parts.append("""FUNCTION_BLOCK FB_Marine_TwoStroke_DualFuel_LNG_SCR
(* ====================================================================================================
  LUMINA CYBER-PHYSICAL SYSTEMS ARCHITECTURE - HEAVY MARINE PROPULSION & PROPULSION DYNAMICS DIVISION
  SYSTEM IDENTIFIER: CPS-MAR-PROP-75MW-2S-DF-LNG-SCR-V8.4
  ENGINE DESIGNATION: 75 MW 11-Cylinder Two-Stroke Crosshead Dual-Fuel (High-Pressure LNG / MGO) Marine Engine
                      Direct-Coupled to Fixed-Pitch Propeller with High-Pressure Selective Catalytic Reduction
  GOVERNING INDUSTRIAL & CLASSIFICATION SOCIETY STANDARDS:
    - IMO MARPOL Annex VI Regulation 13 (Tier III NOx Emission Control Area - ECA Standards: <= 3.4 g/kWh)
    - DNV-GL Part 4 Chapter 2 / IACS UR M71 & M72 (Safety Regulations for Dual-Fuel Engines & FGSS)
    - IGF Code (International Code of Safety for Ships Using Gases or Other Low-Flashpoint Fuels - IMO MSC.391(95))
    - CIMAC Working Group 19 (Recommendations for Marine Two-Stroke Gas & Dual-Fuel Engine Integration)
    - IEC 61508 / IEC 61511 (SIL-3 Functional Safety Architecture for Gas Valve Train & Fast Bleed Venting)
    - ISA-18.2 / EEMUA 191 (Alarm Management Lifecycle & Bit-Packed Alarm Telemetry)
    - IEC 61131-3 3rd Edition (Deterministic Industrial Programmable Logic Controller Structured Text)

  CYBER-PHYSICAL MECHANICAL, THERMODYNAMIC & CHEMICAL NOMENCLATURE:
    1. ENGINE ARCHITECTURE & COMBUSTION KINETICS:
       - Engine Configuration: 11-cylinder in-line, uniflow-scavenged, two-stroke crosshead diesel cycle.
       - Bore: 950 mm (0.950 m), Stroke: 3,400 mm (3.400 m).
       - Swept Cylinder Displacement: V_s = (pi / 4) * D^2 * S = 2,409.8 liters (2.410 m3) per cylinder.
       - Total Engine Swept Volume: V_total = 11 * 2,409.8 = 26,508 liters (26.508 m3).
       - Rated Maximum Continuous Rating (MCR): 75,000 kW (75.0 MW) at 84.0 RPM.
       - Mean Effective Pressure: MEP = 21.5 bar at MCR. Mean Piston Speed: c_m = 9.52 m/s.
       - Direct Drive: Crankshaft rigidly coupled to 10.2 m diameter, 5-bladed Nickel-Aluminum-Bronze propeller.

    2. HIGH-PRESSURE LNG FUEL GAS SUPPLY SYSTEM (FGSS):
       - Cryogenic storage at -162 deg C, delivered via triplex high-pressure piston pumps at 300 bar (30.0 MPa).
       - Supercritical methane vaporized via high-pressure Printed Circuit Heat Exchangers (PCHE) to +45 deg C.
       - Electronically controlled common-rail gas injection valves (ELGI / FIVA) injected directly into combustion
         chamber at Top Dead Center (TDC, approx 3 deg CA before TDC to 18 deg CA after TDC) at 300 bar.
       - High-pressure Diesel cycle combustion: avoids Otto-cycle pre-mixed combustion knock, eliminating
         methane slip (< 0.2 g/kWh) while achieving diesel thermal efficiency (> 51.5%).
       - Micro-pilot Marine Gas Oil (MGO) injection: 0.5% to 1.0% of total fuel energy initiates ignition of
         the high-pressure natural gas jets under supercritical gas rail pressure.
       - Double-walled fuel gas supply piping: inert Nitrogen (N2) pressurized annulus continuously monitored
         via optical hydrocarbon infrared gas detection sniffer channels.

    3. CYLINDER-BY-CYLINDER ELECTRO-HYDRAULIC EXHAUST VALVE ACTUATION (FIVA / ELFI):
       - Variable Exhaust Valve Closing (VEC): modulates effective compression ratio based on engine load
         and scavenge receiver temperature to optimize Miller timing and suppress peak in-cylinder temperature.
       - Variable Exhaust Valve Opening (VO): optimizes turbocharger blow-down pulse energy at part-load.

    4. HIGH-PRESSURE SELECTIVE CATALYTIC REDUCTION (HP-SCR) & THERMO-KINETICS:
       - Reactor vessel installed upstream of twin turbochargers to exploit high pre-turbine exhaust enthalpy
         (T_exh = 320 to 385 deg C, P_exh = 3.6 to 4.2 bar abs).
       - Aqueous Urea Solution (AUS40 - 40 wt% aqueous urea) atomized via compressed air into static mixer.
       - Monolithic honeycomb V2O5-WO3/TiO2 catalyst blocks driving selective catalytic reduction:
           4 NO + 4 NH3 + O2 -> 4 N2 + 6 H2O   (Standard SCR)
           NO + NO2 + 2 NH3  -> 2 N2 + 3 H2O   (Fast SCR)
       - Critical Ammonium Bisulfate (ABS) Thermal Constraint:
           NH3 + SO3 + H2O <-> NH4HSO4 (s,l)
         ABS solidifies into highly corrosive, sticky deposit below 305-310 deg C in exhaust containing SOx.
         Catalyst thermal management bypass damper dynamically controls pre-SCR temperature > 310 deg C.

    5. MARINE PROPELLER HYDRODYNAMICS & HEAVY SEAS DISTURBANCE:
       - Propeller Absorbed Torque: Q_prop = K_Q(J) * rho_water * n^2 * D^5
       - Advance Ratio: J = V_a / (n * D), where V_a = V_ship * (1 - w_wake).
       - Wave encounter torque perturbation: Delta_Q_wave = A_wave * sin(omega_enc * t) + noise, causing
         massive cyclic load fluctuations and risking overspeed / turbocharger compressor surge.

    6. DISCRETE 16-STATE MULTIVARIABLE STATE-SPACE & RECEDING-HORIZON MPC:
       - 16 discrete physical states, 8 manipulated actuator variables, 4 environmental disturbances.
       - Real-time unrolled quadratic optimization minimizing specific fuel consumption (SFC) and urea dosing
         while enforcing hard bounds on peak firing pressure (P_max <= 225 bar) and IMO Tier III NOx (<= 3.4 g/kWh).
==================================================================================================== *)
""")

    # =========================================================================
    # 2. VAR_INPUT BLOCK (MINIMUM 8 STRONGLY TYPED PHYSICAL INPUTS WITH UNITS)
    # =========================================================================
    parts.append("""VAR_INPUT
    (* ========================================================================================= *)
    (* PHYSICAL SENSOR INPUTS (WITH STRICT CIMAC / IMO / ISO BRACKETED PHYSICAL ENGINEERING UNITS)*)
    (* ========================================================================================= *)

    (* --- Crankshaft Angular Position & Speed Resolver Triplet (2oo3 TMR Bank) --- *)
    rCrankAngle_degCA_A             : REAL;     (* [deg] Optical resolver channel A crankshaft angle (0.00-359.95) *)
    rCrankAngle_degCA_B             : REAL;     (* [deg] Optical resolver channel B crankshaft angle (0.00-359.95) *)
    rCrankAngle_degCA_C             : REAL;     (* [deg] Optical resolver channel C crankshaft angle (0.00-359.95) *)
    rEngineSpeed_rpm_A              : REAL;     (* [rpm] Crankshaft flywheel magnetic pickup speed sensor A *)
    rEngineSpeed_rpm_B              : REAL;     (* [rpm] Crankshaft flywheel magnetic pickup speed sensor B *)
    rEngineSpeed_rpm_C              : REAL;     (* [rpm] Crankshaft flywheel magnetic pickup speed sensor C *)

    (* --- High-Pressure Fuel Gas Rail Pressure Transducers (2oo3 TMR Bank) --- *)
    rGasRailPress_bar_A             : REAL;     (* [bar] Supercritical natural gas common-rail pressure transmitter A *)
    rGasRailPress_bar_B             : REAL;     (* [bar] Supercritical natural gas common-rail pressure transmitter B *)
    rGasRailPress_bar_C             : REAL;     (* [bar] Supercritical natural gas common-rail pressure transmitter C *)
    rGasRailTemp_degC               : REAL;     (* [deg C] Supercritical natural gas common-rail temperature transmitter *)

    (* --- Scavenge Air Receiver Pressure & Temperature Transmitters (2oo3 TMR Bank) --- *)
    rScavAirPress_bar_A             : REAL;     (* [bar] Scavenge air receiver absolute pressure transmitter A *)
    rScavAirPress_bar_B             : REAL;     (* [bar] Scavenge air receiver absolute pressure transmitter B *)
    rScavAirPress_bar_C             : REAL;     (* [bar] Scavenge air receiver absolute pressure transmitter C *)
    rScavAirTemp_degC_A             : REAL;     (* [deg C] Scavenge air receiver temperature sensor A *)
    rScavAirTemp_degC_B             : REAL;     (* [deg C] Scavenge air receiver temperature sensor B *)
    rScavAirTemp_degC_C             : REAL;     (* [deg C] Scavenge air receiver temperature sensor C *)

    (* --- Cylinder Peak Combustion Pressure Transducers (11 Individual In-Cylinder Optical Sensors) --- *)
    rCylPeakPress_bar_01            : REAL;     (* [bar] Cylinder 01 piezoelectric peak firing pressure P_max *)
    rCylPeakPress_bar_02            : REAL;     (* [bar] Cylinder 02 piezoelectric peak firing pressure P_max *)
    rCylPeakPress_bar_03            : REAL;     (* [bar] Cylinder 03 piezoelectric peak firing pressure P_max *)
    rCylPeakPress_bar_04            : REAL;     (* [bar] Cylinder 04 piezoelectric peak firing pressure P_max *)
    rCylPeakPress_bar_05            : REAL;     (* [bar] Cylinder 05 piezoelectric peak firing pressure P_max *)
    rCylPeakPress_bar_06            : REAL;     (* [bar] Cylinder 06 piezoelectric peak firing pressure P_max *)
    rCylPeakPress_bar_07            : REAL;     (* [bar] Cylinder 07 piezoelectric peak firing pressure P_max *)
    rCylPeakPress_bar_08            : REAL;     (* [bar] Cylinder 08 piezoelectric peak firing pressure P_max *)
    rCylPeakPress_bar_09            : REAL;     (* [bar] Cylinder 09 piezoelectric peak firing pressure P_max *)
    rCylPeakPress_bar_10            : REAL;     (* [bar] Cylinder 10 piezoelectric peak firing pressure P_max *)
    rCylPeakPress_bar_11            : REAL;     (* [bar] Cylinder 11 piezoelectric peak firing pressure P_max *)

    (* --- Cylinder Exhaust Gas Temperatures (11 Duplex Thermocouples at Cylinder Exits) --- *)
    rCylExhTemp_degC_01             : REAL;     (* [deg C] Cylinder 01 exhaust gas outlet temperature *)
    rCylExhTemp_degC_02             : REAL;     (* [deg C] Cylinder 02 exhaust gas outlet temperature *)
    rCylExhTemp_degC_03             : REAL;     (* [deg C] Cylinder 03 exhaust gas outlet temperature *)
    rCylExhTemp_degC_04             : REAL;     (* [deg C] Cylinder 04 exhaust gas outlet temperature *)
    rCylExhTemp_degC_05             : REAL;     (* [deg C] Cylinder 05 exhaust gas outlet temperature *)
    rCylExhTemp_degC_06             : REAL;     (* [deg C] Cylinder 06 exhaust gas outlet temperature *)
    rCylExhTemp_degC_07             : REAL;     (* [deg C] Cylinder 07 exhaust gas outlet temperature *)
    rCylExhTemp_degC_08             : REAL;     (* [deg C] Cylinder 08 exhaust gas outlet temperature *)
    rCylExhTemp_degC_09             : REAL;     (* [deg C] Cylinder 09 exhaust gas outlet temperature *)
    rCylExhTemp_degC_10             : REAL;     (* [deg C] Cylinder 10 exhaust gas outlet temperature *)
    rCylExhTemp_degC_11             : REAL;     (* [deg C] Cylinder 11 exhaust gas outlet temperature *)

    (* --- High-Pressure SCR Reactor Thermal & Differential Pressure Sensors (2oo3 TMR Bank) --- *)
    rSCR_InletTemp_degC_A           : REAL;     (* [deg C] SCR reactor inlet pre-catalyst gas temperature A *)
    rSCR_InletTemp_degC_B           : REAL;     (* [deg C] SCR reactor inlet pre-catalyst gas temperature B *)
    rSCR_InletTemp_degC_C           : REAL;     (* [deg C] SCR reactor inlet pre-catalyst gas temperature C *)
    rSCR_BedDiffPress_mbar          : REAL;     (* [mbar] Differential pressure across SCR catalyst honeycomb bed *)
    rSCR_OutletTemp_degC            : REAL;     (* [deg C] Post-catalyst exhaust gas temperature downstream *)

    (* --- Continuous Emission Monitoring System (CEMS 2oo3 TMR Gas Analyzers) --- *)
    rCEMS_NOx_ppm_A                 : REAL;     (* [ppm] Tailpipe NOx concentration analyzer channel A *)
    rCEMS_NOx_ppm_B                 : REAL;     (* [ppm] Tailpipe NOx concentration analyzer channel B *)
    rCEMS_NOx_ppm_C                 : REAL;     (* [ppm] Tailpipe NOx concentration analyzer channel C *)
    rCEMS_O2_Pct                    : REAL;     (* [%] Zirconia oxygen sensor stack concentration *)
    rCEMS_NH3_Slip_ppm              : REAL;     (* [ppm] Quantum cascade laser tailpipe ammonia slip analyzer *)
    rCEMS_SO2_ppm                   : REAL;     (* [ppm] Ultraviolet resonance stack SO2 concentration analyzer *)

    (* --- Twin Variable-Geometry Turbochargers (VGT) & Auxiliary Blowers --- *)
    rTC1_Speed_rpm                  : REAL;     (* [rpm] Turbocharger unit 1 rotor shaft speed *)
    rTC2_Speed_rpm                  : REAL;     (* [rpm] Turbocharger unit 2 rotor shaft speed *)
    rTC1_Vibration_mms              : REAL;     (* [mm/s] Turbocharger unit 1 bearing casing RMS vibration velocity *)
    rTC2_Vibration_mms              : REAL;     (* [mm/s] Turbocharger unit 2 bearing casing RMS vibration velocity *)

    (* --- Marine Propeller Hydrodynamics & Seaway Disturbance Inputs --- *)
    rShipSpeed_knots                : REAL;     (* [knots] Doppler speed log speed through water (STW) *)
    rSignificantWaveHeight_m        : REAL;     (* [m] Radar wave gauge significant sea wave height H_s *)
    rWaveEncounterFreq_rads         : REAL;     (* [rad/s] Doppler-corrected wave encounter frequency omega_e *)
    rPropellerShaftTorque_kNm       : REAL;     (* [kNm] Optical strain-gauge torsion meter propeller shaft torque *)

    (* --- Engine Auxiliary Mechanical & Safety Systems --- *)
    rMainLubeOilPress_bar           : REAL;     (* [bar] Crosshead bearing main lubricating oil header pressure *)
    rCrossheadBearingTempMax_degC   : REAL;     (* [deg C] Maximum monitored temperature across 11 crosshead bearings *)
    rJackingOilPress_bar            : REAL;     (* [bar] High-pressure crosshead jacking oil pump discharge pressure *)
    rDoubleWallPipeHydrocarbon_ppm  : REAL;     (* [ppm] Double-wall gas supply pipe annulus hydrocarbon sniffer *)
    rFuelGasLHV_MJkg                : REAL;     (* [MJ/kg] Online gas chromatograph natural gas Lower Heating Value *)
    rMGO_FuelTemp_degC              : REAL;     (* [deg C] Pilot Marine Gas Oil supply temperature at booster unit *)

    (* --- Supervisory Bridge Telegraph & Automation Commands --- *)
    rBridgeTelegraphOrder_rpm       : REAL;     (* [rpm] Bridge electronic telegraph engine speed demand *)
    rMCR_PowerRating_MW             : REAL;     (* [MW] Maximum continuous rating nameplate engine power (75.0 MW) *)
    tScanPeriod_s                   : REAL;     (* [s] Deterministic cyclic task execution period (0.010 to 0.050 s) *)

    (* --- Discrete Safety Interlocks & Operator Commands --- *)
    bMasterEnable                   : BOOL;     (* Master automation block enable command *)
    bEmergencyStopSIL3              : BOOL;     (* Hardwired dual-channel fail-safe emergency stop relay (Active High = OK) *)
    bFGSS_GasReadyPermissive        : BOOL;     (* Fuel Gas Supply System skid ready, pressurized, and leak-free *)
    bTurningGearEngaged             : BOOL;     (* Engine maintenance turning gear mechanical position limit switch *)
    bIndicatorCocksOpen             : BOOL;     (* Cylinder head indicator cocks manual verification switch *)
    bRoughWeatherModeCmd            : BOOL;     (* Bridge command for heavy seas torque limiter and governor damping *)
    bHarborManoeuvringCmd           : BOOL;     (* Bridge command for harbor manoeuvring mode (MGO forced operation) *)
    bAcknowledgeAlarms              : BOOL;     (* Operator alarm reset and acknowledgment push-button *)
END_VAR
""")

    # =========================================================================
    # 3. VAR_OUTPUT BLOCK (MINIMUM 7 STRONGLY TYPED PHYSICAL OUTPUTS WITH UNITS)
    # =========================================================================
    parts.append("""VAR_OUTPUT
    (* ========================================================================================= *)
    (* ACTUATOR COMMANDS & TELEMETRY REGISTERS (WITH STRICT CIMAC / ISO PHYSICAL UNITS)         *)
    (* ========================================================================================= *)

    (* --- High-Pressure Common-Rail Gas Admission Actuator Commands (ELGI Valves) --- *)
    rGasInjectionDuration_ms        : REAL;     (* [ms] Base common-rail gas injection valve opening duration *)
    rGasInjectionStartAngle_degCA   : REAL;     (* [deg] Common-rail gas injection start crank angle (BTDC / ATDC) *)
    rGasFuelMassFlow_kgh            : REAL;     (* [kg/h] Total natural gas fuel consumption mass flow rate *)
    rGasEnergySharePercent          : REAL;     (* [%] Percentage of total combustion energy supplied by natural gas *)

    (* --- Micro-Pilot Diesel Fuel Oil Injection Actuator Commands (ELFI Valves) --- *)
    rPilotDieselDuration_ms         : REAL;     (* [ms] Micro-pilot MGO injection valve pulse width command *)
    rPilotDieselMassPerStroke_mg    : REAL;     (* [mg] Mass of pilot diesel fuel injected per cylinder stroke *)
    rPilotDieselFlow_lh             : REAL;     (* [l/h] Volumetric pilot diesel fuel oil consumption rate *)

    (* --- Cylinder Variable Exhaust Valve Actuation (FIVA / VEC Actuators) --- *)
    rExhValveCloseAngle_degCA       : REAL;     (* [deg] Variable exhaust valve closing angle command (VEC) *)
    rExhValveOpenAngle_degCA        : REAL;     (* [deg] Variable exhaust valve opening angle command (VO) *)

    (* --- High-Pressure SCR Emission Abatement Actuator Commands --- *)
    rSCR_UreaDosingFlow_kgh         : REAL;     (* [kg/h] Aqueous urea solution (AUS40) high-pressure dosing rate *)
    rSCR_ThermalBypassDamper_Pct    : REAL;     (* [%] Pre-SCR exhaust thermal management bypass damper position *)
    rSCR_DeNOxEfficiency_Pct        : REAL;     (* [%] Real-time calculated catalytic NOx reduction efficiency *)
    rCalculatedNOxSpecific_gkWh     : REAL;     (* [g/kWh] Specific brake NOx emission rate (IMO Tier III target <= 3.4) *)

    (* --- Scavenge Air & Turbocharger Modulation Actuator Commands --- *)
    rVGT_NozzlePosition_Pct         : REAL;     (* [%] Twin variable-geometry turbocharger vane position command *)
    rAuxBlowerSpeedCmd_rpm_01       : REAL;     (* [rpm] Auxiliary electric scavenge blower 1 speed setpoint *)
    rAuxBlowerSpeedCmd_rpm_02       : REAL;     (* [rpm] Auxiliary electric scavenge blower 2 speed setpoint *)
    rScavAirPressureDemand_bar      : REAL;     (* [bar] Dynamic target scavenge air absolute pressure setpoint *)

    (* --- Fuel Gas Supply Skid Pressure Modulation --- *)
    rFGSS_RailPressDemand_bar       : REAL;     (* [bar] Dynamic high-pressure cryogenic pump discharge setpoint *)
    rGasVentFastBleedValve_Pct      : REAL;     (* [%] Fast gas depressurization bleed vent valve command *)

    (* --- Engine Propulsion Performance & Indicated Mechanical Outputs --- *)
    rEngineShaftPower_MW            : REAL;     (* [MW] Engine delivered brake shaft propulsion power *)
    rEngineBrakeTorque_kNm          : REAL;     (* [kNm] Total instantaneous brake torque produced by engine *)
    rIndicatedThermalEff_Pct        : REAL;     (* [%] Real-time cycle indicated thermal efficiency *)
    rPropellerAdvanceRatio_J        : REAL;     (* [-] Instantaneous propeller hydrodynamic advance ratio J *)

    (* --- Standardized Status & Diagnostic 32-Bit Bit-Packed Words --- *)
    dwSystemStatusWord              : DWORD;    (* Bit-packed engine propulsion operational state and mode telemetry *)
    dwAlarmStatusWord               : DWORD;    (* Bit-packed ISA-18.2 severity classified alarm registry *)
    dwTMR_DiagnosticWord            : DWORD;    (* Bit-packed 2oo3 sensor triplet degradation and fault matrix *)
    dwSafetyInterlockWord           : DWORD;    (* Bit-packed SIL-3 safety shutdown permissive and trip latches *)
    dwMPC_DiagnosticsWord           : DWORD;    (* Bit-packed state-space observer and MPC QP solver health flags *)

    (* --- Discrete Operational Mode & Permissive Flags --- *)
    bEngineRunning                  : BOOL;     (* Engine rotating under fuel combustion power *)
    bEngineReadyForStart            : BOOL;     (* All starting permissives verified healthy *)
    bDualFuelModeActive             : BOOL;     (* Operating on high-pressure LNG + micro-pilot diesel *)
    bDieselBackupModeActive         : BOOL;     (* Operating on 100% marine diesel / gas oil backup fuel *)
    bTierIII_Compliant              : BOOL;     (* Verified real-time specific NOx emission <= 3.40 g/kWh *)
    bRoughWeatherDampingOn          : BOOL;     (* Heavy seas governor torque damping filter active *)
    bGasEmergencyVented             : BOOL;     (* Safety shutdown fast gas depressurization active *)
    bSIL3_ShutdownTripped           : BOOL;     (* SIL-3 engine emergency trip safety circuit open *)
END_VAR
""")

    # =========================================================================
    # 4. VAR BLOCK (INTERNAL CONSTANTS, MATRICES, 2oo3 TMR, FSM, ALARMS)
    # =========================================================================
    parts.append("""VAR
    (* ========================================================================================= *)
    (* INTERNAL CYBER-PHYSICAL STATE VARIABLES, MATRICES, OBSERVERS & CONTROL ARRAYS            *)
    (* ========================================================================================= *)

    (* First Scan Initialization Sentinel *)
    bFirstScanInitialized           : BOOL := FALSE;

    (* ----------------------------------------------------------------------------------------- *)
    (* 1. THERMODYNAMIC, CHEMICAL & NAVAL ARCHITECTURE CONSTANTS                                *)
    (* ----------------------------------------------------------------------------------------- *)
    rCylBore_m                      : REAL := 0.950;    (* Cylinder bore diameter [m] *)
    rCylStroke_m                    : REAL := 3.400;    (* Piston stroke length [m] *)
    rCylDisplacement_m3             : REAL := 2.4098;   (* Single cylinder swept volume [m3] *)
    rEngineTotalDispl_m3            : REAL := 26.508;   (* Total 11-cylinder displacement [m3] *)
    rConnectingRodLength_m          : REAL := 3.800;    (* Connecting rod center-to-center length [m] *)
    rCompressionRatioNominal        : REAL := 18.50;    (* Nominal geometric compression ratio [-] *)
    rEngineTotalInertia_kgm2        : REAL := 1850000.0;(* Engine crankshaft, flywheel, and propeller total inertia [kg*m2] *)
    rPropellerDiameter_m            : REAL := 10.20;    (* 5-bladed fixed-pitch marine propeller diameter [m] *)
    rPropellerPitchRatio_PD         : REAL := 0.880;    (* Propeller pitch-to-diameter ratio P/D [-] *)
    rSeawaterDensity_kgm3           : REAL := 1025.0;   (* Ambient standard seawater mass density [kg/m3] *)
    rWageningen_KQ0                 : REAL := 0.0385;   (* Wageningen B-series zero-advance torque coefficient K_Q0 *)
    rWageningen_dKQ_dJ              : REAL := -0.0245;  (* Slope of torque coefficient vs advance ratio dK_Q/dJ *)
    rNominalWakeFraction_w0         : REAL := 0.285;    (* Nominal hull boundary-layer wake fraction w_0 [-] *)

    (* Thermochemical Constants for Natural Gas & Selective Catalytic Reduction *)
    rMolarMass_CH4_kgkmol           : REAL := 16.043;   (* Methane molecular weight [kg/kmol] *)
    rMolarMass_NOx_kgkmol           : REAL := 46.0055;  (* Nitrogen dioxide equivalent molecular weight [kg/kmol] *)
    rMolarMass_Urea_kgkmol          : REAL := 60.056;   (* Solid urea molecular weight [kg/kmol] *)
    rMolarMass_NH3_kgkmol           : REAL := 17.031;   (* Ammonia molecular weight [kg/kmol] *)
    rMolarMass_SO3_kgkmol           : REAL := 80.063;   (* Sulfur trioxide molecular weight [kg/kmol] *)
    rUreaAqueousConcentration       : REAL := 0.400;    (* Commercial AUS40 aqueous urea solution mass fraction [-] *)
    rStoichUreaToNOx_kgkg           : REAL := 0.6527;   (* Theoretical stoichiometric mass ratio: kg urea / kg NOx *)
    rUniversalGasConst_JmolK        : REAL := 8.31446;  (* Universal ideal gas constant [J/(mol*K)] *)

    (* Ammonium Bisulfate (ABS) Solidification Boundary Parameters *)
    rABS_Antoine_A                  : REAL := 14.850;   (* Log-partial pressure equilibrium parameter A *)
    rABS_Antoine_B                  : REAL := 4280.0;   (* Log-partial pressure equilibrium parameter B [K] *)
    rABS_CriticalMinTemp_degC       : REAL := 310.0;    (* Absolute critical catalyst lower temperature limit [deg C] *)
    rABS_DepositionRiskIndex        : REAL := 0.0;      (* Real-time normalized ABS deposition risk index [0.0-1.0] *)

    (* ----------------------------------------------------------------------------------------- *)
    (* 2. TRIPLE MODULAR REDUNDANCY (2oo3 TMR) FILTER REGISTERS & TOLERANCES                    *)
    (* ----------------------------------------------------------------------------------------- *)
    (* Voted Primary Signals *)
    rVoted_EngineSpeed_rpm          : REAL := 0.0;
    rVoted_CrankAngle_degCA         : REAL := 0.0;
    rVoted_GasRailPress_bar         : REAL := 300.0;
    rVoted_ScavAirPress_bar         : REAL := 1.013;
    rVoted_ScavAirTemp_degC         : REAL := 35.0;
    rVoted_SCR_InletTemp_degC       : REAL := 340.0;
    rVoted_CEMS_NOx_ppm             : REAL := 35.0;

    (* Sensor Discrepancy Allowable Tolerances *)
    rTol_Speed_rpm                  : REAL := 2.5;      (* Max allowable deviation among speed sensors [rpm] *)
    rTol_Angle_degCA                : REAL := 1.5;      (* Max allowable resolver phase angle discrepancy [deg] *)
    rTol_GasPress_bar               : REAL := 12.0;     (* Max allowable gas rail pressure transmitter spread [bar] *)
    rTol_ScavPress_bar              : REAL := 0.25;     (* Max allowable scavenge receiver pressure spread [bar] *)
    rTol_ScavTemp_degC              : REAL := 4.0;      (* Max allowable scavenge air temperature spread [deg C] *)
    rTol_SCR_Temp_degC              : REAL := 15.0;     (* Max allowable SCR inlet exhaust thermocouple spread [deg C] *)
    rTol_CEMS_NOx_ppm               : REAL := 18.0;     (* Max allowable stack NOx analyzer spread [ppm] *)

    (* Stuck Sensor Frozen Value Counters *)
    iStuckCnt_Speed_A : INT := 0; iStuckCnt_Speed_B : INT := 0; iStuckCnt_Speed_C : INT := 0;
    iStuckCnt_Angle_A : INT := 0; iStuckCnt_Angle_B : INT := 0; iStuckCnt_Angle_C : INT := 0;
    iStuckCnt_GasP_A  : INT := 0; iStuckCnt_GasP_B  : INT := 0; iStuckCnt_GasP_C  : INT := 0;
    iStuckCnt_ScavP_A : INT := 0; iStuckCnt_ScavP_B : INT := 0; iStuckCnt_ScavP_C : INT := 0;
    iStuckCnt_SCRT_A  : INT := 0; iStuckCnt_SCRT_B  : INT := 0; iStuckCnt_SCRT_C  : INT := 0;
    iStuckCnt_NOx_A   : INT := 0; iStuckCnt_NOx_B   : INT := 0; iStuckCnt_NOx_C   : INT := 0;

    (* Previous Scan Telemetry for Derivative / Frozen Tracking *)
    rPrev_Speed_A : REAL := 0.0; rPrev_Speed_B : REAL := 0.0; rPrev_Speed_C : REAL := 0.0;
    rPrev_Angle_A : REAL := 0.0; rPrev_Angle_B : REAL := 0.0; rPrev_Angle_C : REAL := 0.0;
    rPrev_GasP_A  : REAL := 300.0; rPrev_GasP_B  : REAL := 300.0; rPrev_GasP_C  : REAL := 300.0;
    rPrev_ScavP_A : REAL := 1.013; rPrev_ScavP_B : REAL := 1.013; rPrev_ScavP_C : REAL := 1.013;
    rPrev_SCRT_A  : REAL := 340.0; rPrev_SCRT_B  : REAL := 340.0; rPrev_SCRT_C  : REAL := 340.0;
    rPrev_NOx_A   : REAL := 35.0;  rPrev_NOx_B   : REAL := 35.0;  rPrev_NOx_C   : REAL := 35.0;

    (* Health Validity Bits *)
    bHealth_Speed_A : BOOL := TRUE; bHealth_Speed_B : BOOL := TRUE; bHealth_Speed_C : BOOL := TRUE;
    bHealth_Angle_A : BOOL := TRUE; bHealth_Angle_B : BOOL := TRUE; bHealth_Angle_C : BOOL := TRUE;
    bHealth_GasP_A  : BOOL := TRUE; bHealth_GasP_B  : BOOL := TRUE; bHealth_GasP_C  : BOOL := TRUE;
    bHealth_ScavP_A : BOOL := TRUE; bHealth_ScavP_B : BOOL := TRUE; bHealth_ScavP_C : BOOL := TRUE;
    bHealth_SCRT_A  : BOOL := TRUE; bHealth_SCRT_B  : BOOL := TRUE; bHealth_SCRT_C  : BOOL := TRUE;
    bHealth_NOx_A   : BOOL := TRUE; bHealth_NOx_B   : BOOL := TRUE; bHealth_NOx_C   : BOOL := TRUE;

    (* TMR Degradation Status Bits *)
    bDegraded_Speed_1oo2 : BOOL := FALSE; bDegraded_Speed_1oo1 : BOOL := FALSE;
    bDegraded_GasP_1oo2  : BOOL := FALSE; bDegraded_GasP_1oo1  : BOOL := FALSE;
    bDegraded_ScavP_1oo2 : BOOL := FALSE; bDegraded_ScavP_1oo1 : BOOL := FALSE;
    bDegraded_SCRT_1oo2  : BOOL := FALSE; bDegraded_SCRT_1oo1  : BOOL := FALSE;
    bDegraded_NOx_1oo2   : BOOL := FALSE; bDegraded_NOx_1oo1   : BOOL := FALSE;

    (* ----------------------------------------------------------------------------------------- *)
    (* 3. 16x16 MULTIVARIABLE STATE-SPACE MATRICES & KALMAN OBSERVER ARRAYS                     *)
    (* ----------------------------------------------------------------------------------------- *)
    (* State Vector Definitions x[0..15]:
         x[0]  : Engine crankshaft rotational speed deviation Delta omega_e [rad/s]
         x[1]  : Shaft torsional angle twist Delta theta_shaft [rad]
         x[2]  : Propeller rotational speed in water wake Delta omega_p [rad/s]
         x[3]  : Scavenge air receiver manifold pressure Delta P_scav [bar]
         x[4]  : Scavenge air receiver temperature Delta T_scav [K]
         x[5]  : Exhaust gas manifold pressure upstream of SCR Delta P_exh [bar]
         x[6]  : Exhaust gas manifold temperature upstream of SCR Delta T_exh [K]
         x[7]  : SCR catalyst monolith substrate surface temperature Delta T_cat [K]
         x[8]  : SCR chemisorbed surface ammonia coverage fraction Delta theta_NH3 [-]
         x[9]  : Stack downstream tailpipe NOx concentration Delta C_NOx [ppm]
         x[10] : Stack downstream tailpipe unreacted ammonia slip Delta C_NH3 [ppm]
         x[11] : Turbocharger TC-1 rotor shaft speed Delta omega_tc1 [rad/s]
         x[12] : Turbocharger TC-2 rotor shaft speed Delta omega_tc2 [rad/s]
         x[13] : High-pressure common rail fuel gas pressure Delta P_gas [bar]
         x[14] : Cylinder average peak combustion pressure Delta P_max [bar]
         x[15] : Mean indicated engine propulsion torque Delta T_ind [kNm] *)
    aState_x                        : ARRAY[0..15] OF REAL;
    aState_x_hat                    : ARRAY[0..15] OF REAL;
    aState_x_pred                   : ARRAY[0..15] OF REAL;

    (* Manipulated Control Actuator Variables u[0..7]:
         u[0] : High-pressure common rail gas injection duration Delta m_gas [ms] (Base: 14.5 ms)
         u[1] : Micro-pilot diesel fuel injection quantity Delta m_pilot [mg] (Base: 125.0 mg)
         u[2] : Variable Exhaust Valve Closing timing Delta CA_VEC [deg CA] (Base: 25.0 deg ATDC)
         u[3] : High-pressure SCR urea dosing mass flow rate Delta m_dot_urea [kg/h] (Base: 85.0 kg/h)
         u[4] : Pre-SCR exhaust thermal bypass damper position Delta u_byp [%] (Base: 0.0%)
         u[5] : Twin VGT turbine nozzle guide vane position Delta u_VGT [%] (Base: 55.0%)
         u[6] : Scavenge air auxiliary electric blower speed Delta N_blow [rpm] (Base: 0.0 rpm)
         u[7] : FGSS high-pressure fuel gas rail pressure demand Delta P_gas_sp [bar] (Base: 300.0 bar)*)
    aControl_u                      : ARRAY[0..7] OF REAL;
    aControl_u_prev                 : ARRAY[0..7] OF REAL;
    aControl_du                     : ARRAY[0..7] OF REAL;
    aControl_u_base                 : ARRAY[0..7] OF REAL := [14.5, 125.0, 25.0, 85.0, 0.0, 55.0, 0.0, 300.0];

    (* Disturbance Inputs d[0..3]:
         d[0] : Propeller hydrodynamic wave encounter torque fluctuation Delta Q_wave [kNm]
         d[1] : Fuel gas methane number / Lower Heating Value variation Delta LHV [MJ/kg]
         d[2] : Ambient seawater cooling temperature fluctuation Delta T_sea [deg C]
         d[3] : Barometric ambient atmospheric pressure disturbance Delta P_baro [mbar] *)
    aDisturb_d                      : ARRAY[0..3] OF REAL;

    (* Controlled Plant Outputs y[0..7]:
         y[0] : Engine speed [rpm] (Setpoint: 75.0 to 84.0 rpm)
         y[1] : Specific NOx emission rate [g/kWh] (Setpoint: 3.20 g/kWh)
         y[2] : Stack ammonia slip [ppm] (Setpoint: <= 5.0 ppm)
         y[3] : SCR catalyst temperature [deg C] (Setpoint: 340.0 deg C, strictly > 310 deg C)
         y[4] : Scavenge air receiver absolute pressure [bar] (Setpoint: load dependent 1.8 - 4.2 bar)
         y[5] : High-pressure fuel gas common-rail pressure [bar] (Setpoint: 300.0 bar)
         y[6] : Maximum cylinder firing pressure P_max [bar] (Setpoint: <= 215.0 bar, hard limit 225.0)
         y[7] : Propeller delivered shaft propulsion power [MW] (Setpoint: demand based) *)
    aOutput_y                       : ARRAY[0..7] OF REAL;
    aOutput_y_sp                    : ARRAY[0..7] OF REAL;
    aOutput_y_error                 : ARRAY[0..7] OF REAL;

    (* Complete 16x16 Discrete System State Matrix A *)
    aMatrix_A                       : ARRAY[0..15, 0..15] OF REAL;
    (* 16x8 Input Actuator Coupling Matrix B *)
    aMatrix_B                       : ARRAY[0..15, 0..7] OF REAL;
    (* 8x16 Output Measurement Projection Matrix C *)
    aMatrix_C                       : ARRAY[0..7, 0..15] OF REAL;
    (* 8x8 Direct Feedthrough Matrix D *)
    aMatrix_D                       : ARRAY[0..7, 0..7] OF REAL;
    (* 16x4 Disturbance Coupling Matrix E *)
    aMatrix_E                       : ARRAY[0..15, 0..3] OF REAL;
    (* 16x8 Steady-State Multivariable Kalman Filter Observer Gain Matrix K_obs *)
    aMatrix_K_obs                   : ARRAY[0..15, 0..7] OF REAL;

    (* ----------------------------------------------------------------------------------------- *)
    (* 4. MODEL PREDICTIVE CONTROL (MPC) QUADRATIC COST OPTIMIZATION WEIGHTS                    *)
    (* ----------------------------------------------------------------------------------------- *)
    aWeight_Q                       : ARRAY[0..7] OF REAL := [95.0, 180.0, 120.0, 65.0, 45.0, 30.0, 85.0, 50.0];
    aWeight_R                       : ARRAY[0..7] OF REAL := [0.15, 0.40, 0.25, 0.08, 0.35, 0.12, 0.05, 0.02];
    aWeight_P                       : ARRAY[0..15] OF REAL;

    (* Actuator Slew Rate Bounds per Scan Interval *)
    aLimit_du_Max                   : ARRAY[0..7] OF REAL := [0.35, 8.0, 0.8, 4.5, 2.5, 2.0, 60.0, 3.5];
    aLimit_du_Min                   : ARRAY[0..7] OF REAL := [-0.35, -8.0, -0.8, -4.5, -2.5, -2.0, -60.0, -3.5];

    (* Actuator Absolute Physical Saturation Envelopes *)
    aLimit_u_Max                    : ARRAY[0..7] OF REAL := [24.0, 250.0, 45.0, 220.0, 100.0, 95.0, 1800.0, 325.0];
    aLimit_u_Min                    : ARRAY[0..7] OF REAL := [0.0, 30.0, 5.0, 0.0, 0.0, 10.0, 0.0, 240.0];

    (* Projected Gradient Optimization Temporary Registers *)
    aGrad_g                         : ARRAY[0..7] OF REAL;
    aHessian_diag                   : ARRAY[0..7] OF REAL;
    aStep_du                        : ARRAY[0..7] OF REAL;
    iIterQP                         : INT := 0;
    iMaxIterQP                      : INT := 16;
    rAlphaStep                      : REAL := 0.028;
    rGradNorm                       : REAL := 0.0;

    (* ----------------------------------------------------------------------------------------- *)
    (* 5. CYLINDER BALANCING, COMBUSTION MONITORING & ANTI-KNOCK ARRAYS                          *)
    (* ----------------------------------------------------------------------------------------- *)
    aCyl_Pmax_bar                   : ARRAY[1..11] OF REAL;
    aCyl_Texh_degC                  : ARRAY[1..11] OF REAL;
    aCyl_GasDurationTrim_ms         : ARRAY[1..11] OF REAL;
    aCyl_PilotMassTrim_mg           : ARRAY[1..11] OF REAL;
    aCyl_VEC_AngleTrim_degCA        : ARRAY[1..11] OF REAL;
    aCyl_KnockIntensity_Pct         : ARRAY[1..11] OF REAL;
    aCyl_IMEP_bar                   : ARRAY[1..11] OF REAL;
    rAvgCyl_Pmax_bar                : REAL := 185.0;
    rAvgCyl_Texh_degC               : REAL := 365.0;
    rMaxCyl_Pmax_bar                : REAL := 185.0;
    rMinCyl_Pmax_bar                : REAL := 185.0;
    iWorstImbalanceCyl              : INT := 1;
    bCylinderKnockDetected          : BOOL := FALSE;

    (* ----------------------------------------------------------------------------------------- *)
    (* 6. DECOUPLED GAIN-SCHEDULED PID CONTROLLERS (GRACEFUL DEGRADATION BACKUP)                 *)
    (* ----------------------------------------------------------------------------------------- *)
    rPID_Speed_Kp                   : REAL := 1.850;
    rPID_Speed_Ki                   : REAL := 0.120;
    rPID_Speed_Kd                   : REAL := 0.350;
    rPID_Speed_Integ                : REAL := 14.50;
    rPID_Speed_PrevErr              : REAL := 0.0;

    rPID_GasPress_Kp                : REAL := 0.450;
    rPID_GasPress_Ki                : REAL := 0.085;
    rPID_GasPress_Kd                : REAL := 0.050;
    rPID_GasPress_Integ             : REAL := 50.0;
    rPID_GasPress_PrevErr           : REAL := 0.0;

    rPID_SCR_Temp_Kp                : REAL := 1.250;
    rPID_SCR_Temp_Ki                : REAL := 0.025;
    rPID_SCR_Temp_Kd                : REAL := 0.400;
    rPID_SCR_Temp_Integ             : REAL := 0.0;
    rPID_SCR_Temp_PrevErr           : REAL := 0.0;

    rPID_Urea_Kp                    : REAL := 2.400;
    rPID_Urea_Ki                    : REAL := 0.180;
    rPID_Urea_Kd                    : REAL := 0.150;
    rPID_Urea_Integ                 : REAL := 85.0;
    rPID_Urea_PrevErr               : REAL := 0.0;

    (* ----------------------------------------------------------------------------------------- *)
    (* 7. 12-STAGE OPERATIONAL FINITE STATE MACHINE (FSM) VARIABLES                              *)
    (* ----------------------------------------------------------------------------------------- *)
    iFSM_State                      : INT := 0;         (* Current active operational state index [0..11] *)
    iFSM_PreviousState              : INT := 0;         (* Previous state index memory *)
    rStateTimer_s                   : REAL := 0.0;      (* Elapsed monotonic timer in current state [s] *)
    rAirStartRampTimer_s            : REAL := 0.0;      (* Compressed air starting cycle duration timer [s] *)
    rFGSS_PrecoolTimer_s            : REAL := 0.0;      (* Cryogenic piping pre-cooling stabilization timer [s] *)
    rDualFuelTransitionTimer_s      : REAL := 0.0;      (* Gas admission energy ramp transfer timer [s] *)
    rHarborDecelTimer_s             : REAL := 0.0;      (* Harbor manoeuvring deceleration slope timer [s] *)
    rFastGasBleedTimer_s            : REAL := 0.0;      (* Fast gas bleed-off blowdown duration timer [s] *)
    rEmergencyTripTimer_s           : REAL := 0.0;      (* Safety shutdown latch hold timer [s] *)
    iStartingAirFiringCyl           : INT := 1;         (* Current cylinder index on air starting distributor *)

    (* ----------------------------------------------------------------------------------------- *)
    (* 8. INTERMEDIATE HYDRODYNAMIC, THERMAL & SCR CALCULATIONS                                  *)
    (* ----------------------------------------------------------------------------------------- *)
    rCurrentAdvanceRatio_J          : REAL := 0.650;
    rEstimatedKQ                    : REAL := 0.0225;
    rHydrodynamicTorqueDemand_kNm   : REAL := 8520.0;
    rWaveTorqueOscillation_kNm      : REAL := 0.0;
    rTorqueLimitEnvelop_kNm         : REAL := 9200.0;
    rThermalExhaustFlow_kgh         : REAL := 485000.0;
    rSpecificFuelOilEquiv_gkWh      : REAL := 162.5;
    rExhaustSO3_Concentration_ppm   : REAL := 4.2;
    rCatalystEquilibriumABS_Temp_C  : REAL := 304.5;
    rEffectiveCompressionRatio      : REAL := 14.8;
    rInCylinderTrappedAirMass_kg    : REAL := 3.45;
    rScavengeEfficiencyEta          : REAL := 0.945;
    rTheoreticalUreaReq_kgh         : REAL := 78.4;
    rAmmoniaSlipRatio               : REAL := 0.05;
    rSlewRate_GasDuration           : REAL := 0.0;
    rSlewRate_PilotMass             : REAL := 0.0;
    rSlewRate_UreaFlow              : REAL := 0.0;

    (* Loop Counters and Temporary Matrix Registers *)
    iIdxRow                         : INT := 0;
    iIdxCol                         : INT := 0;
    iIdxK                           : INT := 0;
    iIdxCyl                         : INT := 0;
    rTmpSum                         : REAL := 0.0;
    rTmpVal                         : REAL := 0.0;
    rTmpGrad                        : REAL := 0.0;
    rTmpHess                        : REAL := 0.0;
END_VAR
""")

    # =========================================================================
    # 5. SECTION 1: SAFETY INTERLOCKS & FIRST-SCAN 16x16 MATRIX UNROLLING
    # =========================================================================
    parts.append("""
(* ============================================================================================= *)
(* SECTION 1: SIL-3 HARDWIRED SAFETY INTERLOCKS & FIRST-SCAN 16x16 MATRIX INITIALIZATION         *)
(* ============================================================================================= *)

(* Supervision of SIL-3 Emergency Stop Relay Circuit *)
IF NOT bEmergencyStopSIL3 THEN
    iFSM_State                  := 11;                  (* Force immediately to EMERGENCY_SHUTDOWN_TRIP *)
    rGasInjectionDuration_ms    := 0.0;                 (* Shut off common-rail gas injection instantly *)
    rPilotDieselDuration_ms     := 0.0;                 (* Shut off pilot diesel injection *)
    rSCR_UreaDosingFlow_kgh     := 0.0;                 (* Cut off aqueous urea dosing *)
    rSCR_ThermalBypassDamper_Pct:= 100.0;               (* Open SCR bypass damper fully *)
    rVGT_NozzlePosition_Pct     := 100.0;               (* Open turbocharger vanes fully for blowdown *)
    rAuxBlowerSpeedCmd_rpm_01   := 0.0;
    rAuxBlowerSpeedCmd_rpm_02   := 0.0;
    rFGSS_RailPressDemand_bar   := 0.0;                 (* Vent high-pressure gas rail *)
    rGasVentFastBleedValve_Pct  := 100.0;               (* Fast depressurization to vent mast *)
    bEngineRunning              := FALSE;
    bDualFuelModeActive         := FALSE;
    bDieselBackupModeActive     := FALSE;
    bTierIII_Compliant          := FALSE;
    bGasEmergencyVented         := TRUE;
    bSIL3_ShutdownTripped       := TRUE;
    dwSafetyInterlockWord       := 16#8000_0001;        (* Emergency Stop Activated *)
    dwAlarmStatusWord           := dwAlarmStatusWord OR 16#8000_0000; (* Bit 31: SIL-3 Emergency Stop Trip *)
    dwSystemStatusWord          := 16#0000_000B;        (* State 11 *)
    RETURN;
END_IF;

(* Master Enable Verification *)
IF NOT bMasterEnable THEN
    iFSM_State                  := 0;                   (* Engine Stopped / Standby *)
    rGasInjectionDuration_ms    := 0.0;
    rPilotDieselDuration_ms     := 0.0;
    rSCR_UreaDosingFlow_kgh     := 0.0;
    rSCR_ThermalBypassDamper_Pct:= 0.0;
    rVGT_NozzlePosition_Pct     := 25.0;
    rAuxBlowerSpeedCmd_rpm_01   := 0.0;
    rAuxBlowerSpeedCmd_rpm_02   := 0.0;
    rGasVentFastBleedValve_Pct  := 0.0;
    bEngineRunning              := FALSE;
    bDualFuelModeActive         := FALSE;
    bDieselBackupModeActive     := FALSE;
    bTierIII_Compliant          := FALSE;
    dwSystemStatusWord          := 16#0000_0000;
    RETURN;
END_IF;

(* First-Scan State-Space 16x16 Matrices Unrolling & Memory Initialization *)
IF NOT bFirstScanInitialized THEN
    (* ----------------------------------------------------------------------------------------- *)
    (* Complete 16x16 Discrete State Transition Matrix A (Ts = 0.020 s, Marine Propulsion Cycle) *)
    (* ----------------------------------------------------------------------------------------- *)
    (* Initialize all entries to zero first *)
    FOR iIdxRow := 0 TO 15 DO
        FOR iIdxCol := 0 TO 15 DO
            aMatrix_A[iIdxRow, iIdxCol] := 0.0;
        END_FOR;
    END_FOR;

    (* Row 0: Engine crankshaft speed dynamics d(omega_e)/dt *)
    aMatrix_A[0, 0] := 0.9885;  aMatrix_A[0, 1] := -0.0425; aMatrix_A[0, 2] := 0.0085;  aMatrix_A[0, 3] := 0.0125;
    aMatrix_A[0, 13] := 0.0018; aMatrix_A[0, 14] := 0.0145; aMatrix_A[0, 15] := 0.0385;

    (* Row 1: Shaft torsional angle twist d(theta_s)/dt *)
    aMatrix_A[1, 0] := 0.0195;  aMatrix_A[1, 1] := 0.9650;  aMatrix_A[1, 2] := -0.0195; aMatrix_A[1, 15] := 0.0012;

    (* Row 2: Propeller speed in wake d(omega_p)/dt *)
    aMatrix_A[2, 0] := 0.0045;  aMatrix_A[2, 1] := 0.0520;  aMatrix_A[2, 2] := 0.9785;  aMatrix_A[2, 15] := -0.0025;

    (* Row 3: Scavenge air receiver manifold pressure d(P_scav)/dt *)
    aMatrix_A[3, 0] := 0.0085;  aMatrix_A[3, 3] := 0.9420;  aMatrix_A[3, 4] := -0.0015; aMatrix_A[3, 11] := 0.0245;
    aMatrix_A[3, 12] := 0.0245;

    (* Row 4: Scavenge air receiver temperature d(T_scav)/dt *)
    aMatrix_A[4, 3] := 0.0180;  aMatrix_A[4, 4] := 0.9150;  aMatrix_A[4, 11] := 0.0085; aMatrix_A[4, 12] := 0.0085;

    (* Row 5: Exhaust gas manifold pressure upstream of SCR d(P_exh)/dt *)
    aMatrix_A[5, 0] := 0.0125;  aMatrix_A[5, 3] := 0.0085;  aMatrix_A[5, 5] := 0.9280;  aMatrix_A[5, 6] := 0.0022;
    aMatrix_A[5, 14] := 0.0320; aMatrix_A[5, 15] := 0.0185;

    (* Row 6: Exhaust gas manifold temperature d(T_exh)/dt *)
    aMatrix_A[6, 0] := -0.0085; aMatrix_A[6, 3] := -0.0150; aMatrix_A[6, 5] := 0.0065;  aMatrix_A[6, 6] := 0.9380;
    aMatrix_A[6, 14] := 0.0450; aMatrix_A[6, 15] := 0.0285;

    (* Row 7: SCR catalyst monolith surface temperature d(T_cat)/dt *)
    aMatrix_A[7, 5] := 0.0018;  aMatrix_A[7, 6] := 0.0450;  aMatrix_A[7, 7] := 0.9620;  aMatrix_A[7, 8] := -0.0012;

    (* Row 8: SCR chemisorbed ammonia surface coverage d(theta_NH3)/dt *)
    aMatrix_A[8, 6] := -0.0025; aMatrix_A[8, 7] := -0.0085; aMatrix_A[8, 8] := 0.8850;  aMatrix_A[8, 9] := -0.0185;

    (* Row 9: Stack downstream NOx concentration d(C_NOx)/dt *)
    aMatrix_A[9, 6] := 0.0350;  aMatrix_A[9, 7] := 0.0180;  aMatrix_A[9, 8] := -0.1450; aMatrix_A[9, 9] := 0.8120;
    aMatrix_A[9, 14] := 0.0650;

    (* Row 10: Stack unreacted ammonia slip d(C_NH3)/dt *)
    aMatrix_A[10, 7] := 0.0045; aMatrix_A[10, 8] := 0.0980; aMatrix_A[10, 9] := -0.0120; aMatrix_A[10, 10] := 0.7850;

    (* Row 11: Turbocharger TC-1 rotor shaft speed d(omega_tc1)/dt *)
    aMatrix_A[11, 5] := 0.0580; aMatrix_A[11, 6] := 0.0380; aMatrix_A[11, 11] := 0.9580;

    (* Row 12: Turbocharger TC-2 rotor shaft speed d(omega_tc2)/dt *)
    aMatrix_A[12, 5] := 0.0580; aMatrix_A[12, 6] := 0.0380; aMatrix_A[12, 12] := 0.9580;

    (* Row 13: High-pressure common rail fuel gas pressure d(P_gas)/dt *)
    aMatrix_A[13, 0] := -0.0055; aMatrix_A[13, 13] := 0.9850; aMatrix_A[13, 15] := -0.0085;

    (* Row 14: Cylinder peak combustion pressure d(P_max)/dt *)
    aMatrix_A[14, 0] := 0.0150; aMatrix_A[14, 3] := 0.0450; aMatrix_A[14, 13] := 0.0380; aMatrix_A[14, 14] := 0.7650;

    (* Row 15: Mean indicated engine torque d(T_ind)/dt *)
    aMatrix_A[15, 0] := -0.0120; aMatrix_A[15, 3] := 0.0280; aMatrix_A[15, 13] := 0.0220; aMatrix_A[15, 14] := 0.0850;
    aMatrix_A[15, 15] := 0.7850;

    (* ----------------------------------------------------------------------------------------- *)
    (* Complete 16x8 Input Actuator Coupling Matrix B                                            *)
    (* ----------------------------------------------------------------------------------------- *)
    FOR iIdxRow := 0 TO 15 DO
        FOR iIdxCol := 0 TO 7 DO
            aMatrix_B[iIdxRow, iIdxCol] := 0.0;
        END_FOR;
    END_FOR;

    (* u[0]: Gas Duration, u[1]: Pilot Mass, u[2]: VEC Angle, u[3]: Urea Flow,
       u[4]: SCR Bypass,   u[5]: VGT Vanes,   u[6]: Aux Blowers, u[7]: FGSS Pressure Demand *)
    aMatrix_B[0, 0] := 0.0485;  aMatrix_B[0, 1] := 0.0125;  aMatrix_B[0, 2] := -0.0085;
    aMatrix_B[1, 0] := 0.0085;  aMatrix_B[1, 1] := 0.0025;
    aMatrix_B[3, 5] := 0.0280;  aMatrix_B[3, 6] := 0.0420;
    aMatrix_B[4, 5] := 0.0095;  aMatrix_B[4, 6] := 0.0150;
    aMatrix_B[5, 0] := 0.0320;  aMatrix_B[5, 2] := 0.0180;  aMatrix_B[5, 4] := -0.0120; aMatrix_B[5, 5] := -0.0240;
    aMatrix_B[6, 0] := 0.0450;  aMatrix_B[6, 1] := 0.0150;  aMatrix_B[6, 2] := -0.0220; aMatrix_B[6, 4] := 0.0350;
    aMatrix_B[7, 4] := -0.0650;
    aMatrix_B[8, 3] := 0.0850;  aMatrix_B[8, 4] := -0.0180;
    aMatrix_B[9, 0] := 0.0280;  aMatrix_B[9, 1] := 0.0350;  aMatrix_B[9, 2] := -0.0480; aMatrix_B[9, 3] := -0.1850;
    aMatrix_B[9, 4] := 0.0950;
    aMatrix_B[10, 3] := 0.0620; aMatrix_B[10, 4] := -0.0150;
    aMatrix_B[11, 4] := -0.0250; aMatrix_B[11, 5] := 0.0850;
    aMatrix_B[12, 4] := -0.0250; aMatrix_B[12, 5] := 0.0850;
    aMatrix_B[13, 0] := -0.0450; aMatrix_B[13, 7] := 0.0850;
    aMatrix_B[14, 0] := 0.0950; aMatrix_B[14, 1] := 0.0420; aMatrix_B[14, 2] := -0.0620; aMatrix_B[14, 7] := 0.0150;
    aMatrix_B[15, 0] := 0.1150; aMatrix_B[15, 1] := 0.0350; aMatrix_B[15, 2] := -0.0180;

    (* ----------------------------------------------------------------------------------------- *)
    (* Complete 8x16 Output Measurement Projection Matrix C                                      *)
    (* ----------------------------------------------------------------------------------------- *)
    FOR iIdxRow := 0 TO 7 DO
        FOR iIdxCol := 0 TO 15 DO
            aMatrix_C[iIdxRow, iIdxCol] := 0.0;
        END_FOR;
    END_FOR;

    aMatrix_C[0, 0] := 9.5493;  (* rad/s to RPM: (60 / 2pi) = 9.5493 *)
    aMatrix_C[1, 9] := 0.0825;  (* Stack NOx ppm to g/kWh factor *)
    aMatrix_C[2, 10]:= 1.0000;  (* Ammonia slip ppm *)
    aMatrix_C[3, 7] := 1.0000;  (* Catalyst temp K to deg C offset *)
    aMatrix_C[4, 3] := 1.0000;  (* Scavenge air pressure bar *)
    aMatrix_C[5, 13]:= 1.0000;  (* Fuel gas rail pressure bar *)
    aMatrix_C[6, 14]:= 1.0000;  (* Cylinder peak firing pressure bar *)
    aMatrix_C[7, 15]:= 0.0084;  (* Torque kNm and speed to MW power factor *)

    (* ----------------------------------------------------------------------------------------- *)
    (* Complete 8x8 Direct Feedthrough Matrix D (Zero for Physical Inertial Plant)               *)
    (* ----------------------------------------------------------------------------------------- *)
    FOR iIdxRow := 0 TO 7 DO
        FOR iIdxCol := 0 TO 7 DO
            aMatrix_D[iIdxRow, iIdxCol] := 0.0;
        END_FOR;
    END_FOR;

    (* ----------------------------------------------------------------------------------------- *)
    (* Complete 16x4 Disturbance Coupling Matrix E                                               *)
    (* ----------------------------------------------------------------------------------------- *)
    FOR iIdxRow := 0 TO 15 DO
        FOR iIdxCol := 0 TO 3 DO
            aMatrix_E[iIdxRow, iIdxCol] := 0.0;
        END_FOR;
    END_FOR;

    (* d[0]: Wave Torque, d[1]: LHV, d[2]: Sea Temp, d[3]: Baro Pressure *)
    aMatrix_E[0, 0] := -0.0185;
    aMatrix_E[2, 0] := -0.0450;
    aMatrix_E[6, 1] := 0.0150;  aMatrix_E[6, 2] := 0.0085;
    aMatrix_E[14, 1] := 0.0250; aMatrix_E[14, 3] := 0.0050;
    aMatrix_E[15, 1] := 0.0380;

    (* ----------------------------------------------------------------------------------------- *)
    (* Complete 16x8 Steady-State Kalman Filter Gain Matrix K_obs                                *)
    (* ----------------------------------------------------------------------------------------- *)
    FOR iIdxRow := 0 TO 15 DO
        FOR iIdxCol := 0 TO 7 DO
            aMatrix_K_obs[iIdxRow, iIdxCol] := 0.0;
        END_FOR;
    END_FOR;

    aMatrix_K_obs[0, 0] := 0.2450;
    aMatrix_K_obs[1, 0] := 0.0480;
    aMatrix_K_obs[2, 0] := 0.1250;
    aMatrix_K_obs[3, 4] := 0.3200;
    aMatrix_K_obs[4, 4] := 0.0850;
    aMatrix_K_obs[5, 4] := 0.0650;
    aMatrix_K_obs[6, 3] := 0.0450;
    aMatrix_K_obs[7, 3] := 0.2800;
    aMatrix_K_obs[8, 2] := 0.0520; aMatrix_K_obs[8, 1] := -0.0380;
    aMatrix_K_obs[9, 1] := 0.3800;
    aMatrix_K_obs[10, 2]:= 0.4200;
    aMatrix_K_obs[11, 4]:= 0.1150;
    aMatrix_K_obs[12, 4]:= 0.1150;
    aMatrix_K_obs[13, 5]:= 0.3500;
    aMatrix_K_obs[14, 6]:= 0.2900;
    aMatrix_K_obs[15, 7]:= 0.2100; aMatrix_K_obs[15, 0] := 0.0850;

    (* Terminal State Penalty Matrix P *)
    FOR iIdxRow := 0 TO 15 DO
        aWeight_P[iIdxRow] := 25.0;
    END_FOR;
    aWeight_P[0] := 180.0; (* High penalty on speed error *)
    aWeight_P[9] := 250.0; (* High penalty on NOx violation *)
    aWeight_P[14] := 150.0;(* High penalty on peak firing pressure *)

    (* Initialize Control Vectors to Base Setpoints *)
    FOR iIdxCol := 0 TO 7 DO
        aControl_u[iIdxCol] := aControl_u_base[iIdxCol];
        aControl_u_prev[iIdxCol] := aControl_u_base[iIdxCol];
        aControl_du[iIdxCol] := 0.0;
    END_FOR;

    bFirstScanInitialized := TRUE;
END_IF;
""")

    # =========================================================================
    # 6. SECTION 2: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING
    # =========================================================================
    parts.append("""
(* ============================================================================================= *)
(* SECTION 2: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) VOTING & FAULT DETECTION ENGINES              *)
(* ============================================================================================= *)

(* --------------------------------------------------------------------------------------------- *)
(* 1. Engine Speed Magnetic Pickup Sensor Triplet (rEngineSpeed_rpm_A, B, C)                     *)
(* --------------------------------------------------------------------------------------------- *)
IF ABS(rEngineSpeed_rpm_A - rPrev_Speed_A) < 0.001 THEN iStuckCnt_Speed_A := iStuckCnt_Speed_A + 1; ELSE iStuckCnt_Speed_A := 0; END_IF;
IF ABS(rEngineSpeed_rpm_B - rPrev_Speed_B) < 0.001 THEN iStuckCnt_Speed_B := iStuckCnt_Speed_B + 1; ELSE iStuckCnt_Speed_B := 0; END_IF;
IF ABS(rEngineSpeed_rpm_C - rPrev_Speed_C) < 0.001 THEN iStuckCnt_Speed_C := iStuckCnt_Speed_C + 1; ELSE iStuckCnt_Speed_C := 0; END_IF;
rPrev_Speed_A := rEngineSpeed_rpm_A; rPrev_Speed_B := rEngineSpeed_rpm_B; rPrev_Speed_C := rEngineSpeed_rpm_C;

bHealth_Speed_A := (rEngineSpeed_rpm_A >= 0.0) AND (rEngineSpeed_rpm_A <= 120.0) AND (iStuckCnt_Speed_A < 300);
bHealth_Speed_B := (rEngineSpeed_rpm_B >= 0.0) AND (rEngineSpeed_rpm_B <= 120.0) AND (iStuckCnt_Speed_B < 300);
bHealth_Speed_C := (rEngineSpeed_rpm_C >= 0.0) AND (rEngineSpeed_rpm_C <= 120.0) AND (iStuckCnt_Speed_C < 300);

IF bHealth_Speed_A AND bHealth_Speed_B AND bHealth_Speed_C THEN
    bDegraded_Speed_1oo2 := FALSE; bDegraded_Speed_1oo1 := FALSE;
    (* True Median Selection Algorithm *)
    IF ((rEngineSpeed_rpm_A >= rEngineSpeed_rpm_B) AND (rEngineSpeed_rpm_A <= rEngineSpeed_rpm_C)) OR
       ((rEngineSpeed_rpm_A >= rEngineSpeed_rpm_C) AND (rEngineSpeed_rpm_A <= rEngineSpeed_rpm_B)) THEN
        rVoted_EngineSpeed_rpm := rEngineSpeed_rpm_A;
    ELSIF ((rEngineSpeed_rpm_B >= rEngineSpeed_rpm_A) AND (rEngineSpeed_rpm_B <= rEngineSpeed_rpm_C)) OR
          ((rEngineSpeed_rpm_B >= rEngineSpeed_rpm_C) AND (rEngineSpeed_rpm_B <= rEngineSpeed_rpm_A)) THEN
        rVoted_EngineSpeed_rpm := rEngineSpeed_rpm_B;
    ELSE
        rVoted_EngineSpeed_rpm := rEngineSpeed_rpm_C;
    END_IF;
    IF (ABS(rEngineSpeed_rpm_A - rEngineSpeed_rpm_B) > rTol_Speed_rpm) OR
       (ABS(rEngineSpeed_rpm_B - rEngineSpeed_rpm_C) > rTol_Speed_rpm) OR
       (ABS(rEngineSpeed_rpm_A - rEngineSpeed_rpm_C) > rTol_Speed_rpm) THEN
        dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0001; (* Speed Triplet Discrepancy *)
    END_IF;
ELSIF bHealth_Speed_A AND bHealth_Speed_B THEN
    bDegraded_Speed_1oo2 := TRUE; rVoted_EngineSpeed_rpm := (rEngineSpeed_rpm_A + rEngineSpeed_rpm_B) * 0.5;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0002;
ELSIF bHealth_Speed_A AND bHealth_Speed_C THEN
    bDegraded_Speed_1oo2 := TRUE; rVoted_EngineSpeed_rpm := (rEngineSpeed_rpm_A + rEngineSpeed_rpm_C) * 0.5;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0002;
ELSIF bHealth_Speed_B AND bHealth_Speed_C THEN
    bDegraded_Speed_1oo2 := TRUE; rVoted_EngineSpeed_rpm := (rEngineSpeed_rpm_B + rEngineSpeed_rpm_C) * 0.5;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0002;
ELSIF bHealth_Speed_A THEN
    bDegraded_Speed_1oo1 := TRUE; rVoted_EngineSpeed_rpm := rEngineSpeed_rpm_A;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0004;
ELSIF bHealth_Speed_B THEN
    bDegraded_Speed_1oo1 := TRUE; rVoted_EngineSpeed_rpm := rEngineSpeed_rpm_B;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0004;
ELSIF bHealth_Speed_C THEN
    bDegraded_Speed_1oo1 := TRUE; rVoted_EngineSpeed_rpm := rEngineSpeed_rpm_C;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0004;
ELSE
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0008; (* Total Speed Triplet Failure *)
    iFSM_State := 11; (* Trip to Emergency Stop *)
END_IF;

(* --------------------------------------------------------------------------------------------- *)
(* 2. High-Pressure Common-Rail Gas Pressure Transducers (rGasRailPress_bar_A, B, C)             *)
(* --------------------------------------------------------------------------------------------- *)
IF ABS(rGasRailPress_bar_A - rPrev_GasP_A) < 0.01 THEN iStuckCnt_GasP_A := iStuckCnt_GasP_A + 1; ELSE iStuckCnt_GasP_A := 0; END_IF;
IF ABS(rGasRailPress_bar_B - rPrev_GasP_B) < 0.01 THEN iStuckCnt_GasP_B := iStuckCnt_GasP_B + 1; ELSE iStuckCnt_GasP_B := 0; END_IF;
IF ABS(rGasRailPress_bar_C - rPrev_GasP_C) < 0.01 THEN iStuckCnt_GasP_C := iStuckCnt_GasP_C + 1; ELSE iStuckCnt_GasP_C := 0; END_IF;
rPrev_GasP_A := rGasRailPress_bar_A; rPrev_GasP_B := rGasRailPress_bar_B; rPrev_GasP_C := rGasRailPress_bar_C;

bHealth_GasP_A := (rGasRailPress_bar_A >= 0.0) AND (rGasRailPress_bar_A <= 380.0) AND (iStuckCnt_GasP_A < 200);
bHealth_GasP_B := (rGasRailPress_bar_B >= 0.0) AND (rGasRailPress_bar_B <= 380.0) AND (iStuckCnt_GasP_B < 200);
bHealth_GasP_C := (rGasRailPress_bar_C >= 0.0) AND (rGasRailPress_bar_C <= 380.0) AND (iStuckCnt_GasP_C < 200);

IF bHealth_GasP_A AND bHealth_GasP_B AND bHealth_GasP_C THEN
    bDegraded_GasP_1oo2 := FALSE; bDegraded_GasP_1oo1 := FALSE;
    IF ((rGasRailPress_bar_A >= rGasRailPress_bar_B) AND (rGasRailPress_bar_A <= rGasRailPress_bar_C)) OR
       ((rGasRailPress_bar_A >= rGasRailPress_bar_C) AND (rGasRailPress_bar_A <= rGasRailPress_bar_B)) THEN
        rVoted_GasRailPress_bar := rGasRailPress_bar_A;
    ELSIF ((rGasRailPress_bar_B >= rGasRailPress_bar_A) AND (rGasRailPress_bar_B <= rGasRailPress_bar_C)) OR
          ((rGasRailPress_bar_B >= rGasRailPress_bar_C) AND (rGasRailPress_bar_B <= rGasRailPress_bar_A)) THEN
        rVoted_GasRailPress_bar := rGasRailPress_bar_B;
    ELSE
        rVoted_GasRailPress_bar := rGasRailPress_bar_C;
    END_IF;
    IF (ABS(rGasRailPress_bar_A - rGasRailPress_bar_B) > rTol_GasPress_bar) OR
       (ABS(rGasRailPress_bar_B - rGasRailPress_bar_C) > rTol_GasPress_bar) OR
       (ABS(rGasRailPress_bar_A - rGasRailPress_bar_C) > rTol_GasPress_bar) THEN
        dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0010;
    END_IF;
ELSIF bHealth_GasP_A AND bHealth_GasP_B THEN
    bDegraded_GasP_1oo2 := TRUE; rVoted_GasRailPress_bar := (rGasRailPress_bar_A + rGasRailPress_bar_B) * 0.5;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0020;
ELSIF bHealth_GasP_A AND bHealth_GasP_C THEN
    bDegraded_GasP_1oo2 := TRUE; rVoted_GasRailPress_bar := (rGasRailPress_bar_A + rGasRailPress_bar_C) * 0.5;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0020;
ELSIF bHealth_GasP_B AND bHealth_GasP_C THEN
    bDegraded_GasP_1oo2 := TRUE; rVoted_GasRailPress_bar := (rGasRailPress_bar_B + rGasRailPress_bar_C) * 0.5;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0020;
ELSIF bHealth_GasP_A THEN
    bDegraded_GasP_1oo1 := TRUE; rVoted_GasRailPress_bar := rGasRailPress_bar_A;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0040;
ELSIF bHealth_GasP_B THEN
    bDegraded_GasP_1oo1 := TRUE; rVoted_GasRailPress_bar := rGasRailPress_bar_B;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0040;
ELSIF bHealth_GasP_C THEN
    bDegraded_GasP_1oo1 := TRUE; rVoted_GasRailPress_bar := rGasRailPress_bar_C;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0040;
ELSE
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0080; (* Gas Pressure Failure -> Instant Gas Trip *)
    IF bDualFuelModeActive THEN
        iFSM_State := 8; (* Transfer to Diesel Backup *)
    END_IF;
END_IF;

(* --------------------------------------------------------------------------------------------- *)
(* 3. Scavenge Air Receiver Pressure Transmitters (rScavAirPress_bar_A, B, C)                     *)
(* --------------------------------------------------------------------------------------------- *)
IF ABS(rScavAirPress_bar_A - rPrev_ScavP_A) < 0.001 THEN iStuckCnt_ScavP_A := iStuckCnt_ScavP_A + 1; ELSE iStuckCnt_ScavP_A := 0; END_IF;
IF ABS(rScavAirPress_bar_B - rPrev_ScavP_B) < 0.001 THEN iStuckCnt_ScavP_B := iStuckCnt_ScavP_B + 1; ELSE iStuckCnt_ScavP_B := 0; END_IF;
IF ABS(rScavAirPress_bar_C - rPrev_ScavP_C) < 0.001 THEN iStuckCnt_ScavP_C := iStuckCnt_ScavP_C + 1; ELSE iStuckCnt_ScavP_C := 0; END_IF;
rPrev_ScavP_A := rScavAirPress_bar_A; rPrev_ScavP_B := rScavAirPress_bar_B; rPrev_ScavP_C := rScavAirPress_bar_C;

bHealth_ScavP_A := (rScavAirPress_bar_A >= 0.5) AND (rScavAirPress_bar_A <= 5.5) AND (iStuckCnt_ScavP_A < 200);
bHealth_ScavP_B := (rScavAirPress_bar_B >= 0.5) AND (rScavAirPress_bar_B <= 5.5) AND (iStuckCnt_ScavP_B < 200);
bHealth_ScavP_C := (rScavAirPress_bar_C >= 0.5) AND (rScavAirPress_bar_C <= 5.5) AND (iStuckCnt_ScavP_C < 200);

IF bHealth_ScavP_A AND bHealth_ScavP_B AND bHealth_ScavP_C THEN
    bDegraded_ScavP_1oo2 := FALSE; bDegraded_ScavP_1oo1 := FALSE;
    IF ((rScavAirPress_bar_A >= rScavAirPress_bar_B) AND (rScavAirPress_bar_A <= rScavAirPress_bar_C)) OR
       ((rScavAirPress_bar_A >= rScavAirPress_bar_C) AND (rScavAirPress_bar_A <= rScavAirPress_bar_B)) THEN
        rVoted_ScavAirPress_bar := rScavAirPress_bar_A;
    ELSIF ((rScavAirPress_bar_B >= rScavAirPress_bar_A) AND (rScavAirPress_bar_B <= rScavAirPress_bar_C)) OR
          ((rScavAirPress_bar_B >= rScavAirPress_bar_C) AND (rScavAirPress_bar_B <= rScavAirPress_bar_A)) THEN
        rVoted_ScavAirPress_bar := rScavAirPress_bar_B;
    ELSE
        rVoted_ScavAirPress_bar := rScavAirPress_bar_C;
    END_IF;
ELSIF bHealth_ScavP_A AND bHealth_ScavP_B THEN
    bDegraded_ScavP_1oo2 := TRUE; rVoted_ScavAirPress_bar := (rScavAirPress_bar_A + rScavAirPress_bar_B) * 0.5;
ELSIF bHealth_ScavP_A AND bHealth_ScavP_C THEN
    bDegraded_ScavP_1oo2 := TRUE; rVoted_ScavAirPress_bar := (rScavAirPress_bar_A + rScavAirPress_bar_C) * 0.5;
ELSIF bHealth_ScavP_B AND bHealth_ScavP_C THEN
    bDegraded_ScavP_1oo2 := TRUE; rVoted_ScavAirPress_bar := (rScavAirPress_bar_B + rScavAirPress_bar_C) * 0.5;
ELSIF bHealth_ScavP_A THEN
    bDegraded_ScavP_1oo1 := TRUE; rVoted_ScavAirPress_bar := rScavAirPress_bar_A;
ELSIF bHealth_ScavP_B THEN
    bDegraded_ScavP_1oo1 := TRUE; rVoted_ScavAirPress_bar := rScavAirPress_bar_B;
ELSIF bHealth_ScavP_C THEN
    bDegraded_ScavP_1oo1 := TRUE; rVoted_ScavAirPress_bar := rScavAirPress_bar_C;
ELSE
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0800;
END_IF;

(* --------------------------------------------------------------------------------------------- *)
(* 4. SCR Reactor Pre-Catalyst Exhaust Temperature (rSCR_InletTemp_degC_A, B, C)                 *)
(* --------------------------------------------------------------------------------------------- *)
IF ABS(rSCR_InletTemp_degC_A - rPrev_SCRT_A) < 0.01 THEN iStuckCnt_SCRT_A := iStuckCnt_SCRT_A + 1; ELSE iStuckCnt_SCRT_A := 0; END_IF;
IF ABS(rSCR_InletTemp_degC_B - rPrev_SCRT_B) < 0.01 THEN iStuckCnt_SCRT_B := iStuckCnt_SCRT_B + 1; ELSE iStuckCnt_SCRT_B := 0; END_IF;
IF ABS(rSCR_InletTemp_degC_C - rPrev_SCRT_C) < 0.01 THEN iStuckCnt_SCRT_C := iStuckCnt_SCRT_C + 1; ELSE iStuckCnt_SCRT_C := 0; END_IF;
rPrev_SCRT_A := rSCR_InletTemp_degC_A; rPrev_SCRT_B := rSCR_InletTemp_degC_B; rPrev_SCRT_C := rSCR_InletTemp_degC_C;

bHealth_SCRT_A := (rSCR_InletTemp_degC_A >= 100.0) AND (rSCR_InletTemp_degC_A <= 550.0) AND (iStuckCnt_SCRT_A < 200);
bHealth_SCRT_B := (rSCR_InletTemp_degC_B >= 100.0) AND (rSCR_InletTemp_degC_B <= 550.0) AND (iStuckCnt_SCRT_B < 200);
bHealth_SCRT_C := (rSCR_InletTemp_degC_C >= 100.0) AND (rSCR_InletTemp_degC_C <= 550.0) AND (iStuckCnt_SCRT_C < 200);

IF bHealth_SCRT_A AND bHealth_SCRT_B AND bHealth_SCRT_C THEN
    bDegraded_SCRT_1oo2 := FALSE; bDegraded_SCRT_1oo1 := FALSE;
    IF ((rSCR_InletTemp_degC_A >= rSCR_InletTemp_degC_B) AND (rSCR_InletTemp_degC_A <= rSCR_InletTemp_degC_C)) OR
       ((rSCR_InletTemp_degC_A >= rSCR_InletTemp_degC_C) AND (rSCR_InletTemp_degC_A <= rSCR_InletTemp_degC_B)) THEN
        rVoted_SCR_InletTemp_degC := rSCR_InletTemp_degC_A;
    ELSIF ((rSCR_InletTemp_degC_B >= rSCR_InletTemp_degC_A) AND (rSCR_InletTemp_degC_B <= rSCR_InletTemp_degC_C)) OR
          ((rSCR_InletTemp_degC_B >= rSCR_InletTemp_degC_C) AND (rSCR_InletTemp_degC_B <= rSCR_InletTemp_degC_A)) THEN
        rVoted_SCR_InletTemp_degC := rSCR_InletTemp_degC_B;
    ELSE
        rVoted_SCR_InletTemp_degC := rSCR_InletTemp_degC_C;
    END_IF;
ELSIF bHealth_SCRT_A AND bHealth_SCRT_B THEN
    bDegraded_SCRT_1oo2 := TRUE; rVoted_SCR_InletTemp_degC := (rSCR_InletTemp_degC_A + rSCR_InletTemp_degC_B) * 0.5;
ELSIF bHealth_SCRT_A AND bHealth_SCRT_C THEN
    bDegraded_SCRT_1oo2 := TRUE; rVoted_SCR_InletTemp_degC := (rSCR_InletTemp_degC_A + rSCR_InletTemp_degC_C) * 0.5;
ELSIF bHealth_SCRT_B AND bHealth_SCRT_C THEN
    bDegraded_SCRT_1oo2 := TRUE; rVoted_SCR_InletTemp_degC := (rSCR_InletTemp_degC_B + rSCR_InletTemp_degC_C) * 0.5;
ELSIF bHealth_SCRT_A THEN
    bDegraded_SCRT_1oo1 := TRUE; rVoted_SCR_InletTemp_degC := rSCR_InletTemp_degC_A;
ELSIF bHealth_SCRT_B THEN
    bDegraded_SCRT_1oo1 := TRUE; rVoted_SCR_InletTemp_degC := rSCR_InletTemp_degC_B;
ELSIF bHealth_SCRT_C THEN
    bDegraded_SCRT_1oo1 := TRUE; rVoted_SCR_InletTemp_degC := rSCR_InletTemp_degC_C;
ELSE
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_8000;
END_IF;

(* --------------------------------------------------------------------------------------------- *)
(* 5. CEMS Tailpipe Stack NOx Gas Analyzers (rCEMS_NOx_ppm_A, B, C)                              *)
(* --------------------------------------------------------------------------------------------- *)
IF ABS(rCEMS_NOx_ppm_A - rPrev_NOx_A) < 0.01 THEN iStuckCnt_NOx_A := iStuckCnt_NOx_A + 1; ELSE iStuckCnt_NOx_A := 0; END_IF;
IF ABS(rCEMS_NOx_ppm_B - rPrev_NOx_B) < 0.01 THEN iStuckCnt_NOx_B := iStuckCnt_NOx_B + 1; ELSE iStuckCnt_NOx_B := 0; END_IF;
IF ABS(rCEMS_NOx_ppm_C - rPrev_NOx_C) < 0.01 THEN iStuckCnt_NOx_C := iStuckCnt_NOx_C + 1; ELSE iStuckCnt_NOx_C := 0; END_IF;
rPrev_NOx_A := rCEMS_NOx_ppm_A; rPrev_NOx_B := rCEMS_NOx_ppm_B; rPrev_NOx_C := rCEMS_NOx_ppm_C;

bHealth_NOx_A := (rCEMS_NOx_ppm_A >= 0.0) AND (rCEMS_NOx_ppm_A <= 1200.0) AND (iStuckCnt_NOx_A < 200);
bHealth_NOx_B := (rCEMS_NOx_ppm_B >= 0.0) AND (rCEMS_NOx_ppm_B <= 1200.0) AND (iStuckCnt_NOx_B < 200);
bHealth_NOx_C := (rCEMS_NOx_ppm_C >= 0.0) AND (rCEMS_NOx_ppm_C <= 1200.0) AND (iStuckCnt_NOx_C < 200);

IF bHealth_NOx_A AND bHealth_NOx_B AND bHealth_NOx_C THEN
    bDegraded_NOx_1oo2 := FALSE; bDegraded_NOx_1oo1 := FALSE;
    IF ((rCEMS_NOx_ppm_A >= rCEMS_NOx_ppm_B) AND (rCEMS_NOx_ppm_A <= rCEMS_NOx_ppm_C)) OR
       ((rCEMS_NOx_ppm_A >= rCEMS_NOx_ppm_C) AND (rCEMS_NOx_ppm_A <= rCEMS_NOx_ppm_B)) THEN
        rVoted_CEMS_NOx_ppm := rCEMS_NOx_ppm_A;
    ELSIF ((rCEMS_NOx_ppm_B >= rCEMS_NOx_ppm_A) AND (rCEMS_NOx_ppm_B <= rCEMS_NOx_ppm_C)) OR
          ((rCEMS_NOx_ppm_B >= rCEMS_NOx_ppm_C) AND (rCEMS_NOx_ppm_B <= rCEMS_NOx_ppm_A)) THEN
        rVoted_CEMS_NOx_ppm := rCEMS_NOx_ppm_B;
    ELSE
        rVoted_CEMS_NOx_ppm := rCEMS_NOx_ppm_C;
    END_IF;
ELSIF bHealth_NOx_A AND bHealth_NOx_B THEN
    bDegraded_NOx_1oo2 := TRUE; rVoted_CEMS_NOx_ppm := (rCEMS_NOx_ppm_A + rCEMS_NOx_ppm_B) * 0.5;
ELSIF bHealth_NOx_A AND bHealth_NOx_C THEN
    bDegraded_NOx_1oo2 := TRUE; rVoted_CEMS_NOx_ppm := (rCEMS_NOx_ppm_A + rCEMS_NOx_ppm_C) * 0.5;
ELSIF bHealth_NOx_B AND bHealth_NOx_C THEN
    bDegraded_NOx_1oo2 := TRUE; rVoted_CEMS_NOx_ppm := (rCEMS_NOx_ppm_B + rCEMS_NOx_ppm_C) * 0.5;
ELSIF bHealth_NOx_A THEN
    bDegraded_NOx_1oo1 := TRUE; rVoted_CEMS_NOx_ppm := rCEMS_NOx_ppm_A;
ELSIF bHealth_NOx_B THEN
    bDegraded_NOx_1oo1 := TRUE; rVoted_CEMS_NOx_ppm := rCEMS_NOx_ppm_B;
ELSIF bHealth_NOx_C THEN
    bDegraded_NOx_1oo1 := TRUE; rVoted_CEMS_NOx_ppm := rCEMS_NOx_ppm_C;
ELSE
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0008_0000;
END_IF;
""")

    # =========================================================================
    # 7. SECTION 3: PROPELLER HYDRODYNAMICS & HEAVY SEAS TORQUE DAMPING
    # =========================================================================
    parts.append("""
(* ============================================================================================= *)
(* SECTION 3: PROPELLER HYDRODYNAMICS & HEAVY SEAS TORQUE DAMPING MODEL                         *)
(* ============================================================================================= *)

(* Calculate Ship Speed of Advance V_a [m/s] *)
(* Conversion: 1 knot = 0.51444 m/s *)
rTmpVal := rShipSpeed_knots * 0.51444 * (1.0 - rNominalWakeFraction_w0);

(* Advance Ratio J = V_a / (n * D) *)
IF rVoted_EngineSpeed_rpm > 5.0 THEN
    rCurrentAdvanceRatio_J := rTmpVal / ((rVoted_EngineSpeed_rpm / 60.0) * rPropellerDiameter_m);
    IF rCurrentAdvanceRatio_J < 0.10 THEN rCurrentAdvanceRatio_J := 0.10; END_IF;
    IF rCurrentAdvanceRatio_J > 1.20 THEN rCurrentAdvanceRatio_J := 1.20; END_IF;
ELSE
    rCurrentAdvanceRatio_J := 0.10;
END_IF;
rPropellerAdvanceRatio_J := rCurrentAdvanceRatio_J;

(* Torque Coefficient K_Q(J) using Wageningen B-Series Linearized Approximation *)
rEstimatedKQ := rWageningen_KQ0 + (rWageningen_dKQ_dJ * rCurrentAdvanceRatio_J);
IF rEstimatedKQ < 0.012 THEN rEstimatedKQ := 0.012; END_IF;

(* Absorbed Propeller Torque Q_p = K_Q * rho * n^2 * D^5 [kNm] *)
rTmpVal := (rVoted_EngineSpeed_rpm / 60.0);
rHydrodynamicTorqueDemand_kNm := (rEstimatedKQ * rSeawaterDensity_kgm3 * (rTmpVal * rTmpVal) *
                                 (rPropellerDiameter_m * rPropellerDiameter_m * rPropellerDiameter_m *
                                  rPropellerDiameter_m * rPropellerDiameter_m)) / 1000.0;

(* Wave Encounter Induced Cyclic Torque Fluctuations (Heavy Seas State) *)
IF (rSignificantWaveHeight_m > 3.0) OR bRoughWeatherModeCmd THEN
    bRoughWeatherDampingOn := TRUE;
    (* First-order cyclic wave torque perturbation *)
    rWaveTorqueOscillation_kNm := 0.18 * rHydrodynamicTorqueDemand_kNm * (rSignificantWaveHeight_m / 6.0) *
                                 SIN(rWaveEncounterFreq_rads * rStateTimer_s);
    aDisturb_d[0] := rWaveTorqueOscillation_kNm;
ELSE
    bRoughWeatherDampingOn := FALSE;
    rWaveTorqueOscillation_kNm := 0.0;
    aDisturb_d[0] := 0.0;
END_IF;

(* CIMAC / MAN B&W Engine Load Envelope Torque Limiter *)
(* Max torque limit curve as function of engine speed: Q_lim(n) *)
IF rVoted_EngineSpeed_rpm > 20.0 THEN
    rTorqueLimitEnvelop_kNm := 8520.0 * (rVoted_EngineSpeed_rpm / 84.0) * 1.10; (* 110% Torque limit *)
    IF rTorqueLimitEnvelop_kNm > 9370.0 THEN rTorqueLimitEnvelop_kNm := 9370.0; END_IF;
ELSE
    rTorqueLimitEnvelop_kNm := 2500.0;
END_IF;

(* Measured Propeller Shaft Torque from Strain Gauges *)
rEngineBrakeTorque_kNm := rPropellerShaftTorque_kNm;
rEngineShaftPower_MW   := (rEngineBrakeTorque_kNm * (rVoted_EngineSpeed_rpm * 2.0 * 3.14159265 / 60.0)) / 1000.0;
""")

    # =========================================================================
    # 8. SECTION 4: 16-STATE DISCRETE STATE-SPACE PROPAGATION & KALMAN OBSERVER
    # =========================================================================
    parts.append("""
(* ============================================================================================= *)
(* SECTION 4: 16-STATE DISCRETE STATE-SPACE PROPAGATION & KALMAN OBSERVER                        *)
(* ============================================================================================= *)

(* Assemble Plant Measured Output Vector y_meas[0..7] *)
aOutput_y[0] := rVoted_EngineSpeed_rpm;
aOutput_y[1] := rCalculatedNOxSpecific_gkWh;
aOutput_y[2] := rCEMS_NH3_Slip_ppm;
aOutput_y[3] := rVoted_SCR_InletTemp_degC;
aOutput_y[4] := rVoted_ScavAirPress_bar;
aOutput_y[5] := rVoted_GasRailPress_bar;
aOutput_y[6] := rAvgCyl_Pmax_bar;
aOutput_y[7] := rEngineShaftPower_MW;

(* Compute Output Estimation Error: e_y = y_meas - C * x_pred *)
FOR iIdxRow := 0 TO 7 DO
    rTmpSum := 0.0;
    FOR iIdxCol := 0 TO 15 DO
        rTmpSum := rTmpSum + (aMatrix_C[iIdxRow, iIdxCol] * aState_x_pred[iIdxCol]);
    END_FOR;
    aOutput_y_error[iIdxRow] := aOutput_y[iIdxRow] - rTmpSum;
END_FOR;

(* Kalman State Correction: x_hat = x_pred + K_obs * (y_meas - C * x_pred) *)
FOR iIdxRow := 0 TO 15 DO
    rTmpSum := aState_x_pred[iIdxRow];
    FOR iIdxCol := 0 TO 7 DO
        rTmpSum := rTmpSum + (aMatrix_K_obs[iIdxRow, iIdxCol] * aOutput_y_error[iIdxCol]);
    END_FOR;
    aState_x_hat[iIdxRow] := rTmpSum;
    aState_x[iIdxRow]     := rTmpSum;
END_FOR;

(* Compute Actuator Step Move: du = u - u_prev *)
FOR iIdxCol := 0 TO 7 DO
    aControl_du[iIdxCol] := aControl_u[iIdxCol] - aControl_u_prev[iIdxCol];
END_FOR;

(* One-Step Ahead State Prediction: x_pred(k+1) = A * x_hat(k) + B * du(k) + E * d(k) *)
FOR iIdxRow := 0 TO 15 DO
    rTmpSum := 0.0;
    (* Matrix A multiplication *)
    FOR iIdxCol := 0 TO 15 DO
        rTmpSum := rTmpSum + (aMatrix_A[iIdxRow, iIdxCol] * aState_x_hat[iIdxCol]);
    END_FOR;
    (* Matrix B multiplication *)
    FOR iIdxCol := 0 TO 7 DO
        rTmpSum := rTmpSum + (aMatrix_B[iIdxRow, iIdxCol] * aControl_du[iIdxCol]);
    END_FOR;
    (* Matrix E disturbance multiplication *)
    FOR iIdxCol := 0 TO 3 DO
        rTmpSum := rTmpSum + (aMatrix_E[iIdxRow, iIdxCol] * aDisturb_d[iIdxCol]);
    END_FOR;
    aState_x_pred[iIdxRow] := rTmpSum;
END_FOR;
""")

    # =========================================================================
    # 9. SECTION 5: RECEDING-HORIZON MPC QUADRATIC OPTIMIZATION SOLVER
    # =========================================================================
    parts.append("""
(* ============================================================================================= *)
(* SECTION 5: RECEDING-HORIZON MPC QUADRATIC COST OPTIMIZATION SOLVER                           *)
(* ============================================================================================= *)

(* Assemble Setpoint Vector aOutput_y_sp[0..7] *)
aOutput_y_sp[0] := rBridgeTelegraphOrder_rpm;
aOutput_y_sp[1] := 3.20;    (* IMO Tier III strict target: 3.20 g/kWh *)
aOutput_y_sp[2] := 4.5;     (* Target NH3 slip <= 4.5 ppm *)
aOutput_y_sp[3] := 345.0;   (* Catalyst target temperature [deg C] *)
IF rVoted_EngineSpeed_rpm > 50.0 THEN
    aOutput_y_sp[4] := 1.20 + (2.80 * (rVoted_EngineSpeed_rpm / 84.0)); (* Scavenge air setpoint *)
ELSE
    aOutput_y_sp[4] := 1.50;
END_IF;
aOutput_y_sp[5] := 300.0;   (* Gas rail pressure demand: 300.0 bar *)
aOutput_y_sp[6] := 195.0;   (* Target peak combustion pressure *)
aOutput_y_sp[7] := rMCR_PowerRating_MW * (rVoted_EngineSpeed_rpm / 84.0);

(* MPC Quadratic Cost Projected Gradient Descent (Unrolled Iterations) *)
(* Minimize J = 0.5 * du^T * H * du + g^T * du subject to du_min <= du <= du_max *)
IF bMasterEnable AND bEngineRunning AND (iFSM_State >= 4) AND (iFSM_State <= 7) THEN
    (* Compute Linear Gradient Vector g = B^T * Q * (C * x_hat - y_sp) *)
    FOR iIdxRow := 0 TO 7 DO
        rTmpGrad := 0.0;
        rTmpHess := aWeight_R[iIdxRow]; (* Base Hessian diagonal from R *)
        FOR iIdxK := 0 TO 7 DO
            rTmpVal := (aOutput_y[iIdxK] - aOutput_y_sp[iIdxK]) * aWeight_Q[iIdxK];
            (* Accumulate projected gain through B and C *)
            rTmpGrad := rTmpGrad + (aMatrix_B[iIdxK, iIdxRow] * rTmpVal);
            rTmpHess := rTmpHess + (aMatrix_B[iIdxK, iIdxRow] * aMatrix_B[iIdxK, iIdxRow] * aWeight_Q[iIdxK]);
        END_FOR;
        aGrad_g[iIdxRow]       := rTmpGrad;
        aHessian_diag[iIdxRow] := rTmpHess;
        IF aHessian_diag[iIdxRow] < 0.05 THEN aHessian_diag[iIdxRow] := 0.05; END_IF;
    END_FOR;

    (* Projected Gradient Optimization Loop *)
    FOR iIterQP := 1 TO iMaxIterQP DO
        FOR iIdxCol := 0 TO 7 DO
            (* Newton-like gradient step: step = - grad / hessian *)
            aStep_du[iIdxCol] := - (aGrad_g[iIdxCol] / aHessian_diag[iIdxCol]) * rAlphaStep;

            (* Apply step update *)
            aControl_du[iIdxCol] := aControl_du[iIdxCol] + aStep_du[iIdxCol];

            (* Enforce Actuator Slew Rate Bounds [du_min, du_max] *)
            IF aControl_du[iIdxCol] > aLimit_du_Max[iIdxCol] THEN
                aControl_du[iIdxCol] := aLimit_du_Max[iIdxCol];
            ELSIF aControl_du[iIdxCol] < aLimit_du_Min[iIdxCol] THEN
                aControl_du[iIdxCol] := aLimit_du_Min[iIdxCol];
            END_IF;

            (* Enforce Absolute Amplitude Bounds [u_min, u_max] *)
            rTmpVal := aControl_u_prev[iIdxCol] + aControl_du[iIdxCol];
            IF rTmpVal > aLimit_u_Max[iIdxCol] THEN
                aControl_du[iIdxCol] := aLimit_u_Max[iIdxCol] - aControl_u_prev[iIdxCol];
            ELSIF rTmpVal < aLimit_u_Min[iIdxCol] THEN
                aControl_du[iIdxCol] := aLimit_u_Min[iIdxCol] - aControl_u_prev[iIdxCol];
            END_IF;
        END_FOR;
    END_FOR;

    (* Apply Optimal Control Move *)
    FOR iIdxCol := 0 TO 7 DO
        aControl_u[iIdxCol] := aControl_u_prev[iIdxCol] + aControl_du[iIdxCol];
    END_FOR;
    dwMPC_DiagnosticsWord := 16#0000_0001; (* MPC Active & Converged *)
ELSE
    (* Fallback to Gain-Scheduled Decoupled PID Governors *)
    (* PID Loop 1: Engine Speed Governor -> Fuel Injection Duration *)
    rTmpVal := aOutput_y_sp[0] - rVoted_EngineSpeed_rpm;
    rPID_Speed_Integ := rPID_Speed_Integ + (rPID_Speed_Ki * rTmpVal * tScanPeriod_s);
    IF rPID_Speed_Integ > 22.0 THEN rPID_Speed_Integ := 22.0; END_IF;
    IF rPID_Speed_Integ < 0.0  THEN rPID_Speed_Integ := 0.0;  END_IF;
    aControl_u[0] := (rPID_Speed_Kp * rTmpVal) + rPID_Speed_Integ +
                     (rPID_Speed_Kd * (rTmpVal - rPID_Speed_PrevErr) / tScanPeriod_s);
    rPID_Speed_PrevErr := rTmpVal;
    IF aControl_u[0] > aLimit_u_Max[0] THEN aControl_u[0] := aLimit_u_Max[0]; END_IF;
    IF aControl_u[0] < aLimit_u_Min[0] THEN aControl_u[0] := aLimit_u_Min[0]; END_IF;

    (* PID Loop 2: SCR Catalyst Temperature -> Bypass Damper *)
    rTmpVal := aOutput_y_sp[3] - rVoted_SCR_InletTemp_degC;
    rPID_SCR_Temp_Integ := rPID_SCR_Temp_Integ + (rPID_SCR_Temp_Ki * rTmpVal * tScanPeriod_s);
    IF rPID_SCR_Temp_Integ > 100.0 THEN rPID_SCR_Temp_Integ := 100.0; END_IF;
    IF rPID_SCR_Temp_Integ < 0.0   THEN rPID_SCR_Temp_Integ := 0.0;   END_IF;
    aControl_u[4] := (rPID_SCR_Temp_Kp * rTmpVal) + rPID_SCR_Temp_Integ;
    IF aControl_u[4] > 100.0 THEN aControl_u[4] := 100.0; END_IF;
    IF aControl_u[4] < 0.0   THEN aControl_u[4] := 0.0;   END_IF;

    (* PID Loop 3: Tailpipe NOx Control -> Urea Dosing Flow *)
    rTmpVal := rVoted_CEMS_NOx_ppm - 35.0; (* 35 ppm target *)
    rPID_Urea_Integ := rPID_Urea_Integ + (rPID_Urea_Ki * rTmpVal * tScanPeriod_s);
    IF rPID_Urea_Integ > 200.0 THEN rPID_Urea_Integ := 200.0; END_IF;
    IF rPID_Urea_Integ < 0.0   THEN rPID_Urea_Integ := 0.0;   END_IF;
    aControl_u[3] := (rPID_Urea_Kp * rTmpVal) + rPID_Urea_Integ;
    IF aControl_u[3] > aLimit_u_Max[3] THEN aControl_u[3] := aLimit_u_Max[3]; END_IF;
    IF aControl_u[3] < aLimit_u_Min[3] THEN aControl_u[3] := aLimit_u_Min[3]; END_IF;

    dwMPC_DiagnosticsWord := 16#0000_0002; (* Graceful Degradation PID Active *)
END_IF;

(* Save Control History for Derivative Tracking *)
FOR iIdxCol := 0 TO 7 DO
    aControl_u_prev[iIdxCol] := aControl_u[iIdxCol];
END_FOR;
""")

    # =========================================================================
    # 10. SECTION 6: CYLINDER-BY-CYLINDER INDIVIDUAL BALANCING & ANTI-KNOCK
    # =========================================================================
    parts.append("""
(* ============================================================================================= *)
(* SECTION 6: CYLINDER-BY-CYLINDER INDIVIDUAL BALANCING & ANTI-KNOCK SUPERVISION                 *)
(* ============================================================================================= *)

(* Unpack Individual Cylinder Firing Pressures & Exhaust Temperatures *)
aCyl_Pmax_bar[1]  := rCylPeakPress_bar_01; aCyl_Texh_degC[1]  := rCylExhTemp_degC_01;
aCyl_Pmax_bar[2]  := rCylPeakPress_bar_02; aCyl_Texh_degC[2]  := rCylExhTemp_degC_02;
aCyl_Pmax_bar[3]  := rCylPeakPress_bar_03; aCyl_Texh_degC[3]  := rCylExhTemp_degC_03;
aCyl_Pmax_bar[4]  := rCylPeakPress_bar_04; aCyl_Texh_degC[4]  := rCylExhTemp_degC_04;
aCyl_Pmax_bar[5]  := rCylPeakPress_bar_05; aCyl_Texh_degC[5]  := rCylExhTemp_degC_05;
aCyl_Pmax_bar[6]  := rCylPeakPress_bar_06; aCyl_Texh_degC[6]  := rCylExhTemp_degC_06;
aCyl_Pmax_bar[7]  := rCylPeakPress_bar_07; aCyl_Texh_degC[7]  := rCylExhTemp_degC_07;
aCyl_Pmax_bar[8]  := rCylPeakPress_bar_08; aCyl_Texh_degC[8]  := rCylExhTemp_degC_08;
aCyl_Pmax_bar[9]  := rCylPeakPress_bar_09; aCyl_Texh_degC[9]  := rCylExhTemp_degC_09;
aCyl_Pmax_bar[10] := rCylPeakPress_bar_10; aCyl_Texh_degC[10] := rCylExhTemp_degC_10;
aCyl_Pmax_bar[11] := rCylPeakPress_bar_11; aCyl_Texh_degC[11] := rCylExhTemp_degC_11;

(* Calculate Engine 11-Cylinder Average and Spread *)
rTmpSum := 0.0;
rMaxCyl_Pmax_bar := aCyl_Pmax_bar[1];
rMinCyl_Pmax_bar := aCyl_Pmax_bar[1];
FOR iIdxCyl := 1 TO 11 DO
    rTmpSum := rTmpSum + aCyl_Pmax_bar[iIdxCyl];
    IF aCyl_Pmax_bar[iIdxCyl] > rMaxCyl_Pmax_bar THEN
        rMaxCyl_Pmax_bar := aCyl_Pmax_bar[iIdxCyl];
        iWorstImbalanceCyl := iIdxCyl;
    END_IF;
    IF aCyl_Pmax_bar[iIdxCyl] < rMinCyl_Pmax_bar THEN
        rMinCyl_Pmax_bar := aCyl_Pmax_bar[iIdxCyl];
    END_IF;
END_FOR;
rAvgCyl_Pmax_bar := rTmpSum / 11.0;

(* Individual Cylinder Combustion Balancing & Knock Mitigation *)
bCylinderKnockDetected := FALSE;
FOR iIdxCyl := 1 TO 11 DO
    (* Peak Pressure Deviation from Mean *)
    rTmpVal := aCyl_Pmax_bar[iIdxCyl] - rAvgCyl_Pmax_bar;

    (* Closed-loop integral trim on gas injection duration: +/- 1.5 ms limit *)
    aCyl_GasDurationTrim_ms[iIdxCyl] := aCyl_GasDurationTrim_ms[iIdxCyl] - (0.005 * rTmpVal * tScanPeriod_s);
    IF aCyl_GasDurationTrim_ms[iIdxCyl] > 1.50 THEN aCyl_GasDurationTrim_ms[iIdxCyl] := 1.50; END_IF;
    IF aCyl_GasDurationTrim_ms[iIdxCyl] < -1.50 THEN aCyl_GasDurationTrim_ms[iIdxCyl] := -1.50; END_IF;

    (* Anti-Knock Supervision: Detect high pressure oscillations or excessive P_max *)
    IF aCyl_Pmax_bar[iIdxCyl] > 220.0 THEN
        aCyl_KnockIntensity_Pct[iIdxCyl] := (aCyl_Pmax_bar[iIdxCyl] - 220.0) * 15.0;
        IF aCyl_KnockIntensity_Pct[iIdxCyl] > 100.0 THEN aCyl_KnockIntensity_Pct[iIdxCyl] := 100.0; END_IF;
        bCylinderKnockDetected := TRUE;

        (* Instantaneous knock mitigation: retard gas injection & advance exhaust valve closing *)
        aCyl_GasDurationTrim_ms[iIdxCyl] := aCyl_GasDurationTrim_ms[iIdxCyl] - 0.80;
        aCyl_VEC_AngleTrim_degCA[iIdxCyl]:= -2.5; (* Lower effective compression ratio *)
    ELSE
        aCyl_KnockIntensity_Pct[iIdxCyl] := 0.0;
        aCyl_VEC_AngleTrim_degCA[iIdxCyl]:= 0.0;
    END_IF;
END_FOR;
""")

    # =========================================================================
    # 11. SECTION 7: HP-SCR CATALYST KINETICS & ABS DEPOSITION PREVENTION
    # =========================================================================
    parts.append("""
(* ============================================================================================= *)
(* SECTION 7: HP-SCR CATALYST KINETICS & AMMONIUM BISULFATE (ABS) DEPOSITION AVOIDANCE           *)
(* ============================================================================================= *)

(* Calculate Exhaust Gas Total Mass Flow Rate [kg/h] *)
(* Based on scavenge air receiver pressure, engine speed, and volumetric displacement *)
IF rVoted_EngineSpeed_rpm > 5.0 THEN
    rThermalExhaustFlow_kgh := (rEngineTotalDispl_m3 * (rVoted_EngineSpeed_rpm * 60.0) *
                               (rVoted_ScavAirPress_bar * 100000.0 / (287.05 * (rVoted_ScavAirTemp_degC + 273.15)))) *
                               rScavEfficiencyEta;
ELSE
    rThermalExhaustFlow_kgh := 50000.0;
END_IF;

(* Sulfur Trioxide (SO3) Partial Pressure Calculation *)
(* Typical heavy fuel / MGO sulfur content conversion to SO3 *)
rExhaustSO3_Concentration_ppm := 3.5 + (0.015 * rCalculatedNOxSpecific_gkWh);

(* Minimum Safe Equilibrium Temperature for Ammonium Bisulfate (ABS) Solidification *)
(* ln(P_NH3 * P_SO3) equilibrium boundary: T_min = B / (A - ln(P_NH3 * P_SO3)) *)
rTmpVal := (rCEMS_NH3_Slip_ppm * 0.000001) * (rExhaustSO3_Concentration_ppm * 0.000001);
IF rTmpVal > 1.0E-14 THEN
    rCatalystEquilibriumABS_Temp_C := (rABS_Antoine_B / (rABS_Antoine_A - LN(rTmpVal))) - 273.15;
ELSE
    rCatalystEquilibriumABS_Temp_C := 295.0;
END_IF;

(* Guarantee Hard Operational ABS Boundary Margin (at least 310.0 deg C) *)
IF rCatalystEquilibriumABS_Temp_C < rABS_CriticalMinTemp_degC THEN
    rCatalystEquilibriumABS_Temp_C := rABS_CriticalMinTemp_degC;
END_IF;

(* ABS Deposition Risk Index [0.0 to 1.0] *)
IF rVoted_SCR_InletTemp_degC < (rCatalystEquilibriumABS_Temp_C + 5.0) THEN
    rABS_DepositionRiskIndex := ( (rCatalystEquilibriumABS_Temp_C + 5.0) - rVoted_SCR_InletTemp_degC ) / 20.0;
    IF rABS_DepositionRiskIndex > 1.0 THEN rABS_DepositionRiskIndex := 1.0; END_IF;
    (* Force open SCR thermal bypass damper to protect catalyst bed from low-temp fouling *)
    IF rVoted_SCR_InletTemp_degC < rABS_CriticalMinTemp_degC THEN
        rSCR_ThermalBypassDamper_Pct := 100.0;
        dwAlarmStatusWord := dwAlarmStatusWord OR 16#0000_0100; (* ABS Fouling Risk Alarm *)
    END_IF;
ELSE
    rABS_DepositionRiskIndex := 0.0;
END_IF;

(* Real-Time Specific NOx Emission Calculation [g/kWh] *)
(* Formula: NOx [g/kWh] = (C_NOx [ppm] * M_NOx * m_dot_exh) / (P_shaft [kW] * M_exh) *)
IF rEngineShaftPower_MW > 2.0 THEN
    rCalculatedNOxSpecific_gkWh := (rVoted_CEMS_NOx_ppm * 0.000001 * rMolarMass_NOx_kgkmol * rThermalExhaustFlow_kgh) /
                                   (rEngineShaftPower_MW * 1000.0 * 0.02896);
    IF rCalculatedNOxSpecific_gkWh < 0.20 THEN rCalculatedNOxSpecific_gkWh := 0.20; END_IF;
ELSE
    rCalculatedNOxSpecific_gkWh := 3.40;
END_IF;

(* Check IMO Tier III Compliance Status *)
bTierIII_Compliant := (rCalculatedNOxSpecific_gkWh <= 3.40) AND (rCEMS_NH3_Slip_ppm <= 10.0);

(* DeNOx Catalytic Reduction Efficiency *)
IF rCalculatedNOxSpecific_gkWh > 0.10 THEN
    rSCR_DeNOxEfficiency_Pct := ((14.50 - rCalculatedNOxSpecific_gkWh) / 14.50) * 100.0;
    IF rSCR_DeNOxEfficiency_Pct > 98.5 THEN rSCR_DeNOxEfficiency_Pct := 98.5; END_IF;
    IF rSCR_DeNOxEfficiency_Pct < 0.0  THEN rSCR_DeNOxEfficiency_Pct := 0.0;  END_IF;
ELSE
    rSCR_DeNOxEfficiency_Pct := 0.0;
END_IF;
""")

    # =========================================================================
    # 12. SECTION 8: 12-STAGE OPERATIONAL FINITE STATE MACHINE (FSM)
    # =========================================================================
    parts.append("""
(* ============================================================================================= *)
(* SECTION 8: 12-STAGE OPERATIONAL FINITE STATE MACHINE (FSM)                                    *)
(* ============================================================================================= *)

rStateTimer_s := rStateTimer_s + tScanPeriod_s;

CASE iFSM_State OF
    0: (* STATE_TURNING_GEAR_JACKING_OIL *)
        (* Engine barred over at 0.2 RPM via electric turning gear with 250 bar jacking oil *)
        bEngineRunning              := FALSE;
        bEngineReadyForStart        := FALSE;
        bDualFuelModeActive         := FALSE;
        bDieselBackupModeActive     := FALSE;
        rGasInjectionDuration_ms    := 0.0;
        rPilotDieselDuration_ms     := 0.0;
        rSCR_UreaDosingFlow_kgh     := 0.0;
        rSCR_ThermalBypassDamper_Pct:= 100.0;
        rVGT_NozzlePosition_Pct     := 25.0;
        rAuxBlowerSpeedCmd_rpm_01   := 0.0;
        rAuxBlowerSpeedCmd_rpm_02   := 0.0;
        rGasVentFastBleedValve_Pct  := 0.0;

        IF (rJackingOilPress_bar >= 220.0) AND (rMainLubeOilPress_bar >= 3.5) AND
           NOT bTurningGearEngaged AND bIndicatorCocksOpen THEN
            iFSM_State := 1; (* Advance to Slow Turning Air Purge *)
            rStateTimer_s := 0.0;
        END_IF;

    1: (* STATE_SLOW_TURNING_AIR_PURGE *)
        (* Rotate crankshaft one full revolution on compressed air to clear hydraulic lock *)
        bEngineRunning              := FALSE;
        bEngineReadyForStart        := FALSE;
        rGasInjectionDuration_ms    := 0.0;
        rPilotDieselDuration_ms     := 0.0;
        rAuxBlowerSpeedCmd_rpm_01   := 600.0; (* Pre-scavenge air space *)
        rAuxBlowerSpeedCmd_rpm_02   := 600.0;

        IF (rStateTimer_s >= 25.0) AND (rVoted_EngineSpeed_rpm >= 8.0) THEN
            IF NOT bIndicatorCocksOpen THEN
                bEngineReadyForStart := TRUE;
                iFSM_State := 2; (* Advance to Diesel Mode Start & Speed Ramp *)
                rStateTimer_s := 0.0;
            END_IF;
        END_IF;

    2: (* STATE_DIESEL_MODE_AIR_START_RAMP *)
        (* Compressed starting air fires cylinders in order, diesel injectors ignite at 18 RPM *)
        bEngineRunning              := TRUE;
        bDieselBackupModeActive     := TRUE;
        bDualFuelModeActive         := FALSE;
        rPilotDieselDuration_ms     := aControl_u[1];
        rGasInjectionDuration_ms    := 0.0; (* Zero gas on start *)
        rGasEnergySharePercent      := 0.0;
        rSCR_ThermalBypassDamper_Pct:= 100.0; (* Warm up pre-SCR piping *)
        rAuxBlowerSpeedCmd_rpm_01   := 1450.0; (* Auxiliary blowers at full speed *)
        rAuxBlowerSpeedCmd_rpm_02   := 1450.0;

        IF (rVoted_EngineSpeed_rpm >= 45.0) AND (rStateTimer_s >= 60.0) THEN
            IF bFGSS_GasReadyPermissive THEN
                iFSM_State := 3; (* Advance to FGSS Cryogenic Pre-Cooling & Leak Test *)
                rStateTimer_s := 0.0;
            END_IF;
        END_IF;

    3: (* STATE_FGSS_CRYOGENIC_PRECOOL_LEAKTEST *)
        (* Nitrogen inert pressure decay leak test and cryogenic LNG pump chilldown *)
        bEngineRunning              := TRUE;
        bDieselBackupModeActive     := TRUE;
        bDualFuelModeActive         := FALSE;
        rPilotDieselDuration_ms     := aControl_u[1];
        rGasInjectionDuration_ms    := 0.0;
        rGasVentFastBleedValve_Pct  := 0.0;
        rFGSS_RailPressDemand_bar   := 300.0;

        IF (rStateTimer_s >= 45.0) AND (rDoubleWallPipeHydrocarbon_ppm < 5.0) AND
           (rVoted_GasRailPress_bar >= 285.0) THEN
            iFSM_State := 4; (* Advance to Dual-Fuel Transition Handshake *)
            rStateTimer_s := 0.0;
        END_IF;

    4: (* STATE_DUAL_FUEL_TRANSITION_HANDSHAKE *)
        (* Seamless bumpless transfer: ramp gas admission from 0% to 95% energy share *)
        bEngineRunning              := TRUE;
        bDieselBackupModeActive     := FALSE;
        bDualFuelModeActive         := TRUE;
        rDualFuelTransitionTimer_s  := rDualFuelTransitionTimer_s + tScanPeriod_s;

        (* Gradual S-curve ramp of gas injection duration *)
        rTmpVal := rDualFuelTransitionTimer_s / 60.0; (* 60-second ramp *)
        IF rTmpVal > 1.0 THEN rTmpVal := 1.0; END_IF;

        rGasInjectionDuration_ms    := aControl_u[0] * rTmpVal;
        rGasEnergySharePercent      := 98.5 * rTmpVal;
        rPilotDieselDuration_ms     := aControl_u[1] * (1.0 - (0.85 * rTmpVal));

        IF (rDualFuelTransitionTimer_s >= 60.0) AND (rVoted_GasRailPress_bar >= 290.0) THEN
            iFSM_State := 5; (* Steady-State LNG Diesel Mode Full Load *)
            rStateTimer_s := 0.0;
        END_IF;

    5: (* STATE_STEADY_STATE_LNG_DIESEL_FULL_LOAD *)
        (* Engine operating at high-pressure gas admission with micro-pilot MGO *)
        bEngineRunning              := TRUE;
        bDualFuelModeActive         := TRUE;
        bDieselBackupModeActive     := FALSE;
        rGasInjectionDuration_ms    := aControl_u[0] + aCyl_GasDurationTrim_ms[1];
        rPilotDieselDuration_ms     := aControl_u[1];
        rGasEnergySharePercent      := 98.5;
        rExhValveCloseAngle_degCA   := aControl_u[2] + aCyl_VEC_AngleTrim_degCA[1];
        rVGT_NozzlePosition_Pct     := aControl_u[5];

        (* Auxiliary blowers modulated off above 35% engine load *)
        IF rEngineShaftPower_MW > 26.25 THEN
            rAuxBlowerSpeedCmd_rpm_01 := 0.0;
            rAuxBlowerSpeedCmd_rpm_02 := 0.0;
        ELSE
            rAuxBlowerSpeedCmd_rpm_01 := 1200.0;
            rAuxBlowerSpeedCmd_rpm_02 := 1200.0;
        END_IF;

        (* Transitions *)
        IF bRoughWeatherModeCmd OR (rSignificantWaveHeight_m > 4.5) THEN
            iFSM_State := 6; (* Heavy Seas Damping Mode *)
            rStateTimer_s := 0.0;
        ELSIF (rVoted_SCR_InletTemp_degC >= 320.0) AND NOT (iFSM_PreviousState = 7) THEN
            iFSM_State := 7; (* Activate SCR Urea Dosing *)
            rStateTimer_s := 0.0;
        ELSIF bHarborManoeuvringCmd THEN
            iFSM_State := 9; (* Harbor Deceleration *)
            rStateTimer_s := 0.0;
        END_IF;

    6: (* STATE_HEAVY_SEAS_TORQUE_LIMITER_DAMPING *)
        (* Dynamic torque limiter prevents engine overspeed and turbocharger compressor surge *)
        bEngineRunning              := TRUE;
        bDualFuelModeActive         := TRUE;
        bRoughWeatherDampingOn      := TRUE;

        (* Clamp maximum gas injection duration to torque limit envelope *)
        rTmpVal := (rTorqueLimitEnvelop_kNm / 9370.0) * aLimit_u_Max[0];
        IF aControl_u[0] > rTmpVal THEN
            rGasInjectionDuration_ms := rTmpVal;
        ELSE
            rGasInjectionDuration_ms := aControl_u[0];
        END_IF;
        rPilotDieselDuration_ms     := aControl_u[1] * 1.15; (* Enhance pilot robustness in heavy seas *)

        IF NOT bRoughWeatherModeCmd AND (rSignificantWaveHeight_m <= 3.0) AND (rStateTimer_s >= 120.0) THEN
            iFSM_State := 5; (* Return to Normal Steady State *)
            rStateTimer_s := 0.0;
        END_IF;

    7: (* STATE_SCR_HEATING_UREA_DOSING_ACTIVE *)
        (* Closed-loop IMO Tier III catalytic NOx reduction with thermal ABS protection *)
        bEngineRunning              := TRUE;
        bDualFuelModeActive         := TRUE;
        rGasInjectionDuration_ms    := aControl_u[0];
        rPilotDieselDuration_ms     := aControl_u[1];
        rExhValveCloseAngle_degCA   := aControl_u[2];
        rSCR_UreaDosingFlow_kgh     := aControl_u[3];
        rSCR_ThermalBypassDamper_Pct:= aControl_u[4];

        IF rVoted_SCR_InletTemp_degC < rABS_CriticalMinTemp_degC THEN
            rSCR_UreaDosingFlow_kgh := 0.0; (* Cut off urea instantly to avoid ABS fouling *)
            iFSM_State := 5; (* Step back to heating mode *)
            rStateTimer_s := 0.0;
        END_IF;

    8: (* STATE_GAS_TRIP_TRANSFER_TO_DIESEL_BACKUP *)
        (* Instantaneous bumpless gas trip: fuel gas shutoff, diesel ramped within 1 cycle *)
        bEngineRunning              := TRUE;
        bDualFuelModeActive         := FALSE;
        bDieselBackupModeActive     := TRUE;
        rGasInjectionDuration_ms    := 0.0; (* Shut off gas admission immediately *)
        rGasEnergySharePercent      := 0.0;
        rGasVentFastBleedValve_Pct  := 100.0; (* Bleed high-pressure gas rail *)
        rPilotDieselDuration_ms     := aControl_u[0] * 1.45; (* Substitute full energy via MGO injectors *)

        IF (rStateTimer_s >= 30.0) AND (rVoted_GasRailPress_bar < 5.0) THEN
            rGasVentFastBleedValve_Pct := 0.0;
            IF bAcknowledgeAlarms AND bFGSS_GasReadyPermissive THEN
                iFSM_State := 3; (* Re-arm gas supply *)
                rStateTimer_s := 0.0;
            END_IF;
        END_IF;

    9: (* STATE_HARBOR_MANOEUVRING_DECELERATION *)
        (* Deceleration to Dead-Slow / Harbor speed on pure MGO backup fuel *)
        bEngineRunning              := TRUE;
        bDualFuelModeActive         := FALSE;
        bDieselBackupModeActive     := TRUE;
        rGasInjectionDuration_ms    := 0.0;
        rPilotDieselDuration_ms     := aControl_u[1];
        rGasEnergySharePercent      := 0.0;
        rSCR_UreaDosingFlow_kgh     := 0.0;
        rSCR_ThermalBypassDamper_Pct:= 100.0;
        rAuxBlowerSpeedCmd_rpm_01   := 1450.0; (* Keep blowers on full during manoeuvring *)
        rAuxBlowerSpeedCmd_rpm_02   := 1450.0;

        IF (rBridgeTelegraphOrder_rpm <= 0.0) AND (rVoted_EngineSpeed_rpm < 5.0) THEN
            iFSM_State := 0; (* Return to Stopped / Standby *)
            rStateTimer_s := 0.0;
        END_IF;

    10: (* STATE_EMERGENCY_FAST_GAS_BLEED_INERTING *)
        (* Gas double-block-and-bleed venting with inert nitrogen blowdown *)
        bEngineRunning              := TRUE;
        bDualFuelModeActive         := FALSE;
        bDieselBackupModeActive     := TRUE;
        rGasInjectionDuration_ms    := 0.0;
        rGasVentFastBleedValve_Pct  := 100.0;
        rFGSS_RailPressDemand_bar   := 0.0;
        bGasEmergencyVented         := TRUE;

        IF (rStateTimer_s >= 45.0) AND (rVoted_GasRailPress_bar < 2.0) THEN
            rGasVentFastBleedValve_Pct := 0.0;
            iFSM_State := 8; (* Latch in Diesel Backup *)
            rStateTimer_s := 0.0;
        END_IF;

    11: (* STATE_EMERGENCY_SHUTDOWN_TRIP_SIL3 *)
        (* Complete propulsion emergency shutdown trip: fuel index cut to zero *)
        bEngineRunning              := FALSE;
        bDualFuelModeActive         := FALSE;
        bDieselBackupModeActive     := FALSE;
        bTierIII_Compliant          := FALSE;
        bSIL3_ShutdownTripped       := TRUE;
        rGasInjectionDuration_ms    := 0.0;
        rPilotDieselDuration_ms     := 0.0;
        rSCR_UreaDosingFlow_kgh     := 0.0;
        rSCR_ThermalBypassDamper_Pct:= 100.0;
        rGasVentFastBleedValve_Pct  := 100.0;
        rAuxBlowerSpeedCmd_rpm_01   := 0.0;
        rAuxBlowerSpeedCmd_rpm_02   := 0.0;
        dwSafetyInterlockWord       := 16#8000_0002;

        IF bAcknowledgeAlarms AND bEmergencyStopSIL3 AND (rVoted_EngineSpeed_rpm < 1.0) THEN
            bSIL3_ShutdownTripped := FALSE;
            iFSM_State := 0; (* Reset to Standby *)
            rStateTimer_s := 0.0;
        END_IF;
END_CASE;

iFSM_PreviousState := iFSM_State;
""")

    # =========================================================================
    # 13. SECTION 9: ISA-18.2 ALARMS & BIT-PACKED STATUS TELEMETRY WORD
    # =========================================================================
    parts.append("""
(* ============================================================================================= *)
(* SECTION 9: ISA-18.2 MULTI-TIERED ALARM HIERARCHY & BIT-PACKED TELEMETRY REGISTERS             *)
(* ============================================================================================= *)

(* Initialize Alarms Register *)
dwAlarmStatusWord := 16#0000_0000;

(* Alarm 1: Engine Overspeed High-High Trip (>= 92.0 RPM, Nominal MCR: 84.0 RPM) *)
IF rVoted_EngineSpeed_rpm >= 92.0 THEN
    dwAlarmStatusWord := dwAlarmStatusWord OR 16#0000_0001; (* Bit 0: Overspeed HH Trip *)
    iFSM_State := 11;
ELSIF rVoted_EngineSpeed_rpm >= 88.0 THEN
    dwAlarmStatusWord := dwAlarmStatusWord OR 16#0000_0002; (* Bit 1: Overspeed H Warning *)
END_IF;

(* Alarm 2: Fuel Gas Common Rail Pressure Drop High-High Trip *)
IF bDualFuelModeActive AND (rVoted_GasRailPress_bar < 250.0) THEN
    dwAlarmStatusWord := dwAlarmStatusWord OR 16#0000_0004; (* Bit 2: Gas Rail Low-Low Trip *)
    iFSM_State := 8; (* Transfer to Diesel Backup *)
ELSIF bDualFuelModeActive AND (rVoted_GasRailPress_bar < 275.0) THEN
    dwAlarmStatusWord := dwAlarmStatusWord OR 16#0000_0008; (* Bit 3: Gas Rail Low Warning *)
END_IF;

(* Alarm 3: Cylinder Combustion Peak Pressure P_max High-High Trip *)
IF rMaxCyl_Pmax_bar >= 225.0 THEN
    dwAlarmStatusWord := dwAlarmStatusWord OR 16#0000_0010; (* Bit 4: Pmax High-High Trip *)
    IF bDualFuelModeActive THEN iFSM_State := 8; END_IF;
ELSIF rMaxCyl_Pmax_bar >= 218.0 THEN
    dwAlarmStatusWord := dwAlarmStatusWord OR 16#0000_0020; (* Bit 5: Pmax High Warning *)
END_IF;

(* Alarm 4: Double-Wall Fuel Gas Pipe Annulus Hydrocarbon Sniffer Leak *)
IF rDoubleWallPipeHydrocarbon_ppm >= 25.0 THEN
    dwAlarmStatusWord := dwAlarmStatusWord OR 16#0000_0040; (* Bit 6: Double-Wall Pipe Gas Leak HH Trip *)
    iFSM_State := 10; (* Emergency Fast Gas Bleed *)
ELSIF rDoubleWallPipeHydrocarbon_ppm >= 10.0 THEN
    dwAlarmStatusWord := dwAlarmStatusWord OR 16#0000_0080; (* Bit 7: Double-Wall Pipe Gas Leak Warning *)
END_IF;

(* Alarm 5: SCR Catalyst Temperature Low Ammonium Bisulfate (ABS) Risk *)
IF (rVoted_SCR_InletTemp_degC < rABS_CriticalMinTemp_degC) AND (iFSM_State = 7) THEN
    dwAlarmStatusWord := dwAlarmStatusWord OR 16#0000_0100; (* Bit 8: SCR Temp Low ABS Deposition Risk *)
END_IF;

(* Alarm 6: Crosshead Bearing Metal Overtemperature High-High Trip *)
IF rCrossheadBearingTempMax_degC >= 85.0 THEN
    dwAlarmStatusWord := dwAlarmStatusWord OR 16#0000_0200; (* Bit 9: Crosshead Bearing Temp HH Trip *)
    iFSM_State := 11;
ELSIF rCrossheadBearingTempMax_degC >= 78.0 THEN
    dwAlarmStatusWord := dwAlarmStatusWord OR 16#0000_0400; (* Bit 10: Crosshead Bearing Temp High Warning *)
END_IF;

(* Alarm 7: Main Lubricating Oil Header Pressure Low-Low Trip *)
IF rMainLubeOilPress_bar < 2.5 THEN
    dwAlarmStatusWord := dwAlarmStatusWord OR 16#0000_0800; (* Bit 11: Lube Oil Pressure LL Trip *)
    iFSM_State := 11;
ELSIF rMainLubeOilPress_bar < 3.2 THEN
    dwAlarmStatusWord := dwAlarmStatusWord OR 16#0000_1000; (* Bit 12: Lube Oil Pressure Low Warning *)
END_IF;

(* Alarm 8: Turbocharger Rotor Vibration High-High Trip *)
IF (rTC1_Vibration_mms >= 25.0) OR (rTC2_Vibration_mms >= 25.0) THEN
    dwAlarmStatusWord := dwAlarmStatusWord OR 16#0000_2000; (* Bit 13: Turbocharger Vibration HH Trip *)
    iFSM_State := 11;
END_IF;

(* Alarm 9: Scavenge Air Receiver Fire / Overtemperature Detection *)
IF rVoted_ScavAirTemp_degC >= 75.0 THEN
    dwAlarmStatusWord := dwAlarmStatusWord OR 16#0000_4000; (* Bit 14: Scavenge Fire High Temp Trip *)
    iFSM_State := 11;
END_IF;

(* Alarm 10: Stack Ammonia Slip Excessive Violation *)
IF rCEMS_NH3_Slip_ppm >= 15.0 THEN
    dwAlarmStatusWord := dwAlarmStatusWord OR 16#0000_8000; (* Bit 15: NH3 Slip High Warning *)
END_IF;

(* Construct Standardized 32-Bit System Operational Status Word *)
dwSystemStatusWord := 16#0000_0000;
dwSystemStatusWord := dwSystemStatusWord OR INT_TO_DWORD(iFSM_State);
IF bEngineRunning          THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0100; END_IF;
IF bDualFuelModeActive     THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0200; END_IF;
IF bDieselBackupModeActive THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0400; END_IF;
IF bTierIII_Compliant      THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0800; END_IF;
IF bRoughWeatherDampingOn  THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_1000; END_IF;
IF (rAuxBlowerSpeedCmd_rpm_01 > 100.0) THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_2000; END_IF;
IF (dwMPC_DiagnosticsWord = 16#0000_0001) THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_4000; END_IF;
IF (bDegraded_Speed_1oo2 OR bDegraded_GasP_1oo2) THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_8000; END_IF;

(* Calculate Actuator Physical Outputs and Fuel Flow Rates *)
rGasFuelMassFlow_kgh := (rGasInjectionDuration_ms / 14.5) * (rVoted_EngineSpeed_rpm / 84.0) * 4250.0;
rPilotDieselFlow_lh  := (rPilotDieselDuration_ms / 3.5) * (rVoted_EngineSpeed_rpm / 84.0) * 85.0;
rPilotDieselMassPerStroke_mg := rPilotDieselDuration_ms * 35.71;

(* Map Actuator Outputs *)
rExhValveOpenAngle_degCA := 68.0; (* Nominal exhaust valve opening crank angle *)
rGasInjectionStartAngle_degCA := 2.5; (* 2.5 deg BTDC *)
rFGSS_RailPressDemand_bar := aControl_u[7];
rScavAirPressureDemand_bar := aOutput_y_sp[4];

(* Indicated Thermal Efficiency Estimation *)
IF (rGasFuelMassFlow_kgh > 100.0) AND (rEngineShaftPower_MW > 5.0) THEN
    rIndicatedThermalEff_Pct := (rEngineShaftPower_MW * 3600.0) /
                                ((rGasFuelMassFlow_kgh * rFuelGasLHV_MJkg) + (rPilotDieselFlow_lh * 0.84 * 42.7)) * 100.0;
    IF rIndicatedThermalEff_Pct > 54.5 THEN rIndicatedThermalEff_Pct := 54.5; END_IF;
ELSE
    rIndicatedThermalEff_Pct := 49.5;
END_IF;

END_FUNCTION_BLOCK
""")

    return "".join(parts)

if __name__ == "__main__":
    st_code = generate_marine_engine_st()
    print("ST code character count:", len(st_code))

    prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.
You are instructed to CONSUME EXTREME TOKENS: make your output massively exhaustive, mathematically rigorous, and structurally pristine. Include complete state-space matrices (A, B, C, D), Model Predictive Control (MPC) quadratic cost approximation, 2oo3 TMR voting logic, complex alarm trees, and graceful degradation.

**Your assigned domain is: Marine & Heavy Shipbuilding: 75 MW Two-Stroke Crosshead Dual-Fuel (High-Pressure LNG/Diesel) Marine Engine with Common-Rail Gas Admission & Selective Catalytic Reduction (SCR)**

CRITICAL RULES:
1. CODE FENCE: Use TRIPLE backticks + iec-st (```iec-st).
2. STRUCTURE:
   a. First line: FUNCTION_BLOCK FB_Marine_TwoStroke_DualFuel_LNG_SCR
   b. VAR_INPUT ... END_VAR (min 8 typed inputs with physical units [rpm], [bar], [MW], [deg C], [kg/h], [deg], [l/h], [ppm], [%], [kNm])
   c. VAR_OUTPUT ... END_VAR (min 7 typed outputs with engineering units & status words)
   d. VAR ... END_VAR (internal state matrices, filter accumulators, 2oo3 voting vars)
   e. Multi-stage CASE machine with END_CASE;
   f. Last line: END_FUNCTION_BLOCK
3. LENGTH: Assistant content MUST be >= 3500 characters total (target 55,000 - 85,000+ chars). Maximize token usage with deep technical explanations, complex algorithms, and industrial reliability features. DO NOT TRIM OR ENFORCE AN UPPER BOUND LIMIT.
4. PARITY: Ensure 100% exact parity between IF and END_IF, CASE and END_CASE, FOR and END_FOR, WHILE and END_WHILE.
5. SAVE using isolated JSON format in data/swarm_raw/agent_7b1940ca.json.
6. REPLY with: EVOLUTION COMPLETE: Marine & Heavy Shipbuilding: 75 MW Two-Stroke Crosshead Dual-Fuel (High-Pressure LNG/Diesel) Marine Engine with Common-Rail Gas Admission & Selective Catalytic Reduction (SCR)"""

    full_output = f"```iec-st\n{st_code}\n```"
    record = {
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": full_output}
        ]
    }

    target_path = os.path.join("data", "swarm_raw", "agent_7b1940ca.json")
    with open(target_path, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)

    print(f"Successfully saved dataset record to {target_path}")
    print(f"Total assistant content size: {len(full_output)} characters")

