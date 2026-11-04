# build_full_code.py
"""
Build and validate the complete IEC 61131-3 Function Block
FB_Tobacco_CigaretteMaker_HighSpeed_WeightWeight
"""

import sys
import os
import json
import uuid
import re

from generate_full_dataset import (
    get_header_code,
    get_var_input_code,
    get_var_output_code,
    get_var_internal_code
)

def get_phase0_code():
    code = []
    code.append('''
(* === PHASE 0: ONE-TIME DISCRETE STATE-SPACE & MPC MATRICES INITIALIZATION === *)
IF NOT bInit_Done THEN
    (* ------------------------------------------------------------------------- *)
    (* Discrete State Transition Matrix A (8x8)                                  *)
    (* States: 1:Mass_err, 2:Trimmer_Pos, 3:v_rod_err, 4:eps_r_drift,           *)
    (*         5:Moisture_err, 6:Cut_Phase_err, 7:Vent_err, 8:Drum_Vac_err       *)
    (* ------------------------------------------------------------------------- *)
    A_Matrix[1, 1] := 0.9450; A_Matrix[1, 2] := -42.5000; A_Matrix[1, 3] := 2.1500; A_Matrix[1, 4] := 18.2000; A_Matrix[1, 5] := 0.3500; A_Matrix[1, 6] := 0.0000; A_Matrix[1, 7] := 0.0000; A_Matrix[1, 8] := -0.1250;
    A_Matrix[2, 1] := 0.0000; A_Matrix[2, 2] := 0.9850; A_Matrix[2, 3] := 0.0000; A_Matrix[2, 4] := 0.0000; A_Matrix[2, 5] := 0.0000; A_Matrix[2, 6] := 0.0000; A_Matrix[2, 7] := 0.0000; A_Matrix[2, 8] := 0.0000;
    A_Matrix[3, 1] := 0.0010; A_Matrix[3, 2] := 0.0000; A_Matrix[3, 3] := 0.9650; A_Matrix[3, 4] := 0.0000; A_Matrix[3, 5] := 0.0000; A_Matrix[3, 6] := -0.0120; A_Matrix[3, 7] := 0.0000; A_Matrix[3, 8] := 0.0045;
    A_Matrix[4, 1] := 0.0018; A_Matrix[4, 2] := 0.0000; A_Matrix[4, 3] := 0.0000; A_Matrix[4, 4] := 0.9200; A_Matrix[4, 5] := 0.0450; A_Matrix[4, 6] := 0.0000; A_Matrix[4, 7] := 0.0000; A_Matrix[4, 8] := 0.0000;
    A_Matrix[5, 1] := 0.0000; A_Matrix[5, 2] := 0.0000; A_Matrix[5, 3] := 0.0000; A_Matrix[5, 4] := 0.0000; A_Matrix[5, 5] := 0.9880; A_Matrix[5, 6] := 0.0000; A_Matrix[5, 7] := 0.0000; A_Matrix[5, 8] := 0.0000;
    A_Matrix[6, 1] := 0.0000; A_Matrix[6, 2] := 0.0000; A_Matrix[6, 3] := 0.0450; A_Matrix[6, 4] := 0.0000; A_Matrix[6, 5] := 0.0000; A_Matrix[6, 6] := 0.9500; A_Matrix[6, 7] := 0.0000; A_Matrix[6, 8] := 0.0000;
    A_Matrix[7, 1] := 0.0000; A_Matrix[7, 2] := 0.0000; A_Matrix[7, 3] := -0.0850; A_Matrix[7, 4] := 0.0000; A_Matrix[7, 5] := 0.0000; A_Matrix[7, 6] := 0.0000; A_Matrix[7, 7] := 0.9300; A_Matrix[7, 8] := 0.0850;
    A_Matrix[8, 1] := 0.0000; A_Matrix[8, 2] := 0.0000; A_Matrix[8, 3] := 0.0150; A_Matrix[8, 4] := 0.0000; A_Matrix[8, 5] := 0.0000; A_Matrix[8, 6] := 0.0000; A_Matrix[8, 7] := 0.0000; A_Matrix[8, 8] := 0.9400;

    (* ------------------------------------------------------------------------- *)
    (* Discrete Control Input Matrix B (8x4)                                     *)
    (* Inputs: 1:u_Trimmer_Pos, 2:u_Garniture_Vel, 3:u_Knife_Phase, 4:u_Laser_Duty*)
    (* ------------------------------------------------------------------------- *)
    B_Matrix[1, 1] := 42.5000; B_Matrix[1, 2] := -2.1500; B_Matrix[1, 3] := 0.0000; B_Matrix[1, 4] := 0.0000;
    B_Matrix[2, 1] := 0.0150; B_Matrix[2, 2] := 0.0000; B_Matrix[2, 3] := 0.0000; B_Matrix[2, 4] := 0.0000;
    B_Matrix[3, 1] := 0.0000; B_Matrix[3, 2] := 0.0350; B_Matrix[3, 3] := 0.0000; B_Matrix[3, 4] := 0.0000;
    B_Matrix[4, 1] := 0.0000; B_Matrix[4, 2] := 0.0000; B_Matrix[4, 3] := 0.0000; B_Matrix[4, 4] := 0.0000;
    B_Matrix[5, 1] := 0.0000; B_Matrix[5, 2] := 0.0000; B_Matrix[5, 3] := 0.0000; B_Matrix[5, 4] := 0.0000;
    B_Matrix[6, 1] := 0.0000; B_Matrix[6, 2] := 0.0000; B_Matrix[6, 3] := 0.0500; B_Matrix[6, 4] := 0.0000;
    B_Matrix[7, 1] := 0.0000; B_Matrix[7, 2] := 0.0000; B_Matrix[7, 3] := 0.0000; B_Matrix[7, 4] := 0.3850;
    B_Matrix[8, 1] := 0.0000; B_Matrix[8, 2] := 0.0000; B_Matrix[8, 3] := 0.0000; B_Matrix[8, 4] := 0.0000;

    (* ------------------------------------------------------------------------- *)
    (* Discrete Measurement Matrix C (8x8)                                       *)
    (* ------------------------------------------------------------------------- *)
    C_Matrix[1, 1] := 1.0000; C_Matrix[1, 2] := 0.0000; C_Matrix[1, 3] := 0.0000; C_Matrix[1, 4] := 0.0000; C_Matrix[1, 5] := 0.0000; C_Matrix[1, 6] := 0.0000; C_Matrix[1, 7] := 0.0000; C_Matrix[1, 8] := 0.0000;
    C_Matrix[2, 1] := 0.0000; C_Matrix[2, 2] := 1.0000; C_Matrix[2, 3] := 0.0000; C_Matrix[2, 4] := 0.0000; C_Matrix[2, 5] := 0.0000; C_Matrix[2, 6] := 0.0000; C_Matrix[2, 7] := 0.0000; C_Matrix[2, 8] := 0.0000;
    C_Matrix[3, 1] := 0.0000; C_Matrix[3, 2] := 0.0000; C_Matrix[3, 3] := 1.0000; C_Matrix[3, 4] := 0.0000; C_Matrix[3, 5] := 0.0000; C_Matrix[3, 6] := 0.0000; C_Matrix[3, 7] := 0.0000; C_Matrix[3, 8] := 0.0000;
    C_Matrix[4, 1] := 0.0000; C_Matrix[4, 2] := 0.0000; C_Matrix[4, 3] := 0.0000; C_Matrix[4, 4] := 1.0000; C_Matrix[4, 5] := 0.0000; C_Matrix[4, 6] := 0.0000; C_Matrix[4, 7] := 0.0000; C_Matrix[4, 8] := 0.0000;
    C_Matrix[5, 1] := 0.0000; C_Matrix[5, 2] := 0.0000; C_Matrix[5, 3] := 0.0000; C_Matrix[5, 4] := 0.0000; C_Matrix[5, 5] := 1.0000; C_Matrix[5, 6] := 0.0000; C_Matrix[5, 7] := 0.0000; C_Matrix[5, 8] := 0.0000;
    C_Matrix[6, 1] := 0.0000; C_Matrix[6, 2] := 0.0000; C_Matrix[6, 3] := 0.0000; C_Matrix[6, 4] := 0.0000; C_Matrix[6, 5] := 0.0000; C_Matrix[6, 6] := 1.0000; C_Matrix[6, 7] := 0.0000; C_Matrix[6, 8] := 0.0000;
    C_Matrix[7, 1] := 0.0000; C_Matrix[7, 2] := 0.0000; C_Matrix[7, 3] := 0.0000; C_Matrix[7, 4] := 0.0000; C_Matrix[7, 5] := 0.0000; C_Matrix[7, 6] := 0.0000; C_Matrix[7, 7] := 1.0000; C_Matrix[7, 8] := 0.0000;
    C_Matrix[8, 1] := 0.0000; C_Matrix[8, 2] := 0.0000; C_Matrix[8, 3] := 0.0000; C_Matrix[8, 4] := 0.0000; C_Matrix[8, 5] := 0.0000; C_Matrix[8, 6] := 0.0000; C_Matrix[8, 7] := 0.0000; C_Matrix[8, 8] := 1.0000;

    (* ------------------------------------------------------------------------- *)
    (* Discrete Feedthrough Matrix D (8x4)                                       *)
    (* ------------------------------------------------------------------------- *)
    D_Matrix[1, 1] := 0.0; D_Matrix[1, 2] := 0.0; D_Matrix[1, 3] := 0.0; D_Matrix[1, 4] := 0.0;
    D_Matrix[2, 1] := 0.0; D_Matrix[2, 2] := 0.0; D_Matrix[2, 3] := 0.0; D_Matrix[2, 4] := 0.0;
    D_Matrix[3, 1] := 0.0; D_Matrix[3, 2] := 0.0; D_Matrix[3, 3] := 0.0; D_Matrix[3, 4] := 0.0;
    D_Matrix[4, 1] := 0.0; D_Matrix[4, 2] := 0.0; D_Matrix[4, 3] := 0.0; D_Matrix[4, 4] := 0.0;
    D_Matrix[5, 1] := 0.0; D_Matrix[5, 2] := 0.0; D_Matrix[5, 3] := 0.0; D_Matrix[5, 4] := 0.0;
    D_Matrix[6, 1] := 0.0; D_Matrix[6, 2] := 0.0; D_Matrix[6, 3] := 0.0; D_Matrix[6, 4] := 0.0;
    D_Matrix[7, 1] := 0.0; D_Matrix[7, 2] := 0.0; D_Matrix[7, 3] := 0.0; D_Matrix[7, 4] := 0.0;
    D_Matrix[8, 1] := 0.0; D_Matrix[8, 2] := 0.0; D_Matrix[8, 3] := 0.0; D_Matrix[8, 4] := 0.0;

    (* ------------------------------------------------------------------------- *)
    (* Steady-State Kalman Observer Gain Matrix L (8x8)                          *)
    (* ------------------------------------------------------------------------- *)
    L_Kalman[1, 1] := 0.2250; L_Kalman[1, 2] := -0.0500; L_Kalman[1, 3] := 0.0120; L_Kalman[1, 4] := 0.0450; L_Kalman[1, 5] := 0.0050; L_Kalman[1, 6] := 0.0000; L_Kalman[1, 7] := 0.0000; L_Kalman[1, 8] := -0.0025;
    L_Kalman[2, 1] := -0.0015; L_Kalman[2, 2] := 0.1850; L_Kalman[2, 3] := 0.0000; L_Kalman[2, 4] := 0.0000; L_Kalman[2, 5] := 0.0000; L_Kalman[2, 6] := 0.0000; L_Kalman[2, 7] := 0.0000; L_Kalman[2, 8] := 0.0000;
    L_Kalman[3, 1] := 0.0008; L_Kalman[3, 2] := 0.0000; L_Kalman[3, 3] := 0.2100; L_Kalman[3, 4] := 0.0000; L_Kalman[3, 5] := 0.0000; L_Kalman[3, 6] := -0.0045; L_Kalman[3, 7] := 0.0000; L_Kalman[3, 8] := 0.0015;
    L_Kalman[4, 1] := 0.0012; L_Kalman[4, 2] := 0.0000; L_Kalman[4, 3] := 0.0000; L_Kalman[4, 4] := 0.1950; L_Kalman[4, 5] := 0.0150; L_Kalman[4, 6] := 0.0000; L_Kalman[4, 7] := 0.0000; L_Kalman[4, 8] := 0.0000;
    L_Kalman[5, 1] := 0.0000; L_Kalman[5, 2] := 0.0000; L_Kalman[5, 3] := 0.0000; L_Kalman[5, 4] := 0.0000; L_Kalman[5, 5] := 0.2450; L_Kalman[5, 6] := 0.0000; L_Kalman[5, 7] := 0.0000; L_Kalman[5, 8] := 0.0000;
    L_Kalman[6, 1] := 0.0000; L_Kalman[6, 2] := 0.0000; L_Kalman[6, 3] := 0.0085; L_Kalman[6, 4] := 0.0000; L_Kalman[6, 5] := 0.0000; L_Kalman[6, 6] := 0.2850; L_Kalman[6, 7] := 0.0000; L_Kalman[6, 8] := 0.0000;
    L_Kalman[7, 1] := 0.0000; L_Kalman[7, 2] := 0.0000; L_Kalman[7, 3] := -0.0065; L_Kalman[7, 4] := 0.0000; L_Kalman[7, 5] := 0.0000; L_Kalman[7, 6] := 0.0000; L_Kalman[7, 7] := 0.2200; L_Kalman[7, 8] := 0.0185;
    L_Kalman[8, 1] := 0.0000; L_Kalman[8, 2] := 0.0000; L_Kalman[8, 3] := 0.0025; L_Kalman[8, 4] := 0.0000; L_Kalman[8, 5] := 0.0000; L_Kalman[8, 6] := 0.0000; L_Kalman[8, 7] := 0.0000; L_Kalman[8, 8] := 0.1750;

    (* ------------------------------------------------------------------------- *)
    (* Discrete Algebraic Riccati Equation Terminal Cost Matrix P (8x8)          *)
    (* ------------------------------------------------------------------------- *)
    P_Riccati[1, 1] := 14.8500; P_Riccati[1, 2] := -2.1500; P_Riccati[1, 3] := 0.4500; P_Riccati[1, 4] := 1.2500; P_Riccati[1, 5] := 0.1800; P_Riccati[1, 6] := 0.0000; P_Riccati[1, 7] := 0.0000; P_Riccati[1, 8] := -0.0450;
    P_Riccati[2, 1] := -2.1500; P_Riccati[2, 2] := 8.4500; P_Riccati[2, 3] := 0.0000; P_Riccati[2, 4] := 0.0000; P_Riccati[2, 5] := 0.0000; P_Riccati[2, 6] := 0.0000; P_Riccati[2, 7] := 0.0000; P_Riccati[2, 8] := 0.0000;
    P_Riccati[3, 1] := 0.4500; P_Riccati[3, 2] := 0.0000; P_Riccati[3, 3] := 12.3000; P_Riccati[3, 4] := 0.0000; P_Riccati[3, 5] := 0.0000; P_Riccati[3, 6] := -0.3500; P_Riccati[3, 7] := 0.0000; P_Riccati[3, 8] := 0.0850;
    P_Riccati[4, 1] := 1.2500; P_Riccati[4, 2] := 0.0000; P_Riccati[4, 3] := 0.0000; P_Riccati[4, 4] := 6.8500; P_Riccati[4, 5] := 0.4200; P_Riccati[4, 6] := 0.0000; P_Riccati[4, 7] := 0.0000; P_Riccati[4, 8] := 0.0000;
    P_Riccati[5, 1] := 0.1800; P_Riccati[5, 2] := 0.0000; P_Riccati[5, 3] := 0.0000; P_Riccati[5, 4] := 0.4200; P_Riccati[5, 5] := 18.5000; P_Riccati[5, 6] := 0.0000; P_Riccati[5, 7] := 0.0000; P_Riccati[5, 8] := 0.0000;
    P_Riccati[6, 1] := 0.0000; P_Riccati[6, 2] := 0.0000; P_Riccati[6, 3] := -0.3500; P_Riccati[6, 4] := 0.0000; P_Riccati[6, 5] := 0.0000; P_Riccati[6, 6] := 25.4000; P_Riccati[6, 7] := 0.0000; P_Riccati[6, 8] := 0.0000;
    P_Riccati[7, 1] := 0.0000; P_Riccati[7, 2] := 0.0000; P_Riccati[7, 3] := 0.0000; P_Riccati[7, 4] := 0.0000; P_Riccati[7, 5] := 0.0000; P_Riccati[7, 6] := 0.0000; P_Riccati[7, 7] := 16.2000; P_Riccati[7, 8] := 0.4500;
    P_Riccati[8, 1] := -0.0450; P_Riccati[8, 2] := 0.0000; P_Riccati[8, 3] := 0.0850; P_Riccati[8, 4] := 0.0000; P_Riccati[8, 5] := 0.0000; P_Riccati[8, 6] := 0.0000; P_Riccati[8, 7] := 0.4500; P_Riccati[8, 8] := 9.8000;

    (* ------------------------------------------------------------------------- *)
    (* MPC State Cost Diagonal Weights Q & Input Effort Weights R                *)
    (* ------------------------------------------------------------------------- *)
    Q_Weights[1] := 10.00; (* Penalty on Rod Mass Variance [mg] *)
    Q_Weights[2] := 1.50;  (* Penalty on Trimmer Mechanical Displacement *)
    Q_Weights[3] := 8.00;  (* Penalty on Rod Velocity Deviation *)
    Q_Weights[4] := 3.00;  (* Penalty on Dielectric Resonance Drift *)
    Q_Weights[5] := 12.00; (* Penalty on Rod Moisture Deviation [%] *)
    Q_Weights[6] := 20.00; (* Penalty on Knife Cutoff Phase Error [mrad] *)
    Q_Weights[7] := 15.00; (* Penalty on Ventilation Dilution Drift [%] *)
    Q_Weights[8] := 2.50;  (* Penalty on Transfer Drum Vacuum Loss [kPa] *)

    R_Weights[1] := 0.85;  (* Effort penalty on Trimmer Servo Slew Rate *)
    R_Weights[2] := 1.20;  (* Effort penalty on Garniture Velocity Trim *)
    R_Weights[3] := 2.50;  (* Effort penalty on Knife Phase Electronic Cam Trim *)
    R_Weights[4] := 0.45;  (* Effort penalty on Laser Duty Cycle Modulations *)

    (* State and control vector initializations *)
    FOR idx_i := 1 TO 8 DO
        x_State_Est[idx_i] := 0.0;
        x_State_Pred[idx_i] := 0.0;
        y_Meas[idx_i] := 0.0;
        y_Est[idx_i] := 0.0;
        r_Reference[idx_i] := 0.0;
        e_Tracking[idx_i] := 0.0;
    END_FOR;

    FOR idx_k := 1 TO 4 DO
        u_MPC[idx_k] := 0.0;
        u_MPC_Prev[idx_k] := 0.0;
        grad_J[idx_k] := 0.0;
    END_FOR;

    (* Initialize 128-cell shift register arrays *)
    FOR idx_i := 1 TO 128 DO
        sr_Cig_ID[idx_i] := 0;
        sr_Weight_mg[idx_i] := 950.0;
        sr_Moisture_pct[idx_i] := 12.5;
        sr_Diameter_mm[idx_i] := 7.80;
        sr_LooseEnd_Depth_mm[idx_i] := 0.0;
        sr_Ventilation_pct[idx_i] := 35.0;
        sr_Defect_Flags[idx_i] := 16#0000;
        sr_Eject_Command[idx_i] := FALSE;
    END_FOR;

    FOR idx_k := 1 TO 8 DO
        rReject_Pulse_Timer_s[idx_k] := 0.0;
        abReject_Air_Blast_Trig[idx_k] := FALSE;
    END_FOR;

    bInit_Done := TRUE;
END_IF;
''')
    return "".join(code)

