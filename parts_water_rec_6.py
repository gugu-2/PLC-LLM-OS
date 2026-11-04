# parts_water_rec_6.py - PHASE 3: DISCRETE STATE-SPACE PROPAGATION & RECEDING-HORIZON MPC OPTIMIZER

def get_phase3_mpc():
    code = []
    code.append("""(* =====================================================================================================================
 * PHASE 3: DISCRETE 8x8 CYBER-PHYSICAL STATE-SPACE PROPAGATION & RECEDING-HORIZON MPC OPTIMIZER
 * Formulates x[k+1] = A*x[k] + B*u[k] and executes multi-variable quadratic optimization with active-set box
 * constraints and strict actuator slew-rate limitation to eliminate membrane hydraulic water hammer.
 * ===================================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------------------------
 * SUBSECTION 3.1: STATE-SPACE MATRIX INITIALIZATION (DISCRETE TIME Ts = 50 ms)
 * --------------------------------------------------------------------------------------------------------------------- *)
(* State A Matrix Row 1: MABR Bulk Liquid Dissolved Oxygen Dynamics *)
A_mat[1,1] := 0.9450; A_mat[1,2] := -0.0120; A_mat[1,3] := 0.0000; A_mat[1,4] := 0.0000;
A_mat[1,5] := 0.0000; A_mat[1,6] :=  0.0000; A_mat[1,7] := 0.0000; A_mat[1,8] := 0.0000;

(* State A Matrix Row 2: MABR Ammonium Nitrogen (NH4-N) Consumption Dynamics *)
A_mat[2,1] := -0.0350; A_mat[2,2] := 0.9650; A_mat[2,3] := 0.0000; A_mat[2,4] := 0.0000;
A_mat[2,5] :=  0.0000; A_mat[2,6] := 0.0000; A_mat[2,7] := 0.0000; A_mat[2,8] := 0.0000;

(* State A Matrix Row 3: MABR Nitrate Nitrogen (NOx-N) Denitrification Dynamics *)
A_mat[3,1] := 0.0280; A_mat[3,2] := 0.0420; A_mat[3,3] := 0.9380; A_mat[3,4] := 0.0000;
A_mat[3,5] := 0.0000; A_mat[3,6] := 0.0000; A_mat[3,7] := 0.0000; A_mat[3,8] := 0.0000;

(* State A Matrix Row 4: Submerged UF Transmembrane Pressure (TMP) Dynamics *)
A_mat[4,1] := 0.0000; A_mat[4,2] := 0.0000; A_mat[4,3] := 0.0000; A_mat[4,4] := 0.9820;
A_mat[4,5] := 0.0045; A_mat[4,6] := 0.0000; A_mat[4,7] := 0.0000; A_mat[4,8] := 0.0000;

(* State A Matrix Row 5: UF Membrane Foulant Cake Layer Thickness Dynamics *)
A_mat[5,1] := 0.0000; A_mat[5,2] := 0.0000; A_mat[5,3] := 0.0000; A_mat[5,4] := 0.0012;
A_mat[5,5] := 0.9910; A_mat[5,6] := 0.0000; A_mat[5,7] := 0.0000; A_mat[5,8] := 0.0000;

(* State A Matrix Row 6: RO High-Pressure Feed Hydraulic Dynamics *)
A_mat[6,1] := 0.0000; A_mat[6,2] := 0.0000; A_mat[6,3] := 0.0000; A_mat[6,4] := 0.0000;
A_mat[6,5] := 0.0000; A_mat[6,6] := 0.9250; A_mat[6,7] := 0.0000; A_mat[6,8] := 0.0150;

(* State A Matrix Row 7: RO Permeate Electrical Conductivity Purity Dynamics *)
A_mat[7,1] := 0.0000; A_mat[7,2] := 0.0000; A_mat[7,3] := 0.0000; A_mat[7,4] := 0.0000;
A_mat[7,5] := 0.0000; A_mat[7,6] := -0.0240; A_mat[7,7] := 0.9620; A_mat[7,8] := 0.0080;

(* State A Matrix Row 8: ERD Ceramic Rotor Rotational Momentum Dynamics *)
A_mat[8,1] := 0.0000; A_mat[8,2] := 0.0000; A_mat[8,3] := 0.0000; A_mat[8,4] := 0.0000;
A_mat[8,5] := 0.0000; A_mat[8,6] := 0.4200; A_mat[8,7] := 0.0000; A_mat[8,8] := 0.9540;

(* Control Coupling B Matrix: u = [AirValve, RecycleRPM, UFSuct, UFAir, HPFeed, ERDBoost, BrineVlv, Antiscalant] *)
B_mat[1,1] :=  0.0240; B_mat[1,2] := -0.0004; B_mat[1,3] :=  0.0000; B_mat[1,4] :=  0.0000; B_mat[1,5] :=  0.0000; B_mat[1,6] :=  0.0000; B_mat[1,7] :=  0.0000; B_mat[1,8] :=  0.0000;
B_mat[2,1] := -0.0180; B_mat[2,2] :=  0.0012; B_mat[2,3] :=  0.0000; B_mat[2,4] :=  0.0000; B_mat[2,5] :=  0.0000; B_mat[2,6] :=  0.0000; B_mat[2,7] :=  0.0000; B_mat[2,8] :=  0.0000;
B_mat[3,1] :=  0.0120; B_mat[3,2] := -0.0025; B_mat[3,3] :=  0.0000; B_mat[3,4] :=  0.0000; B_mat[3,5] :=  0.0000; B_mat[3,6] :=  0.0000; B_mat[3,7] :=  0.0000; B_mat[3,8] :=  0.0000;
B_mat[4,1] :=  0.0000; B_mat[4,2] :=  0.0000; B_mat[4,3] :=  0.0150; B_mat[4,4] := -0.0080; B_mat[4,5] :=  0.0000; B_mat[4,6] :=  0.0000; B_mat[4,7] :=  0.0000; B_mat[4,8] :=  0.0000;
B_mat[5,1] :=  0.0000; B_mat[5,2] :=  0.0000; B_mat[5,3] :=  0.0220; B_mat[5,4] := -0.0450; B_mat[5,5] :=  0.0000; B_mat[5,6] :=  0.0000; B_mat[5,7] :=  0.0000; B_mat[5,8] :=  0.0000;
B_mat[6,1] :=  0.0000; B_mat[6,2] :=  0.0000; B_mat[6,3] :=  0.0000; B_mat[6,4] :=  0.0000; B_mat[6,5] :=  0.6800; B_mat[6,6] :=  0.2200; B_mat[6,7] := -0.1500; B_mat[6,8] :=  0.0000;
B_mat[7,1] :=  0.0000; B_mat[7,2] :=  0.0000; B_mat[7,3] :=  0.0000; B_mat[7,4] :=  0.0000; B_mat[7,5] := -0.1200; B_mat[7,6] := -0.0400; B_mat[7,7] :=  0.0800; B_mat[7,8] := -0.0650;
B_mat[8,1] :=  0.0000; B_mat[8,2] :=  0.0000; B_mat[8,3] :=  0.0000; B_mat[8,4] :=  0.0000; B_mat[8,5] :=  4.5000; B_mat[8,6] :=  2.8000; B_mat[8,7] := -3.2000; B_mat[8,8] :=  0.0000;

(* MPC Quadratic Cost Penalty Matrices *)
Q_diag[1] := 35.0;  (* MABR Dissolved Oxygen Target Tracking Weight *)
Q_diag[2] := 95.0;  (* Effluent Ammonium Nitrogen Violation Weight *)
Q_diag[3] := 70.0;  (* Effluent Nitrate Nitrogen Violation Weight *)
Q_diag[4] := 55.0;  (* UF Transmembrane Pressure Surge Penalty Weight *)
Q_diag[5] := 45.0;  (* UF Membrane Cake Resistance Penalty Weight *)
Q_diag[6] := 65.0;  (* RO High-Pressure Feed Stabilization Weight *)
Q_diag[7] := 115.0; (* RO Permeate Electrical Purity Violation Weight *)
Q_diag[8] := 25.0;  (* ERD Isobaric Rotor RPM Stability Weight *)

R_diag[1] := 4.5;   (* MABR Lumen Air Valve Slew Effort Penalty *)
R_diag[2] := 1.8;   (* MABR Chemostat Recycle Pump Slew Effort Penalty *)
R_diag[3] := 8.5;   (* UF Suction Pump VFD Slew Effort Penalty *)
R_diag[4] := 3.2;   (* UF Cyclic Aeration Scour Valve Slew Penalty *)
R_diag[5] := 28.0;  (* RO HP Feed Pump VFD Slew Penalty (Strictly Guarded to Prevent Rupture) *)
R_diag[6] := 14.0;  (* ERD Booster Pump VFD Slew Penalty *)
R_diag[7] := 18.0;  (* RO Brine Throttle Valve Slew Penalty *)
R_diag[8] := 3.8;   (* Antiscalant Chemical Metering Pump Slew Penalty *)

(* Actuator Maximum Slew-Rate Limits Per Scan Cycle (Protection Against Water Hammer) *)
u_max_slew[1] := 4.0;   (* MABR Air Valve Max 4.0% per scan *)
u_max_slew[2] := 45.0;  (* MABR Recycle Pump Max 45 RPM per scan *)
u_max_slew[3] := 2.5;   (* UF Suction Pump Max 2.5% per scan *)
u_max_slew[4] := 10.0;  (* UF Air Scour Valve Max 10.0% per scan *)
u_max_slew[5] := 1.2;   (* RO HP Feed Pump Max 1.2% per scan (Controlled Soft Ramp) *)
u_max_slew[6] := 2.0;   (* ERD Booster Pump Max 2.0% per scan *)
u_max_slew[7] := 1.8;   (* Brine Valve Max 1.8% per scan *)
u_max_slew[8] := 5.0;   (* Antiscalant Pump Max 5.0% per scan *)

(* Actuator Physical Saturation Bounds [Low, High] *)
u_bound_low[1] := 5.0;   u_bound_high[1] := 100.0;
u_bound_low[2] := 100.0; u_bound_high[2] := 1800.0;
u_bound_low[3] := 0.0;   u_bound_high[3] := 100.0;
u_bound_low[4] := 0.0;   u_bound_high[4] := 100.0;
u_bound_low[5] := 0.0;   u_bound_high[5] := 100.0;
u_bound_low[6] := 0.0;   u_bound_high[6] := 100.0;
u_bound_low[7] := 5.0;   u_bound_high[7] := 95.0;
u_bound_low[8] := 0.0;   u_bound_high[8] := 100.0;

(* ---------------------------------------------------------------------------------------------------------------------
 * SUBSECTION 3.2: CURRENT STATE VECTOR MAPPING & TARGET SETPOINTS
 * --------------------------------------------------------------------------------------------------------------------- *)
x_state[1] := rVoted_MABR_DO;
x_state[2] := rVoted_MABR_NH4;
x_state[3] := rVoted_MABR_NO3;
x_state[4] := rVoted_UF_TMP;
x_state[5] := rUF_Cake_Resistance_Accum / 1.0E11; (* Normalized scaling for state matrix conditioning *)
x_state[6] := rVoted_RO_HP_Feed;
x_state[7] := rVoted_RO_Cond;
x_state[8] := rST_ERD_ROTOR_RPM_504;

x_ref[1] := rSP_MABR_DO_Target;
x_ref[2] := 1.20;   (* Effluent Ammonium Nitrogen Target [mg/L] *)
x_ref[3] := 5.50;   (* Effluent Nitrate Nitrogen Target [mg/L] *)
x_ref[4] := 0.22;   (* UF Permeate TMP Target [bar] *)
x_ref[5] := 3.00;   (* UF Cake Layer Resistance Target [scaled] *)
x_ref[6] := rSP_RO_HP_Pressure_Target;
x_ref[7] := 18.0;   (* Permeate Electrical Purity Target [uS/cm] *)
x_ref[8] := rERD_Target_RPM;

(* Map current actuator feedback commands *)
u_curr[1] := rCmd_MABR_LumenAir_Valve_Pct;
u_curr[2] := rCmd_MABR_InternalRecycle_RPM;
u_curr[3] := rCmd_UF_PermeateSuction_VFD_Pct;
u_curr[4] := rCmd_UF_AirScour_Valve_Pct;
u_curr[5] := rCmd_RO_HP_FeedPump_VFD_Pct;
u_curr[6] := rCmd_RO_ERD_BoosterPump_VFD_Pct;
u_curr[7] := rCmd_RO_BrineReject_Throttle_Pct;
u_curr[8] := rCmd_RO_Antiscalant_Dosing_Pct;

(* ---------------------------------------------------------------------------------------------------------------------
 * SUBSECTION 3.3: DISCRETE STATE FORWARD PREDICTION: x_pred = A * x + B * u
 * --------------------------------------------------------------------------------------------------------------------- *)
FOR iIdx := 1 TO 8 DO
    x_pred[iIdx] := 0.0;
    FOR jIdx := 1 TO 8 DO
        x_pred[iIdx] := x_pred[iIdx] + (A_mat[iIdx, jIdx] * x_state[jIdx]) + (B_mat[iIdx, jIdx] * u_curr[jIdx]);
    END_FOR;
    x_err[iIdx] := x_pred[iIdx] - x_ref[iIdx];
END_FOR;

(* ---------------------------------------------------------------------------------------------------------------------
 * SUBSECTION 3.4: RECEDING-HORIZON QUADRATIC OPTIMIZATION WITH ACTIVE-SET SLEW CLAMPING
 * --------------------------------------------------------------------------------------------------------------------- *)
(* Initialize optimal control adjustment vectors *)
FOR iIdx := 1 TO 8 DO
    u_delta[iIdx] := 0.0;
END_FOR;

(* 6-Iteration Projected Gradient Descent Optimization *)
FOR iMPC_Iter := 1 TO 6 DO
    FOR iIdx := 1 TO 8 DO
        rGrad_Vec[iIdx] := 0.0;
        FOR jIdx := 1 TO 8 DO
            rGrad_Vec[iIdx] := rGrad_Vec[iIdx] + (B_mat[jIdx, iIdx] * Q_diag[jIdx] * x_err[jIdx]);
        END_FOR;
        rGrad_Vec[iIdx] := rGrad_Vec[iIdx] + (R_diag[iIdx] * u_delta[iIdx]);

        (* Gradient descent step update with learning coefficient *)
        u_delta[iIdx] := u_delta[iIdx] - (rMPC_Alpha_Step * rGrad_Vec[iIdx]);

        (* Enforce hard actuator slew-rate constraints *)
        u_delta[iIdx] := LIMIT(-1.0 * u_max_slew[iIdx], u_delta[iIdx], u_max_slew[iIdx]);
    END_FOR;
END_FOR;

(* Synthesize optimal actuator command targets with physical box bounding *)
FOR iIdx := 1 TO 8 DO
    u_opt[iIdx] := u_curr[iIdx] + u_delta[iIdx];
    u_opt[iIdx] := LIMIT(u_bound_low[iIdx], u_opt[iIdx], u_bound_high[iIdx]);
END_FOR;
\n""")
    return "".join(code)
