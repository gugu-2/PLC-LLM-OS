# -*- coding: utf-8 -*-
"""
Module: aluminum_potline_builder/mod_mpc.py
Implements Phase 3: Receding-Horizon Model Predictive Control (MPC) Optimization
with 10 Unrolled Projected Gradient Descent (PGD) Iterations,
Explicit Adjoint Costate Backpropagation, and Actuator Slew Rate/Dynamic Safety Constraints.
"""

def generate_mpc():
    return '''(* =====================================================================================================================
 * PHASE 3: RECEDING-HORIZON MPC OPTIMIZATION WITH 10 PROJECTED GRADIENT DESCENT (PGD) ITERATIONS
 * Horizon: N = 5 steps (Dt = 0.100 s), 6 States, 5 Actuator Inputs.
 * Explicitly computes:
 *   1. Forward state trajectory rollout (x[k+1] = A*x[k] + B*u[k])
 *   2. Backward adjoint costate propagation (lambda[k] = Q*(x[k] - x_ref) + A^T * lambda[k+1])
 *   3. Actuator gradient computation (grad_u[k] = R*u[k] + B^T * lambda[k+1] + S*(u[k] - u_prev))
 *   4. Gradient descent update with box projection and dynamic thermal/ACD safety constraints
 * ===================================================================================================================== *)

(* Initialize Step 0 of state prediction horizon from current Luenberger observer estimates *)
FOR i := 1 TO 6 DO
    arrX_Trajectory[0, i] := arrX_hat[i];
END_FOR;

(* Warm-start actuator trajectory from previous solution *)
FOR nStep := 0 TO 3 DO
    FOR j := 1 TO 5 DO
        arrU_Trajectory[nStep, j] := arrU_Trajectory[nStep + 1, j];
    END_FOR;
END_FOR;
FOR j := 1 TO 5 DO
    arrU_Trajectory[4, j] := arrU_Trajectory[3, j];
END_FOR;

(* ---------------------------------------------------------------------------------------------------------------------
 * 10 UNROLLED PROJECTED GRADIENT DESCENT (PGD) ITERATION ENGINE
 * --------------------------------------------------------------------------------------------------------------------- *)
FOR nIter := 1 TO 10 DO

    (* ==================== 1. FORWARD STATE TRAJECTORY ROLLOUT (Steps 0..4 -> 1..5) ==================== *)
    FOR nStep := 0 TO 4 DO
        (* State 1: dR_pot *)
        arrX_Trajectory[nStep + 1, 1] :=
            (arrA[1, 1] * arrX_Trajectory[nStep, 1]) + (arrA[1, 2] * arrX_Trajectory[nStep, 2]) +
            (arrA[1, 3] * arrX_Trajectory[nStep, 3]) + (arrA[1, 4] * arrX_Trajectory[nStep, 4]) +
            (arrA[1, 5] * arrX_Trajectory[nStep, 5]) + (arrA[1, 6] * arrX_Trajectory[nStep, 6]) +
            (arrB[1, 1] * arrU_Trajectory[nStep, 1]) + (arrB[1, 2] * arrU_Trajectory[nStep, 2]) +
            (arrB[1, 3] * arrU_Trajectory[nStep, 3]) + (arrB[1, 4] * arrU_Trajectory[nStep, 4]) +
            (arrB[1, 5] * arrU_Trajectory[nStep, 5]);

        (* State 2: C_Al2O3 *)
        arrX_Trajectory[nStep + 1, 2] :=
            (arrA[2, 1] * arrX_Trajectory[nStep, 1]) + (arrA[2, 2] * arrX_Trajectory[nStep, 2]) +
            (arrA[2, 3] * arrX_Trajectory[nStep, 3]) + (arrA[2, 4] * arrX_Trajectory[nStep, 4]) +
            (arrA[2, 5] * arrX_Trajectory[nStep, 5]) + (arrA[2, 6] * arrX_Trajectory[nStep, 6]) +
            (arrB[2, 1] * arrU_Trajectory[nStep, 1]) + (arrB[2, 2] * arrU_Trajectory[nStep, 2]) +
            (arrB[2, 3] * arrU_Trajectory[nStep, 3]) + (arrB[2, 4] * arrU_Trajectory[nStep, 4]) +
            (arrB[2, 5] * arrU_Trajectory[nStep, 5]);

        (* State 3: T_bath *)
        arrX_Trajectory[nStep + 1, 3] :=
            (arrA[3, 1] * arrX_Trajectory[nStep, 1]) + (arrA[3, 2] * arrX_Trajectory[nStep, 2]) +
            (arrA[3, 3] * arrX_Trajectory[nStep, 3]) + (arrA[3, 4] * arrX_Trajectory[nStep, 4]) +
            (arrA[3, 5] * arrX_Trajectory[nStep, 5]) + (arrA[3, 6] * arrX_Trajectory[nStep, 6]) +
            (arrB[3, 1] * arrU_Trajectory[nStep, 1]) + (arrB[3, 2] * arrU_Trajectory[nStep, 2]) +
            (arrB[3, 3] * arrU_Trajectory[nStep, 3]) + (arrB[3, 4] * arrU_Trajectory[nStep, 4]) +
            (arrB[3, 5] * arrU_Trajectory[nStep, 5]);

        (* State 4: dACD *)
        arrX_Trajectory[nStep + 1, 4] :=
            (arrA[4, 1] * arrX_Trajectory[nStep, 1]) + (arrA[4, 2] * arrX_Trajectory[nStep, 2]) +
            (arrA[4, 3] * arrX_Trajectory[nStep, 3]) + (arrA[4, 4] * arrX_Trajectory[nStep, 4]) +
            (arrA[4, 5] * arrX_Trajectory[nStep, 5]) + (arrA[4, 6] * arrX_Trajectory[nStep, 6]) +
            (arrB[4, 1] * arrU_Trajectory[nStep, 1]) + (arrB[4, 2] * arrU_Trajectory[nStep, 2]) +
            (arrB[4, 3] * arrU_Trajectory[nStep, 3]) + (arrB[4, 4] * arrU_Trajectory[nStep, 4]) +
            (arrB[4, 5] * arrU_Trajectory[nStep, 5]);

        (* State 5: BubbleCov *)
        arrX_Trajectory[nStep + 1, 5] :=
            (arrA[5, 1] * arrX_Trajectory[nStep, 1]) + (arrA[5, 2] * arrX_Trajectory[nStep, 2]) +
            (arrA[5, 3] * arrX_Trajectory[nStep, 3]) + (arrA[5, 4] * arrX_Trajectory[nStep, 4]) +
            (arrA[5, 5] * arrX_Trajectory[nStep, 5]) + (arrA[5, 6] * arrX_Trajectory[nStep, 6]) +
            (arrB[5, 1] * arrU_Trajectory[nStep, 1]) + (arrB[5, 2] * arrU_Trajectory[nStep, 2]) +
            (arrB[5, 3] * arrU_Trajectory[nStep, 3]) + (arrB[5, 4] * arrU_Trajectory[nStep, 4]) +
            (arrB[5, 5] * arrU_Trajectory[nStep, 5]);

        (* State 6: MetalPad *)
        arrX_Trajectory[nStep + 1, 6] :=
            (arrA[6, 1] * arrX_Trajectory[nStep, 1]) + (arrA[6, 2] * arrX_Trajectory[nStep, 2]) +
            (arrA[6, 3] * arrX_Trajectory[nStep, 3]) + (arrA[6, 4] * arrX_Trajectory[nStep, 4]) +
            (arrA[6, 5] * arrX_Trajectory[nStep, 5]) + (arrA[6, 6] * arrX_Trajectory[nStep, 6]) +
            (arrB[6, 1] * arrU_Trajectory[nStep, 1]) + (arrB[6, 2] * arrU_Trajectory[nStep, 2]) +
            (arrB[6, 3] * arrU_Trajectory[nStep, 3]) + (arrB[6, 4] * arrU_Trajectory[nStep, 4]) +
            (arrB[6, 5] * arrU_Trajectory[nStep, 5]);
    END_FOR;

    (* ==================== 2. BACKWARD ADJOINT COSTATE PROPAGATION ==================== *)
    (* Step 5 Terminal Costate: lambda[5] = P * (x[5] - x_ref) *)
    arrLambda[5, 1] := arrP[1, 1] * (arrX_Trajectory[5, 1] - 0.0) +
                       arrP[1, 2] * (arrX_Trajectory[5, 2] - rSet_TargetAlumina_pct) +
                       arrP[1, 4] * (arrX_Trajectory[5, 4] - rSet_TargetACD_mm);

    arrLambda[5, 2] := arrP[2, 1] * (arrX_Trajectory[5, 1] - 0.0) +
                       arrP[2, 2] * (arrX_Trajectory[5, 2] - rSet_TargetAlumina_pct);

    arrLambda[5, 3] := arrP[3, 3] * (arrX_Trajectory[5, 3] - rSet_TargetBathTemp_degC);

    arrLambda[5, 4] := arrP[4, 1] * (arrX_Trajectory[5, 1] - 0.0) +
                       arrP[4, 4] * (arrX_Trajectory[5, 4] - rSet_TargetACD_mm);

    arrLambda[5, 5] := arrP[5, 5] * (arrX_Trajectory[5, 5] - 20.0);

    arrLambda[5, 6] := arrP[6, 6] * (arrX_Trajectory[5, 6] - 20.0);

    (* Adjoint Backward Rollout for Steps 4 down to 0: lambda[k] = Q*(x[k] - x_ref) + A^T * lambda[k+1] *)
    FOR nStep := 4 TO 0 BY -1 DO
        (* Costate 1 *)
        arrLambda[nStep, 1] :=
            (arrQ[1, 1] * (arrX_Trajectory[nStep, 1] - 0.0)) +
            (arrQ[1, 2] * (arrX_Trajectory[nStep, 2] - rSet_TargetAlumina_pct)) +
            (arrQ[1, 4] * (arrX_Trajectory[nStep, 4] - rSet_TargetACD_mm)) +
            (arrA[1, 1] * arrLambda[nStep + 1, 1]) + (arrA[2, 1] * arrLambda[nStep + 1, 2]) +
            (arrA[3, 1] * arrLambda[nStep + 1, 3]) + (arrA[4, 1] * arrLambda[nStep + 1, 4]) +
            (arrA[5, 1] * arrLambda[nStep + 1, 5]) + (arrA[6, 1] * arrLambda[nStep + 1, 6]);

        (* Costate 2 *)
        arrLambda[nStep, 2] :=
            (arrQ[2, 1] * (arrX_Trajectory[nStep, 1] - 0.0)) +
            (arrQ[2, 2] * (arrX_Trajectory[nStep, 2] - rSet_TargetAlumina_pct)) +
            (arrA[1, 2] * arrLambda[nStep + 1, 1]) + (arrA[2, 2] * arrLambda[nStep + 1, 2]) +
            (arrA[3, 2] * arrLambda[nStep + 1, 3]) + (arrA[4, 2] * arrLambda[nStep + 1, 4]) +
            (arrA[5, 2] * arrLambda[nStep + 1, 5]) + (arrA[6, 2] * arrLambda[nStep + 1, 6]);

        (* Costate 3 *)
        arrLambda[nStep, 3] :=
            (arrQ[3, 3] * (arrX_Trajectory[nStep, 3] - rSet_TargetBathTemp_degC)) +
            (arrA[1, 3] * arrLambda[nStep + 1, 1]) + (arrA[2, 3] * arrLambda[nStep + 1, 2]) +
            (arrA[3, 3] * arrLambda[nStep + 1, 3]) + (arrA[4, 3] * arrLambda[nStep + 1, 4]) +
            (arrA[5, 3] * arrLambda[nStep + 1, 5]) + (arrA[6, 3] * arrLambda[nStep + 1, 6]);

        (* Costate 4 *)
        arrLambda[nStep, 4] :=
            (arrQ[4, 1] * (arrX_Trajectory[nStep, 1] - 0.0)) +
            (arrQ[4, 4] * (arrX_Trajectory[nStep, 4] - rSet_TargetACD_mm)) +
            (arrA[1, 4] * arrLambda[nStep + 1, 1]) + (arrA[2, 4] * arrLambda[nStep + 1, 2]) +
            (arrA[3, 4] * arrLambda[nStep + 1, 3]) + (arrA[4, 4] * arrLambda[nStep + 1, 4]) +
            (arrA[5, 4] * arrLambda[nStep + 1, 5]) + (arrA[6, 4] * arrLambda[nStep + 1, 6]);

        (* Costate 5 *)
        arrLambda[nStep, 5] :=
            (arrQ[5, 5] * (arrX_Trajectory[nStep, 5] - 20.0)) +
            (arrA[1, 5] * arrLambda[nStep + 1, 1]) + (arrA[2, 5] * arrLambda[nStep + 1, 2]) +
            (arrA[3, 5] * arrLambda[nStep + 1, 3]) + (arrA[4, 5] * arrLambda[nStep + 1, 4]) +
            (arrA[5, 5] * arrLambda[nStep + 1, 5]) + (arrA[6, 5] * arrLambda[nStep + 1, 6]);

        (* Costate 6 *)
        arrLambda[nStep, 6] :=
            (arrQ[6, 6] * (arrX_Trajectory[nStep, 6] - 20.0)) +
            (arrA[1, 6] * arrLambda[nStep + 1, 1]) + (arrA[2, 6] * arrLambda[nStep + 1, 2]) +
            (arrA[3, 6] * arrLambda[nStep + 1, 3]) + (arrA[4, 6] * arrLambda[nStep + 1, 4]) +
            (arrA[5, 6] * arrLambda[nStep + 1, 5]) + (arrA[6, 6] * arrLambda[nStep + 1, 6]);
    END_FOR;

    (* ==================== 3. GRADIENT EVALUATION & PROJECTED INPUT UPDATE ==================== *)
    FOR nStep := 0 TO 4 DO
        FOR j := 1 TO 5 DO
            (* Slew reference selection *)
            IF nStep = 0 THEN
                rScratch1 := arrU_Previous[j];
            ELSE
                rScratch1 := arrU_Trajectory[nStep - 1, j];
            END_IF;

            (* Gradient: grad_u = R*u + B^T * lambda[k+1] + S*(u - u_prev) *)
            arrGrad_U[nStep, j] := (arrR[j, j] * arrU_Trajectory[nStep, j]) +
                                   (arrS[j, j] * (arrU_Trajectory[nStep, j] - rScratch1)) +
                                   (arrB[1, j] * arrLambda[nStep + 1, 1]) +
                                   (arrB[2, j] * arrLambda[nStep + 1, 2]) +
                                   (arrB[3, j] * arrLambda[nStep + 1, 3]) +
                                   (arrB[4, j] * arrLambda[nStep + 1, 4]) +
                                   (arrB[5, j] * arrLambda[nStep + 1, 5]) +
                                   (arrB[6, j] * arrLambda[nStep + 1, 6]);

            (* Gradient descent step *)
            arrU_Trajectory[nStep, j] := arrU_Trajectory[nStep, j] - (rPGD_StepSize * arrGrad_U[nStep, j]);

            (* Slew Rate Clamping *)
            rScratch2 := rScratch1 - (arrDeltaU_Max[j] * rLocalDeltaT_s);
            rScratch3 := rScratch1 + (arrDeltaU_Max[j] * rLocalDeltaT_s);
            IF arrU_Trajectory[nStep, j] < rScratch2 THEN
                arrU_Trajectory[nStep, j] := rScratch2;
            ELSIF arrU_Trajectory[nStep, j] > rScratch3 THEN
                arrU_Trajectory[nStep, j] := rScratch3;
            END_IF;

            (* Box Hardware Bounds Clamping *)
            IF arrU_Trajectory[nStep, j] < arrU_Min[j] THEN
                arrU_Trajectory[nStep, j] := arrU_Min[j];
            ELSIF arrU_Trajectory[nStep, j] > arrU_Max[j] THEN
                arrU_Trajectory[nStep, j] := arrU_Max[j];
            END_IF;
        END_FOR;
    END_FOR;

END_FOR; (* End of 10 PGD iterations *)

(* ---------------------------------------------------------------------------------------------------------------------
 * DYNAMIC CYBER-PHYSICAL SAFETY INTERLOCKS ON OPTIMIZER OUTPUTS
 * --------------------------------------------------------------------------------------------------------------------- *)
(* Thermal Under-Temperature Inhibit: If bath superheat < 6.0 deg C, lock out beam lowering *)
IF rPot_EstSuperheat_degC < 6.00 THEN
    IF arrU_Trajectory[0, 1] < 0.0 THEN
        arrU_Trajectory[0, 1] := 0.0; (* Inhibit downward hoist command to avoid quenching Joule heat *)
    END_IF;
END_IF;

(* ACD Collapse Protection: If real estimated ACD <= 32.0 mm, strictly prohibit any downward move *)
IF rPot_EstAnodeCathodeDist_mm <= 32.00 THEN
    IF arrU_Trajectory[0, 1] < 0.0 THEN
        arrU_Trajectory[0, 1] := 0.0; (* Prevent cathode short circuit *)
    END_IF;
END_IF;

(* Anode Carbon Dusting & Top Crust Freeze Inhibit: Cap upward hoist travel if cell voltage is high *)
IF rPot_VotedCellVoltage_V > 4.55 THEN
    IF arrU_Trajectory[0, 1] > 1.20 THEN
        arrU_Trajectory[0, 1] := 1.20; (* Restrict excessive ACD expansion *)
    END_IF;
END_IF;

(* Extract First Control Action for Physical Deployment *)
FOR j := 1 TO 5 DO
    arrU_Applied[j] := arrU_Trajectory[0, j];
    arrU_Previous[j] := arrU_Applied[j];
END_FOR;
'''
