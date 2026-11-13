# scripts/build_cement_kiln.py
# Generator for FB_Cement_RotaryKiln_Precalciner_ClinkerCooler
# V7 Max-Persona: 75+ years Principal Automation Fellow & Cyber-Physical Systems Chair

import sys
import os
import json
import uuid

def generate_header():
    return """FUNCTION_BLOCK FB_Cement_RotaryKiln_Precalciner_ClinkerCooler
(*
========================================================================================================================
  LUMINA AI CYBER-PHYSICAL SYSTEMS & ADVANCED INDUSTRIAL AUTOMATION ARCHITECTURE GROUP
  HEAVY BUILDING MATERIALS, CEMENT & MINERAL PROCESSING REFERENCE IMPLEMENTATION — SYNTHETIC DATASET ENGINE V7
  
  SYSTEM DESIGNATION : 10,000 tpd PRECALCINER ROTARY CEMENT KILN & 5-STAGE CYCLONE SUSPENSION PREHEATER TOWER
  CALCINER SUBSYSTEM : RISER-DUCT IN-LINE CALCINER (ILC) WITH DUAL TERTIARY AIR DUCT (TAD) BALANCE & MEAL INJECTION
  KILN FIRING SYSTEM : MULTI-CHANNEL LOW-NOx MAIN BURNER (PULVERIZED COAL + ALTERNATIVE FUEL RDF/SRF CO-FIRING)
  SHELL MONITORING   : 40-POINT INFRARED LINE SCANNER HOT-SPOT DETECTION, COATING LOSS & TYRE CREEP SLIP OBSERVER
  MAIN DRIVE SYSTEM  : DUAL 1,200 kW INVERTER-DUTY MOTORS WITH MASTER-FOLLOWER TORQUE SHARING ON GIRTH GEAR
  COOLING SUBSYSTEM  : 6-COMPARTMENT CROSS-FLOW RECIPROCATING HYDRAULIC STEP GRATE CLINKER COOLER & FREE-LIME SOFT SENSOR
  SAFETY INTEGRITY   : IEC 61508 / IEC 61511 SIL-2 / SIL-3 KILN OVER-PRESSURE & HOT-SPOT EMERGENCY FAST FUEL CUTOFF
  APPLICABLE NORMS   : DIN EN 197-1 (CEMENT COMPOSITION & CONFORMITY CRITERIA), NFPA 85 (BOILER & COMBUSTION HAZARDS),
                       ISO 50001 (ENERGY MANAGEMENT IN CLINKER PRODUCTION), ISA-18.2 / IEC 62682 (ALARM MANAGEMENT),
                       VDI 2048 (THERMAL ENERGY BALANCE & MEASUREMENT UNCERTAINTIES), IEEE 841 (SEVERE DUTY MOTORS).
  AUTHOR             : 75+ YEARS VETERAN PRINCIPAL AUTOMATION FELLOW & CYBER-PHYSICAL SYSTEMS CHAIR
========================================================================================================================

  THEORETICAL & FIRST-PRINCIPLES CYBER-PHYSICAL THERMODYNAMICS:
  ----------------------------------------------------------------------------------------------------------------------
  1. 5-STAGE CYCLONE SUSPENSION PREHEATER & IN-LINE PRECALCINER (ILC) DECARBONATION KINETICS:
     - In modern 10,000 metric ton per day (tpd) dry-process cement clinker production lines, ground raw meal
       (composed predominantly of calcite CaCO3, quartz SiO2, clay minerals Al2O3.2SiO2.2H2O, and iron ore Fe2O3)
       enters the top stage (Cyclone C1) at 50 to 70 deg C and countercurrently cascades down through 5 suspension
       cyclone stages against upward-flowing hot exhaust gases (330 deg C at top ID fan to 1100 deg C at kiln inlet).
     - The chemical decarbonation (calcination) of limestone represents the single largest endothermic energy sink
       in clinker fabrication:
           CaCO3(s) + Delta_H_cal --> CaO(s) + CO2(g)
           Delta_H_cal = +1782 kJ / kg CaCO3 (+426 kcal / kg CaCO3)
     - In the riser-duct precalciner, raw meal preheated to 780-820 deg C in Cyclone C4 is dispersed directly into
       the turbulent combustion zone fed by tertiary air from the clinker cooler (850-950 deg C) and high-temperature
       kiln riser gases. Fuel injection (pulverized coal and Refuse-Derived Fuel RDF) supplies 55% to 65% of the total
       plant thermal energy input.
     - The solid decarbonation rate follows first-order shrinking core Arrhenius kinetics:
           d(alpha_calc) / dt = k_0 * exp(-E_act / (R_gas * T_gas)) * (1.0 - alpha_calc)^n_ord * (1.0 - (P_CO2 / P_CO2_eq))
       where:
           alpha_calc   = Fractional degree of apparent raw meal calcination (0.0 to 1.0)
           E_act        = Effective activation energy of calcination (170 to 195 kJ/mol)
           R_gas        = Universal gas constant = 8.31446 J/(mol*K)
           P_CO2_eq     = Equilibrium CO2 partial pressure (Knudsen relation: ln(P_CO2_eq) = 17.74 - 18700 / T_K [bar])
           P_CO2        = Local partial pressure of CO2 in calciner riser duct [bar]
     - Target apparent calcination degree entering the rotary kiln feed inlet is governed tightly between 92.0% and 95.0%.
       Under-calcination (<90%) causes thermal shock, ring formation, and excessive burning zone thermal load.
       Over-calcination (>96%) causes meal stickiness, cyclone cyclone cyclone chokes, and calciner refractory overheating.

  2. ROTARY KILN MAIN BURNER MULTI-CHANNEL FLAME MOMENTUM & BURNING ZONE OPTICAL PYROMETRY:
     - The 5.5 m diameter x 85 m long rotary kiln receives 93% calcined meal at 850-900 deg C and completes solid-state
       reactions (Belite C2S formation at 1100-1250 deg C), liquid phase flux melt formation (C4AF + C3A at 1338 deg C),
       and clinkering sintering alite crystallization (C3S = 3CaO.SiO2 at 1400-1480 deg C):
           2 CaO + SiO2 --> 2CaO.SiO2 (C2S / Belite)   [Exothermic: -710 kJ/kg]
           2CaO.SiO2 + CaO --> 3CaO.SiO2 (C3S / Alite) [Endothermic: +450 kJ/kg in liquid matrix]
     - The multi-channel low-NOx main burner injects pulverized coal and secondary alternative fuel (RDF/SRF) via
       independent concentric annuli:
       * Central Core Channel: Oil/gas pilot igniter and optical flame sensor sight glass.
       * Coal Channel: Dense-phase pneumatic pulverized coal transport air (v_transport = 28 to 34 m/s).
       * Alternative Fuel Channel: Coarse RDF fluff pneumatic delivery channel.
       * Axial Air Channel: High-pressure jet nozzles producing longitudinal axial momentum (v_axial = 140 to 180 m/s).
       * Tangential Swirl Air Channel: Adjustable angled swirl blades imparting radial vorticity (v_swirl = 100 to 140 m/s).
     - Net flame momentum G_m [Newtons] and specific momentum-to-thermal power ratio G_m / Q_thermal [N/MW]:
           G_m = sum_i ( m_dot_i * v_i )
           G_m_ratio = G_m / ( m_dot_coal * LHV_coal + m_dot_rdf * LHV_rdf )
       Nominal operational range: G_m = 1400 to 1850 N; G_m_ratio = 1.35 to 1.75 N/MW.
     - Burning zone temperature is monitored via 2oo3 Triple Modular Redundancy (TMR) dual-wavelength ratio pyrometers
       operating at 0.95 um and 1.05 um wavelengths, eliminating measurement error from kiln dust clouds and fume absorption.
       Target sintering bed temperature: 1420 to 1460 deg C.

  3. KILN SHELL 40-POINT INFRARED LINE SCANNER, TYRE SLIP OBSERVER & DUAL-DRIVE TORQUE SHARING:
     - The cylindrical steel shell is subjected to extreme thermal and mechanical stresses. A high-speed infrared (IR)
       line scanner continuously maps surface temperatures along 40 equidistant axial slices (Slices 1 to 40) across
       every kiln revolution (t_rev = 15 to 30 s).
     - 1D inverse radial thermal conduction through refractory brick and coating layer:
           T_shell_i = T_ambient + ( T_internal_i - T_ambient ) / ( 1.0 + ( k_refr / ( h_ext * r_shell ) ) * ln(r_shell / r_inner) )
       Detection thresholds:
       * Normal Shell Surface Temp: 220 to 320 deg C (indicating healthy 200 mm clinker coating + 200 mm brick).
       * Coating Loss / Thinning: 340 to 380 deg C (initiates shell cooling fan bank modulation).
       * Critical Shell Red Hot-Spot (HH): > 420 deg C (triggers emergency fast coal cutoff to avoid shell plastic collapse).
     - Floating Kiln Tyre Creep Slip Angle Observer:
       The kiln is supported by 3 or 4 tyre rings resting on twin support roller stations. Because the steel shell expands
       thermally more than the tyre ring, a mechanical clearance (expansion gap) exists at ambient conditions.
       During rotation, the tyre creeps relative to the shell:
           Delta_s = pi * ( D_tyre_inner - D_shell_seat ) [mm per kiln revolution]
       Creep slip is detected via proximity sensors recording the time delta between tyre reference pulse and shell pulse:
           Optimal Slip: 8.0 to 15.0 mm/rev.
           Excessive Slip (> 25 mm/rev): Loose tyre, excessive shim wear, risk of shell ovalization and brick spalling.
           Constricting Tyre (< 2.0 mm/rev): Zero clearance, risk of tyre seizure, shell constriction, and necking.
     - Dual-Motor Master-Follower Torque Sharing:
       Two 1200 kW inverter-duty slip-ring/induction motors drive the girth gear via dual pinions. Master motor governs
       kiln rotational speed (0.5 to 4.5 rpm); follower motor governs torque matching via a closed-loop PI trim loop
       to enforce torque imbalance |Tau_1 - Tau_2| / (Tau_1 + Tau_2) < 2.0%.

  4. CROSS-FLOW RECIPROCATING STEP GRATE CLINKER COOLER & FREE-LIME (CaO_free) SOFT SENSOR:
     - 10,000 tpd of white-hot clinker drops from the kiln discharge hood at 1350-1400 deg C onto a 6-compartment
       hydraulic reciprocating step grate cooler.
     - Six under-grate aeration compartments inject pressurized cross-flow air through perforated grate plates:
       * Compartment 1 (Static Horseshoe Incline): Critical clinker quenching zone (recuperates 1050-1150 deg C secondary air
         directly into the rotary kiln for main burner combustion).
       * Compartment 2 & 3: High-efficiency recuperation zone (recuperates 850-950 deg C tertiary air to the precalciner).
       * Compartment 4, 5, 6: Clinker cooling zone (discharging cooled clinker onto pan conveyors at < 100 deg C + ambient).
     - Grate stroke frequency (strokes/min) is modulated to maintain constant clinker bed depth (600 to 750 mm)
       and constant Compartment 1 under-grate aeration static pressure (45 to 60 mbar).
     - Real-Time Clinker Free-Lime (CaO_free) Soft Sensor:
       Unreacted free calcium oxide (free lime, CaO_free) is the paramount quality metric of Portland cement clinker.
       Target range: 0.8% to 1.5% CaO_free.
       A multivariate hybrid neural/kinetic estimator calculates free lime dynamically:
           CaO_free = f( T_burning_zone, Tau_kiln_drive, NOx_preheater, Feed_rate, Coal_rate, LSF )
       where high burning zone temperature and high drive torque (indicating dense clinker nodulization and liquid melt)
       exponentially decrease free lime per sintering reaction kinetics.

  5. 8-STATE CYBER-PHYSICAL DISCRETE STATE-SPACE FORMULATION (Ts = 50 ms):
     - The coupled thermodynamic, aerodynamic, and chemical system is formulated in discrete state-space:
           x[k+1] = A * x[k] + B * u[k] + E * d[k]
           y[k]   = C * x[k] + D * u[k]
       State Vector x (8x1):
         x[1]: Burning Zone Sintering Bed Optical Temperature                    [deg C]
         x[2]: Precalciner Riser Outlet Gas Temperature                          [deg C]
         x[3]: Kiln Inlet Static Draft Pressure                                  [mbar]
         x[4]: Kiln Main Girth Gear Dual-Drive Total Operating Torque            [kNm]
         x[5]: Real-Time Clinker Free-Lime (CaO_free) Soft-Sensor Concentration  [%]
         x[6]: Clinker Cooler Secondary Combustion Air Recovery Temperature      [deg C]
         x[7]: Cyclone Preheater Tower Top Stage (C1) Residual Oxygen            [%]
         x[8]: Kiln Shell Critical Hot-Spot Surface Peak Temperature             [deg C]
       Manipulated Control Input Vector u (8x1):
         u[1]: Main Burner Pulverized Coal Dosing Feed Rate                      [t/h]
         u[2]: Precalciner Fuel (Coal + RDF) Dosing Feed Rate                    [t/h]
         u[3]: Kiln Main Drive Inverter Master Speed Setpoint                    [rpm]
         u[4]: Raw Meal Infeed Flow Rate to Preheater Top Stage                  [t/h]
         u[5]: Preheater Induced Draft (ID) Exhaust Fan VFD Speed Demand         [%]
         u[6]: Tertiary Air Duct (TAD) Control Damper Angular Position           [%]
         u[7]: Clinker Cooler Reciprocating Grate Hydraulic Drive Speed          [strokes/min]
         u[8]: Cooler Compartment 1 Aeration Air Blower Damper Demand            [%]
       External Disturbance Vector d (4x1):
         d[1]: Raw Meal Chemical Burnability Deviation (Lime Saturation Factor)  [% LSF]
         d[2]: Alternative Fuel (RDF) Net Calorific Value Heating Fluctuation    [MJ/kg]
         d[3]: Atmospheric Ambient Temperature & Barometric Pressure Shock       [deg C / mbar]
         d[4]: Kiln Coating Ring Dam Obstruction / Clinker Snowman Buildup       [%]
*)
"""

def generate_var_input():
    return """VAR_INPUT
    (* ============================================================================================== *)
    (* MASTER SYSTEM ENABLES, PERMISSIVES & SAFETY SIGNALS                                           *)
    (* ============================================================================================== *)
    bSystemEnable                       : BOOL;     (* Master Automation System Hardware Permissive *)
    bKilnProductionRunCmd               : BOOL;     (* Production Run Command from Central Plant SCADA *)
    bEmergencyStop                      : BOOL;     (* Hardwired SIL-3 Safety Circuit Status (1=Healthy, 0=Tripped) *)
    bAlarmAcknowledge                   : BOOL;     (* Operator Alarm Acknowledge Pushbutton Trigger *)
    bAlarmReset                         : BOOL;     (* Master Alarm Reset Pushbutton Trigger *)

    (* ============================================================================================== *)
    (* RAW MEAL INFEED CHEMICAL MODULI & PROPERTIES WITH BRACKETED PHYSICAL UNITS                    *)
    (* ============================================================================================== *)
    rRawMealFeedRate_tph                : REAL;     (* Raw Meal Infeed Flow Rate to Stage 1 Preheater [t/h] *)
    rRawMealLossOnIgnition_pct          : REAL;     (* Raw Meal Loss on Ignition (LOI) Chemical Factor [%] *)
    rRawMealLimeSaturationFactor_LSF    : REAL;     (* Raw Meal Lime Saturation Factor [LSF] *)
    rRawMealSilicaModulus_SM            : REAL;     (* Raw Meal Silica Modulus Ratio [SM] *)
    rRawMealAluminaModulus_AM           : REAL;     (* Raw Meal Alumina Modulus Ratio [AM] *)
    rRawMealMoisture_pct                : REAL;     (* Raw Meal Surface Moisture Content [%] *)

    (* ============================================================================================== *)
    (* MAIN BURNER & ALTERNATIVE FUEL FEEDING PARAMETERS                                             *)
    (* ============================================================================================== *)
    rMainBurnerCoalFeedRate_tph         : REAL;     (* Main Burner Pulverized Coal Gravimetric Feeder Feedback [t/h] *)
    rMainBurnerRDF_FeedRate_tph         : REAL;     (* Main Burner Refuse-Derived Alternative Fuel Feeder Feedback [t/h] *)
    rMainBurnerPrimaryAirPressure_mbar  : REAL;     (* Main Burner Primary Air Supply Manifold Pressure [mbar] *)
    rMainBurnerPrimaryAirFlow_Nm3h      : REAL;     (* Main Burner Primary Air Total Mass Flow Rate [Nm3/h] *)
    rMainBurnerAxialAirFlow_Nm3h        : REAL;     (* Main Burner Concentric Axial Jet Nozzle Air Flow Rate [Nm3/h] *)
    rMainBurnerSwirlAirFlow_Nm3h        : REAL;     (* Main Burner Tangential Swirl Jet Nozzle Air Flow Rate [Nm3/h] *)
    rCoalLowerHeatingValue_MJkg         : REAL;     (* Pulverized Solid Coal Net Lower Heating Value [MJ/kg] *)
    rRDF_LowerHeatingValue_MJkg         : REAL;     (* Alternative Fuel (RDF) Net Lower Heating Value [MJ/kg] *)

    (* ============================================================================================== *)
    (* PRECALCINER FUEL & TERTIARY AIR PARAMETERS                                                    *)
    (* ============================================================================================== *)
    rCalcinerCoalFeedRate_tph           : REAL;     (* Precalciner Coal Gravimetric Feeder Feedback [t/h] *)
    rCalcinerRDF_FeedRate_tph           : REAL;     (* Precalciner Refuse-Derived Solid Alternative Fuel Feeder Feedback [t/h] *)
    rTertiaryAirDuctDraft_mbar          : REAL;     (* Tertiary Air Duct Static Pressure [mbar] *)
    rTertiaryAirTemp_degC               : REAL;     (* Tertiary Air Recovery Duct Gas Temperature [deg C] *)

    (* ============================================================================================== *)
    (* 2oo3 TRIPLE MODULAR REDUNDANT (TMR) INSTRUMENT TRIPLET 1: KILN INLET DRAFT PRESSURE            *)
    (* ============================================================================================== *)
    rKilnInletDraft_PT_A_mbar           : REAL;     (* Kiln Smoke Chamber Inlet Draft Pressure Sensor Channel A [mbar] *)
    rKilnInletDraft_PT_B_mbar           : REAL;     (* Kiln Smoke Chamber Inlet Draft Pressure Sensor Channel B [mbar] *)
    rKilnInletDraft_PT_C_mbar           : REAL;     (* Kiln Smoke Chamber Inlet Draft Pressure Sensor Channel C [mbar] *)

    (* ============================================================================================== *)
    (* 2oo3 TRIPLE MODULAR REDUNDANT (TMR) INSTRUMENT TRIPLET 2: BURNING ZONE OPTICAL PYROMETER       *)
    (* ============================================================================================== *)
    rBurningZoneTemp_PY_A_degC          : REAL;     (* Burning Zone Dual-Wavelength Ratio Pyrometer Channel A [deg C] *)
    rBurningZoneTemp_PY_B_degC          : REAL;     (* Burning Zone Dual-Wavelength Ratio Pyrometer Channel B [deg C] *)
    rBurningZoneTemp_PY_C_degC          : REAL;     (* Burning Zone Dual-Wavelength Ratio Pyrometer Channel C [deg C] *)

    (* ============================================================================================== *)
    (* 2oo3 TRIPLE MODULAR REDUNDANT (TMR) INSTRUMENT TRIPLET 3: PRECALCINER OUTLET THERMOCOUPLE      *)
    (* ============================================================================================== *)
    rCalcinerOutletTemp_TC_A_degC       : REAL;     (* Precalciner Riser Outlet Duplex Thermocouple Channel A [deg C] *)
    rCalcinerOutletTemp_TC_B_degC       : REAL;     (* Precalciner Riser Outlet Duplex Thermocouple Channel B [deg C] *)
    rCalcinerOutletTemp_TC_C_degC       : REAL;     (* Precalciner Riser Outlet Duplex Thermocouple Channel C [deg C] *)

    (* ============================================================================================== *)
    (* 2oo3 TRIPLE MODULAR REDUNDANT (TMR) INSTRUMENT TRIPLET 4: PREHEATER TOP RESIDUAL OXYGEN        *)
    (* ============================================================================================== *)
    rPreheaterTop_O2_A_pct              : REAL;     (* Top Stage Cyclone C1 Exhaust Residual Oxygen Analyzer Channel A [%] *)
    rPreheaterTop_O2_B_pct              : REAL;     (* Top Stage Cyclone C1 Exhaust Residual Oxygen Analyzer Channel B [%] *)
    rPreheaterTop_O2_C_pct              : REAL;     (* Top Stage Cyclone C1 Exhaust Residual Oxygen Analyzer Channel C [%] *)

    (* ============================================================================================== *)
    (* 2oo3 TRIPLE MODULAR REDUNDANT (TMR) INSTRUMENT TRIPLET 5: COOLER COMPARTMENT 1 PRESSURE        *)
    (* ============================================================================================== *)
    rCoolerUndergrate_PT_A_mbar         : REAL;     (* Clinker Cooler Compartment 1 Aeration Air Pressure Channel A [mbar] *)
    rCoolerUndergrate_PT_B_mbar         : REAL;     (* Clinker Cooler Compartment 1 Aeration Air Pressure Channel B [mbar] *)
    rCoolerUndergrate_PT_C_mbar         : REAL;     (* Clinker Cooler Compartment 1 Aeration Air Pressure Channel C [mbar] *)

    (* ============================================================================================== *)
    (* PREHEATER TOWER EXHAUST & CYCLONE STAGE TEMPERATURES                                           *)
    (* ============================================================================================== *)
    rCycloneGasTemp_C1_degC             : REAL;     (* Cyclone Stage 1 Gas Outlet Temperature [deg C] *)
    rCycloneGasTemp_C2_degC             : REAL;     (* Cyclone Stage 2 Gas Outlet Temperature [deg C] *)
    rCycloneGasTemp_C3_degC             : REAL;     (* Cyclone Stage 3 Gas Outlet Temperature [deg C] *)
    rCycloneGasTemp_C4_degC             : REAL;     (* Cyclone Stage 4 Gas Outlet Temperature [deg C] *)
    rCycloneGasTemp_C5_degC             : REAL;     (* Cyclone Stage 5 Bottom Stage Gas Outlet Temperature [deg C] *)
    rPreheaterTop_CO_ppm                : REAL;     (* Top Stage Preheater Carbon Monoxide (CO) Concentration [ppm] *)
    rPreheaterTop_NOx_ppm               : REAL;     (* Top Stage Preheater Nitrogen Oxides (NOx) Concentration [ppm] *)
    rPreheaterTop_SO2_mgNm3             : REAL;     (* Top Stage Preheater Sulfur Dioxide (SO2) Concentration [mg/Nm3] *)
    rIDFanSuctionDraft_mbar             : REAL;     (* Preheater Induced Draft (ID) Fan Inlet Suction Pressure [mbar] *)
    rIDFanOperatingSpeed_rpm            : REAL;     (* Preheater Induced Draft (ID) Fan VFD Running Speed [rpm] *)

    (* ============================================================================================== *)
    (* KILN DRIVE MECHANICAL, SHELL MONITORING & TYRE CREEP SENSORS                                  *)
    (* ============================================================================================== *)
    rKilnDriveSpeed_Feedback_rpm        : REAL;     (* Kiln Girth Gear Drive Rotational Speed Feedback [rpm] *)
    rKilnDriveMotorTorque1_kNm          : REAL;     (* Kiln Drive Dual-Motor 1 Operating Torque [kNm] *)
    rKilnDriveMotorTorque2_kNm          : REAL;     (* Kiln Drive Dual-Motor 2 Operating Torque [kNm] *)
    rKilnDriveMotorCurrent1_A           : REAL;     (* Kiln Drive Dual-Motor 1 Stator Current [A] *)
    rKilnDriveMotorCurrent2_A           : REAL;     (* Kiln Drive Dual-Motor 2 Stator Current [A] *)
    rTyreSlipPulseInterval_Tyre_s       : REAL;     (* Tyre Creep Proximity Sensor Pulse Time Delta [s] *)
    rTyreSlipPulseInterval_Shell_s      : REAL;     (* Kiln Shell Reference Flag Proximity Pulse Time Delta [s] *)
    rKilnShellIR_Scanner_40Point_degC   : ARRAY[1..40] OF REAL; (* 40-Point Infrared Shell Line Scanner Profile [deg C] *)

    (* ============================================================================================== *)
    (* CLINKER COOLER MECHANICAL & THERMAL AERATION SENSORS                                          *)
    (* ============================================================================================== *)
    rCoolerSecondaryAirTemp_degC        : REAL;     (* Clinker Cooler Secondary Combustion Air Recovery Temp [deg C] *)
    rCoolerSecondaryAirDraft_mbar       : REAL;     (* Rotary Kiln Discharge Hood Static Pressure [mbar] *)
    rCoolerClinkerDischargeTemp_degC    : REAL;     (* Cooled Clinker Discharge Apron Conveyor Temp [deg C] *)
    rCoolerGrateSpeed_Feedback_spm      : REAL;     (* Hydraulic Reciprocating Grate Stroke Rate Feedback [strokes/min] *)
    rCoolerUndergrate_PT2_mbar          : REAL;     (* Clinker Cooler Compartment 2 Aeration Pressure [mbar] *)
    rCoolerUndergrate_PT3_mbar          : REAL;     (* Clinker Cooler Compartment 3 Aeration Pressure [mbar] *)
    rCoolerTotalAerationFlow_Nm3h       : REAL;     (* Clinker Cooler Total Under-Grate Aeration Air Flow [Nm3/h] *)
END_VAR
"""

