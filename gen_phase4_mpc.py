# -*- coding: utf-8 -*-
"""
Generator module: Phase 4 Receding-Horizon Model Predictive Control (MPC)
"""

def get_phase4_mpc():
    return """(* =========================================================================================== *)
(* PHASE 4: RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) ACTION                             *)
(* =========================================================================================== *)
(* Initialize Horizon Control Move Sequence from Current Commands *)
FOR nHorz_k := 1 TO 5 DO
    FOR nIdx_m := 1 TO 6 DO
        arrMPC_U_Seq[nHorz_k, nIdx_m] := arrU_Cmd[nIdx_m];
    END_FOR;
END_FOR;

(* Multi-Step State Trajectory Prediction over 5-Step Horizon *)
FOR nHorz_k := 1 TO 5 DO
    FOR nIdx_i := 1 TO 8 DO
        rAccumulator := 0.0;
        IF nHorz_k = 1 THEN
            (* Step 1: Propagate from current state x[k] *)
            FOR nIdx_j := 1 TO 8 DO
                rAccumulator := rAccumulator + (arrA[nIdx_i, nIdx_j] * arrX_State[nIdx_j]);
            END_FOR;
            FOR nIdx_m := 1 TO 6 DO
                rAccumulator := rAccumulator + (arrB[nIdx_i, nIdx_m] * arrMPC_U_Seq[1, nIdx_m]);
            END_FOR;
        ELSE
            (* Steps 2..5: Propagate from previous predicted horizon step *)
            FOR nIdx_j := 1 TO 8 DO
                rAccumulator := rAccumulator + (arrA[nIdx_i, nIdx_j] * arrMPC_X_Pred[nHorz_k - 1, nIdx_j]);
            END_FOR;
            FOR nIdx_m := 1 TO 6 DO
                rAccumulator := rAccumulator + (arrB[nIdx_i, nIdx_m] * arrMPC_U_Seq[nHorz_k, nIdx_m]);
            END_FOR;
        END_IF;
        arrMPC_X_Pred[nHorz_k, nIdx_i] := rAccumulator;
    END_FOR;
END_FOR;

(* Quadratic Cost Function Evaluation: J = Sum(x^T Q x + u^T R u + Delta_u^T S Delta_u) + x_N^T P x_N *)
rMPC_CostState := 0.0;
rMPC_CostInput := 0.0;
rMPC_CostSlew := 0.0;
rMPC_CostTerminal := 0.0;

FOR nHorz_k := 1 TO 5 DO
    (* State Tracking Error Penalty: x_k^T * Q * x_k *)
    FOR nIdx_i := 1 TO 8 DO
        rStateError := arrMPC_X_Pred[nHorz_k, nIdx_i];
        rMPC_CostState := rMPC_CostState + (arrQ_Weight[nIdx_i] * rStateError * rStateError);
    END_FOR;
    (* Actuator Energy Penalty: u_k^T * R * u_k *)
    FOR nIdx_m := 1 TO 6 DO
        rInputDiff := arrMPC_U_Seq[nHorz_k, nIdx_m];
        rMPC_CostInput := rMPC_CostInput + (arrR_Weight[nIdx_m] * rInputDiff * rInputDiff);
    END_FOR;
    (* Actuator Slew Rate Penalty: Delta_u_k^T * S * Delta_u_k *)
    FOR nIdx_m := 1 TO 6 DO
        IF nHorz_k = 1 THEN
            rInputDiff := arrMPC_U_Seq[1, nIdx_m] - arrU_Prev[nIdx_m];
        ELSE
            rInputDiff := arrMPC_U_Seq[nHorz_k, nIdx_m] - arrMPC_U_Seq[nHorz_k - 1, nIdx_m];
        END_IF;
        rMPC_CostSlew := rMPC_CostSlew + (arrS_Weight[nIdx_m] * rInputDiff * rInputDiff);
    END_FOR;
END_FOR;

(* Terminal State Cost Penalty: x_N^T * P * x_N *)
FOR nIdx_i := 1 TO 8 DO
    rStateError := arrMPC_X_Pred[5, nIdx_i];
    rMPC_CostTerminal := rMPC_CostTerminal + (arrP_Weight[nIdx_i] * rStateError * rStateError);
END_FOR;

rMPC_CostTotal := rMPC_CostState + rMPC_CostInput + rMPC_CostSlew + rMPC_CostTerminal;

(* Analytical Projected Gradient Evaluation: Nabla_u J *)
FOR nIdx_m := 1 TO 6 DO
    (* Direct Actuator Effort and Slew Gradient Components *)
    arrMPC_Grad[nIdx_m] := (2.0 * arrR_Weight[nIdx_m] * arrU_Cmd[nIdx_m]) +
                           (2.0 * arrS_Weight[nIdx_m] * (arrU_Cmd[nIdx_m] - arrU_Prev[nIdx_m]));
    (* Backpropagated State Error Gradient Components over Horizon *)
    FOR nHorz_k := 1 TO 5 DO
        FOR nIdx_i := 1 TO 8 DO
            arrMPC_Grad[nIdx_m] := arrMPC_Grad[nIdx_m] +
                (2.0 * arrQ_Weight[nIdx_i] * arrMPC_X_Pred[nHorz_k, nIdx_i] * arrB[nIdx_i, nIdx_m]);
        END_FOR;
    END_FOR;
END_FOR;

(* Projected Gradient Descent Optimization with Slew Limiting & Saturation Clipping *)
IF bAutoMpcEnable AND bMasterEnable AND NOT bEmergencyStop THEN
    FOR nIdx_m := 1 TO 6 DO
        (* Gradient Descent Update Move *)
        rAccumulator := arrU_Cmd[nIdx_m] - (arrMPC_StepSize[nIdx_m] * arrMPC_Grad[nIdx_m]);
        
        (* Slew Rate Clamping *)
        rInputDiff := rAccumulator - arrU_Prev[nIdx_m];
        IF rInputDiff > arrDeltaU_Max[nIdx_m] THEN
            rAccumulator := arrU_Prev[nIdx_m] + arrDeltaU_Max[nIdx_m];
        ELSIF rInputDiff < -arrDeltaU_Max[nIdx_m] THEN
            rAccumulator := arrU_Prev[nIdx_m] - arrDeltaU_Max[nIdx_m];
        END_IF;

        (* Box Constraint Saturation *)
        IF rAccumulator > arrU_Max[nIdx_m] THEN
            rAccumulator := arrU_Max[nIdx_m];
        ELSIF rAccumulator < arrU_Min[nIdx_m] THEN
            rAccumulator := arrU_Min[nIdx_m];
        END_IF;

        (* Store Optimized Control Action *)
        arrU_Cmd[nIdx_m] := rAccumulator;
    END_FOR;

    (* Store Previous Step Actuator Vector *)
    FOR nIdx_m := 1 TO 6 DO
        arrU_Prev[nIdx_m] := arrU_Cmd[nIdx_m];
    END_FOR;
END_IF;
"""

print("gen_phase4_mpc ready.")
