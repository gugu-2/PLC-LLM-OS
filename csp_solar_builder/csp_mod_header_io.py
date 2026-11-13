# -*- coding: utf-8 -*-
"""
Module 1: Header and I/O Variable Declarations
FB_Power_SolarCSP_MoltenSalt_Receiver_ThermalStorage
"""

def get_header_and_io():
    return """FUNCTION_BLOCK FB_Power_SolarCSP_MoltenSalt_Receiver_ThermalStorage
(*
========================================================================================================================
  LUMINA CYBER-PHYSICAL AUTOMATION ENGINE - SYNTHETIC DATASET V7 MAX-PERSONA
  COMMERCIAL POWER GENERATION DIVISION - CONCENTRATED SOLAR POWER (CSP) TOWER
========================================================================================================================
SYSTEM SPECIFICATION:
  - Facility Type       : 150 MWe (560 MWth) Commercial Molten-Salt Central Receiver Solar Thermal Tower Power Plant.
  - Solar Field         : 10,000 Dual-Axis Computer-Controlled Heliostats (Total Reflective Aperture Area: 1,320,000 m2).
  - Tower Architecture  : 240-Meter Reinforced Slip-Form Concrete Tower with 360-Degree Cylindrical External Tubular Receiver.
  - Receiver Design     : 16 Serpentine Twin-Pass Flow Panels (Inconel 625 / Alloy 800H Thin-Wall Absorber Tubes).
  - Heat Transfer Fluid : Binary Nitrate Solar Salt Eutectic (60 wt% NaNO3, 40 wt% KNO3; Liquid Range: 220 deg C - 600 deg C).
  - Thermal Energy Store: Two-Tank Indirect Sensible Thermal Energy Storage System (14 Full-Load Hours, ~28,500 Metric Tons).
  - Power Block Dispatch: Molten-Salt Steam Generator (MSSG) Superheater / Reheater Train Driving a 150 MWe Reheat Turbine.
========================================================================================================================
CYBER-PHYSICAL & THEORETICAL PROCESS DYNAMICS:
  1. Molten-Salt Thermophysical Equations:
     - Density rho(T) [kg/m3]              : rho(T) = 2090.0 - 0.636 * T_celsius
     - Specific Heat Cp(T) [J/(kg*K)]       : Cp(T)  = 1443.0 + 0.172 * T_celsius
     - Dynamic Viscosity mu(T) [mPa*s]      : mu(T)  = EXP(-4.343 - 2.014E-3 * T_celsius + 2.87E-6 * T_celsius**2)
     - Thermal Conductivity k(T) [W/(m*K)]  : k(T)   = 0.443 + 1.9E-4 * T_celsius
  2. Inconel 625 Receiver Tube Thermoelastic Stress & Creep-Fatigue:
     - Circumferential & Radial Tube Wall Thermal Gradient: Delta_T_wall = (q_flux * t_wall) / k_metal + (q_flux / h_conv)
     - Peak Thermoelastic Stress: sigma_th = (E_mod * alpha_th * Delta_T_wall) / (2.0 * (1.0 - nu_poisson))
     - Maximum Allowable Solar Flux Threshold: q_max = 950.0 kW/m2 to guarantee 30-year design life against creep-fatigue.
  3. Dynamic Heliostat Aimpoint Optimization:
     - Real-time Gaussian flux superposition distributing 10,000 heliostats across 16 panels.
     - Fast Cloud-Edge Attenuation Feedforward: d(DNI)/dt < -50 W/(m2*s) triggers emergency standby defocus sweep in < 2.0 s.
  4. Salt Solidification & Freeze Watchdog:
     - Liquidus Solidification Limit: T_freeze = 220.0 deg C (Safety Emergency Floor: 260.0 deg C).
     - Automated anti-siphon gravity drainback dumping 100% receiver inventory to cold sump in < 90 seconds.
========================================================================================================================
*)
VAR_INPUT
    (* Triplicated Sensor Triplet 1: Receiver Molten Salt Outlet High-Temperature Thermocouples *)
    rSaltOutletTemp_A_degC              : REAL;     (* Receiver Salt Outlet High-Temp Thermocouple Channel A [deg C] *)
    rSaltOutletTemp_B_degC              : REAL;     (* Receiver Salt Outlet High-Temp Thermocouple Channel B [deg C] *)
    rSaltOutletTemp_C_degC              : REAL;     (* Receiver Salt Outlet High-Temp Thermocouple Channel C [deg C] *)

    (* Triplicated Sensor Triplet 2: Receiver Peak Tube Surface Crown Infrared Pyrometers *)
    rTubeSurfaceTemp_A_degC             : REAL;     (* Receiver Crown Infrared Optical Pyrometer Channel A [deg C] *)
    rTubeSurfaceTemp_B_degC             : REAL;     (* Receiver Crown Infrared Optical Pyrometer Channel B [deg C] *)
    rTubeSurfaceTemp_C_degC             : REAL;     (* Receiver Crown Infrared Optical Pyrometer Channel C [deg C] *)

    (* Triplicated Sensor Triplet 3: Direct Normal Irradiance (DNI) Solar Pyrheliometers *)
    rSolarDNI_A_Wm2                     : REAL;     (* Tower Base High-Precision Pyrheliometer Channel A [W/m2] *)
    rSolarDNI_B_Wm2                     : REAL;     (* Tower Base High-Precision Pyrheliometer Channel B [W/m2] *)
    rSolarDNI_C_Wm2                     : REAL;     (* Tower Base High-Precision Pyrheliometer Channel C [W/m2] *)

    (* Triplicated Sensor Triplet 4: Molten Salt Receiver Transit-Time Ultrasonic Flowmeters *)
    rSaltFlow_A_kgs                     : REAL;     (* High-Temperature Clamp-On Ultrasonic Flowmeter Channel A [kg/s] *)
    rSaltFlow_B_kgs                     : REAL;     (* High-Temperature Clamp-On Ultrasonic Flowmeter Channel B [kg/s] *)
    rSaltFlow_C_kgs                     : REAL;     (* High-Temperature Clamp-On Ultrasonic Flowmeter Channel C [kg/s] *)

    (* Receiver 16-Panel Individual Crown Thermocouple Bank *)
    rPanel1_CrownTemp_degC              : REAL;     (* Receiver Panel 01 Inconel Tube Crown Temperature [deg C] *)
    rPanel2_CrownTemp_degC              : REAL;     (* Receiver Panel 02 Inconel Tube Crown Temperature [deg C] *)
    rPanel3_CrownTemp_degC              : REAL;     (* Receiver Panel 03 Inconel Tube Crown Temperature [deg C] *)
    rPanel4_CrownTemp_degC              : REAL;     (* Receiver Panel 04 Inconel Tube Crown Temperature [deg C] *)
    rPanel5_CrownTemp_degC              : REAL;     (* Receiver Panel 05 Inconel Tube Crown Temperature [deg C] *)
    rPanel6_CrownTemp_degC              : REAL;     (* Receiver Panel 06 Inconel Tube Crown Temperature [deg C] *)
    rPanel7_CrownTemp_degC              : REAL;     (* Receiver Panel 07 Inconel Tube Crown Temperature [deg C] *)
    rPanel8_CrownTemp_degC              : REAL;     (* Receiver Panel 08 Inconel Tube Crown Temperature [deg C] *)
    rPanel9_CrownTemp_degC              : REAL;     (* Receiver Panel 09 Inconel Tube Crown Temperature [deg C] *)
    rPanel10_CrownTemp_degC             : REAL;     (* Receiver Panel 10 Inconel Tube Crown Temperature [deg C] *)
    rPanel11_CrownTemp_degC             : REAL;     (* Receiver Panel 11 Inconel Tube Crown Temperature [deg C] *)
    rPanel12_CrownTemp_degC             : REAL;     (* Receiver Panel 12 Inconel Tube Crown Temperature [deg C] *)
    rPanel13_CrownTemp_degC             : REAL;     (* Receiver Panel 13 Inconel Tube Crown Temperature [deg C] *)
    rPanel14_CrownTemp_degC             : REAL;     (* Receiver Panel 14 Inconel Tube Crown Temperature [deg C] *)
    rPanel15_CrownTemp_degC             : REAL;     (* Receiver Panel 15 Inconel Tube Crown Temperature [deg C] *)
    rPanel16_CrownTemp_degC             : REAL;     (* Receiver Panel 16 Inconel Tube Crown Temperature [deg C] *)

    (* Process Hydraulic & Thermal Pressures and Temperatures *)
    rReceiverInletTemp_degC             : REAL;     (* Receiver Inlet Header Molten Salt Temperature [deg C] *)
    rReceiverInletPress_bar             : REAL;     (* Receiver Riser Cold Salt Inlet Pressure [bar] *)
    rReceiverOutletPress_bar            : REAL;     (* Receiver Downcomer Hot Salt Outlet Pressure [bar] *)

    (* Two-Tank Sensible Thermal Energy Storage (TES) Telemetry *)
    rHotTankLevel_pct                   : REAL;     (* Hot Molten Salt Storage Tank Hydrostatic Level [%] *)
    rHotTankBulkTemp_degC               : REAL;     (* Hot Molten Salt Storage Tank Internal Bulk Temp [deg C] *)
    rColdTankLevel_pct                  : REAL;     (* Cold Molten Salt Storage Tank Hydrostatic Level [%] *)
    rColdTankBulkTemp_degC              : REAL;     (* Cold Molten Salt Storage Tank Internal Bulk Temp [deg C] *)

    (* Power Block Molten-Salt Steam Generator (MSSG) Interface *)
    rSteamGenInletTemp_degC             : REAL;     (* Steam Generator Superheater Salt Inlet Temperature [deg C] *)
    rSteamGenReturnTemp_degC            : REAL;     (* Steam Generator Preheater Salt Return Temperature [deg C] *)
    rSteamGenSaltFlow_kgs               : REAL;     (* Molten Salt Flow Rate Dispatched to Steam Generator Train [kg/s] *)
    rPowerBlockLoadDemand_MW            : REAL;     (* Grid Power Dispatch Target Electric Output Demand [MW] *)

    (* Meteorological & Ephemeris Solar Position Inputs *)
    rAmbientTemp_degC                   : REAL;     (* Solar Field Ambient Air Temperature [deg C] *)
    rAmbientWindSpeed_ms                : REAL;     (* 10-Meter Mast Anemometer Wind Velocity [m/s] *)
    rSunElevation_deg                   : REAL;     (* True Astronomical Solar Elevation Angle [deg] *)
    rSunAzimuth_deg                     : REAL;     (* True Astronomical Solar Azimuth Angle [deg] *)

    (* Control System Commands, Flags & Scan Interval *)
    bMasterEnable                       : BOOL;     (* Master Automation System Run Enable Flag [-] *)
    bAutoModeActive                     : BOOL;     (* Autonomous Closed-Loop MPC Supervisory Mode Select [-] *)
    bEmergencyStop                      : BOOL;     (* Plant Hardwired Emergency Stop Active-Low Circuit [-] *)
    bAlarmAcknowledge                   : BOOL;     (* Operator Alarm Acknowledgment Pushbutton Pulse [-] *)
    bManualDrainCommand                 : BOOL;     (* Operator Forced Gravity Drainback Dump Command [-] *)
    bTurbineDispatchEnable              : BOOL;     (* Grid Supervisory Dispatch Enable for Power Block [-] *)
    rTaskCycleTime_sec                  : REAL;     (* Deterministic Controller Execution Scan Cycle Time [s] *)
END_VAR

VAR_OUTPUT
    (* Primary Actuator Command Signals *)
    rCmd_ColdSaltPump_RPM               : REAL;     (* Cold Salt Vertical Turbine VFD Pump Speed Command [RPM] *)
    rCmd_HeliostatDefocus_pct           : REAL;     (* Heliostat Field Global Defocus / Standby Aimpoint Ring [%] *)
    rCmd_InletModulatingValve_pct       : REAL;     (* Receiver Riser Cold Salt Modulating Control Valve Trim [%] *)
    rCmd_HotSaltDischargePump_RPM       : REAL;     (* Hot Salt Tank Discharge Pump VFD Speed to Steam Generator [RPM] *)
    rCmd_TraceHeatingPower_pct          : REAL;     (* Electric Resistance Heat Trace SCR Thyristor Duty Power [%] *)

    (* Discrete Safety Actuators & Automated Isolation Valves *)
    bCmd_EmergencyDrainValve1_Open      : BOOL;     (* Fail-Open Pneumatic Receiver Dump Valve 1 to Cold Sump [-] *)
    bCmd_EmergencyDrainValve2_Open      : BOOL;     (* Fail-Open Pneumatic Receiver Dump Valve 2 to Cold Sump [-] *)
    bCmd_TowerTopVentValve_Open         : BOOL;     (* Fail-Open Top Receiver Anti-Siphon Vacuum Breaker Vent [-] *)
    bCmd_ReceiverInletIso_Open          : BOOL;     (* Receiver Cold Salt Riser Motorized Isolation Gate Valve [-] *)
    bCmd_ReceiverOutletIso_Open         : BOOL;     (* Receiver Hot Salt Downcomer Motorized Isolation Gate Valve [-] *)
    bCmd_HeliostatStowActive            : BOOL;     (* Emergency Heliostat Field Defensive Inverted Stow Command [-] *)

    (* Discrete State-Space Model Observer Estimates (6 States) *)
    rEst_SaltOutletTemp_degC            : REAL;     (* Observer State 1: Receiver Salt Outlet Temperature [deg C] *)
    rEst_PeakCrownTemp_degC             : REAL;     (* Observer State 2: Peak Receiver Panel Crown Temperature [deg C] *)
    rEst_SaltMassFlow_kgs               : REAL;     (* Observer State 3: Receiver Dynamic Salt Mass Flow Rate [kg/s] *)
    rEst_HotTankLevel_pct               : REAL;     (* Observer State 4: Hot Storage Tank Dynamic Mass Level [%] *)
    rEst_ReceiverEfficiency_pct         : REAL;     (* Observer State 5: Real-Time Solar Receiver Thermal Efficiency [%] *)
    rEst_SteamGenInletTemp_degC         : REAL;     (* Observer State 6: Primary Salt Temperature to Steam Generator [deg C] *)

    (* First-Principles Cyber-Physical Diagnostic Metrics *)
    rCalc_SaltDensity_kgm3              : REAL;     (* Real-Time Binary Solar Salt Dynamic Density [kg/m3] *)
    rCalc_SaltSpecificHeat_JkgK         : REAL;     (* Real-Time Binary Solar Salt Specific Heat Capacity [J/(kg*K)] *)
    rCalc_SaltViscosity_mPas            : REAL;     (* Real-Time Binary Solar Salt Dynamic Viscosity [mPa*s] *)
    rCalc_MaxThermalStress_MPa          : REAL;     (* Calculated Peak Thermoelastic Wall Stress on Crown Tube [MPa] *)
    rCalc_PeakSolarFlux_kWm2            : REAL;     (* Peak Incident Flux Density on Active Receiver Aperture [kW/m2] *)
    rCalc_ThermalStorageEnergy_MWh      : REAL;     (* Available Usable Stored Sensible Thermal Energy [MWh] *)
    rCalc_DNI_RateOfChange_Wms          : REAL;     (* Differentiated Solar DNI Cloud Shadow Derivative [W/(m2*s)] *)

    (* Operational State Machine & Telemetry Registers *)
    nActiveFsmState                     : DINT;     (* Active 14-Stage Operational Production FSM State Number [-] *)
    sActiveFsmStateName                 : STRING[40];(* Human-Readable Descriptive Text Name of Active State [-] *)
    bSystemHealthy                      : BOOL;     (* Global Cyber-Physical System Health Status Flag [-] *)
    bCloudTransientActive               : BOOL;     (* Active Fast Cloud Edge Transient Detected Flag [-] *)
    bFreezeProtectionTrip               : BOOL;     (* Salt Solidification Risk Emergency Drain Triggered [-] *)
    bOverfluxTrip                       : BOOL;     (* Peak Solar Flux Limit Exceeded Emergency Defocus Triggered [-] *)
    bTMR_AnyDiscrepancyTrip             : BOOL;     (* Any 2oo3 Sensor Triplet Active Discrepancy Failure Latched [-] *)

    (* 32-Bit Bit-Packed Telemetry & ISA-18.2 Alarm Registers *)
    dwStatusWord1                       : DWORD;    (* Bit-Packed Primary Operating Telemetry Register 1 [-] *)
    dwStatusWord2                       : DWORD;    (* Bit-Packed Secondary Actuator & Mode Telemetry Register 2 [-] *)
    dwAlarmWord1                        : DWORD;    (* Bit-Packed ISA-18.2 Process Trips and High-High Alarms [-] *)
    dwAlarmWord2                        : DWORD;    (* Bit-Packed ISA-18.2 Process Warnings and Discrepancies [-] *)
    dwFirstOutWord                      : DWORD     (* Bit-Packed Latched First-Out Primary Trip Root Cause Register [-] *)
END_VAR
"""
