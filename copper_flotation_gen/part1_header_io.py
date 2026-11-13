# copper_flotation_gen/part1_header_io.py

def get_header_and_io():
    return """FUNCTION_BLOCK FB_Mining_Copper_FrothFlotation_PulpLevel_AirRecovery
(*
====================================================================================================
LUMINA CYBER-PHYSICAL AUTOMATION KERNEL - IEC 61131-3 STRUCTURED TEXT
DOMAIN: MINING & MINERAL EXTRACTION / HYDROMETALLURGICAL BENEFICIATION
PROCESS: 12-CELL INDUSTRIAL COPPER FROTH FLOTATION BANK - PULP LEVEL, AIR FLOW & RECOVERY OPTIMIZATION
SUBSYSTEMS:
  - 12-CELL INDUSTRIAL CASCADE (ROUGHER CELLS 1-4, CLEANER/MIDDLINGS CELLS 5-8, SCAVENGER CELLS 9-12)
  - HYDRAULICALLY COUPLED DART VALVES (1 TO 6) WITH HYDROSTATIC HEAD CROSS-COUPLING COMPENSATION
  - LOW-PRESSURE HIGH-VOLUME FORCED AERATION MANIFOLD (BLOWERS, ORIFICE DP, PIEZORESISTIVE SENSORS)
  - FROTH BED THICKNESS & OVERFLOW LIP DEPTH WEIR KINETICS (BUBBLE SURFACE AREA FLUX Sb = 6*Jg/d32)
  - CHEMICAL REAGENT DOSING: POTASSIUM AMYL XANTHATE (PAX) COLLECTOR & MIBC FROTHER METERING PUMPS
  - IN-STREAM X-RAY FLUORESCENCE (XRF) MULTI-STREAM CONTINUOUS COPPER/IRON/SILICA SLURRY ANALYZERS
  - TAILINGS NUCLEAR DENSITY GAUGES & CELL SANDING / MECHANICAL AGITATOR TORQUE OVERLOAD DETECTOR
  - 8-STATE FIRST-PRINCIPLES CYBER-PHYSICAL STATE-SPACE DYNAMICS OBSERVER (SAMPLE TIME Ts = 20 [ms])
  - RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) WITH PROJECTED GRADIENT DESCENT (PGD, 6 ITERATIONS)
  - 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING SUITE ACROSS 5 CRITICAL MEASUREMENT CHANNELS
  - DETERMINISTIC 14-STAGE FLOTATION BANK PRODUCTION FINITE STATE MACHINE (FSM, STATES 0 TO 13)
  - DART VALVE ANTI-STICTION CALCIFICATION DITHER & CELL BOTTOM SANDING PRE-TRIP JET FLUSH
  - ISA-18.2 MULTI-TIER PROCESS ALARM MATRIX (HH, H, L, LL) WITH 32-BIT BIT-PACKED TELEMETRY DWORDS
====================================================================================================
*)

VAR_INPUT
    (* Master System Commands & Plant Permissives *)
    bEnable                         : BOOL;         (* Master Execution Enable Command [-] *)
    bAutoCycleStart                 : BOOL;         (* Automatic 12-Cell Bank Flotation Sequence Start [-] *)
    bBankStop                       : BOOL;         (* Controlled Flotation Bank Slurry Run-Down Command [-] *)
    bEmergencyStop                  : BOOL;         (* Safety Cat-4 Emergency Hardwired Master Trip [-] *)
    bFaultReset                     : BOOL;         (* Process Fault & Trip Latch Acknowledge Reset [-] *)
    bAlarmAck                       : BOOL;         (* ISA-18.2 Alarm Pushbutton Silence & Acknowledge [-] *)
    bMpcManualOverride              : BOOL;         (* MPC Manual Actuator Override Permissive [-] *)
    bWaterFlushPermissive           : BOOL;         (* Fresh Water Flotation Flush Line Supply Permissive [-] *)
    bFrothWashWaterActive           : BOOL;         (* Concentrate Launder Froth Wash Spray Activation [-] *)
    bAirBlowerReady                 : BOOL;         (* Main Aeration Air Blower Skid Running & Ready [-] *)
    bTailingsGateOpenFeedback       : BOOL;         (* Downstream Tailings Box Isolation Gate Status [-] *)
    bThickenerReadyFeedback         : BOOL;         (* Downstream Concentrate Thickener Surge Permissive [-] *)

    (* Channel Group 1: Rougher Cell 1 Ultrasonic & Float Pulp Level Transmitters (2oo3 TMR) *)
    rPulpLevel_Cell1_1A_mm          : REAL;         (* Rougher Cell 1 Slurry Pulp Level Channel 1A [mm] *)
    rPulpLevel_Cell1_1B_mm          : REAL;         (* Rougher Cell 1 Slurry Pulp Level Channel 1B [mm] *)
    rPulpLevel_Cell1_1C_mm          : REAL;         (* Rougher Cell 1 Slurry Pulp Level Channel 1C [mm] *)

    (* Channel Group 1 Mid: Cleaner Cell 6 Mid-Bank Guided-Wave Radar Pulp Level Transmitters (2oo3 TMR) *)
    rPulpLevel_Cell6_1A_mm          : REAL;         (* Cleaner Cell 6 Slurry Pulp Level Channel 1A [mm] *)
    rPulpLevel_Cell6_1B_mm          : REAL;         (* Cleaner Cell 6 Slurry Pulp Level Channel 1B [mm] *)
    rPulpLevel_Cell6_1C_mm          : REAL;         (* Cleaner Cell 6 Slurry Pulp Level Channel 1C [mm] *)

    (* Channel Group 1 End: Scavenger Cell 12 Tailings Discharge Pulp Level Transmitters (2oo3 TMR) *)
    rPulpLevel_Cell12_1A_mm         : REAL;         (* Scavenger Cell 12 Slurry Pulp Level Channel 1A [mm] *)
    rPulpLevel_Cell12_1B_mm         : REAL;         (* Scavenger Cell 12 Slurry Pulp Level Channel 1B [mm] *)
    rPulpLevel_Cell12_1C_mm         : REAL;         (* Scavenger Cell 12 Slurry Pulp Level Channel 1C [mm] *)

    (* Channel Group 2: Froth Bed Thickness / Overflow Lip Depth Transmitters (2oo3 TMR) *)
    rFrothHeight_2A_mm              : REAL;         (* Cell 1-4 Overflow Froth Bed Depth Channel 2A [mm] *)
    rFrothHeight_2B_mm              : REAL;         (* Cell 1-4 Overflow Froth Bed Depth Channel 2B [mm] *)
    rFrothHeight_2C_mm              : REAL;         (* Cell 1-4 Overflow Froth Bed Depth Channel 2C [mm] *)

    (* Channel Group 3: Forced Aeration Orifice Differential Pressure / Superficial Gas Velocity (2oo3 TMR) *)
    rAirPress_Manifold_3A_kPa       : REAL;         (* Air Blower Manifold Differential Pressure Channel 3A [kPa] *)
    rAirPress_Manifold_3B_kPa       : REAL;         (* Air Blower Manifold Differential Pressure Channel 3B [kPa] *)
    rAirPress_Manifold_3C_kPa       : REAL;         (* Air Blower Manifold Differential Pressure Channel 3C [kPa] *)

    (* Channel Group 4: In-Stream XRF Slurry Analyzer Concentrate Copper Grade (2oo3 TMR) *)
    rXRF_ConcCu_4A_pct              : REAL;         (* Final Concentrate Copper Grade Channel 4A [% Cu] *)
    rXRF_ConcCu_4B_pct              : REAL;         (* Final Concentrate Copper Grade Channel 4B [% Cu] *)
    rXRF_ConcCu_4C_pct              : REAL;         (* Final Concentrate Copper Grade Channel 4C [% Cu] *)

    (* Channel Group 5: Scavenger Discharge Nuclear Slurry Density Gauges (2oo3 TMR) *)
    rTailings_Density_5A_gcc        : REAL;         (* Scavenger Cell 12 Slurry Specific Gravity 5A [g/cm3] *)
    rTailings_Density_5B_gcc        : REAL;         (* Scavenger Cell 12 Slurry Specific Gravity 5B [g/cm3] *)
    rTailings_Density_5C_gcc        : REAL;         (* Scavenger Cell 12 Slurry Specific Gravity 5C [g/cm3] *)

    (* Plant Feed Disturbances & Physical Slurry Properties *)
    rFeed_SlurryFlow_m3h            : REAL;         (* Flotation Bank Feed Slurry Inflow Rate [m3/h] *)
    rFeed_SolidsContent_pct         : REAL;         (* Ore Slurry Solids Mass Fraction [% solids] *)
    rFeed_CopperHeadGrade_pct       : REAL;         (* Feed Copper Elemental Grade [% Cu] *)
    rFeed_SlurryPH                  : REAL;         (* Feed Slurry Electrochemical Acidity/Alkalinity [-] *)
    rSlurry_Temperature_degC        : REAL;         (* Slurry Pulp Bulk Process Temperature [deg C] *)

    (* Mechanical Rotor Agitator Drive Feedback *)
    rAgitatorTorque_Cell1_Nm        : REAL;         (* Rougher Cell 1 Mechanical Agitator Drive Torque [Nm] *)
    rAgitatorTorque_Cell6_Nm        : REAL;         (* Cleaner Cell 6 Mechanical Agitator Drive Torque [Nm] *)
    rAgitatorTorque_Cell12_Nm       : REAL;         (* Scavenger Cell 12 Mechanical Agitator Drive Torque [Nm] *)
    rAgitatorCurrent_Cell1_A        : REAL;         (* Rougher Cell 1 Motor Stator Electrical Current [A] *)

    (* Actuator Position Feedback Signals *)
    rDartValve_PosFb_1_pct          : REAL;         (* Cell 1-2 Dart Valve Actual Position Feedback [%] *)
    rDartValve_PosFb_2_pct          : REAL;         (* Cell 3-4 Dart Valve Actual Position Feedback [%] *)
    rDartValve_PosFb_3_pct          : REAL;         (* Cell 5-6 Dart Valve Actual Position Feedback [%] *)
    rDartValve_PosFb_4_pct          : REAL;         (* Cell 7-8 Dart Valve Actual Position Feedback [%] *)
    rDartValve_PosFb_5_pct          : REAL;         (* Cell 9-10 Dart Valve Actual Position Feedback [%] *)
    rDartValve_PosFb_6_pct          : REAL;         (* Cell 11-12 Tailings Dart Valve Actual Position Feedback [%] *)
    rAirControlValve_PosFb_pct      : REAL;         (* Main Forced Aeration Flow Valve Position Feedback [%] *)
    rReagentPump_PaxSpeedFb_pct     : REAL;         (* PAX Collector Metering Dosing Pump Speed Feedback [%] *)
    rReagentPump_MibcSpeedFb_pct    : REAL;         (* MIBC Frother Metering Dosing Pump Speed Feedback [%] *)
END_VAR

VAR_OUTPUT
    (* Primary Modulating Control Actuators *)
    rDartValve_Cmd_1_pct            : REAL;         (* Cell 1-2 Inter-Cell Dart Valve Modulating Command [%] *)
    rDartValve_Cmd_2_pct            : REAL;         (* Cell 3-4 Inter-Cell Dart Valve Modulating Command [%] *)
    rDartValve_Cmd_3_pct            : REAL;         (* Cell 5-6 Inter-Cell Dart Valve Modulating Command [%] *)
    rDartValve_Cmd_4_pct            : REAL;         (* Cell 7-8 Inter-Cell Dart Valve Modulating Command [%] *)
    rDartValve_Cmd_5_pct            : REAL;         (* Cell 9-10 Inter-Cell Dart Valve Modulating Command [%] *)
    rDartValve_Cmd_6_pct            : REAL;         (* Cell 11-12 Tailings Discharge Dart Valve Command [%] *)
    rAirControlValve_Cmd_pct        : REAL;         (* Main Aeration Air Flow Control Valve Command [%] *)
    rReagentPump_PaxCmd_pct         : REAL;         (* PAX Xanthate Collector Metering Pump Speed Command [%] *)
    rReagentPump_MibcCmd_pct        : REAL;         (* MIBC Surfactant Frother Metering Pump Speed Command [%] *)
    rFrothWashWaterValve_Cmd_pct    : REAL;         (* Froth Bed Launder Gangue Wash Water Valve Command [%] *)

    (* Fast Discrete Auxiliary Actuation & Isolation Valves *)
    bTailingsEmergencyDumpValve     : BOOL;         (* Emergency Bottom Slurry Dump Gate Solenoid Actuation [-] *)
    bSanderUpBottomFlushSolenoid    : BOOL;         (* High-Pressure Pulp Bottom De-Sanding Jet Water Flush [-] *)
    bFeedDivertToTailingsDam        : BOOL;         (* Automatic Feed Divert Gate to Tailings Impoundment [-] *)
    bFrothCrowderPaddleMotorRun     : BOOL;         (* Mechanical Froth Lip Crowder Paddle Drive Command [-] *)
    bAirPurgeNonReturnValveOpen     : BOOL;         (* Aeration Sparger Slurry Anti-Ingress Air Purge Valve [-] *)

    (* First-Principles Cyber-Physical Observer Estimated States *)
    rEst_PulpLevel_Cell1_mm         : REAL;         (* Observer Estimated Rougher Cell 1 Pulp Level [mm] *)
    rEst_PulpLevel_Cell6_mm         : REAL;         (* Observer Estimated Cleaner Cell 6 Pulp Level [mm] *)
    rEst_PulpLevel_Cell12_mm        : REAL;         (* Observer Estimated Scavenger Cell 12 Pulp Level [mm] *)
    rEst_FrothThickness_mm          : REAL;         (* Observer Estimated Froth Bed Overflow Lip Depth [mm] *)
    rEst_AirHoldup_pct              : REAL;         (* Observer Estimated Slurry Gas Holdup Fraction [% vol] *)
    rEst_SuperficialGasVel_cms      : REAL;         (* Observer Estimated Superficial Gas Velocity Jg [cm/s] *)
    rEst_ConcentrateGrade_pct       : REAL;         (* Observer Estimated Copper Concentrate Grade [% Cu] *)
    rEst_CumulativeRecovery_pct     : REAL;         (* Observer Estimated Cumulative Copper Recovery [% Rec] *)

    (* Flotation Kinetics & Diagnostic Quality Metrics *)
    rCalc_BubbleSurfaceAreaFlux_s   : REAL;         (* Bubble Surface Area Flux Sb = 6*Jg/d32 [1/s] *)
    rCalc_FrothRecoveryFactor       : REAL;         (* True Flotation Froth Recovery Factor Alpha_f [-] *)
    rCalc_SandingSeverityIndex      : REAL;         (* Cell Slurry Sanding & Impeller Packing Risk Index [-] *)
    rMpc_QuadraticCostMetric        : REAL;         (* MPC Optimization Quadratic Objective Cost Value [-] *)
    iActiveFsmState                 : INT;          (* Deterministic Flotation State Machine Active State [0..13] *)

    (* 32-Bit Bit-Packed Telemetry & Diagnostic Status Words *)
    dwStatusWord1                   : DWORD;        (* Bank Operational Status & Actuator Subsystem Health Bits *)
    dwStatusWord2                   : DWORD;        (* 2oo3 TMR Voting Health & Observer Convergence Telemetry *)
    dwAlarmWord1                    : DWORD;        (* ISA-18.2 Critical Trips & Safety Interlocks (HH/LL) *)
    dwAlarmWord2                    : DWORD;        (* ISA-18.2 Process High/Low Deviations & Discrepancies (H/L) *)
    dwFirstOutWord                  : DWORD;        (* First-Out Latching Root Cause Fault Telemetry Code *)
END_VAR
"""
