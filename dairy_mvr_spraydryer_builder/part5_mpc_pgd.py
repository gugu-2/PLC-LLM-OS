# dairy_mvr_spraydryer_builder/part5_mpc_pgd.py
# Lumina Cyber-Physical Systems Chair - V7 Max-Persona
# Part 5: Phase 3 - Receding-Horizon Model Predictive Control (MPC) with Projected Gradient Descent (PGD) & Slew Limiters

def get_part5_mpc_pgd():
    return """(* === PHASE 3: RECEDING-HORIZON MPC OPTIMIZATION WITH PGD & SLEW LIMITS === *)

(* ------------------------------------------------------------------------------------------------- *)
(* INITIALIZE CONTROL TRAJECTORY OVER HORIZON N = 5 FROM ACTIVE/PREVIOUS INPUT COMMANDS             *)
(* ------------------------------------------------------------------------------------------------- *)
FOR k := 0 TO 4 DO
    FOR m := 1 TO 6 DO
        mat_uHoriz[k, m] := vec_uCmd[m];
    END_FOR;
END_FOR;

(* ------------------------------------------------------------------------------------------------- *)
(* UNROLLED PROJECTED GRADIENT DESCENT (PGD) OPTIMIZATION: 6 ITERATIONS                              *)
(* Solves multi-variable constrained quadratic optimal control problem in real time:                 *)
(* min J = 0.5 * SUM_{k=0..4} [(x_k - x_ref)^T Q (x_k - x_ref) + u_k^T R u_k]                       *)
(*       + 0.5 * (x_5 - x_ref)^T P (x_5 - x_ref)                                                     *)
(* subject to x_{k+1} = A x_k + B u_k, uMin <= u_k <= uMax                                           *)
(* ------------------------------------------------------------------------------------------------- *)
FOR nIter := 1 TO 6 DO
    (* --------------------------------------------------------------------------------------------- *)
    (* SUB-STEP A: FORWARD SYSTEM TRAJECTORY SIMULATION OVER HORIZON (k = 0..4)                      *)
    (* --------------------------------------------------------------------------------------------- *)
    FOR i := 1 TO 8 DO
        mat_xHoriz[0, i] := vec_xEst[i];
    END_FOR;

    FOR k := 0 TO 4 DO
        FOR i := 1 TO 8 DO
            rSum := 0.0;
            (* State drift contribution: A * x[k] *)
            FOR j := 1 TO 8 DO
                rSum := rSum + (matA[i, j] * mat_xHoriz[k, j]);
            END_FOR;
            (* Control actuation contribution: B * u[k] *)
            FOR m := 1 TO 6 DO
                rSum := rSum + (matB[i, m] * mat_uHoriz[k, m]);
            END_FOR;
            mat_xHoriz[k + 1, i] := rSum;
        END_FOR;
    END_FOR;

    (* --------------------------------------------------------------------------------------------- *)
    (* SUB-STEP B: BACKWARD ADJOINT COSTATE DYNAMICS (PONTRYAGIN MINIMUM PRINCIPLE)                  *)
    (* Terminal condition: lambda[5] = P * (x[5] - xRef)                                             *)
    (* Recursive step: lambda[k] = Q * (x[k] - xRef) + A^T * lambda[k+1]                             *)
    (* --------------------------------------------------------------------------------------------- *)
    FOR i := 1 TO 8 DO
        mat_lambda[5, i] := vec_diagP[i] * (mat_xHoriz[5, i] - vec_xRef[i]);
    END_FOR;

    FOR k := 4 DOWNTO 0 DO
        FOR i := 1 TO 8 DO
            rSum := vec_diagQ[i] * (mat_xHoriz[k, i] - vec_xRef[i]);
            (* Adjoint back-propagation via A transposed *)
            FOR j := 1 TO 8 DO
                rSum := rSum + (matA[j, i] * mat_lambda[k + 1, j]);
            END_FOR;
            mat_lambda[k, i] := rSum;
        END_FOR;
    END_FOR;

    (* --------------------------------------------------------------------------------------------- *)
    (* SUB-STEP C: GRADIENT EVALUATION, DESCENT UPDATE & ACTUATOR BOX PROJECTION                     *)
    (* grad_u[k] = R * u[k] + B^T * lambda[k+1]                                                      *)
    (* u[k] := Project_{[uMin, uMax]} ( u[k] - alpha * grad_u[k] )                                   *)
    (* --------------------------------------------------------------------------------------------- *)
    FOR k := 0 TO 4 DO
        FOR m := 1 TO 6 DO
            (* Compute analytical cost gradient with respect to actuator input m *)
            rSum := vec_diagR[m] * mat_uHoriz[k, m];
            FOR j := 1 TO 8 DO
                rSum := rSum + (matB[j, m] * mat_lambda[k + 1, j]);
            END_FOR;
            mat_gradU[k, m] := rSum;

            (* Gradient descent step *)
            mat_uHoriz[k, m] := mat_uHoriz[k, m] - (rPgdStepSize * mat_gradU[k, m]);

            (* Euclidean projection onto physical actuator box constraints *)
            IF mat_uHoriz[k, m] < vec_uMin[m] THEN
                mat_uHoriz[k, m] := vec_uMin[m];
            ELSIF mat_uHoriz[k, m] > vec_uMax[m] THEN
                mat_uHoriz[k, m] := vec_uMax[m];
            END_IF;
        END_FOR;
    END_FOR;
END_FOR;

(* ------------------------------------------------------------------------------------------------- *)
(* SUB-STEP D: FIRST-STEP RECEDING HORIZON SELECTION & DYNAMIC SLEW RATE LIMITATION                  *)
(* Restricts maximum rate of change of actuators between successive 20 ms execution frames          *)
(* ------------------------------------------------------------------------------------------------- *)
FOR m := 1 TO 6 DO
    rDelta := mat_uHoriz[0, m] - vec_uPrev[m];
    IF rDelta > vec_duMax[m] THEN
        vec_uCmd[m] := vec_uPrev[m] + vec_duMax[m];
    ELSIF rDelta < -vec_duMax[m] THEN
        vec_uCmd[m] := vec_uPrev[m] - vec_duMax[m];
    ELSE
        vec_uCmd[m] := mat_uHoriz[0, m];
    END_IF;

    (* Final Safety Bounds Check on Slew-Limited Command *)
    IF vec_uCmd[m] < vec_uMin[m] THEN
        vec_uCmd[m] := vec_uMin[m];
    ELSIF vec_uCmd[m] > vec_uMax[m] THEN
        vec_uCmd[m] := vec_uMax[m];
    END_IF;

    (* Update history register for subsequent control cycle *)
    vec_uPrev[m] := vec_uCmd[m];
END_FOR;

(* ------------------------------------------------------------------------------------------------- *)
(* DEFAULT ASSIGNMENT OF OPTIMIZED ACTUATOR COMMANDS TO PHYSICAL OUTPUTS                             *)
(* ------------------------------------------------------------------------------------------------- *)
rCV_FeedRateValve_pct       := vec_uCmd[1];
rSPD_MvrCompressor_rpm      := vec_uCmd[2];
rCV_SteamInjectionValve_pct := vec_uCmd[3];
rCV_AtomizerNozzlePress_bar := vec_uCmd[4];
rCV_BurnerGasModulation_pct := vec_uCmd[5];
rCV_ExhaustDamper_pct       := vec_uCmd[6];
"""
