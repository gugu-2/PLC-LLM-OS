# copper_flotation_gen/part3_phase0_init.py

def get_phase0_init():
    lines = []
    lines.append("(* ==================================================================================================== *)")
    lines.append("(* PHASE 0: SYSTEM INITIALIZATION & DISCRETE CYBER-PHYSICAL STATE-SPACE MATRIX INITIALIZATION           *)")
    lines.append("(* First-Principles Discretization at Ts = 0.020 [s] (20 [ms] deterministic scan cycle)                  *)")
    lines.append("(* ==================================================================================================== *)")
    lines.append("IF NOT bFirstScanDone THEN")
    lines.append("    (* ------------------------------------------------------------------------------------------------ *)")
    lines.append("    (* 8x8 Discrete Plant Transition Matrix A: Inter-Cell Slurry Hydraulics, Phase Kinetics & Holdup  *)")
    lines.append("    (* ------------------------------------------------------------------------------------------------ *)")
    
    # 8x8 matrix A values
    matA_vals = [
        [0.9842, 0.0045, 0.0008, -0.0125,  0.0350,  0.0185, -0.0020,  0.0015],
        [0.0182, 0.9765, 0.0062, -0.0095,  0.0280,  0.0142, -0.0015,  0.0022],
        [0.0035, 0.0245, 0.9710, -0.0065,  0.0210,  0.0110, -0.0008,  0.0031],
        [-0.0085, -0.0055, -0.0032, 0.9520, 0.0840,  0.1250,  0.0140, -0.0080],
        [0.0012, 0.0015, 0.0009, -0.0042,  0.9250,  0.1850, -0.0035,  0.0028],
        [0.0005, 0.0008, 0.0004, -0.0025,  0.0420,  0.8950, -0.0018,  0.0012],
        [-0.0028, -0.0019, -0.0011, 0.0185, -0.0150, -0.0380, 0.9880, -0.0220],
        [0.0032, 0.0041, 0.0055, -0.0140,  0.0220,  0.0450, -0.0185,  0.9915]
    ]
    for i in range(8):
        for j in range(8):
            lines.append(f"    matA[{i}, {j}] := {matA_vals[i][j]:.4f};")

    lines.append("")
    lines.append("    (* ------------------------------------------------------------------------------------------------ *)")
    lines.append("    (* 8x6 Actuator Input Mapping Matrix B: Dart Valves, Air Valve, PAX Collector & MIBC Frother Pumps *)")
    lines.append("    (* ------------------------------------------------------------------------------------------------ *)")
    matB_vals = [
        [-0.2450,  0.0380,  0.0042,  0.0520,  0.0012,  0.0085],
        [ 0.1850, -0.2850,  0.0410,  0.0450,  0.0025,  0.0072],
        [ 0.0250,  0.1980, -0.3120,  0.0380,  0.0045,  0.0061],
        [-0.0650, -0.0480, -0.0320,  0.2850, -0.0120,  0.1950],
        [ 0.0085,  0.0062,  0.0041,  0.3450,  0.0018,  0.0820],
        [ 0.0042,  0.0031,  0.0018,  0.4250,  0.0005,  0.0150],
        [-0.0180, -0.0140, -0.0095, -0.0850,  0.1450, -0.0620],
        [ 0.0120,  0.0180,  0.0240,  0.0920,  0.1820,  0.0750]
    ]
    for i in range(8):
        for j in range(6):
            lines.append(f"    matB[{i}, {j}] := {matB_vals[i][j]:.4f};")

    lines.append("")
    lines.append("    (* ------------------------------------------------------------------------------------------------ *)")
    lines.append("    (* 6x8 Measurement Mapping Matrix C: Voted Sensory Observation Projections                        *)")
    lines.append("    (* ------------------------------------------------------------------------------------------------ *)")
    matC_vals = [
        [1.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
        [0.0000, 1.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
        [0.0000, 0.0000, 1.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
        [0.0000, 0.0000, 0.0000, 1.0000, 0.0000, 0.0000, 0.0000, 0.0000],
        [0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 1.0000, 0.0000, 0.0000],
        [0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 1.0000, 0.0000]
    ]
    for i in range(6):
        for j in range(8):
            lines.append(f"    matC[{i}, {j}] := {matC_vals[i][j]:.4f};")

    lines.append("")
    lines.append("    (* ------------------------------------------------------------------------------------------------ *)")
    lines.append("    (* 6x6 Direct Feedthrough Transmission Matrix D: Fast Pressure-Velocity Acoustic Coupling         *)")
    lines.append("    (* ------------------------------------------------------------------------------------------------ *)")
    matD_vals = [
        [ 0.0050,  0.0000,  0.0000,  0.0020,  0.0000,  0.0000],
        [ 0.0010,  0.0050,  0.0000,  0.0020,  0.0000,  0.0000],
        [ 0.0005,  0.0012,  0.0050,  0.0018,  0.0000,  0.0000],
        [ 0.0000,  0.0000,  0.0000,  0.0150,  0.0000,  0.0080],
        [ 0.0000,  0.0000,  0.0000,  0.0450,  0.0000,  0.0010],
        [ 0.0000,  0.0000,  0.0000, -0.0050,  0.0080, -0.0025]
    ]
    for i in range(6):
        for j in range(6):
            lines.append(f"    matD[{i}, {j}] := {matD_vals[i][j]:.4f};")

    lines.append("")
    lines.append("    (* ------------------------------------------------------------------------------------------------ *)")
    lines.append("    (* 8x6 Luenberger Observer Innovation Gain Matrix L: Steady-State Kalman Filter Solution          *)")
    lines.append("    (* ------------------------------------------------------------------------------------------------ *)")
    matL_vals = [
        [0.2850, 0.0320, 0.0080, 0.0150, 0.0040, 0.0010],
        [0.0380, 0.2720, 0.0290, 0.0120, 0.0050, 0.0015],
        [0.0090, 0.0410, 0.2650, 0.0080, 0.0060, 0.0020],
        [0.0210, 0.0180, 0.0120, 0.3150, 0.0450, 0.0080],
        [0.0080, 0.0090, 0.0070, 0.0520, 0.2450, 0.0035],
        [0.0030, 0.0040, 0.0030, 0.0850, 0.3850, 0.0020],
        [0.0015, 0.0020, 0.0018, 0.0120, 0.0080, 0.3450],
        [0.0040, 0.0060, 0.0080, 0.0250, 0.0320, 0.1850]
    ]
    for i in range(8):
        for j in range(6):
            lines.append(f"    matL[{i}, {j}] := {matL_vals[i][j]:.4f};")

    lines.append("")
    lines.append("    (* ------------------------------------------------------------------------------------------------ *)")
    lines.append("    (* 6x6 Inter-Cell Dart Valve Hydrostatic Cross-Coupling Matrix M_hydro                             *)")
    lines.append("    (* ------------------------------------------------------------------------------------------------ *)")
    matM_vals = [
        [ 1.0000, -0.4200,  0.1150, -0.0350,  0.0120, -0.0040],
        [-0.3850,  1.0000, -0.4450,  0.1250, -0.0420,  0.0150],
        [ 0.0950, -0.3950,  1.0000, -0.4650,  0.1380, -0.0480],
        [-0.0280,  0.1080, -0.4120,  1.0000, -0.4850,  0.1450],
        [ 0.0080, -0.0320,  0.1180, -0.4250,  1.0000, -0.5100],
        [-0.0020,  0.0090, -0.0380,  0.1280, -0.4450,  1.0000]
    ]
    for i in range(6):
        for j in range(6):
            lines.append(f"    matM_hydro[{i}, {j}] := {matM_vals[i][j]:.4f};")

    lines.append("")
    lines.append("    (* ------------------------------------------------------------------------------------------------ *)")
    lines.append("    (* Quadratic Cost Penalty Weights: State Deviations Q, Actuators R, Slew R_delta, Terminal P       *)")
    lines.append("    (* ------------------------------------------------------------------------------------------------ *)")
    q_weights = [1.25, 1.45, 1.85, 2.40, 0.85, 1.10, 4.50, 3.80]
    for i in range(8):
        lines.append(f"    vecQ_weight[{i}] := {q_weights[i]:.4f};")
        lines.append(f"    vecP_terminal[{i}] := {q_weights[i] * 2.8:.4f};")

    r_weights = [0.45, 0.45, 0.55, 0.35, 0.75, 0.85]
    r_delta_weights = [1.80, 1.80, 2.20, 1.50, 3.20, 3.50]
    for i in range(6):
        lines.append(f"    vecR_weight[{i}] := {r_weights[i]:.4f};")
        lines.append(f"    vecR_delta_weight[{i}] := {r_delta_weights[i]:.4f};")

    lines.append("")
    lines.append("    (* ------------------------------------------------------------------------------------------------ *)")
    lines.append("    (* Actuator Physical Saturation & Slew Rate Limits per Ts = 0.020 [s] Cycle                         *)")
    lines.append("    (* ------------------------------------------------------------------------------------------------ *)")
    slew_limits = [0.20, 0.20, 0.20, 0.30, 0.10, 0.10] # Dart valves: 10%/s => 0.20%/cycle; Air: 15%/s; Reagents: 5%/s
    for i in range(6):
        lines.append(f"    vecU_min[{i}] := 0.0;")
        lines.append(f"    vecU_max[{i}] := 100.0;")
        lines.append(f"    vecU_slewMax[{i}] := {slew_limits[i]:.4f};")
        lines.append(f"    rDartValve_StationaryTime_s[{i}] := 0.0;")
        lines.append(f"    bDartValve_DitherActive[{i}] := FALSE;")

    lines.append("")
    lines.append("    (* ------------------------------------------------------------------------------------------------ *)")
    lines.append("    (* Nominal Process Setpoints & Initial State Vector Allocations                                     *)")
    lines.append("    (* ------------------------------------------------------------------------------------------------ *)")
    target_x = [1100.0, 1050.0, 1000.0, 150.0, 16.5, 1.25, 28.5, 88.5]
    for i in range(8):
        lines.append(f"    vecX_target[{i}] := {target_x[i]:.2f};")
        lines.append(f"    vecX[{i}] := {target_x[i]:.2f};")
        lines.append(f"    vecX_hat[{i}] := {target_x[i]:.2f};")
        lines.append(f"    vecX_pred[{i}] := {target_x[i]:.2f};")

    target_u = [52.5, 54.0, 56.5, 48.0, 42.0, 38.0]
    for i in range(6):
        lines.append(f"    vecU_target[{i}] := {target_u[i]:.2f};")
        lines.append(f"    vecU[{i}] := {target_u[i]:.2f};")
        lines.append(f"    vecU_prev[{i}] := {target_u[i]:.2f};")
        lines.append(f"    vecU_rate[{i}] := 0.0;")

    lines.append("")
    lines.append("    (* Mark First Scan Initialization Sequence Complete *)")
    lines.append("    bFirstScanDone := TRUE;")
    lines.append("END_IF;")
    return "\n".join(lines)