print("Phase 0 code ready.")
# Append Phase 1 to build_full_code.py
def get_phase1_code():
    return '''
(* === PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY SENSOR VOTING & ARBITRATION === *)

(* ------------------------------------------------------------------------- *)
(* 1. TRIAD 1: MICROWAVE RESONANT CAVITY TOBACCO DENSITY SENSORS             *)
(* ------------------------------------------------------------------------- *)
IF (AI_MW_Density_ChA >= AI_MW_Density_ChB AND AI_MW_Density_ChA <= AI_MW_Density_ChC) OR 
   (AI_MW_Density_ChA <= AI_MW_Density_ChB AND AI_MW_Density_ChA >= AI_MW_Density_ChC) THEN
    rDensity_Med := AI_MW_Density_ChA;
ELSIF (AI_MW_Density_ChB >= AI_MW_Density_ChA AND AI_MW_Density_ChB <= AI_MW_Density_ChC) OR 
      (AI_MW_Density_ChB <= AI_MW_Density_ChA AND AI_MW_Density_ChB >= AI_MW_Density_ChC) THEN
    rDensity_Med := AI_MW_Density_ChB;
ELSE
    rDensity_Med := AI_MW_Density_ChC;
END_IF;

rDensity_Dev_AB := ABS(AI_MW_Density_ChA - AI_MW_Density_ChB);
rDensity_Dev_BC := ABS(AI_MW_Density_ChB - AI_MW_Density_ChC);
rDensity_Dev_CA := ABS(AI_MW_Density_ChC - AI_MW_Density_ChA);

(* Discrepancy accumulation timers (Persistence filter: 0.050 s) *)
IF rDensity_Dev_AB > 20.000 AND rDensity_Dev_CA > 20.000 THEN
    rDensity_Timer_A := rDensity_Timer_A + tDelta_s;
ELSE
    rDensity_Timer_A := MAX(0.000, rDensity_Timer_A - (2.000 * tDelta_s));
END_IF;

IF rDensity_Dev_AB > 20.000 AND rDensity_Dev_BC > 20.000 THEN
    rDensity_Timer_B := rDensity_Timer_B + tDelta_s;
ELSE
    rDensity_Timer_B := MAX(0.000, rDensity_Timer_B - (2.000 * tDelta_s));
END_IF;

IF rDensity_Dev_BC > 20.000 AND rDensity_Dev_CA > 20.000 THEN
    rDensity_Timer_C := rDensity_Timer_C + tDelta_s;
ELSE
    rDensity_Timer_C := MAX(0.000, rDensity_Timer_C - (2.000 * tDelta_s));
END_IF;

IF rDensity_Timer_A > 0.0500 THEN bDensity_Fault_A := TRUE; END_IF;
IF rDensity_Timer_B > 0.0500 THEN bDensity_Fault_B := TRUE; END_IF;
IF rDensity_Timer_C > 0.0500 THEN bDensity_Fault_C := TRUE; END_IF;

iDensity_Healthy_Count := 3;
IF bDensity_Fault_A THEN iDensity_Healthy_Count := iDensity_Healthy_Count - 1; END_IF;
IF bDensity_Fault_B THEN iDensity_Healthy_Count := iDensity_Healthy_Count - 1; END_IF;
IF bDensity_Fault_C THEN iDensity_Healthy_Count := iDensity_Healthy_Count - 1; END_IF;

IF iDensity_Healthy_Count = 3 THEN
    rVoted_Rod_Weight_mg := rDensity_Med;
ELSIF iDensity_Healthy_Count = 2 THEN
    IF bDensity_Fault_A THEN
        rVoted_Rod_Weight_mg := 0.500 * (AI_MW_Density_ChB + AI_MW_Density_ChC);
    ELSIF bDensity_Fault_B THEN
        rVoted_Rod_Weight_mg := 0.500 * (AI_MW_Density_ChA + AI_MW_Density_ChC);
    ELSE
        rVoted_Rod_Weight_mg := 0.500 * (AI_MW_Density_ChA + AI_MW_Density_ChB);
    END_IF;
ELSIF iDensity_Healthy_Count = 1 THEN
    IF NOT bDensity_Fault_A THEN
        rVoted_Rod_Weight_mg := AI_MW_Density_ChA;
    ELSIF NOT bDensity_Fault_B THEN
        rVoted_Rod_Weight_mg := AI_MW_Density_ChB;
    ELSE
        rVoted_Rod_Weight_mg := AI_MW_Density_ChC;
    END_IF;
ELSE
    (* Dual failure: Freeze to nominal setpoint and flag critical fault *)
    rVoted_Rod_Weight_mg := rSP_Target_Weight_mg;
END_IF;


(* ------------------------------------------------------------------------- *)
(* 2. TRIAD 2: MICROWAVE DIELECTRIC LOSS MOISTURE SENSORS                    *)
(* ------------------------------------------------------------------------- *)
IF (AI_MW_Moisture_ChA >= AI_MW_Moisture_ChB AND AI_MW_Moisture_ChA <= AI_MW_Moisture_ChC) OR 
   (AI_MW_Moisture_ChA <= AI_MW_Moisture_ChB AND AI_MW_Moisture_ChA >= AI_MW_Moisture_ChC) THEN
    rMoisture_Med := AI_MW_Moisture_ChA;
ELSIF (AI_MW_Moisture_ChB >= AI_MW_Moisture_ChA AND AI_MW_Moisture_ChB <= AI_MW_Moisture_ChC) OR 
      (AI_MW_Moisture_ChB <= AI_MW_Moisture_ChA AND AI_MW_Moisture_ChB >= AI_MW_Moisture_ChC) THEN
    rMoisture_Med := AI_MW_Moisture_ChB;
ELSE
    rMoisture_Med := AI_MW_Moisture_ChC;
END_IF;

rMoisture_Dev_AB := ABS(AI_MW_Moisture_ChA - AI_MW_Moisture_ChB);
rMoisture_Dev_BC := ABS(AI_MW_Moisture_ChB - AI_MW_Moisture_ChC);
rMoisture_Dev_CA := ABS(AI_MW_Moisture_ChC - AI_MW_Moisture_ChA);

IF rMoisture_Dev_AB > 0.600 AND rMoisture_Dev_CA > 0.600 THEN
    rMoisture_Timer_A := rMoisture_Timer_A + tDelta_s;
ELSE
    rMoisture_Timer_A := MAX(0.000, rMoisture_Timer_A - (2.000 * tDelta_s));
END_IF;

IF rMoisture_Dev_AB > 0.600 AND rMoisture_Dev_BC > 0.600 THEN
    rMoisture_Timer_B := rMoisture_Timer_B + tDelta_s;
ELSE
    rMoisture_Timer_B := MAX(0.000, rMoisture_Timer_B - (2.000 * tDelta_s));
END_IF;

IF rMoisture_Dev_BC > 0.600 AND rMoisture_Dev_CA > 0.600 THEN
    rMoisture_Timer_C := rMoisture_Timer_C + tDelta_s;
ELSE
    rMoisture_Timer_C := MAX(0.000, rMoisture_Timer_C - (2.000 * tDelta_s));
END_IF;

IF rMoisture_Timer_A > 0.0500 THEN bMoisture_Fault_A := TRUE; END_IF;
IF rMoisture_Timer_B > 0.0500 THEN bMoisture_Fault_B := TRUE; END_IF;
IF rMoisture_Timer_C > 0.0500 THEN bMoisture_Fault_C := TRUE; END_IF;

iMoisture_Healthy_Count := 3;
IF bMoisture_Fault_A THEN iMoisture_Healthy_Count := iMoisture_Healthy_Count - 1; END_IF;
IF bMoisture_Fault_B THEN iMoisture_Healthy_Count := iMoisture_Healthy_Count - 1; END_IF;
IF bMoisture_Fault_C THEN iMoisture_Healthy_Count := iMoisture_Healthy_Count - 1; END_IF;

IF iMoisture_Healthy_Count = 3 THEN
    rVoted_Rod_Moisture_pct := rMoisture_Med;
ELSIF iMoisture_Healthy_Count = 2 THEN
    IF bMoisture_Fault_A THEN
        rVoted_Rod_Moisture_pct := 0.500 * (AI_MW_Moisture_ChB + AI_MW_Moisture_ChC);
    ELSIF bMoisture_Fault_B THEN
        rVoted_Rod_Moisture_pct := 0.500 * (AI_MW_Moisture_ChA + AI_MW_Moisture_ChC);
    ELSE
        rVoted_Rod_Moisture_pct := 0.500 * (AI_MW_Moisture_ChA + AI_MW_Moisture_ChB);
    END_IF;
ELSIF iMoisture_Healthy_Count = 1 THEN
    IF NOT bMoisture_Fault_A THEN
        rVoted_Rod_Moisture_pct := AI_MW_Moisture_ChA;
    ELSIF NOT bMoisture_Fault_B THEN
        rVoted_Rod_Moisture_pct := AI_MW_Moisture_ChB;
    ELSE
        rVoted_Rod_Moisture_pct := AI_MW_Moisture_ChC;
    END_IF;
ELSE
    rVoted_Rod_Moisture_pct := rSP_Target_Moisture_pct;
END_IF;


(* ------------------------------------------------------------------------- *)
(* 3. TRIAD 3: HIGH-FREQUENCY DUAL-AXIS LASER DIAMETER GAUGES                *)
(* ------------------------------------------------------------------------- *)
IF (AI_Laser_Dia_ChA >= AI_Laser_Dia_ChB AND AI_Laser_Dia_ChA <= AI_Laser_Dia_ChC) OR 
   (AI_Laser_Dia_ChA <= AI_Laser_Dia_ChB AND AI_Laser_Dia_ChA >= AI_Laser_Dia_ChC) THEN
    rDiameter_Med := AI_Laser_Dia_ChA;
ELSIF (AI_Laser_Dia_ChB >= AI_Laser_Dia_ChA AND AI_Laser_Dia_ChB <= AI_Laser_Dia_ChC) OR 
      (AI_Laser_Dia_ChB <= AI_Laser_Dia_ChA AND AI_Laser_Dia_ChB >= AI_Laser_Dia_ChC) THEN
    rDiameter_Med := AI_Laser_Dia_ChB;
ELSE
    rDiameter_Med := AI_Laser_Dia_ChC;
END_IF;

rDiameter_Dev_AB := ABS(AI_Laser_Dia_ChA - AI_Laser_Dia_ChB);
rDiameter_Dev_BC := ABS(AI_Laser_Dia_ChB - AI_Laser_Dia_ChC);
rDiameter_Dev_CA := ABS(AI_Laser_Dia_ChC - AI_Laser_Dia_ChA);

IF rDiameter_Dev_AB > 0.040 AND rDiameter_Dev_CA > 0.040 THEN
    rDiameter_Timer_A := rDiameter_Timer_A + tDelta_s;
ELSE
    rDiameter_Timer_A := MAX(0.000, rDiameter_Timer_A - (2.000 * tDelta_s));
END_IF;

IF rDiameter_Dev_AB > 0.040 AND rDiameter_Dev_BC > 0.040 THEN
    rDiameter_Timer_B := rDiameter_Timer_B + tDelta_s;
ELSE
    rDiameter_Timer_B := MAX(0.000, rDiameter_Timer_B - (2.000 * tDelta_s));
END_IF;

IF rDiameter_Dev_BC > 0.040 AND rDiameter_Dev_CA > 0.040 THEN
    rDiameter_Timer_C := rDiameter_Timer_C + tDelta_s;
ELSE
    rDiameter_Timer_C := MAX(0.000, rDiameter_Timer_C - (2.000 * tDelta_s));
END_IF;

IF rDiameter_Timer_A > 0.0500 THEN bDiameter_Fault_A := TRUE; END_IF;
IF rDiameter_Timer_B > 0.0500 THEN bDiameter_Fault_B := TRUE; END_IF;
IF rDiameter_Timer_C > 0.0500 THEN bDiameter_Fault_C := TRUE; END_IF;

iDiameter_Healthy_Count := 3;
IF bDiameter_Fault_A THEN iDiameter_Healthy_Count := iDiameter_Healthy_Count - 1; END_IF;
IF bDiameter_Fault_B THEN iDiameter_Healthy_Count := iDiameter_Healthy_Count - 1; END_IF;
IF bDiameter_Fault_C THEN iDiameter_Healthy_Count := iDiameter_Healthy_Count - 1; END_IF;

IF iDiameter_Healthy_Count = 3 THEN
    rVoted_Rod_Diameter_mm := rDiameter_Med;
ELSIF iDiameter_Healthy_Count = 2 THEN
    IF bDiameter_Fault_A THEN
        rVoted_Rod_Diameter_mm := 0.500 * (AI_Laser_Dia_ChB + AI_Laser_Dia_ChC);
    ELSIF bDiameter_Fault_B THEN
        rVoted_Rod_Diameter_mm := 0.500 * (AI_Laser_Dia_ChA + AI_Laser_Dia_ChC);
    ELSE
        rVoted_Rod_Diameter_mm := 0.500 * (AI_Laser_Dia_ChA + AI_Laser_Dia_ChB);
    END_IF;
ELSIF iDiameter_Healthy_Count = 1 THEN
    IF NOT bDiameter_Fault_A THEN
        rVoted_Rod_Diameter_mm := AI_Laser_Dia_ChA;
    ELSIF NOT bDiameter_Fault_B THEN
        rVoted_Rod_Diameter_mm := AI_Laser_Dia_ChB;
    ELSE
        rVoted_Rod_Diameter_mm := AI_Laser_Dia_ChC;
    END_IF;
ELSE
    rVoted_Rod_Diameter_mm := rSP_Target_Diameter_mm;
END_IF;


(* ------------------------------------------------------------------------- *)
(* 4. TRIAD 4: MAIN LINE SHAFT VIRTUAL MASTER SERVO VELOCITY ENCODERS       *)
(* ------------------------------------------------------------------------- *)
IF (AI_LineShaft_Speed_ChA >= AI_LineShaft_Speed_ChB AND AI_LineShaft_Speed_ChA <= AI_LineShaft_Speed_ChC) OR 
   (AI_LineShaft_Speed_ChA <= AI_LineShaft_Speed_ChB AND AI_LineShaft_Speed_ChA >= AI_LineShaft_Speed_ChC) THEN
    rLineSpeed_Med := AI_LineShaft_Speed_ChA;
ELSIF (AI_LineShaft_Speed_ChB >= AI_LineShaft_Speed_ChA AND AI_LineShaft_Speed_ChB <= AI_LineShaft_Speed_ChC) OR 
      (AI_LineShaft_Speed_ChB <= AI_LineShaft_Speed_ChA AND AI_LineShaft_Speed_ChB >= AI_LineShaft_Speed_ChC) THEN
    rLineSpeed_Med := AI_LineShaft_Speed_ChB;
ELSE
    rLineSpeed_Med := AI_LineShaft_Speed_ChC;
END_IF;

rLineSpeed_Dev_AB := ABS(AI_LineShaft_Speed_ChA - AI_LineShaft_Speed_ChB);
rLineSpeed_Dev_BC := ABS(AI_LineShaft_Speed_ChB - AI_LineShaft_Speed_ChC);
rLineSpeed_Dev_CA := ABS(AI_LineShaft_Speed_ChC - AI_LineShaft_Speed_ChA);

IF rLineSpeed_Dev_AB > 0.800 AND rLineSpeed_Dev_CA > 0.800 THEN
    rLineSpeed_Timer_A := rLineSpeed_Timer_A + tDelta_s;
ELSE
    rLineSpeed_Timer_A := MAX(0.000, rLineSpeed_Timer_A - (2.000 * tDelta_s));
END_IF;

IF rLineSpeed_Dev_AB > 0.800 AND rLineSpeed_Dev_BC > 0.800 THEN
    rLineSpeed_Timer_B := rLineSpeed_Timer_B + tDelta_s;
ELSE
    rLineSpeed_Timer_B := MAX(0.000, rLineSpeed_Timer_B - (2.000 * tDelta_s));
END_IF;

IF rLineSpeed_Dev_BC > 0.800 AND rLineSpeed_Dev_CA > 0.800 THEN
    rLineSpeed_Timer_C := rLineSpeed_Timer_C + tDelta_s;
ELSE
    rLineSpeed_Timer_C := MAX(0.000, rLineSpeed_Timer_C - (2.000 * tDelta_s));
END_IF;

IF rLineSpeed_Timer_A > 0.0500 THEN bLineSpeed_Fault_A := TRUE; END_IF;
IF rLineSpeed_Timer_B > 0.0500 THEN bLineSpeed_Fault_B := TRUE; END_IF;
IF rLineSpeed_Timer_C > 0.0500 THEN bLineSpeed_Fault_C := TRUE; END_IF;

iLineSpeed_Healthy_Count := 3;
IF bLineSpeed_Fault_A THEN iLineSpeed_Healthy_Count := iLineSpeed_Healthy_Count - 1; END_IF;
IF bLineSpeed_Fault_B THEN iLineSpeed_Healthy_Count := iLineSpeed_Healthy_Count - 1; END_IF;
IF bLineSpeed_Fault_C THEN iLineSpeed_Healthy_Count := iLineSpeed_Healthy_Count - 1; END_IF;

IF iLineSpeed_Healthy_Count = 3 THEN
    rVoted_Line_Speed_ms := rLineSpeed_Med;
ELSIF iLineSpeed_Healthy_Count = 2 THEN
    IF bLineSpeed_Fault_A THEN
        rVoted_Line_Speed_ms := 0.500 * (AI_LineShaft_Speed_ChB + AI_LineShaft_Speed_ChC);
    ELSIF bLineSpeed_Fault_B THEN
        rVoted_Line_Speed_ms := 0.500 * (AI_LineShaft_Speed_ChA + AI_LineShaft_Speed_ChC);
    ELSE
        rVoted_Line_Speed_ms := 0.500 * (AI_LineShaft_Speed_ChA + AI_LineShaft_Speed_ChB);
    END_IF;
ELSIF iLineSpeed_Healthy_Count = 1 THEN
    IF NOT bLineSpeed_Fault_A THEN
        rVoted_Line_Speed_ms := AI_LineShaft_Speed_ChA;
    ELSIF NOT bLineSpeed_Fault_B THEN
        rVoted_Line_Speed_ms := AI_LineShaft_Speed_ChB;
    ELSE
        rVoted_Line_Speed_ms := AI_LineShaft_Speed_ChC;
    END_IF;
ELSE
    rVoted_Line_Speed_ms := 0.000;
END_IF;


(* ------------------------------------------------------------------------- *)
(* 5. TRIAD 5: FLUTED TRANSFER DRUM PNEUMATIC VACUUM TRANSMITTERS            *)
(* ------------------------------------------------------------------------- *)
IF (AI_Drum_Vacuum_ChA >= AI_Drum_Vacuum_ChB AND AI_Drum_Vacuum_ChA <= AI_Drum_Vacuum_ChC) OR 
   (AI_Drum_Vacuum_ChA <= AI_Drum_Vacuum_ChB AND AI_Drum_Vacuum_ChA >= AI_Drum_Vacuum_ChC) THEN
    rDrumVac_Med := AI_Drum_Vacuum_ChA;
ELSIF (AI_Drum_Vacuum_ChB >= AI_Drum_Vacuum_ChA AND AI_Drum_Vacuum_ChB <= AI_Drum_Vacuum_ChC) OR 
      (AI_Drum_Vacuum_ChB <= AI_Drum_Vacuum_ChA AND AI_Drum_Vacuum_ChB >= AI_Drum_Vacuum_ChC) THEN
    rDrumVac_Med := AI_Drum_Vacuum_ChB;
ELSE
    rDrumVac_Med := AI_Drum_Vacuum_ChC;
END_IF;

rDrumVac_Dev_AB := ABS(AI_Drum_Vacuum_ChA - AI_Drum_Vacuum_ChB);
rDrumVac_Dev_BC := ABS(AI_Drum_Vacuum_ChB - AI_Drum_Vacuum_ChC);
rDrumVac_Dev_CA := ABS(AI_Drum_Vacuum_ChC - AI_Drum_Vacuum_ChA);

IF rDrumVac_Dev_AB > 8.000 AND rDrumVac_Dev_CA > 8.000 THEN
    rDrumVac_Timer_A := rDrumVac_Timer_A + tDelta_s;
ELSE
    rDrumVac_Timer_A := MAX(0.000, rDrumVac_Timer_A - (2.000 * tDelta_s));
END_IF;

IF rDrumVac_Dev_AB > 8.000 AND rDrumVac_Dev_BC > 8.000 THEN
    rDrumVac_Timer_B := rDrumVac_Timer_B + tDelta_s;
ELSE
    rDrumVac_Timer_B := MAX(0.000, rDrumVac_Timer_B - (2.000 * tDelta_s));
END_IF;

IF rDrumVac_Dev_BC > 8.000 AND rDrumVac_Dev_CA > 8.000 THEN
    rDrumVac_Timer_C := rDrumVac_Timer_C + tDelta_s;
ELSE
    rDrumVac_Timer_C := MAX(0.000, rDrumVac_Timer_C - (2.000 * tDelta_s));
END_IF;

IF rDrumVac_Timer_A > 0.0500 THEN bDrumVac_Fault_A := TRUE; END_IF;
IF rDrumVac_Timer_B > 0.0500 THEN bDrumVac_Fault_B := TRUE; END_IF;
IF rDrumVac_Timer_C > 0.0500 THEN bDrumVac_Fault_C := TRUE; END_IF;

iDrumVac_Healthy_Count := 3;
IF bDrumVac_Fault_A THEN iDrumVac_Healthy_Count := iDrumVac_Healthy_Count - 1; END_IF;
IF bDrumVac_Fault_B THEN iDrumVac_Healthy_Count := iDrumVac_Healthy_Count - 1; END_IF;
IF bDrumVac_Fault_C THEN iDrumVac_Healthy_Count := iDrumVac_Healthy_Count - 1; END_IF;

IF iDrumVac_Healthy_Count = 3 THEN
    rVoted_Drum_Vacuum_kPa := rDrumVac_Med;
ELSIF iDrumVac_Healthy_Count = 2 THEN
    IF bDrumVac_Fault_A THEN
        rVoted_Drum_Vacuum_kPa := 0.500 * (AI_Drum_Vacuum_ChB + AI_Drum_Vacuum_ChC);
    ELSIF bDrumVac_Fault_B THEN
        rVoted_Drum_Vacuum_kPa := 0.500 * (AI_Drum_Vacuum_ChA + AI_Drum_Vacuum_ChC);
    ELSE
        rVoted_Drum_Vacuum_kPa := 0.500 * (AI_Drum_Vacuum_ChA + AI_Drum_Vacuum_ChB);
    END_IF;
ELSIF iDrumVac_Healthy_Count = 1 THEN
    IF NOT bDrumVac_Fault_A THEN
        rVoted_Drum_Vacuum_kPa := AI_Drum_Vacuum_ChA;
    ELSIF NOT bDrumVac_Fault_B THEN
        rVoted_Drum_Vacuum_kPa := AI_Drum_Vacuum_ChB;
    ELSE
        rVoted_Drum_Vacuum_kPa := AI_Drum_Vacuum_ChC;
    END_IF;
ELSE
    rVoted_Drum_Vacuum_kPa := -75.000;
END_IF;
'''

