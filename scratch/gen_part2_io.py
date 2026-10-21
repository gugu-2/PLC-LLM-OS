# -*- coding: utf-8 -*-
"""
Part 2: VAR_INPUT and VAR_OUTPUT for FB_GeothermalKalina_AmmoniaWater_ExpansionTurbine
"""

part2_io = """VAR_INPUT
    (* ===================================================================================== *)
    (* 1.0 SYSTEM MASTER DIGITAL PERMISSIVES & OPERATOR COMMANDS                             *)
    (* ===================================================================================== *)
    bEnableSystem                   : BOOL := FALSE;    (* Master Supervisory Execution Enable Command *)
    bEmergencyStop                  : BOOL := TRUE;     (* Hardwired SIL-3 Dual-Channel E-Stop Relay OK (Active High) *)
    bAcknowledgeFault               : BOOL := FALSE;    (* Operator Master Alarm & Trip Reset Acknowledge Pulse *)
    bGridBreakerClosed              : BOOL := FALSE;    (* High-Voltage Main Substation Generator Breaker Auxiliary Status *)
    bAutoConcentrationShiftEnable   : BOOL := TRUE;     (* Enable Dynamic Basic Concentration Seasonal/Diurnal Shifting *)
    bManualNCGPurgeTrigger          : BOOL := FALSE;    (* Operator Manual Override Request for NCG Vacuum Purge Cycle *)
    bTurbineSlowRollEngaged         : BOOL := FALSE;    (* Hydraulic Turning Gear Slow-Roll Engaged Status (50 rpm) *)
    bBypassGovernorDroop            : BOOL := FALSE;    (* Test Override: Force Isochronous Governing in Island Mode *)

    (* ===================================================================================== *)
    (* 2.0 TRIPLE MODULAR REDUNDANCY (2oo3) GEOTHERMAL BRINE RESOURCE TRANSMITTERS           *)
    (* Pressurized liquid geothermal brine from production wells at 165.0 deg C              *)
    (* ===================================================================================== *)
    rBrineInletTemp_A               : REAL := 165.0;    (* Brine Heat Exchanger Supply Temperature Channel A [deg C] *)
    rBrineInletTemp_B               : REAL := 165.0;    (* Brine Heat Exchanger Supply Temperature Channel B [deg C] *)
    rBrineInletTemp_C               : REAL := 165.0;    (* Brine Heat Exchanger Supply Temperature Channel C [deg C] *)

    rBrineInletPress_A              : REAL := 18.5;     (* Brine Wellhead Delivery Pressure Channel A [bar] *)
    rBrineInletPress_B              : REAL := 18.5;     (* Brine Wellhead Delivery Pressure Channel B [bar] *)
    rBrineInletPress_C              : REAL := 18.5;     (* Brine Wellhead Delivery Pressure Channel C [bar] *)

    rBrineMassFlow_A                : REAL := 140.0;    (* Total Brine Delivery Mass Flowrate Channel A [kg/s] *)
    rBrineMassFlow_B                : REAL := 140.0;    (* Total Brine Delivery Mass Flowrate Channel B [kg/s] *)
    rBrineMassFlow_C                : REAL := 140.0;    (* Total Brine Delivery Mass Flowrate Channel C [kg/s] *)

    rBrineOutletTemp_A              : REAL := 75.0;     (* Brine Reinjection Header Temperature Channel A [deg C] *)
    rBrineOutletTemp_B              : REAL := 75.0;     (* Brine Reinjection Header Temperature Channel B [deg C] *)
    rBrineOutletTemp_C              : REAL := 75.0;     (* Brine Reinjection Header Temperature Channel C [deg C] *)

    (* ===================================================================================== *)
    (* 3.0 TRIPLE MODULAR REDUNDANCY (2oo3) SEPARATOR & WORKING FLUID THERMODYNAMIC SENSORS  *)
    (* High-pressure zeotropic vapor-liquid equilibrium fractionation distillation column   *)
    (* ===================================================================================== *)
    rSeparatorPress_A               : REAL := 32.5;     (* High-Pressure Separator Drum Pressure Channel A [bar] *)
    rSeparatorPress_B               : REAL := 32.5;     (* High-Pressure Separator Drum Pressure Channel B [bar] *)
    rSeparatorPress_C               : REAL := 32.5;     (* High-Pressure Separator Drum Pressure Channel C [bar] *)

    rSeparatorVaporTemp_A           : REAL := 142.0;    (* Separator Overhead Rich Vapor Temperature Channel A [deg C] *)
    rSeparatorVaporTemp_B           : REAL := 142.0;    (* Separator Overhead Rich Vapor Temperature Channel B [deg C] *)
    rSeparatorVaporTemp_C           : REAL := 142.0;    (* Separator Overhead Rich Vapor Temperature Channel C [deg C] *)

    rVaporAmmoniaConc_A             : REAL := 0.945;    (* Separator Overhead Rich Vapor Ammonia Fraction Channel A [mol/mol] *)
    rVaporAmmoniaConc_B             : REAL := 0.945;    (* Separator Overhead Rich Vapor Ammonia Fraction Channel B [mol/mol] *)
    rVaporAmmoniaConc_C             : REAL := 0.945;    (* Separator Overhead Rich Vapor Ammonia Fraction Channel C [mol/mol] *)

    rBasicAmmoniaConc_A             : REAL := 0.780;    (* Basic Working Fluid Circulation Ammonia Fraction Channel A [mol/mol] *)
    rBasicAmmoniaConc_B             : REAL := 0.780;    (* Basic Working Fluid Circulation Ammonia Fraction Channel B [mol/mol] *)
    rBasicAmmoniaConc_C             : REAL := 0.780;    (* Basic Working Fluid Circulation Ammonia Fraction Channel C [mol/mol] *)

    rSeparatorFloatLevel_A          : REAL := 50.0;     (* Separator Drum Liquid Level Float Transmitter Channel A [%] *)
    rSeparatorFloatLevel_B          : REAL := 50.0;     (* Separator Drum Liquid Level Float Transmitter Channel B [%] *)
    rSeparatorFloatLevel_C          : REAL := 50.0;     (* Separator Drum Liquid Level Float Transmitter Channel C [%] *)

    rWorkingFluidFeedFlow_A         : REAL := 38.5;     (* High-Pressure Working Fluid Evaporator Feed Flow Channel A [kg/s] *)
    rWorkingFluidFeedFlow_B         : REAL := 38.5;     (* High-Pressure Working Fluid Evaporator Feed Flow Channel B [kg/s] *)
    rWorkingFluidFeedFlow_C         : REAL := 38.5;     (* High-Pressure Working Fluid Evaporator Feed Flow Channel C [kg/s] *)

    (* ===================================================================================== *)
    (* 4.0 TRIPLE MODULAR REDUNDANCY (2oo3) VARIABLE-GEOMETRY TURBINE & ROTORDYNAMICS       *)
    (* High-speed radial inflow expander geared to synchronous generator                     *)
    (* ===================================================================================== *)
    rTurbineSpeed_A                 : REAL := 12000.0;  (* Turbine Expander Rotor Shaft Speed Channel A [rpm] *)
    rTurbineSpeed_B                 : REAL := 12000.0;  (* Turbine Expander Rotor Shaft Speed Channel B [rpm] *)
    rTurbineSpeed_C                 : REAL := 12000.0;  (* Turbine Expander Rotor Shaft Speed Channel C [rpm] *)

    rTurbineInletPress_A            : REAL := 31.8;     (* Turbine Expander Casing Inlet Pressure Channel A [bar] *)
    rTurbineInletPress_B            : REAL := 31.8;     (* Turbine Expander Casing Inlet Pressure Channel B [bar] *)
    rTurbineInletPress_C            : REAL := 31.8;     (* Turbine Expander Casing Inlet Pressure Channel C [bar] *)

    rTurbineInletTemp_A             : REAL := 141.5;    (* Turbine Expander Casing Inlet Temperature Channel A [deg C] *)
    rTurbineInletTemp_B             : REAL := 141.5;    (* Turbine Expander Casing Inlet Temperature Channel B [deg C] *)
    rTurbineInletTemp_C             : REAL := 141.5;    (* Turbine Expander Casing Inlet Temperature Channel C [deg C] *)

    rTurbineExhaustPress_A          : REAL := 4.85;     (* Turbine Expander Radial Diffuser Exhaust Pressure Channel A [bar] *)
    rTurbineExhaustPress_B          : REAL := 4.85;     (* Turbine Expander Radial Diffuser Exhaust Pressure Channel B [bar] *)
    rTurbineExhaustPress_C          : REAL := 4.85;     (* Turbine Expander Radial Diffuser Exhaust Pressure Channel C [bar] *)

    rGeneratorRealPower_A           : REAL := 7200.0;   (* 3-Phase Generator Active Real Electrical Power Channel A [kW] *)
    rGeneratorRealPower_B           : REAL := 7200.0;   (* 3-Phase Generator Active Real Electrical Power Channel B [kW] *)
    rGeneratorRealPower_C           : REAL := 7200.0;   (* 3-Phase Generator Active Real Electrical Power Channel C [kW] *)

    rGridFrequency_Hz               : REAL := 50.00;    (* High-Voltage Utility Interconnection Grid Frequency [Hz] *)
    rTurbineVibrationRadial_X       : REAL := 12.5;     (* Expander Drive-End Non-Contacting Proximity Probe X [um] *)
    rTurbineVibrationRadial_Y       : REAL := 14.0;     (* Expander Drive-End Non-Contacting Proximity Probe Y [um] *)
    rTurbineThrustDisplacement      : REAL := 0.12;     (* Axial Active-Face Thrust Bearing Rotor Position [mm] *)

    (* ===================================================================================== *)
    (* 5.0 RECUPERATOR, CONDENSER & VACUUM ABSORBER TRANSDUCERS                              *)
    (* Liquid-level float pots and vacuum monitoring across low-pressure heat rejection sink *)
    (* ===================================================================================== *)
    rCondenserPressure_A            : REAL := 465.0;    (* Condenser / Absorber Low-Pressure Shell Channel A [kPa] *)
    rCondenserPressure_B            : REAL := 465.0;    (* Condenser / Absorber Low-Pressure Shell Channel B [kPa] *)
    rCondenserPressure_C            : REAL := 465.0;    (* Condenser / Absorber Low-Pressure Shell Channel C [kPa] *)

    rHotwellFloatLevel_A            : REAL := 52.0;     (* Condenser Sump / Hotwell Condensate Float Level Channel A [%] *)
    rHotwellFloatLevel_B            : REAL := 52.0;     (* Condenser Sump / Hotwell Condensate Float Level Channel B [%] *)
    rHotwellFloatLevel_C            : REAL := 52.0;     (* Condenser Sump / Hotwell Condensate Float Level Channel C [%] *)

    rHTR_FloatLevel_A               : REAL := 48.0;     (* High-Temperature Recuperator Drain Float Level Channel A [%] *)
    rHTR_FloatLevel_B               : REAL := 48.0;     (* High-Temperature Recuperator Drain Float Level Channel B [%] *)
    rHTR_FloatLevel_C               : REAL := 48.0;     (* High-Temperature Recuperator Drain Float Level Channel C [%] *)

    rLTR_FloatLevel_A               : REAL := 51.0;     (* Low-Temperature Recuperator Drain Float Level Channel A [%] *)
    rLTR_FloatLevel_B               : REAL := 51.0;     (* Low-Temperature Recuperator Drain Float Level Channel B [%] *)
    rLTR_FloatLevel_C               : REAL := 51.0;     (* Low-Temperature Recuperator Drain Float Level Channel C [%] *)

    rPreheaterFloatLevel_A          : REAL := 49.5;     (* Evaporator Preheater Condensate Float Level Channel A [%] *)
    rPreheaterFloatLevel_B          : REAL := 49.5;     (* Evaporator Preheater Condensate Float Level Channel B [%] *)
    rPreheaterFloatLevel_C          : REAL := 49.5;     (* Evaporator Preheater Condensate Float Level Channel C [%] *)

    rCoolingWaterSupplyTemp         : REAL := 22.5;     (* Cooling Tower Basin Supply Water Temperature [deg C] *)
    rCoolingWaterReturnTemp         : REAL := 31.0;     (* Condenser Cooling Water Discharge Temperature [deg C] *)
    rCoolingWaterFlow_kg_s          : REAL := 380.0;    (* Condenser Shell Cooling Water Total Circulating Flow [kg/s] *)
    rAmbientWetBulbTemp             : REAL := 18.0;     (* Psychrometric Ambient Station Wet-Bulb Temperature [deg C] *)

    (* ===================================================================================== *)
    (* 6.0 NON-CONDENSABLE GAS (NCG) PURGE VACUUM LOCK SYSTEM TRANSDUCERS                   *)
    (* Differential-pressure lock-hopper with ammonia absorption wash scrubber               *)
    (* ===================================================================================== *)
    rNCGLockPressure_A              : REAL := 450.0;    (* NCG Accumulator Lock-Chamber Internal Pressure Channel A [kPa] *)
    rNCGLockPressure_B              : REAL := 450.0;    (* NCG Accumulator Lock-Chamber Internal Pressure Channel B [kPa] *)
    rNCGScrubberTemp                : REAL := 19.5;     (* Ammonia Absorption Scrubber Recirculating Liquid Temp [deg C] *)
    rNCGScrubberLevel               : REAL := 65.0;     (* Ammonia Wash Scrubber Sump Level Float Transmitter [%] *)
    rNCGAmmoniaVaporPPM             : REAL := 8.5;      (* Scrubber Discharge Atmospheric Vent NH3 Toxic Gas Detector [ppm] *)
    rNCGVaccumPumpDischargePress    : REAL := 102.5;    (* Liquid-Ring Vacuum Pump Vent Exhaust Pressure [kPa] *)
END_VAR

VAR_OUTPUT
    (* ===================================================================================== *)
    (* 1.0 CYBER-PHYSICAL ACTUATOR COMMANDS & VALVE MODULATION SIGNALS                       *)
    (* ===================================================================================== *)
    rVanePitchAngle_Cmd             : REAL := 0.0;      (* Variable-Geometry Turbine Nozzle Guide Vane Command (0-100%) [%] *)
    rTurbineThrottleValve_Cmd       : REAL := 0.0;      (* Turbine High-Pressure Quick-Acting Throttle Governor Valve [%] *)
    rTurbineBypassValve_Cmd         : REAL := 100.0;    (* High-Pressure Fast Expander Bypass / Dump Valve [%] *)
    rBrineControlValve_Cmd          : REAL := 0.0;      (* Primary Geothermal Brine Heat Exchanger Supply Valve [%] *)
    rBrineBypassValve_Cmd           : REAL := 100.0;    (* Emergency Geothermal Brine Resource Fast Bypass Valve [%] *)
    rDistillationReflux_Cmd         : REAL := 0.0;      (* Fractionation Distillation Overhead Reflux Trim Valve [%] *)
    rLeanLiquidDrainValve_Cmd       : REAL := 0.0;      (* Separator Drum Lean Solution Bottoms Float Valve [%] *)
    rCondensatePumpSpeed_Cmd        : REAL := 0.0;      (* Multi-Stage Working Fluid Booster Extraction Pump VFD [%] *)
    rHTR_DrainFloatValve_Cmd        : REAL := 0.0;      (* High-Temperature Recuperator Condensation Float Valve [%] *)
    rLTR_DrainFloatValve_Cmd        : REAL := 0.0;      (* Low-Temperature Recuperator Condensation Float Valve [%] *)
    rPreheaterDrainValve_Cmd        : REAL := 0.0;      (* Evaporator Preheater Condensation Float Balance Valve [%] *)
    bEmergencyStopValve_Trip        : BOOL := FALSE;    (* SIL-3 Electro-Hydraulic ESV Trip Solenoid (True=Energized/Open, False=Tripped) *)

    (* ===================================================================================== *)
    (* 2.0 NON-CONDENSABLE GAS (NCG) PURGE VACUUM LOCK ACTUATION                             *)
    (* ===================================================================================== *)
    rNCGLockInletValve_Cmd          : REAL := 0.0;      (* Condenser Vapor Pocket to NCG Lock Intake Modulating Valve [%] *)
    rNCGLockVentValve_Cmd           : REAL := 0.0;      (* NCG Scrubber Purified Atmospheric Vent Modulating Valve [%] *)
    bNCGVacuumPump_Run              : BOOL := FALSE;    (* Liquid-Ring Vacuum Extraction Pump Motor Contactor Run *)
    bNCGScrubberPump_Run            : BOOL := FALSE;    (* Cold Water Ammonia Scrubber Spray Circulation Pump Run *)

    (* ===================================================================================== *)
    (* 3.0 THERMODYNAMIC PROCESS EFFICIENCIES, EXERGY BALANCES & PERFORMANCE METRICS         *)
    (* ===================================================================================== *)
    rTotalThermalDuty_kW            : REAL := 0.0;      (* Real-Time Evaporator / Superheater Heat Absorption Duty [kW] *)
    rBrineHeatExtraction_kW         : REAL := 0.0;      (* Thermal Power Extracted from Pressurized Geothermal Brine [kW] *)
    rKalinaThermalEfficiency        : REAL := 0.0;      (* Gross First-Law Cycle Thermodynamic Conversion Efficiency [%] *)
    rSecondLawExergyEfficiency      : REAL := 0.0;      (* Second-Law Exergetic Efficiency Based on 165°C Brine Potential [%] *)
    rTurbineIsentropicEff           : REAL := 0.0;      (* Real-Time Radial Expander Stage Isentropic Expansion Efficiency [%] *)
    rTurbineSpecificSpeed_Ns        : REAL := 0.0;      (* Dimensionless Turbine Stage Specific Speed Coefficient [-] *)
    rTurbineVelocityRatio_u_c0      : REAL := 0.0;      (* Expander Blade Tip Speed to Spouting Velocity Ratio (u/c0) [-] *)
    rDewPointMargin_degC            : REAL := 0.0;      (* Separator Rich Vapor Superheat Clearance Above Dew Point [deg C] *)
    rSilicaSaturationIndex          : REAL := 0.0;      (* Geothermal Brine Reinjection Silica Precipitation Margin [-] *)
    rNCGAccumulationIndex           : REAL := 0.0;      (* Estimated Non-Condensable Gas Incondensable Partial Pressure [%] *)
    rTargetBasicAmmoniaConc         : REAL := 0.780;    (* Dynamically Calculated Optimal Basic Working Fluid Fraction [mol/mol] *)

    (* ===================================================================================== *)
    (* 4.0 SUPERVISORY STATE, DIAGNOSTICS & TRIPLE MODULAR FAULT BITMASKS                    *)
    (* ===================================================================================== *)
    bSystemReady                    : BOOL := FALSE;    (* Power Generation System Ready for Start Permissive *)
    bSystemRunning                  : BOOL := FALSE;    (* Online Power Generation Baseload State Active *)
    bSystemTrip                     : BOOL := FALSE;    (* Master Safety Interlock Latched Emergency Trip Status *)
    bSystemWarning                  : BOOL := FALSE;    (* Master Operational Advisory Warning Status *)
    bMPC_Active                     : BOOL := FALSE;    (* 6-State Constrained MPC Quadratic Optimization Loop Closed *)
    bGovernorSynchronized           : BOOL := FALSE;    (* Turbine Governor Synchronous Speed / Frequency Lock Achieved *)
    bDegradedSensorMode             : BOOL := FALSE;    (* Sensor Failure Detected - Degraded from 2oo3 to 1oo2 or Hold *)
    iCurrentState                   : INT := 0;         (* Active Supervisory Operating State Machine Identifier *)
    dwSystemStatusWord              : DWORD := 16#0000_0000; (* 32-Bit Comprehensive Operational Status Bitmask *)
    dwAlarmWord1                    : DWORD := 16#0000_0000; (* 32-Bit Primary Process Excursion & Threshold Alarm Bitmask *)
    dwAlarmWord2                    : DWORD := 16#0000_0000; (* 32-Bit Secondary Turbomachinery & Vacuum System Alarm Bitmask *)
    dwTripWord                      : DWORD := 16#0000_0000; (* 32-Bit Master Safety Trip Cause & SIL-3 Interlock Word *)
END_VAR
"""

with open("scratch/part2_io.txt", "w", encoding="utf-8") as f:
    f.write(part2_io)

print("Part 2 IO written. Length:", len(part2_io))
