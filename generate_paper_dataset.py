# generate_paper_dataset.py
# High-density IEC 61131-3 Function Block Generator for World-Scale 1,800 m/min Fourdrinier Paper Machine
# Lumina Swarm V7 Max-Persona Protocol (Principal Automation Fellow & Cyber-Physical Systems Chair)

import os
import sys
import re
import json
import uuid

def generate_iec_code():
    parts = []
    
    # -------------------------------------------------------------------------
    # PART 1: Function Block Declaration & Engineering Documentation Header
    # -------------------------------------------------------------------------
    parts.append("""FUNCTION_BLOCK FB_PulpPaper_Fourdrinier_Headbox_ShoePress_Dryer
(* =====================================================================================================================
 * LUMINA CYBER-PHYSICAL AUTOMATION ENGINE - SYNTHETIC DATASET V7 MAX-PERSONA
 * COMMERCIAL INDUSTRIAL SECTOR : Pulp & Paper Heavy Process Manufacturing (Mass Continuous Production)
 * SYSTEM                       : World-Scale 1,800 m/min Multi-Ply Fourdrinier Paper Machine
 * KEY SUBSYSTEMS INTEGRATED    :
 *   1. Hydraulic Headbox Multi-Channel Consistency Dilution Profiling with Jet-to-Wire Speed Ratio (v_jet/v_wire = 1.015)
 *      Decoupled Total Head Air-Pad Cushion / Liquid Pond Level Hydrodynamic Observer.
 *   2. Dynamic Slice Lip Thermal Expansion Micro-Actuator Array (8,500 mm wide web profile, 32 CD zones) coupled with
 *      CD Thin Stock Consistency Dilution Injection Headers.
 *   3. Multi-Zone Wire Vacuum Dewatering Suction Boxes (Forming Board, Low-Vac, High-Vac Flat Boxes & Suction Couch Roll).
 *   4. Multi-Nip Extended Shoe Press (ENP) Dynamic Linear Load (1,500 kN/m) Balancing with Hydrodynamic Oil Film
 *      Thickness Observer (Vogel Viscosity-Temperature Lubrication Regimes).
 *   5. 6-Section 60-Cylinder Steam Dryer Cascade with Stationary Siphon Condensate Evacuation & Blow-Through Steam
 *      Recompression Energy Optimization (Enthalpy & Mass Evaporative Transfer Observer).
 *   6. Cross-Direction (CD) Decoupled Control: Radiometric Beta-Ray Basis Weight (g/m2) and Infrared Moisture Scanners.
 *   7. Multi-Roll Soft Calender Induction Thermal Roll Camber Profiling & High-Speed Reel Web Tension Control (450 N/m).
 *   8. 2oo3 Triple Modular Redundancy (TMR) Voting on 12 Critical Process Loops with Debounce & Bumpless Degradation.
 *   9. Discrete 8x8 Multivariable State-Space Model Predictive Control (MPC) running at deterministic 10 ms cycle.
 *  10. 12-Stage Deterministic Finite State Machine (FSM) & ISA-18.2 5-Tier Alarm Ladder with < 15 ms Web Break E-Dump.
 * DESIGN SPECIFICATIONS & RATINGS:
 *   - Web Width                 : 8,500 mm (8.5 m trim width)
 *   - Maximum Design Line Speed : 1,800 m/min (30.0 m/s web velocity)
 *   - Basis Weight Target Range : 40.0 g/m2 to 150.0 g/m2 (Nominal: 80.0 g/m2 +/- 0.25 g/m2 2-sigma)
 *   - Reel Moisture Target      : 5.50 % H2O +/- 0.15 % H2O (2-sigma CD spread)
 *   - Shoe Press Linear Nip Load: 1,500 kN/m (Total Pressing Force: 12,750 kN / 1,300 metric tons)
 *   - Dryer Cylinders           : 60 x 1,800 mm Cast Iron Steam Cylinders (10 cylinders per section x 6 sections)
 *   - Deterministic Execution   : 10.0 ms (T_s = 0.010 s) Real-Time PLC Cyclic Interrupt Task
 * ===================================================================================================================== *)
""")

    # -------------------------------------------------------------------------
    # PART 2: VAR_INPUT Declaration
    # -------------------------------------------------------------------------
    parts.append("""VAR_INPUT
    (* =================================================================================================================
     * SECTION 1: 2oo3 TRIPLE MODULAR REDUNDANT PROCESS SENSORS (12 TRIPLETS, TOTAL 36 ANALOG TRANSMITTERS)
     * ================================================================================================================= *)
    (* 1.1: Headbox Total Head Hydrodynamic Pressure Transmitters [kPa], Calibrated 0.0 .. 600.0 kPa *)
    PT_HEADBOX_TOTAL_HEAD_101A        : REAL := 468.30;  (* Headbox Total Head Pressure Transmitter Ch A [kPa] *)
    PT_HEADBOX_TOTAL_HEAD_101B        : REAL := 468.30;  (* Headbox Total Head Pressure Transmitter Ch B [kPa] *)
    PT_HEADBOX_TOTAL_HEAD_101C        : REAL := 468.30;  (* Headbox Total Head Pressure Transmitter Ch C [kPa] *)

    (* 1.2: Approach Flow Primary Fan Pump Discharge Volumetric Flow Transmitters [m3/h], Calibrated 0.0 .. 15000.0 m3/h *)
    FT_STOCK_FEED_PUMP_102A           : REAL := 9850.00; (* Stock Fan Pump Volumetric Flow Transmitter Ch A [m3/h] *)
    FT_STOCK_FEED_PUMP_102B           : REAL := 9850.00; (* Stock Fan Pump Volumetric Flow Transmitter Ch B [m3/h] *)
    FT_STOCK_FEED_PUMP_102C           : REAL := 9850.00; (* Stock Fan Pump Volumetric Flow Transmitter Ch C [m3/h] *)

    (* 1.3: Thin Stock Consistency Microwave / Optical Transmitters [%], Calibrated 0.200 .. 2.000 % *)
    AIT_THIN_STOCK_CONSISTENCY_103A   : REAL := 0.750;   (* Thin Stock Consistency Transmitter Ch A [% solids] *)
    AIT_THIN_STOCK_CONSISTENCY_103B   : REAL := 0.750;   (* Thin Stock Consistency Transmitter Ch B [% solids] *)
    AIT_THIN_STOCK_CONSISTENCY_103C   : REAL := 0.750;   (* Thin Stock Consistency Transmitter Ch C [% solids] *)

    (* 1.4: Forming Wire Section Drive Velocity Encoders [m/min], Calibrated 0.0 .. 2200.0 m/min *)
    ST_FORMING_WIRE_SPEED_104A        : REAL := 1800.00; (* Forming Wire Surface Speed Encoder Ch A [m/min] *)
    ST_FORMING_WIRE_SPEED_104B        : REAL := 1800.00; (* Forming Wire Surface Speed Encoder Ch B [m/min] *)
    ST_FORMING_WIRE_SPEED_104C        : REAL := 1800.00; (* Forming Wire Surface Speed Encoder Ch C [m/min] *)

    (* 1.5: Wire Flat Suction Box High-Vacuum Differential Transmitters [kPa], Calibrated -80.0 .. 0.0 kPa *)
    DPS_WIRE_SUCTION_BOX_201A         : REAL := -42.50;  (* Wire High-Vac Flat Box Diff Pressure Ch A [kPa] *)
    DPS_WIRE_SUCTION_BOX_201B         : REAL := -42.50;  (* Wire High-Vac Flat Box Diff Pressure Ch B [kPa] *)
    DPS_WIRE_SUCTION_BOX_201C         : REAL := -42.50;  (* Wire High-Vac Flat Box Diff Pressure Ch C [kPa] *)

    (* 1.6: Extended Nip Shoe Press Hydraulic Cylinder Pressure Transmitters [bar], Calibrated 0.0 .. 350.0 bar *)
    PT_SHOE_PRESS_HYD_PRESSURE_301A   : REAL := 215.00;  (* Shoe Press Main Hydraulic Header Pressure Ch A [bar] *)
    PT_SHOE_PRESS_HYD_PRESSURE_301B   : REAL := 215.00;  (* Shoe Press Main Hydraulic Header Pressure Ch B [bar] *)
    PT_SHOE_PRESS_HYD_PRESSURE_301C   : REAL := 215.00;  (* Shoe Press Main Hydraulic Header Pressure Ch C [bar] *)

    (* 1.7: Extended Nip Shoe Press Dynamic Linear Load Transmitters [kN/m], Calibrated 0.0 .. 2000.0 kN/m *)
    WT_SHOE_PRESS_NIP_LOAD_302A       : REAL := 1500.00; (* Shoe Press Calibrated Nip Linear Load Ch A [kN/m] *)
    WT_SHOE_PRESS_NIP_LOAD_302B       : REAL := 1500.00; (* Shoe Press Calibrated Nip Linear Load Ch B [kN/m] *)
    WT_SHOE_PRESS_NIP_LOAD_302C       : REAL := 1500.00; (* Shoe Press Calibrated Nip Linear Load Ch C [kN/m] *)

    (* 1.8: Dryer Section 1 (Preheat) Saturated Steam Pressure Transmitters [bar], Calibrated 0.0 .. 10.0 bar *)
    PT_DRYER_SEC1_STEAM_PRESS_401A    : REAL := 2.100;   (* Dryer Section 1 Steam Header Pressure Ch A [bar] *)
    PT_DRYER_SEC1_STEAM_PRESS_401B    : REAL := 2.100;   (* Dryer Section 1 Steam Header Pressure Ch B [bar] *)
    PT_DRYER_SEC1_STEAM_PRESS_401C    : REAL := 2.100;   (* Dryer Section 1 Steam Header Pressure Ch C [bar] *)

    (* 1.9: Dryer Section 4 (Main Evaporative) Steam Pressure Transmitters [bar], Calibrated 0.0 .. 10.0 bar *)
    PT_DRYER_SEC4_STEAM_PRESS_404A    : REAL := 4.850;   (* Dryer Section 4 Steam Header Pressure Ch A [bar] *)
    PT_DRYER_SEC4_STEAM_PRESS_404B    : REAL := 4.850;   (* Dryer Section 4 Steam Header Pressure Ch B [bar] *)
    PT_DRYER_SEC4_STEAM_PRESS_404C    : REAL := 4.850;   (* Dryer Section 4 Steam Header Pressure Ch C [bar] *)

    (* 1.10: Dryer Stationary Siphon Evacuation Differential Transmitters [kPa], Calibrated 0.0 .. 120.0 kPa *)
    DPS_DRYER_SIPHON_DIFF_PRESS_407A  : REAL := 48.20;   (* Siphon Evacuation Differential Pressure Ch A [kPa] *)
    DPS_DRYER_SIPHON_DIFF_PRESS_407B  : REAL := 48.20;   (* Siphon Evacuation Differential Pressure Ch B [kPa] *)
    DPS_DRYER_SIPHON_DIFF_PRESS_407C  : REAL := 48.20;   (* Siphon Evacuation Differential Pressure Ch C [kPa] *)

    (* 1.11: QCS Scanning Beta-Ray Radiometric Basis Weight Transmitters [g/m2], Calibrated 20.0 .. 300.0 g/m2 *)
    WT_SCANNER_BASIS_WEIGHT_501A      : REAL := 80.05;   (* On-Line Scanner Beta-Ray Basis Weight Ch A [g/m2] *)
    WT_SCANNER_BASIS_WEIGHT_501B      : REAL := 80.05;   (* On-Line Scanner Beta-Ray Basis Weight Ch B [g/m2] *)
    WT_SCANNER_BASIS_WEIGHT_501C      : REAL := 80.05;   (* On-Line Scanner Beta-Ray Basis Weight Ch C [g/m2] *)

    (* 1.12: QCS Scanning Infrared Spectroscopic Moisture Transmitters [%], Calibrated 0.0 .. 20.0 % H2O *)
    AT_SCANNER_IR_MOISTURE_502A       : REAL := 5.52;    (* On-Line Scanner Infrared Sheet Moisture Ch A [%] *)
    AT_SCANNER_IR_MOISTURE_502B       : REAL := 5.52;    (* On-Line Scanner Infrared Sheet Moisture Ch B [%] *)
    AT_SCANNER_IR_MOISTURE_502C       : REAL := 5.52;    (* On-Line Scanner Infrared Sheet Moisture Ch C [%] *)

    (* =================================================================================================================
     * SECTION 2: ADDITIONAL AUXILIARY PROCESS TRANSMITTERS & CRITICAL HARDWIRED SIGNALS
     * ================================================================================================================= *)
    (* Dryer Steam Pressure Transmitters Sections 2, 3, 5, 6 [bar] *)
    PT_DRYER_SEC2_STEAM_PRESS_402     : REAL := 3.250;   (* Dryer Section 2 Steam Pressure [bar] *)
    PT_DRYER_SEC3_STEAM_PRESS_403     : REAL := 4.100;   (* Dryer Section 3 Steam Pressure [bar] *)
    PT_DRYER_SEC5_STEAM_PRESS_405     : REAL := 3.900;   (* Dryer Section 5 Steam Pressure [bar] *)
    PT_DRYER_SEC6_STEAM_PRESS_406     : REAL := 2.300;   (* Dryer Section 6 Steam Pressure [bar] *)

    (* Headbox Pond Level and Dilution Header Pressures *)
    LT_HEADBOX_LIQUID_LEVEL_106       : REAL := 420.00;  (* Headbox Liquid Stock Pond Level [mm] *)
    PT_DILUTION_HEADER_105            : REAL := 520.00;  (* CD Dilution Profiling Water Header Pressure [kPa] *)

    (* Shoe Press Lubrication & Thermal Sensors *)
    TT_SHOE_PRESS_OIL_TEMP_303        : REAL := 58.50;   (* Shoe Press Recirculating Oil Sump Temp [deg C] *)
    ZT_SHOE_PRESS_OIL_FILM_304        : REAL := 28.50;   (* Measured Hydrodynamic Lubrication Film Thickness [um] *)

    (* Forming Wire Vacuum Couch & White Water Sensors *)
    DPS_COUCH_VACUUM_202              : REAL := -65.00;  (* Suction Couch Roll Vacuum Level [kPa] *)
    FT_WIRE_WHITE_WATER_TRAY_203      : REAL := 8200.00; (* Forming Section White Water Drainage Flow [m3/h] *)

    (* Dryer Infrared Sheet Surface Temperatures [deg C] *)
    TT_SHEET_TEMP_SEC1_408            : REAL := 62.50;   (* Sheet Surface Temperature Exiting Sec 1 [deg C] *)
    TT_SHEET_TEMP_SEC2_409            : REAL := 78.40;   (* Sheet Surface Temperature Exiting Sec 2 [deg C] *)
    TT_SHEET_TEMP_SEC3_410            : REAL := 89.20;   (* Sheet Surface Temperature Exiting Sec 3 [deg C] *)
    TT_SHEET_TEMP_SEC4_411            : REAL := 96.80;   (* Sheet Surface Temperature Exiting Sec 4 [deg C] *)
    TT_SHEET_TEMP_SEC5_412            : REAL := 92.10;   (* Sheet Surface Temperature Exiting Sec 5 [deg C] *)
    TT_SHEET_TEMP_SEC6_413            : REAL := 75.30;   (* Sheet Surface Temperature Exiting Sec 6 [deg C] *)

    (* Calender and Reel Process Sensors *)
    TT_CALENDER_ROLL_TEMP_503         : REAL := 142.00;  (* Soft Calender Induction Heated Roll Temp [deg C] *)
    WT_REEL_WEB_TENSION_601A          : REAL := 450.00;  (* Reel Web Tension Loadcell Ch A [N/m] *)
    WT_REEL_WEB_TENSION_601B          : REAL := 450.00;  (* Reel Web Tension Loadcell Ch B [N/m] *)
    WT_REEL_WEB_TENSION_601C          : REAL := 450.00;  (* Reel Web Tension Loadcell Ch C [N/m] *)

    (* High-Speed Optical Web Break Transmitters (< 15 ms detection time) *)
    OPT_WEB_BREAK_OPTICAL_701A        : BOOL := FALSE;   (* Optical Sheet Reflection Sensor Ch A (TRUE=Break) *)
    OPT_WEB_BREAK_OPTICAL_701B        : BOOL := FALSE;   (* Optical Sheet Reflection Sensor Ch B (TRUE=Break) *)
    OPT_WEB_BREAK_OPTICAL_701C        : BOOL := FALSE;   (* Optical Sheet Reflection Sensor Ch C (TRUE=Break) *)

    (* Cross-Direction Raw Profile Arrays from Traversing QCS Scanner (32 CD Bins across 8,500 mm Web) *)
    aScanner_CD_BasisWeight_Raw_gsm   : ARRAY[1..32] OF REAL; (* Measured CD Basis Weight Profile [g/m2] *)
    aScanner_CD_Moisture_Raw_pct      : ARRAY[1..32] OF REAL; (* Measured CD Moisture Profile [%] *)

    (* =================================================================================================================
     * SECTION 3: OPERATOR SETPOINTS & PRODUCTION RECIPE TARGETS
     * ================================================================================================================= *)
    rMachineSpeed_Target_mpm          : REAL := 1800.00; (* Production Line Target Velocity [m/min] *)
    rBasisWeight_SP_gsm               : REAL := 80.00;   (* Dry Basis Weight Quality Setpoint [g/m2] *)
    rMoisture_SP_pct                  : REAL := 5.50;    (* Reel Finished Moisture Quality Setpoint [%] *)
    rJetToWire_Ratio_SP               : REAL := 1.015;   (* Optimal Jet-to-Wire Spouting Ratio [-] *)
    rShoePress_LinearLoad_SP_kNm      : REAL := 1500.00; (* Target Shoe Press Compressive Load [kN/m] *)
    rReelTension_SP_Nm                : REAL := 450.00;  (* Reel Web Tension Quality Setpoint [N/m] *)
    rHeadboxPondLevel_SP_mm           : REAL := 420.00;  (* Headbox Liquid Stock Depth Setpoint [mm] *)

    (* Dryer Cascade Steam Group Setpoints [bar] *)
    rDryerSec1_SteamPress_SP_bar      : REAL := 2.100;   (* Section 1 Target Steam Pressure [bar] *)
    rDryerSec2_SteamPress_SP_bar      : REAL := 3.250;   (* Section 2 Target Steam Pressure [bar] *)
    rDryerSec3_SteamPress_SP_bar      : REAL := 4.100;   (* Section 3 Target Steam Pressure [bar] *)
    rDryerSec4_SteamPress_SP_bar      : REAL := 4.850;   (* Section 4 Target Steam Pressure [bar] *)
    rDryerSec5_SteamPress_SP_bar      : REAL := 3.900;   (* Section 5 Target Steam Pressure [bar] *)
    rDryerSec6_SteamPress_SP_bar      : REAL := 2.300;   (* Section 6 Target Steam Pressure [bar] *)

    (* =================================================================================================================
     * SECTION 4: MACHINE SUPERVISORY COMMANDS & INTERLOCK PERMISSIVES
     * ================================================================================================================= *)
    bMasterMachineEnable              : BOOL := TRUE;    (* Master Supervisory Machine Run Permissive *)
    bStartTailThreadingCmd            : BOOL := FALSE;   (* Operator Initiate Tail Threading Sequence *)
    bEngageFullWidthProductionCmd     : BOOL := FALSE;   (* Operator Expand Web to Full 8,500 mm Width *)
    bEnableCDProfileOptimization      : BOOL := TRUE;    (* Enable Closed-Loop CD Dilution & Slice Profile *)
    bAcknowledgeAlarmsCmd             : BOOL := FALSE;   (* Operator Alarm Reset & Acknowledge *)
    bEmergencyStopManual              : BOOL := FALSE;   (* Hardwired Field E-Stop Pushbutton Actuated *)
    bBrokePulperAgitatorRunning       : BOOL := TRUE;    (* Wet-End Broke Pit Pulper Drive Running Confirmation *)
    bLubricationLubePackReady         : BOOL := TRUE;    (* Shoe Press Hydraulic & Hydrodynamic Lubrication Ready *)
END_VAR
""")

    # -------------------------------------------------------------------------
    # PART 3: VAR_OUTPUT Declaration
    # -------------------------------------------------------------------------
    parts.append("""VAR_OUTPUT
    (* =================================================================================================================
     * SECTION 1: PRIMARY ACTUATOR COMMAND SIGNALS (SPEEDS, VALVES, CYLINDERS, PROFILERS)
     * ================================================================================================================= *)
    (* Headbox & Approach Flow Actuators *)
    rStockFanPump_SpeedCmd_pct        : REAL := 0.0;     (* Stock Fan Pump VFD Speed Reference [0.0 .. 100.0 %] *)
    rHeadboxAirPad_PressValve_pct     : REAL := 0.0;     (* Headbox Pressurized Air Pad Inflow Valve [0..100 %] *)
    rHeadboxAirPad_ExhaustValve_pct   : REAL := 0.0;     (* Headbox Air Pad Vent/Exhaust Valve [0..100 %] *)
    rSliceDilution_MasterHeaderValve_pct : REAL := 0.0;  (* Master Consistency Dilution Flow Header Valve [0..100 %] *)

    (* Cross-Direction Profile Actuator Arrays (32 CD Actuation Zones across 8,500 mm) *)
    aSliceDilution_ZoneValveCmd_pct   : ARRAY[1..32] OF REAL; (* CD Dilution Injection Proportional Valves [0..100 %] *)
    aSliceLip_ThermalActuatorPwr_pct  : ARRAY[1..32] OF REAL; (* CD Slice Lip Thermal Expansion Heating Rods [0..100 %] *)

    (* Forming Wire Drive & Dewatering Vacuum Valves *)
    rFormingWire_DriveSpeedCmd_mpm    : REAL := 0.0;     (* Forming Wire Section Sectional Drive Speed [m/min] *)
    rSuctionBox_VacuumControlValve_pct: REAL := 0.0;     (* Wire Flat Vacuum Box Modulating Control Valve [0..100 %] *)
    rCouchRoll_VacuumControlValve_pct : REAL := 0.0;     (* Suction Couch Roll Vacuum Regulating Valve [0..100 %] *)

    (* Shoe Press Hydraulic & Crown Balancing Actuators *)
    rShoePress_HydraulicServoCmd_pct  : REAL := 0.0;     (* Shoe Press Proportional Hydraulic Valve [0..100 %] *)
    rShoePress_TendingSideLoadCmd_kNm : REAL := 0.0;     (* Shoe Press Front (Tending) Edge Linear Load [kN/m] *)
    rShoePress_CenterLoadCmd_kNm      : REAL := 0.0;     (* Shoe Press Center Crown Linear Load [kN/m] *)
    rShoePress_DriveSideLoadCmd_kNm   : REAL := 0.0;     (* Shoe Press Back (Drive) Edge Linear Load [kN/m] *)

    (* 6-Section Steam Dryer Cascade Control Valves *)
    rDryerSec1_SteamValveCmd_pct      : REAL := 0.0;     (* Section 1 Main Steam Control Valve [0..100 %] *)
    rDryerSec2_SteamValveCmd_pct      : REAL := 0.0;     (* Section 2 Main Steam Control Valve [0..100 %] *)
    rDryerSec3_SteamValveCmd_pct      : REAL := 0.0;     (* Section 3 Main Steam Control Valve [0..100 %] *)
    rDryerSec4_SteamValveCmd_pct      : REAL := 0.0;     (* Section 4 Main Steam Control Valve [0..100 %] *)
    rDryerSec5_SteamValveCmd_pct      : REAL := 0.0;     (* Section 5 Main Steam Control Valve [0..100 %] *)
    rDryerSec6_SteamValveCmd_pct      : REAL := 0.0;     (* Section 6 Main Steam Control Valve [0..100 %] *)
    rDryerSiphon_DiffPressValve_pct   : REAL := 0.0;     (* Stationary Siphon Diff Pressure Blow-Through Valve [0..100 %] *)
    rDryerBlowThrough_RecycleValve_pct: REAL := 0.0;     (* Thermocompressor Steam Recompression Valve [0..100 %] *)

    (* Calender Induction Heating & Reel Web Winding *)
    aCalender_InductionHeaterPwr_pct  : ARRAY[1..16] OF REAL; (* Multi-Zone Calender Induction Roll Heaters [0..100 %] *)
    rReel_DriveTorqueCmd_Nm           : REAL := 0.0;     (* Surface Reel Drum Master Drive Torque Reference [N*m] *)

    (* Fast-Acting Emergency Safeguard Actuation Signals *)
    bStockDumpValve_ToBrokePulper     : BOOL := FALSE;   (* Rapid Stock Diverter Valve to Broke Pit (TRUE=Dump) *)
    bShoePress_EmergencyNipOpen       : BOOL := FALSE;   (* Fast Hydraulic Nip Separation Solenoid (TRUE=Open) *)
    bDryerSteam_FastSetbackVent       : BOOL := FALSE;   (* Rapid Steam Depressurization & Venting (TRUE=Vent) *)
    bCalender_RapidRollSeparate       : BOOL := FALSE;   (* Calender Roll Quick-Drop Pneumatic Separation *)

    (* =================================================================================================================
     * SECTION 2: OBSERVED PROCESS CHARACTERISTICS & CYBER-PHYSICAL ESTIMATES
     * ================================================================================================================= *)
    rObserved_JetSpeed_mps            : REAL := 0.0;     (* Bernoulli Calculated Slice Spouting Velocity [m/s] *)
    rObserved_WireSpeed_mps           : REAL := 0.0;     (* Forming Wire Calibrated Linear Velocity [m/s] *)
    rObserved_JetToWireRatio          : REAL := 0.0;     (* Hydrodynamic Velocity Spouting Ratio [v_jet / v_wire] *)
    rObserved_ShoeOilFilm_um          : REAL := 0.0;     (* Hydrodynamic Lubricating Fluid Film Thickness [um] *)
    rObserved_PressDrySolids_pct      : REAL := 0.0;     (* Estimated Sheet Dry Solids Content After Shoe Press [%] *)
    rObserved_DryerEvapRate_Total_kgh : REAL := 0.0;     (* Total Cumulative Water Evaporation Rate [kg/h] *)
    rObserved_ReelDrySolids_pct       : REAL := 0.0;     (* Final Web Dry Solids Content at Reel [%] *)
    rObserved_BasisWeightAvg_gsm      : REAL := 0.0;     (* Scan-Averaged True Basis Weight [g/m2] *)
    rObserved_MoistureAvg_pct         : REAL := 0.0;     (* Scan-Averaged True Finished Moisture [%] *)
    rObserved_CD_2Sigma_BW            : REAL := 0.0;     (* Cross-Direction Basis Weight 2-Sigma Variation [g/m2] *)
    rObserved_CD_2Sigma_Moist         : REAL := 0.0;     (* Cross-Direction Moisture 2-Sigma Variation [%] *)

    (* =================================================================================================================
     * SECTION 3: FINITE STATE MACHINE, ISA-18.2 ALARMS & DIAGNOSTIC PACKING
     * ================================================================================================================= *)
    iActiveFSM_State                  : INT := 1;        (* Numeric Machine Operating Sequence State [1..12] *)
    sActiveFSM_StateName              : STRING[40] := 'STANDBY_WARM_CIRCULATION'; (* Human-Readable State String *)
    wAlarmWord_Critical_ISA18         : DWORD := 16#00000000; (* Priority 1 Critical Trip Alarm Bitmask *)
    wAlarmWord_Warning_ISA18          : DWORD := 16#00000000; (* Priority 2 Process Operating Warning Bitmask *)
    wAlarmWord_Advisory_ISA18         : DWORD := 16#00000000; (* Priority 3 Advisory Notice Bitmask *)
    wDiagnosticState_Word             : DWORD := 16#00000000; (* Packed Machine Health and Subsystem Status Word *)
    wTMR_ChannelFaultMask             : DWORD := 16#00000000; (* Packed TMR Sensor Discrepancy Failure Bitmask *)
    bWebBreakActive                   : BOOL := FALSE;   (* Active Sheet Break Status (Optical Fast Interlock) *)
    bMachineInInterlock               : BOOL := FALSE;   (* Hardwired Machine Interlock Circuit Tripped *)
    bMachineRunningAtTarget           : BOOL := FALSE;   (* Paper Machine Steady-State Production Reached *)
END_VAR
""")

    # -------------------------------------------------------------------------
    # PART 4: VAR Declaration (Internal States, MPC, TMR, Observers, Alarms)
    # -------------------------------------------------------------------------
    parts.append("""VAR
    (* =================================================================================================================
     * SECTION 1: EXECUTION CYCLE & TIME CONSTANTS
     * ================================================================================================================= *)
    c_rCycleTime_s                    : REAL := 0.010;   (* Scan Interrupt Task Sample Interval (10 ms) [s] *)
    c_rGravity_mps2                   : REAL := 9.80665; (* Standard Acceleration of Gravity [m/s2] *)
    c_rWaterDensity_kgm3              : REAL := 1000.00; (* Fluid Stock Slurry Reference Density [kg/m3] *)
    c_rWebTrimWidth_m                 : REAL := 8.500;   (* Fourdrinier Machine Nominal Trim Width [m] *)

    (* =================================================================================================================
     * SECTION 2: 2oo3 TMR SENSOR VOTING STRUCTURES, DISCREPANCY TIMERS & DEGRADATION MASKS
     * ================================================================================================================= *)
    (* Voted Process Variables *)
    rVoted_HeadboxTotalHead_kPa       : REAL := 468.30;
    rVoted_StockFlow_m3h              : REAL := 9850.00;
    rVoted_ThinStockConsistency_pct   : REAL := 0.750;
    rVoted_FormingWireSpeed_mpm       : REAL := 1800.00;
    rVoted_WireSuctionBox_kPa         : REAL := -42.50;
    rVoted_ShoePressHydPressure_bar   : REAL := 215.00;
    rVoted_ShoePressNipLoad_kNm       : REAL := 1500.00;
    rVoted_DryerSec1Steam_bar         : REAL := 2.100;
    rVoted_DryerSec4Steam_bar         : REAL := 4.850;
    rVoted_DryerSiphonDiff_kPa        : REAL := 48.20;
    rVoted_BasisWeight_gsm            : REAL := 80.05;
    rVoted_Moisture_pct               : REAL := 5.52;
    rVoted_ReelTension_Nm             : REAL := 450.00;
    bVoted_WebBreak_Optical           : BOOL := FALSE;

    (* TMR Channel Discrepancy Fault Accumulator Timers [s] *)
    tTMR_HeadboxPress_DiscrepTimer    : REAL := 0.0;
    tTMR_StockFlow_DiscrepTimer       : REAL := 0.0;
    tTMR_Consistency_DiscrepTimer     : REAL := 0.0;
    tTMR_WireSpeed_DiscrepTimer       : REAL := 0.0;
    tTMR_SuctionBox_DiscrepTimer      : REAL := 0.0;
    tTMR_ShoeHydPress_DiscrepTimer    : REAL := 0.0;
    tTMR_ShoeNipLoad_DiscrepTimer     : REAL := 0.0;
    tTMR_DryerSec1_DiscrepTimer       : REAL := 0.0;
    tTMR_DryerSec4_DiscrepTimer       : REAL := 0.0;
    tTMR_SiphonDiff_DiscrepTimer      : REAL := 0.0;
    tTMR_BasisWeight_DiscrepTimer     : REAL := 0.0;
    tTMR_Moisture_DiscrepTimer        : REAL := 0.0;
    tTMR_ReelTension_DiscrepTimer     : REAL := 0.0;

    (* TMR Discrepancy Fault Flags per Subsystem *)
    bTMR_HeadboxPress_Degraded        : BOOL := FALSE;
    bTMR_StockFlow_Degraded           : BOOL := FALSE;
    bTMR_Consistency_Degraded         : BOOL := FALSE;
    bTMR_WireSpeed_Degraded           : BOOL := FALSE;
    bTMR_SuctionBox_Degraded          : BOOL := FALSE;
    bTMR_ShoeHydPress_Degraded        : BOOL := FALSE;
    bTMR_ShoeNipLoad_Degraded         : BOOL := FALSE;
    bTMR_DryerSec1_Degraded           : BOOL := FALSE;
    bTMR_DryerSec4_Degraded           : BOOL := FALSE;
    bTMR_SiphonDiff_Degraded          : BOOL := FALSE;
    bTMR_BasisWeight_Degraded         : BOOL := FALSE;
    bTMR_Moisture_Degraded            : BOOL := FALSE;
    bTMR_ReelTension_Degraded         : BOOL := FALSE;

    (* Sensor Discrepancy Tolerances (Engineering Units) *)
    c_rTol_HeadboxPress_kPa           : REAL := 4.50;    (* Discrepancy limit: 4.5 kPa *)
    c_rTol_StockFlow_m3h              : REAL := 120.00;  (* Discrepancy limit: 120 m3/h *)
    c_rTol_Consistency_pct            : REAL := 0.035;   (* Discrepancy limit: 0.035 % *)
    c_rTol_WireSpeed_mpm              : REAL := 5.00;    (* Discrepancy limit: 5.0 m/min *)
    c_rTol_SuctionBox_kPa             : REAL := 2.50;    (* Discrepancy limit: 2.5 kPa *)
    c_rTol_ShoeHydPress_bar           : REAL := 4.00;    (* Discrepancy limit: 4.0 bar *)
    c_rTol_ShoeNipLoad_kNm            : REAL := 25.00;   (* Discrepancy limit: 25 kN/m *)
    c_rTol_DryerSec1_bar              : REAL := 0.120;   (* Discrepancy limit: 0.12 bar *)
    c_rTol_DryerSec4_bar              : REAL := 0.150;   (* Discrepancy limit: 0.15 bar *)
    c_rTol_SiphonDiff_kPa             : REAL := 3.00;    (* Discrepancy limit: 3.0 kPa *)
    c_rTol_BasisWeight_gsm            : REAL := 0.65;    (* Discrepancy limit: 0.65 g/m2 *)
    c_rTol_Moisture_pct               : REAL := 0.25;    (* Discrepancy limit: 0.25 % *)
    c_rTol_ReelTension_Nm             : REAL := 15.00;   (* Discrepancy limit: 15 N/m *)
    c_rDebounceDelay_s                : REAL := 0.050;   (* 50 ms Debounce Persistence Threshold *)

    (* =================================================================================================================
     * SECTION 3: 8x8 MULTIVARIABLE DISCRETE STATE-SPACE MPC MATRICES (Ts = 0.010 s)
     * States x = [ x1: Delta Headbox Total Head [kPa]
     *              x2: Delta Headbox Pond Level [mm]
     *              x3: Delta Thin Stock Consistency [%*100]
     *              x4: Delta Jet-to-Wire Ratio [- * 1000]
     *              x5: Delta Shoe Press Linear Load [kN/m]
     *              x6: Delta Dryer Sec 1-3 Evap Steam Pressure [bar*10]
     *              x7: Delta Dryer Sec 4-6 Evap Steam Pressure [bar*10]
     *              x8: Delta Final Reel Basis Weight [g/m2] ]
     *
     * Inputs u = [ u1: Fan Pump Speed VFD Trim [%]
     *              u2: Air Pad Pressurization / Exhaust Valve Trim [%]
     *              u3: CD Dilution Master Header Trim [%]
     *              u4: Forming Wire Section Speed Reference Trim [%]
     *              u5: Shoe Press Hydraulic Proportional Servo Valve Trim [%]
     *              u6: Dryer Section 1-3 Steam Valve Trim [%]
     *              u7: Dryer Section 4-6 Steam Valve Trim [%]
     *              u8: CD Thermal Slice Lip Master Energy Trim [%] ]
     * ================================================================================================================= *)
    (* Discrete State Transition Matrix A (8x8) *)
    A_mat_11 : REAL := 0.9420; A_mat_12 : REAL := 0.0185; A_mat_13 : REAL := 0.0000; A_mat_14 : REAL := 0.0000;
    A_mat_15 : REAL := 0.0000; A_mat_16 : REAL := 0.0000; A_mat_17 : REAL := 0.0000; A_mat_18 : REAL := 0.0000;

    A_mat_21 : REAL := 0.0125; A_mat_22 : REAL := 0.9650; A_mat_23 : REAL := 0.0000; A_mat_24 : REAL := 0.0000;
    A_mat_25 : REAL := 0.0000; A_mat_26 : REAL := 0.0000; A_mat_27 : REAL := 0.0000; A_mat_28 : REAL := 0.0000;

    A_mat_31 : REAL := 0.0000; A_mat_32 : REAL := 0.0000; A_mat_33 : REAL := 0.9250; A_mat_34 : REAL := 0.0000;
    A_mat_35 : REAL := 0.0000; A_mat_36 : REAL := 0.0000; A_mat_37 : REAL := 0.0000; A_mat_38 : REAL := 0.0000;

    A_mat_41 : REAL := 0.0385; A_mat_42 : REAL := 0.0000; A_mat_43 : REAL := 0.0000; A_mat_44 : REAL := 0.9120;
    A_mat_45 : REAL := 0.0000; A_mat_46 : REAL := 0.0000; A_mat_47 : REAL := 0.0000; A_mat_48 : REAL := 0.0000;

    A_mat_51 : REAL := 0.0000; A_mat_52 : REAL := 0.0000; A_mat_53 : REAL := 0.0000; A_mat_54 : REAL := 0.0000;
    A_mat_55 : REAL := 0.9380; A_mat_56 : REAL := 0.0000; A_mat_57 : REAL := 0.0000; A_mat_58 : REAL := 0.0000;

    A_mat_61 : REAL := 0.0000; A_mat_62 : REAL := 0.0000; A_mat_63 : REAL := 0.0000; A_mat_64 : REAL := 0.0000;
    A_mat_65 : REAL := 0.0042; A_mat_66 : REAL := 0.9550; A_mat_67 : REAL := 0.0180; A_mat_68 : REAL := 0.0000;

    A_mat_71 : REAL := 0.0000; A_mat_72 : REAL := 0.0000; A_mat_73 : REAL := 0.0000; A_mat_74 : REAL := 0.0000;
    A_mat_75 : REAL := 0.0028; A_mat_76 : REAL := 0.0210; A_mat_77 : REAL := 0.9620; A_mat_78 : REAL := 0.0000;

    A_mat_81 : REAL := 0.0150; A_mat_82 : REAL := 0.0000; A_mat_83 : REAL := 0.0820; A_mat_84 : REAL := 0.0045;
    A_mat_85 : REAL := -0.0120; A_mat_86 : REAL := 0.0000; A_mat_87 : REAL := 0.0000; A_mat_88 : REAL := 0.9810;

    (* Discrete Input Coupling Matrix B (8x8) *)
    B_mat_11 : REAL := 0.0520; B_mat_12 : REAL := 0.0410; B_mat_13 : REAL := 0.0000; B_mat_14 : REAL := 0.0000;
    B_mat_15 : REAL := 0.0000; B_mat_16 : REAL := 0.0000; B_mat_17 : REAL := 0.0000; B_mat_18 : REAL := 0.0000;

    B_mat_21 : REAL := 0.0380; B_mat_22 : REAL := -0.0450; B_mat_23 : REAL := 0.0000; B_mat_24 : REAL := 0.0000;
    B_mat_25 : REAL := 0.0000; B_mat_26 : REAL := 0.0000; B_mat_27 : REAL := 0.0000; B_mat_28 : REAL := 0.0000;

    B_mat_31 : REAL := 0.0000; B_mat_32 : REAL := 0.0000; B_mat_33 : REAL := -0.0680; B_mat_34 : REAL := 0.0000;
    B_mat_35 : REAL := 0.0000; B_mat_36 : REAL := 0.0000; B_mat_37 : REAL := 0.0000; B_mat_38 : REAL := 0.0000;

    B_mat_41 : REAL := 0.0420; B_mat_42 : REAL := 0.0000; B_mat_43 : REAL := 0.0000; B_mat_44 : REAL := -0.0780;
    B_mat_45 : REAL := 0.0000; B_mat_46 : REAL := 0.0000; B_mat_47 : REAL := 0.0000; B_mat_48 : REAL := 0.0000;

    B_mat_51 : REAL := 0.0000; B_mat_52 : REAL := 0.0000; B_mat_53 : REAL := 0.0000; B_mat_54 : REAL := 0.0000;
    B_mat_55 : REAL := 0.0860; B_mat_56 : REAL := 0.0000; B_mat_57 : REAL := 0.0000; B_mat_58 : REAL := 0.0000;

    B_mat_61 : REAL := 0.0000; B_mat_62 : REAL := 0.0000; B_mat_63 : REAL := 0.0000; B_mat_64 : REAL := 0.0000;
    B_mat_65 : REAL := 0.0000; B_mat_66 : REAL := 0.0480; B_mat_67 : REAL := 0.0000; B_mat_68 : REAL := 0.0000;

    B_mat_71 : REAL := 0.0000; B_mat_72 : REAL := 0.0000; B_mat_73 : REAL := 0.0000; B_mat_74 : REAL := 0.0000;
    B_mat_75 : REAL := 0.0000; B_mat_76 : REAL := 0.0000; B_mat_77 : REAL := 0.0540; B_mat_78 : REAL := 0.0000;

    B_mat_81 : REAL := 0.0120; B_mat_82 : REAL := 0.0000; B_mat_83 : REAL := -0.0420; B_mat_84 : REAL := -0.0280;
    B_mat_85 : REAL := -0.0080; B_mat_86 : REAL := 0.0000; B_mat_87 : REAL := 0.0000; B_mat_88 : REAL := 0.0180;

    (* MPC Quadratic State Error Penalty Diagonal Weights Q (8x8) *)
    Q_w1 : REAL := 12.0;  (* Headbox Pressure Weight *)
    Q_w2 : REAL := 8.5;   (* Headbox Pond Level Weight *)
    Q_w3 : REAL := 15.0;  (* Consistency Weight *)
    Q_w4 : REAL := 25.0;  (* Jet-to-Wire Speed Ratio Weight *)
    Q_w5 : REAL := 10.0;  (* Shoe Press Nip Load Weight *)
    Q_w6 : REAL := 6.0;   (* Dryer Sec 1-3 Pressure Weight *)
    Q_w7 : REAL := 7.5;   (* Dryer Sec 4-6 Pressure Weight *)
    Q_w8 : REAL := 30.0;  (* Reel Basis Weight Primary Quality Weight *)

    (* MPC Actuator Slew Rate Suppression Diagonal Weights R (8x8) *)
    R_w1 : REAL := 1.20;  (* Fan Pump VFD Slew Penalty *)
    R_w2 : REAL := 0.85;  (* Air Pad Valve Slew Penalty *)
    R_w3 : REAL := 1.10;  (* CD Dilution Valve Slew Penalty *)
    R_w4 : REAL := 2.50;  (* Wire Drive Velocity Slew Penalty *)
    R_w5 : REAL := 1.50;  (* Shoe Press Servo Slew Penalty *)
    R_w6 : REAL := 0.90;  (* Steam Sec 1-3 Slew Penalty *)
    R_w7 : REAL := 0.95;  (* Steam Sec 4-6 Slew Penalty *)
    R_w8 : REAL := 1.80;  (* CD Thermal Rod Slew Penalty *)

    (* State Vector Registers x[k], x_pred[k+1] and Actuator Vectors u[k], Delta_u[k] *)
    x_k1 : REAL := 0.0; x_k2 : REAL := 0.0; x_k3 : REAL := 0.0; x_k4 : REAL := 0.0;
    x_k5 : REAL := 0.0; x_k6 : REAL := 0.0; x_k7 : REAL := 0.0; x_k8 : REAL := 0.0;

    x_pred1 : REAL := 0.0; x_pred2 : REAL := 0.0; x_pred3 : REAL := 0.0; x_pred4 : REAL := 0.0;
    x_pred5 : REAL := 0.0; x_pred6 : REAL := 0.0; x_pred7 : REAL := 0.0; x_pred8 : REAL := 0.0;

    u_cmd1 : REAL := 65.0; u_cmd2 : REAL := 45.0; u_cmd3 : REAL := 50.0; u_cmd4 : REAL := 1800.0;
    u_cmd5 : REAL := 72.0; u_cmd6 : REAL := 38.0; u_cmd7 : REAL := 58.0; u_cmd8 : REAL := 50.0;

    (* =================================================================================================================
     * SECTION 4: THERMODYNAMIC, HYDRODYNAMIC & MASS BALANCE OBSERVER VARIABLES
     * ================================================================================================================= *)
    (* Headbox Bernoulli Jet & Slice Geometry Variables *)
    rHeadboxPondStockHead_m           : REAL := 0.0;     (* Liquid Stock Static Head [m] *)
    rHeadboxAirPadHead_m              : REAL := 0.0;     (* Air Cushion Equivalent Hydraulic Head [m] *)
    rHeadboxTotalEffectiveHead_m      : REAL := 0.0;     (* Total Bernoulli Hydrodynamic Head [m] *)
    rTheoreticalSpoutingJetVelocity   : REAL := 0.0;     (* Theoretical Jet Spouting Velocity [m/s] *)
    rDischargeCoefficient_Cd          : REAL := 0.982;   (* Slice Lip Hydrodynamic Discharge Orifice Coeff *)
    rActualJetVelocity_mps            : REAL := 0.0;     (* Actual Stock Jet Velocity at Wire Impingement [m/s] *)
    rWireVelocity_mps                 : REAL := 0.0;     (* Forming Fabric Surface Velocity [m/s] *)

    (* Shoe Press Hydrodynamic Oil Film Observer (Reynolds/Vogel Viscosity Model) *)
    (* mu(T) = mu_0 * exp(b / (T + c)) *)
    c_rOilViscosity_Zero_Pa_s         : REAL := 0.00185; (* Base Kinematic Viscosity Constant [Pa*s] *)
    c_rOilViscosity_Beta              : REAL := 820.00;  (* Vogel Temperature Sensitivity Coeff [deg C] *)
    c_rOilViscosity_T0                : REAL := 95.00;   (* Vogel Reference Shift [deg C] *)
    rCalculated_OilViscosity_Pas      : REAL := 0.045;   (* Current In-Nip Hydrodynamic Oil Viscosity [Pa*s] *)
    rShoePress_SpecificPressure_MPa   : REAL := 6.25;    (* Average Hydrostatic Shoe Pressure in Nip [MPa] *)
    rShoePress_HydrodynamicFilm_um    : REAL := 28.5;    (* Calculated Floating Belt Fluid Film [um] *)

    (* Dewatering & Dry Solids Mass Balance Progression *)
    rWireDrySolids_pct                : REAL := 19.8;    (* Solids Leaving Forming Couch Roll [%] *)
    rShoePressExitSolids_pct          : REAL := 48.5;    (* Solids Exiting Extended Nip Press [%] *)
    rDryerSec1ExitSolids_pct          : REAL := 56.2;    (* Solids Exiting Dryer Section 1 [%] *)
    rDryerSec2ExitSolids_pct          : REAL := 65.8;    (* Solids Exiting Dryer Section 2 [%] *)
    rDryerSec3ExitSolids_pct          : REAL := 76.4;    (* Solids Exiting Dryer Section 3 [%] *)
    rDryerSec4ExitSolids_pct          : REAL := 86.5;    (* Solids Exiting Dryer Section 4 [%] *)
    rDryerSec5ExitSolids_pct          : REAL := 92.2;    (* Solids Exiting Dryer Section 5 [%] *)
    rDryerSec6ExitSolids_pct          : REAL := 94.5;    (* Solids Exiting Dryer Section 6 (Reel) [%] *)

    (* Steam Dryer Enthalpy & Evaporation Observers *)
    (* Latent Heat Delta H_vap(P) = 2257.0 - 2.45*(T_sat - 100.0) [kJ/kg] *)
    rLatentHeat_Sec1_kJkg             : REAL := 2200.0;
    rLatentHeat_Sec4_kJkg             : REAL := 2120.0;
    rEvaporationRate_Sec1_kgh         : REAL := 4200.0;
    rEvaporationRate_Sec4_kgh         : REAL := 8850.0;
    rTotalEvaporation_kgh             : REAL := 32500.0;

    (* =================================================================================================================
     * SECTION 5: CROSS-DIRECTION (CD) BASIS WEIGHT & MOISTURE PROFILING MATRICES
     * ================================================================================================================= *)
    (* Spatial Decoupling Interaction Matrix M_CD (Toeplitz 3-Point Tridiagonal Smear Profile) *)
    (* Zone effect: Center = 0.68, Adjacent Neighbors = 0.16 each *)
    c_rCD_CouplingCenter              : REAL := 0.680;
    c_rCD_CouplingNeighbor            : REAL := 0.160;

    aCD_BasisWeight_Filtered_gsm      : ARRAY[1..32] OF REAL;
    aCD_Moisture_Filtered_pct         : ARRAY[1..32] OF REAL;
    aCD_BW_Error_gsm                  : ARRAY[1..32] OF REAL;
    aCD_Moist_Error_pct               : ARRAY[1..32] OF REAL;
    aCD_DilutionTrim_pct              : ARRAY[1..32] OF REAL;
    aCD_ThermalExpansionTrim_pct      : ARRAY[1..32] OF REAL;
    aCD_CalenderInductionTrim_pct     : ARRAY[1..16] OF REAL;

    iCD_ZoneIdx                       : INT := 1;
    rCD_SumBW                         : REAL := 0.0;
    rCD_SumMoist                      : REAL := 0.0;
    rCD_VarBW                         : REAL := 0.0;
    rCD_VarMoist                      : REAL := 0.0;

    (* =================================================================================================================
     * SECTION 6: ISA-18.2 MULTI-TIERED ALARM SETPOINTS, DEADBANDS & INTERLOCK TIMERS
     * ================================================================================================================= *)
    (* Headbox Pressure Trip Thresholds [kPa] *)
    c_rTrip_HB_Press_HI_HI            : REAL := 540.0;
    c_rTrip_HB_Press_HI               : REAL := 510.0;
    c_rTrip_HB_Press_LO               : REAL := 420.0;
    c_rTrip_HB_Press_LO_LO            : REAL := 380.0;
    c_rDeadband_HB_Press              : REAL := 5.0;

    (* Shoe Press Linear Load Trip Thresholds [kN/m] *)
    c_rTrip_ShoeLoad_HI_HI            : REAL := 1750.0;
    c_rTrip_ShoeLoad_HI               : REAL := 1620.0;
    c_rTrip_ShoeLoad_LO               : REAL := 1300.0;
    c_rTrip_ShoeLoad_LO_LO            : REAL := 1100.0;
    c_rDeadband_ShoeLoad              : REAL := 15.0;

    (* Shoe Press Oil Film Thickness Min Thresholds [um] *)
    c_rTrip_OilFilm_LO                : REAL := 20.0;
    c_rTrip_OilFilm_LO_LO             : REAL := 14.0;
    c_rDeadband_OilFilm               : REAL := 1.5;

    (* Dryer Steam Pressure Trip Thresholds Sec 4 [bar] *)
    c_rTrip_DryerSec4_HI_HI           : REAL := 7.00;
    c_rTrip_DryerSec4_HI              : REAL := 6.20;
    c_rTrip_DryerSec4_LO              : REAL := 3.20;
    c_rTrip_DryerSec4_LO_LO           : REAL := 2.50;
    c_rDeadband_Dryer                 : REAL := 0.15;

    (* Dryer Siphon Evacuation Differential Min Threshold [kPa] *)
    c_rTrip_SiphonDiff_LO             : REAL := 28.0;
    c_rTrip_SiphonDiff_LO_LO          : REAL := 18.0;
    c_rDeadband_SiphonDiff            : REAL := 2.0;

    (* Reel Web Tension Low Snap Threshold [N/m] *)
    c_rTrip_ReelTension_LO_LO         : REAL := 180.0;
    c_rTrip_ReelTension_HI_HI         : REAL := 620.0;
    c_rDeadband_ReelTension           : REAL := 12.0;

    (* Rate-of-Change (ROC) Tension Snap Observer *)
    rReelTension_Prev                 : REAL := 450.0;
    rReelTension_ROC                  : REAL := 0.0;
    c_rTrip_ReelTension_ROC_Snap      : REAL := -3500.0; (* N/m/s *)

    (* Alarm Status Flags *)
    bAlarm_HB_Press_HI_HI             : BOOL := FALSE;
    bAlarm_HB_Press_HI                : BOOL := FALSE;
    bAlarm_HB_Press_LO                : BOOL := FALSE;
    bAlarm_HB_Press_LO_LO             : BOOL := FALSE;

    bAlarm_ShoeLoad_HI_HI             : BOOL := FALSE;
    bAlarm_ShoeLoad_HI                : BOOL := FALSE;
    bAlarm_ShoeLoad_LO                : BOOL := FALSE;
    bAlarm_ShoeLoad_LO_LO             : BOOL := FALSE;

    bAlarm_OilFilm_LO                 : BOOL := FALSE;
    bAlarm_OilFilm_LO_LO              : BOOL := FALSE;

    bAlarm_DryerSec4_HI_HI            : BOOL := FALSE;
    bAlarm_DryerSec4_HI               : BOOL := FALSE;
    bAlarm_DryerSec4_LO               : BOOL := FALSE;
    bAlarm_DryerSec4_LO_LO            : BOOL := FALSE;

    bAlarm_SiphonDiff_LO              : BOOL := FALSE;
    bAlarm_SiphonDiff_LO_LO           : BOOL := FALSE;

    bAlarm_ReelTension_HI_HI          : BOOL := FALSE;
    bAlarm_ReelTension_LO_LO          : BOOL := FALSE;
    bAlarm_ReelTension_SnapROC        : BOOL := FALSE;

    (* Fast Web Break Event Register *)
    bWebBreakOpticalDetected          : BOOL := FALSE;
    tWebBreakPersistenceTimer         : REAL := 0.0;

    (* =================================================================================================================
     * SECTION 7: 12-STAGE OPERATIONAL FINITE STATE MACHINE (FSM) VARIABLES
     * ================================================================================================================= *)
    iFSM_CurrentState                 : INT := 1;
    iFSM_NextState                    : INT := 1;
    tFSM_StateTimer_s                 : REAL := 0.0;
    bFSM_TransitionRequested          : BOOL := FALSE;

    (* State Timers & Stabilizing Delays *)
    tTailThreadingDwell_s             : REAL := 0.0;
    tFullWidthRampDwell_s             : REAL := 0.0;
    tBrokeFlushingDwell_s             : REAL := 0.0;
    tEmergencyDumpDwell_s             : REAL := 0.0;
END_VAR
""")

    # -------------------------------------------------------------------------
    # PART 5: Code Body - Phase 1: 2oo3 TMR Voting Logic
    # -------------------------------------------------------------------------
    parts.append("""(* =====================================================================================================
 * PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) PROCESS SENSOR VOTING ENGINE
 * Executes robust pairwise voting with tolerance bounds, discrepancy debounce timers and bumpless degradation.
 * ===================================================================================================== *)

(* --- 1.1: Headbox Total Head Pressure Voting [PT_HEADBOX_TOTAL_HEAD_101A/B/C] --- *)
IF (ABS(PT_HEADBOX_TOTAL_HEAD_101A - PT_HEADBOX_TOTAL_HEAD_101B) <= c_rTol_HeadboxPress_kPa) AND
   (ABS(PT_HEADBOX_TOTAL_HEAD_101A - PT_HEADBOX_TOTAL_HEAD_101C) <= c_rTol_HeadboxPress_kPa) THEN
    (* All 3 channels agree: Median of 3 *)
    rVoted_HeadboxTotalHead_kPa := PT_HEADBOX_TOTAL_HEAD_101A;
    tTMR_HeadboxPress_DiscrepTimer := 0.0;
    bTMR_HeadboxPress_Degraded := FALSE;
ELSIF ABS(PT_HEADBOX_TOTAL_HEAD_101A - PT_HEADBOX_TOTAL_HEAD_101B) <= c_rTol_HeadboxPress_kPa THEN
    (* Ch A and Ch B agree; Ch C divergent *)
    rVoted_HeadboxTotalHead_kPa := (PT_HEADBOX_TOTAL_HEAD_101A + PT_HEADBOX_TOTAL_HEAD_101B) * 0.50;
    tTMR_HeadboxPress_DiscrepTimer := tTMR_HeadboxPress_DiscrepTimer + c_rCycleTime_s;
    IF tTMR_HeadboxPress_DiscrepTimer >= c_rDebounceDelay_s THEN
        bTMR_HeadboxPress_Degraded := TRUE;
    END_IF;
ELSIF ABS(PT_HEADBOX_TOTAL_HEAD_101B - PT_HEADBOX_TOTAL_HEAD_101C) <= c_rTol_HeadboxPress_kPa THEN
    (* Ch B and Ch C agree; Ch A divergent *)
    rVoted_HeadboxTotalHead_kPa := (PT_HEADBOX_TOTAL_HEAD_101B + PT_HEADBOX_TOTAL_HEAD_101C) * 0.50;
    tTMR_HeadboxPress_DiscrepTimer := tTMR_HeadboxPress_DiscrepTimer + c_rCycleTime_s;
    IF tTMR_HeadboxPress_DiscrepTimer >= c_rDebounceDelay_s THEN
        bTMR_HeadboxPress_Degraded := TRUE;
    END_IF;
ELSIF ABS(PT_HEADBOX_TOTAL_HEAD_101C - PT_HEADBOX_TOTAL_HEAD_101A) <= c_rTol_HeadboxPress_kPa THEN
    (* Ch C and Ch A agree; Ch B divergent *)
    rVoted_HeadboxTotalHead_kPa := (PT_HEADBOX_TOTAL_HEAD_101C + PT_HEADBOX_TOTAL_HEAD_101A) * 0.50;
    tTMR_HeadboxPress_DiscrepTimer := tTMR_HeadboxPress_DiscrepTimer + c_rCycleTime_s;
    IF tTMR_HeadboxPress_DiscrepTimer >= c_rDebounceDelay_s THEN
        bTMR_HeadboxPress_Degraded := TRUE;
    END_IF;
ELSE
    (* Total TMR divergence: Freeze last known good value *)
    tTMR_HeadboxPress_DiscrepTimer := tTMR_HeadboxPress_DiscrepTimer + c_rCycleTime_s;
    bTMR_HeadboxPress_Degraded := TRUE;
END_IF;

(* --- 1.2: Approach Flow Fan Pump Volumetric Flow Voting [FT_STOCK_FEED_PUMP_102A/B/C] --- *)
IF (ABS(FT_STOCK_FEED_PUMP_102A - FT_STOCK_FEED_PUMP_102B) <= c_rTol_StockFlow_m3h) AND
   (ABS(FT_STOCK_FEED_PUMP_102A - FT_STOCK_FEED_PUMP_102C) <= c_rTol_StockFlow_m3h) THEN
    rVoted_StockFlow_m3h := FT_STOCK_FEED_PUMP_102A;
    tTMR_StockFlow_DiscrepTimer := 0.0;
    bTMR_StockFlow_Degraded := FALSE;
ELSIF ABS(FT_STOCK_FEED_PUMP_102A - FT_STOCK_FEED_PUMP_102B) <= c_rTol_StockFlow_m3h THEN
    rVoted_StockFlow_m3h := (FT_STOCK_FEED_PUMP_102A + FT_STOCK_FEED_PUMP_102B) * 0.50;
    tTMR_StockFlow_DiscrepTimer := tTMR_StockFlow_DiscrepTimer + c_rCycleTime_s;
    IF tTMR_StockFlow_DiscrepTimer >= c_rDebounceDelay_s THEN
        bTMR_StockFlow_Degraded := TRUE;
    END_IF;
ELSIF ABS(FT_STOCK_FEED_PUMP_102B - FT_STOCK_FEED_PUMP_102C) <= c_rTol_StockFlow_m3h THEN
    rVoted_StockFlow_m3h := (FT_STOCK_FEED_PUMP_102B + FT_STOCK_FEED_PUMP_102C) * 0.50;
    tTMR_StockFlow_DiscrepTimer := tTMR_StockFlow_DiscrepTimer + c_rCycleTime_s;
    IF tTMR_StockFlow_DiscrepTimer >= c_rDebounceDelay_s THEN
        bTMR_StockFlow_Degraded := TRUE;
    END_IF;
ELSIF ABS(FT_STOCK_FEED_PUMP_102C - FT_STOCK_FEED_PUMP_102A) <= c_rTol_StockFlow_m3h THEN
    rVoted_StockFlow_m3h := (FT_STOCK_FEED_PUMP_102C + FT_STOCK_FEED_PUMP_102A) * 0.50;
    tTMR_StockFlow_DiscrepTimer := tTMR_StockFlow_DiscrepTimer + c_rCycleTime_s;
    IF tTMR_StockFlow_DiscrepTimer >= c_rDebounceDelay_s THEN
        bTMR_StockFlow_Degraded := TRUE;
    END_IF;
ELSE
    tTMR_StockFlow_DiscrepTimer := tTMR_StockFlow_DiscrepTimer + c_rCycleTime_s;
    bTMR_StockFlow_Degraded := TRUE;
END_IF;

(* --- 1.3: Thin Stock Consistency Voting [AIT_THIN_STOCK_CONSISTENCY_103A/B/C] --- *)
IF (ABS(AIT_THIN_STOCK_CONSISTENCY_103A - AIT_THIN_STOCK_CONSISTENCY_103B) <= c_rTol_Consistency_pct) AND
   (ABS(AIT_THIN_STOCK_CONSISTENCY_103A - AIT_THIN_STOCK_CONSISTENCY_103C) <= c_rTol_Consistency_pct) THEN
    rVoted_ThinStockConsistency_pct := AIT_THIN_STOCK_CONSISTENCY_103A;
    tTMR_Consistency_DiscrepTimer := 0.0;
    bTMR_Consistency_Degraded := FALSE;
ELSIF ABS(AIT_THIN_STOCK_CONSISTENCY_103A - AIT_THIN_STOCK_CONSISTENCY_103B) <= c_rTol_Consistency_pct THEN
    rVoted_ThinStockConsistency_pct := (AIT_THIN_STOCK_CONSISTENCY_103A + AIT_THIN_STOCK_CONSISTENCY_103B) * 0.50;
    tTMR_Consistency_DiscrepTimer := tTMR_Consistency_DiscrepTimer + c_rCycleTime_s;
    IF tTMR_Consistency_DiscrepTimer >= c_rDebounceDelay_s THEN
        bTMR_Consistency_Degraded := TRUE;
    END_IF;
ELSIF ABS(AIT_THIN_STOCK_CONSISTENCY_103B - AIT_THIN_STOCK_CONSISTENCY_103C) <= c_rTol_Consistency_pct THEN
    rVoted_ThinStockConsistency_pct := (AIT_THIN_STOCK_CONSISTENCY_103B + AIT_THIN_STOCK_CONSISTENCY_103C) * 0.50;
    tTMR_Consistency_DiscrepTimer := tTMR_Consistency_DiscrepTimer + c_rCycleTime_s;
    IF tTMR_Consistency_DiscrepTimer >= c_rDebounceDelay_s THEN
        bTMR_Consistency_Degraded := TRUE;
    END_IF;
ELSIF ABS(AIT_THIN_STOCK_CONSISTENCY_103C - AIT_THIN_STOCK_CONSISTENCY_103A) <= c_rTol_Consistency_pct THEN
    rVoted_ThinStockConsistency_pct := (AIT_THIN_STOCK_CONSISTENCY_103C + AIT_THIN_STOCK_CONSISTENCY_103A) * 0.50;
    tTMR_Consistency_DiscrepTimer := tTMR_Consistency_DiscrepTimer + c_rCycleTime_s;
    IF tTMR_Consistency_DiscrepTimer >= c_rDebounceDelay_s THEN
        bTMR_Consistency_Degraded := TRUE;
    END_IF;
ELSE
    tTMR_Consistency_DiscrepTimer := tTMR_Consistency_DiscrepTimer + c_rCycleTime_s;
    bTMR_Consistency_Degraded := TRUE;
END_IF;

(* --- 1.4: Forming Wire Section Speed Voting [ST_FORMING_WIRE_SPEED_104A/B/C] --- *)
IF (ABS(ST_FORMING_WIRE_SPEED_104A - ST_FORMING_WIRE_SPEED_104B) <= c_rTol_WireSpeed_mpm) AND
   (ABS(ST_FORMING_WIRE_SPEED_104A - ST_FORMING_WIRE_SPEED_104C) <= c_rTol_WireSpeed_mpm) THEN
    rVoted_FormingWireSpeed_mpm := ST_FORMING_WIRE_SPEED_104A;
    tTMR_WireSpeed_DiscrepTimer := 0.0;
    bTMR_WireSpeed_Degraded := FALSE;
ELSIF ABS(ST_FORMING_WIRE_SPEED_104A - ST_FORMING_WIRE_SPEED_104B) <= c_rTol_WireSpeed_mpm THEN
    rVoted_FormingWireSpeed_mpm := (ST_FORMING_WIRE_SPEED_104A + ST_FORMING_WIRE_SPEED_104B) * 0.50;
    tTMR_WireSpeed_DiscrepTimer := tTMR_WireSpeed_DiscrepTimer + c_rCycleTime_s;
    IF tTMR_WireSpeed_DiscrepTimer >= c_rDebounceDelay_s THEN
        bTMR_WireSpeed_Degraded := TRUE;
    END_IF;
ELSIF ABS(ST_FORMING_WIRE_SPEED_104B - ST_FORMING_WIRE_SPEED_104C) <= c_rTol_WireSpeed_mpm THEN
    rVoted_FormingWireSpeed_mpm := (ST_FORMING_WIRE_SPEED_104B + ST_FORMING_WIRE_SPEED_104C) * 0.50;
    tTMR_WireSpeed_DiscrepTimer := tTMR_WireSpeed_DiscrepTimer + c_rCycleTime_s;
    IF tTMR_WireSpeed_DiscrepTimer >= c_rDebounceDelay_s THEN
        bTMR_WireSpeed_Degraded := TRUE;
    END_IF;
ELSIF ABS(ST_FORMING_WIRE_SPEED_104C - ST_FORMING_WIRE_SPEED_104A) <= c_rTol_WireSpeed_mpm THEN
    rVoted_FormingWireSpeed_mpm := (ST_FORMING_WIRE_SPEED_104C + ST_FORMING_WIRE_SPEED_104A) * 0.50;
    tTMR_WireSpeed_DiscrepTimer := tTMR_WireSpeed_DiscrepTimer + c_rCycleTime_s;
    IF tTMR_WireSpeed_DiscrepTimer >= c_rDebounceDelay_s THEN
        bTMR_WireSpeed_Degraded := TRUE;
    END_IF;
ELSE
    tTMR_WireSpeed_DiscrepTimer := tTMR_WireSpeed_DiscrepTimer + c_rCycleTime_s;
    bTMR_WireSpeed_Degraded := TRUE;
END_IF;

(* --- 1.5: Wire Flat Box High-Vacuum Voting [DPS_WIRE_SUCTION_BOX_201A/B/C] --- *)
IF (ABS(DPS_WIRE_SUCTION_BOX_201A - DPS_WIRE_SUCTION_BOX_201B) <= c_rTol_SuctionBox_kPa) AND
   (ABS(DPS_WIRE_SUCTION_BOX_201A - DPS_WIRE_SUCTION_BOX_201C) <= c_rTol_SuctionBox_kPa) THEN
    rVoted_WireSuctionBox_kPa := DPS_WIRE_SUCTION_BOX_201A;
    tTMR_SuctionBox_DiscrepTimer := 0.0;
    bTMR_SuctionBox_Degraded := FALSE;
ELSIF ABS(DPS_WIRE_SUCTION_BOX_201A - DPS_WIRE_SUCTION_BOX_201B) <= c_rTol_SuctionBox_kPa THEN
    rVoted_WireSuctionBox_kPa := (DPS_WIRE_SUCTION_BOX_201A + DPS_WIRE_SUCTION_BOX_201B) * 0.50;
    tTMR_SuctionBox_DiscrepTimer := tTMR_SuctionBox_DiscrepTimer + c_rCycleTime_s;
    IF tTMR_SuctionBox_DiscrepTimer >= c_rDebounceDelay_s THEN
        bTMR_SuctionBox_Degraded := TRUE;
    END_IF;
ELSIF ABS(DPS_WIRE_SUCTION_BOX_201B - DPS_WIRE_SUCTION_BOX_201C) <= c_rTol_SuctionBox_kPa THEN
    rVoted_WireSuctionBox_kPa := (DPS_WIRE_SUCTION_BOX_201B + DPS_WIRE_SUCTION_BOX_201C) * 0.50;
    tTMR_SuctionBox_DiscrepTimer := tTMR_SuctionBox_DiscrepTimer + c_rCycleTime_s;
    IF tTMR_SuctionBox_DiscrepTimer >= c_rDebounceDelay_s THEN
        bTMR_SuctionBox_Degraded := TRUE;
    END_IF;
ELSIF ABS(DPS_WIRE_SUCTION_BOX_201C - DPS_WIRE_SUCTION_BOX_201A) <= c_rTol_SuctionBox_kPa THEN
    rVoted_WireSuctionBox_kPa := (DPS_WIRE_SUCTION_BOX_201C + DPS_WIRE_SUCTION_BOX_201A) * 0.50;
    tTMR_SuctionBox_DiscrepTimer := tTMR_SuctionBox_DiscrepTimer + c_rCycleTime_s;
    IF tTMR_SuctionBox_DiscrepTimer >= c_rDebounceDelay_s THEN
        bTMR_SuctionBox_Degraded := TRUE;
    END_IF;
ELSE
    tTMR_SuctionBox_DiscrepTimer := tTMR_SuctionBox_DiscrepTimer + c_rCycleTime_s;
    bTMR_SuctionBox_Degraded := TRUE;
END_IF;

(* --- 1.6: Extended Nip Shoe Press Hydraulic Pressure Voting [PT_SHOE_PRESS_HYD_PRESSURE_301A/B/C] --- *)
IF (ABS(PT_SHOE_PRESS_HYD_PRESSURE_301A - PT_SHOE_PRESS_HYD_PRESSURE_301B) <= c_rTol_ShoeHydPress_bar) AND
   (ABS(PT_SHOE_PRESS_HYD_PRESSURE_301A - PT_SHOE_PRESS_HYD_PRESSURE_301C) <= c_rTol_ShoeHydPress_bar) THEN
    rVoted_ShoePressHydPressure_bar := PT_SHOE_PRESS_HYD_PRESSURE_301A;
    tTMR_ShoeHydPress_DiscrepTimer := 0.0;
    bTMR_ShoeHydPress_Degraded := FALSE;
ELSIF ABS(PT_SHOE_PRESS_HYD_PRESSURE_301A - PT_SHOE_PRESS_HYD_PRESSURE_301B) <= c_rTol_ShoeHydPress_bar THEN
    rVoted_ShoePressHydPressure_bar := (PT_SHOE_PRESS_HYD_PRESSURE_301A + PT_SHOE_PRESS_HYD_PRESSURE_301B) * 0.50;
    tTMR_ShoeHydPress_DiscrepTimer := tTMR_ShoeHydPress_DiscrepTimer + c_rCycleTime_s;
    IF tTMR_ShoeHydPress_DiscrepTimer >= c_rDebounceDelay_s THEN
        bTMR_ShoeHydPress_Degraded := TRUE;
    END_IF;
ELSIF ABS(PT_SHOE_PRESS_HYD_PRESSURE_301B - PT_SHOE_PRESS_HYD_PRESSURE_301C) <= c_rTol_ShoeHydPress_bar THEN
    rVoted_ShoePressHydPressure_bar := (PT_SHOE_PRESS_HYD_PRESSURE_301B + PT_SHOE_PRESS_HYD_PRESSURE_301C) * 0.50;
    tTMR_ShoeHydPress_DiscrepTimer := tTMR_ShoeHydPress_DiscrepTimer + c_rCycleTime_s;
    IF tTMR_ShoeHydPress_DiscrepTimer >= c_rDebounceDelay_s THEN
        bTMR_ShoeHydPress_Degraded := TRUE;
    END_IF;
ELSIF ABS(PT_SHOE_PRESS_HYD_PRESSURE_301C - PT_SHOE_PRESS_HYD_PRESSURE_301A) <= c_rTol_ShoeHydPress_bar THEN
    rVoted_ShoePressHydPressure_bar := (PT_SHOE_PRESS_HYD_PRESSURE_301C + PT_SHOE_PRESS_HYD_PRESSURE_301A) * 0.50;
    tTMR_ShoeHydPress_DiscrepTimer := tTMR_ShoeHydPress_DiscrepTimer + c_rCycleTime_s;
    IF tTMR_ShoeHydPress_DiscrepTimer >= c_rDebounceDelay_s THEN
        bTMR_ShoeHydPress_Degraded := TRUE;
    END_IF;
ELSE
    tTMR_ShoeHydPress_DiscrepTimer := tTMR_ShoeHydPress_DiscrepTimer + c_rCycleTime_s;
    bTMR_ShoeHydPress_Degraded := TRUE;
END_IF;

(* --- 1.7: Extended Nip Shoe Press Linear Load Voting [WT_SHOE_PRESS_NIP_LOAD_302A/B/C] --- *)
IF (ABS(WT_SHOE_PRESS_NIP_LOAD_302A - WT_SHOE_PRESS_NIP_LOAD_302B) <= c_rTol_ShoeNipLoad_kNm) AND
   (ABS(WT_SHOE_PRESS_NIP_LOAD_302A - WT_SHOE_PRESS_NIP_LOAD_302C) <= c_rTol_ShoeNipLoad_kNm) THEN
    rVoted_ShoePressNipLoad_kNm := WT_SHOE_PRESS_NIP_LOAD_302A;
    tTMR_ShoeNipLoad_DiscrepTimer := 0.0;
    bTMR_ShoeNipLoad_Degraded := FALSE;
ELSIF ABS(WT_SHOE_PRESS_NIP_LOAD_302A - WT_SHOE_PRESS_NIP_LOAD_302B) <= c_rTol_ShoeNipLoad_kNm THEN
    rVoted_ShoePressNipLoad_kNm := (WT_SHOE_PRESS_NIP_LOAD_302A + WT_SHOE_PRESS_NIP_LOAD_302B) * 0.50;
    tTMR_ShoeNipLoad_DiscrepTimer := tTMR_ShoeNipLoad_DiscrepTimer + c_rCycleTime_s;
    IF tTMR_ShoeNipLoad_DiscrepTimer >= c_rDebounceDelay_s THEN
        bTMR_ShoeNipLoad_Degraded := TRUE;
    END_IF;
ELSIF ABS(WT_SHOE_PRESS_NIP_LOAD_302B - WT_SHOE_PRESS_NIP_LOAD_302C) <= c_rTol_ShoeNipLoad_kNm THEN
    rVoted_ShoePressNipLoad_kNm := (WT_SHOE_PRESS_NIP_LOAD_302B + WT_SHOE_PRESS_NIP_LOAD_302C) * 0.50;
    tTMR_ShoeNipLoad_DiscrepTimer := tTMR_ShoeNipLoad_DiscrepTimer + c_rCycleTime_s;
    IF tTMR_ShoeNipLoad_DiscrepTimer >= c_rDebounceDelay_s THEN
        bTMR_ShoeNipLoad_Degraded := TRUE;
    END_IF;
ELSIF ABS(WT_SHOE_PRESS_NIP_LOAD_302C - WT_SHOE_PRESS_NIP_LOAD_302A) <= c_rTol_ShoeNipLoad_kNm THEN
    rVoted_ShoePressNipLoad_kNm := (WT_SHOE_PRESS_NIP_LOAD_302C + WT_SHOE_PRESS_NIP_LOAD_302A) * 0.50;
    tTMR_ShoeNipLoad_DiscrepTimer := tTMR_ShoeNipLoad_DiscrepTimer + c_rCycleTime_s;
    IF tTMR_ShoeNipLoad_DiscrepTimer >= c_rDebounceDelay_s THEN
        bTMR_ShoeNipLoad_Degraded := TRUE;
    END_IF;
ELSE
    tTMR_ShoeNipLoad_DiscrepTimer := tTMR_ShoeNipLoad_DiscrepTimer + c_rCycleTime_s;
    bTMR_ShoeNipLoad_Degraded := TRUE;
END_IF;

(* --- 1.8: Dryer Section 1 Saturated Steam Pressure Voting [PT_DRYER_SEC1_STEAM_PRESS_401A/B/C] --- *)
IF (ABS(PT_DRYER_SEC1_STEAM_PRESS_401A - PT_DRYER_SEC1_STEAM_PRESS_401B) <= c_rTol_DryerSec1_bar) AND
   (ABS(PT_DRYER_SEC1_STEAM_PRESS_401A - PT_DRYER_SEC1_STEAM_PRESS_401C) <= c_rTol_DryerSec1_bar) THEN
    rVoted_DryerSec1Steam_bar := PT_DRYER_SEC1_STEAM_PRESS_401A;
    tTMR_DryerSec1_DiscrepTimer := 0.0;
    bTMR_DryerSec1_Degraded := FALSE;
ELSIF ABS(PT_DRYER_SEC1_STEAM_PRESS_401A - PT_DRYER_SEC1_STEAM_PRESS_401B) <= c_rTol_DryerSec1_bar THEN
    rVoted_DryerSec1Steam_bar := (PT_DRYER_SEC1_STEAM_PRESS_401A + PT_DRYER_SEC1_STEAM_PRESS_401B) * 0.50;
    tTMR_DryerSec1_DiscrepTimer := tTMR_DryerSec1_DiscrepTimer + c_rCycleTime_s;
    IF tTMR_DryerSec1_DiscrepTimer >= c_rDebounceDelay_s THEN
        bTMR_DryerSec1_Degraded := TRUE;
    END_IF;
ELSIF ABS(PT_DRYER_SEC1_STEAM_PRESS_401B - PT_DRYER_SEC1_STEAM_PRESS_401C) <= c_rTol_DryerSec1_bar THEN
    rVoted_DryerSec1Steam_bar := (PT_DRYER_SEC1_STEAM_PRESS_401B + PT_DRYER_SEC1_STEAM_PRESS_401C) * 0.50;
    tTMR_DryerSec1_DiscrepTimer := tTMR_DryerSec1_DiscrepTimer + c_rCycleTime_s;
    IF tTMR_DryerSec1_DiscrepTimer >= c_rDebounceDelay_s THEN
        bTMR_DryerSec1_Degraded := TRUE;
    END_IF;
ELSIF ABS(PT_DRYER_SEC1_STEAM_PRESS_401C - PT_DRYER_SEC1_STEAM_PRESS_401A) <= c_rTol_DryerSec1_bar THEN
    rVoted_DryerSec1Steam_bar := (PT_DRYER_SEC1_STEAM_PRESS_401C + PT_DRYER_SEC1_STEAM_PRESS_401A) * 0.50;
    tTMR_DryerSec1_DiscrepTimer := tTMR_DryerSec1_DiscrepTimer + c_rCycleTime_s;
    IF tTMR_DryerSec1_DiscrepTimer >= c_rDebounceDelay_s THEN
        bTMR_DryerSec1_Degraded := TRUE;
    END_IF;
ELSE
    tTMR_DryerSec1_DiscrepTimer := tTMR_DryerSec1_DiscrepTimer + c_rCycleTime_s;
    bTMR_DryerSec1_Degraded := TRUE;
END_IF;

(* --- 1.9: Dryer Section 4 Main Steam Pressure Voting [PT_DRYER_SEC4_STEAM_PRESS_404A/B/C] --- *)
IF (ABS(PT_DRYER_SEC4_STEAM_PRESS_404A - PT_DRYER_SEC4_STEAM_PRESS_404B) <= c_rTol_DryerSec4_bar) AND
   (ABS(PT_DRYER_SEC4_STEAM_PRESS_404A - PT_DRYER_SEC4_STEAM_PRESS_404C) <= c_rTol_DryerSec4_bar) THEN
    rVoted_DryerSec4Steam_bar := PT_DRYER_SEC4_STEAM_PRESS_404A;
    tTMR_DryerSec4_DiscrepTimer := 0.0;
    bTMR_DryerSec4_Degraded := FALSE;
ELSIF ABS(PT_DRYER_SEC4_STEAM_PRESS_404A - PT_DRYER_SEC4_STEAM_PRESS_404B) <= c_rTol_DryerSec4_bar THEN
    rVoted_DryerSec4Steam_bar := (PT_DRYER_SEC4_STEAM_PRESS_404A + PT_DRYER_SEC4_STEAM_PRESS_404B) * 0.50;
    tTMR_DryerSec4_DiscrepTimer := tTMR_DryerSec4_DiscrepTimer + c_rCycleTime_s;
    IF tTMR_DryerSec4_DiscrepTimer >= c_rDebounceDelay_s THEN
        bTMR_DryerSec4_Degraded := TRUE;
    END_IF;
ELSIF ABS(PT_DRYER_SEC4_STEAM_PRESS_404B - PT_DRYER_SEC4_STEAM_PRESS_404C) <= c_rTol_DryerSec4_bar THEN
    rVoted_DryerSec4Steam_bar := (PT_DRYER_SEC4_STEAM_PRESS_404B + PT_DRYER_SEC4_STEAM_PRESS_404C) * 0.50;
    tTMR_DryerSec4_DiscrepTimer := tTMR_DryerSec4_DiscrepTimer + c_rCycleTime_s;
    IF tTMR_DryerSec4_DiscrepTimer >= c_rDebounceDelay_s THEN
        bTMR_DryerSec4_Degraded := TRUE;
    END_IF;
ELSIF ABS(PT_DRYER_SEC4_STEAM_PRESS_404C - PT_DRYER_SEC4_STEAM_PRESS_404A) <= c_rTol_DryerSec4_bar THEN
    rVoted_DryerSec4Steam_bar := (PT_DRYER_SEC4_STEAM_PRESS_404C + PT_DRYER_SEC4_STEAM_PRESS_404A) * 0.50;
    tTMR_DryerSec4_DiscrepTimer := tTMR_DryerSec4_DiscrepTimer + c_rCycleTime_s;
    IF tTMR_DryerSec4_DiscrepTimer >= c_rDebounceDelay_s THEN
        bTMR_DryerSec4_Degraded := TRUE;
    END_IF;
ELSE
    tTMR_DryerSec4_DiscrepTimer := tTMR_DryerSec4_DiscrepTimer + c_rCycleTime_s;
    bTMR_DryerSec4_Degraded := TRUE;
END_IF;

(* --- 1.10: Dryer Stationary Siphon Diff Pressure Voting [DPS_DRYER_SIPHON_DIFF_PRESS_407A/B/C] --- *)
IF (ABS(DPS_DRYER_SIPHON_DIFF_PRESS_407A - DPS_DRYER_SIPHON_DIFF_PRESS_407B) <= c_rTol_SiphonDiff_kPa) AND
   (ABS(DPS_DRYER_SIPHON_DIFF_PRESS_407A - DPS_DRYER_SIPHON_DIFF_PRESS_407C) <= c_rTol_SiphonDiff_kPa) THEN
    rVoted_DryerSiphonDiff_kPa := DPS_DRYER_SIPHON_DIFF_PRESS_407A;
    tTMR_SiphonDiff_DiscrepTimer := 0.0;
    bTMR_SiphonDiff_Degraded := FALSE;
ELSIF ABS(DPS_DRYER_SIPHON_DIFF_PRESS_407A - DPS_DRYER_SIPHON_DIFF_PRESS_407B) <= c_rTol_SiphonDiff_kPa THEN
    rVoted_DryerSiphonDiff_kPa := (DPS_DRYER_SIPHON_DIFF_PRESS_407A + DPS_DRYER_SIPHON_DIFF_PRESS_407B) * 0.50;
    tTMR_SiphonDiff_DiscrepTimer := tTMR_SiphonDiff_DiscrepTimer + c_rCycleTime_s;
    IF tTMR_SiphonDiff_DiscrepTimer >= c_rDebounceDelay_s THEN
        bTMR_SiphonDiff_Degraded := TRUE;
    END_IF;
ELSIF ABS(DPS_DRYER_SIPHON_DIFF_PRESS_407B - DPS_DRYER_SIPHON_DIFF_PRESS_407C) <= c_rTol_SiphonDiff_kPa THEN
    rVoted_DryerSiphonDiff_kPa := (DPS_DRYER_SIPHON_DIFF_PRESS_407B + DPS_DRYER_SIPHON_DIFF_PRESS_407C) * 0.50;
    tTMR_SiphonDiff_DiscrepTimer := tTMR_SiphonDiff_DiscrepTimer + c_rCycleTime_s;
    IF tTMR_SiphonDiff_DiscrepTimer >= c_rDebounceDelay_s THEN
        bTMR_SiphonDiff_Degraded := TRUE;
    END_IF;
ELSIF ABS(DPS_DRYER_SIPHON_DIFF_PRESS_407C - DPS_DRYER_SIPHON_DIFF_PRESS_407A) <= c_rTol_SiphonDiff_kPa THEN
    rVoted_DryerSiphonDiff_kPa := (DPS_DRYER_SIPHON_DIFF_PRESS_407C + DPS_DRYER_SIPHON_DIFF_PRESS_407A) * 0.50;
    tTMR_SiphonDiff_DiscrepTimer := tTMR_SiphonDiff_DiscrepTimer + c_rCycleTime_s;
    IF tTMR_SiphonDiff_DiscrepTimer >= c_rDebounceDelay_s THEN
        bTMR_SiphonDiff_Degraded := TRUE;
    END_IF;
ELSE
    tTMR_SiphonDiff_DiscrepTimer := tTMR_SiphonDiff_DiscrepTimer + c_rCycleTime_s;
    bTMR_SiphonDiff_Degraded := TRUE;
END_IF;

(* --- 1.11: Radiometric Beta-Ray Basis Weight Voting [WT_SCANNER_BASIS_WEIGHT_501A/B/C] --- *)
IF (ABS(WT_SCANNER_BASIS_WEIGHT_501A - WT_SCANNER_BASIS_WEIGHT_501B) <= c_rTol_BasisWeight_gsm) AND
   (ABS(WT_SCANNER_BASIS_WEIGHT_501A - WT_SCANNER_BASIS_WEIGHT_501C) <= c_rTol_BasisWeight_gsm) THEN
    rVoted_BasisWeight_gsm := WT_SCANNER_BASIS_WEIGHT_501A;
    tTMR_BasisWeight_DiscrepTimer := 0.0;
    bTMR_BasisWeight_Degraded := FALSE;
ELSIF ABS(WT_SCANNER_BASIS_WEIGHT_501A - WT_SCANNER_BASIS_WEIGHT_501B) <= c_rTol_BasisWeight_gsm THEN
    rVoted_BasisWeight_gsm := (WT_SCANNER_BASIS_WEIGHT_501A + WT_SCANNER_BASIS_WEIGHT_501B) * 0.50;
    tTMR_BasisWeight_DiscrepTimer := tTMR_BasisWeight_DiscrepTimer + c_rCycleTime_s;
    IF tTMR_BasisWeight_DiscrepTimer >= c_rDebounceDelay_s THEN
        bTMR_BasisWeight_Degraded := TRUE;
    END_IF;
ELSIF ABS(WT_SCANNER_BASIS_WEIGHT_501B - WT_SCANNER_BASIS_WEIGHT_501C) <= c_rTol_BasisWeight_gsm THEN
    rVoted_BasisWeight_gsm := (WT_SCANNER_BASIS_WEIGHT_501B + WT_SCANNER_BASIS_WEIGHT_501C) * 0.50;
    tTMR_BasisWeight_DiscrepTimer := tTMR_BasisWeight_DiscrepTimer + c_rCycleTime_s;
    IF tTMR_BasisWeight_DiscrepTimer >= c_rDebounceDelay_s THEN
        bTMR_BasisWeight_Degraded := TRUE;
    END_IF;
ELSIF ABS(WT_SCANNER_BASIS_WEIGHT_501C - WT_SCANNER_BASIS_WEIGHT_501A) <= c_rTol_BasisWeight_gsm THEN
    rVoted_BasisWeight_gsm := (WT_SCANNER_BASIS_WEIGHT_501C + WT_SCANNER_BASIS_WEIGHT_501A) * 0.50;
    tTMR_BasisWeight_DiscrepTimer := tTMR_BasisWeight_DiscrepTimer + c_rCycleTime_s;
    IF tTMR_BasisWeight_DiscrepTimer >= c_rDebounceDelay_s THEN
        bTMR_BasisWeight_Degraded := TRUE;
    END_IF;
ELSE
    tTMR_BasisWeight_DiscrepTimer := tTMR_BasisWeight_DiscrepTimer + c_rCycleTime_s;
    bTMR_BasisWeight_Degraded := TRUE;
END_IF;

(* --- 1.12: Infrared Moisture Sensor Voting [AT_SCANNER_IR_MOISTURE_502A/B/C] --- *)
IF (ABS(AT_SCANNER_IR_MOISTURE_502A - AT_SCANNER_IR_MOISTURE_502B) <= c_rTol_Moisture_pct) AND
   (ABS(AT_SCANNER_IR_MOISTURE_502A - AT_SCANNER_IR_MOISTURE_502C) <= c_rTol_Moisture_pct) THEN
    rVoted_Moisture_pct := AT_SCANNER_IR_MOISTURE_502A;
    tTMR_Moisture_DiscrepTimer := 0.0;
    bTMR_Moisture_Degraded := FALSE;
ELSIF ABS(AT_SCANNER_IR_MOISTURE_502A - AT_SCANNER_IR_MOISTURE_502B) <= c_rTol_Moisture_pct THEN
    rVoted_Moisture_pct := (AT_SCANNER_IR_MOISTURE_502A + AT_SCANNER_IR_MOISTURE_502B) * 0.50;
    tTMR_Moisture_DiscrepTimer := tTMR_Moisture_DiscrepTimer + c_rCycleTime_s;
    IF tTMR_Moisture_DiscrepTimer >= c_rDebounceDelay_s THEN
        bTMR_Moisture_Degraded := TRUE;
    END_IF;
ELSIF ABS(AT_SCANNER_IR_MOISTURE_502B - AT_SCANNER_IR_MOISTURE_502C) <= c_rTol_Moisture_pct THEN
    rVoted_Moisture_pct := (AT_SCANNER_IR_MOISTURE_502B + AT_SCANNER_IR_MOISTURE_502C) * 0.50;
    tTMR_Moisture_DiscrepTimer := tTMR_Moisture_DiscrepTimer + c_rCycleTime_s;
    IF tTMR_Moisture_DiscrepTimer >= c_rDebounceDelay_s THEN
        bTMR_Moisture_Degraded := TRUE;
    END_IF;
ELSIF ABS(AT_SCANNER_IR_MOISTURE_502C - AT_SCANNER_IR_MOISTURE_502A) <= c_rTol_Moisture_pct THEN
    rVoted_Moisture_pct := (AT_SCANNER_IR_MOISTURE_502C + AT_SCANNER_IR_MOISTURE_502A) * 0.50;
    tTMR_Moisture_DiscrepTimer := tTMR_Moisture_DiscrepTimer + c_rCycleTime_s;
    IF tTMR_Moisture_DiscrepTimer >= c_rDebounceDelay_s THEN
        bTMR_Moisture_Degraded := TRUE;
    END_IF;
ELSE
    tTMR_Moisture_DiscrepTimer := tTMR_Moisture_DiscrepTimer + c_rCycleTime_s;
    bTMR_Moisture_Degraded := TRUE;
END_IF;

(* --- 1.13: Reel Web Tension Loadcell Voting [WT_REEL_WEB_TENSION_601A/B/C] --- *)
IF (ABS(WT_REEL_WEB_TENSION_601A - WT_REEL_WEB_TENSION_601B) <= c_rTol_ReelTension_Nm) AND
   (ABS(WT_REEL_WEB_TENSION_601A - WT_REEL_WEB_TENSION_601C) <= c_rTol_ReelTension_Nm) THEN
    rVoted_ReelTension_Nm := WT_REEL_WEB_TENSION_601A;
    tTMR_ReelTension_DiscrepTimer := 0.0;
    bTMR_ReelTension_Degraded := FALSE;
ELSIF ABS(WT_REEL_WEB_TENSION_601A - WT_REEL_WEB_TENSION_601B) <= c_rTol_ReelTension_Nm THEN
    rVoted_ReelTension_Nm := (WT_REEL_WEB_TENSION_601A + WT_REEL_WEB_TENSION_601B) * 0.50;
    tTMR_ReelTension_DiscrepTimer := tTMR_ReelTension_DiscrepTimer + c_rCycleTime_s;
    IF tTMR_ReelTension_DiscrepTimer >= c_rDebounceDelay_s THEN
        bTMR_ReelTension_Degraded := TRUE;
    END_IF;
ELSIF ABS(WT_REEL_WEB_TENSION_601B - WT_REEL_WEB_TENSION_601C) <= c_rTol_ReelTension_Nm THEN
    rVoted_ReelTension_Nm := (WT_REEL_WEB_TENSION_601B + WT_REEL_WEB_TENSION_601C) * 0.50;
    tTMR_ReelTension_DiscrepTimer := tTMR_ReelTension_DiscrepTimer + c_rCycleTime_s;
    IF tTMR_ReelTension_DiscrepTimer >= c_rDebounceDelay_s THEN
        bTMR_ReelTension_Degraded := TRUE;
    END_IF;
ELSIF ABS(WT_REEL_WEB_TENSION_601C - WT_REEL_WEB_TENSION_601A) <= c_rTol_ReelTension_Nm THEN
    rVoted_ReelTension_Nm := (WT_REEL_WEB_TENSION_601C + WT_REEL_WEB_TENSION_601A) * 0.50;
    tTMR_ReelTension_DiscrepTimer := tTMR_ReelTension_DiscrepTimer + c_rCycleTime_s;
    IF tTMR_ReelTension_DiscrepTimer >= c_rDebounceDelay_s THEN
        bTMR_ReelTension_Degraded := TRUE;
    END_IF;
ELSE
    tTMR_ReelTension_DiscrepTimer := tTMR_ReelTension_DiscrepTimer + c_rCycleTime_s;
    bTMR_ReelTension_Degraded := TRUE;
END_IF;

(* --- 1.14: 2oo3 Optical Web Break Detection Voting [OPT_WEB_BREAK_OPTICAL_701A/B/C] --- *)
IF (OPT_WEB_BREAK_OPTICAL_701A AND OPT_WEB_BREAK_OPTICAL_701B) OR
   (OPT_WEB_BREAK_OPTICAL_701B AND OPT_WEB_BREAK_OPTICAL_701C) OR
   (OPT_WEB_BREAK_OPTICAL_701C AND OPT_WEB_BREAK_OPTICAL_701A) THEN
    bVoted_WebBreak_Optical := TRUE;
ELSE
    bVoted_WebBreak_Optical := FALSE;
END_IF;

(* Bitmask Packing for TMR Channel Faults *)
wTMR_ChannelFaultMask := 16#00000000;
IF bTMR_HeadboxPress_Degraded    THEN wTMR_ChannelFaultMask := wTMR_ChannelFaultMask OR 16#00000001; END_IF;
IF bTMR_StockFlow_Degraded       THEN wTMR_ChannelFaultMask := wTMR_ChannelFaultMask OR 16#00000002; END_IF;
IF bTMR_Consistency_Degraded     THEN wTMR_ChannelFaultMask := wTMR_ChannelFaultMask OR 16#00000004; END_IF;
IF bTMR_WireSpeed_Degraded       THEN wTMR_ChannelFaultMask := wTMR_ChannelFaultMask OR 16#00000008; END_IF;
IF bTMR_SuctionBox_Degraded      THEN wTMR_ChannelFaultMask := wTMR_ChannelFaultMask OR 16#00000010; END_IF;
IF bTMR_ShoeHydPress_Degraded    THEN wTMR_ChannelFaultMask := wTMR_ChannelFaultMask OR 16#00000020; END_IF;
IF bTMR_ShoeNipLoad_Degraded     THEN wTMR_ChannelFaultMask := wTMR_ChannelFaultMask OR 16#00000040; END_IF;
IF bTMR_DryerSec1_Degraded       THEN wTMR_ChannelFaultMask := wTMR_ChannelFaultMask OR 16#00000080; END_IF;
IF bTMR_DryerSec4_Degraded       THEN wTMR_ChannelFaultMask := wTMR_ChannelFaultMask OR 16#00000100; END_IF;
IF bTMR_SiphonDiff_Degraded      THEN wTMR_ChannelFaultMask := wTMR_ChannelFaultMask OR 16#00000200; END_IF;
IF bTMR_BasisWeight_Degraded     THEN wTMR_ChannelFaultMask := wTMR_ChannelFaultMask OR 16#00000400; END_IF;
IF bTMR_Moisture_Degraded        THEN wTMR_ChannelFaultMask := wTMR_ChannelFaultMask OR 16#00000800; END_IF;
IF bTMR_ReelTension_Degraded     THEN wTMR_ChannelFaultMask := wTMR_ChannelFaultMask OR 16#00001000; END_IF;
""")

    # -------------------------------------------------------------------------
    # PART 6: Code Body - Phase 2: Observers & Cyber-Physical Algorithms
    # -------------------------------------------------------------------------
    parts.append("""(* =====================================================================================================
 * PHASE 2: CYBER-PHYSICAL STATE ESTIMATORS, HYDRODYNAMICS & ENTHALPY OBSERVERS
 * Bernoulli free-surface spouting velocity, Shoe Press Vogel oil lubrication film thickness,
 * multi-cylinder drying enthalpy rate, and Campbell filtration dewatering mass balance.
 * ===================================================================================================== *)

(* --- 2.1: Headbox Hydrodynamics & Bernoulli Spouting Jet Velocity --- *)
(* P_total = P_airpad + rho * g * h_pond. Effective Head H = P_total / (rho * g) *)
rHeadboxPondStockHead_m := LT_HEADBOX_LIQUID_LEVEL_106 * 0.0010; (* mm to meters *)
rHeadboxTotalEffectiveHead_m := (rVoted_HeadboxTotalHead_kPa * 1000.0) / (c_rWaterDensity_kgm3 * c_rGravity_mps2);

IF rHeadboxTotalEffectiveHead_m > 0.10 THEN
    (* v_theoretical = sqrt(2 * g * H_total) *)
    rTheoreticalSpoutingJetVelocity := SQRT(2.0 * c_rGravity_mps2 * rHeadboxTotalEffectiveHead_m);
ELSE
    rTheoreticalSpoutingJetVelocity := 0.0;
END_IF;

(* v_actual = Cd * v_theoretical *)
rActualJetVelocity_mps := rDischargeCoefficient_Cd * rTheoreticalSpoutingJetVelocity;
rObserved_JetSpeed_mps := rActualJetVelocity_mps;

(* Forming Wire Surface Linear Velocity [m/s] *)
rWireVelocity_mps := rVoted_FormingWireSpeed_mpm / 60.0;
rObserved_WireSpeed_mps := rWireVelocity_mps;

(* Jet-to-Wire Speed Ratio v_jet / v_wire *)
IF rWireVelocity_mps > 0.50 THEN
    rObserved_JetToWireRatio := rActualJetVelocity_mps / rWireVelocity_mps;
ELSE
    rObserved_JetToWireRatio := 1.000;
END_IF;

(* --- 2.2: Extended Nip Shoe Press Hydrodynamic Oil Film Observer --- *)
(* Vogel Temperature Viscosity Model: mu(T) = mu_0 * EXP(Beta / (T + T_0)) [Pa*s] *)
IF TT_SHOE_PRESS_OIL_TEMP_303 > 10.0 THEN
    rCalculated_OilViscosity_Pas := c_rOilViscosity_Zero_Pa_s *
        EXP(c_rOilViscosity_Beta / (TT_SHOE_PRESS_OIL_TEMP_303 + c_rOilViscosity_T0));
ELSE
    rCalculated_OilViscosity_Pas := 0.085;
END_IF;

(* Shoe Press Specific Hydrostatic Area Pressure [MPa] from Linear Nip Load (kN/m) over 250 mm Shoe Length *)
rShoePress_SpecificPressure_MPa := (rVoted_ShoePressNipLoad_kNm / 0.250) * 0.0010;

(* Hydrodynamic Film Thickness h_film = K_hydro * (mu * v / P_spec)^0.5 [um] *)
IF (rShoePress_SpecificPressure_MPa > 0.50) AND (rWireVelocity_mps > 1.0) THEN
    rShoePress_HydrodynamicFilm_um := 185.0 * SQRT((rCalculated_OilViscosity_Pas * rWireVelocity_mps) /
                                                   rShoePress_SpecificPressure_MPa);
ELSE
    rShoePress_HydrodynamicFilm_um := 15.0;
END_IF;
rObserved_ShoeOilFilm_um := rShoePress_HydrodynamicFilm_um;

(* --- 2.3: Sheet Dewatering & Dry Solids Gradient Across the Machine --- *)
(* Forming Section Drainage solids from Suction Box Vacuum *)
rWireDrySolids_pct := 16.5 + (ABS(rVoted_WireSuctionBox_kPa) * 0.085) + (ABS(DPS_COUCH_VACUUM_202) * 0.045);
IF rWireDrySolids_pct > 23.5 THEN rWireDrySolids_pct := 23.5; END_IF;

(* Shoe Press Compressive Dewatering Solids [%] *)
rShoePressExitSolids_pct := rWireDrySolids_pct + (rVoted_ShoePressNipLoad_kNm * 0.0195);
IF rShoePressExitSolids_pct > 53.5 THEN rShoePressExitSolids_pct := 53.5; END_IF;
rObserved_PressDrySolids_pct := rShoePressExitSolids_pct;

(* Dryer Section Progressive Evaporation Mass Transfer Observer *)
(* Delta H_vap(P) = 2257.0 - 2.45 * (T_sat - 100.0) [kJ/kg] *)
(* Evaporation: m_dot_evap = U * A * (T_steam - T_sheet) / Delta H_vap *)
rLatentHeat_Sec1_kJkg := 2257.0 - (2.45 * (121.0 - 100.0));
rEvaporationRate_Sec1_kgh := (185.0 * 240.0 * (121.0 - TT_SHEET_TEMP_SEC1_408)) / rLatentHeat_Sec1_kJkg;
IF rEvaporationRate_Sec1_kgh < 100.0 THEN rEvaporationRate_Sec1_kgh := 100.0; END_IF;

rLatentHeat_Sec4_kJkg := 2257.0 - (2.45 * (151.0 - 100.0));
rEvaporationRate_Sec4_kgh := (260.0 * 240.0 * (151.0 - TT_SHEET_TEMP_SEC4_411)) / rLatentHeat_Sec4_kJkg;
IF rEvaporationRate_Sec4_kgh < 100.0 THEN rEvaporationRate_Sec4_kgh := 100.0; END_IF;

rTotalEvaporation_kgh := (rEvaporationRate_Sec1_kgh * 1.8) + (rEvaporationRate_Sec4_kgh * 2.6);
rObserved_DryerEvapRate_Total_kgh := rTotalEvaporation_kgh;

(* Finished Sheet Dry Solids at Reel *)
rObserved_ReelDrySolids_pct := 100.0 - rVoted_Moisture_pct;
rObserved_BasisWeightAvg_gsm := rVoted_BasisWeight_gsm;
rObserved_MoistureAvg_pct := rVoted_Moisture_pct;

(* --- 2.4: Cross-Direction (CD) Profile Statistical Observer (2-Sigma Calculation) --- *)
rCD_SumBW := 0.0;
rCD_SumMoist := 0.0;
FOR iCD_ZoneIdx := 1 TO 32 DO
    aCD_BasisWeight_Filtered_gsm[iCD_ZoneIdx] := aScanner_CD_BasisWeight_Raw_gsm[iCD_ZoneIdx];
    aCD_Moisture_Filtered_pct[iCD_ZoneIdx] := aScanner_CD_Moisture_Raw_pct[iCD_ZoneIdx];
    rCD_SumBW := rCD_SumBW + aCD_BasisWeight_Filtered_gsm[iCD_ZoneIdx];
    rCD_SumMoist := rCD_SumMoist + aCD_Moisture_Filtered_pct[iCD_ZoneIdx];
END_FOR;

rCD_VarBW := 0.0;
rCD_VarMoist := 0.0;
FOR iCD_ZoneIdx := 1 TO 32 DO
    rCD_VarBW := rCD_VarBW + ((aCD_BasisWeight_Filtered_gsm[iCD_ZoneIdx] - (rCD_SumBW / 32.0)) *
                              (aCD_BasisWeight_Filtered_gsm[iCD_ZoneIdx] - (rCD_SumBW / 32.0)));
    rCD_VarMoist := rCD_VarMoist + ((aCD_Moisture_Filtered_pct[iCD_ZoneIdx] - (rCD_SumMoist / 32.0)) *
                                    (aCD_Moisture_Filtered_pct[iCD_ZoneIdx] - (rCD_SumMoist / 32.0)));
END_FOR;

rObserved_CD_2Sigma_BW := 2.0 * SQRT(rCD_VarBW / 32.0);
rObserved_CD_2Sigma_Moist := 2.0 * SQRT(rCD_VarMoist / 32.0);
""")

    # -------------------------------------------------------------------------
    # PART 7: Code Body - Phase 3: Receding-Horizon Model Predictive Control
    # -------------------------------------------------------------------------
    parts.append("""(* =====================================================================================================
 * PHASE 3: RECEDING-HORIZON 8x8 MODEL PREDICTIVE CONTROL (MPC) ENGINE
 * Solves discrete state prediction (x[k+1] = A*x[k] + B*u[k]), quadratic tracking cost gradient descent,
 * and actuator constraint saturation bounds at 10 ms cycle time.
 * ===================================================================================================== *)

(* 3.1: Compute State Deviations (x[k] = Actual - Setpoint) *)
x_k1 := rVoted_HeadboxTotalHead_kPa - ( (rJetToWire_Ratio_SP * (rVoted_FormingWireSpeed_mpm / 60.0) /
                                         rDischargeCoefficient_Cd) *
                                        (rJetToWire_Ratio_SP * (rVoted_FormingWireSpeed_mpm / 60.0) /
                                         rDischargeCoefficient_Cd) *
                                        (c_rWaterDensity_kgm3 * c_rGravity_mps2 / (2.0 * c_rGravity_mps2 * 1000.0)) );
x_k2 := LT_HEADBOX_LIQUID_LEVEL_106 - rHeadboxPondLevel_SP_mm;
x_k3 := (rVoted_ThinStockConsistency_pct - 0.750) * 100.0;
x_k4 := (rObserved_JetToWireRatio - rJetToWire_Ratio_SP) * 1000.0;
x_k5 := rVoted_ShoePressNipLoad_kNm - rShoePress_LinearLoad_SP_kNm;
x_k6 := (rVoted_DryerSec1Steam_bar - rDryerSec1_SteamPress_SP_bar) * 10.0;
x_k7 := (rVoted_DryerSec4Steam_bar - rDryerSec4_SteamPress_SP_bar) * 10.0;
x_k8 := rVoted_BasisWeight_gsm - rBasisWeight_SP_gsm;

(* 3.2: State-Space Prediction Propagation: x_pred[k+1] = A * x[k] + B * u[k] *)
x_pred1 := (A_mat_11 * x_k1) + (A_mat_12 * x_k2) + (A_mat_13 * x_k3) + (A_mat_14 * x_k4) +
           (A_mat_15 * x_k5) + (A_mat_16 * x_k6) + (A_mat_17 * x_k7) + (A_mat_18 * x_k8) +
           (B_mat_11 * (u_cmd1 - 65.0)) + (B_mat_12 * (u_cmd2 - 45.0));

x_pred2 := (A_mat_21 * x_k1) + (A_mat_22 * x_k2) + (A_mat_23 * x_k3) + (A_mat_24 * x_k4) +
           (A_mat_25 * x_k5) + (A_mat_26 * x_k6) + (A_mat_27 * x_k7) + (A_mat_28 * x_k8) +
           (B_mat_21 * (u_cmd1 - 65.0)) + (B_mat_22 * (u_cmd2 - 45.0));

x_pred3 := (A_mat_31 * x_k1) + (A_mat_32 * x_k2) + (A_mat_33 * x_k3) + (A_mat_34 * x_k4) +
           (A_mat_35 * x_k5) + (A_mat_36 * x_k6) + (A_mat_37 * x_k7) + (A_mat_38 * x_k8) +
           (B_mat_33 * (u_cmd3 - 50.0));

x_pred4 := (A_mat_41 * x_k1) + (A_mat_42 * x_k2) + (A_mat_43 * x_k3) + (A_mat_44 * x_k4) +
           (A_mat_45 * x_k5) + (A_mat_46 * x_k6) + (A_mat_47 * x_k7) + (A_mat_48 * x_k8) +
           (B_mat_41 * (u_cmd1 - 65.0)) + (B_mat_44 * ((u_cmd4 - 1800.0) * 0.05));

x_pred5 := (A_mat_51 * x_k1) + (A_mat_52 * x_k2) + (A_mat_53 * x_k3) + (A_mat_54 * x_k4) +
           (A_mat_55 * x_k5) + (A_mat_56 * x_k6) + (A_mat_57 * x_k7) + (A_mat_58 * x_k8) +
           (B_mat_55 * (u_cmd5 - 72.0));

x_pred6 := (A_mat_61 * x_k1) + (A_mat_62 * x_k2) + (A_mat_63 * x_k3) + (A_mat_64 * x_k4) +
           (A_mat_65 * x_k5) + (A_mat_66 * x_k6) + (A_mat_67 * x_k7) + (A_mat_68 * x_k8) +
           (B_mat_66 * (u_cmd6 - 38.0));

x_pred7 := (A_mat_71 * x_k1) + (A_mat_72 * x_k2) + (A_mat_73 * x_k3) + (A_mat_74 * x_k4) +
           (A_mat_75 * x_k5) + (A_mat_76 * x_k6) + (A_mat_77 * x_k7) + (A_mat_78 * x_k8) +
           (B_mat_77 * (u_cmd7 - 58.0));

x_pred8 := (A_mat_81 * x_k1) + (A_mat_82 * x_k2) + (A_mat_83 * x_k3) + (A_mat_84 * x_k4) +
           (A_mat_85 * x_k5) + (A_mat_86 * x_k6) + (A_mat_87 * x_k7) + (A_mat_88 * x_k8) +
           (B_mat_81 * (u_cmd1 - 65.0)) + (B_mat_83 * (u_cmd3 - 50.0)) +
           (B_mat_85 * (u_cmd5 - 72.0)) + (B_mat_88 * (u_cmd8 - 50.0));

(* 3.3: Receding-Horizon Quadratic Cost Optimization Gradient Step *)
(* Delta_u = - alpha * (B^T * Q * x_pred + R * Delta_u_prev) *)
IF (iFSM_CurrentState >= 5) AND (iFSM_CurrentState <= 10) THEN
    (* Control Loop 1: Stock Fan Pump VFD *)
    u_cmd1 := u_cmd1 - (0.015 * ((B_mat_11 * Q_w1 * x_pred1) + (B_mat_41 * Q_w4 * x_pred4) +
                                 (B_mat_81 * Q_w8 * x_pred8) + (R_w1 * (u_cmd1 - 65.0))));

    (* Control Loop 2: Headbox Air Pad Pressurization / Exhaust Valve *)
    u_cmd2 := u_cmd2 - (0.018 * ((B_mat_12 * Q_w1 * x_pred1) + (B_mat_22 * Q_w2 * x_pred2) +
                                 (R_w2 * (u_cmd2 - 45.0))));

    (* Control Loop 3: CD Dilution Master Header Valve *)
    u_cmd3 := u_cmd3 - (0.012 * ((B_mat_33 * Q_w3 * x_pred3) + (B_mat_83 * Q_w8 * x_pred8) +
                                 (R_w3 * (u_cmd3 - 50.0))));

    (* Control Loop 4: Forming Wire Velocity Reference Trim *)
    u_cmd4 := u_cmd4 - (0.008 * ((B_mat_44 * Q_w4 * x_pred4) + (R_w4 * (u_cmd4 - rMachineSpeed_Target_mpm))));

    (* Control Loop 5: Shoe Press Hydraulic Proportional Servo Valve *)
    u_cmd5 := u_cmd5 - (0.014 * ((B_mat_55 * Q_w5 * x_pred5) + (B_mat_85 * Q_w8 * x_pred8) +
                                 (R_w5 * (u_cmd5 - 72.0))));

    (* Control Loop 6: Dryer Section 1-3 Cascade Steam Valve *)
    u_cmd6 := u_cmd6 - (0.020 * ((B_mat_66 * Q_w6 * x_pred6) + (R_w6 * (u_cmd6 - 38.0))));

    (* Control Loop 7: Dryer Section 4-6 Cascade Steam Valve *)
    u_cmd7 := u_cmd7 - (0.022 * ((B_mat_77 * Q_w7 * x_pred7) + (R_w7 * (u_cmd7 - 58.0))));

    (* Control Loop 8: CD Thermal Slice Lip Master Energy *)
    u_cmd8 := u_cmd8 - (0.016 * ((B_mat_88 * Q_w8 * x_pred8) + (R_w8 * (u_cmd8 - 50.0))));
END_IF;

(* 3.4: Saturation Constraints on Actuators *)
IF u_cmd1 > 100.0 THEN u_cmd1 := 100.0; ELSIF u_cmd1 < 0.0 THEN u_cmd1 := 0.0; END_IF;
IF u_cmd2 > 100.0 THEN u_cmd2 := 100.0; ELSIF u_cmd2 < 0.0 THEN u_cmd2 := 0.0; END_IF;
IF u_cmd3 > 100.0 THEN u_cmd3 := 100.0; ELSIF u_cmd3 < 0.0 THEN u_cmd3 := 0.0; END_IF;
IF u_cmd4 > 1900.0 THEN u_cmd4 := 1900.0; ELSIF u_cmd4 < 300.0 THEN u_cmd4 := 300.0; END_IF;
IF u_cmd5 > 100.0 THEN u_cmd5 := 100.0; ELSIF u_cmd5 < 0.0 THEN u_cmd5 := 0.0; END_IF;
IF u_cmd6 > 100.0 THEN u_cmd6 := 100.0; ELSIF u_cmd6 < 0.0 THEN u_cmd6 := 0.0; END_IF;
IF u_cmd7 > 100.0 THEN u_cmd7 := 100.0; ELSIF u_cmd7 < 0.0 THEN u_cmd7 := 0.0; END_IF;
IF u_cmd8 > 100.0 THEN u_cmd8 := 100.0; ELSIF u_cmd8 < 0.0 THEN u_cmd8 := 0.0; END_IF;

(* Assign MPC commands to physical actuator outputs *)
rStockFanPump_SpeedCmd_pct := u_cmd1;
IF u_cmd2 >= 50.0 THEN
    rHeadboxAirPad_PressValve_pct := (u_cmd2 - 50.0) * 2.0;
    rHeadboxAirPad_ExhaustValve_pct := 0.0;
ELSE
    rHeadboxAirPad_PressValve_pct := 0.0;
    rHeadboxAirPad_ExhaustValve_pct := (50.0 - u_cmd2) * 2.0;
END_IF;
rSliceDilution_MasterHeaderValve_pct := u_cmd3;
rFormingWire_DriveSpeedCmd_mpm := u_cmd4;
rShoePress_HydraulicServoCmd_pct := u_cmd5;
rDryerSec1_SteamValveCmd_pct := u_cmd6;
rDryerSec2_SteamValveCmd_pct := u_cmd6 * 1.15;
rDryerSec3_SteamValveCmd_pct := u_cmd6 * 1.25;
rDryerSec4_SteamValveCmd_pct := u_cmd7;
rDryerSec5_SteamValveCmd_pct := u_cmd7 * 0.90;
rDryerSec6_SteamValveCmd_pct := u_cmd7 * 0.65;
""")

    # -------------------------------------------------------------------------
    # PART 8: Code Body - Phase 4: 12-Stage Operational Finite State Machine
    # -------------------------------------------------------------------------
    parts.append("""(* =====================================================================================================
 * PHASE 4: 12-STAGE DETERMINISTIC OPERATIONAL FINITE STATE MACHINE (FSM)
 * Controls paper machine sequencing from standby warm circulation through full-speed production,
 * broke recovery, and optical web break emergency dump.
 * ===================================================================================================== *)

tFSM_StateTimer_s := tFSM_StateTimer_s + c_rCycleTime_s;

CASE iFSM_CurrentState OF

    1: (* STANDBY_WARM_CIRCULATION *)
        sActiveFSM_StateName := 'STANDBY_WARM_CIRCULATION';
        bStockDumpValve_ToBrokePulper := TRUE; (* Diverted *)
        bShoePress_EmergencyNipOpen := TRUE;   (* Disengaged *)
        bDryerSteam_FastSetbackVent := FALSE;
        bCalender_RapidRollSeparate := TRUE;
        rFormingWire_DriveSpeedCmd_mpm := 150.0; (* Creep / Wash Speed *)
        rShoePress_LinearLoadActual_kNm := 0.0;
        rReel_DriveTorqueCmd_Nm := 0.0;

        IF bMasterMachineEnable AND bLubricationLubePackReady AND (tFSM_StateTimer_s >= 5.0) THEN
            iFSM_NextState := 2; (* Advance to Dryer Preheating *)
            tFSM_StateTimer_s := 0.0;
        END_IF;

    2: (* DRYER_SECTION_PREHEAT_STEAM *)
        sActiveFSM_StateName := 'DRYER_SECTION_PREHEAT_STEAM';
        (* Warm up steam cylinders gradually at 0.5 bar to evacuate condensate rimming *)
        rDryerSec1_SteamValveCmd_pct := 15.0;
        rDryerSec4_SteamValveCmd_pct := 20.0;
        rDryerSiphon_DiffPressValve_pct := 35.0;
        rFormingWire_DriveSpeedCmd_mpm := 250.0;

        IF (rVoted_DryerSec1Steam_bar >= 1.20) AND (tFSM_StateTimer_s >= 10.0) THEN
            iFSM_NextState := 3; (* Advance to Wire Fabric Wash *)
            tFSM_StateTimer_s := 0.0;
        END_IF;

    3: (* WIRE_FABRIC_WASH_AND_START *)
        sActiveFSM_StateName := 'WIRE_FABRIC_WASH_AND_START';
        rFormingWire_DriveSpeedCmd_mpm := 600.0;
        rSuctionBox_VacuumControlValve_pct := 20.0;

        IF (rVoted_FormingWireSpeed_mpm >= 580.0) AND (tFSM_StateTimer_s >= 5.0) THEN
            iFSM_NextState := 4; (* Advance to Headbox Total Head Priming *)
            tFSM_StateTimer_s := 0.0;
        END_IF;

    4: (* HEADBOX_TOTAL_HEAD_PRIME *)
        sActiveFSM_StateName := 'HEADBOX_TOTAL_HEAD_PRIME';
        rStockFanPump_SpeedCmd_pct := 40.0;
        rHeadboxAirPad_PressValve_pct := 30.0;
        rFormingWire_DriveSpeedCmd_mpm := 900.0;

        IF (rVoted_HeadboxTotalHead_kPa >= 200.0) AND (tFSM_StateTimer_s >= 5.0) THEN
            iFSM_NextState := 5; (* Advance to Stock Jet Engagement *)
            tFSM_StateTimer_s := 0.0;
        END_IF;

    5: (* STOCK_JET_ENGAGEMENT_ON_WIRE *)
        sActiveFSM_StateName := 'STOCK_JET_ENGAGEMENT_ON_WIRE';
        bStockDumpValve_ToBrokePulper := FALSE; (* Direct stock jet to forming wire *)
        rFormingWire_DriveSpeedCmd_mpm := 1200.0;

        IF (rObserved_JetToWireRatio >= 0.980) AND (rObserved_JetToWireRatio <= 1.050) AND
           (tFSM_StateTimer_s >= 6.0) THEN
            iFSM_NextState := 6; (* Advance to Vacuum Dewatering Step-Up *)
            tFSM_StateTimer_s := 0.0;
        END_IF;

    6: (* VACUUM_DEWATERING_STEPUP *)
        sActiveFSM_StateName := 'VACUUM_DEWATERING_STEPUP';
        rSuctionBox_VacuumControlValve_pct := 65.0;
        rCouchRoll_VacuumControlValve_pct := 75.0;

        IF (rVoted_WireSuctionBox_kPa <= -35.0) AND (tFSM_StateTimer_s >= 5.0) THEN
            iFSM_NextState := 7; (* Advance to Shoe Press Nip Engagement *)
            tFSM_StateTimer_s := 0.0;
        END_IF;

    7: (* SHOE_PRESS_NIP_ENGAGEMENT *)
        sActiveFSM_StateName := 'SHOE_PRESS_NIP_ENGAGEMENT';
        bShoePress_EmergencyNipOpen := FALSE; (* Engage Hydraulic Loading *)
        rShoePress_LinearLoadCmd_kNm := 800.0; (* Ramp step 1 *)
        rShoePress_TendingSideLoadCmd_kNm := 790.0;
        rShoePress_CenterLoadCmd_kNm := 810.0;
        rShoePress_DriveSideLoadCmd_kNm := 800.0;
        rShoePress_LinearLoadActual_kNm := rVoted_ShoePressNipLoad_kNm;

        IF (rVoted_ShoePressNipLoad_kNm >= 750.0) AND (rObserved_ShoeOilFilm_um >= 20.0) AND
           (tFSM_StateTimer_s >= 8.0) THEN
            iFSM_NextState := 8; (* Advance to Tail Threading *)
            tFSM_StateTimer_s := 0.0;
        END_IF;

    8: (* TAIL_THREADING_VACUUM_TRANSFER *)
        sActiveFSM_StateName := 'TAIL_THREADING_VACUUM_TRANSFER';
        rFormingWire_DriveSpeedCmd_mpm := 1400.0;
        rShoePress_LinearLoadCmd_kNm := 1200.0;
        rReel_DriveTorqueCmd_Nm := 250.0;

        IF bStartTailThreadingCmd OR (tFSM_StateTimer_s >= 12.0) THEN
            iFSM_NextState := 9; (* Advance to Full Width 1,800 m/min Production *)
            tFSM_StateTimer_s := 0.0;
        END_IF;

    9: (* FULL_WIDTH_1800MPM_PRODUCTION *)
        sActiveFSM_StateName := 'FULL_WIDTH_1800MPM_PRODUCTION';
        bShoePress_EmergencyNipOpen := FALSE;
        bCalender_RapidRollSeparate := FALSE;
        rShoePress_LinearLoadCmd_kNm := rShoePress_LinearLoad_SP_kNm;
        rShoePress_TendingSideLoadCmd_kNm := rShoePress_LinearLoad_SP_kNm * 0.995;
        rShoePress_CenterLoadCmd_kNm := rShoePress_LinearLoad_SP_kNm * 1.010;
        rShoePress_DriveSideLoadCmd_kNm := rShoePress_LinearLoad_SP_kNm * 0.995;
        rShoePress_LinearLoadActual_kNm := rVoted_ShoePressNipLoad_kNm;
        rReel_DriveTorqueCmd_Nm := 450.0;

        IF (rVoted_FormingWireSpeed_mpm >= 1780.0) AND (tFSM_StateTimer_s >= 15.0) THEN
            bMachineRunningAtTarget := TRUE;
            IF bEnableCDProfileOptimization THEN
                iFSM_NextState := 10; (* Advance to CD Profile Optimization *)
                tFSM_StateTimer_s := 0.0;
            END_IF;
        END_IF;

    10: (* CROSS_DIRECTION_PROFILE_OPTIMIZE *)
        sActiveFSM_StateName := 'CROSS_DIRECTION_PROFILE_OPTIMIZE';
        bMachineRunningAtTarget := TRUE;
        (* Actively running CD multivariable decoupling loop in Phase 5 *)

    11: (* BROKE_RECOVERY_AND_FLUSH *)
        sActiveFSM_StateName := 'BROKE_RECOVERY_AND_FLUSH';
        bMachineRunningAtTarget := FALSE;
        bStockDumpValve_ToBrokePulper := TRUE; (* Dump to broke pit *)
        bShoePress_EmergencyNipOpen := TRUE;   (* Lift press *)
        bCalender_RapidRollSeparate := TRUE;
        rFormingWire_DriveSpeedCmd_mpm := 300.0;
        rShoePress_LinearLoadActual_kNm := 0.0;
        rReel_DriveTorqueCmd_Nm := 0.0;

        IF bAcknowledgeAlarmsCmd AND (tFSM_StateTimer_s >= 10.0) THEN
            iFSM_NextState := 1; (* Return to Warm Circulation *)
            tFSM_StateTimer_s := 0.0;
        END_IF;

    12: (* EMERGENCY_ESTOP_WEB_BREAK_DUMP *)
        sActiveFSM_StateName := 'EMERGENCY_ESTOP_WEB_BREAK_DUMP';
        bMachineRunningAtTarget := FALSE;
        bWebBreakActive := TRUE;
        bStockDumpValve_ToBrokePulper := TRUE; (* < 15 ms Fast Dump *)
        bShoePress_EmergencyNipOpen := TRUE;   (* Rapid Hydraulic Depressurization *)
        bDryerSteam_FastSetbackVent := TRUE;   (* Vent Steam Headers *)
        bCalender_RapidRollSeparate := TRUE;   (* Drop Calender Rolls *)
        rStockFanPump_SpeedCmd_pct := 0.0;
        rHeadboxAirPad_PressValve_pct := 0.0;
        rHeadboxAirPad_ExhaustValve_pct := 100.0;
        rShoePress_LinearLoadActual_kNm := 0.0;
        rReel_DriveTorqueCmd_Nm := 0.0;

        IF bAcknowledgeAlarmsCmd AND NOT bEmergencyStopManual AND (tFSM_StateTimer_s >= 8.0) THEN
            iFSM_NextState := 11; (* Proceed to Broke Recovery *)
            tFSM_StateTimer_s := 0.0;
        END_IF;

END_CASE;

(* Update active FSM state register *)
iFSM_CurrentState := iFSM_NextState;
iActiveFSM_State := iFSM_CurrentState;
""")

    # -------------------------------------------------------------------------
    # PART 9: Code Body - Phase 5: Cross-Direction Profiling
    # -------------------------------------------------------------------------
    parts.append("""(* =====================================================================================================
 * PHASE 5: CROSS-DIRECTION (CD) BASIS WEIGHT & MOISTURE DECOUPLING PROFILE ENGINE
 * Implements 32-zone slice dilution valves, 32-zone thermal expansion micro-bolts,
 * and 16-zone soft calender induction roll heating coils across 8,500 mm web.
 * ===================================================================================================== *)

IF (iFSM_CurrentState = 9) OR (iFSM_CurrentState = 10) THEN
    FOR iCD_ZoneIdx := 1 TO 32 DO
        (* Basis Weight error per zone [g/m2] *)
        aCD_BW_Error_gsm[iCD_ZoneIdx] := aCD_BasisWeight_Filtered_gsm[iCD_ZoneIdx] - rBasisWeight_SP_gsm;

        (* Moisture error per zone [%] *)
        aCD_Moist_Error_pct[iCD_ZoneIdx] := aCD_Moisture_Filtered_pct[iCD_ZoneIdx] - rMoisture_SP_pct;

        (* CD Dilution Valve Control: Increased dilution lowers local consistency and lowers basis weight *)
        (* Coupling with adjacent neighbors to eliminate spatial checkerboarding *)
        IF iCD_ZoneIdx = 1 THEN
            aCD_DilutionTrim_pct[1] := 50.0 + (c_rCD_CouplingCenter * aCD_BW_Error_gsm[1] * 2.80) +
                                       (c_rCD_CouplingNeighbor * aCD_BW_Error_gsm[2] * 2.80);
        ELSIF iCD_ZoneIdx = 32 THEN
            aCD_DilutionTrim_pct[32] := 50.0 + (c_rCD_CouplingCenter * aCD_BW_Error_gsm[32] * 2.80) +
                                        (c_rCD_CouplingNeighbor * aCD_BW_Error_gsm[31] * 2.80);
        ELSE
            aCD_DilutionTrim_pct[iCD_ZoneIdx] := 50.0 +
                (c_rCD_CouplingCenter * aCD_BW_Error_gsm[iCD_ZoneIdx] * 2.80) +
                (c_rCD_CouplingNeighbor * aCD_BW_Error_gsm[iCD_ZoneIdx - 1] * 1.40) +
                (c_rCD_CouplingNeighbor * aCD_BW_Error_gsm[iCD_ZoneIdx + 1] * 1.40);
        END_IF;

        (* Clamp dilution trim bounds [0.0 .. 100.0 %] *)
        IF aCD_DilutionTrim_pct[iCD_ZoneIdx] > 100.0 THEN
            aCD_DilutionTrim_pct[iCD_ZoneIdx] := 100.0;
        ELSIF aCD_DilutionTrim_pct[iCD_ZoneIdx] < 0.0 THEN
            aCD_DilutionTrim_pct[iCD_ZoneIdx] := 0.0;
        END_IF;
        aSliceDilution_ZoneValveCmd_pct[iCD_ZoneIdx] := aCD_DilutionTrim_pct[iCD_ZoneIdx];

        (* Slice Lip Thermal Expansion Actuators: Thermal heating expands bolt and narrows local slice gap *)
        aCD_ThermalExpansionTrim_pct[iCD_ZoneIdx] := 50.0 + (aCD_BW_Error_gsm[iCD_ZoneIdx] * 3.50);
        IF aCD_ThermalExpansionTrim_pct[iCD_ZoneIdx] > 100.0 THEN
            aCD_ThermalExpansionTrim_pct[iCD_ZoneIdx] := 100.0;
        ELSIF aCD_ThermalExpansionTrim_pct[iCD_ZoneIdx] < 0.0 THEN
            aCD_ThermalExpansionTrim_pct[iCD_ZoneIdx] := 0.0;
        END_IF;
        aSliceLip_ThermalActuatorPwr_pct[iCD_ZoneIdx] := aCD_ThermalExpansionTrim_pct[iCD_ZoneIdx];
    END_FOR;

    (* 16-Zone Soft Calender Induction Thermal Roll Camber Profiling *)
    FOR iCD_ZoneIdx := 1 TO 16 DO
        (* Induction heating expands roll diameter locally to increase nip pressure and compact moisture/caliper *)
        aCD_CalenderInductionTrim_pct[iCD_ZoneIdx] := 50.0 +
            (((aCD_Moist_Error_pct[(iCD_ZoneIdx * 2) - 1] + aCD_Moist_Error_pct[iCD_ZoneIdx * 2]) * 0.50) * 8.50);
        IF aCD_CalenderInductionTrim_pct[iCD_ZoneIdx] > 100.0 THEN
            aCD_CalenderInductionTrim_pct[iCD_ZoneIdx] := 100.0;
        ELSIF aCD_CalenderInductionTrim_pct[iCD_ZoneIdx] < 0.0 THEN
            aCD_CalenderInductionTrim_pct[iCD_ZoneIdx] := 0.0;
        END_IF;
        aCalender_InductionHeaterPwr_pct[iCD_ZoneIdx] := aCD_CalenderInductionTrim_pct[iCD_ZoneIdx];
    END_FOR;
ELSE
    (* Machine not in full production: Hold CD profiling at nominal 50% baseline *)
    FOR iCD_ZoneIdx := 1 TO 32 DO
        aSliceDilution_ZoneValveCmd_pct[iCD_ZoneIdx] := 50.0;
        aSliceLip_ThermalActuatorPwr_pct[iCD_ZoneIdx] := 50.0;
    END_FOR;
    FOR iCD_ZoneIdx := 1 TO 16 DO
        aCalender_InductionHeaterPwr_pct[iCD_ZoneIdx] := 30.0;
    END_FOR;
END_IF;
""")

    # -------------------------------------------------------------------------
    # PART 10: Code Body - Phase 6: ISA-18.2 Process Alarms & Emergency Interlocks
    # -------------------------------------------------------------------------
    parts.append("""(* =====================================================================================================
 * PHASE 6: ISA-18.2 MULTI-TIERED PROCESS ALARMS & FAST WEB BREAK EMERGENCY INTERLOCK
 * 5-tier alarm evaluation (HI_HI, HI, LO, LO_LO, ROC) with deadband hysteresis,
 * < 15 ms optical web break detection, and automatic transition to emergency broke dump.
 * ===================================================================================================== *)

(* --- 6.1: Headbox Total Head Pressure Alarms --- *)
IF rVoted_HeadboxTotalHead_kPa >= c_rTrip_HB_Press_HI_HI THEN
    bAlarm_HB_Press_HI_HI := TRUE;
ELSIF rVoted_HeadboxTotalHead_kPa <= (c_rTrip_HB_Press_HI_HI - c_rDeadband_HB_Press) THEN
    bAlarm_HB_Press_HI_HI := FALSE;
END_IF;

IF rVoted_HeadboxTotalHead_kPa >= c_rTrip_HB_Press_HI THEN
    bAlarm_HB_Press_HI := TRUE;
ELSIF rVoted_HeadboxTotalHead_kPa <= (c_rTrip_HB_Press_HI - c_rDeadband_HB_Press) THEN
    bAlarm_HB_Press_HI := FALSE;
END_IF;

IF rVoted_HeadboxTotalHead_kPa <= c_rTrip_HB_Press_LO_LO THEN
    bAlarm_HB_Press_LO_LO := TRUE;
ELSIF rVoted_HeadboxTotalHead_kPa >= (c_rTrip_HB_Press_LO_LO + c_rDeadband_HB_Press) THEN
    bAlarm_HB_Press_LO_LO := FALSE;
END_IF;

IF rVoted_HeadboxTotalHead_kPa <= c_rTrip_HB_Press_LO THEN
    bAlarm_HB_Press_LO := TRUE;
ELSIF rVoted_HeadboxTotalHead_kPa >= (c_rTrip_HB_Press_LO + c_rDeadband_HB_Press) THEN
    bAlarm_HB_Press_LO := FALSE;
END_IF;

(* --- 6.2: Extended Nip Shoe Press Linear Load Alarms --- *)
IF rVoted_ShoePressNipLoad_kNm >= c_rTrip_ShoeLoad_HI_HI THEN
    bAlarm_ShoeLoad_HI_HI := TRUE;
ELSIF rVoted_ShoePressNipLoad_kNm <= (c_rTrip_ShoeLoad_HI_HI - c_rDeadband_ShoeLoad) THEN
    bAlarm_ShoeLoad_HI_HI := FALSE;
END_IF;

IF rVoted_ShoePressNipLoad_kNm >= c_rTrip_ShoeLoad_HI THEN
    bAlarm_ShoeLoad_HI := TRUE;
ELSIF rVoted_ShoePressNipLoad_kNm <= (c_rTrip_ShoeLoad_HI - c_rDeadband_ShoeLoad) THEN
    bAlarm_ShoeLoad_HI := FALSE;
END_IF;

IF rVoted_ShoePressNipLoad_kNm <= c_rTrip_ShoeLoad_LO_LO THEN
    bAlarm_ShoeLoad_LO_LO := TRUE;
ELSIF rVoted_ShoePressNipLoad_kNm >= (c_rTrip_ShoeLoad_LO_LO + c_rDeadband_ShoeLoad) THEN
    bAlarm_ShoeLoad_LO_LO := FALSE;
END_IF;

IF rVoted_ShoePressNipLoad_kNm <= c_rTrip_ShoeLoad_LO THEN
    bAlarm_ShoeLoad_LO := TRUE;
ELSIF rVoted_ShoePressNipLoad_kNm >= (c_rTrip_ShoeLoad_LO + c_rDeadband_ShoeLoad) THEN
    bAlarm_ShoeLoad_LO := FALSE;
END_IF;

(* --- 6.3: Shoe Press Hydrodynamic Oil Film Thickness Critical Protection --- *)
IF rObserved_ShoeOilFilm_um <= c_rTrip_OilFilm_LO_LO THEN
    bAlarm_OilFilm_LO_LO := TRUE;
    (* Imminent shoe rubbing / belt delamination danger -> trigger emergency nip separation *)
    bShoePress_EmergencyNipOpen := TRUE;
ELSIF rObserved_ShoeOilFilm_um >= (c_rTrip_OilFilm_LO_LO + c_rDeadband_OilFilm) THEN
    bAlarm_OilFilm_LO_LO := FALSE;
END_IF;

IF rObserved_ShoeOilFilm_um <= c_rTrip_OilFilm_LO THEN
    bAlarm_OilFilm_LO := TRUE;
ELSIF rObserved_ShoeOilFilm_um >= (c_rTrip_OilFilm_LO + c_rDeadband_OilFilm) THEN
    bAlarm_OilFilm_LO := FALSE;
END_IF;

(* --- 6.4: Dryer Section 4 Steam Pressure & Siphon Evacuation Alarms --- *)
IF rVoted_DryerSec4Steam_bar >= c_rTrip_DryerSec4_HI_HI THEN
    bAlarm_DryerSec4_HI_HI := TRUE;
ELSIF rVoted_DryerSec4Steam_bar <= (c_rTrip_DryerSec4_HI_HI - c_rDeadband_Dryer) THEN
    bAlarm_DryerSec4_HI_HI := FALSE;
END_IF;

IF rVoted_DryerSec4Steam_bar <= c_rTrip_DryerSec4_LO_LO THEN
    bAlarm_DryerSec4_LO_LO := TRUE;
ELSIF rVoted_DryerSec4Steam_bar >= (c_rTrip_DryerSec4_LO_LO + c_rDeadband_Dryer) THEN
    bAlarm_DryerSec4_LO_LO := FALSE;
END_IF;

IF rVoted_DryerSiphonDiff_kPa <= c_rTrip_SiphonDiff_LO_LO THEN
    bAlarm_SiphonDiff_LO_LO := TRUE;
ELSIF rVoted_DryerSiphonDiff_kPa >= (c_rTrip_SiphonDiff_LO_LO + c_rDeadband_SiphonDiff) THEN
    bAlarm_SiphonDiff_LO_LO := FALSE;
END_IF;

(* --- 6.5: Reel Web Tension Snap ROC & Level Alarms --- *)
rReelTension_ROC := (rVoted_ReelTension_Nm - rReelTension_Prev) / c_rCycleTime_s;
rReelTension_Prev := rVoted_ReelTension_Nm;

IF rReelTension_ROC <= c_rTrip_ReelTension_ROC_Snap THEN
    bAlarm_ReelTension_SnapROC := TRUE;
ELSE
    bAlarm_ReelTension_SnapROC := FALSE;
END_IF;

IF rVoted_ReelTension_Nm <= c_rTrip_ReelTension_LO_LO THEN
    bAlarm_ReelTension_LO_LO := TRUE;
ELSIF rVoted_ReelTension_Nm >= (c_rTrip_ReelTension_LO_LO + c_rDeadband_ReelTension) THEN
    bAlarm_ReelTension_LO_LO := FALSE;
END_IF;

IF rVoted_ReelTension_Nm >= c_rTrip_ReelTension_HI_HI THEN
    bAlarm_ReelTension_HI_HI := TRUE;
ELSIF rVoted_ReelTension_Nm <= (c_rTrip_ReelTension_HI_HI - c_rDeadband_ReelTension) THEN
    bAlarm_ReelTension_HI_HI := FALSE;
END_IF;

(* --- 6.6: Fast Web Break Emergency Interlock Trip (< 15 ms Response) --- *)
IF bVoted_WebBreak_Optical OR bAlarm_ReelTension_SnapROC THEN
    bWebBreakOpticalDetected := TRUE;
    tWebBreakPersistenceTimer := tWebBreakPersistenceTimer + c_rCycleTime_s;
    IF tWebBreakPersistenceTimer >= 0.015 THEN (* 15 ms confirmation *)
        bWebBreakActive := TRUE;
        iFSM_NextState := 12; (* Force Emergency Broke Dump State *)
        iFSM_CurrentState := 12;
    END_IF;
ELSE
    bWebBreakOpticalDetected := FALSE;
    tWebBreakPersistenceTimer := 0.0;
END_IF;

(* Manual Emergency Stop Pushbutton Trip *)
IF bEmergencyStopManual THEN
    bMachineInInterlock := TRUE;
    iFSM_NextState := 12;
    iFSM_CurrentState := 12;
END_IF;
""")

    # -------------------------------------------------------------------------
    # PART 11: Code Body - Phase 7: Diagnostic Words & Final Packing
    # -------------------------------------------------------------------------
    parts.append("""(* =====================================================================================================
 * PHASE 7: ISA-18.2 BIT-PACKING INTO DIAGNOSTIC & STATUS WORDS
 * ===================================================================================================== *)

(* Critical Priority 1 Trips: wAlarmWord_Critical_ISA18 *)
wAlarmWord_Critical_ISA18 := 16#00000000;
IF bAlarm_HB_Press_HI_HI       THEN wAlarmWord_Critical_ISA18 := wAlarmWord_Critical_ISA18 OR 16#00000001; END_IF;
IF bAlarm_HB_Press_LO_LO       THEN wAlarmWord_Critical_ISA18 := wAlarmWord_Critical_ISA18 OR 16#00000002; END_IF;
IF bAlarm_ShoeLoad_HI_HI       THEN wAlarmWord_Critical_ISA18 := wAlarmWord_Critical_ISA18 OR 16#00000004; END_IF;
IF bAlarm_ShoeLoad_LO_LO       THEN wAlarmWord_Critical_ISA18 := wAlarmWord_Critical_ISA18 OR 16#00000008; END_IF;
IF bAlarm_OilFilm_LO_LO        THEN wAlarmWord_Critical_ISA18 := wAlarmWord_Critical_ISA18 OR 16#00000010; END_IF;
IF bAlarm_DryerSec4_HI_HI      THEN wAlarmWord_Critical_ISA18 := wAlarmWord_Critical_ISA18 OR 16#00000020; END_IF;
IF bAlarm_SiphonDiff_LO_LO     THEN wAlarmWord_Critical_ISA18 := wAlarmWord_Critical_ISA18 OR 16#00000040; END_IF;
IF bWebBreakActive             THEN wAlarmWord_Critical_ISA18 := wAlarmWord_Critical_ISA18 OR 16#00000080; END_IF;
IF bEmergencyStopManual        THEN wAlarmWord_Critical_ISA18 := wAlarmWord_Critical_ISA18 OR 16#00000100; END_IF;

(* Operational Priority 2 Warnings: wAlarmWord_Warning_ISA18 *)
wAlarmWord_Warning_ISA18 := 16#00000000;
IF bAlarm_HB_Press_HI          THEN wAlarmWord_Warning_ISA18 := wAlarmWord_Warning_ISA18 OR 16#00000001; END_IF;
IF bAlarm_HB_Press_LO          THEN wAlarmWord_Warning_ISA18 := wAlarmWord_Warning_ISA18 OR 16#00000002; END_IF;
IF bAlarm_ShoeLoad_HI          THEN wAlarmWord_Warning_ISA18 := wAlarmWord_Warning_ISA18 OR 16#00000004; END_IF;
IF bAlarm_ShoeLoad_LO          THEN wAlarmWord_Warning_ISA18 := wAlarmWord_Warning_ISA18 OR 16#00000008; END_IF;
IF bAlarm_OilFilm_LO           THEN wAlarmWord_Warning_ISA18 := wAlarmWord_Warning_ISA18 OR 16#00000010; END_IF;
IF bAlarm_DryerSec4_HI         THEN wAlarmWord_Warning_ISA18 := wAlarmWord_Warning_ISA18 OR 16#00000020; END_IF;
IF bAlarm_DryerSec4_LO         THEN wAlarmWord_Warning_ISA18 := wAlarmWord_Warning_ISA18 OR 16#00000040; END_IF;
IF bAlarm_SiphonDiff_LO        THEN wAlarmWord_Warning_ISA18 := wAlarmWord_Warning_ISA18 OR 16#00000080; END_IF;
IF bAlarm_ReelTension_HI_HI    THEN wAlarmWord_Warning_ISA18 := wAlarmWord_Warning_ISA18 OR 16#00000100; END_IF;
IF bAlarm_ReelTension_LO_LO    THEN wAlarmWord_Warning_ISA18 := wAlarmWord_Warning_ISA18 OR 16#00000200; END_IF;

(* Machine Subsystem Health & Diagnostics Word: wDiagnosticState_Word *)
wDiagnosticState_Word := 16#00000000;
IF bMasterMachineEnable        THEN wDiagnosticState_Word := wDiagnosticState_Word OR 16#00000001; END_IF;
IF bLubricationLubePackReady   THEN wDiagnosticState_Word := wDiagnosticState_Word OR 16#00000002; END_IF;
IF bBrokePulperAgitatorRunning THEN wDiagnosticState_Word := wDiagnosticState_Word OR 16#00000004; END_IF;
IF bMachineRunningAtTarget     THEN wDiagnosticState_Word := wDiagnosticState_Word OR 16#00000008; END_IF;
IF bEnableCDProfileOptimization THEN wDiagnosticState_Word := wDiagnosticState_Word OR 16#00000010; END_IF;
wDiagnosticState_Word := wDiagnosticState_Word OR SHL(INT_TO_DWORD(iActiveFSM_State), 8);

END_FUNCTION_BLOCK
""")

    st_code = "".join(parts)
    return st_code