print("Phase 1 code ready.")
# Append Phase 2 and Phase 3 to build_full_code.py
def get_phase2_code():
    return '''
(* === PHASE 2: ADVANCED CYBER-PHYSICAL OBSERVERS & MULTIPHYSICS ESTIMATION === *)

(* 1. Temperature-Compensated Microwave Resonant Cavity Calculations *)
(* Real permittivity thermal expansion compensation: alpha = 0.00185 1/K *)
rComp_Density := rVoted_Rod_Weight_mg * (1.000 - (0.00185 * (AI_Infeed_Tobacco_Temp_degC - 20.000)) + (0.000045 * (AI_Infeed_Tobacco_Temp_degC - 20.000) * (AI_Infeed_Tobacco_Temp_degC - 20.000)));

(* Dielectric loss Arrhenius moisture compensation: beta = 0.00342 1/K *)
rComp_Moisture := rVoted_Rod_Moisture_pct * (1.000 - (0.00342 * (AI_Infeed_Tobacco_Temp_degC - 20.000)));

(* 2. Laser Micrometer Geometric Cross-Section & Ovality Calculation *)
(* Elliptical cross-section: Area = pi * (dx / 2) * (dy / 2) *)
rCrossSectionArea_mm2 := 3.14159265 * 0.250 * rVoted_Rod_Diameter_mm * (rVoted_Rod_Diameter_mm + AI_Laser_Ovality_ChA);

(* Tobacco rod porous bed permeability estimation: Darcy law *)
IF ABS(rVoted_Drum_Vacuum_kPa) > 5.000 THEN
    rCalc_Permeability := (0.0182 * 12.500 * (rVoted_Line_Speed_ms / 27.778)) / ABS(rVoted_Drum_Vacuum_kPa);
ELSE
    rCalc_Permeability := 1.250;
END_IF;

(* 3. Online Welford Algorithm for Unbiased Mass Variance & Standard Deviation *)
IF rVoted_Line_Speed_ms > 5.000 AND iFSM_Internal_State >= 4 THEN
    udiWelford_Count := udiWelford_Count + 1;
    rWelford_Delta := rComp_Density - rWelford_Mean;
    rWelford_Mean := rWelford_Mean + (rWelford_Delta / UDINT_TO_REAL(udiWelford_Count));
    rWelford_Delta2 := rComp_Density - rWelford_Mean;
    rWelford_M2 := rWelford_M2 + (rWelford_Delta * rWelford_Delta2);
    
    IF udiWelford_Count > 1 THEN
        rWelford_Variance := rWelford_M2 / UDINT_TO_REAL(udiWelford_Count - 1);
        IF rWelford_Variance > 0.000100 THEN
            rStat_Weight_StdDev_mg := SQRT(rWelford_Variance);
        ELSE
            rStat_Weight_StdDev_mg := 0.000;
        END_IF;
    END_IF;
    rStat_Weight_Mean_mg := rWelford_Mean;
END_IF;

(* 4. Flying Shear Accelerometer Acoustic Emission Exponential Smoothing Filter *)
rKnife_Vib_Filtered := (0.950 * rKnife_Vib_Filtered) + (0.050 * AI_Knife_Vibration_RMS_mms);

(* 5. Online Filter Ventilation Dilution Ratio Hydrodynamic Model *)
(* Modeled dilution ratio based on laser hole geometry and pressure drop *)
IF rVoted_Line_Speed_ms > 2.000 AND AI_Laser_Perf_Power_W > 10.000 THEN
    rCalc_Ventilation_pct := (AI_Laser_Perf_Power_W / 85.000) * 35.000 * (1.000 + (0.0085 * (ABS(rVoted_Drum_Vacuum_kPa) - 75.000)));
ELSE
    rCalc_Ventilation_pct := 0.000;
END_IF;
'''

