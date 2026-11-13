# parts_phase0.py
# Generates Phase 0: One-shot initialization of all discrete state-space and MPC matrices

def get_phase0_code():
    lines = []
    lines.append("(* ====================================================================================================")
    lines.append("   PHASE 0: ONE-SHOT FIRST-SCAN SYSTEM INITIALIZATION & CYBER-PHYSICAL MATRIX ALLOCATION")
    lines.append("   ==================================================================================================== *)")
    lines.append("IF NOT bFirstScanDone THEN")
    lines.append("    (* ------------------------------------------------------------------------------------------------")
    lines.append("       DISCRETE STATE TRANSITION MATRIX A [18x18] (Ts = 1.0 ms)")
    lines.append("       Rigid Body 6-DOF Double Integrator Kinematics + 3 Structural Modal Resonators (450, 820, 1250 Hz)")
    lines.append("       ------------------------------------------------------------------------------------------------ *)")
    
    # Generate A matrix assignments (18 x 18 = 324 elements)
    # Default is 0.0 except kinematics and resonators
    for row in range(1, 19):
        for col in range(1, 19):
            val = 0.0
            # Rigid body diagonal: pos to pos = 1.0, vel to vel = 1.0
            if row == col and row <= 12:
                val = 1.0
            # Kinematic coupling: pos to vel = Ts (0.001 s)
            elif row <= 6 and col == row + 6:
                val = 0.001
            # Resonator 1: 450 Hz (omega1 = 2827.4 rad/s, zeta1 = 0.012)
            elif row == 13 and col == 13:
                val = 0.996005
            elif row == 13 and col == 14:
                val = 0.000998
            elif row == 14 and col == 13:
                val = -7.994320
            elif row == 14 and col == 14:
                val = 0.994012
            # Resonator 2: 820 Hz (omega2 = 5152.2 rad/s, zeta2 = 0.015)
            elif row == 15 and col == 15:
                val = 0.986842
            elif row == 15 and col == 16:
                val = 0.000994
            elif row == 16 and col == 15:
                val = -26.54512
            elif row == 16 and col == 16:
                val = 0.983210
            # Resonator 3: 1250 Hz (omega3 = 7854.0 rad/s, zeta3 = 0.018)
            elif row == 17 and col == 17:
                val = 0.969315
            elif row == 17 and col == 18:
                val = 0.000985
            elif row == 18 and col == 17:
                val = -61.68502
            elif row == 18 and col == 18:
                val = 0.963420
            lines.append(f"    aMatA[{row}, {col}] := {val:.6f};")

    lines.append("")
    lines.append("    (* ------------------------------------------------------------------------------------------------")
    lines.append("       DISCRETE INPUT DISTRIBUTION MATRIX B [18x6]")
    lines.append("       Inputs: [Fx (N), Fy (N), Fz (N), Tx (N*m), Ty (N*m), Tz (N*m)]")
    lines.append("       ------------------------------------------------------------------------------------------------ *)")
    # Generate B matrix assignments (18 x 6 = 108 elements)
    # Mass = 32.5 kg -> 1/M = 0.030769, Ts/M = 3.076923e-5
    # Inertias: Ixx = 0.42 -> Ts/Ixx = 2.380952e-3, Iyy = 0.45 -> Ts/Iyy = 2.222222e-3, Izz = 0.85 -> Ts/Izz = 1.176471e-3
    for row in range(1, 19):
        for col in range(1, 7):
            val = 0.0
            # Position second-order feedthrough (0.5 * Ts^2 / M)
            if row == 1 and col == 1:
                val = 1.538462e-8
            elif row == 2 and col == 2:
                val = 1.538462e-8
            elif row == 3 and col == 3:
                val = 1.538462e-8
            elif row == 4 and col == 4:
                val = 1.190476e-6
            elif row == 5 and col == 5:
                val = 1.111111e-6
            elif row == 6 and col == 6:
                val = 5.882353e-7
            # Velocity first-order response (Ts / M or Ts / I)
            elif row == 7 and col == 1:
                val = 3.076923e-5
            elif row == 8 and col == 2:
                val = 3.076923e-5
            elif row == 9 and col == 3:
                val = 3.076923e-5
            elif row == 10 and col == 4:
                val = 2.380952e-3
            elif row == 11 and col == 5:
                val = 2.222222e-3
            elif row == 12 and col == 6:
                val = 1.176471e-3
            # Modal excitation gains
            elif row == 14 and col == 1:
                val = 0.000125
            elif row == 14 and col == 5:
                val = 0.000342
            elif row == 16 and col == 2:
                val = 0.000118
            elif row == 16 and col == 4:
                val = 0.000295
            elif row == 18 and col == 3:
                val = 0.000085
            elif row == 18 and col == 6:
                val = 0.000160
            lines.append(f"    aMatB[{row}, {col}] := {val:.8f};")

    lines.append("")
    lines.append("    (* ------------------------------------------------------------------------------------------------")
    lines.append("       DISCRETE MEASUREMENT OUTPUT MATRIX C [6x18]")
    lines.append("       Outputs: [X (m), Y (m), Z (m), Rx (rad), Ry (rad), Rz (rad)]")
    lines.append("       Couples rigid body kinematics and optical mirror block modal flexures")
    lines.append("       ------------------------------------------------------------------------------------------------ *)")
    # Generate C matrix assignments (6 x 18 = 108 elements)
    for row in range(1, 7):
        for col in range(1, 19):
            val = 0.0
            if row == col:
                val = 1.0 # Direct rigid body position coupling
            elif row == 1 and col == 13:
                val = 0.015200 # Mode 1 flexure into X interferometer
            elif row == 2 and col == 15:
                val = 0.012400 # Mode 2 flexure into Y interferometer
            elif row == 3 and col == 17:
                val = 0.008900 # Mode 3 flexure into Z capacitive gap
            elif row == 4 and col == 15:
                val = 0.003500 # Mode 2 flexure into Rx tilt
            elif row == 5 and col == 13:
                val = 0.004100 # Mode 1 flexure into Ry tilt
            lines.append(f"    aMatC[{row}, {col}] := {val:.6f};")

    lines.append("")
    lines.append("    (* ------------------------------------------------------------------------------------------------")
    lines.append("       DIRECT FEEDTHROUGH MATRIX D [6x6] (Strictly Proper Physical Mechatronic Plant)")
    lines.append("       ------------------------------------------------------------------------------------------------ *)")
    for row in range(1, 7):
        for col in range(1, 7):
            lines.append(f"    aMatD[{row}, {col}] := 0.000000;")

    lines.append("")
    lines.append("    (* ------------------------------------------------------------------------------------------------")
    lines.append("       STEADY-STATE KALMAN OBSERVER GAIN MATRIX L [18x6]")
    lines.append("       Optimized for sub-0.1 nm interferometer noise covariance Q_k and R_k")
    lines.append("       ------------------------------------------------------------------------------------------------ *)")
    for row in range(1, 19):
        for col in range(1, 7):
            val = 0.0
            # Position correction gains
            if row == col:
                val = 0.650000
            # Velocity correction gains
            elif row == col + 6:
                val = 42.500000
            # Modal observer gains
            elif row == 13 and col == 1:
                val = 0.085000
            elif row == 14 and col == 1:
                val = 8.250000
            elif row == 15 and col == 2:
                val = 0.078000
            elif row == 16 and col == 2:
                val = 7.820000
            elif row == 17 and col == 3:
                val = 0.062000
            elif row == 18 and col == 3:
                val = 6.450000
            lines.append(f"    aMatL[{row}, {col}] := {val:.6f};")

    lines.append("")
    lines.append("    (* ------------------------------------------------------------------------------------------------")
    lines.append("       GENERALIZED FORCE TO 8 LORENTZ COILS ALLOCATION MATRIX M_alloc [8x6]")
    lines.append("       Actuators: [X1, X2, Y1, Y2, Z1, Z2, Z3, Z4]")
    lines.append("       Inputs: [Fx, Fy, Fz, Tx, Ty, Tz]")
    lines.append("       Lorentz motor constant Kf = 28.5 N/A, Coil arm geometry: Lx = 0.22 m, Ly = 0.22 m")
    lines.append("       ------------------------------------------------------------------------------------------------ *)")
    # Actuator allocation:
    # X1, X2 share Fx and Tz
    # Y1, Y2 share Fy and Tz
    # Z1, Z2, Z3, Z4 share Fz, Tx, Ty
    alloc_table = [
        # Fx,       Fy,       Fz,       Tx,       Ty,       Tz
        [0.017544, 0.000000, 0.000000, 0.000000, 0.000000, -0.079745], # X1
        [0.017544, 0.000000, 0.000000, 0.000000, 0.000000,  0.079745], # X2
        [0.000000, 0.017544, 0.000000, 0.000000, 0.000000,  0.079745], # Y1
        [0.000000, 0.017544, 0.000000, 0.000000, 0.000000, -0.079745], # Y2
        [0.000000, 0.000000, 0.008772, -0.039872, -0.039872, 0.000000], # Z1 (corner -x, -y)
        [0.000000, 0.000000, 0.008772, -0.039872,  0.039872, 0.000000], # Z2 (corner +x, -y)
        [0.000000, 0.000000, 0.008772,  0.039872,  0.039872, 0.000000], # Z3 (corner +x, +y)
        [0.000000, 0.000000, 0.008772,  0.039872, -0.039872, 0.000000], # Z4 (corner -x, +y)
    ]
    for act_idx in range(1, 9):
        for force_idx in range(1, 7):
            val = alloc_table[act_idx - 1][force_idx - 1]
            lines.append(f"    aMatAlloc[{act_idx}, {force_idx}] := {val:.6f};")

    lines.append("")
    lines.append("    (* ------------------------------------------------------------------------------------------------")
    lines.append("       MPC QUADRATIC COST WEIGHTING MATRICES (Q, R, S, P) [6x6]")
    lines.append("       Tracking Penalty Q, Actuator Penalty R, Slew Penalty S, Terminal Penalty P")
    lines.append("       ------------------------------------------------------------------------------------------------ *)")
    # Q matrix: High weight on X, Y, Z overlay tracking error
    q_diag = [1.25e6, 1.25e6, 8.50e5, 4.20e4, 4.20e4, 6.80e4]
    r_diag = [0.0150, 0.0150, 0.0200, 0.0450, 0.0450, 0.0350]
    s_diag = [0.0850, 0.0850, 0.1200, 0.2500, 0.2500, 0.1800]
    p_diag = [3.50e6, 3.50e6, 2.20e6, 1.10e5, 1.10e5, 1.85e5]

    for r in range(1, 7):
        for c in range(1, 7):
            q_val = q_diag[r - 1] if r == c else 0.0
            r_val = r_diag[r - 1] if r == c else 0.0
            s_val = s_diag[r - 1] if r == c else 0.0
            p_val = p_diag[r - 1] if r == c else 0.0
            lines.append(f"    aMatQ[{r}, {c}] := {q_val:.4f};")
            lines.append(f"    aMatR[{r}, {c}] := {r_val:.4f};")
            lines.append(f"    aMatS[{r}, {c}] := {s_val:.4f};")
            lines.append(f"    aMatP[{r}, {c}] := {p_val:.4f};")

    lines.append("")
    lines.append("    (* Initialize estimated states and statistical ring buffers *)")
    lines.append("    FOR i := 1 TO 18 DO")
    lines.append("        aStateX[i] := 0.0;")
    lines.append("        aStateX_Pred[i] := 0.0;")
    lines.append("        aStateX_Next[i] := 0.0;")
    lines.append("    END_FOR;")
    lines.append("    FOR i := 1 TO 6 DO")
    lines.append("        aForceCmd6Dof[i] := 0.0;")
    lines.append("        aMpcControlU[i] := 0.0;")
    lines.append("        aMpcControlU_Prev[i] := 0.0;")
    lines.append("    END_FOR;")
    lines.append("    FOR i := 0 TO 63 DO")
    lines.append("        aJitterBufferX[i] := 0.0;")
    lines.append("        aJitterBufferY[i] := 0.0;")
    lines.append("    END_FOR;")
    lines.append("    nJitterBufferIdx := 0;")
    lines.append("    bJitterBufferFull := FALSE;")
    lines.append("    bFirstScanDone := TRUE;")
    lines.append("END_IF;")
    return "\n".join(lines)

print("parts_phase0.py generated.")
