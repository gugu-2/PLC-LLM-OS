# generate_fuel_tank_dataset.py
import os
import sys
import json
import re

def build_full_st_code():
    out = []

    # -------------------------------------------------------------------------
    # HEADER
    # -------------------------------------------------------------------------
    out.append("""FUNCTION_BLOCK FB_Plastics_EBM_FuelTank_ParisonControl_Sync
(*
 * ====================================================================================================================
 * SYSTEM ARCHITECTURE & CYBER-PHYSICAL SPECIFICATION
 * ====================================================================================================================
 * PROJECT:          Continuous 6-Layer Co-Extrusion Blow Molding (EBM) Automotive Fuel Tank Production Line
 *                   High-Speed Electro-Hydraulic Tooling Gap, 100-Point Axial/Radial Wall Thickness Distribution (WDS/PWDS),
 *                   Non-Linear Parison Viscoelastic Sag & Die Swell Dynamics, Robotic Bottom Pre-Pinch Manipulation,
 *                   and In-Mold High-Pressure Cryogenic Nitrogen Blow Conditioning Suite.
 * DOMAIN:           Plastics & Polymer Processing / Automotive Clean Fuel Storage Systems (CARB PZEV / LEV III / Euro 6d).
 * CONTROLLER:       IEC 61131-3 Real-Time Industrial Controller (Beckhoff TwinCAT 3 / Siemens S7-1500 / Allen-Bradley Logix).
 * SAFETY INTEGRITY: ISO 13849-1 Category 4 / PLe, IEC 62061 SIL-3 Hardened Cyber-Physical Architecture.
 * EXECUTION CYCLE:  Deterministic Real-Time Scan Cycle: Ts = 1.000 ms (1000 Hz Execution Rate).
 *
 * CYBER-PHYSICAL SYSTEM DESCRIPTION & SUBSYSTEMS INTEGRATION:
 * This Function Block FB_Plastics_EBM_FuelTank_ParisonControl_Sync executes deterministic, sub-millisecond synchronous
 * control over a multi-million-dollar continuous co-extrusion blow molding cell producing 6-layer high-density
 * polyethylene (HDPE) automotive fuel tanks (nominal 75-liter fuel capacity, 11.8 kg parison mass, 1,800 mm hanging length).
 *
 * 1. 6-LAYER CO-EXTRUSION MELT STREAM ARCHITECTURE:
 *    - Extruder A (Layer 1 - Inner Skin): Virgin HDPE with antistatic and bio-fuel permeation resistant resin (30.0% mass).
 *    - Extruder B (Layer 2 - Core Regrind): Post-Industrial Recycled / Regrind HDPE blended with virgin base (42.0% mass).
 *    - Extruder C (Layer 3 - Outer Tie): Maleic Anhydride (MAH) grafted PE adhesive bonding agent (2.5% mass).
 *    - Extruder D (Layer 4 - Permeation Barrier): Ethylene Vinyl Alcohol (EVOH 29-32 mol% ethylene) gas barrier (3.0% mass).
 *    - Extruder E (Layer 5 - Inner Tie): Maleic Anhydride (MAH) grafted PE adhesive bonding agent (2.5% mass).
 *    - Extruder F (Layer 6 - Outer Skin): Virgin HDPE compounded with carbon black for UV and electrostatic dissipation (20.0% mass).
 *
 * 2. 100-POINT WALL THICKNESS DISTRIBUTION SYSTEM (WDS & PWDS):
 *    - Axial Wall Thickness (WDS): Dynamic electro-hydraulic servo tooling gap (0.5 mm to 12.0 mm nominal annular orifice)
 *      driven by a high-bandwidth Moog servo valve with LVDT positional feedback (< 8 ms step response, > 70 Hz bandwidth).
 *    - Partial / Radial Wall Thickness (PWDS / RWDS): High-speed electro-hydraulic servo pushrod ring ovalization (+/- 3.5 mm)
 *      dynamically compensating for deep-draw saddle bridge geometries, propshaft tunnels, and fuel filler neck pinch contours.
 *    - Synchronous 100-point axial interpolation mapped against parison vertical drop encoder and laser distance sensors.
 *
 * 3. NON-LINEAR POLYMER RHEOLOGY & CYBER-PHYSICAL DYNAMICS:
 *    - Tanner Elastic Recovery Die Swell Constitutive Law: Computes radial swell ratio B based on first normal stress
 *      difference N1 and die wall shear stress tau_w: B = (1 + 0.5 * (N1 / (2 * tau_w))^2)^0.1667.
 *    - Cross-WLF Viscosity Model: Shear-thinning and temperature-dependent viscosity accounting for viscous dissipation.
 *    - Viscoelastic Sag Elongation: Modified Maxwell-Voigt constitutive model tracking parison gravitational elongation
 *      strain under continuous hanging self-weight, counteracted by real-time profile bias compensation.
 *
 * 4. DISCRETE STATE-SPACE MODEL & STEADY-STATE KALMAN FILTER (12 States, 4 Inputs, 6 Outputs):
 *    - States x[k]:
 *        x1:  Parison tip vertical position [mm]
 *        x2:  Parison sag elongation strain [mm/mm]
 *        x3:  Radial die swell ratio [dimensionless]
 *        x4:  Melt temperature at die exit [deg C]
 *        x5:  Inner layer HDPE thickness [mm]
 *        x6:  EVOH barrier layer thickness [mm]
 *        x7:  Die gap hydraulic servo spool position [mm]
 *        x8:  Extruder head pressure [bar]
 *        x9:  Parison internal pre-blow pressure [bar]
 *        x10: Parison pinch-off weld temperature [deg C]
 *        x11: Mold nitrogen inflation pressure [bar]
 *        x12: Mold cavity cooling surface heat flux [kW/m2]
 *    - Inputs u[k]:
 *        u1: Hydraulic servo valve spool command [%] (-100.0% to +100.0%)
 *        u2: Master extruder screw speed command [RPM] (0.0 to 120.0 RPM)
 *        u3: Pre-blow air / high-pressure N2 servo valve command [%] (0.0% to 100.0%)
 *        u4: Mold cavity chilled water proportional valve command [%] (0.0% to 100.0%)
 *    - Outputs y[k]:
 *        y1: Parison tip vertical position [mm] (laser triangulation sensor)
 *        y2: Parison swell diameter / wall thickness proxy [mm] (optical diameter gauge)
 *        y3: Die exit melt temperature [deg C] (die orifice IR pyrometer)
 *        y4: Die head melt pressure [bar] (diaphragm piezoelectric transducer)
 *        y5: Parison internal / mold cavity pressure [bar] (piezoresistive pressure sensor)
 *        y6: Die gap servo LVDT position [mm] (inductive linear position transducer)
 *    - Observer Equations:
 *        x_pred[k+1] = A * x[k] + B * u[k]
 *        y_pred[k]   = C * x_pred[k] + D * u[k]
 *        e[k]        = y_meas[k] - y_pred[k]
 *        x_corr[k+1] = x_pred[k+1] + L * e[k]
 *
 * 5. RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) WITH PROJECTED GRADIENT DESCENT:
 *    - 10-step look-ahead receding horizon (k = 0 to 9) with unrolled Projected Gradient Descent (PGD) iterations.
 *    - Quadratic cost function penalizing state trajectory tracking errors (Q), control effort (R), terminal state (P),
 *      and actuator slew rate variations (S):
 *        J = sum_{h=0..9} [ (x_h - x_ref)^T * Q * (x_h - x_ref) + (u_h - u_ref)^T * R * (u_h - u_ref) + (delta_u_h)^T * S * (delta_u_h) ]
 *            + (x_10 - x_ref)^T * P * (x_10 - x_ref)
 *    - Full forward simulation rollout, terminal costate initialization, backward adjoint costate propagation,
 *      control gradient evaluation, and projected saturation clipping with hydraulic servo slew rate constraints.
 *
 * 6. TRIPLE MODULAR REDUNDANCY (2oo3 TMR) SENSOR VOTING:
 *    - Four independent safety-critical sensor channels:
 *        Channel 1: Die Gap LVDT Servo Position Sensors (ChA, ChB, ChC) [mm]
 *        Channel 2: Co-Extrusion Melt Pressure Transducers (ChA, ChB, ChC) [bar]
 *        Channel 3: Die Orifice IR Melt Pyrometers (ChA, ChB, ChC) [deg C]
 *        Channel 4: Mold Cavity Nitrogen Gas Pressure Transducers (ChA, ChB, ChC) [bar]
 *    - 15 ms discrepancy persistence timers, automated bumpless degradation to 1oo2 on single sensor failure,
 *      and immediate fail-safe tool gap freeze / emergency shutdown upon dual disagreement.
 *
 * 7. DETERMINISTIC 14-STAGE PRODUCTION FINITE STATE MACHINE (FSM):
 *    - State 0:  IDLE_SAFE_STANDBY
 *    - State 1:  EXTRUDER_MELT_TEMPERATURE_HOMOGENIZATION
 *    - State 2:  DIE_GAP_CALIBRATION_ZERO_SEEKING
 *    - State 3:  PARISON_CONTINUOUS_EXTRUSION_PROFILE_RAMP
 *    - State 4:  100_POINT_WDS_SERVO_GAP_SYNCHRONIZATION
 *    - State 5:  PRE_BLOW_AIR_INJECTION_PARISON_SHAPING
 *    - State 6:  ROBOTIC_BOTTOM_PRE_PINCH_MANIPULATION
 *    - State 7:  MOLD_CLAMPING_HIGH_TONNAGE_LOCK
 *    - State 8:  BLOW_PIN_INSERTION_HIGH_PRESSURE_N2_BLOW
 *    - State 9:  IN_MOLD_CRYOGENIC_COOLING_CYCLE
 *    - State 10: EXHAUST_DEPRESSURIZATION_DEFLATION
 *    - State 11: MOLD_OPENING_PART_GRIPPER_EXTRACTION
 *    - State 12: FLASH_DEFLASHING_PUNCH_TRIM_CYCLE
 *    - State 13: EMERGENCY_PARISON_DROP_PURGE_TRIP
 *
 * 8. ANSI/ISA-18.2 MULTI-TIERED ALARM ENGINE & 32-BIT BIT-PACKED TELEMETRY:
 *    - Multi-tiered threshold supervision: HH (High-High Trip), H (High Warning), L (Low Warning), LL (Low-Low Trip).
 *    - Configurable hysteresis deadbands, persistence timers, startup alarm suppression masks, and latching registers.
 *    - Bit-packed DWORD telemetry and alarm registers for SCADA, MES, and functional safety PLCs.
 * ====================================================================================================================
 *)
""")

    # -------------------------------------------------------------------------
    # VAR_INPUT
    # -------------------------------------------------------------------------
    out.append("""VAR_INPUT
    (* Master Operational Control & Interlock Commands *)
    bSystem_Enable_In                   : BOOL;    (* Master Automation Suite Enable Permissive [bool] *)
    bCycle_Start_In                     : BOOL;    (* Operator Automatic Production Cycle Start Command [bool] *)
    bCycle_Stop_In                      : BOOL;    (* Controlled Orderly Production Cycle Stop Command [bool] *)
    bEmergency_Stop_Trip_In             : BOOL;    (* Dual-Channel Hardwired Safety Circuit E-Stop Trip Active [bool] *)
    bSafety_Gate_Interlock_Closed_In    : BOOL;    (* Extrusion Enclosure Perimeter Dual Safety Gate Closed [bool] *)
    bFlash_Granulator_Ready_In          : BOOL;    (* In-Line Deflashing Flash Regrind Granulator Running [bool] *)
    bRobot_PrePinch_Handshake_Ready_In  : BOOL;    (* Bottom Pre-Pinch Robotic Arm Synchronous Ready Handshake [bool] *)
    bPart_Extractor_Robot_Ready_In      : BOOL;    (* Demolding Tank Unloading 6-Axis Robot Ready Handshake [bool] *)
    bChilled_Water_Flow_Confirmed_In    : BOOL;    (* Mold Cavity Chilled Cooling Water Recirculation Verified [bool] *)
    bNitrogen_Supply_Pressure_OK_In     : BOOL;    (* Bulk High-Pressure Cryogenic Nitrogen Storage Supply Confirmed [bool] *)

    (* Process Recipe Setpoints & Physical Parameters *)
    rRecipe_Target_Parison_Length_mm_In : REAL;    (* Target Extruded Parison Hanging Drop Length [mm] *)
    rRecipe_Cycle_Time_Target_s_In      : REAL;    (* Target Total Mold Blow Molding Cycle Time [s] *)
    rRecipe_Extrusion_Mass_Flow_kgh_In  : REAL;    (* Total 6-Layer Extrusion Co-Ex Throughput Rate [kg/h] *)
    rRecipe_Nominal_Tooling_Gap_mm_In   : REAL;    (* Nominal Baseline Conical Die Mandrel Tooling Gap [mm] *)
    rRecipe_Inner_HDPE_Layer_Ratio_In   : REAL;    (* Layer 1 Inner Virgin HDPE Mass Proportion Setpoint [%] *)
    rRecipe_EVOH_Barrier_Layer_Ratio_In : REAL;    (* Layer 4 EVOH Permeation Barrier Mass Proportion Setpoint [%] *)
    rRecipe_PreBlow_Pressure_bar_In     : REAL;    (* Parison Preliminary Internal Shaping Air Pressure [bar] *)
    rRecipe_High_Pressure_N2_bar_In     : REAL;    (* Mold Cavity High-Pressure Nitrogen Blow Setpoint [bar] *)
    rRecipe_Mold_Chilled_Temp_In        : REAL;    (* Regulated Mold Cavity Chilled Cooling Water Supply Temperature [deg C] *)
    rRecipe_InMold_Cooling_Time_s_In    : REAL;    (* In-Mold Nitrogen Pressure Soak & Cryogenic Cooling Duration [s] *)
    rRecipe_Mold_Clamp_Tonnage_kN_In    : REAL;    (* Hydraulic Mold Clamping Tie-Bar Full Lockup Tonnage [kN] *)
    rRecipe_WDS_Profile_Weight_Bias_In  : REAL;    (* Master Axial Wall Thickness Global Scaling Weight Bias [%] *)

    (* Channel 1: 2oo3 Triple Modular Redundant (TMR) Die Gap LVDT Servo Position Sensors *)
    rDieGap_LVDT_ChA_mm_In              : REAL;    (* Die Gap Hydraulic Proportional Servo LVDT Sensor ChA [mm] *)
    rDieGap_LVDT_ChB_mm_In              : REAL;    (* Die Gap Hydraulic Proportional Servo LVDT Sensor ChB [mm] *)
    rDieGap_LVDT_ChC_mm_In              : REAL;    (* Die Gap Hydraulic Proportional Servo LVDT Sensor ChC [mm] *)

    (* Channel 2: 2oo3 Triple Modular Redundant (TMR) Co-Extrusion Melt Pressure Transducers *)
    rMeltPressure_Transducer_ChA_bar_In : REAL;    (* Extruder Die Head Co-Ex Melt Pressure Transducer ChA [bar] *)
    rMeltPressure_Transducer_ChB_bar_In : REAL;    (* Extruder Die Head Co-Ex Melt Pressure Transducer ChB [bar] *)
    rMeltPressure_Transducer_ChC_bar_In : REAL;    (* Extruder Die Head Co-Ex Melt Pressure Transducer ChC [bar] *)

    (* Channel 3: 2oo3 Triple Modular Redundant (TMR) Die Orifice IR Melt Pyrometers *)
    rDieMeltTemp_IR_ChA_In              : REAL;    (* Die Orifice Melt Exit Temperature Non-Contact IR Pyrometer ChA [deg C] *)
    rDieMeltTemp_IR_ChB_In              : REAL;    (* Die Orifice Melt Exit Temperature Non-Contact IR Pyrometer ChB [deg C] *)
    rDieMeltTemp_IR_ChC_In              : REAL;    (* Die Orifice Melt Exit Temperature Non-Contact IR Pyrometer ChC [deg C] *)

    (* Channel 4: 2oo3 Triple Modular Redundant (TMR) Mold Cavity Nitrogen Gas Pressure Transducers *)
    rMoldN2Pressure_Transducer_ChA_bar_In : REAL;  (* Mold Cavity Nitrogen Gas Pressure Transducer ChA [bar] *)
    rMoldN2Pressure_Transducer_ChB_bar_In : REAL;  (* Mold Cavity Nitrogen Gas Pressure Transducer ChB [bar] *)
    rMoldN2Pressure_Transducer_ChC_bar_In : REAL;  (* Mold Cavity Nitrogen Gas Pressure Transducer ChC [bar] *)

    (* Secondary Field Sensor Instrumentation & Handshake Feedbacks *)
    rParison_Tip_Laser_Pos_mm_In        : REAL;    (* High-Speed Optical Laser Parison Drop Tip Distance [mm] *)
    rParison_Extrusion_Speed_mms_In     : REAL;    (* Non-Contact Optical Parison Surface Extrusion Velocity [mm/s] *)
    rHydraulic_Supply_Pressure_bar_In   : REAL;    (* Hydraulic Power Unit (HPU) High-Pressure Manifold [bar] *)
    rHydraulic_Oil_Temp_In              : REAL;    (* Hydraulic Power Unit Fluid Reservoir Temperature [deg C] *)
    rMold_Cooling_Flow_Lpm_In           : REAL;    (* Ultrasonic In-Line Mold Chilled Water Flow Rate [L/min] *)
    rMold_Cooling_Return_Temp_In        : REAL;    (* Mold Cavity Cooling Water Return Line Temperature [deg C] *)
    rRobotic_PrePinch_Clamping_Force_kN_In : REAL; (* Robotic Bottom Pre-Pinch Servo Tooling Clamping Force [kN] *)
    rMold_Actual_Clamping_Tonnage_kN_In : REAL;    (* Mold Tie-Bar Extensometer Strain Gauge Actual Tonnage [kN] *)
    bBlowPin_Full_Insertion_LS_In       : BOOL;    (* High-Pressure Nitrogen Blow Pin Fully Engaged Limit Switch [bool] *)
    bMold_Closed_Parting_Line_LS_In     : BOOL;    (* Mold Clamping Parting Line Fully Locked Proximity Switch [bool] *)
    bFlash_Trimmer_Cycle_Completed_In   : BOOL;    (* Hydraulic Flash Trimming Press De-flashing Cycle Complete [bool] *)
    bOperator_Alarm_Reset_Cmd_In        : BOOL;    (* Operator Pushbutton ISA-18.2 Alarm Acknowledge & Reset [bool] *)
END_VAR
""")

    # -------------------------------------------------------------------------
    # VAR_OUTPUT
    # -------------------------------------------------------------------------
    out.append("""VAR_OUTPUT
    (* Continuous Electro-Hydraulic & Pneumatic Actuator Output Commands *)
    rServo_DieGap_Spool_Cmd_Pct_Out     : REAL;    (* Hydraulic Proportional Servo Valve Spool Position Command [-100.0..+100.0 %] *)
    rExtruder_Master_Speed_RPM_Out      : REAL;    (* Master Extruder Drive Screw Rotational Speed Command [RPM] *)
    rPreBlow_Air_Servo_Cmd_Pct_Out      : REAL;    (* Low-Pressure Parison Shaping Air Servo Valve Command [0.0..100.0 %] *)
    rHighPress_N2_Blow_Valve_Pct_Out    : REAL;    (* High-Pressure Nitrogen Gas Inflation Servo Valve Command [0.0..100.0 %] *)
    rMold_Cooling_Water_Valve_Pct_Out   : REAL;    (* Mold Cavity Chilled Water Modulating Valve Command [0.0..100.0 %] *)
    rPWDS_Radial_Ovalization_mm_Out     : REAL;    (* Radial Partial Wall Thickness Dynamic Core Ovalization Command [mm] *)

    (* Co-Extruder Sub-Drive Synchronous RPM Setpoints (Layers 1 to 6) *)
    rExtruder_A_InnerHDPE_RPM_Out       : REAL;    (* Extruder A (Virgin Inner HDPE Skin) Screw Speed Setpoint [RPM] *)
    rExtruder_B_Regrind_RPM_Out         : REAL;    (* Extruder B (Post-Consumer Regrind HDPE) Screw Speed Setpoint [RPM] *)
    rExtruder_C_TieLayer1_RPM_Out       : REAL;    (* Extruder C (Adhesive Tie Resin 1) Screw Speed Setpoint [RPM] *)
    rExtruder_D_EVOH_RPM_Out            : REAL;    (* Extruder D (EVOH Gas Barrier Resin) Screw Speed Setpoint [RPM] *)
    rExtruder_E_TieLayer2_RPM_Out       : REAL;    (* Extruder E (Adhesive Tie Resin 2) Screw Speed Setpoint [RPM] *)
    rExtruder_F_OuterHDPE_RPM_Out       : REAL;    (* Extruder F (Antistatic Outer HDPE Skin) Screw Speed Setpoint [RPM] *)

    (* Discrete Digital Actuators, Solenoid Valves & Robotic Interlocks *)
    bMold_Close_HighTonnage_Cmd_Out     : BOOL;    (* Mold Hydraulic Clamping High-Tonnage Lockup Solenoid Command [bool] *)
    bMold_Open_PartExtraction_Cmd_Out   : BOOL;    (* Mold Hydraulic Unclamping & Opening Solenoid Command [bool] *)
    bBlowPin_Cylinder_Advance_Cmd_Out   : BOOL;    (* High-Pressure Nitrogen Blow Pin Hydraulic Insertion Command [bool] *)
    bBlowPin_Cylinder_Retract_Cmd_Out   : BOOL;    (* High-Pressure Nitrogen Blow Pin Hydraulic Retraction Command [bool] *)
    bExhaust_Depressurization_Valve_Cmd_Out : BOOL;(* Mold Cavity Fast Exhaust Decompression Solenoid Command [bool] *)
    bParison_CutOff_HotKnife_Cmd_Out    : BOOL;    (* Parison Cut-Off Rotary Hot Knife / Shear Guillotine Fire Command [bool] *)
    bRobot_PrePinch_Start_Permissive_Out: BOOL;    (* Permissive Strobe to Robotic Arm for Bottom Parison Pre-Pinch [bool] *)
    bRobot_PartExtract_Start_Permissive_Out : BOOL;(* Permissive Strobe to Demolding Robot for Fuel Tank Extraction [bool] *)
    bFlash_Trimmer_Start_Permissive_Out : BOOL;    (* Permissive Strobe to Hydraulic Trimming Press for Flash Cut [bool] *)

    (* Synthesized State-Space & Real-Time Production Diagnostics *)
    iFSM_State_Current_Out              : INT;     (* Deterministic 14-Stage Blow Molding State Machine Active State [enum] *)
    rParison_Current_Length_mm_Out      : REAL;    (* Synthesized Voted Parison Hanging Drop Length [mm] *)
    rWDS_Active_Profile_Point_Out       : REAL;    (* Current Active WDS Axial Interpolation Index [0.0..99.0] *)
    rCalculated_FuelTank_Mass_kg_Out    : REAL;    (* Real-Time Dynamic Estimated Parison / Fuel Tank Weight [kg] *)
    rEVOH_Estimated_Layer_Thickness_um_Out : REAL; (* Estimated Real-Time EVOH Barrier Layer Thickness [um] *)
    rActual_DieSwell_Ratio_Out          : REAL;    (* Dynamic Tanner-Derived Radial Die Swell Ratio [dimensionless] *)
    rEstimated_PinchWeld_Temp_Out       : REAL;    (* Bottom Pinch-Off Weld Line Fusion Temperature [deg C] *)

    (* 32-Bit Bit-Packed Operating Telemetry & ISA-18.2 Alarm Words *)
    dwSystem_Status_Word_Out            : DWORD;   (* 32-Bit Bit-Packed Machine Operating Telemetry Status Register [dword] *)
    dwAlarm_Word_01_CriticalTrips_Out   : DWORD;   (* ISA-18.2 Priority 1 Hard Safety Shutdown Trip Alarm Word [dword] *)
    dwAlarm_Word_02_Warnings_Out        : DWORD;   (* ISA-18.2 Priority 2 Process Out-Of-Spec Warning Alarm Word [dword] *)
    dwAlarm_Word_03_TMR_Discrepancies_Out : DWORD; (* ISA-18.2 Priority 3 Triple Modular Redundancy Sensor Faults [dword] *)
    dwAlarm_Word_04_ProcessDeviations_Out : DWORD; (* ISA-18.2 Priority 4 Hydraulic, Extruder & Cooling Fault Word [dword] *)
END_VAR
""")

    # -------------------------------------------------------------------------
    # VAR
    # -------------------------------------------------------------------------
    out.append("""VAR
    (* Real-Time Deterministic Clock & Initialization Registers *)
    bInitialized                        : BOOL := FALSE; (* Cold-Start Initialization One-Shot Flag *)
    rCycle_Time_s                       : REAL := 0.001; (* Fixed Deterministic Loop Execution Sample Time [s] *)
    rMaster_Clock_Seconds               : REAL := 0.0;   (* Free-Running Monotonic System Master Clock [s] *)

    (* SECTION 1: 12-STATE FIRST-PRINCIPLES DISCRETE CYBER-PHYSICAL OBSERVER VECTORS *)
    rVec_x_State_1                      : REAL := 0.0;   (* x1: Parison tip vertical drop position [mm] *)
    rVec_x_State_2                      : REAL := 0.0;   (* x2: Parison sag elongation strain [mm/mm] *)
    rVec_x_State_3                      : REAL := 1.45;  (* x3: Radial die swell ratio [dimensionless] *)
    rVec_x_State_4                      : REAL := 210.0; (* x4: Melt temperature at die exit [deg C] *)
    rVec_x_State_5                      : REAL := 3.20;  (* x5: Inner layer HDPE thickness [mm] *)
    rVec_x_State_6                      : REAL := 0.180; (* x6: EVOH barrier layer thickness [mm] *)
    rVec_x_State_7                      : REAL := 4.50;  (* x7: Die gap hydraulic servo spool position [mm] *)
    rVec_x_State_8                      : REAL := 185.0; (* x8: Extruder head melt pressure [bar] *)
    rVec_x_State_9                      : REAL := 0.0;   (* x9: Parison internal pre-blow pressure [bar] *)
    rVec_x_State_10                     : REAL := 205.0; (* x10: Parison pinch-off weld line temperature [deg C] *)
    rVec_x_State_11                     : REAL := 0.0;   (* x11: Mold cavity nitrogen inflation pressure [bar] *)
    rVec_x_State_12                     : REAL := 0.0;   (* x12: Mold cavity cooling surface heat flux [kW/m2] *)

    rVec_x_Pred_1                       : REAL := 0.0;   (* Prior State Prediction x_hat[k+1|k] State 1 *)
    rVec_x_Pred_2                       : REAL := 0.0;   (* Prior State Prediction x_hat[k+1|k] State 2 *)
    rVec_x_Pred_3                       : REAL := 0.0;   (* Prior State Prediction x_hat[k+1|k] State 3 *)
    rVec_x_Pred_4                       : REAL := 0.0;   (* Prior State Prediction x_hat[k+1|k] State 4 *)
    rVec_x_Pred_5                       : REAL := 0.0;   (* Prior State Prediction x_hat[k+1|k] State 5 *)
    rVec_x_Pred_6                       : REAL := 0.0;   (* Prior State Prediction x_hat[k+1|k] State 6 *)
    rVec_x_Pred_7                       : REAL := 0.0;   (* Prior State Prediction x_hat[k+1|k] State 7 *)
    rVec_x_Pred_8                       : REAL := 0.0;   (* Prior State Prediction x_hat[k+1|k] State 8 *)
    rVec_x_Pred_9                       : REAL := 0.0;   (* Prior State Prediction x_hat[k+1|k] State 9 *)
    rVec_x_Pred_10                      : REAL := 0.0;   (* Prior State Prediction x_hat[k+1|k] State 10 *)
    rVec_x_Pred_11                      : REAL := 0.0;   (* Prior State Prediction x_hat[k+1|k] State 11 *)
    rVec_x_Pred_12                      : REAL := 0.0;   (* Prior State Prediction x_hat[k+1|k] State 12 *)

    rVec_x_Corr_1                       : REAL := 0.0;   (* Posterior State Correction x_hat[k|k] State 1 *)
    rVec_x_Corr_2                       : REAL := 0.0;   (* Posterior State Correction x_hat[k|k] State 2 *)
    rVec_x_Corr_3                       : REAL := 0.0;   (* Posterior State Correction x_hat[k|k] State 3 *)
    rVec_x_Corr_4                       : REAL := 0.0;   (* Posterior State Correction x_hat[k|k] State 4 *)
    rVec_x_Corr_5                       : REAL := 0.0;   (* Posterior State Correction x_hat[k|k] State 5 *)
    rVec_x_Corr_6                       : REAL := 0.0;   (* Posterior State Correction x_hat[k|k] State 6 *)
    rVec_x_Corr_7                       : REAL := 0.0;   (* Posterior State Correction x_hat[k|k] State 7 *)
    rVec_x_Corr_8                       : REAL := 0.0;   (* Posterior State Correction x_hat[k|k] State 8 *)
    rVec_x_Corr_9                       : REAL := 0.0;   (* Posterior State Correction x_hat[k|k] State 9 *)
    rVec_x_Corr_10                      : REAL := 0.0;   (* Posterior State Correction x_hat[k|k] State 10 *)
    rVec_x_Corr_11                      : REAL := 0.0;   (* Posterior State Correction x_hat[k|k] State 11 *)
    rVec_x_Corr_12                      : REAL := 0.0;   (* Posterior State Correction x_hat[k|k] State 12 *)

    (* Applied Physical Input Vector u[k] (4 Inputs) *)
    rVec_u_1                            : REAL := 0.0;   (* u1: Hydraulic servo valve command [%] *)
    rVec_u_2                            : REAL := 0.0;   (* u2: Master extruder screw speed command [RPM] *)
    rVec_u_3                            : REAL := 0.0;   (* u3: Pre-blow / high-pressure N2 servo valve command [%] *)
    rVec_u_4                            : REAL := 0.0;   (* u4: Mold cooling water proportional valve command [%] *)

    (* Measured Output Vector y_meas[k] (6 Outputs) *)
    rVec_y_Meas_1                       : REAL := 0.0;   (* y1: Parison tip vertical position [mm] *)
    rVec_y_Meas_2                       : REAL := 0.0;   (* y2: Parison swell diameter / wall thickness proxy [mm] *)
    rVec_y_Meas_3                       : REAL := 0.0;   (* y3: Die exit melt temperature [deg C] *)
    rVec_y_Meas_4                       : REAL := 0.0;   (* y4: Die head melt pressure [bar] *)
    rVec_y_Meas_5                       : REAL := 0.0;   (* y5: Parison internal / mold cavity pressure [bar] *)
    rVec_y_Meas_6                       : REAL := 0.0;   (* y6: Die gap servo LVDT position [mm] *)

    (* Model Output Prediction y_pred[k] (6 Outputs) *)
    rVec_y_Pred_1                       : REAL := 0.0;   (* y_pred 1 *)
    rVec_y_Pred_2                       : REAL := 0.0;   (* y_pred 2 *)
    rVec_y_Pred_3                       : REAL := 0.0;   (* y_pred 3 *)
    rVec_y_Pred_4                       : REAL := 0.0;   (* y_pred 4 *)
    rVec_y_Pred_5                       : REAL := 0.0;   (* y_pred 5 *)
    rVec_y_Pred_6                       : REAL := 0.0;   (* y_pred 6 *)

    (* Innovation Residual Vector e[k] = y_meas - y_pred (6 Residuals) *)
    rVec_e_Resid_1                      : REAL := 0.0;   (* Innovation residual 1 *)
    rVec_e_Resid_2                      : REAL := 0.0;   (* Innovation residual 2 *)
    rVec_e_Resid_3                      : REAL := 0.0;   (* Innovation residual 3 *)
    rVec_e_Resid_4                      : REAL := 0.0;   (* Innovation residual 4 *)
    rVec_e_Resid_5                      : REAL := 0.0;   (* Innovation residual 5 *)
    rVec_e_Resid_6                      : REAL := 0.0;   (* Innovation residual 6 *)
""")

    # Declare Matrix A (12x12), B (12x4), C (6x12), D (6x4), L (12x6)
    out.append("    (* SECTION 2: 12x12 DISCRETE STATE TRANSITION MATRIX Ad DECLARATIONS *)")
    for i in range(1, 13):
        for j in range(1, 13):
            out.append(f"    rMat_Ad_{i}_{j} : REAL := 0.0; (* Ad[{i},{j}] *)")

    out.append("\n    (* SECTION 3: 12x4 DISCRETE INPUT COUPLING MATRIX Bd DECLARATIONS *)")
    for i in range(1, 13):
        for j in range(1, 5):
            out.append(f"    rMat_Bd_{i}_{j} : REAL := 0.0; (* Bd[{i},{j}] *)")

    out.append("\n    (* SECTION 4: 6x12 DISCRETE MEASUREMENT MATRIX Cd DECLARATIONS *)")
    for i in range(1, 7):
        for j in range(1, 13):
            out.append(f"    rMat_Cd_{i}_{j} : REAL := 0.0; (* Cd[{i},{j}] *)")

    out.append("\n    (* SECTION 5: 6x4 DISCRETE DIRECT FEEDTHROUGH MATRIX Dd DECLARATIONS *)")
    for i in range(1, 7):
        for j in range(1, 5):
            out.append(f"    rMat_Dd_{i}_{j} : REAL := 0.0; (* Dd[{i},{j}] *)")

    out.append("\n    (* SECTION 6: 12x6 STEADY-STATE KALMAN FILTER GAIN MATRIX L DECLARATIONS *)")
    for i in range(1, 13):
        for j in range(1, 7):
            out.append(f"    rMat_L_{i}_{j} : REAL := 0.0; (* L[{i},{j}] *)")

    # Declare 100-Point WDS Profile Arrays
    out.append("""
    (* SECTION 7: 100-POINT PARISON WALL THICKNESS DISTRIBUTION (WDS/PWDS) PROFILE ARRAYS *)
    aWDS_Profile_AxialGap_Pct           : ARRAY[0..99] OF REAL; (* Conical Die Core Mandrel Gap Percentage Profile [0..100%] *)
    aWDS_Profile_RadialPWDS_mm          : ARRAY[0..99] OF REAL; (* Radial Partial Core Ovalization Displacement Profile [-3.5..+3.5 mm] *)
    aWDS_Profile_TargetWeight_g         : ARRAY[0..99] OF REAL; (* Cumulative Parison Segment Target Mass Distribution [g] *)
    aWDS_Profile_PreBlow_bar            : ARRAY[0..99] OF REAL; (* Dynamic Synchronized Parison Pre-Blow Pressure Profile [bar] *)
""")

    # Declare MPC Variables
    out.append("    (* SECTION 8: RECEDING-HORIZON MPC OPTIMIZATION TRAJECTORY REGISTERS (10 STEPS, 12 STATES, 4 INPUTS) *)")
    # Horizon state trajectories (h = 0 to 10, states 1 to 12)
    for h in range(11):
        for s in range(1, 13):
            out.append(f"    rMPC_x{s}_H{h} : REAL := 0.0; (* Horizon Step {h} State x{s} *)")

    # Horizon input trajectories (h = 0 to 9, inputs 1 to 4)
    for h in range(10):
        for u in range(1, 5):
            out.append(f"    rMPC_u{u}_H{h} : REAL := 0.0; (* Horizon Step {h} Input u{u} *)")

    # Horizon costate trajectories (h = 0 to 10, costates 1 to 12)
    for h in range(11):
        for s in range(1, 13):
            out.append(f"    rMPC_lambda{s}_H{h} : REAL := 0.0; (* Horizon Step {h} Adjoint Costate lambda{s} *)")

    # Horizon input gradient trajectories (h = 0 to 9, inputs 1 to 4)
    for h in range(10):
        for u in range(1, 5):
            out.append(f"    rMPC_grad_u{u}_H{h} : REAL := 0.0; (* Horizon Step {h} Input Gradient grad_u{u} *)")

    # Reference setpoints & weighting matrices
    out.append("""
    (* MPC Reference Trajectory Targets *)
    rRef_x1_TipPos_mm                   : REAL := 0.0;
    rRef_x2_SagStrain                   : REAL := 0.05;
    rRef_x3_SwellRatio                  : REAL := 1.45;
    rRef_x4_MeltTemp_C                  : REAL := 210.0;
    rRef_x5_InnerHDPE_mm                : REAL := 3.20;
    rRef_x6_EVOH_mm                     : REAL := 0.180;
    rRef_x7_DieGap_mm                   : REAL := 4.50;
    rRef_x8_HeadPress_bar               : REAL := 185.0;
    rRef_x9_PreBlow_bar                 : REAL := 0.35;
    rRef_x10_WeldTemp_C                 : REAL := 205.0;
    rRef_x11_MoldN2_bar                 : REAL := 12.0;
    rRef_x12_HeatFlux_kWm2              : REAL := 45.0;

    rRef_u1_ServoSpool_Pct              : REAL := 0.0;
    rRef_u2_MasterSpeed_RPM             : REAL := 65.0;
    rRef_u3_PreBlowN2_Pct               : REAL := 35.0;
    rRef_u4_MoldCooling_Pct             : REAL := 80.0;

    (* MPC Quadratic Weights (Diagonal Q, R, S, P) *)
    rMPC_Weight_Q_1                     : REAL := 1.50;  (* Q11: Tip position tracking penalty *)
    rMPC_Weight_Q_2                     : REAL := 25.0;  (* Q22: Sag strain suppression penalty *)
    rMPC_Weight_Q_3                     : REAL := 15.0;  (* Q33: Die swell deviation penalty *)
    rMPC_Weight_Q_4                     : REAL := 0.85;  (* Q44: Melt temperature deviation penalty *)
    rMPC_Weight_Q_5                     : REAL := 50.0;  (* Q55: Inner HDPE thickness regulation *)
    rMPC_Weight_Q_6                     : REAL := 120.0; (* Q66: EVOH barrier thickness regulation *)
    rMPC_Weight_Q_7                     : REAL := 10.0;  (* Q77: Die gap spool position penalty *)
    rMPC_Weight_Q_8                     : REAL := 0.25;  (* Q88: Extruder head pressure penalty *)
    rMPC_Weight_Q_9                     : REAL := 40.0;  (* Q99: Pre-blow air pressure penalty *)
    rMPC_Weight_Q_10                    : REAL := 2.50;  (* Q10,10: Pinch-off weld temp penalty *)
    rMPC_Weight_Q_11                    : REAL := 8.00;  (* Q11,11: Mold N2 pressure penalty *)
    rMPC_Weight_Q_12                    : REAL := 1.20;  (* Q12,12: Cavity heat flux penalty *)

    rMPC_Weight_R_1                     : REAL := 0.050; (* R11: Servo spool control effort penalty *)
    rMPC_Weight_R_2                     : REAL := 0.010; (* R22: Extruder speed control effort penalty *)
    rMPC_Weight_R_3                     : REAL := 0.020; (* R33: Pre-blow / N2 valve effort penalty *)
    rMPC_Weight_R_4                     : REAL := 0.015; (* R44: Mold cooling valve effort penalty *)

    rMPC_Weight_S_1                     : REAL := 0.250; (* S11: Servo spool slew rate penalty *)
    rMPC_Weight_S_2                     : REAL := 0.100; (* S22: Extruder speed slew rate penalty *)
    rMPC_Weight_S_3                     : REAL := 0.080; (* S33: Pre-blow / N2 valve slew penalty *)
    rMPC_Weight_S_4                     : REAL := 0.050; (* S44: Mold cooling valve slew penalty *)

    rMPC_Weight_P_1                     : REAL := 5.00;  (* P11: Terminal tip position penalty *)
    rMPC_Weight_P_2                     : REAL := 50.0;  (* P22: Terminal sag strain penalty *)
    rMPC_Weight_P_3                     : REAL := 25.0;  (* P33: Terminal die swell penalty *)
    rMPC_Weight_P_4                     : REAL := 1.50;  (* P44: Terminal melt temp penalty *)
    rMPC_Weight_P_5                     : REAL := 100.0; (* P55: Terminal inner HDPE penalty *)
    rMPC_Weight_P_6                     : REAL := 250.0; (* P66: Terminal EVOH barrier penalty *)
    rMPC_Weight_P_7                     : REAL := 20.0;  (* P77: Terminal die gap penalty *)
    rMPC_Weight_P_8                     : REAL := 0.50;  (* P88: Terminal head pressure penalty *)
    rMPC_Weight_P_9                     : REAL := 80.0;  (* P99: Terminal pre-blow penalty *)
    rMPC_Weight_P_10                    : REAL := 5.00;  (* P10,10: Terminal pinch weld penalty *)
    rMPC_Weight_P_11                    : REAL := 15.0;  (* P11,11: Terminal mold N2 penalty *)
    rMPC_Weight_P_12                    : REAL := 2.50;  (* P12,12: Terminal heat flux penalty *)

    rMPC_Alpha_Step                     : REAL := 0.0025;(* PGD Gradient Descent Step Size *)
    rActuator_u1_Max                    : REAL := 100.0; (* Servo valve max % *)
    rActuator_u1_Min                    : REAL := -100.0;(* Servo valve min % *)
    rActuator_u2_Max                    : REAL := 120.0; (* Master extruder max RPM *)
    rActuator_u2_Min                    : REAL := 0.0;   (* Master extruder min RPM *)
    rActuator_u3_Max                    : REAL := 100.0; (* Pre-blow/N2 valve max % *)
    rActuator_u3_Min                    : REAL := 0.0;   (* Pre-blow/N2 valve min % *)
    rActuator_u4_Max                    : REAL := 100.0; (* Cooling water valve max % *)
    rActuator_u4_Min                    : REAL := 0.0;   (* Cooling water valve min % *)

    rActuator_Slew_u1_Max               : REAL := 15.0;  (* Max allowable servo spool delta % per ms *)
    rActuator_Slew_u2_Max               : REAL := 2.50;  (* Max allowable extruder RPM delta per ms *)
    rActuator_Slew_u3_Max               : REAL := 10.0;  (* Max allowable pre-blow valve delta % per ms *)
    rActuator_Slew_u4_Max               : REAL := 5.00;  (* Max allowable cooling valve delta % per ms *)

    rMPC_u1_Prev                        : REAL := 0.0;   (* Previous applied u1 *)
    rMPC_u2_Prev                        : REAL := 0.0;   (* Previous applied u2 *)
    rMPC_u3_Prev                        : REAL := 0.0;   (* Previous applied u3 *)
    rMPC_u4_Prev                        : REAL := 0.0;   (* Previous applied u4 *)
""")

    # Declare TMR Variables
    out.append("""
    (* SECTION 9: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) DISCREPANCY & HEALTH REGISTERS *)
    (* Channel 1: Die Gap LVDT Sensors *)
    rDiff_DieGap_AB                     : REAL := 0.0;
    rDiff_DieGap_BC                     : REAL := 0.0;
    rDiff_DieGap_CA                     : REAL := 0.0;
    tTimer_DieGap_Discrep_AB            : REAL := 0.0;
    tTimer_DieGap_Discrep_BC            : REAL := 0.0;
    tTimer_DieGap_Discrep_CA            : REAL := 0.0;
    bHealth_DieGap_ChA                  : BOOL := TRUE;
    bHealth_DieGap_ChB                  : BOOL := TRUE;
    bHealth_DieGap_ChC                  : BOOL := TRUE;
    iDegradedMode_DieGap                : INT := 0;      (* 0: 2oo3, 1: 1oo2 AB, 2: 1oo2 BC, 3: 1oo2 CA, 4: Fail-Safe *)
    rVoted_DieGap_mm                    : REAL := 4.50;
    bFailSafe_DieGap_Freeze             : BOOL := FALSE;

    (* Channel 2: Co-Extrusion Melt Pressure Transducers *)
    rDiff_MeltPress_AB                  : REAL := 0.0;
    rDiff_MeltPress_BC                  : REAL := 0.0;
    rDiff_MeltPress_CA                  : REAL := 0.0;
    tTimer_MeltPress_Discrep_AB         : REAL := 0.0;
    tTimer_MeltPress_Discrep_BC         : REAL := 0.0;
    tTimer_MeltPress_Discrep_CA         : REAL := 0.0;
    bHealth_MeltPress_ChA               : BOOL := TRUE;
    bHealth_MeltPress_ChB               : BOOL := TRUE;
    bHealth_MeltPress_ChC               : BOOL := TRUE;
    iDegradedMode_MeltPress             : INT := 0;
    rVoted_MeltPressure_bar             : REAL := 185.0;
    bFailSafe_MeltPress_Trip            : BOOL := FALSE;

    (* Channel 3: Die Orifice IR Melt Pyrometers *)
    rDiff_DieTemp_AB                    : REAL := 0.0;
    rDiff_DieTemp_BC                    : REAL := 0.0;
    rDiff_DieTemp_CA                    : REAL := 0.0;
    tTimer_DieTemp_Discrep_AB           : REAL := 0.0;
    tTimer_DieTemp_Discrep_BC           : REAL := 0.0;
    tTimer_DieTemp_Discrep_CA           : REAL := 0.0;
    bHealth_DieTemp_ChA                 : BOOL := TRUE;
    bHealth_DieTemp_ChB                 : BOOL := TRUE;
    bHealth_DieTemp_ChC                 : BOOL := TRUE;
    iDegradedMode_DieTemp               : INT := 0;
    rVoted_DieMeltTemp_C                : REAL := 210.0;
    bFailSafe_DieTemp_Trip              : BOOL := FALSE;

    (* Channel 4: Mold Cavity Nitrogen Gas Pressure Transducers *)
    rDiff_MoldN2_AB                     : REAL := 0.0;
    rDiff_MoldN2_BC                     : REAL := 0.0;
    rDiff_MoldN2_CA                     : REAL := 0.0;
    tTimer_MoldN2_Discrep_AB            : REAL := 0.0;
    tTimer_MoldN2_Discrep_BC            : REAL := 0.0;
    tTimer_MoldN2_Discrep_CA            : REAL := 0.0;
    bHealth_MoldN2_ChA                  : BOOL := TRUE;
    bHealth_MoldN2_ChB                  : BOOL := TRUE;
    bHealth_MoldN2_ChC                  : BOOL := TRUE;
    iDegradedMode_MoldN2                : INT := 0;
    rVoted_MoldN2Pressure_bar           : REAL := 0.0;
    bFailSafe_MoldN2_Trip               : BOOL := FALSE;

    (* TMR Discrepancy Tolerance Limits & Trip Thresholds *)
    rTol_DieGap_Discrep_mm              : REAL := 0.25;  (* Max allowable LVDT gap deviation [mm] *)
    rTol_MeltPress_Discrep_bar          : REAL := 15.0;  (* Max allowable melt pressure deviation [bar] *)
    rTol_DieTemp_Discrep_C              : REAL := 5.00;  (* Max allowable IR temperature deviation [deg C] *)
    rTol_MoldN2_Discrep_bar             : REAL := 0.85;  (* Max allowable mold N2 pressure deviation [bar] *)
    rPersistence_TMR_Limit_s            : REAL := 0.015; (* 15 ms persistence timer limit [s] *)
""")

    # Declare Polymer Rheology Variables
    out.append("""
    (* SECTION 10: POLYMER RHEOLOGICAL & CYBER-PHYSICAL INTERNAL REGISTERS *)
    rNominal_Die_Diameter_mm            : REAL := 280.0;  (* Annular Die Bushing Outside Diameter [mm] *)
    rMelt_Density_kg_m3                 : REAL := 760.0;  (* Molten HDPE Melt Density at 210 deg C [kg/m3] *)
    rThermal_Conductivity_HDPE          : REAL := 0.245;  (* HDPE Melt Thermal Conductivity [W/(m*K)] *)
    rSpecific_Heat_HDPE                 : REAL := 2400.0; (* HDPE Melt Specific Heat Capacity [J/(kg*K)] *)
    rNominal_Wall_Thickness_m           : REAL := 0.0055; (* Baseline Finished Tank Shell Wall Thickness [m] *)
    rCross_Sectional_Area_m2            : REAL := 0.0048; (* Parison Annular Melt Flow Area [m2] *)
    rWall_Shear_Stress_tau_w            : REAL := 85000.0;(* Die Wall Shear Stress [Pa] *)
    rWeissenberg_Number_Wi              : REAL := 2.85;   (* Polymer Elastic Weissenberg Number *)
    rFirst_Normal_Stress_N1             : REAL := 0.0;    (* First Normal Stress Difference [Pa] *)
    rDie_Swell_Ratio_B                  : REAL := 1.45;   (* Tanner Elastic Recovery Swell Ratio *)
    rVisc_A1                            : REAL := 18500.0;(* Cross-WLF Viscosity Parameter A1 [Pa*s] *)
    rVisc_A2                            : REAL := 28.5;   (* Cross-WLF Viscosity Parameter A2 [dimensionless] *)
    rVisc_A3                            : REAL := 51.6;   (* Cross-WLF Viscosity Parameter A3 [K] *)
    rVisc_T_ref                         : REAL := 190.0;  (* Cross-WLF Reference Melt Temperature [deg C] *)
    rRelaxation_Time_lambda             : REAL := 1.25;   (* Characteristic Polymer Relaxation Time [s] *)
    rShear_Rate_gamma_dot               : REAL := 125.0;  (* Die Orifice Apparent Shear Rate [1/s] *)
    rPower_Law_Index_n                  : REAL := 0.38;   (* Cross Model Pseudoplastic Shear-Thinning Exponent *)
    rZero_Shear_Viscosity_eta0          : REAL := 0.0;    (* Zero-Shear Viscosity [Pa*s] *)
    rApparent_Viscosity_eta             : REAL := 0.0;    (* Effective Apparent Shear Viscosity [Pa*s] *)
    rParison_Mass_Hanging_kg            : REAL := 0.0;    (* Cumulative Extruded Parison Hanging Weight [kg] *)
    rAxial_Gravity_Stress_Pa            : REAL := 0.0;    (* Parison Tensile Sag Gravitational Stress [Pa] *)
    rElongational_Viscosity_Pa_s        : REAL := 0.0;    (* Trouton Elongational Extensional Viscosity [Pa*s] *)
    rSag_Strain_Rate_per_s              : REAL := 0.0;    (* Instantaneous Parison Creep Strain Rate [1/s] *)
    rDieSwell_Proxy_Diameter_mm         : REAL := 385.0;  (* Voted Parison Free-Hanging Outer Diameter [mm] *)
""")

    # Declare FSM Sequencer Variables
    out.append("""
    (* SECTION 11: DETERMINISTIC 14-STAGE FINITE STATE MACHINE (FSM) SEQUENCER REGISTERS *)
    iFSM_State_Current                  : INT := 0;      (* Active Production Sequencer Stage [0..13] *)
    iFSM_State_Next                     : INT := 0;      (* Pending Production Sequencer Stage [0..13] *)
    rFSM_State_Elapsed_s                : REAL := 0.0;   (* Time Spent in Current FSM Stage [s] *)
    rFSM_Cycle_Elapsed_s                : REAL := 0.0;   (* Total Elapsed Production Cycle Duration [s] *)
    bFSM_Stage_Entry_Strobe             : BOOL := TRUE;  (* First-Scan One-Shot Pulse on State Entry *)
    iFSM_Cycle_Counter                  : DINT := 0;     (* Completed Fuel Tank Production Batch Counter *)

    (* Stage Watchdog Timeout Constants [s] *)
    rTimeout_Stage_01_Homog_s           : REAL := 120.0; (* Melt temperature homogenization timeout *)
    rTimeout_Stage_02_ZeroSeek_s        : REAL := 15.0;  (* Tooling gap zero calibration timeout *)
    rTimeout_Stage_03_ExtrudeRamp_s     : REAL := 25.0;  (* Extrusion throughput ramp-up timeout *)
    rTimeout_Stage_04_WDSSync_s         : REAL := 45.0;  (* 100-Point WDS drop profile completion timeout *)
    rTimeout_Stage_05_PreBlow_s         : REAL := 5.0;   (* Parison internal pre-blow shaping timeout *)
    rTimeout_Stage_06_PrePinch_s        : REAL := 8.0;   (* Bottom pre-pinch robotic manipulation timeout *)
    rTimeout_Stage_07_ClampLock_s       : REAL := 10.0;  (* Mold closing & tie-bar high-tonnage lock timeout *)
    rTimeout_Stage_08_N2Blow_s          : REAL := 12.0;  (* High-pressure nitrogen blow pin inflation timeout *)
    rTimeout_Stage_09_InMoldCool_s      : REAL := 90.0;  (* In-mold cryogenic nitrogen cooling soak timeout *)
    rTimeout_Stage_10_Exhaust_s         : REAL := 10.0;  (* Cavity fast exhaust depressurization timeout *)
    rTimeout_Stage_11_Demold_s          : REAL := 15.0;  (* Mold unclamping & robotic part extraction timeout *)
    rTimeout_Stage_12_Deflash_s         : REAL := 20.0;  (* Flash punch guillotine trimming press timeout *)
""")

    # Declare ISA-18.2 Process Alarm Variables
    out.append("""
    (* SECTION 12: ANSI/ISA-18.2 MULTI-TIERED PROCESS ALARM ENGINE REGISTERS *)
    (* Alarm Thresholds: HH (Trip), H (Warning), L (Low Warning), LL (Low Trip) *)
    rThresh_DieGap_Err_HH_mm            : REAL := 0.60;
    rThresh_DieGap_Err_H_mm             : REAL := 0.30;
    rThresh_MeltPress_HH_bar            : REAL := 265.0;
    rThresh_MeltPress_H_bar             : REAL := 235.0;
    rThresh_MeltPress_L_bar             : REAL := 120.0;
    rThresh_MeltPress_LL_bar            : REAL := 85.0;
    rThresh_DieTemp_HH_C                : REAL := 235.0;
    rThresh_DieTemp_H_C                 : REAL := 222.0;
    rThresh_DieTemp_L_C                 : REAL := 195.0;
    rThresh_DieTemp_LL_C                : REAL := 182.0;
    rThresh_MoldN2_HH_bar               : REAL := 16.5;
    rThresh_MoldN2_H_bar                : REAL := 14.5;
    rThresh_MoldN2_L_bar                : REAL := 9.5;
    rThresh_MoldN2_LL_bar               : REAL := 7.0;
    rThresh_HPU_Press_LL_bar            : REAL := 140.0;
    rThresh_HPU_Press_L_bar             : REAL := 165.0;
    rThresh_HPU_Temp_HH_C               : REAL := 65.0;
    rThresh_HPU_Temp_H_C                : REAL := 55.0;
    rThresh_CoolingWater_Temp_HH_C      : REAL := 22.0;
    rThresh_CoolingWater_Temp_H_C       : REAL := 16.0;
    rThresh_CoolingWater_Flow_LL_Lpm    : REAL := 180.0;
    rThresh_CoolingWater_Flow_L_Lpm     : REAL := 240.0;
    rThresh_ClampTonnage_LL_kN          : REAL := 18500.0;
    rThresh_ClampTonnage_L_kN           : REAL := 22000.0;

    (* Deadband Hysteresis Values *)
    rDeadband_DieGap_mm                 : REAL := 0.05;
    rDeadband_MeltPress_bar             : REAL := 3.0;
    rDeadband_DieTemp_C                 : REAL := 1.5;
    rDeadband_MoldN2_bar                : REAL := 0.25;
    rDeadband_HPU_Press_bar             : REAL := 4.0;
    rDeadband_HPU_Temp_C                : REAL := 1.0;
    rDeadband_Cooling_Temp_C            : REAL := 0.8;
    rDeadband_Cooling_Flow_Lpm          : REAL := 10.0;
    rDeadband_ClampTonnage_kN           : REAL := 500.0;

    (* Persistence Debounce Timers [s] *)
    rTimer_Alarm_DieGap_HH              : REAL := 0.0;
    rTimer_Alarm_DieGap_H               : REAL := 0.0;
    rTimer_Alarm_MeltPress_HH           : REAL := 0.0;
    rTimer_Alarm_MeltPress_H            : REAL := 0.0;
    rTimer_Alarm_MeltPress_L            : REAL := 0.0;
    rTimer_Alarm_MeltPress_LL           : REAL := 0.0;
    rTimer_Alarm_DieTemp_HH             : REAL := 0.0;
    rTimer_Alarm_DieTemp_H              : REAL := 0.0;
    rTimer_Alarm_DieTemp_L              : REAL := 0.0;
    rTimer_Alarm_DieTemp_LL             : REAL := 0.0;
    rTimer_Alarm_MoldN2_HH              : REAL := 0.0;
    rTimer_Alarm_MoldN2_H               : REAL := 0.0;
    rTimer_Alarm_MoldN2_L               : REAL := 0.0;
    rTimer_Alarm_MoldN2_LL              : REAL := 0.0;
    rTimer_Alarm_HPU_Press_LL           : REAL := 0.0;
    rTimer_Alarm_HPU_Temp_HH            : REAL := 0.0;
    rTimer_Alarm_Cooling_Temp_HH        : REAL := 0.0;
    rTimer_Alarm_Cooling_Flow_LL        : REAL := 0.0;
    rTimer_Alarm_ClampTonnage_LL        : REAL := 0.0;

    (* Latched Alarm Flags *)
    bLatch_Alarm_DieGap_HH              : BOOL := FALSE;
    bLatch_Alarm_DieGap_H               : BOOL := FALSE;
    bLatch_Alarm_MeltPress_HH           : BOOL := FALSE;
    bLatch_Alarm_MeltPress_H            : BOOL := FALSE;
    bLatch_Alarm_MeltPress_L            : BOOL := FALSE;
    bLatch_Alarm_MeltPress_LL           : BOOL := FALSE;
    bLatch_Alarm_DieTemp_HH             : BOOL := FALSE;
    bLatch_Alarm_DieTemp_H              : BOOL := FALSE;
    bLatch_Alarm_DieTemp_L              : BOOL := FALSE;
    bLatch_Alarm_DieTemp_LL             : BOOL := FALSE;
    bLatch_Alarm_MoldN2_HH              : BOOL := FALSE;
    bLatch_Alarm_MoldN2_H               : BOOL := FALSE;
    bLatch_Alarm_MoldN2_L               : BOOL := FALSE;
    bLatch_Alarm_MoldN2_LL              : BOOL := FALSE;
    bLatch_Alarm_HPU_Press_LL           : BOOL := FALSE;
    bLatch_Alarm_HPU_Temp_HH            : BOOL := FALSE;
    bLatch_Alarm_Cooling_Temp_HH        : BOOL := FALSE;
    bLatch_Alarm_Cooling_Flow_LL        : BOOL := FALSE;
    bLatch_Alarm_ClampTonnage_LL        : BOOL := FALSE;
    bLatch_Alarm_TMR_Discrepancy        : BOOL := FALSE;
    bLatch_Alarm_Watchdog_Timeout       : BOOL := FALSE;

    (* Math & Scratch Temporary Registers *)
    rScratch_Interpol_Frac              : REAL := 0.0;
    iScratch_Index_Low                  : INT := 0;
    iScratch_Index_High                 : INT := 0;
    rScratch_Target_Gap_Pct             : REAL := 0.0;
    rScratch_Target_PWDS_mm             : REAL := 0.0;
    rScratch_Target_PreBlow_bar         : REAL := 0.0;
    rScratch_Active_Index_Real          : REAL := 0.0;
    rScratch_Slew_Delta                 : REAL := 0.0;
    rScratch_Grad_Val                   : REAL := 0.0;
    rScratch_State_Delta                : REAL := 0.0;
END_VAR
""")

    # -------------------------------------------------------------------------
    # PHASE 0: SYSTEM INITIALIZATION & 100-POINT WDS PROFILE TABLE LOADING
    # -------------------------------------------------------------------------
    out.append("""
(* ==================================================================================================================== *)
(* PHASE 0: REAL-TIME TIMEKEEPING, COLD-START MATRIX INITIALIZATION & 100-POINT WDS PROFILE LOADING                     *)
(* ==================================================================================================================== *)

(* Monotonic Master Clock Advance *)
rMaster_Clock_Seconds := rMaster_Clock_Seconds + rCycle_Time_s;

(* Execute One-Time Deterministic Cold-Start Initialization *)
IF NOT bInitialized THEN
    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* SUB-PHASE 0.1: POPULATION OF 12x12 DISCRETE STATE TRANSITION MATRIX Ad (Ts = 1.0 ms)                              *)
    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* State 1: Parison tip vertical position [mm] *)
    rMat_Ad_1_1  := 0.99850; (* Tip velocity kinematic integration pole *)
    rMat_Ad_1_2  := 12.5000; (* Viscoelastic sag elongation strain downward acceleration *)
    rMat_Ad_1_3  := 0.45000; (* Die swell relaxation coupling *)
    rMat_Ad_1_4  := 0.08500; (* Melt temperature thermal expansion effect *)
    rMat_Ad_1_5  := 0.00000;
    rMat_Ad_1_6  := 0.00000;
    rMat_Ad_1_7  := 2.45000; (* Tooling die gap opening feed rate gain *)
    rMat_Ad_1_8  := 0.12500; (* Extruder head pressure extrusion drive *)
    rMat_Ad_1_9  := 0.00000;
    rMat_Ad_1_10 := 0.00000;
    rMat_Ad_1_11 := 0.00000;
    rMat_Ad_1_12 := 0.00000;

    (* State 2: Parison sag elongation strain [mm/mm] *)
    rMat_Ad_2_1  := 0.00012; (* Hanging weight accumulation from parison length *)
    rMat_Ad_2_2  := 0.99400; (* Viscoelastic strain relaxation damping *)
    rMat_Ad_2_3  := -0.0050; (* Cross-sectional swell tension attenuation *)
    rMat_Ad_2_4  := 0.00035; (* Arrhenius temperature softening acceleration *)
    rMat_Ad_2_5  := 0.00010; (* Wall mass loading *)
    rMat_Ad_2_6  := 0.00000;
    rMat_Ad_2_7  := 0.00080; (* Die gap mass flow rate coupling *)
    rMat_Ad_2_8  := 0.00005;
    rMat_Ad_2_9  := -0.0012; (* Internal pre-blow pressure hooping stiffness *)
    rMat_Ad_2_10 := 0.00000;
    rMat_Ad_2_11 := 0.00000;
    rMat_Ad_2_12 := 0.00000;

    (* State 3: Radial die swell ratio [dimensionless] *)
    rMat_Ad_3_1  := 0.00000;
    rMat_Ad_3_2  := -0.0150; (* Axial draw thinning cross-coupling *)
    rMat_Ad_3_3  := 0.98500; (* First normal stress elastic memory relaxation *)
    rMat_Ad_3_4  := -0.0012; (* Melt temperature viscosity reduction *)
    rMat_Ad_3_5  := 0.00500;
    rMat_Ad_3_6  := 0.00100;
    rMat_Ad_3_7  := 0.04500; (* Tooling gap shear rate dependency *)
    rMat_Ad_3_8  := 0.00085; (* Head melt pressure elasticity driving force *)
    rMat_Ad_3_9  := 0.00000;
    rMat_Ad_3_10 := 0.00000;
    rMat_Ad_3_11 := 0.00000;
    rMat_Ad_3_12 := 0.00000;

    (* State 4: Melt temperature at die exit [deg C] *)
    rMat_Ad_4_1  := 0.00000;
    rMat_Ad_4_2  := 0.00000;
    rMat_Ad_4_3  := 0.00000;
    rMat_Ad_4_4  := 0.99700; (* Extrusion head thermal mass dissipation *)
    rMat_Ad_4_5  := 0.00000;
    rMat_Ad_4_6  := 0.00000;
    rMat_Ad_4_7  := -0.0150; (* Tooling gap throttle expansion cooling *)
    rMat_Ad_4_8  := 0.01250; (* Viscous shear dissipation heating *)
    rMat_Ad_4_9  := -0.0020; (* Internal pre-blow convective heat loss *)
    rMat_Ad_4_10 := 0.00000;
    rMat_Ad_4_11 := 0.00000;
    rMat_Ad_4_12 := 0.00000;

    (* State 5: Inner layer HDPE thickness [mm] *)
    rMat_Ad_5_1  := -0.0002; (* Axial drawdown thinning *)
    rMat_Ad_5_2  := -0.0850; (* Tensile sag elongation thinning *)
    rMat_Ad_5_3  := 0.02500; (* Die swell radial thickening *)
    rMat_Ad_5_4  := -0.0015;
    rMat_Ad_5_5  := 0.99200; (* Layer volumetric continuity pole *)
    rMat_Ad_5_6  := 0.00000;
    rMat_Ad_5_7  := 0.28500; (* Tooling gap opening volumetric gain *)
    rMat_Ad_5_8  := 0.00450;
    rMat_Ad_5_9  := -0.0150; (* Pre-blow hoop expansion thinning *)
    rMat_Ad_5_10 := 0.00000;
    rMat_Ad_5_11 := 0.00000;
    rMat_Ad_5_12 := 0.00000;

    (* State 6: EVOH barrier layer thickness [mm] *)
    rMat_Ad_6_1  := -0.00002;
    rMat_Ad_6_2  := -0.00650;
    rMat_Ad_6_3  := 0.00180;
    rMat_Ad_6_4  := -0.00010;
    rMat_Ad_6_5  := 0.00000;
    rMat_Ad_6_6  := 0.99100; (* EVOH layer continuity pole *)
    rMat_Ad_6_7  := 0.03500; (* Tooling gap co-ex layer feed gain *)
    rMat_Ad_6_8  := 0.00035;
    rMat_Ad_6_9  := -0.00120;
    rMat_Ad_6_10 := 0.00000;
    rMat_Ad_6_11 := 0.00000;
    rMat_Ad_6_12 := 0.00000;

    (* State 7: Die gap hydraulic servo spool position [mm] *)
    rMat_Ad_7_1  := 0.00000;
    rMat_Ad_7_2  := 0.00000;
    rMat_Ad_7_3  := 0.00000;
    rMat_Ad_7_4  := 0.00000;
    rMat_Ad_7_5  := 0.00000;
    rMat_Ad_7_6  := 0.00000;
    rMat_Ad_7_7  := 0.96500; (* High-speed hydraulic servo closed-loop pole (75 Hz bandwidth) *)
    rMat_Ad_7_8  := -0.00050;(* Hydraulic backpressure reaction *)
    rMat_Ad_7_9  := 0.00000;
    rMat_Ad_7_10 := 0.00000;
    rMat_Ad_7_11 := 0.00000;
    rMat_Ad_7_12 := 0.00000;

    (* State 8: Extruder head melt pressure [bar] *)
    rMat_Ad_8_1  := 0.00000;
    rMat_Ad_8_2  := 0.00000;
    rMat_Ad_8_3  := 0.00000;
    rMat_Ad_8_4  := -0.15000;(* Thermal viscosity reduction depressurization *)
    rMat_Ad_8_5  := 0.00000;
    rMat_Ad_8_6  := 0.00000;
    rMat_Ad_8_7  := -1.85000;(* Tooling gap opening flow relief *)
    rMat_Ad_8_8  := 0.97800; (* Polymer melt compressibility & die resistance pole *)
    rMat_Ad_8_9  := 0.00000;
    rMat_Ad_8_10 := 0.00000;
    rMat_Ad_8_11 := 0.00000;
    rMat_Ad_8_12 := 0.00000;

    (* State 9: Parison internal pre-blow pressure [bar] *)
    rMat_Ad_9_1  := -0.00010;(* Volume expansion from parison drop *)
    rMat_Ad_9_2  := 0.00000;
    rMat_Ad_9_3  := 0.00000;
    rMat_Ad_9_4  := 0.00050; (* Thermal gas expansion *)
    rMat_Ad_9_5  := 0.00000;
    rMat_Ad_9_6  := 0.00000;
    rMat_Ad_9_7  := 0.00000;
    rMat_Ad_9_8  := 0.00000;
    rMat_Ad_9_9  := 0.98200; (* Pneumatic chamber leakage and volume expansion pole *)
    rMat_Ad_9_10 := 0.00000;
    rMat_Ad_9_11 := 0.00000;
    rMat_Ad_9_12 := 0.00000;

    (* State 10: Parison pinch-off weld line temperature [deg C] *)
    rMat_Ad_10_1 := -0.00250;(* Ambient convective cooling during parison drop *)
    rMat_Ad_10_2 := 0.00000;
    rMat_Ad_10_3 := 0.00000;
    rMat_Ad_10_4 := 0.00450; (* Melt temperature propagation to pinch zone *)
    rMat_Ad_10_5 := 0.00000;
    rMat_Ad_10_6 := 0.00000;
    rMat_Ad_10_7 := 0.00000;
    rMat_Ad_10_8 := 0.00000;
    rMat_Ad_10_9 := 0.00000;
    rMat_Ad_10_10:= 0.99500; (* Pinch zone thermal inertia pole *)
    rMat_Ad_10_11:= 0.00000;
    rMat_Ad_10_12:= 0.00000;

    (* State 11: Mold cavity nitrogen inflation pressure [bar] *)
    rMat_Ad_11_1 := 0.00000;
    rMat_Ad_11_2 := 0.00000;
    rMat_Ad_11_3 := 0.00000;
    rMat_Ad_11_4 := 0.00000;
    rMat_Ad_11_5 := 0.00000;
    rMat_Ad_11_6 := 0.00000;
    rMat_Ad_11_7 := 0.00000;
    rMat_Ad_11_8 := 0.00000;
    rMat_Ad_11_9 := 0.00000;
    rMat_Ad_11_10:= 0.00000;
    rMat_Ad_11_11:= 0.99000; (* Cavity N2 compressibility & seal leakage pole *)
    rMat_Ad_11_12:= 0.00000;

    (* State 12: Mold cavity cooling surface heat flux [kW/m2] *)
    rMat_Ad_12_1 := 0.00000;
    rMat_Ad_12_2 := 0.00000;
    rMat_Ad_12_3 := 0.00000;
    rMat_Ad_12_4 := 0.08500; (* Thermal driving gradient from melt *)
    rMat_Ad_12_5 := -0.25000;(* Wall thickness thermal resistance *)
    rMat_Ad_12_6 := 0.00000;
    rMat_Ad_12_7 := 0.00000;
    rMat_Ad_12_8 := 0.00000;
    rMat_Ad_12_9 := 0.00000;
    rMat_Ad_12_10:= 0.00000;
    rMat_Ad_12_11:= 1.25000; (* Contact heat transfer coefficient enhancement by N2 pressure *)
    rMat_Ad_12_12:= 0.97500; (* Mold steel boundary layer thermal decay pole *)

    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* SUB-PHASE 0.2: POPULATION OF 12x4 DISCRETE INPUT COUPLING MATRIX Bd (Ts = 1.0 ms)                                *)
    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* Row 1: Parison tip position *)
    rMat_Bd_1_1  := 0.01500; (* Servo valve spool direct velocity feed *)
    rMat_Bd_1_2  := 0.42000; (* Extruder screw RPM feed velocity *)
    rMat_Bd_1_3  := 0.00000;
    rMat_Bd_1_4  := 0.00000;

    (* Row 2: Parison sag elongation strain *)
    rMat_Bd_2_1  := 0.00005;
    rMat_Bd_2_2  := 0.00250; (* Throughput mass addition to hanging parison *)
    rMat_Bd_2_3  := -0.00080;(* Pre-blow air pressure hooping *)
    rMat_Bd_2_4  := 0.00000;

    (* Row 3: Radial die swell ratio *)
    rMat_Bd_3_1  := 0.00250; (* Servo gap velocity dynamic shear transient *)
    rMat_Bd_3_2  := 0.00180; (* Screw RPM shear rate increase *)
    rMat_Bd_3_3  := 0.00000;
    rMat_Bd_3_4  := 0.00000;

    (* Row 4: Die exit melt temperature *)
    rMat_Bd_4_1  := -0.00050;
    rMat_Bd_4_2  := 0.01500; (* Screw mechanical work viscous shear heating *)
    rMat_Bd_4_3  := -0.00150;(* Pre-blow internal air cooling *)
    rMat_Bd_4_4  := 0.00000;

    (* Row 5: Inner HDPE layer thickness *)
    rMat_Bd_5_1  := 0.02850; (* Servo gap spool opening direct gain *)
    rMat_Bd_5_2  := 0.00850; (* Extruder screw throughput gain *)
    rMat_Bd_5_3  := -0.00250;(* Pre-blow thinning *)
    rMat_Bd_5_4  := 0.00000;

    (* Row 6: EVOH barrier layer thickness *)
    rMat_Bd_6_1  := 0.00350;
    rMat_Bd_6_2  := 0.00120;
    rMat_Bd_6_3  := -0.00025;
    rMat_Bd_6_4  := 0.00000;

    (* Row 7: Die gap hydraulic servo spool position *)
    rMat_Bd_7_1  := 0.12500; (* Direct servo valve command to spool displacement gain *)
    rMat_Bd_7_2  := 0.00000;
    rMat_Bd_7_3  := 0.00000;
    rMat_Bd_7_4  := 0.00000;

    (* Row 8: Extruder head melt pressure *)
    rMat_Bd_8_1  := -0.22000;(* Servo gap opening pressure relief *)
    rMat_Bd_8_2  := 1.65000; (* Screw speed positive displacement pumping gain *)
    rMat_Bd_8_3  := 0.00000;
    rMat_Bd_8_4  := 0.00000;

    (* Row 9: Parison internal pre-blow pressure *)
    rMat_Bd_9_1  := 0.00000;
    rMat_Bd_9_2  := 0.00000;
    rMat_Bd_9_3  := 0.08500; (* Pre-blow air servo valve proportional gain *)
    rMat_Bd_9_4  := 0.00000;

    (* Row 10: Pinch-off weld line temperature *)
    rMat_Bd_10_1 := 0.00000;
    rMat_Bd_10_2 := 0.00500; (* Faster extrusion delivers warmer melt to pinch line *)
    rMat_Bd_10_3 := -0.00100;
    rMat_Bd_10_4 := 0.00000;

    (* Row 11: Mold cavity nitrogen inflation pressure *)
    rMat_Bd_11_1 := 0.00000;
    rMat_Bd_11_2 := 0.00000;
    rMat_Bd_11_3 := 0.18500; (* High-pressure N2 servo valve direct pressurization *)
    rMat_Bd_11_4 := 0.00000;

    (* Row 12: Mold cavity cooling surface heat flux *)
    rMat_Bd_12_1 := 0.00000;
    rMat_Bd_12_2 := 0.00000;
    rMat_Bd_12_3 := 0.05000;
    rMat_Bd_12_4 := 0.85000; (* Mold chilled water valve convective heat flux gain *)

    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* SUB-PHASE 0.3: POPULATION OF 6x12 DISCRETE MEASUREMENT MATRIX Cd                                                 *)
    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* Output 1: Parison tip vertical position [mm] *)
    rMat_Cd_1_1  := 1.00000;
    (* Output 2: Parison swell diameter / wall thickness proxy [mm] *)
    rMat_Cd_2_3  := 85.0000; (* Swell ratio to diameter sensitivity *)
    rMat_Cd_2_5  := 12.0000; (* Wall thickness component *)
    rMat_Cd_2_7  := 5.20000; (* Tooling gap component *)
    (* Output 3: Die exit melt temperature [deg C] *)
    rMat_Cd_3_4  := 1.00000;
    (* Output 4: Die head melt pressure [bar] *)
    rMat_Cd_4_8  := 1.00000;
    (* Output 5: Parison internal / mold cavity pressure [bar] *)
    rMat_Cd_5_9  := 1.00000; (* Pre-blow pressure *)
    rMat_Cd_5_11 := 1.00000; (* High-pressure N2 inflation *)
    (* Output 6: Die gap servo LVDT position [mm] *)
    rMat_Cd_6_7  := 1.00000;

    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* SUB-PHASE 0.4: POPULATION OF 6x4 DIRECT FEEDTHROUGH MATRIX Dd                                                    *)
    (* ---------------------------------------------------------------------------------------------------------------- *)
    rMat_Dd_5_3  := 0.00500; (* Minor pneumatic valve acoustic ripple *)

    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* SUB-PHASE 0.5: POPULATION OF 12x6 STEADY-STATE KALMAN FILTER GAIN MATRIX L                                       *)
    (* ---------------------------------------------------------------------------------------------------------------- *)
    rMat_L_1_1   := 0.45000; rMat_L_1_2   := 0.00200; rMat_L_1_6   := 0.01500;
    rMat_L_2_1   := 0.00085; rMat_L_2_2   := 0.00550; rMat_L_2_4   := 0.00010;
    rMat_L_3_2   := 0.00850; rMat_L_3_3   := -0.0002; rMat_L_3_4   := 0.00015;
    rMat_L_4_3   := 0.35000; rMat_L_4_4   := 0.00850;
    rMat_L_5_2   := 0.01500; rMat_L_5_6   := 0.04500;
    rMat_L_6_2   := 0.00180; rMat_L_6_6   := 0.00650;
    rMat_L_7_6   := 0.65000; (* Strong LVDT feedback to servo spool state *)
    rMat_L_8_4   := 0.55000; (* Melt pressure feedback *)
    rMat_L_9_5   := 0.50000; (* Pre-blow pressure feedback *)
    rMat_L_10_3  := 0.08500;
    rMat_L_11_5  := 0.60000; (* Cavity N2 pressure feedback *)
    rMat_L_12_5  := 0.02500;

    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* SUB-PHASE 0.6: POPULATION OF 100-POINT WALL THICKNESS DISTRIBUTION (WDS/PWDS) PROFILE TABLE                     *)
    (* ---------------------------------------------------------------------------------------------------------------- *)
""")

    # Populate all 100 points of the WDS profile with rich realistic engineering data!
    for i in range(100):
        # Determine geometric feature of the automotive fuel tank based on point index
        if i <= 5:
            # Bottom pinch-off weld zone: thick wall, low pre-blow, high strength
            gap = 42.5 + (i * 0.5)
            pwds = 0.15 + (i * 0.02)
            wt = 115.0 + (i * 1.5)
            pb = 0.20 + (i * 0.01)
            desc = "Bottom Pinch Weld Zone - High Impact Integrity"
        elif i <= 18:
            # Lower tank shell & swirl pot fuel pump sump
            gap = 34.0 + ((i - 6) * 0.35)
            pwds = 0.50 + ((i - 6) * 0.05)
            wt = 96.0 + ((i - 6) * 0.8)
            pb = 0.28 + ((i - 6) * 0.005)
            desc = "Lower Reservoir & Fuel Pump Swirl Pot Sump"
        elif i <= 35:
            # Main lower tank reservoir body: mass-optimized thinner wall
            gap = 28.5 + ((i - 19) * 0.20)
            pwds = -0.20 + ((i - 19) * 0.03)
            wt = 84.0 + ((i - 19) * 0.4)
            pb = 0.35 + ((i - 19) * 0.002)
            desc = "Main Lower Tank Volume Shell - Lightweight Optimized"
        elif i <= 50:
            # Saddle tank tunnel bridge / propshaft clearance contour: heavy draw zone requiring thick walls
            gap = 56.0 + ((i - 36) * 0.85)
            pwds = 1.85 + ((i - 36) * 0.06)
            wt = 142.0 + ((i - 36) * 1.6)
            pb = 0.24 + ((i - 36) * 0.004)
            desc = "Saddle Propshaft Tunnel Arch - High Draw Ratio Compensation"
        elif i <= 68:
            # Upper reservoir & fuel sender level flange
            gap = 33.5 + ((i - 51) * 0.25)
            pwds = 0.45 + ((i - 51) * 0.03)
            wt = 92.0 + ((i - 51) * 0.6)
            pb = 0.34 + ((i - 51) * 0.002)
            desc = "Upper Reservoir Body & Fuel Sender Flange Land"
        elif i <= 82:
            # Filler pipe neck junction & vent line routing channels
            gap = 48.0 + ((i - 69) * 0.70)
            pwds = 1.30 + ((i - 69) * 0.05)
            wt = 126.0 + ((i - 69) * 1.3)
            pb = 0.28 + ((i - 69) * 0.003)
            desc = "Filler Pipe Neck Junction & Vent Boss Zone"
        elif i <= 95:
            # Top dome & chassis mounting brackets
            gap = 41.0 + ((i - 83) * 0.40)
            pwds = 0.65 + ((i - 83) * 0.04)
            wt = 110.0 + ((i - 83) * 0.8)
            pb = 0.25 + ((i - 83) * 0.002)
            desc = "Upper Dome & Chassis Fastener Lug Reinforcement"
        else:
            # Top flash pinch-off zone
            gap = 31.0 - ((i - 96) * 0.5)
            pwds = 0.05 - ((i - 96) * 0.01)
            wt = 82.0 - ((i - 96) * 1.0)
            pb = 0.15 - ((i - 96) * 0.01)
            desc = "Top Flash Pinch-Off - Trimmer Guillotine Cut Land"

        out.append(f"    aWDS_Profile_AxialGap_Pct[{i}] := {gap:.2f}; aWDS_Profile_RadialPWDS_mm[{i}] := {pwds:.2f}; aWDS_Profile_TargetWeight_g[{i}] := {wt:.1f}; aWDS_Profile_PreBlow_bar[{i}] := {pb:.2f}; (* P{i:02d}: {desc} *)")

    out.append("""
    (* Cold-Start Complete *)
    bInitialized := TRUE;
END_IF;
""")

    # -------------------------------------------------------------------------
    # PHASE 1: 2oo3 TMR SENSOR VOTING WITH 15MS DISCREPANCY TIMERS
    # -------------------------------------------------------------------------
    out.append("""
(* ==================================================================================================================== *)
(* PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING WITH 15 MS DISCREPANCY TIMERS                            *)
(* ==================================================================================================================== *)

(* -------------------------------------------------------------------------------------------------------------------- *)
(* CHANNEL 1: DIE GAP HYDRAULIC PROPORTIONAL SERVO LVDT SENSORS (ChA, ChB, ChC) [mm]                                   *)
(* -------------------------------------------------------------------------------------------------------------------- *)
rDiff_DieGap_AB := ABS(rDieGap_LVDT_ChA_mm_In - rDieGap_LVDT_ChB_mm_In);
rDiff_DieGap_BC := ABS(rDieGap_LVDT_ChB_mm_In - rDieGap_LVDT_ChC_mm_In);
rDiff_DieGap_CA := ABS(rDieGap_LVDT_ChC_mm_In - rDieGap_LVDT_ChA_mm_In);

(* Discrepancy Persistence Integration *)
IF rDiff_DieGap_AB > rTol_DieGap_Discrep_mm THEN
    tTimer_DieGap_Discrep_AB := tTimer_DieGap_Discrep_AB + rCycle_Time_s;
ELSE
    tTimer_DieGap_Discrep_AB := 0.0;
END_IF;

IF rDiff_DieGap_BC > rTol_DieGap_Discrep_mm THEN
    tTimer_DieGap_Discrep_BC := tTimer_DieGap_Discrep_BC + rCycle_Time_s;
ELSE
    tTimer_DieGap_Discrep_BC := 0.0;
END_IF;

IF rDiff_DieGap_CA > rTol_DieGap_Discrep_mm THEN
    tTimer_DieGap_Discrep_CA := tTimer_DieGap_Discrep_CA + rCycle_Time_s;
ELSE
    tTimer_DieGap_Discrep_CA := 0.0;
END_IF;

(* Channel Health Discrimination *)
bHealth_DieGap_ChA := NOT ((tTimer_DieGap_Discrep_AB >= rPersistence_TMR_Limit_s) AND (tTimer_DieGap_Discrep_CA >= rPersistence_TMR_Limit_s));
bHealth_DieGap_ChB := NOT ((tTimer_DieGap_Discrep_AB >= rPersistence_TMR_Limit_s) AND (tTimer_DieGap_Discrep_BC >= rPersistence_TMR_Limit_s));
bHealth_DieGap_ChC := NOT ((tTimer_DieGap_Discrep_BC >= rPersistence_TMR_Limit_s) AND (tTimer_DieGap_Discrep_CA >= rPersistence_TMR_Limit_s));

(* Voting Execution & Bumpless Degradation *)
IF bHealth_DieGap_ChA AND bHealth_DieGap_ChB AND bHealth_DieGap_ChC THEN
    (* 2oo3 Normal Median Voting *)
    iDegradedMode_DieGap := 0;
    IF (rDieGap_LVDT_ChA_mm_In >= rDieGap_LVDT_ChB_mm_In AND rDieGap_LVDT_ChA_mm_In <= rDieGap_LVDT_ChC_mm_In) OR
       (rDieGap_LVDT_ChA_mm_In <= rDieGap_LVDT_ChB_mm_In AND rDieGap_LVDT_ChA_mm_In >= rDieGap_LVDT_ChC_mm_In) THEN
        rVoted_DieGap_mm := rDieGap_LVDT_ChA_mm_In;
    ELSIF (rDieGap_LVDT_ChB_mm_In >= rDieGap_LVDT_ChA_mm_In AND rDieGap_LVDT_ChB_mm_In <= rDieGap_LVDT_ChC_mm_In) OR
          (rDieGap_LVDT_ChB_mm_In <= rDieGap_LVDT_ChA_mm_In AND rDieGap_LVDT_ChB_mm_In >= rDieGap_LVDT_ChC_mm_In) THEN
        rVoted_DieGap_mm := rDieGap_LVDT_ChB_mm_In;
    ELSE
        rVoted_DieGap_mm := rDieGap_LVDT_ChC_mm_In;
    END_IF;
ELSIF bHealth_DieGap_ChA AND bHealth_DieGap_ChB AND (NOT bHealth_DieGap_ChC) THEN
    (* Degraded 1oo2: ChA and ChB Average *)
    iDegradedMode_DieGap := 1;
    rVoted_DieGap_mm := (rDieGap_LVDT_ChA_mm_In + rDieGap_LVDT_ChB_mm_In) * 0.50;
ELSIF bHealth_DieGap_ChB AND bHealth_DieGap_ChC AND (NOT bHealth_DieGap_ChA) THEN
    (* Degraded 1oo2: ChB and ChC Average *)
    iDegradedMode_DieGap := 2;
    rVoted_DieGap_mm := (rDieGap_LVDT_ChB_mm_In + rDieGap_LVDT_ChC_mm_In) * 0.50;
ELSIF bHealth_DieGap_ChA AND bHealth_DieGap_ChC AND (NOT bHealth_DieGap_ChB) THEN
    (* Degraded 1oo2: ChA and ChC Average *)
    iDegradedMode_DieGap := 3;
    rVoted_DieGap_mm := (rDieGap_LVDT_ChA_mm_In + rDieGap_LVDT_ChC_mm_In) * 0.50;
ELSE
    (* Dual Disagreement: Fail-Safe Freeze Tooling Gap & Alarm Trip *)
    iDegradedMode_DieGap := 4;
    bFailSafe_DieGap_Freeze := TRUE;
    bLatch_Alarm_TMR_Discrepancy := TRUE;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* CHANNEL 2: CO-EXTRUSION MELT PRESSURE TRANSDUCERS (ChA, ChB, ChC) [bar]                                             *)
(* -------------------------------------------------------------------------------------------------------------------- *)
rDiff_MeltPress_AB := ABS(rMeltPressure_Transducer_ChA_bar_In - rMeltPressure_Transducer_ChB_bar_In);
rDiff_MeltPress_BC := ABS(rMeltPressure_Transducer_ChB_bar_In - rMeltPressure_Transducer_ChC_bar_In);
rDiff_MeltPress_CA := ABS(rMeltPressure_Transducer_ChC_bar_In - rMeltPressure_Transducer_ChA_bar_In);

IF rDiff_MeltPress_AB > rTol_MeltPress_Discrep_bar THEN
    tTimer_MeltPress_Discrep_AB := tTimer_MeltPress_Discrep_AB + rCycle_Time_s;
ELSE
    tTimer_MeltPress_Discrep_AB := 0.0;
END_IF;

IF rDiff_MeltPress_BC > rTol_MeltPress_Discrep_bar THEN
    tTimer_MeltPress_Discrep_BC := tTimer_MeltPress_Discrep_BC + rCycle_Time_s;
ELSE
    tTimer_MeltPress_Discrep_BC := 0.0;
END_IF;

IF rDiff_MeltPress_CA > rTol_MeltPress_Discrep_bar THEN
    tTimer_MeltPress_Discrep_CA := tTimer_MeltPress_Discrep_CA + rCycle_Time_s;
ELSE
    tTimer_MeltPress_Discrep_CA := 0.0;
END_IF;

bHealth_MeltPress_ChA := NOT ((tTimer_MeltPress_Discrep_AB >= rPersistence_TMR_Limit_s) AND (tTimer_MeltPress_Discrep_CA >= rPersistence_TMR_Limit_s));
bHealth_MeltPress_ChB := NOT ((tTimer_MeltPress_Discrep_AB >= rPersistence_TMR_Limit_s) AND (tTimer_MeltPress_Discrep_BC >= rPersistence_TMR_Limit_s));
bHealth_MeltPress_ChC := NOT ((tTimer_MeltPress_Discrep_BC >= rPersistence_TMR_Limit_s) AND (tTimer_MeltPress_Discrep_CA >= rPersistence_TMR_Limit_s));

IF bHealth_MeltPress_ChA AND bHealth_MeltPress_ChB AND bHealth_MeltPress_ChC THEN
    iDegradedMode_MeltPress := 0;
    IF (rMeltPressure_Transducer_ChA_bar_In >= rMeltPressure_Transducer_ChB_bar_In AND rMeltPressure_Transducer_ChA_bar_In <= rMeltPressure_Transducer_ChC_bar_In) OR
       (rMeltPressure_Transducer_ChA_bar_In <= rMeltPressure_Transducer_ChB_bar_In AND rMeltPressure_Transducer_ChA_bar_In >= rMeltPressure_Transducer_ChC_bar_In) THEN
        rVoted_MeltPressure_bar := rMeltPressure_Transducer_ChA_bar_In;
    ELSIF (rMeltPressure_Transducer_ChB_bar_In >= rMeltPressure_Transducer_ChA_bar_In AND rMeltPressure_Transducer_ChB_bar_In <= rMeltPressure_Transducer_ChC_bar_In) OR
          (rMeltPressure_Transducer_ChB_bar_In <= rMeltPressure_Transducer_ChA_bar_In AND rMeltPressure_Transducer_ChB_bar_In >= rMeltPressure_Transducer_ChC_bar_In) THEN
        rVoted_MeltPressure_bar := rMeltPressure_Transducer_ChB_bar_In;
    ELSE
        rVoted_MeltPressure_bar := rMeltPressure_Transducer_ChC_bar_In;
    END_IF;
ELSIF bHealth_MeltPress_ChA AND bHealth_MeltPress_ChB AND (NOT bHealth_MeltPress_ChC) THEN
    iDegradedMode_MeltPress := 1;
    rVoted_MeltPressure_bar := (rMeltPressure_Transducer_ChA_bar_In + rMeltPressure_Transducer_ChB_bar_In) * 0.50;
ELSIF bHealth_MeltPress_ChB AND bHealth_MeltPress_ChC AND (NOT bHealth_MeltPress_ChA) THEN
    iDegradedMode_MeltPress := 2;
    rVoted_MeltPressure_bar := (rMeltPressure_Transducer_ChB_bar_In + rMeltPressure_Transducer_ChC_bar_In) * 0.50;
ELSIF bHealth_MeltPress_ChA AND bHealth_MeltPress_ChC AND (NOT bHealth_MeltPress_ChB) THEN
    iDegradedMode_MeltPress := 3;
    rVoted_MeltPressure_bar := (rMeltPressure_Transducer_ChA_bar_In + rMeltPressure_Transducer_ChC_bar_In) * 0.50;
ELSE
    iDegradedMode_MeltPress := 4;
    bFailSafe_MeltPress_Trip := TRUE;
    bLatch_Alarm_TMR_Discrepancy := TRUE;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* CHANNEL 3: DIE ORIFICE IR MELT PYROMETERS (ChA, ChB, ChC) [deg C]                                                    *)
(* -------------------------------------------------------------------------------------------------------------------- *)
rDiff_DieTemp_AB := ABS(rDieMeltTemp_IR_ChA_In - rDieMeltTemp_IR_ChB_In);
rDiff_DieTemp_BC := ABS(rDieMeltTemp_IR_ChB_In - rDieMeltTemp_IR_ChC_In);
rDiff_DieTemp_CA := ABS(rDieMeltTemp_IR_ChC_In - rDieMeltTemp_IR_ChA_In);

IF rDiff_DieTemp_AB > rTol_DieTemp_Discrep_C THEN
    tTimer_DieTemp_Discrep_AB := tTimer_DieTemp_Discrep_AB + rCycle_Time_s;
ELSE
    tTimer_DieTemp_Discrep_AB := 0.0;
END_IF;

IF rDiff_DieTemp_BC > rTol_DieTemp_Discrep_C THEN
    tTimer_DieTemp_Discrep_BC := tTimer_DieTemp_Discrep_BC + rCycle_Time_s;
ELSE
    tTimer_DieTemp_Discrep_BC := 0.0;
END_IF;

IF rDiff_DieTemp_CA > rTol_DieTemp_Discrep_C THEN
    tTimer_DieTemp_Discrep_CA := tTimer_DieTemp_Discrep_CA + rCycle_Time_s;
ELSE
    tTimer_DieTemp_Discrep_CA := 0.0;
END_IF;

bHealth_DieTemp_ChA := NOT ((tTimer_DieTemp_Discrep_AB >= rPersistence_TMR_Limit_s) AND (tTimer_DieTemp_Discrep_CA >= rPersistence_TMR_Limit_s));
bHealth_DieTemp_ChB := NOT ((tTimer_DieTemp_Discrep_AB >= rPersistence_TMR_Limit_s) AND (tTimer_DieTemp_Discrep_BC >= rPersistence_TMR_Limit_s));
bHealth_DieTemp_ChC := NOT ((tTimer_DieTemp_Discrep_BC >= rPersistence_TMR_Limit_s) AND (tTimer_DieTemp_Discrep_CA >= rPersistence_TMR_Limit_s));

IF bHealth_DieTemp_ChA AND bHealth_DieTemp_ChB AND bHealth_DieTemp_ChC THEN
    iDegradedMode_DieTemp := 0;
    IF (rDieMeltTemp_IR_ChA_In >= rDieMeltTemp_IR_ChB_In AND rDieMeltTemp_IR_ChA_In <= rDieMeltTemp_IR_ChC_In) OR
       (rDieMeltTemp_IR_ChA_In <= rDieMeltTemp_IR_ChB_In AND rDieMeltTemp_IR_ChA_In >= rDieMeltTemp_IR_ChC_In) THEN
        rVoted_DieMeltTemp_C := rDieMeltTemp_IR_ChA_In;
    ELSIF (rDieMeltTemp_IR_ChB_In >= rDieMeltTemp_IR_ChA_In AND rDieMeltTemp_IR_ChB_In <= rDieMeltTemp_IR_ChC_In) OR
          (rDieMeltTemp_IR_ChB_In <= rDieMeltTemp_IR_ChA_In AND rDieMeltTemp_IR_ChB_In >= rDieMeltTemp_IR_ChC_In) THEN
        rVoted_DieMeltTemp_C := rDieMeltTemp_IR_ChB_In;
    ELSE
        rVoted_DieMeltTemp_C := rDieMeltTemp_IR_ChC_In;
    END_IF;
ELSIF bHealth_DieTemp_ChA AND bHealth_DieTemp_ChB AND (NOT bHealth_DieTemp_ChC) THEN
    iDegradedMode_DieTemp := 1;
    rVoted_DieMeltTemp_C := (rDieMeltTemp_IR_ChA_In + rDieMeltTemp_IR_ChB_In) * 0.50;
ELSIF bHealth_DieTemp_ChB AND bHealth_DieTemp_ChC AND (NOT bHealth_DieTemp_ChA) THEN
    iDegradedMode_DieTemp := 2;
    rVoted_DieMeltTemp_C := (rDieMeltTemp_IR_ChB_In + rDieMeltTemp_IR_ChC_In) * 0.50;
ELSIF bHealth_DieTemp_ChA AND bHealth_DieTemp_ChC AND (NOT bHealth_DieTemp_ChB) THEN
    iDegradedMode_DieTemp := 3;
    rVoted_DieMeltTemp_C := (rDieMeltTemp_IR_ChA_In + rDieMeltTemp_IR_ChC_In) * 0.50;
ELSE
    iDegradedMode_DieTemp := 4;
    bFailSafe_DieTemp_Trip := TRUE;
    bLatch_Alarm_TMR_Discrepancy := TRUE;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* CHANNEL 4: MOLD CAVITY NITROGEN GAS PRESSURE TRANSDUCERS (ChA, ChB, ChC) [bar]                                     *)
(* -------------------------------------------------------------------------------------------------------------------- *)
rDiff_MoldN2_AB := ABS(rMoldN2Pressure_Transducer_ChA_bar_In - rMoldN2Pressure_Transducer_ChB_bar_In);
rDiff_MoldN2_BC := ABS(rMoldN2Pressure_Transducer_ChB_bar_In - rMoldN2Pressure_Transducer_ChC_bar_In);
rDiff_MoldN2_CA := ABS(rMoldN2Pressure_Transducer_ChC_bar_In - rMoldN2Pressure_Transducer_ChA_bar_In);

IF rDiff_MoldN2_AB > rTol_MoldN2_Discrep_bar THEN
    tTimer_MoldN2_Discrep_AB := tTimer_MoldN2_Discrep_AB + rCycle_Time_s;
ELSE
    tTimer_MoldN2_Discrep_AB := 0.0;
END_IF;

IF rDiff_MoldN2_BC > rTol_MoldN2_Discrep_bar THEN
    tTimer_MoldN2_Discrep_BC := tTimer_MoldN2_Discrep_BC + rCycle_Time_s;
ELSE
    tTimer_MoldN2_Discrep_BC := 0.0;
END_IF;

IF rDiff_MoldN2_CA > rTol_MoldN2_Discrep_bar THEN
    tTimer_MoldN2_Discrep_CA := tTimer_MoldN2_Discrep_CA + rCycle_Time_s;
ELSE
    tTimer_MoldN2_Discrep_CA := 0.0;
END_IF;

bHealth_MoldN2_ChA := NOT ((tTimer_MoldN2_Discrep_AB >= rPersistence_TMR_Limit_s) AND (tTimer_MoldN2_Discrep_CA >= rPersistence_TMR_Limit_s));
bHealth_MoldN2_ChB := NOT ((tTimer_MoldN2_Discrep_AB >= rPersistence_TMR_Limit_s) AND (tTimer_MoldN2_Discrep_BC >= rPersistence_TMR_Limit_s));
bHealth_MoldN2_ChC := NOT ((tTimer_MoldN2_Discrep_BC >= rPersistence_TMR_Limit_s) AND (tTimer_MoldN2_Discrep_CA >= rPersistence_TMR_Limit_s));

IF bHealth_MoldN2_ChA AND bHealth_MoldN2_ChB AND bHealth_MoldN2_ChC THEN
    iDegradedMode_MoldN2 := 0;
    IF (rMoldN2Pressure_Transducer_ChA_bar_In >= rMoldN2Pressure_Transducer_ChB_bar_In AND rMoldN2Pressure_Transducer_ChA_bar_In <= rMoldN2Pressure_Transducer_ChC_bar_In) OR
       (rMoldN2Pressure_Transducer_ChA_bar_In <= rMoldN2Pressure_Transducer_ChB_bar_In AND rMoldN2Pressure_Transducer_ChA_bar_In >= rMoldN2Pressure_Transducer_ChC_bar_In) THEN
        rVoted_MoldN2Pressure_bar := rMoldN2Pressure_Transducer_ChA_bar_In;
    ELSIF (rMoldN2Pressure_Transducer_ChB_bar_In >= rMoldN2Pressure_Transducer_ChA_bar_In AND rMoldN2Pressure_Transducer_ChB_bar_In <= rMoldN2Pressure_Transducer_ChC_bar_In) OR
          (rMoldN2Pressure_Transducer_ChB_bar_In <= rMoldN2Pressure_Transducer_ChA_bar_In AND rMoldN2Pressure_Transducer_ChB_bar_In >= rMoldN2Pressure_Transducer_ChC_bar_In) THEN
        rVoted_MoldN2Pressure_bar := rMoldN2Pressure_Transducer_ChB_bar_In;
    ELSE
        rVoted_MoldN2Pressure_bar := rMoldN2Pressure_Transducer_ChC_bar_In;
    END_IF;
ELSIF bHealth_MoldN2_ChA AND bHealth_MoldN2_ChB AND (NOT bHealth_MoldN2_ChC) THEN
    iDegradedMode_MoldN2 := 1;
    rVoted_MoldN2Pressure_bar := (rMoldN2Pressure_Transducer_ChA_bar_In + rMoldN2Pressure_Transducer_ChB_bar_In) * 0.50;
ELSIF bHealth_MoldN2_ChB AND bHealth_MoldN2_ChC AND (NOT bHealth_MoldN2_ChA) THEN
    iDegradedMode_MoldN2 := 2;
    rVoted_MoldN2Pressure_bar := (rMoldN2Pressure_Transducer_ChB_bar_In + rMoldN2Pressure_Transducer_ChC_bar_In) * 0.50;
ELSIF bHealth_MoldN2_ChA AND bHealth_MoldN2_ChC AND (NOT bHealth_MoldN2_ChB) THEN
    iDegradedMode_MoldN2 := 3;
    rVoted_MoldN2Pressure_bar := (rMoldN2Pressure_Transducer_ChA_bar_In + rMoldN2Pressure_Transducer_ChC_bar_In) * 0.50;
ELSE
    iDegradedMode_MoldN2 := 4;
    bFailSafe_MoldN2_Trip := TRUE;
    bLatch_Alarm_TMR_Discrepancy := TRUE;
END_IF;
""")

    # -------------------------------------------------------------------------
    # PHASE 2: FIRST-PRINCIPLES CYBER-PHYSICAL 12-STATE DISCRETE STATE-SPACE MODEL & KALMAN FILTER
    # -------------------------------------------------------------------------
    out.append("""
(* ==================================================================================================================== *)
(* PHASE 2: FIRST-PRINCIPLES CYBER-PHYSICAL 12-STATE DISCRETE STATE-SPACE MODEL & KALMAN FILTER                         *)
(* ==================================================================================================================== *)

(* -------------------------------------------------------------------------------------------------------------------- *)
(* SUB-PHASE 2.1: SENSOR MEASUREMENT VECTOR & CONTROL INPUT VECTOR ASSEMBLY                                             *)
(* -------------------------------------------------------------------------------------------------------------------- *)
rVec_y_Meas_1 := rParison_Tip_Laser_Pos_mm_In;
rVec_y_Meas_2 := rDieSwell_Proxy_Diameter_mm;
rVec_y_Meas_3 := rVoted_DieMeltTemp_C;
rVec_y_Meas_4 := rVoted_MeltPressure_bar;
IF iFSM_State_Current >= 8 THEN
    rVec_y_Meas_5 := rVoted_MoldN2Pressure_bar;
ELSE
    rVec_y_Meas_5 := rRecipe_PreBlow_Pressure_bar_In;
END_IF;
rVec_y_Meas_6 := rVoted_DieGap_mm;

(* Current Applied Inputs *)
rVec_u_1 := rServo_DieGap_Spool_Cmd_Pct_Out;
rVec_u_2 := rExtruder_Master_Speed_RPM_Out;
rVec_u_3 := rPreBlow_Air_Servo_Cmd_Pct_Out + rHighPress_N2_Blow_Valve_Pct_Out;
rVec_u_4 := rMold_Cooling_Water_Valve_Pct_Out;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* SUB-PHASE 2.2: UNROLLED ONE-STEP AHEAD STATE PREDICTION (x_pred = Ad * x + Bd * u)                                  *)
(* -------------------------------------------------------------------------------------------------------------------- *)
""")

    # Generate 12 fully expanded unrolled state prediction equations
    for i in range(1, 13):
        terms_a = " + ".join([f"(rMat_Ad_{i}_{j} * rVec_x_State_{j})" for j in range(1, 13)])
        terms_b = " + ".join([f"(rMat_Bd_{i}_{k} * rVec_u_{k})" for k in range(1, 5)])
        out.append(f"rVec_x_Pred_{i} := {terms_a} +\n               {terms_b};\n")

    out.append("""
(* -------------------------------------------------------------------------------------------------------------------- *)
(* SUB-PHASE 2.3: UNROLLED MEASUREMENT OUTPUT PREDICTION (y_pred = Cd * x_pred + Dd * u)                                *)
(* -------------------------------------------------------------------------------------------------------------------- *)
""")
    # Generate 6 fully expanded unrolled measurement prediction equations
    for m in range(1, 7):
        terms_c = " + ".join([f"(rMat_Cd_{m}_{j} * rVec_x_Pred_{j})" for j in range(1, 13)])
        terms_d = " + ".join([f"(rMat_Dd_{m}_{k} * rVec_u_{k})" for k in range(1, 5)])
        out.append(f"rVec_y_Pred_{m} := {terms_c} +\n               {terms_d};\n")

    out.append("""
(* -------------------------------------------------------------------------------------------------------------------- *)
(* SUB-PHASE 2.4: INNOVATION RESIDUAL CALCULATION (e = y_meas - y_pred)                                                 *)
(* -------------------------------------------------------------------------------------------------------------------- *)
rVec_e_Resid_1 := rVec_y_Meas_1 - rVec_y_Pred_1;
rVec_e_Resid_2 := rVec_y_Meas_2 - rVec_y_Pred_2;
rVec_e_Resid_3 := rVec_y_Meas_3 - rVec_y_Pred_3;
rVec_e_Resid_4 := rVec_y_Meas_4 - rVec_y_Pred_4;
rVec_e_Resid_5 := rVec_y_Meas_5 - rVec_y_Pred_5;
rVec_e_Resid_6 := rVec_y_Meas_6 - rVec_y_Pred_6;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* SUB-PHASE 2.5: UNROLLED KALMAN FILTER POSTERIOR STATE CORRECTION (x_corr = x_pred + L * e)                         *)
(* -------------------------------------------------------------------------------------------------------------------- *)
""")
    # Generate 12 fully expanded Kalman innovation update equations
    for i in range(1, 13):
        terms_l = " + ".join([f"(rMat_L_{i}_{m} * rVec_e_Resid_{m})" for m in range(1, 7)])
        out.append(f"rVec_x_Corr_{i} := rVec_x_Pred_{i} + {terms_l};")
        out.append(f"rVec_x_State_{i} := rVec_x_Corr_{i};\n")

    out.append("""
(* -------------------------------------------------------------------------------------------------------------------- *)
(* SUB-PHASE 2.6: ADVANCED POLYMER RHEOLOGICAL CONSTITUTIVE EQUATIONS & RECURRENT ESTIMATORS                            *)
(* -------------------------------------------------------------------------------------------------------------------- *)
(* 1. Cross-WLF Viscosity Model Evaluation *)
rZero_Shear_Viscosity_eta0 := rVisc_A1 * EXP(-rVisc_A2 * (rVec_x_State_4 - rVisc_T_ref) / (rVisc_A3 + (rVec_x_State_4 - rVisc_T_ref) + 1.0E-6));
rApparent_Viscosity_eta := rZero_Shear_Viscosity_eta0 / (1.0 + EXPT(rRelaxation_Time_lambda * rShear_Rate_gamma_dot, 1.0 - rPower_Law_Index_n) + 1.0E-6);

(* 2. Tanner Elastic Recovery Radial Die Swell Law *)
rFirst_Normal_Stress_N1 := 2.0 * rWall_Shear_Stress_tau_w * rWeissenberg_Number_Wi;
rDie_Swell_Ratio_B := EXPT(1.0 + 0.50 * EXPT(rFirst_Normal_Stress_N1 / (2.0 * rWall_Shear_Stress_tau_w + 1.0E-6), 2.0), 0.1666667);
rActual_DieSwell_Ratio_Out := rDie_Swell_Ratio_B;
rDieSwell_Proxy_Diameter_mm := rNominal_Die_Diameter_mm * rDie_Swell_Ratio_B;

(* 3. Non-Linear Viscoelastic Parison Gravitational Sag Strain Accumulation *)
rParison_Mass_Hanging_kg := 3.14159265 * (rNominal_Die_Diameter_mm * 0.001) * (rVec_x_State_7 * 0.001) * (rVec_x_State_1 * 0.001) * rMelt_Density_kg_m3;
rCalculated_FuelTank_Mass_kg_Out := rParison_Mass_Hanging_kg;
rAxial_Gravity_Stress_Pa := (rParison_Mass_Hanging_kg * 9.80665) / (rCross_Sectional_Area_m2 + 1.0E-6);
rElongational_Viscosity_Pa_s := 3.0 * rApparent_Viscosity_eta; (* Trouton ratio = 3 for un-oriented linear melt *)
rSag_Strain_Rate_per_s := rAxial_Gravity_Stress_Pa / (rElongational_Viscosity_Pa_s + 1.0E-6);
rVec_x_State_2 := rVec_x_State_2 + (rSag_Strain_Rate_per_s * rCycle_Time_s);

(* 4. 6-Layer Co-Ex EVOH Barrier Layer Thickness Preservation Law *)
rEVOH_Estimated_Layer_Thickness_um_Out := rVec_x_State_6 * 1000.0;
rParison_Current_Length_mm_Out := rVec_x_State_1;
rEstimated_PinchWeld_Temp_Out := rVec_x_State_10;
""")

    # -------------------------------------------------------------------------
    # PHASE 3: RECEDING-HORIZON MPC OPTIMIZATION WITH 3 UNROLLED PGD ITERATIONS
    # -------------------------------------------------------------------------
    out.append("""
(* ==================================================================================================================== *)
(* PHASE 3: RECEDING-HORIZON MPC OPTIMIZATION WITH UNROLLED 10-STEP PROJECTED GRADIENT DESCENT (PGD)                     *)
(* ==================================================================================================================== *)

(* -------------------------------------------------------------------------------------------------------------------- *)
(* SUB-PHASE 3.1: DYNAMIC REFERENCE PROFILE SYNCHRONIZATION BASED ON PRODUCTION FSM STATE                               *)
(* -------------------------------------------------------------------------------------------------------------------- *)
IF iFSM_State_Current = 4 THEN
    (* State 4: 100-Point WDS Profile Interpolation Mapped to Parison Length *)
    rScratch_Active_Index_Real := (rParison_Current_Length_mm_Out / (rRecipe_Target_Parison_Length_mm_In + 1.0E-6)) * 99.0;
    IF rScratch_Active_Index_Real < 0.0 THEN
        rScratch_Active_Index_Real := 0.0;
    ELSIF rScratch_Active_Index_Real > 99.0 THEN
        rScratch_Active_Index_Real := 99.0;
    END_IF;
    rWDS_Active_Profile_Point_Out := rScratch_Active_Index_Real;

    iScratch_Index_Low := REAL_TO_INT(rScratch_Active_Index_Real - 0.4999);
    IF iScratch_Index_Low < 0 THEN
        iScratch_Index_Low := 0;
    ELSIF iScratch_Index_Low > 98 THEN
        iScratch_Index_Low := 98;
    END_IF;
    iScratch_Index_High := iScratch_Index_Low + 1;
    rScratch_Interpol_Frac := rScratch_Active_Index_Real - INT_TO_REAL(iScratch_Index_Low);

    (* Linear Spline Interpolation of Tooling Gap, PWDS Ovalization, and Pre-Blow Pressure *)
    rScratch_Target_Gap_Pct := aWDS_Profile_AxialGap_Pct[iScratch_Index_Low] +
        rScratch_Interpol_Frac * (aWDS_Profile_AxialGap_Pct[iScratch_Index_High] - aWDS_Profile_AxialGap_Pct[iScratch_Index_Low]);

    rScratch_Target_PWDS_mm := aWDS_Profile_RadialPWDS_mm[iScratch_Index_Low] +
        rScratch_Interpol_Frac * (aWDS_Profile_RadialPWDS_mm[iScratch_Index_High] - aWDS_Profile_RadialPWDS_mm[iScratch_Index_Low]);

    rScratch_Target_PreBlow_bar := aWDS_Profile_PreBlow_bar[iScratch_Index_Low] +
        rScratch_Interpol_Frac * (aWDS_Profile_PreBlow_bar[iScratch_Index_High] - aWDS_Profile_PreBlow_bar[iScratch_Index_Low]);

    (* Apply Global Weight Bias Scaling *)
    rScratch_Target_Gap_Pct := rScratch_Target_Gap_Pct * (1.0 + (rRecipe_WDS_Profile_Weight_Bias_In / 100.0));
    rRef_x7_DieGap_mm := (rScratch_Target_Gap_Pct / 100.0) * rRecipe_Nominal_Tooling_Gap_mm_In * 2.0;
    rRef_x9_PreBlow_bar := rScratch_Target_PreBlow_bar;
    rRef_u1_ServoSpool_Pct := rScratch_Target_Gap_Pct;
    rPWDS_Radial_Ovalization_mm_Out := rScratch_Target_PWDS_mm;

ELSIF (iFSM_State_Current = 8) OR (iFSM_State_Current = 9) THEN
    (* State 8 & 9: High-Pressure Nitrogen Gas Blow & In-Mold Cooling *)
    rRef_x11_MoldN2_bar := rRecipe_High_Pressure_N2_bar_In;
    rRef_x12_HeatFlux_kWm2 := 45.0;
    rRef_u3_PreBlowN2_Pct := 100.0;
    rRef_u4_MoldCooling_Pct := 90.0;
ELSE
    (* Baseline Calibration / Standby Targets *)
    rRef_x7_DieGap_mm := rRecipe_Nominal_Tooling_Gap_mm_In;
    rRef_x9_PreBlow_bar := 0.0;
    rRef_x11_MoldN2_bar := 0.0;
    rRef_u1_ServoSpool_Pct := 0.0;
    rRef_u3_PreBlowN2_Pct := 0.0;
    rRef_u4_MoldCooling_Pct := 50.0;
END_IF;

(* Initialize Horizon Step 0 States to Current Physical State Estimates *)
rMPC_x1_H0 := rVec_x_State_1;
rMPC_x2_H0 := rVec_x_State_2;
rMPC_x3_H0 := rVec_x_State_3;
rMPC_x4_H0 := rVec_x_State_4;
rMPC_x5_H0 := rVec_x_State_5;
rMPC_x6_H0 := rVec_x_State_6;
rMPC_x7_H0 := rVec_x_State_7;
rMPC_x8_H0 := rVec_x_State_8;
rMPC_x9_H0 := rVec_x_State_9;
rMPC_x10_H0 := rVec_x_State_10;
rMPC_x11_H0 := rVec_x_State_11;
rMPC_x12_H0 := rVec_x_State_12;
""")

    # Generate 3 UNROLLED PGD ITERATIONS (Iteration 01, Iteration 02, Iteration 03)
    # Each iteration has:
    # 1. Forward Rollout (h = 0 to 9, 12 states each = 120 equations)
    # 2. Terminal Costate (h = 10, 12 costates)
    # 3. Backward Costate Pass (h = 9 down to 0, 12 costates each = 120 equations)
    # 4. Gradient Computation (h = 0 to 9, 4 inputs each = 40 equations)
    # 5. Projected Gradient Update & Slew Limiting (h = 0 to 9, 4 inputs each = 40 blocks)
    for iter_idx in range(1, 4):
        out.append(f"""
(* ==================================================================================================================== *)
(* UNROLLED PGD ITERATION {iter_idx:02d} OF 03: FORWARD TRAJECTORY, BACKWARD ADJOINT & PROJECTED GRADIENT UPDATE         *)
(* ==================================================================================================================== *)
""")
        # Step 1: Forward Rollout (h = 0 to 9)
        out.append(f"(* --- Iteration {iter_idx:02d} Step 1: Forward Horizon State Simulation Rollout (h = 0 to 9) --- *)\n")
        for h in range(10):
            out.append(f"(* Forward Simulation Step h = {h} -> h = {h+1} *)")
            for i in range(1, 13):
                terms_a = " + ".join([f"(rMat_Ad_{i}_{j} * rMPC_x{j}_H{h})" for j in range(1, 13)])
                terms_b = " + ".join([f"(rMat_Bd_{i}_{k} * rMPC_u{k}_H{h})" for k in range(1, 5)])
                out.append(f"rMPC_x{i}_H{h+1} := {terms_a} +\n                   {terms_b};")
            out.append("")

        # Step 2: Terminal Costate at h = 10
        out.append(f"(* --- Iteration {iter_idx:02d} Step 2: Terminal Adjoint Costate Initialization at h = 10 --- *)\n")
        ref_names = [
            "rRef_x1_TipPos_mm", "rRef_x2_SagStrain", "rRef_x3_SwellRatio", "rRef_x4_MeltTemp_C",
            "rRef_x5_InnerHDPE_mm", "rRef_x6_EVOH_mm", "rRef_x7_DieGap_mm", "rRef_x8_HeadPress_bar",
            "rRef_x9_PreBlow_bar", "rRef_x10_WeldTemp_C", "rRef_x11_MoldN2_bar", "rRef_x12_HeatFlux_kWm2"
        ]
        for s in range(1, 13):
            out.append(f"rMPC_lambda{s}_H10 := rMPC_Weight_P_{s} * (rMPC_x{s}_H10 - {ref_names[s-1]});")

        # Step 3: Backward Adjoint Pass (h = 9 down to 0)
        out.append(f"\n(* --- Iteration {iter_idx:02d} Step 3: Backward Adjoint Costate Propagation (h = 9 down to 0) --- *)\n")
        for h in range(9, -1, -1):
            out.append(f"(* Backward Adjoint Step h = {h} from lambda_H{h+1} *)")
            for i in range(1, 13):
                # lambda_i_H[h] = sum_j (Ad_ji * lambda_j_H[h+1]) + Q_i * (x_i_H[h] - x_ref_i)
                terms_at = " + ".join([f"(rMat_Ad_{j}_{i} * rMPC_lambda{j}_H{h+1})" for j in range(1, 13)])
                out.append(f"rMPC_lambda{i}_H{h} := {terms_at} +\n                   (rMPC_Weight_Q_{i} * (rMPC_x{i}_H{h} - {ref_names[i-1]}));")
            out.append("")

        # Step 4: Gradient Computation (h = 0 to 9)
        out.append(f"(* --- Iteration {iter_idx:02d} Step 4: Actuator Control Gradient Computation (h = 0 to 9) --- *)\n")
        ref_u_names = [
            "rRef_u1_ServoSpool_Pct", "rRef_u2_MasterSpeed_RPM", "rRef_u3_PreBlowN2_Pct", "rRef_u4_MoldCooling_Pct"
        ]
        for h in range(10):
            for u in range(1, 5):
                # grad_u_k_H[h] = sum_i (Bd_ik * lambda_i_H[h+1]) + R_k * (u_k_H[h] - u_ref_k)
                terms_bt = " + ".join([f"(rMat_Bd_{i}_{u} * rMPC_lambda{i}_H{h+1})" for i in range(1, 13)])
                if h == 0:
                    slew_term = f" + (rMPC_Weight_S_{u} * (rMPC_u{u}_H0 - rMPC_u{u}_Prev))"
                else:
                    slew_term = f" + (rMPC_Weight_S_{u} * (rMPC_u{u}_H{h} - rMPC_u{u}_H{h-1}))"
                out.append(f"rMPC_grad_u{u}_H{h} := {terms_bt} +\n                     (rMPC_Weight_R_{u} * (rMPC_u{u}_H{h} - {ref_u_names[u-1]})){slew_term};")
            out.append("")

        # Step 5: Projected Gradient Update & Actuator Slew Rate Limiting
        out.append(f"(* --- Iteration {iter_idx:02d} Step 5: Projected Gradient Descent Update with Actuator Bounds --- *)\n")
        for h in range(10):
            for u in range(1, 5):
                out.append(f"rMPC_u{u}_H{h} := rMPC_u{u}_H{h} - (rMPC_Alpha_Step * rMPC_grad_u{u}_H{h});")
                out.append(f"IF rMPC_u{u}_H{h} > rActuator_u{u}_Max THEN")
                out.append(f"    rMPC_u{u}_H{h} := rActuator_u{u}_Max;")
                out.append(f"ELSIF rMPC_u{u}_H{h} < rActuator_u{u}_Min THEN")
                out.append(f"    rMPC_u{u}_H{h} := rActuator_u{u}_Min;")
                out.append("END_IF;")
            out.append("")

    # Commit MPC horizon step 0 to actuator commands
    out.append("""
(* -------------------------------------------------------------------------------------------------------------------- *)
(* SUB-PHASE 3.4: SLEW RATE LIMITING & COMMITMENT OF FIRST HORIZON STEP TO MASTER ACTUATORS                             *)
(* -------------------------------------------------------------------------------------------------------------------- *)
(* Actuator 1: Hydraulic Servo Spool Command Slew Rate Limiting *)
rScratch_Slew_Delta := rMPC_u1_H0 - rMPC_u1_Prev;
IF rScratch_Slew_Delta > rActuator_Slew_u1_Max THEN
    rMPC_u1_H0 := rMPC_u1_Prev + rActuator_Slew_u1_Max;
ELSIF rScratch_Slew_Delta < -rActuator_Slew_u1_Max THEN
    rMPC_u1_H0 := rMPC_u1_Prev - rActuator_Slew_u1_Max;
END_IF;
rMPC_u1_Prev := rMPC_u1_H0;

(* Actuator 2: Master Extruder Speed Slew Rate Limiting *)
rScratch_Slew_Delta := rMPC_u2_H0 - rMPC_u2_Prev;
IF rScratch_Slew_Delta > rActuator_Slew_u2_Max THEN
    rMPC_u2_H0 := rMPC_u2_Prev + rActuator_Slew_u2_Max;
ELSIF rScratch_Slew_Delta < -rActuator_Slew_u2_Max THEN
    rMPC_u2_H0 := rMPC_u2_Prev - rActuator_Slew_u2_Max;
END_IF;
rMPC_u2_Prev := rMPC_u2_H0;

(* Actuator 3: Pre-Blow / High-Pressure N2 Valve Slew Rate Limiting *)
rScratch_Slew_Delta := rMPC_u3_H0 - rMPC_u3_Prev;
IF rScratch_Slew_Delta > rActuator_Slew_u3_Max THEN
    rMPC_u3_H0 := rMPC_u3_Prev + rActuator_Slew_u3_Max;
ELSIF rScratch_Slew_Delta < -rActuator_Slew_u3_Max THEN
    rMPC_u3_H0 := rMPC_u3_Prev - rActuator_Slew_u3_Max;
END_IF;
rMPC_u3_Prev := rMPC_u3_H0;

(* Actuator 4: Mold Cooling Water Valve Slew Rate Limiting *)
rScratch_Slew_Delta := rMPC_u4_H0 - rMPC_u4_Prev;
IF rScratch_Slew_Delta > rActuator_Slew_u4_Max THEN
    rMPC_u4_H0 := rMPC_u4_Prev + rActuator_Slew_u4_Max;
ELSIF rScratch_Slew_Delta < -rActuator_Slew_u4_Max THEN
    rMPC_u4_H0 := rMPC_u4_Prev - rActuator_Slew_u4_Max;
END_IF;
rMPC_u4_Prev := rMPC_u4_H0;

(* Output Assignment with Fail-Safe Override *)
IF bFailSafe_DieGap_Freeze THEN
    rServo_DieGap_Spool_Cmd_Pct_Out := 0.0; (* Neutral center spool position *)
ELSE
    rServo_DieGap_Spool_Cmd_Pct_Out := rMPC_u1_H0;
END_IF;

rExtruder_Master_Speed_RPM_Out := rMPC_u2_H0;

(* Coordinate 6 Co-Extrusion Layer Drives Proportional to Master Speed *)
rExtruder_A_InnerHDPE_RPM_Out := rMPC_u2_H0 * (rRecipe_Inner_HDPE_Layer_Ratio_In / 30.0);
rExtruder_B_Regrind_RPM_Out   := rMPC_u2_H0 * 1.050; (* Regrind layer 42% proportion *)
rExtruder_C_TieLayer1_RPM_Out := rMPC_u2_H0 * 0.125; (* Tie layer 1 proportion *)
rExtruder_D_EVOH_RPM_Out      := rMPC_u2_H0 * (rRecipe_EVOH_Barrier_Layer_Ratio_In / 3.0) * 0.150;
rExtruder_E_TieLayer2_RPM_Out := rMPC_u2_H0 * 0.125; (* Tie layer 2 proportion *)
rExtruder_F_OuterHDPE_RPM_Out := rMPC_u2_H0 * 0.650; (* Outer HDPE layer 20% proportion *)

IF iFSM_State_Current = 5 THEN
    rPreBlow_Air_Servo_Cmd_Pct_Out := rMPC_u3_H0;
    rHighPress_N2_Blow_Valve_Pct_Out := 0.0;
ELSIF (iFSM_State_Current = 8) OR (iFSM_State_Current = 9) THEN
    rPreBlow_Air_Servo_Cmd_Pct_Out := 0.0;
    rHighPress_N2_Blow_Valve_Pct_Out := rMPC_u3_H0;
ELSE
    rPreBlow_Air_Servo_Cmd_Pct_Out := 0.0;
    rHighPress_N2_Blow_Valve_Pct_Out := 0.0;
END_IF;

rMold_Cooling_Water_Valve_Pct_Out := rMPC_u4_H0;
""")

    # -------------------------------------------------------------------------
    # PHASE 4: DETERMINISTIC 14-STAGE PRODUCTION FINITE STATE MACHINE (FSM)
    # -------------------------------------------------------------------------
    out.append("""
(* ==================================================================================================================== *)
(* PHASE 4: DETERMINISTIC 14-STAGE PRODUCTION FINITE STATE MACHINE (FSM) SEQUENCER                                       *)
(* ==================================================================================================================== *)

(* State Timer Accumulation *)
rFSM_State_Elapsed_s := rFSM_State_Elapsed_s + rCycle_Time_s;
rFSM_Cycle_Elapsed_s := rFSM_Cycle_Elapsed_s + rCycle_Time_s;

(* Master Safety Hard Interlocks *)
IF bEmergency_Stop_Trip_In OR (NOT bSafety_Gate_Interlock_Closed_In) OR bFailSafe_MeltPress_Trip OR bFailSafe_DieGap_Freeze THEN
    iFSM_State_Next := 13; (* Trip Immediately to Emergency Purge State *)
END_IF;

(* Sequencer Execution Matrix *)
CASE iFSM_State_Current OF

    0: (* IDLE_SAFE_STANDBY *)
        bMold_Close_HighTonnage_Cmd_Out := FALSE;
        bMold_Open_PartExtraction_Cmd_Out := FALSE;
        bBlowPin_Cylinder_Advance_Cmd_Out := FALSE;
        bBlowPin_Cylinder_Retract_Cmd_Out := TRUE;
        bExhaust_Depressurization_Valve_Cmd_Out := TRUE;
        bParison_CutOff_HotKnife_Cmd_Out := FALSE;
        bRobot_PrePinch_Start_Permissive_Out := FALSE;
        bRobot_PartExtract_Start_Permissive_Out := FALSE;
        bFlash_Trimmer_Start_Permissive_Out := FALSE;
        rFSM_Cycle_Elapsed_s := 0.0;

        (* Transition Permissives to State 1 *)
        IF bSystem_Enable_In AND bCycle_Start_In AND bSafety_Gate_Interlock_Closed_In AND (NOT bEmergency_Stop_Trip_In) THEN
            iFSM_State_Next := 1;
        END_IF;

    1: (* EXTRUDER_MELT_TEMPERATURE_HOMOGENIZATION *)
        (* Maintain extrusion zone temperatures and check thermal stability *)
        bBlowPin_Cylinder_Retract_Cmd_Out := TRUE;
        bExhaust_Depressurization_Valve_Cmd_Out := TRUE;

        IF (rVoted_DieMeltTemp_C >= (rRecipe_Nominal_Tooling_Gap_mm_In * 0.0 + 205.0)) AND
           (rVoted_DieMeltTemp_C <= 220.0) AND (rFSM_State_Elapsed_s >= 5.0) THEN
            iFSM_State_Next := 2;
        ELSIF rFSM_State_Elapsed_s > rTimeout_Stage_01_Homog_s THEN
            bLatch_Alarm_Watchdog_Timeout := TRUE;
            iFSM_State_Next := 13;
        END_IF;

    2: (* DIE_GAP_CALIBRATION_ZERO_SEEKING *)
        (* Automated LVDT zero reference calibration routine *)
        IF (rVoted_DieGap_mm >= (rRecipe_Nominal_Tooling_Gap_mm_In - 0.20)) AND
           (rVoted_DieGap_mm <= (rRecipe_Nominal_Tooling_Gap_mm_In + 0.20)) AND
           (rFSM_State_Elapsed_s >= 2.0) THEN
            iFSM_State_Next := 3;
        ELSIF rFSM_State_Elapsed_s > rTimeout_Stage_02_ZeroSeek_s THEN
            bLatch_Alarm_Watchdog_Timeout := TRUE;
            iFSM_State_Next := 13;
        END_IF;

    3: (* PARISON_CONTINUOUS_EXTRUSION_PROFILE_RAMP *)
        (* Ramp master extruder screw speed to production throughput *)
        IF (rExtruder_Master_Speed_RPM_Out >= 45.0) AND (rParison_Current_Length_mm_Out >= 50.0) THEN
            iFSM_State_Next := 4;
        ELSIF rFSM_State_Elapsed_s > rTimeout_Stage_03_ExtrudeRamp_s THEN
            bLatch_Alarm_Watchdog_Timeout := TRUE;
            iFSM_State_Next := 13;
        END_IF;

    4: (* 100_POINT_WDS_SERVO_GAP_SYNCHRONIZATION *)
        (* Execute real-time 100-point WDS profile interpolation synchronized to parison drop *)
        IF rParison_Current_Length_mm_Out >= rRecipe_Target_Parison_Length_mm_In THEN
            iFSM_State_Next := 5;
        ELSIF rFSM_State_Elapsed_s > rTimeout_Stage_04_WDSSync_s THEN
            bLatch_Alarm_Watchdog_Timeout := TRUE;
            iFSM_State_Next := 13;
        END_IF;

    5: (* PRE_BLOW_AIR_INJECTION_PARISON_SHAPING *)
        (* Activate low-pressure pre-blow shaping air to prevent internal parison collapse *)
        IF rFSM_State_Elapsed_s >= 1.20 THEN
            iFSM_State_Next := 6;
        ELSIF rFSM_State_Elapsed_s > rTimeout_Stage_05_PreBlow_s THEN
            bLatch_Alarm_Watchdog_Timeout := TRUE;
            iFSM_State_Next := 13;
        END_IF;

    6: (* ROBOTIC_BOTTOM_PRE_PINCH_MANIPULATION *)
        (* Handshake with bottom robotic gripper to pre-pinch and tension parison bottom *)
        bRobot_PrePinch_Start_Permissive_Out := TRUE;

        IF bRobot_PrePinch_Handshake_Ready_In AND (rRobotic_PrePinch_Clamping_Force_kN_In >= 3.50) THEN
            bRobot_PrePinch_Start_Permissive_Out := FALSE;
            iFSM_State_Next := 7;
        ELSIF rFSM_State_Elapsed_s > rTimeout_Stage_06_PrePinch_s THEN
            bLatch_Alarm_Watchdog_Timeout := TRUE;
            iFSM_State_Next := 13;
        END_IF;

    7: (* MOLD_CLAMPING_HIGH_TONNAGE_LOCK *)
        (* Close mold platens, lock tie-bars to high tonnage, and cut parison top *)
        bMold_Close_HighTonnage_Cmd_Out := TRUE;

        IF bMold_Closed_Parting_Line_LS_In AND (rMold_Actual_Clamping_Tonnage_kN_In >= (rRecipe_Mold_Clamp_Tonnage_kN_In * 0.95)) THEN
            bParison_CutOff_HotKnife_Cmd_Out := TRUE;
            IF rFSM_State_Elapsed_s >= 1.50 THEN
                bParison_CutOff_HotKnife_Cmd_Out := FALSE;
                iFSM_State_Next := 8;
            END_IF;
        ELSIF rFSM_State_Elapsed_s > rTimeout_Stage_07_ClampLock_s THEN
            bLatch_Alarm_Watchdog_Timeout := TRUE;
            iFSM_State_Next := 13;
        END_IF;

    8: (* BLOW_PIN_INSERTION_HIGH_PRESSURE_N2_BLOW *)
        (* Insert blow pin into neck dome and ramp high-pressure nitrogen gas *)
        bBlowPin_Cylinder_Advance_Cmd_Out := TRUE;
        bBlowPin_Cylinder_Retract_Cmd_Out := FALSE;
        bExhaust_Depressurization_Valve_Cmd_Out := FALSE;

        IF bBlowPin_Full_Insertion_LS_In AND (rVoted_MoldN2Pressure_bar >= (rRecipe_High_Pressure_N2_bar_In * 0.92)) THEN
            iFSM_State_Next := 9;
        ELSIF rFSM_State_Elapsed_s > rTimeout_Stage_08_N2Blow_s THEN
            bLatch_Alarm_Watchdog_Timeout := TRUE;
            iFSM_State_Next := 13;
        END_IF;

    9: (* IN_MOLD_CRYOGENIC_COOLING_CYCLE *)
        (* Maintain 12 bar N2 holding pressure and circulate chilled water to freeze HDPE *)
        bBlowPin_Cylinder_Advance_Cmd_Out := TRUE;
        bExhaust_Depressurization_Valve_Cmd_Out := FALSE;

        IF rFSM_State_Elapsed_s >= rRecipe_InMold_Cooling_Time_s_In THEN
            iFSM_State_Next := 10;
        ELSIF rFSM_State_Elapsed_s > rTimeout_Stage_09_InMoldCool_s THEN
            bLatch_Alarm_Watchdog_Timeout := TRUE;
            iFSM_State_Next := 13;
        END_IF;

    10: (* EXHAUST_DEPRESSURIZATION_DEFLATION *)
        (* Open fast exhaust decompression valve and retract blow pin *)
        bExhaust_Depressurization_Valve_Cmd_Out := TRUE;
        bBlowPin_Cylinder_Advance_Cmd_Out := FALSE;
        bBlowPin_Cylinder_Retract_Cmd_Out := TRUE;

        IF (rVoted_MoldN2Pressure_bar <= 0.20) AND (rFSM_State_Elapsed_s >= 2.50) THEN
            iFSM_State_Next := 11;
        ELSIF rFSM_State_Elapsed_s > rTimeout_Stage_10_Exhaust_s THEN
            bLatch_Alarm_Watchdog_Timeout := TRUE;
            iFSM_State_Next := 13;
        END_IF;

    11: (* MOLD_OPENING_PART_GRIPPER_EXTRACTION *)
        (* Open mold platens and signal demolding robot for fuel tank part extraction *)
        bMold_Close_HighTonnage_Cmd_Out := FALSE;
        bMold_Open_PartExtraction_Cmd_Out := TRUE;
        bRobot_PartExtract_Start_Permissive_Out := TRUE;

        IF bPart_Extractor_Robot_Ready_In AND (rFSM_State_Elapsed_s >= 3.50) THEN
            bRobot_PartExtract_Start_Permissive_Out := FALSE;
            bMold_Open_PartExtraction_Cmd_Out := FALSE;
            iFSM_State_Next := 12;
        ELSIF rFSM_State_Elapsed_s > rTimeout_Stage_11_Demold_s THEN
            bLatch_Alarm_Watchdog_Timeout := TRUE;
            iFSM_State_Next := 13;
        END_IF;

    12: (* FLASH_DEFLASHING_PUNCH_TRIM_CYCLE *)
        (* Trigger hydraulic trimming press to punch pinch-off flash into granulator *)
        bFlash_Trimmer_Start_Permissive_Out := TRUE;

        IF bFlash_Trimmer_Cycle_Completed_In AND bFlash_Granulator_Ready_In THEN
            bFlash_Trimmer_Start_Permissive_Out := FALSE;
            iFSM_Cycle_Counter := iFSM_Cycle_Counter + 1;

            (* Continuous Cycle Permissive *)
            IF bCycle_Start_In AND (NOT bCycle_Stop_In) AND bSystem_Enable_In THEN
                iFSM_State_Next := 3; (* Loop back to continuous parison extrusion *)
            ELSE
                iFSM_State_Next := 0; (* Return to Standby *)
            END_IF;
        ELSIF rFSM_State_Elapsed_s > rTimeout_Stage_12_Deflash_s THEN
            bLatch_Alarm_Watchdog_Timeout := TRUE;
            iFSM_State_Next := 13;
        END_IF;

    13: (* EMERGENCY_PARISON_DROP_PURGE_TRIP *)
        (* Emergency fail-safe trip: open die gap, drop parison, decelerate extruders *)
        rServo_DieGap_Spool_Cmd_Pct_Out := 100.0; (* Open die tooling gap to purge *)
        rExtruder_Master_Speed_RPM_Out := 0.0;
        rPreBlow_Air_Servo_Cmd_Pct_Out := 0.0;
        rHighPress_N2_Blow_Valve_Pct_Out := 0.0;
        bMold_Close_HighTonnage_Cmd_Out := FALSE;
        bMold_Open_PartExtraction_Cmd_Out := TRUE;
        bBlowPin_Cylinder_Advance_Cmd_Out := FALSE;
        bBlowPin_Cylinder_Retract_Cmd_Out := TRUE;
        bExhaust_Depressurization_Valve_Cmd_Out := TRUE;
        bParison_CutOff_HotKnife_Cmd_Out := TRUE;
        bRobot_PrePinch_Start_Permissive_Out := FALSE;
        bRobot_PartExtract_Start_Permissive_Out := FALSE;
        bFlash_Trimmer_Start_Permissive_Out := FALSE;

        (* Operator Manual Reset Condition *)
        IF bOperator_Alarm_Reset_Cmd_In AND (NOT bEmergency_Stop_Trip_In) AND bSafety_Gate_Interlock_Closed_In THEN
            bLatch_Alarm_DieGap_HH := FALSE;
            bLatch_Alarm_MeltPress_HH := FALSE;
            bLatch_Alarm_DieTemp_HH := FALSE;
            bLatch_Alarm_MoldN2_HH := FALSE;
            bLatch_Alarm_TMR_Discrepancy := FALSE;
            bLatch_Alarm_Watchdog_Timeout := FALSE;
            bFailSafe_DieGap_Freeze := FALSE;
            bFailSafe_MeltPress_Trip := FALSE;
            bFailSafe_DieTemp_Trip := FALSE;
            bFailSafe_MoldN2_Trip := FALSE;
            bParison_CutOff_HotKnife_Cmd_Out := FALSE;
            iFSM_State_Next := 0;
        END_IF;

    ELSE
        iFSM_State_Next := 13;
END_CASE;

(* Execute FSM State Transition *)
IF iFSM_State_Next <> iFSM_State_Current THEN
    iFSM_State_Current := iFSM_State_Next;
    rFSM_State_Elapsed_s := 0.0;
    bFSM_Stage_Entry_Strobe := TRUE;
ELSE
    bFSM_Stage_Entry_Strobe := FALSE;
END_IF;

iFSM_State_Current_Out := iFSM_State_Current;
""")

    # -------------------------------------------------------------------------
    # PHASE 5: ANSI/ISA-18.2 MULTI-TIERED ALARM ENGINE & 32-BIT BIT-PACKED TELEMETRY
    # -------------------------------------------------------------------------
    out.append("""
(* ==================================================================================================================== *)
(* PHASE 5: ANSI/ISA-18.2 MULTI-TIERED PROCESS ALARM ENGINE & 32-BIT BIT-PACKED TELEMETRY REGISTERS                      *)
(* ==================================================================================================================== *)

(* -------------------------------------------------------------------------------------------------------------------- *)
(* SUB-PHASE 5.1: CONTINUOUS SENSOR SUPERVISION WITH HYSTERESIS & DEBOUNCE FILTRATION                                   *)
(* -------------------------------------------------------------------------------------------------------------------- *)
(* 1. Die Gap LVDT Servo Position Error *)
rScratch_State_Delta := ABS(rVoted_DieGap_mm - rRef_x7_DieGap_mm);
IF rScratch_State_Delta > rThresh_DieGap_Err_HH_mm THEN
    rTimer_Alarm_DieGap_HH := rTimer_Alarm_DieGap_HH + rCycle_Time_s;
    IF rTimer_Alarm_DieGap_HH >= 0.050 THEN
        bLatch_Alarm_DieGap_HH := TRUE;
    END_IF;
ELSIF rScratch_State_Delta < (rThresh_DieGap_Err_HH_mm - rDeadband_DieGap_mm) THEN
    rTimer_Alarm_DieGap_HH := 0.0;
END_IF;

IF rScratch_State_Delta > rThresh_DieGap_Err_H_mm THEN
    rTimer_Alarm_DieGap_H := rTimer_Alarm_DieGap_H + rCycle_Time_s;
    IF rTimer_Alarm_DieGap_H >= 0.150 THEN
        bLatch_Alarm_DieGap_H := TRUE;
    END_IF;
ELSIF rScratch_State_Delta < (rThresh_DieGap_Err_H_mm - rDeadband_DieGap_mm) THEN
    rTimer_Alarm_DieGap_H := 0.0;
END_IF;

(* 2. Co-Extrusion Melt Pressure Transducer *)
IF rVoted_MeltPressure_bar > rThresh_MeltPress_HH_bar THEN
    rTimer_Alarm_MeltPress_HH := rTimer_Alarm_MeltPress_HH + rCycle_Time_s;
    IF rTimer_Alarm_MeltPress_HH >= 0.025 THEN
        bLatch_Alarm_MeltPress_HH := TRUE;
    END_IF;
ELSIF rVoted_MeltPressure_bar < (rThresh_MeltPress_HH_bar - rDeadband_MeltPress_bar) THEN
    rTimer_Alarm_MeltPress_HH := 0.0;
END_IF;

IF rVoted_MeltPressure_bar > rThresh_MeltPress_H_bar THEN
    rTimer_Alarm_MeltPress_H := rTimer_Alarm_MeltPress_H + rCycle_Time_s;
    IF rTimer_Alarm_MeltPress_H >= 0.100 THEN
        bLatch_Alarm_MeltPress_H := TRUE;
    END_IF;
ELSIF rVoted_MeltPressure_bar < (rThresh_MeltPress_H_bar - rDeadband_MeltPress_bar) THEN
    rTimer_Alarm_MeltPress_H := 0.0;
END_IF;

IF (rVoted_MeltPressure_bar < rThresh_MeltPress_LL_bar) AND (iFSM_State_Current >= 3) THEN
    rTimer_Alarm_MeltPress_LL := rTimer_Alarm_MeltPress_LL + rCycle_Time_s;
    IF rTimer_Alarm_MeltPress_LL >= 0.250 THEN
        bLatch_Alarm_MeltPress_LL := TRUE;
    END_IF;
ELSIF rVoted_MeltPressure_bar > (rThresh_MeltPress_LL_bar + rDeadband_MeltPress_bar) THEN
    rTimer_Alarm_MeltPress_LL := 0.0;
END_IF;

(* 3. Die Orifice IR Melt Pyrometer *)
IF rVoted_DieMeltTemp_C > rThresh_DieTemp_HH_C THEN
    rTimer_Alarm_DieTemp_HH := rTimer_Alarm_DieTemp_HH + rCycle_Time_s;
    IF rTimer_Alarm_DieTemp_HH >= 0.100 THEN
        bLatch_Alarm_DieTemp_HH := TRUE;
    END_IF;
ELSIF rVoted_DieMeltTemp_C < (rThresh_DieTemp_HH_C - rDeadband_DieTemp_C) THEN
    rTimer_Alarm_DieTemp_HH := 0.0;
END_IF;

IF (rVoted_DieMeltTemp_C < rThresh_DieTemp_LL_C) AND (iFSM_State_Current >= 2) THEN
    rTimer_Alarm_DieTemp_LL := rTimer_Alarm_DieTemp_LL + rCycle_Time_s;
    IF rTimer_Alarm_DieTemp_LL >= 0.200 THEN
        bLatch_Alarm_DieTemp_LL := TRUE;
    END_IF;
ELSIF rVoted_DieMeltTemp_C > (rThresh_DieTemp_LL_C + rDeadband_DieTemp_C) THEN
    rTimer_Alarm_DieTemp_LL := 0.0;
END_IF;

(* 4. Mold Cavity High-Pressure Nitrogen Gas *)
IF (rVoted_MoldN2Pressure_bar > rThresh_MoldN2_HH_bar) AND (iFSM_State_Current >= 8) THEN
    rTimer_Alarm_MoldN2_HH := rTimer_Alarm_MoldN2_HH + rCycle_Time_s;
    IF rTimer_Alarm_MoldN2_HH >= 0.050 THEN
        bLatch_Alarm_MoldN2_HH := TRUE;
    END_IF;
ELSIF rVoted_MoldN2Pressure_bar < (rThresh_MoldN2_HH_bar - rDeadband_MoldN2_bar) THEN
    rTimer_Alarm_MoldN2_HH := 0.0;
END_IF;

IF (rVoted_MoldN2Pressure_bar < rThresh_MoldN2_LL_bar) AND (iFSM_State_Current = 9) THEN
    rTimer_Alarm_MoldN2_LL := rTimer_Alarm_MoldN2_LL + rCycle_Time_s;
    IF rTimer_Alarm_MoldN2_LL >= 0.250 THEN
        bLatch_Alarm_MoldN2_LL := TRUE;
    END_IF;
ELSIF rVoted_MoldN2Pressure_bar > (rThresh_MoldN2_LL_bar + rDeadband_MoldN2_bar) THEN
    rTimer_Alarm_MoldN2_LL := 0.0;
END_IF;

(* 5. Hydraulic Power Unit (HPU) Pressure & Temperature *)
IF rHydraulic_Supply_Pressure_bar_In < rThresh_HPU_Press_LL_bar THEN
    rTimer_Alarm_HPU_Press_LL := rTimer_Alarm_HPU_Press_LL + rCycle_Time_s;
    IF rTimer_Alarm_HPU_Press_LL >= 0.100 THEN
        bLatch_Alarm_HPU_Press_LL := TRUE;
    END_IF;
ELSIF rHydraulic_Supply_Pressure_bar_In > (rThresh_HPU_Press_LL_bar + rDeadband_HPU_Press_bar) THEN
    rTimer_Alarm_HPU_Press_LL := 0.0;
END_IF;

IF rHydraulic_Oil_Temp_In > rThresh_HPU_Temp_HH_C THEN
    rTimer_Alarm_HPU_Temp_HH := rTimer_Alarm_HPU_Temp_HH + rCycle_Time_s;
    IF rTimer_Alarm_HPU_Temp_HH >= 1.0 THEN
        bLatch_Alarm_HPU_Temp_HH := TRUE;
    END_IF;
ELSIF rHydraulic_Oil_Temp_In < (rThresh_HPU_Temp_HH_C - rDeadband_HPU_Temp_C) THEN
    rTimer_Alarm_HPU_Temp_HH := 0.0;
END_IF;

(* 6. Mold Chilled Cooling Water Recirculation *)
IF rMold_Cooling_Flow_Lpm_In < rThresh_CoolingWater_Flow_LL_Lpm THEN
    rTimer_Alarm_Cooling_Flow_LL := rTimer_Alarm_Cooling_Flow_LL + rCycle_Time_s;
    IF rTimer_Alarm_Cooling_Flow_LL >= 0.500 THEN
        bLatch_Alarm_Cooling_Flow_LL := TRUE;
    END_IF;
ELSIF rMold_Cooling_Flow_Lpm_In > (rThresh_CoolingWater_Flow_LL_Lpm + rDeadband_Cooling_Flow_Lpm) THEN
    rTimer_Alarm_Cooling_Flow_LL := 0.0;
END_IF;

IF rMold_Cooling_Return_Temp_In > rThresh_CoolingWater_Temp_HH_C THEN
    rTimer_Alarm_Cooling_Temp_HH := rTimer_Alarm_Cooling_Temp_HH + rCycle_Time_s;
    IF rTimer_Alarm_Cooling_Temp_HH >= 1.0 THEN
        bLatch_Alarm_Cooling_Temp_HH := TRUE;
    END_IF;
ELSIF rMold_Cooling_Return_Temp_In < (rThresh_CoolingWater_Temp_HH_C - rDeadband_Cooling_Temp_C) THEN
    rTimer_Alarm_Cooling_Temp_HH := 0.0;
END_IF;

(* 7. Mold High-Tonnage Lockup Clamping *)
IF (rMold_Actual_Clamping_Tonnage_kN_In < rThresh_ClampTonnage_LL_kN) AND (iFSM_State_Current >= 7) AND (iFSM_State_Current <= 9) THEN
    rTimer_Alarm_ClampTonnage_LL := rTimer_Alarm_ClampTonnage_LL + rCycle_Time_s;
    IF rTimer_Alarm_ClampTonnage_LL >= 0.200 THEN
        bLatch_Alarm_ClampTonnage_LL := TRUE;
    END_IF;
ELSIF rMold_Actual_Clamping_Tonnage_kN_In > (rThresh_ClampTonnage_LL_kN + rDeadband_ClampTonnage_kN) THEN
    rTimer_Alarm_ClampTonnage_LL := 0.0;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* SUB-PHASE 5.2: OPERATOR ALARM ACKNOWLEDGE & LATCH RESET PROCESSING                                                  *)
(* -------------------------------------------------------------------------------------------------------------------- *)
IF bOperator_Alarm_Reset_Cmd_In THEN
    IF rScratch_State_Delta < rThresh_DieGap_Err_H_mm THEN
        bLatch_Alarm_DieGap_H := FALSE;
    END_IF;
    IF rVoted_MeltPressure_bar < rThresh_MeltPress_H_bar THEN
        bLatch_Alarm_MeltPress_H := FALSE;
    END_IF;
    IF rVoted_MeltPressure_bar > rThresh_MeltPress_L_bar THEN
        bLatch_Alarm_MeltPress_L := FALSE;
    END_IF;
    IF rVoted_DieMeltTemp_C < rThresh_DieTemp_H_C THEN
        bLatch_Alarm_DieTemp_H := FALSE;
    END_IF;
    IF rVoted_DieMeltTemp_C > rThresh_DieTemp_L_C THEN
        bLatch_Alarm_DieTemp_L := FALSE;
    END_IF;
    IF rVoted_MoldN2Pressure_bar < rThresh_MoldN2_H_bar THEN
        bLatch_Alarm_MoldN2_H := FALSE;
    END_IF;
    IF rVoted_MoldN2Pressure_bar > rThresh_MoldN2_L_bar THEN
        bLatch_Alarm_MoldN2_L := FALSE;
    END_IF;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* SUB-PHASE 5.3: SYNTHESIS OF 32-BIT BIT-PACKED TELEMETRY STATUS WORD                                                  *)
(* -------------------------------------------------------------------------------------------------------------------- *)
dwSystem_Status_Word_Out := 16#00000000;
IF bSystem_Enable_In THEN
    dwSystem_Status_Word_Out := dwSystem_Status_Word_Out OR 16#00000001; (* Bit 0: System Enabled *)
END_IF;
IF bCycle_Start_In THEN
    dwSystem_Status_Word_Out := dwSystem_Status_Word_Out OR 16#00000002; (* Bit 1: Production Run Active *)
END_IF;
IF bSafety_Gate_Interlock_Closed_In THEN
    dwSystem_Status_Word_Out := dwSystem_Status_Word_Out OR 16#00000004; (* Bit 2: Safety Gates Closed *)
END_IF;
IF NOT bEmergency_Stop_Trip_In THEN
    dwSystem_Status_Word_Out := dwSystem_Status_Word_Out OR 16#00000008; (* Bit 3: E-Stop Healthy *)
END_IF;
IF bFlash_Granulator_Ready_In THEN
    dwSystem_Status_Word_Out := dwSystem_Status_Word_Out OR 16#00000010; (* Bit 4: Granulator Ready *)
END_IF;
IF bChilled_Water_Flow_Confirmed_In THEN
    dwSystem_Status_Word_Out := dwSystem_Status_Word_Out OR 16#00000020; (* Bit 5: Chilled Water Flow Confirmed *)
END_IF;
IF bNitrogen_Supply_Pressure_OK_In THEN
    dwSystem_Status_Word_Out := dwSystem_Status_Word_Out OR 16#00000040; (* Bit 6: N2 Storage Pressure Confirmed *)
END_IF;
IF bMold_Closed_Parting_Line_LS_In THEN
    dwSystem_Status_Word_Out := dwSystem_Status_Word_Out OR 16#00000080; (* Bit 7: Mold Clamped & Locked *)
END_IF;
IF bBlowPin_Full_Insertion_LS_In THEN
    dwSystem_Status_Word_Out := dwSystem_Status_Word_Out OR 16#00000100; (* Bit 8: Blow Pin Fully Engaged *)
END_IF;
IF iDegradedMode_DieGap = 0 THEN
    dwSystem_Status_Word_Out := dwSystem_Status_Word_Out OR 16#00000200; (* Bit 9: Die Gap LVDT TMR Healthy (2oo3) *)
END_IF;
IF iDegradedMode_MeltPress = 0 THEN
    dwSystem_Status_Word_Out := dwSystem_Status_Word_Out OR 16#00000400; (* Bit 10: Melt Pressure TMR Healthy (2oo3) *)
END_IF;
IF iDegradedMode_DieTemp = 0 THEN
    dwSystem_Status_Word_Out := dwSystem_Status_Word_Out OR 16#00000800; (* Bit 11: Die Pyrometer TMR Healthy (2oo3) *)
END_IF;
IF iDegradedMode_MoldN2 = 0 THEN
    dwSystem_Status_Word_Out := dwSystem_Status_Word_Out OR 16#00001000; (* Bit 12: Mold N2 TMR Healthy (2oo3) *)
END_IF;
IF bFailSafe_DieGap_Freeze THEN
    dwSystem_Status_Word_Out := dwSystem_Status_Word_Out OR 16#00002000; (* Bit 13: Die Gap Spool Frozen Fail-Safe *)
END_IF;
IF bFailSafe_MeltPress_Trip THEN
    dwSystem_Status_Word_Out := dwSystem_Status_Word_Out OR 16#00004000; (* Bit 14: Melt Overpressure Fail-Safe Trip *)
END_IF;
(* Encode Active FSM State into Bits 16..20 *)
dwSystem_Status_Word_Out := dwSystem_Status_Word_Out OR SHL(INT_TO_DWORD(iFSM_State_Current AND 16#1F), 16);

(* -------------------------------------------------------------------------------------------------------------------- *)
(* SUB-PHASE 5.4: SYNTHESIS OF ISA-18.2 MULTI-TIER 32-BIT BIT-PACKED ALARM WORDS                                        *)
(* -------------------------------------------------------------------------------------------------------------------- *)
(* Alarm Word 1: Priority 1 Critical Safety Shutdown Trips (HH / LL) *)
dwAlarm_Word_01_CriticalTrips_Out := 16#00000000;
IF bLatch_Alarm_DieGap_HH THEN
    dwAlarm_Word_01_CriticalTrips_Out := dwAlarm_Word_01_CriticalTrips_Out OR 16#00000001; (* Bit 0: Die Gap Error HH *)
END_IF;
IF bLatch_Alarm_MeltPress_HH THEN
    dwAlarm_Word_01_CriticalTrips_Out := dwAlarm_Word_01_CriticalTrips_Out OR 16#00000002; (* Bit 1: Melt Pressure HH *)
END_IF;
IF bLatch_Alarm_MeltPress_LL THEN
    dwAlarm_Word_01_CriticalTrips_Out := dwAlarm_Word_01_CriticalTrips_Out OR 16#00000004; (* Bit 2: Melt Pressure LL *)
END_IF;
IF bLatch_Alarm_DieTemp_HH THEN
    dwAlarm_Word_01_CriticalTrips_Out := dwAlarm_Word_01_CriticalTrips_Out OR 16#00000008; (* Bit 3: Die Melt Temp HH *)
END_IF;
IF bLatch_Alarm_DieTemp_LL THEN
    dwAlarm_Word_01_CriticalTrips_Out := dwAlarm_Word_01_CriticalTrips_Out OR 16#00000010; (* Bit 4: Die Melt Temp LL *)
END_IF;
IF bLatch_Alarm_MoldN2_HH THEN
    dwAlarm_Word_01_CriticalTrips_Out := dwAlarm_Word_01_CriticalTrips_Out OR 16#00000020; (* Bit 5: Mold N2 Pressure HH *)
END_IF;
IF bLatch_Alarm_MoldN2_LL THEN
    dwAlarm_Word_01_CriticalTrips_Out := dwAlarm_Word_01_CriticalTrips_Out OR 16#00000040; (* Bit 6: Mold N2 Pressure LL *)
END_IF;
IF bLatch_Alarm_HPU_Press_LL THEN
    dwAlarm_Word_01_CriticalTrips_Out := dwAlarm_Word_01_CriticalTrips_Out OR 16#00000080; (* Bit 7: HPU Hydraulic Press LL *)
END_IF;
IF bLatch_Alarm_HPU_Temp_HH THEN
    dwAlarm_Word_01_CriticalTrips_Out := dwAlarm_Word_01_CriticalTrips_Out OR 16#00000100; (* Bit 8: HPU Oil Temp HH *)
END_IF;
IF bLatch_Alarm_Cooling_Flow_LL THEN
    dwAlarm_Word_01_CriticalTrips_Out := dwAlarm_Word_01_CriticalTrips_Out OR 16#00000200; (* Bit 9: Mold Cooling Flow LL *)
END_IF;
IF bLatch_Alarm_Cooling_Temp_HH THEN
    dwAlarm_Word_01_CriticalTrips_Out := dwAlarm_Word_01_CriticalTrips_Out OR 16#00000400; (* Bit 10: Mold Cooling Temp HH *)
END_IF;
IF bLatch_Alarm_ClampTonnage_LL THEN
    dwAlarm_Word_01_CriticalTrips_Out := dwAlarm_Word_01_CriticalTrips_Out OR 16#00000800; (* Bit 11: Mold Clamp Tonnage LL *)
END_IF;
IF bEmergency_Stop_Trip_In THEN
    dwAlarm_Word_01_CriticalTrips_Out := dwAlarm_Word_01_CriticalTrips_Out OR 16#00001000; (* Bit 12: E-Stop Circuit Trip *)
END_IF;
IF NOT bSafety_Gate_Interlock_Closed_In THEN
    dwAlarm_Word_01_CriticalTrips_Out := dwAlarm_Word_01_CriticalTrips_Out OR 16#00002000; (* Bit 13: Safety Gate Open *)
END_IF;
IF bLatch_Alarm_Watchdog_Timeout THEN
    dwAlarm_Word_01_CriticalTrips_Out := dwAlarm_Word_01_CriticalTrips_Out OR 16#00004000; (* Bit 14: Stage Watchdog Timeout *)
END_IF;

(* Alarm Word 2: Priority 2 Process Warnings (H / L) *)
dwAlarm_Word_02_Warnings_Out := 16#00000000;
IF bLatch_Alarm_DieGap_H THEN
    dwAlarm_Word_02_Warnings_Out := dwAlarm_Word_02_Warnings_Out OR 16#00000001; (* Bit 0: Die Gap Warning H *)
END_IF;
IF bLatch_Alarm_MeltPress_H THEN
    dwAlarm_Word_02_Warnings_Out := dwAlarm_Word_02_Warnings_Out OR 16#00000002; (* Bit 1: Melt Pressure Warning H *)
END_IF;
IF bLatch_Alarm_MeltPress_L THEN
    dwAlarm_Word_02_Warnings_Out := dwAlarm_Word_02_Warnings_Out OR 16#00000004; (* Bit 2: Melt Pressure Warning L *)
END_IF;
IF bLatch_Alarm_DieTemp_H THEN
    dwAlarm_Word_02_Warnings_Out := dwAlarm_Word_02_Warnings_Out OR 16#00000008; (* Bit 3: Die Melt Temp Warning H *)
END_IF;
IF bLatch_Alarm_DieTemp_L THEN
    dwAlarm_Word_02_Warnings_Out := dwAlarm_Word_02_Warnings_Out OR 16#00000010; (* Bit 4: Die Melt Temp Warning L *)
END_IF;
IF bLatch_Alarm_MoldN2_H THEN
    dwAlarm_Word_02_Warnings_Out := dwAlarm_Word_02_Warnings_Out OR 16#00000020; (* Bit 5: Mold N2 Warning H *)
END_IF;
IF bLatch_Alarm_MoldN2_L THEN
    dwAlarm_Word_02_Warnings_Out := dwAlarm_Word_02_Warnings_Out OR 16#00000040; (* Bit 6: Mold N2 Warning L *)
END_IF;

(* Alarm Word 3: Priority 3 TMR Sensor Faults & Discrepancy Degradations *)
dwAlarm_Word_03_TMR_Discrepancies_Out := 16#00000000;
IF NOT bHealth_DieGap_ChA THEN
    dwAlarm_Word_03_TMR_Discrepancies_Out := dwAlarm_Word_03_TMR_Discrepancies_Out OR 16#00000001; (* Bit 0: Die Gap ChA Fault *)
END_IF;
IF NOT bHealth_DieGap_ChB THEN
    dwAlarm_Word_03_TMR_Discrepancies_Out := dwAlarm_Word_03_TMR_Discrepancies_Out OR 16#00000002; (* Bit 1: Die Gap ChB Fault *)
END_IF;
IF NOT bHealth_DieGap_ChC THEN
    dwAlarm_Word_03_TMR_Discrepancies_Out := dwAlarm_Word_03_TMR_Discrepancies_Out OR 16#00000004; (* Bit 2: Die Gap ChC Fault *)
END_IF;
IF NOT bHealth_MeltPress_ChA THEN
    dwAlarm_Word_03_TMR_Discrepancies_Out := dwAlarm_Word_03_TMR_Discrepancies_Out OR 16#00000008; (* Bit 3: Melt Press ChA Fault *)
END_IF;
IF NOT bHealth_MeltPress_ChB THEN
    dwAlarm_Word_03_TMR_Discrepancies_Out := dwAlarm_Word_03_TMR_Discrepancies_Out OR 16#00000010; (* Bit 4: Melt Press ChB Fault *)
END_IF;
IF NOT bHealth_MeltPress_ChC THEN
    dwAlarm_Word_03_TMR_Discrepancies_Out := dwAlarm_Word_03_TMR_Discrepancies_Out OR 16#00000020; (* Bit 5: Melt Press ChC Fault *)
END_IF;
IF NOT bHealth_DieTemp_ChA THEN
    dwAlarm_Word_03_TMR_Discrepancies_Out := dwAlarm_Word_03_TMR_Discrepancies_Out OR 16#00000040; (* Bit 6: Die Temp ChA Fault *)
END_IF;
IF NOT bHealth_DieTemp_ChB THEN
    dwAlarm_Word_03_TMR_Discrepancies_Out := dwAlarm_Word_03_TMR_Discrepancies_Out OR 16#00000080; (* Bit 7: Die Temp ChB Fault *)
END_IF;
IF NOT bHealth_DieTemp_ChC THEN
    dwAlarm_Word_03_TMR_Discrepancies_Out := dwAlarm_Word_03_TMR_Discrepancies_Out OR 16#00000100; (* Bit 8: Die Temp ChC Fault *)
END_IF;
IF NOT bHealth_MoldN2_ChA THEN
    dwAlarm_Word_03_TMR_Discrepancies_Out := dwAlarm_Word_03_TMR_Discrepancies_Out OR 16#00000200; (* Bit 9: Mold N2 ChA Fault *)
END_IF;
IF NOT bHealth_MoldN2_ChB THEN
    dwAlarm_Word_03_TMR_Discrepancies_Out := dwAlarm_Word_03_TMR_Discrepancies_Out OR 16#00000400; (* Bit 10: Mold N2 ChB Fault *)
END_IF;
IF NOT bHealth_MoldN2_ChC THEN
    dwAlarm_Word_03_TMR_Discrepancies_Out := dwAlarm_Word_03_TMR_Discrepancies_Out OR 16#00000800; (* Bit 11: Mold N2 ChC Fault *)
END_IF;
IF bLatch_Alarm_TMR_Discrepancy THEN
    dwAlarm_Word_03_TMR_Discrepancies_Out := dwAlarm_Word_03_TMR_Discrepancies_Out OR 16#00001000; (* Bit 12: Dual Disagreement Trip *)
END_IF;

(* Alarm Word 4: Priority 4 Hydraulic, Extrusion & Cooling Process Deviations *)
dwAlarm_Word_04_ProcessDeviations_Out := 16#00000000;
IF NOT bChilled_Water_Flow_Confirmed_In THEN
    dwAlarm_Word_04_ProcessDeviations_Out := dwAlarm_Word_04_ProcessDeviations_Out OR 16#00000001; (* Bit 0: Chilled Flow Unconfirmed *)
END_IF;
IF NOT bNitrogen_Supply_Pressure_OK_In THEN
    dwAlarm_Word_04_ProcessDeviations_Out := dwAlarm_Word_04_ProcessDeviations_Out OR 16#00000002; (* Bit 1: N2 Supply Unconfirmed *)
END_IF;
IF NOT bFlash_Granulator_Ready_In THEN
    dwAlarm_Word_04_ProcessDeviations_Out := dwAlarm_Word_04_ProcessDeviations_Out OR 16#00000004; (* Bit 2: Granulator Not Ready *)
END_IF;
""")

    # -------------------------------------------------------------------------
    # FOOTER
    # -------------------------------------------------------------------------
    out.append("""END_FUNCTION_BLOCK
""")

    return "\n".join(out)