def check_parity(code_text):
    clean_lines = []
    in_block_comment = False
    
    for line in code_text.splitlines():
        cleaned = ""
        i = 0
        while i < len(line):
            if in_block_comment:
                if line[i:i+2] == "*)":
                    in_block_comment = False
                    i += 2
                else:
                    i += 1
            else:
                if line[i:i+2] == "(*":
                    in_block_comment = True
                    i += 2
                elif line[i:i+2] == "//":
                    break
                else:
                    cleaned += line[i]
                    i += 1
        clean_lines.append(cleaned)
        
    clean_text = "\n".join(clean_lines)
    
    if_count = len(re.findall(r'\bIF\b', clean_text, re.IGNORECASE))
    end_if_count = len(re.findall(r'\bEND_IF\b', clean_text, re.IGNORECASE))
    
    case_count = len(re.findall(r'\bCASE\b', clean_text, re.IGNORECASE))
    end_case_count = len(re.findall(r'\bEND_CASE\b', clean_text, re.IGNORECASE))
    
    for_count = len(re.findall(r'\bFOR\b', clean_text, re.IGNORECASE))
    end_for_count = len(re.findall(r'\bEND_FOR\b', clean_text, re.IGNORECASE))
    
    while_count = len(re.findall(r'\bWHILE\b', clean_text, re.IGNORECASE))
    end_while_count = len(re.findall(r'\bEND_WHILE\b', clean_text, re.IGNORECASE))
    
    fb_count = len(re.findall(r'\bFUNCTION_BLOCK\b', clean_text, re.IGNORECASE))
    end_fb_count = len(re.findall(r'\bEND_FUNCTION_BLOCK\b', clean_text, re.IGNORECASE))
    
    var_count = len(re.findall(r'\bVAR\b|\bVAR_INPUT\b|\bVAR_OUTPUT\b|\bVAR_IN_OUT\b', clean_text, re.IGNORECASE))
    end_var_count = len(re.findall(r'\bEND_VAR\b', clean_text, re.IGNORECASE))
    
    results = {
        "IF / END_IF": (if_count, end_if_count, if_count == end_if_count),
        "CASE / END_CASE": (case_count, end_case_count, case_count == end_case_count),
        "FOR / END_FOR": (for_count, end_for_count, for_count == end_for_count),
        "WHILE / END_WHILE": (while_count, end_while_count, while_count == end_while_count),
        "FUNCTION_BLOCK / END_FB": (fb_count, end_fb_count, fb_count == end_fb_count),
        "VAR / END_VAR": (var_count, end_var_count, var_count == end_var_count),
    }
    
    all_ok = all(v[2] for v in results.values())
    return all_ok, results

if __name__ == "__main__":
    code = generate_iec_code()
    print(f"Generated characters: {len(code)}")
    print(f"Generated lines: {len(code.splitlines())}")
    ok, res = check_parity(code)
    for k, v in res.items():
        print(f"{k}: {v[0]} vs {v[1]} -> {'PASS' if v[2] else 'FAIL'}")
    if not ok:
        print("FAIL: Parity mismatch")
        sys.exit(1)
    print("SUCCESS: 100% Parity Passed!")
