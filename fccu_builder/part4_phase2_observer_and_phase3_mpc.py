# fccu_builder/part4_phase2_observer_and_phase3_mpc.py

def get_part4_phase2_observer_and_phase3_mpc():
    lines = []
    lines.append("""(*
========================================================================================================================
  PHASE 2: FIRST-PRINCIPLES CYBER-PHYSICAL STATE-SPACE ESTIMATION & LUENBERGER OBSERVER (Ts = 25 ms)
========================================================================================================================
*)
(* ---------------------------------------------------------------------------------------------------------------------
   2.1 Formulate Validated Physical Measurement Vector y_meas[1..6]
   - y1: Riser Outlet Temperature [deg C] (from 2oo3 voted sensor)
   - y2: Riser Bottom-to-Top Total Differential Pressure [kPa] (from PDT_RISER_TOTAL)
   - y3: Regenerator 1st Stage Dense Bed Temperature [deg C] (from 2oo3 voted sensor)
   - y4: Spent Catalyst Slide Valve Differential Pressure [kPa] (from 2oo3 voted sensor)
   - y5: Regenerated Catalyst Slide Valve Differential Pressure [kPa] (from 2oo3 voted sensor)
   - y6: Regenerator Flue Gas Excess Oxygen Content [% O2] (from 2oo3 voted analyzer)
   --------------------------------------------------------------------------------------------------------------------- *)
y_meas[1] := rVoted_RiserTemp_degC;
y_meas[2] := rPDT_RISER_TOTAL_kPa;
y_meas[3] := rVoted_RegenBedTemp_degC;
y_meas[4] := rVoted_SCSV_dP_kPa;
y_meas[5] := rVoted_RCSV_dP_kPa;
y_meas[6] := rVoted_FlueGasO2_pct;

(* ---------------------------------------------------------------------------------------------------------------------
   2.2 Open-Loop State Prediction Propagation: x_pred = A * x_hat + B * u_cmd
   Discrete dynamic slip-flow, cracked molar expansion, and coke combustion transport model
   --------------------------------------------------------------------------------------------------------------------- *)
FOR iIdx := 1 TO 8 DO
    rTempScalar1 := 0.0;
    (* State transition matrix drift contribution *)
    FOR jIdx := 1 TO 8 DO
        rTempScalar1 := rTempScalar1 + (A_Matrix[iIdx, jIdx] * x_hat[jIdx]);
    END_FOR;
    (* Manipulated actuator coupling transmission contribution *)
    FOR mIdx := 1 TO 6 DO
        rTempScalar1 := rTempScalar1 + (B_Matrix[iIdx, mIdx] * u_cmd[mIdx]);
    END_FOR;
    x_pred[iIdx] := rTempScalar1;
END_FOR;

(* ---------------------------------------------------------------------------------------------------------------------
   2.3 Synthetic Observation Vector y_est and Innovation Residuals y_innov
   y_est = C * x_pred + D * u_cmd
   y_innov = y_meas - y_est
   --------------------------------------------------------------------------------------------------------------------- *)
FOR iIdx := 1 TO 6 DO
    rTempScalar1 := 0.0;
    FOR jIdx := 1 TO 8 DO
        rTempScalar1 := rTempScalar1 + (C_Matrix[iIdx, jIdx] * x_pred[jIdx]);
    END_FOR;
    FOR mIdx := 1 TO 6 DO
        rTempScalar1 := rTempScalar1 + (D_Matrix[iIdx, mIdx] * u_cmd[mIdx]);
    END_FOR;
    y_est[iIdx] := rTempScalar1;
    y_innov[iIdx] := y_meas[iIdx] - y_est[iIdx];
END_FOR;

(* ---------------------------------------------------------------------------------------------------------------------
   2.4 Posteriori State Estimate Correction (Luenberger Observer Feedback Update)
   x_hat = x_pred + L * y_innov
   --------------------------------------------------------------------------------------------------------------------- *)
FOR iIdx := 1 TO 8 DO
    rTempScalar1 := x_pred[iIdx];
    FOR jIdx := 1 TO 6 DO
        rTempScalar1 := rTempScalar1 + (L_Matrix[iIdx, jIdx] * y_innov[jIdx]);
    END_FOR;
    x_hat[iIdx] := rTempScalar1;
    x_err[iIdx] := x_hat[iIdx] - x_sp[iIdx];
END_FOR;

(* Assign Cyber-Physical Filtered State Estimates to External VAR_OUTPUT Diagnostics *)
rObs_RiserTemp_degC       := x_hat[1];
rObs_RiserTopDP_kPa       := x_hat[2];
rObs_RegenStage1Temp_degC := x_hat[3];
rObs_RegenStage2Temp_degC := x_hat[4];
rObs_SCSV_dP_kPa          := x_hat[5];
rObs_RCSV_dP_kPa          := x_hat[6];
rObs_ExcessO2_pct         := x_hat[7];
rObs_CO_ppmv              := x_hat[8];

(* ---------------------------------------------------------------------------------------------------------------------
   2.5 First-Principles Chemical Engineering Thermodynamic & Kinetic Diagnostics
   --------------------------------------------------------------------------------------------------------------------- *)
(* 1. Riser Endothermic Reaction Heat Absorption Power [MW] *)
(* Formula: Q_absorb = F_feed * [Delta_H_vap + C_p_oil * (T_riser - T_feed) + Delta_H_crack * X_feed] *)
IF rFT_OIL_FEED_th > 1.0 THEN
    rRiserHeatAbsorptionRate_MW := ((rFT_OIL_FEED_th * 1000.0 / 3600.0) * (380.0 + 2.85 * (x_hat[1] - rTT_FEED_PREHEAT_degC) + (450.0 * 0.76))) / 1000.0;
ELSE
    rRiserHeatAbsorptionRate_MW := 0.0;
END_IF;
IF rRiserHeatAbsorptionRate_MW < 0.0 THEN
    rRiserHeatAbsorptionRate_MW := 0.0;
END_IF;

(* 2. Fluidized Catalyst Mass Circulation Rate [t/h] from Mixing Zone Heat Balance *)
(* Sensible heat transfer from incoming regenerated catalyst satisfies riser heat requirement: *)
(* F_cat * C_p_cat * (T_regen - T_riser) = Q_absorb *)
IF (x_hat[3] - x_hat[1]) > 45.0 AND rRiserHeatAbsorptionRate_MW > 0.1 THEN
    rCatalystCirculationRate_th := ((rRiserHeatAbsorptionRate_MW * 1000.0) / (1.15 * (x_hat[3] - x_hat[1]))) * 3.6;
ELSE
    rCatalystCirculationRate_th := 0.0;
END_IF;
IF rCatalystCirculationRate_th < 0.0 THEN
    rCatalystCirculationRate_th := 0.0;
ELSIF rCatalystCirculationRate_th > 4200.0 THEN
    rCatalystCirculationRate_th := 4200.0;
END_IF;

(* 3. Instantaneous Catalyst-to-Oil Ratio (C/O) [wt/wt] *)
IF rFT_OIL_FEED_th > 5.0 THEN
    rCatalystToOilRatio_wt := rCatalystCirculationRate_th / rFT_OIL_FEED_th;
ELSE
    rCatalystToOilRatio_wt := 0.0;
END_IF;
IF rCatalystToOilRatio_wt < 0.0 THEN
    rCatalystToOilRatio_wt := 0.0;
ELSIF rCatalystToOilRatio_wt > 15.0 THEN
    rCatalystToOilRatio_wt := 15.0;
END_IF;

(* 4. Regenerator Bed Exothermic Coke Combustion Power [MW] *)
(* Evaluates total thermal energy generated by complete and partial coke oxidation *)
IF rFT_COMBUSTION_AIR_kgs > 5.0 THEN
    rCokeCombustionPower_MW := (rFT_COMBUSTION_AIR_kgs * 0.2315 / 32.0) * (((1.0 - (x_hat[7] / 21.0)) * 393.5) + ((x_hat[8] / 10000.0) * 110.5));
ELSE
    rCokeCombustionPower_MW := 0.0;
END_IF;
IF rCokeCombustionPower_MW < 0.0 THEN
    rCokeCombustionPower_MW := 0.0;
END_IF;

(* 5. Regenerator Cyclone Dilute Phase Afterburn Temperature Differential [deg C] *)
rAfterburnDeltaT_degC := rTT_REGEN_CYCLONE_degC - x_hat[3];


(*
========================================================================================================================
  PHASE 3: RECEDING-HORIZON MPC OPTIMIZATION WITH PROJECTED GRADIENT DESCENT (PGD) & BARRIER PENALTIES
========================================================================================================================
*)
(* ---------------------------------------------------------------------------------------------------------------------
   3.1 Initialize Control Trajectory Horizon N = 5 Steps (k = 0..4)
   --------------------------------------------------------------------------------------------------------------------- *)
FOR kIdx := 0 TO 4 DO
    FOR mIdx := 1 TO 6 DO
        u_horiz[kIdx, mIdx] := u_cmd[mIdx];
    END_FOR;
END_FOR;

(* ---------------------------------------------------------------------------------------------------------------------
   3.2 Unrolled Projected Gradient Descent (PGD) Solver (6 Fixed Iterations)
   Constrained multivariable quadratic cost with severe hydraulic anti-reversal barrier functions
   Cost = 0.5 * SUM_{k=0..4} [ (x_k - x_sp)^T Q (x_k - x_sp) + Barrier(dP) + (u_k - u_prev)^T R (u_k - u_prev) ]
          + 0.5 * (x_5 - x_sp)^T P (x_5 - x_sp) + Barrier(dP_5)
   --------------------------------------------------------------------------------------------------------------------- *)
FOR nIter := 1 TO 6 DO
    (* -----------------------------------------------------------------------------------------------------------------
       SUB-STEP A: Forward State Trajectory Simulation Across Horizon (k = 0..4)
       x_horiz[k+1] = A * x_horiz[k] + B * u_horiz[k]
       ----------------------------------------------------------------------------------------------------------------- *)
    FOR iIdx := 1 TO 8 DO
        x_horiz[0, iIdx] := x_hat[iIdx];
    END_FOR;

    FOR kIdx := 0 TO 4 DO
        FOR iIdx := 1 TO 8 DO
            rTempScalar1 := 0.0;
            FOR jIdx := 1 TO 8 DO
                rTempScalar1 := rTempScalar1 + (A_Matrix[iIdx, jIdx] * x_horiz[kIdx, jIdx]);
            END_FOR;
            FOR mIdx := 1 TO 6 DO
                rTempScalar1 := rTempScalar1 + (B_Matrix[iIdx, mIdx] * u_horiz[kIdx, mIdx]);
            END_FOR;
            x_horiz[kIdx + 1, iIdx] := rTempScalar1;
        END_FOR;
    END_FOR;

    (* -----------------------------------------------------------------------------------------------------------------
       SUB-STEP B: Backward Adjoint Costate Back-propagation (Pontryagin Minimum Principle)
       Terminal Costate: lambda[5] = P * (x[5] - x_sp) + dTerminalBarrier/dx
       ----------------------------------------------------------------------------------------------------------------- *)
    FOR iIdx := 1 TO 8 DO
        lambda_costate[5, iIdx] := P_diag[iIdx] * (x_horiz[5, iIdx] - x_sp[iIdx]);
    END_FOR;

    (* Terminal Slide Valve Hydraulic Seal Barrier Penalties on x5 (SCSV) and x6 (RCSV) *)
    (* Lower Anti-Reversal Deflagration Barrier (< 35 kPa) *)
    IF x_horiz[5, 5] < 35.0 THEN
        lambda_costate[5, 5] := lambda_costate[5, 5] - (rSlideValveBarrierWeight * 2.0 * (35.0 - x_horiz[5, 5]));
    ELSIF x_horiz[5, 5] > 70.0 THEN
        lambda_costate[5, 5] := lambda_costate[5, 5] + (rSlideValveHighBarrierWeight * 2.0 * (x_horiz[5, 5] - 70.0));
    END_IF;

    IF x_horiz[5, 6] < 35.0 THEN
        lambda_costate[5, 6] := lambda_costate[5, 6] - (rSlideValveBarrierWeight * 2.0 * (35.0 - x_horiz[5, 6]));
    ELSIF x_horiz[5, 6] > 70.0 THEN
        lambda_costate[5, 6] := lambda_costate[5, 6] + (rSlideValveHighBarrierWeight * 2.0 * (x_horiz[5, 6] - 70.0));
    END_IF;

    (* Recursive Costate Back-Propagation (k = 4 DOWNTO 0) *)
    (* lambda[k] = Q * (x[k] - x_sp) + dBarrier/dx + A^T * lambda[k+1] *)
    FOR kIdx := 4 DOWNTO 0 DO
        FOR iIdx := 1 TO 8 DO
            dJ_dx[iIdx] := Q_diag[iIdx] * (x_horiz[kIdx, iIdx] - x_sp[iIdx]);
            
            (* Add dynamic barrier gradient for slide valve differential pressures *)
            IF iIdx = 5 THEN
                IF x_horiz[kIdx, 5] < 35.0 THEN
                    dJ_dx[5] := dJ_dx[5] - (rSlideValveBarrierWeight * (35.0 - x_horiz[kIdx, 5]));
                ELSIF x_horiz[kIdx, 5] > 70.0 THEN
                    dJ_dx[5] := dJ_dx[5] + (rSlideValveHighBarrierWeight * (x_horiz[kIdx, 5] - 70.0));
                END_IF;
            ELSIF iIdx = 6 THEN
                IF x_horiz[kIdx, 6] < 35.0 THEN
                    dJ_dx[6] := dJ_dx[6] - (rSlideValveBarrierWeight * (35.0 - x_horiz[kIdx, 6]));
                ELSIF x_horiz[kIdx, 6] > 70.0 THEN
                    dJ_dx[6] := dJ_dx[6] + (rSlideValveHighBarrierWeight * (x_horiz[kIdx, 6] - 70.0));
                END_IF;
            END_IF;

            rTempScalar1 := dJ_dx[iIdx];
            FOR jIdx := 1 TO 8 DO
                rTempScalar1 := rTempScalar1 + (A_Matrix[jIdx, iIdx] * lambda_costate[kIdx + 1, jIdx]);
            END_FOR;
            lambda_costate[kIdx, iIdx] := rTempScalar1;
        END_FOR;
    END_FOR;

    (* -----------------------------------------------------------------------------------------------------------------
       SUB-STEP C: Analytical Input Gradient Evaluation, Descent Step & Actuator Projection
       grad_u[k] = R * (u[k] - u_prev) + B^T * lambda[k+1]
       u[k] := Project_[u_min, u_max, du_max] ( u[k] - alpha * grad_u[k] )
       ----------------------------------------------------------------------------------------------------------------- *)
    FOR kIdx := 0 TO 4 DO
        FOR mIdx := 1 TO 6 DO
            rTempScalar1 := R_diag[mIdx] * (u_horiz[kIdx, mIdx] - u_prev[mIdx]);
            FOR jIdx := 1 TO 8 DO
                rTempScalar1 := rTempScalar1 + (B_Matrix[jIdx, mIdx] * lambda_costate[kIdx + 1, jIdx]);
            END_FOR;
            grad_u[kIdx, mIdx] := rTempScalar1;

            (* Gradient descent update *)
            u_horiz[kIdx, mIdx] := u_horiz[kIdx, mIdx] - (rPGD_AlphaStep * grad_u[kIdx, mIdx]);

            (* Euclidean projection onto physical actuator box constraints [0..100%] *)
            IF u_horiz[kIdx, mIdx] < u_min[mIdx] THEN
                u_horiz[kIdx, mIdx] := u_min[mIdx];
            ELSIF u_horiz[kIdx, mIdx] > u_max[mIdx] THEN
                u_horiz[kIdx, mIdx] := u_max[mIdx];
            END_IF;

            (* Slew rate boundary projection relative to u_prev *)
            IF (u_horiz[kIdx, mIdx] - u_prev[mIdx]) > (du_max[mIdx] * INT_TO_REAL(kIdx + 1)) THEN
                u_horiz[kIdx, mIdx] := u_prev[mIdx] + (du_max[mIdx] * INT_TO_REAL(kIdx + 1));
            ELSIF (u_horiz[kIdx, mIdx] - u_prev[mIdx]) < (-du_max[mIdx] * INT_TO_REAL(kIdx + 1)) THEN
                u_horiz[kIdx, mIdx] := u_prev[mIdx] - (du_max[mIdx] * INT_TO_REAL(kIdx + 1));
            END_IF;
        END_FOR;
    END_FOR;
END_FOR;

(* ---------------------------------------------------------------------------------------------------------------------
   3.3 Evaluate Total Objective Cost J, Optimization Residual & Extract Next Actuation Command
   --------------------------------------------------------------------------------------------------------------------- *)
rMPC_CostFunctionJ := 0.0;
FOR kIdx := 0 TO 4 DO
    FOR iIdx := 1 TO 8 DO
        rMPC_CostFunctionJ := rMPC_CostFunctionJ + (0.5 * Q_diag[iIdx] * (x_horiz[kIdx, iIdx] - x_sp[iIdx]) * (x_horiz[kIdx, iIdx] - x_sp[iIdx]));
    END_FOR;
    (* Add barrier cost *)
    IF x_horiz[kIdx, 5] < 35.0 THEN
        rMPC_CostFunctionJ := rMPC_CostFunctionJ + (0.5 * rSlideValveBarrierWeight * (35.0 - x_horiz[kIdx, 5]) * (35.0 - x_horiz[kIdx, 5]));
    ELSIF x_horiz[kIdx, 5] > 70.0 THEN
        rMPC_CostFunctionJ := rMPC_CostFunctionJ + (0.5 * rSlideValveHighBarrierWeight * (x_horiz[kIdx, 5] - 70.0) * (x_horiz[kIdx, 5] - 70.0));
    END_IF;
    IF x_horiz[kIdx, 6] < 35.0 THEN
        rMPC_CostFunctionJ := rMPC_CostFunctionJ + (0.5 * rSlideValveBarrierWeight * (35.0 - x_horiz[kIdx, 6]) * (35.0 - x_horiz[kIdx, 6]));
    ELSIF x_horiz[kIdx, 6] > 70.0 THEN
        rMPC_CostFunctionJ := rMPC_CostFunctionJ + (0.5 * rSlideValveHighBarrierWeight * (x_horiz[kIdx, 6] - 70.0) * (x_horiz[kIdx, 6] - 70.0));
    END_IF;
    FOR mIdx := 1 TO 6 DO
        rMPC_CostFunctionJ := rMPC_CostFunctionJ + (0.5 * R_diag[mIdx] * (u_horiz[kIdx, mIdx] - u_prev[mIdx]) * (u_horiz[kIdx, mIdx] - u_prev[mIdx]));
    END_FOR;
END_FOR;

(* Terminal step cost *)
FOR iIdx := 1 TO 8 DO
    rMPC_CostFunctionJ := rMPC_CostFunctionJ + (0.5 * P_diag[iIdx] * (x_horiz[5, iIdx] - x_sp[iIdx]) * (x_horiz[5, iIdx] - x_sp[iIdx]));
END_FOR;

(* Evaluate Infinity Norm of First Step Gradient for Solver Convergence Monitoring *)
rMPC_OptimizationError := 0.0;
FOR mIdx := 1 TO 6 DO
    IF ABS(grad_u[0, mIdx]) > rMPC_OptimizationError THEN
        rMPC_OptimizationError := ABS(grad_u[0, mIdx]);
    END_IF;
END_FOR;

(* Extract First Horizon Manipulated Command Vector into u_opt *)
FOR mIdx := 1 TO 6 DO
    u_opt[mIdx] := u_horiz[0, mIdx];
END_FOR;
""")
    return "\n".join(lines)
