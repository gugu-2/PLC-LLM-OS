# gen_part5.py

part5 = """(* ==================================================================================================== *)
(* PHASE 3: RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) WITH PROJECTED GRADIENT DESCENT (PGD)       *)
(* Configuration: Horizon N = 5 Steps (100 [ms]), 10 Unrolled PGD Iterations, Slew & Physical Bounds    *)
(* Actuators: u[0]=CV_H2 [%], u[1]=CV_Cl2 [%], u[2]=CV_Water [%], u[3]=CV_Brine [%], u[4]=I_rect [kA]     *)
(* Adjoint Sensitivity Backpropagation: Costates lambda[k] & Analytical Gradient w.r.t Control Action   *)
(* ==================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------- *)
(* Step 1: Dynamic State Trajectory Setpoint Adaptation Based on FSM State & Electrolyzer Regime        *)
(* ---------------------------------------------------------------------------------------------------- *)
IF eState = 1 THEN
    (* State 1: Nitrogen Purge & Leak Check - Depressurized Balanced State *)
    vecX_target[0] := 0.0;     (* Target DP: 0.0 mbar *)
    vecX_target[1] := 0.100;   (* Target Cl2 Purge Pressure: 0.10 bar *)
    vecX_target[2] := 0.100;   (* Target H2 Purge Pressure: 0.10 bar *)
    vecX_target[3] := 305.0;   (* Saturated Inflow Baseline [g/L] *)
    vecX_target[4] := 30.0;    (* Weak Caustic Inventory [wt%] *)
    vecX_target[5] := 25.0;    (* Cold Purge Temperature [deg C] *)
ELSIF eState = 2 THEN
    (* State 2: Brine Warmup Circulation - Elevating Stack Temperature Without Current *)
    vecX_target[0] := 0.0;     (* Balanced Hydraulic Head *)
    vecX_target[1] := 0.020;   (* Open Manifolds *)
    vecX_target[2] := 0.020;   (* Open Manifolds *)
    vecX_target[3] := 300.0;   (* Fresh Brine Saturation [g/L] *)
    vecX_target[4] := 30.5;    (* Caustic [wt%] *)
    vecX_target[5] := 82.0;    (* Pre-Energization Target Temperature [deg C] *)
ELSIF eState = 3 THEN
    (* State 3: Rectifier Polarization Current Initialization (5% Load, 3.5 kA) *)
    vecX_target[0] := 5.0;     (* Establish Positive Differential Pressure [mbar] *)
    vecX_target[1] := 0.080;   (* Initial Cl2 Blanket [bar] *)
    vecX_target[2] := 0.085;   (* Initial H2 Blanket [bar] *)
    vecX_target[3] := 285.0;   (* Slight Depletion [g/L] *)
    vecX_target[4] := 31.0;    (* Caustic Beginning to Form [wt%] *)
    vecX_target[5] := 84.0;    (* Warm Electrolyte [deg C] *)
ELSIF eState = 4 THEN
    (* State 4: Ramp Current to 25% Low Load (~17.5 kA) *)
    vecX_target[0] := 18.0;    (* Transitional Differential Pressure [mbar] *)
    vecX_target[1] := 0.160;   (* Cl2 Header Pressure [bar] *)
    vecX_target[2] := 0.178;   (* H2 Header Pressure [bar] *)
    vecX_target[3] := 240.0;   (* Depleted Brine Transition [g/L] *)
    vecX_target[4] := 32.0;    (* Caustic Product [wt%] *)
    vecX_target[5] := 86.0;    (* Approaching Operating Temp [deg C] *)
ELSIF eState = 5 THEN
    (* State 5: Pressure Equilibration Transition - Locking Tight +/- 1.5 mbar DP *)
    vecX_target[0] := 30.0;    (* Nominal Baseload DP Setpoint [mbar] *)
    vecX_target[1] := 0.220;   (* Cl2 Header Pressure [bar] *)
    vecX_target[2] := 0.250;   (* H2 Header Pressure [bar] *)
    vecX_target[3] := 215.0;   (* Depleted Brine [g/L] *)
    vecX_target[4] := 32.2;    (* Caustic [wt%] *)
    vecX_target[5] := 87.5;    (* Near Steady State [deg C] *)
ELSIF eState = 6 THEN
    (* State 6: Nominal Baseload Production (Full Load, 2.5 kA/m2, 67.5 kA) *)
    vecX_target[0] := 30.0;    (* Strict DP Setpoint: 30.0 mbar *)
    vecX_target[1] := 0.250;   (* Cl2 Header Steady Pressure: 0.250 bar *)
    vecX_target[2] := 0.280;   (* H2 Header Steady Pressure: 0.280 bar *)
    vecX_target[3] := 205.0;   (* Optimal Anolyte Outlet Brine: 205.0 g/L *)
    vecX_target[4] := 32.5;    (* Commercial High-Purity Caustic: 32.5 wt% *)
    vecX_target[5] := 88.0;    (* Optimal Cell Thermal Equilibrium: 88.0 deg C *)
ELSIF eState = 7 THEN
    (* State 7: Dedicated Caustic Concentration Control Loop Tuning *)
    vecX_target[0] := 30.0;    (* Maintain Strict DP *)
    vecX_target[1] := 0.250;
    vecX_target[2] := 0.280;
    vecX_target[3] := 205.0;
    vecX_target[4] := 32.5;    (* High Priority Focus on 32.5 wt% NaOH *)
    vecX_target[5] := 88.0;
ELSIF eState = 8 THEN
    (* State 8: Dedicated Brine Depletion Feed Control Loop Tuning *)
    vecX_target[0] := 30.0;
    vecX_target[1] := 0.250;
    vecX_target[2] := 0.280;
    vecX_target[3] := 205.0;   (* High Priority Focus on 205.0 g/L NaCl *)
    vecX_target[4] := 32.5;
    vecX_target[5] := 88.0;
ELSIF eState = 9 THEN
    (* State 9: Membrane Health & Specific Resistance Diagnostic Sweep *)
    vecX_target[0] := 30.0;
    vecX_target[1] := 0.250;
    vecX_target[2] := 0.280;
    vecX_target[3] := 215.0;   (* Slightly Richer Brine to Reduce Membrane IR *)
    vecX_target[4] := 32.0;    (* Optimal Hydration Caustic Concentration *)
    vecX_target[5] := 88.5;    (* Elevated Temp to Lower Membrane Resistance *)
ELSIF eState = 10 THEN
    (* State 10: Controlled Ramp-Down Turndown Sequence *)
    vecX_target[0] := 15.0;    (* Decreasing DP to Match Lower Gas Flow Rates *)
    vecX_target[1] := 0.150;
    vecX_target[2] := 0.165;
    vecX_target[3] := 240.0;
    vecX_target[4] := 31.5;
    vecX_target[5] := 82.0;
ELSIF eState = 11 THEN
    (* State 11: Automated Shutdown Polarization Hold (5% Current, 3.5 kA) *)
    vecX_target[0] := 5.0;
    vecX_target[1] := 0.050;
    vecX_target[2] := 0.055;
    vecX_target[3] := 280.0;
    vecX_target[4] := 30.5;
    vecX_target[5] := 75.0;
ELSIF eState = 12 OR eState = 13 THEN
    (* State 12 & 13: Emergency Trip & Post-Trip Inert Blanket *)
    vecX_target[0] := 0.0;     (* Zero Differential Pressure to Relieve Stress *)
    vecX_target[1] := 0.020;   (* Low Inert Nitrogen Header Pressure *)
    vecX_target[2] := 0.020;   (* Low Inert Nitrogen Header Pressure *)
    vecX_target[3] := 290.0;
    vecX_target[4] := 30.0;
    vecX_target[5] := 50.0;    (* Cooling Stack *)
ELSE
    (* Default Baseline Setpoint *)
    vecX_target[0] := 30.0;
    vecX_target[1] := 0.250;
    vecX_target[2] := 0.280;
    vecX_target[3] := 205.0;
    vecX_target[4] := 32.5;
    vecX_target[5] := 88.0;
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* Step 2: Initialize Receding Horizon Trajectory: State Seed & Actuator Warm Start                     *)
(* ---------------------------------------------------------------------------------------------------- *)
FOR iIdx := 0 TO 5 DO
    trajX_mpc[0, iIdx] := vecX_hat[iIdx];
END_FOR;

FOR kStep := 0 TO 4 DO
    FOR mIdx := 0 TO 4 DO
        trajU_mpc[kStep, mIdx] := vecU[mIdx];
    END_FOR;
END_FOR;

(* ---------------------------------------------------------------------------------------------------- *)
(* Step 3: Unrolled Projected Gradient Descent (PGD) Solver Core (10 Full Unrolled Iterations)          *)
(* Solves Quadratic Program: min 1/2 sum(e^T Q e + u^T R u + du^T R_delta du) + 1/2 e_N^T P e_N         *)
(* ---------------------------------------------------------------------------------------------------- *)
FOR iIter := 0 TO 9 DO
    (* 3a. Forward Simulation Across Receding Horizon Steps k = 0 to 4 *)
    FOR kStep := 0 TO 4 DO
        FOR iIdx := 0 TO 5 DO
            rTempSum := 0.0;
            FOR jIdx := 0 TO 5 DO
                rTempSum := rTempSum + (matA[iIdx, jIdx] * trajX_mpc[kStep, jIdx]);
            END_FOR;
            FOR mIdx := 0 TO 4 DO
                rTempSum := rTempSum + (matB[iIdx, mIdx] * trajU_mpc[kStep, mIdx]);
            END_FOR;
            trajX_mpc[kStep + 1, iIdx] := rTempSum;
        END_FOR;
    END_FOR;

    (* 3b. Evaluate Objective Function Quadratic Cost *)
    rMpc_AccumulatedCost := 0.0;
    FOR kStep := 0 TO 4 DO
        (* State Tracking Cost Term *)
        FOR iIdx := 0 TO 5 DO
            rTempDiff := trajX_mpc[kStep, iIdx] - vecX_target[iIdx];
            rMpc_AccumulatedCost := rMpc_AccumulatedCost + (vecQ_weight[iIdx] * rTempDiff * rTempDiff);
        END_FOR;
        (* Actuator Effort & Slew Rate Cost Terms *)
        FOR mIdx := 0 TO 4 DO
            rTempDiff := trajU_mpc[kStep, mIdx];
            rMpc_AccumulatedCost := rMpc_AccumulatedCost + (vecR_weight[mIdx] * rTempDiff * rTempDiff);
            rTempDeltaU := trajU_mpc[kStep, mIdx] - vecU_prev[mIdx];
            rMpc_AccumulatedCost := rMpc_AccumulatedCost + (vecR_delta_weight[mIdx] * rTempDeltaU * rTempDeltaU);
        END_FOR;
    END_FOR;
    (* Terminal Horizon Penalty Cost Term *)
    FOR iIdx := 0 TO 5 DO
        rTempDiff := trajX_mpc[5, iIdx] - vecX_target[iIdx];
        rMpc_AccumulatedCost := rMpc_AccumulatedCost + (vecP_terminal[iIdx] * rTempDiff * rTempDiff);
    END_FOR;

    (* 3c. Terminal Adjoint Costate Vector Initialization: lambda[N] = 2 * P * (x[N] - x_target) *)
    FOR iIdx := 0 TO 5 DO
        trajLambda[5, iIdx] := 2.0 * vecP_terminal[iIdx] * (trajX_mpc[5, iIdx] - vecX_target[iIdx]);
    END_FOR;

    (* 3d. Backward Adjoint Sensitivity Propagation & Control Gradient Extraction *)
    FOR kStep := 4 TO 0 BY -1 DO
        (* Costate Backpropagation: lambda[k] = A^T * lambda[k+1] + 2 * Q * (x[k] - x_target) *)
        FOR iIdx := 0 TO 5 DO
            rTempSum := 0.0;
            FOR jIdx := 0 TO 5 DO
                rTempSum := rTempSum + (matA[jIdx, iIdx] * trajLambda[kStep + 1, jIdx]);
            END_FOR;
            trajLambda[kStep, iIdx] := rTempSum + (2.0 * vecQ_weight[iIdx] * (trajX_mpc[kStep, iIdx] - vecX_target[iIdx]));
        END_FOR;

        (* Control Gradient: grad_J[k] = B^T * lambda[k+1] + 2 * R * u[k] + 2 * R_delta * (u[k] - u_prev) *)
        FOR mIdx := 0 TO 4 DO
            rTempSum := 0.0;
            FOR iIdx := 0 TO 5 DO
                rTempSum := rTempSum + (matB[iIdx, mIdx] * trajLambda[kStep + 1, iIdx]);
            END_FOR;
            trajGrad_J[kStep, mIdx] := rTempSum +
                                      (2.0 * vecR_weight[mIdx] * trajU_mpc[kStep, mIdx]) +
                                      (2.0 * vecR_delta_weight[mIdx] * (trajU_mpc[kStep, mIdx] - vecU_prev[mIdx]));
        END_FOR;
    END_FOR;

    (* 3e. Projected Gradient Descent Update Step & Constraint Projection *)
    FOR kStep := 0 TO 4 DO
        FOR mIdx := 0 TO 4 DO
            (* Gradient Descent Step: u_cand = u - gamma * grad_J *)
            rTempCandidate := trajU_mpc[kStep, mIdx] - (rPgd_StepSize * trajGrad_J[kStep, mIdx]);

            (* Projection 1: Slew Rate Limit Clamping w.r.t Previous Plant Command *)
            rTempDeltaU := rTempCandidate - vecU_prev[mIdx];
            IF rTempDeltaU > vecU_slewMax[mIdx] THEN
                rTempDeltaU := vecU_slewMax[mIdx];
            ELSIF rTempDeltaU < -vecU_slewMax[mIdx] THEN
                rTempDeltaU := -vecU_slewMax[mIdx];
            END_IF;
            rTempCandidate := vecU_prev[mIdx] + rTempDeltaU;

            (* Projection 2: Physical Lower & Upper Actuator Saturation Box Clamping *)
            IF rTempCandidate > vecU_max[mIdx] THEN
                trajU_mpc[kStep, mIdx] := vecU_max[mIdx];
            ELSIF rTempCandidate < vecU_min[mIdx] THEN
                trajU_mpc[kStep, mIdx] := vecU_min[mIdx];
            ELSE
                trajU_mpc[kStep, mIdx] := rTempCandidate;
            END_IF;
        END_FOR;
    END_FOR;
END_FOR;

(* ---------------------------------------------------------------------------------------------------- *)
(* Step 4: Apply Optimal Control Action from Horizon Step 0 to Physical Actuator Outputs                *)
(* ---------------------------------------------------------------------------------------------------- *)
IF NOT bMpcManualOverride AND eState <> 12 AND eState <> 0 THEN
    FOR mIdx := 0 TO 4 DO
        vecU[mIdx] := trajU_mpc[0, mIdx];
        vecU_rate[mIdx] := (vecU[mIdx] - vecU_prev[mIdx]) / tScanCycleTime_s;
        vecU_prev[mIdx] := vecU[mIdx];
    END_FOR;

    rValve_H2_BackPress_Cmd_pct  := vecU[0];
    rValve_Cl2_Vent_Cmd_pct      := vecU[1];
    rValve_WaterDilution_Cmd_pct := vecU[2];
    rValve_BrineTrim_Cmd_pct     := vecU[3];
    rRectifier_Current_Cmd_kA    := vecU[4];
END_IF;

rMpc_CostFunction_Val := rMpc_AccumulatedCost;
"""

with open("dataset_parts/part5_mpc.txt", "w", encoding="utf-8") as f:
    f.write(part5)

print("Part 5 written successfully.")
