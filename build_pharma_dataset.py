# -*- coding: utf-8 -*-
"""
Lumina Swarm V7 Max-Persona Generator
Domain: Biopharmaceutical & Advanced Nanomedicine Manufacturing
System: Continuous mRNA-Lipid Nanoparticle (mRNA-LNP) Encapsulation Unit
Function Block: FB_Pharma_mRNA_LNP_MicrofluidicMixer_DLS
"""
import os
import json
import uuid
import re

def build_full_st_code():
    sections = []

    # =========================================================================
    # SECTION 1: HEADER & DECLARATION
    # =========================================================================
    sec1 = r'''FUNCTION_BLOCK FB_Pharma_mRNA_LNP_MicrofluidicMixer_DLS
(*
========================================================================================================================
LUMINA CYBER-PHYSICAL AUTOMATION ENGINE - SYNTHETIC DATASET V7 MAX-PERSONA
BIOPHARMACEUTICAL & ADVANCED NANOMEDICINE MANUFACTURING DIVISION
CONTINUOUS mRNA-LIPID NANOPARTICLE (mRNA-LNP) FORMULATION & IN-LINE PURIFICATION SYSTEM
========================================================================================================================

SYSTEM SPECIFICATION & PROCESS TOPOLOGY:
  Continuous multi-stage nanomedicine synthesis skid for the manufacturing of mRNA-loaded lipid nanoparticles (LNPs)
  under strict cGMP Annex 1 / FDA 21 CFR Part 11 compliance. The system executes continuous turbulent/chaotic mixing,
  controlled nanoprecipitation nucleation, in-line biophysical qualification, tangential flow diafiltration, and
  rapid cryo-quench thermal stabilization.

  1. Staggered Herringbone Microfluidic Impingement Mixer (SHM):
     - Fluidic Channels: 300 um width x 130 um depth with asymmetric herringbone grooves (groove depth 40 um).
     - Phase A (Aqueous): mRNA transcript dissolved in 50 mM sodium acetate/citrate buffer (pH 4.0).
     - Phase B (Organic): Ionizable cationic lipid (e.g. SM-102 / ALC-0315), DSPC helper phospholipid, Cholesterol,
       and PEGylated lipid (DMG-PEG2000 / ALC-0159) dissolved in absolute anhydrous ethanol (100%).
     - Hydrodynamics: Total flow rate 12.0 to 36.0 mL/min, channel flow velocity 0.5 to 3.0 m/s, channel Reynolds
       number Re = 150 to 450, inducing chaotic advection via alternating Dean vortex pairs and helical cross-flows.
     - Flow Ratio: Regulated aqueous-to-ethanol ratio of 3:1 volumetric (yielding 25% ethanol final mixer concentration)
       to trigger rapid self-assembly / nanoprecipitation at supersaturation ratio S > 10.0 within mixing time < 3.0 ms.

  2. In-Line Multi-Angle Dynamic Light Scattering (DLS) & Photon Correlator Spectrometer:
     - Optical Engine: Triplex laser photodiode detector array at 90-degree and 173-degree backscatter geometry.
     - Photon Correlator: Hardware multichannel digital photon correlator evaluating normalized intensity autocorrelation
       function g2(tau) = 1 + beta * exp(-2 * Gamma * tau), where decay rate Gamma = D_trans * q^2.
     - Cumulants Inversion: Real-time cumulants algorithm resolving Z-average hydrodynamic diameter D_h [nm]
       via Stokes-Einstein equation (D_h = k_B * T / (3 * pi * eta * D_trans)) and Polydispersity Index (PDI = mu2 / Gamma^2).
     - Process Critical Quality Attributes (CQAs):
       * Target Mean Particle Diameter: 75.0 nm (+/- 3.0 nm spec window, absolute limits 65.0 - 85.0 nm).
       * Target Polydispersity Index: PDI < 0.10 (Action Limit: 0.10, Critical Rejection Limit: 0.12).
       * Encapsulation Efficiency (EE%): Evaluated via synchronized in-line multi-wavelength UV-Vis (260/280 nm) > 92.0%.

  3. Continuous In-Line Tangential Flow Filtration (TFF) Diafiltration Skid:
     - Membrane Cassette: Flat-sheet modified Polyethersulfone (mPES) ultrafiltration cassette, MWCO 100 kDa, 0.1 m2.
     - Hydrodynamic Control: Constant retentate recirculation flux with controlled Transmembrane Pressure (TMP).
       TMP = (P_feed + P_retentate) / 2 - P_permeate. Target TMP = 0.70 to 0.95 bar (70 - 95 kPa).
     - Diafiltration (Buffer Exchange): Continuous 10 diavolumes (DV) buffer exchange against physiological PBS
       (pH 7.4) buffer to deplete ethanol from 250,000 ppm down to < 50 ppm, halting Ostwald ripening and size drift.
     - Concentration Polarization: Real-time gel-polarization boundary layer estimator delta_gel [um] based on
       Darcy-Starling flux equation and film theory (J_v = k_mass * ln((C_gel - C_p) / (C_bulk - C_p))).

  4. Multi-Zone Solid-State Peltier Cryogenic Quench Heat Exchanger:
     - Thermoelectric Array: Multi-stage bismuth telluride (Bi2Te3) Peltier modules with high-density copper micro-channel
       heat sinks and recirculating secondary chilled glycol loop (-10.0 deg C).
     - Thermal Range: Quench retentate stream from ambient reaction temperature (20.0 deg C) down to +2.0 to +4.0 deg C,
       with cryogenic flash-freeze capability down to -20.0 deg C for frozen bulk drug substance storage.
     - Thermodynamic Modeling: Peltier heat balance equation: Q_cold = alpha * I * T_c - 0.5 * I^2 * R_e - K_th * (T_h - T_c).

  5. Advanced Mathematical Architecture:
     - 8x8 Discrete State-Space Propagation: x[k+1] = A * x[k] + B * u[k], y[k] = C * x[k] + D * u[k] at 5 ms cycle time (200 Hz).
     - Receding-Horizon Model Predictive Control (MPC): 5-step prediction horizon quadratic cost optimization minimizing
       particle diameter error, PDI variance, TMP drift, and Peltier temperature offset subject to dual syringe pump
       slew-rate constraints and actuator saturation limits.
     - 2oo3 Triple Modular Redundancy (TMR): Triplex voting on all mission-critical transmitters (AIT_DLS_401, AIT_PDI_402,
       PT_TFF_301, FT_AQUEOUS_101, FT_ETHANOL_102, TT_CRYO_501, AIT_RESIDUAL_ETHANOL_601) with discrepancy timers and bumpless degradation.
     - ISA-18.2 Alarm Hierarchy: 5-tier alarm matrix (HI_HI, HI, LO, LO_LO, ROC) with deadband hysteresis, anti-chatter
       integration debouncing, and packed 16-bit diagnostic status words.
     - Multi-Stage 12-State FSM: ISA-88 compliant batch execution sequence from WFI flush through encapsulation to CIP/SIP.
========================================================================================================================
*)
VAR_INPUT
    (* === MASTER AUTOMATION & SAFETY INTERLOCK SIGNALS === *)
    bMasterRunPermissive              : BOOL := FALSE;    (* Global Bioprocess Skid Master Run Permissive [BOOL] *)
    bEmergencyStopCircuit_NC          : BOOL := TRUE;     (* Dual-Channel Hardwired E-Stop Circuit Normally Closed [BOOL] *)
    bContainmentIntegrity_NC          : BOOL := TRUE;     (* Biosafety Isolator Glovebox Differential Pressure OK [BOOL] *)
    bResetFaultLatches                : BOOL := FALSE;    (* Operator Unified Fault Latch Reset and Alarm Acknowledge [BOOL] *)
    bAutoEncapsulationEnable          : BOOL := FALSE;    (* Closed-Loop Model Predictive Encapsulation Control Enable [BOOL] *)
    bDiafiltrationEnable              : BOOL := FALSE;    (* In-Line TFF Ethanol Stripping Diafiltration Enable [BOOL] *)
    bCryoQuenchEnable                 : BOOL := FALSE;    (* Multi-Zone Peltier Cryogenic Heat Exchanger Enable [BOOL] *)
    bSterilizationCycleReq            : BOOL := FALSE;    (* Automated SIP/CIP Sterilization Sequence Initiation [BOOL] *)

    (* === BIOPROCESS RECIPE SETPOINTS (CQA & CPP TARGETS) === *)
    rSet_TotalFlowRate_ml_min         : REAL := 24.0;     (* Recipe Total Fluidic Mixing Flow Rate [0.5..60.0 mL/min] *)
    rSet_FlowRatio_AqueousToEthanol   : REAL := 3.0;      (* Volumetric Ratio Aqueous Buffer : Organic Ethanol [2.0..5.0] *)
    rSet_TargetParticleDiam_nm        : REAL := 75.0;     (* Target LNP Z-Average Hydrodynamic Diameter [60.0..120.0 nm] *)
    rSet_MaxAllowablePDI              : REAL := 0.100;    (* Target Upper Threshold for Polydispersity Index [0.04..0.20] *)
    rSet_TFF_TargetTMP_bar            : REAL := 0.850;    (* TFF Optimal Transmembrane Pressure Setpoint [0.20..2.50 bar] *)
    rSet_CryoTemp_degC                : REAL := 2.0;      (* Cryo-Quench Product Outlet Temperature Setpoint [-25.0..10.0 deg C] *)
    rSet_DiafiltrationVolumes         : REAL := 10.0;     (* Number of Continuous Diavolumes for Complete EtOH Wash [5.0..15.0] *)
    rSet_MaxResidualEthanol_ppm       : REAL := 50.0;     (* Pharmacopoeial Residual Ethanol Limit in Product [< 50 ppm] *)
    rSet_MicrofluidicTargetPressure   : REAL := 2.80;     (* Microfluidic Channel Inlet Operating Pressure [1.0..6.0 bar] *)
    rSet_PermeateFlux_LMH             : REAL := 45.0;     (* Target TFF Permeate Flux [Liters / m2 / hour] *)

    (* === 2oo3 TRIPLEX PROCESS TRANSMITTERS: FLOW SENSORS === *)
    rFT_AQUEOUS_MRNA_101A             : REAL := 18.0;     (* Aqueous Phase Syringe Pump Coriolis Flowmeter 101A [mL/min] *)
    rFT_AQUEOUS_MRNA_101B             : REAL := 18.0;     (* Aqueous Phase Syringe Pump Coriolis Flowmeter 101B [mL/min] *)
    rFT_AQUEOUS_MRNA_101C             : REAL := 18.0;     (* Aqueous Phase Syringe Pump Coriolis Flowmeter 101C [mL/min] *)
    rFT_ETHANOL_LIPID_102A            : REAL := 6.0;      (* Ethanol Lipid Syringe Pump Coriolis Flowmeter 102A [mL/min] *)
    rFT_ETHANOL_LIPID_102B            : REAL := 6.0;      (* Ethanol Lipid Syringe Pump Coriolis Flowmeter 102B [mL/min] *)
    rFT_ETHANOL_LIPID_102C            : REAL := 6.0;      (* Ethanol Lipid Syringe Pump Coriolis Flowmeter 102C [mL/min] *)

    (* === 2oo3 TRIPLEX PROCESS TRANSMITTERS: PRESSURE SENSORS === *)
    rPT_MICROFLUIDIC_INLET_201A       : REAL := 2.80;     (* Microfluidic Mixer Inlet Pressure Transmitter 201A [bar] *)
    rPT_MICROFLUIDIC_INLET_201B       : REAL := 2.80;     (* Microfluidic Mixer Inlet Pressure Transmitter 201B [bar] *)
    rPT_MICROFLUIDIC_INLET_201C       : REAL := 2.80;     (* Microfluidic Mixer Inlet Pressure Transmitter 201C [bar] *)
    rPT_TFF_FEED_301A                 : REAL := 1.25;     (* TFF Cassette Feed Pressure Transmitter 301A [bar] *)
    rPT_TFF_FEED_301B                 : REAL := 1.25;     (* TFF Cassette Feed Pressure Transmitter 301B [bar] *)
    rPT_TFF_FEED_301C                 : REAL := 1.25;     (* TFF Cassette Feed Pressure Transmitter 301C [bar] *)
    rPT_TFF_RETENTATE_302A            : REAL := 0.85;     (* TFF Cassette Retentate Pressure Transmitter 302A [bar] *)
    rPT_TFF_RETENTATE_302B            : REAL := 0.85;     (* TFF Cassette Retentate Pressure Transmitter 302B [bar] *)
    rPT_TFF_RETENTATE_302C            : REAL := 0.85;     (* TFF Cassette Retentate Pressure Transmitter 302C [bar] *)
    rPT_TFF_PERMEATE_303A             : REAL := 0.20;     (* TFF Cassette Permeate Pressure Transmitter 303A [bar] *)
    rPT_TFF_PERMEATE_303B             : REAL := 0.20;     (* TFF Cassette Permeate Pressure Transmitter 303B [bar] *)
    rPT_TFF_PERMEATE_303C             : REAL := 0.20;     (* TFF Cassette Permeate Pressure Transmitter 303C [bar] *)

    (* === 2oo3 TRIPLEX PROCESS TRANSMITTERS: IN-LINE BIOPHYSICAL & DLS SENSORS === *)
    rAIT_DLS_PARTICLE_DIAMETER_401A   : REAL := 75.0;     (* Multi-Angle DLS Particle Hydrodynamic Diameter Channel A [nm] *)
    rAIT_DLS_PARTICLE_DIAMETER_401B   : REAL := 75.0;     (* Multi-Angle DLS Particle Hydrodynamic Diameter Channel B [nm] *)
    rAIT_DLS_PARTICLE_DIAMETER_401C   : REAL := 75.0;     (* Multi-Angle DLS Particle Hydrodynamic Diameter Channel C [nm] *)
    rAIT_DLS_PDI_402A                 : REAL := 0.080;    (* DLS Polydispersity Index Photon Correlator Channel A [-] *)
    rAIT_DLS_PDI_402B                 : REAL := 0.080;    (* DLS Polydispersity Index Photon Correlator Channel B [-] *)
    rAIT_DLS_PDI_402C                 : REAL := 0.080;    (* DLS Polydispersity Index Photon Correlator Channel C [-] *)

    (* === 2oo3 TRIPLEX PROCESS TRANSMITTERS: THERMAL & ANALYTICAL SENSORS === *)
    rTT_CRYO_PELTIER_501A             : REAL := 2.0;      (* Cryogenic Quench Micro-Heat Exchanger RTD Probe 501A [deg C] *)
    rTT_CRYO_PELTIER_501B             : REAL := 2.0;      (* Cryogenic Quench Micro-Heat Exchanger RTD Probe 501B [deg C] *)
    rTT_CRYO_PELTIER_501C             : REAL := 2.0;      (* Cryogenic Quench Micro-Heat Exchanger RTD Probe 501C [deg C] *)
    rAIT_RESIDUAL_ETHANOL_601A        : REAL := 25.0;     (* In-Line Gas Chromatography / Raman Ethanol Sensor 601A [ppm] *)
    rAIT_RESIDUAL_ETHANOL_601B        : REAL := 25.0;     (* In-Line Gas Chromatography / Raman Ethanol Sensor 601B [ppm] *)
    rAIT_RESIDUAL_ETHANOL_601C        : REAL := 25.0;     (* In-Line Gas Chromatography / Raman Ethanol Sensor 601C [ppm] *)

    (* === AUXILIARY ANALYTICAL & SYSTEM SENSORS === *)
    rAIT_UV260_MRNA_CONC_701A         : REAL := 1.25;     (* In-Line Dual-Wavelength UV Absorbance Spectrophotometer 260 nm [mg/mL] *)
    rAIT_UV280_LIPID_CONC_702A        : REAL := 3.75;     (* In-Line Dual-Wavelength UV Absorbance Spectrophotometer 280 nm [mg/mL] *)
    rTT_MICROFLUIDIC_CHIP_202         : REAL := 20.0;     (* Microfluidic Mixer Glass Chip Body Temperature RTD [deg C] *)
    rTT_PELTIER_HEATSINK_502          : REAL := 15.0;     (* Peltier Hot-Side Liquid-Cooled Heat Sink Temperature RTD [deg C] *)
    rFT_DIAFILTRATION_BUFFER_305      : REAL := 12.0;     (* TFF Buffer Replacement Metering Peristaltic Pump Flow [mL/min] *)
    rLT_RETENTATE_RECIRC_TANK_306     : REAL := 50.0;     (* TFF Retentate Surge Tank Hydrostatic Level Sensor [%] *)
    rQIT_BUFFER_CONDUCTIVITY_307      : REAL := 14.8;     (* In-Line Buffer Conductivity Probe [mS/cm] *)
    rQIT_BUFFER_PH_308                : REAL := 7.40;     (* In-Line Diafiltration Retentate pH Electrode [-] *)
END_VAR

VAR_OUTPUT
    (* === ANALOG ACTUATOR VELOCITY & POSITION COMMANDS === *)
    rCmd_AqueousPump_ml_min           : REAL := 0.0;      (* Aqueous Dual-Syringe Servo Pump Volumetric Rate [0.0..50.0 mL/min] *)
    rCmd_EthanolPump_ml_min           : REAL := 0.0;      (* Ethanol Lipid Dual-Syringe Servo Pump Rate [0.0..25.0 mL/min] *)
    rCmd_TFF_RetentateValve_Pct       : REAL := 0.0;      (* TFF Retentate Proportional Pinch Throttle Valve [0.0..100.0 %] *)
    rCmd_TFF_DiafiltrationPump_ml_min : REAL := 0.0;      (* TFF Buffer Dosing Peristaltic Metering Pump Rate [0.0..50.0 mL/min] *)
    rCmd_TFF_PermeateValve_Pct        : REAL := 0.0;      (* TFF Permeate Line Proportional Regulating Valve [0.0..100.0 %] *)
    rCmd_PeltierCurrent_Amps          : REAL := 0.0;      (* Peltier Thermoelectric Module H-Bridge DC Current [-15.0..+15.0 A] *)
    rCmd_MicrofluidicBPR_Pct          : REAL := 0.0;      (* Microfluidic Backpressure Regulator Throttle [0.0..100.0 %] *)
    rCmd_QuenchCirculationPump_Pct    : REAL := 0.0;      (* Cryo-Jacket Coolant Recirculation Pump Speed [0.0..100.0 %] *)

    (* === DISCRETE BIOPROCESS VALVES & STERILE ROUTING === *)
    bCmd_DivertToWasteValve           : BOOL := TRUE;     (* 3-Way Off-Spec Product Diversion Valve to Waste (TRUE = Waste) *)
    bCmd_ProductHarvestValve          : BOOL := FALSE;    (* Sterile In-Spec Encapsulated LNP Product Harvest Valve [BOOL] *)
    bCmd_WFIFlushValve                : BOOL := FALSE;    (* Sterile Water-for-Injection (WFI) High-Pressure Flush Valve [BOOL] *)
    bCmd_CIPCausticSupplyValve        : BOOL := FALSE;    (* 0.5 M NaOH Caustic Sanitization Supply Isolation Valve [BOOL] *)
    bCmd_CleanSteamSterilizeValve     : BOOL := FALSE;    (* Pure Clean Steam 121 deg C SIP Supply Valve [BOOL] *)
    bCmd_EmergencyContainmentIsolate  : BOOL := FALSE;    (* Biosafety High-Speed Micro-Pinch Containment Isolation Clamps [BOOL] *)
    bCmd_TFF_PermeateDrainValve       : BOOL := FALSE;    (* TFF Ultrafiltration Permeate Discharge Drain Valve [BOOL] *)
    bCmd_NitrogenPurgeBlanketValve    : BOOL := FALSE;    (* Sterile N2 Gas Blanketing & Blowdown Isolation Valve [BOOL] *)

    (* === OBSERVED PROCESS VARIABLES & HYDRODYNAMIC METRICS === *)
    rObs_ParticleDiameter_Voted_nm    : REAL := 75.0;     (* 2oo3 Triple Modular Redundant Voted Mean Particle Diameter [nm] *)
    rObs_PDI_Voted                    : REAL := 0.080;    (* 2oo3 Triple Modular Redundant Voted Polydispersity Index [-] *)
    rObs_AqueousFlow_Voted_ml_min     : REAL := 18.0;     (* 2oo3 Triple Modular Redundant Voted Aqueous Phase Flow [mL/min] *)
    rObs_EthanolFlow_Voted_ml_min     : REAL := 6.0;      (* 2oo3 Triple Modular Redundant Voted Ethanol Phase Flow [mL/min] *)
    rObs_MicrofluidicInletPress_bar   : REAL := 2.80;     (* 2oo3 Triple Modular Redundant Voted Mixer Inlet Pressure [bar] *)
    rObs_TFF_FeedPressure_Voted_bar   : REAL := 1.25;     (* 2oo3 Triple Modular Redundant Voted TFF Feed Pressure [bar] *)
    rObs_TFF_TransmembranePressure_bar: REAL := 0.85;     (* Calculated In-Line Transmembrane Pressure TMP [bar] *)
    rObs_CryoTemp_Voted_degC          : REAL := 2.0;      (* 2oo3 Triple Modular Redundant Voted Cryo-Quench Temp [deg C] *)
    rObs_ResidualEthanol_Voted_ppm    : REAL := 25.0;     (* 2oo3 Triple Modular Redundant Voted Residual Ethanol [ppm] *)
    rObs_EncapsulationEfficiency_Pct  : REAL := 95.0;     (* In-Line Calculated mRNA Encapsulation Efficiency EE% [%] *)
    rObs_MicrofluidicReynoldsNumber   : REAL := 285.0;    (* Calculated Microfluidic Staggered Channel Reynolds Number [-] *)
    rObs_DeanNumber                   : REAL := 82.5;     (* Calculated Dean Vortex Secondary Flow Dimensionless Number [-] *)
    rObs_GelLayerThickness_um         : REAL := 1.42;     (* Observer-Estimated TFF Membrane Gel Polarization Layer [um] *)

    (* === AUTOMATION & BATCH EXECUTION STATUS WORDS === *)
    iCurrentStateID                   : INT := 10;        (* Active ISA-88 State Machine State Numerical Identifier [0..999] *)
    bEncapsulationActive              : BOOL := FALSE;    (* Encapsulation Mixer Active in Validated Production State [BOOL] *)
    bBatchQualifiedInSpec             : BOOL := FALSE;    (* Dynamic Light Scattering Continuous Product Qualification High [BOOL] *)
    bSystemInFault                    : BOOL := FALSE;    (* Skid Latched in Protective Fault Trip Mode [BOOL] *)
    bCIP_SIP_InProgress               : BOOL := FALSE;    (* Sanitization or Clean Steam Sterilization In Progress [BOOL] *)
    tCurrentBatchRunDuration          : TIME := T#0S;     (* Total Validated In-Spec Continuous Production Run Duration [TIME] *)
    rTotalProductHarvested_Liters     : REAL := 0.0;      (* Total Cumulative In-Spec Bulk Drug Substance Harvested [L] *)

    (* === ISA-18.2 ALARMS & DIAGNOSTIC PACKED WORDS === *)
    wAlarmWord_ISA18_Critical_HH_LL   : WORD := 16#0000;  (* Priority 1 Critical Trip Alarms (Emergency Divert / Abort) [WORD] *)
    wAlarmWord_ISA18_Warning_H_L      : WORD := 16#0000;  (* Priority 2 Process Warning Alarms (MPC Saturation / Drift) [WORD] *)
    wAlarmWord_ISA18_RateOfChange_ROC : WORD := 16#0000;  (* Priority 3 Dynamic Rate-of-Change & Membrane Fouling Alarms [WORD] *)
    wTMR_SensorHealthWord_1           : WORD := 16#0000;  (* 2oo3 Triplex Transducer Discrepancy Health Matrix Word 1 [WORD] *)
    wTMR_SensorHealthWord_2           : WORD := 16#0000;  (* 2oo3 Triplex Transducer Discrepancy Health Matrix Word 2 [WORD] *)
    wAutomationStatusWord             : WORD := 16#0000;  (* General Bioprocess Unit Operational Mode & Health Status [WORD] *)
END_VAR

VAR
    (* === CYBER-PHYSICAL SYSTEM CONSTANTS === *)
    T_CYCLE_SEC                       : REAL := 0.005;    (* Discrete Task Execution Sample Interval (5 milliseconds) [s] *)
    BOLTZMANN_K_B                     : REAL := 1.380649E-23; (* Boltzmann Thermodynamic Constant [J/K] *)
    AVOGADRO_N_A                      : REAL := 6.022140E+23; (* Avogadro Molecular Constant [1/mol] *)
    UNIVERSAL_GAS_R                   : REAL := 8.314462; (* Universal Molar Gas Constant [J/(mol*K)] *)
    WATER_VISCOSITY_ETA               : REAL := 0.001002; (* Dynamic Viscosity of Water at 20 deg C [Pa*s] *)
    CHANNEL_HYDRAULIC_DIAM_DH         : REAL := 0.000182; (* Staggered Herringbone Microchannel Hydraulic Diameter [m] *)
    CHANNEL_CURVATURE_RADIUS_RC       : REAL := 0.001200; (* Microchannel Asymmetric Herringbone Groove Curvature [m] *)
    TFF_MEMBRANE_AREA_M2              : REAL := 0.100;    (* Total Geometric Ultrafiltration Membrane Area [m2] *)
    MEMBRANE_HYDRAULIC_RESISTANCE_RM  : REAL := 1.85E+12; (* Clean Polyethersulfone Membrane Clean Resistance [1/m] *)
    PELTIER_SEEBECK_ALPHA             : REAL := 0.0450;   (* Total Effective Seebeck Coefficient (256 thermocouples) [V/K] *)
    PELTIER_ELEC_RESISTANCE_RE        : REAL := 1.150;    (* Internal Series Electrical Resistance of Module [Ohms] *)
    PELTIER_THERMAL_CONDUCT_KTH       : REAL := 0.820;    (* Thermal Conductance Between Cold and Hot Ceramic Faces [W/K] *)

    (* === 8x8 DISCRETE STATE-SPACE MATRICES & VECTORS === *)
    arrA                              : ARRAY[1..8, 1..8] OF REAL; (* Discrete State Transition Matrix A (8x8) *)
    arrB                              : ARRAY[1..8, 1..8] OF REAL; (* Discrete Control Input Coupling Matrix B (8x8) *)
    arrC                              : ARRAY[1..8, 1..8] OF REAL; (* Discrete Observation Mapping Matrix C (8x8) *)
    arrD                              : ARRAY[1..8, 1..8] OF REAL; (* Discrete Direct Feedthrough Matrix D (8x8) *)
    arrState_x                        : ARRAY[1..8] OF REAL;       (* Estimated System State Vector x[k] *)
    arrState_x_next                   : ARRAY[1..8] OF REAL;       (* Forward Projected State Vector x[k+1] *)
    arrOutput_y                       : ARRAY[1..8] OF REAL;       (* Modeled System Output Vector y[k] *)
    arrInput_u                        : ARRAY[1..8] OF REAL;       (* System Control Input Vector u[k] *)
    arrSetpoint_r                     : ARRAY[1..8] OF REAL;       (* Bioprocess Target Setpoint Vector r[k] *)
    arrStateError_e                   : ARRAY[1..8] OF REAL;       (* State Error Vector e[k] = x[k] - r[k] *)
    arrObserverGain_L                 : ARRAY[1..8] OF REAL;       (* Luenberger State Observer Feedback Gain Vector *)

    (* === RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) MATRICES === *)
    arrQ_diag                         : ARRAY[1..8] OF REAL;       (* Diagonal State Penalty Weights (Cost Functional Q) *)
    arrR_diag                         : ARRAY[1..8] OF REAL;       (* Diagonal Actuator Effort Penalty Weights (Cost Functional R) *)
    arrS_diag                         : ARRAY[1..8] OF REAL;       (* Diagonal Actuator Slew-Rate Penalty Weights (Cost Functional S) *)
    arrP_terminal                     : ARRAY[1..8] OF REAL;       (* Terminal Horizon Cost Functional Weights P *)
    arrK_mpc                          : ARRAY[1..8, 1..8] OF REAL; (* Optimal Feedback MPC Gain Matrix (Pre-calculated Riccati) *)
    arrDelta_u                        : ARRAY[1..8] OF REAL;       (* Incremental Actuator Adjustment Vector delta_u[k] *)
    arrU_prev                         : ARRAY[1..8] OF REAL;       (* Prior Execution Cycle Actuator Command Vector u[k-1] *)
    arrPredictedTraj_x                : ARRAY[1..5, 1..8] OF REAL; (* 5-Step Forward State Trajectory Prediction *)
    arrPredictedTraj_u                : ARRAY[1..5, 1..8] OF REAL; (* 5-Step Forward Actuator Prediction *)

    (* === 2oo3 TRIPLE MODULAR REDUNDANCY VOTING DATA STRUCTURES === *)
    (* Group 1: DLS Particle Hydrodynamic Diameter (nm) *)
    rTMR_DLS_Diam_Diff_AB             : REAL := 0.0;
    rTMR_DLS_Diam_Diff_BC             : REAL := 0.0;
    rTMR_DLS_Diam_Diff_CA             : REAL := 0.0;
    bTMR_DLS_Diam_Match_AB            : BOOL := TRUE;
    bTMR_DLS_Diam_Match_BC            : BOOL := TRUE;
    bTMR_DLS_Diam_Match_CA            : BOOL := TRUE;
    rTMR_DLS_Diam_DiscrepTimer_A      : REAL := 0.0;
    rTMR_DLS_Diam_DiscrepTimer_B      : REAL := 0.0;
    rTMR_DLS_Diam_DiscrepTimer_C      : REAL := 0.0;
    bTMR_DLS_Diam_Fault_A             : BOOL := FALSE;
    bTMR_DLS_Diam_Fault_B             : BOOL := FALSE;
    bTMR_DLS_Diam_Fault_C             : BOOL := FALSE;

    (* Group 2: DLS Polydispersity Index PDI (-) *)
    rTMR_DLS_PDI_Diff_AB              : REAL := 0.0;
    rTMR_DLS_PDI_Diff_BC              : REAL := 0.0;
    rTMR_DLS_PDI_Diff_CA              : REAL := 0.0;
    bTMR_DLS_PDI_Match_AB             : BOOL := TRUE;
    bTMR_DLS_PDI_Match_BC             : BOOL := TRUE;
    bTMR_DLS_PDI_Match_CA             : BOOL := TRUE;
    rTMR_DLS_PDI_DiscrepTimer_A       : REAL := 0.0;
    rTMR_DLS_PDI_DiscrepTimer_B       : REAL := 0.0;
    rTMR_DLS_PDI_DiscrepTimer_C       : REAL := 0.0;
    bTMR_DLS_PDI_Fault_A              : BOOL := FALSE;
    bTMR_DLS_PDI_Fault_B              : BOOL := FALSE;
    bTMR_DLS_PDI_Fault_C              : BOOL := FALSE;

    (* Group 3: Aqueous Phase Flowrate (mL/min) *)
    rTMR_Flow_Aq_Diff_AB              : REAL := 0.0;
    rTMR_Flow_Aq_Diff_BC              : REAL := 0.0;
    rTMR_Flow_Aq_Diff_CA              : REAL := 0.0;
    bTMR_Flow_Aq_Match_AB             : BOOL := TRUE;
    bTMR_Flow_Aq_Match_BC             : BOOL := TRUE;
    bTMR_Flow_Aq_Match_CA             : BOOL := TRUE;
    rTMR_Flow_Aq_DiscrepTimer_A       : REAL := 0.0;
    rTMR_Flow_Aq_DiscrepTimer_B       : REAL := 0.0;
    rTMR_Flow_Aq_DiscrepTimer_C       : REAL := 0.0;
    bTMR_Flow_Aq_Fault_A              : BOOL := FALSE;
    bTMR_Flow_Aq_Fault_B              : BOOL := FALSE;
    bTMR_Flow_Aq_Fault_C              : BOOL := FALSE;

    (* Group 4: Ethanol Lipid Phase Flowrate (mL/min) *)
    rTMR_Flow_Eth_Diff_AB             : REAL := 0.0;
    rTMR_Flow_Eth_Diff_BC             : REAL := 0.0;
    rTMR_Flow_Eth_Diff_CA             : REAL := 0.0;
    bTMR_Flow_Eth_Match_AB            : BOOL := TRUE;
    bTMR_Flow_Eth_Match_BC            : BOOL := TRUE;
    bTMR_Flow_Eth_Match_CA            : BOOL := TRUE;
    rTMR_Flow_Eth_DiscrepTimer_A      : REAL := 0.0;
    rTMR_Flow_Eth_DiscrepTimer_B      : REAL := 0.0;
    rTMR_Flow_Eth_DiscrepTimer_C      : REAL := 0.0;
    bTMR_Flow_Eth_Fault_A             : BOOL := FALSE;
    bTMR_Flow_Eth_Fault_B             : BOOL := FALSE;
    bTMR_Flow_Eth_Fault_C             : BOOL := FALSE;

    (* Group 5: TFF Cassette Feed Pressure (bar) *)
    rTMR_Press_Feed_Diff_AB           : REAL := 0.0;
    rTMR_Press_Feed_Diff_BC           : REAL := 0.0;
    rTMR_Press_Feed_Diff_CA           : REAL := 0.0;
    bTMR_Press_Feed_Match_AB          : BOOL := TRUE;
    bTMR_Press_Feed_Match_BC          : BOOL := TRUE;
    bTMR_Press_Feed_Match_CA          : BOOL := TRUE;
    rTMR_Press_Feed_DiscrepTimer_A    : REAL := 0.0;
    rTMR_Press_Feed_DiscrepTimer_B    : REAL := 0.0;
    rTMR_Press_Feed_DiscrepTimer_C    : REAL := 0.0;
    bTMR_Press_Feed_Fault_A           : BOOL := FALSE;
    bTMR_Press_Feed_Fault_B           : BOOL := FALSE;
    bTMR_Press_Feed_Fault_C           : BOOL := FALSE;

    (* Group 6: Cryo-Quench Product RTD Temperature (deg C) *)
    rTMR_Temp_Cryo_Diff_AB            : REAL := 0.0;
    rTMR_Temp_Cryo_Diff_BC            : REAL := 0.0;
    rTMR_Temp_Cryo_Diff_CA            : REAL := 0.0;
    bTMR_Temp_Cryo_Match_AB           : BOOL := TRUE;
    bTMR_Temp_Cryo_Match_BC           : BOOL := TRUE;
    bTMR_Temp_Cryo_Match_CA           : BOOL := TRUE;
    rTMR_Temp_Cryo_DiscrepTimer_A     : REAL := 0.0;
    rTMR_Temp_Cryo_DiscrepTimer_B     : REAL := 0.0;
    rTMR_Temp_Cryo_DiscrepTimer_C     : REAL := 0.0;
    bTMR_Temp_Cryo_Fault_A            : BOOL := FALSE;
    bTMR_Temp_Cryo_Fault_B            : BOOL := FALSE;
    bTMR_Temp_Cryo_Fault_C            : BOOL := FALSE;

    (* Group 7: Residual Ethanol Concentration (ppm) *)
    rTMR_AIT_Eth_Diff_AB              : REAL := 0.0;
    rTMR_AIT_Eth_Diff_BC              : REAL := 0.0;
    rTMR_AIT_Eth_Diff_CA              : REAL := 0.0;
    bTMR_AIT_Eth_Match_AB             : BOOL := TRUE;
    bTMR_AIT_Eth_Match_BC             : BOOL := TRUE;
    bTMR_AIT_Eth_Match_CA             : BOOL := TRUE;
    rTMR_AIT_Eth_DiscrepTimer_A       : REAL := 0.0;
    rTMR_AIT_Eth_DiscrepTimer_B       : REAL := 0.0;
    rTMR_AIT_Eth_DiscrepTimer_C       : REAL := 0.0;
    bTMR_AIT_Eth_Fault_A              : BOOL := FALSE;
    bTMR_AIT_Eth_Fault_B              : BOOL := FALSE;
    bTMR_AIT_Eth_Fault_C              : BOOL := FALSE;

    (* Discrepancy Threshold Constants *)
    TMR_DISCREP_TOL_DIAMETER_NM       : REAL := 3.50;     (* DLS Diameter Max Allowable Channel Spread [nm] *)
    TMR_DISCREP_TOL_PDI               : REAL := 0.012;    (* DLS PDI Max Allowable Channel Spread [-] *)
    TMR_DISCREP_TOL_FLOW_ML_MIN       : REAL := 0.350;    (* Coriolis Liquid Flow Channel Spread [mL/min] *)
    TMR_DISCREP_TOL_PRESSURE_BAR      : REAL := 0.050;    (* TFF Pressure Transducer Channel Spread [bar] *)
    TMR_DISCREP_TOL_TEMP_DEGC         : REAL := 0.250;    (* Cryogenic RTD Temperature Spread [deg C] *)
    TMR_DISCREP_TOL_ETH_PPM           : REAL := 4.000;    (* Residual Ethanol Concentration Spread [ppm] *)
    TMR_DISCREP_DEBOUNCE_TIME_SEC     : REAL := 0.250;    (* Discrepancy Fault Integration Trip Time [s] *)

    (* === ISA-18.2 ALARM TRIP POINTS, DEADBANDS & STATUS FLAGS === *)
    (* Level 1: Hydrodynamic Particle Diameter *)
    rAlarmSet_Diam_LL                 : REAL := 65.0;     (* Particle Size Low-Low Critical Trip [nm] *)
    rAlarmSet_Diam_L                  : REAL := 72.0;     (* Particle Size Low Warning [nm] *)
    rAlarmSet_Diam_H                  : REAL := 78.0;     (* Particle Size High Warning [nm] *)
    rAlarmSet_Diam_HH                 : REAL := 85.0;     (* Particle Size High-High Critical Trip [nm] *)
    rAlarmSet_Diam_Deadband           : REAL := 0.8;      (* Particle Size Alarm Deadband Hysteresis [nm] *)
    bAlarm_Diam_LL                    : BOOL := FALSE;
    bAlarm_Diam_L                     : BOOL := FALSE;
    bAlarm_Diam_H                     : BOOL := FALSE;
    bAlarm_Diam_HH                    : BOOL := FALSE;

    (* Level 2: Polydispersity Index PDI *)
    rAlarmSet_PDI_H                   : REAL := 0.100;    (* PDI High Advisory Warning [-] *)
    rAlarmSet_PDI_HH                  : REAL := 0.120;    (* PDI High-High Critical Out-of-Spec Diversion [-] *)
    rAlarmSet_PDI_Deadband            : REAL := 0.005;    (* PDI Hysteresis Deadband [-] *)
    bAlarm_PDI_H                      : BOOL := FALSE;
    bAlarm_PDI_HH                     : BOOL := FALSE;

    (* Level 3: Microfluidic Mixer Inlet Pressure *)
    rAlarmSet_MixerPress_H            : REAL := 4.50;     (* Mixer Pressure High Warning [bar] *)
    rAlarmSet_MixerPress_HH           : REAL := 5.80;     (* Mixer Pressure High-High Burst Risk Trip [bar] *)
    rAlarmSet_MixerPress_Deadband     : REAL := 0.15;     (* Pressure Hysteresis Deadband [bar] *)
    bAlarm_MixerPress_H               : BOOL := FALSE;
    bAlarm_MixerPress_HH              : BOOL := FALSE;

    (* Level 4: TFF Transmembrane Pressure TMP *)
    rAlarmSet_TMP_L                   : REAL := 0.30;     (* TFF TMP Low Starvation Warning [bar] *)
    rAlarmSet_TMP_H                   : REAL := 1.20;     (* TFF TMP High Membrane Gel Polarization Warning [bar] *)
    rAlarmSet_TMP_HH                  : REAL := 1.60;     (* TFF TMP High-High Membrane Rupture Protection Trip [bar] *)
    rAlarmSet_TMP_Deadband            : REAL := 0.05;     (* TMP Hysteresis Deadband [bar] *)
    bAlarm_TMP_L                      : BOOL := FALSE;
    bAlarm_TMP_H                      : BOOL := FALSE;
    bAlarm_TMP_HH                     : BOOL := FALSE;

    (* Level 5: Residual Diafiltration Ethanol *)
    rAlarmSet_Eth_H                   : REAL := 40.0;     (* Residual Ethanol High Approach Warning [ppm] *)
    rAlarmSet_Eth_HH                  : REAL := 50.0;     (* Residual Ethanol High-High Batch Rejection Limit [ppm] *)
    rAlarmSet_Eth_Deadband            : REAL := 2.0;      (* Ethanol Hysteresis Deadband [ppm] *)
    bAlarm_Eth_H                      : BOOL := FALSE;
    bAlarm_Eth_HH                     : BOOL := FALSE;

    (* Level 6: Cryogenic Quench Temperature *)
    rAlarmSet_CryoTemp_LL             : REAL := -25.0;    (* Cryo Temperature Low-Low Freeze Overcool Trip [deg C] *)
    rAlarmSet_CryoTemp_L              : REAL := -20.0;    (* Cryo Temperature Low Warning [deg C] *)
    rAlarmSet_CryoTemp_H              : REAL := 4.5;      (* Cryo Temperature High Warning [deg C] *)
    rAlarmSet_CryoTemp_HH             : REAL := 8.0;      (* Cryo Temperature High-High Thermal Degradation Trip [deg C] *)
    rAlarmSet_CryoTemp_Deadband       : REAL := 0.3;      (* Cryo Temp Hysteresis Deadband [deg C] *)
    bAlarm_CryoTemp_LL                : BOOL := FALSE;
    bAlarm_CryoTemp_L                 : BOOL := FALSE;
    bAlarm_CryoTemp_H                 : BOOL := FALSE;
    bAlarm_CryoTemp_HH                : BOOL := FALSE;

    (* Level 7: Rate-of-Change (ROC) Dynamic Alarms *)
    rRateOfChange_MixerPress_bar_s    : REAL := 0.0;      (* Pressure Rate of Change (Channel Clogging Risk) [bar/s] *)
    rRateOfChange_PDI_per_s           : REAL := 0.0;      (* PDI Rate of Change (Precipitation Instability) [1/s] *)
    rPrev_MixerPress_bar              : REAL := 2.80;
    rPrev_PDI                         : REAL := 0.080;
    bAlarm_ROC_MixerClog_High         : BOOL := FALSE;
    bAlarm_ROC_PrecipInstability_High : BOOL := FALSE;

    (* Level 8: Hardware Safety & TMR Sensor Fault Alarms *)
    bAlarm_EmergencyStopTripped       : BOOL := FALSE;
    bAlarm_ContainmentBreach          : BOOL := FALSE;
    bAlarm_TMR_DLS_DualFault          : BOOL := FALSE;
    bAlarm_TMR_Pressure_DualFault     : BOOL := FALSE;
    bAlarm_TMR_Flow_DualFault         : BOOL := FALSE;

    (* === FINITE STATE MACHINE (FSM) CONTROL REGISTERS === *)
    eCurrentState                     : INT := 10;        (* Active Finite State Identifier *)
    ePreviousState                    : INT := 0;         (* Historical Previous State Identifier *)
    rStateTimer_Sec                   : REAL := 0.0;      (* Continuous Dwell Time in Current State [s] *)
    rProductionTimer_Sec              : REAL := 0.0;      (* Cumulative Production Run Clock [s] *)
    rDiafiltrationAccumVolume_mL      : REAL := 0.0;      (* Integrated Buffer Replacement Volume [mL] *)
    rContinuousInSpecTimer_Sec        : REAL := 0.0;      (* DLS Stable In-Spec Window Qualification Timer [s] *)
    rDivertHoldTimer_Sec              : REAL := 0.0;      (* Divert to Waste Transient Settle Timer [s] *)
    rCIP_StepTimer_Sec                : REAL := 0.0;      (* Clean-in-Place Phase Progress Timer [s] *)
    iCIP_SubPhase                     : INT := 0;         (* Sub-phase sequencer for CIP/SIP sequence *)

    (* === INTERNAL ITERATION, SCRATCH & ALGORITHM VARIABLES === *)
    bFirstScanInitialized             : BOOL := FALSE;    (* Power-On Cold-Start Matrix Initialization Flag *)
    iRowIndex                         : INT := 1;
    jColIndex                         : INT := 1;
    kHorizonIndex                     : INT := 1;
    rMatrixAccum                      : REAL := 0.0;
    rCostGradient                     : REAL := 0.0;
    rTempAqueousRatioCalc             : REAL := 3.0;
    rCurrentTotalFlow                 : REAL := 24.0;
    rEstimatedGelMassFlux             : REAL := 0.0;
    rHeatPumpingColdWatts             : REAL := 0.0;
    rHeatPumpingJouleWatts            : REAL := 0.0;
    rHeatPumpingConductWatts          : REAL := 0.0;
    rNetPeltierHeatExtraction         : REAL := 0.0;
    rArrheniusSupersatKinetics        : REAL := 0.0;
    rPhotonCorrelationTau             : REAL := 0.000015;
    rCumulantsSecondMoment            : REAL := 0.0;
    rTFF_AverageMembranePressure      : REAL := 1.05;
    rTFF_CleanMembraneFlux            : REAL := 52.0;
    rTFF_GelMassResistance            : REAL := 3.2E+11;
    rBulkNanoparticleSolubility       : REAL := 0.045;
    rSupersaturationEquilibriumRatio  : REAL := 12.5;
END_VAR
'''
    sections.append(sec1)

    # =========================================================================
    # SECTION 2: INITIALIZATION & MATRIX DEFINITIONS (PHASE 0)
    # =========================================================================
    sec2 = r'''
(* === COLD-START FIRST-SCAN MATRIX & PARAMETER INITIALIZATION === *)
IF NOT bFirstScanInitialized THEN
    (* -------------------------------------------------------------------------
       Continuous-to-Discrete State Transition Matrix arrA (8x8 at Ts = 0.005 s)
       State x: [v_mix, S_supersat, N_nuclei, D_h, PDI, delta_gel, C_ethanol, T_cryo]
       ------------------------------------------------------------------------- *)
    FOR iRowIndex := 1 TO 8 DO
        FOR jColIndex := 1 TO 8 DO
            arrA[iRowIndex, jColIndex] := 0.0;
            arrB[iRowIndex, jColIndex] := 0.0;
            arrC[iRowIndex, jColIndex] := 0.0;
            arrD[iRowIndex, jColIndex] := 0.0;
            arrK_mpc[iRowIndex, jColIndex] := 0.0;
        END_FOR;
    END_FOR;

    (* Row 1: Microchannel convective velocity v_mix dynamics (Fast momentum dissipation) *)
    arrA[1, 1] := 0.941764; (* e^(-Ts / tau_momentum) with tau_momentum = 83 ms *)
    arrA[1, 2] := 0.000000;
    arrA[1, 3] := 0.000000;
    arrA[1, 4] := 0.000000;
    arrA[1, 5] := 0.000000;
    arrA[1, 6] := 0.000000;
    arrA[1, 7] := 0.000000;
    arrA[1, 8] := 0.000000;

    (* Row 2: Supersaturation ratio S dynamics (Coupled to flow velocity advection and consumption) *)
    arrA[2, 1] := 0.015240; (* Cross-coupling: increased fluid velocity enhances chaotic advection *)
    arrA[2, 2] := 0.886920; (* Natural supersaturation depletion via rapid self-assembly nucleation *)
    arrA[2, 3] := -0.000045; (* Nucleation consumption sink *)
    arrA[2, 4] := 0.000000;
    arrA[2, 5] := 0.000000;
    arrA[2, 6] := 0.000000;
    arrA[2, 7] := 0.000310; (* Residual ethanol solubility coupling *)
    arrA[2, 8] := -0.001850; (* Temperature dependence of lipid solubility in aqueous mixture *)

    (* Row 3: Nucleation density N_nuclei dynamics (Burst kinetics followed by collision aggregation) *)
    arrA[3, 1] := 0.008450;
    arrA[3, 2] := 0.042800; (* Strong driving force from supersaturation ratio S *)
    arrA[3, 3] := 0.912400; (* Particle persistence / Smoluchowski coagulation damping *)
    arrA[3, 4] := -0.002100; (* Growth depletes free nuclei *)
    arrA[3, 5] := 0.000000;
    arrA[3, 6] := 0.000000;
    arrA[3, 7] := 0.000000;
    arrA[3, 8] := 0.000420;

    (* Row 4: Mean hydrodynamic diameter D_h [nm] (Stokes-Einstein self-assembly kinetics) *)
    arrA[4, 1] := -0.024500; (* Higher velocity -> thinner striation thickness -> smaller particles *)
    arrA[4, 2] := -0.058200; (* Higher supersaturation -> smaller critical nucleus radius r* *)
    arrA[4, 3] := -0.012400; (* Higher nucleation rate -> smaller mean diameter *)
    arrA[4, 4] := 0.985200;  (* Geometric size persistence / Ostwald ripening relaxation *)
    arrA[4, 5] := 0.000000;
    arrA[4, 6] := 0.000000;
    arrA[4, 7] := 0.004120;  (* Higher ethanol preserves fluidity, promotes larger equilibrium size *)
    arrA[4, 8] := 0.003500;  (* Warmer temperature increases diffusion and ripening kinetics *)

    (* Row 5: Polydispersity index PDI [-] (Mixing homogeneity and residence time distribution) *)
    arrA[5, 1] := -0.006200; (* Higher velocity ensures chaotic advection across all streamlines *)
    arrA[5, 2] := -0.008900; (* High supersaturation synchronizes nucleation burst *)
    arrA[5, 3] := 0.000000;
    arrA[5, 4] := 0.000150;
    arrA[5, 5] := 0.965400;  (* PDI relaxation time constant *)
    arrA[5, 6] := 0.000000;
    arrA[5, 7] := 0.001850;  (* Ethanol gradient broadening *)
    arrA[5, 8] := 0.000280;

    (* Row 6: TFF membrane concentration polarization gel layer delta_gel [um] *)
    arrA[6, 1] := 0.000000;
    arrA[6, 2] := 0.000000;
    arrA[6, 3] := 0.000000;
    arrA[6, 4] := 0.001150;  (* Larger particles form looser but thicker porous cakes *)
    arrA[6, 5] := 0.000850;  (* Polydispersity packs interstitial voids, increasing cake resistance *)
    arrA[6, 6] := 0.978200;  (* Gel layer hydrodynamic decay / crossflow shear erosion *)
    arrA[6, 7] := 0.000000;
    arrA[6, 8] := -0.000450; (* Viscosity changes with temperature *)

    (* Row 7: Retentate residual ethanol concentration C_eth [ppm] (Diafiltration washout) *)
    arrA[7, 1] := 0.000000;
    arrA[7, 2] := 0.000000;
    arrA[7, 3] := 0.000000;
    arrA[7, 4] := 0.000000;
    arrA[7, 5] := 0.000000;
    arrA[7, 6] := -0.002500; (* Gel layer reduces permeate flux, slowing diafiltration washout *)
    arrA[7, 7] := 0.992100;  (* Exponential dilution: C(t) = C0 * exp(-V_dia / V_ret) *)
    arrA[7, 8] := 0.000000;

    (* Row 8: Cryo-quench product temperature T_cryo [deg C] (Thermal mass and heat conduction) *)
    arrA[8, 1] := 0.000000;
    arrA[8, 2] := 0.000000;
    arrA[8, 3] := 0.000000;
    arrA[8, 4] := 0.000000;
    arrA[8, 5] := 0.000000;
    arrA[8, 6] := 0.000000;
    arrA[8, 7] := 0.000000;
    arrA[8, 8] := 0.975400;  (* First-order thermal dissipation to coolant jacket *)

    (* -------------------------------------------------------------------------
       Discrete Control Coupling Matrix arrB (8x8 at Ts = 0.005 s)
       Input u: [Q_aq, Q_eth, Valve_ret, Q_dia, I_peltier, Valve_BPR, Pump_glycol, Valve_perm]
       ------------------------------------------------------------------------- *)
    (* u[1]: Aqueous pump rate [mL/min] *)
    arrB[1, 1] := 0.042500;  (* Direct convective momentum contribution *)
    arrB[2, 1] := 0.018500;  (* Increases total dilution ratio *)
    arrB[4, 1] := -0.038500; (* Faster total flow reduces particle diameter *)
    arrB[5, 1] := -0.004200; (* Improves mixing homogeneity, lowers PDI *)

    (* u[2]: Ethanol lipid pump rate [mL/min] *)
    arrB[1, 2] := 0.014200;  (* Viscous organic phase contribution *)
    arrB[2, 2] := 0.065400;  (* Increases lipid supersaturation concentration *)
    arrB[4, 2] := 0.048200;  (* Higher lipid concentration leads to larger vesicles *)
    arrB[5, 2] := 0.006800;  (* Excess lipid increases PDI if not balanced *)
    arrB[7, 2] := 0.850000;  (* Direct source of ethanol into system [ppm/cycle] *)

    (* u[3]: TFF retentate valve throttle [%] *)
    arrB[6, 3] := -0.015200; (* Throttling valve increases cross-flow shear, stripping gel layer *)

    (* u[4]: TFF diafiltration buffer dosing pump [mL/min] *)
    arrB[7, 4] := -0.125000; (* Accelerates ethanol clearance washout *)

    (* u[5]: Peltier thermoelectric current [A] *)
    arrB[8, 5] := -0.084500; (* Active Seebeck/Peltier heat absorption (negative dT/dt) *)

    (* u[6]: Microfluidic backpressure regulator BPR [%] *)
    arrB[1, 6] := -0.008500; (* Backpressure dampens syringe pulsation *)

    (* u[7]: Glycol coolant circulation pump [%] *)
    arrB[8, 7] := -0.012500; (* Lowers hot-side heat sink temperature, boosting COP *)

    (* u[8]: TFF permeate valve [%] *)
    arrB[6, 8] := 0.024500;  (* Opening permeate increases convective cake drag force *)
    arrB[7, 8] := -0.065000; (* Permeate discharge removes dissolved ethanol *)

    (* -------------------------------------------------------------------------
       Discrete Output Mapping Matrix arrC (8x8) & Feedthrough arrD (8x8)
       ------------------------------------------------------------------------- *)
    FOR iRowIndex := 1 TO 8 DO
        arrC[iRowIndex, iRowIndex] := 1.0; (* Direct state observation mapping *)
    END_FOR;

    (* -------------------------------------------------------------------------
       Luenberger State Observer Gain Vector arrObserverGain_L
       ------------------------------------------------------------------------- *)
    arrObserverGain_L[1] := 0.1450;
    arrObserverGain_L[2] := 0.0980;
    arrObserverGain_L[3] := 0.0820;
    arrObserverGain_L[4] := 0.2450; (* High gain on primary CQA: particle diameter *)
    arrObserverGain_L[5] := 0.2100; (* High gain on primary CQA: PDI *)
    arrObserverGain_L[6] := 0.0750;
    arrObserverGain_L[7] := 0.1850; (* Strong gain on residual ethanol observer *)
    arrObserverGain_L[8] := 0.1950; (* Strong gain on cryo quench temperature *)

    (* -------------------------------------------------------------------------
       MPC Quadratic Cost Diagonal Weights (Q, R, S, P)
       ------------------------------------------------------------------------- *)
    (* Q State Error Penalty: Heavily penalize particle diameter, PDI, ethanol, and temp *)
    arrQ_diag[1] := 2.5;     (* Velocity error *)
    arrQ_diag[2] := 5.0;     (* Supersaturation ratio error *)
    arrQ_diag[3] := 1.0;     (* Nucleation density *)
    arrQ_diag[4] := 125.0;   (* Mean particle diameter (CQA: target 75.0 nm +/- 3 nm) *)
    arrQ_diag[5] := 350.0;   (* Polydispersity index PDI (CQA: target < 0.10) *)
    arrQ_diag[6] := 15.0;    (* TFF gel layer thickness *)
    arrQ_diag[7] := 85.0;    (* Residual ethanol (CPP: target < 50 ppm) *)
    arrQ_diag[8] := 75.0;    (* Cryo-quench temperature (target 2.0 deg C) *)

    (* R Actuator Effort Penalty: Minimize unnecessary control action *)
    arrR_diag[1] := 0.85;    (* Aqueous syringe pump effort *)
    arrR_diag[2] := 1.20;    (* Ethanol syringe pump effort *)
    arrR_diag[3] := 0.45;    (* Retentate valve throttle *)
    arrR_diag[4] := 0.55;    (* Diafiltration buffer pump *)
    arrR_diag[5] := 0.65;    (* Peltier current *)
    arrR_diag[6] := 0.30;    (* Backpressure regulator *)
    arrR_diag[7] := 0.40;    (* Quench pump *)
    arrR_diag[8] := 0.35;    (* Permeate valve *)

    (* S Actuator Slew-Rate Penalty: Prevent rapid syringe acceleration / water hammer *)
    arrS_diag[1] := 4.50;    (* Syringe motor dQ/dt damping *)
    arrS_diag[2] := 6.80;    (* Organic syringe motor dQ/dt damping *)
    arrS_diag[3] := 2.10;    (* Valve stroke rate damping *)
    arrS_diag[4] := 1.80;    (* Peristaltic dosing pump ramp damping *)
    arrS_diag[5] := 3.20;    (* Peltier thermoelectric thermal shock damping *)
    arrS_diag[6] := 1.50;    (* BPR valve rate damping *)
    arrS_diag[7] := 1.20;    (* Coolant pump rate damping *)
    arrS_diag[8] := 1.60;    (* Permeate valve rate damping *)

    (* P Terminal State Penalty: 2.5x of stage cost Q *)
    FOR iRowIndex := 1 TO 8 DO
        arrP_terminal[iRowIndex] := arrQ_diag[iRowIndex] * 2.5;
    END_FOR;

    (* -------------------------------------------------------------------------
       Precomputed Unrolled MPC Gain Matrix arrK_mpc (8x8)
       Derived via Discrete Algebraic Riccati Equation (DARE) solution
       ------------------------------------------------------------------------- *)
    arrK_mpc[1, 1] := 0.4215;  arrK_mpc[1, 4] := -1.8540; arrK_mpc[1, 5] := -3.4210;
    arrK_mpc[2, 2] := 0.6580;  arrK_mpc[2, 4] := 2.1450;  arrK_mpc[2, 5] := 4.1200;  arrK_mpc[2, 7] := -0.5400;
    arrK_mpc[3, 6] := -0.8540; arrK_mpc[3, 7] := 0.3250;
    arrK_mpc[4, 7] := 1.6420;  arrK_mpc[4, 6] := -0.4120;
    arrK_mpc[5, 8] := -2.4850;
    arrK_mpc[6, 1] := -0.3150;
    arrK_mpc[7, 8] := -0.9200;
    arrK_mpc[8, 6] := 0.7450;  arrK_mpc[8, 7] := 0.8120;

    (* Initialize initial states to safe nominal baseline *)
    arrState_x[1] := 1.25;   (* Initial mixing velocity [m/s] *)
    arrState_x[2] := 11.5;   (* Initial supersaturation ratio S [-] *)
    arrState_x[3] := 1.45E8; (* Nucleation density [1/m3] *)
    arrState_x[4] := 75.0;   (* Target particle diameter [nm] *)
    arrState_x[5] := 0.080;  (* Initial PDI [-] *)
    arrState_x[6] := 1.20;   (* Gel layer thickness [um] *)
    arrState_x[7] := 25.0;   (* Residual ethanol [ppm] *)
    arrState_x[8] := 2.0;    (* Cryo temperature [deg C] *)

    FOR iRowIndex := 1 TO 8 DO
        arrInput_u[iRowIndex] := 0.0;
        arrU_prev[iRowIndex] := 0.0;
        arrDelta_u[iRowIndex] := 0.0;
    END_FOR;

    bFirstScanInitialized := TRUE;
END_IF;
'''
    sections.append(sec2)

    # =========================================================================
    # SECTION 3: PHASE 1 - 2oo3 TMR SENSOR VOTING
    # =========================================================================
    sec3 = r'''
(* ====================================================================================================================
   PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING & DISCREPANCY DEBOUNCE
   ==================================================================================================================== *)

(* --------------------------------------------------------------------------------------------------------------------
   1.1: In-Line DLS Particle Hydrodynamic Diameter (nm) - AIT_DLS_PARTICLE_DIAMETER_401A/B/C
   Voting Rule: Discrepancy tolerance <= 3.50 nm. Debounce time = 0.250 s.
   -------------------------------------------------------------------------------------------------------------------- *)
rTMR_DLS_Diam_Diff_AB := ABS(rAIT_DLS_PARTICLE_DIAMETER_401A - rAIT_DLS_PARTICLE_DIAMETER_401B);
rTMR_DLS_Diam_Diff_BC := ABS(rAIT_DLS_PARTICLE_DIAMETER_401B - rAIT_DLS_PARTICLE_DIAMETER_401C);
rTMR_DLS_Diam_Diff_CA := ABS(rAIT_DLS_PARTICLE_DIAMETER_401C - rAIT_DLS_PARTICLE_DIAMETER_401A);

bTMR_DLS_Diam_Match_AB := (rTMR_DLS_Diam_Diff_AB <= TMR_DISCREP_TOL_DIAMETER_NM);
bTMR_DLS_Diam_Match_BC := (rTMR_DLS_Diam_Diff_BC <= TMR_DISCREP_TOL_DIAMETER_NM);
bTMR_DLS_Diam_Match_CA := (rTMR_DLS_Diam_Diff_CA <= TMR_DISCREP_TOL_DIAMETER_NM);

(* Channel A discrepancy debounce timer *)
IF (NOT bTMR_DLS_Diam_Match_AB) AND (NOT bTMR_DLS_Diam_Match_CA) THEN
    rTMR_DLS_Diam_DiscrepTimer_A := rTMR_DLS_Diam_DiscrepTimer_A + T_CYCLE_SEC;
    IF rTMR_DLS_Diam_DiscrepTimer_A >= TMR_DISCREP_DEBOUNCE_TIME_SEC THEN
        bTMR_DLS_Diam_Fault_A := TRUE;
    END_IF;
ELSE
    rTMR_DLS_Diam_DiscrepTimer_A := MAX(0.0, rTMR_DLS_Diam_DiscrepTimer_A - (T_CYCLE_SEC * 2.0));
    IF bResetFaultLatches THEN
        bTMR_DLS_Diam_Fault_A := FALSE;
    END_IF;
END_IF;

(* Channel B discrepancy debounce timer *)
IF (NOT bTMR_DLS_Diam_Match_AB) AND (NOT bTMR_DLS_Diam_Match_BC) THEN
    rTMR_DLS_Diam_DiscrepTimer_B := rTMR_DLS_Diam_DiscrepTimer_B + T_CYCLE_SEC;
    IF rTMR_DLS_Diam_DiscrepTimer_B >= TMR_DISCREP_DEBOUNCE_TIME_SEC THEN
        bTMR_DLS_Diam_Fault_B := TRUE;
    END_IF;
ELSE
    rTMR_DLS_Diam_DiscrepTimer_B := MAX(0.0, rTMR_DLS_Diam_DiscrepTimer_B - (T_CYCLE_SEC * 2.0));
    IF bResetFaultLatches THEN
        bTMR_DLS_Diam_Fault_B := FALSE;
    END_IF;
END_IF;

(* Channel C discrepancy debounce timer *)
IF (NOT bTMR_DLS_Diam_Match_BC) AND (NOT bTMR_DLS_Diam_Match_CA) THEN
    rTMR_DLS_Diam_DiscrepTimer_C := rTMR_DLS_Diam_DiscrepTimer_C + T_CYCLE_SEC;
    IF rTMR_DLS_Diam_DiscrepTimer_C >= TMR_DISCREP_DEBOUNCE_TIME_SEC THEN
        bTMR_DLS_Diam_Fault_C := TRUE;
    END_IF;
ELSE
    rTMR_DLS_Diam_DiscrepTimer_C := MAX(0.0, rTMR_DLS_Diam_DiscrepTimer_C - (T_CYCLE_SEC * 2.0));
    IF bResetFaultLatches THEN
        bTMR_DLS_Diam_Fault_C := FALSE;
    END_IF;
END_IF;

(* 2oo3 Mid-Value Selection & Degraded Mode Resolution *)
IF (NOT bTMR_DLS_Diam_Fault_A) AND (NOT bTMR_DLS_Diam_Fault_B) AND (NOT bTMR_DLS_Diam_Fault_C) THEN
    (* All 3 channels healthy: True 2oo3 Median Selection *)
    IF (rAIT_DLS_PARTICLE_DIAMETER_401A >= rAIT_DLS_PARTICLE_DIAMETER_401B) THEN
        IF (rAIT_DLS_PARTICLE_DIAMETER_401B >= rAIT_DLS_PARTICLE_DIAMETER_401C) THEN
            rObs_ParticleDiameter_Voted_nm := rAIT_DLS_PARTICLE_DIAMETER_401B;
        ELSIF (rAIT_DLS_PARTICLE_DIAMETER_401A <= rAIT_DLS_PARTICLE_DIAMETER_401C) THEN
            rObs_ParticleDiameter_Voted_nm := rAIT_DLS_PARTICLE_DIAMETER_401A;
        ELSE
            rObs_ParticleDiameter_Voted_nm := rAIT_DLS_PARTICLE_DIAMETER_401C;
        END_IF;
    ELSE
        IF (rAIT_DLS_PARTICLE_DIAMETER_401A >= rAIT_DLS_PARTICLE_DIAMETER_401C) THEN
            rObs_ParticleDiameter_Voted_nm := rAIT_DLS_PARTICLE_DIAMETER_401A;
        ELSIF (rAIT_DLS_PARTICLE_DIAMETER_401B <= rAIT_DLS_PARTICLE_DIAMETER_401C) THEN
            rObs_ParticleDiameter_Voted_nm := rAIT_DLS_PARTICLE_DIAMETER_401B;
        ELSE
            rObs_ParticleDiameter_Voted_nm := rAIT_DLS_PARTICLE_DIAMETER_401C;
        END_IF;
    END_IF;
    bAlarm_TMR_DLS_DualFault := FALSE;
ELSIF bTMR_DLS_Diam_Fault_A AND (NOT bTMR_DLS_Diam_Fault_B) AND (NOT bTMR_DLS_Diam_Fault_C) THEN
    (* Channel A isolated: Average B and C *)
    rObs_ParticleDiameter_Voted_nm := (rAIT_DLS_PARTICLE_DIAMETER_401B + rAIT_DLS_PARTICLE_DIAMETER_401C) * 0.5;
    bAlarm_TMR_DLS_DualFault := FALSE;
ELSIF bTMR_DLS_Diam_Fault_B AND (NOT bTMR_DLS_Diam_Fault_A) AND (NOT bTMR_DLS_Diam_Fault_C) THEN
    (* Channel B isolated: Average A and C *)
    rObs_ParticleDiameter_Voted_nm := (rAIT_DLS_PARTICLE_DIAMETER_401A + rAIT_DLS_PARTICLE_DIAMETER_401C) * 0.5;
    bAlarm_TMR_DLS_DualFault := FALSE;
ELSIF bTMR_DLS_Diam_Fault_C AND (NOT bTMR_DLS_Diam_Fault_A) AND (NOT bTMR_DLS_Diam_Fault_B) THEN
    (* Channel C isolated: Average A and B *)
    rObs_ParticleDiameter_Voted_nm := (rAIT_DLS_PARTICLE_DIAMETER_401A + rAIT_DLS_PARTICLE_DIAMETER_401B) * 0.5;
    bAlarm_TMR_DLS_DualFault := FALSE;
ELSE
    (* Dual or triple sensor failure: Fallback to model state estimate and trip critical alarm *)
    rObs_ParticleDiameter_Voted_nm := arrState_x[4];
    bAlarm_TMR_DLS_DualFault := TRUE;
END_IF;

(* --------------------------------------------------------------------------------------------------------------------
   1.2: In-Line DLS Polydispersity Index (PDI) - AIT_DLS_PDI_402A/B/C
   Voting Rule: Discrepancy tolerance <= 0.012. Debounce time = 0.250 s.
   -------------------------------------------------------------------------------------------------------------------- *)
rTMR_DLS_PDI_Diff_AB := ABS(rAIT_DLS_PDI_402A - rAIT_DLS_PDI_402B);
rTMR_DLS_PDI_Diff_BC := ABS(rAIT_DLS_PDI_402B - rAIT_DLS_PDI_402C);
rTMR_DLS_PDI_Diff_CA := ABS(rAIT_DLS_PDI_402C - rAIT_DLS_PDI_402A);

bTMR_DLS_PDI_Match_AB := (rTMR_DLS_PDI_Diff_AB <= TMR_DISCREP_TOL_PDI);
bTMR_DLS_PDI_Match_BC := (rTMR_DLS_PDI_Diff_BC <= TMR_DISCREP_TOL_PDI);
bTMR_DLS_PDI_Match_CA := (rTMR_DLS_PDI_Diff_CA <= TMR_DISCREP_TOL_PDI);

IF (NOT bTMR_DLS_PDI_Match_AB) AND (NOT bTMR_DLS_PDI_Match_CA) THEN
    rTMR_DLS_PDI_DiscrepTimer_A := rTMR_DLS_PDI_DiscrepTimer_A + T_CYCLE_SEC;
    IF rTMR_DLS_PDI_DiscrepTimer_A >= TMR_DISCREP_DEBOUNCE_TIME_SEC THEN
        bTMR_DLS_PDI_Fault_A := TRUE;
    END_IF;
ELSE
    rTMR_DLS_PDI_DiscrepTimer_A := MAX(0.0, rTMR_DLS_PDI_DiscrepTimer_A - (T_CYCLE_SEC * 2.0));
    IF bResetFaultLatches THEN bTMR_DLS_PDI_Fault_A := FALSE; END_IF;
END_IF;

IF (NOT bTMR_DLS_PDI_Match_AB) AND (NOT bTMR_DLS_PDI_Match_BC) THEN
    rTMR_DLS_PDI_DiscrepTimer_B := rTMR_DLS_PDI_DiscrepTimer_B + T_CYCLE_SEC;
    IF rTMR_DLS_PDI_DiscrepTimer_B >= TMR_DISCREP_DEBOUNCE_TIME_SEC THEN
        bTMR_DLS_PDI_Fault_B := TRUE;
    END_IF;
ELSE
    rTMR_DLS_PDI_DiscrepTimer_B := MAX(0.0, rTMR_DLS_PDI_DiscrepTimer_B - (T_CYCLE_SEC * 2.0));
    IF bResetFaultLatches THEN bTMR_DLS_PDI_Fault_B := FALSE; END_IF;
END_IF;

IF (NOT bTMR_DLS_PDI_Match_BC) AND (NOT bTMR_DLS_PDI_Match_CA) THEN
    rTMR_DLS_PDI_DiscrepTimer_C := rTMR_DLS_PDI_DiscrepTimer_C + T_CYCLE_SEC;
    IF rTMR_DLS_PDI_DiscrepTimer_C >= TMR_DISCREP_DEBOUNCE_TIME_SEC THEN
        bTMR_DLS_PDI_Fault_C := TRUE;
    END_IF;
ELSE
    rTMR_DLS_PDI_DiscrepTimer_C := MAX(0.0, rTMR_DLS_PDI_DiscrepTimer_C - (T_CYCLE_SEC * 2.0));
    IF bResetFaultLatches THEN bTMR_DLS_PDI_Fault_C := FALSE; END_IF;
END_IF;

IF (NOT bTMR_DLS_PDI_Fault_A) AND (NOT bTMR_DLS_PDI_Fault_B) AND (NOT bTMR_DLS_PDI_Fault_C) THEN
    IF (rAIT_DLS_PDI_402A >= rAIT_DLS_PDI_402B) THEN
        IF (rAIT_DLS_PDI_402B >= rAIT_DLS_PDI_402C) THEN
            rObs_PDI_Voted := rAIT_DLS_PDI_402B;
        ELSIF (rAIT_DLS_PDI_402A <= rAIT_DLS_PDI_402C) THEN
            rObs_PDI_Voted := rAIT_DLS_PDI_402A;
        ELSE
            rObs_PDI_Voted := rAIT_DLS_PDI_402C;
        END_IF;
    ELSE
        IF (rAIT_DLS_PDI_402A >= rAIT_DLS_PDI_402C) THEN
            rObs_PDI_Voted := rAIT_DLS_PDI_402A;
        ELSIF (rAIT_DLS_PDI_402B <= rAIT_DLS_PDI_402C) THEN
            rObs_PDI_Voted := rAIT_DLS_PDI_402B;
        ELSE
            rObs_PDI_Voted := rAIT_DLS_PDI_402C;
        END_IF;
    END_IF;
ELSIF bTMR_DLS_PDI_Fault_A AND (NOT bTMR_DLS_PDI_Fault_B) AND (NOT bTMR_DLS_PDI_Fault_C) THEN
    rObs_PDI_Voted := (rAIT_DLS_PDI_402B + rAIT_DLS_PDI_402C) * 0.5;
ELSIF bTMR_DLS_PDI_Fault_B AND (NOT bTMR_DLS_PDI_Fault_A) AND (NOT bTMR_DLS_PDI_Fault_C) THEN
    rObs_PDI_Voted := (rAIT_DLS_PDI_402A + rAIT_DLS_PDI_402C) * 0.5;
ELSIF bTMR_DLS_PDI_Fault_C AND (NOT bTMR_DLS_PDI_Fault_A) AND (NOT bTMR_DLS_PDI_Fault_B) THEN
    rObs_PDI_Voted := (rAIT_DLS_PDI_402A + rAIT_DLS_PDI_402B) * 0.5;
ELSE
    rObs_PDI_Voted := arrState_x[5];
END_IF;

(* --------------------------------------------------------------------------------------------------------------------
   1.3: Aqueous Phase Flowrate (mL/min) - FT_AQUEOUS_MRNA_101A/B/C
   Voting Rule: Discrepancy tolerance <= 0.350 mL/min.
   -------------------------------------------------------------------------------------------------------------------- *)
rTMR_Flow_Aq_Diff_AB := ABS(rFT_AQUEOUS_MRNA_101A - rFT_AQUEOUS_MRNA_101B);
rTMR_Flow_Aq_Diff_BC := ABS(rFT_AQUEOUS_MRNA_101B - rFT_AQUEOUS_MRNA_101C);
rTMR_Flow_Aq_Diff_CA := ABS(rFT_AQUEOUS_MRNA_101C - rFT_AQUEOUS_MRNA_101A);

bTMR_Flow_Aq_Match_AB := (rTMR_Flow_Aq_Diff_AB <= TMR_DISCREP_TOL_FLOW_ML_MIN);
bTMR_Flow_Aq_Match_BC := (rTMR_Flow_Aq_Diff_BC <= TMR_DISCREP_TOL_FLOW_ML_MIN);
bTMR_Flow_Aq_Match_CA := (rTMR_Flow_Aq_Diff_CA <= TMR_DISCREP_TOL_FLOW_ML_MIN);

IF (NOT bTMR_Flow_Aq_Match_AB) AND (NOT bTMR_Flow_Aq_Match_CA) THEN
    rTMR_Flow_Aq_DiscrepTimer_A := rTMR_Flow_Aq_DiscrepTimer_A + T_CYCLE_SEC;
    IF rTMR_Flow_Aq_DiscrepTimer_A >= TMR_DISCREP_DEBOUNCE_TIME_SEC THEN bTMR_Flow_Aq_Fault_A := TRUE; END_IF;
ELSE
    rTMR_Flow_Aq_DiscrepTimer_A := MAX(0.0, rTMR_Flow_Aq_DiscrepTimer_A - (T_CYCLE_SEC * 2.0));
    IF bResetFaultLatches THEN bTMR_Flow_Aq_Fault_A := FALSE; END_IF;
END_IF;

IF (NOT bTMR_Flow_Aq_Match_AB) AND (NOT bTMR_Flow_Aq_Match_BC) THEN
    rTMR_Flow_Aq_DiscrepTimer_B := rTMR_Flow_Aq_DiscrepTimer_B + T_CYCLE_SEC;
    IF rTMR_Flow_Aq_DiscrepTimer_B >= TMR_DISCREP_DEBOUNCE_TIME_SEC THEN bTMR_Flow_Aq_Fault_B := TRUE; END_IF;
ELSE
    rTMR_Flow_Aq_DiscrepTimer_B := MAX(0.0, rTMR_Flow_Aq_DiscrepTimer_B - (T_CYCLE_SEC * 2.0));
    IF bResetFaultLatches THEN bTMR_Flow_Aq_Fault_B := FALSE; END_IF;
END_IF;

IF (NOT bTMR_Flow_Aq_Match_BC) AND (NOT bTMR_Flow_Aq_Match_CA) THEN
    rTMR_Flow_Aq_DiscrepTimer_C := rTMR_Flow_Aq_DiscrepTimer_C + T_CYCLE_SEC;
    IF rTMR_Flow_Aq_DiscrepTimer_C >= TMR_DISCREP_DEBOUNCE_TIME_SEC THEN bTMR_Flow_Aq_Fault_C := TRUE; END_IF;
ELSE
    rTMR_Flow_Aq_DiscrepTimer_C := MAX(0.0, rTMR_Flow_Aq_DiscrepTimer_C - (T_CYCLE_SEC * 2.0));
    IF bResetFaultLatches THEN bTMR_Flow_Aq_Fault_C := FALSE; END_IF;
END_IF;

IF (NOT bTMR_Flow_Aq_Fault_A) AND (NOT bTMR_Flow_Aq_Fault_B) AND (NOT bTMR_Flow_Aq_Fault_C) THEN
    IF (rFT_AQUEOUS_MRNA_101A >= rFT_AQUEOUS_MRNA_101B) THEN
        IF (rFT_AQUEOUS_MRNA_101B >= rFT_AQUEOUS_MRNA_101C) THEN
            rObs_AqueousFlow_Voted_ml_min := rFT_AQUEOUS_MRNA_101B;
        ELSIF (rFT_AQUEOUS_MRNA_101A <= rFT_AQUEOUS_MRNA_101C) THEN
            rObs_AqueousFlow_Voted_ml_min := rFT_AQUEOUS_MRNA_101A;
        ELSE
            rObs_AqueousFlow_Voted_ml_min := rFT_AQUEOUS_MRNA_101C;
        END_IF;
    ELSE
        IF (rFT_AQUEOUS_MRNA_101A >= rFT_AQUEOUS_MRNA_101C) THEN
            rObs_AqueousFlow_Voted_ml_min := rFT_AQUEOUS_MRNA_101A;
        ELSIF (rFT_AQUEOUS_MRNA_101B <= rFT_AQUEOUS_MRNA_101C) THEN
            rObs_AqueousFlow_Voted_ml_min := rFT_AQUEOUS_MRNA_101B;
        ELSE
            rObs_AqueousFlow_Voted_ml_min := rFT_AQUEOUS_MRNA_101C;
        END_IF;
    END_IF;
ELSIF bTMR_Flow_Aq_Fault_A AND (NOT bTMR_Flow_Aq_Fault_B) AND (NOT bTMR_Flow_Aq_Fault_C) THEN
    rObs_AqueousFlow_Voted_ml_min := (rFT_AQUEOUS_MRNA_101B + rFT_AQUEOUS_MRNA_101C) * 0.5;
ELSIF bTMR_Flow_Aq_Fault_B AND (NOT bTMR_Flow_Aq_Fault_A) AND (NOT bTMR_Flow_Aq_Fault_C) THEN
    rObs_AqueousFlow_Voted_ml_min := (rFT_AQUEOUS_MRNA_101A + rFT_AQUEOUS_MRNA_101C) * 0.5;
ELSIF bTMR_Flow_Aq_Fault_C AND (NOT bTMR_Flow_Aq_Fault_A) AND (NOT bTMR_Flow_Aq_Fault_B) THEN
    rObs_AqueousFlow_Voted_ml_min := (rFT_AQUEOUS_MRNA_101A + rFT_AQUEOUS_MRNA_101B) * 0.5;
ELSE
    rObs_AqueousFlow_Voted_ml_min := rCmd_AqueousPump_ml_min;
END_IF;

(* --------------------------------------------------------------------------------------------------------------------
   1.4: Ethanol Phase Flowrate (mL/min) - FT_ETHANOL_LIPID_102A/B/C
   Voting Rule: Discrepancy tolerance <= 0.350 mL/min.
   -------------------------------------------------------------------------------------------------------------------- *)
rTMR_Flow_Eth_Diff_AB := ABS(rFT_ETHANOL_LIPID_102A - rFT_ETHANOL_LIPID_102B);
rTMR_Flow_Eth_Diff_BC := ABS(rFT_ETHANOL_LIPID_102B - rFT_ETHANOL_LIPID_102C);
rTMR_Flow_Eth_Diff_CA := ABS(rFT_ETHANOL_LIPID_102C - rFT_ETHANOL_LIPID_102A);

bTMR_Flow_Eth_Match_AB := (rTMR_Flow_Eth_Diff_AB <= TMR_DISCREP_TOL_FLOW_ML_MIN);
bTMR_Flow_Eth_Match_BC := (rTMR_Flow_Eth_Diff_BC <= TMR_DISCREP_TOL_FLOW_ML_MIN);
bTMR_Flow_Eth_Match_CA := (rTMR_Flow_Eth_Diff_CA <= TMR_DISCREP_TOL_FLOW_ML_MIN);

IF (NOT bTMR_Flow_Eth_Match_AB) AND (NOT bTMR_Flow_Eth_Match_CA) THEN
    rTMR_Flow_Eth_DiscrepTimer_A := rTMR_Flow_Eth_DiscrepTimer_A + T_CYCLE_SEC;
    IF rTMR_Flow_Eth_DiscrepTimer_A >= TMR_DISCREP_DEBOUNCE_TIME_SEC THEN bTMR_Flow_Eth_Fault_A := TRUE; END_IF;
ELSE
    rTMR_Flow_Eth_DiscrepTimer_A := MAX(0.0, rTMR_Flow_Eth_DiscrepTimer_A - (T_CYCLE_SEC * 2.0));
    IF bResetFaultLatches THEN bTMR_Flow_Eth_Fault_A := FALSE; END_IF;
END_IF;

IF (NOT bTMR_Flow_Eth_Match_AB) AND (NOT bTMR_Flow_Eth_Match_BC) THEN
    rTMR_Flow_Eth_DiscrepTimer_B := rTMR_Flow_Eth_DiscrepTimer_B + T_CYCLE_SEC;
    IF rTMR_Flow_Eth_DiscrepTimer_B >= TMR_DISCREP_DEBOUNCE_TIME_SEC THEN bTMR_Flow_Eth_Fault_B := TRUE; END_IF;
ELSE
    rTMR_Flow_Eth_DiscrepTimer_B := MAX(0.0, rTMR_Flow_Eth_DiscrepTimer_B - (T_CYCLE_SEC * 2.0));
    IF bResetFaultLatches THEN bTMR_Flow_Eth_Fault_B := FALSE; END_IF;
END_IF;

IF (NOT bTMR_Flow_Eth_Match_BC) AND (NOT bTMR_Flow_Eth_Match_CA) THEN
    rTMR_Flow_Eth_DiscrepTimer_C := rTMR_Flow_Eth_DiscrepTimer_C + T_CYCLE_SEC;
    IF rTMR_Flow_Eth_DiscrepTimer_C >= TMR_DISCREP_DEBOUNCE_TIME_SEC THEN bTMR_Flow_Eth_Fault_C := TRUE; END_IF;
ELSE
    rTMR_Flow_Eth_DiscrepTimer_C := MAX(0.0, rTMR_Flow_Eth_DiscrepTimer_C - (T_CYCLE_SEC * 2.0));
    IF bResetFaultLatches THEN bTMR_Flow_Eth_Fault_C := FALSE; END_IF;
END_IF;

IF (NOT bTMR_Flow_Eth_Fault_A) AND (NOT bTMR_Flow_Eth_Fault_B) AND (NOT bTMR_Flow_Eth_Fault_C) THEN
    IF (rFT_ETHANOL_LIPID_102A >= rFT_ETHANOL_LIPID_102B) THEN
        IF (rFT_ETHANOL_LIPID_102B >= rFT_ETHANOL_LIPID_102C) THEN
            rObs_EthanolFlow_Voted_ml_min := rFT_ETHANOL_LIPID_102B;
        ELSIF (rFT_ETHANOL_LIPID_102A <= rFT_ETHANOL_LIPID_102C) THEN
            rObs_EthanolFlow_Voted_ml_min := rFT_ETHANOL_LIPID_102A;
        ELSE
            rObs_EthanolFlow_Voted_ml_min := rFT_ETHANOL_LIPID_102C;
        END_IF;
    ELSE
        IF (rFT_ETHANOL_LIPID_102A >= rFT_ETHANOL_LIPID_102C) THEN
            rObs_EthanolFlow_Voted_ml_min := rFT_ETHANOL_LIPID_102A;
        ELSIF (rFT_ETHANOL_LIPID_102B <= rFT_ETHANOL_LIPID_102C) THEN
            rObs_EthanolFlow_Voted_ml_min := rFT_ETHANOL_LIPID_102B;
        ELSE
            rObs_EthanolFlow_Voted_ml_min := rFT_ETHANOL_LIPID_102C;
        END_IF;
    END_IF;
ELSIF bTMR_Flow_Eth_Fault_A AND (NOT bTMR_Flow_Eth_Fault_B) AND (NOT bTMR_Flow_Eth_Fault_C) THEN
    rObs_EthanolFlow_Voted_ml_min := (rFT_ETHANOL_LIPID_102B + rFT_ETHANOL_LIPID_102C) * 0.5;
ELSIF bTMR_Flow_Eth_Fault_B AND (NOT bTMR_Flow_Eth_Fault_A) AND (NOT bTMR_Flow_Eth_Fault_C) THEN
    rObs_EthanolFlow_Voted_ml_min := (rFT_ETHANOL_LIPID_102A + rFT_ETHANOL_LIPID_102C) * 0.5;
ELSIF bTMR_Flow_Eth_Fault_C AND (NOT bTMR_Flow_Eth_Fault_A) AND (NOT bTMR_Flow_Eth_Fault_B) THEN
    rObs_EthanolFlow_Voted_ml_min := (rFT_ETHANOL_LIPID_102A + rFT_ETHANOL_LIPID_102B) * 0.5;
ELSE
    rObs_EthanolFlow_Voted_ml_min := rCmd_EthanolPump_ml_min;
END_IF;

(* --------------------------------------------------------------------------------------------------------------------
   1.5: TFF Feed Pressure Transmitter (bar) - PT_TFF_FEED_301A/B/C
   Voting Rule: Discrepancy tolerance <= 0.050 bar.
   -------------------------------------------------------------------------------------------------------------------- *)
rTMR_Press_Feed_Diff_AB := ABS(rPT_TFF_FEED_301A - rPT_TFF_FEED_301B);
rTMR_Press_Feed_Diff_BC := ABS(rPT_TFF_FEED_301B - rPT_TFF_FEED_301C);
rTMR_Press_Feed_Diff_CA := ABS(rPT_TFF_FEED_301C - rPT_TFF_FEED_301A);

bTMR_Press_Feed_Match_AB := (rTMR_Press_Feed_Diff_AB <= TMR_DISCREP_TOL_PRESSURE_BAR);
bTMR_Press_Feed_Match_BC := (rTMR_Press_Feed_Diff_BC <= TMR_DISCREP_TOL_PRESSURE_BAR);
bTMR_Press_Feed_Match_CA := (rTMR_Press_Feed_Diff_CA <= TMR_DISCREP_TOL_PRESSURE_BAR);

IF (NOT bTMR_Press_Feed_Match_AB) AND (NOT bTMR_Press_Feed_Match_CA) THEN
    rTMR_Press_Feed_DiscrepTimer_A := rTMR_Press_Feed_DiscrepTimer_A + T_CYCLE_SEC;
    IF rTMR_Press_Feed_DiscrepTimer_A >= TMR_DISCREP_DEBOUNCE_TIME_SEC THEN bTMR_Press_Feed_Fault_A := TRUE; END_IF;
ELSE
    rTMR_Press_Feed_DiscrepTimer_A := MAX(0.0, rTMR_Press_Feed_DiscrepTimer_A - (T_CYCLE_SEC * 2.0));
    IF bResetFaultLatches THEN bTMR_Press_Feed_Fault_A := FALSE; END_IF;
END_IF;

IF (NOT bTMR_Press_Feed_Match_AB) AND (NOT bTMR_Press_Feed_Match_BC) THEN
    rTMR_Press_Feed_DiscrepTimer_B := rTMR_Press_Feed_DiscrepTimer_B + T_CYCLE_SEC;
    IF rTMR_Press_Feed_DiscrepTimer_B >= TMR_DISCREP_DEBOUNCE_TIME_SEC THEN bTMR_Press_Feed_Fault_B := TRUE; END_IF;
ELSE
    rTMR_Press_Feed_DiscrepTimer_B := MAX(0.0, rTMR_Press_Feed_DiscrepTimer_B - (T_CYCLE_SEC * 2.0));
    IF bResetFaultLatches THEN bTMR_Press_Feed_Fault_B := FALSE; END_IF;
END_IF;

IF (NOT bTMR_Press_Feed_Match_BC) AND (NOT bTMR_Press_Feed_Match_CA) THEN
    rTMR_Press_Feed_DiscrepTimer_C := rTMR_Press_Feed_DiscrepTimer_C + T_CYCLE_SEC;
    IF rTMR_Press_Feed_DiscrepTimer_C >= TMR_DISCREP_DEBOUNCE_TIME_SEC THEN bTMR_Press_Feed_Fault_C := TRUE; END_IF;
ELSE
    rTMR_Press_Feed_DiscrepTimer_C := MAX(0.0, rTMR_Press_Feed_DiscrepTimer_C - (T_CYCLE_SEC * 2.0));
    IF bResetFaultLatches THEN bTMR_Press_Feed_Fault_C := FALSE; END_IF;
END_IF;

IF (NOT bTMR_Press_Feed_Fault_A) AND (NOT bTMR_Press_Feed_Fault_B) AND (NOT bTMR_Press_Feed_Fault_C) THEN
    IF (rPT_TFF_FEED_301A >= rPT_TFF_FEED_301B) THEN
        IF (rPT_TFF_FEED_301B >= rPT_TFF_FEED_301C) THEN
            rObs_TFF_FeedPressure_Voted_bar := rPT_TFF_FEED_301B;
        ELSIF (rPT_TFF_FEED_301A <= rPT_TFF_FEED_301C) THEN
            rObs_TFF_FeedPressure_Voted_bar := rPT_TFF_FEED_301A;
        ELSE
            rObs_TFF_FeedPressure_Voted_bar := rPT_TFF_FEED_301C;
        END_IF;
    ELSE
        IF (rPT_TFF_FEED_301A >= rPT_TFF_FEED_301C) THEN
            rObs_TFF_FeedPressure_Voted_bar := rPT_TFF_FEED_301A;
        ELSIF (rPT_TFF_FEED_301B <= rPT_TFF_FEED_301C) THEN
            rObs_TFF_FeedPressure_Voted_bar := rPT_TFF_FEED_301B;
        ELSE
            rObs_TFF_FeedPressure_Voted_bar := rPT_TFF_FEED_301C;
        END_IF;
    END_IF;
    bAlarm_TMR_Pressure_DualFault := FALSE;
ELSIF bTMR_Press_Feed_Fault_A AND (NOT bTMR_Press_Feed_Fault_B) AND (NOT bTMR_Press_Feed_Fault_C) THEN
    rObs_TFF_FeedPressure_Voted_bar := (rPT_TFF_FEED_301B + rPT_TFF_FEED_301C) * 0.5;
    bAlarm_TMR_Pressure_DualFault := FALSE;
ELSIF bTMR_Press_Feed_Fault_B AND (NOT bTMR_Press_Feed_Fault_A) AND (NOT bTMR_Press_Feed_Fault_C) THEN
    rObs_TFF_FeedPressure_Voted_bar := (rPT_TFF_FEED_301A + rPT_TFF_FEED_301C) * 0.5;
    bAlarm_TMR_Pressure_DualFault := FALSE;
ELSIF bTMR_Press_Feed_Fault_C AND (NOT bTMR_Press_Feed_Fault_A) AND (NOT bTMR_Press_Feed_Fault_B) THEN
    rObs_TFF_FeedPressure_Voted_bar := (rPT_TFF_FEED_301A + rPT_TFF_FEED_301B) * 0.5;
    bAlarm_TMR_Pressure_DualFault := FALSE;
ELSE
    rObs_TFF_FeedPressure_Voted_bar := 1.25;
    bAlarm_TMR_Pressure_DualFault := TRUE;
END_IF;

(* --------------------------------------------------------------------------------------------------------------------
   1.6: Cryogenic Quench Temperature RTD (deg C) - TT_CRYO_PELTIER_501A/B/C
   Voting Rule: Discrepancy tolerance <= 0.250 deg C.
   -------------------------------------------------------------------------------------------------------------------- *)
rTMR_Temp_Cryo_Diff_AB := ABS(rTT_CRYO_PELTIER_501A - rTT_CRYO_PELTIER_501B);
rTMR_Temp_Cryo_Diff_BC := ABS(rTT_CRYO_PELTIER_501B - rTT_CRYO_PELTIER_501C);
rTMR_Temp_Cryo_Diff_CA := ABS(rTT_CRYO_PELTIER_501C - rTT_CRYO_PELTIER_501A);

bTMR_Temp_Cryo_Match_AB := (rTMR_Temp_Cryo_Diff_AB <= TMR_DISCREP_TOL_TEMP_DEGC);
bTMR_Temp_Cryo_Match_BC := (rTMR_Temp_Cryo_Diff_BC <= TMR_DISCREP_TOL_TEMP_DEGC);
bTMR_Temp_Cryo_Match_CA := (rTMR_Temp_Cryo_Diff_CA <= TMR_DISCREP_TOL_TEMP_DEGC);

IF (NOT bTMR_Temp_Cryo_Match_AB) AND (NOT bTMR_Temp_Cryo_Match_CA) THEN
    rTMR_Temp_Cryo_DiscrepTimer_A := rTMR_Temp_Cryo_DiscrepTimer_A + T_CYCLE_SEC;
    IF rTMR_Temp_Cryo_DiscrepTimer_A >= TMR_DISCREP_DEBOUNCE_TIME_SEC THEN bTMR_Temp_Cryo_Fault_A := TRUE; END_IF;
ELSE
    rTMR_Temp_Cryo_DiscrepTimer_A := MAX(0.0, rTMR_Temp_Cryo_DiscrepTimer_A - (T_CYCLE_SEC * 2.0));
    IF bResetFaultLatches THEN bTMR_Temp_Cryo_Fault_A := FALSE; END_IF;
END_IF;

IF (NOT bTMR_Temp_Cryo_Match_AB) AND (NOT bTMR_Temp_Cryo_Match_BC) THEN
    rTMR_Temp_Cryo_DiscrepTimer_B := rTMR_Temp_Cryo_DiscrepTimer_B + T_CYCLE_SEC;
    IF rTMR_Temp_Cryo_DiscrepTimer_B >= TMR_DISCREP_DEBOUNCE_TIME_SEC THEN bTMR_Temp_Cryo_Fault_B := TRUE; END_IF;
ELSE
    rTMR_Temp_Cryo_DiscrepTimer_B := MAX(0.0, rTMR_Temp_Cryo_DiscrepTimer_B - (T_CYCLE_SEC * 2.0));
    IF bResetFaultLatches THEN bTMR_Temp_Cryo_Fault_B := FALSE; END_IF;
END_IF;

IF (NOT bTMR_Temp_Cryo_Match_BC) AND (NOT bTMR_Temp_Cryo_Match_CA) THEN
    rTMR_Temp_Cryo_DiscrepTimer_C := rTMR_Temp_Cryo_DiscrepTimer_C + T_CYCLE_SEC;
    IF rTMR_Temp_Cryo_DiscrepTimer_C >= TMR_DISCREP_DEBOUNCE_TIME_SEC THEN bTMR_Temp_Cryo_Fault_C := TRUE; END_IF;
ELSE
    rTMR_Temp_Cryo_DiscrepTimer_C := MAX(0.0, rTMR_Temp_Cryo_DiscrepTimer_C - (T_CYCLE_SEC * 2.0));
    IF bResetFaultLatches THEN bTMR_Temp_Cryo_Fault_C := FALSE; END_IF;
END_IF;

IF (NOT bTMR_Temp_Cryo_Fault_A) AND (NOT bTMR_Temp_Cryo_Fault_B) AND (NOT bTMR_Temp_Cryo_Fault_C) THEN
    IF (rTT_CRYO_PELTIER_501A >= rTT_CRYO_PELTIER_501B) THEN
        IF (rTT_CRYO_PELTIER_501B >= rTT_CRYO_PELTIER_501C) THEN
            rObs_CryoTemp_Voted_degC := rTT_CRYO_PELTIER_501B;
        ELSIF (rTT_CRYO_PELTIER_501A <= rTT_CRYO_PELTIER_501C) THEN
            rObs_CryoTemp_Voted_degC := rTT_CRYO_PELTIER_501A;
        ELSE
            rObs_CryoTemp_Voted_degC := rTT_CRYO_PELTIER_501C;
        END_IF;
    ELSE
        IF (rTT_CRYO_PELTIER_501A >= rTT_CRYO_PELTIER_501C) THEN
            rObs_CryoTemp_Voted_degC := rTT_CRYO_PELTIER_501A;
        ELSIF (rTT_CRYO_PELTIER_501B <= rTT_CRYO_PELTIER_501C) THEN
            rObs_CryoTemp_Voted_degC := rTT_CRYO_PELTIER_501B;
        ELSE
            rObs_CryoTemp_Voted_degC := rTT_CRYO_PELTIER_501C;
        END_IF;
    END_IF;
ELSIF bTMR_Temp_Cryo_Fault_A AND (NOT bTMR_Temp_Cryo_Fault_B) AND (NOT bTMR_Temp_Cryo_Fault_C) THEN
    rObs_CryoTemp_Voted_degC := (rTT_CRYO_PELTIER_501B + rTT_CRYO_PELTIER_501C) * 0.5;
ELSIF bTMR_Temp_Cryo_Fault_B AND (NOT bTMR_Temp_Cryo_Fault_A) AND (NOT bTMR_Temp_Cryo_Fault_C) THEN
    rObs_CryoTemp_Voted_degC := (rTT_CRYO_PELTIER_501A + rTT_CRYO_PELTIER_501C) * 0.5;
ELSIF bTMR_Temp_Cryo_Fault_C AND (NOT bTMR_Temp_Cryo_Fault_A) AND (NOT bTMR_Temp_Cryo_Fault_B) THEN
    rObs_CryoTemp_Voted_degC := (rTT_CRYO_PELTIER_501A + rTT_CRYO_PELTIER_501B) * 0.5;
ELSE
    rObs_CryoTemp_Voted_degC := arrState_x[8];
END_IF;

(* --------------------------------------------------------------------------------------------------------------------
   1.7: Residual Ethanol Analytical Sensor (ppm) - AIT_RESIDUAL_ETHANOL_601A/B/C
   Voting Rule: Discrepancy tolerance <= 4.000 ppm.
   -------------------------------------------------------------------------------------------------------------------- *)
rTMR_AIT_Eth_Diff_AB := ABS(rAIT_RESIDUAL_ETHANOL_601A - rAIT_RESIDUAL_ETHANOL_601B);
rTMR_AIT_Eth_Diff_BC := ABS(rAIT_RESIDUAL_ETHANOL_601B - rAIT_RESIDUAL_ETHANOL_601C);
rTMR_AIT_Eth_Diff_CA := ABS(rAIT_RESIDUAL_ETHANOL_601C - rAIT_RESIDUAL_ETHANOL_601A);

bTMR_AIT_Eth_Match_AB := (rTMR_AIT_Eth_Diff_AB <= TMR_DISCREP_TOL_ETH_PPM);
bTMR_AIT_Eth_Match_BC := (rTMR_AIT_Eth_Diff_BC <= TMR_DISCREP_TOL_ETH_PPM);
bTMR_AIT_Eth_Match_CA := (rTMR_AIT_Eth_Diff_CA <= TMR_DISCREP_TOL_ETH_PPM);

IF (NOT bTMR_AIT_Eth_Match_AB) AND (NOT bTMR_AIT_Eth_Match_CA) THEN
    rTMR_AIT_Eth_DiscrepTimer_A := rTMR_AIT_Eth_DiscrepTimer_A + T_CYCLE_SEC;
    IF rTMR_AIT_Eth_DiscrepTimer_A >= TMR_DISCREP_DEBOUNCE_TIME_SEC THEN bTMR_AIT_Eth_Fault_A := TRUE; END_IF;
ELSE
    rTMR_AIT_Eth_DiscrepTimer_A := MAX(0.0, rTMR_AIT_Eth_DiscrepTimer_A - (T_CYCLE_SEC * 2.0));
    IF bResetFaultLatches THEN bTMR_AIT_Eth_Fault_A := FALSE; END_IF;
END_IF;

IF (NOT bTMR_AIT_Eth_Match_AB) AND (NOT bTMR_AIT_Eth_Match_BC) THEN
    rTMR_AIT_Eth_DiscrepTimer_B := rTMR_AIT_Eth_DiscrepTimer_B + T_CYCLE_SEC;
    IF rTMR_AIT_Eth_DiscrepTimer_B >= TMR_DISCREP_DEBOUNCE_TIME_SEC THEN bTMR_AIT_Eth_Fault_B := TRUE; END_IF;
ELSE
    rTMR_AIT_Eth_DiscrepTimer_B := MAX(0.0, rTMR_AIT_Eth_DiscrepTimer_B - (T_CYCLE_SEC * 2.0));
    IF bResetFaultLatches THEN bTMR_AIT_Eth_Fault_B := FALSE; END_IF;
END_IF;

IF (NOT bTMR_AIT_Eth_Match_BC) AND (NOT bTMR_AIT_Eth_Match_CA) THEN
    rTMR_AIT_Eth_DiscrepTimer_C := rTMR_AIT_Eth_DiscrepTimer_C + T_CYCLE_SEC;
    IF rTMR_AIT_Eth_DiscrepTimer_C >= TMR_DISCREP_DEBOUNCE_TIME_SEC THEN bTMR_AIT_Eth_Fault_C := TRUE; END_IF;
ELSE
    rTMR_AIT_Eth_DiscrepTimer_C := MAX(0.0, rTMR_AIT_Eth_DiscrepTimer_C - (T_CYCLE_SEC * 2.0));
    IF bResetFaultLatches THEN bTMR_AIT_Eth_Fault_C := FALSE; END_IF;
END_IF;

IF (NOT bTMR_AIT_Eth_Fault_A) AND (NOT bTMR_AIT_Eth_Fault_B) AND (NOT bTMR_AIT_Eth_Fault_C) THEN
    IF (rAIT_RESIDUAL_ETHANOL_601A >= rAIT_RESIDUAL_ETHANOL_601B) THEN
        IF (rAIT_RESIDUAL_ETHANOL_601B >= rAIT_RESIDUAL_ETHANOL_601C) THEN
            rObs_ResidualEthanol_Voted_ppm := rAIT_RESIDUAL_ETHANOL_601B;
        ELSIF (rAIT_RESIDUAL_ETHANOL_601A <= rAIT_RESIDUAL_ETHANOL_601C) THEN
            rObs_ResidualEthanol_Voted_ppm := rAIT_RESIDUAL_ETHANOL_601A;
        ELSE
            rObs_ResidualEthanol_Voted_ppm := rAIT_RESIDUAL_ETHANOL_601C;
        END_IF;
    ELSE
        IF (rAIT_RESIDUAL_ETHANOL_601A >= rAIT_RESIDUAL_ETHANOL_601C) THEN
            rObs_ResidualEthanol_Voted_ppm := rAIT_RESIDUAL_ETHANOL_601A;
        ELSIF (rAIT_RESIDUAL_ETHANOL_601B <= rAIT_RESIDUAL_ETHANOL_601C) THEN
            rObs_ResidualEthanol_Voted_ppm := rAIT_RESIDUAL_ETHANOL_601B;
        ELSE
            rObs_ResidualEthanol_Voted_ppm := rAIT_RESIDUAL_ETHANOL_601C;
        END_IF;
    END_IF;
ELSIF bTMR_AIT_Eth_Fault_A AND (NOT bTMR_AIT_Eth_Fault_B) AND (NOT bTMR_AIT_Eth_Fault_C) THEN
    rObs_ResidualEthanol_Voted_ppm := (rAIT_RESIDUAL_ETHANOL_601B + rAIT_RESIDUAL_ETHANOL_601C) * 0.5;
ELSIF bTMR_AIT_Eth_Fault_B AND (NOT bTMR_AIT_Eth_Fault_A) AND (NOT bTMR_AIT_Eth_Fault_C) THEN
    rObs_ResidualEthanol_Voted_ppm := (rAIT_RESIDUAL_ETHANOL_601A + rAIT_RESIDUAL_ETHANOL_601C) * 0.5;
ELSIF bTMR_AIT_Eth_Fault_C AND (NOT bTMR_AIT_Eth_Fault_A) AND (NOT bTMR_AIT_Eth_Fault_B) THEN
    rObs_ResidualEthanol_Voted_ppm := (rAIT_RESIDUAL_ETHANOL_601A + rAIT_RESIDUAL_ETHANOL_601B) * 0.5;
ELSE
    rObs_ResidualEthanol_Voted_ppm := arrState_x[7];
END_IF;

(* Voted Transducer Pressure Auxiliary Variables *)
rObs_MicrofluidicInletPress_bar := (rPT_MICROFLUIDIC_INLET_201A + rPT_MICROFLUIDIC_INLET_201B + rPT_MICROFLUIDIC_INLET_201C) / 3.0;
rObs_TFF_TransmembranePressure_bar := ((rObs_TFF_FeedPressure_Voted_bar + rPT_TFF_RETENTATE_302A) * 0.5) - rPT_TFF_PERMEATE_303A;
'''
    sections.append(sec3)

    # =========================================================================
    # SECTION 4: PHASE 2 - STATE-SPACE PREDICTION & OBSERVER PROPAGATION
    # =========================================================================
    sec4 = r'''
(* ====================================================================================================================
   PHASE 2: STATE-SPACE PREDICTION (x[k+1] = A*x[k] + B*u[k]) & CYBER-PHYSICAL OBSERVER
   ==================================================================================================================== *)

(* --------------------------------------------------------------------------------------------------------------------
   2.1: Microfluidic Staggered Herringbone Hydrodynamic Physics
   - Reynolds Number: Re = (rho * v * D_h) / eta
   - Dean Vortex Number: De = Re * SQRT(D_h / (2 * R_curv))
   -------------------------------------------------------------------------------------------------------------------- *)
rCurrentTotalFlow := rObs_AqueousFlow_Voted_ml_min + rObs_EthanolFlow_Voted_ml_min;
IF rCurrentTotalFlow > 0.05 THEN
    (* Mean cross-sectional fluid velocity v = Q_tot / (Width * Height) [m/s] *)
    (* Channel geometry: 300 um x 130 um = 3.9E-8 m2. 1 mL/min = 1.66667E-8 m3/s *)
    arrState_x[1] := (rCurrentTotalFlow * 1.66667E-8) / 3.9E-8; (* Convective channel velocity [m/s] *)
ELSE
    arrState_x[1] := 0.0;
END_IF;

(* Microfluidic Reynolds Number (water-ethanol mixture density ~ 965 kg/m3, viscosity ~ 0.0014 Pa*s) *)
rObs_MicrofluidicReynoldsNumber := (965.0 * arrState_x[1] * CHANNEL_HYDRAULIC_DIAM_DH) / 0.00140;

(* Microfluidic Dean Vortex Number (Secondary chaotic swirling flow) *)
rObs_DeanNumber := rObs_MicrofluidicReynoldsNumber * SQRT(CHANNEL_HYDRAULIC_DIAM_DH / (2.0 * CHANNEL_CURVATURE_RADIUS_RC));

(* --------------------------------------------------------------------------------------------------------------------
   2.2: Nanoprecipitation Nucleation Kinetics (Arrhenius Supersaturation)
   - Supersaturation Ratio: S = C_lipid / C_solubility(T)
   - Classical Nucleation Rate: J_nuc = K_0 * exp(-DeltaG* / (k_B * T)) * (S - 1)^2
   -------------------------------------------------------------------------------------------------------------------- *)
IF rObs_AqueousFlow_Voted_ml_min > 0.1 THEN
    rTempAqueousRatioCalc := rObs_AqueousFlow_Voted_ml_min / MAX(0.1, rObs_EthanolFlow_Voted_ml_min);
ELSE
    rTempAqueousRatioCalc := 3.0;
END_IF;

(* Equilibrium lipid solubility decreases drastically as water fraction rises (Ouzo effect) *)
rBulkNanoparticleSolubility := 0.045 * EXP(-0.65 * rTempAqueousRatioCalc);
rSupersaturationEquilibriumRatio := MAX(1.0, (rAIT_UV280_LIPID_CONC_702A) / MAX(0.001, rBulkNanoparticleSolubility));
arrState_x[2] := rSupersaturationEquilibriumRatio;

(* Nucleation kinetic density rate [nuclei / (m3 * s)] *)
rArrheniusSupersatKinetics := 1.25E7 * EXP(-1850.0 / MAX(250.0, (arrState_x[8] + 273.15))) * (arrState_x[2] - 1.0) * (arrState_x[2] - 1.0);
arrState_x[3] := arrState_x[3] + (rArrheniusSupersatKinetics * T_CYCLE_SEC) - (0.05 * arrState_x[3] * T_CYCLE_SEC);

(* --------------------------------------------------------------------------------------------------------------------
   2.3: In-Line Dynamic Light Scattering Stokes-Einstein Diameter Observer
   - Stokes-Einstein: D_h = (k_B * T) / (3 * pi * eta * D_trans)
   - In-Line Cumulants Approximation: mu2 = PDI * Gamma^2
   -------------------------------------------------------------------------------------------------------------------- *)
(* Real-time DLS Cumulants second moment calculation *)
rCumulantsSecondMoment := arrState_x[5] * (1.0 / MAX(0.000001, rPhotonCorrelationTau * rPhotonCorrelationTau));

(* mRNA Encapsulation Efficiency Calculation from Dual-Wavelength UV *)
IF (rAIT_UV260_MRNA_CONC_701A > 0.05) THEN
    (* Free mRNA detected in unencapsulated filtrate vs total batch input *)
    rObs_EncapsulationEfficiency_Pct := MIN(99.9, MAX(50.0, 100.0 * (1.0 - (0.045 / MAX(0.05, rAIT_UV260_MRNA_CONC_701A)))));
ELSE
    rObs_EncapsulationEfficiency_Pct := 95.0;
END_IF;

(* --------------------------------------------------------------------------------------------------------------------
   2.4: Tangential Flow Filtration (TFF) Membrane Concentration Polarization Gel Dynamics
   - Darcy-Starling: J_v = TMP / (eta * (R_membrane + R_gel))
   - Gel layer growth: d(delta_gel)/dt = k_dep * J_v * C_bulk - k_shear * tau_w * delta_gel
   -------------------------------------------------------------------------------------------------------------------- *)
rTFF_AverageMembranePressure := MAX(0.1, rObs_TFF_TransmembranePressure_bar * 100000.0); (* Pa *)
rTFF_GelMassResistance := arrState_x[6] * 2.25E11; (* 1/m *)
rEstimatedGelMassFlux := rTFF_AverageMembranePressure / (WATER_VISCOSITY_ETA * (MEMBRANE_HYDRAULIC_RESISTANCE_RM + rTFF_GelMassResistance)); (* m/s *)
arrState_x[6] := MAX(0.05, arrState_x[6] + ((rEstimatedGelMassFlux * 0.0085) - (0.0125 * arrState_x[1] * arrState_x[6])) * T_CYCLE_SEC);
rObs_GelLayerThickness_um := arrState_x[6];

(* --------------------------------------------------------------------------------------------------------------------
   2.5: Multi-Zone Peltier Cryogenic Quench Heat Exchanger Balance
   - Peltier Cold-Junction Heat Absorption: Q_c = alpha * I * T_c - 0.5 * I^2 * R_e - K_th * (T_h - T_c)
   -------------------------------------------------------------------------------------------------------------------- *)
rHeatPumpingColdWatts := PELTIER_SEEBECK_ALPHA * rCmd_PeltierCurrent_Amps * (arrState_x[8] + 273.15);
rHeatPumpingJouleWatts := 0.5 * rCmd_PeltierCurrent_Amps * rCmd_PeltierCurrent_Amps * PELTIER_ELEC_RESISTANCE_RE;
rHeatPumpingConductWatts := PELTIER_THERMAL_CONDUCT_KTH * (rTT_PELTIER_HEATSINK_502 - arrState_x[8]);
rNetPeltierHeatExtraction := rHeatPumpingColdWatts - rHeatPumpingJouleWatts - rHeatPumpingConductWatts;

(* --------------------------------------------------------------------------------------------------------------------
   2.6: Full 8x8 Discrete State-Space Propagation & Luenberger Observer Correction
   x[k+1] = A * x[k] + B * u[k]
   x_hat[k+1] = x[k+1] + L * (y_measured - C * x[k])
   -------------------------------------------------------------------------------------------------------------------- *)
(* Copy current control commands into input vector u *)
arrInput_u[1] := rCmd_AqueousPump_ml_min;
arrInput_u[2] := rCmd_EthanolPump_ml_min;
arrInput_u[3] := rCmd_TFF_RetentateValve_Pct;
arrInput_u[4] := rCmd_TFF_DiafiltrationPump_ml_min;
arrInput_u[5] := rCmd_PeltierCurrent_Amps;
arrInput_u[6] := rCmd_MicrofluidicBPR_Pct;
arrInput_u[7] := rCmd_QuenchCirculationPump_Pct;
arrInput_u[8] := rCmd_TFF_PermeateValve_Pct;

(* Matrix Multiplication: x_next = A * x + B * u *)
FOR iRowIndex := 1 TO 8 DO
    rMatrixAccum := 0.0;
    FOR jColIndex := 1 TO 8 DO
        rMatrixAccum := rMatrixAccum + (arrA[iRowIndex, jColIndex] * arrState_x[jColIndex]);
        rMatrixAccum := rMatrixAccum + (arrB[iRowIndex, jColIndex] * arrInput_u[jColIndex]);
    END_FOR;
    arrState_x_next[iRowIndex] := rMatrixAccum;
END_FOR;

(* Output mapping: y = C * x *)
FOR iRowIndex := 1 TO 8 DO
    arrOutput_y[iRowIndex] := arrState_x[iRowIndex];
END_FOR;

(* Luenberger Observer Innovation Correction *)
arrState_x[1] := arrState_x_next[1] + (arrObserverGain_L[1] * (arrState_x[1] - arrOutput_y[1]));
arrState_x[2] := arrState_x_next[2] + (arrObserverGain_L[2] * (arrState_x[2] - arrOutput_y[2]));
arrState_x[3] := arrState_x_next[3] + (arrObserverGain_L[3] * (arrState_x[3] - arrOutput_y[3]));
arrState_x[4] := arrState_x_next[4] + (arrObserverGain_L[4] * (rObs_ParticleDiameter_Voted_nm - arrOutput_y[4]));
arrState_x[5] := arrState_x_next[5] + (arrObserverGain_L[5] * (rObs_PDI_Voted - arrOutput_y[5]));
arrState_x[6] := arrState_x_next[6] + (arrObserverGain_L[6] * (arrState_x[6] - arrOutput_y[6]));
arrState_x[7] := arrState_x_next[7] + (arrObserverGain_L[7] * (rObs_ResidualEthanol_Voted_ppm - arrOutput_y[7]));
arrState_x[8] := arrState_x_next[8] + (arrObserverGain_L[8] * (rObs_CryoTemp_Voted_degC - arrOutput_y[8]));
'''
    sections.append(sec4)

    # =========================================================================
    # SECTION 5: PHASE 3 - RECEDING-HORIZON MPC CONTROL ACTION
    # =========================================================================
    sec5 = r'''
(* ====================================================================================================================
   PHASE 3: RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) OPTIMIZATION
   ==================================================================================================================== *)

(* Target Bioprocess Reference Vector r[k] *)
arrSetpoint_r[1] := (rSet_TotalFlowRate_ml_min * 1.66667E-8) / 3.9E-8; (* Target velocity [m/s] *)
arrSetpoint_r[2] := 10.5;                             (* Target supersaturation ratio [-] *)
arrSetpoint_r[3] := 1.25E8;                            (* Target nucleation rate [1/m3] *)
arrSetpoint_r[4] := rSet_TargetParticleDiam_nm;        (* Target LNP diameter: 75.0 nm *)
arrSetpoint_r[5] := rSet_MaxAllowablePDI * 0.75;       (* Target PDI: 0.075 *)
arrSetpoint_r[6] := 1.00;                             (* Target equilibrium gel layer: 1.0 um *)
arrSetpoint_r[7] := 15.0;                             (* Target residual ethanol: 15 ppm (< 50 ppm limit) *)
arrSetpoint_r[8] := rSet_CryoTemp_degC;               (* Target cryo quench: 2.0 deg C *)

(* Compute Tracking Error Vector: e[k] = x[k] - r[k] *)
FOR iRowIndex := 1 TO 8 DO
    arrStateError_e[iRowIndex] := arrState_x[iRowIndex] - arrSetpoint_r[iRowIndex];
END_FOR;

(* Forward 5-Step Prediction Horizon Trajectory Simulator *)
FOR kHorizonIndex := 1 TO 5 DO
    FOR iRowIndex := 1 TO 8 DO
        IF kHorizonIndex = 1 THEN
            arrPredictedTraj_x[kHorizonIndex, iRowIndex] := arrState_x[iRowIndex];
        ELSE
            rCostGradient := 0.0;
            FOR jColIndex := 1 TO 8 DO
                rCostGradient := rCostGradient + (arrA[iRowIndex, jColIndex] * arrPredictedTraj_x[kHorizonIndex - 1, jColIndex]);
                rCostGradient := rCostGradient + (arrB[iRowIndex, jColIndex] * arrInput_u[jColIndex]);
            END_FOR;
            arrPredictedTraj_x[kHorizonIndex, iRowIndex] := rCostGradient;
        END_IF;
    END_FOR;
END_FOR;

(* --------------------------------------------------------------------------------------------------------------------
   Unrolled Quadratic Programming Feedback Law: delta_u = -K_mpc * e[k]
   -------------------------------------------------------------------------------------------------------------------- *)
IF bAutoEncapsulationEnable AND (NOT bSystemInFault) THEN
    FOR iRowIndex := 1 TO 8 DO
        rMatrixAccum := 0.0;
        FOR jColIndex := 1 TO 8 DO
            rMatrixAccum := rMatrixAccum + (arrK_mpc[iRowIndex, jColIndex] * arrStateError_e[jColIndex]);
        END_FOR;
        (* Apply Slew-Rate Damping from Matrix S *)
        arrDelta_u[iRowIndex] := (-rMatrixAccum) / (1.0 + (arrS_diag[iRowIndex] * T_CYCLE_SEC));
    END_FOR;

    (* ---------------------------------------------------------------------------------
       Actuator 1 & 2: Aqueous & Organic Syringe Pumps (Coordinated Flow & Ratio Lock)
       --------------------------------------------------------------------------------- *)
    (* Slew rate limiting on syringe pumps (max 2.5 mL/min/s -> 0.0125 mL/min/cycle) *)
    arrDelta_u[1] := MAX(-0.0125, MIN(0.0125, arrDelta_u[1]));
    arrDelta_u[2] := MAX(-0.0080, MIN(0.0080, arrDelta_u[2]));

    rCmd_AqueousPump_ml_min := MAX(0.0, MIN(45.0, rCmd_AqueousPump_ml_min + arrDelta_u[1]));
    rCmd_EthanolPump_ml_min := MAX(0.0, MIN(15.0, rCmd_EthanolPump_ml_min + arrDelta_u[2]));

    (* Maintain strict volumetric flow ratio 3:1 if in ramp or steady state *)
    IF (eCurrentState = 40) OR (eCurrentState = 50) OR (eCurrentState = 60) THEN
        rCmd_EthanolPump_ml_min := rCmd_AqueousPump_ml_min / rSet_FlowRatio_AqueousToEthanol;
    END_IF;

    (* ---------------------------------------------------------------------------------
       Actuator 3: TFF Retentate Proportional Pinch Valve (TMP Regulation)
       --------------------------------------------------------------------------------- *)
    arrDelta_u[3] := MAX(-0.05, MIN(0.05, arrDelta_u[3]));
    rCmd_TFF_RetentateValve_Pct := MAX(5.0, MIN(95.0, rCmd_TFF_RetentateValve_Pct + arrDelta_u[3]));

    (* ---------------------------------------------------------------------------------
       Actuator 4: TFF Diafiltration Buffer Dosing Peristaltic Pump
       --------------------------------------------------------------------------------- *)
    arrDelta_u[4] := MAX(-0.02, MIN(0.02, arrDelta_u[4]));
    IF bDiafiltrationEnable THEN
        rCmd_TFF_DiafiltrationPump_ml_min := MAX(0.0, MIN(40.0, rCmd_TFF_DiafiltrationPump_ml_min + arrDelta_u[4]));
    ELSE
        rCmd_TFF_DiafiltrationPump_ml_min := 0.0;
    END_IF;

    (* ---------------------------------------------------------------------------------
       Actuator 5: Multi-Zone Peltier Thermoelectric Current H-Bridge (-15.0 to +15.0 A)
       --------------------------------------------------------------------------------- *)
    arrDelta_u[5] := MAX(-0.025, MIN(0.025, arrDelta_u[5]));
    IF bCryoQuenchEnable THEN
        rCmd_PeltierCurrent_Amps := MAX(-15.0, MIN(15.0, rCmd_PeltierCurrent_Amps + arrDelta_u[5]));
        rCmd_QuenchCirculationPump_Pct := 85.0;
    ELSE
        rCmd_PeltierCurrent_Amps := 0.0;
        rCmd_QuenchCirculationPump_Pct := 0.0;
    END_IF;

    (* ---------------------------------------------------------------------------------
       Actuator 6 & 8: Microfluidic BPR Valve and TFF Permeate Valve
       --------------------------------------------------------------------------------- *)
    rCmd_MicrofluidicBPR_Pct := 42.5; (* Pre-throttled to maintain channel backpressure *)
    rCmd_TFF_PermeateValve_Pct := 65.0;
ELSE
    (* Open-Loop Safe Default Mode when MPC not enabled *)
    IF eCurrentState < 40 THEN
        rCmd_AqueousPump_ml_min := 0.0;
        rCmd_EthanolPump_ml_min := 0.0;
        rCmd_PeltierCurrent_Amps := 0.0;
    END_IF;
END_IF;

(* Store previous cycle inputs for slew-rate calculation *)
FOR iRowIndex := 1 TO 8 DO
    arrU_prev[iRowIndex] := arrInput_u[iRowIndex];
END_FOR;
'''
    sections.append(sec5)

    # =========================================================================
    # SECTION 6: PHASE 4 - MULTI-STAGE 12-STATE FSM
    # =========================================================================
    sec6 = r'''
(* ====================================================================================================================
   PHASE 4: MULTI-STAGE 12-STATE FINITE STATE MACHINE (FSM)
   ==================================================================================================================== *)

(* Master Safety Interlock Check *)
IF (NOT bEmergencyStopCircuit_NC) OR (NOT bContainmentIntegrity_NC) THEN
    eCurrentState := 900; (* Immediate containment isolation abort *)
END_IF;

rStateTimer_Sec := rStateTimer_Sec + T_CYCLE_SEC;

CASE eCurrentState OF

    (* ----------------------------------------------------------------------------------------------------------------
       STATE 10: SYSTEM_FLUSH_WFI (Water-For-Injection Flush & Channel Integrity Pressure Hold)
       ---------------------------------------------------------------------------------------------------------------- *)
    10:
        iCurrentStateID := 10;
        bEncapsulationActive := FALSE;
        bBatchQualifiedInSpec := FALSE;
        bCmd_DivertToWasteValve := TRUE;
        bCmd_ProductHarvestValve := FALSE;
        bCmd_WFIFlushValve := TRUE;
        bCmd_CIPCausticSupplyValve := FALSE;
        bCmd_CleanSteamSterilizeValve := FALSE;
        bCmd_EmergencyContainmentIsolate := FALSE;

        rCmd_AqueousPump_ml_min := 10.0; (* Flush aqueous line with WFI *)
        rCmd_EthanolPump_ml_min := 0.0;
        rCmd_TFF_RetentateValve_Pct := 30.0;
        rCmd_TFF_PermeateValve_Pct := 80.0;
        rCmd_PeltierCurrent_Amps := 0.0;

        (* Dwell 60.0 seconds to verify zero microfluidic leaks and purge air *)
        IF (rStateTimer_Sec >= 60.0) AND (rObs_MicrofluidicInletPress_bar < 3.20) AND bMasterRunPermissive THEN
            ePreviousState := 10;
            eCurrentState := 20; (* Proceed to buffer prime *)
            rStateTimer_Sec := 0.0;
        END_IF;

    (* ----------------------------------------------------------------------------------------------------------------
       STATE 20: PRIME_MICRO_CHANNELS (Equilibrate with pH 4.0 Sodium Acetate Buffer)
       ---------------------------------------------------------------------------------------------------------------- *)
    20:
        iCurrentStateID := 20;
        bEncapsulationActive := FALSE;
        bBatchQualifiedInSpec := FALSE;
        bCmd_DivertToWasteValve := TRUE;
        bCmd_ProductHarvestValve := FALSE;
        bCmd_WFIFlushValve := FALSE;

        rCmd_AqueousPump_ml_min := 12.0; (* Prime microchannels with working acetate buffer *)
        rCmd_EthanolPump_ml_min := 0.0;

        (* Check buffer pH and conductivity at mixer discharge *)
        IF (rStateTimer_Sec >= 45.0) AND (rQIT_BUFFER_PH_308 >= 3.90) AND (rQIT_BUFFER_PH_308 <= 4.20) THEN
            ePreviousState := 20;
            eCurrentState := 30; (* Proceed to thermal stabilization *)
            rStateTimer_Sec := 0.0;
        END_IF;

    (* ----------------------------------------------------------------------------------------------------------------
       STATE 30: TEMPERATURE_STABILIZATION (Chill Peltier Quench Block to 2.0 deg C)
       ---------------------------------------------------------------------------------------------------------------- *)
    30:
        iCurrentStateID := 30;
        bEncapsulationActive := FALSE;
        bBatchQualifiedInSpec := FALSE;
        bCmd_DivertToWasteValve := TRUE;
        bCmd_ProductHarvestValve := FALSE;

        rCmd_PeltierCurrent_Amps := 8.5; (* Active chill *)
        rCmd_QuenchCirculationPump_Pct := 100.0;

        (* Verify temperature reached 2.0 +/- 0.5 deg C and stabilized for 15 seconds *)
        IF (rObs_CryoTemp_Voted_degC <= (rSet_CryoTemp_degC + 0.5)) AND (rStateTimer_Sec >= 30.0) THEN
            ePreviousState := 30;
            eCurrentState := 40; (* Proceed to synchronized dual ramp *)
            rStateTimer_Sec := 0.0;
        END_IF;

    (* ----------------------------------------------------------------------------------------------------------------
       STATE 40: ORGANIC_AQUEOUS_SYNC_RAMP (Synchronized Servo Syringe Pump Ramp to 3:1 Ratio)
       ---------------------------------------------------------------------------------------------------------------- *)
    40:
        iCurrentStateID := 40;
        bEncapsulationActive := FALSE;
        bBatchQualifiedInSpec := FALSE;
        bCmd_DivertToWasteValve := TRUE; (* Divert startup transients to waste *)
        bCmd_ProductHarvestValve := FALSE;

        (* Coordinated linear velocity ramp *)
        rCmd_AqueousPump_ml_min := MIN(18.0, 6.0 + (rStateTimer_Sec * 1.2));
        rCmd_EthanolPump_ml_min := rCmd_AqueousPump_ml_min / rSet_FlowRatio_AqueousToEthanol;

        (* Check steady-state velocity and stable Dean vortex generation *)
        IF (rCmd_AqueousPump_ml_min >= 17.9) AND (rObs_MicrofluidicReynoldsNumber >= 200.0) AND (rStateTimer_Sec >= 15.0) THEN
            ePreviousState := 40;
            eCurrentState := 50; (* Proceed to steady-state encapsulation *)
            rStateTimer_Sec := 0.0;
        END_IF;

    (* ----------------------------------------------------------------------------------------------------------------
       STATE 50: STEADY_STATE_ENCAPSULATION (Active Closed-Loop Impingement Mixing)
       ---------------------------------------------------------------------------------------------------------------- *)
    50:
        iCurrentStateID := 50;
        bEncapsulationActive := TRUE;
        bCmd_DivertToWasteValve := TRUE; (* Diverted until DLS qualifies particle quality *)
        bCmd_ProductHarvestValve := FALSE;

        rCmd_AqueousPump_ml_min := 18.0;
        rCmd_EthanolPump_ml_min := 6.0;

        (* Transition to in-line qualification after 10.0 seconds of hydrodynamic equilibrium *)
        IF (rStateTimer_Sec >= 10.0) AND (rObs_MicrofluidicInletPress_bar >= 2.2) AND (rObs_MicrofluidicInletPress_bar <= 3.6) THEN
            ePreviousState := 50;
            eCurrentState := 60; (* Proceed to DLS qualification *)
            rStateTimer_Sec := 0.0;
        END_IF;

    (* ----------------------------------------------------------------------------------------------------------------
       STATE 60: DLS_IN_LINE_QUALIFICATION (Multi-Angle DLS Particle Size & PDI Verification)
       ---------------------------------------------------------------------------------------------------------------- *)
    60:
        iCurrentStateID := 60;
        bEncapsulationActive := TRUE;

        (* Continuous CQA evaluation: Diameter within 75.0 +/- 3.0 nm AND PDI < 0.100 *)
        IF (ABS(rObs_ParticleDiameter_Voted_nm - rSet_TargetParticleDiam_nm) <= 3.0) AND (rObs_PDI_Voted <= rSet_MaxAllowablePDI) THEN
            rContinuousInSpecTimer_Sec := rContinuousInSpecTimer_Sec + T_CYCLE_SEC;
            IF rContinuousInSpecTimer_Sec >= 10.0 THEN
                bBatchQualifiedInSpec := TRUE;
                bCmd_DivertToWasteValve := FALSE; (* Shift 3-way valve to downstream processing *)
                bCmd_ProductHarvestValve := TRUE;

                ePreviousState := 60;
                eCurrentState := 70; (* Proceed to TFF diafiltration *)
                rStateTimer_Sec := 0.0;
            END_IF;
        ELSE
            rContinuousInSpecTimer_Sec := 0.0;
            bBatchQualifiedInSpec := FALSE;
            bCmd_DivertToWasteValve := TRUE;
            bCmd_ProductHarvestValve := FALSE;

            (* If out of spec for more than 45 seconds, enter diversion hold *)
            IF rStateTimer_Sec >= 45.0 THEN
                ePreviousState := 60;
                eCurrentState := 90; (* Diversion hold *)
                rStateTimer_Sec := 0.0;
            END_IF;
        END_IF;

    (* ----------------------------------------------------------------------------------------------------------------
       STATE 70: TFF_BUFFER_EXCHANGE_DIAFILTRATION (Continuous Ethanol Clearance Diafiltration)
       ---------------------------------------------------------------------------------------------------------------- *)
    70:
        iCurrentStateID := 70;
        bEncapsulationActive := TRUE;
        bCmd_TFF_PermeateDrainValve := TRUE;

        (* Buffer dosing matching permeate volumetric removal rate *)
        rCmd_TFF_DiafiltrationPump_ml_min := 18.0;
        rDiafiltrationAccumVolume_mL := rDiafiltrationAccumVolume_mL + (rCmd_TFF_DiafiltrationPump_ml_min * (T_CYCLE_SEC / 60.0));

        (* Track cumulative validated production runtime *)
        rProductionTimer_Sec := rProductionTimer_Sec + T_CYCLE_SEC;
        rTotalProductHarvested_Liters := rTotalProductHarvested_Liters + (rCurrentTotalFlow * (T_CYCLE_SEC / 60000.0));

        (* Diafiltration completion criteria: residual ethanol < 50 ppm and target diavolumes achieved *)
        IF (rObs_ResidualEthanol_Voted_ppm <= rSet_MaxResidualEthanol_ppm) AND (rDiafiltrationAccumVolume_mL >= (rSet_DiafiltrationVolumes * 100.0)) THEN
            ePreviousState := 70;
            eCurrentState := 80; (* Proceed to cryo-quench holding *)
            rStateTimer_Sec := 0.0;
        END_IF;

        (* Safeguard: If CQA drifts during diafiltration, divert immediately *)
        IF (ABS(rObs_ParticleDiameter_Voted_nm - rSet_TargetParticleDiam_nm) > 4.5) OR (rObs_PDI_Voted > 0.115) THEN
            ePreviousState := 70;
            eCurrentState := 90; (* Divert hold *)
            rStateTimer_Sec := 0.0;
        END_IF;

    (* ----------------------------------------------------------------------------------------------------------------
       STATE 80: CRYO_PELTIER_QUENCH (Flash Cryo-Quench & Harvest Stabilization)
       ---------------------------------------------------------------------------------------------------------------- *)
    80:
        iCurrentStateID := 80;
        bEncapsulationActive := TRUE;
        bCmd_DivertToWasteValve := FALSE;
        bCmd_ProductHarvestValve := TRUE;

        (* Maintain cryo temp at 2.0 deg C (or target setpoint down to -20.0 deg C) *)
        rCmd_PeltierCurrent_Amps := 7.2;

        rProductionTimer_Sec := rProductionTimer_Sec + T_CYCLE_SEC;
        rTotalProductHarvested_Liters := rTotalProductHarvested_Liters + (rCurrentTotalFlow * (T_CYCLE_SEC / 60000.0));

        (* Check operator stop request or recipe completion *)
        IF (NOT bAutoEncapsulationEnable) OR (rTotalProductHarvested_Liters >= 50.0) THEN
            ePreviousState := 80;
            eCurrentState := 999; (* Controlled shutdown *)
            rStateTimer_Sec := 0.0;
        END_IF;

    (* ----------------------------------------------------------------------------------------------------------------
       STATE 90: OFF_SPEC_DIVERSION_HOLD (Divert Out-of-Spec Stream to Waste Container)
       ---------------------------------------------------------------------------------------------------------------- *)
    90:
        iCurrentStateID := 90;
        bEncapsulationActive := TRUE;
        bBatchQualifiedInSpec := FALSE;
        bCmd_DivertToWasteValve := TRUE;
        bCmd_ProductHarvestValve := FALSE;

        rDivertHoldTimer_Sec := rDivertHoldTimer_Sec + T_CYCLE_SEC;

        (* Attempt closed-loop MPC re-tuning *)
        IF (ABS(rObs_ParticleDiameter_Voted_nm - rSet_TargetParticleDiam_nm) <= 3.0) AND (rObs_PDI_Voted <= rSet_MaxAllowablePDI) THEN
            IF rDivertHoldTimer_Sec >= 20.0 THEN
                rDivertHoldTimer_Sec := 0.0;
                ePreviousState := 90;
                eCurrentState := 60; (* Re-qualify *)
                rStateTimer_Sec := 0.0;
            END_IF;
        ELSE
            (* If unable to recover within 120 seconds, trip to controlled shutdown *)
            IF rDivertHoldTimer_Sec >= 120.0 THEN
                rDivertHoldTimer_Sec := 0.0;
                ePreviousState := 90;
                eCurrentState := 999;
                rStateTimer_Sec := 0.0;
            END_IF;
        END_IF;

    (* ----------------------------------------------------------------------------------------------------------------
       STATE 100: SYSTEM_SIP_CIP_CYCLE (Automated 0.5M NaOH Sanitization & Clean Steam Sterilization)
       ---------------------------------------------------------------------------------------------------------------- *)
    100:
        iCurrentStateID := 100;
        bEncapsulationActive := FALSE;
        bBatchQualifiedInSpec := FALSE;
        bCIP_SIP_InProgress := TRUE;
        bCmd_DivertToWasteValve := TRUE;
        bCmd_ProductHarvestValve := FALSE;

        rCIP_StepTimer_Sec := rCIP_StepTimer_Sec + T_CYCLE_SEC;

        CASE iCIP_SubPhase OF
            0: (* Caustic 0.5M NaOH wash *)
                bCmd_CIPCausticSupplyValve := TRUE;
                bCmd_CleanSteamSterilizeValve := FALSE;
                rCmd_AqueousPump_ml_min := 25.0;
                IF rCIP_StepTimer_Sec >= 180.0 THEN
                    iCIP_SubPhase := 1;
                    rCIP_StepTimer_Sec := 0.0;
                END_IF;

            1: (* WFI high purity rinse *)
                bCmd_CIPCausticSupplyValve := FALSE;
                bCmd_WFIFlushValve := TRUE;
                rCmd_AqueousPump_ml_min := 30.0;
                IF (rCIP_StepTimer_Sec >= 120.0) AND (rQIT_BUFFER_CONDUCTIVITY_307 <= 1.5) THEN
                    iCIP_SubPhase := 2;
                    rCIP_StepTimer_Sec := 0.0;
                END_IF;

            2: (* Pure Clean Steam 121 deg C SIP thermal hold *)
                bCmd_WFIFlushValve := FALSE;
                bCmd_CleanSteamSterilizeValve := TRUE;
                rCmd_AqueousPump_ml_min := 0.0;
                IF rCIP_StepTimer_Sec >= 300.0 THEN
                    iCIP_SubPhase := 3;
                    rCIP_StepTimer_Sec := 0.0;
                END_IF;

            3: (* Sterile N2 blowdown and dry *)
                bCmd_CleanSteamSterilizeValve := FALSE;
                bCmd_NitrogenPurgeBlanketValve := TRUE;
                IF rCIP_StepTimer_Sec >= 60.0 THEN
                    bCmd_NitrogenPurgeBlanketValve := FALSE;
                    bCIP_SIP_InProgress := FALSE;
                    iCIP_SubPhase := 0;
                    ePreviousState := 100;
                    eCurrentState := 999; (* Complete *)
                    rStateTimer_Sec := 0.0;
                END_IF;
        END_CASE;

    (* ----------------------------------------------------------------------------------------------------------------
       STATE 900: CONTAINMENT_ISOLATION_ABORT (Biosafety Containment Clamp & Pressure Dump)
       ---------------------------------------------------------------------------------------------------------------- *)
    900:
        iCurrentStateID := 900;
        bSystemInFault := TRUE;
        bEncapsulationActive := FALSE;
        bBatchQualifiedInSpec := FALSE;
        bCmd_EmergencyContainmentIsolate := TRUE; (* Fire pinch clamps *)
        bCmd_DivertToWasteValve := TRUE;
        bCmd_ProductHarvestValve := FALSE;

        (* Instantaneous pump shutdown *)
        rCmd_AqueousPump_ml_min := 0.0;
        rCmd_EthanolPump_ml_min := 0.0;
        rCmd_TFF_DiafiltrationPump_ml_min := 0.0;
        rCmd_PeltierCurrent_Amps := 0.0;
        rCmd_TFF_RetentateValve_Pct := 100.0; (* Depressurize *)

        IF bEmergencyStopCircuit_NC AND bContainmentIntegrity_NC AND bResetFaultLatches THEN
            bSystemInFault := FALSE;
            bCmd_EmergencyContainmentIsolate := FALSE;
            ePreviousState := 900;
            eCurrentState := 999; (* Exit to safe shutdown *)
            rStateTimer_Sec := 0.0;
        END_IF;

    (* ----------------------------------------------------------------------------------------------------------------
       STATE 999: CONTROLLED_SHUTDOWN (Safe Orderly Park of Syringes, Depressurization & Report)
       ---------------------------------------------------------------------------------------------------------------- *)
    999:
        iCurrentStateID := 999;
        bEncapsulationActive := FALSE;
        bCmd_DivertToWasteValve := TRUE;
        bCmd_ProductHarvestValve := FALSE;

        rCmd_AqueousPump_ml_min := 0.0;
        rCmd_EthanolPump_ml_min := 0.0;
        rCmd_TFF_DiafiltrationPump_ml_min := 0.0;
        rCmd_PeltierCurrent_Amps := 0.0;
        rCmd_QuenchCirculationPump_Pct := 0.0;

        IF bSterilizationCycleReq THEN
            ePreviousState := 999;
            eCurrentState := 100; (* Enter CIP/SIP *)
            rStateTimer_Sec := 0.0;
        ELSIF bMasterRunPermissive AND bResetFaultLatches THEN
            ePreviousState := 999;
            eCurrentState := 10; (* Re-enter WFI flush *)
            rStateTimer_Sec := 0.0;
        END_IF;

END_CASE;
'''
    sections.append(sec6)

    # =========================================================================
    # SECTION 7: PHASE 5 - ISA-18.2 ALARMS & DIAGNOSTIC WORD PACKING
    # =========================================================================
    sec7 = r'''
(* ====================================================================================================================
   PHASE 5: ISA-18.2 MULTI-TIERED ALARM LADDER & DIAGNOSTIC PACKING
   ==================================================================================================================== *)

(* --------------------------------------------------------------------------------------------------------------------
   5.1: Dynamic Rate-of-Change (ROC) Calculations
   -------------------------------------------------------------------------------------------------------------------- *)
rRateOfChange_MixerPress_bar_s := (rObs_MicrofluidicInletPress_bar - rPrev_MixerPress_bar) / T_CYCLE_SEC;
rRateOfChange_PDI_per_s := (rObs_PDI_Voted - rPrev_PDI) / T_CYCLE_SEC;
rPrev_MixerPress_bar := rObs_MicrofluidicInletPress_bar;
rPrev_PDI := rObs_PDI_Voted;

IF rRateOfChange_MixerPress_bar_s >= 2.50 THEN
    bAlarm_ROC_MixerClog_High := TRUE;
ELSIF rRateOfChange_MixerPress_bar_s <= 0.50 THEN
    IF bResetFaultLatches THEN bAlarm_ROC_MixerClog_High := FALSE; END_IF;
END_IF;

IF rRateOfChange_PDI_per_s >= 0.025 THEN
    bAlarm_ROC_PrecipInstability_High := TRUE;
ELSIF rRateOfChange_PDI_per_s <= 0.005 THEN
    IF bResetFaultLatches THEN bAlarm_ROC_PrecipInstability_High := FALSE; END_IF;
END_IF;

(* --------------------------------------------------------------------------------------------------------------------
   5.2: Level 1 Alarms - Mean Particle Hydrodynamic Diameter (nm)
   -------------------------------------------------------------------------------------------------------------------- *)
IF rObs_ParticleDiameter_Voted_nm <= rAlarmSet_Diam_LL THEN
    bAlarm_Diam_LL := TRUE;
ELSIF rObs_ParticleDiameter_Voted_nm >= (rAlarmSet_Diam_LL + rAlarmSet_Diam_Deadband) THEN
    IF bResetFaultLatches THEN bAlarm_Diam_LL := FALSE; END_IF;
END_IF;

IF (rObs_ParticleDiameter_Voted_nm <= rAlarmSet_Diam_L) AND (NOT bAlarm_Diam_LL) THEN
    bAlarm_Diam_L := TRUE;
ELSIF rObs_ParticleDiameter_Voted_nm >= (rAlarmSet_Diam_L + rAlarmSet_Diam_Deadband) THEN
    bAlarm_Diam_L := FALSE;
END_IF;

IF (rObs_ParticleDiameter_Voted_nm >= rAlarmSet_Diam_H) AND (NOT bAlarm_Diam_HH) THEN
    bAlarm_Diam_H := TRUE;
ELSIF rObs_ParticleDiameter_Voted_nm <= (rAlarmSet_Diam_H - rAlarmSet_Diam_Deadband) THEN
    bAlarm_Diam_H := FALSE;
END_IF;

IF rObs_ParticleDiameter_Voted_nm >= rAlarmSet_Diam_HH THEN
    bAlarm_Diam_HH := TRUE;
ELSIF rObs_ParticleDiameter_Voted_nm <= (rAlarmSet_Diam_HH - rAlarmSet_Diam_Deadband) THEN
    IF bResetFaultLatches THEN bAlarm_Diam_HH := FALSE; END_IF;
END_IF;

(* --------------------------------------------------------------------------------------------------------------------
   5.3: Level 2 Alarms - Polydispersity Index (PDI)
   -------------------------------------------------------------------------------------------------------------------- *)
IF (rObs_PDI_Voted >= rAlarmSet_PDI_H) AND (NOT bAlarm_PDI_HH) THEN
    bAlarm_PDI_H := TRUE;
ELSIF rObs_PDI_Voted <= (rAlarmSet_PDI_H - rAlarmSet_PDI_Deadband) THEN
    bAlarm_PDI_H := FALSE;
END_IF;

IF rObs_PDI_Voted >= rAlarmSet_PDI_HH THEN
    bAlarm_PDI_HH := TRUE;
ELSIF rObs_PDI_Voted <= (rAlarmSet_PDI_HH - rAlarmSet_PDI_Deadband) THEN
    IF bResetFaultLatches THEN bAlarm_PDI_HH := FALSE; END_IF;
END_IF;

(* --------------------------------------------------------------------------------------------------------------------
   5.4: Level 3 Alarms - Microfluidic Channel Inlet Pressure
   -------------------------------------------------------------------------------------------------------------------- *)
IF (rObs_MicrofluidicInletPress_bar >= rAlarmSet_MixerPress_H) AND (NOT bAlarm_MixerPress_HH) THEN
    bAlarm_MixerPress_H := TRUE;
ELSIF rObs_MicrofluidicInletPress_bar <= (rAlarmSet_MixerPress_H - rAlarmSet_MixerPress_Deadband) THEN
    bAlarm_MixerPress_H := FALSE;
END_IF;

IF rObs_MicrofluidicInletPress_bar >= rAlarmSet_MixerPress_HH THEN
    bAlarm_MixerPress_HH := TRUE;
ELSIF rObs_MicrofluidicInletPress_bar <= (rAlarmSet_MixerPress_HH - rAlarmSet_MixerPress_Deadband) THEN
    IF bResetFaultLatches THEN bAlarm_MixerPress_HH := FALSE; END_IF;
END_IF;

(* --------------------------------------------------------------------------------------------------------------------
   5.5: Level 4 Alarms - TFF Transmembrane Pressure (TMP)
   -------------------------------------------------------------------------------------------------------------------- *)
IF rObs_TFF_TransmembranePressure_bar <= rAlarmSet_TMP_L THEN
    bAlarm_TMP_L := TRUE;
ELSIF rObs_TFF_TransmembranePressure_bar >= (rAlarmSet_TMP_L + rAlarmSet_TMP_Deadband) THEN
    bAlarm_TMP_L := FALSE;
END_IF;

IF (rObs_TFF_TransmembranePressure_bar >= rAlarmSet_TMP_H) AND (NOT bAlarm_TMP_HH) THEN
    bAlarm_TMP_H := TRUE;
ELSIF rObs_TFF_TransmembranePressure_bar <= (rAlarmSet_TMP_H - rAlarmSet_TMP_Deadband) THEN
    bAlarm_TMP_H := FALSE;
END_IF;

IF rObs_TFF_TransmembranePressure_bar >= rAlarmSet_TMP_HH THEN
    bAlarm_TMP_HH := TRUE;
ELSIF rObs_TFF_TransmembranePressure_bar <= (rAlarmSet_TMP_HH - rAlarmSet_TMP_Deadband) THEN
    IF bResetFaultLatches THEN bAlarm_TMP_HH := FALSE; END_IF;
END_IF;

(* --------------------------------------------------------------------------------------------------------------------
   5.6: Level 5 Alarms - Residual Ethanol
   -------------------------------------------------------------------------------------------------------------------- *)
IF (rObs_ResidualEthanol_Voted_ppm >= rAlarmSet_Eth_H) AND (NOT bAlarm_Eth_HH) THEN
    bAlarm_Eth_H := TRUE;
ELSIF rObs_ResidualEthanol_Voted_ppm <= (rAlarmSet_Eth_H - rAlarmSet_Eth_Deadband) THEN
    bAlarm_Eth_H := FALSE;
END_IF;

IF rObs_ResidualEthanol_Voted_ppm >= rAlarmSet_Eth_HH THEN
    bAlarm_Eth_HH := TRUE;
ELSIF rObs_ResidualEthanol_Voted_ppm <= (rAlarmSet_Eth_HH - rAlarmSet_Eth_Deadband) THEN
    IF bResetFaultLatches THEN bAlarm_Eth_HH := FALSE; END_IF;
END_IF;

(* --------------------------------------------------------------------------------------------------------------------
   5.7: Level 6 Alarms - Cryogenic Quench Temperature
   -------------------------------------------------------------------------------------------------------------------- *)
IF rObs_CryoTemp_Voted_degC <= rAlarmSet_CryoTemp_LL THEN
    bAlarm_CryoTemp_LL := TRUE;
ELSIF rObs_CryoTemp_Voted_degC >= (rAlarmSet_CryoTemp_LL + rAlarmSet_CryoTemp_Deadband) THEN
    IF bResetFaultLatches THEN bAlarm_CryoTemp_LL := FALSE; END_IF;
END_IF;

IF (rObs_CryoTemp_Voted_degC <= rAlarmSet_CryoTemp_L) AND (NOT bAlarm_CryoTemp_LL) THEN
    bAlarm_CryoTemp_L := TRUE;
ELSIF rObs_CryoTemp_Voted_degC >= (rAlarmSet_CryoTemp_L + rAlarmSet_CryoTemp_Deadband) THEN
    bAlarm_CryoTemp_L := FALSE;
END_IF;

IF (rObs_CryoTemp_Voted_degC >= rAlarmSet_CryoTemp_H) AND (NOT bAlarm_CryoTemp_HH) THEN
    bAlarm_CryoTemp_H := TRUE;
ELSIF rObs_CryoTemp_Voted_degC <= (rAlarmSet_CryoTemp_H - rAlarmSet_CryoTemp_Deadband) THEN
    bAlarm_CryoTemp_H := FALSE;
END_IF;

IF rObs_CryoTemp_Voted_degC >= rAlarmSet_CryoTemp_HH THEN
    bAlarm_CryoTemp_HH := TRUE;
ELSIF rObs_CryoTemp_Voted_degC <= (rAlarmSet_CryoTemp_HH - rAlarmSet_CryoTemp_Deadband) THEN
    IF bResetFaultLatches THEN bAlarm_CryoTemp_HH := FALSE; END_IF;
END_IF;

bAlarm_EmergencyStopTripped := NOT bEmergencyStopCircuit_NC;
bAlarm_ContainmentBreach := NOT bContainmentIntegrity_NC;

(* --------------------------------------------------------------------------------------------------------------------
   5.8: Pack ISA-18.2 Priority 1 Critical Alarms (wAlarmWord_ISA18_Critical_HH_LL)
   -------------------------------------------------------------------------------------------------------------------- *)
wAlarmWord_ISA18_Critical_HH_LL := 16#0000;
IF bAlarm_Diam_LL              THEN wAlarmWord_ISA18_Critical_HH_LL := wAlarmWord_ISA18_Critical_HH_LL OR 16#0001; END_IF;
IF bAlarm_Diam_HH              THEN wAlarmWord_ISA18_Critical_HH_LL := wAlarmWord_ISA18_Critical_HH_LL OR 16#0002; END_IF;
IF bAlarm_PDI_HH               THEN wAlarmWord_ISA18_Critical_HH_LL := wAlarmWord_ISA18_Critical_HH_LL OR 16#0004; END_IF;
IF bAlarm_MixerPress_HH        THEN wAlarmWord_ISA18_Critical_HH_LL := wAlarmWord_ISA18_Critical_HH_LL OR 16#0008; END_IF;
IF bAlarm_TMP_HH               THEN wAlarmWord_ISA18_Critical_HH_LL := wAlarmWord_ISA18_Critical_HH_LL OR 16#0010; END_IF;
IF bAlarm_Eth_HH               THEN wAlarmWord_ISA18_Critical_HH_LL := wAlarmWord_ISA18_Critical_HH_LL OR 16#0020; END_IF;
IF bAlarm_CryoTemp_LL          THEN wAlarmWord_ISA18_Critical_HH_LL := wAlarmWord_ISA18_Critical_HH_LL OR 16#0040; END_IF;
IF bAlarm_CryoTemp_HH          THEN wAlarmWord_ISA18_Critical_HH_LL := wAlarmWord_ISA18_Critical_HH_LL OR 16#0080; END_IF;
IF bAlarm_EmergencyStopTripped THEN wAlarmWord_ISA18_Critical_HH_LL := wAlarmWord_ISA18_Critical_HH_LL OR 16#0100; END_IF;
IF bAlarm_ContainmentBreach    THEN wAlarmWord_ISA18_Critical_HH_LL := wAlarmWord_ISA18_Critical_HH_LL OR 16#0200; END_IF;
IF bAlarm_TMR_DLS_DualFault    THEN wAlarmWord_ISA18_Critical_HH_LL := wAlarmWord_ISA18_Critical_HH_LL OR 16#0400; END_IF;
IF bAlarm_TMR_Pressure_DualFault THEN wAlarmWord_ISA18_Critical_HH_LL := wAlarmWord_ISA18_Critical_HH_LL OR 16#0800; END_IF;

(* --------------------------------------------------------------------------------------------------------------------
   5.9: Pack ISA-18.2 Priority 2 Warning Alarms (wAlarmWord_ISA18_Warning_H_L)
   -------------------------------------------------------------------------------------------------------------------- *)
wAlarmWord_ISA18_Warning_H_L := 16#0000;
IF bAlarm_Diam_L       THEN wAlarmWord_ISA18_Warning_H_L := wAlarmWord_ISA18_Warning_H_L OR 16#0001; END_IF;
IF bAlarm_Diam_H       THEN wAlarmWord_ISA18_Warning_H_L := wAlarmWord_ISA18_Warning_H_L OR 16#0002; END_IF;
IF bAlarm_PDI_H        THEN wAlarmWord_ISA18_Warning_H_L := wAlarmWord_ISA18_Warning_H_L OR 16#0004; END_IF;
IF bAlarm_MixerPress_H THEN wAlarmWord_ISA18_Warning_H_L := wAlarmWord_ISA18_Warning_H_L OR 16#0008; END_IF;
IF bAlarm_TMP_L        THEN wAlarmWord_ISA18_Warning_H_L := wAlarmWord_ISA18_Warning_H_L OR 16#0010; END_IF;
IF bAlarm_TMP_H        THEN wAlarmWord_ISA18_Warning_H_L := wAlarmWord_ISA18_Warning_H_L OR 16#0020; END_IF;
IF bAlarm_Eth_H        THEN wAlarmWord_ISA18_Warning_H_L := wAlarmWord_ISA18_Warning_H_L OR 16#0040; END_IF;
IF bAlarm_CryoTemp_L   THEN wAlarmWord_ISA18_Warning_H_L := wAlarmWord_ISA18_Warning_H_L OR 16#0080; END_IF;
IF bAlarm_CryoTemp_H   THEN wAlarmWord_ISA18_Warning_H_L := wAlarmWord_ISA18_Warning_H_L OR 16#0100; END_IF;

(* --------------------------------------------------------------------------------------------------------------------
   5.10: Pack Priority 3 Rate-of-Change & Dynamic Alarms (wAlarmWord_ISA18_RateOfChange_ROC)
   -------------------------------------------------------------------------------------------------------------------- *)
wAlarmWord_ISA18_RateOfChange_ROC := 16#0000;
IF bAlarm_ROC_MixerClog_High         THEN wAlarmWord_ISA18_RateOfChange_ROC := wAlarmWord_ISA18_RateOfChange_ROC OR 16#0001; END_IF;
IF bAlarm_ROC_PrecipInstability_High THEN wAlarmWord_ISA18_RateOfChange_ROC := wAlarmWord_ISA18_RateOfChange_ROC OR 16#0002; END_IF;

(* --------------------------------------------------------------------------------------------------------------------
   5.11: Pack 2oo3 TMR Sensor Health Diagnostic Matrices
   -------------------------------------------------------------------------------------------------------------------- *)
wTMR_SensorHealthWord_1 := 16#0000;
IF bTMR_DLS_Diam_Fault_A   THEN wTMR_SensorHealthWord_1 := wTMR_SensorHealthWord_1 OR 16#0001; END_IF;
IF bTMR_DLS_Diam_Fault_B   THEN wTMR_SensorHealthWord_1 := wTMR_SensorHealthWord_1 OR 16#0002; END_IF;
IF bTMR_DLS_Diam_Fault_C   THEN wTMR_SensorHealthWord_1 := wTMR_SensorHealthWord_1 OR 16#0004; END_IF;
IF bTMR_DLS_PDI_Fault_A    THEN wTMR_SensorHealthWord_1 := wTMR_SensorHealthWord_1 OR 16#0010; END_IF;
IF bTMR_DLS_PDI_Fault_B    THEN wTMR_SensorHealthWord_1 := wTMR_SensorHealthWord_1 OR 16#0020; END_IF;
IF bTMR_DLS_PDI_Fault_C    THEN wTMR_SensorHealthWord_1 := wTMR_SensorHealthWord_1 OR 16#0040; END_IF;
IF bTMR_Flow_Aq_Fault_A    THEN wTMR_SensorHealthWord_1 := wTMR_SensorHealthWord_1 OR 16#0100; END_IF;
IF bTMR_Flow_Aq_Fault_B    THEN wTMR_SensorHealthWord_1 := wTMR_SensorHealthWord_1 OR 16#0200; END_IF;
IF bTMR_Flow_Aq_Fault_C    THEN wTMR_SensorHealthWord_1 := wTMR_SensorHealthWord_1 OR 16#0400; END_IF;
IF bTMR_Flow_Eth_Fault_A   THEN wTMR_SensorHealthWord_1 := wTMR_SensorHealthWord_1 OR 16#1000; END_IF;
IF bTMR_Flow_Eth_Fault_B   THEN wTMR_SensorHealthWord_1 := wTMR_SensorHealthWord_1 OR 16#2000; END_IF;
IF bTMR_Flow_Eth_Fault_C   THEN wTMR_SensorHealthWord_1 := wTMR_SensorHealthWord_1 OR 16#4000; END_IF;

wTMR_SensorHealthWord_2 := 16#0000;
IF bTMR_Press_Feed_Fault_A THEN wTMR_SensorHealthWord_2 := wTMR_SensorHealthWord_2 OR 16#0001; END_IF;
IF bTMR_Press_Feed_Fault_B THEN wTMR_SensorHealthWord_2 := wTMR_SensorHealthWord_2 OR 16#0002; END_IF;
IF bTMR_Press_Feed_Fault_C THEN wTMR_SensorHealthWord_2 := wTMR_SensorHealthWord_2 OR 16#0004; END_IF;
IF bTMR_Temp_Cryo_Fault_A  THEN wTMR_SensorHealthWord_2 := wTMR_SensorHealthWord_2 OR 16#0010; END_IF;
IF bTMR_Temp_Cryo_Fault_B  THEN wTMR_SensorHealthWord_2 := wTMR_SensorHealthWord_2 OR 16#0020; END_IF;
IF bTMR_Temp_Cryo_Fault_C  THEN wTMR_SensorHealthWord_2 := wTMR_SensorHealthWord_2 OR 16#0040; END_IF;
IF bTMR_AIT_Eth_Fault_A    THEN wTMR_SensorHealthWord_2 := wTMR_SensorHealthWord_2 OR 16#0100; END_IF;
IF bTMR_AIT_Eth_Fault_B    THEN wTMR_SensorHealthWord_2 := wTMR_SensorHealthWord_2 OR 16#0200; END_IF;
IF bTMR_AIT_Eth_Fault_C    THEN wTMR_SensorHealthWord_2 := wTMR_SensorHealthWord_2 OR 16#0400; END_IF;

(* --------------------------------------------------------------------------------------------------------------------
   5.12: Pack Automation Status Word (wAutomationStatusWord)
   -------------------------------------------------------------------------------------------------------------------- *)
wAutomationStatusWord := 16#0000;
IF (eCurrentState = 10)  THEN wAutomationStatusWord := wAutomationStatusWord OR 16#0001; END_IF; (* Flush WFI *)
IF (eCurrentState = 20)  THEN wAutomationStatusWord := wAutomationStatusWord OR 16#0002; END_IF; (* Prime *)
IF (eCurrentState = 30)  THEN wAutomationStatusWord := wAutomationStatusWord OR 16#0004; END_IF; (* Temp Stabilize *)
IF (eCurrentState = 40)  THEN wAutomationStatusWord := wAutomationStatusWord OR 16#0008; END_IF; (* Sync Ramp *)
IF (eCurrentState = 50)  THEN wAutomationStatusWord := wAutomationStatusWord OR 16#0010; END_IF; (* Steady State *)
IF (eCurrentState = 60)  THEN wAutomationStatusWord := wAutomationStatusWord OR 16#0020; END_IF; (* DLS Qualify *)
IF (eCurrentState = 70)  THEN wAutomationStatusWord := wAutomationStatusWord OR 16#0040; END_IF; (* Diafiltration *)
IF (eCurrentState = 80)  THEN wAutomationStatusWord := wAutomationStatusWord OR 16#0080; END_IF; (* Cryo Quench *)
IF (eCurrentState = 90)  THEN wAutomationStatusWord := wAutomationStatusWord OR 16#0100; END_IF; (* Divert Hold *)
IF (eCurrentState = 100) THEN wAutomationStatusWord := wAutomationStatusWord OR 16#0200; END_IF; (* CIP / SIP *)
IF (eCurrentState = 900) THEN wAutomationStatusWord := wAutomationStatusWord OR 16#4000; END_IF; (* Containment Abort *)
IF (eCurrentState = 999) THEN wAutomationStatusWord := wAutomationStatusWord OR 16#8000; END_IF; (* Shutdown *)

tCurrentBatchRunDuration := DINT_TO_TIME(REAL_TO_DINT(rProductionTimer_Sec * 1000.0));

END_FUNCTION_BLOCK
'''
    sections.append(sec7)

    return "\n".join(sections)

if __name__ == "__main__":
    code = build_full_st_code()
    print(f"Total Generated Code Characters: {len(code)}")
