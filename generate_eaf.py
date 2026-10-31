# generate_eaf.py
# High-density IEC 61131-3 generator for 150-Ton AC Electric Arc Furnace

import sys
import os
import json
import uuid

def build_full_st_code():
    parts = []
    
    # 0. Declaration
    parts.append("FUNCTION_BLOCK FB_Steel_ElectricArcFurnace_150Ton_ArcImpedance")
    
    # 1. Header comments
    parts.append("""(*
========================================================================================================================
  METALLURGY & INDUSTRIAL AUTOMATION ARCHITECTURE:
  150-TON AC ELECTRIC ARC FURNACE (EAF, 160 MVA TRANSFORMER) WITH HYDRAULIC ELECTRODE REGULATOR,
  DYNAMIC ARC IMPEDANCE CONTROL, POWER QUALITY FLICKER SUPPRESSION & CO-JET CHEMICAL ENERGY INJECTION
  Compliant with IEC 61131-3 3rd Ed., IEC 61508 SIL-3 TMR Safety, and ISA-18.2 Alarm Management Standards.
  Deterministic Cycle Task: Ts = 1.0 ms (1000 Hz Hard Real-Time Industrial Ethernet Fieldbus).
========================================================================================================================
  1. METALLURGICAL & ELECTRICAL PROCESS SPECIFICATIONS:
     - Liquid Steel Tap Weight: 150 Metric Tons per Heat; Nominal Tap-to-Tap Time: 42 Minutes.
     - Furnace Transformer: 160 MVA Rated Capacity with On-Load Tap Changer (OLTC) 18 Symmetrical Steps.
     - Secondary Operating Voltage: 600 V to 1,200 V Phase-to-Phase (Star and Delta configurations).
     - Secondary Operating Current: Up to 80,000 A (80.0 kA) continuous RMS per phase; Peak short-circuit > 180 kA.
     - Electrode Columns: 3x 600 mm (24-inch) Ultra-High-Power (UHP) Premium Needle-Coke Graphite Electrodes.
     - Specific Energy Target: < 360 kWh/ton with combined chemical energy injection; Target Meltdown Power: 110 MW.

  2. ELECTROHYDRAULIC ELECTRODE REGULATOR DYNAMICS:
     - 3 Independent High-Speed Servo Actuators driving hydraulic electrode lifting masts.
     - Actuator Specification: Single-acting differential cylinders (Bore: 250 mm, Rod: 180 mm, Stroke: 4,500 mm).
     - Servo Valves: Moog D661 series dual-stage proportional servo valves (Bandwidth: 45 Hz, Max Flow: 450 L/min).
     - Dynamic Performance: Mast Lifting Velocity up to 250 mm/s; Slew Acceleration up to 8.0 m/s2.
     - Dynamic Arc Impedance Setpoint Regulation:
       Z_arc(t) = V_arc(t) / I_arc(t) [mOhm]
       R_arc(t) = P_arc(t) / (I_arc(t)^2) [mOhm]
       Hydraulic position trim: Delta_Y = K_reg * (Z_arc - Z_setpoint) + K_deriv * dZ/dt.

  3. NON-LINEAR DYNAMIC CASSIE-MAYR ELECTRIC ARC FORMULATION:
     - High-Current Column Conduction (Cassie Dynamic Regime):
       (1 / g_c) * d(g_c)/dt = (1 / theta_C) * ( (v * i) / (E0^2 * g_c) - 1 )
     - Low-Current / Zero-Crossing Conduction (Mayr Dynamic Regime):
       (1 / g_m) * d(g_m)/dt = (1 / theta_M) * ( (v * i) / P0 - 1 )
     - Transition Conductance Blending Function:
       sigma(i) = exp( - (i / I0)^2 )
       g_total(t) = (1.0 - sigma(i)) * g_c(t) + sigma(i) * g_m(t)
     - Arc Column Length Electric Field:
       E0(L_arc) = E_const + alpha_field * L_arc(t)

  4. DYNAMIC SCRAP CAVE-IN & ARC BREAK FAST OVERRIDE LOGIC:
     - Scrap Collapse Short-Circuit Detection:
       Instantaneous Current Spike > 2.5 * I_nominal (or dI/dt > 1.2 * 10^7 A/s with V_arc < 80 V).
       Sub-30 ms upward fast hydraulic retraction (+100.0% spool command) to eliminate graphite tip breakage.
     - Arc Break / Extinguishment Detection:
       Current collapse < 0.08 * I_nominal with Open-Circuit Secondary Voltage > 0.85 * V_sec_open.
       Fast downward strike plunge (-60.0% spool command) until strike ignition current is re-established.

  5. POWER QUALITY & HARMONIC FLICKER MITIGATION:
     - Instantaneous flicker sensation estimation (IEC 61000-4-15 demodulation and human eye-brain response model).
     - Static Var Compensator (SVC) / STATCOM coordination:
       Dynamic reactive susceptance command B_statcom = - Q_furnace / (V_grid^2).
     - Real-time Total Harmonic Distortion (THD) tracking across 2nd, 3rd, and 5th harmonic components.

  6. CO-JET CHEMICAL ENERGY & CONTINUOUS OFF-GAS CEM SAFETY AUDIT:
     - 4 Sidewall Water-Cooled Multi-Function Co-Jet Injectors delivering supersonic oxygen (Mach 2.0, 4,000 Nm3/h)
       for molten bath decarburization and primary post-combustion.
     - Pneumatic Carbon Powder Injection (0 to 60 kg/min) for foamy slag generation to shroud arc radiation.
     - Off-Gas Continuous Emission Monitoring (CEM) in primary duct: CO, CO2, H2, O2.
     - SIL-3 Water Leak Explosion Trip: If H2 concentration exceeds 4.0 vol% in off-gas duct, immediate furnace
       master circuit breaker dump is commanded to prevent violent water-metal explosion.

  7. 16x16 STATE-SPACE & RECEDING-HORIZON MPC OPTIMIZER:
     - Discrete-time state vector x[k] in R^16, control vector u[k] in R^8.
     - Incorporates transformer secondary inductance, Cassie-Mayr conductance, hydraulic oil bulk modulus beta,
       foamy slag height radiation attenuation, and molten bath enthalpy.
     - Quadratic cost minimization: J = x^T * Q * x + u^T * R * u + Delta_u^T * S * Delta_u.

  8. 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) ARCHITECTURE:
     - Redundant Rogowski coils, capacitive dividers, linear optical encoders, and ultrasonic cooling water meters.
     - Median voting with discrepancy timers, fault latches, and bumpless degradation to dual/single channel mode.
*)""")
    
    # 2. VAR_INPUT
    parts.append("""VAR_INPUT
    (* ================================================================================================================
       SECTION 2.1: MASTER SUPERVISORY CONTROL & SAFETY INTERLOCK SIGNALS
       ================================================================================================================ *)
    bMasterEnable                   : BOOL;     (* Master functional automation enable [bool] *)
    bSafetyCircuitHealthy           : BOOL;     (* Hardwired SIL-3 emergency stop circuit healthy [bool] *)
    bAlarmAcknowledgeReset          : BOOL;     (* Operator pushbutton for alarm reset and fault unlatch [bool] *)
    bAutoTapChangerEnable           : BOOL;     (* Enable automatic closed-loop On-Load Tap Changer selection [bool] *)
    bChemicalInjectionEnable        : BOOL;     (* Enable automatic Co-Jet supersonic O2 and carbon dosing [bool] *)
    bFlickerCompensatorEnable       : BOOL;     (* Enable STATCOM / SVC dynamic reactive power fast tracking [bool] *)
    bRoofClosedAndLocked            : BOOL;     (* Proximity limit switches: Roof fully swung and clamped [bool] *)
    bElectrodeMastGantryLocked      : BOOL;     (* Hydraulic mechanical clamp: Mast gantry locked in position [bool] *)

    (* ================================================================================================================
       SECTION 2.2: 2oo3 TRIPLE MODULAR REDUNDANT SECONDARY PHASE CURRENTS [kA]
       ================================================================================================================ *)
    rCurrent_PhaseA_RawA_kA         : REAL;     (* Phase A Secondary Current: Rogowski Coil Transducer A [kA] *)
    rCurrent_PhaseA_RawB_kA         : REAL;     (* Phase A Secondary Current: Rogowski Coil Transducer B [kA] *)
    rCurrent_PhaseA_RawC_kA         : REAL;     (* Phase A Secondary Current: Fiber-Optic Faraday Sensor C [kA] *)
    rCurrent_PhaseB_RawA_kA         : REAL;     (* Phase B Secondary Current: Rogowski Coil Transducer A [kA] *)
    rCurrent_PhaseB_RawB_kA         : REAL;     (* Phase B Secondary Current: Rogowski Coil Transducer B [kA] *)
    rCurrent_PhaseB_RawC_kA         : REAL;     (* Phase B Secondary Current: Fiber-Optic Faraday Sensor C [kA] *)
    rCurrent_PhaseC_RawA_kA         : REAL;     (* Phase C Secondary Current: Rogowski Coil Transducer A [kA] *)
    rCurrent_PhaseC_RawB_kA         : REAL;     (* Phase C Secondary Current: Rogowski Coil Transducer B [kA] *)
    rCurrent_PhaseC_RawC_kA         : REAL;     (* Phase C Secondary Current: Fiber-Optic Faraday Sensor C [kA] *)

    (* ================================================================================================================
       SECTION 2.3: 2oo3 TRIPLE MODULAR REDUNDANT ARC VOLTAGES [V]
       ================================================================================================================ *)
    rVoltage_PhaseA_RawA_V          : REAL;     (* Phase A Arc Voltage: High-Voltage Capacitive Divider A [V] *)
    rVoltage_PhaseA_RawB_V          : REAL;     (* Phase A Arc Voltage: High-Voltage Capacitive Divider B [V] *)
    rVoltage_PhaseA_RawC_V          : REAL;     (* Phase A Arc Voltage: Resistive Potential Transformer C [V] *)
    rVoltage_PhaseB_RawA_V          : REAL;     (* Phase B Arc Voltage: High-Voltage Capacitive Divider A [V] *)
    rVoltage_PhaseB_RawB_V          : REAL;     (* Phase B Arc Voltage: High-Voltage Capacitive Divider B [V] *)
    rVoltage_PhaseB_RawC_V          : REAL;     (* Phase B Arc Voltage: Resistive Potential Transformer C [V] *)
    rVoltage_PhaseC_RawA_V          : REAL;     (* Phase C Arc Voltage: High-Voltage Capacitive Divider A [V] *)
    rVoltage_PhaseC_RawB_V          : REAL;     (* Phase C Arc Voltage: High-Voltage Capacitive Divider B [V] *)
    rVoltage_PhaseC_RawC_V          : REAL;     (* Phase C Arc Voltage: Resistive Potential Transformer C [V] *)

    (* ================================================================================================================
       SECTION 2.4: 2oo3 TRIPLE MODULAR REDUNDANT HYDRAULIC MAST CYLINDER POSITIONS [mm]
       ================================================================================================================ *)
    rMastPos_PhaseA_RawA_mm         : REAL;     (* Mast A Cylinder Displacement: SSI Absolute Linear Scale A [mm] *)
    rMastPos_PhaseA_RawB_mm         : REAL;     (* Mast A Cylinder Displacement: Magnetostrictive LVDT Transducer B [mm] *)
    rMastPos_PhaseA_RawC_mm         : REAL;     (* Mast A Cylinder Displacement: Optical Laser Telemetry Sensor C [mm] *)
    rMastPos_PhaseB_RawA_mm         : REAL;     (* Mast B Cylinder Displacement: SSI Absolute Linear Scale A [mm] *)
    rMastPos_PhaseB_RawB_mm         : REAL;     (* Mast B Cylinder Displacement: Magnetostrictive LVDT Transducer B [mm] *)
    rMastPos_PhaseB_RawC_mm         : REAL;     (* Mast B Cylinder Displacement: Optical Laser Telemetry Sensor C [mm] *)
    rMastPos_PhaseC_RawA_mm         : REAL;     (* Mast C Cylinder Displacement: SSI Absolute Linear Scale A [mm] *)
    rMastPos_PhaseC_RawB_mm         : REAL;     (* Mast C Cylinder Displacement: Magnetostrictive LVDT Transducer B [mm] *)
    rMastPos_PhaseC_RawC_mm         : REAL;     (* Mast C Cylinder Displacement: Optical Laser Telemetry Sensor C [mm] *)

    (* ================================================================================================================
       SECTION 2.5: HYDRAULIC SYSTEM SUPPLY & CYLINDER CHAMBER PRESSURES [bar]
       ================================================================================================================ *)
    rHydraulicSupplyPress_bar       : REAL;     (* Main Hydraulic Ring Main Supply Pressure Transmitter [bar] *)
    rHydraulicReturnPress_bar       : REAL;     (* Main Hydraulic Tank Low-Pressure Return Manifold [bar] *)
    rCylCapPress_PhaseA_bar         : REAL;     (* Mast A Cylinder Cap-End Lifting Chamber Fluid Pressure [bar] *)
    rCylRodPress_PhaseA_bar         : REAL;     (* Mast A Cylinder Rod-End Counterbalance Chamber Fluid Pressure [bar] *)
    rCylCapPress_PhaseB_bar         : REAL;     (* Mast B Cylinder Cap-End Lifting Chamber Fluid Pressure [bar] *)
    rCylRodPress_PhaseB_bar         : REAL;     (* Mast B Cylinder Rod-End Counterbalance Chamber Fluid Pressure [bar] *)
    rCylCapPress_PhaseC_bar         : REAL;     (* Mast C Cylinder Cap-End Lifting Chamber Fluid Pressure [bar] *)
    rCylRodPress_PhaseC_bar         : REAL;     (* Mast C Cylinder Rod-End Counterbalance Chamber Fluid Pressure [bar] *)

    (* ================================================================================================================
       SECTION 2.6: 2oo3 PRIMARY COOLING WATER CIRCUITS [m3/h] & [deg C]
       ================================================================================================================ *)
    rCoolingFlow_Roof_RawA_m3h      : REAL;     (* Water-Cooled Roof Header Flow: Magnetic Inductive Flowmeter A [m3/h] *)
    rCoolingFlow_Roof_RawB_m3h      : REAL;     (* Water-Cooled Roof Header Flow: Ultrasonic Transit-Time Meter B [m3/h] *)
    rCoolingFlow_Roof_RawC_m3h      : REAL;     (* Water-Cooled Roof Header Flow: Differential Pressure Venturi C [m3/h] *)
    rCoolingFlow_Panel_RawA_m3h     : REAL;     (* Water-Cooled Wall Panels Flow: Magnetic Inductive Flowmeter A [m3/h] *)
    rCoolingFlow_Panel_RawB_m3h     : REAL;     (* Water-Cooled Wall Panels Flow: Ultrasonic Transit-Time Meter B [m3/h] *)
    rCoolingFlow_Panel_RawC_m3h     : REAL;     (* Water-Cooled Wall Panels Flow: Differential Pressure Venturi C [m3/h] *)
    rCoolingInletTemp_degC          : REAL;     (* Primary Cooling Water Supply Header Common Temperature [deg C] *)
    rCoolingOutletTemp_Roof_degC    : REAL;     (* Roof Cooling Discharge Manifold Mixed Temperature [deg C] *)
    rCoolingOutletTemp_Panel_degC   : REAL;     (* Sidewall Panel Cooling Discharge Manifold Mixed Temperature [deg C] *)

    (* ================================================================================================================
       SECTION 2.7: OFF-GAS CONTINUOUS EMISSION MONITORING (CEM) IN PRIMARY DUCT [vol %], [deg C], [mbar]
       ================================================================================================================ *)
    rOffGas_CO_vol_pct              : REAL;     (* Continuous Laser Spectrometer: Carbon Monoxide Concentration [vol %] *)
    rOffGas_CO2_vol_pct             : REAL;     (* Continuous Non-Dispersive IR: Carbon Dioxide Concentration [vol %] *)
    rOffGas_H2_vol_pct              : REAL;     (* Continuous Thermal Conductivity Analyzer: Hydrogen Gas [vol %] *)
    rOffGas_O2_vol_pct              : REAL;     (* Paramagnetic Sensor: Residual Excess Oxygen Concentration [vol %] *)
    rOffGas_Temp_degC               : REAL;     (* Primary Water-Cooled Duct Elbow Off-Gas Temperature [deg C] *)
    rOffGas_SuctionPressure_mbar    : REAL;     (* Furnace Primary Exhaust Canopy Static Draught Depression [mbar] *)
    rOffGas_VolFlow_Nm3h            : REAL;     (* Primary Exhaust Baghouse Booster Fan Actual Volumetric Flow [Nm3/h] *)

    (* ================================================================================================================
       SECTION 2.8: 160 MVA FURNACE TRANSFORMER, UTILITY GRID & POWER QUALITY [MVA], [MW], [MVAR], [%]
       ================================================================================================================ *)
    iTransformerTap_Current         : INT;      (* Current Physical Step Position of 18-Step Motorized OLTC [1..18] *)
    rTransformerOilTemp_degC        : REAL;     (* Transformer Top Dielectric Oil Bulk Temperature [deg C] *)
    rTransformerWindingTemp_degC    : REAL;     (* Transformer Secondary Copper Winding Hot-Spot Temperature [deg C] *)
    rGridActivePower_MW             : REAL;     (* Primary High-Voltage 33 kV Substation Active Power Meter [MW] *)
    rGridReactivePower_MVAR         : REAL;     (* Primary High-Voltage 33 kV Substation Reactive Power Meter [MVAR] *)
    rGridFrequency_Hz               : REAL;     (* Utility Interconnection Bus Line Frequency [Hz] *)
    rTHD_Current_pct                : REAL;     (* Real-Time Fast Fourier Harmonic Analyzer: Current THD [%] *)
    rTHD_Voltage_pct                : REAL;     (* Real-Time Fast Fourier Harmonic Analyzer: Voltage THD [%] *)

    (* ================================================================================================================
       SECTION 2.9: METALLURGICAL PROCESS RECIPES, HEAT CHARGE & SETPOINTS
       ================================================================================================================ *)
    rScrapChargeWeight_Ton          : REAL;     (* Total Scrap Mass Charged into Furnace Shell for Current Heat [Ton] *)
    rLiquidSteelBathTemp_degC       : REAL;     (* Periodic Celox Optical/Disposable Thermocouple Bath Probe [deg C] *)
    rTargetImpedance_PhaseA_mOhm    : REAL;     (* Operator/Level-2 Setpoint Arc Impedance Phase A [mOhm] *)
    rTargetImpedance_PhaseB_mOhm    : REAL;     (* Operator/Level-2 Setpoint Arc Impedance Phase B [mOhm] *)
    rTargetImpedance_PhaseC_mOhm    : REAL;     (* Operator/Level-2 Setpoint Arc Impedance Phase C [mOhm] *)
    rTargetSpecificEnergy_kWh_t     : REAL;     (* Heat Specific Electrical Energy Target (< 360 kWh/ton) [kWh/t] *)
    rTargetTappingTemp_degC         : REAL;     (* Metallurgical Aim Tapping Temperature (e.g., 1630 deg C) [deg C] *)
    rMaxOxygenFlow_Nm3h             : REAL;     (* Supersonic Wall Injector Maximum Oxygen Permissible Delivery [Nm3/h] *)
    rMaxCarbonInjection_kgh         : REAL;     (* Pneumatic Slag Foaming Carbon Dispenser Max Feed Rate [kg/h] *)
END_VAR""")
    
    # 3. VAR_OUTPUT
    parts.append("""VAR_OUTPUT
    (* ================================================================================================================
       SECTION 3.1: ELECTROHYDRAULIC SERVO VALVE POSITION COMMANDS [-100.0% to +100.0%]
       ================================================================================================================ *)
    rServoCmd_MastA_pct             : REAL;     (* Moog Servo Valve Spool Command Phase A: Raise(+)/Lower(-) [%] *)
    rServoCmd_MastB_pct             : REAL;     (* Moog Servo Valve Spool Command Phase B: Raise(+)/Lower(-) [%] *)
    rServoCmd_MastC_pct             : REAL;     (* Moog Servo Valve Spool Command Phase C: Raise(+)/Lower(-) [%] *)

    (* ================================================================================================================
       SECTION 3.2: 160 MVA TRANSFORMER ON-LOAD TAP CHANGER (OLTC) STEP COMMANDS
       ================================================================================================================ *)
    iTransformerTap_Command         : INT;      (* Demanded Target Tap Changer Step Position [1..18] *)
    bTapRaisePulse                  : BOOL;     (* One-Shot Discrete Digital Pulse to Step Motor: Raise Tap [bool] *)
    bTapLowerPulse                  : BOOL;     (* One-Shot Discrete Digital Pulse to Step Motor: Lower Tap [bool] *)

    (* ================================================================================================================
       SECTION 3.3: CO-JET CHEMICAL INJECTION & COMBUSTION ACTUATOR SETPOINTS
       ================================================================================================================ *)
    rOxygenFlowCmd_Nm3h             : REAL;     (* Supersonic Main Decarburization Oxygen Flow Setpoint [Nm3/h] *)
    rCarbonFlowCmd_kgh              : REAL;     (* Pneumatic Carbon Powder Feeder Mass Flow Setpoint [kg/h] *)
    rPostCombustionO2_Nm3h          : REAL;     (* Secondary Post-Combustion Ring Header Oxygen Delivery [Nm3/h] *)

    (* ================================================================================================================
       SECTION 3.4: ARC ELECTRICAL IMPEDANCES, RESISTANCES & POWER FEEDBACKS
       ================================================================================================================ *)
    rArcImpedance_PhaseA_mOhm       : REAL;     (* 2oo3 Evaluated Dynamic Arc Impedance Phase A [mOhm] *)
    rArcImpedance_PhaseB_mOhm       : REAL;     (* 2oo3 Evaluated Dynamic Arc Impedance Phase B [mOhm] *)
    rArcImpedance_PhaseC_mOhm       : REAL;     (* 2oo3 Evaluated Dynamic Arc Impedance Phase C [mOhm] *)
    rArcResistance_PhaseA_mOhm      : REAL;     (* Dynamic Cassie-Mayr Arc Resistance Phase A [mOhm] *)
    rArcResistance_PhaseB_mOhm      : REAL;     (* Dynamic Cassie-Mayr Arc Resistance Phase B [mOhm] *)
    rArcResistance_PhaseC_mOhm      : REAL;     (* Dynamic Cassie-Mayr Arc Resistance Phase C [mOhm] *)
    rActivePower_Total_MW           : REAL;     (* Total Dissipated Active Arc & Bath Power in Furnace [MW] *)
    rReactivePower_Total_MVAR       : REAL;     (* Total Fundamental Reactive Power Drawn by Arc [MVAR] *)
    rFurnacePowerFactor             : REAL;     (* Instantaneous Operating Furnace Power Factor cos(phi) [-] *)
    rSpecificEnergyDelivered_kWh_t  : REAL;     (* Cumulative Electrical Energy Consumption per Ton of Charge [kWh/t] *)

    (* ================================================================================================================
       SECTION 3.5: FLICKER, SVC STATCOM & CHEMICAL EFFICIENCY METRICS
       ================================================================================================================ *)
    rSVC_ReactiveDemand_MVAR        : REAL;     (* Static Var Compensator Fast Reactive Power Offset Demand [MVAR] *)
    rFlickerPst_Estimate            : REAL;     (* Calculated Short-Term Flicker Severity Pst Approximation [-] *)
    rChemicalPowerRecovered_MW      : REAL;     (* Thermal Power Yield from In-Furnace CO/H2 Post-Combustion [MW] *)
    rPostCombustionRatio_pct        : REAL;     (* Calculated Primary Off-Gas Post-Combustion Ratio [%] *)
    rFoamSlagAcousticIndex_pct      : REAL;     (* Slag Foaming Level & Arc Shrouding Acoustic Sensor Metric [%] *)

    (* ================================================================================================================
       SECTION 3.6: SYSTEM OPERATIONAL STATUS, INTERLOCKS & DYNAMIC OVERRIDES
       ================================================================================================================ *)
    iCurrentFSMState                : INT;      (* 12-Stage Heavy Industrial Operational FSM State Index [0..11] *)
    bSystemHealthy                  : BOOL;     (* All safety, cooling, hydraulic and grid interlocks satisfied [bool] *)
    bArcIgnited_PhaseA              : BOOL;     (* Stable arc column active and conducting on Phase A [bool] *)
    bArcIgnited_PhaseB              : BOOL;     (* Stable arc column active and conducting on Phase B [bool] *)
    bArcIgnited_PhaseC              : BOOL;     (* Stable arc column active and conducting on Phase C [bool] *)
    bScrapCaveIn_PhaseA             : BOOL;     (* Phase A fast scrap collapse upward override active [bool] *)
    bScrapCaveIn_PhaseB             : BOOL;     (* Phase B fast scrap collapse upward override active [bool] *)
    bScrapCaveIn_PhaseC             : BOOL;     (* Phase C fast scrap collapse upward override active [bool] *)
    bArcBreak_PhaseA                : BOOL;     (* Phase A arc extinguished, fast strike plunge active [bool] *)
    bArcBreak_PhaseB                : BOOL;     (* Phase B arc extinguished, fast strike plunge active [bool] *)
    bArcBreak_PhaseC                : BOOL;     (* Phase C arc extinguished, fast strike plunge active [bool] *)
    bWaterLeakExplosionHazard       : BOOL;     (* SIL-3 Critical Trip: Off-Gas H2 exceeds safe threshold [bool] *)
    bEmergencyMasterArcTrip         : BOOL;     (* SIL-3 Master Circuit Breaker High-Speed Dump Commanded [bool] *)

    (* ================================================================================================================
       SECTION 3.7: ISA-18.2 ALARM TELEMETRY & TMR DIAGNOSTIC DWORDS
       ================================================================================================================ *)
    dwAlarmWord_1                   : DWORD;    (* Critical Emergency Trip Alarm Bitmask (HH Level SIL-3) *)
    dwAlarmWord_2                   : DWORD;    (* Process Warning & Operational Anomaly Bitmask (H / L Level) *)
    dwAlarmWord_3                   : DWORD;    (* Power Quality, Thermal & Grid Stability Bitmask *)
    dwTMR_Diagnostic_1              : DWORD;    (* 2oo3 Sensor Channel Discrepancy & Health Bitmask 1 *)
    dwTMR_Diagnostic_2              : DWORD;    (* 2oo3 Sensor Channel Discrepancy & Health Bitmask 2 *)
END_VAR""")
    
    # 4. VAR internal
    parts.append("""VAR
    (* ================================================================================================================
       SECTION 4.1: PHYSICAL, HYDRAULIC, ELECTRICAL & METALLURGICAL SYSTEM CONSTANTS
       ================================================================================================================ *)
    c_rSamplingPeriod_sec           : REAL := 0.001;    (* Deterministic execution interval Ts = 1.0 ms (1000 Hz) *)
    c_rPi                           : REAL := 3.141592653589793;
    c_rRatedCurrent_kA              : REAL := 77.0;     (* Nominal rated secondary phase RMS current [kA] *)
    c_rShortCircuitTripCurrent_kA   : REAL := 192.5;    (* Scrap cave-in instant trip threshold (2.5 * I_nominal) [kA] *)
    c_rArcExtinguishThreshold_kA    : REAL := 6.16;     (* Arc break detection threshold (0.08 * I_nominal) [kA] *)
    c_rArcStrikeDetection_kA        : REAL := 23.1;     (* Minimum arc strike recognition threshold (0.30 * I_nom) [kA] *)
    c_rHydraulicBulkModulus_bar     : REAL := 16000.0;  (* Effective hydraulic fluid bulk modulus beta [bar] *)
    c_rCylinderPistonArea_cm2       : REAL := 490.87;   (* Cylinder bore 250 mm area: (pi/4)*25^2 [cm2] *)
    c_rCylinderAnnulusArea_cm2      : REAL := 236.40;   (* Cylinder rod 180 mm annulus: (pi/4)*(25^2 - 18^2) [cm2] *)
    c_rMastAssemblyMass_kg          : REAL := 18500.0;  (* Total mast arm, electrode clamp, and graphite column mass [kg] *)
    c_rMaxMastVelocity_mms          : REAL := 250.0;    (* Max electrohydraulic mast stroke rate [mm/s] *)
    c_rMaxMastAcceleration_mms2     : REAL := 8000.0;   (* Max electrohydraulic mast acceleration [mm/s2] *)
    c_rMaxMastStroke_mm             : REAL := 4500.0;   (* Maximum mechanical travel of electrode mast [mm] *)
    c_rMinMastStroke_mm             : REAL := 50.0;     (* Lower mechanical travel hard-stop [mm] *)
    c_rRoofCoolingNominalFlow_m3h   : REAL := 550.0;    (* Design cooling water flow rate through roof circuit [m3/h] *)
    c_rPanelCoolingNominalFlow_m3h  : REAL := 750.0;    (* Design cooling water flow rate through wall panel circuit [m3/h] *)

    (* ================================================================================================================
       SECTION 4.2: CASSIE-MAYR DYNAMIC ARC MODEL PARAMETERS
       ================================================================================================================ *)
    c_rCassieTimeConst_sec          : REAL := 0.00085;  (* Cassie dynamic thermal cooling time constant theta_C [s] *)
    c_rMayrTimeConst_sec            : REAL := 0.00165;  (* Mayr dynamic thermal cooling time constant theta_M [s] *)
    c_rArcFieldConstant_E0          : REAL := 11.8;     (* Steady-state Cassie arc column field gradient [V/cm] *)
    c_rArcLengthSensitivity_alpha   : REAL := 0.35;     (* Gradient expansion coefficient per cm of arc elongation *)
    c_rMayrCoolingPower_P0          : REAL := 4.2E6;    (* Mayr zero-crossing cooling dissipation power P0 [W] *)
    c_rTransitionCurrent_I0         : REAL := 10.5;     (* Conductance regime transition threshold current [kA] *)

    (* Dynamic Conductance State Registers *)
    rArcConductance_PhaseA_S        : REAL := 35.0;     (* Phase A Dynamic Conductance g_A [Siemens] *)
    rArcConductance_PhaseB_S        : REAL := 35.0;     (* Phase B Dynamic Conductance g_B [Siemens] *)
    rArcConductance_PhaseC_S        : REAL := 35.0;     (* Phase C Dynamic Conductance g_C [Siemens] *)
    rArcLength_PhaseA_cm            : REAL := 18.0;     (* Estimated arc column physical length Phase A [cm] *)
    rArcLength_PhaseB_cm            : REAL := 18.0;     (* Estimated arc column physical length Phase B [cm] *)
    rArcLength_PhaseC_cm            : REAL := 18.0;     (* Estimated arc column physical length Phase C [cm] *)

    (* ================================================================================================================
       SECTION 4.3: 2oo3 TMR VOTING VARIABLES, THRESHOLDS & PERSISTENT FAULT COUNTERS
       ================================================================================================================ *)
    c_rCurrentDiscrepancyLimit_kA   : REAL := 6.5;      (* Permissible secondary current deviation between sensors [kA] *)
    c_rVoltageDiscrepancyLimit_V    : REAL := 45.0;     (* Permissible arc voltage deviation between sensors [V] *)
    c_rPositionDiscrepancyLimit_mm  : REAL := 8.0;      (* Permissible mast position deviation between sensors [mm] *)
    c_rFlowDiscrepancyLimit_m3h     : REAL := 40.0;     (* Permissible cooling flow deviation between sensors [m3/h] *)

    (* 2oo3 Voted Real Feedback Variables *)
    rVotedCurrent_PhaseA_kA         : REAL := 0.0;
    rVotedCurrent_PhaseB_kA         : REAL := 0.0;
    rVotedCurrent_PhaseC_kA         : REAL := 0.0;
    rVotedVoltage_PhaseA_V          : REAL := 0.0;
    rVotedVoltage_PhaseB_V          : REAL := 0.0;
    rVotedVoltage_PhaseC_V          : REAL := 0.0;
    rVotedMastPos_PhaseA_mm         : REAL := 2200.0;
    rVotedMastPos_PhaseB_mm         : REAL := 2200.0;
    rVotedMastPos_PhaseC_mm         : REAL := 2200.0;
    rVotedCoolingFlow_Roof_m3h      : REAL := 550.0;
    rVotedCoolingFlow_Panel_m3h     : REAL := 750.0;

    (* TMR Channel Fault Counters *)
    iCurrentFaultCount_A_RawA       : INT := 0;  iCurrentFaultCount_A_RawB : INT := 0;  iCurrentFaultCount_A_RawC : INT := 0;
    iCurrentFaultCount_B_RawA       : INT := 0;  iCurrentFaultCount_B_RawB : INT := 0;  iCurrentFaultCount_B_RawC : INT := 0;
    iCurrentFaultCount_C_RawA       : INT := 0;  iCurrentFaultCount_C_RawB : INT := 0;  iCurrentFaultCount_C_RawC : INT := 0;
    iVoltageFaultCount_A_RawA       : INT := 0;  iVoltageFaultCount_A_RawB : INT := 0;  iVoltageFaultCount_A_RawC : INT := 0;
    iVoltageFaultCount_B_RawA       : INT := 0;  iVoltageFaultCount_B_RawB : INT := 0;  iVoltageFaultCount_B_RawC : INT := 0;
    iVoltageFaultCount_C_RawA       : INT := 0;  iVoltageFaultCount_C_RawB : INT := 0;  iVoltageFaultCount_C_RawC : INT := 0;
    iMastPosFaultCount_A_RawA       : INT := 0;  iMastPosFaultCount_A_RawB : INT := 0;  iMastPosFaultCount_A_RawC : INT := 0;
    iMastPosFaultCount_B_RawA       : INT := 0;  iMastPosFaultCount_B_RawB : INT := 0;  iMastPosFaultCount_B_RawC : INT := 0;
    iMastPosFaultCount_C_RawA       : INT := 0;  iMastPosFaultCount_C_RawB : INT := 0;  iMastPosFaultCount_C_RawC : INT := 0;
    iCoolingFaultCount_Roof_RawA    : INT := 0;  iCoolingFaultCount_Roof_RawB : INT := 0;  iCoolingFaultCount_Roof_RawC : INT := 0;
    iCoolingFaultCount_Panel_RawA   : INT := 0;  iCoolingFaultCount_Panel_RawB : INT := 0;  iCoolingFaultCount_Panel_RawC : INT := 0;

    (* Degradation Flags *)
    bDegradedCurrent_PhaseA         : BOOL := FALSE;
    bDegradedCurrent_PhaseB         : BOOL := FALSE;
    bDegradedCurrent_PhaseC         : BOOL := FALSE;
    bDegradedVoltage_PhaseA         : BOOL := FALSE;
    bDegradedVoltage_PhaseB         : BOOL := FALSE;
    bDegradedVoltage_PhaseC         : BOOL := FALSE;
    bDegradedMastPos_PhaseA         : BOOL := FALSE;
    bDegradedMastPos_PhaseB         : BOOL := FALSE;
    bDegradedMastPos_PhaseC         : BOOL := FALSE;
    bDegradedCooling_Roof           : BOOL := FALSE;
    bDegradedCooling_Panel          : BOOL := FALSE;

    (* ================================================================================================================
       SECTION 4.4: 16x16 DISCRETE STATE-SPACE MATRICES & MPC OPTIMIZATION REGISTERS
       ================================================================================================================ *)
    matA                            : ARRAY[1..16, 1..16] OF REAL;  (* Discrete Plant Transition Matrix (16x16) *)
    matB                            : ARRAY[1..16, 1..8] OF REAL;   (* Discrete Input Coupling Matrix (16x8) *)
    matC                            : ARRAY[1..8, 1..16] OF REAL;   (* Discrete Measurement Output Matrix (8x16) *)
    matD                            : ARRAY[1..8, 1..8] OF REAL;    (* Direct Feedthrough Matrix (8x8) *)

    vecState_x                      : ARRAY[1..16] OF REAL;         (* Current State Vector x[k] in R^16 *)
    vecStateTarget_x                : ARRAY[1..16] OF REAL;         (* Reference Target State Vector in R^16 *)
    vecStateNext_x                  : ARRAY[1..16] OF REAL;         (* Predicted Future State Vector x[k+1] *)
    vecControl_u                    : ARRAY[1..8] OF REAL;          (* Optimized Actuator Command Vector u[k] in R^8 *)
    vecControlPrev_u                : ARRAY[1..8] OF REAL;          (* Previous Step Actuator Vector u[k-1] in R^8 *)
    vecDeltaControl_du              : ARRAY[1..8] OF REAL;          (* Rate-of-Change Vector du[k] = u[k] - u[k-1] *)
    vecGradient_g                   : ARRAY[1..8] OF REAL;          (* Quadratic Cost Function Gradient Vector in R^8 *)

    (* MPC Quadratic Cost Penalties *)
    vecCostWeight_Q                 : ARRAY[1..16] OF REAL;         (* State Tracking Error Weight Matrix Diagonal Q *)
    vecCostWeight_R                 : ARRAY[1..8] OF REAL;          (* Actuator Effort Weight Matrix Diagonal R *)
    vecCostWeight_S                 : ARRAY[1..8] OF REAL;          (* Actuator Slew Rate Slew Weight Matrix Diagonal S *)
    vecCostWeight_P                 : ARRAY[1..16] OF REAL;         (* Terminal Horizon State Penalty Vector P *)

    (* Actuator Hard Saturation & Slew Bounds *)
    vecControlMin_u                 : ARRAY[1..8] OF REAL;
    vecControlMax_u                 : ARRAY[1..8] OF REAL;
    vecDeltaMax_du                  : ARRAY[1..8] OF REAL;

    rMPC_StepAlpha                  : REAL := 0.0185;               (* Projected Gradient Descent Learning Rate *)
    iMPC_MaxIterations              : INT := 8;                     (* Inner Loop Receding Horizon Solver Iterations *)
    bMPC_MatricesInitialized        : BOOL := FALSE;

    (* ================================================================================================================
       SECTION 4.5: FAST DERIVATIVES, CAVE-IN OVERRIDE & ARC BREAK REGISTERS
       ================================================================================================================ *)
    rPrevCurrent_PhaseA_kA          : REAL := 0.0;
    rPrevCurrent_PhaseB_kA          : REAL := 0.0;
    rPrevCurrent_PhaseC_kA          : REAL := 0.0;
    rDerivCurrent_PhaseA_kA_s       : REAL := 0.0;
    rDerivCurrent_PhaseB_kA_s       : REAL := 0.0;
    rDerivCurrent_PhaseC_kA_s       : REAL := 0.0;

    rPrevOffGas_H2_vol_pct          : REAL := 0.0;
    rDerivOffGas_H2_pct_s           : REAL := 0.0;

    tCaveInHoldTimer_A              : TON;
    tCaveInHoldTimer_B              : TON;
    tCaveInHoldTimer_C              : TON;
    tArcBreakHoldTimer_A            : TON;
    tArcBreakHoldTimer_B            : TON;
    tArcBreakHoldTimer_C            : TON;

    rCaveInFastRetractCmd_pct       : REAL := 100.0;                (* Full upwards servo spool slew [100.0%] *)
    rArcBreakFastPlungeCmd_pct      : REAL := -60.0;                (* Fast downwards search plunge [-60.0%] *)

    (* ================================================================================================================
       SECTION 4.6: POWER QUALITY, FLICKER FILTER & SVC INTERFACE
       ================================================================================================================ *)
    rFlickerFilterState_1           : REAL := 0.0;                  (* IEC 61000-4-15 8.8 Hz Bandpass State 1 *)
    rFlickerFilterState_2           : REAL := 0.0;                  (* IEC 61000-4-15 8.8 Hz Bandpass State 2 *)
    rInstantaneousSensation_S       : REAL := 0.0;                  (* Demodulated eye-brain flicker perception S(t) *)
    rShortTermFlickerAccumulator    : REAL := 0.0;
    iFlickerSampleCounter           : DINT := 0;

    (* ================================================================================================================
       SECTION 4.7: CO-JET THERMOCHEMISTRY & FOAMY SLAG REGISTERS
       ================================================================================================================ *)
    rCalculatedFoamHeight_mm        : REAL := 120.0;                (* Current estimated foamy slag depth [mm] *)
    rRadiationShieldingFactor       : REAL := 0.45;                 (* Thermal radiation opacity factor (0.0 to 1.0) *)
    rSpecificHeatSteel_kJ_kgK       : REAL := 0.68;                 (* Molten steel specific heat capacity *)
    rEnthalpyDecarburization_kJ_mol : REAL := 111.0;                (* C + 0.5 O2 -> CO exothermic yield *)
    rEnthalpyPostCombustion_kJ_mol  : REAL := 283.0;                (* CO + 0.5 O2 -> CO2 exothermic yield *)
    rEnthalpyHydrogenComb_kJ_mol    : REAL := 242.0;                (* H2 + 0.5 O2 -> H2O exothermic yield *)

    (* Cumulative Energy Integrators *)
    rCumulativeActiveEnergy_MWh     : REAL := 0.0;
    rCumulativeOxygen_Nm3           : REAL := 0.0;
    rCumulativeCarbon_kg            : REAL := 0.0;

    (* ================================================================================================================
       SECTION 4.8: 12-STAGE OPERATIONAL FINITE STATE MACHINE (FSM) TIMERS & REGISTERS
       ================================================================================================================ *)
    iState                          : INT := 0;                     (* Internal FSM operational state pointer *)
    tFSM_StateTimer                 : TON;                          (* General dwell and state duration timer *)
    tTapChangeDwellTimer            : TON;                          (* Minimum dwell time between OLTC tap shifts *)
    tBoringPhaseTimer               : TON;                          (* Scrap boring cycle elapsed timer *)
    tRefiningPhaseTimer             : TON;                          (* Bath refining superheating elapsed timer *)
    tRoofSwingTimer                 : TON;                          (* Roof traverse and locking safety monitor *)

    (* Tap Changer Pulse Engine *)
    bTapPulseActive                 : BOOL := FALSE;
    tTapPulseTimer                  : TON;
    iTargetTapMemory                : INT := 6;

    (* ================================================================================================================
       SECTION 4.9: ISA-18.2 ALARM MATRIX TRIP POINTS, HYSTERESIS & DIAGNOSTICS
       ================================================================================================================ *)
    c_rCurrentTripHH_kA             : REAL := 185.0;                (* SIL-3 Overcurrent trip limit [kA] *)
    c_rPanelTempTripHH_degC         : REAL := 82.0;                 (* Cooling water wall panel high runaway trip [deg C] *)
    c_rPanelTempWarnH_degC          : REAL := 70.0;                 (* Cooling water wall panel temperature warning [deg C] *)
    c_rRoofCoolingLowTripLL_m3h     : REAL := 380.0;                (* Roof cooling minimum water flow trip [m3/h] *)
    c_rPanelCoolingLowTripLL_m3h    : REAL := 520.0;                (* Wall panel minimum water flow trip [m3/h] *)
    c_rOffGasH2_TripHH_pct          : REAL := 4.0;                  (* Off-Gas Hydrogen explosion hazard trip [vol %] *)
    c_rOffGasH2_WarnH_pct           : REAL := 2.5;                  (* Off-Gas Hydrogen water leak warning [vol %] *)
    c_rHydraulicLowPressTripLL_bar  : REAL := 120.0;                (* Hydraulic accumulator main pressure trip [bar] *)
    c_rTransformerWindingTripHH_degC: REAL := 115.0;                (* Transformer winding hot-spot trip limit [deg C] *)
    c_rAlarmHysteresis_degC         : REAL := 2.5;                  (* Temperature alarm deadband hysteresis *)
    c_rAlarmHysteresis_m3h          : REAL := 15.0;                 (* Flow alarm deadband hysteresis *)

    (* Latched Trip Flags *)
    bTripLatched_Overcurrent        : BOOL := FALSE;
    bTripLatched_WaterLeakExplosion : BOOL := FALSE;
    bTripLatched_CoolingLoss        : BOOL := FALSE;
    bTripLatched_TransformerOvertemp: BOOL := FALSE;
    bTripLatched_HydraulicFailure   : BOOL := FALSE;

    (* Loop and Math Iteration Indices *)
    iIdx                            : INT := 1;
    jIdx                            : INT := 1;
    kIdx                            : INT := 1;
    rTempDotProduct                 : REAL := 0.0;
    rTempDiff                       : REAL := 0.0;
END_VAR""")
    
    # 5. SECTION 1: MASTER SAFETY & EMERGENCY TRIP
    parts.append("""(* ====================================================================================================================
   SECTION 1: HARD SAFETY CIRCUIT, SIL-3 CIRCUIT BREAKER ARC TRIP & EMERGENCY SHUTDOWN INTERLOCK
   ==================================================================================================================== *)
IF (NOT bSafetyCircuitHealthy) OR bEmergencyMasterArcTrip OR bTripLatched_WaterLeakExplosion THEN
    bSystemHealthy                  := FALSE;
    bEmergencyMasterArcTrip         := TRUE;
    iTransformerTap_Command         := 1;           (* Command minimum voltage tap step *)
    bTapRaisePulse                  := FALSE;
    bTapLowerPulse                  := FALSE;

    (* Depressurize servo valves, command high-speed hydraulic mast full upward retraction *)
    rServoCmd_MastA_pct             := c_rMaxMastVelocity_mms;
    rServoCmd_MastB_pct             := c_rMaxMastVelocity_mms;
    rServoCmd_MastC_pct             := c_rMaxMastVelocity_mms;

    (* Isolate supersonic oxygen, post-combustion headers, and pneumatic carbon dispensers immediately *)
    rOxygenFlowCmd_Nm3h             := 0.0;
    rCarbonFlowCmd_kgh              := 0.0;
    rPostCombustionO2_Nm3h          := 0.0;
    rSVC_ReactiveDemand_MVAR        := 0.0;

    bArcIgnited_PhaseA              := FALSE;
    bArcIgnited_PhaseB              := FALSE;
    bArcIgnited_PhaseC              := FALSE;

    dwAlarmWord_1.0                 := NOT bSafetyCircuitHealthy;
    dwAlarmWord_1.1                 := bTripLatched_WaterLeakExplosion;

    iState := 11;                   (* State 11: Emergency Fast Arc Trip & SIL-3 Nitrogen Blast Dump *)
    iCurrentFSMState := iState;
    RETURN;
END_IF;""")
    
    # 6. SECTION 2: 2oo3 TMR SENSOR VOTING
    parts.append("""(* ====================================================================================================================
   SECTION 2: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING & HEALTH PLAUSIBILITY ENGINE
   ==================================================================================================================== *)
(* --- 2.1 SECONDARY PHASE A CURRENT 2oo3 VOTER --- *)
IF (ABS(rCurrent_PhaseA_RawA_kA - rCurrent_PhaseA_RawB_kA) <= c_rCurrentDiscrepancyLimit_kA) THEN
    IF (ABS(rCurrent_PhaseA_RawA_kA - rCurrent_PhaseA_RawC_kA) <= c_rCurrentDiscrepancyLimit_kA) THEN
        IF (rCurrent_PhaseA_RawA_kA >= rCurrent_PhaseA_RawB_kA AND rCurrent_PhaseA_RawA_kA <= rCurrent_PhaseA_RawC_kA) OR
           (rCurrent_PhaseA_RawA_kA <= rCurrent_PhaseA_RawB_kA AND rCurrent_PhaseA_RawA_kA >= rCurrent_PhaseA_RawC_kA) THEN
            rVotedCurrent_PhaseA_kA := rCurrent_PhaseA_RawA_kA;
        ELSIF (rCurrent_PhaseA_RawB_kA >= rCurrent_PhaseA_RawA_kA AND rCurrent_PhaseA_RawB_kA <= rCurrent_PhaseA_RawC_kA) OR
              (rCurrent_PhaseA_RawB_kA <= rCurrent_PhaseA_RawA_kA AND rCurrent_PhaseA_RawB_kA >= rCurrent_PhaseA_RawC_kA) THEN
            rVotedCurrent_PhaseA_kA := rCurrent_PhaseA_RawB_kA;
        ELSE
            rVotedCurrent_PhaseA_kA := rCurrent_PhaseA_RawC_kA;
        END_IF;
        iCurrentFaultCount_A_RawA := 0;  iCurrentFaultCount_A_RawB := 0;  iCurrentFaultCount_A_RawC := 0;
        bDegradedCurrent_PhaseA := FALSE;
    ELSE
        rVotedCurrent_PhaseA_kA := 0.5 * (rCurrent_PhaseA_RawA_kA + rCurrent_PhaseA_RawB_kA);
        iCurrentFaultCount_A_RawC := iCurrentFaultCount_A_RawC + 1;
        bDegradedCurrent_PhaseA := TRUE;
    END_IF;
ELSIF (ABS(rCurrent_PhaseA_RawA_kA - rCurrent_PhaseA_RawC_kA) <= c_rCurrentDiscrepancyLimit_kA) THEN
    rVotedCurrent_PhaseA_kA := 0.5 * (rCurrent_PhaseA_RawA_kA + rCurrent_PhaseA_RawC_kA);
    iCurrentFaultCount_A_RawB := iCurrentFaultCount_A_RawB + 1;
    bDegradedCurrent_PhaseA := TRUE;
ELSIF (ABS(rCurrent_PhaseA_RawB_kA - rCurrent_PhaseA_RawC_kA) <= c_rCurrentDiscrepancyLimit_kA) THEN
    rVotedCurrent_PhaseA_kA := 0.5 * (rCurrent_PhaseA_RawB_kA + rCurrent_PhaseA_RawC_kA);
    iCurrentFaultCount_A_RawA := iCurrentFaultCount_A_RawA + 1;
    bDegradedCurrent_PhaseA := TRUE;
ELSE
    rVotedCurrent_PhaseA_kA := rCurrent_PhaseA_RawA_kA;
    bDegradedCurrent_PhaseA := TRUE;
END_IF;

(* --- 2.2 SECONDARY PHASE B CURRENT 2oo3 VOTER --- *)
IF (ABS(rCurrent_PhaseB_RawA_kA - rCurrent_PhaseB_RawB_kA) <= c_rCurrentDiscrepancyLimit_kA) THEN
    IF (ABS(rCurrent_PhaseB_RawA_kA - rCurrent_PhaseB_RawC_kA) <= c_rCurrentDiscrepancyLimit_kA) THEN
        IF (rCurrent_PhaseB_RawA_kA >= rCurrent_PhaseB_RawB_kA AND rCurrent_PhaseB_RawA_kA <= rCurrent_PhaseB_RawC_kA) OR
           (rCurrent_PhaseB_RawA_kA <= rCurrent_PhaseB_RawB_kA AND rCurrent_PhaseB_RawA_kA >= rCurrent_PhaseB_RawC_kA) THEN
            rVotedCurrent_PhaseB_kA := rCurrent_PhaseB_RawA_kA;
        ELSIF (rCurrent_PhaseB_RawB_kA >= rCurrent_PhaseB_RawA_kA AND rCurrent_PhaseB_RawB_kA <= rCurrent_PhaseB_RawC_kA) OR
              (rCurrent_PhaseB_RawB_kA <= rCurrent_PhaseB_RawA_kA AND rCurrent_PhaseB_RawB_kA >= rCurrent_PhaseB_RawC_kA) THEN
            rVotedCurrent_PhaseB_kA := rCurrent_PhaseB_RawB_kA;
        ELSE
            rVotedCurrent_PhaseB_kA := rCurrent_PhaseB_RawC_kA;
        END_IF;
        iCurrentFaultCount_B_RawA := 0;  iCurrentFaultCount_B_RawB := 0;  iCurrentFaultCount_B_RawC := 0;
        bDegradedCurrent_PhaseB := FALSE;
    ELSE
        rVotedCurrent_PhaseB_kA := 0.5 * (rCurrent_PhaseB_RawA_kA + rCurrent_PhaseB_RawB_kA);
        iCurrentFaultCount_B_RawC := iCurrentFaultCount_B_RawC + 1;
        bDegradedCurrent_PhaseB := TRUE;
    END_IF;
ELSIF (ABS(rCurrent_PhaseB_RawA_kA - rCurrent_PhaseB_RawC_kA) <= c_rCurrentDiscrepancyLimit_kA) THEN
    rVotedCurrent_PhaseB_kA := 0.5 * (rCurrent_PhaseB_RawA_kA + rCurrent_PhaseB_RawC_kA);
    iCurrentFaultCount_B_RawB := iCurrentFaultCount_B_RawB + 1;
    bDegradedCurrent_PhaseB := TRUE;
ELSIF (ABS(rCurrent_PhaseB_RawB_kA - rCurrent_PhaseB_RawC_kA) <= c_rCurrentDiscrepancyLimit_kA) THEN
    rVotedCurrent_PhaseB_kA := 0.5 * (rCurrent_PhaseB_RawB_kA + rCurrent_PhaseB_RawC_kA);
    iCurrentFaultCount_B_RawA := iCurrentFaultCount_B_RawA + 1;
    bDegradedCurrent_PhaseB := TRUE;
ELSE
    rVotedCurrent_PhaseB_kA := rCurrent_PhaseB_RawB_kA;
    bDegradedCurrent_PhaseB := TRUE;
END_IF;

(* --- 2.3 SECONDARY PHASE C CURRENT 2oo3 VOTER --- *)
IF (ABS(rCurrent_PhaseC_RawA_kA - rCurrent_PhaseC_RawB_kA) <= c_rCurrentDiscrepancyLimit_kA) THEN
    IF (ABS(rCurrent_PhaseC_RawA_kA - rCurrent_PhaseC_RawC_kA) <= c_rCurrentDiscrepancyLimit_kA) THEN
        IF (rCurrent_PhaseC_RawA_kA >= rCurrent_PhaseC_RawB_kA AND rCurrent_PhaseC_RawA_kA <= rCurrent_PhaseC_RawC_kA) OR
           (rCurrent_PhaseC_RawA_kA <= rCurrent_PhaseC_RawB_kA AND rCurrent_PhaseC_RawA_kA >= rCurrent_PhaseC_RawC_kA) THEN
            rVotedCurrent_PhaseC_kA := rCurrent_PhaseC_RawA_kA;
        ELSIF (rCurrent_PhaseC_RawB_kA >= rCurrent_PhaseC_RawA_kA AND rCurrent_PhaseC_RawB_kA <= rCurrent_PhaseC_RawC_kA) OR
              (rCurrent_PhaseC_RawB_kA <= rCurrent_PhaseC_RawA_kA AND rCurrent_PhaseC_RawB_kA >= rCurrent_PhaseC_RawC_kA) THEN
            rVotedCurrent_PhaseC_kA := rCurrent_PhaseC_RawB_kA;
        ELSE
            rVotedCurrent_PhaseC_kA := rCurrent_PhaseC_RawC_kA;
        END_IF;
        iCurrentFaultCount_C_RawA := 0;  iCurrentFaultCount_C_RawB := 0;  iCurrentFaultCount_C_RawC := 0;
        bDegradedCurrent_PhaseC := FALSE;
    ELSE
        rVotedCurrent_PhaseC_kA := 0.5 * (rCurrent_PhaseC_RawA_kA + rCurrent_PhaseC_RawB_kA);
        iCurrentFaultCount_C_RawC := iCurrentFaultCount_C_RawC + 1;
        bDegradedCurrent_PhaseC := TRUE;
    END_IF;
ELSIF (ABS(rCurrent_PhaseC_RawA_kA - rCurrent_PhaseC_RawC_kA) <= c_rCurrentDiscrepancyLimit_kA) THEN
    rVotedCurrent_PhaseC_kA := 0.5 * (rCurrent_PhaseC_RawA_kA + rCurrent_PhaseC_RawC_kA);
    iCurrentFaultCount_C_RawB := iCurrentFaultCount_C_RawB + 1;
    bDegradedCurrent_PhaseC := TRUE;
ELSIF (ABS(rCurrent_PhaseC_RawB_kA - rCurrent_PhaseC_RawC_kA) <= c_rCurrentDiscrepancyLimit_kA) THEN
    rVotedCurrent_PhaseC_kA := 0.5 * (rCurrent_PhaseC_RawB_kA + rCurrent_PhaseC_RawC_kA);
    iCurrentFaultCount_C_RawA := iCurrentFaultCount_C_RawA + 1;
    bDegradedCurrent_PhaseC := TRUE;
ELSE
    rVotedCurrent_PhaseC_kA := rCurrent_PhaseC_RawC_kA;
    bDegradedCurrent_PhaseC := TRUE;
END_IF;

(* --- 2.4 ARC VOLTAGE PHASE A 2oo3 VOTER --- *)
IF (ABS(rVoltage_PhaseA_RawA_V - rVoltage_PhaseA_RawB_V) <= c_rVoltageDiscrepancyLimit_V) THEN
    IF (ABS(rVoltage_PhaseA_RawA_V - rVoltage_PhaseA_RawC_V) <= c_rVoltageDiscrepancyLimit_V) THEN
        IF (rVoltage_PhaseA_RawA_V >= rVoltage_PhaseA_RawB_V AND rVoltage_PhaseA_RawA_V <= rVoltage_PhaseA_RawC_V) OR
           (rVoltage_PhaseA_RawA_V <= rVoltage_PhaseA_RawB_V AND rVoltage_PhaseA_RawA_V >= rVoltage_PhaseA_RawC_V) THEN
            rVotedVoltage_PhaseA_V := rVoltage_PhaseA_RawA_V;
        ELSIF (rVoltage_PhaseA_RawB_V >= rVoltage_PhaseA_RawA_V AND rVoltage_PhaseA_RawB_V <= rVoltage_PhaseA_RawC_V) OR
              (rVoltage_PhaseA_RawB_V <= rVoltage_PhaseA_RawA_V AND rVoltage_PhaseA_RawB_V >= rVoltage_PhaseA_RawC_V) THEN
            rVotedVoltage_PhaseA_V := rVoltage_PhaseA_RawB_V;
        ELSE
            rVotedVoltage_PhaseA_V := rVoltage_PhaseA_RawC_V;
        END_IF;
        iVoltageFaultCount_A_RawA := 0;  iVoltageFaultCount_A_RawB := 0;  iVoltageFaultCount_A_RawC := 0;
        bDegradedVoltage_PhaseA := FALSE;
    ELSE
        rVotedVoltage_PhaseA_V := 0.5 * (rVoltage_PhaseA_RawA_V + rVoltage_PhaseA_RawB_V);
        iVoltageFaultCount_A_RawC := iVoltageFaultCount_A_RawC + 1;
        bDegradedVoltage_PhaseA := TRUE;
    END_IF;
ELSIF (ABS(rVoltage_PhaseA_RawA_V - rVoltage_PhaseA_RawC_V) <= c_rVoltageDiscrepancyLimit_V) THEN
    rVotedVoltage_PhaseA_V := 0.5 * (rVoltage_PhaseA_RawA_V + rVoltage_PhaseA_RawC_V);
    iVoltageFaultCount_A_RawB := iVoltageFaultCount_A_RawB + 1;
    bDegradedVoltage_PhaseA := TRUE;
ELSIF (ABS(rVoltage_PhaseA_RawB_V - rVoltage_PhaseA_RawC_V) <= c_rVoltageDiscrepancyLimit_V) THEN
    rVotedVoltage_PhaseA_V := 0.5 * (rVoltage_PhaseA_RawB_V + rVoltage_PhaseA_RawC_V);
    iVoltageFaultCount_A_RawA := iVoltageFaultCount_A_RawA + 1;
    bDegradedVoltage_PhaseA := TRUE;
ELSE
    rVotedVoltage_PhaseA_V := rVoltage_PhaseA_RawA_V;
    bDegradedVoltage_PhaseA := TRUE;
END_IF;

(* --- 2.5 ARC VOLTAGE PHASE B 2oo3 VOTER --- *)
IF (ABS(rVoltage_PhaseB_RawA_V - rVoltage_PhaseB_RawB_V) <= c_rVoltageDiscrepancyLimit_V) THEN
    IF (ABS(rVoltage_PhaseB_RawA_V - rVoltage_PhaseB_RawC_V) <= c_rVoltageDiscrepancyLimit_V) THEN
        IF (rVoltage_PhaseB_RawA_V >= rVoltage_PhaseB_RawB_V AND rVoltage_PhaseB_RawA_V <= rVoltage_PhaseB_RawC_V) OR
           (rVoltage_PhaseB_RawA_V <= rVoltage_PhaseB_RawB_V AND rVoltage_PhaseB_RawA_V >= rVoltage_PhaseB_RawC_V) THEN
            rVotedVoltage_PhaseB_V := rVoltage_PhaseB_RawA_V;
        ELSIF (rVoltage_PhaseB_RawB_V >= rVoltage_PhaseB_RawA_V AND rVoltage_PhaseB_RawB_V <= rVoltage_PhaseB_RawC_V) OR
              (rVoltage_PhaseB_RawB_V <= rVoltage_PhaseB_RawA_V AND rVoltage_PhaseB_RawB_V >= rVoltage_PhaseB_RawC_V) THEN
            rVotedVoltage_PhaseB_V := rVoltage_PhaseB_RawB_V;
        ELSE
            rVotedVoltage_PhaseB_V := rVoltage_PhaseB_RawC_V;
        END_IF;
        iVoltageFaultCount_B_RawA := 0;  iVoltageFaultCount_B_RawB := 0;  iVoltageFaultCount_B_RawC := 0;
        bDegradedVoltage_PhaseB := FALSE;
    ELSE
        rVotedVoltage_PhaseB_V := 0.5 * (rVoltage_PhaseB_RawA_V + rVoltage_PhaseB_RawB_V);
        iVoltageFaultCount_B_RawC := iVoltageFaultCount_B_RawC + 1;
        bDegradedVoltage_PhaseB := TRUE;
    END_IF;
ELSIF (ABS(rVoltage_PhaseB_RawA_V - rVoltage_PhaseB_RawC_V) <= c_rVoltageDiscrepancyLimit_V) THEN
    rVotedVoltage_PhaseB_V := 0.5 * (rVoltage_PhaseB_RawA_V + rVoltage_PhaseB_RawC_V);
    iVoltageFaultCount_B_RawB := iVoltageFaultCount_B_RawB + 1;
    bDegradedVoltage_PhaseB := TRUE;
ELSIF (ABS(rVoltage_PhaseB_RawB_V - rVoltage_PhaseB_RawC_V) <= c_rVoltageDiscrepancyLimit_V) THEN
    rVotedVoltage_PhaseB_V := 0.5 * (rVoltage_PhaseB_RawB_V + rVoltage_PhaseB_RawC_V);
    iVoltageFaultCount_B_RawA := iVoltageFaultCount_B_RawA + 1;
    bDegradedVoltage_PhaseB := TRUE;
ELSE
    rVotedVoltage_PhaseB_V := rVoltage_PhaseB_RawB_V;
    bDegradedVoltage_PhaseB := TRUE;
END_IF;

(* --- 2.6 ARC VOLTAGE PHASE C 2oo3 VOTER --- *)
IF (ABS(rVoltage_PhaseC_RawA_V - rVoltage_PhaseC_RawB_V) <= c_rVoltageDiscrepancyLimit_V) THEN
    IF (ABS(rVoltage_PhaseC_RawA_V - rVoltage_PhaseC_RawC_V) <= c_rVoltageDiscrepancyLimit_V) THEN
        IF (rVoltage_PhaseC_RawA_V >= rVoltage_PhaseC_RawB_V AND rVoltage_PhaseC_RawA_V <= rVoltage_PhaseC_RawC_V) OR
           (rVoltage_PhaseC_RawA_V <= rVoltage_PhaseC_RawB_V AND rVoltage_PhaseC_RawA_V >= rVoltage_PhaseC_RawC_V) THEN
            rVotedVoltage_PhaseC_V := rVoltage_PhaseC_RawA_V;
        ELSIF (rVoltage_PhaseC_RawB_V >= rVoltage_PhaseC_RawA_V AND rVoltage_PhaseC_RawB_V <= rVoltage_PhaseC_RawC_V) OR
              (rVoltage_PhaseC_RawB_V <= rVoltage_PhaseC_RawA_V AND rVoltage_PhaseC_RawB_V >= rVoltage_PhaseC_RawC_V) THEN
            rVotedVoltage_PhaseC_V := rVoltage_PhaseC_RawB_V;
        ELSE
            rVotedVoltage_PhaseC_V := rVoltage_PhaseC_RawC_V;
        END_IF;
        iVoltageFaultCount_C_RawA := 0;  iVoltageFaultCount_C_RawB := 0;  iVoltageFaultCount_C_RawC := 0;
        bDegradedVoltage_PhaseC := FALSE;
    ELSE
        rVotedVoltage_PhaseC_V := 0.5 * (rVoltage_PhaseC_RawA_V + rVoltage_PhaseC_RawB_V);
        iVoltageFaultCount_C_RawC := iVoltageFaultCount_C_RawC + 1;
        bDegradedVoltage_PhaseC := TRUE;
    END_IF;
ELSIF (ABS(rVoltage_PhaseC_RawA_V - rVoltage_PhaseC_RawC_V) <= c_rVoltageDiscrepancyLimit_V) THEN
    rVotedVoltage_PhaseC_V := 0.5 * (rVoltage_PhaseC_RawA_V + rVoltage_PhaseC_RawC_V);
    iVoltageFaultCount_C_RawB := iVoltageFaultCount_C_RawB + 1;
    bDegradedVoltage_PhaseC := TRUE;
ELSIF (ABS(rVoltage_PhaseC_RawB_V - rVoltage_PhaseC_RawC_V) <= c_rVoltageDiscrepancyLimit_V) THEN
    rVotedVoltage_PhaseC_V := 0.5 * (rVoltage_PhaseC_RawB_V + rVoltage_PhaseC_RawC_V);
    iVoltageFaultCount_C_RawA := iVoltageFaultCount_C_RawA + 1;
    bDegradedVoltage_PhaseC := TRUE;
ELSE
    rVotedVoltage_PhaseC_V := rVoltage_PhaseC_RawC_V;
    bDegradedVoltage_PhaseC := TRUE;
END_IF;

(* --- 2.7 MAST CYLINDER DISPLACEMENT PHASE A 2oo3 VOTER --- *)
IF (ABS(rMastPos_PhaseA_RawA_mm - rMastPos_PhaseA_RawB_mm) <= c_rPositionDiscrepancyLimit_mm) THEN
    IF (ABS(rMastPos_PhaseA_RawA_mm - rMastPos_PhaseA_RawC_mm) <= c_rPositionDiscrepancyLimit_mm) THEN
        IF (rMastPos_PhaseA_RawA_mm >= rMastPos_PhaseA_RawB_mm AND rMastPos_PhaseA_RawA_mm <= rMastPos_PhaseA_RawC_mm) OR
           (rMastPos_PhaseA_RawA_mm <= rMastPos_PhaseA_RawB_mm AND rMastPos_PhaseA_RawA_mm >= rMastPos_PhaseA_RawC_mm) THEN
            rVotedMastPos_PhaseA_mm := rMastPos_PhaseA_RawA_mm;
        ELSIF (rMastPos_PhaseA_RawB_mm >= rMastPos_PhaseA_RawA_mm AND rMastPos_PhaseA_RawB_mm <= rMastPos_PhaseA_RawC_mm) OR
              (rMastPos_PhaseA_RawB_mm <= rMastPos_PhaseA_RawA_mm AND rMastPos_PhaseA_RawB_mm >= rMastPos_PhaseA_RawC_mm) THEN
            rVotedMastPos_PhaseA_mm := rMastPos_PhaseA_RawB_mm;
        ELSE
            rVotedMastPos_PhaseA_mm := rMastPos_PhaseA_RawC_mm;
        END_IF;
        iMastPosFaultCount_A_RawA := 0;  iMastPosFaultCount_A_RawB := 0;  iMastPosFaultCount_A_RawC := 0;
        bDegradedMastPos_PhaseA := FALSE;
    ELSE
        rVotedMastPos_PhaseA_mm := 0.5 * (rMastPos_PhaseA_RawA_mm + rMastPos_PhaseA_RawB_mm);
        iMastPosFaultCount_A_RawC := iMastPosFaultCount_A_RawC + 1;
        bDegradedMastPos_PhaseA := TRUE;
    END_IF;
ELSIF (ABS(rMastPos_PhaseA_RawA_mm - rMastPos_PhaseA_RawC_mm) <= c_rPositionDiscrepancyLimit_mm) THEN
    rVotedMastPos_PhaseA_mm := 0.5 * (rMastPos_PhaseA_RawA_mm + rMastPos_PhaseA_RawC_mm);
    iMastPosFaultCount_A_RawB := iMastPosFaultCount_A_RawB + 1;
    bDegradedMastPos_PhaseA := TRUE;
ELSIF (ABS(rMastPos_PhaseA_RawB_mm - rMastPos_PhaseA_RawC_mm) <= c_rPositionDiscrepancyLimit_mm) THEN
    rVotedMastPos_PhaseA_mm := 0.5 * (rMastPos_PhaseA_RawB_mm + rMastPos_PhaseA_RawC_mm);
    iMastPosFaultCount_A_RawA := iMastPosFaultCount_A_RawA + 1;
    bDegradedMastPos_PhaseA := TRUE;
ELSE
    rVotedMastPos_PhaseA_mm := rMastPos_PhaseA_RawA_mm;
    bDegradedMastPos_PhaseA := TRUE;
END_IF;

(* --- 2.8 MAST CYLINDER DISPLACEMENT PHASE B 2oo3 VOTER --- *)
IF (ABS(rMastPos_PhaseB_RawA_mm - rMastPos_PhaseB_RawB_mm) <= c_rPositionDiscrepancyLimit_mm) THEN
    IF (ABS(rMastPos_PhaseB_RawA_mm - rMastPos_PhaseB_RawC_mm) <= c_rPositionDiscrepancyLimit_mm) THEN
        IF (rMastPos_PhaseB_RawA_mm >= rMastPos_PhaseB_RawB_mm AND rMastPos_PhaseB_RawA_mm <= rMastPos_PhaseB_RawC_mm) OR
           (rMastPos_PhaseB_RawA_mm <= rMastPos_PhaseB_RawB_mm AND rMastPos_PhaseB_RawA_mm >= rMastPos_PhaseB_RawC_mm) THEN
            rVotedMastPos_PhaseB_mm := rMastPos_PhaseB_RawA_mm;
        ELSIF (rMastPos_PhaseB_RawB_mm >= rMastPos_PhaseB_RawA_mm AND rMastPos_PhaseB_RawB_mm <= rMastPos_PhaseB_RawC_mm) OR
              (rMastPos_PhaseB_RawB_mm <= rMastPos_PhaseB_RawA_mm AND rMastPos_PhaseB_RawB_mm >= rMastPos_PhaseB_RawC_mm) THEN
            rVotedMastPos_PhaseB_mm := rMastPos_PhaseB_RawB_mm;
        ELSE
            rVotedMastPos_PhaseB_mm := rMastPos_PhaseB_RawC_mm;
        END_IF;
        iMastPosFaultCount_B_RawA := 0;  iMastPosFaultCount_B_RawB := 0;  iMastPosFaultCount_B_RawC := 0;
        bDegradedMastPos_PhaseB := FALSE;
    ELSE
        rVotedMastPos_PhaseB_mm := 0.5 * (rMastPos_PhaseB_RawA_mm + rMastPos_PhaseB_RawB_mm);
        iMastPosFaultCount_B_RawC := iMastPosFaultCount_B_RawC + 1;
        bDegradedMastPos_PhaseB := TRUE;
    END_IF;
ELSIF (ABS(rMastPos_PhaseB_RawA_mm - rMastPos_PhaseB_RawC_mm) <= c_rPositionDiscrepancyLimit_mm) THEN
    rVotedMastPos_PhaseB_mm := 0.5 * (rMastPos_PhaseB_RawA_mm + rMastPos_PhaseB_RawC_mm);
    iMastPosFaultCount_B_RawB := iMastPosFaultCount_B_RawB + 1;
    bDegradedMastPos_PhaseB := TRUE;
ELSIF (ABS(rMastPos_PhaseB_RawB_mm - rMastPos_PhaseB_RawC_mm) <= c_rPositionDiscrepancyLimit_mm) THEN
    rVotedMastPos_PhaseB_mm := 0.5 * (rMastPos_PhaseB_RawB_mm + rMastPos_PhaseB_RawC_mm);
    iMastPosFaultCount_B_RawA := iMastPosFaultCount_B_RawA + 1;
    bDegradedMastPos_PhaseB := TRUE;
ELSE
    rVotedMastPos_PhaseB_mm := rMastPos_PhaseB_RawB_mm;
    bDegradedMastPos_PhaseB := TRUE;
END_IF;

(* --- 2.9 MAST CYLINDER DISPLACEMENT PHASE C 2oo3 VOTER --- *)
IF (ABS(rMastPos_PhaseC_RawA_mm - rMastPos_PhaseC_RawB_mm) <= c_rPositionDiscrepancyLimit_mm) THEN
    IF (ABS(rMastPos_PhaseC_RawA_mm - rMastPos_PhaseC_RawC_mm) <= c_rPositionDiscrepancyLimit_mm) THEN
        IF (rMastPos_PhaseC_RawA_mm >= rMastPos_PhaseC_RawB_mm AND rMastPos_PhaseC_RawA_mm <= rMastPos_PhaseC_RawC_mm) OR
           (rMastPos_PhaseC_RawA_mm <= rMastPos_PhaseC_RawB_mm AND rMastPos_PhaseC_RawA_mm >= rMastPos_PhaseC_RawC_mm) THEN
            rVotedMastPos_PhaseC_mm := rMastPos_PhaseC_RawA_mm;
        ELSIF (rMastPos_PhaseC_RawB_mm >= rMastPos_PhaseC_RawA_mm AND rMastPos_PhaseC_RawB_mm <= rMastPos_PhaseC_RawC_mm) OR
              (rMastPos_PhaseC_RawB_mm <= rMastPos_PhaseC_RawA_mm AND rMastPos_PhaseC_RawB_mm >= rMastPos_PhaseC_RawC_mm) THEN
            rVotedMastPos_PhaseC_mm := rMastPos_PhaseC_RawB_mm;
        ELSE
            rVotedMastPos_PhaseC_mm := rMastPos_PhaseC_RawC_mm;
        END_IF;
        iMastPosFaultCount_C_RawA := 0;  iMastPosFaultCount_C_RawB := 0;  iMastPosFaultCount_C_RawC := 0;
        bDegradedMastPos_PhaseC := FALSE;
    ELSE
        rVotedMastPos_PhaseC_mm := 0.5 * (rMastPos_PhaseC_RawA_mm + rMastPos_PhaseC_RawB_mm);
        iMastPosFaultCount_C_RawC := iMastPosFaultCount_C_RawC + 1;
        bDegradedMastPos_PhaseC := TRUE;
    END_IF;
ELSIF (ABS(rMastPos_PhaseC_RawA_mm - rMastPos_PhaseC_RawC_mm) <= c_rPositionDiscrepancyLimit_mm) THEN
    rVotedMastPos_PhaseC_mm := 0.5 * (rMastPos_PhaseC_RawA_mm + rMastPos_PhaseC_RawC_mm);
    iMastPosFaultCount_C_RawB := iMastPosFaultCount_C_RawB + 1;
    bDegradedMastPos_PhaseC := TRUE;
ELSIF (ABS(rMastPos_PhaseC_RawB_mm - rMastPos_PhaseC_RawC_mm) <= c_rPositionDiscrepancyLimit_mm) THEN
    rVotedMastPos_PhaseC_mm := 0.5 * (rMastPos_PhaseC_RawB_mm + rMastPos_PhaseC_RawC_mm);
    iMastPosFaultCount_C_RawA := iMastPosFaultCount_C_RawA + 1;
    bDegradedMastPos_PhaseC := TRUE;
ELSE
    rVotedMastPos_PhaseC_mm := rMastPos_PhaseC_RawC_mm;
    bDegradedMastPos_PhaseC := TRUE;
END_IF;

(* --- 2.10 ROOF COOLING WATER CIRCUIT 2oo3 VOTER --- *)
IF (ABS(rCoolingFlow_Roof_RawA_m3h - rCoolingFlow_Roof_RawB_m3h) <= c_rFlowDiscrepancyLimit_m3h) THEN
    IF (ABS(rCoolingFlow_Roof_RawA_m3h - rCoolingFlow_Roof_RawC_m3h) <= c_rFlowDiscrepancyLimit_m3h) THEN
        IF (rCoolingFlow_Roof_RawA_m3h >= rCoolingFlow_Roof_RawB_m3h AND rCoolingFlow_Roof_RawA_m3h <= rCoolingFlow_Roof_RawC_m3h) OR
           (rCoolingFlow_Roof_RawA_m3h <= rCoolingFlow_Roof_RawB_m3h AND rCoolingFlow_Roof_RawA_m3h >= rCoolingFlow_Roof_RawC_m3h) THEN
            rVotedCoolingFlow_Roof_m3h := rCoolingFlow_Roof_RawA_m3h;
        ELSIF (rCoolingFlow_Roof_RawB_m3h >= rCoolingFlow_Roof_RawA_m3h AND rCoolingFlow_Roof_RawB_m3h <= rCoolingFlow_Roof_RawC_m3h) OR
              (rCoolingFlow_Roof_RawB_m3h <= rCoolingFlow_Roof_RawA_m3h AND rCoolingFlow_Roof_RawB_m3h >= rCoolingFlow_Roof_RawC_m3h) THEN
            rVotedCoolingFlow_Roof_m3h := rCoolingFlow_Roof_RawB_m3h;
        ELSE
            rVotedCoolingFlow_Roof_m3h := rCoolingFlow_Roof_RawC_m3h;
        END_IF;
        iCoolingFaultCount_Roof_RawA := 0;  iCoolingFaultCount_Roof_RawB := 0;  iCoolingFaultCount_Roof_RawC := 0;
        bDegradedCooling_Roof := FALSE;
    ELSE
        rVotedCoolingFlow_Roof_m3h := 0.5 * (rCoolingFlow_Roof_RawA_m3h + rCoolingFlow_Roof_RawB_m3h);
        iCoolingFaultCount_Roof_RawC := iCoolingFaultCount_Roof_RawC + 1;
        bDegradedCooling_Roof := TRUE;
    END_IF;
ELSIF (ABS(rCoolingFlow_Roof_RawA_m3h - rCoolingFlow_Roof_RawC_m3h) <= c_rFlowDiscrepancyLimit_m3h) THEN
    rVotedCoolingFlow_Roof_m3h := 0.5 * (rCoolingFlow_Roof_RawA_m3h + rCoolingFlow_Roof_RawC_m3h);
    iCoolingFaultCount_Roof_RawB := iCoolingFaultCount_Roof_RawB + 1;
    bDegradedCooling_Roof := TRUE;
ELSIF (ABS(rCoolingFlow_Roof_RawB_m3h - rCoolingFlow_Roof_RawC_m3h) <= c_rFlowDiscrepancyLimit_m3h) THEN
    rVotedCoolingFlow_Roof_m3h := 0.5 * (rCoolingFlow_Roof_RawB_m3h + rCoolingFlow_Roof_RawC_m3h);
    iCoolingFaultCount_Roof_RawA := iCoolingFaultCount_Roof_RawA + 1;
    bDegradedCooling_Roof := TRUE;
ELSE
    rVotedCoolingFlow_Roof_m3h := rCoolingFlow_Roof_RawA_m3h;
    bDegradedCooling_Roof := TRUE;
END_IF;

(* --- 2.11 WALL PANEL COOLING WATER CIRCUIT 2oo3 VOTER --- *)
IF (ABS(rCoolingFlow_Panel_RawA_m3h - rCoolingFlow_Panel_RawB_m3h) <= c_rFlowDiscrepancyLimit_m3h) THEN
    IF (ABS(rCoolingFlow_Panel_RawA_m3h - rCoolingFlow_Panel_RawC_m3h) <= c_rFlowDiscrepancyLimit_m3h) THEN
        IF (rCoolingFlow_Panel_RawA_m3h >= rCoolingFlow_Panel_RawB_m3h AND rCoolingFlow_Panel_RawA_m3h <= rCoolingFlow_Panel_RawC_m3h) OR
           (rCoolingFlow_Panel_RawA_m3h <= rCoolingFlow_Panel_RawB_m3h AND rCoolingFlow_Panel_RawA_m3h >= rCoolingFlow_Panel_RawC_m3h) THEN
            rVotedCoolingFlow_Panel_m3h := rCoolingFlow_Panel_RawA_m3h;
        ELSIF (rCoolingFlow_Panel_RawB_m3h >= rCoolingFlow_Panel_RawA_m3h AND rCoolingFlow_Panel_RawB_m3h <= rCoolingFlow_Panel_RawC_m3h) OR
              (rCoolingFlow_Panel_RawB_m3h <= rCoolingFlow_Panel_RawA_m3h AND rCoolingFlow_Panel_RawB_m3h >= rCoolingFlow_Panel_RawC_m3h) THEN
            rVotedCoolingFlow_Panel_m3h := rCoolingFlow_Panel_RawB_m3h;
        ELSE
            rVotedCoolingFlow_Panel_m3h := rCoolingFlow_Panel_RawC_m3h;
        END_IF;
        iCoolingFaultCount_Panel_RawA := 0;  iCoolingFaultCount_Panel_RawB := 0;  iCoolingFaultCount_Panel_RawC := 0;
        bDegradedCooling_Panel := FALSE;
    ELSE
        rVotedCoolingFlow_Panel_m3h := 0.5 * (rCoolingFlow_Panel_RawA_m3h + rCoolingFlow_Panel_RawB_m3h);
        iCoolingFaultCount_Panel_RawC := iCoolingFaultCount_Panel_RawC + 1;
        bDegradedCooling_Panel := TRUE;
    END_IF;
ELSIF (ABS(rCoolingFlow_Panel_RawA_m3h - rCoolingFlow_Panel_RawC_m3h) <= c_rFlowDiscrepancyLimit_m3h) THEN
    rVotedCoolingFlow_Panel_m3h := 0.5 * (rCoolingFlow_Panel_RawA_m3h + rCoolingFlow_Panel_RawC_m3h);
    iCoolingFaultCount_Panel_RawB := iCoolingFaultCount_Panel_RawB + 1;
    bDegradedCooling_Panel := TRUE;
ELSIF (ABS(rCoolingFlow_Panel_RawB_m3h - rCoolingFlow_Panel_RawC_m3h) <= c_rFlowDiscrepancyLimit_m3h) THEN
    rVotedCoolingFlow_Panel_m3h := 0.5 * (rCoolingFlow_Panel_RawB_m3h + rCoolingFlow_Panel_RawC_m3h);
    iCoolingFaultCount_Panel_RawA := iCoolingFaultCount_Panel_RawA + 1;
    bDegradedCooling_Panel := TRUE;
ELSE
    rVotedCoolingFlow_Panel_m3h := rCoolingFlow_Panel_RawA_m3h;
    bDegradedCooling_Panel := TRUE;
END_IF;

(* Telemetry Serialization for 2oo3 Sensor Diagnostics *)
dwTMR_Diagnostic_1.0  := (iCurrentFaultCount_A_RawA > 15);
dwTMR_Diagnostic_1.1  := (iCurrentFaultCount_A_RawB > 15);
dwTMR_Diagnostic_1.2  := (iCurrentFaultCount_A_RawC > 15);
dwTMR_Diagnostic_1.3  := bDegradedCurrent_PhaseA;
dwTMR_Diagnostic_1.4  := (iCurrentFaultCount_B_RawA > 15);
dwTMR_Diagnostic_1.5  := (iCurrentFaultCount_B_RawB > 15);
dwTMR_Diagnostic_1.6  := (iCurrentFaultCount_B_RawC > 15);
dwTMR_Diagnostic_1.7  := bDegradedCurrent_PhaseB;
dwTMR_Diagnostic_1.8  := (iCurrentFaultCount_C_RawA > 15);
dwTMR_Diagnostic_1.9  := (iCurrentFaultCount_C_RawB > 15);
dwTMR_Diagnostic_1.10 := (iCurrentFaultCount_C_RawC > 15);
dwTMR_Diagnostic_1.11 := bDegradedCurrent_PhaseC;
dwTMR_Diagnostic_1.12 := (iVoltageFaultCount_A_RawA > 15);
dwTMR_Diagnostic_1.13 := (iVoltageFaultCount_A_RawB > 15);
dwTMR_Diagnostic_1.14 := (iVoltageFaultCount_A_RawC > 15);
dwTMR_Diagnostic_1.15 := bDegradedVoltage_PhaseA;

dwTMR_Diagnostic_2.0  := (iMastPosFaultCount_A_RawA > 15);
dwTMR_Diagnostic_2.1  := (iMastPosFaultCount_A_RawB > 15);
dwTMR_Diagnostic_2.2  := (iMastPosFaultCount_A_RawC > 15);
dwTMR_Diagnostic_2.3  := bDegradedMastPos_PhaseA;
dwTMR_Diagnostic_2.4  := (iCoolingFaultCount_Roof_RawA > 15);
dwTMR_Diagnostic_2.5  := (iCoolingFaultCount_Roof_RawB > 15);
dwTMR_Diagnostic_2.6  := (iCoolingFaultCount_Roof_RawC > 15);
dwTMR_Diagnostic_2.7  := bDegradedCooling_Roof;
dwTMR_Diagnostic_2.8  := (iCoolingFaultCount_Panel_RawA > 15);
dwTMR_Diagnostic_2.9  := (iCoolingFaultCount_Panel_RawB > 15);
dwTMR_Diagnostic_2.10 := (iCoolingFaultCount_Panel_RawC > 15);
dwTMR_Diagnostic_2.11 := bDegradedCooling_Panel;""")
    
    # 7. SECTION 3: DYNAMIC ELECTRICAL & POWER QUALITY
    parts.append("""(* ====================================================================================================================
   SECTION 3: DYNAMIC ELECTRICAL CALCULATIONS, ARC IMPEDANCE & POWER QUALITY HARMONIC FLICKER
   ==================================================================================================================== *)
(* --- 3.1 DYNAMIC ARC IMPEDANCE & RESISTANCE EVALUATION --- *)
IF rVotedCurrent_PhaseA_kA > 1.0 THEN
    rArcImpedance_PhaseA_mOhm  := (rVotedVoltage_PhaseA_V / rVotedCurrent_PhaseA_kA);
    rArcResistance_PhaseA_mOhm := rArcImpedance_PhaseA_mOhm * 0.725; (* Empirical active arc resistance *)
ELSE
    rArcImpedance_PhaseA_mOhm  := 999.9;
    rArcResistance_PhaseA_mOhm := 999.9;
END_IF;

IF rVotedCurrent_PhaseB_kA > 1.0 THEN
    rArcImpedance_PhaseB_mOhm  := (rVotedVoltage_PhaseB_V / rVotedCurrent_PhaseB_kA);
    rArcResistance_PhaseB_mOhm := rArcImpedance_PhaseB_mOhm * 0.725;
ELSE
    rArcImpedance_PhaseB_mOhm  := 999.9;
    rArcResistance_PhaseB_mOhm := 999.9;
END_IF;

IF rVotedCurrent_PhaseC_kA > 1.0 THEN
    rArcImpedance_PhaseC_mOhm  := (rVotedVoltage_PhaseC_V / rVotedCurrent_PhaseC_kA);
    rArcResistance_PhaseC_mOhm := rArcImpedance_PhaseC_mOhm * 0.725;
ELSE
    rArcImpedance_PhaseC_mOhm  := 999.9;
    rArcResistance_PhaseC_mOhm := 999.9;
END_IF;

(* Fundamental 3-Phase Active and Reactive Power Calculations *)
rActivePower_Total_MW := (rVotedVoltage_PhaseA_V * rVotedCurrent_PhaseA_kA * 0.725 +
                          rVotedVoltage_PhaseB_V * rVotedCurrent_PhaseB_kA * 0.725 +
                          rVotedVoltage_PhaseC_V * rVotedCurrent_PhaseC_kA * 0.725) / 1000.0;

rReactivePower_Total_MVAR := (rVotedVoltage_PhaseA_V * rVotedCurrent_PhaseA_kA * 0.688 +
                              rVotedVoltage_PhaseB_V * rVotedCurrent_PhaseB_kA * 0.688 +
                              rVotedVoltage_PhaseC_V * rVotedCurrent_PhaseC_kA * 0.688) / 1000.0;

IF (rActivePower_Total_MW > 0.5) THEN
    rFurnacePowerFactor := rActivePower_Total_MW / SQRT(rActivePower_Total_MW * rActivePower_Total_MW +
                                                        rReactivePower_Total_MVAR * rReactivePower_Total_MVAR + 0.001);
ELSE
    rFurnacePowerFactor := 1.0;
END_IF;

(* Cumulative Specific Energy Accounting *)
IF (rActivePower_Total_MW > 1.0) AND (rScrapChargeWeight_Ton > 10.0) THEN
    rCumulativeActiveEnergy_MWh := rCumulativeActiveEnergy_MWh + (rActivePower_Total_MW * c_rSamplingPeriod_sec / 3600.0);
    rSpecificEnergyDelivered_kWh_t := (rCumulativeActiveEnergy_MWh * 1000.0) / rScrapChargeWeight_Ton;
END_IF;

(* --- 3.2 DYNAMIC CASSIE-MAYR ARC CONDUCTANCE UPDATES --- *)
(* Phase A Dynamic Conductance Update *)
rArcLength_PhaseA_cm := (rVotedMastPos_PhaseA_mm - 1800.0) * 0.05 + 12.0;
IF rArcLength_PhaseA_cm < 4.0 THEN rArcLength_PhaseA_cm := 4.0; END_IF;

rArcConductance_PhaseA_S := rArcConductance_PhaseA_S + c_rSamplingPeriod_sec * (
    (1.0 / c_rCassieTimeConst_sec) * (
        (rVotedVoltage_PhaseA_V * rVotedCurrent_PhaseA_kA * 1000.0) /
        ((c_rArcFieldConstant_E0 + c_rArcLengthSensitivity_alpha * rArcLength_PhaseA_cm) *
         (c_rArcFieldConstant_E0 + c_rArcLengthSensitivity_alpha * rArcLength_PhaseA_cm) *
         rArcConductance_PhaseA_S + 1.0) - rArcConductance_PhaseA_S
    )
);
IF rArcConductance_PhaseA_S < 0.5 THEN rArcConductance_PhaseA_S := 0.5; END_IF;
IF rArcConductance_PhaseA_S > 180.0 THEN rArcConductance_PhaseA_S := 180.0; END_IF;

(* Phase B Dynamic Conductance Update *)
rArcLength_PhaseB_cm := (rVotedMastPos_PhaseB_mm - 1800.0) * 0.05 + 12.0;
IF rArcLength_PhaseB_cm < 4.0 THEN rArcLength_PhaseB_cm := 4.0; END_IF;

rArcConductance_PhaseB_S := rArcConductance_PhaseB_S + c_rSamplingPeriod_sec * (
    (1.0 / c_rCassieTimeConst_sec) * (
        (rVotedVoltage_PhaseB_V * rVotedCurrent_PhaseB_kA * 1000.0) /
        ((c_rArcFieldConstant_E0 + c_rArcLengthSensitivity_alpha * rArcLength_PhaseB_cm) *
         (c_rArcFieldConstant_E0 + c_rArcLengthSensitivity_alpha * rArcLength_PhaseB_cm) *
         rArcConductance_PhaseB_S + 1.0) - rArcConductance_PhaseB_S
    )
);
IF rArcConductance_PhaseB_S < 0.5 THEN rArcConductance_PhaseB_S := 0.5; END_IF;
IF rArcConductance_PhaseB_S > 180.0 THEN rArcConductance_PhaseB_S := 180.0; END_IF;

(* Phase C Dynamic Conductance Update *)
rArcLength_PhaseC_cm := (rVotedMastPos_PhaseC_mm - 1800.0) * 0.05 + 12.0;
IF rArcLength_PhaseC_cm < 4.0 THEN rArcLength_PhaseC_cm := 4.0; END_IF;

rArcConductance_PhaseC_S := rArcConductance_PhaseC_S + c_rSamplingPeriod_sec * (
    (1.0 / c_rCassieTimeConst_sec) * (
        (rVotedVoltage_PhaseC_V * rVotedCurrent_PhaseC_kA * 1000.0) /
        ((c_rArcFieldConstant_E0 + c_rArcLengthSensitivity_alpha * rArcLength_PhaseC_cm) *
         (c_rArcFieldConstant_E0 + c_rArcLengthSensitivity_alpha * rArcLength_PhaseC_cm) *
         rArcConductance_PhaseC_S + 1.0) - rArcConductance_PhaseC_S
    )
);
IF rArcConductance_PhaseC_S < 0.5 THEN rArcConductance_PhaseC_S := 0.5; END_IF;
IF rArcConductance_PhaseC_S > 180.0 THEN rArcConductance_PhaseC_S := 180.0; END_IF;

(* --- 3.3 POWER QUALITY, FLICKER ESTIMATION & SVC INTERACTION --- *)
IF bFlickerCompensatorEnable THEN
    rSVC_ReactiveDemand_MVAR := -1.0 * rReactivePower_Total_MVAR;
    IF rSVC_ReactiveDemand_MVAR > 0.0 THEN rSVC_ReactiveDemand_MVAR := 0.0; END_IF;
    IF rSVC_ReactiveDemand_MVAR < -120.0 THEN rSVC_ReactiveDemand_MVAR := -120.0; END_IF;
ELSE
    rSVC_ReactiveDemand_MVAR := 0.0;
END_IF;

(* IEC 61000-4-15 Eye-Brain Flicker Sensation Model State Integration (8.8 Hz Bandpass) *)
rFlickerFilterState_1 := rFlickerFilterState_1 + c_rSamplingPeriod_sec * (
    rFlickerFilterState_2 - 55.2 * rFlickerFilterState_1
);
rFlickerFilterState_2 := rFlickerFilterState_2 + c_rSamplingPeriod_sec * (
    -3060.0 * rFlickerFilterState_1 + 420.0 * (rVotedCurrent_PhaseA_kA - c_rRatedCurrent_kA)
);
rInstantaneousSensation_S := (rFlickerFilterState_1 * rFlickerFilterState_1) * 0.000125;
rShortTermFlickerAccumulator := rShortTermFlickerAccumulator + rInstantaneousSensation_S;
iFlickerSampleCounter := iFlickerSampleCounter + 1;

IF iFlickerSampleCounter >= 10000 THEN (* 10-second sliding appraisal window *)
    rFlickerPst_Estimate := SQRT(rShortTermFlickerAccumulator / 10000.0);
    rShortTermFlickerAccumulator := 0.0;
    iFlickerSampleCounter := 0;
END_IF;""")
    
    # 8. SECTION 4: SCRAP CAVE-IN & ARC BREAK
    parts.append("""(* ====================================================================================================================
   SECTION 4: DYNAMIC SCRAP CAVE-IN SHORT-CIRCUIT & ARC BREAK FAST ELECTROHYDRAULIC OVERRIDE
   ==================================================================================================================== *)
(* --- 4.1 SECONDARY CURRENT DERIVATIVE COMPUTATION --- *)
rDerivCurrent_PhaseA_kA_s := (rVotedCurrent_PhaseA_kA - rPrevCurrent_PhaseA_kA) / c_rSamplingPeriod_sec;
rDerivCurrent_PhaseB_kA_s := (rVotedCurrent_PhaseB_kA - rPrevCurrent_PhaseB_kA) / c_rSamplingPeriod_sec;
rDerivCurrent_PhaseC_kA_s := (rVotedCurrent_PhaseC_kA - rPrevCurrent_PhaseC_kA) / c_rSamplingPeriod_sec;
rPrevCurrent_PhaseA_kA    := rVotedCurrent_PhaseA_kA;
rPrevCurrent_PhaseB_kA    := rVotedCurrent_PhaseB_kA;
rPrevCurrent_PhaseC_kA    := rVotedCurrent_PhaseC_kA;

(* --- 4.2 PHASE A SCRAP CAVE-IN OVERRIDE --- *)
IF (rVotedCurrent_PhaseA_kA > c_rShortCircuitTripCurrent_kA) OR
   (rDerivCurrent_PhaseA_kA_s > 12000.0 AND rVotedVoltage_PhaseA_V < 80.0) THEN
    bScrapCaveIn_PhaseA := TRUE;
    tCaveInHoldTimer_A(IN := FALSE);
END_IF;

IF bScrapCaveIn_PhaseA THEN
    tCaveInHoldTimer_A(IN := TRUE, PT := T#120MS);
    IF tCaveInHoldTimer_A.Q AND (rVotedCurrent_PhaseA_kA < (1.4 * c_rRatedCurrent_kA)) THEN
        bScrapCaveIn_PhaseA := FALSE;
        tCaveInHoldTimer_A(IN := FALSE);
    END_IF;
END_IF;

(* --- 4.3 PHASE B SCRAP CAVE-IN OVERRIDE --- *)
IF (rVotedCurrent_PhaseB_kA > c_rShortCircuitTripCurrent_kA) OR
   (rDerivCurrent_PhaseB_kA_s > 12000.0 AND rVotedVoltage_PhaseB_V < 80.0) THEN
    bScrapCaveIn_PhaseB := TRUE;
    tCaveInHoldTimer_B(IN := FALSE);
END_IF;

IF bScrapCaveIn_PhaseB THEN
    tCaveInHoldTimer_B(IN := TRUE, PT := T#120MS);
    IF tCaveInHoldTimer_B.Q AND (rVotedCurrent_PhaseB_kA < (1.4 * c_rRatedCurrent_kA)) THEN
        bScrapCaveIn_PhaseB := FALSE;
        tCaveInHoldTimer_B(IN := FALSE);
    END_IF;
END_IF;

(* --- 4.4 PHASE C SCRAP CAVE-IN OVERRIDE --- *)
IF (rVotedCurrent_PhaseC_kA > c_rShortCircuitTripCurrent_kA) OR
   (rDerivCurrent_PhaseC_kA_s > 12000.0 AND rVotedVoltage_PhaseC_V < 80.0) THEN
    bScrapCaveIn_PhaseC := TRUE;
    tCaveInHoldTimer_C(IN := FALSE);
END_IF;

IF bScrapCaveIn_PhaseC THEN
    tCaveInHoldTimer_C(IN := TRUE, PT := T#120MS);
    IF tCaveInHoldTimer_C.Q AND (rVotedCurrent_PhaseC_kA < (1.4 * c_rRatedCurrent_kA)) THEN
        bScrapCaveIn_PhaseC := FALSE;
        tCaveInHoldTimer_C(IN := FALSE);
    END_IF;
END_IF;

(* --- 4.5 ARC EXTINGUISHMENT & FAST DOWNWARD STRIKE PLUNGE --- *)
IF (iState >= 2 AND iState <= 7) THEN
    (* Phase A Arc Break *)
    IF (rVotedCurrent_PhaseA_kA < c_rArcExtinguishThreshold_kA) AND (rVotedVoltage_PhaseA_V > 450.0) THEN
        bArcBreak_PhaseA := TRUE;
        tArcBreakHoldTimer_A(IN := FALSE);
    END_IF;
    IF bArcBreak_PhaseA THEN
        tArcBreakHoldTimer_A(IN := TRUE, PT := T#800MS);
        IF (rVotedCurrent_PhaseA_kA > c_rArcStrikeDetection_kA) OR tArcBreakHoldTimer_A.Q THEN
            bArcBreak_PhaseA := FALSE;
            tArcBreakHoldTimer_A(IN := FALSE);
        END_IF;
    END_IF;

    (* Phase B Arc Break *)
    IF (rVotedCurrent_PhaseB_kA < c_rArcExtinguishThreshold_kA) AND (rVotedVoltage_PhaseB_V > 450.0) THEN
        bArcBreak_PhaseB := TRUE;
        tArcBreakHoldTimer_B(IN := FALSE);
    END_IF;
    IF bArcBreak_PhaseB THEN
        tArcBreakHoldTimer_B(IN := TRUE, PT := T#800MS);
        IF (rVotedCurrent_PhaseB_kA > c_rArcStrikeDetection_kA) OR tArcBreakHoldTimer_B.Q THEN
            bArcBreak_PhaseB := FALSE;
            tArcBreakHoldTimer_B(IN := FALSE);
        END_IF;
    END_IF;

    (* Phase C Arc Break *)
    IF (rVotedCurrent_PhaseC_kA < c_rArcExtinguishThreshold_kA) AND (rVotedVoltage_PhaseC_V > 450.0) THEN
        bArcBreak_PhaseC := TRUE;
        tArcBreakHoldTimer_C(IN := FALSE);
    END_IF;
    IF bArcBreak_PhaseC THEN
        tArcBreakHoldTimer_C(IN := TRUE, PT := T#800MS);
        IF (rVotedCurrent_PhaseC_kA > c_rArcStrikeDetection_kA) OR tArcBreakHoldTimer_C.Q THEN
            bArcBreak_PhaseC := FALSE;
            tArcBreakHoldTimer_C(IN := FALSE);
        END_IF;
    END_IF;
ELSE
    bArcBreak_PhaseA := FALSE;
    bArcBreak_PhaseB := FALSE;
    bArcBreak_PhaseC := FALSE;
END_IF;

bArcIgnited_PhaseA := (rVotedCurrent_PhaseA_kA > c_rArcStrikeDetection_kA);
bArcIgnited_PhaseB := (rVotedCurrent_PhaseB_kA > c_rArcStrikeDetection_kA);
bArcIgnited_PhaseC := (rVotedCurrent_PhaseC_kA > c_rArcStrikeDetection_kA);""")
    
    # 9. SECTION 5: CO-JET & CONTINUOUS OFF-GAS CEM
    parts.append("""(* ====================================================================================================================
   SECTION 5: CO-JET CHEMICAL ENERGY, FOAMY SLAG DYNAMICS & PRIMARY OFF-GAS CEM SAFETY AUDIT
   ==================================================================================================================== *)
(* Off-Gas Post-Combustion Ratio (PCR) Calculation *)
IF (rOffGas_CO_vol_pct + rOffGas_CO2_vol_pct) > 0.5 THEN
    rPostCombustionRatio_pct := (rOffGas_CO2_vol_pct / (rOffGas_CO_vol_pct + rOffGas_CO2_vol_pct)) * 100.0;
ELSE
    rPostCombustionRatio_pct := 0.0;
END_IF;

(* Thermal Chemical Power Recovery in Exhaust Duct [MW] *)
rChemicalPowerRecovered_MW := (
    (rOffGas_VolFlow_Nm3h / 22.414) * (
        (rOffGas_CO2_vol_pct * 0.01) * rEnthalpyPostCombustion_kJ_mol +
        (rOffGas_H2_vol_pct  * 0.01) * rEnthalpyHydrogenComb_kJ_mol
    )
) / 3600.0;
IF rChemicalPowerRecovered_MW < 0.0 THEN rChemicalPowerRecovered_MW := 0.0; END_IF;

(* Foamy Slag Height & Acoustic Arc Radiation Shrouding *)
IF (rCarbonFlowCmd_kgh > 50.0) AND (iState >= 4) THEN
    rCalculatedFoamHeight_mm := rCalculatedFoamHeight_mm + c_rSamplingPeriod_sec * (
        0.185 * rCarbonFlowCmd_kgh - 0.045 * rCalculatedFoamHeight_mm
    );
ELSE
    rCalculatedFoamHeight_mm := rCalculatedFoamHeight_mm - c_rSamplingPeriod_sec * 5.0;
END_IF;
IF rCalculatedFoamHeight_mm < 50.0 THEN rCalculatedFoamHeight_mm := 50.0; END_IF;
IF rCalculatedFoamHeight_mm > 480.0 THEN rCalculatedFoamHeight_mm := 480.0; END_IF;

rRadiationShieldingFactor := 1.0 - EXP(-0.0075 * rCalculatedFoamHeight_mm);
rFoamSlagAcousticIndex_pct := rRadiationShieldingFactor * 100.0;

(* --- 5.1 SIL-3 WATER LEAK EXPLOSION HAZARD EVALUATION --- *)
rDerivOffGas_H2_pct_s  := (rOffGas_H2_vol_pct - rPrevOffGas_H2_vol_pct) / c_rSamplingPeriod_sec;
rPrevOffGas_H2_vol_pct := rOffGas_H2_vol_pct;

IF (rOffGas_H2_vol_pct >= c_rOffGasH2_TripHH_pct) OR
   (rOffGas_H2_vol_pct > c_rOffGasH2_WarnH_pct AND rDerivOffGas_H2_pct_s > 0.45) THEN
    bWaterLeakExplosionHazard       := TRUE;
    bTripLatched_WaterLeakExplosion := TRUE;
    bEmergencyMasterArcTrip         := TRUE;
END_IF;""")
    
    # 10. SECTION 6: 16x16 STATE SPACE & MPC
    mpc_code = []
    mpc_code.append("""(* ====================================================================================================================
   SECTION 6: 16x16 DISCRETE-TIME STATE-SPACE SYSTEM PROPAGATION & RECEDING-HORIZON MPC SOLVER
   ==================================================================================================================== *)
IF NOT bMPC_MatricesInitialized THEN
    (* ---------------- 16x16 State Transition Matrix matA Initialization ---------------- *)""")
    for i in range(1, 17):
        row_str = "    "
        for j in range(1, 17):
            val = 0.0
            if i == j:
                if i in [1, 2, 3]: val = 0.9420     # Conductances g_A, g_B, g_C
                elif i in [4, 5, 6]: val = 0.9150   # Currents i_A, i_B, i_C
                elif i in [7, 9, 11]: val = 0.9980  # Mast positions y_A, y_B, y_C
                elif i in [8, 10, 12]: val = 0.8850 # Mast velocities v_A, v_B, v_C
                elif i == 13: val = 0.9850          # Foamy slag height
                elif i == 14: val = 0.9995          # Steel bath temp
                elif i == 15: val = 0.9650          # Cooling panel delta temp
                elif i == 16: val = 0.9200          # Off-gas hydrogen
            elif i == 7 and j == 8: val = 0.0010    # y_A coupled to v_A
            elif i == 9 and j == 10: val = 0.0010   # y_B coupled to v_B
            elif i == 11 and j == 12: val = 0.0010  # y_C coupled to v_C
            elif i == 1 and j == 7: val = -0.0125   # Conductance g_A drops as mast raises
            elif i == 2 and j == 9: val = -0.0125   # Conductance g_B drops as mast raises
            elif i == 3 and j == 11: val = -0.0125  # Conductance g_C drops as mast raises
            elif i == 14 and j in [4, 5, 6]: val = 0.00045 # Bath heating from currents
            elif i == 15 and j == 13: val = -0.0240 # Foam shields panels from radiation
            elif i == 16 and j == 15: val = 0.0018  # Panel steam leak increases H2
            row_str += f"matA[{i:2d},{j:2d}] := {val:7.4f}; "
            if j % 4 == 0:
                mpc_code.append(row_str)
                row_str = "    "
        if len(row_str.strip()) > 0:
            mpc_code.append(row_str)
            
    mpc_code.append("""
    (* ---------------- 16x8 Input Coupling Matrix matB Initialization ---------------- *)""")
    for i in range(1, 17):
        row_str = "    "
        for j in range(1, 8+1):
            val = 0.0
            if i == 8 and j == 1: val = 2.4500      # Mast A acceleration from servo A
            elif i == 10 and j == 2: val = 2.4500   # Mast B acceleration from servo B
            elif i == 12 and j == 3: val = 2.4500   # Mast C acceleration from servo C
            elif i in [4, 5, 6] and j == 4: val = 3.8500 # Current boost from OLTC tap raise
            elif i == 14 and j == 5: val = 0.0185   # Bath superheating from supersonic O2
            elif i == 13 and j == 6: val = 0.0420   # Foamy slag generation from carbon
            elif i == 15 and j == 7: val = 0.0150   # Post-combustion panel heat
            elif i in [4, 5, 6] and j == 8: val = -0.0050 # SVC stabilizing current swings
            row_str += f"matB[{i:2d},{j:2d}] := {val:7.4f}; "
            if j % 4 == 0:
                mpc_code.append(row_str)
                row_str = "    "
        if len(row_str.strip()) > 0:
            mpc_code.append(row_str)

    mpc_code.append("""
    (* ---------------- 8x16 Measurement Matrix matC Initialization ---------------- *)""")
    for i in range(1, 8+1):
        row_str = "    "
        for j in range(1, 17):
            val = 0.0
            if i == 1 and j == 1: val = 1.0     # Impedance error A
            elif i == 2 and j == 2: val = 1.0   # Impedance error B
            elif i == 3 and j == 3: val = 1.0   # Impedance error C
            elif i == 4 and j in [4, 5, 6]: val = 0.3333 # Mean current
            elif i == 5 and j == 13: val = 1.0  # Slag foam
            elif i == 6 and j == 14: val = 1.0  # Bath temp
            elif i == 7 and j == 15: val = 1.0  # Panel temp
            elif i == 8 and j == 16: val = 1.0  # Offgas H2
            row_str += f"matC[{i:2d},{j:2d}] := {val:7.4f}; "
            if j % 4 == 0:
                mpc_code.append(row_str)
                row_str = "    "
        if len(row_str.strip()) > 0:
            mpc_code.append(row_str)

    mpc_code.append("""
    (* ---------------- 8x8 Direct Feedthrough Matrix matD Initialization ---------------- *)""")
    for i in range(1, 8+1):
        row_str = "    "
        for j in range(1, 8+1):
            val = 0.0
            row_str += f"matD[{i:2d},{j:2d}] := {val:7.4f}; "
            if j % 4 == 0:
                mpc_code.append(row_str)
                row_str = "    "
        if len(row_str.strip()) > 0:
            mpc_code.append(row_str)

    mpc_code.append("""
    (* ---------------- MPC Quadratic Cost Penalties & Actuator Limits ---------------- *)
    vecCostWeight_Q[1]  := 85.0;   vecCostWeight_Q[2]  := 85.0;   vecCostWeight_Q[3]  := 85.0;
    vecCostWeight_Q[4]  := 12.0;   vecCostWeight_Q[5]  := 12.0;   vecCostWeight_Q[6]  := 12.0;
    vecCostWeight_Q[7]  := 0.15;   vecCostWeight_Q[8]  := 0.05;   vecCostWeight_Q[9]  := 0.15;
    vecCostWeight_Q[10] := 0.05;   vecCostWeight_Q[11] := 0.15;   vecCostWeight_Q[12] := 0.05;
    vecCostWeight_Q[13] := 45.0;   vecCostWeight_Q[14] := 120.0;  vecCostWeight_Q[15] := 250.0;
    vecCostWeight_Q[16] := 1500.0;

    vecCostWeight_R[1]  := 1.25;   vecCostWeight_R[2]  := 1.25;   vecCostWeight_R[3]  := 1.25;
    vecCostWeight_R[4]  := 15.0;   vecCostWeight_R[5]  := 0.08;   vecCostWeight_R[6]  := 0.12;
    vecCostWeight_R[7]  := 0.06;   vecCostWeight_R[8]  := 0.02;

    vecCostWeight_S[1]  := 4.50;   vecCostWeight_S[2]  := 4.50;   vecCostWeight_S[3]  := 4.50;
    vecCostWeight_S[4]  := 85.0;   vecCostWeight_S[5]  := 0.25;   vecCostWeight_S[6]  := 0.35;
    vecCostWeight_S[7]  := 0.18;   vecCostWeight_S[8]  := 0.05;

    vecControlMin_u[1]  := -100.0; vecControlMax_u[1]  := 100.0;  vecDeltaMax_du[1]   := 15.0;
    vecControlMin_u[2]  := -100.0; vecControlMax_u[2]  := 100.0;  vecDeltaMax_du[2]   := 15.0;
    vecControlMin_u[3]  := -100.0; vecControlMax_u[3]  := 100.0;  vecDeltaMax_du[3]   := 15.0;
    vecControlMin_u[4]  := -1.0;   vecControlMax_u[4]  := 1.0;    vecDeltaMax_du[4]   := 1.0;
    vecControlMin_u[5]  := 0.0;    vecControlMax_u[5]  := 4000.0; vecDeltaMax_du[5]   := 250.0;
    vecControlMin_u[6]  := 0.0;    vecControlMax_u[6]  := 3600.0; vecDeltaMax_du[6]   := 180.0;
    vecControlMin_u[7]  := 0.0;    vecControlMax_u[7]  := 1500.0; vecDeltaMax_du[7]   := 120.0;
    vecControlMin_u[8]  := -120.0; vecControlMax_u[8]  := 0.0;    vecDeltaMax_du[8]   := 25.0;

    bMPC_MatricesInitialized := TRUE;
END_IF;

(* Construct Current Error State Vector x[k] *)
vecState_x[1]  := rArcImpedance_PhaseA_mOhm - rTargetImpedance_PhaseA_mOhm;
vecState_x[2]  := rArcImpedance_PhaseB_mOhm - rTargetImpedance_PhaseB_mOhm;
vecState_x[3]  := rArcImpedance_PhaseC_mOhm - rTargetImpedance_PhaseC_mOhm;
vecState_x[4]  := rVotedCurrent_PhaseA_kA - c_rRatedCurrent_kA;
vecState_x[5]  := rVotedCurrent_PhaseB_kA - c_rRatedCurrent_kA;
vecState_x[6]  := rVotedCurrent_PhaseC_kA - c_rRatedCurrent_kA;
vecState_x[7]  := rVotedMastPos_PhaseA_mm - 2200.0;
vecState_x[8]  := (rVotedMastPos_PhaseA_mm - 2200.0) * 0.1;
vecState_x[9]  := rVotedMastPos_PhaseB_mm - 2200.0;
vecState_x[10] := (rVotedMastPos_PhaseB_mm - 2200.0) * 0.1;
vecState_x[11] := rVotedMastPos_PhaseC_mm - 2200.0;
vecState_x[12] := (rVotedMastPos_PhaseC_mm - 2200.0) * 0.1;
vecState_x[13] := 250.0 - rCalculatedFoamHeight_mm;
vecState_x[14] := rTargetTappingTemp_degC - rLiquidSteelBathTemp_degC;
vecState_x[15] := (rCoolingOutletTemp_Panel_degC - rCoolingInletTemp_degC) - 18.0;
vecState_x[16] := rOffGas_H2_vol_pct - 0.5;

(* Inner Receding Horizon Projected Gradient Descent Loop *)
IF (iState >= 2 AND iState <= 7) AND bMasterEnable THEN
    FOR kIdx := 1 TO iMPC_MaxIterations DO
        (* Predict Next State Vector: x[k+1] = A * x[k] + B * u[k] *)
        FOR iIdx := 1 TO 16 DO
            rTempDotProduct := 0.0;
            FOR jIdx := 1 TO 16 DO
                rTempDotProduct := rTempDotProduct + matA[iIdx, jIdx] * vecState_x[jIdx];
            END_FOR;
            FOR jIdx := 1 TO 8 DO
                rTempDotProduct := rTempDotProduct + matB[iIdx, jIdx] * vecControl_u[jIdx];
            END_FOR;
            vecStateNext_x[iIdx] := rTempDotProduct;
        END_FOR;

        (* Compute Cost Gradient: g = B^T * Q * x[k+1] + R * u + S * (u - u_prev) *)
        FOR iIdx := 1 TO 8 DO
            rTempDotProduct := 0.0;
            FOR jIdx := 1 TO 16 DO
                rTempDotProduct := rTempDotProduct + matB[jIdx, iIdx] * vecCostWeight_Q[jIdx] * vecStateNext_x[jIdx];
            END_FOR;
            rTempDotProduct := rTempDotProduct + vecCostWeight_R[iIdx] * vecControl_u[iIdx];
            rTempDotProduct := rTempDotProduct + vecCostWeight_S[iIdx] * (vecControl_u[iIdx] - vecControlPrev_u[iIdx]);
            vecGradient_g[iIdx] := rTempDotProduct;

            (* Projected Gradient Update with Actuator Slew Rate Limiter *)
            vecControl_u[iIdx] := vecControl_u[iIdx] - rMPC_StepAlpha * vecGradient_g[iIdx];

            vecDeltaControl_du[iIdx] := vecControl_u[iIdx] - vecControlPrev_u[iIdx];
            IF vecDeltaControl_du[iIdx] > vecDeltaMax_du[iIdx] THEN
                vecControl_u[iIdx] := vecControlPrev_u[iIdx] + vecDeltaMax_du[iIdx];
            ELSIF vecDeltaControl_du[iIdx] < -vecDeltaMax_du[iIdx] THEN
                vecControl_u[iIdx] := vecControlPrev_u[iIdx] - vecDeltaMax_du[iIdx];
            END_IF;

            (* Actuator Box Saturation *)
            IF vecControl_u[iIdx] < vecControlMin_u[iIdx] THEN
                vecControl_u[iIdx] := vecControlMin_u[iIdx];
            ELSIF vecControl_u[iIdx] > vecControlMax_u[iIdx] THEN
                vecControl_u[iIdx] := vecControlMax_u[iIdx];
            END_IF;
        END_FOR;
    END_FOR;

    FOR iIdx := 1 TO 8 DO
        vecControlPrev_u[iIdx] := vecControl_u[iIdx];
    END_FOR;
ELSE
    FOR iIdx := 1 TO 8 DO
        vecControl_u[iIdx] := 0.0;
        vecControlPrev_u[iIdx] := 0.0;
    END_FOR;
END_IF;""")
    parts.append("\n".join(mpc_code))
    
    # 11. SECTION 7: 12-STAGE OPERATIONAL FSM
    parts.append("""(* ====================================================================================================================
   SECTION 7: 12-STAGE HEAVY INDUSTRIAL OPERATIONAL FINITE STATE MACHINE (FSM)
   ==================================================================================================================== *)
CASE iState OF
    0: (* ---------------- STATE 0: SCRAP BUCKET CHARGE HANDSHAKE & PRE-FLIGHT AUDIT ---------------- *)
        bSystemHealthy                  := FALSE;
        rServoCmd_MastA_pct             := 0.0;
        rServoCmd_MastB_pct             := 0.0;
        rServoCmd_MastC_pct             := 0.0;
        iTransformerTap_Command         := 1;
        rOxygenFlowCmd_Nm3h             := 0.0;
        rCarbonFlowCmd_kgh              := 0.0;
        rPostCombustionO2_Nm3h          := 0.0;
        bTapRaisePulse                  := FALSE;
        bTapLowerPulse                  := FALSE;

        IF bMasterEnable AND bSafetyCircuitHealthy AND (rScrapChargeWeight_Ton > 30.0) THEN
            iState := 1;
        END_IF;

    1: (* ---------------- STATE 1: ROOF SWING, ELECTRODE GANTRY ALIGNMENT & FURNACE CLOSURE ---------------- *)
        rServoCmd_MastA_pct := 0.0;
        rServoCmd_MastB_pct := 0.0;
        rServoCmd_MastC_pct := 0.0;

        tRoofSwingTimer(IN := TRUE, PT := T#4S);
        IF bRoofClosedAndLocked AND bElectrodeMastGantryLocked AND tRoofSwingTimer.Q THEN
            tRoofSwingTimer(IN := FALSE);
            iTargetTapMemory := 4;      (* Ignition Tap Step 4 *)
            iState := 2;
        END_IF;

    2: (* ---------------- STATE 2: 160 MVA TRANSFORMER ENERGIZATION & INITIAL ARC IGNITION ---------------- *)
        bSystemHealthy := TRUE;
        iTransformerTap_Command := iTargetTapMemory;

        (* Plunge electrodes down slowly until arc strikes scrap *)
        IF NOT bArcIgnited_PhaseA THEN
            rServoCmd_MastA_pct := -35.0;
        ELSE
            rServoCmd_MastA_pct := vecControl_u[1];
        END_IF;

        IF NOT bArcIgnited_PhaseB THEN
            rServoCmd_MastB_pct := -35.0;
        ELSE
            rServoCmd_MastB_pct := vecControl_u[2];
        END_IF;

        IF NOT bArcIgnited_PhaseC THEN
            rServoCmd_MastC_pct := -35.0;
        ELSE
            rServoCmd_MastC_pct := vecControl_u[3];
        END_IF;

        IF bArcIgnited_PhaseA AND bArcIgnited_PhaseB AND bArcIgnited_PhaseC THEN
            tFSM_StateTimer(IN := TRUE, PT := T#5S);
            IF tFSM_StateTimer.Q THEN
                tFSM_StateTimer(IN := FALSE);
                iState := 3;            (* Transition to Scrap Boring *)
            END_IF;
        ELSE
            tFSM_StateTimer(IN := FALSE);
        END_IF;

    3: (* ---------------- STATE 3: SCRAP BORING PHASE AT REDUCED TAP & SHORT ARC ---------------- *)
        (* Maintain low impedance short arc to bore through dense scrap without sidewall flare *)
        iTransformerTap_Command := 7;

        rServoCmd_MastA_pct := vecControl_u[1];
        rServoCmd_MastB_pct := vecControl_u[2];
        rServoCmd_MastC_pct := vecControl_u[3];

        IF bChemicalInjectionEnable THEN
            rOxygenFlowCmd_Nm3h    := 1200.0;
            rPostCombustionO2_Nm3h := 450.0;
        END_IF;

        tBoringPhaseTimer(IN := TRUE, PT := T#350S);
        IF (rVotedMastPos_PhaseA_mm < 1200.0) OR tBoringPhaseTimer.Q THEN
            tBoringPhaseTimer(IN := FALSE);
            iState := 4;                (* Transition to Main Meltdown *)
        END_IF;

    4: (* ---------------- STATE 4: MAIN MELTING PHASE AT MAXIMUM POWER (TAP 15-18) ---------------- *)
        IF bAutoTapChangerEnable THEN
            iTransformerTap_Command := 17; (* High Power Tap 17 (~115 MW) *)
        END_IF;

        rServoCmd_MastA_pct := vecControl_u[1];
        rServoCmd_MastB_pct := vecControl_u[2];
        rServoCmd_MastC_pct := vecControl_u[3];

        IF bChemicalInjectionEnable THEN
            rOxygenFlowCmd_Nm3h    := 3200.0;
            rPostCombustionO2_Nm3h := 850.0;
        END_IF;

        IF (rSpecificEnergyDelivered_kWh_t > 220.0) THEN
            iState := 5;                (* Transition to Foamy Slag Dosing *)
        END_IF;

    5: (* ---------------- STATE 5: FOAMY SLAG CARBON DOSING INITIATION & ACOUSTIC SHROUDING ---------------- *)
        iTransformerTap_Command := 18;  (* Maximum Voltage Tap for long foaming arc *)

        rServoCmd_MastA_pct := vecControl_u[1];
        rServoCmd_MastB_pct := vecControl_u[2];
        rServoCmd_MastC_pct := vecControl_u[3];

        IF bChemicalInjectionEnable THEN
            rCarbonFlowCmd_kgh     := 2400.0; (* Deep slag foaming *)
            rOxygenFlowCmd_Nm3h    := 3600.0;
            rPostCombustionO2_Nm3h := 1100.0;
        END_IF;

        IF (rFoamSlagAcousticIndex_pct > 75.0) AND (rSpecificEnergyDelivered_kWh_t > 290.0) THEN
            iState := 6;                (* Transition to Decarburization Cut-In *)
        END_IF;

    6: (* ---------------- STATE 6: SUPERSONIC OXYGEN DECARBURIZATION CUT-IN ---------------- *)
        iTransformerTap_Command := 16;

        rServoCmd_MastA_pct := vecControl_u[1];
        rServoCmd_MastB_pct := vecControl_u[2];
        rServoCmd_MastC_pct := vecControl_u[3];

        IF bChemicalInjectionEnable THEN
            rOxygenFlowCmd_Nm3h    := c_rMaxOxygenFlow_Nm3h;
            rCarbonFlowCmd_kgh     := 1800.0;
            rPostCombustionO2_Nm3h := 950.0;
        END_IF;

        IF (rSpecificEnergyDelivered_kWh_t >= (rTargetSpecificEnergy_kWh_t - 25.0)) THEN
            iState := 7;                (* Transition to Refining & Superheating *)
        END_IF;

    7: (* ---------------- STATE 7: REFINING, CHEMICAL SUPERHEATING & TARGET TEMPERATURE ---------------- *)
        iTransformerTap_Command := 12;  (* Reduced holding power for metallurgical refining *)

        rServoCmd_MastA_pct := vecControl_u[1];
        rServoCmd_MastB_pct := vecControl_u[2];
        rServoCmd_MastC_pct := vecControl_u[3];

        IF bChemicalInjectionEnable THEN
            rOxygenFlowCmd_Nm3h    := 1400.0;
            rCarbonFlowCmd_kgh     := 800.0;
            rPostCombustionO2_Nm3h := 400.0;
        END_IF;

        IF (rLiquidSteelBathTemp_degC >= rTargetTappingTemp_degC) AND
           (rSpecificEnergyDelivered_kWh_t >= rTargetSpecificEnergy_kWh_t) THEN
            iState := 8;                (* Transition to Safety Audit *)
        END_IF;

    8: (* ---------------- STATE 8: OFF-GAS WATER LEAK SAFETY AUDIT & THERMAL BALANCING ---------------- *)
        rServoCmd_MastA_pct    := 0.0;
        rServoCmd_MastB_pct    := 0.0;
        rServoCmd_MastC_pct    := 0.0;
        rOxygenFlowCmd_Nm3h    := 0.0;
        rCarbonFlowCmd_kgh     := 0.0;
        rPostCombustionO2_Nm3h := 0.0;

        tFSM_StateTimer(IN := TRUE, PT := T#2S);
        IF tFSM_StateTimer.Q THEN
            tFSM_StateTimer(IN := FALSE);
            IF NOT bTripLatched_WaterLeakExplosion THEN
                iState := 9;            (* Proceed to Power Off & Retract *)
            ELSE
                iState := 11;           (* Emergency Dump *)
            END_IF;
        END_IF;

    9: (* ---------------- STATE 9: TRANSFORMER DE-ENERGIZATION & HIGH-SPEED MAST RETRACT ---------------- *)
        iTransformerTap_Command := 1;
        bTapRaisePulse          := FALSE;
        bTapLowerPulse          := FALSE;

        (* High-speed upward mast retraction to park position *)
        rServoCmd_MastA_pct     := 85.0;
        rServoCmd_MastB_pct     := 85.0;
        rServoCmd_MastC_pct     := 85.0;

        IF (rVotedMastPos_PhaseA_mm >= 4200.0) AND
           (rVotedMastPos_PhaseB_mm >= 4200.0) AND
           (rVotedMastPos_PhaseC_mm >= 4200.0) THEN
            rServoCmd_MastA_pct := 0.0;
            rServoCmd_MastB_pct := 0.0;
            rServoCmd_MastC_pct := 0.0;
            iState := 10;               (* Transition to Tapping & Deslagging *)
        END_IF;

    10: (* ---------------- STATE 10: SLAG DOOR DESLAGGING & ECCENTRIC BOTTOM TAPPING (EBT) ---------------- *)
        rServoCmd_MastA_pct    := 0.0;
        rServoCmd_MastB_pct    := 0.0;
        rServoCmd_MastC_pct    := 0.0;
        rOxygenFlowCmd_Nm3h    := 0.0;
        rCarbonFlowCmd_kgh     := 0.0;
        rPostCombustionO2_Nm3h := 0.0;

        tFSM_StateTimer(IN := TRUE, PT := T#120S);
        IF tFSM_StateTimer.Q THEN
            tFSM_StateTimer(IN := FALSE);
            rCumulativeActiveEnergy_MWh := 0.0;
            iState := 0;                (* Heat Complete, Return to Standby *)
        END_IF;

    11: (* ---------------- STATE 11: EMERGENCY FAST ARC TRIP & SIL-3 NITROGEN BLAST DUMP ---------------- *)
        bEmergencyMasterArcTrip := TRUE;
        iTransformerTap_Command := 1;
        rOxygenFlowCmd_Nm3h     := 0.0;
        rCarbonFlowCmd_kgh      := 0.0;
        rPostCombustionO2_Nm3h  := 0.0;

        (* Emergency high-speed retract *)
        rServoCmd_MastA_pct     := c_rMaxMastVelocity_mms;
        rServoCmd_MastB_pct     := c_rMaxMastVelocity_mms;
        rServoCmd_MastC_pct     := c_rMaxMastVelocity_mms;

        IF bAlarmAcknowledgeReset AND bSafetyCircuitHealthy AND (NOT bTripLatched_WaterLeakExplosion) THEN
            bEmergencyMasterArcTrip := FALSE;
            iState := 0;
        END_IF;

ELSE
    iState := 0;
END_CASE;

iCurrentFSMState := iState;

(* --- 7.1 FAST OVERRIDE INJECTION INTO SERVO OUTPUTS --- *)
IF (iState >= 2 AND iState <= 7) THEN
    (* Phase A Overrides *)
    IF bScrapCaveIn_PhaseA THEN
        rServoCmd_MastA_pct := rCaveInFastRetractCmd_pct;
    ELSIF bArcBreak_PhaseA THEN
        rServoCmd_MastA_pct := rArcBreakFastPlungeCmd_pct;
    END_IF;

    (* Phase B Overrides *)
    IF bScrapCaveIn_PhaseB THEN
        rServoCmd_MastB_pct := rCaveInFastRetractCmd_pct;
    ELSIF bArcBreak_PhaseB THEN
        rServoCmd_MastB_pct := rArcBreakFastPlungeCmd_pct;
    END_IF;

    (* Phase C Overrides *)
    IF bScrapCaveIn_PhaseC THEN
        rServoCmd_MastC_pct := rCaveInFastRetractCmd_pct;
    ELSIF bArcBreak_PhaseC THEN
        rServoCmd_MastC_pct := rArcBreakFastPlungeCmd_pct;
    END_IF;
END_IF;

(* --- 7.2 MOTORIZED ON-LOAD TAP CHANGER (OLTC) PULSE GENERATOR --- *)
IF bAutoTapChangerEnable AND (iState >= 2 AND iState <= 7) THEN
    tTapChangeDwellTimer(IN := TRUE, PT := T#4S);
    IF tTapChangeDwellTimer.Q THEN
        IF (iTransformerTap_Command > iTransformerTap_Current) AND (NOT bTapPulseActive) THEN
            bTapRaisePulse := TRUE;
            bTapLowerPulse := FALSE;
            bTapPulseActive := TRUE;
            tTapPulseTimer(IN := FALSE);
        ELSIF (iTransformerTap_Command < iTransformerTap_Current) AND (NOT bTapPulseActive) THEN
            bTapRaisePulse := FALSE;
            bTapLowerPulse := TRUE;
            bTapPulseActive := TRUE;
            tTapPulseTimer(IN := FALSE);
        END_IF;
    END_IF;
ELSE
    tTapChangeDwellTimer(IN := FALSE);
END_IF;

IF bTapPulseActive THEN
    tTapPulseTimer(IN := TRUE, PT := T#450MS);
    IF tTapPulseTimer.Q THEN
        bTapRaisePulse := FALSE;
        bTapLowerPulse := FALSE;
        bTapPulseActive := FALSE;
        tTapPulseTimer(IN := FALSE);
        tTapChangeDwellTimer(IN := FALSE);
    END_IF;
END_IF;""")
    
    # 12. SECTION 8: ISA-18.2 ALARMS & BITFIELD PACKING
    parts.append("""(* ====================================================================================================================
   SECTION 8: ISA-18.2 MULTI-TIERED ALARM MATRIX, DEADBAND HYSTERESIS & TELEMETRY SERIALIZATION
   ==================================================================================================================== *)
(* --- 8.1 CRITICAL SHUTDOWN ALARMS (dwAlarmWord_1) --- *)
IF (rVotedCurrent_PhaseA_kA >= c_rCurrentTripHH_kA) OR
   (rVotedCurrent_PhaseB_kA >= c_rCurrentTripHH_kA) OR
   (rVotedCurrent_PhaseC_kA >= c_rCurrentTripHH_kA) THEN
    bTripLatched_Overcurrent := TRUE;
END_IF;

IF (rCoolingOutletTemp_Panel_degC >= c_rPanelTempTripHH_degC) THEN
    bTripLatched_CoolingLoss := TRUE;
END_IF;

IF (rVotedCoolingFlow_Roof_m3h <= c_rRoofCoolingLowTripLL_m3h) OR
   (rVotedCoolingFlow_Panel_m3h <= c_rPanelCoolingLowTripLL_m3h) THEN
    bTripLatched_CoolingLoss := TRUE;
END_IF;

IF (rHydraulicSupplyPress_bar <= c_rHydraulicLowPressTripLL_bar) THEN
    bTripLatched_HydraulicFailure := TRUE;
END_IF;

IF (rTransformerWindingTemp_degC >= c_rTransformerWindingTripHH_degC) THEN
    bTripLatched_TransformerOvertemp := TRUE;
END_IF;

IF bAlarmAcknowledgeReset THEN
    bTripLatched_Overcurrent        := FALSE;
    bTripLatched_CoolingLoss        := FALSE;
    bTripLatched_HydraulicFailure   := FALSE;
    bTripLatched_TransformerOvertemp:= FALSE;
    bTripLatched_WaterLeakExplosion := FALSE;
END_IF;

dwAlarmWord_1.0  := bTripLatched_Overcurrent;
dwAlarmWord_1.1  := bTripLatched_WaterLeakExplosion;
dwAlarmWord_1.2  := bTripLatched_CoolingLoss;
dwAlarmWord_1.3  := bTripLatched_HydraulicFailure;
dwAlarmWord_1.4  := bTripLatched_TransformerOvertemp;
dwAlarmWord_1.5  := bScrapCaveIn_PhaseA OR bScrapCaveIn_PhaseB OR bScrapCaveIn_PhaseC;
dwAlarmWord_1.6  := bArcBreak_PhaseA OR bArcBreak_PhaseB OR bArcBreak_PhaseC;
dwAlarmWord_1.7  := (rOffGas_SuctionPressure_mbar > 2.0); (* Primary duct positive pressure puff hazard *)
dwAlarmWord_1.8  := (rVotedMastPos_PhaseA_mm >= (c_rMaxMastStroke_mm - 50.0));
dwAlarmWord_1.9  := (rVotedMastPos_PhaseB_mm >= (c_rMaxMastStroke_mm - 50.0));
dwAlarmWord_1.10 := (rVotedMastPos_PhaseC_mm >= (c_rMaxMastStroke_mm - 50.0));
dwAlarmWord_1.11 := (rVotedMastPos_PhaseA_mm <= (c_rMinMastStroke_mm + 50.0));
dwAlarmWord_1.12 := (rVotedMastPos_PhaseB_mm <= (c_rMinMastStroke_mm + 50.0));
dwAlarmWord_1.13 := (rVotedMastPos_PhaseC_mm <= (c_rMinMastStroke_mm + 50.0));

(* --- 8.2 PROCESS WARNING ALARMS (dwAlarmWord_2) --- *)
dwAlarmWord_2.0  := (rCoolingOutletTemp_Panel_degC > c_rPanelTempWarnH_degC);
dwAlarmWord_2.1  := (rCoolingOutletTemp_Roof_degC > 65.0);
dwAlarmWord_2.2  := (rOffGas_H2_vol_pct > c_rOffGasH2_WarnH_pct);
dwAlarmWord_2.3  := (rOffGas_CO_vol_pct > 25.0);
dwAlarmWord_2.4  := (rTransformerOilTemp_degC > 85.0);
dwAlarmWord_2.5  := (rCalculatedFoamHeight_mm < 90.0) AND (iState >= 5);
dwAlarmWord_2.6  := (rHydraulicReturnPress_bar > 18.0);
dwAlarmWord_2.7  := bDegradedCurrent_PhaseA OR bDegradedCurrent_PhaseB OR bDegradedCurrent_PhaseC;
dwAlarmWord_2.8  := bDegradedVoltage_PhaseA OR bDegradedVoltage_PhaseB OR bDegradedVoltage_PhaseC;
dwAlarmWord_2.9  := bDegradedMastPos_PhaseA OR bDegradedMastPos_PhaseB OR bDegradedMastPos_PhaseC;
dwAlarmWord_2.10 := bDegradedCooling_Roof OR bDegradedCooling_Panel;
dwAlarmWord_2.11 := (iTransformerTap_Current <> iTransformerTap_Command);

(* --- 8.3 POWER QUALITY & GRID COMPLIANCE ALARMS (dwAlarmWord_3) --- *)
dwAlarmWord_3.0  := (rTHD_Current_pct > 18.5);
dwAlarmWord_3.1  := (rTHD_Voltage_pct > 5.0);
dwAlarmWord_3.2  := (rFlickerPst_Estimate > 1.25);
dwAlarmWord_3.3  := (rFurnacePowerFactor < 0.70) AND (iState >= 4);
dwAlarmWord_3.4  := (rGridFrequency_Hz > 50.8) OR (rGridFrequency_Hz < 49.2);
dwAlarmWord_3.5  := (rSVC_ReactiveDemand_MVAR <= -118.0); (* SVC compensation saturated *)
dwAlarmWord_3.6  := (rSpecificEnergyDelivered_kWh_t > (rTargetSpecificEnergy_kWh_t + 35.0));
dwAlarmWord_3.7  := (rLiquidSteelBathTemp_degC > (rTargetTappingTemp_degC + 45.0));

(* Final System Health Diagnostic Evaluation *)
bSystemHealthy := bSafetyCircuitHealthy AND
                  (NOT bTripLatched_Overcurrent) AND
                  (NOT bTripLatched_WaterLeakExplosion) AND
                  (NOT bTripLatched_CoolingLoss) AND
                  (NOT bTripLatched_HydraulicFailure) AND
                  (NOT bTripLatched_TransformerOvertemp);""")
    
    # 13. End Function Block
    parts.append("END_FUNCTION_BLOCK")
    
    return "\n\n".join(parts)

