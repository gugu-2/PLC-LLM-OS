(* ==================================================================================================== *)
(* PHASE 3: RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) WITH 10 UNROLLED ITERATIONS OF PGD           *)
(* ==================================================================================================== *)
(* MATHEMATICAL OPTIMAL CONTROL PROBLEM FORMULATION:                                                    *)
(*   Minimize J(u) = 0.5 * sum_{k=0}^{N-1} [ ||x_k - x_ref||^2_Q + ||u_k||^2_R + ||u_k - u_{k-1}||^2_S ]   *)
(*                 + 0.5 * ||x_N - x_ref||^2_P                                                           *)
(*   Subject to:                                                                                        *)
(*     x_{k+1} = A * x_k + B * u_k                                                                       *)
(*     u_min <= u_k <= u_max                                                                            *)
(*     -delta_u_max <= u_k - u_{k-1} <= delta_u_max                                                      *)
(*                                                                                                      *)
(* PREDICTION HORIZON: N = 5 steps (Dt = 1.0 ms per step; Total predictive window = 5.0 ms).            *)
(* OPTIMIZATION SOLVER: 10 Explicitly Unrolled Iterations of Accelerated Projected Gradient Descent    *)
(*                      (PGD) with Adjoint Costate Vector Back-Propagation, Dynamic Slew Saturation,     *)
(*                      and Actuator Box Constraint Hard Projections.                                   *)
(* ==================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------- *)
(* 3.1 DYNAMIC REFERENCE TRAJECTORY & SUPERPLASTIC STRAIN RATE TRACKING                                  *)
(* ---------------------------------------------------------------------------------------------------- *)
(* Target Ram Height Setpoint: Web Thickness [mm] *)
x_ref[1] := r_FinalForgedWebThickness_mm;

(* Superplastic Isothermal Target Velocity Setpoint: v_ref(t) = -h(t) * (dEps/dt)_target [mm/s]        *)
(* For Ti-6Al-4V at 950 deg C, true strain rate is regulated strictly at 1.0e-3 s^-1 to avoid flow shear *)
IF (x_est[1] > r_FinalForgedWebThickness_mm) AND (n_FSM_State = 8) THEN
    x_ref[2] := -1.0 * x_est[1] * r_SuperplasticStrainRate_s_inv;
    IF x_ref[2] < -5.0 THEN
        x_ref[2] := -5.0; (* Maximum superplastic pressing velocity limit [mm/s] *)
    ELSIF x_ref[2] > -0.010 THEN
        x_ref[2] := -0.010; (* Minimum crawl velocity limit [mm/s] *)
    END_IF;
ELSE
    x_ref[2] := 0.0;
END_IF;

(* Workpiece Flow Stress Target: 65.0 MPa at 950 deg C *)
x_ref[3] := 65.0;
(* Target Microstructure Grain Size: 8.5 um (Refined Equiaxed Alpha Blisk Spec) *)
x_ref[4] := 8.5;
(* Target Isothermal Die Block Temperature: 950.0 deg C *)
x_ref[5] := r_TargetIsothermalDieTemp_DegC;
(* Target Ram Leveling Angular Skew: 0.0 um (Zero Tilt across 4 Columns) *)
x_ref[6] := 0.0;

(* ---------------------------------------------------------------------------------------------------- *)
(* 3.2 INITIALIZE PREDICTION HORIZON BASE STATE & CONTROL WARM START                                    *)
(* ---------------------------------------------------------------------------------------------------- *)
x_traj[0, 1] := x_est[1];
x_traj[0, 2] := x_est[2];
x_traj[0, 3] := x_est[3];
x_traj[0, 4] := x_est[4];
x_traj[0, 5] := x_est[5];
x_traj[0, 6] := x_est[6];

(* Warm Start Control Trajectory with Previous Solution *)
FOR idx_k := 0 TO 4 DO
    u_traj[idx_k, 1] := u_cmd[1];
    u_traj[idx_k, 2] := u_cmd[2];
    u_traj[idx_k, 3] := u_cmd[3];
    u_traj[idx_k, 4] := u_cmd[4];
    u_traj[idx_k, 5] := u_cmd[5];
END_FOR;

(* ---------------------------------------------------------------------------------------------------- *)
(* 3.3 10 EXPLICITLY UNROLLED PROJECTED GRADIENT DESCENT (PGD) ITERATIONS                               *)
(* ---------------------------------------------------------------------------------------------------- *)
(* ============================================================================================== *)
(* PGD UNROLLED ITERATION 1 OF 10                                                               *)
(* ============================================================================================== *)
(* Step 1.A: Forward State Simulation over Horizon k = 0 to 4 *)
FOR idx_k := 0 TO 4 DO
    x_traj[idx_k + 1, 1] := ((A_mat[1, 1] * x_traj[idx_k, 1]) + (A_mat[1, 2] * x_traj[idx_k, 2]) + (A_mat[1, 3] * x_traj[idx_k, 3]) + (A_mat[1, 4] * x_traj[idx_k, 4]) + (A_mat[1, 5] * x_traj[idx_k, 5]) + (A_mat[1, 6] * x_traj[idx_k, 6])) + ((B_mat[1, 1] * u_traj[idx_k, 1]) + (B_mat[1, 2] * u_traj[idx_k, 2]) + (B_mat[1, 3] * u_traj[idx_k, 3]) + (B_mat[1, 4] * u_traj[idx_k, 4]) + (B_mat[1, 5] * u_traj[idx_k, 5]));
    x_traj[idx_k + 1, 2] := ((A_mat[2, 1] * x_traj[idx_k, 1]) + (A_mat[2, 2] * x_traj[idx_k, 2]) + (A_mat[2, 3] * x_traj[idx_k, 3]) + (A_mat[2, 4] * x_traj[idx_k, 4]) + (A_mat[2, 5] * x_traj[idx_k, 5]) + (A_mat[2, 6] * x_traj[idx_k, 6])) + ((B_mat[2, 1] * u_traj[idx_k, 1]) + (B_mat[2, 2] * u_traj[idx_k, 2]) + (B_mat[2, 3] * u_traj[idx_k, 3]) + (B_mat[2, 4] * u_traj[idx_k, 4]) + (B_mat[2, 5] * u_traj[idx_k, 5]));
    x_traj[idx_k + 1, 3] := ((A_mat[3, 1] * x_traj[idx_k, 1]) + (A_mat[3, 2] * x_traj[idx_k, 2]) + (A_mat[3, 3] * x_traj[idx_k, 3]) + (A_mat[3, 4] * x_traj[idx_k, 4]) + (A_mat[3, 5] * x_traj[idx_k, 5]) + (A_mat[3, 6] * x_traj[idx_k, 6])) + ((B_mat[3, 1] * u_traj[idx_k, 1]) + (B_mat[3, 2] * u_traj[idx_k, 2]) + (B_mat[3, 3] * u_traj[idx_k, 3]) + (B_mat[3, 4] * u_traj[idx_k, 4]) + (B_mat[3, 5] * u_traj[idx_k, 5]));
    x_traj[idx_k + 1, 4] := ((A_mat[4, 1] * x_traj[idx_k, 1]) + (A_mat[4, 2] * x_traj[idx_k, 2]) + (A_mat[4, 3] * x_traj[idx_k, 3]) + (A_mat[4, 4] * x_traj[idx_k, 4]) + (A_mat[4, 5] * x_traj[idx_k, 5]) + (A_mat[4, 6] * x_traj[idx_k, 6])) + ((B_mat[4, 1] * u_traj[idx_k, 1]) + (B_mat[4, 2] * u_traj[idx_k, 2]) + (B_mat[4, 3] * u_traj[idx_k, 3]) + (B_mat[4, 4] * u_traj[idx_k, 4]) + (B_mat[4, 5] * u_traj[idx_k, 5]));
    x_traj[idx_k + 1, 5] := ((A_mat[5, 1] * x_traj[idx_k, 1]) + (A_mat[5, 2] * x_traj[idx_k, 2]) + (A_mat[5, 3] * x_traj[idx_k, 3]) + (A_mat[5, 4] * x_traj[idx_k, 4]) + (A_mat[5, 5] * x_traj[idx_k, 5]) + (A_mat[5, 6] * x_traj[idx_k, 6])) + ((B_mat[5, 1] * u_traj[idx_k, 1]) + (B_mat[5, 2] * u_traj[idx_k, 2]) + (B_mat[5, 3] * u_traj[idx_k, 3]) + (B_mat[5, 4] * u_traj[idx_k, 4]) + (B_mat[5, 5] * u_traj[idx_k, 5]));
    x_traj[idx_k + 1, 6] := ((A_mat[6, 1] * x_traj[idx_k, 1]) + (A_mat[6, 2] * x_traj[idx_k, 2]) + (A_mat[6, 3] * x_traj[idx_k, 3]) + (A_mat[6, 4] * x_traj[idx_k, 4]) + (A_mat[6, 5] * x_traj[idx_k, 5]) + (A_mat[6, 6] * x_traj[idx_k, 6])) + ((B_mat[6, 1] * u_traj[idx_k, 1]) + (B_mat[6, 2] * u_traj[idx_k, 2]) + (B_mat[6, 3] * u_traj[idx_k, 3]) + (B_mat[6, 4] * u_traj[idx_k, 4]) + (B_mat[6, 5] * u_traj[idx_k, 5]));
END_FOR;

(* Step 1.B: Terminal Horizon Adjoint Costate Evaluation (k = 5) *)
lambda_costate[5, 1] := P_term[1] * (x_traj[5, 1] - x_ref[1]);
lambda_costate[5, 2] := P_term[2] * (x_traj[5, 2] - x_ref[2]);
lambda_costate[5, 3] := P_term[3] * (x_traj[5, 3] - x_ref[3]);
lambda_costate[5, 4] := P_term[4] * (x_traj[5, 4] - x_ref[4]);
lambda_costate[5, 5] := P_term[5] * (x_traj[5, 5] - x_ref[5]);
lambda_costate[5, 6] := P_term[6] * (x_traj[5, 6] - x_ref[6]);

(* Step 1.C: Backward Adjoint Costate Propagation over Horizon k = 4 downto 0 *)
FOR idx_k := 4 TO 0 BY -1 DO
    lambda_costate[idx_k, 1] := ((A_mat[1, 1] * lambda_costate[idx_k + 1, 1]) + (A_mat[2, 1] * lambda_costate[idx_k + 1, 2]) + (A_mat[3, 1] * lambda_costate[idx_k + 1, 3]) + (A_mat[4, 1] * lambda_costate[idx_k + 1, 4]) + (A_mat[5, 1] * lambda_costate[idx_k + 1, 5]) + (A_mat[6, 1] * lambda_costate[idx_k + 1, 6])) + (Q_diag[1] * (x_traj[idx_k, 1] - x_ref[1]));
    lambda_costate[idx_k, 2] := ((A_mat[1, 2] * lambda_costate[idx_k + 1, 1]) + (A_mat[2, 2] * lambda_costate[idx_k + 1, 2]) + (A_mat[3, 2] * lambda_costate[idx_k + 1, 3]) + (A_mat[4, 2] * lambda_costate[idx_k + 1, 4]) + (A_mat[5, 2] * lambda_costate[idx_k + 1, 5]) + (A_mat[6, 2] * lambda_costate[idx_k + 1, 6])) + (Q_diag[2] * (x_traj[idx_k, 2] - x_ref[2]));
    lambda_costate[idx_k, 3] := ((A_mat[1, 3] * lambda_costate[idx_k + 1, 1]) + (A_mat[2, 3] * lambda_costate[idx_k + 1, 2]) + (A_mat[3, 3] * lambda_costate[idx_k + 1, 3]) + (A_mat[4, 3] * lambda_costate[idx_k + 1, 4]) + (A_mat[5, 3] * lambda_costate[idx_k + 1, 5]) + (A_mat[6, 3] * lambda_costate[idx_k + 1, 6])) + (Q_diag[3] * (x_traj[idx_k, 3] - x_ref[3]));
    lambda_costate[idx_k, 4] := ((A_mat[1, 4] * lambda_costate[idx_k + 1, 1]) + (A_mat[2, 4] * lambda_costate[idx_k + 1, 2]) + (A_mat[3, 4] * lambda_costate[idx_k + 1, 3]) + (A_mat[4, 4] * lambda_costate[idx_k + 1, 4]) + (A_mat[5, 4] * lambda_costate[idx_k + 1, 5]) + (A_mat[6, 4] * lambda_costate[idx_k + 1, 6])) + (Q_diag[4] * (x_traj[idx_k, 4] - x_ref[4]));
    lambda_costate[idx_k, 5] := ((A_mat[1, 5] * lambda_costate[idx_k + 1, 1]) + (A_mat[2, 5] * lambda_costate[idx_k + 1, 2]) + (A_mat[3, 5] * lambda_costate[idx_k + 1, 3]) + (A_mat[4, 5] * lambda_costate[idx_k + 1, 4]) + (A_mat[5, 5] * lambda_costate[idx_k + 1, 5]) + (A_mat[6, 5] * lambda_costate[idx_k + 1, 6])) + (Q_diag[5] * (x_traj[idx_k, 5] - x_ref[5]));
    lambda_costate[idx_k, 6] := ((A_mat[1, 6] * lambda_costate[idx_k + 1, 1]) + (A_mat[2, 6] * lambda_costate[idx_k + 1, 2]) + (A_mat[3, 6] * lambda_costate[idx_k + 1, 3]) + (A_mat[4, 6] * lambda_costate[idx_k + 1, 4]) + (A_mat[5, 6] * lambda_costate[idx_k + 1, 5]) + (A_mat[6, 6] * lambda_costate[idx_k + 1, 6])) + (Q_diag[6] * (x_traj[idx_k, 6] - x_ref[6]));
END_FOR;

(* Step 1.D: Control Gradient Computation & Projected Descent Step over Horizon k = 0 to 4 *)
FOR idx_k := 0 TO 4 DO
    (* Gradient Evaluation Control 1 *)
    IF idx_k = 0 THEN
        grad_u[0, 1] := ((B_mat[1, 1] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 1] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 1] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 1] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 1] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 1] * lambda_costate[idx_k + 1, 6])) + (R_diag[1] * u_traj[0, 1]) + (S_diag[1] * (u_traj[0, 1] - u_prev[1]));
    ELSE
        grad_u[idx_k, 1] := ((B_mat[1, 1] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 1] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 1] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 1] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 1] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 1] * lambda_costate[idx_k + 1, 6])) + (R_diag[1] * u_traj[idx_k, 1]) + (S_diag[1] * (u_traj[idx_k, 1] - u_traj[idx_k - 1, 1]));
    END_IF;
    
    (* Descent Step *)
    u_traj[idx_k, 1] := u_traj[idx_k, 1] - (r_PGD_StepSize_Alpha * grad_u[idx_k, 1]);
    
    (* Box Constraint Projection *)
    IF u_traj[idx_k, 1] < u_min[1] THEN
        u_traj[idx_k, 1] := u_min[1];
    ELSIF u_traj[idx_k, 1] > u_max[1] THEN
        u_traj[idx_k, 1] := u_max[1];
    END_IF;
    
    (* Dynamic Slew Rate Projection *)
    IF idx_k = 0 THEN
        r_TmpDeltaU := u_traj[0, 1] - u_prev[1];
        IF r_TmpDeltaU > delta_u_max[1] THEN
            u_traj[0, 1] := u_prev[1] + delta_u_max[1];
        ELSIF r_TmpDeltaU < -delta_u_max[1] THEN
            u_traj[0, 1] := u_prev[1] - delta_u_max[1];
        END_IF;
    ELSE
        r_TmpDeltaU := u_traj[idx_k, 1] - u_traj[idx_k - 1, 1];
        IF r_TmpDeltaU > delta_u_max[1] THEN
            u_traj[idx_k, 1] := u_traj[idx_k - 1, 1] + delta_u_max[1];
        ELSIF r_TmpDeltaU < -delta_u_max[1] THEN
            u_traj[idx_k, 1] := u_traj[idx_k - 1, 1] - delta_u_max[1];
        END_IF;
    END_IF;
    (* Gradient Evaluation Control 2 *)
    IF idx_k = 0 THEN
        grad_u[0, 2] := ((B_mat[1, 2] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 2] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 2] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 2] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 2] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 2] * lambda_costate[idx_k + 1, 6])) + (R_diag[2] * u_traj[0, 2]) + (S_diag[2] * (u_traj[0, 2] - u_prev[2]));
    ELSE
        grad_u[idx_k, 2] := ((B_mat[1, 2] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 2] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 2] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 2] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 2] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 2] * lambda_costate[idx_k + 1, 6])) + (R_diag[2] * u_traj[idx_k, 2]) + (S_diag[2] * (u_traj[idx_k, 2] - u_traj[idx_k - 1, 2]));
    END_IF;
    
    (* Descent Step *)
    u_traj[idx_k, 2] := u_traj[idx_k, 2] - (r_PGD_StepSize_Alpha * grad_u[idx_k, 2]);
    
    (* Box Constraint Projection *)
    IF u_traj[idx_k, 2] < u_min[2] THEN
        u_traj[idx_k, 2] := u_min[2];
    ELSIF u_traj[idx_k, 2] > u_max[2] THEN
        u_traj[idx_k, 2] := u_max[2];
    END_IF;
    
    (* Dynamic Slew Rate Projection *)
    IF idx_k = 0 THEN
        r_TmpDeltaU := u_traj[0, 2] - u_prev[2];
        IF r_TmpDeltaU > delta_u_max[2] THEN
            u_traj[0, 2] := u_prev[2] + delta_u_max[2];
        ELSIF r_TmpDeltaU < -delta_u_max[2] THEN
            u_traj[0, 2] := u_prev[2] - delta_u_max[2];
        END_IF;
    ELSE
        r_TmpDeltaU := u_traj[idx_k, 2] - u_traj[idx_k - 1, 2];
        IF r_TmpDeltaU > delta_u_max[2] THEN
            u_traj[idx_k, 2] := u_traj[idx_k - 1, 2] + delta_u_max[2];
        ELSIF r_TmpDeltaU < -delta_u_max[2] THEN
            u_traj[idx_k, 2] := u_traj[idx_k - 1, 2] - delta_u_max[2];
        END_IF;
    END_IF;
    (* Gradient Evaluation Control 3 *)
    IF idx_k = 0 THEN
        grad_u[0, 3] := ((B_mat[1, 3] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 3] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 3] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 3] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 3] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 3] * lambda_costate[idx_k + 1, 6])) + (R_diag[3] * u_traj[0, 3]) + (S_diag[3] * (u_traj[0, 3] - u_prev[3]));
    ELSE
        grad_u[idx_k, 3] := ((B_mat[1, 3] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 3] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 3] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 3] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 3] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 3] * lambda_costate[idx_k + 1, 6])) + (R_diag[3] * u_traj[idx_k, 3]) + (S_diag[3] * (u_traj[idx_k, 3] - u_traj[idx_k - 1, 3]));
    END_IF;
    
    (* Descent Step *)
    u_traj[idx_k, 3] := u_traj[idx_k, 3] - (r_PGD_StepSize_Alpha * grad_u[idx_k, 3]);
    
    (* Box Constraint Projection *)
    IF u_traj[idx_k, 3] < u_min[3] THEN
        u_traj[idx_k, 3] := u_min[3];
    ELSIF u_traj[idx_k, 3] > u_max[3] THEN
        u_traj[idx_k, 3] := u_max[3];
    END_IF;
    
    (* Dynamic Slew Rate Projection *)
    IF idx_k = 0 THEN
        r_TmpDeltaU := u_traj[0, 3] - u_prev[3];
        IF r_TmpDeltaU > delta_u_max[3] THEN
            u_traj[0, 3] := u_prev[3] + delta_u_max[3];
        ELSIF r_TmpDeltaU < -delta_u_max[3] THEN
            u_traj[0, 3] := u_prev[3] - delta_u_max[3];
        END_IF;
    ELSE
        r_TmpDeltaU := u_traj[idx_k, 3] - u_traj[idx_k - 1, 3];
        IF r_TmpDeltaU > delta_u_max[3] THEN
            u_traj[idx_k, 3] := u_traj[idx_k - 1, 3] + delta_u_max[3];
        ELSIF r_TmpDeltaU < -delta_u_max[3] THEN
            u_traj[idx_k, 3] := u_traj[idx_k - 1, 3] - delta_u_max[3];
        END_IF;
    END_IF;
    (* Gradient Evaluation Control 4 *)
    IF idx_k = 0 THEN
        grad_u[0, 4] := ((B_mat[1, 4] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 4] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 4] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 4] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 4] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 4] * lambda_costate[idx_k + 1, 6])) + (R_diag[4] * u_traj[0, 4]) + (S_diag[4] * (u_traj[0, 4] - u_prev[4]));
    ELSE
        grad_u[idx_k, 4] := ((B_mat[1, 4] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 4] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 4] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 4] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 4] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 4] * lambda_costate[idx_k + 1, 6])) + (R_diag[4] * u_traj[idx_k, 4]) + (S_diag[4] * (u_traj[idx_k, 4] - u_traj[idx_k - 1, 4]));
    END_IF;
    
    (* Descent Step *)
    u_traj[idx_k, 4] := u_traj[idx_k, 4] - (r_PGD_StepSize_Alpha * grad_u[idx_k, 4]);
    
    (* Box Constraint Projection *)
    IF u_traj[idx_k, 4] < u_min[4] THEN
        u_traj[idx_k, 4] := u_min[4];
    ELSIF u_traj[idx_k, 4] > u_max[4] THEN
        u_traj[idx_k, 4] := u_max[4];
    END_IF;
    
    (* Dynamic Slew Rate Projection *)
    IF idx_k = 0 THEN
        r_TmpDeltaU := u_traj[0, 4] - u_prev[4];
        IF r_TmpDeltaU > delta_u_max[4] THEN
            u_traj[0, 4] := u_prev[4] + delta_u_max[4];
        ELSIF r_TmpDeltaU < -delta_u_max[4] THEN
            u_traj[0, 4] := u_prev[4] - delta_u_max[4];
        END_IF;
    ELSE
        r_TmpDeltaU := u_traj[idx_k, 4] - u_traj[idx_k - 1, 4];
        IF r_TmpDeltaU > delta_u_max[4] THEN
            u_traj[idx_k, 4] := u_traj[idx_k - 1, 4] + delta_u_max[4];
        ELSIF r_TmpDeltaU < -delta_u_max[4] THEN
            u_traj[idx_k, 4] := u_traj[idx_k - 1, 4] - delta_u_max[4];
        END_IF;
    END_IF;
    (* Gradient Evaluation Control 5 *)
    IF idx_k = 0 THEN
        grad_u[0, 5] := ((B_mat[1, 5] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 5] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 5] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 5] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 5] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 5] * lambda_costate[idx_k + 1, 6])) + (R_diag[5] * u_traj[0, 5]) + (S_diag[5] * (u_traj[0, 5] - u_prev[5]));
    ELSE
        grad_u[idx_k, 5] := ((B_mat[1, 5] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 5] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 5] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 5] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 5] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 5] * lambda_costate[idx_k + 1, 6])) + (R_diag[5] * u_traj[idx_k, 5]) + (S_diag[5] * (u_traj[idx_k, 5] - u_traj[idx_k - 1, 5]));
    END_IF;
    
    (* Descent Step *)
    u_traj[idx_k, 5] := u_traj[idx_k, 5] - (r_PGD_StepSize_Alpha * grad_u[idx_k, 5]);
    
    (* Box Constraint Projection *)
    IF u_traj[idx_k, 5] < u_min[5] THEN
        u_traj[idx_k, 5] := u_min[5];
    ELSIF u_traj[idx_k, 5] > u_max[5] THEN
        u_traj[idx_k, 5] := u_max[5];
    END_IF;
    
    (* Dynamic Slew Rate Projection *)
    IF idx_k = 0 THEN
        r_TmpDeltaU := u_traj[0, 5] - u_prev[5];
        IF r_TmpDeltaU > delta_u_max[5] THEN
            u_traj[0, 5] := u_prev[5] + delta_u_max[5];
        ELSIF r_TmpDeltaU < -delta_u_max[5] THEN
            u_traj[0, 5] := u_prev[5] - delta_u_max[5];
        END_IF;
    ELSE
        r_TmpDeltaU := u_traj[idx_k, 5] - u_traj[idx_k - 1, 5];
        IF r_TmpDeltaU > delta_u_max[5] THEN
            u_traj[idx_k, 5] := u_traj[idx_k - 1, 5] + delta_u_max[5];
        ELSIF r_TmpDeltaU < -delta_u_max[5] THEN
            u_traj[idx_k, 5] := u_traj[idx_k - 1, 5] - delta_u_max[5];
        END_IF;
    END_IF;
END_FOR;

