# fpso_gen/phase3_mpc.py
def get_phase3():
    return """
(* =====================================================================================================================
 * PHASE 3: RECEDING-HORIZON MPC OPTIMIZATION WITH PROJECTED GRADIENT DESCENT (PGD) & SLEW LIMITS
 * Real-time constrained multi-variable optimization unrolled over prediction horizon Np = 5 steps.
 * Minimizes export pressure tracking error, stabilizes flow, protects 3-stage surge margin (Ss >= 1.10) with asymmetric
 * barrier penalties, and strictly enforces 1.2s pneumatic actuator slew rates (0.833% / 10ms).
 * ===================================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------------------------
 * SUBSECTION 3.1: SETPOINT FORMULATION & INITIALIZATION OF PREDICTION TRAJECTORY
 * --------------------------------------------------------------------------------------------------------------------- *)
rVec_x_sp[1] := 0.0;     (* Suction pressure setpoint deviation (nominal 25.0 bar) *)
rVec_x_sp[2] := 0.0;     (* Discharge pressure setpoint deviation (nominal 250.0 bar) *)
rVec_x_sp[3] := 0.0;     (* Flow rate setpoint deviation (nominal 120.0 mbar orifice DP) *)
rVec_x_sp[4] := 0.0;     (* VFD speed setpoint deviation (nominal 9,800 rpm) *)
rVec_x_sp[5] := -3.0;    (* Export moisture setpoint deviation (aiming for 15.0 ppmv, 3 ppmv below nominal) *)
rVec_x_sp[6] := 0.0;     (* Recycle line inventory setpoint deviation *)

(* Seed the initial prediction state with current observer estimated state *)
FOR iLoopCol := 1 TO 6 DO
    rMPC_x_pred[1, iLoopCol] := rVec_x[iLoopCol];
END_FOR;

(* Seed control horizon with previous control values *)
FOR iLoopHorizon := 1 TO 5 DO
    rMPC_u_pred[iLoopHorizon, 1] := rVec_u[1];
    rMPC_u_pred[iLoopHorizon, 2] := rVec_u[2];
    rMPC_u_pred[iLoopHorizon, 3] := rVec_u[3];
    rMPC_u_pred[iLoopHorizon, 4] := rVec_u[4];
END_FOR;

(* ---------------------------------------------------------------------------------------------------------------------
 * SUBSECTION 3.2: UNROLLED PROJECTED GRADIENT DESCENT (PGD) ITERATIVE OPTIMIZATION LOOP
 * Executes 5 unrolled iterations per 10 ms cycle to achieve quadratic convergence within PLC deterministic scan.
 * --------------------------------------------------------------------------------------------------------------------- *)
FOR iLoopIter := 1 TO 5 DO

    (* Step A: Forward State Rollout Over Prediction Horizon Np = 5 *)
    FOR iLoopHorizon := 2 TO 5 DO
        FOR iLoopRow := 1 TO 6 DO
            rMPC_x_pred[iLoopHorizon, iLoopRow] := 0.0;
            (* Propagate previous state *)
            FOR iLoopCol := 1 TO 6 DO
                rMPC_x_pred[iLoopHorizon, iLoopRow] := rMPC_x_pred[iLoopHorizon, iLoopRow] +
                    (rMatrix_A[iLoopRow, iLoopCol] * rMPC_x_pred[iLoopHorizon - 1, iLoopCol]);
            END_FOR;
            (* Inject control input *)
            FOR iLoopCol := 1 TO 4 DO
                rMPC_x_pred[iLoopHorizon, iLoopRow] := rMPC_x_pred[iLoopHorizon, iLoopRow] +
                    (rMatrix_B[iLoopRow, iLoopCol] * rMPC_u_pred[iLoopHorizon - 1, iLoopCol]);
            END_FOR;
        END_FOR;
    END_FOR;

    (* Step B: Unrolled Gradient Computation with Asymmetric Surge Barrier Penalty *)
    FOR iLoopHorizon := 1 TO 5 DO
        (* Control 1: Stage 1 Anti-Surge Valve (ASV 1) *)
        rMPC_grad[iLoopHorizon, 1] := 0.0;
        FOR iLoopRow := 1 TO 6 DO
            rMPC_grad[iLoopHorizon, 1] := rMPC_grad[iLoopHorizon, 1] +
                (rMatrix_B[iLoopRow, 1] * rMPC_Weight_Q[iLoopRow] * (rMPC_x_pred[iLoopHorizon, iLoopRow] - rVec_x_sp[iLoopRow]));
        END_FOR;
        IF iLoopHorizon = 5 THEN
            FOR iLoopRow := 1 TO 6 DO
                rMPC_grad[iLoopHorizon, 1] := rMPC_grad[iLoopHorizon, 1] +
                    (rMatrix_B[iLoopRow, 1] * rMPC_Weight_P[iLoopRow] * (rMPC_x_pred[5, iLoopRow] - rVec_x_sp[iLoopRow]));
            END_FOR;
        END_IF;
        rMPC_grad[iLoopHorizon, 1] := rMPC_grad[iLoopHorizon, 1] + (rMPC_Weight_R[1] * rMPC_u_pred[iLoopHorizon, 1]);
        IF iLoopHorizon = 1 THEN
            rMPC_grad[iLoopHorizon, 1] := rMPC_grad[iLoopHorizon, 1] +
                (2.0 * rMPC_Weight_S[1] * (rMPC_u_pred[1, 1] - rVec_u_prev[1]));
        ELSE
            rMPC_grad[iLoopHorizon, 1] := rMPC_grad[iLoopHorizon, 1] +
                (2.0 * rMPC_Weight_S[1] * (rMPC_u_pred[iLoopHorizon, 1] - rMPC_u_pred[iLoopHorizon - 1, 1]));
        END_IF;

        (* Stage 1 Surge Proximity Asymmetric Barrier: If surge margin drops below target, force valve open *)
        IF rSurgeMargin_Stg1 < rSurgeMargin_Target THEN
            rMPC_grad[iLoopHorizon, 1] := rMPC_grad[iLoopHorizon, 1] -
                (rMPC_BarrierGain / (0.010 + ((rSurgeMargin_Target - rSurgeMargin_Stg1) * (rSurgeMargin_Target - rSurgeMargin_Stg1))));
        END_IF;

        (* Control 2: Stage 2 Anti-Surge Valve (ASV 2) *)
        rMPC_grad[iLoopHorizon, 2] := 0.0;
        FOR iLoopRow := 1 TO 6 DO
            rMPC_grad[iLoopHorizon, 2] := rMPC_grad[iLoopHorizon, 2] +
                (rMatrix_B[iLoopRow, 2] * rMPC_Weight_Q[iLoopRow] * (rMPC_x_pred[iLoopHorizon, iLoopRow] - rVec_x_sp[iLoopRow]));
        END_FOR;
        IF iLoopHorizon = 5 THEN
            FOR iLoopRow := 1 TO 6 DO
                rMPC_grad[iLoopHorizon, 2] := rMPC_grad[iLoopHorizon, 2] +
                    (rMatrix_B[iLoopRow, 2] * rMPC_Weight_P[iLoopRow] * (rMPC_x_pred[5, iLoopRow] - rVec_x_sp[iLoopRow]));
            END_FOR;
        END_IF;
        rMPC_grad[iLoopHorizon, 2] := rMPC_grad[iLoopHorizon, 2] + (rMPC_Weight_R[2] * rMPC_u_pred[iLoopHorizon, 2]);
        IF iLoopHorizon = 1 THEN
            rMPC_grad[iLoopHorizon, 2] := rMPC_grad[iLoopHorizon, 2] +
                (2.0 * rMPC_Weight_S[2] * (rMPC_u_pred[1, 2] - rVec_u_prev[2]));
        ELSE
            rMPC_grad[iLoopHorizon, 2] := rMPC_grad[iLoopHorizon, 2] +
                (2.0 * rMPC_Weight_S[2] * (rMPC_u_pred[iLoopHorizon, 2] - rMPC_u_pred[iLoopHorizon - 1, 2]));
        END_IF;

        (* Stage 2 Surge Proximity Asymmetric Barrier *)
        IF rSurgeMargin_Stg2 < rSurgeMargin_Target THEN
            rMPC_grad[iLoopHorizon, 2] := rMPC_grad[iLoopHorizon, 2] -
                (rMPC_BarrierGain / (0.010 + ((rSurgeMargin_Target - rSurgeMargin_Stg2) * (rSurgeMargin_Target - rSurgeMargin_Stg2))));
        END_IF;

        (* Control 3: Stage 3 Anti-Surge Valve (ASV 3) *)
        rMPC_grad[iLoopHorizon, 3] := 0.0;
        FOR iLoopRow := 1 TO 6 DO
            rMPC_grad[iLoopHorizon, 3] := rMPC_grad[iLoopHorizon, 3] +
                (rMatrix_B[iLoopRow, 3] * rMPC_Weight_Q[iLoopRow] * (rMPC_x_pred[iLoopHorizon, iLoopRow] - rVec_x_sp[iLoopRow]));
        END_FOR;
        IF iLoopHorizon = 5 THEN
            FOR iLoopRow := 1 TO 6 DO
                rMPC_grad[iLoopHorizon, 3] := rMPC_grad[iLoopHorizon, 3] +
                    (rMatrix_B[iLoopRow, 3] * rMPC_Weight_P[iLoopRow] * (rMPC_x_pred[5, iLoopRow] - rVec_x_sp[iLoopRow]));
            END_FOR;
        END_IF;
        rMPC_grad[iLoopHorizon, 3] := rMPC_grad[iLoopHorizon, 3] + (rMPC_Weight_R[3] * rMPC_u_pred[iLoopHorizon, 3]);
        IF iLoopHorizon = 1 THEN
            rMPC_grad[iLoopHorizon, 3] := rMPC_grad[iLoopHorizon, 3] +
                (2.0 * rMPC_Weight_S[3] * (rMPC_u_pred[1, 3] - rVec_u_prev[3]));
        ELSE
            rMPC_grad[iLoopHorizon, 3] := rMPC_grad[iLoopHorizon, 3] +
                (2.0 * rMPC_Weight_S[3] * (rMPC_u_pred[iLoopHorizon, 3] - rMPC_u_pred[iLoopHorizon - 1, 3]));
        END_IF;

        (* Stage 3 Surge Proximity Asymmetric Barrier *)
        IF rSurgeMargin_Stg3 < rSurgeMargin_Target THEN
            rMPC_grad[iLoopHorizon, 3] := rMPC_grad[iLoopHorizon, 3] -
                (rMPC_BarrierGain / (0.010 + ((rSurgeMargin_Target - rSurgeMargin_Stg3) * (rSurgeMargin_Target - rSurgeMargin_Stg3))));
        END_IF;

        (* Control 4: VFD Motor Speed Setpoint Deviation *)
        rMPC_grad[iLoopHorizon, 4] := 0.0;
        FOR iLoopRow := 1 TO 6 DO
            rMPC_grad[iLoopHorizon, 4] := rMPC_grad[iLoopHorizon, 4] +
                (rMatrix_B[iLoopRow, 4] * rMPC_Weight_Q[iLoopRow] * (rMPC_x_pred[iLoopHorizon, iLoopRow] - rVec_x_sp[iLoopRow]));
        END_FOR;
        IF iLoopHorizon = 5 THEN
            FOR iLoopRow := 1 TO 6 DO
                rMPC_grad[iLoopHorizon, 4] := rMPC_grad[iLoopHorizon, 4] +
                    (rMatrix_B[iLoopRow, 4] * rMPC_Weight_P[iLoopRow] * (rMPC_x_pred[5, iLoopRow] - rVec_x_sp[iLoopRow]));
            END_FOR;
        END_IF;
        rMPC_grad[iLoopHorizon, 4] := rMPC_grad[iLoopHorizon, 4] + (rMPC_Weight_R[4] * rMPC_u_pred[iLoopHorizon, 4]);
        IF iLoopHorizon = 1 THEN
            rMPC_grad[iLoopHorizon, 4] := rMPC_grad[iLoopHorizon, 4] +
                (2.0 * rMPC_Weight_S[4] * (rMPC_u_pred[1, 4] - rVec_u_prev[4]));
        ELSE
            rMPC_grad[iLoopHorizon, 4] := rMPC_grad[iLoopHorizon, 4] +
                (2.0 * rMPC_Weight_S[4] * (rMPC_u_pred[iLoopHorizon, 4] - rMPC_u_pred[iLoopHorizon - 1, 4]));
        END_IF;
    END_FOR;

    (* Step C: Projected Descent Step with Strict Actuator Rate Clamping *)
    FOR iLoopHorizon := 1 TO 5 DO
        (* Update ASV 1 *)
        rMPC_u_pred[iLoopHorizon, 1] := rMPC_u_pred[iLoopHorizon, 1] - (rMPC_StepSize * rMPC_grad[iLoopHorizon, 1]);
        (* Physical Box Constraints [0.0% to 100.0%] *)
        IF rMPC_u_pred[iLoopHorizon, 1] < 0.0 THEN
            rMPC_u_pred[iLoopHorizon, 1] := 0.0;
        ELSIF rMPC_u_pred[iLoopHorizon, 1] > 100.0 THEN
            rMPC_u_pred[iLoopHorizon, 1] := 100.0;
        END_IF;

        (* Update ASV 2 *)
        rMPC_u_pred[iLoopHorizon, 2] := rMPC_u_pred[iLoopHorizon, 2] - (rMPC_StepSize * rMPC_grad[iLoopHorizon, 2]);
        IF rMPC_u_pred[iLoopHorizon, 2] < 0.0 THEN
            rMPC_u_pred[iLoopHorizon, 2] := 0.0;
        ELSIF rMPC_u_pred[iLoopHorizon, 2] > 100.0 THEN
            rMPC_u_pred[iLoopHorizon, 2] := 100.0;
        END_IF;

        (* Update ASV 3 *)
        rMPC_u_pred[iLoopHorizon, 3] := rMPC_u_pred[iLoopHorizon, 3] - (rMPC_StepSize * rMPC_grad[iLoopHorizon, 3]);
        IF rMPC_u_pred[iLoopHorizon, 3] < 0.0 THEN
            rMPC_u_pred[iLoopHorizon, 3] := 0.0;
        ELSIF rMPC_u_pred[iLoopHorizon, 3] > 100.0 THEN
            rMPC_u_pred[iLoopHorizon, 3] := 100.0;
        END_IF;

        (* Update VFD Speed *)
        rMPC_u_pred[iLoopHorizon, 4] := rMPC_u_pred[iLoopHorizon, 4] - (rMPC_StepSize * rMPC_grad[iLoopHorizon, 4]);
        (* Speed Deviation Box Constraints [-1500.0 rpm to +1500.0 rpm] *)
        IF rMPC_u_pred[iLoopHorizon, 4] < -1500.0 THEN
            rMPC_u_pred[iLoopHorizon, 4] := -1500.0;
        ELSIF rMPC_u_pred[iLoopHorizon, 4] > 1500.0 THEN
            rMPC_u_pred[iLoopHorizon, 4] := 1500.0;
        END_IF;
    END_FOR;

END_FOR;

(* ---------------------------------------------------------------------------------------------------------------------
 * SUBSECTION 3.3: EXTRACT RECEDING HORIZON FIRST ELEMENT & APPLY DYNAMIC ACTUATOR SLEW FILTERING
 * --------------------------------------------------------------------------------------------------------------------- *)
(* Store previous control vector for next execution cycle rate penalties *)
rVec_u_prev[1] := rVec_u[1];
rVec_u_prev[2] := rVec_u[2];
rVec_u_prev[3] := rVec_u[3];
rVec_u_prev[4] := rVec_u[4];

(* Stage 1 ASV Rate Clamping: Maximum 0.833% per 10ms cycle (100% in 1.2s) *)
IF (rMPC_u_pred[1, 1] - rVec_u[1]) > rMPC_MaxSlewASV THEN
    rVec_u[1] := rVec_u[1] + rMPC_MaxSlewASV;
ELSIF (rVec_u[1] - rMPC_u_pred[1, 1]) > rMPC_MaxSlewASV THEN
    rVec_u[1] := rVec_u[1] - rMPC_MaxSlewASV;
ELSE
    rVec_u[1] := rMPC_u_pred[1, 1];
END_IF;

(* Stage 2 ASV Rate Clamping *)
IF (rMPC_u_pred[1, 2] - rVec_u[2]) > rMPC_MaxSlewASV THEN
    rVec_u[2] := rVec_u[2] + rMPC_MaxSlewASV;
ELSIF (rVec_u[2] - rMPC_u_pred[1, 2]) > rMPC_MaxSlewASV THEN
    rVec_u[2] := rVec_u[2] - rMPC_MaxSlewASV;
ELSE
    rVec_u[2] := rMPC_u_pred[1, 2];
END_IF;

(* Stage 3 ASV Rate Clamping *)
IF (rMPC_u_pred[1, 3] - rVec_u[3]) > rMPC_MaxSlewASV THEN
    rVec_u[3] := rVec_u[3] + rMPC_MaxSlewASV;
ELSIF (rVec_u[3] - rMPC_u_pred[1, 3]) > rMPC_MaxSlewASV THEN
    rVec_u[3] := rVec_u[3] - rMPC_MaxSlewASV;
ELSE
    rVec_u[3] := rMPC_u_pred[1, 3];
END_IF;

(* VFD Speed Deviation Rate Clamping: Maximum 0.50 rpm per 10ms cycle (50 rpm/s) *)
IF (rMPC_u_pred[1, 4] - rVec_u[4]) > rMPC_MaxSlewVFD THEN
    rVec_u[4] := rVec_u[4] + rMPC_MaxSlewVFD;
ELSIF (rVec_u[4] - rMPC_u_pred[1, 4]) > rMPC_MaxSlewVFD THEN
    rVec_u[4] := rVec_u[4] - rMPC_MaxSlewVFD;
ELSE
    rVec_u[4] := rMPC_u_pred[1, 4];
END_IF;
"""
