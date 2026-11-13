# build_st_phase3_mpc.py
# Section 6: Phase 3 - Receding Horizon Model Predictive Control (MPC) with Projected Gradient Descent (PGD)

def get_phase3_mpc():
    code = []
    code.append("""(* =====================================================================================================================
 * PHASE 3: RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) WITH PROJECTED GRADIENT DESCENT (PGD)
 * Mathematical Formulation:
 *   Prediction Horizon: Np = 5 steps (tau_horizon = 125 ms ahead)
 *   Cost Functional:
 *     J = 0.5 * sum_{k=1..Np} [ (x[k] - x_ref)^T * Q * (x[k] - x_ref) + (u[k] - u_prev)^T * R * (u[k] - u_prev) ]
 *       + 0.5 * (x[Np+1] - x_ref)^T * P * (x[Np+1] - x_ref)
 *   Optimization Algorithm:
 *     Unrolled 5-iteration Projected Gradient Descent (PGD)
 *     Forward State Rollout:   x[k+1] = A * x[k] + B * u[k]
 *     Backward Adjoint Costate: lambda[k] = A^T * lambda[k+1] + Q * (x[k] - x_ref)
 *     Gradient Vector:         grad_u[k] = B^T * lambda[k+1] + R * (u[k] - u_prev)
 *     Actuator Projections:    u_traj[k] := Clip(u_traj[k] - alpha * grad_u[k], U_min, U_max)
 *                              Slew_Limit: |u[k] - u[k-1]| <= rMax_Slew_Per_Cycle (5.0 %/s)
 *   Dynamic Feedforward:
 *     Cancels non-minimum phase zero (shrink/swell illusion) via steam flow / feedwater flow feedforward ratio.
 * ===================================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------------------------
 * SECTION 3.1: ESTABLISH TARGET REFERENCE STATE VECTOR x_ref[1..8]
 * --------------------------------------------------------------------------------------------------------------------- *)
(* Level NR reference: deviation from calibrated nominal center (2500.0 mm) *)
x_ref[1] := rOperator_Level_Setpoint_NR - 2500.0;
x_ref[2] := 0.0; (* Flow deviation centered on equilibrium *)
x_ref[3] := 0.0; (* Void fraction centered on nominal boiling equilibrium *)
x_ref[4] := 0.0; (* Heat transfer centered on equilibrium *)
x_ref[5] := 0.0; (* Drum pressure tracking nominal 68.5 bar *)
x_ref[6] := 0.0; (* Cold leg temp tracking nominal 292.0 deg C *)
x_ref[7] := 0.0; (* Valve trim equilibrium *)
x_ref[8] := 0.0; (* Target zero dynamic shrink/swell disturbance state *)

(* ---------------------------------------------------------------------------------------------------------------------
 * SECTION 3.2: WARM-START MPC CONTROL TRAJECTORY FROM PREVIOUS CYCLE
 * Shift horizon: u[k] := u[k+1], repeat last step at end
 * --------------------------------------------------------------------------------------------------------------------- *)
FOR k_idx := 1 TO 4 DO
    FOR j_idx := 1 TO 5 DO
        u_traj[k_idx, j_idx] := u_traj[k_idx + 1, j_idx];
    END_FOR;
END_FOR;
FOR j_idx := 1 TO 5 DO
    u_traj[5, j_idx] := u_traj[4, j_idx];
END_FOR;

(* Seed current plant control as baseline *)
u_prev[1] := rCommand_MFRV_Position;
u_prev[2] := rCommand_Bypass_Valve_Pos;
u_prev[3] := rCommand_AFW_Motor_Pump_Speed;
u_prev[4] := rCommand_AFW_Turbine_Pump_Flow;
u_prev[5] := rCommand_Blowdown_Valve_Pos;

(* ---------------------------------------------------------------------------------------------------------------------
 * SECTION 3.3: UNROLLED 5-ITERATION PROJECTED GRADIENT DESCENT (PGD) SOLVER LOOP
 * --------------------------------------------------------------------------------------------------------------------- *)
FOR m_idx := 1 TO 5 DO
    (* -----------------------------------------------------------------------------------------------------------------
     * STEP A: FORWARD TRAJECTORY ROLLOUT (x_traj[k+1] = A * x_traj[k] + B * u_traj[k])
     * ----------------------------------------------------------------------------------------------------------------- *)
    (* Initialize step 1 with current estimated state x_hat *)
    FOR i_idx := 1 TO 8 DO
        x_traj[1, i_idx] := x_hat[i_idx];
    END_FOR;

    FOR k_idx := 1 TO 5 DO
        FOR i_idx := 1 TO 8 DO
            sum_accum := 0.0;
            (* State dynamics contribution: A * x *)
            FOR j_idx := 1 TO 8 DO
                sum_accum := sum_accum + (A_mat[i_idx, j_idx] * x_traj[k_idx, j_idx]);
            END_FOR;
            (* Control input contribution: B * u *)
            FOR j_idx := 1 TO 5 DO
                sum_accum := sum_accum + (B_mat[i_idx, j_idx] * u_traj[k_idx, j_idx]);
            END_FOR;
            x_traj[k_idx + 1, i_idx] := sum_accum;
        END_FOR;
    END_FOR;

    (* -----------------------------------------------------------------------------------------------------------------
     * STEP B: BACKWARD ADJOINT COSTATE PROPAGATION (lambda[k] = A^T * lambda[k+1] + Q * (x[k] - x_ref))
     * ----------------------------------------------------------------------------------------------------------------- *)
    (* Terminal Costate at step Np+1 = 6: lambda[6] = P * (x[6] - x_ref) *)
    FOR i_idx := 1 TO 8 DO
        sum_accum := 0.0;
        FOR j_idx := 1 TO 8 DO
            sum_accum := sum_accum + (P_mat[i_idx, j_idx] * (x_traj[6, j_idx] - x_ref[j_idx]));
        END_FOR;
        lambda_costate[6, i_idx] := sum_accum;
    END_FOR;

    (* Backward recursion for k = 5 DOWNTO 1 *)
    FOR k_idx := 5 TO 1 BY -1 DO
        FOR i_idx := 1 TO 8 DO
            sum_accum := 0.0;
            (* Adjoint dynamic transpose contribution: A^T * lambda[k+1] *)
            FOR j_idx := 1 TO 8 DO
                sum_accum := sum_accum + (A_mat[j_idx, i_idx] * lambda_costate[k_idx + 1, j_idx]);
            END_FOR;
            (* Running state tracking error cost gradient: Q * (x[k] - x_ref) *)
            FOR j_idx := 1 TO 8 DO
                sum_accum := sum_accum + (Q_mat[i_idx, j_idx] * (x_traj[k_idx, j_idx] - x_ref[j_idx]));
            END_FOR;
            lambda_costate[k_idx, i_idx] := sum_accum;
        END_FOR;
    END_FOR;

    (* -----------------------------------------------------------------------------------------------------------------
     * STEP C: GRADIENT COMPUTATION, DESCENT STEP & CONSTRAINT PROJECTION
     * ----------------------------------------------------------------------------------------------------------------- *)
    FOR k_idx := 1 TO 5 DO
        FOR j_idx := 1 TO 5 DO
            sum_accum := 0.0;
            (* Adjoint input transpose contribution: B^T * lambda[k+1] *)
            FOR i_idx := 1 TO 8 DO
                sum_accum := sum_accum + (B_mat[i_idx, j_idx] * lambda_costate[k_idx + 1, i_idx]);
            END_FOR;
            (* Actuator effort penalty: R * (u[k] - u_prev) *)
            FOR i_idx := 1 TO 5 DO
                sum_accum := sum_accum + (R_mat[j_idx, i_idx] * (u_traj[k_idx, i_idx] - u_prev[i_idx]));
            END_FOR;
            grad_u[k_idx, j_idx] := sum_accum;

            (* Projected Gradient Descent update *)
            u_traj[k_idx, j_idx] := u_traj[k_idx, j_idx] - (rPGD_StepSize * grad_u[k_idx, j_idx]);
        END_FOR;

        (* -------------------------------------------------------------------------------------------------------------
         * HARD PHYSICAL ACTUATOR CONSTRAINTS & BOUND PROJECTIONS
         * ------------------------------------------------------------------------------------------------------------- *)
        (* Actuator 1: MFRV Position Limits [0.0 % .. 100.0 %] *)
        IF u_traj[k_idx, 1] > rMPC_MFRV_Upper_Bound THEN
            u_traj[k_idx, 1] := rMPC_MFRV_Upper_Bound;
        ELSIF u_traj[k_idx, 1] < rMPC_MFRV_Lower_Bound THEN
            u_traj[k_idx, 1] := rMPC_MFRV_Lower_Bound;
        END_IF;

        (* Actuator 2: Low-Power Bypass Limits [0.0 % .. 100.0 %] *)
        IF u_traj[k_idx, 2] > rMPC_Bypass_Upper_Bound THEN
            u_traj[k_idx, 2] := rMPC_Bypass_Upper_Bound;
        ELSIF u_traj[k_idx, 2] < rMPC_Bypass_Lower_Bound THEN
            u_traj[k_idx, 2] := rMPC_Bypass_Lower_Bound;
        END_IF;

        (* Actuator 3: Motor-Driven AFW Pump Speed Limits [0.0 % .. 100.0 %] *)
        IF u_traj[k_idx, 3] > 100.0 THEN
            u_traj[k_idx, 3] := 100.0;
        ELSIF u_traj[k_idx, 3] < 0.0 THEN
            u_traj[k_idx, 3] := 0.0;
        END_IF;

        (* Actuator 4: Turbine-Driven AFW Flow Limits [0.0 t/h .. 150.0 t/h] *)
        IF u_traj[k_idx, 4] > 150.0 THEN
            u_traj[k_idx, 4] := 150.0;
        ELSIF u_traj[k_idx, 4] < 0.0 THEN
            u_traj[k_idx, 4] := 0.0;
        END_IF;

        (* Actuator 5: Blowdown Valve Limits [0.0 % .. 10.0 %] *)
        IF u_traj[k_idx, 5] > 10.0 THEN
            u_traj[k_idx, 5] := 10.0;
        ELSIF u_traj[k_idx, 5] < 0.0 THEN
            u_traj[k_idx, 5] := 0.0;
        END_IF;

        (* -------------------------------------------------------------------------------------------------------------
         * ACTUATOR SLEW RATE CONSTRAINTS (5.0 %/s = 0.125 % / 25 ms tick)
         * ------------------------------------------------------------------------------------------------------------- *)
        IF k_idx = 1 THEN
            (* Clamping against previous cycle real executed position *)
            IF (u_traj[1, 1] - u_prev[1]) > rMax_Slew_Per_Cycle THEN
                u_traj[1, 1] := u_prev[1] + rMax_Slew_Per_Cycle;
            ELSIF (u_traj[1, 1] - u_prev[1]) < -rMax_Slew_Per_Cycle THEN
                u_traj[1, 1] := u_prev[1] - rMax_Slew_Per_Cycle;
            END_IF;

            IF (u_traj[1, 2] - u_prev[2]) > rMax_Slew_Per_Cycle THEN
                u_traj[1, 2] := u_prev[2] + rMax_Slew_Per_Cycle;
            ELSIF (u_traj[1, 2] - u_prev[2]) < -rMax_Slew_Per_Cycle THEN
                u_traj[1, 2] := u_prev[2] - rMax_Slew_Per_Cycle;
            END_IF;
        ELSE
            (* Clamping against horizon prior step trajectory *)
            IF (u_traj[k_idx, 1] - u_traj[k_idx - 1, 1]) > rMax_Slew_Per_Cycle THEN
                u_traj[k_idx, 1] := u_traj[k_idx - 1, 1] + rMax_Slew_Per_Cycle;
            ELSIF (u_traj[k_idx, 1] - u_traj[k_idx - 1, 1]) < -rMax_Slew_Per_Cycle THEN
                u_traj[k_idx, 1] := u_traj[k_idx - 1, 1] - rMax_Slew_Per_Cycle;
            END_IF;

            IF (u_traj[k_idx, 2] - u_traj[k_idx - 1, 2]) > rMax_Slew_Per_Cycle THEN
                u_traj[k_idx, 2] := u_traj[k_idx - 1, 2] + rMax_Slew_Per_Cycle;
            ELSIF (u_traj[k_idx, 2] - u_traj[k_idx - 1, 2]) < -rMax_Slew_Per_Cycle THEN
                u_traj[k_idx, 2] := u_traj[k_idx - 1, 2] - rMax_Slew_Per_Cycle;
            END_IF;
        END_IF;
    END_FOR;
END_FOR;

(* ---------------------------------------------------------------------------------------------------------------------
 * SECTION 3.4: QUADRATIC COST FUNCTION J EVALUATION & TELEMETRY
 * --------------------------------------------------------------------------------------------------------------------- *)
cost_accum := 0.0;
FOR k_idx := 1 TO 5 DO
    FOR i_idx := 1 TO 8 DO
        FOR j_idx := 1 TO 8 DO
            cost_accum := cost_accum + (0.5 * (x_traj[k_idx, i_idx] - x_ref[i_idx]) * Q_mat[i_idx, j_idx] * (x_traj[k_idx, j_idx] - x_ref[j_idx]));
        END_FOR;
    END_FOR;
    FOR i_idx := 1 TO 5 DO
        FOR j_idx := 1 TO 5 DO
            cost_accum := cost_accum + (0.5 * (u_traj[k_idx, i_idx] - u_prev[i_idx]) * R_mat[i_idx, j_idx] * (u_traj[k_idx, j_idx] - u_prev[j_idx]));
        END_FOR;
    END_FOR;
END_FOR;
FOR i_idx := 1 TO 8 DO
    FOR j_idx := 1 TO 8 DO
        cost_accum := cost_accum + (0.5 * (x_traj[6, i_idx] - x_ref[i_idx]) * P_mat[i_idx, j_idx] * (x_traj[6, j_idx] - x_ref[j_idx]));
    END_FOR;
END_FOR;
rMPC_Optimization_Cost_J := cost_accum;

(* ---------------------------------------------------------------------------------------------------------------------
 * SECTION 3.5: DYNAMIC INVERSE RESPONSE COMPENSATION SUPERPOSITION
 * Extract first step of optimal control trajectory and superimpose dynamic feedforward decoupling
 * --------------------------------------------------------------------------------------------------------------------- *)
rMFRV_Auto_Demand_Unclamped   := u_traj[1, 1] + (rDynamic_Feedforward_Bias * 0.045);
rBypass_Auto_Demand_Unclamped := u_traj[1, 2] + (rDynamic_Feedforward_Bias * 0.015);
""")
    return "\n".join(code)

if __name__ == "__main__":
    s = get_phase3_mpc()
    print("Phase 3 MPC length:", len(s))
