# -*- coding: utf-8 -*-
"""
Generator for Phase 0: Discrete State-Space Matrices & MPC Weights Initialization
"""

def generate_matrices_st():
    lines = []
    lines.append("(* ==================================================================================================================== *)")
    lines.append("(* PHASE 0: ONE-TIME DETERMINISTIC INITIALIZATION OF DISCRETE STATE-SPACE MATRICES & MPC WEIGHTS                         *)")
    lines.append("(* ==================================================================================================================== *)")
    lines.append("IF NOT bMatricesInitialized THEN")
    
    # 16x16 A Matrix
    lines.append("    (* --- 16x16 Discrete State Transition Matrix A (Sample Time Ts = 0.050 s) --- *)")
    
    # Let's create realistic thermodynamic matrix values
    # A[16, 16]
    A_matrix = [[0.0 for _ in range(16)] for _ in range(16)]
    
    # State dynamics:
    # 1. Tank P: stable storage with coupling to manifold pressure and boiloff
    A_matrix[0][0] = 0.9982; A_matrix[0][1] = 0.0015; A_matrix[0][2] = 0.00042
    # 2. Manifold P: fast equilibrium with tank and compressor suction
    A_matrix[1][0] = 0.0028; A_matrix[1][1] = 0.9850; A_matrix[1][2] = 0.00085; A_matrix[1][4] = -0.0035; A_matrix[1][7] = 0.0012
    # 3. BOG Rate: slow thermal ingress decay
    A_matrix[2][2] = 0.9995; A_matrix[2][0] = -0.00015
    # 4. T_suct: suction temperature thermal inertia
    A_matrix[3][3] = 0.9920; A_matrix[3][1] = 0.0008; A_matrix[3][6] = 0.0045 # heating from recycle
    # 5. P_d1: compressor stage 1 disch press
    A_matrix[4][1] = 0.1250; A_matrix[4][4] = 0.9420; A_matrix[4][5] = -0.0025; A_matrix[4][6] = 0.0018
    # 6. m_c2: compressor stage 2 mass flow
    A_matrix[5][1] = 0.8500; A_matrix[5][4] = 0.1450; A_matrix[5][5] = 0.9350; A_matrix[5][6] = -0.4200
    # 7. m_as: anti-surge recycle flow
    A_matrix[6][4] = 0.0850; A_matrix[6][6] = 0.9100; A_matrix[6][7] = -0.1500
    # 8. SurgeIdx: surge proximity
    A_matrix[7][5] = -0.00045; A_matrix[7][4] = 0.0012; A_matrix[7][7] = 0.9550; A_matrix[7][6] = -0.0018
    # 9. P_rc: Recondenser pressure
    A_matrix[8][5] = 0.00065; A_matrix[8][8] = 0.9780; A_matrix[8][9] = -0.0022; A_matrix[8][10] = -0.00052
    # 10. L_rc: Recondenser sump level
    A_matrix[9][8] = 0.0085; A_matrix[9][9] = 0.9960; A_matrix[9][10] = 0.0125; A_matrix[9][11] = -0.0048
    # 11. m_spray: spray mass flow dynamics
    A_matrix[10][10] = 0.9250; A_matrix[10][8] = -0.0015; A_matrix[10][9] = 0.0005
    # 12. P_hp: HP pump discharge pressure
    A_matrix[11][9] = 0.0450; A_matrix[11][11] = 0.9650; A_matrix[11][13] = -0.0250
    # 13. T_fg: PCHE gas delivery temp
    A_matrix[12][11] = -0.0015; A_matrix[12][12] = 0.9750; A_matrix[12][13] = -0.0025
    # 14. P_me: ME-GI 300 bar fuel header pressure
    A_matrix[13][11] = 0.0380; A_matrix[13][13] = 0.9820; A_matrix[13][14] = 0.0085
    # 15. m_acc: accumulator buffer mass
    A_matrix[14][13] = 0.1250; A_matrix[14][14] = 0.9975
    # 16. Q_gcu: GCU thermal influx
    A_matrix[15][1] = 0.0450; A_matrix[15][8] = 0.0250; A_matrix[15][15] = 0.9400
    
    for row in range(16):
        row_str = "    "
        for col in range(16):
            val = A_matrix[row][col]
            row_str += f"A[{row+1}, {col+1}] := {val:.6f}; "
            if (col + 1) % 4 == 0 and col != 15:
                lines.append(row_str)
                row_str = "    "
        lines.append(row_str)
        
    lines.append("")
    lines.append("    (* --- 16x8 Input Actuator Coupling Matrix B --- *)")
    B_matrix = [[0.0 for _ in range(8)] for _ in range(16)]
    # Inputs:
    # 1: IGV%, 2: ASV%, 3: Spray%, 4: HPPump_rpm, 5: MEGI_PCV%, 6: Glycol%, 7: GCU%, 8: SuctThrot%
    # x1 (Tank P):
    B_matrix[0][7] = -0.0028 # SuctThrot reduces tank dome pressure
    # x2 (Manifold P):
    B_matrix[1][0] = -0.0150 # IGV increases suction draw
    B_matrix[1][1] = 0.0085  # ASV recirculates gas to suction
    B_matrix[1][7] = 0.0220  # SuctThrot opens manifold
    # x3 (BOG rate):
    B_matrix[2][7] = -0.0005
    # x4 (T_suct):
    B_matrix[3][1] = 0.0450  # ASV brings hotter gas from discharge
    # x5 (P_d1):
    B_matrix[4][0] = 0.0380  # IGV boosts stage 1 discharge
    B_matrix[4][1] = -0.0180 # ASV drops pressure
    # x6 (m_c2):
    B_matrix[5][0] = 45.000  # IGV increases compressor throughput [kg/h]
    B_matrix[5][1] = -35.000 # ASV diverts flow
    # x7 (m_as):
    B_matrix[6][1] = 55.000  # ASV stroke directly increases recycle flow [kg/h]
    # x8 (SurgeIdx):
    B_matrix[7][0] = 0.0025  # IGV affects surge line
    B_matrix[7][1] = -0.0085 # ASV moves away from surge line!
    # x9 (P_rc):
    B_matrix[8][0] = 0.0125  # IGV increases vapor flow into recondenser
    B_matrix[8][2] = -0.0280 # Spray condenses vapor rapidly reducing P_rc!
    # x10 (L_rc):
    B_matrix[9][2] = 0.0450  # Spray adds liquid to sump
    B_matrix[9][3] = -0.0320 # HP Pump draws liquid from sump
    # x11 (m_spray):
    B_matrix[10][2] = 38.500 # Spray valve directly opens liquid flow [kg/h]
    # x12 (P_hp):
    B_matrix[11][3] = 0.0850 # HP pump rpm increases discharge pressure [bar]
    B_matrix[11][4] = -0.0420# ME-GI PCV opening causes pressure drop
    # x13 (T_fg):
    B_matrix[12][5] = 0.4500 # Glycol valve raises gas delivery temp [deg C]
    # x14 (P_me):
    B_matrix[13][3] = 0.0650 # HP pump rpm delivers pressure
    B_matrix[13][4] = 0.0950 # ME-GI PCV controls header pressure
    # x15 (m_acc):
    B_matrix[14][4] = 0.0850 # PCV stroke increases mass packing in bottle
    # x16 (Q_gcu):
    B_matrix[15][6] = 85.000 # GCU valve feeds thermal oxidizer [kW]

    for row in range(16):
        row_str = "    "
        for col in range(8):
            val = B_matrix[row][col]
            row_str += f"B[{row+1}, {col+1}] := {val:.6f}; "
            if (col + 1) % 4 == 0 and col != 7:
                lines.append(row_str)
                row_str = "    "
        lines.append(row_str)
        
    lines.append("")
    lines.append("    (* --- 8x16 Output Measurement Observation Matrix C --- *)")
    # Outputs:
    # 1: P_tank (mbar), 2: P_cd (bar), 3: SurgeMargin (%), 4: L_rc (%), 5: P_rc (bar), 6: P_me (bar), 7: T_me (deg C), 8: Q_gcu (kW)
    C_matrix = [[0.0 for _ in range(16)] for _ in range(8)]
    C_matrix[0][0] = 1.0000; C_matrix[0][1] = 0.0500 # P_tank from x1, x2
    C_matrix[1][4] = 0.4500; C_matrix[1][5] = 0.00025 # P_cd from x5, x6
    C_matrix[2][7] = -100.00; C_matrix[2][5] = 0.0150 # SurgeMargin from x8, x6
    C_matrix[3][9] = 1.0000 # L_rc from x10
    C_matrix[4][8] = 1.0000 # P_rc from x9
    C_matrix[5][13] = 1.0000; C_matrix[5][11] = 0.0500 # P_me from x14, x12
    C_matrix[6][12] = 1.0000 # T_me from x13
    C_matrix[7][15] = 1.0000 # Q_gcu from x16

    for row in range(8):
        row_str = "    "
        for col in range(16):
            val = C_matrix[row][col]
            row_str += f"C[{row+1}, {col+1}] := {val:.6f}; "
            if (col + 1) % 4 == 0 and col != 15:
                lines.append(row_str)
                row_str = "    "
        lines.append(row_str)

    lines.append("")
    lines.append("    (* --- 8x8 Direct Feedforward Actuator Matrix D --- *)")
    D_matrix = [[0.0 for _ in range(8)] for _ in range(8)]
    # Slight direct feedforward coupling:
    D_matrix[1][0] = 0.0050 # IGV to discharge pressure
    D_matrix[2][1] = 0.1250 # ASV directly improves surge margin
    D_matrix[3][2] = 0.0080 # Spray directly affects column level
    D_matrix[4][2] = -0.0120# Spray directly cools column pressure
    D_matrix[5][4] = 0.0250 # Master PCV stroke to header pressure
    D_matrix[6][5] = 0.0150 # Glycol valve to exit temperature
    D_matrix[7][6] = 0.5000 # GCU valve to burner heat release
    
    for row in range(8):
        row_str = "    "
        for col in range(8):
            val = D_matrix[row][col]
            row_str += f"D[{row+1}, {col+1}] := {val:.6f}; "
            if (col + 1) % 4 == 0 and col != 7:
                lines.append(row_str)
                row_str = "    "
        lines.append(row_str)
        
    lines.append("")
    lines.append("    (* --- Receding-Horizon MPC Quadratic Weight Penalties --- *)")
    lines.append("    Q[1] := 12.50; (* Cargo Tank Vapor Pressure Penalty (Maintain ~1040 mbar) *)")
    lines.append("    Q[2] := 5.80;  (* Compressor Final Discharge Pressure Penalty *)")
    lines.append("    Q[3] := 25.00; (* Compressor Anti-Surge Margin Penalty (Keep > 15%) *)")
    lines.append("    Q[4] := 18.00; (* Recondenser Sump Level Penalty (Maintain ~50%) *)")
    lines.append("    Q[5] := 14.50; (* Recondenser Column Pressure Penalty (Maintain ~5.5 bar) *)")
    lines.append("    Q[6] := 85.00; (* ME-GI 300 Bar Fuel Header Pressure Penalty (STRICT 300 +/- 2.5 bar!) *)")
    lines.append("    Q[7] := 16.00; (* Fuel Gas Delivery Temperature Penalty (Target 45.0 deg C) *)")
    lines.append("    Q[8] := 8.50;  (* GCU Flaring Minimization Penalty (Zero Vent Policy) *)")
    lines.append("")
    lines.append("    (* --- Actuator Slew Rate Movement Penalty Matrix R --- *)")
    lines.append("    R[1] := 0.45; (* IGV Guide Vanes Slew Penalty *)")
    lines.append("    R[2] := 0.20; (* Anti-Surge Valve Fast Opening Penalty *)")
    lines.append("    R[3] := 0.35; (* Subcooled Spray Regulating Valve Penalty *)")
    lines.append("    R[4] := 0.55; (* HP Cryogenic Pump VFD Speed Slew Penalty *)")
    lines.append("    R[5] := 0.30; (* ME-GI Master PCV Modulating Penalty *)")
    lines.append("    R[6] := 0.25; (* PCHE Glycol Heating Valve Penalty *)")
    lines.append("    R[7] := 0.85; (* GCU Venting Peaking Valve Slew Penalty *)")
    lines.append("    R[8] := 0.40; (* Tank Suction Throttle Valve Penalty *)")
    lines.append("")
    lines.append("    (* --- MPC Terminal State Penalty Vector P_term --- *)")
    lines.append("    P_term[1] := 45.00;")
    lines.append("    P_term[2] := 18.50;")
    lines.append("    P_term[3] := 95.00;")
    lines.append("    P_term[4] := 55.00;")
    lines.append("    P_term[5] := 42.00;")
    lines.append("    P_term[6] := 250.00; (* Super-Heavy Terminal Weight on 300 Bar Delivery *) ")
    lines.append("    P_term[7] := 48.00;")
    lines.append("    P_term[8] := 28.00;")
    lines.append("")
    lines.append("    (* --- Actuator Hard Physical Limits [u_min, u_max] & Slew Limits du_max --- *)")
    lines.append("    u_min[1] := 0.0;   u_max[1] := 100.0; du_max[1] := 4.5;  (* IGV Angle [%] *)")
    lines.append("    u_min[2] := 0.0;   u_max[2] := 100.0; du_max[2] := 25.0; (* Anti-Surge Valve [%] (Fast Opening) *) ")
    lines.append("    u_min[3] := 0.0;   u_max[3] := 100.0; du_max[3] := 8.0;  (* Spray Valve [%] *)")
    lines.append("    u_min[4] := 0.0;   u_max[4] := 100.0; du_max[4] := 5.0;  (* HP Pump VFD [%] *)")
    lines.append("    u_min[5] := 0.0;   u_max[5] := 100.0; du_max[5] := 12.0; (* ME-GI PCV [%] *)")
    lines.append("    u_min[6] := 0.0;   u_max[6] := 100.0; du_max[6] := 6.0;  (* Glycol Valve [%] *)")
    lines.append("    u_min[7] := 0.0;   u_max[7] := 100.0; du_max[7] := 15.0; (* GCU Vent [%] *)")
    lines.append("    u_min[8] := 0.0;   u_max[8] := 100.0; du_max[8] := 5.0;  (* Tank Suction Throttle [%] *)")
    lines.append("")
    lines.append("    bMatricesInitialized := TRUE;")
    lines.append("END_IF;")
    return "\n".join(lines)

print("Part 2 matrices code generator written.")