def generate_var_output():
    return """VAR_OUTPUT
    (* ============================================================================================== *)
    (* MASTER SYSTEM STATUS & SAFETY SUPERVISORY FLAGS                                               *)
    (* ============================================================================================== *)
    bSystemReady                        : BOOL;     (* Kiln System Fully Operational & Ready for Production *)
    bProductionActive                   : BOOL;     (* Active Rotary Kiln Clinker Burning Operation Active *)
    bEmergencyTripActive                : BOOL;     (* Safety Interlock or Shell Hot-Spot Fast Fuel Trip Active *)
    nKilnOperationalState               : INT;      (* Current 12-Stage Production FSM State Code (0..12) *)

    (* ============================================================================================== *)
    (* 2oo3 TMR RECONCILED SENSOR VALUES & INTEGRATED METRICS                                        *)
    (* ============================================================================================== *)
    rVotedKilnInletDraft_mbar           : REAL;     (* 2oo3 Voted Kiln Inlet Static Draft Pressure [mbar] *)
    rVotedBurningZoneTemp_degC          : REAL;     (* 2oo3 Voted Burning Zone Sintering Temperature [deg C] *)
    rVotedCalcinerOutletTemp_degC       : REAL;     (* 2oo3 Voted Precalciner Riser Outlet Gas Temperature [deg C] *)
    rVotedPreheaterTop_O2_pct           : REAL;     (* 2oo3 Voted Top Cyclone Residual Oxygen [%] *)
    rVotedCoolerUndergrate_PT1_mbar     : REAL;     (* 2oo3 Voted Cooler Compartment 1 Pressure [mbar] *)
    rObservedFreeLime_CaO_pct           : REAL;     (* Real-Time Clinker Free-Lime (CaO_free) Soft Sensor Output [%] *)
    rEstimatedDegreeOfCalcination_pct   : REAL;     (* Calculated Apparent Meal Calcination Degree Prior to Kiln [%] *)
    rPeakShellTemperature_degC          : REAL;     (* Maximum Detected Longitudinal Kiln Shell Temperature [deg C] *)
    nPeakShellSliceIndex                : INT;      (* Longitudinal Slice Index (1..40) with Maximum Shell Hot-Spot *)
    rComputedTyreSlipAngle_mmprev       : REAL;     (* Calculated Tyre Creep Slip per Kiln Revolution [mm/rev] *)
    rDualDriveTorqueDeviation_pct       : REAL;     (* Torque Sharing Discrepancy Between Motor 1 & 2 [%] *)
    rFlameMomentum_N                    : REAL;     (* Main Burner Calculated Flame Momentum [N] *)
    rFlameMomentumRatio_NpMW            : REAL;     (* Burner Flame Momentum to Thermal Power Ratio [N/MW] *)
    rKilnThermalEfficiency_pct          : REAL;     (* Calculated Overall Specific Thermal Energy Efficiency [%] *)

    (* ============================================================================================== *)
    (* ACTUATOR COMMAND OUTPUTS FOR ROTARY KILN & PRECALCINER                                        *)
    (* ============================================================================================== *)
    rMainBurnerCoalCommand_tph          : REAL;     (* Main Burner Coal Dosing Feeder Speed Demand [t/h] *)
    rMainBurnerRDF_Command_tph          : REAL;     (* Main Burner Alternative Fuel Feeder Demand [t/h] *)
    rMainBurnerPrimaryAirFan_pct        : REAL;     (* Main Burner Primary Air Blower VFD Speed Command [%] *)
    rMainBurnerSwirlDamper_pct          : REAL;     (* Main Burner Tangential Swirl Air Damper Position [%] *)
    rCalcinerCoalCommand_tph            : REAL;     (* Calciner Pulverized Coal Dosing Feeder Command [t/h] *)
    rCalcinerRDF_Command_tph            : REAL;     (* Calciner Alternative Fuel Dosing Feeder Command [t/h] *)
    rKilnDriveSpeedCommand_rpm          : REAL;     (* Kiln Main Gear Drive Inverter Master Speed Setpoint [rpm] *)
    rKilnDriveMotor2_TorqueTrim_pct     : REAL;     (* Motor 2 Follower Torque Trim Command [%] *)
    rRawMealFeederCommand_tph           : REAL;     (* Top Stage Preheater Raw Meal Flow Rate Command [t/h] *)
    rIDFanSpeedCommand_pct              : REAL;     (* Preheater Induced Draft (ID) Fan VFD Speed Command [%] *)
    rTertiaryAirDamperCommand_pct       : REAL;     (* Tertiary Air Duct (TAD) Control Damper Position [%] *)

    (* ============================================================================================== *)
    (* CLINKER COOLER & SHELL COOLING ACTUATOR OUTPUTS                                               *)
    (* ============================================================================================== *)
    rCoolerGrateSpeedCommand_spm        : REAL;     (* Reciprocating Grate Hydraulic Proportional Drive Speed [strokes/min] *)
    rCoolerAerationFanDamper1_pct       : REAL;     (* Grate Compartment 1 Aeration Air Damper [%] *)
    rCoolerAerationFanDamper2_pct       : REAL;     (* Grate Compartment 2 Aeration Air Damper [%] *)
    rCoolerAerationFanDamper3_pct       : REAL;     (* Grate Compartment 3 Aeration Air Damper [%] *)
    bShellCoolingFanBank1_On            : BOOL;     (* Shell Infrared Hot-Spot Cooling Fan Bank 1 Run Solenoid *)
    bShellCoolingFanBank2_On            : BOOL;     (* Shell Infrared Hot-Spot Cooling Fan Bank 2 Run Solenoid *)
    bEmergencyCoalCutoffValve           : BOOL;     (* Emergency Fast-Acting Pulverized Coal Shutoff Valve (1=Open, 0=Tripped) *)

    (* ============================================================================================== *)
    (* 32-BIT BIT-PACKED STATUS WORDS & ISA-18.2 ALARMS                                              *)
    (* ============================================================================================== *)
    dwKilnStatusWord                    : DWORD;    (* 32-Bit Kiln System Operational Status Bitmask *)
    dwKilnDiagnosticWord                : DWORD;    (* 32-Bit Kiln Hardware Alarm and Fault Diagnostic Word *)
    dwPreheaterStatusWord               : DWORD;    (* 32-Bit Cyclone Preheater & Calciner Diagnostic Bitmask *)
    dwCoolerStatusWord                  : DWORD;    (* 32-Bit Clinker Cooler Subsystem Diagnostic Word *)
    bAlarm_BurningZoneOverTemp_HH       : BOOL;     (* High-High Burning Zone Sintering Temperature Alarm (>1520 deg C) *)
    bAlarm_KilnShellHotSpot_HH          : BOOL;     (* High-High Kiln Shell Red Hot-Spot Alarm (>420 deg C) *)
    bAlarm_KilnInletPositivePressure_HH : BOOL;     (* High-High Kiln Inlet Draft Positive Pressure Blowback Alarm (>+0.5 mbar) *)
    bAlarm_PreheaterCO_ExplosionRisk_HH : BOOL;     (* High-High Cyclone Preheater Carbon Monoxide Explosive Range Alarm (>2.5% CO) *)
    bAlarm_CalcinerUnderTemp_LL         : BOOL;     (* Low-Low Calciner Flame Quenching Temperature Alarm (<820 deg C) *)
    bAlarm_DriveTorqueImbalance_H       : BOOL;     (* High Kiln Dual Motor Torque Discrepancy Trip (>10% deviation) *)
    bAlarm_TyreSlipHigh_H               : BOOL;     (* High Kiln Tyre Creep Slip Alarm (>25 mm/rev or <2 mm/rev constricting) *)
    bAlarm_FreeLimeOutOfSpec_H          : BOOL;     (* Clinker Free-Lime CaO Quality Out of Tolerance Alarm (>2.0% or <0.5%) *)
END_VAR
"""

