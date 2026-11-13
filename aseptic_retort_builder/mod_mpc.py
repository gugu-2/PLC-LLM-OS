# -*- coding: utf-8 -*-
"""
Module: aseptic_retort_builder/mod_mpc.py
Implements Phase 3: Receding-Horizon Decoupled Model Predictive Control (MPC)
with 10-Iteration Unrolled Projected Gradient Descent (PGD), Dynamic Reference Trajectory,
and Active Container Differential Stress Regulation (|Delta_P| < 0.12 bar).
"""

def generate_mpc():
    return '''(* =====================================================================================================================
 * PHASE 3: RECEDING-HORIZON DECOUPLED MPC OPTIMIZER WITH 10-ITERATION PROJECTED GRADIENT DESCENT (PGD)
 * Optimization Horizon: N = 5 steps (500 ms lookahead at Ts = 100 ms)
 * Numerical Algorithm: Unrolled 10-Iteration Projected Gradient Descent (PGD)
 * Mathematical Formulation:
 *   Minimize Quadratic Cost:
 *     J = SUM_h=1..N [ (x_h - x_ref)^T * Q * (x_h - x_ref) + u_h^T * R * u_h + (u_h - u_h-1)^T * S * (u_h - u_h-1) ]
 *         + (x_N - x_ref)^T * P * (x_N - x_ref) + J_stress(Delta_P)
 *   Subject to:
 *     x_h+1 = A * x_h + B * u_h
 *     rMPC_Umin[m] <= u_h,m <= rMPC_Umax[m]
 *     |u_h,m - u_h-1,m| <= rMPC_DeltaUmax[m] * Ts
 * Cyber-Physical Decoupling:
 *   Independently governs Saturated Steam Modulating Valve [%], Compressed Air Overpressure Valve [%],
 *   Top Exhaust Vent Valve [%], Cascade Cooling Water Spray [%], and Rotary Drum Speed [RPM]
 *   to tightly control temperature while maintaining net container stress |Delta_P| < 0.12 bar.
 * ===================================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------------------------
 * SUB-SECTION 3.1: DYNAMIC MPC STATE REFERENCE TRAJECTORY (x_ref) SYNTHESIS
 * Reference trajectories synthesized dynamically based on active 14-Stage FSM status.
 * States: x1=T_retort, x2=T_core, x3=P_retort, x4=P_internal, x5=F0, x6=C0
 * --------------------------------------------------------------------------------------------------------------------- *)
CASE iFSM_CurrentState OF
    cSTATE_IDLE: (* State 0: Idle & Standby *)
        rX_Reference[1] := 22.5;  (* Ambient room temperature [deg C] *)
        rX_Reference[2] := 20.0;  (* Product core ambient [deg C] *)
        rX_Reference[3] := 1.013; (* Atmospheric sea level datum [bar] *)
        rX_Reference[4] := 1.013; (* Container internal ambient [bar] *)
        rX_Reference[5] := 0.000; (* Zero initial lethality *)
        rX_Reference[6] := 0.000; (* Zero initial cook value *)

    cSTATE_CHAMBER_LOAD_AND_SAFETY_DOOR_INTERLOCK_LOCK: (* State 1: Chamber Loading & Door Lock *)
        rX_Reference[1] := 25.0;
        rX_Reference[2] := 20.0;
        rX_Reference[3] := 1.013;
        rX_Reference[4] := 1.013;
        rX_Reference[5] := 0.000;
        rX_Reference[6] := 0.000;

    cSTATE_VENTING_AIR_DISPLACEMENT_STEAM_PURGE: (* State 2: Venting Air Purge at Atmospheric Boiling *)
        rX_Reference[1] := 100.8; (* Atmospheric pure steam displacement sweep [deg C] *)
        rX_Reference[2] := 35.0;  (* Initial product warming [deg C] *)
        rX_Reference[3] := 1.060; (* Slight positive purge backpressure to exhaust air [bar] *)
        rX_Reference[4] := 1.050;
        rX_Reference[5] := 0.000;
        rX_Reference[6] := 0.000;

    cSTATE_COME_UP_HEATING_RAMP_TO_121C: (* State 3: Thermal Come-Up Heating Ramp *)
        (* Linear heating ramp calculation based on elapsed state timer *)
        rTempCalc1 := 100.0 + (rSet_ComeUpRampRate_degCpm * (rFSM_StateTimer_s / 60.0));
        IF rTempCalc1 > rSet_SterilizationTemp_degC THEN
            rTempCalc1 := rSet_SterilizationTemp_degC;
        END_IF;
        rX_Reference[1] := rTempCalc1;
        rX_Reference[2] := rTempCalc1 * 0.85; (* Product core thermal lag trajectory *)
        (* Dynamic counter-pressure reference: steam saturation + air cushion *)
        rX_Reference[3] := rAntoine_Pv_sat_bar + 0.450;
        rX_Reference[4] := rTotalEstimatedPcan_bar;
        rX_Reference[5] := 0.000;
        rX_Reference[6] := 0.000;

    cSTATE_STEAM_AIR_OVERPRESSURE_EQUILIBRIUM_LOCK: (* State 4: Steam-Air Equilibrium Lock *)
        rX_Reference[1] := rSet_SterilizationTemp_degC;
        rX_Reference[2] := rSet_SterilizationTemp_degC - 0.50;
        rX_Reference[3] := rSet_RetortOverpressure_bar;
        rX_Reference[4] := rTotalEstimatedPcan_bar;
        rX_Reference[5] := 0.000;
        rX_Reference[6] := 0.000;

    cSTATE_NOMINAL_STERILIZATION_HOLD_LETHALITY_ACCUM: (* State 5: Nominal Sterilization Hold *)
        rX_Reference[1] := rSet_SterilizationTemp_degC;
        rX_Reference[2] := rSet_SterilizationTemp_degC;
        rX_Reference[3] := rSet_RetortOverpressure_bar;
        rX_Reference[4] := rTotalEstimatedPcan_bar;
        rX_Reference[5] := rSet_TargetF0_min; (* Target lethality tracking *)
        rX_Reference[6] := 15.0;             (* Target cook value benchmark *)

    cSTATE_TARGET_F0_REACHED_HEATING_CUTOFF: (* State 6: Lethality Target Reached, Steam Cutoff *)
        rX_Reference[1] := rSet_SterilizationTemp_degC - 1.0;
        rX_Reference[2] := rSet_SterilizationTemp_degC;
        rX_Reference[3] := rSet_RetortOverpressure_bar; (* Maintain absolute overpressure to lock stress *)
        rX_Reference[4] := rTotalEstimatedPcan_bar;
        rX_Reference[5] := rIntegratedF0_min;
        rX_Reference[6] := rIntegratedC0_min;

    cSTATE_PRESSURE_MAINTAINED_PRE_COOL_WATER_INJECTION: (* State 7: Pre-Cool Water Injection *)
        rX_Reference[1] := 95.0;  (* Controlled drop below boiling [deg C] *)
        rX_Reference[2] := 115.0; (* Internal food still retains thermal core heat *)
        rX_Reference[3] := rSet_RetortOverpressure_bar; (* Critical: prevent can burst during steam collapse *)
        rX_Reference[4] := rTotalEstimatedPcan_bar;
        rX_Reference[5] := rIntegratedF0_min;
        rX_Reference[6] := rIntegratedC0_min;

    cSTATE_FULL_IMMERSION_TEMPERED_COOLING_CASCADE: (* State 8: Tempered Cooling Cascade *)
        rX_Reference[1] := 68.0;  (* Tempered spray zone [deg C] *)
        rX_Reference[2] := 80.0;
        (* Ramp overpressure down proportional to internal can pressure collapse *)
        rX_Reference[3] := rTotalEstimatedPcan_bar + 0.050;
        rX_Reference[4] := rTotalEstimatedPcan_bar;
        rX_Reference[5] := rIntegratedF0_min;
        rX_Reference[6] := rIntegratedC0_min;

    cSTATE_FINAL_COLD_WATER_CHILLDOWN_TO_40C: (* State 9: Final Cold Water Chilldown *)
        rX_Reference[1] := rSet_TargetCoolingTemp_degC; (* 40.0 deg C *)
        rX_Reference[2] := rSet_TargetCoolingTemp_degC + 2.0;
        rX_Reference[3] := 1.250; (* Moderate residual cushion *)
        rX_Reference[4] := 1.150;
        rX_Reference[5] := rIntegratedF0_min;
        rX_Reference[6] := rIntegratedC0_min;

    cSTATE_CONTROLLED_DEPRESSURIZATION_AND_DRAIN: (* State 10: Controlled Depressurization & Drain *)
        rX_Reference[1] := 38.0;
        rX_Reference[2] := 40.0;
        rX_Reference[3] := 1.050; (* Controlled atmospheric return *)
        rX_Reference[4] := 1.050;
        rX_Reference[5] := rIntegratedF0_min;
        rX_Reference[6] := rIntegratedC0_min;

    cSTATE_SAFETY_AIR_VENT_AND_DOOR_UNLATCH: (* State 11: Safety Air Vent & Door Unlatch *)
        rX_Reference[1] := 32.0;
        rX_Reference[2] := 38.0;
        rX_Reference[3] := 1.013; (* Complete atmospheric equilibrium *)
        rX_Reference[4] := 1.013;
        rX_Reference[5] := rIntegratedF0_min;
        rX_Reference[6] := rIntegratedC0_min;

    cSTATE_STERILE_CONTAINER_DISCHARGE_CONVEYOR_RUN: (* State 12: Continuous Product Discharge *)
        rX_Reference[1] := 30.0;
        rX_Reference[2] := 35.0;
        rX_Reference[3] := 1.013;
        rX_Reference[4] := 1.013;
        rX_Reference[5] := rIntegratedF0_min;
        rX_Reference[6] := rIntegratedC0_min;

    cSTATE_EMERGENCY_OVERPRESSURE_OR_UNDERPROCESSING_TRIP: (* State 13: Emergency Trip *)
        rX_Reference[1] := 25.0;
        rX_Reference[2] := 25.0;
        rX_Reference[3] := 1.013;
        rX_Reference[4] := 1.013;
        rX_Reference[5] := rIntegratedF0_min;
        rX_Reference[6] := rIntegratedC0_min;
ELSE
    rX_Reference[1] := 22.5;
    rX_Reference[2] := 20.0;
    rX_Reference[3] := 1.013;
    rX_Reference[4] := 1.013;
    rX_Reference[5] := 0.000;
    rX_Reference[6] := 0.000;
END_CASE;

(* ---------------------------------------------------------------------------------------------------------------------
 * SUB-SECTION 3.2: UNROLLED 10-ITERATION PROJECTED GRADIENT DESCENT (PGD) OPTIMIZER
 * Horizon Length N = 5 steps. Unrolled 10 full forward-backward iterative sweeps.
 * --------------------------------------------------------------------------------------------------------------------- *)
(* Initialize candidate control trajectory across horizon with previous optimal control *)
FOR iIdx1 := 1 TO 5 DO
    FOR iIdx2 := 1 TO 5 DO
        rMPC_CandInputs[iIdx1, iIdx2] := rU_ControlPrev[iIdx2];
    END_FOR;
END_FOR;

(* Optimization Iteration Loop: Unrolled 10 PGD Iterations *)
FOR iIdx4 := 1 TO 10 DO
    (* -------------------------------------------------------------------------
     * STEP 1: FORWARD TRAJECTORY PROPAGATION ACROSS HORIZON h = 1..5
     * ------------------------------------------------------------------------- *)
    FOR iIdx1 := 1 TO 5 DO
        FOR iIdx2 := 1 TO 6 DO
            rTempSum := 0.0;
            (* State transition contribution: SUM_j (A[i, j] * x_prev[j]) *)
            FOR iIdx3 := 1 TO 6 DO
                IF iIdx1 = 1 THEN
                    rTempSum := rTempSum + (rA[iIdx2, iIdx3] * rX_State[iIdx3]);
                ELSE
                    rTempSum := rTempSum + (rA[iIdx2, iIdx3] * rMPC_PredStates[iIdx1 - 1, iIdx3]);
                END_IF;
            END_FOR;
            (* Actuator coupling contribution: SUM_m (B[i, m] * u_cand[h, m]) *)
            FOR iIdx3 := 1 TO 5 DO
                rTempSum := rTempSum + (rB[iIdx2, iIdx3] * rMPC_CandInputs[iIdx1, iIdx3]);
            END_FOR;
            rMPC_PredStates[iIdx1, iIdx2] := rTempSum;
        END_FOR;
    END_FOR;

    (* -------------------------------------------------------------------------
     * STEP 2: BACKWARD COST GRADIENT EVALUATION dJ/du[h, m]
     * ------------------------------------------------------------------------- *)
    FOR iIdx1 := 1 TO 5 DO
        FOR iIdx2 := 1 TO 5 DO
            rTempSum := 0.0;

            (* 1. Tracking Error Gradient: 2 * SUM_j (Q[j] * (x[h, j] - xref[j]) * B[j, m]) *)
            FOR iIdx3 := 1 TO 6 DO
                rTempCalc1 := rMPC_PredStates[iIdx1, iIdx3] - rX_Reference[iIdx3];
                IF iIdx1 = 5 THEN
                    (* Terminal horizon step adds terminal penalty P[j] *)
                    rTempSum := rTempSum + (2.0 * (rQ_Weights[iIdx3] + rP_TerminalWeights[iIdx3]) * rTempCalc1 * rB[iIdx3, iIdx2]);
                ELSE
                    rTempSum := rTempSum + (2.0 * rQ_Weights[iIdx3] * rTempCalc1 * rB[iIdx3, iIdx2]);
                END_IF;
            END_FOR;

            (* 2. Actuator Effort Penalty Gradient: 2 * R[m] * u[h, m] *)
            rTempSum := rTempSum + (2.0 * rR_Weights[iIdx2] * rMPC_CandInputs[iIdx1, iIdx2]);

            (* 3. Actuator Slew Rate Gradient: 2 * S[m] * (u[h, m] - u[h-1, m]) *)
            IF iIdx1 = 1 THEN
                rTempCalc2 := rMPC_CandInputs[1, iIdx2] - rU_ControlPrev[iIdx2];
            ELSE
                rTempCalc2 := rMPC_CandInputs[iIdx1, iIdx2] - rMPC_CandInputs[iIdx1 - 1, iIdx2];
            END_IF;
            rTempSum := rTempSum + (2.0 * rS_Weights[iIdx2] * rTempCalc2);

            (* 4. Active Container Wall Stress Penalty: DeltaP = Pcan - Pretort = x4 - x3 *)
            rTempCalc3 := rMPC_PredStates[iIdx1, 4] - rMPC_PredStates[iIdx1, 3];
            IF rTempCalc3 > 0.080 THEN
                (* Positive differential exceeds safe pouch limit: penalize steam, boost overpressure air *)
                rTempSum := rTempSum + (500.0 * (rTempCalc3 - 0.080) * (rB[4, iIdx2] - rB[3, iIdx2]));
            ELSIF rTempCalc3 < -0.080 THEN
                (* Negative differential threatens can buckling: penalize air, boost vent *)
                rTempSum := rTempSum + (500.0 * (rTempCalc3 + 0.080) * (rB[4, iIdx2] - rB[3, iIdx2]));
            END_IF;

            rMPC_Gradients[iIdx1, iIdx2] := rTempSum;
        END_FOR;
    END_FOR;

    (* -------------------------------------------------------------------------
     * STEP 3: GRADIENT DESCENT UPDATE & PROJECTION ONTO CONSTRAINTS
     * ------------------------------------------------------------------------- *)
    FOR iIdx1 := 1 TO 5 DO
        FOR iIdx2 := 1 TO 5 DO
            (* Gradient Descent Step: u = u - alpha * grad *)
            rMPC_CandInputs[iIdx1, iIdx2] := rMPC_CandInputs[iIdx1, iIdx2] - (rMPC_AlphaStep * rMPC_Gradients[iIdx1, iIdx2]);

            (* Box Constraint Projection: Lower and Upper Bounds [Umin, Umax] *)
            IF rMPC_CandInputs[iIdx1, iIdx2] < rMPC_Umin[iIdx2] THEN
                rMPC_CandInputs[iIdx1, iIdx2] := rMPC_Umin[iIdx2];
            ELSIF rMPC_CandInputs[iIdx1, iIdx2] > rMPC_Umax[iIdx2] THEN
                rMPC_CandInputs[iIdx1, iIdx2] := rMPC_Umax[iIdx2];
            END_IF;

            (* Slew Rate Constraint Clamping across horizon *)
            IF iIdx1 = 1 THEN
                rTempCalc1 := rMPC_DeltaUmax[iIdx2] * rTs_s;
                IF (rMPC_CandInputs[1, iIdx2] - rU_ControlPrev[iIdx2]) > rTempCalc1 THEN
                    rMPC_CandInputs[1, iIdx2] := rU_ControlPrev[iIdx2] + rTempCalc1;
                ELSIF (rMPC_CandInputs[1, iIdx2] - rU_ControlPrev[iIdx2]) < -rTempCalc1 THEN
                    rMPC_CandInputs[1, iIdx2] := rU_ControlPrev[iIdx2] - rTempCalc1;
                END_IF;
            ELSE
                rTempCalc1 := rMPC_DeltaUmax[iIdx2] * rTs_s;
                IF (rMPC_CandInputs[iIdx1, iIdx2] - rMPC_CandInputs[iIdx1 - 1, iIdx2]) > rTempCalc1 THEN
                    rMPC_CandInputs[iIdx1, iIdx2] := rMPC_CandInputs[iIdx1 - 1, iIdx2] + rTempCalc1;
                ELSIF (rMPC_CandInputs[iIdx1, iIdx2] - rMPC_CandInputs[iIdx1 - 1, iIdx2]) < -rTempCalc1 THEN
                    rMPC_CandInputs[iIdx1, iIdx2] := rMPC_CandInputs[iIdx1 - 1, iIdx2] - rTempCalc1;
                END_IF;
            END_IF;
        END_FOR;
    END_FOR;
END_FOR;

(* ---------------------------------------------------------------------------------------------------------------------
 * SUB-SECTION 3.3: OPTIMAL CONTROL EXTRACTION & ACTUATOR COMMAND APPLICATION
 * Extract step 1 candidate input vector as optimal output u*[k]
 * --------------------------------------------------------------------------------------------------------------------- *)
FOR iIdx1 := 1 TO 5 DO
    rU_Control[iIdx1] := rMPC_CandInputs[1, iIdx1];
    rU_ControlPrev[iIdx1] := rU_Control[iIdx1];
END_FOR;

(* Map to physical modulating actuator outputs *)
rCmd_SteamModValve_pct           := rU_Control[1];
rCmd_AirOverpressValve_pct       := rU_Control[2];
rCmd_ExhaustVentValve_pct        := rU_Control[3];
rCmd_CoolingWaterCascadeValve_pct:= rU_Control[4];
rCmd_RotaryDrumSpeed_RPM         := rU_Control[5];'''
