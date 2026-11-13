# subsea_boosting_builder/st_phase3_mpc.py

def get_phase3_mpc():
    return """(* ==================================================================================================== *)
(* PHASE 3: RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) WITH UNROLLED PGD OPTIMIZATION               *)
(* 10-Step Prediction Horizon (Np=10), 5-Step Control Horizon (Nc=5), 10 Unrolled PGD Iterations         *)
(* Dynamic Multi-Actuator Coordination: VFD Motor Speed, Fast Kickback Valve, MEG Inhibitor Valve,       *)
(* Barrier Fluid Accumulator Valve, Subsea Production Choke Trim, and Mist Cooling Recycle               *)
(* ==================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------- *)
(* 3.1: Reference Target Trajectory Generation & Linearization Offset Update                            *)
(* ---------------------------------------------------------------------------------------------------- *)
vecX_ref[0] := rTargetSuctionPress_Setpoint_bar - vecX_nominal[0];
vecX_ref[1] := rTargetDischargePress_Setpoint_bar - vecX_nominal[1];
vecX_ref[2] := 0.0; (* Regulate GVF disturbances back to nominal *)
vecX_ref[3] := 0.0; (* Regulate sonic velocity fluctuations back to acoustic nominal *)
vecX_ref[4] := (rTargetDischargePress_Setpoint_bar - rTargetSuctionPress_Setpoint_bar) - vecX_nominal[4];
vecX_ref[5] := 0.0; (* Minimize excess hydraulic absorbed torque *)

(* Dynamic State Tracking Error *)
FOR mIdx := 0 TO 5 DO
    vecX_err[mIdx] := vecX_est[mIdx] - vecX_ref[mIdx];
END_FOR;

(* Seed Trajectory Initial Condition with Current Observer State *)
FOR mIdx := 0 TO 5 DO
    matX_traj[0, mIdx] := vecX_est[mIdx];
END_FOR;

(* Initialize Control Trajectory with Previous Solution (Warm Starting) *)
FOR nStepMPC := 0 TO 8 DO
    FOR mIdx := 0 TO 5 DO
        matU_traj[nStepMPC, mIdx] := matU_traj[nStepMPC + 1, mIdx];
    END_FOR;
END_FOR;
FOR mIdx := 0 TO 5 DO
    matU_traj[9, mIdx] := matU_traj[8, mIdx];
END_FOR;

(* Clamp Warm-Started Trajectory to Physical Box Limits *)
FOR nStepMPC := 0 TO 9 DO
    FOR mIdx := 0 TO 5 DO
        IF matU_traj[nStepMPC, mIdx] < vecU_min[mIdx] THEN
            matU_traj[nStepMPC, mIdx] := vecU_min[mIdx];
        ELSIF matU_traj[nStepMPC, mIdx] > vecU_max[mIdx] THEN
            matU_traj[nStepMPC, mIdx] := vecU_max[mIdx];
        END_IF;
    END_FOR;
END_FOR;

(* ---------------------------------------------------------------------------------------------------- *)
(* 3.2: Unrolled Projected Gradient Descent (PGD) Optimization Loop (10 Iterations)                     *)
(* ---------------------------------------------------------------------------------------------------- *)
FOR nIterMPC := 1 TO 10 DO
    (* -------------------------------------------------------------------------------------------- *)
    (* Step 3.2A: Forward Simulation Rollout of Predictive State Horizon (k = 0 TO 9)              *)
    (* x[k+1] = A * x[k] + B * (u[k] - u_target)                                                    *)
    (* -------------------------------------------------------------------------------------------- *)
    FOR nStepMPC := 0 TO 9 DO
        FOR mIdx := 0 TO 5 DO
            matX_traj[nStepMPC + 1, mIdx] := 0.0;
            (* State Drift: A * x[k] *)
            FOR nIdx := 0 TO 5 DO
                matX_traj[nStepMPC + 1, mIdx] := matX_traj[nStepMPC + 1, mIdx] +
                    (matA[mIdx, nIdx] * matX_traj[nStepMPC, nIdx]);
            END_FOR;

            (* Actuator Control Input Drift: B * (u[k] - u_target) with scaling *)
            matX_traj[nStepMPC + 1, mIdx] := matX_traj[nStepMPC + 1, mIdx] +
                (matB[mIdx, 0] * (matU_traj[nStepMPC, 0] - vecU_target[0]) * 0.001) +
                (matB[mIdx, 1] * (matU_traj[nStepMPC, 1] - vecU_target[1]) * 0.01) +
                (matB[mIdx, 2] * (matU_traj[nStepMPC, 2] - vecU_target[2]) * 0.01) +
                (matB[mIdx, 3] * (matU_traj[nStepMPC, 3] - vecU_target[3]) * 0.01) +
                (matB[mIdx, 4] * (matU_traj[nStepMPC, 4] - vecU_target[4]) * 0.01) +
                (matB[mIdx, 5] * (matU_traj[nStepMPC, 5] - vecU_target[5]) * 0.01);
        END_FOR;
    END_FOR;

    (* -------------------------------------------------------------------------------------------- *)
    (* Step 3.2B: Cost Functional Evaluation (Tracking, Actuation Effort, Slew Rate & Terminal)     *)
    (* -------------------------------------------------------------------------------------------- *)
    rCost_State := 0.0;
    rCost_Control := 0.0;
    rCost_Slew := 0.0;

    FOR nStepMPC := 0 TO 9 DO
        (* State Quadratic Error Cost: e[k]^T * Q * e[k] *)
        FOR mIdx := 0 TO 5 DO
            rCost_State := rCost_State +
                (vecQ_weight[mIdx] * (matX_traj[nStepMPC + 1, mIdx] - vecX_ref[mIdx]) *
                                     (matX_traj[nStepMPC + 1, mIdx] - vecX_ref[mIdx]));
        END_FOR;

        (* Actuator Effort Quadratic Cost: (u[k] - u_target)^T * R * (u[k] - u_target) *)
        rCost_Control := rCost_Control +
            (vecR_weight[0] * ((matU_traj[nStepMPC, 0] - vecU_target[0]) * 0.001) *
                              ((matU_traj[nStepMPC, 0] - vecU_target[0]) * 0.001)) +
            (vecR_weight[1] * ((matU_traj[nStepMPC, 1] - vecU_target[1]) * 0.01) *
                              ((matU_traj[nStepMPC, 1] - vecU_target[1]) * 0.01)) +
            (vecR_weight[2] * ((matU_traj[nStepMPC, 2] - vecU_target[2]) * 0.01) *
                              ((matU_traj[nStepMPC, 2] - vecU_target[2]) * 0.01)) +
            (vecR_weight[3] * ((matU_traj[nStepMPC, 3] - vecU_target[3]) * 0.01) *
                              ((matU_traj[nStepMPC, 3] - vecU_target[3]) * 0.01)) +
            (vecR_weight[4] * ((matU_traj[nStepMPC, 4] - vecU_target[4]) * 0.01) *
                              ((matU_traj[nStepMPC, 4] - vecU_target[4]) * 0.01)) +
            (vecR_weight[5] * ((matU_traj[nStepMPC, 5] - vecU_target[5]) * 0.01) *
                              ((matU_traj[nStepMPC, 5] - vecU_target[5]) * 0.01));

        (* Actuator Slew Rate Quadratic Penalty: (u[k] - u[k-1])^T * R_rate * (u[k] - u[k-1]) *)
        IF nStepMPC = 0 THEN
            rCost_Slew := rCost_Slew +
                (vecR_rate_weight[0] * ((matU_traj[0, 0] - vecU_prev[0]) * 0.001) *
                                       ((matU_traj[0, 0] - vecU_prev[0]) * 0.001)) +
                (vecR_rate_weight[1] * ((matU_traj[0, 1] - vecU_prev[1]) * 0.01) *
                                       ((matU_traj[0, 1] - vecU_prev[1]) * 0.01)) +
                (vecR_rate_weight[2] * ((matU_traj[0, 2] - vecU_prev[2]) * 0.01) *
                                       ((matU_traj[0, 2] - vecU_prev[2]) * 0.01)) +
                (vecR_rate_weight[3] * ((matU_traj[0, 3] - vecU_prev[3]) * 0.01) *
                                       ((matU_traj[0, 3] - vecU_prev[3]) * 0.01)) +
                (vecR_rate_weight[4] * ((matU_traj[0, 4] - vecU_prev[4]) * 0.01) *
                                       ((matU_traj[0, 4] - vecU_prev[4]) * 0.01)) +
                (vecR_rate_weight[5] * ((matU_traj[0, 5] - vecU_prev[5]) * 0.01) *
                                       ((matU_traj[0, 5] - vecU_prev[5]) * 0.01));
        ELSE
            rCost_Slew := rCost_Slew +
                (vecR_rate_weight[0] * ((matU_traj[nStepMPC, 0] - matU_traj[nStepMPC - 1, 0]) * 0.001) *
                                       ((matU_traj[nStepMPC, 0] - matU_traj[nStepMPC - 1, 0]) * 0.001)) +
                (vecR_rate_weight[1] * ((matU_traj[nStepMPC, 1] - matU_traj[nStepMPC - 1, 1]) * 0.01) *
                                       ((matU_traj[nStepMPC, 1] - matU_traj[nStepMPC - 1, 1]) * 0.01)) +
                (vecR_rate_weight[2] * ((matU_traj[nStepMPC, 2] - matU_traj[nStepMPC - 1, 2]) * 0.01) *
                                       ((matU_traj[nStepMPC, 2] - matU_traj[nStepMPC - 1, 2]) * 0.01)) +
                (vecR_rate_weight[3] * ((matU_traj[nStepMPC, 3] - matU_traj[nStepMPC - 1, 3]) * 0.01) *
                                       ((matU_traj[nStepMPC, 3] - matU_traj[nStepMPC - 1, 3]) * 0.01)) +
                (vecR_rate_weight[4] * ((matU_traj[nStepMPC, 4] - matU_traj[nStepMPC - 1, 4]) * 0.01) *
                                       ((matU_traj[nStepMPC, 4] - matU_traj[nStepMPC - 1, 4]) * 0.01)) +
                (vecR_rate_weight[5] * ((matU_traj[nStepMPC, 5] - matU_traj[nStepMPC - 1, 5]) * 0.01) *
                                       ((matU_traj[nStepMPC, 5] - matU_traj[nStepMPC - 1, 5]) * 0.01));
        END_IF;
    END_FOR;

    (* Terminal Lyapunov Stability Penalty: e[10]^T * P * e[10] *)
    rCost_Terminal := 0.0;
    FOR mIdx := 0 TO 5 DO
        rCost_Terminal := rCost_Terminal +
            (vecP_terminal[mIdx] * (matX_traj[10, mIdx] - vecX_ref[mIdx]) *
                                   (matX_traj[10, mIdx] - vecX_ref[mIdx]));
    END_FOR;

    rCost_Total := rCost_State + rCost_Control + rCost_Slew + rCost_Terminal;

    (* -------------------------------------------------------------------------------------------- *)
    (* Step 3.2C: Unrolled Cost Functional Gradient Computation via Adjoint Recurrence              *)
    (* Backpropagation of Terminal & Stage Cost Gradients w.r.t Control Sequence U                   *)
    (* -------------------------------------------------------------------------------------------- *)
    FOR nStepMPC := 0 TO 9 DO
        (* Gradient w.r.t Control Effort R *)
        matGrad_U[nStepMPC, 0] := vecR_weight[0] * (matU_traj[nStepMPC, 0] - vecU_target[0]) * 0.001 * 0.001;
        matGrad_U[nStepMPC, 1] := vecR_weight[1] * (matU_traj[nStepMPC, 1] - vecU_target[1]) * 0.01 * 0.01;
        matGrad_U[nStepMPC, 2] := vecR_weight[2] * (matU_traj[nStepMPC, 2] - vecU_target[2]) * 0.01 * 0.01;
        matGrad_U[nStepMPC, 3] := vecR_weight[3] * (matU_traj[nStepMPC, 3] - vecU_target[3]) * 0.01 * 0.01;
        matGrad_U[nStepMPC, 4] := vecR_weight[4] * (matU_traj[nStepMPC, 4] - vecU_target[4]) * 0.01 * 0.01;
        matGrad_U[nStepMPC, 5] := vecR_weight[5] * (matU_traj[nStepMPC, 5] - vecU_target[5]) * 0.01 * 0.01;

        (* Slew Rate Gradient Components *)
        IF nStepMPC = 0 THEN
            matGrad_U[0, 0] := matGrad_U[0, 0] + (vecR_rate_weight[0] * (matU_traj[0, 0] - vecU_prev[0]) * 0.001 * 0.001);
            matGrad_U[0, 1] := matGrad_U[0, 1] + (vecR_rate_weight[1] * (matU_traj[0, 1] - vecU_prev[1]) * 0.01 * 0.01);
            matGrad_U[0, 2] := matGrad_U[0, 2] + (vecR_rate_weight[2] * (matU_traj[0, 2] - vecU_prev[2]) * 0.01 * 0.01);
            matGrad_U[0, 3] := matGrad_U[0, 3] + (vecR_rate_weight[3] * (matU_traj[0, 3] - vecU_prev[3]) * 0.01 * 0.01);
            matGrad_U[0, 4] := matGrad_U[0, 4] + (vecR_rate_weight[4] * (matU_traj[0, 4] - vecU_prev[4]) * 0.01 * 0.01);
            matGrad_U[0, 5] := matGrad_U[0, 5] + (vecR_rate_weight[5] * (matU_traj[0, 5] - vecU_prev[5]) * 0.01 * 0.01);
        ELSE
            matGrad_U[nStepMPC, 0] := matGrad_U[nStepMPC, 0] +
                (vecR_rate_weight[0] * (matU_traj[nStepMPC, 0] - matU_traj[nStepMPC - 1, 0]) * 0.001 * 0.001);
            matGrad_U[nStepMPC, 1] := matGrad_U[nStepMPC, 1] +
                (vecR_rate_weight[1] * (matU_traj[nStepMPC, 1] - matU_traj[nStepMPC - 1, 1]) * 0.01 * 0.01);
            matGrad_U[nStepMPC, 2] := matGrad_U[nStepMPC, 2] +
                (vecR_rate_weight[2] * (matU_traj[nStepMPC, 2] - matU_traj[nStepMPC - 1, 2]) * 0.01 * 0.01);
            matGrad_U[nStepMPC, 3] := matGrad_U[nStepMPC, 3] +
                (vecR_rate_weight[3] * (matU_traj[nStepMPC, 3] - matU_traj[nStepMPC - 1, 3]) * 0.01 * 0.01);
            matGrad_U[nStepMPC, 4] := matGrad_U[nStepMPC, 4] +
                (vecR_rate_weight[4] * (matU_traj[nStepMPC, 4] - matU_traj[nStepMPC - 1, 4]) * 0.01 * 0.01);
            matGrad_U[nStepMPC, 5] := matGrad_U[nStepMPC, 5] +
                (vecR_rate_weight[5] * (matU_traj[nStepMPC, 5] - matU_traj[nStepMPC - 1, 5]) * 0.01 * 0.01);
        END_IF;

        (* Projected State Gradient Contribution through Matrix B *)
        FOR mIdx := 0 TO 5 DO
            matGrad_U[nStepMPC, 0] := matGrad_U[nStepMPC, 0] +
                (matB[mIdx, 0] * 0.001 * vecQ_weight[mIdx] * (matX_traj[nStepMPC + 1, mIdx] - vecX_ref[mIdx]));
            matGrad_U[nStepMPC, 1] := matGrad_U[nStepMPC, 1] +
                (matB[mIdx, 1] * 0.01 * vecQ_weight[mIdx] * (matX_traj[nStepMPC + 1, mIdx] - vecX_ref[mIdx]));
            matGrad_U[nStepMPC, 2] := matGrad_U[nStepMPC, 2] +
                (matB[mIdx, 2] * 0.01 * vecQ_weight[mIdx] * (matX_traj[nStepMPC + 1, mIdx] - vecX_ref[mIdx]));
            matGrad_U[nStepMPC, 3] := matGrad_U[nStepMPC, 3] +
                (matB[mIdx, 3] * 0.01 * vecQ_weight[mIdx] * (matX_traj[nStepMPC + 1, mIdx] - vecX_ref[mIdx]));
            matGrad_U[nStepMPC, 4] := matGrad_U[nStepMPC, 4] +
                (matB[mIdx, 4] * 0.01 * vecQ_weight[mIdx] * (matX_traj[nStepMPC + 1, mIdx] - vecX_ref[mIdx]));
            matGrad_U[nStepMPC, 5] := matGrad_U[nStepMPC, 5] +
                (matB[mIdx, 5] * 0.01 * vecQ_weight[mIdx] * (matX_traj[nStepMPC + 1, mIdx] - vecX_ref[mIdx]));
        END_FOR;
    END_FOR;

    (* -------------------------------------------------------------------------------------------- *)
    (* Step 3.2D: Projected Gradient Descent Step & Physical Box Constraint Projection             *)
    (* u[k] = Project( u[k] - alpha * grad_u )                                                      *)
    (* -------------------------------------------------------------------------------------------- *)
    FOR nStepMPC := 0 TO 9 DO
        (* Update VFD Motor Speed Trajectory [RPM] *)
        matU_traj[nStepMPC, 0] := matU_traj[nStepMPC, 0] - (rAlpha_step * matGrad_U[nStepMPC, 0] * 8000.0);
        IF matU_traj[nStepMPC, 0] < vecU_min[0] THEN
            matU_traj[nStepMPC, 0] := vecU_min[0];
        ELSIF matU_traj[nStepMPC, 0] > vecU_max[0] THEN
            matU_traj[nStepMPC, 0] := vecU_max[0];
        END_IF;

        (* Update Kickback Recycle Valve Trajectory [%] *)
        matU_traj[nStepMPC, 1] := matU_traj[nStepMPC, 1] - (rAlpha_step * matGrad_U[nStepMPC, 1] * 2500.0);
        IF matU_traj[nStepMPC, 1] < vecU_min[1] THEN
            matU_traj[nStepMPC, 1] := vecU_min[1];
        ELSIF matU_traj[nStepMPC, 1] > vecU_max[1] THEN
            matU_traj[nStepMPC, 1] := vecU_max[1];
        END_IF;

        (* Update MEG Inhibitor Valve Trajectory [%] *)
        matU_traj[nStepMPC, 2] := matU_traj[nStepMPC, 2] - (rAlpha_step * matGrad_U[nStepMPC, 2] * 1200.0);
        IF matU_traj[nStepMPC, 2] < vecU_min[2] THEN
            matU_traj[nStepMPC, 2] := vecU_min[2];
        ELSIF matU_traj[nStepMPC, 2] > vecU_max[2] THEN
            matU_traj[nStepMPC, 2] := vecU_max[2];
        END_IF;

        (* Update Barrier Fluid Accumulator Valve Trajectory [%] *)
        matU_traj[nStepMPC, 3] := matU_traj[nStepMPC, 3] - (rAlpha_step * matGrad_U[nStepMPC, 3] * 800.0);
        IF matU_traj[nStepMPC, 3] < vecU_min[3] THEN
            matU_traj[nStepMPC, 3] := vecU_min[3];
        ELSIF matU_traj[nStepMPC, 3] > vecU_max[3] THEN
            matU_traj[nStepMPC, 3] := vecU_max[3];
        END_IF;

        (* Update Subsea Production Export Choke Trajectory [%] *)
        matU_traj[nStepMPC, 4] := matU_traj[nStepMPC, 4] - (rAlpha_step * matGrad_U[nStepMPC, 4] * 1500.0);
        IF matU_traj[nStepMPC, 4] < vecU_min[4] THEN
            matU_traj[nStepMPC, 4] := vecU_min[4];
        ELSIF matU_traj[nStepMPC, 4] > vecU_max[4] THEN
            matU_traj[nStepMPC, 4] := vecU_max[4];
        END_IF;

        (* Update Mist Cooling Recycle Valve Trajectory [%] *)
        matU_traj[nStepMPC, 5] := matU_traj[nStepMPC, 5] - (rAlpha_step * matGrad_U[nStepMPC, 5] * 1800.0);
        IF matU_traj[nStepMPC, 5] < vecU_min[5] THEN
            matU_traj[nStepMPC, 5] := vecU_min[5];
        ELSIF matU_traj[nStepMPC, 5] > vecU_max[5] THEN
            matU_traj[nStepMPC, 5] := vecU_max[5];
        END_IF;
    END_FOR;
END_FOR;

(* ---------------------------------------------------------------------------------------------------- *)
(* 3.3: First-Step Control Extraction & Actuator Slew Rate Limiter Implementation                       *)
(* ---------------------------------------------------------------------------------------------------- *)
vecU_cmd[0] := matU_traj[0, 0];
vecU_cmd[1] := matU_traj[0, 1];
vecU_cmd[2] := matU_traj[0, 2];
vecU_cmd[3] := matU_traj[0, 3];
vecU_cmd[4] := matU_traj[0, 4];
vecU_cmd[5] := matU_traj[0, 5];

(* Slew Rate Limiter for Each Actuator Channel *)
FOR mIdx := 0 TO 5 DO
    vecU_rate[mIdx] := (vecU_cmd[mIdx] - vecU_prev[mIdx]) / rCycleTime_s;

    IF ABS(vecU_rate[mIdx]) > vecU_slew_max[mIdx] THEN
        IF vecU_rate[mIdx] > 0.0 THEN
            vecU[mIdx] := vecU_prev[mIdx] + (vecU_slew_max[mIdx] * rCycleTime_s);
        ELSE
            vecU[mIdx] := vecU_prev[mIdx] - (vecU_slew_max[mIdx] * rCycleTime_s);
        END_IF;
    ELSE
        vecU[mIdx] := vecU_cmd[mIdx];
    END_IF;

    (* Hard Box Clamp *)
    IF vecU[mIdx] < vecU_min[mIdx] THEN
        vecU[mIdx] := vecU_min[mIdx];
    ELSIF vecU[mIdx] > vecU_max[mIdx] THEN
        vecU[mIdx] := vecU_max[mIdx];
    END_IF;

    vecU_prev[mIdx] := vecU[mIdx];
END_FOR;
"""
