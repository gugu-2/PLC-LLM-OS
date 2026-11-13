# build_bess_dataset.py
import os
import sys
import uuid
import json
import re

def generate_iec_st():
    parts = []
    
    # Header
    parts.append("""FUNCTION_BLOCK FB_Power_BESS_GridForming_VirtualSynchronousGenerator_Thermal
(*
====================================================================================================
LUMINA CYBER-PHYSICAL AUTOMATION KERNEL - IEC 61131-3 STRUCTURED TEXT
DOMAIN: RENEWABLE ENERGY & POWER GRID / UTILITY-SCALE ENERGY STORAGE
SYSTEM: 100 MW / 400 MWh BESS WITH GRID-FORMING VIRTUAL SYNCHRONOUS MACHINE & ACTIVE THERMAL LOOP
ARCHITECTURAL OVERVIEW:
  - 100 MW / 120 MVA GRID-FORMING (GFM) 4-QUADRANT CENTRAL INVERTER ARRAYS (34.5 kV INTERCONNECTION)
  - VIRTUAL SYNCHRONOUS GENERATOR (VSG) 2ND-ORDER ROTOR SWING EQUATION & TRANSIENT FLUX EMULATION
  - SUB-20 ms HIGH-SPEED SYNTHETIC INERTIAL RESPONSE & DYNAMIC RoCoF (df/dt) POWER INJECTION
  - P-f ACTIVE POWER FREQUENCY DROOP & Q-V VOLTAGE REACTIVE SUPPORT DROOP COMPENSATION ENGINES
  - 1,500 V DC CENTRAL BUS PRECHARGE, VACUUM CONTACTOR AUTOMATION & GROUND FAULT INSULATION MONITORING
  - 4-STRING BATTERY RACK ACTIVE STATE-OF-CHARGE (SoC) EQUALIZATION VIA MODULATED DC-DC CURRENT TRIMS
  - CLOSED-LOOP REFRIGERATION CHILLER SKID WITH VARIABLE COMPRESSOR VFD & STRING COOLING VALVES
  - MULTI-STAGE OFF-GAS ELECTROCHEMICAL DETECTION (H2, CO, AEROSOL) & NFPA 855 COMPLIANT FIRE DELUGE
  - 12-STATE DISCRETE FIRST-PRINCIPLES CYBER-PHYSICAL STATE-SPACE DYNAMICS WITH LUENBERGER OBSERVER
  - RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) WITH 10 UNROLLED PROJECTED GRADIENT DESCENT ITERATIONS
  - 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING ACROSS 4 CRITICAL MEASUREMENT CHANNELS
  - DETERMINISTIC 14-STAGE PRODUCTION FINITE STATE MACHINE (FSM, STATES 0 TO 13)
  - ISA-18.2 MULTI-TIER PROCESS ALARM MATRIX (HH, H, L, LL) WITH 32-BIT BIT-PACKED TELEMETRY DWORDS
====================================================================================================
*)

VAR_INPUT
    (* Master Plant Automation Permissives & Operator Commands *)
    bEnable                         : BOOL;         (* Master Automation Execution Enable Command [-] *)
    bAutoDispatchStart              : BOOL;         (* Automatic 100 MW BESS Sequence Start Command [-] *)
    bControlledStop                 : BOOL;         (* Controlled Plant Ramp-down and Standby Request [-] *)
    bEmergencyStop                  : BOOL;         (* Safety Cat-4 Emergency Hardwired Master Trip [-] *)
    bFaultReset                     : BOOL;         (* Process Fault and Latched Safety Trip Reset [-] *)
    bAlarmAck                       : BOOL;         (* ISA-18.2 Process Alarm Acknowledge and Silence [-] *)
    bBlackStartPermissive           : BOOL;         (* Black Start Islanded Microgrid Energization Permissive [-] *)
    bGridSynchronizeCmd             : BOOL;         (* PCC Grid Synchronization Automatic Closure Initiate [-] *)
    bChillerSkidReady               : BOOL;         (* Central Chiller Refrigeration Skid Ready Permissive [-] *)
    bFireSuppressionDelugeArmed     : BOOL;         (* Clean Agent / Novec / Water Mist Deluge Armed Feedback [-] *)
    bInverterHeartbeatOk            : BOOL;         (* Inverter Power Conversion System DSP High-Speed Watchdog [-] *)
    bManualTrimOverride             : BOOL;         (* Battery DC-DC String Current Trim Manual Override [-] *)

    (* Channel Group 1: PCC 3-Phase RMS Grid Voltage Transducers (2oo3 TMR) *)
    rPCC_Voltage_1A_kV              : REAL;         (* PCC 3-Phase RMS Grid Voltage Channel 1A [kV] *)
    rPCC_Voltage_1B_kV              : REAL;         (* PCC 3-Phase RMS Grid Voltage Channel 1B [kV] *)
    rPCC_Voltage_1C_kV              : REAL;         (* PCC 3-Phase RMS Grid Voltage Channel 1C [kV] *)

    (* Channel Group 2: PCC Utility Grid Frequency Measurement Units / PMUs (2oo3 TMR) *)
    rPCC_Frequency_2A_Hz            : REAL;         (* PCC Utility Grid Frequency Channel 2A [Hz] *)
    rPCC_Frequency_2B_Hz            : REAL;         (* PCC Utility Grid Frequency Channel 2B [Hz] *)
    rPCC_Frequency_2C_Hz            : REAL;         (* PCC Utility Grid Frequency Channel 2C [Hz] *)

    (* Channel Group 3: BESS Central DC Link Bus Voltage Transducers (2oo3 TMR) *)
    rDCLink_Voltage_3A_V            : REAL;         (* Central Inverter DC Link Bus Voltage Channel 3A [V] *)
    rDCLink_Voltage_3B_V            : REAL;         (* Central Inverter DC Link Bus Voltage Channel 3B [V] *)
    rDCLink_Voltage_3C_V            : REAL;         (* Central Inverter DC Link Bus Voltage Channel 3C [V] *)

    (* Channel Group 4: Battery Rack Off-Gas Multi-Gas Sensing Sensors (2oo3 TMR) *)
    rOffGas_H2_CO_4A_ppm            : REAL;         (* Battery Off-Gas Multi-Gas Sensor Channel 4A [ppm] *)
    rOffGas_H2_CO_4B_ppm            : REAL;         (* Battery Off-Gas Multi-Gas Sensor Channel 4B [ppm] *)
    rOffGas_H2_CO_4C_ppm            : REAL;         (* Battery Off-Gas Multi-Gas Sensor Channel 4C [ppm] *)

    (* Battery Rack String Electrical & State Feedback *)
    rBattery_TotalCurrent_A         : REAL;         (* Total Aggregated Battery String DC Current (+Disch/-Chg) [A] *)
    rBattery_String1_Current_A      : REAL;         (* Battery Rack String 1 DC Current Feedback [A] *)
    rBattery_String2_Current_A      : REAL;         (* Battery Rack String 2 DC Current Feedback [A] *)
    rBattery_String3_Current_A      : REAL;         (* Battery Rack String 3 DC Current Feedback [A] *)
    rBattery_String4_Current_A      : REAL;         (* Battery Rack String 4 DC Current Feedback [A] *)
    rBattery_String1_SoC_pct        : REAL;         (* Battery Rack String 1 State-of-Charge [%] *)
    rBattery_String2_SoC_pct        : REAL;         (* Battery Rack String 2 State-of-Charge [%] *)
    rBattery_String3_SoC_pct        : REAL;         (* Battery Rack String 3 State-of-Charge [%] *)
    rBattery_String4_SoC_pct        : REAL;         (* Battery Rack String 4 State-of-Charge [%] *)
    rBattery_CellMaxTemp_degC       : REAL;         (* Maximum Module Core Cell Thermocouple Temperature [deg C] *)
    rBattery_CellMinTemp_degC       : REAL;         (* Minimum Module Core Cell Thermocouple Temperature [deg C] *)
    rBattery_CellMaxVoltage_V       : REAL;         (* Maximum Single Cell Electrochemical Potential [V] *)
    rBattery_CellMinVoltage_V       : REAL;         (* Minimum Single Cell Electrochemical Potential [V] *)
    rInsulation_Resistance_kOhm     : REAL;         (* DC Bus Insulation Resistance to Earth Ground [kOhm] *)

    (* Utility Grid Dispatch Schedule & Baseline Setpoints *)
    rDispatch_ActivePower_MW        : REAL;         (* Remote TSO/ISO Active Power Dispatch Schedule Target [MW] *)
    rDispatch_ReactivePower_MVAr    : REAL;         (* Remote TSO/ISO Reactive Power Dispatch Schedule Target [MVAr] *)
    rGrid_NominalVoltage_kV         : REAL;         (* Point of Common Coupling Nominal Base Line Voltage [kV] *)
    rGrid_NominalFrequency_Hz       : REAL;         (* Utility Interconnection Nominal Base System Frequency [Hz] *)

    (* Chiller Skid & Liquid Glycol Hydraulic Feedback *)
    rGlycol_SupplyTemp_degC         : REAL;         (* Chiller Evaporator Coolant Supply Temperature [deg C] *)
    rGlycol_ReturnTemp_degC         : REAL;         (* BESS Container Return Coolant Collector Temperature [deg C] *)
    rGlycol_CoolantFlow_m3h         : REAL;         (* Liquid Glycol Coolant Volumetric Circulation Rate [m3/h] *)
    rGlycol_ManifoldPressure_bar    : REAL;         (* Closed-Loop Liquid Glycol Hydraulic Supply Pressure [bar] *)
    rAmbient_AirTemp_degC           : REAL;         (* Container External Meteorological Ambient Temperature [deg C] *)
    rChiller_CompressorPower_kW     : REAL;         (* Central Refrigeration Compressor Skid Electrical Power [kW] *)
    rInverter_IGBT_MaxTemp_degC     : REAL;         (* Inverter Phase Leg IGBT Junction Maximum Temperature [deg C] *)

    (* Switchgear & Contactor Digital Feedback *)
    bAC_MainBreaker_ClosedFb        : BOOL;         (* PCC 34.5 kV Medium-Voltage Vacuum Breaker Status [-] *)
    bDC_MainContactor_ClosedFb      : BOOL;         (* 1500 V DC Main Contactor Closed Feedback Contact [-] *)
    bDC_PrechargeContactor_ClosedFb : BOOL;         (* DC Bus Soft-Start Precharge Contactor Closed Contact [-] *)
    bEarthSwitch_OpenFb             : BOOL;         (* 1500 V DC Disconnect Manual Grounding Earth Switch Open [-] *)
END_VAR

VAR_OUTPUT
    (* Virtual Synchronous Generator (VSG) & Inverter Commands *)
    rVSG_VirtualPowerCmd_P_MW       : REAL;         (* Virtual Mechanical Shaft Power Command P_m [MW] *)
    rVSG_VirtualVoltageCmd_E_kV     : REAL;         (* Virtual Excitation Voltage Field Command E_v [kV] *)
    rVSG_RotorAngle_delta_rad       : REAL;         (* Virtual Rotor Power Angle Delta [rad] *)
    rVSG_RotorSpeed_omega_rads      : REAL;         (* Virtual Rotor Angular Velocity Omega_vsg [rad/s] *)
    rVSG_SyntheticInertiaPower_MW   : REAL;         (* Sub-20 ms Synthetic Inertial Power Injection [MW] *)
    rVSG_FrequencyDroopPower_MW     : REAL;         (* Primary Frequency P-f Droop Regulation Response [MW] *)
    rVSG_VoltageDroopReactive_MVAr  : REAL;         (* Reactive Voltage Q-V Droop Regulation Response [MVAr] *)
    rPCC_ActivePower_Actual_MW      : REAL;         (* Realized Net PCC Active Power Generation/Absorption [MW] *)
    rPCC_ReactivePower_Actual_MVAr  : REAL;         (* Realized Net PCC Reactive Power Injection/Absorption [MVAr] *)

    (* Battery String Balancing Trims & Contactor Actuation *)
    rString1_CurrentTrimCmd_A       : REAL;         (* DC-DC Converter String 1 Balancing Current Trim [A] *)
    rString2_CurrentTrimCmd_A       : REAL;         (* DC-DC Converter String 2 Balancing Current Trim [A] *)
    rString3_CurrentTrimCmd_A       : REAL;         (* DC-DC Converter String 3 Balancing Current Trim [A] *)
    rString4_CurrentTrimCmd_A       : REAL;         (* DC-DC Converter String 4 Balancing Current Trim [A] *)
    bDC_PrechargeContactor_Cmd      : BOOL;         (* 1500 V DC Precharge Resistor Inrush Contactor Coil [-] *)
    bDC_MainContactor_Cmd           : BOOL;         (* 1500 V DC Main Vacuum Circuit Contactor Coil Command [-] *)
    bAC_MainBreaker_TripCmd         : BOOL;         (* PCC 34.5 kV Vacuum Interrupter Emergency Shunt Trip [-] *)
    bAC_MainBreaker_CloseCmd        : BOOL;         (* PCC 34.5 kV Synchronous Breaker Closing Pulse Command [-] *)

    (* Central Thermal Management & Chiller Commands *)
    rChiller_CompressorVFD_RPM      : REAL;         (* Central Chiller Refrigeration Compressor Speed Setpoint [RPM] *)
    rGlycol_CirculationPump_pct     : REAL;         (* Coolant Distribution Variable Frequency Pump Command [%] *)
    rCoolingValve_String1_pct       : REAL;         (* Proportional Thermal Cooling Valve Rack String 1 Opening [%] *)
    rCoolingValve_String2_pct       : REAL;         (* Proportional Thermal Cooling Valve Rack String 2 Opening [%] *)
    rCoolingValve_String3_pct       : REAL;         (* Proportional Thermal Cooling Valve Rack String 3 Opening [%] *)
    rCoolingValve_String4_pct       : REAL;         (* Proportional Thermal Cooling Valve Rack String 4 Opening [%] *)
    rInverter_CoolingFan_pct        : REAL;         (* Inverter Power Stage Forced Air Cooling Fan VFD Command [%] *)

    (* Fire Deluge & Container Isolation Actuators *)
    bFireSuppressionReleaseValve    : BOOL;         (* Clean Agent / Novec / Water Mist Deluge Discharge Solenoid [-] *)
    bBatteryRoomVentLouversOpen     : BOOL;         (* Deflagration Blast Relief Pressure Louver Actuator Open [-] *)
    bHVAC_EmergencyShutoff_Trip     : BOOL;         (* HVAC Fresh Air Damper Rapid Isolation Solenoid [-] *)

    (* First-Principles Cyber-Physical Observer Estimated States *)
    rEst_VirtualRotorAngle_rad      : REAL;         (* Luenberger Observer Estimated Virtual Rotor Angle [rad] *)
    rEst_VirtualRotorSpeed_rads     : REAL;         (* Luenberger Observer Estimated Virtual Angular Speed [rad/s] *)
    rEst_PCC_ActivePower_MW         : REAL;         (* Observer Filtered PCC Net Active Power Output [MW] *)
    rEst_PCC_ReactivePower_MVAr     : REAL;         (* Observer Filtered PCC Net Reactive Power Output [MVAr] *)
    rEst_BulkBatterySoC_pct         : REAL;         (* Coulomb-Counting & OCV Filtered Bulk String SoC [%] *)
    rEst_PolarizationOverpotential_V: REAL;         (* Equivalent Circuit Diffusion Polarization Voltage [V] *)
    rEst_MaxCellTemp_degC           : REAL;         (* Observer Core Cell Junction Maximum Temperature [deg C] *)
    rEst_ThermalGradient_degC       : REAL;         (* Observer Estimated Inter-Rack Thermal Gradient Delta_T [deg C] *)
    rEst_ThermalAbsorption_kW       : REAL;         (* Observer Estimated Coolant Loop Heat Absorption Rate [kW] *)
    rEst_ChillerSupplyTemp_degC     : REAL;         (* Observer Estimated Chiller Supply Evaporator Temperature [deg C] *)
    rEst_DCLinkVoltage_V            : REAL;         (* Observer Filtered Central Inverter DC Link Voltage [V] *)
    rEst_DCHarmonicRipple_A         : REAL;         (* Observer Estimated DC Current High-Frequency Ripple [A] *)

    (* Performance Telemetry & Diagnostic Status Words *)
    rMpc_ObjectiveCostMetric        : REAL;         (* Receding-Horizon MPC Quadratic Cost Objective Function [-] *)
    rGrid_RoCoF_Hz_per_s            : REAL;         (* Instantaneous Rate-of-Change-of-Frequency (RoCoF) [Hz/s] *)
    iActiveStateIndex               : INT;          (* Deterministic Production Finite State Machine State [0..13] *)
    dwStatusWord1                   : DWORD;        (* BESS Operational Subsystem & Inverter State Bits [-] *)
    dwStatusWord2                   : DWORD;        (* 2oo3 TMR Channel Health & Grid Synchronization Status Bits [-] *)
    dwAlarmWord1                    : DWORD;        (* ISA-18.2 Critical Trips & Safety Interlocks (HH/LL) [-] *)
    dwAlarmWord2                    : DWORD;        (* ISA-18.2 Operational Warnings & Sensor Discrepancies (H/L) [-] *)
    dwFirstOutWord                  : DWORD;        (* Root Cause First-Out Latching Telemetry Code [-] *)
END_VAR

VAR
    (* Execution Control & Initialization Flags *)
    bFirstScanDone                  : BOOL := FALSE;    (* First Scan Initialization Completed Flag [-] *)
    tScanCycleTime_s                : REAL := 0.010;    (* Discrete Task Execution Sample Period (10 ms) [s] *)
    iCycleCounter                   : DINT := 0;        (* Rolling Scan Execution Cycle Counter [-] *)

    (* Discrete State-Space Cyber-Physical Matrices (12 States x 8 Inputs) *)
    matA                            : ARRAY[0..11, 0..11] OF REAL; (* Discrete System Transition Matrix A (12x12) [-] *)
    matB                            : ARRAY[0..11, 0..7] OF REAL;  (* Input Distribution Matrix B (12x8) [-] *)
    matC                            : ARRAY[0..7, 0..11] OF REAL;  (* Measurement Output Matrix C (8x12) [-] *)
    matD                            : ARRAY[0..7, 0..7] OF REAL;   (* Direct Feedthrough Matrix D (8x8) [-] *)
    matL                            : ARRAY[0..11, 0..7] OF REAL;  (* Luenberger Observer Innovation Gain L (12x8) [-] *)

    (* State Vectors & Estimation Buffers *)
    vecX                            : ARRAY[0..11] OF REAL; (* Cyber-Physical Plant True/Predicted State Vector [-] *)
    vecX_hat                        : ARRAY[0..11] OF REAL; (* Luenberger Filtered State Estimate Vector [-] *)
    vecX_pred                       : ARRAY[0..11] OF REAL; (* One-Step-Ahead Observer State Prediction Vector [-] *)
    vecY_meas                       : ARRAY[0..7] OF REAL;  (* Voted Sensor Measurement Vector [-] *)
    vecY_hat                        : ARRAY[0..7] OF REAL;  (* Observer Estimated Measurement Vector [-] *)
    vecInnov                        : ARRAY[0..7] OF REAL;  (* Innovation Estimation Residual Vector (y - y_hat) [-] *)
    vecU                            : ARRAY[0..7] OF REAL;  (* Current Optimal Actuator Command Vector [-] *)
    vecU_prev                       : ARRAY[0..7] OF REAL;  (* Previous Execution Cycle Actuator Command Vector [-] *)
    vecU_rate                       : ARRAY[0..7] OF REAL;  (* Instantaneous Actuator Slew Rate Vector [%/s] *)
    vecX_target                     : ARRAY[0..11] OF REAL; (* Target State Reference Equilibrium Vector [-] *)
    vecU_target                     : ARRAY[0..7] OF REAL;  (* Actuator Nominal Steady-State Setpoint Vector [-] *)

    (* Model Predictive Control (MPC) Cost Weighting & Sizing Arrays *)
    vecQ_weight                     : ARRAY[0..11] OF REAL; (* Quadratic State Tracking Penalty Diagonal Weights [-] *)
    vecR_weight                     : ARRAY[0..7] OF REAL;  (* Actuator Effort Penalty Diagonal Weights [-] *)
    vecR_delta_weight               : ARRAY[0..7] OF REAL;  (* Actuator Slew Rate-of-Change Penalty Weights [-] *)
    vecP_terminal                   : ARRAY[0..11] OF REAL; (* Terminal Horizon State Penalty Diagonal Weights [-] *)
    vecU_min                        : ARRAY[0..7] OF REAL;  (* Actuator Absolute Physical Lower Saturation Bounds [-] *)
    vecU_max                        : ARRAY[0..7] OF REAL;  (* Actuator Absolute Physical Upper Saturation Bounds [-] *)
    vecU_slewMax                    : ARRAY[0..7] OF REAL;  (* Actuator Maximum Slew Rate Limit Per Execution Cycle [-] *)

    (* Receding-Horizon Prediction & Gradient Descent Workspace (Horizon N=5, Iterations=10) *)
    trajX_mpc                       : ARRAY[0..5, 0..11] OF REAL; (* MPC State Trajectory Over Horizon N=5 [-] *)
    trajU_mpc                       : ARRAY[0..4, 0..7] OF REAL;  (* MPC Control Trajectory Over Horizon N=5 [-] *)
    trajU_cand                      : ARRAY[0..4, 0..7] OF REAL;  (* PGD Candidate Actuator Update Trajectory [-] *)
    trajGrad_J                      : ARRAY[0..4, 0..7] OF REAL;  (* Analytical Gradient Vector of Cost w.r.t U [-] *)
    rPgd_StepSize                   : REAL := 0.025;    (* Projected Gradient Descent Learning Step Size Gamma [-] *)
    rMpc_AccumulatedCost            : REAL := 0.0;      (* Unrolled MPC Quadratic Objective Cost Function Value [-] *)

    (* 2oo3 Triple Modular Redundancy (TMR) Sensor Channels *)
    (* Channel Group 1: PCC 3-Phase RMS Grid Voltage *)
    rPCC_Voltage_Voted              : REAL := 34.5;     (* 2oo3 Voted PCC 3-Phase RMS Grid Voltage [kV] *)
    bPCC_Voltage_HealthA            : BOOL := TRUE;     (* Channel 1A Voltage Transducer Healthy [-] *)
    bPCC_Voltage_HealthB            : BOOL := TRUE;     (* Channel 1B Voltage Transducer Healthy [-] *)
    bPCC_Voltage_HealthC            : BOOL := TRUE;     (* Channel 1C Voltage Transducer Healthy [-] *)
    rPCC_Voltage_Disc_AB_ms         : REAL := 0.0;      (* Channel 1A vs 1B Discrepancy Timer [ms] *)
    rPCC_Voltage_Disc_BC_ms         : REAL := 0.0;      (* Channel 1B vs 1C Discrepancy Timer [ms] *)
    rPCC_Voltage_Disc_CA_ms         : REAL := 0.0;      (* Channel 1C vs 1A Discrepancy Timer [ms] *)
    bPCC_Voltage_Degraded           : BOOL := FALSE;    (* Voltage Operating on Degraded 2oo2 Voting [-] *)
    bPCC_Voltage_SingleFallback     : BOOL := FALSE;    (* Voltage Operating on Single Channel [-] *)
    bPCC_Voltage_Trip               : BOOL := FALSE;    (* Voltage Transducer Complete Failure Trip [-] *)

    (* Channel Group 2: PCC Utility Grid Frequency *)
    rPCC_Frequency_Voted            : REAL := 50.0;     (* 2oo3 Voted PCC Grid Frequency [Hz] *)
    bPCC_Frequency_HealthA          : BOOL := TRUE;     (* Channel 2A Frequency PMU Sensor Healthy [-] *)
    bPCC_Frequency_HealthB          : BOOL := TRUE;     (* Channel 2B Frequency PMU Sensor Healthy [-] *)
    bPCC_Frequency_HealthC          : BOOL := TRUE;     (* Channel 2C Frequency PMU Sensor Healthy [-] *)
    rPCC_Frequency_Disc_AB_ms       : REAL := 0.0;      (* Channel 2A vs 2B Discrepancy Timer [ms] *)
    rPCC_Frequency_Disc_BC_ms       : REAL := 0.0;      (* Channel 2B vs 2C Discrepancy Timer [ms] *)
    rPCC_Frequency_Disc_CA_ms       : REAL := 0.0;      (* Channel 2C vs 2A Discrepancy Timer [ms] *)
    bPCC_Frequency_Degraded         : BOOL := FALSE;    (* Frequency Operating on Degraded 2oo2 Voting [-] *)
    bPCC_Frequency_SingleFallback   : BOOL := FALSE;    (* Frequency Operating on Single Channel [-] *)
    bPCC_Frequency_Trip             : BOOL := FALSE;    (* Frequency Sensor Complete Failure Trip [-] *)

    (* Channel Group 3: BESS Central DC Link Bus Voltage *)
    rDCLink_Voltage_Voted           : REAL := 1500.0;   (* 2oo3 Voted DC Link Bus Voltage [V] *)
    bDCLink_Voltage_HealthA         : BOOL := TRUE;     (* Channel 3A DC Voltage Transducer Healthy [-] *)
    bDCLink_Voltage_HealthB         : BOOL := TRUE;     (* Channel 3B DC Voltage Transducer Healthy [-] *)
    bDCLink_Voltage_HealthC         : BOOL := TRUE;     (* Channel 3C DC Voltage Transducer Healthy [-] *)
    rDCLink_Voltage_Disc_AB_ms      : REAL := 0.0;      (* Channel 3A vs 3B Discrepancy Timer [ms] *)
    rDCLink_Voltage_Disc_BC_ms      : REAL := 0.0;      (* Channel 3B vs 3C Discrepancy Timer [ms] *)
    rDCLink_Voltage_Disc_CA_ms      : REAL := 0.0;      (* Channel 3C vs 3A Discrepancy Timer [ms] *)
    bDCLink_Voltage_Degraded        : BOOL := FALSE;    (* DC Link Operating on Degraded 2oo2 Voting [-] *)
    bDCLink_Voltage_SingleFallback  : BOOL := FALSE;    (* DC Link Operating on Single Channel [-] *)
    bDCLink_Voltage_Trip            : BOOL := FALSE;    (* DC Link Transducer Complete Failure Trip [-] *)

    (* Channel Group 4: Battery Rack Off-Gas Multi-Gas Sensing *)
    rOffGas_H2_CO_Voted             : REAL := 0.0;      (* 2oo3 Voted Off-Gas Concentration [ppm] *)
    bOffGas_HealthA                 : BOOL := TRUE;     (* Channel 4A Off-Gas Sensor Healthy [-] *)
    bOffGas_HealthB                 : BOOL := TRUE;     (* Channel 4B Off-Gas Sensor Healthy [-] *)
    bOffGas_HealthC                 : BOOL := TRUE;     (* Channel 4C Off-Gas Sensor Healthy [-] *)
    rOffGas_Disc_AB_ms              : REAL := 0.0;      (* Channel 4A vs 4B Discrepancy Timer [ms] *)
    rOffGas_Disc_BC_ms              : REAL := 0.0;      (* Channel 4B vs 4C Discrepancy Timer [ms] *)
    rOffGas_Disc_CA_ms              : REAL := 0.0;      (* Channel 4C vs 4A Discrepancy Timer [ms] *)
    bOffGas_Degraded                : BOOL := FALSE;    (* Off-Gas Operating on Degraded 2oo2 Voting [-] *)
    bOffGas_SingleFallback          : BOOL := FALSE;    (* Off-Gas Operating on Single Channel [-] *)
    bOffGas_Trip                    : BOOL := FALSE;    (* Off-Gas Sensor Complete Failure Trip [-] *)

    (* Virtual Synchronous Generator Physical & Electrical Parameters *)
    rVSG_Inertia_J_kgm2             : REAL := 25000.0;  (* Virtual Synchronous Machine Moment of Inertia J [kg*m^2] *)
    rVSG_DampingFactor_Dp           : REAL := 42.0;     (* Virtual Damping Power Coefficient D_p [MW*s/rad] *)
    rVSG_Droop_Pf_pct               : REAL := 3.0;      (* P-f Active Power Frequency Droop Percentage [%] *)
    rVSG_Droop_Qv_pct               : REAL := 4.0;      (* Q-V Reactive Power Voltage Droop Percentage [%] *)
    rVSG_TransientReactance_Xdp     : REAL := 0.22;     (* Direct-Axis Transient Reactance X_d' [p.u.] *)
    rVSG_SynchronousReactance_Xd    : REAL := 1.15;     (* Direct-Axis Synchronous Reactance X_d [p.u.] *)
    rVSG_TransientTimeConst_Tdp     : REAL := 1.85;     (* Direct-Axis Transient Open-Circuit Time Constant T_d0' [s] *)
    rVSG_NominalOmega_rads          : REAL := 314.159265; (* Nominal Angular Frequency Omega_0 (2*pi*50) [rad/s] *)
    rVSG_RotorAngle_delta           : REAL := 0.0;      (* Instantaneous Virtual Rotor Angle Delta [rad] *)
    rVSG_RotorSpeed_omega           : REAL := 314.159265; (* Instantaneous Virtual Rotor Angular Speed [rad/s] *)
    rVSG_VirtualEMF_E               : REAL := 34.5;     (* Virtual Internal Excitation Back-EMF Voltage E_v [kV] *)
    rVSG_FilteredRoCoF              : REAL := 0.0;      (* Low-Pass Filtered Grid Frequency Rate-of-Change [Hz/s] *)
    rPrev_PCC_Frequency             : REAL := 50.0;     (* Previous Execution Cycle Grid Frequency [Hz] *)

    (* Battery Equivalent Circuit Model (ECM) & String Balancing *)
    rBulk_SoC_Filtered              : REAL := 65.0;     (* Coulomb-Counted Weighted Bulk Battery State of Charge [%] *)
    rString_SoC_Mean                : REAL := 65.0;     (* Arithmetic Mean of 4 Battery String SoCs [%] *)
    rString1_SoC_Dev                : REAL := 0.0;      (* String 1 SoC Deviation from String Mean [%] *)
    rString2_SoC_Dev                : REAL := 0.0;      (* String 2 SoC Deviation from String Mean [%] *)
    rString3_SoC_Dev                : REAL := 0.0;      (* String 3 SoC Deviation from String Mean [%] *)
    rString4_SoC_Dev                : REAL := 0.0;      (* String 4 SoC Deviation from String Mean [%] *)
    rBalancingGain_A_per_pct        : REAL := 12.5;     (* Active Balancing Trim Gain Factor [A/%] *)
    rBattery_ECM_R0_Ohm             : REAL := 0.0125;   (* High-Frequency Ohmic Internal Resistance R0 [Ohm] *)
    rBattery_ECM_R1_Ohm             : REAL := 0.0085;   (* Charge-Transfer Polarization Resistance R1 [Ohm] *)
    rBattery_ECM_C1_Farad           : REAL := 4500.0;   (* Double-Layer Electrochemical Capacitance C1 [F] *)
    rBattery_PolarizationOverpot    : REAL := 0.0;      (* Overpotential Voltage Drop Across RC Pair [V] *)

    (* Thermal Hydraulics & Refrigeration Parameters *)
    rGlycol_SpecificHeat_kJ_kgK     : REAL := 3.42;     (* 50/50 Water-Glycol Mixture Specific Heat Capacity [kJ/(kg*K)] *)
    rGlycol_Density_kg_m3           : REAL := 1065.0;   (* Water-Glycol Mixture Fluid Density [kg/m^3] *)
    rThermal_HeatAbsorption_kW      : REAL := 0.0;      (* Real-Time Liquid Coolant Thermal Extraction Power [kW] *)
    rThermal_RackGradient_DeltaT    : REAL := 0.0;      (* Maximum Difference in Cell Core Temperatures [deg C] *)
    rChiller_TargetSupplyTemp_degC  : REAL := 18.0;     (* Dynamic Chiller Temperature Setpoint [deg C] *)
    rChiller_PID_Integral           : REAL := 0.0;      (* Chiller Compressor Speed Closed-Loop Integral Error [-] *)
    rChiller_PID_PrevError          : REAL := 0.0;      (* Chiller Closed-Loop Error Previous Cycle [-] *)

    (* Deterministic 14-Stage Production Finite State Machine (FSM) Engine *)
    eState                          : INT := 0;         (* Active Operational State Index [0..13] *)
    ePrevState                      : INT := 0;         (* Previous Cycle Operational State Index [0..13] *)
    rStateTimer_s                   : REAL := 0.0;      (* Dwell Time Elapsed in Active State [s] *)
    rSubStateTimer_s                : REAL := 0.0;      (* Auxiliary Internal Sub-State Dwell Timer [s] *)
    iFsmStepIndex                   : INT := 0;         (* Sequential Step Index Within Active State [-] *)
    bPrechargeComplete              : BOOL := FALSE;    (* DC Bus Precharge Soft-Start Voltage Matched Flag [-] *)
    bSyncCriteriaMet                : BOOL := FALSE;    (* Voltage, Phase Angle & Frequency Synchronized Flag [-] *)
    rSyncAngleDiff_deg              : REAL := 0.0;      (* Phase Angle Displacement Across Open AC Breaker [deg] *)
    rSyncVoltageDiff_kV             : REAL := 0.0;      (* Voltage Magnitude Difference Across Open AC Breaker [kV] *)
    rSyncFreqDiff_Hz                : REAL := 0.0;      (* Frequency Slip Difference Across Open AC Breaker [Hz] *)
    rLVRT_SagDepth_pct              : REAL := 0.0;      (* Low-Voltage Ride-Through Sag Depth Below Nominal [%] *)
    rLVRT_ReactiveBoost_MVAr        : REAL := 0.0;      (* Dynamic Fast Reactive Current Injection Under Sag [MVAr] *)
    rThermalRunawaySeverity         : REAL := 0.0;      (* Multi-Sensor Combined Thermal Runaway Risk Index [-] *)
    bThermalRunawayLatched          : BOOL := FALSE;    (* Irreversible Catastrophic Thermal Runaway Latched [-] *)

    (* ISA-18.2 Multi-Tier Process Alarm Limits & Deadbands *)
    (* PCC Grid Voltage Alarms *)
    rPCC_Volt_HH_Limit_kV           : REAL := 39.675;   (* PCC Overvoltage Trip (+15%) [kV] *)
    rPCC_Volt_H_Limit_kV            : REAL := 36.225;   (* PCC High Voltage Advisory (+5%) [kV] *)
    rPCC_Volt_L_Limit_kV            : REAL := 32.775;   (* PCC Low Voltage Advisory (-5%) [kV] *)
    rPCC_Volt_LL_Limit_kV           : REAL := 29.325;   (* PCC Undervoltage Trip (-15%) [kV] *)
    rPCC_Volt_Deadband_kV           : REAL := 0.345;    (* PCC Voltage Alarm Clearance Hysteresis [kV] *)

    (* PCC Grid Frequency Alarms *)
    rPCC_Freq_HH_Limit_Hz           : REAL := 52.0;     (* Grid Extreme High Frequency Trip [Hz] *)
    rPCC_Freq_H_Limit_Hz            : REAL := 50.5;     (* Grid High Frequency Advisory [Hz] *)
    rPCC_Freq_L_Limit_Hz            : REAL := 49.5;     (* Grid Low Frequency Advisory [Hz] *)
    rPCC_Freq_LL_Limit_Hz           : REAL := 47.5;     (* Grid Extreme Low Frequency Trip [Hz] *)
    rPCC_Freq_Deadband_Hz           : REAL := 0.05;     (* Frequency Alarm Clearance Hysteresis [Hz] *)

    (* DC Link Voltage Alarms *)
    rDCLink_Volt_HH_Limit_V         : REAL := 1580.0;   (* DC Link Overvoltage Catastrophic Trip [V] *)
    rDCLink_Volt_H_Limit_V          : REAL := 1540.0;   (* DC Link High Voltage Warning [V] *)
    rDCLink_Volt_L_Limit_V          : REAL := 1350.0;   (* DC Link Low Voltage Warning [V] *)
    rDCLink_Volt_LL_Limit_V         : REAL := 1250.0;   (* DC Link Undervoltage Trip [V] *)
    rDCLink_Volt_Deadband_V         : REAL := 10.0;     (* DC Voltage Alarm Clearance Hysteresis [V] *)

    (* Battery Module Core Cell Temperature Alarms *)
    rCellTemp_HH_Limit_degC         : REAL := 55.0;     (* Cell Core Critical Thermal Runaway Trip [deg C] *)
    rCellTemp_H_Limit_degC          : REAL := 42.0;     (* Cell Core High Temperature Boost Warning [deg C] *)
    rCellTemp_L_Limit_degC          : REAL := 12.0;     (* Cell Core Low Temperature Inhibit Charge [deg C] *)
    rCellTemp_LL_Limit_degC         : REAL := 0.0;      (* Cell Core Freezing Inhibit Operation [deg C] *)
    rCellTemp_Deadband_degC         : REAL := 1.5;      (* Cell Temperature Clearance Hysteresis [deg C] *)

    (* Inter-Rack Thermal Gradient Alarms *)
    rGradient_HH_Limit_degC         : REAL := 8.0;      (* Inter-Rack Severe Thermal Imbalance Trip [deg C] *)
    rGradient_H_Limit_degC          : REAL := 4.5;      (* Inter-Rack Elevated Gradient Advisory [deg C] *)
    rGradient_Deadband_degC         : REAL := 0.5;      (* Thermal Gradient Alarm Clearance Hysteresis [deg C] *)

    (* Battery Off-Gas Multi-Gas Sensing Alarms *)
    rOffGas_HH_Limit_ppm            : REAL := 50.0;     (* Off-Gas Critical Deluge Discharge Trip [ppm] *)
    rOffGas_H_Limit_ppm             : REAL := 20.0;     (* Off-Gas Vent Isolation Warning [ppm] *)
    rOffGas_Deadband_ppm            : REAL := 2.0;      (* Off-Gas Clearance Hysteresis [ppm] *)

    (* DC Ground Insulation Resistance Alarms *)
    rInsul_L_Limit_kOhm             : REAL := 500.0;    (* Ground Fault Early Warning [kOhm] *)
    rInsul_LL_Limit_kOhm            : REAL := 100.0;    (* Ground Fault Critical Isolation Trip [kOhm] *)
    rInsul_Deadband_kOhm            : REAL := 25.0;     (* Insulation Resistance Alarm Hysteresis [kOhm] *)

    (* Liquid Glycol Coolant Flow Alarms *)
    rFlow_L_Limit_m3h               : REAL := 45.0;     (* Coolant Circulation Flow Loss Warning [m3/h] *)
    rFlow_LL_Limit_m3h              : REAL := 25.0;     (* Coolant Hydraulic Failure Chiller Trip [m3/h] *)
    rFlow_Deadband_m3h              : REAL := 3.0;      (* Coolant Flow Alarm Clearance Hysteresis [m3/h] *)

    (* Inverter Phase Leg IGBT Junction Temperature Alarms *)
    rIGBT_Temp_HH_Limit_degC        : REAL := 115.0;    (* Inverter IGBT Junction Over-Temp Trip [deg C] *)
    rIGBT_Temp_H_Limit_degC         : REAL := 95.0;     (* Inverter IGBT Elevated Temp Fan Boost [deg C] *)
    rIGBT_Temp_Deadband_degC        : REAL := 3.0;      (* Inverter IGBT Temp Clearance Hysteresis [deg C] *)

    (* Active Alarm State Boolean Latch Flags *)
    bPCC_Volt_HH_Active             : BOOL := FALSE;
    bPCC_Volt_H_Active              : BOOL := FALSE;
    bPCC_Volt_L_Active              : BOOL := FALSE;
    bPCC_Volt_LL_Active             : BOOL := FALSE;
    bPCC_Freq_HH_Active             : BOOL := FALSE;
    bPCC_Freq_H_Active              : BOOL := FALSE;
    bPCC_Freq_L_Active              : BOOL := FALSE;
    bPCC_Freq_LL_Active             : BOOL := FALSE;
    bDCLink_Volt_HH_Active          : BOOL := FALSE;
    bDCLink_Volt_H_Active           : BOOL := FALSE;
    bDCLink_Volt_L_Active           : BOOL := FALSE;
    bDCLink_Volt_LL_Active          : BOOL := FALSE;
    rCellTemp_HH_Active             : BOOL := FALSE;
    rCellTemp_H_Active              : BOOL := FALSE;
    rCellTemp_L_Active              : BOOL := FALSE;
    rCellTemp_LL_Active             : BOOL := FALSE;
    rGradient_HH_Active             : BOOL := FALSE;
    rGradient_H_Active              : BOOL := FALSE;
    rOffGas_HH_Active               : BOOL := FALSE;
    rOffGas_H_Active                : BOOL := FALSE;
    rInsul_L_Active                 : BOOL := FALSE;
    rInsul_LL_Active                : BOOL := FALSE;
    rFlow_L_Active                  : BOOL := FALSE;
    rFlow_LL_Active                 : BOOL := FALSE;
    rIGBT_Temp_HH_Active            : BOOL := FALSE;
    rIGBT_Temp_H_Active             : BOOL := FALSE;

    (* First-Out Latching Internal Logic *)
    bFirstOutLatched                : BOOL := FALSE;    (* First-Out Root Cause Latched Flag [-] *)
    dwFirstOutCapturedCode          : DWORD := 16#00000000; (* Captured Initial Fault Root Cause Code [-] *)

    (* Loop Counters & Auxiliary Real Workspace *)
    iIdx                            : INT := 0;         (* Primary State Index Counter [-] *)
    jIdx                            : INT := 0;         (* Inner Matrix Column Counter [-] *)
    mIdx                            : INT := 0;         (* Actuator Dimension Loop Counter [-] *)
    kStep                           : INT := 0;         (* MPC Horizon Time Step Counter [-] *)
    iIter                           : INT := 0;         (* PGD Optimization Iteration Counter [-] *)
    rTempSum                        : REAL := 0.0;      (* Inner Dot Product Matrix Multiply Accumulator [-] *)
    rTempDiff                       : REAL := 0.0;      (* Scalar Difference Intermediate Real [-] *)
    rTempCandidate                  : REAL := 0.0;      (* Actuator Gradient Candidate Value [-] *)
    rTempMaxDev                     : REAL := 0.0;      (* Maximum State Vector Deviation Diagnostic [-] *)
    rTempGrad                       : REAL := 0.0;      (* Instantaneous Analytical Cost Gradient [-] *)
    rTempRate                       : REAL := 0.0;      (* Actuator Slew Rate Check Intermediate [-] *)
END_VAR
""")

    # PHASE 0: State-Space Initialization
    parts.append("""
(* ==================================================================================================== *)
(* PHASE 0: FIRST-SCAN STATE-SPACE MATRICES & MPC WEIGHTS INITIALIZATION                                 *)
(* Discretization Sample Time Ts = 0.010 [s] (10 [ms] deterministic scan cycle)                         *)
(* State Vector x (12x1):                                                                               *)
(*   x[0] : Virtual Rotor Angle delta [rad]                                                             *)
(*   x[1] : Virtual Rotor Angular Speed omega_vsg [rad/s]                                               *)
(*   x[2] : Grid PCC Active Power P_grid [MW]                                                           *)
(*   x[3] : Grid PCC Reactive Power Q_grid [MVAr]                                                       *)
(*   x[4] : Battery String Bulk State-of-Charge SoC [%]                                                 *)
(*   x[5] : Battery Equivalent Circuit Polarization Overpotential eta_p [V]                            *)
(*   x[6] : Maximum Battery Module Core Cell Temperature T_max [deg C]                                 *)
(*   x[7] : Inter-Rack Thermal Gradient Delta_T [deg C]                                                 *)
(*   x[8] : Liquid Glycol Cooling Loop Thermal Absorption Rate Q_cool [kW]                             *)
(*   x[9] : Chiller Evaporator Supply Coolant Temperature T_chiller [deg C]                             *)
(*   x[10]: BESS DC Bus Central Inverter Voltage V_dc [V]                                               *)
(*   x[11]: DC Current High-Frequency Harmonic Ripple I_ripple [A]                                      *)
(* Actuator Vector u (8x1):                                                                             *)
(*   u[0] : Virtual Mechanical Power Setpoint P_m [MW]                                                  *)
(*   u[1] : Virtual Excitation Voltage Field Command E_v [kV]                                           *)
(*   u[2] : Battery String 1 DC-DC Current Trim I_trim_1 [A]                                            *)
(*   u[3] : Battery String 2 DC-DC Current Trim I_trim_2 [A]                                            *)
(*   u[4] : Battery String 3 DC-DC Current Trim I_trim_3 [A]                                            *)
(*   u[5] : Battery String 4 DC-DC Current Trim I_trim_4 [A]                                            *)
(*   u[6] : Chiller Refrigeration Compressor VFD Speed N_comp [RPM]                                     *)
(*   u[7] : Proportional Glycol Distribution Valves Collective Command V_glycol [%]                     *)
(* ==================================================================================================== *)
IF NOT bFirstScanDone THEN
""")

    # Explicit Matrix A initialization (12x12)
    # Generate realistic coupling coefficients for grid forming VSG + BESS + Thermal
    matA_vals = [
        # x0 (delta)
        [1.0000, 0.0100, -0.0001, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
        # x1 (omega_vsg)
        [-0.0450, 0.9850, -0.0125, -0.0015, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0002, 0.0000],
        # x2 (P_grid)
        [0.1850, 0.0620, 0.9250, -0.0180, 0.0012, -0.0045, -0.0010, 0.0000, 0.0000, 0.0000, 0.0450, -0.0020],
        # x3 (Q_grid)
        [-0.0120, -0.0080, 0.0150, 0.9320, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0280, 0.0015],
        # x4 (SoC)
        [0.0000, 0.0000, -0.00025, 0.0000, 1.0000, 0.00001, -0.00002, 0.0000, 0.0000, 0.0000, 0.00001, 0.0000],
        # x5 (eta_p)
        [0.0000, 0.0000, 0.0018, 0.0000, 0.0000, 0.8950, 0.0008, 0.0000, 0.0000, 0.0000, -0.0005, 0.0002],
        # x6 (T_max)
        [0.0000, 0.0000, 0.0035, 0.0008, 0.0000, 0.0012, 0.9920, 0.0040, -0.0085, 0.0030, -0.0002, 0.0005],
        # x7 (Delta_T)
        [0.0000, 0.0000, 0.0015, 0.0004, 0.0000, 0.0005, 0.0085, 0.9850, -0.0042, 0.0015, 0.0000, 0.0002],
        # x8 (Q_cool)
        [0.0000, 0.0000, 0.0080, 0.0020, 0.0000, 0.0000, 0.0450, 0.0180, 0.9150, -0.0650, 0.0000, 0.0000],
        # x9 (T_chiller)
        [0.0000, 0.0000, 0.0012, 0.0000, 0.0000, 0.0000, 0.0025, 0.0010, 0.0085, 0.9750, 0.0000, 0.0000],
        # x10 (V_dc)
        [-0.0150, -0.0080, -0.1250, -0.0350, 0.0850, -0.0450, -0.0120, -0.0050, 0.0000, 0.0000, 0.9450, -0.0180],
        # x11 (I_ripple)
        [0.0000, 0.0000, 0.0450, 0.0280, 0.0000, 0.0015, 0.0080, 0.0020, 0.0000, 0.0000, -0.0320, 0.8850]
    ]

    for i in range(12):
        for j in range(12):
            parts.append(f"    matA[{i}, {j}] := {matA_vals[i][j]:.4f};\n")

    parts.append("\n    (* 12x8 Input Distribution Matrix B *)\n")
    matB_vals = [
        # u0 (P_m), u1 (E_v), u2 (I_tr1), u3 (I_tr2), u4 (I_tr3), u5 (I_tr4), u6 (N_comp), u7 (V_glycol)
        [0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
        [0.0125, -0.0012, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
        [0.0850, 0.0180, 0.0042, 0.0042, 0.0042, 0.0042, 0.0000, 0.0000],
        [-0.0085, 0.1250, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
        [-0.00018, 0.0000, -0.00005, -0.00005, -0.00005, -0.00005, 0.0000, 0.0000],
        [0.0015, 0.0000, 0.0008, 0.0008, 0.0008, 0.0008, 0.0000, 0.0000],
        [0.0025, 0.0005, 0.0003, 0.0003, 0.0003, 0.0003, -0.0015, -0.0035],
        [0.0008, 0.0000, 0.0012, -0.0004, -0.0004, -0.0004, -0.0005, -0.0018],
        [0.0050, 0.0010, 0.0000, 0.0000, 0.0000, 0.0000, 0.0450, 0.0850],
        [0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, -0.0085, -0.0025],
        [-0.0650, -0.0150, 0.0180, 0.0180, 0.0180, 0.0180, 0.0000, 0.0000],
        [0.0350, 0.0120, 0.0045, 0.0045, 0.0045, 0.0045, 0.0010, 0.0000]
    ]

    for i in range(12):
        for j in range(8):
            parts.append(f"    matB[{i}, {j}] := {matB_vals[i][j]:.5f};\n")

    parts.append("\n    (* 8x12 Measurement Output Matrix C *)\n")
    # y0: V_pcc, y1: f_pcc, y2: P_pcc, y3: Q_pcc, y4: V_dc, y5: T_max, y6: Q_cool, y7: T_chiller
    for i in range(8):
        for j in range(12):
            val = 0.0
            if i == 0 and j == 3: val = 0.0500 # Q couples to V
            elif i == 0 and j == 10: val = 0.0225 # Vdc couples to V
            elif i == 1 and j == 1: val = 0.159155 # omega to f (1/2pi)
            elif i == 2 and j == 2: val = 1.0000 # P_grid
            elif i == 3 and j == 3: val = 1.0000 # Q_grid
            elif i == 4 and j == 10: val = 1.0000 # V_dc
            elif i == 5 and j == 6: val = 1.0000 # T_max
            elif i == 6 and j == 8: val = 1.0000 # Q_cool
            elif i == 7 and j == 9: val = 1.0000 # T_chiller
            parts.append(f"    matC[{i}, {j}] := {val:.4f};\n")

    parts.append("\n    (* 8x8 Direct Feedthrough Matrix D *)\n")
    for i in range(8):
        for j in range(8):
            val = 0.0
            if i == 0 and j == 1: val = 0.0850 # field excitation Ev directly feeds V_pcc
            parts.append(f"    matD[{i}, {j}] := {val:.4f};\n")

    parts.append("\n    (* 12x8 Luenberger Observer Innovation Gain Matrix L *)\n")
    # Innovation gain L
    for i in range(12):
        for j in range(8):
            val = 0.0
            if i == j: val = 0.2500
            elif i == 1 and j == 1: val = 0.4200
            elif i == 2 and j == 2: val = 0.3800
            elif i == 3 and j == 3: val = 0.3500
            elif i == 10 and j == 4: val = 0.4500
            elif i == 6 and j == 5: val = 0.2800
            elif i == 8 and j == 6: val = 0.3200
            elif i == 9 and j == 7: val = 0.3000
            parts.append(f"    matL[{i}, {j}] := {val:.4f};\n")

    # MPC Weights & Constraints
    parts.append("""
    (* MPC Quadratic Cost Objective Weighting Vectors *)
    vecQ_weight[0] := 1.50;      (* delta tracking weight *)
    vecQ_weight[1] := 18.50;     (* omega_vsg frequency tracking weight *)
    vecQ_weight[2] := 25.00;     (* P_grid active power tracking weight *)
    vecQ_weight[3] := 20.00;     (* Q_grid reactive power tracking weight *)
    vecQ_weight[4] := 4.50;      (* SoC bulk balancing weight *)
    vecQ_weight[5] := 2.00;      (* polarization overpotential damping *)
    vecQ_weight[6] := 12.00;     (* T_max cell core temperature suppression *)
    vecQ_weight[7] := 15.00;     (* Delta_T inter-rack gradient penalty *)
    vecQ_weight[8] := 1.20;      (* cooling absorption heat tracking *)
    vecQ_weight[9] := 3.50;      (* chiller supply temperature regulation *)
    vecQ_weight[10] := 30.00;    (* V_dc bus voltage stabilization *)
    vecQ_weight[11] := 5.00;     (* harmonic ripple suppression *)

    (* Actuator Effort Penalties R *)
    vecR_weight[0] := 0.085;     (* P_m virtual mechanical power command *)
    vecR_weight[1] := 0.065;     (* E_v virtual field excitation voltage *)
    vecR_weight[2] := 0.015;     (* String 1 DC-DC current trim *)
    vecR_weight[3] := 0.015;     (* String 2 DC-DC current trim *)
    vecR_weight[4] := 0.015;     (* String 3 DC-DC current trim *)
    vecR_weight[5] := 0.015;     (* String 4 DC-DC current trim *)
    vecR_weight[6] := 0.005;     (* Chiller compressor VFD speed *)
    vecR_weight[7] := 0.008;     (* Glycol proportional valve command *)

    (* Actuator Slew Rate Penalties R_delta *)
    vecR_delta_weight[0] := 0.250;
    vecR_delta_weight[1] := 0.180;
    vecR_delta_weight[2] := 0.045;
    vecR_delta_weight[3] := 0.045;
    vecR_delta_weight[4] := 0.045;
    vecR_delta_weight[5] := 0.045;
    vecR_delta_weight[6] := 0.025;
    vecR_delta_weight[7] := 0.035;

    (* Terminal Horizon Penalty P *)
    vecP_terminal[0] := 2.50;
    vecP_terminal[1] := 28.00;
    vecP_terminal[2] := 40.00;
    vecP_terminal[3] := 32.00;
    vecP_terminal[4] := 8.00;
    vecP_terminal[5] := 3.50;
    vecP_terminal[6] := 22.00;
    vecP_terminal[7] := 25.00;
    vecP_terminal[8] := 2.00;
    vecP_terminal[9] := 6.00;
    vecP_terminal[10] := 55.00;
    vecP_terminal[11] := 8.50;

    (* Actuator Physical Saturation Lower Bounds *)
    vecU_min[0] := -100.0;       (* P_m lower limit: -100 MW (Full Charge) *)
    vecU_min[1] := 28.0;         (* E_v lower limit: 28.0 kV *)
    vecU_min[2] := -150.0;       (* String 1 trim: -150 A *)
    vecU_min[3] := -150.0;       (* String 2 trim: -150 A *)
    vecU_min[4] := -150.0;       (* String 3 trim: -150 A *)
    vecU_min[5] := -150.0;       (* String 4 trim: -150 A *)
    vecU_min[6] := 0.0;          (* Chiller compressor: 0 RPM *)
    vecU_min[7] := 0.0;          (* Glycol valves: 0.0 % *)

    (* Actuator Physical Saturation Upper Bounds *)
    vecU_max[0] := 100.0;        (* P_m upper limit: +100 MW (Full Discharge) *)
    vecU_max[1] := 40.0;         (* E_v upper limit: 40.0 kV *)
    vecU_max[2] := 150.0;        (* String 1 trim: +150 A *)
    vecU_max[3] := 150.0;        (* String 2 trim: +150 A *)
    vecU_max[4] := 150.0;        (* String 3 trim: +150 A *)
    vecU_max[5] := 150.0;        (* String 4 trim: +150 A *)
    vecU_max[6] := 4500.0;       (* Chiller compressor: 4500 RPM *)
    vecU_max[7] := 100.0;        (* Glycol valves: 100.0 % *)

    (* Actuator Maximum Slew Rate Per 10 ms Cycle *)
    vecU_slewMax[0] := 1.50;     (* 1.5 MW per 10 ms (150 MW/s ramp) *)
    vecU_slewMax[1] := 0.35;     (* 0.35 kV per 10 ms *)
    vecU_slewMax[2] := 12.0;     (* 12 A per 10 ms *)
    vecU_slewMax[3] := 12.0;
    vecU_slewMax[4] := 12.0;
    vecU_slewMax[5] := 12.0;
    vecU_slewMax[6] := 150.0;    (* 150 RPM per 10 ms *)
    vecU_slewMax[7] := 2.5;      (* 2.5 % per 10 ms *)

    bFirstScanDone := TRUE;
END_IF;
""")

    # PHASE 1: 2oo3 TMR Sensor Voting across 4 Channels
    parts.append("""
(* ==================================================================================================== *)
(* PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING SUITE                                     *)
(* Features: Discrepancy accumulation timers, degraded 2oo2 voting, single fallback & bumpless smoothing *)
(* ==================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------- *)
(* Channel Group 1: PCC 3-Phase RMS Grid Voltage Transducers (1A, 1B, 1C) [kV]                         *)
(* Discrepancy Tolerance: 1.25 kV, Accumulation Timeout: 250 ms                                        *)
(* ---------------------------------------------------------------------------------------------------- *)
rTempDiff := ABS(rPCC_Voltage_1A_kV - rPCC_Voltage_1B_kV);
IF rTempDiff > 1.25 THEN
    rPCC_Voltage_Disc_AB_ms := rPCC_Voltage_Disc_AB_ms + (tScanCycleTime_s * 1000.0);
ELSE
    rPCC_Voltage_Disc_AB_ms := MAX(0.0, rPCC_Voltage_Disc_AB_ms - (tScanCycleTime_s * 2000.0));
END_IF;

rTempDiff := ABS(rPCC_Voltage_1B_kV - rPCC_Voltage_1C_kV);
IF rTempDiff > 1.25 THEN
    rPCC_Voltage_Disc_BC_ms := rPCC_Voltage_Disc_BC_ms + (tScanCycleTime_s * 1000.0);
ELSE
    rPCC_Voltage_Disc_BC_ms := MAX(0.0, rPCC_Voltage_Disc_BC_ms - (tScanCycleTime_s * 2000.0));
END_IF;

rTempDiff := ABS(rPCC_Voltage_1C_kV - rPCC_Voltage_1A_kV);
IF rTempDiff > 1.25 THEN
    rPCC_Voltage_Disc_CA_ms := rPCC_Voltage_Disc_CA_ms + (tScanCycleTime_s * 1000.0);
ELSE
    rPCC_Voltage_Disc_CA_ms := MAX(0.0, rPCC_Voltage_Disc_CA_ms - (tScanCycleTime_s * 2000.0));
END_IF;

(* Evaluate Individual Channel Health *)
IF rPCC_Voltage_Disc_AB_ms > 250.0 AND rPCC_Voltage_Disc_CA_ms > 250.0 THEN
    bPCC_Voltage_HealthA := FALSE;
END_IF;
IF rPCC_Voltage_Disc_AB_ms > 250.0 AND rPCC_Voltage_Disc_BC_ms > 250.0 THEN
    bPCC_Voltage_HealthB := FALSE;
END_IF;
IF rPCC_Voltage_Disc_BC_ms > 250.0 AND rPCC_Voltage_Disc_CA_ms > 250.0 THEN
    bPCC_Voltage_HealthC := FALSE;
END_IF;

(* Automatic Fault Reset Check *)
IF bFaultReset THEN
    bPCC_Voltage_HealthA := TRUE;
    bPCC_Voltage_HealthB := TRUE;
    bPCC_Voltage_HealthC := TRUE;
    rPCC_Voltage_Disc_AB_ms := 0.0;
    rPCC_Voltage_Disc_BC_ms := 0.0;
    rPCC_Voltage_Disc_CA_ms := 0.0;
    bPCC_Voltage_Degraded := FALSE;
    bPCC_Voltage_SingleFallback := FALSE;
    bPCC_Voltage_Trip := FALSE;
END_IF;

(* Voting Decision Engine *)
IF bPCC_Voltage_HealthA AND bPCC_Voltage_HealthB AND bPCC_Voltage_HealthC THEN
    (* Full 2oo3 Triple Modular Redundancy Median Voting *)
    bPCC_Voltage_Degraded := FALSE;
    bPCC_Voltage_SingleFallback := FALSE;
    bPCC_Voltage_Trip := FALSE;
    IF rPCC_Voltage_1A_kV >= rPCC_Voltage_1B_kV THEN
        IF rPCC_Voltage_1B_kV >= rPCC_Voltage_1C_kV THEN
            rPCC_Voltage_Voted := rPCC_Voltage_1B_kV;
        ELSIF rPCC_Voltage_1A_kV <= rPCC_Voltage_1C_kV THEN
            rPCC_Voltage_Voted := rPCC_Voltage_1A_kV;
        ELSE
            rPCC_Voltage_Voted := rPCC_Voltage_1C_kV;
        END_IF;
    ELSE
        IF rPCC_Voltage_1A_kV >= rPCC_Voltage_1C_kV THEN
            rPCC_Voltage_Voted := rPCC_Voltage_1A_kV;
        ELSIF rPCC_Voltage_1B_kV <= rPCC_Voltage_1C_kV THEN
            rPCC_Voltage_Voted := rPCC_Voltage_1B_kV;
        ELSE
            rPCC_Voltage_Voted := rPCC_Voltage_1C_kV;
        END_IF;
    END_IF;
ELSIF bPCC_Voltage_HealthA AND bPCC_Voltage_HealthB THEN
    bPCC_Voltage_Degraded := TRUE;
    bPCC_Voltage_SingleFallback := FALSE;
    bPCC_Voltage_Voted := (rPCC_Voltage_1A_kV + rPCC_Voltage_1B_kV) * 0.50;
ELSIF bPCC_Voltage_HealthB AND bPCC_Voltage_HealthC THEN
    bPCC_Voltage_Degraded := TRUE;
    bPCC_Voltage_SingleFallback := FALSE;
    bPCC_Voltage_Voted := (rPCC_Voltage_1B_kV + rPCC_Voltage_1C_kV) * 0.50;
ELSIF bPCC_Voltage_HealthC AND bPCC_Voltage_HealthA THEN
    bPCC_Voltage_Degraded := TRUE;
    bPCC_Voltage_SingleFallback := FALSE;
    bPCC_Voltage_Voted := (rPCC_Voltage_1C_kV + rPCC_Voltage_1A_kV) * 0.50;
ELSIF bPCC_Voltage_HealthA THEN
    bPCC_Voltage_Degraded := FALSE;
    bPCC_Voltage_SingleFallback := TRUE;
    rPCC_Voltage_Voted := rPCC_Voltage_1A_kV;
ELSIF bPCC_Voltage_HealthB THEN
    bPCC_Voltage_Degraded := FALSE;
    bPCC_Voltage_SingleFallback := TRUE;
    rPCC_Voltage_Voted := rPCC_Voltage_1B_kV;
ELSIF bPCC_Voltage_HealthC THEN
    bPCC_Voltage_Degraded := FALSE;
    bPCC_Voltage_SingleFallback := TRUE;
    rPCC_Voltage_Voted := rPCC_Voltage_1C_kV;
ELSE
    bPCC_Voltage_Degraded := FALSE;
    bPCC_Voltage_SingleFallback := FALSE;
    bPCC_Voltage_Trip := TRUE;
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* Channel Group 2: PCC Utility Grid Frequency PMU Measurement Units (2A, 2B, 2C) [Hz]                 *)
(* Discrepancy Tolerance: 0.08 Hz, Accumulation Timeout: 200 ms                                        *)
(* ---------------------------------------------------------------------------------------------------- *)
rTempDiff := ABS(rPCC_Frequency_2A_Hz - rPCC_Frequency_2B_Hz);
IF rTempDiff > 0.08 THEN
    rPCC_Frequency_Disc_AB_ms := rPCC_Frequency_Disc_AB_ms + (tScanCycleTime_s * 1000.0);
ELSE
    rPCC_Frequency_Disc_AB_ms := MAX(0.0, rPCC_Frequency_Disc_AB_ms - (tScanCycleTime_s * 2000.0));
END_IF;

rTempDiff := ABS(rPCC_Frequency_2B_Hz - rPCC_Frequency_2C_Hz);
IF rTempDiff > 0.08 THEN
    rPCC_Frequency_Disc_BC_ms := rPCC_Frequency_Disc_BC_ms + (tScanCycleTime_s * 1000.0);
ELSE
    rPCC_Frequency_Disc_BC_ms := MAX(0.0, rPCC_Frequency_Disc_BC_ms - (tScanCycleTime_s * 2000.0));
END_IF;

rTempDiff := ABS(rPCC_Frequency_2C_Hz - rPCC_Frequency_2A_Hz);
IF rTempDiff > 0.08 THEN
    rPCC_Frequency_Disc_CA_ms := rPCC_Frequency_Disc_CA_ms + (tScanCycleTime_s * 1000.0);
ELSE
    rPCC_Frequency_Disc_CA_ms := MAX(0.0, rPCC_Frequency_Disc_CA_ms - (tScanCycleTime_s * 2000.0));
END_IF;

IF rPCC_Frequency_Disc_AB_ms > 200.0 AND rPCC_Frequency_Disc_CA_ms > 200.0 THEN
    bPCC_Frequency_HealthA := FALSE;
END_IF;
IF rPCC_Frequency_Disc_AB_ms > 200.0 AND rPCC_Frequency_Disc_BC_ms > 200.0 THEN
    bPCC_Frequency_HealthB := FALSE;
END_IF;
IF rPCC_Frequency_Disc_BC_ms > 200.0 AND rPCC_Frequency_Disc_CA_ms > 200.0 THEN
    bPCC_Frequency_HealthC := FALSE;
END_IF;

IF bFaultReset THEN
    bPCC_Frequency_HealthA := TRUE;
    bPCC_Frequency_HealthB := TRUE;
    bPCC_Frequency_HealthC := TRUE;
    rPCC_Frequency_Disc_AB_ms := 0.0;
    rPCC_Frequency_Disc_BC_ms := 0.0;
    rPCC_Frequency_Disc_CA_ms := 0.0;
    bPCC_Frequency_Degraded := FALSE;
    bPCC_Frequency_SingleFallback := FALSE;
    bPCC_Frequency_Trip := FALSE;
END_IF;

IF bPCC_Frequency_HealthA AND bPCC_Frequency_HealthB AND bPCC_Frequency_HealthC THEN
    bPCC_Frequency_Degraded := FALSE;
    bPCC_Frequency_SingleFallback := FALSE;
    bPCC_Frequency_Trip := FALSE;
    IF rPCC_Frequency_2A_Hz >= rPCC_Frequency_2B_Hz THEN
        IF rPCC_Frequency_2B_Hz >= rPCC_Frequency_2C_Hz THEN
            rPCC_Frequency_Voted := rPCC_Frequency_2B_Hz;
        ELSIF rPCC_Frequency_2A_Hz <= rPCC_Frequency_2C_Hz THEN
            rPCC_Frequency_Voted := rPCC_Frequency_2A_Hz;
        ELSE
            rPCC_Frequency_Voted := rPCC_Frequency_2C_Hz;
        END_IF;
    ELSE
        IF rPCC_Frequency_2A_Hz >= rPCC_Frequency_2C_Hz THEN
            rPCC_Frequency_Voted := rPCC_Frequency_2A_Hz;
        ELSIF rPCC_Frequency_2B_Hz <= rPCC_Frequency_2C_Hz THEN
            rPCC_Frequency_Voted := rPCC_Frequency_2B_Hz;
        ELSE
            rPCC_Frequency_Voted := rPCC_Frequency_2C_Hz;
        END_IF;
    END_IF;
ELSIF bPCC_Frequency_HealthA AND bPCC_Frequency_HealthB THEN
    bPCC_Frequency_Degraded := TRUE;
    bPCC_Frequency_SingleFallback := FALSE;
    rPCC_Frequency_Voted := (rPCC_Frequency_2A_Hz + rPCC_Frequency_2B_Hz) * 0.50;
ELSIF bPCC_Frequency_HealthB AND bPCC_Frequency_HealthC THEN
    bPCC_Frequency_Degraded := TRUE;
    bPCC_Frequency_SingleFallback := FALSE;
    rPCC_Frequency_Voted := (rPCC_Frequency_2B_Hz + rPCC_Frequency_2C_Hz) * 0.50;
ELSIF bPCC_Frequency_HealthC AND bPCC_Frequency_HealthA THEN
    bPCC_Frequency_Degraded := TRUE;
    bPCC_Frequency_SingleFallback := FALSE;
    rPCC_Frequency_Voted := (rPCC_Frequency_2C_Hz + rPCC_Frequency_2A_Hz) * 0.50;
ELSIF bPCC_Frequency_HealthA THEN
    bPCC_Frequency_Degraded := FALSE;
    bPCC_Frequency_SingleFallback := TRUE;
    rPCC_Frequency_Voted := rPCC_Frequency_2A_Hz;
ELSIF bPCC_Frequency_HealthB THEN
    bPCC_Frequency_Degraded := FALSE;
    bPCC_Frequency_SingleFallback := TRUE;
    rPCC_Frequency_Voted := rPCC_Frequency_2B_Hz;
ELSIF bPCC_Frequency_HealthC THEN
    bPCC_Frequency_Degraded := FALSE;
    bPCC_Frequency_SingleFallback := TRUE;
    rPCC_Frequency_Voted := rPCC_Frequency_2C_Hz;
ELSE
    bPCC_Frequency_Degraded := FALSE;
    bPCC_Frequency_SingleFallback := FALSE;
    bPCC_Frequency_Trip := TRUE;
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* Channel Group 3: BESS Central DC Link Bus Voltage Transducers (3A, 3B, 3C) [V]                       *)
(* Discrepancy Tolerance: 35.0 V, Accumulation Timeout: 300 ms                                         *)
(* ---------------------------------------------------------------------------------------------------- *)
rTempDiff := ABS(rDCLink_Voltage_3A_V - rDCLink_Voltage_3B_V);
IF rTempDiff > 35.0 THEN
    rDCLink_Voltage_Disc_AB_ms := rDCLink_Voltage_Disc_AB_ms + (tScanCycleTime_s * 1000.0);
ELSE
    rDCLink_Voltage_Disc_AB_ms := MAX(0.0, rDCLink_Voltage_Disc_AB_ms - (tScanCycleTime_s * 2000.0));
END_IF;

rTempDiff := ABS(rDCLink_Voltage_3B_V - rDCLink_Voltage_3C_V);
IF rTempDiff > 35.0 THEN
    rDCLink_Voltage_Disc_BC_ms := rDCLink_Voltage_Disc_BC_ms + (tScanCycleTime_s * 1000.0);
ELSE
    rDCLink_Voltage_Disc_BC_ms := MAX(0.0, rDCLink_Voltage_Disc_BC_ms - (tScanCycleTime_s * 2000.0));
END_IF;

rTempDiff := ABS(rDCLink_Voltage_3C_V - rDCLink_Voltage_3A_V);
IF rTempDiff > 35.0 THEN
    rDCLink_Voltage_Disc_CA_ms := rDCLink_Voltage_Disc_CA_ms + (tScanCycleTime_s * 1000.0);
ELSE
    rDCLink_Voltage_Disc_CA_ms := MAX(0.0, rDCLink_Voltage_Disc_CA_ms - (tScanCycleTime_s * 2000.0));
END_IF;

IF rDCLink_Voltage_Disc_AB_ms > 300.0 AND rDCLink_Voltage_Disc_CA_ms > 300.0 THEN
    bDCLink_Voltage_HealthA := FALSE;
END_IF;
IF rDCLink_Voltage_Disc_AB_ms > 300.0 AND rDCLink_Voltage_Disc_BC_ms > 300.0 THEN
    bDCLink_Voltage_HealthB := FALSE;
END_IF;
IF rDCLink_Voltage_Disc_BC_ms > 300.0 AND rDCLink_Voltage_Disc_CA_ms > 300.0 THEN
    bDCLink_Voltage_HealthC := FALSE;
END_IF;

IF bFaultReset THEN
    bDCLink_Voltage_HealthA := TRUE;
    bDCLink_Voltage_HealthB := TRUE;
    bDCLink_Voltage_HealthC := TRUE;
    rDCLink_Voltage_Disc_AB_ms := 0.0;
    rDCLink_Voltage_Disc_BC_ms := 0.0;
    rDCLink_Voltage_Disc_CA_ms := 0.0;
    bDCLink_Voltage_Degraded := FALSE;
    bDCLink_Voltage_SingleFallback := FALSE;
    bDCLink_Voltage_Trip := FALSE;
END_IF;

IF bDCLink_Voltage_HealthA AND bDCLink_Voltage_HealthB AND bDCLink_Voltage_HealthC THEN
    bDCLink_Voltage_Degraded := FALSE;
    bDCLink_Voltage_SingleFallback := FALSE;
    bDCLink_Voltage_Trip := FALSE;
    IF rDCLink_Voltage_3A_V >= rDCLink_Voltage_3B_V THEN
        IF rDCLink_Voltage_3B_V >= rDCLink_Voltage_3C_V THEN
            rDCLink_Voltage_Voted := rDCLink_Voltage_3B_V;
        ELSIF rDCLink_Voltage_3A_V <= rDCLink_Voltage_3C_V THEN
            rDCLink_Voltage_Voted := rDCLink_Voltage_3A_V;
        ELSE
            rDCLink_Voltage_Voted := rDCLink_Voltage_3C_V;
        END_IF;
    ELSE
        IF rDCLink_Voltage_3A_V >= rDCLink_Voltage_3C_V THEN
            rDCLink_Voltage_Voted := rDCLink_Voltage_3A_V;
        ELSIF rDCLink_Voltage_3B_V <= rDCLink_Voltage_3C_V THEN
            rDCLink_Voltage_Voted := rDCLink_Voltage_3B_V;
        ELSE
            rDCLink_Voltage_Voted := rDCLink_Voltage_3C_V;
        END_IF;
    END_IF;
ELSIF bDCLink_Voltage_HealthA AND bDCLink_Voltage_HealthB THEN
    bDCLink_Voltage_Degraded := TRUE;
    bDCLink_Voltage_SingleFallback := FALSE;
    rDCLink_Voltage_Voted := (rDCLink_Voltage_3A_V + rDCLink_Voltage_3B_V) * 0.50;
ELSIF bDCLink_Voltage_HealthB AND bDCLink_Voltage_HealthC THEN
    bDCLink_Voltage_Degraded := TRUE;
    bDCLink_Voltage_SingleFallback := FALSE;
    rDCLink_Voltage_Voted := (rDCLink_Voltage_3B_V + rDCLink_Voltage_3C_V) * 0.50;
ELSIF bDCLink_Voltage_HealthC AND bDCLink_Voltage_HealthA THEN
    bDCLink_Voltage_Degraded := TRUE;
    bDCLink_Voltage_SingleFallback := FALSE;
    rDCLink_Voltage_Voted := (rDCLink_Voltage_3C_V + rDCLink_Voltage_3A_V) * 0.50;
ELSIF bDCLink_Voltage_HealthA THEN
    bDCLink_Voltage_Degraded := FALSE;
    bDCLink_Voltage_SingleFallback := TRUE;
    rDCLink_Voltage_Voted := rDCLink_Voltage_3A_V;
ELSIF bDCLink_Voltage_HealthB THEN
    bDCLink_Voltage_Degraded := FALSE;
    bDCLink_Voltage_SingleFallback := TRUE;
    rDCLink_Voltage_Voted := rDCLink_Voltage_3B_V;
ELSIF bDCLink_Voltage_HealthC THEN
    bDCLink_Voltage_Degraded := FALSE;
    bDCLink_Voltage_SingleFallback := TRUE;
    rDCLink_Voltage_Voted := rDCLink_Voltage_3C_V;
ELSE
    bDCLink_Voltage_Degraded := FALSE;
    bDCLink_Voltage_SingleFallback := FALSE;
    bDCLink_Voltage_Trip := TRUE;
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* Channel Group 4: Battery Rack Off-Gas Multi-Gas Sensing Sensors (4A, 4B, 4C) [ppm H2/CO]            *)
(* Discrepancy Tolerance: 15.0 ppm, Accumulation Timeout: 400 ms                                       *)
(* Note: In Safety Gas Sensing, we take the highest healthy reading (maximum conservative voting)      *)
(* ---------------------------------------------------------------------------------------------------- *)
rTempDiff := ABS(rOffGas_H2_CO_4A_ppm - rOffGas_H2_CO_4B_ppm);
IF rTempDiff > 15.0 THEN
    rOffGas_Disc_AB_ms := rOffGas_Disc_AB_ms + (tScanCycleTime_s * 1000.0);
ELSE
    rOffGas_Disc_AB_ms := MAX(0.0, rOffGas_Disc_AB_ms - (tScanCycleTime_s * 2000.0));
END_IF;

rTempDiff := ABS(rOffGas_H2_CO_4B_ppm - rOffGas_H2_CO_4C_ppm);
IF rTempDiff > 15.0 THEN
    rOffGas_Disc_BC_ms := rOffGas_Disc_BC_ms + (tScanCycleTime_s * 1000.0);
ELSE
    rOffGas_Disc_BC_ms := MAX(0.0, rOffGas_Disc_BC_ms - (tScanCycleTime_s * 2000.0));
END_IF;

rTempDiff := ABS(rOffGas_H2_CO_4C_ppm - rOffGas_H2_CO_4A_ppm);
IF rTempDiff > 15.0 THEN
    rOffGas_Disc_CA_ms := rOffGas_Disc_CA_ms + (tScanCycleTime_s * 1000.0);
ELSE
    rOffGas_Disc_CA_ms := MAX(0.0, rOffGas_Disc_CA_ms - (tScanCycleTime_s * 2000.0));
END_IF;

IF rOffGas_Disc_AB_ms > 400.0 AND rOffGas_Disc_CA_ms > 400.0 THEN
    bOffGas_HealthA := FALSE;
END_IF;
IF rOffGas_Disc_AB_ms > 400.0 AND rOffGas_Disc_BC_ms > 400.0 THEN
    bOffGas_HealthB := FALSE;
END_IF;
IF rOffGas_Disc_BC_ms > 400.0 AND rOffGas_Disc_CA_ms > 400.0 THEN
    bOffGas_HealthC := FALSE;
END_IF;

IF bFaultReset THEN
    bOffGas_HealthA := TRUE;
    bOffGas_HealthB := TRUE;
    bOffGas_HealthC := TRUE;
    rOffGas_Disc_AB_ms := 0.0;
    rOffGas_Disc_BC_ms := 0.0;
    rOffGas_Disc_CA_ms := 0.0;
    bOffGas_Degraded := FALSE;
    bOffGas_SingleFallback := FALSE;
    bOffGas_Trip := FALSE;
END_IF;

IF bOffGas_HealthA AND bOffGas_HealthB AND bOffGas_HealthC THEN
    bOffGas_Degraded := FALSE;
    bOffGas_SingleFallback := FALSE;
    bOffGas_Trip := FALSE;
    (* Conservative maximum healthy gas reading *)
    rOffGas_H2_CO_Voted := MAX(rOffGas_H2_CO_4A_ppm, MAX(rOffGas_H2_CO_4B_ppm, rOffGas_H2_CO_4C_ppm));
ELSIF bOffGas_HealthA AND bOffGas_HealthB THEN
    bOffGas_Degraded := TRUE;
    bOffGas_SingleFallback := FALSE;
    rOffGas_H2_CO_Voted := MAX(rOffGas_H2_CO_4A_ppm, rOffGas_H2_CO_4B_ppm);
ELSIF bOffGas_HealthB AND bOffGas_HealthC THEN
    bOffGas_Degraded := TRUE;
    bOffGas_SingleFallback := FALSE;
    rOffGas_H2_CO_Voted := MAX(rOffGas_H2_CO_4B_ppm, rOffGas_H2_CO_4C_ppm);
ELSIF bOffGas_HealthC AND bOffGas_HealthA THEN
    bOffGas_Degraded := TRUE;
    bOffGas_SingleFallback := FALSE;
    rOffGas_H2_CO_Voted := MAX(rOffGas_H2_CO_4C_ppm, rOffGas_H2_CO_4A_ppm);
ELSIF bOffGas_HealthA THEN
    bOffGas_Degraded := FALSE;
    bOffGas_SingleFallback := TRUE;
    rOffGas_H2_CO_Voted := rOffGas_H2_CO_4A_ppm;
ELSIF bOffGas_HealthB THEN
    bOffGas_Degraded := FALSE;
    bOffGas_SingleFallback := TRUE;
    rOffGas_H2_CO_Voted := rOffGas_H2_CO_4B_ppm;
ELSIF bOffGas_HealthC THEN
    bOffGas_Degraded := FALSE;
    bOffGas_SingleFallback := TRUE;
    rOffGas_H2_CO_Voted := rOffGas_H2_CO_4C_ppm;
ELSE
    bOffGas_Degraded := FALSE;
    bOffGas_SingleFallback := FALSE;
    bOffGas_Trip := TRUE;
END_IF;
""")

    # PHASE 2: Cyber-Physical State-Space Observer & First-Principles Physics
    parts.append("""
(* ==================================================================================================== *)
(* PHASE 2: CYBER-PHYSICAL STATE-SPACE ESTIMATION & FIRST-PRINCIPLES DYNAMICS                           *)
(* Luenberger State-Space Observer (x_hat[k+1] = A*x_hat[k] + B*u[k] + L*(y[k] - C*x_hat[k]))            *)
(* First-Principles Virtual Synchronous Generator (VSG) Swing Equations, Droop & ECM Diffusion         *)
(* ==================================================================================================== *)

(* Pack Voted Sensor Observation Vector y_meas (8x1) *)
vecY_meas[0] := rPCC_Voltage_Voted;
vecY_meas[1] := rPCC_Frequency_Voted;
vecY_meas[2] := rPCC_ActivePower_Actual_MW;
vecY_meas[3] := rPCC_ReactivePower_Actual_MVAr;
vecY_meas[4] := rDCLink_Voltage_Voted;
vecY_meas[5] := rBattery_CellMaxTemp_degC;
vecY_meas[6] := rThermal_HeatAbsorption_kW;
vecY_meas[7] := rGlycol_SupplyTemp_degC;

(* 1. Prior One-Step-Ahead State Prediction: x_pred = A * x_hat + B * u *)
FOR iIdx := 0 TO 11 DO
    rTempSum := 0.0;
    FOR jIdx := 0 TO 11 DO
        rTempSum := rTempSum + (matA[iIdx, jIdx] * vecX_hat[jIdx]);
    END_FOR;
    FOR mIdx := 0 TO 7 DO
        rTempSum := rTempSum + (matB[iIdx, mIdx] * vecU[mIdx]);
    END_FOR;
    vecX_pred[iIdx] := rTempSum;
END_FOR;

(* 2. Measurement Output Prediction: y_hat = C * x_pred + D * u *)
FOR iIdx := 0 TO 7 DO
    rTempSum := 0.0;
    FOR jIdx := 0 TO 11 DO
        rTempSum := rTempSum + (matC[iIdx, jIdx] * vecX_pred[jIdx]);
    END_FOR;
    FOR mIdx := 0 TO 7 DO
        rTempSum := rTempSum + (matD[iIdx, mIdx] * vecU[mIdx]);
    END_FOR;
    vecY_hat[iIdx] := rTempSum;
    vecInnov[iIdx] := vecY_meas[iIdx] - vecY_hat[iIdx];
END_FOR;

(* 3. Posterior State Correction: x_hat = x_pred + L * innov *)
FOR iIdx := 0 TO 11 DO
    rTempSum := vecX_pred[iIdx];
    FOR jIdx := 0 TO 7 DO
        rTempSum := rTempSum + (matL[iIdx, jIdx] * vecInnov[jIdx]);
    END_FOR;
    vecX_hat[iIdx] := rTempSum;
END_FOR;

(* Expose Cyber-Physical State Estimates to External Telemetry *)
rEst_VirtualRotorAngle_rad       := vecX_hat[0];
rEst_VirtualRotorSpeed_rads      := vecX_hat[1];
rEst_PCC_ActivePower_MW          := vecX_hat[2];
rEst_PCC_ReactivePower_MVAr      := vecX_hat[3];
rEst_BulkBatterySoC_pct          := vecX_hat[4];
rEst_PolarizationOverpotential_V := vecX_hat[5];
rEst_MaxCellTemp_degC            := vecX_hat[6];
rEst_ThermalGradient_degC        := vecX_hat[7];
rEst_ThermalAbsorption_kW        := vecX_hat[8];
rEst_ChillerSupplyTemp_degC      := vecX_hat[9];
rEst_DCLinkVoltage_V             := vecX_hat[10];
rEst_DCHarmonicRipple_A          := vecX_hat[11];

(* ---------------------------------------------------------------------------------------------------- *)
(* First-Principles Virtual Synchronous Machine (VSM/VSG) Dynamics                                      *)
(* ---------------------------------------------------------------------------------------------------- *)
(* High-Speed Rate-of-Change-of-Frequency (RoCoF) Estimation *)
IF tScanCycleTime_s > 0.001 THEN
    rGrid_RoCoF_Hz_per_s := (rPCC_Frequency_Voted - rPrev_PCC_Frequency) / tScanCycleTime_s;
    rPrev_PCC_Frequency := rPCC_Frequency_Voted;
END_IF;

(* 1st-Order Low-Pass Filter on RoCoF for Synthetic Inertia Noise Rejection (tau = 40 ms) *)
rVSG_FilteredRoCoF := rVSG_FilteredRoCoF + (tScanCycleTime_s / 0.040) * (rGrid_RoCoF_Hz_per_s - rVSG_FilteredRoCoF);

(* Synthetic Inertial Response Power Injection: P_inert = -2 * H * (P_n / f_0) * (df/dt) *)
(* With H = 4.5 s, P_n = 100 MW, f_0 = 50.0 Hz -> Gain = -2 * 4.5 * 100 / 50 = -18.0 MW/(Hz/s) *)
rVSG_SyntheticInertiaPower_MW := -18.0 * rVSG_FilteredRoCoF;
IF rVSG_SyntheticInertiaPower_MW > 40.0 THEN
    rVSG_SyntheticInertiaPower_MW := 40.0;
ELSIF rVSG_SyntheticInertiaPower_MW < -40.0 THEN
    rVSG_SyntheticInertiaPower_MW := -40.0;
END_IF;

(* Primary Frequency P-f Droop Regulation Response: Delta_P = - (P_n / (R * f_0)) * (f - f_0) *)
(* With R = 3.0% droop (0.03 p.u.), P_n = 100 MW, f_0 = 50.0 Hz -> Gain = 100 / (0.03 * 50) = 66.67 MW/Hz *)
rVSG_FrequencyDroopPower_MW := -66.6667 * (rPCC_Frequency_Voted - rGrid_NominalFrequency_Hz);
IF rVSG_FrequencyDroopPower_MW > 50.0 THEN
    rVSG_FrequencyDroopPower_MW := 50.0;
ELSIF rVSG_FrequencyDroopPower_MW < -50.0 THEN
    rVSG_FrequencyDroopPower_MW := -50.0;
END_IF;

(* Reactive Voltage Q-V Droop Regulation Response: Delta_Q = - (Q_n / (K_v * V_0)) * (V - V_0) *)
(* With K_v = 4.0% droop (0.04 p.u.), Q_n = 60 MVAr, V_0 = 34.5 kV -> Gain = 60 / (0.04 * 34.5) = 43.48 MVAr/kV *)
rVSG_VoltageDroopReactive_MVAr := -43.4783 * (rPCC_Voltage_Voted - rGrid_NominalVoltage_kV);
IF rVSG_VoltageDroopReactive_MVAr > 50.0 THEN
    rVSG_VoltageDroopReactive_MVAr := 50.0;
ELSIF rVSG_VoltageDroopReactive_MVAr < -50.0 THEN
    rVSG_VoltageDroopReactive_MVAr := -50.0;
END_IF;

(* Continuous 2nd-Order Swing Equation Numerical Integration *)
(* J * d(omega)/dt = P_m / omega - P_e / omega_0 - D_p * (omega - omega_0) *)
rTempDiff := (vecU[0] / MAX(100.0, rVSG_RotorSpeed_omega)) - (rPCC_ActivePower_Actual_MW / rVSG_NominalOmega_rads)
             - (rVSG_DampingFactor_Dp * (rVSG_RotorSpeed_omega - rVSG_NominalOmega_rads));
rVSG_RotorSpeed_omega := rVSG_RotorSpeed_omega + (tScanCycleTime_s * (rTempDiff / (rVSG_Inertia_J_kgm2 * 1.0E-6)));
rVSG_RotorAngle_delta := rVSG_RotorAngle_delta + (tScanCycleTime_s * (rVSG_RotorSpeed_omega - rVSG_NominalOmega_rads));

(* Wrap Rotor Angle to [-pi, +pi] *)
IF rVSG_RotorAngle_delta > 3.14159265 THEN
    rVSG_RotorAngle_delta := rVSG_RotorAngle_delta - 6.2831853;
ELSIF rVSG_RotorAngle_delta < -3.14159265 THEN
    rVSG_RotorAngle_delta := rVSG_RotorAngle_delta + 6.2831853;
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* Battery Equivalent Circuit Model (ECM) Polarization & Active String SoC Balancing                   *)
(* ---------------------------------------------------------------------------------------------------- *)
(* 1st-Order RC Polarization Diffusion: d(eta_p)/dt = - eta_p / (R1*C1) + I_batt / C1 *)
rTempDiff := (-rBattery_PolarizationOverpot / (rBattery_ECM_R1_Ohm * rBattery_ECM_C1_Farad))
             + (rBattery_TotalCurrent_A / rBattery_ECM_C1_Farad);
rBattery_PolarizationOverpot := rBattery_PolarizationOverpot + (tScanCycleTime_s * rTempDiff);

(* String State-of-Charge Mean & Individual Divergence Deviations *)
rString_SoC_Mean := (rBattery_String1_SoC_pct + rBattery_String2_SoC_pct + rBattery_String3_SoC_pct + rBattery_String4_SoC_pct) * 0.250;
rString1_SoC_Dev := rBattery_String1_SoC_pct - rString_SoC_Mean;
rString2_SoC_Dev := rBattery_String2_SoC_pct - rString_SoC_Mean;
rString3_SoC_Dev := rBattery_String3_SoC_pct - rString_SoC_Mean;
rString4_SoC_Dev := rBattery_String4_SoC_pct - rString_SoC_Mean;

(* Active DC-DC Current Trim Balancing: Higher SoC strings discharge more (+), lower SoC discharge less (-) *)
IF NOT bManualTrimOverride THEN
    rString1_CurrentTrimCmd_A := rBalancingGain_A_per_pct * rString1_SoC_Dev;
    rString2_CurrentTrimCmd_A := rBalancingGain_A_per_pct * rString2_SoC_Dev;
    rString3_CurrentTrimCmd_A := rBalancingGain_A_per_pct * rString3_SoC_Dev;
    rString4_CurrentTrimCmd_A := rBalancingGain_A_per_pct * rString4_SoC_Dev;
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* Liquid Glycol Thermal Management Dynamics & Chiller Compressor PI Control                            *)
(* ---------------------------------------------------------------------------------------------------- *)
(* Coolant Thermal Energy Extraction: Q_cool = m_dot * Cp * (T_return - T_supply) *)
(* Mass flow m_dot [kg/s] = Flow [m3/h] * Density [kg/m3] / 3600 *)
rThermal_HeatAbsorption_kW := (rGlycol_CoolantFlow_m3h * rGlycol_Density_kg_m3 / 3600.0) 
                              * rGlycol_SpecificHeat_kJ_kgK 
                              * (rGlycol_ReturnTemp_degC - rGlycol_SupplyTemp_degC);

(* Inter-Rack Thermal Gradient: Delta_T = T_max - T_min *)
rThermal_RackGradient_DeltaT := rBattery_CellMaxTemp_degC - rBattery_CellMinTemp_degC;

(* Dynamic Chiller Supply Temperature Setpoint based on Ambient and Cell Temps *)
IF rBattery_CellMaxTemp_degC > 35.0 THEN
    rChiller_TargetSupplyTemp_degC := 15.0;
ELSIF rBattery_CellMaxTemp_degC > 28.0 THEN
    rChiller_TargetSupplyTemp_degC := 18.0;
ELSE
    rChiller_TargetSupplyTemp_degC := 22.0;
END_IF;

(* Closed-Loop Chiller Refrigeration Compressor PI Speed Controller *)
rTempDiff := rGlycol_SupplyTemp_degC - rChiller_TargetSupplyTemp_degC;
rChiller_PID_Integral := rChiller_PID_Integral + (rTempDiff * tScanCycleTime_s * 12.5);
IF rChiller_PID_Integral > 2500.0 THEN
    rChiller_PID_Integral := 2500.0;
ELSIF rChiller_PID_Integral < 0.0 THEN
    rChiller_PID_Integral := 0.0;
END_IF;

rChiller_CompressorVFD_RPM := 1500.0 + (rTempDiff * 250.0) + rChiller_PID_Integral;
IF rChiller_CompressorVFD_RPM > 4500.0 THEN
    rChiller_CompressorVFD_RPM := 4500.0;
ELSIF rChiller_CompressorVFD_RPM < 0.0 THEN
    rChiller_CompressorVFD_RPM := 0.0;
END_IF;
""")

    # PHASE 3: Receding Horizon MPC with 10 Unrolled PGD Iterations
    parts.append("""
(* ==================================================================================================== *)
(* PHASE 3: RECEDING-HORIZON MPC OPTIMIZATION WITH UNROLLED PGD (10 ITERATIONS)                         *)
(* Optimization Horizon N = 5 steps, 12 States, 8 Actuators                                            *)
(* Unrolled Projected Gradient Descent (PGD) with Actuator Slew Rate Limiting & Box Constraints         *)
(* ==================================================================================================== *)

(* Establish Target Equilibrium Reference Vector vecX_target *)
vecX_target[0] := 0.0;                                     (* Virtual delta reference: 0.0 rad *)
vecX_target[1] := rVSG_NominalOmega_rads;                  (* Nominal angular velocity: 314.16 rad/s *)
vecX_target[2] := rDispatch_ActivePower_MW;                (* Dispatch active power target [MW] *)
vecX_target[3] := rDispatch_ReactivePower_MVAr;            (* Dispatch reactive power target [MVAr] *)
vecX_target[4] := 65.0;                                    (* Nominal bulk SoC target: 65.0% *)
vecX_target[5] := 0.0;                                     (* Zero polarization overpotential target *)
vecX_target[6] := 25.0;                                    (* Target battery core temperature: 25.0 deg C *)
vecX_target[7] := 0.0;                                     (* Zero inter-rack gradient target *)
vecX_target[8] := 120.0;                                   (* Nominal thermal absorption: 120.0 kW *)
vecX_target[9] := rChiller_TargetSupplyTemp_degC;          (* Dynamic chiller supply target *)
vecX_target[10] := 1500.0;                                 (* DC bus voltage target: 1500.0 V *)
vecX_target[11] := 0.0;                                    (* Zero DC harmonic ripple target *)

(* Establish Nominal Actuator Targets vecU_target *)
vecU_target[0] := rDispatch_ActivePower_MW;
vecU_target[1] := 34.5;
vecU_target[2] := rString1_CurrentTrimCmd_A;
vecU_target[3] := rString2_CurrentTrimCmd_A;
vecU_target[4] := rString3_CurrentTrimCmd_A;
vecU_target[5] := rString4_CurrentTrimCmd_A;
vecU_target[6] := rChiller_CompressorVFD_RPM;
vecU_target[7] := 65.0;

(* Initialize MPC Initial Horizon State from Current State Estimate *)
FOR iIdx := 0 TO 11 DO
    trajX_mpc[0, iIdx] := vecX_hat[iIdx];
END_FOR;

(* Warm-Start Initial Control Trajectory from Previous Solution or Target *)
FOR kStep := 0 TO 4 DO
    FOR mIdx := 0 TO 7 DO
        trajU_mpc[kStep, mIdx] := vecU[mIdx];
    END_FOR;
END_FOR;
""")

    # Unroll 10 iterations of Projected Gradient Descent
    for iter_num in range(1, 11):
        parts.append(f"""
(* --- PGD Optimization Unrolled Iteration #{iter_num} of 10 --- *)
(* Forward State Simulation Over Horizon N = 5 Steps *)
FOR kStep := 0 TO 4 DO
    FOR iIdx := 0 TO 11 DO
        rTempSum := 0.0;
        FOR jIdx := 0 TO 11 DO
            rTempSum := rTempSum + (matA[iIdx, jIdx] * trajX_mpc[kStep, jIdx]);
        END_FOR;
        FOR mIdx := 0 TO 7 DO
            rTempSum := rTempSum + (matB[iIdx, mIdx] * trajU_mpc[kStep, mIdx]);
        END_FOR;
        trajX_mpc[kStep + 1, iIdx] := rTempSum;
    END_FOR;
END_FOR;

(* Analytical Gradient Evaluation & Projected Gradient Descent Update *)
FOR kStep := 0 TO 4 DO
    FOR mIdx := 0 TO 7 DO
        (* Cost Gradient Contribution from Actuator Effort & Slew Penalties *)
        rTempGrad := (vecR_weight[mIdx] * (trajU_mpc[kStep, mIdx] - vecU_target[mIdx]));
        IF kStep > 0 THEN
            rTempGrad := rTempGrad + (vecR_delta_weight[mIdx] * (trajU_mpc[kStep, mIdx] - trajU_mpc[kStep - 1, mIdx]));
        ELSE
            rTempGrad := rTempGrad + (vecR_delta_weight[mIdx] * (trajU_mpc[kStep, mIdx] - vecU_prev[mIdx]));
        END_IF;

        (* Backward Adjoint Gradient Contribution from State Deviation via Matrix B *)
        FOR iIdx := 0 TO 11 DO
            rTempDiff := trajX_mpc[kStep + 1, iIdx] - vecX_target[iIdx];
            IF kStep = 4 THEN
                rTempGrad := rTempGrad + (matB[iIdx, mIdx] * vecP_terminal[iIdx] * rTempDiff);
            ELSE
                rTempGrad := rTempGrad + (matB[iIdx, mIdx] * vecQ_weight[iIdx] * rTempDiff);
            END_IF;
        END_FOR;

        (* Projected Gradient Descent Step: u_cand = u - gamma * grad *)
        rTempCandidate := trajU_mpc[kStep, mIdx] - (rPgd_StepSize * rTempGrad);

        (* Box Saturation Projection: [vecU_min, vecU_max] *)
        IF rTempCandidate > vecU_max[mIdx] THEN
            rTempCandidate := vecU_max[mIdx];
        ELSIF rTempCandidate < vecU_min[mIdx] THEN
            rTempCandidate := vecU_min[mIdx];
        END_IF;

        (* Slew Rate Clamping Projection *)
        IF kStep = 0 THEN
            rTempRate := rTempCandidate - vecU_prev[mIdx];
            IF rTempRate > vecU_slewMax[mIdx] THEN
                rTempCandidate := vecU_prev[mIdx] + vecU_slewMax[mIdx];
            ELSIF rTempRate < -vecU_slewMax[mIdx] THEN
                rTempCandidate := vecU_prev[mIdx] - vecU_slewMax[mIdx];
            END_IF;
        ELSE
            rTempRate := rTempCandidate - trajU_mpc[kStep - 1, mIdx];
            IF rTempRate > vecU_slewMax[mIdx] THEN
                rTempCandidate := trajU_mpc[kStep - 1, mIdx] + vecU_slewMax[mIdx];
            ELSIF rTempRate < -vecU_slewMax[mIdx] THEN
                rTempCandidate := trajU_mpc[kStep - 1, mIdx] - vecU_slewMax[mIdx];
            END_IF;
        END_IF;

        trajU_mpc[kStep, mIdx] := rTempCandidate;
    END_FOR;
END_FOR;
""")

    # Cost Function Computation & Optimal Actuator Vector Extraction
    parts.append("""
(* Compute Evaluated MPC Quadratic Objective Cost Function *)
rMpc_AccumulatedCost := 0.0;
FOR kStep := 0 TO 4 DO
    FOR iIdx := 0 TO 11 DO
        rTempDiff := trajX_mpc[kStep, iIdx] - vecX_target[iIdx];
        rMpc_AccumulatedCost := rMpc_AccumulatedCost + (vecQ_weight[iIdx] * rTempDiff * rTempDiff);
    END_FOR;
    FOR mIdx := 0 TO 7 DO
        rTempDiff := trajU_mpc[kStep, mIdx] - vecU_target[mIdx];
        rMpc_AccumulatedCost := rMpc_AccumulatedCost + (vecR_weight[mIdx] * rTempDiff * rTempDiff);
    END_FOR;
END_FOR;
FOR iIdx := 0 TO 11 DO
    rTempDiff := trajX_mpc[5, iIdx] - vecX_target[iIdx];
    rMpc_AccumulatedCost := rMpc_AccumulatedCost + (vecP_terminal[iIdx] * rTempDiff * rTempDiff);
END_FOR;
rMpc_ObjectiveCostMetric := rMpc_AccumulatedCost;

(* Extract First Horizon Control Action as Current Cycle Actuator Vector *)
FOR mIdx := 0 TO 7 DO
    vecU[mIdx] := trajU_mpc[0, mIdx];
END_FOR;
""")

    # PHASE 4: 14-Stage Deterministic Production Finite State Machine
    parts.append("""
(* ==================================================================================================== *)
(* PHASE 4: 14-STAGE DETERMINISTIC PRODUCTION FINITE STATE MACHINE (FSM)                                *)
(* Sequence:                                                                                            *)
(*   0: STATE_IDLE                                                                                      *)
(*   1: STATE_CHILLER_GLYCOL_PRECOOL_AND_PRESSURE_LOCK                                                 *)
(*   2: STATE_INSULATION_MONITORING_AND_PRECHARGE_RESISTOR_ENGAGE                                       *)
(*   3: STATE_DC_MAIN_CONTACTOR_CLOSING_SEQUENCE                                                        *)
(*   4: STATE_INVERTER_BLACK_START_GRID_FORMING_VOLTAGE_RAMP                                            *)
(*   5: STATE_GRID_SYNCHRONIZATION_AND_AC_BREAKER_CLOSE                                                 *)
(*   6: STATE_NOMINAL_BASELOAD_ENERGY_DISPATCH                                                          *)
(*   7: STATE_FAST_FREQUENCY_RESPONSE_INERTIA_SURGE                                                     *)
(*   8: STATE_VOLTAGE_SAG_LOW_VOLTAGE_RIDE_THROUGH_LVRT                                                 *)
(*   9: STATE_DYNAMIC_STRING_SOC_EQUALIZATION_BALANCING                                                 *)
(*   10: STATE_PEAK_THERMAL_COOLING_BOOST_CHILLER_MAX                                                   *)
(*   11: STATE_CONTROLLED_RAMPDOWN_AND_FLOAT_STANDBY                                                    *)
(*   12: STATE_POST_DISPATCH_REST_AND_OCV_RELAXATION                                                    *)
(*   13: STATE_EMERGENCY_THERMAL_RUNAWAY_OR_ARC_FLASH_TRIP                                              *)
(* ==================================================================================================== *)

(* Update Operational State Dwell Timers *)
IF eState = ePrevState THEN
    rStateTimer_s := rStateTimer_s + tScanCycleTime_s;
    rSubStateTimer_s := rSubStateTimer_s + tScanCycleTime_s;
ELSE
    rStateTimer_s := 0.0;
    rSubStateTimer_s := 0.0;
    iFsmStepIndex := 0;
    ePrevState := eState;
END_IF;

(* Continuous Thermal Runaway Severity Calculation (NFPA 855 Early Warning) *)
rThermalRunawaySeverity := (rOffGas_H2_CO_Voted / 50.0) * 0.60;
IF rBattery_CellMaxTemp_degC > 45.0 THEN
    rThermalRunawaySeverity := rThermalRunawaySeverity + ((rBattery_CellMaxTemp_degC - 45.0) / 30.0) * 0.40;
END_IF;

(* Global Emergency Trip Interlocks *)
IF bEmergencyStop OR rOffGas_HH_Active OR rCellTemp_HH_Active OR rInsul_LL_Active OR bDCLink_Volt_HH_Active THEN
    eState := 13; (* Immediate transition to Emergency Trip *)
END_IF;

CASE eState OF
    0: (* STATE_IDLE *)
        iActiveStateIndex := 0;
        bDC_PrechargeContactor_Cmd   := FALSE;
        bDC_MainContactor_Cmd        := FALSE;
        bAC_MainBreaker_CloseCmd     := FALSE;
        bAC_MainBreaker_TripCmd      := FALSE;
        rVSG_VirtualPowerCmd_P_MW    := 0.0;
        rVSG_VirtualVoltageCmd_E_kV  := 0.0;
        rChiller_CompressorVFD_RPM   := 0.0;
        rGlycol_CirculationPump_pct  := 0.0;
        rCoolingValve_String1_pct    := 0.0;
        rCoolingValve_String2_pct    := 0.0;
        rCoolingValve_String3_pct    := 0.0;
        rCoolingValve_String4_pct    := 0.0;
        rInverter_CoolingFan_pct     := 0.0;
        bFireSuppressionReleaseValve := FALSE;
        bBatteryRoomVentLouversOpen  := FALSE;
        bHVAC_EmergencyShutoff_Trip  := FALSE;

        (* Check Start Permissives *)
        IF bEnable AND bAutoDispatchStart AND NOT bEmergencyStop AND bEarthSwitch_OpenFb THEN
            eState := 1;
        END_IF;

    1: (* STATE_CHILLER_GLYCOL_PRECOOL_AND_PRESSURE_LOCK *)
        iActiveStateIndex := 1;
        rGlycol_CirculationPump_pct := 75.0;
        rCoolingValve_String1_pct   := 100.0;
        rCoolingValve_String2_pct   := 100.0;
        rCoolingValve_String3_pct   := 100.0;
        rCoolingValve_String4_pct   := 100.0;
        rChiller_CompressorVFD_RPM  := 2200.0;

        (* Verify Coolant Loop Pressure & Flow *)
        IF rStateTimer_s > 5.0 THEN
            IF rGlycol_ManifoldPressure_bar >= 1.5 AND rGlycol_ManifoldPressure_bar <= 3.8 THEN
                IF rGlycol_CoolantFlow_m3h >= 45.0 THEN
                    IF rBattery_CellMaxTemp_degC <= 26.0 OR rStateTimer_s > 15.0 THEN
                        eState := 2;
                    END_IF;
                END_IF;
            END_IF;
        END_IF;

    2: (* STATE_INSULATION_MONITORING_AND_PRECHARGE_RESISTOR_ENGAGE *)
        iActiveStateIndex := 2;
        (* Verify DC Ground Insulation Resistance *)
        IF rInsulation_Resistance_kOhm < 500.0 THEN
            eState := 13; (* Ground fault detected, abort start *)
        ELSE
            (* Engage Precharge Resistor Circuit *)
            bDC_PrechargeContactor_Cmd := TRUE;
            bDC_MainContactor_Cmd      := FALSE;

            (* Precharge Voltage Matching: DC bus must reach >= 95% of Battery String Voltage *)
            IF rDCLink_Voltage_Voted >= 1425.0 AND rStateTimer_s > 2.5 THEN
                bPrechargeComplete := TRUE;
                eState := 3;
            ELSIF rStateTimer_s > 8.0 THEN
                (* Precharge Timeout Fault *)
                eState := 13;
            END_IF;
        END_IF;

    3: (* STATE_DC_MAIN_CONTACTOR_CLOSING_SEQUENCE *)
        iActiveStateIndex := 3;
        bDC_MainContactor_Cmd := TRUE;

        (* Once Main Contactor Feedback is Verified, Safely Open Precharge Contactor *)
        IF bDC_MainContactor_ClosedFb AND rStateTimer_s > 0.50 THEN
            bDC_PrechargeContactor_Cmd := FALSE;
            IF rStateTimer_s > 1.50 THEN
                IF bBlackStartPermissive THEN
                    eState := 4; (* Inverter Black Start *)
                ELSE
                    eState := 5; (* Direct Grid Synchronization *)
                END_IF;
            END_IF;
        ELSIF rStateTimer_s > 5.0 THEN
            eState := 13; (* Main contactor failed to close *)
        END_IF;

    4: (* STATE_INVERTER_BLACK_START_GRID_FORMING_VOLTAGE_RAMP *)
        iActiveStateIndex := 4;
        (* Soft-Ramp Virtual Back-EMF Voltage from 0.0 to 34.5 kV at 2.5 kV/s *)
        IF rVSG_VirtualVoltageCmd_E_kV < 34.5 THEN
            rVSG_VirtualVoltageCmd_E_kV := MIN(34.5, rVSG_VirtualVoltageCmd_E_kV + (tScanCycleTime_s * 2.5));
        END_IF;
        rVSG_VirtualPowerCmd_P_MW := 0.0;

        (* Voltage Stability Verified *)
        IF rVSG_VirtualVoltageCmd_E_kV >= 34.4 AND rStateTimer_s > 15.0 THEN
            eState := 5;
        END_IF;

    5: (* STATE_GRID_SYNCHRONIZATION_AND_AC_BREAKER_CLOSE *)
        iActiveStateIndex := 5;
        (* Active Synchrocheck Comparison Across Open AC Vacuum Breaker *)
        rSyncAngleDiff_deg  := ABS(rVSG_RotorAngle_delta * 57.2957795);
        rSyncVoltageDiff_kV := ABS(rVSG_VirtualVoltageCmd_E_kV - rPCC_Voltage_Voted);
        rSyncFreqDiff_Hz    := ABS((rVSG_RotorSpeed_omega * 0.159155) - rPCC_Frequency_Voted);

        (* Active Virtual Governor & Exciter Adjustment to Drive Slip to Zero *)
        IF rSyncVoltageDiff_kV > 0.10 THEN
            rVSG_VirtualVoltageCmd_E_kV := rVSG_VirtualVoltageCmd_E_kV + (0.05 * (rPCC_Voltage_Voted - rVSG_VirtualVoltageCmd_E_kV));
        END_IF;

        (* Synchrocheck Window: Angle <= 3.0 deg, Voltage <= 0.35 kV, Slip <= 0.05 Hz *)
        IF rSyncAngleDiff_deg <= 3.0 AND rSyncVoltageDiff_kV <= 0.35 AND rSyncFreqDiff_Hz <= 0.05 THEN
            bSyncCriteriaMet := TRUE;
            bAC_MainBreaker_CloseCmd := TRUE;
            IF bAC_MainBreaker_ClosedFb THEN
                bAC_MainBreaker_CloseCmd := FALSE;
                eState := 6; (* Enter Baseload Dispatch *)
            END_IF;
        ELSE
            bSyncCriteriaMet := FALSE;
            bAC_MainBreaker_CloseCmd := FALSE;
        END_IF;

        IF rStateTimer_s > 30.0 THEN
            (* Synchronization Timeout *)
            eState := 11;
        END_IF;

    6: (* STATE_NOMINAL_BASELOAD_ENERGY_DISPATCH *)
        iActiveStateIndex := 6;
        (* Actuator Commands Dispatched Directly from Receding-Horizon MPC *)
        rVSG_VirtualPowerCmd_P_MW   := vecU[0] + rVSG_SyntheticInertiaPower_MW + rVSG_FrequencyDroopPower_MW;
        rVSG_VirtualVoltageCmd_E_kV := vecU[1] + (rVSG_VoltageDroopReactive_MVAr * 0.025);
        rPCC_ActivePower_Actual_MW  := rVSG_VirtualPowerCmd_P_MW;
        rPCC_ReactivePower_Actual_MVAr := rVSG_VoltageDroopReactive_MVAr;

        (* Closed-Loop Thermal & String Balancing Commands *)
        rCoolingValve_String1_pct := 65.0 + (rString1_SoC_Dev * 2.0);
        rCoolingValve_String2_pct := 65.0 + (rString2_SoC_Dev * 2.0);
        rCoolingValve_String3_pct := 65.0 + (rString3_SoC_Dev * 2.0);
        rCoolingValve_String4_pct := 65.0 + (rString4_SoC_Dev * 2.0);
        rInverter_CoolingFan_pct  := 70.0;

        (* Dynamic Transitions to Contingency States *)
        IF ABS(rGrid_RoCoF_Hz_per_s) > 0.40 OR ABS(rPCC_Frequency_Voted - rGrid_NominalFrequency_Hz) > 0.25 THEN
            eState := 7; (* Fast Frequency Response Inertia Surge *)
        ELSIF rPCC_Voltage_Voted < (rGrid_NominalVoltage_kV * 0.90) THEN
            eState := 8; (* Low Voltage Ride-Through *)
        ELSIF ABS(rString1_SoC_Dev) > 3.0 OR ABS(rString2_SoC_Dev) > 3.0 OR ABS(rString3_SoC_Dev) > 3.0 OR ABS(rString4_SoC_Dev) > 3.0 THEN
            eState := 9; (* String SoC Equalization Balancing *)
        ELSIF rBattery_CellMaxTemp_degC > 38.0 OR rThermal_RackGradient_DeltaT > 4.0 THEN
            eState := 10; (* Peak Thermal Cooling Boost *)
        ELSIF bControlledStop OR NOT bEnable THEN
            eState := 11; (* Controlled Rampdown *)
        END_IF;

    7: (* STATE_FAST_FREQUENCY_RESPONSE_INERTIA_SURGE *)
        iActiveStateIndex := 7;
        (* Deliver Up to 140 MW Peak Surge for Primary Grid Frequency Arrest *)
        rVSG_VirtualPowerCmd_P_MW := vecU[0] + (rVSG_SyntheticInertiaPower_MW * 1.5) + (rVSG_FrequencyDroopPower_MW * 1.25);
        IF rVSG_VirtualPowerCmd_P_MW > 140.0 THEN
            rVSG_VirtualPowerCmd_P_MW := 140.0;
        ELSIF rVSG_VirtualPowerCmd_P_MW < -140.0 THEN
            rVSG_VirtualPowerCmd_P_MW := -140.0;
        END_IF;

        (* Return to Baseload once Frequency Stabilizes *)
        IF ABS(rPCC_Frequency_Voted - rGrid_NominalFrequency_Hz) <= 0.05 AND ABS(rGrid_RoCoF_Hz_per_s) <= 0.08 THEN
            IF rStateTimer_s > 3.0 THEN
                eState := 6;
            END_IF;
        ELSIF rStateTimer_s > 15.0 THEN
            (* Inertia Surge Thermal Limit Timeout *)
            eState := 6;
        END_IF;

    8: (* STATE_VOLTAGE_SAG_LOW_VOLTAGE_RIDE_THROUGH_LVRT *)
        iActiveStateIndex := 8;
        (* Grid Code Compliant Reactive Current Injection under Severe Sag *)
        rLVRT_SagDepth_pct := (rGrid_NominalVoltage_kV - rPCC_Voltage_Voted) / rGrid_NominalVoltage_kV * 100.0;
        rLVRT_ReactiveBoost_MVAr := 2.0 * (rLVRT_SagDepth_pct / 100.0) * 60.0; (* 2.0 p.u. reactive current slope *)
        IF rLVRT_ReactiveBoost_MVAr > 60.0 THEN
            rLVRT_ReactiveBoost_MVAr := 60.0;
        END_IF;
        rVSG_VoltageDroopReactive_MVAr := rLVRT_ReactiveBoost_MVAr;
        rVSG_VirtualPowerCmd_P_MW := MAX(0.0, rDispatch_ActivePower_MW * (rPCC_Voltage_Voted / rGrid_NominalVoltage_kV));

        (* Voltage Sag Recovery *)
        IF rPCC_Voltage_Voted >= (rGrid_NominalVoltage_kV * 0.90) THEN
            IF rStateTimer_s > 0.50 THEN
                eState := 6;
            END_IF;
        ELSIF rStateTimer_s > 3.0 THEN
            (* Severe Sag Duration Exceeded Standard LVRT Boundary -> Trip *)
            eState := 13;
        END_IF;

    9: (* STATE_DYNAMIC_STRING_SOC_EQUALIZATION_BALANCING *)
        iActiveStateIndex := 9;
        (* High-Gain DC-DC Converter Current Trim Modulation *)
        rString1_CurrentTrimCmd_A := 25.0 * rString1_SoC_Dev;
        rString2_CurrentTrimCmd_A := 25.0 * rString2_SoC_Dev;
        rString3_CurrentTrimCmd_A := 25.0 * rString3_SoC_Dev;
        rString4_CurrentTrimCmd_A := 25.0 * rString4_SoC_Dev;

        (* Check Convergence Criteria: All deviations <= 0.5% *)
        IF ABS(rString1_SoC_Dev) <= 0.5 AND ABS(rString2_SoC_Dev) <= 0.5 AND ABS(rString3_SoC_Dev) <= 0.5 AND ABS(rString4_SoC_Dev) <= 0.5 THEN
            IF rStateTimer_s > 10.0 THEN
                eState := 6;
            END_IF;
        ELSIF rStateTimer_s > 120.0 THEN
            eState := 6; (* Maximum Balancing Window Complete *)
        END_IF;

    10: (* STATE_PEAK_THERMAL_COOLING_BOOST_CHILLER_MAX *)
        iActiveStateIndex := 10;
        rChiller_CompressorVFD_RPM  := 4500.0; (* Max Chiller Speed *)
        rGlycol_CirculationPump_pct := 100.0;  (* Max Flow *)
        rCoolingValve_String1_pct   := 100.0;
        rCoolingValve_String2_pct   := 100.0;
        rCoolingValve_String3_pct   := 100.0;
        rCoolingValve_String4_pct   := 100.0;
        rInverter_CoolingFan_pct    := 100.0;

        (* Derate Active Power Dispatch if Core Temp Exceeds 45 deg C *)
        IF rBattery_CellMaxTemp_degC > 45.0 THEN
            rVSG_VirtualPowerCmd_P_MW := rDispatch_ActivePower_MW * 0.50;
        END_IF;

        (* Thermal Clearance Check *)
        IF rBattery_CellMaxTemp_degC <= 30.0 AND rThermal_RackGradient_DeltaT <= 2.5 THEN
            IF rStateTimer_s > 30.0 THEN
                eState := 6;
            END_IF;
        END_IF;

    11: (* STATE_CONTROLLED_RAMPDOWN_AND_FLOAT_STANDBY *)
        iActiveStateIndex := 11;
        (* Smoothly Ramp Active Power to 0.0 MW at 5.0 MW/s *)
        IF rVSG_VirtualPowerCmd_P_MW > 0.0 THEN
            rVSG_VirtualPowerCmd_P_MW := MAX(0.0, rVSG_VirtualPowerCmd_P_MW - (tScanCycleTime_s * 5.0));
        ELSIF rVSG_VirtualPowerCmd_P_MW < 0.0 THEN
            rVSG_VirtualPowerCmd_P_MW := MIN(0.0, rVSG_VirtualPowerCmd_P_MW + (tScanCycleTime_s * 5.0));
        END_IF;

        (* Once Power is Zero, Open AC Main Breaker *)
        IF ABS(rVSG_VirtualPowerCmd_P_MW) <= 0.10 THEN
            bAC_MainBreaker_CloseCmd := FALSE;
            IF NOT bAC_MainBreaker_ClosedFb OR rStateTimer_s > 5.0 THEN
                eState := 12;
            END_IF;
        END_IF;

    12: (* STATE_POST_DISPATCH_REST_AND_OCV_RELAXATION *)
        iActiveStateIndex := 12;
        bDC_MainContactor_Cmd      := FALSE;
        bDC_PrechargeContactor_Cmd := FALSE;
        rVSG_VirtualVoltageCmd_E_kV := 0.0;

        (* Maintain Low Coolant Flow for 5 Minutes to Dissipate Residual Core Heat *)
        rGlycol_CirculationPump_pct := 30.0;
        rChiller_CompressorVFD_RPM  := 1200.0;

        IF rStateTimer_s > 300.0 THEN
            eState := 0; (* Return to Idle Standby *)
        END_IF;

    13: (* STATE_EMERGENCY_THERMAL_RUNAWAY_OR_ARC_FLASH_TRIP *)
        iActiveStateIndex := 13;
        (* Immediate Cat-4 Safety Shutdown *)
        bAC_MainBreaker_TripCmd      := TRUE;
        bAC_MainBreaker_CloseCmd     := FALSE;
        bDC_MainContactor_Cmd        := FALSE;
        bDC_PrechargeContactor_Cmd   := FALSE;
        rVSG_VirtualPowerCmd_P_MW    := 0.0;
        rVSG_VirtualVoltageCmd_E_kV  := 0.0;
        rChiller_CompressorVFD_RPM   := 0.0;
        rGlycol_CirculationPump_pct  := 0.0;
        bHVAC_EmergencyShutoff_Trip  := TRUE;

        (* If Severe Thermal Runaway or Explosive Off-Gas Detected -> Discharge Deluge *)
        IF rOffGas_HH_Active OR rCellTemp_HH_Active OR rThermalRunawaySeverity > 0.85 THEN
            bThermalRunawayLatched := TRUE;
            bFireSuppressionReleaseValve := TRUE;
            bBatteryRoomVentLouversOpen  := TRUE;
        END_IF;

        (* Manual Reset Only when Safe *)
        IF bFaultReset AND NOT bEmergencyStop AND NOT rOffGas_HH_Active AND NOT rCellTemp_HH_Active THEN
            bThermalRunawayLatched       := FALSE;
            bFireSuppressionReleaseValve := FALSE;
            bBatteryRoomVentLouversOpen  := FALSE;
            bHVAC_EmergencyShutoff_Trip  := FALSE;
            bAC_MainBreaker_TripCmd      := FALSE;
            eState := 0;
        END_IF;
END_CASE;
""")

    # PHASE 5: ISA-18.2 Process Alarms & 32-Bit Telemetry Status Words
    parts.append("""
(* ==================================================================================================== *)
(* PHASE 5: ISA-18.2 MULTI-TIER PROCESS ALARMS & BIT-PACKED STATUS WORDS                                *)
(* Multi-Tier Process Alarms (HH, H, L, LL) with Clearance Deadbands & First-Out Latching Engine        *)
(* ==================================================================================================== *)

(* PCC Grid Voltage Alarms *)
IF rPCC_Voltage_Voted >= rPCC_Volt_HH_Limit_kV THEN
    bPCC_Volt_HH_Active := TRUE;
ELSIF rPCC_Voltage_Voted <= (rPCC_Volt_HH_Limit_kV - rPCC_Volt_Deadband_kV) THEN
    bPCC_Volt_HH_Active := FALSE;
END_IF;

IF rPCC_Voltage_Voted >= rPCC_Volt_H_Limit_kV THEN
    bPCC_Volt_H_Active := TRUE;
ELSIF rPCC_Voltage_Voted <= (rPCC_Volt_H_Limit_kV - rPCC_Volt_Deadband_kV) THEN
    bPCC_Volt_H_Active := FALSE;
END_IF;

IF rPCC_Voltage_Voted <= rPCC_Volt_LL_Limit_kV THEN
    bPCC_Volt_LL_Active := TRUE;
ELSIF rPCC_Voltage_Voted >= (rPCC_Volt_LL_Limit_kV + rPCC_Volt_Deadband_kV) THEN
    bPCC_Volt_LL_Active := FALSE;
END_IF;

IF rPCC_Voltage_Voted <= rPCC_Volt_L_Limit_kV THEN
    bPCC_Volt_L_Active := TRUE;
ELSIF rPCC_Voltage_Voted >= (rPCC_Volt_L_Limit_kV + rPCC_Volt_Deadband_kV) THEN
    bPCC_Volt_L_Active := FALSE;
END_IF;

(* PCC Grid Frequency Alarms *)
IF rPCC_Frequency_Voted >= rPCC_Freq_HH_Limit_Hz THEN
    bPCC_Freq_HH_Active := TRUE;
ELSIF rPCC_Frequency_Voted <= (rPCC_Freq_HH_Limit_Hz - rPCC_Freq_Deadband_Hz) THEN
    bPCC_Freq_HH_Active := FALSE;
END_IF;

IF rPCC_Frequency_Voted >= rPCC_Freq_H_Limit_Hz THEN
    bPCC_Freq_H_Active := TRUE;
ELSIF rPCC_Frequency_Voted <= (rPCC_Freq_H_Limit_Hz - rPCC_Freq_Deadband_Hz) THEN
    bPCC_Freq_H_Active := FALSE;
END_IF;

IF rPCC_Frequency_Voted <= rPCC_Freq_LL_Limit_Hz THEN
    bPCC_Freq_LL_Active := TRUE;
ELSIF rPCC_Frequency_Voted >= (rPCC_Freq_LL_Limit_Hz + rPCC_Freq_Deadband_Hz) THEN
    bPCC_Freq_LL_Active := FALSE;
END_IF;

IF rPCC_Frequency_Voted <= rPCC_Freq_L_Limit_Hz THEN
    bPCC_Freq_L_Active := TRUE;
ELSIF rPCC_Frequency_Voted >= (rPCC_Freq_L_Limit_Hz + rPCC_Freq_Deadband_Hz) THEN
    bPCC_Freq_L_Active := FALSE;
END_IF;

(* DC Link Voltage Alarms *)
IF rDCLink_Voltage_Voted >= rDCLink_Volt_HH_Limit_V THEN
    bDCLink_Volt_HH_Active := TRUE;
ELSIF rDCLink_Voltage_Voted <= (rDCLink_Volt_HH_Limit_V - rDCLink_Volt_Deadband_V) THEN
    bDCLink_Volt_HH_Active := FALSE;
END_IF;

IF rDCLink_Voltage_Voted >= rDCLink_Volt_H_Limit_V THEN
    bDCLink_Volt_H_Active := TRUE;
ELSIF rDCLink_Voltage_Voted <= (rDCLink_Volt_H_Limit_V - rDCLink_Volt_Deadband_V) THEN
    bDCLink_Volt_H_Active := FALSE;
END_IF;

IF rDCLink_Voltage_Voted <= rDCLink_Volt_LL_Limit_V THEN
    bDCLink_Volt_LL_Active := TRUE;
ELSIF rDCLink_Voltage_Voted >= (rDCLink_Volt_LL_Limit_V + rDCLink_Volt_Deadband_V) THEN
    bDCLink_Volt_LL_Active := FALSE;
END_IF;

IF rDCLink_Voltage_Voted <= rDCLink_Volt_L_Limit_V THEN
    bDCLink_Volt_L_Active := TRUE;
ELSIF rDCLink_Voltage_Voted >= (rDCLink_Volt_L_Limit_V + rDCLink_Volt_Deadband_V) THEN
    bDCLink_Volt_L_Active := FALSE;
END_IF;

(* Battery Module Core Cell Temperature Alarms *)
IF rBattery_CellMaxTemp_degC >= rCellTemp_HH_Limit_degC THEN
    rCellTemp_HH_Active := TRUE;
ELSIF rBattery_CellMaxTemp_degC <= (rCellTemp_HH_Limit_degC - rCellTemp_Deadband_degC) THEN
    rCellTemp_HH_Active := FALSE;
END_IF;

IF rBattery_CellMaxTemp_degC >= rCellTemp_H_Limit_degC THEN
    rCellTemp_H_Active := TRUE;
ELSIF rBattery_CellMaxTemp_degC <= (rCellTemp_H_Limit_degC - rCellTemp_Deadband_degC) THEN
    rCellTemp_H_Active := FALSE;
END_IF;

IF rBattery_CellMinTemp_degC <= rCellTemp_LL_Limit_degC THEN
    rCellTemp_LL_Active := TRUE;
ELSIF rBattery_CellMinTemp_degC >= (rCellTemp_LL_Limit_degC + rCellTemp_Deadband_degC) THEN
    rCellTemp_LL_Active := FALSE;
END_IF;

IF rBattery_CellMinTemp_degC <= rCellTemp_L_Limit_degC THEN
    rCellTemp_L_Active := TRUE;
ELSIF rBattery_CellMinTemp_degC >= (rCellTemp_L_Limit_degC + rCellTemp_Deadband_degC) THEN
    rCellTemp_L_Active := FALSE;
END_IF;

(* Inter-Rack Thermal Gradient Alarms *)
IF rThermal_RackGradient_DeltaT >= rGradient_HH_Limit_degC THEN
    rGradient_HH_Active := TRUE;
ELSIF rThermal_RackGradient_DeltaT <= (rGradient_HH_Limit_degC - rGradient_Deadband_degC) THEN
    rGradient_HH_Active := FALSE;
END_IF;

IF rThermal_RackGradient_DeltaT >= rGradient_H_Limit_degC THEN
    rGradient_H_Active := TRUE;
ELSIF rThermal_RackGradient_DeltaT <= (rGradient_H_Limit_degC - rGradient_Deadband_degC) THEN
    rGradient_H_Active := FALSE;
END_IF;

(* Battery Off-Gas Multi-Gas Sensing Alarms *)
IF rOffGas_H2_CO_Voted >= rOffGas_HH_Limit_ppm THEN
    rOffGas_HH_Active := TRUE;
ELSIF rOffGas_H2_CO_Voted <= (rOffGas_HH_Limit_ppm - rOffGas_Deadband_ppm) THEN
    rOffGas_HH_Active := FALSE;
END_IF;

IF rOffGas_H2_CO_Voted >= rOffGas_H_Limit_ppm THEN
    rOffGas_H_Active := TRUE;
ELSIF rOffGas_H2_CO_Voted <= (rOffGas_H_Limit_ppm - rOffGas_Deadband_ppm) THEN
    rOffGas_H_Active := FALSE;
END_IF;

(* DC Ground Insulation Resistance Alarms *)
IF rInsulation_Resistance_kOhm <= rInsul_LL_Limit_kOhm THEN
    rInsul_LL_Active := TRUE;
ELSIF rInsulation_Resistance_kOhm >= (rInsul_LL_Limit_kOhm + rInsul_Deadband_kOhm) THEN
    rInsul_LL_Active := FALSE;
END_IF;

IF rInsulation_Resistance_kOhm <= rInsul_L_Limit_kOhm THEN
    rInsul_L_Active := TRUE;
ELSIF rInsulation_Resistance_kOhm >= (rInsul_L_Limit_kOhm + rInsul_Deadband_kOhm) THEN
    rInsul_L_Active := FALSE;
END_IF;

(* Coolant Circulation Flow Alarms *)
IF rGlycol_CoolantFlow_m3h <= rFlow_LL_Limit_m3h THEN
    rFlow_LL_Active := TRUE;
ELSIF rGlycol_CoolantFlow_m3h >= (rFlow_LL_Limit_m3h + rFlow_Deadband_m3h) THEN
    rFlow_LL_Active := FALSE;
END_IF;

IF rGlycol_CoolantFlow_m3h <= rFlow_L_Limit_m3h THEN
    rFlow_L_Active := TRUE;
ELSIF rGlycol_CoolantFlow_m3h >= (rFlow_L_Limit_m3h + rFlow_Deadband_m3h) THEN
    rFlow_L_Active := FALSE;
END_IF;

(* Inverter Phase Leg IGBT Temperature Alarms *)
IF rInverter_IGBT_MaxTemp_degC >= rIGBT_Temp_HH_Limit_degC THEN
    rIGBT_Temp_HH_Active := TRUE;
ELSIF rInverter_IGBT_MaxTemp_degC <= (rIGBT_Temp_HH_Limit_degC - rIGBT_Temp_Deadband_degC) THEN
    rIGBT_Temp_HH_Active := FALSE;
END_IF;

IF rInverter_IGBT_MaxTemp_degC >= rIGBT_Temp_H_Limit_degC THEN
    rIGBT_Temp_H_Active := TRUE;
ELSIF rInverter_IGBT_MaxTemp_degC <= (rIGBT_Temp_H_Limit_degC - rIGBT_Temp_Deadband_degC) THEN
    rIGBT_Temp_H_Active := FALSE;
END_IF;

(* First-Out Latching Identification Engine *)
IF NOT bFirstOutLatched THEN
    IF bEmergencyStop THEN
        bFirstOutLatched := TRUE;
        dwFirstOutCapturedCode := 16#00000001; (* Emergency Pushbutton *)
    ELSIF rOffGas_HH_Active THEN
        bFirstOutLatched := TRUE;
        dwFirstOutCapturedCode := 16#00000002; (* Battery Off-Gas HH Trip *)
    ELSIF rCellTemp_HH_Active THEN
        bFirstOutLatched := TRUE;
        dwFirstOutCapturedCode := 16#00000004; (* Core Cell Temp HH Trip *)
    ELSIF rInsul_LL_Active THEN
        bFirstOutLatched := TRUE;
        dwFirstOutCapturedCode := 16#00000008; (* DC Bus Ground Fault LL *)
    ELSIF bDCLink_Volt_HH_Active THEN
        bFirstOutLatched := TRUE;
        dwFirstOutCapturedCode := 16#00000010; (* DC Link Overvoltage HH *)
    ELSIF bDCLink_Volt_LL_Active THEN
        bFirstOutLatched := TRUE;
        dwFirstOutCapturedCode := 16#00000020; (* DC Link Undervoltage LL *)
    ELSIF bPCC_Volt_HH_Active THEN
        bFirstOutLatched := TRUE;
        dwFirstOutCapturedCode := 16#00000040; (* PCC Grid Voltage HH *)
    ELSIF bPCC_Volt_LL_Active THEN
        bFirstOutLatched := TRUE;
        dwFirstOutCapturedCode := 16#00000080; (* PCC Grid Voltage LL *)
    ELSIF bPCC_Freq_HH_Active THEN
        bFirstOutLatched := TRUE;
        dwFirstOutCapturedCode := 16#00000100; (* Grid Frequency HH *)
    ELSIF bPCC_Freq_LL_Active THEN
        bFirstOutLatched := TRUE;
        dwFirstOutCapturedCode := 16#00000200; (* Grid Frequency LL *)
    ELSIF rIGBT_Temp_HH_Active THEN
        bFirstOutLatched := TRUE;
        dwFirstOutCapturedCode := 16#00000400; (* Inverter IGBT Temp HH *)
    ELSIF rFlow_LL_Active THEN
        bFirstOutLatched := TRUE;
        dwFirstOutCapturedCode := 16#00000800; (* Coolant Flow Loss LL *)
    END_IF;
END_IF;

IF bFaultReset THEN
    bFirstOutLatched := FALSE;
    dwFirstOutCapturedCode := 16#00000000;
END_IF;
dwFirstOutWord := dwFirstOutCapturedCode;

(* ---------------------------------------------------------------------------------------------------- *)
(* 32-Bit Bit-Packed Telemetry Status Words                                                             *)
(* ---------------------------------------------------------------------------------------------------- *)
(* StatusWord1: BESS Operational Subsystem & Inverter State Bits *)
dwStatusWord1 := 16#00000000;
IF bEnable THEN dwStatusWord1 := dwStatusWord1 OR 16#00000001; END_IF;
IF bAC_MainBreaker_ClosedFb THEN dwStatusWord1 := dwStatusWord1 OR 16#00000002; END_IF;
IF bDC_MainContactor_ClosedFb THEN dwStatusWord1 := dwStatusWord1 OR 16#00000004; END_IF;
IF bDC_PrechargeContactor_ClosedFb THEN dwStatusWord1 := dwStatusWord1 OR 16#00000008; END_IF;
IF bPrechargeComplete THEN dwStatusWord1 := dwStatusWord1 OR 16#00000010; END_IF;
IF bSyncCriteriaMet THEN dwStatusWord1 := dwStatusWord1 OR 16#00000020; END_IF;
IF bChillerSkidReady THEN dwStatusWord1 := dwStatusWord1 OR 16#00000040; END_IF;
IF bFireSuppressionDelugeArmed THEN dwStatusWord1 := dwStatusWord1 OR 16#00000080; END_IF;
IF bInverterHeartbeatOk THEN dwStatusWord1 := dwStatusWord1 OR 16#00000100; END_IF;
IF bEarthSwitch_OpenFb THEN dwStatusWord1 := dwStatusWord1 OR 16#00000200; END_IF;
IF eState = 6 THEN dwStatusWord1 := dwStatusWord1 OR 16#00000400; END_IF; (* Baseload Dispatch Active *)
IF eState = 7 THEN dwStatusWord1 := dwStatusWord1 OR 16#00000800; END_IF; (* Synthetic Inertia Active *)
IF eState = 8 THEN dwStatusWord1 := dwStatusWord1 OR 16#00001000; END_IF; (* LVRT Active *)
IF eState = 9 THEN dwStatusWord1 := dwStatusWord1 OR 16#00002000; END_IF; (* String Balancing Active *)
IF eState = 10 THEN dwStatusWord1 := dwStatusWord1 OR 16#00004000; END_IF; (* Chiller Max Boost Active *)
IF eState = 13 THEN dwStatusWord1 := dwStatusWord1 OR 16#00008000; END_IF; (* Emergency Tripped *)

(* StatusWord2: 2oo3 TMR Channel Health & Sensor Status Bits *)
dwStatusWord2 := 16#00000000;
IF bPCC_Voltage_HealthA AND bPCC_Voltage_HealthB AND bPCC_Voltage_HealthC THEN dwStatusWord2 := dwStatusWord2 OR 16#00000001; END_IF;
IF bPCC_Voltage_Degraded THEN dwStatusWord2 := dwStatusWord2 OR 16#00000002; END_IF;
IF bPCC_Voltage_SingleFallback THEN dwStatusWord2 := dwStatusWord2 OR 16#00000004; END_IF;
IF bPCC_Voltage_Trip THEN dwStatusWord2 := dwStatusWord2 OR 16#00000008; END_IF;

IF bPCC_Frequency_HealthA AND bPCC_Frequency_HealthB AND bPCC_Frequency_HealthC THEN dwStatusWord2 := dwStatusWord2 OR 16#00000010; END_IF;
IF bPCC_Frequency_Degraded THEN dwStatusWord2 := dwStatusWord2 OR 16#00000020; END_IF;
IF bPCC_Frequency_SingleFallback THEN dwStatusWord2 := dwStatusWord2 OR 16#00000040; END_IF;
IF bPCC_Frequency_Trip THEN dwStatusWord2 := dwStatusWord2 OR 16#00000080; END_IF;

IF bDCLink_Voltage_HealthA AND bDCLink_Voltage_HealthB AND bDCLink_Voltage_HealthC THEN dwStatusWord2 := dwStatusWord2 OR 16#00000100; END_IF;
IF bDCLink_Voltage_Degraded THEN dwStatusWord2 := dwStatusWord2 OR 16#00000200; END_IF;
IF bDCLink_Voltage_SingleFallback THEN dwStatusWord2 := dwStatusWord2 OR 16#00000400; END_IF;
IF bDCLink_Voltage_Trip THEN dwStatusWord2 := dwStatusWord2 OR 16#00000800; END_IF;

IF bOffGas_HealthA AND bOffGas_HealthB AND bOffGas_HealthC THEN dwStatusWord2 := dwStatusWord2 OR 16#00001000; END_IF;
IF bOffGas_Degraded THEN dwStatusWord2 := dwStatusWord2 OR 16#00002000; END_IF;
IF bOffGas_SingleFallback THEN dwStatusWord2 := dwStatusWord2 OR 16#00004000; END_IF;
IF bOffGas_Trip THEN dwStatusWord2 := dwStatusWord2 OR 16#00008000; END_IF;

(* AlarmWord1: ISA-18.2 Critical Emergency Trips (HH / LL) *)
dwAlarmWord1 := 16#00000000;
IF bPCC_Volt_HH_Active THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000001; END_IF;
IF bPCC_Volt_LL_Active THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000002; END_IF;
IF bPCC_Freq_HH_Active THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000004; END_IF;
IF bPCC_Freq_LL_Active THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000008; END_IF;
IF bDCLink_Volt_HH_Active THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000010; END_IF;
IF bDCLink_Volt_LL_Active THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000020; END_IF;
IF rCellTemp_HH_Active THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000040; END_IF;
IF rCellTemp_LL_Active THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000080; END_IF;
IF rGradient_HH_Active THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000100; END_IF;
IF rOffGas_HH_Active THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000200; END_IF;
IF rInsul_LL_Active THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000400; END_IF;
IF rFlow_LL_Active THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000800; END_IF;
IF rIGBT_Temp_HH_Active THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00001000; END_IF;
IF bThermalRunawayLatched THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00002000; END_IF;

(* AlarmWord2: ISA-18.2 Process High/Low Warnings & Advisories (H / L) *)
dwAlarmWord2 := 16#00000000;
IF bPCC_Volt_H_Active THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000001; END_IF;
IF bPCC_Volt_L_Active THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000002; END_IF;
IF bPCC_Freq_H_Active THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000004; END_IF;
IF bPCC_Freq_L_Active THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000008; END_IF;
IF bDCLink_Volt_H_Active THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000010; END_IF;
IF bDCLink_Volt_L_Active THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000020; END_IF;
IF rCellTemp_H_Active THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000040; END_IF;
IF rCellTemp_L_Active THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000080; END_IF;
IF rGradient_H_Active THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000100; END_IF;
IF rOffGas_H_Active THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000200; END_IF;
IF rInsul_L_Active THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000400; END_IF;
IF rFlow_L_Active THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000800; END_IF;
IF rIGBT_Temp_H_Active THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00001000; END_IF;
""")

    # PHASE 6: Physical Actuator Clamping, Slew Rate Updates & Final Bookkeeping
    parts.append("""
(* ==================================================================================================== *)
(* PHASE 6: PHYSICAL ACTUATOR CLAMPING & EXECUTION CYCLE BOOKKEEPING                                   *)
(* Slew Rate Clamping, Actuator Saturation & History Buffer Propagation                                 *)
(* ==================================================================================================== *)

(* Slew-Rate Limiting on Active Power Virtual Machine Command *)
rTempDiff := rVSG_VirtualPowerCmd_P_MW - vecU_prev[0];
IF rTempDiff > vecU_slewMax[0] THEN
    rVSG_VirtualPowerCmd_P_MW := vecU_prev[0] + vecU_slewMax[0];
ELSIF rTempDiff < -vecU_slewMax[0] THEN
    rVSG_VirtualPowerCmd_P_MW := vecU_prev[0] - vecU_slewMax[0];
END_IF;

(* Expose Virtual Synchronous Rotor States *)
rVSG_RotorAngle_delta_rad  := rVSG_RotorAngle_delta;
rVSG_RotorSpeed_omega_rads := rVSG_RotorSpeed_omega;

(* Save Actuator State History for Slew Penalties in Next Execution Scan *)
FOR mIdx := 0 TO 7 DO
    vecU_prev[mIdx] := vecU[mIdx];
END_FOR;

(* Increment Execution Cycle Counter *)
iCycleCounter := iCycleCounter + 1;

END_FUNCTION_BLOCK
""")

    full_code = "".join(parts)
    return full_code

if __name__ == "__main__":
    code = generate_iec_st()
    print("Generated ST code character count:", len(code))
    
    # Check delimiters in code
    no_comments = re.sub(r'\(\*[\s\S]*?\*\)', '', code)
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
    
    print(f"Delimiters parity check:")
    print(f"  IF: {ifs} | END_IF: {end_ifs} (Match: {ifs == end_ifs})")
    print(f"  CASE: {cases} | END_CASE: {end_cases} (Match: {cases == end_cases})")
    print(f"  FOR: {fors} | END_FOR: {end_fors} (Match: {fors == end_fors})")
    print(f"  WHILE: {whiles} | END_WHILE: {end_whiles} (Match: {whiles == end_whiles})")
    print(f"  FUNCTION_BLOCK: {fb_starts} | END_FUNCTION_BLOCK: {fb_ends} (Match: {fb_starts == fb_ends})")
    
    # Save to JSON
    prompt = """You are Lumina's Elite Synthetic Data Architect for IEC 61131-3 Programmable Logic Controllers (V7 Max-Persona: 75+ years Principal Automation Fellow & Cyber-Physical Systems Chair).

Commercial Sector: Renewable Energy & Power Grid / 100 MW Utility-Scale BESS & Grid-Forming Inverter
Function Block Name: FB_Power_BESS_GridForming_VirtualSynchronousGenerator_Thermal

System Scope:
100 MW / 400 MWh Utility-Scale Battery Energy Storage System (BESS) paired with Grid-Forming (GFM) Virtual Synchronous Machine (VSM) inverters and centralized liquid thermal management. Sub-20 ms synthetic inertia injection, dynamic RoCoF (Rate of Change of Frequency) damping, P-f frequency droop and Q-V voltage support, 1,500 V DC battery rack string State-of-Charge (SoC) active balancing, multi-circuit closed-loop chiller glycol coolant flow allocation, and multi-stage battery thermal runaway off-gas detection (H2, CO, aerosol) with emergency fire deluge isolation.

Mathematical & Cyber-Physical Requirements:
1. Discrete State-Space Matrices (A, B, C, D) 6x6 system representing:
   - Virtual synchronous rotor angle delta [rad] and virtual rotor angular speed omega_vsg [rad/s]
   - Grid point of common coupling (PCC) active power P_grid [MW] and reactive power Q_grid [MVAr]
   - Battery string bulk State of Charge (SoC) [%] and internal equivalent circuit polarization overpotential [V]
   - Maximum battery module core cell temperature T_max [deg C] and rack-to-rack thermal gradient Delta_T [deg C]
   - Liquid glycol cooling loop thermal energy absorption rate [kW] and chiller supply temperature [deg C]
   - BESS DC bus voltage stability V_dc [V] and DC harmonic ripple current [A]
2. Receding-Horizon Model Predictive Control (MPC) with unrolled Projected Gradient Descent (PGD) (10 iterations) balancing virtual mechanical power setpoint P_m [MW], virtual excitation voltage E_v [kV], rack-level DC-DC converter current trims [A], liquid chiller compressor VFD speeds [RPM], and proportional glycol cooling valves [%].
3. 2oo3 Triple Modular Redundant (TMR) voting logic with discrepancy timers and bumpless degradation across:
   - PCC utility grid voltage transducers (Grid_Volt: 1, 2, 3) [kV]
   - PCC utility grid frequency measurement units (Grid_Freq: 1, 2, 3) [Hz]
   - BESS main DC link voltage transducers (DC_Volt: 1, 2, 3) [V]
   - Battery rack off-gas composite electrochemical sensors (Gas_Sensors: 1, 2, 3) [ppm H2 / CO]
4. 14-Stage Deterministic Production Finite State Machine:
   - 0: STATE_IDLE
   - 1: STATE_CHILLER_GLYCOL_PRECOOL_AND_PRESSURE_LOCK
   - 2: STATE_INSULATION_MONITORING_AND_PRECHARGE_RESISTOR_ENGAGE
   - 3: STATE_DC_MAIN_CONTACTOR_CLOSING_SEQUENCE
   - 4: STATE_INVERTER_BLACK_START_GRID_FORMING_VOLTAGE_RAMP
   - 5: STATE_GRID_SYNCHRONIZATION_AND_AC_BREAKER_CLOSE
   - 6: STATE_NOMINAL_BASELOAD_ENERGY_DISPATCH
   - 7: STATE_FAST_FREQUENCY_RESPONSE_INERTIA_SURGE
   - 8: STATE_VOLTAGE_SAG_LOW_VOLTAGE_RIDE_THROUGH_LVRT
   - 9: STATE_DYNAMIC_STRING_SOC_EQUALIZATION_BALANCING
   - 10: STATE_PEAK_THERMAL_COOLING_BOOST_CHILLER_MAX
   - 11: STATE_CONTROLLED_RAMPDOWN_AND_FLOAT_STANDBY
   - 12: STATE_POST_DISPATCH_REST_AND_OCV_RELAXATION
   - 13: STATE_EMERGENCY_THERMAL_RUNAWAY_OR_ARC_FLASH_TRIP
5. ISA-18.2 Multi-tiered alarm engine (HH, H, L, LL, deadbands) with bit-packed 32-bit DWORD alarm and status words.
6. Target length: >= 85,000 to 140,000+ characters. Zero placeholders, zero truncation comments.
7. Enforce 100% exact delimiter parity: every IF has END_IF;, every CASE has END_CASE;, every FOR has END_FOR;.
8. Validate code with 'python validate_iec.py' and save the JSON dataset to 'data/swarm_raw/agent_<uuid>.json' using the 3-message schema with system prompt. Report completion when done."""

    asst_content = f"```iec-st\n{code}\n```"
    print("Assistant message total character count:", len(asst_content))
    
    file_uuid = uuid.uuid4().hex[:8]
    out_path = f"data/swarm_raw/agent_{file_uuid}.json"
    
    record = {
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": asst_content}
        ]
    }
    
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)
        
    print(f"Saved dataset file to: {out_path}")
