# -*- coding: utf-8 -*-
"""
Builder module for FB_Fertilizer_AmmoniumNitrate_Granulation_Scrubber
Part 1: Header, VAR_INPUT, VAR_OUTPUT, VAR declarations
"""

def get_header_and_vars():
    code = """FUNCTION_BLOCK FB_Fertilizer_AmmoniumNitrate_Granulation_Scrubber
(*
========================================================================================================================
 LUMINA CYBER-PHYSICAL AUTOMATION ENGINE - SYNTHETIC DATASET V7 MAX-PERSONA
 PERSONA          : 75+ Years Principal Automation Fellow & Cyber-Physical Systems Chair
 DOMAIN           : Agrochemicals & Heavy Chemical Processing
 SYSTEM           : Ammonium Nitrate (AN) & NPK Industrial Fertilizer Granulation Complex (120 t/h Capacity)
 COMPLEX HARDWARE : - High-Capacity Rotary Granulation Drum (D = 4.2 m, L = 18.0 m, 120 t/h Nominal Output)
                    - Dual-Fluid Molten Slurry Spray Nozzle Atomization Array (175 deg C, 6.5 bar, 96.5 wt% AN Slurry)
                    - Rotary Flighted Co-Current Dryer with Natural Gas Low-NOx Burner (18 MW, Air-to-Fuel Ratio Control)
                    - Counter-Current Fluidized Bed Granule Cooler (4-Chamber Active Aeration & Dehumidified Chilled Air)
                    - Multi-Stage Tail-Gas Venturi Acid Scrubber (Delta P Throttle, pH Neutralization, Particulate < 15 mg/Nm3)
                    - Granule Moisture, Porosity & Mechanical Crush Strength Dynamic Observer (Fc >= 35 N Spec)
                    - Oversize/Undersize Double-Deck Vibratory Screen Recycle Ratio Closed-Loop Balancing (R = 2.5:1 to 4.2:1)
                    - Safety Instrumented System (SIS) SIL-3 Thermal Runaway Decomposition Deluge & Rapid Dump Interlocks
 CYBER-PHYSICS    : - Full 8-State Discrete State-Space Dynamic Model (x[k+1] = A*x[k] + B*u[k], y[k] = C*x[k] + D*u[k])
                    - Receding-Horizon Model Predictive Control (MPC) with Projected Gradient Descent (PGD)
                    - 2oo3 Triple Modular Redundancy (TMR) Voting with Bumpless Degradation Across 16 Field Channels
                    - ISA-18.2 Five-Tier Process Alarm Hierarchy & Diagnostic Bit-Packed Telemetry Words
                    - 12-Stage Deterministic Industrial Production Finite State Machine (FSM)
========================================================================================================================
 THERMOCHEMICAL, KINEMATIC & GRANULATION FOUNDATIONS:
 1. Molten Ammonium Nitrate (NH4NO3) Slurry Atomization & Onion-Skin Layering Kinetics:
    Molten AN slurry is sprayed at 175 deg C (melting point = 169.6 deg C) through dual-fluid nozzles at 6.5 bar with atomizing
    steam/air at 7.5 bar. Granule growth in the cascading curtain of the rotary drum occurs via viscous layering (onion-skin)
    and controlled binder agglomeration. Droplet coalescence is governed by the Ennis viscous Stokes number:
      St_v = (8 * rho_p * v_rel * r_p) / (9 * mu_liquid)
    Granule radius growth rate dr/dt follows the solids deposition mass flux:
      dr/dt = (m_dot_slurry * X_solids) / (4 * PI * r_p^2 * rho_bed * (1 - epsilon_bed))
 2. Ammonium Nitrate Autocatalytic Decomposition & Thermal Runaway Chemistry:
    Pure NH4NO3 decomposes exothermically above 210 deg C:
      NH4NO3 -> N2O + 2 H2O    (Delta H = -36 kJ/mol at 210-260 deg C)
    If free acidity rises (pH < 3.2) or chloride/transition-metal impurities exist, autocatalytic runaway accelerates:
      2 NH4NO3 -> 2 N2 + 4 H2O + O2 (Delta H = -118 kJ/mol)
    The SIL-3 SIS interlock continuously evaluates the Arrhenius thermal rate of rise (dT/dt > 0.75 deg C/s and T > 185 deg C)
    to command an immediate deluge water flood (< 1.2 s) and rapid dump of the molten slurry header to prevent detonation.
 3. Co-Current Flighted Rotary Drum Drying Kinetics:
    Granules containing 1.8 to 2.5 wt% moisture discharge from the drum into an 18 m flighted rotary dryer.
    Gas-to-particle heat transfer and moisture desorption follow the falling-rate drying equation:
      d(omega)/dt = - k_desorp * exp(-E_a / (R * T_granule)) * (omega - omega_equilibrium)
    Closed-loop burner firing controls the combustion air-to-fuel ratio lambda = 1.15 to 1.22 to ensure clean burnout,
    keeping flue gas inlet temperature between 140 deg C and 165 deg C to prevent granule remelting.
 4. 4-Chamber Counter-Current Fluid Bed Cooler & Crystal Phase Transition Stabilization:
    Solid AN undergoes a critical polymorphic phase transition (Phase IV orthorhombic to Phase III orthorhombic) at 32.1 deg C.
    Repeated cycling across 32.1 deg C causes crystal volume expansion (+3.6%), granule micro-cracking, and caking.
    Chambers 1-2 utilize filtered ambient air; Chambers 3-4 utilize dehumidified chilled air (12 deg C) to cool granules
    rapidly below 28 deg C before coating and bagging.
 5. Multi-Stage Venturi Acid Scrubber Tail-Gas Clean-Up:
    The tail-gas stream (240,000 Nm3/h) carrying AN dust and ammonia fumes passes through a variable-throat venturi scrubber.
    Aerosol capture efficiency follows the Johnstone impaction parameter:
      eta = 1 - exp(- k_venturi * (L / G) * sqrt(Psi))
    where Psi = (C_c * rho_particle * v_throat * d_aerosol^2) / (18 * mu_gas * D_throat).
    Recirculating scrubber liquor pH is precisely maintained between 3.8 and 4.4 by metering 93% nitric acid trim to
    react stoichiometric ammonia slip (NH3 + HNO3 -> NH4NO3) while avoiding excess acidity.
 6. Receding-Horizon Model Predictive Control (MPC):
    Optimizes an 8-state, 4-actuator quadratic cost function J over a receding prediction horizon:
      J = 0.5 * (x[k+1] - x_ref)^T * Q * (x[k+1] - x_ref) + 0.5 * u^T * R * u + 0.5 * Delta_u^T * S * Delta_u + 0.5 * x[k+1]^T * P * x[k+1]
    Iterative Projected Gradient Descent (PGD) enforces hard actuator saturation bounds [u_min, u_max] and slew rate limits.
========================================================================================================================
*)

VAR_INPUT
    (* ============================================================================================================== *)
    (* SECTION 1: MASTER AUTOMATION PERMISSIVES, SAFETY CIRCUITS & TIMING SIGNALS                                      *)
    (* ============================================================================================================== *)
    bMasterAutoEnable                 : BOOL := FALSE;    (* Master Plant Automation Enable Permissive [BOOL] *)
    bSafetyCircuitHealthy_NC          : BOOL := TRUE;     (* Dual-Channel Hardwired Emergency Trip Active Low [BOOL] *)
    bEmergencyDelugeManualTrip        : BOOL := FALSE;    (* Operator Emergency Deluge Manual Pushbutton Trip [BOOL] *)
    bFaultReset                       : BOOL := FALSE;    (* Master Plant Alarm Unlatch & Reset Command [BOOL] *)
    bNitrogenPurgePermissive          : BOOL := TRUE;     (* High-Pressure Inert Nitrogen Header Pressure Ready [BOOL] *)
    bBoilerSteamHeaderReady           : BOOL := TRUE;     (* Atomizing & Jacket Steam Supply Header Permissive [BOOL] *)
    bNaturalGasHeaderReady            : BOOL := TRUE;     (* Burner Natural Gas Fuel Supply Permissive [BOOL] *)
    bDelugeWaterSupplyReady           : BOOL := TRUE;     (* Dedicated Fire/Deluge Water Reservoir Level & Pressure Ok [BOOL] *)
    bEmergencyPowerAvailable          : BOOL := TRUE;     (* Plant UPS & Essential Diesel Generator System Healthy [BOOL] *)
    nRecipeFertilizerGradeID          : DINT := 3350;     (* Active Formulation Recipe ID (33.5% N Ammonium Nitrate) [-] *)
    tScanCycleTime_ms                 : TIME := T#100MS;  (* Discrete Execution Scan Period (100 ms) [TIME] *)

    (* ============================================================================================================== *)
    (* SECTION 2: 2oo3 TMR GRANULATION DRUM SENSORS (TAGS 101-104)                                                    *)
    (* ============================================================================================================== *)
    (* TT_DRUM_BED_TEMP_101: Triplicated Multi-Point Infrared / Sliding RTD Granule Bed Temperature [deg C] *)
    TT_DRUM_BED_TEMP_101A             : REAL := 102.50;   (* Drum Granule Bed Internal Temperature Channel A [deg C] *)
    TT_DRUM_BED_TEMP_101B             : REAL := 102.50;   (* Drum Granule Bed Internal Temperature Channel B [deg C] *)
    TT_DRUM_BED_TEMP_101C             : REAL := 102.50;   (* Drum Granule Bed Internal Temperature Channel C [deg C] *)

    (* PT_SLURRY_FEED_102: Molten Slurry Spray Header Dual-Fluid Injection Pressure [bar] *)
    PT_SLURRY_FEED_102A               : REAL := 6.50;     (* Molten AN Slurry Spray Manifold Pressure Channel A [bar] *)
    PT_SLURRY_FEED_102B               : REAL := 6.50;     (* Molten AN Slurry Spray Manifold Pressure Channel B [bar] *)
    PT_SLURRY_FEED_102C               : REAL := 6.50;     (* Molten AN Slurry Spray Manifold Pressure Channel C [bar] *)

    (* TT_SLURRY_FEED_103: Molten Slurry Spray Header Core Temperature [deg C] *)
    TT_SLURRY_FEED_103A               : REAL := 175.00;   (* Molten AN Slurry Header Temperature Channel A [deg C] *)
    TT_SLURRY_FEED_103B               : REAL := 175.00;   (* Molten AN Slurry Header Temperature Channel B [deg C] *)
    TT_SLURRY_FEED_103C               : REAL := 175.00;   (* Molten AN Slurry Header Temperature Channel C [deg C] *)

    (* TT_DRUM_SHELL_HOTSPOT_104: Continuous Multi-Zone Infrared Drum Shell Line-Scanner [deg C] *)
    TT_DRUM_SHELL_HOTSPOT_104A        : REAL := 82.00;    (* Drum Outer Shell Hotspot Pyrometer Channel A [deg C] *)
    TT_DRUM_SHELL_HOTSPOT_104B        : REAL := 82.00;    (* Drum Outer Shell Hotspot Pyrometer Channel B [deg C] *)
    TT_DRUM_SHELL_HOTSPOT_104C        : REAL := 82.00;    (* Drum Outer Shell Hotspot Pyrometer Channel C [deg C] *)

    (* ============================================================================================================== *)
    (* SECTION 3: 2oo3 TMR ROTARY DRYER & COMBUSTION SYSTEM (TAGS 201-204)                                            *)
    (* ============================================================================================================== *)
    (* TT_DRYER_INLET_TEMP_201: Co-Current Rotary Dryer Flue Gas Inlet Temperature [deg C] *)
    TT_DRYER_INLET_TEMP_201A          : REAL := 152.00;   (* Dryer Flue Gas Inlet Temperature Channel A [deg C] *)
    TT_DRYER_INLET_TEMP_201B          : REAL := 152.00;   (* Dryer Flue Gas Inlet Temperature Channel B [deg C] *)
    TT_DRYER_INLET_TEMP_201C          : REAL := 152.00;   (* Dryer Flue Gas Inlet Temperature Channel C [deg C] *)

    (* FT_BURNER_FUEL_GAS_202: 18 MW Low-NOx Burner Natural Gas Volumetric Flow [Nm3/h] *)
    FT_BURNER_FUEL_GAS_202A           : REAL := 1250.00;  (* Burner Natural Gas Fuel Flow Channel A [Nm3/h] *)
    FT_BURNER_FUEL_GAS_202B           : REAL := 1250.00;  (* Burner Natural Gas Fuel Flow Channel B [Nm3/h] *)
    FT_BURNER_FUEL_GAS_202C           : REAL := 1250.00;  (* Burner Natural Gas Fuel Flow Channel C [Nm3/h] *)

    (* FT_BURNER_AIR_FLOW_203: Forced Draft Combustion Air Volumetric Flow [Nm3/h] *)
    FT_BURNER_AIR_FLOW_203A           : REAL := 14200.00; (* Forced Draft Combustion Air Flow Channel A [Nm3/h] *)
    FT_BURNER_AIR_FLOW_203B           : REAL := 14200.00; (* Forced Draft Combustion Air Flow Channel B [Nm3/h] *)
    FT_BURNER_AIR_FLOW_203C           : REAL := 14200.00; (* Forced Draft Combustion Air Flow Channel C [Nm3/h] *)

    (* BE_BURNER_FLAME_SCAN_204: Dual-Spectrum UV/IR Burner Optical Flame Scanner [%] *)
    BE_BURNER_FLAME_SCAN_204A         : REAL := 94.50;    (* Burner Optical Flame Intensity Channel A [%] *)
    BE_BURNER_FLAME_SCAN_204B         : REAL := 94.50;    (* Burner Optical Flame Intensity Channel B [%] *)
    BE_BURNER_FLAME_SCAN_204C         : REAL := 94.50;    (* Burner Optical Flame Intensity Channel C [%] *)

    (* ============================================================================================================== *)
    (* SECTION 4: 2oo3 TMR FLUID BED COOLER SENSORS (TAGS 301-302)                                                    *)
    (* ============================================================================================================== *)
    (* TT_COOLER_ZONE4_TEMP_301: Counter-Current Cooler Chamber 4 Granule Discharge Temp [deg C] *)
    TT_COOLER_ZONE4_TEMP_301A         : REAL := 26.50;    (* Fluid Bed Cooler Exit Granule Temperature Channel A [deg C] *)
    TT_COOLER_ZONE4_TEMP_301B         : REAL := 26.50;    (* Fluid Bed Cooler Exit Granule Temperature Channel B [deg C] *)
    TT_COOLER_ZONE4_TEMP_301C         : REAL := 26.50;    (* Fluid Bed Cooler Exit Granule Temperature Channel C [deg C] *)

    (* PT_COOLER_PLENUM_302: Fluid Bed Aeration Plenum Distribution Differential Pressure [mbar] *)
    PT_COOLER_PLENUM_302A             : REAL := 28.50;    (* Cooler Deck Air Plenum Differential Pressure Channel A [mbar] *)
    PT_COOLER_PLENUM_302B             : REAL := 28.50;    (* Cooler Deck Air Plenum Differential Pressure Channel B [mbar] *)
    PT_COOLER_PLENUM_302C             : REAL := 28.50;    (* Cooler Deck Air Plenum Differential Pressure Channel C [mbar] *)

    (* ============================================================================================================== *)
    (* SECTION 5: 2oo3 TMR SOLID RECYCLE & PRODUCT SCALES (TAGS 401-402)                                               *)
    (* ============================================================================================================== *)
    (* WT_RECYCLE_MASS_FLOW_401: Radiometric / Impact Drag Conveyor Fines+Crushed Recycle Mass Rate [t/h] *)
    WT_RECYCLE_MASS_FLOW_401A         : REAL := 360.00;   (* Total Recycle Seed Solid Mass Flow Channel A [t/h] *)
    WT_RECYCLE_MASS_FLOW_401B         : REAL := 360.00;   (* Total Recycle Seed Solid Mass Flow Channel B [t/h] *)
    WT_RECYCLE_MASS_FLOW_401C         : REAL := 360.00;   (* Total Recycle Seed Solid Mass Flow Channel C [t/h] *)

    (* WT_PRODUCT_MASS_FLOW_402: Belt Scale Finished On-Spec Granule Mass Flow [t/h] *)
    WT_PRODUCT_MASS_FLOW_402A         : REAL := 120.00;   (* Finished On-Spec Product Mass Flow Channel A [t/h] *)
    WT_PRODUCT_MASS_FLOW_402B         : REAL := 120.00;   (* Finished On-Spec Product Mass Flow Channel B [t/h] *)
    WT_PRODUCT_MASS_FLOW_402C         : REAL := 120.00;   (* Finished On-Spec Product Mass Flow Channel C [t/h] *)

    (* ============================================================================================================== *)
    (* SECTION 6: 2oo3 TMR VENTURI SCRUBBER & EMISSIONS CEMS (TAGS 501-504)                                           *)
    (* ============================================================================================================== *)
    (* PDT_SCRUBBER_VENTURI_501: Venturi Throat Aerodynamic Differential Pressure [mbar] *)
    PDT_SCRUBBER_VENTURI_501A         : REAL := 48.00;    (* Venturi Scrubber Throat Delta P Channel A [mbar] *)
    PDT_SCRUBBER_VENTURI_501B         : REAL := 48.00;    (* Venturi Scrubber Throat Delta P Channel B [mbar] *)
    PDT_SCRUBBER_VENTURI_501C         : REAL := 48.00;    (* Venturi Scrubber Throat Delta P Channel C [mbar] *)

    (* AT_SCRUBBER_SUMP_PH_502: Triple Glass Electrode Acidic Recirculating Liquor pH [-] *)
    AT_SCRUBBER_SUMP_PH_502A          : REAL := 4.10;     (* Scrubber Recirculating Liquor pH Probe Channel A [pH] *)
    AT_SCRUBBER_SUMP_PH_502B          : REAL := 4.10;     (* Scrubber Recirculating Liquor pH Probe Channel B [pH] *)
    AT_SCRUBBER_SUMP_PH_502C          : REAL := 4.10;     (* Scrubber Recirculating Liquor pH Probe Channel C [pH] *)

    (* AT_STACK_PARTICULATE_503: Optical Cross-Stack Particulate Dust CEMS Analyzer [mg/Nm3] *)
    AT_STACK_PARTICULATE_503A         : REAL := 6.80;     (* Tail-Gas Stack Particulate Dust Analyzer Channel A [mg/Nm3] *)
    AT_STACK_PARTICULATE_503B         : REAL := 6.80;     (* Tail-Gas Stack Particulate Dust Analyzer Channel B [mg/Nm3] *)
    AT_STACK_PARTICULATE_503C         : REAL := 6.80;     (* Tail-Gas Stack Particulate Dust Analyzer Channel C [mg/Nm3] *)

    (* AT_STACK_AMMONIA_SLIP_504: Tunable Diode Laser (TDLS) Stack Ammonia Slip CEMS Analyzer [ppmv] *)
    AT_STACK_AMMONIA_SLIP_504A        : REAL := 4.20;     (* Tail-Gas Stack Free Ammonia Slip Channel A [ppmv] *)
    AT_STACK_AMMONIA_SLIP_504B        : REAL := 4.20;     (* Tail-Gas Stack Free Ammonia Slip Channel B [ppmv] *)
    AT_STACK_AMMONIA_SLIP_504C        : REAL := 4.20;     (* Tail-Gas Stack Free Ammonia Slip Channel C [ppmv] *)

    (* ============================================================================================================== *)
    (* SECTION 7: OPERATIONAL SETPOINTS, QUALITY CRITERIA & LAB ASSAYS                                                *)
    (* ============================================================================================================== *)
    rSet_TargetBedTemperature_degC    : REAL := 102.00;   (* Target Drum Bed Steady-State Temperature [deg C] *)
    rSet_TargetGranuleMoisture_pct    : REAL := 1.45;     (* Target Granulation Bed Operating Moisture [wt %] *)
    rSet_TargetMeanDiameter_d50_mm    : REAL := 3.10;     (* Target Product Granule Mass-Mean Diameter d50 [mm] *)
    rSet_TargetRecycleRatio           : REAL := 3.00;     (* Optimum Solid Seed Recycle-to-Product Ratio [-] *)
    rSet_TargetScrubberDeltaP_mbar    : REAL := 50.00;    (* Target Venturi Throat Aerodynamic Pressure Drop [mbar] *)
    rSet_TargetScrubber_pH            : REAL := 4.05;     (* Target Recirculating Liquor Neutralization pH [pH] *)
    rSet_SlurryFeedRateNominal_tph    : REAL := 122.50;   (* Nominal Molten AN Slurry Feed Flow Demand [t/h] *)
    rSet_DryerOutletMoistureMax_pct   : REAL := 0.35;     (* Strict Upper Limit for Dryer Discharge Moisture [wt %] *)
    rSet_CoolerDischargeTempMax_degC  : REAL := 28.00;    (* Strict Upper Limit for Granule Bagging Temperature [deg C] *)
    rSet_AtomizingSteamRatio          : REAL := 0.082;    (* Mass Ratio of Atomizing Steam to Molten Slurry [kg/kg] *)
    rSet_MinCrushStrength_N           : REAL := 35.00;    (* Minimum Mechanical Granule Breaking Force Spec [N] *)
    rAmbientAirTemperature_degC       : REAL := 22.00;    (* Plant Ambient Air Temperature [deg C] *)
    rAmbientAirRelativeHumidity_pct   : REAL := 65.00;    (* Plant Ambient Air Relative Humidity [%] *)
END_VAR

VAR_OUTPUT
    (* ============================================================================================================== *)
    (* SECTION 1: PLANT ACTUATOR DEMANDS, MODULATING VALVES & VARIABLE FREQUENCY DRIVES                              *)
    (* ============================================================================================================== *)
    rOut_SlurrySprayValve_pct         : REAL := 0.00;     (* Molten Slurry Flow Control Proportional Valve [0..100 %] *)
    rOut_AtomizingSteamValve_pct      : REAL := 0.00;     (* Atomizing Superheated Steam Throttle Valve [0..100 %] *)
    rOut_BurnerGasThrottle_pct        : REAL := 0.00;     (* Dryer Natural Gas Burner Control Valve [0..100 %] *)
    rOut_CombustionAirDamper_pct      : REAL := 0.00;     (* Burner Forced Draft Combustion Air Damper [0..100 %] *)
    rOut_DryerInducedDraftFan_pct     : REAL := 0.00;     (* Dryer ID Fan Variable Speed Drive [0..100 %] *)
    rOut_CoolerChamber1AirFan_pct     : REAL := 0.00;     (* Cooler Ambient Air Blower VFD [0..100 %] *)
    rOut_CoolerChilledAirFan_pct      : REAL := 0.00;     (* Cooler Chilled Air Blower VFD [0..100 %] *)
    rOut_VenturiThroatDamper_pct      : REAL := 0.00;     (* Venturi Scrubber Hydraulic Throat Damper Actuator [0..100 %] *)
    rOut_ScrubberRecircPumpHz         : REAL := 0.00;     (* Scrubber Acidic Recirculation Pump Inverter Speed [0..60 Hz] *)
    rOut_NitricAcidTrimValve_pct      : REAL := 0.00;     (* Concentrated 93% Nitric Acid Neutralization Valve [0..100 %] *)
    rOut_RecycleDragConveyorSpeed_pct : REAL := 0.00;     (* Solid Recycle Drag Flight Conveyor VFD [0..100 %] *)
    rOut_OversizeCageMillSpeed_RPM    : REAL := 0.00;     (* Double-Cage Mill Lump Crusher Speed [0..1200 RPM] *)

    (* ============================================================================================================== *)
    (* SECTION 2: SIL-3 SAFETY INSTRUMENTED SYSTEM (SIS) FAST TRIP ACTUATION SIGNALS                                 *)
    (* ============================================================================================================== *)
    bOut_EmergencyDelugeFloodActuate  : BOOL := FALSE;    (* High-Capacity Drum Emergency Quench Deluge Flood Valve [BOOL] *)
    bOut_SlurryEmergencyDumpValve     : BOOL := FALSE;    (* Rapid Slurry Header De-pressurization Dump to Sump [BOOL] *)
    bOut_BurnerSafetyShutoffValve_Trip: BOOL := FALSE;    (* Double-Block-and-Bleed Natural Gas Safety Trip [BOOL] *)
    bOut_NitrogenPurgeFloodValve      : BOOL := FALSE;    (* Emergency Inert Nitrogen Inerting Injection Valve [BOOL] *)

    (* ============================================================================================================== *)
    (* SECTION 3: 2oo3 TMR VALIDATED TELEMETRY VALUES                                                                *)
    (* ============================================================================================================== *)
    rVoted_DrumBedTemp_degC           : REAL := 102.50;   (* 2oo3 Voted Granule Bed Internal Temperature [deg C] *)
    rVoted_SlurryFeedPress_bar        : REAL := 6.50;     (* 2oo3 Voted Molten Slurry Injection Pressure [bar] *)
    rVoted_SlurryFeedTemp_degC        : REAL := 175.00;   (* 2oo3 Voted Molten Slurry Injection Temperature [deg C] *)
    rVoted_DrumShellHotspot_degC      : REAL := 82.00;    (* 2oo3 Voted Rotary Drum Outer Shell Hotspot [deg C] *)
    rVoted_DryerInletTemp_degC        : REAL := 152.00;   (* 2oo3 Voted Dryer Flue Gas Inlet Temperature [deg C] *)
    rVoted_BurnerGasFlow_Nm3h         : REAL := 1250.00;  (* 2oo3 Voted Natural Gas Fuel Flow [Nm3/h] *)
    rVoted_BurnerAirFlow_Nm3h         : REAL := 14200.00; (* 2oo3 Voted Combustion Air Flow [Nm3/h] *)
    rVoted_BurnerFlameIntensity_pct   : REAL := 94.50;    (* 2oo3 Voted Burner Optical Flame Scanner Signal [%] *)
    rVoted_CoolerZone4Temp_degC       : REAL := 26.50;    (* 2oo3 Voted Granule Cooler Exit Temperature [deg C] *)
    rVoted_CoolerPlenumPress_mbar     : REAL := 28.50;    (* 2oo3 Voted Cooler Deck Air Plenum Pressure [mbar] *)
    rVoted_RecycleMassFlow_tph        : REAL := 360.00;   (* 2oo3 Voted Solid Recycle Seed Mass Flow [t/h] *)
    rVoted_ProductMassFlow_tph        : REAL := 120.00;   (* 2oo3 Voted Finished On-Spec Product Mass Flow [t/h] *)
    rVoted_VenturiDeltaP_mbar         : REAL := 48.00;    (* 2oo3 Voted Venturi Scrubber Differential Pressure [mbar] *)
    rVoted_Scrubber_pH                : REAL := 4.10;     (* 2oo3 Voted Scrubber Recirculating Liquor pH [pH] *)
    rVoted_StackDust_mgNm3            : REAL := 6.80;     (* 2oo3 Voted Tail-Gas Stack Particulate Dust [mg/Nm3] *)
    rVoted_StackAmmoniaSlip_ppmv      : REAL := 4.20;     (* 2oo3 Voted Tail-Gas Stack Free Ammonia Slip [ppmv] *)

    (* ============================================================================================================== *)
    (* SECTION 4: ADVANCED CYBER-PHYSICAL STATE OBSERVERS & CHEMICAL KINETICS METRICS                                 *)
    (* ============================================================================================================== *)
    rCalc_EstimatedGranuleMoisture_pct: REAL := 1.45;     (* Arrhenius Desorption Observer Drum Bed Moisture [wt %] *)
    rCalc_EstimatedCrushStrength_N    : REAL := 42.50;    (* Dynamic Porosity & Crystal Compaction Breaking Force [N] *)
    rCalc_CalculatedRecycleRatio      : REAL := 3.00;     (* Measured Mass Ratio of Recycle Solid to Product [-] *)
    rCalc_AirToFuelRatio_Lambda       : REAL := 1.18;     (* Actual Combustion Excess Air Coefficient Lambda [-] *)
    rCalc_ThermalRunawayMargin_degC   : REAL := 107.50;   (* Temperature Margin to Catastrophic Decomposition [deg C] *)
    rCalc_ThermalRateOfRise_degCps    : REAL := 0.00;     (* Moving Window Bed Temperature Derivative dT/dt [deg C/s] *)
    rCalc_ScrubberAerosolCollectionEff: REAL := 99.45;    (* Johnstone Venturi Sub-Micron Aerosol Efficiency [%] *)
    rCalc_DrumGranuleHoldUp_tons      : REAL := 46.20;    (* Estimated Granule Dynamic Mass Inside Drum [tons] *)
    rCalc_GranulePorosity_pct         : REAL := 4.80;     (* Calculated Internal Granule Void Porosity Fraction [%] *)
    rCalc_MPC_OptimalCost_J           : REAL := 0.00;     (* Discrete Receding-Horizon MPC Realized Quadratic Cost [-] *)

    (* ============================================================================================================== *)
    (* SECTION 5: ISA-18.2 ALARMS, DIAGNOSTICS & SYSTEM STATUS WORDS                                                  *)
    (* ============================================================================================================== *)
    wAlarmWord_Critical_ISA18         : DWORD := 16#00000000; (* Priority 1 Critical Plant Safety Trips *)
    wAlarmWord_Warning_ISA18          : DWORD := 16#00000000; (* Priority 2 Process Quality & Operating Deviations *)
    wDiagnosticMask_TMR_Health        : DWORD := 16#00000000; (* 2oo3 TMR Channel Discrepancy & Health Bitmask *)
    wPlantSubsystemStatus             : DWORD := 16#00000000; (* Complex Subsystem Operational Readiness Word *)
    iActiveFSM_State                  : INT   := 0;          (* Current 12-Stage Production FSM State [0..11] *)
    bPlantInProduction                : BOOL  := FALSE;      (* Granulation Complex Operating in Steady-State *)
    bEmergencyDelugeActive            : BOOL  := FALSE;      (* Deluge Quench Solenoid Actively Flooding *)
    bRunawayDecompositionTripped      : BOOL  := FALSE;      (* Autocatalytic AN Runaway Safety Interlock Tripped *)
END_VAR

VAR
    (* ============================================================================================================== *)
    (* SECTION 1: PHYSICAL CONSTANTS & THERMOCHEMICAL SYSTEM PARAMETERS                                               *)
    (* ============================================================================================================== *)
    c_rTs                             : REAL := 0.100;    (* Discrete Servo Task Scan Interval (100 ms) [s] *)
    c_rPi                             : REAL := 3.141592653589793; (* Mathematical Constant Pi *)
    c_rDrumDiameter_m                 : REAL := 4.20;     (* Rotary Granulation Drum Internal Diameter [m] *)
    c_rDrumLength_m                   : REAL := 18.00;    (* Rotary Granulation Drum Length [m] *)
    c_rDrumVolume_m3                  : REAL := 249.38;   (* Total Internal Cylindrical Volume [m3] *)
    c_rDensityAN_Solid_kgm3           : REAL := 1725.0;   (* Solid Phase Ammonium Nitrate Bulk Density [kg/m3] *)
    c_rDensitySlurry_kgm3             : REAL := 1420.0;   (* Molten 96.5% AN Slurry Density at 175 deg C [kg/m3] *)
    c_rCp_AN_Slurry_kJkgK             : REAL := 2.240;    (* Specific Heat Capacity of Molten Slurry [kJ/kg*K] *)
    c_rCp_Granules_kJkgK              : REAL := 1.740;    (* Specific Heat Capacity of Solid Granules [kJ/kg*K] *)
    c_rCp_FlueGas_kJkgK               : REAL := 1.085;    (* Specific Heat Capacity of Flue Gas [kJ/kg*K] *)
    c_rHeatOfFusion_AN_kJkg           : REAL := 74.50;    (* Latent Heat of Crystallization of AN [kJ/kg] *)
    c_rHeatOfVapWater_kJkg            : REAL := 2257.0;   (* Latent Heat of Water Vaporization [kJ/kg] *)
    c_rGasConstant_R_kJkmolK          : REAL := 8.31446;  (* Universal Gas Constant [kJ/kmol*K] *)
    c_rArrheniusEa_Decomp_kJmol       : REAL := 142.5;    (* Activation Energy for AN Decomposition [kJ/mol] *)
    c_rArrheniusA0_Decomp             : REAL := 1.85E+11; (* Frequency Factor for Exothermic Decomposition [1/s] *)
    c_rCriticalRunawayTemp_degC       : REAL := 210.00;   (* Uncontrolled Autocatalytic Runaway Threshold [deg C] *)
    c_rWarningRunawayTemp_degC        : REAL := 185.00;   (* Thermal Acceleration Pre-Alarm Threshold [deg C] *)
    c_rMaxAllowableRateOfRise_degCps  : REAL := 0.750;    (* Maximum Allowable Bed Temp Rate of Rise [deg C/s] *)
    c_rStoichAirToGasRatio            : REAL := 9.52;     (* Stoichiometric Volume Ratio Air/Natural Gas [-] *)
    c_rTargetAirFuelLambda            : REAL := 1.18;     (* Optimal Excess Combustion Air Coefficient [-] *)

    (* ============================================================================================================== *)
    (* SECTION 2: 8x8 DISCRETE STATE-SPACE MODEL & RECEDING-HORIZON MPC MATRICES                                      *)
    (* ============================================================================================================== *)
    bMatricesInitialized              : BOOL := FALSE;    (* First-Scan State-Space Matrices Initialization Flag *)
    aA                                : ARRAY[1..8, 1..8] OF REAL; (* Discrete State Transition Matrix A (8x8) *)
    aB                                : ARRAY[1..8, 1..4] OF REAL; (* Discrete Control Input Matrix B (8x4) *)
    aC                                : ARRAY[1..8, 1..8] OF REAL; (* Discrete Output Observation Matrix C (8x8) *)
    aD                                : ARRAY[1..8, 1..4] OF REAL; (* Discrete Feedforward Matrix D (8x4) *)
    ax_state                          : ARRAY[1..8] OF REAL;       (* Dynamic State Vector x[k] *)
    ax_next                           : ARRAY[1..8] OF REAL;       (* Projected State Vector x[k+1] *)
    ax_ref                            : ARRAY[1..8] OF REAL;       (* Equilibrium Reference Trajectory x_ref *)
    ae_tracking                       : ARRAY[1..8] OF REAL;       (* Dynamic Tracking Error Vector e[k] *)
    au_control                        : ARRAY[1..4] OF REAL;       (* Actuator Control Vector u[k] *)
    au_prev                           : ARRAY[1..4] OF REAL;       (* Previous Cycle Actuator Vector u[k-1] *)
    au_delta                          : ARRAY[1..4] OF REAL;       (* Actuator Slew Rate Vector Delta_u[k] *)
    ay_output                         : ARRAY[1..8] OF REAL;       (* Observed Synthetic Output Vector y[k] *)
    aQ_Weight                         : ARRAY[1..8] OF REAL;       (* Diagonal State Error Penalty Matrix Q *)
    aR_Weight                         : ARRAY[1..4] OF REAL;       (* Diagonal Control Effort Penalty Matrix R *)
    aS_Weight                         : ARRAY[1..4] OF REAL;       (* Diagonal Actuator Slew Rate Penalty Matrix S *)
    aP_TerminalWeight                 : ARRAY[1..8] OF REAL;       (* Diagonal Terminal Horizon Stability Matrix P *)
    au_min                            : ARRAY[1..4] OF REAL;       (* Lower Hard Actuator Saturation Constraints *)
    au_max                            : ARRAY[1..4] OF REAL;       (* Upper Hard Actuator Saturation Constraints *)
    adelta_u_max                      : ARRAY[1..4] OF REAL;       (* Maximum Allowable Slew Rate per 100 ms Step *)
    aGrad_u                           : ARRAY[1..4] OF REAL;       (* Analytical Gradient Vector dJ/du *)
    c_rMPC_StepAlpha                  : REAL := 0.00032;           (* Projected Gradient Descent Learning Rate *)
    rMPC_QuadraticCostAccum           : REAL := 0.0;               (* Evaluated Cost Metric J *)

    (* ============================================================================================================== *)
    (* SECTION 3: 2oo3 TMR TOLERANCE GATES, PERSISTENCY TIMERS & ISOLATION FLAGS                                      *)
    (* ============================================================================================================== *)
    c_rTol_DrumBedTemp_degC           : REAL := 3.50;     (* Bed RTD Permissible Discrepancy Gate [deg C] *)
    c_rTol_SlurryPress_bar            : REAL := 0.45;     (* Slurry Header Pressure Gate [bar] *)
    c_rTol_SlurryTemp_degC            : REAL := 4.00;     (* Slurry Header Temperature Gate [deg C] *)
    c_rTol_DrumShellHotspot_degC      : REAL := 5.00;     (* Drum Outer Shell Hotspot Gate [deg C] *)
    c_rTol_DryerInletTemp_degC        : REAL := 6.00;     (* Dryer Flue Gas Temperature Gate [deg C] *)
    c_rTol_BurnerGasFlow_Nm3h         : REAL := 65.00;    (* Natural Gas Flow Gate [Nm3/h] *)
    c_rTol_BurnerAirFlow_Nm3h         : REAL := 450.00;   (* Combustion Air Flow Gate [Nm3/h] *)
    c_rTol_BurnerFlameScan_pct        : REAL := 8.00;     (* Optical Flame Intensity Gate [%] *)
    c_rTol_CoolerZone4Temp_degC       : REAL := 2.50;     (* Fluid Bed Cooler Exit Temp Gate [deg C] *)
    c_rTol_CoolerPlenumPress_mbar     : REAL := 3.20;     (* Cooler Deck Air Plenum Pressure Gate [mbar] *)
    c_rTol_RecycleMassFlow_tph        : REAL := 18.00;    (* Recycle Solid Mass Flow Gate [t/h] *)
    c_rTol_ProductMassFlow_tph        : REAL := 8.00;     (* Finished Product Mass Flow Gate [t/h] *)
    c_rTol_VenturiDeltaP_mbar         : REAL := 3.80;     (* Venturi Scrubber Delta P Gate [mbar] *)
    c_rTol_Scrubber_pH                : REAL := 0.28;     (* Scrubber Liquor pH Gate [pH] *)
    c_rTol_StackDust_mgNm3            : REAL := 2.20;     (* Particulate Optical Dust Gate [mg/Nm3] *)
    c_rTol_StackAmmoniaSlip_ppmv      : REAL := 1.50;     (* Tunable Diode Laser Ammonia Gate [ppmv] *)
    c_rTMR_PersistencyLimit_s         : REAL := 0.250;    (* 2oo3 Discrepancy Debounce Timer Limit (250 ms) [s] *)

    (* 16x Discrepancy Elapsed Accumulator Timers *)
    rTimer_BedTemp_Disc_s             : REAL := 0.0;
    rTimer_SlurryPress_Disc_s         : REAL := 0.0;
    rTimer_SlurryTemp_Disc_s          : REAL := 0.0;
    rTimer_ShellHotspot_Disc_s        : REAL := 0.0;
    rTimer_DryerInletTemp_Disc_s      : REAL := 0.0;
    rTimer_BurnerGasFlow_Disc_s       : REAL := 0.0;
    rTimer_BurnerAirFlow_Disc_s       : REAL := 0.0;
    rTimer_BurnerFlame_Disc_s         : REAL := 0.0;
    rTimer_CoolerTemp_Disc_s          : REAL := 0.0;
    rTimer_CoolerPlenum_Disc_s        : REAL := 0.0;
    rTimer_RecycleFlow_Disc_s         : REAL := 0.0;
    rTimer_ProductFlow_Disc_s         : REAL := 0.0;
    rTimer_VenturiDeltaP_Disc_s       : REAL := 0.0;
    rTimer_Scrubber_pH_Disc_s         : REAL := 0.0;
    rTimer_StackDust_Disc_s           : REAL := 0.0;
    rTimer_AmmoniaSlip_Disc_s         : REAL := 0.0;

    (* 16x Triplet Isolation Latches (TRUE = Channel Discarded as Outlier) *)
    bIso_BedTemp_ChA, bIso_BedTemp_ChB, bIso_BedTemp_ChC : BOOL := FALSE;
    bIso_SlurryPress_ChA, bIso_SlurryPress_ChB, bIso_SlurryPress_ChC : BOOL := FALSE;
    bIso_SlurryTemp_ChA, bIso_SlurryTemp_ChB, bIso_SlurryTemp_ChC : BOOL := FALSE;
    bIso_ShellHotspot_ChA, bIso_ShellHotspot_ChB, bIso_ShellHotspot_ChC : BOOL := FALSE;
    bIso_DryerInletTemp_ChA, bIso_DryerInletTemp_ChB, bIso_DryerInletTemp_ChC : BOOL := FALSE;
    bIso_BurnerGasFlow_ChA, bIso_BurnerGasFlow_ChB, bIso_BurnerGasFlow_ChC : BOOL := FALSE;
    bIso_BurnerAirFlow_ChA, bIso_BurnerAirFlow_ChB, bIso_BurnerAirFlow_ChC : BOOL := FALSE;
    bIso_BurnerFlame_ChA, bIso_BurnerFlame_ChB, bIso_BurnerFlame_ChC : BOOL := FALSE;
    bIso_CoolerTemp_ChA, bIso_CoolerTemp_ChB, bIso_CoolerTemp_ChC : BOOL := FALSE;
    bIso_CoolerPlenum_ChA, bIso_CoolerPlenum_ChB, bIso_CoolerPlenum_ChC : BOOL := FALSE;
    bIso_RecycleFlow_ChA, bIso_RecycleFlow_ChB, bIso_RecycleFlow_ChC : BOOL := FALSE;
    bIso_ProductFlow_ChA, bIso_ProductFlow_ChB, bIso_ProductFlow_ChC : BOOL := FALSE;
    bIso_VenturiDeltaP_ChA, bIso_VenturiDeltaP_ChB, bIso_VenturiDeltaP_ChC : BOOL := FALSE;
    bIso_Scrubber_pH_ChA, bIso_Scrubber_pH_ChB, bIso_Scrubber_pH_ChC : BOOL := FALSE;
    bIso_StackDust_ChA, bIso_StackDust_ChB, bIso_StackDust_ChC : BOOL := FALSE;
    bIso_AmmoniaSlip_ChA, bIso_AmmoniaSlip_ChB, bIso_AmmoniaSlip_ChC : BOOL := FALSE;

    (* ============================================================================================================== *)
    (* SECTION 4: GRANULE OBSERVER, DRYING KINETICS & SCREEN BALANCING REGISTERS                                      *)
    (* ============================================================================================================== *)
    rGranuleMoistureInternal_pct      : REAL := 1.45;     (* Drum Bed Observed Moisture [wt %] *)
    rGranulePorosityInternal_frac     : REAL := 0.048;    (* Granule Internal Void Fraction [-] *)
    rGranuleMeanDiameter_mm           : REAL := 3.10;     (* Calculated Mass-Mean Particle Diameter d50 [mm] *)
    rRecycleRatioFiltered             : REAL := 3.00;     (* Low-Pass Filtered Recycle Ratio [-] *)
    rBedHoldupEstimated_tons          : REAL := 46.20;    (* Drum Dynamic Granule Mass Inventory [tons] *)
    rBedTemperaturePriorCycle_degC    : REAL := 102.50;   (* Prior 100 ms Sample Bed Temp for dT/dt [deg C] *)
    rBedTempDerivFiltered_degCps      : REAL := 0.00;     (* First-Order Filtered Rate of Rise dT/dt [deg C/s] *)
    rCombustionAirDemand_Nm3h         : REAL := 14200.0;  (* Air Flow Setpoint from Stoichiometric Ratio [Nm3/h] *)
    rScrubberAcidDemand_Lh            : REAL := 42.0;     (* 93% Nitric Acid Neutralization Flow Demand [L/h] *)
    rVenturiCollectionEffEst_pct      : REAL := 99.45;    (* Estimated Sub-Micron Aerosol Removal Efficiency [%] *)

    (* ============================================================================================================== *)
    (* SECTION 5: ISA-18.2 FIVE-TIER PROCESS ALARM THRESHOLDS & DEADBANDS                                             *)
    (* ============================================================================================================== *)
    c_rTrip_DrumBedTemp_HI_HI         : REAL := 135.00;   (* Drum Granule Overheating Safety Interlock Trip [deg C] *)
    c_rAlarm_DrumBedTemp_HI           : REAL := 115.00;   (* Drum Granule Bed Temperature High Warning [deg C] *)
    c_rAlarm_DrumBedTemp_LO           : REAL := 88.00;    (* Drum Bed Low Temp Incomplete Granulation Warning [deg C] *)
    c_rTrip_DrumBedTemp_LO_LO         : REAL := 75.00;    (* Slurry Freezing / Mud Caking Risk Trip [deg C] *)
    c_rTrip_SlurryPress_HI_HI         : REAL := 8.50;     (* Slurry Header Overpressure Rupture Trip [bar] *)
    c_rAlarm_SlurryPress_HI           : REAL := 7.40;     (* Slurry Header High Pressure Warning [bar] *)
    c_rAlarm_SlurryPress_LO           : REAL := 5.20;     (* Slurry Header Low Pressure Atomization Loss Warning [bar] *)
    c_rTrip_SlurryPress_LO_LO         : REAL := 4.00;     (* Slurry Header Severe Pressure Loss Trip [bar] *)
    c_rTrip_SlurryTemp_HI_HI          : REAL := 188.00;   (* Slurry Decomposition Danger Trip [deg C] *)
    c_rAlarm_SlurryTemp_HI            : REAL := 182.00;   (* Slurry Temperature High Warning [deg C] *)
    c_rAlarm_SlurryTemp_LO            : REAL := 168.00;   (* Slurry Crystallization Freeze Risk Warning [deg C] *)
    c_rTrip_SlurryTemp_LO_LO          : REAL := 162.00;   (* Slurry Severe Low Temp Header Freeze Trip [deg C] *)
    c_rTrip_ShellHotspot_HI_HI        : REAL := 125.00;   (* Drum Outer Shell Hotspot Structural Trip [deg C] *)
    c_rAlarm_ShellHotspot_HI          : REAL := 95.00;    (* Drum Shell High Temperature Warning [deg C] *)
    c_rTrip_DryerInletTemp_HI_HI      : REAL := 180.00;   (* Dryer Inlet Granule Decomposition Safety Trip [deg C] *)
    c_rAlarm_DryerInletTemp_HI        : REAL := 168.00;   (* Dryer Inlet High Temperature Warning [deg C] *)
    c_rTrip_BurnerFlameLoss_Trip      : REAL := 25.00;    (* Burner Optical Flameout Emergency Trip [%] *)
    c_rTrip_CoolerExitTemp_HI_HI      : REAL := 36.00;    (* Granule Polymorphic Transition Hazard Trip [deg C] *)
    c_rAlarm_CoolerExitTemp_HI        : REAL := 30.00;    (* Granule Cooler High Temperature Warning [deg C] *)
    c_rTrip_ScrubberDeltaP_HI_HI      : REAL := 75.00;    (* Venturi Scrubber Severe Hydraulic Choke Trip [mbar] *)
    c_rAlarm_ScrubberDeltaP_HI        : REAL := 62.00;    (* Venturi Throat High Differential Pressure Warning [mbar] *)
    c_rAlarm_ScrubberDeltaP_LO        : REAL := 32.00;    (* Venturi Throat Low Impaction Warning [mbar] *)
    c_rTrip_ScrubberDeltaP_LO_LO      : REAL := 20.00;    (* Venturi Throat Gas Channeling Loss Trip [mbar] *)
    c_rTrip_Scrubber_pH_LO_LO         : REAL := 3.20;     (* Severe Acidification / AN Explosion Hazard Trip [pH] *)
    c_rAlarm_Scrubber_pH_LO           : REAL := 3.65;     (* Low pH Acid Overfeed Warning [pH] *)
    c_rAlarm_Scrubber_pH_HI           : REAL := 4.60;     (* High pH Ammonia Slip Breakthrough Warning [pH] *)
    c_rTrip_Scrubber_pH_HI_HI         : REAL := 5.20;     (* Severe Ammonia Loss / Regulatory Breach Trip [pH] *)
    c_rTrip_StackDust_HI_HI           : REAL := 25.00;    (* Environmental Stack Particulate Breach Trip [mg/Nm3] *)
    c_rAlarm_StackDust_HI             : REAL := 14.50;    (* Stack Particulate Pre-Alarm Warning [mg/Nm3] *)
    c_rTrip_AmmoniaSlip_HI_HI         : REAL := 15.00;    (* Environmental Stack Ammonia Slip Trip [ppmv] *)
    c_rAlarm_AmmoniaSlip_HI           : REAL := 8.50;     (* Stack Ammonia Slip Pre-Alarm Warning [ppmv] *)
    c_rDeadband_Temperature          : REAL := 1.80;     (* Temperature Alarm Reset Hysteresis [deg C] *)
    c_rDeadband_Pressure             : REAL := 0.25;     (* Pressure Alarm Reset Hysteresis [bar] *)
    c_rDeadband_DeltaP               : REAL := 2.00;     (* Differential Pressure Reset Hysteresis [mbar] *)
    c_rDeadband_pH                   : REAL := 0.15;     (* pH Reset Hysteresis [pH] *)
    c_rDeadband_StackDust            : REAL := 1.20;     (* Dust Reset Hysteresis [mg/Nm3] *)

    (* Latched Process Alarm Bits *)
    bAlarm_DrumBedTemp_HI_HI          : BOOL := FALSE;
    bAlarm_DrumBedTemp_HI             : BOOL := FALSE;
    bAlarm_DrumBedTemp_LO             : BOOL := FALSE;
    bAlarm_DrumBedTemp_LO_LO          : BOOL := FALSE;
    bAlarm_SlurryPress_HI_HI          : BOOL := FALSE;
    bAlarm_SlurryPress_HI             : BOOL := FALSE;
    bAlarm_SlurryPress_LO             : BOOL := FALSE;
    bAlarm_SlurryPress_LO_LO          : BOOL := FALSE;
    bAlarm_SlurryTemp_HI_HI           : BOOL := FALSE;
    bAlarm_SlurryTemp_HI              : BOOL := FALSE;
    bAlarm_SlurryTemp_LO              : BOOL := FALSE;
    bAlarm_SlurryTemp_LO_LO           : BOOL := FALSE;
    bAlarm_ShellHotspot_HI_HI         : BOOL := FALSE;
    bAlarm_ShellHotspot_HI            : BOOL := FALSE;
    bAlarm_DryerInletTemp_HI_HI       : BOOL := FALSE;
    bAlarm_DryerInletTemp_HI          : BOOL := FALSE;
    bAlarm_BurnerFlameLoss_Trip       : BOOL := FALSE;
    bAlarm_CoolerExitTemp_HI_HI       : BOOL := FALSE;
    bAlarm_CoolerExitTemp_HI          : BOOL := FALSE;
    bAlarm_ScrubberDeltaP_HI_HI       : BOOL := FALSE;
    bAlarm_ScrubberDeltaP_HI          : BOOL := FALSE;
    bAlarm_ScrubberDeltaP_LO          : BOOL := FALSE;
    bAlarm_ScrubberDeltaP_LO_LO       : BOOL := FALSE;
    bAlarm_Scrubber_pH_LO_LO          : BOOL := FALSE;
    bAlarm_Scrubber_pH_LO             : BOOL := FALSE;
    bAlarm_Scrubber_pH_HI             : BOOL := FALSE;
    bAlarm_Scrubber_pH_HI_HI          : BOOL := FALSE;
    bAlarm_StackDust_HI_HI            : BOOL := FALSE;
    bAlarm_StackDust_HI               : BOOL := FALSE;
    bAlarm_AmmoniaSlip_HI_HI          : BOOL := FALSE;
    bAlarm_AmmoniaSlip_HI             : BOOL := FALSE;
    bAlarm_ThermalRateOfRise_Trip     : BOOL := FALSE;
    bAlarm_TMR_MajorDegraded_Warn     : BOOL := FALSE;

    (* ============================================================================================================== *)
    (* SECTION 6: 12-STAGE OPERATIONAL FINITE STATE MACHINE (FSM) STEP REGISTERS                                      *)
    (* ============================================================================================================== *)
    iFSM_CurrentState                 : INT := 0;         (* Active Operational State [0..11] *)
    iFSM_NextState                    : INT := 0;         (* Sequenced State Transition Target [0..11] *)
    rStateDwellTimer_s                : REAL := 0.0;      (* Active State Elapsed Residency Chronometer [s] *)
    rPurgeSequenceTimer_s             : REAL := 0.0;      (* Inert Gas Sweep Duration Timer [s] *)
    rPreheatRampTimer_s               : REAL := 0.0;      (* Dryer Refractory & Bed Thermal Soak Timer [s] *)
    rCoolerAerationTimer_s            : REAL := 0.0;      (* Fluid Bed Fluidization Initialization Timer [s] *)
    rSeedLoopTimer_s                  : REAL := 0.0;      (* Dry Granule Circulation Stabilization Timer [s] *)
    rNozzlePrimeTimer_s               : REAL := 0.0;      (* Slurry Spray Header Steam Warmup Timer [s] *)
    rDelugeHoldTimer_s                : REAL := 0.0;      (* Post-Trip Quench Deluge Persistence Timer [s] *)
    rNozzleCleanoutTimer_s            : REAL := 0.0;      (* Atomizer Superheated Steam Rodding Timer [s] *)
    rRampDownTimer_s                  : REAL := 0.0;      (* Controlled Slurry Cut-Back Emptying Timer [s] *)

    (* Math Scopes, Matrix Indexes & TMR Helper Variables *)
    idx_i                             : INT := 1;
    idx_j                             : INT := 1;
    idx_k                             : INT := 1;
    rDiffAB                           : REAL := 0.0;
    rDiffBC                           : REAL := 0.0;
    rDiffCA                           : REAL := 0.0;
    bAgreeAB                          : BOOL := FALSE;
    bAgreeBC                          : BOOL := FALSE;
    bAgreeCA                          : BOOL := FALSE;
    rTempSum                          : REAL := 0.0;
    rValA                             : REAL := 0.0;
    rValB                             : REAL := 0.0;
    rValC                             : REAL := 0.0;
    rVotedVal                         : REAL := 0.0;
    rArrheniusExp                     : REAL := 0.0;
    rDesorptionRate                   : REAL := 0.0;
    rCombustionStoichFlow             : REAL := 0.0;
    rVenturiPsiParam                  : REAL := 0.0;
END_VAR
"""
    return code