if __name__ == "__main__":
    st_code = build_full_st_code()
    print(f"Generated ST code length: {len(st_code)} characters")

    user_prompt = """You are Lumina's Elite Synthetic Data Architect for IEC 61131-3 Programmable Logic Controllers (V7 Max-Persona: 75+ years Principal Automation Fellow & Cyber-Physical Systems Chair).

Target Function Block: `FB_Plastics_EBM_FuelTank_ParisonControl_Sync`
Sector: Heavy Commercial Manufacturing - Plastics & Polymer Processing: Continuous 6-Layer Co-Extrusion Blow Molding (EBM) Automotive Fuel Tank Line (100-point axial/radial wall thickness distribution system WDS, electro-hydraulic servo tooling gap, parison sag & swell dynamics, mold nitrogen gas blow, active pre-pinch robotic manipulation).
Target Output File: `data/swarm_raw/agent_63a81fe2.json`

MANDATORY ARCHITECTURAL & MATHEMATICAL SPECIFICATIONS:
1. Extreme Depth & Rigor: Massively exhaustive, deeply engineered code (250,000+ characters). Zero summaries, zero placeholders, zero `// ... rest of code`. Every matrix, equation, timer, and state transition MUST be fully written out.
2. Discrete State-Space Model (12 States, 4 Inputs, 6 Outputs):
   - States: Parison tip vertical position, parison sag elongation strain, radial die swell ratio, melt temperature at die exit, inner layer HDPE thickness, EVOH barrier layer thickness, die gap hydraulic servo spool position, extruder head pressure, parison internal pre-blow pressure, parison pinch-off weld temperature, mold nitrogen inflation pressure, mold cavity cooling surface heat flux.
   - Fully unrolled matrix update: x_{k+1} = A * x_k + B * u_k, y_k = C * x_k + D * u_k.
   - Discrete steady-state Kalman Filter: x_hat_{k|k} = x_hat_{k|k-1} + L * (y_meas - C * x_hat_{k|k-1}).
3. Model Predictive Control (MPC):
   - Unrolled 10-step horizon Projected Gradient Descent (PGD).
   - Quadratic stage cost: (x - x_ref)^T * Q * (x - x_ref) + u^T * R * u.
   - High-speed electro-hydraulic servo valve bandwidth and gap acceleration constraints.
4. Triple Modular Redundant (TMR) 2oo3 Voting Logic:
   - 4 safety-critical channels: Die Gap LVDT Servo Position Sensors (ChA, ChB, ChC), Co-Extrusion Melt Pressure Transducers (ChA, ChB, ChC), Die Orifice IR Pyrometers (ChA, ChB, ChC), Mold Cavity Nitrogen Gas Pressure Sensors (ChA, ChB, ChC).
   - Discrepancy timers (15ms), bumpless degradation to 1oo2, and fail-safe tool gap freeze on dual disagreement.
5. 14-Stage Production FSM:
   - CASE State OF:
     0: IDLE_SAFE_STANDBY
     1: EXTRUDER_MELT_TEMPERATURE_HOMOGENIZATION
     2: DIE_GAP_CALIBRATION_ZERO_SEEKING
     3: PARISON_CONTINUOUS_EXTRUSION_PROFILE_RAMP
     4: 100_POINT_WDS_SERVO_GAP_SYNCHRONIZATION
     5: PRE_BLOW_AIR_INJECTION_PARISON_SHAPING
     6: ROBOTIC_BOTTOM_PRE_PINCH_MANIPULATION
     7: MOLD_CLAMPING_HIGH_TONNAGE_LOCK
     8: BLOW_PIN_INSERTION_HIGH_PRESSURE_N2_BLOW
     9: IN_MOLD_CRYOGENIC_COOLING_CYCLE
     10: EXHAUST_DEPRESSURIZATION_DEFLATION
     11: MOLD_OPENING_PART_GRIPPER_EXTRACTION
     12: FLASH_DEFLASHING_PUNCH_TRIM_CYCLE
     13: EMERGENCY_PARISON_DROP_PURGE_TRIP
   - Fully detailed transitions, interlocks, timeout fault traps, and diagnostic tracking.
6. ANSI/ISA-18.2 Multi-Tiered Alarm Engine:
   - HH (Trip), H (Warning), L (Low Warning), LL (Low Trip) for all critical physical variables.
   - Configurable hysteresis deadbands, persistence timers, alarm suppression during startup, and bit-packed DWORD alarm registers.
7. 100% Exact Syntax & Parity:
   - Triple backticks with `iec-st`.
   - First line: `FUNCTION_BLOCK FB_Plastics_EBM_FuelTank_ParisonControl_Sync`
   - Last line: `END_FUNCTION_BLOCK`
   - Every IF has END_IF;, every CASE has END_CASE;, every FOR has END_FOR;.
8. Save format:
   - Format strictly as a JSON object:
     `{"messages": [{"role": "user", "content": "..."}, {"role": "assistant", "content": "```iec-st\\n...\\n```"}]}`
   - Save to `data/swarm_raw/agent_63a81fe2.json`.
   - Run `python validate_iec.py data/swarm_raw/agent_63a81fe2.json` to verify 0 errors."""

    dataset = {
        "messages": [
            {"role": "user", "content": user_prompt},
            {"role": "assistant", "content": f"```iec-st\n{st_code}\n```"}
        ]
    }

    output_path = "data/swarm_raw/agent_63a81fe2.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)

    print(f"Successfully saved to {output_path}")
