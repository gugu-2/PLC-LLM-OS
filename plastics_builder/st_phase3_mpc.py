(* =====================================================================================================================
 * PHASE 3: DISCRETE 8x8 CYBER-PHYSICAL STATE-SPACE PROPAGATION & RECEDING-HORIZON MPC OPTIMIZER
 * Mathematical Structure:
 *   Continuous LTI State-Space: dx/dt = A_c * x(t) + B_c * u(t)
 *   Discrete Discretization at Ts = 1.0 ms via Zero-Order Hold (ZOH): x[k+1] = A * x[k] + B * u[k]
 *   Receding-Horizon MPC: Multi-step trajectory prediction with active-set Projected Gradient Descent (PGD)
 * ===================================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------------------------
 * SUBSECTION 3.1: DISCRETE STATE-SPACE MATRIX INITIALIZATION (Ts = 1.0 ms)
 * State Dimension n = 8, Control Input Dimension m = 5
 * Physical constants:
 *   m_screw = 450.0 kg, beta_visc = 1250.0 N.s/m, Bulk Modulus K_polymer = 1.6e9 Pa,
 *   Cavity compliance C_cav = 2.4e-11 m3/Pa, Toggle stiffness k_toggle = 3.2e9 N/m
 * --------------------------------------------------------------------------------------------------------------------- *)
