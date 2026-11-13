# biopharm_aseptic_vial_builder/build_st_matrices.py

def get_matrices_initialization():
    lines = []
    lines.append("(* ========================================================================================= *)")
    lines.append("(* PHASE 0: FIRST-PRINCIPLES CYBER-PHYSICAL STATE-SPACE & MPC MATRICES INITIALIZATION        *)")
    lines.append("(* Explicit Discretization at Ts = 5 ms (0.005 s) for Aseptic VPM Monoblock & Grade A Isolator *)")
    lines.append("(* ========================================================================================= *)")
    lines.append("IF NOT bMatricesInitialized THEN")
    lines.append("    (* --- 1. System Dynamic Matrix mA [12x12] --- *)")
    lines.append("    (* Physical States: x1=z_pist, x2=v_pist, x3=theta_rot, x4=P_cham, x5=z_need, x6=v_need, *)")
    lines.append("    (*                  x7=h_menisc, x8=I_emfr, x9=P_iso, x10=v_air, x11=C_vhp, x12=RH_iso     *)")
    
    # 12x12 mA
    mA_vals = [
        # Row 1: z_pist (kinematics: dz/dt = v)
        [0.9985, 0.00495, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        # Row 2: v_pist (viscous damping & spring backpressure)
        [0.0, 0.9420, 0.0012, -0.0035, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        # Row 3: theta_rot (servo rotation)
        [0.0, 0.0, 0.9850, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        # Row 4: P_cham (chamber bulk modulus compressibility dP/dt = beta/V*(Q_in - Q_out))
        [0.0125, 0.0850, -0.0450, 0.8920, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        # Row 5: z_need (needle vertical kinematics)
        [0.0, 0.0, 0.0, 0.0, 0.9990, 0.00498, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        # Row 6: v_need (needle servo acceleration and mechanical friction)
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.9350, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        # Row 7: h_menisc (meniscus rise: depends on piston stroke speed and chamber pressure)
        [0.0022, 0.0385, 0.0015, 0.0142, 0.0, 0.0, 0.9995, 0.0, 0.0, 0.0, 0.0, 0.0],
        # Row 8: I_emfr (voice-coil current dynamics with settling time tau = 35 ms)
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0045, 0.8650, 0.0, 0.0, 0.0, 0.0],
        # Row 9: P_iso (isolator pressure pneumatic time constant tau = 180 ms)
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.9725, 0.0185, 0.0, 0.0],
        # Row 10: v_air (HEPA plenum airflow inertia)
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0025, 0.9650, 0.0, 0.0],
        # Row 11: C_vhp (catalytic breakdown & dilution rate)
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.0085, 0.9880, 0.0042],
        # Row 12: RH_iso (dehumidification / condensation balance)
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.0045, 0.0020, 0.9910]
    ]
    for r in range(12):
        for c in range(12):
            lines.append(f"    mA[{r+1}, {c+1}] := {mA_vals[r][c]:.6f};")

    lines.append("")
    lines.append("    (* --- 2. Input Coupling Matrix mB [12x8] --- *)")
    lines.append("    (* Inputs: u1=u_stroke, u2=u_rot, u3=u_dive, u4=u_trim, u5=u_blow, u6=u_exh, u7=u_vhp, u8=u_crimp *)")
    mB_vals = [
        [0.00185, 0.0, 0.0, 0.00045, 0.0, 0.0, 0.0, 0.0],
        [0.05420, 0.0, 0.0, 0.01250, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.08250, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.04850, 0.01520, 0.0, 0.02400, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.00245, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.06850, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.02450, 0.00550, 0.0, 0.00850, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.04500, -0.03850, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.03250, -0.00850, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, -0.01500, 0.0, 0.12500, 0.0],
        [0.0, 0.0, 0.0, 0.0, -0.00950, 0.0, 0.06500, 0.0]
    ]
    for r in range(12):
        for c in range(8):
            lines.append(f"    mB[{r+1}, {c+1}] := {mB_vals[r][c]:.6f};")

    lines.append("")
    lines.append("    (* --- 3. Disturbance Matrix mEw [12x4] --- *)")
    lines.append("    (* Disturbances: w1=delta_mu, w2=delta_Pin, w3=delta_V_glove, w4=delta_P_amb *)")
    mEw_vals = [
        [0.0, 0.00015, 0.0, 0.0],
        [-0.01850, 0.00850, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0],
        [-0.03500, 0.04500, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0],
        [-0.01200, 0.00450, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, -0.08500, 0.06500],
        [0.0, 0.0, -0.01250, 0.01800],
        [0.0, 0.0, 0.0, -0.00550],
        [0.0, 0.0, 0.0, 0.01200]
    ]
    for r in range(12):
        for c in range(4):
            lines.append(f"    mEw[{r+1}, {c+1}] := {mEw_vals[r][c]:.6f};")

    lines.append("")
    lines.append("    (* --- 4. Measurement Output Matrix mC [8x12] --- *)")
    lines.append("    (* Outputs: y1=Q_disp, y2=delta_z_tip, y3=m_gross, y4=P_iso, y5=v_air, y6=C_vhp, y7=RH_iso, y8=F_crimp *)")
    mC_vals = [
        [0.0, 0.1540, 0.0250, 0.0850, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 1.0000, 0.0, -1.0000, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 102.80, 1.0000, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0000, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0000, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0000, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0000],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    ]
    for r in range(8):
        for c in range(12):
            lines.append(f"    mC[{r+1}, {c+1}] := {mC_vals[r][c]:.6f};")

    lines.append("")
    lines.append("    (* --- 5. Direct Feedthrough Matrix mD [8x8] --- *)")
    for r in range(8):
        for c in range(8):
            if r == 7 and c == 7:
                lines.append(f"    mD[{r+1}, {c+1}] := 1.450000; (* Actuator direct coupling to crimp force *)")
            else:
                lines.append(f"    mD[{r+1}, {c+1}] := 0.000000;")

    lines.append("")
    lines.append("    (* --- 6. Steady-State Kalman Observer Gain Matrix mK [12x8] --- *)")
    mK_vals = [
        [0.0420, 0.0, 0.0015, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.1250, 0.0, 0.0085, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0850, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0950, 0.0, 0.0042, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0820, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.1450, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0380, -0.0420, 0.0125, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.1650, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.1850, 0.0120, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0150, 0.1550, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.1750, 0.0085, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0120, 0.1620, 0.0]
    ]
    for r in range(12):
        for c in range(8):
            lines.append(f"    mK[{r+1}, {c+1}] := {mK_vals[r][c]:.6f};")

    lines.append("")
    lines.append("    (* --- 7. MPC Output Tracking Weight Matrix mQ [8x8] --- *)")
    mQ_diag = [12.5, 45.0, 8.5, 35.0, 25.0, 18.0, 10.0, 15.0]
    for r in range(8):
        for c in range(8):
            val = mQ_diag[r] if r == c else 0.0
            lines.append(f"    mQ[{r+1}, {c+1}] := {val:.4f};")

    lines.append("")
    lines.append("    (* --- 8. MPC Actuator Effort Weight Matrix mR [8x8] --- *)")
    mR_diag = [0.85, 0.65, 1.25, 2.50, 0.45, 0.55, 1.10, 0.90]
    for r in range(8):
        for c in range(8):
            val = mR_diag[r] if r == c else 0.0
            lines.append(f"    mR[{r+1}, {c+1}] := {val:.4f};")

    lines.append("")
    lines.append("    (* --- 9. MPC Slew-Rate Penalty Matrix mS [8x8] --- *)")
    mS_diag = [2.50, 1.80, 4.20, 5.00, 1.50, 1.60, 2.80, 2.20]
    for r in range(8):
        for c in range(8):
            val = mS_diag[r] if r == c else 0.0
            lines.append(f"    mS[{r+1}, {c+1}] := {val:.4f};")

    lines.append("")
    lines.append("    (* --- 10. MPC Terminal State Penalty Matrix mP [12x12] --- *)")
    mP_diag = [15.0, 8.0, 12.0, 18.0, 25.0, 14.0, 50.0, 10.0, 40.0, 30.0, 22.0, 16.0]
    for r in range(12):
        for c in range(12):
            val = mP_diag[r] if r == c else 0.0
            lines.append(f"    mP[{r+1}, {c+1}] := {val:.4f};")

    lines.append("")
    lines.append("    bMatricesInitialized := TRUE;")
    lines.append("END_IF;")
    return "\n".join(lines)