(* ============================================================================================== *)
(* PGD UNROLLED ITERATION 2 OF 10                                                               *)
(* ============================================================================================== *)
(* Step 2.A: Forward State Simulation over Horizon k = 0 to 4 *)
FOR idx_k := 0 TO 4 DO
    x_traj[idx_k + 1, 1] := ((A_mat[1, 1] * x_traj[idx_k, 1]) + (A_mat[1, 2] * x_traj[idx_k, 2]) + (A_mat[1, 3] * x_traj[idx_k, 3]) + (A_mat[1, 4] * x_traj[idx_k, 4]) + (A_mat[1, 5] * x_traj[idx_k, 5]) + (A_mat[1, 6] * x_traj[idx_k, 6])) + ((B_mat[1, 1] * u_traj[idx_k, 1]) + (B_mat[1, 2] * u_traj[idx_k, 2]) + (B_mat[1, 3] * u_traj[idx_k, 3]) + (B_mat[1, 4] * u_traj[idx_k, 4]) + (B_mat[1, 5] * u_traj[idx_k, 5]));
    x_traj[idx_k + 1, 2] := ((A_mat[2, 1] * x_traj[idx_k, 1]) + (A_mat[2, 2] * x_traj[idx_k, 2]) + (A_mat[2, 3] * x_traj[idx_k, 3]) + (A_mat[2, 4] * x_traj[idx_k, 4]) + (A_mat[2, 5] * x_traj[idx_k, 5]) + (A_mat[2, 6] * x_traj[idx_k, 6])) + ((B_mat[2, 1] * u_traj[idx_k, 1]) + (B_mat[2, 2] * u_traj[idx_k, 2]) + (B_mat[2, 3] * u_traj[idx_k, 3]) + (B_mat[2, 4] * u_traj[idx_k, 4]) + (B_mat[2, 5] * u_traj[idx_k, 5]));
    x_traj[idx_k + 1, 3] := ((A_mat[3, 1] * x_traj[idx_k, 1]) + (A_mat[3, 2] * x_traj[idx_k, 2]) + (A_mat[3, 3] * x_traj[idx_k, 3]) + (A_mat[3, 4] * x_traj[idx_k, 4]) + (A_mat[3, 5] * x_traj[idx_k, 5]) + (A_mat[3, 6] * x_traj[idx_k, 6])) + ((B_mat[3, 1] * u_traj[idx_k, 1]) + (B_mat[3, 2] * u_traj[idx_k, 2]) + (B_mat[3, 3] * u_traj[idx_k, 3]) + (B_mat[3, 4] * u_traj[idx_k, 4]) + (B_mat[3, 5] * u_traj[idx_k, 5]));
    x_traj[idx_k + 1, 4] := ((A_mat[4, 1] * x_traj[idx_k, 1]) + (A_mat[4, 2] * x_traj[idx_k, 2]) + (A_mat[4, 3] * x_traj[idx_k, 3]) + (A_mat[4, 4] * x_traj[idx_k, 4]) + (A_mat[4, 5] * x_traj[idx_k, 5]) + (A_mat[4, 6] * x_traj[idx_k, 6])) + ((B_mat[4, 1] * u_traj[idx_k, 1]) + (B_mat[4, 2] * u_traj[idx_k, 2]) + (B_mat[4, 3] * u_traj[idx_k, 3]) + (B_mat[4, 4] * u_traj[idx_k, 4]) + (B_mat[4, 5] * u_traj[idx_k, 5]));
    x_traj[idx_k + 1, 5] := ((A_mat[5, 1] * x_traj[idx_k, 1]) + (A_mat[5, 2] * x_traj[idx_k, 2]) + (A_mat[5, 3] * x_traj[idx_k, 3]) + (A_mat[5, 4] * x_traj[idx_k, 4]) + (A_mat[5, 5] * x_traj[idx_k, 5]) + (A_mat[5, 6] * x_traj[idx_k, 6])) + ((B_mat[5, 1] * u_traj[idx_k, 1]) + (B_mat[5, 2] * u_traj[idx_k, 2]) + (B_mat[5, 3] * u_traj[idx_k, 3]) + (B_mat[5, 4] * u_traj[idx_k, 4]) + (B_mat[5, 5] * u_traj[idx_k, 5]));
    x_traj[idx_k + 1, 6] := ((A_mat[6, 1] * x_traj[idx_k, 1]) + (A_mat[6, 2] * x_traj[idx_k, 2]) + (A_mat[6, 3] * x_traj[idx_k, 3]) + (A_mat[6, 4] * x_traj[idx_k, 4]) + (A_mat[6, 5] * x_traj[idx_k, 5]) + (A_mat[6, 6] * x_traj[idx_k, 6])) + ((B_mat[6, 1] * u_traj[idx_k, 1]) + (B_mat[6, 2] * u_traj[idx_k, 2]) + (B_mat[6, 3] * u_traj[idx_k, 3]) + (B_mat[6, 4] * u_traj[idx_k, 4]) + (B_mat[6, 5] * u_traj[idx_k, 5]));
END_FOR;

(* Step 2.B: Terminal Horizon Adjoint Costate Evaluation (k = 5) *)
lambda_costate[5, 1] := P_term[1] * (x_traj[5, 1] - x_ref[1]);
lambda_costate[5, 2] := P_term[2] * (x_traj[5, 2] - x_ref[2]);
lambda_costate[5, 3] := P_term[3] * (x_traj[5, 3] - x_ref[3]);
lambda_costate[5, 4] := P_term[4] * (x_traj[5, 4] - x_ref[4]);
lambda_costate[5, 5] := P_term[5] * (x_traj[5, 5] - x_ref[5]);
lambda_costate[5, 6] := P_term[6] * (x_traj[5, 6] - x_ref[6]);

(* Step 2.C: Backward Adjoint Costate Propagation over Horizon k = 4 downto 0 *)
FOR idx_k := 4 TO 0 BY -1 DO
    lambda_costate[idx_k, 1] := ((A_mat[1, 1] * lambda_costate[idx_k + 1, 1]) + (A_mat[2, 1] * lambda_costate[idx_k + 1, 2]) + (A_mat[3, 1] * lambda_costate[idx_k + 1, 3]) + (A_mat[4, 1] * lambda_costate[idx_k + 1, 4]) + (A_mat[5, 1] * lambda_costate[idx_k + 1, 5]) + (A_mat[6, 1] * lambda_costate[idx_k + 1, 6])) + (Q_diag[1] * (x_traj[idx_k, 1] - x_ref[1]));
    lambda_costate[idx_k, 2] := ((A_mat[1, 2] * lambda_costate[idx_k + 1, 1]) + (A_mat[2, 2] * lambda_costate[idx_k + 1, 2]) + (A_mat[3, 2] * lambda_costate[idx_k + 1, 3]) + (A_mat[4, 2] * lambda_costate[idx_k + 1, 4]) + (A_mat[5, 2] * lambda_costate[idx_k + 1, 5]) + (A_mat[6, 2] * lambda_costate[idx_k + 1, 6])) + (Q_diag[2] * (x_traj[idx_k, 2] - x_ref[2]));
    lambda_costate[idx_k, 3] := ((A_mat[1, 3] * lambda_costate[idx_k + 1, 1]) + (A_mat[2, 3] * lambda_costate[idx_k + 1, 2]) + (A_mat[3, 3] * lambda_costate[idx_k + 1, 3]) + (A_mat[4, 3] * lambda_costate[idx_k + 1, 4]) + (A_mat[5, 3] * lambda_costate[idx_k + 1, 5]) + (A_mat[6, 3] * lambda_costate[idx_k + 1, 6])) + (Q_diag[3] * (x_traj[idx_k, 3] - x_ref[3]));
    lambda_costate[idx_k, 4] := ((A_mat[1, 4] * lambda_costate[idx_k + 1, 1]) + (A_mat[2, 4] * lambda_costate[idx_k + 1, 2]) + (A_mat[3, 4] * lambda_costate[idx_k + 1, 3]) + (A_mat[4, 4] * lambda_costate[idx_k + 1, 4]) + (A_mat[5, 4] * lambda_costate[idx_k + 1, 5]) + (A_mat[6, 4] * lambda_costate[idx_k + 1, 6])) + (Q_diag[4] * (x_traj[idx_k, 4] - x_ref[4]));
    lambda_costate[idx_k, 5] := ((A_mat[1, 5] * lambda_costate[idx_k + 1, 1]) + (A_mat[2, 5] * lambda_costate[idx_k + 1, 2]) + (A_mat[3, 5] * lambda_costate[idx_k + 1, 3]) + (A_mat[4, 5] * lambda_costate[idx_k + 1, 4]) + (A_mat[5, 5] * lambda_costate[idx_k + 1, 5]) + (A_mat[6, 5] * lambda_costate[idx_k + 1, 6])) + (Q_diag[5] * (x_traj[idx_k, 5] - x_ref[5]));
    lambda_costate[idx_k, 6] := ((A_mat[1, 6] * lambda_costate[idx_k + 1, 1]) + (A_mat[2, 6] * lambda_costate[idx_k + 1, 2]) + (A_mat[3, 6] * lambda_costate[idx_k + 1, 3]) + (A_mat[4, 6] * lambda_costate[idx_k + 1, 4]) + (A_mat[5, 6] * lambda_costate[idx_k + 1, 5]) + (A_mat[6, 6] * lambda_costate[idx_k + 1, 6])) + (Q_diag[6] * (x_traj[idx_k, 6] - x_ref[6]));
END_FOR;

(* Step 2.D: Control Gradient Computation & Projected Descent Step over Horizon k = 0 to 4 *)
FOR idx_k := 0 TO 4 DO
    (* Gradient Evaluation Control 1 *)
    IF idx_k = 0 THEN
        grad_u[0, 1] := ((B_mat[1, 1] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 1] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 1] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 1] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 1] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 1] * lambda_costate[idx_k + 1, 6])) + (R_diag[1] * u_traj[0, 1]) + (S_diag[1] * (u_traj[0, 1] - u_prev[1]));
    ELSE
        grad_u[idx_k, 1] := ((B_mat[1, 1] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 1] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 1] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 1] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 1] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 1] * lambda_costate[idx_k + 1, 6])) + (R_diag[1] * u_traj[idx_k, 1]) + (S_diag[1] * (u_traj[idx_k, 1] - u_traj[idx_k - 1, 1]));
    END_IF;
    
    (* Descent Step *)
    u_traj[idx_k, 1] := u_traj[idx_k, 1] - (r_PGD_StepSize_Alpha * grad_u[idx_k, 1]);
    
    (* Box Constraint Projection *)
    IF u_traj[idx_k, 1] < u_min[1] THEN
        u_traj[idx_k, 1] := u_min[1];
    ELSIF u_traj[idx_k, 1] > u_max[1] THEN
        u_traj[idx_k, 1] := u_max[1];
    END_IF;
    
    (* Dynamic Slew Rate Projection *)
    IF idx_k = 0 THEN
        r_TmpDeltaU := u_traj[0, 1] - u_prev[1];
        IF r_TmpDeltaU > delta_u_max[1] THEN
            u_traj[0, 1] := u_prev[1] + delta_u_max[1];
        ELSIF r_TmpDeltaU < -delta_u_max[1] THEN
            u_traj[0, 1] := u_prev[1] - delta_u_max[1];
        END_IF;
    ELSE
        r_TmpDeltaU := u_traj[idx_k, 1] - u_traj[idx_k - 1, 1];
        IF r_TmpDeltaU > delta_u_max[1] THEN
            u_traj[idx_k, 1] := u_traj[idx_k - 1, 1] + delta_u_max[1];
        ELSIF r_TmpDeltaU < -delta_u_max[1] THEN
            u_traj[idx_k, 1] := u_traj[idx_k - 1, 1] - delta_u_max[1];
        END_IF;
    END_IF;
    (* Gradient Evaluation Control 2 *)
    IF idx_k = 0 THEN
        grad_u[0, 2] := ((B_mat[1, 2] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 2] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 2] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 2] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 2] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 2] * lambda_costate[idx_k + 1, 6])) + (R_diag[2] * u_traj[0, 2]) + (S_diag[2] * (u_traj[0, 2] - u_prev[2]));
    ELSE
        grad_u[idx_k, 2] := ((B_mat[1, 2] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 2] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 2] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 2] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 2] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 2] * lambda_costate[idx_k + 1, 6])) + (R_diag[2] * u_traj[idx_k, 2]) + (S_diag[2] * (u_traj[idx_k, 2] - u_traj[idx_k - 1, 2]));
    END_IF;
    
    (* Descent Step *)
    u_traj[idx_k, 2] := u_traj[idx_k, 2] - (r_PGD_StepSize_Alpha * grad_u[idx_k, 2]);
    
    (* Box Constraint Projection *)
    IF u_traj[idx_k, 2] < u_min[2] THEN
        u_traj[idx_k, 2] := u_min[2];
    ELSIF u_traj[idx_k, 2] > u_max[2] THEN
        u_traj[idx_k, 2] := u_max[2];
    END_IF;
    
    (* Dynamic Slew Rate Projection *)
    IF idx_k = 0 THEN
        r_TmpDeltaU := u_traj[0, 2] - u_prev[2];
        IF r_TmpDeltaU > delta_u_max[2] THEN
            u_traj[0, 2] := u_prev[2] + delta_u_max[2];
        ELSIF r_TmpDeltaU < -delta_u_max[2] THEN
            u_traj[0, 2] := u_prev[2] - delta_u_max[2];
        END_IF;
    ELSE
        r_TmpDeltaU := u_traj[idx_k, 2] - u_traj[idx_k - 1, 2];
        IF r_TmpDeltaU > delta_u_max[2] THEN
            u_traj[idx_k, 2] := u_traj[idx_k - 1, 2] + delta_u_max[2];
        ELSIF r_TmpDeltaU < -delta_u_max[2] THEN
            u_traj[idx_k, 2] := u_traj[idx_k - 1, 2] - delta_u_max[2];
        END_IF;
    END_IF;
    (* Gradient Evaluation Control 3 *)
    IF idx_k = 0 THEN
        grad_u[0, 3] := ((B_mat[1, 3] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 3] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 3] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 3] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 3] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 3] * lambda_costate[idx_k + 1, 6])) + (R_diag[3] * u_traj[0, 3]) + (S_diag[3] * (u_traj[0, 3] - u_prev[3]));
    ELSE
        grad_u[idx_k, 3] := ((B_mat[1, 3] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 3] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 3] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 3] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 3] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 3] * lambda_costate[idx_k + 1, 6])) + (R_diag[3] * u_traj[idx_k, 3]) + (S_diag[3] * (u_traj[idx_k, 3] - u_traj[idx_k - 1, 3]));
    END_IF;
    
    (* Descent Step *)
    u_traj[idx_k, 3] := u_traj[idx_k, 3] - (r_PGD_StepSize_Alpha * grad_u[idx_k, 3]);
    
    (* Box Constraint Projection *)
    IF u_traj[idx_k, 3] < u_min[3] THEN
        u_traj[idx_k, 3] := u_min[3];
    ELSIF u_traj[idx_k, 3] > u_max[3] THEN
        u_traj[idx_k, 3] := u_max[3];
    END_IF;
    
    (* Dynamic Slew Rate Projection *)
    IF idx_k = 0 THEN
        r_TmpDeltaU := u_traj[0, 3] - u_prev[3];
        IF r_TmpDeltaU > delta_u_max[3] THEN
            u_traj[0, 3] := u_prev[3] + delta_u_max[3];
        ELSIF r_TmpDeltaU < -delta_u_max[3] THEN
            u_traj[0, 3] := u_prev[3] - delta_u_max[3];
        END_IF;
    ELSE
        r_TmpDeltaU := u_traj[idx_k, 3] - u_traj[idx_k - 1, 3];
        IF r_TmpDeltaU > delta_u_max[3] THEN
            u_traj[idx_k, 3] := u_traj[idx_k - 1, 3] + delta_u_max[3];
        ELSIF r_TmpDeltaU < -delta_u_max[3] THEN
            u_traj[idx_k, 3] := u_traj[idx_k - 1, 3] - delta_u_max[3];
        END_IF;
    END_IF;
    (* Gradient Evaluation Control 4 *)
    IF idx_k = 0 THEN
        grad_u[0, 4] := ((B_mat[1, 4] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 4] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 4] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 4] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 4] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 4] * lambda_costate[idx_k + 1, 6])) + (R_diag[4] * u_traj[0, 4]) + (S_diag[4] * (u_traj[0, 4] - u_prev[4]));
    ELSE
        grad_u[idx_k, 4] := ((B_mat[1, 4] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 4] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 4] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 4] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 4] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 4] * lambda_costate[idx_k + 1, 6])) + (R_diag[4] * u_traj[idx_k, 4]) + (S_diag[4] * (u_traj[idx_k, 4] - u_traj[idx_k - 1, 4]));
    END_IF;
    
    (* Descent Step *)
    u_traj[idx_k, 4] := u_traj[idx_k, 4] - (r_PGD_StepSize_Alpha * grad_u[idx_k, 4]);
    
    (* Box Constraint Projection *)
    IF u_traj[idx_k, 4] < u_min[4] THEN
        u_traj[idx_k, 4] := u_min[4];
    ELSIF u_traj[idx_k, 4] > u_max[4] THEN
        u_traj[idx_k, 4] := u_max[4];
    END_IF;
    
    (* Dynamic Slew Rate Projection *)
    IF idx_k = 0 THEN
        r_TmpDeltaU := u_traj[0, 4] - u_prev[4];
        IF r_TmpDeltaU > delta_u_max[4] THEN
            u_traj[0, 4] := u_prev[4] + delta_u_max[4];
        ELSIF r_TmpDeltaU < -delta_u_max[4] THEN
            u_traj[0, 4] := u_prev[4] - delta_u_max[4];
        END_IF;
    ELSE
        r_TmpDeltaU := u_traj[idx_k, 4] - u_traj[idx_k - 1, 4];
        IF r_TmpDeltaU > delta_u_max[4] THEN
            u_traj[idx_k, 4] := u_traj[idx_k - 1, 4] + delta_u_max[4];
        ELSIF r_TmpDeltaU < -delta_u_max[4] THEN
            u_traj[idx_k, 4] := u_traj[idx_k - 1, 4] - delta_u_max[4];
        END_IF;
    END_IF;
    (* Gradient Evaluation Control 5 *)
    IF idx_k = 0 THEN
        grad_u[0, 5] := ((B_mat[1, 5] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 5] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 5] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 5] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 5] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 5] * lambda_costate[idx_k + 1, 6])) + (R_diag[5] * u_traj[0, 5]) + (S_diag[5] * (u_traj[0, 5] - u_prev[5]));
    ELSE
        grad_u[idx_k, 5] := ((B_mat[1, 5] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 5] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 5] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 5] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 5] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 5] * lambda_costate[idx_k + 1, 6])) + (R_diag[5] * u_traj[idx_k, 5]) + (S_diag[5] * (u_traj[idx_k, 5] - u_traj[idx_k - 1, 5]));
    END_IF;
    
    (* Descent Step *)
    u_traj[idx_k, 5] := u_traj[idx_k, 5] - (r_PGD_StepSize_Alpha * grad_u[idx_k, 5]);
    
    (* Box Constraint Projection *)
    IF u_traj[idx_k, 5] < u_min[5] THEN
        u_traj[idx_k, 5] := u_min[5];
    ELSIF u_traj[idx_k, 5] > u_max[5] THEN
        u_traj[idx_k, 5] := u_max[5];
    END_IF;
    
    (* Dynamic Slew Rate Projection *)
    IF idx_k = 0 THEN
        r_TmpDeltaU := u_traj[0, 5] - u_prev[5];
        IF r_TmpDeltaU > delta_u_max[5] THEN
            u_traj[0, 5] := u_prev[5] + delta_u_max[5];
        ELSIF r_TmpDeltaU < -delta_u_max[5] THEN
            u_traj[0, 5] := u_prev[5] - delta_u_max[5];
        END_IF;
    ELSE
        r_TmpDeltaU := u_traj[idx_k, 5] - u_traj[idx_k - 1, 5];
        IF r_TmpDeltaU > delta_u_max[5] THEN
            u_traj[idx_k, 5] := u_traj[idx_k - 1, 5] + delta_u_max[5];
        ELSIF r_TmpDeltaU < -delta_u_max[5] THEN
            u_traj[idx_k, 5] := u_traj[idx_k - 1, 5] - delta_u_max[5];
        END_IF;
    END_IF;
END_FOR;

(* ============================================================================================== *)
(* PGD UNROLLED ITERATION 3 OF 10                                                               *)
(* ============================================================================================== *)
(* Step 3.A: Forward State Simulation over Horizon k = 0 to 4 *)
FOR idx_k := 0 TO 4 DO
    x_traj[idx_k + 1, 1] := ((A_mat[1, 1] * x_traj[idx_k, 1]) + (A_mat[1, 2] * x_traj[idx_k, 2]) + (A_mat[1, 3] * x_traj[idx_k, 3]) + (A_mat[1, 4] * x_traj[idx_k, 4]) + (A_mat[1, 5] * x_traj[idx_k, 5]) + (A_mat[1, 6] * x_traj[idx_k, 6])) + ((B_mat[1, 1] * u_traj[idx_k, 1]) + (B_mat[1, 2] * u_traj[idx_k, 2]) + (B_mat[1, 3] * u_traj[idx_k, 3]) + (B_mat[1, 4] * u_traj[idx_k, 4]) + (B_mat[1, 5] * u_traj[idx_k, 5]));
    x_traj[idx_k + 1, 2] := ((A_mat[2, 1] * x_traj[idx_k, 1]) + (A_mat[2, 2] * x_traj[idx_k, 2]) + (A_mat[2, 3] * x_traj[idx_k, 3]) + (A_mat[2, 4] * x_traj[idx_k, 4]) + (A_mat[2, 5] * x_traj[idx_k, 5]) + (A_mat[2, 6] * x_traj[idx_k, 6])) + ((B_mat[2, 1] * u_traj[idx_k, 1]) + (B_mat[2, 2] * u_traj[idx_k, 2]) + (B_mat[2, 3] * u_traj[idx_k, 3]) + (B_mat[2, 4] * u_traj[idx_k, 4]) + (B_mat[2, 5] * u_traj[idx_k, 5]));
    x_traj[idx_k + 1, 3] := ((A_mat[3, 1] * x_traj[idx_k, 1]) + (A_mat[3, 2] * x_traj[idx_k, 2]) + (A_mat[3, 3] * x_traj[idx_k, 3]) + (A_mat[3, 4] * x_traj[idx_k, 4]) + (A_mat[3, 5] * x_traj[idx_k, 5]) + (A_mat[3, 6] * x_traj[idx_k, 6])) + ((B_mat[3, 1] * u_traj[idx_k, 1]) + (B_mat[3, 2] * u_traj[idx_k, 2]) + (B_mat[3, 3] * u_traj[idx_k, 3]) + (B_mat[3, 4] * u_traj[idx_k, 4]) + (B_mat[3, 5] * u_traj[idx_k, 5]));
    x_traj[idx_k + 1, 4] := ((A_mat[4, 1] * x_traj[idx_k, 1]) + (A_mat[4, 2] * x_traj[idx_k, 2]) + (A_mat[4, 3] * x_traj[idx_k, 3]) + (A_mat[4, 4] * x_traj[idx_k, 4]) + (A_mat[4, 5] * x_traj[idx_k, 5]) + (A_mat[4, 6] * x_traj[idx_k, 6])) + ((B_mat[4, 1] * u_traj[idx_k, 1]) + (B_mat[4, 2] * u_traj[idx_k, 2]) + (B_mat[4, 3] * u_traj[idx_k, 3]) + (B_mat[4, 4] * u_traj[idx_k, 4]) + (B_mat[4, 5] * u_traj[idx_k, 5]));
    x_traj[idx_k + 1, 5] := ((A_mat[5, 1] * x_traj[idx_k, 1]) + (A_mat[5, 2] * x_traj[idx_k, 2]) + (A_mat[5, 3] * x_traj[idx_k, 3]) + (A_mat[5, 4] * x_traj[idx_k, 4]) + (A_mat[5, 5] * x_traj[idx_k, 5]) + (A_mat[5, 6] * x_traj[idx_k, 6])) + ((B_mat[5, 1] * u_traj[idx_k, 1]) + (B_mat[5, 2] * u_traj[idx_k, 2]) + (B_mat[5, 3] * u_traj[idx_k, 3]) + (B_mat[5, 4] * u_traj[idx_k, 4]) + (B_mat[5, 5] * u_traj[idx_k, 5]));
    x_traj[idx_k + 1, 6] := ((A_mat[6, 1] * x_traj[idx_k, 1]) + (A_mat[6, 2] * x_traj[idx_k, 2]) + (A_mat[6, 3] * x_traj[idx_k, 3]) + (A_mat[6, 4] * x_traj[idx_k, 4]) + (A_mat[6, 5] * x_traj[idx_k, 5]) + (A_mat[6, 6] * x_traj[idx_k, 6])) + ((B_mat[6, 1] * u_traj[idx_k, 1]) + (B_mat[6, 2] * u_traj[idx_k, 2]) + (B_mat[6, 3] * u_traj[idx_k, 3]) + (B_mat[6, 4] * u_traj[idx_k, 4]) + (B_mat[6, 5] * u_traj[idx_k, 5]));
END_FOR;

(* Step 3.B: Terminal Horizon Adjoint Costate Evaluation (k = 5) *)
lambda_costate[5, 1] := P_term[1] * (x_traj[5, 1] - x_ref[1]);
lambda_costate[5, 2] := P_term[2] * (x_traj[5, 2] - x_ref[2]);
lambda_costate[5, 3] := P_term[3] * (x_traj[5, 3] - x_ref[3]);
lambda_costate[5, 4] := P_term[4] * (x_traj[5, 4] - x_ref[4]);
lambda_costate[5, 5] := P_term[5] * (x_traj[5, 5] - x_ref[5]);
lambda_costate[5, 6] := P_term[6] * (x_traj[5, 6] - x_ref[6]);

(* Step 3.C: Backward Adjoint Costate Propagation over Horizon k = 4 downto 0 *)
FOR idx_k := 4 TO 0 BY -1 DO
    lambda_costate[idx_k, 1] := ((A_mat[1, 1] * lambda_costate[idx_k + 1, 1]) + (A_mat[2, 1] * lambda_costate[idx_k + 1, 2]) + (A_mat[3, 1] * lambda_costate[idx_k + 1, 3]) + (A_mat[4, 1] * lambda_costate[idx_k + 1, 4]) + (A_mat[5, 1] * lambda_costate[idx_k + 1, 5]) + (A_mat[6, 1] * lambda_costate[idx_k + 1, 6])) + (Q_diag[1] * (x_traj[idx_k, 1] - x_ref[1]));
    lambda_costate[idx_k, 2] := ((A_mat[1, 2] * lambda_costate[idx_k + 1, 1]) + (A_mat[2, 2] * lambda_costate[idx_k + 1, 2]) + (A_mat[3, 2] * lambda_costate[idx_k + 1, 3]) + (A_mat[4, 2] * lambda_costate[idx_k + 1, 4]) + (A_mat[5, 2] * lambda_costate[idx_k + 1, 5]) + (A_mat[6, 2] * lambda_costate[idx_k + 1, 6])) + (Q_diag[2] * (x_traj[idx_k, 2] - x_ref[2]));
    lambda_costate[idx_k, 3] := ((A_mat[1, 3] * lambda_costate[idx_k + 1, 1]) + (A_mat[2, 3] * lambda_costate[idx_k + 1, 2]) + (A_mat[3, 3] * lambda_costate[idx_k + 1, 3]) + (A_mat[4, 3] * lambda_costate[idx_k + 1, 4]) + (A_mat[5, 3] * lambda_costate[idx_k + 1, 5]) + (A_mat[6, 3] * lambda_costate[idx_k + 1, 6])) + (Q_diag[3] * (x_traj[idx_k, 3] - x_ref[3]));
    lambda_costate[idx_k, 4] := ((A_mat[1, 4] * lambda_costate[idx_k + 1, 1]) + (A_mat[2, 4] * lambda_costate[idx_k + 1, 2]) + (A_mat[3, 4] * lambda_costate[idx_k + 1, 3]) + (A_mat[4, 4] * lambda_costate[idx_k + 1, 4]) + (A_mat[5, 4] * lambda_costate[idx_k + 1, 5]) + (A_mat[6, 4] * lambda_costate[idx_k + 1, 6])) + (Q_diag[4] * (x_traj[idx_k, 4] - x_ref[4]));
    lambda_costate[idx_k, 5] := ((A_mat[1, 5] * lambda_costate[idx_k + 1, 1]) + (A_mat[2, 5] * lambda_costate[idx_k + 1, 2]) + (A_mat[3, 5] * lambda_costate[idx_k + 1, 3]) + (A_mat[4, 5] * lambda_costate[idx_k + 1, 4]) + (A_mat[5, 5] * lambda_costate[idx_k + 1, 5]) + (A_mat[6, 5] * lambda_costate[idx_k + 1, 6])) + (Q_diag[5] * (x_traj[idx_k, 5] - x_ref[5]));
    lambda_costate[idx_k, 6] := ((A_mat[1, 6] * lambda_costate[idx_k + 1, 1]) + (A_mat[2, 6] * lambda_costate[idx_k + 1, 2]) + (A_mat[3, 6] * lambda_costate[idx_k + 1, 3]) + (A_mat[4, 6] * lambda_costate[idx_k + 1, 4]) + (A_mat[5, 6] * lambda_costate[idx_k + 1, 5]) + (A_mat[6, 6] * lambda_costate[idx_k + 1, 6])) + (Q_diag[6] * (x_traj[idx_k, 6] - x_ref[6]));
