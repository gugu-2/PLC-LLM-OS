# mining_flotation_builder/section_phase3_mpc.py
"""
Section: Phase 3 - Receding-Horizon Model Predictive Control (MPC) with 10 Unrolled PGD Iterations
Function Block: FB_Mining_Flotation_RougherScavenger_FrothDepth_ReagentDosing
"""

def get_phase3_code():
    return """(* ========================================================================= *)
(* === PHASE 3: RECEDING-HORIZON MPC OPTIMIZATION WITH 10 UNROLLED PGD    === *)
(* ===          PROJECTED GRADIENT DESCENT & PARETO CURVE ENFORCEMENT    === *)
(* ========================================================================= *)

(* ------------------------------------------------------------------------- *)
(* SUB-SECTION 3.1: REFERENCE SETPOINT VECTOR GENERATION & PARETO SHAPING    *)
(* ------------------------------------------------------------------------- *)
x_ref[1] := rPulpLevel_SP;               (* State 1 Target: Pulp level [mm] *)
x_ref[2] := rFrothDepth_SP;              (* State 2 Target: Froth bed thickness [mm] *)
x_ref[3] := rTargetPH_SP;                (* State 3 Target: Conditioning slurry pH [pH] *)
x_ref[4] := rTargetRecovery_SP;          (* State 4 Target: Rougher copper recovery [%] *)
x_ref[5] := rTargetGrade_Cu_SP;          (* State 5 Target: Concentrate Cu grade [% Cu] *)
x_ref[6] := (rSuperficialGasVelocity_Jg_SP * 5.85) / (rSuperficialGasVelocity_Jg_SP + 1.25); (* Target Air Holdup [%] *)

(* Pareto Curve Trade-Off: Enforce Grade Floor to prevent silicate gangue entrainment *)
IF x_hat[5] < rParetoGradePenaltyThreshold THEN
    (* Exponential penalty scalar multiplier when concentrate grade drops below economic limit *)
    rDynamicGradePenaltyWeight := 1.0 + (rParetoTradeOffSlope * ((rParetoGradePenaltyThreshold - x_hat[5]) / 2.0));
    IF rDynamicGradePenaltyWeight > 6.0 THEN rDynamicGradePenaltyWeight := 6.0; END_IF;
ELSE
    rDynamicGradePenaltyWeight := 1.0;
END_IF;

(* Seed PGD initial candidate with previous control input *)
u_cand[1] := u_prev[1];
u_cand[2] := u_prev[2];
u_cand[3] := u_prev[3];
u_cand[4] := u_prev[4];
u_cand[5] := u_prev[5];

(* Initial state rollout initialized to current estimated state *)
x_rollout[1] := x_hat[1];
x_rollout[2] := x_hat[2];
x_rollout[3] := x_hat[3];
x_rollout[4] := x_hat[4];
x_rollout[5] := x_hat[5];
x_rollout[6] := x_hat[6];

(* ========================================================================= *)
(* UNROLLED PGD ITERATION 1 / 10                                             *)
(* ========================================================================= *)
x_err[1] := x_rollout[1] - x_ref[1];
x_err[2] := x_rollout[2] - x_ref[2];
x_err[3] := x_rollout[3] - x_ref[3];
x_err[4] := x_rollout[4] - x_ref[4];
x_err[5] := (x_rollout[5] - x_ref[5]) * rDynamicGradePenaltyWeight;
x_err[6] := x_rollout[6] - x_ref[6];

(* Adjoint costate vector backward propagation: lambda = P * x_err *)
lambda_costate[1] := (P_Weight[1,1]*x_err[1]) + (P_Weight[1,2]*x_err[2]) + (P_Weight[1,3]*x_err[3]) + (P_Weight[1,4]*x_err[4]) + (P_Weight[1,5]*x_err[5]) + (P_Weight[1,6]*x_err[6]);
lambda_costate[2] := (P_Weight[2,1]*x_err[1]) + (P_Weight[2,2]*x_err[2]) + (P_Weight[2,3]*x_err[3]) + (P_Weight[2,4]*x_err[4]) + (P_Weight[2,5]*x_err[5]) + (P_Weight[2,6]*x_err[6]);
lambda_costate[3] := (P_Weight[3,1]*x_err[1]) + (P_Weight[3,2]*x_err[2]) + (P_Weight[3,3]*x_err[3]) + (P_Weight[3,4]*x_err[4]) + (P_Weight[3,5]*x_err[5]) + (P_Weight[3,6]*x_err[6]);
lambda_costate[4] := (P_Weight[4,1]*x_err[1]) + (P_Weight[4,2]*x_err[2]) + (P_Weight[4,3]*x_err[3]) + (P_Weight[4,4]*x_err[4]) + (P_Weight[4,5]*x_err[5]) + (P_Weight[4,6]*x_err[6]);
lambda_costate[5] := (P_Weight[5,1]*x_err[1]) + (P_Weight[5,2]*x_err[2]) + (P_Weight[5,3]*x_err[3]) + (P_Weight[5,4]*x_err[4]) + (P_Weight[5,5]*x_err[5]) + (P_Weight[5,6]*x_err[6]);
lambda_costate[6] := (P_Weight[6,1]*x_err[1]) + (P_Weight[6,2]*x_err[2]) + (P_Weight[6,3]*x_err[3]) + (P_Weight[6,4]*x_err[4]) + (P_Weight[6,5]*x_err[5]) + (P_Weight[6,6]*x_err[6]);

(* Gradient computation: grad_J = R * u + S * (u - u_prev) + B' * lambda *)
grad_J[1] := (R_Weight[1,1]*u_cand[1]) + (S_Weight[1,1]*(u_cand[1] - u_prev[1])) + (B_Matrix[1,1]*lambda_costate[1]) + (B_Matrix[2,1]*lambda_costate[2]) + (B_Matrix[3,1]*lambda_costate[3]) + (B_Matrix[4,1]*lambda_costate[4]) + (B_Matrix[5,1]*lambda_costate[5]) + (B_Matrix[6,1]*lambda_costate[6]);
grad_J[2] := (R_Weight[2,2]*u_cand[2]) + (S_Weight[2,2]*(u_cand[2] - u_prev[2])) + (B_Matrix[1,2]*lambda_costate[1]) + (B_Matrix[2,2]*lambda_costate[2]) + (B_Matrix[3,2]*lambda_costate[3]) + (B_Matrix[4,2]*lambda_costate[4]) + (B_Matrix[5,2]*lambda_costate[5]) + (B_Matrix[6,2]*lambda_costate[6]);
grad_J[3] := (R_Weight[3,3]*u_cand[3]) + (S_Weight[3,3]*(u_cand[3] - u_prev[3])) + (B_Matrix[1,3]*lambda_costate[1]) + (B_Matrix[2,3]*lambda_costate[2]) + (B_Matrix[3,3]*lambda_costate[3]) + (B_Matrix[4,3]*lambda_costate[4]) + (B_Matrix[5,3]*lambda_costate[5]) + (B_Matrix[6,3]*lambda_costate[6]);
grad_J[4] := (R_Weight[4,4]*u_cand[4]) + (S_Weight[4,4]*(u_cand[4] - u_prev[4])) + (B_Matrix[1,4]*lambda_costate[1]) + (B_Matrix[2,4]*lambda_costate[2]) + (B_Matrix[3,4]*lambda_costate[3]) + (B_Matrix[4,4]*lambda_costate[4]) + (B_Matrix[5,4]*lambda_costate[5]) + (B_Matrix[6,4]*lambda_costate[6]);
grad_J[5] := (R_Weight[5,5]*u_cand[5]) + (S_Weight[5,5]*(u_cand[5] - u_prev[5])) + (B_Matrix[1,5]*lambda_costate[1]) + (B_Matrix[2,5]*lambda_costate[2]) + (B_Matrix[3,5]*lambda_costate[3]) + (B_Matrix[4,5]*lambda_costate[4]) + (B_Matrix[5,5]*lambda_costate[5]) + (B_Matrix[6,5]*lambda_costate[6]);

(* Gradient update & projection onto constraints *)
rTempDelta := (u_cand[1] - (rPGD_StepSize * grad_J[1])) - u_prev[1];
IF rTempDelta < du_min[1] THEN rTempDelta := du_min[1]; ELSIF rTempDelta > du_max[1] THEN rTempDelta := du_max[1]; END_IF;
u_cand[1] := u_prev[1] + rTempDelta;
IF u_cand[1] < u_min[1] THEN u_cand[1] := u_min[1]; ELSIF u_cand[1] > u_max[1] THEN u_cand[1] := u_max[1]; END_IF;

rTempDelta := (u_cand[2] - (rPGD_StepSize * grad_J[2])) - u_prev[2];
IF rTempDelta < du_min[2] THEN rTempDelta := du_min[2]; ELSIF rTempDelta > du_max[2] THEN rTempDelta := du_max[2]; END_IF;
u_cand[2] := u_prev[2] + rTempDelta;
IF u_cand[2] < u_min[2] THEN u_cand[2] := u_min[2]; ELSIF u_cand[2] > u_max[2] THEN u_cand[2] := u_max[2]; END_IF;

rTempDelta := (u_cand[3] - (rPGD_StepSize * grad_J[3])) - u_prev[3];
IF rTempDelta < du_min[3] THEN rTempDelta := du_min[3]; ELSIF rTempDelta > du_max[3] THEN rTempDelta := du_max[3]; END_IF;
u_cand[3] := u_prev[3] + rTempDelta;
IF u_cand[3] < u_min[3] THEN u_cand[3] := u_min[3]; ELSIF u_cand[3] > u_max[3] THEN u_cand[3] := u_max[3]; END_IF;

rTempDelta := (u_cand[4] - (rPGD_StepSize * grad_J[4])) - u_prev[4];
IF rTempDelta < du_min[4] THEN rTempDelta := du_min[4]; ELSIF rTempDelta > du_max[4] THEN rTempDelta := du_max[4]; END_IF;
u_cand[4] := u_prev[4] + rTempDelta;
IF u_cand[4] < u_min[4] THEN u_cand[4] := u_min[4]; ELSIF u_cand[4] > u_max[4] THEN u_cand[4] := u_max[4]; END_IF;

rTempDelta := (u_cand[5] - (rPGD_StepSize * grad_J[5])) - u_prev[5];
IF rTempDelta < du_min[5] THEN rTempDelta := du_min[5]; ELSIF rTempDelta > du_max[5] THEN rTempDelta := du_max[5]; END_IF;
u_cand[5] := u_prev[5] + rTempDelta;
IF u_cand[5] < u_min[5] THEN u_cand[5] := u_min[5]; ELSIF u_cand[5] > u_max[5] THEN u_cand[5] := u_max[5]; END_IF;

(* Forward rollout simulated state *)
x_rollout[1] := (A_Matrix[1,1]*x_hat[1]) + (A_Matrix[1,2]*x_hat[2]) + (A_Matrix[1,3]*x_hat[3]) + (A_Matrix[1,4]*x_hat[4]) + (A_Matrix[1,5]*x_hat[5]) + (A_Matrix[1,6]*x_hat[6]) + (B_Matrix[1,1]*u_cand[1]) + (B_Matrix[1,2]*u_cand[2]) + (B_Matrix[1,3]*u_cand[3]) + (B_Matrix[1,4]*u_cand[4]) + (B_Matrix[1,5]*u_cand[5]);
x_rollout[2] := (A_Matrix[2,1]*x_hat[1]) + (A_Matrix[2,2]*x_hat[2]) + (A_Matrix[2,3]*x_hat[3]) + (A_Matrix[2,4]*x_hat[4]) + (A_Matrix[2,5]*x_hat[5]) + (A_Matrix[2,6]*x_hat[6]) + (B_Matrix[2,1]*u_cand[1]) + (B_Matrix[2,2]*u_cand[2]) + (B_Matrix[2,3]*u_cand[3]) + (B_Matrix[2,4]*u_cand[4]) + (B_Matrix[2,5]*u_cand[5]);
x_rollout[3] := (A_Matrix[3,1]*x_hat[1]) + (A_Matrix[3,2]*x_hat[2]) + (A_Matrix[3,3]*x_hat[3]) + (A_Matrix[3,4]*x_hat[4]) + (A_Matrix[3,5]*x_hat[5]) + (A_Matrix[3,6]*x_hat[6]) + (B_Matrix[3,1]*u_cand[1]) + (B_Matrix[3,2]*u_cand[2]) + (B_Matrix[3,3]*u_cand[3]) + (B_Matrix[3,4]*u_cand[4]) + (B_Matrix[3,5]*u_cand[5]);
x_rollout[4] := (A_Matrix[4,1]*x_hat[1]) + (A_Matrix[4,2]*x_hat[2]) + (A_Matrix[4,3]*x_hat[3]) + (A_Matrix[4,4]*x_hat[4]) + (A_Matrix[4,5]*x_hat[5]) + (A_Matrix[4,6]*x_hat[6]) + (B_Matrix[4,1]*u_cand[1]) + (B_Matrix[4,2]*u_cand[2]) + (B_Matrix[4,3]*u_cand[3]) + (B_Matrix[4,4]*u_cand[4]) + (B_Matrix[4,5]*u_cand[5]);
x_rollout[5] := (A_Matrix[5,1]*x_hat[1]) + (A_Matrix[5,2]*x_hat[2]) + (A_Matrix[5,3]*x_hat[3]) + (A_Matrix[5,4]*x_hat[4]) + (A_Matrix[5,5]*x_hat[5]) + (A_Matrix[5,6]*x_hat[6]) + (B_Matrix[5,1]*u_cand[1]) + (B_Matrix[5,2]*u_cand[2]) + (B_Matrix[5,3]*u_cand[3]) + (B_Matrix[5,4]*u_cand[4]) + (B_Matrix[5,5]*u_cand[5]);
x_rollout[6] := (A_Matrix[6,1]*x_hat[1]) + (A_Matrix[6,2]*x_hat[2]) + (A_Matrix[6,3]*x_hat[3]) + (A_Matrix[6,4]*x_hat[4]) + (A_Matrix[6,5]*x_hat[5]) + (A_Matrix[6,6]*x_hat[6]) + (B_Matrix[6,1]*u_cand[1]) + (B_Matrix[6,2]*u_cand[2]) + (B_Matrix[6,3]*u_cand[3]) + (B_Matrix[6,4]*u_cand[4]) + (B_Matrix[6,5]*u_cand[5]);


(* ========================================================================= *)
(* UNROLLED PGD ITERATION 2 / 10                                             *)
(* ========================================================================= *)
x_err[1] := x_rollout[1] - x_ref[1];
x_err[2] := x_rollout[2] - x_ref[2];
x_err[3] := x_rollout[3] - x_ref[3];
x_err[4] := x_rollout[4] - x_ref[4];
x_err[5] := (x_rollout[5] - x_ref[5]) * rDynamicGradePenaltyWeight;
x_err[6] := x_rollout[6] - x_ref[6];

lambda_costate[1] := (P_Weight[1,1]*x_err[1]) + (P_Weight[1,2]*x_err[2]) + (P_Weight[1,3]*x_err[3]) + (P_Weight[1,4]*x_err[4]) + (P_Weight[1,5]*x_err[5]) + (P_Weight[1,6]*x_err[6]);
lambda_costate[2] := (P_Weight[2,1]*x_err[1]) + (P_Weight[2,2]*x_err[2]) + (P_Weight[2,3]*x_err[3]) + (P_Weight[2,4]*x_err[4]) + (P_Weight[2,5]*x_err[5]) + (P_Weight[2,6]*x_err[6]);
lambda_costate[3] := (P_Weight[3,1]*x_err[1]) + (P_Weight[3,2]*x_err[2]) + (P_Weight[3,3]*x_err[3]) + (P_Weight[3,4]*x_err[4]) + (P_Weight[3,5]*x_err[5]) + (P_Weight[3,6]*x_err[6]);
lambda_costate[4] := (P_Weight[4,1]*x_err[1]) + (P_Weight[4,2]*x_err[2]) + (P_Weight[4,3]*x_err[3]) + (P_Weight[4,4]*x_err[4]) + (P_Weight[4,5]*x_err[5]) + (P_Weight[4,6]*x_err[6]);
lambda_costate[5] := (P_Weight[5,1]*x_err[1]) + (P_Weight[5,2]*x_err[2]) + (P_Weight[5,3]*x_err[3]) + (P_Weight[5,4]*x_err[4]) + (P_Weight[5,5]*x_err[5]) + (P_Weight[5,6]*x_err[6]);
lambda_costate[6] := (P_Weight[6,1]*x_err[1]) + (P_Weight[6,2]*x_err[2]) + (P_Weight[6,3]*x_err[3]) + (P_Weight[6,4]*x_err[4]) + (P_Weight[6,5]*x_err[5]) + (P_Weight[6,6]*x_err[6]);

grad_J[1] := (R_Weight[1,1]*u_cand[1]) + (S_Weight[1,1]*(u_cand[1] - u_prev[1])) + (B_Matrix[1,1]*lambda_costate[1]) + (B_Matrix[2,1]*lambda_costate[2]) + (B_Matrix[3,1]*lambda_costate[3]) + (B_Matrix[4,1]*lambda_costate[4]) + (B_Matrix[5,1]*lambda_costate[5]) + (B_Matrix[6,1]*lambda_costate[6]);
grad_J[2] := (R_Weight[2,2]*u_cand[2]) + (S_Weight[2,2]*(u_cand[2] - u_prev[2])) + (B_Matrix[1,2]*lambda_costate[1]) + (B_Matrix[2,2]*lambda_costate[2]) + (B_Matrix[3,2]*lambda_costate[3]) + (B_Matrix[4,2]*lambda_costate[4]) + (B_Matrix[5,2]*lambda_costate[5]) + (B_Matrix[6,2]*lambda_costate[6]);
grad_J[3] := (R_Weight[3,3]*u_cand[3]) + (S_Weight[3,3]*(u_cand[3] - u_prev[3])) + (B_Matrix[1,3]*lambda_costate[1]) + (B_Matrix[2,3]*lambda_costate[2]) + (B_Matrix[3,3]*lambda_costate[3]) + (B_Matrix[4,3]*lambda_costate[4]) + (B_Matrix[5,3]*lambda_costate[5]) + (B_Matrix[6,3]*lambda_costate[6]);
grad_J[4] := (R_Weight[4,4]*u_cand[4]) + (S_Weight[4,4]*(u_cand[4] - u_prev[4])) + (B_Matrix[1,4]*lambda_costate[1]) + (B_Matrix[2,4]*lambda_costate[2]) + (B_Matrix[3,4]*lambda_costate[3]) + (B_Matrix[4,4]*lambda_costate[4]) + (B_Matrix[5,4]*lambda_costate[5]) + (B_Matrix[6,4]*lambda_costate[6]);
grad_J[5] := (R_Weight[5,5]*u_cand[5]) + (S_Weight[5,5]*(u_cand[5] - u_prev[5])) + (B_Matrix[1,5]*lambda_costate[1]) + (B_Matrix[2,5]*lambda_costate[2]) + (B_Matrix[3,5]*lambda_costate[3]) + (B_Matrix[4,5]*lambda_costate[4]) + (B_Matrix[5,5]*lambda_costate[5]) + (B_Matrix[6,5]*lambda_costate[6]);

rTempDelta := (u_cand[1] - (rPGD_StepSize * grad_J[1])) - u_prev[1];
IF rTempDelta < du_min[1] THEN rTempDelta := du_min[1]; ELSIF rTempDelta > du_max[1] THEN rTempDelta := du_max[1]; END_IF;
u_cand[1] := u_prev[1] + rTempDelta;
IF u_cand[1] < u_min[1] THEN u_cand[1] := u_min[1]; ELSIF u_cand[1] > u_max[1] THEN u_cand[1] := u_max[1]; END_IF;

rTempDelta := (u_cand[2] - (rPGD_StepSize * grad_J[2])) - u_prev[2];
IF rTempDelta < du_min[2] THEN rTempDelta := du_min[2]; ELSIF rTempDelta > du_max[2] THEN rTempDelta := du_max[2]; END_IF;
u_cand[2] := u_prev[2] + rTempDelta;
IF u_cand[2] < u_min[2] THEN u_cand[2] := u_min[2]; ELSIF u_cand[2] > u_max[2] THEN u_cand[2] := u_max[2]; END_IF;

rTempDelta := (u_cand[3] - (rPGD_StepSize * grad_J[3])) - u_prev[3];
IF rTempDelta < du_min[3] THEN rTempDelta := du_min[3]; ELSIF rTempDelta > du_max[3] THEN rTempDelta := du_max[3]; END_IF;
u_cand[3] := u_prev[3] + rTempDelta;
IF u_cand[3] < u_min[3] THEN u_cand[3] := u_min[3]; ELSIF u_cand[3] > u_max[3] THEN u_cand[3] := u_max[3]; END_IF;

rTempDelta := (u_cand[4] - (rPGD_StepSize * grad_J[4])) - u_prev[4];
IF rTempDelta < du_min[4] THEN rTempDelta := du_min[4]; ELSIF rTempDelta > du_max[4] THEN rTempDelta := du_max[4]; END_IF;
u_cand[4] := u_prev[4] + rTempDelta;
IF u_cand[4] < u_min[4] THEN u_cand[4] := u_min[4]; ELSIF u_cand[4] > u_max[4] THEN u_cand[4] := u_max[4]; END_IF;

rTempDelta := (u_cand[5] - (rPGD_StepSize * grad_J[5])) - u_prev[5];
IF rTempDelta < du_min[5] THEN rTempDelta := du_min[5]; ELSIF rTempDelta > du_max[5] THEN rTempDelta := du_max[5]; END_IF;
u_cand[5] := u_prev[5] + rTempDelta;
IF u_cand[5] < u_min[5] THEN u_cand[5] := u_min[5]; ELSIF u_cand[5] > u_max[5] THEN u_cand[5] := u_max[5]; END_IF;

x_rollout[1] := (A_Matrix[1,1]*x_hat[1]) + (A_Matrix[1,2]*x_hat[2]) + (A_Matrix[1,3]*x_hat[3]) + (A_Matrix[1,4]*x_hat[4]) + (A_Matrix[1,5]*x_hat[5]) + (A_Matrix[1,6]*x_hat[6]) + (B_Matrix[1,1]*u_cand[1]) + (B_Matrix[1,2]*u_cand[2]) + (B_Matrix[1,3]*u_cand[3]) + (B_Matrix[1,4]*u_cand[4]) + (B_Matrix[1,5]*u_cand[5]);
x_rollout[2] := (A_Matrix[2,1]*x_hat[1]) + (A_Matrix[2,2]*x_hat[2]) + (A_Matrix[2,3]*x_hat[3]) + (A_Matrix[2,4]*x_hat[4]) + (A_Matrix[2,5]*x_hat[5]) + (A_Matrix[2,6]*x_hat[6]) + (B_Matrix[2,1]*u_cand[1]) + (B_Matrix[2,2]*u_cand[2]) + (B_Matrix[2,3]*u_cand[3]) + (B_Matrix[2,4]*u_cand[4]) + (B_Matrix[2,5]*u_cand[5]);
x_rollout[3] := (A_Matrix[3,1]*x_hat[1]) + (A_Matrix[3,2]*x_hat[2]) + (A_Matrix[3,3]*x_hat[3]) + (A_Matrix[3,4]*x_hat[4]) + (A_Matrix[3,5]*x_hat[5]) + (A_Matrix[3,6]*x_hat[6]) + (B_Matrix[3,1]*u_cand[1]) + (B_Matrix[3,2]*u_cand[2]) + (B_Matrix[3,3]*u_cand[3]) + (B_Matrix[3,4]*u_cand[4]) + (B_Matrix[3,5]*u_cand[5]);
x_rollout[4] := (A_Matrix[4,1]*x_hat[1]) + (A_Matrix[4,2]*x_hat[2]) + (A_Matrix[4,3]*x_hat[3]) + (A_Matrix[4,4]*x_hat[4]) + (A_Matrix[4,5]*x_hat[5]) + (A_Matrix[4,6]*x_hat[6]) + (B_Matrix[4,1]*u_cand[1]) + (B_Matrix[4,2]*u_cand[2]) + (B_Matrix[4,3]*u_cand[3]) + (B_Matrix[4,4]*u_cand[4]) + (B_Matrix[4,5]*u_cand[5]);
x_rollout[5] := (A_Matrix[5,1]*x_hat[1]) + (A_Matrix[5,2]*x_hat[2]) + (A_Matrix[5,3]*x_hat[3]) + (A_Matrix[5,4]*x_hat[4]) + (A_Matrix[5,5]*x_hat[5]) + (A_Matrix[5,6]*x_hat[6]) + (B_Matrix[5,1]*u_cand[1]) + (B_Matrix[5,2]*u_cand[2]) + (B_Matrix[5,3]*u_cand[3]) + (B_Matrix[5,4]*u_cand[4]) + (B_Matrix[5,5]*u_cand[5]);
x_rollout[6] := (A_Matrix[6,1]*x_hat[1]) + (A_Matrix[6,2]*x_hat[2]) + (A_Matrix[6,3]*x_hat[3]) + (A_Matrix[6,4]*x_hat[4]) + (A_Matrix[6,5]*x_hat[5]) + (A_Matrix[6,6]*x_hat[6]) + (B_Matrix[6,1]*u_cand[1]) + (B_Matrix[6,2]*u_cand[2]) + (B_Matrix[6,3]*u_cand[3]) + (B_Matrix[6,4]*u_cand[4]) + (B_Matrix[6,5]*u_cand[5]);


(* ========================================================================= *)
(* UNROLLED PGD ITERATION 3 / 10                                             *)
(* ========================================================================= *)
x_err[1] := x_rollout[1] - x_ref[1];
x_err[2] := x_rollout[2] - x_ref[2];
x_err[3] := x_rollout[3] - x_ref[3];
x_err[4] := x_rollout[4] - x_ref[4];
x_err[5] := (x_rollout[5] - x_ref[5]) * rDynamicGradePenaltyWeight;
x_err[6] := x_rollout[6] - x_ref[6];

lambda_costate[1] := (P_Weight[1,1]*x_err[1]) + (P_Weight[1,2]*x_err[2]) + (P_Weight[1,3]*x_err[3]) + (P_Weight[1,4]*x_err[4]) + (P_Weight[1,5]*x_err[5]) + (P_Weight[1,6]*x_err[6]);
lambda_costate[2] := (P_Weight[2,1]*x_err[1]) + (P_Weight[2,2]*x_err[2]) + (P_Weight[2,3]*x_err[3]) + (P_Weight[2,4]*x_err[4]) + (P_Weight[2,5]*x_err[5]) + (P_Weight[2,6]*x_err[6]);
lambda_costate[3] := (P_Weight[3,1]*x_err[1]) + (P_Weight[3,2]*x_err[2]) + (P_Weight[3,3]*x_err[3]) + (P_Weight[3,4]*x_err[4]) + (P_Weight[3,5]*x_err[5]) + (P_Weight[3,6]*x_err[6]);
lambda_costate[4] := (P_Weight[4,1]*x_err[1]) + (P_Weight[4,2]*x_err[2]) + (P_Weight[4,3]*x_err[3]) + (P_Weight[4,4]*x_err[4]) + (P_Weight[4,5]*x_err[5]) + (P_Weight[4,6]*x_err[6]);
lambda_costate[5] := (P_Weight[5,1]*x_err[1]) + (P_Weight[5,2]*x_err[2]) + (P_Weight[5,3]*x_err[3]) + (P_Weight[5,4]*x_err[4]) + (P_Weight[5,5]*x_err[5]) + (P_Weight[5,6]*x_err[6]);
lambda_costate[6] := (P_Weight[6,1]*x_err[1]) + (P_Weight[6,2]*x_err[2]) + (P_Weight[6,3]*x_err[3]) + (P_Weight[6,4]*x_err[4]) + (P_Weight[6,5]*x_err[5]) + (P_Weight[6,6]*x_err[6]);

grad_J[1] := (R_Weight[1,1]*u_cand[1]) + (S_Weight[1,1]*(u_cand[1] - u_prev[1])) + (B_Matrix[1,1]*lambda_costate[1]) + (B_Matrix[2,1]*lambda_costate[2]) + (B_Matrix[3,1]*lambda_costate[3]) + (B_Matrix[4,1]*lambda_costate[4]) + (B_Matrix[5,1]*lambda_costate[5]) + (B_Matrix[6,1]*lambda_costate[6]);
grad_J[2] := (R_Weight[2,2]*u_cand[2]) + (S_Weight[2,2]*(u_cand[2] - u_prev[2])) + (B_Matrix[1,2]*lambda_costate[1]) + (B_Matrix[2,2]*lambda_costate[2]) + (B_Matrix[3,2]*lambda_costate[3]) + (B_Matrix[4,2]*lambda_costate[4]) + (B_Matrix[5,2]*lambda_costate[5]) + (B_Matrix[6,2]*lambda_costate[6]);
grad_J[3] := (R_Weight[3,3]*u_cand[3]) + (S_Weight[3,3]*(u_cand[3] - u_prev[3])) + (B_Matrix[1,3]*lambda_costate[1]) + (B_Matrix[2,3]*lambda_costate[2]) + (B_Matrix[3,3]*lambda_costate[3]) + (B_Matrix[4,3]*lambda_costate[4]) + (B_Matrix[5,3]*lambda_costate[5]) + (B_Matrix[6,3]*lambda_costate[6]);
grad_J[4] := (R_Weight[4,4]*u_cand[4]) + (S_Weight[4,4]*(u_cand[4] - u_prev[4])) + (B_Matrix[1,4]*lambda_costate[1]) + (B_Matrix[2,4]*lambda_costate[2]) + (B_Matrix[3,4]*lambda_costate[3]) + (B_Matrix[4,4]*lambda_costate[4]) + (B_Matrix[5,4]*lambda_costate[5]) + (B_Matrix[6,4]*lambda_costate[6]);
grad_J[5] := (R_Weight[5,5]*u_cand[5]) + (S_Weight[5,5]*(u_cand[5] - u_prev[5])) + (B_Matrix[1,5]*lambda_costate[1]) + (B_Matrix[2,5]*lambda_costate[2]) + (B_Matrix[3,5]*lambda_costate[3]) + (B_Matrix[4,5]*lambda_costate[4]) + (B_Matrix[5,5]*lambda_costate[5]) + (B_Matrix[6,5]*lambda_costate[6]);

rTempDelta := (u_cand[1] - (rPGD_StepSize * grad_J[1])) - u_prev[1];
IF rTempDelta < du_min[1] THEN rTempDelta := du_min[1]; ELSIF rTempDelta > du_max[1] THEN rTempDelta := du_max[1]; END_IF;
u_cand[1] := u_prev[1] + rTempDelta;
IF u_cand[1] < u_min[1] THEN u_cand[1] := u_min[1]; ELSIF u_cand[1] > u_max[1] THEN u_cand[1] := u_max[1]; END_IF;

rTempDelta := (u_cand[2] - (rPGD_StepSize * grad_J[2])) - u_prev[2];
IF rTempDelta < du_min[2] THEN rTempDelta := du_min[2]; ELSIF rTempDelta > du_max[2] THEN rTempDelta := du_max[2]; END_IF;
u_cand[2] := u_prev[2] + rTempDelta;
IF u_cand[2] < u_min[2] THEN u_cand[2] := u_min[2]; ELSIF u_cand[2] > u_max[2] THEN u_cand[2] := u_max[2]; END_IF;

rTempDelta := (u_cand[3] - (rPGD_StepSize * grad_J[3])) - u_prev[3];
IF rTempDelta < du_min[3] THEN rTempDelta := du_min[3]; ELSIF rTempDelta > du_max[3] THEN rTempDelta := du_max[3]; END_IF;
u_cand[3] := u_prev[3] + rTempDelta;
IF u_cand[3] < u_min[3] THEN u_cand[3] := u_min[3]; ELSIF u_cand[3] > u_max[3] THEN u_cand[3] := u_max[3]; END_IF;

rTempDelta := (u_cand[4] - (rPGD_StepSize * grad_J[4])) - u_prev[4];
IF rTempDelta < du_min[4] THEN rTempDelta := du_min[4]; ELSIF rTempDelta > du_max[4] THEN rTempDelta := du_max[4]; END_IF;
u_cand[4] := u_prev[4] + rTempDelta;
IF u_cand[4] < u_min[4] THEN u_cand[4] := u_min[4]; ELSIF u_cand[4] > u_max[4] THEN u_cand[4] := u_max[4]; END_IF;

rTempDelta := (u_cand[5] - (rPGD_StepSize * grad_J[5])) - u_prev[5];
IF rTempDelta < du_min[5] THEN rTempDelta := du_min[5]; ELSIF rTempDelta > du_max[5] THEN rTempDelta := du_max[5]; END_IF;
u_cand[5] := u_prev[5] + rTempDelta;
IF u_cand[5] < u_min[5] THEN u_cand[5] := u_min[5]; ELSIF u_cand[5] > u_max[5] THEN u_cand[5] := u_max[5]; END_IF;

x_rollout[1] := (A_Matrix[1,1]*x_hat[1]) + (A_Matrix[1,2]*x_hat[2]) + (A_Matrix[1,3]*x_hat[3]) + (A_Matrix[1,4]*x_hat[4]) + (A_Matrix[1,5]*x_hat[5]) + (A_Matrix[1,6]*x_hat[6]) + (B_Matrix[1,1]*u_cand[1]) + (B_Matrix[1,2]*u_cand[2]) + (B_Matrix[1,3]*u_cand[3]) + (B_Matrix[1,4]*u_cand[4]) + (B_Matrix[1,5]*u_cand[5]);
x_rollout[2] := (A_Matrix[2,1]*x_hat[1]) + (A_Matrix[2,2]*x_hat[2]) + (A_Matrix[2,3]*x_hat[3]) + (A_Matrix[2,4]*x_hat[4]) + (A_Matrix[2,5]*x_hat[5]) + (A_Matrix[2,6]*x_hat[6]) + (B_Matrix[2,1]*u_cand[1]) + (B_Matrix[2,2]*u_cand[2]) + (B_Matrix[2,3]*u_cand[3]) + (B_Matrix[2,4]*u_cand[4]) + (B_Matrix[2,5]*u_cand[5]);
x_rollout[3] := (A_Matrix[3,1]*x_hat[1]) + (A_Matrix[3,2]*x_hat[2]) + (A_Matrix[3,3]*x_hat[3]) + (A_Matrix[3,4]*x_hat[4]) + (A_Matrix[3,5]*x_hat[5]) + (A_Matrix[3,6]*x_hat[6]) + (B_Matrix[3,1]*u_cand[1]) + (B_Matrix[3,2]*u_cand[2]) + (B_Matrix[3,3]*u_cand[3]) + (B_Matrix[3,4]*u_cand[4]) + (B_Matrix[3,5]*u_cand[5]);
x_rollout[4] := (A_Matrix[4,1]*x_hat[1]) + (A_Matrix[4,2]*x_hat[2]) + (A_Matrix[4,3]*x_hat[3]) + (A_Matrix[4,4]*x_hat[4]) + (A_Matrix[4,5]*x_hat[5]) + (A_Matrix[4,6]*x_hat[6]) + (B_Matrix[4,1]*u_cand[1]) + (B_Matrix[4,2]*u_cand[2]) + (B_Matrix[4,3]*u_cand[3]) + (B_Matrix[4,4]*u_cand[4]) + (B_Matrix[4,5]*u_cand[5]);
x_rollout[5] := (A_Matrix[5,1]*x_hat[1]) + (A_Matrix[5,2]*x_hat[2]) + (A_Matrix[5,3]*x_hat[3]) + (A_Matrix[5,4]*x_hat[4]) + (A_Matrix[5,5]*x_hat[5]) + (A_Matrix[5,6]*x_hat[6]) + (B_Matrix[5,1]*u_cand[1]) + (B_Matrix[5,2]*u_cand[2]) + (B_Matrix[5,3]*u_cand[3]) + (B_Matrix[5,4]*u_cand[4]) + (B_Matrix[5,5]*u_cand[5]);
x_rollout[6] := (A_Matrix[6,1]*x_hat[1]) + (A_Matrix[6,2]*x_hat[2]) + (A_Matrix[6,3]*x_hat[3]) + (A_Matrix[6,4]*x_hat[4]) + (A_Matrix[6,5]*x_hat[5]) + (A_Matrix[6,6]*x_hat[6]) + (B_Matrix[6,1]*u_cand[1]) + (B_Matrix[6,2]*u_cand[2]) + (B_Matrix[6,3]*u_cand[3]) + (B_Matrix[6,4]*u_cand[4]) + (B_Matrix[6,5]*u_cand[5]);


(* ========================================================================= *)
(* UNROLLED PGD ITERATION 4 / 10                                             *)
(* ========================================================================= *)
x_err[1] := x_rollout[1] - x_ref[1];
x_err[2] := x_rollout[2] - x_ref[2];
x_err[3] := x_rollout[3] - x_ref[3];
x_err[4] := x_rollout[4] - x_ref[4];
x_err[5] := (x_rollout[5] - x_ref[5]) * rDynamicGradePenaltyWeight;
x_err[6] := x_rollout[6] - x_ref[6];

lambda_costate[1] := (P_Weight[1,1]*x_err[1]) + (P_Weight[1,2]*x_err[2]) + (P_Weight[1,3]*x_err[3]) + (P_Weight[1,4]*x_err[4]) + (P_Weight[1,5]*x_err[5]) + (P_Weight[1,6]*x_err[6]);
lambda_costate[2] := (P_Weight[2,1]*x_err[1]) + (P_Weight[2,2]*x_err[2]) + (P_Weight[2,3]*x_err[3]) + (P_Weight[2,4]*x_err[4]) + (P_Weight[2,5]*x_err[5]) + (P_Weight[2,6]*x_err[6]);
lambda_costate[3] := (P_Weight[3,1]*x_err[1]) + (P_Weight[3,2]*x_err[2]) + (P_Weight[3,3]*x_err[3]) + (P_Weight[3,4]*x_err[4]) + (P_Weight[3,5]*x_err[5]) + (P_Weight[3,6]*x_err[6]);
lambda_costate[4] := (P_Weight[4,1]*x_err[1]) + (P_Weight[4,2]*x_err[2]) + (P_Weight[4,3]*x_err[3]) + (P_Weight[4,4]*x_err[4]) + (P_Weight[4,5]*x_err[5]) + (P_Weight[4,6]*x_err[6]);
lambda_costate[5] := (P_Weight[5,1]*x_err[1]) + (P_Weight[5,2]*x_err[2]) + (P_Weight[5,3]*x_err[3]) + (P_Weight[5,4]*x_err[4]) + (P_Weight[5,5]*x_err[5]) + (P_Weight[5,6]*x_err[6]);
lambda_costate[6] := (P_Weight[6,1]*x_err[1]) + (P_Weight[6,2]*x_err[2]) + (P_Weight[6,3]*x_err[3]) + (P_Weight[6,4]*x_err[4]) + (P_Weight[6,5]*x_err[5]) + (P_Weight[6,6]*x_err[6]);

grad_J[1] := (R_Weight[1,1]*u_cand[1]) + (S_Weight[1,1]*(u_cand[1] - u_prev[1])) + (B_Matrix[1,1]*lambda_costate[1]) + (B_Matrix[2,1]*lambda_costate[2]) + (B_Matrix[3,1]*lambda_costate[3]) + (B_Matrix[4,1]*lambda_costate[4]) + (B_Matrix[5,1]*lambda_costate[5]) + (B_Matrix[6,1]*lambda_costate[6]);
grad_J[2] := (R_Weight[2,2]*u_cand[2]) + (S_Weight[2,2]*(u_cand[2] - u_prev[2])) + (B_Matrix[1,2]*lambda_costate[1]) + (B_Matrix[2,2]*lambda_costate[2]) + (B_Matrix[3,2]*lambda_costate[3]) + (B_Matrix[4,2]*lambda_costate[4]) + (B_Matrix[5,2]*lambda_costate[5]) + (B_Matrix[6,2]*lambda_costate[6]);
grad_J[3] := (R_Weight[3,3]*u_cand[3]) + (S_Weight[3,3]*(u_cand[3] - u_prev[3])) + (B_Matrix[1,3]*lambda_costate[1]) + (B_Matrix[2,3]*lambda_costate[2]) + (B_Matrix[3,3]*lambda_costate[3]) + (B_Matrix[4,3]*lambda_costate[4]) + (B_Matrix[5,3]*lambda_costate[5]) + (B_Matrix[6,3]*lambda_costate[6]);
grad_J[4] := (R_Weight[4,4]*u_cand[4]) + (S_Weight[4,4]*(u_cand[4] - u_prev[4])) + (B_Matrix[1,4]*lambda_costate[1]) + (B_Matrix[2,4]*lambda_costate[2]) + (B_Matrix[3,4]*lambda_costate[3]) + (B_Matrix[4,4]*lambda_costate[4]) + (B_Matrix[5,4]*lambda_costate[5]) + (B_Matrix[6,4]*lambda_costate[6]);
grad_J[5] := (R_Weight[5,5]*u_cand[5]) + (S_Weight[5,5]*(u_cand[5] - u_prev[5])) + (B_Matrix[1,5]*lambda_costate[1]) + (B_Matrix[2,5]*lambda_costate[2]) + (B_Matrix[3,5]*lambda_costate[3]) + (B_Matrix[4,5]*lambda_costate[4]) + (B_Matrix[5,5]*lambda_costate[5]) + (B_Matrix[6,5]*lambda_costate[6]);

rTempDelta := (u_cand[1] - (rPGD_StepSize * grad_J[1])) - u_prev[1];
IF rTempDelta < du_min[1] THEN rTempDelta := du_min[1]; ELSIF rTempDelta > du_max[1] THEN rTempDelta := du_max[1]; END_IF;
u_cand[1] := u_prev[1] + rTempDelta;
IF u_cand[1] < u_min[1] THEN u_cand[1] := u_min[1]; ELSIF u_cand[1] > u_max[1] THEN u_cand[1] := u_max[1]; END_IF;

rTempDelta := (u_cand[2] - (rPGD_StepSize * grad_J[2])) - u_prev[2];
IF rTempDelta < du_min[2] THEN rTempDelta := du_min[2]; ELSIF rTempDelta > du_max[2] THEN rTempDelta := du_max[2]; END_IF;
u_cand[2] := u_prev[2] + rTempDelta;
IF u_cand[2] < u_min[2] THEN u_cand[2] := u_min[2]; ELSIF u_cand[2] > u_max[2] THEN u_cand[2] := u_max[2]; END_IF;

rTempDelta := (u_cand[3] - (rPGD_StepSize * grad_J[3])) - u_prev[3];
IF rTempDelta < du_min[3] THEN rTempDelta := du_min[3]; ELSIF rTempDelta > du_max[3] THEN rTempDelta := du_max[3]; END_IF;
u_cand[3] := u_prev[3] + rTempDelta;
IF u_cand[3] < u_min[3] THEN u_cand[3] := u_min[3]; ELSIF u_cand[3] > u_max[3] THEN u_cand[3] := u_max[3]; END_IF;

rTempDelta := (u_cand[4] - (rPGD_StepSize * grad_J[4])) - u_prev[4];
IF rTempDelta < du_min[4] THEN rTempDelta := du_min[4]; ELSIF rTempDelta > du_max[4] THEN rTempDelta := du_max[4]; END_IF;
u_cand[4] := u_prev[4] + rTempDelta;
IF u_cand[4] < u_min[4] THEN u_cand[4] := u_min[4]; ELSIF u_cand[4] > u_max[4] THEN u_cand[4] := u_max[4]; END_IF;

rTempDelta := (u_cand[5] - (rPGD_StepSize * grad_J[5])) - u_prev[5];
IF rTempDelta < du_min[5] THEN rTempDelta := du_min[5]; ELSIF rTempDelta > du_max[5] THEN rTempDelta := du_max[5]; END_IF;
u_cand[5] := u_prev[5] + rTempDelta;
IF u_cand[5] < u_min[5] THEN u_cand[5] := u_min[5]; ELSIF u_cand[5] > u_max[5] THEN u_cand[5] := u_max[5]; END_IF;

x_rollout[1] := (A_Matrix[1,1]*x_hat[1]) + (A_Matrix[1,2]*x_hat[2]) + (A_Matrix[1,3]*x_hat[3]) + (A_Matrix[1,4]*x_hat[4]) + (A_Matrix[1,5]*x_hat[5]) + (A_Matrix[1,6]*x_hat[6]) + (B_Matrix[1,1]*u_cand[1]) + (B_Matrix[1,2]*u_cand[2]) + (B_Matrix[1,3]*u_cand[3]) + (B_Matrix[1,4]*u_cand[4]) + (B_Matrix[1,5]*u_cand[5]);
x_rollout[2] := (A_Matrix[2,1]*x_hat[1]) + (A_Matrix[2,2]*x_hat[2]) + (A_Matrix[2,3]*x_hat[3]) + (A_Matrix[2,4]*x_hat[4]) + (A_Matrix[2,5]*x_hat[5]) + (A_Matrix[2,6]*x_hat[6]) + (B_Matrix[2,1]*u_cand[1]) + (B_Matrix[2,2]*u_cand[2]) + (B_Matrix[2,3]*u_cand[3]) + (B_Matrix[2,4]*u_cand[4]) + (B_Matrix[2,5]*u_cand[5]);
x_rollout[3] := (A_Matrix[3,1]*x_hat[1]) + (A_Matrix[3,2]*x_hat[2]) + (A_Matrix[3,3]*x_hat[3]) + (A_Matrix[3,4]*x_hat[4]) + (A_Matrix[3,5]*x_hat[5]) + (A_Matrix[3,6]*x_hat[6]) + (B_Matrix[3,1]*u_cand[1]) + (B_Matrix[3,2]*u_cand[2]) + (B_Matrix[3,3]*u_cand[3]) + (B_Matrix[3,4]*u_cand[4]) + (B_Matrix[3,5]*u_cand[5]);
x_rollout[4] := (A_Matrix[4,1]*x_hat[1]) + (A_Matrix[4,2]*x_hat[2]) + (A_Matrix[4,3]*x_hat[3]) + (A_Matrix[4,4]*x_hat[4]) + (A_Matrix[4,5]*x_hat[5]) + (A_Matrix[4,6]*x_hat[6]) + (B_Matrix[4,1]*u_cand[1]) + (B_Matrix[4,2]*u_cand[2]) + (B_Matrix[4,3]*u_cand[3]) + (B_Matrix[4,4]*u_cand[4]) + (B_Matrix[4,5]*u_cand[5]);
x_rollout[5] := (A_Matrix[5,1]*x_hat[1]) + (A_Matrix[5,2]*x_hat[2]) + (A_Matrix[5,3]*x_hat[3]) + (A_Matrix[5,4]*x_hat[4]) + (A_Matrix[5,5]*x_hat[5]) + (A_Matrix[5,6]*x_hat[6]) + (B_Matrix[5,1]*u_cand[1]) + (B_Matrix[5,2]*u_cand[2]) + (B_Matrix[5,3]*u_cand[3]) + (B_Matrix[5,4]*u_cand[4]) + (B_Matrix[5,5]*u_cand[5]);
x_rollout[6] := (A_Matrix[6,1]*x_hat[1]) + (A_Matrix[6,2]*x_hat[2]) + (A_Matrix[6,3]*x_hat[3]) + (A_Matrix[6,4]*x_hat[4]) + (A_Matrix[6,5]*x_hat[5]) + (A_Matrix[6,6]*x_hat[6]) + (B_Matrix[6,1]*u_cand[1]) + (B_Matrix[6,2]*u_cand[2]) + (B_Matrix[6,3]*u_cand[3]) + (B_Matrix[6,4]*u_cand[4]) + (B_Matrix[6,5]*u_cand[5]);


(* ========================================================================= *)
(* UNROLLED PGD ITERATION 5 / 10                                             *)
(* ========================================================================= *)
x_err[1] := x_rollout[1] - x_ref[1];
x_err[2] := x_rollout[2] - x_ref[2];
x_err[3] := x_rollout[3] - x_ref[3];
x_err[4] := x_rollout[4] - x_ref[4];
x_err[5] := (x_rollout[5] - x_ref[5]) * rDynamicGradePenaltyWeight;
x_err[6] := x_rollout[6] - x_ref[6];

lambda_costate[1] := (P_Weight[1,1]*x_err[1]) + (P_Weight[1,2]*x_err[2]) + (P_Weight[1,3]*x_err[3]) + (P_Weight[1,4]*x_err[4]) + (P_Weight[1,5]*x_err[5]) + (P_Weight[1,6]*x_err[6]);
lambda_costate[2] := (P_Weight[2,1]*x_err[1]) + (P_Weight[2,2]*x_err[2]) + (P_Weight[2,3]*x_err[3]) + (P_Weight[2,4]*x_err[4]) + (P_Weight[2,5]*x_err[5]) + (P_Weight[2,6]*x_err[6]);
lambda_costate[3] := (P_Weight[3,1]*x_err[1]) + (P_Weight[3,2]*x_err[2]) + (P_Weight[3,3]*x_err[3]) + (P_Weight[3,4]*x_err[4]) + (P_Weight[3,5]*x_err[5]) + (P_Weight[3,6]*x_err[6]);
lambda_costate[4] := (P_Weight[4,1]*x_err[1]) + (P_Weight[4,2]*x_err[2]) + (P_Weight[4,3]*x_err[3]) + (P_Weight[4,4]*x_err[4]) + (P_Weight[4,5]*x_err[5]) + (P_Weight[4,6]*x_err[6]);
lambda_costate[5] := (P_Weight[5,1]*x_err[1]) + (P_Weight[5,2]*x_err[2]) + (P_Weight[5,3]*x_err[3]) + (P_Weight[5,4]*x_err[4]) + (P_Weight[5,5]*x_err[5]) + (P_Weight[5,6]*x_err[6]);
lambda_costate[6] := (P_Weight[6,1]*x_err[1]) + (P_Weight[6,2]*x_err[2]) + (P_Weight[6,3]*x_err[3]) + (P_Weight[6,4]*x_err[4]) + (P_Weight[6,5]*x_err[5]) + (P_Weight[6,6]*x_err[6]);

grad_J[1] := (R_Weight[1,1]*u_cand[1]) + (S_Weight[1,1]*(u_cand[1] - u_prev[1])) + (B_Matrix[1,1]*lambda_costate[1]) + (B_Matrix[2,1]*lambda_costate[2]) + (B_Matrix[3,1]*lambda_costate[3]) + (B_Matrix[4,1]*lambda_costate[4]) + (B_Matrix[5,1]*lambda_costate[5]) + (B_Matrix[6,1]*lambda_costate[6]);
grad_J[2] := (R_Weight[2,2]*u_cand[2]) + (S_Weight[2,2]*(u_cand[2] - u_prev[2])) + (B_Matrix[1,2]*lambda_costate[1]) + (B_Matrix[2,2]*lambda_costate[2]) + (B_Matrix[3,2]*lambda_costate[3]) + (B_Matrix[4,2]*lambda_costate[4]) + (B_Matrix[5,2]*lambda_costate[5]) + (B_Matrix[6,2]*lambda_costate[6]);
grad_J[3] := (R_Weight[3,3]*u_cand[3]) + (S_Weight[3,3]*(u_cand[3] - u_prev[3])) + (B_Matrix[1,3]*lambda_costate[1]) + (B_Matrix[2,3]*lambda_costate[2]) + (B_Matrix[3,3]*lambda_costate[3]) + (B_Matrix[4,3]*lambda_costate[4]) + (B_Matrix[5,3]*lambda_costate[5]) + (B_Matrix[6,3]*lambda_costate[6]);
grad_J[4] := (R_Weight[4,4]*u_cand[4]) + (S_Weight[4,4]*(u_cand[4] - u_prev[4])) + (B_Matrix[1,4]*lambda_costate[1]) + (B_Matrix[2,4]*lambda_costate[2]) + (B_Matrix[3,4]*lambda_costate[3]) + (B_Matrix[4,4]*lambda_costate[4]) + (B_Matrix[5,4]*lambda_costate[5]) + (B_Matrix[6,4]*lambda_costate[6]);
grad_J[5] := (R_Weight[5,5]*u_cand[5]) + (S_Weight[5,5]*(u_cand[5] - u_prev[5])) + (B_Matrix[1,5]*lambda_costate[1]) + (B_Matrix[2,5]*lambda_costate[2]) + (B_Matrix[3,5]*lambda_costate[3]) + (B_Matrix[4,5]*lambda_costate[4]) + (B_Matrix[5,5]*lambda_costate[5]) + (B_Matrix[6,5]*lambda_costate[6]);

rTempDelta := (u_cand[1] - (rPGD_StepSize * grad_J[1])) - u_prev[1];
IF rTempDelta < du_min[1] THEN rTempDelta := du_min[1]; ELSIF rTempDelta > du_max[1] THEN rTempDelta := du_max[1]; END_IF;
u_cand[1] := u_prev[1] + rTempDelta;
IF u_cand[1] < u_min[1] THEN u_cand[1] := u_min[1]; ELSIF u_cand[1] > u_max[1] THEN u_cand[1] := u_max[1]; END_IF;

rTempDelta := (u_cand[2] - (rPGD_StepSize * grad_J[2])) - u_prev[2];
IF rTempDelta < du_min[2] THEN rTempDelta := du_min[2]; ELSIF rTempDelta > du_max[2] THEN rTempDelta := du_max[2]; END_IF;
u_cand[2] := u_prev[2] + rTempDelta;
IF u_cand[2] < u_min[2] THEN u_cand[2] := u_min[2]; ELSIF u_cand[2] > u_max[2] THEN u_cand[2] := u_max[2]; END_IF;

rTempDelta := (u_cand[3] - (rPGD_StepSize * grad_J[3])) - u_prev[3];
IF rTempDelta < du_min[3] THEN rTempDelta := du_min[3]; ELSIF rTempDelta > du_max[3] THEN rTempDelta := du_max[3]; END_IF;
u_cand[3] := u_prev[3] + rTempDelta;
IF u_cand[3] < u_min[3] THEN u_cand[3] := u_min[3]; ELSIF u_cand[3] > u_max[3] THEN u_cand[3] := u_max[3]; END_IF;

rTempDelta := (u_cand[4] - (rPGD_StepSize * grad_J[4])) - u_prev[4];
IF rTempDelta < du_min[4] THEN rTempDelta := du_min[4]; ELSIF rTempDelta > du_max[4] THEN rTempDelta := du_max[4]; END_IF;
u_cand[4] := u_prev[4] + rTempDelta;
IF u_cand[4] < u_min[4] THEN u_cand[4] := u_min[4]; ELSIF u_cand[4] > u_max[4] THEN u_cand[4] := u_max[4]; END_IF;

rTempDelta := (u_cand[5] - (rPGD_StepSize * grad_J[5])) - u_prev[5];
IF rTempDelta < du_min[5] THEN rTempDelta := du_min[5]; ELSIF rTempDelta > du_max[5] THEN rTempDelta := du_max[5]; END_IF;
u_cand[5] := u_prev[5] + rTempDelta;
IF u_cand[5] < u_min[5] THEN u_cand[5] := u_min[5]; ELSIF u_cand[5] > u_max[5] THEN u_cand[5] := u_max[5]; END_IF;

x_rollout[1] := (A_Matrix[1,1]*x_hat[1]) + (A_Matrix[1,2]*x_hat[2]) + (A_Matrix[1,3]*x_hat[3]) + (A_Matrix[1,4]*x_hat[4]) + (A_Matrix[1,5]*x_hat[5]) + (A_Matrix[1,6]*x_hat[6]) + (B_Matrix[1,1]*u_cand[1]) + (B_Matrix[1,2]*u_cand[2]) + (B_Matrix[1,3]*u_cand[3]) + (B_Matrix[1,4]*u_cand[4]) + (B_Matrix[1,5]*u_cand[5]);
x_rollout[2] := (A_Matrix[2,1]*x_hat[1]) + (A_Matrix[2,2]*x_hat[2]) + (A_Matrix[2,3]*x_hat[3]) + (A_Matrix[2,4]*x_hat[4]) + (A_Matrix[2,5]*x_hat[5]) + (A_Matrix[2,6]*x_hat[6]) + (B_Matrix[2,1]*u_cand[1]) + (B_Matrix[2,2]*u_cand[2]) + (B_Matrix[2,3]*u_cand[3]) + (B_Matrix[2,4]*u_cand[4]) + (B_Matrix[2,5]*u_cand[5]);
x_rollout[3] := (A_Matrix[3,1]*x_hat[1]) + (A_Matrix[3,2]*x_hat[2]) + (A_Matrix[3,3]*x_hat[3]) + (A_Matrix[3,4]*x_hat[4]) + (A_Matrix[3,5]*x_hat[5]) + (A_Matrix[3,6]*x_hat[6]) + (B_Matrix[3,1]*u_cand[1]) + (B_Matrix[3,2]*u_cand[2]) + (B_Matrix[3,3]*u_cand[3]) + (B_Matrix[3,4]*u_cand[4]) + (B_Matrix[3,5]*u_cand[5]);
x_rollout[4] := (A_Matrix[4,1]*x_hat[1]) + (A_Matrix[4,2]*x_hat[2]) + (A_Matrix[4,3]*x_hat[3]) + (A_Matrix[4,4]*x_hat[4]) + (A_Matrix[4,5]*x_hat[5]) + (A_Matrix[4,6]*x_hat[6]) + (B_Matrix[4,1]*u_cand[1]) + (B_Matrix[4,2]*u_cand[2]) + (B_Matrix[4,3]*u_cand[3]) + (B_Matrix[4,4]*u_cand[4]) + (B_Matrix[4,5]*u_cand[5]);
x_rollout[5] := (A_Matrix[5,1]*x_hat[1]) + (A_Matrix[5,2]*x_hat[2]) + (A_Matrix[5,3]*x_hat[3]) + (A_Matrix[5,4]*x_hat[4]) + (A_Matrix[5,5]*x_hat[5]) + (A_Matrix[5,6]*x_hat[6]) + (B_Matrix[5,1]*u_cand[1]) + (B_Matrix[5,2]*u_cand[2]) + (B_Matrix[5,3]*u_cand[3]) + (B_Matrix[5,4]*u_cand[4]) + (B_Matrix[5,5]*u_cand[5]);
x_rollout[6] := (A_Matrix[6,1]*x_hat[1]) + (A_Matrix[6,2]*x_hat[2]) + (A_Matrix[6,3]*x_hat[3]) + (A_Matrix[6,4]*x_hat[4]) + (A_Matrix[6,5]*x_hat[5]) + (A_Matrix[6,6]*x_hat[6]) + (B_Matrix[6,1]*u_cand[1]) + (B_Matrix[6,2]*u_cand[2]) + (B_Matrix[6,3]*u_cand[3]) + (B_Matrix[6,4]*u_cand[4]) + (B_Matrix[6,5]*u_cand[5]);


(* ========================================================================= *)
(* UNROLLED PGD ITERATION 6 / 10                                             *)
(* ========================================================================= *)
x_err[1] := x_rollout[1] - x_ref[1];
x_err[2] := x_rollout[2] - x_ref[2];
x_err[3] := x_rollout[3] - x_ref[3];
x_err[4] := x_rollout[4] - x_ref[4];
x_err[5] := (x_rollout[5] - x_ref[5]) * rDynamicGradePenaltyWeight;
x_err[6] := x_rollout[6] - x_ref[6];

lambda_costate[1] := (P_Weight[1,1]*x_err[1]) + (P_Weight[1,2]*x_err[2]) + (P_Weight[1,3]*x_err[3]) + (P_Weight[1,4]*x_err[4]) + (P_Weight[1,5]*x_err[5]) + (P_Weight[1,6]*x_err[6]);
lambda_costate[2] := (P_Weight[2,1]*x_err[1]) + (P_Weight[2,2]*x_err[2]) + (P_Weight[2,3]*x_err[3]) + (P_Weight[2,4]*x_err[4]) + (P_Weight[2,5]*x_err[5]) + (P_Weight[2,6]*x_err[6]);
lambda_costate[3] := (P_Weight[3,1]*x_err[1]) + (P_Weight[3,2]*x_err[2]) + (P_Weight[3,3]*x_err[3]) + (P_Weight[3,4]*x_err[4]) + (P_Weight[3,5]*x_err[5]) + (P_Weight[3,6]*x_err[6]);
lambda_costate[4] := (P_Weight[4,1]*x_err[1]) + (P_Weight[4,2]*x_err[2]) + (P_Weight[4,3]*x_err[3]) + (P_Weight[4,4]*x_err[4]) + (P_Weight[4,5]*x_err[5]) + (P_Weight[4,6]*x_err[6]);
lambda_costate[5] := (P_Weight[5,1]*x_err[1]) + (P_Weight[5,2]*x_err[2]) + (P_Weight[5,3]*x_err[3]) + (P_Weight[5,4]*x_err[4]) + (P_Weight[5,5]*x_err[5]) + (P_Weight[5,6]*x_err[6]);
lambda_costate[6] := (P_Weight[6,1]*x_err[1]) + (P_Weight[6,2]*x_err[2]) + (P_Weight[6,3]*x_err[3]) + (P_Weight[6,4]*x_err[4]) + (P_Weight[6,5]*x_err[5]) + (P_Weight[6,6]*x_err[6]);

grad_J[1] := (R_Weight[1,1]*u_cand[1]) + (S_Weight[1,1]*(u_cand[1] - u_prev[1])) + (B_Matrix[1,1]*lambda_costate[1]) + (B_Matrix[2,1]*lambda_costate[2]) + (B_Matrix[3,1]*lambda_costate[3]) + (B_Matrix[4,1]*lambda_costate[4]) + (B_Matrix[5,1]*lambda_costate[5]) + (B_Matrix[6,1]*lambda_costate[6]);
grad_J[2] := (R_Weight[2,2]*u_cand[2]) + (S_Weight[2,2]*(u_cand[2] - u_prev[2])) + (B_Matrix[1,2]*lambda_costate[1]) + (B_Matrix[2,2]*lambda_costate[2]) + (B_Matrix[3,2]*lambda_costate[3]) + (B_Matrix[4,2]*lambda_costate[4]) + (B_Matrix[5,2]*lambda_costate[5]) + (B_Matrix[6,2]*lambda_costate[6]);
grad_J[3] := (R_Weight[3,3]*u_cand[3]) + (S_Weight[3,3]*(u_cand[3] - u_prev[3])) + (B_Matrix[1,3]*lambda_costate[1]) + (B_Matrix[2,3]*lambda_costate[2]) + (B_Matrix[3,3]*lambda_costate[3]) + (B_Matrix[4,3]*lambda_costate[4]) + (B_Matrix[5,3]*lambda_costate[5]) + (B_Matrix[6,3]*lambda_costate[6]);
grad_J[4] := (R_Weight[4,4]*u_cand[4]) + (S_Weight[4,4]*(u_cand[4] - u_prev[4])) + (B_Matrix[1,4]*lambda_costate[1]) + (B_Matrix[2,4]*lambda_costate[2]) + (B_Matrix[3,4]*lambda_costate[3]) + (B_Matrix[4,4]*lambda_costate[4]) + (B_Matrix[5,4]*lambda_costate[5]) + (B_Matrix[6,4]*lambda_costate[6]);
grad_J[5] := (R_Weight[5,5]*u_cand[5]) + (S_Weight[5,5]*(u_cand[5] - u_prev[5])) + (B_Matrix[1,5]*lambda_costate[1]) + (B_Matrix[2,5]*lambda_costate[2]) + (B_Matrix[3,5]*lambda_costate[3]) + (B_Matrix[4,5]*lambda_costate[4]) + (B_Matrix[5,5]*lambda_costate[5]) + (B_Matrix[6,5]*lambda_costate[6]);

rTempDelta := (u_cand[1] - (rPGD_StepSize * grad_J[1])) - u_prev[1];
IF rTempDelta < du_min[1] THEN rTempDelta := du_min[1]; ELSIF rTempDelta > du_max[1] THEN rTempDelta := du_max[1]; END_IF;
u_cand[1] := u_prev[1] + rTempDelta;
IF u_cand[1] < u_min[1] THEN u_cand[1] := u_min[1]; ELSIF u_cand[1] > u_max[1] THEN u_cand[1] := u_max[1]; END_IF;

rTempDelta := (u_cand[2] - (rPGD_StepSize * grad_J[2])) - u_prev[2];
IF rTempDelta < du_min[2] THEN rTempDelta := du_min[2]; ELSIF rTempDelta > du_max[2] THEN rTempDelta := du_max[2]; END_IF;
u_cand[2] := u_prev[2] + rTempDelta;
IF u_cand[2] < u_min[2] THEN u_cand[2] := u_min[2]; ELSIF u_cand[2] > u_max[2] THEN u_cand[2] := u_max[2]; END_IF;

rTempDelta := (u_cand[3] - (rPGD_StepSize * grad_J[3])) - u_prev[3];
IF rTempDelta < du_min[3] THEN rTempDelta := du_min[3]; ELSIF rTempDelta > du_max[3] THEN rTempDelta := du_max[3]; END_IF;
u_cand[3] := u_prev[3] + rTempDelta;
IF u_cand[3] < u_min[3] THEN u_cand[3] := u_min[3]; ELSIF u_cand[3] > u_max[3] THEN u_cand[3] := u_max[3]; END_IF;

rTempDelta := (u_cand[4] - (rPGD_StepSize * grad_J[4])) - u_prev[4];
IF rTempDelta < du_min[4] THEN rTempDelta := du_min[4]; ELSIF rTempDelta > du_max[4] THEN rTempDelta := du_max[4]; END_IF;
u_cand[4] := u_prev[4] + rTempDelta;
IF u_cand[4] < u_min[4] THEN u_cand[4] := u_min[4]; ELSIF u_cand[4] > u_max[4] THEN u_cand[4] := u_max[4]; END_IF;

rTempDelta := (u_cand[5] - (rPGD_StepSize * grad_J[5])) - u_prev[5];
IF rTempDelta < du_min[5] THEN rTempDelta := du_min[5]; ELSIF rTempDelta > du_max[5] THEN rTempDelta := du_max[5]; END_IF;
u_cand[5] := u_prev[5] + rTempDelta;
IF u_cand[5] < u_min[5] THEN u_cand[5] := u_min[5]; ELSIF u_cand[5] > u_max[5] THEN u_cand[5] := u_max[5]; END_IF;

x_rollout[1] := (A_Matrix[1,1]*x_hat[1]) + (A_Matrix[1,2]*x_hat[2]) + (A_Matrix[1,3]*x_hat[3]) + (A_Matrix[1,4]*x_hat[4]) + (A_Matrix[1,5]*x_hat[5]) + (A_Matrix[1,6]*x_hat[6]) + (B_Matrix[1,1]*u_cand[1]) + (B_Matrix[1,2]*u_cand[2]) + (B_Matrix[1,3]*u_cand[3]) + (B_Matrix[1,4]*u_cand[4]) + (B_Matrix[1,5]*u_cand[5]);
x_rollout[2] := (A_Matrix[2,1]*x_hat[1]) + (A_Matrix[2,2]*x_hat[2]) + (A_Matrix[2,3]*x_hat[3]) + (A_Matrix[2,4]*x_hat[4]) + (A_Matrix[2,5]*x_hat[5]) + (A_Matrix[2,6]*x_hat[6]) + (B_Matrix[2,1]*u_cand[1]) + (B_Matrix[2,2]*u_cand[2]) + (B_Matrix[2,3]*u_cand[3]) + (B_Matrix[2,4]*u_cand[4]) + (B_Matrix[2,5]*u_cand[5]);
x_rollout[3] := (A_Matrix[3,1]*x_hat[1]) + (A_Matrix[3,2]*x_hat[2]) + (A_Matrix[3,3]*x_hat[3]) + (A_Matrix[3,4]*x_hat[4]) + (A_Matrix[3,5]*x_hat[5]) + (A_Matrix[3,6]*x_hat[6]) + (B_Matrix[3,1]*u_cand[1]) + (B_Matrix[3,2]*u_cand[2]) + (B_Matrix[3,3]*u_cand[3]) + (B_Matrix[3,4]*u_cand[4]) + (B_Matrix[3,5]*u_cand[5]);
x_rollout[4] := (A_Matrix[4,1]*x_hat[1]) + (A_Matrix[4,2]*x_hat[2]) + (A_Matrix[4,3]*x_hat[3]) + (A_Matrix[4,4]*x_hat[4]) + (A_Matrix[4,5]*x_hat[5]) + (A_Matrix[4,6]*x_hat[6]) + (B_Matrix[4,1]*u_cand[1]) + (B_Matrix[4,2]*u_cand[2]) + (B_Matrix[4,3]*u_cand[3]) + (B_Matrix[4,4]*u_cand[4]) + (B_Matrix[4,5]*u_cand[5]);
x_rollout[5] := (A_Matrix[5,1]*x_hat[1]) + (A_Matrix[5,2]*x_hat[2]) + (A_Matrix[5,3]*x_hat[3]) + (A_Matrix[5,4]*x_hat[4]) + (A_Matrix[5,5]*x_hat[5]) + (A_Matrix[5,6]*x_hat[6]) + (B_Matrix[5,1]*u_cand[1]) + (B_Matrix[5,2]*u_cand[2]) + (B_Matrix[5,3]*u_cand[3]) + (B_Matrix[5,4]*u_cand[4]) + (B_Matrix[5,5]*u_cand[5]);
x_rollout[6] := (A_Matrix[6,1]*x_hat[1]) + (A_Matrix[6,2]*x_hat[2]) + (A_Matrix[6,3]*x_hat[3]) + (A_Matrix[6,4]*x_hat[4]) + (A_Matrix[6,5]*x_hat[5]) + (A_Matrix[6,6]*x_hat[6]) + (B_Matrix[6,1]*u_cand[1]) + (B_Matrix[6,2]*u_cand[2]) + (B_Matrix[6,3]*u_cand[3]) + (B_Matrix[6,4]*u_cand[4]) + (B_Matrix[6,5]*u_cand[5]);


(* ========================================================================= *)
(* UNROLLED PGD ITERATION 7 / 10                                             *)
(* ========================================================================= *)
x_err[1] := x_rollout[1] - x_ref[1];
x_err[2] := x_rollout[2] - x_ref[2];
x_err[3] := x_rollout[3] - x_ref[3];
x_err[4] := x_rollout[4] - x_ref[4];
x_err[5] := (x_rollout[5] - x_ref[5]) * rDynamicGradePenaltyWeight;
x_err[6] := x_rollout[6] - x_ref[6];

lambda_costate[1] := (P_Weight[1,1]*x_err[1]) + (P_Weight[1,2]*x_err[2]) + (P_Weight[1,3]*x_err[3]) + (P_Weight[1,4]*x_err[4]) + (P_Weight[1,5]*x_err[5]) + (P_Weight[1,6]*x_err[6]);
lambda_costate[2] := (P_Weight[2,1]*x_err[1]) + (P_Weight[2,2]*x_err[2]) + (P_Weight[2,3]*x_err[3]) + (P_Weight[2,4]*x_err[4]) + (P_Weight[2,5]*x_err[5]) + (P_Weight[2,6]*x_err[6]);
lambda_costate[3] := (P_Weight[3,1]*x_err[1]) + (P_Weight[3,2]*x_err[2]) + (P_Weight[3,3]*x_err[3]) + (P_Weight[3,4]*x_err[4]) + (P_Weight[3,5]*x_err[5]) + (P_Weight[3,6]*x_err[6]);
lambda_costate[4] := (P_Weight[4,1]*x_err[1]) + (P_Weight[4,2]*x_err[2]) + (P_Weight[4,3]*x_err[3]) + (P_Weight[4,4]*x_err[4]) + (P_Weight[4,5]*x_err[5]) + (P_Weight[4,6]*x_err[6]);
lambda_costate[5] := (P_Weight[5,1]*x_err[1]) + (P_Weight[5,2]*x_err[2]) + (P_Weight[5,3]*x_err[3]) + (P_Weight[5,4]*x_err[4]) + (P_Weight[5,5]*x_err[5]) + (P_Weight[5,6]*x_err[6]);
lambda_costate[6] := (P_Weight[6,1]*x_err[1]) + (P_Weight[6,2]*x_err[2]) + (P_Weight[6,3]*x_err[3]) + (P_Weight[6,4]*x_err[4]) + (P_Weight[6,5]*x_err[5]) + (P_Weight[6,6]*x_err[6]);

grad_J[1] := (R_Weight[1,1]*u_cand[1]) + (S_Weight[1,1]*(u_cand[1] - u_prev[1])) + (B_Matrix[1,1]*lambda_costate[1]) + (B_Matrix[2,1]*lambda_costate[2]) + (B_Matrix[3,1]*lambda_costate[3]) + (B_Matrix[4,1]*lambda_costate[4]) + (B_Matrix[5,1]*lambda_costate[5]) + (B_Matrix[6,1]*lambda_costate[6]);
grad_J[2] := (R_Weight[2,2]*u_cand[2]) + (S_Weight[2,2]*(u_cand[2] - u_prev[2])) + (B_Matrix[1,2]*lambda_costate[1]) + (B_Matrix[2,2]*lambda_costate[2]) + (B_Matrix[3,2]*lambda_costate[3]) + (B_Matrix[4,2]*lambda_costate[4]) + (B_Matrix[5,2]*lambda_costate[5]) + (B_Matrix[6,2]*lambda_costate[6]);
grad_J[3] := (R_Weight[3,3]*u_cand[3]) + (S_Weight[3,3]*(u_cand[3] - u_prev[3])) + (B_Matrix[1,3]*lambda_costate[1]) + (B_Matrix[2,3]*lambda_costate[2]) + (B_Matrix[3,3]*lambda_costate[3]) + (B_Matrix[4,3]*lambda_costate[4]) + (B_Matrix[5,3]*lambda_costate[5]) + (B_Matrix[6,3]*lambda_costate[6]);
grad_J[4] := (R_Weight[4,4]*u_cand[4]) + (S_Weight[4,4]*(u_cand[4] - u_prev[4])) + (B_Matrix[1,4]*lambda_costate[1]) + (B_Matrix[2,4]*lambda_costate[2]) + (B_Matrix[3,4]*lambda_costate[3]) + (B_Matrix[4,4]*lambda_costate[4]) + (B_Matrix[5,4]*lambda_costate[5]) + (B_Matrix[6,4]*lambda_costate[6]);
grad_J[5] := (R_Weight[5,5]*u_cand[5]) + (S_Weight[5,5]*(u_cand[5] - u_prev[5])) + (B_Matrix[1,5]*lambda_costate[1]) + (B_Matrix[2,5]*lambda_costate[2]) + (B_Matrix[3,5]*lambda_costate[3]) + (B_Matrix[4,5]*lambda_costate[4]) + (B_Matrix[5,5]*lambda_costate[5]) + (B_Matrix[6,5]*lambda_costate[6]);

rTempDelta := (u_cand[1] - (rPGD_StepSize * grad_J[1])) - u_prev[1];
IF rTempDelta < du_min[1] THEN rTempDelta := du_min[1]; ELSIF rTempDelta > du_max[1] THEN rTempDelta := du_max[1]; END_IF;
u_cand[1] := u_prev[1] + rTempDelta;
IF u_cand[1] < u_min[1] THEN u_cand[1] := u_min[1]; ELSIF u_cand[1] > u_max[1] THEN u_cand[1] := u_max[1]; END_IF;

rTempDelta := (u_cand[2] - (rPGD_StepSize * grad_J[2])) - u_prev[2];
IF rTempDelta < du_min[2] THEN rTempDelta := du_min[2]; ELSIF rTempDelta > du_max[2] THEN rTempDelta := du_max[2]; END_IF;
u_cand[2] := u_prev[2] + rTempDelta;
IF u_cand[2] < u_min[2] THEN u_cand[2] := u_min[2]; ELSIF u_cand[2] > u_max[2] THEN u_cand[2] := u_max[2]; END_IF;

rTempDelta := (u_cand[3] - (rPGD_StepSize * grad_J[3])) - u_prev[3];
IF rTempDelta < du_min[3] THEN rTempDelta := du_min[3]; ELSIF rTempDelta > du_max[3] THEN rTempDelta := du_max[3]; END_IF;
u_cand[3] := u_prev[3] + rTempDelta;
IF u_cand[3] < u_min[3] THEN u_cand[3] := u_min[3]; ELSIF u_cand[3] > u_max[3] THEN u_cand[3] := u_max[3]; END_IF;

rTempDelta := (u_cand[4] - (rPGD_StepSize * grad_J[4])) - u_prev[4];
IF rTempDelta < du_min[4] THEN rTempDelta := du_min[4]; ELSIF rTempDelta > du_max[4] THEN rTempDelta := du_max[4]; END_IF;
u_cand[4] := u_prev[4] + rTempDelta;
IF u_cand[4] < u_min[4] THEN u_cand[4] := u_min[4]; ELSIF u_cand[4] > u_max[4] THEN u_cand[4] := u_max[4]; END_IF;

rTempDelta := (u_cand[5] - (rPGD_StepSize * grad_J[5])) - u_prev[5];
IF rTempDelta < du_min[5] THEN rTempDelta := du_min[5]; ELSIF rTempDelta > du_max[5] THEN rTempDelta := du_max[5]; END_IF;
u_cand[5] := u_prev[5] + rTempDelta;
IF u_cand[5] < u_min[5] THEN u_cand[5] := u_min[5]; ELSIF u_cand[5] > u_max[5] THEN u_cand[5] := u_max[5]; END_IF;

x_rollout[1] := (A_Matrix[1,1]*x_hat[1]) + (A_Matrix[1,2]*x_hat[2]) + (A_Matrix[1,3]*x_hat[3]) + (A_Matrix[1,4]*x_hat[4]) + (A_Matrix[1,5]*x_hat[5]) + (A_Matrix[1,6]*x_hat[6]) + (B_Matrix[1,1]*u_cand[1]) + (B_Matrix[1,2]*u_cand[2]) + (B_Matrix[1,3]*u_cand[3]) + (B_Matrix[1,4]*u_cand[4]) + (B_Matrix[1,5]*u_cand[5]);
x_rollout[2] := (A_Matrix[2,1]*x_hat[1]) + (A_Matrix[2,2]*x_hat[2]) + (A_Matrix[2,3]*x_hat[3]) + (A_Matrix[2,4]*x_hat[4]) + (A_Matrix[2,5]*x_hat[5]) + (A_Matrix[2,6]*x_hat[6]) + (B_Matrix[2,1]*u_cand[1]) + (B_Matrix[2,2]*u_cand[2]) + (B_Matrix[2,3]*u_cand[3]) + (B_Matrix[2,4]*u_cand[4]) + (B_Matrix[2,5]*u_cand[5]);
x_rollout[3] := (A_Matrix[3,1]*x_hat[1]) + (A_Matrix[3,2]*x_hat[2]) + (A_Matrix[3,3]*x_hat[3]) + (A_Matrix[3,4]*x_hat[4]) + (A_Matrix[3,5]*x_hat[5]) + (A_Matrix[3,6]*x_hat[6]) + (B_Matrix[3,1]*u_cand[1]) + (B_Matrix[3,2]*u_cand[2]) + (B_Matrix[3,3]*u_cand[3]) + (B_Matrix[3,4]*u_cand[4]) + (B_Matrix[3,5]*u_cand[5]);
x_rollout[4] := (A_Matrix[4,1]*x_hat[1]) + (A_Matrix[4,2]*x_hat[2]) + (A_Matrix[4,3]*x_hat[3]) + (A_Matrix[4,4]*x_hat[4]) + (A_Matrix[4,5]*x_hat[5]) + (A_Matrix[4,6]*x_hat[6]) + (B_Matrix[4,1]*u_cand[1]) + (B_Matrix[4,2]*u_cand[2]) + (B_Matrix[4,3]*u_cand[3]) + (B_Matrix[4,4]*u_cand[4]) + (B_Matrix[4,5]*u_cand[5]);
x_rollout[5] := (A_Matrix[5,1]*x_hat[1]) + (A_Matrix[5,2]*x_hat[2]) + (A_Matrix[5,3]*x_hat[3]) + (A_Matrix[5,4]*x_hat[4]) + (A_Matrix[5,5]*x_hat[5]) + (A_Matrix[5,6]*x_hat[6]) + (B_Matrix[5,1]*u_cand[1]) + (B_Matrix[5,2]*u_cand[2]) + (B_Matrix[5,3]*u_cand[3]) + (B_Matrix[5,4]*u_cand[4]) + (B_Matrix[5,5]*u_cand[5]);
x_rollout[6] := (A_Matrix[6,1]*x_hat[1]) + (A_Matrix[6,2]*x_hat[2]) + (A_Matrix[6,3]*x_hat[3]) + (A_Matrix[6,4]*x_hat[4]) + (A_Matrix[6,5]*x_hat[5]) + (A_Matrix[6,6]*x_hat[6]) + (B_Matrix[6,1]*u_cand[1]) + (B_Matrix[6,2]*u_cand[2]) + (B_Matrix[6,3]*u_cand[3]) + (B_Matrix[6,4]*u_cand[4]) + (B_Matrix[6,5]*u_cand[5]);


(* ========================================================================= *)
(* UNROLLED PGD ITERATION 8 / 10                                             *)
(* ========================================================================= *)
x_err[1] := x_rollout[1] - x_ref[1];
x_err[2] := x_rollout[2] - x_ref[2];
x_err[3] := x_rollout[3] - x_ref[3];
x_err[4] := x_rollout[4] - x_ref[4];
x_err[5] := (x_rollout[5] - x_ref[5]) * rDynamicGradePenaltyWeight;
x_err[6] := x_rollout[6] - x_ref[6];

lambda_costate[1] := (P_Weight[1,1]*x_err[1]) + (P_Weight[1,2]*x_err[2]) + (P_Weight[1,3]*x_err[3]) + (P_Weight[1,4]*x_err[4]) + (P_Weight[1,5]*x_err[5]) + (P_Weight[1,6]*x_err[6]);
lambda_costate[2] := (P_Weight[2,1]*x_err[1]) + (P_Weight[2,2]*x_err[2]) + (P_Weight[2,3]*x_err[3]) + (P_Weight[2,4]*x_err[4]) + (P_Weight[2,5]*x_err[5]) + (P_Weight[2,6]*x_err[6]);
lambda_costate[3] := (P_Weight[3,1]*x_err[1]) + (P_Weight[3,2]*x_err[2]) + (P_Weight[3,3]*x_err[3]) + (P_Weight[3,4]*x_err[4]) + (P_Weight[3,5]*x_err[5]) + (P_Weight[3,6]*x_err[6]);
lambda_costate[4] := (P_Weight[4,1]*x_err[1]) + (P_Weight[4,2]*x_err[2]) + (P_Weight[4,3]*x_err[3]) + (P_Weight[4,4]*x_err[4]) + (P_Weight[4,5]*x_err[5]) + (P_Weight[4,6]*x_err[6]);
lambda_costate[5] := (P_Weight[5,1]*x_err[1]) + (P_Weight[5,2]*x_err[2]) + (P_Weight[5,3]*x_err[3]) + (P_Weight[5,4]*x_err[4]) + (P_Weight[5,5]*x_err[5]) + (P_Weight[5,6]*x_err[6]);
lambda_costate[6] := (P_Weight[6,1]*x_err[1]) + (P_Weight[6,2]*x_err[2]) + (P_Weight[6,3]*x_err[3]) + (P_Weight[6,4]*x_err[4]) + (P_Weight[6,5]*x_err[5]) + (P_Weight[6,6]*x_err[6]);

grad_J[1] := (R_Weight[1,1]*u_cand[1]) + (S_Weight[1,1]*(u_cand[1] - u_prev[1])) + (B_Matrix[1,1]*lambda_costate[1]) + (B_Matrix[2,1]*lambda_costate[2]) + (B_Matrix[3,1]*lambda_costate[3]) + (B_Matrix[4,1]*lambda_costate[4]) + (B_Matrix[5,1]*lambda_costate[5]) + (B_Matrix[6,1]*lambda_costate[6]);
grad_J[2] := (R_Weight[2,2]*u_cand[2]) + (S_Weight[2,2]*(u_cand[2] - u_prev[2])) + (B_Matrix[1,2]*lambda_costate[1]) + (B_Matrix[2,2]*lambda_costate[2]) + (B_Matrix[3,2]*lambda_costate[3]) + (B_Matrix[4,2]*lambda_costate[4]) + (B_Matrix[5,2]*lambda_costate[5]) + (B_Matrix[6,2]*lambda_costate[6]);
grad_J[3] := (R_Weight[3,3]*u_cand[3]) + (S_Weight[3,3]*(u_cand[3] - u_prev[3])) + (B_Matrix[1,3]*lambda_costate[1]) + (B_Matrix[2,3]*lambda_costate[2]) + (B_Matrix[3,3]*lambda_costate[3]) + (B_Matrix[4,3]*lambda_costate[4]) + (B_Matrix[5,3]*lambda_costate[5]) + (B_Matrix[6,3]*lambda_costate[6]);
grad_J[4] := (R_Weight[4,4]*u_cand[4]) + (S_Weight[4,4]*(u_cand[4] - u_prev[4])) + (B_Matrix[1,4]*lambda_costate[1]) + (B_Matrix[2,4]*lambda_costate[2]) + (B_Matrix[3,4]*lambda_costate[3]) + (B_Matrix[4,4]*lambda_costate[4]) + (B_Matrix[5,4]*lambda_costate[5]) + (B_Matrix[6,4]*lambda_costate[6]);
grad_J[5] := (R_Weight[5,5]*u_cand[5]) + (S_Weight[5,5]*(u_cand[5] - u_prev[5])) + (B_Matrix[1,5]*lambda_costate[1]) + (B_Matrix[2,5]*lambda_costate[2]) + (B_Matrix[3,5]*lambda_costate[3]) + (B_Matrix[4,5]*lambda_costate[4]) + (B_Matrix[5,5]*lambda_costate[5]) + (B_Matrix[6,5]*lambda_costate[6]);

rTempDelta := (u_cand[1] - (rPGD_StepSize * grad_J[1])) - u_prev[1];
IF rTempDelta < du_min[1] THEN rTempDelta := du_min[1]; ELSIF rTempDelta > du_max[1] THEN rTempDelta := du_max[1]; END_IF;
u_cand[1] := u_prev[1] + rTempDelta;
IF u_cand[1] < u_min[1] THEN u_cand[1] := u_min[1]; ELSIF u_cand[1] > u_max[1] THEN u_cand[1] := u_max[1]; END_IF;

rTempDelta := (u_cand[2] - (rPGD_StepSize * grad_J[2])) - u_prev[2];
IF rTempDelta < du_min[2] THEN rTempDelta := du_min[2]; ELSIF rTempDelta > du_max[2] THEN rTempDelta := du_max[2]; END_IF;
u_cand[2] := u_prev[2] + rTempDelta;
IF u_cand[2] < u_min[2] THEN u_cand[2] := u_min[2]; ELSIF u_cand[2] > u_max[2] THEN u_cand[2] := u_max[2]; END_IF;

rTempDelta := (u_cand[3] - (rPGD_StepSize * grad_J[3])) - u_prev[3];
IF rTempDelta < du_min[3] THEN rTempDelta := du_min[3]; ELSIF rTempDelta > du_max[3] THEN rTempDelta := du_max[3]; END_IF;
u_cand[3] := u_prev[3] + rTempDelta;
IF u_cand[3] < u_min[3] THEN u_cand[3] := u_min[3]; ELSIF u_cand[3] > u_max[3] THEN u_cand[3] := u_max[3]; END_IF;

rTempDelta := (u_cand[4] - (rPGD_StepSize * grad_J[4])) - u_prev[4];
IF rTempDelta < du_min[4] THEN rTempDelta := du_min[4]; ELSIF rTempDelta > du_max[4] THEN rTempDelta := du_max[4]; END_IF;
u_cand[4] := u_prev[4] + rTempDelta;
IF u_cand[4] < u_min[4] THEN u_cand[4] := u_min[4]; ELSIF u_cand[4] > u_max[4] THEN u_cand[4] := u_max[4]; END_IF;

rTempDelta := (u_cand[5] - (rPGD_StepSize * grad_J[5])) - u_prev[5];
IF rTempDelta < du_min[5] THEN rTempDelta := du_min[5]; ELSIF rTempDelta > du_max[5] THEN rTempDelta := du_max[5]; END_IF;
u_cand[5] := u_prev[5] + rTempDelta;
IF u_cand[5] < u_min[5] THEN u_cand[5] := u_min[5]; ELSIF u_cand[5] > u_max[5] THEN u_cand[5] := u_max[5]; END_IF;

x_rollout[1] := (A_Matrix[1,1]*x_hat[1]) + (A_Matrix[1,2]*x_hat[2]) + (A_Matrix[1,3]*x_hat[3]) + (A_Matrix[1,4]*x_hat[4]) + (A_Matrix[1,5]*x_hat[5]) + (A_Matrix[1,6]*x_hat[6]) + (B_Matrix[1,1]*u_cand[1]) + (B_Matrix[1,2]*u_cand[2]) + (B_Matrix[1,3]*u_cand[3]) + (B_Matrix[1,4]*u_cand[4]) + (B_Matrix[1,5]*u_cand[5]);
x_rollout[2] := (A_Matrix[2,1]*x_hat[1]) + (A_Matrix[2,2]*x_hat[2]) + (A_Matrix[2,3]*x_hat[3]) + (A_Matrix[2,4]*x_hat[4]) + (A_Matrix[2,5]*x_hat[5]) + (A_Matrix[2,6]*x_hat[6]) + (B_Matrix[2,1]*u_cand[1]) + (B_Matrix[2,2]*u_cand[2]) + (B_Matrix[2,3]*u_cand[3]) + (B_Matrix[2,4]*u_cand[4]) + (B_Matrix[2,5]*u_cand[5]);
x_rollout[3] := (A_Matrix[3,1]*x_hat[1]) + (A_Matrix[3,2]*x_hat[2]) + (A_Matrix[3,3]*x_hat[3]) + (A_Matrix[3,4]*x_hat[4]) + (A_Matrix[3,5]*x_hat[5]) + (A_Matrix[3,6]*x_hat[6]) + (B_Matrix[3,1]*u_cand[1]) + (B_Matrix[3,2]*u_cand[2]) + (B_Matrix[3,3]*u_cand[3]) + (B_Matrix[3,4]*u_cand[4]) + (B_Matrix[3,5]*u_cand[5]);
x_rollout[4] := (A_Matrix[4,1]*x_hat[1]) + (A_Matrix[4,2]*x_hat[2]) + (A_Matrix[4,3]*x_hat[3]) + (A_Matrix[4,4]*x_hat[4]) + (A_Matrix[4,5]*x_hat[5]) + (A_Matrix[4,6]*x_hat[6]) + (B_Matrix[4,1]*u_cand[1]) + (B_Matrix[4,2]*u_cand[2]) + (B_Matrix[4,3]*u_cand[3]) + (B_Matrix[4,4]*u_cand[4]) + (B_Matrix[4,5]*u_cand[5]);
x_rollout[5] := (A_Matrix[5,1]*x_hat[1]) + (A_Matrix[5,2]*x_hat[2]) + (A_Matrix[5,3]*x_hat[3]) + (A_Matrix[5,4]*x_hat[4]) + (A_Matrix[5,5]*x_hat[5]) + (A_Matrix[5,6]*x_hat[6]) + (B_Matrix[5,1]*u_cand[1]) + (B_Matrix[5,2]*u_cand[2]) + (B_Matrix[5,3]*u_cand[3]) + (B_Matrix[5,4]*u_cand[4]) + (B_Matrix[5,5]*u_cand[5]);
x_rollout[6] := (A_Matrix[6,1]*x_hat[1]) + (A_Matrix[6,2]*x_hat[2]) + (A_Matrix[6,3]*x_hat[3]) + (A_Matrix[6,4]*x_hat[4]) + (A_Matrix[6,5]*x_hat[5]) + (A_Matrix[6,6]*x_hat[6]) + (B_Matrix[6,1]*u_cand[1]) + (B_Matrix[6,2]*u_cand[2]) + (B_Matrix[6,3]*u_cand[3]) + (B_Matrix[6,4]*u_cand[4]) + (B_Matrix[6,5]*u_cand[5]);


(* ========================================================================= *)
(* UNROLLED PGD ITERATION 9 / 10                                             *)
(* ========================================================================= *)
x_err[1] := x_rollout[1] - x_ref[1];
x_err[2] := x_rollout[2] - x_ref[2];
x_err[3] := x_rollout[3] - x_ref[3];
x_err[4] := x_rollout[4] - x_ref[4];
x_err[5] := (x_rollout[5] - x_ref[5]) * rDynamicGradePenaltyWeight;
x_err[6] := x_rollout[6] - x_ref[6];

lambda_costate[1] := (P_Weight[1,1]*x_err[1]) + (P_Weight[1,2]*x_err[2]) + (P_Weight[1,3]*x_err[3]) + (P_Weight[1,4]*x_err[4]) + (P_Weight[1,5]*x_err[5]) + (P_Weight[1,6]*x_err[6]);
lambda_costate[2] := (P_Weight[2,1]*x_err[1]) + (P_Weight[2,2]*x_err[2]) + (P_Weight[2,3]*x_err[3]) + (P_Weight[2,4]*x_err[4]) + (P_Weight[2,5]*x_err[5]) + (P_Weight[2,6]*x_err[6]);
lambda_costate[3] := (P_Weight[3,1]*x_err[1]) + (P_Weight[3,2]*x_err[2]) + (P_Weight[3,3]*x_err[3]) + (P_Weight[3,4]*x_err[4]) + (P_Weight[3,5]*x_err[5]) + (P_Weight[3,6]*x_err[6]);
lambda_costate[4] := (P_Weight[4,1]*x_err[1]) + (P_Weight[4,2]*x_err[2]) + (P_Weight[4,3]*x_err[3]) + (P_Weight[4,4]*x_err[4]) + (P_Weight[4,5]*x_err[5]) + (P_Weight[4,6]*x_err[6]);
lambda_costate[5] := (P_Weight[5,1]*x_err[1]) + (P_Weight[5,2]*x_err[2]) + (P_Weight[5,3]*x_err[3]) + (P_Weight[5,4]*x_err[4]) + (P_Weight[5,5]*x_err[5]) + (P_Weight[5,6]*x_err[6]);
lambda_costate[6] := (P_Weight[6,1]*x_err[1]) + (P_Weight[6,2]*x_err[2]) + (P_Weight[6,3]*x_err[3]) + (P_Weight[6,4]*x_err[4]) + (P_Weight[6,5]*x_err[5]) + (P_Weight[6,6]*x_err[6]);

grad_J[1] := (R_Weight[1,1]*u_cand[1]) + (S_Weight[1,1]*(u_cand[1] - u_prev[1])) + (B_Matrix[1,1]*lambda_costate[1]) + (B_Matrix[2,1]*lambda_costate[2]) + (B_Matrix[3,1]*lambda_costate[3]) + (B_Matrix[4,1]*lambda_costate[4]) + (B_Matrix[5,1]*lambda_costate[5]) + (B_Matrix[6,1]*lambda_costate[6]);
grad_J[2] := (R_Weight[2,2]*u_cand[2]) + (S_Weight[2,2]*(u_cand[2] - u_prev[2])) + (B_Matrix[1,2]*lambda_costate[1]) + (B_Matrix[2,2]*lambda_costate[2]) + (B_Matrix[3,2]*lambda_costate[3]) + (B_Matrix[4,2]*lambda_costate[4]) + (B_Matrix[5,2]*lambda_costate[5]) + (B_Matrix[6,2]*lambda_costate[6]);
grad_J[3] := (R_Weight[3,3]*u_cand[3]) + (S_Weight[3,3]*(u_cand[3] - u_prev[3])) + (B_Matrix[1,3]*lambda_costate[1]) + (B_Matrix[2,3]*lambda_costate[2]) + (B_Matrix[3,3]*lambda_costate[3]) + (B_Matrix[4,3]*lambda_costate[4]) + (B_Matrix[5,3]*lambda_costate[5]) + (B_Matrix[6,3]*lambda_costate[6]);
grad_J[4] := (R_Weight[4,4]*u_cand[4]) + (S_Weight[4,4]*(u_cand[4] - u_prev[4])) + (B_Matrix[1,4]*lambda_costate[1]) + (B_Matrix[2,4]*lambda_costate[2]) + (B_Matrix[3,4]*lambda_costate[3]) + (B_Matrix[4,4]*lambda_costate[4]) + (B_Matrix[5,4]*lambda_costate[5]) + (B_Matrix[6,4]*lambda_costate[6]);
grad_J[5] := (R_Weight[5,5]*u_cand[5]) + (S_Weight[5,5]*(u_cand[5] - u_prev[5])) + (B_Matrix[1,5]*lambda_costate[1]) + (B_Matrix[2,5]*lambda_costate[2]) + (B_Matrix[3,5]*lambda_costate[3]) + (B_Matrix[4,5]*lambda_costate[4]) + (B_Matrix[5,5]*lambda_costate[5]) + (B_Matrix[6,5]*lambda_costate[6]);

rTempDelta := (u_cand[1] - (rPGD_StepSize * grad_J[1])) - u_prev[1];
IF rTempDelta < du_min[1] THEN rTempDelta := du_min[1]; ELSIF rTempDelta > du_max[1] THEN rTempDelta := du_max[1]; END_IF;
u_cand[1] := u_prev[1] + rTempDelta;
IF u_cand[1] < u_min[1] THEN u_cand[1] := u_min[1]; ELSIF u_cand[1] > u_max[1] THEN u_cand[1] := u_max[1]; END_IF;

rTempDelta := (u_cand[2] - (rPGD_StepSize * grad_J[2])) - u_prev[2];
IF rTempDelta < du_min[2] THEN rTempDelta := du_min[2]; ELSIF rTempDelta > du_max[2] THEN rTempDelta := du_max[2]; END_IF;
u_cand[2] := u_prev[2] + rTempDelta;
IF u_cand[2] < u_min[2] THEN u_cand[2] := u_min[2]; ELSIF u_cand[2] > u_max[2] THEN u_cand[2] := u_max[2]; END_IF;

rTempDelta := (u_cand[3] - (rPGD_StepSize * grad_J[3])) - u_prev[3];
IF rTempDelta < du_min[3] THEN rTempDelta := du_min[3]; ELSIF rTempDelta > du_max[3] THEN rTempDelta := du_max[3]; END_IF;
u_cand[3] := u_prev[3] + rTempDelta;
IF u_cand[3] < u_min[3] THEN u_cand[3] := u_min[3]; ELSIF u_cand[3] > u_max[3] THEN u_cand[3] := u_max[3]; END_IF;

rTempDelta := (u_cand[4] - (rPGD_StepSize * grad_J[4])) - u_prev[4];
IF rTempDelta < du_min[4] THEN rTempDelta := du_min[4]; ELSIF rTempDelta > du_max[4] THEN rTempDelta := du_max[4]; END_IF;
u_cand[4] := u_prev[4] + rTempDelta;
IF u_cand[4] < u_min[4] THEN u_cand[4] := u_min[4]; ELSIF u_cand[4] > u_max[4] THEN u_cand[4] := u_max[4]; END_IF;

rTempDelta := (u_cand[5] - (rPGD_StepSize * grad_J[5])) - u_prev[5];
IF rTempDelta < du_min[5] THEN rTempDelta := du_min[5]; ELSIF rTempDelta > du_max[5] THEN rTempDelta := du_max[5]; END_IF;
u_cand[5] := u_prev[5] + rTempDelta;
IF u_cand[5] < u_min[5] THEN u_cand[5] := u_min[5]; ELSIF u_cand[5] > u_max[5] THEN u_cand[5] := u_max[5]; END_IF;

x_rollout[1] := (A_Matrix[1,1]*x_hat[1]) + (A_Matrix[1,2]*x_hat[2]) + (A_Matrix[1,3]*x_hat[3]) + (A_Matrix[1,4]*x_hat[4]) + (A_Matrix[1,5]*x_hat[5]) + (A_Matrix[1,6]*x_hat[6]) + (B_Matrix[1,1]*u_cand[1]) + (B_Matrix[1,2]*u_cand[2]) + (B_Matrix[1,3]*u_cand[3]) + (B_Matrix[1,4]*u_cand[4]) + (B_Matrix[1,5]*u_cand[5]);
x_rollout[2] := (A_Matrix[2,1]*x_hat[1]) + (A_Matrix[2,2]*x_hat[2]) + (A_Matrix[2,3]*x_hat[3]) + (A_Matrix[2,4]*x_hat[4]) + (A_Matrix[2,5]*x_hat[5]) + (A_Matrix[2,6]*x_hat[6]) + (B_Matrix[2,1]*u_cand[1]) + (B_Matrix[2,2]*u_cand[2]) + (B_Matrix[2,3]*u_cand[3]) + (B_Matrix[2,4]*u_cand[4]) + (B_Matrix[2,5]*u_cand[5]);
x_rollout[3] := (A_Matrix[3,1]*x_hat[1]) + (A_Matrix[3,2]*x_hat[2]) + (A_Matrix[3,3]*x_hat[3]) + (A_Matrix[3,4]*x_hat[4]) + (A_Matrix[3,5]*x_hat[5]) + (A_Matrix[3,6]*x_hat[6]) + (B_Matrix[3,1]*u_cand[1]) + (B_Matrix[3,2]*u_cand[2]) + (B_Matrix[3,3]*u_cand[3]) + (B_Matrix[3,4]*u_cand[4]) + (B_Matrix[3,5]*u_cand[5]);
x_rollout[4] := (A_Matrix[4,1]*x_hat[1]) + (A_Matrix[4,2]*x_hat[2]) + (A_Matrix[4,3]*x_hat[3]) + (A_Matrix[4,4]*x_hat[4]) + (A_Matrix[4,5]*x_hat[5]) + (A_Matrix[4,6]*x_hat[6]) + (B_Matrix[4,1]*u_cand[1]) + (B_Matrix[4,2]*u_cand[2]) + (B_Matrix[4,3]*u_cand[3]) + (B_Matrix[4,4]*u_cand[4]) + (B_Matrix[4,5]*u_cand[5]);
x_rollout[5] := (A_Matrix[5,1]*x_hat[1]) + (A_Matrix[5,2]*x_hat[2]) + (A_Matrix[5,3]*x_hat[3]) + (A_Matrix[5,4]*x_hat[4]) + (A_Matrix[5,5]*x_hat[5]) + (A_Matrix[5,6]*x_hat[6]) + (B_Matrix[5,1]*u_cand[1]) + (B_Matrix[5,2]*u_cand[2]) + (B_Matrix[5,3]*u_cand[3]) + (B_Matrix[5,4]*u_cand[4]) + (B_Matrix[5,5]*u_cand[5]);
x_rollout[6] := (A_Matrix[6,1]*x_hat[1]) + (A_Matrix[6,2]*x_hat[2]) + (A_Matrix[6,3]*x_hat[3]) + (A_Matrix[6,4]*x_hat[4]) + (A_Matrix[6,5]*x_hat[5]) + (A_Matrix[6,6]*x_hat[6]) + (B_Matrix[6,1]*u_cand[1]) + (B_Matrix[6,2]*u_cand[2]) + (B_Matrix[6,3]*u_cand[3]) + (B_Matrix[6,4]*u_cand[4]) + (B_Matrix[6,5]*u_cand[5]);


(* ========================================================================= *)
(* UNROLLED PGD ITERATION 10 / 10 (FINAL CONVERGED STEP)                     *)
(* ========================================================================= *)
x_err[1] := x_rollout[1] - x_ref[1];
x_err[2] := x_rollout[2] - x_ref[2];
x_err[3] := x_rollout[3] - x_ref[3];
x_err[4] := x_rollout[4] - x_ref[4];
x_err[5] := (x_rollout[5] - x_ref[5]) * rDynamicGradePenaltyWeight;
x_err[6] := x_rollout[6] - x_ref[6];

lambda_costate[1] := (P_Weight[1,1]*x_err[1]) + (P_Weight[1,2]*x_err[2]) + (P_Weight[1,3]*x_err[3]) + (P_Weight[1,4]*x_err[4]) + (P_Weight[1,5]*x_err[5]) + (P_Weight[1,6]*x_err[6]);
lambda_costate[2] := (P_Weight[2,1]*x_err[1]) + (P_Weight[2,2]*x_err[2]) + (P_Weight[2,3]*x_err[3]) + (P_Weight[2,4]*x_err[4]) + (P_Weight[2,5]*x_err[5]) + (P_Weight[2,6]*x_err[6]);
lambda_costate[3] := (P_Weight[3,1]*x_err[1]) + (P_Weight[3,2]*x_err[2]) + (P_Weight[3,3]*x_err[3]) + (P_Weight[3,4]*x_err[4]) + (P_Weight[3,5]*x_err[5]) + (P_Weight[3,6]*x_err[6]);
lambda_costate[4] := (P_Weight[4,1]*x_err[1]) + (P_Weight[4,2]*x_err[2]) + (P_Weight[4,3]*x_err[3]) + (P_Weight[4,4]*x_err[4]) + (P_Weight[4,5]*x_err[5]) + (P_Weight[4,6]*x_err[6]);
lambda_costate[5] := (P_Weight[5,1]*x_err[1]) + (P_Weight[5,2]*x_err[2]) + (P_Weight[5,3]*x_err[3]) + (P_Weight[5,4]*x_err[4]) + (P_Weight[5,5]*x_err[5]) + (P_Weight[5,6]*x_err[6]);
lambda_costate[6] := (P_Weight[6,1]*x_err[1]) + (P_Weight[6,2]*x_err[2]) + (P_Weight[6,3]*x_err[3]) + (P_Weight[6,4]*x_err[4]) + (P_Weight[6,5]*x_err[5]) + (P_Weight[6,6]*x_err[6]);

grad_J[1] := (R_Weight[1,1]*u_cand[1]) + (S_Weight[1,1]*(u_cand[1] - u_prev[1])) + (B_Matrix[1,1]*lambda_costate[1]) + (B_Matrix[2,1]*lambda_costate[2]) + (B_Matrix[3,1]*lambda_costate[3]) + (B_Matrix[4,1]*lambda_costate[4]) + (B_Matrix[5,1]*lambda_costate[5]) + (B_Matrix[6,1]*lambda_costate[6]);
grad_J[2] := (R_Weight[2,2]*u_cand[2]) + (S_Weight[2,2]*(u_cand[2] - u_prev[2])) + (B_Matrix[1,2]*lambda_costate[1]) + (B_Matrix[2,2]*lambda_costate[2]) + (B_Matrix[3,2]*lambda_costate[3]) + (B_Matrix[4,2]*lambda_costate[4]) + (B_Matrix[5,2]*lambda_costate[5]) + (B_Matrix[6,2]*lambda_costate[6]);
grad_J[3] := (R_Weight[3,3]*u_cand[3]) + (S_Weight[3,3]*(u_cand[3] - u_prev[3])) + (B_Matrix[1,3]*lambda_costate[1]) + (B_Matrix[2,3]*lambda_costate[2]) + (B_Matrix[3,3]*lambda_costate[3]) + (B_Matrix[4,3]*lambda_costate[4]) + (B_Matrix[5,3]*lambda_costate[5]) + (B_Matrix[6,3]*lambda_costate[6]);
grad_J[4] := (R_Weight[4,4]*u_cand[4]) + (S_Weight[4,4]*(u_cand[4] - u_prev[4])) + (B_Matrix[1,4]*lambda_costate[1]) + (B_Matrix[2,4]*lambda_costate[2]) + (B_Matrix[3,4]*lambda_costate[3]) + (B_Matrix[4,4]*lambda_costate[4]) + (B_Matrix[5,4]*lambda_costate[5]) + (B_Matrix[6,4]*lambda_costate[6]);
grad_J[5] := (R_Weight[5,5]*u_cand[5]) + (S_Weight[5,5]*(u_cand[5] - u_prev[5])) + (B_Matrix[1,5]*lambda_costate[1]) + (B_Matrix[2,5]*lambda_costate[2]) + (B_Matrix[3,5]*lambda_costate[3]) + (B_Matrix[4,5]*lambda_costate[4]) + (B_Matrix[5,5]*lambda_costate[5]) + (B_Matrix[6,5]*lambda_costate[6]);

rTempDelta := (u_cand[1] - (rPGD_StepSize * grad_J[1])) - u_prev[1];
IF rTempDelta < du_min[1] THEN rTempDelta := du_min[1]; ELSIF rTempDelta > du_max[1] THEN rTempDelta := du_max[1]; END_IF;
u_cand[1] := u_prev[1] + rTempDelta;
IF u_cand[1] < u_min[1] THEN u_cand[1] := u_min[1]; ELSIF u_cand[1] > u_max[1] THEN u_cand[1] := u_max[1]; END_IF;

rTempDelta := (u_cand[2] - (rPGD_StepSize * grad_J[2])) - u_prev[2];
IF rTempDelta < du_min[2] THEN rTempDelta := du_min[2]; ELSIF rTempDelta > du_max[2] THEN rTempDelta := du_max[2]; END_IF;
u_cand[2] := u_prev[2] + rTempDelta;
IF u_cand[2] < u_min[2] THEN u_cand[2] := u_min[2]; ELSIF u_cand[2] > u_max[2] THEN u_cand[2] := u_max[2]; END_IF;

rTempDelta := (u_cand[3] - (rPGD_StepSize * grad_J[3])) - u_prev[3];
IF rTempDelta < du_min[3] THEN rTempDelta := du_min[3]; ELSIF rTempDelta > du_max[3] THEN rTempDelta := du_max[3]; END_IF;
u_cand[3] := u_prev[3] + rTempDelta;
IF u_cand[3] < u_min[3] THEN u_cand[3] := u_min[3]; ELSIF u_cand[3] > u_max[3] THEN u_cand[3] := u_max[3]; END_IF;

rTempDelta := (u_cand[4] - (rPGD_StepSize * grad_J[4])) - u_prev[4];
IF rTempDelta < du_min[4] THEN rTempDelta := du_min[4]; ELSIF rTempDelta > du_max[4] THEN rTempDelta := du_max[4]; END_IF;
u_cand[4] := u_prev[4] + rTempDelta;
IF u_cand[4] < u_min[4] THEN u_cand[4] := u_min[4]; ELSIF u_cand[4] > u_max[4] THEN u_cand[4] := u_max[4]; END_IF;

rTempDelta := (u_cand[5] - (rPGD_StepSize * grad_J[5])) - u_prev[5];
IF rTempDelta < du_min[5] THEN rTempDelta := du_min[5]; ELSIF rTempDelta > du_max[5] THEN rTempDelta := du_max[5]; END_IF;
u_cand[5] := u_prev[5] + rTempDelta;
IF u_cand[5] < u_min[5] THEN u_cand[5] := u_min[5]; ELSIF u_cand[5] > u_max[5] THEN u_cand[5] := u_max[5]; END_IF;

(* Optimized Actuator Commands Ready for Supervisory Mode Gate *)
u_opt[1] := u_cand[1];
u_opt[2] := u_cand[2];
u_opt[3] := u_cand[3];
u_opt[4] := u_cand[4];
u_opt[5] := u_cand[5];
"""
