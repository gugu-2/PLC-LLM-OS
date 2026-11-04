# scripts/feedmill_builder/part6_phase3_mpc.py
# -*- coding: utf-8 -*-

def get_phase3_block():
    return """(* ====================================================================================================
   PHASE 3: DISCRETE STATE-SPACE PROPAGATION & RECEDING-HORIZON MPC
   ==================================================================================================== *)

(* ----------------------------------------------------------------------------------------------------
   3.1 TARGET SETPOINT VECTOR & DISTURBANCE VECTOR PACKING
   ---------------------------------------------------------------------------------------------------- *)
x_target[1] := rTargetMashTemp_SP_degC;     (* Conditioner Target Mash Temp [deg C] *)
x_target[2] := rTargetMashMoist_SP_pct;     (* Conditioned Mash Target Moisture [%] *)
x_target[3] := rTargetGelatinization_SP;    (* Target Starch Gelatinization Extent [0..1] *)
x_target[4] := 580.0;                       (* Pellet Mill Motor Current Target (81% FLC) [A] *)
x_target[5] := 98.0;                        (* Ring Die Normal Operating Surface Temp [deg C] *)
x_target[6] := rTargetRollerGap_SP_mm;      (* Target Dynamic Roller Hydraulic Gap [mm] *)
x_target[7] := rTargetCoolerBed_SP_mm;      (* Counterflow Cooler Regulated Bed Depth [mm] *)
x_target[8] := rTargetFinalMoist_SP_pct;    (* Final Cooled Pellets Target Moisture [%] *)

d_dist[1]   := rRawMashTemp_Inlet_degC;     (* Inlet Grain Temperature Disturbance [deg C] *)
d_dist[2]   := rRawMashMoist_Inlet_pct;     (* Inlet Grain Moisture Disturbance [%] *)
d_dist[3]   := rSteamHdrPress_Supply_bar;   (* Culinary Steam Supply Pressure [bar] *)

(* Tracking Error Evaluation e_x = x_state - x_target *)
FOR i := 1 TO 8 DO
    x_error[i] := x_state[i] - x_target[i];
END_FOR;

(* ----------------------------------------------------------------------------------------------------
   3.2 ONE-STEP AHEAD DISCRETE STATE PROPAGATION: x(k+1) = A * x(k) + B * u(k) + E * d(k)
   ---------------------------------------------------------------------------------------------------- *)
FOR i := 1 TO 8 DO
    rTempAccum := 0.0;
    (* State Transition Dynamics A * x *)
    FOR j := 1 TO 8 DO
        rTempAccum := rTempAccum + A_mat[i,j] * x_state[j];
    END_FOR;
    (* Control Input Actuation B * u *)
    FOR m := 1 TO 6 DO
        rTempAccum := rTempAccum + B_mat[i,m] * u_ctrl[m];
    END_FOR;
    (* Disturbance Coupling E * d *)
    FOR j := 1 TO 3 DO
        rTempAccum := rTempAccum + E_mat[i,j] * d_dist[j];
    END_FOR;
    x_next[i] := rTempAccum;
END_FOR;

(* ----------------------------------------------------------------------------------------------------
   3.3 RECEDING-HORIZON TRAJECTORY PREDICTION (HORIZON Np = 3)
   ---------------------------------------------------------------------------------------------------- *)
(* Horizon Step 1: x_pred[1] = A * x_state + B * u + E * d *)
FOR i := 1 TO 8 DO
    rTempAccum := 0.0;
    FOR j := 1 TO 8 DO
        rTempAccum := rTempAccum + A_mat[i,j] * x_state[j];
    END_FOR;
    FOR m := 1 TO 6 DO
        rTempAccum := rTempAccum + B_mat[i,m] * u_ctrl[m];
    END_FOR;
    FOR j := 1 TO 3 DO
        rTempAccum := rTempAccum + E_mat[i,j] * d_dist[j];
    END_FOR;
    x_pred[1, i] := rTempAccum;
END_FOR;

(* Horizon Step 2: x_pred[2] = A * x_pred[1] + B * u + E * d *)
FOR i := 1 TO 8 DO
    rTempAccum := 0.0;
    FOR j := 1 TO 8 DO
        rTempAccum := rTempAccum + A_mat[i,j] * x_pred[1, j];
    END_FOR;
    FOR m := 1 TO 6 DO
        rTempAccum := rTempAccum + B_mat[i,m] * u_ctrl[m];
    END_FOR;
    FOR j := 1 TO 3 DO
        rTempAccum := rTempAccum + E_mat[i,j] * d_dist[j];
    END_FOR;
    x_pred[2, i] := rTempAccum;
END_FOR;

(* Horizon Step 3: x_pred[3] = A * x_pred[2] + B * u + E * d *)
FOR i := 1 TO 8 DO
    rTempAccum := 0.0;
    FOR j := 1 TO 8 DO
        rTempAccum := rTempAccum + A_mat[i,j] * x_pred[2, j];
    END_FOR;
    FOR m := 1 TO 6 DO
        rTempAccum := rTempAccum + B_mat[i,m] * u_ctrl[m];
    END_FOR;
    FOR j := 1 TO 3 DO
        rTempAccum := rTempAccum + E_mat[i,j] * d_dist[j];
    END_FOR;
    x_pred[3, i] := rTempAccum;
END_FOR;

(* ----------------------------------------------------------------------------------------------------
   3.4 MPC QUADRATIC OBJECTIVE COST FUNCTION EVALUATION J
   J = SUM_k [ (x_pred - x_sp)^T * Q * (x_pred - x_sp) ] + Delta_u^T * R * Delta_u + (x_pred3 - x_sp)^T * P * (...)
   ---------------------------------------------------------------------------------------------------- *)
J_cost := 0.0;

(* Stage Cost for Prediction Step 1 and Step 2 *)
FOR k_step := 1 TO 2 DO
    FOR i := 1 TO 8 DO
        rTempAccum := x_pred[k_step, i] - x_target[i];
        J_cost     := J_cost + Q_diag[i] * (rTempAccum * rTempAccum);
    END_FOR;
END_FOR;

(* Actuator Slew Rate Penalties Delta_u^T * R * Delta_u *)
FOR m := 1 TO 6 DO
    rTempAccum := u_ctrl[m] - u_prev[m];
    J_cost     := J_cost + R_diag[m] * (rTempAccum * rTempAccum);
END_FOR;

(* Terminal Cost at Prediction Step 3 with Heavy P_term Weights *)
FOR i := 1 TO 8 DO
    rTempAccum := x_pred[3, i] - x_target[i];
    J_cost     := J_cost + P_diag[i] * (rTempAccum * rTempAccum);
END_FOR;

(* ----------------------------------------------------------------------------------------------------
   3.5 ANALYTICAL GRADIENT EVALUATION & ACTIVE-SET CONSTRAINED QP UPDATE
   dJ / du_m = 2 * SUM_k [ Q_i * (x_pred_k - x_sp) * S_k,m ] + 2 * R_m * Delta_u_m + 2 * P_i * (...)
   ---------------------------------------------------------------------------------------------------- *)
IF bAutoMode AND nFsm_CurrentState = 8 THEN
    (* Steady-State Automatic Pelleting: Execute receding horizon optimization step *)
    FOR m := 1 TO 6 DO
        u_gradient[m] := 0.0;

        (* Sensitivity propagation for Horizon Step 1: dx_pred[1]/du_m = B[i,m] *)
        FOR i := 1 TO 8 DO
            rTempAccum    := x_pred[1, i] - x_target[i];
            u_gradient[m] := u_gradient[m] + 2.0 * Q_diag[i] * rTempAccum * B_mat[i,m];
        END_FOR;

        (* Sensitivity propagation for Horizon Step 2: dx_pred[2]/du_m = (A * B + B)[i,m] *)
        FOR i := 1 TO 8 DO
            rTempAccum := 0.0;
            FOR j := 1 TO 8 DO
                rTempAccum := rTempAccum + A_mat[i,j] * B_mat[j,m];
            END_FOR;
            rTempAccum := rTempAccum + B_mat[i,m];
            u_gradient[m] := u_gradient[m] + 2.0 * Q_diag[i] * (x_pred[2, i] - x_target[i]) * rTempAccum;
        END_FOR;

        (* Terminal Step 3 Sensitivity with P_term: dx_pred[3]/du_m *)
        FOR i := 1 TO 8 DO
            rTempAccum := 0.0;
            FOR j := 1 TO 8 DO
                FOR k_step := 1 TO 8 DO
                    rTempAccum := rTempAccum + A_mat[i,j] * A_mat[j,k_step] * B_mat[k_step,m];
                END_FOR;
                rTempAccum := rTempAccum + A_mat[i,j] * B_mat[j,m];
            END_FOR;
            rTempAccum := rTempAccum + B_mat[i,m];
            u_gradient[m] := u_gradient[m] + 2.0 * P_diag[i] * (x_pred[3, i] - x_target[i]) * rTempAccum;
        END_FOR;

        (* Add Actuator Slew Regularization Gradient *)
        u_gradient[m] := u_gradient[m] + 2.0 * R_diag[m] * (u_ctrl[m] - u_prev[m]);

        (* Adaptive Projected Gradient Step *)
        rTempAccum := u_ctrl[m] - (rMpcStepGamma * u_gradient[m]);

        (* Slew Rate Clamping [-du_max, +du_max] *)
        rSumPredCost := rTempAccum - u_prev[m];
        IF rSumPredCost > du_max[m] THEN
            rSumPredCost := du_max[m];
        ELSIF rSumPredCost < -du_max[m] THEN
            rSumPredCost := -du_max[m];
        END_IF;

        (* Physical Actuator Saturation Bounds Clamping [u_min, u_max] *)
        rTempAccum := u_prev[m] + rSumPredCost;
        IF rTempAccum > u_max[m] THEN
            rTempAccum := u_max[m];
        ELSIF rTempAccum < u_min[m] THEN
            rTempAccum := u_min[m];
        END_IF;

        u_delta[m] := rTempAccum - u_prev[m];
        u_ctrl[m]  := rTempAccum;
    END_FOR;
ELSE
    (* Manual / Sequence Controlled Modes: Maintain previous actuator baseline *)
    FOR m := 1 TO 6 DO
        u_delta[m]    := 0.0;
        u_gradient[m] := 0.0;
    END_FOR;
END_IF;
"""