END_FOR;

(* Step 3.D: Control Gradient Computation & Projected Descent Step over Horizon k = 0 to 4 *)
FOR idx_k := 0 TO 4 DO
    (* Gradient Evaluation Control 1 *)
    IF idx_k = 0 THEN
        grad_u[0, 1] := ((B_mat[1, 1] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 1] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 1] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 1] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 1] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 1] * lambda_costate[idx_k + 1, 6])) + (R_diag[1] * u_traj[0, 1]) + (S_diag[1] * (u_traj[0, 1] - u_prev[1]));
    ELSE
        grad_u[idx_k, 1] := ((B_mat[1, 1] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 1] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 1] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 1] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 1] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 1] * lambda_costate[idx_k + 1, 6])) + (R_diag[1] * u_traj[idx_k, 1]) + (S_diag[1] * (u_traj[idx_k, 1] - u_traj[idx_k - 1, 1]));
    END_IF;
    
    (* Descent Step *)
    u_traj[idx_k, 1] := u_traj[idx_k, 1] - (r_PGD_StepSize_Alpha * grad_u[idx_k, 1]);
    
    (* Box Constraint Projection *)
    IF u_traj[idx_k, 1] < u_min[1] THEN
        u_traj[idx_k, 1] := u_min[1];
    ELSIF u_traj[idx_k, 1] > u_max[1] THEN
        u_traj[idx_k, 1] := u_max[1];
    END_IF;
    
    (* Dynamic Slew Rate Projection *)
    IF idx_k = 0 THEN
        r_TmpDeltaU := u_traj[0, 1] - u_prev[1];
        IF r_TmpDeltaU > delta_u_max[1] THEN
            u_traj[0, 1] := u_prev[1] + delta_u_max[1];
        ELSIF r_TmpDeltaU < -delta_u_max[1] THEN
            u_traj[0, 1] := u_prev[1] - delta_u_max[1];
        END_IF;
    ELSE
        r_TmpDeltaU := u_traj[idx_k, 1] - u_traj[idx_k - 1, 1];
        IF r_TmpDeltaU > delta_u_max[1] THEN
            u_traj[idx_k, 1] := u_traj[idx_k - 1, 1] + delta_u_max[1];
        ELSIF r_TmpDeltaU < -delta_u_max[1] THEN
            u_traj[idx_k, 1] := u_traj[idx_k - 1, 1] - delta_u_max[1];
        END_IF;
    END_IF;
    (* Gradient Evaluation Control 2 *)
    IF idx_k = 0 THEN
        grad_u[0, 2] := ((B_mat[1, 2] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 2] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 2] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 2] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 2] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 2] * lambda_costate[idx_k + 1, 6])) + (R_diag[2] * u_traj[0, 2]) + (S_diag[2] * (u_traj[0, 2] - u_prev[2]));
    ELSE
        grad_u[idx_k, 2] := ((B_mat[1, 2] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 2] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 2] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 2] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 2] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 2] * lambda_costate[idx_k + 1, 6])) + (R_diag[2] * u_traj[idx_k, 2]) + (S_diag[2] * (u_traj[idx_k, 2] - u_traj[idx_k - 1, 2]));
    END_IF;
    
    (* Descent Step *)
    u_traj[idx_k, 2] := u_traj[idx_k, 2] - (r_PGD_StepSize_Alpha * grad_u[idx_k, 2]);
    
    (* Box Constraint Projection *)
    IF u_traj[idx_k, 2] < u_min[2] THEN
        u_traj[idx_k, 2] := u_min[2];
    ELSIF u_traj[idx_k, 2] > u_max[2] THEN
        u_traj[idx_k, 2] := u_max[2];
    END_IF;
    
    (* Dynamic Slew Rate Projection *)
    IF idx_k = 0 THEN
        r_TmpDeltaU := u_traj[0, 2] - u_prev[2];
        IF r_TmpDeltaU > delta_u_max[2] THEN
            u_traj[0, 2] := u_prev[2] + delta_u_max[2];
        ELSIF r_TmpDeltaU < -delta_u_max[2] THEN
            u_traj[0, 2] := u_prev[2] - delta_u_max[2];
        END_IF;
    ELSE
        r_TmpDeltaU := u_traj[idx_k, 2] - u_traj[idx_k - 1, 2];
        IF r_TmpDeltaU > delta_u_max[2] THEN
            u_traj[idx_k, 2] := u_traj[idx_k - 1, 2] + delta_u_max[2];
        ELSIF r_TmpDeltaU < -delta_u_max[2] THEN
            u_traj[idx_k, 2] := u_traj[idx_k - 1, 2] - delta_u_max[2];
        END_IF;
    END_IF;
    (* Gradient Evaluation Control 3 *)
    IF idx_k = 0 THEN
        grad_u[0, 3] := ((B_mat[1, 3] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 3] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 3] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 3] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 3] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 3] * lambda_costate[idx_k + 1, 6])) + (R_diag[3] * u_traj[0, 3]) + (S_diag[3] * (u_traj[0, 3] - u_prev[3]));
    ELSE
        grad_u[idx_k, 3] := ((B_mat[1, 3] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 3] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 3] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 3] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 3] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 3] * lambda_costate[idx_k + 1, 6])) + (R_diag[3] * u_traj[idx_k, 3]) + (S_diag[3] * (u_traj[idx_k, 3] - u_traj[idx_k - 1, 3]));
    END_IF;
    
    (* Descent Step *)
    u_traj[idx_k, 3] := u_traj[idx_k, 3] - (r_PGD_StepSize_Alpha * grad_u[idx_k, 3]);
    
    (* Box Constraint Projection *)
    IF u_traj[idx_k, 3] < u_min[3] THEN
        u_traj[idx_k, 3] := u_min[3];
    ELSIF u_traj[idx_k, 3] > u_max[3] THEN
        u_traj[idx_k, 3] := u_max[3];
    END_IF;
    
    (* Dynamic Slew Rate Projection *)
    IF idx_k = 0 THEN
        r_TmpDeltaU := u_traj[0, 3] - u_prev[3];
        IF r_TmpDeltaU > delta_u_max[3] THEN
            u_traj[0, 3] := u_prev[3] + delta_u_max[3];
        ELSIF r_TmpDeltaU < -delta_u_max[3] THEN
            u_traj[0, 3] := u_prev[3] - delta_u_max[3];
        END_IF;
    ELSE
        r_TmpDeltaU := u_traj[idx_k, 3] - u_traj[idx_k - 1, 3];
        IF r_TmpDeltaU > delta_u_max[3] THEN
            u_traj[idx_k, 3] := u_traj[idx_k - 1, 3] + delta_u_max[3];
        ELSIF r_TmpDeltaU < -delta_u_max[3] THEN
            u_traj[idx_k, 3] := u_traj[idx_k - 1, 3] - delta_u_max[3];
        END_IF;
    END_IF;
    (* Gradient Evaluation Control 4 *)
    IF idx_k = 0 THEN
        grad_u[0, 4] := ((B_mat[1, 4] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 4] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 4] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 4] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 4] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 4] * lambda_costate[idx_k + 1, 6])) + (R_diag[4] * u_traj[0, 4]) + (S_diag[4] * (u_traj[0, 4] - u_prev[4]));
    ELSE
        grad_u[idx_k, 4] := ((B_mat[1, 4] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 4] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 4] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 4] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 4] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 4] * lambda_costate[idx_k + 1, 6])) + (R_diag[4] * u_traj[idx_k, 4]) + (S_diag[4] * (u_traj[idx_k, 4] - u_traj[idx_k - 1, 4]));
    END_IF;
    
    (* Descent Step *)
    u_traj[idx_k, 4] := u_traj[idx_k, 4] - (r_PGD_StepSize_Alpha * grad_u[idx_k, 4]);
    
    (* Box Constraint Projection *)
    IF u_traj[idx_k, 4] < u_min[4] THEN
        u_traj[idx_k, 4] := u_min[4];
    ELSIF u_traj[idx_k, 4] > u_max[4] THEN
        u_traj[idx_k, 4] := u_max[4];
    END_IF;
    
    (* Dynamic Slew Rate Projection *)
    IF idx_k = 0 THEN
        r_TmpDeltaU := u_traj[0, 4] - u_prev[4];
        IF r_TmpDeltaU > delta_u_max[4] THEN
            u_traj[0, 4] := u_prev[4] + delta_u_max[4];
        ELSIF r_TmpDeltaU < -delta_u_max[4] THEN
            u_traj[0, 4] := u_prev[4] - delta_u_max[4];
        END_IF;
    ELSE
        r_TmpDeltaU := u_traj[idx_k, 4] - u_traj[idx_k - 1, 4];
        IF r_TmpDeltaU > delta_u_max[4] THEN
            u_traj[idx_k, 4] := u_traj[idx_k - 1, 4] + delta_u_max[4];
        ELSIF r_TmpDeltaU < -delta_u_max[4] THEN
            u_traj[idx_k, 4] := u_traj[idx_k - 1, 4] - delta_u_max[4];
        END_IF;
    END_IF;
    (* Gradient Evaluation Control 5 *)
    IF idx_k = 0 THEN
        grad_u[0, 5] := ((B_mat[1, 5] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 5] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 5] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 5] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 5] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 5] * lambda_costate[idx_k + 1, 6])) + (R_diag[5] * u_traj[0, 5]) + (S_diag[5] * (u_traj[0, 5] - u_prev[5]));
    ELSE
        grad_u[idx_k, 5] := ((B_mat[1, 5] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 5] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 5] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 5] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 5] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 5] * lambda_costate[idx_k + 1, 6])) + (R_diag[5] * u_traj[idx_k, 5]) + (S_diag[5] * (u_traj[idx_k, 5] - u_traj[idx_k - 1, 5]));
    END_IF;
    
    (* Descent Step *)
    u_traj[idx_k, 5] := u_traj[idx_k, 5] - (r_PGD_StepSize_Alpha * grad_u[idx_k, 5]);
    
    (* Box Constraint Projection *)
    IF u_traj[idx_k, 5] < u_min[5] THEN
        u_traj[idx_k, 5] := u_min[5];
    ELSIF u_traj[idx_k, 5] > u_max[5] THEN
        u_traj[idx_k, 5] := u_max[5];
    END_IF;
    
    (* Dynamic Slew Rate Projection *)
    IF idx_k = 0 THEN
        r_TmpDeltaU := u_traj[0, 5] - u_prev[5];
        IF r_TmpDeltaU > delta_u_max[5] THEN
            u_traj[0, 5] := u_prev[5] + delta_u_max[5];
        ELSIF r_TmpDeltaU < -delta_u_max[5] THEN
            u_traj[0, 5] := u_prev[5] - delta_u_max[5];
        END_IF;
    ELSE
        r_TmpDeltaU := u_traj[idx_k, 5] - u_traj[idx_k - 1, 5];
        IF r_TmpDeltaU > delta_u_max[5] THEN
            u_traj[idx_k, 5] := u_traj[idx_k - 1, 5] + delta_u_max[5];
        ELSIF r_TmpDeltaU < -delta_u_max[5] THEN
            u_traj[idx_k, 5] := u_traj[idx_k - 1, 5] - delta_u_max[5];
        END_IF;
    END_IF;
END_FOR;

(* ============================================================================================== *)
(* PGD UNROLLED ITERATION 4 OF 10                                                               *)
(* ============================================================================================== *)
(* Step 4.A: Forward State Simulation over Horizon k = 0 to 4 *)
FOR idx_k := 0 TO 4 DO
    x_traj[idx_k + 1, 1] := ((A_mat[1, 1] * x_traj[idx_k, 1]) + (A_mat[1, 2] * x_traj[idx_k, 2]) + (A_mat[1, 3] * x_traj[idx_k, 3]) + (A_mat[1, 4] * x_traj[idx_k, 4]) + (A_mat[1, 5] * x_traj[idx_k, 5]) + (A_mat[1, 6] * x_traj[idx_k, 6])) + ((B_mat[1, 1] * u_traj[idx_k, 1]) + (B_mat[1, 2] * u_traj[idx_k, 2]) + (B_mat[1, 3] * u_traj[idx_k, 3]) + (B_mat[1, 4] * u_traj[idx_k, 4]) + (B_mat[1, 5] * u_traj[idx_k, 5]));
    x_traj[idx_k + 1, 2] := ((A_mat[2, 1] * x_traj[idx_k, 1]) + (A_mat[2, 2] * x_traj[idx_k, 2]) + (A_mat[2, 3] * x_traj[idx_k, 3]) + (A_mat[2, 4] * x_traj[idx_k, 4]) + (A_mat[2, 5] * x_traj[idx_k, 5]) + (A_mat[2, 6] * x_traj[idx_k, 6])) + ((B_mat[2, 1] * u_traj[idx_k, 1]) + (B_mat[2, 2] * u_traj[idx_k, 2]) + (B_mat[2, 3] * u_traj[idx_k, 3]) + (B_mat[2, 4] * u_traj[idx_k, 4]) + (B_mat[2, 5] * u_traj[idx_k, 5]));
    x_traj[idx_k + 1, 3] := ((A_mat[3, 1] * x_traj[idx_k, 1]) + (A_mat[3, 2] * x_traj[idx_k, 2]) + (A_mat[3, 3] * x_traj[idx_k, 3]) + (A_mat[3, 4] * x_traj[idx_k, 4]) + (A_mat[3, 5] * x_traj[idx_k, 5]) + (A_mat[3, 6] * x_traj[idx_k, 6])) + ((B_mat[3, 1] * u_traj[idx_k, 1]) + (B_mat[3, 2] * u_traj[idx_k, 2]) + (B_mat[3, 3] * u_traj[idx_k, 3]) + (B_mat[3, 4] * u_traj[idx_k, 4]) + (B_mat[3, 5] * u_traj[idx_k, 5]));
    x_traj[idx_k + 1, 4] := ((A_mat[4, 1] * x_traj[idx_k, 1]) + (A_mat[4, 2] * x_traj[idx_k, 2]) + (A_mat[4, 3] * x_traj[idx_k, 3]) + (A_mat[4, 4] * x_traj[idx_k, 4]) + (A_mat[4, 5] * x_traj[idx_k, 5]) + (A_mat[4, 6] * x_traj[idx_k, 6])) + ((B_mat[4, 1] * u_traj[idx_k, 1]) + (B_mat[4, 2] * u_traj[idx_k, 2]) + (B_mat[4, 3] * u_traj[idx_k, 3]) + (B_mat[4, 4] * u_traj[idx_k, 4]) + (B_mat[4, 5] * u_traj[idx_k, 5]));
    x_traj[idx_k + 1, 5] := ((A_mat[5, 1] * x_traj[idx_k, 1]) + (A_mat[5, 2] * x_traj[idx_k, 2]) + (A_mat[5, 3] * x_traj[idx_k, 3]) + (A_mat[5, 4] * x_traj[idx_k, 4]) + (A_mat[5, 5] * x_traj[idx_k, 5]) + (A_mat[5, 6] * x_traj[idx_k, 6])) + ((B_mat[5, 1] * u_traj[idx_k, 1]) + (B_mat[5, 2] * u_traj[idx_k, 2]) + (B_mat[5, 3] * u_traj[idx_k, 3]) + (B_mat[5, 4] * u_traj[idx_k, 4]) + (B_mat[5, 5] * u_traj[idx_k, 5]));
    x_traj[idx_k + 1, 6] := ((A_mat[6, 1] * x_traj[idx_k, 1]) + (A_mat[6, 2] * x_traj[idx_k, 2]) + (A_mat[6, 3] * x_traj[idx_k, 3]) + (A_mat[6, 4] * x_traj[idx_k, 4]) + (A_mat[6, 5] * x_traj[idx_k, 5]) + (A_mat[6, 6] * x_traj[idx_k, 6])) + ((B_mat[6, 1] * u_traj[idx_k, 1]) + (B_mat[6, 2] * u_traj[idx_k, 2]) + (B_mat[6, 3] * u_traj[idx_k, 3]) + (B_mat[6, 4] * u_traj[idx_k, 4]) + (B_mat[6, 5] * u_traj[idx_k, 5]));
END_FOR;

(* Step 4.B: Terminal Horizon Adjoint Costate Evaluation (k = 5) *)
lambda_costate[5, 1] := P_term[1] * (x_traj[5, 1] - x_ref[1]);
lambda_costate[5, 2] := P_term[2] * (x_traj[5, 2] - x_ref[2]);
lambda_costate[5, 3] := P_term[3] * (x_traj[5, 3] - x_ref[3]);
lambda_costate[5, 4] := P_term[4] * (x_traj[5, 4] - x_ref[4]);
lambda_costate[5, 5] := P_term[5] * (x_traj[5, 5] - x_ref[5]);
lambda_costate[5, 6] := P_term[6] * (x_traj[5, 6] - x_ref[6]);

(* Step 4.C: Backward Adjoint Costate Propagation over Horizon k = 4 downto 0 *)
FOR idx_k := 4 TO 0 BY -1 DO
    lambda_costate[idx_k, 1] := ((A_mat[1, 1] * lambda_costate[idx_k + 1, 1]) + (A_mat[2, 1] * lambda_costate[idx_k + 1, 2]) + (A_mat[3, 1] * lambda_costate[idx_k + 1, 3]) + (A_mat[4, 1] * lambda_costate[idx_k + 1, 4]) + (A_mat[5, 1] * lambda_costate[idx_k + 1, 5]) + (A_mat[6, 1] * lambda_costate[idx_k + 1, 6])) + (Q_diag[1] * (x_traj[idx_k, 1] - x_ref[1]));
    lambda_costate[idx_k, 2] := ((A_mat[1, 2] * lambda_costate[idx_k + 1, 1]) + (A_mat[2, 2] * lambda_costate[idx_k + 1, 2]) + (A_mat[3, 2] * lambda_costate[idx_k + 1, 3]) + (A_mat[4, 2] * lambda_costate[idx_k + 1, 4]) + (A_mat[5, 2] * lambda_costate[idx_k + 1, 5]) + (A_mat[6, 2] * lambda_costate[idx_k + 1, 6])) + (Q_diag[2] * (x_traj[idx_k, 2] - x_ref[2]));
    lambda_costate[idx_k, 3] := ((A_mat[1, 3] * lambda_costate[idx_k + 1, 1]) + (A_mat[2, 3] * lambda_costate[idx_k + 1, 2]) + (A_mat[3, 3] * lambda_costate[idx_k + 1, 3]) + (A_mat[4, 3] * lambda_costate[idx_k + 1, 4]) + (A_mat[5, 3] * lambda_costate[idx_k + 1, 5]) + (A_mat[6, 3] * lambda_costate[idx_k + 1, 6])) + (Q_diag[3] * (x_traj[idx_k, 3] - x_ref[3]));
    lambda_costate[idx_k, 4] := ((A_mat[1, 4] * lambda_costate[idx_k + 1, 1]) + (A_mat[2, 4] * lambda_costate[idx_k + 1, 2]) + (A_mat[3, 4] * lambda_costate[idx_k + 1, 3]) + (A_mat[4, 4] * lambda_costate[idx_k + 1, 4]) + (A_mat[5, 4] * lambda_costate[idx_k + 1, 5]) + (A_mat[6, 4] * lambda_costate[idx_k + 1, 6])) + (Q_diag[4] * (x_traj[idx_k, 4] - x_ref[4]));
    lambda_costate[idx_k, 5] := ((A_mat[1, 5] * lambda_costate[idx_k + 1, 1]) + (A_mat[2, 5] * lambda_costate[idx_k + 1, 2]) + (A_mat[3, 5] * lambda_costate[idx_k + 1, 3]) + (A_mat[4, 5] * lambda_costate[idx_k + 1, 4]) + (A_mat[5, 5] * lambda_costate[idx_k + 1, 5]) + (A_mat[6, 5] * lambda_costate[idx_k + 1, 6])) + (Q_diag[5] * (x_traj[idx_k, 5] - x_ref[5]));
    lambda_costate[idx_k, 6] := ((A_mat[1, 6] * lambda_costate[idx_k + 1, 1]) + (A_mat[2, 6] * lambda_costate[idx_k + 1, 2]) + (A_mat[3, 6] * lambda_costate[idx_k + 1, 3]) + (A_mat[4, 6] * lambda_costate[idx_k + 1, 4]) + (A_mat[5, 6] * lambda_costate[idx_k + 1, 5]) + (A_mat[6, 6] * lambda_costate[idx_k + 1, 6])) + (Q_diag[6] * (x_traj[idx_k, 6] - x_ref[6]));
END_FOR;

