# -*- coding: utf-8 -*-
"""
Full Cyber-Physical Code Generator for FB_Steelmaking_6High_ColdReversingMill_AFC_Sync
"""

import sys
import os
import json
import re

def generate_iec_st():
    lines = []
    
    # Header
    lines.append("FUNCTION_BLOCK FB_Steelmaking_6High_ColdReversingMill_AFC_Sync")
    lines.append("(*")
    lines.append("=============================================================================================================")
    lines.append("LUMINA CYBER-PHYSICAL AUTOMATION ENGINE - ADVANCED HEAVY COMMERCIAL METALLURGY DIVISION")
    lines.append("FACILITY: 2,500 mm ULTRA-WIDE 6-HIGH COLD REVERSING STRIP ROLLING MILL STAND (CRM-01)")
    lines.append("MAX DESIGN SPEED: 1,800.0 [m/min] (30.0 [m/s]) | MAX PASS FORCE: 45,000.0 [kN] (4,500 Metric Tons)")
    lines.append("ACTUATION ARCHITECTURE:")
    lines.append("  1. HIGH-FREQUENCY HYDRAULIC AUTOMATIC GAUGE CONTROL (HAGC) VIA DUAL MOOG D664 SERVO VALVES")
    lines.append("  2. HYDRAULIC WORK ROLL BENDING (WRB) CROWN ACTUATION: [-1,500.0 .. +2,500.0 kN]")
    lines.append("  3. INTERMEDIATE ROLL (IR) AXIAL SHIFTING ACTUATION: [-350.0 .. +350.0 mm]")
    lines.append("  4. INTERMEDIATE ROLL BENDING (IRB) ACTUATION: [-1,200.0 .. +1,200.0 kN]")
    lines.append("  5. 40-ZONE SEGMENTED COOLANT SPRAY BAR AUTOMATIC FLATNESS CONTROL (AFC) ACROSS 2,500 mm STRIP")
    lines.append("REDUNDANCY ARCHITECTURE:")
    lines.append("  4-CHANNEL 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING WITH DUAL-DISAGREEMENT QUICK-OPEN SAFETY")
    lines.append("ADVANCED CONTROL ARCHITECTURE:")
    lines.append("  12-STATE, 4-INPUT, 6-OUTPUT FIRST-PRINCIPLES CYBER-PHYSICAL STATE-SPACE DISCRETE KALMAN OBSERVER")
    lines.append("  10-STEP UNROLLED RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) WITH PROJECTED GRADIENT DESCENT (PGD)")
    lines.append("  14-STAGE DETERMINISTIC REVERSING MILL FINITE STATE MACHINE (FSM)")
    lines.append("  ANSI/ISA-18.2 MULTI-TIER ALARM ENGINE (HH/H/L/LL) WITH RUNTIME SUPPRESSION & PERSISTENCE TIMERS")
    lines.append("=============================================================================================================")
    lines.append("*)")
    lines.append("")
    
    # VAR_INPUT
    lines.append("VAR_INPUT")
    lines.append("    (* ========================================================================= *)")
    lines.append("    (* 2oo3 REDUNDANT CHANNEL 1: TOTAL ROLL FORCE LOAD CELLS [kN]                *)")
    lines.append("    (* ========================================================================= *)")
    lines.append("    rRollForce_DS_ChA_kN                : REAL;   (* Drive Side Load Cell Channel A Force Measurement [kN] *)")
    lines.append("    rRollForce_DS_ChB_kN                : REAL;   (* Drive Side Load Cell Channel B Force Measurement [kN] *)")
    lines.append("    rRollForce_DS_ChC_kN                : REAL;   (* Drive Side Load Cell Channel C Force Measurement [kN] *)")
    lines.append("    bRollForce_DS_ChA_Valid             : BOOL;   (* Drive Side Load Cell Channel A Signal Integrity Permissive [-] *)")
    lines.append("    bRollForce_DS_ChB_Valid             : BOOL;   (* Drive Side Load Cell Channel B Signal Integrity Permissive [-] *)")
    lines.append("    bRollForce_DS_ChC_Valid             : BOOL;   (* Drive Side Load Cell Channel C Signal Integrity Permissive [-] *)")
    lines.append("    rRollForce_OS_ChA_kN                : REAL;   (* Operator Side Load Cell Channel A Force Measurement [kN] *)")
    lines.append("    rRollForce_OS_ChB_kN                : REAL;   (* Operator Side Load Cell Channel B Force Measurement [kN] *)")
    lines.append("    rRollForce_OS_ChC_kN                : REAL;   (* Operator Side Load Cell Channel C Force Measurement [kN] *)")
    lines.append("    bRollForce_OS_ChA_Valid             : BOOL;   (* Operator Side Load Cell Channel A Signal Integrity Permissive [-] *)")
    lines.append("    bRollForce_OS_ChB_Valid             : BOOL;   (* Operator Side Load Cell Channel B Signal Integrity Permissive [-] *)")
    lines.append("    bRollForce_OS_ChC_Valid             : BOOL;   (* Operator Side Load Cell Channel C Signal Integrity Permissive [-] *)")
    lines.append("")
    lines.append("    (* ========================================================================= *)")
    lines.append("    (* 2oo3 REDUNDANT CHANNEL 2: EXIT STRIP THICKNESS GAUGES [mm]                *)")
    lines.append("    (* ========================================================================= *)")
    lines.append("    rExitThickness_ChA_mm               : REAL;   (* Primary Scintillation Isotope/X-Ray Thickness Sensor Ch A [mm] *)")
    lines.append("    rExitThickness_ChB_mm               : REAL;   (* Secondary High-Speed Laser/Isotope Thickness Sensor Ch B [mm] *)")
    lines.append("    rExitThickness_ChC_mm               : REAL;   (* Tertiary Solid-State Silicon Drift Detector Thickness Ch C [mm] *)")
    lines.append("    bExitThickness_ChA_Valid            : BOOL;   (* Thickness Gauge Channel A Diagnostic OK Permissive [-] *)")
    lines.append("    bExitThickness_ChB_Valid            : BOOL;   (* Thickness Gauge Channel B Diagnostic OK Permissive [-] *)")
    lines.append("    bExitThickness_ChC_Valid            : BOOL;   (* Thickness Gauge Channel C Diagnostic OK Permissive [-] *)")
    lines.append("")
    lines.append("    (* ========================================================================= *)")
    lines.append("    (* 2oo3 REDUNDANT CHANNEL 3: MAGNETO-ELASTIC FLATNESS ROLL PARABOLIC [I-unit]*)")
    lines.append("    (* ========================================================================= *)")
    lines.append("    rFlatness_Sym_ChA_Iunit             : REAL;   (* Contactless Transverse Shape Symmetrical Parabolic Ch A [I-units] *)")
    lines.append("    rFlatness_Sym_ChB_Iunit             : REAL;   (* Contactless Transverse Shape Symmetrical Parabolic Ch B [I-units] *)")
    lines.append("    rFlatness_Sym_ChC_Iunit             : REAL;   (* Contactless Transverse Shape Symmetrical Parabolic Ch C [I-units] *)")
    lines.append("    bFlatness_Sym_ChA_Valid             : BOOL;   (* Flatness Deflector Roll Transducer Ch A Permissive [-] *)")
    lines.append("    bFlatness_Sym_ChB_Valid             : BOOL;   (* Flatness Deflector Roll Transducer Ch B Permissive [-] *)")
    lines.append("    bFlatness_Sym_ChC_Valid             : BOOL;   (* Flatness Deflector Roll Transducer Ch C Permissive [-] *)")
    lines.append("")
    lines.append("    (* ========================================================================= *)")
    lines.append("    (* 2oo3 REDUNDANT CHANNEL 4: STRIP SURFACE SPEED & EXIT SPECIFIC TENSION     *)")
    lines.append("    (* ========================================================================= *)")
    lines.append("    rStripSpeed_ChA_mpm                 : REAL;   (* Non-Contact Laser Doppler Velocimeter Speed Channel A [m/min] *)")
    lines.append("    rStripSpeed_ChB_mpm                 : REAL;   (* Non-Contact Spatial Filter Optical Velocimeter Speed Ch B [m/min] *)")
    lines.append("    rStripSpeed_ChC_mpm                 : REAL;   (* Deflector Tensiometer Roll Sine/Cosine High-Res Encoder Ch C [m/min] *)")
    lines.append("    bStripSpeed_ChA_Valid               : BOOL;   (* Laser Speed Sensor Channel A Signal Valid [-] *)")
    lines.append("    bStripSpeed_ChB_Valid               : BOOL;   (* Optical Speed Sensor Channel B Signal Valid [-] *)")
    lines.append("    bStripSpeed_ChC_Valid               : BOOL;   (* Encoder Speed Sensor Channel C Signal Valid [-] *)")
    lines.append("    rExitTension_ChA_MPa                : REAL;   (* Exit Deflector Tensiometer Load Cell Strain Ch A Specific [MPa] *)")
    lines.append("    rExitTension_ChB_MPa                : REAL;   (* Exit Deflector Tensiometer Load Cell Strain Ch B Specific [MPa] *)")
    lines.append("    rExitTension_ChC_MPa                : REAL;   (* Exit Deflector Tensiometer Load Cell Strain Ch C Specific [MPa] *)")
    lines.append("    bExitTension_ChA_Valid              : BOOL;   (* Exit Tensiometer Channel A Diagnostic Health Permissive [-] *)")
    lines.append("    bExitTension_ChB_Valid              : BOOL;   (* Exit Tensiometer Channel B Diagnostic Health Permissive [-] *)")
    lines.append("    bExitTension_ChC_Valid              : BOOL;   (* Exit Tensiometer Channel C Diagnostic Health Permissive [-] *)")
    lines.append("")
    lines.append("    (* ========================================================================= *)")
    lines.append("    (* ENTRY & INTERMEDIATE MECHANICAL SENSORS & HYDRAULIC POSITIONS             *)")
    lines.append("    (* ========================================================================= *)")
    lines.append("    rEntryThickness_mm                  : REAL;   (* Entry Stand Laser Thickness Gauge Strip Measurement [mm] *)")
    lines.append("    rEntryTension_MPa                   : REAL;   (* Entry Deflector Tensiometer Roll Strip Specific Tension [MPa] *)")
    lines.append("    rRollGap_DS_Pos_um                  : REAL;   (* Drive Side Hydraulic AGC Screwdown Cylinder LVDT Position [um] *)")
    lines.append("    rRollGap_OS_Pos_um                  : REAL;   (* Operator Side Hydraulic AGC Screwdown Cylinder LVDT Position [um] *)")
    lines.append("    rWRB_Force_Actual_kN                : REAL;   (* Work Roll Bending Cylinder Differential Strain Total Force [kN] *)")
    lines.append("    rIRB_Force_Actual_kN                : REAL;   (* Intermediate Roll Bending Hydraulic Cylinder Total Force [kN] *)")
    lines.append("    rIRS_Pos_Top_Actual_mm              : REAL;   (* Top Intermediate Roll Axial Shifting LVDT Cylinder Position [mm] *)")
    lines.append("    rIRS_Pos_Bot_Actual_mm              : REAL;   (* Bottom Intermediate Roll Axial Shifting LVDT Cylinder Position [mm] *)")
    lines.append("    rFlatness_Asym_Iunit                : REAL;   (* Real-Time Strip Linear Tilt Asymmetrical Flatness Component [I-units] *)")
    lines.append("    rFlatness_4th_Iunit                 : REAL;   (* Real-Time Strip 4th-Order Quarter-Buckle Wave Component [I-units] *)")
    lines.append("")
    lines.append("    (* ========================================================================= *)")
    lines.append("    (* FLUID POWER, THERMAL SENSING & STRIP TRACKING                             *)")
    lines.append("    (* ========================================================================= *)")
    lines.append("    rCoolantHeaderPressure_bar          : REAL;   (* 40-Zone Segmented Coolant Spray Main Header Emulsion Pressure [bar] *)")
    lines.append("    rCoolantEmulsionTemp_degC           : REAL;   (* Coolant Recirculation Emulsion Supply Header Temperature [deg C] *)")
    lines.append("    rRollTemp_DS_degC                   : REAL;   (* Work Roll Surface Infrared Pyrometer Drive Side Choke [deg C] *)")
    lines.append("    rRollTemp_OS_degC                   : REAL;   (* Work Roll Surface Infrared Pyrometer Operator Side Choke [deg C] *)")
    lines.append("    rHPU_SupplyPressure_bar             : REAL;   (* High-Pressure Hydraulic Power Unit Main AGC Supply Rail [bar] *)")
    lines.append("    rStripCenterlineOffset_mm           : REAL;   (* Optical Centerline Strip Tracking Sensor Lateral Deviation [mm] *)")
    lines.append("")
    lines.append("    (* ========================================================================= *)")
    lines.append("    (* METALLURGICAL PASS SCHEDULE & MILL OPERATIONAL SETPOINTS                  *)")
    lines.append("    (* ========================================================================= *)")
    lines.append("    rTargetThickness_mm                 : REAL;   (* Current Rolling Pass Nominal Exit Thickness Target Setpoint [mm] *)")
    lines.append("    rTargetSpeed_mpm                    : REAL;   (* Synchronized Mill Master Line Speed Target Setpoint [m/min] *)")
    lines.append("    rTargetEntryTension_MPa             : REAL;   (* Controlled Entry Specific Strip Tension Target Setpoint [MPa] *)")
    lines.append("    rTargetExitTension_MPa              : REAL;   (* Controlled Exit Specific Strip Tension Target Setpoint [MPa] *)")
    lines.append("    rStripWidth_mm                      : REAL;   (* Strip Nominal Width Across Roll Barrel Face [mm] *)")
    lines.append("    rStripYieldStrength_MPa             : REAL;   (* Strip Material Plastic Flow Stress Yield Strength [MPa] *)")
    lines.append("    rStripElasticModulus_GPa            : REAL;   (* Strip Material Youngs Elastic Modulus of Elasticity [GPa] *)")
    lines.append("    rMillHousingModulus_kNmm            : REAL;   (* Stand Housing Frame Elastic Structural Modulus Calibration [kN/mm] *)")
    lines.append("    rWR_Diameter_mm                     : REAL;   (* Calibrated Initial Work Roll Body Diameter [mm] *)")
    lines.append("    rIR_ShiftTarget_mm                  : REAL;   (* Pass Schedule Intermediate Roll Crown Compensation Shift [mm] *)")
    lines.append("    nPassNumber                         : INT;    (* Active Rolling Pass Index In Schedule Sequence [1..7] [-] *)")
    lines.append("    bReverseDirection                   : BOOL;   (* Mill Rolling Pass Direction: FALSE = L-to-R, TRUE = R-to-L [-] *)")
    lines.append("")
    lines.append("    (* ========================================================================= *)")
    lines.append("    (* SUPERVISORY DIGITAL COMMANDS & REAL-TIME SCHEDULING                       *)")
    lines.append("    (* ========================================================================= *)")
    lines.append("    bEnableMillRun                      : BOOL;   (* Master Supervisory Rolling Automation Sequence Run Permissive [-] *)")
    lines.append("    bAutoAGC_Enable                     : BOOL;   (* High-Frequency Closed-Loop Hydraulic AGC Mode Enable Command [-] *)")
    lines.append("    bAutoAFC_Enable                     : BOOL;   (* 40-Zone Segmented Coolant Closed-Loop AFC Mode Enable Command [-] *)")
    lines.append("    bEmergencyQuickOpenCmd              : BOOL;   (* Operator / Safety System Fast Hydraulic Gap Separation Command [-] *)")
    lines.append("    bRollChangeRequest                  : BOOL;   (* Supervisory Roll Change Carousel Sequence Request Flag [-] *)")
    lines.append("    bCalibZeroRequest                   : BOOL;   (* Roll Stack Kiss-Pass Zero Gap Mechanical Calibration Request [-] *)")
    lines.append("    bTareLoadCellsRequest               : BOOL;   (* Mill Load Cell Electronic Tare Zero Balance Request Flag [-] *)")
    lines.append("    bResetFaults                        : BOOL;   (* Master System Latched Alarm & Fault Reset Command [-] *)")
    lines.append("    rScanCycleTime_s                    : REAL;   (* Real-Time Deterministic Cyclic Scan Interval Execution Period [s] *)")
    lines.append("    rZone_Flatness_Meas_Iunit           : ARRAY[1..40] OF REAL; (* Transverse 40-Zone Flatness Stress Profile [I-units] *)")
    lines.append("END_VAR")
    lines.append("")
    
    # VAR_OUTPUT
    lines.append("VAR_OUTPUT")
    lines.append("    (* ========================================================================= *)")
    lines.append("    (* HYDRAULIC AGC SCREWDOWN CYLINDER SERVO ACTUATOR COMMANDS                  *)")
    lines.append("    (* ========================================================================= *)")
    lines.append("    rGapCmd_DS_um                       : REAL;   (* Drive Side Hydraulic AGC Cylinder Target Position Setpoint [um] *)")
    lines.append("    rGapCmd_OS_um                       : REAL;   (* Operator Side Hydraulic AGC Cylinder Target Position Setpoint [um] *)")
    lines.append("    rServoCurrent_DS_mA                 : REAL;   (* Drive Side Moog D664 Dual Flapper High-Frequency Solenoid Current [mA] *)")
    lines.append("    rServoCurrent_OS_mA                 : REAL;   (* Operator Side Moog D664 Dual Flapper High-Frequency Solenoid Current [mA] *)")
    lines.append("    rGapDifferential_um                 : REAL;   (* Dynamic Roll Gap Differential Leveling Tilt Trim [um] *)")
    lines.append("")
    lines.append("    (* ========================================================================= *)")
    lines.append("    (* ROLL BENDING & AXIAL SHIFTING ACTUATOR COMMANDS                           *)")
    lines.append("    (* ========================================================================= *)")
    lines.append("    rWRB_ForceCmd_kN                    : REAL;   (* Work Roll Hydraulic Bending Closed-Loop Force Demand [kN] *)")
    lines.append("    rWRB_PressureCmd_bar                : REAL;   (* Work Roll Hydraulic Bending Cylinder Proportional Pressure [bar] *)")
    lines.append("    rIRB_ForceCmd_kN                    : REAL;   (* Intermediate Roll Hydraulic Bending Closed-Loop Force Demand [kN] *)")
    lines.append("    rIRS_VelocityCmd_mms                : REAL;   (* Intermediate Roll Axial Shifting Directional Valve Velocity [mm/s] *)")
    lines.append("    rIRS_TargetPos_mm                   : REAL;   (* Intermediate Roll Axial Shifting Final Target Setpoint [mm] *)")
    lines.append("")
    lines.append("    (* ========================================================================= *)")
    lines.append("    (* 40-ZONE SEGMENTED COOLANT SPRAY BAR AUTOMATIC FLATNESS CONTROL OUTPUTS    *)")
    lines.append("    (* ========================================================================= *)")
    lines.append("    rCoolant_Zone_Flow_Pct              : ARRAY[1..40] OF REAL; (* Transverse 40-Zone Coolant Spray PWM Duty Cycle [%] *)")
    lines.append("")
    lines.append("    (* ========================================================================= *)")
    lines.append("    (* COILER DRIVE DYNAMIC AGC TRIM & COORDINATED SPEED REFERENCES              *)")
    lines.append("    (* ========================================================================= *)")
    lines.append("    rEntryReelTorqueTrim_Nm             : REAL;   (* Entry Tension Reel Variable Frequency Drive AGC Torque Trim [Nm] *)")
    lines.append("    rExitReelTorqueTrim_Nm              : REAL;   (* Exit Tension Reel Variable Frequency Drive AGC Torque Trim [Nm] *)")
    lines.append("    rLineSpeedRef_mpm                   : REAL;   (* Coordinated Mill Main Stand Master Line Speed Reference [m/min] *)")
    lines.append("")
    lines.append("    (* ========================================================================= *)")
    lines.append("    (* ANSI/ISA-18.2 BIT-PACKED ALARM REGISTERS & SYSTEM DIAGNOSTICS             *)")
    lines.append("    (* ========================================================================= *)")
    lines.append("    dwStatus_MillFSM                    : DWORD;  (* 32-Bit Bit-Packed Mill Finite State Machine Execution Status [-] *)")
    lines.append("    dwAlarms_EmergencyTrip_HH           : DWORD;  (* 32-Bit Bit-Packed Critical Safety High-High Trip Alarm Word [-] *)")
    lines.append("    dwAlarms_ProcessWarning_H           : DWORD;  (* 32-Bit Bit-Packed Operational Process High Warning Alarm Word [-] *)")
    lines.append("    dwAlarms_LowWarning_L               : DWORD;  (* 32-Bit Bit-Packed Operational Process Low Warning Alarm Word [-] *)")
    lines.append("    dwAlarms_LowTrip_LL                 : DWORD;  (* 32-Bit Bit-Packed Critical Safety Low-Low Trip Alarm Word [-] *)")
    lines.append("    dwTMR_Diagnostic_Word               : DWORD;  (* 32-Bit Bit-Packed TMR 2oo3 Sensor Redundancy Health Bitfield [-] *)")
    lines.append("")
    lines.append("    (* ========================================================================= *)")
    lines.append("    (* OBSERVED CYBER-PHYSICAL SYSTEM STATES & REAL-TIME PERFORMANCE METRICS     *)")
    lines.append("    (* ========================================================================= *)")
    lines.append("    rVoted_RollForce_Total_kN           : REAL;   (* TMR 2oo3 Synthesized Redundant Total Mill Rolling Force [kN] *)")
    lines.append("    rVoted_ExitThickness_mm             : REAL;   (* TMR 2oo3 Synthesized Redundant Exit Strip Finished Thickness [mm] *)")
    lines.append("    rThicknessDeviation_um              : REAL;   (* Exit Strip Thickness Error Relative to Target Setpoint [um] *)")
    lines.append("    rVoted_StripSpeed_mpm               : REAL;   (* TMR 2oo3 Synthesized Strip Surface Rolling Velocity [m/min] *)")
    lines.append("    rVoted_ExitTension_MPa              : REAL;   (* TMR 2oo3 Synthesized Exit Specific Strip Tension [MPa] *)")
    lines.append("    rFlatness_Parabolic_Iunit           : REAL;   (* Closed-Loop Estimated 2nd-Order Symmetrical Flatness [I-units] *)")
    lines.append("    rFlatness_LinearTilt_Iunit          : REAL;   (* Closed-Loop Estimated 1st-Order Asymmetrical Tilt Flatness [I-units] *)")
    lines.append("    rFlatness_4thOrder_Iunit            : REAL;   (* Closed-Loop Estimated 4th-Order Buckling Flatness [I-units] *)")
    lines.append("    rStandElasticStretch_um             : REAL;   (* Mill Stand Housing Modulus Dynamic Elastic Stretch [um] *)")
    lines.append("    rRollThermalExpansion_um            : REAL;   (* Work Roll Body Integrated Thermal Crown Thermal Expansion [um] *)")
    lines.append("    rMPC_QuadraticCost                  : REAL;   (* Receding-Horizon MPC Instantaneous Objective Tracking Cost [-] *)")
    lines.append("    nActiveFSM_StateID                  : INT;    (* Current Mill Automation Finite State Machine State Index [0..13] [-] *)")
    lines.append("    bMillReadyForPass                   : BOOL;   (* Master Interlock Permissive: Stand Synchronized For Strip Entry [-] *)")
    lines.append("    bPassCompletedFlag                  : BOOL;   (* Cold Rolling Reduction Pass Finished Pulse Flag [-] *)")
    lines.append("    bQuickOpenActive                    : BOOL;   (* Hydraulic Gap Separation Quick Opening Active Safety Status [-] *)")
    lines.append("END_VAR")
    lines.append("")
    
    # VAR (Internal variables)
    lines.append("VAR")
    lines.append("    (* Real-Time Execution Clamping & Initialization *)")
    lines.append("    fScanTimeClamped_s                  : REAL;")
    lines.append("    bSystemInitialized                  : BOOL;")
    lines.append("")
    lines.append("    (* 12x12 Discrete State-Space Matrices *)")
    lines.append("    A_Matrix                            : ARRAY[1..12, 1..12] OF REAL;")
    lines.append("    B_Matrix                            : ARRAY[1..12, 1..4] OF REAL;")
    lines.append("    C_Matrix                            : ARRAY[1..6, 1..12] OF REAL;")
    lines.append("    D_Matrix                            : ARRAY[1..6, 1..4] OF REAL;")
    lines.append("    L_Matrix                            : ARRAY[1..12, 1..6] OF REAL;")
    lines.append("")
    lines.append("    (* MPC Penalty & Terminal Matrices *)")
    lines.append("    Q_Matrix                            : ARRAY[1..12, 1..12] OF REAL;")
    lines.append("    R_Matrix                            : ARRAY[1..4, 1..4] OF REAL;")
    lines.append("    P_Matrix                            : ARRAY[1..12, 1..12] OF REAL;")
    lines.append("")
    lines.append("    (* Cyber-Physical State & Observer Vectors *)")
    lines.append("    x_StateEst                          : ARRAY[1..12] OF REAL;")
    lines.append("    x_StatePred                         : ARRAY[1..12] OF REAL;")
    lines.append("    x_StateRef                          : ARRAY[1..12] OF REAL;")
    lines.append("    y_Pred                              : ARRAY[1..6] OF REAL;")
    lines.append("    y_Meas                              : ARRAY[1..6] OF REAL;")
    lines.append("    y_Innov                             : ARRAY[1..6] OF REAL;")
    lines.append("    u_Input                             : ARRAY[1..4] OF REAL;")
    lines.append("    u_InputPrev                         : ARRAY[1..4] OF REAL;")
    lines.append("    u_Optimal                           : ARRAY[1..4] OF REAL;")
    lines.append("")
    lines.append("    (* Actuator & Physical Bounds *)")
    lines.append("    rRollForce_Min_kN                   : REAL;")
    lines.append("    rRollForce_Max_kN                   : REAL;")
    lines.append("    rGap_Min_um                         : REAL;")
    lines.append("    rGap_Max_um                         : REAL;")
    lines.append("    rWRB_Min_kN                         : REAL;")
    lines.append("    rWRB_Max_kN                         : REAL;")
    lines.append("    rIRS_Min_mm                         : REAL;")
    lines.append("    rIRS_Max_mm                         : REAL;")
    lines.append("    rMaxSlew_Gap_um                     : REAL;")
    lines.append("    rMaxSlew_WRB_kN                     : REAL;")
    lines.append("    rMaxSlew_IRS_mms                    : REAL;")
    lines.append("    rMaxSlew_Cool_Lmin                  : REAL;")
    lines.append("")
    lines.append("    (* TMR Channel 1: Total Roll Force Load Cells *)")
    lines.append("    rForce_ValA_kN                      : REAL;")
    lines.append("    rForce_ValB_kN                      : REAL;")
    lines.append("    rForce_ValC_kN                      : REAL;")
    lines.append("    bForce_HealthyA                     : BOOL;")
    lines.append("    bForce_HealthyB                     : BOOL;")
    lines.append("    bForce_HealthyC                     : BOOL;")
    lines.append("    bForce_DiscrepancyAB                : BOOL;")
    lines.append("    bForce_DiscrepancyBC                : BOOL;")
    lines.append("    bForce_DiscrepancyCA                : BOOL;")
    lines.append("    tForce_DebounceAB_s                 : REAL;")
    lines.append("    tForce_DebounceBC_s                 : REAL;")
    lines.append("    tForce_DebounceCA_s                 : REAL;")
    lines.append("    nForce_DegradationMode              : INT;")
    lines.append("    rForce_Voted_kN                     : REAL;")
    lines.append("")
    lines.append("    (* TMR Channel 2: Exit Strip Thickness *)")
    lines.append("    rThick_ValA_mm                      : REAL;")
    lines.append("    rThick_ValB_mm                      : REAL;")
    lines.append("    rThick_ValC_mm                      : REAL;")
    lines.append("    bThick_HealthyA                     : BOOL;")
    lines.append("    bThick_HealthyB                     : BOOL;")
    lines.append("    bThick_HealthyC                     : BOOL;")
    lines.append("    bThick_DiscrepancyAB                : BOOL;")
    lines.append("    bThick_DiscrepancyBC                : BOOL;")
    lines.append("    bThick_DiscrepancyCA                : BOOL;")
    lines.append("    tThick_DebounceAB_s                 : REAL;")
    lines.append("    tThick_DebounceBC_s                 : REAL;")
    lines.append("    tThick_DebounceCA_s                 : REAL;")
    lines.append("    nThick_DegradationMode              : INT;")
    lines.append("    rThick_Voted_mm                     : REAL;")
    lines.append("")
    lines.append("    (* TMR Channel 3: Symmetrical Flatness *)")
    lines.append("    rFlat_ValA_Iunit                    : REAL;")
    lines.append("    rFlat_ValB_Iunit                    : REAL;")
    lines.append("    rFlat_ValC_Iunit                    : REAL;")
    lines.append("    bFlat_HealthyA                      : BOOL;")
    lines.append("    bFlat_HealthyB                      : BOOL;")
    lines.append("    bFlat_HealthyC                      : BOOL;")
    lines.append("    bFlat_DiscrepancyAB                 : BOOL;")
    lines.append("    bFlat_DiscrepancyBC                 : BOOL;")
    lines.append("    bFlat_DiscrepancyCA                 : BOOL;")
    lines.append("    tFlat_DebounceAB_s                  : REAL;")
    lines.append("    tFlat_DebounceBC_s                  : REAL;")
    lines.append("    tFlat_DebounceCA_s                  : REAL;")
    lines.append("    nFlat_DegradationMode               : INT;")
    lines.append("    rFlat_Voted_Iunit                   : REAL;")
    lines.append("")
    lines.append("    (* TMR Channel 4: Strip Speed & Exit Specific Tension *)")
    lines.append("    rSpeed_ValA_mpm                     : REAL;")
    lines.append("    rSpeed_ValB_mpm                     : REAL;")
    lines.append("    rSpeed_ValC_mpm                     : REAL;")
    lines.append("    bSpeed_HealthyA                     : BOOL;")
    lines.append("    bSpeed_HealthyB                     : BOOL;")
    lines.append("    bSpeed_HealthyC                     : BOOL;")
    lines.append("    bSpeed_DiscrepancyAB                : BOOL;")
    lines.append("    bSpeed_DiscrepancyBC                : BOOL;")
    lines.append("    bSpeed_DiscrepancyCA                : BOOL;")
    lines.append("    tSpeed_DebounceAB_s                 : REAL;")
    lines.append("    tSpeed_DebounceBC_s                 : REAL;")
    lines.append("    tSpeed_DebounceCA_s                 : REAL;")
    lines.append("    nSpeed_DegradationMode              : INT;")
    lines.append("    rSpeed_Voted_mpm                    : REAL;")
    lines.append("")
    lines.append("    rTens_ValA_MPa                      : REAL;")
    lines.append("    rTens_ValB_MPa                      : REAL;")
    lines.append("    rTens_ValC_MPa                      : REAL;")
    lines.append("    bTens_HealthyA                      : BOOL;")
    lines.append("    bTens_HealthyB                      : BOOL;")
    lines.append("    bTens_HealthyC                      : BOOL;")
    lines.append("    bTens_DiscrepancyAB                 : BOOL;")
    lines.append("    bTens_DiscrepancyBC                 : BOOL;")
    lines.append("    bTens_DiscrepancyCA                 : BOOL;")
    lines.append("    tTens_DebounceAB_s                  : REAL;")
    lines.append("    tTens_DebounceBC_s                  : REAL;")
    lines.append("    tTens_DebounceCA_s                  : REAL;")
    lines.append("    nTens_DegradationMode               : INT;")
    lines.append("    rTens_Voted_MPa                     : REAL;")
    lines.append("")
    lines.append("    (* TMR Persistence Thresholds *)")
    lines.append("    fTMR_DiscrepancyPersistence_s       : REAL;")
    lines.append("    fTol_Force_kN                       : REAL;")
    lines.append("    fTol_Thick_mm                       : REAL;")
    lines.append("    fTol_Flat_Iunit                     : REAL;")
    lines.append("    fTol_Speed_mpm                      : REAL;")
    lines.append("    fTol_Tens_MPa                       : REAL;")
    lines.append("")
    lines.append("    (* MPC Unrolled PGD Working Variables *)")
    lines.append("    fPGD_StepSize                       : REAL;")
    lines.append("    fCost_Best                          : REAL;")
    lines.append("    fCost_Iter                          : REAL;")
    lines.append("    fStateTrackingCost                  : REAL;")
    lines.append("    fActuatorRateCost                   : REAL;")
    lines.append("    u_Cand1                             : REAL;")
    lines.append("    u_Cand2                             : REAL;")
    lines.append("    u_Cand3                             : REAL;")
    lines.append("    u_Cand4                             : REAL;")
    lines.append("    u_Iter1                             : REAL;")
    lines.append("    u_Iter2                             : REAL;")
    lines.append("    u_Iter3                             : REAL;")
    lines.append("    u_Iter4                             : REAL;")
    lines.append("    grad_u1                             : REAL;")
    lines.append("    grad_u2                             : REAL;")
    lines.append("    grad_u3                             : REAL;")
    lines.append("    grad_u4                             : REAL;")
    for i in range(1, 13):
        lines.append(f"    e_State_{i:<27} : REAL;")
    for i in range(1, 13):
        lines.append(f"    x_PredIter_{i:<24} : REAL;")
    lines.append("")
    lines.append("    (* 14-Stage FSM Variables *)")
    lines.append("    nMill_FSM_State                     : INT;")
    lines.append("    nMill_FSM_PrevState                 : INT;")
    lines.append("    tStateDwellTimer_s                  : REAL;")
    lines.append("    tCoilAlignTimer_s                   : REAL;")
    lines.append("    tZeroCalibTimer_s                   : REAL;")
    lines.append("    tThreadingTimer_s                   : REAL;")
    lines.append("    tReelGripTimer_s                    : REAL;")
    lines.append("    tDecelTrackTimer_s                  : REAL;")
    lines.append("    tTailOutTimer_s                     : REAL;")
    lines.append("    tReversalTimer_s                    : REAL;")
    lines.append("    rRolledStripLength_m                : REAL;")
    lines.append("    rTotalPassLength_m                  : REAL;")
    lines.append("    bStripHeadDetected                  : BOOL;")
    lines.append("    bStripTailDetected                  : BOOL;")
    lines.append("    bStripBreakDetected                 : BOOL;")
    lines.append("    bKissCalibComplete                  : BOOL;")
    lines.append("")
    lines.append("    (* 40-Zone Segmented Coolant Spray AFC Internal Variables *)")
    lines.append("    rZone_Coord_Z_mm                    : ARRAY[1..40] OF REAL;")
    lines.append("    rZone_Normalized_Z                  : ARRAY[1..40] OF REAL;")
    lines.append("    rZone_Poly_P1                       : ARRAY[1..40] OF REAL;")
    lines.append("    rZone_Poly_P2                       : ARRAY[1..40] OF REAL;")
    lines.append("    rZone_Poly_P4                       : ARRAY[1..40] OF REAL;")
    lines.append("    rZone_ThermalState_degC             : ARRAY[1..40] OF REAL;")
    lines.append("    rZone_ThermalExpansion_um           : ARRAY[1..40] OF REAL;")
    lines.append("    rZone_FlowSetpoint_Pct              : ARRAY[1..40] OF REAL;")
    lines.append("    rZone_FlowPrev_Pct                  : ARRAY[1..40] OF REAL;")
    lines.append("    fMaxZoneFlowSlew_PctScan            : REAL;")
    lines.append("")
    
    # Alarm variables for 12 channels
    alarm_vars = [
        "Force", "Thick", "WRB", "IRS", "EntryTens", "ExitTens",
        "FlatSym", "Flat4th", "CoolPres", "RollTemp", "HPU", "Center"
    ]
    for ch in alarm_vars:
        for t in ["HH", "H", "L", "LL"]:
            lines.append(f"    tAlarmTimer_{ch}_{t:<15} : REAL;")
    for ch in alarm_vars:
        for t in ["HH", "H", "L", "LL"]:
            lines.append(f"    bAlarmLatch_{ch}_{t:<15} : BOOL;")
    lines.append("    fPersistence_Trip_s                 : REAL;")
    lines.append("    fPersistence_Warn_s                 : REAL;")
    lines.append("    fAlarmSuppressionActive             : BOOL;")
    
    # Alarm limits
    limits = [
        ("Force_kN", "Force"), ("ThickDev_um", "Thickness Deviation"), ("WRB_bar", "WR Bending"),
        ("IRS_mm", "IR Shifting"), ("EntryTens_MPa", "Entry Tension"), ("ExitTens_MPa", "Exit Tension"),
        ("FlatSym_Iunit", "Flatness Sym"), ("Flat4th_Iunit", "Flatness 4th"), ("CoolPres_bar", "Coolant Pressure"),
        ("RollTemp_degC", "Roll Temp"), ("HPU_bar", "HPU Pressure"), ("Center_mm", "Centerline Offset")
    ]
    for tag, desc in limits:
        lines.append(f"    fLimit_{tag}_HH : REAL; (* {desc} High-High Trip Limit *)")
        lines.append(f"    fLimit_{tag}_H  : REAL; (* {desc} High Warning Limit *)")
        lines.append(f"    fLimit_{tag}_L  : REAL; (* {desc} Low Warning Limit *)")
        lines.append(f"    fLimit_{tag}_LL : REAL; (* {desc} Low-Low Trip Limit *)")
        lines.append(f"    fHyst_{tag}     : REAL; (* {desc} Recovery Hysteresis Deadband *)")
    
    lines.append("END_VAR")
    lines.append("")
    
    # -------------------------------------------------------------------------
    # PHASE 0: REAL-TIME SCAN TIMING & COLD-BOOT MATRIX INITIALIZATION
    # -------------------------------------------------------------------------
    lines.append("(* === PHASE 0: REAL-TIME SCAN TIMING & COLD-BOOT MATRIX INITIALIZATION === *)")
    lines.append("(* Clamping scan interval between 0.5 ms and 50.0 ms to guarantee numeric stability *)")
    lines.append("IF rScanCycleTime_s < 0.000500 THEN")
    lines.append("    fScanTimeClamped_s := 0.000500;")
    lines.append("ELSIF rScanCycleTime_s > 0.050000 THEN")
    lines.append("    fScanTimeClamped_s := 0.050000;")
    lines.append("ELSE")
    lines.append("    fScanTimeClamped_s := rScanCycleTime_s;")
    lines.append("END_IF;")
    lines.append("")
    
    lines.append("IF NOT bSystemInitialized THEN")
    lines.append("    (* Initialize Actuator Slew Limits and Bounds *)")
    lines.append("    rRollForce_Min_kN     := 5000.000;   (* Minimum rolling load to prevent chattering [kN] *)")
    lines.append("    rRollForce_Max_kN     := 45000.00;   (* Max stand load rating [kN] *)")
    lines.append("    rGap_Min_um           := -500.000;   (* Minimum closed gap [um] *)")
    lines.append("    rGap_Max_um           := 1500.000;   (* Maximum gap separation [um] *)")
    lines.append("    rWRB_Min_kN           := -1500.00;   (* Negative work roll bending [kN] *)")
    lines.append("    rWRB_Max_kN           := 2500.000;   (* Positive work roll bending [kN] *)")
    lines.append("    rIRS_Min_mm           := -350.000;   (* Intermediate roll negative shift stroke [mm] *)")
    lines.append("    rIRS_Max_mm           := 350.0000;   (* Intermediate roll positive shift stroke [mm] *)")
    lines.append("    rMaxSlew_Gap_um       := 15.00000;   (* High-speed Moog AGC dynamic slew limit [um/scan] *)")
    lines.append("    rMaxSlew_WRB_kN       := 25.00000;   (* Hydraulic bending force slew limit [kN/scan] *)")
    lines.append("    rMaxSlew_IRS_mms      := 0.500000;   (* Intermediate roll shifting velocity slew [mm/s/scan] *)")
    lines.append("    rMaxSlew_Cool_Lmin    := 5.000000;   (* Segmented coolant flow slew limit [L/min/scan] *)")
    lines.append("    fMaxZoneFlowSlew_PctScan := 2.50000; (* Anti-thermal shock rate limit [%/scan] *)")
    lines.append("    fPGD_StepSize         := 0.001250;   (* Projected Gradient Descent optimal step size *)")
    lines.append("")
    lines.append("    (* TMR Discrepancy Tolerances and Debounce Timers *)")
    lines.append("    fTMR_DiscrepancyPersistence_s := 0.020000; (* 20 ms Discrepancy Persistence Debounce Window *)")
    lines.append("    fTol_Force_kN         := 250.0000;   (* Force discrepancy threshold [kN] *)")
    lines.append("    fTol_Thick_mm         := 0.005000;   (* Thickness discrepancy threshold [mm] (5 um) *)")
    lines.append("    fTol_Flat_Iunit       := 1.500000;   (* Flatness discrepancy threshold [I-units] *)")
    lines.append("    fTol_Speed_mpm        := 10.00000;   (* Strip speed discrepancy threshold [m/min] *)")
    lines.append("    fTol_Tens_MPa         := 2.000000;   (* Specific tension discrepancy threshold [MPa] *)")
    lines.append("")
    lines.append("    (* ISA-18.2 Alarm Limits and Deadbands *)")
    lines.append("    fPersistence_Trip_s   := 0.040000;   (* 40 ms Trip Debounce Persistence *)")
    lines.append("    fPersistence_Warn_s   := 0.150000;   (* 150 ms Warning Debounce Persistence *)")
    lines.append("")
    lines.append("    fLimit_Force_HH_kN    := 44000.00; fLimit_Force_H_kN   := 40000.00; fLimit_Force_L_kN   := 4000.000; fLimit_Force_LL_kN  := 1500.000; fHyst_Force_kN   := 250.000;")
    lines.append("    fLimit_ThickDev_HH_um := 25.00000; fLimit_ThickDev_H_um:= 12.00000; fLimit_ThickDev_L_um:= -12.0000; fLimit_ThickDev_LL_um:= -25.0000; fHyst_ThickDev_um:= 1.50000;")
    lines.append("    fLimit_WRB_HH_bar     := 295.0000; fLimit_WRB_H_bar    := 275.0000; fLimit_WRB_L_bar    := 30.00000; fLimit_WRB_LL_bar   := 10.00000; fHyst_WRB_bar    := 5.00000;")
    lines.append("    fLimit_IRS_HH_mm      := 345.0000; fLimit_IRS_H_mm     := 330.0000; fLimit_IRS_L_mm     := -330.000; fLimit_IRS_LL_mm    := -345.000; fHyst_IRS_mm     := 2.00000;")
    lines.append("    fLimit_EntryTens_HH_MPa:=160.0000; fLimit_EntryTens_H_MPa:=140.000; fLimit_EntryTens_L_MPa:= 25.00000; fLimit_EntryTens_LL_MPa:= 8.000000; fHyst_EntryTens_MPa:=2.0000;")
    lines.append("    fLimit_ExitTens_HH_MPa :=165.0000; fLimit_ExitTens_H_MPa :=145.000; fLimit_ExitTens_L_MPa := 28.00000; fLimit_ExitTens_LL_MPa := 10.00000; fHyst_ExitTens_MPa :=2.0000;")
    lines.append("    fLimit_FlatSym_HH_Iunit:= 15.0000; fLimit_FlatSym_H_Iunit:= 8.00000; fLimit_FlatSym_L_Iunit:= -8.00000; fLimit_FlatSym_LL_Iunit:= -15.0000; fHyst_FlatSym_Iunit:=0.8000;")
    lines.append("    fLimit_Flat4th_HH_Iunit:= 12.0000; fLimit_Flat4th_H_Iunit:= 6.50000; fLimit_Flat4th_L_Iunit:= -6.50000; fLimit_Flat4th_LL_Iunit:= -12.0000; fHyst_Flat4th_Iunit:=0.6000;")
    lines.append("    fLimit_CoolPres_HH_bar := 18.0000; fLimit_CoolPres_H_bar := 16.5000; fLimit_CoolPres_L_bar := 8.50000; fLimit_CoolPres_LL_bar := 5.000000; fHyst_CoolPres_bar :=0.5000;")
    lines.append("    fLimit_RollTemp_HH_degC:= 115.000; fLimit_RollTemp_H_degC:= 95.0000; fLimit_RollTemp_L_degC:= 35.00000; fLimit_RollTemp_LL_degC:= 20.00000; fHyst_RollTemp_degC:=2.0000;")
    lines.append("    fLimit_HPU_HH_bar      := 330.000; fLimit_HPU_H_bar     := 310.000; fLimit_HPU_L_bar     := 240.0000; fLimit_HPU_LL_bar    := 210.0000; fHyst_HPU_bar     :=5.00000;")
    lines.append("    fLimit_Center_HH_mm    := 20.0000; fLimit_Center_H_mm    := 12.0000; fLimit_Center_L_mm    := -12.0000; fLimit_Center_LL_mm   := -20.0000; fHyst_Center_mm  :=1.00000;")
    lines.append("")
    
    # Fully write out A_Matrix[1..12, 1..12] (144 assignments)
    lines.append("    (* 12x12 Discrete State Transition Dynamics Matrix A_Matrix *)")
    # Physically grounded values for discrete state transitions
    A_vals = [
        # x1: delta_h
        [0.885000, 0.450000, 0.000015, -0.000020, 0.000100, -0.000250, 0.000300, 0.380000, 0.120000, 0.000000, 0.000000, 0.000000],
        # x2: s_gap
        [0.000000, 0.920000, 0.000000,  0.000000, 0.000000,  0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000],
        # x3: F_roll
        [420.0000, -12500.0, 0.895000,  0.150000, -2.50000, -18.5000, 22.00000, 11500.00, 45.00000, 0.000000, 0.000000, 0.000000],
        # x4: F_wrb
        [0.000000, 0.000000, 0.000000,  0.940000, 0.000000,  0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000],
        # x5: delta_s_ir
        [0.000000, 0.000000, 0.000000,  0.000000, 0.985000,  0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000],
        # x6: sigma_entry
        [2.500000, 0.150000, 0.000120,  0.000000, 0.000000,  0.965000, 0.005000, 0.080000, 0.000000, 0.000000, 0.000000, 0.000000],
        # x7: sigma_exit
        [-3.20000, -0.22000, 0.000180,  0.000000, 0.000000,  0.005000, 0.960000, -0.12000, 0.000000, 0.000000, 0.000000, 0.000000],
        # x8: delta_S_stand
        [0.000000, 0.000000, 0.000080,  0.000000, 0.000000,  0.000000, 0.000000, 0.850000, 0.000000, 0.000000, 0.000000, 0.000000],
        # x9: delta_R_therm
        [0.000000, 0.000000, 0.000005,  0.000000, 0.000000,  0.000000, 0.000000, 0.000000, 0.992000, 0.000000, 0.000000, 0.000000],
        # x10: delta_Lambda_sym
        [0.050000, 0.020000, 0.000040, -0.004500, 0.025000, -0.010000, 0.012000, 0.035000, 0.085000, 0.910000, 0.000000, 0.015000],
        # x11: delta_Lambda_asym
        [0.000000, 0.000000, 0.000000,  0.000000, -0.01500, 0.000000,  0.000000, 0.000000, 0.000000, 0.000000, 0.930000, 0.000000],
        # x12: delta_Lambda_4th
        [0.020000, 0.000000, 0.000010,  0.001200, -0.04500, 0.000000,  0.000000, 0.010000, 0.020000, 0.010000, 0.000000, 0.895000],
    ]
    for r in range(1, 13):
        for c in range(1, 13):
            val = A_vals[r-1][c-1]
            lines.append(f"    A_Matrix[{r:2d}, {c:2d}] := {val:12.6f};")
    lines.append("")
    
    # Fully write out B_Matrix[1..12, 1..4] (48 assignments)
    lines.append("    (* 12x4 Input Coupling Dynamics Matrix B_Matrix *)")
    B_vals = [
        # u1: delta_s_gap_cmd, u2: delta_F_bend_cmd, u3: delta_v_shift_cmd, u4: delta_Q_cool_cmd
        [0.550000, -0.000050,  0.000200, -0.000100], # x1: delta_h
        [0.080000,  0.000000,  0.000000,  0.000000], # x2: s_gap
        [-1250.00,  0.250000, -5.000000, -0.500000], # x3: F_roll
        [0.000000,  0.060000,  0.000000,  0.000000], # x4: F_wrb
        [0.000000,  0.000000,  0.015000,  0.000000], # x5: delta_s_ir
        [0.250000,  0.000000,  0.000000,  0.000000], # x6: sigma_entry
        [-0.35000,  0.000000,  0.000000,  0.000000], # x7: sigma_exit
        [-0.01000,  0.000000,  0.000000,  0.000000], # x8: delta_S_stand
        [0.000000,  0.000000,  0.000000, -0.008000], # x9: delta_R_therm
        [0.040000, -0.005500,  0.035000, -0.025000], # x10: delta_Lambda_sym
        [0.000000,  0.000000, -0.020000,  0.000000], # x11: delta_Lambda_asym
        [0.015000,  0.001800, -0.055000, -0.018000], # x12: delta_Lambda_4th
    ]
    for r in range(1, 13):
        for c in range(1, 5):
            val = B_vals[r-1][c-1]
            lines.append(f"    B_Matrix[{r:2d}, {c:2d}] := {val:12.6f};")
    lines.append("")
    
    # Fully write out C_Matrix[6, 12] (72 assignments)
    lines.append("    (* 6x12 Measurement Output Matrix C_Matrix *)")
    C_vals = [
        # y1: delta_h_meas
        [1.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000],
        # y2: F_roll_meas
        [0.000000, 0.000000, 1.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000],
        # y3: Lambda_sym_meas
        [0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 1.000000, 0.000000, 0.000000],
        # y4: Lambda_asym_meas
        [0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 1.000000, 0.000000],
        # y5: Lambda_4th_meas
        [0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 1.000000],
        # y6: delta_sigma_exit_meas
        [0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 1.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000],
    ]
    for r in range(1, 7):
        for c in range(1, 13):
            val = C_vals[r-1][c-1]
            lines.append(f"    C_Matrix[{r:2d}, {c:2d}] := {val:12.6f};")
    lines.append("")
    
    # Fully write out D_Matrix[6, 4] (24 assignments)
    lines.append("    (* 6x4 Direct Feedthrough Coupling Matrix D_Matrix *)")
    for r in range(1, 7):
        for c in range(1, 5):
            lines.append(f"    D_Matrix[{r:2d}, {c:2d}] := 0.000000;")
    lines.append("")
    
    # Fully write out L_Matrix[12, 6] (72 assignments) Kalman Gains
    lines.append("    (* 12x6 Steady-State Kalman Filter Observer Gain Matrix L_Matrix *)")
    L_vals = [
        # e1: delta_h, e2: F_roll, e3: L_sym, e4: L_asym, e5: L_4th, e6: delta_sigma
        [0.450000,  0.000025,  0.000000,  0.000000,  0.000000, -0.000150], # x1
        [0.120000, -0.000010,  0.000000,  0.000000,  0.000000,  0.000000], # x2
        [15.50000,  0.550000,  0.000000,  0.000000,  0.000000,  0.120000], # x3
        [0.000000,  0.000000, -0.002500,  0.000000,  0.000500,  0.000000], # x4
        [0.000000, -0.000005,  0.001500, -0.005000, -0.008500,  0.000000], # x5
        [0.050000,  0.000015,  0.000000,  0.000000,  0.000000,  0.025000], # x6
        [-0.08000,  0.000020,  0.000000,  0.000000,  0.000000,  0.420000], # x7
        [0.000000,  0.000065,  0.000000,  0.000000,  0.000000,  0.000000], # x8
        [0.000000,  0.000002,  0.005500,  0.000000,  0.001200,  0.000000], # x9
        [0.015000,  0.000010,  0.520000,  0.000000,  0.015000,  0.002000], # x10
        [0.000000,  0.000000,  0.000000,  0.580000,  0.000000,  0.000000], # x11
        [0.008000,  0.000005,  0.020000,  0.000000,  0.480000,  0.000000], # x12
    ]
    for r in range(1, 13):
        for c in range(1, 7):
            val = L_vals[r-1][c-1]
            lines.append(f"    L_Matrix[{r:2d}, {c:2d}] := {val:12.6f};")
    lines.append("")
    
    # Fully write out Q_Matrix[12, 12] (144 assignments)
    lines.append("    (* 12x12 MPC State Tracking Cost Quadratic Weight Matrix Q_Matrix *)")
    Q_diag = [100.0, 5.0, 0.001, 0.02, 0.5, 0.8, 1.2, 0.05, 0.2, 45.0, 35.0, 25.0]
    for r in range(1, 13):
        for c in range(1, 13):
            val = Q_diag[r-1] if r == c else 0.0
            lines.append(f"    Q_Matrix[{r:2d}, {c:2d}] := {val:12.6f};")
    lines.append("")
    
    # Fully write out R_Matrix[4, 4] (16 assignments)
    lines.append("    (* 4x4 MPC Actuator Rate Cost Matrix R_Matrix *)")
    R_diag = [2.5, 0.8, 5.0, 1.5]
    for r in range(1, 5):
        for c in range(1, 5):
            val = R_diag[r-1] if r == c else 0.0
            lines.append(f"    R_Matrix[{r:2d}, {c:2d}] := {val:12.6f};")
    lines.append("")
    
    # Fully write out P_Matrix[12, 12] (144 assignments) Terminal cost
    lines.append("    (* 12x12 MPC Terminal State Cost Penalty Matrix P_Matrix *)")
    P_diag = [250.0, 12.0, 0.002, 0.05, 1.2, 2.0, 3.0, 0.1, 0.5, 120.0, 85.0, 65.0]
    for r in range(1, 13):
        for c in range(1, 13):
            val = P_diag[r-1] if r == c else 0.0
            lines.append(f"    P_Matrix[{r:2d}, {c:2d}] := {val:12.6f};")
    lines.append("")
    
    # Fully write out 40 zones transverse coordinates and Legendre polynomials (40 * 5 = 200 lines)
    lines.append("    (* 40-Zone Transverse Geometry & Legendre Orthogonal Polynomial Initialization *)")
    strip_w = 2500.0
    zone_pitch = strip_w / 40.0 # 62.5 mm
    for i in range(1, 41):
        z_coord = - (strip_w / 2.0) + (i - 0.5) * zone_pitch # -1218.75 to +1218.75
        z_norm = z_coord / (strip_w / 2.0) # -0.975 to +0.975 (dimensionless -1..1)
        # Legendre polynomials:
        # P1(z) = z_norm (linear tilt)
        # P2(z) = 0.5 * (3*z_norm^2 - 1) (parabolic crown)
        # P4(z) = 0.125 * (35*z_norm^4 - 30*z_norm^2 + 3) (4th order quarter-buckle)
        p1 = z_norm
        p2 = 0.5 * (3.0 * (z_norm**2) - 1.0)
        p4 = 0.125 * (35.0 * (z_norm**4) - 30.0 * (z_norm**2) + 3.0)
        lines.append(f"    rZone_Coord_Z_mm[{i:2d}]      := {z_coord:12.4f};")
        lines.append(f"    rZone_Normalized_Z[{i:2d}]    := {z_norm:12.6f};")
        lines.append(f"    rZone_Poly_P1[{i:2d}]         := {p1:12.6f};")
        lines.append(f"    rZone_Poly_P2[{i:2d}]         := {p2:12.6f};")
        lines.append(f"    rZone_Poly_P4[{i:2d}]         := {p4:12.6f};")
        lines.append(f"    rZone_ThermalState_degC[{i:2d}]:= 45.000000; (* Calibrated baseline thermal state [deg C] *)")
    lines.append("")
    lines.append("    bSystemInitialized := TRUE;")
    lines.append("END_IF;")
    lines.append("")
    
    return lines

print("Phase 0 builder ready...")
