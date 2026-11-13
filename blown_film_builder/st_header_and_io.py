# blown_film_builder/st_header_and_io.py

def get_header_and_io():
    return """FUNCTION_BLOCK FB_Plastics_BlownFilm_7Layer_AirRing_ThicknessProfile
(*
====================================================================================================
LUMINA CYBER-PHYSICAL AUTOMATION KERNEL - IEC 61131-3 STRUCTURED TEXT
DOMAIN: PLASTICS & ADVANCED POLYMER PROCESSING / CO-EXTRUSION TIER-1
PROCESS: COMMERCIAL 7-LAYER BARRIER BLOWN FILM CO-EXTRUSION LINE FOR ASEPTIC FOOD PACKAGING
SUBSYSTEMS:
  - 7-LAYER CO-EXTRUSION DIE TOOLING: SPIRAL MANDREL DIE WITH SEPARATE FLOW CHANNELS FOR:
      * EXTRUDER A: OUTER SKIN (LDPE / LLDPE, GLOSS & ABRASION RESISTANCE, 25% MASS FRACTION)
      * EXTRUDER B: TIE LAYER 1 (MODIFIED POLYOLEFIN COPOLYMER ADHESIVE, 5% MASS FRACTION)
      * EXTRUDER C: BARRIER LAYER 1 (POLYAMIDE / NYLON-6, FLEX-CRACK & GAS RESISTANCE, 15% MASS FRACTION)
      * EXTRUDER D: CORE BARRIER (EVOH 32-MOL% ETHYLENE HIGH-OXYGEN BARRIER, 10% MASS FRACTION)
      * EXTRUDER E: BARRIER LAYER 2 (POLYAMIDE / NYLON-6, MECHANICAL STRENGTH, 15% MASS FRACTION)
      * EXTRUDER F: TIE LAYER 2 (MODIFIED POLYOLEFIN COPOLYMER ADHESIVE, 5% MASS FRACTION)
      * EXTRUDER G: INNER SEALANT (METALLOCENE mLLDPE HIGH-SEAL-INTEGRITY, 25% MASS FRACTION)
  - NON-CONTACT SEGMENTED DUAL-LIP AUTOMATIC AIR RING WITH 128 THERMAL EXPANSION BOLT SERVO ZONES
  - INTERNAL BUBBLE COOLING (IBC) WITH CLOSED-LOOP ULTRASONIC DIAMETER & DIFFERENTIAL PRESSURE CONTROL
  - OPTICAL INFRARED PYROMETER / NIR SPECTRAL FROST-LINE HEIGHT (FLH) TRACKING DETECTOR
  - ROTATING CAPACITIVE / BETA-GAUGE NON-CONTACT CIRCUMFERENTIAL FILM THICKNESS PROFILE SENSOR (128 BINS)
  - OSCILLATING REVERSING HAUL-OFF COLLAPSING CAGE NIP ROLL WEB TENSION & PHASE SYNCHRONIZATION
  - 6-STATE FIRST-PRINCIPLES CYBER-PHYSICAL DISCRETE STATE-SPACE OBSERVER (Ts = 20 [ms])
  - RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) WITH 10 UNROLLED ITERATIONS OF PROJECTED GRADIENT DESCENT (PGD)
  - 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING SUITE ACROSS 4 CRITICAL MEASUREMENT CHANNELS
  - DETERMINISTIC 14-STAGE BLOWN FILM PRODUCTION FINITE STATE MACHINE (FSM, STATES 0 TO 13)
  - ISA-18.2 MULTI-TIER PROCESS ALARM MATRIX (HH, H, L, LL) & BIT-PACKED 32-BIT TELEMETRY REGISTERS
====================================================================================================
*)
VAR_INPUT
    (* Master Supervisory Commands & Timing *)
    bEnable                         : BOOL;         (* Master Function Block Enable Signal [-] *)
    bAutoMode                       : BOOL;         (* Automatic Multi-Variable Closed-Loop Control Mode [-] *)
    bStartCycle                     : BOOL;         (* Sequence Start Production Command Signal [-] *)
    bStopCycle                      : BOOL;         (* Coordinated Production Line Stop Command [-] *)
    bEmergencyStop                  : BOOL;         (* Hardwired Catastrophic Safety Emergency Stop [-] *)
    bResetAlarms                    : BOOL;         (* Operator Alarm Reset & First-Out Latch Clearance [-] *)
    tScanCycleTime_s                : REAL := 0.020;(* Controller Real-Time Scan Cycle Sample Period [s] *)

    (* Production Recipe Setpoint Targets *)
    rRecipe_TargetThickness_um      : REAL := 60.0; (* Nominal Total Barrier Film Target Thickness [um] *)
    rRecipe_LayFlatWidth_mm         : REAL := 2600.0;(* Nominal Collapsed Web Lay-Flat Width [mm] *)
    rRecipe_LineSpeed_mpm           : REAL := 150.0;(* Nominal Haul-Off Line Speed Target [m/min] *)
    rRecipe_TargetFLH_mm            : REAL := 950.0;(* Target Bubble Frost-Line Solidification Height [mm] *)
    rRecipe_WebTension_N            : REAL := 420.0;(* Target Oscillating Haul-Off Nip Web Tension [N] *)
    rRecipe_DieTemp_Target_degC     : REAL := 225.0;(* Target Tooling Co-Extrusion Die Temperature [deg C] *)
    rRecipe_IBC_DiffPress_Target_Pa : REAL := 18.0; (* Target IBC Internal Differential Air Pressure [Pa] *)
    rRecipe_BlowUpRatio_BUR         : REAL := 3.31; (* Nominal Bubble Blow-Up Ratio (BUR = D_bubble/D_die) [-] *)

    (* 7-Layer Co-Extrusion Layer Distribution Fractions [%] *)
    rRecipe_ExtruderRatio_A_pct     : REAL := 25.0; (* Layer A: Outer Skin LDPE/LLDPE Target Mass Fraction [%] *)
    rRecipe_ExtruderRatio_B_pct     : REAL := 5.0;  (* Layer B: Tie Layer 1 Modified Copolymer Mass Fraction [%] *)
    rRecipe_ExtruderRatio_C_pct     : REAL := 15.0; (* Layer C: Barrier Layer 1 Nylon-6 PA Mass Fraction [%] *)
    rRecipe_ExtruderRatio_D_pct     : REAL := 10.0; (* Layer D: Core High-Barrier EVOH 32-Mol% Mass Fraction [%] *)
    rRecipe_ExtruderRatio_E_pct     : REAL := 15.0; (* Layer E: Barrier Layer 2 Nylon-6 PA Mass Fraction [%] *)
    rRecipe_ExtruderRatio_F_pct     : REAL := 5.0;  (* Layer F: Tie Layer 2 Modified Copolymer Mass Fraction [%] *)
    rRecipe_ExtruderRatio_G_pct     : REAL := 25.0; (* Layer G: Inner Sealant Metallocene mLLDPE Mass Fraction [%] *)

    (* Channel Group 1: 2oo3 Redundant IBC Ultrasonic Bubble Diameter Transducers [mm] *)
    rIBC_Transducer_1A_mm           : REAL;         (* IBC Non-Contact Ultrasonic Diameter Transducer 1A [mm] *)
    rIBC_Transducer_1B_mm           : REAL;         (* IBC Non-Contact Ultrasonic Diameter Transducer 1B [mm] *)
    rIBC_Transducer_1C_mm           : REAL;         (* IBC Non-Contact Ultrasonic Diameter Transducer 1C [mm] *)

    (* Channel Group 2: 2oo3 Redundant Frost-Line Optical Infrared Camera Height Sensors [mm] *)
    rFLH_Camera_2A_mm               : REAL;         (* Optical Infrared Phase-Transition FLH Camera 2A [mm] *)
    rFLH_Camera_2B_mm               : REAL;         (* Optical Infrared Phase-Transition FLH Camera 2B [mm] *)
    rFLH_Camera_2C_mm               : REAL;         (* Optical Infrared Phase-Transition FLH Camera 2C [mm] *)

    (* Channel Group 3: 2oo3 Redundant Die Exit Melt Pressure Transducers [bar] *)
    rMeltPress_Die_3A_bar           : REAL;         (* Co-Extrusion Die Exit Total Melt Pressure 3A [bar] *)
    rMeltPress_Die_3B_bar           : REAL;         (* Co-Extrusion Die Exit Total Melt Pressure 3B [bar] *)
    rMeltPress_Die_3C_bar           : REAL;         (* Co-Extrusion Die Exit Total Melt Pressure 3C [bar] *)

    (* Channel Group 4: 2oo3 Redundant Oscillating Haul-Off Web Tension Load Cells [N] *)
    rWebTension_HaulOff_4A_N        : REAL;         (* Oscillating Haul-Off Reversing Web Tension Cell 4A [N] *)
    rWebTension_HaulOff_4B_N        : REAL;         (* Oscillating Haul-Off Reversing Web Tension Cell 4B [N] *)
    rWebTension_HaulOff_4C_N        : REAL;         (* Oscillating Haul-Off Reversing Web Tension Cell 4C [N] *)

    (* Physical Process Feedback & Kinematic Sensor Inputs *)
    rGauge_CurrentAngle_deg         : REAL;         (* Rotating Thickness Scanner Angular Ring Position [deg] *)
    rHaulOff_OscillatingAngle_deg   : REAL;         (* Haul-Off Reversing Tower Oscillation Angle [deg] *)
    bHaulOff_OscillatingDirRev      : BOOL;         (* Haul-Off Oscillation Direction Flag (TRUE=CCW, FALSE=CW) [-] *)
    rExtruder_MeltTemp_A_degC       : REAL;         (* Extruder A Measured Barrel Discharge Melt Temp [deg C] *)
    rExtruder_MeltTemp_B_degC       : REAL;         (* Extruder B Measured Barrel Discharge Melt Temp [deg C] *)
    rExtruder_MeltTemp_C_degC       : REAL;         (* Extruder C Measured Barrel Discharge Melt Temp [deg C] *)
    rExtruder_MeltTemp_D_degC       : REAL;         (* Extruder D Measured Barrel Discharge Melt Temp [deg C] *)
    rExtruder_MeltTemp_E_degC       : REAL;         (* Extruder E Measured Barrel Discharge Melt Temp [deg C] *)
    rExtruder_MeltTemp_F_degC       : REAL;         (* Extruder F Measured Barrel Discharge Melt Temp [deg C] *)
    rExtruder_MeltTemp_G_degC       : REAL;         (* Extruder G Measured Barrel Discharge Melt Temp [deg C] *)
    rAirRing_SupplyFlowVelocity_mps : REAL;         (* Dual-Lip Air Ring Main Plenum Flow Velocity [m/s] *)
    rAirRing_SecondaryChilledAirTemp_degC : REAL;   (* Air Ring Secondary Lip Chilled Air Temperature [deg C] *)
    rIBC_DiffPressure_Sensor_Pa     : REAL;         (* Internal Bubble Cooling Air Cage Differential Pressure [Pa] *)
    arrThicknessProfile_Raw_um      : ARRAY[0..127] OF REAL; (* Rotating Gauge 128-Sector Raw Film Thickness Profile [um] *)
END_VAR
VAR_OUTPUT
    (* Segmented Air Ring 128 Thermal Expansion Bolt Actuator Power Commands [%] *)
    arrAirRing_ThermalBoltPower_pct : ARRAY[0..127] OF REAL; (* 128-Zone Thermal Bolt Heating Power Trim [0..100 %] *)

    (* Dual-Lip Air Ring & Chiller Actuator Commands *)
    rAirRing_BlowerFlowValve_pct    : REAL;         (* Primary Dual-Lip Air Ring Blower Throttle Valve [0..100 %] *)
    rAirRing_ChillerTrimValve_pct   : REAL;         (* Secondary Lip Modulating Chilled Air Heat Exchanger [0..100 %] *)

    (* Internal Bubble Cooling (IBC) Fan Inverter Speed Commands *)
    rIBC_SupplyBlower_Speed_RPM     : REAL;         (* IBC Internal Supply Blower VFD Speed Reference [RPM] *)
    rIBC_ExhaustBlower_Speed_RPM    : REAL;         (* IBC Internal Exhaust Blower VFD Speed Reference [RPM] *)

    (* 7-Layer Co-Extrusion Extruder Drive Speed References [RPM] *)
    rExtruder_SpeedCmd_A_RPM        : REAL;         (* Extruder A Outer Skin Screw Speed Command [RPM] *)
    rExtruder_SpeedCmd_B_RPM        : REAL;         (* Extruder B Tie 1 Screw Speed Command [RPM] *)
    rExtruder_SpeedCmd_C_RPM        : REAL;         (* Extruder C Barrier 1 PA Screw Speed Command [RPM] *)
    rExtruder_SpeedCmd_D_RPM        : REAL;         (* Extruder D Barrier Core EVOH Screw Speed Command [RPM] *)
    rExtruder_SpeedCmd_E_RPM        : REAL;         (* Extruder E Barrier 2 PA Screw Speed Command [RPM] *)
    rExtruder_SpeedCmd_F_RPM        : REAL;         (* Extruder F Tie 2 Screw Speed Command [RPM] *)
    rExtruder_SpeedCmd_G_RPM        : REAL;         (* Extruder G Sealant Inner Skin Screw Speed Command [RPM] *)

    (* Oscillating Haul-Off Line Drive & Web Tension Commands *)
    rHaulOff_LineSpeed_Cmd_mpm      : REAL;         (* Oscillating Haul-Off Nip Roll Line Speed Command [m/min] *)
    rHaulOff_NipTensionTrim_N       : REAL;         (* Oscillating Nip Roll Web Tension Pneumatic Trim [N] *)

    (* Production Supervisory Status & Diagnostic Metrics *)
    eState_Current                  : INT;          (* Active 14-Stage Blown Film Extrusion Machine State [0..13] *)
    bSystemReady                    : BOOL;         (* Extrusion Line Interlocks Clear and Operational [-] *)
    bInProduction                   : BOOL;         (* High-Speed Steady Production Active Within Spec [-] *)
    bDegradedSensorMode             : BOOL;         (* TMR Sensor Channel Operating in Degraded Redundancy [-] *)
    bCriticalTrip                   : BOOL;         (* Production Abort Trip Latched on Critical Safety Interlock [-] *)

    (* Film Quality Metrology & Statistical Quality Control (SQC) *)
    rProfile_AverageThickness_um    : REAL;         (* Measured Arithmetic Mean Circumferential Thickness [um] *)
    rProfile_2SigmaThickness_pct    : REAL;         (* Circumferential Thickness 2-Sigma Gauge Variation [%] *)
    rProfile_MaxPeak_um             : REAL;         (* Maximum Spatial Thickness Peak Detected [um] *)
    rProfile_MinTrough_um           : REAL;         (* Minimum Spatial Thickness Trough Detected [um] *)

    (* First-Principles Cyber-Physical Observer Estimated States *)
    rEstimated_ThicknessDev_um      : REAL;         (* Observer Estimated 2-Sigma Thickness Error [um] *)
    rEstimated_BubbleDiameter_mm    : REAL;         (* Observer Estimated Internal Bubble Diameter [mm] *)
    rEstimated_IBC_DiffPress_Pa     : REAL;         (* Observer Estimated Air Differential Pressure [Pa] *)
    rEstimated_FLH_mm               : REAL;         (* Observer Estimated Frost-Line Solidification Height [mm] *)
    rEstimated_MeltTemp_degC        : REAL;         (* Observer Estimated Bulk Melt Tooling Temperature [deg C] *)
    rEstimated_WebTension_N         : REAL;         (* Observer Estimated Haul-Off Nip Web Tension [N] *)
    rMPC_CurrentCost_J              : REAL;         (* Receding-Horizon MPC Quadratic Cost Objective J [-] *)

    (* 32-Bit Bit-Packed Telemetry & Diagnostic Registers *)
    dwStatusWord1                   : DWORD;        (* Machine Operating State Telemetry Bitfield 1 [-] *)
    dwStatusWord2                   : DWORD;        (* Extruder & Subsystem Run Interlock Bitfield 2 [-] *)
    dwAlarmWord1                    : DWORD;        (* ISA-18.2 Process Trip & TMR Alarm Bitfield 1 [-] *)
    dwAlarmWord2                    : DWORD;        (* Film Quality & Thermal Excursion Alarm Bitfield 2 [-] *)
    dwFirstOutWord                  : DWORD;        (* Latched First-Out Emergency Trip Diagnostic Word [-] *)
END_VAR
"""
