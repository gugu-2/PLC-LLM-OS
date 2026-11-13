# scratch/gen_phase3.py

def get_phase3():
    lines = []
    lines.append("""
(* ============================================================================== *)
(* PHASE 3: RECEDING-HORIZON MPC OPTIMIZATION WITH PGD & SLEW LIMITS              *)
(* ============================================================================== *)
(* Receding Horizon N = 5 steps, 6 Projected Gradient Descent (PGD) iterations.   *)
(* Dynamic non-minimum phase shrink/swell feedforward compensation.               *)
(* Actuator constraints: [0.0..100.0 %], max slew rate 5.0 %/s (0.125 %/scan).    *)
(* ------------------------------------------------------------------------------ *)

(* ----------------------------------------------------------------------------- *)
(* STEP 1: DYNAMIC INVERSE RESPONSE (SHRINK/SWELL) FEEDFORWARD COMPENSATION     *)
(* Cancels prompt false level rise on steam draw & false plunge on cold feedwater*)
(* ----------------------------------------------------------------------------- *)
fDerivSteamFlow := (fVotedSteamFlow_t_h - fSteamFlow_Filtered_Prev) / fCycleTime_Ts;
fDerivFeedwaterFlow := (fVotedFeedwaterFlow_t_h - fFeedwaterFlow_Filtered_Prev) / fCycleTime_Ts;
fSteamFlow_Filtered_Prev := fVotedSteamFlow_t_h;
fFeedwaterFlow_Filtered_Prev := fVotedFeedwaterFlow_t_h;

(* Dynamic Lead-Lag Filter discrete update: tau_lag = 0.40s, Ts = 0.025s -> alpha = 0.940 *)
fLeadLagInternalState := (0.94000000 * fLeadLagInternalState) + 
                         (0.06000000 * ((0.04500000 * fDerivSteamFlow) - (0.03500000 * fDerivFeedwaterFlow)));

(* Anti-swell bias: negative bias when steam flow surges (suppresses false swell) *)
fAntiSwellBias := fLeadLagInternalState;
fShrinkSwellCompensatedDemand_pct := fAntiSwellBias;

(* ----------------------------------------------------------------------------- *)
(* STEP 2: POWER-DEPENDENT TARGET REFERENCE TRAJECTORY GENERATION               *)
(* Level setpoint programmed to ramp from 0 mm NWL at 0% power to +50 mm at 100% *)
(* ----------------------------------------------------------------------------- *)
fPowerFraction := fNI_ReactorThermalPower / 100.00000000;
IF fPowerFraction < 0.00000000 THEN
    fPowerFraction := 0.00000000;
ELSIF fPowerFraction > 1.20000000 THEN
    fPowerFraction := 1.20000000;
END_IF;

fProgrammedLevelTarget := 0.00000000 + (fPowerFraction * 50.00000000) + fOperatorLevelBias_mm;

(* Establish Reference Vectors r_mpc_ref across Horizon N = 5 steps *)
FOR nStepIdx := 1 TO 5 DO
    r_mpc_ref[nStepIdx, 1] := fProgrammedLevelTarget;
    r_mpc_ref[nStepIdx, 2] := (fVotedSteamFlow_t_h / 3.60000000); (* Balanced mass flow *)
    r_mpc_ref[nStepIdx, 3] := 0.42500000 * fPowerFraction; (* Void fraction target *)
    r_mpc_ref[nStepIdx, 4] := 950.00000000 * fPowerFraction; (* Heat transfer target [MW] *)
    r_mpc_ref[nStepIdx, 5] := 68.50000000; (* Steam drum rated pressure [bar] *)
    r_mpc_ref[nStepIdx, 6] := 292.00000000; (* Cold leg reference temperature [deg C] *)
    r_mpc_ref[nStepIdx, 7] := (fVotedSteamFlow_t_h / 2500.00000000) * 100.00000000; (* Nominal trim *)
    r_mpc_ref[nStepIdx, 8] := 0.00000000; (* Zero non-minimum phase residual *)
END_FOR;

(* ----------------------------------------------------------------------------- *)
(* STEP 3: CONTROL TRAJECTORY WARM-START FROM PREVIOUS RECESSED CYCLE            *)
(* ----------------------------------------------------------------------------- *)
u_mpc_horiz[1, 1] := u_mpc_horiz[2, 1];
u_mpc_horiz[1, 2] := u_mpc_horiz[2, 2];
u_mpc_horiz[2, 1] := u_mpc_horiz[3, 1];
u_mpc_horiz[2, 2] := u_mpc_horiz[3, 2];
u_mpc_horiz[3, 1] := u_mpc_horiz[4, 1];
u_mpc_horiz[3, 2] := u_mpc_horiz[4, 2];
u_mpc_horiz[4, 1] := u_mpc_horiz[5, 1];
u_mpc_horiz[4, 2] := u_mpc_horiz[5, 2];
u_mpc_horiz[5, 1] := u_mpc_horiz[4, 1];
u_mpc_horiz[5, 2] := u_mpc_horiz[4, 2];

(* ----------------------------------------------------------------------------- *)
(* STEP 4: PROJECTED GRADIENT DESCENT (PGD) OPTIMIZATION LOOP (6 ITERATIONS)     *)
(* ----------------------------------------------------------------------------- *)
FOR nIterIdx := 1 TO 6 DO
    (* --- Sub-step 4.1: Forward State Trajectory Rollout across Horizon N = 5 --- *)
    (* Step 1 Rollout starting from current observer state x_hat *)
    x_mpc_horiz[1, 1] := (A_Matrix[1, 1] * x_hat[1]) + (A_Matrix[1, 2] * x_hat[2]) + 
                         (A_Matrix[1, 3] * x_hat[3]) + (A_Matrix[1, 4] * x_hat[4]) + 
                         (A_Matrix[1, 5] * x_hat[5]) + (A_Matrix[1, 6] * x_hat[6]) + 
                         (A_Matrix[1, 7] * x_hat[7]) + (A_Matrix[1, 8] * x_hat[8]) + 
                         (B_Matrix[1, 1] * u_mpc_horiz[1, 1]) + (B_Matrix[1, 2] * u_mpc_horiz[1, 2]) + 
                         (B_Matrix[1, 3] * u_vector[3]) + (B_Matrix[1, 4] * u_vector[4]) + 
                         (B_Matrix[1, 5] * u_vector[5]);

    x_mpc_horiz[1, 2] := (A_Matrix[2, 1] * x_hat[1]) + (A_Matrix[2, 2] * x_hat[2]) + 
                         (A_Matrix[2, 3] * x_hat[3]) + (A_Matrix[2, 4] * x_hat[4]) + 
                         (A_Matrix[2, 5] * x_hat[5]) + (A_Matrix[2, 6] * x_hat[6]) + 
                         (A_Matrix[2, 7] * x_hat[7]) + (A_Matrix[2, 8] * x_hat[8]) + 
                         (B_Matrix[2, 1] * u_mpc_horiz[1, 1]) + (B_Matrix[2, 2] * u_mpc_horiz[1, 2]) + 
                         (B_Matrix[2, 3] * u_vector[3]) + (B_Matrix[2, 4] * u_vector[4]) + 
                         (B_Matrix[2, 5] * u_vector[5]);

    x_mpc_horiz[1, 3] := (A_Matrix[3, 1] * x_hat[1]) + (A_Matrix[3, 2] * x_hat[2]) + 
                         (A_Matrix[3, 3] * x_hat[3]) + (A_Matrix[3, 4] * x_hat[4]) + 
                         (A_Matrix[3, 5] * x_hat[5]) + (A_Matrix[3, 6] * x_hat[6]) + 
                         (A_Matrix[3, 7] * x_hat[7]) + (A_Matrix[3, 8] * x_hat[8]) + 
                         (B_Matrix[3, 1] * u_mpc_horiz[1, 1]) + (B_Matrix[3, 2] * u_mpc_horiz[1, 2]) + 
                         (B_Matrix[3, 3] * u_vector[3]) + (B_Matrix[3, 4] * u_vector[4]) + 
                         (B_Matrix[3, 5] * u_vector[5]);

    x_mpc_horiz[1, 4] := (A_Matrix[4, 1] * x_hat[1]) + (A_Matrix[4, 2] * x_hat[2]) + 
                         (A_Matrix[4, 3] * x_hat[3]) + (A_Matrix[4, 4] * x_hat[4]) + 
                         (A_Matrix[4, 5] * x_hat[5]) + (A_Matrix[4, 6] * x_hat[6]) + 
                         (A_Matrix[4, 7] * x_hat[7]) + (A_Matrix[4, 8] * x_hat[8]) + 
                         (B_Matrix[4, 1] * u_mpc_horiz[1, 1]) + (B_Matrix[4, 2] * u_mpc_horiz[1, 2]) + 
                         (B_Matrix[4, 3] * u_vector[3]) + (B_Matrix[4, 4] * u_vector[4]) + 
                         (B_Matrix[4, 5] * u_vector[5]);

    x_mpc_horiz[1, 5] := (A_Matrix[5, 1] * x_hat[1]) + (A_Matrix[5, 2] * x_hat[2]) + 
                         (A_Matrix[5, 3] * x_hat[3]) + (A_Matrix[5, 4] * x_hat[4]) + 
                         (A_Matrix[5, 5] * x_hat[5]) + (A_Matrix[5, 6] * x_hat[6]) + 
                         (A_Matrix[5, 7] * x_hat[7]) + (A_Matrix[5, 8] * x_hat[8]) + 
                         (B_Matrix[5, 1] * u_mpc_horiz[1, 1]) + (B_Matrix[5, 2] * u_mpc_horiz[1, 2]) + 
                         (B_Matrix[5, 3] * u_vector[3]) + (B_Matrix[5, 4] * u_vector[4]) + 
                         (B_Matrix[5, 5] * u_vector[5]);

    x_mpc_horiz[1, 6] := (A_Matrix[6, 1] * x_hat[1]) + (A_Matrix[6, 2] * x_hat[2]) + 
                         (A_Matrix[6, 3] * x_hat[3]) + (A_Matrix[6, 4] * x_hat[4]) + 
                         (A_Matrix[6, 5] * x_hat[5]) + (A_Matrix[6, 6] * x_hat[6]) + 
                         (A_Matrix[6, 7] * x_hat[7]) + (A_Matrix[6, 8] * x_hat[8]) + 
                         (B_Matrix[6, 1] * u_mpc_horiz[1, 1]) + (B_Matrix[6, 2] * u_mpc_horiz[1, 2]) + 
                         (B_Matrix[6, 3] * u_vector[3]) + (B_Matrix[6, 4] * u_vector[4]) + 
                         (B_Matrix[6, 5] * u_vector[5]);

    x_mpc_horiz[1, 7] := (A_Matrix[7, 1] * x_hat[1]) + (A_Matrix[7, 2] * x_hat[2]) + 
                         (A_Matrix[7, 3] * x_hat[3]) + (A_Matrix[7, 4] * x_hat[4]) + 
                         (A_Matrix[7, 5] * x_hat[5]) + (A_Matrix[7, 6] * x_hat[6]) + 
                         (A_Matrix[7, 7] * x_hat[7]) + (A_Matrix[7, 8] * x_hat[8]) + 
                         (B_Matrix[7, 1] * u_mpc_horiz[1, 1]) + (B_Matrix[7, 2] * u_mpc_horiz[1, 2]) + 
                         (B_Matrix[7, 3] * u_vector[3]) + (B_Matrix[7, 4] * u_vector[4]) + 
                         (B_Matrix[7, 5] * u_vector[5]);

    x_mpc_horiz[1, 8] := (A_Matrix[8, 1] * x_hat[1]) + (A_Matrix[8, 2] * x_hat[2]) + 
                         (A_Matrix[8, 3] * x_hat[3]) + (A_Matrix[8, 4] * x_hat[4]) + 
                         (A_Matrix[8, 5] * x_hat[5]) + (A_Matrix[8, 6] * x_hat[6]) + 
                         (A_Matrix[8, 7] * x_hat[7]) + (A_Matrix[8, 8] * x_hat[8]) + 
                         (B_Matrix[8, 1] * u_mpc_horiz[1, 1]) + (B_Matrix[8, 2] * u_mpc_horiz[1, 2]) + 
                         (B_Matrix[8, 3] * u_vector[3]) + (B_Matrix[8, 4] * u_vector[4]) + 
                         (B_Matrix[8, 5] * u_vector[5]);

    (* Steps 2 to 5 Forward State Propagation *)
    FOR nStepIdx := 2 TO 5 DO
        FOR nLoopIdx1 := 1 TO 8 DO
            fTempSum := 0.00000000;
            FOR nLoopIdx2 := 1 TO 8 DO
                fTempSum := fTempSum + (A_Matrix[nLoopIdx1, nLoopIdx2] * x_mpc_horiz[nStepIdx - 1, nLoopIdx2]);
            END_FOR;
            fTempSum := fTempSum + (B_Matrix[nLoopIdx1, 1] * u_mpc_horiz[nStepIdx, 1]);
            fTempSum := fTempSum + (B_Matrix[nLoopIdx1, 2] * u_mpc_horiz[nStepIdx, 2]);
            fTempSum := fTempSum + (B_Matrix[nLoopIdx1, 3] * u_vector[3]);
            fTempSum := fTempSum + (B_Matrix[nLoopIdx1, 4] * u_vector[4]);
            fTempSum := fTempSum + (B_Matrix[nLoopIdx1, 5] * u_vector[5]);
            x_mpc_horiz[nStepIdx, nLoopIdx1] := fTempSum;
        END_FOR;
    END_FOR;

    (* --- Sub-step 4.2: Adjoint / Costate Backpropagation --- *)
    (* Terminal Step 5 Costate: lambda_5 = P * (x_5 - r_5) *)
    FOR nLoopIdx1 := 1 TO 8 DO
        lambda_mpc[5, nLoopIdx1] := P_diag[nLoopIdx1] * (x_mpc_horiz[5, nLoopIdx1] - r_mpc_ref[5, nLoopIdx1]);
    END_FOR;

    (* Steps 4 down to 1 Costate Backpropagation *)
    FOR nStepIdx := 4 TO 1 BY -1 DO
        FOR nLoopIdx1 := 1 TO 8 DO
            fTempSum := Q_diag[nLoopIdx1] * (x_mpc_horiz[nStepIdx, nLoopIdx1] - r_mpc_ref[nStepIdx, nLoopIdx1]);
            FOR nLoopIdx2 := 1 TO 8 DO
                fTempSum := fTempSum + (A_Matrix[nLoopIdx2, nLoopIdx1] * lambda_mpc[nStepIdx + 1, nLoopIdx2]);
            END_FOR;
            lambda_mpc[nStepIdx, nLoopIdx1] := fTempSum;
        END_FOR;
    END_FOR;

    (* --- Sub-step 4.3: Gradient Computation w.r.t Manipulated Inputs --- *)
    FOR nStepIdx := 1 TO 5 DO
        (* Gradient for MFRV (Input 1) *)
        fTempSum := 0.00000000;
        FOR nLoopIdx1 := 1 TO 8 DO
            fTempSum := fTempSum + (B_Matrix[nLoopIdx1, 1] * lambda_mpc[nStepIdx, nLoopIdx1]);
        END_FOR;
        fTempSum := fTempSum + (R_diag[1] * u_mpc_horiz[nStepIdx, 1]);
        IF nStepIdx = 1 THEN
            fTempSum := fTempSum + (S_diag[1] * (u_mpc_horiz[1, 1] - u_prev_cycle[1]));
        ELSE
            fTempSum := fTempSum + (S_diag[1] * (u_mpc_horiz[nStepIdx, 1] - u_mpc_horiz[nStepIdx - 1, 1]));
        END_IF;
        grad_u_mpc[nStepIdx, 1] := fTempSum;

        (* Gradient for BPV (Input 2) *)
        fTempSum := 0.00000000;
        FOR nLoopIdx1 := 1 TO 8 DO
            fTempSum := fTempSum + (B_Matrix[nLoopIdx1, 2] * lambda_mpc[nStepIdx, nLoopIdx1]);
        END_FOR;
        fTempSum := fTempSum + (R_diag[2] * u_mpc_horiz[nStepIdx, 2]);
        IF nStepIdx = 1 THEN
            fTempSum := fTempSum + (S_diag[2] * (u_mpc_horiz[1, 2] - u_prev_cycle[2]));
        ELSE
            fTempSum := fTempSum + (S_diag[2] * (u_mpc_horiz[nStepIdx, 2] - u_mpc_horiz[nStepIdx - 1, 2]));
        END_IF;
        grad_u_mpc[nStepIdx, 2] := fTempSum;
    END_FOR;

    (* --- Sub-step 4.4: Gradient Descent Update with Slew and Box Projection --- *)
    fMaxAllowedDelta := 5.00000000 * fCycleTime_Ts; (* Max 5.0%/s = 0.125% per 25 ms scan *)

    FOR nStepIdx := 1 TO 5 DO
        (* Update Input 1: MFRV *)
        fTrialInput := u_mpc_horiz[nStepIdx, 1] - (0.04500000 * grad_u_mpc[nStepIdx, 1]);
        IF nStepIdx = 1 THEN
            fTempDelta := fTrialInput - u_prev_cycle[1];
            IF fTempDelta > fMaxAllowedDelta THEN
                fTrialInput := u_prev_cycle[1] + fMaxAllowedDelta;
            ELSIF fTempDelta < -fMaxAllowedDelta THEN
                fTrialInput := u_prev_cycle[1] - fMaxAllowedDelta;
            END_IF;
        ELSE
            fTempDelta := fTrialInput - u_mpc_horiz[nStepIdx - 1, 1];
            IF fTempDelta > fMaxAllowedDelta THEN
                fTrialInput := u_mpc_horiz[nStepIdx - 1, 1] + fMaxAllowedDelta;
            ELSIF fTempDelta < -fMaxAllowedDelta THEN
                fTrialInput := u_mpc_horiz[nStepIdx - 1, 1] - fMaxAllowedDelta;
            END_IF;
        END_IF;
        (* Box Constraint Projection [0.0..100.0 %] *)
        IF fTrialInput < 0.00000000 THEN
            fTrialInput := 0.00000000;
        ELSIF fTrialInput > 100.00000000 THEN
            fTrialInput := 100.00000000;
        END_IF;
        u_mpc_horiz[nStepIdx, 1] := fTrialInput;

        (* Update Input 2: BPV *)
        fTrialInput := u_mpc_horiz[nStepIdx, 2] - (0.04500000 * grad_u_mpc[nStepIdx, 2]);
        IF nStepIdx = 1 THEN
            fTempDelta := fTrialInput - u_prev_cycle[2];
            IF fTempDelta > fMaxAllowedDelta THEN
                fTrialInput := u_prev_cycle[2] + fMaxAllowedDelta;
            ELSIF fTempDelta < -fMaxAllowedDelta THEN
                fTrialInput := u_prev_cycle[2] - fMaxAllowedDelta;
            END_IF;
        ELSE
            fTempDelta := fTrialInput - u_mpc_horiz[nStepIdx - 1, 2];
            IF fTempDelta > fMaxAllowedDelta THEN
                fTrialInput := u_mpc_horiz[nStepIdx - 1, 2] + fMaxAllowedDelta;
            ELSIF fTempDelta < -fMaxAllowedDelta THEN
                fTrialInput := u_mpc_horiz[nStepIdx - 1, 2] - fMaxAllowedDelta;
            END_IF;
        END_IF;
        (* Box Constraint Projection [0.0..100.0 %] *)
        IF fTrialInput < 0.00000000 THEN
            fTrialInput := 0.00000000;
        ELSIF fTrialInput > 100.00000000 THEN
            fTrialInput := 100.00000000;
        END_IF;
        u_mpc_horiz[nStepIdx, 2] := fTrialInput;
    END_FOR;
END_FOR;

(* ----------------------------------------------------------------------------- *)
(* STEP 5: EXTRACT OPTIMAL ACTUATION COMMANDS & EVALUATE OBJECTIVE COST          *)
(* ----------------------------------------------------------------------------- *)
fTrialInput := u_mpc_horiz[1, 1] + fAntiSwellBias;
IF fTrialInput < 0.00000000 THEN
    fTrialInput := 0.00000000;
ELSIF fTrialInput > 100.00000000 THEN
    fTrialInput := 100.00000000;
END_IF;
fMFRV_PositionDemand := fTrialInput;
fBPV_PositionDemand := u_mpc_horiz[1, 2];

u_prev_cycle[1] := fMFRV_PositionDemand;
u_prev_cycle[2] := fBPV_PositionDemand;

(* Compute Receding Horizon Quadratic Objective Cost Value J *)
fMPC_ComputedCostJ := 0.00000000;
FOR nStepIdx := 1 TO 5 DO
    FOR nLoopIdx1 := 1 TO 8 DO
        fTempDelta := x_mpc_horiz[nStepIdx, nLoopIdx1] - r_mpc_ref[nStepIdx, nLoopIdx1];
        IF nStepIdx = 5 THEN
            fMPC_ComputedCostJ := fMPC_ComputedCostJ + (P_diag[nLoopIdx1] * fTempDelta * fTempDelta);
        ELSE
            fMPC_ComputedCostJ := fMPC_ComputedCostJ + (Q_diag[nLoopIdx1] * fTempDelta * fTempDelta);
        END_IF;
    END_FOR;
    fMPC_ComputedCostJ := fMPC_ComputedCostJ + (R_diag[1] * u_mpc_horiz[nStepIdx, 1] * u_mpc_horiz[nStepIdx, 1]);
    fMPC_ComputedCostJ := fMPC_ComputedCostJ + (R_diag[2] * u_mpc_horiz[nStepIdx, 2] * u_mpc_horiz[nStepIdx, 2]);
END_FOR;
""")
    return "".join(lines)

if __name__ == "__main__":
    p3 = get_phase3()
    print(f"Phase 3 generated. Length: {len(p3)} characters.")