def get_phase3_code():
    return '''
(* === PHASE 3: DISCRETE 8x8 STATE-SPACE MODEL & KALMAN OBSERVER STATE UPDATE === *)

(* 1. Assemble Pre-Processed Measurement Vector y_Meas (8x1) *)
y_Meas[1] := rComp_Density;
y_Meas[2] := u_MPC[1]; (* Trimmer disc actual vertical position *)
y_Meas[3] := rVoted_Line_Speed_ms;
y_Meas[4] := (rComp_Density - 950.000) * 0.00220; (* Resonant cavity dielectric shift *)
y_Meas[5] := rComp_Moisture;
y_Meas[6] := rKnife_Sync_Phase_Error_rad;
y_Meas[7] := rCalc_Ventilation_pct;
y_Meas[8] := rVoted_Drum_Vacuum_kPa;

(* 2. Reconstruct Measurement Vector from State Prediction: y_Est = C * x_Pred + D * u *)
FOR idx_i := 1 TO 8 DO
    rTemp_Sum := 0.000;
    FOR idx_j := 1 TO 8 DO
        rTemp_Sum := rTemp_Sum + (C_Matrix[idx_i, idx_j] * x_State_Pred[idx_j]);
    END_FOR;
    FOR idx_k := 1 TO 4 DO
        rTemp_Sum := rTemp_Sum + (D_Matrix[idx_i, idx_k] * u_MPC[idx_k]);
    END_FOR;
    y_Est[idx_i] := rTemp_Sum;
END_FOR;

(* 3. Kalman Innovation Measurement Update: x_Est = x_Pred + L * (y_Meas - y_Est) *)
FOR idx_i := 1 TO 8 DO
    rTemp_Sum := 0.000;
    FOR idx_j := 1 TO 8 DO
        rTemp_Sum := rTemp_Sum + (L_Kalman[idx_i, idx_j] * (y_Meas[idx_j] - y_Est[idx_j]));
    END_FOR;
    x_State_Est[idx_i] := x_State_Pred[idx_i] + rTemp_Sum;
END_FOR;

(* 4. State Prediction for Next Time Step k+1: x_Pred = A * x_Est + B * u *)
FOR idx_i := 1 TO 8 DO
    rTemp_Sum := 0.000;
    FOR idx_j := 1 TO 8 DO
        rTemp_Sum := rTemp_Sum + (A_Matrix[idx_i, idx_j] * x_State_Est[idx_j]);
    END_FOR;
    FOR idx_k := 1 TO 4 DO
        rTemp_Sum := rTemp_Sum + (B_Matrix[idx_i, idx_k] * u_MPC[idx_k]);
    END_FOR;
    x_State_Pred[idx_i] := rTemp_Sum;
END_FOR;

(* 5. Update State Tracking Error Vector: e = x_Pred - r_Reference *)
r_Reference[1] := rSP_Target_Weight_mg;
r_Reference[2] := 0.000; (* Zero trimmer nominal bias *)
r_Reference[3] := rSP_Production_Rate_cpm * (83.3333 / 60000.000); (* 27.778 m/s for 20,000 cpm *)
r_Reference[4] := 0.000; (* Zero dielectric drift *)
r_Reference[5] := rSP_Target_Moisture_pct;
r_Reference[6] := 0.000; (* Zero knife phase error *)
r_Reference[7] := rSP_Target_Ventilation_pct;
r_Reference[8] := -75.000; (* Nominal drum vacuum level [kPa] *)

FOR idx_i := 1 TO 8 DO
    e_Tracking[idx_i] := x_State_Pred[idx_i] - r_Reference[idx_i];
END_FOR;
'''

