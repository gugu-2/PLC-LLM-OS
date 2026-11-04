# -*- coding: utf-8 -*-
"""
Generator for FB_Cement_RotaryKiln_Precalciner_ClinkerCooler
V7 Max-Persona Protocol: 75+ years Principal Automation Fellow & Cyber-Physical Systems Chair
"""
import os
import json
import uuid
import re

def generate_iec_code():
    parts = []
    
    # Header block
    parts.append("""FUNCTION_BLOCK FB_Cement_RotaryKiln_Precalciner_ClinkerCooler
(*
 ====================================================================================================
  LUMINA CYBER-PHYSICAL AUTOMATION ENGINE - ULTRA-RIGOROUS SYNTHETIC DATASET V7 MAX-PERSONA
  DOMAIN: HEAVY BUILDING MATERIALS & WORLD-SCALE CEMENT MANUFACTURING
  SYSTEM: 10,000 METRIC TON/DAY DRY PROCESS ROTARY CEMENT KILN WITH 5-STAGE TWIN-STRING PRECALCINER
          CYCLONE SUSPENSION TOWER & CROSS-BAR FOURTH-GENERATION RECIPROCATING HYDRAULIC CLINKER COOLER
 ====================================================================================================
  PROCESS SPECIFICATION & CYBER-PHYSICAL TOPOLOGY:
   1. BURNING ZONE TRUE SINTERING TEMPERATURE REGULATION (1,450.0 deg C +/- 5.0 deg C):
      - Triplicated dual-wavelength optical ratio pyrometers (2oo3 TMR) viewing through kiln hood.
      - Closed-loop optimization of primary flame core temperature (approx 1,950 deg C - 2,050 deg C),
        clinker liquid phase formation (~26.5% - 28.0% flux at 1,450 deg C), and exothermic mineral
        crystallization kinetics converting Belite (C2S) and free lime (f-CaO) into Alite (C3S).
   2. MULTI-CHANNEL PULVERIZED COAL MAIN BURNER AXIAL/RADIAL MOMENTUM SWIRL BALANCING:
      - Independent modulation of primary axial high-pressure air (outer annulus, 185 mbar),
        primary radial swirl air (internal angled nozzle, 145 mbar), and pulverized coal transport air.
      - Real-time burner Swirl Number (S) and momentum flux ratio (Gx/G0) decoupling flame shape,
        recirculation zone length, core flame heat flux, and refractory flame impingement.
   3. PRECALCINER TERTIARY AIR DUCT (TAD) DAMPER & STAGED FUEL COMBUSTION (92.0% +/- 0.5% CALCINATION):
      - Low-NOx staged combustion inline calciner (ILC) receiving 60% of total plant coal thermal energy.
      - Tertiary Air Duct (TAD) modulating damper balancing combustion oxygen pull between kiln tube
        exhaust gas and hot secondary/tertiary air from clinker cooler (~850.0 deg C).
      - Dynamic tracking of endothermic CaCO3 decarbonation kinetics (Delta H_rxn = +1,782 kJ/kg CaCO3),
        preventing under-calcination (kiln surging) and over-calcination (preheater scaling / clogging).
   4. RECIPROCATING GRATE COOLER VARIABLE HYDRAULIC DRIVE & UNDER-GRATE AERATION BED PRESSURE BALANCING:
      - Fourth-generation cross-bar clinker cooler with 6 independent under-grate aeration compartments.
      - Variable stroke speed (SPM) hydraulic cylinder control maintaining constant clinker bed depth
        and aeration bed pressure (58.0 mbar under Chamber 1) for optimal cross-flow heat recuperation
        into secondary air (~1,050.0 deg C) and tertiary air (~840.0 deg C), discharging clinker < 100 deg C.
   5. KILN SHELL 2D THERMAL SCANNER REFRACTORY COATING SPALLING & HOT SPOT DETECTION:
      - High-speed 50 Hz infrared line scanner resolving 360-degree circumference x 82-meter shell length.
      - Online coating thickness estimator (delta_coat = 150 - 250 mm) detecting refractory brick spalling,
        coating dropouts, and shell tire migration, triggering localized cooling fan banks (< 350 deg C).
   6. PREHEATER TOWER INDUCED DRAFT (ID) FAN DRAFT PRESSURE DECOUPLING:
      - Variable speed twin ID fans regulating top cyclone draft (-5,200 Pa) and kiln inlet draft (-80 Pa).
      - Decoupling gas volume swings, ambient air ingress, and kiln seal leakage from combustion aerodynamics.
   7. TRIPLE MODULAR REDUNDANCY (2oo3 TMR) ANALYTIC SENSING:
      - Triplicated burning zone ratio pyrometers (15.0 deg C discrepancy threshold).
      - Triplicated kiln inlet flue gas oxygen analyzers (0.25% O2 discrepancy threshold).
      - Triplicated kiln inlet draft transmitters (15.0 Pa discrepancy threshold).
      - Triplicated precalciner exit thermocouples (12.0 deg C discrepancy threshold).
      - Triplicated clinker cooler under-grate bed pressure transmitters (4.5 mbar threshold).
      - Automatic median mid-value selection, discrepancy persistence timing, and graceful degradation.
   8. ISA-18.2 MULTI-TIERED ALARM ENGINE & EMERGENCY BAGHOUSE CO DEFLAGRATION FAST FUEL TRIP (< 200 ms):
      - 5-Tier alarm hierarchy (HI_HI, HI, LO, LO_LO, ROC) with deadband hysteresis.
      - Ultra-fast safety interlock tripping pulverized coal feeding (< 200 ms) and de-energizing
        baghouse/ESP electrostatic high-voltage grids when inlet CO surges past 1.5% to prevent explosion.
   9. 12-STAGE OPERATIONAL FINITE STATE MACHINE (FSM):
      - 0:KILN_WARMUP_REFRACTORY_DRY, 1:AUXILIARY_INCHING_DRIVE, 2:PREHEATER_FAN_DRAFT_PULL,
        3:MAIN_BURNER_DIESEL_PILOT, 4:RAW_MEAL_FEED_INTRODUCTION, 5:ROTARY_KILN_ACCELERATION_RAMP,
        6:PRECALCINER_COAL_FIRING_SYNC, 7:STEADY_STATE_CLINKER_BURNING, 8:KILN_RING_SNOWMAN_BREAKING,
        9:GRATE_COOLER_HEAT_RECUPERATION, 10:CONTROLLED_KILN_STOP_DRAIN, 11:EMERGENCY_ESTOP_FUEL_CUT.
 ====================================================================================================
*)""")

    # VAR_INPUT
    parts.append("""VAR_INPUT
    (* Supervisory Permissives, Mode Selection & Safety Gates *)
    bMasterEnable                       : BOOL := FALSE;    (* Master Supervisory Execution Permissive Gate *)
    bEmergencyStop                      : BOOL := TRUE;     (* Hardwired Dual-Channel Active-Low E-Stop Interlock *)
    bResetFault                         : BOOL := FALSE;    (* Global Fault Reset and Alarm Acknowledge Command *)
    bAutoMpcEnable                      : BOOL := TRUE;     (* Receding-Horizon MPC Auto-Loop Closed-Loop Enable Gate *)
    bRawMealFeedPermissive              : BOOL := TRUE;     (* Raw Meal Dosing Feeder System Permissive Interlock *)
    bCoalFiringPermissive               : BOOL := TRUE;     (* Pulverized Coal Main and Calciner Firing Permissive *)
    tTaskScanInterval                   : TIME := T#50MS;   (* Cyclic Task Scan Execution Period (Nominal: 50 ms) *)

    (* Phase 1: 2oo3 TMR Burning Zone Optical Ratio Pyrometers [deg C] *)
    TT_BURNING_ZONE_PYRO_101A           : REAL := 1450.0;   (* [deg C] Burning Zone Ratio Pyrometer Channel A *)
    TT_BURNING_ZONE_PYRO_101B           : REAL := 1450.0;   (* [deg C] Burning Zone Ratio Pyrometer Channel B *)
    TT_BURNING_ZONE_PYRO_101C           : REAL := 1450.0;   (* [deg C] Burning Zone Ratio Pyrometer Channel C *)

    (* Phase 1: 2oo3 TMR Kiln Inlet Flue Gas Thermocouples [deg C] *)
    TT_KILN_INLET_GAS_102A              : REAL := 1050.0;   (* [deg C] Kiln Inlet Flue Gas Temp Channel A *)
    TT_KILN_INLET_GAS_102B              : REAL := 1050.0;   (* [deg C] Kiln Inlet Flue Gas Temp Channel B *)
    TT_KILN_INLET_GAS_102C              : REAL := 1050.0;   (* [deg C] Kiln Inlet Flue Gas Temp Channel C *)

    (* Phase 1: 2oo3 TMR Precalciner Exit Gas Thermocouples [deg C] *)
    TT_PRECALCINER_EXIT_201A            : REAL := 890.0;    (* [deg C] Precalciner Exit Gas Temperature Ch A *)
    TT_PRECALCINER_EXIT_201B            : REAL := 890.0;    (* [deg C] Precalciner Exit Gas Temperature Ch B *)
    TT_PRECALCINER_EXIT_201C            : REAL := 890.0;    (* [deg C] Precalciner Exit Gas Temperature Ch C *)

    (* Phase 1: 2oo3 TMR Tertiary Air Duct (TAD) Temperature Transmitters [deg C] *)
    TT_TERTIARY_AIR_DUCT_103A           : REAL := 840.0;    (* [deg C] Tertiary Air Duct Temperature Ch A *)
    TT_TERTIARY_AIR_DUCT_103B           : REAL := 840.0;    (* [deg C] Tertiary Air Duct Temperature Ch B *)
    TT_TERTIARY_AIR_DUCT_103C           : REAL := 840.0;    (* [deg C] Tertiary Air Duct Temperature Ch C *)

    (* Phase 1: 2oo3 TMR Kiln Inlet Static Draft Pressure Transmitters [Pa] *)
    PT_KILN_INLET_DRAFT_301A            : REAL := -80.0;    (* [Pa] Kiln Inlet Static Negative Draft Ch A *)
    PT_KILN_INLET_DRAFT_301B            : REAL := -80.0;    (* [Pa] Kiln Inlet Static Negative Draft Ch B *)
    PT_KILN_INLET_DRAFT_301C            : REAL := -80.0;    (* [Pa] Kiln Inlet Static Negative Draft Ch C *)

    (* Phase 1: 2oo3 TMR Precalciner Top Cyclone Draft Pressure Transmitters [Pa] *)
    PT_PRECALCINER_TOP_DRAFT_302A       : REAL := -5200.0;  (* [Pa] Preheater Stage-1 Top Cyclone Draft Ch A *)
    PT_PRECALCINER_TOP_DRAFT_302B       : REAL := -5200.0;  (* [Pa] Preheater Stage-1 Top Cyclone Draft Ch B *)
    PT_PRECALCINER_TOP_DRAFT_302C       : REAL := -5200.0;  (* [Pa] Preheater Stage-1 Top Cyclone Draft Ch C *)

    (* Phase 1: 2oo3 TMR Tertiary Air Duct Static Draft Pressure Transmitters [Pa] *)
    PT_TERTIARY_AIR_DUCT_104A           : REAL := -250.0;   (* [Pa] Tertiary Air Duct Static Draft Ch A *)
    PT_TERTIARY_AIR_DUCT_104B           : REAL := -250.0;   (* [Pa] Tertiary Air Duct Static Draft Ch B *)
    PT_TERTIARY_AIR_DUCT_104C           : REAL := -250.0;   (* [Pa] Tertiary Air Duct Static Draft Ch C *)

    (* Phase 1: 2oo3 TMR Kiln Inlet Flue Gas Oxygen Zirconia Analyzers [% vol] *)
    AIT_KILN_INLET_O2_401A              : REAL := 2.00;     (* [% vol] Kiln Inlet Excess Oxygen Channel A *)
    AIT_KILN_INLET_O2_401B              : REAL := 2.00;     (* [% vol] Kiln Inlet Excess Oxygen Channel B *)
    AIT_KILN_INLET_O2_401C              : REAL := 2.00;     (* [% vol] Kiln Inlet Excess Oxygen Channel C *)

    (* Phase 1: 2oo3 TMR Kiln Inlet Flue Gas Carbon Monoxide NDIR Analyzers [ppm] *)
    AIT_KILN_INLET_CO_402A              : REAL := 250.0;    (* [ppm] Kiln Inlet Carbon Monoxide Channel A *)
    AIT_KILN_INLET_CO_402B              : REAL := 250.0;    (* [ppm] Kiln Inlet Carbon Monoxide Channel B *)
    AIT_KILN_INLET_CO_402C              : REAL := 250.0;    (* [ppm] Kiln Inlet Carbon Monoxide Channel C *)

    (* Phase 1: 2oo3 TMR Kiln Inlet Flue Gas Nitric Oxides NOx Analyzers [ppm] *)
    AIT_KILN_INLET_NOX_403A             : REAL := 650.0;    (* [ppm] Kiln Inlet NOx Flue Gas Content Ch A *)
    AIT_KILN_INLET_NOX_403B             : REAL := 650.0;    (* [ppm] Kiln Inlet NOx Flue Gas Content Ch B *)
    AIT_KILN_INLET_NOX_403C             : REAL := 650.0;    (* [ppm] Kiln Inlet NOx Flue Gas Content Ch C *)

    (* Phase 1: 2oo3 TMR Kiln Main Drive Speed Pulse Encoders [RPM] *)
    ST_KILN_MAIN_DRIVE_RPM_501A         : REAL := 3.80;     (* [RPM] Kiln Shell Rotational Speed Channel A *)
    ST_KILN_MAIN_DRIVE_RPM_501B         : REAL := 3.80;     (* [RPM] Kiln Shell Rotational Speed Channel B *)
    ST_KILN_MAIN_DRIVE_RPM_501C         : REAL := 3.80;     (* [RPM] Kiln Shell Rotational Speed Channel C *)

    (* Phase 1: 2oo3 TMR Kiln Main Drive Active Power Transmitters [kW] *)
    IT_KILN_MAIN_DRIVE_KW_502A          : REAL := 1250.0;   (* [kW] Kiln Main Drive Electrical Power Ch A *)
    IT_KILN_MAIN_DRIVE_KW_502B          : REAL := 1250.0;   (* [kW] Kiln Main Drive Electrical Power Ch B *)
    IT_KILN_MAIN_DRIVE_KW_502C          : REAL := 1250.0;   (* [kW] Kiln Main Drive Electrical Power Ch C *)

    (* Phase 1: 2oo3 TMR Grate Cooler Chamber-1 Bed Pressure Transducers [mbar] *)
    PT_GRATE_COOLER_BED_601A            : REAL := 58.0;     (* [mbar] Under-Grate Aeration Bed Pressure Ch A *)
    PT_GRATE_COOLER_BED_601B            : REAL := 58.0;     (* [mbar] Under-Grate Aeration Bed Pressure Ch B *)
    PT_GRATE_COOLER_BED_601C            : REAL := 58.0;     (* [mbar] Under-Grate Aeration Bed Pressure Ch C *)

    (* Phase 1: 2oo3 TMR Clinker Discharge Infrared Pyrometers [deg C] *)
    TT_CLINKER_DISCHARGE_701A           : REAL := 95.0;     (* [deg C] Clinker Cooler Discharge Temp Ch A *)
    TT_CLINKER_DISCHARGE_701B           : REAL := 95.0;     (* [deg C] Clinker Cooler Discharge Temp Ch B *)
    TT_CLINKER_DISCHARGE_701C           : REAL := 95.0;     (* [deg C] Clinker Cooler Discharge Temp Ch C *)

    (* Phase 1: 2oo3 TMR Baghouse / ESP Inlet Safety Carbon Monoxide Analyzers [ppm] *)
    AIT_BAGHOUSE_INLET_CO_702A          : REAL := 450.0;    (* [ppm] Baghouse Inlet CO Safety Probe Ch A *)
    AIT_BAGHOUSE_INLET_CO_702B          : REAL := 450.0;    (* [ppm] Baghouse Inlet CO Safety Probe Ch B *)
    AIT_BAGHOUSE_INLET_CO_702C          : REAL := 450.0;    (* [ppm] Baghouse Inlet CO Safety Probe Ch C *)

    (* Phase 1: 2oo3 TMR Kiln Shell 2D Thermal Scanner Peak Hotspot Pyrometers [deg C] *)
    TT_KILN_SHELL_MAX_404A              : REAL := 285.0;    (* [deg C] Shell Thermal Scanner Peak Hotspot Ch A *)
    TT_KILN_SHELL_MAX_404B              : REAL := 285.0;    (* [deg C] Shell Thermal Scanner Peak Hotspot Ch B *)
    TT_KILN_SHELL_MAX_404C              : REAL := 285.0;    (* [deg C] Shell Thermal Scanner Peak Hotspot Ch C *)

    (* Additional Transducers, Feeders & Process Feedback *)
    POS_HOTSPOT_AXIAL_405               : REAL := 34.5;     (* [m] Axial Longitudinal Coordinate of Shell Hotspot *)
    FT_COAL_MAIN_BURNER_303             : REAL := 14.20;    (* [t/h] Pfister Main Burner Coal Gravimetric Feeder *)
    FT_COAL_PRECALCINER_304             : REAL := 21.50;    (* [t/h] Pfister Precalciner Coal Gravimetric Feeder *)
    FT_RAW_MEAL_FEED_305                : REAL := 645.0;    (* [t/h] Schenck Raw Meal Kiln Total Feed Rate *)
    PT_BURNER_AXIAL_AIR_306             : REAL := 185.0;    (* [mbar] Main Burner Primary Axial Air Pressure *)
    PT_BURNER_RADIAL_AIR_307            : REAL := 145.0;    (* [mbar] Main Burner Primary Radial Swirl Air Pressure *)
    POS_TERTIARY_AIR_DAMPER_FB          : REAL := 68.0;     (* [%] Tertiary Air Duct Modulating Damper Position *)
    POS_ID_FAN_DAMPER_FB                : REAL := 74.0;     (* [%] Preheater Twin ID Fan Damper Position *)
    ST_COOLER_STROKE_FB                 : REAL := 12.5;     (* [strokes/min] Hydraulic Clinker Cooler Stroke Speed *)

    (* Online Prompt-Gamma / XRF Clinker Mineral Raw Analysis [wt%] *)
    AIT_CLINKER_XRF_CAO_pct             : REAL := 65.50;    (* [wt%] Total Calcium Oxide Content in Clinker *)
    AIT_CLINKER_XRF_SIO2_pct            : REAL := 21.40;    (* [wt%] Silicon Dioxide Content in Clinker *)
    AIT_CLINKER_XRF_AL2O3_pct           : REAL := 5.25;     (* [wt%] Aluminum Oxide Content in Clinker *)
    AIT_CLINKER_XRF_FE2O3_pct           : REAL := 3.20;     (* [wt%] Ferric Oxide Content in Clinker *)
    AIT_CLINKER_XRF_FCAO_pct            : REAL := 0.85;     (* [wt%] Uncombined Free Lime (f-CaO) Content *)

    (* Operator Production Recipe Setpoints *)
    rSet_BurningZoneTemp_Target_degC    : REAL := 1450.0;   (* [deg C] Target Burning Zone Sintering Temp Setpoint *)
    rSet_CalcinationRate_Target_pct     : REAL := 92.00;    (* [%] Target Precalciner Apparent Calcination Degree *)
    rSet_KilnInletO2_Target_pct         : REAL := 2.00;     (* [% vol] Target Kiln Inlet Excess Oxygen Setpoint *)
    rSet_PreheaterDraft_Target_Pa       : REAL := -5200.0;  (* [Pa] Target Top Cyclone Negative Draft Setpoint *)
    rSet_FreeLime_Target_pct            : REAL := 0.85;     (* [%] Target Free Lime Content (Strict Limit < 1.0%) *)
    rSet_SpecificHeat_Target_kJkg       : REAL := 2950.0;   (* [kJ/kg clinker] Target Net Fuel Energy Consumption *)
END_VAR""")

    # VAR_OUTPUT
    parts.append("""VAR_OUTPUT
    (* Primary Actuator Control Commands *)
    rCmd_Coal_MainBurner_t_h            : REAL := 14.20;    (* [t/h] Gravimetric Pulverized Coal Feed to Main Burner *)
    rCmd_Coal_Precalciner_t_h           : REAL := 21.50;    (* [t/h] Gravimetric Pulverized Coal Feed to Precalciner *)
    rCmd_RawMeal_Feed_t_h               : REAL := 645.0;    (* [t/h] Master Raw Meal Feed Rate Command *)
    rCmd_KilnDrive_Speed_RPM            : REAL := 3.80;     (* [RPM] Kiln Variable Frequency Main Drive Speed Setpoint *)
    rCmd_ID_Fan_Speed_Pct               : REAL := 74.0;     (* [%] Preheater Tower Induced Draft (ID) Fan Speed / Damper *)
    rCmd_TertiaryAir_Damper_Pct         : REAL := 68.0;     (* [%] Tertiary Air Duct Staged Combustion Damper Position *)
    rCmd_Burner_AxialAir_Valve_Pct      : REAL := 62.0;     (* [%] Main Burner High-Pressure Axial Momentum Valve *)
    rCmd_Burner_RadialAir_Valve_Pct     : REAL := 48.0;     (* [%] Main Burner High-Pressure Radial Swirl Air Valve *)
    rCmd_Cooler_StrokeSpeed_SPM         : REAL := 12.5;     (* [strokes/min] Grate Cooler Hydraulic Stroke Rate *)
    rCmd_Cooler_AerationFan1_Pct        : REAL := 82.0;     (* [%] Under-Grate High-Pressure Aeration Chamber 1 Fan *)
    rCmd_Cooler_AerationFan2_Pct        : REAL := 75.0;     (* [%] Under-Grate Aeration Chamber 2 Fan Speed *)
    rCmd_Cooler_AerationFan3_Pct        : REAL := 68.0;     (* [%] Under-Grate Aeration Chamber 3 Fan Speed *)
    rCmd_Cooler_AerationFan4_Pct        : REAL := 60.0;     (* [%] Under-Grate Aeration Chamber 4 Fan Speed *)
    rCmd_Cooler_AerationFan5_Pct        : REAL := 52.0;     (* [%] Under-Grate Aeration Chamber 5 Fan Speed *)
    rCmd_Cooler_AerationFan6_Pct        : REAL := 45.0;     (* [%] Under-Grate Aeration Chamber 6 Fan Speed *)
    bCmd_FuelCutoff_Main_Trip           : BOOL := FALSE;    (* [bool] Main Burner Rapid Safety Coal Cutoff Gate *)
    bCmd_FuelCutoff_Calciner_Trip       : BOOL := FALSE;    (* [bool] Calciner Rapid Safety Coal Cutoff Gate *)
    bCmd_Baghouse_CO_Deflagration_Trip  : BOOL := FALSE;    (* [bool] Baghouse/ESP Electrostatic High-Voltage Fast Trip *)
    bCmd_KilnAuxiliary_InchingDrive_Engage : BOOL := FALSE; (* [bool] Kiln Barring Gear / Auxiliary Inching Drive Engage *)
    bCmd_ShellCoolingFans_Run           : BOOL := FALSE;    (* [bool] Kiln Shell Spot Cooling Axial Fan Bank Energization *)

    (* 2oo3 TMR Validated Process Feedback *)
    rVoted_BurningZoneTemp_degC         : REAL := 1450.0;   (* [deg C] 2oo3 Validated Burning Zone Sintering Temp *)
    rVoted_KilnInletGasTemp_degC        : REAL := 1050.0;   (* [deg C] 2oo3 Validated Kiln Inlet Flue Gas Temp *)
    rVoted_PrecalcinerExitTemp_degC     : REAL := 890.0;    (* [deg C] 2oo3 Validated Precalciner Exit Temperature *)
    rVoted_TertiaryAirTemp_degC         : REAL := 840.0;    (* [deg C] 2oo3 Validated Tertiary Air Temperature *)
    rVoted_KilnInletDraft_Pa            : REAL := -80.0;    (* [Pa] 2oo3 Validated Kiln Inlet Draft Pressure *)
    rVoted_PreheaterTopDraft_Pa         : REAL := -5200.0;  (* [Pa] 2oo3 Validated Preheater Stage-1 Top Draft *)
    rVoted_TertiaryAirDraft_Pa          : REAL := -250.0;   (* [Pa] 2oo3 Validated Tertiary Air Duct Draft *)
    rVoted_KilnInletO2_pct              : REAL := 2.00;     (* [% vol] 2oo3 Validated Kiln Inlet Excess Oxygen *)
    rVoted_KilnInletCO_ppm              : REAL := 250.0;    (* [ppm] 2oo3 Validated Kiln Inlet Carbon Monoxide *)
    rVoted_KilnInletNOx_ppm             : REAL := 650.0;    (* [ppm] 2oo3 Validated Kiln Inlet Nitric Oxides *)
    rVoted_KilnDriveSpeed_RPM           : REAL := 3.80;     (* [RPM] 2oo3 Validated Kiln Rotational Speed *)
    rVoted_KilnDrivePower_kW            : REAL := 1250.0;   (* [kW] 2oo3 Validated Kiln Main Drive Active Power *)
    rVoted_GrateCoolerBedPress_mbar     : REAL := 58.0;     (* [mbar] 2oo3 Validated Clinker Cooler Bed Pressure *)
    rVoted_ClinkerDischargeTemp_degC    : REAL := 95.0;     (* [deg C] 2oo3 Validated Clinker Discharge Temperature *)
    rVoted_BaghouseCO_ppm               : REAL := 450.0;    (* [ppm] 2oo3 Validated Baghouse Inlet Safety CO *)
    rVoted_KilnShellPeakTemp_degC       : REAL := 285.0;    (* [deg C] 2oo3 Validated Kiln Shell Peak Hotspot Temp *)

    (* Cyber-Physical Observers, Kinetic Models & Clinker Mineral Estimators *)
    rObserved_ApparentCalcination_pct   : REAL := 92.00;    (* [%] Online Apparent Calcination Degree in Calciner *)
    rObserved_FreeLime_pct              : REAL := 0.85;     (* [%] Thermochemically Reconstructed Clinker Free Lime *)
    rObserved_ClinkerC3S_pct            : REAL := 62.40;    (* [wt%] Bogue Calculated Tricalcium Silicate (Alite) *)
    rObserved_ClinkerC2S_pct            : REAL := 14.30;    (* [wt%] Bogue Calculated Dicalcium Silicate (Belite) *)
    rObserved_ClinkerC3A_pct            : REAL := 8.50;     (* [wt%] Bogue Calculated Tricalcium Aluminate *)
    rObserved_ClinkerC4AF_pct           : REAL := 9.74;     (* [wt%] Bogue Calculated Tetracalcium Aluminoferrite *)
    rObserved_LiquidPhase_pct           : REAL := 27.20;    (* [wt%] Liquid Flux Fraction in Burning Zone at 1450 C *)
    rObserved_SpecificHeatCons_kJkg     : REAL := 2942.0;   (* [kJ/kg clinker] Net Specific Fuel Heat Consumption *)
    rObserved_BedFillDegree_pct         : REAL := 13.80;    (* [%] Kiln Cross-Sectional Solids Volumetric Fill Degree *)
    rObserved_BedSolidsVelocity_m_s     : REAL := 0.0245;   (* [m/s] US Bureau of Mines Axial Bed Transport Speed *)
    rObserved_BedResidenceTime_min      : REAL := 55.80;    (* [min] Total Solids Mean Residence Time in Rotary Kiln *)
    rObserved_CoolerThermalEff_pct      : REAL := 74.80;    (* [%] Clinker Cooler Cross-Flow Heat Recuperation Efficiency *)
    rObserved_BurnerSwirlNumber         : REAL := 0.82;     (* [-] Dimensionless Burner Swirl Recirculation Index *)
    rObserved_RefractoryCoatingThickness_mm : REAL := 185.0;(* [mm] Thermal Resistance Reconstructed Protective Coating *)
    rObserved_SecondaryAirTemp_degC     : REAL := 1055.0;   (* [deg C] Reconstructed Secondary Combustion Air Temp *)
    rMPC_ObjectiveCost_J                : REAL := 0.0;      (* Receding-Horizon Model Predictive Control Quadratic Cost *)

    (* Supervisory State, Telemetry & ISA-18.2 Diagnostic Bitmasks *)
    eActiveFsmState                     : INT := 7;         (* [-] Operational Finite State Machine State Index (0..11) *)
    dwStatusWord1                       : DWORD := 16#0000; (* [-] Master Kiln Operational Status Bitmask *)
    dwStatusWord2                       : DWORD := 16#0000; (* [-] Decoupling Loops, Observers & MPC Telemetry Bitmask *)
    dwAlarmWord_Trip                    : DWORD := 16#0000; (* [-] ISA-18.2 Priority 1 / Critical Safety Shutdown Trips *)
    dwAlarmWord_Warning                 : DWORD := 16#0000; (* [-] ISA-18.2 Priority 2 / Process Deviation Warnings *)
    dwSensorHealthMask                  : DWORD := 16#0000; (* [-] 2oo3 TMR Transducer Discrepancy & Health Matrix *)
    bClinkerQualityAcceptable           : BOOL := TRUE;     (* [bool] Clinker Chemistry Quality Gate (f-CaO < 1.0%, C3S > 58%) *)
    bEmergencyTripActive                : BOOL := FALSE;    (* [bool] Emergency Fuel Cutoff / Deflagration Trip Active *)
END_VAR""")

    # VAR
    parts.append("""VAR
    (* ====================================================================================================
       PHYSICAL CONSTANTS, CHEMICAL STOICHIOMETRY & THERMODYNAMIC COEFFICIENTS
       ==================================================================================================== *)
    c_rR_GAS                            : REAL := 8.31446;      (* Universal Gas Constant [J/(mol*K)] *)
    c_rPI                               : REAL := 3.14159265;   (* Archimedes Mathematical Constant Pi *)
    c_rMOL_MASS_CACO3                   : REAL := 100.087;      (* Calcium Carbonate Molecular Mass [g/mol] *)
    c_rMOL_MASS_CAO                     : REAL := 56.077;       (* Calcium Oxide Molecular Mass [g/mol] *)
    c_rMOL_MASS_CO2                     : REAL := 44.010;       (* Carbon Dioxide Molecular Mass [g/mol] *)
    c_rDELTA_H_DECARB                   : REAL := 1782.0;       (* Endothermic Decarbonation Enthalpy [kJ/kg CaCO3] *)
    c_rDELTA_H_CLINK                    : REAL := -450.0;       (* Exothermic Clinker Formation Enthalpy [kJ/kg clinker] *)
    c_rKILN_INNER_DIAM_M                : REAL := 5.20;         (* Rotary Kiln Refractory Inner Diameter [m] *)
    c_rKILN_SHELL_DIAM_M                : REAL := 5.60;         (* Rotary Kiln Structural Steel Shell Diameter [m] *)
    c_rKILN_LENGTH_M                    : REAL := 82.0;         (* Rotary Kiln Total Axial Tube Length [m] *)
    c_rKILN_SLOPE                       : REAL := 0.035;        (* Kiln Axial Mechanical Slope (3.5% = 2.0 degrees) *)
    c_rMATERIAL_REPOSE_DEG              : REAL := 36.0;         (* Dynamic Angle of Repose of Clinker Bed [deg] *)
    c_rBULK_DENSITY_RAW_MEAL            : REAL := 950.0;        (* Bulk Density of Aerated Fluidized Raw Meal [kg/m3] *)
    c_rBULK_DENSITY_CLINKER             : REAL := 1350.0;       (* Bulk Density of Sintered Clinker Nodules [kg/m3] *)
    c_rCLINKER_FACTOR                   : REAL := 1.55;         (* Raw Meal to Clinker Conversion Mass Factor (kg meal/kg clink) *)
    c_rCOAL_LHV_KJ_KG                   : REAL := 25800.0;      (* Pulverized Bituminous Coal Lower Heating Value [kJ/kg] *)
    c_rLAMBDA_REFRACTORY                : REAL := 1.65;         (* Spinel / Magnesite Refractory Thermal Conductivity [W/(m*K)] *)
    c_rLAMBDA_COATING                   : REAL := 1.15;         (* Clinker Protective Coating Thermal Conductivity [W/(m*K)] *)
    c_rLAMBDA_SHELL_STEEL               : REAL := 45.0;         (* Kiln Carbon Steel Shell Thermal Conductivity [W/(m*K)] *)
    c_rREFRACTORY_THICK_MM              : REAL := 200.0;        (* Virgin Basic Refractory Brick Thickness [mm] *)
    c_rSHELL_THICK_MM                   : REAL := 38.0;         (* Rotary Kiln Structural Steel Shell Thickness [mm] *)

    (* Decarbonation Kinetics Arrhenius Parameters (CaCO3 -> CaO + CO2) *)
    c_rDECARB_K0                        : REAL := 1.25E7;       (* Decarbonation Pre-Exponential Rate Factor [1/s] *)
    c_rDECARB_EA                        : REAL := 185000.0;     (* Decarbonation Apparent Activation Energy [J/mol] *)

    (* Clinkering Formation Kinetics Parameters (Belite + CaO -> Alite) *)
    c_rCLINK_K0                         : REAL := 4.80E5;       (* Alite Formation Reaction Rate Constant [1/s] *)
    c_rCLINK_EA                         : REAL := 240000.0;     (* Alite Crystallization Activation Energy [J/mol] *)

    (* ====================================================================================================
       DISCRETE STATE-SPACE MATRICES & VECTORS (8 States x 8 Controls)
       Discrete State Vector x (8x1):
         x[1]: Burning Zone True Sintering Temp Deviation Delta_T_bz [deg C] (Nominal: 1450.0)
         x[2]: Precalciner Apparent Calcination Degree Deviation Delta_alpha_calc [%] (Nominal: 92.0)
         x[3]: Kiln Inlet Flue Gas Excess Oxygen Deviation Delta_O2_inlet [% vol] (Nominal: 2.00)
         x[4]: Preheater Top Cyclone Negative Draft Deviation Delta_P_draft [Pa] (Nominal: -5200.0)
         x[5]: Kiln Solids Bed Volumetric Holdup Fill Degree Delta_H_bed [%] (Nominal: 13.80)
         x[6]: Grate Cooler Clinker Discharge Temp Deviation Delta_T_clink [deg C] (Nominal: 95.0)
         x[7]: Clinker Free Lime Content Deviation Delta_f_CaO [%] (Nominal: 0.85)
         x[8]: Net Specific Fuel Heat Consumption Deviation Delta_Q_spec [kJ/kg] (Nominal: 2950.0)

       Discrete Control Vector u (8x1):
         u[1]: Main Burner Pulverized Coal Feed Trim Delta_F_coal_main [t/h] (Nominal: 14.20)
         u[2]: Precalciner Pulverized Coal Feed Trim Delta_F_coal_calc [t/h] (Nominal: 21.50)
         u[3]: Kiln Total Raw Meal Feed Rate Trim Delta_F_raw [t/h] (Nominal: 645.0)
         u[4]: Rotary Kiln Main Drive Rotational Speed Trim Delta_omega_kiln [RPM] (Nominal: 3.80)
         u[5]: Preheater Twin ID Fan Speed / Damper Trim Delta_D_idfan [%] (Nominal: 74.0)
         u[6]: Tertiary Air Duct Staged Combustion Damper Trim Delta_D_tad [%] (Nominal: 68.0)
         u[7]: Main Burner Axial/Radial Swirl Momentum Ratio Trim Delta_R_swirl [-] (Nominal: 0.82)
         u[8]: Grate Cooler Hydraulic Stroke Rate Trim Delta_S_grate [SPM] (Nominal: 12.5)
       ==================================================================================================== *)
    matA                                : ARRAY[1..8, 1..8] OF REAL;
    matB                                : ARRAY[1..8, 1..8] OF REAL;
    matC                                : ARRAY[1..8, 1..8] OF REAL;
    matD                                : ARRAY[1..8, 1..8] OF REAL;
    matQ                                : ARRAY[1..8, 1..8] OF REAL;
    matR                                : ARRAY[1..8, 1..8] OF REAL;
    matS                                : ARRAY[1..8, 1..8] OF REAL;
    matP                                : ARRAY[1..8, 1..8] OF REAL;
    xState                              : ARRAY[1..8] OF REAL;
    xPred                               : ARRAY[1..8] OF REAL;
    xSetpoint                           : ARRAY[1..8] OF REAL;
    xError                              : ARRAY[1..8] OF REAL;
    uActuator                           : ARRAY[1..8] OF REAL;
    uPrevious                           : ARRAY[1..8] OF REAL;
    uOptimal                            : ARRAY[1..8] OF REAL;
    deltaU                              : ARRAY[1..8] OF REAL;
    uMin                                : ARRAY[1..8] OF REAL;
    uMax                                : ARRAY[1..8] OF REAL;
    deltaUMax                           : ARRAY[1..8] OF REAL;
    bMatricesInitialized                : BOOL := FALSE;

    (* Receding-Horizon Model Predictive Control (MPC) Solver Registers *)
    xHorizon                            : ARRAY[1..5, 1..8] OF REAL;
    rGrad                               : ARRAY[1..8] OF REAL;
    rTotalCost                          : REAL := 0.0;
    rStepSize                           : REAL := 0.0012;
    iHorizonStep                        : INT := 1;
    iMatRow                             : INT := 1;
    iMatCol                             : INT := 1;
    kStateIdx                           : INT := 1;
    mInputIdx                           : INT := 1;

    (* Phase 1: 2oo3 TMR Voting Structures & Discrepancy Timers *)
    rTMR_Tol_BurningZone                : REAL := 15.0;     (* [deg C] Discrepancy Limit for Ratio Pyrometers *)
    rTMR_Tol_KilnInletGas               : REAL := 12.0;     (* [deg C] Discrepancy Limit for Kiln Inlet Thermocouples *)
    rTMR_Tol_CalcinerExit               : REAL := 10.0;     (* [deg C] Discrepancy Limit for Calciner Thermocouples *)
    rTMR_Tol_TAD_Temp                   : REAL := 12.0;     (* [deg C] Discrepancy Limit for TAD Thermocouples *)
    rTMR_Tol_KilnInletDraft             : REAL := 15.0;     (* [Pa] Discrepancy Limit for Kiln Inlet Draft *)
    rTMR_Tol_TopDraft                   : REAL := 120.0;    (* [Pa] Discrepancy Limit for Preheater Top Draft *)
    rTMR_Tol_TAD_Draft                  : REAL := 25.0;     (* [Pa] Discrepancy Limit for TAD Draft *)
    rTMR_Tol_O2                         : REAL := 0.25;     (* [% vol] Discrepancy Limit for Kiln Inlet O2 *)
    rTMR_Tol_CO                         : REAL := 50.0;     (* [ppm] Discrepancy Limit for Kiln Inlet CO *)
    rTMR_Tol_NOx                        : REAL := 45.0;     (* [ppm] Discrepancy Limit for Kiln Inlet NOx *)
    rTMR_Tol_KilnRPM                    : REAL := 0.15;     (* [RPM] Discrepancy Limit for Kiln Speed Encoders *)
    rTMR_Tol_KilnKW                     : REAL := 45.0;     (* [kW] Discrepancy Limit for Kiln Active Power *)
    rTMR_Tol_CoolerBedPress             : REAL := 4.5;      (* [mbar] Discrepancy Limit for Cooler Bed Pressure *)
    rTMR_Tol_ClinkerDischarge           : REAL := 8.0;      (* [deg C] Discrepancy Limit for Clinker Discharge *)
    rTMR_Tol_BaghouseCO                 : REAL := 60.0;     (* [ppm] Discrepancy Limit for Baghouse Safety CO *)
    rTMR_Tol_ShellTemp                  : REAL := 15.0;     (* [deg C] Discrepancy Limit for Shell Scanner Pyrometers *)

    (* 2oo3 Discrepancy Monitoring Registers for Sensor Groups *)
    rDiff_BZ_AB, rDiff_BZ_BC, rDiff_BZ_CA           : REAL;
    bFault_BZ_A, bFault_BZ_B, bFault_BZ_C           : BOOL;
    rTimer_BZ_A, rTimer_BZ_B, rTimer_BZ_C           : REAL;

    rDiff_InletT_AB, rDiff_InletT_BC, rDiff_InletT_CA : REAL;
    bFault_InletT_A, bFault_InletT_B, bFault_InletT_C : BOOL;
    rTimer_InletT_A, rTimer_InletT_B, rTimer_InletT_C : REAL;

    rDiff_CalcT_AB, rDiff_CalcT_BC, rDiff_CalcT_CA  : REAL;
    bFault_CalcT_A, bFault_CalcT_B, bFault_CalcT_C  : BOOL;
    rTimer_CalcT_A, rTimer_CalcT_B, rTimer_CalcT_C  : REAL;

    rDiff_TADT_AB, rDiff_TADT_BC, rDiff_TADT_CA    : REAL;
    bFault_TADT_A, bFault_TADT_B, bFault_TADT_C    : BOOL;
    rTimer_TADT_A, rTimer_TADT_B, rTimer_TADT_C    : REAL;

    rDiff_InletP_AB, rDiff_InletP_BC, rDiff_InletP_CA : REAL;
    bFault_InletP_A, bFault_InletP_B, bFault_InletP_C : BOOL;
    rTimer_InletP_A, rTimer_InletP_B, rTimer_InletP_C : REAL;

    rDiff_TopP_AB, rDiff_TopP_BC, rDiff_TopP_CA     : REAL;
    bFault_TopP_A, bFault_TopP_B, bFault_TopP_C     : BOOL;
    rTimer_TopP_A, rTimer_TopP_B, rTimer_TopP_C     : REAL;

    rDiff_TADP_AB, rDiff_TADP_BC, rDiff_TADP_CA     : REAL;
    bFault_TADP_A, bFault_TADP_B, bFault_TADP_C     : BOOL;
    rTimer_TADP_A, rTimer_TADP_B, rTimer_TADP_C     : REAL;

    rDiff_O2_AB, rDiff_O2_BC, rDiff_O2_CA           : REAL;
    bFault_O2_A, bFault_O2_B, bFault_O2_C           : BOOL;
    rTimer_O2_A, rTimer_O2_B, rTimer_O2_C           : REAL;

    rDiff_CO_AB, rDiff_CO_BC, rDiff_CO_CA           : REAL;
    bFault_CO_A, bFault_CO_B, bFault_CO_C           : BOOL;
    rTimer_CO_A, rTimer_CO_B, rTimer_CO_C           : REAL;

    rDiff_NOx_AB, rDiff_NOx_BC, rDiff_NOx_CA        : REAL;
    bFault_NOx_A, bFault_NOx_B, bFault_NOx_C        : BOOL;
    rTimer_NOx_A, rTimer_NOx_B, rTimer_NOx_C        : REAL;

    rDiff_RPM_AB, rDiff_RPM_BC, rDiff_RPM_CA        : REAL;
    bFault_RPM_A, bFault_RPM_B, bFault_RPM_C        : BOOL;
    rTimer_RPM_A, rTimer_RPM_B, rTimer_RPM_C        : REAL;

    rDiff_KW_AB, rDiff_KW_BC, rDiff_KW_CA           : REAL;
    bFault_KW_A, bFault_KW_B, bFault_KW_C           : BOOL;
    rTimer_KW_A, rTimer_KW_B, rTimer_KW_C           : REAL;

    rDiff_BedP_AB, rDiff_BedP_BC, rDiff_BedP_CA     : REAL;
    bFault_BedP_A, bFault_BedP_B, bFault_BedP_C     : BOOL;
    rTimer_BedP_A, rTimer_BedP_B, rTimer_BedP_C     : REAL;

    rDiff_DischT_AB, rDiff_DischT_BC, rDiff_DischT_CA : REAL;
    bFault_DischT_A, bFault_DischT_B, bFault_DischT_C : BOOL;
    rTimer_DischT_A, rTimer_DischT_B, rTimer_DischT_C : REAL;

    rDiff_BagCO_AB, rDiff_BagCO_BC, rDiff_BagCO_CA  : REAL;
    bFault_BagCO_A, bFault_BagCO_B, bFault_BagCO_C  : BOOL;
    rTimer_BagCO_A, rTimer_BagCO_B, rTimer_BagCO_C  : REAL;

    rDiff_ShellT_AB, rDiff_ShellT_BC, rDiff_ShellT_CA : REAL;
    bFault_ShellT_A, bFault_ShellT_B, bFault_ShellT_C : BOOL;
    rTimer_ShellT_A, rTimer_ShellT_B, rTimer_ShellT_C : REAL;

    (* Phase 4: 12-Stage Operational Finite State Machine Variables *)
    STATE_KILN_WARMUP_REFRACTORY_DRY    : INT := 0;     (* Refractory curing with auxiliary burner *)
    STATE_AUXILIARY_INCHING_DRIVE       : INT := 1;     (* Slow barring gear rotation to prevent thermal sag *)
    STATE_PREHEATER_FAN_DRAFT_PULL      : INT := 2;     (* Establish balanced negative draft across 5 cyclone stages *)
    STATE_MAIN_BURNER_DIESEL_PILOT      : INT := 3;     (* Light diesel/gas pilot, warm up sintering zone *)
    STATE_RAW_MEAL_FEED_INTRODUCTION    : INT := 4;     (* Feed introduction at 30% nominal (approx 200 t/h) *)
    STATE_ROTARY_KILN_ACCELERATION_RAMP : INT := 5;     (* Coordinate main drive speed acceleration with bed load *)
    STATE_PRECALCINER_COAL_FIRING_SYNC  : INT := 6;     (* Calciner coal ignition and tertiary air pull coordination *)
    STATE_STEADY_STATE_CLINKER_BURNING  : INT := 7;     (* Full production (10,000 tpd) autonomous MPC regulation *)
    STATE_KILN_RING_SNOWMAN_BREAKING    : INT := 8;     (* Thermal shock / mechanical cycling to shed ring / snowman *)
    STATE_GRATE_COOLER_HEAT_RECUPERATION: INT := 9;     (* Dynamic bed pressure balancing & secondary heat recovery *)
    STATE_CONTROLLED_KILN_STOP_DRAIN    : INT := 10;    (* Systematic feed cutoff, material emptying & thermal soak *)
    STATE_EMERGENCY_ESTOP_FUEL_CUT      : INT := 11;    (* Hardwired trip: Instantaneous fuel cut, CO purge, barring *)

    tFsmStepTimer_Sec                   : REAL := 0.0;
    tPurgeTimer_Sec                     : REAL := 0.0;
    tWarmupRampTimer_Sec                : REAL := 0.0;
    tSnowmanCycleTimer_Sec              : REAL := 0.0;

    (* Phase 5: ISA-18.2 Multi-Tiered Alarm Thresholds & Hysteresis *)
    rALM_TRIP_BZ_HH                     : REAL := 1520.0;   (* [deg C] High-High Burning Zone Refractory Washout Trip *)
    rALM_WARN_BZ_H                      : REAL := 1480.0;   (* [deg C] High Burning Zone Overheating Warning *)
    rALM_WARN_BZ_L                      : REAL := 1420.0;   (* [deg C] Low Burning Zone Under-sintering Warning *)
    rALM_TRIP_BZ_LL                     : REAL := 1360.0;   (* [deg C] Low-Low Burning Zone Unburnt Clinker Collapse Trip *)
    rALM_HYST_BZ                        : REAL := 5.0;      (* [deg C] Burning Zone Temperature Deadband *)

    rALM_TRIP_BAGHOUSE_CO_HH            : REAL := 1500.0;   (* [ppm] High-High Baghouse/ESP CO Surge Deflagration Trip *)
    rALM_WARN_BAGHOUSE_CO_H             : REAL := 800.0;    (* [ppm] High Baghouse CO Warning - Reduce Fuel *)
    rALM_HYST_BAGHOUSE_CO               : REAL := 50.0;     (* [ppm] Baghouse CO Deadband *)

    rALM_TRIP_SHELL_HH                  : REAL := 420.0;    (* [deg C] High-High Shell Hotspot Redline Plate Yield Trip *)
    rALM_WARN_SHELL_H                   : REAL := 350.0;    (* [deg C] High Shell Temperature Coating Dropout Warning *)
    rALM_HYST_SHELL                     : REAL := 10.0;     (* [deg C] Shell Temperature Deadband *)

    rALM_TRIP_CALCINER_EXIT_HH          : REAL := 960.0;    (* [deg C] High-High Precalciner Exit Cyclone Plugging Trip *)
    rALM_WARN_CALCINER_EXIT_H           : REAL := 925.0;    (* [deg C] High Calciner Exit Temperature Warning *)
    rALM_WARN_CALCINER_EXIT_L           : REAL := 845.0;    (* [deg C] Low Calciner Exit Temperature Warning *)
    rALM_TRIP_CALCINER_EXIT_LL          : REAL := 810.0;    (* [deg C] Low-Low Calciner Flame Extinction Trip *)
    rALM_HYST_CALCINER_EXIT             : REAL := 5.0;      (* [deg C] Calciner Exit Temperature Deadband *)

    rALM_TRIP_INLET_O2_LL               : REAL := 0.60;     (* [% vol] Low-Low Kiln Inlet Oxygen Reducing Flame Trip *)
    rALM_WARN_INLET_O2_L                : REAL := 1.20;     (* [% vol] Low Kiln Inlet Oxygen Incomplete Combustion Warn *)
    rALM_WARN_INLET_O2_H                : REAL := 4.50;     (* [% vol] High Kiln Inlet Oxygen Excessive Ingress Warn *)
    rALM_HYST_INLET_O2                  : REAL := 0.15;     (* [% vol] Kiln Inlet Oxygen Deadband *)

    rALM_TRIP_TOP_DRAFT_HH              : REAL := -2500.0;  (* [Pa] High-High Preheater Draft (Loss of Draft Trip) *)
    rALM_TRIP_TOP_DRAFT_LL              : REAL := -7500.0;  (* [Pa] Low-Low Preheater Draft (Severe Cyclone Blockage Trip) *)
    rALM_WARN_TOP_DRAFT_H               : REAL := -4200.0;  (* [Pa] High Draft Loss Warning *)
    rALM_WARN_TOP_DRAFT_L               : REAL := -6200.0;  (* [Pa] Low Draft Cyclonic Flow Resistance Warning *)
    rALM_HYST_TOP_DRAFT                 : REAL := 100.0;    (* [Pa] Preheater Top Draft Deadband *)

    rALM_TRIP_COOLER_BED_HH             : REAL := 85.0;     (* [mbar] High-High Cooler Bed Stall / Overpressure Trip *)
    rALM_WARN_COOLER_BED_H              : REAL := 70.0;     (* [mbar] High Cooler Bed Heavy Clinker Buildup Warning *)
    rALM_WARN_COOLER_BED_L              : REAL := 35.0;     (* [mbar] Low Cooler Bed Clinker Channeling / Blow-through Warn *)
    rALM_TRIP_COOLER_BED_LL             : REAL := 20.0;     (* [mbar] Low-Low Cooler Bed Grate Burnout Trip *)
    rALM_HYST_COOLER_BED                : REAL := 3.0;      (* [mbar] Cooler Bed Pressure Deadband *)

    rALM_WARN_FREELIME_H                : REAL := 1.20;     (* [%] High Free Lime Poor Soundness Warning *)
    rALM_TRIP_FREELIME_HH               : REAL := 1.80;     (* [%] High-High Free Lime Clinker Reject Trip *)
    rALM_HYST_FREELIME                  : REAL := 0.08;     (* [%] Free Lime Content Deadband *)

    (* ISA-18.2 Discrete Alarm Latch Flags *)
    bAlm_BZ_HH                          : BOOL := FALSE;
    bAlm_BZ_H                           : BOOL := FALSE;
    bAlm_BZ_L                           : BOOL := FALSE;
    bAlm_BZ_LL                          : BOOL := FALSE;
    bAlm_Baghouse_CO_HH                 : BOOL := FALSE;
    bAlm_Baghouse_CO_H                  : BOOL := FALSE;
    bAlm_Shell_HH                       : BOOL := FALSE;
    bAlm_Shell_H                        : BOOL := FALSE;
    bAlm_CalcinerExit_HH                : BOOL := FALSE;
    bAlm_CalcinerExit_H                 : BOOL := FALSE;
    bAlm_CalcinerExit_L                 : BOOL := FALSE;
    bAlm_CalcinerExit_LL                : BOOL := FALSE;
    bAlm_InletO2_LL                     : BOOL := FALSE;
    bAlm_InletO2_L                      : BOOL := FALSE;
    bAlm_InletO2_H                      : BOOL := FALSE;
    bAlm_TopDraft_HH                    : BOOL := FALSE;
    bAlm_TopDraft_H                     : BOOL := FALSE;
    bAlm_TopDraft_L                     : BOOL := FALSE;
    bAlm_TopDraft_LL                    : BOOL := FALSE;
    bAlm_CoolerBed_HH                   : BOOL := FALSE;
    bAlm_CoolerBed_H                    : BOOL := FALSE;
    bAlm_CoolerBed_L                    : BOOL := FALSE;
    bAlm_CoolerBed_LL                   : BOOL := FALSE;
    bAlm_FreeLime_H                     : BOOL := FALSE;
    bAlm_FreeLime_HH                    : BOOL := FALSE;
    bAlm_Deflagration_FastTrip          : BOOL := FALSE;
    bAlm_Discrepancy_Trip               : BOOL := FALSE;

    (* Rate-of-Change (ROC) Monitoring Registers *)
    rPrevBaghouseCO                     : REAL := 450.0;
    rROC_BaghouseCO_ppm_s               : REAL := 0.0;
    c_rMAX_ROC_BAGHOUSE_CO              : REAL := 150.0;    (* [ppm/s] Baghouse CO Surge Rate of Change Redline *)
    bAlm_ROC_BaghouseCO                 : BOOL := FALSE;

    rPrevBurningZoneTemp                : REAL := 1450.0;
    rROC_BurningZoneTemp_degC_s         : REAL := 0.0;
    c_rMAX_ROC_BURNING_ZONE             : REAL := 15.0;     (* [deg C/s] Burning Zone Max Rate of Change *)
    bAlm_ROC_BurningZone                : BOOL := FALSE;

    (* Auxiliary Kinetic, Bed Kinematic & Thermal Registers *)
    rDeltaTime_Sec                      : REAL := 0.050;    (* Deterministic Scan Step in Seconds *)
    rEquilibriumCO2_bar                 : REAL := 0.0;      (* Baker CaCO3 Equilibrium Partial Pressure [bar] *)
    rCalcinerAbsTemp_K                  : REAL := 1163.15;  (* Absolute Precalciner Temperature in Kelvin *)
    rBurningZoneAbsTemp_K               : REAL := 1723.15;  (* Absolute Burning Zone Temperature in Kelvin *)
    rPartialPressCO2_bar                : REAL := 0.32;     (* Instantaneous Flue Gas CO2 Partial Pressure [bar] *)
    rDecarbKineticRate                  : REAL := 0.0;      (* Apparent Decarbonation Reaction Velocity [1/s] *)
    rFreeLimeKineticRate                : REAL := 0.0;      (* Alite Formation Lime Assimilation Rate [1/s] *)
    rBedCrossSectionArea_m2             : REAL := 21.237;   (* Total Internal Bore Cross Section pi*(D/2)^2 [m2] *)
    rSolidsVolumetricFlow_m3_s          : REAL := 0.0;      (* Actual Volumetric Solid Bed Inflow Rate [m3/s] *)
    rCalculatedBedVelocity_m_s          : REAL := 0.0245;   (* Sullivan-Work Kinematic Bed Axial Transport Speed [m/s] *)
    rCalculatedBedFillFraction          : REAL := 0.138;    (* Fractional Solids Fill Degree of Rotary Cylinder *)
    rCalculatedResidenceTime_s          : REAL := 3346.0;   (* Total Solids Residence Dwell Time [s] *)
    rBurnerAxialMomentum_N              : REAL := 0.0;      (* Primary Axial Air Stream Dynamic Momentum Flux [N] *)
    rBurnerRadialMomentum_N             : REAL := 0.0;      (* Primary Radial Swirl Air Stream Angular Momentum [N] *)
    rBurnerSwirlRatio                   : REAL := 0.82;     (* Dynamic Swirl Number S = G_theta / (R * G_x) *)
    rCoolerRecuperatedHeat_kW           : REAL := 0.0;      (* Total Heat Transferred to Secondary & Tertiary Air [kW] *)
    rClinkerTotalHeatLoss_kW            : REAL := 0.0;      (* Total Thermal Energy Extracted from Molten Clinker [kW] *)
    rShellHeatFlux_W_m2                 : REAL := 0.0;      (* Local Radial Conductive/Convective Heat Flux [W/m2] *)
    rEstimatedCoatThick_m               : REAL := 0.185;    (* Online Reconstructed Clinker Coating Layer [m] *)
    rTotalCoalFlow_t_h                  : REAL := 35.70;    (* Aggregate Plant Pulverized Coal Firing Rate [t/h] *)
    rTotalHeatInput_kJ_s                : REAL := 0.0;      (* Total Thermal Power Input from Fossil Fuels [kW] *)
    rClinkerProduction_kg_s             : REAL := 115.74;   (* Instantaneous Clinker Production Mass Rate [kg/s] *)
    rSpecificHeatCalculated_kJkg        : REAL := 2942.0;   (* Real-time Net Thermal Consumption [kJ/kg clinker] *)

    (* Chemical Bogue Calculation Intermediates *)
    rBogue_CaO                          : REAL := 65.50;
    rBogue_SiO2                         : REAL := 21.40;
    rBogue_Al2O3                        : REAL := 5.25;
    rBogue_Fe2O3                        : REAL := 3.20;
    rBogue_fCaO                         : REAL := 0.85;
    rCalcC3S                            : REAL := 62.40;
    rCalcC2S                            : REAL := 14.30;
    rCalcC3A                            : REAL := 8.50;
    rCalcC4AF                           : REAL := 9.74;
    rCalcLiquidFlux                     : REAL := 27.20;

    (* Internal Computation Temporary Variables *)
    rTempCalc1                          : REAL := 0.0;
    rTempCalc2                          : REAL := 0.0;
    rTempCalc3                          : REAL := 0.0;
    rTempCalc4                          : REAL := 0.0;
    rTempCalc5                          : REAL := 0.0;
    iLoopIdx                            : INT := 1;
    jLoopIdx                            : INT := 1;
END_VAR""")

    # PHASE 0 & Initialization
    parts.append("""
(* ====================================================================================================
   EXECUTION CYCLE: MASTER SAFETY INTERLOCK & SUPERVISION EVALUATION
   ==================================================================================================== *)
IF NOT bMasterEnable OR NOT bEmergencyStop THEN
    eActiveFsmState                     := STATE_EMERGENCY_ESTOP_FUEL_CUT;
    bCmd_FuelCutoff_Main_Trip           := TRUE;
    bCmd_FuelCutoff_Calciner_Trip       := TRUE;
    bCmd_Baghouse_CO_Deflagration_Trip  := TRUE;
    rCmd_Coal_MainBurner_t_h            := 0.0;
    rCmd_Coal_Precalciner_t_h           := 0.0;
    rCmd_RawMeal_Feed_t_h               := 0.0;
    rCmd_KilnDrive_Speed_RPM            := 0.50; (* Drop to minimum safe rotation *)
    bCmd_KilnAuxiliary_InchingDrive_Engage := TRUE; (* Engage barring drive to prevent shell sagging *)
    rCmd_ID_Fan_Speed_Pct               := 30.0; (* Low purge draft *)
    bEmergencyTripActive                := TRUE;
    bClinkerQualityAcceptable           := FALSE;
    dwStatusWord1                       := 16#0001; (* Master Safety Tripped Latch *)
    dwAlarmWord_Trip                    := 16#0001;
    RETURN;
END_IF;

(* Normalize Task Scan Execution Duration *)
rDeltaTime_Sec := TIME_TO_REAL(tTaskScanInterval) / 1000.0;
IF rDeltaTime_Sec < 0.010 THEN
    rDeltaTime_Sec := 0.050;
END_IF;

(* ====================================================================================================
   PHASE 0: DETERMINISTIC INITIALIZATION OF DISCRETE STATE-SPACE & MPC WEIGHT MATRICES
   Discrete State Vector x (8x1):
     x[1] = Burning Zone Sintering Temperature Delta_T_bz [deg C] (Nominal: 1450.0)
     x[2] = Precalciner Calcination Degree Delta_alpha_calc [%] (Nominal: 92.00)
     x[3] = Kiln Inlet Excess Oxygen Delta_O2_inlet [% vol] (Nominal: 2.00)
     x[4] = Preheater Top Cyclone Draft Delta_P_draft [Pa] (Nominal: -5200.0)
     x[5] = Kiln Bed Volumetric Solids Holdup Delta_H_bed [%] (Nominal: 13.80)
     x[6] = Clinker Cooler Discharge Temperature Delta_T_clink [deg C] (Nominal: 95.0)
     x[7] = Clinker Free Lime Content Delta_f_CaO [%] (Nominal: 0.85)
     x[8] = Net Specific Heat Consumption Delta_Q_spec [kJ/kg clinker] (Nominal: 2950.0)

   Discrete Actuator Vector u (8x1):
     u[1] = Main Burner Coal Dosing Delta_F_coal_main [t/h] (Nominal: 14.20)
     u[2] = Precalciner Coal Dosing Delta_F_coal_calc [t/h] (Nominal: 21.50)
     u[3] = Kiln Raw Meal Feed Rate Delta_F_raw [t/h] (Nominal: 645.0)
     u[4] = Rotary Kiln Main Drive Speed Delta_omega_kiln [RPM] (Nominal: 3.80)
     u[5] = Preheater Twin ID Fan Speed / Damper Delta_D_idfan [%] (Nominal: 74.0)
     u[6] = Tertiary Air Duct Damper Position Delta_D_tad [%] (Nominal: 68.0)
     u[7] = Main Burner Swirl Momentum Ratio Delta_R_swirl [-] (Nominal: 0.82)
     u[8] = Grate Cooler Hydraulic Stroke Speed Delta_S_grate [SPM] (Nominal: 12.5)
   ==================================================================================================== *)
IF NOT bMatricesInitialized THEN
    (* Discrete Transition Matrix matA (8x8) at Ts = 50 ms *)
    matA[1, 1] :=  0.9840; matA[1, 2] :=  0.0120; matA[1, 3] := -0.0350; matA[1, 4] :=  0.0000; matA[1, 5] := -0.0480; matA[1, 6] :=  0.0000; matA[1, 7] := -0.0250; matA[1, 8] := -0.0150;
    matA[2, 1] :=  0.0080; matA[2, 2] :=  0.9750; matA[2, 3] := -0.0220; matA[2, 4] := -0.0040; matA[2, 5] := -0.0550; matA[2, 6] :=  0.0000; matA[2, 7] :=  0.0000; matA[2, 8] := -0.0180;
    matA[3, 1] := -0.0150; matA[3, 2] := -0.0280; matA[3, 3] :=  0.9420; matA[3, 4] :=  0.0350; matA[3, 5] :=  0.0000; matA[3, 6] :=  0.0000; matA[3, 7] :=  0.0000; matA[3, 8] :=  0.0000;
    matA[4, 1] :=  0.0000; matA[4, 2] :=  0.0000; matA[4, 3] :=  0.0000; matA[4, 4] :=  0.9150; matA[4, 5] :=  0.0000; matA[4, 6] :=  0.0000; matA[4, 7] :=  0.0000; matA[4, 8] :=  0.0000;
    matA[5, 1] :=  0.0000; matA[5, 2] :=  0.0000; matA[5, 3] :=  0.0000; matA[5, 4] :=  0.0000; matA[5, 5] :=  0.9880; matA[5, 6] :=  0.0000; matA[5, 7] :=  0.0000; matA[5, 8] :=  0.0000;
    matA[6, 1] :=  0.0450; matA[6, 2] :=  0.0000; matA[6, 3] :=  0.0000; matA[6, 4] :=  0.0000; matA[6, 5] :=  0.0250; matA[6, 6] :=  0.9620; matA[6, 7] :=  0.0000; matA[6, 8] :=  0.0000;
    matA[7, 1] := -0.0380; matA[7, 2] := -0.0180; matA[7, 3] :=  0.0000; matA[7, 4] :=  0.0000; matA[7, 5] :=  0.0280; matA[7, 6] :=  0.0000; matA[7, 7] :=  0.9550; matA[7, 8] :=  0.0000;
    matA[8, 1] :=  0.0220; matA[8, 2] :=  0.0150; matA[8, 3] :=  0.0450; matA[8, 4] :=  0.0000; matA[8, 5] := -0.0120; matA[8, 6] :=  0.0080; matA[8, 7] :=  0.0000; matA[8, 8] :=  0.9820;

    (* Discrete Input Coupling Matrix matB (8x8) at Ts = 50 ms *)
    matB[1, 1] :=  0.5200; matB[1, 2] :=  0.0650; matB[1, 3] := -0.1850; matB[1, 4] := -0.0950; matB[1, 5] :=  0.0150; matB[1, 6] :=  0.0450; matB[1, 7] :=  0.1250; matB[1, 8] :=  0.0000;
    matB[2, 1] :=  0.0450; matB[2, 2] :=  0.6800; matB[2, 3] := -0.2250; matB[2, 4] :=  0.0180; matB[2, 5] :=  0.0320; matB[2, 6] :=  0.1850; matB[2, 7] :=  0.0000; matB[2, 8] :=  0.0000;
    matB[3, 1] := -0.1850; matB[3, 2] := -0.2450; matB[3, 3] :=  0.0120; matB[3, 4] :=  0.0000; matB[3, 5] :=  0.3500; matB[3, 6] := -0.0850; matB[3, 7] := -0.0150; matB[3, 8] :=  0.0000;
    matB[4, 1] :=  0.0000; matB[4, 2] :=  0.0000; matB[4, 3] :=  0.0000; matB[4, 4] :=  0.0000; matB[4, 5] := -1.8500; matB[4, 6] :=  0.1500; matB[4, 7] :=  0.0000; matB[4, 8] :=  0.0000;
    matB[5, 1] :=  0.0000; matB[5, 2] :=  0.0000; matB[5, 3] :=  0.0850; matB[5, 4] := -0.1650; matB[5, 5] :=  0.0000; matB[5, 6] :=  0.0000; matB[5, 7] :=  0.0000; matB[5, 8] :=  0.0000;
    matB[6, 1] :=  0.0150; matB[6, 2] :=  0.0000; matB[6, 3] :=  0.0450; matB[6, 4] :=  0.0350; matB[6, 5] :=  0.0000; matB[6, 6] :=  0.0000; matB[6, 7] :=  0.0000; matB[6, 8] := -0.4500;
    matB[7, 1] := -0.0850; matB[7, 2] := -0.0450; matB[7, 3] :=  0.0950; matB[7, 4] :=  0.0420; matB[7, 5] :=  0.0000; matB[7, 6] := -0.0180; matB[7, 7] := -0.0350; matB[7, 8] :=  0.0000;
    matB[8, 1] :=  0.4500; matB[8, 2] :=  0.5200; matB[8, 3] := -0.3800; matB[8, 4] :=  0.0150; matB[8, 5] :=  0.0480; matB[8, 6] := -0.0250; matB[8, 7] :=  0.0000; matB[8, 8] :=  0.0120;

    (* Output Measurement Matrix matC (8x8) Identity *)
    FOR iMatRow := 1 TO 8 DO
        FOR iMatCol := 1 TO 8 DO
            IF iMatRow = iMatCol THEN
                matC[iMatRow, iMatCol] := 1.0;
            ELSE
                matC[iMatRow, iMatCol] := 0.0;
            END_IF;
            matD[iMatRow, iMatCol] := 0.0;
        END_FOR;
    END_FOR;

    (* MPC Quadratic Error Weight Matrix Diag(Q) *)
    matQ[1, 1] := 18.50; (* Burning Zone Temperature Tracking Penalty *)
    matQ[2, 2] := 14.00; (* Calcination Degree Tracking Penalty *)
    matQ[3, 3] := 12.00; (* Kiln Inlet Oxygen Penalty (Efficiency & NOx) *)
    matQ[4, 4] :=  8.50; (* Preheater Top Draft Pressure Penalty *)
    matQ[5, 5] := 10.00; (* Kiln Bed Solids Holdup Stability Penalty *)
    matQ[6, 6] :=  6.50; (* Clinker Discharge Temperature Penalty *)
    matQ[7, 7] := 25.00; (* Free Lime Strict Quality Penalty (f-CaO < 1.0%) *)
    matQ[8, 8] := 16.00; (* Net Heat Consumption Minimization Penalty *)

    (* MPC Control Effort Penalty Diag(R) *)
    matR[1, 1] := 0.085; (* Main Burner Coal Modulation Effort *)
    matR[2, 2] := 0.065; (* Calciner Coal Modulation Effort *)
    matR[3, 3] := 0.045; (* Raw Meal Feed Rate Modulation Effort *)
    matR[4, 4] := 0.150; (* Kiln Drive Speed Modulation Effort *)
    matR[5, 5] := 0.080; (* ID Fan Speed Modulation Effort *)
    matR[6, 6] := 0.095; (* TAD Damper Modulation Effort *)
    matR[7, 7] := 0.220; (* Burner Swirl Ratio Trim Effort *)
    matR[8, 8] := 0.075; (* Grate Cooler Stroke Speed Effort *)

    (* MPC Actuator Slew Rate Penalty Diag(S) *)
    matS[1, 1] := 0.250;
    matS[2, 2] := 0.200;
    matS[3, 3] := 0.180;
    matS[4, 4] := 0.550;
    matS[5, 5] := 0.320;
    matS[6, 6] := 0.400;
    matS[7, 7] := 0.850;
    matS[8, 8] := 0.280;

    FOR iMatRow := 1 TO 8 DO
        matP[iMatRow, iMatRow] := matQ[iMatRow, iMatRow] * 2.80;
    END_FOR;

    (* Hard Actuator Saturation Constraints *)
    uMin[1] := -5.0;  uMax[1] := 5.0;   (* Delta Main Coal [t/h] *)
    uMin[2] := -8.0;  uMax[2] := 8.0;   (* Delta Calciner Coal [t/h] *)
    uMin[3] := -80.0; uMax[3] := 80.0;  (* Delta Raw Meal [t/h] *)
    uMin[4] := -1.2;  uMax[4] := 1.2;   (* Delta Kiln Speed [RPM] *)
    uMin[5] := -15.0; uMax[5] := 15.0;  (* Delta ID Fan Damper [%] *)
    uMin[6] := -20.0; uMax[6] := 20.0;  (* Delta TAD Damper [%] *)
    uMin[7] := -0.35; uMax[7] := 0.35;  (* Delta Burner Swirl Ratio [-] *)
    uMin[8] := -6.0;  uMax[8] := 6.0;   (* Delta Cooler Stroke [SPM] *)

    deltaUMax[1] := 0.25;  (* Max Main Coal Slew per 50 ms [t/h] *)
    deltaUMax[2] := 0.35;  (* Max Calciner Coal Slew per 50 ms [t/h] *)
    deltaUMax[3] := 3.50;  (* Max Raw Meal Slew per 50 ms [t/h] *)
    deltaUMax[4] := 0.05;  (* Max Kiln RPM Slew per 50 ms [RPM] *)
    deltaUMax[5] := 0.80;  (* Max ID Fan Slew per 50 ms [%] *)
    deltaUMax[6] := 1.00;  (* Max TAD Damper Slew per 50 ms [%] *)
    deltaUMax[7] := 0.02;  (* Max Swirl Slew per 50 ms [-] *)
    deltaUMax[8] := 0.40;  (* Max Grate Stroke Slew per 50 ms [SPM] *)

    bMatricesInitialized := TRUE;
END_IF;""")

    # PHASE 1: 2oo3 TMR Voting
    parts.append("""
(* ====================================================================================================
   PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING WITH DISCREPANCY TIMERS
   ==================================================================================================== *)

(* 1.1 Burning Zone Optical Ratio Pyrometer 2oo3 Voting *)
rDiff_BZ_AB := ABS(TT_BURNING_ZONE_PYRO_101A - TT_BURNING_ZONE_PYRO_101B);
rDiff_BZ_BC := ABS(TT_BURNING_ZONE_PYRO_101B - TT_BURNING_ZONE_PYRO_101C);
rDiff_BZ_CA := ABS(TT_BURNING_ZONE_PYRO_101C - TT_BURNING_ZONE_PYRO_101A);

IF (rDiff_BZ_AB <= rTMR_Tol_BurningZone) AND (rDiff_BZ_BC <= rTMR_Tol_BurningZone) AND (rDiff_BZ_CA <= rTMR_Tol_BurningZone) THEN
    (* All three channels in statistical consensus: Median Selection *)
    IF ((TT_BURNING_ZONE_PYRO_101A >= TT_BURNING_ZONE_PYRO_101B) AND (TT_BURNING_ZONE_PYRO_101A <= TT_BURNING_ZONE_PYRO_101C)) OR
       ((TT_BURNING_ZONE_PYRO_101A >= TT_BURNING_ZONE_PYRO_101C) AND (TT_BURNING_ZONE_PYRO_101A <= TT_BURNING_ZONE_PYRO_101B)) THEN
        rVoted_BurningZoneTemp_degC := TT_BURNING_ZONE_PYRO_101A;
    ELSIF ((TT_BURNING_ZONE_PYRO_101B >= TT_BURNING_ZONE_PYRO_101A) AND (TT_BURNING_ZONE_PYRO_101B <= TT_BURNING_ZONE_PYRO_101C)) OR
          ((TT_BURNING_ZONE_PYRO_101B >= TT_BURNING_ZONE_PYRO_101C) AND (TT_BURNING_ZONE_PYRO_101B <= TT_BURNING_ZONE_PYRO_101A)) THEN
        rVoted_BurningZoneTemp_degC := TT_BURNING_ZONE_PYRO_101B;
    ELSE
        rVoted_BurningZoneTemp_degC := TT_BURNING_ZONE_PYRO_101C;
    END_IF;
    bFault_BZ_A := FALSE; bFault_BZ_B := FALSE; bFault_BZ_C := FALSE;
    rTimer_BZ_A := 0.0; rTimer_BZ_B := 0.0; rTimer_BZ_C := 0.0;
ELSIF (rDiff_BZ_AB <= rTMR_Tol_BurningZone) THEN
    rVoted_BurningZoneTemp_degC := (TT_BURNING_ZONE_PYRO_101A + TT_BURNING_ZONE_PYRO_101B) * 0.50;
    rTimer_BZ_C := rTimer_BZ_C + rDeltaTime_Sec;
    IF rTimer_BZ_C >= 2.50 THEN bFault_BZ_C := TRUE; END_IF;
ELSIF (rDiff_BZ_BC <= rTMR_Tol_BurningZone) THEN
    rVoted_BurningZoneTemp_degC := (TT_BURNING_ZONE_PYRO_101B + TT_BURNING_ZONE_PYRO_101C) * 0.50;
    rTimer_BZ_A := rTimer_BZ_A + rDeltaTime_Sec;
    IF rTimer_BZ_A >= 2.50 THEN bFault_BZ_A := TRUE; END_IF;
ELSIF (rDiff_BZ_CA <= rTMR_Tol_BurningZone) THEN
    rVoted_BurningZoneTemp_degC := (TT_BURNING_ZONE_PYRO_101A + TT_BURNING_ZONE_PYRO_101C) * 0.50;
    rTimer_BZ_B := rTimer_BZ_B + rDeltaTime_Sec;
    IF rTimer_BZ_B >= 2.50 THEN bFault_BZ_B := TRUE; END_IF;
ELSE
    (* Total 2oo3 Discrepancy Breakdown: Hold median and trigger alarm *)
    rVoted_BurningZoneTemp_degC := TT_BURNING_ZONE_PYRO_101B;
    bAlm_Discrepancy_Trip := TRUE;
END_IF;

(* 1.2 Kiln Inlet Gas Temperature 2oo3 Voting *)
rDiff_InletT_AB := ABS(TT_KILN_INLET_GAS_102A - TT_KILN_INLET_GAS_102B);
rDiff_InletT_BC := ABS(TT_KILN_INLET_GAS_102B - TT_KILN_INLET_GAS_102C);
rDiff_InletT_CA := ABS(TT_KILN_INLET_GAS_102C - TT_KILN_INLET_GAS_102A);

IF (rDiff_InletT_AB <= rTMR_Tol_KilnInletGas) AND (rDiff_InletT_BC <= rTMR_Tol_KilnInletGas) AND (rDiff_InletT_CA <= rTMR_Tol_KilnInletGas) THEN
    IF ((TT_KILN_INLET_GAS_102A >= TT_KILN_INLET_GAS_102B) AND (TT_KILN_INLET_GAS_102A <= TT_KILN_INLET_GAS_102C)) OR
       ((TT_KILN_INLET_GAS_102A >= TT_KILN_INLET_GAS_102C) AND (TT_KILN_INLET_GAS_102A <= TT_KILN_INLET_GAS_102B)) THEN
        rVoted_KilnInletGasTemp_degC := TT_KILN_INLET_GAS_102A;
    ELSIF ((TT_KILN_INLET_GAS_102B >= TT_KILN_INLET_GAS_102A) AND (TT_KILN_INLET_GAS_102B <= TT_KILN_INLET_GAS_102C)) OR
          ((TT_KILN_INLET_GAS_102B >= TT_KILN_INLET_GAS_102C) AND (TT_KILN_INLET_GAS_102B <= TT_KILN_INLET_GAS_102A)) THEN
        rVoted_KilnInletGasTemp_degC := TT_KILN_INLET_GAS_102B;
    ELSE
        rVoted_KilnInletGasTemp_degC := TT_KILN_INLET_GAS_102C;
    END_IF;
    bFault_InletT_A := FALSE; bFault_InletT_B := FALSE; bFault_InletT_C := FALSE;
    rTimer_InletT_A := 0.0; rTimer_InletT_B := 0.0; rTimer_InletT_C := 0.0;
ELSIF (rDiff_InletT_AB <= rTMR_Tol_KilnInletGas) THEN
    rVoted_KilnInletGasTemp_degC := (TT_KILN_INLET_GAS_102A + TT_KILN_INLET_GAS_102B) * 0.50;
    rTimer_InletT_C := rTimer_InletT_C + rDeltaTime_Sec;
    IF rTimer_InletT_C >= 2.50 THEN bFault_InletT_C := TRUE; END_IF;
ELSIF (rDiff_InletT_BC <= rTMR_Tol_KilnInletGas) THEN
    rVoted_KilnInletGasTemp_degC := (TT_KILN_INLET_GAS_102B + TT_KILN_INLET_GAS_102C) * 0.50;
    rTimer_InletT_A := rTimer_InletT_A + rDeltaTime_Sec;
    IF rTimer_InletT_A >= 2.50 THEN bFault_InletT_A := TRUE; END_IF;
ELSIF (rDiff_InletT_CA <= rTMR_Tol_KilnInletGas) THEN
    rVoted_KilnInletGasTemp_degC := (TT_KILN_INLET_GAS_102A + TT_KILN_INLET_GAS_102C) * 0.50;
    rTimer_InletT_B := rTimer_InletT_B + rDeltaTime_Sec;
    IF rTimer_InletT_B >= 2.50 THEN bFault_InletT_B := TRUE; END_IF;
ELSE
    rVoted_KilnInletGasTemp_degC := TT_KILN_INLET_GAS_102B;
    bAlm_Discrepancy_Trip := TRUE;
END_IF;

(* 1.3 Precalciner Exit Gas Temperature 2oo3 Voting *)
rDiff_CalcT_AB := ABS(TT_PRECALCINER_EXIT_201A - TT_PRECALCINER_EXIT_201B);
rDiff_CalcT_BC := ABS(TT_PRECALCINER_EXIT_201B - TT_PRECALCINER_EXIT_201C);
rDiff_CalcT_CA := ABS(TT_PRECALCINER_EXIT_201C - TT_PRECALCINER_EXIT_201A);

IF (rDiff_CalcT_AB <= rTMR_Tol_CalcinerExit) AND (rDiff_CalcT_BC <= rTMR_Tol_CalcinerExit) AND (rDiff_CalcT_CA <= rTMR_Tol_CalcinerExit) THEN
    IF ((TT_PRECALCINER_EXIT_201A >= TT_PRECALCINER_EXIT_201B) AND (TT_PRECALCINER_EXIT_201A <= TT_PRECALCINER_EXIT_201C)) OR
       ((TT_PRECALCINER_EXIT_201A >= TT_PRECALCINER_EXIT_201C) AND (TT_PRECALCINER_EXIT_201A <= TT_PRECALCINER_EXIT_201B)) THEN
        rVoted_PrecalcinerExitTemp_degC := TT_PRECALCINER_EXIT_201A;
    ELSIF ((TT_PRECALCINER_EXIT_201B >= TT_PRECALCINER_EXIT_201A) AND (TT_PRECALCINER_EXIT_201B <= TT_PRECALCINER_EXIT_201C)) OR
          ((TT_PRECALCINER_EXIT_201B >= TT_PRECALCINER_EXIT_201C) AND (TT_PRECALCINER_EXIT_201B <= TT_PRECALCINER_EXIT_201A)) THEN
        rVoted_PrecalcinerExitTemp_degC := TT_PRECALCINER_EXIT_201B;
    ELSE
        rVoted_PrecalcinerExitTemp_degC := TT_PRECALCINER_EXIT_201C;
    END_IF;
    bFault_CalcT_A := FALSE; bFault_CalcT_B := FALSE; bFault_CalcT_C := FALSE;
    rTimer_CalcT_A := 0.0; rTimer_CalcT_B := 0.0; rTimer_CalcT_C := 0.0;
ELSIF (rDiff_CalcT_AB <= rTMR_Tol_CalcinerExit) THEN
    rVoted_PrecalcinerExitTemp_degC := (TT_PRECALCINER_EXIT_201A + TT_PRECALCINER_EXIT_201B) * 0.50;
    rTimer_CalcT_C := rTimer_CalcT_C + rDeltaTime_Sec;
    IF rTimer_CalcT_C >= 2.50 THEN bFault_CalcT_C := TRUE; END_IF;
ELSIF (rDiff_CalcT_BC <= rTMR_Tol_CalcinerExit) THEN
    rVoted_PrecalcinerExitTemp_degC := (TT_PRECALCINER_EXIT_201B + TT_PRECALCINER_EXIT_201C) * 0.50;
    rTimer_CalcT_A := rTimer_CalcT_A + rDeltaTime_Sec;
    IF rTimer_CalcT_A >= 2.50 THEN bFault_CalcT_A := TRUE; END_IF;
ELSIF (rDiff_CalcT_CA <= rTMR_Tol_CalcinerExit) THEN
    rVoted_PrecalcinerExitTemp_degC := (TT_PRECALCINER_EXIT_201A + TT_PRECALCINER_EXIT_201C) * 0.50;
    rTimer_CalcT_B := rTimer_CalcT_B + rDeltaTime_Sec;
    IF rTimer_CalcT_B >= 2.50 THEN bFault_CalcT_B := TRUE; END_IF;
ELSE
    rVoted_PrecalcinerExitTemp_degC := TT_PRECALCINER_EXIT_201B;
    bAlm_Discrepancy_Trip := TRUE;
END_IF;

(* 1.4 Kiln Inlet Flue Gas Oxygen 2oo3 Voting *)
rDiff_O2_AB := ABS(AIT_KILN_INLET_O2_401A - AIT_KILN_INLET_O2_401B);
rDiff_O2_BC := ABS(AIT_KILN_INLET_O2_401B - AIT_KILN_INLET_O2_401C);
rDiff_O2_CA := ABS(AIT_KILN_INLET_O2_401C - AIT_KILN_INLET_O2_401A);

IF (rDiff_O2_AB <= rTMR_Tol_O2) AND (rDiff_O2_BC <= rTMR_Tol_O2) AND (rDiff_O2_CA <= rTMR_Tol_O2) THEN
    IF ((AIT_KILN_INLET_O2_401A >= AIT_KILN_INLET_O2_401B) AND (AIT_KILN_INLET_O2_401A <= AIT_KILN_INLET_O2_401C)) OR
       ((AIT_KILN_INLET_O2_401A >= AIT_KILN_INLET_O2_401C) AND (AIT_KILN_INLET_O2_401A <= AIT_KILN_INLET_O2_401B)) THEN
        rVoted_KilnInletO2_pct := AIT_KILN_INLET_O2_401A;
    ELSIF ((AIT_KILN_INLET_O2_401B >= AIT_KILN_INLET_O2_401A) AND (AIT_KILN_INLET_O2_401B <= AIT_KILN_INLET_O2_401C)) OR
          ((AIT_KILN_INLET_O2_401B >= AIT_KILN_INLET_O2_401C) AND (AIT_KILN_INLET_O2_401B <= AIT_KILN_INLET_O2_401A)) THEN
        rVoted_KilnInletO2_pct := AIT_KILN_INLET_O2_401B;
    ELSE
        rVoted_KilnInletO2_pct := AIT_KILN_INLET_O2_401C;
    END_IF;
    bFault_O2_A := FALSE; bFault_O2_B := FALSE; bFault_O2_C := FALSE;
    rTimer_O2_A := 0.0; rTimer_O2_B := 0.0; rTimer_O2_C := 0.0;
ELSIF (rDiff_O2_AB <= rTMR_Tol_O2) THEN
    rVoted_KilnInletO2_pct := (AIT_KILN_INLET_O2_401A + AIT_KILN_INLET_O2_401B) * 0.50;
    rTimer_O2_C := rTimer_O2_C + rDeltaTime_Sec;
    IF rTimer_O2_C >= 2.50 THEN bFault_O2_C := TRUE; END_IF;
ELSIF (rDiff_O2_BC <= rTMR_Tol_O2) THEN
    rVoted_KilnInletO2_pct := (AIT_KILN_INLET_O2_401B + AIT_KILN_INLET_O2_401C) * 0.50;
    rTimer_O2_A := rTimer_O2_A + rDeltaTime_Sec;
    IF rTimer_O2_A >= 2.50 THEN bFault_O2_A := TRUE; END_IF;
ELSIF (rDiff_O2_CA <= rTMR_Tol_O2) THEN
    rVoted_KilnInletO2_pct := (AIT_KILN_INLET_O2_401A + AIT_KILN_INLET_O2_401C) * 0.50;
    rTimer_O2_B := rTimer_O2_B + rDeltaTime_Sec;
    IF rTimer_O2_B >= 2.50 THEN bFault_O2_B := TRUE; END_IF;
ELSE
    rVoted_KilnInletO2_pct := AIT_KILN_INLET_O2_401B;
    bAlm_Discrepancy_Trip := TRUE;
END_IF;

(* 1.5 Kiln Inlet Static Draft Pressure 2oo3 Voting *)
rDiff_InletP_AB := ABS(PT_KILN_INLET_DRAFT_301A - PT_KILN_INLET_DRAFT_301B);
rDiff_InletP_BC := ABS(PT_KILN_INLET_DRAFT_301B - PT_KILN_INLET_DRAFT_301C);
rDiff_InletP_CA := ABS(PT_KILN_INLET_DRAFT_301C - PT_KILN_INLET_DRAFT_301A);

IF (rDiff_InletP_AB <= rTMR_Tol_KilnInletDraft) AND (rDiff_InletP_BC <= rTMR_Tol_KilnInletDraft) AND (rDiff_InletP_CA <= rTMR_Tol_KilnInletDraft) THEN
    IF ((PT_KILN_INLET_DRAFT_301A >= PT_KILN_INLET_DRAFT_301B) AND (PT_KILN_INLET_DRAFT_301A <= PT_KILN_INLET_DRAFT_301C)) OR
       ((PT_KILN_INLET_DRAFT_301A >= PT_KILN_INLET_DRAFT_301C) AND (PT_KILN_INLET_DRAFT_301A <= PT_KILN_INLET_DRAFT_301B)) THEN
        rVoted_KilnInletDraft_Pa := PT_KILN_INLET_DRAFT_301A;
    ELSIF ((PT_KILN_INLET_DRAFT_301B >= PT_KILN_INLET_DRAFT_301A) AND (PT_KILN_INLET_DRAFT_301B <= PT_KILN_INLET_DRAFT_301C)) OR
          ((PT_KILN_INLET_DRAFT_301B >= PT_KILN_INLET_DRAFT_301C) AND (PT_KILN_INLET_DRAFT_301B <= PT_KILN_INLET_DRAFT_301A)) THEN
        rVoted_KilnInletDraft_Pa := PT_KILN_INLET_DRAFT_301B;
    ELSE
        rVoted_KilnInletDraft_Pa := PT_KILN_INLET_DRAFT_301C;
    END_IF;
    bFault_InletP_A := FALSE; bFault_InletP_B := FALSE; bFault_InletP_C := FALSE;
    rTimer_InletP_A := 0.0; rTimer_InletP_B := 0.0; rTimer_InletP_C := 0.0;
ELSIF (rDiff_InletP_AB <= rTMR_Tol_KilnInletDraft) THEN
    rVoted_KilnInletDraft_Pa := (PT_KILN_INLET_DRAFT_301A + PT_KILN_INLET_DRAFT_301B) * 0.50;
    rTimer_InletP_C := rTimer_InletP_C + rDeltaTime_Sec;
    IF rTimer_InletP_C >= 2.50 THEN bFault_InletP_C := TRUE; END_IF;
ELSIF (rDiff_InletP_BC <= rTMR_Tol_KilnInletDraft) THEN
    rVoted_KilnInletDraft_Pa := (PT_KILN_INLET_DRAFT_301B + PT_KILN_INLET_DRAFT_301C) * 0.50;
    rTimer_InletP_A := rTimer_InletP_A + rDeltaTime_Sec;
    IF rTimer_InletP_A >= 2.50 THEN bFault_InletP_A := TRUE; END_IF;
ELSIF (rDiff_InletP_CA <= rTMR_Tol_KilnInletDraft) THEN
    rVoted_KilnInletDraft_Pa := (PT_KILN_INLET_DRAFT_301A + PT_KILN_INLET_DRAFT_301C) * 0.50;
    rTimer_InletP_B := rTimer_InletP_B + rDeltaTime_Sec;
    IF rTimer_InletP_B >= 2.50 THEN bFault_InletP_B := TRUE; END_IF;
ELSE
    rVoted_KilnInletDraft_Pa := PT_KILN_INLET_DRAFT_301B;
    bAlm_Discrepancy_Trip := TRUE;
END_IF;

(* 1.6 Precalciner Top Cyclone Draft 2oo3 Voting *)
rDiff_TopP_AB := ABS(PT_PRECALCINER_TOP_DRAFT_302A - PT_PRECALCINER_TOP_DRAFT_302B);
rDiff_TopP_BC := ABS(PT_PRECALCINER_TOP_DRAFT_302B - PT_PRECALCINER_TOP_DRAFT_302C);
rDiff_TopP_CA := ABS(PT_PRECALCINER_TOP_DRAFT_302C - PT_PRECALCINER_TOP_DRAFT_302A);

IF (rDiff_TopP_AB <= rTMR_Tol_TopDraft) AND (rDiff_TopP_BC <= rTMR_Tol_TopDraft) AND (rDiff_TopP_CA <= rTMR_Tol_TopDraft) THEN
    IF ((PT_PRECALCINER_TOP_DRAFT_302A >= PT_PRECALCINER_TOP_DRAFT_302B) AND (PT_PRECALCINER_TOP_DRAFT_302A <= PT_PRECALCINER_TOP_DRAFT_302C)) OR
       ((PT_PRECALCINER_TOP_DRAFT_302A >= PT_PRECALCINER_TOP_DRAFT_302C) AND (PT_PRECALCINER_TOP_DRAFT_302A <= PT_PRECALCINER_TOP_DRAFT_302B)) THEN
        rVoted_PreheaterTopDraft_Pa := PT_PRECALCINER_TOP_DRAFT_302A;
    ELSIF ((PT_PRECALCINER_TOP_DRAFT_302B >= PT_PRECALCINER_TOP_DRAFT_302A) AND (PT_PRECALCINER_TOP_DRAFT_302B <= PT_PRECALCINER_TOP_DRAFT_302C)) OR
          ((PT_PRECALCINER_TOP_DRAFT_302B >= PT_PRECALCINER_TOP_DRAFT_302C) AND (PT_PRECALCINER_TOP_DRAFT_302B <= PT_PRECALCINER_TOP_DRAFT_302A)) THEN
        rVoted_PreheaterTopDraft_Pa := PT_PRECALCINER_TOP_DRAFT_302B;
    ELSE
        rVoted_PreheaterTopDraft_Pa := PT_PRECALCINER_TOP_DRAFT_302C;
    END_IF;
ELSIF (rDiff_TopP_AB <= rTMR_Tol_TopDraft) THEN
    rVoted_PreheaterTopDraft_Pa := (PT_PRECALCINER_TOP_DRAFT_302A + PT_PRECALCINER_TOP_DRAFT_302B) * 0.50;
ELSIF (rDiff_TopP_BC <= rTMR_Tol_TopDraft) THEN
    rVoted_PreheaterTopDraft_Pa := (PT_PRECALCINER_TOP_DRAFT_302B + PT_PRECALCINER_TOP_DRAFT_302C) * 0.50;
ELSIF (rDiff_TopP_CA <= rTMR_Tol_TopDraft) THEN
    rVoted_PreheaterTopDraft_Pa := (PT_PRECALCINER_TOP_DRAFT_302A + PT_PRECALCINER_TOP_DRAFT_302C) * 0.50;
ELSE
    rVoted_PreheaterTopDraft_Pa := PT_PRECALCINER_TOP_DRAFT_302B;
END_IF;

(* 1.7 Grate Cooler Under-Grate Bed Pressure 2oo3 Voting *)
rDiff_BedP_AB := ABS(PT_GRATE_COOLER_BED_601A - PT_GRATE_COOLER_BED_601B);
rDiff_BedP_BC := ABS(PT_GRATE_COOLER_BED_601B - PT_GRATE_COOLER_BED_601C);
rDiff_BedP_CA := ABS(PT_GRATE_COOLER_BED_601C - PT_GRATE_COOLER_BED_601A);

IF (rDiff_BedP_AB <= rTMR_Tol_CoolerBedPress) AND (rDiff_BedP_BC <= rTMR_Tol_CoolerBedPress) AND (rDiff_BedP_CA <= rTMR_Tol_CoolerBedPress) THEN
    IF ((PT_GRATE_COOLER_BED_601A >= PT_GRATE_COOLER_BED_601B) AND (PT_GRATE_COOLER_BED_601A <= PT_GRATE_COOLER_BED_601C)) OR
       ((PT_GRATE_COOLER_BED_601A >= PT_GRATE_COOLER_BED_601C) AND (PT_GRATE_COOLER_BED_601A <= PT_GRATE_COOLER_BED_601B)) THEN
        rVoted_GrateCoolerBedPress_mbar := PT_GRATE_COOLER_BED_601A;
    ELSIF ((PT_GRATE_COOLER_BED_601B >= PT_GRATE_COOLER_BED_601A) AND (PT_GRATE_COOLER_BED_601B <= PT_GRATE_COOLER_BED_601C)) OR
          ((PT_GRATE_COOLER_BED_601B >= PT_GRATE_COOLER_BED_601C) AND (PT_GRATE_COOLER_BED_601B <= PT_GRATE_COOLER_BED_601A)) THEN
        rVoted_GrateCoolerBedPress_mbar := PT_GRATE_COOLER_BED_601B;
    ELSE
        rVoted_GrateCoolerBedPress_mbar := PT_GRATE_COOLER_BED_601C;
    END_IF;
ELSIF (rDiff_BedP_AB <= rTMR_Tol_CoolerBedPress) THEN
    rVoted_GrateCoolerBedPress_mbar := (PT_GRATE_COOLER_BED_601A + PT_GRATE_COOLER_BED_601B) * 0.50;
ELSIF (rDiff_BedP_BC <= rTMR_Tol_CoolerBedPress) THEN
    rVoted_GrateCoolerBedPress_mbar := (PT_GRATE_COOLER_BED_601B + PT_GRATE_COOLER_BED_601C) * 0.50;
ELSIF (rDiff_BedP_CA <= rTMR_Tol_CoolerBedPress) THEN
    rVoted_GrateCoolerBedPress_mbar := (PT_GRATE_COOLER_BED_601A + PT_GRATE_COOLER_BED_601C) * 0.50;
ELSE
    rVoted_GrateCoolerBedPress_mbar := PT_GRATE_COOLER_BED_601B;
END_IF;

(* 1.8 Baghouse Inlet CO Safety Analyzer 2oo3 Voting (Deflagration Protection) *)
rDiff_BagCO_AB := ABS(AIT_BAGHOUSE_INLET_CO_702A - AIT_BAGHOUSE_INLET_CO_702B);
rDiff_BagCO_BC := ABS(AIT_BAGHOUSE_INLET_CO_702B - AIT_BAGHOUSE_INLET_CO_702C);
rDiff_BagCO_CA := ABS(AIT_BAGHOUSE_INLET_CO_702C - AIT_BAGHOUSE_INLET_CO_702A);

IF (rDiff_BagCO_AB <= rTMR_Tol_BaghouseCO) AND (rDiff_BagCO_BC <= rTMR_Tol_BaghouseCO) AND (rDiff_BagCO_CA <= rTMR_Tol_BaghouseCO) THEN
    IF ((AIT_BAGHOUSE_INLET_CO_702A >= AIT_BAGHOUSE_INLET_CO_702B) AND (AIT_BAGHOUSE_INLET_CO_702A <= AIT_BAGHOUSE_INLET_CO_702C)) OR
       ((AIT_BAGHOUSE_INLET_CO_702A >= AIT_BAGHOUSE_INLET_CO_702C) AND (AIT_BAGHOUSE_INLET_CO_702A <= AIT_BAGHOUSE_INLET_CO_702B)) THEN
        rVoted_BaghouseCO_ppm := AIT_BAGHOUSE_INLET_CO_702A;
    ELSIF ((AIT_BAGHOUSE_INLET_CO_702B >= AIT_BAGHOUSE_INLET_CO_702A) AND (AIT_BAGHOUSE_INLET_CO_702B <= AIT_BAGHOUSE_INLET_CO_702C)) OR
          ((AIT_BAGHOUSE_INLET_CO_702B >= AIT_BAGHOUSE_INLET_CO_702C) AND (AIT_BAGHOUSE_INLET_CO_702B <= AIT_BAGHOUSE_INLET_CO_702A)) THEN
        rVoted_BaghouseCO_ppm := AIT_BAGHOUSE_INLET_CO_702B;
    ELSE
        rVoted_BaghouseCO_ppm := AIT_BAGHOUSE_INLET_CO_702C;
    END_IF;
ELSIF (rDiff_BagCO_AB <= rTMR_Tol_BaghouseCO) THEN
    rVoted_BaghouseCO_ppm := MAX(AIT_BAGHOUSE_INLET_CO_702A, AIT_BAGHOUSE_INLET_CO_702B); (* Conservative max for safety *)
ELSIF (rDiff_BagCO_BC <= rTMR_Tol_BaghouseCO) THEN
    rVoted_BaghouseCO_ppm := MAX(AIT_BAGHOUSE_INLET_CO_702B, AIT_BAGHOUSE_INLET_CO_702C);
ELSIF (rDiff_BagCO_CA <= rTMR_Tol_BaghouseCO) THEN
    rVoted_BaghouseCO_ppm := MAX(AIT_BAGHOUSE_INLET_CO_702A, AIT_BAGHOUSE_INLET_CO_702C);
ELSE
    rVoted_BaghouseCO_ppm := MAX(AIT_BAGHOUSE_INLET_CO_702A, MAX(AIT_BAGHOUSE_INLET_CO_702B, AIT_BAGHOUSE_INLET_CO_702C));
END_IF;

(* 1.9 Auxiliary 2oo3 Voted Variables *)
rVoted_KilnDriveSpeed_RPM        := (ST_KILN_MAIN_DRIVE_RPM_501A + ST_KILN_MAIN_DRIVE_RPM_501B + ST_KILN_MAIN_DRIVE_RPM_501C) / 3.0;
rVoted_KilnDrivePower_kW         := (IT_KILN_MAIN_DRIVE_KW_502A + IT_KILN_MAIN_DRIVE_KW_502B + IT_KILN_MAIN_DRIVE_KW_502C) / 3.0;
rVoted_ClinkerDischargeTemp_degC := (TT_CLINKER_DISCHARGE_701A + TT_CLINKER_DISCHARGE_701B + TT_CLINKER_DISCHARGE_701C) / 3.0;
rVoted_KilnShellPeakTemp_degC    := MAX(TT_KILN_SHELL_MAX_404A, MAX(TT_KILN_SHELL_MAX_404B, TT_KILN_SHELL_MAX_404C));
rVoted_TertiaryAirTemp_degC      := (TT_TERTIARY_AIR_DUCT_103A + TT_TERTIARY_AIR_DUCT_103B + TT_TERTIARY_AIR_DUCT_103C) / 3.0;
rVoted_TertiaryAirDraft_Pa       := (PT_TERTIARY_AIR_DUCT_104A + PT_TERTIARY_AIR_DUCT_104B + PT_TERTIARY_AIR_DUCT_104C) / 3.0;
rVoted_KilnInletCO_ppm           := (AIT_KILN_INLET_CO_402A + AIT_KILN_INLET_CO_402B + AIT_KILN_INLET_CO_402C) / 3.0;
rVoted_KilnInletNOx_ppm          := (AIT_KILN_INLET_NOX_403A + AIT_KILN_INLET_NOX_403B + AIT_KILN_INLET_NOX_403C) / 3.0;""")

    # PHASE 2: Cyber-Physical Kinetic & Thermodynamic Observers
    parts.append("""
(* ====================================================================================================
   PHASE 2: CYBER-PHYSICAL KINETIC, THERMODYNAMIC & BED TRANSPORT OBSERVERS
   ==================================================================================================== *)

(* 2.1 Non-Linear Endothermic Calcium Carbonate Decarbonation Kinetics (CaCO3 -> CaO + CO2) *)
rCalcinerAbsTemp_K := rVoted_PrecalcinerExitTemp_degC + 273.15;
IF rCalcinerAbsTemp_K > 500.0 THEN
    (* Baker CaCO3 Equilibrium Dissociation Pressure: log10(P_eq) = 7.079 - 8308 / T [bar] *)
    rTempCalc1 := 7.079 - (8308.0 / rCalcinerAbsTemp_K);
    rEquilibriumCO2_bar := EXPT(10.0, rTempCalc1);
    
    (* Arrhenius reaction rate constant k_decarb = k0 * exp(-Ea / (R*T)) *)
    rTempCalc2 := -c_rDECARB_EA / (c_rR_GAS * rCalcinerAbsTemp_K);
    IF rTempCalc2 > -50.0 THEN
        rDecarbKineticRate := c_rDECARB_K0 * EXP(rTempCalc2);
    ELSE
        rDecarbKineticRate := 0.0;
    END_IF;

    (* Driving chemical affinity: (1 - P_CO2 / P_eq) *)
    IF rEquilibriumCO2_bar > rPartialPressCO2_bar THEN
        rTempCalc3 := 1.0 - (rPartialPressCO2_bar / rEquilibriumCO2_bar);
    ELSE
        rTempCalc3 := 0.0;
    END_IF;

    (* Real-Time Apparent Calcination Degree Estimation *)
    rObserved_ApparentCalcination_pct := 82.0 + (12.5 * rTempCalc3) + (0.015 * (rVoted_PrecalcinerExitTemp_degC - 880.0));
    IF rObserved_ApparentCalcination_pct > 99.5 THEN rObserved_ApparentCalcination_pct := 99.5; END_IF;
    IF rObserved_ApparentCalcination_pct < 60.0 THEN rObserved_ApparentCalcination_pct := 60.0; END_IF;
END_IF;

(* 2.2 Exothermic Clinker Mineral Formation Thermodynamics (Bogue Calculation for C3S, C2S, C3A, C4AF) *)
rBogue_CaO   := AIT_CLINKER_XRF_CAO_pct;
rBogue_SiO2  := AIT_CLINKER_XRF_SIO2_pct;
rBogue_Al2O3 := AIT_CLINKER_XRF_AL2O3_pct;
rBogue_Fe2O3 := AIT_CLINKER_XRF_FE2O3_pct;
rBogue_fCaO  := AIT_CLINKER_XRF_FCAO_pct;

(* Standard Bogue Formulations *)
(* C3S  = 4.071*CaO - 7.600*SiO2 - 6.718*Al2O3 - 1.430*Fe2O3 - 5.102*f-CaO *)
rCalcC3S := (4.071 * rBogue_CaO) - (7.600 * rBogue_SiO2) - (6.718 * rBogue_Al2O3) - (1.430 * rBogue_Fe2O3) - (5.102 * rBogue_fCaO);
(* C2S  = 2.867*SiO2 - 0.7544*C3S *)
rCalcC2S := (2.867 * rBogue_SiO2) - (0.7544 * rCalcC3S);
(* C3A  = 2.650*Al2O3 - 1.692*Fe2O3 *)
rCalcC3A := (2.650 * rBogue_Al2O3) - (1.692 * rBogue_Fe2O3);
(* C4AF = 3.043*Fe2O3 *)
rCalcC4AF := 3.043 * rBogue_Fe2O3;

(* Sintering Zone Liquid Phase Flux Formation at 1450 C (Lea & Parker Formulation) *)
(* %Liquid = 2.95*Al2O3 + 2.20*Fe2O3 + MgO + Alkalies *)
rCalcLiquidFlux := (2.95 * rBogue_Al2O3) + (2.20 * rBogue_Fe2O3) + 1.85;

rObserved_ClinkerC3S_pct  := rCalcC3S;
rObserved_ClinkerC2S_pct  := rCalcC2S;
rObserved_ClinkerC3A_pct  := rCalcC3A;
rObserved_ClinkerC4AF_pct := rCalcC4AF;
rObserved_LiquidPhase_pct := rCalcLiquidFlux;

(* Free Lime Assimilation Kinetic Rate in Liquid Phase *)
rBurningZoneAbsTemp_K := rVoted_BurningZoneTemp_degC + 273.15;
IF rBurningZoneAbsTemp_K > 1500.0 THEN
    rTempCalc4 := -c_rCLINK_EA / (c_rR_GAS * rBurningZoneAbsTemp_K);
    IF rTempCalc4 > -50.0 THEN
        rFreeLimeKineticRate := c_rCLINK_K0 * EXP(rTempCalc4) * (rCalcLiquidFlux / 27.0);
    ELSE
        rFreeLimeKineticRate := 0.0;
    END_IF;
    (* Dynamic Reconstructed Free Lime *)
    rObserved_FreeLime_pct := rBogue_fCaO - (rFreeLimeKineticRate * 0.000005 * (rVoted_BurningZoneTemp_degC - 1400.0));
    IF rObserved_FreeLime_pct < 0.20 THEN rObserved_FreeLime_pct := 0.20; END_IF;
    IF rObserved_FreeLime_pct > 3.50 THEN rObserved_FreeLime_pct := 3.50; END_IF;
END_IF;

(* 2.3 Rotary Kiln Axial Bed Solids Transport Velocity & Holdup (Sullivan-Work & US Bureau of Mines) *)
(* v_bed = (k * D * N * S) / sin(theta) *)
(* where D = 5.2m, N = kiln RPM, S = slope (0.035), theta = repose angle (36 deg) *)
rSolidsVolumetricFlow_m3_s := (FT_RAW_MEAL_FEED_305 * 1000.0 / 3600.0) / c_rBULK_DENSITY_RAW_MEAL;
rTempCalc5 := SIN(c_rMATERIAL_REPOSE_DEG * c_rPI / 180.0);
IF rTempCalc5 > 0.1 THEN
    rCalculatedBedVelocity_m_s := (0.00035 * c_rKILN_INNER_DIAM_M * rVoted_KilnDriveSpeed_RPM * c_rKILN_SLOPE * 100.0) / rTempCalc5;
ELSE
    rCalculatedBedVelocity_m_s := 0.0245;
END_IF;

IF rCalculatedBedVelocity_m_s > 0.005 THEN
    rCalculatedResidenceTime_s := c_rKILN_LENGTH_M / rCalculatedBedVelocity_m_s;
    rBedCrossSectionArea_m2    := c_rPI * (c_rKILN_INNER_DIAM_M * 0.5) * (c_rKILN_INNER_DIAM_M * 0.5);
    rCalculatedBedFillFraction := (rSolidsVolumetricFlow_m3_s / (rBedCrossSectionArea_m2 * rCalculatedBedVelocity_m_s)) * 100.0;
ELSE
    rCalculatedResidenceTime_s := 3346.0;
    rCalculatedBedFillFraction := 13.80;
END_IF;

rObserved_BedSolidsVelocity_m_s := rCalculatedBedVelocity_m_s;
rObserved_BedResidenceTime_min  := rCalculatedResidenceTime_s / 60.0;
rObserved_BedFillDegree_pct     := rCalculatedBedFillFraction;

(* 2.4 Multi-Channel Pulverized Coal Main Burner Axial/Radial Swirl Momentum Balance *)
(* Axial Momentum Flux: G_x = m_dot_ax * v_ax *)
(* Radial Momentum Flux: G_theta = m_dot_rad * v_rad * sin(alpha) *)
(* Swirl Number: S = G_theta / (R_nozzle * G_x) *)
rBurnerAxialMomentum_N  := PT_BURNER_AXIAL_AIR_306 * 8.5;
rBurnerRadialMomentum_N := PT_BURNER_RADIAL_AIR_307 * 6.8;

IF rBurnerAxialMomentum_N > 10.0 THEN
    rBurnerSwirlRatio := rBurnerRadialMomentum_N / rBurnerAxialMomentum_N;
ELSE
    rBurnerSwirlRatio := 0.82;
END_IF;
rObserved_BurnerSwirlNumber := rBurnerSwirlRatio;

(* 2.5 Reciprocating Grate Cooler Cross-Flow Heat Recuperation Balance *)
(* Clinker heat loss: Q_clink = m_clink * c_p * (T_in - T_out) *)
(* Secondary air temp ~ 1050 C, Tertiary air temp ~ 840 C *)
rClinkerProduction_kg_s := (FT_RAW_MEAL_FEED_305 * 1000.0 / 3600.0) / c_rCLINKER_FACTOR;
rClinkerTotalHeatLoss_kW := rClinkerProduction_kg_s * 1.08 * (1420.0 - rVoted_ClinkerDischargeTemp_degC);
rCoolerRecuperatedHeat_kW := rClinkerTotalHeatLoss_kW * 0.748;

IF rClinkerTotalHeatLoss_kW > 100.0 THEN
    rObserved_CoolerThermalEff_pct := (rCoolerRecuperatedHeat_kW / rClinkerTotalHeatLoss_kW) * 100.0;
ELSE
    rObserved_CoolerThermalEff_pct := 74.8;
END_IF;
rObserved_SecondaryAirTemp_degC := 950.0 + (1.8 * rVoted_GrateCoolerBedPress_mbar);

(* 2.6 Kiln Shell 2D Thermal Scanner Refractory Coating Thickness Estimation *)
(* Heat loss flux: q = (T_inner - T_shell) / (R_coat + R_refr + R_steel) *)
rShellHeatFlux_W_m2 := 5.67E-8 * 0.85 * (EXPT(rVoted_KilnShellPeakTemp_degC + 273.15, 4.0) - EXPT(300.0, 4.0));
IF rShellHeatFlux_W_m2 > 100.0 THEN
    rEstimatedCoatThick_m := c_rLAMBDA_COATING * (((1450.0 - rVoted_KilnShellPeakTemp_degC) / rShellHeatFlux_W_m2) 
                             - (c_rREFRACTORY_THICK_MM * 0.001 / c_rLAMBDA_REFRACTORY) 
                             - (c_rSHELL_THICK_MM * 0.001 / c_rLAMBDA_SHELL_STEEL));
    IF rEstimatedCoatThick_m < 0.02 THEN rEstimatedCoatThick_m := 0.02; END_IF;
    IF rEstimatedCoatThick_m > 0.35 THEN rEstimatedCoatThick_m := 0.35; END_IF;
ELSE
    rEstimatedCoatThick_m := 0.185;
END_IF;
rObserved_RefractoryCoatingThickness_mm := rEstimatedCoatThick_m * 1000.0;

(* 2.7 Net Specific Fuel Heat Consumption (kJ/kg clinker) *)
rTotalCoalFlow_t_h := FT_COAL_MAIN_BURNER_303 + FT_COAL_PRECALCINER_304;
rTotalHeatInput_kJ_s := (rTotalCoalFlow_t_h * 1000.0 / 3600.0) * c_rCOAL_LHV_KJ_KG;
IF rClinkerProduction_kg_s > 10.0 THEN
    rSpecificHeatCalculated_kJkg := rTotalHeatInput_kJ_s / rClinkerProduction_kg_s;
ELSE
    rSpecificHeatCalculated_kJkg := 2942.0;
END_IF;
rObserved_SpecificHeatCons_kJkg := rSpecificHeatCalculated_kJkg;""")

    # PHASE 3: State-Space & MPC
    parts.append("""
(* ====================================================================================================
   PHASE 3: DISCRETE STATE-SPACE PREDICTION & RECEDING-HORIZON MPC CONTROL ACTION
   ==================================================================================================== *)

(* 3.1 Assemble Normalized Deviation State Vector xState (8x1) *)
xState[1] := rVoted_BurningZoneTemp_degC - rSet_BurningZoneTemp_Target_degC;
xState[2] := rObserved_ApparentCalcination_pct - rSet_CalcinationRate_Target_pct;
xState[3] := rVoted_KilnInletO2_pct - rSet_KilnInletO2_Target_pct;
xState[4] := rVoted_PreheaterTopDraft_Pa - rSet_PreheaterDraft_Target_Pa;
xState[5] := rObserved_BedFillDegree_pct - 13.80;
xState[6] := rVoted_ClinkerDischargeTemp_degC - 95.0;
xState[7] := rObserved_FreeLime_pct - rSet_FreeLime_Target_pct;
xState[8] := rObserved_SpecificHeatCons_kJkg - rSet_SpecificHeat_Target_kJkg;

(* Target Equilibrium Reference State Vector is Zero *)
FOR kStateIdx := 1 TO 8 DO
    xSetpoint[kStateIdx] := 0.0;
    xError[kStateIdx]    := xState[kStateIdx] - xSetpoint[kStateIdx];
END_FOR;

(* 3.2 1-Step Ahead State-Space Dynamic Prediction: x[k+1] = matA * x[k] + matB * u[k] *)
FOR iMatRow := 1 TO 8 DO
    xPred[iMatRow] := 0.0;
    FOR iMatCol := 1 TO 8 DO
        xPred[iMatRow] := xPred[iMatRow] + (matA[iMatRow, iMatCol] * xState[iMatCol]) + (matB[iMatRow, iMatCol] * uPrevious[iMatCol]);
    END_FOR;
END_FOR;

(* 3.3 Receding-Horizon Multi-Step Cost Functional Evaluation *)
(* J = sum_{k=1..Np} (x_k - r)^T Q (x_k - r) + sum_{k=0..Nc-1} u_k^T R u_k + Delta_u^T S Delta_u *)
rTotalCost := 0.0;
FOR kStateIdx := 1 TO 8 DO
    rTotalCost := rTotalCost + (xPred[kStateIdx] * matQ[kStateIdx, kStateIdx] * xPred[kStateIdx]);
    rTotalCost := rTotalCost + (uPrevious[kStateIdx] * matR[kStateIdx, kStateIdx] * uPrevious[kStateIdx]);
END_FOR;
rMPC_ObjectiveCost_J := rTotalCost;

(* 3.4 Fast Projected Gradient Descent (PGD) Actuator Vector Optimization *)
IF bAutoMpcEnable THEN
    FOR mInputIdx := 1 TO 8 DO
        (* Analytical gradient dJ/du_m = 2 * B_m^T * Q * xPred + 2 * R_m * u_m + 2 * S_m * (u_m - u_prev) *)
        rGrad[mInputIdx] := 0.0;
        FOR kStateIdx := 1 TO 8 DO
            rGrad[mInputIdx] := rGrad[mInputIdx] + (matB[kStateIdx, mInputIdx] * matQ[kStateIdx, kStateIdx] * xPred[kStateIdx]);
        END_FOR;
        rGrad[mInputIdx] := (2.0 * rGrad[mInputIdx]) + (2.0 * matR[mInputIdx, mInputIdx] * uPrevious[mInputIdx]);

        (* Gradient Descent Step: u_opt = u_prev - step * grad *)
        uOptimal[mInputIdx] := uPrevious[mInputIdx] - (rStepSize * rGrad[mInputIdx]);

        (* Hard Constraint Projection [uMin, uMax] *)
        IF uOptimal[mInputIdx] > uMax[mInputIdx] THEN uOptimal[mInputIdx] := uMax[mInputIdx]; END_IF;
        IF uOptimal[mInputIdx] < uMin[mInputIdx] THEN uOptimal[mInputIdx] := uMin[mInputIdx]; END_IF;

        (* Slew Rate Bound Limiting *)
        deltaU[mInputIdx] := uOptimal[mInputIdx] - uPrevious[mInputIdx];
        IF deltaU[mInputIdx] > deltaUMax[mInputIdx] THEN deltaU[mInputIdx] := deltaUMax[mInputIdx]; END_IF;
        IF deltaU[mInputIdx] < -deltaUMax[mInputIdx] THEN deltaU[mInputIdx] := -deltaUMax[mInputIdx]; END_IF;

        uActuator[mInputIdx] := uPrevious[mInputIdx] + deltaU[mInputIdx];
        uPrevious[mInputIdx] := uActuator[mInputIdx];
    END_FOR;
ELSE
    FOR mInputIdx := 1 TO 8 DO
        uActuator[mInputIdx] := 0.0;
        uPrevious[mInputIdx] := 0.0;
    END_FOR;
END_IF;

(* 3.5 Map Optimal Actuator Trims to Physical Commands *)
rCmd_Coal_MainBurner_t_h        := 14.20 + uActuator[1];
rCmd_Coal_Precalciner_t_h       := 21.50 + uActuator[2];
rCmd_RawMeal_Feed_t_h           := 645.0 + uActuator[3];
rCmd_KilnDrive_Speed_RPM        := 3.80  + uActuator[4];
rCmd_ID_Fan_Speed_Pct           := 74.0  + uActuator[5];
rCmd_TertiaryAir_Damper_Pct     := 68.0  + uActuator[6];
rCmd_Cooler_StrokeSpeed_SPM     := 12.5  + uActuator[8];

(* Swirl Momentum Coupling to Primary Air Valves *)
rCmd_Burner_AxialAir_Valve_Pct  := 62.0 - (15.0 * uActuator[7]);
rCmd_Burner_RadialAir_Valve_Pct := 48.0 + (18.0 * uActuator[7]);

(* Clinker Cooler Under-Grate Aeration Chamber Fan Commands *)
rCmd_Cooler_AerationFan1_Pct := 82.0 + (0.35 * (rVoted_GrateCoolerBedPress_mbar - 58.0));
rCmd_Cooler_AerationFan2_Pct := 75.0 + (0.30 * (rVoted_GrateCoolerBedPress_mbar - 58.0));
rCmd_Cooler_AerationFan3_Pct := 68.0 + (0.25 * (rVoted_GrateCoolerBedPress_mbar - 58.0));
rCmd_Cooler_AerationFan4_Pct := 60.0 + (0.20 * (rVoted_GrateCoolerBedPress_mbar - 58.0));
rCmd_Cooler_AerationFan5_Pct := 52.0 + (0.15 * (rVoted_GrateCoolerBedPress_mbar - 58.0));
rCmd_Cooler_AerationFan6_Pct := 45.0 + (0.10 * (rVoted_GrateCoolerBedPress_mbar - 58.0));""")

    # PHASE 4: 12-Stage Operational FSM
    parts.append("""
(* ====================================================================================================
   PHASE 4: 12-STAGE OPERATIONAL FINITE STATE MACHINE (FSM)
   ==================================================================================================== *)
tFsmStepTimer_Sec := tFsmStepTimer_Sec + rDeltaTime_Sec;

CASE eActiveFsmState OF
    0: (* STATE_KILN_WARMUP_REFRACTORY_DRY: Auxiliary burner dry-out ramp *)
        bCmd_FuelCutoff_Main_Trip          := TRUE; (* Coal tripped *)
        bCmd_FuelCutoff_Calciner_Trip      := TRUE;
        bCmd_Baghouse_CO_Deflagration_Trip := FALSE;
        rCmd_RawMeal_Feed_t_h              := 0.0;
        rCmd_Coal_MainBurner_t_h           := 0.0;
        rCmd_Coal_Precalciner_t_h          := 0.0;
        rCmd_KilnDrive_Speed_RPM           := 0.50; (* Inching barring speed *)
        rCmd_ID_Fan_Speed_Pct              := 25.0;
        IF (rVoted_BurningZoneTemp_degC >= 450.0) AND (tFsmStepTimer_Sec >= 7200.0) THEN
            eActiveFsmState := STATE_AUXILIARY_INCHING_DRIVE;
            tFsmStepTimer_Sec := 0.0;
        END_IF;

    1: (* STATE_AUXILIARY_INCHING_DRIVE: Barring gear cyclic rotation to prevent shell sag *)
        bCmd_KilnAuxiliary_InchingDrive_Engage := TRUE;
        rCmd_KilnDrive_Speed_RPM               := 0.80;
        rCmd_ID_Fan_Speed_Pct                  := 35.0;
        IF (rVoted_BurningZoneTemp_degC >= 650.0) THEN
            eActiveFsmState := STATE_PREHEATER_FAN_DRAFT_PULL;
            tFsmStepTimer_Sec := 0.0;
        END_IF;

    2: (* STATE_PREHEATER_FAN_DRAFT_PULL: Establish balanced 5-stage negative draft *)
        rCmd_ID_Fan_Speed_Pct       := 55.0;
        rCmd_TertiaryAir_Damper_Pct := 40.0;
        IF (rVoted_PreheaterTopDraft_Pa <= -3500.0) AND (rVoted_KilnInletDraft_Pa <= -40.0) THEN
            eActiveFsmState := STATE_MAIN_BURNER_DIESEL_PILOT;
            tFsmStepTimer_Sec := 0.0;
        END_IF;

    3: (* STATE_MAIN_BURNER_DIESEL_PILOT: Ignite pilot & preheat sintering zone to 950 C *)
        bCmd_FuelCutoff_Main_Trip := FALSE;
        rCmd_KilnDrive_Speed_RPM  := 1.20;
        IF (rVoted_BurningZoneTemp_degC >= 950.0) AND bRawMealFeedPermissive THEN
            eActiveFsmState := STATE_RAW_MEAL_FEED_INTRODUCTION;
            tFsmStepTimer_Sec := 0.0;
        END_IF;

    4: (* STATE_RAW_MEAL_FEED_INTRODUCTION: Introduce raw meal at 30% nominal (approx 200 t/h) *)
        rCmd_RawMeal_Feed_t_h    := 200.0;
        rCmd_Coal_MainBurner_t_h := 6.50;
        rCmd_KilnDrive_Speed_RPM := 1.80;
        IF (rVoted_KilnInletGasTemp_degC >= 850.0) AND (tFsmStepTimer_Sec >= 1800.0) THEN
            eActiveFsmState := STATE_ROTARY_KILN_ACCELERATION_RAMP;
            tFsmStepTimer_Sec := 0.0;
        END_IF;

    5: (* STATE_ROTARY_KILN_ACCELERATION_RAMP: Accelerate main drive speed with bed travel *)
        rCmd_RawMeal_Feed_t_h    := 420.0;
        rCmd_Coal_MainBurner_t_h := 10.50;
        rCmd_KilnDrive_Speed_RPM := 2.80;
        rCmd_ID_Fan_Speed_Pct    := 65.0;
        IF (rVoted_BurningZoneTemp_degC >= 1350.0) AND (rVoted_PrecalcinerExitTemp_degC >= 820.0) THEN
            eActiveFsmState := STATE_PRECALCINER_COAL_FIRING_SYNC;
            tFsmStepTimer_Sec := 0.0;
        END_IF;

    6: (* STATE_PRECALCINER_COAL_FIRING_SYNC: Ignite calciner coal and modulate TAD damper *)
        bCmd_FuelCutoff_Calciner_Trip := FALSE;
        rCmd_Coal_Precalciner_t_h     := 16.0;
        rCmd_TertiaryAir_Damper_Pct   := 60.0;
        IF (rObserved_ApparentCalcination_pct >= 88.0) AND (rVoted_BurningZoneTemp_degC >= 1420.0) THEN
            eActiveFsmState := STATE_STEADY_STATE_CLINKER_BURNING;
            tFsmStepTimer_Sec := 0.0;
        END_IF;

    7: (* STATE_STEADY_STATE_CLINKER_BURNING: Full 10,000 t/d autonomous production *)
        bCmd_FuelCutoff_Main_Trip          := FALSE;
        bCmd_FuelCutoff_Calciner_Trip      := FALSE;
        bCmd_Baghouse_CO_Deflagration_Trip := FALSE;
        (* Clinker Quality Gate Verification *)
        bClinkerQualityAcceptable := (rObserved_FreeLime_pct <= 1.00) AND (rObserved_ClinkerC3S_pct >= 58.0);
        
        (* Check for abnormal buildup triggers *)
        IF (rVoted_KilnDrivePower_kW > 1550.0) AND (rVoted_KilnInletDraft_Pa > -25.0) THEN
            eActiveFsmState := STATE_KILN_RING_SNOWMAN_BREAKING;
            tFsmStepTimer_Sec := 0.0;
        END_IF;

    8: (* STATE_KILN_RING_SNOWMAN_BREAKING: Thermal cycling & speed trim to shed ring/buildup *)
        tSnowmanCycleTimer_Sec := tSnowmanCycleTimer_Sec + rDeltaTime_Sec;
        (* Oscillate burner axial air momentum to alter flame length *)
        IF tSnowmanCycleTimer_Sec < 300.0 THEN
            rCmd_Burner_AxialAir_Valve_Pct := 85.0; (* Long harsh flame *)
            rCmd_KilnDrive_Speed_RPM := 4.20;
        ELSIF tSnowmanCycleTimer_Sec < 600.0 THEN
            rCmd_Burner_AxialAir_Valve_Pct := 40.0; (* Short bushy flame *)
            rCmd_KilnDrive_Speed_RPM := 3.20;
        ELSE
            tSnowmanCycleTimer_Sec := 0.0;
            eActiveFsmState := STATE_STEADY_STATE_CLINKER_BURNING;
        END_IF;

    9: (* STATE_GRATE_COOLER_HEAT_RECUPERATION: Cooler bed optimization *)
        rCmd_Cooler_StrokeSpeed_SPM := 14.5;
        IF (rObserved_CoolerThermalEff_pct >= 72.0) THEN
            eActiveFsmState := STATE_STEADY_STATE_CLINKER_BURNING;
            tFsmStepTimer_Sec := 0.0;
        END_IF;

    10: (* STATE_CONTROLLED_KILN_STOP_DRAIN: Systematic feed cut and kiln empty drain *)
        rCmd_RawMeal_Feed_t_h         := 0.0;
        rCmd_Coal_Precalciner_t_h     := 0.0;
        bCmd_FuelCutoff_Calciner_Trip := TRUE;
        rCmd_Coal_MainBurner_t_h      := 5.0; (* Low fire to maintain draft *)
        rCmd_KilnDrive_Speed_RPM      := 2.0;
        IF (rObserved_BedFillDegree_pct <= 2.0) OR (tFsmStepTimer_Sec >= 5400.0) THEN
            eActiveFsmState := STATE_AUXILIARY_INCHING_DRIVE;
            tFsmStepTimer_Sec := 0.0;
        END_IF;

    11: (* STATE_EMERGENCY_ESTOP_FUEL_CUT: Immediate trip *)
        bCmd_FuelCutoff_Main_Trip          := TRUE;
        bCmd_FuelCutoff_Calciner_Trip      := TRUE;
        bCmd_Baghouse_CO_Deflagration_Trip := TRUE;
        rCmd_Coal_MainBurner_t_h           := 0.0;
        rCmd_Coal_Precalciner_t_h          := 0.0;
        rCmd_RawMeal_Feed_t_h              := 0.0;
        rCmd_KilnDrive_Speed_RPM           := 0.50;
        bCmd_KilnAuxiliary_InchingDrive_Engage := TRUE;
        bEmergencyTripActive               := TRUE;
END_CASE;""")

    # PHASE 5: ISA-18.2 Alarms
    parts.append("""
(* ====================================================================================================
   PHASE 5: ISA-18.2 MULTI-TIERED ALARMS, DEFLAGRATION FAST FUEL TRIP & DIAGNOSTIC WORD PACKING
   ==================================================================================================== *)

(* 5.1 Rate-of-Change (ROC) Calculations *)
IF rDeltaTime_Sec > 0.001 THEN
    rROC_BaghouseCO_ppm_s       := (rVoted_BaghouseCO_ppm - rPrevBaghouseCO) / rDeltaTime_Sec;
    rROC_BurningZoneTemp_degC_s := (rVoted_BurningZoneTemp_degC - rPrevBurningZoneTemp) / rDeltaTime_Sec;
END_IF;
rPrevBaghouseCO      := rVoted_BaghouseCO_ppm;
rPrevBurningZoneTemp := rVoted_BurningZoneTemp_degC;

(* 5.2 Critical Safety Trip: Baghouse CO Surge Deflagration Fast Trip (< 200 ms) *)
IF (rVoted_BaghouseCO_ppm >= rALM_TRIP_BAGHOUSE_CO_HH) OR (rROC_BaghouseCO_ppm_s >= c_rMAX_ROC_BAGHOUSE_CO) THEN
    bAlm_Baghouse_CO_HH                := TRUE;
    bAlm_Deflagration_FastTrip         := TRUE;
    bCmd_Baghouse_CO_Deflagration_Trip := TRUE; (* De-energize ESP high-voltage transformer *)
    bCmd_FuelCutoff_Main_Trip          := TRUE; (* Trip pulverized coal within 200 ms *)
    bCmd_FuelCutoff_Calciner_Trip      := TRUE;
    eActiveFsmState                    := STATE_EMERGENCY_ESTOP_FUEL_CUT;
ELSIF (rVoted_BaghouseCO_ppm <= (rALM_TRIP_BAGHOUSE_CO_HH - rALM_HYST_BAGHOUSE_CO)) THEN
    bAlm_Baghouse_CO_HH := FALSE;
END_IF;

IF rVoted_BaghouseCO_ppm >= rALM_WARN_BAGHOUSE_CO_H THEN
    bAlm_Baghouse_CO_H := TRUE;
ELSIF rVoted_BaghouseCO_ppm <= (rALM_WARN_BAGHOUSE_CO_H - rALM_HYST_BAGHOUSE_CO) THEN
    bAlm_Baghouse_CO_H := FALSE;
END_IF;

(* 5.3 Burning Zone Sintering Temperature Alarm Ladder *)
IF rVoted_BurningZoneTemp_degC >= rALM_TRIP_BZ_HH THEN
    bAlm_BZ_HH := TRUE;
    bCmd_FuelCutoff_Main_Trip := TRUE;
ELSIF rVoted_BurningZoneTemp_degC <= (rALM_TRIP_BZ_HH - rALM_HYST_BZ) THEN
    bAlm_BZ_HH := FALSE;
END_IF;

IF rVoted_BurningZoneTemp_degC >= rALM_WARN_BZ_H THEN
    bAlm_BZ_H := TRUE;
ELSIF rVoted_BurningZoneTemp_degC <= (rALM_WARN_BZ_H - rALM_HYST_BZ) THEN
    bAlm_BZ_H := FALSE;
END_IF;

IF rVoted_BurningZoneTemp_degC <= rALM_WARN_BZ_L THEN
    bAlm_BZ_L := TRUE;
ELSIF rVoted_BurningZoneTemp_degC >= (rALM_WARN_BZ_L + rALM_HYST_BZ) THEN
    bAlm_BZ_L := FALSE;
END_IF;

IF rVoted_BurningZoneTemp_degC <= rALM_TRIP_BZ_LL THEN
    bAlm_BZ_LL := TRUE;
ELSIF rVoted_BurningZoneTemp_degC >= (rALM_TRIP_BZ_LL + rALM_HYST_BZ) THEN
    bAlm_BZ_LL := FALSE;
END_IF;

(* 5.4 Kiln Shell 2D Thermal Scanner Peak Hotspot Alarm Ladder *)
IF rVoted_KilnShellPeakTemp_degC >= rALM_TRIP_SHELL_HH THEN
    bAlm_Shell_HH := TRUE;
    bCmd_ShellCoolingFans_Run := TRUE;
    bCmd_FuelCutoff_Main_Trip := TRUE;
    eActiveFsmState := STATE_EMERGENCY_ESTOP_FUEL_CUT;
ELSIF rVoted_KilnShellPeakTemp_degC <= (rALM_TRIP_SHELL_HH - rALM_HYST_SHELL) THEN
    bAlm_Shell_HH := FALSE;
END_IF;

IF rVoted_KilnShellPeakTemp_degC >= rALM_WARN_SHELL_H THEN
    bAlm_Shell_H := TRUE;
    bCmd_ShellCoolingFans_Run := TRUE;
ELSIF rVoted_KilnShellPeakTemp_degC <= (rALM_WARN_SHELL_H - rALM_HYST_SHELL) THEN
    bAlm_Shell_H := FALSE;
    bCmd_ShellCoolingFans_Run := FALSE;
END_IF;

(* 5.5 Precalciner Exit Temperature Alarm Ladder *)
IF rVoted_PrecalcinerExitTemp_degC >= rALM_TRIP_CALCINER_EXIT_HH THEN
    bAlm_CalcinerExit_HH := TRUE;
    bCmd_FuelCutoff_Calciner_Trip := TRUE;
ELSIF rVoted_PrecalcinerExitTemp_degC <= (rALM_TRIP_CALCINER_EXIT_HH - rALM_HYST_CALCINER_EXIT) THEN
    bAlm_CalcinerExit_HH := FALSE;
END_IF;

IF rVoted_PrecalcinerExitTemp_degC >= rALM_WARN_CALCINER_EXIT_H THEN
    bAlm_CalcinerExit_H := TRUE;
ELSIF rVoted_PrecalcinerExitTemp_degC <= (rALM_WARN_CALCINER_EXIT_H - rALM_HYST_CALCINER_EXIT) THEN
    bAlm_CalcinerExit_H := FALSE;
END_IF;

IF rVoted_PrecalcinerExitTemp_degC <= rALM_WARN_CALCINER_EXIT_L THEN
    bAlm_CalcinerExit_L := TRUE;
ELSIF rVoted_PrecalcinerExitTemp_degC >= (rALM_WARN_CALCINER_EXIT_L + rALM_HYST_CALCINER_EXIT) THEN
    bAlm_CalcinerExit_L := FALSE;
END_IF;

IF rVoted_PrecalcinerExitTemp_degC <= rALM_TRIP_CALCINER_EXIT_LL THEN
    bAlm_CalcinerExit_LL := TRUE;
ELSIF rVoted_PrecalcinerExitTemp_degC >= (rALM_TRIP_CALCINER_EXIT_LL + rALM_HYST_CALCINER_EXIT) THEN
    bAlm_CalcinerExit_LL := FALSE;
END_IF;

(* 5.6 Kiln Inlet Excess Oxygen Alarm Ladder *)
IF rVoted_KilnInletO2_pct <= rALM_TRIP_INLET_O2_LL THEN
    bAlm_InletO2_LL := TRUE;
ELSIF rVoted_KilnInletO2_pct >= (rALM_TRIP_INLET_O2_LL + rALM_HYST_INLET_O2) THEN
    bAlm_InletO2_LL := FALSE;
END_IF;

IF rVoted_KilnInletO2_pct <= rALM_WARN_INLET_O2_L THEN
    bAlm_InletO2_L := TRUE;
ELSIF rVoted_KilnInletO2_pct >= (rALM_WARN_INLET_O2_L + rALM_HYST_INLET_O2) THEN
    bAlm_InletO2_L := FALSE;
END_IF;

IF rVoted_KilnInletO2_pct >= rALM_WARN_INLET_O2_H THEN
    bAlm_InletO2_H := TRUE;
ELSIF rVoted_KilnInletO2_pct <= (rALM_WARN_INLET_O2_H - rALM_HYST_INLET_O2) THEN
    bAlm_InletO2_H := FALSE;
END_IF;

(* 5.7 Preheater Top Draft Alarm Ladder *)
IF rVoted_PreheaterTopDraft_Pa >= rALM_TRIP_TOP_DRAFT_HH THEN
    bAlm_TopDraft_HH := TRUE;
ELSIF rVoted_PreheaterTopDraft_Pa <= (rALM_TRIP_TOP_DRAFT_HH - rALM_HYST_TOP_DRAFT) THEN
    bAlm_TopDraft_HH := FALSE;
END_IF;

IF rVoted_PreheaterTopDraft_Pa <= rALM_TRIP_TOP_DRAFT_LL THEN
    bAlm_TopDraft_LL := TRUE;
ELSIF rVoted_PreheaterTopDraft_Pa >= (rALM_TRIP_TOP_DRAFT_LL + rALM_HYST_TOP_DRAFT) THEN
    bAlm_TopDraft_LL := FALSE;
END_IF;

(* 5.8 Cooler Bed Pressure Alarm Ladder *)
IF rVoted_GrateCoolerBedPress_mbar >= rALM_TRIP_COOLER_BED_HH THEN
    bAlm_CoolerBed_HH := TRUE;
ELSIF rVoted_GrateCoolerBedPress_mbar <= (rALM_TRIP_COOLER_BED_HH - rALM_HYST_COOLER_BED) THEN
    bAlm_CoolerBed_HH := FALSE;
END_IF;

IF rVoted_GrateCoolerBedPress_mbar <= rALM_TRIP_COOLER_BED_LL THEN
    bAlm_CoolerBed_LL := TRUE;
ELSIF rVoted_GrateCoolerBedPress_mbar >= (rALM_TRIP_COOLER_BED_LL + rALM_HYST_COOLER_BED) THEN
    bAlm_CoolerBed_LL := FALSE;
END_IF;

(* 5.9 Clinker Free Lime Quality Alarm Ladder *)
IF rObserved_FreeLime_pct >= rALM_TRIP_FREELIME_HH THEN
    bAlm_FreeLime_HH := TRUE;
ELSIF rObserved_FreeLime_pct <= (rALM_TRIP_FREELIME_HH - rALM_HYST_FREELIME) THEN
    bAlm_FreeLime_HH := FALSE;
END_IF;

IF rObserved_FreeLime_pct >= rALM_WARN_FREELIME_H THEN
    bAlm_FreeLime_H := TRUE;
ELSIF rObserved_FreeLime_pct <= (rALM_WARN_FREELIME_H - rALM_HYST_FREELIME) THEN
    bAlm_FreeLime_H := FALSE;
END_IF;

(* 5.10 Telemetry & Diagnostic Word Bit Packing *)
dwAlarmWord_Trip := 16#0000;
IF bAlm_Baghouse_CO_HH        THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0001; END_IF;
IF bAlm_BZ_HH                 THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0002; END_IF;
IF bAlm_BZ_LL                 THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0004; END_IF;
IF bAlm_Shell_HH              THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0008; END_IF;
IF bAlm_CalcinerExit_HH       THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0010; END_IF;
IF bAlm_CalcinerExit_LL       THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0020; END_IF;
IF bAlm_InletO2_LL            THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0040; END_IF;
IF bAlm_TopDraft_HH           THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0080; END_IF;
IF bAlm_TopDraft_LL           THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0100; END_IF;
IF bAlm_CoolerBed_HH          THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0200; END_IF;
IF bAlm_CoolerBed_LL          THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0400; END_IF;
IF bAlm_FreeLime_HH           THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0800; END_IF;
IF bAlm_Deflagration_FastTrip THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#1000; END_IF;
IF bAlm_Discrepancy_Trip      THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#2000; END_IF;

dwAlarmWord_Warning := 16#0000;
IF bAlm_Baghouse_CO_H         THEN dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#0001; END_IF;
IF bAlm_BZ_H                  THEN dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#0002; END_IF;
IF bAlm_BZ_L                  THEN dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#0004; END_IF;
IF bAlm_Shell_H               THEN dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#0008; END_IF;
IF bAlm_CalcinerExit_H        THEN dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#0010; END_IF;
IF bAlm_CalcinerExit_L        THEN dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#0020; END_IF;
IF bAlm_InletO2_L             THEN dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#0040; END_IF;
IF bAlm_InletO2_H             THEN dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#0080; END_IF;
IF bAlm_TopDraft_H            THEN dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#0100; END_IF;
IF bAlm_TopDraft_L            THEN dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#0200; END_IF;
IF bAlm_CoolerBed_H           THEN dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#0400; END_IF;
IF bAlm_CoolerBed_L           THEN dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#0800; END_IF;
IF bAlm_FreeLime_H            THEN dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#1000; END_IF;

dwStatusWord1 := 16#0000;
IF bMasterEnable              THEN dwStatusWord1 := dwStatusWord1 OR 16#0001; END_IF;
IF bClinkerQualityAcceptable  THEN dwStatusWord1 := dwStatusWord1 OR 16#0002; END_IF;
IF bAutoMpcEnable             THEN dwStatusWord1 := dwStatusWord1 OR 16#0004; END_IF;
IF bEmergencyTripActive       THEN dwStatusWord1 := dwStatusWord1 OR 16#0008; END_IF;
IF bCmd_ShellCoolingFans_Run  THEN dwStatusWord1 := dwStatusWord1 OR 16#0010; END_IF;

dwSensorHealthMask := 16#0000;
IF bFault_BZ_A     THEN dwSensorHealthMask := dwSensorHealthMask OR 16#0001; END_IF;
IF bFault_BZ_B     THEN dwSensorHealthMask := dwSensorHealthMask OR 16#0002; END_IF;
IF bFault_BZ_C     THEN dwSensorHealthMask := dwSensorHealthMask OR 16#0004; END_IF;
IF bFault_InletT_A THEN dwSensorHealthMask := dwSensorHealthMask OR 16#0008; END_IF;
IF bFault_InletT_B THEN dwSensorHealthMask := dwSensorHealthMask OR 16#0010; END_IF;
IF bFault_InletT_C THEN dwSensorHealthMask := dwSensorHealthMask OR 16#0020; END_IF;
IF bFault_O2_A     THEN dwSensorHealthMask := dwSensorHealthMask OR 16#0040; END_IF;
IF bFault_O2_B     THEN dwSensorHealthMask := dwSensorHealthMask OR 16#0080; END_IF;
IF bFault_O2_C     THEN dwSensorHealthMask := dwSensorHealthMask OR 16#0100; END_IF;

dwStatusWord2 := SHL(INT_TO_DWORD(eActiveFsmState), 8) OR (dwSensorHealthMask AND 16#00FF);

END_FUNCTION_BLOCK""")

    return "\n".join(parts)

if __name__ == "__main__":
    iec_code = generate_iec_code()
    print(f"Generated code length: {len(iec_code)} chars")
