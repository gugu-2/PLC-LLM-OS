import sys
import os
import json
import re

def generate_full_fadec_code():
    code_lines = []

    # 1. Opening declaration & comprehensive specification
    code_lines.append("""FUNCTION_BLOCK FB_Aerospace_Turbofan_DualChannelFADEC_110klbf
(*
========================================================================================================================
LUMINA CYBER-PHYSICAL PROPULSION SYSTEMS - SYNTHETIC DATASET V7 MAX-PERSONA
COMMERCIAL AEROSPACE PROPULSION DIVISION - 110,000 LBF HIGH-BYPASS TURBOFAN DUAL-CHANNEL FADEC / EEC
========================================================================================================================
SYSTEM SPECIFICATION & ARCHITECTURAL OVERVIEW:
  - Propulsion Plant Classification:
    * Twin-Spool Axial-Flow High-Bypass Commercial Turbofan Engine.
    * Sea-Level Static Maximum Rated Takeoff Thrust: 110,000 lbf (489.3 kN).
    * Bypass Ratio (BPR): 11.2 : 1 at Sea-Level Standard Takeoff rating.
    * Overall Pressure Ratio (OPR): 42.5 : 1 at Top-of-Climb (TOC) flight envelope.
    * Fan Architecture: 134-inch (3.40 m) outer diameter, 18 solid diffusion-bonded 3D curved hollow-titanium blades.
    * Fan / LP Booster (LPC): 1-stage Fan + 3-stage booster driven by 6-stage Low Pressure Turbine (LPT).
    * Core High-Pressure Compressor (HPC): 10-stage axial-flow compressor with active Variable Stator Vanes (VSV)
      on inlet guide vanes (IGV) and stages 1-3, plus 4-port Variable Bleed Valves (VBV) on stage 7 booster bleed.
    * High-Pressure Turbine (HPT): 2-stage air-cooled single-crystal superalloy turbine driving HPC via outer spool.
    * Low-Pressure Rotor Spool (N1): Rated speed 100.0% = 2,850 RPM; Maximum overspeed trip redline 106.0% = 3,021 RPM.
    * High-Pressure Rotor Spool (N2): Rated speed 100.0% = 10,800 RPM; Maximum overspeed trip redline 105.0% = 11,340 RPM.
  - Dual-Channel Fault-Tolerant Engine Electronic Controller (EEC / FADEC):
    * Fully Independent Dual-Channel Architecture (Channel A and Channel B) housed in an environmentally sealed,
      convection-and-fuel-cooled cast aluminum enclosure mounted on the fan casing.
    * ARINC-429 Cross-Channel Data Link (CCDL) operating at 100 kbps for sub-millisecond parameter exchange, cross-lane
      discrepancy checking, sensor parity arbitration, and bumpless master/standby command handover.
    * Independent isolated internal DC-DC power converters powered by engine-driven dual-stator permanent magnet
      alternator (PMA) above 10% N2, with 28V DC aircraft emergency essential bus battery backup.
    * Fail-Operational / Fail-Safe redundant flight control dispatch capability complying with RTCA DO-178C Level A.
  - Fuel Delivery & Metering Valve Subsystem:
    * High-Pressure Hydro-Mechanical Unit (HMU) driven by engine accessory gearbox (AGB).
    * Dual-stage fuel pump: low-pressure centrifugal boost pump and high-pressure positive-displacement spur gear pump.
    * Fuel Metering Valve (FMV): Precision flapper-nozzle electrohydraulic servo valve (EHSV) / dual-coil torque motor
      regulating fuel metering orifice area (Afmv) with closed-loop linear variable differential transformer (LVDT).
    * Delta-P Regulating Valve: Spring-balanced diaphragm spool holding constant differential pressure (approx 42 psid)
      across FMV orifice, establishing volumetric fuel flow directly proportional to FMV spool displacement.
    * Independent Electronic Overspeed Shutoff Solenoid Valve (OSV) with hardwired discrete trip circuit.
  - Core Aerodynamic Flow Stability (VSV & VBV Automation):
    * High-Pressure Compressor Variable Stator Vanes (VSV): High-pressure fuel-actuated dual push-pull torque tubes
      and unison rings modulating stator blade pitch angles (-15.0 deg closed to +35.0 deg fully open) as a non-linear
      function of corrected high-pressure spool speed (N2 / sqrt(Theta2)) and compressor inlet temperature (Tt2).
    * Variable Bleed Valves (VBV): Electrohydraulic hinge-flapper bleed doors venting compressor booster discharge
      air into the fan bypass duct during low-power deceleration, dry motoring, and ground idle to prevent rotating stall.
  - High-Pressure and Low-Pressure Active Turbine Clearance Control (HPTACC & LPTACC):
    * Modulated fan bypass duct bleed air ducted through thermal distributor manifold manifolds onto outer turbine cases.
    * Precision electrohydraulic modulating butterfly valves varying cooling mass air flow onto case structural rings.
    * Regulates radial casing shrinkage to precisely track centrifugal and thermal blade tip growth, locking radial
      tip clearance to 0.25 mm (+/- 0.05 mm) during high-altitude cruise, reducing TSFC by up to 1.8% and preserving EGT.
  - Exhaust Gas Temperature (EGT) Surveillance & Hot-Section Life Management:
    * Eight (8) dual-element Type K (Chromel-Alumel) ungrounded thermocouple probes circumferentially disposed in the
      Low-Pressure Turbine inlet plane (T4.5 / Station 4.5), totaling 16 independent sensing junctions.
    * Real-time extraction of spatial peak EGT, arithmetic mean, circumferential temperature spread, rate-of-rise (dEGT/dt),
      and continuous Larson-Miller creep / thermal-mechanical fatigue cycle consumption accumulation.
  - Cyber-Physical Mathematical Formulation:
    * 16x16 Discrete State-Space Model:
      State Vector x = [N1, N2, Ps3, Tt3, Pcomb, Tcomb, T4.5_EGT, Tcase_HPT, Tdisk_HPT, Clr_HPT, Tcase_LPT, Clr_LPT, Pos_VBV, Ang_VSV, Pos_FMV, Thrust_Net]
      Input Vector u = [i_FMV_mA, AngCmd_VSV, PosCmd_VBV, ModCmd_HPTACC, ModCmd_LPTACC, Cmd_Starter, Cmd_Igniters, Cmd_Reverser]
      Output Vector y = [Thrust_Net, Ratio_Spool, FuelFlow_Wf, SurgeMargin_pct, EGT_Margin, ClrErr_HPT, TSFC, EquivRatio]
    * Receding-Horizon Model Predictive Control (MPC): Quadratic cost minimization tracking pilot thrust demand (TLA)
      while strictly enforcing compressor surge limits ((Wf/Ps3)_accel), lean blow-out boundaries ((Wf/Ps3)_decel),
      rotor shaft acceleration rates, and maximum structural turbine gas temperatures.
    * 2oo3 Triple Modular Redundancy (TMR) voting across N1 optical pickups, N2 resolvers, and Ps3 transducers.
    * 12-Stage Comprehensive Industrial Aerospace Finite State Machine (DO-178C operational sequencing).
    * ISA-18.2 / MIL-STD-882E Alarm Matrix with bit-packed ARINC-429 telemetry transmission words.
========================================================================================================================
*)
VAR_INPUT
    (* Pilot Command & Airframe Flight Conditions *)
    rThrottleLeverAngle_deg          : REAL;    (* [deg] Cockpit Power Management Throttle Lever Angle (0.0=Idle, 45.0=Takeoff) *)
    rMachNumber                     : REAL;    (* [Mach] Flight Mach Number (0.00 to 0.92) *)
    rAltitude_ft                    : REAL;    (* [ft] Pressure Altitude (-1000.0 to 45000.0) *)
    rTotalAirTemp_degC              : REAL;    (* [deg C] Total Air Temperature TAT at Engine Inlet Station 2 (-60.0 to 55.0) *)
    rTotalPressure_psia             : REAL;    (* [psia] Total Pressure Pt2 at Engine Inlet Station 2 (2.0 to 16.0) *)
    rBleedAirDemand_pct             : REAL;    (* [%] Airframe Environmental Control System Customer Bleed Extraction (0 to 100) *)
    rElectricalAccessoryLoad_kVA    : REAL;    (* [kVA] Airframe IDG Electrical Power Generation Load (0.0 to 125.0) *)
    bWeightOnWheels                 : BOOL;    (* [bool] Landing Gear Ground Proximity WOW Switch: TRUE=Ground, FALSE=Flight *)
    bThrustReverserArmed            : BOOL;    (* [bool] Flight Deck Thrust Reverser System Master Deploy Arming Interlock *)

    (* Channel Management & Cross-Lane Status *)
    bChannelA_MasterRequest         : BOOL;    (* [bool] Pilot / Maintenance Override Channel A Primary Control Selector *)
    bChannelA_HealthOK              : BOOL;    (* [bool] Channel A Hardware Built-In-Test BIT Integrity OK Discrete *)
    bChannelB_HealthOK              : BOOL;    (* [bool] Channel B Hardware Built-In-Test BIT Integrity OK Discrete *)
    wCCDL_RxWord_ChB_Status         : WORD;    (* [raw] ARINC-429 Cross-Channel Data Link Status Word Received from Channel B *)
    rCCDL_Rx_FMV_Pos_ChB_mm         : REAL;    (* [mm] FMV Spool Position Measurement Transmitted from Channel B via CCDL *)
    rCCDL_Rx_N2_Speed_ChB_RPM       : REAL;    (* [rpm] High-Pressure Spool Speed Transmitted from Channel B via CCDL *)

    (* Triplex TMR Low-Pressure Rotor Speed (N1) Pickups *)
    rN1_Speed_ChA_RPM               : REAL;    (* [rpm] Triplex N1 Low-Pressure Spool Speed Pickup Channel A (0.0 to 3200.0) *)
    rN1_Speed_ChB_RPM               : REAL;    (* [rpm] Triplex N1 Low-Pressure Spool Speed Pickup Channel B (0.0 to 3200.0) *)
    rN1_Speed_ChC_RPM               : REAL;    (* [rpm] Triplex N1 Low-Pressure Spool Speed Pickup Channel C (0.0 to 3200.0) *)

    (* Triplex TMR High-Pressure Rotor Speed (N2) Resolvers *)
    rN2_Speed_ChA_RPM               : REAL;    (* [rpm] Triplex N2 High-Pressure Spool Speed Resolver Channel A (0.0 to 12000.0) *)
    rN2_Speed_ChB_RPM               : REAL;    (* [rpm] Triplex N2 High-Pressure Spool Speed Resolver Channel B (0.0 to 12000.0) *)
    rN2_Speed_ChC_RPM               : REAL;    (* [rpm] Triplex N2 High-Pressure Spool Speed Resolver Channel C (0.0 to 12000.0) *)

    (* Triplex TMR Compressor Discharge Static Pressure (Ps3) Transducers *)
    rPs3_ChA_psia                   : REAL;    (* [psia] Triplex Compressor Discharge Static Pressure Ps3 Ch A (10.0 to 700.0) *)
    rPs3_ChB_psia                   : REAL;    (* [psia] Triplex Compressor Discharge Static Pressure Ps3 Ch B (10.0 to 700.0) *)
    rPs3_ChC_psia                   : REAL;    (* [psia] Triplex Compressor Discharge Static Pressure Ps3 Ch C (10.0 to 700.0) *)

    (* Triplex TMR Fan Inlet Static Pressure (P2) Transducers *)
    rP2_ChA_psia                    : REAL;    (* [psia] Triplex Engine Inlet Static Pressure P2 Channel A (2.0 to 16.0) *)
    rP2_ChB_psia                    : REAL;    (* [psia] Triplex Engine Inlet Static Pressure P2 Channel B (2.0 to 16.0) *)
    rP2_ChC_psia                    : REAL;    (* [psia] Triplex Engine Inlet Static Pressure P2 Channel C (2.0 to 16.0) *)

    (* Core Exhaust Gas Temperature (EGT) 8-Thermocouple Circumferential Harness *)
    rEGT_TC1_degC                   : REAL;    (* [deg C] Exhaust Gas Temp Dual-Element Thermocouple Probe 1 (0.0 to 1200.0) *)
    rEGT_TC2_degC                   : REAL;    (* [deg C] Exhaust Gas Temp Dual-Element Thermocouple Probe 2 (0.0 to 1200.0) *)
    rEGT_TC3_degC                   : REAL;    (* [deg C] Exhaust Gas Temp Dual-Element Thermocouple Probe 3 (0.0 to 1200.0) *)
    rEGT_TC4_degC                   : REAL;    (* [deg C] Exhaust Gas Temp Dual-Element Thermocouple Probe 4 (0.0 to 1200.0) *)
    rEGT_TC5_degC                   : REAL;    (* [deg C] Exhaust Gas Temp Dual-Element Thermocouple Probe 5 (0.0 to 1200.0) *)
    rEGT_TC6_degC                   : REAL;    (* [deg C] Exhaust Gas Temp Dual-Element Thermocouple Probe 6 (0.0 to 1200.0) *)
    rEGT_TC7_degC                   : REAL;    (* [deg C] Exhaust Gas Temp Dual-Element Thermocouple Probe 7 (0.0 to 1200.0) *)
    rEGT_TC8_degC                   : REAL;    (* [deg C] Exhaust Gas Temp Dual-Element Thermocouple Probe 8 (0.0 to 1200.0) *)

    (* Dual-Wound Actuator LVDT Feedbacks & Fluid Conditions *)
    rFMV_Pos_LVDT1_mm               : REAL;    (* [mm] Fuel Metering Valve Dual LVDT Coil 1 Spool Position (0.0 to 35.0) *)
    rFMV_Pos_LVDT2_mm               : REAL;    (* [mm] Fuel Metering Valve Dual LVDT Coil 2 Spool Position (0.0 to 35.0) *)
    rVSV_Pos_LVDT1_deg              : REAL;    (* [deg] Variable Stator Vane Dual LVDT Coil 1 Angular Feedback (-15.0 to 35.0) *)
    rVSV_Pos_LVDT2_deg              : REAL;    (* [deg] Variable Stator Vane Dual LVDT Coil 2 Angular Feedback (-15.0 to 35.0) *)
    rVBV_Pos_LVDT1_pct              : REAL;    (* [%] Variable Bleed Valve Dual LVDT Coil 1 Stroke Feedback (0.0 to 100.0) *)
    rVBV_Pos_LVDT2_pct              : REAL;    (* [%] Variable Bleed Valve Dual LVDT Coil 2 Stroke Feedback (0.0 to 100.0) *)
    rHPTACC_Pos_LVDT_pct            : REAL;    (* [%] High-Pressure Turbine Active Clearance Valve LVDT (0.0 to 100.0) *)
    rLPTACC_Pos_LVDT_pct            : REAL;    (* [%] Low-Pressure Turbine Active Clearance Valve LVDT (0.0 to 100.0) *)
    rDeltaP_FMV_psid                : REAL;    (* [psid] Fuel Metering Valve Regulating Differential Pressure (30.0 to 65.0) *)
    rFuelSupplyTemp_degC            : REAL;    (* [deg C] Inflow Aviation Kerosene Fuel Temperature (-40.0 to 95.0) *)
    rFuelFilterDeltaP_psid          : REAL;    (* [psid] Fuel Filter Impending Bypass Differential Pressure (0.0 to 35.0) *)
    rOilPressure_psid               : REAL;    (* [psid] Engine Lubrication Oil Supply Differential Pressure (10.0 to 120.0) *)
    rOilTemp_degC                   : REAL;    (* [deg C] Engine Scavenge Lubrication Oil Return Temperature (-20.0 to 160.0) *)
    rStarterAirPress_psia           : REAL;    (* [psia] Air Turbine Starter Pneumatic Supply Duct Pressure (0.0 to 80.0) *)

    (* Cockpit Crew Switch Discretes *)
    bMasterEngineStartSwitch        : BOOL;    (* [bool] Cockpit Engine Master Start Run/Cutoff Switch: TRUE=Run, FALSE=Cutoff *)
    bCrankMotoringSelector          : BOOL;    (* [bool] Cockpit Engine Dry/Wet Motoring Selector: TRUE=Crank, FALSE=Normal *)
    bFireHandleCutoff               : BOOL;    (* [bool] Cockpit Emergency Engine Fire Pull Handle Fuel Shutoff *)
    rDeltaTime_s                    : REAL;    (* [s] Discrete Control Execution Sample Interval (Nominal 0.020 s = 50 Hz) *)
END_VAR
VAR_OUTPUT
    (* Primary Electrohydraulic Actuator Commands *)
    rFMV_TorqueMotorCmd_mA          : REAL;    (* [mA] Fuel Metering Valve Dual-Coil Torque Motor Drive Current (-40.0 to 40.0) *)
    rVSV_ActuatorDemand_deg         : REAL;    (* [deg] Variable Stator Vane Electrohydraulic Actuator Angular Setpoint (-15.0 to 35.0) *)
    rVBV_ActuatorDemand_pct         : REAL;    (* [%] Variable Bleed Valve Electrohydraulic Actuator Stroke Demand (0.0 to 100.0) *)
    rHPTACC_ValveDemand_pct         : REAL;    (* [%] High-Pressure Turbine Active Clearance Coolant Valve Demand (0.0 to 100.0) *)
    rLPTACC_ValveDemand_pct         : REAL;    (* [%] Low-Pressure Turbine Active Clearance Coolant Valve Demand (0.0 to 100.0) *)

    (* Solenoid & Discretes Actuator Controls *)
    bStarterAirValve_Open           : BOOL;    (* [bool] Pneumatic Air Turbine Starter Control Valve Solenoid Energize *)
    bIgniterA_Fire                  : BOOL;    (* [bool] High-Energy Ignition System Exciter Box Channel A Fire Command *)
    bIgniterB_Fire                  : BOOL;    (* [bool] High-Energy Ignition System Exciter Box Channel B Fire Command *)
    bOverspeedShutoff_Trip          : BOOL;    (* [bool] Independent Hardware Electronic Overspeed Governor OSG Trip Actuation *)
    bThrustReverser_DeployCmd       : BOOL;    (* [bool] Thrust Reverser Translating Cowl Electrohydraulic Deploy Command *)

    (* Cyber-Physical Engine State Estimators & Flight Deck Metrology *)
    rCalculatedNetThrust_lbf        : REAL;    (* [lbf] Real-Time Cyber-Physical Model Filtered Net Engine Thrust (0 to 115000) *)
    rActiveFuelFlow_pph             : REAL;    (* [pph] Calibrated Real-Time Engine Mass Fuel Flow Rate Wf (0 to 45000) *)
    rEstimatedEGT_Margin_degC       : REAL;    (* [deg C] Instantaneous Turbine Gas Temperature Margin to Redline (0 to 400) *)
    rSurgeMargin_pct                : REAL;    (* [%] High-Pressure Compressor Aerodynamic Surge Margin Relative to Limit (0 to 50) *)
    rHPT_RunningClearance_mm        : REAL;    (* [mm] High-Pressure Turbine Blade Tip Radial Running Clearance (0.10 to 1.50) *)
    rLPT_RunningClearance_mm        : REAL;    (* [mm] Low-Pressure Turbine Blade Tip Radial Running Clearance (0.20 to 2.00) *)

    (* FADEC Operational Channel & Sequence Status *)
    wFADEC_OperatingState           : WORD;    (* [raw] 12-Stage Operational Finite State Machine State Code (0 to 12) *)
    bFADEC_ChannelA_InControl       : BOOL;    (* [bool] Channel Arbitration Master Status: TRUE=Ch A In Control, FALSE=Ch B *)
    dwChannelHealthStatus_ChA       : DWORD;   (* [raw] Channel A Comprehensive Health & BIT Status Word *)
    dwChannelHealthStatus_ChB       : DWORD;   (* [raw] Channel B Comprehensive Health & BIT Status Word *)

    (* DO-178C Level A / ISA-18.2 Diagnostic & Alarm Status Words *)
    dwISA18_Alarms_Trips            : DWORD;   (* [raw] ISA-18.2 Priority 1 Emergency Engine Trip Mask (Bit-Packed) *)
    dwISA18_Alarms_Severity1        : DWORD;   (* [raw] ISA-18.2 Priority 2 Critical Operating Alarms Mask (Bit-Packed) *)
    dwISA18_Alarms_Severity2        : DWORD;   (* [raw] ISA-18.2 Priority 3 Advisory / Maintenance Alerts Mask (Bit-Packed) *)

    (* ARINC-429 Propulsion Telemetry Broadcast 32-Bit Encodings (Lower & Upper 16-bit packed words) *)
    wARINC429_TelemetryWord1        : WORD;    (* [raw] ARINC-429 Propulsion Bus High-Frequency Dynamic Broadcast Word 1 *)
    wARINC429_TelemetryWord2        : WORD;    (* [raw] ARINC-429 Propulsion Bus High-Frequency Dynamic Broadcast Word 2 *)
    wARINC429_TelemetryWord3        : WORD;    (* [raw] ARINC-429 Propulsion Bus High-Frequency Dynamic Broadcast Word 3 *)
    wARINC429_TelemetryWord4        : WORD;    (* [raw] ARINC-429 Propulsion Bus High-Frequency Dynamic Broadcast Word 4 *)
END_VAR
VAR
    (* Discrete State-Space Model 16x16 Matrices & Vectors *)
    aA                              : ARRAY[1..16, 1..16] OF REAL;  (* State transition matrix A (16x16) *)
    aB                              : ARRAY[1..16, 1..8] OF REAL;   (* Control input matrix B (16x8) *)
    aC                              : ARRAY[1..8, 1..16] OF REAL;   (* Measurement output matrix C (8x16) *)
    aD                              : ARRAY[1..8, 1..8] OF REAL;    (* Direct feedthrough matrix D (8x8) *)
    aState_x                        : ARRAY[1..16] OF REAL;         (* Real-time discrete state vector x[k] *)
    aState_x_next                   : ARRAY[1..16] OF REAL;         (* Forward propagated state vector x[k+1] *)
    aControl_u                      : ARRAY[1..8] OF REAL;          (* Engine control actuator vector u[k] *)
    aOutput_y                       : ARRAY[1..8] OF REAL;          (* Cyber-physical engine observables y[k] *)
    bStateSpaceInitialized          : BOOL := FALSE;                (* One-time deterministic matrix load flag *)

    (* Model Predictive Control (MPC) Receding Horizon Arrays *)
    aQ_Weight                       : ARRAY[1..8] OF REAL;          (* Output tracking quadratic penalty weights Q *)
    aR_Weight                       : ARRAY[1..8] OF REAL;          (* Actuator slew rate penalty weights R *)
    aY_Ref                          : ARRAY[1..8] OF REAL;          (* Real-time aerodynamic reference vector y_ref *)
    aU_Prev                         : ARRAY[1..8] OF REAL;          (* Previous cycle control input vector u[k-1] *)
    aDeltaU                         : ARRAY[1..8] OF REAL;          (* Optimal control incremental moves delta_u *)
    aPred_x                         : ARRAY[1..5, 1..16] OF REAL;   (* 5-Step receding state prediction trajectories *)
    aPred_y                         : ARRAY[1..5, 1..8] OF REAL;    (* 5-Step receding output prediction trajectories *)
    rMPC_CostJ                      : REAL;                         (* Evaluated quadratic performance index J *)
    rMPC_BestCost                   : REAL;                         (* Minimum cost candidate in receding horizon *)
    rDeltaWf_Candidate              : REAL;                         (* Candidate fuel flow increment [pph] *)
    rDeltaVSV_Candidate             : REAL;                         (* Candidate VSV angular increment [deg] *)
    rDeltaACC_Candidate             : REAL;                         (* Candidate HPTACC valve increment [%] *)
    rGrad_Wf                        : REAL;                         (* Numerical cost gradient wrt fuel flow *)
    rGrad_VSV                       : REAL;                         (* Numerical cost gradient wrt VSV angle *)
    rGrad_ACC                       : REAL;                         (* Numerical cost gradient wrt clearance valve *)
    rStepSize_Wf                    : REAL := 48.0;                 (* Optimization gradient descent step size Wf *)
    rStepSize_VSV                   : REAL := 0.28;                 (* Optimization gradient descent step size VSV *)
    rStepSize_ACC                   : REAL := 0.55;                 (* Optimization gradient descent step size ACC *)

    (* 2oo3 TMR Low-Pressure Rotor Speed (N1) Voting Variables *)
    rN1_Voted_RPM                   : REAL;                         (* Consolidated 2oo3 voted N1 shaft speed [rpm] *)
    bN1_Degraded_1oo2               : BOOL;                         (* N1 sensor redundancy degraded to 1oo2 mode *)
    bN1_TotalFailure                : BOOL;                         (* N1 all-sensor failure flag (synthetic mode active) *)
    rTimer_N1_Discrepancy_s         : REAL;                         (* N1 cross-channel persistence discrepancy timer [s] *)
    bN1_ChA_Fault                   : BOOL;                         (* N1 Channel A pickup permanent fault latch *)
    bN1_ChB_Fault                   : BOOL;                         (* N1 Channel B pickup permanent fault latch *)
    bN1_ChC_Fault                   : BOOL;                         (* N1 Channel C pickup permanent fault latch *)

    (* 2oo3 TMR High-Pressure Rotor Speed (N2) Voting Variables *)
    rN2_Voted_RPM                   : REAL;                         (* Consolidated 2oo3 voted N2 shaft speed [rpm] *)
    bN2_Degraded_1oo2               : BOOL;                         (* N2 sensor redundancy degraded to 1oo2 mode *)
    bN2_TotalFailure                : BOOL;                         (* N2 all-sensor failure flag *)
    rTimer_N2_Discrepancy_s         : REAL;                         (* N2 cross-channel persistence discrepancy timer [s] *)
    bN2_ChA_Fault                   : BOOL;                         (* N2 Channel A resolver fault latch *)
    bN2_ChB_Fault                   : BOOL;                         (* N2 Channel B resolver fault latch *)
    bN2_ChC_Fault                   : BOOL;                         (* N2 Channel C resolver fault latch *)

    (* 2oo3 TMR Compressor Discharge Pressure (Ps3) Voting Variables *)
    rPs3_Voted_psia                 : REAL;                         (* Consolidated 2oo3 voted Ps3 static pressure [psia] *)
    bPs3_Degraded_1oo2              : BOOL;                         (* Ps3 sensor redundancy degraded to 1oo2 mode *)
    bPs3_TotalFailure               : BOOL;                         (* Ps3 all-sensor failure flag *)
    rTimer_Ps3_Discrepancy_s        : REAL;                         (* Ps3 cross-channel discrepancy persistence timer [s] *)
    bPs3_ChA_Fault                  : BOOL;                         (* Ps3 Channel A transducer fault latch *)
    bPs3_ChB_Fault                  : BOOL;                         (* Ps3 Channel B transducer fault latch *)
    bPs3_ChC_Fault                  : BOOL;                         (* Ps3 Channel C transducer fault latch *)

    (* 2oo3 TMR Engine Inlet Pressure (P2) Voting Variables *)
    rP2_Voted_psia                  : REAL;                         (* Consolidated 2oo3 voted P2 static pressure [psia] *)
    bP2_Degraded_1oo2               : BOOL;                         (* P2 sensor redundancy degraded to 1oo2 mode *)
    bP2_TotalFailure                : BOOL;                         (* P2 all-sensor failure flag *)
    rTimer_P2_Discrepancy_s         : REAL;                         (* P2 cross-channel discrepancy persistence timer [s] *)

    (* 8-Thermocouple EGT Circumferential Harness Surveillance *)
    aEGT_Raw_degC                   : ARRAY[1..8] OF REAL;          (* Raw thermocouple readings array [deg C] *)
    aEGT_Valid                      : ARRAY[1..8] OF BOOL;          (* Thermocouple electrical integrity valid flags *)
    rEGT_Voted_Average_degC         : REAL;                         (* Validated arithmetic average EGT [deg C] *)
    rEGT_Peak_degC                  : REAL;                         (* Spatial peak hot-spot thermocouple reading [deg C] *)
    rEGT_Min_degC                   : REAL;                         (* Minimum valid thermocouple reading [deg C] *)
    rEGT_Spread_degC                : REAL;                         (* Circumferential temperature spread (Peak - Min) [deg C] *)
    rEGT_Prev_degC                  : REAL;                         (* Previous cycle consolidated EGT reading [deg C] *)
    rEGT_RateOfRise_degCs           : REAL;                         (* Low-pass filtered EGT rate of rise dEGT/dt [deg C/s] *)
    iEGT_ValidCount                 : INT;                          (* Count of electrically valid thermocouple junctions *)

    (* Dual LVDT Voting for FMV, VSV, and VBV Actuators *)
    rFMV_Voted_Pos_mm               : REAL;                         (* Validated FMV spool position feedback [mm] *)
    rVSV_Voted_Pos_deg              : REAL;                         (* Validated VSV unison ring angular feedback [deg] *)
    rVBV_Voted_Pos_pct              : REAL;                         (* Validated VBV bleed door stroke feedback [%] *)
    bFMV_LVDT_Discrepancy           : BOOL;                         (* FMV dual-wound coil discrepancy alert *)
    bVSV_LVDT_Discrepancy           : BOOL;                         (* VSV dual-wound coil discrepancy alert *)
    bVBV_LVDT_Discrepancy           : BOOL;                         (* VBV dual-wound coil discrepancy alert *)

    (* FADEC Dual-Channel Cross-Talk Arbitration & Mastership *)
    rTimer_CCDL_Timeout_s           : REAL;                         (* Cross-Channel Data Link watchdog timer [s] *)
    bCCDL_LinkLost                  : BOOL;                         (* Cross-Channel Data Link communication lost flag *)
    bMasterChannelActive            : BOOL := TRUE;                 (* True when Channel A is commanding the engine *)

    (* Aerodynamic Schedules & Thermodynamic Performance Observers *)
    rTheta_T2                       : REAL;                         (* Total temperature ratio Station 2 (Tt2 / 288.15 K) *)
    rDelta_P2                       : REAL;                         (* Total pressure ratio Station 2 (Pt2 / 14.696 psia) *)
    rSqrtTheta                      : REAL;                         (* Square root of temperature ratio sqrt(Theta) *)
    rN1_Corrected_RPM               : REAL;                         (* Corrected low-pressure rotor speed N1 / sqrt(Theta) *)
    rN2_Corrected_RPM               : REAL;                         (* Corrected high-pressure rotor speed N2 / sqrt(Theta) *)
    rN1_Pct                         : REAL;                         (* Low-pressure rotor speed percent of rated (2850 RPM) *)
    rN2_Pct                         : REAL;                         (* High-pressure rotor speed percent of rated (10800 RPM) *)
    rEPR_EnginePressureRatio        : REAL;                         (* Engine pressure ratio Pt4.5 / Pt2 *)
    rCompressorPrRatio              : REAL;                         (* High-pressure compressor pressure ratio Ps3 / P2 *)
    rVSV_Schedule_Target_deg        : REAL;                         (* Aerodynamic schedule target VSV angle [deg] *)
    rVBV_Schedule_Target_pct        : REAL;                         (* Aerodynamic schedule target VBV bleed stroke [%] *)
    rSurgeLine_WfPs3                : REAL;                         (* HPC aerodynamic stall surge boundary (Wf/Ps3) *)
    rAccelLimit_WfPs3               : REAL;                         (* Dynamic acceleration surge fuel schedule boundary *)
    rDecelLimit_WfPs3               : REAL;                         (* Dynamic deceleration lean flameout fuel schedule *)
    rActual_WfPs3                   : REAL;                         (* Real-time operating fuel-to-pressure ratio *)
    rDemandThrust_lbf               : REAL;                         (* Cockpit TLA mapped thrust setpoint [lbf] *)
    rTargetFuelFlow_pph             : REAL;                         (* Aerodynamic fuel flow demand setpoint Wf [pph] *)
    rSurgeMargin_Calculated         : REAL;                         (* Real-time compressor surge margin [%] *)
    rPs3_Prev_psia                  : REAL;                         (* Previous cycle compressor discharge pressure [psia] *)
    rPs3_RateOfChange_psias         : REAL;                         (* Ps3 time derivative dPs3/dt [psia/s] *)
    bStallSurgeDetected             : BOOL;                         (* Severe HPC aerodynamic surge event latch *)

    (* Active Turbine Clearance Control (HPTACC & LPTACC) Cyber-Physics *)
    rThermalGrowth_Rotor_HPT_mm     : REAL;                         (* HPT turbine disk & blade thermal expansion [mm] *)
    rThermalGrowth_Case_HPT_mm      : REAL;                         (* HPT outer casing structural ring thermal growth [mm] *)
    rCentrifugalGrowth_HPT_mm       : REAL;                         (* HPT mechanical blade tip centrifugal stretch [mm] *)
    rRunningClearance_HPT_calc_mm   : REAL;                         (* Calculated HPT radial running tip clearance [mm] *)
    rTargetClearance_HPT_mm         : REAL := 0.25;                 (* HPT target cruise running tip clearance [mm] *)
    rClearanceError_HPT_mm          : REAL;                         (* HPT active tip clearance regulation error [mm] *)
    rHPTACC_Integrator_pct          : REAL;                         (* HPTACC cooling valve PI integral accumulator [%] *)
    rThermalGrowth_Rotor_LPT_mm     : REAL;                         (* LPT rotor disk & blade thermal expansion [mm] *)
    rThermalGrowth_Case_LPT_mm      : REAL;                         (* LPT outer casing structural ring thermal growth [mm] *)
    rCentrifugalGrowth_LPT_mm       : REAL;                         (* LPT mechanical blade tip centrifugal stretch [mm] *)
    rRunningClearance_LPT_calc_mm   : REAL;                         (* Calculated LPT radial running tip clearance [mm] *)
    rTargetClearance_LPT_mm         : REAL := 0.50;                 (* LPT target cruise running tip clearance [mm] *)
    rClearanceError_LPT_mm          : REAL;                         (* LPT active tip clearance regulation error [mm] *)
    rLPTACC_Integrator_pct          : REAL;                         (* LPTACC cooling valve PI integral accumulator [%] *)
    rHotSectionCreepFactor          : REAL;                         (* Instantaneous thermal creep acceleration factor *)
    rLarsonMillerParameter          : REAL;                         (* Larson-Miller parameter for turbine blade alloy *)
    rThermalDamageAccumulator       : REAL;                         (* Integrated turbine thermal fatigue damage index *)

    (* Fuel Metering Valve (FMV) Closed-Loop Servo Loop *)
    rFMV_TargetSpool_mm             : REAL;                         (* Target FMV spool displacement setpoint [mm] *)
    rFMV_PositionError_mm           : REAL;                         (* Spool position servo error [mm] *)
    rFMV_LoopIntegrator_mA          : REAL;                         (* Servo current PI loop integral accumulator [mA] *)
    rFMV_LoopProportional_mA        : REAL;                         (* Servo current PI loop proportional term [mA] *)
    rFMV_DitherCurrent_mA           : REAL;                         (* 85 Hz dither anti-stiction dither current [mA] *)
    rFMV_DitherPhase_rad            : REAL;                         (* Dither waveform harmonic phase angle [rad] *)
    rFMV_TotalDriveCurrent_mA       : REAL;                         (* Consolidated torque motor drive current [mA] *)

    (* 12-Stage Operational Finite State Machine (FSM) Variables *)
    iFSM_State                      : INT := 0;                     (* Discrete operational sequencer state index (0..12) *)
    rStateTimer_s                   : REAL := 0.0;                  (* Time elapsed in active operational state [s] *)
    bStateFirstCycle                : BOOL := TRUE;                 (* First-cycle state entry strobe flag *)
    bLightoffDetected               : BOOL := FALSE;                (* Combustor flame light-off confirmation flag *)
    bStarterCutoutComplete          : BOOL := FALSE;                (* Pneumatic starter cutout threshold crossed flag *)
    bTakeoffThrustReached           : BOOL := FALSE;                (* 110,000 lbf rated takeoff thrust reached flag *)
    bInFlightFlameoutDetected       : BOOL := FALSE;                (* In-flight flameout event detection flag *)
    bAutoRelightArmed               : BOOL := FALSE;                (* Emergency auto-relight logic armed flag *)
    iRelightAttempts                : INT := 0;                     (* Cumulative in-flight relight attempts counter *)
    rFlameoutTimer_s                : REAL := 0.0;                  (* Flameout persistence duration timer [s] *)
    bOverspeedShutoff_Latch         : BOOL := FALSE;                (* Independent overspeed trip solenoid latch *)
    bEGT_Redline_Latch              : BOOL := FALSE;                (* Turbine gas temperature redline trip latch *)
    bSurgeStall_Latch               : BOOL := FALSE;                (* HPC aerodynamic surge stall trip latch *)

    (* DO-178C / ISA-18.2 Diagnostic Counters, Deadbands & Timers *)
    rTimer_EGT_HighAlarm_s          : REAL;                         (* EGT advisory high persistence timer [s] *)
    rTimer_OilPressureLow_s         : REAL;                         (* Lubrication oil low pressure persistence timer [s] *)
    rTimer_FilterBypass_s           : REAL;                         (* Fuel filter impending bypass timer [s] *)
    rDeadband_EGT_degC              : REAL := 15.0;                 (* EGT alarm deadband hysteresis [deg C] *)
    rDeadband_N2_RPM                : REAL := 120.0;                (* N2 speed alarm deadband hysteresis [rpm] *)
    dwTripBits                      : DWORD;                        (* Priority 1 emergency trip bit accumulator *)
    dwSev1Bits                      : DWORD;                        (* Priority 2 critical operating alarm bitfield *)
    dwSev2Bits                      : DWORD;                        (* Priority 3 advisory / maintenance bitfield *)

    (* Working Loop Iterators & Mathematics Scratchpad *)
    i                               : INT;                          (* Outer loop row iterator *)
    j                               : INT;                          (* Inner loop column iterator *)
    k                               : INT;                          (* Control input vector iterator *)
    m                               : INT;                          (* Measurement output vector iterator *)
    n                               : INT;                          (* Receding prediction horizon step iterator *)
    rSum                            : REAL;                         (* Matrix dot product accumulation scalar *)
    rDiffAB                         : REAL;                         (* Sensor channel A-B discrepancy scalar *)
    rDiffBC                         : REAL;                         (* Sensor channel B-C discrepancy scalar *)
    rDiffCA                         : REAL;                         (* Sensor channel C-A discrepancy scalar *)
    rDt_sec                         : REAL;                         (* Filtered execution cycle delta time [s] *)
    dwRawWord                       : DWORD;                        (* ARINC-429 telemetry packaging accumulator *)
    iParityCount                    : INT;                          (* ARINC-429 odd parity bit counter *)
    bOddParity                      : BOOL;                         (* ARINC-429 odd parity flag *)
END_VAR
""")

    # 2. PHASE 0: Deterministic Matrix Initialization
    code_lines.append("""
(* ================================================================================================================ *)
(* PHASE 0: ONE-TIME DETERMINISTIC INITIALIZATION OF 16x16 STATE-SPACE & RECEDING-HORIZON MPC MATRICES             *)
(* ================================================================================================================ *)
IF NOT bStateSpaceInitialized THEN
    (* Zeroize complete 16x16 state transition matrix A *)
    FOR i := 1 TO 16 DO
        FOR j := 1 TO 16 DO
            aA[i, j] := 0.0;
        END_FOR;
    END_FOR;

    (* Zeroize complete 16x8 control input matrix B *)
    FOR i := 1 TO 16 DO
        FOR k := 1 TO 8 DO
            aB[i, k] := 0.0;
        END_FOR;
    END_FOR;

    (* Zeroize complete 8x16 measurement output matrix C *)
    FOR m := 1 TO 8 DO
        FOR j := 1 TO 16 DO
            aC[m, j] := 0.0;
        END_FOR;
    END_FOR;

    (* Zeroize complete 8x8 direct feedthrough matrix D *)
    FOR m := 1 TO 8 DO
        FOR k := 1 TO 8 DO
            aD[m, k] := 0.0;
        END_FOR;
    END_FOR;

    (* ------------------------------------------------------------------------------------------------------------ *)
    (* STATE TRANSITION MATRIX A COEFFICIENT POPULATION (Diagonal Retention & Aerodynamic Cross-Couplings)           *)
    (* States: 1:N1, 2:N2, 3:Ps3, 4:Tt3, 5:Pcomb, 6:Tcomb, 7:EGT, 8:Tcase_HPT, 9:Tdisk_HPT, 10:Clr_HPT,           *)
    (*         11:Tcase_LPT, 12:Clr_LPT, 13:Pos_VBV, 14:Ang_VSV, 15:Pos_FMV, 16:Thrust_Net                          *)
    (* ------------------------------------------------------------------------------------------------------------ *)
    (* Row 1: Low-Pressure Spool Speed N1 dynamics (Fan & LPT inertia, mechanical damping, LPT work extraction) *)
    aA[1, 1]  := 0.9825;    (* Low-pressure rotor aerodynamic self-damping and spool inertia decay *)
    aA[1, 2]  := 0.0084;    (* Inter-spool aerodynamic torque cross-coupling from HP core flow *)
    aA[1, 5]  := 0.0142;    (* Combustor pressure expansion driving LPT enthalpy extraction *)
    aA[1, 7]  := 0.0068;    (* Turbine inlet gas temperature driving LPT expansion work *)
    aA[1, 16] := 0.00012;   (* Fan thrust aerodynamic reaction feedback *)

    (* Row 2: High-Pressure Spool Speed N2 dynamics (HPC & HPT inertia, combustor heat release, compressor load) *)
    aA[2, 2]  := 0.9760;    (* High-pressure core rotor inertia time constant (tau = 0.83 s) *)
    aA[2, 3]  := -0.0185;   (* HPC aerodynamic adverse pressure gradient back-pressure torque *)
    aA[2, 5]  := 0.0220;    (* Combustor driving pressure over HPT nozzle guide vanes *)
    aA[2, 6]  := 0.0315;    (* Combustor gas temperature enthalpy expansion into HPT rotor *)
    aA[2, 14] := 0.0450;    (* Variable Stator Vane (VSV) aerodynamic incidence angle torque modulation *)

    (* Row 3: Compressor Discharge Static Pressure Ps3 dynamics (HPC 10-stage compression, volume storage lag) *)
    aA[3, 2]  := 0.0385;    (* HPC pressure rise characteristic as a function of N2 core speed *)
    aA[3, 3]  := 0.9150;    (* HPC diffuser and combustion chamber manifold pneumatic storage retention *)
    aA[3, 4]  := 0.0125;    (* Thermal expansion of air inside compressor discharge diffuser *)
    aA[3, 13] := -0.0520;   (* Variable Bleed Valve (VBV) mass flow extraction pressure reduction *)
    aA[3, 14] := 0.0280;    (* VSV vane staging opening increasing core airflow and pressure ratio *)

    (* Row 4: Compressor Discharge Total Temperature Tt3 dynamics (Polytropic compression heating) *)
    aA[4, 2]  := 0.0240;    (* Polytropic compression work heating from N2 rotor speed *)
    aA[4, 3]  := 0.0410;    (* Pressure ratio adiabatic temperature rise coupling *)
    aA[4, 4]  := 0.9420;    (* Compressor casing and stator blade thermal capacitance decay *)

    (* Row 5: Combustor Internal Burner Static Pressure Pcomb dynamics (Combustion chamber plenum volume lag) *)
    aA[5, 3]  := 0.8850;    (* Direct pneumatic feed through compressor diffuser into combustor liner *)
    aA[5, 5]  := 0.0950;    (* Combustor volume filling time constant retention *)
    aA[5, 6]  := 0.0180;    (* Gas thermal expansion in constant volume combustor dome *)

    (* Row 6: Combustor Gas Temperature Tcomb dynamics (Fuel-air stoichiometric heat release and mixing lag) *)
    aA[6, 3]  := -0.0160;   (* Air mass flow cooling effect on local combustor equivalence ratio *)
    aA[6, 6]  := 0.8920;    (* Combustor liner residence time and recirculation zone thermal delay *)
    aA[6, 15] := 0.1420;    (* Fuel Metering Valve (FMV) fuel mass injection thermal heat release *)

    (* Row 7: Exhaust Gas Temperature EGT (T4.5 Station at LPT inlet plane, expansion work drop) *)
    aA[7, 1]  := -0.0150;   (* LPT work extraction temperature drop *)
    aA[7, 2]  := -0.0280;   (* HPT work extraction temperature drop *)
    aA[7, 6]  := 0.4850;    (* Combustor gas temperature enthalpy carry-over through HPT stages *)
    aA[7, 7]  := 0.5100;    (* Thermocouple probe protective sheath thermal lag retention *)

    (* Row 8: HPT Outer Casing Ring Metal Temperature Tcase_HPT (Convection from hot gas & cooling air) *)
    aA[8, 7]  := 0.0580;    (* Hot gas aerodynamic radiation and convection into inner shroud *)
    aA[8, 8]  := 0.9380;    (* Thick superalloy turbine case thermal capacitance lag (tau = 16.0 s) *)

    (* Row 9: HPT Rotor Disk Bulk Temperature Tdisk_HPT (Conductive heat transfer from blade roots) *)
    aA[9, 7]  := 0.0240;    (* Blade root conduction and rim purge cavity convection into disk *)
    aA[9, 9]  := 0.9740;    (* Heavy forged nickel-alloy rotor disk thermal inertia (tau = 38.0 s) *)

    (* Row 10: HPT Blade Tip Radial Running Clearance Clr_HPT (Casing expansion minus rotor growth) *)
    aA[10, 2]  := -0.00045; (* Centrifugal elastic radial stretch of turbine blades with N2 speed *)
    aA[10, 8]  := 0.00185;  (* Radial casing expansion opening the blade tip clearance gap *)
    aA[10, 9]  := -0.00192; (* Rotor disk and blade radial thermal growth closing the clearance gap *)
    aA[10, 10] := 0.9850;   (* Running clearance mechanical compliance retention *)

    (* Row 11: LPT Outer Casing Metal Temperature Tcase_LPT (Thermal convection from LPT gas path) *)
    aA[11, 7]  := 0.0420;   (* Gas path convection from Station 4.5 into LPT case structural rings *)
    aA[11, 11] := 0.9550;   (* LPT casing structural thermal capacitance retention (tau = 22.0 s) *)

    (* Row 12: LPT Blade Tip Radial Running Clearance Clr_LPT (LPT casing expansion minus LPT rotor growth) *)
    aA[12, 1]  := -0.00032; (* Centrifugal radial stretch of LPT titanium-aluminide blades with N1 *)
    aA[12, 11] := 0.00155;  (* LPT casing thermal expansion increasing radial gap *)
    aA[12, 12] := 0.9880;   (* LPT tip running clearance retention *)

    (* Row 13: Variable Bleed Valve Position Pos_VBV (Electrohydraulic actuator valve stroke dynamics) *)
    aA[13, 13] := 0.8800;   (* VBV electrohydraulic cylinder mechanical response (tau = 0.16 s) *)

    (* Row 14: Variable Stator Vane Angle Ang_VSV (Electrohydraulic torque tube unison ring dynamics) *)
    aA[14, 14] := 0.8500;   (* VSV unison ring dual-actuator response (tau = 0.13 s) *)

    (* Row 15: Fuel Metering Valve Position Pos_FMV (EHSV torque motor spool positioning dynamics) *)
    aA[15, 15] := 0.8200;   (* FMV flapper-nozzle second-order hydraulic response (tau = 0.10 s) *)

    (* Row 16: Engine Net Propulsive Thrust Thrust_Net (Fan momentum thrust plus core jet reaction) *)
    aA[16, 1]  := 34.50;    (* 134-inch fan mass airflow momentum thrust per RPM of N1 shaft *)
    aA[16, 2]  := 2.85;     (* Core engine high-pressure spool exhaust jet gas velocity contribution *)
    aA[16, 5]  := 18.20;    (* Combustor pressure driving core convergent exhaust nozzle pressure thrust *)
    aA[16, 16] := 0.9200;   (* Propulsive jet wake momentum consolidation time constant *)

    (* ------------------------------------------------------------------------------------------------------------ *)
    (* CONTROL INPUT MATRIX B COEFFICIENT POPULATION (Actuator Forces, Current Drives & Thermal Modulations)       *)
    (* Inputs: 1:i_FMV_mA, 2:AngCmd_VSV, 3:PosCmd_VBV, 4:ModCmd_HPTACC, 5:ModCmd_LPTACC, 6:Cmd_ATS, 7:Cmd_Ign, 8:TRV*)
    (* ------------------------------------------------------------------------------------------------------------ *)
    (* Input 1: Fuel Metering Valve torque motor current i_FMV_mA *)
    aB[15, 1] := 0.1800;    (* Direct torque motor current driving FMV hydraulic spool displacement [mm/mA] *)

    (* Input 2: VSV actuator angular command AngCmd_VSV *)
    aB[14, 2] := 0.1500;    (* VSV electrohydraulic servo demand driving stator unison ring angle [deg/deg] *)

    (* Input 3: VBV actuator stroke command PosCmd_VBV *)
    aB[13, 3] := 0.1200;    (* VBV electrohydraulic command driving booster bleed door position [%/%] *)

    (* Input 4: HPTACC modulating cooling air valve command ModCmd_HPTACC *)
    aB[8, 4]  := -0.0850;   (* Modulated fan bypass cooling air reducing HPT case metal temperature [deg C/%] *)
    aB[10, 4] := -0.0022;   (* HPTACC cooling shrinking case to close radial blade tip clearance [mm/%] *)

    (* Input 5: LPTACC modulating cooling air valve command ModCmd_LPTACC *)
    aB[11, 5] := -0.0620;   (* Modulated cooling air reducing LPT casing temperature [deg C/%] *)
    aB[12, 5] := -0.0018;   (* LPTACC cooling shrinking LPT case to regulate tip running gap [mm/%] *)

    (* Input 6: Air Turbine Starter (ATS) pneumatic valve solenoid Cmd_ATS *)
    aB[2, 6]  := 42.50;     (* Pneumatic starter turbine torque accelerating N2 core rotor spool [RPM/cmd] *)

    (* Input 7: High-energy dual ignition exciter spark discharge Cmd_Igniters *)
    aB[6, 7]  := 85.00;     (* Initial combustion flame kernel ignition enthalpy release [deg C/cmd] *)

    (* Input 8: Thrust reverser translating cowl deployment command Cmd_Reverser *)
    aB[16, 8] := -45000.0;  (* Aerodynamic blocker doors redirecting fan bypass flow into reverse [lbf/cmd] *)

    (* ------------------------------------------------------------------------------------------------------------ *)
    (* MEASUREMENT OUTPUT MATRIX C COEFFICIENT POPULATION                                                           *)
    (* Outputs: 1:Thrust_Net, 2:Ratio_N2_N1, 3:FuelFlow_Wf, 4:SurgeMargin, 5:EGT_Margin, 6:ClrErr_HPT, 7:TSFC, 8:Phi*)
    (* ------------------------------------------------------------------------------------------------------------ *)
    aC[1, 16] := 1.000;     (* Output 1: Real-time net propulsive thrust [lbf] *)
    aC[2, 1]  := -0.00135;  (* Output 2: Core spool ratio N2 / N1 denominator dependency *)
    aC[2, 2]  := 0.00035;   (* Output 2: Core spool ratio N2 / N1 numerator dependency *)
    aC[3, 15] := 1150.0;    (* Output 3: Calibrated mass fuel flow rate Wf as a function of FMV spool [pph/mm] *)
    aC[4, 3]  := -0.0450;   (* Output 4: Surge margin dependency on compressor discharge pressure *)
    aC[4, 14] := 0.6500;    (* Output 4: Surge margin improvement from VSV vane optimization *)
    aC[5, 7]  := -1.000;    (* Output 5: Instantaneous EGT margin to redline (Redline_EGT - T4.5) *)
    aC[6, 10] := 1.000;     (* Output 6: HPT active blade tip clearance tracking error [mm] *)
    aC[7, 15] := 0.0125;    (* Output 7: Thrust Specific Fuel Consumption TSFC numerator coupling *)
    aC[7, 16] := -0.000008; (* Output 7: TSFC denominator thrust expansion *)
    aC[8, 6]  := 0.00085;   (* Output 8: Combustor equivalence ratio Phi from burner temperature *)

    (* ------------------------------------------------------------------------------------------------------------ *)
    (* DIRECT FEEDTHROUGH MATRIX D & MPC QUADRATIC PENALTY WEIGHT INITIALIZATION                                    *)
    (* ------------------------------------------------------------------------------------------------------------ *)
    aD[1, 8] := -8500.0;    (* Immediate thrust reversal upon blocker door aerodynamic interlock *)

    (* MPC Quadratic Output Tracking Error Weights Q *)
    aQ_Weight[1] := 0.00015; (* Net thrust tracking penalty (110,000 lbf scale) *)
    aQ_Weight[2] := 2.5000;  (* Core spool speed ratio N2/N1 aerodynamic match penalty *)
    aQ_Weight[3] := 0.0008;  (* Fuel flow rate economic consumption weight *)
    aQ_Weight[4] := 45.000;  (* High-pressure compressor surge margin preservation penalty *)
    aQ_Weight[5] := 1.8500;  (* Turbine gas temperature EGT redline avoidance penalty *)
    aQ_Weight[6] := 12500.0; (* HPT active clearance control tracking precision penalty (0.25 mm target) *)
    aQ_Weight[7] := 120.00;  (* Thrust Specific Fuel Consumption (TSFC) minimization weight *)
    aQ_Weight[8] := 850.00;  (* Combustor fuel-air equivalence ratio stability weight *)

    (* MPC Actuator Slew Rate Penalties R *)
    aR_Weight[1] := 0.085;   (* FMV torque motor current slew rate damping *)
    aR_Weight[2] := 1.250;   (* VSV stator unison ring mechanical fatigue suppression *)
    aR_Weight[3] := 0.750;   (* VBV bleed valve mechanical wear suppression *)
    aR_Weight[4] := 2.800;   (* HPTACC thermal butterfly valve cycle preservation *)
    aR_Weight[5] := 2.200;   (* LPTACC thermal butterfly valve cycle preservation *)
    aR_Weight[6] := 5.000;   (* Pneumatic starter engagement solenoid wear penalty *)
    aR_Weight[7] := 1.000;   (* Ignition exciter box spark cycle consumption penalty *)
    aR_Weight[8] := 10.00;   (* Thrust reverser translating sleeve actuation wear penalty *)

    (* Initial State Vector Initialization to Cold Quiescent Engine *)
    aState_x[1]  := 0.0;     (* N1 speed = 0 RPM *)
    aState_x[2]  := 0.0;     (* N2 speed = 0 RPM *)
    aState_x[3]  := 14.696;  (* Ps3 = Ambient standard sea level pressure [psia] *)
    aState_x[4]  := 15.0;    (* Tt3 = Ambient temperature [deg C] *)
    aState_x[5]  := 14.696;  (* Pcomb = Ambient pressure [psia] *)
    aState_x[6]  := 15.0;    (* Tcomb = Ambient temperature [deg C] *)
    aState_x[7]  := 15.0;    (* EGT = Ambient temperature [deg C] *)
    aState_x[8]  := 15.0;    (* HPT casing metal temp [deg C] *)
    aState_x[9]  := 15.0;    (* HPT rotor disk temp [deg C] *)
    aState_x[10] := 0.850;   (* Cold static HPT clearance = 0.850 mm *)
    aState_x[11] := 15.0;    (* LPT casing metal temp [deg C] *)
    aState_x[12] := 1.150;   (* Cold static LPT clearance = 1.150 mm *)
    aState_x[13] := 85.0;    (* VBV bleed doors resting open [85%] *)
    aState_x[14] := -15.0;   (* VSV vanes resting fully closed [-15 deg] *)
    aState_x[15] := 0.0;     (* FMV spool at mechanical zero cutoff [0 mm] *)
    aState_x[16] := 0.0;     (* Net thrust = 0 lbf *)

    bStateSpaceInitialized := TRUE;
END_IF;
""")

    # 3. PHASE 1: 2oo3 TMR Sensor Voting & Discrepancy Arbitration
    code_lines.append("""
(* ================================================================================================================ *)
(* PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING & DISCREPANCY ARBITRATION                              *)
(* ================================================================================================================ *)
(* Execution cycle delta time bounding and integrity clamping *)
IF rDeltaTime_s > 0.001 AND rDeltaTime_s < 0.100 THEN
    rDt_sec := rDeltaTime_s;
ELSE
    rDt_sec := 0.020; (* Nominal 50 Hz execution interval *)
END_IF;

(* ---------------------------------------------------------------------------------------------------------------- *)
(* SUB-MODULE 1.1: TRIPLEX N1 LOW-PRESSURE ROTOR SPEED 2oo3 SENSOR VOTING                                          *)
(* Pickups: Ch A (Optical phonic wheel), Ch B (Eddy current probe), Ch C (Inductive magnetic pickup)                *)
(* ---------------------------------------------------------------------------------------------------------------- *)
rDiffAB := ABS(rN1_Speed_ChA_RPM - rN1_Speed_ChB_RPM);
rDiffBC := ABS(rN1_Speed_ChB_RPM - rN1_Speed_ChC_RPM);
rDiffCA := ABS(rN1_Speed_ChC_RPM - rN1_Speed_ChA_RPM);

(* Discrepancy threshold: 120.0 RPM cross-channel tolerance *)
IF NOT bN1_ChA_Fault AND NOT bN1_ChB_Fault AND NOT bN1_ChC_Fault THEN
    IF (rDiffAB <= 120.0) AND (rDiffCA <= 120.0) AND (rDiffBC <= 120.0) THEN
        (* All three pickups healthy: Select mathematical median *)
        IF (rN1_Speed_ChA_RPM >= rN1_Speed_ChB_RPM AND rN1_Speed_ChA_RPM <= rN1_Speed_ChC_RPM) OR
           (rN1_Speed_ChA_RPM <= rN1_Speed_ChB_RPM AND rN1_Speed_ChA_RPM >= rN1_Speed_ChC_RPM) THEN
            rN1_Voted_RPM := rN1_Speed_ChA_RPM;
        ELSIF (rN1_Speed_ChB_RPM >= rN1_Speed_ChA_RPM AND rN1_Speed_ChB_RPM <= rN1_Speed_ChC_RPM) OR
              (rN1_Speed_ChB_RPM <= rN1_Speed_ChA_RPM AND rN1_Speed_ChB_RPM >= rN1_Speed_ChC_RPM) THEN
            rN1_Voted_RPM := rN1_Speed_ChB_RPM;
        ELSE
            rN1_Voted_RPM := rN1_Speed_ChC_RPM;
        END_IF;
        rTimer_N1_Discrepancy_s := 0.0;
        bN1_Degraded_1oo2 := FALSE;
    ELSE
        (* Discrepancy detected: Integrate persistence timer (100 ms qualification time) *)
        rTimer_N1_Discrepancy_s := rTimer_N1_Discrepancy_s + rDt_sec;
        IF rTimer_N1_Discrepancy_s > 0.100 THEN
            IF (rDiffAB > 120.0) AND (rDiffCA > 120.0) THEN
                bN1_ChA_Fault := TRUE; (* Channel A isolated as faulty *)
            ELSIF (rDiffAB > 120.0) AND (rDiffBC > 120.0) THEN
                bN1_ChB_Fault := TRUE; (* Channel B isolated as faulty *)
            ELSE
                bN1_ChC_Fault := TRUE; (* Channel C isolated as faulty *)
            END_IF;
            bN1_Degraded_1oo2 := TRUE;
        END_IF;
        (* Provide temporary median during qualification *)
        rN1_Voted_RPM := (rN1_Speed_ChA_RPM + rN1_Speed_ChB_RPM + rN1_Speed_ChC_RPM) / 3.0;
    END_IF;
ELSIF bN1_Degraded_1oo2 AND NOT bN1_TotalFailure THEN
    (* Degraded 1oo2 dual-sensor averaging mode *)
    IF bN1_ChA_Fault AND NOT bN1_ChB_Fault AND NOT bN1_ChC_Fault THEN
        IF rDiffBC <= 140.0 THEN
            rN1_Voted_RPM := (rN1_Speed_ChB_RPM + rN1_Speed_ChC_RPM) * 0.5;
        ELSE
            bN1_TotalFailure := TRUE;
        END_IF;
    ELSIF bN1_ChB_Fault AND NOT bN1_ChA_Fault AND NOT bN1_ChC_Fault THEN
        IF rDiffCA <= 140.0 THEN
            rN1_Voted_RPM := (rN1_Speed_ChA_RPM + rN1_Speed_ChC_RPM) * 0.5;
        ELSE
            bN1_TotalFailure := TRUE;
        END_IF;
    ELSIF bN1_ChC_Fault AND NOT bN1_ChA_Fault AND NOT bN1_ChB_Fault THEN
        IF rDiffAB <= 140.0 THEN
            rN1_Voted_RPM := (rN1_Speed_ChA_RPM + rN1_Speed_ChB_RPM) * 0.5;
        ELSE
            bN1_TotalFailure := TRUE;
        END_IF;
    ELSE
        bN1_TotalFailure := TRUE;
    END_IF;
ELSE
    (* Total N1 sensor failure: Synthesize N1 speed from N2 core speed and compressor pressure ratio *)
    bN1_TotalFailure := TRUE;
    rN1_Voted_RPM := aState_x[1]; (* Fallback to state-space observer estimate *)
END_IF;

(* ---------------------------------------------------------------------------------------------------------------- *)
(* SUB-MODULE 1.2: TRIPLEX N2 HIGH-PRESSURE ROTOR SPEED 2oo3 SENSOR VOTING                                         *)
(* Resolvers: Ch A (Core gearbox resolver 1), Ch B (Resolver 2), Ch C (PMA frequency counter)                       *)
(* ---------------------------------------------------------------------------------------------------------------- *)
rDiffAB := ABS(rN2_Speed_ChA_RPM - rN2_Speed_ChB_RPM);
rDiffBC := ABS(rN2_Speed_ChB_RPM - rN2_Speed_ChC_RPM);
rDiffCA := ABS(rN2_Speed_ChC_RPM - rN2_Speed_ChA_RPM);

IF NOT bN2_ChA_Fault AND NOT bN2_ChB_Fault AND NOT bN2_ChC_Fault THEN
    IF (rDiffAB <= 180.0) AND (rDiffCA <= 180.0) AND (rDiffBC <= 180.0) THEN
        (* 2oo3 Median selection *)
        IF (rN2_Speed_ChA_RPM >= rN2_Speed_ChB_RPM AND rN2_Speed_ChA_RPM <= rN2_Speed_ChC_RPM) OR
           (rN2_Speed_ChA_RPM <= rN2_Speed_ChB_RPM AND rN2_Speed_ChA_RPM >= rN2_Speed_ChC_RPM) THEN
            rN2_Voted_RPM := rN2_Speed_ChA_RPM;
        ELSIF (rN2_Speed_ChB_RPM >= rN2_Speed_ChA_RPM AND rN2_Speed_ChB_RPM <= rN2_Speed_ChC_RPM) OR
              (rN2_Speed_ChB_RPM <= rN2_Speed_ChA_RPM AND rN2_Speed_ChB_RPM >= rN2_Speed_ChC_RPM) THEN
            rN2_Voted_RPM := rN2_Speed_ChB_RPM;
        ELSE
            rN2_Voted_RPM := rN2_Speed_ChC_RPM;
        END_IF;
        rTimer_N2_Discrepancy_s := 0.0;
        bN2_Degraded_1oo2 := FALSE;
    ELSE
        rTimer_N2_Discrepancy_s := rTimer_N2_Discrepancy_s + rDt_sec;
        IF rTimer_N2_Discrepancy_s > 0.080 THEN
            IF (rDiffAB > 180.0) AND (rDiffCA > 180.0) THEN
                bN2_ChA_Fault := TRUE;
            ELSIF (rDiffAB > 180.0) AND (rDiffBC > 180.0) THEN
                bN2_ChB_Fault := TRUE;
            ELSE
                bN2_ChC_Fault := TRUE;
            END_IF;
            bN2_Degraded_1oo2 := TRUE;
        END_IF;
        rN2_Voted_RPM := (rN2_Speed_ChA_RPM + rN2_Speed_ChB_RPM + rN2_Speed_ChC_RPM) / 3.0;
    END_IF;
ELSIF bN2_Degraded_1oo2 AND NOT bN2_TotalFailure THEN
    IF bN2_ChA_Fault AND NOT bN2_ChB_Fault AND NOT bN2_ChC_Fault THEN
        IF rDiffBC <= 220.0 THEN
            rN2_Voted_RPM := (rN2_Speed_ChB_RPM + rN2_Speed_ChC_RPM) * 0.5;
        ELSE
            bN2_TotalFailure := TRUE;
        END_IF;
    ELSIF bN2_ChB_Fault AND NOT bN2_ChA_Fault AND NOT bN2_ChC_Fault THEN
        IF rDiffCA <= 220.0 THEN
            rN2_Voted_RPM := (rN2_Speed_ChA_RPM + rN2_Speed_ChC_RPM) * 0.5;
        ELSE
            bN2_TotalFailure := TRUE;
        END_IF;
    ELSIF bN2_ChC_Fault AND NOT bN2_ChA_Fault AND NOT bN2_ChB_Fault THEN
        IF rDiffAB <= 220.0 THEN
            rN2_Voted_RPM := (rN2_Speed_ChA_RPM + rN2_Speed_ChB_RPM) * 0.5;
        ELSE
            bN2_TotalFailure := TRUE;
        END_IF;
    ELSE
        bN2_TotalFailure := TRUE;
    END_IF;
ELSE
    bN2_TotalFailure := TRUE;
    rN2_Voted_RPM := aState_x[2]; (* State-space observer fallback *)
END_IF;

(* ---------------------------------------------------------------------------------------------------------------- *)
(* SUB-MODULE 1.3: TRIPLEX COMPRESSOR DISCHARGE PRESSURE (Ps3) 2oo3 SENSOR VOTING                                   *)
(* Transducers: Silicon piezoresistive resonant quartz sensors Ch A, Ch B, Ch C (Tolerance = 18.0 psia)             *)
(* ---------------------------------------------------------------------------------------------------------------- *)
rDiffAB := ABS(rPs3_ChA_psia - rPs3_ChB_psia);
rDiffBC := ABS(rPs3_ChB_psia - rPs3_ChC_psia);
rDiffCA := ABS(rPs3_ChC_psia - rPs3_ChA_psia);

IF NOT bPs3_ChA_Fault AND NOT bPs3_ChB_Fault AND NOT bPs3_ChC_Fault THEN
    IF (rDiffAB <= 18.0) AND (rDiffCA <= 18.0) AND (rDiffBC <= 18.0) THEN
        IF (rPs3_ChA_psia >= rPs3_ChB_psia AND rPs3_ChA_psia <= rPs3_ChC_psia) OR
           (rPs3_ChA_psia <= rPs3_ChB_psia AND rPs3_ChA_psia >= rPs3_ChC_psia) THEN
            rPs3_Voted_psia := rPs3_ChA_psia;
        ELSIF (rPs3_ChB_psia >= rPs3_ChA_psia AND rPs3_ChB_psia <= rPs3_ChC_psia) OR
              (rPs3_ChB_psia <= rPs3_ChA_psia AND rPs3_ChB_psia >= rPs3_ChC_psia) THEN
            rPs3_Voted_psia := rPs3_ChB_psia;
        ELSE
            rPs3_Voted_psia := rPs3_ChC_psia;
        END_IF;
        rTimer_Ps3_Discrepancy_s := 0.0;
        bPs3_Degraded_1oo2 := FALSE;
    ELSE
        rTimer_Ps3_Discrepancy_s := rTimer_Ps3_Discrepancy_s + rDt_sec;
        IF rTimer_Ps3_Discrepancy_s > 0.120 THEN
            IF (rDiffAB > 18.0) AND (rDiffCA > 18.0) THEN
                bPs3_ChA_Fault := TRUE;
            ELSIF (rDiffAB > 18.0) AND (rDiffBC > 18.0) THEN
                bPs3_ChB_Fault := TRUE;
            ELSE
                bPs3_ChC_Fault := TRUE;
            END_IF;
            bPs3_Degraded_1oo2 := TRUE;
        END_IF;
        rPs3_Voted_psia := (rPs3_ChA_psia + rPs3_ChB_psia + rPs3_ChC_psia) / 3.0;
    END_IF;
ELSIF bPs3_Degraded_1oo2 AND NOT bPs3_TotalFailure THEN
    IF bPs3_ChA_Fault AND NOT bPs3_ChB_Fault AND NOT bPs3_ChC_Fault THEN
        rPs3_Voted_psia := (rPs3_ChB_psia + rPs3_ChC_psia) * 0.5;
    ELSIF bPs3_ChB_Fault AND NOT bPs3_ChA_Fault AND NOT bPs3_ChC_Fault THEN
        rPs3_Voted_psia := (rPs3_ChA_psia + rPs3_ChC_psia) * 0.5;
    ELSE
        rPs3_Voted_psia := (rPs3_ChA_psia + rPs3_ChB_psia) * 0.5;
    END_IF;
ELSE
    bPs3_TotalFailure := TRUE;
    rPs3_Voted_psia := aState_x[3];
END_IF;

(* ---------------------------------------------------------------------------------------------------------------- *)
(* SUB-MODULE 1.4: TRIPLEX ENGINE INLET PRESSURE (P2) 2oo3 SENSOR VOTING                                            *)
(* ---------------------------------------------------------------------------------------------------------------- *)
IF (ABS(rP2_ChA_psia - rP2_ChB_psia) <= 1.2) AND (ABS(rP2_ChA_psia - rP2_ChC_psia) <= 1.2) THEN
    IF (rP2_ChA_psia >= rP2_ChB_psia AND rP2_ChA_psia <= rP2_ChC_psia) OR
       (rP2_ChA_psia <= rP2_ChB_psia AND rP2_ChA_psia >= rP2_ChC_psia) THEN
        rP2_Voted_psia := rP2_ChA_psia;
    ELSIF (rP2_ChB_psia >= rP2_ChA_psia AND rP2_ChB_psia <= rP2_ChC_psia) OR
          (rP2_ChB_psia <= rP2_ChA_psia AND rP2_ChB_psia >= rP2_ChC_psia) THEN
        rP2_Voted_psia := rP2_ChB_psia;
    ELSE
        rP2_Voted_psia := rP2_ChC_psia;
    END_IF;
ELSE
    rP2_Voted_psia := (rP2_ChA_psia + rP2_ChB_psia + rP2_ChC_psia) / 3.0;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------- *)
(* SUB-MODULE 1.5: 8-THERMOCOUPLE CIRCUMFERENTIAL EGT HARNESS VALIDATION & PEAK EXTRACTION                          *)
(* ---------------------------------------------------------------------------------------------------------------- *)
aEGT_Raw_degC[1] := rEGT_TC1_degC;
aEGT_Raw_degC[2] := rEGT_TC2_degC;
aEGT_Raw_degC[3] := rEGT_TC3_degC;
aEGT_Raw_degC[4] := rEGT_TC4_degC;
aEGT_Raw_degC[5] := rEGT_TC5_degC;
aEGT_Raw_degC[6] := rEGT_TC6_degC;
aEGT_Raw_degC[7] := rEGT_TC7_degC;
aEGT_Raw_degC[8] := rEGT_TC8_degC;

rSum := 0.0;
iEGT_ValidCount := 0;
rEGT_Peak_degC := -100.0;
rEGT_Min_degC  := 2500.0;

(* Electrical validity boundaries: -40.0 deg C to +1250.0 deg C *)
FOR i := 1 TO 8 DO
    IF aEGT_Raw_degC[i] >= -40.0 AND aEGT_Raw_degC[i] <= 1250.0 THEN
        aEGT_Valid[i] := TRUE;
        rSum := rSum + aEGT_Raw_degC[i];
        iEGT_ValidCount := iEGT_ValidCount + 1;
        IF aEGT_Raw_degC[i] > rEGT_Peak_degC THEN
            rEGT_Peak_degC := aEGT_Raw_degC[i];
        END_IF;
        IF aEGT_Raw_degC[i] < rEGT_Min_degC THEN
            rEGT_Min_degC := aEGT_Raw_degC[i];
        END_IF;
    ELSE
        aEGT_Valid[i] := FALSE;
    END_IF;
END_FOR;

IF iEGT_ValidCount >= 4 THEN
    rEGT_Voted_Average_degC := rSum / REAL_TO_INT(iEGT_ValidCount);
    rEGT_Spread_degC := rEGT_Peak_degC - rEGT_Min_degC;
ELSE
    (* Severe thermocouple harness degradation: Use state observer estimate *)
    rEGT_Voted_Average_degC := aState_x[7];
    rEGT_Peak_degC := aState_x[7] + 35.0;
    rEGT_Spread_degC := 45.0;
END_IF;

(* Differentiate EGT to establish rate of rise dEGT/dt with low-pass filtering *)
rEGT_RateOfRise_degCs := 0.85 * rEGT_RateOfRise_degCs + 0.15 * ((rEGT_Voted_Average_degC - rEGT_Prev_degC) / rDt_sec);
rEGT_Prev_degC := rEGT_Voted_Average_degC;

(* ---------------------------------------------------------------------------------------------------------------- *)
(* SUB-MODULE 1.6: DUAL LVDT SENSOR VOTING (FMV, VSV, VBV)                                                         *)
(* ---------------------------------------------------------------------------------------------------------------- *)
(* Fuel Metering Valve (FMV) Dual LVDT *)
IF ABS(rFMV_Pos_LVDT1_mm - rFMV_Pos_LVDT2_mm) <= 0.85 THEN
    rFMV_Voted_Pos_mm := (rFMV_Pos_LVDT1_mm + rFMV_Pos_LVDT2_mm) * 0.5;
    bFMV_LVDT_Discrepancy := FALSE;
ELSE
    bFMV_LVDT_Discrepancy := TRUE;
    (* Arbitrate against Channel B cross-talk value if valid *)
    IF ABS(rFMV_Pos_LVDT1_mm - rCCDL_Rx_FMV_Pos_ChB_mm) < ABS(rFMV_Pos_LVDT2_mm - rCCDL_Rx_FMV_Pos_ChB_mm) THEN
        rFMV_Voted_Pos_mm := rFMV_Pos_LVDT1_mm;
    ELSE
        rFMV_Voted_Pos_mm := rFMV_Pos_LVDT2_mm;
    END_IF;
END_IF;

(* Variable Stator Vane (VSV) Dual LVDT *)
IF ABS(rVSV_Pos_LVDT1_deg - rVSV_Pos_LVDT2_deg) <= 1.5 THEN
    rVSV_Voted_Pos_deg := (rVSV_Pos_LVDT1_deg + rVSV_Pos_LVDT2_deg) * 0.5;
    bVSV_LVDT_Discrepancy := FALSE;
ELSE
    bVSV_LVDT_Discrepancy := TRUE;
    rVSV_Voted_Pos_deg := rVSV_Pos_LVDT1_deg; (* Channel A prioritized *)
END_IF;

(* Variable Bleed Valve (VBV) Dual LVDT *)
IF ABS(rVBV_Pos_LVDT1_pct - rVBV_Pos_LVDT2_pct) <= 3.0 THEN
    rVBV_Voted_Pos_pct := (rVBV_Pos_LVDT1_pct + rVBV_Pos_LVDT2_pct) * 0.5;
    bVBV_LVDT_Discrepancy := FALSE;
ELSE
    bVBV_LVDT_Discrepancy := TRUE;
    rVBV_Voted_Pos_pct := rVBV_Pos_LVDT1_pct;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------- *)
(* SUB-MODULE 1.7: FADEC DUAL-CHANNEL MASTER / HOT-STANDBY ARBITRATION                                              *)
(* ---------------------------------------------------------------------------------------------------------------- *)
IF (wCCDL_RxWord_ChB_Status AND 16#8000) <> 16#0000 THEN
    rTimer_CCDL_Timeout_s := 0.0;
    bCCDL_LinkLost := FALSE;
ELSE
    rTimer_CCDL_Timeout_s := rTimer_CCDL_Timeout_s + rDt_sec;
    IF rTimer_CCDL_Timeout_s > 0.150 THEN
        bCCDL_LinkLost := TRUE;
    END_IF;
END_IF;

(* Master Channel Arbitration Logic: Channel A retains control unless internal BIT fails *)
IF bChannelA_HealthOK THEN
    IF bChannelA_MasterRequest OR NOT bChannelB_HealthOK THEN
        bMasterChannelActive := TRUE;
    ELSE
        bMasterChannelActive := TRUE; (* Standard dispatch default *)
    END_IF;
ELSIF bChannelB_HealthOK THEN
    bMasterChannelActive := FALSE; (* Bumpless transfer to Channel B *)
ELSE
    bMasterChannelActive := TRUE;  (* Freeze in place on dual degradation *)
END_IF;
bFADEC_ChannelA_InControl := bMasterChannelActive;
""")

    # 4. PHASE 2: Cyber-Physical Propulsion Observers, Aerodynamics & Clearance
    code_lines.append("""
(* ================================================================================================================ *)
(* PHASE 2: CYBER-PHYSICAL PROPULSION OBSERVERS, COMPRESSOR AERODYNAMICS & TURBINE CLEARANCE                           *)
(* ================================================================================================================ *)
(* Ambient Station 2 Total Temperature and Pressure Dimensionless Ratios *)
rTheta_T2 := (rTotalAirTemp_degC + 273.15) / 288.15;
IF rTheta_T2 < 0.40 THEN
    rTheta_T2 := 0.40;
END_IF;
rSqrtTheta := SQRT(rTheta_T2);

rDelta_P2 := rTotalPressure_psia / 14.696;
IF rDelta_P2 < 0.15 THEN
    rDelta_P2 := 0.15;
END_IF;

(* Aerodynamically Corrected Spool Speeds *)
rN1_Corrected_RPM := rN1_Voted_RPM / rSqrtTheta;
rN2_Corrected_RPM := rN2_Voted_RPM / rSqrtTheta;

(* Physical Spool Speed Percentages *)
rN1_Pct := (rN1_Voted_RPM / 2850.0) * 100.0;
rN2_Pct := (rN2_Voted_RPM / 10800.0) * 100.0;

(* Pressure Ratios *)
rCompressorPrRatio       := rPs3_Voted_psia / MAX(rP2_Voted_psia, 2.0);
rEPR_EnginePressureRatio := rPs3_Voted_psia / MAX(rTotalPressure_psia, 2.0);

(* ---------------------------------------------------------------------------------------------------------------- *)
(* SUB-MODULE 2.1: HIGH-PRESSURE COMPRESSOR VARIABLE STATOR VANE (VSV) AERODYNAMIC SCHEDULE                         *)
(* Prevents Rotating Stall and Acoustic Blade Flutter via Staged Vane Pitch Modulation                              *)
(* ---------------------------------------------------------------------------------------------------------------- *)
IF rN2_Corrected_RPM < 6200.0 THEN
    (* Low speed & starting: Vanes parked at extreme closed position to minimize start torque *)
    rVSV_Schedule_Target_deg := -15.0;
ELSIF rN2_Corrected_RPM >= 6200.0 AND rN2_Corrected_RPM < 8800.0 THEN
    (* Sub-idle to intermediate transition ramp *)
    rVSV_Schedule_Target_deg := -15.0 + ((rN2_Corrected_RPM - 6200.0) / 2600.0) * 25.0;
ELSIF rN2_Corrected_RPM >= 8800.0 AND rN2_Corrected_RPM < 10400.0 THEN
    (* Core power acceleration ramp *)
    rVSV_Schedule_Target_deg := 10.0 + ((rN2_Corrected_RPM - 8800.0) / 1600.0) * 22.0;
ELSE
    (* Maximum rated takeoff & climb core speed: Vanes fully open for maximum core mass flow *)
    rVSV_Schedule_Target_deg := 32.0;
END_IF;

(* Ambient temperature trim modifier (-0.06 deg per deg C above standard 15 C day) *)
rVSV_Schedule_Target_deg := rVSV_Schedule_Target_deg - 0.06 * (rTotalAirTemp_degC - 15.0);

(* Clamp VSV target within physical travel stops *)
IF rVSV_Schedule_Target_deg > 35.0 THEN
    rVSV_Schedule_Target_deg := 35.0;
ELSIF rVSV_Schedule_Target_deg < -15.0 THEN
    rVSV_Schedule_Target_deg := -15.0;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------- *)
(* SUB-MODULE 2.2: COMPRESSOR VARIABLE BLEED VALVE (VBV) SCHEDULE                                                   *)
(* Vents Booster Discharge Air into Bypass Duct during Deceleration & Idle to Prevent Booster Stall                  *)
(* ---------------------------------------------------------------------------------------------------------------- *)
IF rN2_Corrected_RPM < 6800.0 THEN
    (* Ground idle & dry crank: VBV open to 85% *)
    rVBV_Schedule_Target_pct := 85.0;
ELSIF rN2_Corrected_RPM >= 6800.0 AND rN2_Corrected_RPM < 9400.0 THEN
    (* Staged linear closing schedule *)
    rVBV_Schedule_Target_pct := 85.0 - ((rN2_Corrected_RPM - 6800.0) / 2600.0) * 85.0;
ELSE
    (* High power cruise, climb and takeoff: VBV fully shut *)
    rVBV_Schedule_Target_pct := 0.0;
END_IF;

(* Dynamic deceleration modifier: If pilot is chopping throttle rapidly, force VBV open *)
IF (rThrottleLeverAngle_deg < 10.0) AND (rN2_Pct > 70.0) THEN
    rVBV_Schedule_Target_pct := MAX(rVBV_Schedule_Target_pct, 45.0);
END_IF;

(* Clamp VBV target to mechanical stops *)
IF rVBV_Schedule_Target_pct > 100.0 THEN
    rVBV_Schedule_Target_pct := 100.0;
ELSIF rVBV_Schedule_Target_pct < 0.0 THEN
    rVBV_Schedule_Target_pct := 0.0;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------- *)
(* SUB-MODULE 2.3: AERODYNAMIC COMPRESSOR SURGE MARGIN & RATE-OF-CHANGE SURVEILLANCE                               *)
(* Surge Boundary Line Formulation: (Wf / Ps3)_surge = c0 + c1 * N2c + c2 * N2c^2                                   *)
(* ---------------------------------------------------------------------------------------------------------------- *)
rSurgeLine_WfPs3 := 0.0450 + 0.0000185 * rN2_Corrected_RPM + 0.00000000125 * (rN2_Corrected_RPM * rN2_Corrected_RPM);
rAccelLimit_WfPs3 := 0.865 * rSurgeLine_WfPs3; (* 13.5% Surge safety acceleration buffer *)
rDecelLimit_WfPs3 := 0.0125 + 0.0000038 * rN2_Corrected_RPM; (* Lean flameout limit *)

(* Real-Time Operating Fuel Flow to Static Pressure Ratio *)
rActiveFuelFlow_pph := aState_x[15] * 1150.0; (* Calibrated fuel flow from FMV orifice *)
rActual_WfPs3 := rActiveFuelFlow_pph / MAX(rPs3_Voted_psia, 12.0);

(* Calculated Compressor Surge Margin Percentage *)
IF rSurgeLine_WfPs3 > 0.001 THEN
    rSurgeMargin_Calculated := ((rSurgeLine_WfPs3 - rActual_WfPs3) / rSurgeLine_WfPs3) * 100.0;
ELSE
    rSurgeMargin_Calculated := 20.0;
END_IF;
rSurgeMargin_pct := rSurgeMargin_Calculated;

(* Severe Aerodynamic Compressor Stall / Surge Detection *)
rPs3_RateOfChange_psias := (rPs3_Voted_psia - rPs3_Prev_psia) / rDt_sec;
rPs3_Prev_psia := rPs3_Voted_psia;

IF (rPs3_RateOfChange_psias < -185.0) AND (rN2_Pct > 55.0) THEN
    bStallSurgeDetected := TRUE;
ELSE
    bStallSurgeDetected := FALSE;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------- *)
(* SUB-MODULE 2.4: HIGH-PRESSURE TURBINE ACTIVE CLEARANCE CONTROL (HPTACC) CYBER-PHYSICS                            *)
(* Regulates Fan Bleed Air onto Casing Flange to Hold Radial Blade Tip Clearance at 0.25 mm (+/- 0.05 mm)            *)
(* ---------------------------------------------------------------------------------------------------------------- *)
(* Thermal Expansion of Turbine Outer Casing Ring: delta_r_case = r0 * alpha_case * (T_case - T_ref) *)
rThermalGrowth_Case_HPT_mm := 480.0 * 0.0000142 * (aState_x[8] - 20.0);

(* Thermal Growth of Turbine Rotor Disk & Blade: delta_r_rotor = r0 * alpha_disk * (T_disk - T_ref) *)
rThermalGrowth_Rotor_HPT_mm := 480.0 * 0.0000128 * (aState_x[9] - 20.0);

(* Mechanical Centrifugal Stretch of HPT Blades: delta_r_centrif = k * (N2 / 10000)^2 *)
rCentrifugalGrowth_HPT_mm := 0.420 * ((rN2_Voted_RPM / 10000.0) * (rN2_Voted_RPM / 10000.0));

(* Real-Time Running Blade Tip Radial Clearance Gap *)
rRunningClearance_HPT_calc_mm := 0.850 + rThermalGrowth_Case_HPT_mm - (rThermalGrowth_Rotor_HPT_mm + rCentrifugalGrowth_HPT_mm);
IF rRunningClearance_HPT_calc_mm < 0.05 THEN
    rRunningClearance_HPT_calc_mm := 0.05; (* Rub-in physical shroud limit *)
END_IF;
rHPT_RunningClearance_mm := rRunningClearance_HPT_calc_mm;

(* HPT Active Clearance Control PI Regulation Loop *)
rClearanceError_HPT_mm := rRunningClearance_HPT_calc_mm - rTargetClearance_HPT_mm;

(* Integrate cooling demand when engine is in stabilized cruise condition *)
IF (rN2_Pct > 82.0) AND (rMachNumber > 0.65) AND NOT bWeightOnWheels THEN
    rHPTACC_Integrator_pct := rHPTACC_Integrator_pct + 45.0 * rClearanceError_HPT_mm * rDt_sec;
    IF rHPTACC_Integrator_pct > 100.0 THEN
        rHPTACC_Integrator_pct := 100.0;
    ELSIF rHPTACC_Integrator_pct < 0.0 THEN
        rHPTACC_Integrator_pct := 0.0;
    END_IF;
    rHPTACC_ValveDemand_pct := 35.0 * rClearanceError_HPT_mm + rHPTACC_Integrator_pct;
ELSE
    (* Ground, takeoff and low climb: Inhibit HPTACC to prevent blade pinch during re-acceleration *)
    rHPTACC_Integrator_pct := 0.0;
    rHPTACC_ValveDemand_pct := 0.0;
END_IF;

(* Clamp HPTACC valve command *)
IF rHPTACC_ValveDemand_pct > 100.0 THEN
    rHPTACC_ValveDemand_pct := 100.0;
ELSIF rHPTACC_ValveDemand_pct < 0.0 THEN
    rHPTACC_ValveDemand_pct := 0.0;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------- *)
(* SUB-MODULE 2.5: LOW-PRESSURE TURBINE ACTIVE CLEARANCE CONTROL (LPTACC) CYBER-PHYSICS                             *)
(* ---------------------------------------------------------------------------------------------------------------- *)
rThermalGrowth_Case_LPT_mm  := 680.0 * 0.0000135 * (aState_x[11] - 20.0);
rThermalGrowth_Rotor_LPT_mm := 680.0 * 0.0000118 * (aState_x[7] * 0.65 - 20.0);
rCentrifugalGrowth_LPT_mm   := 0.310 * ((rN1_Voted_RPM / 2850.0) * (rN1_Voted_RPM / 2850.0));

rRunningClearance_LPT_calc_mm := 1.150 + rThermalGrowth_Case_LPT_mm - (rThermalGrowth_Rotor_LPT_mm + rCentrifugalGrowth_LPT_mm);
IF rRunningClearance_LPT_calc_mm < 0.10 THEN
    rRunningClearance_LPT_calc_mm := 0.10;
END_IF;
rLPT_RunningClearance_mm := rRunningClearance_LPT_calc_mm;

rClearanceError_LPT_mm := rRunningClearance_LPT_calc_mm - rTargetClearance_LPT_mm;
IF (rN1_Pct > 75.0) AND NOT bWeightOnWheels THEN
    rLPTACC_Integrator_pct := rLPTACC_Integrator_pct + 32.0 * rClearanceError_LPT_mm * rDt_sec;
    IF rLPTACC_Integrator_pct > 100.0 THEN
        rLPTACC_Integrator_pct := 100.0;
    ELSIF rLPTACC_Integrator_pct < 0.0 THEN
        rLPTACC_Integrator_pct := 0.0;
    END_IF;
    rLPTACC_ValveDemand_pct := 28.0 * rClearanceError_LPT_mm + rLPTACC_Integrator_pct;
ELSE
    rLPTACC_Integrator_pct := 0.0;
    rLPTACC_ValveDemand_pct := 0.0;
END_IF;

IF rLPTACC_ValveDemand_pct > 100.0 THEN
    rLPTACC_ValveDemand_pct := 100.0;
ELSIF rLPTACC_ValveDemand_pct < 0.0 THEN
    rLPTACC_ValveDemand_pct := 0.0;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------- *)
(* SUB-MODULE 2.6: TURBINE HOT-SECTION CUMULATIVE THERMAL CREEP FATIGUE LIFE CONSUMPTION                            *)
(* ---------------------------------------------------------------------------------------------------------------- *)
IF rEGT_Peak_degC > 820.0 THEN
    (* Larson-Miller parameter exponentiation: Creep damage accelerates exponentially with temperature *)
    rHotSectionCreepFactor := EXP(0.0195 * (rEGT_Peak_degC - 820.0));
    rThermalDamageAccumulator := rThermalDamageAccumulator + (rHotSectionCreepFactor * rDt_sec) / 3600.0;
END_IF;
rLarsonMillerParameter := (rEGT_Peak_degC + 273.15) * (20.0 + 4.25);
rEstimatedEGT_Margin_degC := 1040.0 - rEGT_Peak_degC;
""")

    # 5. PHASE 3: Discrete State-Space Model Propagation
    code_lines.append("""
(* ================================================================================================================ *)
(* PHASE 3: DISCRETE STATE-SPACE MODEL PROPAGATION (x[k+1] = A * x[k] + B * u[k])                                    *)
(* ================================================================================================================ *)
(* Assemble internal control vector u[1..8] *)
aControl_u[1] := rFMV_TorqueMotorCmd_mA;
aControl_u[2] := rVSV_ActuatorDemand_deg;
aControl_u[3] := rVBV_ActuatorDemand_pct;
aControl_u[4] := rHPTACC_ValveDemand_pct;
aControl_u[5] := rLPTACC_ValveDemand_pct;
IF bStarterAirValve_Open THEN
    aControl_u[6] := 1.0;
ELSE
    aControl_u[6] := 0.0;
END_IF;
IF bIgniterA_Fire OR bIgniterB_Fire THEN
    aControl_u[7] := 1.0;
ELSE
    aControl_u[7] := 0.0;
END_IF;
IF bThrustReverser_DeployCmd THEN
    aControl_u[8] := 1.0;
ELSE
    aControl_u[8] := 0.0;
END_IF;

(* Compute x[k+1] = A * x[k] + B * u[k] *)
FOR i := 1 TO 16 DO
    rSum := 0.0;
    FOR j := 1 TO 16 DO
        rSum := rSum + aA[i, j] * aState_x[j];
    END_FOR;
    FOR k := 1 TO 8 DO
        rSum := rSum + aB[i, k] * aControl_u[k];
    END_FOR;
    aState_x_next[i] := rSum;
END_FOR;

(* Apply Cyber-Physical Boundary Clamping on State Vector *)
(* State 1: N1 Speed (0.0 to 3300.0 RPM) *)
IF aState_x_next[1] < 0.0 THEN
    aState_x_next[1] := 0.0;
ELSIF aState_x_next[1] > 3300.0 THEN
    aState_x_next[1] := 3300.0;
END_IF;

(* State 2: N2 Speed (0.0 to 12200.0 RPM) *)
IF aState_x_next[2] < 0.0 THEN
    aState_x_next[2] := 0.0;
ELSIF aState_x_next[2] > 12200.0 THEN
    aState_x_next[2] := 12200.0;
END_IF;

(* State 3: Ps3 Static Pressure (8.0 to 750.0 psia) *)
IF aState_x_next[3] < 8.0 THEN
    aState_x_next[3] := 8.0;
ELSIF aState_x_next[3] > 750.0 THEN
    aState_x_next[3] := 750.0;
END_IF;

(* State 4: Tt3 Total Temperature (-40.0 to 750.0 deg C) *)
IF aState_x_next[4] < -40.0 THEN
    aState_x_next[4] := -40.0;
ELSIF aState_x_next[4] > 750.0 THEN
    aState_x_next[4] := 750.0;
END_IF;

(* State 5: Combustor Pressure (8.0 to 720.0 psia) *)
IF aState_x_next[5] < 8.0 THEN
    aState_x_next[5] := 8.0;
ELSIF aState_x_next[5] > 720.0 THEN
    aState_x_next[5] := 720.0;
END_IF;

(* State 6: Combustor Gas Temperature (0.0 to 1850.0 deg C) *)
IF aState_x_next[6] < 0.0 THEN
    aState_x_next[6] := 0.0;
ELSIF aState_x_next[6] > 1850.0 THEN
    aState_x_next[6] := 1850.0;
END_IF;

(* State 7: T4.5 EGT Temperature (-40.0 to 1250.0 deg C) *)
IF aState_x_next[7] < -40.0 THEN
    aState_x_next[7] := -40.0;
ELSIF aState_x_next[7] > 1250.0 THEN
    aState_x_next[7] := 1250.0;
END_IF;

(* State 8: HPT Case Metal Temp (-40.0 to 800.0 deg C) *)
IF aState_x_next[8] < -40.0 THEN
    aState_x_next[8] := -40.0;
ELSIF aState_x_next[8] > 800.0 THEN
    aState_x_next[8] := 800.0;
END_IF;

(* State 9: HPT Disk Bulk Temp (-40.0 to 750.0 deg C) *)
IF aState_x_next[9] < -40.0 THEN
    aState_x_next[9] := -40.0;
ELSIF aState_x_next[9] > 750.0 THEN
    aState_x_next[9] := 750.0;
END_IF;

(* State 10: HPT Tip Clearance Gap (0.05 to 2.50 mm) *)
IF aState_x_next[10] < 0.05 THEN
    aState_x_next[10] := 0.05;
ELSIF aState_x_next[10] > 2.50 THEN
    aState_x_next[10] := 2.50;
END_IF;

(* State 11: LPT Case Metal Temp (-40.0 to 700.0 deg C) *)
IF aState_x_next[11] < -40.0 THEN
    aState_x_next[11] := -40.0;
ELSIF aState_x_next[11] > 700.0 THEN
    aState_x_next[11] := 700.0;
END_IF;

(* State 12: LPT Tip Clearance Gap (0.10 to 3.00 mm) *)
IF aState_x_next[12] < 0.10 THEN
    aState_x_next[12] := 0.10;
ELSIF aState_x_next[12] > 3.00 THEN
    aState_x_next[12] := 3.00;
END_IF;

(* State 13: VBV Position (0.0 to 100.0 %) *)
IF aState_x_next[13] < 0.0 THEN
    aState_x_next[13] := 0.0;
ELSIF aState_x_next[13] > 100.0 THEN
    aState_x_next[13] := 100.0;
END_IF;

(* State 14: VSV Angle (-15.0 to 35.0 deg) *)
IF aState_x_next[14] < -15.0 THEN
    aState_x_next[14] := -15.0;
ELSIF aState_x_next[14] > 35.0 THEN
    aState_x_next[14] := 35.0;
END_IF;

(* State 15: FMV Spool Position (0.0 to 35.0 mm) *)
IF aState_x_next[15] < 0.0 THEN
    aState_x_next[15] := 0.0;
ELSIF aState_x_next[15] > 35.0 THEN
    aState_x_next[15] := 35.0;
END_IF;

(* State 16: Net Propulsive Thrust (-50000.0 to 118000.0 lbf) *)
IF aState_x_next[16] < -50000.0 THEN
    aState_x_next[16] := -50000.0;
ELSIF aState_x_next[16] > 118000.0 THEN
    aState_x_next[16] := 118000.0;
END_IF;

(* Advance state vector *)
FOR i := 1 TO 16 DO
    aState_x[i] := aState_x_next[i];
END_FOR;

(* Calculate Measurement Observables y = C * x + D * u *)
FOR m := 1 TO 8 DO
    rSum := 0.0;
    FOR j := 1 TO 16 DO
        rSum := rSum + aC[m, j] * aState_x[j];
    END_FOR;
    FOR k := 1 TO 8 DO
        rSum := rSum + aD[m, k] * aControl_u[k];
    END_FOR;
    aOutput_y[m] := rSum;
END_FOR;

rCalculatedNetThrust_lbf := aOutput_y[1];
""")

    # 6. PHASE 4: Receding-Horizon Model Predictive Control (MPC)
    code_lines.append("""
(* ================================================================================================================ *)
(* PHASE 4: RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) & FUEL METERING SERVO PACING                              *)
(* ================================================================================================================ *)
(* Map Cockpit Throttle Lever Angle (TLA: 0.0 to 45.0 deg) into Target Thrust Schedule *)
IF rThrottleLeverAngle_deg <= 2.5 THEN
    (* Ground Idle Rating *)
    rDemandThrust_lbf := 4500.0;
ELSIF rThrottleLeverAngle_deg > 2.5 AND rThrottleLeverAngle_deg <= 16.0 THEN
    (* Taxi Thrust Zone: 4,500 to 18,000 lbf *)
    rDemandThrust_lbf := 4500.0 + ((rThrottleLeverAngle_deg - 2.5) / 13.5) * 13500.0;
ELSIF rThrottleLeverAngle_deg > 16.0 AND rThrottleLeverAngle_deg <= 32.0 THEN
    (* Maximum Cruise / Climb Thrust: 18,000 to 86,000 lbf *)
    rDemandThrust_lbf := 18000.0 + ((rThrottleLeverAngle_deg - 16.0) / 16.0) * 68000.0;
ELSE
    (* Rated Takeoff Thrust Zone: 86,000 to 110,000 lbf (Sea-Level Static Rating) *)
    rDemandThrust_lbf := 86000.0 + ((rThrottleLeverAngle_deg - 32.0) / 13.0) * 24000.0;
END_IF;

(* Altitude and Temperature Thrust Derate Compensator *)
IF rAltitude_ft > 1000.0 THEN
    (* Thrust lapses with air density ratio sigma = (1 - 0.000006875 * Alt)^4.256 *)
    rDemandThrust_lbf := rDemandThrust_lbf * MAX((1.0 - 0.0000215 * rAltitude_ft), 0.22);
END_IF;

(* Populate MPC Reference Vector y_ref *)
aY_Ref[1] := rDemandThrust_lbf;                           (* Net thrust target *)
aY_Ref[2] := 3.789;                                       (* Target spool speed ratio N2/N1 *)
aY_Ref[3] := (rDemandThrust_lbf / 110000.0) * 38500.0;     (* Steady-state fuel flow schedule [pph] *)
aY_Ref[4] := 22.5;                                        (* Target surge margin [22.5%] *)
aY_Ref[5] := 110.0;                                       (* Target EGT margin to redline [deg C] *)
aY_Ref[6] := 0.0;                                         (* HPT active tip clearance error target [0.0 mm] *)
aY_Ref[7] := 0.355;                                       (* Target TSFC [lb/(lbf*h)] *)
aY_Ref[8] := 0.038;                                       (* Equivalence ratio *)

(* ---------------------------------------------------------------------------------------------------------------- *)
(* SUB-MODULE 4.1: 5-STEP RECEDING HORIZON TRAJECTORY PREDICTION                                                   *)
(* Evaluates forward state-space propagation across prediction horizon Np = 5                                      *)
(* ---------------------------------------------------------------------------------------------------------------- *)
(* Initialize prediction state at Step 1 from current state *)
FOR j := 1 TO 16 DO
    aPred_x[1, j] := aState_x[j];
END_FOR;

FOR n := 1 TO 4 DO
    FOR i := 1 TO 16 DO
        rSum := 0.0;
        FOR j := 1 TO 16 DO
            rSum := rSum + aA[i, j] * aPred_x[n, j];
        END_FOR;
        FOR k := 1 TO 8 DO
            rSum := rSum + aB[i, k] * aControl_u[k];
        END_FOR;
        aPred_x[n + 1, i] := rSum;
    END_FOR;
END_FOR;

(* Calculate Predicted Measurement Outputs Across Horizon *)
FOR n := 1 TO 5 DO
    FOR m := 1 TO 8 DO
        rSum := 0.0;
        FOR j := 1 TO 16 DO
            rSum := rSum + aC[m, j] * aPred_x[n, j];
        END_FOR;
        FOR k := 1 TO 8 DO
            rSum := rSum + aD[m, k] * aControl_u[k];
        END_FOR;
        aPred_y[n, m] := rSum;
    END_FOR;
END_FOR;

(* ---------------------------------------------------------------------------------------------------------------- *)
(* SUB-MODULE 4.2: QUADRATIC COST FUNCTION EVALUATION & NUMERICAL GRADIENT ESTIMATION                               *)
(* J = SUM_{p=1..5} (y_pred - y_ref)^T * Q * (y_pred - y_ref) + Delta_u^T * R * Delta_u + Constraints               *)
(* ---------------------------------------------------------------------------------------------------------------- *)
rMPC_CostJ := 0.0;
FOR n := 1 TO 5 DO
    FOR m := 1 TO 8 DO
        rMPC_CostJ := rMPC_CostJ + aQ_Weight[m] * (aPred_y[n, m] - aY_Ref[m]) * (aPred_y[n, m] - aY_Ref[m]);
    END_FOR;
END_FOR;

(* Add Actuator Slew Rate Penalties *)
FOR k := 1 TO 8 DO
    rMPC_CostJ := rMPC_CostJ + aR_Weight[k] * (aControl_u[k] - aU_Prev[k]) * (aControl_u[k] - aU_Prev[k]);
END_FOR;

(* Surge Constraint Soft-Barrier Penalty *)
FOR n := 1 TO 5 DO
    IF aPred_y[n, 4] < 12.0 THEN (* Surge margin drops below critical 12.0% *)
        rMPC_CostJ := rMPC_CostJ + 8500.0 * (12.0 - aPred_y[n, 4]) * (12.0 - aPred_y[n, 4]);
    END_IF;
    IF aPred_x[n, 7] > 1010.0 THEN (* EGT exceeds thermal caution 1010.0 deg C *)
        rMPC_CostJ := rMPC_CostJ + 12000.0 * (aPred_x[n, 7] - 1010.0) * (aPred_x[n, 7] - 1010.0);
    END_IF;
END_FOR;

(* Numerical Cost Gradient with respect to Fuel Flow Command *)
rGrad_Wf := 2.0 * aQ_Weight[1] * (aPred_y[5, 1] - aY_Ref[1]) * 0.035 + 2.0 * aR_Weight[1] * (aControl_u[1] - aU_Prev[1]);
rGrad_VSV := 2.0 * aQ_Weight[4] * (aPred_y[5, 4] - aY_Ref[4]) * (-0.65) + 2.0 * aR_Weight[2] * (aControl_u[2] - aU_Prev[2]);
rGrad_ACC := 2.0 * aQ_Weight[6] * (aPred_y[5, 6] - aY_Ref[6]) * (-0.0022) + 2.0 * aR_Weight[4] * (aControl_u[4] - aU_Prev[4]);

(* Gradient Descent Candidate Updates with Projection onto Surge Schedules *)
rDeltaWf_Candidate := -rStepSize_Wf * rGrad_Wf;
rDeltaVSV_Candidate := -rStepSize_VSV * rGrad_VSV;
rDeltaACC_Candidate := -rStepSize_ACC * rGrad_ACC;

(* Compute Dynamic Fuel Flow Demand Wf *)
rTargetFuelFlow_pph := rActiveFuelFlow_pph + rDeltaWf_Candidate;

(* ---------------------------------------------------------------------------------------------------------------- *)
(* SUB-MODULE 4.3: COMPRESSOR ACCELERATION & DECELERATION SURGE SCHEDULE LIMITING                                   *)
(* ---------------------------------------------------------------------------------------------------------------- *)
(* Enforce Dynamic Surge Margin Fuel Acceleration Ceiling *)
IF (rTargetFuelFlow_pph / MAX(rPs3_Voted_psia, 12.0)) > rAccelLimit_WfPs3 THEN
    rTargetFuelFlow_pph := rAccelLimit_WfPs3 * rPs3_Voted_psia;
END_IF;

(* Enforce Lean Blowout Deceleration Floor *)
IF (rTargetFuelFlow_pph / MAX(rPs3_Voted_psia, 12.0)) < rDecelLimit_WfPs3 THEN
    rTargetFuelFlow_pph := rDecelLimit_WfPs3 * rPs3_Voted_psia;
END_IF;

(* Physical Absolute Maximum Fuel Flow Envelope (Takeoff rating ceiling 42,000 pph) *)
IF rTargetFuelFlow_pph > 42000.0 THEN
    rTargetFuelFlow_pph := 42000.0;
ELSIF rTargetFuelFlow_pph < 450.0 THEN
    rTargetFuelFlow_pph := 450.0; (* Sub-idle minimum flame retention flow *)
END_IF;

(* ---------------------------------------------------------------------------------------------------------------- *)
(* SUB-MODULE 4.4: FUEL METERING VALVE (FMV) TORQUE MOTOR CLOSED-LOOP POSITION SERVO                                *)
(* ---------------------------------------------------------------------------------------------------------------- *)
(* Compute required FMV spool opening from mass fuel flow and Delta-P regulating valve pressure *)
(* Formula: A_fmv = Wf / (Cd * sqrt(2 * rho * DeltaP)) *)
IF rDeltaP_FMV_psid > 15.0 THEN
    rFMV_TargetSpool_mm := (rTargetFuelFlow_pph / 1150.0) * SQRT(42.0 / rDeltaP_FMV_psid);
ELSE
    rFMV_TargetSpool_mm := rTargetFuelFlow_pph / 1150.0;
END_IF;

IF rFMV_TargetSpool_mm > 34.0 THEN
    rFMV_TargetSpool_mm := 34.0;
ELSIF rFMV_TargetSpool_mm < 0.0 THEN
    rFMV_TargetSpool_mm := 0.0;
END_IF;

(* Dual-Wound Torque Motor Closed-Loop PI Position Controller *)
rFMV_PositionError_mm := rFMV_TargetSpool_mm - rFMV_Voted_Pos_mm;
rFMV_LoopProportional_mA := 8.50 * rFMV_PositionError_mm;

(* Integral term with anti-windup clamping (-12.0 mA to +12.0 mA) *)
rFMV_LoopIntegrator_mA := rFMV_LoopIntegrator_mA + 18.5 * rFMV_PositionError_mm * rDt_sec;
IF rFMV_LoopIntegrator_mA > 12.0 THEN
    rFMV_LoopIntegrator_mA := 12.0;
ELSIF rFMV_LoopIntegrator_mA < -12.0 THEN
    rFMV_LoopIntegrator_mA := -12.0;
END_IF;

(* 85 Hz Anti-Stiction Dither Current Harmonic Synthesis *)
rFMV_DitherPhase_rad := rFMV_DitherPhase_rad + 2.0 * 3.14159265 * 85.0 * rDt_sec;
IF rFMV_DitherPhase_rad > 6.2831853 THEN
    rFMV_DitherPhase_rad := rFMV_DitherPhase_rad - 6.2831853;
END_IF;
rFMV_DitherCurrent_mA := 2.20 * SIN(rFMV_DitherPhase_rad);

(* Consolidate Total Torque Motor Drive Current Command *)
rFMV_TotalDriveCurrent_mA := rFMV_LoopProportional_mA + rFMV_LoopIntegrator_mA + rFMV_DitherCurrent_mA;

(* Torque Motor Command Current Saturation (-40.0 mA to +40.0 mA) *)
IF rFMV_TotalDriveCurrent_mA > 40.0 THEN
    rFMV_TorqueMotorCmd_mA := 40.0;
ELSIF rFMV_TotalDriveCurrent_mA < -40.0 THEN
    rFMV_TorqueMotorCmd_mA := -40.0;
ELSE
    rFMV_TorqueMotorCmd_mA := rFMV_TotalDriveCurrent_mA;
END_IF;

(* VSV Actuator Demand Consolidation *)
rVSV_ActuatorDemand_deg := rVSV_Schedule_Target_deg + rDeltaVSV_Candidate;
IF rVSV_ActuatorDemand_deg > 35.0 THEN
    rVSV_ActuatorDemand_deg := 35.0;
ELSIF rVSV_ActuatorDemand_deg < -15.0 THEN
    rVSV_ActuatorDemand_deg := -15.0;
END_IF;

(* VBV Actuator Demand Consolidation *)
rVBV_ActuatorDemand_pct := rVBV_Schedule_Target_pct;

(* Save Control Action History for Next Execution Cycle *)
FOR k := 1 TO 8 DO
    aU_Prev[k] := aControl_u[k];
END_FOR;
""")

    # 7. PHASE 5: 12-Stage Operational Finite State Machine
    code_lines.append("""
(* ================================================================================================================ *)
(* PHASE 5: 12-STAGE OPERATIONAL FINITE STATE MACHINE (FSM) INDUSTRIAL AEROSPACE SEQUENCE                            *)
(* ================================================================================================================ *)
rStateTimer_s := rStateTimer_s + rDt_sec;

CASE iFSM_State OF

    (* ------------------------------------------------------------------------------------------------------------ *)
    (* STATE 0: PRE-FLIGHT BUILT-IN-TEST (BIT) & POWER-UP HARDWARE INTEGRITY DIAGNOSTIC                             *)
    (* ------------------------------------------------------------------------------------------------------------ *)
    0: (* STATE_00_PREFLIGHT_BIT_DIAG *)
        wFADEC_OperatingState := 16#0000;
        bStarterAirValve_Open     := FALSE;
        bIgniterA_Fire            := FALSE;
        bIgniterB_Fire            := FALSE;
        bOverspeedShutoff_Trip    := FALSE;
        bThrustReverser_DeployCmd := FALSE;
        rFMV_TorqueMotorCmd_mA    := -40.0; (* Drive FMV fully to mechanical shutoff stop *)
        rVSV_ActuatorDemand_deg   := -15.0; (* Park VSV closed *)
        rVBV_ActuatorDemand_pct   := 85.0;  (* Park VBV open *)
        rHPTACC_ValveDemand_pct   := 0.0;
        rLPTACC_ValveDemand_pct   := 0.0;

        (* Perform Built-In-Test qualification timer *)
        IF rStateTimer_s > 3.0 THEN
            IF bChannelA_HealthOK AND (NOT bFireHandleCutoff) THEN
                IF bMasterEngineStartSwitch THEN
                    iFSM_State := 1; (* Proceed to Starter Engagement *)
                    rStateTimer_s := 0.0;
                    bStateFirstCycle := TRUE;
                ELSIF bCrankMotoringSelector THEN
                    iFSM_State := 2; (* Dry Motoring Crank *)
                    rStateTimer_s := 0.0;
                    bStateFirstCycle := TRUE;
                END_IF;
            END_IF;
        END_IF;

    (* ------------------------------------------------------------------------------------------------------------ *)
    (* STATE 1: PNEUMATIC AIR TURBINE STARTER (ATS) VALVE ENGAGEMENT                                                *)
    (* ------------------------------------------------------------------------------------------------------------ *)
    1: (* STATE_01_ATS_PNEUMATIC_ENGAGE *)
        wFADEC_OperatingState := 16#0001;
        bStarterAirValve_Open := TRUE; (* Energize ATS starter valve solenoid *)
        bIgniterA_Fire        := FALSE;
        bIgniterB_Fire        := FALSE;
        rFMV_TorqueMotorCmd_mA:= -40.0;

        (* Monitor starter pneumatic supply pressure and initial rotor acceleration *)
        IF (rStarterAirPress_psia > 22.0) AND (rN2_Voted_RPM > 250.0) THEN
            iFSM_State := 2; (* Advance to Dry Motoring Crank *)
            rStateTimer_s := 0.0;
            bStateFirstCycle := TRUE;
        ELSIF rStateTimer_s > 12.0 THEN
            (* Starter failure to crank: Abort to safe shutdown *)
            iFSM_State := 12;
            rStateTimer_s := 0.0;
        END_IF;

    (* ------------------------------------------------------------------------------------------------------------ *)
    (* STATE 2: DRY MOTORING FAN & CORE ROTATION CRANK                                                              *)
    (* ------------------------------------------------------------------------------------------------------------ *)
    2: (* STATE_02_DRY_MOTORING_CRANK *)
        wFADEC_OperatingState := 16#0002;
        bStarterAirValve_Open := TRUE;
        bIgniterA_Fire        := FALSE;
        bIgniterB_Fire        := FALSE;
        rFMV_TorqueMotorCmd_mA:= -40.0;
        rVBV_ActuatorDemand_pct := 85.0;

        (* Check engine lubrication oil pressure buildup and crank speed *)
        IF (rN2_Pct >= 20.0) AND (rOilPressure_psid >= 24.0) THEN
            IF bCrankMotoringSelector AND NOT bMasterEngineStartSwitch THEN
                (* Remain in dry motoring indefinitely per flight crew selector *)
                IF rStateTimer_s > 120.0 THEN
                    iFSM_State := 12; (* Starter duty cycle thermal limit reached *)
                    rStateTimer_s := 0.0;
                END_IF;
            ELSIF bMasterEngineStartSwitch THEN
                iFSM_State := 3; (* Proceed to Fuel Light-Off & Ignition *)
                rStateTimer_s := 0.0;
                bStateFirstCycle := TRUE;
            END_IF;
        ELSIF rStateTimer_s > 35.0 THEN
            (* Hung dry crank or inadequate oil pressure *)
            iFSM_State := 12;
            rStateTimer_s := 0.0;
        END_IF;

    (* ------------------------------------------------------------------------------------------------------------ *)
    (* STATE 3: FUEL METERING & DUAL HIGH-ENERGY SPARK IGNITION (LIGHT-OFF)                                         *)
    (* ------------------------------------------------------------------------------------------------------------ *)
    3: (* STATE_03_FUEL_LIGHTOFF_IGNITION *)
        wFADEC_OperatingState := 16#0003;
        bStarterAirValve_Open := TRUE;
        bIgniterA_Fire        := TRUE;  (* Energize dual ignition channel A *)
        bIgniterB_Fire        := TRUE;  (* Energize dual ignition channel B *)
        
        (* Open FMV to calibrated light-off flow (approx 850 pph) *)
        rFMV_TorqueMotorCmd_mA := 4.50;

        (* Detect Combustor Light-Off: EGT rate of rise > 10.0 deg C/s and EGT > 220 deg C *)
        IF (rEGT_RateOfRise_degCs > 10.0) AND (rEGT_Voted_Average_degC > 220.0) THEN
            bLightoffDetected := TRUE;
            iFSM_State := 4; (* Light-off established: Proceed to Ground Idle Stabilize *)
            rStateTimer_s := 0.0;
            bStateFirstCycle := TRUE;
        ELSIF rStateTimer_s > 20.0 THEN
            (* Wet start abort: Failed to light off within 20 seconds *)
            iFSM_State := 12;
            rStateTimer_s := 0.0;
        END_IF;

    (* ------------------------------------------------------------------------------------------------------------ *)
    (* STATE 4: GROUND IDLE SPEED STABILIZATION & STARTER CUTOUT                                                     *)
    (* ------------------------------------------------------------------------------------------------------------ *)
    4: (* STATE_04_GROUND_IDLE_STABILIZE *)
        wFADEC_OperatingState := 16#0004;

        (* Starter Cutout Threshold: N2 >= 52.0% *)
        IF rN2_Pct >= 52.0 THEN
            bStarterAirValve_Open := FALSE; (* De-energize ATS starter air valve *)
            bStarterCutoutComplete := TRUE;
        ELSE
            bStarterAirValve_Open := TRUE;
        END_IF;

        (* De-energize ignition above starter cutout *)
        IF rN2_Pct >= 55.0 THEN
            bIgniterA_Fire := FALSE;
            bIgniterB_Fire := FALSE;
        END_IF;

        (* Ground Idle Governor: Stabilize N2 around 62.5% and N1 around 21.5% *)
        IF (rN2_Pct >= 61.0) AND (rN2_Pct <= 65.0) AND (rStateTimer_s > 10.0) THEN
            iFSM_State := 5; (* Advance to Taxi Thrust Management *)
            rStateTimer_s := 0.0;
            bStateFirstCycle := TRUE;
        ELSIF rStateTimer_s > 60.0 THEN
            (* Hung start: Core speed failed to reach stabilized ground idle *)
            iFSM_State := 12;
            rStateTimer_s := 0.0;
        END_IF;

    (* ------------------------------------------------------------------------------------------------------------ *)
    (* STATE 5: TAXI THRUST MANAGEMENT & GROUND ROLL GOVERNING                                                      *)
    (* ------------------------------------------------------------------------------------------------------------ *)
    5: (* STATE_05_TAXI_THRUST_GOVERN *)
        wFADEC_OperatingState := 16#0005;
        bStarterAirValve_Open := FALSE;
        bIgniterA_Fire        := FALSE;
        bIgniterB_Fire        := FALSE;
        rHPTACC_ValveDemand_pct := 0.0;
        rLPTACC_ValveDemand_pct := 0.0;

        (* Detect Takeoff Throttle Advance: TLA > 32.0 deg while on ground *)
        IF (rThrottleLeverAngle_deg >= 32.0) AND bWeightOnWheels THEN
            iFSM_State := 6; (* Advance to Takeoff Thrust Ramp *)
            rStateTimer_s := 0.0;
            bStateFirstCycle := TRUE;
        ELSIF NOT bMasterEngineStartSwitch THEN
            iFSM_State := 12; (* Normal cockpit fuel shutdown *)
            rStateTimer_s := 0.0;
        END_IF;

    (* ------------------------------------------------------------------------------------------------------------ *)
    (* STATE 6: TAKEOFF RATED 110,000 LBF THRUST RAMP                                                               *)
    (* ------------------------------------------------------------------------------------------------------------ *)
    6: (* STATE_06_TAKEOFF_RATED_RAMP_110KLBF *)
        wFADEC_OperatingState := 16#0006;
        bStarterAirValve_Open := FALSE;
        bIgniterA_Fire        := FALSE;
        bIgniterB_Fire        := FALSE;
        rVBV_ActuatorDemand_pct := 0.0; (* VBV fully closed *)
        rHPTACC_ValveDemand_pct := 0.0; (* ACC disabled during takeoff to prevent pinch *)
        rLPTACC_ValveDemand_pct := 0.0;

        (* Monitor 110,000 lbf rated thrust achievement *)
        IF rCalculatedNetThrust_lbf >= 108000.0 THEN
            bTakeoffThrustReached := TRUE;
        END_IF;

        (* Transition to Climb Thrust Pacing upon Liftoff (Weight on Wheels = FALSE) *)
        IF NOT bWeightOnWheels AND (rStateTimer_s > 8.0) THEN
            iFSM_State := 7; (* Advance to Climb Thrust Pacing *)
            rStateTimer_s := 0.0;
            bStateFirstCycle := TRUE;
        ELSIF rThrottleLeverAngle_deg < 25.0 THEN
            (* Rejected Takeoff (RTO): Throttle retarded *)
            iFSM_State := 5;
            rStateTimer_s := 0.0;
        END_IF;

    (* ------------------------------------------------------------------------------------------------------------ *)
    (* STATE 7: CLIMB THRUST PACING & ALTITUDE LAPSE COMPENSATION                                                   *)
    (* ------------------------------------------------------------------------------------------------------------ *)
    7: (* STATE_07_CLIMB_THRUST_PACING *)
        wFADEC_OperatingState := 16#0007;
        bStarterAirValve_Open := FALSE;
        bIgniterA_Fire        := FALSE;
        bIgniterB_Fire        := FALSE;

        (* Transition to Cruise Active Clearance Control Optimization above 28,000 ft *)
        IF (rAltitude_ft >= 28000.0) AND (rMachNumber >= 0.72) THEN
            iFSM_State := 8; (* Advance to Cruise ACC Optimization *)
            rStateTimer_s := 0.0;
            bStateFirstCycle := TRUE;
        ELSIF (rThrottleLeverAngle_deg <= 5.0) AND NOT bWeightOnWheels THEN
            iFSM_State := 9; (* Flight Idle Descent *)
            rStateTimer_s := 0.0;
        END_IF;

    (* ------------------------------------------------------------------------------------------------------------ *)
    (* STATE 8: CRUISE ACTIVE CLEARANCE CONTROL (HPTACC/LPTACC) OPTIMIZATION                                        *)
    (* ------------------------------------------------------------------------------------------------------------ *)
    8: (* STATE_08_CRUISE_ACC_OPTIMIZE *)
        wFADEC_OperatingState := 16#0008;
        bStarterAirValve_Open := FALSE;
        bIgniterA_Fire        := FALSE;
        bIgniterB_Fire        := FALSE;

        (* In-Flight Flameout Detection Surveillance *)
        IF (rEGT_RateOfRise_degCs < -45.0) AND (rN2_Pct < 58.0) AND (rThrottleLeverAngle_deg > 10.0) THEN
            bInFlightFlameoutDetected := TRUE;
            iFSM_State := 11; (* Emergency In-Flight Flameout Auto-Relight *)
            rStateTimer_s := 0.0;
            bStateFirstCycle := TRUE;
        ELSIF (rThrottleLeverAngle_deg <= 5.0) AND NOT bWeightOnWheels THEN
            iFSM_State := 9; (* Flight Idle Descent *)
            rStateTimer_s := 0.0;
        END_IF;

    (* ------------------------------------------------------------------------------------------------------------ *)
    (* STATE 9: FLIGHT IDLE DESCENT & VBV SURGE BLEED REGULATION                                                    *)
    (* ------------------------------------------------------------------------------------------------------------ *)
    9: (* STATE_09_FLIGHT_IDLE_DESCENT_BLEED *)
        wFADEC_OperatingState := 16#0009;
        bStarterAirValve_Open := FALSE;
        bIgniterA_Fire        := FALSE;
        bIgniterB_Fire        := FALSE;
        rHPTACC_ValveDemand_pct := 0.0;
        rLPTACC_ValveDemand_pct := 0.0;

        (* Touchdown & Reverse Thrust Deployment *)
        IF bWeightOnWheels THEN
            IF bThrustReverserArmed AND (rThrottleLeverAngle_deg < 0.0) THEN
                iFSM_State := 10; (* Deploy Thrust Reverser *)
                rStateTimer_s := 0.0;
                bStateFirstCycle := TRUE;
            ELSE
                iFSM_State := 5;  (* Transition to Taxi Rollout *)
                rStateTimer_s := 0.0;
            END_IF;
        ELSIF rThrottleLeverAngle_deg > 18.0 THEN
            (* Pilot Go-Around or Level-Off *)
            iFSM_State := 7;
            rStateTimer_s := 0.0;
        END_IF;

    (* ------------------------------------------------------------------------------------------------------------ *)
    (* STATE 10: THRUST REVERSER HYDRAULIC DEPLOYMENT                                                               *)
    (* ------------------------------------------------------------------------------------------------------------ *)
    10: (* STATE_10_THRUST_REVERSER_DEPLOY *)
        wFADEC_OperatingState := 16#000A;
        bThrustReverser_DeployCmd := TRUE; (* Hydraulically translate blocker cowls aft *)
        bStarterAirValve_Open     := FALSE;
        bIgniterA_Fire            := FALSE;
        bIgniterB_Fire            := FALSE;
        rHPTACC_ValveDemand_pct   := 0.0;
        rLPTACC_ValveDemand_pct   := 0.0;

        (* Stow Reverser when speed drops below 60 knots or pilot stows levers *)
        IF (rThrottleLeverAngle_deg >= 0.0) OR (rStateTimer_s > 25.0) THEN
            bThrustReverser_DeployCmd := FALSE;
            iFSM_State := 5; (* Return to Taxi *)
            rStateTimer_s := 0.0;
        END_IF;

    (* ------------------------------------------------------------------------------------------------------------ *)
    (* STATE 11: EMERGENCY IN-FLIGHT FLAMEOUT AUTO-RELIGHT & RAPID FUEL ENRICHMENT                                  *)
    (* ------------------------------------------------------------------------------------------------------------ *)
    11: (* STATE_11_EMERGENCY_FLAMEOUT_AUTORELIGHT *)
        wFADEC_OperatingState := 16#000B;
        bIgniterA_Fire := TRUE; (* Immediate continuous dual spark excitation *)
        bIgniterB_Fire := TRUE;
        bThrustReverser_DeployCmd := FALSE;
        rHPTACC_ValveDemand_pct := 0.0;
        rLPTACC_ValveDemand_pct := 0.0;

        (* If rotor speed has dropped below windmilling relight envelope (N2 < 18%), assist with starter *)
        IF rN2_Pct < 18.0 THEN
            bStarterAirValve_Open := TRUE;
        ELSE
            bStarterAirValve_Open := FALSE;
        END_IF;

        (* Meter enriched relight fuel flow (approx 1,200 pph) *)
        rFMV_TorqueMotorCmd_mA := 6.80;

        (* Confirm Flame Recovery: EGT recovery and N2 accelerating through 55% *)
        IF (rEGT_RateOfRise_degCs > 12.0) AND (rN2_Pct > 55.0) THEN
            bInFlightFlameoutDetected := FALSE;
            iRelightAttempts := 0;
            iFSM_State := 8; (* Relight successful: Return to Cruise/Flight Idle *)
            rStateTimer_s := 0.0;
            bStateFirstCycle := TRUE;
        ELSIF rStateTimer_s > 25.0 THEN
            (* Relight attempt timed out *)
            iRelightAttempts := iRelightAttempts + 1;
            IF iRelightAttempts < 3 THEN
                rStateTimer_s := 0.0; (* Retry auto-relight pulse *)
            ELSE
                iFSM_State := 12;     (* Multiple relight attempts exhausted: Secure engine *)
                rStateTimer_s := 0.0;
            END_IF;
        END_IF;

    (* ------------------------------------------------------------------------------------------------------------ *)
    (* STATE 12: SAFE FUEL CUTOFF & POST-SHUTDOWN THERMAL SOAK COOLDOWN                                             *)
    (* ------------------------------------------------------------------------------------------------------------ *)
    12: (* STATE_12_SAFE_FUEL_SHUTDOWN *)
        wFADEC_OperatingState := 16#000C;
        bStarterAirValve_Open     := FALSE;
        bIgniterA_Fire            := FALSE;
        bIgniterB_Fire            := FALSE;
        bThrustReverser_DeployCmd := FALSE;
        rFMV_TorqueMotorCmd_mA    := -40.0; (* Hard shutoff stop *)
        rVSV_ActuatorDemand_deg   := -15.0;
        rVBV_ActuatorDemand_pct   := 85.0;
        rHPTACC_ValveDemand_pct   := 0.0;
        rLPTACC_ValveDemand_pct   := 0.0;

        (* Trip overspeed shutoff valve if trip condition was latched *)
        IF bOverspeedShutoff_Latch OR bEGT_Redline_Latch OR bFireHandleCutoff THEN
            bOverspeedShutoff_Trip := TRUE;
        ELSE
            bOverspeedShutoff_Trip := FALSE;
        END_IF;

        (* Allow restart when engine has completely spooled down below 5% N2 *)
        IF (rN2_Pct < 5.0) AND bMasterEngineStartSwitch AND (NOT bFireHandleCutoff) THEN
            bOverspeedShutoff_Trip := FALSE;
            bOverspeedShutoff_Latch := FALSE;
            bEGT_Redline_Latch := FALSE;
            iFSM_State := 0; (* Reset to Pre-Flight BIT *)
            rStateTimer_s := 0.0;
        END_IF;

END_CASE;
""")

    # 8. PHASE 6: ISA-18.2 / DO-178C Multi-Tiered Alarms & ARINC-429 Broadcast Words
    code_lines.append("""
(* ================================================================================================================ *)
(* PHASE 6: ISA-18.2 / DO-178C MULTI-TIERED ALARM MATRIX & ARINC-429 TELEMETRY PACKING                               *)
(* ================================================================================================================ *)
dwTripBits := 16#00000000;
dwSev1Bits := 16#00000000;
dwSev2Bits := 16#00000000;

(* ---------------------------------------------------------------------------------------------------------------- *)
(* PRIORITY 1: EMERGENCY ENGINE TRIPS (Immediate Fuel Cutoff / Overspeed Solenoid Actuation)                        *)
(* ---------------------------------------------------------------------------------------------------------------- *)
(* Bit 0: High-Pressure Rotor N2 Overspeed Trip (HH > 105.0% = 11,340 RPM) *)
IF rN2_Voted_RPM >= 11340.0 THEN
    bOverspeedShutoff_Latch := TRUE;
    dwTripBits := dwTripBits OR 16#00000001;
END_IF;

(* Bit 1: Low-Pressure Rotor N1 Overspeed Trip (HH > 106.0% = 3,021 RPM) *)
IF rN1_Voted_RPM >= 3021.0 THEN
    bOverspeedShutoff_Latch := TRUE;
    dwTripBits := dwTripBits OR 16#00000002;
END_IF;

(* Bit 2: Turbine Gas Temperature EGT Redline Breach (HH > 1040.0 deg C) *)
IF rEGT_Peak_degC >= 1040.0 THEN
    bEGT_Redline_Latch := TRUE;
    dwTripBits := dwTripBits OR 16#00000004;
END_IF;

(* Bit 3: Cockpit Fire Handle Fuel Cutoff Pulled *)
IF bFireHandleCutoff THEN
    dwTripBits := dwTripBits OR 16#00000008;
END_IF;

(* Bit 4: Severe Aerodynamic Compressor Stall / Surge Uncontained Event *)
IF bStallSurgeDetected AND (rStateTimer_s > 1.5) THEN
    bSurgeStall_Latch := TRUE;
    dwTripBits := dwTripBits OR 16#00000010;
END_IF;

(* Execute Emergency Trip Transition *)
IF (dwTripBits <> 16#00000000) AND (iFSM_State <> 12) THEN
    iFSM_State := 12; (* Safe fuel cutoff *)
    rStateTimer_s := 0.0;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------- *)
(* PRIORITY 2: CRITICAL OPERATING ALARMS (Severity 1 Warnings Requiring Immediate Flight Crew Action)                *)
(* ---------------------------------------------------------------------------------------------------------------- *)
(* Bit 0: EGT Thermal Caution High (H > 980.0 deg C) *)
IF rEGT_Peak_degC >= 980.0 THEN
    rTimer_EGT_HighAlarm_s := rTimer_EGT_HighAlarm_s + rDt_sec;
    IF rTimer_EGT_HighAlarm_s > 2.0 THEN
        dwSev1Bits := dwSev1Bits OR 16#00000001;
    END_IF;
ELSE
    rTimer_EGT_HighAlarm_s := 0.0;
END_IF;

(* Bit 1: Engine Lubrication Oil Pressure Low (L < 25.0 psid while core N2 > 50%) *)
IF (rOilPressure_psid < 25.0) AND (rN2_Pct > 50.0) THEN
    rTimer_OilPressureLow_s := rTimer_OilPressureLow_s + rDt_sec;
    IF rTimer_OilPressureLow_s > 3.0 THEN
        dwSev1Bits := dwSev1Bits OR 16#00000002;
    END_IF;
ELSE
    rTimer_OilPressureLow_s := 0.0;
END_IF;

(* Bit 2: Total N1 Rotor Speed Sensor Failure *)
IF bN1_TotalFailure THEN
    dwSev1Bits := dwSev1Bits OR 16#00000004;
END_IF;

(* Bit 3: Total N2 Rotor Speed Sensor Failure *)
IF bN2_TotalFailure THEN
    dwSev1Bits := dwSev1Bits OR 16#00000008;
END_IF;

(* Bit 4: Total Ps3 Compressor Pressure Sensor Failure *)
IF bPs3_TotalFailure THEN
    dwSev1Bits := dwSev1Bits OR 16#00000010;
END_IF;

(* Bit 5: Cross-Channel Data Link (CCDL) Lost *)
IF bCCDL_LinkLost THEN
    dwSev1Bits := dwSev1Bits OR 16#00000020;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------- *)
(* PRIORITY 3: ADVISORY / MAINTENANCE ALERTS (Severity 2 Maintenance Flags)                                         *)
(* ---------------------------------------------------------------------------------------------------------------- *)
(* Bit 0: Fuel Filter Impending Bypass Differential Pressure (DeltaP > 22.0 psid) *)
IF rFuelFilterDeltaP_psid >= 22.0 THEN
    rTimer_FilterBypass_s := rTimer_FilterBypass_s + rDt_sec;
    IF rTimer_FilterBypass_s > 5.0 THEN
        dwSev2Bits := dwSev2Bits OR 16#00000001;
    END_IF;
ELSE
    rTimer_FilterBypass_s := 0.0;
END_IF;

(* Bit 1: Engine Scavenge Oil Temperature High (> 145.0 deg C) *)
IF rOilTemp_degC >= 145.0 THEN
    dwSev2Bits := dwSev2Bits OR 16#00000002;
END_IF;

(* Bit 2: N1 Sensor Discrepancy (Degraded to 1oo2 mode) *)
IF bN1_Degraded_1oo2 THEN
    dwSev2Bits := dwSev2Bits OR 16#00000004;
END_IF;

(* Bit 3: N2 Sensor Discrepancy (Degraded to 1oo2 mode) *)
IF bN2_Degraded_1oo2 THEN
    dwSev2Bits := dwSev2Bits OR 16#00000008;
END_IF;

(* Bit 4: Ps3 Sensor Discrepancy (Degraded to 1oo2 mode) *)
IF bPs3_Degraded_1oo2 THEN
    dwSev2Bits := dwSev2Bits OR 16#00000010;
END_IF;

(* Bit 5: FMV Dual LVDT Coil Discrepancy *)
IF bFMV_LVDT_Discrepancy THEN
    dwSev2Bits := dwSev2Bits OR 16#00000020;
END_IF;

(* Bit 6: HPT Active Clearance Control Tracking Error > 0.15 mm *)
IF ABS(rClearanceError_HPT_mm) > 0.15 THEN
    dwSev2Bits := dwSev2Bits OR 16#00000040;
END_IF;

(* Bit 7: Circumferential EGT Spread Excessive (> 110.0 deg C) *)
IF rEGT_Spread_degC > 110.0 THEN
    dwSev2Bits := dwSev2Bits OR 16#00000080;
END_IF;

(* Bit 8: Starter Air Duct Pressure Low (< 22.0 psia during start) *)
IF (iFSM_State = 1) AND (rStarterAirPress_psia < 22.0) THEN
    dwSev2Bits := dwSev2Bits OR 16#00000100;
END_IF;

(* Assign Consolidated Diagnostic Output DWORDs *)
dwISA18_Alarms_Trips     := dwTripBits;
dwISA18_Alarms_Severity1 := dwSev1Bits;
dwISA18_Alarms_Severity2 := dwSev2Bits;

(* Pack Comprehensive Channel Health Status Words *)
IF bChannelA_HealthOK THEN
    dwChannelHealthStatus_ChA := 16#80000000 OR (INT_TO_DWORD(iFSM_State) AND 16#0000000F);
ELSE
    dwChannelHealthStatus_ChA := 16#40000000;
END_IF;

IF bChannelB_HealthOK THEN
    dwChannelHealthStatus_ChB := 16#80000000 OR (WORD_TO_DWORD(wCCDL_RxWord_ChB_Status) AND 16#0000FFFF);
ELSE
    dwChannelHealthStatus_ChB := 16#40000000;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------- *)
(* SUB-MODULE 6.1: ARINC-429 PROPULSION TELEMETRY 32-BIT BROADCAST WORD ENCODING                                    *)
(* Encodes Sign/Status Matrix (SSM), BNR Data Fields, and Calculates Odd Parity Bit (Bit 32)                         *)
(* ---------------------------------------------------------------------------------------------------------------- *)
(* Telemetry Word 1: N1 Shaft Speed (Label 240 Octal = 16#A0) *)
dwRawWord := 16#000000A0; (* Label 240 *)
dwRawWord := dwRawWord OR SHL((REAL_TO_DWORD(rN1_Voted_RPM * 8.0) AND 16#0007FFFF), 8); (* 19 bits BNR data *)
dwRawWord := dwRawWord OR 16#60000000; (* SSM = 11 (Normal Operation) *)
(* Compute ARINC-429 Odd Parity across 32 bits *)
iParityCount := 0;
FOR i := 0 TO 30 DO
    IF (dwRawWord AND SHL(16#00000001, i)) <> 16#00000000 THEN
        iParityCount := iParityCount + 1;
    END_IF;
END_FOR;
IF (iParityCount MOD 2) = 0 THEN
    dwRawWord := dwRawWord OR 16#80000000; (* Insert Odd Parity bit *)
END_IF;
wARINC429_TelemetryWord1 := DWORD_TO_WORD(dwRawWord);

(* Telemetry Word 2: N2 Core Speed (Label 241 Octal = 16#A1) *)
dwRawWord := 16#000000A1;
dwRawWord := dwRawWord OR SHL((REAL_TO_DWORD(rN2_Voted_RPM * 2.0) AND 16#0007FFFF), 8);
dwRawWord := dwRawWord OR 16#60000000;
iParityCount := 0;
FOR i := 0 TO 30 DO
    IF (dwRawWord AND SHL(16#00000001, i)) <> 16#00000000 THEN
        iParityCount := iParityCount + 1;
    END_IF;
END_FOR;
IF (iParityCount MOD 2) = 0 THEN
    dwRawWord := dwRawWord OR 16#80000000;
END_IF;
wARINC429_TelemetryWord2 := DWORD_TO_WORD(dwRawWord);

(* Telemetry Word 3: Exhaust Gas Temperature EGT (Label 242 Octal = 16#A2) *)
dwRawWord := 16#000000A2;
dwRawWord := dwRawWord OR SHL((REAL_TO_DWORD(rEGT_Peak_degC * 16.0) AND 16#0007FFFF), 8);
dwRawWord := dwRawWord OR 16#60000000;
iParityCount := 0;
FOR i := 0 TO 30 DO
    IF (dwRawWord AND SHL(16#00000001, i)) <> 16#00000000 THEN
        iParityCount := iParityCount + 1;
    END_IF;
END_FOR;
IF (iParityCount MOD 2) = 0 THEN
    dwRawWord := dwRawWord OR 16#80000000;
END_IF;
wARINC429_TelemetryWord3 := DWORD_TO_WORD(dwRawWord);

(* Telemetry Word 4: Calibrated Mass Fuel Flow Rate Wf (Label 243 Octal = 16#A3) *)
dwRawWord := 16#000000A3;
dwRawWord := dwRawWord OR SHL((REAL_TO_DWORD(rActiveFuelFlow_pph * 0.5) AND 16#0007FFFF), 8);
dwRawWord := dwRawWord OR 16#60000000;
iParityCount := 0;
FOR i := 0 TO 30 DO
    IF (dwRawWord AND SHL(16#00000001, i)) <> 16#00000000 THEN
        iParityCount := iParityCount + 1;
    END_IF;
END_FOR;
IF (iParityCount MOD 2) = 0 THEN
    dwRawWord := dwRawWord OR 16#80000000;
END_IF;
wARINC429_TelemetryWord4 := DWORD_TO_WORD(dwRawWord);

END_FUNCTION_BLOCK
""")

    return "".join(code_lines)

if __name__ == "__main__":
    code = generate_full_fadec_code()
    print("Generated ST code length:", len(code), "characters")
    print("Generated ST lines count:", len(code.splitlines()))
    with open("test_output.st", "w", encoding="utf-8") as f:
        f.write(code)
    print("Saved test_output.st")