(* Step 4.D: Control Gradient Computation & Projected Descent Step over Horizon k = 0 to 4 *)
FOR idx_k := 0 TO 4 DO
    (* Gradient Evaluation Control 1 *)
    IF idx_k = 0 THEN
        grad_u[0, 1] := ((B_mat[1, 1] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 1] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 1] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 1] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 1] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 1] * lambda_costate[idx_k + 1, 6])) + (R_diag[1] * u_traj[0, 1]) + (S_diag[1] * (u_traj[0, 1] - u_prev[1]));
    ELSE
        grad_u[idx_k, 1] := ((B_mat[1, 1] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 1] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 1] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 1] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 1] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 1] * lambda_costate[idx_k + 1, 6])) + (R_diag[1] * u_traj[idx_k, 1]) + (S_diag[1] * (u_traj[idx_k, 1] - u_traj[idx_k - 1, 1]));
    END_IF;
    
    (* Descent Step *)
    u_traj[idx_k, 1] := u_traj[idx_k, 1] - (r_PGD_StepSize_Alpha * grad_u[idx_k, 1]);
    
    (* Box Constraint Projection *)
    IF u_traj[idx_k, 1] < u_min[1] THEN
        u_traj[idx_k, 1] := u_min[1];
    ELSIF u_traj[idx_k, 1] > u_max[1] THEN
        u_traj[idx_k, 1] := u_max[1];
    END_IF;
    
    (* Dynamic Slew Rate Projection *)
    IF idx_k = 0 THEN
        r_TmpDeltaU := u_traj[0, 1] - u_prev[1];
        IF r_TmpDeltaU > delta_u_max[1] THEN
            u_traj[0, 1] := u_prev[1] + delta_u_max[1];
        ELSIF r_TmpDeltaU < -delta_u_max[1] THEN
            u_traj[0, 1] := u_prev[1] - delta_u_max[1];
        END_IF;
    ELSE
        r_TmpDeltaU := u_traj[idx_k, 1] - u_traj[idx_k - 1, 1];
        IF r_TmpDeltaU > delta_u_max[1] THEN
            u_traj[idx_k, 1] := u_traj[idx_k - 1, 1] + delta_u_max[1];
        ELSIF r_TmpDeltaU < -delta_u_max[1] THEN
            u_traj[idx_k, 1] := u_traj[idx_k - 1, 1] - delta_u_max[1];
        END_IF;
    END_IF;
    (* Gradient Evaluation Control 2 *)
    IF idx_k = 0 THEN
        grad_u[0, 2] := ((B_mat[1, 2] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 2] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 2] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 2] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 2] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 2] * lambda_costate[idx_k + 1, 6])) + (R_diag[2] * u_traj[0, 2]) + (S_diag[2] * (u_traj[0, 2] - u_prev[2]));
    ELSE
        grad_u[idx_k, 2] := ((B_mat[1, 2] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 2] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 2] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 2] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 2] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 2] * lambda_costate[idx_k + 1, 6])) + (R_diag[2] * u_traj[idx_k, 2]) + (S_diag[2] * (u_traj[idx_k, 2] - u_traj[idx_k - 1, 2]));
    END_IF;
    
    (* Descent Step *)
    u_traj[idx_k, 2] := u_traj[idx_k, 2] - (r_PGD_StepSize_Alpha * grad_u[idx_k, 2]);
    
    (* Box Constraint Projection *)
    IF u_traj[idx_k, 2] < u_min[2] THEN
        u_traj[idx_k, 2] := u_min[2];
    ELSIF u_traj[idx_k, 2] > u_max[2] THEN
        u_traj[idx_k, 2] := u_max[2];
    END_IF;
    
    (* Dynamic Slew Rate Projection *)
    IF idx_k = 0 THEN
        r_TmpDeltaU := u_traj[0, 2] - u_prev[2];
        IF r_TmpDeltaU > delta_u_max[2] THEN
            u_traj[0, 2] := u_prev[2] + delta_u_max[2];
        ELSIF r_TmpDeltaU < -delta_u_max[2] THEN
            u_traj[0, 2] := u_prev[2] - delta_u_max[2];
        END_IF;
    ELSE
        r_TmpDeltaU := u_traj[idx_k, 2] - u_traj[idx_k - 1, 2];
        IF r_TmpDeltaU > delta_u_max[2] THEN
            u_traj[idx_k, 2] := u_traj[idx_k - 1, 2] + delta_u_max[2];
        ELSIF r_TmpDeltaU < -delta_u_max[2] THEN
            u_traj[idx_k, 2] := u_traj[idx_k - 1, 2] - delta_u_max[2];
        END_IF;
    END_IF;
    (* Gradient Evaluation Control 3 *)
    IF idx_k = 0 THEN
        grad_u[0, 3] := ((B_mat[1, 3] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 3] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 3] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 3] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 3] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 3] * lambda_costate[idx_k + 1, 6])) + (R_diag[3] * u_traj[0, 3]) + (S_diag[3] * (u_traj[0, 3] - u_prev[3]));
    ELSE
        grad_u[idx_k, 3] := ((B_mat[1, 3] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 3] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 3] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 3] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 3] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 3] * lambda_costate[idx_k + 1, 6])) + (R_diag[3] * u_traj[idx_k, 3]) + (S_diag[3] * (u_traj[idx_k, 3] - u_traj[idx_k - 1, 3]));
    END_IF;
    
    (* Descent Step *)
    u_traj[idx_k, 3] := u_traj[idx_k, 3] - (r_PGD_StepSize_Alpha * grad_u[idx_k, 3]);
    
    (* Box Constraint Projection *)
    IF u_traj[idx_k, 3] < u_min[3] THEN
        u_traj[idx_k, 3] := u_min[3];
    ELSIF u_traj[idx_k, 3] > u_max[3] THEN
        u_traj[idx_k, 3] := u_max[3];
    END_IF;
    
    (* Dynamic Slew Rate Projection *)
    IF idx_k = 0 THEN
        r_TmpDeltaU := u_traj[0, 3] - u_prev[3];
        IF r_TmpDeltaU > delta_u_max[3] THEN
            u_traj[0, 3] := u_prev[3] + delta_u_max[3];
        ELSIF r_TmpDeltaU < -delta_u_max[3] THEN
            u_traj[0, 3] := u_prev[3] - delta_u_max[3];
        END_IF;
    ELSE
        r_TmpDeltaU := u_traj[idx_k, 3] - u_traj[idx_k - 1, 3];
        IF r_TmpDeltaU > delta_u_max[3] THEN
            u_traj[idx_k, 3] := u_traj[idx_k - 1, 3] + delta_u_max[3];
        ELSIF r_TmpDeltaU < -delta_u_max[3] THEN
            u_traj[idx_k, 3] := u_traj[idx_k - 1, 3] - delta_u_max[3];
        END_IF;
    END_IF;
    (* Gradient Evaluation Control 4 *)
    IF idx_k = 0 THEN
        grad_u[0, 4] := ((B_mat[1, 4] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 4] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 4] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 4] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 4] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 4] * lambda_costate[idx_k + 1, 6])) + (R_diag[4] * u_traj[0, 4]) + (S_diag[4] * (u_traj[0, 4] - u_prev[4]));
    ELSE
        grad_u[idx_k, 4] := ((B_mat[1, 4] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 4] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 4] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 4] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 4] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 4] * lambda_costate[idx_k + 1, 6])) + (R_diag[4] * u_traj[idx_k, 4]) + (S_diag[4] * (u_traj[idx_k, 4] - u_traj[idx_k - 1, 4]));
    END_IF;
    
    (* Descent Step *)
    u_traj[idx_k, 4] := u_traj[idx_k, 4] - (r_PGD_StepSize_Alpha * grad_u[idx_k, 4]);
    
    (* Box Constraint Projection *)
    IF u_traj[idx_k, 4] < u_min[4] THEN
        u_traj[idx_k, 4] := u_min[4];
    ELSIF u_traj[idx_k, 4] > u_max[4] THEN
        u_traj[idx_k, 4] := u_max[4];
    END_IF;
    
    (* Dynamic Slew Rate Projection *)
    IF idx_k = 0 THEN
        r_TmpDeltaU := u_traj[0, 4] - u_prev[4];
        IF r_TmpDeltaU > delta_u_max[4] THEN
            u_traj[0, 4] := u_prev[4] + delta_u_max[4];
        ELSIF r_TmpDeltaU < -delta_u_max[4] THEN
            u_traj[0, 4] := u_prev[4] - delta_u_max[4];
        END_IF;
    ELSE
        r_TmpDeltaU := u_traj[idx_k, 4] - u_traj[idx_k - 1, 4];
        IF r_TmpDeltaU > delta_u_max[4] THEN
            u_traj[idx_k, 4] := u_traj[idx_k - 1, 4] + delta_u_max[4];
        ELSIF r_TmpDeltaU < -delta_u_max[4] THEN
            u_traj[idx_k, 4] := u_traj[idx_k - 1, 4] - delta_u_max[4];
        END_IF;
    END_IF;
    (* Gradient Evaluation Control 5 *)
    IF idx_k = 0 THEN
        grad_u[0, 5] := ((B_mat[1, 5] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 5] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 5] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 5] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 5] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 5] * lambda_costate[idx_k + 1, 6])) + (R_diag[5] * u_traj[0, 5]) + (S_diag[5] * (u_traj[0, 5] - u_prev[5]));
    ELSE
        grad_u[idx_k, 5] := ((B_mat[1, 5] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 5] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 5] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 5] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 5] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 5] * lambda_costate[idx_k + 1, 6])) + (R_diag[5] * u_traj[idx_k, 5]) + (S_diag[5] * (u_traj[idx_k, 5] - u_traj[idx_k - 1, 5]));
    END_IF;
    
    (* Descent Step *)
    u_traj[idx_k, 5] := u_traj[idx_k, 5] - (r_PGD_StepSize_Alpha * grad_u[idx_k, 5]);
    
    (* Box Constraint Projection *)
    IF u_traj[idx_k, 5] < u_min[5] THEN
        u_traj[idx_k, 5] := u_min[5];
    ELSIF u_traj[idx_k, 5] > u_max[5] THEN
        u_traj[idx_k, 5] := u_max[5];
    END_IF;
    
    (* Dynamic Slew Rate Projection *)
    IF idx_k = 0 THEN
        r_TmpDeltaU := u_traj[0, 5] - u_prev[5];
        IF r_TmpDeltaU > delta_u_max[5] THEN
            u_traj[0, 5] := u_prev[5] + delta_u_max[5];
        ELSIF r_TmpDeltaU < -delta_u_max[5] THEN
            u_traj[0, 5] := u_prev[5] - delta_u_max[5];
        END_IF;
    ELSE
        r_TmpDeltaU := u_traj[idx_k, 5] - u_traj[idx_k - 1, 5];
        IF r_TmpDeltaU > delta_u_max[5] THEN
            u_traj[idx_k, 5] := u_traj[idx_k - 1, 5] + delta_u_max[5];
        ELSIF r_TmpDeltaU < -delta_u_max[5] THEN
            u_traj[idx_k, 5] := u_traj[idx_k - 1, 5] - delta_u_max[5];
        END_IF;
    END_IF;
END_FOR;

(* ============================================================================================== *)
(* PGD UNROLLED ITERATION 5 OF 10                                                               *)
(* ============================================================================================== *)
(* Step 5.A: Forward State Simulation over Horizon k = 0 to 4 *)
FOR idx_k := 0 TO 4 DO
    x_traj[idx_k + 1, 1] := ((A_mat[1, 1] * x_traj[idx_k, 1]) + (A_mat[1, 2] * x_traj[idx_k, 2]) + (A_mat[1, 3] * x_traj[idx_k, 3]) + (A_mat[1, 4] * x_traj[idx_k, 4]) + (A_mat[1, 5] * x_traj[idx_k, 5]) + (A_mat[1, 6] * x_traj[idx_k, 6])) + ((B_mat[1, 1] * u_traj[idx_k, 1]) + (B_mat[1, 2] * u_traj[idx_k, 2]) + (B_mat[1, 3] * u_traj[idx_k, 3]) + (B_mat[1, 4] * u_traj[idx_k, 4]) + (B_mat[1, 5] * u_traj[idx_k, 5]));
    x_traj[idx_k + 1, 2] := ((A_mat[2, 1] * x_traj[idx_k, 1]) + (A_mat[2, 2] * x_traj[idx_k, 2]) + (A_mat[2, 3] * x_traj[idx_k, 3]) + (A_mat[2, 4] * x_traj[idx_k, 4]) + (A_mat[2, 5] * x_traj[idx_k, 5]) + (A_mat[2, 6] * x_traj[idx_k, 6])) + ((B_mat[2, 1] * u_traj[idx_k, 1]) + (B_mat[2, 2] * u_traj[idx_k, 2]) + (B_mat[2, 3] * u_traj[idx_k, 3]) + (B_mat[2, 4] * u_traj[idx_k, 4]) + (B_mat[2, 5] * u_traj[idx_k, 5]));
    x_traj[idx_k + 1, 3] := ((A_mat[3, 1] * x_traj[idx_k, 1]) + (A_mat[3, 2] * x_traj[idx_k, 2]) + (A_mat[3, 3] * x_traj[idx_k, 3]) + (A_mat[3, 4] * x_traj[idx_k, 4]) + (A_mat[3, 5] * x_traj[idx_k, 5]) + (A_mat[3, 6] * x_traj[idx_k, 6])) + ((B_mat[3, 1] * u_traj[idx_k, 1]) + (B_mat[3, 2] * u_traj[idx_k, 2]) + (B_mat[3, 3] * u_traj[idx_k, 3]) + (B_mat[3, 4] * u_traj[idx_k, 4]) + (B_mat[3, 5] * u_traj[idx_k, 5]));
    x_traj[idx_k + 1, 4] := ((A_mat[4, 1] * x_traj[idx_k, 1]) + (A_mat[4, 2] * x_traj[idx_k, 2]) + (A_mat[4, 3] * x_traj[idx_k, 3]) + (A_mat[4, 4] * x_traj[idx_k, 4]) + (A_mat[4, 5] * x_traj[idx_k, 5]) + (A_mat[4, 6] * x_traj[idx_k, 6])) + ((B_mat[4, 1] * u_traj[idx_k, 1]) + (B_mat[4, 2] * u_traj[idx_k, 2]) + (B_mat[4, 3] * u_traj[idx_k, 3]) + (B_mat[4, 4] * u_traj[idx_k, 4]) + (B_mat[4, 5] * u_traj[idx_k, 5]));
    x_traj[idx_k + 1, 5] := ((A_mat[5, 1] * x_traj[idx_k, 1]) + (A_mat[5, 2] * x_traj[idx_k, 2]) + (A_mat[5, 3] * x_traj[idx_k, 3]) + (A_mat[5, 4] * x_traj[idx_k, 4]) + (A_mat[5, 5] * x_traj[idx_k, 5]) + (A_mat[5, 6] * x_traj[idx_k, 6])) + ((B_mat[5, 1] * u_traj[idx_k, 1]) + (B_mat[5, 2] * u_traj[idx_k, 2]) + (B_mat[5, 3] * u_traj[idx_k, 3]) + (B_mat[5, 4] * u_traj[idx_k, 4]) + (B_mat[5, 5] * u_traj[idx_k, 5]));
    x_traj[idx_k + 1, 6] := ((A_mat[6, 1] * x_traj[idx_k, 1]) + (A_mat[6, 2] * x_traj[idx_k, 2]) + (A_mat[6, 3] * x_traj[idx_k, 3]) + (A_mat[6, 4] * x_traj[idx_k, 4]) + (A_mat[6, 5] * x_traj[idx_k, 5]) + (A_mat[6, 6] * x_traj[idx_k, 6])) + ((B_mat[6, 1] * u_traj[idx_k, 1]) + (B_mat[6, 2] * u_traj[idx_k, 2]) + (B_mat[6, 3] * u_traj[idx_k, 3]) + (B_mat[6, 4] * u_traj[idx_k, 4]) + (B_mat[6, 5] * u_traj[idx_k, 5]));
END_FOR;

(* Step 5.B: Terminal Horizon Adjoint Costate Evaluation (k = 5) *)
lambda_costate[5, 1] := P_term[1] * (x_traj[5, 1] - x_ref[1]);
lambda_costate[5, 2] := P_term[2] * (x_traj[5, 2] - x_ref[2]);
lambda_costate[5, 3] := P_term[3] * (x_traj[5, 3] - x_ref[3]);
lambda_costate[5, 4] := P_term[4] * (x_traj[5, 4] - x_ref[4]);
lambda_costate[5, 5] := P_term[5] * (x_traj[5, 5] - x_ref[5]);
lambda_costate[5, 6] := P_term[6] * (x_traj[5, 6] - x_ref[6]);

(* Step 5.C: Backward Adjoint Costate Propagation over Horizon k = 4 downto 0 *)
FOR idx_k := 4 TO 0 BY -1 DO
    lambda_costate[idx_k, 1] := ((A_mat[1, 1] * lambda_costate[idx_k + 1, 1]) + (A_mat[2, 1] * lambda_costate[idx_k + 1, 2]) + (A_mat[3, 1] * lambda_costate[idx_k + 1, 3]) + (A_mat[4, 1] * lambda_costate[idx_k + 1, 4]) + (A_mat[5, 1] * lambda_costate[idx_k + 1, 5]) + (A_mat[6, 1] * lambda_costate[idx_k + 1, 6])) + (Q_diag[1] * (x_traj[idx_k, 1] - x_ref[1]));
    lambda_costate[idx_k, 2] := ((A_mat[1, 2] * lambda_costate[idx_k + 1, 1]) + (A_mat[2, 2] * lambda_costate[idx_k + 1, 2]) + (A_mat[3, 2] * lambda_costate[idx_k + 1, 3]) + (A_mat[4, 2] * lambda_costate[idx_k + 1, 4]) + (A_mat[5, 2] * lambda_costate[idx_k + 1, 5]) + (A_mat[6, 2] * lambda_costate[idx_k + 1, 6])) + (Q_diag[2] * (x_traj[idx_k, 2] - x_ref[2]));
    lambda_costate[idx_k, 3] := ((A_mat[1, 3] * lambda_costate[idx_k + 1, 1]) + (A_mat[2, 3] * lambda_costate[idx_k + 1, 2]) + (A_mat[3, 3] * lambda_costate[idx_k + 1, 3]) + (A_mat[4, 3] * lambda_costate[idx_k + 1, 4]) + (A_mat[5, 3] * lambda_costate[idx_k + 1, 5]) + (A_mat[6, 3] * lambda_costate[idx_k + 1, 6])) + (Q_diag[3] * (x_traj[idx_k, 3] - x_ref[3]));
    lambda_costate[idx_k, 4] := ((A_mat[1, 4] * lambda_costate[idx_k + 1, 1]) + (A_mat[2, 4] * lambda_costate[idx_k + 1, 2]) + (A_mat[3, 4] * lambda_costate[idx_k + 1, 3]) + (A_mat[4, 4] * lambda_costate[idx_k + 1, 4]) + (A_mat[5, 4] * lambda_costate[idx_k + 1, 5]) + (A_mat[6, 4] * lambda_costate[idx_k + 1, 6])) + (Q_diag[4] * (x_traj[idx_k, 4] - x_ref[4]));
    lambda_costate[idx_k, 5] := ((A_mat[1, 5] * lambda_costate[idx_k + 1, 1]) + (A_mat[2, 5] * lambda_costate[idx_k + 1, 2]) + (A_mat[3, 5] * lambda_costate[idx_k + 1, 3]) + (A_mat[4, 5] * lambda_costate[idx_k + 1, 4]) + (A_mat[5, 5] * lambda_costate[idx_k + 1, 5]) + (A_mat[6, 5] * lambda_costate[idx_k + 1, 6])) + (Q_diag[5] * (x_traj[idx_k, 5] - x_ref[5]));
    lambda_costate[idx_k, 6] := ((A_mat[1, 6] * lambda_costate[idx_k + 1, 1]) + (A_mat[2, 6] * lambda_costate[idx_k + 1, 2]) + (A_mat[3, 6] * lambda_costate[idx_k + 1, 3]) + (A_mat[4, 6] * lambda_costate[idx_k + 1, 4]) + (A_mat[5, 6] * lambda_costate[idx_k + 1, 5]) + (A_mat[6, 6] * lambda_costate[idx_k + 1, 6])) + (Q_diag[6] * (x_traj[idx_k, 6] - x_ref[6]));
END_FOR;

(* Step 5.D: Control Gradient Computation & Projected Descent Step over Horizon k = 0 to 4 *)
FOR idx_k := 0 TO 4 DO
    (* Gradient Evaluation Control 1 *)
    IF idx_k = 0 THEN
        grad_u[0, 1] := ((B_mat[1, 1] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 1] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 1] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 1] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 1] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 1] * lambda_costate[idx_k + 1, 6])) + (R_diag[1] * u_traj[0, 1]) + (S_diag[1] * (u_traj[0, 1] - u_prev[1]));
    ELSE
        grad_u[idx_k, 1] := ((B_mat[1, 1] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 1] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 1] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 1] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 1] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 1] * lambda_costate[idx_k + 1, 6])) + (R_diag[1] * u_traj[idx_k, 1]) + (S_diag[1] * (u_traj[idx_k, 1] - u_traj[idx_k - 1, 1]));
    END_IF;
    
    (* Descent Step *)
    u_traj[idx_k, 1] := u_traj[idx_k, 1] - (r_PGD_StepSize_Alpha * grad_u[idx_k, 1]);
    
    (* Box Constraint Projection *)
    IF u_traj[idx_k, 1] < u_min[1] THEN
        u_traj[idx_k, 1] := u_min[1];
    ELSIF u_traj[idx_k, 1] > u_max[1] THEN
        u_traj[idx_k, 1] := u_max[1];
    END_IF;
    
    (* Dynamic Slew Rate Projection *)
    IF idx_k = 0 THEN
        r_TmpDeltaU := u_traj[0, 1] - u_prev[1];
        IF r_TmpDeltaU > delta_u_max[1] THEN
            u_traj[0, 1] := u_prev[1] + delta_u_max[1];
        ELSIF r_TmpDeltaU < -delta_u_max[1] THEN
            u_traj[0, 1] := u_prev[1] - delta_u_max[1];
        END_IF;
    ELSE
        r_TmpDeltaU := u_traj[idx_k, 1] - u_traj[idx_k - 1, 1];
        IF r_TmpDeltaU > delta_u_max[1] THEN
            u_traj[idx_k, 1] := u_traj[idx_k - 1, 1] + delta_u_max[1];
        ELSIF r_TmpDeltaU < -delta_u_max[1] THEN
            u_traj[idx_k, 1] := u_traj[idx_k - 1, 1] - delta_u_max[1];
        END_IF;
    END_IF;
    (* Gradient Evaluation Control 2 *)
    IF idx_k = 0 THEN
        grad_u[0, 2] := ((B_mat[1, 2] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 2] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 2] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 2] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 2] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 2] * lambda_costate[idx_k + 1, 6])) + (R_diag[2] * u_traj[0, 2]) + (S_diag[2] * (u_traj[0, 2] - u_prev[2]));
    ELSE
        grad_u[idx_k, 2] := ((B_mat[1, 2] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 2] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 2] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 2] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 2] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 2] * lambda_costate[idx_k + 1, 6])) + (R_diag[2] * u_traj[idx_k, 2]) + (S_diag[2] * (u_traj[idx_k, 2] - u_traj[idx_k - 1, 2]));
    END_IF;
    
    (* Descent Step *)
    u_traj[idx_k, 2] := u_traj[idx_k, 2] - (r_PGD_StepSize_Alpha * grad_u[idx_k, 2]);
    
    (* Box Constraint Projection *)
    IF u_traj[idx_k, 2] < u_min[2] THEN
        u_traj[idx_k, 2] := u_min[2];
    ELSIF u_traj[idx_k, 2] > u_max[2] THEN
        u_traj[idx_k, 2] := u_max[2];
    END_IF;
    
    (* Dynamic Slew Rate Projection *)
    IF idx_k = 0 THEN
        r_TmpDeltaU := u_traj[0, 2] - u_prev[2];
        IF r_TmpDeltaU > delta_u_max[2] THEN
            u_traj[0, 2] := u_prev[2] + delta_u_max[2];
        ELSIF r_TmpDeltaU < -delta_u_max[2] THEN
            u_traj[0, 2] := u_prev[2] - delta_u_max[2];
        END_IF;
    ELSE
        r_TmpDeltaU := u_traj[idx_k, 2] - u_traj[idx_k - 1, 2];
        IF r_TmpDeltaU > delta_u_max[2] THEN
            u_traj[idx_k, 2] := u_traj[idx_k - 1, 2] + delta_u_max[2];
        ELSIF r_TmpDeltaU < -delta_u_max[2] THEN
            u_traj[idx_k, 2] := u_traj[idx_k - 1, 2] - delta_u_max[2];
        END_IF;
    END_IF;
    (* Gradient Evaluation Control 3 *)
    IF idx_k = 0 THEN
        grad_u[0, 3] := ((B_mat[1, 3] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 3] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 3] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 3] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 3] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 3] * lambda_costate[idx_k + 1, 6])) + (R_diag[3] * u_traj[0, 3]) + (S_diag[3] * (u_traj[0, 3] - u_prev[3]));
    ELSE
        grad_u[idx_k, 3] := ((B_mat[1, 3] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 3] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 3] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 3] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 3] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 3] * lambda_costate[idx_k + 1, 6])) + (R_diag[3] * u_traj[idx_k, 3]) + (S_diag[3] * (u_traj[idx_k, 3] - u_traj[idx_k - 1, 3]));
    END_IF;
    
    (* Descent Step *)
    u_traj[idx_k, 3] := u_traj[idx_k, 3] - (r_PGD_StepSize_Alpha * grad_u[idx_k, 3]);
    
    (* Box Constraint Projection *)
    IF u_traj[idx_k, 3] < u_min[3] THEN
        u_traj[idx_k, 3] := u_min[3];
    ELSIF u_traj[idx_k, 3] > u_max[3] THEN
        u_traj[idx_k, 3] := u_max[3];
    END_IF;
    
    (* Dynamic Slew Rate Projection *)
    IF idx_k = 0 THEN
        r_TmpDeltaU := u_traj[0, 3] - u_prev[3];
        IF r_TmpDeltaU > delta_u_max[3] THEN
            u_traj[0, 3] := u_prev[3] + delta_u_max[3];
        ELSIF r_TmpDeltaU < -delta_u_max[3] THEN
            u_traj[0, 3] := u_prev[3] - delta_u_max[3];
        END_IF;
    ELSE
        r_TmpDeltaU := u_traj[idx_k, 3] - u_traj[idx_k - 1, 3];
        IF r_TmpDeltaU > delta_u_max[3] THEN
            u_traj[idx_k, 3] := u_traj[idx_k - 1, 3] + delta_u_max[3];
        ELSIF r_TmpDeltaU < -delta_u_max[3] THEN
            u_traj[idx_k, 3] := u_traj[idx_k - 1, 3] - delta_u_max[3];
        END_IF;
    END_IF;
    (* Gradient Evaluation Control 4 *)
    IF idx_k = 0 THEN
        grad_u[0, 4] := ((B_mat[1, 4] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 4] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 4] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 4] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 4] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 4] * lambda_costate[idx_k + 1, 6])) + (R_diag[4] * u_traj[0, 4]) + (S_diag[4] * (u_traj[0, 4] - u_prev[4]));
    ELSE
        grad_u[idx_k, 4] := ((B_mat[1, 4] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 4] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 4] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 4] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 4] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 4] * lambda_costate[idx_k + 1, 6])) + (R_diag[4] * u_traj[idx_k, 4]) + (S_diag[4] * (u_traj[idx_k, 4] - u_traj[idx_k - 1, 4]));
    END_IF;
    
    (* Descent Step *)
    u_traj[idx_k, 4] := u_traj[idx_k, 4] - (r_PGD_StepSize_Alpha * grad_u[idx_k, 4]);
    
    (* Box Constraint Projection *)
    IF u_traj[idx_k, 4] < u_min[4] THEN
        u_traj[idx_k, 4] := u_min[4];
    ELSIF u_traj[idx_k, 4] > u_max[4] THEN
        u_traj[idx_k, 4] := u_max[4];
    END_IF;
    
    (* Dynamic Slew Rate Projection *)
    IF idx_k = 0 THEN
        r_TmpDeltaU := u_traj[0, 4] - u_prev[4];
        IF r_TmpDeltaU > delta_u_max[4] THEN
            u_traj[0, 4] := u_prev[4] + delta_u_max[4];
        ELSIF r_TmpDeltaU < -delta_u_max[4] THEN
            u_traj[0, 4] := u_prev[4] - delta_u_max[4];
        END_IF;
    ELSE
        r_TmpDeltaU := u_traj[idx_k, 4] - u_traj[idx_k - 1, 4];
        IF r_TmpDeltaU > delta_u_max[4] THEN
            u_traj[idx_k, 4] := u_traj[idx_k - 1, 4] + delta_u_max[4];
        ELSIF r_TmpDeltaU < -delta_u_max[4] THEN
            u_traj[idx_k, 4] := u_traj[idx_k - 1, 4] - delta_u_max[4];
        END_IF;
    END_IF;
    (* Gradient Evaluation Control 5 *)
    IF idx_k = 0 THEN
        grad_u[0, 5] := ((B_mat[1, 5] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 5] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 5] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 5] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 5] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 5] * lambda_costate[idx_k + 1, 6])) + (R_diag[5] * u_traj[0, 5]) + (S_diag[5] * (u_traj[0, 5] - u_prev[5]));
    ELSE
        grad_u[idx_k, 5] := ((B_mat[1, 5] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 5] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 5] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 5] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 5] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 5] * lambda_costate[idx_k + 1, 6])) + (R_diag[5] * u_traj[idx_k, 5]) + (S_diag[5] * (u_traj[idx_k, 5] - u_traj[idx_k - 1, 5]));
    END_IF;
    
    (* Descent Step *)
    u_traj[idx_k, 5] := u_traj[idx_k, 5] - (r_PGD_StepSize_Alpha * grad_u[idx_k, 5]);
    
    (* Box Constraint Projection *)
    IF u_traj[idx_k, 5] < u_min[5] THEN
        u_traj[idx_k, 5] := u_min[5];
    ELSIF u_traj[idx_k, 5] > u_max[5] THEN
        u_traj[idx_k, 5] := u_max[5];
    END_IF;
    
    (* Dynamic Slew Rate Projection *)
    IF idx_k = 0 THEN
        r_TmpDeltaU := u_traj[0, 5] - u_prev[5];
        IF r_TmpDeltaU > delta_u_max[5] THEN
            u_traj[0, 5] := u_prev[5] + delta_u_max[5];
        ELSIF r_TmpDeltaU < -delta_u_max[5] THEN
            u_traj[0, 5] := u_prev[5] - delta_u_max[5];
        END_IF;
    ELSE
        r_TmpDeltaU := u_traj[idx_k, 5] - u_traj[idx_k - 1, 5];
        IF r_TmpDeltaU > delta_u_max[5] THEN
            u_traj[idx_k, 5] := u_traj[idx_k - 1, 5] + delta_u_max[5];
        ELSIF r_TmpDeltaU < -delta_u_max[5] THEN
            u_traj[idx_k, 5] := u_traj[idx_k - 1, 5] - delta_u_max[5];
        END_IF;
    END_IF;
