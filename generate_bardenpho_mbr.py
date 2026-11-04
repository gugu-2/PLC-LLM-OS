import os, sys, json, uuid, re
from verify_tool import verify_st_syntax

def build_iec_code():
    parts = []

    # 1. HEADER BANNER
    parts.append("""FUNCTION_BLOCK FB_Water_Wastewater_Bardenpho_MBR_Aeration
(*
 ====================================================================================================
  LUMINA CYBER-PHYSICAL AUTOMATION ENGINE - SYNTHETIC DATASET V7 MAX-PERSONA
  COMMERCIAL INDUSTRIAL SECTOR : Municipal & Heavy Industrial Wastewater Treatment
  SYSTEM                       : Advanced 200,000 m3/day Multi-Stage Modified Bardenpho (5-Stage BNR)
                                 & Submerged Hollow-Fiber Membrane Bioreactor (MBR) Plant
  PRIMARY SUBSYSTEMS           : 1. Automated Dissolved Oxygen (DO) Aerobic Basins Cascade Aeration
                                    (4 x 450 kW Centrifugal Blowers with VFD, Micro-Porous Ceramic Diffusers
                                    & Dynamic Alpha-Factor Observer)
                                 2. Anoxic Internal Nitrate Recycle (IR) & Return Activated Sludge (RAS) Ratio Pacing
                                 3. Denitrification External Carbon Dosing (Methanol / Sodium Acetate)
                                 4. Simultaneous Co-Precipitation Chemical Phosphorus Removal (Ferric Chloride FeCl3)
                                 5. Submerged Hollow-Fiber MBR Permeate Suction Pumps (TMP & Cyclic Relaxation / Scour)
                                 6. Secondary Clarifier Dynamic Sludge Blanket Height (SBH) Observer (Vesilind Model)
                                 7. Extreme Storm Peak Wet-Weather Flow Diversion & Toxic Spill Basin Isolation
  MATHEMATICAL RIGOR           : Full 8x8 Discrete State-Space Formulation (Ts = 100 ms), ASM2d Biokinetic Equations,
                                 Vesilind Sludge Flux Mass Balance, Darcy MBR Resistance-In-Series Model,
                                 Dynamic OTR/KLa Air Diffuser Fouling Observer, and Receding-Horizon MPC Optimization.
  REGULATORY & SAFETY NORMS    : EPA 832-R-09-001 (Nutrient Control Design Manual: TN < 5.0 mg/L, TP < 0.2 mg/L),
                                 WEF Manual of Practice No. 8, Ten States Standards, ISA-18.2 / IEC 62682,
                                 IEC 61131-3 3rd Edition (Structured Text).
 ====================================================================================================
*)""")

    # 2. VAR_INPUT
    parts.append("""VAR_INPUT
    (* =========================================================================================== *)
    (* 1.0 SUPERVISORY COMMANDS, MASTER PERMISSIVES & SYSTEM TIMING                                *)
    (* =========================================================================================== *)
    bMasterEnable                       : BOOL := FALSE;        (* Master Wastewater Plant Automation Enable [BOOL] *)
    bSafetyCircuitOK                    : BOOL := FALSE;        (* Dual-Channel Safety E-Stop / Basin Interlock Status [BOOL] *)
    bAlarmResetPulse                    : BOOL := FALSE;        (* Operator Alarm Acknowledge and Fault Latch Reset Pulse [BOOL] *)
    bAutoSequenceStart                  : BOOL := FALSE;        (* Supervisory Master Automatic Sequence Start [BOOL] *)
    bManualOverrideMode                 : BOOL := FALSE;        (* Manual Maintenance Mode & Actuator Overrides [BOOL] *)
    bStormWeatherOverride               : BOOL := FALSE;        (* Operator Wet-Weather Storm Surge Mode Forced Override [BOOL] *)
    bDiffuserBumpCleanCmd               : BOOL := FALSE;        (* Manual Ceramic Diffuser Air Bump-Clean Flush Command [BOOL] *)
    rCycleTime_s                        : REAL := 0.100;        (* Deterministic PLC Execution Task Period [s] *)

    (* =========================================================================================== *)
    (* 2.0 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) PROCESS TRANSMITTER TRIPLETS (20 TRIPLETS = 60 CH) *)
    (* =========================================================================================== *)
    (* 2.1 Influent Ammonia Nitrogen Analyzers (AIT_INFLUENT_NH4_101A/B/C) [mg/L N] *)
    AIT_INFLUENT_NH4_101A               : REAL := 28.5;         (* Influent Ammonia ISE Analyzer Ch A [mg/L N] *)
    AIT_INFLUENT_NH4_101B               : REAL := 28.5;         (* Influent Ammonia ISE Analyzer Ch B [mg/L N] *)
    AIT_INFLUENT_NH4_101C               : REAL := 28.5;         (* Influent Ammonia ISE Analyzer Ch C [mg/L N] *)

    (* 2.2 Influent Chemical Oxygen Demand Analyzers (AIT_INFLUENT_COD_102A/B/C) [mg/L COD] *)
    AIT_INFLUENT_COD_102A               : REAL := 420.0;        (* Influent COD UV-Vis Spectrophotometer Ch A [mg/L] *)
    AIT_INFLUENT_COD_102B               : REAL := 420.0;        (* Influent COD UV-Vis Spectrophotometer Ch B [mg/L] *)
    AIT_INFLUENT_COD_102C               : REAL := 420.0;        (* Influent COD UV-Vis Spectrophotometer Ch C [mg/L] *)

    (* 2.3 Raw Wastewater Influent Flowmeters (FT_INFLUENT_FLOW_103A/B/C) [m3/h] *)
    FT_INFLUENT_FLOW_103A               : REAL := 8333.3;       (* Influent Magmeter Ch A [m3/h] (Nominal 200,000 m3/d) *)
    FT_INFLUENT_FLOW_103B               : REAL := 8333.3;       (* Influent Magmeter Ch B [m3/h] (Nominal 200,000 m3/d) *)
    FT_INFLUENT_FLOW_103C               : REAL := 8333.3;       (* Influent Magmeter Ch C [m3/h] (Nominal 200,000 m3/d) *)

    (* 2.4 Aerobic Basin Optical Dissolved Oxygen Analyzers (AIT_AEROBIC_DO_201A/B/C) [mg/L O2] *)
    AIT_AEROBIC_DO_201A                 : REAL := 2.05;         (* Aerobic Basin Luminescent DO Sensor Ch A [mg/L] *)
    AIT_AEROBIC_DO_201B                 : REAL := 2.05;         (* Aerobic Basin Luminescent DO Sensor Ch B [mg/L] *)
    AIT_AEROBIC_DO_201C                 : REAL := 2.05;         (* Aerobic Basin Luminescent DO Sensor Ch C [mg/L] *)

    (* 2.5 Aerobic Basin Nitrate Nitrogen Analyzers (AIT_AEROBIC_NO3_202A/B/C) [mg/L N] *)
    AIT_AEROBIC_NO3_202A                : REAL := 8.20;         (* Aerobic Basin Nitrate ISE Sensor Ch A [mg/L N] *)
    AIT_AEROBIC_NO3_202B                : REAL := 8.20;         (* Aerobic Basin Nitrate ISE Sensor Ch B [mg/L N] *)
    AIT_AEROBIC_NO3_202C                : REAL := 8.20;         (* Aerobic Basin Nitrate ISE Sensor Ch C [mg/L N] *)

    (* 2.6 Aeration Air Header Static Pressure Transmitters (PT_AERATION_HEADER_203A/B/C) [kPa] *)
    PT_AERATION_HEADER_203A             : REAL := 68.5;         (* Aeration Header Static Pressure Ch A [kPa] *)
    PT_AERATION_HEADER_203B             : REAL := 68.5;         (* Aeration Header Static Pressure Ch B [kPa] *)
    PT_AERATION_HEADER_203C             : REAL := 68.5;         (* Aeration Header Static Pressure Ch C [kPa] *)

    (* 2.7 Aeration Blowers Total Air Mass Flowmeters (FT_BLOWER_AIR_FLOW_204A/B/C) [Nm3/h] *)
    FT_BLOWER_AIR_FLOW_204A             : REAL := 42500.0;      (* Blower Air Mass Flowmeter Ch A [Nm3/h] *)
    FT_BLOWER_AIR_FLOW_204B             : REAL := 42500.0;      (* Blower Air Mass Flowmeter Ch B [Nm3/h] *)
    FT_BLOWER_AIR_FLOW_204C             : REAL := 42500.0;      (* Blower Air Mass Flowmeter Ch C [Nm3/h] *)

    (* 2.8 Pre-Anoxic Basin Oxidation-Reduction Potential (AIT_ANOXIC_ORP_301A/B/C) [mV] *)
    AIT_ANOXIC_ORP_301A                 : REAL := -125.0;       (* Pre-Anoxic Basin ORP Sensor Ch A [mV] *)
    AIT_ANOXIC_ORP_301B                 : REAL := -125.0;       (* Pre-Anoxic Basin ORP Sensor Ch B [mV] *)
    AIT_ANOXIC_ORP_301C                 : REAL := -125.0;       (* Pre-Anoxic Basin ORP Sensor Ch C [mV] *)

    (* 2.9 Internal Nitrate Recycle (IR) Flowmeters (FT_INTERNAL_RECYCLE_IR_302A/B/C) [m3/h] *)
    FT_INTERNAL_RECYCLE_IR_302A         : REAL := 25000.0;      (* Internal Nitrate Recycle Magmeter Ch A [m3/h] *)
    FT_INTERNAL_RECYCLE_IR_302B         : REAL := 25000.0;      (* Internal Nitrate Recycle Magmeter Ch B [m3/h] *)
    FT_INTERNAL_RECYCLE_IR_302C         : REAL := 25000.0;      (* Internal Nitrate Recycle Magmeter Ch C [m3/h] *)

    (* 2.10 External Carbon Dosing Metering Flowmeters (FT_CARBON_SOURCE_DOSE_303A/B/C) [L/h] *)
    FT_CARBON_SOURCE_DOSE_303A          : REAL := 85.0;         (* Methanol/Acetate Dosing Coriolis Ch A [L/h] *)
    FT_CARBON_SOURCE_DOSE_303B          : REAL := 85.0;         (* Methanol/Acetate Dosing Coriolis Ch B [L/h] *)
    FT_CARBON_SOURCE_DOSE_303C          : REAL := 85.0;         (* Methanol/Acetate Dosing Coriolis Ch C [L/h] *)

    (* 2.11 Final Effluent Orthophosphate Analyzers (AIT_EFFLUENT_PO4_401A/B/C) [mg/L P] *)
    AIT_EFFLUENT_PO4_401A               : REAL := 0.12;         (* Effluent PO4 Wet Chemical Colorimeter Ch A [mg/L] *)
    AIT_EFFLUENT_PO4_401B               : REAL := 0.12;         (* Effluent PO4 Wet Chemical Colorimeter Ch B [mg/L] *)
    AIT_EFFLUENT_PO4_401C               : REAL := 0.12;         (* Effluent PO4 Wet Chemical Colorimeter Ch C [mg/L] *)

    (* 2.12 Ferric Chloride Coagulant Dosing Flowmeters (FT_FECL3_COAGULANT_DOSE_402A/B/C) [L/h] *)
    FT_FECL3_COAGULANT_DOSE_402A        : REAL := 48.0;         (* FeCl3 Precipitant Coriolis Flowmeter Ch A [L/h] *)
    FT_FECL3_COAGULANT_DOSE_402B        : REAL := 48.0;         (* FeCl3 Precipitant Coriolis Flowmeter Ch B [L/h] *)
    FT_FECL3_COAGULANT_DOSE_402C        : REAL := 48.0;         (* FeCl3 Precipitant Coriolis Flowmeter Ch C [L/h] *)

    (* 2.13 MBR Permeate Suction Absolute Pressure Transmitters (PT_MBR_PERMEATE_SUCTION_501A/B/C) [kPa] *)
    PT_MBR_PERMEATE_SUCTION_501A        : REAL := -18.5;        (* MBR Permeate Pump Suction Pressure Ch A [kPa] *)
    PT_MBR_PERMEATE_SUCTION_501B        : REAL := -18.5;        (* MBR Permeate Pump Suction Pressure Ch B [kPa] *)
    PT_MBR_PERMEATE_SUCTION_501C        : REAL := -18.5;        (* MBR Permeate Pump Suction Pressure Ch C [kPa] *)

    (* 2.14 MBR Transmembrane Differential Pressure Transmitters (DPS_MBR_TMP_502A/B/C) [kPa] *)
    DPS_MBR_TMP_502A                    : REAL := 18.5;         (* Submerged Hollow-Fiber MBR TMP Ch A [kPa] *)
    DPS_MBR_TMP_502B                    : REAL := 18.5;         (* Submerged Hollow-Fiber MBR TMP Ch B [kPa] *)
    DPS_MBR_TMP_502C                    : REAL := 18.5;         (* Submerged Hollow-Fiber MBR TMP Ch C [kPa] *)

    (* 2.15 Secondary Clarifier Sludge Blanket Height Transmitters (LT_CLARIFIER_SLUDGE_BLANKET_601A/B/C) [m] *)
    LT_CLARIFIER_SLUDGE_BLANKET_601A    : REAL := 1.45;         (* Secondary Clarifier Sludge Blanket Ch A [m] *)
    LT_CLARIFIER_SLUDGE_BLANKET_601B    : REAL := 1.45;         (* Secondary Clarifier Sludge Blanket Ch B [m] *)
    LT_CLARIFIER_SLUDGE_BLANKET_601C    : REAL := 1.45;         (* Secondary Clarifier Sludge Blanket Ch C [m] *)

    (* 2.16 Return Activated Sludge (RAS) Flowmeters (FT_RAS_PUMP_FLOW_602A/B/C) [m3/h] *)
    FT_RAS_PUMP_FLOW_602A               : REAL := 6250.0;       (* Return Activated Sludge Magmeter Ch A [m3/h] *)
    FT_RAS_PUMP_FLOW_602B               : REAL := 6250.0;       (* Return Activated Sludge Magmeter Ch B [m3/h] *)
    FT_RAS_PUMP_FLOW_602C               : REAL := 6250.0;       (* Return Activated Sludge Magmeter Ch C [m3/h] *)

    (* 2.17 Mixed Liquor Water Temperature Pt100 RTDs (TI_WATER_TEMP_104A/B/C) [deg C] *)
    TI_WATER_TEMP_104A                  : REAL := 18.5;         (* Aerobic Basin Water Temperature Ch A [deg C] *)
    TI_WATER_TEMP_104B                  : REAL := 18.5;         (* Aerobic Basin Water Temperature Ch B [deg C] *)
    TI_WATER_TEMP_104C                  : REAL := 18.5;         (* Aerobic Basin Water Temperature Ch C [deg C] *)

    (* 2.18 Wastewater Influent pH Glass Electrodes (AIT_INFLUENT_PH_105A/B/C) [pH] *)
    AIT_INFLUENT_PH_105A                : REAL := 7.35;         (* Biological Basin Influent pH Ch A [pH] *)
    AIT_INFLUENT_PH_105B                : REAL := 7.35;         (* Biological Basin Influent pH Ch B [pH] *)
    AIT_INFLUENT_PH_105C                : REAL := 7.35;         (* Biological Basin Influent pH Ch C [pH] *)

    (* 2.19 Influent Toxic Spike / Heavy Metals Detectors (AIT_TOXIC_SPIKE_106A/B/C) [ppm] *)
    AIT_TOXIC_SPIKE_106A                : REAL := 0.01;         (* Influent Cyanide & Heavy Metal Spike Ch A [ppm] *)
    AIT_TOXIC_SPIKE_106B                : REAL := 0.01;         (* Influent Cyanide & Heavy Metal Spike Ch B [ppm] *)
    AIT_TOXIC_SPIKE_106C                : REAL := 0.01;         (* Influent Cyanide & Heavy Metal Spike Ch C [ppm] *)

    (* 2.20 Storm Peak Equalization Basin Level Radars (LT_STORM_RETENTION_701A/B/C) [m] *)
    LT_STORM_RETENTION_701A             : REAL := 1.20;         (* Storm Retention Basin Level Radar Ch A [m] *)
    LT_STORM_RETENTION_701B             : REAL := 1.20;         (* Storm Retention Basin Level Radar Ch B [m] *)
    LT_STORM_RETENTION_701C             : REAL := 1.20;         (* Storm Retention Basin Level Radar Ch C [m] *)

    (* =========================================================================================== *)
    (* 3.0 PROCESS PARAMETERS, REGULATORY BOUNDS & SUPERVISORY SETPOINTS                           *)
    (* =========================================================================================== *)
    rTargetDO_Setpoint_mg_L             : REAL := 2.00;         (* Aerobic Basin DO Setpoint [mg/L O2] *)
    rTargetEffluentTN_Limit_mg_L        : REAL := 5.00;         (* Regulatory Total Nitrogen Discharge Limit [mg/L N] *)
    rTargetEffluentTP_Limit_mg_L        : REAL := 0.20;         (* Regulatory Total Phosphorus Discharge Limit [mg/L P] *)
    rTargetEffluentTSS_Limit_mg_L       : REAL := 5.00;         (* Regulatory Effluent TSS Turbidity Limit [mg/L] *)
    rTargetAnoxicORP_mV                 : REAL := -120.0;       (* Pre-Anoxic Basin Target ORP Setpoint [mV] *)
    rTargetClarifierBlanket_m           : REAL := 1.50;         (* Target Secondary Clarifier Sludge Blanket [m] *)
    rMaxPermissibleTMP_kPa              : REAL := 35.0;         (* Maximum Normal MBR Transmembrane Pressure [kPa] *)
    rCriticalTMP_Trip_kPa               : REAL := 45.0;         (* Critical Cavitation & Irreversible Fouling Trip [kPa] *)
    rPeakStormFlowThreshold_m3_h        : REAL := 12500.0;      (* Hydraulic Storm Peak Ingress Limit [m3/h] *)
    rToxicSpikeTripThreshold_ppm        : REAL := 0.50;         (* Influent Toxic Spill Immediate Diversion Trip [ppm] *)
    rClarifierDepth_m                   : REAL := 4.50;         (* Physical Depth of Secondary Clarifiers [m] *)
    rClarifierArea_m2                   : REAL := 6200.0;       (* Total Secondary Clarifiers Surface Area [m2] *)
    rBasinVolume_Aerobic_m3             : REAL := 45000.0;      (* Aerobic Zone Total Liquid Volume [m3] *)
    rBasinVolume_Anoxic_m3              : REAL := 28000.0;      (* Pre-Anoxic Zone Liquid Volume [m3] *)
    rBasinLiquidDepth_m                 : REAL := 6.50;         (* Aeration Basin Static Liquid Submergence [m] *)
    rMembraneTotalArea_m2               : REAL := 140000.0;     (* Submerged Hollow-Fiber MBR Active Area [m2] *)
    rNominalMLSS_mg_L                   : REAL := 8500.0;       (* Nominal MBR Mixed Liquor Suspended Solids [mg/L] *)
END_VAR""")

    # 3. VAR_OUTPUT
    parts.append("""VAR_OUTPUT
    (* =========================================================================================== *)
    (* 1.0 ACTUATOR DRIVES, VFD MODULATING SIGNALS & PROCESS INTERFACE COMMANDS                    *)
    (* =========================================================================================== *)
    rBlower01_SpeedCmd_pct              : REAL;                 (* Centrifugal Blower 01 (450 kW) VFD Speed [%] *)
    rBlower02_SpeedCmd_pct              : REAL;                 (* Centrifugal Blower 02 (450 kW) VFD Speed [%] *)
    rBlower03_SpeedCmd_pct              : REAL;                 (* Centrifugal Blower 03 (450 kW) VFD Speed [%] *)
    rBlower04_SpeedCmd_pct              : REAL;                 (* Centrifugal Blower 04 (450 kW) VFD Speed [%] *)
    rBlowerMasterSpeed_pct              : REAL;                 (* Master Aeration Blower VFD Speed Command [%] *)
    rBlowerGuideVanesCmd_deg            : REAL;                 (* Blower Variable Inlet Guide Vanes Position [deg 0..90] *)
    rInternalRecyclePumpVFD_pct         : REAL;                 (* Internal Nitrate Recycle (IR) Pump VFD Speed [%] *)
    rCarbonDosePumpDemand_Lph           : REAL;                 (* Denitrification External Carbon Dosing Rate [L/h] *)
    rFeCl3DosePumpDemand_Lph            : REAL;                 (* FeCl3 Coagulant Metering Pump Demand [L/h] *)
    rMBR_PermeateSuctionPumpVFD_pct     : REAL;                 (* MBR Permeate Suction Pumps VFD Speed [%] *)
    rRAS_PumpVFD_pct                    : REAL;                 (* Return Activated Sludge (RAS) Pumps VFD Speed [%] *)
    rMBR_AirScourBlowerVFD_pct          : REAL;                 (* MBR Hollow-Fiber Air-Scour Blower Speed [%] *)
    rStormDiversionGatePos_pct          : REAL;                 (* Peak Wet-Weather Storm Diversion Gate Position [%] *)

    (* =========================================================================================== *)
    (* 2.0 DISCRETE SOLENOID VALVES, PUMP CONTACTORS & SAFETY INTERLOCKS                           *)
    (* =========================================================================================== *)
    bBlowerMasterRunCmd                 : BOOL;                 (* Aeration Blowers Master Run Command [BOOL] *)
    bMBR_PermeateSuctionRunCmd          : BOOL;                 (* MBR Permeate Suction Harvest Pump Run Command [BOOL] *)
    bMBR_AirScourPulseCmd               : BOOL;                 (* MBR Cyclic Relaxation Air-Scour Pulse Solenoid [BOOL] *)
    bMBR_BackwashPumpRunCmd             : BOOL;                 (* MBR Permeate Reverse Backwash Pump Contactor [BOOL] *)
    bMBR_CIP_IsolationValveOpen         : BOOL;                 (* MBR Clean-In-Place Chemical Isolation Valve Open [BOOL] *)
    bStormDiversionGateOpenCmd          : BOOL;                 (* Storm Peak Wet-Weather Diversion Gate Actuator [BOOL] *)
    bToxicRetentionGateDivertCmd        : BOOL;                 (* Influent Toxic Spill Fast Diversion Gate Open [BOOL] *)
    bDiffuserBumpPurgeValveCmd          : BOOL;                 (* Ceramic Diffuser High-Pressure Air Bump Valve [BOOL] *)
    bClarifierWasteSludgeValveCmd       : BOOL;                 (* Secondary Clarifier WAS Drain Solenoid [BOOL] *)
    bPlantEmergencyIsolationActive      : BOOL;                 (* Facility E-Stop / Critical Basin Isolation Latched [BOOL] *)

    (* =========================================================================================== *)
    (* 3.0 ONLINE 2oo3 VOTED PROCESS VALUES & CYBER-PHYSICAL OBSERVER TELEMETRY                    *)
    (* =========================================================================================== *)
    rVoted_AerobicDO_mg_L               : REAL;                 (* Validated 2oo3 Aerobic Basin DO [mg/L O2] *)
    rVoted_AerobicNO3_mg_L              : REAL;                 (* Validated 2oo3 Aerobic Basin Nitrate [mg/L N] *)
    rVoted_InfluentNH4_mg_L             : REAL;                 (* Validated 2oo3 Influent Ammonia [mg/L N] *)
    rVoted_InfluentCOD_mg_L             : REAL;                 (* Validated 2oo3 Influent COD [mg/L] *)
    rVoted_InfluentFlow_m3_h            : REAL;                 (* Validated 2oo3 Influent Wastewater Flow [m3/h] *)
    rVoted_HeaderPressure_kPa           : REAL;                 (* Validated 2oo3 Aeration Header Pressure [kPa] *)
    rVoted_BlowerAirFlow_Nm3_h          : REAL;                 (* Validated 2oo3 Blower Air Mass Flow [Nm3/h] *)
    rVoted_AnoxicORP_mV                 : REAL;                 (* Validated 2oo3 Pre-Anoxic Basin ORP [mV] *)
    rVoted_EffluentPO4_mg_L             : REAL;                 (* Validated 2oo3 Effluent Orthophosphate [mg/L P] *)
    rVoted_MBR_TMP_kPa                  : REAL;                 (* Validated 2oo3 Submerged MBR TMP [kPa] *)
    rVoted_ClarifierSludgeBlanket_m     : REAL;                 (* Validated 2oo3 Clarifier Sludge Blanket [m] *)
    rVoted_RAS_Flow_m3_h                : REAL;                 (* Validated 2oo3 Return Sludge Flow [m3/h] *)
    rVoted_WaterTemp_degC               : REAL;                 (* Validated 2oo3 Basin Water Temperature [deg C] *)
    rVoted_InfluentPH                   : REAL;                 (* Validated 2oo3 Influent pH [pH] *)
    rVoted_ToxicSpike_ppm               : REAL;                 (* Validated 2oo3 Influent Toxic Spill [ppm] *)

    (* Cyber-Physical Observer Output Estimates *)
    rObs_NitrificationRate_rNH4_g_m3_h  : REAL;                 (* ASM2d Nitrification Rate r_NH4 [g N/(m3*h)] *)
    rObs_DenitrificationRate_rNO3_g_m3_h: REAL;                 (* ASM2d Denitrification Rate r_NO3 [g N/(m3*h)] *)
    rObs_BioP_UptakeRate_rPO4_g_m3_h    : REAL;                 (* ASM2d Biological Phosphorus Luxury Uptake [g P/(m3*h)] *)
    rObs_DynamicAlphaFactor             : REAL;                 (* Real-Time Ceramic Diffuser Dynamic Alpha Factor *)
    rObs_DiffuserCleanlinessDeltaP_kPa  : REAL;                 (* Ceramic Diffuser Fouling Delta-P Resistance [kPa] *)
    rObs_OxygenTransferRate_OTR_kg_h    : REAL;                 (* Dynamic Basin Oxygen Transfer Rate [kg O2/h] *)
    rObs_KLa_Coefficient_per_h          : REAL;                 (* Overall Oxygen Transfer Coefficient KLa [1/h] *)
    rObs_SludgeSettlingVelocity_vs_m_h  : REAL;                 (* Vesilind Dynamic Sludge Settling Velocity [m/h] *)
    rObs_ClarifierLimitingSolidsFlux    : REAL;                 (* Clarifier Limiting Solids Flux [kg/(m2*h)] *)
    rObs_ClarifierWashoutRiskIndex      : REAL;                 (* Clarifier Hydraulic Washout Vulnerability Index [0..2] *)
    rObs_MBR_CakeResistance_Rc_per_m    : REAL;                 (* Darcy Dynamic Cake Layer Resistance Rc [1/m] *)
    rObs_MBR_PoreResistance_Rp_per_m    : REAL;                 (* Darcy Irreversible Pore Constriction Resistance Rp [1/m] *)
    rObs_MBR_TotalHydraulicResistance   : REAL;                 (* Total MBR Hydraulic Filtration Resistance R_tot [1/m] *)
    rMPC_CurrentCostFunctional_J        : REAL;                 (* Instantaneous MPC Objective Quadratic Cost J *)
    iActiveFSMState                     : INT;                  (* Current Operational State Machine Step [0..11] *)
    rStateDwellTime_s                   : REAL;                 (* Monotonic Time Elapsed in Active State [s] *)
    rCurrentDailyTreatedVolume_m3       : REAL;                 (* Cumulative Daily Wastewater Treated [m3] *)
    rCurrentDailyBlowerEnergy_kWh       : REAL;                 (* Cumulative Blower Electrical Power Consumed [kWh] *)
    rPlantEnergySpecific_kWh_per_m3     : REAL;                 (* Specific Aeration Energy Intensity [kWh/m3] *)

    (* =========================================================================================== *)
    (* 4.0 ISA-18.2 DIAGNOSTIC STATUS WORDS                                                        *)
    (* =========================================================================================== *)
    wDiagnosticWord01_Sensors           : WORD;                 (* Word 01: 2oo3 TMR Transducers Health & Skew Flags *)
    wDiagnosticWord02_Actuators         : WORD;                 (* Word 02: Blowers, VFD Pumps, Gates & Dosing Alarms *)
    wDiagnosticWord03_Quality           : WORD;                 (* Word 03: Effluent Nutrient Violations & MBR Fouling *)
    wDiagnosticWord04_SafetyFSM         : WORD;                 (* Word 04: Active FSM Phase, Surge & Toxic Trips *)
END_VAR""")

    # 4. VAR internal declarations
    parts.append("""VAR
    (* =========================================================================================== *)
    (* 1.0 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) REGISTERS, DISCREPANCY TIMERS & TOLERANCES        *)
    (* =========================================================================================== *)
    (* Discrepancy Debounce Timers [s] *)
    rTimer_Disc_NH4                     : REAL := 0.0;
    rTimer_Disc_COD                     : REAL := 0.0;
    rTimer_Disc_InfFlow                 : REAL := 0.0;
    rTimer_Disc_DO                      : REAL := 0.0;
    rTimer_Disc_NO3                     : REAL := 0.0;
    rTimer_Disc_HeaderPres              : REAL := 0.0;
    rTimer_Disc_AirFlow                 : REAL := 0.0;
    rTimer_Disc_ORP                     : REAL := 0.0;
    rTimer_Disc_IRFlow                  : REAL := 0.0;
    rTimer_Disc_CarbonDose              : REAL := 0.0;
    rTimer_Disc_PO4                     : REAL := 0.0;
    rTimer_Disc_FeCl3                   : REAL := 0.0;
    rTimer_Disc_SuctionPres             : REAL := 0.0;
    rTimer_Disc_TMP                     : REAL := 0.0;
    rTimer_Disc_Blanket                 : REAL := 0.0;
    rTimer_Disc_RASFlow                 : REAL := 0.0;
    rTimer_Disc_WaterTemp               : REAL := 0.0;
    rTimer_Disc_PH                      : REAL := 0.0;
    rTimer_Disc_Toxic                   : REAL := 0.0;
    rTimer_Disc_StormLvl                : REAL := 0.0;

    (* Channel Health & Fault Latches *)
    bFault_NH4_A, bFault_NH4_B, bFault_NH4_C : BOOL := FALSE;
    bFault_COD_A, bFault_COD_B, bFault_COD_C : BOOL := FALSE;
    bFault_InfFlow_A, bFault_InfFlow_B, bFault_InfFlow_C : BOOL := FALSE;
    bFault_DO_A, bFault_DO_B, bFault_DO_C : BOOL := FALSE;
    bFault_NO3_A, bFault_NO3_B, bFault_NO3_C : BOOL := FALSE;
    bFault_HeaderPres_A, bFault_HeaderPres_B, bFault_HeaderPres_C : BOOL := FALSE;
    bFault_AirFlow_A, bFault_AirFlow_B, bFault_AirFlow_C : BOOL := FALSE;
    bFault_ORP_A, bFault_ORP_B, bFault_ORP_C : BOOL := FALSE;
    bFault_IRFlow_A, bFault_IRFlow_B, bFault_IRFlow_C : BOOL := FALSE;
    bFault_Carbon_A, bFault_Carbon_B, bFault_Carbon_C : BOOL := FALSE;
    bFault_PO4_A, bFault_PO4_B, bFault_PO4_C : BOOL := FALSE;
    bFault_FeCl3_A, bFault_FeCl3_B, bFault_FeCl3_C : BOOL := FALSE;
    bFault_Suction_A, bFault_Suction_B, bFault_Suction_C : BOOL := FALSE;
    bFault_TMP_A, bFault_TMP_B, bFault_TMP_C : BOOL := FALSE;
    bFault_Blanket_A, bFault_Blanket_B, bFault_Blanket_C : BOOL := FALSE;
    bFault_RASFlow_A, bFault_RASFlow_B, bFault_RASFlow_C : BOOL := FALSE;
    bFault_Temp_A, bFault_Temp_B, bFault_Temp_C : BOOL := FALSE;
    bFault_PH_A, bFault_PH_B, bFault_PH_C : BOOL := FALSE;
    bFault_Toxic_A, bFault_Toxic_B, bFault_Toxic_C : BOOL := FALSE;
    bFault_Storm_A, bFault_Storm_B, bFault_Storm_C : BOOL := FALSE;

    (* Triplet Discrepancy Tolerances *)
    c_Tol_NH4_mg_L                      : REAL := 2.50;         (* Ammonia Tolerance: 2.5 mg/L *)
    c_Tol_COD_mg_L                      : REAL := 35.0;         (* COD Tolerance: 35.0 mg/L *)
    c_Tol_InfFlow_m3_h                  : REAL := 450.0;        (* Influent Flow Tolerance: 450 m3/h *)
    c_Tol_DO_mg_L                       : REAL := 0.25;         (* DO Tolerance: 0.25 mg/L *)
    c_Tol_NO3_mg_L                      : REAL := 1.20;         (* Nitrate Tolerance: 1.2 mg/L *)
    c_Tol_HeaderPres_kPa                : REAL := 3.50;         (* Header Pressure Tolerance: 3.5 kPa *)
    c_Tol_AirFlow_Nm3_h                 : REAL := 2500.0;       (* Blower Air Flow Tolerance: 2500 Nm3/h *)
    c_Tol_ORP_mV                        : REAL := 25.0;         (* Anoxic ORP Tolerance: 25 mV *)
    c_Tol_IRFlow_m3_h                   : REAL := 1200.0;       (* Internal Recycle Tolerance: 1200 m3/h *)
    c_Tol_Carbon_Lph                    : REAL := 8.00;         (* Carbon Dosing Tolerance: 8.0 L/h *)
    c_Tol_PO4_mg_L                      : REAL := 0.040;        (* Orthophosphate Tolerance: 0.04 mg/L *)
    c_Tol_FeCl3_Lph                     : REAL := 5.00;         (* FeCl3 Dosing Tolerance: 5.0 L/h *)
    c_Tol_Suction_kPa                   : REAL := 2.50;         (* Suction Pressure Tolerance: 2.5 kPa *)
    c_Tol_TMP_kPa                       : REAL := 2.50;         (* Transmembrane Pressure Tolerance: 2.5 kPa *)
    c_Tol_Blanket_m                     : REAL := 0.20;         (* Clarifier Blanket Tolerance: 0.20 m *)
    c_Tol_RASFlow_m3_h                  : REAL := 350.0;        (* RAS Flow Tolerance: 350 m3/h *)
    c_Tol_Temp_degC                     : REAL := 1.00;         (* Temperature Tolerance: 1.0 deg C *)
    c_Tol_PH                            : REAL := 0.25;         (* pH Tolerance: 0.25 pH *)
    c_Tol_Toxic_ppm                     : REAL := 0.05;         (* Toxic Spill Tolerance: 0.05 ppm *)
    c_Tol_StormLvl_m                    : REAL := 0.15;         (* Storm Basin Level Tolerance: 0.15 m *)
    c_DebounceLimit_s                   : REAL := 0.500;        (* Discrepancy Debounce Filter Time [s] *)

    (* =========================================================================================== *)
    (* 2.0 8x8 DISCRETE STATE-SPACE MATRICES & KALMAN OBSERVER REGISTERS (Ts = 0.100 s)            *)
    (* =========================================================================================== *)
    (* State Vector x: [1: DO, 2: NH4, 3: NO3, 4: PO4, 5: TMP, 6: SBH, 7: P_header, 8: Effluent_TN] *)
    mat_A                               : ARRAY[1..8, 1..8] OF REAL; (* Discrete System Matrix A *)
    mat_B                               : ARRAY[1..8, 1..8] OF REAL; (* Discrete Input Coupling Matrix B *)
    mat_C                               : ARRAY[1..8, 1..8] OF REAL; (* Measurement Output Direct Matrix C *)
    mat_D                               : ARRAY[1..8, 1..8] OF REAL; (* Direct Feedforward Matrix D *)
    mat_Ke                              : ARRAY[1..8, 1..8] OF REAL; (* Discrete Steady-State Kalman Observer Gain *)

    x_state                             : ARRAY[1..8] OF REAL;       (* Filtered Dynamic State Vector x[k] *)
    x_pred                              : ARRAY[1..8] OF REAL;       (* Prior State Estimate x[k+1|k] *)
    x_obs                               : ARRAY[1..8] OF REAL;       (* Innovation Updated State Estimate *)
    y_meas                              : ARRAY[1..8] OF REAL;       (* Measured Physical Process Output y[k] *)
    y_pred                              : ARRAY[1..8] OF REAL;       (* Output Prediction y[k|k-1] *)
    e_innov                             : ARRAY[1..8] OF REAL;       (* Innovation Residual Vector *)
    r_ref                               : ARRAY[1..8] OF REAL;       (* Reference Setpoint Target Vector r[k] *)
    u_act                               : ARRAY[1..8] OF REAL;       (* Active Actuator Control Vector u[k] *)
    u_prev                              : ARRAY[1..8] OF REAL;       (* Previous Scan Actuator Command u[k-1] *)
    du_delta                            : ARRAY[1..8] OF REAL;       (* Actuator Slew Rate Increment du *)

    (* =========================================================================================== *)
    (* 3.0 MODEL PREDICTIVE CONTROL (MPC) MATRICES & RECEDING-HORIZON PREDICTION ARRAYS            *)
    (* =========================================================================================== *)
    mat_Q                               : ARRAY[1..8, 1..8] OF REAL; (* State Error Penalty Matrix Q (Diagonal) *)
    mat_R                               : ARRAY[1..8, 1..8] OF REAL; (* Actuator Effort Penalty Matrix R (Diagonal) *)
    mat_S                               : ARRAY[1..8, 1..8] OF REAL; (* Actuator Slew Rate Penalty Matrix S (Diagonal) *)
    mat_P                               : ARRAY[1..8, 1..8] OF REAL; (* Terminal State Cost Matrix P (Diagonal) *)

    x_horizon                           : ARRAY[1..4, 1..8] OF REAL; (* State Prediction across Horizon Np=3 *)
    u_horizon                           : ARRAY[1..3, 1..8] OF REAL; (* Actuator Actions across Horizon Nc=3 *)
    grad_u                              : ARRAY[1..8] OF REAL;       (* Projected Objective Gradient Vector *)
    u_min                               : ARRAY[1..8] OF REAL;       (* Actuator Lower Physical Saturation *)
    u_max                               : ARRAY[1..8] OF REAL;       (* Actuator Upper Physical Saturation *)
    du_max                              : ARRAY[1..8] OF REAL;       (* Maximum Permissible Actuator Slew Rate *)
    rMPC_StepSize                       : REAL := 0.042;             (* Gradient Descent Convergence Step Size *)

    (* =========================================================================================== *)
    (* 4.0 CYBER-PHYSICAL BIOKINETIC, HYDRAULIC & MEMBRANE OBSERVER PARAMETERS                     *)
    (* =========================================================================================== *)
    (* ASM2d Biokinetic Constants *)
    c_rMu_AUT                           : REAL := 0.95;         (* Maximum Autotrophic Nitrifier Growth Rate [1/d] *)
    c_rK_NH4                            : REAL := 0.50;         (* Ammonia Half-Saturation Constant [mg/L N] *)
    c_rK_O_AUT                          : REAL := 0.40;         (* Autotrophic Oxygen Affinity Constant [mg/L O2] *)
    c_rTheta_N                          : REAL := 1.072;        (* Nitrification Arrhenius Temp Correction Coeff *)
    c_rX_AUT                            : REAL := 220.0;        (* Autotrophic Biomass Concentration [mg/L] *)
    c_rMu_HET                           : REAL := 4.00;         (* Heterotrophic Denitrifier Max Growth Rate [1/d] *)
    c_rEta_g                            : REAL := 0.80;         (* Anoxic Denitrification Reduction Factor *)
    c_rK_NO3                            : REAL := 0.50;         (* Nitrate Half-Saturation Constant [mg/L N] *)
    c_rK_S                              : REAL := 20.0;         (* Readily Biodegradable COD Half-Saturation [mg/L] *)
    c_rK_O_denit                        : REAL := 0.20;         (* DO Inhibition Constant for Denitrification [mg/L] *)
    c_rTheta_D                          : REAL := 1.040;        (* Denitrification Arrhenius Temperature Coeff *)
    c_rX_HET                            : REAL := 4800.0;       (* Heterotrophic Active Biomass [mg/L] *)
    c_rq_PP                             : REAL := 1.50;         (* Polyphosphate Luxury Storage Rate [g P/(g X*d)] *)
    c_rK_PO4                            : REAL := 0.20;         (* Phosphate Half-Saturation Constant [mg/L P] *)
    c_rK_O_PAO                          : REAL := 0.20;         (* PAO Oxygen Half-Saturation Constant [mg/L O2] *)
    c_rBeta_Fe_stoich                   : REAL := 1.65;         (* Molar Over-Stoichiometric Dosing Ratio (Fe:P) *)
    c_rFe_MolecularWeight               : REAL := 55.845;       (* Iron Atomic Weight [g/mol] *)
    c_rP_MolecularWeight                : REAL := 30.974;       (* Phosphorus Atomic Weight [g/mol] *)

    (* Dynamic Oxygen Transfer & Diffuser Fouling Observer Variables *)
    rC_star_DO_sat                      : REAL := 9.08;         (* Clean Water Saturated DO Concentration [mg/L] *)
    rAlpha_0                            : REAL := 0.65;         (* Baseline Clean Ceramic Diffuser Alpha Factor *)
    rBeta_Salinity                      : REAL := 0.95;         (* Wastewater Salinity Correction Factor *)
    rSurfactantSuppressionRatio         : REAL := 0.0;          (* Surfactant Induced OTR Suppression Ratio *)
    rDiffuserFoulingCoeff               : REAL := 0.0;          (* Ceramic Diffuser Biofilm & Scaling Resistance *)
    rDiffuserCleanCurve_c0              : REAL := 62.5;         (* Clean Diffuser Dynamic Base Pressure [kPa] *)
    rDiffuserCleanCurve_c1              : REAL := 0.00012;      (* Linear Air Velocity Friction Term [kPa/(Nm3/h)] *)
    rDiffuserCleanCurve_c2              : REAL := 1.45E-9;      (* Quadratic Diffuser Orifice Loss Term *)
    rStaticHydrostaticHead_kPa          : REAL := 63.76;        (* Water Depth Static Head (rho*g*h/1000) [kPa] *)

    (* Vesilind Dynamic Sludge Settling Flux & Clarifier SBH Observer *)
    c_rVesilind_v0                      : REAL := 9.50;         (* Vesilind Initial Settling Velocity [m/h] *)
    c_rVesilind_rv                      : REAL := 0.380;        (* Vesilind Settling Parameter [m3/kg] *)
    rClarifierUnderflowVelocity_m_h     : REAL := 0.0;          (* Downward Hydraulic Underflow Velocity [m/h] *)
    rGravitySolidsFlux_kg_m2_h          : REAL := 0.0;          (* Sludge Gravitational Settling Flux [kg/(m2*h)] *)
    rUnderflowSolidsFlux_kg_m2_h        : REAL := 0.0;          (* Sludge Bulk Underflow Suction Flux [kg/(m2*h)] *)
    rTotalSolidsFlux_kg_m2_h            : REAL := 0.0;          (* Total Clarifier Downward Solids Flux [kg/(m2*h)] *)
    rClarifierInfluentSolids_kg_h       : REAL := 0.0;          (* Clarifier Ingress Solids Mass Flow [kg/h] *)
    rClarifierRAS_Solids_kg_h           : REAL := 0.0;          (* RAS Withdrawal Solids Mass Flow [kg/h] *)
    rClarifierBlanketDensity_kg_m3      : REAL := 9.80;         (* Sludge Blanket Compacted Density [kg/m3] *)

    (* Submerged Hollow-Fiber MBR Resistance-In-Series Variables *)
    c_rMembraneIntrinsic_Rm             : REAL := 1.25E12;      (* Clean Membrane Polymeric Resistance Rm [1/m] *)
    c_rCakeAccumulationCoeff            : REAL := 4.80E10;      (* Specific Cake Layer Deposition Coefficient *)
    c_rAirScourCleaningEfficiency       : REAL := 0.035;        (* Bubble Scour Shear Cake Stripping Coeff *)
    c_rPoreFoulingRate_kp               : REAL := 1.80E7;       (* Irreversible Internal Pore Adsorption Rate *)
    rInstantaneousWaterViscosity_Pa_s   : REAL := 0.00105;      (* Water Dynamic Viscosity at Basin Temp [Pa*s] *)
    rPermeateFlux_LMH                   : REAL := 22.5;         (* Instantaneous Permeate Flux [L/(m2*h)] *)
    rPermeateFlux_m_s                   : REAL := 6.25E-6;      (* Instantaneous Permeate Flux [m/s] *)
    rCakeResistance_Rc                  : REAL := 0.85E12;      (* Dynamic Cake Layer Resistance [1/m] *)
    rPoreResistance_Rp                  : REAL := 0.40E12;      (* Irreversible Adsorbed Pore Resistance [1/m] *)

    (* =========================================================================================== *)
    (* 5.0 ISA-18.2 ALARM TRIP THRESHOLDS, DEADBANDS & STATUS REGISTERS                            *)
    (* =========================================================================================== *)
    c_DO_Trip_LL                        : REAL := 0.50;         (* Fast DO Depletion Critical Trip [mg/L O2] *)
    c_DO_Warning_L                      : REAL := 1.20;         (* Low DO Pre-Alarm Warning [mg/L O2] *)
    c_DO_Warning_H                      : REAL := 3.50;         (* Excessive Aeration Energy Waste High [mg/L O2] *)
    c_DO_Trip_HH                        : REAL := 5.00;         (* Aeration Basin High-High DO Trip [mg/L O2] *)
    c_NH4_Warning_H                     : REAL := 2.50;         (* Effluent Ammonia Breakthrough Warning [mg/L N] *)
    c_NH4_Trip_HH                       : REAL := 6.00;         (* Ammonia Acute Toxic Discharge Trip [mg/L N] *)
    c_NO3_Warning_H                     : REAL := 8.50;         (* Denitrification Deficiency Warning [mg/L N] *)
    c_NO3_Trip_HH                       : REAL := 12.0;         (* Total Nitrogen Acute Violation Trip [mg/L N] *)
    c_PO4_Warning_H                     : REAL := 0.18;         (* Effluent Orthophosphate Approach Warning [mg/L P] *)
    c_PO4_Trip_HH                       : REAL := 0.25;         (* Regulatory TP Discharge Breach Trip [mg/L P] *)
    c_TMP_Warning_H                     : REAL := 32.0;         (* MBR Cake Layer Heavy Fouling Warning [kPa] *)
    c_TMP_Trip_HH                       : REAL := 45.0;         (* MBR Permeate Pump Cavitation & Trip [kPa] *)
    c_Blanket_Warning_H                 : REAL := 2.20;         (* Secondary Clarifier Rising Blanket Warning [m] *)
    c_Blanket_Trip_HH                   : REAL := 3.20;         (* Imminent Sludge Washout Emergency Trip [m] *)
    c_Toxic_Trip_HH                     : REAL := 0.50;         (* Influent Cyanide & Heavy Metals Diversion Trip [ppm] *)
    c_BlowerSurgeRatio_Min              : REAL := 1.15;         (* Blower Operating Point Surge Margin Ratio *)

    (* Alarm Deadband Hysteresis Tolerances *)
    rDeadband_DO                        : REAL := 0.05;         (* DO Deadband [mg/L] *)
    rDeadband_Nutrient                  : REAL := 0.10;         (* Nitrogen/Phosphate Deadband [mg/L] *)
    rDeadband_Pressure                  : REAL := 0.50;         (* Pressure Deadband [kPa] *)
    rDeadband_Blanket                   : REAL := 0.05;         (* Blanket Level Deadband [m] *)

    (* Latched Alarm Flags *)
    bAlarm_DO_Depletion_LL              : BOOL := FALSE;
    bAlarm_DO_Low_L                     : BOOL := FALSE;
    bAlarm_DO_High_H                    : BOOL := FALSE;
    bAlarm_DO_HighHigh_HH               : BOOL := FALSE;
    bAlarm_Ammonia_High_H               : BOOL := FALSE;
    bAlarm_Ammonia_HighHigh_HH          : BOOL := FALSE;
    bAlarm_Nitrate_High_H               : BOOL := FALSE;
    bAlarm_Nitrate_HighHigh_HH          : BOOL := FALSE;
    bAlarm_EffluentPO4_High_H           : BOOL := FALSE;
    bAlarm_EffluentPO4_HighHigh_HH      : BOOL := FALSE;
    bAlarm_MBR_TMP_High_H               : BOOL := FALSE;
    bAlarm_MBR_TMP_HighHigh_HH          : BOOL := FALSE;
    bAlarm_SludgeBlanket_High_H         : BOOL := FALSE;
    bAlarm_SludgeBlanket_Washout_HH     : BOOL := FALSE;
    bAlarm_BlowerSurge_Risk_HH          : BOOL := FALSE;
    bAlarm_ToxicSpill_Ingress_HH        : BOOL := FALSE;
    bAlarm_StormSurge_Active            : BOOL := FALSE;
    bAlarm_DiffuserFouling_Warning      : BOOL := FALSE;

    (* =========================================================================================== *)
    (* 6.0 12-STAGE FINITE STATE MACHINE (FSM) SEQUENCING & CYCLIC TIMERS                          *)
    (* =========================================================================================== *)
    eCurrentState                       : INT := 0;             (* Active FSM State Code [0..11] *)
    ePrevState                          : INT := 0;             (* Previous Scan FSM State Code *)
    rStateTimer_s                       : REAL := 0.0;          (* In-State Monotonic Real-Time Timer [s] *)
    rMBR_HarvestTimer_s                 : REAL := 0.0;          (* MBR Permeate Production Sub-Timer [s] *)
    rMBR_RelaxationTimer_s              : REAL := 0.0;          (* MBR Relaxation Scour Sub-Timer [s] *)
    rMBR_CIP_StageTimer_s               : REAL := 0.0;          (* Hypochlorite CIP Maintenance Sub-Timer [s] *)
    rStormDiversionTimer_s              : REAL := 0.0;          (* Wet-Weather Diversion Gate Open Timer [s] *)
    rDiffuserBumpTimer_s                : REAL := 0.0;          (* High-Pressure Air Diffuser Bump Timer [s] *)

    (* MBR Cyclic Pacing Limits *)
    c_rMBR_HarvestDuration_s            : REAL := 540.0;        (* 9.0 Minutes Continuous Permeate Harvest [s] *)
    c_rMBR_RelaxationDuration_s         : REAL := 60.0;         (* 1.0 Minute Air-Scour Relaxation Pulse [s] *)
    c_rMBR_CIP_Duration_s               : REAL := 1800.0;       (* 30.0 Minutes Clean-In-Place Duration [s] *)

    (* Matrix & Loop Iterator Scratchpad *)
    bInitialized                        : BOOL := FALSE;        (* First-Scan Static Matrix Initializer Flag *)
    iRow, iCol, iIdx, jIdx, kStep       : INT := 1;             (* General Loop Indices *)
    rTempAccum                          : REAL := 0.0;          (* General Scratchpad Real Accumulator *)
    rTempVar1                           : REAL := 0.0;          (* Temporary Calculation Register 1 *)
    rTempVar2                           : REAL := 0.0;          (* Temporary Calculation Register 2 *)
    rTempVar3                           : REAL := 0.0;          (* Temporary Calculation Register 3 *)
END_VAR""")

    # 5. PHASE 0: FIRST-SCAN MATRIX & PARAMETER INITIALIZATION
    parts.append("""(* ==================================================================================================== *)
(* PHASE 0: FIRST-SCAN MATRIX & CYBER-PHYSICAL MODEL INITIALIZATION                                     *)
(* ==================================================================================================== *)
IF NOT bInitialized THEN
    (* Discrete State Transition Matrix A (8x8) at Ts = 0.100 s *)
    (* States: 1:DO, 2:NH4, 3:NO3, 4:PO4, 5:TMP, 6:SBH, 7:P_header, 8:TN *)
    mat_A[1,1] := 0.9650; mat_A[1,2] := -0.0120; mat_A[1,3] :=  0.0000; mat_A[1,4] :=  0.0000; mat_A[1,5] :=  0.0000; mat_A[1,6] :=  0.0000; mat_A[1,7] :=  0.0045; mat_A[1,8] :=  0.0000;
    mat_A[2,1] := -0.0185; mat_A[2,2] :=  0.9780; mat_A[2,3] :=  0.0000; mat_A[2,4] :=  0.0000; mat_A[2,5] :=  0.0000; mat_A[2,6] :=  0.0000; mat_A[2,7] :=  0.0000; mat_A[2,8] :=  0.0150;
    mat_A[3,1] :=  0.0125; mat_A[3,2] :=  0.0145; mat_A[3,3] :=  0.9720; mat_A[3,4] :=  0.0000; mat_A[3,5] :=  0.0000; mat_A[3,6] :=  0.0000; mat_A[3,7] :=  0.0000; mat_A[3,8] :=  0.0220;
    mat_A[4,1] := -0.0085; mat_A[4,2] :=  0.0000; mat_A[4,3] :=  0.0000; mat_A[4,4] :=  0.9810; mat_A[4,5] :=  0.0000; mat_A[4,6] :=  0.0000; mat_A[4,7] :=  0.0000; mat_A[4,8] :=  0.0000;
    mat_A[5,1] :=  0.0000; mat_A[5,2] :=  0.0000; mat_A[5,3] :=  0.0000; mat_A[4,4] :=  0.0000; mat_A[5,5] :=  0.9880; mat_A[5,6] :=  0.0000; mat_A[5,7] :=  0.0000; mat_A[5,8] :=  0.0000;
    mat_A[6,1] :=  0.0000; mat_A[6,2] :=  0.0000; mat_A[6,3] :=  0.0000; mat_A[6,4] :=  0.0000; mat_A[6,5] :=  0.0000; mat_A[6,6] :=  0.9840; mat_A[6,7] :=  0.0000; mat_A[6,8] :=  0.0000;
    mat_A[7,1] :=  0.0000; mat_A[7,2] :=  0.0000; mat_A[7,3] :=  0.0000; mat_A[7,4] :=  0.0000; mat_A[7,5] :=  0.0000; mat_A[7,6] :=  0.0000; mat_A[7,7] :=  0.9420; mat_A[7,8] :=  0.0000;
    mat_A[8,1] := -0.0050; mat_A[8,2] :=  0.0180; mat_A[8,3] :=  0.0240; mat_A[8,4] :=  0.0000; mat_A[8,5] :=  0.0000; mat_A[8,6] :=  0.0000; mat_A[8,7] :=  0.0000; mat_A[8,8] :=  0.9890;

    (* Discrete Input Coupling Matrix B (8x8) at Ts = 0.100 s *)
    (* Inputs: 1:Blower, 2:IR_pump, 3:Carbon, 4:FeCl3, 5:Permeate, 6:RAS, 7:AirScour, 8:StormGate *)
    mat_B[1,1] :=  0.0385; mat_B[1,2] :=  0.0000; mat_B[1,3] :=  0.0000; mat_B[1,4] :=  0.0000; mat_B[1,5] :=  0.0000; mat_B[1,6] :=  0.0000; mat_B[1,7] :=  0.0012; mat_B[1,8] :=  0.0000;
    mat_B[2,1] := -0.0120; mat_B[2,2] := -0.0045; mat_B[2,3] :=  0.0000; mat_B[2,4] :=  0.0000; mat_B[2,5] :=  0.0000; mat_B[2,6] := -0.0020; mat_B[2,7] :=  0.0000; mat_B[2,8] :=  0.0015;
    mat_B[3,1] :=  0.0085; mat_B[3,2] := -0.0210; mat_B[3,3] := -0.0345; mat_B[3,4] :=  0.0000; mat_B[3,5] :=  0.0000; mat_B[3,6] := -0.0035; mat_B[3,7] :=  0.0000; mat_B[3,8] :=  0.0000;
    mat_B[4,1] := -0.0040; mat_B[4,2] :=  0.0000; mat_B[4,3] :=  0.0000; mat_B[4,4] := -0.0420; mat_B[4,5] :=  0.0000; mat_B[4,6] := -0.0015; mat_B[4,7] :=  0.0000; mat_B[4,8] :=  0.0000;
    mat_B[5,1] :=  0.0000; mat_B[5,2] :=  0.0000; mat_B[5,3] :=  0.0000; mat_B[5,4] :=  0.0000; mat_B[5,5] :=  0.0265; mat_B[5,6] :=  0.0000; mat_B[5,7] := -0.0145; mat_B[5,8] :=  0.0000;
    mat_B[6,1] :=  0.0000; mat_B[6,2] :=  0.0000; mat_B[6,3] :=  0.0000; mat_B[6,4] :=  0.0000; mat_B[6,5] :=  0.0000; mat_B[6,6] := -0.0310; mat_B[6,7] :=  0.0000; mat_B[6,8] := -0.0180;
    mat_B[7,1] :=  0.0520; mat_B[7,2] :=  0.0000; mat_B[7,3] :=  0.0000; mat_B[7,4] :=  0.0000; mat_B[7,5] :=  0.0000; mat_B[7,6] :=  0.0000; mat_B[7,7] :=  0.0000; mat_B[7,8] :=  0.0000;
    mat_B[8,1] := -0.0080; mat_B[8,2] := -0.0185; mat_B[8,3] := -0.0290; mat_B[8,4] :=  0.0000; mat_B[8,5] :=  0.0000; mat_B[8,6] := -0.0050; mat_B[8,7] :=  0.0000; mat_B[8,8] :=  0.0025;

    (* Measurement Direct Observation Matrix C (8x8) *)
    FOR iRow := 1 TO 8 DO
        FOR iCol := 1 TO 8 DO
            IF iRow = iCol THEN
                mat_C[iRow, iCol] := 1.0;
                mat_D[iRow, iCol] := 0.0;
            ELSE
                mat_C[iRow, iCol] := 0.0;
                mat_D[iRow, iCol] := 0.0;
            END_IF;
        END_FOR;
    END_FOR;

    (* Discrete Steady-State Kalman Observer Gain Matrix Ke (8x8) *)
    mat_Ke[1,1] := 0.3150; mat_Ke[1,2] := 0.0085; mat_Ke[1,3] := 0.0000; mat_Ke[1,4] := 0.0000; mat_Ke[1,5] := 0.0000; mat_Ke[1,6] := 0.0000; mat_Ke[1,7] := 0.0240; mat_Ke[1,8] := 0.0000;
    mat_Ke[2,1] := 0.0120; mat_Ke[2,2] := 0.3420; mat_Ke[2,3] := 0.0110; mat_Ke[2,4] := 0.0000; mat_Ke[2,5] := 0.0000; mat_Ke[2,6] := 0.0000; mat_Ke[2,7] := 0.0000; mat_Ke[2,8] := 0.0180;
    mat_Ke[3,1] := 0.0080; mat_Ke[3,2] := 0.0140; mat_Ke[3,3] := 0.3280; mat_Ke[3,4] := 0.0000; mat_Ke[3,5] := 0.0000; mat_Ke[3,6] := 0.0000; mat_Ke[3,7] := 0.0000; mat_Ke[3,8] := 0.0240;
    mat_Ke[4,1] := 0.0040; mat_Ke[4,2] := 0.0000; mat_Ke[4,3] := 0.0000; mat_Ke[4,4] := 0.3650; mat_Ke[4,5] := 0.0000; mat_Ke[4,6] := 0.0000; mat_Ke[4,7] := 0.0000; mat_Ke[4,8] := 0.0000;
    mat_Ke[5,1] := 0.0000; mat_Ke[5,2] := 0.0000; mat_Ke[5,3] := 0.0000; mat_Ke[5,4] := 0.0000; mat_Ke[5,5] := 0.3850; mat_Ke[5,6] := 0.0000; mat_Ke[5,7] := 0.0000; mat_Ke[5,8] := 0.0000;
    mat_Ke[6,1] := 0.0000; mat_Ke[6,2] := 0.0000; mat_Ke[6,3] := 0.0000; mat_Ke[6,4] := 0.0000; mat_Ke[6,5] := 0.0000; mat_Ke[6,6] := 0.3540; mat_Ke[6,7] := 0.0000; mat_Ke[6,8] := 0.0000;
    mat_Ke[7,1] := 0.0180; mat_Ke[7,2] := 0.0000; mat_Ke[7,3] := 0.0000; mat_Ke[7,4] := 0.0000; mat_Ke[7,5] := 0.0000; mat_Ke[7,6] := 0.0000; mat_Ke[7,7] := 0.3920; mat_Ke[7,8] := 0.0000;
    mat_Ke[8,1] := 0.0050; mat_Ke[8,2] := 0.0160; mat_Ke[8,3] := 0.0210; mat_Ke[8,4] := 0.0000; mat_Ke[8,5] := 0.0000; mat_Ke[8,6] := 0.0000; mat_Ke[8,7] := 0.0000; mat_Ke[8,8] := 0.4100;

    (* Model Predictive Control (MPC) Cost Weighting Matrices *)
    FOR iRow := 1 TO 8 DO
        FOR iCol := 1 TO 8 DO
            mat_Q[iRow, iCol] := 0.0;
            mat_R[iRow, iCol] := 0.0;
            mat_S[iRow, iCol] := 0.0;
            mat_P[iRow, iCol] := 0.0;
        END_FOR;
    END_FOR;

    (* Q Matrix Diagonal (State Error Penalties) *)
    mat_Q[1,1] := 45.0;     (* DO Error Penalty *)
    mat_Q[2,2] := 80.0;     (* Ammonia Error Penalty (Strict EPA Limit) *)
    mat_Q[3,3] := 60.0;     (* Nitrate Error Penalty (Strict TN Limit) *)
    mat_Q[4,4] := 110.0;    (* Orthophosphate Error Penalty (TP < 0.2 mg/L) *)
    mat_Q[5,5] := 35.0;     (* MBR Transmembrane Pressure Penalty *)
    mat_Q[6,6] := 55.0;     (* Sludge Blanket Washout Risk Penalty *)
    mat_Q[7,7] := 12.0;     (* Aeration Header Static Pressure Deviation *)
    mat_Q[8,8] := 95.0;     (* Total Nitrogen Effluent Penalty *)

    (* R Matrix Diagonal (Actuator Energy Penalties - Energy Optimization) *)
    mat_R[1,1] := 2.20;     (* Blower VFD Electrical Energy Penalty (> 20% savings) *)
    mat_R[2,2] := 1.10;     (* Internal Recycle Pump Power *)
    mat_R[3,3] := 3.80;     (* External Carbon Chemical Reagent Cost *)
    mat_R[4,4] := 4.50;     (* FeCl3 Chemical Coagulant Reagent Cost *)
    mat_R[5,5] := 1.50;     (* Permeate Suction Pump Energy *)
    mat_R[6,6] := 0.90;     (* RAS Sludge Pump Power *)
    mat_R[7,7] := 1.80;     (* Air-Scour Blower Power *)
    mat_R[8,8] := 0.50;     (* Storm Diversion Gate Motion *)

    (* S Matrix Diagonal (Actuator Slew Rate Penalties) *)
    mat_S[1,1] := 5.0; mat_S[2,2] := 3.5; mat_S[3,3] := 6.0; mat_S[4,4] := 7.0;
    mat_S[5,5] := 4.0; mat_S[6,6] := 3.0; mat_S[7,7] := 4.5; mat_S[8,8] := 2.0;

    (* P Matrix Diagonal (Terminal State Cost) *)
    FOR iRow := 1 TO 8 DO
        mat_P[iRow, iRow] := mat_Q[iRow, iRow] * 2.5;
    END_FOR;

    (* Actuator Physical Saturation Bounds [u_min, u_max] *)
    u_min[1] := 25.0;  u_max[1] := 100.0; (* Blower Speed [%] Minimum 25% surge limit *)
    u_min[2] := 10.0;  u_max[2] := 100.0; (* IR Pump [%] *)
    u_min[3] := 0.0;   u_max[3] := 250.0; (* Carbon Source Dosing [L/h] *)
    u_min[4] := 0.0;   u_max[4] := 180.0; (* FeCl3 Coagulant Dosing [L/h] *)
    u_min[5] := 0.0;   u_max[5] := 100.0; (* MBR Permeate Pump [%] *)
    u_min[6] := 20.0;  u_max[6] := 100.0; (* RAS Sludge Pump [%] *)
    u_min[7] := 0.0;   u_max[7] := 100.0; (* MBR Air-Scour Blower [%] *)
    u_min[8] := 0.0;   u_max[8] := 100.0; (* Storm Gate Position [%] *)

    (* Maximum Permissible Slew Rate per Scan (du_max) *)
    du_max[1] := 1.50; (* Blower max 1.5% per 100 ms (15%/s ramp) *)
    du_max[2] := 2.00;
    du_max[3] := 5.00;
    du_max[4] := 4.00;
    du_max[5] := 2.50;
    du_max[6] := 2.00;
    du_max[7] := 5.00;
    du_max[8] := 1.00;

    bInitialized := TRUE;
END_IF;""")

    # 6. PHASE 1: 2oo3 TMR SENSOR VOTING
    # We will generate full voting logic for all 20 triplets
    phase1_code = """(* ==================================================================================================== *)
(* PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING & DISCREPANCY FAULT ISOLATION           *)
(* ==================================================================================================== *)

(* 1.1 Influent Ammonia Analyzers (AIT_INFLUENT_NH4_101A/B/C) *)
IF (ABS(AIT_INFLUENT_NH4_101A - AIT_INFLUENT_NH4_101B) <= c_Tol_NH4_mg_L) AND
   (ABS(AIT_INFLUENT_NH4_101B - AIT_INFLUENT_NH4_101C) <= c_Tol_NH4_mg_L) AND
   (ABS(AIT_INFLUENT_NH4_101C - AIT_INFLUENT_NH4_101A) <= c_Tol_NH4_mg_L) THEN
    rVoted_InfluentNH4_mg_L := (AIT_INFLUENT_NH4_101A + AIT_INFLUENT_NH4_101B + AIT_INFLUENT_NH4_101C) / 3.0;
    bFault_NH4_A := FALSE; bFault_NH4_B := FALSE; bFault_NH4_C := FALSE;
    rTimer_Disc_NH4 := 0.0;
ELSIF (ABS(AIT_INFLUENT_NH4_101A - AIT_INFLUENT_NH4_101B) <= c_Tol_NH4_mg_L) THEN
    rVoted_InfluentNH4_mg_L := (AIT_INFLUENT_NH4_101A + AIT_INFLUENT_NH4_101B) * 0.5;
    bFault_NH4_A := FALSE; bFault_NH4_B := FALSE; bFault_NH4_C := TRUE;
    rTimer_Disc_NH4 := rTimer_Disc_NH4 + rCycleTime_s;
ELSIF (ABS(AIT_INFLUENT_NH4_101A - AIT_INFLUENT_NH4_101C) <= c_Tol_NH4_mg_L) THEN
    rVoted_InfluentNH4_mg_L := (AIT_INFLUENT_NH4_101A + AIT_INFLUENT_NH4_101C) * 0.5;
    bFault_NH4_A := FALSE; bFault_NH4_B := TRUE; bFault_NH4_C := FALSE;
    rTimer_Disc_NH4 := rTimer_Disc_NH4 + rCycleTime_s;
ELSIF (ABS(AIT_INFLUENT_NH4_101B - AIT_INFLUENT_NH4_101C) <= c_Tol_NH4_mg_L) THEN
    rVoted_InfluentNH4_mg_L := (AIT_INFLUENT_NH4_101B + AIT_INFLUENT_NH4_101C) * 0.5;
    bFault_NH4_A := TRUE; bFault_NH4_B := FALSE; bFault_NH4_C := FALSE;
    rTimer_Disc_NH4 := rTimer_Disc_NH4 + rCycleTime_s;
ELSE
    bFault_NH4_A := TRUE; bFault_NH4_B := TRUE; bFault_NH4_C := TRUE;
    rTimer_Disc_NH4 := rTimer_Disc_NH4 + rCycleTime_s;
END_IF;

(* 1.2 Influent COD Analyzers (AIT_INFLUENT_COD_102A/B/C) *)
IF (ABS(AIT_INFLUENT_COD_102A - AIT_INFLUENT_COD_102B) <= c_Tol_COD_mg_L) AND
   (ABS(AIT_INFLUENT_COD_102B - AIT_INFLUENT_COD_102C) <= c_Tol_COD_mg_L) AND
   (ABS(AIT_INFLUENT_COD_102C - AIT_INFLUENT_COD_102A) <= c_Tol_COD_mg_L) THEN
    rVoted_InfluentCOD_mg_L := (AIT_INFLUENT_COD_102A + AIT_INFLUENT_COD_102B + AIT_INFLUENT_COD_102C) / 3.0;
    bFault_COD_A := FALSE; bFault_COD_B := FALSE; bFault_COD_C := FALSE;
    rTimer_Disc_COD := 0.0;
ELSIF (ABS(AIT_INFLUENT_COD_102A - AIT_INFLUENT_COD_102B) <= c_Tol_COD_mg_L) THEN
    rVoted_InfluentCOD_mg_L := (AIT_INFLUENT_COD_102A + AIT_INFLUENT_COD_102B) * 0.5;
    bFault_COD_A := FALSE; bFault_COD_B := FALSE; bFault_COD_C := TRUE;
    rTimer_Disc_COD := rTimer_Disc_COD + rCycleTime_s;
ELSIF (ABS(AIT_INFLUENT_COD_102A - AIT_INFLUENT_COD_102C) <= c_Tol_COD_mg_L) THEN
    rVoted_InfluentCOD_mg_L := (AIT_INFLUENT_COD_102A + AIT_INFLUENT_COD_102C) * 0.5;
    bFault_COD_A := FALSE; bFault_COD_B := TRUE; bFault_COD_C := FALSE;
    rTimer_Disc_COD := rTimer_Disc_COD + rCycleTime_s;
ELSIF (ABS(AIT_INFLUENT_COD_102B - AIT_INFLUENT_COD_102C) <= c_Tol_COD_mg_L) THEN
    rVoted_InfluentCOD_mg_L := (AIT_INFLUENT_COD_102B + AIT_INFLUENT_COD_102C) * 0.5;
    bFault_COD_A := TRUE; bFault_COD_B := FALSE; bFault_COD_C := FALSE;
    rTimer_Disc_COD := rTimer_Disc_COD + rCycleTime_s;
ELSE
    bFault_COD_A := TRUE; bFault_COD_B := TRUE; bFault_COD_C := TRUE;
    rTimer_Disc_COD := rTimer_Disc_COD + rCycleTime_s;
END_IF;

(* 1.3 Influent Flowmeters (FT_INFLUENT_FLOW_103A/B/C) *)
IF (ABS(FT_INFLUENT_FLOW_103A - FT_INFLUENT_FLOW_103B) <= c_Tol_InfFlow_m3_h) AND
   (ABS(FT_INFLUENT_FLOW_103B - FT_INFLUENT_FLOW_103C) <= c_Tol_InfFlow_m3_h) AND
   (ABS(FT_INFLUENT_FLOW_103C - FT_INFLUENT_FLOW_103A) <= c_Tol_InfFlow_m3_h) THEN
    rVoted_InfluentFlow_m3_h := (FT_INFLUENT_FLOW_103A + FT_INFLUENT_FLOW_103B + FT_INFLUENT_FLOW_103C) / 3.0;
    bFault_InfFlow_A := FALSE; bFault_InfFlow_B := FALSE; bFault_InfFlow_C := FALSE;
    rTimer_Disc_InfFlow := 0.0;
ELSIF (ABS(FT_INFLUENT_FLOW_103A - FT_INFLUENT_FLOW_103B) <= c_Tol_InfFlow_m3_h) THEN
    rVoted_InfluentFlow_m3_h := (FT_INFLUENT_FLOW_103A + FT_INFLUENT_FLOW_103B) * 0.5;
    bFault_InfFlow_A := FALSE; bFault_InfFlow_B := FALSE; bFault_InfFlow_C := TRUE;
    rTimer_Disc_InfFlow := rTimer_Disc_InfFlow + rCycleTime_s;
ELSIF (ABS(FT_INFLUENT_FLOW_103A - FT_INFLUENT_FLOW_103C) <= c_Tol_InfFlow_m3_h) THEN
    rVoted_InfluentFlow_m3_h := (FT_INFLUENT_FLOW_103A + FT_INFLUENT_FLOW_103C) * 0.5;
    bFault_InfFlow_A := FALSE; bFault_InfFlow_B := TRUE; bFault_InfFlow_C := FALSE;
    rTimer_Disc_InfFlow := rTimer_Disc_InfFlow + rCycleTime_s;
ELSIF (ABS(FT_INFLUENT_FLOW_103B - FT_INFLUENT_FLOW_103C) <= c_Tol_InfFlow_m3_h) THEN
    rVoted_InfluentFlow_m3_h := (FT_INFLUENT_FLOW_103B + FT_INFLUENT_FLOW_103C) * 0.5;
    bFault_InfFlow_A := TRUE; bFault_InfFlow_B := FALSE; bFault_InfFlow_C := FALSE;
    rTimer_Disc_InfFlow := rTimer_Disc_InfFlow + rCycleTime_s;
ELSE
    bFault_InfFlow_A := TRUE; bFault_InfFlow_B := TRUE; bFault_InfFlow_C := TRUE;
    rTimer_Disc_InfFlow := rTimer_Disc_InfFlow + rCycleTime_s;
END_IF;

(* 1.4 Aerobic Basin Optical DO Analyzers (AIT_AEROBIC_DO_201A/B/C) *)
IF (ABS(AIT_AEROBIC_DO_201A - AIT_AEROBIC_DO_201B) <= c_Tol_DO_mg_L) AND
   (ABS(AIT_AEROBIC_DO_201B - AIT_AEROBIC_DO_201C) <= c_Tol_DO_mg_L) AND
   (ABS(AIT_AEROBIC_DO_201C - AIT_AEROBIC_DO_201A) <= c_Tol_DO_mg_L) THEN
    rVoted_AerobicDO_mg_L := (AIT_AEROBIC_DO_201A + AIT_AEROBIC_DO_201B + AIT_AEROBIC_DO_201C) / 3.0;
    bFault_DO_A := FALSE; bFault_DO_B := FALSE; bFault_DO_C := FALSE;
    rTimer_Disc_DO := 0.0;
ELSIF (ABS(AIT_AEROBIC_DO_201A - AIT_AEROBIC_DO_201B) <= c_Tol_DO_mg_L) THEN
    rVoted_AerobicDO_mg_L := (AIT_AEROBIC_DO_201A + AIT_AEROBIC_DO_201B) * 0.5;
    bFault_DO_A := FALSE; bFault_DO_B := FALSE; bFault_DO_C := TRUE;
    rTimer_Disc_DO := rTimer_Disc_DO + rCycleTime_s;
ELSIF (ABS(AIT_AEROBIC_DO_201A - AIT_AEROBIC_DO_201C) <= c_Tol_DO_mg_L) THEN
    rVoted_AerobicDO_mg_L := (AIT_AEROBIC_DO_201A + AIT_AEROBIC_DO_201C) * 0.5;
    bFault_DO_A := FALSE; bFault_DO_B := TRUE; bFault_DO_C := FALSE;
    rTimer_Disc_DO := rTimer_Disc_DO + rCycleTime_s;
ELSIF (ABS(AIT_AEROBIC_DO_201B - AIT_AEROBIC_DO_201C) <= c_Tol_DO_mg_L) THEN
    rVoted_AerobicDO_mg_L := (AIT_AEROBIC_DO_201B + AIT_AEROBIC_DO_201C) * 0.5;
    bFault_DO_A := TRUE; bFault_DO_B := FALSE; bFault_DO_C := FALSE;
    rTimer_Disc_DO := rTimer_Disc_DO + rCycleTime_s;
ELSE
    bFault_DO_A := TRUE; bFault_DO_B := TRUE; bFault_DO_C := TRUE;
    rTimer_Disc_DO := rTimer_Disc_DO + rCycleTime_s;
END_IF;

(* 1.5 Aerobic Basin Nitrate Analyzers (AIT_AEROBIC_NO3_202A/B/C) *)
IF (ABS(AIT_AEROBIC_NO3_202A - AIT_AEROBIC_NO3_202B) <= c_Tol_NO3_mg_L) AND
   (ABS(AIT_AEROBIC_NO3_202B - AIT_AEROBIC_NO3_202C) <= c_Tol_NO3_mg_L) AND
   (ABS(AIT_AEROBIC_NO3_202C - AIT_AEROBIC_NO3_202A) <= c_Tol_NO3_mg_L) THEN
    rVoted_AerobicNO3_mg_L := (AIT_AEROBIC_NO3_202A + AIT_AEROBIC_NO3_202B + AIT_AEROBIC_NO3_202C) / 3.0;
    bFault_NO3_A := FALSE; bFault_NO3_B := FALSE; bFault_NO3_C := FALSE;
    rTimer_Disc_NO3 := 0.0;
ELSIF (ABS(AIT_AEROBIC_NO3_202A - AIT_AEROBIC_NO3_202B) <= c_Tol_NO3_mg_L) THEN
    rVoted_AerobicNO3_mg_L := (AIT_AEROBIC_NO3_202A + AIT_AEROBIC_NO3_202B) * 0.5;
    bFault_NO3_A := FALSE; bFault_NO3_B := FALSE; bFault_NO3_C := TRUE;
    rTimer_Disc_NO3 := rTimer_Disc_NO3 + rCycleTime_s;
ELSIF (ABS(AIT_AEROBIC_NO3_202A - AIT_AEROBIC_NO3_202C) <= c_Tol_NO3_mg_L) THEN
    rVoted_AerobicNO3_mg_L := (AIT_AEROBIC_NO3_202A + AIT_AEROBIC_NO3_202C) * 0.5;
    bFault_NO3_A := FALSE; bFault_NO3_B := TRUE; bFault_NO3_C := FALSE;
    rTimer_Disc_NO3 := rTimer_Disc_NO3 + rCycleTime_s;
ELSIF (ABS(AIT_AEROBIC_NO3_202B - AIT_AEROBIC_NO3_202C) <= c_Tol_NO3_mg_L) THEN
    rVoted_AerobicNO3_mg_L := (AIT_AEROBIC_NO3_202B + AIT_AEROBIC_NO3_202C) * 0.5;
    bFault_NO3_A := TRUE; bFault_NO3_B := FALSE; bFault_NO3_C := FALSE;
    rTimer_Disc_NO3 := rTimer_Disc_NO3 + rCycleTime_s;
ELSE
    bFault_NO3_A := TRUE; bFault_NO3_B := TRUE; bFault_NO3_C := TRUE;
    rTimer_Disc_NO3 := rTimer_Disc_NO3 + rCycleTime_s;
END_IF;

(* 1.6 Aeration Header Pressure Transmitters (PT_AERATION_HEADER_203A/B/C) *)
IF (ABS(PT_AERATION_HEADER_203A - PT_AERATION_HEADER_203B) <= c_Tol_HeaderPres_kPa) AND
   (ABS(PT_AERATION_HEADER_203B - PT_AERATION_HEADER_203C) <= c_Tol_HeaderPres_kPa) AND
   (ABS(PT_AERATION_HEADER_203C - PT_AERATION_HEADER_203A) <= c_Tol_HeaderPres_kPa) THEN
    rVoted_HeaderPressure_kPa := (PT_AERATION_HEADER_203A + PT_AERATION_HEADER_203B + PT_AERATION_HEADER_203C) / 3.0;
    bFault_HeaderPres_A := FALSE; bFault_HeaderPres_B := FALSE; bFault_HeaderPres_C := FALSE;
    rTimer_Disc_HeaderPres := 0.0;
ELSIF (ABS(PT_AERATION_HEADER_203A - PT_AERATION_HEADER_203B) <= c_Tol_HeaderPres_kPa) THEN
    rVoted_HeaderPressure_kPa := (PT_AERATION_HEADER_203A + PT_AERATION_HEADER_203B) * 0.5;
    bFault_HeaderPres_A := FALSE; bFault_HeaderPres_B := FALSE; bFault_HeaderPres_C := TRUE;
    rTimer_Disc_HeaderPres := rTimer_Disc_HeaderPres + rCycleTime_s;
ELSIF (ABS(PT_AERATION_HEADER_203A - PT_AERATION_HEADER_203C) <= c_Tol_HeaderPres_kPa) THEN
    rVoted_HeaderPressure_kPa := (PT_AERATION_HEADER_203A + PT_AERATION_HEADER_203C) * 0.5;
    bFault_HeaderPres_A := FALSE; bFault_HeaderPres_B := TRUE; bFault_HeaderPres_C := FALSE;
    rTimer_Disc_HeaderPres := rTimer_Disc_HeaderPres + rCycleTime_s;
ELSIF (ABS(PT_AERATION_HEADER_203B - PT_AERATION_HEADER_203C) <= c_Tol_HeaderPres_kPa) THEN
    rVoted_HeaderPressure_kPa := (PT_AERATION_HEADER_203B + PT_AERATION_HEADER_203C) * 0.5;
    bFault_HeaderPres_A := TRUE; bFault_HeaderPres_B := FALSE; bFault_HeaderPres_C := FALSE;
    rTimer_Disc_HeaderPres := rTimer_Disc_HeaderPres + rCycleTime_s;
ELSE
    bFault_HeaderPres_A := TRUE; bFault_HeaderPres_B := TRUE; bFault_HeaderPres_C := TRUE;
    rTimer_Disc_HeaderPres := rTimer_Disc_HeaderPres + rCycleTime_s;
END_IF;

(* 1.7 Blower Air Mass Flowmeters (FT_BLOWER_AIR_FLOW_204A/B/C) *)
IF (ABS(FT_BLOWER_AIR_FLOW_204A - FT_BLOWER_AIR_FLOW_204B) <= c_Tol_AirFlow_Nm3_h) AND
   (ABS(FT_BLOWER_AIR_FLOW_204B - FT_BLOWER_AIR_FLOW_204C) <= c_Tol_AirFlow_Nm3_h) AND
   (ABS(FT_BLOWER_AIR_FLOW_204C - FT_BLOWER_AIR_FLOW_204A) <= c_Tol_AirFlow_Nm3_h) THEN
    rVoted_BlowerAirFlow_Nm3_h := (FT_BLOWER_AIR_FLOW_204A + FT_BLOWER_AIR_FLOW_204B + FT_BLOWER_AIR_FLOW_204C) / 3.0;
    bFault_AirFlow_A := FALSE; bFault_AirFlow_B := FALSE; bFault_AirFlow_C := FALSE;
    rTimer_Disc_AirFlow := 0.0;
ELSIF (ABS(FT_BLOWER_AIR_FLOW_204A - FT_BLOWER_AIR_FLOW_204B) <= c_Tol_AirFlow_Nm3_h) THEN
    rVoted_BlowerAirFlow_Nm3_h := (FT_BLOWER_AIR_FLOW_204A + FT_BLOWER_AIR_FLOW_204B) * 0.5;
    bFault_AirFlow_A := FALSE; bFault_AirFlow_B := FALSE; bFault_AirFlow_C := TRUE;
    rTimer_Disc_AirFlow := rTimer_Disc_AirFlow + rCycleTime_s;
ELSIF (ABS(FT_BLOWER_AIR_FLOW_204A - FT_BLOWER_AIR_FLOW_204C) <= c_Tol_AirFlow_Nm3_h) THEN
    rVoted_BlowerAirFlow_Nm3_h := (FT_BLOWER_AIR_FLOW_204A + FT_BLOWER_AIR_FLOW_204C) * 0.5;
    bFault_AirFlow_A := FALSE; bFault_AirFlow_B := TRUE; bFault_AirFlow_C := FALSE;
    rTimer_Disc_AirFlow := rTimer_Disc_AirFlow + rCycleTime_s;
ELSIF (ABS(FT_BLOWER_AIR_FLOW_204B - FT_BLOWER_AIR_FLOW_204C) <= c_Tol_AirFlow_Nm3_h) THEN
    rVoted_BlowerAirFlow_Nm3_h := (FT_BLOWER_AIR_FLOW_204B + FT_BLOWER_AIR_FLOW_204C) * 0.5;
    bFault_AirFlow_A := TRUE; bFault_AirFlow_B := FALSE; bFault_AirFlow_C := FALSE;
    rTimer_Disc_AirFlow := rTimer_Disc_AirFlow + rCycleTime_s;
ELSE
    bFault_AirFlow_A := TRUE; bFault_AirFlow_B := TRUE; bFault_AirFlow_C := TRUE;
    rTimer_Disc_AirFlow := rTimer_Disc_AirFlow + rCycleTime_s;
END_IF;

(* 1.8 Pre-Anoxic Basin ORP Analyzers (AIT_ANOXIC_ORP_301A/B/C) *)
IF (ABS(AIT_ANOXIC_ORP_301A - AIT_ANOXIC_ORP_301B) <= c_Tol_ORP_mV) AND
   (ABS(AIT_ANOXIC_ORP_301B - AIT_ANOXIC_ORP_301C) <= c_Tol_ORP_mV) AND
   (ABS(AIT_ANOXIC_ORP_301C - AIT_ANOXIC_ORP_301A) <= c_Tol_ORP_mV) THEN
    rVoted_AnoxicORP_mV := (AIT_ANOXIC_ORP_301A + AIT_ANOXIC_ORP_301B + AIT_ANOXIC_ORP_301C) / 3.0;
    bFault_ORP_A := FALSE; bFault_ORP_B := FALSE; bFault_ORP_C := FALSE;
    rTimer_Disc_ORP := 0.0;
ELSIF (ABS(AIT_ANOXIC_ORP_301A - AIT_ANOXIC_ORP_301B) <= c_Tol_ORP_mV) THEN
    rVoted_AnoxicORP_mV := (AIT_ANOXIC_ORP_301A + AIT_ANOXIC_ORP_301B) * 0.5;
    bFault_ORP_A := FALSE; bFault_ORP_B := FALSE; bFault_ORP_C := TRUE;
    rTimer_Disc_ORP := rTimer_Disc_ORP + rCycleTime_s;
ELSIF (ABS(AIT_ANOXIC_ORP_301A - AIT_ANOXIC_ORP_301C) <= c_Tol_ORP_mV) THEN
    rVoted_AnoxicORP_mV := (AIT_ANOXIC_ORP_301A + AIT_ANOXIC_ORP_301C) * 0.5;
    bFault_ORP_A := FALSE; bFault_ORP_B := TRUE; bFault_ORP_C := FALSE;
    rTimer_Disc_ORP := rTimer_Disc_ORP + rCycleTime_s;
ELSIF (ABS(AIT_ANOXIC_ORP_301B - AIT_ANOXIC_ORP_301C) <= c_Tol_ORP_mV) THEN
    rVoted_AnoxicORP_mV := (AIT_ANOXIC_ORP_301B + AIT_ANOXIC_ORP_301C) * 0.5;
    bFault_ORP_A := TRUE; bFault_ORP_B := FALSE; bFault_ORP_C := FALSE;
    rTimer_Disc_ORP := rTimer_Disc_ORP + rCycleTime_s;
ELSE
    bFault_ORP_A := TRUE; bFault_ORP_B := TRUE; bFault_ORP_C := TRUE;
    rTimer_Disc_ORP := rTimer_Disc_ORP + rCycleTime_s;
END_IF;

(* 1.9 Internal Nitrate Recycle Flowmeters (FT_INTERNAL_RECYCLE_IR_302A/B/C) *)
IF (ABS(FT_INTERNAL_RECYCLE_IR_302A - FT_INTERNAL_RECYCLE_IR_302B) <= c_Tol_IRFlow_m3_h) AND
   (ABS(FT_INTERNAL_RECYCLE_IR_302B - FT_INTERNAL_RECYCLE_IR_302C) <= c_Tol_IRFlow_m3_h) AND
   (ABS(FT_INTERNAL_RECYCLE_IR_302C - FT_INTERNAL_RECYCLE_IR_302A) <= c_Tol_IRFlow_m3_h) THEN
    rVoted_RAS_Flow_m3_h := (FT_INTERNAL_RECYCLE_IR_302A + FT_INTERNAL_RECYCLE_IR_302B + FT_INTERNAL_RECYCLE_IR_302C) / 3.0;
    bFault_IRFlow_A := FALSE; bFault_IRFlow_B := FALSE; bFault_IRFlow_C := FALSE;
    rTimer_Disc_IRFlow := 0.0;
ELSIF (ABS(FT_INTERNAL_RECYCLE_IR_302A - FT_INTERNAL_RECYCLE_IR_302B) <= c_Tol_IRFlow_m3_h) THEN
    rVoted_RAS_Flow_m3_h := (FT_INTERNAL_RECYCLE_IR_302A + FT_INTERNAL_RECYCLE_IR_302B) * 0.5;
    bFault_IRFlow_A := FALSE; bFault_IRFlow_B := FALSE; bFault_IRFlow_C := TRUE;
    rTimer_Disc_IRFlow := rTimer_Disc_IRFlow + rCycleTime_s;
ELSIF (ABS(FT_INTERNAL_RECYCLE_IR_302A - FT_INTERNAL_RECYCLE_IR_302C) <= c_Tol_IRFlow_m3_h) THEN
    rVoted_RAS_Flow_m3_h := (FT_INTERNAL_RECYCLE_IR_302A + FT_INTERNAL_RECYCLE_IR_302C) * 0.5;
    bFault_IRFlow_A := FALSE; bFault_IRFlow_B := TRUE; bFault_IRFlow_C := FALSE;
    rTimer_Disc_IRFlow := rTimer_Disc_IRFlow + rCycleTime_s;
ELSIF (ABS(FT_INTERNAL_RECYCLE_IR_302B - FT_INTERNAL_RECYCLE_IR_302C) <= c_Tol_IRFlow_m3_h) THEN
    rVoted_RAS_Flow_m3_h := (FT_INTERNAL_RECYCLE_IR_302B + FT_INTERNAL_RECYCLE_IR_302C) * 0.5;
    bFault_IRFlow_A := TRUE; bFault_IRFlow_B := FALSE; bFault_IRFlow_C := FALSE;
    rTimer_Disc_IRFlow := rTimer_Disc_IRFlow + rCycleTime_s;
ELSE
    bFault_IRFlow_A := TRUE; bFault_IRFlow_B := TRUE; bFault_IRFlow_C := TRUE;
    rTimer_Disc_IRFlow := rTimer_Disc_IRFlow + rCycleTime_s;
END_IF;

(* 1.10 External Carbon Dosing Coriolis Flowmeters (FT_CARBON_SOURCE_DOSE_303A/B/C) *)
IF (ABS(FT_CARBON_SOURCE_DOSE_303A - FT_CARBON_SOURCE_DOSE_303B) <= c_Tol_Carbon_Lph) AND
   (ABS(FT_CARBON_SOURCE_DOSE_303B - FT_CARBON_SOURCE_DOSE_303C) <= c_Tol_Carbon_Lph) AND
   (ABS(FT_CARBON_SOURCE_DOSE_303C - FT_CARBON_SOURCE_DOSE_303A) <= c_Tol_Carbon_Lph) THEN
    bFault_Carbon_A := FALSE; bFault_Carbon_B := FALSE; bFault_Carbon_C := FALSE;
    rTimer_Disc_CarbonDose := 0.0;
ELSIF (ABS(FT_CARBON_SOURCE_DOSE_303A - FT_CARBON_SOURCE_DOSE_303B) <= c_Tol_Carbon_Lph) THEN
    bFault_Carbon_A := FALSE; bFault_Carbon_B := FALSE; bFault_Carbon_C := TRUE;
    rTimer_Disc_CarbonDose := rTimer_Disc_CarbonDose + rCycleTime_s;
ELSIF (ABS(FT_CARBON_SOURCE_DOSE_303A - FT_CARBON_SOURCE_DOSE_303C) <= c_Tol_Carbon_Lph) THEN
    bFault_Carbon_A := FALSE; bFault_Carbon_B := TRUE; bFault_Carbon_C := FALSE;
    rTimer_Disc_CarbonDose := rTimer_Disc_CarbonDose + rCycleTime_s;
ELSIF (ABS(FT_CARBON_SOURCE_DOSE_303B - FT_CARBON_SOURCE_DOSE_303C) <= c_Tol_Carbon_Lph) THEN
    bFault_Carbon_A := TRUE; bFault_Carbon_B := FALSE; bFault_Carbon_C := FALSE;
    rTimer_Disc_CarbonDose := rTimer_Disc_CarbonDose + rCycleTime_s;
ELSE
    bFault_Carbon_A := TRUE; bFault_Carbon_B := TRUE; bFault_Carbon_C := TRUE;
    rTimer_Disc_CarbonDose := rTimer_Disc_CarbonDose + rCycleTime_s;
END_IF;

(* 1.11 Effluent Orthophosphate Analyzers (AIT_EFFLUENT_PO4_401A/B/C) *)
IF (ABS(AIT_EFFLUENT_PO4_401A - AIT_EFFLUENT_PO4_401B) <= c_Tol_PO4_mg_L) AND
   (ABS(AIT_EFFLUENT_PO4_401B - AIT_EFFLUENT_PO4_401C) <= c_Tol_PO4_mg_L) AND
   (ABS(AIT_EFFLUENT_PO4_401C - AIT_EFFLUENT_PO4_401A) <= c_Tol_PO4_mg_L) THEN
    rVoted_EffluentPO4_mg_L := (AIT_EFFLUENT_PO4_401A + AIT_EFFLUENT_PO4_401B + AIT_EFFLUENT_PO4_401C) / 3.0;
    bFault_PO4_A := FALSE; bFault_PO4_B := FALSE; bFault_PO4_C := FALSE;
    rTimer_Disc_PO4 := 0.0;
ELSIF (ABS(AIT_EFFLUENT_PO4_401A - AIT_EFFLUENT_PO4_401B) <= c_Tol_PO4_mg_L) THEN
    rVoted_EffluentPO4_mg_L := (AIT_EFFLUENT_PO4_401A + AIT_EFFLUENT_PO4_401B) * 0.5;
    bFault_PO4_A := FALSE; bFault_PO4_B := FALSE; bFault_PO4_C := TRUE;
    rTimer_Disc_PO4 := rTimer_Disc_PO4 + rCycleTime_s;
ELSIF (ABS(AIT_EFFLUENT_PO4_401A - AIT_EFFLUENT_PO4_401C) <= c_Tol_PO4_mg_L) THEN
    rVoted_EffluentPO4_mg_L := (AIT_EFFLUENT_PO4_401A + AIT_EFFLUENT_PO4_401C) * 0.5;
    bFault_PO4_A := FALSE; bFault_PO4_B := TRUE; bFault_PO4_C := FALSE;
    rTimer_Disc_PO4 := rTimer_Disc_PO4 + rCycleTime_s;
ELSIF (ABS(AIT_EFFLUENT_PO4_401B - AIT_EFFLUENT_PO4_401C) <= c_Tol_PO4_mg_L) THEN
    rVoted_EffluentPO4_mg_L := (AIT_EFFLUENT_PO4_401B + AIT_EFFLUENT_PO4_401C) * 0.5;
    bFault_PO4_A := TRUE; bFault_PO4_B := FALSE; bFault_PO4_C := FALSE;
    rTimer_Disc_PO4 := rTimer_Disc_PO4 + rCycleTime_s;
ELSE
    bFault_PO4_A := TRUE; bFault_PO4_B := TRUE; bFault_PO4_C := TRUE;
    rTimer_Disc_PO4 := rTimer_Disc_PO4 + rCycleTime_s;
END_IF;

(* 1.12 FeCl3 Coagulant Flowmeters (FT_FECL3_COAGULANT_DOSE_402A/B/C) *)
IF (ABS(FT_FECL3_COAGULANT_DOSE_402A - FT_FECL3_COAGULANT_DOSE_402B) <= c_Tol_FeCl3_Lph) AND
   (ABS(FT_FECL3_COAGULANT_DOSE_402B - FT_FECL3_COAGULANT_DOSE_402C) <= c_Tol_FeCl3_Lph) AND
   (ABS(FT_FECL3_COAGULANT_DOSE_402C - FT_FECL3_COAGULANT_DOSE_402A) <= c_Tol_FeCl3_Lph) THEN
    bFault_FeCl3_A := FALSE; bFault_FeCl3_B := FALSE; bFault_FeCl3_C := FALSE;
    rTimer_Disc_FeCl3 := 0.0;
ELSIF (ABS(FT_FECL3_COAGULANT_DOSE_402A - FT_FECL3_COAGULANT_DOSE_402B) <= c_Tol_FeCl3_Lph) THEN
    bFault_FeCl3_A := FALSE; bFault_FeCl3_B := FALSE; bFault_FeCl3_C := TRUE;
    rTimer_Disc_FeCl3 := rTimer_Disc_FeCl3 + rCycleTime_s;
ELSIF (ABS(FT_FECL3_COAGULANT_DOSE_402A - FT_FECL3_COAGULANT_DOSE_402C) <= c_Tol_FeCl3_Lph) THEN
    bFault_FeCl3_A := FALSE; bFault_FeCl3_B := TRUE; bFault_FeCl3_C := FALSE;
    rTimer_Disc_FeCl3 := rTimer_Disc_FeCl3 + rCycleTime_s;
ELSIF (ABS(FT_FECL3_COAGULANT_DOSE_402B - FT_FECL3_COAGULANT_DOSE_402C) <= c_Tol_FeCl3_Lph) THEN
    bFault_FeCl3_A := TRUE; bFault_FeCl3_B := FALSE; bFault_FeCl3_C := FALSE;
    rTimer_Disc_FeCl3 := rTimer_Disc_FeCl3 + rCycleTime_s;
ELSE
    bFault_FeCl3_A := TRUE; bFault_FeCl3_B := TRUE; bFault_FeCl3_C := TRUE;
    rTimer_Disc_FeCl3 := rTimer_Disc_FeCl3 + rCycleTime_s;
END_IF;

(* 1.13 MBR Transmembrane Differential Pressure (DPS_MBR_TMP_502A/B/C) *)
IF (ABS(DPS_MBR_TMP_502A - DPS_MBR_TMP_502B) <= c_Tol_TMP_kPa) AND
   (ABS(DPS_MBR_TMP_502B - DPS_MBR_TMP_502C) <= c_Tol_TMP_kPa) AND
   (ABS(DPS_MBR_TMP_502C - DPS_MBR_TMP_502A) <= c_Tol_TMP_kPa) THEN
    rVoted_MBR_TMP_kPa := (DPS_MBR_TMP_502A + DPS_MBR_TMP_502B + DPS_MBR_TMP_502C) / 3.0;
    bFault_TMP_A := FALSE; bFault_TMP_B := FALSE; bFault_TMP_C := FALSE;
    rTimer_Disc_TMP := 0.0;
ELSIF (ABS(DPS_MBR_TMP_502A - DPS_MBR_TMP_502B) <= c_Tol_TMP_kPa) THEN
    rVoted_MBR_TMP_kPa := (DPS_MBR_TMP_502A + DPS_MBR_TMP_502B) * 0.5;
    bFault_TMP_A := FALSE; bFault_TMP_B := FALSE; bFault_TMP_C := TRUE;
    rTimer_Disc_TMP := rTimer_Disc_TMP + rCycleTime_s;
ELSIF (ABS(DPS_MBR_TMP_502A - DPS_MBR_TMP_502C) <= c_Tol_TMP_kPa) THEN
    rVoted_MBR_TMP_kPa := (DPS_MBR_TMP_502A + DPS_MBR_TMP_502C) * 0.5;
    bFault_TMP_A := FALSE; bFault_TMP_B := TRUE; bFault_TMP_C := FALSE;
    rTimer_Disc_TMP := rTimer_Disc_TMP + rCycleTime_s;
ELSIF (ABS(DPS_MBR_TMP_502B - DPS_MBR_TMP_502C) <= c_Tol_TMP_kPa) THEN
    rVoted_MBR_TMP_kPa := (DPS_MBR_TMP_502B + DPS_MBR_TMP_502C) * 0.5;
    bFault_TMP_A := TRUE; bFault_TMP_B := FALSE; bFault_TMP_C := FALSE;
    rTimer_Disc_TMP := rTimer_Disc_TMP + rCycleTime_s;
ELSE
    bFault_TMP_A := TRUE; bFault_TMP_B := TRUE; bFault_TMP_C := TRUE;
    rTimer_Disc_TMP := rTimer_Disc_TMP + rCycleTime_s;
END_IF;

(* 1.14 Secondary Clarifier Sludge Blanket Height (LT_CLARIFIER_SLUDGE_BLANKET_601A/B/C) *)
IF (ABS(LT_CLARIFIER_SLUDGE_BLANKET_601A - LT_CLARIFIER_SLUDGE_BLANKET_601B) <= c_Tol_Blanket_m) AND
   (ABS(LT_CLARIFIER_SLUDGE_BLANKET_601B - LT_CLARIFIER_SLUDGE_BLANKET_601C) <= c_Tol_Blanket_m) AND
   (ABS(LT_CLARIFIER_SLUDGE_BLANKET_601C - LT_CLARIFIER_SLUDGE_BLANKET_601A) <= c_Tol_Blanket_m) THEN
    rVoted_ClarifierSludgeBlanket_m := (LT_CLARIFIER_SLUDGE_BLANKET_601A + LT_CLARIFIER_SLUDGE_BLANKET_601B + LT_CLARIFIER_SLUDGE_BLANKET_601C) / 3.0;
    bFault_Blanket_A := FALSE; bFault_Blanket_B := FALSE; bFault_Blanket_C := FALSE;
    rTimer_Disc_Blanket := 0.0;
ELSIF (ABS(LT_CLARIFIER_SLUDGE_BLANKET_601A - LT_CLARIFIER_SLUDGE_BLANKET_601B) <= c_Tol_Blanket_m) THEN
    rVoted_ClarifierSludgeBlanket_m := (LT_CLARIFIER_SLUDGE_BLANKET_601A + LT_CLARIFIER_SLUDGE_BLANKET_601B) * 0.5;
    bFault_Blanket_A := FALSE; bFault_Blanket_B := FALSE; bFault_Blanket_C := TRUE;
    rTimer_Disc_Blanket := rTimer_Disc_Blanket + rCycleTime_s;
ELSIF (ABS(LT_CLARIFIER_SLUDGE_BLANKET_601A - LT_CLARIFIER_SLUDGE_BLANKET_601C) <= c_Tol_Blanket_m) THEN
    rVoted_ClarifierSludgeBlanket_m := (LT_CLARIFIER_SLUDGE_BLANKET_601A + LT_CLARIFIER_SLUDGE_BLANKET_601C) * 0.5;
    bFault_Blanket_A := FALSE; bFault_Blanket_B := TRUE; bFault_Blanket_C := FALSE;
    rTimer_Disc_Blanket := rTimer_Disc_Blanket + rCycleTime_s;
ELSIF (ABS(LT_CLARIFIER_SLUDGE_BLANKET_601B - LT_CLARIFIER_SLUDGE_BLANKET_601C) <= c_Tol_Blanket_m) THEN
    rVoted_ClarifierSludgeBlanket_m := (LT_CLARIFIER_SLUDGE_BLANKET_601B + LT_CLARIFIER_SLUDGE_BLANKET_601C) * 0.5;
    bFault_Blanket_A := TRUE; bFault_Blanket_B := FALSE; bFault_Blanket_C := FALSE;
    rTimer_Disc_Blanket := rTimer_Disc_Blanket + rCycleTime_s;
ELSE
    bFault_Blanket_A := TRUE; bFault_Blanket_B := TRUE; bFault_Blanket_C := TRUE;
    rTimer_Disc_Blanket := rTimer_Disc_Blanket + rCycleTime_s;
END_IF;

(* 1.15 Return Activated Sludge Flowmeters (FT_RAS_PUMP_FLOW_602A/B/C) *)
IF (ABS(FT_RAS_PUMP_FLOW_602A - FT_RAS_PUMP_FLOW_602B) <= c_Tol_RASFlow_m3_h) AND
   (ABS(FT_RAS_PUMP_FLOW_602B - FT_RAS_PUMP_FLOW_602C) <= c_Tol_RASFlow_m3_h) AND
   (ABS(FT_RAS_PUMP_FLOW_602C - FT_RAS_PUMP_FLOW_602A) <= c_Tol_RASFlow_m3_h) THEN
    rVoted_RAS_Flow_m3_h := (FT_RAS_PUMP_FLOW_602A + FT_RAS_PUMP_FLOW_602B + FT_RAS_PUMP_FLOW_602C) / 3.0;
    bFault_RASFlow_A := FALSE; bFault_RASFlow_B := FALSE; bFault_RASFlow_C := FALSE;
    rTimer_Disc_RASFlow := 0.0;
ELSIF (ABS(FT_RAS_PUMP_FLOW_602A - FT_RAS_PUMP_FLOW_602B) <= c_Tol_RASFlow_m3_h) THEN
    rVoted_RAS_Flow_m3_h := (FT_RAS_PUMP_FLOW_602A + FT_RAS_PUMP_FLOW_602B) * 0.5;
    bFault_RASFlow_A := FALSE; bFault_RASFlow_B := FALSE; bFault_RASFlow_C := TRUE;
    rTimer_Disc_RASFlow := rTimer_Disc_RASFlow + rCycleTime_s;
ELSIF (ABS(FT_RAS_PUMP_FLOW_602A - FT_RAS_PUMP_FLOW_602C) <= c_Tol_RASFlow_m3_h) THEN
    rVoted_RAS_Flow_m3_h := (FT_RAS_PUMP_FLOW_602A + FT_RAS_PUMP_FLOW_602C) * 0.5;
    bFault_RASFlow_A := FALSE; bFault_RASFlow_B := TRUE; bFault_RASFlow_C := FALSE;
    rTimer_Disc_RASFlow := rTimer_Disc_RASFlow + rCycleTime_s;
ELSIF (ABS(FT_RAS_PUMP_FLOW_602B - FT_RAS_PUMP_FLOW_602C) <= c_Tol_RASFlow_m3_h) THEN
    rVoted_RAS_Flow_m3_h := (FT_RAS_PUMP_FLOW_602B + FT_RAS_PUMP_FLOW_602C) * 0.5;
    bFault_RASFlow_A := TRUE; bFault_RASFlow_B := FALSE; bFault_RASFlow_C := FALSE;
    rTimer_Disc_RASFlow := rTimer_Disc_RASFlow + rCycleTime_s;
ELSE
    bFault_RASFlow_A := TRUE; bFault_RASFlow_B := TRUE; bFault_RASFlow_C := TRUE;
    rTimer_Disc_RASFlow := rTimer_Disc_RASFlow + rCycleTime_s;
END_IF;

(* 1.16 Mixed Liquor Water Temperature Pt100 RTDs (TI_WATER_TEMP_104A/B/C) *)
IF (ABS(TI_WATER_TEMP_104A - TI_WATER_TEMP_104B) <= c_Tol_Temp_degC) AND
   (ABS(TI_WATER_TEMP_104B - TI_WATER_TEMP_104C) <= c_Tol_Temp_degC) AND
   (ABS(TI_WATER_TEMP_104C - TI_WATER_TEMP_104A) <= c_Tol_Temp_degC) THEN
    rVoted_WaterTemp_degC := (TI_WATER_TEMP_104A + TI_WATER_TEMP_104B + TI_WATER_TEMP_104C) / 3.0;
    bFault_Temp_A := FALSE; bFault_Temp_B := FALSE; bFault_Temp_C := FALSE;
    rTimer_Disc_WaterTemp := 0.0;
ELSIF (ABS(TI_WATER_TEMP_104A - TI_WATER_TEMP_104B) <= c_Tol_Temp_degC) THEN
    rVoted_WaterTemp_degC := (TI_WATER_TEMP_104A + TI_WATER_TEMP_104B) * 0.5;
    bFault_Temp_A := FALSE; bFault_Temp_B := FALSE; bFault_Temp_C := TRUE;
    rTimer_Disc_WaterTemp := rTimer_Disc_WaterTemp + rCycleTime_s;
ELSIF (ABS(TI_WATER_TEMP_104A - TI_WATER_TEMP_104C) <= c_Tol_Temp_degC) THEN
    rVoted_WaterTemp_degC := (TI_WATER_TEMP_104A + TI_WATER_TEMP_104C) * 0.5;
    bFault_Temp_A := FALSE; bFault_Temp_B := TRUE; bFault_Temp_C := FALSE;
    rTimer_Disc_WaterTemp := rTimer_Disc_WaterTemp + rCycleTime_s;
ELSIF (ABS(TI_WATER_TEMP_104B - TI_WATER_TEMP_104C) <= c_Tol_Temp_degC) THEN
    rVoted_WaterTemp_degC := (TI_WATER_TEMP_104B + TI_WATER_TEMP_104C) * 0.5;
    bFault_Temp_A := TRUE; bFault_Temp_B := FALSE; bFault_Temp_C := FALSE;
    rTimer_Disc_WaterTemp := rTimer_Disc_WaterTemp + rCycleTime_s;
ELSE
    bFault_Temp_A := TRUE; bFault_Temp_B := TRUE; bFault_Temp_C := TRUE;
    rTimer_Disc_WaterTemp := rTimer_Disc_WaterTemp + rCycleTime_s;
END_IF;

(* 1.17 Wastewater Influent pH Electrodes (AIT_INFLUENT_PH_105A/B/C) *)
IF (ABS(AIT_INFLUENT_PH_105A - AIT_INFLUENT_PH_105B) <= c_Tol_PH) AND
   (ABS(AIT_INFLUENT_PH_105B - AIT_INFLUENT_PH_105C) <= c_Tol_PH) AND
   (ABS(AIT_INFLUENT_PH_105C - AIT_INFLUENT_PH_105A) <= c_Tol_PH) THEN
    rVoted_InfluentPH := (AIT_INFLUENT_PH_105A + AIT_INFLUENT_PH_105B + AIT_INFLUENT_PH_105C) / 3.0;
    bFault_PH_A := FALSE; bFault_PH_B := FALSE; bFault_PH_C := FALSE;
    rTimer_Disc_PH := 0.0;
ELSIF (ABS(AIT_INFLUENT_PH_105A - AIT_INFLUENT_PH_105B) <= c_Tol_PH) THEN
    rVoted_InfluentPH := (AIT_INFLUENT_PH_105A + AIT_INFLUENT_PH_105B) * 0.5;
    bFault_PH_A := FALSE; bFault_PH_B := FALSE; bFault_PH_C := TRUE;
    rTimer_Disc_PH := rTimer_Disc_PH + rCycleTime_s;
ELSIF (ABS(AIT_INFLUENT_PH_105A - AIT_INFLUENT_PH_105C) <= c_Tol_PH) THEN
    rVoted_InfluentPH := (AIT_INFLUENT_PH_105A + AIT_INFLUENT_PH_105C) * 0.5;
    bFault_PH_A := FALSE; bFault_PH_B := TRUE; bFault_PH_C := FALSE;
    rTimer_Disc_PH := rTimer_Disc_PH + rCycleTime_s;
ELSIF (ABS(AIT_INFLUENT_PH_105B - AIT_INFLUENT_PH_105C) <= c_Tol_PH) THEN
    rVoted_InfluentPH := (AIT_INFLUENT_PH_105B + AIT_INFLUENT_PH_105C) * 0.5;
    bFault_PH_A := TRUE; bFault_PH_B := FALSE; bFault_PH_C := FALSE;
    rTimer_Disc_PH := rTimer_Disc_PH + rCycleTime_s;
ELSE
    bFault_PH_A := TRUE; bFault_PH_B := TRUE; bFault_PH_C := TRUE;
    rTimer_Disc_PH := rTimer_Disc_PH + rCycleTime_s;
END_IF;

(* 1.18 Influent Toxic Cyanide & Heavy Metals (AIT_TOXIC_SPIKE_106A/B/C) *)
IF (ABS(AIT_TOXIC_SPIKE_106A - AIT_TOXIC_SPIKE_106B) <= c_Tol_Toxic_ppm) AND
   (ABS(AIT_TOXIC_SPIKE_106B - AIT_TOXIC_SPIKE_106C) <= c_Tol_Toxic_ppm) AND
   (ABS(AIT_TOXIC_SPIKE_106C - AIT_TOXIC_SPIKE_106A) <= c_Tol_Toxic_ppm) THEN
    rVoted_ToxicSpike_ppm := (AIT_TOXIC_SPIKE_106A + AIT_TOXIC_SPIKE_106B + AIT_TOXIC_SPIKE_106C) / 3.0;
    bFault_Toxic_A := FALSE; bFault_Toxic_B := FALSE; bFault_Toxic_C := FALSE;
    rTimer_Disc_Toxic := 0.0;
ELSIF (ABS(AIT_TOXIC_SPIKE_106A - AIT_TOXIC_SPIKE_106B) <= c_Tol_Toxic_ppm) THEN
    rVoted_ToxicSpike_ppm := (AIT_TOXIC_SPIKE_106A + AIT_TOXIC_SPIKE_106B) * 0.5;
    bFault_Toxic_A := FALSE; bFault_Toxic_B := FALSE; bFault_Toxic_C := TRUE;
    rTimer_Disc_Toxic := rTimer_Disc_Toxic + rCycleTime_s;
ELSIF (ABS(AIT_TOXIC_SPIKE_106A - AIT_TOXIC_SPIKE_106C) <= c_Tol_Toxic_ppm) THEN
    rVoted_ToxicSpike_ppm := (AIT_TOXIC_SPIKE_106A + AIT_TOXIC_SPIKE_106C) * 0.5;
    bFault_Toxic_A := FALSE; bFault_Toxic_B := TRUE; bFault_Toxic_C := FALSE;
    rTimer_Disc_Toxic := rTimer_Disc_Toxic + rCycleTime_s;
ELSIF (ABS(AIT_TOXIC_SPIKE_106B - AIT_TOXIC_SPIKE_106C) <= c_Tol_Toxic_ppm) THEN
    rVoted_ToxicSpike_ppm := (AIT_TOXIC_SPIKE_106B + AIT_TOXIC_SPIKE_106C) * 0.5;
    bFault_Toxic_A := TRUE; bFault_Toxic_B := FALSE; bFault_Toxic_C := FALSE;
    rTimer_Disc_Toxic := rTimer_Disc_Toxic + rCycleTime_s;
ELSE
    bFault_Toxic_A := TRUE; bFault_Toxic_B := TRUE; bFault_Toxic_C := TRUE;
    rTimer_Disc_Toxic := rTimer_Disc_Toxic + rCycleTime_s;
END_IF;"""
    parts.append(phase1_code)

    # 7. PHASE 2: CYBER-PHYSICAL BIOKINETIC & HYDRODYNAMIC OBSERVERS
    phase2_code = """(* ==================================================================================================== *)
(* PHASE 2: CYBER-PHYSICAL BIOKINETIC, OXYGEN TRANSFER & MEMBRANE FOULING OBSERVERS                    *)
(* ==================================================================================================== *)

(* 2.1 Dynamic Dissolved Oxygen Saturation & Oxygen Transfer Rate (OTR) Observer *)
(* Benson & Krause Empirical Equation for Clean Water Saturation DO *)
rC_star_DO_sat := 14.652 - (0.41022 * rVoted_WaterTemp_degC) + (0.007991 * rVoted_WaterTemp_degC * rVoted_WaterTemp_degC)
                  - (0.000077774 * rVoted_WaterTemp_degC * rVoted_WaterTemp_degC * rVoted_WaterTemp_degC);

(* Dynamic Alpha-Factor Observer (Ceramic Fine-Pore Diffuser Fouling & Surfactants) *)
rSurfactantSuppressionRatio := (rVoted_InfluentCOD_mg_L / 450.0) * 0.08;
IF rSurfactantSuppressionRatio > 0.25 THEN
    rSurfactantSuppressionRatio := 0.25;
END_IF;

rObs_DynamicAlphaFactor := rAlpha_0 * (1.0 - (0.000018 * rNominalMLSS_mg_L)) * (1.0 - rSurfactantSuppressionRatio);
IF rObs_DynamicAlphaFactor < 0.35 THEN
    rObs_DynamicAlphaFactor := 0.35;
ELSIF rObs_DynamicAlphaFactor > 0.85 THEN
    rObs_DynamicAlphaFactor := 0.85;
END_IF;

(* Diffuser Cleanliness & Fouling Headloss Observer *)
rStaticHydrostaticHead_kPa := (998.2 * 9.80665 * rBasinLiquidDepth_m) / 1000.0;
rTempVar1 := rDiffuserCleanCurve_c0 + (rDiffuserCleanCurve_c1 * rVoted_BlowerAirFlow_Nm3_h)
             + (rDiffuserCleanCurve_c2 * rVoted_BlowerAirFlow_Nm3_h * rVoted_BlowerAirFlow_Nm3_h);
rObs_DiffuserCleanlinessDeltaP_kPa := rVoted_HeaderPressure_kPa - rStaticHydrostaticHead_kPa - rTempVar1;

IF rObs_DiffuserCleanlinessDeltaP_kPa > 8.50 THEN
    bAlarm_DiffuserFouling_Warning := TRUE;
ELSE
    bAlarm_DiffuserFouling_Warning := FALSE;
END_IF;

(* KLa Mass Transfer Coefficient Estimation [1/h] *)
rObs_KLa_Coefficient_per_h := (rVoted_BlowerAirFlow_Nm3_h / rBasinVolume_Aerobic_m3) * 0.185 * rObs_DynamicAlphaFactor
                              * EXPT(1.024, (rVoted_WaterTemp_degC - 20.0));

(* Real-Time OTR Delivered to Mixed Liquor [kg O2/h] *)
rTempVar2 := (rObs_DynamicAlphaFactor * rBeta_Salinity * rC_star_DO_sat) - rVoted_AerobicDO_mg_L;
IF rTempVar2 < 0.10 THEN
    rTempVar2 := 0.10;
END_IF;
rObs_OxygenTransferRate_OTR_kg_h := (rObs_KLa_Coefficient_per_h * rTempVar2 * rBasinVolume_Aerobic_m3) / 1000.0;

(* 2.2 ASM2d Biokinetic Kinetics (Nitrification, Denitrification, Phosphorus Uptake) *)
(* Autotrophic Nitrification Monod Rate r_NH4 [g N/(m3*h)] *)
rTempVar1 := rVoted_InfluentNH4_mg_L / (c_rK_NH4 + rVoted_InfluentNH4_mg_L);
rTempVar2 := rVoted_AerobicDO_mg_L / (c_rK_O_AUT + rVoted_AerobicDO_mg_L);
rTempVar3 := EXPT(c_rTheta_N, (rVoted_WaterTemp_degC - 20.0));
rObs_NitrificationRate_rNH4_g_m3_h := (c_rMu_AUT / 24.0) * rTempVar1 * rTempVar2 * rTempVar3 * c_rX_AUT;

(* Heterotrophic Denitrification Rate r_NO3 [g N/(m3*h)] in Pre-Anoxic Zone *)
rTempVar1 := rVoted_AerobicNO3_mg_L / (c_rK_NO3 + rVoted_AerobicNO3_mg_L);
rTempVar2 := (rVoted_InfluentCOD_mg_L * 0.35) / (c_rK_S + (rVoted_InfluentCOD_mg_L * 0.35));
rTempVar3 := c_rK_O_denit / (c_rK_O_denit + 0.15); (* Anoxic DO assumed ~0.15 mg/L *)
rObs_DenitrificationRate_rNO3_g_m3_h := (c_rMu_HET / 24.0) * c_rEta_g * rTempVar1 * rTempVar2 * rTempVar3
                                       * EXPT(c_rTheta_D, (rVoted_WaterTemp_degC - 20.0)) * c_rX_HET;

(* Biological Phosphorus Luxury Uptake Rate r_PO4 [g P/(m3*h)] *)
rTempVar1 := rVoted_EffluentPO4_mg_L / (c_rK_PO4 + rVoted_EffluentPO4_mg_L);
rTempVar2 := rVoted_AerobicDO_mg_L / (c_rK_O_PAO + rVoted_AerobicDO_mg_L);
rObs_BioP_UptakeRate_rPO4_g_m3_h := (c_rq_PP / 24.0) * rTempVar1 * rTempVar2 * 350.0; (* Active PAO biomass ~ 350 mg/L *)

(* 2.3 Vesilind Dynamic Sludge Settling Flux & Clarifier SBH Mass Balance *)
(* Exponential Hindered Settling Velocity vs [m/h] *)
rObs_SludgeSettlingVelocity_vs_m_h := c_rVesilind_v0 * EXP(-c_rVesilind_rv * (rNominalMLSS_mg_L / 1000.0));
IF rObs_SludgeSettlingVelocity_vs_m_h < 0.20 THEN
    rObs_SludgeSettlingVelocity_vs_m_h := 0.20;
END_IF;

(* Downward Underflow Velocity u = Q_RAS / Area [m/h] *)
rClarifierUnderflowVelocity_m_h := rVoted_RAS_Flow_m3_h / rClarifierArea_m2;
rGravitySolidsFlux_kg_m2_h := rObs_SludgeSettlingVelocity_vs_m_h * (rNominalMLSS_mg_L / 1000.0);
rUnderflowSolidsFlux_kg_m2_h := rClarifierUnderflowVelocity_m_h * (rNominalMLSS_mg_L / 1000.0);
rTotalSolidsFlux_kg_m2_h := rGravitySolidsFlux_kg_m2_h + rUnderflowSolidsFlux_kg_m2_h;
rObs_ClarifierLimitingSolidsFlux := rTotalSolidsFlux_kg_m2_h * 0.92;

(* Dynamic Sludge Blanket Height (SBH) Rate of Change [m/s] *)
rClarifierInfluentSolids_kg_h := (rVoted_InfluentFlow_m3_h + rVoted_RAS_Flow_m3_h) * (rNominalMLSS_mg_L / 1000.0);
rClarifierRAS_Solids_kg_h := rVoted_RAS_Flow_m3_h * ((rNominalMLSS_mg_L * 1.35) / 1000.0);

rTempVar1 := (rClarifierInfluentSolids_kg_h - rClarifierRAS_Solids_kg_h) / 3600.0; (* Net solids accumulation kg/s *)
rTempVar2 := rClarifierBlanketDensity_kg_m3 * rClarifierArea_m2;
rTempVar3 := rTempVar1 / rTempVar2; (* d(SBH)/dt in m/s *)

(* Washout Vulnerability Index *)
rObs_ClarifierWashoutRiskIndex := ((rVoted_InfluentFlow_m3_h / rClarifierArea_m2) / rObs_SludgeSettlingVelocity_vs_m_h)
                                 + (rVoted_ClarifierSludgeBlanket_m / rClarifierDepth_m);

(* 2.4 Submerged Hollow-Fiber MBR Resistance-In-Series Observer *)
(* Dynamic Water Viscosity Pa*s *)
rInstantaneousWaterViscosity_Pa_s := 0.001792 * EXP(-0.025 * rVoted_WaterTemp_degC);

(* Permeate Flux J [m/s] & [LMH] *)
rPermeateFlux_m_s := (rVoted_InfluentFlow_m3_h * 0.85) / (rMembraneTotalArea_m2 * 3600.0);
rPermeateFlux_LMH := rPermeateFlux_m_s * 3.6E6;

(* Darcy Resistance-in-Series: R_tot = TMP / (mu * J) *)
IF rPermeateFlux_m_s > 1.0E-7 THEN
    rObs_MBR_TotalHydraulicResistance := (rVoted_MBR_TMP_kPa * 1000.0) / (rInstantaneousWaterViscosity_Pa_s * rPermeateFlux_m_s);
ELSE
    rObs_MBR_TotalHydraulicResistance := c_rMembraneIntrinsic_Rm;
END_IF;

(* Dynamic Cake Layer Resistance Rc Evolution [1/m] *)
rTempVar1 := c_rCakeAccumulationCoeff * (rNominalMLSS_mg_L / 1000.0) * rPermeateFlux_m_s * rPermeateFlux_m_s;
rTempVar2 := c_rAirScourCleaningEfficiency * EXPT(rBlowerMasterSpeed_pct + 1.0, 0.75) * rCakeResistance_Rc * 0.0001;
rCakeResistance_Rc := rCakeResistance_Rc + ((rTempVar1 - rTempVar2) * rCycleTime_s);

IF rCakeResistance_Rc < 0.0 THEN
    rCakeResistance_Rc := 0.0;
END_IF;
rObs_MBR_CakeResistance_Rc_per_m := rCakeResistance_Rc;

(* Irreversible Pore Constriction Resistance Rp Accumulation *)
rPoreResistance_Rp := rPoreResistance_Rp + (c_rPoreFoulingRate_kp * rPermeateFlux_m_s * (rVoted_InfluentCOD_mg_L * 0.05) * rCycleTime_s);
rObs_MBR_PoreResistance_Rp_per_m := rPoreResistance_Rp;"""
    parts.append(phase2_code)

    # 8. PHASE 3: 8x8 DISCRETE STATE-SPACE & RECEDING-HORIZON MPC
    phase3_code = """(* ==================================================================================================== *)
(* PHASE 3: 8x8 DISCRETE STATE-SPACE & RECEDING-HORIZON MPC CONTROL ACTION                              *)
(* ==================================================================================================== *)

(* 3.1 Measurement Vector Packing *)
y_meas[1] := rVoted_AerobicDO_mg_L;
y_meas[2] := rVoted_InfluentNH4_mg_L;
y_meas[3] := rVoted_AerobicNO3_mg_L;
y_meas[4] := rVoted_EffluentPO4_mg_L;
y_meas[5] := rVoted_MBR_TMP_kPa;
y_meas[6] := rVoted_ClarifierSludgeBlanket_m;
y_meas[7] := rVoted_HeaderPressure_kPa;
y_meas[8] := (rVoted_AerobicNO3_mg_L + rVoted_InfluentNH4_mg_L * 0.15); (* Estimated Effluent TN *)

(* 3.2 Reference Target Vector Packing *)
r_ref[1] := rTargetDO_Setpoint_mg_L;
r_ref[2] := 1.00;                       (* Target NH4 < 1.0 mg/L *)
r_ref[3] := 4.00;                       (* Target NO3 < 4.0 mg/L *)
r_ref[4] := rTargetEffluentTP_Limit_mg_L * 0.75; (* Target PO4 = 0.15 mg/L *)
r_ref[5] := 20.0;                       (* Target TMP = 20 kPa *)
r_ref[6] := rTargetClarifierBlanket_m;  (* Target Blanket = 1.5 m *)
r_ref[7] := 65.0;                       (* Target Header Pressure = 65 kPa *)
r_ref[8] := rTargetEffluentTN_Limit_mg_L * 0.80; (* Target TN = 4.0 mg/L *)

(* 3.3 Discrete State-Space Propagation: x[k+1] = A*x[k] + B*u[k] *)
FOR iRow := 1 TO 8 DO
    rTempAccum := 0.0;
    FOR iCol := 1 TO 8 DO
        rTempAccum := rTempAccum + (mat_A[iRow, iCol] * x_state[iCol]) + (mat_B[iRow, iCol] * u_act[iCol]);
    END_FOR;
    x_pred[iRow] := rTempAccum;
END_FOR;

(* Kalman Observer Innovation Update: x_obs = x_pred + Ke*(y_meas - C*x_pred) *)
FOR iRow := 1 TO 8 DO
    y_pred[iRow] := x_pred[iRow]; (* Because C is Identity *)
    e_innov[iRow] := y_meas[iRow] - y_pred[iRow];
END_FOR;

FOR iRow := 1 TO 8 DO
    rTempAccum := 0.0;
    FOR iCol := 1 TO 8 DO
        rTempAccum := rTempAccum + (mat_Ke[iRow, iCol] * e_innov[iCol]);
    END_FOR;
    x_obs[iRow] := x_pred[iRow] + rTempAccum;
    x_state[iRow] := x_obs[iRow];
END_FOR;

(* 3.4 Receding-Horizon Model Predictive Control (MPC) Optimization *)
(* Forward Trajectory Prediction across Horizon Np = 3 *)
FOR iIdx := 1 TO 8 DO
    x_horizon[1, iIdx] := x_state[iIdx];
END_FOR;

FOR kStep := 1 TO 3 DO
    FOR iRow := 1 TO 8 DO
        rTempAccum := 0.0;
        FOR iCol := 1 TO 8 DO
            rTempAccum := rTempAccum + (mat_A[iRow, iCol] * x_horizon[kStep, iCol]) + (mat_B[iRow, iCol] * u_act[iCol]);
        END_FOR;
        x_horizon[kStep + 1, iRow] := rTempAccum;
    END_FOR;
END_FOR;

(* Quadratic Cost Computation J *)
rMPC_CurrentCostFunctional_J := 0.0;
FOR kStep := 1 TO 3 DO
    FOR iRow := 1 TO 8 DO
        rTempVar1 := x_horizon[kStep + 1, iRow] - r_ref[iRow];
        rMPC_CurrentCostFunctional_J := rMPC_CurrentCostFunctional_J + (rTempVar1 * mat_Q[iRow, iRow] * rTempVar1);
        rMPC_CurrentCostFunctional_J := rMPC_CurrentCostFunctional_J + (u_act[iRow] * mat_R[iRow, iRow] * u_act[iRow]);
        rTempVar2 := u_act[iRow] - u_prev[iRow];
        rMPC_CurrentCostFunctional_J := rMPC_CurrentCostFunctional_J + (rTempVar2 * mat_S[iRow, iRow] * rTempVar2);
    END_FOR;
END_FOR;

(* Terminal State Penalty *)
FOR iRow := 1 TO 8 DO
    rTempVar1 := x_horizon[4, iRow] - r_ref[iRow];
    rMPC_CurrentCostFunctional_J := rMPC_CurrentCostFunctional_J + (rTempVar1 * mat_P[iRow, iRow] * rTempVar1);
END_FOR;

(* Projected Gradient Descent Optimization Step *)
(* Compute gradient w.r.t actuator commands grad_u = 2*B^T*Q*(x_pred - r) + 2*R*u + 2*S*(u - u_prev) *)
FOR iIdx := 1 TO 8 DO
    rTempAccum := 0.0;
    FOR jIdx := 1 TO 8 DO
        rTempAccum := rTempAccum + (mat_B[jIdx, iIdx] * mat_Q[jIdx, jIdx] * (x_horizon[2, jIdx] - r_ref[jIdx]));
    END_FOR;
    grad_u[iIdx] := (2.0 * rTempAccum) + (2.0 * mat_R[iIdx, iIdx] * u_act[iIdx]) + (2.0 * mat_S[iIdx, iIdx] * (u_act[iIdx] - u_prev[iIdx]));

    (* Actuator Slew Rate Limiting & Bounds Enforcement *)
    du_delta[iIdx] := -rMPC_StepSize * grad_u[iIdx];
    IF du_delta[iIdx] > du_max[iIdx] THEN
        du_delta[iIdx] := du_max[iIdx];
    ELSIF du_delta[iIdx] < -du_max[iIdx] THEN
        du_delta[iIdx] := -du_max[iIdx];
    END_IF;

    u_prev[iIdx] := u_act[iIdx];
    u_act[iIdx] := u_act[iIdx] + du_delta[iIdx];

    (* Physical Saturation Clamping *)
    IF u_act[iIdx] > u_max[iIdx] THEN
        u_act[iIdx] := u_max[iIdx];
    ELSIF u_act[iIdx] < u_min[iIdx] THEN
        u_act[iIdx] := u_min[iIdx];
    END_IF;
END_FOR;

(* 3.5 Dispatch Actuator Commands to System Outputs *)
rBlowerMasterSpeed_pct := u_act[1];
rInternalRecyclePumpVFD_pct := u_act[2];
rCarbonDosePumpDemand_Lph := u_act[3];
rFeCl3DosePumpDemand_Lph := u_act[4];
rMBR_PermeateSuctionPumpVFD_pct := u_act[5];
rRAS_PumpVFD_pct := u_act[6];
rMBR_AirScourBlowerVFD_pct := u_act[7];
rStormDiversionGatePos_pct := u_act[8];

(* 4 x 450 kW Blower Lead-Lag Staging & Vane Modulation *)
rBlower01_SpeedCmd_pct := rBlowerMasterSpeed_pct;
rBlower02_SpeedCmd_pct := rBlowerMasterSpeed_pct;
IF rBlowerMasterSpeed_pct > 65.0 THEN
    rBlower03_SpeedCmd_pct := (rBlowerMasterSpeed_pct - 65.0) / 0.35;
    rBlower04_SpeedCmd_pct := rBlower03_SpeedCmd_pct * 0.85;
ELSE
    rBlower03_SpeedCmd_pct := 0.0;
    rBlower04_SpeedCmd_pct := 0.0;
END_IF;

rBlowerGuideVanesCmd_deg := (rBlowerMasterSpeed_pct / 100.0) * 85.0; (* 0 to 85 degrees *)
bBlowerMasterRunCmd := bMasterEnable AND NOT bPlantEmergencyIsolationActive;"""
    parts.append(phase3_code)

    # 9. PHASE 4: 12-STAGE FINITE STATE MACHINE (FSM)
    phase4_code = """(* ==================================================================================================== *)
(* PHASE 4: MULTI-STAGE 12-STATE OPERATIONAL FINITE STATE MACHINE (FSM)                                 *)
(* ==================================================================================================== *)

rStateTimer_s := rStateTimer_s + rCycleTime_s;
rStateDwellTime_s := rStateTimer_s;
iActiveFSMState := eCurrentState;

(* State Machine Execution *)
CASE eCurrentState OF
    0: (* STATE_PLANT_DRY_WEATHER_BASELOAD *)
        bMBR_PermeateSuctionRunCmd := TRUE;
        bMBR_AirScourPulseCmd := FALSE;
        bStormDiversionGateOpenCmd := FALSE;
        bToxicRetentionGateDivertCmd := FALSE;
        bMBR_CIP_IsolationValveOpen := FALSE;

        rMBR_HarvestTimer_s := rMBR_HarvestTimer_s + rCycleTime_s;

        (* Transitions *)
        IF bPlantEmergencyIsolationActive THEN
            eCurrentState := 11; (* EMERGENCY_ESTOP_BASIN_ISOLATION *)
            rStateTimer_s := 0.0;
        ELSIF rVoted_ToxicSpike_ppm >= rToxicSpikeTripThreshold_ppm THEN
            eCurrentState := 11;
            rStateTimer_s := 0.0;
        ELSIF rVoted_InfluentFlow_m3_h >= rPeakStormFlowThreshold_m3_h OR bStormWeatherOverride THEN
            eCurrentState := 7; (* WET_WEATHER_STORM_FLOW_SURGE *)
            rStateTimer_s := 0.0;
        ELSIF rVoted_ClarifierSludgeBlanket_m >= c_Blanket_Warning_H THEN
            eCurrentState := 8; (* SLUDGE_BLANKET_EMERGENCY_DEPRESS *)
            rStateTimer_s := 0.0;
        ELSIF rMBR_HarvestTimer_s >= c_rMBR_HarvestDuration_s THEN
            eCurrentState := 4; (* MBR_RELAXATION_AIR_SCOUR_PULSE *)
            rStateTimer_s := 0.0;
            rMBR_HarvestTimer_s := 0.0;
        ELSIF rVoted_MBR_TMP_kPa >= c_TMP_Warning_H THEN
            eCurrentState := 5; (* MBR_HYPOCHLORITE_MAINTENANCE_CLEAN *)
            rStateTimer_s := 0.0;
        ELSIF rVoted_AerobicNO3_mg_L >= c_NO3_Warning_H THEN
            eCurrentState := 1; (* ANOXIC_DENITRIFICATION_HOLD *)
            rStateTimer_s := 0.0;
        ELSIF rVoted_InfluentNH4_mg_L >= c_NH4_Warning_H THEN
            eCurrentState := 2; (* AEROBIC_NITRIFICATION_PEAK *)
            rStateTimer_s := 0.0;
        ELSIF rVoted_EffluentPO4_mg_L >= c_PO4_Warning_H THEN
            eCurrentState := 6; (* CHEMICAL_PHOSPHORUS_PEAK_TRIM *)
            rStateTimer_s := 0.0;
        END_IF;

    1: (* STATE_ANOXIC_DENITRIFICATION_HOLD *)
        (* Pacing Internal Recycle and Methanol for Denitrification *)
        rInternalRecyclePumpVFD_pct := 85.0;
        rCarbonDosePumpDemand_Lph := rCarbonDosePumpDemand_Lph + 15.0;
        IF rCarbonDosePumpDemand_Lph > 220.0 THEN
            rCarbonDosePumpDemand_Lph := 220.0;
        END_IF;

        IF bPlantEmergencyIsolationActive THEN
            eCurrentState := 11;
            rStateTimer_s := 0.0;
        ELSIF rVoted_AerobicNO3_mg_L <= 4.00 AND rStateTimer_s > 120.0 THEN
            eCurrentState := 0; (* Return to baseload *)
            rStateTimer_s := 0.0;
        END_IF;

    2: (* STATE_AEROBIC_NITRIFICATION_PEAK *)
        (* Elevate DO setpoint to boost nitrification *)
        rTargetDO_Setpoint_mg_L := 2.50;
        rBlowerMasterSpeed_pct := rBlowerMasterSpeed_pct + 10.0;
        IF rBlowerMasterSpeed_pct > 100.0 THEN
            rBlowerMasterSpeed_pct := 100.0;
        END_IF;

        IF bPlantEmergencyIsolationActive THEN
            eCurrentState := 11;
            rStateTimer_s := 0.0;
        ELSIF rVoted_InfluentNH4_mg_L <= 1.20 AND rStateTimer_s > 180.0 THEN
            rTargetDO_Setpoint_mg_L := 2.00;
            eCurrentState := 0;
            rStateTimer_s := 0.0;
        END_IF;

    3: (* STATE_MBR_NORMAL_PERMEATE_HARVEST *)
        bMBR_PermeateSuctionRunCmd := TRUE;
        bMBR_AirScourPulseCmd := FALSE;
        rMBR_HarvestTimer_s := rMBR_HarvestTimer_s + rCycleTime_s;

        IF bPlantEmergencyIsolationActive THEN
            eCurrentState := 11;
            rStateTimer_s := 0.0;
        ELSIF rMBR_HarvestTimer_s >= c_rMBR_HarvestDuration_s THEN
            eCurrentState := 4; (* MBR_RELAXATION_AIR_SCOUR_PULSE *)
            rStateTimer_s := 0.0;
            rMBR_HarvestTimer_s := 0.0;
        END_IF;

    4: (* STATE_MBR_RELAXATION_AIR_SCOUR_PULSE *)
        (* Halt permeate pump, pulse air scour blower to 100% to strip cake *)
        bMBR_PermeateSuctionRunCmd := FALSE;
        bMBR_AirScourPulseCmd := TRUE;
        rMBR_AirScourBlowerVFD_pct := 100.0;
        rMBR_RelaxationTimer_s := rMBR_RelaxationTimer_s + rCycleTime_s;

        IF bPlantEmergencyIsolationActive THEN
            eCurrentState := 11;
            rStateTimer_s := 0.0;
        ELSIF rMBR_RelaxationTimer_s >= c_rMBR_RelaxationDuration_s THEN
            bMBR_AirScourPulseCmd := FALSE;
            rMBR_RelaxationTimer_s := 0.0;
            eCurrentState := 0; (* Return to Baseload *)
            rStateTimer_s := 0.0;
        END_IF;

    5: (* STATE_MBR_HYPOCHLORITE_MAINTENANCE_CLEAN *)
        (* Isolate permeate line and perform low-dose NaOCl backwash *)
        bMBR_PermeateSuctionRunCmd := FALSE;
        bMBR_CIP_IsolationValveOpen := TRUE;
        bMBR_BackwashPumpRunCmd := TRUE;
        rMBR_CIP_StageTimer_s := rMBR_CIP_StageTimer_s + rCycleTime_s;

        IF bPlantEmergencyIsolationActive THEN
            eCurrentState := 11;
            rStateTimer_s := 0.0;
        ELSIF rMBR_CIP_StageTimer_s >= c_rMBR_CIP_Duration_s THEN
            bMBR_CIP_IsolationValveOpen := FALSE;
            bMBR_BackwashPumpRunCmd := FALSE;
            rMBR_CIP_StageTimer_s := 0.0;
            rCakeResistance_Rc := 0.15E12; (* Reset cake resistance after chemical clean *)
            rPoreResistance_Rp := rPoreResistance_Rp * 0.65;
            eCurrentState := 0;
            rStateTimer_s := 0.0;
        END_IF;

    6: (* STATE_CHEMICAL_PHOSPHORUS_PEAK_TRIM *)
        (* Boost Ferric Chloride dosing to precipitate phosphorus *)
        rFeCl3DosePumpDemand_Lph := rFeCl3DosePumpDemand_Lph + 25.0;
        IF rFeCl3DosePumpDemand_Lph > 160.0 THEN
            rFeCl3DosePumpDemand_Lph := 160.0;
        END_IF;

        IF bPlantEmergencyIsolationActive THEN
            eCurrentState := 11;
            rStateTimer_s := 0.0;
        ELSIF rVoted_EffluentPO4_mg_L <= 0.10 AND rStateTimer_s > 150.0 THEN
            eCurrentState := 0;
            rStateTimer_s := 0.0;
        END_IF;

    7: (* STATE_WET_WEATHER_STORM_FLOW_SURGE *)
        (* Open storm diversion gate to retention basin and pace clarifiers *)
        bStormDiversionGateOpenCmd := TRUE;
        rStormDiversionGatePos_pct := 100.0;
        rRAS_PumpVFD_pct := 90.0;
        rStormDiversionTimer_s := rStormDiversionTimer_s + rCycleTime_s;

        IF bPlantEmergencyIsolationActive THEN
            eCurrentState := 11;
            rStateTimer_s := 0.0;
        ELSIF rVoted_InfluentFlow_m3_h < (rPeakStormFlowThreshold_m3_h * 0.85) AND NOT bStormWeatherOverride THEN
            bStormDiversionGateOpenCmd := FALSE;
            rStormDiversionGatePos_pct := 0.0;
            rStormDiversionTimer_s := 0.0;
            eCurrentState := 0;
            rStateTimer_s := 0.0;
        END_IF;

    8: (* STATE_SLUDGE_BLANKET_EMERGENCY_DEPRESS *)
        (* Maximize RAS return pumping to lower clarifier sludge blanket *)
        rRAS_PumpVFD_pct := 100.0;
        bClarifierWasteSludgeValveCmd := TRUE;

        IF bPlantEmergencyIsolationActive THEN
            eCurrentState := 11;
            rStateTimer_s := 0.0;
        ELSIF rVoted_ClarifierSludgeBlanket_m <= 1.40 AND rStateTimer_s > 60.0 THEN
            bClarifierWasteSludgeValveCmd := FALSE;
            eCurrentState := 0;
            rStateTimer_s := 0.0;
        END_IF;

    9: (* STATE_CO_DIGESTER_BIOGAS_RECIRCULATION *)
        (* Co-digestion and sludge thickening coordination *)
        IF bPlantEmergencyIsolationActive THEN
            eCurrentState := 11;
            rStateTimer_s := 0.0;
        ELSIF rStateTimer_s > 300.0 THEN
            eCurrentState := 0;
            rStateTimer_s := 0.0;
        END_IF;

    10: (* STATE_EFFLUENT_DISINFECTION_HOLD *)
        (* Effluent polishing hold *)
        IF bPlantEmergencyIsolationActive THEN
            eCurrentState := 11;
            rStateTimer_s := 0.0;
        ELSIF rStateTimer_s > 60.0 THEN
            eCurrentState := 0;
            rStateTimer_s := 0.0;
        END_IF;

    11: (* STATE_EMERGENCY_ESTOP_BASIN_ISOLATION *)
        (* Immediate fail-safe isolation *)
        bBlowerMasterRunCmd := FALSE;
        rBlowerMasterSpeed_pct := 0.0;
        bMBR_PermeateSuctionRunCmd := FALSE;
        rMBR_PermeateSuctionPumpVFD_pct := 0.0;
        rInternalRecyclePumpVFD_pct := 0.0;
        rCarbonDosePumpDemand_Lph := 0.0;
        rFeCl3DosePumpDemand_Lph := 0.0;
        bMBR_AirScourPulseCmd := FALSE;
        bPlantEmergencyIsolationActive := TRUE;

        IF rVoted_ToxicSpike_ppm >= rToxicSpikeTripThreshold_ppm THEN
            bToxicRetentionGateDivertCmd := TRUE;
        END_IF;

        IF bAlarmResetPulse AND bSafetyCircuitOK AND (rVoted_ToxicSpike_ppm < 0.10) THEN
            bPlantEmergencyIsolationActive := FALSE;
            bToxicRetentionGateDivertCmd := FALSE;
            eCurrentState := 0; (* Reset to baseload *)
            rStateTimer_s := 0.0;
        END_IF;
END_CASE;"""
    parts.append(phase4_code)

    # 10. PHASE 5: ISA-18.2 ALARMS & DIAGNOSTIC WORD PACKING
    phase5_code = """(* ==================================================================================================== *)
(* PHASE 5: ISA-18.2 ALARM ENGINE & DIAGNOSTIC STATUS WORD PACKING                                      *)
(* ==================================================================================================== *)

(* 5.1 ISA-18.2 Analog Alarm Hierarchy with Deadband Hysteresis *)
(* Dissolved Oxygen Alarms *)
IF rVoted_AerobicDO_mg_L <= c_DO_Trip_LL THEN
    bAlarm_DO_Depletion_LL := TRUE;
ELSIF rVoted_AerobicDO_mg_L > (c_DO_Trip_LL + rDeadband_DO) THEN
    bAlarm_DO_Depletion_LL := FALSE;
END_IF;

IF rVoted_AerobicDO_mg_L <= c_DO_Warning_L THEN
    bAlarm_DO_Low_L := TRUE;
ELSIF rVoted_AerobicDO_mg_L > (c_DO_Warning_L + rDeadband_DO) THEN
    bAlarm_DO_Low_L := FALSE;
END_IF;

IF rVoted_AerobicDO_mg_L >= c_DO_Warning_H THEN
    bAlarm_DO_High_H := TRUE;
ELSIF rVoted_AerobicDO_mg_L < (c_DO_Warning_H - rDeadband_DO) THEN
    bAlarm_DO_High_H := FALSE;
END_IF;

IF rVoted_AerobicDO_mg_L >= c_DO_Trip_HH THEN
    bAlarm_DO_HighHigh_HH := TRUE;
ELSIF rVoted_AerobicDO_mg_L < (c_DO_Trip_HH - rDeadband_DO) THEN
    bAlarm_DO_HighHigh_HH := FALSE;
END_IF;

(* Ammonia & Nitrate Alarms *)
IF rVoted_InfluentNH4_mg_L >= c_NH4_Trip_HH THEN
    bAlarm_Ammonia_HighHigh_HH := TRUE;
ELSIF rVoted_InfluentNH4_mg_L < (c_NH4_Trip_HH - rDeadband_Nutrient) THEN
    bAlarm_Ammonia_HighHigh_HH := FALSE;
END_IF;

IF rVoted_AerobicNO3_mg_L >= c_NO3_Trip_HH THEN
    bAlarm_Nitrate_HighHigh_HH := TRUE;
ELSIF rVoted_AerobicNO3_mg_L < (c_NO3_Trip_HH - rDeadband_Nutrient) THEN
    bAlarm_Nitrate_HighHigh_HH := FALSE;
END_IF;

(* Phosphate Discharge Breach Alarm *)
IF rVoted_EffluentPO4_mg_L >= c_PO4_Trip_HH THEN
    bAlarm_EffluentPO4_HighHigh_HH := TRUE;
ELSIF rVoted_EffluentPO4_mg_L < (c_PO4_Trip_HH - 0.02) THEN
    bAlarm_EffluentPO4_HighHigh_HH := FALSE;
END_IF;

(* MBR Transmembrane Pressure Cavitation Alarms *)
IF rVoted_MBR_TMP_kPa >= c_TMP_Trip_HH THEN
    bAlarm_MBR_TMP_HighHigh_HH := TRUE;
ELSIF rVoted_MBR_TMP_kPa < (c_TMP_Trip_HH - rDeadband_Pressure) THEN
    bAlarm_MBR_TMP_HighHigh_HH := FALSE;
END_IF;

IF rVoted_MBR_TMP_kPa >= c_TMP_Warning_H THEN
    bAlarm_MBR_TMP_High_H := TRUE;
ELSIF rVoted_MBR_TMP_kPa < (c_TMP_Warning_H - rDeadband_Pressure) THEN
    bAlarm_MBR_TMP_High_H := FALSE;
END_IF;

(* Clarifier Sludge Blanket Washout Alarms *)
IF rVoted_ClarifierSludgeBlanket_m >= c_Blanket_Trip_HH THEN
    bAlarm_SludgeBlanket_Washout_HH := TRUE;
ELSIF rVoted_ClarifierSludgeBlanket_m < (c_Blanket_Trip_HH - rDeadband_Blanket) THEN
    bAlarm_SludgeBlanket_Washout_HH := FALSE;
END_IF;

(* Blower Surge Margin Protection Line *)
IF (rVoted_HeaderPressure_kPa / (rVoted_BlowerAirFlow_Nm3_h * 0.0016 + 1.0)) > c_BlowerSurgeRatio_Min THEN
    bAlarm_BlowerSurge_Risk_HH := TRUE;
ELSE
    bAlarm_BlowerSurge_Risk_HH := FALSE;
END_IF;

(* Influent Toxic Spill Immediate Alarm *)
IF rVoted_ToxicSpike_ppm >= c_Toxic_Trip_HH THEN
    bAlarm_ToxicSpill_Ingress_HH := TRUE;
    bToxicRetentionGateDivertCmd := TRUE;
ELSE
    bAlarm_ToxicSpill_Ingress_HH := FALSE;
END_IF;

(* 5.2 Critical Safety Trip Latches *)
IF bAlarm_DO_Depletion_LL OR bAlarm_MBR_TMP_HighHigh_HH OR bAlarm_SludgeBlanket_Washout_HH OR bAlarm_ToxicSpill_Ingress_HH THEN
    bPlantEmergencyIsolationActive := TRUE;
END_IF;

IF bAlarmResetPulse AND bSafetyCircuitOK THEN
    bAlarm_DO_Depletion_LL := FALSE;
    bAlarm_MBR_TMP_HighHigh_HH := FALSE;
    bAlarm_SludgeBlanket_Washout_HH := FALSE;
    bAlarm_ToxicSpill_Ingress_HH := FALSE;
END_IF;

(* 5.3 Diagnostic Status Word 01: 2oo3 TMR Sensor Health & Skew Bits *)
wDiagnosticWord01_Sensors := 16#0000;
IF bFault_NH4_A OR bFault_NH4_B OR bFault_NH4_C THEN wDiagnosticWord01_Sensors := wDiagnosticWord01_Sensors OR 16#0001; END_IF;
IF bFault_COD_A OR bFault_COD_B OR bFault_COD_C THEN wDiagnosticWord01_Sensors := wDiagnosticWord01_Sensors OR 16#0002; END_IF;
IF bFault_InfFlow_A OR bFault_InfFlow_B OR bFault_InfFlow_C THEN wDiagnosticWord01_Sensors := wDiagnosticWord01_Sensors OR 16#0004; END_IF;
IF bFault_DO_A OR bFault_DO_B OR bFault_DO_C THEN wDiagnosticWord01_Sensors := wDiagnosticWord01_Sensors OR 16#0008; END_IF;
IF bFault_NO3_A OR bFault_NO3_B OR bFault_NO3_C THEN wDiagnosticWord01_Sensors := wDiagnosticWord01_Sensors OR 16#0010; END_IF;
IF bFault_HeaderPres_A OR bFault_HeaderPres_B OR bFault_HeaderPres_C THEN wDiagnosticWord01_Sensors := wDiagnosticWord01_Sensors OR 16#0020; END_IF;
IF bFault_AirFlow_A OR bFault_AirFlow_B OR bFault_AirFlow_C THEN wDiagnosticWord01_Sensors := wDiagnosticWord01_Sensors OR 16#0040; END_IF;
IF bFault_ORP_A OR bFault_ORP_B OR bFault_ORP_C THEN wDiagnosticWord01_Sensors := wDiagnosticWord01_Sensors OR 16#0080; END_IF;
IF bFault_IRFlow_A OR bFault_IRFlow_B OR bFault_IRFlow_C THEN wDiagnosticWord01_Sensors := wDiagnosticWord01_Sensors OR 16#0100; END_IF;
IF bFault_Carbon_A OR bFault_Carbon_B OR bFault_Carbon_C THEN wDiagnosticWord01_Sensors := wDiagnosticWord01_Sensors OR 16#0200; END_IF;
IF bFault_PO4_A OR bFault_PO4_B OR bFault_PO4_C THEN wDiagnosticWord01_Sensors := wDiagnosticWord01_Sensors OR 16#0400; END_IF;
IF bFault_FeCl3_A OR bFault_FeCl3_B OR bFault_FeCl3_C THEN wDiagnosticWord01_Sensors := wDiagnosticWord01_Sensors OR 16#0800; END_IF;
IF bFault_TMP_A OR bFault_TMP_B OR bFault_TMP_C THEN wDiagnosticWord01_Sensors := wDiagnosticWord01_Sensors OR 16#1000; END_IF;
IF bFault_Blanket_A OR bFault_Blanket_B OR bFault_Blanket_C THEN wDiagnosticWord01_Sensors := wDiagnosticWord01_Sensors OR 16#2000; END_IF;
IF bFault_RASFlow_A OR bFault_RASFlow_B OR bFault_RASFlow_C THEN wDiagnosticWord01_Sensors := wDiagnosticWord01_Sensors OR 16#4000; END_IF;
IF bFault_Toxic_A OR bFault_Toxic_B OR bFault_Toxic_C THEN wDiagnosticWord01_Sensors := wDiagnosticWord01_Sensors OR 16#8000; END_IF;

(* 5.4 Diagnostic Status Word 02: Actuators, Blowers & Dosing Pumps *)
wDiagnosticWord02_Actuators := 16#0000;
IF bBlowerMasterRunCmd THEN wDiagnosticWord02_Actuators := wDiagnosticWord02_Actuators OR 16#0001; END_IF;
IF bMBR_PermeateSuctionRunCmd THEN wDiagnosticWord02_Actuators := wDiagnosticWord02_Actuators OR 16#0002; END_IF;
IF bMBR_AirScourPulseCmd THEN wDiagnosticWord02_Actuators := wDiagnosticWord02_Actuators OR 16#0004; END_IF;
IF bMBR_BackwashPumpRunCmd THEN wDiagnosticWord02_Actuators := wDiagnosticWord02_Actuators OR 16#0008; END_IF;
IF bMBR_CIP_IsolationValveOpen THEN wDiagnosticWord02_Actuators := wDiagnosticWord02_Actuators OR 16#0010; END_IF;
IF bStormDiversionGateOpenCmd THEN wDiagnosticWord02_Actuators := wDiagnosticWord02_Actuators OR 16#0020; END_IF;
IF bToxicRetentionGateDivertCmd THEN wDiagnosticWord02_Actuators := wDiagnosticWord02_Actuators OR 16#0040; END_IF;
IF bDiffuserBumpPurgeValveCmd THEN wDiagnosticWord02_Actuators := wDiagnosticWord02_Actuators OR 16#0080; END_IF;
IF bAlarm_BlowerSurge_Risk_HH THEN wDiagnosticWord02_Actuators := wDiagnosticWord02_Actuators OR 16#0100; END_IF;
IF bAlarm_DiffuserFouling_Warning THEN wDiagnosticWord02_Actuators := wDiagnosticWord02_Actuators OR 16#0200; END_IF;

(* 5.5 Diagnostic Status Word 03: Water Quality & Regulatory Compliance *)
wDiagnosticWord03_Quality := 16#0000;
IF bAlarm_DO_Depletion_LL THEN wDiagnosticWord03_Quality := wDiagnosticWord03_Quality OR 16#0001; END_IF;
IF bAlarm_DO_Low_L THEN wDiagnosticWord03_Quality := wDiagnosticWord03_Quality OR 16#0002; END_IF;
IF bAlarm_DO_High_H THEN wDiagnosticWord03_Quality := wDiagnosticWord03_Quality OR 16#0004; END_IF;
IF bAlarm_DO_HighHigh_HH THEN wDiagnosticWord03_Quality := wDiagnosticWord03_Quality OR 16#0008; END_IF;
IF bAlarm_Ammonia_High_H THEN wDiagnosticWord03_Quality := wDiagnosticWord03_Quality OR 16#0010; END_IF;
IF bAlarm_Ammonia_HighHigh_HH THEN wDiagnosticWord03_Quality := wDiagnosticWord03_Quality OR 16#0020; END_IF;
IF bAlarm_Nitrate_High_H THEN wDiagnosticWord03_Quality := wDiagnosticWord03_Quality OR 16#0040; END_IF;
IF bAlarm_Nitrate_HighHigh_HH THEN wDiagnosticWord03_Quality := wDiagnosticWord03_Quality OR 16#0080; END_IF;
IF bAlarm_EffluentPO4_High_H THEN wDiagnosticWord03_Quality := wDiagnosticWord03_Quality OR 16#0100; END_IF;
IF bAlarm_EffluentPO4_HighHigh_HH THEN wDiagnosticWord03_Quality := wDiagnosticWord03_Quality OR 16#0200; END_IF;
IF bAlarm_MBR_TMP_High_H THEN wDiagnosticWord03_Quality := wDiagnosticWord03_Quality OR 16#0400; END_IF;
IF bAlarm_MBR_TMP_HighHigh_HH THEN wDiagnosticWord03_Quality := wDiagnosticWord03_Quality OR 16#0800; END_IF;
IF bAlarm_SludgeBlanket_High_H THEN wDiagnosticWord03_Quality := wDiagnosticWord03_Quality OR 16#1000; END_IF;
IF bAlarm_SludgeBlanket_Washout_HH THEN wDiagnosticWord03_Quality := wDiagnosticWord03_Quality OR 16#2000; END_IF;
IF bAlarm_ToxicSpill_Ingress_HH THEN wDiagnosticWord03_Quality := wDiagnosticWord03_Quality OR 16#4000; END_IF;

(* 5.6 Diagnostic Status Word 04: Active FSM State Code & Safety Status *)
wDiagnosticWord04_SafetyFSM := INT_TO_WORD(eCurrentState) AND 16#000F;
IF bSafetyCircuitOK THEN wDiagnosticWord04_SafetyFSM := wDiagnosticWord04_SafetyFSM OR 16#0010; END_IF;
IF bPlantEmergencyIsolationActive THEN wDiagnosticWord04_SafetyFSM := wDiagnosticWord04_SafetyFSM OR 16#0020; END_IF;
IF bStormWeatherOverride THEN wDiagnosticWord04_SafetyFSM := wDiagnosticWord04_SafetyFSM OR 16#0040; END_IF;
IF bManualOverrideMode THEN wDiagnosticWord04_SafetyFSM := wDiagnosticWord04_SafetyFSM OR 16#0080; END_IF;

(* 5.7 Continuous Running Integrators (Daily Volume & Electrical Energy) *)
rCurrentDailyTreatedVolume_m3 := rCurrentDailyTreatedVolume_m3 + ((rVoted_InfluentFlow_m3_h * rCycleTime_s) / 3600.0);
rCurrentDailyBlowerEnergy_kWh := rCurrentDailyBlowerEnergy_kWh + (((rBlowerMasterSpeed_pct / 100.0) * 1800.0 * rCycleTime_s) / 3600.0);
IF rCurrentDailyTreatedVolume_m3 > 10.0 THEN
    rPlantEnergySpecific_kWh_per_m3 := rCurrentDailyBlowerEnergy_kWh / rCurrentDailyTreatedVolume_m3;
ELSE
    rPlantEnergySpecific_kWh_per_m3 := 0.22; (* Baseline 0.22 kWh/m3 *)
END_IF;

END_FUNCTION_BLOCK"""
    parts.append(phase5_code)

    full_code = "\n\n".join(parts)
    return full_code

if __name__ == "__main__":
    code = build_iec_code()
    print(f"Generated code length: {len(code)} characters, {code.count(chr(10))} lines")
    issues = verify_st_syntax(code)
    if issues:
        print("Syntax issues detected:")
        for issue in issues:
            print(f" - {issue}")
    else:
        print("Syntax verification: 100% PASSED!")
