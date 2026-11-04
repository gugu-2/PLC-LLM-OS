# -*- coding: utf-8 -*-
"""
Module: phase3_mpc.py
Generates Phase 3: Receding-Horizon Model Predictive Control (MPC) & 8x8 Discrete State-Space.
Includes full matrix initialization, state vector extraction, forward prediction over Np=4,
analytical gradient descent optimization, actuator box-constraint projection, and command routing.
"""

def generate_phase3_mpc():
    s = []
    s.append("(* ================================================================================================= *)")
    s.append("(* PHASE 3: 8x8 DISCRETE STATE-SPACE & RECEDING-HORIZON MPC OPTIMIZATION                             *)")
    s.append("(* ================================================================================================= *)")
    s.append("")
    s.append("(* ------------------------------------------------------------------------------------------------- *)")
    s.append("(* 1. Deterministic State-Space Matrices & Cost Weights Initialization                               *)")
    s.append("(* ------------------------------------------------------------------------------------------------- *)")
    s.append("IF NOT b_Matrices_Initialized THEN")
    s.append("    (* Initialize A_sys (8x8) Discrete Transition Matrix - Stable Sampled Poles at Ts = 2 ms *)")
    
    # Generate explicit assignments for all 64 elements of A_sys
    a_diag = [0.988, 0.994, 0.994, 0.994, 0.991, 0.986, 0.982, 0.989]
    for i in range(1, 9):
        for j in range(1, 9):
            if i == j:
                val = a_diag[i-1]
            elif i == 2 and j == 1:
                val = -0.00012
            elif i == 3 and j == 2:
                val = 0.045
            elif i == 4 and j == 3:
                val = 0.042
            elif i == 6 and j == 5:
                val = -0.150
            elif i == 7 and j == 6:
                val = 0.082
            elif i == 8 and j == 6:
                val = 0.035
            elif i == 8 and j == 1:
                val = 0.021
            else:
                val = 0.000
            s.append(f"    A_sys[{i},{j}] := {val:.5f};")

    s.append("")
    s.append("    (* Initialize B_sys (8x8) Discrete Actuator Input Coupling Matrix *)")
    b_diag = [-12.400, 0.1432, 0.1432, 0.1432, 0.0035, 0.285, -0.450, 14.800]
    for i in range(1, 9):
        for j in range(1, 9):
            if i == j:
                val = b_diag[i-1]
            elif i == 2 and j == 1:
                val = -0.0150
            elif i == 3 and j == 1:
                val = -0.0120
            elif i == 4 and j == 1:
                val = -0.0100
            elif i == 7 and j == 6:
                val = 0.0950
            elif i == 8 and j == 6:
                val = -0.0400
            else:
                val = 0.0000
            s.append(f"    B_sys[{i},{j}] := {val:.4f};")

    s.append("")
    s.append("    (* Initialize C_sys (8x8) Direct Observation Matrix *)")
    for i in range(1, 9):
        for j in range(1, 9):
            val = 1.0 if i == j else 0.0
            s.append(f"    C_sys[{i},{j}] := {val:.1f};")

    s.append("")
    s.append("    (* Initialize D_sys (8x8) Direct Feedthrough Matrix *)")
    for i in range(1, 9):
        for j in range(1, 9):
            s.append(f"    D_sys[{i},{j}] := 0.0;")

    s.append("")
    s.append("    (* Initialize Q_weight (8x8) State Penalty Matrix *)")
    q_diag = [0.08, 2500.0, 2500.0, 2500.0, 45.0, 2.5, 85.0, 0.06]
    for i in range(1, 9):
        for j in range(1, 9):
            val = q_diag[i-1] if i == j else 0.0
            s.append(f"    Q_weight[{i},{j}] := {val:.2f};")

    s.append("")
    s.append("    (* Initialize R_weight (8x8) Control Effort Penalty Matrix *)")
    r_diag = [15.0, 40.0, 40.0, 40.0, 0.05, 0.10, 0.12, 12.0]
    for i in range(1, 9):
        for j in range(1, 9):
            val = r_diag[i-1] if i == j else 0.0
            s.append(f"    R_weight[{i},{j}] := {val:.2f};")

    s.append("")
    s.append("    (* Initialize S_rate_weight (8x8) Slew Rate Penalty Matrix *)")
    s_diag = [25.0, 80.0, 80.0, 80.0, 0.20, 0.50, 0.50, 20.0]
    for i in range(1, 9):
        for j in range(1, 9):
            val = s_diag[i-1] if i == j else 0.0
            s.append(f"    S_rate_weight[{i},{j}] := {val:.2f};")

    s.append("")
    s.append("    (* Initialize P_terminal_weight (8x8) Terminal Cost Matrix = 1.5 * Q *)")
    for i in range(1, 9):
        for j in range(1, 9):
            val = 1.5 * q_diag[i-1] if i == j else 0.0
            s.append(f"    P_terminal_weight[{i},{j}] := {val:.2f};")

    s.append("")
    s.append("    (* Initialize Actuator Constraints [u_min, u_max, delta_u_max] *)")
    umin = [-0.15, -0.050, -0.050, -0.050, -150.0, -30.0, -30.0, -0.15]
    umax = [0.15, 0.050, 0.050, 0.050, 150.0, 30.0, 30.0, 0.15]
    dumax = [0.010, 0.004, 0.004, 0.004, 15.0, 3.0, 3.0, 0.010]
    for i in range(1, 9):
        s.append(f"    u_actuator_min[{i}] := {umin[i-1]:.3f};")
        s.append(f"    u_actuator_max[{i}] := {umax[i-1]:.3f};")
        s.append(f"    delta_u_max_rate[{i}] := {dumax[i-1]:.3f};")
        s.append(f"    r_state_ref[{i}] := 0.0;")
        s.append(f"    u_prev_cycle[{i}] := 0.0;")

    s.append("")
    s.append("    b_Matrices_Initialized := TRUE;")
    s.append("END_IF;")
    s.append("")
    s.append("(* ------------------------------------------------------------------------------------------------- *)")
    s.append("(* 2. Current State Vector Assembly x_k [8x1]                                                        *)")
    s.append("(* ------------------------------------------------------------------------------------------------- *)")
    s.append("x_state[1] := r_Infeed_Tension_Voted - r_Infeed_Tension_SetPoint; (* Delta T_in [N] *)")
    s.append("x_state[2] := r_Cyan_Circ_Dev_Voted;                              (* Delta y_C [mm] *)")
    s.append("x_state[3] := r_Magenta_Circ_Dev_Voted;                           (* Delta y_M [mm] *)")
    s.append("x_state[4] := r_Yellow_Circ_Dev_Voted;                            (* Delta y_Y [mm] *)")
    s.append("x_state[5] := r_Web_Moisture_Percent - 5.0;                       (* Delta M_web [%] *)")
    s.append("x_state[6] := r_Web_Temperature_Dryer_Exit - (r_Dryer_Zone_Temp_SetPoint * 0.48); (* Delta T_web [C] *)")
    s.append("x_state[7] := r_Estimated_Flue_LEL_Percent - 18.0;                 (* Delta C_LEL [% LEL] *)")
    s.append("x_state[8] := r_Chill_Tension_Voted - r_Chill_Tension_SetPoint;   (* Delta T_chill [N] *)")
    s.append("")
    s.append("(* ------------------------------------------------------------------------------------------------- *)")
    s.append("(* 3. Receding-Horizon Projected Gradient Descent Optimization (Np = 4 Steps)                        *)")
    s.append("(* ------------------------------------------------------------------------------------------------- *)")
    s.append("(* Seed Candidate Control Horizon from previous solution *)")
    s.append("FOR p_idx := 1 TO 4 DO")
    s.append("    FOR j_idx := 1 TO 8 DO")
    s.append("        U_horizon[p_idx, j_idx] := u_prev_cycle[j_idx];")
    s.append("    END_FOR;")
    s.append("END_FOR;")
    s.append("")
    s.append("(* PGD Optimization Loop *)")
    s.append("FOR k_idx := 1 TO n_MPC_Max_Iterations DO")
    s.append("    (* Forward State Trajectory Prediction *)")
    s.append("    FOR p_idx := 1 TO 4 DO")
    s.append("        FOR i_idx := 1 TO 8 DO")
    s.append("            r_Sum_Accumulator := 0.0;")
    s.append("            FOR j_idx := 1 TO 8 DO")
    s.append("                IF p_idx = 1 THEN")
    s.append("                    r_Sum_Accumulator := r_Sum_Accumulator + (A_sys[i_idx, j_idx] * x_state[j_idx]);")
    s.append("                ELSE")
    s.append("                    r_Sum_Accumulator := r_Sum_Accumulator + (A_sys[i_idx, j_idx] * X_pred_trajectory[p_idx - 1, j_idx]);")
    s.append("                END_IF;")
    s.append("                r_Sum_Accumulator := r_Sum_Accumulator + (B_sys[i_idx, j_idx] * U_horizon[p_idx, j_idx]);")
    s.append("            END_FOR;")
    s.append("            X_pred_trajectory[p_idx, i_idx] := r_Sum_Accumulator;")
    s.append("        END_FOR;")
    s.append("    END_FOR;")
    s.append("")
    s.append("    (* Analytical Cost Gradient Calculation & Projected Update *)")
    s.append("    FOR p_idx := 1 TO 4 DO")
    s.append("        FOR j_idx := 1 TO 8 DO")
    s.append("            (* Tracking Error Gradient *)")
    s.append("            r_Sum_Accumulator := 0.0;")
    s.append("            FOR i_idx := 1 TO 8 DO")
    s.append("                IF p_idx < 4 THEN")
    s.append("                    r_Sum_Accumulator := r_Sum_Accumulator + (B_sys[i_idx, j_idx] * Q_weight[i_idx, i_idx] * (X_pred_trajectory[p_idx, i_idx] - r_state_ref[i_idx]));")
    s.append("                ELSE")
    s.append("                    r_Sum_Accumulator := r_Sum_Accumulator + (B_sys[i_idx, j_idx] * P_terminal_weight[i_idx, i_idx] * (X_pred_trajectory[p_idx, i_idx] - r_state_ref[i_idx]));")
    s.append("                END_IF;")
    s.append("            END_FOR;")
    s.append("            (* Control Effort & Rate Penalty Gradients *)")
    s.append("            r_Sum_Accumulator := r_Sum_Accumulator + (R_weight[j_idx, j_idx] * U_horizon[p_idx, j_idx]);")
    s.append("            IF p_idx = 1 THEN")
    s.append("                r_Sum_Accumulator := r_Sum_Accumulator + (S_rate_weight[j_idx, j_idx] * (U_horizon[1, j_idx] - u_prev_cycle[j_idx]));")
    s.append("            ELSE")
    s.append("                r_Sum_Accumulator := r_Sum_Accumulator + (S_rate_weight[j_idx, j_idx] * (U_horizon[p_idx, j_idx] - U_horizon[p_idx - 1, j_idx]));")
    s.append("            END_IF;")
    s.append("            Grad_Cost_U[p_idx, j_idx] := r_Sum_Accumulator;")
    s.append("")
    s.append("            (* Gradient Descent Step *)")
    s.append("            U_horizon[p_idx, j_idx] := U_horizon[p_idx, j_idx] - (r_MPC_Learning_Rate * Grad_Cost_U[p_idx, j_idx]);")
    s.append("")
    s.append("            (* Actuator Box Constraints & Slew Rate Limiting *)")
    s.append("            IF p_idx = 1 THEN")
    s.append("                r_Delta_Scratch := U_horizon[1, j_idx] - u_prev_cycle[j_idx];")
    s.append("                IF r_Delta_Scratch > delta_u_max_rate[j_idx] THEN")
    s.append("                    U_horizon[1, j_idx] := u_prev_cycle[j_idx] + delta_u_max_rate[j_idx];")
    s.append("                ELSIF r_Delta_Scratch < -delta_u_max_rate[j_idx] THEN")
    s.append("                    U_horizon[1, j_idx] := u_prev_cycle[j_idx] - delta_u_max_rate[j_idx];")
    s.append("                END_IF;")
    s.append("            END_IF;")
    s.append("            IF U_horizon[p_idx, j_idx] > u_actuator_max[j_idx] THEN")
    s.append("                U_horizon[p_idx, j_idx] := u_actuator_max[j_idx];")
    s.append("            ELSIF U_horizon[p_idx, j_idx] < u_actuator_min[j_idx] THEN")
    s.append("                U_horizon[p_idx, j_idx] := u_actuator_min[j_idx];")
    s.append("            END_IF;")
    s.append("        END_FOR;")
    s.append("    END_FOR;")
    s.append("END_FOR;")
    s.append("")
    s.append("(* ------------------------------------------------------------------------------------------------- *)")
    s.append("(* 4. Extract First Control Horizon Vector u*(k) & Apply Actuation                                   *)")
    s.append("(* ------------------------------------------------------------------------------------------------- *)")
    s.append("FOR j_idx := 1 TO 8 DO")
    s.append("    u_control[j_idx] := U_horizon[1, j_idx];")
    s.append("    u_prev_cycle[j_idx] := u_control[j_idx];")
    s.append("END_FOR;")
    s.append("")
    s.append("(* Route MPC Control Outputs to Industrial Physical Actuators *)")
    s.append("r_Infeed_Nip_Speed_Trim_Cmd       := u_control[1];")
    s.append("r_Cyan_Circ_Phase_Trim_Cmd        := u_control[2];")
    s.append("r_Magenta_Circ_Phase_Trim_Cmd     := u_control[3];")
    s.append("r_Yellow_Circ_Phase_Trim_Cmd      := u_control[4];")
    s.append("r_Cyan_Dampening_Brush_Speed_Cmd  := LIMIT(350.0, 650.0 + u_control[5], 1150.0);")
    s.append("r_Dryer_Zone2_Gas_Valve_Cmd       := LIMIT(0.0, 55.0 + u_control[6], 100.0);")
    s.append("r_Dryer_Zone3_Gas_Valve_Cmd       := LIMIT(0.0, 58.0 + u_control[6], 100.0);")
    s.append("r_Dryer_Recirc_Damper_Pos_Cmd     := LIMIT(10.0, 65.0 - u_control[7], 85.0);")
    s.append("r_Chill_Roll_Master_Speed_Trim    := u_control[8];")
    s.append("")
    s.append("(* Calculate Cumulative MPC Tracking Cost Value *)")
    s.append("r_MPC_Cumulative_Cost_Val := 0.0;")
    s.append("FOR p_idx := 1 TO 4 DO")
    s.append("    FOR i_idx := 1 TO 8 DO")
    s.append("        r_MPC_Cumulative_Cost_Val := r_MPC_Cumulative_Cost_Val + (Q_weight[i_idx, i_idx] * (X_pred_trajectory[p_idx, i_idx] * X_pred_trajectory[p_idx, i_idx]));")
    s.append("    END_FOR;")
    s.append("END_FOR;")
    s.append("")
    s.append("(* One-Step Ahead State Estimation *)")
    s.append("FOR i_idx := 1 TO 8 DO")
    s.append("    r_Sum_Accumulator := 0.0;")
    s.append("    FOR j_idx := 1 TO 8 DO")
    s.append("        r_Sum_Accumulator := r_Sum_Accumulator + (A_sys[i_idx, j_idx] * x_state[j_idx]) + (B_sys[i_idx, j_idx] * u_control[j_idx]);")
    s.append("    END_FOR;")
    s.append("    x_state_next[i_idx] := r_Sum_Accumulator;")
    s.append("END_FOR;")
    s.append("")

    return "\n".join(s)
