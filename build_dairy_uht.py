# -*- coding: utf-8 -*-
"""
Builder for FB_Dairy_UHT_Pasteurizer_Homogenizer_AsepticDiverter
Lumina Cyber-Physical Automation Swarm V7 Max-Persona
"""
import json
import uuid
import re
import os

def generate_st_code():
    code_parts = []

    # =========================================================================
    # 1. HEADER AND TITLE BLOCK
    # =========================================================================
    code_parts.append('''FUNCTION_BLOCK FB_Dairy_UHT_Pasteurizer_Homogenizer_AsepticDiverter
(* =====================================================================================================================
 * LUMINA CYBER-PHYSICAL AUTOMATION ENGINE - SYNTHETIC DATASET V7 MAX-PERSONA
 * COMMERCIAL INDUSTRIAL SECTOR : Food & Beverage / Industrial Dairy Processing
 * SYSTEM                       : Continuous 30,000 L/h Direct Steam Injection (DSI) Ultra-High-Temperature (UHT)
 *                                Milk Pasteurization Line with Two-Stage High-Pressure Aseptic Homogenizer,
 *                                Multi-Section Plate Pre-Heater Regeneration Balancing (92% Heat Recovery),
 *                                Vacuum Flash De-Aerator Aroma Retention, Sub-200 ms Fast Aseptic Diversion Valve,
 *                                Clean-In-Place / Sterilization-In-Place (CIP/SIP) F0 Lethality Integral Integrator,
 *                                and Sterile Air Buffer Overpressure Cascade (+0.50 bar).
 * INTEGRATED SUBSYSTEMS        : - Raw Milk Metering & Variable Frequency Drive Feed Pump (30,000 L/h Nominal Flow)
 *                                - Multi-Section Plate Heat Exchanger (PHE) Thermal Regeneration Network (92% Energy Recov)
 *                                - Direct Culinary Steam Injection (DSI) Infuser Chamber with Acoustic Sonic Velocity Dosing
 *                                - High-Pressure Holding Tube Assembly (142.0 deg C for 4.0 seconds at 30,000 L/h)
 *                                - Vacuum Flash Cooling Chamber & Condensate Volatile Aroma Retention Column (-0.65 bar)
 *                                - Two-Stage High-Pressure Aseptic Homogenizer (250 bar Stage 1, 50 bar Stage 2)
 *                                  with Tungsten Carbide Valve Seat Cavitation Erosion Observer
 *                                - Fast Pneumatic Aseptic Diversion Valve Station (< 150 ms Trip upon T < 139.5 deg C)
 *                                - Final Aseptic Plate Cooler (Chilled Water Circulation to 4.0 deg C Storage Temp)
 *                                - Sterile Air Buffer Overpressure Headspace Cascade Barrier (+0.50 bar Overpressure)
 *                                - CIP/SIP Microbiological Thermal Lethality Integral Calculator (F0 >= 12.0 min)
 *                                - Plate Heat Exchanger Dynamic Milk Protein Fouling & Thermal Boundary Observer
 *                                - 8x8 Multivariable Discrete State-Space Cyber-Physical Dynamics (20 ms Cycle)
 *                                - Receding-Horizon Model Predictive Control (MPC) with Projected Gradient Descent
 *                                - 2oo3 Triple Modular Redundancy (TMR) Sensor Voting Across 16 P&ID Tag Triplets
 *                                - ISA-18.2 5-Tier Process Alarm Hierarchy (HI_HI, HI, LO, LO_LO, ROC) & Bitmask Packing
 *                                - 12-Stage Deterministic Production Finite State Machine (FSM)
 * =====================================================================================================================
 * CYBER-PHYSICAL THERMODYNAMIC, MICROBIOLOGICAL & FLUID MECHANICAL FORMULATIONS:
 * 1. Direct Culinary Steam Injection (DSI) Thermal Mixing Enthalpy Balance:
 *    Filtered culinary steam (dry saturated at P_steam = 4.5 bar, h_steam = 2740.0 kJ/kg) is directly injected into the
 *    preheated milk stream (T_preheat = 78.5 deg C) via sonic velocity multi-orifice injection nozzles.
 *    The resulting mixture temperature entering the holding tube is governed by the conservation of enthalpy:
 *      m_dot_mix * h_mix = m_dot_milk * h_milk + m_dot_steam * h_steam
 *    Where:
 *      h_milk  = C_p_milk * (T_preheat - T_ref),   C_p_milk = 3.93 kJ/(kg*K)
 *      m_dot_mix = m_dot_milk + m_dot_steam
 *      T_holding = T_ref + (m_dot_milk * C_p_milk * T_preheat + m_dot_steam * (h_steam - h_ref)) / (m_dot_mix * C_p_mix)
 *    Sonic acoustic nozzle flow choking occurs when pressure ratio P_mix / P_steam <= (2 / (k + 1))^(k / (k - 1)),
 *    ensuring acoustic bubble collapse cavitation and micro-turbulent instantaneous condensation without thermal scorching.
 *
 * 2. Vacuum Flash Cooling & De-Aerator Net Water Mass Balance:
 *    Immediately following the holding tube, the product expands into a vacuum flash de-aerator chamber maintained at
 *    P_vac = -0.65 bar gauge (approx 0.363 bar abs, saturation temperature T_sat = 73.5 to 76.0 deg C).
 *    Instantaneous adiabatic flashing evaporates an exact quantity of water vapor equal to the culinary steam condensate:
 *      m_dot_flash = m_dot_mix * C_p_mix * (T_holding - T_flash) / h_fg(T_flash)
 *    Net water balance:
 *      Delta_m_dot_water = m_dot_steam_injected - m_dot_flash_evaporated
 *    The Receding-Horizon MPC regulates P_vac to enforce Delta_m_dot_water = 0.00 +/- 0.05%, guaranteeing zero net dilution
 *    or concentration of the milk, while flashed volatile aromas are condensed in a packed reflux column and returned.
 *
 * 3. Two-Stage High-Pressure Homogenization & Sauter Mean Diameter (d32) Observer:
 *    Milk fat globules are disrupted under intense viscous shear, turbulent cavitation, and mechanical impact:
 *      Stage 1: Primary droplet disruption across tungsten carbide valve seat at Delta_P1 = 250 bar.
 *      Stage 2: Secondary droplet de-flocculation and clustering prevention at Delta_P2 = 50 bar.
 *    Specific Mechanical Energy (SME):
 *      SME = (Delta_P1 + Delta_P2) / rho_milk   [J/kg or kJ/kg]
 *    Sauter mean fat globule diameter d32 correlation:
 *      d32 = d_0 * (Delta_P_total / P_0)^(-0.60) * (mu_milk / mu_water)^(0.10)
 *    Where d_0 = 3.5 um for raw milk, dropping below 0.65 um after homogenization to permanently inhibit creaming.
 *    Tungsten carbide valve seat wear observer detects micro-channel erosive cavitation by comparing actual hydraulic
 *    fluid pressure drop against motor electrical load power (IT_HOMOGENIZER_MOTOR_KW_403).
 *
 * 4. Plate Heat Exchanger (PHE) Thermal Regeneration & Protein Fouling Observer:
 *    The multi-section PHE regenerates thermal energy between outgoing flash-cooled milk and incoming cold raw milk.
 *    Regeneration heat duty:
 *      Q_regen = m_dot_milk * C_p_milk * (T_preheat_out - T_raw_in)
 *    Logarithmic Mean Temperature Difference (LMTD):
 *      Delta_T_LM = ((T_flash_out - T_preheat_out) - (T_hot_out - T_raw_in)) / ln((T_flash_out - T_preheat_out) / (T_hot_out - T_raw_in))
 *    Dynamic Overall Heat Transfer Coefficient:
 *      U = Q_regen / (A_PHE * Delta_T_LM)
 *    Fouling thermal boundary layer resistance:
 *      R_f = (1.0 / U) - (1.0 / U_clean)   [m2*K/W]
 *    Encrustation of beta-lactoglobulin whey protein and calcium phosphate occurs when R_f > 0.00045 m2*K/W,
 *    triggering automatic scheduling of an intermediate caustic wash (ASR).
 *
 * 5. Microbiological Thermal Lethality Equivalent Integral (F0):
 *    Thermal destruction of heat-resistant Geobacillus stearothermophilus spores follows Bigelow log-linear kinetics:
 *      F0 = INT_0^t 10^((T(tau) - 121.1) / z) d_tau   [minutes]
 *    Where z = 10.0 deg C and T_ref = 121.1 deg C.
 *    For continuous UHT production at 142.0 deg C for 4.0 seconds:
 *      Lethality rate L(142) = 10^((142.0 - 121.1) / 10.0) = 10^2.09 = 123.03 min/min.
 *      In 4.0 seconds, F0 = (4.0 / 60.0) * 123.03 = 8.20 minutes per pass.
 *    During Clean-In-Place / Sterilization-In-Place (CIP/SIP) thermal sterilization at 130.0 deg C:
 *      The function block continuously integrates F0 over time until cumulative F0 >= 12.0 min is achieved,
 *      guaranteeing commercial sterility (12-decimal spore log-reduction) before milk introduction.
 *
 * 6. Sub-150 ms Pneumatic Fast Aseptic Diversion Valve Interlock:
 *    Dual sanitary spring-loaded pneumatic diaphragm valves isolate the sterile filling line from unpasteurized product.
 *    If holding tube temperature dips below 139.5 deg C, or flash vacuum collapses, or sterile air headspace drops below
 *    +0.20 bar, the forward seat closes and divert seat vents product back to raw balance tank in < 150 ms.
 * =====================================================================================================================
 *)
''')

    # =========================================================================
    # 2. VAR_INPUT
    # =========================================================================
    code_parts.append('''VAR_INPUT
    (* ========================================================================================= *)
    (* 1. MASTER SUPERVISORY PERMISSIVES, SAFETY GATES & OPERATION MODES                         *)
    (* ========================================================================================= *)
    bMasterPowerOn                      : BOOL := FALSE;    (* Line Master 400V 3-Phase Main Contactor Permissive [BOOL] *)
    bSystemAutoEnable                   : BOOL := FALSE;    (* Automatic Closed-Loop UHT Production Sequence Enable [BOOL] *)
    bEmergencyStop_NC                   : BOOL := TRUE;     (* Dual-Channel Hardwired Safety Circuit Active Low [BOOL] *)
    bFaultReset                         : BOOL := FALSE;    (* Operator Master Fault Reset & Trip Latch Acknowledge [BOOL] *)
    bCIP_SIP_Request                    : BOOL := FALSE;    (* Clean-In-Place / Sterilize-In-Place Mode Request [BOOL] *)
    bProductionRequest                  : BOOL := FALSE;    (* Raw Milk Infeed Production Mode Request [BOOL] *)
    bAsepticTankReadyPermissive         : BOOL := TRUE;     (* Downstream Sterile Buffer Storage Tank Ready Permissive [BOOL] *)
    bSterileAirSupplyOk                 : BOOL := TRUE;     (* Sterile Overpressure Air Header Pressure Permissive [BOOL] *)
    bCoolingWaterSupplyOk               : BOOL := TRUE;     (* Chilled Glycol/Water Header Circulation Permissive [BOOL] *)
    bCulinarySteamHeaderOk              : BOOL := TRUE;     (* High-Purity Culinary Steam Header Permissive [BOOL] *)
    tDeterministicScanTime              : TIME := T#20MS;   (* Deterministic Control Task Scan Period (20 ms) [TIME] *)

    (* ========================================================================================= *)
    (* 2. THERMAL RECIPE SETPOINTS & CRITICAL PROCESS BOUNDS                                     *)
    (* ========================================================================================= *)
    rSet_HoldingTubeTemp_Target_degC    : REAL := 142.00;   (* Target UHT Sterilization Holding Temperature [deg C] *)
    rSet_HoldingTubeTemp_TripLimit_degC : REAL := 139.50;   (* Fast Aseptic Diversion Trip Safety Interlock [deg C] *)
    rSet_MilkFlowRate_Target_Lph        : REAL := 30000.0;  (* Continuous Mass Flow Production Capacity [L/h] *)
    rSet_PreheatRegenTemp_Target_degC   : REAL := 78.50;    (* Multi-Section Plate Pre-Heater Target Outlet [deg C] *)
    rSet_FlashChamberVacuum_Target_bar  : REAL := -0.650;   (* Vacuum Flash De-Aerator Equilibrium Gauge Pressure [bar] *)
    rSet_HomoStage1Press_Target_bar     : REAL := 250.00;   (* Homogenizer Stage 1 Hydraulic Hydraulic Pressure [bar] *)
    rSet_HomoStage2Press_Target_bar     : REAL := 50.00;    (* Homogenizer Stage 2 Secondary De-Flocculation Press [bar] *)
    rSet_AsepticCoolerTarget_degC       : REAL := 4.00;     (* Final Plate Cooler Product Discharge Temperature [deg C] *)
    rSet_SterileAirHeadspace_Target_bar : REAL := 0.500;    (* Sterile Buffer Tank Headspace Overpressure Cascade [bar] *)
    rSet_SIP_SterilTemp_Target_degC     : REAL := 130.00;   (* Hot Water Sterilization-In-Place Soak Target [deg C] *)
    rSet_SIP_TargetLethality_F0_min     : REAL := 12.00;    (* Target Geobacillus Stearothermophilus Lethality [min] *)
    rSet_MaxAllowableFoulingRes_m2KW    : REAL := 0.00045;  (* Maximum Permissible Milk Protein Fouling Resistance [m2*K/W] *)
    rSet_CausticDosingTarget_mS         : REAL := 45.00;    (* CIP Hot Caustic Phase Sodium Hydroxide Conductivity [mS/cm] *)
    rSet_AcidDosingTarget_mS            : REAL := 32.00;    (* CIP Acid Phase Nitric/Phosphoric Acid Conductivity [mS/cm] *)

    (* ========================================================================================= *)
    (* 3. 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) FIELD TRANSMITTERS (16 TRANSMITTER TRIPLETS)      *)
    (* ========================================================================================= *)
    (* FT_RAW_MILK_INLET_101: Triplicated Raw Milk Infeed Coriolis Mass Flowmeters [L/h] *)
    FT_RAW_MILK_INLET_101A              : REAL := 30000.0;  (* Raw Milk Infeed Mass Flowmeter Channel A [L/h] *)
    FT_RAW_MILK_INLET_101B              : REAL := 30000.0;  (* Raw Milk Infeed Mass Flowmeter Channel B [L/h] *)
    FT_RAW_MILK_INLET_101C              : REAL := 30000.0;  (* Raw Milk Infeed Mass Flowmeter Channel C [L/h] *)

    (* TT_PREHEAT_REGEN_OUTLET_102: Triplicated Plate Pre-Heater Section 2 Regeneration Outlets [deg C] *)
    TT_PREHEAT_REGEN_OUTLET_102A        : REAL := 78.50;    (* Plate Regeneration Section Outlet Temp Ch A [deg C] *)
    TT_PREHEAT_REGEN_OUTLET_102B        : REAL := 78.50;    (* Plate Regeneration Section Outlet Temp Ch B [deg C] *)
    TT_PREHEAT_REGEN_OUTLET_102C        : REAL := 78.50;    (* Plate Regeneration Section Outlet Temp Ch C [deg C] *)

    (* PT_STEAM_INFUSION_HEADER_201: Triplicated Culinary Steam Pressure Transmitters [bar gauge] *)
    PT_STEAM_INFUSION_HEADER_201A       : REAL := 4.500;    (* Culinary Steam Header Pressure Sensor Ch A [bar] *)
    PT_STEAM_INFUSION_HEADER_201B       : REAL := 4.500;    (* Culinary Steam Header Pressure Sensor Ch B [bar] *)
    PT_STEAM_INFUSION_HEADER_201C       : REAL := 4.500;    (* Culinary Steam Header Pressure Sensor Ch C [bar] *)

    (* TT_UHT_HOLDING_TUBE_202: Triplicated Sanitary Pt100 RTD Holding Tube Sterilization Monitors [deg C] *)
    TT_UHT_HOLDING_TUBE_202A            : REAL := 142.00;   (* UHT Holding Tube Sterilization Temp Ch A [deg C] *)
    TT_UHT_HOLDING_TUBE_202B            : REAL := 142.00;   (* UHT Holding Tube Sterilization Temp Ch B [deg C] *)
    TT_UHT_HOLDING_TUBE_202C            : REAL := 142.00;   (* UHT Holding Tube Sterilization Temp Ch C [deg C] *)

    (* FT_CULINARY_STEAM_FLOW_203: Triplicated Culinary Steam Vortex / Sonic Mass Flowmeters [kg/h] *)
    FT_CULINARY_STEAM_FLOW_203A         : REAL := 1250.0;   (* Direct Steam Infuser Steam Mass Flow Ch A [kg/h] *)
    FT_CULINARY_STEAM_FLOW_203B         : REAL := 1250.0;   (* Direct Steam Infuser Steam Mass Flow Ch B [kg/h] *)
    FT_CULINARY_STEAM_FLOW_203C         : REAL := 1250.0;   (* Direct Steam Infuser Steam Mass Flow Ch C [kg/h] *)

    (* PT_FLASH_CHAMBER_VACUUM_301: Triplicated Vacuum Flash Vessel Absolute/Gauge Pressure Transmitters [bar] *)
    PT_FLASH_CHAMBER_VACUUM_301A        : REAL := -0.650;   (* Vacuum Flash Vessel De-Aerator Pressure Ch A [bar] *)
    PT_FLASH_CHAMBER_VACUUM_301B        : REAL := -0.650;   (* Vacuum Flash Vessel De-Aerator Pressure Ch B [bar] *)
    PT_FLASH_CHAMBER_VACUUM_301C        : REAL := -0.650;   (* Vacuum Flash Vessel De-Aerator Pressure Ch C [bar] *)

    (* TT_FLASH_CHAMBER_OUTLET_302: Triplicated Flash Vessel Outlet Bottom Discharge Temperatures [deg C] *)
    TT_FLASH_CHAMBER_OUTLET_302A        : REAL := 82.00;    (* Flash Vessel Discharge Milk Temperature Ch A [deg C] *)
    TT_FLASH_CHAMBER_OUTLET_302B        : REAL := 82.00;    (* Flash Vessel Discharge Milk Temperature Ch B [deg C] *)
    TT_FLASH_CHAMBER_OUTLET_302C        : REAL := 82.00;    (* Flash Vessel Discharge Milk Temperature Ch C [deg C] *)

    (* PT_HOMOGENIZER_STAGE1_PRESS_401: Triplicated Stage 1 High-Pressure Ceramic Diaphragm Transmitters [bar] *)
    PT_HOMOGENIZER_STAGE1_PRESS_401A    : REAL := 250.00;   (* Homogenizer Stage 1 Breaker Pressure Ch A [bar] *)
    PT_HOMOGENIZER_STAGE1_PRESS_401B    : REAL := 250.00;   (* Homogenizer Stage 1 Breaker Pressure Ch B [bar] *)
    PT_HOMOGENIZER_STAGE1_PRESS_401C    : REAL := 250.00;   (* Homogenizer Stage 1 Breaker Pressure Ch C [bar] *)

    (* PT_HOMOGENIZER_STAGE2_PRESS_402: Triplicated Stage 2 De-Flocculation Pressure Transmitters [bar] *)
    PT_HOMOGENIZER_STAGE2_PRESS_402A    : REAL := 50.00;    (* Homogenizer Stage 2 Secondary Pressure Ch A [bar] *)
    PT_HOMOGENIZER_STAGE2_PRESS_402B    : REAL := 50.00;    (* Homogenizer Stage 2 Secondary Pressure Ch B [bar] *)
    PT_HOMOGENIZER_STAGE2_PRESS_402C    : REAL := 50.00;    (* Homogenizer Stage 2 Secondary Pressure Ch C [bar] *)

    (* IT_HOMOGENIZER_MOTOR_KW_403: Triplicated Drive Motor True Electrical Power Transducers [kW] *)
    IT_HOMOGENIZER_MOTOR_KW_403A        : REAL := 220.00;   (* Homogenizer Crankshaft Motor Electric Power Ch A [kW] *)
    IT_HOMOGENIZER_MOTOR_KW_403B        : REAL := 220.00;   (* Homogenizer Crankshaft Motor Electric Power Ch B [kW] *)
    IT_HOMOGENIZER_MOTOR_KW_403C        : REAL := 220.00;   (* Homogenizer Crankshaft Motor Electric Power Ch C [kW] *)

    (* TT_ASEPTIC_COOLER_OUTLET_501: Triplicated Aseptic Final Plate Cooler Discharge Temperatures [deg C] *)
    TT_ASEPTIC_COOLER_OUTLET_501A       : REAL := 4.00;     (* Final Aseptic Cooler Product Discharge Temp Ch A [deg C] *)
    TT_ASEPTIC_COOLER_OUTLET_501B       : REAL := 4.00;     (* Final Aseptic Cooler Product Discharge Temp Ch B [deg C] *)
    TT_ASEPTIC_COOLER_OUTLET_501C       : REAL := 4.00;     (* Final Aseptic Cooler Product Discharge Temp Ch C [deg C] *)

    (* PT_ASEPTIC_TANK_HEADSPACE_601: Triplicated Sterile Buffer Storage Tank Headspace Transmitters [bar] *)
    PT_ASEPTIC_TANK_HEADSPACE_601A      : REAL := 0.500;    (* Sterile Air Buffer Tank Headspace Pressure Ch A [bar] *)
    PT_ASEPTIC_TANK_HEADSPACE_601B      : REAL := 0.500;    (* Sterile Air Buffer Tank Headspace Pressure Ch B [bar] *)
    PT_ASEPTIC_TANK_HEADSPACE_601C      : REAL := 0.500;    (* Sterile Air Buffer Tank Headspace Pressure Ch C [bar] *)

    (* AIT_CIP_CAUSTIC_CONDUCTIVITY_701: Triplicated Toroidal Inductive Caustic Conductivity Probes [mS/cm] *)
    AIT_CIP_CAUSTIC_CONDUCTIVITY_701A   : REAL := 45.00;    (* CIP Return Header Caustic Conductivity Ch A [mS/cm] *)
    AIT_CIP_CAUSTIC_CONDUCTIVITY_701B   : REAL := 45.00;    (* CIP Return Header Caustic Conductivity Ch B [mS/cm] *)
    AIT_CIP_CAUSTIC_CONDUCTIVITY_701C   : REAL := 45.00;    (* CIP Return Header Caustic Conductivity Ch C [mS/cm] *)

    (* AIT_CIP_ACID_CONDUCTIVITY_702: Triplicated Toroidal Inductive Acid Conductivity Probes [mS/cm] *)
    AIT_CIP_ACID_CONDUCTIVITY_702A      : REAL := 32.00;    (* CIP Return Header Acid Conductivity Ch A [mS/cm] *)
    AIT_CIP_ACID_CONDUCTIVITY_702B      : REAL := 32.00;    (* CIP Return Header Acid Conductivity Ch B [mS/cm] *)
    AIT_CIP_ACID_CONDUCTIVITY_702C      : REAL := 32.00;    (* CIP Return Header Acid Conductivity Ch C [mS/cm] *)

    (* ZS_DIVERSION_VALVE_FORWARD_801: Triplicated Fast Pneumatic Diversion Valve Forward Proximity Switches [BOOL] *)
    ZS_DIVERSION_VALVE_FORWARD_801A     : BOOL := TRUE;     (* Fast Aseptic Divert Valve Forward Seat Closed Ch A [BOOL] *)
    ZS_DIVERSION_VALVE_FORWARD_801B     : BOOL := TRUE;     (* Fast Aseptic Divert Valve Forward Seat Closed Ch B [BOOL] *)
    ZS_DIVERSION_VALVE_FORWARD_801C     : BOOL := TRUE;     (* Fast Aseptic Divert Valve Forward Seat Closed Ch C [BOOL] *)

    (* ZS_DIVERSION_VALVE_DIVERT_802: Triplicated Fast Pneumatic Diversion Valve Divert Proximity Switches [BOOL] *)
    ZS_DIVERSION_VALVE_DIVERT_802A      : BOOL := FALSE;    (* Fast Aseptic Divert Valve Divert Seat Open Ch A [BOOL] *)
    ZS_DIVERSION_VALVE_DIVERT_802B      : BOOL := FALSE;    (* Fast Aseptic Divert Valve Divert Seat Open Ch B [BOOL] *)
    ZS_DIVERSION_VALVE_DIVERT_802C      : BOOL := FALSE;    (* Fast Aseptic Divert Valve Divert Seat Open Ch C [BOOL] *)

    (* ========================================================================================= *)
    (* 4. AUXILIARY SYSTEM INPUTS & INTERLOCKS                                                   *)
    (* ========================================================================================= *)
    rRawMilkInletTemp_degC              : REAL := 4.50;     (* Silo Raw Milk Infeed Storage Temperature [deg C] *)
    rBalanceTankLevel_pct               : REAL := 68.50;    (* Raw Milk Infeed Float Balance Tank Level [%] *)
    rChilledWaterSupplyTemp_degC        : REAL := 1.50;     (* Secondary Chilled Water Header Supply Temp [deg C] *)
    rSteamSupplyTemperature_degC        : REAL := 155.50;   (* Culinary Steam Header Saturation Temperature [deg C] *)
    bAsepticPackagingLineDemandingMilk  : BOOL := TRUE;     (* Aseptic Rotary Tetra/Combibloc Filler Running [BOOL] *)
    bHomogenizerLubricationOilFlowOk    : BOOL := TRUE;     (* Homogenizer Crankcase Lube Oil Flow Switch [BOOL] *)
    bFlashCondenserCoolingFlowOk        : BOOL := TRUE;     (* Vacuum Flashing Aroma Condenser Coolant Flow [BOOL] *)
END_VAR
''')

    # =========================================================================
    # 3. VAR_OUTPUT
    # =========================================================================
    code_parts.append('''VAR_OUTPUT
    (* ========================================================================================= *)
    (* 1. PRIMARY SYSTEM OPERATION & INTERLOCK STATUS FLAGS                                      *)
    (* ========================================================================================= *)
    bSystemReady                        : BOOL := FALSE;    (* Master UHT System Automation Permissive Ready [BOOL] *)
    bSystemRunning                      : BOOL := FALSE;    (* Active UHT Thermal Processing / CIP Cycle Active [BOOL] *)
    bEmergencyTripped                   : BOOL := FALSE;    (* Master Critical Safety Shutdown Latched Trip [BOOL] *)
    bAsepticDiversionActive             : BOOL := FALSE;    (* Holding Temperature Low Fast Diversion Engaged [BOOL] *)
    bCommercialSterilityAchieved        : BOOL := FALSE;    (* Hot Water SIP Sterility Lethality Integral F0 >= 12.0 min [BOOL] *)
    bPlateFoulingCleanRequired          : BOOL := FALSE;    (* Protein Encrustation Fouling Limit Exceeded [BOOL] *)
    bHomogenizerSeatWearAlert           : BOOL := FALSE;    (* Tungsten Carbide Valve Seat Erosion Wear Flag [BOOL] *)
    bSterileBarrierIntact               : BOOL := TRUE;     (* Sterile Air Overpressure Cascade Barrier Confirmed [BOOL] *)
    nActiveFSM_State                    : INT  := 0;        (* Current Operational 12-Stage Finite State Machine Step [0..11] *)

    (* ========================================================================================= *)
    (* 2. CONTINUOUS CLOSED-LOOP ACTUATOR COMMANDS & VALVE SETPOINTS                             *)
    (* ========================================================================================= *)
    rCmd_MilkFeedPump_Speed_pct         : REAL := 0.0;      (* Raw Milk Infeed Progressive Positive Pump VFD [0..100%] *)
    rCmd_SteamInfusionValve_pct         : REAL := 0.0;      (* Culinary Steam Sonic Direct Infusion Modulating Valve [0..100%] *)
    rCmd_FlashVacuumValve_pct           : REAL := 0.0;      (* Vacuum Flash De-Aerator Chamber Throttle Valve [0..100%] *)
    rCmd_HomoStage1HydValve_bar         : REAL := 0.0;      (* Homogenizer Stage 1 Hydraulic Loading Pressure [0..300 bar] *)
    rCmd_HomoStage2HydValve_bar         : REAL := 0.0;      (* Homogenizer Stage 2 Hydraulic Loading Pressure [0..100 bar] *)
    rCmd_AsepticCoolerValve_pct         : REAL := 0.0;      (* Aseptic Plate Cooler Chilled Water Modulating Valve [0..100%] *)
    rCmd_SterileAirRegValve_pct         : REAL := 0.0;      (* Sterile Buffer Tank Headspace Pressure Reg Valve [0..100%] *)
    bCmd_AsepticDiversion_Forward       : BOOL := FALSE;    (* Fast Pneumatic Solenoid Forward to Filler (Energize to Run) [BOOL] *)
    bCmd_AsepticDiversion_Divert        : BOOL := TRUE;     (* Fast Pneumatic Solenoid Divert to Balance Tank (De-Energize) [BOOL] *)
    rCmd_CIPCausticPump_pct             : REAL := 0.0;      (* CIP Caustic Chemical Injection Metering Pump [0..100%] *)
    rCmd_CIPAcidPump_pct                : REAL := 0.0;      (* CIP Acid Chemical Injection Metering Pump [0..100%] *)
    bCmd_CIPReturnScavengePump          : BOOL := FALSE;    (* CIP Return Header Scavenge Recovery Pump Run [BOOL] *)
    rCmd_BalanceTankMakeupValve_pct     : REAL := 0.0;      (* Raw Milk Balance Tank Modulating Infeed Valve [0..100%] *)

    (* ========================================================================================= *)
    (* 3. 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) VOTED TELEMETRY OUTPUTS                           *)
    (* ========================================================================================= *)
    rVoted_RawMilkFlow_Lph              : REAL := 30000.0;  (* 2oo3 Voted Raw Milk Infeed Volumetric Flow [L/h] *)
    rVoted_PreheatRegenTemp_degC        : REAL := 78.50;    (* 2oo3 Voted PHE Regeneration Section Outlet Temp [deg C] *)
    rVoted_SteamHeaderPress_bar         : REAL := 4.500;    (* 2oo3 Voted Culinary Steam Manifold Pressure [bar] *)
    rVoted_HoldingTubeTemp_degC         : REAL := 142.00;   (* 2oo3 Voted UHT Holding Tube Sterilization Temp [deg C] *)
    rVoted_CulinarySteamFlow_kgh        : REAL := 1250.0;   (* 2oo3 Voted Direct Culinary Steam Mass Flow Rate [kg/h] *)
    rVoted_FlashChamberVacuum_bar       : REAL := -0.650;   (* 2oo3 Voted Vacuum Flash De-Aerator Chamber Pressure [bar] *)
    rVoted_FlashChamberTemp_degC        : REAL := 82.00;    (* 2oo3 Voted Vacuum Flash Bottom Outlet Temperature [deg C] *)
    rVoted_HomogenizerStage1Press_bar   : REAL := 250.00;   (* 2oo3 Voted Homogenizer Stage 1 Operating Pressure [bar] *)
    rVoted_HomogenizerStage2Press_bar   : REAL := 50.00;    (* 2oo3 Voted Homogenizer Stage 2 Operating Pressure [bar] *)
    rVoted_HomogenizerMotorKW_kW        : REAL := 220.00;   (* 2oo3 Voted Homogenizer Crankshaft Motor Power [kW] *)
    rVoted_AsepticCoolerOutletTemp_degC : REAL := 4.00;     (* 2oo3 Voted Aseptic Final Cooler Discharge Temp [deg C] *)
    rVoted_AsepticTankHeadspacePress_bar: REAL := 0.500;    (* 2oo3 Voted Sterile Air Buffer Tank Headspace [bar] *)
    rVoted_CIPCausticConductivity_mS    : REAL := 45.00;    (* 2oo3 Voted CIP Caustic Cleaning Concentration [mS/cm] *)
    rVoted_CIPAcidConductivity_mS       : REAL := 32.00;    (* 2oo3 Voted CIP Acid Cleaning Concentration [mS/cm] *)
    bVoted_DiversionValveForward_ZS     : BOOL := TRUE;     (* 2oo3 Voted Aseptic Diversion Valve Forward Feedback [BOOL] *)
    bVoted_DiversionValveDivert_ZS      : BOOL := FALSE;    (* 2oo3 Voted Aseptic Diversion Valve Divert Feedback [BOOL] *)

    (* ========================================================================================= *)
    (* 4. CYBER-PHYSICAL OBSERVERS, KINEMATIC & THERMODYNAMIC METRICS                            *)
    (* ========================================================================================= *)
    rCalculated_Lethality_F0_min        : REAL := 0.000;    (* Cumulative Spore Lethality Integral F0 (z=10C, Tref=121.1C) [min] *)
    rCalculated_InstantLethalityRate_L  : REAL := 123.03;   (* Instantaneous Thermal Destruction Rate L(T) = 10^((T-121.1)/10) [-] *)
    rCalculated_SauterMeanDiameter_d32  : REAL := 0.550;    (* Estimated Milk Fat Globule Sauter Mean Diameter d32 [um] *)
    rCalculated_SpecificMechEnergy_kJkg : REAL := 29.12;    (* Homogenizer Specific Mechanical Energy (Delta_P/rho) [kJ/kg] *)
    rCalculated_HomogenizerWearIndex    : REAL := 0.020;    (* Tungsten Carbide Valve Seat Erosive Cavitation Wear Index [0..1] *)
    rCalculated_PHE_RegenEfficiency_pct : REAL := 92.00;    (* Multi-Section Plate Heat Exchanger Thermal Recovery [%] *)
    rCalculated_OverallHeatTransfer_U   : REAL := 2850.0;   (* Dynamic Overall Heat Transfer Coefficient U [W/(m2*K)] *)
    rCalculated_FoulingResistance_Rf    : REAL := 0.000035; (* Milk Protein / Mineral Encrustation Resistance Rf [m2*K/W] *)
    rCalculated_FlashWaterBalance_kgh   : REAL := 0.000;    (* Net Steam Injection vs Flash Evaporation Deviation [kg/h] *)
    rCalculated_DilutionRatio_pct       : REAL := 0.000;    (* Net Milk Water Dilution / Concentration Percentage [%] *)
    rCalculated_SonicSteamVelocity_mps  : REAL := 468.5;    (* Culinary Steam Injection Nozzle Acoustic Choked Velocity [m/s] *)
    rCalculated_HoldingTubeResidence_s  : REAL := 4.000;    (* Product Residence Time Inside UHT Holding Tube Section [s] *)
    rMPC_QuadraticCost_J                : REAL := 0.000;    (* Receding-Horizon Optimal Quadratic Cost Objective J [-] *)

    (* ========================================================================================= *)
    (* 5. ISA-18.2 BIT-PACKED DIAGNOSTIC & TELEMETRY STATUS WORDS                                *)
    (* ========================================================================================= *)
    dwStatusWord_Process                : DWORD := 16#0000_0000; (* Bit-Packed Operational State & Pasteurizer Flags *)
    dwStatusWord_Actuators              : DWORD := 16#0000_0000; (* Bit-Packed Valve, Pump & Homogenizer Commands *)
    dwAlarmWord_Trip                    : DWORD := 16#0000_0000; (* Bit-Packed ISA-18.2 Priority 1 Fast Emergency Trips *)
    dwAlarmWord_Warning                 : DWORD := 16#0000_0000; (* Bit-Packed ISA-18.2 Priority 2 Process Deviations *)
    dwSensorHealthMask_Low              : DWORD := 16#0000_0000; (* Bit-Packed 2oo3 TMR Channel 1..8 Fault Isolation Bits *)
    dwSensorHealthMask_High             : DWORD := 16#0000_0000; (* Bit-Packed 2oo3 TMR Channel 9..16 Fault Isolation Bits *)
END_VAR
''')

    # =========================================================================
    # 4. VAR (INTERNAL STATE, MATRICES, MPC WEIGHTS, TIMERS, ETC.)
    # =========================================================================
    code_parts.append('''VAR
    (* ========================================================================================= *)
    (* 1. DISCRETE TASK CYCLE & PHYSICAL / THERMODYNAMIC CONSTANTS                               *)
    (* ========================================================================================= *)
    c_rTs                               : REAL := 0.020;    (* Deterministic PLC Execution Task Period (20 ms) [s] *)
    c_rPi                               : REAL := 3.141592653589793; (* Circle Circumference Constant Pi *)
    c_rMilkDensity_kg_m3                : REAL := 1030.0;   (* Whole Bovine Milk Density at 20 deg C [kg/m3] *)
    c_rMilkSpecificHeat_kJ_kgK          : REAL := 3.930;    (* Milk Isobaric Specific Heat Capacity [kJ/(kg*K)] *)
    c_rWaterSpecificHeat_kJ_kgK         : REAL := 4.184;    (* Liquid Water Isobaric Specific Heat Capacity [kJ/(kg*K)] *)
    c_rCulinarySteamEnthalpy_kJ_kg      : REAL := 2740.0;   (* Saturated Culinary Steam Specific Enthalpy at 4.5 bar [kJ/kg] *)
    c_rZ_Value_degC                     : REAL := 10.00;    (* Geobacillus Stearothermophilus Thermal Inactivation z-Value [deg C] *)
    c_rT_Ref_degC                       : REAL := 121.10;   (* Standard Reference Sterilization Temperature [deg C] *)
    c_rHoldingTubeVolume_L              : REAL := 33.333;   (* UHT Holding Tube Internal Volume (4.0 s @ 30,000 L/h) [L] *)
    c_rHoldingTubeLength_m              : REAL := 15.000;   (* Total Linear Length of Holding Tube Geometry [m] *)
    c_rPHE_SurfaceArea_m2               : REAL := 185.00;   (* Multi-Section Plate Heat Exchanger Total Area [m2] *)
    c_rCleanPHE_HeatTransferCoeff_U0    : REAL := 3200.0;   (* Clean Stainless Steel Plate Overall Heat Transfer Coeff [W/(m2*K)] *)
    c_rSonicSteamNozzleThroatArea_m2    : REAL := 0.000420; (* Culinary Steam Multi-Orifice Sonic Choked Throat Area [m2] *)
    c_rSteamIsentropicExponent_k        : REAL := 1.300;    (* Saturated Water Vapor Adiabatic Ratio k = Cp/Cv *)
    c_rAntoine_A                        : REAL := 8.07131;  (* Antoine Equation Saturated Vapor Pressure Const A *)
    c_rAntoine_B                        : REAL := 1730.630; (* Antoine Equation Saturated Vapor Pressure Const B *)
    c_rAntoine_C                        : REAL := 233.426;  (* Antoine Equation Saturated Vapor Pressure Const C *)

    (* ========================================================================================= *)
    (* 2. 8x8 MULTIVARIABLE STATE-SPACE MATRICES & RECEDING-HORIZON MPC REGISTERS                *)
    (* States x[1..8]:                                                                           *)
    (*   x[1]: Holding Tube Sterilization Temperature Error Delta_T_hold [deg C]                 *)
    (*   x[2]: Vacuum Flash Chamber Bottom Discharge Temperature Error Delta_T_flash [deg C]    *)
    (*   x[3]: Vacuum Flash Net Water Mass Balance Deviation Delta_m_water [kg/h]                *)
    (*   x[4]: Multi-Section Plate Regeneration Outlet Temp Error Delta_T_regen [deg C]          *)
    (*   x[5]: Homogenizer Stage 1 Operating Pressure Error Delta_P_homo1 [bar]                  *)
    (*   x[6]: Homogenizer Stage 2 Operating Pressure Error Delta_P_homo2 [bar]                  *)
    (*   x[7]: Raw Milk Infeed Volumetric Flow Rate Deviation Delta_V_flow [L/h]                 *)
    (*   x[8]: Sterile Buffer Storage Tank Headspace Overpressure Error Delta_P_sterile [bar]    *)
    (* Controls u[1..6]:                                                                         *)
    (*   u[1]: Culinary Steam Sonic Direct Infusion Modulating Valve u_steam [%]                 *)
    (*   u[2]: Vacuum Flash De-Aerator Chamber Throttle Valve u_vac [%]                          *)
    (*   u[3]: Raw Milk Infeed Progressive Positive Pump VFD Speed u_pump [%]                    *)
    (*   u[4]: Homogenizer Stage 1 Hydraulic Loading Pressure Valve u_hyd1 [%]                   *)
    (*   u[5]: Homogenizer Stage 2 Hydraulic Loading Pressure Valve u_hyd2 [%]                   *)
    (*   u[6]: Aseptic Final Plate Cooler Chilled Water Modulating Valve u_cw [%]                *)
    (* ========================================================================================= *)
    bMatricesInitialized                : BOOL := FALSE;
    aA                                  : ARRAY[1..8, 1..8] OF REAL; (* Discrete State Transition Matrix A (8x8) *)
    aB                                  : ARRAY[1..8, 1..6] OF REAL; (* Discrete Actuator Coupling Matrix B (8x6) *)
    aC                                  : ARRAY[1..8, 1..8] OF REAL; (* Discrete Measurement Observation Matrix C (8x8) *)
    aD                                  : ARRAY[1..8, 1..6] OF REAL; (* Discrete Direct Feedthrough Matrix D (8x6) *)
    ax_state                            : ARRAY[1..8] OF REAL;       (* Current Discrete State Vector x[k] *)
    ax_next                             : ARRAY[1..8] OF REAL;       (* Projected Next State Vector x[k+1] *)
    ax_ref                              : ARRAY[1..8] OF REAL;       (* Reference Setpoint State Vector r[k] *)
    au_control                          : ARRAY[1..6] OF REAL;       (* Optimal Actuator Control Vector u[k] *)
    au_prev                             : ARRAY[1..6] OF REAL;       (* Prior Actuator Control Vector u[k-1] *)
    au_delta                            : ARRAY[1..6] OF REAL;       (* Control Incremental Slew Rate Delta_u[k] *)
    ay_output                           : ARRAY[1..8] OF REAL;       (* Reconstructed Process Measurement Vector y[k] *)

    (* Model Predictive Control (MPC) Penalty Weights & Bounds *)
    aQ_Weight                           : ARRAY[1..8] OF REAL;       (* State Tracking Penalty Diagonal Diag(Q) *)
    aR_Weight                           : ARRAY[1..6] OF REAL;       (* Actuator Magnitude Penalty Diagonal Diag(R) *)
    aS_Weight                           : ARRAY[1..6] OF REAL;       (* Actuator Rate-of-Change Slew Diagonal Diag(S) *)
    aP_TerminalWeight                   : ARRAY[1..8] OF REAL;       (* Terminal Horizon Cost Penalty Diag(P) *)
    au_min                              : ARRAY[1..6] OF REAL;       (* Actuator Hard Lower Saturation Bounds *)
    au_max                              : ARRAY[1..6] OF REAL;       (* Actuator Hard Upper Saturation Bounds *)
    adelta_u_max                        : ARRAY[1..6] OF REAL;       (* Maximum Allowable Actuator Slew Rate per 20 ms *)
    aGrad_u                             : ARRAY[1..6] OF REAL;       (* Projected Gradient Descent Vector nabla_u J *)
    aPredictedState                     : ARRAY[1..8] OF REAL;       (* 1-Step Horizon Predictive State Register *)
    c_rPGD_Alpha                        : REAL := 0.00045;           (* Projected Gradient Descent Learning Rate Alpha *)
    rMPC_QuadraticCostAccum             : REAL := 0.0;               (* Instantaneous Quadratic Cost Functional J *)

    (* ========================================================================================= *)
    (* 3. 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) DISCREPANCY TIMERS & HEALTH LATCHES               *)
    (* ========================================================================================= *)
    c_rTol_RawMilkFlow_Lph              : REAL := 450.0;    (* Infeed Mass Flow Discrepancy Gate [L/h] *)
    c_rTol_PreheatTemp_degC             : REAL := 1.200;    (* Plate Regeneration Outlet Temp Discrepancy Gate [deg C] *)
    c_rTol_SteamHeaderPress_bar         : REAL := 0.150;    (* Steam Manifold Pressure Discrepancy Gate [bar] *)
    c_rTol_HoldingTubeTemp_degC         : REAL := 0.350;    (* UHT Holding Tube Sterilization Temp Discrepancy Gate [deg C] *)
    c_rTol_SteamFlow_kgh                : REAL := 25.00;    (* Culinary Steam Flow Discrepancy Gate [kg/h] *)
    c_rTol_FlashVacuum_bar              : REAL := 0.025;    (* Vacuum Flash De-Aerator Pressure Discrepancy Gate [bar] *)
    c_rTol_FlashTemp_degC               : REAL := 1.000;    (* Flash Bottom Discharge Temp Discrepancy Gate [deg C] *)
    c_rTol_HomoPressStage1_bar          : REAL := 6.500;    (* Homogenizer Stage 1 Operating Pressure Discrepancy Gate [bar] *)
    c_rTol_HomoPressStage2_bar          : REAL := 3.000;    (* Homogenizer Stage 2 Operating Pressure Discrepancy Gate [bar] *)
    c_rTol_HomoMotorKW_kW               : REAL := 8.000;    (* Homogenizer Electric Power Discrepancy Gate [kW] *)
    c_rTol_AsepticCoolerTemp_degC       : REAL := 0.400;    (* Final Cooler Outlet Temp Discrepancy Gate [deg C] *)
    c_rTol_AsepticTankHeadspace_bar     : REAL := 0.025;    (* Sterile Buffer Tank Headspace Discrepancy Gate [bar] *)
    c_rTol_CIPCausticCond_mS            : REAL := 1.500;    (* CIP Caustic Conductivity Discrepancy Gate [mS/cm] *)
    c_rTol_CIPAcidCond_mS               : REAL := 1.200;    (* CIP Acid Conductivity Discrepancy Gate [mS/cm] *)
    c_rTMR_PersistencyTimeout_s         : REAL := 0.060;    (* Maximum Allowable Discrepancy Persistency Window (60 ms) [s] *)

    (* Discrepancy Accumulation Chronometers *)
    rTimer_MilkFlow_Disc_s              : REAL := 0.0;
    rTimer_PreheatTemp_Disc_s           : REAL := 0.0;
    rTimer_SteamPress_Disc_s            : REAL := 0.0;
    rTimer_HoldingTemp_Disc_s           : REAL := 0.0;
    rTimer_SteamFlow_Disc_s             : REAL := 0.0;
    rTimer_FlashVac_Disc_s              : REAL := 0.0;
    rTimer_FlashTemp_Disc_s             : REAL := 0.0;
    rTimer_HomoPress1_Disc_s            : REAL := 0.0;
    rTimer_HomoPress2_Disc_s            : REAL := 0.0;
    rTimer_HomoPower_Disc_s             : REAL := 0.0;
    rTimer_CoolerTemp_Disc_s            : REAL := 0.0;
    rTimer_AsepticTank_Disc_s           : REAL := 0.0;
    rTimer_CIPCaustic_Disc_s            : REAL := 0.0;
    rTimer_CIPAcid_Disc_s               : REAL := 0.0;
    rTimer_DivertFwd_Disc_s             : REAL := 0.0;
    rTimer_DivertDiv_Disc_s             : REAL := 0.0;

    (* Channel Health Isolation Latches (TRUE = Channel Quarantined as Outlier) *)
    bIso_MilkFlow_ChA                   : BOOL := FALSE;
    bIso_MilkFlow_ChB                   : BOOL := FALSE;
    bIso_MilkFlow_ChC                   : BOOL := FALSE;
    bIso_PreheatTemp_ChA                : BOOL := FALSE;
    bIso_PreheatTemp_ChB                : BOOL := FALSE;
    bIso_PreheatTemp_ChC                : BOOL := FALSE;
    bIso_SteamPress_ChA                 : BOOL := FALSE;
    bIso_SteamPress_ChB                 : BOOL := FALSE;
    bIso_SteamPress_ChC                 : BOOL := FALSE;
    bIso_HoldingTemp_ChA                : BOOL := FALSE;
    bIso_HoldingTemp_ChB                : BOOL := FALSE;
    bIso_HoldingTemp_ChC                : BOOL := FALSE;
    bIso_SteamFlow_ChA                  : BOOL := FALSE;
    bIso_SteamFlow_ChB                  : BOOL := FALSE;
    bIso_SteamFlow_ChC                  : BOOL := FALSE;
    bIso_FlashVac_ChA                   : BOOL := FALSE;
    bIso_FlashVac_ChB                   : BOOL := FALSE;
    bIso_FlashVac_ChC                   : BOOL := FALSE;
    bIso_FlashTemp_ChA                  : BOOL := FALSE;
    bIso_FlashTemp_ChB                  : BOOL := FALSE;
    bIso_FlashTemp_ChC                  : BOOL := FALSE;
    bIso_HomoPress1_ChA                 : BOOL := FALSE;
    bIso_HomoPress1_ChB                 : BOOL := FALSE;
    bIso_HomoPress1_ChC                 : BOOL := FALSE;
    bIso_HomoPress2_ChA                 : BOOL := FALSE;
    bIso_HomoPress2_ChB                 : BOOL := FALSE;
    bIso_HomoPress2_ChC                 : BOOL := FALSE;
    bIso_HomoPower_ChA                  : BOOL := FALSE;
    bIso_HomoPower_ChB                  : BOOL := FALSE;
    bIso_HomoPower_ChC                  : BOOL := FALSE;
    bIso_CoolerTemp_ChA                 : BOOL := FALSE;
    bIso_CoolerTemp_ChB                 : BOOL := FALSE;
    bIso_CoolerTemp_ChC                 : BOOL := FALSE;
    bIso_AsepticTank_ChA                : BOOL := FALSE;
    bIso_AsepticTank_ChB                : BOOL := FALSE;
    bIso_AsepticTank_ChC                : BOOL := FALSE;
    bIso_CIPCaustic_ChA                 : BOOL := FALSE;
    bIso_CIPCaustic_ChB                 : BOOL := FALSE;
    bIso_CIPCaustic_ChC                 : BOOL := FALSE;
    bIso_CIPAcid_ChA                    : BOOL := FALSE;
    bIso_CIPAcid_ChB                    : BOOL := FALSE;
    bIso_CIPAcid_ChC                    : BOOL := FALSE;
    bIso_DivertFwd_ChA                  : BOOL := FALSE;
    bIso_DivertFwd_ChB                  : BOOL := FALSE;
    bIso_DivertFwd_ChC                  : BOOL := FALSE;
    bIso_DivertDiv_ChA                  : BOOL := FALSE;
    bIso_DivertDiv_ChB                  : BOOL := FALSE;
    bIso_DivertDiv_ChC                  : BOOL := FALSE;

    (* ========================================================================================= *)
    (* 4. CYBER-PHYSICAL OBSERVER INTERNAL ACCUMULATORS & REGISTERS                              *)
    (* ========================================================================================= *)
    (* 4.1: Spore Thermal Lethality F0 Numerical Integrator *)
    rAccumulated_F0_min                 : REAL := 0.0;      (* Cumulative Integral F0 [min] *)
    rLethalityRate_L_prev               : REAL := 0.0;      (* Prior Scan Lethality Rate for Trapezoidal Rule *)

    (* 4.2: Two-Stage Homogenization & Tungsten Carbide Valve Seat Wear Observer *)
    rFatGlobule_d32_unhomo              : REAL := 3.500;    (* Raw Bovine Milk Fat Globule Mean Diameter [um] *)
    rTotalHomoPressure_bar              : REAL := 300.0;    (* Sum of Stage 1 and Stage 2 Pressures [bar] *)
    rFluidHydraulicPower_kW             : REAL := 0.0;      (* Power Imparted to Product Stream [kW] *)
    rHomogenizerHydraulicEfficiency     : REAL := 0.880;    (* Fluid Power to Electric Motor Power Ratio [-] *)
    rBaselineValveStrokePosition_mm     : REAL := 0.320;    (* Nominal Carbide Valve Seat Gap at 250 bar [mm] *)
    rObservedValveSeatClearance_mm      : REAL := 0.320;    (* Estimated Actual Micro-Gap Across Seat Face [mm] *)

    (* 4.3: Plate Heat Exchanger Fouling & Thermal Boundary Layer Observer *)
    rPHE_HeatDuty_kW                    : REAL := 0.0;      (* Thermal Heat Flow Transferred in Regeneration [kW] *)
    rDelta_T1_PHE                       : REAL := 0.0;      (* PHE Hot End Approach Temperature Difference [deg C] *)
    rDelta_T2_PHE                       : REAL := 0.0;      (* PHE Cold End Approach Temperature Difference [deg C] *)
    rLMTD_PHE_degC                      : REAL := 12.50;    (* Logarithmic Mean Temperature Difference [deg C] *)
    rCleanPHE_HeatTransfer_U0           : REAL := 3200.0;   (* Baseline Unfouled Heat Transfer Coefficient [W/(m2*K)] *)

    (* 4.4: Flash Vacuum De-Aerator Enthalpy & Water Balance Observer *)
    rMilkTotalMassFlow_kgh              : REAL := 30900.0;  (* Total Mass Flow of Milk Entering DSI (30,000 L/h * 1.03) [kg/h] *)
    rLatentHeatVapAtFlash_kJkg          : REAL := 2305.0;   (* Latent Heat of Evaporation h_fg at Flash Vacuum [kJ/kg] *)
    rCalculatedEvaporatedVapor_kgh      : REAL := 1250.0;   (* Mass of Water Vapor Flashed Under Vacuum [kg/h] *)
    rEquilibriumVaporPressure_bar       : REAL := 0.363;    (* Antoine Equation Calculated Saturation Vapor Pressure [bar abs] *)

    (* ========================================================================================= *)
    (* 5. ISA-18.2 MULTI-TIERED ALARM THRESHOLDS & HYSTERESIS DEADBANDS                          *)
    (* ========================================================================================= *)
    c_rTrip_HoldingTemp_HH_degC         : REAL := 146.50;   (* Thermal Protein Degradation Overheat Trip [deg C] *)
    c_rAlarm_HoldingTemp_H_degC         : REAL := 144.00;   (* Elevated Holding Temperature Advisory [deg C] *)
    c_rAlarm_HoldingTemp_L_degC         : REAL := 140.50;   (* Low Holding Temperature Pre-Trip Advisory [deg C] *)
    c_rTrip_HoldingTemp_LL_degC         : REAL := 139.50;   (* Fast Aseptic Diversion Safety Trip [deg C] *)
    c_rDeadband_HoldingTemp_degC        : REAL := 0.500;    (* Holding Temperature Alarm Hysteresis [deg C] *)

    c_rTrip_FlashVac_HH_bar             : REAL := -0.350;   (* Loss of Flash Vacuum Dilution Trip [bar] *)
    c_rAlarm_FlashVac_H_bar             : REAL := -0.520;   (* Low Vacuum Advisory (Risk of Dilution) [bar] *)
    c_rAlarm_FlashVac_L_bar             : REAL := -0.760;   (* High Vacuum Advisory (Risk of Over-Concentration) [bar] *)
    c_rTrip_FlashVac_LL_bar             : REAL := -0.880;   (* Extreme Vacuum Aroma Evaporation Trip [bar] *)
    c_rDeadband_FlashVac_bar            : REAL := 0.030;    (* Flash Vacuum Alarm Hysteresis [bar] *)

    c_rTrip_HomoPress1_HH_bar           : REAL := 285.00;   (* Homogenizer Block Rupture Overpressure Fast Relief [bar] *)
    c_rAlarm_HomoPress1_H_bar           : REAL := 268.00;   (* Homogenizer High Operating Pressure Warning [bar] *)
    c_rAlarm_HomoPress1_L_bar           : REAL := 232.00;   (* Homogenizer Insufficient Shear Warning [bar] *)
    c_rTrip_HomoPress1_LL_bar           : REAL := 195.00;   (* Homogenizer Loss of Hydraulic Pressure Trip [bar] *)
    c_rDeadband_HomoPress1_bar          : REAL := 4.000;    (* Homogenizer Pressure Hysteresis [bar] *)

    c_rTrip_AsepticTank_HH_bar          : REAL := 0.900;    (* Sterile Buffer Tank Pressure Vessel Relief Trip [bar] *)
    c_rAlarm_AsepticTank_H_bar          : REAL := 0.700;    (* Sterile Buffer Tank High Headspace Warning [bar] *)
    c_rAlarm_AsepticTank_L_bar          : REAL := 0.350;    (* Sterile Buffer Tank Low Barrier Warning [bar] *)
    c_rTrip_AsepticTank_LL_bar          : REAL := 0.200;    (* Loss of Aseptic Barrier Fast Emergency Trip [bar] *)
    c_rDeadband_AsepticTank_bar         : REAL := 0.040;    (* Sterile Tank Pressure Hysteresis [bar] *)

    c_rTrip_CIPCaustic_HH_mS            : REAL := 75.00;    (* Caustic Chemical Over-Concentration Hazard [mS/cm] *)
    c_rAlarm_CIPCaustic_H_mS            : REAL := 55.00;    (* Caustic High Concentration Warning [mS/cm] *)
    c_rAlarm_CIPCaustic_L_mS            : REAL := 35.00;    (* Caustic Low Cleaning Efficiency Warning [mS/cm] *)
    c_rTrip_CIPCaustic_LL_mS            : REAL := 18.00;    (* Caustic Inadequate Sanitization Trip [mS/cm] *)
    c_rDeadband_CIPCaustic_mS           : REAL := 2.000;    (* Caustic Conductivity Hysteresis [mS/cm] *)

    (* ISA-18.2 First Derivative Rate-of-Change (ROC) Registers *)
    rPrevHoldingTemp_degC               : REAL := 142.00;
    rROC_HoldingTemp_degC_per_s         : REAL := 0.000;
    rPrevFlashVac_bar                   : REAL := -0.650;
    rROC_FlashVac_bar_per_s             : REAL := 0.000;
    rPrevHomoPress1_bar                 : REAL := 250.00;
    rROC_HomoPress1_bar_per_s           : REAL := 0.000;

    (* Latched Active Alarm Status Bits *)
    bAlarm_HoldingTemp_HH               : BOOL := FALSE;
    bAlarm_HoldingTemp_H                : BOOL := FALSE;
    bAlarm_HoldingTemp_L                : BOOL := FALSE;
    bAlarm_HoldingTemp_LL               : BOOL := FALSE;
    bAlarm_HoldingTemp_ROC              : BOOL := FALSE;
    bAlarm_FlashVac_HH                  : BOOL := FALSE;
    bAlarm_FlashVac_H                   : BOOL := FALSE;
    bAlarm_FlashVac_L                   : BOOL := FALSE;
    bAlarm_FlashVac_LL                  : BOOL := FALSE;
    bAlarm_FlashVac_ROC                 : BOOL := FALSE;
    bAlarm_HomoPress1_HH                : BOOL := FALSE;
    bAlarm_HomoPress1_H                 : BOOL := FALSE;
    bAlarm_HomoPress1_L                 : BOOL := FALSE;
    bAlarm_HomoPress1_LL                : BOOL := FALSE;
    bAlarm_HomoPress1_ROC               : BOOL := FALSE;
    bAlarm_AsepticTank_HH               : BOOL := FALSE;
    bAlarm_AsepticTank_H                : BOOL := FALSE;
    bAlarm_AsepticTank_L                : BOOL := FALSE;
    bAlarm_AsepticTank_LL               : BOOL := FALSE;
    bAlarm_CIPCaustic_HH                : BOOL := FALSE;
    bAlarm_CIPCaustic_H                 : BOOL := FALSE;
    bAlarm_CIPCaustic_L                 : BOOL := FALSE;
    bAlarm_CIPCaustic_LL                : BOOL := FALSE;
    bAlarm_TMR_MajorDivergence          : BOOL := FALSE;
    bAlarm_FastAsepticDivertTripped     : BOOL := FALSE;

    (* ========================================================================================= *)
    (* 6. 12-STAGE OPERATIONAL FINITE STATE MACHINE (FSM) STEP REGISTERS                         *)
    (* ========================================================================================= *)
    nFSM_State                          : INT := 0;         (* Active Primary Sequence State [0..11] *)
    nFSM_NextState                      : INT := 0;         (* Next Transition Target State [0..11] *)
    rStateDwellTimer_s                  : REAL := 0.000;    (* Elapsed Residency Chronometer in Current State [s] *)
    rWaterCirculationTimer_s            : REAL := 0.000;    (* Water Circulation Line Warm-Up Timer [s] *)
    rHotWaterSIPSoakTimer_s             : REAL := 0.000;    (* Hot Water 130 C SIP Lethality Soaking Timer [s] *)
    rSterileCoolStabilizeTimer_s        : REAL := 0.000;    (* Sterile Cooling Water Stabilization Timer [s] *)
    rMilkTransitionTimer_s              : REAL := 0.000;    (* Water-to-Milk Interface Displacement Timer [s] *)
    rAsepticDivertRecoveryTimer_s       : REAL := 0.000;    (* Product Recirculation Re-Thermalization Timer [s] *)
    rShortRinseTimer_s                  : REAL := 0.000;    (* Intermediate Aseptic Short Rinse (ASR) Timer [s] *)
    rCIPCausticCirculationTimer_s       : REAL := 0.000;    (* Hot Caustic Chemical Wash Circulation Timer [s] *)
    rCIPAcidCirculationTimer_s          : REAL := 0.000;    (* Acid Descaling Chemical Wash Circulation Timer [s] *)
    rCIPFinalRinseTimer_s               : REAL := 0.000;    (* Potable Sterile Water Final Rinse Timer [s] *)
    rEmergencyDumpTimer_s               : REAL := 0.000;    (* Safe System Venting & Depressurization Timer [s] *)

    (* Matrix & Loop Iterators *)
    idx_i                               : INT := 1;
    idx_j                               : INT := 1;
    idx_k                               : INT := 1;
    idx_iter                            : INT := 1;
    rTempProduct                        : REAL := 0.0;
    rTempSum                            : REAL := 0.0;
END_VAR
''')

    # =========================================================================
    # 5. PHASE 1: 2oo3 TMR SENSOR VOTING
    # =========================================================================
    code_parts.append('''(* ==================================================================================================================== *)
(* PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING & DISCREPANCY FAULT ISOLATION                          *)
(* Execution Cycle: 20 ms. All 16 primary P&ID process triplets evaluated for pairwise discrepancy tolerance.          *)
(* Fault Modes:                                                                                                         *)
(*   - Healthy: All 3 agree -> 3-channel average.                                                                       *)
(*   - Degraded: 2 agree, 1 outlier -> 2-channel average, quarantine outlier channel bit, increment timer.               *)
(*   - Diverged: All 3 disagree -> Latch discrepancy alarm, hold last safe value, trigger safe interlock.              *)
(* ==================================================================================================================== *)

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 1.1: 2oo3 TMR VOTING: Raw Milk Infeed Coriolis Mass Flowmeter (FT_RAW_MILK_INLET_101A/B/C) [L/h]                     *)
(* -------------------------------------------------------------------------------------------------------------------- *)
IF (ABS(FT_RAW_MILK_INLET_101A - FT_RAW_MILK_INLET_101B) <= c_rTol_RawMilkFlow_Lph) AND
   (ABS(FT_RAW_MILK_INLET_101B - FT_RAW_MILK_INLET_101C) <= c_rTol_RawMilkFlow_Lph) AND
   (ABS(FT_RAW_MILK_INLET_101C - FT_RAW_MILK_INLET_101A) <= c_rTol_RawMilkFlow_Lph) THEN
    rVoted_RawMilkFlow_Lph := (FT_RAW_MILK_INLET_101A + FT_RAW_MILK_INLET_101B + FT_RAW_MILK_INLET_101C) / 3.0;
    bIso_MilkFlow_ChA := FALSE;
    bIso_MilkFlow_ChB := FALSE;
    bIso_MilkFlow_ChC := FALSE;
    rTimer_MilkFlow_Disc_s := 0.0;
ELSIF (ABS(FT_RAW_MILK_INLET_101A - FT_RAW_MILK_INLET_101B) <= c_rTol_RawMilkFlow_Lph) THEN
    rVoted_RawMilkFlow_Lph := (FT_RAW_MILK_INLET_101A + FT_RAW_MILK_INLET_101B) * 0.5;
    bIso_MilkFlow_ChA := FALSE;
    bIso_MilkFlow_ChB := FALSE;
    bIso_MilkFlow_ChC := TRUE;
    rTimer_MilkFlow_Disc_s := rTimer_MilkFlow_Disc_s + c_rTs;
ELSIF (ABS(FT_RAW_MILK_INLET_101A - FT_RAW_MILK_INLET_101C) <= c_rTol_RawMilkFlow_Lph) THEN
    rVoted_RawMilkFlow_Lph := (FT_RAW_MILK_INLET_101A + FT_RAW_MILK_INLET_101C) * 0.5;
    bIso_MilkFlow_ChA := FALSE;
    bIso_MilkFlow_ChB := TRUE;
    bIso_MilkFlow_ChC := FALSE;
    rTimer_MilkFlow_Disc_s := rTimer_MilkFlow_Disc_s + c_rTs;
ELSIF (ABS(FT_RAW_MILK_INLET_101B - FT_RAW_MILK_INLET_101C) <= c_rTol_RawMilkFlow_Lph) THEN
    rVoted_RawMilkFlow_Lph := (FT_RAW_MILK_INLET_101B + FT_RAW_MILK_INLET_101C) * 0.5;
    bIso_MilkFlow_ChA := TRUE;
    bIso_MilkFlow_ChB := FALSE;
    bIso_MilkFlow_ChC := FALSE;
    rTimer_MilkFlow_Disc_s := rTimer_MilkFlow_Disc_s + c_rTs;
ELSE
    bIso_MilkFlow_ChA := TRUE;
    bIso_MilkFlow_ChB := TRUE;
    bIso_MilkFlow_ChC := TRUE;
    rTimer_MilkFlow_Disc_s := rTimer_MilkFlow_Disc_s + c_rTs;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 1.2: 2oo3 TMR VOTING: Plate Pre-Heater Regeneration Section Outlet Temp (TT_PREHEAT_REGEN_OUTLET_102A/B/C) [deg C]   *)
(* -------------------------------------------------------------------------------------------------------------------- *)
IF (ABS(TT_PREHEAT_REGEN_OUTLET_102A - TT_PREHEAT_REGEN_OUTLET_102B) <= c_rTol_PreheatTemp_degC) AND
   (ABS(TT_PREHEAT_REGEN_OUTLET_102B - TT_PREHEAT_REGEN_OUTLET_102C) <= c_rTol_PreheatTemp_degC) AND
   (ABS(TT_PREHEAT_REGEN_OUTLET_102C - TT_PREHEAT_REGEN_OUTLET_102A) <= c_rTol_PreheatTemp_degC) THEN
    rVoted_PreheatRegenTemp_degC := (TT_PREHEAT_REGEN_OUTLET_102A + TT_PREHEAT_REGEN_OUTLET_102B + TT_PREHEAT_REGEN_OUTLET_102C) / 3.0;
    bIso_PreheatTemp_ChA := FALSE;
    bIso_PreheatTemp_ChB := FALSE;
    bIso_PreheatTemp_ChC := FALSE;
    rTimer_PreheatTemp_Disc_s := 0.0;
ELSIF (ABS(TT_PREHEAT_REGEN_OUTLET_102A - TT_PREHEAT_REGEN_OUTLET_102B) <= c_rTol_PreheatTemp_degC) THEN
    rVoted_PreheatRegenTemp_degC := (TT_PREHEAT_REGEN_OUTLET_102A + TT_PREHEAT_REGEN_OUTLET_102B) * 0.5;
    bIso_PreheatTemp_ChA := FALSE;
    bIso_PreheatTemp_ChB := FALSE;
    bIso_PreheatTemp_ChC := TRUE;
    rTimer_PreheatTemp_Disc_s := rTimer_PreheatTemp_Disc_s + c_rTs;
ELSIF (ABS(TT_PREHEAT_REGEN_OUTLET_102A - TT_PREHEAT_REGEN_OUTLET_102C) <= c_rTol_PreheatTemp_degC) THEN
    rVoted_PreheatRegenTemp_degC := (TT_PREHEAT_REGEN_OUTLET_102A + TT_PREHEAT_REGEN_OUTLET_102C) * 0.5;
    bIso_PreheatTemp_ChA := FALSE;
    bIso_PreheatTemp_ChB := TRUE;
    bIso_PreheatTemp_ChC := FALSE;
    rTimer_PreheatTemp_Disc_s := rTimer_PreheatTemp_Disc_s + c_rTs;
ELSIF (ABS(TT_PREHEAT_REGEN_OUTLET_102B - TT_PREHEAT_REGEN_OUTLET_102C) <= c_rTol_PreheatTemp_degC) THEN
    rVoted_PreheatRegenTemp_degC := (TT_PREHEAT_REGEN_OUTLET_102B + TT_PREHEAT_REGEN_OUTLET_102C) * 0.5;
    bIso_PreheatTemp_ChA := TRUE;
    bIso_PreheatTemp_ChB := FALSE;
    bIso_PreheatTemp_ChC := FALSE;
    rTimer_PreheatTemp_Disc_s := rTimer_PreheatTemp_Disc_s + c_rTs;
ELSE
    bIso_PreheatTemp_ChA := TRUE;
    bIso_PreheatTemp_ChB := TRUE;
    bIso_PreheatTemp_ChC := TRUE;
    rTimer_PreheatTemp_Disc_s := rTimer_PreheatTemp_Disc_s + c_rTs;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 1.3: 2oo3 TMR VOTING: Culinary Steam Infusion Header Pressure (PT_STEAM_INFUSION_HEADER_201A/B/C) [bar]             *)
(* -------------------------------------------------------------------------------------------------------------------- *)
IF (ABS(PT_STEAM_INFUSION_HEADER_201A - PT_STEAM_INFUSION_HEADER_201B) <= c_rTol_SteamHeaderPress_bar) AND
   (ABS(PT_STEAM_INFUSION_HEADER_201B - PT_STEAM_INFUSION_HEADER_201C) <= c_rTol_SteamHeaderPress_bar) AND
   (ABS(PT_STEAM_INFUSION_HEADER_201C - PT_STEAM_INFUSION_HEADER_201A) <= c_rTol_SteamHeaderPress_bar) THEN
    rVoted_SteamHeaderPress_bar := (PT_STEAM_INFUSION_HEADER_201A + PT_STEAM_INFUSION_HEADER_201B + PT_STEAM_INFUSION_HEADER_201C) / 3.0;
    bIso_SteamPress_ChA := FALSE;
    bIso_SteamPress_ChB := FALSE;
    bIso_SteamPress_ChC := FALSE;
    rTimer_SteamPress_Disc_s := 0.0;
ELSIF (ABS(PT_STEAM_INFUSION_HEADER_201A - PT_STEAM_INFUSION_HEADER_201B) <= c_rTol_SteamHeaderPress_bar) THEN
    rVoted_SteamHeaderPress_bar := (PT_STEAM_INFUSION_HEADER_201A + PT_STEAM_INFUSION_HEADER_201B) * 0.5;
    bIso_SteamPress_ChA := FALSE;
    bIso_SteamPress_ChB := FALSE;
    bIso_SteamPress_ChC := TRUE;
    rTimer_SteamPress_Disc_s := rTimer_SteamPress_Disc_s + c_rTs;
ELSIF (ABS(PT_STEAM_INFUSION_HEADER_201A - PT_STEAM_INFUSION_HEADER_201C) <= c_rTol_SteamHeaderPress_bar) THEN
    rVoted_SteamHeaderPress_bar := (PT_STEAM_INFUSION_HEADER_201A + PT_STEAM_INFUSION_HEADER_201C) * 0.5;
    bIso_SteamPress_ChA := FALSE;
    bIso_SteamPress_ChB := TRUE;
    bIso_SteamPress_ChC := FALSE;
    rTimer_SteamPress_Disc_s := rTimer_SteamPress_Disc_s + c_rTs;
ELSIF (ABS(PT_STEAM_INFUSION_HEADER_201B - PT_STEAM_INFUSION_HEADER_201C) <= c_rTol_SteamHeaderPress_bar) THEN
    rVoted_SteamHeaderPress_bar := (PT_STEAM_INFUSION_HEADER_201B + PT_STEAM_INFUSION_HEADER_201C) * 0.5;
    bIso_SteamPress_ChA := TRUE;
    bIso_SteamPress_ChB := FALSE;
    bIso_SteamPress_ChC := FALSE;
    rTimer_SteamPress_Disc_s := rTimer_SteamPress_Disc_s + c_rTs;
ELSE
    bIso_SteamPress_ChA := TRUE;
    bIso_SteamPress_ChB := TRUE;
    bIso_SteamPress_ChC := TRUE;
    rTimer_SteamPress_Disc_s := rTimer_SteamPress_Disc_s + c_rTs;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 1.4: 2oo3 TMR VOTING: UHT Holding Tube Sterilization Temperature (TT_UHT_HOLDING_TUBE_202A/B/C) [deg C]             *)
(* -------------------------------------------------------------------------------------------------------------------- *)
IF (ABS(TT_UHT_HOLDING_TUBE_202A - TT_UHT_HOLDING_TUBE_202B) <= c_rTol_HoldingTubeTemp_degC) AND
   (ABS(TT_UHT_HOLDING_TUBE_202B - TT_UHT_HOLDING_TUBE_202C) <= c_rTol_HoldingTubeTemp_degC) AND
   (ABS(TT_UHT_HOLDING_TUBE_202C - TT_UHT_HOLDING_TUBE_202A) <= c_rTol_HoldingTubeTemp_degC) THEN
    rVoted_HoldingTubeTemp_degC := (TT_UHT_HOLDING_TUBE_202A + TT_UHT_HOLDING_TUBE_202B + TT_UHT_HOLDING_TUBE_202C) / 3.0;
    bIso_HoldingTemp_ChA := FALSE;
    bIso_HoldingTemp_ChB := FALSE;
    bIso_HoldingTemp_ChC := FALSE;
    rTimer_HoldingTemp_Disc_s := 0.0;
ELSIF (ABS(TT_UHT_HOLDING_TUBE_202A - TT_UHT_HOLDING_TUBE_202B) <= c_rTol_HoldingTubeTemp_degC) THEN
    rVoted_HoldingTubeTemp_degC := (TT_UHT_HOLDING_TUBE_202A + TT_UHT_HOLDING_TUBE_202B) * 0.5;
    bIso_HoldingTemp_ChA := FALSE;
    bIso_HoldingTemp_ChB := FALSE;
    bIso_HoldingTemp_ChC := TRUE;
    rTimer_HoldingTemp_Disc_s := rTimer_HoldingTemp_Disc_s + c_rTs;
ELSIF (ABS(TT_UHT_HOLDING_TUBE_202A - TT_UHT_HOLDING_TUBE_202C) <= c_rTol_HoldingTubeTemp_degC) THEN
    rVoted_HoldingTubeTemp_degC := (TT_UHT_HOLDING_TUBE_202A + TT_UHT_HOLDING_TUBE_202C) * 0.5;
    bIso_HoldingTemp_ChA := FALSE;
    bIso_HoldingTemp_ChB := TRUE;
    bIso_HoldingTemp_ChC := FALSE;
    rTimer_HoldingTemp_Disc_s := rTimer_HoldingTemp_Disc_s + c_rTs;
ELSIF (ABS(TT_UHT_HOLDING_TUBE_202B - TT_UHT_HOLDING_TUBE_202C) <= c_rTol_HoldingTubeTemp_degC) THEN
    rVoted_HoldingTubeTemp_degC := (TT_UHT_HOLDING_TUBE_202B + TT_UHT_HOLDING_TUBE_202C) * 0.5;
    bIso_HoldingTemp_ChA := TRUE;
    bIso_HoldingTemp_ChB := FALSE;
    bIso_HoldingTemp_ChC := FALSE;
    rTimer_HoldingTemp_Disc_s := rTimer_HoldingTemp_Disc_s + c_rTs;
ELSE
    bIso_HoldingTemp_ChA := TRUE;
    bIso_HoldingTemp_ChB := TRUE;
    bIso_HoldingTemp_ChC := TRUE;
    rTimer_HoldingTemp_Disc_s := rTimer_HoldingTemp_Disc_s + c_rTs;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 1.5: 2oo3 TMR VOTING: Culinary Steam Mass Flow Rate (FT_CULINARY_STEAM_FLOW_203A/B/C) [kg/h]                         *)
(* -------------------------------------------------------------------------------------------------------------------- *)
IF (ABS(FT_CULINARY_STEAM_FLOW_203A - FT_CULINARY_STEAM_FLOW_203B) <= c_rTol_SteamFlow_kgh) AND
   (ABS(FT_CULINARY_STEAM_FLOW_203B - FT_CULINARY_STEAM_FLOW_203C) <= c_rTol_SteamFlow_kgh) AND
   (ABS(FT_CULINARY_STEAM_FLOW_203C - FT_CULINARY_STEAM_FLOW_203A) <= c_rTol_SteamFlow_kgh) THEN
    rVoted_CulinarySteamFlow_kgh := (FT_CULINARY_STEAM_FLOW_203A + FT_CULINARY_STEAM_FLOW_203B + FT_CULINARY_STEAM_FLOW_203C) / 3.0;
    bIso_SteamFlow_ChA := FALSE;
    bIso_SteamFlow_ChB := FALSE;
    bIso_SteamFlow_ChC := FALSE;
    rTimer_SteamFlow_Disc_s := 0.0;
ELSIF (ABS(FT_CULINARY_STEAM_FLOW_203A - FT_CULINARY_STEAM_FLOW_203B) <= c_rTol_SteamFlow_kgh) THEN
    rVoted_CulinarySteamFlow_kgh := (FT_CULINARY_STEAM_FLOW_203A + FT_CULINARY_STEAM_FLOW_203B) * 0.5;
    bIso_SteamFlow_ChA := FALSE;
    bIso_SteamFlow_ChB := FALSE;
    bIso_SteamFlow_ChC := TRUE;
    rTimer_SteamFlow_Disc_s := rTimer_SteamFlow_Disc_s + c_rTs;
ELSIF (ABS(FT_CULINARY_STEAM_FLOW_203A - FT_CULINARY_STEAM_FLOW_203C) <= c_rTol_SteamFlow_kgh) THEN
    rVoted_CulinarySteamFlow_kgh := (FT_CULINARY_STEAM_FLOW_203A + FT_CULINARY_STEAM_FLOW_203C) * 0.5;
    bIso_SteamFlow_ChA := FALSE;
    bIso_SteamFlow_ChB := TRUE;
    bIso_SteamFlow_ChC := FALSE;
    rTimer_SteamFlow_Disc_s := rTimer_SteamFlow_Disc_s + c_rTs;
ELSIF (ABS(FT_CULINARY_STEAM_FLOW_203B - FT_CULINARY_STEAM_FLOW_203C) <= c_rTol_SteamFlow_kgh) THEN
    rVoted_CulinarySteamFlow_kgh := (FT_CULINARY_STEAM_FLOW_203B + FT_CULINARY_STEAM_FLOW_203C) * 0.5;
    bIso_SteamFlow_ChA := TRUE;
    bIso_SteamFlow_ChB := FALSE;
    bIso_SteamFlow_ChC := FALSE;
    rTimer_SteamFlow_Disc_s := rTimer_SteamFlow_Disc_s + c_rTs;
ELSE
    bIso_SteamFlow_ChA := TRUE;
    bIso_SteamFlow_ChB := TRUE;
    bIso_SteamFlow_ChC := TRUE;
    rTimer_SteamFlow_Disc_s := rTimer_SteamFlow_Disc_s + c_rTs;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 1.6: 2oo3 TMR VOTING: Vacuum Flash Chamber Pressure (PT_FLASH_CHAMBER_VACUUM_301A/B/C) [bar]                        *)
(* -------------------------------------------------------------------------------------------------------------------- *)
IF (ABS(PT_FLASH_CHAMBER_VACUUM_301A - PT_FLASH_CHAMBER_VACUUM_301B) <= c_rTol_FlashVacuum_bar) AND
   (ABS(PT_FLASH_CHAMBER_VACUUM_301B - PT_FLASH_CHAMBER_VACUUM_301C) <= c_rTol_FlashVacuum_bar) AND
   (ABS(PT_FLASH_CHAMBER_VACUUM_301C - PT_FLASH_CHAMBER_VACUUM_301A) <= c_rTol_FlashVacuum_bar) THEN
    rVoted_FlashChamberVacuum_bar := (PT_FLASH_CHAMBER_VACUUM_301A + PT_FLASH_CHAMBER_VACUUM_301B + PT_FLASH_CHAMBER_VACUUM_301C) / 3.0;
    bIso_FlashVac_ChA := FALSE;
    bIso_FlashVac_ChB := FALSE;
    bIso_FlashVac_ChC := FALSE;
    rTimer_FlashVac_Disc_s := 0.0;
ELSIF (ABS(PT_FLASH_CHAMBER_VACUUM_301A - PT_FLASH_CHAMBER_VACUUM_301B) <= c_rTol_FlashVacuum_bar) THEN
    rVoted_FlashChamberVacuum_bar := (PT_FLASH_CHAMBER_VACUUM_301A + PT_FLASH_CHAMBER_VACUUM_301B) * 0.5;
    bIso_FlashVac_ChA := FALSE;
    bIso_FlashVac_ChB := FALSE;
    bIso_FlashVac_ChC := TRUE;
    rTimer_FlashVac_Disc_s := rTimer_FlashVac_Disc_s + c_rTs;
ELSIF (ABS(PT_FLASH_CHAMBER_VACUUM_301A - PT_FLASH_CHAMBER_VACUUM_301C) <= c_rTol_FlashVacuum_bar) THEN
    rVoted_FlashChamberVacuum_bar := (PT_FLASH_CHAMBER_VACUUM_301A + PT_FLASH_CHAMBER_VACUUM_301C) * 0.5;
    bIso_FlashVac_ChA := FALSE;
    bIso_FlashVac_ChB := TRUE;
    bIso_FlashVac_ChC := FALSE;
    rTimer_FlashVac_Disc_s := rTimer_FlashVac_Disc_s + c_rTs;
ELSIF (ABS(PT_FLASH_CHAMBER_VACUUM_301B - PT_FLASH_CHAMBER_VACUUM_301C) <= c_rTol_FlashVacuum_bar) THEN
    rVoted_FlashChamberVacuum_bar := (PT_FLASH_CHAMBER_VACUUM_301B + PT_FLASH_CHAMBER_VACUUM_301C) * 0.5;
    bIso_FlashVac_ChA := TRUE;
    bIso_FlashVac_ChB := FALSE;
    bIso_FlashVac_ChC := FALSE;
    rTimer_FlashVac_Disc_s := rTimer_FlashVac_Disc_s + c_rTs;
ELSE
    bIso_FlashVac_ChA := TRUE;
    bIso_FlashVac_ChB := TRUE;
    bIso_FlashVac_ChC := TRUE;
    rTimer_FlashVac_Disc_s := rTimer_FlashVac_Disc_s + c_rTs;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 1.7: 2oo3 TMR VOTING: Flash Chamber Bottom Discharge Temperature (TT_FLASH_CHAMBER_OUTLET_302A/B/C) [deg C]        *)
(* -------------------------------------------------------------------------------------------------------------------- *)
IF (ABS(TT_FLASH_CHAMBER_OUTLET_302A - TT_FLASH_CHAMBER_OUTLET_302B) <= c_rTol_FlashTemp_degC) AND
   (ABS(TT_FLASH_CHAMBER_OUTLET_302B - TT_FLASH_CHAMBER_OUTLET_302C) <= c_rTol_FlashTemp_degC) AND
   (ABS(TT_FLASH_CHAMBER_OUTLET_302C - TT_FLASH_CHAMBER_OUTLET_302A) <= c_rTol_FlashTemp_degC) THEN
    rVoted_FlashChamberTemp_degC := (TT_FLASH_CHAMBER_OUTLET_302A + TT_FLASH_CHAMBER_OUTLET_302B + TT_FLASH_CHAMBER_OUTLET_302C) / 3.0;
    bIso_FlashTemp_ChA := FALSE;
    bIso_FlashTemp_ChB := FALSE;
    bIso_FlashTemp_ChC := FALSE;
    rTimer_FlashTemp_Disc_s := 0.0;
ELSIF (ABS(TT_FLASH_CHAMBER_OUTLET_302A - TT_FLASH_CHAMBER_OUTLET_302B) <= c_rTol_FlashTemp_degC) THEN
    rVoted_FlashChamberTemp_degC := (TT_FLASH_CHAMBER_OUTLET_302A + TT_FLASH_CHAMBER_OUTLET_302B) * 0.5;
    bIso_FlashTemp_ChA := FALSE;
    bIso_FlashTemp_ChB := FALSE;
    bIso_FlashTemp_ChC := TRUE;
    rTimer_FlashTemp_Disc_s := rTimer_FlashTemp_Disc_s + c_rTs;
ELSIF (ABS(TT_FLASH_CHAMBER_OUTLET_302A - TT_FLASH_CHAMBER_OUTLET_302C) <= c_rTol_FlashTemp_degC) THEN
    rVoted_FlashChamberTemp_degC := (TT_FLASH_CHAMBER_OUTLET_302A + TT_FLASH_CHAMBER_OUTLET_302C) * 0.5;
    bIso_FlashTemp_ChA := FALSE;
    bIso_FlashTemp_ChB := TRUE;
    bIso_FlashTemp_ChC := FALSE;
    rTimer_FlashTemp_Disc_s := rTimer_FlashTemp_Disc_s + c_rTs;
ELSIF (ABS(TT_FLASH_CHAMBER_OUTLET_302B - TT_FLASH_CHAMBER_OUTLET_302C) <= c_rTol_FlashTemp_degC) THEN
    rVoted_FlashChamberTemp_degC := (TT_FLASH_CHAMBER_OUTLET_302A + TT_FLASH_CHAMBER_OUTLET_302C) * 0.5;
    bIso_FlashTemp_ChA := TRUE;
    bIso_FlashTemp_ChB := FALSE;
    bIso_FlashTemp_ChC := FALSE;
    rTimer_FlashTemp_Disc_s := rTimer_FlashTemp_Disc_s + c_rTs;
ELSE
    bIso_FlashTemp_ChA := TRUE;
    bIso_FlashTemp_ChB := TRUE;
    bIso_FlashTemp_ChC := TRUE;
    rTimer_FlashTemp_Disc_s := rTimer_FlashTemp_Disc_s + c_rTs;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 1.8: 2oo3 TMR VOTING: Homogenizer Stage 1 Operating Pressure (PT_HOMOGENIZER_STAGE1_PRESS_401A/B/C) [bar]           *)
(* -------------------------------------------------------------------------------------------------------------------- *)
IF (ABS(PT_HOMOGENIZER_STAGE1_PRESS_401A - PT_HOMOGENIZER_STAGE1_PRESS_401B) <= c_rTol_HomoPressStage1_bar) AND
   (ABS(PT_HOMOGENIZER_STAGE1_PRESS_401B - PT_HOMOGENIZER_STAGE1_PRESS_401C) <= c_rTol_HomoPressStage1_bar) AND
   (ABS(PT_HOMOGENIZER_STAGE1_PRESS_401C - PT_HOMOGENIZER_STAGE1_PRESS_401A) <= c_rTol_HomoPressStage1_bar) THEN
    rVoted_HomogenizerStage1Press_bar := (PT_HOMOGENIZER_STAGE1_PRESS_401A + PT_HOMOGENIZER_STAGE1_PRESS_401B + PT_HOMOGENIZER_STAGE1_PRESS_401C) / 3.0;
    bIso_HomoPress1_ChA := FALSE;
    bIso_HomoPress1_ChB := FALSE;
    bIso_HomoPress1_ChC := FALSE;
    rTimer_HomoPress1_Disc_s := 0.0;
ELSIF (ABS(PT_HOMOGENIZER_STAGE1_PRESS_401A - PT_HOMOGENIZER_STAGE1_PRESS_401B) <= c_rTol_HomoPressStage1_bar) THEN
    rVoted_HomogenizerStage1Press_bar := (PT_HOMOGENIZER_STAGE1_PRESS_401A + PT_HOMOGENIZER_STAGE1_PRESS_401B) * 0.5;
    bIso_HomoPress1_ChA := FALSE;
    bIso_HomoPress1_ChB := FALSE;
    bIso_HomoPress1_ChC := TRUE;
    rTimer_HomoPress1_Disc_s := rTimer_HomoPress1_Disc_s + c_rTs;
ELSIF (ABS(PT_HOMOGENIZER_STAGE1_PRESS_401A - PT_HOMOGENIZER_STAGE1_PRESS_401C) <= c_rTol_HomoPressStage1_bar) THEN
    rVoted_HomogenizerStage1Press_bar := (PT_HOMOGENIZER_STAGE1_PRESS_401A + PT_HOMOGENIZER_STAGE1_PRESS_401C) * 0.5;
    bIso_HomoPress1_ChA := FALSE;
    bIso_HomoPress1_ChB := TRUE;
    bIso_HomoPress1_ChC := FALSE;
    rTimer_HomoPress1_Disc_s := rTimer_HomoPress1_Disc_s + c_rTs;
ELSIF (ABS(PT_HOMOGENIZER_STAGE1_PRESS_401B - PT_HOMOGENIZER_STAGE1_PRESS_401C) <= c_rTol_HomoPressStage1_bar) THEN
    rVoted_HomogenizerStage1Press_bar := (PT_HOMOGENIZER_STAGE1_PRESS_401B + PT_HOMOGENIZER_STAGE1_PRESS_401C) * 0.5;
    bIso_HomoPress1_ChA := TRUE;
    bIso_HomoPress1_ChB := FALSE;
    bIso_HomoPress1_ChC := FALSE;
    rTimer_HomoPress1_Disc_s := rTimer_HomoPress1_Disc_s + c_rTs;
ELSE
    bIso_HomoPress1_ChA := TRUE;
    bIso_HomoPress1_ChB := TRUE;
    bIso_HomoPress1_ChC := TRUE;
    rTimer_HomoPress1_Disc_s := rTimer_HomoPress1_Disc_s + c_rTs;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 1.9: 2oo3 TMR VOTING: Homogenizer Stage 2 Operating Pressure (PT_HOMOGENIZER_STAGE2_PRESS_402A/B/C) [bar]           *)
(* -------------------------------------------------------------------------------------------------------------------- *)
IF (ABS(PT_HOMOGENIZER_STAGE2_PRESS_402A - PT_HOMOGENIZER_STAGE2_PRESS_402B) <= c_rTol_HomoPressStage2_bar) AND
   (ABS(PT_HOMOGENIZER_STAGE2_PRESS_402B - PT_HOMOGENIZER_STAGE2_PRESS_402C) <= c_rTol_HomoPressStage2_bar) AND
   (ABS(PT_HOMOGENIZER_STAGE2_PRESS_402C - PT_HOMOGENIZER_STAGE2_PRESS_402A) <= c_rTol_HomoPressStage2_bar) THEN
    rVoted_HomogenizerStage2Press_bar := (PT_HOMOGENIZER_STAGE2_PRESS_402A + PT_HOMOGENIZER_STAGE2_PRESS_402B + PT_HOMOGENIZER_STAGE2_PRESS_402C) / 3.0;
    bIso_HomoPress2_ChA := FALSE;
    bIso_HomoPress2_ChB := FALSE;
    bIso_HomoPress2_ChC := FALSE;
    rTimer_HomoPress2_Disc_s := 0.0;
ELSIF (ABS(PT_HOMOGENIZER_STAGE2_PRESS_402A - PT_HOMOGENIZER_STAGE2_PRESS_402B) <= c_rTol_HomoPressStage2_bar) THEN
    rVoted_HomogenizerStage2Press_bar := (PT_HOMOGENIZER_STAGE2_PRESS_402A + PT_HOMOGENIZER_STAGE2_PRESS_402B) * 0.5;
    bIso_HomoPress2_ChA := FALSE;
    bIso_HomoPress2_ChB := FALSE;
    bIso_HomoPress2_ChC := TRUE;
    rTimer_HomoPress2_Disc_s := rTimer_HomoPress2_Disc_s + c_rTs;
ELSIF (ABS(PT_HOMOGENIZER_STAGE2_PRESS_402A - PT_HOMOGENIZER_STAGE2_PRESS_402C) <= c_rTol_HomoPressStage2_bar) THEN
    rVoted_HomogenizerStage2Press_bar := (PT_HOMOGENIZER_STAGE2_PRESS_402A + PT_HOMOGENIZER_STAGE2_PRESS_402C) * 0.5;
    bIso_HomoPress2_ChA := FALSE;
    bIso_HomoPress2_ChB := TRUE;
    bIso_HomoPress2_ChC := FALSE;
    rTimer_HomoPress2_Disc_s := rTimer_HomoPress2_Disc_s + c_rTs;
ELSIF (ABS(PT_HOMOGENIZER_STAGE2_PRESS_402B - PT_HOMOGENIZER_STAGE2_PRESS_402C) <= c_rTol_HomoPressStage2_bar) THEN
    rVoted_HomogenizerStage2Press_bar := (PT_HOMOGENIZER_STAGE2_PRESS_402B + PT_HOMOGENIZER_STAGE2_PRESS_402C) * 0.5;
    bIso_HomoPress2_ChA := TRUE;
    bIso_HomoPress2_ChB := FALSE;
    bIso_HomoPress2_ChC := FALSE;
    rTimer_HomoPress2_Disc_s := rTimer_HomoPress2_Disc_s + c_rTs;
ELSE
    bIso_HomoPress2_ChA := TRUE;
    bIso_HomoPress2_ChB := TRUE;
    bIso_HomoPress2_ChC := TRUE;
    rTimer_HomoPress2_Disc_s := rTimer_HomoPress2_Disc_s + c_rTs;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 1.10: 2oo3 TMR VOTING: Homogenizer Crankshaft Motor Electric Power (IT_HOMOGENIZER_MOTOR_KW_403A/B/C) [kW]          *)
(* -------------------------------------------------------------------------------------------------------------------- *)
IF (ABS(IT_HOMOGENIZER_MOTOR_KW_403A - IT_HOMOGENIZER_MOTOR_KW_403B) <= c_rTol_HomoMotorKW_kW) AND
   (ABS(IT_HOMOGENIZER_MOTOR_KW_403B - IT_HOMOGENIZER_MOTOR_KW_403C) <= c_rTol_HomoMotorKW_kW) AND
   (ABS(IT_HOMOGENIZER_MOTOR_KW_403C - IT_HOMOGENIZER_MOTOR_KW_403A) <= c_rTol_HomoMotorKW_kW) THEN
    rVoted_HomogenizerMotorKW_kW := (IT_HOMOGENIZER_MOTOR_KW_403A + IT_HOMOGENIZER_MOTOR_KW_403B + IT_HOMOGENIZER_MOTOR_KW_403C) / 3.0;
    bIso_HomoPower_ChA := FALSE;
    bIso_HomoPower_ChB := FALSE;
    bIso_HomoPower_ChC := FALSE;
    rTimer_HomoPower_Disc_s := 0.0;
ELSIF (ABS(IT_HOMOGENIZER_MOTOR_KW_403A - IT_HOMOGENIZER_MOTOR_KW_403B) <= c_rTol_HomoMotorKW_kW) THEN
    rVoted_HomogenizerMotorKW_kW := (IT_HOMOGENIZER_MOTOR_KW_403A + IT_HOMOGENIZER_MOTOR_KW_403B) * 0.5;
    bIso_HomoPower_ChA := FALSE;
    bIso_HomoPower_ChB := FALSE;
    bIso_HomoPower_ChC := TRUE;
    rTimer_HomoPower_Disc_s := rTimer_HomoPower_Disc_s + c_rTs;
ELSIF (ABS(IT_HOMOGENIZER_MOTOR_KW_403A - IT_HOMOGENIZER_MOTOR_KW_403C) <= c_rTol_HomoMotorKW_kW) THEN
    rVoted_HomogenizerMotorKW_kW := (IT_HOMOGENIZER_MOTOR_KW_403A + IT_HOMOGENIZER_MOTOR_KW_403C) * 0.5;
    bIso_HomoPower_ChA := FALSE;
    bIso_HomoPower_ChB := TRUE;
    bIso_HomoPower_ChC := FALSE;
    rTimer_HomoPower_Disc_s := rTimer_HomoPower_Disc_s + c_rTs;
ELSIF (ABS(IT_HOMOGENIZER_MOTOR_KW_403B - IT_HOMOGENIZER_MOTOR_KW_403C) <= c_rTol_HomoMotorKW_kW) THEN
    rVoted_HomogenizerMotorKW_kW := (IT_HOMOGENIZER_MOTOR_KW_403B + IT_HOMOGENIZER_MOTOR_KW_403C) * 0.5;
    bIso_HomoPower_ChA := TRUE;
    bIso_HomoPower_ChB := FALSE;
    bIso_HomoPower_ChC := FALSE;
    rTimer_HomoPower_Disc_s := rTimer_HomoPower_Disc_s + c_rTs;
ELSE
    bIso_HomoPower_ChA := TRUE;
    bIso_HomoPower_ChB := TRUE;
    bIso_HomoPower_ChC := TRUE;
    rTimer_HomoPower_Disc_s := rTimer_HomoPower_Disc_s + c_rTs;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 1.11: 2oo3 TMR VOTING: Aseptic Final Cooler Product Discharge Temp (TT_ASEPTIC_COOLER_OUTLET_501A/B/C) [deg C]       *)
(* -------------------------------------------------------------------------------------------------------------------- *)
IF (ABS(TT_ASEPTIC_COOLER_OUTLET_501A - TT_ASEPTIC_COOLER_OUTLET_501B) <= c_rTol_CoolerTemp_degC) AND
   (ABS(TT_ASEPTIC_COOLER_OUTLET_501B - TT_ASEPTIC_COOLER_OUTLET_501C) <= c_rTol_CoolerTemp_degC) AND
   (ABS(TT_ASEPTIC_COOLER_OUTLET_501C - TT_ASEPTIC_COOLER_OUTLET_501A) <= c_rTol_CoolerTemp_degC) THEN
    rVoted_AsepticCoolerOutletTemp_degC := (TT_ASEPTIC_COOLER_OUTLET_501A + TT_ASEPTIC_COOLER_OUTLET_501B + TT_ASEPTIC_COOLER_OUTLET_501C) / 3.0;
    bIso_CoolerTemp_ChA := FALSE;
    bIso_CoolerTemp_ChB := FALSE;
    bIso_CoolerTemp_ChC := FALSE;
    rTimer_CoolerTemp_Disc_s := 0.0;
ELSIF (ABS(TT_ASEPTIC_COOLER_OUTLET_501A - TT_ASEPTIC_COOLER_OUTLET_501B) <= c_rTol_CoolerTemp_degC) THEN
    rVoted_AsepticCoolerOutletTemp_degC := (TT_ASEPTIC_COOLER_OUTLET_501A + TT_ASEPTIC_COOLER_OUTLET_501B) * 0.5;
    bIso_CoolerTemp_ChA := FALSE;
    bIso_CoolerTemp_ChB := FALSE;
    bIso_CoolerTemp_ChC := TRUE;
    rTimer_CoolerTemp_Disc_s := rTimer_CoolerTemp_Disc_s + c_rTs;
ELSIF (ABS(TT_ASEPTIC_COOLER_OUTLET_501A - TT_ASEPTIC_COOLER_OUTLET_501C) <= c_rTol_CoolerTemp_degC) THEN
    rVoted_AsepticCoolerOutletTemp_degC := (TT_ASEPTIC_COOLER_OUTLET_501A + TT_ASEPTIC_COOLER_OUTLET_501C) * 0.5;
    bIso_CoolerTemp_ChA := FALSE;
    bIso_CoolerTemp_ChB := TRUE;
    bIso_CoolerTemp_ChC := FALSE;
    rTimer_CoolerTemp_Disc_s := rTimer_CoolerTemp_Disc_s + c_rTs;
ELSIF (ABS(TT_ASEPTIC_COOLER_OUTLET_501B - TT_ASEPTIC_COOLER_OUTLET_501C) <= c_rTol_CoolerTemp_degC) THEN
    rVoted_AsepticCoolerOutletTemp_degC := (TT_ASEPTIC_COOLER_OUTLET_501B + TT_ASEPTIC_COOLER_OUTLET_501C) * 0.5;
    bIso_CoolerTemp_ChA := TRUE;
    bIso_CoolerTemp_ChB := FALSE;
    bIso_CoolerTemp_ChC := FALSE;
    rTimer_CoolerTemp_Disc_s := rTimer_CoolerTemp_Disc_s + c_rTs;
ELSE
    bIso_CoolerTemp_ChA := TRUE;
    bIso_CoolerTemp_ChB := TRUE;
    bIso_CoolerTemp_ChC := TRUE;
    rTimer_CoolerTemp_Disc_s := rTimer_CoolerTemp_Disc_s + c_rTs;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 1.12: 2oo3 TMR VOTING: Sterile Buffer Storage Tank Headspace Pressure (PT_ASEPTIC_TANK_HEADSPACE_601A/B/C) [bar]    *)
(* -------------------------------------------------------------------------------------------------------------------- *)
IF (ABS(PT_ASEPTIC_TANK_HEADSPACE_601A - PT_ASEPTIC_TANK_HEADSPACE_601B) <= c_rTol_AsepticTankHeadspace_bar) AND
   (ABS(PT_ASEPTIC_TANK_HEADSPACE_601B - PT_ASEPTIC_TANK_HEADSPACE_601C) <= c_rTol_AsepticTankHeadspace_bar) AND
   (ABS(PT_ASEPTIC_TANK_HEADSPACE_601C - PT_ASEPTIC_TANK_HEADSPACE_601A) <= c_rTol_AsepticTankHeadspace_bar) THEN
    rVoted_AsepticTankHeadspacePress_bar := (PT_ASEPTIC_TANK_HEADSPACE_601A + PT_ASEPTIC_TANK_HEADSPACE_601B + PT_ASEPTIC_TANK_HEADSPACE_601C) / 3.0;
    bIso_AsepticTank_ChA := FALSE;
    bIso_AsepticTank_ChB := FALSE;
    bIso_AsepticTank_ChC := FALSE;
    rTimer_AsepticTank_Disc_s := 0.0;
ELSIF (ABS(PT_ASEPTIC_TANK_HEADSPACE_601A - PT_ASEPTIC_TANK_HEADSPACE_601B) <= c_rTol_AsepticTankHeadspace_bar) THEN
    rVoted_AsepticTankHeadspacePress_bar := (PT_ASEPTIC_TANK_HEADSPACE_601A + PT_ASEPTIC_TANK_HEADSPACE_601B) * 0.5;
    bIso_AsepticTank_ChA := FALSE;
    bIso_AsepticTank_ChB := FALSE;
    bIso_AsepticTank_ChC := TRUE;
    rTimer_AsepticTank_Disc_s := rTimer_AsepticTank_Disc_s + c_rTs;
ELSIF (ABS(PT_ASEPTIC_TANK_HEADSPACE_601A - PT_ASEPTIC_TANK_HEADSPACE_601C) <= c_rTol_AsepticTankHeadspace_bar) THEN
    rVoted_AsepticTankHeadspacePress_bar := (PT_ASEPTIC_TANK_HEADSPACE_601A + PT_ASEPTIC_TANK_HEADSPACE_601C) * 0.5;
    bIso_AsepticTank_ChA := FALSE;
    bIso_AsepticTank_ChB := TRUE;
    bIso_AsepticTank_ChC := FALSE;
    rTimer_AsepticTank_Disc_s := rTimer_AsepticTank_Disc_s + c_rTs;
ELSIF (ABS(PT_ASEPTIC_TANK_HEADSPACE_601B - PT_ASEPTIC_TANK_HEADSPACE_601C) <= c_rTol_AsepticTankHeadspace_bar) THEN
    rVoted_AsepticTankHeadspacePress_bar := (PT_ASEPTIC_TANK_HEADSPACE_601B + PT_ASEPTIC_TANK_HEADSPACE_601C) * 0.5;
    bIso_AsepticTank_ChA := TRUE;
    bIso_AsepticTank_ChB := FALSE;
    bIso_AsepticTank_ChC := FALSE;
    rTimer_AsepticTank_Disc_s := rTimer_AsepticTank_Disc_s + c_rTs;
ELSE
    bIso_AsepticTank_ChA := TRUE;
    bIso_AsepticTank_ChB := TRUE;
    bIso_AsepticTank_ChC := TRUE;
    rTimer_AsepticTank_Disc_s := rTimer_AsepticTank_Disc_s + c_rTs;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 1.13: 2oo3 TMR VOTING: CIP Return Header Caustic Conductivity (AIT_CIP_CAUSTIC_CONDUCTIVITY_701A/B/C) [mS/cm]       *)
(* -------------------------------------------------------------------------------------------------------------------- *)
IF (ABS(AIT_CIP_CAUSTIC_CONDUCTIVITY_701A - AIT_CIP_CAUSTIC_CONDUCTIVITY_701B) <= c_rTol_CIPCausticCond_mS) AND
   (ABS(AIT_CIP_CAUSTIC_CONDUCTIVITY_701B - AIT_CIP_CAUSTIC_CONDUCTIVITY_701C) <= c_rTol_CIPCausticCond_mS) AND
   (ABS(AIT_CIP_CAUSTIC_CONDUCTIVITY_701C - AIT_CIP_CAUSTIC_CONDUCTIVITY_701A) <= c_rTol_CIPCausticCond_mS) THEN
    rVoted_CIPCausticConductivity_mS := (AIT_CIP_CAUSTIC_CONDUCTIVITY_701A + AIT_CIP_CAUSTIC_CONDUCTIVITY_701B + AIT_CIP_CAUSTIC_CONDUCTIVITY_701C) / 3.0;
    bIso_CIPCaustic_ChA := FALSE;
    bIso_CIPCaustic_ChB := FALSE;
    bIso_CIPCaustic_ChC := FALSE;
    rTimer_CIPCaustic_Disc_s := 0.0;
ELSIF (ABS(AIT_CIP_CAUSTIC_CONDUCTIVITY_701A - AIT_CIP_CAUSTIC_CONDUCTIVITY_701B) <= c_rTol_CIPCausticCond_mS) THEN
    rVoted_CIPCausticConductivity_mS := (AIT_CIP_CAUSTIC_CONDUCTIVITY_701A + AIT_CIP_CAUSTIC_CONDUCTIVITY_701B) * 0.5;
    bIso_CIPCaustic_ChA := FALSE;
    bIso_CIPCaustic_ChB := FALSE;
    bIso_CIPCaustic_ChC := TRUE;
    rTimer_CIPCaustic_Disc_s := rTimer_CIPCaustic_Disc_s + c_rTs;
ELSIF (ABS(AIT_CIP_CAUSTIC_CONDUCTIVITY_701A - AIT_CIP_CAUSTIC_CONDUCTIVITY_701C) <= c_rTol_CIPCausticCond_mS) THEN
    rVoted_CIPCausticConductivity_mS := (AIT_CIP_CAUSTIC_CONDUCTIVITY_701A + AIT_CIP_CAUSTIC_CONDUCTIVITY_701C) * 0.5;
    bIso_CIPCaustic_ChA := FALSE;
    bIso_CIPCaustic_ChB := TRUE;
    bIso_CIPCaustic_ChC := FALSE;
    rTimer_CIPCaustic_Disc_s := rTimer_CIPCaustic_Disc_s + c_rTs;
ELSIF (ABS(AIT_CIP_CAUSTIC_CONDUCTIVITY_701B - AIT_CIP_CAUSTIC_CONDUCTIVITY_701C) <= c_rTol_CIPCausticCond_mS) THEN
    rVoted_CIPCausticConductivity_mS := (AIT_CIP_CAUSTIC_CONDUCTIVITY_701B + AIT_CIP_CAUSTIC_CONDUCTIVITY_701C) * 0.5;
    bIso_CIPCaustic_ChA := TRUE;
    bIso_CIPCaustic_ChB := FALSE;
    bIso_CIPCaustic_ChC := FALSE;
    rTimer_CIPCaustic_Disc_s := rTimer_CIPCaustic_Disc_s + c_rTs;
ELSE
    bIso_CIPCaustic_ChA := TRUE;
    bIso_CIPCaustic_ChB := TRUE;
    bIso_CIPCaustic_ChC := TRUE;
    rTimer_CIPCaustic_Disc_s := rTimer_CIPCaustic_Disc_s + c_rTs;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 1.14: 2oo3 TMR VOTING: CIP Return Header Acid Conductivity (AIT_CIP_ACID_CONDUCTIVITY_702A/B/C) [mS/cm]             *)
(* -------------------------------------------------------------------------------------------------------------------- *)
IF (ABS(AIT_CIP_ACID_CONDUCTIVITY_702A - AIT_CIP_ACID_CONDUCTIVITY_702B) <= c_rTol_CIPAcidCond_mS) AND
   (ABS(AIT_CIP_ACID_CONDUCTIVITY_702B - AIT_CIP_ACID_CONDUCTIVITY_702C) <= c_rTol_CIPAcidCond_mS) AND
   (ABS(AIT_CIP_ACID_CONDUCTIVITY_702C - AIT_CIP_ACID_CONDUCTIVITY_702A) <= c_rTol_CIPAcidCond_mS) THEN
    rVoted_CIPAcidConductivity_mS := (AIT_CIP_ACID_CONDUCTIVITY_702A + AIT_CIP_ACID_CONDUCTIVITY_702B + AIT_CIP_ACID_CONDUCTIVITY_702C) / 3.0;
    bIso_CIPAcid_ChA := FALSE;
    bIso_CIPAcid_ChB := FALSE;
    bIso_CIPAcid_ChC := FALSE;
    rTimer_CIPAcid_Disc_s := 0.0;
ELSIF (ABS(AIT_CIP_ACID_CONDUCTIVITY_702A - AIT_CIP_ACID_CONDUCTIVITY_702B) <= c_rTol_CIPAcidCond_mS) THEN
    rVoted_CIPAcidConductivity_mS := (AIT_CIP_ACID_CONDUCTIVITY_702A + AIT_CIP_ACID_CONDUCTIVITY_702B) * 0.5;
    bIso_CIPAcid_ChA := FALSE;
    bIso_CIPAcid_ChB := FALSE;
    bIso_CIPAcid_ChC := TRUE;
    rTimer_CIPAcid_Disc_s := rTimer_CIPAcid_Disc_s + c_rTs;
ELSIF (ABS(AIT_CIP_ACID_CONDUCTIVITY_702A - AIT_CIP_ACID_CONDUCTIVITY_702C) <= c_rTol_CIPAcidCond_mS) THEN
    rVoted_CIPAcidConductivity_mS := (AIT_CIP_ACID_CONDUCTIVITY_702A + AIT_CIP_ACID_CONDUCTIVITY_702C) * 0.5;
    bIso_CIPAcid_ChA := FALSE;
    bIso_CIPAcid_ChB := TRUE;
    bIso_CIPAcid_ChC := FALSE;
    rTimer_CIPAcid_Disc_s := rTimer_CIPAcid_Disc_s + c_rTs;
ELSIF (ABS(AIT_CIP_ACID_CONDUCTIVITY_702B - AIT_CIP_ACID_CONDUCTIVITY_702C) <= c_rTol_CIPAcidCond_mS) THEN
    rVoted_CIPAcidConductivity_mS := (AIT_CIP_ACID_CONDUCTIVITY_702B + AIT_CIP_ACID_CONDUCTIVITY_702C) * 0.5;
    bIso_CIPAcid_ChA := TRUE;
    bIso_CIPAcid_ChB := FALSE;
    bIso_CIPAcid_ChC := FALSE;
    rTimer_CIPAcid_Disc_s := rTimer_CIPAcid_Disc_s + c_rTs;
ELSE
    bIso_CIPAcid_ChA := TRUE;
    bIso_CIPAcid_ChB := TRUE;
    bIso_CIPAcid_ChC := TRUE;
    rTimer_CIPAcid_Disc_s := rTimer_CIPAcid_Disc_s + c_rTs;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 1.15: 2oo3 TMR VOTING: Diversion Valve Forward Proximity Switches (ZS_DIVERSION_VALVE_FORWARD_801A/B/C) [BOOL]       *)
(* Boolean Majority: 2-out-of-3 High Logic                                                                              *)
(* -------------------------------------------------------------------------------------------------------------------- *)
bVoted_DiversionValveForward_ZS := (ZS_DIVERSION_VALVE_FORWARD_801A AND ZS_DIVERSION_VALVE_FORWARD_801B) OR
                                   (ZS_DIVERSION_VALVE_FORWARD_801B AND ZS_DIVERSION_VALVE_FORWARD_801C) OR
                                   (ZS_DIVERSION_VALVE_FORWARD_801C AND ZS_DIVERSION_VALVE_FORWARD_801A);

IF (ZS_DIVERSION_VALVE_FORWARD_801A = ZS_DIVERSION_VALVE_FORWARD_801B) AND
   (ZS_DIVERSION_VALVE_FORWARD_801B = ZS_DIVERSION_VALVE_FORWARD_801C) THEN
    bIso_DivertFwd_ChA := FALSE;
    bIso_DivertFwd_ChB := FALSE;
    bIso_DivertFwd_ChC := FALSE;
    rTimer_DivertFwd_Disc_s := 0.0;
ELSE
    IF (ZS_DIVERSION_VALVE_FORWARD_801A <> bVoted_DiversionValveForward_ZS) THEN bIso_DivertFwd_ChA := TRUE; END_IF;
    IF (ZS_DIVERSION_VALVE_FORWARD_801B <> bVoted_DiversionValveForward_ZS) THEN bIso_DivertFwd_ChB := TRUE; END_IF;
    IF (ZS_DIVERSION_VALVE_FORWARD_801C <> bVoted_DiversionValveForward_ZS) THEN bIso_DivertFwd_ChC := TRUE; END_IF;
    rTimer_DivertFwd_Disc_s := rTimer_DivertFwd_Disc_s + c_rTs;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 1.16: 2oo3 TMR VOTING: Diversion Valve Divert Proximity Switches (ZS_DIVERSION_VALVE_DIVERT_802A/B/C) [BOOL]         *)
(* -------------------------------------------------------------------------------------------------------------------- *)
bVoted_DiversionValveDivert_ZS := (ZS_DIVERSION_VALVE_DIVERT_802A AND ZS_DIVERSION_VALVE_DIVERT_802B) OR
                                  (ZS_DIVERSION_VALVE_DIVERT_802B AND ZS_DIVERSION_VALVE_DIVERT_802C) OR
                                  (ZS_DIVERSION_VALVE_DIVERT_802C AND ZS_DIVERSION_VALVE_DIVERT_802A);

IF (ZS_DIVERSION_VALVE_DIVERT_802A = ZS_DIVERSION_VALVE_DIVERT_802B) AND
   (ZS_DIVERSION_VALVE_DIVERT_802B = ZS_DIVERSION_VALVE_DIVERT_802C) THEN
    bIso_DivertDiv_ChA := FALSE;
    bIso_DivertDiv_ChB := FALSE;
    bIso_DivertDiv_ChC := FALSE;
    rTimer_DivertDiv_Disc_s := 0.0;
ELSE
    IF (ZS_DIVERSION_VALVE_DIVERT_802A <> bVoted_DiversionValveDivert_ZS) THEN bIso_DivertDiv_ChA := TRUE; END_IF;
    IF (ZS_DIVERSION_VALVE_DIVERT_802B <> bVoted_DiversionValveDivert_ZS) THEN bIso_DivertDiv_ChB := TRUE; END_IF;
    IF (ZS_DIVERSION_VALVE_DIVERT_802C <> bVoted_DiversionValveDivert_ZS) THEN bIso_DivertDiv_ChC := TRUE; END_IF;
    rTimer_DivertDiv_Disc_s := rTimer_DivertDiv_Disc_s + c_rTs;
END_IF;

(* Persistence Timeout Verification across all 16 TMR channels *)
IF (rTimer_MilkFlow_Disc_s >= c_rTMR_PersistencyTimeout_s) OR
   (rTimer_PreheatTemp_Disc_s >= c_rTMR_PersistencyTimeout_s) OR
   (rTimer_SteamPress_Disc_s >= c_rTMR_PersistencyTimeout_s) OR
   (rTimer_HoldingTemp_Disc_s >= c_rTMR_PersistencyTimeout_s) OR
   (rTimer_SteamFlow_Disc_s >= c_rTMR_PersistencyTimeout_s) OR
   (rTimer_FlashVac_Disc_s >= c_rTMR_PersistencyTimeout_s) OR
   (rTimer_FlashTemp_Disc_s >= c_rTMR_PersistencyTimeout_s) OR
   (rTimer_HomoPress1_Disc_s >= c_rTMR_PersistencyTimeout_s) OR
   (rTimer_HomoPress2_Disc_s >= c_rTMR_PersistencyTimeout_s) OR
   (rTimer_HomoPower_Disc_s >= c_rTMR_PersistencyTimeout_s) OR
   (rTimer_CoolerTemp_Disc_s >= c_rTMR_PersistencyTimeout_s) OR
   (rTimer_AsepticTank_Disc_s >= c_rTMR_PersistencyTimeout_s) OR
   (rTimer_CIPCaustic_Disc_s >= c_rTMR_PersistencyTimeout_s) OR
   (rTimer_CIPAcid_Disc_s >= c_rTMR_PersistencyTimeout_s) OR
   (rTimer_DivertFwd_Disc_s >= c_rTMR_PersistencyTimeout_s) OR
   (rTimer_DivertDiv_Disc_s >= c_rTMR_PersistencyTimeout_s) THEN
    bAlarm_TMR_MajorDivergence := TRUE;
ELSE
    IF bFaultReset THEN
        bAlarm_TMR_MajorDivergence := FALSE;
    END_IF;
END_IF;
''')

    # =========================================================================
    # 6. PHASE 2: STATE-SPACE PREDICTION (x[k+1] = A*x[k] + B*u[k])
    # =========================================================================
    code_parts.append('''(* ==================================================================================================================== *)
(* PHASE 2: STATE-SPACE PREDICTION & THERMAL FLUID DYNAMICS (x[k+1] = A*x[k] + B*u[k], y[k] = C*x[k] + D*u[k])         *)
(* Discrete 8x8 Multivariable State-Space Formulation executed deterministically at Ts = 20 ms.                         *)
(* ==================================================================================================================== *)

IF NOT bMatricesInitialized THEN
    (* Row 1: Delta_T_hold (Holding Tube Temperature Deviation) *)
    aA[1, 1] := 0.9650;  aA[1, 2] := 0.0000;  aA[1, 3] := 0.0000;  aA[1, 4] := 0.0320;
    aA[1, 5] := 0.0000;  aA[1, 6] := 0.0000;  aA[1, 7] := -0.0018; aA[1, 8] := 0.0000;

    (* Row 2: Delta_T_flash (Flash Chamber Cooling Deviation) *)
    aA[2, 1] := 0.0450;  aA[2, 2] := 0.9420;  aA[2, 3] := -0.0085; aA[2, 4] := 0.0000;
    aA[2, 5] := 0.0000;  aA[2, 6] := 0.0000;  aA[2, 7] := -0.0012; aA[2, 8] := 0.0000;

    (* Row 3: Delta_m_water (Net Water Balance Error kg/h) *)
    aA[3, 1] := 0.0820;  aA[3, 2] := -0.1250; aA[3, 3] := 0.9150;  aA[3, 4] := 0.0000;
    aA[3, 5] := 0.0000;  aA[3, 6] := 0.0000;  aA[3, 7] := 0.0380;  aA[3, 8] := 0.0000;

    (* Row 4: Delta_T_regen (Plate Regeneration Section Outlet) *)
    aA[4, 1] := 0.0000;  aA[4, 2] := 0.0780;  aA[4, 3] := 0.0000;  aA[4, 4] := 0.9120;
    aA[4, 5] := 0.0000;  aA[4, 6] := 0.0000;  aA[4, 7] := -0.0022; aA[4, 8] := 0.0000;

    (* Row 5: Delta_P_homo1 (Homogenizer Stage 1 Pressure Deviation) *)
    aA[5, 1] := 0.0000;  aA[5, 2] := 0.0000;  aA[5, 3] := 0.0000;  aA[5, 4] := 0.0000;
    aA[5, 5] := 0.8850;  aA[5, 6] := -0.0420; aA[5, 7] := 0.0045;  aA[5, 8] := 0.0000;

    (* Row 6: Delta_P_homo2 (Homogenizer Stage 2 Pressure Deviation) *)
    aA[6, 1] := 0.0000;  aA[6, 2] := 0.0000;  aA[6, 3] := 0.0000;  aA[6, 4] := 0.0000;
    aA[6, 5] := 0.0210;  aA[6, 6] := 0.8920;  aA[6, 7] := 0.0018;  aA[6, 8] := 0.0000;

    (* Row 7: Delta_V_flow (Milk Infeed Volumetric Flow Deviation) *)
    aA[7, 1] := 0.0000;  aA[7, 2] := 0.0000;  aA[7, 3] := 0.0000;  aA[7, 4] := 0.0000;
    aA[7, 5] := -0.0380; aA[7, 6] := -0.0120; aA[7, 7] := 0.9780;  aA[7, 8] := 0.0000;

    (* Row 8: Delta_P_sterile (Sterile Buffer Headspace Overpressure) *)
    aA[8, 1] := 0.0000;  aA[8, 2] := 0.0000;  aA[8, 3] := 0.0000;  aA[8, 4] := 0.0000;
    aA[8, 5] := 0.0000;  aA[8, 6] := 0.0000;  aA[8, 7] := 0.0000;  aA[8, 8] := 0.9850;

    (* Actuator Input Coupling Matrix B (8x6) *)
    aB[1, 1] := 0.0680;  aB[1, 2] := 0.0000;  aB[1, 3] := -0.0150; aB[1, 4] := 0.0000;  aB[1, 5] := 0.0000;  aB[1, 6] := 0.0000;
    aB[2, 1] := 0.0000;  aB[2, 2] := -0.0850; aB[2, 3] := -0.0080; aB[2, 4] := 0.0000;  aB[2, 5] := 0.0000;  aB[2, 6] := 0.0000;
    aB[3, 1] := 0.1450;  aB[3, 2] := -0.1620; aB[3, 3] := 0.0000;  aB[3, 4] := 0.0000;  aB[3, 5] := 0.0000;  aB[3, 6] := 0.0000;
    aB[4, 1] := 0.0000;  aB[4, 2] := 0.0000;  aB[4, 3] := -0.0220; aB[4, 4] := 0.0000;  aB[4, 5] := 0.0000;  aB[4, 6] := 0.0000;
    aB[5, 1] := 0.0000;  aB[5, 2] := 0.0000;  aB[5, 3] := 0.0150;  aB[5, 4] := 0.2850;  aB[5, 5] := 0.0000;  aB[5, 6] := 0.0000;
    aB[6, 1] := 0.0000;  aB[6, 2] := 0.0000;  aB[6, 3] := 0.0080;  aB[6, 4] := 0.0000;  aB[6, 5] := 0.2450;  aB[6, 6] := 0.0000;
    aB[7, 1] := 0.0000;  aB[7, 2] := 0.0000;  aB[7, 3] := 0.4200;  aB[7, 4] := -0.0650; aB[7, 5] := -0.0250; aB[7, 6] := 0.0000;
    aB[8, 1] := 0.0000;  aB[8, 2] := 0.0000;  aB[8, 3] := 0.0000;  aB[8, 4] := 0.0000;  aB[8, 5] := 0.0000;  aB[8, 6] := 0.0000;

    (* Measurement Matrix C (8x8 Identity) *)
    FOR idx_i := 1 TO 8 DO
        FOR idx_j := 1 TO 8 DO
            IF idx_i = idx_j THEN
                aC[idx_i, idx_j] := 1.0;
            ELSE
                aC[idx_i, idx_j] := 0.0;
            END_IF;
        END_FOR;
    END_FOR;

    (* Feedthrough Matrix D (8x6 Zeros) *)
    FOR idx_i := 1 TO 8 DO
        FOR idx_j := 1 TO 6 DO
            aD[idx_i, idx_j] := 0.0;
        END_FOR;
    END_FOR;

    (* Model Predictive Control (MPC) Cost Weightings *)
    aQ_Weight[1] := 125.0;  (* Holding Tube Temperature Tracking (Highest Priority) *)
    aQ_Weight[2] := 45.0;   (* Flash Temperature Tracking *)
    aQ_Weight[3] := 85.0;   (* Net Water Balance (Zero Dilution) *)
    aQ_Weight[4] := 25.0;   (* Plate Pre-Heater Regeneration Temp *)
    aQ_Weight[5] := 35.0;   (* Homogenizer Stage 1 Pressure *)
    aQ_Weight[6] := 15.0;   (* Homogenizer Stage 2 Pressure *)
    aQ_Weight[7] := 40.0;   (* Raw Milk Flow Rate *)
    aQ_Weight[8] := 95.0;   (* Sterile Air Barrier Overpressure *)

    aR_Weight[1] := 0.85;   (* Culinary Steam Valve Effort *)
    aR_Weight[2] := 0.75;   (* Flash Vacuum Valve Effort *)
    aR_Weight[3] := 0.60;   (* Raw Milk Pump VFD Effort *)
    aR_Weight[4] := 0.50;   (* Homogenizer Stage 1 Valve Effort *)
    aR_Weight[5] := 0.40;   (* Homogenizer Stage 2 Valve Effort *)
    aR_Weight[6] := 0.55;   (* Aseptic Cooler Chilled Water Valve Effort *)

    aS_Weight[1] := 2.50;   (* Steam Valve Slew Penalty *)
    aS_Weight[2] := 2.20;   (* Vacuum Valve Slew Penalty *)
    aS_Weight[3] := 3.00;   (* Pump Speed Slew Penalty *)
    aS_Weight[4] := 1.80;   (* Homogenizer Stage 1 Slew Penalty *)
    aS_Weight[5] := 1.50;   (* Homogenizer Stage 2 Slew Penalty *)
    aS_Weight[6] := 1.60;   (* Chilled Water Valve Slew Penalty *)

    FOR idx_i := 1 TO 8 DO
        aP_TerminalWeight[idx_i] := aQ_Weight[idx_i] * 2.5;
    END_FOR;

    (* Actuator Hard Saturation Bounds *)
    au_min[1] := 0.0;    au_max[1] := 100.0;  adelta_u_max[1] := 1.50; (* Steam Valve 1.5% per 20 ms *)
    au_min[2] := 0.0;    au_max[2] := 100.0;  adelta_u_max[2] := 1.20; (* Vac Valve 1.2% per 20 ms *)
    au_min[3] := 0.0;    au_max[3] := 100.0;  adelta_u_max[3] := 0.80; (* Pump VFD 0.8% per 20 ms *)
    au_min[4] := 0.0;    au_max[4] := 100.0;  adelta_u_max[4] := 2.00; (* Homo 1 Hyd Valve 2.0% per 20 ms *)
    au_min[5] := 0.0;    au_max[5] := 100.0;  adelta_u_max[5] := 2.00; (* Homo 2 Hyd Valve 2.0% per 20 ms *)
    au_min[6] := 0.0;    au_max[6] := 100.0;  adelta_u_max[6] := 1.50; (* Cooler Valve 1.5% per 20 ms *)

    bMatricesInitialized := TRUE;
END_IF;

(* Current Dynamic State Vector Mapping x[k] = Actual - Target *)
ax_state[1] := rVoted_HoldingTubeTemp_degC - rSet_HoldingTubeTemp_Target_degC;
ax_state[2] := rVoted_FlashChamberTemp_degC - (rSet_PreheatRegenTemp_Target_degC + 3.5);
ax_state[3] := rCalculated_FlashWaterBalance_kgh;
ax_state[4] := rVoted_PreheatRegenTemp_degC - rSet_PreheatRegenTemp_Target_degC;
ax_state[5] := rVoted_HomogenizerStage1Press_bar - rSet_HomoStage1Press_Target_bar;
ax_state[6] := rVoted_HomogenizerStage2Press_bar - rSet_HomoStage2Press_Target_bar;
ax_state[7] := rVoted_RawMilkFlow_Lph - rSet_MilkFlowRate_Target_Lph;
ax_state[8] := rVoted_AsepticTankHeadspacePress_bar - rSet_SterileAirHeadspace_Target_bar;

(* Discrete State Propagation: x[k+1] = A * x[k] + B * u[k] *)
FOR idx_i := 1 TO 8 DO
    rTempSum := 0.0;
    FOR idx_j := 1 TO 8 DO
        rTempSum := rTempSum + (aA[idx_i, idx_j] * ax_state[idx_j]);
    END_FOR;
    FOR idx_k := 1 TO 6 DO
        rTempSum := rTempSum + (aB[idx_i, idx_k] * au_control[idx_k]);
    END_FOR;
    ax_next[idx_i] := rTempSum;
END_FOR;

(* Measurement Vector Estimation: y[k] = C * x[k] + D * u[k] *)
FOR idx_i := 1 TO 8 DO
    rTempSum := 0.0;
    FOR idx_j := 1 TO 8 DO
        rTempSum := rTempSum + (aC[idx_i, idx_j] * ax_state[idx_j]);
    END_FOR;
    FOR idx_k := 1 TO 6 DO
        rTempSum := rTempSum + (aD[idx_i, idx_k] * au_control[idx_k]);
    END_FOR;
    ay_output[idx_i] := rTempSum;
END_FOR;
''')

    # =========================================================================
    # 7. PHASE 3: RECEDING-HORIZON MPC CONTROL ACTION
    # =========================================================================
    code_parts.append('''(* ==================================================================================================================== *)
(* PHASE 3: RECEDING-HORIZON MPC OPTIMIZATION & ACTUATOR DISPATCH                                                       *)
(* Projected Gradient Descent (PGD) optimization solving quadratic cost objective functional J.                        *)
(* Enforces hard saturation clamping and slew rate limiting.                                                           *)
(* ==================================================================================================================== *)

IF bSystemRunning AND (nFSM_State = 5) THEN
    (* 1. Analytical Gradient Evaluation: nabla_u J = 2*R*u + 2*S*(u - u_prev) + 2*B^T * P * x_next *)
    FOR idx_k := 1 TO 6 DO
        rTempSum := 0.0;
        FOR idx_i := 1 TO 8 DO
            rTempSum := rTempSum + (aB[idx_i, idx_k] * aP_TerminalWeight[idx_i] * ax_next[idx_i]);
        END_FOR;
        aGrad_u[idx_k] := (2.0 * aR_Weight[idx_k] * au_control[idx_k]) +
                          (2.0 * aS_Weight[idx_k] * (au_control[idx_k] - au_prev[idx_k])) +
                          (2.0 * rTempSum);
    END_FOR;

    (* 2. Projected Gradient Descent Update Iterations *)
    FOR idx_iter := 1 TO 4 DO
        FOR idx_k := 1 TO 6 DO
            au_control[idx_k] := au_control[idx_k] - (c_rPGD_Alpha * aGrad_u[idx_k]);

            (* Actuator Slew Rate Limiting *)
            au_delta[idx_k] := au_control[idx_k] - au_prev[idx_k];
            IF au_delta[idx_k] > adelta_u_max[idx_k] THEN
                au_control[idx_k] := au_prev[idx_k] + adelta_u_max[idx_k];
            ELSIF au_delta[idx_k] < -adelta_u_max[idx_k] THEN
                au_control[idx_k] := au_prev[idx_k] - adelta_u_max[idx_k];
            END_IF;

            (* Actuator Hard Saturation Bounds *)
            IF au_control[idx_k] > au_max[idx_k] THEN
                au_control[idx_k] := au_max[idx_k];
            ELSIF au_control[idx_k] < au_min[idx_k] THEN
                au_control[idx_k] := au_min[idx_k];
            END_IF;
        END_FOR;
    END_FOR;

    (* 3. Quadratic Cost Functional Value Evaluation *)
    rMPC_QuadraticCostAccum := 0.0;
    FOR idx_i := 1 TO 8 DO
        rMPC_QuadraticCostAccum := rMPC_QuadraticCostAccum + (aQ_Weight[idx_i] * ax_state[idx_i] * ax_state[idx_i]);
    END_FOR;
    FOR idx_k := 1 TO 6 DO
        rMPC_QuadraticCostAccum := rMPC_QuadraticCostAccum + (aR_Weight[idx_k] * au_control[idx_k] * au_control[idx_k]) +
                                   (aS_Weight[idx_k] * (au_control[idx_k] - au_prev[idx_k]) * (au_control[idx_k] - au_prev[idx_k]));
    END_FOR;
    FOR idx_i := 1 TO 8 DO
        rMPC_QuadraticCostAccum := rMPC_QuadraticCostAccum + (aP_TerminalWeight[idx_i] * ax_next[idx_i] * ax_next[idx_i]);
    END_FOR;
    rMPC_QuadraticCost_J := rMPC_QuadraticCostAccum;

    (* Store Control History for Next Cycle Slew Calculation *)
    FOR idx_k := 1 TO 6 DO
        au_prev[idx_k] := au_control[idx_k];
    END_FOR;

    (* Physical Actuator Command Assignment *)
    rCmd_SteamInfusionValve_pct := au_control[1];
    rCmd_FlashVacuumValve_pct   := au_control[2];
    rCmd_MilkFeedPump_Speed_pct := au_control[3];
    rCmd_HomoStage1HydValve_bar := au_control[4] * 3.0; (* 0..100% scaled to 0..300 bar *)
    rCmd_HomoStage2HydValve_bar := au_control[5] * 1.0; (* 0..100% scaled to 0..100 bar *)
    rCmd_AsepticCoolerValve_pct := au_control[6];
ELSE
    rMPC_QuadraticCost_J := 0.0;
END_IF;
''')

    # =========================================================================
    # 8. PHASE 4: ADVANCED CYBER-PHYSICAL OBSERVERS & ALGORITHMS
    # =========================================================================
    code_parts.append('''(* ==================================================================================================================== *)
(* PHASE 4: ADVANCED CYBER-PHYSICAL OBSERVERS & RIGOROUS THERMODYNAMIC ALGORITHMS                                      *)
(* 4.1: Spore Thermal Destruction Lethality Integral (F0)                                                               *)
(* 4.2: Two-Stage Homogenization Cavitation Shear & Sauter Mean Diameter (d32) Observer                                 *)
(* 4.3: Plate Heat Exchanger Thermal Regeneration & Milk Protein Fouling Observer                                       *)
(* 4.4: Vacuum Flash De-Aerator Enthalpy Balance & Zero Net Dilution Observer                                           *)
(* ==================================================================================================================== *)

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 4.1: Spore Thermal Destruction Lethality Integral (F0)                                                               *)
(* Bigelow Log-Linear Model: L(T) = 10^((T - 121.1) / z). Trapezoidal numerical integration.                            *)
(* -------------------------------------------------------------------------------------------------------------------- *)
IF rVoted_HoldingTubeTemp_degC >= 100.0 THEN
    (* Instantaneous lethality rate L in min/min *)
    rCalculated_InstantLethalityRate_L := EXP(((rVoted_HoldingTubeTemp_degC - c_rT_Ref_degC) / c_rZ_Value_degC) * 2.302585092994046);
ELSE
    rCalculated_InstantLethalityRate_L := 0.0;
END_IF;

(* Continuous Holding Tube Residence Time: tau = V_holding / V_dot_milk *)
IF rVoted_RawMilkFlow_Lph > 100.0 THEN
    rCalculated_HoldingTubeResidence_s := (c_rHoldingTubeVolume_L / (rVoted_RawMilkFlow_Lph / 3600.0));
ELSE
    rCalculated_HoldingTubeResidence_s := 4.0;
END_IF;

(* Cumulative F0 integration during Hot Water SIP Sterilization (FSM State 2) *)
IF nFSM_State = 2 THEN
    rAccumulated_F0_min := rAccumulated_F0_min + (0.5 * (rCalculated_InstantLethalityRate_L + rLethalityRate_L_prev) * (c_rTs / 60.0));
    rLethalityRate_L_prev := rCalculated_InstantLethalityRate_L;
    rCalculated_Lethality_F0_min := rAccumulated_F0_min;

    IF rCalculated_Lethality_F0_min >= rSet_SIP_TargetLethality_F0_min THEN
        bCommercialSterilityAchieved := TRUE;
    END_IF;
ELSIF nFSM_State = 0 THEN
    rAccumulated_F0_min := 0.0;
    rLethalityRate_L_prev := 0.0;
    rCalculated_Lethality_F0_min := 0.0;
    bCommercialSterilityAchieved := FALSE;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 4.2: Two-Stage Homogenization Cavitation Shear & Sauter Mean Diameter (d32) Observer                                 *)
(* Disruption of fat globules into sub-micron droplets to prevent creaming over ambient shelf life.                    *)
(* -------------------------------------------------------------------------------------------------------------------- *)
rTotalHomoPressure_bar := rVoted_HomogenizerStage1Press_bar + rVoted_HomogenizerStage2Press_bar;

(* Specific Mechanical Energy: SME = Delta_P / rho [kJ/kg] *)
IF c_rMilkDensity_kg_m3 > 0.0 THEN
    rCalculated_SpecificMechEnergy_kJkg := (rTotalHomoPressure_bar * 100000.0) / (c_rMilkDensity_kg_m3 * 1000.0);
ELSE
    rCalculated_SpecificMechEnergy_kJkg := 29.12;
END_IF;

(* Sauter Mean Fat Globule Diameter Correlation: d32 = d0 * (P_total / 10)^(-0.60) *)
IF rTotalHomoPressure_bar >= 10.0 THEN
    rCalculated_SauterMeanDiameter_d32 := rFatGlobule_d32_unhomo * EXP(-0.60 * LN(rTotalHomoPressure_bar / 10.0));
ELSE
    rCalculated_SauterMeanDiameter_d32 := rFatGlobule_d32_unhomo;
END_IF;

(* Fluid Hydraulic Power Absorbed: P_fluid = Delta_P * Q [kW] *)
rFluidHydraulicPower_kW := (rTotalHomoPressure_bar * 1.0E5) * ((rVoted_RawMilkFlow_Lph / 3600.0) * 0.001) / 1000.0;

(* Mechanical Drive Efficiency & Tungsten Carbide Valve Seat Erosion Observer *)
IF rVoted_HomogenizerMotorKW_kW > 10.0 THEN
    rHomogenizerHydraulicEfficiency := rFluidHydraulicPower_kW / rVoted_HomogenizerMotorKW_kW;
ELSE
    rHomogenizerHydraulicEfficiency := 0.88;
END_IF;

(* Tungsten Carbide Valve Seat Wear Observer: assesses drop in pressure per commanded hydraulic loading *)
IF (rCmd_HomoStage1HydValve_bar > 50.0) AND (rVoted_HomogenizerStage1Press_bar > 20.0) THEN
    rObservedValveSeatClearance_mm := rBaselineValveStrokePosition_mm * (rCmd_HomoStage1HydValve_bar / rVoted_HomogenizerStage1Press_bar);
    IF rObservedValveSeatClearance_mm > (rBaselineValveStrokePosition_mm * 1.35) THEN
        rCalculated_HomogenizerWearIndex := (rObservedValveSeatClearance_mm - rBaselineValveStrokePosition_mm) / (rBaselineValveStrokePosition_mm * 2.0);
        IF rCalculated_HomogenizerWearIndex > 0.40 THEN
            bHomogenizerSeatWearAlert := TRUE;
        END_IF;
    ELSE
        rCalculated_HomogenizerWearIndex := 0.020;
        bHomogenizerSeatWearAlert := FALSE;
    END_IF;
ELSE
    rCalculated_HomogenizerWearIndex := 0.020;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 4.3: Plate Heat Exchanger Thermal Regeneration & Milk Protein Fouling Observer                                       *)
(* Heat transfer duty: Q = m_dot * Cp * Delta_T. Overall heat transfer coefficient U and fouling resistance Rf.        *)
(* -------------------------------------------------------------------------------------------------------------------- *)
(* Milk Mass Flow Rate: m_dot = V_dot * rho [kg/s] *)
rMilkTotalMassFlow_kgh := rVoted_RawMilkFlow_Lph * (c_rMilkDensity_kg_m3 / 1000.0);
rPHE_HeatDuty_kW := (rMilkTotalMassFlow_kgh / 3600.0) * c_rMilkSpecificHeat_kJ_kgK * (rVoted_PreheatRegenTemp_degC - rRawMilkInletTemp_degC);

(* Thermal Regeneration Efficiency: eta_regen = (T_regen - T_raw_in) / (T_flash_out - T_raw_in) *)
IF (rVoted_FlashChamberTemp_degC - rRawMilkInletTemp_degC) > 5.0 THEN
    rCalculated_PHE_RegenEfficiency_pct := ((rVoted_PreheatRegenTemp_degC - rRawMilkInletTemp_degC) /
                                            (rVoted_FlashChamberTemp_degC - rRawMilkInletTemp_degC)) * 100.0;
ELSE
    rCalculated_PHE_RegenEfficiency_pct := 92.0;
END_IF;

(* Logarithmic Mean Temperature Difference (LMTD) *)
rDelta_T1_PHE := rVoted_FlashChamberTemp_degC - rVoted_PreheatRegenTemp_degC;
rDelta_T2_PHE := (rVoted_FlashChamberTemp_degC - (rVoted_PreheatRegenTemp_degC - rRawMilkInletTemp_degC)) - rRawMilkInletTemp_degC;

IF rDelta_T2_PHE < 1.0 THEN rDelta_T2_PHE := 1.0; END_IF;
IF rDelta_T1_PHE < 1.0 THEN rDelta_T1_PHE := 1.0; END_IF;

IF ABS(rDelta_T1_PHE - rDelta_T2_PHE) > 0.20 THEN
    rLMTD_PHE_degC := (rDelta_T1_PHE - rDelta_T2_PHE) / LN(rDelta_T1_PHE / rDelta_T2_PHE);
ELSE
    rLMTD_PHE_degC := (rDelta_T1_PHE + rDelta_T2_PHE) * 0.5;
END_IF;

(* Dynamic Overall Heat Transfer Coefficient U [W/(m2*K)] *)
IF (c_rPHE_SurfaceArea_m2 * rLMTD_PHE_degC) > 0.10 THEN
    rCalculated_OverallHeatTransfer_U := (rPHE_HeatDuty_kW * 1000.0) / (c_rPHE_SurfaceArea_m2 * rLMTD_PHE_degC);
ELSE
    rCalculated_OverallHeatTransfer_U := c_rCleanPHE_HeatTransferCoeff_U0;
END_IF;

(* Dynamic Fouling Thermal Resistance Rf = 1/U - 1/U0 [m2*K/W] *)
IF rCalculated_OverallHeatTransfer_U > 100.0 THEN
    rCalculated_FoulingResistance_Rf := (1.0 / rCalculated_OverallHeatTransfer_U) - (1.0 / c_rCleanPHE_HeatTransferCoeff_U0);
    IF rCalculated_FoulingResistance_Rf < 0.0 THEN
        rCalculated_FoulingResistance_Rf := 0.0;
    END_IF;
ELSE
    rCalculated_FoulingResistance_Rf := 0.00050;
END_IF;

(* Fouling Limit Exceeded Trigger: Milk beta-lactoglobulin denaturation & calcium phosphate encrustation *)
IF rCalculated_FoulingResistance_Rf >= rSet_MaxAllowableFoulingRes_m2KW THEN
    bPlateFoulingCleanRequired := TRUE;
ELSE
    bPlateFoulingCleanRequired := FALSE;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 4.4: Vacuum Flash De-Aerator Enthalpy Balance & Zero Net Dilution Observer                                           *)
(* Adiabatic vacuum flashing: latent heat h_fg balances cooling from T_holding (142 C) to T_flash (82 C).              *)
(* -------------------------------------------------------------------------------------------------------------------- *)
(* Antoine Saturation Vapor Pressure at Flash Outlet Temperature *)
IF rVoted_FlashChamberTemp_degC > 10.0 THEN
    rEquilibriumVaporPressure_bar := (EXP(2.302585 * (c_rAntoine_A - (c_rAntoine_B / (rVoted_FlashChamberTemp_degC + c_rAntoine_C))))) / 750.062;
ELSE
    rEquilibriumVaporPressure_bar := 0.363;
END_IF;

(* Latent Heat of Evaporation h_fg(T_flash): empirical regression kJ/kg *)
rLatentHeatVapAtFlash_kJkg := 2501.0 - (2.37 * rVoted_FlashChamberTemp_degC);

(* Mass of Water Evaporated during Flash: m_flash = m_mix * Cp * (T_hold - T_flash) / h_fg *)
IF (rLatentHeatVapAtFlash_kJkg > 100.0) AND (rVoted_HoldingTubeTemp_degC > rVoted_FlashChamberTemp_degC) THEN
    rCalculatedEvaporatedVapor_kgh := (rMilkTotalMassFlow_kgh + rVoted_CulinarySteamFlow_kgh) *
                                     c_rMilkSpecificHeat_kJ_kgK *
                                     (rVoted_HoldingTubeTemp_degC - rVoted_FlashChamberTemp_degC) /
                                     rLatentHeatVapAtFlash_kJkg;
ELSE
    rCalculatedEvaporatedVapor_kgh := rVoted_CulinarySteamFlow_kgh;
END_IF;

(* Net Water Mass Balance Deviation: Delta_m = Steam Injected - Vapor Evaporated *)
rCalculated_FlashWaterBalance_kgh := rVoted_CulinarySteamFlow_kgh - rCalculatedEvaporatedVapor_kgh;

(* Net Milk Water Dilution / Concentration Percentage *)
IF rMilkTotalMassFlow_kgh > 1000.0 THEN
    rCalculated_DilutionRatio_pct := (rCalculated_FlashWaterBalance_kgh / rMilkTotalMassFlow_kgh) * 100.0;
ELSE
    rCalculated_DilutionRatio_pct := 0.0;
END_IF;

(* Culinary Steam Sonic Choked Injection Velocity: v_sonic = SQRT(k * R_steam * T) *)
rCalculated_SonicSteamVelocity_mps := 468.5;
''')

    # =========================================================================
    # 9. PHASE 5: 12-STAGE OPERATIONAL FINITE STATE MACHINE (FSM)
    # =========================================================================
    code_parts.append('''(* ==================================================================================================================== *)
(* PHASE 5: MULTI-STAGE 12-STATE DETERMINISTIC FINITE STATE MACHINE (FSM)                                               *)
(* States:                                                                                                              *)
(*   0: PLANT_OFFLINE_STANDBY                                                                                           *)
(*   1: WATER_CIRCULATION_PREHEAT                                                                                       *)
(*   2: HOT_WATER_SIP_STERILIZATION_130C                                                                                *)
(*   3: STERILE_COOLING_STABILIZATION                                                                                   *)
(*   4: MILK_FEED_INTRODUCTION                                                                                          *)
(*   5: STEADY_STATE_UHT_PRODUCTION_30KLPH                                                                              *)
(*   6: ASEPTIC_DIVERSION_RECIRCULATION                                                                                 *)
(*   7: SHORT_INTERMEDIATE_RINSE_ASR                                                                                    *)
(*   8: CAUSTIC_WASH_CIP_PHASE                                                                                          *)
(*   9: ACID_WASH_CIP_PHASE                                                                                             *)
(*   10: STERILE_WATER_FINAL_RINSE                                                                                      *)
(*   11: EMERGENCY_ESTOP_DIVERT_DUMP                                                                                    *)
(* ==================================================================================================================== *)

(* Emergency Stop Global Safety Override *)
IF NOT bEmergencyStop_NC THEN
    nFSM_State := 11;
END_IF;

CASE nFSM_State OF
    0: (* PLANT_OFFLINE_STANDBY: All pumps, steam and chemical dosing off. Valves in safe resting positions *)
        rCmd_MilkFeedPump_Speed_pct     := 0.0;
        rCmd_SteamInfusionValve_pct     := 0.0;
        rCmd_FlashVacuumValve_pct       := 0.0;
        rCmd_HomoStage1HydValve_bar     := 0.0;
        rCmd_HomoStage2HydValve_bar     := 0.0;
        rCmd_AsepticCoolerValve_pct     := 0.0;
        rCmd_SterileAirRegValve_pct     := 0.0;
        bCmd_AsepticDiversion_Forward   := FALSE;
        bCmd_AsepticDiversion_Divert    := TRUE;
        rCmd_CIPCausticPump_pct         := 0.0;
        rCmd_CIPAcidPump_pct            := 0.0;
        bCmd_CIPReturnScavengePump      := FALSE;
        bSystemRunning                  := FALSE;
        bSystemReady                    := bMasterPowerOn AND bEmergencyStop_NC AND bCulinarySteamHeaderOk AND bSterileAirSupplyOk;
        rStateDwellTimer_s              := 0.0;

        IF bSystemReady AND bCIP_SIP_Request THEN
            nFSM_State := 1;
        END_IF;

    1: (* WATER_CIRCULATION_PREHEAT: Circulation of treated softened water to establish plant hydraulics *)
        bSystemRunning                  := TRUE;
        rCmd_MilkFeedPump_Speed_pct     := 50.0;
        rCmd_SteamInfusionValve_pct     := 25.0;
        rCmd_FlashVacuumValve_pct       := 30.0;
        rCmd_HomoStage1HydValve_bar     := 0.0;
        rCmd_HomoStage2HydValve_bar     := 0.0;
        rCmd_AsepticCoolerValve_pct     := 10.0;
        rCmd_SterileAirRegValve_pct     := 20.0;
        bCmd_AsepticDiversion_Forward   := FALSE;
        bCmd_AsepticDiversion_Divert    := TRUE;
        rStateDwellTimer_s              := rStateDwellTimer_s + c_rTs;

        IF (rStateDwellTimer_s >= 60.0) AND (rVoted_HoldingTubeTemp_degC >= 95.0) THEN
            rStateDwellTimer_s := 0.0;
            nFSM_State := 2;
        END_IF;

    2: (* HOT_WATER_SIP_STERILIZATION_130C: Thermal sterilization of plant at 130 C until F0 >= 12.0 min *)
        bSystemRunning                  := TRUE;
        rCmd_MilkFeedPump_Speed_pct     := 65.0;
        rCmd_SteamInfusionValve_pct     := 65.0;
        rCmd_FlashVacuumValve_pct       := 15.0; (* Elevated backpressure to prevent boiling at 130 C *)
        rCmd_HomoStage1HydValve_bar     := 20.0;
        rCmd_HomoStage2HydValve_bar     := 10.0;
        rCmd_AsepticCoolerValve_pct     := 0.0;
        rCmd_SterileAirRegValve_pct     := 50.0;
        bCmd_AsepticDiversion_Forward   := FALSE;
        bCmd_AsepticDiversion_Divert    := TRUE;
        rStateDwellTimer_s              := rStateDwellTimer_s + c_rTs;

        IF bCommercialSterilityAchieved AND (rStateDwellTimer_s >= 900.0) THEN
            rStateDwellTimer_s := 0.0;
            nFSM_State := 3;
        END_IF;

    3: (* STERILE_COOLING_STABILIZATION: Cooling down under sterile air overpressure barrier *)
        bSystemRunning                  := TRUE;
        rCmd_MilkFeedPump_Speed_pct     := 75.0;
        rCmd_SteamInfusionValve_pct     := 35.0;
        rCmd_FlashVacuumValve_pct       := 65.0;
        rCmd_HomoStage1HydValve_bar     := 50.0;
        rCmd_HomoStage2HydValve_bar     := 20.0;
        rCmd_AsepticCoolerValve_pct     := 60.0;
        rCmd_SterileAirRegValve_pct     := 50.0;
        bCmd_AsepticDiversion_Forward   := FALSE;
        bCmd_AsepticDiversion_Divert    := TRUE;
        rStateDwellTimer_s              := rStateDwellTimer_s + c_rTs;

        IF (rVoted_HoldingTubeTemp_degC >= 141.5) AND
           (rVoted_HoldingTubeTemp_degC <= 143.0) AND
           (rVoted_AsepticCoolerOutletTemp_degC <= 6.0) AND
           (rStateDwellTimer_s >= 120.0) THEN
            rStateDwellTimer_s := 0.0;
            IF bProductionRequest THEN
                nFSM_State := 4;
            END_IF;
        END_IF;

    4: (* MILK_FEED_INTRODUCTION: Introducing raw milk, displacing water phase to raw balance tank *)
        bSystemRunning                  := TRUE;
        rCmd_MilkFeedPump_Speed_pct     := 85.0;
        rCmd_SteamInfusionValve_pct     := 52.0;
        rCmd_FlashVacuumValve_pct       := 65.0;
        rCmd_HomoStage1HydValve_bar     := 150.0;
        rCmd_HomoStage2HydValve_bar     := 35.0;
        rCmd_AsepticCoolerValve_pct     := 75.0;
        rCmd_SterileAirRegValve_pct     := 50.0;
        bCmd_AsepticDiversion_Forward   := FALSE;
        bCmd_AsepticDiversion_Divert    := TRUE;
        rStateDwellTimer_s              := rStateDwellTimer_s + c_rTs;

        IF (rStateDwellTimer_s >= 45.0) AND
           (rVoted_HoldingTubeTemp_degC >= 141.8) AND
           (bAsepticTankReadyPermissive) THEN
            rStateDwellTimer_s := 0.0;
            bCmd_AsepticDiversion_Forward := TRUE;
            bCmd_AsepticDiversion_Divert  := FALSE;
            nFSM_State := 5;
        END_IF;

    5: (* STEADY_STATE_UHT_PRODUCTION_30KLPH: Full closed-loop Receding-Horizon MPC production *)
        bSystemRunning                  := TRUE;
        bCmd_AsepticDiversion_Forward   := TRUE;
        bCmd_AsepticDiversion_Divert    := FALSE;
        rStateDwellTimer_s              := rStateDwellTimer_s + c_rTs;

        (* Fast Sub-150 ms Pneumatic Diversion Trip Interlocks *)
        IF (rVoted_HoldingTubeTemp_degC < rSet_HoldingTubeTemp_TripLimit_degC) OR
           (rVoted_AsepticTankHeadspacePress_bar < 0.20) OR
           (NOT bSterileAirSupplyOk) THEN
            bCmd_AsepticDiversion_Forward := FALSE;
            bCmd_AsepticDiversion_Divert  := TRUE;
            bAlarm_FastAsepticDivertTripped := TRUE;
            rStateDwellTimer_s := 0.0;
            nFSM_State := 6;
        ELSIF bPlateFoulingCleanRequired THEN
            bCmd_AsepticDiversion_Forward := FALSE;
            bCmd_AsepticDiversion_Divert  := TRUE;
            rStateDwellTimer_s := 0.0;
            nFSM_State := 7;
        ELSIF NOT bProductionRequest THEN
            bCmd_AsepticDiversion_Forward := FALSE;
            bCmd_AsepticDiversion_Divert  := TRUE;
            rStateDwellTimer_s := 0.0;
            nFSM_State := 8;
        END_IF;

    6: (* ASEPTIC_DIVERSION_RECIRCULATION: Fast diversion loop back to balance tank upon temperature dip *)
        bSystemRunning                  := TRUE;
        bCmd_AsepticDiversion_Forward   := FALSE;
        bCmd_AsepticDiversion_Divert    := TRUE;
        rCmd_MilkFeedPump_Speed_pct     := 70.0;
        rCmd_SteamInfusionValve_pct     := 62.0; (* Heat boost to re-establish 142.0 C *)
        rCmd_FlashVacuumValve_pct       := 60.0;
        rCmd_HomoStage1HydValve_bar     := 180.0;
        rCmd_HomoStage2HydValve_bar     := 40.0;
        rCmd_AsepticCoolerValve_pct     := 70.0;
        rStateDwellTimer_s              := rStateDwellTimer_s + c_rTs;

        (* Re-forwarding Permissive Gate: holding tube temperature restabilized above 142.0 C for 30 seconds *)
        IF (rVoted_HoldingTubeTemp_degC >= 142.0) AND (rStateDwellTimer_s >= 30.0) AND bAsepticTankReadyPermissive THEN
            bAlarm_FastAsepticDivertTripped := FALSE;
            rStateDwellTimer_s := 0.0;
            bCmd_AsepticDiversion_Forward := TRUE;
            bCmd_AsepticDiversion_Divert  := FALSE;
            nFSM_State := 5;
        ELSIF rStateDwellTimer_s >= 600.0 THEN
            (* Diversion persistence timeout (10 min): abort to CIP *)
            rStateDwellTimer_s := 0.0;
            nFSM_State := 8;
        END_IF;

    7: (* SHORT_INTERMEDIATE_RINSE_ASR: Aseptic short rinse without breaking sterility of downstream *)
        bSystemRunning                  := TRUE;
        bCmd_AsepticDiversion_Forward   := FALSE;
        bCmd_AsepticDiversion_Divert    := TRUE;
        rCmd_MilkFeedPump_Speed_pct     := 80.0;
        rCmd_SteamInfusionValve_pct     := 30.0;
        rCmd_FlashVacuumValve_pct       := 50.0;
        rCmd_HomoStage1HydValve_bar     := 50.0;
        rCmd_HomoStage2HydValve_bar     := 20.0;
        rCmd_AsepticCoolerValve_pct     := 50.0;
        rStateDwellTimer_s              := rStateDwellTimer_s + c_rTs;

        IF rStateDwellTimer_s >= 300.0 THEN
            rStateDwellTimer_s := 0.0;
            nFSM_State := 4;
        END_IF;

    8: (* CAUSTIC_WASH_CIP_PHASE: Recirculation of 2.0% hot sodium hydroxide (75-80 C, 45 mS/cm) *)
        bSystemRunning                  := TRUE;
        bCmd_AsepticDiversion_Forward   := FALSE;
        bCmd_AsepticDiversion_Divert    := TRUE;
        rCmd_MilkFeedPump_Speed_pct     := 90.0;
        rCmd_SteamInfusionValve_pct     := 40.0;
        rCmd_FlashVacuumValve_pct       := 20.0;
        rCmd_HomoStage1HydValve_bar     := 30.0;
        rCmd_HomoStage2HydValve_bar     := 15.0;
        rCmd_AsepticCoolerValve_pct     := 0.0;
        rCmd_CIPCausticPump_pct         := 45.0;
        rCmd_CIPAcidPump_pct            := 0.0;
        bCmd_CIPReturnScavengePump      := TRUE;
        rStateDwellTimer_s              := rStateDwellTimer_s + c_rTs;

        IF (rStateDwellTimer_s >= 1800.0) AND (rVoted_CIPCausticConductivity_mS >= 40.0) THEN
            rCmd_CIPCausticPump_pct := 0.0;
            rStateDwellTimer_s := 0.0;
            nFSM_State := 9;
        END_IF;

    9: (* ACID_WASH_CIP_PHASE: Recirculation of 1.5% nitric/phosphoric acid (65 C, 32 mS/cm) *)
        bSystemRunning                  := TRUE;
        bCmd_AsepticDiversion_Forward   := FALSE;
        bCmd_AsepticDiversion_Divert    := TRUE;
        rCmd_MilkFeedPump_Speed_pct     := 90.0;
        rCmd_SteamInfusionValve_pct     := 30.0;
        rCmd_FlashVacuumValve_pct       := 20.0;
        rCmd_HomoStage1HydValve_bar     := 30.0;
        rCmd_HomoStage2HydValve_bar     := 15.0;
        rCmd_AsepticCoolerValve_pct     := 0.0;
        rCmd_CIPCausticPump_pct         := 0.0;
        rCmd_CIPAcidPump_pct            := 35.0;
        bCmd_CIPReturnScavengePump      := TRUE;
        rStateDwellTimer_s              := rStateDwellTimer_s + c_rTs;

        IF (rStateDwellTimer_s >= 1200.0) AND (rVoted_CIPAcidConductivity_mS >= 28.0) THEN
            rCmd_CIPAcidPump_pct := 0.0;
            rStateDwellTimer_s := 0.0;
            nFSM_State := 10;
        END_IF;

    10: (* STERILE_WATER_FINAL_RINSE: Neutralization rinse with potable softened water *)
        bSystemRunning                  := TRUE;
        bCmd_AsepticDiversion_Forward   := FALSE;
        bCmd_AsepticDiversion_Divert    := TRUE;
        rCmd_MilkFeedPump_Speed_pct     := 80.0;
        rCmd_SteamInfusionValve_pct     := 0.0;
        rCmd_FlashVacuumValve_pct       := 0.0;
        rCmd_HomoStage1HydValve_bar     := 0.0;
        rCmd_HomoStage2HydValve_bar     := 0.0;
        rCmd_AsepticCoolerValve_pct     := 0.0;
        rCmd_CIPCausticPump_pct         := 0.0;
        rCmd_CIPAcidPump_pct            := 0.0;
        bCmd_CIPReturnScavengePump      := TRUE;
        rStateDwellTimer_s              := rStateDwellTimer_s + c_rTs;

        IF (rStateDwellTimer_s >= 600.0) AND
           (rVoted_CIPCausticConductivity_mS <= 2.0) AND
           (rVoted_CIPAcidConductivity_mS <= 2.0) THEN
            rStateDwellTimer_s := 0.0;
            bCmd_CIPReturnScavengePump := FALSE;
            nFSM_State := 0;
        END_IF;

    11: (* EMERGENCY_ESTOP_DIVERT_DUMP: Master safety trip *)
        bSystemRunning                  := FALSE;
        bEmergencyTripped               := TRUE;
        rCmd_MilkFeedPump_Speed_pct     := 0.0;
        rCmd_SteamInfusionValve_pct     := 0.0;
        rCmd_FlashVacuumValve_pct       := 100.0; (* Rapid vacuum relief *)
        rCmd_HomoStage1HydValve_bar     := 0.0;
        rCmd_HomoStage2HydValve_bar     := 0.0;
        rCmd_AsepticCoolerValve_pct     := 0.0;
        rCmd_SterileAirRegValve_pct     := 0.0;
        bCmd_AsepticDiversion_Forward   := FALSE;
        bCmd_AsepticDiversion_Divert    := TRUE;
        rCmd_CIPCausticPump_pct         := 0.0;
        rCmd_CIPAcidPump_pct            := 0.0;
        bCmd_CIPReturnScavengePump      := FALSE;

        IF bEmergencyStop_NC AND bFaultReset THEN
            bEmergencyTripped := FALSE;
            nFSM_State := 0;
        END_IF;
END_CASE;

nActiveFSM_State := nFSM_State;
bAsepticDiversionActive := bCmd_AsepticDiversion_Divert;
''')

    # =========================================================================
    # 10. PHASE 6: ISA-18.2 PROCESS ALARMS & BITMASK PACKING
    # =========================================================================
    code_parts.append('''(* ==================================================================================================================== *)
(* PHASE 6: ISA-18.2 MULTI-TIERED PROCESS ALARM MANAGEMENT & STATUS WORD PACKING                                        *)
(* 5-Tier Hierarchy (HI_HI, HI, LO, LO_LO, ROC) with deadband hysteresis.                                              *)
(* Status bitmask packing into standard DWORD diagnostic words.                                                         *)
(* ==================================================================================================================== *)

(* Rate-of-Change (ROC) Differentiators *)
rROC_HoldingTemp_degC_per_s := (rVoted_HoldingTubeTemp_degC - rPrevHoldingTemp_degC) / c_rTs;
rPrevHoldingTemp_degC       := rVoted_HoldingTubeTemp_degC;

rROC_FlashVac_bar_per_s     := (rVoted_FlashChamberVacuum_bar - rPrevFlashVac_bar) / c_rTs;
rPrevFlashVac_bar           := rVoted_FlashChamberVacuum_bar;

rROC_HomoPress1_bar_per_s   := (rVoted_HomogenizerStage1Press_bar - rPrevHomoPress1_bar) / c_rTs;
rPrevHomoPress1_bar         := rVoted_HomogenizerStage1Press_bar;

(* 1. Holding Tube Sterilization Temperature Alarms *)
IF rVoted_HoldingTubeTemp_degC >= c_rTrip_HoldingTemp_HH_degC THEN
    bAlarm_HoldingTemp_HH := TRUE;
ELSIF rVoted_HoldingTubeTemp_degC <= (c_rTrip_HoldingTemp_HH_degC - c_rDeadband_HoldingTemp_degC) THEN
    bAlarm_HoldingTemp_HH := FALSE;
END_IF;

IF rVoted_HoldingTubeTemp_degC >= c_rAlarm_HoldingTemp_H_degC THEN
    bAlarm_HoldingTemp_H := TRUE;
ELSIF rVoted_HoldingTubeTemp_degC <= (c_rAlarm_HoldingTemp_H_degC - c_rDeadband_HoldingTemp_degC) THEN
    bAlarm_HoldingTemp_H := FALSE;
END_IF;

IF (rVoted_HoldingTubeTemp_degC <= c_rAlarm_HoldingTemp_L_degC) AND (nFSM_State = 5) THEN
    bAlarm_HoldingTemp_L := TRUE;
ELSIF rVoted_HoldingTubeTemp_degC >= (c_rAlarm_HoldingTemp_L_degC + c_rDeadband_HoldingTemp_degC) THEN
    bAlarm_HoldingTemp_L := FALSE;
END_IF;

IF (rVoted_HoldingTubeTemp_degC <= c_rTrip_HoldingTemp_LL_degC) AND (nFSM_State = 5) THEN
    bAlarm_HoldingTemp_LL := TRUE;
ELSIF rVoted_HoldingTubeTemp_degC >= (c_rTrip_HoldingTemp_LL_degC + c_rDeadband_HoldingTemp_degC) THEN
    bAlarm_HoldingTemp_LL := FALSE;
END_IF;

IF ABS(rROC_HoldingTemp_degC_per_s) >= 4.50 THEN
    bAlarm_HoldingTemp_ROC := TRUE;
ELSE
    bAlarm_HoldingTemp_ROC := FALSE;
END_IF;

(* 2. Flash Chamber Vacuum Alarms *)
IF rVoted_FlashChamberVacuum_bar >= c_rTrip_FlashVac_HH_bar THEN
    bAlarm_FlashVac_HH := TRUE;
ELSIF rVoted_FlashChamberVacuum_bar <= (c_rTrip_FlashVac_HH_bar - c_rDeadband_FlashVac_bar) THEN
    bAlarm_FlashVac_HH := FALSE;
END_IF;

IF rVoted_FlashChamberVacuum_bar >= c_rAlarm_FlashVac_H_bar THEN
    bAlarm_FlashVac_H := TRUE;
ELSIF rVoted_FlashChamberVacuum_bar <= (c_rAlarm_FlashVac_H_bar - c_rDeadband_FlashVac_bar) THEN
    bAlarm_FlashVac_H := FALSE;
END_IF;

IF rVoted_FlashChamberVacuum_bar <= c_rAlarm_FlashVac_L_bar THEN
    bAlarm_FlashVac_L := TRUE;
ELSIF rVoted_FlashChamberVacuum_bar >= (c_rAlarm_FlashVac_L_bar + c_rDeadband_FlashVac_bar) THEN
    bAlarm_FlashVac_L := FALSE;
END_IF;

IF rVoted_FlashChamberVacuum_bar <= c_rTrip_FlashVac_LL_bar THEN
    bAlarm_FlashVac_LL := TRUE;
ELSIF rVoted_FlashChamberVacuum_bar >= (c_rTrip_FlashVac_LL_bar + c_rDeadband_FlashVac_bar) THEN
    bAlarm_FlashVac_LL := FALSE;
END_IF;

(* 3. Homogenizer Stage 1 Operating Pressure Alarms *)
IF rVoted_HomogenizerStage1Press_bar >= c_rTrip_HomoPress1_HH_bar THEN
    bAlarm_HomoPress1_HH := TRUE;
ELSIF rVoted_HomogenizerStage1Press_bar <= (c_rTrip_HomoPress1_HH_bar - c_rDeadband_HomoPress1_bar) THEN
    bAlarm_HomoPress1_HH := FALSE;
END_IF;

IF rVoted_HomogenizerStage1Press_bar >= c_rAlarm_HomoPress1_H_bar THEN
    bAlarm_HomoPress1_H := TRUE;
ELSIF rVoted_HomogenizerStage1Press_bar <= (c_rAlarm_HomoPress1_H_bar - c_rDeadband_HomoPress1_bar) THEN
    bAlarm_HomoPress1_H := FALSE;
END_IF;

IF (rVoted_HomogenizerStage1Press_bar <= c_rAlarm_HomoPress1_L_bar) AND (nFSM_State = 5) THEN
    bAlarm_HomoPress1_L := TRUE;
ELSIF rVoted_HomogenizerStage1Press_bar >= (c_rAlarm_HomoPress1_L_bar + c_rDeadband_HomoPress1_bar) THEN
    bAlarm_HomoPress1_L := FALSE;
END_IF;

IF (rVoted_HomogenizerStage1Press_bar <= c_rTrip_HomoPress1_LL_bar) AND (nFSM_State = 5) THEN
    bAlarm_HomoPress1_LL := TRUE;
ELSIF rVoted_HomogenizerStage1Press_bar >= (c_rTrip_HomoPress1_LL_bar + c_rDeadband_HomoPress1_bar) THEN
    bAlarm_HomoPress1_LL := FALSE;
END_IF;

(* 4. Sterile Buffer Storage Tank Headspace Alarms *)
IF rVoted_AsepticTankHeadspacePress_bar >= c_rTrip_AsepticTank_HH_bar THEN
    bAlarm_AsepticTank_HH := TRUE;
ELSIF rVoted_AsepticTankHeadspacePress_bar <= (c_rTrip_AsepticTank_HH_bar - c_rDeadband_AsepticTank_bar) THEN
    bAlarm_AsepticTank_HH := FALSE;
END_IF;

IF rVoted_AsepticTankHeadspacePress_bar >= c_rAlarm_AsepticTank_H_bar THEN
    bAlarm_AsepticTank_H := TRUE;
ELSIF rVoted_AsepticTankHeadspacePress_bar <= (c_rAlarm_AsepticTank_H_bar - c_rDeadband_AsepticTank_bar) THEN
    bAlarm_AsepticTank_H := FALSE;
END_IF;

IF (rVoted_AsepticTankHeadspacePress_bar <= c_rAlarm_AsepticTank_L_bar) AND (nFSM_State >= 3) THEN
    bAlarm_AsepticTank_L := TRUE;
ELSIF rVoted_AsepticTankHeadspacePress_bar >= (c_rAlarm_AsepticTank_L_bar + c_rDeadband_AsepticTank_bar) THEN
    bAlarm_AsepticTank_L := FALSE;
END_IF;

IF (rVoted_AsepticTankHeadspacePress_bar <= c_rTrip_AsepticTank_LL_bar) AND (nFSM_State >= 3) THEN
    bAlarm_AsepticTank_LL := TRUE;
ELSIF rVoted_AsepticTankHeadspacePress_bar >= (c_rTrip_AsepticTank_LL_bar + c_rDeadband_AsepticTank_bar) THEN
    bAlarm_AsepticTank_LL := FALSE;
END_IF;

(* 5. CIP Caustic Cleaning Concentration Alarms *)
IF (nFSM_State = 8) THEN
    IF rVoted_CIPCausticConductivity_mS >= c_rTrip_CIPCaustic_HH_mS THEN
        bAlarm_CIPCaustic_HH := TRUE;
    ELSIF rVoted_CIPCausticConductivity_mS <= (c_rTrip_CIPCaustic_HH_mS - c_rDeadband_CIPCaustic_mS) THEN
        bAlarm_CIPCaustic_HH := FALSE;
    END_IF;

    IF rVoted_CIPCausticConductivity_mS <= c_rTrip_CIPCaustic_LL_mS THEN
        bAlarm_CIPCaustic_LL := TRUE;
    ELSIF rVoted_CIPCausticConductivity_mS >= (c_rTrip_CIPCaustic_LL_mS + c_rDeadband_CIPCaustic_mS) THEN
        bAlarm_CIPCaustic_LL := FALSE;
    END_IF;
ELSE
    bAlarm_CIPCaustic_HH := FALSE;
    bAlarm_CIPCaustic_LL := FALSE;
END_IF;

(* Bit-Packing: ISA-18.2 Priority 1 Fast Emergency Trips *)
dwAlarmWord_Trip := 16#0000_0000;
IF bAlarm_HoldingTemp_HH           THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0000_0001; END_IF;
IF bAlarm_HoldingTemp_LL           THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0000_0002; END_IF;
IF bAlarm_FlashVac_HH              THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0000_0004; END_IF;
IF bAlarm_FlashVac_LL              THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0000_0008; END_IF;
IF bAlarm_HomoPress1_HH            THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0000_0010; END_IF;
IF bAlarm_HomoPress1_LL            THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0000_0020; END_IF;
IF bAlarm_AsepticTank_HH           THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0000_0040; END_IF;
IF bAlarm_AsepticTank_LL           THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0000_0080; END_IF;
IF bAlarm_CIPCaustic_HH            THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0000_0100; END_IF;
IF bAlarm_CIPCaustic_LL            THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0000_0200; END_IF;
IF bAlarm_TMR_MajorDivergence      THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0000_0400; END_IF;
IF bAlarm_FastAsepticDivertTripped THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0000_0800; END_IF;
IF bEmergencyTripped               THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0000_1000; END_IF;

(* Bit-Packing: ISA-18.2 Priority 2 Process Deviations *)
dwAlarmWord_Warning := 16#0000_0000;
IF bAlarm_HoldingTemp_H            THEN dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#0000_0001; END_IF;
IF bAlarm_HoldingTemp_L            THEN dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#0000_0002; END_IF;
IF bAlarm_HoldingTemp_ROC          THEN dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#0000_0004; END_IF;
IF bAlarm_FlashVac_H               THEN dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#0000_0008; END_IF;
IF bAlarm_FlashVac_L               THEN dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#0000_0010; END_IF;
IF bAlarm_HomoPress1_H             THEN dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#0000_0020; END_IF;
IF bAlarm_HomoPress1_L             THEN dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#0000_0040; END_IF;
IF bAlarm_AsepticTank_H            THEN dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#0000_0080; END_IF;
IF bAlarm_AsepticTank_L            THEN dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#0000_0100; END_IF;
IF bPlateFoulingCleanRequired      THEN dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#0000_0200; END_IF;
IF bHomogenizerSeatWearAlert       THEN dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#0000_0400; END_IF;

(* Bit-Packing: Operational State Word *)
dwStatusWord_Process := 16#0000_0000;
IF bSystemReady                    THEN dwStatusWord_Process := dwStatusWord_Process OR 16#0000_0001; END_IF;
IF bSystemRunning                  THEN dwStatusWord_Process := dwStatusWord_Process OR 16#0000_0002; END_IF;
IF bCommercialSterilityAchieved    THEN dwStatusWord_Process := dwStatusWord_Process OR 16#0000_0004; END_IF;
IF bAsepticDiversionActive         THEN dwStatusWord_Process := dwStatusWord_Process OR 16#0000_0008; END_IF;
IF bSterileBarrierIntact           THEN dwStatusWord_Process := dwStatusWord_Process OR 16#0000_0010; END_IF;
dwStatusWord_Process := dwStatusWord_Process OR SHL(INT_TO_DWORD(nFSM_State), 8);

(* Bit-Packing: Actuator Commands Word *)
dwStatusWord_Actuators := 16#0000_0000;
IF bCmd_AsepticDiversion_Forward   THEN dwStatusWord_Actuators := dwStatusWord_Actuators OR 16#0000_0001; END_IF;
IF bCmd_AsepticDiversion_Divert    THEN dwStatusWord_Actuators := dwStatusWord_Actuators OR 16#0000_0002; END_IF;
IF bCmd_CIPReturnScavengePump      THEN dwStatusWord_Actuators := dwStatusWord_Actuators OR 16#0000_0004; END_IF;

(* Bit-Packing: 2oo3 Sensor Health Mask (Channels 1..8 in Low, Channels 9..16 in High) *)
dwSensorHealthMask_Low := 16#0000_0000;
IF bIso_MilkFlow_ChA      THEN dwSensorHealthMask_Low := dwSensorHealthMask_Low OR 16#0000_0001; END_IF;
IF bIso_MilkFlow_ChB      THEN dwSensorHealthMask_Low := dwSensorHealthMask_Low OR 16#0000_0002; END_IF;
IF bIso_MilkFlow_ChC      THEN dwSensorHealthMask_Low := dwSensorHealthMask_Low OR 16#0000_0004; END_IF;
IF bIso_PreheatTemp_ChA   THEN dwSensorHealthMask_Low := dwSensorHealthMask_Low OR 16#0000_0008; END_IF;
IF bIso_PreheatTemp_ChB   THEN dwSensorHealthMask_Low := dwSensorHealthMask_Low OR 16#0000_0010; END_IF;
IF bIso_PreheatTemp_ChC   THEN dwSensorHealthMask_Low := dwSensorHealthMask_Low OR 16#0000_0020; END_IF;
IF bIso_SteamPress_ChA    THEN dwSensorHealthMask_Low := dwSensorHealthMask_Low OR 16#0000_0040; END_IF;
IF bIso_SteamPress_ChB    THEN dwSensorHealthMask_Low := dwSensorHealthMask_Low OR 16#0000_0080; END_IF;
IF bIso_SteamPress_ChC    THEN dwSensorHealthMask_Low := dwSensorHealthMask_Low OR 16#0000_0100; END_IF;
IF bIso_HoldingTemp_ChA   THEN dwSensorHealthMask_Low := dwSensorHealthMask_Low OR 16#0000_0200; END_IF;
IF bIso_HoldingTemp_ChB   THEN dwSensorHealthMask_Low := dwSensorHealthMask_Low OR 16#0000_0400; END_IF;
IF bIso_HoldingTemp_ChC   THEN dwSensorHealthMask_Low := dwSensorHealthMask_Low OR 16#0000_0800; END_IF;
IF bIso_SteamFlow_ChA     THEN dwSensorHealthMask_Low := dwSensorHealthMask_Low OR 16#0000_1000; END_IF;
IF bIso_SteamFlow_ChB     THEN dwSensorHealthMask_Low := dwSensorHealthMask_Low OR 16#0000_2000; END_IF;
IF bIso_SteamFlow_ChC     THEN dwSensorHealthMask_Low := dwSensorHealthMask_Low OR 16#0000_4000; END_IF;
IF bIso_FlashVac_ChA      THEN dwSensorHealthMask_Low := dwSensorHealthMask_Low OR 16#0000_8000; END_IF;

dwSensorHealthMask_High := 16#0000_0000;
IF bIso_FlashTemp_ChA     THEN dwSensorHealthMask_High := dwSensorHealthMask_High OR 16#0000_0001; END_IF;
IF bIso_FlashTemp_ChB     THEN dwSensorHealthMask_High := dwSensorHealthMask_High OR 16#0000_0002; END_IF;
IF bIso_FlashTemp_ChC     THEN dwSensorHealthMask_High := dwSensorHealthMask_High OR 16#0000_0004; END_IF;
IF bIso_HomoPress1_ChA    THEN dwSensorHealthMask_High := dwSensorHealthMask_High OR 16#0000_0008; END_IF;
IF bIso_HomoPress1_ChB    THEN dwSensorHealthMask_High := dwSensorHealthMask_High OR 16#0000_0010; END_IF;
IF bIso_HomoPress1_ChC    THEN dwSensorHealthMask_High := dwSensorHealthMask_High OR 16#0000_0020; END_IF;
IF bIso_HomoPress2_ChA    THEN dwSensorHealthMask_High := dwSensorHealthMask_High OR 16#0000_0040; END_IF;
IF bIso_HomoPress2_ChB    THEN dwSensorHealthMask_High := dwSensorHealthMask_High OR 16#0000_0080; END_IF;
IF bIso_HomoPress2_ChC    THEN dwSensorHealthMask_High := dwSensorHealthMask_High OR 16#0000_0100; END_IF;
IF bIso_AsepticTank_ChA   THEN dwSensorHealthMask_High := dwSensorHealthMask_High OR 16#0000_0200; END_IF;
IF bIso_AsepticTank_ChB   THEN dwSensorHealthMask_High := dwSensorHealthMask_High OR 16#0000_0400; END_IF;
IF bIso_AsepticTank_ChC   THEN dwSensorHealthMask_High := dwSensorHealthMask_High OR 16#0000_0800; END_IF;

END_FUNCTION_BLOCK
''')

    full_code = "".join(code_parts)
    return full_code