def generate_var():
    return """VAR
    (* ============================================================================================== *)
    (* SYSTEM CONSTANTS & EXECUTION PARAMETERS                                                        *)
    (* ============================================================================================== *)
    T_CYCLE_SEC                         : REAL := 0.050;    (* Deterministic Task Scan Interval Ts = 50 ms [s] *)
    NUM_STATES                          : INT := 8;         (* Cyber-Physical State Dimension *)
    NUM_INPUTS                          : INT := 8;         (* Manipulated Actuator Dimension *)
    NUM_DISTURBANCES                    : INT := 4;         (* External Disturbance Dimension *)
    NUM_SHELL_SLICES                    : INT := 40;        (* Longitudinal Shell Scanner Slices *)
    PREDICTION_HORIZON_NP               : INT := 5;         (* Receding-Horizon MPC Step Depth *)

    (* ============================================================================================== *)
    (* DISCRETE STATE-SPACE MATRICES & CYBER-PHYSICAL OBSERVER                                        *)
    (* x[k+1] = A * x[k] + B * u[k] + E * d[k]                                                        *)
    (* y[k]   = C * x[k] + D * u[k]                                                                   *)
    (* ============================================================================================== *)
    a_mat                               : ARRAY[1..8, 1..8] OF REAL;    (* State Transition Matrix A (8x8) *)
    b_mat                               : ARRAY[1..8, 1..8] OF REAL;    (* Input Coupling Matrix B (8x8) *)
    c_mat                               : ARRAY[1..8, 1..8] OF REAL;    (* Output Measurement Matrix C (8x8) *)
    d_mat                               : ARRAY[1..8, 1..8] OF REAL;    (* Feedthrough Transmission Matrix D (8x8) *)
    e_mat                               : ARRAY[1..8, 1..4] OF REAL;    (* Disturbance Coupling Matrix E (8x4) *)
    l_obs                               : ARRAY[1..8] OF REAL;          (* Luenberger Observer Correction Gains *)

    x_state                             : ARRAY[1..8] OF REAL;          (* Estimated Cyber-Physical State x[k] *)
    x_next                              : ARRAY[1..8] OF REAL;          (* Predicted Next State Vector x[k+1] *)
    y_meas                              : ARRAY[1..8] OF REAL;          (* Reconciled Measurement Vector y[k] *)
    u_ctrl                              : ARRAY[1..8] OF REAL;          (* Active Actuator Command Vector u[k] *)
    u_prev                              : ARRAY[1..8] OF REAL;          (* Previous Scan Actuator Commands u[k-1] *)
    d_dist                              : ARRAY[1..4] OF REAL;          (* Disturbance Estimation Vector d[k] *)
    x_ref                               : ARRAY[1..8] OF REAL;          (* Reference State Setpoint Trajectory *)
    u_ref                               : ARRAY[1..8] OF REAL;          (* Nominal Equilibrium Actuator Command *)
    u_tentative                         : ARRAY[1..8] OF REAL;          (* Candidate Actuator Command *)
    grad_u                              : ARRAY[1..8] OF REAL;          (* Projected Gradient Descent Vector *)
    delta_u                             : ARRAY[1..8] OF REAL;          (* Rate-Limited Step Delta Vector *)

    (* ============================================================================================== *)
    (* MODEL PREDICTIVE CONTROL (MPC) COST MATRICES & PROJECTION BOUNDS                               *)
    (* ============================================================================================== *)
    q_diag                              : ARRAY[1..8] OF REAL;          (* State Error Penalty Diagonal Q *)
    r_diag                              : ARRAY[1..8] OF REAL;          (* Actuator Effort Penalty Diagonal R *)
    s_diag                              : ARRAY[1..8] OF REAL;          (* Slew Rate Slew Penalty Diagonal S *)
    p_diag                              : ARRAY[1..8] OF REAL;          (* Terminal State Weight Diagonal P *)
    u_box_min                           : ARRAY[1..8] OF REAL;          (* Actuator Physical Lower Bound Box Sat *)
    u_box_max                           : ARRAY[1..8] OF REAL;          (* Actuator Physical Upper Bound Box Sat *)
    du_slew_max                         : ARRAY[1..8] OF REAL;          (* Max Allowable Actuator Slew Rate *)
    rMpcAlphaStep                       : REAL := 0.015;                (* PGD Optimization Gradient Step Length *)
    rTotalCostFunctional                : REAL := 0.0;                  (* Accumulated Quadratic Cost J *)

    (* ============================================================================================== *)
    (* 2oo3 TMR VOTING REGISTERS, DISCREPANCY TIMERS & HEALTH FLAGS                                   *)
    (* ============================================================================================== *)
    (* Triplet 1: Kiln Inlet Draft Pressure *)
    rDraft_Delta_AB                     : REAL;     (* |PT_A - PT_B| [mbar] *)
    rDraft_Delta_BC                     : REAL;     (* |PT_B - PT_C| [mbar] *)
    rDraft_Delta_CA                     : REAL;     (* |PT_C - PT_A| [mbar] *)
    rDraft_DiscrepancyLimit_mbar        : REAL := 0.8;      (* Discrepancy Tolerance Window [mbar] *)
    rDraft_DiscrepancyTimer_s           : REAL := 0.0;      (* Discrepancy Persistence Integrator [s] *)
    bDraft_ChA_Valid                    : BOOL := TRUE;     (* Channel A Sensor Health Flag *)
    bDraft_ChB_Valid                    : BOOL := TRUE;     (* Channel B Sensor Health Flag *)
    bDraft_ChC_Valid                    : BOOL := TRUE;     (* Channel C Sensor Health Flag *)
    nDraft_DegradedMode                 : INT := 3;         (* 3=2oo3, 2=1oo2, 1=Single, 0=Fail-Safe *)

    (* Triplet 2: Burning Zone Optical Pyrometer *)
    rBZ_Delta_AB                        : REAL;     (* |PY_A - PY_B| [deg C] *)
    rBZ_Delta_BC                        : REAL;     (* |PY_B - PY_C| [deg C] *)
    rBZ_Delta_CA                        : REAL;     (* |PY_C - PY_A| [deg C] *)
    rBZ_DiscrepancyLimit_degC           : REAL := 25.0;     (* Pyrometer Discrepancy Limit [deg C] *)
    rBZ_DiscrepancyTimer_s              : REAL := 0.0;      (* Pyrometer Discrepancy Integrator [s] *)
    bBZ_ChA_Valid                       : BOOL := TRUE;     (* Pyrometer Channel A Health Flag *)
    bBZ_ChB_Valid                       : BOOL := TRUE;     (* Pyrometer Channel B Health Flag *)
    bBZ_ChC_Valid                       : BOOL := TRUE;     (* Pyrometer Channel C Health Flag *)
    nBZ_DegradedMode                    : INT := 3;         (* 3=2oo3, 2=1oo2, 1=Single, 0=Fail-Safe *)

    (* Triplet 3: Precalciner Outlet Thermocouple *)
    rCalc_Delta_AB                      : REAL;     (* |TC_A - TC_B| [deg C] *)
    rCalc_Delta_BC                      : REAL;     (* |TC_B - TC_C| [deg C] *)
    rCalc_Delta_CA                      : REAL;     (* |TC_C - TC_A| [deg C] *)
    rCalc_DiscrepancyLimit_degC         : REAL := 15.0;     (* Calciner TC Discrepancy Limit [deg C] *)
    rCalc_DiscrepancyTimer_s            : REAL := 0.0;      (* Calciner TC Discrepancy Integrator [s] *)
    bCalc_ChA_Valid                     : BOOL := TRUE;     (* Calciner TC Channel A Health Flag *)
    bCalc_ChB_Valid                     : BOOL := TRUE;     (* Calciner TC Channel B Health Flag *)
    bCalc_ChC_Valid                     : BOOL := TRUE;     (* Calciner TC Channel C Health Flag *)
    nCalc_DegradedMode                  : INT := 3;         (* 3=2oo3, 2=1oo2, 1=Single, 0=Fail-Safe *)

    (* Triplet 4: Preheater Top Stage Residual Oxygen *)
    rO2_Delta_AB                        : REAL;     (* |O2_A - O2_B| [%] *)
    rO2_Delta_BC                        : REAL;     (* |O2_B - O2_C| [%] *)
    rO2_Delta_CA                        : REAL;     (* |O2_C - O2_A| [%] *)
    rO2_DiscrepancyLimit_pct            : REAL := 0.40;     (* Oxygen Analyzer Discrepancy Limit [%] *)
    rO2_DiscrepancyTimer_s              : REAL := 0.0;      (* Oxygen Discrepancy Integrator [s] *)
    bO2_ChA_Valid                       : BOOL := TRUE;     (* Oxygen Analyzer Channel A Health Flag *)
    bO2_ChB_Valid                       : BOOL := TRUE;     (* Oxygen Analyzer Channel B Health Flag *)
    bO2_ChC_Valid                       : BOOL := TRUE;     (* Oxygen Analyzer Channel C Health Flag *)
    nO2_DegradedMode                    : INT := 3;         (* 3=2oo3, 2=1oo2, 1=Single, 0=Fail-Safe *)

    (* Triplet 5: Cooler Compartment 1 Pressure *)
    rCool1_Delta_AB                     : REAL;     (* |PT_A - PT_B| [mbar] *)
    rCool1_Delta_BC                     : REAL;     (* |PT_B - PT_C| [mbar] *)
    rCool1_Delta_CA                     : REAL;     (* |PT_C - PT_A| [mbar] *)
    rCool1_DiscrepancyLimit_mbar        : REAL := 4.0;      (* Cooler PT Discrepancy Limit [mbar] *)
    rCool1_DiscrepancyTimer_s           : REAL := 0.0;      (* Cooler PT Discrepancy Integrator [s] *)
    bCool1_ChA_Valid                    : BOOL := TRUE;     (* Cooler PT Channel A Health Flag *)
    bCool1_ChB_Valid                    : BOOL := TRUE;     (* Cooler PT Channel B Health Flag *)
    bCool1_ChC_Valid                    : BOOL := TRUE;     (* Cooler PT Channel C Health Flag *)
    nCool1_DegradedMode                 : INT := 3;         (* 3=2oo3, 2=1oo2, 1=Single, 0=Fail-Safe *)

    (* ============================================================================================== *)
    (* 40-POINT KILN SHELL SCANNER, REFRACTORY THICKNESS & TYRE SLIP REGISTERS                        *)
    (* ============================================================================================== *)
    rKilnShellTemp_40Point              : ARRAY[1..40] OF REAL; (* Internal Shell Temperature Map [deg C] *)
    rKilnRefractoryThickness_40Point_mm : ARRAY[1..40] OF REAL; (* Estimated Refractory Thickness [mm] *)
    bShellHotSpot_Detected              : ARRAY[1..40] OF BOOL; (* Hot-Spot Warning Flag per Slice *)
    rMaxShellTemp_degC                  : REAL := 260.0;    (* Highest Shell Surface Temperature [deg C] *)
    nMaxShellSlice                      : INT := 1;         (* Slice Index of Maximum Shell Hot-Spot *)
    rShellHotSpotTrip_degC              : REAL := 420.0;    (* Critical Shell Emergency Trip Threshold [deg C] *)
    rShellHotSpotWarn_degC              : REAL := 380.0;    (* Shell High Temperature Warning [deg C] *)
    rShellRingDipTrip_degC              : REAL := 180.0;    (* Kiln Coating Ring Cold Zone Threshold [deg C] *)

    rTyreSlipRaw_mm                     : REAL := 10.5;     (* Raw Measured Tyre Slip per Turn [mm] *)
    rTyreSlipFiltered_mmprev            : REAL := 10.5;     (* Filtered Tyre Creep Slip Rate [mm/rev] *)
    rTyreDiameter_m                     : REAL := 6.20;     (* Floating Tyre Inner Contact Diameter [m] *)
    rShellSeatDiameter_m                : REAL := 5.58;     (* Kiln Shell Tyre Seat Outer Diameter [m] *)
    rTyreSlipLimitHigh_mmprev           : REAL := 25.0;     (* High Slip Limit: Loose Tyre Warning [mm/rev] *)
    rTyreSlipLimitLow_mmprev            : REAL := 2.0;      (* Low Slip Limit: Constricting Tyre Trip [mm/rev] *)

    (* ============================================================================================== *)
    (* DUAL-DRIVE MASTER-FOLLOWER TORQUE SHARING PI CONTROLLER                                        *)
    (* ============================================================================================== *)
    rTorqueError_kNm                    : REAL := 0.0;      (* Drive Torque Error (Motor 1 - Motor 2) [kNm] *)
    rTorqueIntegral_kNm_s               : REAL := 0.0;      (* PI Controller Integral Accumulator [kNm*s] *)
    rTorqueKp                           : REAL := 0.045;    (* Proportional Gain for Speed Trim [rpm/kNm] *)
    rTorqueKi                           : REAL := 0.012;    (* Integral Gain for Speed Trim [rpm/(kNm*s)] *)
    rMotor2_TorqueTrim_Output           : REAL := 0.0;      (* Motor 2 Speed Trim Offset Output [%] *)
    rDualDriveTorqueMaxImbalance_pct    : REAL := 10.0;     (* Max Allowable Torque Imbalance [%] *)

    (* ============================================================================================== *)
    (* CLINKER FREE-LIME (CaO_free) SOFT SENSOR & FLAME MOMENTUM CONSTANTS                            *)
    (* ============================================================================================== *)
    rSoftSensor_FreeLime_Base           : REAL := 1.25;     (* Baseline Nominal Clinker Free Lime [%] *)
    rSoftSensor_TempWeight              : REAL := 0.0075;   (* Free Lime Sensitivity to Sintering Temp [%/deg C] *)
    rSoftSensor_TorqueWeight            : REAL := 0.0035;   (* Free Lime Sensitivity to Bed Torque [%/kNm] *)
    rSoftSensor_FeedWeight              : REAL := 0.0042;   (* Free Lime Sensitivity to Feed Rate [%/(t/h)] *)
    rSoftSensor_NOxWeight               : REAL := 0.0010;   (* Free Lime Sensitivity to Preheater NOx [%/ppm] *)
    rCalcination_k0                     : REAL := 1.85E6;   (* Calcination Arrhenius Pre-Exponential [1/s] *)
    rCalcination_Ea                     : REAL := 182000.0; (* Calcination Activation Energy [J/mol] *)
    rUniversalGas_R                     : REAL := 8.31446;  (* Universal Gas Constant [J/(mol*K)] *)

    (* ============================================================================================== *)
    (* DETERMINISTIC 12-STAGE PRODUCTION FINITE STATE MACHINE (FSM)                                   *)
    (* ============================================================================================== *)
    nOperationalState                   : INT := 0;         (* Active Operational State Code (0..12) *)
    rStateTimer_s                       : REAL := 0.0;      (* Current Operational Stage Dwell Timer [s] *)
    rStagePrePurgeDwell_s               : REAL := 120.0;    (* Stage 1 Purge Dwell Duration [s] *)
    rStageRefractoryCureDwell_s         : REAL := 600.0;    (* Stage 2 Refractory Curing Dwell [s] *)
    rStageTowerExpansionDwell_s         : REAL := 300.0;    (* Stage 3 Thermal Expansion Dwell [s] *)
    rStageIDFanBalanceDwell_s           : REAL := 180.0;    (* Stage 4 Draft Balancing Dwell [s] *)
    rStageBurnerIgnitionDwell_s         : REAL := 240.0;    (* Stage 5 Main Burner Ignition Dwell [s] *)
    rStageSinteringHeatupDwell_s        : REAL := 480.0;    (* Stage 6 Burning Zone Sintering Dwell [s] *)
    rStageMealFeedInitiationDwell_s     : REAL := 300.0;    (* Stage 7 Initial Meal Feeding Dwell [s] *)
    rStageCalcinerIgnitionDwell_s       : REAL := 360.0;    (* Stage 8 Calciner Ignition Dwell [s] *)
    rStageProductionScaleupDwell_s      : REAL := 600.0;    (* Stage 9 Feed Rate Ramp to 10k tpd [s] *)
    rStageCoolerSyncDwell_s             : REAL := 300.0;    (* Stage 10 Clinker Cooler Sync Dwell [s] *)
    rStageRDF_CofireDwell_s             : REAL := 450.0;    (* Stage 11 RDF Co-Firing Ramping Dwell [s] *)
    rStageAbortCoolingDwell_s           : REAL := 900.0;    (* Stage 12 Hot-Spot Emergency Abort Dwell [s] *)

    (* ============================================================================================== *)
    (* ISA-18.2 MULTI-TIER ALARM TRIP THRESHOLDS & CLEARANCE HYSTERESIS DEADBANDS                     *)
    (* ============================================================================================== *)
    rTrip_BZ_OverTemp_HH_degC           : REAL := 1520.0;   (* HH Trip: Burning Zone Sintering Temp [deg C] *)
    rTrip_BZ_OverTemp_H_degC            : REAL := 1480.0;   (* H Warn: Burning Zone Sintering Temp [deg C] *)
    rTrip_BZ_UnderTemp_L_degC           : REAL := 1390.0;   (* L Warn: Sintering Zone Cold Clinker [deg C] *)
    rTrip_BZ_UnderTemp_LL_degC          : REAL := 1350.0;   (* LL Trip: Sintering Zone Freezing Trip [deg C] *)
    rDeadband_BZ_degC                   : REAL := 8.0;      (* Burning Zone Alarm Reset Clearance Deadband [deg C] *)

    rTrip_InletDraft_Positive_HH_mbar   : REAL := 0.50;     (* HH Trip: Positive Kiln Inlet Draft Blowback [mbar] *)
    rTrip_InletDraft_High_H_mbar        : REAL := -0.20;    (* H Warn: Inadequate Kiln Inlet Draft [mbar] *)
    rTrip_InletDraft_Low_L_mbar         : REAL := -2.80;    (* L Warn: Excessive Suction Draft [mbar] *)
    rTrip_InletDraft_Deep_LL_mbar       : REAL := -3.80;    (* LL Trip: Extreme Negative Vacuum Draft [mbar] *)
    rDeadband_Draft_mbar                : REAL := 0.15;     (* Draft Pressure Reset Clearance Deadband [mbar] *)

    rTrip_Preheater_CO_Explosion_HH_ppm : REAL := 25000.0;  (* HH Trip: Preheater Top CO Explosive Limit [ppm] *)
    rTrip_Preheater_CO_High_H_ppm       : REAL := 12000.0;  (* H Warn: Preheater Top CO Combustion Incomplete [ppm] *)
    rDeadband_CO_ppm                    : REAL := 1500.0;   (* Carbon Monoxide Reset Clearance Deadband [ppm] *)

    rTrip_Calciner_OverTemp_HH_degC     : REAL := 950.0;    (* HH Trip: Calciner Refractory Overheating [deg C] *)
    rTrip_Calciner_High_H_degC          : REAL := 915.0;    (* H Warn: Calciner High Operating Temp [deg C] *)
    rTrip_Calciner_Low_L_degC           : REAL := 850.0;    (* L Warn: Calciner Low Decarbonation Temp [deg C] *)
    rTrip_Calciner_UnderTemp_LL_degC    : REAL := 815.0;    (* LL Trip: Calciner Flame Extinction Quench [deg C] *)
    rDeadband_Calciner_degC             : REAL := 6.0;      (* Calciner Alarm Reset Clearance Deadband [deg C] *)

    rTrip_FreeLime_High_H_pct           : REAL := 2.00;     (* H Warn: High Clinker Free Lime Incomplete Burn [%] *)
    rTrip_FreeLime_Low_L_pct            : REAL := 0.50;     (* L Warn: Low Free Lime Hard Burning Over-Fired [%] *)
    rDeadband_FreeLime_pct              : REAL := 0.10;     (* Free Lime Reset Clearance Deadband [%] *)

    (* Alarm State Latches *)
    bAlarm_BZ_HH_Latched                : BOOL := FALSE;
    bAlarm_BZ_H_Latched                 : BOOL := FALSE;
    bAlarm_BZ_L_Latched                 : BOOL := FALSE;
    bAlarm_BZ_LL_Latched                : BOOL := FALSE;
    bAlarm_InletDraft_HH_Latched        : BOOL := FALSE;
    bAlarm_InletDraft_H_Latched         : BOOL := FALSE;
    bAlarm_InletDraft_L_Latched         : BOOL := FALSE;
    bAlarm_InletDraft_LL_Latched        : BOOL := FALSE;
    bAlarm_PreheaterCO_HH_Latched       : BOOL := FALSE;
    bAlarm_PreheaterCO_H_Latched        : BOOL := FALSE;
    bAlarm_Calciner_HH_Latched          : BOOL := FALSE;
    bAlarm_Calciner_H_Latched           : BOOL := FALSE;
    bAlarm_Calciner_L_Latched           : BOOL := FALSE;
    bAlarm_Calciner_LL_Latched          : BOOL := FALSE;
    bAlarm_Shell_HH_Latched             : BOOL := FALSE;
    bAlarm_Shell_H_Latched              : BOOL := FALSE;
    bAlarm_Torque_H_Latched             : BOOL := FALSE;
    bAlarm_TyreSlip_H_Latched           : BOOL := FALSE;
    bAlarm_TyreSlip_L_Latched           : BOOL := FALSE;
    bAlarm_FreeLime_H_Latched           : BOOL := FALSE;
    bAlarm_FreeLime_L_Latched           : BOOL := FALSE;

    (* Iteration & Matrix Arithmetic Indices *)
    iIdx                                : INT := 1;
    jIdx                                : INT := 1;
    kIdx                                : INT := 1;
    mIdx                                : INT := 1;
    nIdx                                : INT := 1;
    rTempAccumulator                    : REAL := 0.0;
END_VAR
"""