END_FOR;

(* ============================================================================================== *)
(* PGD UNROLLED ITERATION 6 OF 10                                                               *)
(* ============================================================================================== *)
(* Step 6.A: Forward State Simulation over Horizon k = 0 to 4 *)
FOR idx_k := 0 TO 4 DO
    x_traj[idx_k + 1, 1] := ((A_mat[1, 1] * x_traj[idx_k, 1]) + (A_mat[1, 2] * x_traj[idx_k, 2]) + (A_mat[1, 3] * x_traj[idx_k, 3]) + (A_mat[1, 4] * x_traj[idx_k, 4]) + (A_mat[1, 5] * x_traj[idx_k, 5]) + (A_mat[1, 6] * x_traj[idx_k, 6])) + ((B_mat[1, 1] * u_traj[idx_k, 1]) + (B_mat[1, 2] * u_traj[idx_k, 2]) + (B_mat[1, 3] * u_traj[idx_k, 3]) + (B_mat[1, 4] * u_traj[idx_k, 4]) + (B_mat[1, 5] * u_traj[idx_k, 5]));
    x_traj[idx_k + 1, 2] := ((A_mat[2, 1] * x_traj[idx_k, 1]) + (A_mat[2, 2] * x_traj[idx_k, 2]) + (A_mat[2, 3] * x_traj[idx_k, 3]) + (A_mat[2, 4] * x_traj[idx_k, 4]) + (A_mat[2, 5] * x_traj[idx_k, 5]) + (A_mat[2, 6] * x_traj[idx_k, 6])) + ((B_mat[2, 1] * u_traj[idx_k, 1]) + (B_mat[2, 2] * u_traj[idx_k, 2]) + (B_mat[2, 3] * u_traj[idx_k, 3]) + (B_mat[2, 4] * u_traj[idx_k, 4]) + (B_mat[2, 5] * u_traj[idx_k, 5]));
    x_traj[idx_k + 1, 3] := ((A_mat[3, 1] * x_traj[idx_k, 1]) + (A_mat[3, 2] * x_traj[idx_k, 2]) + (A_mat[3, 3] * x_traj[idx_k, 3]) + (A_mat[3, 4] * x_traj[idx_k, 4]) + (A_mat[3, 5] * x_traj[idx_k, 5]) + (A_mat[3, 6] * x_traj[idx_k, 6])) + ((B_mat[3, 1] * u_traj[idx_k, 1]) + (B_mat[3, 2] * u_traj[idx_k, 2]) + (B_mat[3, 3] * u_traj[idx_k, 3]) + (B_mat[3, 4] * u_traj[idx_k, 4]) + (B_mat[3, 5] * u_traj[idx_k, 5]));
    x_traj[idx_k + 1, 4] := ((A_mat[4, 1] * x_traj[idx_k, 1]) + (A_mat[4, 2] * x_traj[idx_k, 2]) + (A_mat[4, 3] * x_traj[idx_k, 3]) + (A_mat[4, 4] * x_traj[idx_k, 4]) + (A_mat[4, 5] * x_traj[idx_k, 5]) + (A_mat[4, 6] * x_traj[idx_k, 6])) + ((B_mat[4, 1] * u_traj[idx_k, 1]) + (B_mat[4, 2] * u_traj[idx_k, 2]) + (B_mat[4, 3] * u_traj[idx_k, 3]) + (B_mat[4, 4] * u_traj[idx_k, 4]) + (B_mat[4, 5] * u_traj[idx_k, 5]));
    x_traj[idx_k + 1, 5] := ((A_mat[5, 1] * x_traj[idx_k, 1]) + (A_mat[5, 2] * x_traj[idx_k, 2]) + (A_mat[5, 3] * x_traj[idx_k, 3]) + (A_mat[5, 4] * x_traj[idx_k, 4]) + (A_mat[5, 5] * x_traj[idx_k, 5]) + (A_mat[5, 6] * x_traj[idx_k, 6])) + ((B_mat[5, 1] * u_traj[idx_k, 1]) + (B_mat[5, 2] * u_traj[idx_k, 2]) + (B_mat[5, 3] * u_traj[idx_k, 3]) + (B_mat[5, 4] * u_traj[idx_k, 4]) + (B_mat[5, 5] * u_traj[idx_k, 5]));
    x_traj[idx_k + 1, 6] := ((A_mat[6, 1] * x_traj[idx_k, 1]) + (A_mat[6, 2] * x_traj[idx_k, 2]) + (A_mat[6, 3] * x_traj[idx_k, 3]) + (A_mat[6, 4] * x_traj[idx_k, 4]) + (A_mat[6, 5] * x_traj[idx_k, 5]) + (A_mat[6, 6] * x_traj[idx_k, 6])) + ((B_mat[6, 1] * u_traj[idx_k, 1]) + (B_mat[6, 2] * u_traj[idx_k, 2]) + (B_mat[6, 3] * u_traj[idx_k, 3]) + (B_mat[6, 4] * u_traj[idx_k, 4]) + (B_mat[6, 5] * u_traj[idx_k, 5]));
END_FOR;

(* Step 6.B: Terminal Horizon Adjoint Costate Evaluation (k = 5) *)
lambda_costate[5, 1] := P_term[1] * (x_traj[5, 1] - x_ref[1]);
lambda_costate[5, 2] := P_term[2] * (x_traj[5, 2] - x_ref[2]);
lambda_costate[5, 3] := P_term[3] * (x_traj[5, 3] - x_ref[3]);
lambda_costate[5, 4] := P_term[4] * (x_traj[5, 4] - x_ref[4]);
lambda_costate[5, 5] := P_term[5] * (x_traj[5, 5] - x_ref[5]);
lambda_costate[5, 6] := P_term[6] * (x_traj[5, 6] - x_ref[6]);

(* Step 6.C: Backward Adjoint Costate Propagation over Horizon k = 4 downto 0 *)
FOR idx_k := 4 TO 0 BY -1 DO
    lambda_costate[idx_k, 1] := ((A_mat[1, 1] * lambda_costate[idx_k + 1, 1]) + (A_mat[2, 1] * lambda_costate[idx_k + 1, 2]) + (A_mat[3, 1] * lambda_costate[idx_k + 1, 3]) + (A_mat[4, 1] * lambda_costate[idx_k + 1, 4]) + (A_mat[5, 1] * lambda_costate[idx_k + 1, 5]) + (A_mat[6, 1] * lambda_costate[idx_k + 1, 6])) + (Q_diag[1] * (x_traj[idx_k, 1] - x_ref[1]));
    lambda_costate[idx_k, 2] := ((A_mat[1, 2] * lambda_costate[idx_k + 1, 1]) + (A_mat[2, 2] * lambda_costate[idx_k + 1, 2]) + (A_mat[3, 2] * lambda_costate[idx_k + 1, 3]) + (A_mat[4, 2] * lambda_costate[idx_k + 1, 4]) + (A_mat[5, 2] * lambda_costate[idx_k + 1, 5]) + (A_mat[6, 2] * lambda_costate[idx_k + 1, 6])) + (Q_diag[2] * (x_traj[idx_k, 2] - x_ref[2]));
    lambda_costate[idx_k, 3] := ((A_mat[1, 3] * lambda_costate[idx_k + 1, 1]) + (A_mat[2, 3] * lambda_costate[idx_k + 1, 2]) + (A_mat[3, 3] * lambda_costate[idx_k + 1, 3]) + (A_mat[4, 3] * lambda_costate[idx_k + 1, 4]) + (A_mat[5, 3] * lambda_costate[idx_k + 1, 5]) + (A_mat[6, 3] * lambda_costate[idx_k + 1, 6])) + (Q_diag[3] * (x_traj[idx_k, 3] - x_ref[3]));
    lambda_costate[idx_k, 4] := ((A_mat[1, 4] * lambda_costate[idx_k + 1, 1]) + (A_mat[2, 4] * lambda_costate[idx_k + 1, 2]) + (A_mat[3, 4] * lambda_costate[idx_k + 1, 3]) + (A_mat[4, 4] * lambda_costate[idx_k + 1, 4]) + (A_mat[5, 4] * lambda_costate[idx_k + 1, 5]) + (A_mat[6, 4] * lambda_costate[idx_k + 1, 6])) + (Q_diag[4] * (x_traj[idx_k, 4] - x_ref[4]));
    lambda_costate[idx_k, 5] := ((A_mat[1, 5] * lambda_costate[idx_k + 1, 1]) + (A_mat[2, 5] * lambda_costate[idx_k + 1, 2]) + (A_mat[3, 5] * lambda_costate[idx_k + 1, 3]) + (A_mat[4, 5] * lambda_costate[idx_k + 1, 4]) + (A_mat[5, 5] * lambda_costate[idx_k + 1, 5]) + (A_mat[6, 5] * lambda_costate[idx_k + 1, 6])) + (Q_diag[5] * (x_traj[idx_k, 5] - x_ref[5]));
    lambda_costate[idx_k, 6] := ((A_mat[1, 6] * lambda_costate[idx_k + 1, 1]) + (A_mat[2, 6] * lambda_costate[idx_k + 1, 2]) + (A_mat[3, 6] * lambda_costate[idx_k + 1, 3]) + (A_mat[4, 6] * lambda_costate[idx_k + 1, 4]) + (A_mat[5, 6] * lambda_costate[idx_k + 1, 5]) + (A_mat[6, 6] * lambda_costate[idx_k + 1, 6])) + (Q_diag[6] * (x_traj[idx_k, 6] - x_ref[6]));
END_FOR;

(* Step 6.D: Control Gradient Computation & Projected Descent Step over Horizon k = 0 to 4 *)
FOR idx_k := 0 TO 4 DO
    (* Gradient Evaluation Control 1 *)
    IF idx_k = 0 THEN
        grad_u[0, 1] := ((B_mat[1, 1] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 1] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 1] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 1] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 1] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 1] * lambda_costate[idx_k + 1, 6])) + (R_diag[1] * u_traj[0, 1]) + (S_diag[1] * (u_traj[0, 1] - u_prev[1]));
    ELSE
        grad_u[idx_k, 1] := ((B_mat[1, 1] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 1] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 1] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 1] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 1] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 1] * lambda_costate[idx_k + 1, 6])) + (R_diag[1] * u_traj[idx_k, 1]) + (S_diag[1] * (u_traj[idx_k, 1] - u_traj[idx_k - 1, 1]));
    END_IF;
    
    (* Descent Step *)
    u_traj[idx_k, 1] := u_traj[idx_k, 1] - (r_PGD_StepSize_Alpha * grad_u[idx_k, 1]);
    
    (* Box Constraint Projection *)
    IF u_traj[idx_k, 1] < u_min[1] THEN
        u_traj[idx_k, 1] := u_min[1];
    ELSIF u_traj[idx_k, 1] > u_max[1] THEN
        u_traj[idx_k, 1] := u_max[1];
    END_IF;
    
    (* Dynamic Slew Rate Projection *)
    IF idx_k = 0 THEN
        r_TmpDeltaU := u_traj[0, 1] - u_prev[1];
        IF r_TmpDeltaU > delta_u_max[1] THEN
            u_traj[0, 1] := u_prev[1] + delta_u_max[1];
        ELSIF r_TmpDeltaU < -delta_u_max[1] THEN
            u_traj[0, 1] := u_prev[1] - delta_u_max[1];
        END_IF;
    ELSE
        r_TmpDeltaU := u_traj[idx_k, 1] - u_traj[idx_k - 1, 1];
        IF r_TmpDeltaU > delta_u_max[1] THEN
            u_traj[idx_k, 1] := u_traj[idx_k - 1, 1] + delta_u_max[1];
        ELSIF r_TmpDeltaU < -delta_u_max[1] THEN
            u_traj[idx_k, 1] := u_traj[idx_k - 1, 1] - delta_u_max[1];
        END_IF;
    END_IF;
    (* Gradient Evaluation Control 2 *)
    IF idx_k = 0 THEN
        grad_u[0, 2] := ((B_mat[1, 2] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 2] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 2] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 2] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 2] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 2] * lambda_costate[idx_k + 1, 6])) + (R_diag[2] * u_traj[0, 2]) + (S_diag[2] * (u_traj[0, 2] - u_prev[2]));
    ELSE
        grad_u[idx_k, 2] := ((B_mat[1, 2] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 2] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 2] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 2] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 2] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 2] * lambda_costate[idx_k + 1, 6])) + (R_diag[2] * u_traj[idx_k, 2]) + (S_diag[2] * (u_traj[idx_k, 2] - u_traj[idx_k - 1, 2]));
    END_IF;
    
    (* Descent Step *)
    u_traj[idx_k, 2] := u_traj[idx_k, 2] - (r_PGD_StepSize_Alpha * grad_u[idx_k, 2]);
    
    (* Box Constraint Projection *)
    IF u_traj[idx_k, 2] < u_min[2] THEN
        u_traj[idx_k, 2] := u_min[2];
    ELSIF u_traj[idx_k, 2] > u_max[2] THEN
        u_traj[idx_k, 2] := u_max[2];
    END_IF;
    
    (* Dynamic Slew Rate Projection *)
    IF idx_k = 0 THEN
        r_TmpDeltaU := u_traj[0, 2] - u_prev[2];
        IF r_TmpDeltaU > delta_u_max[2] THEN
            u_traj[0, 2] := u_prev[2] + delta_u_max[2];
        ELSIF r_TmpDeltaU < -delta_u_max[2] THEN
            u_traj[0, 2] := u_prev[2] - delta_u_max[2];
        END_IF;
    ELSE
        r_TmpDeltaU := u_traj[idx_k, 2] - u_traj[idx_k - 1, 2];
        IF r_TmpDeltaU > delta_u_max[2] THEN
            u_traj[idx_k, 2] := u_traj[idx_k - 1, 2] + delta_u_max[2];
        ELSIF r_TmpDeltaU < -delta_u_max[2] THEN
            u_traj[idx_k, 2] := u_traj[idx_k - 1, 2] - delta_u_max[2];
        END_IF;
    END_IF;
    (* Gradient Evaluation Control 3 *)
    IF idx_k = 0 THEN
        grad_u[0, 3] := ((B_mat[1, 3] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 3] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 3] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 3] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 3] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 3] * lambda_costate[idx_k + 1, 6])) + (R_diag[3] * u_traj[0, 3]) + (S_diag[3] * (u_traj[0, 3] - u_prev[3]));
    ELSE
        grad_u[idx_k, 3] := ((B_mat[1, 3] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 3] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 3] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 3] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 3] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 3] * lambda_costate[idx_k + 1, 6])) + (R_diag[3] * u_traj[idx_k, 3]) + (S_diag[3] * (u_traj[idx_k, 3] - u_traj[idx_k - 1, 3]));
    END_IF;
    
    (* Descent Step *)
    u_traj[idx_k, 3] := u_traj[idx_k, 3] - (r_PGD_StepSize_Alpha * grad_u[idx_k, 3]);
    
    (* Box Constraint Projection *)
    IF u_traj[idx_k, 3] < u_min[3] THEN
        u_traj[idx_k, 3] := u_min[3];
    ELSIF u_traj[idx_k, 3] > u_max[3] THEN
        u_traj[idx_k, 3] := u_max[3];
    END_IF;
    
    (* Dynamic Slew Rate Projection *)
    IF idx_k = 0 THEN
        r_TmpDeltaU := u_traj[0, 3] - u_prev[3];
        IF r_TmpDeltaU > delta_u_max[3] THEN
            u_traj[0, 3] := u_prev[3] + delta_u_max[3];
        ELSIF r_TmpDeltaU < -delta_u_max[3] THEN
            u_traj[0, 3] := u_prev[3] - delta_u_max[3];
        END_IF;
    ELSE
        r_TmpDeltaU := u_traj[idx_k, 3] - u_traj[idx_k - 1, 3];
        IF r_TmpDeltaU > delta_u_max[3] THEN
            u_traj[idx_k, 3] := u_traj[idx_k - 1, 3] + delta_u_max[3];
        ELSIF r_TmpDeltaU < -delta_u_max[3] THEN
            u_traj[idx_k, 3] := u_traj[idx_k - 1, 3] - delta_u_max[3];
        END_IF;
    END_IF;
    (* Gradient Evaluation Control 4 *)
    IF idx_k = 0 THEN
        grad_u[0, 4] := ((B_mat[1, 4] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 4] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 4] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 4] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 4] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 4] * lambda_costate[idx_k + 1, 6])) + (R_diag[4] * u_traj[0, 4]) + (S_diag[4] * (u_traj[0, 4] - u_prev[4]));
    ELSE
        grad_u[idx_k, 4] := ((B_mat[1, 4] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 4] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 4] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 4] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 4] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 4] * lambda_costate[idx_k + 1, 6])) + (R_diag[4] * u_traj[idx_k, 4]) + (S_diag[4] * (u_traj[idx_k, 4] - u_traj[idx_k - 1, 4]));
    END_IF;
    
    (* Descent Step *)
    u_traj[idx_k, 4] := u_traj[idx_k, 4] - (r_PGD_StepSize_Alpha * grad_u[idx_k, 4]);
    
    (* Box Constraint Projection *)
    IF u_traj[idx_k, 4] < u_min[4] THEN
        u_traj[idx_k, 4] := u_min[4];
    ELSIF u_traj[idx_k, 4] > u_max[4] THEN
        u_traj[idx_k, 4] := u_max[4];
    END_IF;
    
    (* Dynamic Slew Rate Projection *)
    IF idx_k = 0 THEN
        r_TmpDeltaU := u_traj[0, 4] - u_prev[4];
        IF r_TmpDeltaU > delta_u_max[4] THEN
            u_traj[0, 4] := u_prev[4] + delta_u_max[4];
        ELSIF r_TmpDeltaU < -delta_u_max[4] THEN
            u_traj[0, 4] := u_prev[4] - delta_u_max[4];
        END_IF;
    ELSE
        r_TmpDeltaU := u_traj[idx_k, 4] - u_traj[idx_k - 1, 4];
        IF r_TmpDeltaU > delta_u_max[4] THEN
            u_traj[idx_k, 4] := u_traj[idx_k - 1, 4] + delta_u_max[4];
        ELSIF r_TmpDeltaU < -delta_u_max[4] THEN
            u_traj[idx_k, 4] := u_traj[idx_k - 1, 4] - delta_u_max[4];
        END_IF;
    END_IF;
    (* Gradient Evaluation Control 5 *)
    IF idx_k = 0 THEN
        grad_u[0, 5] := ((B_mat[1, 5] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 5] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 5] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 5] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 5] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 5] * lambda_costate[idx_k + 1, 6])) + (R_diag[5] * u_traj[0, 5]) + (S_diag[5] * (u_traj[0, 5] - u_prev[5]));
    ELSE
        grad_u[idx_k, 5] := ((B_mat[1, 5] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 5] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 5] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 5] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 5] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 5] * lambda_costate[idx_k + 1, 6])) + (R_diag[5] * u_traj[idx_k, 5]) + (S_diag[5] * (u_traj[idx_k, 5] - u_traj[idx_k - 1, 5]));
    END_IF;
    
    (* Descent Step *)
    u_traj[idx_k, 5] := u_traj[idx_k, 5] - (r_PGD_StepSize_Alpha * grad_u[idx_k, 5]);
    
    (* Box Constraint Projection *)
    IF u_traj[idx_k, 5] < u_min[5] THEN
        u_traj[idx_k, 5] := u_min[5];
    ELSIF u_traj[idx_k, 5] > u_max[5] THEN
        u_traj[idx_k, 5] := u_max[5];
    END_IF;
    
    (* Dynamic Slew Rate Projection *)
    IF idx_k = 0 THEN
        r_TmpDeltaU := u_traj[0, 5] - u_prev[5];
        IF r_TmpDeltaU > delta_u_max[5] THEN
            u_traj[0, 5] := u_prev[5] + delta_u_max[5];
        ELSIF r_TmpDeltaU < -delta_u_max[5] THEN
            u_traj[0, 5] := u_prev[5] - delta_u_max[5];
        END_IF;
    ELSE
        r_TmpDeltaU := u_traj[idx_k, 5] - u_traj[idx_k - 1, 5];
        IF r_TmpDeltaU > delta_u_max[5] THEN
            u_traj[idx_k, 5] := u_traj[idx_k - 1, 5] + delta_u_max[5];
        ELSIF r_TmpDeltaU < -delta_u_max[5] THEN
            u_traj[idx_k, 5] := u_traj[idx_k - 1, 5] - delta_u_max[5];
        END_IF;
    END_IF;
END_FOR;

(* ============================================================================================== *)
(* PGD UNROLLED ITERATION 7 OF 10                                                               *)
(* ============================================================================================== *)
(* Step 7.A: Forward State Simulation over Horizon k = 0 to 4 *)
FOR idx_k := 0 TO 4 DO
    x_traj[idx_k + 1, 1] := ((A_mat[1, 1] * x_traj[idx_k, 1]) + (A_mat[1, 2] * x_traj[idx_k, 2]) + (A_mat[1, 3] * x_traj[idx_k, 3]) + (A_mat[1, 4] * x_traj[idx_k, 4]) + (A_mat[1, 5] * x_traj[idx_k, 5]) + (A_mat[1, 6] * x_traj[idx_k, 6])) + ((B_mat[1, 1] * u_traj[idx_k, 1]) + (B_mat[1, 2] * u_traj[idx_k, 2]) + (B_mat[1, 3] * u_traj[idx_k, 3]) + (B_mat[1, 4] * u_traj[idx_k, 4]) + (B_mat[1, 5] * u_traj[idx_k, 5]));
    x_traj[idx_k + 1, 2] := ((A_mat[2, 1] * x_traj[idx_k, 1]) + (A_mat[2, 2] * x_traj[idx_k, 2]) + (A_mat[2, 3] * x_traj[idx_k, 3]) + (A_mat[2, 4] * x_traj[idx_k, 4]) + (A_mat[2, 5] * x_traj[idx_k, 5]) + (A_mat[2, 6] * x_traj[idx_k, 6])) + ((B_mat[2, 1] * u_traj[idx_k, 1]) + (B_mat[2, 2] * u_traj[idx_k, 2]) + (B_mat[2, 3] * u_traj[idx_k, 3]) + (B_mat[2, 4] * u_traj[idx_k, 4]) + (B_mat[2, 5] * u_traj[idx_k, 5]));
    x_traj[idx_k + 1, 3] := ((A_mat[3, 1] * x_traj[idx_k, 1]) + (A_mat[3, 2] * x_traj[idx_k, 2]) + (A_mat[3, 3] * x_traj[idx_k, 3]) + (A_mat[3, 4] * x_traj[idx_k, 4]) + (A_mat[3, 5] * x_traj[idx_k, 5]) + (A_mat[3, 6] * x_traj[idx_k, 6])) + ((B_mat[3, 1] * u_traj[idx_k, 1]) + (B_mat[3, 2] * u_traj[idx_k, 2]) + (B_mat[3, 3] * u_traj[idx_k, 3]) + (B_mat[3, 4] * u_traj[idx_k, 4]) + (B_mat[3, 5] * u_traj[idx_k, 5]));
    x_traj[idx_k + 1, 4] := ((A_mat[4, 1] * x_traj[idx_k, 1]) + (A_mat[4, 2] * x_traj[idx_k, 2]) + (A_mat[4, 3] * x_traj[idx_k, 3]) + (A_mat[4, 4] * x_traj[idx_k, 4]) + (A_mat[4, 5] * x_traj[idx_k, 5]) + (A_mat[4, 6] * x_traj[idx_k, 6])) + ((B_mat[4, 1] * u_traj[idx_k, 1]) + (B_mat[4, 2] * u_traj[idx_k, 2]) + (B_mat[4, 3] * u_traj[idx_k, 3]) + (B_mat[4, 4] * u_traj[idx_k, 4]) + (B_mat[4, 5] * u_traj[idx_k, 5]));
    x_traj[idx_k + 1, 5] := ((A_mat[5, 1] * x_traj[idx_k, 1]) + (A_mat[5, 2] * x_traj[idx_k, 2]) + (A_mat[5, 3] * x_traj[idx_k, 3]) + (A_mat[5, 4] * x_traj[idx_k, 4]) + (A_mat[5, 5] * x_traj[idx_k, 5]) + (A_mat[5, 6] * x_traj[idx_k, 6])) + ((B_mat[5, 1] * u_traj[idx_k, 1]) + (B_mat[5, 2] * u_traj[idx_k, 2]) + (B_mat[5, 3] * u_traj[idx_k, 3]) + (B_mat[5, 4] * u_traj[idx_k, 4]) + (B_mat[5, 5] * u_traj[idx_k, 5]));
    x_traj[idx_k + 1, 6] := ((A_mat[6, 1] * x_traj[idx_k, 1]) + (A_mat[6, 2] * x_traj[idx_k, 2]) + (A_mat[6, 3] * x_traj[idx_k, 3]) + (A_mat[6, 4] * x_traj[idx_k, 4]) + (A_mat[6, 5] * x_traj[idx_k, 5]) + (A_mat[6, 6] * x_traj[idx_k, 6])) + ((B_mat[6, 1] * u_traj[idx_k, 1]) + (B_mat[6, 2] * u_traj[idx_k, 2]) + (B_mat[6, 3] * u_traj[idx_k, 3]) + (B_mat[6, 4] * u_traj[idx_k, 4]) + (B_mat[6, 5] * u_traj[idx_k, 5]));
