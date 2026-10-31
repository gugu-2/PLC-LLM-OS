# st_matrices_init.py
# Generates the complete unrolled discrete state-space matrices A, B, C, D, L, Q, R, P, K

def get_matrices_init():
    lines = []
    lines.append("(* ========================================================================================================== *)")
    lines.append("(* STATE-SPACE MODEL & CONTROL MATRICES INITIALIZATION (Ts = 0.5 ms)                                          *)")
    lines.append("(* ========================================================================================================== *)")
    lines.append("IF NOT b_MatricesInitialized THEN")

    # A Matrix: 16x16
    lines.append("    (* Matrix A (16x16): Discrete State Transition Matrix *)")
    # Base physics values for each diagonal and cross-couplings
    a_vals = [[0.0 for _ in range(16)] for _ in range(16)]
    # Diagonal self-retention
    for i in range(16):
        a_vals[i][i] = 0.9850 - (i % 5) * 0.015

    # Known cyber-physical interactions
    a_vals[0][0] = 1.0000;  a_vals[0][1] = 0.00050; a_vals[0][2] = 0.000018; a_vals[0][3] = -0.00005;
    a_vals[1][1] = 0.9820;  a_vals[1][2] = 0.04250; a_vals[1][3] = -0.00850; a_vals[1][4] = -0.00120;
    a_vals[2][1] = -0.0032; a_vals[2][2] = 0.81500; a_vals[2][3] = 0.00015;
    a_vals[3][0] = 0.00025; a_vals[3][3] = 0.92500; a_vals[3][4] = -0.00015;
    a_vals[4][1] = 0.08500; a_vals[4][3] = 42.5000; a_vals[4][4] = 0.88500;
    a_vals[5][5] = 0.94500; a_vals[5][6] = 0.00048; a_vals[5][7] = -0.00250;
    a_vals[6][5] = -185.00; a_vals[6][6] = 0.91200; a_vals[6][7] = 0.01500;
    a_vals[7][5] = 0.01250; a_vals[7][7] = 0.96500; a_vals[7][8] = -0.00850; a_vals[7][9] = 0.01250;
    a_vals[8][6] = 0.00850; a_vals[8][7] = 0.00620; a_vals[8][8] = 0.95800;
    a_vals[9][6] = 0.08500; a_vals[9][9] = 0.78500; a_vals[9][11] = 0.00450;
    a_vals[10][10] = 1.000; a_vals[10][11] = 0.00245; a_vals[10][9] = 0.00018;
    a_vals[11][9] = 0.03850; a_vals[11][11] = 0.97800; a_vals[11][12] = 0.00120;
    a_vals[12][12] = 0.9995;
    a_vals[13][4] = 0.00018; a_vals[13][13] = 1.0000; a_vals[13][11] = 0.00005;
    a_vals[14][0] = 0.000035; a_vals[14][14] = 0.9950;
    a_vals[15][1] = 0.00850; a_vals[15][15] = 0.9650;

    for r in range(16):
        for c in range(16):
            val = a_vals[r][c]
            lines.append(f"    A_Matrix[{r+1}, {c+1}] := {val:.6f};")

    # B Matrix: 16x8
    lines.append("")
    lines.append("    (* Matrix B (16x8): Discrete Input Coupling Matrix *)")
    b_vals = [[0.0 for _ in range(8)] for _ in range(16)]
    b_vals[0][0] = 0.000012;
    b_vals[1][0] = 0.038500;
    b_vals[2][0] = 0.185000;
    b_vals[4][0] = 0.012500; b_vals[4][4] = 0.005500;
    b_vals[5][1] = 0.045000; b_vals[5][2] = 0.001200;
    b_vals[6][1] = 1.850000; b_vals[6][2] = 0.085000;
    b_vals[7][1] = 0.015000; b_vals[7][2] = 0.008500;
    b_vals[8][1] = 0.008500; b_vals[8][2] = 0.012000;
    b_vals[9][1] = 0.125000;
    b_vals[10][1] = 0.000450; b_vals[10][3] = 0.000120;
    b_vals[11][1] = 0.025000; b_vals[11][5] = 0.001500; b_vals[11][6] = 0.001200; b_vals[11][7] = 0.001000;
    b_vals[12][5] = 0.002800; b_vals[12][6] = 0.002500; b_vals[12][7] = 0.002200;
    b_vals[13][0] = 0.000085; b_vals[13][1] = 0.000150;
    b_vals[14][4] = 0.000250;
    b_vals[15][4] = 0.045000;

    for r in range(16):
        for c in range(8):
            val = b_vals[r][c]
            lines.append(f"    B_Matrix[{r+1}, {c+1}] := {val:.6f};")

    # C Matrix: 8x16
    lines.append("")
    lines.append("    (* Matrix C (8x16): Output Observation Matrix *)")
    c_vals = [[0.0 for _ in range(16)] for _ in range(8)]
    c_vals[0][0] = 1.000000 # y1: Z encoder pos
    c_vals[1][4] = 1.000000 # y2: Bond force
    c_vals[2][6] = 0.450000; c_vals[2][7] = 0.025000 # y3: Ultrasonic electrical power
    c_vals[3][8] = 0.850000 # y4: Ultrasonic phase angle
    c_vals[4][10] = 0.015000 # y5: Free Air Ball diameter
    c_vals[5][13] = 1.000000 # y6: Ball deformation
    c_vals[6][11] = 1.000000; c_vals[6][12] = 0.050000 # y7: Workholder temp
    c_vals[7][15] = 1.000000 # y8: Wire spool tension

    for r in range(8):
        for c in range(16):
            val = c_vals[r][c]
            lines.append(f"    C_Matrix[{r+1}, {c+1}] := {val:.6f};")

    # D Matrix: 8x8
    lines.append("")
    lines.append("    (* Matrix D (8x8): Direct Feedthrough Matrix *)")
    for r in range(8):
        for c in range(8):
            val = 0.000000
            if r == 2 and c == 1:
                val = 0.025000
            lines.append(f"    D_Matrix[{r+1}, {c+1}] := {val:.6f};")

    # L Observer Gain Matrix: 16x8
    lines.append("")
    lines.append("    (* Matrix L (16x8): Luenberger Innovation Observer Gain Matrix *)")
    l_vals = [[0.0 for _ in range(8)] for _ in range(16)]
    l_vals[0][0] = 0.285000;
    l_vals[1][0] = 0.125000;
    l_vals[2][0] = 0.045000;
    l_vals[3][0] = 0.015000; l_vals[3][1] = 0.005500;
    l_vals[4][1] = 0.320000;
    l_vals[5][2] = 0.185000;
    l_vals[6][2] = 0.450000;
    l_vals[7][2] = 0.085000; l_vals[7][3] = 0.045000;
    l_vals[8][3] = 0.250000;
    l_vals[9][2] = 0.065000;
    l_vals[10][4] = 0.150000;
    l_vals[11][6] = 0.220000;
    l_vals[12][6] = 0.085000;
    l_vals[13][5] = 0.350000;
    l_vals[14][0] = 0.008500;
    l_vals[15][7] = 0.280000;

    for r in range(16):
        for c in range(8):
            val = l_vals[r][c]
            lines.append(f"    L_Gain[{r+1}, {c+1}] := {val:.6f};")

    # MPC Weights Q, R, P, S
    lines.append("")
    lines.append("    (* MPC Objective Function Quadratic Weights *)")
    q_weights = [15.0, 25.0, 8.0, 5.0, 20.0, 12.0, 18.0, 6.0]
    r_weights = [0.08, 0.05, 0.12, 0.02, 0.04, 0.01, 0.01, 0.01]
    p_weights = [35.0, 50.0, 15.0, 10.0, 45.0, 25.0, 30.0, 12.0]
    s_weights = [0.15, 0.10, 0.20, 0.05, 0.08, 0.02, 0.02, 0.02]

    for k in range(8):
        lines.append(f"    Q_Weight[{k+1}] := {q_weights[k]:.4f};")
        lines.append(f"    R_Weight[{k+1}] := {r_weights[k]:.4f};")
        lines.append(f"    P_Weight[{k+1}] := {p_weights[k]:.4f};")
        lines.append(f"    S_RateWeight[{k+1}] := {s_weights[k]:.4f};")

    # Thermal Decoupling Matrix K_ThermalCrossCoupling (3x3)
    lines.append("")
    lines.append("    (* Workholder Multi-Zone Thermal Decoupling Matrix *)")
    lines.append("    K_ThermalCrossCoupling[1, 1] := 1.000000; K_ThermalCrossCoupling[1, 2] := -0.185000; K_ThermalCrossCoupling[1, 3] := -0.045000;")
    lines.append("    K_ThermalCrossCoupling[2, 1] := -0.165000; K_ThermalCrossCoupling[2, 2] := 1.000000; K_ThermalCrossCoupling[2, 3] := -0.165000;")
    lines.append("    K_ThermalCrossCoupling[3, 1] := -0.045000; K_ThermalCrossCoupling[3, 2] := -0.185000; K_ThermalCrossCoupling[3, 3] := 1.000000;")

    # State vectors zero initialization
    lines.append("")
    lines.append("    FOR i_Idx := 1 TO 16 DO")
    lines.append("        x_State[i_Idx] := 0.0;")
    lines.append("        x_Pred[i_Idx] := 0.0;")
    lines.append("    END_FOR;")
    lines.append("")
    lines.append("    FOR i_Idx := 1 TO 8 DO")
    lines.append("        u_Input[i_Idx] := 0.0;")
    lines.append("        y_Output[i_Idx] := 0.0;")
    lines.append("        y_Model[i_Idx] := 0.0;")
    lines.append("        e_Innov[i_Idx] := 0.0;")
    lines.append("        u_MPC_Optimal[i_Idx] := 0.0;")
    lines.append("        u_MPC_Previous[i_Idx] := 0.0;")
    lines.append("        delta_u_Cmd[i_Idx] := 0.0;")
    lines.append("    END_FOR;")
    lines.append("")
    lines.append("    b_MatricesInitialized := TRUE;")
    lines.append("END_IF;")
    lines.append("")
    return "\n".join(lines)
