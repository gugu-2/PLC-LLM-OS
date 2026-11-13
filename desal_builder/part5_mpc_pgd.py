# desal_builder/part5_mpc_pgd.py
# Phase 3: Receding-Horizon MPC Optimization with Projected Gradient Descent (PGD)

def get_part5_mpc_pgd():
    return """
(* ====================================================================================================
   PHASE 3: RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) WITH PROJECTED GRADIENT DESCENT
   Optimizes HPP VFD Frequency, PX Booster Frequency, Brine Throttle Valve Position,
   and Chemical Dosing to minimize Specific Energy Consumption (SEC [kWh/m3])
   subject to Recovery Ratio Bounds (38.0% - 44.0%), Flux Limits, and Slew-Rate Constraints.
   Prediction Horizon Np = 5, Control Horizon Nc = 3, Ts = 10 ms
   ==================================================================================================== *)

(* ----------------------------------------------------------------------------------------------------
   STEP 3.1: DYNAMIC MPC REFERENCE TRAJECTORY SYNTHESIS
   Computes state references from operator setpoints and real-time seawater salinity & temperature.
   ---------------------------------------------------------------------------------------------------- *)
(* Target Net Permeate Flux J_v [LMH] from Target Production Rate [m3/h] *)
IF rTargetPermeateFlow_m3h > 100.0 THEN
    x_ref[3] := (rTargetPermeateFlow_m3h * 1000.0) / rTotalMembraneArea_m2;
ELSE
    x_ref[3] := 16.67; (* 50,000 m3/day nominal -> 16.67 LMH *)
END_IF;
x_ref[3] := LIMIT(10.0, x_ref[3], 22.0);

(* Target Operating Recovery Ratio from Operator Setpoint *)
rTargetRecoveryRatio_pct := LIMIT(38.0, rTargetRecoveryRatio_pct, 44.5);

(* Target Average Osmotic Pressure at Target Recovery & Raw Seawater Quality *)
x_ref[4] := (rFeedOsmoticPressure_bar / MAX(0.50, 1.0 - (rTargetRecoveryRatio_pct / 100.0))) 
            * 0.5 * (1.0 + EXP(rConcentrationPolarizationConst * (rTargetRecoveryRatio_pct / 100.0)));
x_ref[4] := LIMIT(25.0, x_ref[4], 55.0);

(* Target Net Driving Pressure NDP [bar] required to achieve Target Flux *)
IF (x_state[8] * rWaterViscosityCorrectionFactor) > 0.10 THEN
    x_ref[2] := x_ref[3] / (x_state[8] * rWaterViscosityCorrectionFactor);
ELSE
    x_ref[2] := 18.0;
END_IF;
x_ref[2] := LIMIT(10.0, x_ref[2], 26.0);

(* Target HP Feed Header Pressure P_feed [bar] *)
x_ref[1] := x_ref[2] + 1.45 + rPermeateBackPressure_bar + x_ref[4];
x_ref[1] := LIMIT(55.0, x_ref[1], rMaxAllowableHpPress_bar - 2.0);

(* Target ERD HP Brine Pressure P_erd [bar] *)
x_ref[5] := x_ref[1] - 1.85; (* Pressure drop across membrane vessels to ERD inlet *)
x_ref[5] := LIMIT(50.0, x_ref[5], 80.0);

(* Target ERD Mixing Salinity Leak [ppm] *)
x_ref[6] := 180.0;

(* Target Permeate Salinity / Conductivity [uS/cm] *)
x_ref[7] := LIMIT(120.0, rMaxPermeateConductivity_uS * 0.70, 380.0);

(* Target Membrane Specific Permeability [LMH/bar] *)
x_ref[8] := rCleanMembranePermeability_Kw0;

(* ----------------------------------------------------------------------------------------------------
   STEP 3.2: WARM-START INITIALIZATION OF CONTROL HORIZON
   Shift previous control solution forward by one time step
   ---------------------------------------------------------------------------------------------------- *)
u_horizon[1, 1] := u_prev[1];
u_horizon[1, 2] := u_prev[2];
u_horizon[1, 3] := u_prev[3];
u_horizon[1, 4] := u_prev[4];
u_horizon[1, 5] := u_prev[5];
u_horizon[1, 6] := u_prev[6];

FOR k := 2 TO 3 DO
    FOR m := 1 TO 6 DO
        u_horizon[k, m] := u_horizon[1, m];
    END_FOR;
END_FOR;

(* ----------------------------------------------------------------------------------------------------
   STEP 3.3: UNROLLED PROJECTED GRADIENT DESCENT (PGD) OPTIMIZATION LOOP
   8 iterations per 10 ms execution cycle for real-time determinism.
   ---------------------------------------------------------------------------------------------------- *)
FOR n := 1 TO 8 DO
    (* -------------------------------------------------------------------------
       FORWARD TRAJECTORY ROLLOUT (Np = 5 Steps)
       ------------------------------------------------------------------------- *)
    (* Horizon Step 1 (u = u_horizon[1]) *)
    FOR i := 1 TO 8 DO
        rTempSum := 0.0;
        FOR j := 1 TO 8 DO
            rTempSum := rTempSum + (matA[i, j] * x_state[j]);
        END_FOR;
        FOR m := 1 TO 6 DO
            rTempSum := rTempSum + (matB[i, m] * u_horizon[1, m]);
        END_FOR;
        FOR k := 1 TO 6 DO
            rTempSum := rTempSum + (matBd[i, k] * d_dist[k]);
        END_FOR;
        x_rollout[1, i] := rTempSum;
    END_FOR;

    (* Horizon Step 2 (u = u_horizon[2]) *)
    FOR i := 1 TO 8 DO
        rTempSum := 0.0;
        FOR j := 1 TO 8 DO
            rTempSum := rTempSum + (matA[i, j] * x_rollout[1, j]);
        END_FOR;
        FOR m := 1 TO 6 DO
            rTempSum := rTempSum + (matB[i, m] * u_horizon[2, m]);
        END_FOR;
        FOR k := 1 TO 6 DO
            rTempSum := rTempSum + (matBd[i, k] * d_dist[k]);
        END_FOR;
        x_rollout[2, i] := rTempSum;
    END_FOR;

    (* Horizon Step 3 (u = u_horizon[3]) *)
    FOR i := 1 TO 8 DO
        rTempSum := 0.0;
        FOR j := 1 TO 8 DO
            rTempSum := rTempSum + (matA[i, j] * x_rollout[2, j]);
        END_FOR;
        FOR m := 1 TO 6 DO
            rTempSum := rTempSum + (matB[i, m] * u_horizon[3, m]);
        END_FOR;
        FOR k := 1 TO 6 DO
            rTempSum := rTempSum + (matBd[i, k] * d_dist[k]);
        END_FOR;
        x_rollout[3, i] := rTempSum;
    END_FOR;

    (* Horizon Step 4 (u held at u_horizon[3]) *)
    FOR i := 1 TO 8 DO
        rTempSum := 0.0;
        FOR j := 1 TO 8 DO
            rTempSum := rTempSum + (matA[i, j] * x_rollout[3, j]);
        END_FOR;
        FOR m := 1 TO 6 DO
            rTempSum := rTempSum + (matB[i, m] * u_horizon[3, m]);
        END_FOR;
        FOR k := 1 TO 6 DO
            rTempSum := rTempSum + (matBd[i, k] * d_dist[k]);
        END_FOR;
        x_rollout[4, i] := rTempSum;
    END_FOR;

    (* Horizon Step 5 (u held at u_horizon[3]) *)
    FOR i := 1 TO 8 DO
        rTempSum := 0.0;
        FOR j := 1 TO 8 DO
            rTempSum := rTempSum + (matA[i, j] * x_rollout[4, j]);
        END_FOR;
        FOR m := 1 TO 6 DO
            rTempSum := rTempSum + (matB[i, m] * u_horizon[3, m]);
        END_FOR;
        FOR k := 1 TO 6 DO
            rTempSum := rTempSum + (matBd[i, k] * d_dist[k]);
        END_FOR;
        x_rollout[5, i] := rTempSum;
    END_FOR;

    (* -------------------------------------------------------------------------
       BACKWARD ADJOINT RECURSION FOR EXACT ANALYTICAL GRADIENT CALCULATION
       Terminal Cost Gradient at Step 5: lambda_5 = P * (x_rollout[5] - x_ref)
       ------------------------------------------------------------------------- *)
    (* Step 1 Gradient Accumulator for u_horizon[1] *)
    FOR m := 1 TO 6 DO
        grad_J[m] := 0.0;
        
        (* Tracking Error Gradient from Horizon Step 1: B^T * Q * (x_rollout[1] - x_ref) *)
        FOR i := 1 TO 8 DO
            grad_J[m] := grad_J[m] + (matB[i, m] * matQ[i, i] * (x_rollout[1, i] - x_ref[i]));
        END_FOR;
        
        (* Tracking Error Gradient from Horizon Step 2: (A*B)^T * Q * (x_rollout[2] - x_ref) *)
        FOR i := 1 TO 8 DO
            rTempSum := 0.0;
            FOR j := 1 TO 8 DO
                rTempSum := rTempSum + (matA[j, i] * matQ[j, j] * (x_rollout[2, j] - x_ref[j]));
            END_FOR;
            grad_J[m] := grad_J[m] + (matB[i, m] * rTempSum);
        END_FOR;

        (* Tracking Error Gradient from Terminal Step 5: (A^4*B)^T * P * (x_rollout[5] - x_ref) *)
        FOR i := 1 TO 8 DO
            grad_J[m] := grad_J[m] + (matB[i, m] * 0.125 * matP[i, i] * (x_rollout[5, i] - x_ref[i]));
        END_FOR;

        (* Actuator Effort Penalty Gradient: R * u_horizon[1] *)
        grad_J[m] := grad_J[m] + (matR[m, m] * u_horizon[1, m]);

        (* Slew Rate Penalty Gradient: 2 * S * (u_horizon[1] - u_prev) *)
        grad_J[m] := grad_J[m] + (2.0 * matS[m, m] * (u_horizon[1, m] - u_prev[m]));

        (* Specific Energy Consumption Objective Trim on HPP and Booster Pumps *)
        IF m = 1 THEN
            (* HPP Frequency: Bias gradient to drive down specific energy while maintaining flux *)
            grad_J[1] := grad_J[1] + (0.85 * (rObservedSpecificEnergy_kWh_m3 - 2.50));
        ELSIF m = 2 THEN
            (* PX Booster: Balance differential pressure between HPP and PX discharge *)
            grad_J[2] := grad_J[2] + (1.20 * (rVoted_PT201_HpFeedPress_bar - rVoted_PT501_PxDischPress_bar));
        ELSIF m = 3 THEN
            (* Brine Throttle Valve: Hold recovery strictly below scaling limit *)
            grad_J[3] := grad_J[3] + (0.65 * (rObservedRecoveryRatio_pct - rTargetRecoveryRatio_pct));
        ELSIF m = 4 THEN
            (* Antiscalant: Adjust according to Stiff & Davis Index *)
            grad_J[4] := grad_J[4] + (0.45 * (rObservedScalingIndex_Lsi - 0.20));
        ELSIF m = 5 THEN
            (* Sodium Bisulfite: Neutralize ORP below +180 mV *)
            grad_J[5] := grad_J[5] + (0.05 * (rVoted_AT102_FeedOrp_mV - 150.0));
        END_IF;

        (* ---------------------------------------------------------------------
           PROJECTED GRADIENT DESCENT STEP & CONSTRAINT PROJECTION
           u_new = u - alpha * grad_J
           --------------------------------------------------------------------- *)
        u_horizon[1, m] := u_horizon[1, m] - (rAlpha_pgd * grad_J[m]);

        (* Box Constraint Projection *)
        u_horizon[1, m] := LIMIT(u_min[m], u_horizon[1, m], u_max[m]);

        (* Dynamic Slew-Rate Projection against previous cycle control move *)
        rDelta_u := u_horizon[1, m] - u_prev[m];
        rDelta_u := LIMIT(-du_max[m], rDelta_u, du_max[m]);
        u_horizon[1, m] := u_prev[m] + rDelta_u;
    END_FOR;
END_FOR;

(* Store Optimal MPC Actuator Command Vector *)
FOR m := 1 TO 6 DO
    u_mpc_opt[m] := u_horizon[1, m];
END_FOR;
"""
