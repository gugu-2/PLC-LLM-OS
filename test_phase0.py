# Python generator to build the full ST code and validate it
import os
import sys
import re

def build_phase0():
    st = []
    st.append("(* ==================================================================================================== *)\n")
    st.append("(* PHASE 0: SYSTEM INITIALIZATION & DISCRETE CYBER-PHYSICAL STATE-SPACE MATRIX INITIALIZATION           *)\n")
    st.append("(* First-Principles Discretization at Ts = 0.010 [s] (10 [ms] deterministic scan cycle)                  *)\n")
    st.append("(* ==================================================================================================== *)\n")
    st.append("IF NOT bFirstScanDone THEN\n")
    st.append("    (* ------------------------------------------------------------------------------------------------ *)\n")
    st.append("    (* 6x6 Discrete Plant Transition Matrix A: Headbox Hydrodynamics, Pneumatics & Retention            *)\n")
    st.append("    (* x1: Total Head [mm H2O], x2: Pond Level [mm], x3: Jet-Wire Diff [m/min],                         *)\n")
    st.append("    (* x4: Mean Basis Weight [g/m2], x5: Fiber Consistency [g/L], x6: Air Pad Pressure [kPa]            *)\n")
    st.append("    (* ------------------------------------------------------------------------------------------------ *)\n")
    
    # matA elements
    a_vals = [
        [0.9820, 0.0145, -0.0035, 0.0012, 0.0085, 0.1019],
        [-0.0042, 0.9965, -0.0018, 0.0005, -0.0010, -0.0028],
        [0.0215, 0.0022, 0.9650, -0.0045, -0.0030, 0.0185],
        [0.0068, 0.0015, 0.0125, 0.9880, 0.0450, 0.0035],
        [0.0018, -0.0025, 0.0005, 0.0002, 0.9780, 0.0012],
        [-0.0085, -0.0450, 0.0010, 0.0000, 0.0000, 0.9850]
    ]
    a_comments = [
        "Head damping, pond level effect, jet draw, slurry friction, consistency viscosity, pneumatic air coupling",
        "Slice discharge outflow, liquid inventory retention, jet draw, fiber drainage, dilution, air suppression",
        "Torricelli head sensitivity d(v_jet)/d(H), pond head, velocity damping, web drag, slurry drag, air accel",
        "Mass flow head gain, level head, jet-wire formation retention, fourdrinier transport, fiber mass, air pad",
        "Recirculation mixing, pond dilution, jet draw effect, wire white water return, CSTR mixing, air pad",
        "Pneumatic back-pressure, Boyle-Mariotte pond displacement compression, jet draw, negligible, leakage damping"
    ]
    for i in range(6):
        st.append(f"    (* Row {i}: {a_comments[i]} *)\n")
        for j in range(6):
            st.append(f"    matA[{i}, {j}] := {a_vals[i][j]:.4f};\n")

    st.append("\n    (* ------------------------------------------------------------------------------------------------ *)\n")
    st.append("    (* 6x5 Actuator Input Mapping Matrix B: Fan Pump, Air Cushion, Slice Lip, Dilution, Overflow        *)\n")
    st.append("    (* u1: Fan Pump VFD [%], u2: Air Pad Proportional Valve [%], u3: Slice Lip Opening [mm],             *)\n")
    st.append("    (* u4: Dilution Header Valve [%], u5: Stock Overflow Bypass Valve [%]                               *)\n")
    st.append("    (* ------------------------------------------------------------------------------------------------ *)\n")
    b_vals = [
        [0.4850, 0.3120, -0.1420, 0.0650, -0.0820],
        [0.1850, -0.0250, -0.2150, 0.0420, -0.1650],
        [0.2150, 0.1680, -0.0850, 0.0280, -0.0380],
        [0.0950, 0.0120, 0.3450, -0.1850, -0.0450],
        [0.0220, 0.0015, 0.0140, -0.2450, 0.0180],
        [0.0080, 0.5250, -0.0180, 0.0020, -0.0120]
    ]
    b_comments = [
        "Fan pump pressure delivery, air pad pressurization, slice opening pressure drop, dilution, overflow bypass",
        "Fan pump volumetric filling, air pad compression, slice discharge outflow, dilution inflow, overflow drain",
        "Fan pump jet acceleration, air cushion boost, slice opening vena contracta, dilution fluid, overflow",
        "Fan pump slurry delivery, air pad velocity, slice lip gap mass flow, dilution basis weight reduction, overflow",
        "Primary thick stock feed, negligible, slice flow consistency, white water profiling dilution, bypass",
        "Acoustic water hammer, pneumatic proportional air charge/bleed, slice surge displacement, negligible, vent"
    ]
    for i in range(6):
        st.append(f"    (* Row {i}: {b_comments[i]} *)\n")
        for j in range(5):
            st.append(f"    matB[{i}, {j}] := {b_vals[i][j]:.4f};\n")

    st.append("\n    (* ------------------------------------------------------------------------------------------------ *)\n")
    st.append("    (* 6x6 Measurement Output Mapping Matrix C: Voted Transmitters & Reconstructed Observables          *)\n")
    st.append("    (* ------------------------------------------------------------------------------------------------ *)\n")
    c_vals = [
        [1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 1.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.0, 1.0]
    ]
    for i in range(6):
        for j in range(6):
            st.append(f"    matC[{i}, {j}] := {c_vals[i][j]:.4f};\n")

    st.append("\n    (* ------------------------------------------------------------------------------------------------ *)\n")
    st.append("    (* 6x5 Direct Feedthrough Matrix D: Acoustic & Mechanical High-Frequency Cross-Coupling              *)\n")
    st.append("    (* ------------------------------------------------------------------------------------------------ *)\n")
    d_vals = [
        [0.0150, 0.0080, 0.0000, 0.0000, -0.0020],
        [0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
        [0.0080, 0.0050, 0.0000, 0.0000, 0.0000],
        [0.0000, 0.0000, 0.0120, 0.0000, 0.0000],
        [0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
        [0.0000, 0.0250, 0.0000, 0.0000, 0.0000]
    ]
    for i in range(6):
        for j in range(5):
            st.append(f"    matD[{i}, {j}] := {d_vals[i][j]:.4f};\n")

    st.append("\n    (* ------------------------------------------------------------------------------------------------ *)\n")
    st.append("    (* 6x6 Luenberger Observer Innovation Gain Matrix L: Asymptotic State Convergence & Noise Filtering *)\n")
    st.append("    (* ------------------------------------------------------------------------------------------------ *)\n")
    l_vals = [
        [0.3450, 0.0210, 0.0180, 0.0040, 0.0080, 0.0520],
        [0.0180, 0.2850, 0.0050, 0.0020, 0.0040, -0.0120],
        [0.0420, 0.0080, 0.3650, -0.0150, -0.0050, 0.0350],
        [0.0120, 0.0040, 0.0220, 0.3120, 0.0450, 0.0060],
        [0.0050, -0.0030, 0.0020, 0.0180, 0.2650, 0.0010],
        [0.0380, -0.0450, 0.0120, 0.0010, 0.0010, 0.3850]
    ]
    for i in range(6):
        for j in range(6):
            st.append(f"    matL[{i}, {j}] := {l_vals[i][j]:.4f};\n")

    st.append("\n    (* ------------------------------------------------------------------------------------------------ *)\n")
    st.append("    (* Model Predictive Control (MPC) Weighting Matrices: Q, R, S, P, Saturation & Slew Bounds         *)\n")
    st.append("    (* ------------------------------------------------------------------------------------------------ *)\n")
    q_vals = [1.85, 2.45, 3.80, 4.50, 1.35, 2.80]
    for i in range(6):
        st.append(f"    vecQ_weight[{i}] := {q_vals[i]:.2f};\n")
    p_vals = [3.70, 4.90, 7.60, 9.00, 2.70, 5.60]
    for i in range(6):
        st.append(f"    vecP_terminal[{i}] := {p_vals[i]:.2f};\n")
    r_vals = [0.35, 0.42, 0.85, 0.28, 0.32]
    for i in range(5):
        st.append(f"    vecR_weight[{i}] := {r_vals[i]:.2f};\n")
    s_vals = [0.65, 0.80, 1.45, 0.50, 0.55]
    for i in range(5):
        st.append(f"    vecS_rate_weight[{i}] := {s_vals[i]:.2f};\n")
    u_min_vals = [15.0, -100.0, 6.0, 5.0, 2.0]
    u_max_vals = [100.0, 100.0, 40.0, 98.0, 95.0]
    u_slew_vals = [1.50, 5.00, 0.20, 2.50, 2.00]
    for i in range(5):
        st.append(f"    vecU_min[{i}] := {u_min_vals[i]:.2f};\n")
        st.append(f"    vecU_max[{i}] := {u_max_vals[i]:.2f};\n")
        st.append(f"    vecU_slewMax[{i}] := {u_slew_vals[i]:.2f};\n")

    st.append("\n    (* ------------------------------------------------------------------------------------------------ *)\n")
    st.append("    (* 64 Cross-Direction (CD) Spatial Cross-Coupling Toeplitz Matrix G Initialization                *)\n")
    st.append("    (* Gaussian Dispersion Attenuation Kernel: g0 = 1.000, g1 = 0.485, g2 = 0.182, g3 = 0.045, g4 = 0.008 *)\n")
    st.append("    (* ------------------------------------------------------------------------------------------------ *)\n")
    st.append("    FOR iAct := 1 TO 64 DO\n")
    st.append("        FOR jAct := 1 TO 64 DO\n")
    st.append("            IF iAct = jAct THEN\n")
    st.append("                matG_Toeplitz[iAct, jAct] := 1.0000;\n")
    st.append("            ELSIF ABS(iAct - jAct) = 1 THEN\n")
    st.append("                matG_Toeplitz[iAct, jAct] := 0.4850;\n")
    st.append("            ELSIF ABS(iAct - jAct) = 2 THEN\n")
    st.append("                matG_Toeplitz[iAct, jAct] := 0.1820;\n")
    st.append("            ELSIF ABS(iAct - jAct) = 3 THEN\n")
    st.append("                matG_Toeplitz[iAct, jAct] := 0.0450;\n")
    st.append("            ELSIF ABS(iAct - jAct) = 4 THEN\n")
    st.append("                matG_Toeplitz[iAct, jAct] := 0.0080;\n")
    st.append("            ELSE\n")
    st.append("                matG_Toeplitz[iAct, jAct] := 0.0000;\n")
    st.append("            END_IF;\n")
    st.append("        END_FOR;\n")
    st.append("        arrTargetBasisWeight_CD[iAct] := 80.0;\n")
    st.append("        arrIntegralError_CD[iAct] := 0.0;\n")
    st.append("        arrFilteredError_CD[iAct] := 0.0;\n")
    st.append("        arrSliceSpindleCmd_um[iAct] := 12500.0;\n")
    st.append("        arrSliceSpindlePrev_um[iAct] := 12500.0;\n")
    st.append("        arrThermalModelTemp_degC[iAct] := 65.0;\n")
    st.append("        arrThermalHeater_PowerCmd_pct[iAct] := 38.8;\n")
    st.append("    END_FOR;\n")

    st.append("\n    (* Initialize State Vector Estimates to Plausible Operating Nominal Baseline *)\n")
    st.append("    vecX_hat[0] := 16200.0; (* 16,200 [mm H2O] total head *)\n")
    st.append("    vecX_hat[1] := 320.0;   (* 320 [mm] pond level *)\n")
    st.append("    vecX_hat[2] := 45.0;    (* +45 [m/min] jet-wire lead (1.025 ratio at 1800 m/min = +45 m/min) *)\n")
    st.append("    vecX_hat[3] := 80.0;    (* 80 [g/m2] finished basis weight *)\n")
    st.append("    vecX_hat[4] := 7.5;     (* 7.5 [g/L] (0.75%) headbox fiber consistency *)\n")
    st.append("    vecX_hat[5] := 155.8;   (* ~155.8 [kPa] air pad compressed cushion *)\n")
    st.append("    FOR iIdx := 0 TO 5 DO\n")
    st.append("        vecX_pred[iIdx] := vecX_hat[iIdx];\n")
    st.append("        vecX[iIdx] := vecX_hat[iIdx];\n")
    st.append("    END_FOR;\n")
    st.append("    vecU_prev[0] := 68.5;   (* Fan pump speed [%] *)\n")
    st.append("    vecU_prev[1] := 12.0;   (* Air valve net charge [%] *)\n")
    st.append("    vecU_prev[2] := 14.5;   (* Mean slice lip opening [mm] *)\n")
    st.append("    vecU_prev[3] := 42.0;   (* Dilution header valve [%] *)\n")
    st.append("    vecU_prev[4] := 18.0;   (* Stock recirculation overflow [%] *)\n")
    st.append("    FOR mIdx := 0 TO 4 DO\n")
    st.append("        vecU[mIdx] := vecU_prev[mIdx];\n")
    st.append("        vecU_target[mIdx] := vecU_prev[mIdx];\n")
    st.append("    END_FOR;\n")
    st.append("    bFirstScanDone := TRUE;\n")
    st.append("END_IF;\n\n")
    return "".join(st)

print("build_phase0 len:", len(build_phase0()))
