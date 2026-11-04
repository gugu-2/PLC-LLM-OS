# -*- coding: utf-8 -*-
"""
Full Generator for FB_OilGas_ContinuousCrudeDistillation_CDU_AtmosphericFurnace
Lumina Swarm V7 Max-Persona Protocol (Principal Automation Fellow & Cyber-Physical Systems Chair)
"""

import sys
import os
import json
import uuid
import re

def get_header_and_interfaces():
    return """FUNCTION_BLOCK FB_OilGas_ContinuousCrudeDistillation_CDU_AtmosphericFurnace
(* =====================================================================================================================
 * LUMINA ADVANCED PROCESS AUTOMATION & CYBER-PHYSICAL SYSTEMS SPECIFICATION
 * CLASSIFICATION               : Petrochemical Refining & Continuous Atmospheric Distillation
 * SYSTEM DESIGNATION           : World-Scale 350,000 BPD Crude Distillation Unit (CDU) Atmospheric Pipestill & Furnace
 * PROCESS EQUIPMENT TAGS       :
 *   - Fired Heater             : F-101 (120 MW Multi-Burner Balanced-Draft Radiant-Convection Pipestill, 4 Radiant Passes)
 *   - Atmospheric Column       : C-101 (54 Sieve & Valve Trays, 8.5m Internal Diameter, Overflash Wash Bed, Sump Baffle)
 *   - Side-Stream Strippers    : C-102 (Heavy Naphtha), C-103 (Kerosene), C-104 (Diesel), C-105 (Atmospheric Gas Oil / AGO)
 *   - Pumparound Circuits      : PA-1 (Kerosene / Top Inter-Zone), PA-2 (Diesel / Gas Oil Mid-Zone)
 *   - Desalter Pre-Flash Train : D-101A/B (2-Stage Electrostatic Desalters with Fast Grid Rag Layer Protection)
 *   - Overhead Condensers      : E-101A..H Fin-Fan Air Coolers, E-102 Trim Coolers, V-101 Overhead Reflux Accumulator
 * INDUSTRY STANDARDS           : IEC 61131-3 3rd Ed., IEC 61508 / IEC 61511 (SIL-3 SIS ESD), ISA-18.2, API 560, API 521, NFPA 85
 * AUTHOR / ARCHITECT           : Principal Automation Fellow & Cyber-Physical Systems Chair (Lumina Swarm V7)
 * =====================================================================================================================
 * CYBER-PHYSICAL PROCESS DYNAMICS & RIGOROUS PROCESS FORMULATIONS:
 *
 * 1. 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) ARCHITECTURE:
 *    All 16 critical process transmitter loops employ triplicated instrumentation (Ch A, Ch B, Ch C) with galvanically
 *    isolated 4-20 mA HART transmitters. Pairwise discrepancy checks evaluate:
 *        Delta_AB = |rawA - rawB|, Delta_BC = |rawB - rawC|, Delta_CA = |rawC - rawA|
 *    If any pairwise delta exceeds the calibrated tolerance threshold for >= 500 ms (debounce timer), a sensor discrepancy
 *    diagnostic fault bit is latched. The voting engine performs bumpless degradation:
 *      - 3 Healthy Channels: Mid-value median selection.
 *      - 2 Healthy Channels: Arithmetic mean of surviving channels.
 *      - 1 Healthy Channel : Single surviving channel fallback with high-priority maintenance alarm.
 *      - 0 Healthy Channels: Failsafe freeze latch and initiation of emergency trip sequence for safety-critical loops.
 *
 * 2. FIRED HEATER COMBUSTION STOICHIOMETRY & THERMAL EFFICIENCY:
 *    The 120 MW crude pipestill combusts refinery fuel gas (mixed methane, ethane, propane, butane with MW approx 21.4 kg/kmol).
 *    Stoichiometric air demand requires approx 16.5 kg dry air per kg fuel gas. Flue gas excess oxygen (AT_201) governs
 *    the theoretical excess air ratio:
 *        lambda_excess = 20.9 / (20.9 - O2_flue)
 *        ExcessAir_pct = (lambda_excess - 1.0) * 100.0
 *    Furnace stack thermal losses are computed via the ASME PTC 4 / Siegert formulation:
 *        Q_stack_loss = [ m_flue * Cp_flue * (T_stack - T_ambient) + m_fuel * CO_ppm * 10^-6 * Delta_H_CO ] / 3.6e6 [MW]
 *    Total furnace fuel-to-crude absorbed efficiency:
 *        eta_furnace = (Q_absorbed_crude / Q_fuel_fired) * 100.0
 *    Cross-limiting fuel/air safety ratio control (NFPA 85) prevents substoichiometric firing: air demand leads fuel gas
 *    on load increases, and fuel gas demand leads air damper on load decreases.
 *
 * 3. MULTICOMPONENT EQUILIBRIUM FLASH VAPORIZATION (EFV) & SHORTCUT VLE:
 *    At the flash zone (P = 1.65 bar_a, T = 368.5 deg C), preheated crude oil expands through the transfer line nozzle.
 *    The vaporized mole fraction e = V/F satisfies the Rachford-Rice flash equation:
 *        Sum_{i=1..6} [ z_i * (K_i - 1) / (1 + e * (K_i - 1)) ] = 0
 *    where K_i = P_sat_i(T) / P_total. The shortcut Fenske-Underwood-Gilliland formulation models the stage-by-stage
 *    internal traffic, reflux ratio R/R_min, and cut point separation between Heavy Naphtha, Kerosene, Diesel, AGO, and Residue.
 *
 * 4. COLUMN INTERNAL SIEVE TRAY HYDRAULICS & FAIR'S FLOODING PREDICTOR:
 *    Trays 1 to 54 are evaluated against entrainment flooding and weeping instability using Fair's correlation:
 *        Liquid Flow Parameter F_lv = (L / V) * sqrt(rho_v / rho_l)
 *        Capacity Factor C_sb = 0.144 * (sigma / 20.0)^0.2 * [ 1.0 - 0.28 * ln(F_lv + 0.01) ]
 *        Flooding Vapor Velocity u_flood = C_sb * sqrt((rho_l - rho_v) / rho_v)
 *        Flooding Factor pct = (u_actual / u_flood) * 100.0
 *    Active area weeping is flagged if dry tray pressure drop Delta_P_dry falls below liquid crest head (h_w + h_ow).
 *
 * 5. DESALTER ELECTROSTATIC EMULSION & WATER-IN-CRUDE CONDUCTIVE RAG LAYER:
 *    Electrostatic desalting utilizes high-voltage AC electric fields (16 kV - 25 kV) to coalesce emulsified brine droplets.
 *    Accumulation of conductive rag layer (water-in-crude emulsion stabilized by asphaltenes and clays) causes electrical
 *    bridging between grid electrodes. The complex impedance Z_grid = V_grid / I_grid and dielectric dissipation factor
 *    tan_delta = R_grid / X_grid detect impending conductive collapse. If current exceeds 120 mA or tan_delta > 0.45,
 *    a sub-cycle (< 20 ms) transformer breaker trip is commanded to prevent explosive transformer rupture.
 *
 * 6. OVERFLASH ZONE LIQUID ENTRAINMENT PREVENTION:
 *    Overflash liquid rate L_of (typically 2-3 vol% of total crude charge) is monitored to maintain wash tray active wetting:
 *        Wetting Rate = L_of / Column_Area >= 0.15 m3/(h * m2)
 *    Insufficient overflash promotes dry-out and severe metals/coke entrainment into the heavy atmospheric gas oil (HAGO).
 *
 * 7. PUMPAROUND DYNAMIC ENTHALPY DUTY BALANCING (PA-1):
 *    Top pumparound circuit PA-1 extracts latent heat directly from tray 14 to unload overhead condenser vapor traffic:
 *        Q_PA1 = m_PA1 * Cp_liquid * (T_draw - T_return) / 3.6e6 [MW]
 *    The controller dynamically adjusts PA-1 circulation flow to maintain optimal tower internal reflux ratios.
 *
 * 8. RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC):
 *    Governs an 8-state, 8-input discrete cyber-physical formulation sampled at Ts = 100 ms:
 *        x[k+1] = A * x[k] + B * u[k]
 *        y[k]   = C * x[k] + D * u[k]
 *    State Vector x = [Delta_T_COT, Delta_O2, Delta_T_ovhd, Delta_L_reflux, Delta_T_diesel, Delta_Q_PA1, Delta_F_overflash, Delta_L_bottoms]^T
 *    Control Vector u = [CV_FuelGas, CV_AirDamper, CV_Reflux, CV_Naphtha, CV_Diesel, CV_PA1, CV_BottomSteam, CV_ResidRundown]^T
 *    Projected Gradient Descent (PGD) minimizes quadratic cost functional:
 *        J = Sum [ (x - x_ref)^T * Q * (x - x_ref) + u^T * R * u + Delta_u^T * S * Delta_u ] + x^T * P * x
 *    subject to valve saturation bounds [0..100%] and slew rate limits.
 *
 * 9. ISA-18.2 MULTI-TIERED ALARM HIERARCHY & SAFETY ESD INTERLOCKS:
 *    Implements 5 alarm levels: High-High (HH), High (H), Low (L), Low-Low (LL), and Rate-of-Change (ROC) with hysteresis.
 *    Emergency shutdown (ESD) actions include fuel gas double-block-and-bleed slam shut (< 50 ms), column flare BDV opening,
 *    and desalter high-voltage power isolation.
 *
 * 10. DETERMINISTIC 12-STAGE OPERATIONAL FINITE STATE MACHINE (FSM):
 *     State 0 : SYSTEM_OFFLINE_N2_BLANKET
 *     State 1 : FURNACE_PURGE_AND_PILOT_IGNITION
 *     State 2 : CRUDE_FEED_COLD_CIRCULATION
 *     State 3 : FURNACE_RAMP_AND_COT_STABILIZE
 *     State 4 : COLUMN_WARMUP_AND_TOTAL_REFLUX
 *     State 5 : SIDESTREAM_CUT_EXTRACTION_ON
 *     State 6 : PUMPAROUND_DUTY_ENGAGEMENT
 *     State 7 : OPTIMAL_MPC_CRUDE_DISTILLATION
 *     State 8 : FURNACE_DECOKING_SOOTBLOW
 *     State 9 : CONTROLLED_DRAIN_AND_COOLDOWN
 *     State 10: EMERGENCY_DEPRESSURIZE_TO_FLARE
 *     State 11: FAILSAFE_SHUTDOWN_TRIPPED
 * =====================================================================================================================
 *)
VAR_INPUT
    (* Master Supervisory Permissives & Safety Commands *)
    bMasterEnable                     : BOOL := FALSE;    (* Master Supervisory Automation Enable Permissive [BOOL] *)
    bAutoCycleStart                   : BOOL := FALSE;    (* Initiate Automatic Start-up Sequence Command [BOOL] *)
    bResetAlarms                      : BOOL := FALSE;    (* Master Alarm Reset & Trip Acknowledge Trigger [BOOL] *)
    bEmergencyTrip_ESD                : BOOL := FALSE;    (* Operator Emergency Manual Unit Trip Pushbutton [BOOL] *)
    bDecokingInitiate                 : BOOL := FALSE;    (* Operator Command to Initiate On-Line Furnace Decoking [BOOL] *)
    bManualOverrideEnable             : BOOL := FALSE;    (* Manual Operator Output Override Permissive [BOOL] *)
    bDesalterGridPermissive           : BOOL := TRUE;     (* Desalter Electrostatic Transformer Run Permissive [BOOL] *)
    bSootblowerPermissive             : BOOL := TRUE;     (* Furnace Radiant/Convection Sootblower Ready [BOOL] *)
    rCycleTime_dt                     : REAL := 0.10;     (* Discrete Automation Execution Sample Interval [s] *)

    (* 2oo3 TMR Triplets (16 Process Loops x 3 Channels = 48 Transmitters) *)
    (* Loop 01: Desalted Crude Feed Booster Discharge Pressure [bar_g] *)
    PT_CDU_FEED_101A                  : REAL := 28.5;     (* Crude Feed Booster Pump Discharge Pressure Ch A [bar_g] *)
    PT_CDU_FEED_101B                  : REAL := 28.5;     (* Crude Feed Booster Pump Discharge Pressure Ch B [bar_g] *)
    PT_CDU_FEED_101C                  : REAL := 28.5;     (* Crude Feed Booster Pump Discharge Pressure Ch C [bar_g] *)

    (* Loop 02: Fired Heater Combined Coil Outlet Temperature (COT) [deg C] *)
    TT_CDU_FURNACE_COT_102A           : REAL := 368.5;    (* Combined Coil Outlet Temperature Ch A [deg C] *)
    TT_CDU_FURNACE_COT_102B           : REAL := 368.5;    (* Combined Coil Outlet Temperature Ch B [deg C] *)
    TT_CDU_FURNACE_COT_102C           : REAL := 368.5;    (* Combined Coil Outlet Temperature Ch C [deg C] *)

    (* Loop 03: Total Raw Crude Charge Flow Rate to Atmospheric Pipestill [m3/h] *)
    FT_CRUDE_CHARGE_103A              : REAL := 2318.0;   (* Total Crude Charge Volumetric Flow Ch A [m3/h] *)
    FT_CRUDE_CHARGE_103B              : REAL := 2318.0;   (* Total Crude Charge Volumetric Flow Ch B [m3/h] *)
    FT_CRUDE_CHARGE_103C              : REAL := 2318.0;   (* Total Crude Charge Volumetric Flow Ch C [m3/h] *)

    (* Loop 04: Fired Heater Radiant Arch Flue Gas Excess Oxygen [vol%] *)
    AT_FLUE_GAS_O2_201A               : REAL := 2.65;     (* Flue Gas Excess Oxygen Concentration Ch A [vol%] *)
    AT_FLUE_GAS_O2_201B               : REAL := 2.65;     (* Flue Gas Excess Oxygen Concentration Ch B [vol%] *)
    AT_FLUE_GAS_O2_201C               : REAL := 2.65;     (* Flue Gas Excess Oxygen Concentration Ch C [vol%] *)

    (* Loop 05: Fired Heater Radiant Box Flue Gas Unburnt Carbon Monoxide [ppm] *)
    AT_FLUE_GAS_CO_202A               : REAL := 35.0;     (* Flue Gas Carbon Monoxide Concentration Ch A [ppm] *)
    AT_FLUE_GAS_CO_202B               : REAL := 35.0;     (* Flue Gas Carbon Monoxide Concentration Ch B [ppm] *)
    AT_FLUE_GAS_CO_202C               : REAL := 35.0;     (* Flue Gas Carbon Monoxide Concentration Ch C [ppm] *)

    (* Loop 06: Fired Heater Radiant Arch Furnace Draft Vacuum Pressure [mbar] *)
    PT_FURNACE_DRAFT_203A             : REAL := -0.45;    (* Radiant Arch Vacuum Draft Pressure Ch A [mbar] *)
    PT_FURNACE_DRAFT_203B             : REAL := -0.45;    (* Radiant Arch Vacuum Draft Pressure Ch B [mbar] *)
    PT_FURNACE_DRAFT_203C             : REAL := -0.45;    (* Radiant Arch Vacuum Draft Pressure Ch C [mbar] *)

    (* Loop 07: Fired Heater Fuel Gas Main Header Mass Flow Rate [kg/h] *)
    FT_FUEL_GAS_SUPPLY_204A           : REAL := 8250.0;   (* Fuel Gas Main Supply Mass Flow Rate Ch A [kg/h] *)
    FT_FUEL_GAS_SUPPLY_204B           : REAL := 8250.0;   (* Fuel Gas Main Supply Mass Flow Rate Ch B [kg/h] *)
    FT_FUEL_GAS_SUPPLY_204C           : REAL := 8250.0;   (* Fuel Gas Main Supply Mass Flow Rate Ch C [kg/h] *)

    (* Loop 08: Atmospheric Column Overhead Vapor Pressure [bar_g] *)
    PT_COLUMN_OVERHEAD_301A           : REAL := 1.48;     (* Main Column Overhead Vapor Pressure Ch A [bar_g] *)
    PT_COLUMN_OVERHEAD_301B           : REAL := 1.48;     (* Main Column Overhead Vapor Pressure Ch B [bar_g] *)
    PT_COLUMN_OVERHEAD_301C           : REAL := 1.48;     (* Main Column Overhead Vapor Pressure Ch C [bar_g] *)

    (* Loop 09: Atmospheric Column Overhead Vapor Temperature [deg C] *)
    TT_COLUMN_OVERHEAD_302A           : REAL := 128.2;    (* Main Column Overhead Vapor Temperature Ch A [deg C] *)
    TT_COLUMN_OVERHEAD_302B           : REAL := 128.2;    (* Main Column Overhead Vapor Temperature Ch B [deg C] *)
    TT_COLUMN_OVERHEAD_302C           : REAL := 128.2;    (* Main Column Overhead Vapor Temperature Ch C [deg C] *)

    (* Loop 10: Overhead Reflux Accumulator Drum Liquid Level [%] *)
    LT_REFLUX_DRUM_303A               : REAL := 52.5;     (* Reflux Accumulator Drum Liquid Level Ch A [%] *)
    LT_REFLUX_DRUM_303B               : REAL := 52.5;     (* Reflux Accumulator Drum Liquid Level Ch B [%] *)
    LT_REFLUX_DRUM_303C               : REAL := 52.5;     (* Reflux Accumulator Drum Liquid Level Ch C [%] *)

    (* Loop 11: Column Top External Reflux Flow Rate [m3/h] *)
    FT_OVERHEAD_REFLUX_304A           : REAL := 420.0;    (* External Liquid Reflux Return Flow Ch A [m3/h] *)
    FT_OVERHEAD_REFLUX_304B           : REAL := 420.0;    (* External Liquid Reflux Return Flow Ch B [m3/h] *)
    FT_OVERHEAD_REFLUX_304C           : REAL := 420.0;    (* External Liquid Reflux Return Flow Ch C [m3/h] *)

    (* Loop 12: Diesel Side-Stream Draw Tray Temperature [deg C] *)
    TT_DIESEL_STRIPPER_TRAY_401A      : REAL := 258.4;    (* Diesel Draw Tray Liquid Temperature Ch A [deg C] *)
    TT_DIESEL_STRIPPER_TRAY_401B      : REAL := 258.4;    (* Diesel Draw Tray Liquid Temperature Ch B [deg C] *)
    TT_DIESEL_STRIPPER_TRAY_401C      : REAL := 258.4;    (* Diesel Draw Tray Liquid Temperature Ch C [deg C] *)

    (* Loop 13: Pumparound PA-1 (Top/Kero) Circulation Flow Rate [m3/h] *)
    FT_PUMPAROUND_PA1_501A            : REAL := 850.0;    (* Pumparound PA-1 Circulation Flow Ch A [m3/h] *)
    FT_PUMPAROUND_PA1_501B            : REAL := 850.0;    (* Pumparound PA-1 Circulation Flow Ch B [m3/h] *)
    FT_PUMPAROUND_PA1_501C            : REAL := 850.0;    (* Pumparound PA-1 Circulation Flow Ch C [m3/h] *)

    (* Loop 14: Pumparound PA-1 Cooled Return Temperature [deg C] *)
    TT_PUMPAROUND_PA1_RET_502A        : REAL := 162.0;    (* Pumparound PA-1 Cooled Return Temp Ch A [deg C] *)
    TT_PUMPAROUND_PA1_RET_502B        : REAL := 162.0;    (* Pumparound PA-1 Cooled Return Temp Ch B [deg C] *)
    TT_PUMPAROUND_PA1_RET_502C        : REAL := 162.0;    (* Pumparound PA-1 Cooled Return Temp Ch C [deg C] *)

    (* Loop 15: Atmospheric Column Bottom Residue Level [%] *)
    LT_COLUMN_BOTTOMS_601A            : REAL := 48.0;     (* Column Bottom Residue Sump Liquid Level Ch A [%] *)
    LT_COLUMN_BOTTOMS_601B            : REAL := 48.0;     (* Column Bottom Residue Sump Liquid Level Ch B [%] *)
    LT_COLUMN_BOTTOMS_601C            : REAL := 48.0;     (* Column Bottom Residue Sump Liquid Level Ch C [%] *)

    (* Loop 16: Atmospheric Residue Bottoms Rundown Flow Rate [m3/h] *)
    FT_RESID_BOTTOMS_602A             : REAL := 865.0;    (* Atmospheric Residue Product Rundown Flow Ch A [m3/h] *)
    FT_RESID_BOTTOMS_602B             : REAL := 865.0;    (* Atmospheric Residue Product Rundown Flow Ch B [m3/h] *)
    FT_RESID_BOTTOMS_602C             : REAL := 865.0;    (* Atmospheric Residue Product Rundown Flow Ch C [m3/h] *)

    (* Desalter Electrostatic Grid Analyzer Signals *)
    rDesalter_GridVoltage_kV          : REAL := 21.5;     (* High-Voltage Transformer Secondary Grid Voltage [kV] *)
    rDesalter_GridCurrent_mA          : REAL := 48.2;     (* Grid Leakage / Emulsion Conduction Current [mA] *)
    rDesalter_PhaseAngle_Deg          : REAL := 72.4;     (* Voltage-to-Current Fundamental Phase Angle [deg] *)
    rDesalter_WaterCut_pct            : REAL := 0.28;     (* Desalted Crude BS&W Water-in-Oil Residual Cut [%] *)

    (* Additional Process Fluid & Hardware Inputs *)
    rOverflashWashFlow_m3h            : REAL := 95.0;     (* Wash Oil Tray Circulation Flow to Flash Zone [m3/h] *)
    rKeroseneDrawFlow_m3h             : REAL := 285.0;    (* Kerosene Stripper Draw Product Flow [m3/h] *)
    rDieselDrawFlow_m3h               : REAL := 620.0;    (* Diesel Stripper Draw Product Flow [m3/h] *)
    rAGODrawFlow_m3h                  : REAL := 195.0;    (* Atmospheric Gas Oil (AGO) Draw Product Flow [m3/h] *)
    rBottomStrippingSteam_kgh         : REAL := 6800.0;   (* Superheated Stripping Steam to Column Bottoms [kg/h] *)
    rAmbientAirTemp_DegC              : REAL := 25.0;     (* Combustion Air Ambient Intake Temperature [deg C] *)
    rFuelGasLHV_MJkg                  : REAL := 47.8;     (* Fired Heater Fuel Gas Lower Heating Value [MJ/kg] *)

    (* Supervisory Setpoints for Closed-Loop Regulation *)
    rSP_FurnaceCOT_DegC               : REAL := 368.0;    (* Target Fired Heater Coil Outlet Temperature [deg C] *)
    rSP_FlueGasO2_pct                 : REAL := 2.50;     (* Target Fired Heater Flue Gas Excess Oxygen [vol%] *)
    rSP_OverheadTemp_DegC             : REAL := 128.0;    (* Target Column Overhead Vapor Temperature [deg C] *)
    rSP_RefluxDrumLevel_pct           : REAL := 50.0;     (* Target Overhead Reflux Drum Liquid Level [%] *)
    rSP_DieselTrayTemp_DegC           : REAL := 258.0;    (* Target Diesel Draw Tray Temperature [deg C] *)
    rSP_PA1_Duty_MW                   : REAL := 32.5;     (* Target Top Pumparound PA-1 Heat Duty [MW] *)
    rSP_OverflashRate_m3h             : REAL := 95.0;     (* Target Overflash Wash Liquid Rate [m3/h] *)
    rSP_BottomsLevel_pct              : REAL := 50.0;     (* Target Column Bottom Residue Level [%] *)

    (* Manual Valve Demand Overrides (Active when bManualOverrideEnable is TRUE) *)
    rManual_FuelGas_pct               : REAL := 45.0;     (* Manual Fuel Gas Valve Demand [0..100 %] *)
    rManual_DamperAir_pct             : REAL := 48.0;     (* Manual Combustion Air Damper Demand [0..100 %] *)
    rManual_Reflux_pct                : REAL := 40.0;     (* Manual External Reflux Valve Demand [0..100 %] *)
    rManual_NaphthaDraw_pct           : REAL := 35.0;     (* Manual Heavy Naphtha Draw Valve Demand [0..100 %] *)
    rManual_DieselDraw_pct            : REAL := 55.0;     (* Manual Diesel Draw Valve Demand [0..100 %] *)
    rManual_PA1_Flow_pct              : REAL := 60.0;     (* Manual Pumparound PA-1 Flow Valve Demand [0..100 %] *)
    rManual_StrippingSteam_pct        : REAL := 30.0;     (* Manual Bottoms Stripping Steam Valve Demand [0..100 %] *)
    rManual_ResidRundown_pct          : REAL := 50.0;     (* Manual Residue Rundown Valve Demand [0..100 %] *)
END_VAR
VAR_OUTPUT
    (* Final Actuator Control Demands (0.0 to 100.0 %) *)
    rCV_FurnaceFuelGas_pct            : REAL;             (* Fired Heater Fuel Gas Main Control Valve Demand [0..100 %] *)
    rCV_FurnaceDamperAir_pct          : REAL;             (* Forced Draft Air Register / Stack Damper Demand [0..100 %] *)
    rCV_OverheadReflux_pct            : REAL;             (* Column Top External Liquid Reflux Control Valve [0..100 %] *)
    rCV_NaphthaDraw_pct               : REAL;             (* Heavy Naphtha Side-Stream Draw Control Valve [0..100 %] *)
    rCV_DieselDraw_pct                : REAL;             (* Diesel Stripper Product Rundown Control Valve [0..100 %] *)
    rCV_PA1_Flow_pct                  : REAL;             (* Pumparound PA-1 Circulation Flow Control Valve [0..100 %] *)
    rCV_BottomStrippingSteam_pct      : REAL;             (* Column Bottom Stripping Steam Valve Demand [0..100 %] *)
    rCV_ResidRundown_pct              : REAL;             (* Atmospheric Residue Bottoms Rundown Valve [0..100 %] *)

    (* Safety Instrumented System (SIS / ESD) Fast Trips & Permissives *)
    bESD_FuelGasDoubleBlockBleed_Trip : BOOL;             (* Emergency Fast Slam-Shut Fuel Gas Double Block & Bleed [BOOL] *)
    bESD_DesalterTransformer_Trip     : BOOL;             (* Desalter Electrostatic Transformer Vacuum Breaker Trip [BOOL] *)
    bESD_ColumnFlareDepressurize_Open : BOOL;             (* Column Overhead Emergency Depressuring to Flare BDV [BOOL] *)
    bESD_CrudeFeedShutoff_Trip        : BOOL;             (* Desalted Crude Charge Booster Feed Emergency Trip [BOOL] *)
    bInterlock_FurnaceDraftTrip       : BOOL;             (* Fired Heater Positive Pressure Flame Rollout Interlock [BOOL] *)
    bUnitTripActive                   : BOOL;             (* Unit Master Trip Latch Status [BOOL] *)
    bUnitInOptimalMPC                 : BOOL;             (* Unit Operating in State 7 Optimal Multivariable MPC [BOOL] *)

    (* Cyber-Physical Observer Diagnostics *)
    rObs_FurnaceThermalEfficiency_pct : REAL;             (* Fired Heater Absorbed Fuel-to-Crude Thermal Efficiency [%] *)
    rObs_ExcessAirRatio_pct           : REAL;             (* Calculated Combustion Excess Air Percentage [%] *)
    rObs_StackLoss_MW                 : REAL;             (* Flue Gas Sensible & Latent Stack Enthalpy Loss [MW] *)
    rObs_TrayFloodingFactor_pct       : REAL;             (* Column Critical Sieve Trays Fair Flooding Ratio [%] *)
    rObs_TrayWeepingRisk_pct          : REAL;             (* Active Area Dry vs Hydrostatic Weeping Probability [%] *)
    rObs_OverflashLiquidRate_m3h      : REAL;             (* Flash Zone Overflash Wash Liquid Rate Observer [m3/h] *)
    rObs_PA1_ActualHeatDuty_MW        : REAL;             (* Pumparound PA-1 Dynamic Heat Extraction Duty [MW] *)
    rObs_DesalterRagLayerRisk_pct     : REAL;             (* Conductive Water-in-Crude Emulsion Rag Layer Growth [%] *)
    rObs_DesalterLossTangent          : REAL;             (* Desalter Grid Emulsion Dielectric Dissipation Factor tan(delta) [-] *)
    rObs_CrudeAPI_Gravity             : REAL;             (* Reconstructed Charge Crude Oil API Gravity [deg API] *)

    (* Production & Unit Performance Metrics *)
    rCrudeThroughput_BPD              : REAL;             (* Volumetric Crude Distillation Unit Processing Rate [BPD] *)
    rTotalDistillateYield_pct         : REAL;             (* Combined Yield of Distillates (Naphtha+Kero+Diesel+AGO) [%] *)
    rMPC_CostObjectiveJ               : REAL;             (* Current Model Predictive Control Cycle Quadratic Cost [-] *)
    rMPC_SolveIterations              : REAL;             (* Projected Gradient Descent Convergence Iteration Count [-] *)

    (* Status & Alarm Bitmask Words *)
    dwSystemStateWord                 : DWORD;            (* Packed FSM Operational State, Modes & Health Word *)
    dwAlarmWord_Critical_HH           : DWORD;            (* ISA-18.2 Priority 1 High-High Critical Trips Bitmask *)
    dwAlarmWord_Warning_H             : DWORD;            (* ISA-18.2 Priority 2 High Process Warnings Bitmask *)
    dwAlarmWord_Low_L                 : DWORD;            (* ISA-18.2 Priority 3 Low Process Warnings Bitmask *)
    dwAlarmWord_LowLow_LL             : DWORD;            (* ISA-18.2 Priority 1 Low-Low Critical Interlocks Bitmask *)
    dwAlarmWord_RateOfChange          : DWORD;            (* Fast Transient Rate-of-Change Alarm Bitmask *)
    dwTMR_Diagnostic_Word1            : DWORD;            (* 2oo3 TMR Sensor Health Bitmask (Transmitters 01 to 08) *)
    dwTMR_Diagnostic_Word2            : DWORD;            (* 2oo3 TMR Sensor Health Bitmask (Transmitters 09 to 16) *)
    wFSM_CurrentStateCode             : WORD;             (* Numerical FSM Operational State Indicator (0 to 11) *)
END_VAR
VAR
    (* 2oo3 TMR Voted Process Variables *)
    rVoted_PT_101                     : REAL := 28.5;     (* Voted Crude Feed Booster Discharge Pressure [bar_g] *)
    rVoted_TT_102                     : REAL := 368.5;    (* Voted Combined Coil Outlet Temperature (COT) [deg C] *)
    rVoted_FT_103                     : REAL := 2318.0;   (* Voted Total Crude Charge Flow Rate [m3/h] *)
    rVoted_AT_201                     : REAL := 2.65;     (* Voted Flue Gas Excess Oxygen [vol%] *)
    rVoted_AT_202                     : REAL := 35.0;     (* Voted Flue Gas Carbon Monoxide [ppm] *)
    rVoted_PT_203                     : REAL := -0.45;    (* Voted Radiant Arch Draft Vacuum Pressure [mbar] *)
    rVoted_FT_204                     : REAL := 8250.0;   (* Voted Fuel Gas Mass Flow Rate [kg/h] *)
    rVoted_PT_301                     : REAL := 1.48;     (* Voted Column Overhead Vapor Pressure [bar_g] *)
    rVoted_TT_302                     : REAL := 128.2;    (* Voted Column Overhead Vapor Temperature [deg C] *)
    rVoted_LT_303                     : REAL := 52.5;     (* Voted Reflux Drum Liquid Level [%] *)
    rVoted_FT_304                     : REAL := 420.0;    (* Voted Column Top External Reflux Flow [m3/h] *)
    rVoted_TT_401                     : REAL := 258.4;    (* Voted Diesel Draw Tray Temperature [deg C] *)
    rVoted_FT_501                     : REAL := 850.0;    (* Voted Pumparound PA-1 Circulation Flow [m3/h] *)
    rVoted_TT_502                     : REAL := 162.0;    (* Voted Pumparound PA-1 Cooled Return Temp [deg C] *)
    rVoted_LT_601                     : REAL := 48.0;     (* Voted Column Bottom Residue Level [%] *)
    rVoted_FT_602                     : REAL := 865.0;    (* Voted Atmospheric Residue Rundown Flow [m3/h] *)

    (* 2oo3 TMR Channel Healthy Flags *)
    bHealthy_PT_101A : BOOL := TRUE; bHealthy_PT_101B : BOOL := TRUE; bHealthy_PT_101C : BOOL := TRUE;
    bHealthy_TT_102A : BOOL := TRUE; bHealthy_TT_102B : BOOL := TRUE; bHealthy_TT_102C : BOOL := TRUE;
    bHealthy_FT_103A : BOOL := TRUE; bHealthy_FT_103B : BOOL := TRUE; bHealthy_FT_103C : BOOL := TRUE;
    bHealthy_AT_201A : BOOL := TRUE; bHealthy_AT_201B : BOOL := TRUE; bHealthy_AT_201C : BOOL := TRUE;
    bHealthy_AT_202A : BOOL := TRUE; bHealthy_AT_202B : BOOL := TRUE; bHealthy_AT_202C : BOOL := TRUE;
    bHealthy_PT_203A : BOOL := TRUE; bHealthy_PT_203B : BOOL := TRUE; bHealthy_PT_203C : BOOL := TRUE;
    bHealthy_FT_204A : BOOL := TRUE; bHealthy_FT_204B : BOOL := TRUE; bHealthy_FT_204C : BOOL := TRUE;
    bHealthy_PT_301A : BOOL := TRUE; bHealthy_PT_301B : BOOL := TRUE; bHealthy_PT_301C : BOOL := TRUE;
    bHealthy_TT_302A : BOOL := TRUE; bHealthy_TT_302B : BOOL := TRUE; bHealthy_TT_302C : BOOL := TRUE;
    bHealthy_LT_303A : BOOL := TRUE; bHealthy_LT_303B : BOOL := TRUE; bHealthy_LT_303C : BOOL := TRUE;
    bHealthy_FT_304A : BOOL := TRUE; bHealthy_FT_304B : BOOL := TRUE; bHealthy_FT_304C : BOOL := TRUE;
    bHealthy_TT_401A : BOOL := TRUE; bHealthy_TT_401B : BOOL := TRUE; bHealthy_TT_401C : BOOL := TRUE;
    bHealthy_FT_501A : BOOL := TRUE; bHealthy_FT_501B : BOOL := TRUE; bHealthy_FT_501C : BOOL := TRUE;
    bHealthy_TT_502A : BOOL := TRUE; bHealthy_TT_502B : BOOL := TRUE; bHealthy_TT_502C : BOOL := TRUE;
    bHealthy_LT_601A : BOOL := TRUE; bHealthy_LT_601B : BOOL := TRUE; bHealthy_LT_601C : BOOL := TRUE;
    bHealthy_FT_602A : BOOL := TRUE; bHealthy_FT_602B : BOOL := TRUE; bHealthy_FT_602C : BOOL := TRUE;

    (* 2oo3 TMR Pairwise Discrepancy Debounce Timers [s] *)
    rTimer_Disc_01 : REAL := 0.0; rTimer_Disc_02 : REAL := 0.0; rTimer_Disc_03 : REAL := 0.0; rTimer_Disc_04 : REAL := 0.0;
    rTimer_Disc_05 : REAL := 0.0; rTimer_Disc_06 : REAL := 0.0; rTimer_Disc_07 : REAL := 0.0; rTimer_Disc_08 : REAL := 0.0;
    rTimer_Disc_09 : REAL := 0.0; rTimer_Disc_10 : REAL := 0.0; rTimer_Disc_11 : REAL := 0.0; rTimer_Disc_12 : REAL := 0.0;
    rTimer_Disc_13 : REAL := 0.0; rTimer_Disc_14 : REAL := 0.0; rTimer_Disc_15 : REAL := 0.0; rTimer_Disc_16 : REAL := 0.0;

    (* 2oo3 TMR Intermediates for Pairwise Deltas & Channel Health Counters *)
    rDelta_AB : REAL := 0.0;
    rDelta_BC : REAL := 0.0;
    rDelta_CA : REAL := 0.0;
    iHealthyCount : INT := 3;

    (* Rate-of-Change Tracking Historical Variables *)
    rPrev_TT_102                      : REAL := 368.5;
    rPrev_PT_301                      : REAL := 1.48;
    rPrev_LT_303                      : REAL := 52.5;
    rPrev_LT_601                      : REAL := 48.0;
    rROC_TT_102                       : REAL := 0.0;
    rROC_PT_301                       : REAL := 0.0;
    rROC_LT_303                       : REAL := 0.0;
    rROC_LT_601                       : REAL := 0.0;

    (* 8x8 State-Space Matrices & Vectors (Ts = 0.1 s) *)
    rMatrixA                          : ARRAY[1..8, 1..8] OF REAL;
    rMatrixB                          : ARRAY[1..8, 1..8] OF REAL;
    rMatrixC                          : ARRAY[1..8, 1..8] OF REAL;
    rMatrixD                          : ARRAY[1..8, 1..8] OF REAL;
    rMatrixQ                          : ARRAY[1..8, 1..8] OF REAL;
    rMatrixR                          : ARRAY[1..8, 1..8] OF REAL;
    rMatrixS                          : ARRAY[1..8, 1..8] OF REAL;
    rMatrixP                          : ARRAY[1..8, 1..8] OF REAL;
    rState_x                          : ARRAY[1..8] OF REAL;
    rState_x_pred                     : ARRAY[1..8] OF REAL;
    rControl_u                        : ARRAY[1..8] OF REAL;
    rControl_u_prev                   : ARRAY[1..8] OF REAL;
    rDelta_u                          : ARRAY[1..8] OF REAL;
    rGrad_g                           : ARRAY[1..8] OF REAL;
    rHessian_H                        : ARRAY[1..8, 1..8] OF REAL;
    rU_min                            : ARRAY[1..8] OF REAL;
    rU_max                            : ARRAY[1..8] OF REAL;
    rDeltaU_max                       : ARRAY[1..8] OF REAL;
    bMPC_Initialized                  : BOOL := FALSE;

    (* Iteration & Matrix Arithmetic Indices *)
    iRow                              : INT := 1;
    iCol                              : INT := 1;
    iIter                             : INT := 1;
    kIdx                              : INT := 1;
    rStepSize_gamma                   : REAL := 0.015;
    rCandidate_u                      : REAL := 0.0;
    rCostStateTerm                    : REAL := 0.0;
    rCostInputTerm                    : REAL := 0.0;
    rCostSlewTerm                     : REAL := 0.0;
    rCostTerminalTerm                 : REAL := 0.0;

    (* Combustion & Fired Heater Observer Variables *)
    rAirStoicRatio                    : REAL := 16.5;     (* kg air / kg fuel *)
    rAirTheoRate_kgh                  : REAL := 0.0;
    rExcessAirMultiplier              : REAL := 1.15;
    rAirActualRate_kgh                : REAL := 0.0;
    rFlueGasRate_kgh                  : REAL := 0.0;
    rFlueGasCp_kJkgK                  : REAL := 1.12;     (* kJ/kg.K *)
    rStackTemp_DegC                   : REAL := 175.0;
    rFiredDuty_MW                     : REAL := 0.0;
    rAbsorbedDuty_MW                  : REAL := 0.0;
    rCrudeCp_kJkgK                    : REAL := 2.45;     (* kJ/kg.K *)
    rCrudeInletTemp_DegC              : REAL := 285.0;    (* After preheat train *)
    rCrudeDensity_kgm3                : REAL := 845.0;    (* 32.5 API crude *)
    rCrossLimitFuelGas_pct            : REAL := 0.0;
    rCrossLimitAirDamper_pct          : REAL := 0.0;

    (* VLE & Column Hydraulics Intermediates *)
    rVaporFraction_e                  : REAL := 0.58;     (* Flash zone vapor fraction *)
    rFlashZoneVapor_m3h               : REAL := 0.0;
    rCalculatedOverflash_m3h          : REAL := 0.0;
    rColumnArea_m2                    : REAL := 56.74;    (* 8.5 m ID *)
    rActiveBubblingArea_m2            : REAL := 45.40;
    rLiquidDensity_kgm3               : REAL := 740.0;    (* Diesel cut at tray 20 *)
    rVaporDensity_kgm3                : REAL := 4.80;     (* Vapor at tray 20 *)
    rSurfaceTension_mNm               : REAL := 18.5;     (* mN/m *)
    rInternalLiquidFlow_kgs           : REAL := 0.0;
    rInternalVaporFlow_kgs            : REAL := 0.0;
    rFlowParameter_Flv                : REAL := 0.0;
    rCapacityFactor_Csb               : REAL := 0.0;
    rFloodingVelocity_ms              : REAL := 0.0;
    rActualVaporVelocity_ms           : REAL := 0.0;
    rDryTrayDrop_mmH2O                : REAL := 42.0;
    rWeirHead_mmH2O                   : REAL := 28.5;

    (* Desalter Electrostatic Observer Variables *)
    rGridImpedance_Ohms               : REAL := 0.0;
    rGridResistance_Ohms              : REAL := 0.0;
    rGridReactance_Ohms               : REAL := 0.0;
    rDesalterTripTimer_s              : REAL := 0.0;

    (* FSM Operational State Tracking *)
    iState                            : INT := 0;
    iPreviousState                    : INT := 0;
    rStateTimer_s                     : REAL := 0.0;
    rPurgeTimer_s                     : REAL := 0.0;
    rWarmupRampTimer_s                : REAL := 0.0;
    rDecokingAirSteamTimer_s          : REAL := 0.0;
    bPurgeComplete                    : BOOL := FALSE;
    bColdCirculationReady             : BOOL := FALSE;
    bFurnaceRampReady                 : BOOL := FALSE;
    bColumnRefluxEstablished          : BOOL := FALSE;
    bSideDrawsStabilized              : BOOL := FALSE;
    bPumparoundEngaged                : BOOL := FALSE;

    (* Constants *)
    PI_CONST                          : REAL := 3.141592653589793;
END_VAR
"""