IF NOT bInitializedMatrices THEN
    (* Row 1: Screw Axial Position x[1] [mm] *)
    matA[1,1] :=  1.0000000;  matA[1,2] := -0.0009850;  matA[1,3] :=  0.0000012;  matA[1,4] :=  0.0000000;
    matA[1,5] :=  0.0000000;  matA[1,6] :=  0.0000000;  matA[1,7] :=  0.0000000;  matA[1,8] :=  0.0000008;

    (* Row 2: Screw Injection Velocity x[2] [mm/s] *)
    matA[2,1] :=  0.0000000;  matA[2,2] :=  0.9452000;  matA[2,3] := -0.0018500;  matA[2,4] := -0.0004500;
    matA[2,5] :=  0.0003200;  matA[2,6] :=  0.0000000;  matA[2,7] :=  0.0000000;  matA[2,8] := -0.0022000;

    (* Row 3: Nozzle Melt Pressure x[3] [bar] *)
    matA[3,1] :=  0.0000000;  matA[3,2] :=  1.4250000;  matA[3,3] :=  0.9125000;  matA[3,4] := -0.0850000;
    matA[3,5] := -0.0450000;  matA[3,6] :=  0.0000000;  matA[3,7] :=  0.0000000;  matA[3,8] :=  0.1500000;

    (* Row 4: Mold Cavity Pressure x[4] [bar] *)
    matA[4,1] :=  0.0000000;  matA[4,2] :=  0.2850000;  matA[4,3] :=  0.1250000;  matA[4,4] :=  0.8840000;
    matA[4,5] := -0.0220000;  matA[4,6] :=  0.0000150;  matA[4,7] :=  0.0000350;  matA[4,8] :=  0.0000000;

    (* Row 5: Extruder Bulk Melt Temperature x[5] [deg C] *)
    matA[5,1] :=  0.0000000;  matA[5,2] :=  0.0000850;  matA[5,3] :=  0.0000450;  matA[5,4] :=  0.0000000;
    matA[5,5] :=  0.9982000;  matA[5,6] :=  0.0000000;  matA[5,7] :=  0.0000000;  matA[5,8] :=  0.0000120;

    (* Row 6: Clamping Toggle Force x[6] [kN] *)
    matA[6,1] :=  0.0000000;  matA[6,2] :=  0.0000000;  matA[6,3] :=  0.0000000;  matA[6,4] :=  0.0085000;
    matA[6,5] :=  0.0150000;  matA[6,6] :=  0.9850000;  matA[6,7] :=  2.2450000;  matA[6,8] :=  0.0000000;

    (* Row 7: Tie-Bar Mean Strain Elongation x[7] [um] *)
    matA[7,1] :=  0.0000000;  matA[7,2] :=  0.0000000;  matA[7,3] :=  0.0000000;  matA[7,4] :=  0.0037500;
    matA[7,5] :=  0.0065000;  matA[7,6] :=  0.4350000;  matA[7,7] :=  0.9820000;  matA[7,8] :=  0.0000000;

    (* Row 8: Hydraulic/Servo Back Pressure x[8] [bar] *)
    matA[8,1] :=  0.0000000;  matA[8,2] := -0.0045000;  matA[8,3] :=  0.0125000;  matA[8,4] :=  0.0000000;
    matA[8,5] :=  0.0001000;  matA[8,6] :=  0.0000000;  matA[8,7] :=  0.0000000;  matA[8,8] :=  0.9250000;

    (* Discrete Input Coupling Matrix B (8x5) at Ts = 1.0 ms *)
    (* Inputs: u[1]=InjVel [mm/s], u[2]=HoldPres [bar], u[3]=ClampTonnage [kN], u[4]=HeaterMaster [%], u[5]=ScrewRPM [RPM] *)
    matB[1,1] := -0.0009850;  matB[1,2] :=  0.0000000;  matB[1,3] :=  0.0000000;  matB[1,4] :=  0.0000000;  matB[1,5] :=  0.0000000;
    matB[2,1] :=  0.0548000;  matB[2,2] := -0.0004500;  matB[2,3] :=  0.0000000;  matB[2,4] :=  0.0000000;  matB[2,5] := -0.0001200;
    matB[3,1] :=  0.2250000;  matB[3,2] :=  0.0875000;  matB[3,3] :=  0.0000000;  matB[3,4] :=  0.0000000;  matB[3,5] :=  0.0450000;
    matB[4,1] :=  0.0450000;  matB[4,2] :=  0.1160000;  matB[4,3] :=  0.0000000;  matB[4,4] :=  0.0000000;  matB[4,5] :=  0.0000000;
    matB[5,1] :=  0.0000150;  matB[5,2] :=  0.0000000;  matB[5,3] :=  0.0000000;  matB[5,4] :=  0.0018000;  matB[5,5] :=  0.0008500;
    matB[6,1] :=  0.0000000;  matB[6,2] :=  0.0000000;  matB[6,3] :=  0.0150000;  matB[6,4] :=  0.0000000;  matB[6,5] :=  0.0000000;
    matB[7,1] :=  0.0000000;  matB[7,2] :=  0.0000000;  matB[7,3] :=  0.0065000;  matB[7,4] :=  0.0000000;  matB[7,5] :=  0.0000000;
    matB[8,1] :=  0.0000000;  matB[8,2] :=  0.0000000;  matB[8,3] :=  0.0000000;  matB[8,4] :=  0.0000000;  matB[8,5] :=  0.0750000;

    (* Output Sensor Scaling Matrix C (8x8) *)
    FOR iLoop_i := 1 TO 8 DO
        FOR iLoop_j := 1 TO 8 DO
            IF iLoop_i = iLoop_j THEN
                matC[iLoop_i, iLoop_j] := 1.0;
            ELSE
                matC[iLoop_i, iLoop_j] := 0.0;
            END_IF;
        END_FOR;
    END_FOR;

    (* Direct Feedthrough Matrix D (8x5) *)
    FOR iLoop_i := 1 TO 8 DO
        FOR iLoop_j := 1 TO 5 DO
            matD[iLoop_i, iLoop_j] := 0.0;
        END_FOR;
    END_FOR;

    bInitializedMatrices := TRUE;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * SUBSECTION 3.2: CURRENT STATE VECTOR MAPPING & REFERENCE SETPOINT VECTOR
 * --------------------------------------------------------------------------------------------------------------------- *)
x_State[1] := rScrewPos_Voted_Val;
x_State[2] := rScrewVelocity_Meas;
x_State[3] := rMeltPres_Voted_Val;
x_State[4] := rCavPres_Voted_Val;
x_State[5] := rMeltTemp_Voted_Val;
x_State[6] := rTB_TotalClampForce;
x_State[7] := rTB_MeanStrain;
x_State[8] := rHydraulic_BackPres_In;

