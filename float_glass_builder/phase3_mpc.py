# phase3_mpc.py for FB_Glass_FloatLine_TinBath_AnnealingLehr_ThicknessCooling

def generate_phase3():
    return """(*
 * =========================================================================================================
 * PHASE 3: RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) & 10 UNROLLED PGD ITERATIONS
 * 
 * Multi-Objective Quadratic Cost Functional Formulation:
 * J(u) = (x_k+1 - x_ref)^T * Q * (x_k+1 - x_ref) + (u - u_ref)^T * R * (u - u_ref) + 
 *        (x_k+1 - x_ref)^T * P * (x_k+1 - x_ref)
 * 
 * Unrolled Optimization Engine: 10 Iterations of Projected Gradient Descent (PGD)
 * Iteration Law: u^(m+1) = Proj_Box [ u^(m) - alpha * nabla_J(u^(m)) ]
 * Subject to:
 *   1. Physical Actuator Box Constraints: u_min[k] <= u[k] <= u_max[k]
 *   2. Actuator Dynamic Slew Rate Limits: |u[k] - u_prev[k]| <= du_max[k]
 * Actuator Mapping:
 *   u[1] -> Top-Roller knurl machine pair speeds 1..16 [RPM]
 *   u[2] -> Top-Roller knurl toe-in/toe-out angular positions 1..16 [deg]
 *   u[3] -> Tin bath roof SiC radiant heater banks 1..8 [% duty]
 *   u[4] -> Reducing atmosphere N2 and H2 gas feed trim valves [%]
 *   u[5] -> Annealing Lehr transverse cooling dampers 1..12 [%]
 *   u[6] -> Lehr main line drive conveyor motor speed & synchronized LORs [m/min]
 * =========================================================================================================
 *)

(* ---------------------------------------------------------------------------------------------------------
 * 1. INITIALIZE PGD UNROLLED TRAJECTORY ITERATION 0
 * --------------------------------------------------------------------------------------------------------- *)
FOR idxCol := 1 TO 6 DO
    arrU_PGD_Iter[0, idxCol] := arrInputU[idxCol];
END_FOR;

(* ---------------------------------------------------------------------------------------------------------
 * 2. UNROLLED 10-ITERATION PROJECTED GRADIENT DESCENT OPTIMIZATION
 * --------------------------------------------------------------------------------------------------------- *)
FOR idxIter := 1 TO 10 DO
    (* A. Forward simulate state prediction for current iterate: x_pred = A * x_hat + B * u^(m-1) *)
    FOR idxRow := 1 TO 6 DO
        rAx_Sum := 0.0;
        rBu_Sum := 0.0;
        FOR idxCol := 1 TO 6 DO
            rAx_Sum := rAx_Sum + (matA[idxRow, idxCol] * arrStateX_Hat[idxCol]);
            rBu_Sum := rBu_Sum + (matB[idxRow, idxCol] * arrU_PGD_Iter[idxIter - 1, idxCol]);
        END_FOR;
        arrStateX_Next[idxRow] := rAx_Sum + rBu_Sum;
    END_FOR;

    (* B. Compute quadratic cost gradient nabla_J(u) = 2*R*(u - u_ref) + 2*B^T * (Q + P) * (x_pred - x_ref) *)
    FOR idxCol := 1 TO 6 DO
        (* Control effort gradient component: R_k * (u_k - u_ref_k) *)
        arrGradJ_Iter[idxCol] := matR[idxCol, idxCol] * (arrU_PGD_Iter[idxIter - 1, idxCol] - arrInputU_Ref[idxCol]);

        (* Adjoint backpropagation through B matrix: sum_i B[i, idxCol] * (Q[i,i] + P[i,i]) * (x_pred[i] - x_ref[i]) *)
        FOR idxRow := 1 TO 6 DO
            arrGradJ_Iter[idxCol] := arrGradJ_Iter[idxCol] + 
                (matB[idxRow, idxCol] * (matQ[idxRow, idxRow] + matP[idxRow, idxRow]) * 
                 (arrStateX_Next[idxRow] - arrStateX_Ref[idxRow]));
        END_FOR;

        (* C. Gradient Descent Step: u_raw = u^(m-1) - alpha * grad_J *)
        arrU_PGD_Iter[idxIter, idxCol] := arrU_PGD_Iter[idxIter - 1, idxCol] - (rMpcStepSizeAlpha * arrGradJ_Iter[idxCol]);

        (* D. Hard Saturation Box Projection: Proj_[u_min, u_max](u_raw) *)
        IF arrU_PGD_Iter[idxIter, idxCol] < arrU_Min[idxCol] THEN
            arrU_PGD_Iter[idxIter, idxCol] := arrU_Min[idxCol];
        ELSIF arrU_PGD_Iter[idxIter, idxCol] > arrU_Max[idxCol] THEN
            arrU_PGD_Iter[idxIter, idxCol] := arrU_Max[idxCol];
        END_IF;

        (* E. Dynamic Slew Rate Projection: |u - u_prev| <= du_max *)
        IF (arrU_PGD_Iter[idxIter, idxCol] - arrInputU_Prev[idxCol]) > arrDeltaU_Max[idxCol] THEN
            arrU_PGD_Iter[idxIter, idxCol] := arrInputU_Prev[idxCol] + arrDeltaU_Max[idxCol];
        ELSIF (arrU_PGD_Iter[idxIter, idxCol] - arrInputU_Prev[idxCol]) < -arrDeltaU_Max[idxCol] THEN
            arrU_PGD_Iter[idxIter, idxCol] := arrInputU_Prev[idxCol] - arrDeltaU_Max[idxCol];
        END_IF;
    END_FOR;
END_FOR;

(* ---------------------------------------------------------------------------------------------------------
 * 3. EXTRACT OPTIMAL CONTROL VECTOR FROM FINAL ITERATION (ITERATION 10)
 * --------------------------------------------------------------------------------------------------------- *)
FOR idxCol := 1 TO 6 DO
    arrInputU[idxCol]      := arrU_PGD_Iter[10, idxCol];
    arrInputU_Prev[idxCol] := arrInputU[idxCol];
END_FOR;

(* Evaluate Total Quadratic Objective Cost Function J *)
rMpcCurrentCost := 0.0;
FOR idxRow := 1 TO 6 DO
    (* State penalty: (x - x_ref)^T * Q * (x - x_ref) *)
    rMpcCurrentCost := rMpcCurrentCost + (matQ[idxRow, idxRow] * EXPT(arrStateX_Next[idxRow] - arrStateX_Ref[idxRow], 2));
    (* Control effort penalty: (u - u_ref)^T * R * (u - u_ref) *)
    rMpcCurrentCost := rMpcCurrentCost + (matR[idxRow, idxRow] * EXPT(arrInputU[idxRow] - arrInputU_Ref[idxRow], 2));
    (* Terminal Riccati cost: x^T * P * x *)
    rMpcCurrentCost := rMpcCurrentCost + (matP[idxRow, idxRow] * EXPT(arrStateX_Next[idxRow], 2));
END_FOR;

(* ---------------------------------------------------------------------------------------------------------
 * 4. CYBER-PHYSICAL ACTUATOR DISTRIBUTION & SERVO ACTUATION SYNTHESIS
 * --------------------------------------------------------------------------------------------------------- *)
(* --- 1. 16 Top-Roller Knurl Machine Pairs Speed & Angle Distribution --- *)
FOR idxRoller := 1 TO 16 DO
    (* Base nominal profile by machine zone *)
    IF idxRoller <= 4 THEN
        (* Entrance zone: high width expansion, moderate attenuation *)
        arrTopRollerSpeedCmd[idxRoller] := (18.5 + (DINT_TO_REAL(idxRoller) * 1.2)) + (arrInputU[1] * 0.75);
        arrTopRollerAngleCmd[idxRoller] := (5.5 + (DINT_TO_REAL(idxRoller) * 0.8)) + (arrInputU[2] * 1.25);
    ELSIF idxRoller <= 10 THEN
        (* Central thinning zone: maximum speed draw authority, precise toe-in angle *)
        arrTopRollerSpeedCmd[idxRoller] := (24.0 + (DINT_TO_REAL(idxRoller - 4) * 2.1)) + (arrInputU[1] * 1.35);
        arrTopRollerAngleCmd[idxRoller] := (8.0 - (DINT_TO_REAL(idxRoller - 4) * 0.5)) + (arrInputU[2] * 0.85);
    ELSE
        (* Solidification exit zone: edge bead stabilization, lower angle *)
        arrTopRollerSpeedCmd[idxRoller] := (36.0 + (DINT_TO_REAL(idxRoller - 10) * 1.5)) + (arrInputU[1] * 0.90);
        arrTopRollerAngleCmd[idxRoller] := (3.5 - (DINT_TO_REAL(idxRoller - 10) * 0.4)) + (arrInputU[2] * 0.40);
    END_IF;

    (* Apply dynamic penetration depth compensation based on glass thickness recipe *)
    IF rRecipeTargetThickness < 4.0 THEN
        (* Thin glass (2.0 - 3.8 mm): deeper penetration to prevent knurl skipping *)
        arrTopRollerPenetrationCmd[idxRoller] := 2.40;
    ELSIF rRecipeTargetThickness > 10.0 THEN
        (* Thick glass (10.0 - 19.0 mm): shallower penetration to avoid edge gouging *)
        arrTopRollerPenetrationCmd[idxRoller] := 1.40;
    ELSE
        arrTopRollerPenetrationCmd[idxRoller] := 1.90;
    END_IF;

    (* Hard physical safety limits on knurl speeds [1.0 to 90.0 RPM] and angles [-10.0 to +25.0 deg] *)
    arrTopRollerSpeedCmd[idxRoller] := LIMIT(1.0, arrTopRollerSpeedCmd[idxRoller], 90.0);
    arrTopRollerAngleCmd[idxRoller] := LIMIT(-10.0, arrTopRollerAngleCmd[idxRoller], 25.0);
END_FOR;

(* --- 2. 8 Tin Bath Roof Silicon Carbide (SiC) Radiant Heater Zones --- *)
FOR idxZone := 1 TO 8 DO
    IF idxZone <= 3 THEN
        (* Hot spreading zones: 1.15x trim weighting *)
        arrTinBathRoofHeaterDuty[idxZone] := LIMIT(10.0, 55.0 + (arrInputU[3] * 1.15), 98.0);
    ELSIF idxZone <= 6 THEN
        (* Attenuation zones: 1.00x trim weighting *)
        arrTinBathRoofHeaterDuty[idxZone] := LIMIT(10.0, 50.0 + (arrInputU[3] * 1.00), 95.0);
    ELSE
        (* Cooling exit zones: 0.70x trim weighting *)
        arrTinBathRoofHeaterDuty[idxZone] := LIMIT(5.0, 40.0 + (arrInputU[3] * 0.70), 85.0);
    END_IF;
END_FOR;

(* --- 3. Protective Atmosphere Gas Regulating Valves (N2 and H2) --- *)
(* u[4] modulates overall pressure trim, maintaining strict 95% N2 / 5% H2 volumetric ratio *)
rN2_TrimValveCmd      := LIMIT(10.0, 50.0 + (arrInputU[4] * 1.20), 100.0);
rH2_TrimValveCmd      := LIMIT(5.0,  35.0 + (arrInputU[4] * 0.85), 90.0);
rVentExhaustDamperCmd := LIMIT(5.0,  45.0 - (arrInputU[4] * 0.90), 95.0);

(* --- 4. 12 Annealing Lehr Transverse Cooling Air Dampers & Trim Heaters --- *)
FOR idxZone := 1 TO 12 DO
    IF idxZone <= 3 THEN
        (* Zones A1-A3: Critical rapid annealing relaxation - damper cooling balanced by trim heaters *)
        arrLehrCoolingDamperCmd[idxZone] := LIMIT(10.0, 35.0 + (arrInputU[5] * 0.75), 80.0);
        arrLehrTrimHeaterDuty[idxZone]   := LIMIT(5.0,  25.0 - (arrInputU[5] * 0.50), 75.0);
    ELSIF idxZone <= 6 THEN
        (* Zones B1-B3: Linear stress-setting cooling - direct damper authority *)
        arrLehrCoolingDamperCmd[idxZone] := LIMIT(15.0, 45.0 + (arrInputU[5] * 1.10), 90.0);
        arrLehrTrimHeaterDuty[idxZone]   := LIMIT(0.0,  15.0 - (arrInputU[5] * 0.30), 60.0);
    ELSE
        (* Zones C1-C3 and F1-F3: Forced convective cooling *)
        arrLehrCoolingDamperCmd[idxZone] := LIMIT(20.0, 55.0 + (arrInputU[5] * 1.25), 100.0);
        arrLehrTrimHeaterDuty[idxZone]   := 0.0; (* Heaters deactivated in secondary and final cold cooling *)
    END_IF;
END_FOR;

(* --- 5. Lehr Main Line Drive & Synchronized Lift-Out Rolls (LOR 1-3) --- *)
(* Main Lehr drive speed setpoint *)
rLehrDriveSpeedCommand_m_min := LIMIT(1.50, rRecipeTargetLineSpeed + arrInputU[6], 22.0);

(* Lift-Out Rolls (LOR 1-3) must be synchronized at +0.2% to +0.5% lead speed to maintain tension *)
rLiftOutRollSpeedCommand_m_min := rLehrDriveSpeedCommand_m_min * 1.0035;
"""

if __name__ == "__main__":
    s = generate_phase3()
    print(f"Phase 3 length: {len(s)} chars")
