# -*- coding: utf-8 -*-
"""
Phase 3: Receding-Horizon Model Predictive Control (MPC) with 8x8 State-Space Dynamics
"""

def generate_phase3():
    lines = []
    lines.append("(* =================================================================================================== *)")
    lines.append("(* === PHASE 3: RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) & 8x8 STATE-SPACE === *)")
    lines.append("(* =================================================================================================== *)")
    lines.append("")
    lines.append("(* --------------------------------------------------------------------------------------------------- *)")
    lines.append("(* 3.1 INITIALIZATION OF 8x8 CYBER-PHYSICAL STATE-SPACE MATRICES (Ts = 100 ms)                         *)")
    lines.append("(* --------------------------------------------------------------------------------------------------- *)")
    lines.append("IF NOT bMPC_Initialized THEN")
    
    # Generate A matrix (8x8)
    a_mat = [
        [0.985, -0.012,  0.000,  0.000,  0.005,  0.000, -0.015,  0.000],
        [0.008,  0.942,  0.000,  0.000,  0.000,  0.000,  0.000,  0.000],
        [0.015,  0.000,  0.965, -0.024,  0.008, -0.012,  0.000,  0.000],
        [0.000,  0.000,  0.018,  0.978,  0.000,  0.000,  0.000,  0.000],
        [0.022,  0.000,  0.000,  0.000,  0.962, -0.018,  0.000,  0.000],
        [0.000,  0.000,  0.000,  0.000,  0.014,  0.958,  0.000,  0.000],
        [0.035,  0.000,  0.000,  0.000,  0.000,  0.000,  0.945, -0.012],
        [0.000,  0.000,  0.000,  0.000,  0.000,  0.000,  0.025,  0.982]
    ]
    for r in range(8):
        for c in range(8):
            lines.append(f"    rMatrixA[{r+1}, {c+1}] := {a_mat[r][c]:.4f};")
    lines.append("")
    
    # Generate B matrix (8x8)
    b_mat = [
        [ 0.0850, -0.0050,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000],
        [-0.0450,  0.0920,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000],
        [ 0.0120,  0.0000, -0.0780, -0.0250,  0.0000, -0.0320,  0.0000,  0.0000],
        [ 0.0000,  0.0000, -0.0650,  0.0450,  0.0000,  0.0000,  0.0000,  0.0000],
        [ 0.0180,  0.0000,  0.0000,  0.0000, -0.0820, -0.0450,  0.0120,  0.0000],
        [ 0.0000,  0.0000,  0.0000,  0.0000,  0.0000,  0.0950,  0.0000,  0.0000],
        [ 0.0280,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000, -0.0150, -0.0520],
        [ 0.0000,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000, -0.0350, -0.0880]
    ]
    for r in range(8):
        for c in range(8):
            lines.append(f"    rMatrixB[{r+1}, {c+1}] := {b_mat[r][c]:.4f};")
    lines.append("")
    
    # Generate C and D matrices (8x8)
    for r in range(8):
        for c in range(8):
            val_c = 1.0 if r == c else 0.0
            lines.append(f"    rMatrixC[{r+1}, {c+1}] := {val_c:.1f};")
            lines.append(f"    rMatrixD[{r+1}, {c+1}] := 0.0;")
    lines.append("")
    
    # Generate Q, R, S, P matrices (8x8)
    q_diag = [15.0, 10.0, 12.0, 8.0, 10.0, 6.0, 14.0, 8.0]
    r_diag = [ 3.5,  2.5,  3.0, 2.0,  2.8, 2.2,  3.0, 3.2]
    s_diag = [12.0,  8.0, 10.0, 8.0,  9.0, 7.5, 10.0, 9.5]
    p_diag = [38.0, 26.0, 32.0, 22.0, 28.0, 18.0, 35.0, 24.0]
    
    for r in range(8):
        for c in range(8):
            val_q = q_diag[r] if r == c else 0.0
            val_r = r_diag[r] if r == c else 0.0
            val_s = s_diag[r] if r == c else 0.0
            val_p = p_diag[r] if r == c else 0.0
            lines.append(f"    rMatrixQ[{r+1}, {c+1}] := {val_q:.1f};")
            lines.append(f"    rMatrixR[{r+1}, {c+1}] := {val_r:.1f};")
            lines.append(f"    rMatrixS[{r+1}, {c+1}] := {val_s:.1f};")
            lines.append(f"    rMatrixP[{r+1}, {c+1}] := {val_p:.1f};")
    lines.append("")
    
    # Actuator limits
    u_mins = [ 5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  0.0,  5.0]
    u_maxs = [95.0, 95.0, 95.0, 95.0, 95.0, 95.0, 90.0, 95.0]
    du_maxs = [0.8,  1.2,  1.5,  1.0,  1.2,  1.5,  1.0,  1.2]
    for i in range(8):
        lines.append(f"    rU_min[{i+1}] := {u_mins[i]:.1f};")
        lines.append(f"    rU_max[{i+1}] := {u_maxs[i]:.1f};")
        lines.append(f"    rDeltaU_max[{i+1}] := {du_maxs[i]:.2f};")
        lines.append(f"    rControl_u_prev[{i+1}] := 50.0;")
        lines.append(f"    rControl_u[{i+1}] := 50.0;")
        
    lines.append("    bMPC_Initialized := TRUE;")
    lines.append("END_IF;")
    lines.append("")
    lines.append("(* --------------------------------------------------------------------------------------------------- *)")
    lines.append("(* 3.2 CURRENT PROCESS STATE ERROR VECTOR DERIVATION (x = y_voted - y_setpoint)                        *)")
    lines.append("(* --------------------------------------------------------------------------------------------------- *)")
    lines.append("rState_x[1] := rVoted_TT_102 - rSP_FurnaceCOT_DegC;        (* x1: Coil Outlet Temp Error [deg C] *)")
    lines.append("rState_x[2] := rVoted_AT_201 - rSP_FlueGasO2_pct;          (* x2: Excess O2 Error [vol%] *)")
    lines.append("rState_x[3] := rVoted_TT_302 - rSP_OverheadTemp_DegC;      (* x3: Overhead Vapor Temp Error [deg C] *)")
    lines.append("rState_x[4] := rVoted_LT_303 - rSP_RefluxDrumLevel_pct;    (* x4: Reflux Drum Level Error [%] *)")
    lines.append("rState_x[5] := rVoted_TT_401 - rSP_DieselTrayTemp_DegC;    (* x5: Diesel Draw Tray Temp Error [deg C] *)")
    lines.append("rState_x[6] := rObs_PA1_ActualHeatDuty_MW - rSP_PA1_Duty_MW; (* x6: PA-1 Heat Duty Error [MW] *)")
    lines.append("rState_x[7] := rObs_OverflashLiquidRate_m3h - rSP_OverflashRate_m3h; (* x7: Overflash Liquid Error [m3/h] *)")
    lines.append("rState_x[8] := rVoted_LT_601 - rSP_BottomsLevel_pct;       (* x8: Column Bottom Residue Level Error [%] *)")
    lines.append("")
    lines.append("(* --------------------------------------------------------------------------------------------------- *)")
    lines.append("(* 3.3 ITERATIVE PROJECTED GRADIENT DESCENT (PGD) OPTIMIZER (10 ITERATIONS)                            *)")
    lines.append("(* --------------------------------------------------------------------------------------------------- *)")
    lines.append("FOR iIter := 1 TO 10 DO")
    lines.append("    (* Step A: Receding-horizon state prediction x[k+1] = A * x[k] + B * u[k] *)")
    lines.append("    FOR iRow := 1 TO 8 DO")
    lines.append("        rState_x_pred[iRow] := 0.0;")
    lines.append("        FOR iCol := 1 TO 8 DO")
    lines.append("            rState_x_pred[iRow] := rState_x_pred[iRow] + (rMatrixA[iRow, iCol] * rState_x[iCol]) + (rMatrixB[iRow, iCol] * rControl_u[iCol]);")
    lines.append("        END_FOR;")
    lines.append("    END_FOR;")
    lines.append("")
    lines.append("    (* Step B: Analytical gradient computation grad_g = 2*R*u + 2*S*(u - u_prev) + 2*B^T*P*x_pred *)")
    lines.append("    FOR iCol := 1 TO 8 DO")
    lines.append("        rGrad_g[iCol] := (2.0 * rMatrixR[iCol, iCol] * rControl_u[iCol]) + (2.0 * rMatrixS[iCol, iCol] * (rControl_u[iCol] - rControl_u_prev[iCol]));")
    lines.append("        FOR iRow := 1 TO 8 DO")
    lines.append("            rGrad_g[iCol] := rGrad_g[iCol] + (2.0 * rMatrixB[iRow, iCol] * rMatrixP[iRow, iRow] * rState_x_pred[iRow]);")
    lines.append("        END_FOR;")
    lines.append("    END_FOR;")
    lines.append("")
    lines.append("    (* Step C: Projected gradient descent step with slew & saturation boundary clamping *)")
    lines.append("    FOR iCol := 1 TO 8 DO")
    lines.append("        rCandidate_u := rControl_u[iCol] - (rStepSize_gamma * rGrad_g[iCol]);")
    lines.append("        rDelta_u[iCol] := rCandidate_u - rControl_u_prev[iCol];")
    lines.append("        rDelta_u[iCol] := MIN(rDeltaU_max[iCol], MAX(-rDeltaU_max[iCol], rDelta_u[iCol]));")
    lines.append("        rControl_u[iCol] := MIN(rU_max[iCol], MAX(rU_min[iCol], rControl_u_prev[iCol] + rDelta_u[iCol]));")
    lines.append("    END_FOR;")
    lines.append("END_FOR;")
    lines.append("")
    lines.append("(* Step D: Evaluation of terminal quadratic cost objective functional J *)")
    lines.append("rCostStateTerm    := 0.0;")
    lines.append("rCostInputTerm    := 0.0;")
    lines.append("rCostSlewTerm     := 0.0;")
    lines.append("rCostTerminalTerm := 0.0;")
    lines.append("FOR iCol := 1 TO 8 DO")
    lines.append("    rCostStateTerm    := rCostStateTerm + (rState_x[iCol] * rMatrixQ[iCol, iCol] * rState_x[iCol]);")
    lines.append("    rCostInputTerm    := rCostInputTerm + (rControl_u[iCol] * rMatrixR[iCol, iCol] * rControl_u[iCol]);")
    lines.append("    rCostSlewTerm     := rCostSlewTerm + (rDelta_u[iCol] * rMatrixS[iCol, iCol] * rDelta_u[iCol]);")
    lines.append("    rCostTerminalTerm := rCostTerminalTerm + (rState_x_pred[iCol] * rMatrixP[iCol, iCol] * rState_x_pred[iCol]);")
    lines.append("END_FOR;")
    lines.append("rMPC_CostObjectiveJ  := 0.50 * (rCostStateTerm + rCostInputTerm + rCostSlewTerm + rCostTerminalTerm);")
    lines.append("rMPC_SolveIterations := 10.0;")
    lines.append("")
    lines.append("(* Step E: Latch previous control vector for rate-of-change slew damping *)")
    lines.append("FOR iCol := 1 TO 8 DO")
    lines.append("    rControl_u_prev[iCol] := rControl_u[iCol];")
    lines.append("END_FOR;\n")
    
    return "\n".join(lines)

if __name__ == "__main__":
    code = generate_phase3()
    print(f"Phase 3 generated length: {len(code)} characters")
