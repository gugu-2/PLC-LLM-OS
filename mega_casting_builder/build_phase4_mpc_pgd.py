# mega_casting_builder/build_phase4_mpc_pgd.py

def get_phase4_mpc_pgd():
    return """(* =====================================================================================================================
 * PHASE 4: RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) WITH UNROLLED PROJECTED GRADIENT DESCENT (PGD)
 * Horizon N = 5 steps, 10 Unrolled Optimization Iterations per PLC Scan (Ts = 1.0 ms)
 * Balances:
 *   u1: Ultra-Fast Servo Proportional Hydraulic Injection Valve Spool Command [%]
 *   u2: High-Speed Accumulator Pilot Pressure Trim [%]
 *   u3: Phase 3 Intensification Booster Valve Fast Spool Command [%]
 *   u4: Parting Plane Vacuum Evacuation Throttle Valve [%]
 *   u5: Mold Multi-Circuit Thermal Oil Flow Trim [%]
 *   u6: Toggle Clamping Locking Pilot Pressure Trim [%]
 * ===================================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------------------------
 * 1. DYNAMIC REFERENCE VECTOR SYNTHESIS (rMPC_Ref_x) BASED ON PRODUCTION FINITE STATE MACHINE
 * --------------------------------------------------------------------------------------------------------------------- *)
CASE iFSM_State OF
    0: (* STATE_IDLE *)
        rMPC_Ref_x[1] := 0.0;     (* Plunger at home 0.0 mm *)
        rMPC_Ref_x[2] := 0.0;     (* Stationary velocity 0.0 m/s *)
        rMPC_Ref_x[3] := 25.0;    (* Standby system idle pressure 25 bar *)
        rMPC_Ref_x[4] := 0.0;     (* Cavity empty atmospheric 0 bar *)
        rMPC_Ref_x[5] := 1013.25; (* Ambient atmospheric pressure 1013 mbar *)
        rMPC_Ref_x[6] := 0.0;     (* Toggle open 0 kN *)

    1: (* STATE_MOLD_DIE_PREHEAT_OIL_BALANCE *)
        rMPC_Ref_x[1] := 0.0;
        rMPC_Ref_x[2] := 0.0;
        rMPC_Ref_x[3] := 35.0;
        rMPC_Ref_x[4] := 0.0;
        rMPC_Ref_x[5] := 1013.25;
        rMPC_Ref_x[6] := 5000.0;  (* Kiss-pressure pre-lockup for thermal conduction *)

    2: (* STATE_LADLE_POUR_MOLTEN_ALUMINUM_SHOT_SLEEVE *)
        rMPC_Ref_x[1] := 0.0;
        rMPC_Ref_x[2] := 0.0;
        rMPC_Ref_x[3] := 35.0;
        rMPC_Ref_x[4] := 0.0;
        rMPC_Ref_x[5] := 1013.25;
        rMPC_Ref_x[6] := 5000.0;

    3: (* STATE_TOGGLE_CLAMP_LOCKUP_60000KN *)
        rMPC_Ref_x[1] := 0.0;
        rMPC_Ref_x[2] := 0.0;
        rMPC_Ref_x[3] := 40.0;
        rMPC_Ref_x[4] := 0.0;
        rMPC_Ref_x[5] := 1013.25;
        rMPC_Ref_x[6] := 580.0;   (* Target tie-bar strain corresponding to 60,000 kN lockup *)

    4: (* STATE_VACUUM_EVACUATION_DRAWDOWN_25MBAR *)
        rMPC_Ref_x[1] := 0.0;
        rMPC_Ref_x[2] := 0.0;
        rMPC_Ref_x[3] := 40.0;
        rMPC_Ref_x[4] := 0.0;
        rMPC_Ref_x[5] := rRecipe_Vacuum_Threshold_mbar; (* Target < 25.0 mbar *)
        rMPC_Ref_x[6] := 580.0;

    5: (* STATE_PHASE1_SLOW_SHOT_WAVE_FREE_ACCEL *)
        rMPC_Ref_x[1] := rRecipe_Phase1_SwitchPos;      (* Advance toward switchpoint *)
        rMPC_Ref_x[2] := rRecipe_Phase1_Velocity;       (* Wave-free slow speed (e.g. 0.45 m/s) *)
        rMPC_Ref_x[3] := 65.0;                          (* Sleeve friction push pressure *)
        rMPC_Ref_x[4] := 0.0;                           (* Cavity not yet reached *)
        rMPC_Ref_x[5] := 20.0;                          (* Maintain deep vacuum *)
        rMPC_Ref_x[6] := 580.0;

    6: (* STATE_PHASE2_FAST_SHOT_GATE_INJECTION_RUN *)
        rMPC_Ref_x[1] := rTotalStrokeLength_mm - rRecipe_Biscuit_Nominal_mm;
        rMPC_Ref_x[2] := rRecipe_Phase2_Velocity;       (* High-speed cavity fill: up to 9.5 m/s! *)
        rMPC_Ref_x[3] := 240.0;                         (* Dynamic head pressure during fill *)
        rMPC_Ref_x[4] := 450.0;                         (* Dynamic gating flow backpressure *)
        rMPC_Ref_x[5] := 15.0;                          (* Ultra-deep vacuum assist *)
        rMPC_Ref_x[6] := 595.0;                         (* Dynamic parting separation compliance *)

    7: (* STATE_PHASE3_INSTANT_INTENSIFICATION_SPIKE *)
        rMPC_Ref_x[1] := rTotalStrokeLength_mm - rRecipe_Biscuit_Nominal_mm;
        rMPC_Ref_x[2] := 0.05;                          (* Rapid deceleration to near-rest *)
        rMPC_Ref_x[3] := rRecipe_Intensification_Press; (* 1,200 bar specific intensification! *)
        rMPC_Ref_x[4] := rRecipe_Intensification_Press * 0.92; (* Cavity hydro-solidification pressure *)
        rMPC_Ref_x[5] := 35.0;
        rMPC_Ref_x[6] := 610.0;                         (* High parting pressure tie-bar stretch *)

    8: (* STATE_PHASE4_BISCUIT_HOLD_AND_SOLIDIFICATION *)
        rMPC_Ref_x[1] := rTotalStrokeLength_mm - rRecipe_Biscuit_Nominal_mm;
        rMPC_Ref_x[2] := 0.0;                           (* Zero velocity during freeze-off *)
        rMPC_Ref_x[3] := 950.0;                         (* Solidification holding pressure *)
        rMPC_Ref_x[4] := 750.0;                         (* Solidifying casting internal pressure *)
        rMPC_Ref_x[5] := 1013.25;                       (* Venting allowed *)
        rMPC_Ref_x[6] := 580.0;

    9..12: (* DEMOLD, RETRACT, SPRAY *)
        rMPC_Ref_x[1] := 0.0;
        rMPC_Ref_x[2] := 0.0;
        rMPC_Ref_x[3] := 25.0;
        rMPC_Ref_x[4] := 0.0;
        rMPC_Ref_x[5] := 1013.25;
        rMPC_Ref_x[6] := 0.0;

    ELSE (* 13: EMERGENCY TRIP *)
        rMPC_Ref_x[1] := rState_x_hat[1];
        rMPC_Ref_x[2] := 0.0;
        rMPC_Ref_x[3] := 0.0;
        rMPC_Ref_x[4] := 0.0;
        rMPC_Ref_x[5] := 1013.25;
        rMPC_Ref_x[6] := 0.0;
END_CASE;

(* ---------------------------------------------------------------------------------------------------------------------
 * 2. INITIALIZE PREDICTION HORIZON TRAJECTORIES (N = 5 steps)
 * Warm-start from previous control inputs or current estimated state
 * --------------------------------------------------------------------------------------------------------------------- *)
FOR n_step := 1 TO 5 DO
    FOR i_idx := 1 TO 6 DO
        IF n_step = 1 THEN
            rMPC_Pred_x[n_step, i_idx] := rState_x_hat[i_idx];
        ELSE
            rMPC_Pred_x[n_step, i_idx] := rMPC_Ref_x[i_idx];
        END_IF;
        rMPC_Pred_u[n_step, i_idx] := rInput_u[i_idx];
    END_FOR;
END_FOR;

(* ---------------------------------------------------------------------------------------------------------------------
 * 3. UNROLLED PROJECTED GRADIENT DESCENT (PGD) OPTIMIZATION LOOP: 10 ITERATIONS
 * Fully evaluates state trajectory cost, actuator penalties, analytical gradients, and box projections
 * --------------------------------------------------------------------------------------------------------------------- *)
FOR k_iter := 1 TO 10 DO

    (* Step 3.1: Forward State Trajectory Simulation Across Horizon N = 5 *)
    FOR n_step := 1 TO 4 DO
        FOR i_idx := 1 TO 6 DO
            rMPC_Pred_x[n_step + 1, i_idx] := 0.0;
            (* Matrix A contribution *)
            FOR j_idx := 1 TO 6 DO
                rMPC_Pred_x[n_step + 1, i_idx] := rMPC_Pred_x[n_step + 1, i_idx] + (rMatrix_A[i_idx, j_idx] * rMPC_Pred_x[n_step, j_idx]);
            END_FOR;
            (* Matrix B contribution *)
            FOR m_idx := 1 TO 6 DO
                rMPC_Pred_x[n_step + 1, i_idx] := rMPC_Pred_x[n_step + 1, i_idx] + (rMatrix_B[i_idx, m_idx] * rMPC_Pred_u[n_step, m_idx]);
            END_FOR;
        END_FOR;
    END_FOR;

    (* Step 3.2: Cumulative Cost Function Evaluation *)
    rMPC_Cost_Total := 0.0;
    rMPC_Cost_State := 0.0;
    rMPC_Cost_Actuator := 0.0;
    rMPC_Cost_Slew := 0.0;

    FOR n_step := 1 TO 5 DO
        (* State Tracking Cost: (x - x_ref)^T * Q * (x - x_ref) *)
        FOR i_idx := 1 TO 6 DO
            IF n_step < 5 THEN
                rMPC_Cost_State := rMPC_Cost_State + (rMPC_Matrix_Q[i_idx, i_idx] * (rMPC_Pred_x[n_step, i_idx] - rMPC_Ref_x[i_idx]) * (rMPC_Pred_x[n_step, i_idx] - rMPC_Ref_x[i_idx]));
            ELSE
                (* Terminal State Cost P *)
                rMPC_Cost_State := rMPC_Cost_State + (rMPC_Matrix_P[i_idx, i_idx] * (rMPC_Pred_x[n_step, i_idx] - rMPC_Ref_x[i_idx]) * (rMPC_Pred_x[n_step, i_idx] - rMPC_Ref_x[i_idx]));
            END_IF;
        END_FOR;

        (* Actuator Energy & Slew Cost *)
        FOR m_idx := 1 TO 6 DO
            rMPC_Cost_Actuator := rMPC_Cost_Actuator + (rMPC_Matrix_R[m_idx, m_idx] * rMPC_Pred_u[n_step, m_idx] * rMPC_Pred_u[n_step, m_idx]);
            IF n_step = 1 THEN
                rMPC_Cost_Slew := rMPC_Cost_Slew + (rMPC_Matrix_S[m_idx, m_idx] * (rMPC_Pred_u[n_step, m_idx] - rInput_u_prev[m_idx]) * (rMPC_Pred_u[n_step, m_idx] - rInput_u_prev[m_idx]));
            ELSE
                rMPC_Cost_Slew := rMPC_Cost_Slew + (rMPC_Matrix_S[m_idx, m_idx] * (rMPC_Pred_u[n_step, m_idx] - rMPC_Pred_u[n_step - 1, m_idx]) * (rMPC_Pred_u[n_step, m_idx] - rMPC_Pred_u[n_step - 1, m_idx]));
            END_IF;
        END_FOR;
    END_FOR;
    rMPC_Cost_Total := rMPC_Cost_State + rMPC_Cost_Actuator + rMPC_Cost_Slew;

    (* Step 3.3: Analytical Gradient Computation dJ/du across Horizon *)
    FOR n_step := 1 TO 5 DO
        FOR m_idx := 1 TO 6 DO
            (* Direct Actuator Effort Gradient *)
            rMPC_Grad_u[n_step, m_idx] := 2.0 * rMPC_Matrix_R[m_idx, m_idx] * rMPC_Pred_u[n_step, m_idx];

            (* Actuator Slew Rate Dynamic Gradient *)
            IF n_step = 1 THEN
                rMPC_Grad_u[n_step, m_idx] := rMPC_Grad_u[n_step, m_idx] + (2.0 * rMPC_Matrix_S[m_idx, m_idx] * (rMPC_Pred_u[n_step, m_idx] - rInput_u_prev[m_idx]));
            ELSE
                rMPC_Grad_u[n_step, m_idx] := rMPC_Grad_u[n_step, m_idx] + (2.0 * rMPC_Matrix_S[m_idx, m_idx] * (rMPC_Pred_u[n_step, m_idx] - rMPC_Pred_u[n_step - 1, m_idx]));
            END_IF;

            (* State Back-Propagation Sensitivity: sum_i (B[i, m] * 2 * Q[i, i] * (x[n+1, i] - x_ref[i])) *)
            IF n_step < 5 THEN
                FOR i_idx := 1 TO 6 DO
                    rMPC_Grad_u[n_step, m_idx] := rMPC_Grad_u[n_step, m_idx] + (rMatrix_B[i_idx, m_idx] * 2.0 * rMPC_Matrix_Q[i_idx, i_idx] * (rMPC_Pred_x[n_step + 1, i_idx] - rMPC_Ref_x[i_idx]));
                END_FOR;
            ELSE
                FOR i_idx := 1 TO 6 DO
                    rMPC_Grad_u[n_step, m_idx] := rMPC_Grad_u[n_step, m_idx] + (rMatrix_B[i_idx, m_idx] * 2.0 * rMPC_Matrix_P[i_idx, i_idx] * (rMPC_Pred_x[n_step, i_idx] - rMPC_Ref_x[i_idx]));
                END_FOR;
            END_IF;

            (* Step 3.4: Gradient Descent Update *)
            rMPC_Pred_u[n_step, m_idx] := rMPC_Pred_u[n_step, m_idx] - (rMPC_LearningRate_Alpha * rMPC_Grad_u[n_step, m_idx]);

            (* Step 3.5: Hard Actuator Saturation Box Projection [u_min, u_max] *)
            IF rMPC_Pred_u[n_step, m_idx] < rMPC_u_Min[m_idx] THEN
                rMPC_Pred_u[n_step, m_idx] := rMPC_u_Min[m_idx];
            ELSIF rMPC_Pred_u[n_step, m_idx] > rMPC_u_Max[m_idx] THEN
                rMPC_Pred_u[n_step, m_idx] := rMPC_u_Max[m_idx];
            END_IF;

            (* Step 3.6: Dynamic Slew Rate Projection *)
            IF n_step = 1 THEN
                IF (rMPC_Pred_u[n_step, m_idx] - rInput_u_prev[m_idx]) > rMPC_Slew_Max[m_idx] THEN
                    rMPC_Pred_u[n_step, m_idx] := rInput_u_prev[m_idx] + rMPC_Slew_Max[m_idx];
                ELSIF (rMPC_Pred_u[n_step, m_idx] - rInput_u_prev[m_idx]) < -rMPC_Slew_Max[m_idx] THEN
                    rMPC_Pred_u[n_step, m_idx] := rInput_u_prev[m_idx] - rMPC_Slew_Max[m_idx];
                END_IF;
            END_IF;
        END_FOR;
    END_FOR;

END_FOR; (* End of 10 Unrolled Optimization Iterations *)

(* ---------------------------------------------------------------------------------------------------------------------
 * 4. DISPATCH FIRST STEP OPTIMAL ACTUATOR COMMANDS u[1] TO PHYSICAL INTERFACE
 * --------------------------------------------------------------------------------------------------------------------- *)
IF bEnable AND NOT bGeneralFault AND bEmergencyStop THEN
    rServoInjectionValve_Cmd  := rMPC_Pred_u[1, 1];
    rAccumulatorPilotTrim_Cmd := rMPC_Pred_u[1, 2];
    rIntensificationValve_Cmd := rMPC_Pred_u[1, 3];
    rVacuumThrottle_Cmd       := rMPC_Pred_u[1, 4];
    rThermalOil_Valve_Cmd     := rMPC_Pred_u[1, 5];
    rToggleClampPilot_Cmd     := rMPC_Pred_u[1, 6];
ELSE
    (* Emergency Safe Actuator Dump *)
    rServoInjectionValve_Cmd  := 0.0;
    rAccumulatorPilotTrim_Cmd := 0.0;
    rIntensificationValve_Cmd := 0.0;
    rVacuumThrottle_Cmd       := 0.0;
    rThermalOil_Valve_Cmd     := 0.0;
    rToggleClampPilot_Cmd     := 0.0;
END_IF;

(* Save history vector for next scan slew rate penalty *)
FOR m_idx := 1 TO 6 DO
    rInput_u_prev[m_idx] := rInput_u[m_idx];
END_FOR;
"""