print("Phases 2 and 3 code ready.")
# Append Phase 4 and Phase 5 to build_full_code.py
def get_phase4_code():
    return '''
(* === PHASE 4: RECEDING-HORIZON MPC PROJECTED GRADIENT DESCENT OPTIMIZATION === *)

(* 1. Compute Intermediate Cost Vector: z_Riccati = P * e_Tracking (8x1) *)
FOR idx_i := 1 TO 8 DO
    rTemp_Sum := 0.000;
    FOR idx_j := 1 TO 8 DO
        rTemp_Sum := rTemp_Sum + (P_Riccati[idx_i, idx_j] * e_Tracking[idx_j]);
    END_FOR;
    (* Re-use y_Est array temporarily to store Riccati intermediate product to save memory *)
    y_Est[idx_i] := rTemp_Sum;
END_FOR;

(* 2. Compute Objective Gradient with Respect to Control Inputs: grad_J = B^T * z + R * u *)
FOR idx_k := 1 TO 4 DO
    rTemp_Sum := 0.000;
    FOR idx_i := 1 TO 8 DO
        rTemp_Sum := rTemp_Sum + (B_Matrix[idx_i, idx_k] * y_Est[idx_i]);
    END_FOR;
    grad_J[idx_k] := rTemp_Sum + (R_Weights[idx_k] * u_MPC[idx_k]);
END_FOR;

(* 3. Iterative Projected Gradient Descent (3 Fast Iterations Per Scan) *)
FOR idx_iter := 1 TO 3 DO
    (* Gradient Descent Candidate Step: u = u - alpha * grad_J *)
    FOR idx_k := 1 TO 4 DO
        u_MPC[idx_k] := u_MPC[idx_k] - (rAlpha_Step * grad_J[idx_k]);
    END_FOR;

    (* Actuator 1: Trimming Disc Vertical Position Projection [-3.0 mm, +3.0 mm] *)
    IF u_MPC[1] > 3.000 THEN
        u_MPC[1] := 3.000;
    ELSIF u_MPC[1] < -3.000 THEN
        u_MPC[1] := -3.000;
    END_IF;

    (* Actuator 2: Garniture Velocity Trim Projection [-1.5 m/s, +1.5 m/s] *)
    IF u_MPC[2] > 1.500 THEN
        u_MPC[2] := 1.500;
    ELSIF u_MPC[2] < -1.500 THEN
        u_MPC[2] := -1.500;
    END_IF;

    (* Actuator 3: Knife Electronic Cam Phase Trim Projection [-0.15 rad, +0.15 rad] *)
    IF u_MPC[3] > 0.150 THEN
        u_MPC[3] := 0.150;
    ELSIF u_MPC[3] < -0.150 THEN
        u_MPC[3] := -0.150;
    END_IF;

    (* Actuator 4: Laser Perforation Duty Cycle Projection [5.0 %, 95.0 %] *)
    IF u_MPC[4] > 95.000 THEN
        u_MPC[4] := 95.000;
    ELSIF u_MPC[4] < 5.000 THEN
        u_MPC[4] := 5.000;
    END_IF;

    (* Actuator Rate-Of-Change Slew Rate Limiters (Avoid Mechanical Shock) *)
    rDelta_U := u_MPC[1] - u_MPC_Prev[1];
    IF ABS(rDelta_U) > 0.050 THEN
        IF rDelta_U > 0.0 THEN
            u_MPC[1] := u_MPC_Prev[1] + 0.050;
        ELSE
            u_MPC[1] := u_MPC_Prev[1] - 0.050;
        END_IF;
    END_IF;

    rDelta_U := u_MPC[2] - u_MPC_Prev[2];
    IF ABS(rDelta_U) > 0.025 THEN
        IF rDelta_U > 0.0 THEN
            u_MPC[2] := u_MPC_Prev[2] + 0.025;
        ELSE
            u_MPC[2] := u_MPC_Prev[2] - 0.025;
        END_IF;
    END_IF;

    rDelta_U := u_MPC[3] - u_MPC_Prev[3];
    IF ABS(rDelta_U) > 0.005 THEN
        IF rDelta_U > 0.0 THEN
            u_MPC[3] := u_MPC_Prev[3] + 0.005;
        ELSE
            u_MPC[3] := u_MPC_Prev[3] - 0.005;
        END_IF;
    END_IF;

    rDelta_U := u_MPC[4] - u_MPC_Prev[4];
    IF ABS(rDelta_U) > 1.250 THEN
        IF rDelta_U > 0.0 THEN
            u_MPC[4] := u_MPC_Prev[4] + 1.250;
        ELSE
            u_MPC[4] := u_MPC_Prev[4] - 1.250;
        END_IF;
    END_IF;
END_FOR;

(* Store previous control action *)
FOR idx_k := 1 TO 4 DO
    u_MPC_Prev[idx_k] := u_MPC[idx_k];
END_FOR;
'''

def get_phase5_code():
    return '''
(* === PHASE 5: ROTARY KNIFE FLYING SHEAR CAM & SHARPENING STONE PROFILING === *)

(* 1. Flying Shear Synchronous Velocity & Angular Increment *)
(* 20,000 cpm = 333.33 cuts/s. For a 2-knife head: 166.67 rev/s = 1047.2 rad/s *)
IF rVoted_Line_Speed_ms > 0.100 THEN
    rCmd_Knife_Angular_Speed_rads := (rVoted_Line_Speed_ms / 0.0833333) * 3.14159265;
ELSE
    rCmd_Knife_Angular_Speed_rads := 0.000;
END_IF;

(* Advance Rotary Knife Master Shaft Angle *)
rKnife_Shaft_Angle_rad := rKnife_Shaft_Angle_rad + (rCmd_Knife_Angular_Speed_rads * tDelta_s);
IF rKnife_Shaft_Angle_rad >= 6.2831853 THEN
    rKnife_Shaft_Angle_rad := rKnife_Shaft_Angle_rad - 6.2831853;
END_IF;

(* 2. Fifth-Order Cam Trajectory Profile Evaluation *)
(* Evaluates dimensionless progress tau over synchronization sector [-0.25 rad .. +0.25 rad] *)
IF rKnife_Shaft_Angle_rad < 0.2500 OR rKnife_Shaft_Angle_rad > 6.033185 THEN
    IF rKnife_Shaft_Angle_rad < 0.2500 THEN
        rTemp_Tau := (rKnife_Shaft_Angle_rad + 0.2500) / 0.5000;
    ELSE
        rTemp_Tau := (rKnife_Shaft_Angle_rad - 6.033185) / 0.5000;
    END_IF;
    rTemp_Tau := MAX(0.000, MIN(1.000, rTemp_Tau));
    
    (* Polynomial: s(tau) = 10*tau^3 - 15*tau^4 + 6*tau^5 *)
    rTemp_CamPos := (10.000 * rTemp_Tau * rTemp_Tau * rTemp_Tau) - 
                    (15.000 * rTemp_Tau * rTemp_Tau * rTemp_Tau * rTemp_Tau) + 
                    (6.000 * rTemp_Tau * rTemp_Tau * rTemp_Tau * rTemp_Tau * rTemp_Tau);
ELSE
    rTemp_CamPos := 0.000;
END_IF;

(* Knife Phase Error Computation *)
rKnife_Sync_Phase_Error_rad := (rKnife_Shaft_Angle_rad - 0.000) + u_MPC[3];

(* 3. Active Knife Blade Wear Degradation Model & Grinding Stone Micro-Infeed *)
IF rVoted_Line_Speed_ms > 5.000 AND iFSM_Internal_State >= 4 THEN
    (* Wear accumulates proportional to cut rag mass and cutting velocity *)
    rKnife_Blade_Wear_Depth_um := rKnife_Blade_Wear_Depth_um + (0.0000085 * (rVoted_Rod_Weight_mg / 950.000) * (rVoted_Line_Speed_ms / 27.778));
    rDiag_Knife_Wear_Pct := MIN(100.000, (rKnife_Blade_Wear_Depth_um / 25.000) * 100.000);
END_IF;

(* Automatic Sharpening Cycle Trigger *)
IF (udiKnife_Cuts_Since_Sharpen >= rSharpening_Interval_Cuts OR bCmd_Manual_Sharpen OR rKnife_Vib_Filtered > 11.500) AND NOT bSharpening_In_Progress THEN
    bSharpening_In_Progress := TRUE;
    rSharpening_Cycle_Timer_s := 0.000;
    rSharpening_Feed_Pulse_Timer_s := 0.000;
END_IF;

(* Sharpening Infeed State Machine Execution *)
IF bSharpening_In_Progress THEN
    rSharpening_Cycle_Timer_s := rSharpening_Cycle_Timer_s + tDelta_s;
    rSharpening_Feed_Pulse_Timer_s := rSharpening_Feed_Pulse_Timer_s + tDelta_s;
    
    (* Micro-infeed pulse generation at 20 Hz *)
    IF rSharpening_Feed_Pulse_Timer_s >= 0.0500 THEN
        rSharpening_Feed_Pulse_Timer_s := 0.000;
        bCmd_Sharpening_Step_Pulse := NOT bCmd_Sharpening_Step_Pulse;
    END_IF;
    
    (* Verify grinding stone motor current *)
    IF AI_Sharpening_Current_A > 4.200 THEN
        (* Excessive pressure: Back off pulse *)
        bCmd_Sharpening_Step_Pulse := FALSE;
    END_IF;
    
    (* Terminate sharpening cycle after 2.5 seconds or when vibration dampens *)
    IF rSharpening_Cycle_Timer_s >= 2.5000 THEN
        bSharpening_In_Progress := FALSE;
        bCmd_Sharpening_Step_Pulse := FALSE;
        udiKnife_Cuts_Since_Sharpen := 0;
        rKnife_Blade_Wear_Depth_um := MAX(0.000, rKnife_Blade_Wear_Depth_um - 18.000);
        rDiag_Knife_Wear_Pct := MIN(100.000, (rKnife_Blade_Wear_Depth_um / 25.000) * 100.000);
    END_IF;
ELSE
    bCmd_Sharpening_Step_Pulse := FALSE;
END_IF;
'''

