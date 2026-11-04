# Section 4: Phase 3 Receding-Horizon MPC & State-Space Propagation

def get_sec4():
    return """
(* =====================================================================================================================
 * PHASE 3: DISCRETE STATE-SPACE PREDICTION & RECEDING-HORIZON MPC (T_s = 20 ms)
 * ===================================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------------------------
 * 3.1 State Tracking Error Vector Assembly x[1..8]
 * --------------------------------------------------------------------------------------------------------------------- *)
ax_state[1] := rVoted_ExtruderMeltPress_bar - rSet_InsulMeltPress_Target_bar;   (* Delta_P_melt [bar] *)
ax_state[2] := rVoted_ExtruderMeltTemp_degC - rSet_InsulMeltTemp_Target_degC;   (* Delta_T_melt [deg C] *)
ax_state[3] := rVoted_CatenarySag_mm        - rSet_CatenarySagTarget_mm;       (* Delta_y_sag [mm] *)
ax_state[4] := rVoted_Zone1Temp_degC        - rSet_Zone1_TempTarget_degC;       (* Delta_T_zone1 [deg C] *)
ax_state[5] := rVoted_TubeN2Press_bar       - rSet_TubeN2PressTarget_bar;       (* Delta_P_N2 [bar] *)
ax_state[6] := rVoted_QuenchWaterLvl_mm     - rSet_QuenchWaterLevel_mm;         (* Delta_L_quench [mm] *)
ax_state[7] := rVoted_HaulOffTension_kN     - rSet_HaulOffTension_kN;           (* Delta_H_tension [kN] *)
ax_state[8] := rVoted_WallThickness_mm      - rSet_NominalWallThickness_mm;     (* Delta_W_wall [mm] *)

(* Catenary Sag Centering Status (+/- 2.0 mm) *)
IF ABS(ax_state[3]) <= rSet_MaxSagDeviationTolerance_mm THEN
    bCatenarySagCenteringOk := TRUE;
ELSE
    bCatenarySagCenteringOk := FALSE;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * 3.2 Discrete State Propagation: x[k+1] = A * x[k] + B * u[k]
 * --------------------------------------------------------------------------------------------------------------------- *)
FOR nLoop_i := 1 TO 8 DO
    ax_next[nLoop_i] := 0.0;
    FOR nLoop_j := 1 TO 8 DO
        ax_next[nLoop_i] := ax_next[nLoop_i] + (aA[nLoop_i, nLoop_j] * ax_state[nLoop_j]);
    END_FOR;
    FOR nLoop_j := 1 TO 7 DO
        ax_next[nLoop_i] := ax_next[nLoop_i] + (aB[nLoop_i, nLoop_j] * au_control[nLoop_j]);
    END_FOR;
END_FOR;

(* Output Reconstruction: y[k] = C * x[k] + D * u[k] *)
FOR nLoop_i := 1 TO 8 DO
    ay_output[nLoop_i] := 0.0;
    FOR nLoop_j := 1 TO 8 DO
        ay_output[nLoop_i] := ay_output[nLoop_i] + (aC[nLoop_i, nLoop_j] * ax_state[nLoop_j]);
    END_FOR;
    FOR nLoop_j := 1 TO 7 DO
        ay_output[nLoop_i] := ay_output[nLoop_i] + (aD[nLoop_i, nLoop_j] * au_control[nLoop_j]);
    END_FOR;
END_FOR;

(* ---------------------------------------------------------------------------------------------------------------------
 * 3.3 Receding-Horizon Quadratic Cost Functional J Evaluation
 *     J = Sum [ x^T * Q * x + u^T * R * u + Delta_u^T * S * Delta_u ] + x_next^T * P * x_next
 * --------------------------------------------------------------------------------------------------------------------- *)
rMPC_QuadraticCostAccum := 0.0;

(* State Tracking Penalty: x^T * Q * x *)
FOR nLoop_i := 1 TO 8 DO
    rMPC_QuadraticCostAccum := rMPC_QuadraticCostAccum + (aQ_Weight[nLoop_i] * (ax_state[nLoop_i]**2.0));
END_FOR;

(* Actuator Effort Penalty: u^T * R * u *)
FOR nLoop_j := 1 TO 7 DO
    rMPC_QuadraticCostAccum := rMPC_QuadraticCostAccum + (aR_Weight[nLoop_j] * (au_control[nLoop_j]**2.0));
END_FOR;

(* Actuator Slew Rate Penalty: Delta_u^T * S * Delta_u *)
FOR nLoop_j := 1 TO 7 DO
    au_delta[nLoop_j] := au_control[nLoop_j] - au_prev[nLoop_j];
    rMPC_QuadraticCostAccum := rMPC_QuadraticCostAccum + (aS_Weight[nLoop_j] * (au_delta[nLoop_j]**2.0));
END_FOR;

(* Terminal Horizon State Penalty: x_next^T * P * x_next *)
FOR nLoop_i := 1 TO 8 DO
    rMPC_QuadraticCostAccum := rMPC_QuadraticCostAccum + (aP_TerminalWeight[nLoop_i] * (ax_next[nLoop_i]**2.0));
END_FOR;

rMPC_QuadraticCost_J := rMPC_QuadraticCostAccum;

(* ---------------------------------------------------------------------------------------------------------------------
 * 3.4 Projected Gradient Descent (PGD) Optimal Control Optimization
 *     nabla_u J = B^T * Q * x + R * u + S * (u - u_prev) + B^T * P * x_next
 * --------------------------------------------------------------------------------------------------------------------- *)
FOR nLoop_j := 1 TO 7 DO
    aGrad_u[nLoop_j] := (aR_Weight[nLoop_j] * au_control[nLoop_j]) + (aS_Weight[nLoop_j] * au_delta[nLoop_j]);
    FOR nLoop_i := 1 TO 8 DO
        aGrad_u[nLoop_j] := aGrad_u[nLoop_j] +
                            (aB[nLoop_i, nLoop_j] * aQ_Weight[nLoop_i] * ax_state[nLoop_i]) +
                            (aB[nLoop_i, nLoop_j] * aP_TerminalWeight[nLoop_i] * ax_next[nLoop_i]);
    END_FOR;

    (* Gradient Descent Step: u = u - alpha * nabla_u J *)
    au_control[nLoop_j] := au_control[nLoop_j] - (c_rPGD_Alpha * aGrad_u[nLoop_j]);

    (* Hard Lower & Upper Saturation Clamping *)
    IF au_control[nLoop_j] > au_max[nLoop_j] THEN
        au_control[nLoop_j] := au_max[nLoop_j];
    ELSIF au_control[nLoop_j] < au_min[nLoop_j] THEN
        au_control[nLoop_j] := au_min[nLoop_j];
    END_IF;

    (* Slew Rate Limiter Enforcement *)
    IF (au_control[nLoop_j] - au_prev[nLoop_j]) > adelta_u_max[nLoop_j] THEN
        au_control[nLoop_j] := au_prev[nLoop_j] + adelta_u_max[nLoop_j];
    ELSIF (au_control[nLoop_j] - au_prev[nLoop_j]) < -adelta_u_max[nLoop_j] THEN
        au_control[nLoop_j] := au_prev[nLoop_j] - adelta_u_max[nLoop_j];
    END_IF;

    (* Update Previous Actuator Vector Register *)
    au_prev[nLoop_j] := au_control[nLoop_j];
END_FOR;
"""

if __name__ == "__main__":
    s4 = get_sec4()
    print("Section 4 Length:", len(s4))
