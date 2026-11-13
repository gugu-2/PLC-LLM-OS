# ccgt_builder/st_header_io.py

def get_header_and_io():
    return """FUNCTION_BLOCK FB_Power_CCGT_GasTurbine_HRSG_Attemperator_Coordinated
(* =====================================================================================================================
 * LUMINA CYBER-PHYSICAL AUTOMATION ENGINE - SYNTHETIC DATASET V7 MAX-PERSONA
 * COMMERCIAL INDUSTRIAL SECTOR : Power Generation & Thermal Turbomachinery
 * SYSTEM                       : Multi-Shaft Combined Cycle Gas Turbine (CCGT) Power Block (350 MWe Class)
 * SUBSYSTEM                    : Coordinated Gas Turbine Load Governor, Triple-Pressure HRSG High-Pressure Drum Level
 *                                & Multi-Stage Attemperator Desuperheater Steam Temperature Control
 * COGNIZANT STANDARDS          : ASME BPVC Section I (Power Boilers), ASME PTC 46 (Overall Plant Performance),
 *                                NFPA 85 (Boiler and Combustion Systems Hazards Code), IEC 61508 / IEC 61511 (SIL-3),
 *                                IEC 61131-3 3rd Ed. (Structured Text), ISA-18.2 / IEC 62682 (Management of Alarm Systems)
 * EXECUTION SCAN PERIOD        : Ts = 20.0 ms (50.0 Hz Hard Real-Time Deterministic Cyclic Task)
 * ARCHITECTURAL SUMMARY:
 *   1) 2oo3 Triple Modular Redundancy (TMR) voting suite across 5 critical process measurement triplets (15 transmitters)
 *      with continuous discrepancy accumulation timers (200 ms fault window) and bumpless degradation.
 *   2) First-Principles 8th-Order Thermo-Hydraulic State-Space Model capturing:
 *      x1 = Gas Turbine Active Electrical Power Output [MW]
 *      x2 = Combustor Exhaust Gas Temperature (EGT / TIT) [deg C]
 *      x3 = Compressor Variable Guide Vane (VGV) Angular Position [deg]
 *      x4 = HRSG High-Pressure Drum Narrow-Range Water Level [mm] (non-minimum phase swell/shrink)
 *      x5 = High-Pressure Evaporator Generated Steam Mass Flow Rate [kg/s]
 *      x6 = Final Superheater Main Steam Exit Temperature [deg C]
 *      x7 = Attemperator Desuperheater Inter-Stage Steam Temperature [deg C]
 *      x8 = Boiler Feedwater Regulating Valve Effective Hydrodynamic Position [%]
 *   3) Discrete-Time Kalman Filter / Luenberger State Observer with gain matrix L (8x6) for real-time state reconstruction.
 *   4) Receding-Horizon Model Predictive Control (MPC) with 5-step prediction horizon (Np=5) and 6 unrolled iterations of
 *      Projected Gradient Descent (PGD) enforcing box bounds, slew rates, and dynamic turbine-boiler decoupling.
 *   5) Deterministic 14-Stage CCGT Power Plant Finite State Machine (FSM) spanning Cold Purge to Base Load, DLN Transfer,
 *      Peaking Duct Firing, Rapid Primary Frequency Grid Support, Deloading, and Emergency Master Fuel Trip (MFT).
 *   6) ISA-18.2 Process Alarm Engine with SIL-3 Drum Low-Low/High-High Fast Trips and 32-bit Bit-Packed Telemetry.
 * ===================================================================================================================== *)

VAR_INPUT
    (* =================================================================================================================
     * SECTION 1.1: MASTER PLANT CONTROL & OPERATOR DISPATCH COMMANDS
     * ================================================================================================================= *)
    bMasterStart_Cmd                : BOOL;  (* [bool] Master Plant Startup Command Sequence Enable *)
    bMasterStop_Cmd                 : BOOL;  (* [bool] Master Coordinated Cooldown and Shutdown Command *)
    bEmergencyTrip_PB               : BOOL;  (* [bool] SIL-3 Hardwired Emergency Stop Pushbutton Trip (Active LOW fail-safe) *)
    bReset_Cmd                      : BOOL;  (* [bool] Master Alarm Latch & Trip Reset Command *)
    bAuto_Coord_Enable              : BOOL;  (* [bool] Coordinated Turbine-Boiler MPC Automatic Control Mode Enable *)
    bEnable_Duct_Burner             : BOOL;  (* [bool] Operator Request for HRSG Peaking Duct Burner Firing *)
    bGrid_Freq_Support_Enable       : BOOL;  (* [bool] Grid Frequency Primary Droop Response Fast Modulation Enable *)

    (* =================================================================================================================
     * SECTION 1.2: GRID DISPATCH, FREQUENCY & ELECTRICAL BOUNDARY INTERFACES
     * ================================================================================================================= *)
    rMW_Demand_Grid                 : REAL;  (* [MW] External AGC / Dispatch Active Power Generation Setpoint [0.0..350.0 MW] *)
    rGrid_Frequency_Hz              : REAL;  (* [Hz] High-Precision Utility Grid Intertie Frequency [45.00..55.00 Hz] *)
    rGrid_Freq_Nominal_Hz           : REAL;  (* [Hz] Nominal Power Grid Base Frequency [50.00 or 60.00 Hz] *)
    rGrid_Droop_Percent             : REAL;  (* [%] Governor Speed Droop Characteristic Percentage [2.0..6.0 %] *)
    bBreaker_52G_Closed             : BOOL;  (* [bool] Generator Main 52G Circuit Breaker Auxiliary Contact Closed Status *)

    (* =================================================================================================================
     * SECTION 1.3: TURBOMACHINERY MECHANICAL & COMBUSTION INTERFACES
     * ================================================================================================================= *)
    rTurbine_Shaft_Speed_RPM        : REAL;  (* [rpm] Gas Turbine Rotor Mechanical Speed [0.0..3600.0 rpm] *)
    rTurning_Gear_Speed_RPM         : REAL;  (* [rpm] Hydraulic Barred Turning Gear Rotor Rotation Speed [0.0..150.0 rpm] *)
    bTurning_Gear_Engaged           : BOOL;  (* [bool] Turning Gear Mechanical Clutch Engagement Limit Switch *)
    bJacking_Oil_Press_OK           : BOOL;  (* [bool] Hydrostatic Rotor Bearing Jacking Oil Pressure Permissive (> 120 bar) *)
    bLube_Oil_Press_OK              : BOOL;  (* [bool] Turbomachinery Bearing Forced Lubrication Header Pressure OK *)
    bCrank_Motor_Running            : BOOL;  (* [bool] Static Frequency Converter (SFC) / Crank Starter Motor Running *)
    rCombustor_Flame_Intensity_Pct  : REAL;  (* [%] Optical Multi-Spectrum UV/IR Flame Scanner Average Intensity [0.0..100.0 %] *)
    nCombustor_Flames_Detected      : INT;   (* [-] Total Number of Healthy Combustor Cans Reporting Established Flame [0..14] *)

    (* =================================================================================================================
     * SECTION 1.4: AMBIENT & BALANCE OF PLANT THERMODYNAMIC CONDITIONS
     * ================================================================================================================= *)
    rAmbient_Temp_degC              : REAL;  (* [deg C] Compressor Inlet Ambient Dry Bulb Air Temperature [-30.0..55.0 deg C] *)
    rAmbient_Pressure_bar           : REAL;  (* [bar] Barometric Atmospheric Pressure at Site Elevation [0.80..1.10 bar] *)
    rHP_Drum_Pressure_bar           : REAL;  (* [bar] HRSG High-Pressure Drum Operating Steam Saturated Pressure [0.0..160.0 bar] *)
    rFeedwater_Supply_Pressure_bar  : REAL;  (* [bar] Boiler Feedwater Pump Discharge Header Pressure [0.0..180.0 bar] *)
    rFeedwater_Supply_Temp_degC     : REAL;  (* [deg C] Economizer Inlet Subcooled Feedwater Temperature [80.0..180.0 deg C] *)
    bSteam_Turbine_Ready_Accept     : BOOL;  (* [bool] Steam Turbine Digital Governor Ready to Accept HP Steam Admission *)
    bCondenser_Vacuum_OK            : BOOL;  (* [bool] Surface Condenser Vacuum Permissive Available (> 0.08 bar abs) *)

    (* =================================================================================================================
     * SECTION 1.5: 2oo3 TRIPLE MODULAR REDUNDANT PROCESS INSTRUMENTATION (15 TRANSMITTERS)
     * ================================================================================================================= *)
    (* Channel Group 1: Combustor Exhaust Gas Temperature (EGT) Pyrometer Rakes [deg C] (0.0 to 800.0 deg C) *)
    rTT_EGT_101A                    : REAL;  (* [deg C] Exhaust Gas Thermocouple Rake Sector A [deg C] *)
    rTT_EGT_101B                    : REAL;  (* [deg C] Exhaust Gas Thermocouple Rake Sector B [deg C] *)
    rTT_EGT_101C                    : REAL;  (* [deg C] Exhaust Gas Thermocouple Rake Sector C [deg C] *)

    (* Channel Group 2: HRSG High-Pressure Drum Narrow-Range Water Level [mm] (-400.0 to +400.0 mm) *)
    rLT_DRUM_201A                   : REAL;  (* [mm] HRSG HP Drum Narrow-Range Level Sensor Channel A [mm] *)
    rLT_DRUM_201B                   : REAL;  (* [mm] HRSG HP Drum Narrow-Range Level Sensor Channel B [mm] *)
    rLT_DRUM_201C                   : REAL;  (* [mm] HRSG HP Drum Narrow-Range Level Sensor Channel C [mm] *)

    (* Channel Group 3: Final Superheater Main Steam Exit Temperature [deg C] (0.0 to 650.0 deg C) *)
    rTT_STEAM_301A                  : REAL;  (* [deg C] Final Superheater Main Steam Exit Temperature Channel A [deg C] *)
    rTT_STEAM_301B                  : REAL;  (* [deg C] Final Superheater Main Steam Exit Temperature Channel B [deg C] *)
    rTT_STEAM_301C                  : REAL;  (* [deg C] Final Superheater Main Steam Exit Temperature Channel C [deg C] *)

    (* Channel Group 4: HP Steam Header Coriolis Mass Flow Rate [kg/s] (0.0 to 300.0 kg/s) *)
    rFT_STEAM_401A                  : REAL;  (* [kg/s] HP Steam Header Coriolis Mass Flow Channel A [kg/s] *)
    rFT_STEAM_401B                  : REAL;  (* [kg/s] HP Steam Header Coriolis Mass Flow Channel B [kg/s] *)
    rFT_STEAM_401C                  : REAL;  (* [kg/s] HP Steam Header Coriolis Mass Flow Channel C [kg/s] *)

    (* Channel Group 5: Generator Active Electrical Power Transducers [MW] (0.0 to 450.0 MW) *)
    rWT_POWER_501A                  : REAL;  (* [MW] Generator Active Electrical Power Transducer Channel A [MW] *)
    rWT_POWER_501B                  : REAL;  (* [MW] Generator Active Electrical Power Transducer Channel B [MW] *)
    rWT_POWER_501C                  : REAL;  (* [MW] Generator Active Electrical Power Transducer Channel C [MW] *)
END_VAR

VAR_OUTPUT
    (* =================================================================================================================
     * SECTION 2.1: CO-ORDINATED ACTUATOR REGULATION DEMANDS
     * ================================================================================================================= *)
    rFuel_Gas_Valve_Cmd_Pct         : REAL;  (* [%] Gas Turbine Main Fuel Gas Control Valve Position Demand [0.0..100.0 %] *)
    rVGV_Position_Cmd_deg           : REAL;  (* [deg] Compressor Variable Guide Vane Angular Position Demand [0.0..85.0 deg] *)
    rFeedwater_Valve_Cmd_Pct        : REAL;  (* [%] HRSG HP Boiler Feedwater Regulating Valve Position Demand [0.0..100.0 %] *)
    rAttemperator_Valve_Cmd_Pct     : REAL;  (* [%] Superheater Attemperator Desuperheater Spray Valve Demand [0.0..100.0 %] *)
    rSteam_Bypass_Valve_Cmd_Pct     : REAL;  (* [%] HP Steam Bypass Valve to Surface Condenser Position Demand [0.0..100.0 %] *)
    rDuct_Burner_Valve_Cmd_Pct      : REAL;  (* [%] HRSG Peaking Duct Burner Fuel Gas Regulating Valve Demand [0.0..100.0 %] *)

    (* =================================================================================================================
     * SECTION 2.2: HARDWIRED SAFETY & AUXILIARY CONTROLLERS
     * ================================================================================================================= *)
    bMaster_Fuel_Trip_MFT           : BOOL;  (* [bool] Master Fuel Trip Solenoid De-Energize Command (TRUE = Plant Tripped) *)
    bTurning_Gear_Motor_Cmd         : BOOL;  (* [bool] Rotor Hydraulic Turning Gear Contactor Run Command *)
    bIgniter_Spark_Cmd              : BOOL;  (* [bool] High-Energy Spark Igniter Coil Excitation Command *)
    bSync_Permissive_52G            : BOOL;  (* [bool] Generator Auto-Synchronizer 52G Breaker Close Permissive *)
    bDLN_Premix_Mode_Active         : BOOL;  (* [bool] Dry Low NOx (DLN 2.6+) Steady-State Premix Mode Engaged *)
    bDrum_Swell_Lockout_Active      : BOOL;  (* [bool] HP Drum Shrink/Swell Transient Decoupling Lockout Active *)
    bPrimary_Freq_Active            : BOOL;  (* [bool] Fast Primary Grid Frequency Governor Support Modulating *)

    (* =================================================================================================================
     * SECTION 2.3: OPERATIONAL STATE & HIGH-RELIABILITY VOTED TELEMETRY
     * ================================================================================================================= *)
    nPlant_FSM_State_Out            : INT;   (* [-] Deterministic 14-Stage CCGT Operational State [0..13] *)
    rVoted_EGT_degC                 : REAL;  (* [deg C] 2oo3 TMR High-Reliability Combustor Exhaust Gas Temperature [deg C] *)
    rVoted_Drum_Level_mm            : REAL;  (* [mm] 2oo3 TMR High-Reliability HP Drum Narrow-Range Water Level [mm] *)
    rVoted_Steam_Temp_degC          : REAL;  (* [deg C] 2oo3 TMR High-Reliability Final Superheater Main Steam Exit Temp [deg C] *)
    rVoted_Steam_Flow_kgs           : REAL;  (* [kg/s] 2oo3 TMR High-Reliability HP Steam Header Mass Flow Rate [kg/s] *)
    rVoted_Active_Power_MW          : REAL;  (* [MW] 2oo3 TMR High-Reliability Generator Active Electrical Power [MW] *)

    (* =================================================================================================================
     * SECTION 2.4: 32-BIT BIT-PACKED TELEMETRY REGISTERS & FIRST-OUT RECORDERS
     * ================================================================================================================= *)
    dwStatusWord1                   : DWORD; (* [bit-field] Plant Subsystem Supervisory Telemetry Status Word 1 *)
    dwStatusWord2                   : DWORD; (* [bit-field] 2oo3 TMR Sensor Channel Health & Degradation Status Word 2 *)
    dwAlarmWord1                    : DWORD; (* [bit-field] Critical SIL-3 Trips & Priority 1 Master Fuel Trip Alarm Word 1 *)
    dwAlarmWord2                    : DWORD; (* [bit-field] Process High/Low Warnings & Deviation Supervisory Alarm Word 2 *)
    dwFirstOutWord                  : DWORD; (* [bit-field] Sequence-of-Events Root-Cause First-Out Trip Origin Latch *)
END_VAR
"""
