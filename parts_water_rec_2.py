# parts_water_rec_2.py - VAR_OUTPUT declarations

def get_var_output():
    return """VAR_OUTPUT
    (* =================================================================================================================
     * FINAL CONTROL ELEMENT (ACTUATOR) MODULATION AND ANALOG SPEED COMMAND OUTPUTS
     * ================================================================================================================= *)
    (* MABR Process Actuators *)
    rCmd_MABR_LumenAir_Valve_Pct    : REAL;     (* MABR Hollow Fiber Lumen Air Supply Control Valve [%] Range: 0.0 to 100.0 *)
    rCmd_MABR_InternalRecycle_RPM   : REAL;     (* MABR Anoxic/Aerobic Internal Chemostat Recycle Pump VFD [RPM] Range: 0.0 to 1800.0 *)

    (* Submerged UF Filtration Actuators *)
    rCmd_UF_PermeateSuction_VFD_Pct : REAL;     (* UF Filtrate Reversible Suction/Backwash Pump VFD Speed [%] Range: 0.0 to 100.0 *)
    rCmd_UF_AirScour_Valve_Pct      : REAL;     (* UF Coarse Bubble Aeration Scour Modulating Control Valve [%] Range: 0.0 to 100.0 *)
    rCmd_UF_NaOCl_Dosing_Pump_Pct   : REAL;     (* UF Chemically Enhanced Backwash (CEB) Sodium Hypochlorite Pump [%] Range: 0.0 to 100.0 *)
    rCmd_UF_CitricAcid_Dosing_Pct   : REAL;     (* UF Chemically Enhanced Backwash Citric Acid Descaling Pump [%] Range: 0.0 to 100.0 *)

    (* High-Pressure RO Trains & Energy Recovery Actuators *)
    rCmd_RO_HP_FeedPump_VFD_Pct     : REAL;     (* RO Stage 1 Primary High-Pressure Feed Pump VFD (65 bar) [%] Range: 0.0 to 100.0 *)
    rCmd_RO_ERD_BoosterPump_VFD_Pct : REAL;     (* RO ERD Auxiliary High-Pressure Booster Pump VFD [%] Range: 0.0 to 100.0 *)
    rCmd_RO_BrineReject_Throttle_Pct: REAL;     (* RO Stage 2 Concentrate Brine Throttle Needle Valve [%] Range: 0.0 to 100.0 *)
    rCmd_RO_Antiscalant_Dosing_Pct  : REAL;     (* RO Feed Phosphonate Scale Inhibitor Metering Pump [%] Range: 0.0 to 100.0 *)

    (* Water Reclamation Distribution and Disinfection Actuators *)
    rCmd_Permeate_Diversion_Valve_Pct: REAL;    (* Reclamation Water Off-Spec Rapid Diversion Valve to Basin [%] Range: 0.0 to 100.0 *)
    rCmd_UV_Reactor_Power_Pct       : REAL;     (* Variable Electronic Ballast UV Lamp Power Modulation [%] Range: 30.0 to 100.0 *)

    (* =================================================================================================================
     * ADVANCED CYBER-PHYSICAL OBSERVER AND TRANSPORT ESTIMATION OUTPUTS
     * ================================================================================================================= *)
    (* MABR Bubbleless Biofilm Mass Transfer Observer *)
    rObs_MABR_Biofilm_Thickness_um  : REAL;     (* Dynamic Estimated Biofilm Boundary Layer Thickness [um] Range: 50.0 to 800.0 *)
    rObs_MABR_O2_Mass_Flux_g_m2_d   : REAL;     (* Hollow Fiber Bubbleless Oxygen Transfer Flux [g/m2/d] Range: 0.0 to 50.0 *)
    rObs_MABR_Total_Nitrogen_mg_L   : REAL;     (* Effluent Total Inorganic Nitrogen (NH4-N + NOx-N) [mg/L] Range: 0.0 to 60.0 *)
    rObs_MABR_Nitrification_Rate    : REAL;     (* Specific Aerobic Nitrification Rate [g_N/m2/d] Range: 0.0 to 10.0 *)
    rObs_MABR_Denitrification_Rate  : REAL;     (* Specific Anoxic Denitrification Rate [g_N/m2/d] Range: 0.0 to 12.0 *)

    (* Submerged UF Resistance-in-Series Membrane Transport Observer *)
    rObs_UF_Intrinsic_Resistance_Rm : REAL;     (* Clean PVDF Membrane Hydraulic Resistance Rm [1/m] Range: 1.0E11 to 5.0E12 *)
    rObs_UF_Cake_Layer_Resistance_Rc: REAL;     (* Dynamic Biomass Fouling Cake Layer Resistance Rc [1/m] Range: 0.0 to 1.0E13 *)
    rObs_UF_Pore_Block_Resistance_Rp: REAL;     (* Colloidal Irreversible Pore Blocking Resistance Rp [1/m] Range: 0.0 to 5.0E12 *)
    rObs_UF_Normalized_TMP_20C      : REAL;     (* Temperature-Normalized Transmembrane Pressure at 20 deg C [bar] Range: 0.00 to 2.50 *)
    rObs_UF_Dynamic_Permeability    : REAL;     (* Temperature-Corrected Specific Membrane Permeability [LMH/bar] Range: 50.0 to 450.0 *)

    (* High-Pressure RO & Isobaric ERD Efficiency Observers *)
    rObs_RO_Net_Driving_Pressure_NDP: REAL;     (* Effective Net Driving Pressure Across Polyamide Membrane [bar] Range: 5.0 to 40.0 *)
    rObs_RO_Concentration_Polar_Beta: REAL;     (* Concentration Polarization Factor at Membrane Surface [dimensionless] Range: 1.00 to 2.50 *)
    rObs_RO_Salt_Rejection_Pct      : REAL;     (* Dynamic Salt Rejection Efficiency [pct] Range: 90.0 to 99.9 *)
    rObs_RO_Specific_Energy_kWh_m3  : REAL;     (* Overall Desalination Specific Energy Consumption [kWh/m3] Range: 0.50 to 3.50 *)
    rObs_ERD_Hydraulic_Recovery_Eff : REAL;     (* Ceramic Rotary Isobaric ERD Pressure Transfer Efficiency [%] Range: 80.0 to 98.5 *)
    rObs_ERD_Volumetric_Brine_Mix   : REAL;     (* ERD Duct High-Salinity Brine Carryover Volumetric Mixing [%] Range: 0.5 to 8.0 *)

    (* Disinfection Validation and Water Quality Observers *)
    rObs_UV_Delivered_Dose_mJ_cm2   : REAL;     (* Validated Delivered In-Situ Fluence Dose [mJ/cm2] Range: 0.0 to 120.0 *)
    rObs_UV_Cryptosporidium_LogRed  : REAL;     (* EPA Disinfection Pathogen Log-Inactivation Credit [log10] Range: 0.0 to 6.0 *)

    (* =================================================================================================================
     * DETERMINISTIC FSM STATE, SYSTEM HEALTH BITMASKS, AND ISA-18.2 ALARM PACKED WORDS
     * ================================================================================================================= *)
    iPlantFSM_State_Active          : INT;      (* Currently Active 12-Stage Plant Automation Sequence State (0..11) *)
    dwStatus_Word_Plant             : DWORD;    (* Bit-Packed Reclamation Complex Plant Status Register (32-Bit Mask) *)
    dwAlarmWord_Critical_Trip       : DWORD;    (* ISA-18.2 Priority 1 Equipment Trip and Hard Interlock Latches (32-Bit Mask) *)
    dwAlarmWord_Process_Warning     : DWORD;    (* ISA-18.2 Priority 2 Process Operating Limit Quality Violations (32-Bit Mask) *)
    dwAlarmWord_Sensor_Discrepancy  : DWORD;    (* ISA-18.2 Priority 3 2oo3 TMR Sensor Failure & Drift Bitmask (32-Bit Mask) *)
    dwSensorHealthMask              : DWORD;    (* Individual Primary Sensor Transmitter Health Bitmask (32-Bit Mask) *)
    bTrip_Plant_Lockout             : BOOL;     (* Master Safety Hard Lockout Active - Plant Shut Down & Isolated *)
    bWarning_Quality_OffSpec        : BOOL;     (* Effluent Disinfection / Salinity Violation Active - Diversion Engaged *)
END_VAR
"""