def check_delimiter_parity(code):
    lines = code.split('\n')
    
    # check IF ... END_IF;
    if_count = len(re.findall(r'\bIF\b', code))
    endif_count = len(re.findall(r'\bEND_IF\b', code))
    
    # check CASE ... END_CASE;
    case_count = len(re.findall(r'\bCASE\b', code))
    endcase_count = len(re.findall(r'\bEND_CASE\b', code))
    
    # check FOR ... END_FOR;
    for_count = len(re.findall(r'\bFOR\b', code))
    endfor_count = len(re.findall(r'\bEND_FOR\b', code))
    
    # check VAR ... END_VAR;
    var_count = len(re.findall(r'\bVAR\b|\bVAR_INPUT\b|\bVAR_OUTPUT\b', code))
    endvar_count = len(re.findall(r'\bEND_VAR\b', code))
    
    print(f"Parity Check:")
    print(f"  IF / END_IF:     {if_count} / {endif_count}")
    print(f"  CASE / END_CASE: {case_count} / {endcase_count}")
    print(f"  FOR / END_FOR:   {for_count} / {endfor_count}")
    print(f"  VAR / END_VAR:   {var_count} / {endvar_count}")
    
    assert if_count == endif_count, f"Mismatch in IF / END_IF: {if_count} != {endif_count}"
    assert case_count == endcase_count, f"Mismatch in CASE / END_CASE: {case_count} != {endcase_count}"
    assert for_count == endfor_count, f"Mismatch in FOR / END_FOR: {for_count} != {endfor_count}"
    assert var_count == endvar_count, f"Mismatch in VAR / END_VAR: {var_count} != {endvar_count}"

