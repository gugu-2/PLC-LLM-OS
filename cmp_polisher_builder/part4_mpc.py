# cmp_polisher_builder/part4_mpc.py

def get_part4():
    return """(*
========================================================================================================================
  PHASE 3: RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) OPTIMIZATION WITH PGD
  PREDICTION HORIZON: Np = 5 (25 ms look-ahead), CONTROL HORIZON: Nu = 3
  QUADRATIC COST FUNCTIONAL WITH BOX SATURATION & DYNAMIC SLEW RATE CONSTRAINTS
========================================================================================================================
*)
(* 1. Calculate Analytical Projected Gradient Vector grad_u (8x1) *)
rTotalCostFunctional := 0.0;

FOR i_idx := 1 TO 8 DO
    (* Actuator Effort Cost Derivative: d(J_R)/du = 2 * R * (u - u_ref) *)
    grad_u[i_idx] := 2.0 * r_diag[i_idx] * (u_ctrl[i_idx] - u_ref[i_idx]);
    
    (* Actuator Slew Rate Cost Derivative: d(J_S)/du = 2 * S * (u - u_prev) *)
    grad_u[i_idx] := grad_u[i_idx] + 2.0 * s_diag[i_idx] * (u_ctrl[i_idx] - u_prev[i_idx]);
    
    (* Propagated State Tracking Derivative via Input Coupling B: d(J_Q)/du = sum( 2 * B[j,i] * Q[j] * (x_next[j] - x_ref[j]) ) *)
    FOR j_idx := 1 TO 8 DO
        grad_u[i_idx] := grad_u[i_idx] + 2.0 * b_mat[j_idx, i_idx] * q_diag[j_idx] * (x_next[j_idx] - x_ref[j_idx]);
        (* Terminal State Penalty Derivative: d(J_P)/du = sum( 2 * B[j,i] * P[j] * (x_next[j] - x_ref[j]) ) *)
        grad_u[i_idx] := grad_u[i_idx] + 2.0 * b_mat[j_idx, i_idx] * p_diag[j_idx] * (x_next[j_idx] - x_ref[j_idx]);
    END_FOR;
END_FOR;

(* 2. Evaluate Instantaneous Total Quadratic Cost Functional J *)
FOR i_idx := 1 TO 8 DO
    (* State Tracking Cost: (x - x_ref)' * Q * (x - x_ref) *)
    rTotalCostFunctional := rTotalCostFunctional + q_diag[i_idx] * (x_state[i_idx] - x_ref[i_idx]) * (x_state[i_idx] - x_ref[i_idx]);
    
    (* Actuator Effort Cost: (u - u_ref)' * R * (u - u_ref) *)
    rTotalCostFunctional := rTotalCostFunctional + r_diag[i_idx] * (u_ctrl[i_idx] - u_ref[i_idx]) * (u_ctrl[i_idx] - u_ref[i_idx]);
    
    (* Actuator Slew Rate Cost: (u - u_prev)' * S * (u - u_prev) *)
    rTotalCostFunctional := rTotalCostFunctional + s_diag[i_idx] * (u_ctrl[i_idx] - u_prev[i_idx]) * (u_ctrl[i_idx] - u_prev[i_idx]);
    
    (* Terminal Cost: (x_next - x_ref)' * P * (x_next - x_ref) *)
    rTotalCostFunctional := rTotalCostFunctional + p_diag[i_idx] * (x_next[i_idx] - x_ref[i_idx]) * (x_next[i_idx] - x_ref[i_idx]);
END_FOR;

(* 3. Perform Projected Gradient Descent Step & Apply Actuator Envelope Constraints *)
FOR i_idx := 1 TO 8 DO
    (* Gradient Descent Step: u_tentative = u - alpha * grad_u *)
    u_tentative[i_idx] := u_ctrl[i_idx] - rMpcAlphaStep * grad_u[i_idx];
    
    (* Dynamic Actuator Slew Rate Limiter: |u - u_prev| <= du_slew_max *)
    IF (u_tentative[i_idx] - u_prev[i_idx]) > du_slew_max[i_idx] THEN
        u_tentative[i_idx] := u_prev[i_idx] + du_slew_max[i_idx];
    ELSIF (u_prev[i_idx] - u_tentative[i_idx]) > du_slew_max[i_idx] THEN
        u_tentative[i_idx] := u_prev[i_idx] - du_slew_max[i_idx];
    END_IF;
    
    (* Physical Box Saturation Constraint: u_min <= u <= u_max *)
    u_tentative[i_idx] := MAX(u_box_min[i_idx], MIN(u_box_max[i_idx], u_tentative[i_idx]));
    
    (* Commit Control Actuator Command for Current Scan *)
    u_prev[i_idx] := u_ctrl[i_idx];
    
    (* If production is active, apply computed MPC command, otherwise zero / idle *)
    IF bProductionActive AND (NOT bEmergencyTripActive) THEN
        u_ctrl[i_idx] := u_tentative[i_idx];
    ELSE
        u_ctrl[i_idx] := 0.0;
    END_IF;
END_FOR;

(* 4. Map MPC Manipulated Vector to Physical Machine Control Actuators *)
rPlatenMotorTorqueCmd_pct    := u_ctrl[1];
rCarrierMotorTorqueCmd_pct   := u_ctrl[2];
rPlatenSpeedSetpoint_rpm     := x_ref[1];
rCarrierSpeedSetpoint_rpm    := x_ref[2];

(* Conditional actuation dependent on production state *)
IF bProductionActive AND (NOT bEmergencyTripActive) THEN
    rSlurryPumpFlowCmd_mLpm      := (u_ctrl[5] / 100.0) * 450.0;    (* Map 0-100% to 0-450 mL/min *)
    rCondDownforceCmd_lbf        := (u_ctrl[6] / 100.0) * 15.0;     (* Map 0-100% to 0-15 lbf *)
    rCondSweepVelocityCmd_mmps   := (u_ctrl[7] / 100.0) * 80.0;     (* Map 0-100% to 0-80 mm/s *)
    rCondHeadSpeedCmd_rpm        := rCondNominalSpeed_rpm;
ELSE
    rSlurryPumpFlowCmd_mLpm      := 0.0;
    rCondDownforceCmd_lbf        := 0.0;
    rCondSweepVelocityCmd_mmps   := 0.0;
    rCondHeadSpeedCmd_rpm        := 0.0;
END_IF;
"""