END_FOR;

(* Step 7.B: Terminal Horizon Adjoint Costate Evaluation (k = 5) *)
lambda_costate[5, 1] := P_term[1] * (x_traj[5, 1] - x_ref[1]);
lambda_costate[5, 2] := P_term[2] * (x_traj[5, 2] - x_ref[2]);
lambda_costate[5, 3] := P_term[3] * (x_traj[5, 3] - x_ref[3]);
lambda_costate[5, 4] := P_term[4] * (x_traj[5, 4] - x_ref[4]);
lambda_costate[5, 5] := P_term[5] * (x_traj[5, 5] - x_ref[5]);
lambda_costate[5, 6] := P_term[6] * (x_traj[5, 6] - x_ref[6]);

(* Step 7.C: Backward Adjoint Costate Propagation over Horizon k = 4 downto 0 *)
FOR idx_k := 4 TO 0 BY -1 DO
    lambda_costate[idx_k, 1] := ((A_mat[1, 1] * lambda_costate[idx_k + 1, 1]) + (A_mat[2, 1] * lambda_costate[idx_k + 1, 2]) + (A_mat[3, 1] * lambda_costate[idx_k + 1, 3]) + (A_mat[4, 1] * lambda_costate[idx_k + 1, 4]) + (A_mat[5, 1] * lambda_costate[idx_k + 1, 5]) + (A_mat[6, 1] * lambda_costate[idx_k + 1, 6])) + (Q_diag[1] * (x_traj[idx_k, 1] - x_ref[1]));
    lambda_costate[idx_k, 2] := ((A_mat[1, 2] * lambda_costate[idx_k + 1, 1]) + (A_mat[2, 2] * lambda_costate[idx_k + 1, 2]) + (A_mat[3, 2] * lambda_costate[idx_k + 1, 3]) + (A_mat[4, 2] * lambda_costate[idx_k + 1, 4]) + (A_mat[5, 2] * lambda_costate[idx_k + 1, 5]) + (A_mat[6, 2] * lambda_costate[idx_k + 1, 6])) + (Q_diag[2] * (x_traj[idx_k, 2] - x_ref[2]));
    lambda_costate[idx_k, 3] := ((A_mat[1, 3] * lambda_costate[idx_k + 1, 1]) + (A_mat[2, 3] * lambda_costate[idx_k + 1, 2]) + (A_mat[3, 3] * lambda_costate[idx_k + 1, 3]) + (A_mat[4, 3] * lambda_costate[idx_k + 1, 4]) + (A_mat[5, 3] * lambda_costate[idx_k + 1, 5]) + (A_mat[6, 3] * lambda_costate[idx_k + 1, 6])) + (Q_diag[3] * (x_traj[idx_k, 3] - x_ref[3]));
    lambda_costate[idx_k, 4] := ((A_mat[1, 4] * lambda_costate[idx_k + 1, 1]) + (A_mat[2, 4] * lambda_costate[idx_k + 1, 2]) + (A_mat[3, 4] * lambda_costate[idx_k + 1, 3]) + (A_mat[4, 4] * lambda_costate[idx_k + 1, 4]) + (A_mat[5, 4] * lambda_costate[idx_k + 1, 5]) + (A_mat[6, 4] * lambda_costate[idx_k + 1, 6])) + (Q_diag[4] * (x_traj[idx_k, 4] - x_ref[4]));
    lambda_costate[idx_k, 5] := ((A_mat[1, 5] * lambda_costate[idx_k + 1, 1]) + (A_mat[2, 5] * lambda_costate[idx_k + 1, 2]) + (A_mat[3, 5] * lambda_costate[idx_k + 1, 3]) + (A_mat[4, 5] * lambda_costate[idx_k + 1, 4]) + (A_mat[5, 5] * lambda_costate[idx_k + 1, 5]) + (A_mat[6, 5] * lambda_costate[idx_k + 1, 6])) + (Q_diag[5] * (x_traj[idx_k, 5] - x_ref[5]));
    lambda_costate[idx_k, 6] := ((A_mat[1, 6] * lambda_costate[idx_k + 1, 1]) + (A_mat[2, 6] * lambda_costate[idx_k + 1, 2]) + (A_mat[3, 6] * lambda_costate[idx_k + 1, 3]) + (A_mat[4, 6] * lambda_costate[idx_k + 1, 4]) + (A_mat[5, 6] * lambda_costate[idx_k + 1, 5]) + (A_mat[6, 6] * lambda_costate[idx_k + 1, 6])) + (Q_diag[6] * (x_traj[idx_k, 6] - x_ref[6]));
END_FOR;

(* Step 7.D: Control Gradient Computation & Projected Descent Step over Horizon k = 0 to 4 *)
FOR idx_k := 0 TO 4 DO
    (* Gradient Evaluation Control 1 *)
    IF idx_k = 0 THEN
        grad_u[0, 1] := ((B_mat[1, 1] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 1] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 1] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 1] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 1] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 1] * lambda_costate[idx_k + 1, 6])) + (R_diag[1] * u_traj[0, 1]) + (S_diag[1] * (u_traj[0, 1] - u_prev[1]));
    ELSE
        grad_u[idx_k, 1] := ((B_mat[1, 1] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 1] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 1] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 1] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 1] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 1] * lambda_costate[idx_k + 1, 6])) + (R_diag[1] * u_traj[idx_k, 1]) + (S_diag[1] * (u_traj[idx_k, 1] - u_traj[idx_k - 1, 1]));
    END_IF;
    
    (* Descent Step *)
    u_traj[idx_k, 1] := u_traj[idx_k, 1] - (r_PGD_StepSize_Alpha * grad_u[idx_k, 1]);
    
    (* Box Constraint Projection *)
    IF u_traj[idx_k, 1] < u_min[1] THEN
        u_traj[idx_k, 1] := u_min[1];
    ELSIF u_traj[idx_k, 1] > u_max[1] THEN
        u_traj[idx_k, 1] := u_max[1];
    END_IF;
    
    (* Dynamic Slew Rate Projection *)
    IF idx_k = 0 THEN
        r_TmpDeltaU := u_traj[0, 1] - u_prev[1];
        IF r_TmpDeltaU > delta_u_max[1] THEN
            u_traj[0, 1] := u_prev[1] + delta_u_max[1];
        ELSIF r_TmpDeltaU < -delta_u_max[1] THEN
            u_traj[0, 1] := u_prev[1] - delta_u_max[1];
        END_IF;
    ELSE
        r_TmpDeltaU := u_traj[idx_k, 1] - u_traj[idx_k - 1, 1];
        IF r_TmpDeltaU > delta_u_max[1] THEN
            u_traj[idx_k, 1] := u_traj[idx_k - 1, 1] + delta_u_max[1];
        ELSIF r_TmpDeltaU < -delta_u_max[1] THEN
            u_traj[idx_k, 1] := u_traj[idx_k - 1, 1] - delta_u_max[1];
        END_IF;
    END_IF;
    (* Gradient Evaluation Control 2 *)
    IF idx_k = 0 THEN
        grad_u[0, 2] := ((B_mat[1, 2] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 2] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 2] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 2] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 2] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 2] * lambda_costate[idx_k + 1, 6])) + (R_diag[2] * u_traj[0, 2]) + (S_diag[2] * (u_traj[0, 2] - u_prev[2]));
    ELSE
        grad_u[idx_k, 2] := ((B_mat[1, 2] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 2] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 2] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 2] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 2] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 2] * lambda_costate[idx_k + 1, 6])) + (R_diag[2] * u_traj[idx_k, 2]) + (S_diag[2] * (u_traj[idx_k, 2] - u_traj[idx_k - 1, 2]));
    END_IF;
    
    (* Descent Step *)
    u_traj[idx_k, 2] := u_traj[idx_k, 2] - (r_PGD_StepSize_Alpha * grad_u[idx_k, 2]);
    
    (* Box Constraint Projection *)
    IF u_traj[idx_k, 2] < u_min[2] THEN
        u_traj[idx_k, 2] := u_min[2];
    ELSIF u_traj[idx_k, 2] > u_max[2] THEN
        u_traj[idx_k, 2] := u_max[2];
    END_IF;
    
    (* Dynamic Slew Rate Projection *)
    IF idx_k = 0 THEN
        r_TmpDeltaU := u_traj[0, 2] - u_prev[2];
        IF r_TmpDeltaU > delta_u_max[2] THEN
            u_traj[0, 2] := u_prev[2] + delta_u_max[2];
        ELSIF r_TmpDeltaU < -delta_u_max[2] THEN
            u_traj[0, 2] := u_prev[2] - delta_u_max[2];
        END_IF;
    ELSE
        r_TmpDeltaU := u_traj[idx_k, 2] - u_traj[idx_k - 1, 2];
        IF r_TmpDeltaU > delta_u_max[2] THEN
            u_traj[idx_k, 2] := u_traj[idx_k - 1, 2] + delta_u_max[2];
        ELSIF r_TmpDeltaU < -delta_u_max[2] THEN
            u_traj[idx_k, 2] := u_traj[idx_k - 1, 2] - delta_u_max[2];
        END_IF;
    END_IF;
    (* Gradient Evaluation Control 3 *)
    IF idx_k = 0 THEN
        grad_u[0, 3] := ((B_mat[1, 3] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 3] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 3] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 3] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 3] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 3] * lambda_costate[idx_k + 1, 6])) + (R_diag[3] * u_traj[0, 3]) + (S_diag[3] * (u_traj[0, 3] - u_prev[3]));
    ELSE
        grad_u[idx_k, 3] := ((B_mat[1, 3] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 3] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 3] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 3] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 3] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 3] * lambda_costate[idx_k + 1, 6])) + (R_diag[3] * u_traj[idx_k, 3]) + (S_diag[3] * (u_traj[idx_k, 3] - u_traj[idx_k - 1, 3]));
    END_IF;
    
    (* Descent Step *)
    u_traj[idx_k, 3] := u_traj[idx_k, 3] - (r_PGD_StepSize_Alpha * grad_u[idx_k, 3]);
    
    (* Box Constraint Projection *)
    IF u_traj[idx_k, 3] < u_min[3] THEN
        u_traj[idx_k, 3] := u_min[3];
    ELSIF u_traj[idx_k, 3] > u_max[3] THEN
        u_traj[idx_k, 3] := u_max[3];
    END_IF;
    
    (* Dynamic Slew Rate Projection *)
    IF idx_k = 0 THEN
        r_TmpDeltaU := u_traj[0, 3] - u_prev[3];
        IF r_TmpDeltaU > delta_u_max[3] THEN
            u_traj[0, 3] := u_prev[3] + delta_u_max[3];
        ELSIF r_TmpDeltaU < -delta_u_max[3] THEN
            u_traj[0, 3] := u_prev[3] - delta_u_max[3];
        END_IF;
    ELSE
        r_TmpDeltaU := u_traj[idx_k, 3] - u_traj[idx_k - 1, 3];
        IF r_TmpDeltaU > delta_u_max[3] THEN
            u_traj[idx_k, 3] := u_traj[idx_k - 1, 3] + delta_u_max[3];
        ELSIF r_TmpDeltaU < -delta_u_max[3] THEN
            u_traj[idx_k, 3] := u_traj[idx_k - 1, 3] - delta_u_max[3];
        END_IF;
    END_IF;
    (* Gradient Evaluation Control 4 *)
    IF idx_k = 0 THEN
        grad_u[0, 4] := ((B_mat[1, 4] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 4] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 4] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 4] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 4] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 4] * lambda_costate[idx_k + 1, 6])) + (R_diag[4] * u_traj[0, 4]) + (S_diag[4] * (u_traj[0, 4] - u_prev[4]));
    ELSE
        grad_u[idx_k, 4] := ((B_mat[1, 4] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 4] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 4] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 4] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 4] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 4] * lambda_costate[idx_k + 1, 6])) + (R_diag[4] * u_traj[idx_k, 4]) + (S_diag[4] * (u_traj[idx_k, 4] - u_traj[idx_k - 1, 4]));
    END_IF;
    
    (* Descent Step *)
    u_traj[idx_k, 4] := u_traj[idx_k, 4] - (r_PGD_StepSize_Alpha * grad_u[idx_k, 4]);
    
    (* Box Constraint Projection *)
    IF u_traj[idx_k, 4] < u_min[4] THEN
        u_traj[idx_k, 4] := u_min[4];
    ELSIF u_traj[idx_k, 4] > u_max[4] THEN
        u_traj[idx_k, 4] := u_max[4];
    END_IF;
    
    (* Dynamic Slew Rate Projection *)
    IF idx_k = 0 THEN
        r_TmpDeltaU := u_traj[0, 4] - u_prev[4];
        IF r_TmpDeltaU > delta_u_max[4] THEN
            u_traj[0, 4] := u_prev[4] + delta_u_max[4];
        ELSIF r_TmpDeltaU < -delta_u_max[4] THEN
            u_traj[0, 4] := u_prev[4] - delta_u_max[4];
        END_IF;
    ELSE
        r_TmpDeltaU := u_traj[idx_k, 4] - u_traj[idx_k - 1, 4];
        IF r_TmpDeltaU > delta_u_max[4] THEN
            u_traj[idx_k, 4] := u_traj[idx_k - 1, 4] + delta_u_max[4];
        ELSIF r_TmpDeltaU < -delta_u_max[4] THEN
            u_traj[idx_k, 4] := u_traj[idx_k - 1, 4] - delta_u_max[4];
        END_IF;
    END_IF;
    (* Gradient Evaluation Control 5 *)
    IF idx_k = 0 THEN
        grad_u[0, 5] := ((B_mat[1, 5] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 5] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 5] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 5] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 5] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 5] * lambda_costate[idx_k + 1, 6])) + (R_diag[5] * u_traj[0, 5]) + (S_diag[5] * (u_traj[0, 5] - u_prev[5]));
    ELSE
        grad_u[idx_k, 5] := ((B_mat[1, 5] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 5] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 5] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 5] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 5] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 5] * lambda_costate[idx_k + 1, 6])) + (R_diag[5] * u_traj[idx_k, 5]) + (S_diag[5] * (u_traj[idx_k, 5] - u_traj[idx_k - 1, 5]));
    END_IF;
    
    (* Descent Step *)
    u_traj[idx_k, 5] := u_traj[idx_k, 5] - (r_PGD_StepSize_Alpha * grad_u[idx_k, 5]);
    
    (* Box Constraint Projection *)
    IF u_traj[idx_k, 5] < u_min[5] THEN
        u_traj[idx_k, 5] := u_min[5];
    ELSIF u_traj[idx_k, 5] > u_max[5] THEN
        u_traj[idx_k, 5] := u_max[5];
    END_IF;
    
    (* Dynamic Slew Rate Projection *)
    IF idx_k = 0 THEN
        r_TmpDeltaU := u_traj[0, 5] - u_prev[5];
        IF r_TmpDeltaU > delta_u_max[5] THEN
            u_traj[0, 5] := u_prev[5] + delta_u_max[5];
        ELSIF r_TmpDeltaU < -delta_u_max[5] THEN
            u_traj[0, 5] := u_prev[5] - delta_u_max[5];
        END_IF;
    ELSE
        r_TmpDeltaU := u_traj[idx_k, 5] - u_traj[idx_k - 1, 5];
        IF r_TmpDeltaU > delta_u_max[5] THEN
            u_traj[idx_k, 5] := u_traj[idx_k - 1, 5] + delta_u_max[5];
        ELSIF r_TmpDeltaU < -delta_u_max[5] THEN
            u_traj[idx_k, 5] := u_traj[idx_k - 1, 5] - delta_u_max[5];
        END_IF;
    END_IF;
END_FOR;

(* ============================================================================================== *)
(* PGD UNROLLED ITERATION 8 OF 10                                                               *)
(* ============================================================================================== *)
(* Step 8.A: Forward State Simulation over Horizon k = 0 to 4 *)
FOR idx_k := 0 TO 4 DO
    x_traj[idx_k + 1, 1] := ((A_mat[1, 1] * x_traj[idx_k, 1]) + (A_mat[1, 2] * x_traj[idx_k, 2]) + (A_mat[1, 3] * x_traj[idx_k, 3]) + (A_mat[1, 4] * x_traj[idx_k, 4]) + (A_mat[1, 5] * x_traj[idx_k, 5]) + (A_mat[1, 6] * x_traj[idx_k, 6])) + ((B_mat[1, 1] * u_traj[idx_k, 1]) + (B_mat[1, 2] * u_traj[idx_k, 2]) + (B_mat[1, 3] * u_traj[idx_k, 3]) + (B_mat[1, 4] * u_traj[idx_k, 4]) + (B_mat[1, 5] * u_traj[idx_k, 5]));
    x_traj[idx_k + 1, 2] := ((A_mat[2, 1] * x_traj[idx_k, 1]) + (A_mat[2, 2] * x_traj[idx_k, 2]) + (A_mat[2, 3] * x_traj[idx_k, 3]) + (A_mat[2, 4] * x_traj[idx_k, 4]) + (A_mat[2, 5] * x_traj[idx_k, 5]) + (A_mat[2, 6] * x_traj[idx_k, 6])) + ((B_mat[2, 1] * u_traj[idx_k, 1]) + (B_mat[2, 2] * u_traj[idx_k, 2]) + (B_mat[2, 3] * u_traj[idx_k, 3]) + (B_mat[2, 4] * u_traj[idx_k, 4]) + (B_mat[2, 5] * u_traj[idx_k, 5]));
    x_traj[idx_k + 1, 3] := ((A_mat[3, 1] * x_traj[idx_k, 1]) + (A_mat[3, 2] * x_traj[idx_k, 2]) + (A_mat[3, 3] * x_traj[idx_k, 3]) + (A_mat[3, 4] * x_traj[idx_k, 4]) + (A_mat[3, 5] * x_traj[idx_k, 5]) + (A_mat[3, 6] * x_traj[idx_k, 6])) + ((B_mat[3, 1] * u_traj[idx_k, 1]) + (B_mat[3, 2] * u_traj[idx_k, 2]) + (B_mat[3, 3] * u_traj[idx_k, 3]) + (B_mat[3, 4] * u_traj[idx_k, 4]) + (B_mat[3, 5] * u_traj[idx_k, 5]));
    x_traj[idx_k + 1, 4] := ((A_mat[4, 1] * x_traj[idx_k, 1]) + (A_mat[4, 2] * x_traj[idx_k, 2]) + (A_mat[4, 3] * x_traj[idx_k, 3]) + (A_mat[4, 4] * x_traj[idx_k, 4]) + (A_mat[4, 5] * x_traj[idx_k, 5]) + (A_mat[4, 6] * x_traj[idx_k, 6])) + ((B_mat[4, 1] * u_traj[idx_k, 1]) + (B_mat[4, 2] * u_traj[idx_k, 2]) + (B_mat[4, 3] * u_traj[idx_k, 3]) + (B_mat[4, 4] * u_traj[idx_k, 4]) + (B_mat[4, 5] * u_traj[idx_k, 5]));
    x_traj[idx_k + 1, 5] := ((A_mat[5, 1] * x_traj[idx_k, 1]) + (A_mat[5, 2] * x_traj[idx_k, 2]) + (A_mat[5, 3] * x_traj[idx_k, 3]) + (A_mat[5, 4] * x_traj[idx_k, 4]) + (A_mat[5, 5] * x_traj[idx_k, 5]) + (A_mat[5, 6] * x_traj[idx_k, 6])) + ((B_mat[5, 1] * u_traj[idx_k, 1]) + (B_mat[5, 2] * u_traj[idx_k, 2]) + (B_mat[5, 3] * u_traj[idx_k, 3]) + (B_mat[5, 4] * u_traj[idx_k, 4]) + (B_mat[5, 5] * u_traj[idx_k, 5]));
    x_traj[idx_k + 1, 6] := ((A_mat[6, 1] * x_traj[idx_k, 1]) + (A_mat[6, 2] * x_traj[idx_k, 2]) + (A_mat[6, 3] * x_traj[idx_k, 3]) + (A_mat[6, 4] * x_traj[idx_k, 4]) + (A_mat[6, 5] * x_traj[idx_k, 5]) + (A_mat[6, 6] * x_traj[idx_k, 6])) + ((B_mat[6, 1] * u_traj[idx_k, 1]) + (B_mat[6, 2] * u_traj[idx_k, 2]) + (B_mat[6, 3] * u_traj[idx_k, 3]) + (B_mat[6, 4] * u_traj[idx_k, 4]) + (B_mat[6, 5] * u_traj[idx_k, 5]));
END_FOR;

(* Step 8.B: Terminal Horizon Adjoint Costate Evaluation (k = 5) *)
lambda_costate[5, 1] := P_term[1] * (x_traj[5, 1] - x_ref[1]);
lambda_costate[5, 2] := P_term[2] * (x_traj[5, 2] - x_ref[2]);
lambda_costate[5, 3] := P_term[3] * (x_traj[5, 3] - x_ref[3]);
lambda_costate[5, 4] := P_term[4] * (x_traj[5, 4] - x_ref[4]);
lambda_costate[5, 5] := P_term[5] * (x_traj[5, 5] - x_ref[5]);
lambda_costate[5, 6] := P_term[6] * (x_traj[5, 6] - x_ref[6]);

(* Step 8.C: Backward Adjoint Costate Propagation over Horizon k = 4 downto 0 *)
FOR idx_k := 4 TO 0 BY -1 DO
    lambda_costate[idx_k, 1] := ((A_mat[1, 1] * lambda_costate[idx_k + 1, 1]) + (A_mat[2, 1] * lambda_costate[idx_k + 1, 2]) + (A_mat[3, 1] * lambda_costate[idx_k + 1, 3]) + (A_mat[4, 1] * lambda_costate[idx_k + 1, 4]) + (A_mat[5, 1] * lambda_costate[idx_k + 1, 5]) + (A_mat[6, 1] * lambda_costate[idx_k + 1, 6])) + (Q_diag[1] * (x_traj[idx_k, 1] - x_ref[1]));
    lambda_costate[idx_k, 2] := ((A_mat[1, 2] * lambda_costate[idx_k + 1, 1]) + (A_mat[2, 2] * lambda_costate[idx_k + 1, 2]) + (A_mat[3, 2] * lambda_costate[idx_k + 1, 3]) + (A_mat[4, 2] * lambda_costate[idx_k + 1, 4]) + (A_mat[5, 2] * lambda_costate[idx_k + 1, 5]) + (A_mat[6, 2] * lambda_costate[idx_k + 1, 6])) + (Q_diag[2] * (x_traj[idx_k, 2] - x_ref[2]));
    lambda_costate[idx_k, 3] := ((A_mat[1, 3] * lambda_costate[idx_k + 1, 1]) + (A_mat[2, 3] * lambda_costate[idx_k + 1, 2]) + (A_mat[3, 3] * lambda_costate[idx_k + 1, 3]) + (A_mat[4, 3] * lambda_costate[idx_k + 1, 4]) + (A_mat[5, 3] * lambda_costate[idx_k + 1, 5]) + (A_mat[6, 3] * lambda_costate[idx_k + 1, 6])) + (Q_diag[3] * (x_traj[idx_k, 3] - x_ref[3]));
    lambda_costate[idx_k, 4] := ((A_mat[1, 4] * lambda_costate[idx_k + 1, 1]) + (A_mat[2, 4] * lambda_costate[idx_k + 1, 2]) + (A_mat[3, 4] * lambda_costate[idx_k + 1, 3]) + (A_mat[4, 4] * lambda_costate[idx_k + 1, 4]) + (A_mat[5, 4] * lambda_costate[idx_k + 1, 5]) + (A_mat[6, 4] * lambda_costate[idx_k + 1, 6])) + (Q_diag[4] * (x_traj[idx_k, 4] - x_ref[4]));
    lambda_costate[idx_k, 5] := ((A_mat[1, 5] * lambda_costate[idx_k + 1, 1]) + (A_mat[2, 5] * lambda_costate[idx_k + 1, 2]) + (A_mat[3, 5] * lambda_costate[idx_k + 1, 3]) + (A_mat[4, 5] * lambda_costate[idx_k + 1, 4]) + (A_mat[5, 5] * lambda_costate[idx_k + 1, 5]) + (A_mat[6, 5] * lambda_costate[idx_k + 1, 6])) + (Q_diag[5] * (x_traj[idx_k, 5] - x_ref[5]));
    lambda_costate[idx_k, 6] := ((A_mat[1, 6] * lambda_costate[idx_k + 1, 1]) + (A_mat[2, 6] * lambda_costate[idx_k + 1, 2]) + (A_mat[3, 6] * lambda_costate[idx_k + 1, 3]) + (A_mat[4, 6] * lambda_costate[idx_k + 1, 4]) + (A_mat[5, 6] * lambda_costate[idx_k + 1, 5]) + (A_mat[6, 6] * lambda_costate[idx_k + 1, 6])) + (Q_diag[6] * (x_traj[idx_k, 6] - x_ref[6]));
END_FOR;

