# parts_water_rec_1.py - VAR_INPUT, VAR_OUTPUT, and VAR declarations

def get_header_and_inputs():
    return """FUNCTION_BLOCK FB_Water_MABR_Ultrafiltration_RO_Reclamation
(* =====================================================================================================================
 * LUMINA CYBER-PHYSICAL AUTOMATION ENGINE - SYNTHETIC DATASET V7 MAX-PERSONA
 * ARCHITECTURAL GRADE : Advanced Water Treatment & Water Reclamation (Tier 1 Global High-Demand Industrial Automation)
 * COMMERCIAL SYSTEM    : Municipal & Industrial Advanced Wastewater Water Reclamation Complex (100 MLD Capacity)
 * UNIT PROCESSES       : 
 *   1. Membrane Aerated Biofilm Reactor (MABR) with Oxygen Permeable Hollow-Fiber Gas Transfer
 *      (Bubbleless gas transfer, Simultaneous Nitrification/Denitrification [SND], dynamic biofilm thickness observer)
 *   2. Submerged Ultrafiltration (UF) Membrane Trains (PVDF 0.04 um hollow fiber)
 *      (Transmembrane pressure [TMP] cascade, cyclic coarse bubble air scour, automated hydraulic backpulse & CEB)
 *   3. High-Pressure Dual-Stage Reverse Osmosis (RO) Trains with Isobaric Energy Recovery Devices (ERD)
 *      (Ceramic isobaric pressure exchangers > 97% recovery, feed brine pressure 65.0 bar, concentration polarization)
 *   4. Real-Time Feed Silt Density Index (SDI-15), Permeate Conductivity, and UV Disinfection Transmittance Validation
 *
 * GOVERNING STANDARDS  : IEC 61131-3 3rd Ed., ISA-18.2 Alarm Management, EPA Water Reuse Guidelines, ISO 20468-1
 * TARGET PLATFORMS     : Siemens S7-1500 / Allen-Bradley ControlLogix 5580 / Beckhoff TwinCAT 3.1 C++ / ST
 * ===================================================================================================================== *)

VAR_INPUT
    (* =================================================================================================================
     * PRIMARY SENSOR CHANNELS - TRI-REDUNDANT 2oo3 TRANSMITTERS WITH PHYSICAL ENGINEERING UNITS
     * ================================================================================================================= *)
    (* MABR Triplicated Dissolved Oxygen Optical Luminescent Probes in Reactor Bulk Mixed Liquor *)
    rAIT_MABR_DO_101A               : REAL;     (* MABR Bulk DO Probe Channel A [mg/L] Range: 0.00 to 10.00 *)
    rAIT_MABR_DO_101B               : REAL;     (* MABR Bulk DO Probe Channel B [mg/L] Range: 0.00 to 10.00 *)
    rAIT_MABR_DO_101C               : REAL;     (* MABR Bulk DO Probe Channel C [mg/L] Range: 0.00 to 10.00 *)

    (* MABR Triplicated Ammonium Ion-Selective Field Electrodes (ISE) in Nitrification Zone *)
    rAIT_MABR_NH4_102A              : REAL;     (* MABR Ammonium Nitrogen Channel A [mg/L] Range: 0.00 to 50.00 *)
    rAIT_MABR_NH4_102B              : REAL;     (* MABR Ammonium Nitrogen Channel B [mg/L] Range: 0.00 to 50.00 *)
    rAIT_MABR_NH4_102C              : REAL;     (* MABR Ammonium Nitrogen Channel C [mg/L] Range: 0.00 to 50.00 *)

    (* MABR Triplicated Nitrate + Nitrite Ion-Selective Field Electrodes (ISE) in Denitrification Zone *)
    rAIT_MABR_NO3_103A              : REAL;     (* MABR Nitrate Nitrogen Channel A [mg/L] Range: 0.00 to 50.00 *)
    rAIT_MABR_NO3_103B              : REAL;     (* MABR Nitrate Nitrogen Channel B [mg/L] Range: 0.00 to 50.00 *)
    rAIT_MABR_NO3_103C              : REAL;     (* MABR Nitrate Nitrogen Channel C [mg/L] Range: 0.00 to 50.00 *)

    (* MABR Gas Lumen Header Pneumatic and Hydraulic Process Inputs *)
    rPT_MABR_AIR_LUMEN_PRESS_104    : REAL;     (* MABR Hollow Fiber Lumen Air Supply Pressure [bar] Range: 0.00 to 6.00 *)
    rFT_MABR_AIR_FLOW_105           : REAL;     (* MABR Lumen Aeration Compressed Air Header Flow [Nm3/h] Range: 0.0 to 5000.0 *)
    rAIT_MABR_MLSS_106              : REAL;     (* MABR Mixed Liquor Suspended Solids [mg/L] Range: 2000.0 to 12000.0 *)
    rAIT_MABR_COD_SOLUBLE_107       : REAL;     (* MABR Influent Readily Biodegradable Soluble COD [mg/L] Range: 20.0 to 800.0 *)
    rTT_WATER_INLET_TEMP_108        : REAL;     (* Reclamation Complex Process Water Temperature [deg C] Range: 5.0 to 45.0 *)

    (* Submerged Ultrafiltration (UF) Triplicated Transmembrane Pressure (TMP) Transmitters *)
    rPDT_UF_TMP_201A                : REAL;     (* Submerged UF Train Differential TMP Cell A [bar] Range: -1.00 to 2.50 *)
    rPDT_UF_TMP_201B                : REAL;     (* Submerged UF Train Differential TMP Cell B [bar] Range: -1.00 to 2.50 *)
    rPDT_UF_TMP_201C                : REAL;     (* Submerged UF Train Differential TMP Cell C [bar] Range: -1.00 to 2.50 *)

    (* Submerged UF Triplicated Permeate Turbidity Optical Analyzers (Laser Nephelometers) *)
    rAIT_UF_TURB_202A               : REAL;     (* UF Permeate Effluent Turbidity Channel A [NTU] Range: 0.000 to 5.000 *)
    rAIT_UF_TURB_202B               : REAL;     (* UF Permeate Effluent Turbidity Channel B [NTU] Range: 0.000 to 5.000 *)
    rAIT_UF_TURB_202C               : REAL;     (* UF Permeate Effluent Turbidity Channel C [NTU] Range: 0.000 to 5.000 *)

    (* UF Hydraulic and Aeration Scour Monitoring *)
    rFT_UF_PERMEATE_FLOW_203        : REAL;     (* Submerged UF Train Filtrate Permeate Flow [m3/h] Range: 0.0 to 2500.0 *)
    rPT_UF_AIR_SCOUR_204            : REAL;     (* UF Membrane Coarse Bubble Air Scour Header Pressure [bar] Range: 0.00 to 4.00 *)
    rPT_UF_BACKWASH_PRESS_205       : REAL;     (* UF Reverse Hydraulic Backpulse Header Pressure [bar] Range: 0.00 to 4.00 *)
    rAIT_FEED_TSS_206               : REAL;     (* Secondary Clarifier Effluent Feed Total Suspended Solids [mg/L] Range: 0.0 to 100.0 *)

    (* High-Pressure RO Triplicated Feed Header Pressure Transmitters (Stage 1 Feed) *)
    rPT_RO_HP_FEED_301A             : REAL;     (* RO Train Primary High-Pressure Feed Sensor A [bar] Range: 0.00 to 90.00 *)
    rPT_RO_HP_FEED_301B             : REAL;     (* RO Train Primary High-Pressure Feed Sensor B [bar] Range: 0.00 to 90.00 *)
    rPT_RO_HP_FEED_301C             : REAL;     (* RO Train Primary High-Pressure Feed Sensor C [bar] Range: 0.00 to 90.00 *)

    (* High-Pressure RO Triplicated Stage 2 Concentrate Brine Pressure Transmitters *)
    rPT_RO_CONC_PRESS_302A          : REAL;     (* RO Stage 2 Concentrate Brine Pressure Sensor A [bar] Range: 0.00 to 90.00 *)
    rPT_RO_CONC_PRESS_302B          : REAL;     (* RO Stage 2 Concentrate Brine Pressure Sensor B [bar] Range: 0.00 to 90.00 *)
    rPT_RO_CONC_PRESS_302C          : REAL;     (* RO Stage 2 Concentrate Brine Pressure Sensor C [bar] Range: 0.00 to 90.00 *)

    (* RO Triplicated Permeate Conductivity Analyzers (High-Accuracy 4-Electrode Cells) *)
    rAIT_RO_COND_401A               : REAL;     (* RO Permeate Electrical Conductivity Sensor A [uS/cm] Range: 0.0 to 1000.0 *)
    rAIT_RO_COND_401B               : REAL;     (* RO Permeate Electrical Conductivity Sensor B [uS/cm] Range: 0.0 to 1000.0 *)
    rAIT_RO_COND_401C               : REAL;     (* RO Permeate Electrical Conductivity Sensor C [uS/cm] Range: 0.0 to 1000.0 *)

    (* RO Permeate and Concentrate Mass Balance Transmitters *)
    rFT_RO_PERMEATE_FLOW_402        : REAL;     (* RO Train Combined Permeate Volumetric Flow [m3/h] Range: 0.0 to 2000.0 *)
    rFT_RO_CONCENTRATE_FLOW_403     : REAL;     (* RO Train Final Concentrate Brine Discharge Flow [m3/h] Range: 0.0 to 800.0 *)
    rAIT_RO_FEED_TDS_404            : REAL;     (* RO Feed Total Dissolved Solids Concentration [mg/L] Range: 100.0 to 8000.0 *)
    rPT_RO_INTERSTAGE_BOOST_405     : REAL;     (* RO Stage 1 to Stage 2 Interstage Booster Pressure [bar] Range: 0.00 to 85.00 *)

    (* Isobaric Energy Recovery Device (ERD) Ceramic Rotary Pressure Exchanger Monitoring *)
    rPT_ERD_HP_IN_501A              : REAL;     (* ERD High-Pressure Brine Inlet Pressure Sensor A [bar] Range: 0.00 to 90.00 *)
    rPT_ERD_HP_IN_501B              : REAL;     (* ERD High-Pressure Brine Inlet Pressure Sensor B [bar] Range: 0.00 to 90.00 *)
    rPT_ERD_HP_IN_501C              : REAL;     (* ERD High-Pressure Brine Inlet Pressure Sensor C [bar] Range: 0.00 to 90.00 *)
    rPT_ERD_HP_OUT_502              : REAL;     (* ERD Pressurized Feed Discharge to RO Feed [bar] Range: 0.00 to 90.00 *)
    rPT_ERD_LP_IN_503               : REAL;     (* ERD Low-Pressure Pre-Filtered Feed Supply [bar] Range: 0.00 to 10.00 *)
    rST_ERD_ROTOR_RPM_504           : REAL;     (* ERD Ceramic Rotor Rotational Speed Magnetic Pickup [RPM] Range: 0.0 to 2500.0 *)

    (* Real-Time Feed Silt Density Index (SDI-15) Online Colloidal Fouling Analyzer *)
    rAIT_FEED_SDI15_505             : REAL;     (* RO Feed Online 15-Minute Silt Density Index [dimensionless] Range: 0.00 to 10.00 *)

    (* Triplicated UV Disinfection Transmittance (UVT-254) Spectrophotometers *)
    rAIT_UV_TRANS_601A              : REAL;     (* UV Disinfection Transmittance at 254nm Channel A [%] Range: 0.0 to 100.0 *)
    rAIT_UV_TRANS_601B              : REAL;     (* UV Disinfection Transmittance at 254nm Channel B [%] Range: 0.0 to 100.0 *)
    rAIT_UV_TRANS_601C              : REAL;     (* UV Disinfection Transmittance at 254nm Channel C [%] Range: 0.0 to 100.0 *)
    rIIT_UV_INTENSITY_602           : REAL;     (* UV Reactor In-Situ Germanium Photodiode Fluence [mW/cm2] Range: 0.0 to 250.0 *)

    (* Operational Process Permissives and Execution Time Configuration *)
    bCmd_Plant_Enable               : BOOL;     (* Master Plant Automation Reclamation Sequence Permissive *)
    bCmd_Reset_Alarms               : BOOL;     (* Operator Master Alarm Acknowledge and Diagnostic Latch Reset *)
    bCmd_Force_UF_Backwash          : BOOL;     (* Operator Manual Override to Trigger UF Air-Scour Backwash Cycle *)
    bCmd_Force_RO_CIP               : BOOL;     (* Operator Manual Request to Initiate RO Membrane CIP Sequence *)
    bCmd_Emergency_Stop             : BOOL;     (* Safety Instrumented System Hardwired E-Stop Interlock Tripped *)
    rPar_SampleTime_Sec             : REAL;     (* Discrete Automation Execution Scan Cycle Time [s] Range: 0.010 to 0.500 *)

    (* Supervisory Regulatory Dynamic Setpoints *)
    rSP_MABR_DO_Target              : REAL;     (* MABR Bulk Liquid Target Dissolved Oxygen Setpoint [mg/L] Nominal: 0.20 *)
    rSP_UF_Flux_Target              : REAL;     (* Submerged UF Operating Clean Permeate Flux Target [LMH] Nominal: 32.5 *)
    rSP_RO_Recovery_Rate            : REAL;     (* Dual-Stage RO Net Hydraulic Permeate Recovery Setpoint [%] Nominal: 85.0 *)
    rSP_RO_HP_Pressure_Target       : REAL;     (* RO Stage 1 High-Pressure Feed Pump Header Target [bar] Nominal: 65.00 *)
    rSP_UV_Dose_Target              : REAL;     (* UV Disinfection Minimum Validated Fluence Dose [mJ/cm2] Nominal: 40.0 *)
END_VAR
"""
