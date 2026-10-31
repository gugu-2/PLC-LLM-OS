import json
import os
import sys

def build_iec_st():
    parts = []
    
    # Header
    parts.append("""FUNCTION_BLOCK FB_Aerospace_Turbofan_DualChannelFADEC_110klbf
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
""")
    return "".join(parts)

print("Builder initialized")