(* Step 8.D: Control Gradient Computation & Projected Descent Step over Horizon k = 0 to 4 *)
FOR idx_k := 0 TO 4 DO
    (* Gradient Evaluation Control 1 *)
    IF idx_k = 0 THEN
        grad_u[0, 1] := ((B_mat[1, 1] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 1] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 1] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 1] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 1] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 1] * lambda_costate[idx_k + 1, 6])) + (R_diag[1] * u_traj[0, 1]) + (S_diag[1] * (u_traj[0, 1] - u_prev[1]));
    ELSE
        grad_u[idx_k, 1] := ((B_mat[1, 1] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 1] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 1] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 1] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 1] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 1] * lambda_costate[idx_k + 1, 6])) + (R_diag[1] * u_traj[idx_k, 1]) + (S_diag[1] * (u_traj[idx_k, 1] - u_traj[idx_k - 1, 1]));
    END_IF;
    
    (* Descent Step *)
    u_traj[idx_k, 1] := u_traj[idx_k, 1] - (r_PGD_StepSize_Alpha * grad_u[idx_k, 1]);
    
    (* Box Constraint Projection *)
    IF u_traj[idx_k, 1] < u_min[1] THEN
        u_traj[idx_k, 1] := u_min[1];
    ELSIF u_traj[idx_k, 1] > u_max[1] THEN
        u_traj[idx_k, 1] := u_max[1];
    END_IF;
    
    (* Dynamic Slew Rate Projection *)
    IF idx_k = 0 THEN
        r_TmpDeltaU := u_traj[0, 1] - u_prev[1];
        IF r_TmpDeltaU > delta_u_max[1] THEN
            u_traj[0, 1] := u_prev[1] + delta_u_max[1];
        ELSIF r_TmpDeltaU < -delta_u_max[1] THEN
            u_traj[0, 1] := u_prev[1] - delta_u_max[1];
        END_IF;
    ELSE
        r_TmpDeltaU := u_traj[idx_k, 1] - u_traj[idx_k - 1, 1];
        IF r_TmpDeltaU > delta_u_max[1] THEN
            u_traj[idx_k, 1] := u_traj[idx_k - 1, 1] + delta_u_max[1];
        ELSIF r_TmpDeltaU < -delta_u_max[1] THEN
            u_traj[idx_k, 1] := u_traj[idx_k - 1, 1] - delta_u_max[1];
        END_IF;
    END_IF;
    (* Gradient Evaluation Control 2 *)
    IF idx_k = 0 THEN
        grad_u[0, 2] := ((B_mat[1, 2] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 2] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 2] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 2] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 2] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 2] * lambda_costate[idx_k + 1, 6])) + (R_diag[2] * u_traj[0, 2]) + (S_diag[2] * (u_traj[0, 2] - u_prev[2]));
    ELSE
        grad_u[idx_k, 2] := ((B_mat[1, 2] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 2] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 2] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 2] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 2] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 2] * lambda_costate[idx_k + 1, 6])) + (R_diag[2] * u_traj[idx_k, 2]) + (S_diag[2] * (u_traj[idx_k, 2] - u_traj[idx_k - 1, 2]));
    END_IF;
    
    (* Descent Step *)
    u_traj[idx_k, 2] := u_traj[idx_k, 2] - (r_PGD_StepSize_Alpha * grad_u[idx_k, 2]);
    
    (* Box Constraint Projection *)
    IF u_traj[idx_k, 2] < u_min[2] THEN
        u_traj[idx_k, 2] := u_min[2];
    ELSIF u_traj[idx_k, 2] > u_max[2] THEN
        u_traj[idx_k, 2] := u_max[2];
    END_IF;
    
    (* Dynamic Slew Rate Projection *)
    IF idx_k = 0 THEN
        r_TmpDeltaU := u_traj[0, 2] - u_prev[2];
        IF r_TmpDeltaU > delta_u_max[2] THEN
            u_traj[0, 2] := u_prev[2] + delta_u_max[2];
        ELSIF r_TmpDeltaU < -delta_u_max[2] THEN
            u_traj[0, 2] := u_prev[2] - delta_u_max[2];
        END_IF;
    ELSE
        r_TmpDeltaU := u_traj[idx_k, 2] - u_traj[idx_k - 1, 2];
        IF r_TmpDeltaU > delta_u_max[2] THEN
            u_traj[idx_k, 2] := u_traj[idx_k - 1, 2] + delta_u_max[2];
        ELSIF r_TmpDeltaU < -delta_u_max[2] THEN
            u_traj[idx_k, 2] := u_traj[idx_k - 1, 2] - delta_u_max[2];
        END_IF;
    END_IF;
    (* Gradient Evaluation Control 3 *)
    IF idx_k = 0 THEN
        grad_u[0, 3] := ((B_mat[1, 3] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 3] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 3] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 3] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 3] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 3] * lambda_costate[idx_k + 1, 6])) + (R_diag[3] * u_traj[0, 3]) + (S_diag[3] * (u_traj[0, 3] - u_prev[3]));
    ELSE
        grad_u[idx_k, 3] := ((B_mat[1, 3] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 3] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 3] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 3] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 3] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 3] * lambda_costate[idx_k + 1, 6])) + (R_diag[3] * u_traj[idx_k, 3]) + (S_diag[3] * (u_traj[idx_k, 3] - u_traj[idx_k - 1, 3]));
    END_IF;
    
    (* Descent Step *)
    u_traj[idx_k, 3] := u_traj[idx_k, 3] - (r_PGD_StepSize_Alpha * grad_u[idx_k, 3]);
    
    (* Box Constraint Projection *)
    IF u_traj[idx_k, 3] < u_min[3] THEN
        u_traj[idx_k, 3] := u_min[3];
    ELSIF u_traj[idx_k, 3] > u_max[3] THEN
        u_traj[idx_k, 3] := u_max[3];
    END_IF;
    
    (* Dynamic Slew Rate Projection *)
    IF idx_k = 0 THEN
        r_TmpDeltaU := u_traj[0, 3] - u_prev[3];
        IF r_TmpDeltaU > delta_u_max[3] THEN
            u_traj[0, 3] := u_prev[3] + delta_u_max[3];
        ELSIF r_TmpDeltaU < -delta_u_max[3] THEN
            u_traj[0, 3] := u_prev[3] - delta_u_max[3];
        END_IF;
    ELSE
        r_TmpDeltaU := u_traj[idx_k, 3] - u_traj[idx_k - 1, 3];
        IF r_TmpDeltaU > delta_u_max[3] THEN
            u_traj[idx_k, 3] := u_traj[idx_k - 1, 3] + delta_u_max[3];
        ELSIF r_TmpDeltaU < -delta_u_max[3] THEN
            u_traj[idx_k, 3] := u_traj[idx_k - 1, 3] - delta_u_max[3];
        END_IF;
    END_IF;
    (* Gradient Evaluation Control 4 *)
    IF idx_k = 0 THEN
        grad_u[0, 4] := ((B_mat[1, 4] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 4] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 4] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 4] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 4] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 4] * lambda_costate[idx_k + 1, 6])) + (R_diag[4] * u_traj[0, 4]) + (S_diag[4] * (u_traj[0, 4] - u_prev[4]));
    ELSE
        grad_u[idx_k, 4] := ((B_mat[1, 4] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 4] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 4] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 4] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 4] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 4] * lambda_costate[idx_k + 1, 6])) + (R_diag[4] * u_traj[idx_k, 4]) + (S_diag[4] * (u_traj[idx_k, 4] - u_traj[idx_k - 1, 4]));
    END_IF;
    
    (* Descent Step *)
    u_traj[idx_k, 4] := u_traj[idx_k, 4] - (r_PGD_StepSize_Alpha * grad_u[idx_k, 4]);
    
    (* Box Constraint Projection *)
    IF u_traj[idx_k, 4] < u_min[4] THEN
        u_traj[idx_k, 4] := u_min[4];
    ELSIF u_traj[idx_k, 4] > u_max[4] THEN
        u_traj[idx_k, 4] := u_max[4];
    END_IF;
    
    (* Dynamic Slew Rate Projection *)
    IF idx_k = 0 THEN
        r_TmpDeltaU := u_traj[0, 4] - u_prev[4];
        IF r_TmpDeltaU > delta_u_max[4] THEN
            u_traj[0, 4] := u_prev[4] + delta_u_max[4];
        ELSIF r_TmpDeltaU < -delta_u_max[4] THEN
            u_traj[0, 4] := u_prev[4] - delta_u_max[4];
        END_IF;
    ELSE
        r_TmpDeltaU := u_traj[idx_k, 4] - u_traj[idx_k - 1, 4];
        IF r_TmpDeltaU > delta_u_max[4] THEN
            u_traj[idx_k, 4] := u_traj[idx_k - 1, 4] + delta_u_max[4];
        ELSIF r_TmpDeltaU < -delta_u_max[4] THEN
            u_traj[idx_k, 4] := u_traj[idx_k - 1, 4] - delta_u_max[4];
        END_IF;
    END_IF;
    (* Gradient Evaluation Control 5 *)
    IF idx_k = 0 THEN
        grad_u[0, 5] := ((B_mat[1, 5] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 5] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 5] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 5] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 5] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 5] * lambda_costate[idx_k + 1, 6])) + (R_diag[5] * u_traj[0, 5]) + (S_diag[5] * (u_traj[0, 5] - u_prev[5]));
    ELSE
        grad_u[idx_k, 5] := ((B_mat[1, 5] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 5] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 5] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 5] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 5] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 5] * lambda_costate[idx_k + 1, 6])) + (R_diag[5] * u_traj[idx_k, 5]) + (S_diag[5] * (u_traj[idx_k, 5] - u_traj[idx_k - 1, 5]));
    END_IF;
    
    (* Descent Step *)
    u_traj[idx_k, 5] := u_traj[idx_k, 5] - (r_PGD_StepSize_Alpha * grad_u[idx_k, 5]);
    
    (* Box Constraint Projection *)
    IF u_traj[idx_k, 5] < u_min[5] THEN
        u_traj[idx_k, 5] := u_min[5];
    ELSIF u_traj[idx_k, 5] > u_max[5] THEN
        u_traj[idx_k, 5] := u_max[5];
    END_IF;
    
    (* Dynamic Slew Rate Projection *)
    IF idx_k = 0 THEN
        r_TmpDeltaU := u_traj[0, 5] - u_prev[5];
        IF r_TmpDeltaU > delta_u_max[5] THEN
            u_traj[0, 5] := u_prev[5] + delta_u_max[5];
        ELSIF r_TmpDeltaU < -delta_u_max[5] THEN
            u_traj[0, 5] := u_prev[5] - delta_u_max[5];
        END_IF;
    ELSE
        r_TmpDeltaU := u_traj[idx_k, 5] - u_traj[idx_k - 1, 5];
        IF r_TmpDeltaU > delta_u_max[5] THEN
            u_traj[idx_k, 5] := u_traj[idx_k - 1, 5] + delta_u_max[5];
        ELSIF r_TmpDeltaU < -delta_u_max[5] THEN
            u_traj[idx_k, 5] := u_traj[idx_k - 1, 5] - delta_u_max[5];
        END_IF;
    END_IF;
END_FOR;

(* ============================================================================================== *)
(* PGD UNROLLED ITERATION 9 OF 10                                                               *)
(* ============================================================================================== *)
(* Step 9.A: Forward State Simulation over Horizon k = 0 to 4 *)
FOR idx_k := 0 TO 4 DO
    x_traj[idx_k + 1, 1] := ((A_mat[1, 1] * x_traj[idx_k, 1]) + (A_mat[1, 2] * x_traj[idx_k, 2]) + (A_mat[1, 3] * x_traj[idx_k, 3]) + (A_mat[1, 4] * x_traj[idx_k, 4]) + (A_mat[1, 5] * x_traj[idx_k, 5]) + (A_mat[1, 6] * x_traj[idx_k, 6])) + ((B_mat[1, 1] * u_traj[idx_k, 1]) + (B_mat[1, 2] * u_traj[idx_k, 2]) + (B_mat[1, 3] * u_traj[idx_k, 3]) + (B_mat[1, 4] * u_traj[idx_k, 4]) + (B_mat[1, 5] * u_traj[idx_k, 5]));
    x_traj[idx_k + 1, 2] := ((A_mat[2, 1] * x_traj[idx_k, 1]) + (A_mat[2, 2] * x_traj[idx_k, 2]) + (A_mat[2, 3] * x_traj[idx_k, 3]) + (A_mat[2, 4] * x_traj[idx_k, 4]) + (A_mat[2, 5] * x_traj[idx_k, 5]) + (A_mat[2, 6] * x_traj[idx_k, 6])) + ((B_mat[2, 1] * u_traj[idx_k, 1]) + (B_mat[2, 2] * u_traj[idx_k, 2]) + (B_mat[2, 3] * u_traj[idx_k, 3]) + (B_mat[2, 4] * u_traj[idx_k, 4]) + (B_mat[2, 5] * u_traj[idx_k, 5]));
    x_traj[idx_k + 1, 3] := ((A_mat[3, 1] * x_traj[idx_k, 1]) + (A_mat[3, 2] * x_traj[idx_k, 2]) + (A_mat[3, 3] * x_traj[idx_k, 3]) + (A_mat[3, 4] * x_traj[idx_k, 4]) + (A_mat[3, 5] * x_traj[idx_k, 5]) + (A_mat[3, 6] * x_traj[idx_k, 6])) + ((B_mat[3, 1] * u_traj[idx_k, 1]) + (B_mat[3, 2] * u_traj[idx_k, 2]) + (B_mat[3, 3] * u_traj[idx_k, 3]) + (B_mat[3, 4] * u_traj[idx_k, 4]) + (B_mat[3, 5] * u_traj[idx_k, 5]));
    x_traj[idx_k + 1, 4] := ((A_mat[4, 1] * x_traj[idx_k, 1]) + (A_mat[4, 2] * x_traj[idx_k, 2]) + (A_mat[4, 3] * x_traj[idx_k, 3]) + (A_mat[4, 4] * x_traj[idx_k, 4]) + (A_mat[4, 5] * x_traj[idx_k, 5]) + (A_mat[4, 6] * x_traj[idx_k, 6])) + ((B_mat[4, 1] * u_traj[idx_k, 1]) + (B_mat[4, 2] * u_traj[idx_k, 2]) + (B_mat[4, 3] * u_traj[idx_k, 3]) + (B_mat[4, 4] * u_traj[idx_k, 4]) + (B_mat[4, 5] * u_traj[idx_k, 5]));
    x_traj[idx_k + 1, 5] := ((A_mat[5, 1] * x_traj[idx_k, 1]) + (A_mat[5, 2] * x_traj[idx_k, 2]) + (A_mat[5, 3] * x_traj[idx_k, 3]) + (A_mat[5, 4] * x_traj[idx_k, 4]) + (A_mat[5, 5] * x_traj[idx_k, 5]) + (A_mat[5, 6] * x_traj[idx_k, 6])) + ((B_mat[5, 1] * u_traj[idx_k, 1]) + (B_mat[5, 2] * u_traj[idx_k, 2]) + (B_mat[5, 3] * u_traj[idx_k, 3]) + (B_mat[5, 4] * u_traj[idx_k, 4]) + (B_mat[5, 5] * u_traj[idx_k, 5]));
    x_traj[idx_k + 1, 6] := ((A_mat[6, 1] * x_traj[idx_k, 1]) + (A_mat[6, 2] * x_traj[idx_k, 2]) + (A_mat[6, 3] * x_traj[idx_k, 3]) + (A_mat[6, 4] * x_traj[idx_k, 4]) + (A_mat[6, 5] * x_traj[idx_k, 5]) + (A_mat[6, 6] * x_traj[idx_k, 6])) + ((B_mat[6, 1] * u_traj[idx_k, 1]) + (B_mat[6, 2] * u_traj[idx_k, 2]) + (B_mat[6, 3] * u_traj[idx_k, 3]) + (B_mat[6, 4] * u_traj[idx_k, 4]) + (B_mat[6, 5] * u_traj[idx_k, 5]));
END_FOR;

(* Step 9.B: Terminal Horizon Adjoint Costate Evaluation (k = 5) *)
lambda_costate[5, 1] := P_term[1] * (x_traj[5, 1] - x_ref[1]);
lambda_costate[5, 2] := P_term[2] * (x_traj[5, 2] - x_ref[2]);
lambda_costate[5, 3] := P_term[3] * (x_traj[5, 3] - x_ref[3]);
lambda_costate[5, 4] := P_term[4] * (x_traj[5, 4] - x_ref[4]);
lambda_costate[5, 5] := P_term[5] * (x_traj[5, 5] - x_ref[5]);
lambda_costate[5, 6] := P_term[6] * (x_traj[5, 6] - x_ref[6]);

(* Step 9.C: Backward Adjoint Costate Propagation over Horizon k = 4 downto 0 *)
FOR idx_k := 4 TO 0 BY -1 DO
    lambda_costate[idx_k, 1] := ((A_mat[1, 1] * lambda_costate[idx_k + 1, 1]) + (A_mat[2, 1] * lambda_costate[idx_k + 1, 2]) + (A_mat[3, 1] * lambda_costate[idx_k + 1, 3]) + (A_mat[4, 1] * lambda_costate[idx_k + 1, 4]) + (A_mat[5, 1] * lambda_costate[idx_k + 1, 5]) + (A_mat[6, 1] * lambda_costate[idx_k + 1, 6])) + (Q_diag[1] * (x_traj[idx_k, 1] - x_ref[1]));
    lambda_costate[idx_k, 2] := ((A_mat[1, 2] * lambda_costate[idx_k + 1, 1]) + (A_mat[2, 2] * lambda_costate[idx_k + 1, 2]) + (A_mat[3, 2] * lambda_costate[idx_k + 1, 3]) + (A_mat[4, 2] * lambda_costate[idx_k + 1, 4]) + (A_mat[5, 2] * lambda_costate[idx_k + 1, 5]) + (A_mat[6, 2] * lambda_costate[idx_k + 1, 6])) + (Q_diag[2] * (x_traj[idx_k, 2] - x_ref[2]));
    lambda_costate[idx_k, 3] := ((A_mat[1, 3] * lambda_costate[idx_k + 1, 1]) + (A_mat[2, 3] * lambda_costate[idx_k + 1, 2]) + (A_mat[3, 3] * lambda_costate[idx_k + 1, 3]) + (A_mat[4, 3] * lambda_costate[idx_k + 1, 4]) + (A_mat[5, 3] * lambda_costate[idx_k + 1, 5]) + (A_mat[6, 3] * lambda_costate[idx_k + 1, 6])) + (Q_diag[3] * (x_traj[idx_k, 3] - x_ref[3]));
    lambda_costate[idx_k, 4] := ((A_mat[1, 4] * lambda_costate[idx_k + 1, 1]) + (A_mat[2, 4] * lambda_costate[idx_k + 1, 2]) + (A_mat[3, 4] * lambda_costate[idx_k + 1, 3]) + (A_mat[4, 4] * lambda_costate[idx_k + 1, 4]) + (A_mat[5, 4] * lambda_costate[idx_k + 1, 5]) + (A_mat[6, 4] * lambda_costate[idx_k + 1, 6])) + (Q_diag[4] * (x_traj[idx_k, 4] - x_ref[4]));
    lambda_costate[idx_k, 5] := ((A_mat[1, 5] * lambda_costate[idx_k + 1, 1]) + (A_mat[2, 5] * lambda_costate[idx_k + 1, 2]) + (A_mat[3, 5] * lambda_costate[idx_k + 1, 3]) + (A_mat[4, 5] * lambda_costate[idx_k + 1, 4]) + (A_mat[5, 5] * lambda_costate[idx_k + 1, 5]) + (A_mat[6, 5] * lambda_costate[idx_k + 1, 6])) + (Q_diag[5] * (x_traj[idx_k, 5] - x_ref[5]));
    lambda_costate[idx_k, 6] := ((A_mat[1, 6] * lambda_costate[idx_k + 1, 1]) + (A_mat[2, 6] * lambda_costate[idx_k + 1, 2]) + (A_mat[3, 6] * lambda_costate[idx_k + 1, 3]) + (A_mat[4, 6] * lambda_costate[idx_k + 1, 4]) + (A_mat[5, 6] * lambda_costate[idx_k + 1, 5]) + (A_mat[6, 6] * lambda_costate[idx_k + 1, 6])) + (Q_diag[6] * (x_traj[idx_k, 6] - x_ref[6]));
END_FOR;

(* Step 9.D: Control Gradient Computation & Projected Descent Step over Horizon k = 0 to 4 *)
FOR idx_k := 0 TO 4 DO
    (* Gradient Evaluation Control 1 *)
    IF idx_k = 0 THEN
        grad_u[0, 1] := ((B_mat[1, 1] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 1] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 1] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 1] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 1] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 1] * lambda_costate[idx_k + 1, 6])) + (R_diag[1] * u_traj[0, 1]) + (S_diag[1] * (u_traj[0, 1] - u_prev[1]));
    ELSE
        grad_u[idx_k, 1] := ((B_mat[1, 1] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 1] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 1] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 1] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 1] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 1] * lambda_costate[idx_k + 1, 6])) + (R_diag[1] * u_traj[idx_k, 1]) + (S_diag[1] * (u_traj[idx_k, 1] - u_traj[idx_k - 1, 1]));
    END_IF;
    
    (* Descent Step *)
    u_traj[idx_k, 1] := u_traj[idx_k, 1] - (r_PGD_StepSize_Alpha * grad_u[idx_k, 1]);
    
    (* Box Constraint Projection *)
    IF u_traj[idx_k, 1] < u_min[1] THEN
        u_traj[idx_k, 1] := u_min[1];
    ELSIF u_traj[idx_k, 1] > u_max[1] THEN
        u_traj[idx_k, 1] := u_max[1];
    END_IF;
    
    (* Dynamic Slew Rate Projection *)
    IF idx_k = 0 THEN
        r_TmpDeltaU := u_traj[0, 1] - u_prev[1];
        IF r_TmpDeltaU > delta_u_max[1] THEN
            u_traj[0, 1] := u_prev[1] + delta_u_max[1];
        ELSIF r_TmpDeltaU < -delta_u_max[1] THEN
            u_traj[0, 1] := u_prev[1] - delta_u_max[1];
        END_IF;
    ELSE
        r_TmpDeltaU := u_traj[idx_k, 1] - u_traj[idx_k - 1, 1];
        IF r_TmpDeltaU > delta_u_max[1] THEN
            u_traj[idx_k, 1] := u_traj[idx_k - 1, 1] + delta_u_max[1];
        ELSIF r_TmpDeltaU < -delta_u_max[1] THEN
            u_traj[idx_k, 1] := u_traj[idx_k - 1, 1] - delta_u_max[1];
        END_IF;
    END_IF;
    (* Gradient Evaluation Control 2 *)
    IF idx_k = 0 THEN
        grad_u[0, 2] := ((B_mat[1, 2] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 2] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 2] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 2] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 2] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 2] * lambda_costate[idx_k + 1, 6])) + (R_diag[2] * u_traj[0, 2]) + (S_diag[2] * (u_traj[0, 2] - u_prev[2]));
    ELSE
        grad_u[idx_k, 2] := ((B_mat[1, 2] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 2] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 2] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 2] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 2] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 2] * lambda_costate[idx_k + 1, 6])) + (R_diag[2] * u_traj[idx_k, 2]) + (S_diag[2] * (u_traj[idx_k, 2] - u_traj[idx_k - 1, 2]));
    END_IF;
    
    (* Descent Step *)
    u_traj[idx_k, 2] := u_traj[idx_k, 2] - (r_PGD_StepSize_Alpha * grad_u[idx_k, 2]);
    
    (* Box Constraint Projection *)
    IF u_traj[idx_k, 2] < u_min[2] THEN
        u_traj[idx_k, 2] := u_min[2];
    ELSIF u_traj[idx_k, 2] > u_max[2] THEN
        u_traj[idx_k, 2] := u_max[2];
    END_IF;
    
    (* Dynamic Slew Rate Projection *)
    IF idx_k = 0 THEN
        r_TmpDeltaU := u_traj[0, 2] - u_prev[2];
        IF r_TmpDeltaU > delta_u_max[2] THEN
            u_traj[0, 2] := u_prev[2] + delta_u_max[2];
        ELSIF r_TmpDeltaU < -delta_u_max[2] THEN
            u_traj[0, 2] := u_prev[2] - delta_u_max[2];
        END_IF;
    ELSE
        r_TmpDeltaU := u_traj[idx_k, 2] - u_traj[idx_k - 1, 2];
        IF r_TmpDeltaU > delta_u_max[2] THEN
            u_traj[idx_k, 2] := u_traj[idx_k - 1, 2] + delta_u_max[2];
        ELSIF r_TmpDeltaU < -delta_u_max[2] THEN
            u_traj[idx_k, 2] := u_traj[idx_k - 1, 2] - delta_u_max[2];
        END_IF;
    END_IF;
    (* Gradient Evaluation Control 3 *)
    IF idx_k = 0 THEN
        grad_u[0, 3] := ((B_mat[1, 3] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 3] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 3] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 3] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 3] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 3] * lambda_costate[idx_k + 1, 6])) + (R_diag[3] * u_traj[0, 3]) + (S_diag[3] * (u_traj[0, 3] - u_prev[3]));
    ELSE
        grad_u[idx_k, 3] := ((B_mat[1, 3] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 3] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 3] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 3] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 3] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 3] * lambda_costate[idx_k + 1, 6])) + (R_diag[3] * u_traj[idx_k, 3]) + (S_diag[3] * (u_traj[idx_k, 3] - u_traj[idx_k - 1, 3]));
    END_IF;
    
    (* Descent Step *)
    u_traj[idx_k, 3] := u_traj[idx_k, 3] - (r_PGD_StepSize_Alpha * grad_u[idx_k, 3]);
    
    (* Box Constraint Projection *)
    IF u_traj[idx_k, 3] < u_min[3] THEN
        u_traj[idx_k, 3] := u_min[3];
    ELSIF u_traj[idx_k, 3] > u_max[3] THEN
        u_traj[idx_k, 3] := u_max[3];
    END_IF;
    
    (* Dynamic Slew Rate Projection *)
    IF idx_k = 0 THEN
        r_TmpDeltaU := u_traj[0, 3] - u_prev[3];
        IF r_TmpDeltaU > delta_u_max[3] THEN
            u_traj[0, 3] := u_prev[3] + delta_u_max[3];
        ELSIF r_TmpDeltaU < -delta_u_max[3] THEN
            u_traj[0, 3] := u_prev[3] - delta_u_max[3];
        END_IF;
    ELSE
        r_TmpDeltaU := u_traj[idx_k, 3] - u_traj[idx_k - 1, 3];
        IF r_TmpDeltaU > delta_u_max[3] THEN
            u_traj[idx_k, 3] := u_traj[idx_k - 1, 3] + delta_u_max[3];
        ELSIF r_TmpDeltaU < -delta_u_max[3] THEN
            u_traj[idx_k, 3] := u_traj[idx_k - 1, 3] - delta_u_max[3];
        END_IF;
    END_IF;
    (* Gradient Evaluation Control 4 *)
    IF idx_k = 0 THEN
        grad_u[0, 4] := ((B_mat[1, 4] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 4] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 4] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 4] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 4] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 4] * lambda_costate[idx_k + 1, 6])) + (R_diag[4] * u_traj[0, 4]) + (S_diag[4] * (u_traj[0, 4] - u_prev[4]));
    ELSE
        grad_u[idx_k, 4] := ((B_mat[1, 4] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 4] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 4] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 4] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 4] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 4] * lambda_costate[idx_k + 1, 6])) + (R_diag[4] * u_traj[idx_k, 4]) + (S_diag[4] * (u_traj[idx_k, 4] - u_traj[idx_k - 1, 4]));
    END_IF;
    
    (* Descent Step *)
    u_traj[idx_k, 4] := u_traj[idx_k, 4] - (r_PGD_StepSize_Alpha * grad_u[idx_k, 4]);
    
    (* Box Constraint Projection *)
    IF u_traj[idx_k, 4] < u_min[4] THEN
        u_traj[idx_k, 4] := u_min[4];
    ELSIF u_traj[idx_k, 4] > u_max[4] THEN
        u_traj[idx_k, 4] := u_max[4];
    END_IF;
    
    (* Dynamic Slew Rate Projection *)
    IF idx_k = 0 THEN
        r_TmpDeltaU := u_traj[0, 4] - u_prev[4];
        IF r_TmpDeltaU > delta_u_max[4] THEN
            u_traj[0, 4] := u_prev[4] + delta_u_max[4];
        ELSIF r_TmpDeltaU < -delta_u_max[4] THEN
            u_traj[0, 4] := u_prev[4] - delta_u_max[4];
        END_IF;
    ELSE
        r_TmpDeltaU := u_traj[idx_k, 4] - u_traj[idx_k - 1, 4];
        IF r_TmpDeltaU > delta_u_max[4] THEN
            u_traj[idx_k, 4] := u_traj[idx_k - 1, 4] + delta_u_max[4];
        ELSIF r_TmpDeltaU < -delta_u_max[4] THEN
            u_traj[idx_k, 4] := u_traj[idx_k - 1, 4] - delta_u_max[4];
        END_IF;
    END_IF;
    (* Gradient Evaluation Control 5 *)
    IF idx_k = 0 THEN
        grad_u[0, 5] := ((B_mat[1, 5] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 5] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 5] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 5] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 5] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 5] * lambda_costate[idx_k + 1, 6])) + (R_diag[5] * u_traj[0, 5]) + (S_diag[5] * (u_traj[0, 5] - u_prev[5]));
    ELSE
        grad_u[idx_k, 5] := ((B_mat[1, 5] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 5] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 5] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 5] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 5] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 5] * lambda_costate[idx_k + 1, 6])) + (R_diag[5] * u_traj[idx_k, 5]) + (S_diag[5] * (u_traj[idx_k, 5] - u_traj[idx_k - 1, 5]));
    END_IF;
    
    (* Descent Step *)
    u_traj[idx_k, 5] := u_traj[idx_k, 5] - (r_PGD_StepSize_Alpha * grad_u[idx_k, 5]);
    
    (* Box Constraint Projection *)
    IF u_traj[idx_k, 5] < u_min[5] THEN
        u_traj[idx_k, 5] := u_min[5];
    ELSIF u_traj[idx_k, 5] > u_max[5] THEN
        u_traj[idx_k, 5] := u_max[5];
    END_IF;
    
    (* Dynamic Slew Rate Projection *)
    IF idx_k = 0 THEN
        r_TmpDeltaU := u_traj[0, 5] - u_prev[5];
        IF r_TmpDeltaU > delta_u_max[5] THEN
            u_traj[0, 5] := u_prev[5] + delta_u_max[5];
        ELSIF r_TmpDeltaU < -delta_u_max[5] THEN
            u_traj[0, 5] := u_prev[5] - delta_u_max[5];
        END_IF;
    ELSE
        r_TmpDeltaU := u_traj[idx_k, 5] - u_traj[idx_k - 1, 5];
        IF r_TmpDeltaU > delta_u_max[5] THEN
            u_traj[idx_k, 5] := u_traj[idx_k - 1, 5] + delta_u_max[5];
        ELSIF r_TmpDeltaU < -delta_u_max[5] THEN
            u_traj[idx_k, 5] := u_traj[idx_k - 1, 5] - delta_u_max[5];
        END_IF;
    END_IF;
