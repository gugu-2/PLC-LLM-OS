# mega_casting_builder/build_phase3_state_space_observer.py

def get_phase3_state_space_observer():
    return """(* =====================================================================================================================
 * PHASE 3: FIRST-PRINCIPLES CYBER-PHYSICAL STATE-SPACE ESTIMATION & KALMAN INNOVATION OBSERVER
 * System order: 6 states, 6 inputs, 6 disturbances, 6 observations
 * Explicitly unrolled matrix-vector multiplications: zero truncation, zero helper function abstraction
 * ===================================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------------------------
 * 1. ASSEMBLE OBSERVATION VECTOR y[k] FROM 2oo3 TMR VOTED SENSORS
 * --------------------------------------------------------------------------------------------------------------------- *)
rOutput_y[1] := rPlungerPos_Voted;
rOutput_y[2] := rPlungerVel_Filtered;
rOutput_y[3] := rHeadPress_Voted;
rOutput_y[4] := rCavityPress_Voted;
rOutput_y[5] := rVacPressure_Voted;
rOutput_y[6] := (rTieBar_Strain_Ch1 + rTieBar_Strain_Ch2 + rTieBar_Strain_Ch3 + rTieBar_Strain_Ch4) * 0.25;

(* ---------------------------------------------------------------------------------------------------------------------
 * 2. ASSEMBLE ACTUATOR INPUT VECTOR u[k] FROM ACTUATOR COMMANDS
 * --------------------------------------------------------------------------------------------------------------------- *)
rInput_u[1] := rServoInjectionValve_Cmd;
rInput_u[2] := rAccumulatorPilotTrim_Cmd;
rInput_u[3] := rIntensificationValve_Cmd;
rInput_u[4] := rVacuumThrottle_Cmd;
rInput_u[5] := rThermalOil_Valve_Cmd;
rInput_u[6] := rToggleClampPilot_Cmd;

(* ---------------------------------------------------------------------------------------------------------------------
 * 3. ESTIMATE EXOGENOUS CYBER-PHYSICAL PROCESS DISTURBANCES w[k]
 * --------------------------------------------------------------------------------------------------------------------- *)
(* w1: Molten Aluminum Flow Rheological Resistance Perturbation *)
IF rLadle_Melt_Temp_Actual > 500.0 THEN
    rDisturbance_w[1] := (680.0 - rLadle_Melt_Temp_Actual) * 0.085; (* Viscosity increases as melt cools *)
ELSE
    rDisturbance_w[1] := 0.0;
END_IF;

(* w2: Wave Surge Crest Disturbance in Cold Chamber Sleeve *)
IF rPlungerVel_Filtered > 0.05 AND rPlungerVel_Filtered < 1.20 THEN
    rDisturbance_w[2] := (rPlungerVel_Filtered - rCritical_Wave_Velocity_ms) * 1.450;
ELSE
    rDisturbance_w[2] := 0.0;
END_IF;

(* w3: Acoustic Cavity Pressure Shockwave Reflection at Gate *)
rDisturbance_w[3] := rAcousticFillShock_bar_ms * 0.120;

(* w4: Parting Line Atmospheric Ingress Leakage Disturbance *)
rDisturbance_w[4] := rVac_LeakRate_Actual_mbar_s * 0.050;

(* w5: Accumulator High-Speed Polytropic Expansion Thermal Drop *)
rDisturbance_w[5] := - (rServoInjectionValve_Cmd * 0.025);

(* w6: Tie-Bar Asymmetric Thermal Growth Load *)
rDisturbance_w[6] := (rFixedDie_Temp_Actual - rMovingDie_Temp_Actual) * 0.015;

(* ---------------------------------------------------------------------------------------------------------------------
 * 4. DISCRETE STATE PREDICTION: x_model = A * x_hat[k] + B * u[k] + Ew * w[k]
 * Unrolled 6x6 matrix-vector multiplication
 * --------------------------------------------------------------------------------------------------------------------- *)
(* State 1: Plunger Linear Stroke Position x_p [mm] *)
rState_x_hat_next[1] := (rMatrix_A[1, 1] * rState_x_hat[1]) +
                        (rMatrix_A[1, 2] * rState_x_hat[2]) +
                        (rMatrix_A[1, 3] * rState_x_hat[3]) +
                        (rMatrix_A[1, 4] * rState_x_hat[4]) +
                        (rMatrix_A[1, 5] * rState_x_hat[5]) +
                        (rMatrix_A[1, 6] * rState_x_hat[6]) +
                        (rMatrix_B[1, 1] * rInput_u[1]) +
                        (rMatrix_B[1, 2] * rInput_u[2]) +
                        (rMatrix_B[1, 3] * rInput_u[3]) +
                        (rMatrix_B[1, 4] * rInput_u[4]) +
                        (rMatrix_B[1, 5] * rInput_u[5]) +
                        (rMatrix_B[1, 6] * rInput_u[6]) +
                        (rMatrix_Ew[1, 1] * rDisturbance_w[1]) +
                        (rMatrix_Ew[1, 2] * rDisturbance_w[2]) +
                        (rMatrix_Ew[1, 3] * rDisturbance_w[3]) +
                        (rMatrix_Ew[1, 4] * rDisturbance_w[4]) +
                        (rMatrix_Ew[1, 5] * rDisturbance_w[5]) +
                        (rMatrix_Ew[1, 6] * rDisturbance_w[6]);

(* State 2: Plunger Axial Velocity v_p [m/s] *)
rState_x_hat_next[2] := (rMatrix_A[2, 1] * rState_x_hat[1]) +
                        (rMatrix_A[2, 2] * rState_x_hat[2]) +
                        (rMatrix_A[2, 3] * rState_x_hat[3]) +
                        (rMatrix_A[2, 4] * rState_x_hat[4]) +
                        (rMatrix_A[2, 5] * rState_x_hat[5]) +
                        (rMatrix_A[2, 6] * rState_x_hat[6]) +
                        (rMatrix_B[2, 1] * rInput_u[1]) +
                        (rMatrix_B[2, 2] * rInput_u[2]) +
                        (rMatrix_B[2, 3] * rInput_u[3]) +
                        (rMatrix_B[2, 4] * rInput_u[4]) +
                        (rMatrix_B[2, 5] * rInput_u[5]) +
                        (rMatrix_B[2, 6] * rInput_u[6]) +
                        (rMatrix_Ew[2, 1] * rDisturbance_w[1]) +
                        (rMatrix_Ew[2, 2] * rDisturbance_w[2]) +
                        (rMatrix_Ew[2, 3] * rDisturbance_w[3]) +
                        (rMatrix_Ew[2, 4] * rDisturbance_w[4]) +
                        (rMatrix_Ew[2, 5] * rDisturbance_w[5]) +
                        (rMatrix_Ew[2, 6] * rDisturbance_w[6]);

(* State 3: Injection Cylinder Head Chamber Hydraulic Pressure P_head [bar] *)
rState_x_hat_next[3] := (rMatrix_A[3, 1] * rState_x_hat[1]) +
                        (rMatrix_A[3, 2] * rState_x_hat[2]) +
                        (rMatrix_A[3, 3] * rState_x_hat[3]) +
                        (rMatrix_A[3, 4] * rState_x_hat[4]) +
                        (rMatrix_A[3, 5] * rState_x_hat[5]) +
                        (rMatrix_A[3, 6] * rState_x_hat[6]) +
                        (rMatrix_B[3, 1] * rInput_u[1]) +
                        (rMatrix_B[3, 2] * rInput_u[2]) +
                        (rMatrix_B[3, 3] * rInput_u[3]) +
                        (rMatrix_B[3, 4] * rInput_u[4]) +
                        (rMatrix_B[3, 5] * rInput_u[5]) +
                        (rMatrix_B[3, 6] * rInput_u[6]) +
                        (rMatrix_Ew[3, 1] * rDisturbance_w[1]) +
                        (rMatrix_Ew[3, 2] * rDisturbance_w[2]) +
                        (rMatrix_Ew[3, 3] * rDisturbance_w[3]) +
                        (rMatrix_Ew[3, 4] * rDisturbance_w[4]) +
                        (rMatrix_Ew[3, 5] * rDisturbance_w[5]) +
                        (rMatrix_Ew[3, 6] * rDisturbance_w[6]);

(* State 4: Molten Aluminum In-Cavity Dynamic Pressure P_cavity [bar] *)
rState_x_hat_next[4] := (rMatrix_A[4, 1] * rState_x_hat[1]) +
                        (rMatrix_A[4, 2] * rState_x_hat[2]) +
                        (rMatrix_A[4, 3] * rState_x_hat[3]) +
                        (rMatrix_A[4, 4] * rState_x_hat[4]) +
                        (rMatrix_A[4, 5] * rState_x_hat[5]) +
                        (rMatrix_A[4, 6] * rState_x_hat[6]) +
                        (rMatrix_B[4, 1] * rInput_u[1]) +
                        (rMatrix_B[4, 2] * rInput_u[2]) +
                        (rMatrix_B[4, 3] * rInput_u[3]) +
                        (rMatrix_B[4, 4] * rInput_u[4]) +
                        (rMatrix_B[4, 5] * rInput_u[5]) +
                        (rMatrix_B[4, 6] * rInput_u[6]) +
                        (rMatrix_Ew[4, 1] * rDisturbance_w[1]) +
                        (rMatrix_Ew[4, 2] * rDisturbance_w[2]) +
                        (rMatrix_Ew[4, 3] * rDisturbance_w[3]) +
                        (rMatrix_Ew[4, 4] * rDisturbance_w[4]) +
                        (rMatrix_Ew[4, 5] * rDisturbance_w[5]) +
                        (rMatrix_Ew[4, 6] * rDisturbance_w[6]);

(* State 5: Parting Plane Vacuum Evacuation Absolute Pressure P_vac [mbar] *)
rState_x_hat_next[5] := (rMatrix_A[5, 1] * rState_x_hat[1]) +
                        (rMatrix_A[5, 2] * rState_x_hat[2]) +
                        (rMatrix_A[5, 3] * rState_x_hat[3]) +
                        (rMatrix_A[5, 4] * rState_x_hat[4]) +
                        (rMatrix_A[5, 5] * rState_x_hat[5]) +
                        (rMatrix_A[5, 6] * rState_x_hat[6]) +
                        (rMatrix_B[5, 1] * rInput_u[1]) +
                        (rMatrix_B[5, 2] * rInput_u[2]) +
                        (rMatrix_B[5, 3] * rInput_u[3]) +
                        (rMatrix_B[5, 4] * rInput_u[4]) +
                        (rMatrix_B[5, 5] * rInput_u[5]) +
                        (rMatrix_B[5, 6] * rInput_u[6]) +
                        (rMatrix_Ew[5, 1] * rDisturbance_w[1]) +
                        (rMatrix_Ew[5, 2] * rDisturbance_w[2]) +
                        (rMatrix_Ew[5, 3] * rDisturbance_w[3]) +
                        (rMatrix_Ew[5, 4] * rDisturbance_w[4]) +
                        (rMatrix_Ew[5, 5] * rDisturbance_w[5]) +
                        (rMatrix_Ew[5, 6] * rDisturbance_w[6]);

(* State 6: Clamping Tie-Bar Dynamic Elastic Strain Stretch [um] *)
rState_x_hat_next[6] := (rMatrix_A[6, 1] * rState_x_hat[1]) +
                        (rMatrix_A[6, 2] * rState_x_hat[2]) +
                        (rMatrix_A[6, 3] * rState_x_hat[3]) +
                        (rMatrix_A[6, 4] * rState_x_hat[4]) +
                        (rMatrix_A[6, 5] * rState_x_hat[5]) +
                        (rMatrix_A[6, 6] * rState_x_hat[6]) +
                        (rMatrix_B[6, 1] * rInput_u[1]) +
                        (rMatrix_B[6, 2] * rInput_u[2]) +
                        (rMatrix_B[6, 3] * rInput_u[3]) +
                        (rMatrix_B[6, 4] * rInput_u[4]) +
                        (rMatrix_B[6, 5] * rInput_u[5]) +
                        (rMatrix_B[6, 6] * rInput_u[6]) +
                        (rMatrix_Ew[6, 1] * rDisturbance_w[1]) +
                        (rMatrix_Ew[6, 2] * rDisturbance_w[2]) +
                        (rMatrix_Ew[6, 3] * rDisturbance_w[3]) +
                        (rMatrix_Ew[6, 4] * rDisturbance_w[4]) +
                        (rMatrix_Ew[6, 5] * rDisturbance_w[5]) +
                        (rMatrix_Ew[6, 6] * rDisturbance_w[6]);

(* ---------------------------------------------------------------------------------------------------------------------
 * 5. MEASUREMENT PREDICTION: y_hat = C * x_hat_next + D * u
 * --------------------------------------------------------------------------------------------------------------------- *)
FOR i_idx := 1 TO 6 DO
    rOutput_y_hat[i_idx] := (rMatrix_C[i_idx, 1] * rState_x_hat_next[1]) +
                            (rMatrix_C[i_idx, 2] * rState_x_hat_next[2]) +
                            (rMatrix_C[i_idx, 3] * rState_x_hat_next[3]) +
                            (rMatrix_C[i_idx, 4] * rState_x_hat_next[4]) +
                            (rMatrix_C[i_idx, 5] * rState_x_hat_next[5]) +
                            (rMatrix_C[i_idx, 6] * rState_x_hat_next[6]) +
                            (rMatrix_D[i_idx, 1] * rInput_u[1]) +
                            (rMatrix_D[i_idx, 2] * rInput_u[2]) +
                            (rMatrix_D[i_idx, 3] * rInput_u[3]) +
                            (rMatrix_D[i_idx, 4] * rInput_u[4]) +
                            (rMatrix_D[i_idx, 5] * rInput_u[5]) +
                            (rMatrix_D[i_idx, 6] * rInput_u[6]);

    (* Innovation Residual Calculation: e_y = y - y_hat *)
    rInnovation_Residual[i_idx] := rOutput_y[i_idx] - rOutput_y_hat[i_idx];
END_FOR;

(* ---------------------------------------------------------------------------------------------------------------------
 * 6. OBSERVER INNOVATION CORRECTION: x_hat = x_hat_next + L * (y - y_hat)
 * --------------------------------------------------------------------------------------------------------------------- *)
FOR i_idx := 1 TO 6 DO
    rState_x_hat[i_idx] := rState_x_hat_next[i_idx] +
                           (rMatrix_L[i_idx, 1] * rInnovation_Residual[1]) +
                           (rMatrix_L[i_idx, 2] * rInnovation_Residual[2]) +
                           (rMatrix_L[i_idx, 3] * rInnovation_Residual[3]) +
                           (rMatrix_L[i_idx, 4] * rInnovation_Residual[4]) +
                           (rMatrix_L[i_idx, 5] * rInnovation_Residual[5]) +
                           (rMatrix_L[i_idx, 6] * rInnovation_Residual[6]);
END_FOR;

(* Copy estimated states to internal physical state vector for monitoring *)
FOR i_idx := 1 TO 6 DO
    rState_x[i_idx] := rState_x_hat[i_idx];
END_FOR;
"""
