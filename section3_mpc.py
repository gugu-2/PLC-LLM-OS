# section3_mpc.py
# Receding-Horizon MPC Optimization with 10 Unrolled Projected Gradient Descent (PGD) Iterations

def get_section3():
    return """
(* ========================================================================================= *)
(* 3.0 RECEDING-HORIZON MPC OPTIMIZATION (10 UNROLLED PGD ITERATIONS)                       *)
(* ========================================================================================= *)
(* Solves an embedded multivariable receding-horizon quadratic optimization problem over     *)
(* a 10-step prediction horizon (N = 10 ms at Ts = 1.0 ms) using Projected Gradient         *)
(* Descent (PGD) with adjoint costate back-propagation and dynamic anti-flash constraints.   *)

IF bMpcGovernorEnable AND NOT bSystemTripped THEN
    bMpcInOptimization := TRUE;

    (* ------------------------------------------------------------------------------------- *)
    (* 3.1 Dynamic State Reference Vector Assignment (x_ref) Based on FSM Injection Phase   *)
    (* ------------------------------------------------------------------------------------- *)
    CASE iState OF
        c_STATE_IDLE, c_STATE_DIE_SAFETY_DOOR_LOCK_AND_PARTING_AGENT_SPRAY:
            x_ref[1] := 0.0;     (* Plunger at complete standstill [m/s] *)
            x_ref[2] := 15.0;    (* Standby pilot charge pressure [bar] *)
            x_ref[3] := 1013.0;  (* Ambient vented atmospheric pressure [mbar] *)
            x_ref[4] := 0.0;     (* Unclamped platen [kN] *)
            x_ref[5] := 230.0;   (* Target preheated die surface temperature [deg C] *)
            x_ref[6] := 0.0;     (* No casting in die *)
            u_target[1] := 0.0;  u_target[2] := 0.0;  u_target[3] := 0.0;  u_target[4] := 0.0;  u_target[5] := 35.0;

        c_STATE_4_TIE_BAR_HYDRAULIC_CLAMP_TO_90000KN:
            x_ref[1] := 0.0;
            x_ref[2] := 25.0;
            x_ref[3] := 1013.0;
            x_ref[4] := 90000.0; (* Ramp clamp force to full 90,000 kN nominal [kN] *)
            x_ref[5] := 235.0;
            x_ref[6] := 0.0;
            u_target[1] := 0.0;  u_target[2] := 0.0;  u_target[3] := 0.0;  u_target[4] := 0.0;  u_target[5] := 40.0;

        c_STATE_LADLE_ROBOT_MOLTEN_ALUMINUM_POUR_INTO_SLEEVE:
            x_ref[1] := 0.0;
            x_ref[2] := 25.0;
            x_ref[3] := 1013.0;
            x_ref[4] := 90000.0;
            x_ref[5] := 240.0;
            x_ref[6] := 0.0;
            u_target[1] := 0.0;  u_target[2] := 0.0;  u_target[3] := 0.0;  u_target[4] := 0.0;  u_target[5] := 45.0;

        c_STATE_MOLD_CAVITY_HIGH_VACUUM_EVACUATION_BELOW_25MBAR:
            x_ref[1] := 0.0;
            x_ref[2] := 25.0;
            x_ref[3] := 18.0;    (* Target deep vacuum < 25.0 mbar [mbar] *)
            x_ref[4] := 90000.0;
            x_ref[5] := 245.0;
            x_ref[6] := 0.0;
            u_target[1] := 0.0;  u_target[2] := 0.0;  u_target[3] := 0.0;  u_target[4] := 85.0; u_target[5] := 50.0;

        c_STATE_PHASE1_SLOW_SHOT_WAVE_SURGE_SUPPRESSION:
            x_ref[1] := 0.25 * rWaveProfileDampingGain; (* Sculpted slow shot velocity [m/s] *)
            x_ref[2] := 48.0;    (* Sleeve gathering backpressure [bar] *)
            x_ref[3] := 15.0;    (* Continue vacuum extraction below 20 mbar *)
            x_ref[4] := 90000.0;
            x_ref[5] := 248.0;
            x_ref[6] := 0.0;
            u_target[1] := 18.5; u_target[2] := 0.0;  u_target[3] := 0.0;  u_target[4] := 95.0; u_target[5] := 55.0;

        c_STATE_PHASE2_FAST_SHOT_HIGH_ACCELERATION_CAVITY_FILL, c_STATE_VACUUM_CHILL_BLOCK_VALVE_FAST_SHUTOFF:
            x_ref[1] := 8.50;    (* High-speed fast shot cavity fill velocity [m/s] *)
            x_ref[2] := 285.0;   (* Cavity filling hydraulic head pressure [bar] *)
            x_ref[3] := 12.0;    (* Deepest vacuum prior to chill vent shutoff *)
            x_ref[4] := 90000.0;
            x_ref[5] := 260.0;
            x_ref[6] := 0.35;    (* Initial shell formation *)
            u_target[1] := 85.0; u_target[2] := 90.0; u_target[3] := 0.0;  u_target[4] := 0.0;  u_target[5] := 65.0;

        c_STATE_PHASE3_INTENSIFICATION_PRESSURE_SQUEEZE_1400BAR:
            x_ref[1] := 0.05;    (* Decelerated plunger forging squeeze speed [m/s] *)
            x_ref[2] := 1400.0;  (* Peak static squeeze pressure [bar] *)
            x_ref[3] := 10.0;
            x_ref[4] := 92500.0; (* Dynamic clamp force expansion compensation [kN] *)
            x_ref[5] := 275.0;
            x_ref[6] := 1.15;    (* Rapid solidification through wall *)
            u_target[1] := 10.0; u_target[2] := 0.0;  u_target[3] := 95.0; u_target[4] := 0.0;  u_target[5] := 80.0;

        c_STATE_IN_DIE_SOLIDIFICATION_COOLING_HOLD:
            x_ref[1] := 0.0;
            x_ref[2] := 650.0;   (* Sustained holding pressure [bar] *)
            x_ref[3] := 500.0;   (* Venting cavity *)
            x_ref[4] := 90000.0;
            x_ref[5] := 240.0;   (* Cooling down to extraction temperature *)
            x_ref[6] := 1.25;    (* 100% through-thickness solidification (1.25 mm skin) *)
            u_target[1] := 0.0;  u_target[2] := 0.0;  u_target[3] := 45.0; u_target[4] := 0.0;  u_target[5] := 90.0;

        c_STATE_TIE_BAR_DECOMPRESSION_AND_DIE_OPEN_STROKE,
        c_STATE_HYDRAULIC_EJECTOR_PINS_MULTI_POINT_PUSH,
        c_STATE_EXTRACTOR_ROBOT_PART_GRIP_AND_LASER_METROLOGY:
            x_ref[1] := 0.0;
            x_ref[2] := 0.0;
            x_ref[3] := 1013.0;
            x_ref[4] := 0.0;     (* Clamping released *)
            x_ref[5] := 225.0;
            x_ref[6] := 1.25;
            u_target[1] := 0.0;  u_target[2] := 0.0;  u_target[3] := 0.0;  u_target[4] := 0.0;  u_target[5] := 40.0;

        ELSE
            (* Safety standby default *)
            x_ref[1] := 0.0;     x_ref[2] := 0.0;     x_ref[3] := 1013.0;
            x_ref[4] := 0.0;     x_ref[5] := 220.0;   x_ref[6] := 0.0;
            u_target[1] := 0.0;  u_target[2] := 0.0;  u_target[3] := 0.0;  u_target[4] := 0.0;  u_target[5] := 30.0;
    END_CASE;

    (* Evaluate Instantaneous State Tracking Errors *)
    FOR iIdx1 := 1 TO 6 DO
        x_err[iIdx1] := x_state[iIdx1] - x_ref[iIdx1];
    END_FOR;

    (* ------------------------------------------------------------------------------------- *)
    (* 3.2 Initialize Prediction Horizon Trajectories (10 Steps Forward)                     *)
    (* ------------------------------------------------------------------------------------- *)
    FOR iIdx1 := 1 TO 10 DO
        FOR iIdx2 := 1 TO 5 DO
            u_traj[iIdx1, iIdx2] := u_mpc[iIdx2];
        END_FOR;
    END_FOR;

    (* Approximate Diagonal Hessian Elements: H_diag[j] = sum_i(B[i,j]^2 * Q[i]) + R[j] + S[j] *)
    FOR iIdx2 := 1 TO 5 DO
        rTempSum := R_diag[iIdx2] + S_diag[iIdx2];
        FOR iIdx1 := 1 TO 6 DO
            rTempSum := rTempSum + (B_mat[iIdx1, iIdx2] * B_mat[iIdx1, iIdx2] * Q_diag[iIdx1]);
        END_FOR;
        IF rTempSum < 0.10 THEN rTempSum := 0.10; END_IF;
        H_diag[iIdx2] := rTempSum;
    END_FOR;

    (* ===================================================================================== *)
    (* 3.3 UNROLLED 10 PROJECTED GRADIENT DESCENT (PGD) ITERATIONS                           *)
    (* ===================================================================================== *)
    FOR iIterPgd := 1 TO 10 DO

        (* --- Forward Simulation of State Trajectory across Horizon k = 1 to 10 --- *)
        FOR iIdx1 := 1 TO 6 DO
            x_traj[1, iIdx1] := x_state[iIdx1];
        END_FOR;

        FOR iIdx3 := 1 TO 9 DO
            FOR iIdx1 := 1 TO 6 DO
                rTempSum := 0.0;
                FOR iIdx2 := 1 TO 6 DO
                    rTempSum := rTempSum + (A_mat[iIdx1, iIdx2] * x_traj[iIdx3, iIdx2]);
                END_FOR;
                FOR iIdx2 := 1 TO 5 DO
                    rTempSum := rTempSum + (B_mat[iIdx1, iIdx2] * u_traj[iIdx3, iIdx2]);
                END_FOR;
                x_traj[iIdx3 + 1, iIdx1] := rTempSum;
            END_FOR;
        END_FOR;

        (* --- Backward Simulation of Adjoint Costates lambda across Horizon k = 10 down to 1 --- *)
        (* Terminal Boundary Condition: lambda[10] = P * (x_traj[10] - x_ref) *)
        FOR iIdx1 := 1 TO 6 DO
            lambda_traj[10, iIdx1] := P_diag[iIdx1] * (x_traj[10, iIdx1] - x_ref[iIdx1]);
        END_FOR;

        FOR iIdx3 := 9 TO 1 BY -1 DO
            FOR iIdx1 := 1 TO 6 DO
                (* lambda[k] = A^T * lambda[k+1] + Q * (x_traj[k] - x_ref) *)
                rTempSum := Q_diag[iIdx1] * (x_traj[iIdx3, iIdx1] - x_ref[iIdx1]);
                FOR iIdx2 := 1 TO 6 DO
                    rTempSum := rTempSum + (A_mat[iIdx2, iIdx1] * lambda_traj[iIdx3 + 1, iIdx2]);
                END_FOR;
                lambda_traj[iIdx3, iIdx1] := rTempSum;
            END_FOR;
        END_FOR;

        (* --- Gradient Evaluation w.r.t Control Trajectory: grad = B^T * lambda + R*(u-u_tgt) + S*(u-u_prev) --- *)
        FOR iIdx3 := 1 TO 10 DO
            FOR iIdx2 := 1 TO 5 DO
                rTempSum := (R_diag[iIdx2] * (u_traj[iIdx3, iIdx2] - u_target[iIdx2])) + 
                            (S_diag[iIdx2] * (u_traj[iIdx3, iIdx2] - u_prev[iIdx2]));
                FOR iIdx1 := 1 TO 6 DO
                    rTempSum := rTempSum + (B_mat[iIdx1, iIdx2] * lambda_traj[iIdx3, iIdx1]);
                END_FOR;
                grad_traj[iIdx3, iIdx2] := rTempSum;

                (* Newton-Raphson Scaled Gradient Step *)
                u_delta[iIdx2] := -1.0 * (grad_traj[iIdx3, iIdx2] / H_diag[iIdx2]) * rStepSize;

                (* Apply Step to Trajectory *)
                u_traj[iIdx3, iIdx2] := u_traj[iIdx3, iIdx2] + u_delta[iIdx2];

                (* Projection onto Slew Rate Bounds *)
                IF iIdx2 = 1 THEN
                    IF (u_traj[iIdx3, 1] - u_prev[1]) > rMaxPilotSlew_pct_ms THEN
                        u_traj[iIdx3, 1] := u_prev[1] + rMaxPilotSlew_pct_ms;
                    ELSIF (u_traj[iIdx3, 1] - u_prev[1]) < -rMaxPilotSlew_pct_ms THEN
                        u_traj[iIdx3, 1] := u_prev[1] - rMaxPilotSlew_pct_ms;
                    END_IF;
                ELSIF iIdx2 = 2 THEN
                    IF (u_traj[iIdx3, 2] - u_prev[2]) > rMaxPoppetSlew_pct_ms THEN
                        u_traj[iIdx3, 2] := u_prev[2] + rMaxPoppetSlew_pct_ms;
                    ELSIF (u_traj[iIdx3, 2] - u_prev[2]) < -rMaxPoppetSlew_pct_ms THEN
                        u_traj[iIdx3, 2] := u_prev[2] - rMaxPoppetSlew_pct_ms;
                    END_IF;
                ELSIF iIdx2 = 3 THEN
                    IF (u_traj[iIdx3, 3] - u_prev[3]) > rMaxIntensifierSlew_pct_ms THEN
                        u_traj[iIdx3, 3] := u_prev[3] + rMaxIntensifierSlew_pct_ms;
                    ELSIF (u_traj[iIdx3, 3] - u_prev[3]) < -rMaxIntensifierSlew_pct_ms THEN
                        u_traj[iIdx3, 3] := u_prev[3] - rMaxIntensifierSlew_pct_ms;
                    END_IF;
                ELSIF iIdx2 = 4 THEN
                    IF (u_traj[iIdx3, 4] - u_prev[4]) > rMaxVacuumSlew_pct_ms THEN
                        u_traj[iIdx3, 4] := u_prev[4] + rMaxVacuumSlew_pct_ms;
                    ELSIF (u_traj[iIdx3, 4] - u_prev[4]) < -rMaxVacuumSlew_pct_ms THEN
                        u_traj[iIdx3, 4] := u_prev[4] - rMaxVacuumSlew_pct_ms;
                    END_IF;
                ELSIF iIdx2 = 5 THEN
                    IF (u_traj[iIdx3, 5] - u_prev[5]) > rMaxTemperingSlew_pct_ms THEN
                        u_traj[iIdx3, 5] := u_prev[5] + rMaxTemperingSlew_pct_ms;
                    ELSIF (u_traj[iIdx3, 5] - u_prev[5]) < -rMaxTemperingSlew_pct_ms THEN
                        u_traj[iIdx3, 5] := u_prev[5] - rMaxTemperingSlew_pct_ms;
                    END_IF;
                END_IF;

                (* Hard Actuator Saturation Projection [0.0% to 100.0%] *)
                IF u_traj[iIdx3, iIdx2] < 0.0 THEN u_traj[iIdx3, iIdx2] := 0.0; END_IF;
                IF u_traj[iIdx3, iIdx2] > 100.0 THEN u_traj[iIdx3, iIdx2] := 100.0; END_IF;
            END_FOR;

            (* --- Critical Cyber-Physical Safety Constraint: Molten Metal Flash Blowout Prevention --- *)
            (* Predicted head pressure under current pilot & booster commands *)
            rFlashCheckSeparation_kN := ((u_traj[iIdx3, 3] * 14.0) * 100.0 * c_PartingProjectedArea_m2 * 0.82);
            IF (rFlashCheckSeparation_kN > (rClampForce_Voted_kN - 5000.0)) THEN
                (* Dynamic clamp reserve violation: immediately de-rate booster multiplier valve *)
                u_traj[iIdx3, 3] := (rClampForce_Voted_kN - 5000.0) / (14.0 * 100.0 * c_PartingProjectedArea_m2 * 0.82);
                IF u_traj[iIdx3, 3] < 0.0 THEN u_traj[iIdx3, 3] := 0.0; END_IF;
            END_IF;
        END_FOR;

    END_FOR; (* End of 10 PGD iterations *)

    (* Extract First Control Action: Receding Horizon Execution *)
    FOR iIdx2 := 1 TO 5 DO
        u_mpc[iIdx2] := u_traj[1, iIdx2];
    END_FOR;

    (* Evaluate Instantaneous Quadratic Tracking Cost *)
    rMpcCost := 0.0;
    FOR iIdx1 := 1 TO 6 DO
        rMpcCost := rMpcCost + (Q_diag[iIdx1] * x_err[iIdx1] * x_err[iIdx1]);
    END_FOR;
    FOR iIdx2 := 1 TO 5 DO
        rMpcCost := rMpcCost + (R_diag[iIdx2] * (u_mpc[iIdx2] - u_target[iIdx2]) * (u_mpc[iIdx2] - u_target[iIdx2]));
    END_FOR;

ELSE
    bMpcInOptimization := FALSE;
    FOR iIdx2 := 1 TO 5 DO
        u_mpc[iIdx2] := 0.0;
    END_FOR;
    rMpcCost := 0.0;
END_IF;
"""

if __name__ == "__main__":
    print("Section 3 len:", len(get_section3()))
