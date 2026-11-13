# Complete generator for Lumina Biopharma TFF Dataset
import os, sys, json, uuid, re

def generate():
    print("Generating FB_Pharma_Bioprocess_TFF_Ultrafiltration_Diafiltration...")
    
    # We will assemble the Structured Text in parts
    st_lines = []
    
    # Header
    st_lines.append("""FUNCTION_BLOCK FB_Pharma_Bioprocess_TFF_Ultrafiltration_Diafiltration
(*
====================================================================================================
LUMINA CYBER-PHYSICAL AUTOMATION KERNEL - IEC 61131-3 STRUCTURED TEXT
SECTOR        : BIOPHARMACEUTICALS & LIFE SCIENCES (TIER-1 CGMP COMMERCIAL DRUG SUBSTANCE PROCESSING)
SYSTEM        : CONTINUOUS TANGENTIAL FLOW FILTRATION (TFF) / CROSS-FLOW ULTRAFILTRATION &
                DIAFILTRATION (UF/DF) CASSETTE SKID FOR MONOCLONAL ANTIBODY (mAb) PURIFICATION
APPLICATION   : THERAPEUTIC RECOMBINANT HUMANIZED IgG1/IgG4 MONOCLONAL ANTIBODY CONCENTRATION AND
                FORMULATION BUFFER EXCHANGE (TARGET FINAL CONCENTRATION: 120.0 - 180.0 [g/L])
MEMBRANE TECH : 30 kDa REGENERATED CELLULOSE (RC) SCREEN-CHANNEL CASSETTES (TOTAL AREA: 10.0 [m2])
SAMPLE PERIOD : Ts = 0.010 [s] (10.0 [ms] REAL-TIME DETERMINISTIC TASK CYCLE)

CYBER-PHYSICAL ARCHITECTURAL SUBSYSTEMS:
  1. FIRST-PRINCIPLES FILM-THEORY 8-STATE DISCRETE CYBER-PHYSICAL STATE-SPACE MODEL
     - x1: Transmembrane Pressure TMP [bar] (Operating: 0.50 - 3.20 [bar], Fast Trip: 3.50 [bar])
     - x2: Permeate Volumetric Flux J_perm [L/m2/h LMH] (Darcy-Starling Hydraulic Resistance Model)
     - x3: Retentate Monoclonal Antibody Bulk Concentration C_ret [g/L] (Mass Balance & Rejection)
     - x4: Membrane Concentration Polarization Gel Layer Hydraulic Resistance Rg [10^11 m-1]
     - x5: Cassette Retentate Flow Channel Wall Shear Rate gamma_w [s-1] (Hydrodynamic Shear Model)
     - x6: Continuous Constant-Volume Diafiltration Buffer Volume Counter DV [-] (Target: 7.0 DV)
     - x7: Retentate Recirculation Loop Process Temperature T_ret [deg C] (Viscous Heat Balance)
     - x8: Diafiltration Continuous Sump Tank Mass Balance Scale Weight Deviation delta_M_sump [g]
  2. DISCRETE FULL SYSTEM MATRICES (8x8 A, 8x6 B, 6x8 C, 6x6 D) & 8x6 STEADY-STATE LUENBERGER OBSERVER
     - Linearized at nominal bioprocess operating trajectory with continuous innovation filtering
  3. RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) WITH PROJECTED GRADIENT DESCENT (PGD)
     - Prediction Horizon N = 5 steps, 6 unrolled iterations of PGD
     - Decoupled TMP and Retentate Wall Shear Rate feedforward decoupling algorithm
     - Physical actuator saturation clamping and dynamic slew-rate limit enforcement
  4. 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING SUITE ACROSS 5 CRITICAL CHANNELS
     - PT_FEED_101A/B/C: Sanitary Diaphragm Pressure Transmitters Feed Line [bar]
     - PT_RET_201A/B/C: Sanitary Diaphragm Pressure Transmitters Retentate Line [bar]
     - PT_PERM_301A/B/C: Sanitary Diaphragm Pressure Transmitters Permeate Line [bar]
     - AT_UV_401A/B/C: In-Line Dual-Wavelength UV-Vis 280 nm Protein Concentration Photometers [g/L]
     - FT_FEED_501A/B/C: Sanitary Coriolis Mass Flowmeters Feed Recirculation Line [L/h]
     - Dual-stage discrepancy integration timers (100 [ms] persistence threshold) & bumpless degradation
  5. DETERMINISTIC 14-STAGE BIOPROCESS PRODUCTION FINITE STATE MACHINE (FSM, STATES 0 TO 13)
     - State 0: SANITARY_STANDBY_AND_INTEGRITY_CHECK (N2 Forward Flow Diffusion Air Hold Test)
     - State 1: WFI_FLUSH_AND_INITIAL_NWP_BASE_WATER_TEST (Pre-Use Baseline Water Permeability)
     - State 2: EQUILIBRATION_BUFFER_CONDITIONING_PRIME (Formulation Buffer Priming & UV Zero)
     - State 3: PROTEIN_BULK_FEED_INTRODUCTION_RAMP (Controlled Shear Feed Loading Ramp)
     - State 4: ULTRAFILTRATION_CONCENTRATION_PHASE_1 (Bulk Concentration to 60.0 [g/L])
     - State 5: AUTOMATED_CONSTANT_VOLUME_DIAFILTRATION (7.0 Diafiltration Volumes Buffer Exchange)
     - State 6: ULTRAFILTRATION_FINAL_TARGET_CONCENTRATION (Final Concentration to 150.0 [g/L])
     - State 7: PRODUCT_CHILLDOWN_AND_STABILIZATION (Cold Jacket Control to 4.0 [deg C])
     - State 8: RETENTATE_RECOVERY_DRAIN_AND_WFI_CHASE (Product Displacement Harvest Yield > 99%)
     - State 9: AIR_BLOWDOWN_FLUID_RECOVERY_CYCLE (Low-Pressure Sterile N2 Recovery Push)
     - State 10: CAUSTIC_CIP_MEMBRANE_CLEANING_RECIRCULATION (0.5M NaOH at 45.0 [deg C] Wash)
     - State 11: POST_CIP_NWP_MEMBRANE_RECOVERY_EVALUATION (Membrane Flux Recovery >= 90.0%)
     - State 12: PRESERVATIVE_STORAGE_FLUSH (0.1M NaOH Cassette Preservation Fill & Seal)
     - State 13: EMERGENCY_OVERPRESSURE_RUPTURE_DISC_INTERLOCK (Cat-4 Fast Hydraulic Trip)
  6. ISA-18.2 MULTI-TIER PROCESS ALARM ENGINE & 32-BIT BIT-PACKED TELEMETRY DIAGNOSTICS
     - 4-Tier Limits (HH, H, L, LL) with deadband clearance hysteresis for TMP, Flux, Temp, Shear, Sump
     - Sub-10ms Fast Overpressure Pump Cutoff Trip for Membrane Cassette Burst Protection
     - Bit-packed DWORD diagnostic telemetry: dwStatusWord1, dwStatusWord2, dwAlarmWord1, dwAlarmWord2, dwFirstOutWord
====================================================================================================
*)""")

    # VAR_INPUT
    st_lines.append("""VAR_INPUT
    (* Master Supervisory Execution & Permissive Commands *)
    bEnable                         : BOOL;         (* Master Function Block Execution Enable Permissive [-] *)
    bAutoCycleStart                 : BOOL;         (* Automatic Sequence Cycle Start Pushbutton Trigger [-] *)
    bCycleAbort                     : BOOL;         (* Controlled Sequence Abort and Cassette Rinse Trigger [-] *)
    bEmergencyStop                  : BOOL;         (* Dual-Channel Cat-4 Hardwired Emergency Stop Circuit Interlock [-] *)
    bResetFault                     : BOOL;         (* Master System Fault Reset and Safety Latch Clear Pushbutton [-] *)
    bAckAlarm                       : BOOL;         (* ISA-18.2 Process Alarm Acknowledge Command [-] *)
    bManualMode                     : BOOL;         (* Manual Maintenance Jog and Calibration Override Permissive [-] *)
    bPauseCycle                     : BOOL;         (* Process Recirculation Hold / Cycle Pause Request [-] *)
    bIntegrityTestStart             : BOOL;         (* Cassette Pre-Use Forward Flow Air Diffusion Integrity Test Start [-] *)
    bNWPTestStart                   : BOOL;         (* Normalized Water Permeability (NWP) Quality Benchmark Test Start [-] *)
    bCIPStart                       : BOOL;         (* Automated Caustic Clean-In-Place (CIP) Sequence Trigger [-] *)
    bStorageFlushStart              : BOOL;         (* Preservative Caustic / Sanitizing Storage Flush Trigger [-] *)

    (* Channel Group 1: Feed Line Diaphragm Pressure Transmitters (2oo3 TMR) *)
    rPT_Feed_101A_bar               : REAL;         (* Sanitary Diaphragm Pressure Transmitter 101A Feed Line [bar] *)
    rPT_Feed_101B_bar               : REAL;         (* Sanitary Diaphragm Pressure Transmitter 101B Feed Line [bar] *)
    rPT_Feed_101C_bar               : REAL;         (* Sanitary Diaphragm Pressure Transmitter 101C Feed Line [bar] *)

    (* Channel Group 2: Retentate Line Diaphragm Pressure Transmitters (2oo3 TMR) *)
    rPT_Ret_201A_bar                : REAL;         (* Sanitary Diaphragm Pressure Transmitter 201A Retentate Line [bar] *)
    rPT_Ret_201B_bar                : REAL;         (* Sanitary Diaphragm Pressure Transmitter 201A Retentate Line [bar] *)
    rPT_Ret_201C_bar                : REAL;         (* Sanitary Diaphragm Pressure Transmitter 201A Retentate Line [bar] *)

    (* Channel Group 3: Permeate Line Diaphragm Pressure Transmitters (2oo3 TMR) *)
    rPT_Perm_301A_bar               : REAL;         (* Sanitary Diaphragm Pressure Transmitter 301A Permeate Line [bar] *)
    rPT_Perm_301B_bar               : REAL;         (* Sanitary Diaphragm Pressure Transmitter 301B Permeate Line [bar] *)
    rPT_Perm_301C_bar               : REAL;         (* Sanitary Diaphragm Pressure Transmitter 301C Permeate Line [bar] *)

    (* Channel Group 4: Inline Flow-Cell UV-Vis 280 nm Protein Concentration Photometers (2oo3 TMR) *)
    rAT_UV_401A_gL                  : REAL;         (* Inline Dual-Wavelength UV-Vis Photometer 401A Protein Conc [g/L] *)
    rAT_UV_401B_gL                  : REAL;         (* Inline Dual-Wavelength UV-Vis Photometer 401B Protein Conc [g/L] *)
    rAT_UV_401C_gL                  : REAL;         (* Inline Dual-Wavelength UV-Vis Photometer 401C Protein Conc [g/L] *)

    (* Channel Group 5: Feed Line Sanitary Coriolis Mass Flowmeters (2oo3 TMR) *)
    rFT_Feed_501A_Lh                : REAL;         (* Feed Line Sanitary Coriolis Mass Flowmeter 501A [L/h] *)
    rFT_Feed_501B_Lh                : REAL;         (* Feed Line Sanitary Coriolis Mass Flowmeter 501B [L/h] *)
    rFT_Feed_501C_Lh                : REAL;         (* Feed Line Sanitary Coriolis Mass Flowmeter 501C [L/h] *)

    (* Auxiliary Process Transducers & Analytical Instrumentation *)
    rFT_Perm_Flow_Lh                : REAL;         (* Permeate Line Magnetic / Ultrasonic Flow Transmitter [L/h] *)
    rFT_Buffer_Flow_Lh              : REAL;         (* Diafiltration Buffer Feed Line Micro-Flowmeter [L/h] *)
    rTT_Ret_Temp_degC               : REAL;         (* Retentate Recirculation Loop Sanitary 4-Wire RTD PT100 [deg C] *)
    rTT_Feed_Temp_degC              : REAL;         (* Feed Supply Manifold Sanitary 4-Wire RTD PT100 [deg C] *)
    rTT_Perm_Temp_degC              : REAL;         (* Permeate Discharge Manifold Sanitary RTD PT100 [deg C] *)
    rTT_GlycolSupply_degC           : REAL;         (* Heat Exchanger Chiller Glycol Supply Temperature Sensor [deg C] *)
    rWT_RecircTank_kg               : REAL;         (* Retentate Recirculation Vessel Load Cell Scale Gross Mass [kg] *)
    rWT_BufferScale_kg              : REAL;         (* Diafiltration Formulation Buffer Sump Load Cell Gross Mass [kg] *)
    rWT_PermeateScale_kg            : REAL;         (* Permeate Collection Carboy Load Cell Scale Mass [kg] *)
    rCT_Ret_Conductivity_mScm       : REAL;         (* Retentate Loop Sanitary 4-Electrode Toroidal Conductivity [mS/cm] *)
    rCT_Perm_Conductivity_mScm      : REAL;         (* Permeate Line Toroidal Conductivity Transmitter [mS/cm] *)
    rpH_Ret_Sensor_pH               : REAL;         (* Retentate Line Glassless ISFET Sanitary pH Sensor [pH] *)
    rPDT_AirDiff_Pressure_bar       : REAL;         (* Pre-Use Integrity Air Diffusion Hold Differential Pressure [bar] *)
    bRuptureDisc_Burst_Sensor       : BOOL;         (* Sanitary Rupture Disc Burst Indicating Circuit Contact [-] *)
    bLevel_High_RecircTank          : BOOL;         (* Retentate Vessel High-Level Tuning Fork Limit Switch [-] *)
    bLevel_Low_RecircTank           : BOOL;         (* Retentate Vessel Low-Low Dry-Run Interlock Level Switch [-] *)

    (* Bioprocess Target Recipes, Geometric Constants & Quality Benchmarks *)
    rTarget_UF1_Conc_gL             : REAL;         (* Recipe Target Ultrafiltration Phase 1 Intermediate Conc [g/L] *)
    rTarget_Final_Conc_gL           : REAL;         (* Recipe Target Final Concentrated Drug Substance Bulk Conc [g/L] *)
    rTarget_Diafiltration_DV        : REAL;         (* Recipe Target Diafiltration Buffer Volume Exchange Number [DV] *)
    rTarget_WallShearRate_s1        : REAL;         (* Recipe Cassette Target Retentate Flow Channel Wall Shear Rate [s-1] *)
    rTarget_TMP_bar                 : REAL;         (* Recipe Active Transmembrane Pressure Operating Setpoint [bar] *)
    rTarget_ProcessTemp_degC        : REAL;         (* Recipe Active Process Recirculation Temperature Setpoint [deg C] *)
    rTarget_ChilldownTemp_degC      : REAL;         (* Recipe Bulk Drug Substance Storage Stabilization Temp [deg C] *)
    rTarget_CIP_Temp_degC           : REAL;         (* Recipe Caustic Clean-In-Place Washing Temperature Setpoint [deg C] *)
    rCassette_MembraneArea_m2       : REAL;         (* Total Active Filtration Membrane Surface Area [m2] *)
    rCassette_ChannelHeight_mm      : REAL;         (* Cassette Feed/Retentate Flow Channel Hydraulic Slit Height [mm] *)
    rCassette_ChannelWidth_mm       : REAL;         (* Cassette Feed/Retentate Flow Channel Total Slit Width [mm] *)
    rBaseline_NWP_LMHbar            : REAL;         (* Pre-Qualified Baseline Normalized Water Permeability Reference [LMH/bar] *)
END_VAR""")

    # VAR_OUTPUT
    st_lines.append("""VAR_OUTPUT
    (* Primary Actuator Modulating Commands *)
    rFeedPump_Speed_Cmd_rpm         : REAL;         (* Feed Quaternary Diaphragm Pump VFD Rotational Speed Command [rpm] *)
    rRetValve_Pos_Cmd_pct           : REAL;         (* Retentate Proportional Diaphragm / Pinch Backpressure Valve Command [%] *)
    rBufferPump_Speed_Cmd_pct       : REAL;         (* Diafiltration Buffer Feed Metering Pump Proportional Stroke Command [%] *)
    rPermValve_Pos_Cmd_pct          : REAL;         (* Permeate Line Sanitary Modulating Control Valve Command [%] *)
    rChillerValve_Pos_Cmd_pct       : REAL;         (* Heat Exchanger Chiller Glycol Modulating Control Valve Command [%] *)
    rFeedDivertValve_Pos_pct        : REAL;         (* Product Harvest Divert / Drain 3-Way Modulating Valve [%] *)

    (* Discrete Actuator & Hardware Safety Permissive Outputs *)
    bFeedPump_Run_Enable            : BOOL;         (* Feed Pump Variable Frequency Drive Hardware Run Permissive [-] *)
    bBufferPump_Run_Enable          : BOOL;         (* Diafiltration Buffer Metering Pump Hardware Run Permissive [-] *)
    bPermeateIsolation_Open         : BOOL;         (* Permeate Line Fail-Closed Sanitary Diaphragm Isolation Valve [-] *)
    bWFI_SupplyValve_Open           : BOOL;         (* WFI Flush Manifold Automated Sanitary Diaphragm Valve [-] *)
    bCIP_SupplyValve_Open           : BOOL;         (* Caustic CIP Wash Manifold Automated Diaphragm Supply Valve [-] *)
    bCIP_ReturnValve_Open           : BOOL;         (* Caustic CIP Wash Recirculation Return Automated Valve [-] *)
    bAirBlowdown_Valve_Open         : BOOL;         (* Sterile High-Purity Nitrogen Air Blowdown Solenoid Valve [-] *)
    bProductDrain_Valve_Open        : BOOL;         (* Retentate Hold-Up Bulk Product Harvest Drain Automated Valve [-] *)
    bSystemTrip_Interlock           : BOOL;         (* Critical Cat-4 Master Safety Interlock Fast-Trip Asserted [-] *)

    (* Cyber-Physical Observer Estimated States & Analytical Process Values *)
    rEst_TMP_bar                    : REAL;         (* Observer Estimated Cassette Transmembrane Pressure [bar] *)
    rEst_PermeateFlux_LMH           : REAL;         (* Observer Estimated Permeate Volumetric Flux [L/m2/h LMH] *)
    rEst_ProteinConc_gL             : REAL;         (* Observer Estimated Retentate Monoclonal Antibody Concentration [g/L] *)
    rEst_GelResistance_m1           : REAL;         (* Observer Estimated Concentration Polarization Gel Resistance [m-1] *)
    rEst_WallShearRate_s1           : REAL;         (* Observer Estimated Retentate Flow Channel Wall Shear Rate [s-1] *)
    rEst_DV_ExchangeCounter         : REAL;         (* Cumulative Diafiltration Buffer Volume Exchange Counter [DV] *)
    rEst_RecircTemp_degC            : REAL;         (* Observer Estimated Retentate Fluid Recirculation Temperature [deg C] *)
    rEst_SumpWeightDev_g            : REAL;         (* Diafiltration Mass Balance Retentate Sump Weight Deviation [g] *)
    rCalc_Current_NWP_LMHbar        : REAL;         (* Temperature-Normalized Water Permeability Current Calculation [LMH/bar] *)
    rCalc_NWPFluxRecovery_pct       : REAL;         (* Post-CIP Clean Water Flux Recovery Relative to Baseline [%] *)
    rCalc_PermeateAccumVol_L        : REAL;         (* Total Cumulative Permeate Filtrate Collected Volume [L] *)
    rCalc_BufferAddedVol_L          : REAL;         (* Total Cumulative Diafiltration Buffer Added Volume [L] *)
    rCalc_ConcentrationFactor       : REAL;         (* Real-Time Retentate Volumetric Concentration Factor VCF [-] *)
    rCalc_FluidViscosity_cP         : REAL;         (* Dynamic Monoclonal Antibody Solution Viscosity Prediction [cP] *)

    (* 14-Stage Production Finite State Machine Execution Telemetry *)
    nState                          : INT;          (* Active 14-Stage Bioprocess Production State Index (0..13) [-] *)
    nSubState                       : INT;          (* Active State Internal Sequence Step / Phase Counter [-] *)
    rStateTime_s                    : REAL;         (* Elapsed Dwell Time within Current Active Operating State [s] *)
    bCycleComplete                  : BOOL;         (* Full Automated Bioprocess Production Cycle Complete Strobe [-] *)
    bSequencePaused                 : BOOL;         (* Automated Sequence Currently in Recirculating Pause Mode [-] *)

    (* 32-Bit Bit-Packed Telemetry & ISA-18.2 Diagnostic DWORDS *)
    dwStatusWord1                   : DWORD;        (* System Status Word 1: Active State & Operation Modes [-] *)
    dwStatusWord2                   : DWORD;        (* System Status Word 2: TMR Voting Health, Actuators & Subsystems [-] *)
    dwAlarmWord1                    : DWORD;        (* Alarm Word 1: ISA-18.2 Critical High/High-High Process Alarms [-] *)
    dwAlarmWord2                    : DWORD;        (* Alarm Word 2: ISA-18.2 Low/Low-Low Alarms & Safety Trips [-] *)
    dwFirstOutWord                  : DWORD;        (* First-Out Root Cause Diagnostic Fault Registration Word [-] *)
END_VAR""")

    print("Header & IO done")
    return st_lines

generate()
