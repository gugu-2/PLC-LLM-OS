# -*- coding: utf-8 -*-
"""
Generator script for FB_Infrastructure_TunnelBoring_EarthPressureBalance_SlurryShield
IEC 61131-3 Structured Text Synthetic Dataset
"""
import sys
import os

def generate_iec_st():
    parts = []

    # =========================================================================
    # HEADER & DECLARATION
    # =========================================================================
    parts.append("""FUNCTION_BLOCK FB_Infrastructure_TunnelBoring_EarthPressureBalance_SlurryShield
(*
====================================================================================================
LUMINA CYBER-PHYSICAL AUTOMATION KERNEL - IEC 61131-3 STRUCTURED TEXT
DOMAIN: CIVIL INFRASTRUCTURE & HEAVY TUNNELING / HEAVY UNDERGROUND MECHANIZED EXCAVATION
SYSTEM: 14.2-METER MIXSHIELD EARTH PRESSURE BALANCE (EPB) & SLURRY SHIELD TUNNEL BORING MACHINE (TBM)
PROCESS CONTROL SPECIFICATION:
  - 14.2m Sub-Riverbed Shield Tunnel Excavation under 6.0 bar Hydrostatic/Overburden Face Pressure
  - 24-Cylinder Hydraulic Propulsion Advance Thrust System (140,000 kN Total Thrust, 4 Articulated Quadrants)
  - 16 Variable-Frequency Cutterhead Hydraulic Drive Motors (22,000 kNm Breakaway/Excavation Torque)
  - Variable-Speed Heavy Ribbon-Shaft Screw Conveyor Volumetric Extraction & Active Pressure Sealing
  - Bentonite Slurry Chamber Submerged Compressed Air Cushion Bubble Level & Pressure Regulation
  - Tail Skin Annular Shield Void Synchronous Bi-Component Cementitious Grouting System (8 Multi-Point Ports)
  - Autonomous Guidance, Articulation Cylinder Pitch/Yaw Differential Steering & Stroke Profile Management
====================================================================================================
*)
VAR_INPUT
    (* ============================================================================================= *)
    (* TRIPLE MODULAR REDUNDANT (TMR 2oo3) CRITICAL SENSOR SUITES                                    *)
    (* ============================================================================================= *)
    (* Primary Bulkhead Earth & Slurry Face Pressure Transducers [bar] *)
    rBulkhead_EarthPress_1_bar          : REAL;         (* Diaphragm Pressure Transmitter 1 - Excavation Bulkhead Crown [bar] *)
    rBulkhead_EarthPress_2_bar          : REAL;         (* Diaphragm Pressure Transmitter 2 - Excavation Bulkhead Center [bar] *)
    rBulkhead_EarthPress_3_bar          : REAL;         (* Diaphragm Pressure Transmitter 3 - Excavation Bulkhead Invert [bar] *)

    (* Cutterhead Hydraulic Drive Manifold Operating Pressure [bar] *)
    rCutterhead_HydPress_1_bar          : REAL;         (* Hydraulic Pressure Transducer Drive Ring Manifold Group 1 [bar] *)
    rCutterhead_HydPress_2_bar          : REAL;         (* Hydraulic Pressure Transducer Drive Ring Manifold Group 2 [bar] *)
    rCutterhead_HydPress_3_bar          : REAL;         (* Hydraulic Pressure Transducer Drive Ring Manifold Group 3 [bar] *)

    (* Slurry Chamber Submerged Compressed Air Cushion Pressure [bar] *)
    rAirCushion_Press_1_bar             : REAL;         (* Slurry Chamber Compressed Air Bubble Pressure Transmitter A [bar] *)
    rAirCushion_Press_2_bar             : REAL;         (* Slurry Chamber Compressed Air Bubble Pressure Transmitter B [bar] *)
    rAirCushion_Press_3_bar             : REAL;         (* Slurry Chamber Compressed Air Bubble Pressure Transmitter C [bar] *)

    (* Tail Skin Annular Shield Void Grout Injection Line Pressure [bar] *)
    rGroutLine_Press_1_bar              : REAL;         (* Bi-Component Grout Injection Line Pressure Port 1-2 [bar] *)
    rGroutLine_Press_2_bar              : REAL;         (* Bi-Component Grout Injection Line Pressure Port 3-4 [bar] *)
    rGroutLine_Press_3_bar              : REAL;         (* Bi-Component Grout Injection Line Pressure Port 5-8 [bar] *)

    (* ============================================================================================= *)
    (* EXCAVATION CHAMBER & SLURRY CIRCUIT SENSORS                                                  *)
    (* ============================================================================================= *)
    rAirCushion_Level_m                 : REAL;         (* Slurry Chamber Compressed Air Cushion Liquid-Gas Interface Level [m] *)
    rSlurryFeed_Flow_m3h                : REAL;         (* Bentonite Slurry Feed Supply Line Magnetic Flowmeter [m3/h] *)
    rSlurryReturn_Flow_m3h              : REAL;         (* Bentonite Slurry Return Discharge Line Magnetic Flowmeter [m3/h] *)
    rSlurryFeed_Density_tm3             : REAL;         (* Bentonite Slurry Feed In-line Coriolis Mass Density [t/m3] *)
    rSlurryReturn_Density_tm3           : REAL;         (* Bentonite Slurry Discharge Line Coriolis Mass Density [t/m3] *)

    (* ============================================================================================= *)
    (* CUTTERHEAD MECHANICAL DRIVE & HYDRAULIC SENSORS                                              *)
    (* ============================================================================================= *)
    rCutterhead_Speed_RPM               : REAL;         (* Optical Tachometer Cutterhead Rotational Speed Feedback [RPM] *)
    rCutterhead_Torque_kNm              : REAL;         (* Dynamic Shaft Torsiometer Cutterhead Main Drive Torque [kNm] *)
    rCutterhead_BearingOilTemp_degC     : REAL;         (* Main Slew Ring Tri-Row Roller Bearing Lubrication Temp [deg C] *)

    (* ============================================================================================= *)
    (* 24 PROPULSION THRUST CYLINDER QUADRANT DISPLACEMENTS & PRESSURES                            *)
    (* ============================================================================================= *)
    rThrustStroke_Q1_Top_mm             : REAL;         (* Magnetostrictive Stroke Sensor - Quadrant 1 Crown Cylinders 1-6 [mm] *)
    rThrustStroke_Q2_Right_mm           : REAL;         (* Magnetostrictive Stroke Sensor - Quadrant 2 Right Cylinders 7-12 [mm] *)
    rThrustStroke_Q3_Bottom_mm          : REAL;         (* Magnetostrictive Stroke Sensor - Quadrant 3 Invert Cylinders 13-18 [mm] *)
    rThrustStroke_Q4_Left_mm            : REAL;         (* Magnetostrictive Stroke Sensor - Quadrant 4 Left Cylinders 19-24 [mm] *)
    rThrustPress_Q1_Top_bar             : REAL;         (* Hydraulic Pressure Transducer - Quadrant 1 Top Advance Circuit [bar] *)
    rThrustPress_Q2_Right_bar           : REAL;         (* Hydraulic Pressure Transducer - Quadrant 2 Right Advance Circuit [bar] *)
    rThrustPress_Q3_Bottom_bar          : REAL;         (* Hydraulic Pressure Transducer - Quadrant 3 Bottom Advance Circuit [bar] *)
    rThrustPress_Q4_Left_bar            : REAL;         (* Hydraulic Pressure Transducer - Quadrant 4 Left Advance Circuit [bar] *)

    (* ============================================================================================= *)
    (* SCREW CONVEYOR EXTRACTION & MUCK MASS BALANCE                                                 *)
    (* ============================================================================================= *)
    rScrewConveyor_Speed_RPM            : REAL;         (* Variable Frequency Drive Screw Conveyor Motor Speed [RPM] *)
    rScrewConveyor_Torque_kNm           : REAL;         (* Hydraulic Displacement Motor Screw Conveyor Shaft Torque [kNm] *)
    rScrewDischargeGate_Feedback_pct    : REAL;         (* Hydraulic Guillotine Discharge Gate Aperture Position [%] *)
    rMuckDischarge_MassRate_tph         : REAL;         (* Continuous Muck Transfer Belt Scale Mass Extraction Rate [t/h] *)
    rExcavatedSoil_Density_tm3          : REAL;         (* Radiometric In-Chamber Excavated Soil Gamma Density [t/m3] *)

    (* ============================================================================================= *)
    (* BI-COMPONENT ANNULAR TAIL VOID GROUTING FLOW FEEDBACK                                         *)
    (* ============================================================================================= *)
    rGroutFlow_CompA_Lmin               : REAL;         (* Positive Displacement Flowmeter Component A Cement Slurry [L/min] *)
    rGroutFlow_CompB_Lmin               : REAL;         (* Positive Displacement Flowmeter Component B Sodium Silicate [L/min] *)

    (* ============================================================================================= *)
    (* SHIELD GUIDANCE, ARTICULATION ATTITUDE & AUXILIARY PERMISSIVES                                *)
    (* ============================================================================================= *)
    rShield_Pitch_mrad                  : REAL;         (* Dual-Axis Inclinometer Shield Pitch Attitude Deviation [mrad] *)
    rShield_Yaw_mrad                    : REAL;         (* Laser Gyro Total Station Shield Horizontal Yaw Deviation [mrad] *)
    rShield_Roll_mrad                   : REAL;         (* Gravity Pendulum Shield Rotational Roll Angle [mrad] *)
    bSegmentErector_RingComplete        : BOOL;         (* Precast Concrete Lining Ring Assembly Completed Interlock [-] *)
    bSegmentErector_Parked              : BOOL;         (* Segment Erector Arm Safely Parked & Mechanical Lock Engaged [-] *)
    bWaterIngressSensor_Bulkhead        : BOOL;         (* Emergency Conductive Moisture Sensor - Excavation Bulkhead Seal [-] *)

    (* ============================================================================================= *)
    (* OPERATOR SUPERVISORY CONTROLS & SETPOINTS                                                    *)
    (* ============================================================================================= *)
    bSystemEnable                       : BOOL;         (* Master Supervisory System Enable & Hydraulic Power Pack Run [-] *)
    bAutoExcavationMode                 : BOOL;         (* Closed-Loop Auto Excavation & Steering Regulation Mode Select [-] *)
    bEmergencyStop                      : BOOL;         (* Hardwired E-Stop Circuit Status (Active Low De-Energized) [-] *)
    bAlarmReset                         : BOOL;         (* Supervisory Alarm Acknowledge & First-Out Latch Reset [-] *)
    bManualOverride                     : BOOL;         (* Manual Operator Jogging & Valve Maintenance Bypass Permit [-] *)
    rSet_FacePressure_bar               : REAL;         (* Desired Closed-Loop Earth Pressure Balance Setpoint [bar] *)
    rSet_AdvanceRate_mmmin              : REAL;         (* Target Shield Propulsion Advance Penetration Velocity [mm/min] *)
    rSet_CutterRPM                      : REAL;         (* Target Cutterhead Rotational Speed Setpoint [RPM] *)
    rSet_ScrewRPM                       : REAL;         (* Baseline Screw Conveyor Rotational Speed Setpoint [RPM] *)
    rSet_AirBubbleLevel_m               : REAL;         (* Slurry Chamber Compressed Air Bubble Equilibrium Level Setpoint [m] *)
    rSet_GroutPressure_bar              : REAL;         (* Annular Tail Shield Void Bi-Component Grout Injection Press SP [bar] *)
    rSet_GroutVolumeRatio_pct           : REAL;         (* Grout Over-Fill Volumetric Theoretical Target Ratio [100.0..140.0] [%] *)
    rSet_ShieldPitch_mrad               : REAL;         (* Tunnel Design Alignment Vertical Pitch Attitude Target [mrad] *)
    rSet_ShieldYaw_mrad                 : REAL;         (* Tunnel Design Alignment Horizontal Yaw Attitude Target [mrad] *)
END_VAR

VAR_OUTPUT
    (* ============================================================================================= *)
    (* 24 HYDRAULIC THRUST PROPULSION QUADRANT PROPORTIONAL FLOW COMMANDS [%]                         *)
    (* ============================================================================================= *)
    rThrustValve_Q1_Top_pct             : REAL;         (* Quadrant 1 Top Advance Proportional Directional Flow Valve [%] *)
    rThrustValve_Q2_Right_pct           : REAL;         (* Quadrant 2 Right Advance Proportional Directional Flow Valve [%] *)
    rThrustValve_Q3_Bottom_pct          : REAL;         (* Quadrant 3 Bottom Advance Proportional Directional Flow Valve [%] *)
    rThrustValve_Q4_Left_pct            : REAL;         (* Quadrant 4 Left Advance Proportional Directional Flow Valve [%] *)
    rThrustAdvanceRate_Cmd_mmmin        : REAL;         (* Coordinated Closed-Loop Propulsion Penetration Rate Command [mm/min] *)

    (* ============================================================================================= *)
    (* CUTTERHEAD MECHANICAL DRIVE COMMANDS                                                          *)
    (* ============================================================================================= *)
    rCutterhead_Speed_Cmd_RPM           : REAL;         (* Frequency Inverter Multi-Motor Speed Master Reference [RPM] *)
    rCutterhead_TorqueLimit_Cmd_kNm     : REAL;         (* Hydraulic Relief / VFD Variable Torque Limit Threshold [kNm] *)
    bCutterhead_Direction_CW            : BOOL;         (* Cutterhead Rotation Direction Command (TRUE=CW, FALSE=CCW) [-] *)

    (* ============================================================================================= *)
    (* MUCK DISCHARGE & SCREW CONVEYOR ACTUATION                                                     *)
    (* ============================================================================================= *)
    rScrewConveyor_Speed_Cmd_RPM        : REAL;         (* Screw Conveyor Hydraulic Drive Proportional Speed Command [RPM] *)
    rScrewGate_Pos_Cmd_pct              : REAL;         (* Screw Conveyor Discharge Hydraulic Gate Position Demand [%] *)

    (* ============================================================================================= *)
    (* SLURRY CIRCUIT & COMPRESSED AIR CUSHION BUBBLE VALVES                                         *)
    (* ============================================================================================= *)
    rAirSupply_Valve_Cmd_pct            : REAL;         (* Slurry Chamber Compressed Air Make-Up Flow Regulator Valve [%] *)
    rAirBleed_Valve_Cmd_pct             : REAL;         (* Slurry Chamber Compressed Air Exhaust Pressure Relief Valve [%] *)
    rSlurryFeedPump_Cmd_pct             : REAL;         (* Bentonite Slurry Surface Charge Feed Pump Variable Speed [%] *)
    rSlurryDischargePump_Cmd_pct        : REAL;         (* Slurry Chamber Slurry Evacuation Slurry Pump Variable Speed [%] *)

    (* ============================================================================================= *)
    (* SYNCHRONOUS ANNULAR TAIL VOID GROUTING ACTUATION                                              *)
    (* ============================================================================================= *)
    rGroutPumpA_Cmd_pct                 : REAL;         (* Component A Cement-Bentonite Slurry Positive Displacement Pump [%] *)
    rGroutPumpB_Cmd_pct                 : REAL;         (* Component B Sodium Silicate Accelerator Dosing Metering Pump [%] *)
    bGroutPort_Open_1                   : BOOL;         (* Tail Skin Annular Grout Injection Port 1 Actuation Solenoid [-] *)
    bGroutPort_Open_2                   : BOOL;         (* Tail Skin Annular Grout Injection Port 2 Actuation Solenoid [-] *)
    bGroutPort_Open_3                   : BOOL;         (* Tail Skin Annular Grout Injection Port 3 Actuation Solenoid [-] *)
    bGroutPort_Open_4                   : BOOL;         (* Tail Skin Annular Grout Injection Port 4 Actuation Solenoid [-] *)
    bGroutPort_Open_5                   : BOOL;         (* Tail Skin Annular Grout Injection Port 5 Actuation Solenoid [-] *)
    bGroutPort_Open_6                   : BOOL;         (* Tail Skin Annular Grout Injection Port 6 Actuation Solenoid [-] *)
    bGroutPort_Open_7                   : BOOL;         (* Tail Skin Annular Grout Injection Port 7 Actuation Solenoid [-] *)
    bGroutPort_Open_8                   : BOOL;         (* Tail Skin Annular Grout Injection Port 8 Actuation Solenoid [-] *)

    (* ============================================================================================= *)
    (* SOIL CONDITIONING & SAFETY EMERGENCY ISOLATION VALVES                                         *)
    (* ============================================================================================= *)
    rConditioner_Valve_Cmd_pct          : REAL;         (* Cutterhead Bulkhead Biodegradable Foam/Polymer Injection Valve [%] *)
    bEmergencySlurryGate_Close          : BOOL;         (* Emergency Bulkhead Hydraulic Submerged Slurry Isolation Gate [-] *)
    bCompressedAirSupply_Trip           : BOOL;         (* Pneumatic Emergency Face Support Compressed Air Cut-Off Trip [-] *)

    (* ============================================================================================= *)
    (* OBSERVER ESTIMATED STATES & GEOTECHNICAL PERFORMANCE INDICES                                  *)
    (* ============================================================================================= *)
    rEst_FacePressure_bar               : REAL;         (* Luenberger State-Space Estimated Face Earth/Slurry Pressure [bar] *)
    rEst_PenetrationRate_mmmin          : REAL;         (* Estimated Instantaneous Shield Advance Penetration Rate [mm/min] *)
    rEst_SpecificEnergy_kJm3            : REAL;         (* Estimated Excavation Specific Mechanical Energy Consumption [kJ/m3] *)
    rEst_TotalThrust_kN                 : REAL;         (* Estimated Aggregate Hydraulic Advance Thrust Force [kN] *)
    rEst_MuckExtractionRate_tph         : REAL;         (* Estimated Soil Volumetric Extraction Mass Discharge Rate [t/h] *)
    rEst_AirBubbleLevel_m               : REAL;         (* Estimated Compressed Air Cushion Liquid-Gas Bubble Level [m] *)
    rEst_AirCushionPress_bar            : REAL;         (* Estimated Compressed Air Bubble Pneumatic Cushion Pressure [bar] *)
    rEst_GroutPressure_bar              : REAL;         (* Estimated Annular Shield Void In-Situ Grouting Pressure [bar] *)
    rEst_GroutVolumeRatio_pct           : REAL;         (* Synchronous Tail Void Grouting Volume Over-Fill Ratio [%] *)
    rEst_ShieldPitch_mrad               : REAL;         (* Kinematic Dynamic Estimated Shield Pitch Deviation Angle [mrad] *)
    rEst_ShieldYaw_mrad                 : REAL;         (* Kinematic Dynamic Estimated Shield Yaw Deviation Angle [mrad] *)
    rCalc_FieldPenetrationIndex_kNmm    : REAL;         (* Geotechnical Field Penetration Index FPI = F_thrust / PR [kN/mm] *)
    rCalc_TorquePenetrationIndex_kNm_mm : REAL;         (* Geotechnical Torque Penetration Index TPI = Torque / PR [kNm/mm] *)
    rCalc_MuckMassDiscrepancy_pct       : REAL;         (* Over/Under Excavation Muck Mass Balance Discrepancy Error [%] *)
    rCalc_AnnularGroutFillRatio_pct     : REAL;         (* Injected Grout Volume vs Theoretical Annular Tail Void [%] *)
    rMpc_QuadraticCostMetric            : REAL;         (* MPC Optimization Quadratic Objective Cost Function Value [-] *)

    (* ============================================================================================= *)
    (* SUPERVISORY STATE MACHINE & 32-BIT BIT-PACKED TELEMETRY                                       *)
    (* ============================================================================================= *)
    iActiveFsmState                     : INT;          (* Deterministic Production State Machine Current State Index [0..13] *)
    bSystemRunning                      : BOOL;         (* TBM Excavation Subsystem Operational Active Running Status [-] *)
    bAdvancePermissive                  : BOOL;         (* All Critical Interlocks Satisfied for Shield Advance Advance [-] *)
    bTripInterlockActive                : BOOL;         (* High-Integrity Safety Instrumented Trip Shutdown Engaged [-] *)
    dwStatusWord1                       : DWORD;        (* TBM Mechanical Subsystems & Propulsion Health Status Bit-Packed *)
    dwStatusWord2                       : DWORD;        (* 2oo3 TMR Voting Health & Observer Convergence Telemetry Bits *)
    dwAlarmWord1                        : DWORD;        (* ISA-18.2 Critical Process Alarm Violations & Hard Trips (HH/LL) *)
    dwAlarmWord2                        : DWORD;        (* ISA-18.2 Process Warning Deviations & Sensor Fault Flags (H/L) *)
    dwFirstOutWord                      : DWORD;        (* First-Out Latching Root Cause Master Trip Code Indicator *)
END_VAR

VAR
    (* ============================================================================================= *)
    (* EXECUTION CONTROL & TIMING CONSTANTS                                                          *)
    (* ============================================================================================= *)
    bFirstScanDone                      : BOOL := FALSE;    (* One-Shot System Initialization Completed Latch Flag [-] *)
    tScanCycleTime_s                    : REAL := 0.050;    (* Discrete Real-Time Task Execution Sample Period [s] *)
    iCycleCounter                       : DINT := 0;        (* Rolling Scan Execution Monotonic Cycle Counter [-] *)

    (* ============================================================================================= *)
    (* TBM GEOMETRICAL, HYDRAULIC & GEOTECHNICAL PHYSICAL CONSTANTS                                  *)
    (* ============================================================================================= *)
    rTBM_Diameter_m                     : REAL := 14.20;    (* Outer Shield Cutterhead Bore Excavation Diameter [m] *)
    rTBM_FaceArea_m2                    : REAL := 158.368;  (* Full Excavation Face Circular Cross-Sectional Area [m2] *)
    rTBM_LiningOuterDia_m               : REAL := 13.80;    (* Precast Segmental Concrete Lining Outer Diameter [m] *)
    rTBM_AnnularVoidVolPerM_m3          : REAL := 8.796;    (* Theoretical Tail Skin Annular Annulus Void Volume Per Meter [m3/m] *)
    rSoil_NominalDensity_tm3            : REAL := 2.05;     (* In-Situ Undisturbed Saturated Riverbed Silt/Clay Density [t/m3] *)
    rHydrostaticEquilibriumSP_bar       : REAL := 6.00;     (* Nominal Riverbed Hydrostatic & Earth Overburden Face SP [bar] *)
    rMaxAllowableStroke_mm              : REAL := 2000.0;   (* Full Hydraulic Propulsion Cylinder Stroke Limit [mm] *)
    rStrokeDecelThreshold_mm            : REAL := 1850.0;   (* Propulsion Cylinder Deceleration Ramp Initiator Stroke [mm] *)

    (* ============================================================================================= *)
    (* DISCRETE CYBER-PHYSICAL STATE-SPACE SYSTEM (6x6 MATRICES Ts=50ms)                             *)
    (* State Vector x in R^6:                                                                        *)
    (*   x[1]: Excavation Chamber Face Pressure P_face [bar]                                         *)
    (*   x[2]: Shield Penetration Advance Velocity PR [mm/min]                                       *)
    (*   x[3]: Cutterhead Specific Mechanical Energy SE [kJ/m3]                                      *)
    (*   x[4]: Total Hydraulic Advance Propulsion Thrust Force F_thrust [kN]                         *)
    (*   x[5]: Screw Conveyor Volumetric Extraction Mass Rate [t/h]                                  *)
    (*   x[6]: Slurry Chamber Compressed Air Cushion Liquid-Gas Bubble Level [m]                     *)
    (* Control Vector u in R^6:                                                                      *)
    (*   u[1]: Master Propulsion Thrust Group Flow Valve Demand [0..100 %]                           *)
    (*   u[2]: Cutterhead Drive Motor Speed Reference [0..3.5 RPM]                                   *)
    (*   u[3]: Screw Conveyor Motor Rotational Speed Reference [0..22.0 RPM]                         *)
    (*   u[4]: Compressed Air Cushion Pressure Make-Up Regulator Valve [0..100 %]                    *)
    (*   u[5]: Bentonite Slurry Feed Supply Pump Speed Demand [0..100 %]                             *)
    (*   u[6]: Annular Tail Void Grout Injection Master Pump Demand [0..100 %]                       *)
    (* Measurement Vector y in R^6:                                                                  *)
    (*   y[1]: Bulkhead 2oo3 Voted Earth/Slurry Face Pressure [bar]                                  *)
    (*   y[2]: Measured Shield Advance Rate from Displacement Transducers [mm/min]                   *)
    (*   y[3]: Calculated Specific Excavation Energy from Torque/Advance [kJ/m3]                     *)
    (*   y[4]: Aggregate Hydraulic Cylinder Thrust Load Feedback [kN]                                *)
    (*   y[5]: Muck Conveyor Belt Scale Mass Flow Extraction Rate [t/h]                              *)
    (*   y[6]: Slurry Chamber Compressed Air Bubble Level Transmitter [m]                            *)
    (* ============================================================================================= *)
    x_state                             : ARRAY[1..6] OF REAL;      (* Estimated Physical State Vector x[k] [various] *)
    x_hat                               : ARRAY[1..6] OF REAL;      (* Luenberger Innovation-Corrected State Vector [various] *)
    x_pred                              : ARRAY[1..6] OF REAL;      (* A-Priori Model Predicted State Vector x[k+1|k] [various] *)
    x_ref                               : ARRAY[1..6] OF REAL;      (* Target State Reference Vector [various] *)
    u_ctrl                              : ARRAY[1..6] OF REAL;      (* Applied Real-Time Actuator Vector u[k] [various] *)
    u_prev                              : ARRAY[1..6] OF REAL;      (* Previous Scan Actuator Output Vector u[k-1] [various] *)
    y_meas                              : ARRAY[1..6] OF REAL;      (* Filtered 2oo3 Sensor Observation Vector y[k] [various] *)
    y_est                               : ARRAY[1..6] OF REAL;      (* Observer Projected Output Vector y_hat[k] [various] *)
    e_innov                             : ARRAY[1..6] OF REAL;      (* Luenberger Innovation Residual Vector [various] *)

    matA                                : ARRAY[1..6, 1..6] OF REAL;(* Discrete State Transition Matrix A (6x6) [-] *)
    matB                                : ARRAY[1..6, 1..6] OF REAL;(* Control Input Coupling Matrix B (6x6) [-] *)
    matC                                : ARRAY[1..6, 1..6] OF REAL;(* Output Measurement Sensitivity Matrix C (6x6) [-] *)
    matD                                : ARRAY[1..6, 1..6] OF REAL;(* Direct Feedthrough Coupling Matrix D (6x6) [-] *)
    matL                                : ARRAY[1..6, 1..6] OF REAL;(* Luenberger Observer Innovation Gain Matrix (6x6) [-] *)

    (* ============================================================================================= *)
    (* RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) MATRICES & PGD WORKSPACE                      *)
    (* ============================================================================================= *)
    matQ                                : ARRAY[1..6, 1..6] OF REAL;(* State Tracking Quadratic Penalty Matrix (6x6) [-] *)
    matR                                : ARRAY[1..6, 1..6] OF REAL;(* Control Effort Quadratic Penalty Matrix (6x6) [-] *)
    matP                                : ARRAY[1..6, 1..6] OF REAL;(* Terminal Riccati State Cost Penalty Matrix (6x6) [-] *)
    u_min                               : ARRAY[1..6] OF REAL;      (* Actuator Lower Box Saturation Constraint Vector [various] *)
    u_max                               : ARRAY[1..6] OF REAL;      (* Actuator Upper Box Saturation Constraint Vector [various] *)
    du_max                              : ARRAY[1..6] OF REAL;      (* Maximum Allowable Actuator Slew Rate Per Scan [various] *)

    (* Receding Prediction Horizon (Np=5 steps, 10 Unrolled PGD Iterations) *)
    x_rollout                           : ARRAY[1..5, 1..6] OF REAL;(* Predicted State Trajectory across Horizon [various] *)
    u_horizon                           : ARRAY[1..5, 1..6] OF REAL;(* Optimization Control Sequence across Horizon [various] *)
    grad_J                              : ARRAY[1..6] OF REAL;      (* Cost Function Projected Gradient Vector [various] *)
    rAlpha_pgd                          : REAL := 0.00045;          (* PGD Optimization Gradient Step Factor [-] *)
    rCost_J                             : REAL;                     (* Cumulative Quadratic Objective Function Metric [-] *)
    rDelta_u                            : REAL;                     (* Temporary Actuator Slew Rate Displacement [various] *)

    (* ============================================================================================= *)
    (* 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SUITE DATA STRUCTURES                                    *)
    (* ============================================================================================= *)
    (* Suite 1: Bulkhead Earth Pressure Diaphragms *)
    bHealthy_EP1                        : BOOL := TRUE;             (* Channel 1 Health Diagnostic Flag - Bulkhead Earth Press [-] *)
    bHealthy_EP2                        : BOOL := TRUE;             (* Channel 2 Health Diagnostic Flag - Bulkhead Earth Press [-] *)
    bHealthy_EP3                        : BOOL := TRUE;             (* Channel 3 Health Diagnostic Flag - Bulkhead Earth Press [-] *)
    rTimer_EP_12_sec                    : REAL := 0.0;              (* Channel 1-2 Pairwise Discrepancy Debounce Timer [s] *)
    rTimer_EP_23_sec                    : REAL := 0.0;              (* Channel 2-3 Pairwise Discrepancy Debounce Timer [s] *)
    rTimer_EP_31_sec                    : REAL := 0.0;              (* Channel 3-1 Pairwise Discrepancy Debounce Timer [s] *)
    bDiscrepancy_EP                     : BOOL := FALSE;            (* Bulkhead Earth Pressure Sensor Suite Discrepancy Flag [-] *)
    bDegraded_EP                        : BOOL := FALSE;            (* Bulkhead Earth Pressure Operating in Degraded 1oo2 Mode [-] *)
    rVoted_EP_bar                       : REAL := 6.0;              (* 2oo3 Voted Excavation Bulkhead Face Earth Pressure [bar] *)
    rVoted_EP_Prev                      : REAL := 6.0;              (* Previous Scan Voted Earth Pressure [bar] *)

    (* Suite 2: Cutterhead Hydraulic Drive Manifold Pressure *)
    bHealthy_CP1                        : BOOL := TRUE;             (* Channel 1 Health Diagnostic Flag - Cutterhead Hyd Press [-] *)
    bHealthy_CP2                        : BOOL := TRUE;             (* Channel 2 Health Diagnostic Flag - Cutterhead Hyd Press [-] *)
    bHealthy_CP3                        : BOOL := TRUE;             (* Channel 3 Health Diagnostic Flag - Cutterhead Hyd Press [-] *)
    rTimer_CP_12_sec                    : REAL := 0.0;              (* Channel 1-2 Pairwise Discrepancy Debounce Timer [s] *)
    rTimer_CP_23_sec                    : REAL := 0.0;              (* Channel 2-3 Pairwise Discrepancy Debounce Timer [s] *)
    rTimer_CP_31_sec                    : REAL := 0.0;              (* Channel 3-1 Pairwise Discrepancy Debounce Timer [s] *)
    bDiscrepancy_CP                     : BOOL := FALSE;            (* Cutterhead Hydraulic Pressure Sensor Discrepancy Flag [-] *)
    bDegraded_CP                        : BOOL := FALSE;            (* Cutterhead Hydraulic Pressure in Degraded 1oo2 Mode [-] *)
    rVoted_CP_bar                       : REAL := 220.0;            (* 2oo3 Voted Cutterhead Drive Hydraulic Pressure [bar] *)
    rVoted_CP_Prev                      : REAL := 220.0;            (* Previous Scan Voted Cutterhead Hydraulic Pressure [bar] *)

    (* Suite 3: Slurry Chamber Submerged Compressed Air Cushion Pressure *)
    bHealthy_AP1                        : BOOL := TRUE;             (* Channel 1 Health Diagnostic Flag - Air Cushion Press [-] *)
    bHealthy_AP2                        : BOOL := TRUE;             (* Channel 2 Health Diagnostic Flag - Air Cushion Press [-] *)
    bHealthy_AP3                        : BOOL := TRUE;             (* Channel 3 Health Diagnostic Flag - Air Cushion Press [-] *)
    rTimer_AP_12_sec                    : REAL := 0.0;              (* Channel 1-2 Pairwise Discrepancy Debounce Timer [s] *)
    rTimer_AP_23_sec                    : REAL := 0.0;              (* Channel 2-3 Pairwise Discrepancy Debounce Timer [s] *)
    rTimer_AP_31_sec                    : REAL := 0.0;              (* Channel 3-1 Pairwise Discrepancy Debounce Timer [s] *)
    bDiscrepancy_AP                     : BOOL := FALSE;            (* Compressed Air Cushion Pressure Discrepancy Flag [-] *)
    bDegraded_AP                        : BOOL := FALSE;            (* Compressed Air Cushion Pressure in Degraded 1oo2 Mode [-] *)
    rVoted_AP_bar                       : REAL := 6.0;              (* 2oo3 Voted Compressed Air Cushion Pressure [bar] *)
    rVoted_AP_Prev                      : REAL := 6.0;              (* Previous Scan Voted Air Cushion Pressure [bar] *)

    (* Suite 4: Tail Skin Annular Grout Injection Line Pressure *)
    bHealthy_GP1                        : BOOL := TRUE;             (* Channel 1 Health Diagnostic Flag - Grout Line Press [-] *)
    bHealthy_GP2                        : BOOL := TRUE;             (* Channel 2 Health Diagnostic Flag - Grout Line Press [-] *)
    bHealthy_GP3                        : BOOL := TRUE;             (* Channel 3 Health Diagnostic Flag - Grout Line Press [-] *)
    rTimer_GP_12_sec                    : REAL := 0.0;              (* Channel 1-2 Pairwise Discrepancy Debounce Timer [s] *)
    rTimer_GP_23_sec                    : REAL := 0.0;              (* Channel 2-3 Pairwise Discrepancy Debounce Timer [s] *)
    rTimer_GP_31_sec                    : REAL := 0.0;              (* Channel 3-1 Pairwise Discrepancy Debounce Timer [s] *)
    bDiscrepancy_GP                     : BOOL := FALSE;            (* Tail Skin Grout Pressure Sensor Discrepancy Flag [-] *)
    bDegraded_GP                        : BOOL := FALSE;            (* Tail Skin Grout Pressure in Degraded 1oo2 Mode [-] *)
    rVoted_GP_bar                       : REAL := 7.2;              (* 2oo3 Voted Annular Tail Void Grouting Pressure [bar] *)
    rVoted_GP_Prev                      : REAL := 7.2;              (* Previous Scan Voted Grout Line Pressure [bar] *)

    (* Discrepancy Limits & Debounce Constants *)
    rDiscrepancyTol_EP_bar              : REAL := 0.35;             (* Bulkhead Earth Pressure Max Pairwise Discrepancy [bar] *)
    rDiscrepancyTol_CP_bar              : REAL := 18.0;             (* Cutterhead Hydraulic Pressure Discrepancy Limit [bar] *)
    rDiscrepancyTol_AP_bar              : REAL := 0.25;             (* Air Cushion Pressure Max Pairwise Discrepancy [bar] *)
    rDiscrepancyTol_GP_bar              : REAL := 0.50;             (* Tail Grout Pressure Max Pairwise Discrepancy [bar] *)
    rDiscrepancyTimeout_sec             : REAL := 0.350;            (* Discrepancy Accumulation Debounce Timeout [s] *)

    (* ============================================================================================= *)
    (* DETERMINISTIC 14-STAGE PRODUCTION FINITE STATE MACHINE (FSM) WORKSPACE                        *)
    (* ============================================================================================= *)
    eState                              : INT := 0;                 (* Active FSM State Variable [0..13] *)
    eState_Prev                         : INT := 0;                 (* State Variable on Previous Scan [0..13] *)
    rStateTimer_sec                     : REAL := 0.0;              (* Monotonic Active State Dwell Timer [s] *)
    bStateFirstScan                     : BOOL := TRUE;             (* State Entry Pulse Flag [-] *)

    (* FSM Specific Step Progression Flags & Timers *)
    rPressurizeRamp_bar                 : REAL := 0.0;              (* Ramp Generator for Chamber Pressurization [bar] *)
    rBreakawayTimer_sec                 : REAL := 0.0;              (* Cutterhead Breakaway Torque Verification Timer [s] *)
    rThrustEngageRamp_kN                : REAL := 0.0;              (* Propulsion Hydraulic Load Pre-Stress Ramp [kN] *)
    bHardRockDetected                   : BOOL := FALSE;            (* Boulder / Hard Strata Encounter Detection Flag [-] *)
    rHardRockDecelTimer_sec             : REAL := 0.0;              (* Obstacle Deceleration & Torque Shedding Timer [s] *)
    bStrokeLimitReached                 : BOOL := FALSE;            (* Full Advance Stroke Limit Deceleration Initiated [-] *)
    rGroutPurgeTimer_sec                : REAL := 0.0;              (* Annular Line Flushing & Water Purge Timer [s] *)
    rSlurryFlushTimer_sec               : REAL := 0.0;              (* Slurry Chamber Agitation & Flushing Timer [s] *)
    bEmergencyTripLatched               : BOOL := FALSE;            (* Face Ingress / Structural Collapse Master Trip Latch [-] *)

    (* ============================================================================================= *)
    (* ARTICULATION STEERING & QUADRANT DIFFERENTIAL PROPORTIONAL FLOW CONTROL                        *)
    (* ============================================================================================= *)
    rPitchError_mrad                    : REAL := 0.0;              (* Vertical Pitch Attitude Alignment Error [mrad] *)
    rYawError_mrad                      : REAL := 0.0;              (* Horizontal Yaw Alignment Error [mrad] *)
    rTrim_Q1_Top_pct                    : REAL := 0.0;              (* Top Quadrant Proportional Steering Differential Trim [%] *)
    rTrim_Q2_Right_pct                  : REAL := 0.0;              (* Right Quadrant Proportional Steering Differential Trim [%] *)
    rTrim_Q3_Bottom_pct                 : REAL := 0.0;              (* Bottom Quadrant Proportional Steering Differential Trim [%] *)
    rTrim_Q4_Left_pct                   : REAL := 0.0;              (* Left Quadrant Proportional Steering Differential Trim [%] *)
    rKp_Steering_Pitch                  : REAL := 0.42;             (* Proportional Steering Gain for Pitch Attitude [%/mrad] *)
    rKp_Steering_Yaw                    : REAL := 0.45;             (* Proportional Steering Gain for Yaw Attitude [%/mrad] *)

    (* ============================================================================================= *)
    (* GEOTECHNICAL & MUCK EXTRACTION MASS BALANCE MONITORING                                        *)
    (* ============================================================================================= *)
    rAvgPropulsionStroke_mm             : REAL := 0.0;              (* Average Current Stroke Displacement of 24 Cylinders [mm] *)
    rPropulsionVelocity_mmmin           : REAL := 0.0;              (* Differential Stroke Derivative Advance Speed [mm/min] *)
    rStrokePrevious_mm                  : REAL := 0.0;              (* Previous Scan Average Stroke Displacement [mm] *)
    rTheoMuckVolumePerMin_m3min         : REAL := 0.0;              (* Theoretical In-Situ Excavated Volume Rate [m3/min] *)
    rTheoMuckMassRate_tph               : REAL := 0.0;              (* Theoretical Ground Mass Extraction Extraction Rate [t/h] *)
    rActualMuckMassRate_tph             : REAL := 0.0;              (* Filtered Muck Transfer Belt Scale Mass Flow [t/h] *)
    rTheoGroutFlow_Lmin                 : REAL := 0.0;              (* Theoretical Annular Tail Void Grout Infill Rate [L/min] *)
    rActualGroutFlow_Lmin               : REAL := 0.0;              (* Combined Delivered Grout Flow Rate Comp A + Comp B [L/min] *)

    (* ============================================================================================= *)
    (* ISA-18.2 ALARM ENGINE THRESHOLDS, DEADBANDS & TIMERS                                          *)
    (* ============================================================================================= *)
    (* Face Pressure Alarm Limits [bar] *)
    rLim_FacePress_HH_bar               : REAL := 7.20;             (* Face Pressure High-High Trip Threshold [bar] *)
    rLim_FacePress_H_bar                : REAL := 6.60;             (* Face Pressure High Warning Limit [bar] *)
    rLim_FacePress_L_bar                : REAL := 5.40;             (* Face Pressure Low Warning Limit [bar] *)
    rLim_FacePress_LL_bar               : REAL := 4.80;             (* Face Pressure Low-Low Cavitation/Collapse Trip Limit [bar] *)
    rDeadband_FacePress_bar             : REAL := 0.10;             (* Face Pressure Clearance Deadband Hysteresis [bar] *)

    (* Cutterhead Torque Alarm Limits [kNm] *)
    rLim_CutterTorque_HH_kNm            : REAL := 21500.0;          (* Cutterhead Torque High-High Main Bearing Protection [kNm] *)
    rLim_CutterTorque_H_kNm             : REAL := 19500.0;          (* Cutterhead Torque High Warning Approaching Boulder [kNm] *)
    rDeadband_CutterTorque_kNm          : REAL := 450.0;            (* Cutterhead Torque Clearance Deadband [kNm] *)

    (* Total Advance Thrust Limits [kN] *)
    rLim_TotalThrust_HH_kN              : REAL := 135000.0;         (* Total Advance Thrust Force High-High Trip Threshold [kN] *)
    rLim_TotalThrust_H_kN               : REAL := 120000.0;         (* Total Advance Thrust Force High Warning Limit [kN] *)
    rDeadband_TotalThrust_kN            : REAL := 2500.0;           (* Total Thrust Clearance Deadband [kN] *)

    (* Compressed Air Cushion Bubble Level Limits [m] *)
    rLim_AirBubbleLevel_HH_m            : REAL := 6.50;             (* Air Bubble Level High-High Ingress Warning [m] *)
    rLim_AirBubbleLevel_H_m             : REAL := 5.50;             (* Air Bubble Level High Warning [m] *)
    rLim_AirBubbleLevel_L_m             : REAL := 3.50;             (* Air Bubble Level Low Warning [m] *)
    rLim_AirBubbleLevel_LL_m            : REAL := 2.50;             (* Air Bubble Level Low-Low Slurry Flooding Trip Limit [m] *)
    rDeadband_AirBubbleLevel_m          : REAL := 0.15;             (* Air Bubble Level Clearance Deadband [m] *)

    (* Tail Skin Grout Pressure Limits [bar] *)
    rLim_GroutPress_HH_bar              : REAL := 8.50;             (* Annular Tail Grout Pressure High-High Seal Rupture Trip [bar] *)
    rLim_GroutPress_H_bar               : REAL := 7.80;             (* Annular Tail Grout Pressure High Warning Limit [bar] *)
    rLim_GroutPress_L_bar               : REAL := 4.50;             (* Annular Tail Grout Pressure Low Void Infill Warning [bar] *)
    rLim_GroutPress_LL_bar              : REAL := 3.50;             (* Annular Tail Grout Pressure Low-Low Cavity Collapse Trip [bar] *)
    rDeadband_GroutPress_bar            : REAL := 0.20;             (* Tail Grout Pressure Clearance Deadband [bar] *)

    (* Muck Mass Balance Over-Excavation Limit [%] *)
    rLim_MuckDiscrepancy_HH_pct         : REAL := 25.0;             (* Over-Excavation Sinkhole Risk Trip Limit [%] *)
    rLim_MuckDiscrepancy_H_pct          : REAL := 15.0;             (* Over-Excavation Geological Deviation Warning [%] *)

    (* Alarm Debounce Timers *)
    rAlarmTimer_FacePress_HH_sec        : REAL := 0.0;              (* Face Pressure HH Trip Debounce Accumulator [s] *)
    rAlarmTimer_FacePress_LL_sec        : REAL := 0.0;              (* Face Pressure LL Trip Debounce Accumulator [s] *)
    rAlarmTimer_CutterTorque_HH_sec     : REAL := 0.0;              (* Cutterhead Torque HH Trip Debounce Accumulator [s] *)
    rAlarmTimer_AirBubble_LL_sec        : REAL := 0.0;              (* Slurry Flooding LL Trip Debounce Accumulator [s] *)
    rAlarmTimer_WaterIngress_sec        : REAL := 0.0;              (* Bulkhead Seal Water Ingress Debounce Accumulator [s] *)

    (* First-Out Latching Identification Register *)
    iFirstOutCode                       : DINT := 0;                (* First-Out Master Fault Sequence Latch Code [-] *)

    (* Mathematical & Loop Scratch Variables *)
    iIter                               : INT;                      (* General Optimization Unrolled Iteration Counter [-] *)
    jIter                               : INT;                      (* General Matrix Column Counter [-] *)
    kIter                               : INT;                      (* General Horizon Step Counter [-] *)
    rTempDot                            : REAL;                     (* Temporary Vector Dot Product Register [-] *)
    rTempNorm                           : REAL;                     (* Temporary Vector Norm Register [-] *)
    rTempClip                           : REAL;                     (* Temporary Saturation Slew Limit Register [-] *)
END_VAR
""")

    # =========================================================================
    # PHASE 0: ONE-SHOT SYSTEM INITIALIZATION & MATRIX ALLOCATION
    # =========================================================================
    parts.append("""
(* ==================================================================================================== *)
(* PHASE 0: ONE-SHOT SYSTEM INITIALIZATION & CYBER-PHYSICAL STATE-SPACE MATRIX ALLOCATION               *)
(* ==================================================================================================== *)
IF NOT bFirstScanDone THEN
    (* ------------------------------------------------------------------------------------------------ *)
    (* Discrete State Transition Matrix matA (6x6) Ts = 0.050 s                                         *)
    (* Models coupled cyber-physics of sub-riverbed earth pressure balance, hydraulic penetration rate, *)
    (* rock fracture specific energy, thrust reaction, screw extraction and compressed air cushion level*)
    (* ------------------------------------------------------------------------------------------------ *)
    matA[1,1] := 0.9850; matA[1,2] := 0.0032; matA[1,3] := -0.0001; matA[1,4] := 0.00005; matA[1,5] := -0.00085; matA[1,6] := 0.0045;
    matA[2,1] := -0.0025; matA[2,2] := 0.9450; matA[2,3] := -0.00065; matA[2,4] := 0.00042; matA[2,5] := 0.00015; matA[2,6] := 0.0000;
    matA[3,1] := 0.0120; matA[3,2] := -0.0250; matA[3,3] := 0.9780; matA[3,4] := 0.0018; matA[3,5] := 0.0000; matA[3,6] := 0.0000;
    matA[4,1] := 0.1500; matA[4,2] := 0.3500; matA[4,3] := 0.0850; matA[4,4] := 0.9200; matA[4,5] := 0.0000; matA[4,6] := 0.0000;
    matA[5,1] := 0.0450; matA[5,2] := 0.2800; matA[5,3] := -0.0120; matA[5,4] := 0.0000; matA[5,5] := 0.9350; matA[5,6] := 0.0000;
    matA[6,1] := -0.0085; matA[6,2] := 0.0000; matA[6,3] := 0.0000; matA[6,4] := 0.0000; matA[6,5] := 0.0000; matA[6,6] := 0.9920;

    (* ------------------------------------------------------------------------------------------------ *)
    (* Control Input Coupling Matrix matB (6x6)                                                         *)
    (* Direct response to thrust flow, cutterhead RPM, screw speed, air valve, slurry pump, grout pump  *)
    (* ------------------------------------------------------------------------------------------------ *)
    matB[1,1] := 0.0042; matB[1,2] := 0.0085; matB[1,3] := -0.0185; matB[1,4] := 0.0125; matB[1,5] := 0.0065; matB[1,6] := 0.0015;
    matB[2,1] := 0.0385; matB[2,2] := 0.1450; matB[2,3] := 0.0000; matB[2,4] := 0.0000; matB[2,5] := 0.0000; matB[2,6] := 0.0000;
    matB[3,1] := 0.0850; matB[3,2] := 0.2200; matB[3,3] := 0.0000; matB[3,4] := 0.0000; matB[3,5] := 0.0000; matB[3,6] := 0.0000;
    matB[4,1] := 185.00; matB[4,2] := 12.50; matB[4,3] := 0.0000; matB[4,4] := 0.0000; matB[4,5] := 0.0000; matB[4,6] := 0.0000;
    matB[5,1] := 0.0000; matB[5,2] := 0.4500; matB[5,3] := 3.2500; matB[5,4] := 0.0000; matB[5,5] := 0.0000; matB[5,6] := 0.0000;
    matB[6,1] := 0.0000; matB[6,2] := 0.0000; matB[6,3] := 0.0000; matB[6,4] := 0.0165; matB[6,5] := -0.0225; matB[6,6] := 0.0000;

    (* ------------------------------------------------------------------------------------------------ *)
    (* Output Measurement Matrix matC (6x6)                                                             *)
    (* Direct physical mapping of state variables to voted sensor channels                              *)
    (* ------------------------------------------------------------------------------------------------ *)
    matC[1,1] := 1.0; matC[1,2] := 0.0; matC[1,3] := 0.0; matC[1,4] := 0.0; matC[1,5] := 0.0; matC[1,6] := 0.0;
    matC[2,1] := 0.0; matC[2,2] := 1.0; matC[2,3] := 0.0; matC[2,4] := 0.0; matC[2,5] := 0.0; matC[2,6] := 0.0;
    matC[3,1] := 0.0; matC[3,2] := 0.0; matC[3,3] := 1.0; matC[3,4] := 0.0; matC[3,5] := 0.0; matC[3,6] := 0.0;
    matC[4,1] := 0.0; matC[4,2] := 0.0; matC[4,3] := 0.0; matC[4,4] := 1.0; matC[4,5] := 0.0; matC[4,6] := 0.0;
    matC[5,1] := 0.0; matC[5,2] := 0.0; matC[5,3] := 0.0; matC[5,4] := 0.0; matC[5,5] := 1.0; matC[5,6] := 0.0;
    matC[6,1] := 0.0; matC[6,2] := 0.0; matC[6,3] := 0.0; matC[6,4] := 0.0; matC[6,5] := 0.0; matC[6,6] := 1.0;

    (* ------------------------------------------------------------------------------------------------ *)
    (* Direct Feedthrough Matrix matD (6x6) - Strictly Zero for Proper Causality                        *)
    (* ------------------------------------------------------------------------------------------------ *)
    FOR iIter := 1 TO 6 DO
        FOR jIter := 1 TO 6 DO
            matD[iIter, jIter] := 0.0;
        END_FOR;
    END_FOR;

    (* ------------------------------------------------------------------------------------------------ *)
    (* Luenberger Observer Innovation Gain Matrix matL (6x6)                                            *)
    (* Calibrated via Discrete-Time Algebraic Riccati Equation (DARE) for Fast Asymptotic Convergence   *)
    (* ------------------------------------------------------------------------------------------------ *)
    matL[1,1] := 0.3250; matL[1,2] := 0.0015; matL[1,3] := 0.0000; matL[1,4] := 0.00001; matL[1,5] := -0.0002; matL[1,6] := 0.0012;
    matL[2,1] := -0.0008; matL[2,2] := 0.2850; matL[2,3] := -0.0001; matL[2,4] := 0.00005; matL[2,5] := 0.0001; matL[2,6] := 0.0000;
    matL[3,1] := 0.0045; matL[3,2] := -0.0085; matL[3,3] := 0.3100; matL[3,4] := 0.0004; matL[3,5] := 0.0000; matL[3,6] := 0.0000;
    matL[4,1] := 0.0550; matL[4,2] := 0.0950; matL[4,3] := 0.0150; matL[4,4] := 0.3500; matL[4,5] := 0.0000; matL[4,6] := 0.0000;
    matL[5,1] := 0.0125; matL[5,2] := 0.0650; matL[5,3] := -0.0025; matL[5,4] := 0.0000; matL[5,5] := 0.2950; matL[5,6] := 0.0000;
    matL[6,1] := -0.0035; matL[6,2] := 0.0000; matL[6,3] := 0.0000; matL[6,4] := 0.0000; matL[6,5] := 0.0000; matL[6,6] := 0.2600;

    (* ------------------------------------------------------------------------------------------------ *)
    (* Model Predictive Control (MPC) Quadratic Weighting Matrices                                      *)
    (* Penalty on Face Pressure Deviation is Paramount to Prevent Sub-Riverbed Surface Collapse         *)
    (* ------------------------------------------------------------------------------------------------ *)
    FOR iIter := 1 TO 6 DO
        FOR jIter := 1 TO 6 DO
            matQ[iIter, jIter] := 0.0;
            matR[iIter, jIter] := 0.0;
            matP[iIter, jIter] := 0.0;
        END_FOR;
    END_FOR;
    matQ[1,1] := 450.0;     (* Face Earth Pressure Tracking Weight [1/bar^2] *)
    matQ[2,2] := 18.0;      (* Shield Advance Penetration Velocity Tracking Weight [1/(mm/min)^2] *)
    matQ[3,3] := 2.5;       (* Specific Mechanical Energy Optimization Penalty [1/(kJ/m3)^2] *)
    matQ[4,4] := 0.0008;    (* Hydraulic Thrust Force Penalty [1/kN^2] *)
    matQ[5,5] := 0.045;     (* Muck Mass Flow Rate Tracking Weight [1/(t/h)^2] *)
    matQ[6,6] := 85.0;      (* Air Cushion Bubble Level Stabilization Weight [1/m^2] *)

    matR[1,1] := 0.85;      (* Thrust Flow Valve Effort Penalty [1/%^2] *)
    matR[2,2] := 35.0;      (* Cutterhead Motor RPM Slew Penalty [1/RPM^2] *)
    matR[3,3] := 2.20;      (* Screw Conveyor Motor RPM Effort Penalty [1/RPM^2] *)
    matR[4,4] := 0.65;      (* Air Cushion Valve Effort Penalty [1/%^2] *)
    matR[5,5] := 0.45;      (* Bentonite Slurry Feed Pump Effort Penalty [1/%^2] *)
    matR[6,6] := 0.75;      (* Annular Grout Injection Master Pump Effort Penalty [1/%^2] *)

    matP[1,1] := 950.0;     (* Terminal Riccati Weight - Face Pressure *)
    matP[2,2] := 45.0;      (* Terminal Riccati Weight - Advance Rate *)
    matP[3,3] := 6.5;       (* Terminal Riccati Weight - Specific Energy *)
    matP[4,4] := 0.0025;    (* Terminal Riccati Weight - Thrust Force *)
    matP[5,5] := 0.120;     (* Terminal Riccati Weight - Muck Rate *)
    matP[6,6] := 210.0;     (* Terminal Riccati Weight - Bubble Level *)

    (* Actuator Slew Rate Maximum Limits Per Cycle (Ts = 0.050 s) *)
    du_max[1] := 1.50;      (* Thrust Valve Slew: max 30.0% / sec *)
    du_max[2] := 0.05;      (* Cutterhead RPM Slew: max 1.0 RPM / sec *)
    du_max[3] := 0.40;      (* Screw Conveyor Slew: max 8.0 RPM / sec *)
    du_max[4] := 2.50;      (* Air Supply Valve Slew: max 50.0% / sec *)
    du_max[5] := 1.80;      (* Slurry Feed Pump Slew: max 36.0% / sec *)
    du_max[6] := 1.20;      (* Grout Pump Slew: max 24.0% / sec *)

    (* Actuator Box Saturation Constraints *)
    u_min[1] := 0.0;    u_max[1] := 100.0;
    u_min[2] := 0.0;    u_max[2] := 3.50;
    u_min[3] := 0.0;    u_max[3] := 22.0;
    u_min[4] := 0.0;    u_max[4] := 100.0;
    u_min[5] := 0.0;    u_max[5] := 100.0;
    u_min[6] := 0.0;    u_max[6] := 100.0;

    (* Initialize State Vector to Hydrostatic Riverbed Equilibrium *)
    x_state[1] := 6.00;     (* Face Pressure nominal 6.0 bar *)
    x_state[2] := 0.0;      (* Stationary advance rate 0 mm/min *)
    x_state[3] := 8500.0;   (* Specific energy baseline 8500 kJ/m3 *)
    x_state[4] := 0.0;      (* Total thrust 0 kN *)
    x_state[5] := 0.0;      (* Muck rate 0 t/h *)
    x_state[6] := 4.50;     (* Compressed air cushion level nominal 4.5 m *)

    FOR iIter := 1 TO 6 DO
        x_hat[iIter] := x_state[iIter];
        x_pred[iIter] := x_state[iIter];
        u_ctrl[iIter] := 0.0;
        u_prev[iIter] := 0.0;
    END_FOR;

    bFirstScanDone := TRUE;
END_IF;

iCycleCounter := iCycleCounter + 1;
""")

    # =========================================================================
    # PHASE 1: 2oo3 TMR VOTING SUITE ACROSS ALL 4 CRITICAL TRANSMITTER GROUPS
    # =========================================================================
    parts.append("""
(* ==================================================================================================== *)
(* PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING WITH DISCREPANCY TIMERS                 *)
(* Across:                                                                                              *)
(*   1) Excavation Bulkhead Earth Pressure Cells (EP_Sensors: 1, 2, 3) [bar]                            *)
(*   2) Cutterhead Hydraulic Drive Manifold Transducers (CP_Sensors: 1, 2, 3) [bar]                     *)
(*   3) Slurry Chamber Compressed Air Bubble Transmitters (AP_Sensors: 1, 2, 3) [bar]                   *)
(*   4) Tail Skin Annular Grout Injection Transducers (GP_Sensors: 1, 2, 3) [bar]                       *)
(* ==================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------- *)
(* SUITE 1: EXCAVATION BULKHEAD EARTH PRESSURE (rBulkhead_EarthPress 1, 2, 3)                           *)
(* ---------------------------------------------------------------------------------------------------- *)
(* Range Validation & Out-of-Bounds Sensor Health Checks [0.0..12.0 bar] *)
bHealthy_EP1 := (rBulkhead_EarthPress_1_bar >= 0.0) AND (rBulkhead_EarthPress_1_bar <= 12.0);
bHealthy_EP2 := (rBulkhead_EarthPress_2_bar >= 0.0) AND (rBulkhead_EarthPress_2_bar <= 12.0);
bHealthy_EP3 := (rBulkhead_EarthPress_3_bar >= 0.0) AND (rBulkhead_EarthPress_3_bar <= 12.0);

(* Pairwise Discrepancy Accumulation Debounce *)
IF ABS(rBulkhead_EarthPress_1_bar - rBulkhead_EarthPress_2_bar) > rDiscrepancyTol_EP_bar THEN
    rTimer_EP_12_sec := rTimer_EP_12_sec + tScanCycleTime_s;
ELSE
    rTimer_EP_12_sec := 0.0;
END_IF;

IF ABS(rBulkhead_EarthPress_2_bar - rBulkhead_EarthPress_3_bar) > rDiscrepancyTol_EP_bar THEN
    rTimer_EP_23_sec := rTimer_EP_23_sec + tScanCycleTime_s;
ELSE
    rTimer_EP_23_sec := 0.0;
END_IF;

IF ABS(rBulkhead_EarthPress_3_bar - rBulkhead_EarthPress_1_bar) > rDiscrepancyTol_EP_bar THEN
    rTimer_EP_31_sec := rTimer_EP_31_sec + tScanCycleTime_s;
ELSE
    rTimer_EP_31_sec := 0.0;
END_IF;

bDiscrepancy_EP := (rTimer_EP_12_sec > rDiscrepancyTimeout_sec) OR
                   (rTimer_EP_23_sec > rDiscrepancyTimeout_sec) OR
                   (rTimer_EP_31_sec > rDiscrepancyTimeout_sec);

(* 2oo3 Median Voting Algorithm with Seamless Degradation *)
IF bHealthy_EP1 AND bHealthy_EP2 AND bHealthy_EP3 THEN
    bDegraded_EP := FALSE;
    (* All 3 Channels Healthy: Exact Median Calculation *)
    IF (rBulkhead_EarthPress_1_bar >= rBulkhead_EarthPress_2_bar AND rBulkhead_EarthPress_1_bar <= rBulkhead_EarthPress_3_bar) OR
       (rBulkhead_EarthPress_1_bar <= rBulkhead_EarthPress_2_bar AND rBulkhead_EarthPress_1_bar >= rBulkhead_EarthPress_3_bar) THEN
        rVoted_EP_bar := rBulkhead_EarthPress_1_bar;
    ELSIF (rBulkhead_EarthPress_2_bar >= rBulkhead_EarthPress_1_bar AND rBulkhead_EarthPress_2_bar <= rBulkhead_EarthPress_3_bar) OR
          (rBulkhead_EarthPress_2_bar <= rBulkhead_EarthPress_1_bar AND rBulkhead_EarthPress_2_bar >= rBulkhead_EarthPress_3_bar) THEN
        rVoted_EP_bar := rBulkhead_EarthPress_2_bar;
    ELSE
        rVoted_EP_bar := rBulkhead_EarthPress_3_bar;
    END_IF;
ELSIF bHealthy_EP1 AND bHealthy_EP2 THEN
    bDegraded_EP := TRUE;
    rVoted_EP_bar := (rBulkhead_EarthPress_1_bar + rBulkhead_EarthPress_2_bar) * 0.5;
ELSIF bHealthy_EP2 AND bHealthy_EP3 THEN
    bDegraded_EP := TRUE;
    rVoted_EP_bar := (rBulkhead_EarthPress_2_bar + rBulkhead_EarthPress_3_bar) * 0.5;
ELSIF bHealthy_EP3 AND bHealthy_EP1 THEN
    bDegraded_EP := TRUE;
    rVoted_EP_bar := (rBulkhead_EarthPress_3_bar + rBulkhead_EarthPress_1_bar) * 0.5;
ELSIF bHealthy_EP1 THEN
    bDegraded_EP := TRUE;
    rVoted_EP_bar := rBulkhead_EarthPress_1_bar;
ELSIF bHealthy_EP2 THEN
    bDegraded_EP := TRUE;
    rVoted_EP_bar := rBulkhead_EarthPress_2_bar;
ELSIF bHealthy_EP3 THEN
    bDegraded_EP := TRUE;
    rVoted_EP_bar := rBulkhead_EarthPress_3_bar;
ELSE
    (* Total Sensor Suite Failure: Freeze to Previous Scan Voted Value and Assert Interlock *)
    rVoted_EP_bar := rVoted_EP_Prev;
    bDegraded_EP := TRUE;
END_IF;
rVoted_EP_Prev := rVoted_EP_bar;

(* ---------------------------------------------------------------------------------------------------- *)
(* SUITE 2: CUTTERHEAD HYDRAULIC DRIVE MANIFOLD PRESSURE (rCutterhead_HydPress 1, 2, 3)                 *)
(* ---------------------------------------------------------------------------------------------------- *)
bHealthy_CP1 := (rCutterhead_HydPress_1_bar >= 0.0) AND (rCutterhead_HydPress_1_bar <= 420.0);
bHealthy_CP2 := (rCutterhead_HydPress_2_bar >= 0.0) AND (rCutterhead_HydPress_2_bar <= 420.0);
bHealthy_CP3 := (rCutterhead_HydPress_3_bar >= 0.0) AND (rCutterhead_HydPress_3_bar <= 420.0);

IF ABS(rCutterhead_HydPress_1_bar - rCutterhead_HydPress_2_bar) > rDiscrepancyTol_CP_bar THEN
    rTimer_CP_12_sec := rTimer_CP_12_sec + tScanCycleTime_s;
ELSE
    rTimer_CP_12_sec := 0.0;
END_IF;

IF ABS(rCutterhead_HydPress_2_bar - rCutterhead_HydPress_3_bar) > rDiscrepancyTol_CP_bar THEN
    rTimer_CP_23_sec := rTimer_CP_23_sec + tScanCycleTime_s;
ELSE
    rTimer_CP_23_sec := 0.0;
END_IF;

IF ABS(rCutterhead_HydPress_3_bar - rCutterhead_HydPress_1_bar) > rDiscrepancyTol_CP_bar THEN
    rTimer_CP_31_sec := rTimer_CP_31_sec + tScanCycleTime_s;
ELSE
    rTimer_CP_31_sec := 0.0;
END_IF;

bDiscrepancy_CP := (rTimer_CP_12_sec > rDiscrepancyTimeout_sec) OR
                   (rTimer_CP_23_sec > rDiscrepancyTimeout_sec) OR
                   (rTimer_CP_31_sec > rDiscrepancyTimeout_sec);

IF bHealthy_CP1 AND bHealthy_CP2 AND bHealthy_CP3 THEN
    bDegraded_CP := FALSE;
    IF (rCutterhead_HydPress_1_bar >= rCutterhead_HydPress_2_bar AND rCutterhead_HydPress_1_bar <= rCutterhead_HydPress_3_bar) OR
       (rCutterhead_HydPress_1_bar <= rCutterhead_HydPress_2_bar AND rCutterhead_HydPress_1_bar >= rCutterhead_HydPress_3_bar) THEN
        rVoted_CP_bar := rCutterhead_HydPress_1_bar;
    ELSIF (rCutterhead_HydPress_2_bar >= rCutterhead_HydPress_1_bar AND rCutterhead_HydPress_2_bar <= rCutterhead_HydPress_3_bar) OR
          (rCutterhead_HydPress_2_bar <= rCutterhead_HydPress_1_bar AND rCutterhead_HydPress_2_bar >= rCutterhead_HydPress_3_bar) THEN
        rVoted_CP_bar := rCutterhead_HydPress_2_bar;
    ELSE
        rVoted_CP_bar := rCutterhead_HydPress_3_bar;
    END_IF;
ELSIF bHealthy_CP1 AND bHealthy_CP2 THEN
    bDegraded_CP := TRUE;
    rVoted_CP_bar := (rCutterhead_HydPress_1_bar + rCutterhead_HydPress_2_bar) * 0.5;
ELSIF bHealthy_CP2 AND bHealthy_CP3 THEN
    bDegraded_CP := TRUE;
    rVoted_CP_bar := (rCutterhead_HydPress_2_bar + rCutterhead_HydPress_3_bar) * 0.5;
ELSIF bHealthy_CP3 AND bHealthy_CP1 THEN
    bDegraded_CP := TRUE;
    rVoted_CP_bar := (rCutterhead_HydPress_3_bar + rCutterhead_HydPress_1_bar) * 0.5;
ELSIF bHealthy_CP1 THEN
    bDegraded_CP := TRUE;
    rVoted_CP_bar := rCutterhead_HydPress_1_bar;
ELSIF bHealthy_CP2 THEN
    bDegraded_CP := TRUE;
    rVoted_CP_bar := rCutterhead_HydPress_2_bar;
ELSIF bHealthy_CP3 THEN
    bDegraded_CP := TRUE;
    rVoted_CP_bar := rCutterhead_HydPress_3_bar;
ELSE
    rVoted_CP_bar := rVoted_CP_Prev;
    bDegraded_CP := TRUE;
END_IF;
rVoted_CP_Prev := rVoted_CP_bar;

(* ---------------------------------------------------------------------------------------------------- *)
(* SUITE 3: SLURRY CHAMBER COMPRESSED AIR CUSHION PRESSURE (rAirCushion_Press 1, 2, 3)                  *)
(* ---------------------------------------------------------------------------------------------------- *)
bHealthy_AP1 := (rAirCushion_Press_1_bar >= 0.0) AND (rAirCushion_Press_1_bar <= 12.0);
bHealthy_AP2 := (rAirCushion_Press_2_bar >= 0.0) AND (rAirCushion_Press_2_bar <= 12.0);
bHealthy_AP3 := (rAirCushion_Press_3_bar >= 0.0) AND (rAirCushion_Press_3_bar <= 12.0);

IF ABS(rAirCushion_Press_1_bar - rAirCushion_Press_2_bar) > rDiscrepancyTol_AP_bar THEN
    rTimer_AP_12_sec := rTimer_AP_12_sec + tScanCycleTime_s;
ELSE
    rTimer_AP_12_sec := 0.0;
END_IF;

IF ABS(rAirCushion_Press_2_bar - rAirCushion_Press_3_bar) > rDiscrepancyTol_AP_bar THEN
    rTimer_AP_23_sec := rTimer_AP_23_sec + tScanCycleTime_s;
ELSE
    rTimer_AP_23_sec := 0.0;
END_IF;

IF ABS(rAirCushion_Press_3_bar - rAirCushion_Press_1_bar) > rDiscrepancyTol_AP_bar THEN
    rTimer_AP_31_sec := rTimer_AP_31_sec + tScanCycleTime_s;
ELSE
    rTimer_AP_31_sec := 0.0;
END_IF;

bDiscrepancy_AP := (rTimer_AP_12_sec > rDiscrepancyTimeout_sec) OR
                   (rTimer_AP_23_sec > rDiscrepancyTimeout_sec) OR
                   (rTimer_AP_31_sec > rDiscrepancyTimeout_sec);

IF bHealthy_AP1 AND bHealthy_AP2 AND bHealthy_AP3 THEN
    bDegraded_AP := FALSE;
    IF (rAirCushion_Press_1_bar >= rAirCushion_Press_2_bar AND rAirCushion_Press_1_bar <= rAirCushion_Press_3_bar) OR
       (rAirCushion_Press_1_bar <= rAirCushion_Press_2_bar AND rAirCushion_Press_1_bar >= rAirCushion_Press_3_bar) THEN
        rVoted_AP_bar := rAirCushion_Press_1_bar;
    ELSIF (rAirCushion_Press_2_bar >= rAirCushion_Press_1_bar AND rAirCushion_Press_2_bar <= rAirCushion_Press_3_bar) OR
          (rAirCushion_Press_2_bar <= rAirCushion_Press_1_bar AND rAirCushion_Press_2_bar >= rAirCushion_Press_3_bar) THEN
        rVoted_AP_bar := rAirCushion_Press_2_bar;
    ELSE
        rVoted_AP_bar := rAirCushion_Press_3_bar;
    END_IF;
ELSIF bHealthy_AP1 AND bHealthy_AP2 THEN
    bDegraded_AP := TRUE;
    rVoted_AP_bar := (rAirCushion_Press_1_bar + rAirCushion_Press_2_bar) * 0.5;
ELSIF bHealthy_AP2 AND bHealthy_AP3 THEN
    bDegraded_AP := TRUE;
    rVoted_AP_bar := (rAirCushion_Press_2_bar + rAirCushion_Press_3_bar) * 0.5;
ELSIF bHealthy_AP3 AND bHealthy_AP1 THEN
    bDegraded_AP := TRUE;
    rVoted_AP_bar := (rAirCushion_Press_3_bar + rAirCushion_Press_1_bar) * 0.5;
ELSIF bHealthy_AP1 THEN
    bDegraded_AP := TRUE;
    rVoted_AP_bar := rAirCushion_Press_1_bar;
ELSIF bHealthy_AP2 THEN
    bDegraded_AP := TRUE;
    rVoted_AP_bar := rAirCushion_Press_2_bar;
ELSIF bHealthy_AP3 THEN
    bDegraded_AP := TRUE;
    rVoted_AP_bar := rAirCushion_Press_3_bar;
ELSE
    rVoted_AP_bar := rVoted_AP_Prev;
    bDegraded_AP := TRUE;
END_IF;
rVoted_AP_Prev := rVoted_AP_bar;

(* ---------------------------------------------------------------------------------------------------- *)
(* SUITE 4: TAIL SKIN ANNULAR GROUT INJECTION LINE PRESSURE (rGroutLine_Press 1, 2, 3)                  *)
(* ---------------------------------------------------------------------------------------------------- *)
bHealthy_GP1 := (rGroutLine_Press_1_bar >= 0.0) AND (rGroutLine_Press_1_bar <= 25.0);
bHealthy_GP2 := (rGroutLine_Press_2_bar >= 0.0) AND (rGroutLine_Press_2_bar <= 25.0);
bHealthy_GP3 := (rGroutLine_Press_3_bar >= 0.0) AND (rGroutLine_Press_3_bar <= 25.0);

IF ABS(rGroutLine_Press_1_bar - rGroutLine_Press_2_bar) > rDiscrepancyTol_GP_bar THEN
    rTimer_GP_12_sec := rTimer_GP_12_sec + tScanCycleTime_s;
ELSE
    rTimer_GP_12_sec := 0.0;
END_IF;

IF ABS(rGroutLine_Press_2_bar - rGroutLine_Press_3_bar) > rDiscrepancyTol_GP_bar THEN
    rTimer_GP_23_sec := rTimer_GP_23_sec + tScanCycleTime_s;
ELSE
    rTimer_GP_23_sec := 0.0;
END_IF;

IF ABS(rGroutLine_Press_3_bar - rGroutLine_Press_1_bar) > rDiscrepancyTol_GP_bar THEN
    rTimer_GP_31_sec := rTimer_GP_31_sec + tScanCycleTime_s;
ELSE
    rTimer_GP_31_sec := 0.0;
END_IF;

bDiscrepancy_GP := (rTimer_GP_12_sec > rDiscrepancyTimeout_sec) OR
                   (rTimer_GP_23_sec > rDiscrepancyTimeout_sec) OR
                   (rTimer_GP_31_sec > rDiscrepancyTimeout_sec);

IF bHealthy_GP1 AND bHealthy_GP2 AND bHealthy_GP3 THEN
    bDegraded_GP := FALSE;
    IF (rGroutLine_Press_1_bar >= rGroutLine_Press_2_bar AND rGroutLine_Press_1_bar <= rGroutLine_Press_3_bar) OR
       (rGroutLine_Press_1_bar <= rGroutLine_Press_2_bar AND rGroutLine_Press_1_bar >= rGroutLine_Press_3_bar) THEN
        rVoted_GP_bar := rGroutLine_Press_1_bar;
    ELSIF (rGroutLine_Press_2_bar >= rGroutLine_Press_1_bar AND rGroutLine_Press_2_bar <= rGroutLine_Press_3_bar) OR
          (rGroutLine_Press_2_bar <= rGroutLine_Press_1_bar AND rGroutLine_Press_2_bar >= rGroutLine_Press_3_bar) THEN
        rVoted_GP_bar := rGroutLine_Press_2_bar;
    ELSE
        rVoted_GP_bar := rGroutLine_Press_3_bar;
    END_IF;
ELSIF bHealthy_GP1 AND bHealthy_GP2 THEN
    bDegraded_GP := TRUE;
    rVoted_GP_bar := (rGroutLine_Press_1_bar + rGroutLine_Press_2_bar) * 0.5;
ELSIF bHealthy_GP2 AND bHealthy_GP3 THEN
    bDegraded_GP := TRUE;
    rVoted_GP_bar := (rGroutLine_Press_2_bar + rGroutLine_Press_3_bar) * 0.5;
ELSIF bHealthy_GP3 AND bHealthy_GP1 THEN
    bDegraded_GP := TRUE;
    rVoted_GP_bar := (rGroutLine_Press_3_bar + rGroutLine_Press_1_bar) * 0.5;
ELSIF bHealthy_GP1 THEN
    bDegraded_GP := TRUE;
    rVoted_GP_bar := rGroutLine_Press_1_bar;
ELSIF bHealthy_GP2 THEN
    bDegraded_GP := TRUE;
    rVoted_GP_bar := rGroutLine_Press_2_bar;
ELSIF bHealthy_GP3 THEN
    bDegraded_GP := TRUE;
    rVoted_GP_bar := rGroutLine_Press_3_bar;
ELSE
    rVoted_GP_bar := rVoted_GP_Prev;
    bDegraded_GP := TRUE;
END_IF;
rVoted_GP_Prev := rVoted_GP_bar;
""")

    # =========================================================================
    # PHASE 2: GEOTECHNICAL CALCULATIONS & KINEMATICS
    # =========================================================================
    parts.append("""
(* ==================================================================================================== *)
(* PHASE 2: FIRST-PRINCIPLES GEOTECHNICAL, HYDRODYNAMIC & KINEMATIC CALCULATIONS                        *)
(* ==================================================================================================== *)

(* 1. Average Propulsion Stroke & Penetration Velocity Estimation *)
rAvgPropulsionStroke_mm := (rThrustStroke_Q1_Top_mm + rThrustStroke_Q2_Right_mm +
                            rThrustStroke_Q3_Bottom_mm + rThrustStroke_Q4_Left_mm) * 0.25;

IF tScanCycleTime_s > 0.001 THEN
    rPropulsionVelocity_mmmin := ((rAvgPropulsionStroke_mm - rStrokePrevious_mm) / tScanCycleTime_s) * 60.0;
    IF rPropulsionVelocity_mmmin < 0.0 THEN
        rPropulsionVelocity_mmmin := 0.0;
    END_IF;
ELSE
    rPropulsionVelocity_mmmin := 0.0;
END_IF;
rStrokePrevious_mm := rAvgPropulsionStroke_mm;

(* 2. Aggregate Hydraulic Advance Thrust Force F_thrust [kN] across 24 Cylinders *)
(* Total Area per Quadrant = 6 cylinders * (pi/4 * d_bore^2). Total effective hydraulic area ~ 0.58 m2 *)
rEst_TotalThrust_kN := (rThrustPress_Q1_Top_bar + rThrustPress_Q2_Right_bar +
                        rThrustPress_Q3_Bottom_bar + rThrustPress_Q4_Left_bar) * 145.0;

(* 3. Specific Mechanical Energy (SE) in [kJ/m3] *)
(* SE = (F_thrust / A_face) + (2 * pi * Torque * RPM) / (A_face * PR) *)
IF (rPropulsionVelocity_mmmin > 0.5) AND (rTBM_FaceArea_m2 > 10.0) THEN
    rEst_SpecificEnergy_kJm3 := (rEst_TotalThrust_kN / rTBM_FaceArea_m2) * 1000.0 +
                                (6.283185 * rCutterhead_Torque_kNm * rCutterhead_Speed_RPM * 60.0) /
                                (rTBM_FaceArea_m2 * (rPropulsionVelocity_mmmin * 0.001));
ELSE
    rEst_SpecificEnergy_kJm3 := 8500.0; (* Baseline reference specific energy for riverbed strata *)
END_IF;

(* 4. Geotechnical Indices: Field Penetration Index (FPI) and Torque Penetration Index (TPI) *)
IF rPropulsionVelocity_mmmin > 0.2 THEN
    rCalc_FieldPenetrationIndex_kNmm := rEst_TotalThrust_kN / rPropulsionVelocity_mmmin;
    rCalc_TorquePenetrationIndex_kNm_mm := rCutterhead_Torque_kNm / rPropulsionVelocity_mmmin;
ELSE
    rCalc_FieldPenetrationIndex_kNmm := 0.0;
    rCalc_TorquePenetrationIndex_kNm_mm := 0.0;
END_IF;

(* 5. Mass Balance Over/Under Excavation Monitoring *)
(* Theoretical Excavation Volume Rate: V_dot = A_face * (PR / 1000) [m3/min] *)
rTheoMuckVolumePerMin_m3min := rTBM_FaceArea_m2 * (rPropulsionVelocity_mmmin * 0.001);
rTheoMuckMassRate_tph := rTheoMuckVolumePerMin_m3min * 60.0 * rSoil_NominalDensity_tm3;
rActualMuckMassRate_tph := rMuckDischarge_MassRate_tph;

IF rTheoMuckMassRate_tph > 10.0 THEN
    rCalc_MuckMassDiscrepancy_pct := ((rActualMuckMassRate_tph - rTheoMuckMassRate_tph) / rTheoMuckMassRate_tph) * 100.0;
ELSE
    rCalc_MuckMassDiscrepancy_pct := 0.0;
END_IF;

(* 6. Annular Tail Void Grout Fill Balance *)
(* Theoretical Infill Grout Volume Rate: Q_grout = AnnularVoidPerMeter * PR [m3/min] -> [L/min] *)
rTheoGroutFlow_Lmin := (rTBM_AnnularVoidVolPerM_m3 * (rPropulsionVelocity_mmmin * 0.001)) * 1000.0 * (rSet_GroutVolumeRatio_pct * 0.01);
rActualGroutFlow_Lmin := rGroutFlow_CompA_Lmin + rGroutFlow_CompB_Lmin;

IF rTheoGroutFlow_Lmin > 5.0 THEN
    rCalc_AnnularGroutFillRatio_pct := (rActualGroutFlow_Lmin / rTheoGroutFlow_Lmin) * 100.0;
ELSE
    rCalc_AnnularGroutFillRatio_pct := 100.0;
END_IF;

(* 7. Articulation Differential Steering Trim Allocation *)
rPitchError_mrad := rSet_ShieldPitch_mrad - rShield_Pitch_mrad;
rYawError_mrad := rSet_ShieldYaw_mrad - rShield_Yaw_mrad;

(* Differential Flow Bias Allocation Across 4 Quadrants: Top/Bottom governs Pitch, Right/Left governs Yaw *)
rTrim_Q1_Top_pct := rPitchError_mrad * rKp_Steering_Pitch;
rTrim_Q3_Bottom_pct := -rPitchError_mrad * rKp_Steering_Pitch;
rTrim_Q2_Right_pct := rYawError_mrad * rKp_Steering_Yaw;
rTrim_Q4_Left_pct := -rYawError_mrad * rKp_Steering_Yaw;

(* Saturate Trims to +/- 15.0% *)
IF rTrim_Q1_Top_pct > 15.0 THEN rTrim_Q1_Top_pct := 15.0; ELSIF rTrim_Q1_Top_pct < -15.0 THEN rTrim_Q1_Top_pct := -15.0; END_IF;
IF rTrim_Q2_Right_pct > 15.0 THEN rTrim_Q2_Right_pct := 15.0; ELSIF rTrim_Q2_Right_pct < -15.0 THEN rTrim_Q2_Right_pct := -15.0; END_IF;
IF rTrim_Q3_Bottom_pct > 15.0 THEN rTrim_Q3_Bottom_pct := 15.0; ELSIF rTrim_Q3_Bottom_pct < -15.0 THEN rTrim_Q3_Bottom_pct := -15.0; END_IF;
IF rTrim_Q4_Left_pct > 15.0 THEN rTrim_Q4_Left_pct := 15.0; ELSIF rTrim_Q4_Left_pct < -15.0 THEN rTrim_Q4_Left_pct := -15.0; END_IF;

(* Pass Kinematic Angles to Outputs *)
rEst_ShieldPitch_mrad := rShield_Pitch_mrad;
rEst_ShieldYaw_mrad := rShield_Yaw_mrad;
rEst_AirCushionPress_bar := rVoted_AP_bar;
rEst_GroutPressure_bar := rVoted_GP_bar;
rEst_GroutVolumeRatio_pct := rCalc_AnnularGroutFillRatio_pct;
""")

    # =========================================================================
    # PHASE 3: DISCRETE STATE-SPACE PROPAGATION & LUENBERGER OBSERVER
    # =========================================================================
    parts.append("""
(* ==================================================================================================== *)
(* PHASE 3: CYBER-PHYSICAL DISCRETE STATE-SPACE PROPAGATION & LUENBERGER OBSERVER                       *)
(* Innovation: x_hat[k] = x_pred[k] + matL * (y_meas[k] - y_est[k])                                     *)
(* Propagation: x_pred[k+1] = matA * x_hat[k] + matB * u_ctrl[k]                                       *)
(* ==================================================================================================== *)

(* 1. Assemble Sensor Observation Vector y_meas from 2oo3 Transmitters *)
y_meas[1] := rVoted_EP_bar;                     (* Bulkhead Earth Pressure [bar] *)
y_meas[2] := rPropulsionVelocity_mmmin;          (* Measured Advance Rate [mm/min] *)
y_meas[3] := rEst_SpecificEnergy_kJm3;          (* Excavation Specific Energy [kJ/m3] *)
y_meas[4] := rEst_TotalThrust_kN;               (* Advance Propulsion Thrust [kN] *)
y_meas[5] := rActualMuckMassRate_tph;           (* Belt Scale Muck Extraction [t/h] *)
y_meas[6] := rAirCushion_Level_m;               (* Compressed Air Bubble Level [m] *)

(* 2. Compute Projected Output y_est[k] = matC * x_pred[k] *)
FOR iIter := 1 TO 6 DO
    rTempDot := 0.0;
    FOR jIter := 1 TO 6 DO
        rTempDot := rTempDot + matC[iIter, jIter] * x_pred[jIter];
    END_FOR;
    y_est[iIter] := rTempDot;
    e_innov[iIter] := y_meas[iIter] - y_est[iIter];
END_FOR;

(* 3. Luenberger Observer Innovation Correction: x_hat[k] = x_pred[k] + matL * e_innov *)
FOR iIter := 1 TO 6 DO
    rTempDot := 0.0;
    FOR jIter := 1 TO 6 DO
        rTempDot := rTempDot + matL[iIter, jIter] * e_innov[jIter];
    END_FOR;
    x_hat[iIter] := x_pred[iIter] + rTempDot;
END_FOR;

(* Physical Plausibility Guard Bounds on Estimated States *)
IF x_hat[1] < 0.0 THEN x_hat[1] := 0.0; ELSIF x_hat[1] > 12.0 THEN x_hat[1] := 12.0; END_IF;
IF x_hat[2] < 0.0 THEN x_hat[2] := 0.0; ELSIF x_hat[2] > 120.0 THEN x_hat[2] := 120.0; END_IF;
IF x_hat[3] < 1000.0 THEN x_hat[3] := 1000.0; ELSIF x_hat[3] > 60000.0 THEN x_hat[3] := 60000.0; END_IF;
IF x_hat[4] < 0.0 THEN x_hat[4] := 0.0; ELSIF x_hat[4] > 160000.0 THEN x_hat[4] := 160000.0; END_IF;
IF x_hat[5] < 0.0 THEN x_hat[5] := 0.0; ELSIF x_hat[5] > 2500.0 THEN x_hat[5] := 2500.0; END_IF;
IF x_hat[6] < 0.0 THEN x_hat[6] := 0.0; ELSIF x_hat[6] > 10.0 THEN x_hat[6] := 10.0; END_IF;

(* Assign Filtered Estimates to Function Block Outputs *)
rEst_FacePressure_bar := x_hat[1];
rEst_PenetrationRate_mmmin := x_hat[2];
rEst_MuckExtractionRate_tph := x_hat[5];
rEst_AirBubbleLevel_m := x_hat[6];

(* 4. State Propagation x_pred[k+1] = matA * x_hat[k] + matB * u_ctrl[k] *)
FOR iIter := 1 TO 6 DO
    rTempDot := 0.0;
    FOR jIter := 1 TO 6 DO
        rTempDot := rTempDot + matA[iIter, jIter] * x_hat[jIter] + matB[iIter, jIter] * u_ctrl[jIter];
    END_FOR;
    x_pred[iIter] := rTempDot;
END_FOR;
""")

    # =========================================================================
    # PHASE 4: RECEDING-HORIZON MPC VIA 10 UNROLLED PGD ITERATIONS
    # =========================================================================
    parts.append("""
(* ==================================================================================================== *)
(* PHASE 4: RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) VIA 10 UNROLLED PGD ITERATIONS             *)
(* Receding Horizon Np = 5 steps, Optimization Vector Dim = 6 (Thrust, Cutter, Screw, Air, Slurry, Grout)*)
(* Projected Gradient Descent: u_new = Clip(u_old - alpha * grad_J, u_min, u_max)                       *)
(* ==================================================================================================== *)

(* 1. Set Reference Trajectory Vector x_ref from Supervisory Operator Setpoints *)
x_ref[1] := rSet_FacePressure_bar;              (* Face Pressure Target [bar] *)
x_ref[2] := rSet_AdvanceRate_mmmin;             (* Advance Speed Target [mm/min] *)
x_ref[3] := 8500.0;                             (* Baseline Ground Specific Energy [kJ/m3] *)
x_ref[4] := 75000.0;                            (* Nominal Mid-Range Thrust Force [kN] *)
x_ref[5] := rTheoMuckMassRate_tph;              (* Target Mass Flow Balancing Face Volume [t/h] *)
x_ref[6] := rSet_AirBubbleLevel_m;              (* Slurry Bubble Level Setpoint [m] *)

(* Initialize Control Horizon with Previous Control Profile *)
FOR kIter := 1 TO 5 DO
    FOR iIter := 1 TO 6 DO
        u_horizon[kIter, iIter] := u_ctrl[iIter];
    END_FOR;
END_FOR;

(* 2. Unrolled Projected Gradient Descent (10 Iterations) *)
FOR iIter := 1 TO 10 DO
    (* Step A: Forward State Rollout along Horizon *)
    FOR jIter := 1 TO 6 DO
        x_rollout[1, jIter] := x_hat[jIter];
    END_FOR;

    FOR kIter := 1 TO 4 DO
        FOR jIter := 1 TO 6 DO
            rTempDot := 0.0;
            FOR iIter := 1 TO 6 DO
                rTempDot := rTempDot + matA[jIter, iIter] * x_rollout[kIter, iIter] +
                            matB[jIter, iIter] * u_horizon[kIter, iIter];
            END_FOR;
            x_rollout[kIter + 1, jIter] := rTempDot;
        END_FOR;
    END_FOR;

    (* Step B: Compute Quadratic Stage Cost Metric J *)
    rCost_J := 0.0;
    FOR kIter := 1 TO 5 DO
        FOR jIter := 1 TO 6 DO
            IF kIter < 5 THEN
                rCost_J := rCost_J + matQ[jIter, jIter] * (x_rollout[kIter, jIter] - x_ref[jIter]) * (x_rollout[kIter, jIter] - x_ref[jIter]) +
                                     matR[jIter, jIter] * u_horizon[kIter, jIter] * u_horizon[kIter, jIter];
            ELSE
                rCost_J := rCost_J + matP[jIter, jIter] * (x_rollout[5, jIter] - x_ref[jIter]) * (x_rollout[5, jIter] - x_ref[jIter]);
            END_IF;
        END_FOR;
    END_FOR;

    (* Step C: Compute Projected Gradient of Cost Function with respect to Step 1 Actuators *)
    (* grad_J = matB^T * matQ * (x_rollout[2] - x_ref) + matR * u_horizon[1] *)
    FOR jIter := 1 TO 6 DO
        rTempDot := 0.0;
        FOR kIter := 1 TO 6 DO
            rTempDot := rTempDot + matB[kIter, jIter] * matQ[kIter, kIter] * (x_rollout[2, kIter] - x_ref[kIter]);
        END_FOR;
        grad_J[jIter] := rTempDot + matR[jIter, jIter] * u_horizon[1, jIter];
    END_FOR;

    (* Step D: Projected Gradient Descent Step with Actuator Box Limits & Slew Rate Saturation *)
    FOR jIter := 1 TO 6 DO
        rTempClip := u_horizon[1, jIter] - rAlpha_pgd * grad_J[jIter];

        (* Apply Slew Rate Clamping *)
        rDelta_u := rTempClip - u_prev[jIter];
        IF rDelta_u > du_max[jIter] THEN
            rTempClip := u_prev[jIter] + du_max[jIter];
        ELSIF rDelta_u < -du_max[jIter] THEN
            rTempClip := u_prev[jIter] - du_max[jIter];
        END_IF;

        (* Apply Box Constraint Saturation *)
        IF rTempClip > u_max[jIter] THEN
            rTempClip := u_max[jIter];
        ELSIF rTempClip < u_min[jIter] THEN
            rTempClip := u_min[jIter];
        END_IF;

        u_horizon[1, jIter] := rTempClip;
    END_FOR;
END_FOR;

rMpc_QuadraticCostMetric := rCost_J;
""")

    # =========================================================================
    # PHASE 5: DETERMINISTIC 14-STAGE FINITE STATE MACHINE (FSM)
    # =========================================================================
    parts.append("""
(* ==================================================================================================== *)
(* PHASE 5: DETERMINISTIC 14-STAGE PRODUCTION FINITE STATE MACHINE (FSM)                                *)
(* Architecture:                                                                                        *)
(*   0:  STATE_IDLE                                                                                     *)
(*   1:  STATE_CHAMBER_PRESSURIZATION_AIR_CUSHION_INIT                                                  *)
(*   2:  STATE_CUTTERHEAD_ROTATION_BREAKAWAY_TORQUE                                                     *)
(*   3:  STATE_THRUST_CYLINDER_STROKE_ENGAGE                                                            *)
(*   4:  STATE_FACE_PRESSURE_EQUILIBRIUM_LOCK                                                           *)
(*   5:  STATE_CLOSED_LOOP_EXCAVATION_ADVANCE_RUN                                                       *)
(*   6:  STATE_ANNULAR_GROUT_SYNCHRONOUS_INJECTION                                                      *)
(*   7:  STATE_GEOLOGICAL_OBSTACLE_HARD_ROCK_SURGE_DECEL                                                *)
(*   8:  STATE_STROKE_LIMIT_DECELERATION_HOLD                                                           *)
(*   9:  STATE_CUTTERHEAD_RETRACT_AND_PRESSURE_MAINTAIN                                                 *)
(*   10: STATE_TAIL_CYLINDER_RETRACT_FOR_SEGMENT_RING                                                   *)
(*   11: STATE_PRECAST_CONCRETE_SEGMENT_ERECTOR_BUILD                                                   *)
(*   12: STATE_CHAMBER_BENTONITE_FLUSH_STANDBY                                                          *)
(*   13: STATE_EMERGENCY_WATER_INGRESS_FACE_COLLAPSE_TRIP                                               *)
(* ==================================================================================================== *)

(* Manage State Dwell Timer & State Entry Transitions *)
IF eState <> eState_Prev THEN
    rStateTimer_sec := 0.0;
    bStateFirstScan := TRUE;
    eState_Prev := eState;
ELSE
    rStateTimer_sec := rStateTimer_sec + tScanCycleTime_s;
    bStateFirstScan := FALSE;
END_IF;

(* Master Safety Hardwired E-Stop & Catastrophic Water Ingress Trip Priority *)
IF (NOT bEmergencyStop) OR bWaterIngressSensor_Bulkhead OR bEmergencyTripLatched THEN
    eState := 13; (* Immediate Jump to EMERGENCY TRIP *)
END_IF;

CASE eState OF
    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 0: STATE_IDLE                                                                              *)
    (* ------------------------------------------------------------------------------------------------ *)
    0:
        bSystemRunning := FALSE;
        bAdvancePermissive := FALSE;

        (* Reset All Modulated Actuator Outputs to Zero / Safe Resting *)
        rThrustValve_Q1_Top_pct := 0.0;
        rThrustValve_Q2_Right_pct := 0.0;
        rThrustValve_Q3_Bottom_pct := 0.0;
        rThrustValve_Q4_Left_pct := 0.0;
        rThrustAdvanceRate_Cmd_mmmin := 0.0;
        rCutterhead_Speed_Cmd_RPM := 0.0;
        rCutterhead_TorqueLimit_Cmd_kNm := 5000.0;
        rScrewConveyor_Speed_Cmd_RPM := 0.0;
        rScrewGate_Pos_Cmd_pct := 0.0;
        rAirSupply_Valve_Cmd_pct := 0.0;
        rAirBleed_Valve_Cmd_pct := 0.0;
        rSlurryFeedPump_Cmd_pct := 0.0;
        rSlurryDischargePump_Cmd_pct := 0.0;
        rGroutPumpA_Cmd_pct := 0.0;
        rGroutPumpB_Cmd_pct := 0.0;
        bGroutPort_Open_1 := FALSE;
        bGroutPort_Open_2 := FALSE;
        bGroutPort_Open_3 := FALSE;
        bGroutPort_Open_4 := FALSE;
        bGroutPort_Open_5 := FALSE;
        bGroutPort_Open_6 := FALSE;
        bGroutPort_Open_7 := FALSE;
        bGroutPort_Open_8 := FALSE;
        rConditioner_Valve_Cmd_pct := 0.0;
        bEmergencySlurryGate_Close := FALSE;
        bCompressedAirSupply_Trip := FALSE;

        (* Transition to Chamber Pressurization if Master Permissives are Satisfied *)
        IF bSystemEnable AND bAutoExcavationMode AND (NOT bTripInterlockActive) AND bSegmentErector_Parked THEN
            eState := 1;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 1: STATE_CHAMBER_PRESSURIZATION_AIR_CUSHION_INIT                                           *)
    (* ------------------------------------------------------------------------------------------------ *)
    1:
        bSystemRunning := TRUE;
        bAdvancePermissive := FALSE;

        (* Ramp Up Slurry Circulation Pumps & Regulate Air Cushion Bubble to Equilibrium *)
        rSlurryFeedPump_Cmd_pct := 35.0;
        rSlurryDischargePump_Cmd_pct := 30.0;

        IF rEst_FacePressure_bar < (rSet_FacePressure_bar - 0.20) THEN
            rAirSupply_Valve_Cmd_pct := 45.0;
            rAirBleed_Valve_Cmd_pct := 0.0;
        ELSIF rEst_FacePressure_bar > (rSet_FacePressure_bar + 0.20) THEN
            rAirSupply_Valve_Cmd_pct := 0.0;
            rAirBleed_Valve_Cmd_pct := 35.0;
        ELSE
            (* Stable Air Cushion Equilibrium Established *)
            rAirSupply_Valve_Cmd_pct := 12.0;
            rAirBleed_Valve_Cmd_pct := 0.0;
        END_IF;

        (* Proceed to Cutterhead Breakaway when Air Cushion & Slurry Head Reach SP *)
        IF (ABS(rEst_FacePressure_bar - rSet_FacePressure_bar) <= 0.25) AND (rStateTimer_sec > 4.0) THEN
            eState := 2;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 2: STATE_CUTTERHEAD_ROTATION_BREAKAWAY_TORQUE                                              *)
    (* ------------------------------------------------------------------------------------------------ *)
    2:
        bSystemRunning := TRUE;
        bAdvancePermissive := FALSE;

        (* Ramp Cutterhead Drive Motor Speed Slowly to Overcome Soil Friction Breakaway *)
        bCutterhead_Direction_CW := TRUE;
        rCutterhead_TorqueLimit_Cmd_kNm := 21000.0; (* Full Breakaway Torque Limit Available *)

        IF rStateTimer_sec < 5.0 THEN
            rCutterhead_Speed_Cmd_RPM := (rStateTimer_sec / 5.0) * 1.20;
        ELSE
            rCutterhead_Speed_Cmd_RPM := 1.20;
        END_IF;

        (* Maintain Face Pressure During Breakaway *)
        rAirSupply_Valve_Cmd_pct := 15.0;
        rSlurryFeedPump_Cmd_pct := 40.0;

        (* Verify Rotation Established without Immediate Stall *)
        IF (rCutterhead_Speed_RPM >= 0.80) AND (rCutterhead_Torque_kNm < 19500.0) AND (rStateTimer_sec > 6.0) THEN
            eState := 3;
        ELSIF (rCutterhead_Torque_kNm >= 21500.0) AND (rStateTimer_sec > 4.0) THEN
            (* Cutterhead Stall: Jump to Obstacle Handling *)
            eState := 7;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 3: STATE_THRUST_CYLINDER_STROKE_ENGAGE                                                     *)
    (* ------------------------------------------------------------------------------------------------ *)
    3:
        bSystemRunning := TRUE;
        bAdvancePermissive := FALSE;

        (* Pre-Stress Hydraulic Propulsion Cylinders against Tunnel Precast Lining *)
        rThrustAdvanceRate_Cmd_mmmin := 5.0; (* Slow Approach Velocity *)
        rThrustValve_Q1_Top_pct := 12.0;
        rThrustValve_Q2_Right_pct := 12.0;
        rThrustValve_Q3_Bottom_pct := 12.0;
        rThrustValve_Q4_Left_pct := 12.0;

        (* Spin Screw Conveyor at Idling Purge Speed to Prevent Tail Packing *)
        rScrewConveyor_Speed_Cmd_RPM := 2.5;
        rScrewGate_Pos_Cmd_pct := 15.0;

        (* Verify Thrust Force Buildup Indicates Solid Contact with Substrate *)
        IF (rEst_TotalThrust_kN >= 25000.0) AND (rStateTimer_sec > 3.0) THEN
            eState := 4;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 4: STATE_FACE_PRESSURE_EQUILIBRIUM_LOCK                                                    *)
    (* ------------------------------------------------------------------------------------------------ *)
    4:
        bSystemRunning := TRUE;
        bAdvancePermissive := TRUE;

        (* Balance Muck Extraction Screw Speed vs Chamber Pressure Inflow *)
        rCutterhead_Speed_Cmd_RPM := rSet_CutterRPM * 0.65;
        rThrustAdvanceRate_Cmd_mmmin := 10.0;

        IF rEst_FacePressure_bar < rSet_FacePressure_bar THEN
            rScrewConveyor_Speed_Cmd_RPM := 2.0;
            rScrewGate_Pos_Cmd_pct := 10.0;
            rConditioner_Valve_Cmd_pct := 25.0;
        ELSE
            rScrewConveyor_Speed_Cmd_RPM := 4.5;
            rScrewGate_Pos_Cmd_pct := 25.0;
        END_IF;

        (* Once Pressure Is Locked Within +/- 0.15 bar, Enter Full Closed-Loop Excavation *)
        IF (ABS(rEst_FacePressure_bar - rSet_FacePressure_bar) <= 0.15) AND (rStateTimer_sec > 4.0) THEN
            eState := 5;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 5: STATE_CLOSED_LOOP_EXCAVATION_ADVANCE_RUN                                                *)
    (* ------------------------------------------------------------------------------------------------ *)
    5:
        bSystemRunning := TRUE;
        bAdvancePermissive := TRUE;

        (* Engage Full Model Predictive Control (MPC) Optimized Vector with Articulation Steering *)
        rCutterhead_Speed_Cmd_RPM := u_horizon[1, 2];
        rScrewConveyor_Speed_Cmd_RPM := u_horizon[1, 3];
        rAirSupply_Valve_Cmd_pct := u_horizon[1, 4];
        rSlurryFeedPump_Cmd_pct := u_horizon[1, 5];
        rGroutPumpA_Cmd_pct := u_horizon[1, 6];
        rGroutPumpB_Cmd_pct := u_horizon[1, 6] * 0.10; (* Accelerator 10:1 Ratio *)

        (* Modulate 4 Quadrant Flow Valves with Steering Trim Allocation *)
        rThrustValve_Q1_Top_pct := u_horizon[1, 1] + rTrim_Q1_Top_pct;
        rThrustValve_Q2_Right_pct := u_horizon[1, 1] + rTrim_Q2_Right_pct;
        rThrustValve_Q3_Bottom_pct := u_horizon[1, 1] + rTrim_Q3_Bottom_pct;
        rThrustValve_Q4_Left_pct := u_horizon[1, 1] + rTrim_Q4_Left_pct;
        rThrustAdvanceRate_Cmd_mmmin := rSet_AdvanceRate_mmmin;

        (* Continuous Foam/Polymer Conditioning Proportionate to Advance Rate *)
        rConditioner_Valve_Cmd_pct := 15.0 + (rPropulsionVelocity_mmmin / 60.0) * 35.0;
        rScrewGate_Pos_Cmd_pct := 45.0;

        (* Transitions: Synchronous Grouting Activation *)
        IF rPropulsionVelocity_mmmin >= 15.0 THEN
            eState := 6;
        END_IF;

        (* Transitions: Hard Rock / Granite Boulder Encounter *)
        IF (rCutterhead_Torque_kNm >= 19500.0) OR (rEst_SpecificEnergy_kJm3 >= 28000.0) THEN
            eState := 7;
        END_IF;

        (* Transitions: Cylinder Stroke Reaching Ring Extension Limit *)
        IF rAvgPropulsionStroke_mm >= rStrokeDecelThreshold_mm THEN
            eState := 8;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 6: STATE_ANNULAR_GROUT_SYNCHRONOUS_INJECTION                                               *)
    (* ------------------------------------------------------------------------------------------------ *)
    6:
        bSystemRunning := TRUE;
        bAdvancePermissive := TRUE;

        (* Full Excavation MPC Running in Coordinated Conjunction with Bi-Component Tail Injection *)
        rCutterhead_Speed_Cmd_RPM := u_horizon[1, 2];
        rScrewConveyor_Speed_Cmd_RPM := u_horizon[1, 3];
        rThrustAdvanceRate_Cmd_mmmin := rSet_AdvanceRate_mmmin;

        rThrustValve_Q1_Top_pct := u_horizon[1, 1] + rTrim_Q1_Top_pct;
        rThrustValve_Q2_Right_pct := u_horizon[1, 1] + rTrim_Q2_Right_pct;
        rThrustValve_Q3_Bottom_pct := u_horizon[1, 1] + rTrim_Q3_Bottom_pct;
        rThrustValve_Q4_Left_pct := u_horizon[1, 1] + rTrim_Q4_Left_pct;

        (* Tail Skin Grout Port Sequencing: Distribute Infill across 8 Circumferential Ports *)
        bGroutPort_Open_1 := TRUE;
        bGroutPort_Open_2 := TRUE;
        bGroutPort_Open_3 := TRUE;
        bGroutPort_Open_4 := TRUE;
        bGroutPort_Open_5 := TRUE;
        bGroutPort_Open_6 := TRUE;
        bGroutPort_Open_7 := TRUE;
        bGroutPort_Open_8 := TRUE;

        (* Synchronous Volume Tracking Loop: Modulate Grout Pump Speed *)
        IF rVoted_GP_bar < rSet_GroutPressure_bar THEN
            rGroutPumpA_Cmd_pct := (rTheoGroutFlow_Lmin / 120.0) * 100.0 + 8.5;
            rGroutPumpB_Cmd_pct := rGroutPumpA_Cmd_pct * 0.10;
        ELSE
            rGroutPumpA_Cmd_pct := (rTheoGroutFlow_Lmin / 120.0) * 100.0 - 5.0;
            rGroutPumpB_Cmd_pct := rGroutPumpA_Cmd_pct * 0.10;
        END_IF;

        (* Transitions *)
        IF (rCutterhead_Torque_kNm >= 19500.0) OR (rEst_SpecificEnergy_kJm3 >= 28000.0) THEN
            eState := 7;
        ELSIF rAvgPropulsionStroke_mm >= rStrokeDecelThreshold_mm THEN
            eState := 8;
        ELSIF rPropulsionVelocity_mmmin < 8.0 THEN
            (* Slowdown: Drop back to Standard Closed-Loop Advance *)
            eState := 5;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 7: STATE_GEOLOGICAL_OBSTACLE_HARD_ROCK_SURGE_DECEL                                         *)
    (* ------------------------------------------------------------------------------------------------ *)
    7:
        bSystemRunning := TRUE;
        bAdvancePermissive := TRUE;
        bHardRockDetected := TRUE;

        (* Decelerate Advance Immediately to Relieve High Tool Contact Stresses *)
        rThrustAdvanceRate_Cmd_mmmin := 8.0;
        rThrustValve_Q1_Top_pct := 15.0;
        rThrustValve_Q2_Right_pct := 15.0;
        rThrustValve_Q3_Bottom_pct := 15.0;
        rThrustValve_Q4_Left_pct := 15.0;

        (* Reduce Cutterhead RPM to Increase Chipping Depth and Reduce Tool Impact Shatter *)
        rCutterhead_Speed_Cmd_RPM := 1.10;
        rCutterhead_TorqueLimit_Cmd_kNm := 22000.0;

        (* Increase Conditioning Foam to Flush Fractured Chips *)
        rConditioner_Valve_Cmd_pct := 65.0;
        rScrewConveyor_Speed_Cmd_RPM := 3.5;

        (* Check if Boulder Chipped Away or Torque Dissipated *)
        IF (rCutterhead_Torque_kNm < 16500.0) AND (rEst_SpecificEnergy_kJm3 < 18000.0) AND (rStateTimer_sec > 8.0) THEN
            bHardRockDetected := FALSE;
            eState := 5; (* Return to Normal Advance *)
        ELSIF rAvgPropulsionStroke_mm >= rStrokeDecelThreshold_mm THEN
            eState := 8;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 8: STATE_STROKE_LIMIT_DECELERATION_HOLD                                                    *)
    (* ------------------------------------------------------------------------------------------------ *)
    8:
        bSystemRunning := TRUE;
        bAdvancePermissive := FALSE;
        bStrokeLimitReached := TRUE;

        (* Decelerate Propulsion Cylinders Smoothly Down to Zero Stroke Extension *)
        rThrustAdvanceRate_Cmd_mmmin := 0.0;
        rThrustValve_Q1_Top_pct := 0.0;
        rThrustValve_Q2_Right_pct := 0.0;
        rThrustValve_Q3_Bottom_pct := 0.0;
        rThrustValve_Q4_Left_pct := 0.0;

        (* Close Tail Grout Ports to Prevent Back-Bleed into Tail Seals *)
        bGroutPort_Open_1 := FALSE;
        bGroutPort_Open_2 := FALSE;
        bGroutPort_Open_3 := FALSE;
        bGroutPort_Open_4 := FALSE;
        bGroutPort_Open_5 := FALSE;
        bGroutPort_Open_6 := FALSE;
        bGroutPort_Open_7 := FALSE;
        bGroutPort_Open_8 := FALSE;
        rGroutPumpA_Cmd_pct := 0.0;
        rGroutPumpB_Cmd_pct := 0.0;

        (* Slow Cutterhead and Clear Chamber Muck *)
        rCutterhead_Speed_Cmd_RPM := 0.80;
        rScrewConveyor_Speed_Cmd_RPM := 2.0;

        IF rStateTimer_sec > 5.0 THEN
            eState := 9;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 9: STATE_CUTTERHEAD_RETRACT_AND_PRESSURE_MAINTAIN                                          *)
    (* ------------------------------------------------------------------------------------------------ *)
    9:
        bSystemRunning := TRUE;
        bAdvancePermissive := FALSE;

        (* Stop Cutterhead Rotation Completely *)
        rCutterhead_Speed_Cmd_RPM := 0.0;
        rScrewConveyor_Speed_Cmd_RPM := 0.0;
        rScrewGate_Pos_Cmd_pct := 0.0; (* Tight Hydraulic Seal *)

        (* Maintain Submerged Air Cushion Equilibrium During Stationary Period *)
        IF rEst_FacePressure_bar < rSet_FacePressure_bar THEN
            rAirSupply_Valve_Cmd_pct := 22.0;
            rAirBleed_Valve_Cmd_pct := 0.0;
        ELSE
            rAirSupply_Valve_Cmd_pct := 0.0;
            rAirBleed_Valve_Cmd_pct := 15.0;
        END_IF;

        IF rStateTimer_sec > 4.0 THEN
            eState := 10;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 10: STATE_TAIL_CYLINDER_RETRACT_FOR_SEGMENT_RING                                           *)
    (* ------------------------------------------------------------------------------------------------ *)
    10:
        bSystemRunning := TRUE;
        bAdvancePermissive := FALSE;

        (* Sequential Retraction of Propulsion Cylinder Groups to Open Space for Ring Segment Erector *)
        (* Maintain Holding Pressure on Opposite Quadrants to Prevent Machine Drift *)
        rThrustValve_Q1_Top_pct := 0.0;
        rThrustValve_Q2_Right_pct := 0.0;
        rThrustValve_Q3_Bottom_pct := 0.0;
        rThrustValve_Q4_Left_pct := 0.0;

        IF rStateTimer_sec > 6.0 THEN
            eState := 11;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 11: STATE_PRECAST_CONCRETE_SEGMENT_ERECTOR_BUILD                                           *)
    (* ------------------------------------------------------------------------------------------------ *)
    11:
        bSystemRunning := FALSE;
        bAdvancePermissive := FALSE;

        (* Mechanical Segment Erector Active: All Propulsion & Cutterhead Drives Hard-Interlocked *)
        rCutterhead_Speed_Cmd_RPM := 0.0;
        rThrustAdvanceRate_Cmd_mmmin := 0.0;
        rScrewConveyor_Speed_Cmd_RPM := 0.0;

        (* Passive Face Pressure Maintenance via Slurry Feed Air Cushion Bubble *)
        IF rEst_FacePressure_bar < (rSet_FacePressure_bar - 0.15) THEN
            rAirSupply_Valve_Cmd_pct := 18.0;
        ELSE
            rAirSupply_Valve_Cmd_pct := 0.0;
        END_IF;

        (* Wait for Operator & Robot Ring Assembly Confirmation *)
        IF bSegmentErector_RingComplete AND bSegmentErector_Parked THEN
            eState := 12;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 12: STATE_CHAMBER_BENTONITE_FLUSH_STANDBY                                                  *)
    (* ------------------------------------------------------------------------------------------------ *)
    12:
        bSystemRunning := TRUE;
        bAdvancePermissive := FALSE;

        (* Agitate Slurry Chamber to Prevent Silt Sedimentation Before Next Advance *)
        rSlurryFeedPump_Cmd_pct := 45.0;
        rSlurryDischargePump_Cmd_pct := 42.0;

        IF rStateTimer_sec > 5.0 THEN
            bStrokeLimitReached := FALSE;
            eState := 0; (* Cycle Complete: Return to Idle / Standby for Next Advance Stroke *)
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 13: STATE_EMERGENCY_WATER_INGRESS_FACE_COLLAPSE_TRIP                                       *)
    (* ------------------------------------------------------------------------------------------------ *)
    13:
        bSystemRunning := FALSE;
        bAdvancePermissive := FALSE;
        bTripInterlockActive := TRUE;
        bEmergencyTripLatched := TRUE;

        (* Immediate Total Plant Isolation: Zero All Propulsion, Cutterhead, Screw Conveyor & Grout *)
        rThrustValve_Q1_Top_pct := 0.0;
        rThrustValve_Q2_Right_pct := 0.0;
        rThrustValve_Q3_Bottom_pct := 0.0;
        rThrustValve_Q4_Left_pct := 0.0;
        rThrustAdvanceRate_Cmd_mmmin := 0.0;
        rCutterhead_Speed_Cmd_RPM := 0.0;
        rScrewConveyor_Speed_Cmd_RPM := 0.0;
        rScrewGate_Pos_Cmd_pct := 0.0; (* Slam Shut Mechanical Guillotine Gate *)

        (* Slam Shut Emergency Bulkhead Gate & Isolate Submerged Slurry Lines *)
        bEmergencySlurryGate_Close := TRUE;
        bCompressedAirSupply_Trip := TRUE;

        (* Isolate Tail Grout Ports *)
        bGroutPort_Open_1 := FALSE;
        bGroutPort_Open_2 := FALSE;
        bGroutPort_Open_3 := FALSE;
        bGroutPort_Open_4 := FALSE;
        bGroutPort_Open_5 := FALSE;
        bGroutPort_Open_6 := FALSE;
        bGroutPort_Open_7 := FALSE;
        bGroutPort_Open_8 := FALSE;
        rGroutPumpA_Cmd_pct := 0.0;
        rGroutPumpB_Cmd_pct := 0.0;

        (* Operator Reset Logic *)
        IF bAlarmReset AND (NOT bWaterIngressSensor_Bulkhead) AND bEmergencyStop THEN
            bEmergencyTripLatched := FALSE;
            bTripInterlockActive := FALSE;
            bEmergencySlurryGate_Close := FALSE;
            bCompressedAirSupply_Trip := FALSE;
            eState := 0;
        END_IF;
END_CASE;

iActiveFsmState := eState;
""")

    # =========================================================================
    # PHASE 6: ISA-18.2 MULTI-TIER PROCESS ALARMS & BIT-PACKED TELEMETRY
    # =========================================================================
    parts.append("""
(* ==================================================================================================== *)
(* PHASE 6: ISA-18.2 MULTI-TIER PROCESS ALARMS, DEADBAND HYSTERESIS & 32-BIT TELEMETRY                  *)
(* ==================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------- *)
(* 1. Face Earth Pressure Alarms (Nominal SP = 6.0 bar)                                                 *)
(* ---------------------------------------------------------------------------------------------------- *)
(* Critical High-High Face Pressure Trip: Risk of Sub-Riverbed Blowout (HH: 7.20 bar) *)
IF rVoted_EP_bar >= rLim_FacePress_HH_bar THEN
    rAlarmTimer_FacePress_HH_sec := rAlarmTimer_FacePress_HH_sec + tScanCycleTime_s;
    IF rAlarmTimer_FacePress_HH_sec >= 0.20 THEN
        dwAlarmWord1 := dwAlarmWord1 OR 16#00000001; (* Bit 0: Face Pressure High-High Trip *)
        IF iFirstOutCode = 0 THEN iFirstOutCode := 101; END_IF;
    END_IF;
ELSIF rVoted_EP_bar <= (rLim_FacePress_HH_bar - rDeadband_FacePress_bar) THEN
    rAlarmTimer_FacePress_HH_sec := 0.0;
    dwAlarmWord1 := dwAlarmWord1 AND NOT 16#00000001;
END_IF;

(* Face Pressure High Warning (H: 6.60 bar) *)
IF rVoted_EP_bar >= rLim_FacePress_H_bar THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#00000001; (* Bit 0: Face Pressure High Warning *)
ELSIF rVoted_EP_bar <= (rLim_FacePress_H_bar - rDeadband_FacePress_bar) THEN
    dwAlarmWord2 := dwAlarmWord2 AND NOT 16#00000001;
END_IF;

(* Face Pressure Low Warning (L: 5.40 bar) *)
IF rVoted_EP_bar <= rLim_FacePress_L_bar THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#00000002; (* Bit 1: Face Pressure Low Warning *)
ELSIF rVoted_EP_bar >= (rLim_FacePress_L_bar + rDeadband_FacePress_bar) THEN
    dwAlarmWord2 := dwAlarmWord2 AND NOT 16#00000002;
END_IF;

(* Critical Low-Low Face Pressure Trip: Risk of Ground Collapse / Ingress (LL: 4.80 bar) *)
IF rVoted_EP_bar <= rLim_FacePress_LL_bar THEN
    rAlarmTimer_FacePress_LL_sec := rAlarmTimer_FacePress_LL_sec + tScanCycleTime_s;
    IF rAlarmTimer_FacePress_LL_sec >= 0.25 THEN
        dwAlarmWord1 := dwAlarmWord1 OR 16#00000002; (* Bit 1: Face Pressure Low-Low Trip *)
        IF iFirstOutCode = 0 THEN iFirstOutCode := 102; END_IF;
    END_IF;
ELSIF rVoted_EP_bar >= (rLim_FacePress_LL_bar + rDeadband_FacePress_bar) THEN
    rAlarmTimer_FacePress_LL_sec := 0.0;
    dwAlarmWord1 := dwAlarmWord1 AND NOT 16#00000002;
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* 2. Cutterhead Drive System Alarms                                                                     *)
(* ---------------------------------------------------------------------------------------------------- *)
(* High-High Cutterhead Torque Overload Trip (HH: 21500 kNm) *)
IF rCutterhead_Torque_kNm >= rLim_CutterTorque_HH_kNm THEN
    rAlarmTimer_CutterTorque_HH_sec := rAlarmTimer_CutterTorque_HH_sec + tScanCycleTime_s;
    IF rAlarmTimer_CutterTorque_HH_sec >= 0.35 THEN
        dwAlarmWord1 := dwAlarmWord1 OR 16#00000004; (* Bit 2: Cutterhead Torque High-High Trip *)
        IF iFirstOutCode = 0 THEN iFirstOutCode := 201; END_IF;
    END_IF;
ELSIF rCutterhead_Torque_kNm <= (rLim_CutterTorque_HH_kNm - rDeadband_CutterTorque_kNm) THEN
    rAlarmTimer_CutterTorque_HH_sec := 0.0;
    dwAlarmWord1 := dwAlarmWord1 AND NOT 16#00000004;
END_IF;

(* Cutterhead Torque High Warning Approaching Hard Rock (H: 19500 kNm) *)
IF rCutterhead_Torque_kNm >= rLim_CutterTorque_H_kNm THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#00000004; (* Bit 2: Cutterhead Torque High Warning *)
ELSIF rCutterhead_Torque_kNm <= (rLim_CutterTorque_H_kNm - rDeadband_CutterTorque_kNm) THEN
    dwAlarmWord2 := dwAlarmWord2 AND NOT 16#00000004;
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* 3. Total Hydraulic Propulsion Thrust Force Alarms                                                     *)
(* ---------------------------------------------------------------------------------------------------- *)
(* Total Advance Thrust High-High Overload (HH: 135000 kN) *)
IF rEst_TotalThrust_kN >= rLim_TotalThrust_HH_kN THEN
    dwAlarmWord1 := dwAlarmWord1 OR 16#00000008; (* Bit 3: Total Thrust High-High Trip *)
    IF iFirstOutCode = 0 THEN iFirstOutCode := 301; END_IF;
ELSIF rEst_TotalThrust_kN <= (rLim_TotalThrust_HH_kN - rDeadband_TotalThrust_kN) THEN
    dwAlarmWord1 := dwAlarmWord1 AND NOT 16#00000008;
END_IF;

(* Total Advance Thrust High Warning (H: 120000 kN) *)
IF rEst_TotalThrust_kN >= rLim_TotalThrust_H_kN THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#00000008; (* Bit 3: Total Thrust High Warning *)
ELSIF rEst_TotalThrust_kN <= (rLim_TotalThrust_H_kN - rDeadband_TotalThrust_kN) THEN
    dwAlarmWord2 := dwAlarmWord2 AND NOT 16#00000008;
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* 4. Slurry Chamber Compressed Air Bubble Level Alarms                                                 *)
(* ---------------------------------------------------------------------------------------------------- *)
(* Air Cushion Liquid Flooding Low-Low Trip (LL: 2.50 m) *)
IF rAirCushion_Level_m <= rLim_AirBubbleLevel_LL_m THEN
    rAlarmTimer_AirBubble_LL_sec := rAlarmTimer_AirBubble_LL_sec + tScanCycleTime_s;
    IF rAlarmTimer_AirBubble_LL_sec >= 0.50 THEN
        dwAlarmWord1 := dwAlarmWord1 OR 16#00000010; (* Bit 4: Compressed Air Cushion Flooding LL Trip *)
        IF iFirstOutCode = 0 THEN iFirstOutCode := 401; END_IF;
    END_IF;
ELSIF rAirCushion_Level_m >= (rLim_AirBubbleLevel_LL_m + rDeadband_AirBubbleLevel_m) THEN
    rAlarmTimer_AirBubble_LL_sec := 0.0;
    dwAlarmWord1 := dwAlarmWord1 AND NOT 16#00000010;
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* 5. Tail Skin Annular Grouting Pressure Alarms                                                        *)
(* ---------------------------------------------------------------------------------------------------- *)
(* Annular Grout Injection High-High Overpressure: Shield Seal Blowout Risk (HH: 8.50 bar) *)
IF rVoted_GP_bar >= rLim_GroutPress_HH_bar THEN
    dwAlarmWord1 := dwAlarmWord1 OR 16#00000020; (* Bit 5: Annular Grout Overpressure HH Trip *)
    IF iFirstOutCode = 0 THEN iFirstOutCode := 501; END_IF;
ELSIF rVoted_GP_bar <= (rLim_GroutPress_HH_bar - rDeadband_GroutPress_bar) THEN
    dwAlarmWord1 := dwAlarmWord1 AND NOT 16#00000020;
END_IF;

(* Annular Grout Injection Low Pressure: Void Cavity Collapse Warning (L: 4.50 bar) *)
IF rVoted_GP_bar <= rLim_GroutPress_L_bar THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#00000010; (* Bit 4: Annular Grout Pressure Low Warning *)
ELSIF rVoted_GP_bar >= (rLim_GroutPress_L_bar + rDeadband_GroutPress_bar) THEN
    dwAlarmWord2 := dwAlarmWord2 AND NOT 16#00000010;
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* 6. Geological Mass Balance Over-Excavation Alarms                                                     *)
(* ---------------------------------------------------------------------------------------------------- *)
IF rCalc_MuckMassDiscrepancy_pct >= rLim_MuckDiscrepancy_HH_pct THEN
    dwAlarmWord1 := dwAlarmWord1 OR 16#00000040; (* Bit 6: Over-Excavation Sinkhole Risk HH Trip *)
    IF iFirstOutCode = 0 THEN iFirstOutCode := 601; END_IF;
ELSIF rCalc_MuckMassDiscrepancy_pct >= rLim_MuckDiscrepancy_H_pct THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#00000020; (* Bit 5: Over-Excavation Warning *)
ELSE
    dwAlarmWord1 := dwAlarmWord1 AND NOT 16#00000040;
    dwAlarmWord2 := dwAlarmWord2 AND NOT 16#00000020;
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* 7. Bulkhead Seal Water Ingress Trip                                                                   *)
(* ---------------------------------------------------------------------------------------------------- *)
IF bWaterIngressSensor_Bulkhead THEN
    rAlarmTimer_WaterIngress_sec := rAlarmTimer_WaterIngress_sec + tScanCycleTime_s;
    IF rAlarmTimer_WaterIngress_sec >= 0.10 THEN
        dwAlarmWord1 := dwAlarmWord1 OR 16#00000080; (* Bit 7: Emergency Water Ingress Bulkhead Trip *)
        IF iFirstOutCode = 0 THEN iFirstOutCode := 701; END_IF;
    END_IF;
ELSE
    rAlarmTimer_WaterIngress_sec := 0.0;
    dwAlarmWord1 := dwAlarmWord1 AND NOT 16#00000080;
END_IF;

(* First-Out Latching Reset *)
IF bAlarmReset THEN
    iFirstOutCode := 0;
END_IF;
dwFirstOutWord := DINT_TO_DWORD(iFirstOutCode);

(* ---------------------------------------------------------------------------------------------------- *)
(* 8. Bit-Packed Diagnostic Status Words                                                                 *)
(* ---------------------------------------------------------------------------------------------------- *)
(* dwStatusWord1: Mechanical & Operational Subsystems Health *)
dwStatusWord1 := 16#00000000;
IF bSystemRunning THEN dwStatusWord1 := dwStatusWord1 OR 16#00000001; END_IF;
IF bAdvancePermissive THEN dwStatusWord1 := dwStatusWord1 OR 16#00000002; END_IF;
IF bCutterhead_Direction_CW THEN dwStatusWord1 := dwStatusWord1 OR 16#00000004; END_IF;
IF bHardRockDetected THEN dwStatusWord1 := dwStatusWord1 OR 16#00000008; END_IF;
IF bStrokeLimitReached THEN dwStatusWord1 := dwStatusWord1 OR 16#00000010; END_IF;
IF bSegmentErector_Parked THEN dwStatusWord1 := dwStatusWord1 OR 16#00000020; END_IF;
IF bSegmentErector_RingComplete THEN dwStatusWord1 := dwStatusWord1 OR 16#00000040; END_IF;
IF bEmergencySlurryGate_Close THEN dwStatusWord1 := dwStatusWord1 OR 16#00000080; END_IF;
IF bCompressedAirSupply_Trip THEN dwStatusWord1 := dwStatusWord1 OR 16#00000100; END_IF;
IF bAutoExcavationMode THEN dwStatusWord1 := dwStatusWord1 OR 16#00000200; END_IF;
IF bSystemEnable THEN dwStatusWord1 := dwStatusWord1 OR 16#00000400; END_IF;
IF bTripInterlockActive THEN dwStatusWord1 := dwStatusWord1 OR 16#00000800; END_IF;

(* dwStatusWord2: 2oo3 TMR Voting Health & Observer Convergence *)
dwStatusWord2 := 16#00000000;
IF bHealthy_EP1 THEN dwStatusWord2 := dwStatusWord2 OR 16#00000001; END_IF;
IF bHealthy_EP2 THEN dwStatusWord2 := dwStatusWord2 OR 16#00000002; END_IF;
IF bHealthy_EP3 THEN dwStatusWord2 := dwStatusWord2 OR 16#00000004; END_IF;
IF bDiscrepancy_EP THEN dwStatusWord2 := dwStatusWord2 OR 16#00000008; END_IF;
IF bDegraded_EP THEN dwStatusWord2 := dwStatusWord2 OR 16#00000010; END_IF;

IF bHealthy_CP1 THEN dwStatusWord2 := dwStatusWord2 OR 16#00000020; END_IF;
IF bHealthy_CP2 THEN dwStatusWord2 := dwStatusWord2 OR 16#00000040; END_IF;
IF bHealthy_CP3 THEN dwStatusWord2 := dwStatusWord2 OR 16#00000080; END_IF;
IF bDiscrepancy_CP THEN dwStatusWord2 := dwStatusWord2 OR 16#00000100; END_IF;
IF bDegraded_CP THEN dwStatusWord2 := dwStatusWord2 OR 16#00000200; END_IF;

IF bHealthy_AP1 THEN dwStatusWord2 := dwStatusWord2 OR 16#00000400; END_IF;
IF bHealthy_AP2 THEN dwStatusWord2 := dwStatusWord2 OR 16#00000800; END_IF;
IF bHealthy_AP3 THEN dwStatusWord2 := dwStatusWord2 OR 16#00001000; END_IF;
IF bDiscrepancy_AP THEN dwStatusWord2 := dwStatusWord2 OR 16#00002000; END_IF;
IF bDegraded_AP THEN dwStatusWord2 := dwStatusWord2 OR 16#00004000; END_IF;

IF bHealthy_GP1 THEN dwStatusWord2 := dwStatusWord2 OR 16#00008000; END_IF;
IF bHealthy_GP2 THEN dwStatusWord2 := dwStatusWord2 OR 16#00010000; END_IF;
IF bHealthy_GP3 THEN dwStatusWord2 := dwStatusWord2 OR 16#00020000; END_IF;
IF bDiscrepancy_GP THEN dwStatusWord2 := dwStatusWord2 OR 16#00040000; END_IF;
IF bDegraded_GP THEN dwStatusWord2 := dwStatusWord2 OR 16#00080000; END_IF;

(* Latch Critical Master Trip if any HH/LL Alarms Asserted *)
IF (dwAlarmWord1 <> 16#00000000) THEN
    bTripInterlockActive := TRUE;
END_IF;

(* Store Previous Actuator Values for Next Scan Slew Rate Rate-Limiting *)
FOR iIter := 1 TO 6 DO
    u_prev[iIter] := u_ctrl[iIter];
END_FOR;
""")

    # =========================================================================
    # CLOSING DECLARATION
    # =========================================================================
    parts.append("""
END_FUNCTION_BLOCK
""")

    return "\n".join(parts)

if __name__ == "__main__":
    code = generate_iec_st()
    print("Generated ST code length:", len(code))
