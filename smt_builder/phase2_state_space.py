# -*- coding: utf-8 -*-
"""
smt_builder/phase2_state_space.py
Generates Phase 2: First-Principles Cyber-Physical State-Space Estimation (x[k+1] = A*x[k] + B*u[k] + L*e)
with full matrix initializations and unrolled matrix-vector operations.
"""

def get_phase2_state_space():
    lines = []
    lines.append("""(*
========================================================================================================================
  PHASE 2: FIRST-PRINCIPLES CYBER-PHYSICAL STATE-SPACE ESTIMATION (x[k+1] = A*x[k] + B*u[k] + L*e)
========================================================================================================================
  Cyber-Physical Model: 10 States, 4 Control Inputs, 6 Measurement Outputs at Discrete Sample Time Ts = 1.0 ms.
  Physical Mechanisms Modeled:
    1. Dual-drive linear motor carriage kinematics (mass M_car = 42.5 kg)
    2. Structural flexure resonance between carriage readhead and placement nozzle tool-center-point (TCP)
       (Stiffness K_flex = 2.45E7 N/m, Damping C_flex = 820.0 N*s/m, Modal mass M_tcp = 3.2 kg)
    3. Spindle head rotary turret hollow-shaft inertia (J_sp = 0.0018 kg*m^2, Viscous friction B_sp = 0.0035 N*m*s/rad)
    4. Vacuum chamber pneumatic siphon orifice pressure-flow dynamics (time constant tau_vac = 3.8 ms)
    5. Dual-drive gantry crossbeam yaw skew dynamics under differential X1/X2 thrust forces
    6. Invar and Zerodur linear scale thermal expansion drift dynamics.
*)

(* -------------------------------------------------------------------------------------------------------------------- *)
(* SUB-PHASE 2.1: REAL-TIME THERMAL LINEAR SCALE GRADIENT EXPANSION COMPENSATION                                        *)
(* -------------------------------------------------------------------------------------------------------------------- *)
rComp_X_Total_mm := (rScaleCTE_Invar * rLength_Gantry_X_mm * (rTemp_LinearScale_X1 - rRefTemp_Baseline))
                    + (0.5 * rThermalGradientGain_X * (rTemp_LinearScale_X1 - rTemp_LinearScale_X2) * rLength_Gantry_X_mm);

rComp_Y_Total_mm := (rScaleCTE_Ceramic * rLength_Gantry_Y_mm * (rTemp_LinearScale_Y - rRefTemp_Baseline));

rComp_Theta_Drum_deg := rTurretDrumExpansionGain * (rTemp_SpindleDrum - rRefTemp_Baseline);

(* Apply dynamic thermal offsets to voted raw measurements *)
rActual_Gantry_X_Pos := rVoted_X_Raw - rComp_X_Total_mm;
rActual_Gantry_Y_Pos := rVoted_Y_Raw - rComp_Y_Total_mm;
rActual_Head_Theta_Deg := rVoted_Theta_Raw - rComp_Theta_Drum_deg;
rActual_VacuumPressure_kPa := rVoted_Vac_Raw;
rActual_PCB_Surface_Z_mm := rVoted_Laser_Raw;

rCalculated_ThermalComp_X_um := rComp_X_Total_mm * 1000.0;
rCalculated_ThermalComp_Y_um := rComp_Y_Total_mm * 1000.0;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* SUB-PHASE 2.2: ONE-SHOT MATRIX INITIALIZATION OF DISCRETE STATE-SPACE (A, B, C, D, L, Q, R, S, P)                   *)
(* -------------------------------------------------------------------------------------------------------------------- *)
IF NOT bStateSpace_Initialized THEN
    (* Matrix A (10x10) Initialization - Discrete System Dynamics at Ts = 0.001s *)""")

    # Let's populate Matrix A: 10x10
    # Realistic continuous-to-discrete physics:
    # Row 1: x_car -> x1 + Ts*x2
    # Row 2: v_car -> x2 - (K_flex*Ts/M_car)*x3 - (C_flex*Ts/M_car)*x4
    # Row 3: delta_tcp -> x3 + Ts*x4
    # Row 4: v_tcp -> -(K_flex*Ts/M_tcp)*x3 + (1 - C_flex*Ts/M_tcp)*x4
    # Row 5: theta_sp -> x5 + 1000*Ts*x6
    # Row 6: omega_sp -> (1 - B_sp*Ts/J_sp)*x6
    # Row 7: P_vac -> (1 - Ts/tau_vac)*x7 - K_flow*x8
    # Row 8: Q_vac -> -alpha_q*x7 + (1 - Ts/tau_q)*x8
    # Row 9: phi_yaw -> (1 - Ts*decay_yaw)*x9
    # Row 10: eps_th -> (1 - Ts*decay_th)*x10
    a_vals = [
        [1.0,    0.001,   0.0,      0.0,      0.0,    0.0,     0.0,    0.0,    0.0,    0.0],
        [0.0,    0.9982, -0.5765,  -0.0193,   0.0,    0.0,     0.0,    0.0,   -0.0125, 0.0],
        [0.0,    0.0,     1.0,      0.001,    0.0,    0.0,     0.0,    0.0,    0.0,    0.0],
        [0.0,    0.0,    -7.6562,   0.7438,   0.0,    0.0,     0.0,    0.0,    0.0,    0.0],
        [0.0,    0.0,     0.0,      0.0,      1.0,    1.000,   0.0,    0.0,    0.0,    0.0],
        [0.0,    0.0,     0.0,      0.0,      0.0,    0.9980,  0.0,    0.0,    0.0,    0.0],
        [0.0,    0.0,     0.0,      0.0,      0.0,    0.0,     0.7634, -0.0482,0.0,    0.0],
        [0.0,    0.0,     0.0,      0.0,      0.0,    0.0,    -0.1245,  0.8850,0.0,    0.0],
        [0.0,    0.0,     0.0,      0.0,      0.0,    0.0,     0.0,    0.0,    0.9850, 0.0],
        [0.0,    0.0,     0.0,      0.0,      0.0,    0.0,     0.0,    0.0,    0.0,    0.9995]
    ]

    for i in range(10):
        for j in range(10):
            val = a_vals[i][j]
            lines.append(f"    a_mat[{i+1}, {j+1}] := {val:.6f};")

    lines.append("\n    (* Matrix B (10x4) Initialization - Input Influence Matrix *)")
    b_vals = [
        [0.000012, 0.0,      0.0,     0.0],
        [0.023529, 0.0,      0.0,     0.0],
        [0.0,      0.0,      0.0,     0.0],
        [0.015625, 0.0,      0.0,     0.0],
        [0.0,      0.0,      0.2778,  0.0],
        [0.0,      0.0,      0.5556,  0.0],
        [0.0,      0.0,      0.0,    -0.8542],
        [0.0,      0.0,      0.0,     1.2450],
        [0.001850, 0.0,      0.0,     0.0],
        [0.0,      0.0,      0.0,     0.0]
    ]
    for i in range(10):
        for j in range(4):
            val = b_vals[i][j]
            lines.append(f"    b_mat[{i+1}, {j+1}] := {val:.6f};")

    lines.append("\n    (* Matrix C (6x10) Initialization - Output Observation Matrix *)")
    c_vals = [
        [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.001],
        [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0]
    ]
    for i in range(6):
        for j in range(10):
            val = c_vals[i][j]
            lines.append(f"    c_mat[{i+1}, {j+1}] := {val:.6f};")

    lines.append("\n    (* Matrix D (6x4) Initialization - Direct Feedthrough Matrix *)")
    for i in range(6):
        for j in range(4):
            lines.append(f"    d_mat[{i+1}, {j+1}] := 0.000000;")

    lines.append("\n    (* Observer Gain Matrix L (10x6) - Steady-State Kalman/Luenberger Observer Gains *)")
    l_vals = [
        [0.2850, 0.0125, 0.0,    0.0,    0.0150, 0.0],
        [0.4520, 0.3120, 0.0,    0.0,    0.0240, 0.0],
        [0.0180, 0.0040, 0.0,    0.0,    0.3850, 0.0],
        [0.0520, 0.0150, 0.0,    0.0,    0.6200, 0.0],
        [0.0,    0.0,    0.3450, 0.0,    0.0,    0.0],
        [0.0,    0.0,    0.5120, 0.0,    0.0,    0.0],
        [0.0,    0.0,    0.0,    0.4280, 0.0,    0.0],
        [0.0,    0.0,    0.0,    0.2850, 0.0,    0.0],
        [0.0085, 0.0020, 0.0,    0.0,    0.0,    0.2950],
        [0.0015, 0.0,    0.0,    0.0,    0.0,    0.0]
    ]
    for i in range(10):
        for j in range(6):
            val = l_vals[i][j]
            lines.append(f"    l_obs[{i+1}, {j+1}] := {val:.6f};")

    lines.append("\n    (* MPC State Cost Diagonal Matrix Q (10x10) *)")
    q_diags = [1500.0, 25.0, 3500.0, 150.0, 850.0, 15.0, 120.0, 10.0, 800.0, 50.0]
    for i in range(10):
        for j in range(10):
            val = q_diags[i] if i == j else 0.0
            lines.append(f"    q_mat[{i+1}, {j+1}] := {val:.4f};")

    lines.append("\n    (* MPC Actuator Penalty Diagonal Matrix R (4x4) *)")
    r_diags = [0.085, 0.095, 0.045, 0.015]
    for i in range(4):
        for j in range(4):
            val = r_diags[i] if i == j else 0.0
            lines.append(f"    r_mat[{i+1}, {j+1}] := {val:.4f};")

    lines.append("\n    (* MPC Actuator Slew Rate Penalty Matrix S (4x4) *)")
    s_diags = [0.250, 0.280, 0.120, 0.050]
    for i in range(4):
        for j in range(4):
            val = s_diags[i] if i == j else 0.0
            lines.append(f"    s_mat[{i+1}, {j+1}] := {val:.4f};")

    lines.append("\n    (* MPC Terminal State Cost Matrix P (10x10) *)")
    p_diags = [2800.0, 50.0, 6200.0, 320.0, 1500.0, 30.0, 240.0, 20.0, 1400.0, 100.0]
    for i in range(10):
        for j in range(10):
            val = p_diags[i] if i == j else 0.0
            lines.append(f"    p_mat[{i+1}, {j+1}] := {val:.4f};")

    lines.append("""
    bStateSpace_Initialized := TRUE;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* SUB-PHASE 2.3: MEASUREMENT VECTOR ACQUISITION & ESTIMATION ERROR RESIDUAL                                            *)
(* -------------------------------------------------------------------------------------------------------------------- *)
y_meas[1] := rActual_Gantry_X_Pos;
y_meas[2] := (rActual_Gantry_X_Pos - x_state[1]) / 0.001;
y_meas[3] := rActual_Head_Theta_Deg * 17.4532925; (* Convert deg to mrad *)
y_meas[4] := rActual_VacuumPressure_kPa;
y_meas[5] := rActual_Gantry_Y_Pos;
y_meas[6] := rActual_PCB_Surface_Z_mm;

(* Compute Predicted Output Vector y_est[k] = C * x_state + D * u_ctrl *)
FOR iRow := 1 TO 6 DO
    rAccumTerm := 0.0;
    FOR iCol := 1 TO 10 DO
        rAccumTerm := rAccumTerm + (c_mat[iRow, iCol] * x_state[iCol]);
    END_FOR;
    FOR iCol := 1 TO 4 DO
        rAccumTerm := rAccumTerm + (d_mat[iRow, iCol] * u_ctrl[iCol]);
    END_FOR;
    y_est[iRow] := rAccumTerm;
    e_innov[iRow] := y_meas[iRow] - y_est[iRow];
END_FOR;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* SUB-PHASE 2.4: CYBER-PHYSICAL STATE PROPAGATION WITH OBSERVER INNOVATION (x[k+1] = A*x + B*u + L*e)                  *)
(* -------------------------------------------------------------------------------------------------------------------- *)
FOR iRow := 1 TO 10 DO
    rAccumTerm := 0.0;
    (* State transition A * x *)
    FOR iCol := 1 TO 10 DO
        rAccumTerm := rAccumTerm + (a_mat[iRow, iCol] * x_state[iCol]);
    END_FOR;
    (* Control input B * u *)
    FOR iCol := 1 TO 4 DO
        rAccumTerm := rAccumTerm + (b_mat[iRow, iCol] * u_ctrl[iCol]);
    END_FOR;
    (* Observer correction L * e *)
    FOR iCol := 1 TO 6 DO
        rAccumTerm := rAccumTerm + (l_obs[iRow, iCol] * e_innov[iCol]);
    END_FOR;
    x_next[iRow] := rAccumTerm;
END_FOR;

(* State update for current cycle *)
FOR iRow := 1 TO 10 DO
    x_state[iRow] := x_next[iRow];
END_FOR;

(* Assign Cyber-Physical Observer Telemetry *)
rEstimated_TCP_Vibration_um := x_state[3] * 1000.0;
rEstimated_Gantry_Yaw_mrad  := x_state[9];
""")
    return "\n".join(lines)