END_FOR;

(* ============================================================================================== *)
(* PGD UNROLLED ITERATION 10 OF 10                                                               *)
(* ============================================================================================== *)
(* Step 10.A: Forward State Simulation over Horizon k = 0 to 4 *)
FOR idx_k := 0 TO 4 DO
    x_traj[idx_k + 1, 1] := ((A_mat[1, 1] * x_traj[idx_k, 1]) + (A_mat[1, 2] * x_traj[idx_k, 2]) + (A_mat[1, 3] * x_traj[idx_k, 3]) + (A_mat[1, 4] * x_traj[idx_k, 4]) + (A_mat[1, 5] * x_traj[idx_k, 5]) + (A_mat[1, 6] * x_traj[idx_k, 6])) + ((B_mat[1, 1] * u_traj[idx_k, 1]) + (B_mat[1, 2] * u_traj[idx_k, 2]) + (B_mat[1, 3] * u_traj[idx_k, 3]) + (B_mat[1, 4] * u_traj[idx_k, 4]) + (B_mat[1, 5] * u_traj[idx_k, 5]));
    x_traj[idx_k + 1, 2] := ((A_mat[2, 1] * x_traj[idx_k, 1]) + (A_mat[2, 2] * x_traj[idx_k, 2]) + (A_mat[2, 3] * x_traj[idx_k, 3]) + (A_mat[2, 4] * x_traj[idx_k, 4]) + (A_mat[2, 5] * x_traj[idx_k, 5]) + (A_mat[2, 6] * x_traj[idx_k, 6])) + ((B_mat[2, 1] * u_traj[idx_k, 1]) + (B_mat[2, 2] * u_traj[idx_k, 2]) + (B_mat[2, 3] * u_traj[idx_k, 3]) + (B_mat[2, 4] * u_traj[idx_k, 4]) + (B_mat[2, 5] * u_traj[idx_k, 5]));
    x_traj[idx_k + 1, 3] := ((A_mat[3, 1] * x_traj[idx_k, 1]) + (A_mat[3, 2] * x_traj[idx_k, 2]) + (A_mat[3, 3] * x_traj[idx_k, 3]) + (A_mat[3, 4] * x_traj[idx_k, 4]) + (A_mat[3, 5] * x_traj[idx_k, 5]) + (A_mat[3, 6] * x_traj[idx_k, 6])) + ((B_mat[3, 1] * u_traj[idx_k, 1]) + (B_mat[3, 2] * u_traj[idx_k, 2]) + (B_mat[3, 3] * u_traj[idx_k, 3]) + (B_mat[3, 4] * u_traj[idx_k, 4]) + (B_mat[3, 5] * u_traj[idx_k, 5]));
    x_traj[idx_k + 1, 4] := ((A_mat[4, 1] * x_traj[idx_k, 1]) + (A_mat[4, 2] * x_traj[idx_k, 2]) + (A_mat[4, 3] * x_traj[idx_k, 3]) + (A_mat[4, 4] * x_traj[idx_k, 4]) + (A_mat[4, 5] * x_traj[idx_k, 5]) + (A_mat[4, 6] * x_traj[idx_k, 6])) + ((B_mat[4, 1] * u_traj[idx_k, 1]) + (B_mat[4, 2] * u_traj[idx_k, 2]) + (B_mat[4, 3] * u_traj[idx_k, 3]) + (B_mat[4, 4] * u_traj[idx_k, 4]) + (B_mat[4, 5] * u_traj[idx_k, 5]));
    x_traj[idx_k + 1, 5] := ((A_mat[5, 1] * x_traj[idx_k, 1]) + (A_mat[5, 2] * x_traj[idx_k, 2]) + (A_mat[5, 3] * x_traj[idx_k, 3]) + (A_mat[5, 4] * x_traj[idx_k, 4]) + (A_mat[5, 5] * x_traj[idx_k, 5]) + (A_mat[5, 6] * x_traj[idx_k, 6])) + ((B_mat[5, 1] * u_traj[idx_k, 1]) + (B_mat[5, 2] * u_traj[idx_k, 2]) + (B_mat[5, 3] * u_traj[idx_k, 3]) + (B_mat[5, 4] * u_traj[idx_k, 4]) + (B_mat[5, 5] * u_traj[idx_k, 5]));
    x_traj[idx_k + 1, 6] := ((A_mat[6, 1] * x_traj[idx_k, 1]) + (A_mat[6, 2] * x_traj[idx_k, 2]) + (A_mat[6, 3] * x_traj[idx_k, 3]) + (A_mat[6, 4] * x_traj[idx_k, 4]) + (A_mat[6, 5] * x_traj[idx_k, 5]) + (A_mat[6, 6] * x_traj[idx_k, 6])) + ((B_mat[6, 1] * u_traj[idx_k, 1]) + (B_mat[6, 2] * u_traj[idx_k, 2]) + (B_mat[6, 3] * u_traj[idx_k, 3]) + (B_mat[6, 4] * u_traj[idx_k, 4]) + (B_mat[6, 5] * u_traj[idx_k, 5]));
END_FOR;

(* Step 10.B: Terminal Horizon Adjoint Costate Evaluation (k = 5) *)
lambda_costate[5, 1] := P_term[1] * (x_traj[5, 1] - x_ref[1]);
lambda_costate[5, 2] := P_term[2] * (x_traj[5, 2] - x_ref[2]);
lambda_costate[5, 3] := P_term[3] * (x_traj[5, 3] - x_ref[3]);
lambda_costate[5, 4] := P_term[4] * (x_traj[5, 4] - x_ref[4]);
lambda_costate[5, 5] := P_term[5] * (x_traj[5, 5] - x_ref[5]);
lambda_costate[5, 6] := P_term[6] * (x_traj[5, 6] - x_ref[6]);

(* Step 10.C: Backward Adjoint Costate Propagation over Horizon k = 4 downto 0 *)
FOR idx_k := 4 TO 0 BY -1 DO
    lambda_costate[idx_k, 1] := ((A_mat[1, 1] * lambda_costate[idx_k + 1, 1]) + (A_mat[2, 1] * lambda_costate[idx_k + 1, 2]) + (A_mat[3, 1] * lambda_costate[idx_k + 1, 3]) + (A_mat[4, 1] * lambda_costate[idx_k + 1, 4]) + (A_mat[5, 1] * lambda_costate[idx_k + 1, 5]) + (A_mat[6, 1] * lambda_costate[idx_k + 1, 6])) + (Q_diag[1] * (x_traj[idx_k, 1] - x_ref[1]));
    lambda_costate[idx_k, 2] := ((A_mat[1, 2] * lambda_costate[idx_k + 1, 1]) + (A_mat[2, 2] * lambda_costate[idx_k + 1, 2]) + (A_mat[3, 2] * lambda_costate[idx_k + 1, 3]) + (A_mat[4, 2] * lambda_costate[idx_k + 1, 4]) + (A_mat[5, 2] * lambda_costate[idx_k + 1, 5]) + (A_mat[6, 2] * lambda_costate[idx_k + 1, 6])) + (Q_diag[2] * (x_traj[idx_k, 2] - x_ref[2]));
    lambda_costate[idx_k, 3] := ((A_mat[1, 3] * lambda_costate[idx_k + 1, 1]) + (A_mat[2, 3] * lambda_costate[idx_k + 1, 2]) + (A_mat[3, 3] * lambda_costate[idx_k + 1, 3]) + (A_mat[4, 3] * lambda_costate[idx_k + 1, 4]) + (A_mat[5, 3] * lambda_costate[idx_k + 1, 5]) + (A_mat[6, 3] * lambda_costate[idx_k + 1, 6])) + (Q_diag[3] * (x_traj[idx_k, 3] - x_ref[3]));
    lambda_costate[idx_k, 4] := ((A_mat[1, 4] * lambda_costate[idx_k + 1, 1]) + (A_mat[2, 4] * lambda_costate[idx_k + 1, 2]) + (A_mat[3, 4] * lambda_costate[idx_k + 1, 3]) + (A_mat[4, 4] * lambda_costate[idx_k + 1, 4]) + (A_mat[5, 4] * lambda_costate[idx_k + 1, 5]) + (A_mat[6, 4] * lambda_costate[idx_k + 1, 6])) + (Q_diag[4] * (x_traj[idx_k, 4] - x_ref[4]));
    lambda_costate[idx_k, 5] := ((A_mat[1, 5] * lambda_costate[idx_k + 1, 1]) + (A_mat[2, 5] * lambda_costate[idx_k + 1, 2]) + (A_mat[3, 5] * lambda_costate[idx_k + 1, 3]) + (A_mat[4, 5] * lambda_costate[idx_k + 1, 4]) + (A_mat[5, 5] * lambda_costate[idx_k + 1, 5]) + (A_mat[6, 5] * lambda_costate[idx_k + 1, 6])) + (Q_diag[5] * (x_traj[idx_k, 5] - x_ref[5]));
    lambda_costate[idx_k, 6] := ((A_mat[1, 6] * lambda_costate[idx_k + 1, 1]) + (A_mat[2, 6] * lambda_costate[idx_k + 1, 2]) + (A_mat[3, 6] * lambda_costate[idx_k + 1, 3]) + (A_mat[4, 6] * lambda_costate[idx_k + 1, 4]) + (A_mat[5, 6] * lambda_costate[idx_k + 1, 5]) + (A_mat[6, 6] * lambda_costate[idx_k + 1, 6])) + (Q_diag[6] * (x_traj[idx_k, 6] - x_ref[6]));
END_FOR;

(* Step 10.D: Control Gradient Computation & Projected Descent Step over Horizon k = 0 to 4 *)
FOR idx_k := 0 TO 4 DO
    (* Gradient Evaluation Control 1 *)
    IF idx_k = 0 THEN
        grad_u[0, 1] := ((B_mat[1, 1] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 1] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 1] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 1] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 1] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 1] * lambda_costate[idx_k + 1, 6])) + (R_diag[1] * u_traj[0, 1]) + (S_diag[1] * (u_traj[0, 1] - u_prev[1]));
    ELSE
        grad_u[idx_k, 1] := ((B_mat[1, 1] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 1] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 1] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 1] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 1] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 1] * lambda_costate[idx_k + 1, 6])) + (R_diag[1] * u_traj[idx_k, 1]) + (S_diag[1] * (u_traj[idx_k, 1] - u_traj[idx_k - 1, 1]));
    END_IF;
    
    (* Descent Step *)
    u_traj[idx_k, 1] := u_traj[idx_k, 1] - (r_PGD_StepSize_Alpha * grad_u[idx_k, 1]);
    
    (* Box Constraint Projection *)
    IF u_traj[idx_k, 1] < u_min[1] THEN
        u_traj[idx_k, 1] := u_min[1];
    ELSIF u_traj[idx_k, 1] > u_max[1] THEN
        u_traj[idx_k, 1] := u_max[1];
    END_IF;
    
    (* Dynamic Slew Rate Projection *)
    IF idx_k = 0 THEN
        r_TmpDeltaU := u_traj[0, 1] - u_prev[1];
        IF r_TmpDeltaU > delta_u_max[1] THEN
            u_traj[0, 1] := u_prev[1] + delta_u_max[1];
        ELSIF r_TmpDeltaU < -delta_u_max[1] THEN
            u_traj[0, 1] := u_prev[1] - delta_u_max[1];
        END_IF;
    ELSE
        r_TmpDeltaU := u_traj[idx_k, 1] - u_traj[idx_k - 1, 1];
        IF r_TmpDeltaU > delta_u_max[1] THEN
            u_traj[idx_k, 1] := u_traj[idx_k - 1, 1] + delta_u_max[1];
        ELSIF r_TmpDeltaU < -delta_u_max[1] THEN
            u_traj[idx_k, 1] := u_traj[idx_k - 1, 1] - delta_u_max[1];
        END_IF;
    END_IF;
    (* Gradient Evaluation Control 2 *)
    IF idx_k = 0 THEN
        grad_u[0, 2] := ((B_mat[1, 2] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 2] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 2] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 2] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 2] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 2] * lambda_costate[idx_k + 1, 6])) + (R_diag[2] * u_traj[0, 2]) + (S_diag[2] * (u_traj[0, 2] - u_prev[2]));
    ELSE
        grad_u[idx_k, 2] := ((B_mat[1, 2] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 2] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 2] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 2] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 2] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 2] * lambda_costate[idx_k + 1, 6])) + (R_diag[2] * u_traj[idx_k, 2]) + (S_diag[2] * (u_traj[idx_k, 2] - u_traj[idx_k - 1, 2]));
    END_IF;
    
    (* Descent Step *)
    u_traj[idx_k, 2] := u_traj[idx_k, 2] - (r_PGD_StepSize_Alpha * grad_u[idx_k, 2]);
    
    (* Box Constraint Projection *)
    IF u_traj[idx_k, 2] < u_min[2] THEN
        u_traj[idx_k, 2] := u_min[2];
    ELSIF u_traj[idx_k, 2] > u_max[2] THEN
        u_traj[idx_k, 2] := u_max[2];
    END_IF;
    
    (* Dynamic Slew Rate Projection *)
    IF idx_k = 0 THEN
        r_TmpDeltaU := u_traj[0, 2] - u_prev[2];
        IF r_TmpDeltaU > delta_u_max[2] THEN
            u_traj[0, 2] := u_prev[2] + delta_u_max[2];
        ELSIF r_TmpDeltaU < -delta_u_max[2] THEN
            u_traj[0, 2] := u_prev[2] - delta_u_max[2];
        END_IF;
    ELSE
        r_TmpDeltaU := u_traj[idx_k, 2] - u_traj[idx_k - 1, 2];
        IF r_TmpDeltaU > delta_u_max[2] THEN
            u_traj[idx_k, 2] := u_traj[idx_k - 1, 2] + delta_u_max[2];
        ELSIF r_TmpDeltaU < -delta_u_max[2] THEN
            u_traj[idx_k, 2] := u_traj[idx_k - 1, 2] - delta_u_max[2];
        END_IF;
    END_IF;
    (* Gradient Evaluation Control 3 *)
    IF idx_k = 0 THEN
        grad_u[0, 3] := ((B_mat[1, 3] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 3] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 3] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 3] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 3] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 3] * lambda_costate[idx_k + 1, 6])) + (R_diag[3] * u_traj[0, 3]) + (S_diag[3] * (u_traj[0, 3] - u_prev[3]));
    ELSE
        grad_u[idx_k, 3] := ((B_mat[1, 3] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 3] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 3] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 3] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 3] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 3] * lambda_costate[idx_k + 1, 6])) + (R_diag[3] * u_traj[idx_k, 3]) + (S_diag[3] * (u_traj[idx_k, 3] - u_traj[idx_k - 1, 3]));
    END_IF;
    
    (* Descent Step *)
    u_traj[idx_k, 3] := u_traj[idx_k, 3] - (r_PGD_StepSize_Alpha * grad_u[idx_k, 3]);
    
    (* Box Constraint Projection *)
    IF u_traj[idx_k, 3] < u_min[3] THEN
        u_traj[idx_k, 3] := u_min[3];
    ELSIF u_traj[idx_k, 3] > u_max[3] THEN
        u_traj[idx_k, 3] := u_max[3];
    END_IF;
    
    (* Dynamic Slew Rate Projection *)
    IF idx_k = 0 THEN
        r_TmpDeltaU := u_traj[0, 3] - u_prev[3];
        IF r_TmpDeltaU > delta_u_max[3] THEN
            u_traj[0, 3] := u_prev[3] + delta_u_max[3];
        ELSIF r_TmpDeltaU < -delta_u_max[3] THEN
            u_traj[0, 3] := u_prev[3] - delta_u_max[3];
        END_IF;
    ELSE
        r_TmpDeltaU := u_traj[idx_k, 3] - u_traj[idx_k - 1, 3];
        IF r_TmpDeltaU > delta_u_max[3] THEN
            u_traj[idx_k, 3] := u_traj[idx_k - 1, 3] + delta_u_max[3];
        ELSIF r_TmpDeltaU < -delta_u_max[3] THEN
            u_traj[idx_k, 3] := u_traj[idx_k - 1, 3] - delta_u_max[3];
        END_IF;
    END_IF;
    (* Gradient Evaluation Control 4 *)
    IF idx_k = 0 THEN
        grad_u[0, 4] := ((B_mat[1, 4] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 4] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 4] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 4] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 4] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 4] * lambda_costate[idx_k + 1, 6])) + (R_diag[4] * u_traj[0, 4]) + (S_diag[4] * (u_traj[0, 4] - u_prev[4]));
    ELSE
        grad_u[idx_k, 4] := ((B_mat[1, 4] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 4] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 4] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 4] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 4] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 4] * lambda_costate[idx_k + 1, 6])) + (R_diag[4] * u_traj[idx_k, 4]) + (S_diag[4] * (u_traj[idx_k, 4] - u_traj[idx_k - 1, 4]));
    END_IF;
    
    (* Descent Step *)
    u_traj[idx_k, 4] := u_traj[idx_k, 4] - (r_PGD_StepSize_Alpha * grad_u[idx_k, 4]);
    
    (* Box Constraint Projection *)
    IF u_traj[idx_k, 4] < u_min[4] THEN
        u_traj[idx_k, 4] := u_min[4];
    ELSIF u_traj[idx_k, 4] > u_max[4] THEN
        u_traj[idx_k, 4] := u_max[4];
    END_IF;
    
    (* Dynamic Slew Rate Projection *)
    IF idx_k = 0 THEN
        r_TmpDeltaU := u_traj[0, 4] - u_prev[4];
        IF r_TmpDeltaU > delta_u_max[4] THEN
            u_traj[0, 4] := u_prev[4] + delta_u_max[4];
        ELSIF r_TmpDeltaU < -delta_u_max[4] THEN
            u_traj[0, 4] := u_prev[4] - delta_u_max[4];
        END_IF;
    ELSE
        r_TmpDeltaU := u_traj[idx_k, 4] - u_traj[idx_k - 1, 4];
        IF r_TmpDeltaU > delta_u_max[4] THEN
            u_traj[idx_k, 4] := u_traj[idx_k - 1, 4] + delta_u_max[4];
        ELSIF r_TmpDeltaU < -delta_u_max[4] THEN
            u_traj[idx_k, 4] := u_traj[idx_k - 1, 4] - delta_u_max[4];
        END_IF;
    END_IF;
    (* Gradient Evaluation Control 5 *)
    IF idx_k = 0 THEN
        grad_u[0, 5] := ((B_mat[1, 5] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 5] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 5] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 5] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 5] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 5] * lambda_costate[idx_k + 1, 6])) + (R_diag[5] * u_traj[0, 5]) + (S_diag[5] * (u_traj[0, 5] - u_prev[5]));
    ELSE
        grad_u[idx_k, 5] := ((B_mat[1, 5] * lambda_costate[idx_k + 1, 1]) + (B_mat[2, 5] * lambda_costate[idx_k + 1, 2]) + (B_mat[3, 5] * lambda_costate[idx_k + 1, 3]) + (B_mat[4, 5] * lambda_costate[idx_k + 1, 4]) + (B_mat[5, 5] * lambda_costate[idx_k + 1, 5]) + (B_mat[6, 5] * lambda_costate[idx_k + 1, 6])) + (R_diag[5] * u_traj[idx_k, 5]) + (S_diag[5] * (u_traj[idx_k, 5] - u_traj[idx_k - 1, 5]));
    END_IF;
    
    (* Descent Step *)
    u_traj[idx_k, 5] := u_traj[idx_k, 5] - (r_PGD_StepSize_Alpha * grad_u[idx_k, 5]);
    
    (* Box Constraint Projection *)
    IF u_traj[idx_k, 5] < u_min[5] THEN
        u_traj[idx_k, 5] := u_min[5];
    ELSIF u_traj[idx_k, 5] > u_max[5] THEN
        u_traj[idx_k, 5] := u_max[5];
    END_IF;
    
    (* Dynamic Slew Rate Projection *)
    IF idx_k = 0 THEN
        r_TmpDeltaU := u_traj[0, 5] - u_prev[5];
        IF r_TmpDeltaU > delta_u_max[5] THEN
            u_traj[0, 5] := u_prev[5] + delta_u_max[5];
        ELSIF r_TmpDeltaU < -delta_u_max[5] THEN
            u_traj[0, 5] := u_prev[5] - delta_u_max[5];
        END_IF;
    ELSE
        r_TmpDeltaU := u_traj[idx_k, 5] - u_traj[idx_k - 1, 5];
        IF r_TmpDeltaU > delta_u_max[5] THEN
            u_traj[idx_k, 5] := u_traj[idx_k - 1, 5] + delta_u_max[5];
        ELSIF r_TmpDeltaU < -delta_u_max[5] THEN
            u_traj[idx_k, 5] := u_traj[idx_k - 1, 5] - delta_u_max[5];
        END_IF;
    END_IF;
END_FOR;

(* ---------------------------------------------------------------------------------------------------- *)
(* 3.4 EXTRACT OPTIMAL CONTROL VECTOR & DISPATCH PHYSICAL ACTUATOR COMMANDS                             *)
(* ---------------------------------------------------------------------------------------------------- *)
u_prev[1] := u_cmd[1];
u_cmd[1] := u_traj[0, 1];
u_prev[2] := u_cmd[2];
u_cmd[2] := u_traj[0, 2];
u_prev[3] := u_cmd[3];
u_cmd[3] := u_traj[0, 3];
u_prev[4] := u_cmd[4];
u_cmd[4] := u_traj[0, 4];
u_prev[5] := u_cmd[5];
u_cmd[5] := u_traj[0, 5];

(* Scale & Assign Hydraulic Variable Displacement Servo Pump Command [%] *)
r_MainPumpSwashplateCmd_Pct := u_cmd[1];

(* Leveling Servo Valves: Differential Flow Command to Counteract Dynamic Eccentric Moments [L/min]   *)
(* Positive u_cmd[2] induces clockwise leveling flow differential across diagonally opposed cylinders   *)
r_RamLevelingValve_FL_Cmd_L_min := u_cmd[2];
r_RamLevelingValve_FR_Cmd_L_min := -1.0 * u_cmd[2];
r_RamLevelingValve_RL_Cmd_L_min := u_cmd[2];
r_RamLevelingValve_RR_Cmd_L_min := -1.0 * u_cmd[2];

(* Multi-Zone Induction Power Generator Master Output [kW] *)
r_InductionPowerCmd_kW := u_cmd[3];

(* Dynamic Counterbalance Valve Backpressure Command [%] *)
r_CounterbalanceValveCmd_Pct := u_cmd[5];
