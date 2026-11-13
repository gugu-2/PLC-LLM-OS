# ccgt_builder/st_phase3_mpc.py

def get_phase3_mpc():
    return """(* =====================================================================================================================
 * PHASE 3: RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) WITH PROJECTED GRADIENT DESCENT (PGD)
 * Mathematical Formulation:
 *   Prediction Horizon: Np = 5 steps (tau_horizon = 100.0 ms ahead @ Ts = 20.0 ms)
 *   Control Vector Dimension: Nu = 6 inputs:
 *     u1 = Main Fuel Gas Valve [%]
 *     u2 = Compressor VGV Position [deg]
 *     u3 = Boiler Feedwater Regulating Valve [%]
 *     u4 = Attemperator Desuperheater Spray Valve [%]
 *     u5 = HP Steam Bypass Valve to Condenser [%]
 *     u6 = Peaking Duct Burner Fuel Valve [%]
 *   Cost Functional:
 *     J = 0.5 * sum_{k=1..Np} [ (x[k] - x_ref)^T * Q * (x[k] - x_ref) + (u[k] - u_ref)^T * R * (u[k] - u_ref)
 *                               + (u[k] - u[k-1])^T * R_delta * (u[k] - u[k-1]) ]
 *       + 0.5 * (x[Np] - x_ref)^T * P * (x[Np] - x_ref)
 *   Optimization Scheme:
 *     Unrolled 6-iteration Projected Gradient Descent (PGD)
 *     Forward State Rollout:       x[k+1] = A * x[k] + B * u[k]
 *     Backward Costate Adjoint:    lambda[k] = A^T * lambda[k+1] + Q * (x[k] - x_ref)
 *     Gradient Vector:             grad_u[k] = B^T * lambda[k] + R * (u[k] - u_ref) + R_delta * (u[k] - u[k-1])
 *     Projected Descent & Slew:    u_traj[k] := Clip(u_traj[k] - alpha * grad_u[k], U_min, U_max)
 *                                  |u[k] - u[k-1]| <= du_max
 * ===================================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------------------------
 * SECTION 3.1: ESTABLISH CO-ORDINATED TARGET REFERENCE STATE VECTOR x_ref[1..8]
 * --------------------------------------------------------------------------------------------------------------------- *)
x_ref[1] := rTarget_Power_MW;
x_ref[2] := rNominal_EGT_degC;
x_ref[3] := rTarget_VGV_Position_deg;
x_ref[4] := rTarget_DrumLevel_mm; (* 0.0 mm Centerline *)
x_ref[5] := rNominal_MainSteam_Flow_kgs * MAX(0.15, rTarget_Power_MW / rGT_Rated_Base_Power_MW);
x_ref[6] := rTarget_SteamTemp_degC; (* 565.0 deg C *)
x_ref[7] := 490.0; (* Desuperheater intermediate temperature target *)
x_ref[8] := 55.0;  (* Baseline feedwater valve equilibrium opening *)

(* Reference Actuator Targets *)
u_ref[1] := (rTarget_Power_MW / rGT_Rated_Base_Power_MW) * 85.0;
u_ref[2] := rTarget_VGV_Position_deg;
u_ref[3] := (rVoted_Steam_Flow_kgs / rNominal_MainSteam_Flow_kgs) * 65.0;
u_ref[4] := rDynamic_Decoupling_Spray_FF;
u_ref[5] := 0.0; (* HP bypass target closed under steady generation *)
u_ref[6] := 0.0; (* Duct burner target off unless dispatched *)

(* ---------------------------------------------------------------------------------------------------------------------
 * SECTION 3.2: WARM-START MPC CONTROL TRAJECTORY FROM PREVIOUS HORIZON
 * Shift control trajectory by 1 step, duplicate end horizon step
 * --------------------------------------------------------------------------------------------------------------------- *)
FOR k_idx := 1 TO 4 DO
    FOR j_idx := 1 TO 6 DO
        u_traj[k_idx, j_idx] := u_traj[k_idx + 1, j_idx];
    END_FOR;
END_FOR;
FOR j_idx := 1 TO 6 DO
    u_traj[5, j_idx] := u_traj[4, j_idx];
END_FOR;

(* If in manual or non-coordinated mode, seed with current actual commands *)
IF NOT bAuto_Coord_Enable THEN
    FOR k_idx := 1 TO 5 DO
        FOR j_idx := 1 TO 6 DO
            u_traj[k_idx, j_idx] := u_vec[j_idx];
        END_FOR;
    END_FOR;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * SECTION 3.3: UNROLLED PROJECTED GRADIENT DESCENT (6 ITERATIONS)
 * --------------------------------------------------------------------------------------------------------------------- *)
FOR iter_idx := 1 TO 6 DO
    (* -----------------------------------------------------------------------------------------------------------------
     * SUB-STEP 3.3.1: FORWARD PREDICTION ROLLOUT
     * ----------------------------------------------------------------------------------------------------------------- *)
    (* Step k=1 starts from current filtered state x_hat *)
    FOR i_idx := 1 TO 8 DO
        rTemp_Sum := 0.0;
        FOR m_idx := 1 TO 8 DO
            rTemp_Sum := rTemp_Sum + (A_mat[i_idx, m_idx] * x_hat[m_idx]);
        END_FOR;
        FOR j_idx := 1 TO 6 DO
            rTemp_Sum := rTemp_Sum + (B_mat[i_idx, j_idx] * u_traj[1, j_idx]);
        END_FOR;
        x_traj[1, i_idx] := rTemp_Sum;
    END_FOR;

    (* Steps k=2 to 5 propagate along predicted trajectory *)
    FOR k_idx := 2 TO 5 DO
        FOR i_idx := 1 TO 8 DO
            rTemp_Sum := 0.0;
            FOR m_idx := 1 TO 8 DO
                rTemp_Sum := rTemp_Sum + (A_mat[i_idx, m_idx] * x_traj[k_idx - 1, m_idx]);
            END_FOR;
            FOR j_idx := 1 TO 6 DO
                rTemp_Sum := rTemp_Sum + (B_mat[i_idx, j_idx] * u_traj[k_idx, j_idx]);
            END_FOR;
            x_traj[k_idx, i_idx] := rTemp_Sum;
        END_FOR;
    END_FOR;

    (* -----------------------------------------------------------------------------------------------------------------
     * SUB-STEP 3.3.2: BACKWARD ADJOINT COSTATE PROPAGATION (lambda)
     * ----------------------------------------------------------------------------------------------------------------- *)
    (* Terminal Step k=5: lambda[5] = P * (x_traj[5] - x_ref) *)
    FOR i_idx := 1 TO 8 DO
        rTemp_Sum := 0.0;
        FOR m_idx := 1 TO 8 DO
            rTemp_Sum := rTemp_Sum + (P_mat[i_idx, m_idx] * (x_traj[5, m_idx] - x_ref[m_idx]));
        END_FOR;
        lambda_vec[5, i_idx] := rTemp_Sum;
    END_FOR;

    (* Backward Steps k=4 DOWNTO 1: lambda[k] = A^T * lambda[k+1] + Q * (x_traj[k] - x_ref) *)
    FOR k_idx := 4 DOWNTO 1 DO
        FOR i_idx := 1 TO 8 DO
            rTemp_Sum := 0.0;
            (* Transpose multiplication A^T: row m, col i *)
            FOR m_idx := 1 TO 8 DO
                rTemp_Sum := rTemp_Sum + (A_mat[m_idx, i_idx] * lambda_vec[k_idx + 1, m_idx]);
            END_FOR;
            FOR m_idx := 1 TO 8 DO
                rTemp_Sum := rTemp_Sum + (Q_mat[i_idx, m_idx] * (x_traj[k_idx, m_idx] - x_ref[m_idx]));
            END_FOR;
            lambda_vec[k_idx, i_idx] := rTemp_Sum;
        END_FOR;
    END_FOR;

    (* -----------------------------------------------------------------------------------------------------------------
     * SUB-STEP 3.3.3: GRADIENT CALCULATION, PROJECTED DESCENT & RATE CLAMPING
     * ----------------------------------------------------------------------------------------------------------------- *)
    FOR k_idx := 1 TO 5 DO
        FOR j_idx := 1 TO 6 DO
            (* B^T * lambda[k] *)
            rTemp_Sum := 0.0;
            FOR m_idx := 1 TO 8 DO
                rTemp_Sum := rTemp_Sum + (B_mat[m_idx, j_idx] * lambda_vec[k_idx, m_idx]);
            END_FOR;

            (* R * (u[k] - u_ref) *)
            rTemp_Sum := rTemp_Sum + (R_mat[j_idx, j_idx] * (u_traj[k_idx, j_idx] - u_ref[j_idx]));

            (* Slew penalty R_delta * (u[k] - u[k-1]) *)
            IF k_idx = 1 THEN
                rTemp_Sum := rTemp_Sum + (R_delta[j_idx, j_idx] * (u_traj[1, j_idx] - u_prev[j_idx]));
            ELSE
                rTemp_Sum := rTemp_Sum + (R_delta[j_idx, j_idx] * (u_traj[k_idx, j_idx] - u_traj[k_idx - 1, j_idx]));
            END_IF;

            grad_u[k_idx, j_idx] := rTemp_Sum;

            (* Apply Projected Gradient Descent Step *)
            rCandidate_U := u_traj[k_idx, j_idx] - (rPGD_Alpha_Step * grad_u[k_idx, j_idx]);

            (* Enforce Physical Box Saturation Bounds [u_min, u_max] *)
            IF rCandidate_U < u_min[j_idx] THEN
                rCandidate_U := u_min[j_idx];
            ELSIF rCandidate_U > u_max[j_idx] THEN
                rCandidate_U := u_max[j_idx];
            END_IF;

            (* Enforce Dynamic Slew Rate Clamping per Scan *)
            IF k_idx = 1 THEN
                rDelta_U := rCandidate_U - u_prev[j_idx];
                IF rDelta_U > du_max[j_idx] THEN
                    rCandidate_U := u_prev[j_idx] + du_max[j_idx];
                ELSIF rDelta_U < -du_max[j_idx] THEN
                    rCandidate_U := u_prev[j_idx] - du_max[j_idx];
                END_IF;
            ELSE
                rDelta_U := rCandidate_U - u_traj[k_idx - 1, j_idx];
                IF rDelta_U > du_max[j_idx] THEN
                    rCandidate_U := u_traj[k_idx - 1, j_idx] + du_max[j_idx];
                ELSIF rDelta_U < -du_max[j_idx] THEN
                    rCandidate_U := u_traj[k_idx - 1, j_idx] - du_max[j_idx];
                END_IF;
            END_IF;

            u_traj[k_idx, j_idx] := rCandidate_U;
        END_FOR;
    END_FOR;
END_FOR;

(* ---------------------------------------------------------------------------------------------------------------------
 * SECTION 3.4: EXTRACT RECEDING HORIZON FIRST CONTROL STEP & APPLY DECOUPLING BIAS
 * --------------------------------------------------------------------------------------------------------------------- *)
IF bAuto_Coord_Enable AND (eCurrentState = 9 OR eCurrentState = 10 OR eCurrentState = 11) THEN
    (* Gas Turbine Fuel Gas Control Valve Demand *)
    u_vec[1] := u_traj[1, 1];

    (* Compressor VGV Angular Position Demand *)
    u_vec[2] := u_traj[1, 2];

    (* HRSG HP Boiler Feedwater Regulating Valve with Dynamic Void Decoupling *)
    u_vec[3] := u_traj[1, 3] + rDynamic_Decoupling_FW_FF;
    IF u_vec[3] < 0.0 THEN
        u_vec[3] := 0.0;
    ELSIF u_vec[3] > 100.0 THEN
        u_vec[3] := 100.0;
    END_IF;

    (* Superheater Attemperator Spray Valve with Anticipatory Desuperheating Bias *)
    u_vec[4] := u_traj[1, 4] + rDynamic_Decoupling_Spray_FF;
    IF u_vec[4] < 0.0 THEN
        u_vec[4] := 0.0;
    ELSIF u_vec[4] > 100.0 THEN
        u_vec[4] := 100.0;
    END_IF;

    (* HP Steam Bypass Valve to Surface Condenser *)
    u_vec[5] := u_traj[1, 5];

    (* HRSG Peaking Duct Burner Fuel Valve *)
    IF bEnable_Duct_Burner THEN
        u_vec[6] := u_traj[1, 6];
    ELSE
        u_vec[6] := 0.0;
    END_IF;
END_IF;

(* Save current control vector into u_prev for subsequent execution cycle *)
FOR j_idx := 1 TO 6 DO
    u_prev[j_idx] := u_vec[j_idx];
END_FOR;
"""
