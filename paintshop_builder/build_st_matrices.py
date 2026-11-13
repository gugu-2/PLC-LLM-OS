# paintshop_builder/build_st_matrices.py

def get_matrices_initialization():
    lines = []
    lines.append("(* ==================================================================================================== *)")
    lines.append("(* PHASE 0: ONE-SHOT FIRST-SCAN SYSTEM INITIALIZATION & CYBER-PHYSICAL MATRIX ALLOCATION             *)")
    lines.append("(* ==================================================================================================== *)")
    lines.append("IF NOT bFirstScanDone THEN")
    lines.append("    (* ------------------------------------------------------------------------------------------------ *)")
    lines.append("    (* 1. Discrete State-Space System Matrix A (8x8) at Ts = 0.010 s                                    *)")
    lines.append("    (* ------------------------------------------------------------------------------------------------ *)")

    # Define A matrix elements
    # States: 1:TurbineSpeed, 2:HV, 3:LinePress, 4:PaintFlow, 5:InnerAir, 6:OuterAir, 7:DowndraftP, 8:VOC_LEL
    A_vals = [
        [0.9820,  0.0000, -0.0125, -0.0080,  0.0040,  0.0030,  0.0000,  0.0000],
        [0.0000,  0.9650,  0.0000, -0.0050,  0.0000,  0.0000,  0.0000,  0.0000],
        [0.0000,  0.0000,  0.9250, -0.0450,  0.0000,  0.0000,  0.0000,  0.0000],
        [0.0020,  0.0000,  0.0820,  0.9400,  0.0000,  0.0000,  0.0000,  0.0000],
        [0.0000,  0.0000,  0.0000,  0.0000,  0.9100, -0.0150,  0.0000,  0.0000],
        [0.0000,  0.0000,  0.0000,  0.0000, -0.0120,  0.9150,  0.0000,  0.0000],
        [0.0000,  0.0000,  0.0000,  0.0000,  0.0050,  0.0060,  0.9780,  0.0000],
        [0.0000,  0.0000,  0.0000,  0.0380,  0.0000,  0.0000, -0.0150,  0.9850]
    ]

    a_comments = [
        "Turbine speed damping & aerodynamic load coupling",
        "HV cascade potential decay & corona dissipation",
        "Paint line hydraulic compressibility & flow resistance",
        "Micro-gear positive displacement flow inertia",
        "Inner shaping shroud air electronic pressure dynamics",
        "Outer shaping shroud air electronic pressure dynamics",
        "Cleanroom downdraft plenum static pressure capacitance",
        "Exhaust solvent VOC vapor transport & recirc balance"
    ]

    for i in range(8):
        lines.append(f"    (* State x[{i+1}]: {a_comments[i]} *)")
        for j in range(8):
            val = A_vals[i][j]
            lines.append(f"    A[{i+1}, {j+1}] := {val:.4f};")

    lines.append("")
    lines.append("    (* ------------------------------------------------------------------------------------------------ *)")
    lines.append("    (* 2. Discrete Input Coupling Matrix B (8x6) at Ts = 0.010 s                                        *)")
    lines.append("    (* ------------------------------------------------------------------------------------------------ *)")

    # Controls: 1:DriveAir, 2:HV_PWM, 3:PumpSpeed, 4:InnerAirCmd, 5:OuterAirCmd, 6:DamperCmd
    B_vals = [
        [145.2000,   0.0000,  -0.4500,   0.0000,   0.0000,   0.0000],
        [  0.0000,  -0.9000,   0.0000,   0.0000,   0.0000,   0.0000],
        [  0.0000,   0.0000,   0.1600,   0.0000,   0.0000,   0.0000],
        [  0.0000,   0.0000,   3.6500,   0.0000,   0.0000,   0.0000],
        [  0.0000,   0.0000,   0.0000,   0.0900,   0.0000,   0.0000],
        [  0.0000,   0.0000,   0.0000,   0.0000,   0.0850,   0.0000],
        [  0.0000,   0.0000,   0.0000,   0.0020,   0.0025,   0.2500],
        [  0.0000,   0.0000,   0.0150,   0.0000,   0.0000,  -0.1200]
    ]

    for i in range(8):
        lines.append(f"    (* Control inputs to State x[{i+1}] *)")
        for j in range(6):
            val = B_vals[i][j]
            lines.append(f"    B[{i+1}, {j+1}] := {val:.4f};")

    lines.append("")
    lines.append("    (* ------------------------------------------------------------------------------------------------ *)")
    lines.append("    (* 3. Output Observation Matrix C_mat (6x8) at Ts = 0.010 s                                         *)")
    lines.append("    (* ------------------------------------------------------------------------------------------------ *)")

    # Outputs: 1:Speed, 2:HV, 3:Flow, 4:InnerAir, 5:OuterAir, 6:DowndraftP
    C_vals = [
        [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0]
    ]

    for i in range(6):
        lines.append(f"    (* Measurement y[{i+1}] observation weights *)")
        for j in range(8):
            val = C_vals[i][j]
            lines.append(f"    C_mat[{i+1}, {j+1}] := {val:.4f};")

    lines.append("")
    lines.append("    (* ------------------------------------------------------------------------------------------------ *)")
    lines.append("    (* 4. Direct Feedthrough Matrix D_mat (6x6)                                                         *)")
    lines.append("    (* ------------------------------------------------------------------------------------------------ *)")
    for i in range(6):
        for j in range(6):
            lines.append(f"    D_mat[{i+1}, {j+1}] := 0.0000;")

    lines.append("")
    lines.append("    (* ------------------------------------------------------------------------------------------------ *)")
    lines.append("    (* 5. Disturbance Coupling Matrix E_w (8x3)                                                         *)")
    lines.append("    (* ------------------------------------------------------------------------------------------------ *)")

    # Disturbances: 1:RobotTCPAccel, 2:PaintViscosity, 3:BoothDraft
    E_vals = [
        [-0.0500,  0.0000,  0.0000],
        [ 0.0000,  0.0000, -0.0200],
        [ 0.1800,  0.0450,  0.0000],
        [-0.0850, -0.2200,  0.0000],
        [ 0.0000,  0.0000,  0.0100],
        [ 0.0000,  0.0000,  0.0120],
        [ 0.0000,  0.0000,  0.4500],
        [ 0.0000,  0.0000, -0.0500]
    ]

    for i in range(8):
        lines.append(f"    (* Disturbance impacts on State x[{i+1}] *)")
        for j in range(3):
            val = E_vals[i][j]
            lines.append(f"    E_w[{i+1}, {j+1}] := {val:.4f};")

    lines.append("")
    lines.append("    (* ------------------------------------------------------------------------------------------------ *)")
    lines.append("    (* 6. Steady-State Kalman Observer Gain Matrix K_obs (8x6)                                          *)")
    lines.append("    (* ------------------------------------------------------------------------------------------------ *)")

    K_vals = [
        [0.2450,  0.0000, -0.0025,  0.0000,  0.0000,  0.0000],
        [0.0000,  0.2850,  0.0000,  0.0000,  0.0000,  0.0000],
        [0.0000,  0.0000,  0.1150,  0.0000,  0.0000,  0.0000],
        [0.0015,  0.0000,  0.3150,  0.0000,  0.0000,  0.0000],
        [0.0000,  0.0000,  0.0000,  0.3400, -0.0050,  0.0000],
        [0.0000,  0.0000,  0.0000, -0.0040,  0.3350,  0.0000],
        [0.0000,  0.0000,  0.0000,  0.0010,  0.0015,  0.2950],
        [0.0000,  0.0000,  0.0420,  0.0000,  0.0000, -0.0180]
    ]

    for i in range(8):
        lines.append(f"    (* Innovation gain for State x[{i+1}] *)")
        for j in range(6):
            val = K_vals[i][j]
            lines.append(f"    K_obs[{i+1}, {j+1}] := {val:.4f};")

    lines.append("")
    lines.append("    (* ------------------------------------------------------------------------------------------------ *)")
    lines.append("    (* 7. MPC State Tracking Cost Weighting Matrix Q_cost (8x8)                                         *)")
    lines.append("    (* ------------------------------------------------------------------------------------------------ *)")
    q_diag = [0.0050, 2.5000, 1.2000, 4.8000, 8.5000, 8.5000, 12.0000, 15.0000]
    for i in range(8):
        for j in range(8):
            val = q_diag[i] if i == j else 0.0
            lines.append(f"    Q_cost[{i+1}, {j+1}] := {val:.4f};")

    lines.append("")
    lines.append("    (* ------------------------------------------------------------------------------------------------ *)")
    lines.append("    (* 8. MPC Control Effort Weighting Matrix R_cost (6x6)                                              *)")
    lines.append("    (* ------------------------------------------------------------------------------------------------ *)")
    r_diag = [0.1500, 0.2000, 0.0800, 1.5000, 1.5000, 0.3500]
    for i in range(6):
        for j in range(6):
            val = r_diag[i] if i == j else 0.0
            lines.append(f"    R_cost[{i+1}, {j+1}] := {val:.4f};")

    lines.append("")
    lines.append("    (* ------------------------------------------------------------------------------------------------ *)")
    lines.append("    (* 9. MPC Terminal State Cost Matrix P_term (8x8)                                                   *)")
    lines.append("    (* ------------------------------------------------------------------------------------------------ *)")
    for i in range(8):
        for j in range(8):
            val = (q_diag[i] * 2.5) if i == j else 0.0
            lines.append(f"    P_term[{i+1}, {j+1}] := {val:.4f};")

    lines.append("")
    lines.append("    (* ------------------------------------------------------------------------------------------------ *)")
    lines.append("    (* 10. MPC Actuator Slew-Rate Penalty Matrix S_slew (6x6)                                           *)")
    lines.append("    (* ------------------------------------------------------------------------------------------------ *)")
    s_diag = [0.8500, 1.2000, 0.4000, 2.5000, 2.5000, 0.9000]
    for i in range(6):
        for j in range(6):
            val = s_diag[i] if i == j else 0.0
            lines.append(f"    S_slew[{i+1}, {j+1}] := {val:.4f};")

    lines.append("")
    lines.append("    (* ------------------------------------------------------------------------------------------------ *)")
    lines.append("    (* 11. Actuator Hard Physical Box Constraints & Slew Limits                                         *)")
    lines.append("    (* ------------------------------------------------------------------------------------------------ *)")
    # Actuators: 1:DriveAir %, 2:HV %, 3:PumpSpeed rpm, 4:InnerAir bar, 5:OuterAir bar, 6:Damper %
    u_mins = [0.0, 0.0, 0.0, 0.5, 0.5, 10.0]
    u_maxs = [100.0, 100.0, 250.0, 5.5, 5.5, 100.0]
    du_maxs = [5.0, 10.0, 20.0, 0.25, 0.25, 4.0]

    for i in range(6):
        lines.append(f"    u_min[{i+1}] := {u_mins[i]:.2f};")
        lines.append(f"    u_max[{i+1}] := {u_maxs[i]:.2f};")
        lines.append(f"    du_max[{i+1}] := {du_maxs[i]:.2f};")

    lines.append("")
    lines.append("    (* ------------------------------------------------------------------------------------------------ *)")
    lines.append("    (* 12. Dynamic State & Trajectory Zero Initialization                                              *)")
    lines.append("    (* ------------------------------------------------------------------------------------------------ *)")
    for i in range(8):
        lines.append(f"    x_state[{i+1}] := 0.0;")
        lines.append(f"    x_hat[{i+1}] := 0.0;")
        lines.append(f"    x_pred[{i+1}] := 0.0;")
        lines.append(f"    r_ref[{i+1}] := 0.0;")

    for i in range(6):
        lines.append(f"    u_ctrl[{i+1}] := 0.0;")
        lines.append(f"    u_prev[{i+1}] := 0.0;")
        lines.append(f"    y_meas[{i+1}] := 0.0;")
        lines.append(f"    y_est[{i+1}] := 0.0;")
        lines.append(f"    e_innov[{i+1}] := 0.0;")

    for i in range(3):
        lines.append(f"    w_dist[{i+1}] := 0.0;")

    for step in range(6):
        for i in range(8):
            lines.append(f"    x_traj[{step}, {i+1}] := 0.0;")
            lines.append(f"    lambda_adj[{step}, {i+1}] := 0.0;")

    for step in range(5):
        for j in range(6):
            lines.append(f"    u_traj[{step}, {j+1}] := 0.0;")
            lines.append(f"    grad_u[{step}, {j+1}] := 0.0;")

    lines.append("")
    lines.append("    bFirstScanDone := TRUE;")
    lines.append("END_IF;")
    lines.append("")
    return "\n".join(lines)
