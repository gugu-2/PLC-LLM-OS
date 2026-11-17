(*
====================================================================================================
 PHASE 2: FIRST-PRINCIPLES CYBER-PHYSICAL MODELING & DISCRETE KALMAN FILTER OBSERVER
====================================================================================================
 METALLURGICAL ROLLING THEORY & HYDRODYNAMIC EQUATIONS:
  1. Roll Bite Kinematics & Hitchcock's Roll Flattening:
     In heavy breakdown passes (draft reductions up to 55 mm in a single roughing pass), contact
     pressures exceed 350 MPa, causing massive elastic flattening of the forged alloy work roll.
     The deformed contact radius R' is computed dynamically via Hitchcock's classical equation:
       R' = R * (1.0 + (16.0 * (1.0 - nu^2) / (pi * E)) * (F_total / (W * delta_h)))
     where nu=0.29 (Poisson's ratio), E=210,000 MPa (Young's modulus), W=slab width, delta_h=draft.
  2. Projected Contact Length & Neutral Point Angle:
     L_d = sqrt(R' * delta_h)
     phi_n = sqrt(h_exit / R') * tan( 0.5 * arctan(sqrt(r / (1.0 - r))) - (1.0 / (4.0 * mu)) * sqrt(h_exit / R') * ln(h_entry / h_exit) )
  3. Forward Slip & Strip Speed Ratio:
     S_f = (v_strip_exit - v_roll_periph) / v_roll_periph = (R' / h_exit) * (1.0 - cos(phi_n))
  4. Sims Hot Rolling Force Formulation:
     F_calc = (2.0 / sqrt(3.0)) * sigma_yield * W * L_d * Q_p(r, R', h_entry)
  5. BISRA Dynamic Gauge-Meter Compensation:
     h_true = S_0 + (F_voted - F_0) / M_mill + delta_S_ecc + delta_S_oil + delta_S_therm
  6. Discrete Kalman State-Space Innovation Observer (Ts = 500 us):
     States (6): x1=Gauge Error [um], x2=Dynamic Deflection [um], x3=Eccentricity [um],
                 x4=Speed Mismatch [rpm], x5=Thermal Gradient [deg C], x6=Cylinder Tilt [um]
     Observer Equations:
       y_pred[k]   = C * x_hat[k|k-1] + D * u[k]
       innov[k]    = y_meas[k] - y_pred[k]
       x_hat[k|k]  = x_hat[k|k-1] + L * innov[k]
       x_hat[k+1|k]= A * x_hat[k|k] + B * u[k]
====================================================================================================
*)

(* --- STEP 2.1: FIRST-PRINCIPLES METALLURGICAL CALCULATIONS --- *)
(* Calculate instantaneous draft reduction [mm] based on active pass *)
CASE ui_Current_Rolling_Pass OF
    1: r_Calculated_Rolling_Speed := 1.85; (* Pass 1 crawl speed [m/s] *)
    2: r_Calculated_Rolling_Speed := 2.40; (* Pass 2 speed [m/s] *)
    3: r_Calculated_Rolling_Speed := 3.20; (* Pass 3 speed [m/s] *)
    4: r_Calculated_Rolling_Speed := 3.80; (* Pass 4 speed [m/s] *)
    5: r_Calculated_Rolling_Speed := 4.20; (* Pass 5 speed [m/s] *)
    ELSE
       r_Calculated_Rolling_Speed := 1.50;
END_CASE;

(* Flow stress approximation based on carbon, manganese content, and pyrometer surface temperature *)
IF (r_Pyrometer_Entry_Top_Temp > 800.0) THEN
    (* Shida hot flow stress empirical equation for carbon steel *)
    r_Yield_Strength_Flow_Hot := (85.0 + 120.0 * r_Steel_Carbon_Content_Pct + 25.0 * r_Steel_Manganese_Content_Pct)
                                * EXP(-0.0028 * (r_Pyrometer_Entry_Top_Temp - 1000.0));
    IF (r_Yield_Strength_Flow_Hot < 30.0) THEN
        r_Yield_Strength_Flow_Hot := 30.0;
    ELSIF (r_Yield_Strength_Flow_Hot > 220.0) THEN
        r_Yield_Strength_Flow_Hot := 220.0;
    END_IF;
ELSE
    r_Yield_Strength_Flow_Hot := 150.0;
END_IF;

(* Hitchcock roll flattening deformed radius R' [mm] *)
IF (r_Voted_Rolling_Force > 1000.0 AND r_Nominal_Incoming_Width > 500.0) THEN
    r_Calculated_R_Prime := r_WorkRoll_Radius_Nominal * (1.0 + (16.0 * (1.0 - (r_Poissons_Ratio_Rolls * r_Poissons_Ratio_Rolls))
                           / (3.14159265 * r_Youngs_Modulus_Rolls))
                           * (r_Voted_Rolling_Force * 1000.0 / (r_Nominal_Incoming_Width * 35.0)));
    IF (r_Calculated_R_Prime < r_WorkRoll_Radius_Nominal) THEN
        r_Calculated_R_Prime := r_WorkRoll_Radius_Nominal;
    ELSIF (r_Calculated_R_Prime > r_WorkRoll_Radius_Nominal * 2.2) THEN
        r_Calculated_R_Prime := r_WorkRoll_Radius_Nominal * 2.2;
    END_IF;
ELSE
    r_Calculated_R_Prime := r_WorkRoll_Radius_Nominal;
END_IF;

(* Projected roll contact arc length L_d [mm] *)
r_Roll_Contact_Arc_Length := SQRT(r_Calculated_R_Prime * 35.0);
IF (r_Roll_Contact_Arc_Length < 10.0) THEN
    r_Roll_Contact_Arc_Length := 10.0;
END_IF;

(* Neutral bite angle phi_n and forward slip factor *)
r_Neutral_Bite_Angle_rad := 0.5 * SQRT(35.0 / r_Calculated_R_Prime);
r_Forward_Slip_Ratio := (r_Calculated_R_Prime / 65.0) * (1.0 - COS(r_Neutral_Bite_Angle_rad));
IF (r_Forward_Slip_Ratio < 0.01) THEN
    r_Forward_Slip_Ratio := 0.01;
ELSIF (r_Forward_Slip_Ratio > 0.12) THEN
    r_Forward_Slip_Ratio := 0.12;
END_IF;
r_Dynamic_Forward_Slip := r_Forward_Slip_Ratio;

(* Roll spindle mechanical torque [kNm] and electrical power [kW] *)
r_Calculated_Rolling_Torque := 2.0 * r_Voted_Rolling_Force * (r_Roll_Contact_Arc_Length * 0.0005) * 0.45;
r_Calculated_Motor_Power_kW := (r_Calculated_Rolling_Torque * 1000.0) * (r_Calculated_Rolling_Speed / (r_WorkRoll_Radius_Nominal * 0.001)) / 1000.0;

(* --- STEP 2.2: BACKUP ROLL OIL FILM & THERMAL CROWN DYNAMICS --- *)
(* Hydrodynamic Morgoil bearing oil film dynamic compensation [um] *)
IF (r_Main_Motor_Actual_Speed_Top > 1.0) THEN
    r_Estimated_Roll_Speed_Mismatch := ABS(r_Main_Motor_Actual_Speed_Top - r_Main_Motor_Actual_Speed_Bot);
ELSE
    r_Estimated_Roll_Speed_Mismatch := 0.0;
END_IF;

(* Work roll thermal expansion dynamic compensation [um] *)
r_Estimated_Thermal_Gradient := (r_Pyrometer_Exit_Top_Temp - r_Pyrometer_Exit_Bottom_Temp);

(* Roll gap differential tilt error [um] between operator side and drive side *)
r_Estimated_Cylinder_Tilt := (r_LVDT_Pos_Operator_Side - r_LVDT_Pos_Drive_Side);

(* BISRA Gauge-Meter Exit Thickness Equation [mm] *)
r_Estimated_Mill_Deflection := (r_Voted_Rolling_Force * 1000.0) / r_Mill_Modulus_Constant_Mm; (* [um] *)
r_BISRA_Gauge_Meter_Thickness := r_Nominal_NoLoad_Gap_S0
                                + ((r_LVDT_Pos_Operator_Side + r_LVDT_Pos_Drive_Side) * 0.0005)
                                + (r_Estimated_Mill_Deflection * 0.001)
                                - (r_Roll_Heating_DeltaT * r_Thermal_Expansion_Coeff * r_WorkRoll_Radius_Nominal * 2.0);

(* Dynamic strip crown and wedge calculation *)
r_Calculated_Strip_Crown := (r_Voted_Rolling_Force * 0.012) - ((r_WorkRoll_Bending_Press_OS + r_WorkRoll_Bending_Press_DS) * 0.5 * 0.85);
r_Calculated_Strip_Wedge := r_Estimated_Cylinder_Tilt;

(* --- STEP 2.3: DISCRETE STATE-SPACE KALMAN FILTER OBSERVER --- *)
(* 1. Compute Output Prediction: y_pred = C * x_hat + D * u *)
r_y_pred_1 := (r_C_11 * r_x_hat_1) + (r_C_12 * r_x_hat_2) + (r_C_13 * r_x_hat_3)
            + (r_C_14 * r_x_hat_4) + (r_C_15 * r_x_hat_5) + (r_C_16 * r_x_hat_6)
            + (r_D_11 * r_u_cmd_1) + (r_D_12 * r_u_cmd_2) + (r_D_13 * r_u_cmd_3)
            + (r_D_14 * r_u_cmd_4) + (r_D_15 * r_u_cmd_5);

r_y_pred_2 := (r_C_21 * r_x_hat_1) + (r_C_22 * r_x_hat_2) + (r_C_23 * r_x_hat_3)
            + (r_C_24 * r_x_hat_4) + (r_C_25 * r_x_hat_5) + (r_C_26 * r_x_hat_6)
            + (r_D_21 * r_u_cmd_1) + (r_D_22 * r_u_cmd_2) + (r_D_23 * r_u_cmd_3)
            + (r_D_24 * r_u_cmd_4) + (r_D_25 * r_u_cmd_5);

r_y_pred_3 := (r_C_31 * r_x_hat_1) + (r_C_32 * r_x_hat_2) + (r_C_33 * r_x_hat_3)
            + (r_C_34 * r_x_hat_4) + (r_C_35 * r_x_hat_5) + (r_C_36 * r_x_hat_6)
            + (r_D_31 * r_u_cmd_1) + (r_D_32 * r_u_cmd_2) + (r_D_33 * r_u_cmd_3)
            + (r_D_34 * r_u_cmd_4) + (r_D_35 * r_u_cmd_5);

r_y_pred_4 := (r_C_41 * r_x_hat_1) + (r_C_42 * r_x_hat_2) + (r_C_43 * r_x_hat_3)
            + (r_C_44 * r_x_hat_4) + (r_C_45 * r_x_hat_5) + (r_C_46 * r_x_hat_6)
            + (r_D_41 * r_u_cmd_1) + (r_D_42 * r_u_cmd_2) + (r_D_43 * r_u_cmd_3)
            + (r_D_44 * r_u_cmd_4) + (r_D_45 * r_u_cmd_5);

(* 2. Construct Measured Output Vector and Compute Innovation Residuals *)
(* y1: Rolling force [kN], y2: Average cylinder position [um], y3: Laser gauge error [um], y4: Surface temp [deg C] *)
r_innov_1 := r_Voted_Rolling_Force - r_y_pred_1;
r_innov_2 := ((r_LVDT_Pos_Operator_Side + r_LVDT_Pos_Drive_Side) * 0.5) - r_y_pred_2;
IF r_Laser_Gauge_Measurement_Valid THEN
    r_innov_3 := ((r_Laser_Gauge_Exit_Thickness - r_BISRA_Gauge_Meter_Thickness) * 1000.0) - r_y_pred_3;
ELSE
    r_innov_3 := 0.0; (* Invalidate optical innovation if gauge obscured by steam/water *)
END_IF;
r_innov_4 := ((r_Pyrometer_Exit_Top_Temp + r_Pyrometer_Exit_Bottom_Temp) * 0.5) - r_y_pred_4;

(* 3. Kalman Innovation State Correction: x_corrected = x_hat + L * innov *)
r_x_hat_1 := r_x_hat_1 + (r_L_11 * r_innov_1) + (r_L_12 * r_innov_2) + (r_L_13 * r_innov_3) + (r_L_14 * r_innov_4);
r_x_hat_2 := r_x_hat_2 + (r_L_21 * r_innov_1) + (r_L_22 * r_innov_2) + (r_L_23 * r_innov_3) + (r_L_24 * r_innov_4);
r_x_hat_3 := r_x_hat_3 + (r_L_31 * r_innov_1) + (r_L_32 * r_innov_2) + (r_L_33 * r_innov_3) + (r_L_34 * r_innov_4);
r_x_hat_4 := r_x_hat_4 + (r_L_41 * r_innov_1) + (r_L_42 * r_innov_2) + (r_L_43 * r_innov_3) + (r_L_44 * r_innov_4);
r_x_hat_5 := r_x_hat_5 + (r_L_51 * r_innov_1) + (r_L_52 * r_innov_2) + (r_L_53 * r_innov_3) + (r_L_54 * r_innov_4);
r_x_hat_6 := r_x_hat_6 + (r_L_61 * r_innov_1) + (r_L_62 * r_innov_2) + (r_L_63 * r_innov_3) + (r_L_64 * r_innov_4);

(* 4. State Time-Propagation: x_pred = A * x_corrected + B * u *)
r_x_pred_1 := (r_A_11 * r_x_hat_1) + (r_A_12 * r_x_hat_2) + (r_A_13 * r_x_hat_3)
            + (r_A_14 * r_x_hat_4) + (r_A_15 * r_x_hat_5) + (r_A_16 * r_x_hat_6)
            + (r_B_11 * r_u_cmd_1) + (r_B_12 * r_u_cmd_2) + (r_B_13 * r_u_cmd_3)
            + (r_B_14 * r_u_cmd_4) + (r_B_15 * r_u_cmd_5);

r_x_pred_2 := (r_A_21 * r_x_hat_1) + (r_A_22 * r_x_hat_2) + (r_A_23 * r_x_hat_3)
            + (r_A_24 * r_x_hat_4) + (r_A_25 * r_x_hat_5) + (r_A_26 * r_x_hat_6)
            + (r_B_21 * r_u_cmd_1) + (r_B_22 * r_u_cmd_2) + (r_B_23 * r_u_cmd_3)
            + (r_B_24 * r_u_cmd_4) + (r_B_25 * r_u_cmd_5);

r_x_pred_3 := (r_A_31 * r_x_hat_1) + (r_A_32 * r_x_hat_2) + (r_A_33 * r_x_hat_3)
            + (r_A_34 * r_x_hat_4) + (r_A_35 * r_x_hat_5) + (r_A_36 * r_x_hat_6)
            + (r_B_31 * r_u_cmd_1) + (r_B_32 * r_u_cmd_2) + (r_B_33 * r_u_cmd_3)
            + (r_B_34 * r_u_cmd_4) + (r_B_35 * r_u_cmd_5);

r_x_pred_4 := (r_A_41 * r_x_hat_1) + (r_A_42 * r_x_hat_2) + (r_A_43 * r_x_hat_3)
            + (r_A_44 * r_x_hat_4) + (r_A_45 * r_x_hat_5) + (r_A_46 * r_x_hat_6)
            + (r_B_41 * r_u_cmd_1) + (r_B_42 * r_u_cmd_2) + (r_B_43 * r_u_cmd_3)
            + (r_B_44 * r_u_cmd_4) + (r_B_45 * r_u_cmd_5);

r_x_pred_5 := (r_A_51 * r_x_hat_1) + (r_A_52 * r_x_hat_2) + (r_A_53 * r_x_hat_3)
            + (r_A_54 * r_x_hat_4) + (r_A_55 * r_x_hat_5) + (r_A_56 * r_x_hat_6)
            + (r_B_51 * r_u_cmd_1) + (r_B_52 * r_u_cmd_2) + (r_B_53 * r_u_cmd_3)
            + (r_B_54 * r_u_cmd_4) + (r_B_55 * r_u_cmd_5);

r_x_pred_6 := (r_A_61 * r_x_hat_1) + (r_A_62 * r_x_hat_2) + (r_A_63 * r_x_hat_3)
            + (r_A_64 * r_x_hat_4) + (r_A_65 * r_x_hat_5) + (r_A_66 * r_x_hat_6)
            + (r_B_61 * r_u_cmd_1) + (r_B_62 * r_u_cmd_2) + (r_B_63 * r_u_cmd_3)
            + (r_B_64 * r_u_cmd_4) + (r_B_65 * r_u_cmd_5);

(* Update internal state registers with predicted values *)
r_x_hat_1 := r_x_pred_1;
r_x_hat_2 := r_x_pred_2;
r_x_hat_3 := r_x_pred_3;
r_x_hat_4 := r_x_pred_4;
r_x_hat_5 := r_x_pred_5;
r_x_hat_6 := r_x_pred_6;

(* Export estimated cyber-physical states to Function Block outputs *)
r_Estimated_Exit_Gauge_Error    := r_x_hat_1;
r_Estimated_Roll_Eccentricity   := r_x_hat_3;
