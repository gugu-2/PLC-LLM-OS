# pharma_tableting_builder/part4_state_space_mpc.py

def get_part4():
    return """(* === PHASE 2: FIRST-PRINCIPLES CYBER-PHYSICAL STATE-SPACE ESTIMATION & LUENBERGER OBSERVER === *)

(* 1. Assemble Sensor Observation Measurement Vector y_meas (8x1) *)
y_meas[1] := rVotedFeederFlow_kgh;
y_meas[2] := (rBinderPumpActualFlow_gpmin / MAX(0.001, (rVotedFeederFlow_kgh * (1000.0 / 60.0)))) * 100.0;
y_meas[3] := 285.0 + 12.50 * (y_meas[2] - 10.50) - 0.045 * (rGranulatorScrewSpeed_rpm - 450.0);
y_meas[4] := rVotedMoistureLOD_pct;
y_meas[5] := rFluidBedInletAirTemp_degC;
y_meas[6] := rVotedTurretSpeed_rpm;
y_meas[7] := rVotedMainCompForce_kN;
y_meas[8] := (2.0 * rVotedMainCompForce_kN * 1000.0 * 0.0038) / (PI_CONST * rPunchDiameter_mm * rTabletNominalThickness_mm) * 100.0;

(* 2. Formulate Physical Disturbance Vector d_dist (4x1) *)
d_dist[1] := (rDieTableTemperature_degC - 25.0) * 0.0045;
d_dist[2] := (rFluidBedExhaustAirTemp_degC - 35.0) * 0.0185;
d_dist[3] := (rBinderDeliveryPressure_bar - 1.50) * 0.0850;
d_dist[4] := (rTabletEjectionForce_N - 180.0) * 0.0018;

(* 3. Explicit Term-by-Term Unrolled State-Space Propagation: x_pred = A*x + B*u + E*d *)
x_pred[1] := (a_mat[1,1] * x_state[1] + a_mat[1,2] * x_state[2] + a_mat[1,3] * x_state[3] + a_mat[1,4] * x_state[4] +
              a_mat[1,5] * x_state[5] + a_mat[1,6] * x_state[6] + a_mat[1,7] * x_state[7] + a_mat[1,8] * x_state[8]) +
             (b_mat[1,1] * u_ctrl[1] + b_mat[1,2] * u_ctrl[2] + b_mat[1,3] * u_ctrl[3] + b_mat[1,4] * u_ctrl[4] +
              b_mat[1,5] * u_ctrl[5] + b_mat[1,6] * u_ctrl[6] + b_mat[1,7] * u_ctrl[7] + b_mat[1,8] * u_ctrl[8]) +
             (e_mat[1,1] * d_dist[1] + e_mat[1,2] * d_dist[2] + e_mat[1,3] * d_dist[3] + e_mat[1,4] * d_dist[4]);

x_pred[2] := (a_mat[2,1] * x_state[1] + a_mat[2,2] * x_state[2] + a_mat[2,3] * x_state[3] + a_mat[2,4] * x_state[4] +
              a_mat[2,5] * x_state[5] + a_mat[2,6] * x_state[6] + a_mat[2,7] * x_state[7] + a_mat[2,8] * x_state[8]) +
             (b_mat[2,1] * u_ctrl[1] + b_mat[2,2] * u_ctrl[2] + b_mat[2,3] * u_ctrl[3] + b_mat[2,4] * u_ctrl[4] +
              b_mat[2,5] * u_ctrl[5] + b_mat[2,6] * u_ctrl[6] + b_mat[2,7] * u_ctrl[7] + b_mat[2,8] * u_ctrl[8]) +
             (e_mat[2,1] * d_dist[1] + e_mat[2,2] * d_dist[2] + e_mat[2,3] * d_dist[3] + e_mat[2,4] * d_dist[4]);

x_pred[3] := (a_mat[3,1] * x_state[1] + a_mat[3,2] * x_state[2] + a_mat[3,3] * x_state[3] + a_mat[3,4] * x_state[4] +
              a_mat[3,5] * x_state[5] + a_mat[3,6] * x_state[6] + a_mat[3,7] * x_state[7] + a_mat[3,8] * x_state[8]) +
             (b_mat[3,1] * u_ctrl[1] + b_mat[3,2] * u_ctrl[2] + b_mat[3,3] * u_ctrl[3] + b_mat[3,4] * u_ctrl[4] +
              b_mat[3,5] * u_ctrl[5] + b_mat[3,6] * u_ctrl[6] + b_mat[3,7] * u_ctrl[7] + b_mat[3,8] * u_ctrl[8]) +
             (e_mat[3,1] * d_dist[1] + e_mat[3,2] * d_dist[2] + e_mat[3,3] * d_dist[3] + e_mat[3,4] * d_dist[4]);

x_pred[4] := (a_mat[4,1] * x_state[1] + a_mat[4,2] * x_state[2] + a_mat[4,3] * x_state[3] + a_mat[4,4] * x_state[4] +
              a_mat[4,5] * x_state[5] + a_mat[4,6] * x_state[6] + a_mat[4,7] * x_state[7] + a_mat[4,8] * x_state[8]) +
             (b_mat[4,1] * u_ctrl[1] + b_mat[4,2] * u_ctrl[2] + b_mat[4,3] * u_ctrl[3] + b_mat[4,4] * u_ctrl[4] +
              b_mat[4,5] * u_ctrl[5] + b_mat[4,6] * u_ctrl[6] + b_mat[4,7] * u_ctrl[7] + b_mat[4,8] * u_ctrl[8]) +
             (e_mat[4,1] * d_dist[1] + e_mat[4,2] * d_dist[2] + e_mat[4,3] * d_dist[3] + e_mat[4,4] * d_dist[4]);

x_pred[5] := (a_mat[5,1] * x_state[1] + a_mat[5,2] * x_state[2] + a_mat[5,3] * x_state[3] + a_mat[5,4] * x_state[4] +
              a_mat[5,5] * x_state[5] + a_mat[5,6] * x_state[6] + a_mat[5,7] * x_state[7] + a_mat[5,8] * x_state[8]) +
             (b_mat[5,1] * u_ctrl[1] + b_mat[5,2] * u_ctrl[2] + b_mat[5,3] * u_ctrl[3] + b_mat[5,4] * u_ctrl[4] +
              b_mat[5,5] * u_ctrl[5] + b_mat[5,6] * u_ctrl[6] + b_mat[5,7] * u_ctrl[7] + b_mat[5,8] * u_ctrl[8]) +
             (e_mat[5,1] * d_dist[1] + e_mat[5,2] * d_dist[2] + e_mat[5,3] * d_dist[3] + e_mat[5,4] * d_dist[4]);

x_pred[6] := (a_mat[6,1] * x_state[1] + a_mat[6,2] * x_state[2] + a_mat[6,3] * x_state[3] + a_mat[6,4] * x_state[4] +
              a_mat[6,5] * x_state[5] + a_mat[6,6] * x_state[6] + a_mat[6,7] * x_state[7] + a_mat[6,8] * x_state[8]) +
             (b_mat[6,1] * u_ctrl[1] + b_mat[6,2] * u_ctrl[2] + b_mat[6,3] * u_ctrl[3] + b_mat[6,4] * u_ctrl[4] +
              b_mat[6,5] * u_ctrl[5] + b_mat[6,6] * u_ctrl[6] + b_mat[6,7] * u_ctrl[7] + b_mat[6,8] * u_ctrl[8]) +
             (e_mat[6,1] * d_dist[1] + e_mat[6,2] * d_dist[2] + e_mat[6,3] * d_dist[3] + e_mat[6,4] * d_dist[4]);

x_pred[7] := (a_mat[7,1] * x_state[1] + a_mat[7,2] * x_state[2] + a_mat[7,3] * x_state[3] + a_mat[7,4] * x_state[4] +
              a_mat[7,5] * x_state[5] + a_mat[7,6] * x_state[6] + a_mat[7,7] * x_state[7] + a_mat[7,8] * x_state[8]) +
             (b_mat[7,1] * u_ctrl[1] + b_mat[7,2] * u_ctrl[2] + b_mat[7,3] * u_ctrl[3] + b_mat[7,4] * u_ctrl[4] +
              b_mat[7,5] * u_ctrl[5] + b_mat[7,6] * u_ctrl[6] + b_mat[7,7] * u_ctrl[7] + b_mat[7,8] * u_ctrl[8]) +
             (e_mat[7,1] * d_dist[1] + e_mat[7,2] * d_dist[2] + e_mat[7,3] * d_dist[3] + e_mat[7,4] * d_dist[4]);

x_pred[8] := (a_mat[8,1] * x_state[1] + a_mat[8,2] * x_state[2] + a_mat[8,3] * x_state[3] + a_mat[8,4] * x_state[4] +
              a_mat[8,5] * x_state[5] + a_mat[8,6] * x_state[6] + a_mat[8,7] * x_state[7] + a_mat[8,8] * x_state[8]) +
             (b_mat[8,1] * u_ctrl[1] + b_mat[8,2] * u_ctrl[2] + b_mat[8,3] * u_ctrl[3] + b_mat[8,4] * u_ctrl[4] +
              b_mat[8,5] * u_ctrl[5] + b_mat[8,6] * u_ctrl[6] + b_mat[8,7] * u_ctrl[7] + b_mat[8,8] * u_ctrl[8]) +
             (e_mat[8,1] * d_dist[1] + e_mat[8,2] * d_dist[2] + e_mat[8,3] * d_dist[3] + e_mat[8,4] * d_dist[4]);

(* 4. Luenberger Observer Correction: x_state = x_pred + L * (y_meas - x_pred) *)
x_state[1] := x_pred[1] + l_observer[1] * (y_meas[1] - x_pred[1]);
x_state[2] := x_pred[2] + l_observer[2] * (y_meas[2] - x_pred[2]);
x_state[3] := x_pred[3] + l_observer[3] * (y_meas[3] - x_pred[3]);
x_state[4] := x_pred[4] + l_observer[4] * (y_meas[4] - x_pred[4]);
x_state[5] := x_pred[5] + l_observer[5] * (y_meas[5] - x_pred[5]);
x_state[6] := x_pred[6] + l_observer[6] * (y_meas[6] - x_pred[6]);
x_state[7] := x_pred[7] + l_observer[7] * (y_meas[7] - x_pred[7]);
x_state[8] := x_pred[8] + l_observer[8] * (y_meas[8] - x_pred[8]);

(* Export Observer Estimates to Outputs *)
rObservedLiquidSolidRatio_pct := x_state[2];
rObservedGranuleMedianD50_um := x_state[3];
rObservedTabletHardness_N := x_state[8];
rObservedTabletWeight_mg := rRecipeTargetTabletWeight_mg + (x_state[7] - rRecipeTargetMainCompForce_kN) * 3.820;
rObservedTabletProductionRate_tph := x_state[6] * 48.0 * 60.0;


(* === PHASE 3: RECEDING-HORIZON MPC OPTIMIZATION WITH PGD & SLEW LIMITS === *)

(* 1. Reference State Trajectory Setup *)
x_ref[1] := rRecipeTargetFeederFlow_kgh;
x_ref[2] := rRecipeTargetLiquidSolidRatio_pct;
x_ref[3] := 285.00; (* Target Granule Median Size 285 um *)
x_ref[4] := rRecipeTargetMoistureLOD_pct;
x_ref[5] := rRecipeTargetFluidBedTemp_degC;
x_ref[6] := rRecipeTargetTurretSpeed_rpm;
x_ref[7] := rRecipeTargetMainCompForce_kN;
x_ref[8] := rRecipeTargetTabletHardness_N;

(* 2. Nominal Actuator Baseline Computation *)
u_ref[1] := 32.50 * (rRecipeTargetFeederFlow_kgh / 25.0);
u_ref[2] := (rRecipeTargetFeederFlow_kgh * (1000.0 / 60.0)) * (rRecipeTargetLiquidSolidRatio_pct / 100.0);
u_ref[3] := rRecipeTargetScrewSpeed_rpm;
u_ref[4] := 48.50 * (rRecipeTargetFluidBedTemp_degC / 58.0);
u_ref[5] := 62.00 * (rRecipeTargetFluidBedAirVel_mps / 1.45);
u_ref[6] := rRecipeTargetTurretSpeed_rpm;
u_ref[7] := 65.00 * (rRecipeTargetTurretSpeed_rpm / 86.80);
u_ref[8] := 5.20 + (rRecipeTargetTabletWeight_mg - 250.0) * 0.025;

(* 3. Multi-Iteration Projected Gradient Descent (PGD) *)
FOR iter := 1 TO 3 DO
    (* Gradient Evaluation for Actuators 1 to 8 *)
    grad_u[1] := 2.0 * r_diag[1] * (u_ctrl[1] - u_ref[1]) + 2.0 * s_diag[1] * (u_ctrl[1] - u_prev[1]) +
                 2.0 * b_mat[1,1] * (q_diag[1] + p_diag[1]) * (x_pred[1] - x_ref[1]) +
                 2.0 * b_mat[2,1] * (q_diag[2] + p_diag[2]) * (x_pred[2] - x_ref[2]);

    grad_u[2] := 2.0 * r_diag[2] * (u_ctrl[2] - u_ref[2]) + 2.0 * s_diag[2] * (u_ctrl[2] - u_prev[2]) +
                 2.0 * b_mat[2,2] * (q_diag[2] + p_diag[2]) * (x_pred[2] - x_ref[2]) +
                 2.0 * b_mat[3,2] * (q_diag[3] + p_diag[3]) * (x_pred[3] - x_ref[3]) +
                 2.0 * b_mat[4,2] * (q_diag[4] + p_diag[4]) * (x_pred[4] - x_ref[4]);

    grad_u[3] := 2.0 * r_diag[3] * (u_ctrl[3] - u_ref[3]) + 2.0 * s_diag[3] * (u_ctrl[3] - u_prev[3]) +
                 2.0 * b_mat[3,3] * (q_diag[3] + p_diag[3]) * (x_pred[3] - x_ref[3]);

    grad_u[4] := 2.0 * r_diag[4] * (u_ctrl[4] - u_ref[4]) + 2.0 * s_diag[4] * (u_ctrl[4] - u_prev[4]) +
                 2.0 * b_mat[4,4] * (q_diag[4] + p_diag[4]) * (x_pred[4] - x_ref[4]) +
                 2.0 * b_mat[5,4] * (q_diag[5] + p_diag[5]) * (x_pred[5] - x_ref[5]);

    grad_u[5] := 2.0 * r_diag[5] * (u_ctrl[5] - u_ref[5]) + 2.0 * s_diag[5] * (u_ctrl[5] - u_prev[5]) +
                 2.0 * b_mat[4,5] * (q_diag[4] + p_diag[4]) * (x_pred[4] - x_ref[4]) +
                 2.0 * b_mat[5,5] * (q_diag[5] + p_diag[5]) * (x_pred[5] - x_ref[5]);

    grad_u[6] := 2.0 * r_diag[6] * (u_ctrl[6] - u_ref[6]) + 2.0 * s_diag[6] * (u_ctrl[6] - u_prev[6]) +
                 2.0 * b_mat[6,6] * (q_diag[6] + p_diag[6]) * (x_pred[6] - x_ref[6]) +
                 2.0 * b_mat[7,6] * (q_diag[7] + p_diag[7]) * (x_pred[7] - x_ref[7]);

    grad_u[7] := 2.0 * r_diag[7] * (u_ctrl[7] - u_ref[7]) + 2.0 * s_diag[7] * (u_ctrl[7] - u_prev[7]) +
                 2.0 * b_mat[7,7] * (q_diag[7] + p_diag[7]) * (x_pred[7] - x_ref[7]) +
                 2.0 * b_mat[8,7] * (q_diag[8] + p_diag[8]) * (x_pred[8] - x_ref[8]);

    grad_u[8] := 2.0 * r_diag[8] * (u_ctrl[8] - u_ref[8]) + 2.0 * s_diag[8] * (u_ctrl[8] - u_prev[8]) +
                 2.0 * b_mat[7,8] * (q_diag[7] + p_diag[7]) * (x_pred[7] - x_ref[7]) +
                 2.0 * b_mat[8,8] * (q_diag[8] + p_diag[8]) * (x_pred[8] - x_ref[8]);

    (* Projected Gradient Descent Step with Physical Box Saturation & Slew Limiting *)
    FOR k := 1 TO 8 DO
        u_tentative[k] := u_ctrl[k] - rMpcStepSize * grad_u[k];
        
        (* Box Constraint Projection *)
        IF u_tentative[k] < u_min[k] THEN
            u_tentative[k] := u_min[k];
        ELSIF u_tentative[k] > u_max[k] THEN
            u_tentative[k] := u_max[k];
        END_IF;

        (* Slew Rate Clamping *)
        IF (u_tentative[k] - u_prev[k]) > du_max[k] THEN
            u_tentative[k] := u_prev[k] + du_max[k];
        ELSIF (u_prev[k] - u_tentative[k]) > du_max[k] THEN
            u_tentative[k] := u_prev[k] - du_max[k];
        END_IF;

        u_ctrl[k] := u_tentative[k];
    END_FOR;
END_FOR;

(* Store Previous Control Vector for Slew Limiter on Next PLC Cycle *)
FOR k := 1 TO 8 DO
    u_prev[k] := u_ctrl[k];
END_FOR;

(* Map Optimized Control Vectors to Primary Hardware Outputs *)
rFeederMotorSpeedCommand_Hz := u_ctrl[1];
rBinderPumpFlowCommand_gpmin := u_ctrl[2];
rGranulatorScrewSpeedCommand_rpm := u_ctrl[3];
rFluidBedHeaterDuty_pct := u_ctrl[4];
rFluidBedAirFlowVelocity_pct := u_ctrl[5];
rTurretDriveSpeedCommand_rpm := u_ctrl[6];
rFeederShoePaddleSpeedCommand_rpm := u_ctrl[7];
rLowerPunchDosingCamCommand_mm := u_ctrl[8];
"""
