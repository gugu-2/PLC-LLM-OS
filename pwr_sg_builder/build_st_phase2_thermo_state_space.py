# build_st_phase2_thermo_state_space.py
# Section 5: Phase 2 - First-Principles Cyber-Physical State-Space Observer and Thermo-Hydraulics

def get_phase2_thermo_state_space():
    code = []
    code.append("""(* =====================================================================================================================
 * PHASE 2: FIRST-PRINCIPLES CYBER-PHYSICAL STATE-SPACE ESTIMATION & THERMO-HYDRAULIC OBSERVER
 * Governing Cyber-Physical Equations:
 *   1) Non-Minimum Phase Reverse Dynamics (Irving-Miossec Model):
 *      When cold feedwater enters the downcomer, subcooled liquid condenses steam bubbles in the boiling riser,
 *      causing an instantaneous volumetric contraction (shrink) before mass accumulation causes level rise.
 *      Conversely, sudden turbine valve opening causes depressurization, flashing liquid to vapor and causing
 *      an immediate false swell before mass depletion drops the level.
 *   2) State-Space Propagation:
 *      x_pred[k+1] = A * x_hat[k] + B * u[k]
 *   3) Measurement Prediction:
 *      y_pred[k]   = C * x_pred[k] + D * u[k]
 *   4) Innovation Residual:
 *      y_res[k]    = y_meas[k] - y_pred[k]
 *   5) Kalman Observer a-posteriori State Update:
 *      x_hat[k+1]  = x_pred[k+1] + L * y_res[k]
 * ===================================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------------------------
 * SECTION 2.1: ASSEMBLE PLANT CONTROL & DISTURBANCE VECTOR u[1..5]
 * --------------------------------------------------------------------------------------------------------------------- *)
u_vec[1] := rCommand_MFRV_Position;          (* Actuator 1: MFRV Position [%] *)
u_vec[2] := rCommand_Bypass_Valve_Pos;       (* Actuator 2: Low-Power Bypass [%] *)
u_vec[3] := rCommand_AFW_Motor_Pump_Speed;   (* Actuator 3: Motor-Driven AFW [%] *)
u_vec[4] := rCommand_AFW_Turbine_Pump_Flow;  (* Actuator 4: Turbine-Driven AFW [t/h] *)
u_vec[5] := rCommand_Blowdown_Valve_Pos;     (* Actuator 5: Bottom Blowdown [%] *)

(* Assemble Validated Measurement Vector y_meas[1..5] *)
y_meas[1] := rVoted_Level_NR;                                    (* Output 1: Narrow-Range Level [mm] *)
y_meas[2] := rVoted_Press_SteamDrum;                             (* Output 2: Drum Saturation Pressure [bar] *)
y_meas[3] := rVoted_Flow_MainSteam;                              (* Output 3: Main Steam Mass Flow Rate [t/h] *)
y_meas[4] := rVoted_Flow_Feedwater;                              (* Output 4: Main Feedwater Mass Flow Rate [t/h] *)
y_meas[5] := rTemp_ColdLeg_Primary;                              (* Output 5: RCS Cold Leg Temperature [deg C] *)

(* ---------------------------------------------------------------------------------------------------------------------
 * SECTION 2.2: FIRST-PRINCIPLES THERMO-HYDRAULIC ALGEBRAIC EQUATIONS & RATE ESTIMATION
 * --------------------------------------------------------------------------------------------------------------------- *)
(* Compute level rate-of-change differential [mm/s] *)
rMeasured_Level_Rate_mm_s := (rVoted_Level_NR - rPrev_Voted_Level_NR) / rScan_Period_Ts;
rPrev_Voted_Level_NR := rVoted_Level_NR;

(* Steam flow rate of change [t/(h*s)] for feedforward lead-lag *)
rSteam_Flow_Derivative := (rVoted_Flow_MainSteam - rPrev_Voted_Steam_Flow) / rScan_Period_Ts;
rPrev_Voted_Steam_Flow := rVoted_Flow_MainSteam;
rPrev_Voted_Feed_Flow := rVoted_Flow_Feedwater;

(* Continuous Lead-Lag Compensator for Dynamic Shrink/Swell Mitigation:
 * T_lead = 8.5 s, T_lag = 18.0 s
 * Discretized with Tustin bilinear transform:
 * dx_leadlag/dt = (1/T_lag) * (K_ff * (Flow_MS - Flow_FW) - x_leadlag)
 *)
rLeadLag_State_X1 := rLeadLag_State_X1 + rScan_Period_Ts * (0.055556 * ((rVoted_Flow_MainSteam - rVoted_Flow_Feedwater) - rLeadLag_State_X1));
rDynamic_Feedforward_Bias := (8.5 * 0.055556 * (rVoted_Flow_MainSteam - rVoted_Flow_Feedwater)) + (1.0 - (8.5 * 0.055556)) * rLeadLag_State_X1;

(* ---------------------------------------------------------------------------------------------------------------------
 * SECTION 2.3: EXPLICIT A-PRIORI STATE PROPAGATION (x_pred = A * x_hat + B * u)
 * Fully written out term-by-term matrix-vector multiplication with zero shortcuts
 * --------------------------------------------------------------------------------------------------------------------- *)
(* State 1 Prediction: Narrow-Range Level [mm] *)
x_pred[1] := (A_mat[1, 1] * x_hat[1]) + (A_mat[1, 2] * x_hat[2]) + (A_mat[1, 3] * x_hat[3]) + (A_mat[1, 4] * x_hat[4]) +
             (A_mat[1, 5] * x_hat[5]) + (A_mat[1, 6] * x_hat[6]) + (A_mat[1, 7] * x_hat[7]) + (A_mat[1, 8] * x_hat[8]) +
             (B_mat[1, 1] * u_vec[1]) + (B_mat[1, 2] * u_vec[2]) + (B_mat[1, 3] * u_vec[3]) + (B_mat[1, 4] * u_vec[4]) +
             (B_mat[1, 5] * u_vec[5]);

(* State 2 Prediction: Downcomer Flow Rate [kg/s] *)
x_pred[2] := (A_mat[2, 1] * x_hat[1]) + (A_mat[2, 2] * x_hat[2]) + (A_mat[2, 3] * x_hat[3]) + (A_mat[2, 4] * x_hat[4]) +
             (A_mat[2, 5] * x_hat[5]) + (A_mat[2, 6] * x_hat[6]) + (A_mat[2, 7] * x_hat[7]) + (A_mat[2, 8] * x_hat[8]) +
             (B_mat[2, 1] * u_vec[1]) + (B_mat[2, 2] * u_vec[2]) + (B_mat[2, 3] * u_vec[3]) + (B_mat[2, 4] * u_vec[4]) +
             (B_mat[2, 5] * u_vec[5]);

(* State 3 Prediction: Boiling Riser Bulk Void Fraction [-] *)
x_pred[3] := (A_mat[3, 1] * x_hat[1]) + (A_mat[3, 2] * x_hat[2]) + (A_mat[3, 3] * x_hat[3]) + (A_mat[3, 4] * x_hat[4]) +
             (A_mat[3, 5] * x_hat[5]) + (A_mat[3, 6] * x_hat[6]) + (A_mat[3, 7] * x_hat[7]) + (A_mat[3, 8] * x_hat[8]) +
             (B_mat[3, 1] * u_vec[1]) + (B_mat[3, 2] * u_vec[2]) + (B_mat[3, 3] * u_vec[3]) + (B_mat[3, 4] * u_vec[4]) +
             (B_mat[3, 5] * u_vec[5]);

(* State 4 Prediction: Primary-to-Secondary U-Tube Heat Transfer Rate [MW] *)
x_pred[4] := (A_mat[4, 1] * x_hat[1]) + (A_mat[4, 2] * x_hat[2]) + (A_mat[4, 3] * x_hat[3]) + (A_mat[4, 4] * x_hat[4]) +
             (A_mat[4, 5] * x_hat[5]) + (A_mat[4, 6] * x_hat[6]) + (A_mat[4, 7] * x_hat[7]) + (A_mat[4, 8] * x_hat[8]) +
             (B_mat[4, 1] * u_vec[1]) + (B_mat[4, 2] * u_vec[2]) + (B_mat[4, 3] * u_vec[3]) + (B_mat[4, 4] * u_vec[4]) +
             (B_mat[4, 5] * u_vec[5]);

(* State 5 Prediction: Steam Drum Saturation Pressure [bar] *)
x_pred[5] := (A_mat[5, 1] * x_hat[1]) + (A_mat[5, 2] * x_hat[2]) + (A_mat[5, 3] * x_hat[3]) + (A_mat[5, 4] * x_hat[4]) +
             (A_mat[5, 5] * x_hat[5]) + (A_mat[5, 6] * x_hat[6]) + (A_mat[5, 7] * x_hat[7]) + (A_mat[5, 8] * x_hat[8]) +
             (B_mat[5, 1] * u_vec[1]) + (B_mat[5, 2] * u_vec[2]) + (B_mat[5, 3] * u_vec[3]) + (B_mat[5, 4] * u_vec[4]) +
             (B_mat[5, 5] * u_vec[5]);

(* State 6 Prediction: Primary Coolant Cold Leg Temperature [deg C] *)
x_pred[6] := (A_mat[6, 1] * x_hat[1]) + (A_mat[6, 2] * x_hat[2]) + (A_mat[6, 3] * x_hat[3]) + (A_mat[6, 4] * x_hat[4]) +
             (A_mat[6, 5] * x_hat[5]) + (A_mat[6, 6] * x_hat[6]) + (A_mat[6, 7] * x_hat[7]) + (A_mat[6, 8] * x_hat[8]) +
             (B_mat[6, 1] * u_vec[1]) + (B_mat[6, 2] * u_vec[2]) + (B_mat[6, 3] * u_vec[3]) + (B_mat[6, 4] * u_vec[4]) +
             (B_mat[6, 5] * u_vec[5]);

(* State 7 Prediction: Main Feedwater Regulating Valve Trim [%] *)
x_pred[7] := (A_mat[7, 1] * x_hat[1]) + (A_mat[7, 2] * x_hat[2]) + (A_mat[7, 3] * x_hat[3]) + (A_mat[7, 4] * x_hat[4]) +
             (A_mat[7, 5] * x_hat[5]) + (A_mat[7, 6] * x_hat[6]) + (A_mat[7, 7] * x_hat[7]) + (A_mat[7, 8] * x_hat[8]) +
             (B_mat[7, 1] * u_vec[1]) + (B_mat[7, 2] * u_vec[2]) + (B_mat[7, 3] * u_vec[3]) + (B_mat[7, 4] * u_vec[4]) +
             (B_mat[7, 5] * u_vec[5]);

(* State 8 Prediction: Non-Minimum Phase Inverse Response Swell State [mm] *)
x_pred[8] := (A_mat[8, 1] * x_hat[1]) + (A_mat[8, 2] * x_hat[2]) + (A_mat[8, 3] * x_hat[3]) + (A_mat[8, 4] * x_hat[4]) +
             (A_mat[8, 5] * x_hat[5]) + (A_mat[8, 6] * x_hat[6]) + (A_mat[8, 7] * x_hat[7]) + (A_mat[8, 8] * x_hat[8]) +
             (B_mat[8, 1] * u_vec[1]) + (B_mat[8, 2] * u_vec[2]) + (B_mat[8, 3] * u_vec[3]) + (B_mat[8, 4] * u_vec[4]) +
             (B_mat[8, 5] * u_vec[5]);

(* ---------------------------------------------------------------------------------------------------------------------
 * SECTION 2.4: MEASUREMENT PREDICTION (y_pred = C * x_pred + D * u)
 * --------------------------------------------------------------------------------------------------------------------- *)
y_pred[1] := (C_mat[1, 1] * x_pred[1]) + (C_mat[1, 2] * x_pred[2]) + (C_mat[1, 3] * x_pred[3]) + (C_mat[1, 4] * x_pred[4]) +
             (C_mat[1, 5] * x_pred[5]) + (C_mat[1, 6] * x_pred[6]) + (C_mat[1, 7] * x_pred[7]) + (C_mat[1, 8] * x_pred[8]) +
             (D_mat[1, 1] * u_vec[1]) + (D_mat[1, 2] * u_vec[2]) + (D_mat[1, 3] * u_vec[3]) + (D_mat[1, 4] * u_vec[4]) +
             (D_mat[1, 5] * u_vec[5]);

y_pred[2] := (C_mat[2, 1] * x_pred[1]) + (C_mat[2, 2] * x_pred[2]) + (C_mat[2, 3] * x_pred[3]) + (C_mat[2, 4] * x_pred[4]) +
             (C_mat[2, 5] * x_pred[5]) + (C_mat[2, 6] * x_pred[6]) + (C_mat[2, 7] * x_pred[7]) + (C_mat[2, 8] * x_pred[8]) +
             (D_mat[2, 1] * u_vec[1]) + (D_mat[2, 2] * u_vec[2]) + (D_mat[2, 3] * u_vec[3]) + (D_mat[2, 4] * u_vec[4]) +
             (D_mat[2, 5] * u_vec[5]);

y_pred[3] := (C_mat[3, 1] * x_pred[1]) + (C_mat[3, 2] * x_pred[2]) + (C_mat[3, 3] * x_pred[3]) + (C_mat[3, 4] * x_pred[4]) +
             (C_mat[3, 5] * x_pred[5]) + (C_mat[3, 6] * x_pred[6]) + (C_mat[3, 7] * x_pred[7]) + (C_mat[3, 8] * x_pred[8]) +
             (D_mat[3, 1] * u_vec[1]) + (D_mat[3, 2] * u_vec[2]) + (D_mat[3, 3] * u_vec[3]) + (D_mat[3, 4] * u_vec[4]) +
             (D_mat[3, 5] * u_vec[5]);

y_pred[4] := (C_mat[4, 1] * x_pred[1]) + (C_mat[4, 2] * x_pred[2]) + (C_mat[4, 3] * x_pred[3]) + (C_mat[4, 4] * x_pred[4]) +
             (C_mat[4, 5] * x_pred[5]) + (C_mat[4, 6] * x_pred[6]) + (C_mat[4, 7] * x_pred[7]) + (C_mat[4, 8] * x_pred[8]) +
             (D_mat[4, 1] * u_vec[1]) + (D_mat[4, 2] * u_vec[2]) + (D_mat[4, 3] * u_vec[3]) + (D_mat[4, 4] * u_vec[4]) +
             (D_mat[4, 5] * u_vec[5]);

y_pred[5] := (C_mat[5, 1] * x_pred[1]) + (C_mat[5, 2] * x_pred[2]) + (C_mat[5, 3] * x_pred[3]) + (C_mat[5, 4] * x_pred[4]) +
             (C_mat[5, 5] * x_pred[5]) + (C_mat[5, 6] * x_pred[6]) + (C_mat[5, 7] * x_pred[7]) + (C_mat[5, 8] * x_pred[8]) +
             (D_mat[5, 1] * u_vec[1]) + (D_mat[5, 2] * u_vec[2]) + (D_mat[5, 3] * u_vec[3]) + (D_mat[5, 4] * u_vec[4]) +
             (D_mat[5, 5] * u_vec[5]);

(* ---------------------------------------------------------------------------------------------------------------------
 * SECTION 2.5: INNOVATION RESIDUAL CALCULATION (y_res = y_meas - y_pred)
 * --------------------------------------------------------------------------------------------------------------------- *)
y_res[1] := y_meas[1] - y_pred[1];
y_res[2] := y_meas[2] - y_pred[2];
y_res[3] := y_meas[3] - y_pred[3];
y_res[4] := y_meas[4] - y_pred[4];
y_res[5] := y_meas[5] - y_pred[5];

(* ---------------------------------------------------------------------------------------------------------------------
 * SECTION 2.6: EXPLICIT KALMAN FILTER STATE CORRECTION (x_hat = x_pred + L * y_res)
 * --------------------------------------------------------------------------------------------------------------------- *)
x_hat[1] := x_pred[1] + (L_mat[1, 1] * y_res[1]) + (L_mat[1, 2] * y_res[2]) + (L_mat[1, 3] * y_res[3]) + (L_mat[1, 4] * y_res[4]) + (L_mat[1, 5] * y_res[5]);
x_hat[2] := x_pred[2] + (L_mat[2, 1] * y_res[1]) + (L_mat[2, 2] * y_res[2]) + (L_mat[2, 3] * y_res[3]) + (L_mat[2, 4] * y_res[4]) + (L_mat[2, 5] * y_res[5]);
x_hat[3] := x_pred[3] + (L_mat[3, 1] * y_res[1]) + (L_mat[3, 2] * y_res[2]) + (L_mat[3, 3] * y_res[3]) + (L_mat[3, 4] * y_res[4]) + (L_mat[3, 5] * y_res[5]);
x_hat[4] := x_pred[4] + (L_mat[4, 1] * y_res[1]) + (L_mat[4, 2] * y_res[2]) + (L_mat[4, 3] * y_res[3]) + (L_mat[4, 4] * y_res[4]) + (L_mat[4, 5] * y_res[5]);
x_hat[5] := x_pred[5] + (L_mat[5, 1] * y_res[1]) + (L_mat[5, 2] * y_res[2]) + (L_mat[5, 3] * y_res[3]) + (L_mat[5, 4] * y_res[4]) + (L_mat[5, 5] * y_res[5]);
x_hat[6] := x_pred[6] + (L_mat[6, 1] * y_res[1]) + (L_mat[6, 2] * y_res[2]) + (L_mat[6, 3] * y_res[3]) + (L_mat[6, 4] * y_res[4]) + (L_mat[6, 5] * y_res[5]);
x_hat[7] := x_pred[7] + (L_mat[7, 1] * y_res[1]) + (L_mat[7, 2] * y_res[2]) + (L_mat[7, 3] * y_res[3]) + (L_mat[7, 4] * y_res[4]) + (L_mat[7, 5] * y_res[5]);
x_hat[8] := x_pred[8] + (L_mat[8, 1] * y_res[1]) + (L_mat[8, 2] * y_res[2]) + (L_mat[8, 3] * y_res[3]) + (L_mat[8, 4] * y_res[4]) + (L_mat[8, 5] * y_res[5]);

(* Map filtered state estimates to external diagnostic outputs *)
rState_Est_Level_NR            := x_hat[1];
rState_Est_Downcomer_Flow      := x_hat[2];
rState_Est_Riser_Void_Fraction := x_hat[3];
rState_Est_Primary_Heat_MW     := x_hat[4];
rState_Est_Drum_Pressure       := x_hat[5];
rState_Est_ColdLeg_Temp        := x_hat[6];
rState_Est_FeedValve_Trim      := x_hat[7];
rState_Est_ShrinkSwell_Bias    := x_hat[8];
""")
    return "\n".join(code)

if __name__ == "__main__":
    s = get_phase2_thermo_state_space()
    print("Phase 2 State-Space length:", len(s))
