# -*- coding: utf-8 -*-
"""
Builder script for:
FB_Marine_LNGCarrier_DualFuel_BoilOffGas_Recondenser
Commercial Sector: Marine Engineering & LNG Cryogenic Fuel Systems
System: 174,000 m3 LNG Carrier Cryogenic Boil-Off Gas (BOG) Handling & High-Pressure Fuel Gas Supply System (FGSS)
"""

import os
import sys
import json
import re

def build_part1_declarations():
    return """FUNCTION_BLOCK FB_Marine_LNGCarrier_DualFuel_BoilOffGas_Recondenser
(*
  ========================================================================================================================
  LUMINA CYBER-PHYSICAL SYNTHETIC AUTONOMOUS INDUSTRIAL AUTOMATION ARCHITECTURE (V7 MAX-PERSONA)
  CORE DOMAIN:       MARINE ENGINEERING & LNG CRYOGENIC FUEL GAS SUPPLY SYSTEMS (FGSS)
  VESSEL CLASS:      174,000 m3 MEMBRANE TANK (MARK III / NO96) LIQUEFIED NATURAL GAS CARRIER (LNGC)
  PROPULSION PLANT:  MAN B&W ME-GI TWO-STROKE DUAL-FUEL HIGH-PRESSURE DIRECT GAS INJECTION ENGINE (300 BAR)
  PROCESS SUBSYSTEM: CRYOGENIC BOIL-OFF GAS (BOG) MULTI-STAGE COMPRESSION & DIRECT-CONTACT RECONDENSER
  EQUIPMENT TRAIN:   1. CRYOGENIC CENTRIFUGAL BOG COMPRESSOR WITH VARIABLE INLET GUIDE VANES (IGV)
                     2. DYNAMIC ANTI-SURGE RECYCLE LOOP WITH PNEUMATIC HIGH-SPEED DIVERTER VALVE
                     3. DIRECT-CONTACT SUBCOOLED LNG SPRAY RECONDENSER COLUMN (5.5 BAR ABS)
                     4. HIGH-PRESSURE CRYOGENIC SUBMERGED MULTI-STAGE FUEL PUMPS (320 BAR DISCHARGE)
                     5. PRINTED CIRCUIT HEAT EXCHANGER (PCHE) SUPERCRITICAL FUEL VAPORIZER WITH GLYCOL-WATER LOOP
                     6. HIGH-PRESSURE FUEL GAS ACCUMULATOR & MAN B&W GAS VALVE UNIT (GVU) DOUBLE-BLOCK-AND-BLEED
                     7. GAS COMBUSTION UNIT (GCU) THERMAL OXIDIZER PEAKING VENT SAFETY SUBSYSTEM
  GOVERNING CODES:   IMO IGC CODE (CH. 16), IGF CODE, IEC 61508 / IEC 61511 SIL-3 HARDWARE FAULT TOLERANCE,
                     ISA-18.2 / IEC 62682 ALARM MANAGEMENT, SIGTTO LNG HANDLING PRINCIPLES, DNV-RU-SHIP PT.5 CH.7.
  MATHEMATICAL CORE: 16x16 DISCRETE STATE-SPACE THERMODYNAMIC EOS PROPAGATION (PENG-ROBINSON REAL GAS),
                     RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) WITH PROJECTED GRADIENT DESCENT,
                     TRIPLE MODULAR REDUNDANCY (2oo3 TMR) SENSOR VOTING WITH DYNAMIC PERSISTENCE & DEGRADATION,
                     12-STAGE OPERATIONAL FINITE STATE MACHINE (FSM), AND 32-BIT PACKED TELEMETRY DIAGNOSTICS.
  ========================================================================================================================
*)
VAR_INPUT
    (* Master Automation Supervisory Permissives & Safety Interlocks *)
    bEnableMasterAuto               : BOOL;   (* FGSS Master Automation Supervisory Permissive [1=Enable, 0=Inhibit] *)
    bMasterTripReset                : BOOL;   (* Marine Emergency Shut Down (ESD) Latched Trip Reset [1=Reset Pulse] *)
    bHardwiredESD_OK                : BOOL;   (* Marine Safety System (MSS) Hardwired Loop Healthy [1=Healthy, 0=Trip] *)
    bCargoTankInertingComplete      : BOOL;   (* Cargo Tanks N2 Inerting Complete Permissive (< 1.0% O2) [1=Ready] *)
    bEngineGasModePermissive        : BOOL;   (* ME-GI Propulsion Engine Ready for Fuel Gas Mode [1=Ready, 0=Fuel Oil] *)
    bMEGI_EngineEmergencyGasTrip    : BOOL;   (* ME-GI Engine Electronic Safety System Gas Block Trip [1=Trip, 0=Healthy] *)
    bGCU_BurnerPermissive           : BOOL;   (* Gas Combustion Unit (GCU) Flame Pilot & Ready Permissive [1=Ready] *)
    
    (* Triple Modular Redundant (2oo3) Cargo Tank Vapor Pressure Transmitters [mbar abs] *)
    rTank_VaporPress_PT101A_mbar    : REAL;   (* Cargo Tank Dome 1 Vapor Pressure Transmitter Channel A [mbar abs] *)
    rTank_VaporPress_PT101B_mbar    : REAL;   (* Cargo Tank Dome 1 Vapor Pressure Transmitter Channel B [mbar abs] *)
    rTank_VaporPress_PT101C_mbar    : REAL;   (* Cargo Tank Dome 1 Vapor Pressure Transmitter Channel C [mbar abs] *)
    
    (* Triple Modular Redundant (2oo3) Cryogenic Compressor Suction Temperature RTDs [deg C] *)
    rComp_SuctTemp_TT201A_degC      : REAL;   (* BOG Compressor Stage 1 Suction Temperature Channel A [deg C] *)
    rComp_SuctTemp_TT201B_degC      : REAL;   (* BOG Compressor Stage 1 Suction Temperature Channel B [deg C] *)
    rComp_SuctTemp_TT201C_degC      : REAL;   (* BOG Compressor Stage 1 Suction Temperature Channel C [deg C] *)
    
    (* Triple Modular Redundant (2oo3) ME-GI 300 Bar Fuel Gas Header Pressure Transmitters [bar] *)
    rMEGI_HeaderPress_PT301A_bar    : REAL;   (* ME-GI Master Fuel Gas Header Pressure Channel A [bar] *)
    rMEGI_HeaderPress_PT301B_bar    : REAL;   (* ME-GI Master Fuel Gas Header Pressure Channel B [bar] *)
    rMEGI_HeaderPress_PT301C_bar    : REAL;   (* ME-GI Master Fuel Gas Header Pressure Channel C [bar] *)
    
    (* Triple Modular Redundant (2oo3) Compressor Machinery Room Optical IR Methane Detectors [% LEL] *)
    rCompRoom_GasLEL_AT401A_pct     : REAL;   (* Cargo Machinery Room CH4 Gas Infrared Detector Channel A [% LEL] *)
    rCompRoom_GasLEL_AT401B_pct     : REAL;   (* Cargo Machinery Room CH4 Gas Infrared Detector Channel B [% LEL] *)
    rCompRoom_GasLEL_AT401C_pct     : REAL;   (* Cargo Machinery Room CH4 Gas Infrared Detector Channel C [% LEL] *)
    
    (* Cryogenic Centrifugal BOG Compressor Process Telemetry *)
    rComp_SuctionPress_PT202_bar    : REAL;   (* BOG Compressor Suction Manifold Absolute Pressure [bar abs] *)
    rComp_Stage1DischPress_PT203_bar: REAL;   (* BOG Compressor Intermediate Stage 1 Discharge Pressure [bar abs] *)
    rComp_Stage2DischPress_PT204_bar: REAL;   (* BOG Compressor Stage 2 Final Discharge Pressure [bar abs] *)
    rComp_DischargeTemp_TT205_degC  : REAL;   (* BOG Compressor Final Discharge Gas Temperature [deg C] *)
    rComp_SuctionFlow_FT201_kgh     : REAL;   (* BOG Compressor Suction Mass Flow Rate [kg/h] *)
    rComp_ShaftSpeed_ST201_rpm      : REAL;   (* BOG Compressor Variable Speed Electric Drive Shaft Speed [rpm] *)
    rComp_BearingVib_VT201_mms      : REAL;   (* BOG Compressor Drive End Bearing Radial Vibration RMS [mm/s] *)
    
    (* Direct-Contact Spray Recondenser Column Subsystem *)
    rRecondenser_Press_PT501_bar    : REAL;   (* Direct-Contact Recondenser Column Operating Pressure [bar abs] *)
    rRecondenser_Level_LT501_pct    : REAL;   (* Recondenser Sump Cryogenic Condensate Liquid Level [%] *)
    rRecondenser_SumpTemp_TT502_degC: REAL;   (* Recondenser Column Sump Subcooled Liquid Temperature [deg C] *)
    rLNG_SpraySupplyPress_PT503_bar : REAL;   (* Subcooled LNG Cargo Spray Pump Supply Header Pressure [bar] *)
    rLNG_SpraySupplyFlow_FT502_m3h  : REAL;   (* Subcooled LNG Spray Inflow Volumetric Rate [m3/h] *)
    rLNG_SprayTemp_TT504_degC       : REAL;   (* Subcooled LNG Spray Liquid Supply Temperature [deg C] *)
    
    (* High-Pressure Submerged Cryogenic Fuel Sendout Pumps & PCHE Vaporizer *)
    rHP_PumpSuctionPress_PT601_bar  : REAL;   (* HP Cryogenic Submerged Fuel Pump Suction Static Head [bar] *)
    rHP_PumpDischargePress_PT602_bar: REAL;   (* HP Cryogenic Fuel Pump Discharge Developed Pressure [bar] *)
    rHP_PumpMotorSpeed_ST601_rpm    : REAL;   (* HP Cryogenic Pump VFD Drive Shaft Speed [rpm] *)
    rHP_PumpMotorPower_JT601_kW     : REAL;   (* HP Cryogenic Pump Drive Motor Electrical Active Power [kW] *)
    rPCHE_GlycolWaterInletTemp_degC : REAL;   (* Glycol-Water PCHE Vaporizer Heating Circuit Inlet Temp [deg C] *)
    rPCHE_GasOutletTemp_TT603_degC  : REAL;   (* PCHE Supercritical Fuel Gas Delivery Exit Temperature [deg C] *)
    rPCHE_GlycolFlow_FT602_m3h      : REAL;   (* Glycol-Water Circulation Volumetric Flow Rate [m3/h] *)
    
    (* ME-GI Propulsion Demands, Gas Combustion Unit (GCU) & Ambient Conditions *)
    rMEGI_FuelGasDemandFlow_kgh     : REAL;   (* MAN B&W ME-GI Propulsion Engine Instantaneous Gas Demand [kg/h] *)
    rGCU_CombustionChamberTemp_degC : REAL;   (* Gas Combustion Unit Incinerator Core Flue Gas Temp [deg C] *)
    bGCU_FlameScannerStatus         : BOOL;   (* Gas Combustion Unit Multi-Spectrum Optical Flame Scanner [1=Flame On] *)
    rAmbientSeaWaterTemp_degC       : REAL;   (* Ship Sub-Surface Hull Ambient Seawater Temperature [deg C] *)
    rAtmosphericPressure_mbar       : REAL;   (* Ambient Atmospheric Barometric Static Pressure [mbar abs] *)
    rScanCycleTime_s                : REAL;   (* PLC Deterministic Discrete Scan Cycle Execution Time [s] *)
END_VAR
VAR_OUTPUT
    (* Continuous Actuator Modulating Commands *)
    rCmd_Comp_IGV_Position_pct      : REAL;   (* BOG Compressor Variable Inlet Guide Vanes (IGV) Angle [0.0 - 100.0 %] *)
    rCmd_Comp_AntiSurgeValve_pct    : REAL;   (* Compressor High-Speed Pneumatic Anti-Surge Recycle Valve [0.0 - 100.0 %] *)
    rCmd_Recondenser_SprayValve_pct : REAL;   (* Subcooled LNG Direct-Contact Spray Regulating Valve [0.0 - 100.0 %] *)
    rCmd_HPPump_VFD_Speed_rpm       : REAL;   (* HP Submerged Cryogenic Fuel Sendout Pump VFD Speed [rpm] *)
    rCmd_MEGI_MasterPCV_pct         : REAL;   (* ME-GI Master Fuel Gas Header Pressure Control Valve [0.0 - 100.0 %] *)
    rCmd_PCHE_GlycolValve_pct       : REAL;   (* PCHE Glycol-Water Heating Circuit Modulating Valve [0.0 - 100.0 %] *)
    rCmd_GCU_PeakingVentValve_pct   : REAL;   (* Gas Combustion Unit BOG Peaking Vent Modulating Valve [0.0 - 100.0 %] *)
    rCmd_Tank_SuctionThrottle_pct   : REAL;   (* Cargo Tanks BOG Common Suction Manifold Throttle Valve [0.0 - 100.0 %] *)
    rCmd_BOG_ReliquefactionReturn_pct:REAL;   (* Recondensed LNG Return Valve to Cargo Tanks [0.0 - 100.0 %] *)
    rCmd_HP_HeaderDepressVent_pct   : REAL;   (* Controlled FGSS 300 Bar Venting Valve to Mast Riser [0.0 - 100.0 %] *)
    
    (* Binary Safety & Double-Block-and-Bleed (DBB) Actuation *)
    bCmd_MEGI_GVU_BlockValve1_Open  : BOOL;   (* Gas Valve Unit Fast-Closing Primary Safety Block Valve [1=Open, 0=Shut] *)
    bCmd_MEGI_GVU_BlockValve2_Open  : BOOL;   (* Gas Valve Unit Fast-Closing Secondary Safety Block Valve [1=Open, 0=Shut] *)
    bCmd_MEGI_GVU_VentValve_Open    : BOOL;   (* Gas Valve Unit High-Pressure Atmospheric Bleed Vent [1=Open, 0=Shut] *)
    bCmd_Tank_BOGSuctionBlock_Open  : BOOL;   (* Cargo Tank Dome BOG Master Suction Isolation Valve [1=Open, 0=Shut] *)
    bCmd_N2_PurgeSupplyValve_Open   : BOOL;   (* Cryogenic System N2 High-Pressure Purge Block Valve [1=Open, 0=Shut] *)
    bCmd_FGSS_MasterESD_Trip        : BOOL;   (* Master Cryogenic Emergency Shut Down Trip to Ship MSS [1=TRIP] *)
    
    (* Validated 2oo3 TMR Process Telemetry *)
    rVoted_CargoTankPress_mbar      : REAL;   (* Validated 2oo3 TMR Cargo Tank Dome Vapor Pressure [mbar abs] *)
    rVoted_CompSuctionTemp_degC     : REAL;   (* Validated 2oo3 TMR Compressor Suction Temperature [deg C] *)
    rVoted_MEGI_HeaderPress_bar     : REAL;   (* Validated 2oo3 TMR ME-GI Fuel Gas Header Pressure [bar] *)
    rVoted_CompRoomGasLEL_pct       : REAL;   (* Validated 2oo3 TMR Compressor Room CH4 Gas Concentration [% LEL] *)
    
    (* Cyber-Physical State Observers & Thermodynamic Metrics *)
    rObs_BOG_GenerationRate_kgh     : REAL;   (* Observed Cargo Tank Natural + Forced Boil-Off Gas Mass Rate [kg/h] *)
    rObs_Comp_SurgeMargin_pct       : REAL;   (* Observed Dynamic Distance to Centrifugal Compressor Surge Line [%] *)
    rObs_Comp_PolytropicHead_kJkg   : REAL;   (* Observed Cryogenic Compressor Polytropic Compression Head [kJ/kg] *)
    rObs_Comp_ShaftPower_kW         : REAL;   (* Observed Compressor Electric Shaft Thermodynamic Power [kW] *)
    rObs_Recondenser_CondRate_kgh   : REAL;   (* Direct-Contact Column Real-Time Vapor Condensation Mass Rate [kg/h] *)
    rObs_HPPump_DeltaPress_bar      : REAL;   (* Submerged Cryogenic Fuel Pump Developed Differential Pressure [bar] *)
    rObs_HPPump_HydraulicPower_kW   : REAL;   (* HP Cryogenic Fuel Pump Instantaneous Hydraulic Fluid Power [kW] *)
    rObs_MEGI_FuelGasDensity_kgm3   : REAL;   (* Observed Supercritical Fuel Gas Real Density (Peng-Robinson) [kg/m3] *)
    rObs_AccumulatorGasMass_kg      : REAL;   (* 300 Bar Fuel Gas Accumulator Bottle Stored Mass Inventory [kg] *)
    rObs_MethaneEmissionAvoided_kgh : REAL;   (* Eco-Friendly Green Propulsion Methane Boil-Off Captured Rate [kg/h] *)
    
    (* Operational Sequencing & ISA-18.2 Diagnostics *)
    iActiveFSM_State                : INT;    (* Active 12-Stage FGSS Operational Finite State Machine Stage [0..12] *)
    dwAlarmWord_1                   : DWORD;  (* ISA-18.2 Critical Process Trips & Double-Block-and-Bleed [Bit-Packed] *)
    dwAlarmWord_2                   : DWORD;  (* ISA-18.2 Process Warnings, Margins & Operating Advisories [Bit-Packed] *)
    dwTMR_Diagnostic_1              : DWORD;  (* 2oo3 TMR Sensor Health, Discrepancies & Degradation Bits [Bit-Packed] *)
    bSystemHealthy                  : BOOL;   (* Master FGSS Cyber-Physical Automation Subsystem Integrity Status *)
END_VAR
VAR
    (* Discrete State-Space Model Matrices (16x16 A, 16x8 B, 8x16 C, 8x8 D) *)
    A                               : ARRAY[1..16, 1..16] OF REAL;
    B                               : ARRAY[1..16, 1..8] OF REAL;
    C                               : ARRAY[1..8, 1..16] OF REAL;
    D                               : ARRAY[1..8, 1..8] OF REAL;
    
    (* Discrete State Vectors and Internal Thermodynamic Model Predictors *)
    x                               : ARRAY[1..16] OF REAL; (* State Vector: Tank P, Manifold P, BOG Rate, T_suct, P_d1, m_c2, m_as, SurgeIdx, P_rc, L_rc, m_spray, P_hp, T_fg, P_me, m_acc, Q_gcu *)
    x_next                          : ARRAY[1..16] OF REAL; (* Next Scan Discrete State Vector *)
    u                               : ARRAY[1..8] OF REAL;  (* Manipulated Vector: IGV%, ASV%, Spray%, HPPump_rpm, MEGI_PCV%, Glycol%, GCU%, SuctThrot% *)
    y                               : ARRAY[1..8] OF REAL;  (* Model Predicted Output Vector *)
    y_sp                            : ARRAY[1..8] OF REAL;  (* Target Setpoint Vector: P_tank, P_cd, SurgeMargin, L_rc, P_rc, P_me(300 bar), T_me(45 C), Q_gcu *)
    
    (* Receding-Horizon Model Predictive Control (MPC) Cost Matrices & Working Storage *)
    Q                               : ARRAY[1..8] OF REAL;  (* State Tracking Error Penalties *)
    R                               : ARRAY[1..8] OF REAL;  (* Actuator Rate Movement Penalties *)
    P_term                          : ARRAY[1..8] OF REAL;  (* Terminal State Error Penalties *)
    u_cand                          : ARRAY[1..8] OF REAL;  (* Projected Gradient Candidate Vector *)
    u_opt                           : ARRAY[1..8] OF REAL;  (* Optimal Actuator Output Vector *)
    u_prev                          : ARRAY[1..8] OF REAL;  (* Previous Scan Actuator Vector *)
    grad                            : ARRAY[1..8] OF REAL;  (* Cost Function Gradient Vector *)
    u_min                           : ARRAY[1..8] OF REAL;  (* Actuator Lower Physical Constraints *)
    u_max                           : ARRAY[1..8] OF REAL;  (* Actuator Upper Physical Constraints *)
    du_max                          : ARRAY[1..8] OF REAL;  (* Maximum Permissible Slew Rate Limit *)
    
    (* 2oo3 TMR Sensor Discrepancy Tracking & Degradation State *)
    (* 1. Cargo Tank Vapor Pressure Transmitters (PT101A, PT101B, PT101C) [mbar abs] *)
    rTankP_Diff_AB                  : REAL;
    rTankP_Diff_BC                  : REAL;
    rTankP_Diff_CA                  : REAL;
    bTankP_Disc_AB                  : BOOL;
    bTankP_Disc_BC                  : BOOL;
    bTankP_Disc_CA                  : BOOL;
    rTankP_DiscAccum_AB_s           : REAL;
    rTankP_DiscAccum_BC_s           : REAL;
    rTankP_DiscAccum_CA_s           : REAL;
    bTankP_A_Healthy                : BOOL := TRUE;
    bTankP_B_Healthy                : BOOL := TRUE;
    bTankP_C_Healthy                : BOOL := TRUE;
    iTankP_HealthyCount             : INT := 3;
    rVoted_TankP_raw                : REAL;
    rPrevVoted_TankP                : REAL;
    
    (* 2. Compressor Suction Temperature RTDs (TT201A, TT201B, TT201C) [deg C] *)
    rSuctT_Diff_AB                  : REAL;
    rSuctT_Diff_BC                  : REAL;
    rSuctT_Diff_CA                  : REAL;
    bSuctT_Disc_AB                  : BOOL;
    bSuctT_Disc_BC                  : BOOL;
    bSuctT_Disc_CA                  : BOOL;
    rSuctT_DiscAccum_AB_s           : REAL;
    rSuctT_DiscAccum_BC_s           : REAL;
    rSuctT_DiscAccum_CA_s           : REAL;
    bSuctT_A_Healthy                : BOOL := TRUE;
    bSuctT_B_Healthy                : BOOL := TRUE;
    bSuctT_C_Healthy                : BOOL := TRUE;
    iSuctT_HealthyCount             : INT := 3;
    rVoted_SuctT_raw                : REAL;
    rPrevVoted_SuctT                : REAL;
    
    (* 3. ME-GI 300 Bar Fuel Gas Header Pressure Transmitters (PT301A, PT301B, PT301C) [bar] *)
    rMEGI_P_Diff_AB                 : REAL;
    rMEGI_P_Diff_BC                 : REAL;
    rMEGI_P_Diff_CA                 : REAL;
    bMEGI_P_Disc_AB                 : BOOL;
    bMEGI_P_Disc_BC                 : BOOL;
    bMEGI_P_Disc_CA                 : BOOL;
    rMEGI_P_DiscAccum_AB_s          : REAL;
    rMEGI_P_DiscAccum_BC_s          : REAL;
    rMEGI_P_DiscAccum_CA_s          : REAL;
    bMEGI_P_A_Healthy               : BOOL := TRUE;
    bMEGI_P_B_Healthy               : BOOL := TRUE;
    bMEGI_P_C_Healthy               : BOOL := TRUE;
    iMEGI_P_HealthyCount            : INT := 3;
    rVoted_MEGI_P_raw               : REAL;
    rPrevVoted_MEGI_P               : REAL;
    
    (* 4. Compressor Machinery Room Optical IR Methane Gas Detectors (AT401A, AT401C, AT401C) [% LEL] *)
    rGasLEL_Diff_AB                 : REAL;
    rGasLEL_Diff_BC                 : REAL;
    rGasLEL_Diff_CA                 : REAL;
    bGasLEL_Disc_AB                 : BOOL;
    bGasLEL_Disc_BC                 : BOOL;
    bGasLEL_Disc_CA                 : BOOL;
    rGasLEL_DiscAccum_AB_s          : REAL;
    rGasLEL_DiscAccum_BC_s          : REAL;
    rGasLEL_DiscAccum_CA_s          : REAL;
    bGasLEL_A_Healthy               : BOOL := TRUE;
    bGasLEL_B_Healthy               : BOOL := TRUE;
    bGasLEL_C_Healthy               : BOOL := TRUE;
    iGasLEL_HealthyCount            : INT := 3;
    rVoted_GasLEL_raw               : REAL;
    rPrevVoted_GasLEL               : REAL;
    
    (* Thermodynamic Physical Constants of Liquefied Natural Gas (Methane CH4 Pure Base) *)
    c_rMethane_MolarMass_kgkmol     : REAL := 16.043;   (* Pure Methane Molecular Weight [kg/kmol] *)
    c_rGasConstant_R_kJkgK          : REAL := 0.51835;  (* Specific Gas Constant R = R_u / M [kJ/kg*K] *)
    c_rMethane_CritTemp_K           : REAL := 190.56;   (* Critical Temperature Tc [K] *)
    c_rMethane_CritPress_bar        : REAL := 45.99;    (* Critical Pressure Pc [bar] *)
    c_rMethane_AcentricFactor_omega : REAL := 0.0115;   (* Pitzer Acentric Factor [dimensionless] *)
    c_rCargoTanksTotalVolume_m3     : REAL := 174000.0; (* LNGC Total Membrane Cargo Tank Capacity [m3] *)
    c_rTankNormalFillFraction       : REAL := 0.985;    (* Maximum Allowable Filling Limit (IGC Code) [ratio] *)
    c_rLNG_LiquidDensity_kgm3       : REAL := 445.0;    (* Subcooled Liquid LNG Density at -161.5 C [kg/m3] *)
    c_rLNG_LatentHeatVap_kJkg       : REAL := 510.0;    (* Latent Heat of Vaporization at 1.013 bar [kJ/kg] *)
    c_rLNG_LiquidCp_kJkgK           : REAL := 3.48;     (* Liquid LNG Specific Heat Capacity [kJ/kg*K] *)
    c_rVaporCp_kJkgK                : REAL := 2.22;     (* Methane Boil-Off Gas Vapor Specific Heat [kJ/kg*K] *)
    c_rPolytropicExponent_n         : REAL := 1.28;     (* Cryogenic Centrifugal Compressor Polytropic Index *)
    c_rPolytropicEfficiency         : REAL := 0.785;    (* Compressor Stage Polytropic Efficiency *)
    c_rAccumulatorVolume_m3         : REAL := 3.20;     (* 300 Bar Supercritical Fuel Gas Buffer Bottle Volume [m3] *)
    c_rDesignPressure_bar           : REAL := 350.0;    (* HP FGSS Pipework Design Pressure Rating [bar] *)
    
    (* Peng-Robinson Equation of State Working Registers *)
    rPR_Tr                          : REAL;
    rPR_m_factor                    : REAL;
    rPR_alpha                       : REAL;
    rPR_a                           : REAL;
    rPR_b                           : REAL;
    rPR_A_dim                       : REAL;
    rPR_B_dim                       : REAL;
    rPR_Z_compressibility           : REAL;
    rPR_Temp_Kelvin                 : REAL;
    rPR_Press_kPa                   : REAL;
    
    (* Compressor Aerodynamic & Anti-Surge Working Registers *)
    rComp_PressRatio                : REAL;
    rComp_SurgeFlowThreshold_kgh    : REAL;
    rComp_SurgeMargin_DeltaFlow     : REAL;
    rComp_SurgeSafetyLine_kgh       : REAL;
    rComp_AntiSurgeValve_Bias       : REAL;
    rComp_PolytropicHead_calc       : REAL;
    rComp_ShaftPower_calc           : REAL;
    
    (* Direct-Contact Recondenser Mass & Energy Balance Registers *)
    rRecondenser_SatTemp_degC       : REAL;
    rRecondenser_Subcooling_DeltaT  : REAL;
    rRecondenser_LatentHeat_eff     : REAL;
    rRecondenser_VaporCondRate_calc : REAL;
    rRecondenser_SprayDemand_m3h    : REAL;
    
    (* High-Pressure Submerged Cryogenic Pump Hydraulic Registers *)
    rHPPump_Head_m                  : REAL;
    rHPPump_MassFlow_kgh            : REAL;
    rHPPump_HydraulicPower_calc     : REAL;
    rHPPump_DeltaPress_calc         : REAL;
    
    (* 12-Stage Master FSM Operational Sequencing Timers & Progression Registers *)
    iFSM_State                      : INT := 0;
    iNextFSM_State                  : INT := 0;
    rInertingTimer_s                : REAL := 0.0;
    rPreCoolTimer_s                 : REAL := 0.0;
    rSuctEqualizeTimer_s            : REAL := 0.0;
    rCompInchingTimer_s             : REAL := 0.0;
    rAntiSurgeTuningTimer_s         : REAL := 0.0;
    rRecondenserStartTimer_s        : REAL := 0.0;
    rHPPumpPrimingTimer_s           : REAL := 0.0;
    rPressurizationTimer_s          : REAL := 0.0;
    rSteadyHoldTimer_s              : REAL := 0.0;
    rGCU_VentTimer_s                : REAL := 0.0;
    rReliquefactionTimer_s          : REAL := 0.0;
    rDepressPurgeTimer_s            : REAL := 0.0;
    rTripHoldTimer_s                : REAL := 0.0;
    
    (* Math & Matrix Propagation Working Variables *)
    rSumAx                          : REAL;
    rSumBu                          : REAL;
    rSumCx                          : REAL;
    rSumDu                          : REAL;
    rCostTotal                      : REAL;
    rCostBest                       : REAL;
    rMPC_StepSize                   : REAL := 0.0150;
    rMPC_HeaderPressurePenalty      : REAL;
    rMPC_TankPressurePenalty        : REAL;
    rMPC_SurgeMarginPenalty         : REAL;
    rMPC_RecondenserLevelPenalty    : REAL;
    
    (* Index Iterators & Initialization Sentinel *)
    i                               : INT;
    j                               : INT;
    k                               : INT;
    m                               : INT;
    n                               : INT;
    iter                            : INT;
    bMatricesInitialized            : BOOL := FALSE;
    bMasterTripLatched              : BOOL := FALSE;
END_VAR
"""

print("Part 1 declarations generated.")
