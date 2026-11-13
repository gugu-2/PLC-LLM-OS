# lyophilizer_builder/build_st_phase4_mpc.py

def get_phase4_mpc():
    code = """(* === PHASE 4: RECEDING-HORIZON MPC OPTIMIZATION WITH 10 UNROLLED PGD ITERATIONS === *)
(* ---------------------------------------------------------------------------------------------------- *)
(* SETUP MPC TARGET REFERENCE TRAJECTORY & COLLAPSE BARRIERS                                           *)
(* ---------------------------------------------------------------------------------------------------- *)
vecX_ref[1] := rTargetShelfTemp_degC;
vecX_ref[2] := rTargetShelfTemp_degC;
vecX_ref[3] := MIN(rTargetShelfTemp_degC, rCollapseTempLimit_degC - 1.25);
vecX_ref[4] := rTargetChamberPress_mbar;
vecX_ref[5] := -85.0; (* Condenser setpoint *)
vecX_ref[6] := rCakeThicknessMax_mm;

(* Initialize Candidate Control Vector from Current Actuator Setpoint *)
vecU_opt[1] := vecU[1];
vecU_opt[2] := vecU[2];
vecU_opt[3] := vecU[3];
vecU_opt[4] := vecU[4];
vecU_opt[5] := vecU[5];
"""

    # Unroll 10 PGD iterations explicitly
    for it in range(1, 11):
        code += f"""
(* ---------------------------------------------------------------------------------------------------- *)
(* PGD OPTIMIZATION ITERATION {it} OF 10                                                                 *)
(* ---------------------------------------------------------------------------------------------------- *)
(* 1. Forward Horizon State Prediction using Candidate Actuator Vector vecU_opt *)
vecX_pred[1] := (matA[1,1] * vecX_hat[1]) + (matA[1,2] * vecX_hat[2]) + (matA[1,3] * vecX_hat[3]) +
                (matA[1,4] * vecX_hat[4]) + (matA[1,5] * vecX_hat[5]) + (matA[1,6] * vecX_hat[6]) +
                (matB[1,1] * vecU_opt[1]) + (matB[1,2] * vecU_opt[2]) + (matB[1,3] * vecU_opt[3]) +
                (matB[1,4] * vecU_opt[4]) + (matB[1,5] * vecU_opt[5]);

vecX_pred[2] := (matA[2,1] * vecX_hat[1]) + (matA[2,2] * vecX_hat[2]) + (matA[2,3] * vecX_hat[3]) +
                (matA[2,4] * vecX_hat[4]) + (matA[2,5] * vecX_hat[5]) + (matA[2,6] * vecX_hat[6]) +
                (matB[2,1] * vecU_opt[1]) + (matB[2,2] * vecU_opt[2]) + (matB[2,3] * vecU_opt[3]) +
                (matB[2,4] * vecU_opt[4]) + (matB[2,5] * vecU_opt[5]);

vecX_pred[3] := (matA[3,1] * vecX_hat[1]) + (matA[3,2] * vecX_hat[2]) + (matA[3,3] * vecX_hat[3]) +
                (matA[3,4] * vecX_hat[4]) + (matA[3,5] * vecX_hat[5]) + (matA[3,6] * vecX_hat[6]) +
                (matB[3,1] * vecU_opt[1]) + (matB[3,2] * vecU_opt[2]) + (matB[3,3] * vecU_opt[3]) +
                (matB[3,4] * vecU_opt[4]) + (matB[3,5] * vecU_opt[5]);

vecX_pred[4] := (matA[4,1] * vecX_hat[1]) + (matA[4,2] * vecX_hat[2]) + (matA[4,3] * vecX_hat[3]) +
                (matA[4,4] * vecX_hat[4]) + (matA[4,5] * vecX_hat[5]) + (matA[4,6] * vecX_hat[6]) +
                (matB[4,1] * vecU_opt[1]) + (matB[4,2] * vecU_opt[2]) + (matB[4,3] * vecU_opt[3]) +
                (matB[4,4] * vecU_opt[4]) + (matB[4,5] * vecU_opt[5]);

vecX_pred[5] := (matA[5,1] * vecX_hat[1]) + (matA[5,2] * vecX_hat[2]) + (matA[5,3] * vecX_hat[3]) +
                (matA[5,4] * vecX_hat[4]) + (matA[5,5] * vecX_hat[5]) + (matA[5,6] * vecX_hat[6]) +
                (matB[5,1] * vecU_opt[1]) + (matB[5,2] * vecU_opt[2]) + (matB[5,3] * vecU_opt[3]) +
                (matB[5,4] * vecU_opt[4]) + (matB[5,5] * vecU_opt[5]);

vecX_pred[6] := (matA[6,1] * vecX_hat[1]) + (matA[6,2] * vecX_hat[2]) + (matA[6,3] * vecX_hat[3]) +
                (matA[6,4] * vecX_hat[4]) + (matA[6,5] * vecX_hat[5]) + (matA[6,6] * vecX_hat[6]) +
                (matB[6,1] * vecU_opt[1]) + (matB[6,2] * vecU_opt[2]) + (matB[6,3] * vecU_opt[3]) +
                (matB[6,4] * vecU_opt[4]) + (matB[6,5] * vecU_opt[5]);

(* 2. Predicted State Tracking Errors *)
vecX_err[1] := vecX_pred[1] - vecX_ref[1];
vecX_err[2] := vecX_pred[2] - vecX_ref[2];
vecX_err[3] := vecX_pred[3] - vecX_ref[3];
vecX_err[4] := vecX_pred[4] - vecX_ref[4];
vecX_err[5] := vecX_pred[5] - vecX_ref[5];
vecX_err[6] := vecX_pred[6] - vecX_ref[6];

(* 3. Non-Linear Cake Collapse Barrier Penalty Function *)
IF vecX_pred[3] > (rCollapseTempLimit_degC - 0.50) THEN
    rTempViolationPenalty := (vecX_pred[3] - (rCollapseTempLimit_degC - 0.50)) * 650.0;
ELSE
    rTempViolationPenalty := 0.0;
END_IF;

(* 4. Adjoint Costate Backpropagation: lambda = Q * e + P * e + Barrier *)
vecLambda[1] := (matQ[1,1] * vecX_err[1]) + (matP[1,1] * vecX_err[1] * 0.150);
vecLambda[2] := (matQ[2,2] * vecX_err[2]) + (matP[2,2] * vecX_err[2] * 0.150);
vecLambda[3] := (matQ[3,3] * vecX_err[3]) + (matP[3,3] * vecX_err[3] * 0.150) + rTempViolationPenalty;
vecLambda[4] := (matQ[4,4] * vecX_err[4]) + (matP[4,4] * vecX_err[4] * 0.150);
vecLambda[5] := (matQ[5,5] * vecX_err[5]) + (matP[5,5] * vecX_err[5] * 0.150);
vecLambda[6] := (matQ[6,6] * vecX_err[6]) + (matP[6,6] * vecX_err[6] * 0.150);

(* Adjoint State Transition Propagation (A^T * lambda) *)
vecLambda[1] := vecLambda[1] + ((matA[1,1]*vecLambda[1] + matA[2,1]*vecLambda[2] + matA[3,1]*vecLambda[3] +
                                matA[4,1]*vecLambda[4] + matA[5,1]*vecLambda[5] + matA[6,1]*vecLambda[6]) * 0.125);
vecLambda[2] := vecLambda[2] + ((matA[1,2]*vecLambda[1] + matA[2,2]*vecLambda[2] + matA[3,2]*vecLambda[3] +
                                matA[4,2]*vecLambda[4] + matA[5,2]*vecLambda[5] + matA[6,2]*vecLambda[6]) * 0.125);
vecLambda[3] := vecLambda[3] + ((matA[1,3]*vecLambda[1] + matA[2,3]*vecLambda[2] + matA[3,3]*vecLambda[3] +
                                matA[4,3]*vecLambda[4] + matA[5,3]*vecLambda[5] + matA[6,3]*vecLambda[6]) * 0.125);
vecLambda[4] := vecLambda[4] + ((matA[1,4]*vecLambda[1] + matA[2,4]*vecLambda[2] + matA[3,4]*vecLambda[3] +
                                matA[4,4]*vecLambda[4] + matA[5,4]*vecLambda[5] + matA[6,4]*vecLambda[6]) * 0.125);
vecLambda[5] := vecLambda[5] + ((matA[1,5]*vecLambda[1] + matA[2,5]*vecLambda[2] + matA[3,5]*vecLambda[3] +
                                matA[4,5]*vecLambda[4] + matA[5,5]*vecLambda[5] + matA[6,5]*vecLambda[6]) * 0.125);
vecLambda[6] := vecLambda[6] + ((matA[1,6]*vecLambda[1] + matA[2,6]*vecLambda[2] + matA[3,6]*vecLambda[3] +
                                matA[4,6]*vecLambda[4] + matA[5,6]*vecLambda[5] + matA[6,6]*vecLambda[6]) * 0.125);

(* 5. Actuator Cost Gradients: grad_u = R * u + S * (u - u_prev) + B^T * lambda *)
vecGradU[1] := (matR[1,1] * vecU_opt[1]) + (matS[1,1] * (vecU_opt[1] - vecU_prev[1])) +
               (matB[1,1] * vecLambda[1]) + (matB[2,1] * vecLambda[2]) + (matB[3,1] * vecLambda[3]) +
               (matB[4,1] * vecLambda[4]) + (matB[5,1] * vecLambda[5]) + (matB[6,1] * vecLambda[6]);

vecGradU[2] := (matR[2,2] * vecU_opt[2]) + (matS[2,2] * (vecU_opt[2] - vecU_prev[2])) +
               (matB[1,2] * vecLambda[1]) + (matB[2,2] * vecLambda[2]) + (matB[3,2] * vecLambda[3]) +
               (matB[4,2] * vecLambda[4]) + (matB[5,2] * vecLambda[5]) + (matB[6,2] * vecLambda[6]);

vecGradU[3] := (matR[3,3] * vecU_opt[3]) + (matS[3,3] * (vecU_opt[3] - vecU_prev[3])) +
               (matB[1,3] * vecLambda[1]) + (matB[2,3] * vecLambda[2]) + (matB[3,3] * vecLambda[3]) +
               (matB[4,3] * vecLambda[4]) + (matB[5,3] * vecLambda[5]) + (matB[6,3] * vecLambda[6]);

vecGradU[4] := (matR[4,4] * vecU_opt[4]) + (matS[4,4] * (vecU_opt[4] - vecU_prev[4])) +
               (matB[1,4] * vecLambda[1]) + (matB[2,4] * vecLambda[2]) + (matB[3,4] * vecLambda[3]) +
               (matB[4,4] * vecLambda[4]) + (matB[5,4] * vecLambda[5]) + (matB[6,4] * vecLambda[6]);

vecGradU[5] := (matR[5,5] * vecU_opt[5]) + (matS[5,5] * (vecU_opt[5] - vecU_prev[5])) +
               (matB[1,5] * vecLambda[1]) + (matB[2,5] * vecLambda[2]) + (matB[3,5] * vecLambda[3]) +
               (matB[4,5] * vecLambda[4]) + (matB[5,5] * vecLambda[5]) + (matB[6,5] * vecLambda[6]);

(* 6. Projected Gradient Descent Input Updates *)
vecU_opt[1] := vecU_opt[1] - (rPGD_Alpha * vecGradU[1]);
vecU_opt[2] := vecU_opt[2] - (rPGD_Alpha * vecGradU[2]);
vecU_opt[3] := vecU_opt[3] - (rPGD_Alpha * vecGradU[3]);
vecU_opt[4] := vecU_opt[4] - (rPGD_Alpha * vecGradU[4]);
vecU_opt[5] := vecU_opt[5] - (rPGD_Alpha * vecGradU[5]);

(* 7. Slew Rate Limit Projections *)
rStepSlew := vecU_opt[1] - vecU_prev[1];
IF rStepSlew > vecU_slew_max[1] THEN
    vecU_opt[1] := vecU_prev[1] + vecU_slew_max[1];
ELSIF rStepSlew < -vecU_slew_max[1] THEN
    vecU_opt[1] := vecU_prev[1] - vecU_slew_max[1];
END_IF;

rStepSlew := vecU_opt[2] - vecU_prev[2];
IF rStepSlew > vecU_slew_max[2] THEN
    vecU_opt[2] := vecU_prev[2] + vecU_slew_max[2];
ELSIF rStepSlew < -vecU_slew_max[2] THEN
    vecU_opt[2] := vecU_prev[2] - vecU_slew_max[2];
END_IF;

rStepSlew := vecU_opt[3] - vecU_prev[3];
IF rStepSlew > vecU_slew_max[3] THEN
    vecU_opt[3] := vecU_prev[3] + vecU_slew_max[3];
ELSIF rStepSlew < -vecU_slew_max[3] THEN
    vecU_opt[3] := vecU_prev[3] - vecU_slew_max[3];
END_IF;

rStepSlew := vecU_opt[4] - vecU_prev[4];
IF rStepSlew > vecU_slew_max[4] THEN
    vecU_opt[4] := vecU_prev[4] + vecU_slew_max[4];
ELSIF rStepSlew < -vecU_slew_max[4] THEN
    vecU_opt[4] := vecU_prev[4] - vecU_slew_max[4];
END_IF;

rStepSlew := vecU_opt[5] - vecU_prev[5];
IF rStepSlew > vecU_slew_max[5] THEN
    vecU_opt[5] := vecU_prev[5] + vecU_slew_max[5];
ELSIF rStepSlew < -vecU_slew_max[5] THEN
    vecU_opt[5] := vecU_prev[5] - vecU_slew_max[5];
END_IF;

(* 8. Box Constrained Saturation Projections [u_min, u_max] *)
vecU_opt[1] := MAX(vecU_min[1], MIN(vecU_max[1], vecU_opt[1]));
vecU_opt[2] := MAX(vecU_min[2], MIN(vecU_max[2], vecU_opt[2]));
vecU_opt[3] := MAX(vecU_min[3], MIN(vecU_max[3], vecU_opt[3]));
vecU_opt[4] := MAX(vecU_min[4], MIN(vecU_max[4], vecU_opt[4]));
vecU_opt[5] := MAX(vecU_min[5], MIN(vecU_max[5], vecU_opt[5]));

(* 9. Hard Collapse Safety Barrier Invariant Override *)
IF vecX_pred[3] >= (rCollapseTempLimit_degC - 0.25) THEN
    vecU_opt[1] := 0.0; (* Instantly quench shelf thyristor heating *)
    vecU_opt[2] := MAX(vecU_opt[2], 30.0); (* Engage shelf refrigeration injection *)
END_IF;
"""

    code += """
(* ---------------------------------------------------------------------------------------------------- *)
(* COMMIT OPTIMIZED CONTROL COMMANDS TO ACTUATOR DRIVER REGISTERS                                       *)
(* ---------------------------------------------------------------------------------------------------- *)
IF bAutoMode AND (nFsmState = 8) THEN
    vecU[1] := vecU_opt[1];
    vecU[2] := vecU_opt[2];
    vecU[3] := vecU_opt[3];
    vecU[4] := vecU_opt[4];
    vecU[5] := vecU_opt[5];
END_IF;
"""
    return code