(* Determine Dynamic Target Reference Vector Based on Operational State *)
CASE iFSM_State OF
    0: (* IDLE *)
        x_Ref[1] := rDose_TargetStroke;
        x_Ref[2] := 0.0;
        x_Ref[3] := 0.0;
        x_Ref[4] := 0.0;
        x_Ref[5] := 300.0;
        x_Ref[6] := 0.0;
        x_Ref[7] := 0.0;
        x_Ref[8] := 0.0;
    1, 2: (* MOLD CLOSE / LPMP *)
        x_Ref[1] := rDose_TargetStroke;
        x_Ref[2] := 0.0;
        x_Ref[3] := 0.0;
        x_Ref[4] := 0.0;
        x_Ref[5] := 300.0;
        x_Ref[6] := 250.0;
        x_Ref[7] := 10.0;
        x_Ref[8] := 0.0;
    3, 4: (* CLAMP LOCKUP / NOZZLE TOUCH *)
        x_Ref[1] := rDose_TargetStroke;
        x_Ref[2] := 0.0;
        x_Ref[3] := 0.0;
        x_Ref[4] := 0.0;
        x_Ref[5] := 310.0;
        x_Ref[6] := rRecipe_ClampTonnage_In;
        x_Ref[7] := rRecipe_ClampTonnage_In / (4.0 * 2.280796);
        x_Ref[8] := 0.0;
    5: (* INJECTION FILLING *)
        x_Ref[1] := rVP_ScrewPosFallback;
        x_Ref[2] := rInjProfile_Vel1;
        x_Ref[3] := 1450.0;
        x_Ref[4] := rRecipe_CavityVPOvershoot_In;
        x_Ref[5] := 315.0;
        x_Ref[6] := rRecipe_ClampTonnage_In;
        x_Ref[7] := rRecipe_ClampTonnage_In / (4.0 * 2.280796);
        x_Ref[8] := 0.0;
    6, 7: (* VP TRANSFER & HOLDING *)
        x_Ref[1] := 12.0;
        x_Ref[2] := 4.0;
        x_Ref[3] := rRecipe_HoldPressure_In * 1.15;
        x_Ref[4] := rRecipe_HoldPressure_In;
        x_Ref[5] := 310.0;
        x_Ref[6] := rRecipe_ClampTonnage_In;
        x_Ref[7] := rRecipe_ClampTonnage_In / (4.0 * 2.280796);
        x_Ref[8] := 0.0;
    8: (* PLASTICIZING DOSING *)
        x_Ref[1] := rDose_TargetStroke;
        x_Ref[2] := -15.0;
        x_Ref[3] := rRecipe_BackPressure_In * 1.8;
        x_Ref[4] := 0.0;
        x_Ref[5] := 305.0;
        x_Ref[6] := rRecipe_ClampTonnage_In;
        x_Ref[7] := rRecipe_ClampTonnage_In / (4.0 * 2.280796);
        x_Ref[8] := rRecipe_BackPressure_In;
    ELSE
        x_Ref[1] := rDose_TargetStroke;
        x_Ref[2] := 0.0;
        x_Ref[3] := 0.0;
        x_Ref[4] := 0.0;
        x_Ref[5] := 300.0;
        x_Ref[6] := 0.0;
        x_Ref[7] := 0.0;
        x_Ref[8] := 0.0;
END_CASE;

(* Calculate State Tracking Error Vector *)
FOR iLoop_i := 1 TO 8 DO
    x_Error[iLoop_i] := x_State[iLoop_i] - x_Ref[iLoop_i];
END_FOR;

(* ---------------------------------------------------------------------------------------------------------------------
 * SUBSECTION 3.3: DISCRETE STATE FORWARD PREDICTION: x_pred = A * x + B * u
 * Explicitly computed without loops or matrix library calls
 * --------------------------------------------------------------------------------------------------------------------- *)
x_Pred[1] := (matA[1,1] * x_State[1]) + (matA[1,2] * x_State[2]) + (matA[1,3] * x_State[3]) + (matA[1,4] * x_State[4]) +
             (matA[1,5] * x_State[5]) + (matA[1,6] * x_State[6]) + (matA[1,7] * x_State[7]) + (matA[1,8] * x_State[8]) +
             (matB[1,1] * u_Cmd[1])   + (matB[1,2] * u_Cmd[2])   + (matB[1,3] * u_Cmd[3])   + (matB[1,4] * u_Cmd[4]) + (matB[1,5] * u_Cmd[5]);