def generate_phase1_tmr():
    return """
(* ============================================================================================== *)
(* === PHASE 1: 2oo3 TMR SENSOR VOTING WITH DISCREPANCY TIMERS & BUMPLESS DEGRADATION ===         *)
(* ============================================================================================== *)
(* 5 critical process instrument triplets undergo continuous pairwise deviation auditing,       *)
(* discrepancy time integration, and bumpless degradation from 2oo3 to 1oo2 to 1oo1 to model.     *)

(* ---------------------------------------------------------------------------------------------- *)
(* 1.1 KILN INLET DRAFT PRESSURE TRANSMITTER 2oo3 TMR VOTING                                      *)
(* ---------------------------------------------------------------------------------------------- *)
rDraft_Delta_AB := ABS(rKilnInletDraft_PT_A_mbar - rKilnInletDraft_PT_B_mbar);
rDraft_Delta_BC := ABS(rKilnInletDraft_PT_B_mbar - rKilnInletDraft_PT_C_mbar);
rDraft_Delta_CA := ABS(rKilnInletDraft_PT_C_mbar - rKilnInletDraft_PT_A_mbar);

IF (rDraft_Delta_AB > rDraft_DiscrepancyLimit_mbar) OR 
   (rDraft_Delta_BC > rDraft_DiscrepancyLimit_mbar) OR 
   (rDraft_Delta_CA > rDraft_DiscrepancyLimit_mbar) THEN
    rDraft_DiscrepancyTimer_s := rDraft_DiscrepancyTimer_s + T_CYCLE_SEC;
    IF rDraft_DiscrepancyTimer_s >= 2.00 THEN
        IF (rDraft_Delta_AB > rDraft_DiscrepancyLimit_mbar) AND (rDraft_Delta_CA > rDraft_DiscrepancyLimit_mbar) THEN
            bDraft_ChA_Valid := FALSE;
        END_IF;
        IF (rDraft_Delta_AB > rDraft_DiscrepancyLimit_mbar) AND (rDraft_Delta_BC > rDraft_DiscrepancyLimit_mbar) THEN
            bDraft_ChB_Valid := FALSE;
        END_IF;
        IF (rDraft_Delta_BC > rDraft_DiscrepancyLimit_mbar) AND (rDraft_Delta_CA > rDraft_DiscrepancyLimit_mbar) THEN
            bDraft_ChC_Valid := FALSE;
        END_IF;
    END_IF;
ELSE
    rDraft_DiscrepancyTimer_s := 0.0;
END_IF;

IF bAlarmReset THEN
    bDraft_ChA_Valid := TRUE;
    bDraft_ChB_Valid := TRUE;
    bDraft_ChC_Valid := TRUE;
    rDraft_DiscrepancyTimer_s := 0.0;
END_IF;

(* Voting Selection *)
IF bDraft_ChA_Valid AND bDraft_ChB_Valid AND bDraft_ChC_Valid THEN
    nDraft_DegradedMode := 3; (* Full 2oo3 Voting *)
    IF ((rKilnInletDraft_PT_A_mbar >= rKilnInletDraft_PT_B_mbar) AND (rKilnInletDraft_PT_A_mbar <= rKilnInletDraft_PT_C_mbar)) OR
       ((rKilnInletDraft_PT_A_mbar <= rKilnInletDraft_PT_B_mbar) AND (rKilnInletDraft_PT_A_mbar >= rKilnInletDraft_PT_C_mbar)) THEN
        rVotedKilnInletDraft_mbar := rKilnInletDraft_PT_A_mbar;
    ELSIF ((rKilnInletDraft_PT_B_mbar >= rKilnInletDraft_PT_A_mbar) AND (rKilnInletDraft_PT_B_mbar <= rKilnInletDraft_PT_C_mbar)) OR
          ((rKilnInletDraft_PT_B_mbar <= rKilnInletDraft_PT_A_mbar) AND (rKilnInletDraft_PT_B_mbar >= rKilnInletDraft_PT_C_mbar)) THEN
        rVotedKilnInletDraft_mbar := rKilnInletDraft_PT_B_mbar;
    ELSE
        rVotedKilnInletDraft_mbar := rKilnInletDraft_PT_C_mbar;
    END_IF;
ELSIF bDraft_ChA_Valid AND bDraft_ChB_Valid AND NOT bDraft_ChC_Valid THEN
    nDraft_DegradedMode := 2; (* 1oo2 Degraded Mode *)
    rVotedKilnInletDraft_mbar := (rKilnInletDraft_PT_A_mbar + rKilnInletDraft_PT_B_mbar) * 0.5;
ELSIF bDraft_ChA_Valid AND NOT bDraft_ChB_Valid AND bDraft_ChC_Valid THEN
    nDraft_DegradedMode := 2;
    rVotedKilnInletDraft_mbar := (rKilnInletDraft_PT_A_mbar + rKilnInletDraft_PT_C_mbar) * 0.5;
ELSIF NOT bDraft_ChA_Valid AND bDraft_ChB_Valid AND bDraft_ChC_Valid THEN
    nDraft_DegradedMode := 2;
    rVotedKilnInletDraft_mbar := (rKilnInletDraft_PT_B_mbar + rKilnInletDraft_PT_C_mbar) * 0.5;
ELSIF bDraft_ChA_Valid THEN
    nDraft_DegradedMode := 1; (* 1oo1 Single Channel Mode *)
    rVotedKilnInletDraft_mbar := rKilnInletDraft_PT_A_mbar;
ELSIF bDraft_ChB_Valid THEN
    nDraft_DegradedMode := 1;
    rVotedKilnInletDraft_mbar := rKilnInletDraft_PT_B_mbar;
ELSIF bDraft_ChC_Valid THEN
    nDraft_DegradedMode := 1;
    rVotedKilnInletDraft_mbar := rKilnInletDraft_PT_C_mbar;
ELSE
    nDraft_DegradedMode := 0; (* Fail-Safe Model Estimate *)
    rVotedKilnInletDraft_mbar := x_state[3];
END_IF;

(* ---------------------------------------------------------------------------------------------- *)
(* 1.2 BURNING ZONE TWO-COLOR OPTICAL PYROMETER 2oo3 TMR VOTING                                   *)
(* ---------------------------------------------------------------------------------------------- *)
rBZ_Delta_AB := ABS(rBurningZoneTemp_PY_A_degC - rBurningZoneTemp_PY_B_degC);
rBZ_Delta_BC := ABS(rBurningZoneTemp_PY_B_degC - rBurningZoneTemp_PY_C_degC);
rBZ_Delta_CA := ABS(rBurningZoneTemp_PY_C_degC - rBurningZoneTemp_PY_A_degC);

IF (rBZ_Delta_AB > rBZ_DiscrepancyLimit_degC) OR 
   (rBZ_Delta_BC > rBZ_DiscrepancyLimit_degC) OR 
   (rBZ_Delta_CA > rBZ_DiscrepancyLimit_degC) THEN
    rBZ_DiscrepancyTimer_s := rBZ_DiscrepancyTimer_s + T_CYCLE_SEC;
    IF rBZ_DiscrepancyTimer_s >= 2.00 THEN
        IF (rBZ_Delta_AB > rBZ_DiscrepancyLimit_degC) AND (rBZ_Delta_CA > rBZ_DiscrepancyLimit_degC) THEN
            bBZ_ChA_Valid := FALSE;
        END_IF;
        IF (rBZ_Delta_AB > rBZ_DiscrepancyLimit_degC) AND (rBZ_Delta_BC > rBZ_DiscrepancyLimit_degC) THEN
            bBZ_ChB_Valid := FALSE;
        END_IF;
        IF (rBZ_Delta_BC > rBZ_DiscrepancyLimit_degC) AND (rBZ_Delta_CA > rBZ_DiscrepancyLimit_degC) THEN
            bBZ_ChC_Valid := FALSE;
        END_IF;
    END_IF;
ELSE
    rBZ_DiscrepancyTimer_s := 0.0;
END_IF;

IF bAlarmReset THEN
    bBZ_ChA_Valid := TRUE;
    bBZ_ChB_Valid := TRUE;
    bBZ_ChC_Valid := TRUE;
    rBZ_DiscrepancyTimer_s := 0.0;
END_IF;

IF bBZ_ChA_Valid AND bBZ_ChB_Valid AND bBZ_ChC_Valid THEN
    nBZ_DegradedMode := 3;
    IF ((rBurningZoneTemp_PY_A_degC >= rBurningZoneTemp_PY_B_degC) AND (rBurningZoneTemp_PY_A_degC <= rBurningZoneTemp_PY_C_degC)) OR
       ((rBurningZoneTemp_PY_A_degC <= rBurningZoneTemp_PY_B_degC) AND (rBurningZoneTemp_PY_A_degC >= rBurningZoneTemp_PY_C_degC)) THEN
        rVotedBurningZoneTemp_degC := rBurningZoneTemp_PY_A_degC;
    ELSIF ((rBurningZoneTemp_PY_B_degC >= rBurningZoneTemp_PY_A_degC) AND (rBurningZoneTemp_PY_B_degC <= rBurningZoneTemp_PY_C_degC)) OR
          ((rBurningZoneTemp_PY_B_degC <= rBurningZoneTemp_PY_A_degC) AND (rBurningZoneTemp_PY_B_degC >= rBurningZoneTemp_PY_C_degC)) THEN
        rVotedBurningZoneTemp_degC := rBurningZoneTemp_PY_B_degC;
    ELSE
        rVotedBurningZoneTemp_degC := rBurningZoneTemp_PY_C_degC;
    END_IF;
ELSIF bBZ_ChA_Valid AND bBZ_ChB_Valid AND NOT bBZ_ChC_Valid THEN
    nBZ_DegradedMode := 2;
    rVotedBurningZoneTemp_degC := (rBurningZoneTemp_PY_A_degC + rBurningZoneTemp_PY_B_degC) * 0.5;
ELSIF bBZ_ChA_Valid AND NOT bBZ_ChB_Valid AND bBZ_ChC_Valid THEN
    nBZ_DegradedMode := 2;
    rVotedBurningZoneTemp_degC := (rBurningZoneTemp_PY_A_degC + rBurningZoneTemp_PY_C_degC) * 0.5;
ELSIF NOT bBZ_ChA_Valid AND bBZ_ChB_Valid AND bBZ_ChC_Valid THEN
    nBZ_DegradedMode := 2;
    rVotedBurningZoneTemp_degC := (rBurningZoneTemp_PY_B_degC + rBurningZoneTemp_PY_C_degC) * 0.5;
ELSIF bBZ_ChA_Valid THEN
    nBZ_DegradedMode := 1;
    rVotedBurningZoneTemp_degC := rBurningZoneTemp_PY_A_degC;
ELSIF bBZ_ChB_Valid THEN
    nBZ_DegradedMode := 1;
    rVotedBurningZoneTemp_degC := rBurningZoneTemp_PY_B_degC;
ELSIF bBZ_ChC_Valid THEN
    nBZ_DegradedMode := 1;
    rVotedBurningZoneTemp_degC := rBurningZoneTemp_PY_C_degC;
ELSE
    nBZ_DegradedMode := 0;
    rVotedBurningZoneTemp_degC := x_state[1];
END_IF;

(* ---------------------------------------------------------------------------------------------- *)
(* 1.3 PRECALCINER RISER OUTLET THERMOCOUPLE 2oo3 TMR VOTING                                      *)
(* ---------------------------------------------------------------------------------------------- *)
rCalc_Delta_AB := ABS(rCalcinerOutletTemp_TC_A_degC - rCalcinerOutletTemp_TC_B_degC);
rCalc_Delta_BC := ABS(rCalcinerOutletTemp_TC_B_degC - rCalcinerOutletTemp_TC_C_degC);
rCalc_Delta_CA := ABS(rCalcinerOutletTemp_TC_C_degC - rCalcinerOutletTemp_TC_A_degC);

IF (rCalc_Delta_AB > rCalc_DiscrepancyLimit_degC) OR 
   (rCalc_Delta_BC > rCalc_DiscrepancyLimit_degC) OR 
   (rCalc_Delta_CA > rCalc_DiscrepancyLimit_degC) THEN
    rCalc_DiscrepancyTimer_s := rCalc_DiscrepancyTimer_s + T_CYCLE_SEC;
    IF rCalc_DiscrepancyTimer_s >= 2.00 THEN
        IF (rCalc_Delta_AB > rCalc_DiscrepancyLimit_degC) AND (rCalc_Delta_CA > rCalc_DiscrepancyLimit_degC) THEN
            bCalc_ChA_Valid := FALSE;
        END_IF;
        IF (rCalc_Delta_AB > rCalc_DiscrepancyLimit_degC) AND (rCalc_Delta_BC > rCalc_DiscrepancyLimit_degC) THEN
            bCalc_ChB_Valid := FALSE;
        END_IF;
        IF (rCalc_Delta_BC > rCalc_DiscrepancyLimit_degC) AND (rCalc_Delta_CA > rCalc_DiscrepancyLimit_degC) THEN
            bCalc_ChC_Valid := FALSE;
        END_IF;
    END_IF;
ELSE
    rCalc_DiscrepancyTimer_s := 0.0;
END_IF;

IF bAlarmReset THEN
    bCalc_ChA_Valid := TRUE;
    bCalc_ChB_Valid := TRUE;
    bCalc_ChC_Valid := TRUE;
    rCalc_DiscrepancyTimer_s := 0.0;
END_IF;

IF bCalc_ChA_Valid AND bCalc_ChB_Valid AND bCalc_ChC_Valid THEN
    nCalc_DegradedMode := 3;
    IF ((rCalcinerOutletTemp_TC_A_degC >= rCalcinerOutletTemp_TC_B_degC) AND (rCalcinerOutletTemp_TC_A_degC <= rCalcinerOutletTemp_TC_C_degC)) OR
       ((rCalcinerOutletTemp_TC_A_degC <= rCalcinerOutletTemp_TC_B_degC) AND (rCalcinerOutletTemp_TC_A_degC >= rCalcinerOutletTemp_TC_C_degC)) THEN
        rVotedCalcinerOutletTemp_degC := rCalcinerOutletTemp_TC_A_degC;
    ELSIF ((rCalcinerOutletTemp_TC_B_degC >= rCalcinerOutletTemp_TC_A_degC) AND (rCalcinerOutletTemp_TC_B_degC <= rCalcinerOutletTemp_TC_C_degC)) OR
          ((rCalcinerOutletTemp_TC_B_degC <= rCalcinerOutletTemp_TC_A_degC) AND (rCalcinerOutletTemp_TC_B_degC >= rCalcinerOutletTemp_TC_C_degC)) THEN
        rVotedCalcinerOutletTemp_degC := rCalcinerOutletTemp_TC_B_degC;
    ELSE
        rVotedCalcinerOutletTemp_degC := rCalcinerOutletTemp_TC_C_degC;
    END_IF;
ELSIF bCalc_ChA_Valid AND bCalc_ChB_Valid AND NOT bCalc_ChC_Valid THEN
    nCalc_DegradedMode := 2;
    rVotedCalcinerOutletTemp_degC := (rCalcinerOutletTemp_TC_A_degC + rCalcinerOutletTemp_TC_B_degC) * 0.5;
ELSIF bCalc_ChA_Valid AND NOT bCalc_ChB_Valid AND bCalc_ChC_Valid THEN
    nCalc_DegradedMode := 2;
    rVotedCalcinerOutletTemp_degC := (rCalcinerOutletTemp_TC_A_degC + rCalcinerOutletTemp_TC_C_degC) * 0.5;
ELSIF NOT bCalc_ChA_Valid AND bCalc_ChB_Valid AND bCalc_ChC_Valid THEN
    nCalc_DegradedMode := 2;
    rVotedCalcinerOutletTemp_degC := (rCalcinerOutletTemp_TC_B_degC + rCalcinerOutletTemp_TC_C_degC) * 0.5;
ELSIF bCalc_ChA_Valid THEN
    nCalc_DegradedMode := 1;
    rVotedCalcinerOutletTemp_degC := rCalcinerOutletTemp_TC_A_degC;
ELSIF bCalc_ChB_Valid THEN
    nCalc_DegradedMode := 1;
    rVotedCalcinerOutletTemp_degC := rCalcinerOutletTemp_TC_B_degC;
ELSIF bCalc_ChC_Valid THEN
    nCalc_DegradedMode := 1;
    rVotedCalcinerOutletTemp_degC := rCalcinerOutletTemp_TC_C_degC;
ELSE
    nCalc_DegradedMode := 0;
    rVotedCalcinerOutletTemp_degC := x_state[2];
END_IF;

(* ---------------------------------------------------------------------------------------------- *)
(* 1.4 PREHEATER TOP STAGE C1 RESIDUAL OXYGEN ANALYZER 2oo3 TMR VOTING                            *)
(* ---------------------------------------------------------------------------------------------- *)
rO2_Delta_AB := ABS(rPreheaterTop_O2_A_pct - rPreheaterTop_O2_B_pct);
rO2_Delta_BC := ABS(rPreheaterTop_O2_B_pct - rPreheaterTop_O2_C_pct);
rO2_Delta_CA := ABS(rPreheaterTop_O2_C_pct - rPreheaterTop_O2_A_pct);

IF (rO2_Delta_AB > rO2_DiscrepancyLimit_pct) OR 
   (rO2_Delta_BC > rO2_DiscrepancyLimit_pct) OR 
   (rO2_Delta_CA > rO2_DiscrepancyLimit_pct) THEN
    rO2_DiscrepancyTimer_s := rO2_DiscrepancyTimer_s + T_CYCLE_SEC;
    IF rO2_DiscrepancyTimer_s >= 2.50 THEN
        IF (rO2_Delta_AB > rO2_DiscrepancyLimit_pct) AND (rO2_Delta_CA > rO2_DiscrepancyLimit_pct) THEN
            bO2_ChA_Valid := FALSE;
        END_IF;
        IF (rO2_Delta_AB > rO2_DiscrepancyLimit_pct) AND (rO2_Delta_BC > rO2_DiscrepancyLimit_pct) THEN
            bO2_ChB_Valid := FALSE;
        END_IF;
        IF (rO2_Delta_BC > rO2_DiscrepancyLimit_pct) AND (rO2_Delta_CA > rO2_DiscrepancyLimit_pct) THEN
            bO2_ChC_Valid := FALSE;
        END_IF;
    END_IF;
ELSE
    rO2_DiscrepancyTimer_s := 0.0;
END_IF;

IF bAlarmReset THEN
    bO2_ChA_Valid := TRUE;
    bO2_ChB_Valid := TRUE;
    bO2_ChC_Valid := TRUE;
    rO2_DiscrepancyTimer_s := 0.0;
END_IF;

IF bO2_ChA_Valid AND bO2_ChB_Valid AND bO2_ChC_Valid THEN
    nO2_DegradedMode := 3;
    IF ((rPreheaterTop_O2_A_pct >= rPreheaterTop_O2_B_pct) AND (rPreheaterTop_O2_A_pct <= rPreheaterTop_O2_C_pct)) OR
       ((rPreheaterTop_O2_A_pct <= rPreheaterTop_O2_B_pct) AND (rPreheaterTop_O2_A_pct >= rPreheaterTop_O2_C_pct)) THEN
        rVotedPreheaterTop_O2_pct := rPreheaterTop_O2_A_pct;
    ELSIF ((rPreheaterTop_O2_B_pct >= rPreheaterTop_O2_A_pct) AND (rPreheaterTop_O2_B_pct <= rPreheaterTop_O2_C_pct)) OR
          ((rPreheaterTop_O2_B_pct <= rPreheaterTop_O2_A_pct) AND (rPreheaterTop_O2_B_pct >= rPreheaterTop_O2_C_pct)) THEN
        rVotedPreheaterTop_O2_pct := rPreheaterTop_O2_B_pct;
    ELSE
        rVotedPreheaterTop_O2_pct := rPreheaterTop_O2_C_pct;
    END_IF;
ELSIF bO2_ChA_Valid AND bO2_ChB_Valid AND NOT bO2_ChC_Valid THEN
    nO2_DegradedMode := 2;
    rVotedPreheaterTop_O2_pct := (rPreheaterTop_O2_A_pct + rPreheaterTop_O2_B_pct) * 0.5;
ELSIF bO2_ChA_Valid AND NOT bO2_ChB_Valid AND bO2_ChC_Valid THEN
    nO2_DegradedMode := 2;
    rVotedPreheaterTop_O2_pct := (rPreheaterTop_O2_A_pct + rPreheaterTop_O2_C_pct) * 0.5;
ELSIF NOT bO2_ChA_Valid AND bO2_ChB_Valid AND bO2_ChC_Valid THEN
    nO2_DegradedMode := 2;
    rVotedPreheaterTop_O2_pct := (rPreheaterTop_O2_B_pct + rPreheaterTop_O2_C_pct) * 0.5;
ELSIF bO2_ChA_Valid THEN
    nO2_DegradedMode := 1;
    rVotedPreheaterTop_O2_pct := rPreheaterTop_O2_A_pct;
ELSIF bO2_ChB_Valid THEN
    nO2_DegradedMode := 1;
    rVotedPreheaterTop_O2_pct := rPreheaterTop_O2_B_pct;
ELSIF bO2_ChC_Valid THEN
    nO2_DegradedMode := 1;
    rVotedPreheaterTop_O2_pct := rPreheaterTop_O2_C_pct;
ELSE
    nO2_DegradedMode := 0;
    rVotedPreheaterTop_O2_pct := x_state[7];
END_IF;

(* ---------------------------------------------------------------------------------------------- *)
(* 1.5 CLINKER COOLER COMPARTMENT 1 AERATION PRESSURE 2oo3 TMR VOTING                            *)
(* ---------------------------------------------------------------------------------------------- *)
rCool1_Delta_AB := ABS(rCoolerUndergrate_PT_A_mbar - rCoolerUndergrate_PT_B_mbar);
rCool1_Delta_BC := ABS(rCoolerUndergrate_PT_B_mbar - rCoolerUndergrate_PT_C_mbar);
rCool1_Delta_CA := ABS(rCoolerUndergrate_PT_C_mbar - rCoolerUndergrate_PT_A_mbar);

IF (rCool1_Delta_AB > rCool1_DiscrepancyLimit_mbar) OR 
   (rCool1_Delta_BC > rCool1_DiscrepancyLimit_mbar) OR 
   (rCool1_Delta_CA > rCool1_DiscrepancyLimit_mbar) THEN
    rCool1_DiscrepancyTimer_s := rCool1_DiscrepancyTimer_s + T_CYCLE_SEC;
    IF rCool1_DiscrepancyTimer_s >= 2.00 THEN
        IF (rCool1_Delta_AB > rCool1_DiscrepancyLimit_mbar) AND (rCool1_Delta_CA > rCool1_DiscrepancyLimit_mbar) THEN
            bCool1_ChA_Valid := FALSE;
        END_IF;
        IF (rCool1_Delta_AB > rCool1_DiscrepancyLimit_mbar) AND (rCool1_Delta_BC > rCool1_DiscrepancyLimit_mbar) THEN
            bCool1_ChB_Valid := FALSE;
        END_IF;
        IF (rCool1_Delta_BC > rCool1_DiscrepancyLimit_mbar) AND (rCool1_Delta_CA > rCool1_DiscrepancyLimit_mbar) THEN
            bCool1_ChC_Valid := FALSE;
        END_IF;
    END_IF;
ELSE
    rCool1_DiscrepancyTimer_s := 0.0;
END_IF;

IF bAlarmReset THEN
    bCool1_ChA_Valid := TRUE;
    bCool1_ChB_Valid := TRUE;
    bCool1_ChC_Valid := TRUE;
    rCool1_DiscrepancyTimer_s := 0.0;
END_IF;

IF bCool1_ChA_Valid AND bCool1_ChB_Valid AND bCool1_ChC_Valid THEN
    nCool1_DegradedMode := 3;
    IF ((rCoolerUndergrate_PT_A_mbar >= rCoolerUndergrate_PT_B_mbar) AND (rCoolerUndergrate_PT_A_mbar <= rCoolerUndergrate_PT_C_mbar)) OR
       ((rCoolerUndergrate_PT_A_mbar <= rCoolerUndergrate_PT_B_mbar) AND (rCoolerUndergrate_PT_A_mbar >= rCoolerUndergrate_PT_C_mbar)) THEN
        rVotedCoolerUndergrate_PT1_mbar := rCoolerUndergrate_PT_A_mbar;
    ELSIF ((rCoolerUndergrate_PT_B_mbar >= rCoolerUndergrate_PT_A_mbar) AND (rCoolerUndergrate_PT_B_mbar <= rCoolerUndergrate_PT_C_mbar)) OR
          ((rCoolerUndergrate_PT_B_mbar <= rCoolerUndergrate_PT_A_mbar) AND (rCoolerUndergrate_PT_B_mbar >= rCoolerUndergrate_PT_C_mbar)) THEN
        rVotedCoolerUndergrate_PT1_mbar := rCoolerUndergrate_PT_B_mbar;
    ELSE
        rVotedCoolerUndergrate_PT1_mbar := rCoolerUndergrate_PT_C_mbar;
    END_IF;
ELSIF bCool1_ChA_Valid AND bCool1_ChB_Valid AND NOT bCool1_ChC_Valid THEN
    nCool1_DegradedMode := 2;
    rVotedCoolerUndergrate_PT1_mbar := (rCoolerUndergrate_PT_A_mbar + rCoolerUndergrate_PT_B_mbar) * 0.5;
ELSIF bCool1_ChA_Valid AND NOT bCool1_ChB_Valid AND bCool1_ChC_Valid THEN
    nCool1_DegradedMode := 2;
    rVotedCoolerUndergrate_PT1_mbar := (rCoolerUndergrate_PT_A_mbar + rCoolerUndergrate_PT_C_mbar) * 0.5;
ELSIF NOT bCool1_ChA_Valid AND bCool1_ChB_Valid AND bCool1_ChC_Valid THEN
    nCool1_DegradedMode := 2;
    rVotedCoolerUndergrate_PT1_mbar := (rCoolerUndergrate_PT_B_mbar + rCoolerUndergrate_PT_C_mbar) * 0.5;
ELSIF bCool1_ChA_Valid THEN
    nCool1_DegradedMode := 1;
    rVotedCoolerUndergrate_PT1_mbar := rCoolerUndergrate_PT_A_mbar;
ELSIF bCool1_ChB_Valid THEN
    nCool1_DegradedMode := 1;
    rVotedCoolerUndergrate_PT1_mbar := rCoolerUndergrate_PT_B_mbar;
ELSIF bCool1_ChC_Valid THEN
    nCool1_DegradedMode := 1;
    rVotedCoolerUndergrate_PT1_mbar := rCoolerUndergrate_PT_C_mbar;
ELSE
    nCool1_DegradedMode := 0;
    rVotedCoolerUndergrate_PT1_mbar := 52.0; (* Nominal under-grate baseline *)
END_IF;
"""

