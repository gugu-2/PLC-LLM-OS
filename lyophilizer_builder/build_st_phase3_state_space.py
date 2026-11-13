# lyophilizer_builder/build_st_phase3_state_space.py

def get_phase3_state_space():
    return """(* === PHASE 3: FIRST-PRINCIPLES CYBER-PHYSICAL STATE-SPACE ESTIMATION === *)
(* ---------------------------------------------------------------------------------------------------- *)
(* SYNTHESIZE SENSOR MEASUREMENT VECTOR y[k] (6x1)                                                      *)
(* ---------------------------------------------------------------------------------------------------- *)
vecY_meas[1] := rVotedShelfFluidTemp;
vecY_meas[2] := rVotedProductVialTemp;
vecY_meas[3] := vecX_hat[3]; (* Sublimation interface proxy *)
vecY_meas[4] := rVotedCap;
vecY_meas[5] := rCondenserVotedTemp;
vecY_meas[6] := vecX_hat[6];

(* ---------------------------------------------------------------------------------------------------- *)
(* ESTIMATED OUTPUT COMPUTATION: y_est = C * x_hat (6x1)                                                *)
(* ---------------------------------------------------------------------------------------------------- *)
vecY_est[1] := (matC[1,1] * vecX_hat[1]) + (matC[1,2] * vecX_hat[2]) + (matC[1,3] * vecX_hat[3]) +
               (matC[1,4] * vecX_hat[4]) + (matC[1,5] * vecX_hat[5]) + (matC[1,6] * vecX_hat[6]);

vecY_est[2] := (matC[2,1] * vecX_hat[1]) + (matC[2,2] * vecX_hat[2]) + (matC[2,3] * vecX_hat[3]) +
               (matC[2,4] * vecX_hat[4]) + (matC[2,5] * vecX_hat[5]) + (matC[2,6] * vecX_hat[6]);

vecY_est[3] := (matC[3,1] * vecX_hat[1]) + (matC[3,2] * vecX_hat[2]) + (matC[3,3] * vecX_hat[3]) +
               (matC[3,4] * vecX_hat[4]) + (matC[3,5] * vecX_hat[5]) + (matC[3,6] * vecX_hat[6]);

vecY_est[4] := (matC[4,1] * vecX_hat[1]) + (matC[4,2] * vecX_hat[2]) + (matC[4,3] * vecX_hat[3]) +
               (matC[4,4] * vecX_hat[4]) + (matC[4,5] * vecX_hat[5]) + (matC[4,6] * vecX_hat[6]);

vecY_est[5] := (matC[5,1] * vecX_hat[1]) + (matC[5,2] * vecX_hat[2]) + (matC[5,3] * vecX_hat[3]) +
               (matC[5,4] * vecX_hat[4]) + (matC[5,5] * vecX_hat[5]) + (matC[5,6] * vecX_hat[6]);

vecY_est[6] := (matC[6,1] * vecX_hat[1]) + (matC[6,2] * vecX_hat[2]) + (matC[6,3] * vecX_hat[3]) +
               (matC[6,4] * vecX_hat[4]) + (matC[6,5] * vecX_hat[5]) + (matC[6,6] * vecX_hat[6]);

(* Innovation Residuals: e = y_meas - y_est *)
vecInnov[1] := vecY_meas[1] - vecY_est[1];
vecInnov[2] := vecY_meas[2] - vecY_est[2];
vecInnov[3] := vecY_meas[3] - vecY_est[3];
vecInnov[4] := vecY_meas[4] - vecY_est[4];
vecInnov[5] := vecY_meas[5] - vecY_est[5];
vecInnov[6] := vecY_meas[6] - vecY_est[6];

(* ---------------------------------------------------------------------------------------------------- *)
(* LUENBERGER OBSERVER INNOVATION UPDATE: dx_obs = L * vecInnov (6x1)                                   *)
(* ---------------------------------------------------------------------------------------------------- *)
vecObsUpdate[1] := (matL[1,1] * vecInnov[1]) + (matL[1,2] * vecInnov[2]) + (matL[1,3] * vecInnov[3]) +
                   (matL[1,4] * vecInnov[4]) + (matL[1,5] * vecInnov[5]) + (matL[1,6] * vecInnov[6]);

vecObsUpdate[2] := (matL[2,1] * vecInnov[1]) + (matL[2,2] * vecInnov[2]) + (matL[2,3] * vecInnov[3]) +
                   (matL[2,4] * vecInnov[4]) + (matL[2,5] * vecInnov[5]) + (matL[2,6] * vecInnov[6]);

vecObsUpdate[3] := (matL[3,1] * vecInnov[1]) + (matL[3,2] * vecInnov[2]) + (matL[3,3] * vecInnov[3]) +
                   (matL[3,4] * vecInnov[4]) + (matL[3,5] * vecInnov[5]) + (matL[3,6] * vecInnov[6]);

vecObsUpdate[4] := (matL[4,1] * vecInnov[1]) + (matL[4,2] * vecInnov[2]) + (matL[4,3] * vecInnov[3]) +
                   (matL[4,4] * vecInnov[4]) + (matL[4,5] * vecInnov[5]) + (matL[4,6] * vecInnov[6]);

vecObsUpdate[5] := (matL[5,1] * vecInnov[1]) + (matL[5,2] * vecInnov[2]) + (matL[5,3] * vecInnov[3]) +
                   (matL[5,4] * vecInnov[4]) + (matL[5,5] * vecInnov[5]) + (matL[5,6] * vecInnov[6]);

vecObsUpdate[6] := (matL[6,1] * vecInnov[1]) + (matL[6,2] * vecInnov[2]) + (matL[6,3] * vecInnov[3]) +
                   (matL[6,4] * vecInnov[4]) + (matL[6,5] * vecInnov[5]) + (matL[6,6] * vecInnov[6]);

(* ---------------------------------------------------------------------------------------------------- *)
(* DISCRETE STATE PROPAGATION: x[k+1] = A * x[k] + B * u[k] + dx_obs (6x1)                              *)
(* ---------------------------------------------------------------------------------------------------- *)
vecX_pred[1] := (matA[1,1] * vecX_hat[1]) + (matA[1,2] * vecX_hat[2]) + (matA[1,3] * vecX_hat[3]) +
                (matA[1,4] * vecX_hat[4]) + (matA[1,5] * vecX_hat[5]) + (matA[1,6] * vecX_hat[6]) +
                (matB[1,1] * vecU[1])     + (matB[1,2] * vecU[2])     + (matB[1,3] * vecU[3])     +
                (matB[1,4] * vecU[4])     + (matB[1,5] * vecU[5])     + vecObsUpdate[1];

vecX_pred[2] := (matA[2,1] * vecX_hat[1]) + (matA[2,2] * vecX_hat[2]) + (matA[2,3] * vecX_hat[3]) +
                (matA[2,4] * vecX_hat[4]) + (matA[2,5] * vecX_hat[5]) + (matA[2,6] * vecX_hat[6]) +
                (matB[2,1] * vecU[1])     + (matB[2,2] * vecU[2])     + (matB[2,3] * vecU[3])     +
                (matB[2,4] * vecU[4])     + (matB[2,5] * vecU[5])     + vecObsUpdate[2];

vecX_pred[3] := (matA[3,1] * vecX_hat[1]) + (matA[3,2] * vecX_hat[2]) + (matA[3,3] * vecX_hat[3]) +
                (matA[3,4] * vecX_hat[4]) + (matA[3,5] * vecX_hat[5]) + (matA[3,6] * vecX_hat[6]) +
                (matB[3,1] * vecU[1])     + (matB[3,2] * vecU[2])     + (matB[3,3] * vecU[3])     +
                (matB[3,4] * vecU[4])     + (matB[3,5] * vecU[5])     + vecObsUpdate[3];

vecX_pred[4] := (matA[4,1] * vecX_hat[1]) + (matA[4,2] * vecX_hat[2]) + (matA[4,3] * vecX_hat[3]) +
                (matA[4,4] * vecX_hat[4]) + (matA[4,5] * vecX_hat[5]) + (matA[4,6] * vecX_hat[6]) +
                (matB[4,1] * vecU[1])     + (matB[4,2] * vecU[2])     + (matB[4,3] * vecU[3])     +
                (matB[4,4] * vecU[4])     + (matB[4,5] * vecU[5])     + vecObsUpdate[4];

vecX_pred[5] := (matA[5,1] * vecX_hat[1]) + (matA[5,2] * vecX_hat[2]) + (matA[5,3] * vecX_hat[3]) +
                (matA[5,4] * vecX_hat[4]) + (matA[5,5] * vecX_hat[5]) + (matA[5,6] * vecX_hat[6]) +
                (matB[5,1] * vecU[1])     + (matB[5,2] * vecU[2])     + (matB[5,3] * vecU[3])     +
                (matB[5,4] * vecU[4])     + (matB[5,5] * vecU[5])     + vecObsUpdate[5];

vecX_pred[6] := (matA[6,1] * vecX_hat[1]) + (matA[6,2] * vecX_hat[2]) + (matA[6,3] * vecX_hat[3]) +
                (matA[6,4] * vecX_hat[4]) + (matA[6,5] * vecX_hat[5]) + (matA[6,6] * vecX_hat[6]) +
                (matB[6,1] * vecU[1])     + (matB[6,2] * vecU[2])     + (matB[6,3] * vecU[3])     +
                (matB[6,4] * vecU[4])     + (matB[6,5] * vecU[5])     + vecObsUpdate[6];

(* Physical Boundary Clamping on State Estimates *)
vecX_hat[1] := MAX(-70.0, MIN(130.0, vecX_pred[1]));
vecX_hat[2] := MAX(-65.0, MIN(125.0, vecX_pred[2]));
vecX_hat[3] := MAX(-65.0, MIN(120.0, vecX_pred[3]));
vecX_hat[4] := MAX(0.001, MIN(1200.0, vecX_pred[4]));
vecX_hat[5] := MAX(-95.0, MIN(60.0, vecX_pred[5]));
vecX_hat[6] := MAX(0.0, MIN(rCakeThicknessMax_mm, vecX_pred[6]));
"""