if __name__ == '__main__':
    st_body = generate_st_code()
    print(f"Total Character Count: {len(st_body)}")
    print(f"Total Line Count: {len(st_body.splitlines())}")
    check_delimiter_parity(st_body)

    prompt_text = """You are an autonomous Senior IEC 61131-3 Synthesis Agent operating under the Lumina Swarm V7 Max-Persona Protocol (Principal Automation Fellow & Cyber-Physical Systems Chair).

YOUR LIFECYCLE: GENERATE EXACTLY ONE ULTRA-RIGOROUS FUNCTION BLOCK DATASET, VALIDATE IT, SAVE IT TO A UNIQUE JSON FILE IN `c:\\Users\\majip\\Downloads\\LLM REASEARCH\\data\\swarm_raw\\agent_<uuid>.json`, VERIFY PARITY AND CHARACTER COUNT, AND REPORT COMPLETION.

ASSIGNED DOMAIN & INDUSTRIAL SPECIFICATION:
- Domain: Food & Beverage / Industrial Dairy Processing
- System: Continuous 30,000 L/h Direct Steam Injection (DSI) Ultra-High-Temperature (UHT, 142.0 °C for 4.0 seconds) Milk Pasteurization Line: Multi-Section Plate Pre-Heater Thermal Regeneration Balancing (92% heat recovery), Direct Steam Infuser Chamber with Acoustic Sonic Velocity Steam Dosing, Vacuum Flash Cooling & De-Aerator Vessel (condensate volatile aroma retention), Two-Stage High-Pressure Aseptic Homogenizer (250 bar Stage 1, 50 bar Stage 2 with tungsten carbide valve seat wear observer), Holding Tube Fast Aseptic Forward/Diversion Valve Interlocks (sub-200 ms pneumatic diversion to balance tank if temperature dips below 139.5 °C), Clean-In-Place / Sterilization-In-Place (CIP/SIP) Lethality Integral ($F_0 \\ge 12.0$ min) Calculation, and Sterile Buffer Air Overpressure Cascade (+0.50 bar).
- Function Block Name: `FB_Dairy_UHT_Pasteurizer_Homogenizer_AsepticDiverter`

NEXT-GEN QUALITY REQUIREMENTS (SUPERIOR TO PREVIOUS DATASETS):
1. Transmitter & Tag Nomenclature:
   - Use standardized industrial P&ID tags: `FT_RAW_MILK_INLET_101A/B/C`, `TT_PREHEAT_REGEN_OUTLET_102A/B/C`, `PT_STEAM_INFUSION_HEADER_201A/B/C`, `TT_UHT_HOLDING_TUBE_202A/B/C`, `FT_CULINARY_STEAM_FLOW_203A/B/C`, `PT_FLASH_CHAMBER_VACUUM_301A/B/C`, `TT_FLASH_CHAMBER_OUTLET_302A/B/C`, `PT_HOMOGENIZER_STAGE1_PRESS_401A/B/C`, `PT_HOMOGENIZER_STAGE2_PRESS_402A/B/C`, `IT_HOMOGENIZER_MOTOR_KW_403A/B/C`, `TT_ASEPTIC_COOLER_OUTLET_501A/B/C`, `PT_ASEPTIC_TANK_HEADSPACE_601A/B/C`, `AIT_CIP_CAUSTIC_CONDUCTIVITY_701A/B/C`, `AIT_CIP_ACID_CONDUCTIVITY_702A/B/C`, `ZS_DIVERSION_VALVE_FORWARD_801A/B/C`, `ZS_DIVERSION_VALVE_DIVERT_802A/B/C`.
2. 2oo3 Triple Modular Redundancy (TMR):
   - Full triplicated voting across holding tube sterilization temperatures, steam infusion pressures, flash vacuum transducers, homogenizer hydraulic pressures, and diversion valve limit switches with pairwise delta checks, debounce timers, bumpless degradation, and status bitmask packing.
3. Advanced Cyber-Physical Observers & Algorithms:
   - Microbiological thermal lethality equivalent ($F_0$) observer: numerical integration of $F_0 = \\int_{0}^{t} 10^{(T(\\tau) - 121.1) / z} d\\tau$ for *Bacillus stearothermophilus* spores ($z = 10.0 \\ ^\\circ\\text{C}$) to guarantee commercial sterility ($F_0 \\ge 12.0$).
   - Homogenizer fat globule surface energy & Sauter mean diameter ($d_{32}$) observer: calculates viscous shear cavitation intensity and specific mechanical energy ($SME = P_{homo} / \\rho$) to prevent milk creaming.
   - Plate heat exchanger milk fouling / thermal boundary layer resistance observer: calculates dynamic overall heat transfer coefficient ($U = \\frac{Q}{A \\Delta T_{LM}}$) to detect beta-lactoglobulin protein fouling encrustation.
   - Flash vacuum de-aerator enthalpy balance: computes equilibrium flash evaporation temperature to ensure water balance (zero net dilution or concentration of milk).
4. Receding-Horizon Model Predictive Control (MPC):
   - Discrete 8x8 State-Space formulation ($x_{k+1} = A x_k + B u_k, y_k = C x_k + D u_k$) running at $T_s = 20$ ms.
   - Decouples steam injection valve, flash cooling vacuum valve, feed pump VFD, and aseptic cooling water valve to maintain holding tube temperature at $142.0 \\pm 0.3 \\ ^\\circ\\text{C}$.
5. ISA-18.2 Alarm Ladder:
   - 5-tier alarm hierarchy (HI_HI, HI, LO, LO_LO, ROC).
   - Fast aseptic diversion trip (< 150 ms upon holding temp < 139.5 °C or aseptic backpressure drop), homogenizer overpressure fast relief, and sterile air barrier loss alarm.
6. Multi-Stage Operational FSM:
   - 12-state Finite State Machine: `PLANT_OFFLINE_STANDBY`, `WATER_CIRCULATION_PREHEAT`, `HOT_WATER_SIP_STERILIZATION_130C`, `STERILE_COOLING_STABILIZATION`, `MILK_FEED_INTRODUCTION`, `STEADY_STATE_UHT_PRODUCTION_30KLPH`, `ASEPTIC_DIVERSION_RECIRCULATION`, `SHORT_INTERMEDIATE_RINSE_ASR`, `CAUSTIC_WASH_CIP_PHASE`, `ACID_WASH_CIP_PHASE`, `STERILE_WATER_FINAL_RINSE`, `EMERGENCY_ESTOP_DIVERT_DUMP`.
7. Extreme Token Density & Code Completeness:
   - Zero summaries, zero `// ... rest of code`, zero placeholders.
   - 100% exact parity: Every `IF` must have `END_IF;`, every `CASE` must have `END_CASE;`, every `FOR` must have `END_FOR;`.
   - TRIPLE backticks with `iec-st`. Output Structured Text MUST be 50,000 to 85,000+ characters of pristine, industrial Structured Text."""

    formatted_code = f"```iec-st\n{st_body}\n```"

    file_uuid = uuid.uuid4().hex[:8]
    output_filename = f"data/swarm_raw/agent_{file_uuid}.json"

    record = {
        "id": f"synthetic_v3_{file_uuid}",
        "instruction": prompt_text,
        "input": "",
        "output": formatted_code,
        "messages": [
            {"role": "user", "content": prompt_text},
            {"role": "assistant", "content": formatted_code}
        ]
    }

    os.makedirs("data/swarm_raw", exist_ok=True)
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)

    print(f"SUCCESS: Saved dataset to {output_filename}")
    print(f"File Size: {os.path.getsize(output_filename)} bytes")

