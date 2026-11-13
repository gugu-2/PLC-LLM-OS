# hpdc_megacasting_builder/build_st_phase3_mpc.py

def get_phase3_mpc():
    return """(* =====================================================================================================================
 * PHASE 3: RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) WITH PROJECTED GRADIENT DESCENT (PGD)
 * Unrolled 6-iteration real-time optimization ensuring bumpless transition between kinematic Phase 2 velocity control
 * and hydrostatic Phase 3 intensification pressure hold to eliminate parting line flash and gas porosity.
 * ===================================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------------------------
 * 1. DYNAMIC REFERENCE TRAJECTORY GENERATION r[k] ACCORDING TO FSM OPERATIONAL PHASE
 * --------------------------------------------------------------------------------------------------------------------- *)
CASE iFSM_CurrentState OF

    3: (* STATE_03_BISCUIT_SLOW_SHOT_PHASE1: Controlled planar wave formation *)
        rVec_r_Reference[1] := rRecipe_Phase1_Stroke_In;
        (* Parabolic soft ramp to target slow velocity *)
        IF rFSM_StateTimer_s < 0.250 THEN
            rVec_r_Reference[2] := rRecipe_Phase1_Velocity_In * (rFSM_StateTimer_s / 0.250) * (rFSM_StateTimer_s / 0.250);
        ELSE
            rVec_r_Reference[2] := rRecipe_Phase1_Velocity_In;
        END_IF;
        rVec_r_Reference[3] := 45.0;  (* Gentle forward head pressure [bar] *)
        rVec_r_Reference[4] := 15.0;  (* Counter balance rod pressure [bar] *)
        rVec_r_Reference[5] := 350.0; (* Pre-evacuation ambient envelope [mbar] *)
        rVec_r_Reference[6] := 240.0; (* Target die surface temperature [deg C] *)

    4: (* STATE_04_VACUUM_EVACUATION_PUMP: Deep cavity degassing *)
        rVec_r_Reference[1] := rRecipe_Phase1_Stroke_In;
        rVec_r_Reference[2] := 0.050; (* Creep forward while drawing vacuum *)
        rVec_r_Reference[3] := 40.0;
        rVec_r_Reference[4] := 20.0;
        rVec_r_Reference[5] := rRecipe_VacuumSetpoint_In; (* Deep vacuum setpoint (e.g. 40 mbar) *)
        rVec_r_Reference[6] := 240.0;

    5: (* STATE_05_HIGH_SPEED_INJECTION_PHASE2: Explosive cavity filling *)
        rVec_r_Reference[1] := rRecipe_Phase2_CutoffPos_In;
        (* S-curve jerk-limited velocity tracking up to 10 m/s *)
        IF rTMR_ENC301_Voted < (rRecipe_Phase2_CutoffPos_In - 40.0) THEN
            rVec_r_Reference[2] := rRecipe_Phase2_Velocity_In;
        ELSE
            (* Smooth deceleration cushion prior to cavity metal impact to prevent pressure spike *)
            rVec_r_Reference[2] := rRecipe_Phase2_Velocity_In * 0.70;
        END_IF;
        rVec_r_Reference[3] := 180.0; (* High driving accumulator pressure [bar] *)
        rVec_r_Reference[4] := 10.0;  (* Rod chamber low resistance dump *)
        rVec_r_Reference[5] := rRecipe_VacuumSetpoint_In;
        rVec_r_Reference[6] := 250.0;

    6: (* STATE_06_INTENSIFICATION_HOLD_PHASE3: Hydrostatic shrinkage compaction (< 15 ms rise) *)
        rVec_r_Reference[1] := rMachine_Full_Stroke_mm - rRecipe_TargetBiscuit_In;
        rVec_r_Reference[2] := 0.0;   (* Zero kinematic velocity - Pure hydrostatic squeeze *)
        (* Target hydraulic head pressure required to achieve target metal intensification pressure *)
        IF rCylHead_Area_m2 > 0.001 THEN
            rVec_r_Reference[3] := (rRecipe_Phase3_IntensPres_In * 100.0 * rPlunger_Area_m2) / (rCylHead_Area_m2 * 100.0);
        ELSE
            rVec_r_Reference[3] := 260.0;
        END_IF;
        rVec_r_Reference[4] := 5.0;
        rVec_r_Reference[5] := 1000.0; (* Vacuum valve closed, ambient venting *)
        rVec_r_Reference[6] := 230.0;

    7: (* STATE_07_SOLIDIFICATION_COOLING: In-die metallurgical dwell *)
        rVec_r_Reference[1] := rMachine_Full_Stroke_mm - rRecipe_TargetBiscuit_In;
        rVec_r_Reference[2] := 0.0;
        rVec_r_Reference[3] := 220.0; (* Maintain compaction pressure during dendritic crystallization *)
        rVec_r_Reference[4] := 5.0;
        rVec_r_Reference[5] := 1000.0;
        rVec_r_Reference[6] := 210.0;

ELSE
    (* Quiescent / Standby Trajectory for Clamp, Ladle, Ejection, and Spray phases *)
    rVec_r_Reference[1] := 0.0;
    rVec_r_Reference[2] := 0.0;
    rVec_r_Reference[3] := 10.0;
    rVec_r_Reference[4] := 10.0;
    rVec_r_Reference[5] := 1013.0;
    rVec_r_Reference[6] := 220.0;
END_CASE;

(* ---------------------------------------------------------------------------------------------------------------------
 * 2. INITIALIZE CANDIDATE CONTROL VECTOR FROM PREVIOUS CONTROL ACTION (WARM START)
 * --------------------------------------------------------------------------------------------------------------------- *)
FOR iMPC_Actuator := 1 TO 6 DO
    rVec_u_Optimized[iMPC_Actuator] := rVec_u_Previous[iMPC_Actuator];
END_FOR;

(* ---------------------------------------------------------------------------------------------------------------------
 * 3. UNROLLED PROJECTED GRADIENT DESCENT (PGD) ITERATIONS (6 CYCLES)
 * Objective: Minimize J(u) = (y - r)^T * Q * (y - r) + u^T * R * u + (u - u_prev)^T * S * (u - u_prev)
 * --------------------------------------------------------------------------------------------------------------------- *)
FOR iMPC_Iteration := 1 TO 6 DO

    (* Compute Cost Contributions for Telemetry and Diagnostics *)
    rMPC_Cost_Tracking := 0.0;
    FOR iRow_Idx := 1 TO 6 DO
        rMPC_Cost_Tracking := rMPC_Cost_Tracking + (rMPC_Weight_Q[iRow_Idx] * (rVec_y_Estimated[iRow_Idx] - rVec_r_Reference[iRow_Idx])
                                                    * (rVec_y_Estimated[iRow_Idx] - rVec_r_Reference[iRow_Idx]));
    END_FOR;

    rMPC_Cost_Effort := 0.0;
    rMPC_Cost_Slew := 0.0;
    FOR iMPC_Actuator := 1 TO 6 DO
        rMPC_Cost_Effort := rMPC_Cost_Effort + (rMPC_Weight_R[iMPC_Actuator] * rVec_u_Optimized[iMPC_Actuator] * rVec_u_Optimized[iMPC_Actuator]);
        rMPC_Cost_Slew := rMPC_Cost_Slew + (rMPC_Weight_S[iMPC_Actuator] * (rVec_u_Optimized[iMPC_Actuator] - rVec_u_Previous[iMPC_Actuator])
                                            * (rVec_u_Optimized[iMPC_Actuator] - rVec_u_Previous[iMPC_Actuator]));
    END_FOR;
    rMPC_Cost_Total := rMPC_Cost_Tracking + rMPC_Cost_Effort + rMPC_Cost_Slew;

    (* -----------------------------------------------------------------------------------------------------------------
     * ANALYTIC GRADIENT COMPUTATION: dJ/du_j
     * dJ/du_j = 2 * sum_i( Q_i * (y_i - r_i) * (dy_i / du_j) ) + 2 * R_j * u_j + 2 * S_j * (u_j - u_prev_j)
     * Sensitivity dy_i / du_j = G_ij = (C * B)_ij * dt
     * ----------------------------------------------------------------------------------------------------------------- *)
    (* Actuator 1: Main Shot Servo Valve Spool [%] *)
    rVec_u_Gradient[1] := (2.0 * rMPC_Weight_Q[1] * (rVec_y_Estimated[1] - rVec_r_Reference[1]) * 0.000050)
                        + (2.0 * rMPC_Weight_Q[2] * (rVec_y_Estimated[2] - rVec_r_Reference[2]) * 0.085000)
                        + (2.0 * rMPC_Weight_Q[3] * (rVec_y_Estimated[3] - rVec_r_Reference[3]) * 2.850000)
                        + (2.0 * rMPC_Weight_Q[4] * (rVec_y_Estimated[4] - rVec_r_Reference[4]) * -0.650000)
                        + (2.0 * rMPC_Weight_R[1] * rVec_u_Optimized[1])
                        + (2.0 * rMPC_Weight_S[1] * (rVec_u_Optimized[1] - rVec_u_Previous[1]));

    (* Actuator 2: High-Speed Dump Cartridge [%] *)
    rVec_u_Gradient[2] := (2.0 * rMPC_Weight_Q[2] * (rVec_y_Estimated[2] - rVec_r_Reference[2]) * 0.065000)
                        + (2.0 * rMPC_Weight_Q[3] * (rVec_y_Estimated[3] - rVec_r_Reference[3]) * 1.950000)
                        + (2.0 * rMPC_Weight_R[2] * rVec_u_Optimized[2])
                        + (2.0 * rMPC_Weight_S[2] * (rVec_u_Optimized[2] - rVec_u_Previous[2]));

    (* Actuator 3: Intensifier Spool Valve [%] *)
    rVec_u_Gradient[3] := (2.0 * rMPC_Weight_Q[2] * (rVec_y_Estimated[2] - rVec_r_Reference[2]) * 0.012000)
                        + (2.0 * rMPC_Weight_Q[3] * (rVec_y_Estimated[3] - rVec_r_Reference[3]) * 4.250000)
                        + (2.0 * rMPC_Weight_R[3] * rVec_u_Optimized[3])
                        + (2.0 * rMPC_Weight_S[3] * (rVec_u_Optimized[3] - rVec_u_Previous[3]));

    (* Actuator 4: Vacuum Isolation Valve [%] *)
    rVec_u_Gradient[4] := (2.0 * rMPC_Weight_Q[5] * (rVec_y_Estimated[5] - rVec_r_Reference[5]) * -1.850000)
                        + (2.0 * rMPC_Weight_R[4] * rVec_u_Optimized[4])
                        + (2.0 * rMPC_Weight_S[4] * (rVec_u_Optimized[4] - rVec_u_Previous[4]));

    (* Actuator 5: Clamping Line Pressure [bar] *)
    rVec_u_Gradient[5] := (2.0 * rMPC_Weight_R[5] * rVec_u_Optimized[5])
                        + (2.0 * rMPC_Weight_S[5] * (rVec_u_Optimized[5] - rVec_u_Previous[5]));

    (* Actuator 6: Die Cooling Flow [%] *)
    rVec_u_Gradient[6] := (2.0 * rMPC_Weight_Q[6] * (rVec_y_Estimated[6] - rVec_r_Reference[6]) * -0.054000)
                        + (2.0 * rMPC_Weight_R[6] * rVec_u_Optimized[6])
                        + (2.0 * rMPC_Weight_S[6] * (rVec_u_Optimized[6] - rVec_u_Previous[6]));

    (* -----------------------------------------------------------------------------------------------------------------
     * DESCENT STEP, BOX CONSTRAINT PROJECTION & HARD SLEW-RATE LIMITING
     * ----------------------------------------------------------------------------------------------------------------- *)
    FOR iMPC_Actuator := 1 TO 6 DO
        (* Gradient step *)
        rVec_u_Optimized[iMPC_Actuator] := rVec_u_Optimized[iMPC_Actuator] - (rMPC_StepSize_Alpha * rVec_u_Gradient[iMPC_Actuator]);

        (* Box Constraint Hard Projection *)
        IF rVec_u_Optimized[iMPC_Actuator] < rVec_u_MinLimit[iMPC_Actuator] THEN
            rVec_u_Optimized[iMPC_Actuator] := rVec_u_MinLimit[iMPC_Actuator];
        ELSIF rVec_u_Optimized[iMPC_Actuator] > rVec_u_MaxLimit[iMPC_Actuator] THEN
            rVec_u_Optimized[iMPC_Actuator] := rVec_u_MaxLimit[iMPC_Actuator];
        END_IF;

        (* Slew Rate Physical Valve Inertia Limiting (Per Millisecond) *)
        IF (rVec_u_Optimized[iMPC_Actuator] - rVec_u_Previous[iMPC_Actuator]) > rVec_du_MaxRate[iMPC_Actuator] THEN
            rVec_u_Optimized[iMPC_Actuator] := rVec_u_Previous[iMPC_Actuator] + rVec_du_MaxRate[iMPC_Actuator];
        ELSIF (rVec_u_Optimized[iMPC_Actuator] - rVec_u_Previous[iMPC_Actuator]) < -rVec_du_MaxRate[iMPC_Actuator] THEN
            rVec_u_Optimized[iMPC_Actuator] := rVec_u_Previous[iMPC_Actuator] - rVec_du_MaxRate[iMPC_Actuator];
        END_IF;
    END_FOR;

END_FOR;

(* ---------------------------------------------------------------------------------------------------------------------
 * 4. ASSIGN ACTUATOR ANALOG COMMAND OUTPUTS WITH MECHANICAL ANTI-STICTION DITHER
 * --------------------------------------------------------------------------------------------------------------------- *)
(* High-frequency dither (+/- 0.4% at 50 Hz, 20 ms cycle) to eliminate servo spool seal stiction *)
IF (iPWM_CycleCounter_ms MOD 20) < 10 THEN
    rServo_ShotSpool_Cmd_Out := rVec_u_Optimized[1] + 0.40;
ELSE
    rServo_ShotSpool_Cmd_Out := rVec_u_Optimized[1] - 0.40;
END_IF;

rFastValv_Cartridge_Cmd_Out := rVec_u_Optimized[2];
rIntensifier_Valve_Cmd_Out  := rVec_u_Optimized[3];
rVacuum_Isolation_Cmd_Out   := rVec_u_Optimized[4];
rClamp_Proportional_Cmd_Out := (rVec_u_Optimized[5] / 350.0) * 100.0; (* Scaled 0 to 100% *)

(* Store Optimized Solution for Next Control Loop *)
FOR iMPC_Actuator := 1 TO 6 DO
    rVec_u_Previous[iMPC_Actuator] := rVec_u_Optimized[iMPC_Actuator];
    rVec_u_Control[iMPC_Actuator]  := rVec_u_Optimized[iMPC_Actuator];
END_FOR;
"""