def generate_phase2_shell_tyre_torque():
    return """
(* ============================================================================================== *)
(* === PHASE 2: 40-POINT KILN SHELL SCANNER, TYRE SLIP OBSERVER & DUAL-DRIVE TORQUE SHARING ===   *)
(* ============================================================================================== *)
(* Longitudinal thermal mapping, coating thickness estimation, tyre creep slip dynamics,         *)
(* and dual 1200 kW slip-ring motor master-follower torque load balancing.                        *)

(* ---------------------------------------------------------------------------------------------- *)
(* 2.1 40-POINT INFRARED SHELL LINE SCANNER & REFRACTORY COATING INVERSE OBSERVER                 *)
(* ---------------------------------------------------------------------------------------------- *)
rMaxShellTemp_degC := -100.0;
nMaxShellSlice := 1;

FOR iIdx := 1 TO 40 DO
    rKilnShellTemp_40Point[iIdx] := rKilnShellIR_Scanner_40Point_degC[iIdx];
    
    (* Peak Temperature Tracking *)
    IF rKilnShellTemp_40Point[iIdx] > rMaxShellTemp_degC THEN
        rMaxShellTemp_degC := rKilnShellTemp_40Point[iIdx];
        nMaxShellSlice := iIdx;
    END_IF;

    (* Refractory Lining Thickness Soft Estimation [mm] *)
    (* Inversely proportional to shell surface conduction heat loss *)
    IF rKilnShellTemp_40Point[iIdx] >= 420.0 THEN
        rKilnRefractoryThickness_40Point_mm[iIdx] := 35.0; (* Critical brick spalling / bare shell *)
        bShellHotSpot_Detected[iIdx] := TRUE;
    ELSIF rKilnShellTemp_40Point[iIdx] >= 380.0 THEN
        rKilnRefractoryThickness_40Point_mm[iIdx] := 75.0 + (420.0 - rKilnShellTemp_40Point[iIdx]) * 1.5;
        bShellHotSpot_Detected[iIdx] := TRUE;
    ELSIF rKilnShellTemp_40Point[iIdx] >= 320.0 THEN
        rKilnRefractoryThickness_40Point_mm[iIdx] := 135.0 + (380.0 - rKilnShellTemp_40Point[iIdx]) * 1.8;
        bShellHotSpot_Detected[iIdx] := FALSE;
    ELSIF rKilnShellTemp_40Point[iIdx] >= 220.0 THEN
        rKilnRefractoryThickness_40Point_mm[iIdx] := 200.0 + (320.0 - rKilnShellTemp_40Point[iIdx]) * 1.2;
        bShellHotSpot_Detected[iIdx] := FALSE;
    ELSE
        (* Low temperature indicates excessive clinker coating ring dam *)
        rKilnRefractoryThickness_40Point_mm[iIdx] := 320.0 + (220.0 - rKilnShellTemp_40Point[iIdx]) * 2.0;
        bShellHotSpot_Detected[iIdx] := FALSE;
    END_IF;
END_FOR;

rPeakShellTemperature_degC := rMaxShellTemp_degC;
nPeakShellSliceIndex := nMaxShellSlice;

(* Shell Cooling Fan Banks Activation *)
(* Bank 1 cools Slices 1 to 20 (Discharge, Sintering & Transition Zones) *)
bShellCoolingFanBank1_On := FALSE;
FOR iIdx := 1 TO 20 DO
    IF rKilnShellTemp_40Point[iIdx] > 340.0 THEN
        bShellCoolingFanBank1_On := TRUE;
    END_IF;
END_FOR;

(* Bank 2 cools Slices 21 to 40 (Calcining & Kiln Inlet Zones) *)
bShellCoolingFanBank2_On := FALSE;
FOR iIdx := 21 TO 40 DO
    IF rKilnShellTemp_40Point[iIdx] > 320.0 THEN
        bShellCoolingFanBank2_On := TRUE;
    END_IF;
END_FOR;

(* Critical Shell Hot-Spot Fast Fuel Trip Flag *)
IF rMaxShellTemp_degC >= rShellHotSpotTrip_degC THEN
    bAlarm_KilnShellHotSpot_HH := TRUE;
    bAlarm_Shell_HH_Latched := TRUE;
ELSIF rMaxShellTemp_degC <= (rShellHotSpotTrip_degC - 15.0) THEN
    IF bAlarmReset THEN
        bAlarm_KilnShellHotSpot_HH := FALSE;
        bAlarm_Shell_HH_Latched := FALSE;
    END_IF;
END_IF;

(* ---------------------------------------------------------------------------------------------- *)
(* 2.2 FLOATING KILN TYRE CREEP SLIP ANGLE OBSERVER                                               *)
(* ---------------------------------------------------------------------------------------------- *)
(* Tyre creep is measured via proximity sensor pulse intervals comparing shell rotation time     *)
(* to tyre circumference travel time: Delta_s = (Delta_t / T_rev) * PI * D_tyre                  *)
IF rKilnDriveSpeed_Feedback_rpm > 0.30 THEN
    IF rTyreSlipPulseInterval_Shell_s > 0.10 THEN
        rTyreSlipRaw_mm := ABS(rTyreSlipPulseInterval_Tyre_s - rTyreSlipPulseInterval_Shell_s) / 
                           rTyreSlipPulseInterval_Shell_s * 3.14159265 * rTyreDiameter_m * 1000.0;
        (* First-order lag digital filtering (Ts = 50 ms, Tau = 2.0 s) *)
        rTyreSlipFiltered_mmprev := (0.975 * rTyreSlipFiltered_mmprev) + (0.025 * rTyreSlipRaw_mm);
    END_IF;
ELSE
    rTyreSlipFiltered_mmprev := 10.5; (* Standby default nominal creep *)
END_IF;

rComputedTyreSlipAngle_mmprev := rTyreSlipFiltered_mmprev;

(* Tyre Creep Diagnostic Thresholds *)
IF rComputedTyreSlipAngle_mmprev > rTyreSlipLimitHigh_mmprev THEN
    bAlarm_TyreSlipHigh_H := TRUE;
    bAlarm_TyreSlip_H_Latched := TRUE;
ELSIF rComputedTyreSlipAngle_mmprev < rTyreSlipLimitLow_mmprev THEN
    bAlarm_TyreSlipHigh_H := TRUE; (* Low slip indicates tyre constriction / danger of kiln pinching *)
    bAlarm_TyreSlip_L_Latched := TRUE;
ELSIF (rComputedTyreSlipAngle_mmprev <= (rTyreSlipLimitHigh_mmprev - 2.0)) AND 
      (rComputedTyreSlipAngle_mmprev >= (rTyreSlipLimitLow_mmprev + 1.0)) THEN
    IF bAlarmReset THEN
        bAlarm_TyreSlipHigh_H := FALSE;
        bAlarm_TyreSlip_H_Latched := FALSE;
        bAlarm_TyreSlip_L_Latched := FALSE;
    END_IF;
END_IF;

(* ---------------------------------------------------------------------------------------------- *)
(* 2.3 DUAL 1,200 kW DRIVE MOTOR MASTER-FOLLOWER TORQUE SHARING PI CONTROLLER                    *)
(* ---------------------------------------------------------------------------------------------- *)
(* Motor 1 runs in master speed control; Motor 2 receives speed trim to equalize load torque     *)
rTorqueError_kNm := rKilnDriveMotorTorque1_kNm - rKilnDriveMotorTorque2_kNm;

(* Compute Relative Imbalance Percentage *)
IF (rKilnDriveMotorTorque1_kNm + rKilnDriveMotorTorque2_kNm) > 5.0 THEN
    rDualDriveTorqueDeviation_pct := (ABS(rTorqueError_kNm) / 
        (rKilnDriveMotorTorque1_kNm + rKilnDriveMotorTorque2_kNm)) * 100.0;
ELSE
    rDualDriveTorqueDeviation_pct := 0.0;
END_IF;

(* PI Controller with Anti-Windup Clamping *)
rTorqueIntegral_kNm_s := rTorqueIntegral_kNm_s + (rTorqueError_kNm * T_CYCLE_SEC);
IF rTorqueIntegral_kNm_s > 50.0 THEN
    rTorqueIntegral_kNm_s := 50.0;
ELSIF rTorqueIntegral_kNm_s < -50.0 THEN
    rTorqueIntegral_kNm_s := -50.0;
END_IF;

rMotor2_TorqueTrim_Output := (rTorqueKp * rTorqueError_kNm) + (rTorqueKi * rTorqueIntegral_kNm_s);
IF rMotor2_TorqueTrim_Output > 5.0 THEN
    rMotor2_TorqueTrim_Output := 5.0;
ELSIF rMotor2_TorqueTrim_Output < -5.0 THEN
    rMotor2_TorqueTrim_Output := -5.0;
END_IF;

rKilnDriveMotor2_TorqueTrim_pct := rMotor2_TorqueTrim_Output;

(* Dual-Drive Torque Imbalance Alarm Trip *)
IF rDualDriveTorqueDeviation_pct > rDualDriveTorqueMaxImbalance_pct THEN
    bAlarm_DriveTorqueImbalance_H := TRUE;
    bAlarm_Torque_H_Latched := TRUE;
ELSIF rDualDriveTorqueDeviation_pct <= (rDualDriveTorqueMaxImbalance_pct - 2.5) THEN
    IF bAlarmReset THEN
        bAlarm_DriveTorqueImbalance_H := FALSE;
        bAlarm_Torque_H_Latched := FALSE;
    END_IF;
END_IF;
"""

def generate_phase3_kinetics_softsensors():
    return """
(* ============================================================================================== *)
(* === PHASE 3: FIRST-PRINCIPLES CYBER-PHYSICAL KINETIC ESTIMATION & SOFT SENSORS ===             *)
(* ============================================================================================== *)
(* Real-time clinker free-lime (CaO_free) neural/kinetic estimator, preheater tower 5-stage       *)
(* suspension heat balance, calciner decarbonation kinetics, and burner flame momentum.           *)

(* ---------------------------------------------------------------------------------------------- *)
(* 3.1 REAL-TIME CLINKER FREE-LIME (CaO_free) SOFT SENSOR                                         *)
(* ---------------------------------------------------------------------------------------------- *)
(* Clinker free lime indicates the completeness of tricalcium silicate (C3S / Alite) formation. *)
(* High burning zone temperature and high bed torque (indicating dense nodulization and liquid     *)
(* flux melt) drive free lime down, while high feed rate and high Lime Saturation Factor drive it up.*)
rTempAccumulator := rSoftSensor_FreeLime_Base
    - (rSoftSensor_TempWeight * (rVotedBurningZoneTemp_degC - 1450.0))
    - (rSoftSensor_TorqueWeight * ((rKilnDriveMotorTorque1_kNm + rKilnDriveMotorTorque2_kNm) - 180.0))
    + (rSoftSensor_FeedWeight * (rRawMealFeedRate_tph - 400.0))
    - (rSoftSensor_NOxWeight * (rPreheaterTop_NOx_ppm - 450.0))
    + (0.045 * (rRawMealLimeSaturationFactor_LSF - 96.0))
    + (0.020 * (rRawMealSilicaModulus_SM - 2.50));

(* Physical Lower and Upper Clamping *)
IF rTempAccumulator < 0.10 THEN
    rTempAccumulator := 0.10;
ELSIF rTempAccumulator > 5.00 THEN
    rTempAccumulator := 5.00;
END_IF;

rObservedFreeLime_CaO_pct := rTempAccumulator;

(* Free-Lime Quality Window Trip Diagnostics *)
IF rObservedFreeLime_CaO_pct > rTrip_FreeLime_High_H_pct THEN
    bAlarm_FreeLimeOutOfSpec_H := TRUE;
    bAlarm_FreeLime_H_Latched := TRUE;
ELSIF rObservedFreeLime_CaO_pct < rTrip_FreeLime_Low_L_pct THEN
    bAlarm_FreeLimeOutOfSpec_H := TRUE; (* Over-burned clinker / wasted fuel & hard grindability *)
    bAlarm_FreeLime_L_Latched := TRUE;
ELSIF (rObservedFreeLime_CaO_pct <= (rTrip_FreeLime_High_H_pct - rDeadband_FreeLime_pct)) AND
      (rObservedFreeLime_CaO_pct >= (rTrip_FreeLime_Low_L_pct + rDeadband_FreeLime_pct)) THEN
    IF bAlarmReset THEN
        bAlarm_FreeLimeOutOfSpec_H := FALSE;
        bAlarm_FreeLime_H_Latched := FALSE;
        bAlarm_FreeLime_L_Latched := FALSE;
    END_IF;
END_IF;

(* ---------------------------------------------------------------------------------------------- *)
(* 3.2 PRECALCINER APPARENT DEGREE OF CALCINATION KINETICS & TOWER SUSPENSION BALANCE             *)
(* ---------------------------------------------------------------------------------------------- *)
(* Solid limestone decarbonation: CaCO3 -> CaO + CO2 in precalciner riser duct.                   *)
(* Temperature in Kelvin: T_calc_K = T_calc_degC + 273.15 *)
rTempAccumulator := rVotedCalcinerOutletTemp_degC + 273.15;
IF rTempAccumulator < 900.0 THEN
    rTempAccumulator := 900.0;
END_IF;

(* Arrhenius Reaction Velocity Rate Constant: k = k0 * exp(-Ea / (R * T)) *)
(* Pre-calculated nominal kinetic rate around 880 deg C (1153 K): k_calc approx 0.85 s^-1 *)
(* Decarbonation fraction over 3.2 s gas residence time: *)
rEstimatedDegreeOfCalcination_pct := 92.50 
    + (0.035 * (rVotedCalcinerOutletTemp_degC - 880.0))
    + (0.015 * (rTertiaryAirTemp_degC - 900.0))
    - (0.018 * (rRawMealFeedRate_tph - 400.0))
    + (0.060 * (rCalcinerCoalFeedRate_tph - 24.0));

IF rEstimatedDegreeOfCalcination_pct > 98.0 THEN
    rEstimatedDegreeOfCalcination_pct := 98.0;
ELSIF rEstimatedDegreeOfCalcination_pct < 70.0 THEN
    rEstimatedDegreeOfCalcination_pct := 70.0;
END_IF;

(* ---------------------------------------------------------------------------------------------- *)
(* 3.3 MAIN BURNER MULTI-CHANNEL FLAME MOMENTUM & AERODYNAMIC RECIRCULATION RATIO                *)
(* ---------------------------------------------------------------------------------------------- *)
(* Jet momentum G_m = m_dot_axial * v_axial + m_dot_swirl * v_swirl + m_dot_primary * v_coal      *)
(* Standard air density rho = 1.20 kg/m3; jet exit velocities 120-160 m/s *)
rFlameMomentum_N := (rMainBurnerAxialAirFlow_Nm3h * 1.20 / 3600.0 * 145.0) 
                  + (rMainBurnerSwirlAirFlow_Nm3h * 1.20 / 3600.0 * 110.0) 
                  + (rMainBurnerPrimaryAirFlow_Nm3h * 1.20 / 3600.0 * 32.0);

(* Total Thermal Fuel Power in Main Burner [MW] *)
rTempAccumulator := ((rMainBurnerCoalFeedRate_tph * rCoalLowerHeatingValue_MJkg) + 
                     (rMainBurnerRDF_FeedRate_tph * rRDF_LowerHeatingValue_MJkg)) / 3.60;

IF rTempAccumulator > 10.0 THEN
    rFlameMomentumRatio_NpMW := rFlameMomentum_N / rTempAccumulator;
ELSE
    rFlameMomentumRatio_NpMW := 1.50; (* Default baseline momentum ratio *)
END_IF;

(* Overall Specific Thermal Energy Efficiency [%] *)
(* Evaluates heat utilized in calcination + sintering vs total fuel input *)
IF (rRawMealFeedRate_tph > 50.0) AND (rTempAccumulator > 20.0) THEN
    rKilnThermalEfficiency_pct := 78.50 
        + (0.025 * (rCoolerSecondaryAirTemp_degC - 1050.0))
        + (0.015 * (rTertiaryAirTemp_degC - 900.0))
        - (0.040 * (rCycloneGasTemp_C1_degC - 310.0))
        - (0.020 * (rPeakShellTemperature_degC - 260.0));
    IF rKilnThermalEfficiency_pct > 88.0 THEN
        rKilnThermalEfficiency_pct := 88.0;
    ELSIF rKilnThermalEfficiency_pct < 65.0 THEN
        rKilnThermalEfficiency_pct := 65.0;
    END_IF;
ELSE
    rKilnThermalEfficiency_pct := 72.0;
END_IF;
"""

