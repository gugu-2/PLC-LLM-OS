# -*- coding: utf-8 -*-
"""
cement_kiln_builder/part5_mpc_optimization.py
Part 5: Phase 3 - Receding-Horizon MPC Optimization with 10 Unrolled PGD Iterations
Explicit unrolled projected gradient descent, adjoint costates, quadratic stage cost,
actuator saturation clamping, and dynamic slew rate limit enforcement.
"""

def get_part5_mpc_optimization():
    return """
(* ========================================================================================================= *)
(* === PHASE 3: RECEDING-HORIZON MPC OPTIMIZATION WITH 10 UNROLLED PGD ITERATIONS                        === *)
(* ========================================================================================================= *)

(* Initialize MPC Candidate Actuator Vector with Previous Solution / Warm Start *)
rActuator_u_opt[1] := rActuator_u[1];
rActuator_u_opt[2] := rActuator_u[2];
rActuator_u_opt[3] := rActuator_u[3];
rActuator_u_opt[4] := rActuator_u[4];
rActuator_u_opt[5] := rActuator_u[5];

(* --------------------------------------------------------------------------------------------------------- *)
(* PGD ITERATION 1 (UNROLLED)                                                                                *)
(* --------------------------------------------------------------------------------------------------------- *)
(* Forward State Simulation with Candidate u *)
FOR rLoop_idx_i := 1 TO 6 DO
    rState_Iter[rLoop_idx_i] := (A[rLoop_idx_i, 1] * rState_x_hat[1]) + (A[rLoop_idx_i, 2] * rState_x_hat[2]) +
                                (A[rLoop_idx_i, 3] * rState_x_hat[3]) + (A[rLoop_idx_i, 4] * rState_x_hat[4]) +
                                (A[rLoop_idx_i, 5] * rState_x_hat[5]) + (A[rLoop_idx_i, 6] * rState_x_hat[6]) +
                                (B[rLoop_idx_i, 1] * rActuator_u_opt[1]) + (B[rLoop_idx_i, 2] * rActuator_u_opt[2]) +
                                (B[rLoop_idx_i, 3] * rActuator_u_opt[3]) + (B[rLoop_idx_i, 4] * rActuator_u_opt[4]) +
                                (B[rLoop_idx_i, 5] * rActuator_u_opt[5]);
END_FOR;

(* Adjoint Costate Vector lambda = P * (x_iter - x_ref) + Q * (x_iter - x_ref) *)
FOR rLoop_idx_i := 1 TO 6 DO
    rCostate_lambda[rLoop_idx_i] := (P[rLoop_idx_i, rLoop_idx_i] + Q[rLoop_idx_i, rLoop_idx_i]) * (rState_Iter[rLoop_idx_i] - rState_x_ref[rLoop_idx_i]);
END_FOR;

(* Objective Gradient w.r.t Actuators grad_u = R * u + S * (u - u_prev) + B' * lambda *)
FOR rLoop_idx_m := 1 TO 5 DO
    rGradient_grad_u[rLoop_idx_m] := (R[rLoop_idx_m, rLoop_idx_m] * rActuator_u_opt[rLoop_idx_m]) +
                                     (S[rLoop_idx_m, rLoop_idx_m] * (rActuator_u_opt[rLoop_idx_m] - rActuator_u_prev[rLoop_idx_m])) +
                                     (B[1, rLoop_idx_m] * rCostate_lambda[1]) +
                                     (B[2, rLoop_idx_m] * rCostate_lambda[2]) +
                                     (B[3, rLoop_idx_m] * rCostate_lambda[3]) +
                                     (B[4, rLoop_idx_m] * rCostate_lambda[4]) +
                                     (B[5, rLoop_idx_m] * rCostate_lambda[5]) +
                                     (B[6, rLoop_idx_m] * rCostate_lambda[6]);
    
    (* Projected Gradient Step *)
    rPGD_Temp_u[rLoop_idx_m] := rActuator_u_opt[rLoop_idx_m] - (rPGD_Alpha * rGradient_grad_u[rLoop_idx_m]);
    
    (* Hard Saturation Projection *)
    rPGD_Temp_u[rLoop_idx_m] := LIMIT(rActuator_u_min[rLoop_idx_m], rPGD_Temp_u[rLoop_idx_m], rActuator_u_max[rLoop_idx_m]);
    
    (* Hard Dynamic Slew Rate Projection *)
    rActuator_u_opt[rLoop_idx_m] := LIMIT(rActuator_u_prev[rLoop_idx_m] - rActuator_du_max[rLoop_idx_m],
                                          rPGD_Temp_u[rLoop_idx_m],
                                          rActuator_u_prev[rLoop_idx_m] + rActuator_du_max[rLoop_idx_m]);
END_FOR;

(* --------------------------------------------------------------------------------------------------------- *)
(* PGD ITERATION 2 (UNROLLED)                                                                                *)
(* --------------------------------------------------------------------------------------------------------- *)
FOR rLoop_idx_i := 1 TO 6 DO
    rState_Iter[rLoop_idx_i] := (A[rLoop_idx_i, 1] * rState_x_hat[1]) + (A[rLoop_idx_i, 2] * rState_x_hat[2]) +
                                (A[rLoop_idx_i, 3] * rState_x_hat[3]) + (A[rLoop_idx_i, 4] * rState_x_hat[4]) +
                                (A[rLoop_idx_i, 5] * rState_x_hat[5]) + (A[rLoop_idx_i, 6] * rState_x_hat[6]) +
                                (B[rLoop_idx_i, 1] * rActuator_u_opt[1]) + (B[rLoop_idx_i, 2] * rActuator_u_opt[2]) +
                                (B[rLoop_idx_i, 3] * rActuator_u_opt[3]) + (B[rLoop_idx_i, 4] * rActuator_u_opt[4]) +
                                (B[rLoop_idx_i, 5] * rActuator_u_opt[5]);
    rCostate_lambda[rLoop_idx_i] := (P[rLoop_idx_i, rLoop_idx_i] + Q[rLoop_idx_i, rLoop_idx_i]) * (rState_Iter[rLoop_idx_i] - rState_x_ref[rLoop_idx_i]);
END_FOR;

FOR rLoop_idx_m := 1 TO 5 DO
    rGradient_grad_u[rLoop_idx_m] := (R[rLoop_idx_m, rLoop_idx_m] * rActuator_u_opt[rLoop_idx_m]) +
                                     (S[rLoop_idx_m, rLoop_idx_m] * (rActuator_u_opt[rLoop_idx_m] - rActuator_u_prev[rLoop_idx_m])) +
                                     (B[1, rLoop_idx_m] * rCostate_lambda[1]) +
                                     (B[2, rLoop_idx_m] * rCostate_lambda[2]) +
                                     (B[3, rLoop_idx_m] * rCostate_lambda[3]) +
                                     (B[4, rLoop_idx_m] * rCostate_lambda[4]) +
                                     (B[5, rLoop_idx_m] * rCostate_lambda[5]) +
                                     (B[6, rLoop_idx_m] * rCostate_lambda[6]);
    rPGD_Temp_u[rLoop_idx_m] := rActuator_u_opt[rLoop_idx_m] - (rPGD_Alpha * rGradient_grad_u[rLoop_idx_m]);
    rPGD_Temp_u[rLoop_idx_m] := LIMIT(rActuator_u_min[rLoop_idx_m], rPGD_Temp_u[rLoop_idx_m], rActuator_u_max[rLoop_idx_m]);
    rActuator_u_opt[rLoop_idx_m] := LIMIT(rActuator_u_prev[rLoop_idx_m] - rActuator_du_max[rLoop_idx_m],
                                          rPGD_Temp_u[rLoop_idx_m],
                                          rActuator_u_prev[rLoop_idx_m] + rActuator_du_max[rLoop_idx_m]);
END_FOR;

(* --------------------------------------------------------------------------------------------------------- *)
(* PGD ITERATION 3 (UNROLLED)                                                                                *)
(* --------------------------------------------------------------------------------------------------------- *)
FOR rLoop_idx_i := 1 TO 6 DO
    rState_Iter[rLoop_idx_i] := (A[rLoop_idx_i, 1] * rState_x_hat[1]) + (A[rLoop_idx_i, 2] * rState_x_hat[2]) +
                                (A[rLoop_idx_i, 3] * rState_x_hat[3]) + (A[rLoop_idx_i, 4] * rState_x_hat[4]) +
                                (A[rLoop_idx_i, 5] * rState_x_hat[5]) + (A[rLoop_idx_i, 6] * rState_x_hat[6]) +
                                (B[rLoop_idx_i, 1] * rActuator_u_opt[1]) + (B[rLoop_idx_i, 2] * rActuator_u_opt[2]) +
                                (B[rLoop_idx_i, 3] * rActuator_u_opt[3]) + (B[rLoop_idx_i, 4] * rActuator_u_opt[4]) +
                                (B[rLoop_idx_i, 5] * rActuator_u_opt[5]);
    rCostate_lambda[rLoop_idx_i] := (P[rLoop_idx_i, rLoop_idx_i] + Q[rLoop_idx_i, rLoop_idx_i]) * (rState_Iter[rLoop_idx_i] - rState_x_ref[rLoop_idx_i]);
END_FOR;

FOR rLoop_idx_m := 1 TO 5 DO
    rGradient_grad_u[rLoop_idx_m] := (R[rLoop_idx_m, rLoop_idx_m] * rActuator_u_opt[rLoop_idx_m]) +
                                     (S[rLoop_idx_m, rLoop_idx_m] * (rActuator_u_opt[rLoop_idx_m] - rActuator_u_prev[rLoop_idx_m])) +
                                     (B[1, rLoop_idx_m] * rCostate_lambda[1]) +
                                     (B[2, rLoop_idx_m] * rCostate_lambda[2]) +
                                     (B[3, rLoop_idx_m] * rCostate_lambda[3]) +
                                     (B[4, rLoop_idx_m] * rCostate_lambda[4]) +
                                     (B[5, rLoop_idx_m] * rCostate_lambda[5]) +
                                     (B[6, rLoop_idx_m] * rCostate_lambda[6]);
    rPGD_Temp_u[rLoop_idx_m] := rActuator_u_opt[rLoop_idx_m] - (rPGD_Alpha * rGradient_grad_u[rLoop_idx_m]);
    rPGD_Temp_u[rLoop_idx_m] := LIMIT(rActuator_u_min[rLoop_idx_m], rPGD_Temp_u[rLoop_idx_m], rActuator_u_max[rLoop_idx_m]);
    rActuator_u_opt[rLoop_idx_m] := LIMIT(rActuator_u_prev[rLoop_idx_m] - rActuator_du_max[rLoop_idx_m],
                                          rPGD_Temp_u[rLoop_idx_m],
                                          rActuator_u_prev[rLoop_idx_m] + rActuator_du_max[rLoop_idx_m]);
END_FOR;

(* --------------------------------------------------------------------------------------------------------- *)
(* PGD ITERATION 4 (UNROLLED)                                                                                *)
(* --------------------------------------------------------------------------------------------------------- *)
FOR rLoop_idx_i := 1 TO 6 DO
    rState_Iter[rLoop_idx_i] := (A[rLoop_idx_i, 1] * rState_x_hat[1]) + (A[rLoop_idx_i, 2] * rState_x_hat[2]) +
                                (A[rLoop_idx_i, 3] * rState_x_hat[3]) + (A[rLoop_idx_i, 4] * rState_x_hat[4]) +
                                (A[rLoop_idx_i, 5] * rState_x_hat[5]) + (A[rLoop_idx_i, 6] * rState_x_hat[6]) +
                                (B[rLoop_idx_i, 1] * rActuator_u_opt[1]) + (B[rLoop_idx_i, 2] * rActuator_u_opt[2]) +
                                (B[rLoop_idx_i, 3] * rActuator_u_opt[3]) + (B[rLoop_idx_i, 4] * rActuator_u_opt[4]) +
                                (B[rLoop_idx_i, 5] * rActuator_u_opt[5]);
    rCostate_lambda[rLoop_idx_i] := (P[rLoop_idx_i, rLoop_idx_i] + Q[rLoop_idx_i, rLoop_idx_i]) * (rState_Iter[rLoop_idx_i] - rState_x_ref[rLoop_idx_i]);
END_FOR;

FOR rLoop_idx_m := 1 TO 5 DO
    rGradient_grad_u[rLoop_idx_m] := (R[rLoop_idx_m, rLoop_idx_m] * rActuator_u_opt[rLoop_idx_m]) +
                                     (S[rLoop_idx_m, rLoop_idx_m] * (rActuator_u_opt[rLoop_idx_m] - rActuator_u_prev[rLoop_idx_m])) +
                                     (B[1, rLoop_idx_m] * rCostate_lambda[1]) +
                                     (B[2, rLoop_idx_m] * rCostate_lambda[2]) +
                                     (B[3, rLoop_idx_m] * rCostate_lambda[3]) +
                                     (B[4, rLoop_idx_m] * rCostate_lambda[4]) +
                                     (B[5, rLoop_idx_m] * rCostate_lambda[5]) +
                                     (B[6, rLoop_idx_m] * rCostate_lambda[6]);
    rPGD_Temp_u[rLoop_idx_m] := rActuator_u_opt[rLoop_idx_m] - (rPGD_Alpha * rGradient_grad_u[rLoop_idx_m]);
    rPGD_Temp_u[rLoop_idx_m] := LIMIT(rActuator_u_min[rLoop_idx_m], rPGD_Temp_u[rLoop_idx_m], rActuator_u_max[rLoop_idx_m]);
    rActuator_u_opt[rLoop_idx_m] := LIMIT(rActuator_u_prev[rLoop_idx_m] - rActuator_du_max[rLoop_idx_m],
                                          rPGD_Temp_u[rLoop_idx_m],
                                          rActuator_u_prev[rLoop_idx_m] + rActuator_du_max[rLoop_idx_m]);
END_FOR;

(* --------------------------------------------------------------------------------------------------------- *)
(* PGD ITERATION 5 (UNROLLED)                                                                                *)
(* --------------------------------------------------------------------------------------------------------- *)
FOR rLoop_idx_i := 1 TO 6 DO
    rState_Iter[rLoop_idx_i] := (A[rLoop_idx_i, 1] * rState_x_hat[1]) + (A[rLoop_idx_i, 2] * rState_x_hat[2]) +
                                (A[rLoop_idx_i, 3] * rState_x_hat[3]) + (A[rLoop_idx_i, 4] * rState_x_hat[4]) +
                                (A[rLoop_idx_i, 5] * rState_x_hat[5]) + (A[rLoop_idx_i, 6] * rState_x_hat[6]) +
                                (B[rLoop_idx_i, 1] * rActuator_u_opt[1]) + (B[rLoop_idx_i, 2] * rActuator_u_opt[2]) +
                                (B[rLoop_idx_i, 3] * rActuator_u_opt[3]) + (B[rLoop_idx_i, 4] * rActuator_u_opt[4]) +
                                (B[rLoop_idx_i, 5] * rActuator_u_opt[5]);
    rCostate_lambda[rLoop_idx_i] := (P[rLoop_idx_i, rLoop_idx_i] + Q[rLoop_idx_i, rLoop_idx_i]) * (rState_Iter[rLoop_idx_i] - rState_x_ref[rLoop_idx_i]);
END_FOR;

FOR rLoop_idx_m := 1 TO 5 DO
    rGradient_grad_u[rLoop_idx_m] := (R[rLoop_idx_m, rLoop_idx_m] * rActuator_u_opt[rLoop_idx_m]) +
                                     (S[rLoop_idx_m, rLoop_idx_m] * (rActuator_u_opt[rLoop_idx_m] - rActuator_u_prev[rLoop_idx_m])) +
                                     (B[1, rLoop_idx_m] * rCostate_lambda[1]) +
                                     (B[2, rLoop_idx_m] * rCostate_lambda[2]) +
                                     (B[3, rLoop_idx_m] * rCostate_lambda[3]) +
                                     (B[4, rLoop_idx_m] * rCostate_lambda[4]) +
                                     (B[5, rLoop_idx_m] * rCostate_lambda[5]) +
                                     (B[6, rLoop_idx_m] * rCostate_lambda[6]);
    rPGD_Temp_u[rLoop_idx_m] := rActuator_u_opt[rLoop_idx_m] - (rPGD_Alpha * rGradient_grad_u[rLoop_idx_m]);
    rPGD_Temp_u[rLoop_idx_m] := LIMIT(rActuator_u_min[rLoop_idx_m], rPGD_Temp_u[rLoop_idx_m], rActuator_u_max[rLoop_idx_m]);
    rActuator_u_opt[rLoop_idx_m] := LIMIT(rActuator_u_prev[rLoop_idx_m] - rActuator_du_max[rLoop_idx_m],
                                          rPGD_Temp_u[rLoop_idx_m],
                                          rActuator_u_prev[rLoop_idx_m] + rActuator_du_max[rLoop_idx_m]);
END_FOR;

(* --------------------------------------------------------------------------------------------------------- *)
(* PGD ITERATION 6 (UNROLLED)                                                                                *)
(* --------------------------------------------------------------------------------------------------------- *)
FOR rLoop_idx_i := 1 TO 6 DO
    rState_Iter[rLoop_idx_i] := (A[rLoop_idx_i, 1] * rState_x_hat[1]) + (A[rLoop_idx_i, 2] * rState_x_hat[2]) +
                                (A[rLoop_idx_i, 3] * rState_x_hat[3]) + (A[rLoop_idx_i, 4] * rState_x_hat[4]) +
                                (A[rLoop_idx_i, 5] * rState_x_hat[5]) + (A[rLoop_idx_i, 6] * rState_x_hat[6]) +
                                (B[rLoop_idx_i, 1] * rActuator_u_opt[1]) + (B[rLoop_idx_i, 2] * rActuator_u_opt[2]) +
                                (B[rLoop_idx_i, 3] * rActuator_u_opt[3]) + (B[rLoop_idx_i, 4] * rActuator_u_opt[4]) +
                                (B[rLoop_idx_i, 5] * rActuator_u_opt[5]);
    rCostate_lambda[rLoop_idx_i] := (P[rLoop_idx_i, rLoop_idx_i] + Q[rLoop_idx_i, rLoop_idx_i]) * (rState_Iter[rLoop_idx_i] - rState_x_ref[rLoop_idx_i]);
END_FOR;

FOR rLoop_idx_m := 1 TO 5 DO
    rGradient_grad_u[rLoop_idx_m] := (R[rLoop_idx_m, rLoop_idx_m] * rActuator_u_opt[rLoop_idx_m]) +
                                     (S[rLoop_idx_m, rLoop_idx_m] * (rActuator_u_opt[rLoop_idx_m] - rActuator_u_prev[rLoop_idx_m])) +
                                     (B[1, rLoop_idx_m] * rCostate_lambda[1]) +
                                     (B[2, rLoop_idx_m] * rCostate_lambda[2]) +
                                     (B[3, rLoop_idx_m] * rCostate_lambda[3]) +
                                     (B[4, rLoop_idx_m] * rCostate_lambda[4]) +
                                     (B[5, rLoop_idx_m] * rCostate_lambda[5]) +
                                     (B[6, rLoop_idx_m] * rCostate_lambda[6]);
    rPGD_Temp_u[rLoop_idx_m] := rActuator_u_opt[rLoop_idx_m] - (rPGD_Alpha * rGradient_grad_u[rLoop_idx_m]);
    rPGD_Temp_u[rLoop_idx_m] := LIMIT(rActuator_u_min[rLoop_idx_m], rPGD_Temp_u[rLoop_idx_m], rActuator_u_max[rLoop_idx_m]);
    rActuator_u_opt[rLoop_idx_m] := LIMIT(rActuator_u_prev[rLoop_idx_m] - rActuator_du_max[rLoop_idx_m],
                                          rPGD_Temp_u[rLoop_idx_m],
                                          rActuator_u_prev[rLoop_idx_m] + rActuator_du_max[rLoop_idx_m]);
END_FOR;

(* --------------------------------------------------------------------------------------------------------- *)
(* PGD ITERATION 7 (UNROLLED)                                                                                *)
(* --------------------------------------------------------------------------------------------------------- *)
FOR rLoop_idx_i := 1 TO 6 DO
    rState_Iter[rLoop_idx_i] := (A[rLoop_idx_i, 1] * rState_x_hat[1]) + (A[rLoop_idx_i, 2] * rState_x_hat[2]) +
                                (A[rLoop_idx_i, 3] * rState_x_hat[3]) + (A[rLoop_idx_i, 4] * rState_x_hat[4]) +
                                (A[rLoop_idx_i, 5] * rState_x_hat[5]) + (A[rLoop_idx_i, 6] * rState_x_hat[6]) +
                                (B[rLoop_idx_i, 1] * rActuator_u_opt[1]) + (B[rLoop_idx_i, 2] * rActuator_u_opt[2]) +
                                (B[rLoop_idx_i, 3] * rActuator_u_opt[3]) + (B[rLoop_idx_i, 4] * rActuator_u_opt[4]) +
                                (B[rLoop_idx_i, 5] * rActuator_u_opt[5]);
    rCostate_lambda[rLoop_idx_i] := (P[rLoop_idx_i, rLoop_idx_i] + Q[rLoop_idx_i, rLoop_idx_i]) * (rState_Iter[rLoop_idx_i] - rState_x_ref[rLoop_idx_i]);
END_FOR;

FOR rLoop_idx_m := 1 TO 5 DO
    rGradient_grad_u[rLoop_idx_m] := (R[rLoop_idx_m, rLoop_idx_m] * rActuator_u_opt[rLoop_idx_m]) +
                                     (S[rLoop_idx_m, rLoop_idx_m] * (rActuator_u_opt[rLoop_idx_m] - rActuator_u_prev[rLoop_idx_m])) +
                                     (B[1, rLoop_idx_m] * rCostate_lambda[1]) +
                                     (B[2, rLoop_idx_m] * rCostate_lambda[2]) +
                                     (B[3, rLoop_idx_m] * rCostate_lambda[3]) +
                                     (B[4, rLoop_idx_m] * rCostate_lambda[4]) +
                                     (B[5, rLoop_idx_m] * rCostate_lambda[5]) +
                                     (B[6, rLoop_idx_m] * rCostate_lambda[6]);
    rPGD_Temp_u[rLoop_idx_m] := rActuator_u_opt[rLoop_idx_m] - (rPGD_Alpha * rGradient_grad_u[rLoop_idx_m]);
    rPGD_Temp_u[rLoop_idx_m] := LIMIT(rActuator_u_min[rLoop_idx_m], rPGD_Temp_u[rLoop_idx_m], rActuator_u_max[rLoop_idx_m]);
    rActuator_u_opt[rLoop_idx_m] := LIMIT(rActuator_u_prev[rLoop_idx_m] - rActuator_du_max[rLoop_idx_m],
                                          rPGD_Temp_u[rLoop_idx_m],
                                          rActuator_u_prev[rLoop_idx_m] + rActuator_du_max[rLoop_idx_m]);
END_FOR;

(* --------------------------------------------------------------------------------------------------------- *)
(* PGD ITERATION 8 (UNROLLED)                                                                                *)
(* --------------------------------------------------------------------------------------------------------- *)
FOR rLoop_idx_i := 1 TO 6 DO
    rState_Iter[rLoop_idx_i] := (A[rLoop_idx_i, 1] * rState_x_hat[1]) + (A[rLoop_idx_i, 2] * rState_x_hat[2]) +
                                (A[rLoop_idx_i, 3] * rState_x_hat[3]) + (A[rLoop_idx_i, 4] * rState_x_hat[4]) +
                                (A[rLoop_idx_i, 5] * rState_x_hat[5]) + (A[rLoop_idx_i, 6] * rState_x_hat[6]) +
                                (B[rLoop_idx_i, 1] * rActuator_u_opt[1]) + (B[rLoop_idx_i, 2] * rActuator_u_opt[2]) +
                                (B[rLoop_idx_i, 3] * rActuator_u_opt[3]) + (B[rLoop_idx_i, 4] * rActuator_u_opt[4]) +
                                (B[rLoop_idx_i, 5] * rActuator_u_opt[5]);
    rCostate_lambda[rLoop_idx_i] := (P[rLoop_idx_i, rLoop_idx_i] + Q[rLoop_idx_i, rLoop_idx_i]) * (rState_Iter[rLoop_idx_i] - rState_x_ref[rLoop_idx_i]);
END_FOR;

FOR rLoop_idx_m := 1 TO 5 DO
    rGradient_grad_u[rLoop_idx_m] := (R[rLoop_idx_m, rLoop_idx_m] * rActuator_u_opt[rLoop_idx_m]) +
                                     (S[rLoop_idx_m, rLoop_idx_m] * (rActuator_u_opt[rLoop_idx_m] - rActuator_u_prev[rLoop_idx_m])) +
                                     (B[1, rLoop_idx_m] * rCostate_lambda[1]) +
                                     (B[2, rLoop_idx_m] * rCostate_lambda[2]) +
                                     (B[3, rLoop_idx_m] * rCostate_lambda[3]) +
                                     (B[4, rLoop_idx_m] * rCostate_lambda[4]) +
                                     (B[5, rLoop_idx_m] * rCostate_lambda[5]) +
                                     (B[6, rLoop_idx_m] * rCostate_lambda[6]);
    rPGD_Temp_u[rLoop_idx_m] := rActuator_u_opt[rLoop_idx_m] - (rPGD_Alpha * rGradient_grad_u[rLoop_idx_m]);
    rPGD_Temp_u[rLoop_idx_m] := LIMIT(rActuator_u_min[rLoop_idx_m], rPGD_Temp_u[rLoop_idx_m], rActuator_u_max[rLoop_idx_m]);
    rActuator_u_opt[rLoop_idx_m] := LIMIT(rActuator_u_prev[rLoop_idx_m] - rActuator_du_max[rLoop_idx_m],
                                          rPGD_Temp_u[rLoop_idx_m],
                                          rActuator_u_prev[rLoop_idx_m] + rActuator_du_max[rLoop_idx_m]);
END_FOR;

(* --------------------------------------------------------------------------------------------------------- *)
(* PGD ITERATION 9 (UNROLLED)                                                                                *)
(* --------------------------------------------------------------------------------------------------------- *)
FOR rLoop_idx_i := 1 TO 6 DO
    rState_Iter[rLoop_idx_i] := (A[rLoop_idx_i, 1] * rState_x_hat[1]) + (A[rLoop_idx_i, 2] * rState_x_hat[2]) +
                                (A[rLoop_idx_i, 3] * rState_x_hat[3]) + (A[rLoop_idx_i, 4] * rState_x_hat[4]) +
                                (A[rLoop_idx_i, 5] * rState_x_hat[5]) + (A[rLoop_idx_i, 6] * rState_x_hat[6]) +
                                (B[rLoop_idx_i, 1] * rActuator_u_opt[1]) + (B[rLoop_idx_i, 2] * rActuator_u_opt[2]) +
                                (B[rLoop_idx_i, 3] * rActuator_u_opt[3]) + (B[rLoop_idx_i, 4] * rActuator_u_opt[4]) +
                                (B[rLoop_idx_i, 5] * rActuator_u_opt[5]);
    rCostate_lambda[rLoop_idx_i] := (P[rLoop_idx_i, rLoop_idx_i] + Q[rLoop_idx_i, rLoop_idx_i]) * (rState_Iter[rLoop_idx_i] - rState_x_ref[rLoop_idx_i]);
END_FOR;

FOR rLoop_idx_m := 1 TO 5 DO
    rGradient_grad_u[rLoop_idx_m] := (R[rLoop_idx_m, rLoop_idx_m] * rActuator_u_opt[rLoop_idx_m]) +
                                     (S[rLoop_idx_m, rLoop_idx_m] * (rActuator_u_opt[rLoop_idx_m] - rActuator_u_prev[rLoop_idx_m])) +
                                     (B[1, rLoop_idx_m] * rCostate_lambda[1]) +
                                     (B[2, rLoop_idx_m] * rCostate_lambda[2]) +
                                     (B[3, rLoop_idx_m] * rCostate_lambda[3]) +
                                     (B[4, rLoop_idx_m] * rCostate_lambda[4]) +
                                     (B[5, rLoop_idx_m] * rCostate_lambda[5]) +
                                     (B[6, rLoop_idx_m] * rCostate_lambda[6]);
    rPGD_Temp_u[rLoop_idx_m] := rActuator_u_opt[rLoop_idx_m] - (rPGD_Alpha * rGradient_grad_u[rLoop_idx_m]);
    rPGD_Temp_u[rLoop_idx_m] := LIMIT(rActuator_u_min[rLoop_idx_m], rPGD_Temp_u[rLoop_idx_m], rActuator_u_max[rLoop_idx_m]);
    rActuator_u_opt[rLoop_idx_m] := LIMIT(rActuator_u_prev[rLoop_idx_m] - rActuator_du_max[rLoop_idx_m],
                                          rPGD_Temp_u[rLoop_idx_m],
                                          rActuator_u_prev[rLoop_idx_m] + rActuator_du_max[rLoop_idx_m]);
END_FOR;

(* --------------------------------------------------------------------------------------------------------- *)
(* PGD ITERATION 10 (FINAL UNROLLED TERMINATION STEP)                                                        *)
(* --------------------------------------------------------------------------------------------------------- *)
FOR rLoop_idx_i := 1 TO 6 DO
    rState_Iter[rLoop_idx_i] := (A[rLoop_idx_i, 1] * rState_x_hat[1]) + (A[rLoop_idx_i, 2] * rState_x_hat[2]) +
                                (A[rLoop_idx_i, 3] * rState_x_hat[3]) + (A[rLoop_idx_i, 4] * rState_x_hat[4]) +
                                (A[rLoop_idx_i, 5] * rState_x_hat[5]) + (A[rLoop_idx_i, 6] * rState_x_hat[6]) +
                                (B[rLoop_idx_i, 1] * rActuator_u_opt[1]) + (B[rLoop_idx_i, 2] * rActuator_u_opt[2]) +
                                (B[rLoop_idx_i, 3] * rActuator_u_opt[3]) + (B[rLoop_idx_i, 4] * rActuator_u_opt[4]) +
                                (B[rLoop_idx_i, 5] * rActuator_u_opt[5]);
    rCostate_lambda[rLoop_idx_i] := (P[rLoop_idx_i, rLoop_idx_i] + Q[rLoop_idx_i, rLoop_idx_i]) * (rState_Iter[rLoop_idx_i] - rState_x_ref[rLoop_idx_i]);
END_FOR;

FOR rLoop_idx_m := 1 TO 5 DO
    rGradient_grad_u[rLoop_idx_m] := (R[rLoop_idx_m, rLoop_idx_m] * rActuator_u_opt[rLoop_idx_m]) +
                                     (S[rLoop_idx_m, rLoop_idx_m] * (rActuator_u_opt[rLoop_idx_m] - rActuator_u_prev[rLoop_idx_m])) +
                                     (B[1, rLoop_idx_m] * rCostate_lambda[1]) +
                                     (B[2, rLoop_idx_m] * rCostate_lambda[2]) +
                                     (B[3, rLoop_idx_m] * rCostate_lambda[3]) +
                                     (B[4, rLoop_idx_m] * rCostate_lambda[4]) +
                                     (B[5, rLoop_idx_m] * rCostate_lambda[5]) +
                                     (B[6, rLoop_idx_m] * rCostate_lambda[6]);
    rPGD_Temp_u[rLoop_idx_m] := rActuator_u_opt[rLoop_idx_m] - (rPGD_Alpha * rGradient_grad_u[rLoop_idx_m]);
    rPGD_Temp_u[rLoop_idx_m] := LIMIT(rActuator_u_min[rLoop_idx_m], rPGD_Temp_u[rLoop_idx_m], rActuator_u_max[rLoop_idx_m]);
    rActuator_u_opt[rLoop_idx_m] := LIMIT(rActuator_u_prev[rLoop_idx_m] - rActuator_du_max[rLoop_idx_m],
                                          rPGD_Temp_u[rLoop_idx_m],
                                          rActuator_u_prev[rLoop_idx_m] + rActuator_du_max[rLoop_idx_m]);
END_FOR;

(* Dynamic Constraint Trim: Suppress Kiln Inlet CO and Prevent Ring Coating Build-up *)
IF rState_x_hat[6] > 0.15 THEN
    (* Bias ID fan open and trim coal feed to ensure excess combustion oxygen *)
    rActuator_u_opt[4] := MIN(rActuator_u_max[4], rActuator_u_opt[4] + 1.2);
    rActuator_u_opt[1] := MAX(rActuator_u_min[1], rActuator_u_opt[1] - 0.25);
END_IF;

IF rState_x_hat[3] > 310.0 THEN
    (* Refractory hotspot protection: reduce main coal firing rate *)
    rActuator_u_opt[1] := MAX(rActuator_u_min[1], rActuator_u_opt[1] - 0.40);
END_IF;

IF rState_x_hat[5] > 470.0 THEN
    (* Mechanical drive torque high: slight speed bump to distribute bed and clear damming *)
    rActuator_u_opt[3] := MIN(rActuator_u_max[3], rActuator_u_opt[3] + 0.08);
END_IF;
"""