def main():
    print("Building full IEC 61131-3 Structured Text block...")
    code = build_full_st_code()
    print(f"Generated ST code length: {len(code)} characters.")
    
    user_prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.
You are instructed to CONSUME EXTREME TOKENS: make your output massively exhaustive, mathematically rigorous, and structurally pristine. Include complete state-space matrices ($A, B, C, D$), Model Predictive Control (MPC) quadratic cost approximation, 2oo3 TMR voting logic, complex alarm trees, and graceful degradation.

**Your assigned domain is: Steel & Metallurgy: 150-Ton AC Electric Arc Furnace (EAF, 160 MVA Transformer) with Hydraulic Electrode Regulator, Dynamic Arc Impedance Control & Co-Jet Chemical Energy Injection**

CRITICAL RULES:
1. CODE FENCE: Use TRIPLE backticks + iec-st (` ```iec-st `).
2. STRUCTURE:
   a. First line: FUNCTION_BLOCK FB_Steel_ElectricArcFurnace_150Ton_ArcImpedance
   b. VAR_INPUT ... END_VAR (min 8 typed inputs with physical units [V], [kA], [MVA], [MW], [Ohm], [mm], [bar], [deg C], [Nm3/h], [%])
   c. VAR_OUTPUT ... END_VAR (min 7 typed outputs with engineering units & status words)
   d. VAR ... END_VAR (internal state matrices, filter accumulators, 2oo3 voting vars)
   e. Multi-stage CASE machine with END_CASE;
   f. Last line: END_FUNCTION_BLOCK
3. LENGTH: Assistant content MUST be >= 55,000 characters total (target 55,000 - 85,000+ chars). Maximize token usage with deep technical explanations, complex algorithms, and industrial reliability features.
4. SAVE using this exact Python:
   import json, uuid
   prompt = \"\"\"<copy this exact user prompt here>\"\"\"
   code = \"\"\"```iec-st
FUNCTION_BLOCK FB_Steel_ElectricArcFurnace_150Ton_ArcImpedance
//...
END_FUNCTION_BLOCK
```\"\"\"
   record = {\"messages\": [{\"role\": \"user\", \"content\": prompt}, {\"role\": \"assistant\", \"content\": code}]}
   with open(\"data/swarm_raw/agent_2b4019ca.json\", \"w\", encoding=\"utf-8\") as f:
       json.dump(record, f, ensure_ascii=False)
5. REPLY with: EVOLUTION COMPLETE: Steel & Metallurgy: 150-Ton AC Electric Arc Furnace (EAF, 160 MVA Transformer) with Hydraulic Electrode Regulator, Dynamic Arc Impedance Control & Co-Jet Chemical Energy Injection"""

    assistant_content = f"```iec-st\n{code}\n```"
    
    record = {
        "messages": [
            {"role": "user", "content": user_prompt},
            {"role": "assistant", "content": assistant_content}
        ]
    }
    
    target_path = "data/swarm_raw/agent_2b4019ca.json"
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    with open(target_path, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)
    
    print(f"Saved dataset record to: {target_path}")
    print(f"Assistant content character count: {len(assistant_content)}")

if __name__ == "__main__":
    main()