def generate_phase4_statespace():
    return """
(* ============================================================================================== *)
(* === PHASE 4: FIRST-PRINCIPLES CYBER-PHYSICAL STATE-SPACE ESTIMATION (Ts = 50 ms) ===            *)
(* ============================================================================================== *)
(* 8-State discrete state-space formulation: x[k+1] = A*x[k] + B*u[k] + E*d[k], y[k] = C*x + D*u. *)
(* Dynamic state correction via Luenberger observer innovations across all 8 process channels.   *)

(* ---------------------------------------------------------------------------------------------- *)
(* 4.1 DISCRETE STATE TRANSITION MATRIX A (8x8) INITIALIZATION                                    *)
(* ---------------------------------------------------------------------------------------------- *)
a_mat[1,1] := 0.9850; a_mat[1,2] := 0.0080; a_mat[1,3] := -0.0120; a_mat[1,4] := 0.0045; a_mat[1,5] := -0.0150; a_mat[1,6] := 0.0220; a_mat[1,7] := -0.0035; a_mat[1,8] := -0.0015;
a_mat[2,1] := 0.0050; a_mat[2,2] := 0.9820; a_mat[2,3] := -0.0180; a_mat[2,4] := 0.0020; a_mat[2,5] := 0.0000;  a_mat[2,6] := 0.0140; a_mat[2,7] := -0.0080; a_mat[2,8] := 0.0000;
a_mat[3,1] := 0.0010; a_mat[3,2] := 0.0035; a_mat[3,3] := 0.9450;  a_mat[3,4] := 0.0000; a_mat[3,5] := 0.0000;  a_mat[3,6] := -0.0025; a_mat[3,7] := 0.0120; a_mat[3,8] := 0.0000;
a_mat[4,1] := 0.0120; a_mat[4,2] := 0.0040; a_mat[4,3] := 0.0000;  a_mat[4,4] := 0.9780; a_mat[4,5] := -0.0240; a_mat[4,6] := 0.0065; a_mat[4,7] := 0.0000;  a_mat[4,8] := -0.0030;
a_mat[5,1] := -0.0085; a_mat[5,2] := -0.0042; a_mat[5,3] := 0.0000; a_mat[5,4] := -0.0055; a_mat[5,5] := 0.9650; a_mat[5,6] := -0.0060; a_mat[5,7] := 0.0000; a_mat[5,8] := 0.0000;
a_mat[6,1] := 0.0180; a_mat[6,2] := 0.0000; a_mat[6,3] := 0.0050;  a_mat[6,4] := 0.0030; a_mat[6,5] := 0.0000;  a_mat[6,6] := 0.9810; a_mat[6,7] := -0.0040; a_mat[6,8] := -0.0020;
a_mat[7,1] := -0.0040; a_mat[7,2] := -0.0090; a_mat[7,3] := 0.0150; a_mat[7,4] := 0.0000; a_mat[7,5] := 0.0000; a_mat[7,6] := -0.0050; a_mat[7,7] := 0.9520; a_mat[7,8] := 0.0000;
a_mat[8,1] := 0.0065; a_mat[8,2] := 0.0025; a_mat[8,3] := 0.0000;  a_mat[8,4] := 0.0015; a_mat[8,5] := 0.0000;  a_mat[8,6] := 0.0000;  a_mat[8,7] := 0.0000;  a_mat[8,8] := 0.9920;

(* ---------------------------------------------------------------------------------------------- *)
(* 4.2 DISCRETE INPUT COUPLING MATRIX B (8x8) INITIALIZATION                                      *)
(* ---------------------------------------------------------------------------------------------- *)
b_mat[1,1] := 0.3200;  b_mat[1,2] := 0.0450;  b_mat[1,3] := -0.0850; b_mat[1,4] := -0.1800; b_mat[1,5] := 0.0250;  b_mat[1,6] := 0.0350;  b_mat[1,7] := -0.0450; b_mat[1,8] := 0.0650;
b_mat[2,1] := 0.0250;  b_mat[2,2] := 0.2850;  b_mat[2,3] := -0.0450; b_mat[2,4] := -0.2200; b_mat[2,5] := 0.0450;  b_mat[2,6] := 0.0850;  b_mat[2,7] := 0.0000;  b_mat[2,8] := 0.0150;
b_mat[3,1] := -0.0080; b_mat[3,2] := -0.0150; b_mat[3,3] := 0.0050;  b_mat[3,4] := 0.0085;  b_mat[3,5] := -0.0480; b_mat[3,6] := 0.0180;  b_mat[3,7] := 0.0000;  b_mat[3,8] := -0.0120;
b_mat[4,1] := 0.1250;  b_mat[4,2] := 0.0350;  b_mat[4,3] := 0.2500;  b_mat[4,4] := 0.3800;  b_mat[4,5] := 0.0000;  b_mat[4,6] := 0.0150;  b_mat[4,7] := 0.0000;  b_mat[4,8] := 0.0250;
b_mat[5,1] := -0.0650; b_mat[5,2] := -0.0450; b_mat[5,3] := 0.0320;  b_mat[5,4] := 0.0950;  b_mat[5,5] := -0.0120; b_mat[5,6] := -0.0180; b_mat[5,7] := 0.0220;  b_mat[5,8] := -0.0350;
b_mat[6,1] := 0.0450;  b_mat[6,2] := 0.0000;  b_mat[6,3] := 0.0850;  b_mat[6,4] := 0.1400;  b_mat[6,5] := 0.0000;  b_mat[6,6] := -0.0450; b_mat[6,7] := -0.1650; b_mat[6,8] := 0.2200;
b_mat[7,1] := -0.0550; b_mat[7,2] := -0.0750; b_mat[7,3] := 0.0000;  b_mat[7,4] := 0.0150;  b_mat[7,5] := 0.0850;  b_mat[7,6] := 0.0250;  b_mat[7,7] := 0.0000;  b_mat[7,8] := 0.0450;
b_mat[8,1] := 0.0850;  b_mat[8,2] := 0.0250;  b_mat[8,3] := 0.0150;  b_mat[8,4] := 0.0000;  b_mat[8,5] := 0.0000;  b_mat[8,6] := 0.0000;  b_mat[8,7] := 0.0000;  b_mat[8,8] := 0.0000;

(* ---------------------------------------------------------------------------------------------- *)
(* 4.3 OUTPUT C (8x8) & DIRECT FEEDTHROUGH D (8x8) INITIALIZATION                                 *)
(* ---------------------------------------------------------------------------------------------- *)
FOR iIdx := 1 TO 8 DO
    FOR jIdx := 1 TO 8 DO
        IF iIdx = jIdx THEN
            c_mat[iIdx, jIdx] := 1.0;
        ELSE
            c_mat[iIdx, jIdx] := 0.0;
        END_IF;
        d_mat[iIdx, jIdx] := 0.0;
    END_FOR;
END_FOR;

(* ---------------------------------------------------------------------------------------------- *)
(* 4.4 DISTURBANCE COUPLING MATRIX E (8x4) INITIALIZATION                                         *)
(* ---------------------------------------------------------------------------------------------- *)
e_mat[1,1] := -0.1200; e_mat[1,2] := 0.0850;  e_mat[1,3] := -0.0150; e_mat[1,4] := -0.0450;
e_mat[2,1] := -0.1500; e_mat[2,2] := 0.0950;  e_mat[2,3] := -0.0220; e_mat[2,4] := -0.0120;
e_mat[3,1] := 0.0000;  e_mat[3,2] := -0.0050; e_mat[3,3] := 0.0180;  e_mat[3,4] := -0.0350;
e_mat[4,1] := 0.1800;  e_mat[4,2] := -0.0250; e_mat[4,3] := 0.0000;  e_mat[4,4] := 0.2200;
e_mat[5,1] := 0.2400;  e_mat[5,2] := -0.0650; e_mat[5,3] := 0.0080;  e_mat[5,4] := 0.0550;
e_mat[6,1] := 0.0000;  e_mat[6,2] := 0.0000;  e_mat[6,3] := -0.0350; e_mat[6,4] := -0.0850;
e_mat[7,1] := 0.0000;  e_mat[7,2] := -0.0150; e_mat[7,3] := 0.0000;  e_mat[7,4] := -0.0250;
e_mat[8,1] := 0.0350;  e_mat[8,2] := 0.0150;  e_mat[8,3] := -0.0180; e_mat[8,4] := -0.0750;

(* ---------------------------------------------------------------------------------------------- *)
(* 4.5 LUENBERGER OBSERVER GAIN VECTOR L (8x1)                                                    *)
(* ---------------------------------------------------------------------------------------------- *)
l_obs[1] := 0.1250;
l_obs[2] := 0.1180;
l_obs[3] := 0.1850;
l_obs[4] := 0.0950;
l_obs[5] := 0.0820;
l_obs[6] := 0.1050;
l_obs[7] := 0.1450;
l_obs[8] := 0.0650;

(* ---------------------------------------------------------------------------------------------- *)
(* 4.6 GATHER RECONCILED MEASUREMENTS & CURRENT ACTUATOR COMMANDS                                 *)
(* ---------------------------------------------------------------------------------------------- *)
y_meas[1] := rVotedBurningZoneTemp_degC;
y_meas[2] := rVotedCalcinerOutletTemp_degC;
y_meas[3] := rVotedKilnInletDraft_mbar;
y_meas[4] := rKilnDriveMotorTorque1_kNm + rKilnDriveMotorTorque2_kNm;
y_meas[5] := rObservedFreeLime_CaO_pct;
y_meas[6] := rCoolerSecondaryAirTemp_degC;
y_meas[7] := rVotedPreheaterTop_O2_pct;
y_meas[8] := rPeakShellTemperature_degC;

u_ctrl[1] := rMainBurnerCoalFeedRate_tph;
u_ctrl[2] := rCalcinerCoalFeedRate_tph + (rCalcinerRDF_FeedRate_tph * 0.65);
u_ctrl[3] := rKilnDriveSpeed_Feedback_rpm;
u_ctrl[4] := rRawMealFeedRate_tph;
u_ctrl[5] := rIDFanOperatingSpeed_rpm / 10.0; (* Scaled % equivalent *)
u_ctrl[6] := rTertiaryAirDamperCommand_pct;
u_ctrl[7] := rCoolerGrateSpeed_Feedback_spm;
u_ctrl[8] := rCoolerAerationFanDamper1_pct;

d_dist[1] := rRawMealLimeSaturationFactor_LSF - 96.0;
d_dist[2] := rRDF_LowerHeatingValue_MJkg - 18.0;
d_dist[3] := rCycloneGasTemp_C1_degC - 320.0;
d_dist[4] := (rKilnDriveMotorTorque1_kNm + rKilnDriveMotorTorque2_kNm) - 180.0;

(* ---------------------------------------------------------------------------------------------- *)
(* 4.7 LUENBERGER OBSERVER INNOVATION & CORRECTION                                                *)
(* x_corr[i] = x[i] + L[i] * (y_meas[i] - sum_j(C[i,j] * x[j]))                                  *)
(* ---------------------------------------------------------------------------------------------- *)
FOR iIdx := 1 TO 8 DO
    rTempAccumulator := 0.0;
    FOR jIdx := 1 TO 8 DO
        rTempAccumulator := rTempAccumulator + (c_mat[iIdx, jIdx] * x_state[jIdx]);
    END_FOR;
    (* Add direct transmission feedthrough if non-zero *)
    FOR jIdx := 1 TO 8 DO
        rTempAccumulator := rTempAccumulator + (d_mat[iIdx, jIdx] * u_ctrl[jIdx]);
    END_FOR;
    x_state[iIdx] := x_state[iIdx] + (l_obs[iIdx] * (y_meas[iIdx] - rTempAccumulator));
END_FOR;

(* ---------------------------------------------------------------------------------------------- *)
(* 4.8 EXPLICIT DISCRETE TIME STATE PROPAGATION: x[k+1] = A*x[k] + B*u[k] + E*d[k]                *)
(* ---------------------------------------------------------------------------------------------- *)
FOR iIdx := 1 TO 8 DO
    x_next[iIdx] := 0.0;
    FOR jIdx := 1 TO 8 DO
        x_next[iIdx] := x_next[iIdx] + (a_mat[iIdx, jIdx] * x_state[jIdx]);
    END_FOR;
    FOR jIdx := 1 TO 8 DO
        x_next[iIdx] := x_next[iIdx] + (b_mat[iIdx, jIdx] * u_ctrl[jIdx]);
    END_FOR;
    FOR kIdx := 1 TO 4 DO
        x_next[iIdx] := x_next[iIdx] + (e_mat[iIdx, kIdx] * d_dist[kIdx]);
    END_FOR;
END_FOR;

(* State Vector Update *)
FOR iIdx := 1 TO 8 DO
    x_state[iIdx] := x_next[iIdx];
END_FOR;
"""

def generate_phase5_mpc():
    return """
(* ============================================================================================== *)
(* === PHASE 5: RECEDING-HORIZON MPC OPTIMIZATION WITH PGD & ACTUATOR SLEW LIMITS ===             *)
(* ============================================================================================== *)
(* Multivariable quadratic objective functional optimization via unrolled Projected Gradient    *)
(* Descent (PGD) with physical box saturation constraints and dynamic slew rate limiters.         *)

(* ---------------------------------------------------------------------------------------------- *)
(* 5.1 STATE REFERENCE TRAJECTORY & PENALTY MATRICES CONFIGURATION                                *)
(* ---------------------------------------------------------------------------------------------- *)
(* Adapt reference trajectory based on whether kiln is in full production or warm-up *)
IF (nOperationalState >= 9) THEN
    x_ref[1] := 1450.0; (* Burning zone sintering bed setpoint [deg C] *)
    x_ref[2] := 880.0;  (* Precalciner riser outlet temp [deg C] *)
    x_ref[3] := -1.50;  (* Kiln inlet static draft pressure [mbar] *)
    x_ref[4] := 185.0;  (* Total drive motor operating torque [kNm] *)
    x_ref[5] := 1.15;   (* Target clinker free lime CaO [%] *)
    x_ref[6] := 1050.0; (* Cooler secondary air recovery temp [deg C] *)
    x_ref[7] := 3.20;   (* Top cyclone residual oxygen [%] *)
    x_ref[8] := 260.0;  (* Normal shell temperature baseline [deg C] *)

    u_ref[1] := 18.5;   (* Main burner coal nominal feed rate [t/h] *)
    u_ref[2] := 26.0;   (* Precalciner fuel nominal feed rate [t/h] *)
    u_ref[3] := 3.80;   (* Kiln drive nominal speed [rpm] *)
    u_ref[4] := 415.0;  (* Raw meal nominal infeed [t/h] (10,000 tpd clinker) *)
    u_ref[5] := 72.0;   (* ID fan nominal speed demand [%] *)
    u_ref[6] := 65.0;   (* Tertiary air damper nominal position [%] *)
    u_ref[7] := 14.5;   (* Cooler reciprocating grate nominal stroke rate [spm] *)
    u_ref[8] := 68.0;   (* Cooler compartment 1 aeration damper [%] *)
ELSE
    x_ref[1] := 1250.0;
    x_ref[2] := 820.0;
    x_ref[3] := -1.00;
    x_ref[4] := 120.0;
    x_ref[5] := 2.50;
    x_ref[6] := 800.0;
    x_ref[7] := 5.50;
    x_ref[8] := 210.0;

    u_ref[1] := 8.5;
    u_ref[2] := 10.0;
    u_ref[3] := 1.50;
    u_ref[4] := 100.0;
    u_ref[5] := 45.0;
    u_ref[6] := 40.0;
    u_ref[7] := 8.0;
    u_ref[8] := 40.0;
END_IF;

(* Penalty Diagonal Matrices Weights *)
q_diag[1] := 4.50;  (* Burning zone temperature tracking penalty *)
q_diag[2] := 3.80;  (* Calciner temperature tracking penalty *)
q_diag[3] := 14.50; (* Inlet draft pressure tracking penalty (blowback prevention) *)
q_diag[4] := 2.20;  (* Drive torque penalty *)
q_diag[5] := 18.50; (* Clinker free-lime quality penalty *)
q_diag[6] := 3.20;  (* Secondary air temperature penalty *)
q_diag[7] := 8.50;  (* Preheater top oxygen penalty *)
q_diag[8] := 5.50;  (* Shell hot-spot penalty *)

r_diag[1] := 1.50;  (* Main burner coal effort penalty *)
r_diag[2] := 1.20;  (* Calciner fuel effort penalty *)
r_diag[3] := 2.20;  (* Kiln drive speed effort penalty *)
r_diag[4] := 0.85;  (* Raw meal infeed effort penalty *)
r_diag[5] := 1.60;  (* ID fan speed effort penalty *)
r_diag[6] := 1.40;  (* TAD damper effort penalty *)
r_diag[7] := 1.10;  (* Grate speed effort penalty *)
r_diag[8] := 0.95;  (* Aeration damper effort penalty *)

s_diag[1] := 3.20;  (* Main burner coal slew penalty *)
s_diag[2] := 2.80;  (* Calciner fuel slew penalty *)
s_diag[3] := 4.50;  (* Kiln speed slew penalty *)
s_diag[4] := 1.80;  (* Raw meal slew penalty *)
s_diag[5] := 3.50;  (* ID fan slew penalty *)
s_diag[6] := 2.50;  (* TAD damper slew penalty *)
s_diag[7] := 2.00;  (* Grate speed slew penalty *)
s_diag[8] := 1.80;  (* Aeration damper slew penalty *)

p_diag[1] := 12.50;
p_diag[2] := 10.20;
p_diag[3] := 35.00;
p_diag[4] := 6.50;
p_diag[5] := 48.00;
p_diag[6] := 9.00;
p_diag[7] := 22.00;
p_diag[8] := 16.00;

(* Actuator Physical Box Saturation Bounds [min, max] *)
u_box_min[1] := 0.0;    u_box_max[1] := 32.0;   (* Main burner coal [t/h] *)
u_box_min[2] := 0.0;    u_box_max[2] := 45.0;   (* Calciner fuel [t/h] *)
u_box_min[3] := 0.40;   u_box_max[3] := 4.50;   (* Kiln drive speed [rpm] *)
u_box_min[4] := 0.0;    u_box_max[4] := 440.0;  (* Raw meal infeed [t/h] *)
u_box_min[5] := 15.0;   u_box_max[5] := 100.0;  (* ID fan speed [%] *)
u_box_min[6] := 10.0;   u_box_max[6] := 100.0;  (* TAD damper position [%] *)
u_box_min[7] := 4.0;    u_box_max[7] := 24.0;   (* Grate speed [strokes/min] *)
u_box_min[8] := 15.0;   u_box_max[8] := 100.0;  (* Cooler aeration fan damper [%] *)

(* Actuator Dynamic Slew Rate Limiters per PLC scan (Ts = 50 ms) *)
du_slew_max[1] := 0.025; (* Max coal slew: 0.5 t/h per second *)
du_slew_max[2] := 0.035; (* Max calciner fuel slew: 0.7 t/h per second *)
du_slew_max[3] := 0.005; (* Max kiln speed slew: 0.1 rpm per second *)
du_slew_max[4] := 0.450; (* Max meal slew: 9.0 t/h per second *)
du_slew_max[5] := 0.100; (* Max ID fan slew: 2.0 % per second *)
du_slew_max[6] := 0.075; (* Max TAD damper slew: 1.5 % per second *)
du_slew_max[7] := 0.040; (* Max grate speed slew: 0.8 spm per second *)
du_slew_max[8] := 0.125; (* Max aeration damper slew: 2.5 % per second *)

(* ---------------------------------------------------------------------------------------------- *)
(* 5.2 UNROLLED ANALYTICAL GRADIENT COMPUTATION OF QUADRATIC COST FUNCTION                       *)
(* grad_u[m] = sum_k (B[k,m] * Q[k] * (x[k] - x_ref[k])) + R[m]*(u[m] - u_ref[m]) + S[m]*(u[m]-u_prev[m]) *)
(* ---------------------------------------------------------------------------------------------- *)
FOR mIdx := 1 TO 8 DO
    grad_u[mIdx] := 0.0;
    FOR kIdx := 1 TO 8 DO
        grad_u[mIdx] := grad_u[mIdx] + (b_mat[kIdx, mIdx] * q_diag[kIdx] * (x_state[kIdx] - x_ref[kIdx]));
    END_FOR;
    grad_u[mIdx] := grad_u[mIdx] + (r_diag[mIdx] * (u_ctrl[mIdx] - u_ref[mIdx]))
                                 + (s_diag[mIdx] * (u_ctrl[mIdx] - u_prev[mIdx]));
END_FOR;

(* ---------------------------------------------------------------------------------------------- *)
(* 5.3 PROJECTED GRADIENT DESCENT STEP, SLEW LIMITING & PHYSICAL BOX SATURATION                   *)
(* ---------------------------------------------------------------------------------------------- *)
FOR mIdx := 1 TO 8 DO
    (* Gradient Descent Step: delta_u = - alpha * grad_u *)
    delta_u[mIdx] := - (rMpcAlphaStep * grad_u[mIdx]);

    (* Dynamic Slew Rate Saturation *)
    IF delta_u[mIdx] > du_slew_max[mIdx] THEN
        delta_u[mIdx] := du_slew_max[mIdx];
    ELSIF delta_u[mIdx] < -du_slew_max[mIdx] THEN
        delta_u[mIdx] := -du_slew_max[mIdx];
    END_IF;

    (* Compute Candidate Command *)
    u_tentative[mIdx] := u_ctrl[mIdx] + delta_u[mIdx];

    (* Physical Box Bounds Saturation *)
    IF u_tentative[mIdx] > u_box_max[mIdx] THEN
        u_tentative[mIdx] := u_box_max[mIdx];
    ELSIF u_tentative[mIdx] < u_box_min[mIdx] THEN
        u_tentative[mIdx] := u_box_min[mIdx];
    END_IF;
END_FOR;

(* ---------------------------------------------------------------------------------------------- *)
(* 5.4 EVALUATE TOTAL QUADRATIC COST FUNCTIONAL J                                                 *)
(* ---------------------------------------------------------------------------------------------- *)
rTotalCostFunctional := 0.0;
FOR kIdx := 1 TO 8 DO
    rTotalCostFunctional := rTotalCostFunctional + (q_diag[kIdx] * (x_state[kIdx] - x_ref[kIdx]) * (x_state[kIdx] - x_ref[kIdx]));
END_FOR;
FOR mIdx := 1 TO 8 DO
    rTotalCostFunctional := rTotalCostFunctional + (r_diag[mIdx] * (u_ctrl[mIdx] - u_ref[mIdx]) * (u_ctrl[mIdx] - u_ref[mIdx]))
                                                 + (s_diag[mIdx] * delta_u[mIdx] * delta_u[mIdx]);
END_FOR;

(* Store Actuator State for Next Scan Derivative *)
FOR mIdx := 1 TO 8 DO
    u_prev[mIdx] := u_ctrl[mIdx];
END_FOR;
"""