print("Phases 4 and 5 code ready.")
# Append Phase 6 and Phase 7 to build_full_code.py
def get_phase6_code():
    return '''
(* === PHASE 6: FILTER TIP ATTACHMENT DRUM TRANSFER & LASER PERFORATION === *)

(* 1. Drum Transfer Pneumatic Vacuum Modulation *)
(* Scales drum vacuum blower VFD speed proportionally from 20 Hz (idle) to 50 Hz (20,000 cpm) *)
IF rVoted_Line_Speed_ms > 0.500 THEN
    rCmd_Vacuum_Blower_VFD_Hz := 20.000 + (30.000 * (rVoted_Line_Speed_ms / 27.778));
ELSE
    rCmd_Vacuum_Blower_VFD_Hz := 10.000;
END_IF;

(* 2. Seam Sealer Heating Iron Power Regulation (245 deg C Target) *)
IF AI_Seam_Sealer_Temp_degC < (rLimit_Seam_Temp_LL_degC + 5.000) THEN
    rCmd_Seam_Sealer_Power_pct := 100.000;
ELSIF AI_Seam_Sealer_Temp_degC > 245.000 THEN
    rCmd_Seam_Sealer_Power_pct := MAX(0.000, 45.000 - (2.500 * (AI_Seam_Sealer_Temp_degC - 245.000)));
ELSE
    rCmd_Seam_Sealer_Power_pct := MIN(100.000, 45.000 + (4.000 * (245.000 - AI_Seam_Sealer_Temp_degC)));
END_IF;

(* 3. Laser Perforation Optical Firing Modulation *)
IF rVoted_Line_Speed_ms > 2.000 AND iFSM_Internal_State = 7 THEN
    (* 4 perforations per circumference per track = 48.0 Hz per m/s *)
    rCmd_Laser_Pulse_Freq_Hz := 48.000 * rVoted_Line_Speed_ms;
    rCmd_Laser_DutyCycle_pct := u_MPC[4] * (rSP_Target_Ventilation_pct / 35.000);
ELSE
    rCmd_Laser_Pulse_Freq_Hz := 0.000;
    rCmd_Laser_DutyCycle_pct := 0.000;
END_IF;
'''

def get_phase7_code():
    return '''
(* === PHASE 7: 128-STAGE TRACKING SHIFT REGISTER & FAST SOLENOID REJECTION === *)

(* 1. Shift Register Propagation on Knife Cut Apex Event *)
IF (rKnife_Shaft_Angle_rad < (rCmd_Knife_Angular_Speed_rads * tDelta_s)) AND (rVoted_Line_Speed_ms > 1.000) THEN
    udiKnife_Total_Cuts := udiKnife_Total_Cuts + 1;
    udiKnife_Cuts_Since_Sharpen := udiKnife_Cuts_Since_Sharpen + 1;
    udiCount_Produced := udiCount_Produced + 1;

    (* Ripple shift 128 flutes forward *)
    FOR idx_i := 128 TO 2 BY -1 DO
        sr_Cig_ID[idx_i]            := sr_Cig_ID[idx_i - 1];
        sr_Weight_mg[idx_i]         := sr_Weight_mg[idx_i - 1];
        sr_Moisture_pct[idx_i]      := sr_Moisture_pct[idx_i - 1];
        sr_Diameter_mm[idx_i]       := sr_Diameter_mm[idx_i - 1];
        sr_LooseEnd_Depth_mm[idx_i] := sr_LooseEnd_Depth_mm[idx_i - 1];
        sr_Ventilation_pct[idx_i]   := sr_Ventilation_pct[idx_i - 1];
        sr_Defect_Flags[idx_i]      := sr_Defect_Flags[idx_i - 1];
        sr_Eject_Command[idx_i]     := sr_Eject_Command[idx_i - 1];
    END_FOR;

    (* Load new rod at Index 1 (Cutoff Knife Position) *)
    sr_Cig_ID[1]            := udiNextCigaretteID;
    udiNextCigaretteID      := udiNextCigaretteID + 1;
    sr_Weight_mg[1]         := rComp_Density;
    sr_Moisture_pct[1]      := rComp_Moisture;
    sr_Diameter_mm[1]       := rVoted_Rod_Diameter_mm;
    sr_LooseEnd_Depth_mm[1] := 0.000;
    sr_Ventilation_pct[1]   := rCalc_Ventilation_pct;
    sr_Defect_Flags[1]      := 16#0000;
    sr_Eject_Command[1]     := FALSE;
END_IF;

(* 2. Synchronous Inspection Station Defect Flagging Across Transfer Flutes *)
(* Station 18: Microwave Resonant Cavity Station *)
sr_Weight_mg[18]    := rComp_Density;
sr_Moisture_pct[18] := rComp_Moisture;
IF rComp_Density < rLimit_Weight_L_mg THEN
    sr_Defect_Flags[18] := sr_Defect_Flags[18] OR 16#0001; (* Bit 0: Underweight *)
END_IF;
IF rComp_Density > rLimit_Weight_H_mg THEN
    sr_Defect_Flags[18] := sr_Defect_Flags[18] OR 16#0002; (* Bit 1: Overweight *)
END_IF;
IF rComp_Moisture < rLimit_Moisture_L_pct OR rComp_Moisture > rLimit_Moisture_H_pct THEN
    sr_Defect_Flags[18] := sr_Defect_Flags[18] OR 16#0004; (* Bit 2: Moisture Out-of-Spec *)
END_IF;

(* Station 34: Laser Diameter & Ovality Micrometer *)
sr_Diameter_mm[34] := rVoted_Rod_Diameter_mm;
IF rVoted_Rod_Diameter_mm < rLimit_Diameter_L_mm OR rVoted_Rod_Diameter_mm > rLimit_Diameter_H_mm THEN
    sr_Defect_Flags[34] := sr_Defect_Flags[34] OR 16#0008; (* Bit 3: Diameter Out-of-Spec *)
END_IF;
IF AI_Laser_Ovality_ChA > 0.040 THEN
    sr_Defect_Flags[34] := sr_Defect_Flags[34] OR 16#0010; (* Bit 4: Excessive Ovality *)
END_IF;

(* Station 58: Filter Tip Drum Presence Sensor *)
IF NOT DI_Filter_Plug_Present THEN
    sr_Defect_Flags[58] := sr_Defect_Flags[58] OR 16#0020; (* Bit 5: Missing Filter Plug *)
END_IF;

(* Station 76: Dual-Wavelength Optical Loose-End Void Scanner *)
sr_LooseEnd_Depth_mm[76] := AI_LooseEnd_Optical_Depth_mm;
IF AI_LooseEnd_Optical_Depth_mm > 1.800 THEN
    sr_Defect_Flags[76] := sr_Defect_Flags[76] OR 16#0040; (* Bit 6: Loose End Tobacco Fallout *)
END_IF;

(* Station 94: Laser Ventilation Optical Evaluation *)
sr_Ventilation_pct[94] := rCalc_Ventilation_pct;
IF ABS(rCalc_Ventilation_pct - rSP_Target_Ventilation_pct) > 6.000 THEN
    sr_Defect_Flags[94] := sr_Defect_Flags[94] OR 16#0080; (* Bit 7: Ventilation Dilution Defect *)
END_IF;

(* 3. Station 116: Ultra-Fast 40-Bar Reject Blast Solenoid Actuation (< 1.2 ms) *)
IF (sr_Defect_Flags[116] <> 16#0000) AND NOT sr_Eject_Command[116] THEN
    sr_Eject_Command[116] := TRUE;
    abReject_Air_Blast_Trig[1] := TRUE;
    rReject_Pulse_Timer_s[1] := 0.001200; (* 1.2 ms firing duration *)
    
    udiCount_Rejected := udiCount_Rejected + 1;
    IF (sr_Defect_Flags[116] AND 16#0003) <> 16#0000 THEN
        udiCount_Weight_Rejects := udiCount_Weight_Rejects + 1;
    END_IF;
    IF (sr_Defect_Flags[116] AND 16#0040) <> 16#0000 THEN
        udiCount_LooseEnd_Rejects := udiCount_LooseEnd_Rejects + 1;
    END_IF;
END_IF;

(* Manage 40-Bar Solenoid Air Blast Pulse Duration Countdown *)
FOR idx_k := 1 TO 8 DO
    IF abReject_Air_Blast_Trig[idx_k] THEN
        rReject_Pulse_Timer_s[idx_k] := rReject_Pulse_Timer_s[idx_k] - tDelta_s;
        IF rReject_Pulse_Timer_s[idx_k] <= 0.000000 THEN
            abReject_Air_Blast_Trig[idx_k] := FALSE;
            rReject_Pulse_Timer_s[idx_k] := 0.000000;
        END_IF;
    END_IF;
END_FOR;
'''

