# generate_tobacco_code.py
"""
Lumina Swarm V7 Max-Persona IEC 61131-3 Structured Text Synthesizer
Domain: High-Speed Consumer Goods & Tobacco Processing Machinery
System: Ultra-High-Speed Cigarette Maker (20,000 cpm / 333 Hz rod velocity, v_rod = 27.78 m/s)
Function Block: FB_Tobacco_CigaretteMaker_HighSpeed_WeightWeight
"""

import sys
import os
import json
import uuid
import re

def build_iec_code():
    chunks = []
    
    # -------------------------------------------------------------------------
    # 1. HEADER & ARCHITECTURAL OVERVIEW
    # -------------------------------------------------------------------------
    chunks.append('''FUNCTION_BLOCK FB_Tobacco_CigaretteMaker_HighSpeed_WeightWeight
(*
====================================================================================================
 LUMINA CYBER-PHYSICAL AUTOMATION ARCHITECTURE - V7 MAX-PERSONA SPECIFICATION
 CORE SECTOR  : HIGH-SPEED CONSUMER GOODS & TOBACCO PROCESSING MACHINERY
 SUBSYSTEM    : ULTRA-HIGH-SPEED CONTINUOUS CIGARETTE MAKER & FILTER ASSEMBLER (20,000 CPM / 333 HZ)
                CONTINUOUS SUCTION BAND ROD FORMER, HOPPER CHIMNEY FLUIDIZED INFEED,
                MULTI-POINT MICROWAVE RESONANT CAVITY DENSITY & DIELECTRIC LOSS PROFILER,
                HIGH-FREQUENCY DUAL-AXIS LASER MICROMETER FOR DIAMETER & OVALITY (50 KHZ),
                ELECTRONIC CAM FLYING SHEAR ROTARY CUTOFF KNIFE WITH SHARPENING STONE PROFILER,
                FILTER TIP ATTACHMENT FLUTED VACUUM TRANSFER DRUMS & TIPPING GLUING NOZZLE,
                HIGH-SPEED CO2 LASER PERFORATION FOR ONLINE FILTER VENTILATION DILUTION,
                DUAL-WAVELENGTH OPTICAL DENSITY & LOOSE-END TOBACCO VOID SCANNER,
                ULTRA-FAST 40-BAR COMPRESSED AIR SOLENOID DEFECT EJECTION BUS (< 1.2 MS RESPONSE).
 DESIGNATION   : ISA-5.1 / IEC 61131-3 INDUSTRIAL CONTROL SYSTEM ARCHITECTURE
 CYBER-PHYSICS : 8x8 DISCRETE STATE-SPACE (Ts = 0.5 ms / 2,000 Hz) WITH KALMAN OBSERVER
 OPTIMIZATION  : RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) PROJECTED GRADIENT DESCENT
 REDUNDANCY    : 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) WITH PERSISTENCE TIMERS & BUMPLESS DEGRADATION
 SAFETY/ALARM  : ISA-18.2 FIVE-TIER MULTI-PARAMETRIC ALARM ENGINE WITH 32-BIT DWORD PACKING
 FSM TOPOLOGY  : 12-STAGE DETERMINISTIC FINITE STATE MACHINE (STATES 0 TO 11)
====================================================================================================

MATHEMATICAL CYBER-PHYSICAL FORMULATIONS:
----------------------------------------------------------------------------------------------------
1. Porous Suction Band Bernoulli Aerodynamics:
   DeltaP_vac = 0.5 * rho_air * v_suction^2 + (mu_air / k_permeability) * L_bed * v_flow
   Mass flow rate into garniture: dm/dt = rho_bulk * W_chimney * H_trim * v_rod

2. Dual-Frequency Microwave Resonant Cavity Perturbation Theory (2.45 GHz & 5.80 GHz):
   Delta_f0 / f0 = -0.5 * (eps_r' - 1) * (V_sample / V_cavity)
   Delta(1 / Q_L) = eps_r'' * (V_sample / V_cavity)
   Rod mass:      m_rod = a1 * Delta_f0 + a2 * Delta(1/Q_L) + a3 * T_rod + b0   [mg/rod]
   Rod moisture:  M_pct = g1 * (Delta(1/Q_L) / Delta_f0) + g2 * T_rod + d0      [%]

3. Rotary Knife Flying Shear Kinematic Synchronization:
   Rod cutoff velocity matching at tangential apex:
   v_knife_x(theta) = omega_knife * R_knife * cos(theta_lead) == v_rod (27.78 m/s at 20,000 cpm)
   5th-Order Cam Polynomial Trajectory:
   s(tau) = 10*tau^3 - 15*tau^4 + 6*tau^5, where tau = (t - t_sync_start) / T_sync_window

4. Active Knife Wear Kinetics & Sharpening Stone Feed:
   Wear rate: dr_edge/dt = c_abrasion * (m_rod * v_rod) * (1 - Lubrication_factor)
   Acoustic emission RMS: AE_rms = k_ae * (r_edge / r_sharp)^1.5 + noise

5. Online Filter Ventilation Perforation Hydrodynamics:
   Dilution Ratio: V_vent = (Q_perforation / Q_total_smoke) * 100%
   Perforation flow: Q_perf = C_d * N_holes * A_hole * sqrt(2 * DeltaP_insp / rho_air)

6. Receding-Horizon MPC Quadratic Cost Objective:
   J(u) = Sum_{k=0}^{N-1} [ (x_k - r_k)^T * Q * (x_k - r_k) + u_k^T * R * u_k ] + (x_N - r_N)^T * P * (x_N - r_N)
   Constrained by: u_min <= u_k <= u_max, and |u_{k} - u_{k-1}| <= Delta_u_max
====================================================================================================
*)
''')

    # -------------------------------------------------------------------------
    # 2. VAR_INPUT BLOCK
    # -------------------------------------------------------------------------
    chunks.append('''
VAR_INPUT
    (* ========================================================================================= *)
    (* 1. 2oo3 TMR TRIAD: MICROWAVE RESONANT CAVITY DENSITY SENSORS                              *)
    (* ========================================================================================= *)
    AI_MW_Density_ChA                : REAL := 950.000;  (* Microwave Cavity Sensor Channel A Tobacco Mass [mg/rod] *)
    AI_MW_Density_ChB                : REAL := 950.000;  (* Microwave Cavity Sensor Channel B Tobacco Mass [mg/rod] *)
    AI_MW_Density_ChC                : REAL := 950.000;  (* Microwave Cavity Sensor Channel C Tobacco Mass [mg/rod] *)

    (* ========================================================================================= *)
    (* 2. 2oo3 TMR TRIAD: MICROWAVE DIELECTRIC LOSS MOISTURE SENSORS                             *)
    (* ========================================================================================= *)
    AI_MW_Moisture_ChA               : REAL := 12.500;   (* Microwave Resonant Loss Channel A Moisture Content [%] *)
    AI_MW_Moisture_ChB               : REAL := 12.500;   (* Microwave Resonant Loss Channel B Moisture Content [%] *)
    AI_MW_Moisture_ChC               : REAL := 12.500;   (* Microwave Resonant Loss Channel C Moisture Content [%] *)

    (* ========================================================================================= *)
    (* 3. 2oo3 TMR TRIAD: HIGH-FREQUENCY DUAL-AXIS LASER DIAMETER GAUGES                         *)
    (* ========================================================================================= *)
    AI_Laser_Dia_ChA                 : REAL := 7.800;    (* High-Speed Laser Optical Gauge Channel A Outer Diameter [mm] *)
    AI_Laser_Dia_ChB                 : REAL := 7.800;    (* High-Speed Laser Optical Gauge Channel B Outer Diameter [mm] *)
    AI_Laser_Dia_ChC                 : REAL := 7.800;    (* High-Speed Laser Optical Gauge Channel C Outer Diameter [mm] *)
    AI_Laser_Ovality_ChA             : REAL := 0.015;    (* Laser Micrometer Channel A Cross-Axis Ovality Deviation [mm] *)
    AI_Laser_Ovality_ChB             : REAL := 0.015;    (* Laser Micrometer Channel B Cross-Axis Ovality Deviation [mm] *)

    (* ========================================================================================= *)
    (* 4. 2oo3 TMR TRIAD: MAIN LINE SHAFT VIRTUAL MASTER SERVO VELOCITY ENCODERS                 *)
    (* ========================================================================================= *)
    AI_LineShaft_Speed_ChA           : REAL := 27.778;   (* Line Shaft Master Virtual Axis Speed Channel A [m/s] *)
    AI_LineShaft_Speed_ChB           : REAL := 27.778;   (* Line Shaft Master Virtual Axis Speed Channel B [m/s] *)
    AI_LineShaft_Speed_ChC           : REAL := 27.778;   (* Line Shaft Master Virtual Axis Speed Channel C [m/s] *)

    (* ========================================================================================= *)
    (* 5. 2oo3 TMR TRIAD: FLUTED TRANSFER DRUM PNEUMATIC VACUUM MANIFOLD TRANSMITTERS            *)
    (* ========================================================================================= *)
    AI_Drum_Vacuum_ChA               : REAL := -75.000;  (* Fluted Transfer Drum Vacuum Differential Channel A [kPa] *)
    AI_Drum_Vacuum_ChB               : REAL := -75.000;  (* Fluted Transfer Drum Vacuum Differential Channel B [kPa] *)
    AI_Drum_Vacuum_ChC               : REAL := -75.000;  (* Fluted Transfer Drum Vacuum Differential Channel C [kPa] *)

    (* ========================================================================================= *)
    (* 6. ANCILLARY PROCESS TRANSDUCERS & CYBER-PHYSICAL FEEDBACK                                *)
    (* ========================================================================================= *)
    AI_Hopper_Tobacco_Level_pct      : REAL := 65.000;   (* Distributor Chimney Tobacco Reservoir Bed Height [%] *)
    AI_Infeed_Tobacco_Temp_degC      : REAL := 22.500;   (* Infeed Shredded Cut-Rag Bulk Temperature [deg C] *)
    AI_Garniture_Tape_Tension_N      : REAL := 145.000;  (* Endless Garniture Woven Drive Belt Tension [N] *)
    AI_Seam_Sealer_Temp_degC         : REAL := 245.000;  (* Heated Seam Sealing Iron Tongue Temperature [deg C] *)
    AI_Seam_Glue_Pressure_bar        : REAL := 3.800;    (* Longitudinal Seam PVA Adhesive Metering Pressure [bar] *)
    AI_Tipping_Paper_Tension_N       : REAL := 28.500;   (* Filter Tipping Paper Unwind Web Tension [N] *)
    AI_Tipping_Glue_Temp_degC        : REAL := 160.000;  (* Hot-Melt Adhesive Glue Station Reservoir Temperature [deg C] *)
    AI_Laser_Perf_Power_W            : REAL := 85.000;   (* Multi-Beam CO2 Perforation Laser Emitted Power [W] *)
    AI_Knife_Vibration_RMS_mms       : REAL := 3.400;    (* Rotary Cutoff Knife Spindle Accelerometer RMS Velocity [mm/s] *)
    AI_Sharpening_Current_A          : REAL := 2.100;    (* Sharpening Stone Feed Stepper Motor Current [A] *)
    AI_Reject_Air_Pressure_bar       : REAL := 42.000;   (* High-Speed Solenoid Blow-Off Air Reservoir Pressure [bar] *)
    AI_LooseEnd_Optical_Depth_mm     : REAL := 0.850;    (* Dual-Wavelength Optical Loose-End Void Detection Depth [mm] *)
    DI_Filter_Plug_Present           : BOOL := TRUE;     (* Fluted Drum Optical Proximity Filter Plug Interlock [BOOL] *)
    AI_Splicer_Bobbin_Angle_deg      : REAL := 45.000;   (* Auto-Splicer Dual Turret Paper Reel Turntable Angle [deg] *)

    (* ========================================================================================= *)
    (* 7. OPERATOR SETPOINTS & TIMING CONTROLS                                                   *)
    (* ========================================================================================= *)
    rSP_Target_Weight_mg             : REAL := 950.000;  (* Nominal Cigarette Rod Mass Setpoint [mg/rod] *)
    rSP_Target_Moisture_pct          : REAL := 12.500;   (* Nominal Finished Rod Moisture Equilibrium Setpoint [%] *)
    rSP_Target_Diameter_mm           : REAL := 7.800;    (* Nominal Cigarette Rod Outside Diameter Setpoint [mm] *)
    rSP_Target_Ventilation_pct       : REAL := 35.000;   (* Target Online Filter Ventilation Dilution Ratio Setpoint [%] *)
    rSP_Production_Rate_cpm          : REAL := 20000.000;(* Target Master Cigarette Machine Velocity [cpm] *)
    tDelta_s                         : REAL := 0.000500; (* High-Speed PLC Task Execution Interval (0.5 ms) [s] *)
    bCmd_Machine_Run                 : BOOL := FALSE;    (* Master Operational Run Command From Line HMI [BOOL] *)
    bCmd_Auto_Splice                 : BOOL := FALSE;    (* Manual Or Automated Paper Reel Flying Splice Command [BOOL] *)
    bCmd_Manual_Sharpen              : BOOL := FALSE;    (* Operator Commanded Knife Infeed Sharpening Cycle [BOOL] *)
    bCmd_Alarm_Ack                   : BOOL := FALSE;    (* Master Alarm Reset & Acknowledgment Command [BOOL] *)
    bSafety_Circuit_OK               : BOOL := TRUE;     (* Hardwired Dual-Channel Guard & Knife Interlock PLe [BOOL] *)
END_VAR
''')

    # -------------------------------------------------------------------------
    # 3. VAR_OUTPUT BLOCK
    # -------------------------------------------------------------------------
    chunks.append('''
VAR_OUTPUT
    (* ========================================================================================= *)
    (* 1. HIGH-SPEED ACTUATION COMMANDS & SERVO TRIM OFFSETS                                      *)
    (* ========================================================================================= *)
    rCmd_Trimmer_Height_mm           : REAL := 0.000;    (* Trimming Disc Linear Servo Position Adjustment [mm] *)
    rCmd_Garniture_Velocity_ms       : REAL := 0.000;    (* Garniture Forming Tape Synchronous Drive Velocity [m/s] *)
    rCmd_Knife_Phase_Advance_mrad    : REAL := 0.000;    (* Rotary Cutoff Knife Electronic Cam Phase Correction [mrad] *)
    rCmd_Knife_Angular_Speed_rads    : REAL := 0.000;    (* Rotary Cutoff Knife Master Angular Velocity [rad/s] *)
    rCmd_Laser_DutyCycle_pct         : REAL := 0.000;    (* CO2 Perforation Laser PWM Firing Pulse Width [%] *)
    rCmd_Laser_Pulse_Freq_Hz         : REAL := 0.000;    (* CO2 Perforation Laser Optical Pulse Frequency [Hz] *)
    rCmd_Vacuum_Blower_VFD_Hz        : REAL := 0.000;    (* Suction Band & Vacuum Drum Inverter Frequency Command [Hz] *)
    rCmd_Seam_Sealer_Power_pct       : REAL := 0.000;    (* Seam Sealing Iron Solid State Relay Duty Cycle [%] *)
    bCmd_Sharpening_Step_Pulse       : BOOL := FALSE;    (* Micro-Stepping Pulse To Knife Infeed Grinding Stone [BOOL] *)
    bCmd_Splicer_Actuate             : BOOL := FALSE;    (* Pneumatic Flying Splice Knife Clamp & Tape Trigger [BOOL] *)
    abReject_Air_Blast_Trig          : ARRAY[1..8] OF BOOL; (* Ultra-Fast 40-Bar Reject Solenoid Pulse Outputs [BOOL] *)

    (* ========================================================================================= *)
    (* 2. PROCESS TELEMETRY & ARBITRATED SENSOR VALUES                                           *)
    (* ========================================================================================= *)
    rVoted_Rod_Weight_mg             : REAL := 950.000;  (* Arbitrated 2oo3 Rod Mass Telemetry [mg/rod] *)
    rVoted_Rod_Moisture_pct          : REAL := 12.500;   (* Arbitrated 2oo3 Rod Moisture Content Telemetry [%] *)
    rVoted_Rod_Diameter_mm           : REAL := 7.800;    (* Arbitrated 2oo3 Rod Outside Diameter Telemetry [mm] *)
    rVoted_Line_Speed_ms             : REAL := 0.000;    (* Arbitrated 2oo3 Virtual Line Shaft Speed [m/s] *)
    rVoted_Drum_Vacuum_kPa           : REAL := 0.000;    (* Arbitrated 2oo3 Drum Transfer Vacuum Level [kPa] *)
    rCalc_Ventilation_pct            : REAL := 0.000;    (* Hydrodynamically Modeled Ventilation Dilution Ratio [%] *)
    rStat_Weight_StdDev_mg           : REAL := 0.000;    (* Online Welford Running Standard Deviation Of Weight [mg] *)
    rStat_Weight_Mean_mg             : REAL := 950.000;  (* Online Running Arithmetic Mean Of Cigarette Weight [mg] *)
    rDiag_Knife_Wear_Pct             : REAL := 0.000;    (* Blade Dullness / Edge Erosion Degradation Index [%] *)

    (* ========================================================================================= *)
    (* 3. PRODUCTION ACCOUNTING, STATE MACHINE & ALARM REGISTERS                                 *)
    (* ========================================================================================= *)
    udiCount_Produced                : UDINT := 0;       (* Total Good Cigarette Rods Cut & Transferred [UDINT] *)
    udiCount_Rejected                : UDINT := 0;       (* Total Out-Of-Spec Cigarettes Ejected By Blast Solenoid [UDINT] *)
    udiCount_Weight_Rejects          : UDINT := 0;       (* Rejects Due To Tobacco Mass Deviation Counter [UDINT] *)
    udiCount_LooseEnd_Rejects        : UDINT := 0;       (* Rejects Due To Loose End Tobacco Cavity Counter [UDINT] *)
    iFSM_State                       : INT := 0;         (* Current 12-Stage Deterministic FSM Operational State [INT] *)
    dwAlarms_Critical                : DWORD := 16#00000000; (* ISA-18.2 Priority 1 Hard Trip & Clamp Alarms [DWORD] *)
    dwAlarms_Warning                 : DWORD := 16#00000000; (* ISA-18.2 Priority 2 Process Out-Of-Bounds Warnings [DWORD] *)
    dwAlarms_Diagnostic              : DWORD := 16#00000000; (* ISA-18.2 Priority 3 Sensor Fault & Discrepancy Reg [DWORD] *)
    bSystem_Ready_20k                : BOOL := FALSE;    (* Machine Qualified For Ultra-High-Speed 20,000 cpm Run [BOOL] *)
END_VAR
''')

    # -------------------------------------------------------------------------
    # 4. VAR BLOCK (INTERNAL MATRICES, ARRAYS, SHIFT REGISTERS)
    # -------------------------------------------------------------------------
    chunks.append('''
VAR
    (* ========================================================================================= *)
    (* 1. DISCRETE STATE-SPACE CYBER-PHYSICAL MATRICES (8-STATE x 4-INPUT x 8-OUTPUT)            *)
    (*    States: [1: d_Mass_mg, 2: Trimmer_Height_mm, 3: d_v_rod_ms, 4: d_eps_r_prime,         *)
    (*             5: d_Moisture_pct, 6: d_Cut_Phase_mrad, 7: d_Vent_pct, 8: d_Vac_Drum_kPa]    *)
    (*    Inputs: [1: u_Trimmer_Pos_cmd, 2: u_Garniture_Vel_trim, 3: u_Knife_Phase_trim,        *)
    (*             4: u_Laser_Duty_cmd]                                                          *)
    (* ========================================================================================= *)
    A_Matrix                         : ARRAY[1..8, 1..8] OF REAL; (* Discrete State Transition Matrix A *)
    B_Matrix                         : ARRAY[1..8, 1..4] OF REAL; (* Discrete Control Input Matrix B *)
    C_Matrix                         : ARRAY[1..8, 1..8] OF REAL; (* Discrete Measurement Matrix C *)
    D_Matrix                         : ARRAY[1..8, 1..4] OF REAL; (* Discrete Feedthrough Matrix D *)
    L_Kalman                         : ARRAY[1..8, 1..8] OF REAL; (* Steady-State Kalman Filter Observer Gain Matrix *)
    P_Riccati                        : ARRAY[1..8, 1..8] OF REAL; (* Discrete Algebraic Riccati Terminal Cost Matrix *)
    Q_Weights                        : ARRAY[1..8] OF REAL;       (* MPC State Tracking Error Cost Weights *)
    R_Weights                        : ARRAY[1..4] OF REAL;       (* MPC Actuator Control Effort Penalties *)
    x_State_Est                      : ARRAY[1..8] OF REAL;       (* Kalman Estimated Cyber-Physical State Vector *)
    x_State_Pred                     : ARRAY[1..8] OF REAL;       (* One-Step Ahead State Prediction Vector *)
    y_Meas                           : ARRAY[1..8] OF REAL;       (* Pre-Processed Sensor Measurement Vector *)
    y_Est                            : ARRAY[1..8] OF REAL;       (* Observer Reconstructed Measurement Vector *)
    u_MPC                            : ARRAY[1..4] OF REAL;       (* Optimal Control Actuation Command Vector *)
    u_MPC_Prev                       : ARRAY[1..4] OF REAL;       (* Preceding Step Control Actuation Vector *)
    r_Reference                      : ARRAY[1..8] OF REAL;       (* Setpoint Reference Vector *)
    e_Tracking                       : ARRAY[1..8] OF REAL;       (* State Regulation Error Vector (x - r) *)
    grad_J                           : ARRAY[1..4] OF REAL;       (* Receding-Horizon Gradient Vector *)
    bInit_Done                       : BOOL := FALSE;            (* One-Time Initialization Completed Flag *)

    (* ========================================================================================= *)
    (* 2. 2oo3 TMR VOTING DATA STRUCTURES & DISCREPANCY TIMERS (5 SENSOR TRIADS)                 *)
    (* ========================================================================================= *)
    (* Triad 1: Microwave Density Sensors *)
    rDensity_Med                     : REAL := 950.0;
    rDensity_Dev_AB                  : REAL := 0.0;
    rDensity_Dev_BC                  : REAL := 0.0;
    rDensity_Dev_CA                  : REAL := 0.0;
    rDensity_Timer_A                 : REAL := 0.0;
    rDensity_Timer_B                 : REAL := 0.0;
    rDensity_Timer_C                 : REAL := 0.0;
    bDensity_Fault_A                 : BOOL := FALSE;
    bDensity_Fault_B                 : BOOL := FALSE;
    bDensity_Fault_C                 : BOOL := FALSE;
    iDensity_Healthy_Count           : INT := 3;

    (* Triad 2: Microwave Moisture Sensors *)
    rMoisture_Med                    : REAL := 12.5;
    rMoisture_Dev_AB                 : REAL := 0.0;
    rMoisture_Dev_BC                 : REAL := 0.0;
    rMoisture_Dev_CA                 : REAL := 0.0;
    rMoisture_Timer_A                : REAL := 0.0;
    rMoisture_Timer_B                : REAL := 0.0;
    rMoisture_Timer_C                : REAL := 0.0;
    bMoisture_Fault_A                : BOOL := FALSE;
    bMoisture_Fault_B                : BOOL := FALSE;
    bMoisture_Fault_C                : BOOL := FALSE;
    iMoisture_Healthy_Count          : INT := 3;

    (* Triad 3: Laser Diameter Gauges *)
    rDiameter_Med                    : REAL := 7.80;
    rDiameter_Dev_AB                 : REAL := 0.0;
    rDiameter_Dev_BC                 : REAL := 0.0;
    rDiameter_Dev_CA                 : REAL := 0.0;
    rDiameter_Timer_A                : REAL := 0.0;
    rDiameter_Timer_B                : REAL := 0.0;
    rDiameter_Timer_C                : REAL := 0.0;
    bDiameter_Fault_A                : BOOL := FALSE;
    bDiameter_Fault_B                : BOOL := FALSE;
    bDiameter_Fault_C                : BOOL := FALSE;
    iDiameter_Healthy_Count          : INT := 3;

    (* Triad 4: Line Shaft Speed Encoders *)
    rLineSpeed_Med                   : REAL := 27.778;
    rLineSpeed_Dev_AB                : REAL := 0.0;
    rLineSpeed_Dev_BC                : REAL := 0.0;
    rLineSpeed_Dev_CA                : REAL := 0.0;
    rLineSpeed_Timer_A               : REAL := 0.0;
    rLineSpeed_Timer_B               : REAL := 0.0;
    rLineSpeed_Timer_C               : REAL := 0.0;
    bLineSpeed_Fault_A               : BOOL := FALSE;
    bLineSpeed_Fault_B               : BOOL := FALSE;
    bLineSpeed_Fault_C               : BOOL := FALSE;
    iLineSpeed_Healthy_Count         : INT := 3;

    (* Triad 5: Drum Fluted Vacuum Transmitters *)
    rDrumVac_Med                     : REAL := -75.0;
    rDrumVac_Dev_AB                  : REAL := 0.0;
    rDrumVac_Dev_BC                  : REAL := 0.0;
    rDrumVac_Dev_CA                  : REAL := 0.0;
    rDrumVac_Timer_A                 : REAL := 0.0;
    rDrumVac_Timer_B                 : REAL := 0.0;
    rDrumVac_Timer_C                 : REAL := 0.0;
    bDrumVac_Fault_A                 : BOOL := FALSE;
    bDrumVac_Fault_B                 : BOOL := FALSE;
    bDrumVac_Fault_C                 : BOOL := FALSE;
    iDrumVac_Healthy_Count           : INT := 3;

    (* ========================================================================================= *)
    (* 3. 128-STAGE SYNCHRONOUS FIFO TRACKING SHIFT REGISTER FOR DEFECT DISCHARGE               *)
    (*    Index 1   : Cutoff Knife Flying Shear Separation Point                                 *)
    (*    Index 18  : Microwave Density & Moisture Resonant Cavity Station                       *)
    (*    Index 34  : High-Speed Dual-Axis Laser Micrometer Station                              *)
    (*    Index 58  : Filter Tip Attachment & Tipping Paper Glue Roll Drum                       *)
    (*    Index 76  : Dual-Wavelength Optical Loose-End Void Scanner                             *)
    (*    Index 94  : Laser Ventilation Perforation Focal Inspection Station                     *)
    (*    Index 116 : Ultra-Fast 40-Bar Reject Solenoid Air Blast Nozzle Array                   *)
    (*    Index 128 : Accepted Cigarette Collator Belt Drum Transfer Point                       *)
    (* ========================================================================================= *)
    sr_Cig_ID                        : ARRAY[1..128] OF UDINT;
    sr_Weight_mg                     : ARRAY[1..128] OF REAL;
    sr_Moisture_pct                  : ARRAY[1..128] OF REAL;
    sr_Diameter_mm                   : ARRAY[1..128] OF REAL;
    sr_LooseEnd_Depth_mm             : ARRAY[1..128] OF REAL;
    sr_Ventilation_pct               : ARRAY[1..128] OF REAL;
    sr_Defect_Flags                  : ARRAY[1..128] OF WORD;
    sr_Eject_Command                 : ARRAY[1..128] OF BOOL;
    udiNextCigaretteID               : UDINT := 1;
    rReject_Pulse_Timer_s            : ARRAY[1..8] OF REAL;

    (* ========================================================================================= *)
    (* 4. ROTARY KNIFE FLYING SHEAR CAM PROFILE & KNIFE WEAR GRINDING STONE MODEL                *)
    (* ========================================================================================= *)
    rKnife_Shaft_Angle_rad           : REAL := 0.0;
    rKnife_Cut_Window_Phase_rad      : REAL := 0.0;
    rKnife_Sync_Phase_Error_rad      : REAL := 0.0;
    rCam_c0                          : REAL := 0.0;
    rCam_c1                          : REAL := 0.0;
    rCam_c2                          : REAL := 0.0;
    rCam_c3                          : REAL := 10.0;
    rCam_c4                          : REAL := -15.0;
    rCam_c5                          : REAL := 6.0;
    udiKnife_Total_Cuts              : UDINT := 0;
    udiKnife_Cuts_Since_Sharpen      : UDINT := 0;
    rKnife_Blade_Wear_Depth_um       : REAL := 0.0;
    rSharpening_Interval_Cuts        : UDINT := 25000;
    bSharpening_In_Progress          : BOOL := FALSE;
    rSharpening_Cycle_Timer_s        : REAL := 0.0;
    rSharpening_Feed_Pulse_Timer_s   : REAL := 0.0;

    (* ========================================================================================= *)
    (* 5. ONLINE WELFORD ALGORITHM FOR STATISTICAL QUALITY CONTROL (MASS VARIANCE)               *)
    (* ========================================================================================= *)
    udiWelford_Count                 : UDINT := 0;
    rWelford_Mean                    : REAL := 950.0;
    rWelford_M2                      : REAL := 0.0;
    rWelford_Variance                : REAL := 0.0;
    rWelford_Delta                   : REAL := 0.0;
    rWelford_Delta2                  : REAL := 0.0;

    (* ========================================================================================= *)
    (* 6. FINITE STATE MACHINE INTERNAL CONTROLS & TIMERS (STATES 0 TO 11)                       *)
    (* ========================================================================================= *)
    iFSM_Internal_State              : INT := 0;
    rFSM_State_Timer_s               : REAL := 0.0;
    bState_First_Scan                : BOOL := TRUE;
    rPurge_Duration_s                : REAL := 4.0;
    rSuction_Prime_Duration_s        : REAL := 3.0;
    rWeb_Thread_Duration_s           : REAL := 5.0;
    rBlade_Accel_Duration_s          : REAL := 4.0;
    rTest_Cut_Duration_s             : REAL := 3.0;
    rFilter_Sync_Duration_s          : REAL := 3.0;
    rQuality_Verify_Duration_s       : REAL := 4.0;
    rSplicer_Timer_s                 : REAL := 0.0;
    bSplicer_Sequence_Active         : BOOL := FALSE;
    rDecel_Ramp_Timer_s              : REAL := 0.0;
    rEmergency_Brake_Timer_s         : REAL := 0.0;

    (* ========================================================================================= *)
    (* 7. ISA-18.2 ALARM THRESHOLDS, DEADBANDS & PERSISTENCE REGISTERS                           *)
    (* ========================================================================================= *)
    rLimit_Weight_HH_mg              : REAL := 975.0;
    rLimit_Weight_H_mg               : REAL := 960.0;
    rLimit_Weight_L_mg               : REAL := 940.0;
    rLimit_Weight_LL_mg              : REAL := 925.0;
    rDeadband_Weight_mg              : REAL := 2.5;

    rLimit_Moisture_HH_pct           : REAL := 13.5;
    rLimit_Moisture_H_pct            : REAL := 12.8;
    rLimit_Moisture_L_pct            : REAL := 12.2;
    rLimit_Moisture_LL_pct           : REAL := 11.5;
    rDeadband_Moisture_pct           : REAL := 0.15;

    rLimit_Diameter_HH_mm            : REAL := 7.86;
    rLimit_Diameter_H_mm             : REAL := 7.83;
    rLimit_Diameter_L_mm             : REAL := 7.77;
    rLimit_Diameter_LL_mm            : REAL := 7.74;
    rDeadband_Diameter_mm            : REAL := 0.01;

    rLimit_Vacuum_LL_kPa             : REAL := -55.0;
    rLimit_Vacuum_L_kPa              : REAL := -65.0;
    rDeadband_Vacuum_kPa             : REAL := 2.0;

    rLimit_Knife_Vib_HH_mms          : REAL := 18.0;
    rLimit_Knife_Vib_H_mms           : REAL := 12.0;
    rDeadband_Knife_Vib_mms          : REAL := 1.0;

    rLimit_Seam_Temp_HH_degC         : REAL := 295.0;
    rLimit_Seam_Temp_LL_degC         : REAL := 210.0;
    rDeadband_Seam_Temp_degC         : REAL := 5.0;

    rDebounce_Weight_HH_s            : REAL := 0.0;
    rDebounce_Weight_LL_s            : REAL := 0.0;
    rDebounce_Vacuum_LL_s            : REAL := 0.0;
    rDebounce_Knife_HH_s             : REAL := 0.0;

    (* Temporary math variables & loop indices *)
    idx_i                            : INT := 1;
    idx_j                            : INT := 1;
    idx_k                            : INT := 1;
    rTemp_Sum                        : REAL := 0.0;
    rTemp_Val                        : REAL := 0.0;
    rTemp_Tau                        : REAL := 0.0;
    rTemp_CamPos                     : REAL := 0.0;
    rDelta_U                         : REAL := 0.0;
END_VAR
''')

    return chunks

print("Scaffold module compiled.")