def generate_phase6_fsm():
    return """
(* ============================================================================================== *)
(* === PHASE 6: 12-STAGE DETERMINISTIC PRODUCTION FINITE STATE MACHINE (FSM) ===                 *)
(* ============================================================================================== *)
(* Deterministic production life cycle executing refractory dry-out, thermal expansion,          *)
(* burner ignition, feed initiation, precalciner ramp, nominal 10,000 tpd scale-up,               *)
(* alternative fuel co-firing, and fast coal shutoff abort modes.                                 *)

(* Update Stage Dwell Timer *)
rStateTimer_s := rStateTimer_s + T_CYCLE_SEC;

(* Global Safety Trip Override *)
IF (NOT bEmergencyStop) OR bAlarm_KilnShellHotSpot_HH OR bAlarm_KilnInletPositivePressure_HH OR 
   bAlarm_PreheaterCO_ExplosionRisk_HH OR bAlarm_BurningZoneOverTemp_HH THEN
    IF nOperationalState <> 12 AND nOperationalState <> 0 THEN
        IF bAlarm_KilnShellHotSpot_HH THEN
            nOperationalState := 12; (* Divert to Hot-Spot Controlled Fast Abort *)
            rStateTimer_s := 0.0;
        ELSE
            nOperationalState := 0;  (* Immediate Lockout Trip *)
            rStateTimer_s := 0.0;
        END_IF;
    END_IF;
END_IF;

CASE nOperationalState OF

    0: (* STATE 0: LOCKOUT / EMERGENCY SHUTDOWN *)
        bSystemReady := FALSE;
        bProductionActive := FALSE;
        bEmergencyTripActive := TRUE;
        nKilnOperationalState := 0;

        (* Safe Actuator Parking *)
        bEmergencyCoalCutoffValve := FALSE; (* Fast-Acting Coal Valve Closed *)
        rMainBurnerCoalCommand_tph := 0.0;
        rMainBurnerRDF_Command_tph := 0.0;
        rCalcinerCoalCommand_tph := 0.0;
        rCalcinerRDF_Command_tph := 0.0;
        rRawMealFeederCommand_tph := 0.0;
        rKilnDriveSpeedCommand_rpm := 0.20; (* Emergency slow barring speed to prevent shell sag *)
        rIDFanSpeedCommand_pct := 25.0;     (* Minimum keep-alive sweep draft *)
        rTertiaryAirDamperCommand_pct := 15.0;
        rCoolerGrateSpeedCommand_spm := 0.0;
        rCoolerAerationFanDamper1_pct := 20.0;
        rCoolerAerationFanDamper2_pct := 15.0;
        rCoolerAerationFanDamper3_pct := 10.0;

        (* Permissive to Clear State 0 *)
        IF bSystemEnable AND bEmergencyStop AND NOT bAlarm_KilnShellHotSpot_HH AND 
           NOT bAlarm_KilnInletPositivePressure_HH AND NOT bAlarm_PreheaterCO_ExplosionRisk_HH AND 
           bAlarmReset THEN
            bEmergencyTripActive := FALSE;
            nOperationalState := 1; (* Advance to Pre-Purge & System Check *)
            rStateTimer_s := 0.0;
        END_IF;

    1: (* STATE 1: PRE_PURGE_AND_CHECK *)
        bSystemReady := FALSE;
        bProductionActive := FALSE;
        bEmergencyTripActive := FALSE;
        nKilnOperationalState := 1;

        bEmergencyCoalCutoffValve := FALSE;
        rMainBurnerCoalCommand_tph := 0.0;
        rMainBurnerRDF_Command_tph := 0.0;
        rCalcinerCoalCommand_tph := 0.0;
        rCalcinerRDF_Command_tph := 0.0;
        rRawMealFeederCommand_tph := 0.0;
        rKilnDriveSpeedCommand_rpm := 0.30;
        rIDFanSpeedCommand_pct := 40.0; (* Pre-purge flow per NFPA 85 *)
        rTertiaryAirDamperCommand_pct := 30.0;
        rCoolerGrateSpeedCommand_spm := 0.0;
        rCoolerAerationFanDamper1_pct := 30.0;

        (* Advance when purge time elapsed and CO analyzer is safe *)
        IF (rStateTimer_s >= rStagePrePurgeDwell_s) AND (rPreheaterTop_CO_ppm < 500.0) AND 
           (rVotedKilnInletDraft_mbar < -0.80) THEN
            nOperationalState := 2; (* Advance to Refractory Dry-Out *)
            rStateTimer_s := 0.0;
        END_IF;

    2: (* STATE 2: REFRACTORY_DRYOUT_CURING *)
        bSystemReady := FALSE;
        bProductionActive := FALSE;
        nKilnOperationalState := 2;

        (* Low-fire curing curve with auxiliary burner *)
        bEmergencyCoalCutoffValve := FALSE;
        rMainBurnerCoalCommand_tph := 0.0;
        rMainBurnerRDF_Command_tph := 0.0;
        rCalcinerCoalCommand_tph := 0.0;
        rCalcinerRDF_Command_tph := 0.0;
        rRawMealFeederCommand_tph := 0.0;
        rKilnDriveSpeedCommand_rpm := 0.40;
        rIDFanSpeedCommand_pct := 35.0;
        rTertiaryAirDamperCommand_pct := 25.0;
        rCoolerGrateSpeedCommand_spm := 0.0;
        rCoolerAerationFanDamper1_pct := 25.0;

        IF (rStateTimer_s >= rStageRefractoryCureDwell_s) AND (rVotedBurningZoneTemp_degC >= 550.0) THEN
            nOperationalState := 3; (* Advance to Tower Expansion & Barring *)
            rStateTimer_s := 0.0;
        END_IF;

    3: (* STATE 3: TOWER_EXPANSION_BARRING *)
        bSystemReady := FALSE;
        bProductionActive := FALSE;
        nKilnOperationalState := 3;

        rKilnDriveSpeedCommand_rpm := 0.60;
        rIDFanSpeedCommand_pct := 42.0;
        rTertiaryAirDamperCommand_pct := 35.0;

        IF (rStateTimer_s >= rStageTowerExpansionDwell_s) AND (rCycloneGasTemp_C1_degC >= 180.0) THEN
            nOperationalState := 4; (* Advance to ID Fan Draft Balancing *)
            rStateTimer_s := 0.0;
        END_IF;

    4: (* STATE 4: ID_FAN_DRAFT_BALANCING *)
        bSystemReady := FALSE;
        bProductionActive := FALSE;
        nKilnOperationalState := 4;

        rKilnDriveSpeedCommand_rpm := 0.80;
        rIDFanSpeedCommand_pct := 50.0;
        rTertiaryAirDamperCommand_pct := 40.0;
        rCoolerAerationFanDamper1_pct := 35.0;

        IF (rStateTimer_s >= rStageIDFanBalanceDwell_s) AND (rVotedKilnInletDraft_mbar <= -1.20) THEN
            nOperationalState := 5; (* Advance to Main Burner Coal Ignition *)
            rStateTimer_s := 0.0;
        END_IF;

    5: (* STATE 5: MAIN_BURNER_COAL_IGNITION *)
        bSystemReady := FALSE;
        bProductionActive := FALSE;
        nKilnOperationalState := 5;

        (* Open Safety Cutoff Valve and light pulverized coal *)
        bEmergencyCoalCutoffValve := TRUE;
        rMainBurnerCoalCommand_tph := 4.50;
        rMainBurnerRDF_Command_tph := 0.0;
        rMainBurnerPrimaryAirFan_pct := 55.0;
        rMainBurnerSwirlDamper_pct := 45.0;
        rKilnDriveSpeedCommand_rpm := 1.00;
        rIDFanSpeedCommand_pct := 52.0;

        IF (rStateTimer_s >= rStageBurnerIgnitionDwell_s) AND (rVotedBurningZoneTemp_degC >= 850.0) THEN
            nOperationalState := 6; (* Advance to Burning Zone Sintering Heatup *)
            rStateTimer_s := 0.0;
        END_IF;

    6: (* STATE 6: BURNING_ZONE_HEATUP *)
        bSystemReady := FALSE;
        bProductionActive := FALSE;
        nKilnOperationalState := 6;

        bEmergencyCoalCutoffValve := TRUE;
        rMainBurnerCoalCommand_tph := 8.50;
        rMainBurnerPrimaryAirFan_pct := 65.0;
        rMainBurnerSwirlDamper_pct := 50.0;
        rKilnDriveSpeedCommand_rpm := 1.40;
        rIDFanSpeedCommand_pct := 55.0;
        rTertiaryAirDamperCommand_pct := 45.0;
        rCoolerAerationFanDamper1_pct := 40.0;

        IF (rStateTimer_s >= rStageSinteringHeatupDwell_s) AND (rVotedBurningZoneTemp_degC >= 1250.0) AND 
           (rVotedCalcinerOutletTemp_degC >= 720.0) THEN
            nOperationalState := 7; (* Advance to Raw Meal Feed Initiation *)
            rStateTimer_s := 0.0;
        END_IF;

    7: (* STATE 7: RAW_MEAL_FEED_INITIATION *)
        bSystemReady := FALSE;
        bProductionActive := TRUE;
        nKilnOperationalState := 7;

        (* Feed initial minimum meal into cyclone string (50 t/h) *)
        rRawMealFeederCommand_tph := 50.0;
        rMainBurnerCoalCommand_tph := 9.50;
        rKilnDriveSpeedCommand_rpm := 1.60;
        rIDFanSpeedCommand_pct := 58.0;
        rTertiaryAirDamperCommand_pct := 50.0;
        rCoolerGrateSpeedCommand_spm := 6.0;

        IF (rStateTimer_s >= rStageMealFeedInitiationDwell_s) AND (rCycloneGasTemp_C5_degC >= 650.0) THEN
            nOperationalState := 8; (* Advance to Calciner Burner Ignition *)
            rStateTimer_s := 0.0;
        END_IF;

    8: (* STATE 8: CALCINER_BURNER_IGNITION *)
        bSystemReady := FALSE;
        bProductionActive := TRUE;
        nKilnOperationalState := 8;

        (* Fire Calciner Solid Fuel *)
        rCalcinerCoalCommand_tph := 6.50;
        rRawMealFeederCommand_tph := 90.0;
        rMainBurnerCoalCommand_tph := 11.00;
        rKilnDriveSpeedCommand_rpm := 2.00;
        rIDFanSpeedCommand_pct := 62.0;
        rTertiaryAirDamperCommand_pct := 55.0;
        rCoolerGrateSpeedCommand_spm := 8.0;

        IF (rStateTimer_s >= rStageCalcinerIgnitionDwell_s) AND (rVotedCalcinerOutletTemp_degC >= 850.0) AND 
           (rEstimatedDegreeOfCalcination_pct >= 88.0) THEN
            nOperationalState := 9; (* Advance to Production Feed Scale-Up *)
            rStateTimer_s := 0.0;
        END_IF;

    9: (* STATE 9: PRODUCTION_FEED_SCALEUP *)
        bSystemReady := TRUE;
        bProductionActive := TRUE;
        nKilnOperationalState := 9;

        (* Coordinated Scale-Up toward 10,000 tpd Clinker (415 t/h meal) via MPC tentative commands *)
        bEmergencyCoalCutoffValve := TRUE;
        rRawMealFeederCommand_tph := u_tentative[4];
        rMainBurnerCoalCommand_tph := u_tentative[1];
        rCalcinerCoalCommand_tph := u_tentative[2];
        rKilnDriveSpeedCommand_rpm := u_tentative[3];
        rIDFanSpeedCommand_pct := u_tentative[5];
        rTertiaryAirDamperCommand_pct := u_tentative[6];
        rCoolerGrateSpeedCommand_spm := u_tentative[7];
        rCoolerAerationFanDamper1_pct := u_tentative[8];

        IF (rStateTimer_s >= rStageProductionScaleupDwell_s) AND (rRawMealFeedRate_tph >= 360.0) AND 
           (rVotedBurningZoneTemp_degC >= 1420.0) THEN
            nOperationalState := 10; (* Advance to Clinker Cooler Bed Synchronization *)
            rStateTimer_s := 0.0;
        END_IF;

    10: (* STATE 10: COOLER_AERATION_SYNC *)
        bSystemReady := TRUE;
        bProductionActive := TRUE;
        nKilnOperationalState := 10;

        (* Execute MPC Commands *)
        rRawMealFeederCommand_tph := u_tentative[4];
        rMainBurnerCoalCommand_tph := u_tentative[1];
        rCalcinerCoalCommand_tph := u_tentative[2];
        rKilnDriveSpeedCommand_rpm := u_tentative[3];
        rIDFanSpeedCommand_pct := u_tentative[5];
        rTertiaryAirDamperCommand_pct := u_tentative[6];
        rCoolerGrateSpeedCommand_spm := u_tentative[7];
        rCoolerAerationFanDamper1_pct := u_tentative[8];

        IF (rStateTimer_s >= rStageCoolerSyncDwell_s) AND (rCoolerSecondaryAirTemp_degC >= 1000.0) AND 
           (rVotedCoolerUndergrate_PT1_mbar >= 45.0) THEN
            nOperationalState := 11; (* Advance to Alternative Fuel RDF Co-Firing *)
            rStateTimer_s := 0.0;
        END_IF;

    11: (* STATE 11: ALTERNATIVE_FUEL_RDF_COFIRE *)
        bSystemReady := TRUE;
        bProductionActive := TRUE;
        nKilnOperationalState := 11;

        (* Full Commercial Steady-State Production with 40-50% Thermal Substitution Rate *)
        bEmergencyCoalCutoffValve := TRUE;
        rRawMealFeederCommand_tph := u_tentative[4];
        rMainBurnerCoalCommand_tph := u_tentative[1];
        rMainBurnerRDF_Command_tph := 3.80;  (* Solid alternative fuel injection *)
        rCalcinerCoalCommand_tph := u_tentative[2] * 0.65;
        rCalcinerRDF_Command_tph := 12.50;   (* Calciner RDF fluff injection *)
        rKilnDriveSpeedCommand_rpm := u_tentative[3];
        rIDFanSpeedCommand_pct := u_tentative[5];
        rTertiaryAirDamperCommand_pct := u_tentative[6];
        rCoolerGrateSpeedCommand_spm := u_tentative[7];
        rCoolerAerationFanDamper1_pct := u_tentative[8];

        (* Remain in steady production unless command changed or trip *)
        IF NOT bKilnProductionRunCmd THEN
            nOperationalState := 1; (* Orderly rampdown to pre-purge *)
            rStateTimer_s := 0.0;
        END_IF;

    12: (* STATE 12: HOTSPOT_RING_FAST_ABORT *)
        bSystemReady := FALSE;
        bProductionActive := FALSE;
        bEmergencyTripActive := TRUE;
        nKilnOperationalState := 12;

        (* Fast Fuel Cutoff & Emergency Shell Preservation *)
        bEmergencyCoalCutoffValve := FALSE;
        rMainBurnerCoalCommand_tph := 0.0;
        rMainBurnerRDF_Command_tph := 0.0;
        rCalcinerCoalCommand_tph := 0.0;
        rCalcinerRDF_Command_tph := 0.0;
        rRawMealFeederCommand_tph := 0.0;
        rKilnDriveSpeedCommand_rpm := 0.50; (* Keep rotating to prevent plastic thermal bending *)
        rIDFanSpeedCommand_pct := 30.0;
        rTertiaryAirDamperCommand_pct := 20.0;
        bShellCoolingFanBank1_On := TRUE;  (* Force maximum shell cooling *)
        bShellCoolingFanBank2_On := TRUE;

        IF (rStateTimer_s >= rStageAbortCoolingDwell_s) AND (rMaxShellTemp_degC <= 320.0) AND bAlarmReset THEN
            bEmergencyTripActive := FALSE;
            nOperationalState := 0; (* Return to safe parked lockout *)
            rStateTimer_s := 0.0;
        END_IF;

END_CASE;
"""

def generate_phase7_cooler_cascade():
    return """
(* ============================================================================================== *)
(* === PHASE 7: CLINKER COOLER RECIPROCATING HYDRAULIC GRATE & AERATION CASCADE ===               *)
(* ============================================================================================== *)
(* Hydraulic reciprocating step grate stroke speed regulation, under-grate aeration compartment   *)
(* pressure stabilization, and secondary/tertiary air recuperation thermal optimization.          *)

(* ---------------------------------------------------------------------------------------------- *)
(* 7.1 HYDRAULIC RECIPROCATING GRATE SPEED BED PRESSURE CASCADE                                   *)
(* ---------------------------------------------------------------------------------------------- *)
(* If in production states (9..11), closed-loop trim around MPC command *)
IF (nOperationalState >= 9) AND (nOperationalState <= 11) THEN
    (* Compartment 1 Under-Grate Aeration Pressure Trim (Target: 52.0 mbar) *)
    (* High pressure = thick clinker bed -> increase grate stroke frequency *)
    (* Low pressure = thin clinker bed -> reduce grate stroke frequency to prevent red river *)
    rTempAccumulator := u_tentative[7] + (0.35 * (rVotedCoolerUndergrate_PT1_mbar - 52.0));

    (* Clinker Discharge Temperature Overheat Protection *)
    IF rCoolerClinkerDischargeTemp_degC > 120.0 THEN
        rTempAccumulator := rTempAccumulator + (0.05 * (rCoolerClinkerDischargeTemp_degC - 120.0));
    END_IF;

    (* Bound Grate Stroke Rate *)
    IF rTempAccumulator > 24.0 THEN
        rTempAccumulator := 24.0;
    ELSIF rTempAccumulator < 4.0 THEN
        rTempAccumulator := 4.0;
    END_IF;

    rCoolerGrateSpeedCommand_spm := rTempAccumulator;
END_IF;

(* ---------------------------------------------------------------------------------------------- *)
(* 7.2 UNDER-GRATE COMPARTMENTS 1, 2, 3 AERATION DAMPER MODULATION                                *)
(* ---------------------------------------------------------------------------------------------- *)
IF (nOperationalState >= 9) AND (nOperationalState <= 11) THEN
    (* Compartment 1 Aeration Damper: Quenching & Secondary Air Recovery into Kiln Hood *)
    rTempAccumulator := u_tentative[8] + (0.08 * (1050.0 - rCoolerSecondaryAirTemp_degC));
    IF rTempAccumulator > 100.0 THEN rTempAccumulator := 100.0; ELSIF rTempAccumulator < 20.0 THEN rTempAccumulator := 20.0; END_IF;
    rCoolerAerationFanDamper1_pct := rTempAccumulator;

    (* Compartment 2 Aeration Damper: Tertiary Air Recovery into Precalciner Duct *)
    rTempAccumulator := 60.0 + (0.06 * (900.0 - rTertiaryAirTemp_degC));
    IF rTempAccumulator > 100.0 THEN rTempAccumulator := 100.0; ELSIF rTempAccumulator < 20.0 THEN rTempAccumulator := 20.0; END_IF;
    rCoolerAerationFanDamper2_pct := rTempAccumulator;

    (* Compartment 3 Aeration Damper: Final Cooling Zone *)
    rTempAccumulator := 55.0 + (0.12 * (rCoolerClinkerDischargeTemp_degC - 90.0));
    IF rTempAccumulator > 100.0 THEN rTempAccumulator := 100.0; ELSIF rTempAccumulator < 15.0 THEN rTempAccumulator := 15.0; END_IF;
    rCoolerAerationFanDamper3_pct := rTempAccumulator;
END_IF;
"""