print("Phases 6 and 7 code ready.")
# Append Phase 8 to build_full_code.py
def get_phase8_code():
    return '''
(* === PHASE 8: 12-STAGE DETERMINISTIC FINITE STATE MACHINE (FSM) === *)

rFSM_State_Timer_s := rFSM_State_Timer_s + tDelta_s;

(* Global Safety Interlock Override: Immediate Transition to State 11 *)
IF NOT bSafety_Circuit_OK OR (dwAlarms_Critical <> 16#00000000 AND iFSM_Internal_State <> 11) THEN
    iFSM_Internal_State := 11;
    rFSM_State_Timer_s := 0.000;
END_IF;

CASE iFSM_Internal_State OF
    0: (* ------------------------------------------------------------------ *)
       (* STATE 0: PURGE_INIT                                                *)
       (* Purge vacuum flutes, verify pneumatics, reset counters, check guards*)
       (* ------------------------------------------------------------------ *)
        bSystem_Ready_20k             := FALSE;
        rCmd_Trimmer_Height_mm        := 0.000;
        rCmd_Garniture_Velocity_ms    := 0.000;
        rCmd_Knife_Phase_Advance_mrad := 0.000;
        rCmd_Vacuum_Blower_VFD_Hz     := 10.000;
        rCmd_Seam_Sealer_Power_pct    := 0.000;
        bCmd_Sharpening_Step_Pulse    := FALSE;
        bCmd_Splicer_Actuate          := FALSE;

        IF bCmd_Machine_Run AND bSafety_Circuit_OK AND (AI_Reject_Air_Pressure_bar > 35.000) THEN
            IF rFSM_State_Timer_s >= rPurge_Duration_s THEN
                iFSM_Internal_State := 1;
                rFSM_State_Timer_s  := 0.000;
            END_IF;
        ELSE
            IF NOT bCmd_Machine_Run THEN
                rFSM_State_Timer_s := 0.000;
            END_IF;
        END_IF;

    1: (* ------------------------------------------------------------------ *)
       (* STATE 1: SUCTION_BAND_PRIME                                        *)
       (* Accelerate vacuum blowers, establish fluidized tobacco hopper feed *)
       (* ------------------------------------------------------------------ *)
        bSystem_Ready_20k             := FALSE;
        rCmd_Vacuum_Blower_VFD_Hz     := 45.000;
        rCmd_Trimmer_Height_mm        := 0.000;
        rCmd_Garniture_Velocity_ms    := 0.000;
        rCmd_Knife_Phase_Advance_mrad := 0.000;

        IF (rVoted_Drum_Vacuum_kPa <= -60.000) AND (AI_Hopper_Tobacco_Level_pct > 30.000) THEN
            IF rFSM_State_Timer_s >= rSuction_Prime_Duration_s THEN
                iFSM_Internal_State := 2;
                rFSM_State_Timer_s  := 0.000;
            END_IF;
        END_IF;

        IF NOT bCmd_Machine_Run THEN
            iFSM_Internal_State := 10;
            rFSM_State_Timer_s  := 0.000;
        END_IF;

    2: (* ------------------------------------------------------------------ *)
       (* STATE 2: PAPER_WEB_THREADING                                       *)
       (* Unwind cigarette paper web, tension garniture belt, warm seam iron *)
       (* ------------------------------------------------------------------ *)
        bSystem_Ready_20k          := FALSE;
        rCmd_Vacuum_Blower_VFD_Hz  := 45.000;
        rCmd_Garniture_Velocity_ms := 1.500; (* Low-speed threading crawl *)

        IF (AI_Garniture_Tape_Tension_N > 100.000) AND 
           (AI_Seam_Sealer_Temp_degC >= 230.000 AND AI_Seam_Sealer_Temp_degC <= 260.000) AND 
           (AI_Seam_Glue_Pressure_bar > 2.000) THEN
            IF rFSM_State_Timer_s >= rWeb_Thread_Duration_s THEN
                iFSM_Internal_State := 3;
                rFSM_State_Timer_s  := 0.000;
            END_IF;
        END_IF;

        IF NOT bCmd_Machine_Run THEN
            iFSM_Internal_State := 10;
            rFSM_State_Timer_s  := 0.000;
        END_IF;

    3: (* ------------------------------------------------------------------ *)
       (* STATE 3: BLADE_PRE_ACCEL                                           *)
       (* Spin flying shear rotary knife to idling speed, check vibration     *)
       (* ------------------------------------------------------------------ *)
        bSystem_Ready_20k             := FALSE;
        rCmd_Garniture_Velocity_ms    := 2.500;
        rCmd_Knife_Phase_Advance_mrad := 0.000;

        IF (rKnife_Vib_Filtered < 8.000) AND (rCmd_Knife_Angular_Speed_rads > 50.000) THEN
            IF rFSM_State_Timer_s >= rBlade_Accel_Duration_s THEN
                iFSM_Internal_State := 4;
                rFSM_State_Timer_s  := 0.000;
            END_IF;
        END_IF;

        IF NOT bCmd_Machine_Run THEN
            iFSM_Internal_State := 10;
            rFSM_State_Timer_s  := 0.000;
        END_IF;

    4: (* ------------------------------------------------------------------ *)
       (* STATE 4: SYNCHRONOUS_ROD_CUT                                       *)
       (* Engage electronic cam flying shear to moving rod at low test speed *)
       (* ------------------------------------------------------------------ *)
        bSystem_Ready_20k          := FALSE;
        rCmd_Garniture_Velocity_ms := 5.000; (* 3,600 cpm test speed *)
        rCmd_Trimmer_Height_mm     := u_MPC[1];

        IF (ABS(rKnife_Sync_Phase_Error_rad) < 0.080) AND (udiCount_Produced > 50) THEN
            IF rFSM_State_Timer_s >= rTest_Cut_Duration_s THEN
                iFSM_Internal_State := 5;
                rFSM_State_Timer_s  := 0.000;
            END_IF;
        END_IF;

        IF NOT bCmd_Machine_Run THEN
            iFSM_Internal_State := 10;
            rFSM_State_Timer_s  := 0.000;
        END_IF;

    5: (* ------------------------------------------------------------------ *)
       (* STATE 5: FILTER_TIPPING_SYNC                                       *)
       (* Engage fluted drums, 2-up filter plug feed & tipping gluing nozzle *)
       (* ------------------------------------------------------------------ *)
        bSystem_Ready_20k          := FALSE;
        rCmd_Garniture_Velocity_ms := 8.000; (* 5,760 cpm transition *)
        rCmd_Trimmer_Height_mm     := u_MPC[1];

        IF DI_Filter_Plug_Present AND (AI_Tipping_Paper_Tension_N > 15.000) AND 
           (AI_Tipping_Glue_Temp_degC >= 150.000) THEN
            IF rFSM_State_Timer_s >= rFilter_Sync_Duration_s THEN
                iFSM_Internal_State := 6;
                rFSM_State_Timer_s  := 0.000;
            END_IF;
        END_IF;

        IF NOT bCmd_Machine_Run THEN
            iFSM_Internal_State := 10;
            rFSM_State_Timer_s  := 0.000;
        END_IF;

    6: (* ------------------------------------------------------------------ *)
       (* STATE 6: QUALITY_SORTING_VERIFY                                    *)
       (* Calibrate microwave profiler, laser gauge & test reject solenoid   *)
       (* ------------------------------------------------------------------ *)
        bSystem_Ready_20k          := FALSE;
        rCmd_Garniture_Velocity_ms := 14.000; (* 10,000 cpm ramp *)
        rCmd_Trimmer_Height_mm     := u_MPC[1];

        IF (iDensity_Healthy_Count >= 2) AND (iDiameter_Healthy_Count >= 2) AND 
           (AI_Reject_Air_Pressure_bar >= 38.000) THEN
            IF rFSM_State_Timer_s >= rQuality_Verify_Duration_s THEN
                iFSM_Internal_State := 7;
                rFSM_State_Timer_s  := 0.000;
            END_IF;
        END_IF;

        IF NOT bCmd_Machine_Run THEN
            iFSM_Internal_State := 10;
            rFSM_State_Timer_s  := 0.000;
        END_IF;

    7: (* ------------------------------------------------------------------ *)
       (* STATE 7: STEADY_STATE_PRODUCTION_20K                               *)
       (* Full 20,000 cpm (333 Hz rod velocity, v_rod = 27.78 m/s), full MPC *)
       (* ------------------------------------------------------------------ *)
        bSystem_Ready_20k          := TRUE;
        rCmd_Garniture_Velocity_ms := 27.778 + u_MPC[2];
        rCmd_Trimmer_Height_mm     := u_MPC[1];
        rCmd_Knife_Phase_Advance_mrad := u_MPC[3];

        (* Transition to Auto-Splicer reel transfer *)
        IF bCmd_Auto_Splice OR (AI_Splicer_Bobbin_Angle_deg > 85.000) THEN
            iFSM_Internal_State := 8;
            rFSM_State_Timer_s  := 0.000;
        END_IF;

        (* Transition to Online Blade Sharpening *)
        IF bSharpening_In_Progress THEN
            iFSM_Internal_State := 9;
            rFSM_State_Timer_s  := 0.000;
        END_IF;

        (* Controlled Normal Stop Requested *)
        IF NOT bCmd_Machine_Run THEN
            iFSM_Internal_State := 10;
            rFSM_State_Timer_s  := 0.000;
        END_IF;

    8: (* ------------------------------------------------------------------ *)
       (* STATE 8: AUTO_SPLICER_REEL_TRANSFER                                *)
       (* High-speed flying splice of paper reel without stopping production *)
       (* ------------------------------------------------------------------ *)
        bSystem_Ready_20k          := TRUE;
        rCmd_Garniture_Velocity_ms := 27.778;
        rCmd_Trimmer_Height_mm     := u_MPC[1];
        rSplicer_Timer_s           := rSplicer_Timer_s + tDelta_s;

        IF rSplicer_Timer_s < 0.1500 THEN
            bCmd_Splicer_Actuate := TRUE;
        ELSE
            bCmd_Splicer_Actuate := FALSE;
        END_IF;

        IF rSplicer_Timer_s >= 0.8500 THEN
            rSplicer_Timer_s    := 0.000;
            iFSM_Internal_State := 7;
            rFSM_State_Timer_s  := 0.000;
        END_IF;

        IF NOT bCmd_Machine_Run THEN
            iFSM_Internal_State := 10;
            rFSM_State_Timer_s  := 0.000;
        END_IF;

    9: (* ------------------------------------------------------------------ *)
       (* STATE 9: BLADE_RESHARPEN_PROFILING                                 *)
       (* Active micro-infeed grinding stone dressing spinning blade edge    *)
       (* ------------------------------------------------------------------ *)
        bSystem_Ready_20k          := TRUE;
        rCmd_Garniture_Velocity_ms := 27.778 + u_MPC[2];
        rCmd_Trimmer_Height_mm     := u_MPC[1];

        IF NOT bSharpening_In_Progress THEN
            iFSM_Internal_State := 7;
            rFSM_State_Timer_s  := 0.000;
        END_IF;

        IF NOT bCmd_Machine_Run THEN
            iFSM_Internal_State := 10;
            rFSM_State_Timer_s  := 0.000;
        END_IF;

    10: (* ----------------------------------------------------------------- *)
        (* STATE 10: CONTROLLED_DECEL                                        *)
        (* Controlled line deceleration at 5 m/s^2, purge flutes and stop    *)
        (* ----------------------------------------------------------------- *)
        bSystem_Ready_20k          := FALSE;
        bCmd_Sharpening_Step_Pulse := FALSE;
        bCmd_Splicer_Actuate       := FALSE;
        rCmd_Trimmer_Height_mm     := 0.000;
        rDecel_Ramp_Timer_s        := rDecel_Ramp_Timer_s + tDelta_s;

        (* Controlled deceleration ramp *)
        IF rCmd_Garniture_Velocity_ms > 0.100 THEN
            rCmd_Garniture_Velocity_ms := MAX(0.000, rCmd_Garniture_Velocity_ms - (5.000 * tDelta_s));
        ELSE
            rCmd_Garniture_Velocity_ms := 0.000;
        END_IF;

        IF rCmd_Garniture_Velocity_ms <= 0.000 AND rDecel_Ramp_Timer_s >= 5.500 THEN
            rDecel_Ramp_Timer_s := 0.000;
            iFSM_Internal_State := 0;
            rFSM_State_Timer_s  := 0.000;
        END_IF;

    11: (* ----------------------------------------------------------------- *)
        (* STATE 11: EMERGENCY_KNIFE_CLAMP_STOP                              *)
        (* Hard safety trip: Instantly fire pneumatic caliper clamp on knife *)
        (* ----------------------------------------------------------------- *)
        bSystem_Ready_20k             := FALSE;
        rCmd_Garniture_Velocity_ms    := 0.000;
        rCmd_Trimmer_Height_mm        := 0.000;
        rCmd_Knife_Phase_Advance_mrad := 0.000;
        rCmd_Knife_Angular_Speed_rads := 0.000;
        rCmd_Laser_DutyCycle_pct      := 0.000;
        rCmd_Laser_Pulse_Freq_Hz      := 0.000;
        rCmd_Vacuum_Blower_VFD_Hz     := 0.000;
        rCmd_Seam_Sealer_Power_pct    := 0.000;
        bCmd_Sharpening_Step_Pulse    := FALSE;
        bCmd_Splicer_Actuate          := FALSE;
        
        rEmergency_Brake_Timer_s := rEmergency_Brake_Timer_s + tDelta_s;

        (* Latching trip: Requires operator reset, safety circuit healthy, and alarm acknowledge *)
        IF bSafety_Circuit_OK AND bCmd_Alarm_Ack AND (dwAlarms_Critical = 16#00000000) AND NOT bCmd_Machine_Run THEN
            IF rEmergency_Brake_Timer_s >= 2.000 THEN
                rEmergency_Brake_Timer_s := 0.000;
                iFSM_Internal_State      := 0;
                rFSM_State_Timer_s       := 0.000;
            END_IF;
        END_IF;

ELSE
    (* Invalid State Recovery Fallback *)
    iFSM_Internal_State := 11;
    rFSM_State_Timer_s  := 0.000;
END_CASE;

iFSM_State := iFSM_Internal_State;
'''