x_Pred[2] := (matA[2,1] * x_State[1]) + (matA[2,2] * x_State[2]) + (matA[2,3] * x_State[3]) + (matA[2,4] * x_State[4]) +
             (matA[2,5] * x_State[5]) + (matA[2,6] * x_State[6]) + (matA[2,7] * x_State[7]) + (matA[2,8] * x_State[8]) +
             (matB[2,1] * u_Cmd[1])   + (matB[2,2] * u_Cmd[2])   + (matB[2,3] * u_Cmd[3])   + (matB[2,4] * u_Cmd[4]) + (matB[2,5] * u_Cmd[5]);

x_Pred[3] := (matA[3,1] * x_State[1]) + (matA[3,2] * x_State[2]) + (matA[3,3] * x_State[3]) + (matA[3,4] * x_State[4]) +
             (matA[3,5] * x_State[5]) + (matA[3,6] * x_State[6]) + (matA[3,7] * x_State[7]) + (matA[3,8] * x_State[8]) +
             (matB[3,1] * u_Cmd[1])   + (matB[3,2] * u_Cmd[2])   + (matB[3,3] * u_Cmd[3])   + (matB[3,4] * u_Cmd[4]) + (matB[3,5] * u_Cmd[5]);

x_Pred[4] := (matA[4,1] * x_State[1]) + (matA[4,2] * x_State[2]) + (matA[4,3] * x_State[3]) + (matA[4,4] * x_State[4]) +
             (matA[4,5] * x_State[5]) + (matA[4,6] * x_State[6]) + (matA[4,7] * x_State[7]) + (matA[4,8] * x_State[8]) +
             (matB[4,1] * u_Cmd[1])   + (matB[4,2] * u_Cmd[2])   + (matB[4,3] * u_Cmd[3])   + (matB[4,4] * u_Cmd[4]) + (matB[4,5] * u_Cmd[5]);

x_Pred[5] := (matA[5,1] * x_State[1]) + (matA[5,2] * x_State[2]) + (matA[5,3] * x_State[3]) + (matA[5,4] * x_State[4]) +
             (matA[5,5] * x_State[5]) + (matA[5,6] * x_State[6]) + (matA[5,7] * x_State[7]) + (matA[5,8] * x_State[8]) +
             (matB[5,1] * u_Cmd[1])   + (matB[5,2] * u_Cmd[2])   + (matB[5,3] * u_Cmd[3])   + (matB[5,4] * u_Cmd[4]) + (matB[5,5] * u_Cmd[5]);

x_Pred[6] := (matA[6,1] * x_State[1]) + (matA[6,2] * x_State[2]) + (matA[6,3] * x_State[3]) + (matA[6,4] * x_State[4]) +
             (matA[6,5] * x_State[5]) + (matA[6,6] * x_State[6]) + (matA[6,7] * x_State[7]) + (matA[6,8] * x_State[8]) +
             (matB[6,1] * u_Cmd[1])   + (matB[6,2] * u_Cmd[2])   + (matB[6,3] * u_Cmd[3])   + (matB[6,4] * u_Cmd[4]) + (matB[6,5] * u_Cmd[5]);

x_Pred[7] := (matA[7,1] * x_State[1]) + (matA[7,2] * x_State[2]) + (matA[7,3] * x_State[3]) + (matA[7,4] * x_State[4]) +
             (matA[7,5] * x_State[5]) + (matA[7,6] * x_State[6]) + (matA[7,7] * x_State[7]) + (matA[7,8] * x_State[8]) +
             (matB[7,1] * u_Cmd[1])   + (matB[7,2] * u_Cmd[2])   + (matB[7,3] * u_Cmd[3])   + (matB[7,4] * u_Cmd[4]) + (matB[7,5] * u_Cmd[5]);

