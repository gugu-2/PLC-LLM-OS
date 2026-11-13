# Phase 3 generator: Receding-Horizon MPC Optimization via PGD
import os

def generate_phase3_mpc():
    lines = []
    lines.append("(* ========================================================================= *)")
    lines.append("(* PHASE 3: RECEDING-HORIZON MPC OPTIMIZATION WITH PGD & SLEW LIMITS         *)")
    lines.append("(* Multi-Objective Quadratic Cost: J = sum(e^T Q e) + sum(du^T R du) + P    *)")
    lines.append("(* ========================================================================= *)")
    lines.append("")
    
    # 1. Setpoint Trajectory Assignment
    lines.append("(* Define Target Process References (r[1..8]) for Steady-State Closed Loop *)")
    lines.append("aSetpoints_r[1] := 1850.0; (* [t] Target SAG Dynamic Total Charge Mass *)")
    lines.append("aSetpoints_r[2] := 18.50;  (* [m3] Target Internal Slurry Volumetric Holdup *)")
    lines.append("aSetpoints_r[3] := 52.00;  (* [deg] Optimal Cataracting Toe Impact Angle *)")
    lines.append("aSetpoints_r[4] := 23500.0;(* [kW] 28 MW GMD Peak Efficiency Power Target *)")
    lines.append("aSetpoints_r[5] := 55.00;  (* [%] Sump Steady-State Buffer Storage Level *)")
    lines.append("aSetpoints_r[6] := 1.280;  (* [t/m3] Hydrocyclone Overflow Target Slurry Density *)")
    lines.append("aSetpoints_r[7] := 1650.0; (* [t/h] Optimal Ball Mill Circulating Load *)")
    lines.append("aSetpoints_r[8] := 75.00;  (* [um] Beneficiation Flotation Target P80 Grind Size *)")
    lines.append("")

    # 2. Weighting Matrices Assignment
    lines.append("(* Assign Multi-Objective Quadratic Penalty Weights *)")
    q_weights = [
        (1, "0.0085", "Penalty on SAG charge mass deviation [t]"),
        (2, "0.0450", "Penalty on slurry pool holdup deviation [m3]"),
        (3, "0.1200", "Penalty on toe angle shift [deg]"),
        (4, "0.000025", "Penalty on GMD power draw deviation [kW]"),
        (5, "0.0150", "Penalty on sump level variance [%]"),
        (6, "45.000", "Penalty on overflow slurry density deviation [t/m3]"),
        (7, "0.00045", "Penalty on circulating load imbalance [t/h]"),
        (8, "0.8500", "High priority penalty on product P80 fineness [um]")
    ]
    for idx, val, comment in q_weights:
        lines.append(f"aWeight_Q[{idx}] := {val}; (* {comment} *)")
    lines.append("")

    r_weights = [
        (1, "0.00025", "Slew rate penalty on fresh ore feed belt [t/h]"),
        (2, "0.00080", "Slew rate penalty on SAG water valve [m3/h]"),
        (3, "45.0000", "Slew rate penalty on 28 MW GMD speed changes [rpm]"),
        (4, "0.00150", "Slew rate penalty on 1600 kW cyclone pump speed [rpm]"),
        (5, "0.00060", "Slew rate penalty on sump dilution water valve [m3/h]"),
        (6, "12.5000", "Slew penalty on opening/closing knife gate valves [count]"),
        (7, "0.02500", "Slew penalty on pebble splitter flap actuator [%]"),
        (8, "0.00200", "Slew penalty on ball mill dilution water valve [m3/h]")
    ]
    for idx, val, comment in r_weights:
        lines.append(f"aWeight_R[{idx}] := {val}; (* {comment} *)")
    lines.append("")

    s_weights = [
        (1, "15.00", "Soft constraint slack on max charge mass [2350 t]"),
        (2, "25.00", "Soft constraint slack on max slurry pool [35 m3]"),
        (3, "50.00", "Soft constraint slack on direct liner impact toe angle [>60 deg]"),
        (4, "0.005", "Soft constraint slack on GMD thermal overload [>26.5 MW]"),
        (5, "8.000", "Soft constraint slack on sump overflow risk [>85%]"),
        (6, "85.00", "Soft constraint slack on cyclone roping density [>1.55 t/m3]"),
        (7, "0.050", "Soft constraint slack on ball mill choking load [>2800 t/h]"),
        (8, "2.500", "Soft constraint slack on coarse flotation carryover [>95 um]")
    ]
    for idx, val, comment in s_weights:
        lines.append(f"aWeight_S[{idx}] := {val}; (* {comment} *)")
    lines.append("")

    p_weights = [
        (1, "0.0250", "Terminal state penalty on charge mass"),
        (2, "0.0850", "Terminal state penalty on slurry pool"),
        (3, "0.2500", "Terminal state penalty on toe angle"),
        (4, "0.00008", "Terminal state penalty on GMD power"),
        (5, "0.0450", "Terminal state penalty on sump level"),
        (6, "95.000", "Terminal state penalty on overflow density"),
        (7, "0.0012", "Terminal state penalty on circulating load"),
        (8, "1.8500", "Terminal state penalty on product P80")
    ]
    for idx, val, comment in p_weights:
        lines.append(f"aWeight_P[{idx}] := {val}; (* {comment} *)")
    lines.append("")

    # 3. Actuator Box & Slew Constraints
    lines.append("(* Physical Actuator Box Saturation Limits & Scan Slew Limits *)")
    u_limits = [
        (1, "0.0", "3400.0", "20.0", "Fresh ore feed rate [t/h]"),
        (2, "0.0", "1200.0", "10.0", "SAG feed dilution water [m3/h]"),
        (3, "0.0", "11.20", "0.04", "SAG mill rotational speed [rpm]"),
        (4, "200.0", "950.0", "8.00", "Cyclone feed slurry pump speed [rpm]"),
        (5, "0.0", "1500.0", "12.0", "Cyclone sump dilution water [m3/h]"),
        (6, "4.0", "14.0", "1.00", "Active hydrocyclones [count]"),
        (7, "0.0", "100.0", "2.50", "Pebble recycle splitter ratio [%]"),
        (8, "0.0", "600.0", "6.00", "Ball mill dilution water [m3/h]")
    ]
    for idx, u_min, u_max, slew_max, comment in u_limits:
        lines.append(f"aActuator_Min[{idx}]     := {u_min}; (* Lower box bound: {comment} *)")
        lines.append(f"aActuator_Max[{idx}]     := {u_max}; (* Upper box bound: {comment} *)")
        lines.append(f"aActuator_MaxSlew[{idx}] := {slew_max}; (* Max slew per 50ms scan: {comment} *)")
    lines.append("")

    # Initialize optimization candidate
    lines.append("(* Seed PGD Optimizer with Previous Dispatched Control Vector *)")
    for idx in range(1, 9):
        lines.append(f"aControl_u_opt[{idx}] := aControl_u[{idx}];")
    lines.append("")

    # 4. Projected Gradient Descent Optimization Loop
    lines.append("(* Execute 15 Projected Gradient Descent (PGD) Iterations *)")
    lines.append("rStepSize_alpha := 0.00035; (* Gradient descent step size *)")
    lines.append("FOR nIter := 1 TO 15 DO")
    lines.append("    (* Forward Predict State & Output Trajectory over Prediction Horizon Np = 10 *)")
    lines.append("    FOR j := 1 TO 8 DO")
    lines.append("        aState_pred[0, j] := aState_x[j];")
    lines.append("    END_FOR;")
    lines.append("")
    lines.append("    FOR nStep := 1 TO 10 DO")
    for i in range(1, 9):
        terms_apred = " + ".join([f"aMatrix_A[{i},{j}] * aState_pred[nStep - 1, {j}]" for j in range(1, 9)])
        terms_bpred = " + ".join([f"aMatrix_B[{i},{j}] * aControl_u_opt[{j}]" for j in range(1, 9)])
        terms_epred = f"aMatrix_E[{i},1] * aDisturbance_d[1] + aMatrix_E[{i},2] * aDisturbance_d[2]"
        lines.append(f"        aState_pred[nStep, {i}] := {terms_apred} +")
        lines.append(f"                                   {terms_bpred} +")
        lines.append(f"                                   {terms_epred};")
    lines.append("")
    for i in range(1, 9):
        terms_cpred = " + ".join([f"aMatrix_C[{i},{j}] * aState_pred[nStep, {j}]" for j in range(1, 9)])
        lines.append(f"        aOutput_pred[nStep, {i}] := {terms_cpred};")
    lines.append("    END_FOR;")
    lines.append("")
    lines.append("    (* Evaluate Multi-Objective Cost Functional *)")
    lines.append("    rCost_Tracking      := 0.0;")
    lines.append("    rCost_ControlEffort := 0.0;")
    lines.append("    rCost_Terminal      := 0.0;")
    lines.append("")
    lines.append("    FOR nStep := 1 TO 10 DO")
    for m in range(1, 9):
        lines.append(f"        rTempDiff := aOutput_pred[nStep, {m}] - aSetpoints_r[{m}];")
        lines.append(f"        rCost_Tracking := rCost_Tracking + (rTempDiff * rTempDiff * aWeight_Q[{m}]);")
    lines.append("    END_FOR;")
    lines.append("")
    for m in range(1, 9):
        lines.append(f"    rTempDiff := aControl_u_opt[{m}] - aControl_u_prev[{m}];")
        lines.append(f"    rCost_ControlEffort := rCost_ControlEffort + (rTempDiff * rTempDiff * aWeight_R[{m}]);")
    lines.append("")
    for m in range(1, 9):
        lines.append(f"    rTempDiff := aState_pred[10, {m}] - aSetpoints_r[{m}];")
        lines.append(f"    rCost_Terminal := rCost_Terminal + (rTempDiff * rTempDiff * aWeight_P[{m}]);")
    lines.append("")
    lines.append("    rCost_Total := rCost_Tracking + rCost_ControlEffort + rCost_Terminal;")
    lines.append("")
    lines.append("    (* Compute Analytical Gradient Vector wrt Control Vector: grad_J = sum(B^T C^T Q (y-r)) + R du *)")
    for m in range(1, 9):
        lines.append(f"    rTempGrad := 2.0 * aWeight_R[{m}] * (aControl_u_opt[{m}] - aControl_u_prev[{m}]);")
        lines.append("    FOR nStep := 1 TO 10 DO")
        for p in range(1, 9):
            lines.append(f"        rTempGrad := rTempGrad + (aMatrix_B[{p},{m}] * aWeight_Q[{p}] * (aOutput_pred[nStep, {p}] - aSetpoints_r[{p}]));")
        lines.append("    END_FOR;")
        lines.append(f"    aGradient_u[{m}] := rTempGrad;")
    lines.append("")
    lines.append("    (* Projected Gradient Descent Update Step with Line Search Scaling *)")
    for m in range(1, 9):
        lines.append(f"    aControl_u_opt[{m}] := aControl_u_opt[{m}] - (rStepSize_alpha * aGradient_u[{m}]);")
        lines.append(f"    (* Box Boundary Constraint Projection *)")
        lines.append(f"    aControl_u_opt[{m}] := LIMIT(aActuator_Min[{m}], aControl_u_opt[{m}], aActuator_Max[{m}]);")
        lines.append(f"    (* Slew Rate Boundary Projection *)")
        lines.append(f"    aControl_u_opt[{m}] := LIMIT(aControl_u_prev[{m}] - aActuator_MaxSlew[{m}], aControl_u_opt[{m}], aControl_u_prev[{m}] + aActuator_MaxSlew[{m}]);")
    lines.append("END_FOR;")
    lines.append("")

    # 5. Output Dispatching
    lines.append("(* Commit Optimized Actuator Vector to Active Control Registers If Auto Mode Permissive *)")
    lines.append("IF bAutoMode AND NOT bFault AND NOT bFrozenChargeTrip THEN")
    for m in range(1, 9):
        lines.append(f"    aControl_u[{m}] := aControl_u_opt[{m}];")
    lines.append("END_IF;")
    lines.append("")
    lines.append("(* Record Dispatched Controls for Slew Rate Filtering Next Cycle *)")
    for m in range(1, 9):
        lines.append(f"aControl_u_prev[{m}] := aControl_u[{m}];")
    lines.append("")

    return "\n".join(lines)

print("Phase 3 generator written.")
