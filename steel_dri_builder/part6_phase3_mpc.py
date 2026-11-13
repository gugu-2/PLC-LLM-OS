# steel_dri_builder/part6_phase3_mpc.py
"""
Part 6: Phase 3 - Receding-Horizon Model Predictive Control (MPC) with Projected Gradient Descent (PGD)
"""

def get_phase3_mpc():
    return """(* ==================================================================================================== *)
(* PHASE 3: RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) WITH PROJECTED GRADIENT DESCENT (PGD)       *)
(* ==================================================================================================== *)

(* 3.1 Setup Dynamic Reference Trajectory Vector x_Ref[1..8] *)
x_Ref[1] := rSP_BustleTemp;     (* 950.0 deg C Bustle Gas Temp *)
x_Ref[2] := rSP_Metallization;    (* 95.0 % Fe DRI Reduction Degree *)
IF rPV_ShaftDP_Voted > 72.0 THEN
    x_Ref[3] := 48.0;             (* Lower target DP to relieve sticking burden *)
ELSE
    x_Ref[3] := 52.0;             (* Nominal Shaft DP 52.0 kPa *)
END_IF;
x_Ref[4] := rSP_TopGasH2CO;       (* 2.85 H2/CO Ratio Setpoint *)
x_Ref[5] := 14.8;                 (* Optimal Top Gas CO2 % vol *)
x_Ref[6] := rSP_ProductCarbon;    (* 2.20 wt% C Target Carburization *)
x_Ref[7] := 65.0;                 (* 65.0 deg C Cooling Zone Bottom Gas *)
x_Ref[8] := rSP_DischargeRate;    (* 150.0 t/h Discharge Feeder Extraction *)

(* 3.2 Determine MPC Closed-Loop Permissive *)
bMPC_OptimalActive := bEnable AND bAutoMode AND (NOT bEmergencyStop) AND
                      (iState = 6 OR iState = 7 OR iState = 9);

IF bMPC_OptimalActive THEN
    (* 3.3 Dynamic Decoupling Feedforward References *)
    (* Hydrogen injection requires simultaneous preheater fuel increase to offset endothermic Delta H *)
    u_Ref[1] := 45.0 + ((x_Ref[4] - 2.50) * 18.0);
    u_Ref[2] := 55.0 - ((x_Ref[4] - 2.50) * 12.0);
    u_Ref[3] := 60.0 + ((x_Ref[1] - 920.0) * 0.45) + (u_Ref[1] * 0.22);
    u_Ref[4] := 18.0 + ((x_Ref[6] - 2.00) * 22.0);
    u_Ref[5] := 75.0 + ((rPV_DRITemp_Voted - 650.0) * 0.15);
    u_Ref[6] := (x_Ref[8] / 150.0) * 65.0;

    (* 3.4 Projected Gradient Descent (PGD) Unrolled Optimization (6 Iterations) *)
    FOR idx_iter := 1 TO 6 DO
        (* Step A: Forward State Trajectory Simulation Over Horizon N = 5 *)
        (* Step 1 of 5 *)
        FOR idx_i := 1 TO 8 DO
            rTempSum := 0.0;
            FOR idx_j := 1 TO 8 DO
                rTempSum := rTempSum + (matA[idx_i, idx_j] * x_Hat[idx_j]);
            END_FOR;
            FOR idx_k := 1 TO 6 DO
                rTempSum := rTempSum + (matB[idx_i, idx_k] * u_MPC_Trajectory[1, idx_k]);
            END_FOR;
            x_MPC_Predict[1, idx_i] := rTempSum;
        END_FOR;

        (* Steps 2 to 5 of 5 *)
        FOR idx_n := 2 TO 5 DO
            FOR idx_i := 1 TO 8 DO
                rTempSum := 0.0;
                FOR idx_j := 1 TO 8 DO
                    rTempSum := rTempSum + (matA[idx_i, idx_j] * x_MPC_Predict[idx_n - 1, idx_j]);
                END_FOR;
                FOR idx_k := 1 TO 6 DO
                    rTempSum := rTempSum + (matB[idx_i, idx_k] * u_MPC_Trajectory[idx_n, idx_k]);
                END_FOR;
                x_MPC_Predict[idx_n, idx_i] := rTempSum;
            END_FOR;
        END_FOR;

        (* Step B: Compute Objective Cost Function J *)
        rPV_MPC_CostFunctionJ := 0.0;
        FOR idx_n := 1 TO 4 DO
            FOR idx_i := 1 TO 8 DO
                rPV_MPC_CostFunctionJ := rPV_MPC_CostFunctionJ + (matQ[idx_i, idx_i] * (x_MPC_Predict[idx_n, idx_i] - x_Ref[idx_i]) * (x_MPC_Predict[idx_n, idx_i] - x_Ref[idx_i]));
            END_FOR;
            FOR idx_j := 1 TO 6 DO
                rPV_MPC_CostFunctionJ := rPV_MPC_CostFunctionJ + (matR[idx_j, idx_j] * (u_MPC_Trajectory[idx_n, idx_j] - u_Ref[idx_j]) * (u_MPC_Trajectory[idx_n, idx_j] - u_Ref[idx_j]));
            END_FOR;
        END_FOR;
        (* Terminal Stage 5 Penalty P *)
        FOR idx_i := 1 TO 8 DO
            rPV_MPC_CostFunctionJ := rPV_MPC_CostFunctionJ + (matP[idx_i, idx_i] * (x_MPC_Predict[5, idx_i] - x_Ref[idx_i]) * (x_MPC_Predict[5, idx_i] - x_Ref[idx_i]));
        END_FOR;

        (* Step C: Compute Analytical Gradient Vectors Over Horizon grad_MPC[n, j] *)
        FOR idx_n := 1 TO 5 DO
            FOR idx_j := 1 TO 6 DO
                (* Actuator effort component *)
                rGradSum := 2.0 * matR[idx_j, idx_j] * (u_MPC_Trajectory[idx_n, idx_j] - u_Ref[idx_j]);

                (* State-tracking backpropagation component *)
                FOR idx_h := idx_n TO 5 DO
                    FOR idx_i := 1 TO 8 DO
                        IF idx_h = 5 THEN
                            rGradSum := rGradSum + (2.0 * matB[idx_i, idx_j] * matP[idx_i, idx_i] * (x_MPC_Predict[idx_h, idx_i] - x_Ref[idx_i]));
                        ELSE
                            rGradSum := rGradSum + (2.0 * matB[idx_i, idx_j] * matQ[idx_i, idx_i] * (x_MPC_Predict[idx_h, idx_i] - x_Ref[idx_i]));
                        END_IF;
                    END_FOR;
                END_FOR;

                (* Decoupled Thermal Compensation Cross-Gradients *)
                IF idx_j = 1 THEN
                    (* Green H2 injection requires negative gradient bias for temperature drop *)
                    rGradSum := rGradSum + (rMPC_Lambda_H2Syngas * (x_MPC_Predict[idx_n, 1] - x_Ref[1]) * (-0.125));
                ELSIF idx_j = 3 THEN
                    (* Preheater fuel gas requires positive gradient bias for temperature compensation *)
                    rGradSum := rGradSum + (rMPC_Lambda_H2Syngas * (x_MPC_Predict[idx_n, 1] - x_Ref[1]) * 0.285);
                ELSIF idx_j = 4 THEN
                    (* Natural gas trim gradient coupled to carbon setpoint and temperature cooling *)
                    rGradSum := rGradSum + (rMPC_Lambda_CarbDep * (x_MPC_Predict[idx_n, 6] - x_Ref[6]) * 0.450);
                ELSIF idx_j = 6 THEN
                    (* Feeder speed gradient coupled to shaft DP relief and metallization *)
                    IF x_MPC_Predict[idx_n, 3] > 70.0 THEN
                        rGradSum := rGradSum - (1.85 * (x_MPC_Predict[idx_n, 3] - 70.0));
                    END_IF;
                END_IF;

                grad_MPC[idx_n, idx_j] := rGradSum;
            END_FOR;
        END_FOR;

        (* Step D: Projected Gradient Descent Update & Constraint Enforcement *)
        FOR idx_n := 1 TO 5 DO
            FOR idx_j := 1 TO 6 DO
                rPGD_ProjVal := u_MPC_Trajectory[idx_n, idx_j] - (rPGD_StepSize * grad_MPC[idx_n, idx_j]);

                (* Box Saturation Projection [u_Min .. u_Max] *)
                IF rPGD_ProjVal < u_Min[idx_j] THEN
                    rPGD_ProjVal := u_Min[idx_j];
                ELSIF rPGD_ProjVal > u_Max[idx_j] THEN
                    rPGD_ProjVal := u_Max[idx_j];
                END_IF;

                (* Dynamic Slew Rate Projection *)
                IF idx_n = 1 THEN
                    rSlewDelta := rPGD_ProjVal - u_Prev[idx_j];
                    IF rSlewDelta > du_MaxSlew[idx_j] THEN
                        rPGD_ProjVal := u_Prev[idx_j] + du_MaxSlew[idx_j];
                    ELSIF rSlewDelta < (-du_MaxSlew[idx_j]) THEN
                        rPGD_ProjVal := u_Prev[idx_j] - du_MaxSlew[idx_j];
                    END_IF;
                ELSE
                    rSlewDelta := rPGD_ProjVal - u_MPC_Trajectory[idx_n - 1, idx_j];
                    IF rSlewDelta > du_MaxSlew[idx_j] THEN
                        rPGD_ProjVal := u_MPC_Trajectory[idx_n - 1, idx_j] + du_MaxSlew[idx_j];
                    ELSIF rSlewDelta < (-du_MaxSlew[idx_j]) THEN
                        rPGD_ProjVal := u_MPC_Trajectory[idx_n - 1, idx_j] - du_MaxSlew[idx_j];
                    END_IF;
                END_IF;

                u_MPC_Trajectory[idx_n, idx_j] := rPGD_ProjVal;
            END_FOR;
        END_FOR;
    END_FOR;

    (* 3.5 Dispatch Horizon Step 1 as Instantaneous Optimal Actuator Commands *)
    FOR idx_j := 1 TO 6 DO
        u_Act[idx_j] := u_MPC_Trajectory[1, idx_j];
        du_Act[idx_j] := u_Act[idx_j] - u_Prev[idx_j];
        u_Prev[idx_j] := u_Act[idx_j];
    END_FOR;

ELSE
    (* Fallback Mode: Coordinated Manual / State Machine Tracking *)
    rPV_MPC_CostFunctionJ := 0.0;
    FOR idx_j := 1 TO 6 DO
        du_Act[idx_j] := u_Act[idx_j] - u_Prev[idx_j];
        u_Prev[idx_j] := u_Act[idx_j];
        FOR idx_n := 1 TO 5 DO
            u_MPC_Trajectory[idx_n, idx_j] := u_Act[idx_j];
        END_FOR;
    END_FOR;
END_IF;

(* 3.6 Valve Packing Anti-Stiction Dither Generation (2.5 Hz Sine Modulation) *)
rDither_Phase := rDither_Phase + (2.0 * 3.14159265 * rDither_Frequency * rTs_Seconds);
IF rDither_Phase > 6.28318530 THEN
    rDither_Phase := rDither_Phase - 6.28318530;
END_IF;
rDither_Signal := rDither_Amplitude * SIN(rDither_Phase);

(* 3.7 Assign Primary Continuous Control Actuator Outputs *)
rCV_GreenH2_Valve_Cmd     := u_Act[1] + (rDither_Signal * 0.5);
rCV_Syngas_Valve_Cmd      := u_Act[2] + (rDither_Signal * 0.5);
rCV_Heater_Fuel_Cmd       := u_Act[3] + (rDither_Signal * 0.3);
rCV_NatGas_Trim_Cmd       := u_Act[4] + (rDither_Signal * 0.4);
rCV_CoolingBlower_VFD_Cmd := u_Act[5];
rCV_Feeder_Speed_Cmd      := u_Act[6];

(* Hard Clamping of Final Command Signals [0.0 .. 100.0%] *)
IF rCV_GreenH2_Valve_Cmd < 0.0 THEN rCV_GreenH2_Valve_Cmd := 0.0; ELSIF rCV_GreenH2_Valve_Cmd > 100.0 THEN rCV_GreenH2_Valve_Cmd := 100.0; END_IF;
IF rCV_Syngas_Valve_Cmd < 0.0 THEN rCV_Syngas_Valve_Cmd := 0.0; ELSIF rCV_Syngas_Valve_Cmd > 100.0 THEN rCV_Syngas_Valve_Cmd := 100.0; END_IF;
IF rCV_Heater_Fuel_Cmd < 0.0 THEN rCV_Heater_Fuel_Cmd := 0.0; ELSIF rCV_Heater_Fuel_Cmd > 100.0 THEN rCV_Heater_Fuel_Cmd := 100.0; END_IF;
IF rCV_NatGas_Trim_Cmd < 0.0 THEN rCV_NatGas_Trim_Cmd := 0.0; ELSIF rCV_NatGas_Trim_Cmd > 100.0 THEN rCV_NatGas_Trim_Cmd := 100.0; END_IF;
IF rCV_CoolingBlower_VFD_Cmd < 0.0 THEN rCV_CoolingBlower_VFD_Cmd := 0.0; ELSIF rCV_CoolingBlower_VFD_Cmd > 100.0 THEN rCV_CoolingBlower_VFD_Cmd := 100.0; END_IF;
IF rCV_Feeder_Speed_Cmd < 0.0 THEN rCV_Feeder_Speed_Cmd := 0.0; ELSIF rCV_Feeder_Speed_Cmd > 100.0 THEN rCV_Feeder_Speed_Cmd := 100.0; END_IF;
"""
