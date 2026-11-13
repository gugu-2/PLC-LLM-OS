# -*- coding: utf-8 -*-
"""
Module: retort_builder/mod_mpc.py
Implements Phase 3: Receding-Horizon Decoupled Model Predictive Control (MPC)
with Unrolled Projected Gradient Descent (PGD), Temperature/Pressure Decoupling,
Steam Collapse Feedforward Compensation, and Actuator Slew Rate Clamping.
"""

def generate_mpc():
    return '''(* =====================================================================================================================
 * PHASE 3: RECEDING-HORIZON DECOUPLED MPC OPTIMIZER WITH PROJECTED GRADIENT DESCENT (PGD)
 * Optimization Objective:
 *   Minimize Multivariable Quadratic Tracking Cost:
 *     J = SUM_k=1..N [ e_k^T * Q * e_k + u_k^T * R * u_k + Delta_u_k^T * S * Delta_u_k ] + e_N^T * P * e_N
 *   Subject to:
 *     x[k+1] = A * x[k] + B * u[k]
 *     u_min <= u[k] <= u_max
 *     |u[k] - u[k-1]| <= SlewLimit * Ts
 * Cyber-Physical Decoupling:
 *   Simultaneous independent governing of Retort Temperature Tv and Retort Absolute Pressure Pv
 *   to maintain container wall differential stress DeltaP within safe structural boundary [-0.10..+0.15 bar].
 * ===================================================================================================================== *)

(* -------------------------------------------------------------------------
 * SUB-SECTION 3.1: DYNAMIC MPC STATE REFERENCE VECTOR x_ref FORMULATION
 * Dynamic trajectory synthesis driven by active FSM stage requirements
 * ------------------------------------------------------------------------- *)
CASE iFSM_CurrentState OF
    0: (* STATE_IDLE_STANDBY *)
        rX_Reference[1] := 25.0;  (* Tv idle ambient [deg C] *)
        rX_Reference[2] := 1.013; (* Pv atmospheric [bar] *)
        rX_Reference[3] := 25.0;  (* Tcore ambient [deg C] *)
        rX_Reference[4] := 1.013; (* Pcan ambient [bar] *)
        rX_Reference[5] := 0.000; (* DeltaP zero stress [bar] *)
        rX_Reference[6] := 0.000; (* Zero lethality rate *)
        rX_Reference[7] := 0.000; (* Cumulative F0 *)
        rX_Reference[8] := 0.000; (* Sump dry *)

    1: (* STATE_DOOR_LOCK_SEAL_INFLATION *)
        rX_Reference[1] := 25.0;
        rX_Reference[2] := 1.013;
        rX_Reference[3] := 25.0;
        rX_Reference[4] := 1.013;
        rX_Reference[5] := 0.000;
        rX_Reference[6] := 0.000;
        rX_Reference[7] := 0.000;
        rX_Reference[8] := 0.000;

    2: (* STATE_AIR_VENT_PURGE *)
        rX_Reference[1] := 100.5; (* Tv atmospheric boiling sweep [deg C] *)
        rX_Reference[2] := 1.050; (* Pv slightly positive for air purge [bar] *)
        rX_Reference[3] := 30.0;
        rX_Reference[4] := 1.050;
        rX_Reference[5] := 0.000;
        rX_Reference[6] := 0.000;
        rX_Reference[7] := 0.000;
        rX_Reference[8] := 15.0;  (* Condensate accumulation *)

    3: (* STATE_STEAM_COME_UP_RAMP *)
        (* Linear ramp generation up to scheduled sterilization cook temperature *)
        rTempCalc1 := 100.0 + (rSet_ComeUpRampRate_degCpm * (rFSM_StateTimer_s / 60.0));
        IF rTempCalc1 > rSet_TargetCookTemp_degC THEN
            rTempCalc1 := rSet_TargetCookTemp_degC;
        END_IF;
        rX_Reference[1] := rTempCalc1;
        (* Pressure trajectory tracking steam saturation plus linear air overpressure cushion *)
        rX_Reference[2] := rAntoine_Pv_sat_bar + 0.350;
        rX_Reference[3] := rTempCalc1 * 0.75;
        rX_Reference[4] := rTotalEstimatedPcan_bar;
        rX_Reference[5] := 0.020; (* Nominal positive cushion *)
        rX_Reference[6] := 0.000;
        rX_Reference[7] := rIntegratedF0;
        rX_Reference[8] := 35.0;

    4, 5, 6: (* TEMPERATURE_CUT_IN, STERILIZATION_HOLD, BALL_DEVIATION_CATCHUP *)
        rX_Reference[1] := rSet_TargetCookTemp_degC;
        rX_Reference[2] := rSet_TargetOverpressure_bar;
        rX_Reference[3] := rSet_TargetCookTemp_degC;
        rX_Reference[4] := rTotalEstimatedPcan_bar;
        rX_Reference[5] := 0.000; (* Strict zero wall deflection stress *)
        rX_Reference[6] := EXP(((rSet_TargetCookTemp_degC - rRefSterilTemp_degC) / rSet_Ball_z_degC) * 2.302585);
        rX_Reference[7] := rSet_TargetF0_min;
        rX_Reference[8] := 45.0;

    7: (* STATE_PRE_COOLING_AIR_EQUALIZATION *)
        rX_Reference[1] := rSet_TargetCookTemp_degC;
        (* Pre-charge vessel with additional overpressure air before cold water inrush *)
        rX_Reference[2] := rSet_TargetOverpressure_bar + rSet_PreCoolAirCushion_bar;
        rX_Reference[3] := rSet_TargetCookTemp_degC;
        rX_Reference[4] := rTotalEstimatedPcan_bar;
        rX_Reference[5] := -0.050; (* Safe compressive cushion *)
        rX_Reference[6] := rInstantLethality;
        rX_Reference[7] := rIntegratedF0;
        rX_Reference[8] := 50.0;

    8, 9: (* CASCADE_COOLING & RECIRCULATION_EVAP_COOLING *)
        (* Linear downward cooling trajectory towards safe handling temperature *)
        rTempCalc1 := rSet_TargetCookTemp_degC - (3.50 * (rFSM_StateTimer_s / 60.0));
        IF rTempCalc1 < rSet_TargetCoolingTemp_degC THEN
            rTempCalc1 := rSet_TargetCoolingTemp_degC;
        END_IF;
        rX_Reference[1] := rTempCalc1;
        (* Dynamic overpressure tracking to counter water condensation collapse *)
        rX_Reference[2] := rAntoine_Pcan_sat_bar + 0.400;
        rX_Reference[3] := rTempCalc1 + 5.0;
        rX_Reference[4] := rTotalEstimatedPcan_bar;
        rX_Reference[5] := 0.000;
        rX_Reference[6] := 0.000;
        rX_Reference[7] := rIntegratedF0;
        rX_Reference[8] := 250.0; (* Full cooling water sump *)

    10: (* STATE_OVERPRESSURE_WATER_DRAIN *)
        rX_Reference[1] := rSet_TargetCoolingTemp_degC;
        rX_Reference[2] := 1.450; (* Maintain air cushion while draining sump *)
        rX_Reference[3] := rSet_TargetCoolingTemp_degC;
        rX_Reference[4] := 1.150;
        rX_Reference[5] := 0.000;
        rX_Reference[6] := 0.000;
        rX_Reference[7] := rIntegratedF0;
        rX_Reference[8] := 0.000; (* Target empty sump *)

    11, 12: (* VACUUM_BREAK & SEAL_DEFLATE *)
        rX_Reference[1] := rSet_TargetCoolingTemp_degC;
        rX_Reference[2] := 1.013; (* Vent to atmospheric datum *)
        rX_Reference[3] := rSet_TargetCoolingTemp_degC;
        rX_Reference[4] := 1.013;
        rX_Reference[5] := 0.000;
        rX_Reference[6] := 0.000;
        rX_Reference[7] := rIntegratedF0;
        rX_Reference[8] := 0.000;

    13: (* STATE_CIP_SIP_SANITATION *)
        rX_Reference[1] := 85.0;  (* Caustic wash temperature *)
        rX_Reference[2] := 1.300;
        rX_Reference[3] := 85.0;
        rX_Reference[4] := 1.013;
        rX_Reference[5] := 0.000;
        rX_Reference[6] := 0.000;
        rX_Reference[7] := 0.000;
        rX_Reference[8] := 120.0;

    14: (* STATE_EMERGENCY_SAFETY_ABORT *)
        rX_Reference[1] := 25.0;
        rX_Reference[2] := 1.013;
        rX_Reference[3] := 25.0;
        rX_Reference[4] := 1.013;
        rX_Reference[5] := 0.000;
        rX_Reference[6] := 0.000;
        rX_Reference[7] := rIntegratedF0;
        rX_Reference[8] := 0.000;
ELSE
    rX_Reference[1] := 25.0;
    rX_Reference[2] := 1.013;
END_CASE;

(* -------------------------------------------------------------------------
 * SUB-SECTION 3.2: RECEDING-HORIZON PGD OPTIMIZATION (HORIZON N = 5)
 * Unrolled 3 Iterative Gradient Descent Sweeps Across Horizon
 * ------------------------------------------------------------------------- *)
(* Initialize candidate control inputs with prior optimal solution *)
FOR iIdx1 := 1 TO 5 DO
    FOR iIdx2 := 1 TO 5 DO
        rMPC_CandInputs[iIdx1, iIdx2] := rU_ControlPrev[iIdx2];
    END_FOR;
END_FOR;

(* Begin PGD Optimization Loop (3 Unrolled Gradient Descent Iterations) *)
FOR iIdx4 := 1 TO 3 DO
    (* Step 1: Forward State Propagation across Horizon N=1..5 *)
    FOR iIdx1 := 1 TO 5 DO
        FOR iIdx2 := 1 TO 8 DO
            rTempSum := 0.0;
            (* State feedback from previous horizon step or initial state *)
            FOR iIdx3 := 1 TO 8 DO
                IF iIdx1 = 1 THEN
                    rTempSum := rTempSum + (rA[iIdx2, iIdx3] * rX_State[iIdx3]);
                ELSE
                    rTempSum := rTempSum + (rA[iIdx2, iIdx3] * rMPC_PredStates[iIdx1 - 1, iIdx3]);
                END_IF;
            END_FOR;
            (* Control input contribution *)
            FOR iIdx3 := 1 TO 5 DO
                rTempSum := rTempSum + (rB[iIdx2, iIdx3] * rMPC_CandInputs[iIdx1, iIdx3]);
            END_FOR;
            rMPC_PredStates[iIdx1, iIdx2] := rTempSum;
        END_FOR;
    END_FOR;

    (* Step 2: Backward Cost Gradient Formulation dJ/du[k, m] *)
    FOR iIdx1 := 1 TO 5 DO
        FOR iIdx2 := 1 TO 5 DO
            rTempSum := 0.0;
            (* Tracking error gradient: 2 * SUM_j (Q[j] * e[k, j] * B[j, m]) *)
            FOR iIdx3 := 1 TO 8 DO
                rTempCalc1 := rMPC_PredStates[iIdx1, iIdx3] - rX_Reference[iIdx3];
                IF iIdx1 = 5 THEN
                    (* Terminal horizon step incorporates terminal penalty P *)
                    rTempSum := rTempSum + (2.0 * (rQ_Weights[iIdx3] + rP_TerminalWeights[iIdx3]) * rTempCalc1 * rB[iIdx3, iIdx2]);
                ELSE
                    rTempSum := rTempSum + (2.0 * rQ_Weights[iIdx3] * rTempCalc1 * rB[iIdx3, iIdx2]);
                END_IF;
            END_FOR;

            (* Actuator effort gradient: 2 * R[m] * u[k, m] *)
            rTempSum := rTempSum + (2.0 * rR_Weights[iIdx2] * rMPC_CandInputs[iIdx1, iIdx2]);

            (* Slew rate penalty gradient: 2 * S[m] * (u[k, m] - u[k-1, m]) *)
            IF iIdx1 = 1 THEN
                rTempCalc2 := rMPC_CandInputs[1, iIdx2] - rU_ControlPrev[iIdx2];
            ELSE
                rTempCalc2 := rMPC_CandInputs[iIdx1, iIdx2] - rMPC_CandInputs[iIdx1 - 1, iIdx2];
            END_IF;
            rTempSum := rTempSum + (2.0 * rS_Weights[iIdx2] * rTempCalc2);

            rMPC_Gradients[iIdx1, iIdx2] := rTempSum;
        END_FOR;
    END_FOR;

    (* Step 3: Gradient Descent Step & Projection Onto Box Constraints *)
    FOR iIdx1 := 1 TO 5 DO
        FOR iIdx2 := 1 TO 5 DO
            rMPC_CandInputs[iIdx1, iIdx2] := rMPC_CandInputs[iIdx1, iIdx2] - (rMPC_StepSize_alpha * rMPC_Gradients[iIdx1, iIdx2]);
            (* Box Projection *)
            IF rMPC_CandInputs[iIdx1, iIdx2] < rU_LowerBound_pct[iIdx2] THEN
                rMPC_CandInputs[iIdx1, iIdx2] := rU_LowerBound_pct[iIdx2];
            ELSIF rMPC_CandInputs[iIdx1, iIdx2] > rU_UpperBound_pct[iIdx2] THEN
                rMPC_CandInputs[iIdx1, iIdx2] := rU_UpperBound_pct[iIdx2];
            END_IF;
        END_FOR;
    END_FOR;
END_FOR;

(* -------------------------------------------------------------------------
 * SUB-SECTION 3.3: CYBER-PHYSICAL DECOUPLING & FEEDFORWARD ADJUSTMENT
 * ------------------------------------------------------------------------- *)
(* Steam to Air Decoupling: When steam valve opens, inject slight air trim to counter condensation lag *)
IF rMPC_CandInputs[1, 1] > 20.0 THEN
    rMPC_CandInputs[1, 2] := rMPC_CandInputs[1, 2] + (rMPC_CandInputs[1, 1] * 0.05);
END_IF;

(* Steam Collapse Feedforward: When cooling water valve opens, inject rapid air inrush to prevent pouch crush *)
IF rMPC_CandInputs[1, 3] > 10.0 THEN
    rMPC_CandInputs[1, 2] := rMPC_CandInputs[1, 2] + (rMPC_CandInputs[1, 3] * rDecouple_CoolToAirRate);
    IF rMPC_CandInputs[1, 2] > 100.0 THEN
        rMPC_CandInputs[1, 2] := 100.0;
    END_IF;
END_IF;

(* -------------------------------------------------------------------------
 * SUB-SECTION 3.4: SLEW RATE LIMITING & FINAL ACTUATOR CLAMPING
 * First Horizon Step u_opt = rMPC_CandInputs[1, :]
 * ------------------------------------------------------------------------- *)
FOR iIdx1 := 1 TO 5 DO
    rTempCalc1 := rMPC_CandInputs[1, iIdx1] - rU_ControlPrev[iIdx1];
    rTempCalc2 := rU_SlewLimit_pct_per_s[iIdx1] * rTs_s;

    IF rTempCalc1 > rTempCalc2 THEN
        rMPC_OptimizedU[iIdx1] := rU_ControlPrev[iIdx1] + rTempCalc2;
    ELSIF rTempCalc1 < -rTempCalc2 THEN
        rMPC_OptimizedU[iIdx1] := rU_ControlPrev[iIdx1] - rTempCalc2;
    ELSE
        rMPC_OptimizedU[iIdx1] := rMPC_CandInputs[1, iIdx1];
    END_IF;

    (* Final boundary saturation clamp *)
    IF rMPC_OptimizedU[iIdx1] < rU_LowerBound_pct[iIdx1] THEN
        rMPC_OptimizedU[iIdx1] := rU_LowerBound_pct[iIdx1];
    ELSIF rMPC_OptimizedU[iIdx1] > rU_UpperBound_pct[iIdx1] THEN
        rMPC_OptimizedU[iIdx1] := rU_UpperBound_pct[iIdx1];
    END_IF;
END_FOR;
'''

if __name__ == "__main__":
    mp = generate_mpc()
    print("MPC length:", len(mp))
    print(mp[:300])
