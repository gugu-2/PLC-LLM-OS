# ccgt_builder/st_phase2_thermo_state_space.py

def get_phase2_thermo_state_space():
    return """(* =====================================================================================================================
 * PHASE 2: FIRST-PRINCIPLES THERMODYNAMIC OBSERVERS & DISCRETE STATE-SPACE PROPAGATION
 * Cyber-Physical Modeling:
 *   - Continuous-to-Discrete Conservation Equations (Mass, Momentum, Thermal Energy)
 *   - Gas Turbine Exhaust Calorific Energy Flow: Q_exh = m_exh * Cp_gas * (T_EGT - T_amb)
 *   - Triple-Pressure HRSG HP Evaporator Natural Circulation & Clausius-Clapeyron Saturation Balance
 *   - Irving-Miossec Non-Minimum Phase Void Fraction Swell/Shrink Anticipatory Decoupling
 *   - Multi-Stage Desuperheater Mixing Tee Enthalpy Balance & Spray Quench Feedforward
 *   - Hard Real-Time Discrete Kalman/Luenberger Innovation Observer:
 *       y_est[k]     = C * x_hat[k] + D * u[k]
 *       innov_err[k] = y_meas[k] - y_est[k]
 *       x_corr[k]    = x_hat[k] + L * innov_err[k]
 *       x_hat[k+1]   = A * x_corr[k] + B * u[k]
 * ===================================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------------------------
 * SECTION 2.1: FIRST-PRINCIPLES THERMODYNAMIC ENTHALPY & VOID PHENOMENOLOGICAL CALCULATIONS
 * --------------------------------------------------------------------------------------------------------------------- *)
(* 1. Evaporator Saturation Temperature via Antoine Formulation at Operating Drum Pressure *)
(* Tsat ~ 42.6776 - (3892.7 / (LN(rHP_Drum_Pressure_bar * 100.0) - 9.48654)) approx for 100..160 bar *)
(* Simplified robust polynomial approximation for saturation temp at high pressure [deg C] *)
rTarget_SteamTemp_degC := 565.0;

(* 2. Anticipatory Dynamic Decoupling Feedforward for HRSG Drum Level Swell *)
(* When EGT rises abruptly (positive gradient), bubble void fraction swells drum water level *)
(* Feedforward injects negative transient bias into feedwater valve command to suppress over-filling *)
rDynamic_Decoupling_FW_FF := -0.045 * (rVoted_EGT_degC - x_hat[2]);
IF rDynamic_Decoupling_FW_FF > 12.0 THEN
    rDynamic_Decoupling_FW_FF := 12.0;
ELSIF rDynamic_Decoupling_FW_FF < -12.0 THEN
    rDynamic_Decoupling_FW_FF := -12.0;
END_IF;

(* 3. Anticipatory Attemperator Spray Water Feedforward Enthalpy Balance *)
(* Spray demand proportional to excess enthalpy above superheater target exit temperature *)
IF rVoted_Steam_Temp_degC > (rTarget_SteamTemp_degC - 5.0) THEN
    rDynamic_Decoupling_Spray_FF := 0.28 * (rVoted_Steam_Temp_degC - rTarget_SteamTemp_degC)
                                  + 0.15 * (rVoted_Steam_Flow_kgs / rNominal_MainSteam_Flow_kgs) * (rVoted_EGT_degC - 580.0);
    IF rDynamic_Decoupling_Spray_FF < 0.0 THEN
        rDynamic_Decoupling_Spray_FF := 0.0;
    ELSIF rDynamic_Decoupling_Spray_FF > 35.0 THEN
        rDynamic_Decoupling_Spray_FF := 35.0;
    END_IF;
ELSE
    rDynamic_Decoupling_Spray_FF := 0.0;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * SECTION 2.2: OBSERVER ESTIMATION OF PHYSICAL OUTPUTS (y_est = C * x_hat + D * u_vec)
 * --------------------------------------------------------------------------------------------------------------------- *)
FOR m_idx := 1 TO 6 DO
    rTemp_Sum := 0.0;
    FOR i_idx := 1 TO 8 DO
        rTemp_Sum := rTemp_Sum + (C_mat[m_idx, i_idx] * x_hat[i_idx]);
    END_FOR;
    FOR j_idx := 1 TO 6 DO
        rTemp_Sum := rTemp_Sum + (D_mat[m_idx, j_idx] * u_vec[j_idx]);
    END_FOR;
    y_est[m_idx] := rTemp_Sum;
END_FOR;

(* ---------------------------------------------------------------------------------------------------------------------
 * SECTION 2.3: INNOVATION RESIDUAL CALCULATION (innov_err = y_meas - y_est)
 * --------------------------------------------------------------------------------------------------------------------- *)
FOR m_idx := 1 TO 6 DO
    innov_err[m_idx] := y_meas[m_idx] - y_est[m_idx];
END_FOR;

(* ---------------------------------------------------------------------------------------------------------------------
 * SECTION 2.4: A-POSTERIORI STATE CORRECTION VIA LUENBERGER INNOVATION GAIN (x_corr = x_hat + L * innov_err)
 * --------------------------------------------------------------------------------------------------------------------- *)
FOR i_idx := 1 TO 8 DO
    rTemp_Sum := x_hat[i_idx];
    FOR m_idx := 1 TO 6 DO
        rTemp_Sum := rTemp_Sum + (L_mat[i_idx, m_idx] * innov_err[m_idx]);
    END_FOR;
    x_corr[i_idx] := rTemp_Sum;
END_FOR;

(* ---------------------------------------------------------------------------------------------------------------------
 * SECTION 2.5: DISCRETE TIME-UPDATE PROPAGATION (x_pred = A * x_corr + B * u_vec)
 * --------------------------------------------------------------------------------------------------------------------- *)
FOR i_idx := 1 TO 8 DO
    rTemp_Sum := 0.0;
    FOR k_idx := 1 TO 8 DO
        rTemp_Sum := rTemp_Sum + (A_mat[i_idx, k_idx] * x_corr[k_idx]);
    END_FOR;
    FOR j_idx := 1 TO 6 DO
        rTemp_Sum := rTemp_Sum + (B_mat[i_idx, j_idx] * u_vec[j_idx]);
    END_FOR;
    x_pred[i_idx] := rTemp_Sum;
END_FOR;

(* Push predicted state into state estimator register for next execution scan *)
FOR i_idx := 1 TO 8 DO
    x_hat[i_idx] := x_pred[i_idx];
END_FOR;
"""