x_Pred[8] := (matA[8,1] * x_State[1]) + (matA[8,2] * x_State[2]) + (matA[8,3] * x_State[3]) + (matA[8,4] * x_State[4]) +
             (matA[8,5] * x_State[5]) + (matA[8,6] * x_State[6]) + (matA[8,7] * x_State[7]) + (matA[8,8] * x_State[8]) +
             (matB[8,1] * u_Cmd[1])   + (matB[8,2] * u_Cmd[2])   + (matB[8,3] * u_Cmd[3])   + (matB[8,4] * u_Cmd[4]) + (matB[8,5] * u_Cmd[5]);

(* ---------------------------------------------------------------------------------------------------------------------
 * SUBSECTION 3.4: RECEDING-HORIZON QUADRATIC OPTIMIZATION WITH PROJECTED GRADIENT DESCENT (PGD)
 * Optimization Objective:
 *   min J = sum_{h=1..Np} [ (x_h - x_ref)^T Q (x_h - x_ref) ] + sum_{k=1..Nc} [ u_k^T R u_k + Delta_u_k^T S Delta_u_k ]
 * Subject to:
 *   u_Min[k] <= u[k] <= u_Max[k],  |u[k] - u_prev[k]| <= u_MaxSlew[k]
 * --------------------------------------------------------------------------------------------------------------------- *)
(* Initialize PGD Candidate Vector with Previous Control Command *)
FOR iLoop_j := 1 TO 5 DO
    u_Candidate[iLoop_j] := u_Cmd[iLoop_j];
END_FOR;

bMPC_Converged := FALSE;