def generate_phase8_alarms():
    return """
(* ============================================================================================== *)
(* === PHASE 8: ISA-18.2 MULTI-TIER ALARMS & BIT-PACKED 32-BIT STATUS WORDS ===                   *)
(* ============================================================================================== *)
(* Multi-tiered High-High, High, Low, Low-Low alarm trip detection with clearance deadband       *)
(* hysteresis, latching behavior, and bitfield packing into 32-bit status and diagnostic words.  *)

(* ---------------------------------------------------------------------------------------------- *)
(* 8.1 BURNING ZONE TEMPERATURE ALARMS                                                            *)
(* ---------------------------------------------------------------------------------------------- *)
(* HH Trip: 1520 deg C *)
IF rVotedBurningZoneTemp_degC >= rTrip_BZ_OverTemp_HH_degC THEN
    bAlarm_BurningZoneOverTemp_HH := TRUE;
    bAlarm_BZ_HH_Latched := TRUE;
ELSIF rVotedBurningZoneTemp_degC <= (rTrip_BZ_OverTemp_HH_degC - rDeadband_BZ_degC) THEN
    IF bAlarmReset THEN
        bAlarm_BurningZoneOverTemp_HH := FALSE;
        bAlarm_BZ_HH_Latched := FALSE;
    END_IF;
END_IF;

(* H Warning: 1480 deg C *)
IF rVotedBurningZoneTemp_degC >= rTrip_BZ_OverTemp_H_degC THEN
    bAlarm_BZ_H_Latched := TRUE;
ELSIF rVotedBurningZoneTemp_degC <= (rTrip_BZ_OverTemp_H_degC - rDeadband_BZ_degC) THEN
    bAlarm_BZ_H_Latched := FALSE;
END_IF;

(* L Warning: 1390 deg C *)
IF rVotedBurningZoneTemp_degC <= rTrip_BZ_UnderTemp_L_degC THEN
    bAlarm_BZ_L_Latched := TRUE;
ELSIF rVotedBurningZoneTemp_degC >= (rTrip_BZ_UnderTemp_L_degC + rDeadband_BZ_degC) THEN
    bAlarm_BZ_L_Latched := FALSE;
END_IF;

(* LL Trip: 1350 deg C (Freeze-up / Ring collapse hazard) *)
IF rVotedBurningZoneTemp_degC <= rTrip_BZ_UnderTemp_LL_degC THEN
    bAlarm_BZ_LL_Latched := TRUE;
ELSIF rVotedBurningZoneTemp_degC >= (rTrip_BZ_UnderTemp_LL_degC + rDeadband_BZ_degC) THEN
    IF bAlarmReset THEN
        bAlarm_BZ_LL_Latched := FALSE;
    END_IF;
END_IF;

(* ---------------------------------------------------------------------------------------------- *)
(* 8.2 KILN INLET STATIC DRAFT PRESSURE ALARMS                                                    *)
(* ---------------------------------------------------------------------------------------------- *)
(* HH Trip: +0.50 mbar (Dangerous Positive Blowback Hazard per NFPA 85) *)
IF rVotedKilnInletDraft_mbar >= rTrip_InletDraft_Positive_HH_mbar THEN
    bAlarm_KilnInletPositivePressure_HH := TRUE;
    bAlarm_InletDraft_HH_Latched := TRUE;
ELSIF rVotedKilnInletDraft_mbar <= (rTrip_InletDraft_Positive_HH_mbar - rDeadband_Draft_mbar) THEN
    IF bAlarmReset THEN
        bAlarm_KilnInletPositivePressure_HH := FALSE;
        bAlarm_InletDraft_HH_Latched := FALSE;
    END_IF;
END_IF;

(* H Warning: -0.20 mbar (Inadequate Draft) *)
IF rVotedKilnInletDraft_mbar >= rTrip_InletDraft_High_H_mbar THEN
    bAlarm_InletDraft_H_Latched := TRUE;
ELSIF rVotedKilnInletDraft_mbar <= (rTrip_InletDraft_High_H_mbar - rDeadband_Draft_mbar) THEN
    bAlarm_InletDraft_H_Latched := FALSE;
END_IF;

(* L Warning: -2.80 mbar *)
IF rVotedKilnInletDraft_mbar <= rTrip_InletDraft_Low_L_mbar THEN
    bAlarm_InletDraft_L_Latched := TRUE;
ELSIF rVotedKilnInletDraft_mbar >= (rTrip_InletDraft_Low_L_mbar + rDeadband_Draft_mbar) THEN
    bAlarm_InletDraft_L_Latched := FALSE;
END_IF;

(* LL Trip: -3.80 mbar (Excessive Suction / Cold Ingress) *)
IF rVotedKilnInletDraft_mbar <= rTrip_InletDraft_Deep_LL_mbar THEN
    bAlarm_InletDraft_LL_Latched := TRUE;
ELSIF rVotedKilnInletDraft_mbar >= (rTrip_InletDraft_Deep_LL_mbar + rDeadband_Draft_mbar) THEN
    IF bAlarmReset THEN
        bAlarm_InletDraft_LL_Latched := FALSE;
    END_IF;
END_IF;

(* ---------------------------------------------------------------------------------------------- *)
(* 8.3 PREHEATER TOP CO EXPLOSION RISK ALARMS                                                     *)
(* ---------------------------------------------------------------------------------------------- *)
(* HH Trip: 25,000 ppm (2.5% CO Deflagration / Explosion Interlock) *)
IF rPreheaterTop_CO_ppm >= rTrip_Preheater_CO_Explosion_HH_ppm THEN
    bAlarm_PreheaterCO_ExplosionRisk_HH := TRUE;
    bAlarm_PreheaterCO_HH_Latched := TRUE;
ELSIF rPreheaterTop_CO_ppm <= (rTrip_Preheater_CO_Explosion_HH_ppm - rDeadband_CO_ppm) THEN
    IF bAlarmReset THEN
        bAlarm_PreheaterCO_ExplosionRisk_HH := FALSE;
        bAlarm_PreheaterCO_HH_Latched := FALSE;
    END_IF;
END_IF;

(* H Warning: 12,000 ppm (1.2% CO High Incomplete Combustion) *)
IF rPreheaterTop_CO_ppm >= rTrip_Preheater_CO_High_H_ppm THEN
    bAlarm_PreheaterCO_H_Latched := TRUE;
ELSIF rPreheaterTop_CO_ppm <= (rTrip_Preheater_CO_High_H_ppm - rDeadband_CO_ppm) THEN
    bAlarm_PreheaterCO_H_Latched := FALSE;
END_IF;

(* ---------------------------------------------------------------------------------------------- *)
(* 8.4 PRECALCINER RISER TEMPERATURE ALARMS                                                       *)
(* ---------------------------------------------------------------------------------------------- *)
(* HH Trip: 950 deg C *)
IF rVotedCalcinerOutletTemp_degC >= rTrip_Calciner_OverTemp_HH_degC THEN
    bAlarm_Calciner_HH_Latched := TRUE;
ELSIF rVotedCalcinerOutletTemp_degC <= (rTrip_Calciner_OverTemp_HH_degC - rDeadband_Calciner_degC) THEN
    IF bAlarmReset THEN
        bAlarm_Calciner_HH_Latched := FALSE;
    END_IF;
END_IF;

(* H Warning: 915 deg C *)
IF rVotedCalcinerOutletTemp_degC >= rTrip_Calciner_High_H_degC THEN
    bAlarm_Calciner_H_Latched := TRUE;
ELSIF rVotedCalcinerOutletTemp_degC <= (rTrip_Calciner_High_H_degC - rDeadband_Calciner_degC) THEN
    bAlarm_Calciner_H_Latched := FALSE;
END_IF;

(* L Warning: 850 deg C *)
IF rVotedCalcinerOutletTemp_degC <= rTrip_Calciner_Low_L_degC THEN
    bAlarm_Calciner_L_Latched := TRUE;
ELSIF rVotedCalcinerOutletTemp_degC >= (rTrip_Calciner_Low_L_degC + rDeadband_Calciner_degC) THEN
    bAlarm_Calciner_L_Latched := FALSE;
END_IF;

(* LL Trip: 815 deg C (Calciner Flame Quench / Incomplete Decarbonation) *)
IF rVotedCalcinerOutletTemp_degC <= rTrip_Calciner_UnderTemp_LL_degC THEN
    bAlarm_CalcinerUnderTemp_LL := TRUE;
    bAlarm_Calciner_LL_Latched := TRUE;
ELSIF rVotedCalcinerOutletTemp_degC >= (rTrip_Calciner_UnderTemp_LL_degC + rDeadband_Calciner_degC) THEN
    IF bAlarmReset THEN
        bAlarm_CalcinerUnderTemp_LL := FALSE;
        bAlarm_Calciner_LL_Latched := FALSE;
    END_IF;
END_IF;

(* ---------------------------------------------------------------------------------------------- *)
(* 8.5 BITFIELD PACKING INTO 32-BIT STATUS & DIAGNOSTIC WORDS                                     *)
(* ---------------------------------------------------------------------------------------------- *)
(* dwKilnStatusWord: Machine Operational States and Mode Flags *)
dwKilnStatusWord := 16#0000_0000;
IF bSystemEnable THEN                       dwKilnStatusWord := dwKilnStatusWord OR 16#0000_0001; END_IF;
IF bKilnProductionRunCmd THEN               dwKilnStatusWord := dwKilnStatusWord OR 16#0000_0002; END_IF;
IF bProductionActive THEN                   dwKilnStatusWord := dwKilnStatusWord OR 16#0000_0004; END_IF;
IF bSystemReady THEN                        dwKilnStatusWord := dwKilnStatusWord OR 16#0000_0008; END_IF;
IF bEmergencyTripActive THEN                dwKilnStatusWord := dwKilnStatusWord OR 16#0000_0010; END_IF;
IF bEmergencyCoalCutoffValve THEN           dwKilnStatusWord := dwKilnStatusWord OR 16#0000_0020; END_IF;
IF bShellCoolingFanBank1_On THEN            dwKilnStatusWord := dwKilnStatusWord OR 16#0000_0040; END_IF;
IF bShellCoolingFanBank2_On THEN            dwKilnStatusWord := dwKilnStatusWord OR 16#0000_0080; END_IF;
(* State Code in bits 8..15 *)
dwKilnStatusWord := dwKilnStatusWord OR SHL(INT_TO_DWORD(nOperationalState), 8);
IF (nDraft_DegradedMode < 3) THEN           dwKilnStatusWord := dwKilnStatusWord OR 16#0001_0000; END_IF;
IF (nBZ_DegradedMode < 3) THEN              dwKilnStatusWord := dwKilnStatusWord OR 16#0002_0000; END_IF;
IF (nCalc_DegradedMode < 3) THEN            dwKilnStatusWord := dwKilnStatusWord OR 16#0004_0000; END_IF;
IF (nO2_DegradedMode < 3) THEN              dwKilnStatusWord := dwKilnStatusWord OR 16#0008_0000; END_IF;
IF (nCool1_DegradedMode < 3) THEN           dwKilnStatusWord := dwKilnStatusWord OR 16#0010_0000; END_IF;
IF (rEstimatedDegreeOfCalcination_pct >= 90.0) THEN dwKilnStatusWord := dwKilnStatusWord OR 16#0020_0000; END_IF;
IF (rObservedFreeLime_CaO_pct <= 1.50) AND (rObservedFreeLime_CaO_pct >= 0.80) THEN
    dwKilnStatusWord := dwKilnStatusWord OR 16#0040_0000;
END_IF;

(* dwKilnDiagnosticWord: Hardware Health & ISA-18.2 Latch Alarms *)
dwKilnDiagnosticWord := 16#0000_0000;
IF bAlarm_BurningZoneOverTemp_HH THEN       dwKilnDiagnosticWord := dwKilnDiagnosticWord OR 16#0000_0001; END_IF;
IF bAlarm_BZ_H_Latched THEN                 dwKilnDiagnosticWord := dwKilnDiagnosticWord OR 16#0000_0002; END_IF;
IF bAlarm_BZ_L_Latched THEN                 dwKilnDiagnosticWord := dwKilnDiagnosticWord OR 16#0000_0004; END_IF;
IF bAlarm_BZ_LL_Latched THEN                dwKilnDiagnosticWord := dwKilnDiagnosticWord OR 16#0000_0008; END_IF;
IF bAlarm_KilnInletPositivePressure_HH THEN dwKilnDiagnosticWord := dwKilnDiagnosticWord OR 16#0000_0010; END_IF;
IF bAlarm_InletDraft_H_Latched THEN         dwKilnDiagnosticWord := dwKilnDiagnosticWord OR 16#0000_0020; END_IF;
IF bAlarm_InletDraft_L_Latched THEN         dwKilnDiagnosticWord := dwKilnDiagnosticWord OR 16#0000_0040; END_IF;
IF bAlarm_InletDraft_LL_Latched THEN        dwKilnDiagnosticWord := dwKilnDiagnosticWord OR 16#0000_0080; END_IF;
IF bAlarm_KilnShellHotSpot_HH THEN          dwKilnDiagnosticWord := dwKilnDiagnosticWord OR 16#0000_0100; END_IF;
IF bAlarm_Shell_H_Latched THEN              dwKilnDiagnosticWord := dwKilnDiagnosticWord OR 16#0000_0200; END_IF;
IF bAlarm_DriveTorqueImbalance_H THEN       dwKilnDiagnosticWord := dwKilnDiagnosticWord OR 16#0000_0400; END_IF;
IF bAlarm_TyreSlipHigh_H THEN               dwKilnDiagnosticWord := dwKilnDiagnosticWord OR 16#0000_0800; END_IF;
IF bAlarm_FreeLimeOutOfSpec_H THEN          dwKilnDiagnosticWord := dwKilnDiagnosticWord OR 16#0000_1000; END_IF;
IF NOT bDraft_ChA_Valid THEN                dwKilnDiagnosticWord := dwKilnDiagnosticWord OR 16#0001_0000; END_IF;
IF NOT bDraft_ChB_Valid THEN                dwKilnDiagnosticWord := dwKilnDiagnosticWord OR 16#0002_0000; END_IF;
IF NOT bDraft_ChC_Valid THEN                dwKilnDiagnosticWord := dwKilnDiagnosticWord OR 16#0004_0000; END_IF;
IF NOT bBZ_ChA_Valid THEN                   dwKilnDiagnosticWord := dwKilnDiagnosticWord OR 16#0010_0000; END_IF;
IF NOT bBZ_ChB_Valid THEN                   dwKilnDiagnosticWord := dwKilnDiagnosticWord OR 16#0020_0000; END_IF;
IF NOT bBZ_ChC_Valid THEN                   dwKilnDiagnosticWord := dwKilnDiagnosticWord OR 16#0040_0000; END_IF;

(* dwPreheaterStatusWord: Cyclone Tower & Precalciner System Status *)
dwPreheaterStatusWord := 16#0000_0000;
IF bAlarm_PreheaterCO_ExplosionRisk_HH THEN dwPreheaterStatusWord := dwPreheaterStatusWord OR 16#0000_0001; END_IF;
IF bAlarm_PreheaterCO_H_Latched THEN        dwPreheaterStatusWord := dwPreheaterStatusWord OR 16#0000_0002; END_IF;
IF bAlarm_Calciner_HH_Latched THEN          dwPreheaterStatusWord := dwPreheaterStatusWord OR 16#0000_0004; END_IF;
IF bAlarm_Calciner_H_Latched THEN           dwPreheaterStatusWord := dwPreheaterStatusWord OR 16#0000_0008; END_IF;
IF bAlarm_Calciner_L_Latched THEN           dwPreheaterStatusWord := dwPreheaterStatusWord OR 16#0000_0010; END_IF;
IF bAlarm_CalcinerUnderTemp_LL THEN         dwPreheaterStatusWord := dwPreheaterStatusWord OR 16#0000_0020; END_IF;
IF NOT bCalc_ChA_Valid THEN                 dwPreheaterStatusWord := dwPreheaterStatusWord OR 16#0000_0100; END_IF;
IF NOT bCalc_ChB_Valid THEN                 dwPreheaterStatusWord := dwPreheaterStatusWord OR 16#0000_0200; END_IF;
IF NOT bCalc_ChC_Valid THEN                 dwPreheaterStatusWord := dwPreheaterStatusWord OR 16#0000_0400; END_IF;
IF NOT bO2_ChA_Valid THEN                   dwPreheaterStatusWord := dwPreheaterStatusWord OR 16#0000_1000; END_IF;
IF NOT bO2_ChB_Valid THEN                   dwPreheaterStatusWord := dwPreheaterStatusWord OR 16#0000_2000; END_IF;
IF NOT bO2_ChC_Valid THEN                   dwPreheaterStatusWord := dwPreheaterStatusWord OR 16#0000_4000; END_IF;

(* dwCoolerStatusWord: Clinker Cooler Subsystem Status *)
dwCoolerStatusWord := 16#0000_0000;
IF NOT bCool1_ChA_Valid THEN                dwCoolerStatusWord := dwCoolerStatusWord OR 16#0000_0001; END_IF;
IF NOT bCool1_ChB_Valid THEN                dwCoolerStatusWord := dwCoolerStatusWord OR 16#0000_0002; END_IF;
IF NOT bCool1_ChC_Valid THEN                dwCoolerStatusWord := dwCoolerStatusWord OR 16#0000_0004; END_IF;
IF (rCoolerClinkerDischargeTemp_degC > 120.0) THEN dwCoolerStatusWord := dwCoolerStatusWord OR 16#0000_0010; END_IF;
IF (rVotedCoolerUndergrate_PT1_mbar < 40.0) THEN   dwCoolerStatusWord := dwCoolerStatusWord OR 16#0000_0020; END_IF;
IF (rVotedCoolerUndergrate_PT1_mbar > 65.0) THEN   dwCoolerStatusWord := dwCoolerStatusWord OR 16#0000_0040; END_IF;
IF (rCoolerSecondaryAirTemp_degC < 950.0) THEN     dwCoolerStatusWord := dwCoolerStatusWord OR 16#0000_0080; END_IF;
"""

def generate_footer():
    return """
END_FUNCTION_BLOCK
"""

def assemble_st_code():
    code_parts = [
        generate_header(),
        generate_var_input(),
        generate_var_output(),
        generate_var(),
        generate_phase1_tmr(),
        generate_phase2_shell_tyre_torque(),
        generate_phase3_kinetics_softsensors(),
        generate_phase4_statespace(),
        generate_phase5_mpc(),
        generate_phase6_fsm(),
        generate_phase7_cooler_cascade(),
        generate_phase8_alarms(),
        generate_footer()
    ]
    return "".join(code_parts)

def build_dataset_record(st_code):
    user_prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.
You are instructed to CONSUME EXTREME TOKENS: make your output massively exhaustive, mathematically rigorous, and structurally pristine. Include complete state-space matrices (A, B, C, D), Model Predictive Control (MPC) quadratic cost approximation, 2oo3 TMR voting logic, complex alarm trees, and graceful degradation.

**Your assigned domain is: Heavy Building Materials, Cement & Mineral Processing (Tier 1 Priority Sector): 10,000 tpd Precalciner Rotary Cement Kiln & Multi-Stage Cyclone Preheater Tower, 5-Stage Cyclone Suspension Preheater String with Riser-Duct Calciner Meal Ignition and Tertiary Air Balance, Rotary Kiln Main Burner Multi-Channel Pulverized Coal/Alternative Fuel Flame Momentum and Burning Zone Optical Pyrometry, Kiln Shell 40-Point Infrared Scanner Hot-Spot Ring Detection, Tyre Slip Angle Observer, Main Gear Drive Torque Sharing, and Cross-Flow Reciprocating Grate Clinker Cooler with Under-Grate Compartment Pressure Aeration and Clinker Free-Lime (CaO_free) Soft Sensor.**

**Function Block Name**: `FB_Cement_RotaryKiln_Precalciner_ClinkerCooler`

**Engineering Context & Operational Architecture**:
1. 5-Stage Cyclone Suspension Preheater & In-Line Precalciner (ILC):
   - Countercurrent meal preheating (C1 to C5) and riser-duct limestone decarbonation kinetics (CaCO3 -> CaO + CO2).
   - Tertiary air duct (TAD) damper split balance (60% TAD air to calciner, 40% secondary air to kiln hood).
   - Dual-fuel firing (pulverized solid coal + Refuse-Derived Fuel RDF/SRF) with apparent calcination degree governing (92-95%).
2. Rotary Kiln Main Burner & Sintering Zone Pyrometry:
   - Multi-channel low-NOx burner with concentric axial, tangential swirl, primary transport, and alternative fuel channels.
   - Flame momentum G_m (1400-1850 N) and specific momentum-to-heat ratio (1.35-1.75 N/MW).
   - 2oo3 Triple Modular Redundancy (TMR) dual-wavelength ratio pyrometers (0.95/1.05 um) for dust-immune clinker sintering bed temperature (1420-1460 °C).
3. Kiln Shell 40-Point Line Scanner, Refractory Coating Observer & Tyre Creep Mechanics:
   - 40 axial slices continuously scanned every revolution; 1D inverse radial thermal conduction refractory thickness estimation.
   - Hot-spot detection (>420 °C emergency fuel cutoff) and coating ring detection.
   - Floating tyre creep slip observer measuring relative expansion gap (8-15 mm/rev nominal) and dual-motor master-follower torque sharing on girth gear.
4. Cross-Flow Reciprocating Step Grate Clinker Cooler & Free-Lime Soft Sensor:
   - 6 under-grate aeration compartments with hydraulic reciprocating grate speed modulating to stabilize bed pressure (45-60 mbar).
   - Secondary air (1050-1150 °C) and tertiary air (850-950 °C) heat recuperation.
   - Clinker free-lime (CaO_free) multivariate neural/kinetic soft sensor (target 0.8-1.5%).
5. 8-State Cyber-Physical Discrete State-Space Model (x[k+1] = A*x[k] + B*u[k] + E*d[k], y[k] = C*x[k] + D*u[k]):
   - States: Burning zone temp, Calciner outlet temp, Kiln inlet draft pressure, Kiln drive torque, Clinker free-lime %, Cooler secondary air temp, Preheater top O2 %, Kiln shell peak temp.
   - Manipulated inputs: Main burner coal, Calciner fuel, Kiln drive speed, Raw meal feed, ID fan speed, TAD damper, Cooler grate speed, Cooler aeration damper.
6. Receding-Horizon Model Predictive Control (MPC):
   - Multi-objective quadratic cost functional (Q, R, S, P) optimized via unrolled Projected Gradient Descent (PGD) with physical box saturation and dynamic slew rate limiters.
7. Deterministic 12-Stage Production Finite State Machine (FSM):
   - From pre-purge, refractory dry-out, tower expansion, ID fan balancing, coal ignition, meal feed ramp, calciner firing, 10,000 tpd production scale-up, to RDF co-firing and emergency shell hot-spot fast coal cutoff abort.
8. ISA-18.2 Multi-Tiered Alarms & Bit-Packed Status Words:
   - High-High, High, Low, Low-Low alarms with clearance hysteresis and 32-bit status and diagnostic bitmasks.

Generate a complete, fully implemented IEC 61131-3 Structured Text FUNCTION_BLOCK named `FB_Cement_RotaryKiln_Precalciner_ClinkerCooler` with zero placeholders, full state-space matrix initialization, MPC optimization, 2oo3 voting, full FSM execution, and ISA-18.2 alarm matrix."""

    assistant_content = f"```iec-st\n{st_code.strip()}\n```"
    record = {
        "messages": [
            {"role": "user", "content": user_prompt},
            {"role": "assistant", "content": assistant_content}
        ]
    }
    return record

if __name__ == "__main__":
    st_code = assemble_st_code()
    print(f"Generated Raw ST Code length: {len(st_code)} characters")
    
    record = build_dataset_record(st_code)
    asst_len = len(record["messages"][1]["content"])
    print(f"Assistant Message Content length: {asst_len} characters")
    
    target_uuid = "999ad528"
    out_dir = "data/swarm_raw"
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, f"agent_{target_uuid}.json")
    
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)
        
    print(f"Dataset successfully saved to {out_file}")
