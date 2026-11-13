# cz_silicon_builder/mod_mpc.py
# -*- coding: utf-8 -*-

def generate_mpc():
    return """(* ==========================================================================================
   PHASE 3: RECEDING-HORIZON MPC OPTIMIZATION WITH 10 UNROLLED PGD ITERATIONS
   ==========================================================================================
   Optimizes control trajectory over prediction horizon N = 5 steps (Ts = 100 ms).
   Minimizes multi-objective quadratic performance index:
     J = 0.5 * SUM_{k=0}^{N-1} [ (x[k] - x_ref)' * Q * (x[k] - x_ref) + u[k]' * R * u[k]
                                  + (u[k] - u[k-1])' * S * (u[k] - u[k-1]) ]
         + 0.5 * (x[N] - x_ref)' * P * (x[N] - x_ref)
   
   Enforces:
     1. Crystal Dislocation Slip Suppression & Voronkov V/G defect-free window
     2. Physical Actuator Box Constraints (Saturation Limits)
     3. Maximum Allowable Actuator Slew Rate Bounds
     4. 10 Unrolled Forward-Backward Adjoint Passes via Projected Gradient Descent (PGD)
   ========================================================================================== *)

(* Only execute active MPC optimization when in body growth or shoulder states *)
IF (iCurrentFSMState = STATE_BODY_EQUAL_DIAMETER_GROWTH_MPC_ACTIVE)
   OR (iCurrentFSMState = STATE_SHOULDER_RADIUS_ROLLOVER_TRANSITION)
   OR (iCurrentFSMState = STATE_CROWN_EXPANSION_CONE_ANGLE_RAMP) THEN

    (* Initialize prediction horizon starting point with current observer estimate *)
    FOR iLoopIndex := 1 TO 6 DO
        x_pred[0, iLoopIndex] := x_hat[iLoopIndex];
    END_FOR;

    (* --------------------------------------------------------------------------------------
       EXECUTE 10 UNROLLED PROJECTED GRADIENT DESCENT (PGD) ITERATIONS
       -------------------------------------------------------------------------------------- *)
    FOR iPGDIteration := 1 TO 10 DO

        (* STEP 1: FORWARD TRAJECTORY PROPAGATION (k = 0 TO 4)
           x_pred[k+1] = A * x_pred[k] + B * u_plan[k] *)
        FOR iHor := 0 TO 4 DO
            FOR iRow := 1 TO 6 DO
                x_pred[iHor + 1, iRow] := 0.0;
                (* A * x_pred term *)
                FOR jLoopIndex := 1 TO 6 DO
                    x_pred[iHor + 1, iRow] := x_pred[iHor + 1, iRow] + (A_mat[iRow, jLoopIndex] * x_pred[iHor, jLoopIndex]);
                END_FOR;
                (* B * u_plan term *)
                FOR kLoopIndex := 1 TO 5 DO
                    x_pred[iHor + 1, iRow] := x_pred[iHor + 1, iRow] + (B_mat[iRow, kLoopIndex] * u_plan[iHor, kLoopIndex]);
                END_FOR;
            END_FOR;
        END_FOR;

        (* STEP 2: TERMINAL ADJOINT COSTATE CALCULATION (k = 5)
           lambda[5] = P * (x_pred[5] - x_ref) *)
        FOR iRow := 1 TO 6 DO
            lambda_costate[5, iRow] := 0.0;
            FOR jLoopIndex := 1 TO 6 DO
                lambda_costate[5, iRow] := lambda_costate[5, iRow] + (P_mat[iRow, jLoopIndex] * (x_pred[5, jLoopIndex] - x_ref[jLoopIndex]));
            END_FOR;
        END_FOR;

        (* STEP 3: BACKWARD ADJOINT COSTATE PROPAGATION (k = 4 DOWNTO 0)
           lambda[k] = Q * (x_pred[k] - x_ref) + A' * lambda[k+1] *)
        FOR iHor := 4 DOWNTO 0 DO
            FOR iRow := 1 TO 6 DO
                lambda_costate[iHor, iRow] := 0.0;
                (* State deviation penalty term: Q * (x_pred - x_ref) *)
                FOR jLoopIndex := 1 TO 6 DO
                    lambda_costate[iHor, iRow] := lambda_costate[iHor, iRow] + (Q_mat[iRow, jLoopIndex] * (x_pred[iHor, jLoopIndex] - x_ref[jLoopIndex]));
                END_FOR;
                (* Adjoint backward transition term: A' * lambda[k+1] *)
                FOR jLoopIndex := 1 TO 6 DO
                    lambda_costate[iHor, iRow] := lambda_costate[iHor, iRow] + (A_mat[jLoopIndex, iRow] * lambda_costate[iHor + 1, jLoopIndex]);
                END_FOR;
            END_FOR;
        END_FOR;

        (* STEP 4: GRADIENT COMPUTATION & PROJECTED INPUT UPDATE ACROSS HORIZON (k = 0 TO 4)
           grad[k] = R * u_plan[k] + S * (u_plan[k] - u_prev) + B' * lambda[k+1]
           u_plan[k] = Project( u_plan[k] - alpha * grad[k] ) *)
        FOR iHor := 0 TO 4 DO
            FOR kLoopIndex := 1 TO 5 DO
                grad_cost[iHor, kLoopIndex] := 0.0;
                (* Actuator effort penalty: R * u_plan *)
                FOR jLoopIndex := 1 TO 5 DO
                    grad_cost[iHor, kLoopIndex] := grad_cost[iHor, kLoopIndex] + (R_mat[kLoopIndex, jLoopIndex] * u_plan[iHor, jLoopIndex]);
                END_FOR;
                (* Actuator slew rate damping: S * (u_plan - u_prev) *)
                IF iHor = 0 THEN
                    grad_cost[iHor, kLoopIndex] := grad_cost[iHor, kLoopIndex] + (S_mat[kLoopIndex, kLoopIndex] * (u_plan[0, kLoopIndex] - u_prev[kLoopIndex]));
                ELSE
                    grad_cost[iHor, kLoopIndex] := grad_cost[iHor, kLoopIndex] + (S_mat[kLoopIndex, kLoopIndex] * (u_plan[iHor, kLoopIndex] - u_plan[iHor - 1, kLoopIndex]));
                END_IF;
                (* Input coupling term: B' * lambda[k+1] *)
                FOR jLoopIndex := 1 TO 6 DO
                    grad_cost[iHor, kLoopIndex] := grad_cost[iHor, kLoopIndex] + (B_mat[jLoopIndex, kLoopIndex] * lambda_costate[iHor + 1, jLoopIndex]);
                END_FOR;

                (* Gradient descent step update *)
                u_plan[iHor, kLoopIndex] := u_plan[iHor, kLoopIndex] - (alpha_pgd_step * grad_cost[iHor, kLoopIndex]);

                (* SATURATION & BOX CONSTRAINT PROJECTION *)
                IF u_plan[iHor, kLoopIndex] < u_min[kLoopIndex] THEN
                    u_plan[iHor, kLoopIndex] := u_min[kLoopIndex];
                ELSIF u_plan[iHor, kLoopIndex] > u_max[kLoopIndex] THEN
                    u_plan[iHor, kLoopIndex] := u_max[kLoopIndex];
                END_IF;

                (* SLEW RATE CONSTRAINT PROJECTION FOR STEP 0 *)
                IF iHor = 0 THEN
                    IF (u_plan[0, kLoopIndex] - u_prev[kLoopIndex]) > du_max[kLoopIndex] THEN
                        u_plan[0, kLoopIndex] := u_prev[kLoopIndex] + du_max[kLoopIndex];
                    ELSIF (u_plan[0, kLoopIndex] - u_prev[kLoopIndex]) < -du_max[kLoopIndex] THEN
                        u_plan[0, kLoopIndex] := u_prev[kLoopIndex] - du_max[kLoopIndex];
                    END_IF;
                END_IF;
            END_FOR;

            (* DYNAMIC VORONKOV DEFECT-FREE (v/G) RATIO CONSTRAINT PROJECTION ON PULL SPEED (u1)
               During nominal equal-diameter body growth, constrain crystal pull rate to:
                 0.200 * G_0 <= v_pull <= 0.240 * G_0 *)
            IF iCurrentFSMState = STATE_BODY_EQUAL_DIAMETER_GROWTH_MPC_ACTIVE THEN
                IF u_plan[iHor, 1] < (xi_window_min * rInterfaceAxialGradient_G0) THEN
                    u_plan[iHor, 1] := xi_window_min * rInterfaceAxialGradient_G0;
                ELSIF u_plan[iHor, 1] > (xi_window_max * rInterfaceAxialGradient_G0) THEN
                    u_plan[iHor, 1] := xi_window_max * rInterfaceAxialGradient_G0;
                END_IF;
            END_IF;

        END_FOR;

    END_FOR; (* End of 10 PGD iterations *)

    (* Assign first control action from receding horizon to system actuators *)
    u_cmd[1] := u_plan[0, 1]; (* Crystal Pull Servo Speed [mm/min] *)
    u_cmd[2] := u_plan[0, 2]; (* Main Graphite Heater Power [kW] *)
    u_cmd[3] := u_plan[0, 3]; (* Bottom Crucible Lift Speed [mm/min] *)
    u_cmd[4] := u_plan[0, 4]; (* Top/Bottom Cusp Field Coil Current [A] *)
    u_cmd[5] := u_plan[0, 5]; (* Crystal Seed Rotation Speed [RPM] *)

ELSE
    (* MPC inactive during preparation, meltdown, dipping, or emergency trip phases.
       Individual FSM states govern open-loop feedforward ramps. *)
    FOR kLoopIndex := 1 TO 5 DO
        u_plan[0, kLoopIndex] := u_cmd[kLoopIndex];
    END_FOR;
END_IF;

(* Compute actual actuator slew rates for telemetry *)
FOR kLoopIndex := 1 TO 5 DO
    u_rate[kLoopIndex] := (u_cmd[kLoopIndex] - u_prev[kLoopIndex]) / rCycleTimeSec;
    u_prev[kLoopIndex] := u_cmd[kLoopIndex];
END_FOR;"""