(* PGD Iteration Loop (5 Iterations per 1.0 ms cycle) *)
FOR iMPC_IterCounter := 1 TO 5 DO
    (* 1. Multi-Step Forward Simulation over Horizon Np = 5 *)
    FOR iLoop_k := 1 TO 5 DO
        IF iLoop_k = 1 THEN
            FOR iLoop_i := 1 TO 8 DO
                x_Horizon[1, iLoop_i] := (matA[iLoop_i, 1] * x_State[1]) + (matA[iLoop_i, 2] * x_State[2]) +
                                         (matA[iLoop_i, 3] * x_State[3]) + (matA[iLoop_i, 4] * x_State[4]) +
                                         (matA[iLoop_i, 5] * x_State[5]) + (matA[iLoop_i, 6] * x_State[6]) +
                                         (matA[iLoop_i, 7] * x_State[7]) + (matA[iLoop_i, 8] * x_State[8]) +
                                         (matB[iLoop_i, 1] * u_Candidate[1]) + (matB[iLoop_i, 2] * u_Candidate[2]) +
                                         (matB[iLoop_i, 3] * u_Candidate[3]) + (matB[iLoop_i, 4] * u_Candidate[4]) +
                                         (matB[iLoop_i, 5] * u_Candidate[5]);
            END_FOR;
        ELSE
            FOR iLoop_i := 1 TO 8 DO
                x_Horizon[iLoop_k, iLoop_i] := (matA[iLoop_i, 1] * x_Horizon[iLoop_k - 1, 1]) +
                                               (matA[iLoop_i, 2] * x_Horizon[iLoop_k - 1, 2]) +
                                               (matA[iLoop_i, 3] * x_Horizon[iLoop_k - 1, 3]) +
                                               (matA[iLoop_i, 4] * x_Horizon[iLoop_k - 1, 4]) +
                                               (matA[iLoop_i, 5] * x_Horizon[iLoop_k - 1, 5]) +
                                               (matA[iLoop_i, 6] * x_Horizon[iLoop_k - 1, 6]) +
                                               (matA[iLoop_i, 7] * x_Horizon[iLoop_k - 1, 7]) +
                                               (matA[iLoop_i, 8] * x_Horizon[iLoop_k - 1, 8]) +
                                               (matB[iLoop_i, 1] * u_Candidate[1]) + (matB[iLoop_i, 2] * u_Candidate[2]) +
                                               (matB[iLoop_i, 3] * u_Candidate[3]) + (matB[iLoop_i, 4] * u_Candidate[4]) +
                                               (matB[iLoop_i, 5] * u_Candidate[5]);
            END_FOR;
        END_IF;
    END_FOR;

    (* 2. Compute Cost Functional Evaluation J *)
    rMPC_CostObjective := 0.0;
    FOR iLoop_k := 1 TO 5 DO
        FOR iLoop_i := 1 TO 8 DO
            rTemp_Delta := x_Horizon[iLoop_k, iLoop_i] - x_Ref[iLoop_i];
            rMPC_CostObjective := rMPC_CostObjective + (rMPC_WeightQ[iLoop_i] * rTemp_Delta * rTemp_Delta);
        END_FOR;
    END_FOR;

    FOR iLoop_j := 1 TO 5 DO
        rMPC_CostObjective := rMPC_CostObjective + (rMPC_WeightR[iLoop_j] * u_Candidate[iLoop_j] * u_Candidate[iLoop_j]);
        rTemp_Diff := u_Candidate[iLoop_j] - u_Prev[iLoop_j];
        rMPC_CostObjective := rMPC_CostObjective + (rMPC_WeightS[iLoop_j] * rTemp_Diff * rTemp_Diff);
    END_FOR;

    (* 3. Compute Analytic Gradient Vector Grad_J(u) *)
    FOR iLoop_j := 1 TO 5 DO
        (* Actuator Effort and Slew Rate Gradient Components *)
        u_Grad[iLoop_j] := (2.0 * rMPC_WeightR[iLoop_j] * u_Candidate[iLoop_j]) +
                           (2.0 * rMPC_WeightS[iLoop_j] * (u_Candidate[iLoop_j] - u_Prev[iLoop_j]));

        (* Backpropagation of Tracking Error through Input Matrix B *)
        FOR iLoop_k := 1 TO 5 DO
            FOR iLoop_i := 1 TO 8 DO
                rTemp_Delta := x_Horizon[iLoop_k, iLoop_i] - x_Ref[iLoop_i];
                u_Grad[iLoop_j] := u_Grad[iLoop_j] + (2.0 * rMPC_WeightQ[iLoop_i] * matB[iLoop_i, iLoop_j] * rTemp_Delta);
            END_FOR;
        END_FOR;
    END_FOR;

    (* 4. Compute Euclidean Norm of Gradient for Stopping Metric *)
    rMPC_GradNorm := SQRT((u_Grad[1] * u_Grad[1]) + (u_Grad[2] * u_Grad[2]) + (u_Grad[3] * u_Grad[3]) +
                          (u_Grad[4] * u_Grad[4]) + (u_Grad[5] * u_Grad[5]));

    IF rMPC_GradNorm < rMPC_GradTolerance THEN
        bMPC_Converged := TRUE;
    END_IF;

    (* 5. Projected Gradient Step with Box Saturation and Slew Clamping *)
    FOR iLoop_j := 1 TO 5 DO
        (* Gradient Descent Step *)
        u_Candidate[iLoop_j] := u_Candidate[iLoop_j] - (rMPC_StepSize_Alpha * u_Grad[iLoop_j]);

        (* Actuator Physical Box Saturation: [u_Min, u_Max] *)
        IF u_Candidate[iLoop_j] > u_Max[iLoop_j] THEN
            u_Candidate[iLoop_j] := u_Max[iLoop_j];
        ELSIF u_Candidate[iLoop_j] < u_Min[iLoop_j] THEN
            u_Candidate[iLoop_j] := u_Min[iLoop_j];
        END_IF;

        (* Dynamic Actuator Slew Rate Limiters: |Delta u| <= MaxSlew *)
        rTemp_Delta := u_Candidate[iLoop_j] - u_Prev[iLoop_j];
        IF rTemp_Delta > u_MaxSlew[iLoop_j] THEN
            u_Candidate[iLoop_j] := u_Prev[iLoop_j] + u_MaxSlew[iLoop_j];
        ELSIF rTemp_Delta < (-1.0 * u_MaxSlew[iLoop_j]) THEN
            u_Candidate[iLoop_j] := u_Prev[iLoop_j] - u_MaxSlew[iLoop_j];
        END_IF;
    END_FOR;
END_FOR;

(* Store Previous Inputs and Assign MPC Outputs *)
FOR iLoop_j := 1 TO 5 DO
    u_Prev[iLoop_j] := u_Cmd[iLoop_j];
    u_Cmd[iLoop_j] := u_Candidate[iLoop_j];
END_FOR;