print("Phase 8 code ready.")
# Append Phase 9, Phase 10, and assemble to build_full_code.py
def get_phase9_code():
    return '''
(* === PHASE 9: ISA-18.2 FIVE-TIER MULTI-PARAMETRIC ALARM ENGINE === *)

(* 1. Debounce and Persistence Timers for Critical Limits *)
IF rVoted_Rod_Weight_mg > rLimit_Weight_HH_mg THEN
    rDebounce_Weight_HH_s := rDebounce_Weight_HH_s + tDelta_s;
ELSE
    rDebounce_Weight_HH_s := MAX(0.000, rDebounce_Weight_HH_s - (2.000 * tDelta_s));
END_IF;

IF rVoted_Rod_Weight_mg < rLimit_Weight_LL_mg THEN
    rDebounce_Weight_LL_s := rDebounce_Weight_LL_s + tDelta_s;
ELSE
    rDebounce_Weight_LL_s := MAX(0.000, rDebounce_Weight_LL_s - (2.000 * tDelta_s));
END_IF;

IF rVoted_Drum_Vacuum_kPa > rLimit_Vacuum_LL_kPa THEN (* Vacuum less negative than -55 kPa *)
    rDebounce_Vacuum_LL_s := rDebounce_Vacuum_LL_s + tDelta_s;
ELSE
    rDebounce_Vacuum_LL_s := MAX(0.000, rDebounce_Vacuum_LL_s - (2.000 * tDelta_s));
END_IF;

IF rKnife_Vib_Filtered > rLimit_Knife_Vib_HH_mms THEN
    rDebounce_Knife_HH_s := rDebounce_Knife_HH_s + tDelta_s;
ELSE
    rDebounce_Knife_HH_s := MAX(0.000, rDebounce_Knife_HH_s - (2.000 * tDelta_s));
END_IF;

(* 2. Reset or Acknowledge Alarms *)
IF bCmd_Alarm_Ack THEN
    dwAlarms_Critical   := 16#00000000;
    dwAlarms_Warning    := 16#00000000;
    dwAlarms_Diagnostic := 16#00000000;
END_IF;

(* 3. Evaluate Priority 1 Critical Hard Trip Alarms (dwAlarms_Critical) *)
IF NOT bSafety_Circuit_OK THEN
    dwAlarms_Critical := dwAlarms_Critical OR 16#00000001; (* Bit 0: Emergency Safety Interlock Broken *)
END_IF;

IF rDebounce_Knife_HH_s > 0.0200 THEN
    dwAlarms_Critical := dwAlarms_Critical OR 16#00000002; (* Bit 1: Cutoff Knife Extreme High-High Vibration *)
END_IF;

IF rDebounce_Vacuum_LL_s > 0.0500 AND (iFSM_Internal_State >= 4) THEN
    dwAlarms_Critical := dwAlarms_Critical OR 16#00000004; (* Bit 2: Drum Vacuum Severe Loss *)
END_IF;

IF AI_Reject_Air_Pressure_bar < 32.000 THEN
    dwAlarms_Critical := dwAlarms_Critical OR 16#00000008; (* Bit 3: 40-Bar Reject Air Pressure Depleted *)
END_IF;

IF AI_Seam_Sealer_Temp_degC > rLimit_Seam_Temp_HH_degC THEN
    dwAlarms_Critical := dwAlarms_Critical OR 16#00000010; (* Bit 4: Seam Sealer Thermal Runaway (> 295 deg C) *)
END_IF;

IF iDensity_Healthy_Count <= 1 THEN
    dwAlarms_Critical := dwAlarms_Critical OR 16#00000020; (* Bit 5: 2oo3 TMR Dual Sensor Failure on Density *)
END_IF;

IF iDiameter_Healthy_Count <= 1 THEN
    dwAlarms_Critical := dwAlarms_Critical OR 16#00000040; (* Bit 6: 2oo3 TMR Dual Sensor Failure on Diameter *)
END_IF;

IF iDrumVac_Healthy_Count <= 1 THEN
    dwAlarms_Critical := dwAlarms_Critical OR 16#00000080; (* Bit 7: 2oo3 TMR Dual Sensor Failure on Drum Vac *)
END_IF;

IF (rDebounce_Weight_HH_s > 0.1000 OR rDebounce_Weight_LL_s > 0.1000) AND (iFSM_Internal_State = 7) THEN
    dwAlarms_Critical := dwAlarms_Critical OR 16#00000100; (* Bit 8: Uncontrolled Rod Weight Runaway *)
END_IF;

(* 4. Evaluate Priority 2 Process Out-Of-Bounds Warnings (dwAlarms_Warning) *)
IF rVoted_Rod_Weight_mg > (rLimit_Weight_H_mg + rDeadband_Weight_mg) THEN
    dwAlarms_Warning := dwAlarms_Warning OR 16#00000001; (* Bit 0: Rod Weight High Warning *)
ELSIF rVoted_Rod_Weight_mg < (rLimit_Weight_H_mg - rDeadband_Weight_mg) THEN
    dwAlarms_Warning := dwAlarms_Warning AND 16#FFFFFFFE;
END_IF;

IF rVoted_Rod_Weight_mg < (rLimit_Weight_L_mg - rDeadband_Weight_mg) THEN
    dwAlarms_Warning := dwAlarms_Warning OR 16#00000002; (* Bit 1: Rod Weight Low Warning *)
ELSIF rVoted_Rod_Weight_mg > (rLimit_Weight_L_mg + rDeadband_Weight_mg) THEN
    dwAlarms_Warning := dwAlarms_Warning AND 16#FFFFFFFD;
END_IF;

IF rVoted_Rod_Moisture_pct > (rLimit_Moisture_H_pct + rDeadband_Moisture_pct) THEN
    dwAlarms_Warning := dwAlarms_Warning OR 16#00000004; (* Bit 2: Rod Moisture High Warning *)
ELSIF rVoted_Rod_Moisture_pct < (rLimit_Moisture_H_pct - rDeadband_Moisture_pct) THEN
    dwAlarms_Warning := dwAlarms_Warning AND 16#FFFFFFFB;
END_IF;

IF rVoted_Rod_Moisture_pct < (rLimit_Moisture_L_pct - rDeadband_Moisture_pct) THEN
    dwAlarms_Warning := dwAlarms_Warning OR 16#00000008; (* Bit 3: Rod Moisture Low Warning *)
ELSIF rVoted_Rod_Moisture_pct > (rLimit_Moisture_L_pct + rDeadband_Moisture_pct) THEN
    dwAlarms_Warning := dwAlarms_Warning AND 16#FFFFFFF7;
END_IF;

IF rVoted_Rod_Diameter_mm > (rLimit_Diameter_H_mm + rDeadband_Diameter_mm) THEN
    dwAlarms_Warning := dwAlarms_Warning OR 16#00000010; (* Bit 4: Rod Diameter High Warning *)
ELSIF rVoted_Rod_Diameter_mm < (rLimit_Diameter_H_mm - rDeadband_Diameter_mm) THEN
    dwAlarms_Warning := dwAlarms_Warning AND 16#FFFFFFEF;
END_IF;

IF rVoted_Rod_Diameter_mm < (rLimit_Diameter_L_mm - rDeadband_Diameter_mm) THEN
    dwAlarms_Warning := dwAlarms_Warning OR 16#00000020; (* Bit 5: Rod Diameter Low Warning *)
ELSIF rVoted_Rod_Diameter_mm > (rLimit_Diameter_L_mm + rDeadband_Diameter_mm) THEN
    dwAlarms_Warning := dwAlarms_Warning AND 16#FFFFFFDF;
END_IF;

IF AI_Laser_Ovality_ChA > 0.0350 THEN
    dwAlarms_Warning := dwAlarms_Warning OR 16#00000040; (* Bit 6: Rod Ovality Distortion *)
ELSE
    dwAlarms_Warning := dwAlarms_Warning AND 16#FFFFFFBF;
END_IF;

IF ABS(rCalc_Ventilation_pct - rSP_Target_Ventilation_pct) > 5.000 AND (iFSM_Internal_State = 7) THEN
    dwAlarms_Warning := dwAlarms_Warning OR 16#00000080; (* Bit 7: Filter Ventilation Dilution Deviation *)
ELSE
    dwAlarms_Warning := dwAlarms_Warning AND 16#FFFFFF7F;
END_IF;

IF AI_Hopper_Tobacco_Level_pct < 25.000 THEN
    dwAlarms_Warning := dwAlarms_Warning OR 16#00000100; (* Bit 8: Tobacco Hopper Level Low *)
ELSE
    dwAlarms_Warning := dwAlarms_Warning AND 16#FFFFFEFF;
END_IF;

IF rDiag_Knife_Wear_Pct > 80.000 THEN
    dwAlarms_Warning := dwAlarms_Warning OR 16#00000200; (* Bit 9: Knife Blade Sharpness Degraded *)
ELSE
    dwAlarms_Warning := dwAlarms_Warning AND 16#FFFFFDFF;
END_IF;

(* 5. Evaluate Priority 3 Diagnostics Reg (dwAlarms_Diagnostic) *)
IF bDensity_Fault_A THEN dwAlarms_Diagnostic := dwAlarms_Diagnostic OR 16#00000001; END_IF;
IF bDensity_Fault_B THEN dwAlarms_Diagnostic := dwAlarms_Diagnostic OR 16#00000002; END_IF;
IF bDensity_Fault_C THEN dwAlarms_Diagnostic := dwAlarms_Diagnostic OR 16#00000004; END_IF;

IF bMoisture_Fault_A THEN dwAlarms_Diagnostic := dwAlarms_Diagnostic OR 16#00000008; END_IF;
IF bMoisture_Fault_B THEN dwAlarms_Diagnostic := dwAlarms_Diagnostic OR 16#00000010; END_IF;
IF bMoisture_Fault_C THEN dwAlarms_Diagnostic := dwAlarms_Diagnostic OR 16#00000020; END_IF;

IF bDiameter_Fault_A THEN dwAlarms_Diagnostic := dwAlarms_Diagnostic OR 16#00000040; END_IF;
IF bDiameter_Fault_B THEN dwAlarms_Diagnostic := dwAlarms_Diagnostic OR 16#00000080; END_IF;
IF bDiameter_Fault_C THEN dwAlarms_Diagnostic := dwAlarms_Diagnostic OR 16#00000100; END_IF;

IF bLineSpeed_Fault_A THEN dwAlarms_Diagnostic := dwAlarms_Diagnostic OR 16#00000200; END_IF;
IF bLineSpeed_Fault_B THEN dwAlarms_Diagnostic := dwAlarms_Diagnostic OR 16#00000400; END_IF;
IF bLineSpeed_Fault_C THEN dwAlarms_Diagnostic := dwAlarms_Diagnostic OR 16#00000800; END_IF;

IF bDrumVac_Fault_A THEN dwAlarms_Diagnostic := dwAlarms_Diagnostic OR 16#00001000; END_IF;
IF bDrumVac_Fault_B THEN dwAlarms_Diagnostic := dwAlarms_Diagnostic OR 16#00002000; END_IF;
IF bDrumVac_Fault_C THEN dwAlarms_Diagnostic := dwAlarms_Diagnostic OR 16#00004000; END_IF;
'''

def get_phase10_code():
    return '''
(* === PHASE 10: ACTUATOR OUTPUT CLAMPING, DIAGNOSTICS & SYSTEM TELEMETRY === *)

(* Safe Physical Limits Clamping on All Actuators *)
rCmd_Trimmer_Height_mm        := MAX(-3.000, MIN(3.000, rCmd_Trimmer_Height_mm));
rCmd_Garniture_Velocity_ms    := MAX(0.000, MIN(30.000, rCmd_Garniture_Velocity_ms));
rCmd_Knife_Phase_Advance_mrad := MAX(-0.200, MIN(0.200, rCmd_Knife_Phase_Advance_mrad));
rCmd_Knife_Angular_Speed_rads := MAX(0.000, MIN(1200.000, rCmd_Knife_Angular_Speed_rads));
rCmd_Laser_DutyCycle_pct      := MAX(0.000, MIN(100.000, rCmd_Laser_DutyCycle_pct));
rCmd_Laser_Pulse_Freq_Hz      := MAX(0.000, MIN(2000.000, rCmd_Laser_Pulse_Freq_Hz));
rCmd_Vacuum_Blower_VFD_Hz     := MAX(0.000, MIN(60.000, rCmd_Vacuum_Blower_VFD_Hz));
rCmd_Seam_Sealer_Power_pct    := MAX(0.000, MIN(100.000, rCmd_Seam_Sealer_Power_pct));

(* Override to Safe De-Energized State if Emergency State Active *)
IF iFSM_Internal_State = 11 THEN
    rCmd_Trimmer_Height_mm        := 0.000;
    rCmd_Garniture_Velocity_ms    := 0.000;
    rCmd_Knife_Phase_Advance_mrad := 0.000;
    rCmd_Knife_Angular_Speed_rads := 0.000;
    rCmd_Laser_DutyCycle_pct      := 0.000;
    rCmd_Laser_Pulse_Freq_Hz      := 0.000;
    rCmd_Vacuum_Blower_VFD_Hz     := 0.000;
    rCmd_Seam_Sealer_Power_pct    := 0.000;
    bCmd_Sharpening_Step_Pulse    := FALSE;
    bCmd_Splicer_Actuate          := FALSE;
    bSystem_Ready_20k             := FALSE;
END_IF;

END_FUNCTION_BLOCK
'''

def assemble_full_function_block():
    parts = [
        get_header_code(),
        get_var_input_code(),
        get_var_output_code(),
        get_var_internal_code(),
        get_phase0_code(),
        get_phase1_code(),
        get_phase2_code(),
        get_phase3_code(),
        get_phase4_code(),
        get_phase5_code(),
        get_phase6_code(),
        get_phase7_code(),
        get_phase8_code(),
        get_phase9_code(),
        get_phase10_code()
    ]
    return "".join(parts)

if __name__ == "__main__":
    code = assemble_full_function_block()
    print(f"Total Generated Function Block Length: {len(code)} characters")
    with open("temp_fb.st", "w", encoding="utf-8") as f:
        f.write(code)
    print("Saved to temp_fb.st")
