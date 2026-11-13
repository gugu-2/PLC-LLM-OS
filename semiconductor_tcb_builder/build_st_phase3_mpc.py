# semiconductor_tcb_builder/build_st_phase3_mpc.py

def get_phase3_mpc():
    return """(*
====================================================================================================
PHASE 3: RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) WITH UNROLLED PGD (10 ITERATIONS)
Quadratic Cost Objective Function:
  J = sum_{k=0}^{9} [ (x[k] - x_ref)^T * Q * (x[k] - x_ref) + u[k]^T * R * u[k] + Delta_u[k]^T * S * Delta_u[k] ]
    + (x[10] - x_ref)^T * P * (x[10] - x_ref)

Actuator Constraints & Hard Box Projections:
  - Piezo Fine Positioner Trim     : -10.0 um <= u[1] <= +10.0 um,  |Delta_u[1]| <= 1.2 um/scan
  - Voice Coil Motor Drive Current : -15.0 A  <= u[2] <= +15.0 A,   |Delta_u[2]| <= 2.5 A/scan
  - Pulse Ceramic Heater Duty      :   0.0 %  <= u[3] <= 100.0 %,   |Delta_u[3]| <= 18.0 %/scan
  - Chilled Nitrogen Quench Valve  :   0.0 %  <= u[4] <= 100.0 %,   |Delta_u[4]| <= 22.0 %/scan
  - Formic Acid Purge Flow Valve   :   0.0 %  <= u[5] <= 100.0 %,   |Delta_u[5]| <= 8.0 %/scan

Iterative Architecture:
  10 Unrolled Projected Gradient Descent (PGD) optimization iterations executed deterministically
  within the fixed cyclic task time (Ts = 1.0 ms) guaranteeing bounded WCET without online solver stall.
====================================================================================================
*)

(* Initialize State Horizon Initial Condition from Kalman Corrected Estimate *)
FOR iStateIdx := 1 TO 6 DO
    arrX_Horiz[0, iStateIdx] := vecX_Hat[iStateIdx];
END_FOR;

(* Warm-Start Control Trajectory: Shift Previous Horizon by One Step *)
FOR iHorizStep := 0 TO 8 DO
    FOR iInputIdx := 1 TO 5 DO
        arrU_Horiz[iHorizStep, iInputIdx] := arrU_Horiz[iHorizStep + 1, iInputIdx];
    END_FOR;
END_FOR;
(* Duplicate last step into tail *)
FOR iInputIdx := 1 TO 5 DO
    arrU_Horiz[9, iInputIdx] := arrU_Horiz[8, iInputIdx];
END_FOR;

(* ============================================================================================== *)
(* UNROLLED PROJECTED GRADIENT DESCENT (PGD) OPTIMIZATION LOOP - 10 ITERATIONS                    *)
(* ============================================================================================== *)
FOR iPgdIteration := 1 TO 10 DO

    (* ------------------------------------------------------------------------------------------ *)
    (* STEP 1: FORWARD TRAJECTORY SIMULATION OVER PREDICTION HORIZON (k = 0..9)                   *)
    (* x[k+1] = A * x[k] + B * u[k]                                                               *)
    (* ------------------------------------------------------------------------------------------ *)
    FOR iHorizStep := 0 TO 9 DO
        FOR iStateIdx := 1 TO 6 DO
            arrX_Horiz[iHorizStep + 1, iStateIdx] :=
                  (matA[iStateIdx, 1] * arrX_Horiz[iHorizStep, 1])
                + (matA[iStateIdx, 2] * arrX_Horiz[iHorizStep, 2])
                + (matA[iStateIdx, 3] * arrX_Horiz[iHorizStep, 3])
                + (matA[iStateIdx, 4] * arrX_Horiz[iHorizStep, 4])
                + (matA[iStateIdx, 5] * arrX_Horiz[iHorizStep, 5])
                + (matA[iStateIdx, 6] * arrX_Horiz[iHorizStep, 6])
                + (matB[iStateIdx, 1] * arrU_Horiz[iHorizStep, 1])
                + (matB[iStateIdx, 2] * arrU_Horiz[iHorizStep, 2])
                + (matB[iStateIdx, 3] * arrU_Horiz[iHorizStep, 3])
                + (matB[iStateIdx, 4] * arrU_Horiz[iHorizStep, 4])
                + (matB[iStateIdx, 5] * arrU_Horiz[iHorizStep, 5]);
        END_FOR;
    END_FOR;

    (* ------------------------------------------------------------------------------------------ *)
    (* STEP 2: BACKWARD ADJOINT CO-STATE RECURSION (Pontryagin Maximum Principle)                *)
    (* Terminal condition: lambda[10] = P * (x[10] - x_ref)                                       *)
    (* Backward recursion: lambda[k] = A^T * lambda[k+1] + Q * (x[k] - x_ref)                    *)
    (* ------------------------------------------------------------------------------------------ *)
    FOR iStateIdx := 1 TO 6 DO
        arrLambda[10, iStateIdx] := matP_Diag[iStateIdx] * (arrX_Horiz[10, iStateIdx] - vecX_Ref[iStateIdx]);
    END_FOR;

    FOR iHorizStep := 9 TO 0 BY -1 DO
        FOR iStateIdx := 1 TO 6 DO
            arrLambda[iHorizStep, iStateIdx] :=
                  (matA[1, iStateIdx] * arrLambda[iHorizStep + 1, 1])
                + (matA[2, iStateIdx] * arrLambda[iHorizStep + 1, 2])
                + (matA[3, iStateIdx] * arrLambda[iHorizStep + 1, 3])
                + (matA[4, iStateIdx] * arrLambda[iHorizStep + 1, 4])
                + (matA[5, iStateIdx] * arrLambda[iHorizStep + 1, 5])
                + (matA[6, iStateIdx] * arrLambda[iHorizStep + 1, 6])
                + (matQ_Diag[iStateIdx] * (arrX_Horiz[iHorizStep, iStateIdx] - vecX_Ref[iStateIdx]));
        END_FOR;
    END_FOR;

    (* ------------------------------------------------------------------------------------------ *)
    (* STEP 3: ANALYTICAL COST GRADIENT EVALUATION & DESCENT STEP                                 *)
    (* grad_u[k] = B^T * lambda[k+1] + R * u[k] + S * (u[k] - u[k-1])                             *)
    (* u_new[k]  = u[k] - gamma * grad_u[k]                                                       *)
    (* ------------------------------------------------------------------------------------------ *)
    FOR iHorizStep := 0 TO 9 DO
        FOR iInputIdx := 1 TO 5 DO
            (* Compute rate of change penalty gradient component *)
            IF iHorizStep = 0 THEN
                arrGradU[iHorizStep, iInputIdx] :=
                      (matB[1, iInputIdx] * arrLambda[iHorizStep + 1, 1])
                    + (matB[2, iInputIdx] * arrLambda[iHorizStep + 1, 2])
                    + (matB[3, iInputIdx] * arrLambda[iHorizStep + 1, 3])
                    + (matB[4, iInputIdx] * arrLambda[iHorizStep + 1, 4])
                    + (matB[5, iInputIdx] * arrLambda[iHorizStep + 1, 5])
                    + (matB[6, iInputIdx] * arrLambda[iHorizStep + 1, 6])
                    + (matR_Diag[iInputIdx] * arrU_Horiz[iHorizStep, iInputIdx])
                    + (matS_Diag[iInputIdx] * (arrU_Horiz[iHorizStep, iInputIdx] - vecU_Prev[iInputIdx]));
            ELSE
                arrGradU[iHorizStep, iInputIdx] :=
                      (matB[1, iInputIdx] * arrLambda[iHorizStep + 1, 1])
                    + (matB[2, iInputIdx] * arrLambda[iHorizStep + 1, 2])
                    + (matB[3, iInputIdx] * arrLambda[iHorizStep + 1, 3])
                    + (matB[4, iInputIdx] * arrLambda[iHorizStep + 1, 4])
                    + (matB[5, iInputIdx] * arrLambda[iHorizStep + 1, 5])
                    + (matB[6, iInputIdx] * arrLambda[iHorizStep + 1, 6])
                    + (matR_Diag[iInputIdx] * arrU_Horiz[iHorizStep, iInputIdx])
                    + (matS_Diag[iInputIdx] * (arrU_Horiz[iHorizStep, iInputIdx] - arrU_Horiz[iHorizStep - 1, iInputIdx]));
            END_IF;

            (* Gradient Descent Update *)
            arrU_Horiz[iHorizStep, iInputIdx] := arrU_Horiz[iHorizStep, iInputIdx] - (rPgdStepSize * arrGradU[iHorizStep, iInputIdx]);

            (* ---------------------------------------------------------------------------------- *)
            (* STEP 4: HARD BOX CONSTRAINTS & SLEW RATE PROJECTION (CLIP TO FEASIBLE SET)          *)
            (* ---------------------------------------------------------------------------------- *)
            (* Saturation bound projection *)
            IF arrU_Horiz[iHorizStep, iInputIdx] > rU_UpperBound[iInputIdx] THEN
                arrU_Horiz[iHorizStep, iInputIdx] := rU_UpperBound[iInputIdx];
            ELSIF arrU_Horiz[iHorizStep, iInputIdx] < rU_LowerBound[iInputIdx] THEN
                arrU_Horiz[iHorizStep, iInputIdx] := rU_LowerBound[iInputIdx];
            END_IF;

            (* Slew rate projection relative to predecessor *)
            IF iHorizStep = 0 THEN
                IF (arrU_Horiz[iHorizStep, iInputIdx] - vecU_Prev[iInputIdx]) > rDeltaU_MaxRate[iInputIdx] THEN
                    arrU_Horiz[iHorizStep, iInputIdx] := vecU_Prev[iInputIdx] + rDeltaU_MaxRate[iInputIdx];
                ELSIF (arrU_Horiz[iHorizStep, iInputIdx] - vecU_Prev[iInputIdx]) < -rDeltaU_MaxRate[iInputIdx] THEN
                    arrU_Horiz[iHorizStep, iInputIdx] := vecU_Prev[iInputIdx] - rDeltaU_MaxRate[iInputIdx];
                END_IF;
            ELSE
                IF (arrU_Horiz[iHorizStep, iInputIdx] - arrU_Horiz[iHorizStep - 1, iInputIdx]) > rDeltaU_MaxRate[iInputIdx] THEN
                    arrU_Horiz[iHorizStep, iInputIdx] := arrU_Horiz[iHorizStep - 1, iInputIdx] + rDeltaU_MaxRate[iInputIdx];
                ELSIF (arrU_Horiz[iHorizStep, iInputIdx] - arrU_Horiz[iHorizStep - 1, iInputIdx]) < -rDeltaU_MaxRate[iInputIdx] THEN
                    arrU_Horiz[iHorizStep, iInputIdx] := arrU_Horiz[iHorizStep - 1, iInputIdx] - rDeltaU_MaxRate[iInputIdx];
                END_IF;
            END_IF;
        END_FOR;
    END_FOR;

END_FOR;

(* ---------------------------------------------------------------------------------------------- *)
(* RECEDING HORIZON ACTUATION INGESTION: EXTRACT STEP 0 OF HORIZON                               *)
(* ---------------------------------------------------------------------------------------------- *)
vecU_Active[1] := arrU_Horiz[0, 1]; (* Piezo Micro-Trim [um] *)
vecU_Active[2] := arrU_Horiz[0, 2]; (* Voice Coil Current [A] *)
vecU_Active[3] := arrU_Horiz[0, 3]; (* Pulse Ceramic Heater PWM [%] *)
vecU_Active[4] := arrU_Horiz[0, 4]; (* Chilled N2 Quench Valve [%] *)
vecU_Active[5] := arrU_Horiz[0, 5]; (* Formic Purge Flow Valve [%] *)

(* Compute and store active slews for next cycle execution *)
FOR iInputIdx := 1 TO 5 DO
    vecDeltaU[iInputIdx] := vecU_Active[iInputIdx] - vecU_Prev[iInputIdx];
    vecU_Prev[iInputIdx] := vecU_Active[iInputIdx];
END_FOR;

(* Export Actuator Commands to Block Outputs *)
rPiezoZ_Trim_Cmd_um         := vecU_Active[1];
rVoiceCoilCurrent_Cmd_A     := vecU_Active[2];
rCeramicHeaterDuty_Cmd_Pct  := vecU_Active[3];
rN2QuenchValve_Cmd_Pct      := vecU_Active[4];
rFormicPurgeValve_Cmd_Pct   := vecU_Active[5];
"""
