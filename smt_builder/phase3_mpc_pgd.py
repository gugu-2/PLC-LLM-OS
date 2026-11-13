# -*- coding: utf-8 -*-
"""
smt_builder/phase3_mpc_pgd.py
Generates Phase 3: Receding-Horizon MPC Optimization with Projected Gradient Descent (PGD)
and physical slew rate limiters.
"""

def get_phase3_mpc():
    lines = []
    lines.append("""(*
========================================================================================================================
  PHASE 3: RECEDING-HORIZON MPC OPTIMIZATION WITH PROJECTED GRADIENT DESCENT (PGD) & PHYSICAL SLEW LIMITS
========================================================================================================================
  Solves the finite-horizon constrained quadratic optimal control problem:
      min  J = sum_{k=0}^{Np-1} [ (x_k - x_ref)^T * Q * (x_k - x_ref) + u_k^T * R * u_k + (u_k - u_{k-1})^T * S * (u_k - u_{k-1}) ]
               + (x_Np - x_ref)^T * P * (x_Np - x_ref)
      s.t. x_{k+1} = A * x_k + B * u_k
           u_min <= u_k <= u_max
           |u_k - u_{k-1}| <= Delta_u_max

  Optimization Parameters:
    - Prediction Horizon: Np = 5 steps (5.0 ms look-ahead)
    - Control Horizon   : Nc = 3 steps (first move implemented receding-horizon style)
    - Optimization Method: Unrolled Projected Gradient Descent (PGD) with analytical gradient backpropagation
    - Actuator Slew Protection: Dual jerk-bounded rate limiters on linear motor thrust and spindle theta torque.
*)

(* -------------------------------------------------------------------------------------------------------------------- *)
(* SUB-PHASE 3.1: DYNAMIC REFERENCE STATE TRAJECTORY VECTOR GENERATION (x_ref)                                          *)
(* -------------------------------------------------------------------------------------------------------------------- *)
x_ref[1]  := rProfile_Pos_Target_X;           (* Target X coordinate on PCBA [mm] *)
x_ref[2]  := 0.0;                             (* Zero cruising velocity at settle point [mm/s] *)
x_ref[3]  := 0.0;                             (* Zero TCP flexure vibration deflection [mm] *)
x_ref[4]  := 0.0;                             (* Zero TCP flexure vibration velocity [mm/s] *)
x_ref[5]  := rProfile_Pos_Target_Y;           (* Target Y coordinate on PCBA [mm] *)
x_ref[6]  := 0.0;                             (* Settled rotational velocity [rad/s] *)

(* Spindle Vacuum Reference depends on active component grip status *)
IF arrSpindle_HasComponent[iActive_Spindle_Index] THEN
    x_ref[7] := -72.0;                        (* Target holding vacuum: -72.0 kPa *)
ELSE
    x_ref[7] := 0.0;                          (* Atmospheric pressure when empty *)
END_IF;

x_ref[8]  := 0.0;                             (* Zero acoustic leakage flow [L/min] *)
x_ref[9]  := 0.0;                             (* Zero gantry crossbeam yaw skew angle [mrad] *)
x_ref[10] := 0.0;                             (* Zero uncompensated thermal expansion strain [um] *)

(* Initialize candidate control inputs over control horizon Nc = 3 *)
FOR iCol := 1 TO 4 DO
    u_cand_h0[iCol] := u_prev[iCol];
    u_cand_h1[iCol] := u_prev[iCol];
    u_cand_h2[iCol] := u_prev[iCol];
END_FOR;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* SUB-PHASE 3.2: UNROLLED PROJECTED GRADIENT DESCENT (PGD) SOLVER (4 COMPLETE ITERATIONS)                             *)
(* -------------------------------------------------------------------------------------------------------------------- *)
FOR iPGD_IterCount := 1 TO 4 DO
    (* Step 1: Forward State Propagation along Prediction Horizon Np = 5 *)
    (* Step h0: x_pred_h0 = current estimated state *)
    FOR iRow := 1 TO 10 DO
        x_pred_h0[iRow] := x_state[iRow];
    END_FOR;

    (* Step h1: x_pred_h1 = A * x_pred_h0 + B * u_cand_h0 *)
    FOR iRow := 1 TO 10 DO
        rAccumTerm := 0.0;
        FOR iCol := 1 TO 10 DO
            rAccumTerm := rAccumTerm + (a_mat[iRow, iCol] * x_pred_h0[iCol]);
        END_FOR;
        FOR iCol := 1 TO 4 DO
            rAccumTerm := rAccumTerm + (b_mat[iRow, iCol] * u_cand_h0[iCol]);
        END_FOR;
        x_pred_h1[iRow] := rAccumTerm;
    END_FOR;

    (* Step h2: x_pred_h2 = A * x_pred_h1 + B * u_cand_h1 *)
    FOR iRow := 1 TO 10 DO
        rAccumTerm := 0.0;
        FOR iCol := 1 TO 10 DO
            rAccumTerm := rAccumTerm + (a_mat[iRow, iCol] * x_pred_h1[iCol]);
        END_FOR;
        FOR iCol := 1 TO 4 DO
            rAccumTerm := rAccumTerm + (b_mat[iRow, iCol] * u_cand_h1[iCol]);
        END_FOR;
        x_pred_h2[iRow] := rAccumTerm;
    END_FOR;

    (* Step h3: x_pred_h3 = A * x_pred_h2 + B * u_cand_h2 *)
    FOR iRow := 1 TO 10 DO
        rAccumTerm := 0.0;
        FOR iCol := 1 TO 10 DO
            rAccumTerm := rAccumTerm + (a_mat[iRow, iCol] * x_pred_h2[iCol]);
        END_FOR;
        FOR iCol := 1 TO 4 DO
            rAccumTerm := rAccumTerm + (b_mat[iRow, iCol] * u_cand_h2[iCol]);
        END_FOR;
        x_pred_h3[iRow] := rAccumTerm;
    END_FOR;

    (* Step h4: x_pred_h4 = A * x_pred_h3 + B * u_cand_h2 (Zero-order hold on input for k >= Nc) *)
    FOR iRow := 1 TO 10 DO
        rAccumTerm := 0.0;
        FOR iCol := 1 TO 10 DO
            rAccumTerm := rAccumTerm + (a_mat[iRow, iCol] * x_pred_h3[iCol]);
        END_FOR;
        FOR iCol := 1 TO 4 DO
            rAccumTerm := rAccumTerm + (b_mat[iRow, iCol] * u_cand_h2[iCol]);
        END_FOR;
        x_pred_h4[iRow] := rAccumTerm;
    END_FOR;

    (* Step h5: x_pred_h5 = A * x_pred_h4 + B * u_cand_h2 (Terminal step) *)
    FOR iRow := 1 TO 10 DO
        rAccumTerm := 0.0;
        FOR iCol := 1 TO 10 DO
            rAccumTerm := rAccumTerm + (a_mat[iRow, iCol] * x_pred_h4[iCol]);
        END_FOR;
        FOR iCol := 1 TO 4 DO
            rAccumTerm := rAccumTerm + (b_mat[iRow, iCol] * u_cand_h2[iCol]);
        END_FOR;
        x_pred_h5[iRow] := rAccumTerm;
    END_FOR;

    (* Step 2: Analytical Gradient Computation with respect to u_cand_h0 *)
    FOR iCol := 1 TO 4 DO
        (* Actuator cost penalty gradient term: 2 * R * u *)
        rAccumTerm := 2.0 * r_mat[iCol, iCol] * u_cand_h0[iCol];
        (* Slew rate penalty gradient term: 2 * S * (u_h0 - u_prev) - 2 * S * (u_h1 - u_h0) *)
        rAccumTerm := rAccumTerm + (2.0 * s_mat[iCol, iCol] * (u_cand_h0[iCol] - u_prev[iCol]))
                                 - (2.0 * s_mat[iCol, iCol] * (u_cand_h1[iCol] - u_cand_h0[iCol]));
        (* State tracking backpropagation: 2 * B^T * Q * (x_pred_h1 - x_ref) *)
        FOR iRow := 1 TO 10 DO
            rAccumTerm := rAccumTerm + (2.0 * b_mat[iRow, iCol] * q_mat[iRow, iRow] * (x_pred_h1[iRow] - x_ref[iRow]));
        END_FOR;
        grad_u_h0[iCol] := rAccumTerm;
    END_FOR;

    (* Step 3: Analytical Gradient Computation with respect to u_cand_h1 *)
    FOR iCol := 1 TO 4 DO
        rAccumTerm := 2.0 * r_mat[iCol, iCol] * u_cand_h1[iCol];
        rAccumTerm := rAccumTerm + (2.0 * s_mat[iCol, iCol] * (u_cand_h1[iCol] - u_cand_h0[iCol]))
                                 - (2.0 * s_mat[iCol, iCol] * (u_cand_h2[iCol] - u_cand_h1[iCol]));
        FOR iRow := 1 TO 10 DO
            rAccumTerm := rAccumTerm + (2.0 * b_mat[iRow, iCol] * q_mat[iRow, iRow] * (x_pred_h2[iRow] - x_ref[iRow]));
        END_FOR;
        grad_u_h1[iCol] := rAccumTerm;
    END_FOR;

    (* Step 4: Analytical Gradient Computation with respect to u_cand_h2 *)
    FOR iCol := 1 TO 4 DO
        rAccumTerm := 2.0 * r_mat[iCol, iCol] * u_cand_h2[iCol];
        rAccumTerm := rAccumTerm + (2.0 * s_mat[iCol, iCol] * (u_cand_h2[iCol] - u_cand_h1[iCol]));
        FOR iRow := 1 TO 10 DO
            rAccumTerm := rAccumTerm + (2.0 * b_mat[iRow, iCol] * q_mat[iRow, iRow] * (x_pred_h3[iRow] - x_ref[iRow]))
                                     + (2.0 * b_mat[iRow, iCol] * p_mat[iRow, iRow] * (x_pred_h5[iRow] - x_ref[iRow]));
        END_FOR;
        grad_u_h2[iCol] := rAccumTerm;
    END_FOR;

    (* Step 5: Gradient Descent Update *)
    FOR iCol := 1 TO 4 DO
        u_cand_h0[iCol] := u_cand_h0[iCol] - (rPGD_StepSize * grad_u_h0[iCol]);
        u_cand_h1[iCol] := u_cand_h1[iCol] - (rPGD_StepSize * grad_u_h1[iCol]);
        u_cand_h2[iCol] := u_cand_h2[iCol] - (rPGD_StepSize * grad_u_h2[iCol]);
    END_FOR;

    (* Step 6: Projection onto Physical Box Constraints for u_cand_h0 *)
    (* Control Channel 1: Gantry X Linear Motor Force [N] *)
    IF u_cand_h0[1] > rLimit_ForceX_Max THEN
        u_cand_h0[1] := rLimit_ForceX_Max;
    ELSIF u_cand_h0[1] < rLimit_ForceX_Min THEN
        u_cand_h0[1] := rLimit_ForceX_Min;
    END_IF;

    (* Control Channel 2: Gantry Y Linear Motor Force [N] *)
    IF u_cand_h0[2] > rLimit_ForceY_Max THEN
        u_cand_h0[2] := rLimit_ForceY_Max;
    ELSIF u_cand_h0[2] < rLimit_ForceY_Min THEN
        u_cand_h0[2] := rLimit_ForceY_Min;
    END_IF;

    (* Control Channel 3: Spindle Theta Torque [mN*m] *)
    IF u_cand_h0[3] > rLimit_ThetaTorque_Max THEN
        u_cand_h0[3] := rLimit_ThetaTorque_Max;
    ELSIF u_cand_h0[3] < rLimit_ThetaTorque_Min THEN
        u_cand_h0[3] := rLimit_ThetaTorque_Min;
    END_IF;

    (* Control Channel 4: Vacuum PWM [%] *)
    IF u_cand_h0[4] > rLimit_VacuumPWM_Max THEN
        u_cand_h0[4] := rLimit_VacuumPWM_Max;
    ELSIF u_cand_h0[4] < rLimit_VacuumPWM_Min THEN
        u_cand_h0[4] := rLimit_VacuumPWM_Min;
    END_IF;
END_FOR;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* SUB-PHASE 3.3: DYNAMIC PHYSICAL SLEW RATE LIMITING & FINAL ACTUATOR ASSIGNMENT                                       *)
(* -------------------------------------------------------------------------------------------------------------------- *)
(* Slew rate limiting on Gantry X Force *)
delta_u[1] := u_cand_h0[1] - u_prev[1];
IF delta_u[1] > rLimit_SlewRate_Force_Max THEN
    u_ctrl[1] := u_prev[1] + rLimit_SlewRate_Force_Max;
ELSIF delta_u[1] < -rLimit_SlewRate_Force_Max THEN
    u_ctrl[1] := u_prev[1] - rLimit_SlewRate_Force_Max;
ELSE
    u_ctrl[1] := u_cand_h0[1];
END_IF;

(* Slew rate limiting on Gantry Y Force *)
delta_u[2] := u_cand_h0[2] - u_prev[2];
IF delta_u[2] > rLimit_SlewRate_Force_Max THEN
    u_ctrl[2] := u_prev[2] + rLimit_SlewRate_Force_Max;
ELSIF delta_u[2] < -rLimit_SlewRate_Force_Max THEN
    u_ctrl[2] := u_prev[2] - rLimit_SlewRate_Force_Max;
ELSE
    u_ctrl[2] := u_cand_h0[2];
END_IF;

(* Slew rate limiting on Spindle Theta Torque *)
delta_u[3] := u_cand_h0[3] - u_prev[3];
IF delta_u[3] > rLimit_SlewRate_Torque_Max THEN
    u_ctrl[3] := u_prev[3] + rLimit_SlewRate_Torque_Max;
ELSIF delta_u[3] < -rLimit_SlewRate_Torque_Max THEN
    u_ctrl[3] := u_prev[3] - rLimit_SlewRate_Torque_Max;
ELSE
    u_ctrl[3] := u_cand_h0[3];
END_IF;

(* Fast Direct Assignment on Vacuum Valve PWM (solenoid has microsecond response) *)
u_ctrl[4] := u_cand_h0[4];

(* Update prior control action register for next cycle *)
FOR iCol := 1 TO 4 DO
    u_prev[iCol] := u_ctrl[iCol];
END_FOR;

(* Assign Optimal Actuator Outputs *)
rCmd_Gantry_X_Force    := u_ctrl[1];
rCmd_Gantry_Y_Force    := u_ctrl[2];
rCmd_Head_Theta_Torque := u_ctrl[3];
rCmd_VacuumValve_PWM   := u_ctrl[4];
""")
    return "\n".join(lines)
