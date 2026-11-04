# -*- coding: utf-8 -*-
"""
Generator for FB_Energy_Subsea_Wellhead_HIPPS_ChokeAntiSlug
Domain: Heavy Energy & Subsea Hydrocarbon Production
System: Deep-Sea 3,000-Meter Ultra-Deepwater Subsea Production System (SPS)
"""

import os
import sys
import json
import uuid
import re

AGENT_UUID = "78709445"
OUTPUT_FILE = f"data/swarm_raw/agent_{AGENT_UUID}.json"

def generate_subsea_st_code():
    parts = []
    
    # -------------------------------------------------------------
    # 1. HEADER & DECLARATION
    # -------------------------------------------------------------
    parts.append("""FUNCTION_BLOCK FB_Energy_Subsea_Wellhead_HIPPS_ChokeAntiSlug
(*
====================================================================================================
  LUMINA CYBER-PHYSICAL AUTOMATION ARCHITECTURE - SYNTHETIC IEC 61131-3 DATASET ENGINE
  SYSTEM DESIGNATION: CPS-ENERGY-SUBSEA-3000M-HIPPS-ANTISLUG-MK-VII
  DOMAIN ASSIGNMENT: Heavy Energy & Subsea Hydrocarbon Production
  PROCESS UNIT: Deep-Sea 3,000-Meter Ultra-Deepwater Subsea Production System (SPS)
  
  PHYSICAL ARCHITECTURE & SUBSEA SPECIFICATIONS:
    - Water Depth & Ambient Environment: 3,000 meters depth, 300.0 bar abyssal hydrostatic pressure, 4.0 deg C ambient
    - Wellhead Tubing Head: 15,000 psi (1,034 bar) rated tree, Shut-In Tubing Pressure (SITP) up to 450.0 bar
    - Electro-Hydraulic Multiplexed (MUX) Subsea Control Module (SCM):
        * Dual redundant Subsea Electronics Modules (SEM-A and SEM-B)
        * High-Pressure (HP: 207 bar above ambient = 507 bar abs) and Low-Pressure (LP: 103 bar above ambient = 403 bar abs)
        * Subsea hydraulic accumulator banks with fast-acting electro-hydraulic pilot servo valves
    - High-Integrity Pressure Protection System (HIPPS):
        * IEC 61508 / IEC 61511 SIL-3 Certified Functional Safety Architecture (2oo3 voting)
        * Dual fast-acting fail-close isolation ball valves (HIPPS-XV-101 and HIPPS-XV-102)
        * Valve closure stroke time <= 2.000 seconds to isolate ANSI 900# flowline (< 155.0 bar) from 450 bar tree
        * Fast hydraulic quick-exhaust dump valves and inter-valve cavity monitoring
    - Dual-Chamber Anti-Surge Multiphase Subsea Choke Valve:
        * Tungsten carbide cage-and-sleeve trim with hydraulic stepping linear motor actuator
        * Hydrodynamic severe slugging mitigation algorithm throttling gas surges and holding back liquid slugs
    - Multiphase Flow & Process Instrumentation:
        * Wet Gas Venturi Ultrasonic Mass Flowmeter (FT_WETGAS_ULTRASONIC_301A/B/C) measuring gas and liquid mass rates
        * Fast Gamma-Ray Densitometer (DT_SLUG_GAMMA_DENSITY_401A/B/C) measuring in-situ mixture bulk density
        * Wellhead fluid temperature RTD array (TT_WELLHEAD_FLUID_201A/B/C)
        * Upstream fast pressure transmitters (PT_WELLHEAD_INLET_101A/B/C)
        * Choke downstream manifold pressure transmitters (PT_CHOKE_DOWNSTREAM_102A/B/C)
        * HIPPS intermediate cavity pressure transmitters (PT_HIPPS_INTERMEDIATE_501A/B/C)
    - Thermodynamic Methane Hydrate Mitigation:
        * Real-time calculation of Towler-Mokhatab Type-I methane gas hydrate equilibrium curve:
            T_eq = 13.385 * ln(P_bar) - 43.125  [deg C]
        * Continuous evaluation of subcooling margin Delta_T_sub = T_eq - T_fluid
        * Dynamic Monoethylene Glycol (MEG) Chemical Injection Metering Valve (CIMV) regulation
    - Subsea Multiphase Booster Pump Protection:
        * Multiphase twin-screw / helico-axial pump cavitation interlocks
        * Dynamic Net Positive Suction Head Available (NPSHA) vs Required (NPSHR) monitoring
        * Gas Volume Fraction (GVF) dynamic de-rating to prevent impeller vapor lock and cavitation erosion
    - Cyber-Physical Control Core:
        * 8x8 Discrete State-Space Model (A, B, C, D) executed at 5.0 ms deterministic cycle time
        * Receding-Horizon Model Predictive Control (MPC) with Active-Set Projected Gradient Descent
        * 2oo3 Triple Modular Redundancy (TMR) voting with bumpless degradation across 8 transmitter triplets
        * 12-Stage Operational Finite State Machine (FSM)
        * ISA-18.2 / EEMUA 191 Multi-Tiered Process Alarm Hierarchy
====================================================================================================
*)
VAR_INPUT
    (* ===================================================================================== *)
    (* 1. PRIMARY SUPERVISORY DIGITAL COMMANDS & SAFETY PERMISSIVES                          *)
    (* ===================================================================================== *)
    bEnableSystem                       : BOOL;     (* Master Subsea Production Control Permissive [bool] *)
    bEmergencyShutdown_ESD              : BOOL;     (* Active-low SIL-3 hardwired hydraulic safety trip [bool] *)
    bHippsManualTripCmd                 : BOOL;     (* Operator manual HIPPS fast isolation trip [bool] *)
    bResetFaults                        : BOOL;     (* Master alarm unlatch and safety reset command [bool] *)
    bChokeManualControlPermissive       : BOOL;     (* Permissive to allow manual choke stepping override [bool] *)
    bMegInjectionEnable                 : BOOL;     (* Enable automated dynamic MEG chemical inhibitor injection [bool] *)
    bBoosterPumpEnable                  : BOOL;     (* Subsea multiphase booster pump operational permissive [bool] *)
    bMpcAntiSlugActive                  : BOOL;     (* Enable 8-state multivariable receding-horizon MPC anti-slug solver [bool] *)
    bHippsBypassKeySwitch               : BOOL;     (* Maintenance bypass key for HIPPS routine proof testing [bool] *)
    bHydraulicHpuSupplyPermissive       : BOOL;     (* Umbilical hydraulic pressure healthy permissive [bool] *)

    (* ===================================================================================== *)
    (* 2. 2oo3 TRIPLE MODULAR REDUNDANCY: WELLHEAD TUBING HEAD PRESSURE TRANSMITTERS [bar]   *)
    (* ===================================================================================== *)
    PT_WELLHEAD_INLET_101A              : REAL;     (* Wellhead Tubing Head Pressure Channel A [bar] *)
    PT_WELLHEAD_INLET_101B              : REAL;     (* Wellhead Tubing Head Pressure Channel B [bar] *)
    PT_WELLHEAD_INLET_101C              : REAL;     (* Wellhead Tubing Head Pressure Channel C [bar] *)

    (* ===================================================================================== *)
    (* 3. 2oo3 TRIPLE MODULAR REDUNDANCY: CHOKE DOWNSTREAM MANIFOLD PRESSURE [bar]           *)
    (* ===================================================================================== *)
    PT_CHOKE_DOWNSTREAM_102A            : REAL;     (* Choke Downstream Manifold Pressure Channel A [bar] *)
    PT_CHOKE_DOWNSTREAM_102B            : REAL;     (* Choke Downstream Manifold Pressure Channel B [bar] *)
    PT_CHOKE_DOWNSTREAM_102C            : REAL;     (* Choke Downstream Manifold Pressure Channel C [bar] *)

    (* ===================================================================================== *)
    (* 4. 2oo3 TRIPLE MODULAR REDUNDANCY: WELLHEAD FLUID BORE TEMPERATURE [deg C]            *)
    (* ===================================================================================== *)
    TT_WELLHEAD_FLUID_201A              : REAL;     (* Wellhead Fluid Bore 4-Wire RTD Sensor Channel A [deg C] *)
    TT_WELLHEAD_FLUID_201B              : REAL;     (* Wellhead Fluid Bore 4-Wire RTD Sensor Channel B [deg C] *)
    TT_WELLHEAD_FLUID_201C              : REAL;     (* Wellhead Fluid Bore 4-Wire RTD Sensor Channel C [deg C] *)

    (* ===================================================================================== *)
    (* 5. 2oo3 TRIPLE MODULAR REDUNDANCY: WET GAS ULTRASONIC FLOWMETERS [kg/s]               *)
    (* ===================================================================================== *)
    FT_WETGAS_ULTRASONIC_301A           : REAL;     (* Ultrasonic Wet Gas Mass Flow Transducer Channel A [kg/s] *)
    FT_WETGAS_ULTRASONIC_301B           : REAL;     (* Ultrasonic Wet Gas Mass Flow Transducer Channel B [kg/s] *)
    FT_WETGAS_ULTRASONIC_301C           : REAL;     (* Ultrasonic Wet Gas Mass Flow Transducer Channel C [kg/s] *)

    (* ===================================================================================== *)
    (* 6. 2oo3 TRIPLE MODULAR REDUNDANCY: FAST GAMMA-RAY SLUG DENSITOMETERS [kg/m3]          *)
    (* ===================================================================================== *)
    DT_SLUG_GAMMA_DENSITY_401A          : REAL;     (* Fast Gamma-Ray Mixture Bulk Density Channel A [kg/m3] *)
    DT_SLUG_GAMMA_DENSITY_401B          : REAL;     (* Fast Gamma-Ray Mixture Bulk Density Channel B [kg/m3] *)
    DT_SLUG_GAMMA_DENSITY_401C          : REAL;     (* Fast Gamma-Ray Mixture Bulk Density Channel C [kg/m3] *)

    (* ===================================================================================== *)
    (* 7. 2oo3 TRIPLE MODULAR REDUNDANCY: HIPPS INTER-VALVE CAVITY PRESSURE [bar]            *)
    (* ===================================================================================== *)
    PT_HIPPS_INTERMEDIATE_501A          : REAL;     (* HIPPS Cavity Fast Piezoresistive Transmitter Channel A [bar] *)
    PT_HIPPS_INTERMEDIATE_501B          : REAL;     (* HIPPS Cavity Fast Piezoresistive Transmitter Channel B [bar] *)
    PT_HIPPS_INTERMEDIATE_501C          : REAL;     (* HIPPS Cavity Fast Piezoresistive Transmitter Channel C [bar] *)

    (* ===================================================================================== *)
    (* 8. 2oo3 TRIPLE MODULAR REDUNDANCY: DYNAMIC MEG CHEMICAL INJECTION FLOW [L/h]          *)
    (* ===================================================================================== *)
    FT_MEG_INHIBITOR_601A               : REAL;     (* Coriolis MEG Injection Flow Transmitter Channel A [L/h] *)
    FT_MEG_INHIBITOR_601B               : REAL;     (* Coriolis MEG Injection Flow Transmitter Channel B [L/h] *)
    FT_MEG_INHIBITOR_601C               : REAL;     (* Coriolis MEG Injection Flow Transmitter Channel C [L/h] *)

    (* ===================================================================================== *)
    (* 9. 2oo3 TRIPLE MODULAR REDUNDANCY: CHOKE VALVE ACTUATOR POSITION LVDT [%]             *)
    (* ===================================================================================== *)
    ZT_CHOKE_ACTUATOR_POS_701A          : REAL;     (* Choke Linear Position Dual-Coil LVDT Channel A [%] *)
    ZT_CHOKE_ACTUATOR_POS_701B          : REAL;     (* Choke Linear Position Dual-Coil LVDT Channel B [%] *)
    ZT_CHOKE_ACTUATOR_POS_701C          : REAL;     (* Choke Linear Position Dual-Coil LVDT Channel C [%] *)

    (* ===================================================================================== *)
    (* 10. SUBSEA HYDRAULIC POWER UNIT (HPU) & AMBIENT ABYSSAL TELEMETRY                     *)
    (* ===================================================================================== *)
    PT_HYDRAULIC_HPU_HP_bar             : REAL;     (* Subsea MUX HP Hydraulic Supply Line Pressure [bar] *)
    PT_HYDRAULIC_HPU_LP_bar             : REAL;     (* Subsea MUX LP Hydraulic Return Line Pressure [bar] *)
    PT_SUBSEA_AMBIENT_HYDROSTATIC_bar   : REAL;     (* Abyssal Seawater Ambient Hydrostatic Pressure [bar] *)
    TT_SUBSEA_SEAWATER_degC             : REAL;     (* Deepwater Ambient Ocean Seawater Temperature [deg C] *)

    (* ===================================================================================== *)
    (* 11. SUBSEA MULTIPHASE BOOSTER PUMP MONITORING TELEMETRY                               *)
    (* ===================================================================================== *)
    rBoosterPumpActualRPM               : REAL;     (* Multiphase Booster Pump Actual Rotational Speed [rpm] *)
    rBoosterPumpVibrationRMS_mms        : REAL;     (* Booster Pump Radial Bearing Vibration RMS Velocity [mm/s] *)
    rBoosterPumpSuctionPressure_bar     : REAL;     (* Booster Pump Suction Manifold Absolute Pressure [bar] *)
    rBoosterPumpMotorTemp_degC          : REAL;     (* Subsea Inverter-Fed Motor Stator Winding Temperature [deg C] *)

    (* ===================================================================================== *)
    (* 12. OPERATIONAL TARGET SETPOINTS & ENGINEERING LIMITS                                 *)
    (* ===================================================================================== *)
    rTargetManifoldPressure_bar         : REAL;     (* Target Downstream Flowline Manifold Pressure Setpoint [bar] *)
    rTargetProductionRate_kgs           : REAL;     (* Target Wellhead Hydrocarbon Mass Production Rate [kg/s] *)
    rMaxAllowableChokeSlew_pct_per_s    : REAL;     (* Maximum Choke Valve Opening/Closing Speed [%/s] *)
    rHippsTripPressureLimit_bar         : REAL;     (* IEC 61508 SIL-3 Fast HIPPS Overpressure Trip Limit [bar] *)
    rWellheadOverpressureTrip_bar       : REAL;     (* Tubing Head Severe Overpressure Safety Limit [bar] *)
    rMinHydrateMargin_degC              : REAL;     (* Minimum Permissible Thermal Margin Above Hydrate T_eq [deg C] *)
    rBoosterPumpMinNpshReq_bar          : REAL;     (* Multiphase Pump Net Positive Suction Head Required [bar] *)
    tScanCycleInterval                  : TIME := T#5MS; (* Deterministic Subsea Controller Execution Cycle [ms] *)
END_VAR
""")

    # -------------------------------------------------------------
    # 2. VAR_OUTPUT
    # -------------------------------------------------------------
    parts.append("""VAR_OUTPUT
    (* ===================================================================================== *)
    (* 1. IEC 61508 SIL-3 HIPPS DISCRETE SAFETY TRIPS & ISOLATION COMMANDS                   *)
    (* ===================================================================================== *)
    bHippsValve1_TripClose              : BOOL;     (* SIL-3 HIPPS Primary Isolation Ball Valve Fast Trip Command [bool] *)
    bHippsValve2_TripClose              : BOOL;     (* SIL-3 HIPPS Secondary Isolation Ball Valve Fast Trip Command [bool] *)
    bSubseaHydraulicDumpValve_cmd       : BOOL;     (* SCM Fast Hydraulic Dump De-energize Solenoid Command [bool] *)
    bWellheadMasterWingValve_Close      : BOOL;     (* Subsea Tree Production Wing Valve Safety Close Interlock [bool] *)

    (* ===================================================================================== *)
    (* 2. CONTINUOUS PROCESS ACTUATOR SETPOINTS & MODULATION COMMANDS                        *)
    (* ===================================================================================== *)
    rChokePositionDemand_pct            : REAL;     (* Dual-Chamber Anti-Surge Choke Actuator Stroke Demand [%] *)
    rMegInjectionRateDemand_Lh          : REAL;     (* Dynamic Chemical Injection Metering Valve Flow Demand [L/h] *)
    rBoosterPumpSpeedDemand_RPM         : REAL;     (* Multiphase Booster Pump Variable Speed Drive Command [rpm] *)
    bChokeSteppingMotorPulse            : BOOL;     (* Stepping Motor Actuator Discrete Directional Advance Pulse [bool] *)
    bChokeStepDirectionClose            : BOOL;     (* Stepping Motor Direction: TRUE=Close/Throttle, FALSE=Open [bool] *)

    (* ===================================================================================== *)
    (* 3. 2oo3 TMR VALIDATED & VOTED PROCESS VARIABLES                                       *)
    (* ===================================================================================== *)
    rVotedWellheadPressure_bar          : REAL;     (* 2oo3 Median Validated Wellhead Tubing Head Pressure [bar] *)
    rVotedChokeDownstreamPressure_bar   : REAL;     (* 2oo3 Median Validated Downstream Manifold Pressure [bar] *)
    rVotedWellheadTemp_degC             : REAL;     (* 2oo3 Median Validated Wellhead Fluid Temperature [deg C] *)
    rVotedWetGasFlow_kgs                : REAL;     (* 2oo3 Median Validated Ultrasonic Multiphase Mass Flow [kg/s] *)
    rVotedSlugDensity_kgm3              : REAL;     (* 2oo3 Median Validated Gamma-Ray Mixture Bulk Density [kg/m3] *)
    rVotedHippsPressure_bar             : REAL;     (* 2oo3 Median Validated HIPPS Cavity Intermediate Pressure [bar] *)
    rVotedMegFlow_Lh                    : REAL;     (* 2oo3 Median Validated Dynamic MEG Chemical Injection Rate [L/h] *)
    rVotedChokePosition_pct             : REAL;     (* 2oo3 Median Validated Choke Actuator LVDT Actual Stroke [%] *)

    (* ===================================================================================== *)
    (* 4. CYBER-PHYSICAL OBSERVERS, HYDRODYNAMICS & THERMODYNAMIC METRICS                    *)
    (* ===================================================================================== *)
    rChokePressureDrop_bar              : REAL;     (* Differential Pressure Drop Across Choke Valve (P_wh - P_dn) [bar] *)
    rCalculatedGasVolumeFraction_GVF    : REAL;     (* In-Situ Gas Volume Fraction from Gamma Densitometer [-] *)
    rEstimatedLiquidHoldup              : REAL;     (* Hydrodynamic Drift-Flux Liquid Holdup Fraction (1 - GVF) [-] *)
    rHydrateEquilibriumTemp_degC        : REAL;     (* Towler-Mokhatab Thermodynamic Hydrate Formation Boundary [deg C] *)
    rHydrateSubcoolingMargin_degC       : REAL;     (* Thermal Margin Above Hydrate Formation Zone (T_fluid - T_eq) [deg C] *)
    rCalculatedMegConcentration_wtPct   : REAL;     (* Effective Aqueous Phase MEG Inhibitor Weight Concentration [%] *)
    rBoosterPumpNPSHMargin_bar          : REAL;     (* Multiphase Pump Net Positive Suction Head Margin (NPSHA - NPSHR) [bar] *)
    rSluggingSeverityIndex              : REAL;     (* Hydrodynamic Slugging Severity Metric (RMS Pressure Variance) [%] *)
    rMpcObjectiveCostJ                  : REAL;     (* Evaluated Quadratic Cost Functional in MPC Optimizer [-] *)

    (* ===================================================================================== *)
    (* 5. ISA-18.2 ALARM WORDS, STATUS REGISTERS & FAULT DIAGNOSTICS                         *)
    (* ===================================================================================== *)
    bSystemReady                        : BOOL;     (* All Subsea Permissives and Hydraulic Pressures Healthy [bool] *)
    bSystemRunning                      : BOOL;     (* Well Producing Steadily Through Anti-Surge Choke [bool] *)
    bHippsTripped                       : BOOL;     (* SIL-3 HIPPS Overpressure Fast Isolation Tripped [bool] *)
    bActiveSluggingMitigationActive     : BOOL;     (* Anti-Surge MPC Choke Damping Algorithm Actively Modulating [bool] *)
    bHydrateInhibitionWarning           : BOOL;     (* Subcooling Approaching Hydrate Boundary Envelope [bool] *)
    bPumpCavitationMitigationActive     : BOOL;     (* Booster Pump Speed Curtailed Due to Low NPSH Margin [bool] *)
    bTMRSensorDegradedMode              : BOOL;     (* At Least One 2oo3 Sensor Triplet Operating in Degraded 1oo2 [bool] *)
    eActiveFsmStateCode                 : INT;      (* Active 12-Stage Finite State Machine Operational Step Code [-] *)
    dwSystemStatusWord                  : DWORD;    (* Bit-Packed Subsea Control Module Operational Modes & Permissives *)
    dwAlarmWord1_Trips                  : DWORD;    (* Bit-Packed SIL-3 Safety Shutdowns, HIPPS Trips, ESD *)
    dwAlarmWord2_ProcessAlarms          : DWORD;    (* Bit-Packed Process Level Boundary Alarms (HH, H, L, LL, ROC) *)
    dwWarningWord                       : DWORD;    (* Bit-Packed Advisory Alarms (Hydrate risk, Cavitation, Slug wave) *)
    dwTMR_DegradationWord               : DWORD;    (* Bit-Packed 2oo3 Sensor Channel Integrity & Fault Health *)
END_VAR
""")

    # -------------------------------------------------------------
    # 3. VAR (State-Space, MPC, TMR, FSM, Timers, Internal Math)
    # -------------------------------------------------------------
    parts.append("""VAR
    (* ===================================================================================== *)
    (* 1. 8x8 DISCRETE CYBER-PHYSICAL STATE-SPACE MATRICES                                   *)
    (* States x:                                                                             *)
    (*   x[1]: Wellhead Tubing Pressure Deviation Delta_P_wh [bar]                           *)
    (*   x[2]: Downstream Manifold Pressure Deviation Delta_P_dn [bar]                       *)
    (*   x[3]: Choke Inflow Hydrodynamic Liquid Slug Holdup Delta_H_L [m3]                   *)
    (*   x[4]: Multiphase Mixture Mass Flow Rate Deviation Delta_m_dot [kg/s]                *)
    (*   x[5]: Choke Throat Fluid Temperature Deviation Delta_T_fluid [deg C]                *)
    (*   x[6]: Aqueous Phase MEG Chemical Concentration Delta_W_meg [wt%]                    *)
    (*   x[7]: Subsea Booster Pump Generated Differential Head Delta_H_pump [bar]            *)
    (*   x[8]: SCM Electro-Hydraulic Umbilical Pilot Pressure Delta_P_hyd [bar]              *)
    (* Inputs u:                                                                             *)
    (*   u[1]: Anti-Surge Choke Valve Actuator Stroke Command Delta_z_choke [%]              *)
    (*   u[2]: Multiphase Booster Pump Variable Frequency Speed Delta_N_pump [rpm]           *)
    (*   u[3]: Dynamic Chemical Injection Metering Valve (CIMV) Delta_z_meg [%]              *)
    (*   u[4]: Subsea MUX Pilot Hydraulic Solenoid Modulation Delta_u_hyd [%]                *)
    (* ===================================================================================== *)
    matA                                : ARRAY[1..8, 1..8] OF REAL; (* Discrete State Transition Matrix A (8x8) *)
    matB                                : ARRAY[1..8, 1..4] OF REAL; (* Discrete Actuator Coupling Matrix B (8x4) *)
    matC                                : ARRAY[1..8, 1..8] OF REAL; (* State Observation Output Matrix C (8x8) *)
    matD                                : ARRAY[1..8, 1..4] OF REAL; (* Direct Feedthrough Matrix D (8x4) *)

    (* Model Predictive Control (MPC) Cost Weighting Tensors *)
    matQ                                : ARRAY[1..8, 1..8] OF REAL; (* State Deviation Penalty Weights (8x8) *)
    matR                                : ARRAY[1..4, 1..4] OF REAL; (* Actuator Effort Rate Penalties (4x4) *)
    matP                                : ARRAY[1..8, 1..8] OF REAL; (* Terminal Horizon Penalty Weights (8x8) *)

    (* Real-Time State Space Vectors & Control Trajectories *)
    xState                              : ARRAY[1..8] OF REAL;       (* Current Estimated State Vector *)
    xNextState                          : ARRAY[1..8] OF REAL;       (* One-Step Ahead State Space Prediction *)
    xSetpoint                           : ARRAY[1..8] OF REAL;       (* Target State Space Reference Trajectory *)
    xTrackingError                      : ARRAY[1..8] OF REAL;       (* Error Vector (xState - xSetpoint) *)
    uActuator                           : ARRAY[1..4] OF REAL;       (* Current Commanded Control Vector *)
    uPrevious                           : ARRAY[1..4] OF REAL;       (* Prior Scan Control Vector *)
    uLowerLimit                         : ARRAY[1..4] OF REAL;       (* Hard Lower Actuator Bounds *)
    uUpperLimit                         : ARRAY[1..4] OF REAL;       (* Hard Upper Actuator Bounds *)
    deltaUMaxLimit                      : ARRAY[1..4] OF REAL;       (* Maximum Slew Rate Constraints per Scan *)

    (* Active-Set Projected Gradient Descent Optimization Arrays *)
    xPredictedHorizon                   : ARRAY[1..4, 1..8] OF REAL; (* 4-Step Receding Horizon State Trajectory *)
    rMpcGradient                        : ARRAY[1..4] OF REAL;       (* Cost Functional Gradient Vector *)
    rMpcStepSize                        : REAL := 0.00045;           (* Gradient Descent Search Step Coefficient *)
    rStateCostAccumulator               : REAL := 0.0;               (* Accumulated State Deviation Cost *)
    rActuatorCostAccumulator            : REAL := 0.0;               (* Accumulated Control Effort Cost *)
    bMatrixInitialized                  : BOOL := FALSE;             (* Cold-Start Matrix Population Latch *)

    (* Matrix Loop Indices *)
    iRow                                : INT := 1;
    jCol                                : INT := 1;
    kState                              : INT := 1;
    mInput                              : INT := 1;
    iHorizonStep                        : INT := 1;
    iMpcIteration                       : INT := 1;

    (* ===================================================================================== *)
    (* 2. 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) CHANNEL INTEGRITY & TIMERS                    *)
    (* ===================================================================================== *)
    (* Wellhead Pressure TMR Channel Discrepancy Bank *)
    rDev_PT101_AB                       : REAL := 0.0;
    rDev_PT101_BC                       : REAL := 0.0;
    rDev_PT101_CA                       : REAL := 0.0;
    tDiscrepancy_PT101_AB               : TON;
    tDiscrepancy_PT101_BC               : TON;
    tDiscrepancy_PT101_CA               : TON;
    bFault_PT101_A                      : BOOL := FALSE;
    bFault_PT101_B                      : BOOL := FALSE;
    bFault_PT101_C                      : BOOL := FALSE;
    iHealthyCount_PT101                 : INT := 3;

    (* Downstream Manifold Pressure TMR Channel Discrepancy Bank *)
    rDev_PT102_AB                       : REAL := 0.0;
    rDev_PT102_BC                       : REAL := 0.0;
    rDev_PT102_CA                       : REAL := 0.0;
    tDiscrepancy_PT102_AB               : TON;
    tDiscrepancy_PT102_BC               : TON;
    tDiscrepancy_PT102_CA               : TON;
    bFault_PT102_A                      : BOOL := FALSE;
    bFault_PT102_B                      : BOOL := FALSE;
    bFault_PT102_C                      : BOOL := FALSE;
    iHealthyCount_PT102                 : INT := 3;

    (* Wellhead Fluid Temperature TMR Channel Discrepancy Bank *)
    rDev_TT201_AB                       : REAL := 0.0;
    rDev_TT201_BC                       : REAL := 0.0;
    rDev_TT201_CA                       : REAL := 0.0;
    tDiscrepancy_TT201_AB               : TON;
    tDiscrepancy_TT201_BC               : TON;
    tDiscrepancy_TT201_CA               : TON;
    bFault_TT201_A                      : BOOL := FALSE;
    bFault_TT201_B                      : BOOL := FALSE;
    bFault_TT201_C                      : BOOL := FALSE;
    iHealthyCount_TT201                 : INT := 3;

    (* Wet Gas Ultrasonic Flowmeter TMR Channel Discrepancy Bank *)
    rDev_FT301_AB                       : REAL := 0.0;
    rDev_FT301_BC                       : REAL := 0.0;
    rDev_FT301_CA                       : REAL := 0.0;
    tDiscrepancy_FT301_AB               : TON;
    tDiscrepancy_FT301_BC               : TON;
    tDiscrepancy_FT301_CA               : TON;
    bFault_FT301_A                      : BOOL := FALSE;
    bFault_FT301_B                      : BOOL := FALSE;
    bFault_FT301_C                      : BOOL := FALSE;
    iHealthyCount_FT301                 : INT := 3;

    (* Gamma-Ray Slug Densitometer TMR Channel Discrepancy Bank *)
    rDev_DT401_AB                       : REAL := 0.0;
    rDev_DT401_BC                       : REAL := 0.0;
    rDev_DT401_CA                       : REAL := 0.0;
    tDiscrepancy_DT401_AB               : TON;
    tDiscrepancy_DT401_BC               : TON;
    tDiscrepancy_DT401_CA               : TON;
    bFault_DT401_A                      : BOOL := FALSE;
    bFault_DT401_B                      : BOOL := FALSE;
    bFault_DT401_C                      : BOOL := FALSE;
    iHealthyCount_DT401                 : INT := 3;

    (* HIPPS Intermediate Cavity Pressure TMR Channel Discrepancy Bank *)
    rDev_PT501_AB                       : REAL := 0.0;
    rDev_PT501_BC                       : REAL := 0.0;
    rDev_PT501_CA                       : REAL := 0.0;
    tDiscrepancy_PT501_AB               : TON;
    tDiscrepancy_PT501_BC               : TON;
    tDiscrepancy_PT501_CA               : TON;
    bFault_PT501_A                      : BOOL := FALSE;
    bFault_PT501_B                      : BOOL := FALSE;
    bFault_PT501_C                      : BOOL := FALSE;
    iHealthyCount_PT501                 : INT := 3;

    (* Dynamic MEG Chemical Flow TMR Channel Discrepancy Bank *)
    rDev_FT601_AB                       : REAL := 0.0;
    rDev_FT601_BC                       : REAL := 0.0;
    rDev_FT601_CA                       : REAL := 0.0;
    tDiscrepancy_FT601_AB               : TON;
    tDiscrepancy_FT601_BC               : TON;
    tDiscrepancy_FT601_CA               : TON;
    bFault_FT601_A                      : BOOL := FALSE;
    bFault_FT601_B                      : BOOL := FALSE;
    bFault_FT601_C                      : BOOL := FALSE;
    iHealthyCount_FT601                 : INT := 3;

    (* Choke Position LVDT TMR Channel Discrepancy Bank *)
    rDev_ZT701_AB                       : REAL := 0.0;
    rDev_ZT701_BC                       : REAL := 0.0;
    rDev_ZT701_CA                       : REAL := 0.0;
    tDiscrepancy_ZT701_AB               : TON;
    tDiscrepancy_ZT701_BC               : TON;
    tDiscrepancy_ZT701_CA               : TON;
    bFault_ZT701_A                      : BOOL := FALSE;
    bFault_ZT701_B                      : BOOL := FALSE;
    bFault_ZT701_C                      : BOOL := FALSE;
    iHealthyCount_ZT701                 : INT := 3;

    (* TMR Discrepancy Threshold Constants *)
    c_TmrTol_WellheadPress_bar          : REAL := 2.50;  (* Upstream Wellhead Pressure Tolerance [bar] *)
    c_TmrTol_ManifoldPress_bar          : REAL := 1.80;  (* Downstream Manifold Pressure Tolerance [bar] *)
    c_TmrTol_FluidTemp_degC             : REAL := 2.00;  (* Wellhead Bore Fluid Temperature Tolerance [deg C] *)
    c_TmrTol_WetGasFlow_kgs             : REAL := 3.50;  (* Wet Gas Ultrasonic Mass Flow Tolerance [kg/s] *)
    c_TmrTol_SlugDensity_kgm3           : REAL := 35.0;  (* Fast Gamma-Ray Bulk Density Tolerance [kg/m3] *)
    c_TmrTol_HippsPress_bar             : REAL := 2.50;  (* HIPPS Fast Cavity Pressure Tolerance [bar] *)
    c_TmrTol_MegFlow_Lh                 : REAL := 1.50;  (* MEG Chemical Coriolis Flow Tolerance [L/h] *)
    c_TmrTol_ChokePos_pct               : REAL := 2.00;  (* Choke Linear Stroke LVDT Tolerance [%] *)
    c_TmrPersistenceTime                : TIME := T#200MS; (* Discrepancy Persistence Debounce Window *)

    (* ===================================================================================== *)
    (* 3. HYDRODYNAMIC DRIFT-FLUX, THERMODYNAMIC HYDRATE & CAVITATION REGISTERS              *)
    (* ===================================================================================== *)
    (* Multiphase Fluid Phase Physical Constants *)
    c_GasDensityStandard_kgm3           : REAL := 82.50;   (* Natural Gas Density at 100 bar, 40 deg C [kg/m3] *)
    c_OilCondensateDensity_kgm3         : REAL := 785.0;   (* Hydrocarbon Condensate Phase Density [kg/m3] *)
    c_FormationWaterDensity_kgm3        : REAL := 1045.0;  (* Subsea Saline Formation Water Density [kg/m3] *)
    c_PureMegDensity_kgm3               : REAL := 1115.0;  (* Pure Monoethylene Glycol Solution Density [kg/m3] *)
    c_MegMolarMass_gmol                 : REAL := 62.07;   (* MEG Molecular Weight [g/mol] *)
    c_WaterMolarMass_gmol               : REAL := 18.015;  (* Pure Water Molecular Weight [g/mol] *)
    c_HammerschmidtConstant             : REAL := 2220.0;  (* Nielsen-Hammerschmidt Hydrate Depression Factor *)
    c_AtmosphericPressure_bar           : REAL := 1.01325; (* Standard Sea-Level Atmospheric Pressure [bar] *)
    c_GravitationalAccel_ms2            : REAL := 9.80665; (* Gravitational Acceleration Constant [m/s2] *)

    (* Hydrodynamic Drift-Flux Slugging Calculation Registers *)
    rMixtureVelocity_ms                 : REAL := 0.0;     (* Superficial Mixture Velocity U_m [m/s] *)
    rGasSuperficialVelocity_ms          : REAL := 0.0;     (* Superficial Gas Velocity U_sg [m/s] *)
    rLiquidSuperficialVelocity_ms       : REAL := 0.0;     (* Superficial Liquid Velocity U_sl [m/s] *)
    rDriftVelocity_ms                   : REAL := 0.0;     (* Bubble Drift Velocity v_gj [m/s] *)
    rDistributionParameterC0            : REAL := 1.20;    (* Zuber-Findlay Profile Distribution Factor *)
    rPipeCrossSectionArea_m2            : REAL := 0.0452;  (* 10-Inch Internal Diameter Riser Spool Area [m2] *)
    rSluggingPressureBuffer             : ARRAY[1..10] OF REAL; (* FIFO History Buffer for Slugging RMS Variance *)
    iSlugBufferIndex                    : INT := 1;
    rMeanChokeDeltaP_bar                : REAL := 0.0;
    rVarianceSumChokeDeltaP             : REAL := 0.0;
    rStandardDeviationDeltaP            : REAL := 0.0;

    (* Towler-Mokhatab Hydrate Boundary & MEG Dosing Math *)
    rNaturalLogPressure                 : REAL := 0.0;
    rTaylorSeriesLogTerm                : REAL := 0.0;
    rNormalizedPressureArg              : REAL := 0.0;
    rRequiredHydrateDepression_degC     : REAL := 0.0;
    rTargetMegConcentration_wtPct       : REAL := 0.0;
    rEstimatedWaterCutFraction          : REAL := 0.125;   (* Formation Water Mass Fraction in Produced Stream *)
    rWaterMassFlowRate_kgh              : REAL := 0.0;
    rStoichiometricMegDemand_Lh         : REAL := 0.0;

    (* Subsea Multiphase Booster Pump NPSH & Cavitation Tracking *)
    rFluidVaporPressure_bar             : REAL := 28.50;   (* Hydrocarbon Bubble Point / Vapor Pressure [bar] *)
    rPumpSuctionSpecificHead_m          : REAL := 0.0;     (* P_suction / (rho_mix * g) Dynamic Head [m] *)
    rPumpVaporSpecificHead_m            : REAL := 0.0;     (* P_vapor / (rho_mix * g) Vapor Head [m] *)
    rPumpSuctionDynamicVelocityHead_m   : REAL := 0.0;     (* v^2 / (2*g) Suction Kinetic Velocity Head [m] *)
    rCalculatedNpsha_m                  : REAL := 0.0;     (* Net Positive Suction Head Available [m] *)
    rCalculatedNpshr_m                  : REAL := 0.0;     (* Net Positive Suction Head Required at Operating RPM [m] *)
    rNpshMarginHead_m                   : REAL := 0.0;     (* Net Margin Head (NPSHA - NPSHR) [m] *)
    rPumpSpeedDerateFactor              : REAL := 1.00;    (* Cavitation Throttle Derate Multiplier (0.2 to 1.0) *)

    (* ===================================================================================== *)
    (* 4. 12-STAGE OPERATIONAL FINITE STATE MACHINE (FSM) REGISTERS                          *)
    (* ===================================================================================== *)
    eCurrentState                       : INT := 10;       (* Active Operating State Register *)
    ePreviousState                      : INT := 10;       (* Historical Prior Scan State Register *)
    tStateDwellTimer                    : TON;             (* State Dwell and Transition Settle Timer *)
    tHippsStrokeTimer                   : TON;             (* HIPPS Full Stroke Closure Verification Timer *)
    tChokeWarmupRampTimer               : TON;             (* Choke Valve Initial Cracking Ramp Timer *)
    tHydraulicAccumulatorTimer          : TON;             (* Subsea Hydraulic Reservoir Pressure Charge Timer *)
    tMegLinePrimeTimer                  : TON;             (* Subsea Umbilical MEG Chemical Header Purge Timer *)
    tWellheadUnlatchTimer               : TON;             (* Tree Mandrel Hydraulic Lock Verification Timer *)
    tSlugStabilizationTimer             : TON;             (* Slugging Disturbance Damping Settle Timer *)

    (* Choke Linear Stepping Motor Actuation Engine *)
    rActualChokePosition_pct            : REAL := 0.0;     (* Filtered Choke Actual Position *)
    rChokeTargetPosition_pct            : REAL := 0.0;     (* Ramped / Commanded Anti-Surge Choke Stroke *)
    rChokePositionError_pct             : REAL := 0.0;     (* Position Tracking Deviation *)
    iChokeStepAccumulator               : INT := 0;        (* Discrete Hydraulic Pulse Counter *)
    bChokePulseTrigger                  : BOOL := FALSE;   (* Discrete Motor Advance Trigger *)
    tChokePulseTimer                    : TON;             (* Stepping Actuator Pulse Duration Timer *)

    (* ===================================================================================== *)
    (* 5. ISA-18.2 ALARM LIMITS, DEADBANDS & TRIP REGISTERS                                  *)
    (* ===================================================================================== *)
    (* Alarm Trip Limits *)
    c_Limit_HippsTrip_HH_bar            : REAL := 148.0;   (* SIL-3 Fast HIPPS Overpressure Shutdown [bar] *)
    c_Limit_ManifoldPress_H_bar         : REAL := 135.0;   (* Downstream Manifold High Pressure Warning [bar] *)
    c_Limit_ManifoldPress_L_bar         : REAL := 65.0;    (* Downstream Manifold Low Pressure Warning [bar] *)
    c_Limit_ManifoldPress_LL_bar        : REAL := 45.0;    (* Downstream Manifold Severe Depressurization [bar] *)
    c_Limit_WellheadPress_HH_bar        : REAL := 430.0;   (* Wellhead Tubing Head Extreme Overpressure Trip [bar] *)
    c_Limit_WellheadPress_H_bar         : REAL := 380.0;   (* Wellhead Tubing Head High Alarm [bar] *)
    c_Limit_WellheadTemp_LL_degC        : REAL := 8.00;    (* Severe Cold Hydrocarbon Inflow Hydrate Danger [deg C] *)
    c_Limit_WellheadTemp_L_degC         : REAL := 14.00;   (* Low Wellhead Temperature Advisory [deg C] *)
    c_Limit_WellheadTemp_HH_degC        : REAL := 95.00;   (* High Fluid Temperature Elastomer Hazard [deg C] *)
    c_Limit_WetGasFlow_HH_kgs           : REAL := 85.00;   (* Extreme Production Flow Erosion Trip Limit [kg/s] *)
    c_Limit_WetGasFlow_H_kgs            : REAL := 72.00;   (* High Production Flow Warning [kg/s] *)
    c_Limit_SlugSeverity_H_pct          : REAL := 25.00;   (* Active Slugging Warning Inception Threshold [%] *)
    c_Limit_SlugSeverity_HH_pct         : REAL := 45.00;   (* Severe Liquid Slug Impact Hazard Threshold [%] *)
    c_Limit_PumpVibration_HH_mms        : REAL := 12.50;   (* Booster Pump Bearing Mechanical Trip Limit [mm/s] *)
    c_Limit_PumpVibration_H_mms         : REAL := 7.50;    (* Booster Pump Elevated Vibration Advisory [mm/s] *)
    c_Limit_HpuSupplyPress_LL_bar       : REAL := 340.0;   (* Hydraulic Supply Pressure Loss Safety Trip [bar] *)
    c_Limit_HpuSupplyPress_L_bar        : REAL := 380.0;   (* Hydraulic Supply Pressure Low Advisory [bar] *)

    (* Deadband Hysteresis Margins *)
    c_Deadband_Pressure_bar             : REAL := 1.50;
    c_Deadband_Temperature_degC         : REAL := 0.80;
    c_Deadband_Flow_kgs                 : REAL := 1.20;
    c_Deadband_Vibration_mms            : REAL := 0.50;

    (* Process Alarm Delay Debounce Timers *)
    tTimer_HippsOverpressure            : TON;
    tTimer_WellheadOverpressure         : TON;
    tTimer_WellheadColdHypothermia      : TON;
    tTimer_PumpVibrationTrip            : TON;
    tTimer_HpuPressureLoss              : TON;
    tTimer_SluggingSevere               : TON;

    (* General Scan Execution Counter *)
    iCycleCounter                       : DINT := 0;
END_VAR
""")

    return "".join(parts)

if __name__ == "__main__":
    print("Testing subsea decl generation...")
    res = generate_subsea_st_code()
    print("Length of decl:", len(res))
