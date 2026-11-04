# brain_scratch/can_seamer_builder/part4_ss_mpc.py

PART4_SS_MPC = """
(* ==========================================================================================
 * PHASE 4: 8-STATE DISCRETE STATE-SPACE MODEL & LUENBERGER OBSERVER UPDATE
 * Mathematical Foundation:
 *   x[k+1] = A * x[k] + B * u[k]
 *   y[k]   = C * x[k] + D * u[k]
 * Observer Formulation:
 *   x_hat[k+1] = A * x_hat[k] + B * u[k] + L * (y[k] - C * x_hat[k])
 * ========================================================================================== *)

(* Step 1: Assemble Physical Process Measurement Vector y[k] [6x1] *)
ay_Meas[1] := rVoted_Chuck_AxialLoad_kN;
ay_Meas[2] := rCan_InternalPressure_bar;
ay_Meas[3] := rVoted_AcousticResonance_kHz;
ay_Meas[4] := rVoted_SteamBarrier_Temp_degC;
ay_Meas[5] := (rInfeed_Starwheel_Phase_Deg - rSP_Infeed_Phase_Deg) * 17.45329; (* Convert deg to mrad *)
ay_Meas[6] := rLaser_SeamThickness_mm;

(* Step 2: Compute Observer Estimated Measurement Vector y_hat[k] = C * x_hat[k] + D * u[k] *)
FOR iMatrixRow := 1 TO 6 DO
    ay_Hat[iMatrixRow] := 0.0;
    FOR iMatrixCol := 1 TO 8 DO
        ay_Hat[iMatrixRow] := ay_Hat[iMatrixRow] + (aC_Matrix[iMatrixRow, iMatrixCol] * ax_Hat[iMatrixCol]);
    END_FOR;
    (* Add direct feedthrough D * u[k] *)
    FOR iMatrixCol := 1 TO 6 DO
        ay_Hat[iMatrixRow] := ay_Hat[iMatrixRow] + (aD_Matrix[iMatrixRow, iMatrixCol] * au_Control[iMatrixCol]);
    END_FOR;
END_FOR;

(* Step 3: Compute Innovation Residual Vector e_y = y[k] - y_hat[k] *)
FOR iMatrixRow := 1 TO 6 DO
    ay_Residual[iMatrixRow] := ay_Meas[iMatrixRow] - ay_Hat[iMatrixRow];
END_FOR;

(* Step 4: Compute One-Step Ahead Observer State Prediction x_hat[k+1] = A * x_hat[k] + B * u[k] + L * e_y *)
FOR iMatrixRow := 1 TO 8 DO
    ax_Pred[iMatrixRow] := 0.0;
    
    (* Dynamic state transition A * x_hat *)
    FOR iMatrixCol := 1 TO 8 DO
        ax_Pred[iMatrixRow] := ax_Pred[iMatrixRow] + (aA_Matrix[iMatrixRow, iMatrixCol] * ax_Hat[iMatrixCol]);
    END_FOR;

    (* Actuator input coupling B * u *)
    FOR iMatrixCol := 1 TO 6 DO
        ax_Pred[iMatrixRow] := ax_Pred[iMatrixRow] + (aB_Matrix[iMatrixRow, iMatrixCol] * au_Control[iMatrixCol]);
    END_FOR;

    (* Innovation correction L * (y - y_hat) *)
    FOR iMatrixCol := 1 TO 6 DO
        ax_Pred[iMatrixRow] := ax_Pred[iMatrixRow] + (aL_ObserverGain[iMatrixRow, iMatrixCol] * ay_Residual[iMatrixCol]);
    END_FOR;
END_FOR;

(* Step 5: Update Estimated State Vector x_hat[k] with Bound Sanitization *)
ax_Hat[1] := MAX(-15.0, MIN(15.0, ax_Pred[1]));     (* Speed Error [-15 to +15 rpm] *)
ax_Hat[2] := MAX(1.0,   MIN(12.0, ax_Pred[2]));     (* Chuck Load [1 to 12 kN] *)
ax_Hat[3] := MAX(2.0,   MIN(35.0, ax_Pred[3]));     (* LN2 Pulse [2 to 35 ms] *)
ax_Hat[4] := MAX(0.5,   MIN(4.5,  ax_Pred[4]));     (* Can Headspace [0.5 to 4.5 bar] *)
ax_Hat[5] := MAX(1.5,   MIN(5.0,  ax_Pred[5]));     (* Acoustic Peak [1.5 to 5.0 kHz] *)
ax_Hat[6] := MAX(20.0,  MIN(150.0,ax_Pred[6]));     (* Steam Temp [20 to 150 deg C] *)
ax_Hat[7] := MAX(-25.0, MIN(25.0, ax_Pred[7]));     (* Sync Error [-25 to +25 mrad] *)
ax_Hat[8] := MAX(-50.0, MIN(50.0, ax_Pred[8]));     (* Torque Ripple [-50 to +50 Nm] *)

(* ==========================================================================================
 * PHASE 5: RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) OPTIMIZATION
 * Objective Function:
 *   Min J = SUM_{h=1}^{Np} (x_h - x_ref)^T * Q * (x_h - x_ref)
 *         + SUM_{j=1}^{Nc} (u_j - u_ref)^T * R * (u_j - u_ref)
 *         + (x_Np - x_ref)^T * P * (x_Np - x_ref)
 * Subject to Actuator Physical Hard Limits and Slew Rates.
 * ========================================================================================== *)

(* Setpoint Reference Trajectory Vector x_ref [8x1] *)
ax_Reference[1] := 0.0;                        (* Zero speed tracking error [rpm] *)
ax_Reference[2] := rSP_Chuck_AxialLoad_kN;     (* Nominal 5.50 kN chuck seaming load *)
ax_Reference[3] := rSP_LN2_DosingPulse_ms;     (* Nominal 14.50 ms nitrogen dosing pulse *)
ax_Reference[4] := rSP_HeadspacePressure_bar;  (* Nominal 1.85 bar internal can pressure *)
ax_Reference[5] := rSP_AcousticResonance_kHz;  (* Nominal 3.15 kHz acoustic peak *)
ax_Reference[6] := rSP_SteamBarrier_Temp_degC; (* Nominal 125.0 deg C sterile steam enclosure *)
ax_Reference[7] := 0.0;                        (* Zero infeed synchronization phase error [mrad] *)
ax_Reference[8] := 0.0;                        (* Zero torque ripple harmonic disturbance [Nm] *)

(* Initialize Horizon States from Current Observer State *)
FOR iMatrixCol := 1 TO 8 DO
    ax_Horizon[1, iMatrixCol] := ax_Hat[iMatrixCol];
END_FOR;

(* Seed Control Sequence Horizon from Previous Control Action *)
FOR iHorizonIdx := 1 TO 3 DO
    FOR iMatrixCol := 1 TO 6 DO
        au_Horizon[iHorizonIdx, iMatrixCol] := au_Control[iMatrixCol];
    END_FOR;
END_FOR;

(* Projected Gradient Descent Optimization Loop (3 Iterations per scan cycle) *)
FOR iOptStep := 1 TO 3 DO
    rMPC_Cost_J := 0.0;

    (* Forward State Horizon Propagation: x[h+1] = A * x[h] + B * u[h] *)
    FOR iHorizonIdx := 1 TO 4 DO
        FOR iMatrixRow := 1 TO 8 DO
            ax_Horizon[iHorizonIdx + 1, iMatrixRow] := 0.0;
            
            (* A * x[h] *)
            FOR iMatrixCol := 1 TO 8 DO
                ax_Horizon[iHorizonIdx + 1, iMatrixRow] := ax_Horizon[iHorizonIdx + 1, iMatrixRow] + 
                    (aA_Matrix[iMatrixRow, iMatrixCol] * ax_Horizon[iHorizonIdx, iMatrixCol]);
            END_FOR;

            (* B * u[h] (receding to last control action beyond Nc=3) *)
            IF iHorizonIdx <= 3 THEN
                FOR iMatrixCol := 1 TO 6 DO
                    ax_Horizon[iHorizonIdx + 1, iMatrixRow] := ax_Horizon[iHorizonIdx + 1, iMatrixRow] + 
                        (aB_Matrix[iMatrixRow, iMatrixCol] * au_Horizon[iHorizonIdx, iMatrixCol]);
                END_FOR;
            ELSE
                FOR iMatrixCol := 1 TO 6 DO
                    ax_Horizon[iHorizonIdx + 1, iMatrixRow] := ax_Horizon[iHorizonIdx + 1, iMatrixRow] + 
                        (aB_Matrix[iMatrixRow, iMatrixCol] * au_Horizon[3, iMatrixCol]);
                END_FOR;
            END_IF;
        END_FOR;
    END_FOR;

    (* Evaluate Quadratic Tracking Cost Function J across Prediction Horizon *)
    FOR iHorizonIdx := 1 TO 5 DO
        FOR iMatrixRow := 1 TO 8 DO
            IF iHorizonIdx < 5 THEN
                (* Intermediate Horizon State Cost: (x - x_ref)^2 * Q *)
                rMPC_Cost_J := rMPC_Cost_J + (EXPT(ax_Horizon[iHorizonIdx, iMatrixRow] - ax_Reference[iMatrixRow], 2) * 
                                              aQ_StateWeight[iMatrixRow, iMatrixRow]);
            ELSE
                (* Terminal State Cost: (x - x_ref)^2 * P *)
                rMPC_Cost_J := rMPC_Cost_J + (EXPT(ax_Horizon[iHorizonIdx, iMatrixRow] - ax_Reference[iMatrixRow], 2) * 
                                              aP_TerminalWeight[iMatrixRow, iMatrixRow]);
            END_IF;
        END_FOR;

        (* Control Action Penalty: u^2 * R *)
        IF iHorizonIdx <= 3 THEN
            FOR iMatrixCol := 1 TO 6 DO
                rMPC_Cost_J := rMPC_Cost_J + (EXPT(au_Horizon[iHorizonIdx, iMatrixCol], 2) * 
                                              aR_ControlWeight[iMatrixCol, iMatrixCol]);
            END_FOR;
        END_IF;
    END_FOR;

    (* Gradient Descent Direction Update for u[1] (First control action in horizon) *)
    (* Turret Speed Trim Control Update *)
    au_Unconstrained[1] := au_Horizon[1, 1] - rMPC_Gradient_Step * 
        ((ax_Horizon[2, 1] - ax_Reference[1]) * aQ_StateWeight[1, 1] * aB_Matrix[1, 1] + 
         au_Horizon[1, 1] * aR_ControlWeight[1, 1]);

    (* Lifter Axial Preload Bias Update *)
    au_Unconstrained[2] := au_Horizon[1, 2] - rMPC_Gradient_Step * 
        ((ax_Horizon[2, 2] - ax_Reference[2]) * aQ_StateWeight[2, 2] * aB_Matrix[2, 2] + 
         au_Horizon[1, 2] * aR_ControlWeight[2, 2]);

    (* LN2 Injection Pulse Duration Trim Update *)
    au_Unconstrained[3] := au_Horizon[1, 3] - rMPC_Gradient_Step * 
        ((ax_Horizon[2, 4] - ax_Reference[4]) * aQ_StateWeight[4, 4] * aB_Matrix[4, 3] + 
         au_Horizon[1, 3] * aR_ControlWeight[3, 3]);

    (* Steam Barrier Regulation Valve Position Update *)
    au_Unconstrained[4] := au_Horizon[1, 4] - rMPC_Gradient_Step * 
        ((ax_Horizon[2, 6] - ax_Reference[6]) * aQ_StateWeight[6, 6] * aB_Matrix[6, 4] + 
         au_Horizon[1, 4] * aR_ControlWeight[4, 4]);

    (* Infeed Worm Screw Phase Offset Update *)
    au_Unconstrained[5] := au_Horizon[1, 5] - rMPC_Gradient_Step * 
        ((ax_Horizon[2, 7] - ax_Reference[7]) * aQ_StateWeight[7, 7] * aB_Matrix[7, 5] + 
         au_Horizon[1, 5] * aR_ControlWeight[5, 5]);

    (* Dynamic Seaming Roll Cam Depth Bias Update *)
    au_Unconstrained[6] := au_Horizon[1, 6] - rMPC_Gradient_Step * 
        ((ax_Horizon[2, 2] - ax_Reference[2]) * aQ_StateWeight[2, 2] * aB_Matrix[2, 6] + 
         au_Horizon[1, 6] * aR_ControlWeight[6, 6]);

    (* Squeeze Control Horizons into Bounds *)
    au_Horizon[1, 1] := MAX(-5.0,  MIN(5.0,   au_Unconstrained[1])); (* Speed Trim [-5 to +5 rpm] *)
    au_Horizon[1, 2] := MAX(-1.5,  MIN(1.5,   au_Unconstrained[2])); (* Preload Trim [-1.5 to +1.5 kN] *)
    au_Horizon[1, 3] := MAX(-6.0,  MIN(6.0,   au_Unconstrained[3])); (* LN2 Pulse Trim [-6 to +6 ms] *)
    au_Horizon[1, 4] := MAX(0.0,   MIN(100.0, au_Unconstrained[4])); (* Steam Valve [0 to 100%] *)
    au_Horizon[1, 5] := MAX(-8.0,  MIN(8.0,   au_Unconstrained[5])); (* Infeed Phase [-8 to +8 mrad] *)
    au_Horizon[1, 6] := MAX(-0.35, MIN(0.35,  au_Unconstrained[6])); (* Cam Depth [-0.35 to +0.35 mm] *)
END_FOR;

(* Commit First Step Control Actions to Applied Control Vector *)
au_Control[1] := au_Horizon[1, 1];
au_Control[2] := au_Horizon[1, 2];
au_Control[3] := au_Horizon[1, 3];
au_Control[4] := au_Horizon[1, 4];
au_Control[5] := au_Horizon[1, 5];
au_Control[6] := au_Horizon[1, 6];
"""
