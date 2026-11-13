# parts_body2.py

PHASE2_STATESPACE_BLOCK = """
(* ==================================================================================================== *)
(* PHASE 2: FIRST-PRINCIPLES CYBER-PHYSICAL STATE-SPACE ESTIMATION & ADVANCED OBSERVERS                  *)
(* ==================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------- *)
(* 2.1: Multi-Node Lumped Parameter Spindle Thermal Observer (ISO 230-3 Formulation)                    *)
(* ---------------------------------------------------------------------------------------------------- *)
(* Calculate Instantaneous Electrical Inverter RMS Stator Current *)
rTempSum := (rSpindleCurrent_Iu_A * rSpindleCurrent_Iu_A) +
            (rSpindleCurrent_Iv_A * rSpindleCurrent_Iv_A) +
            (rSpindleCurrent_Iw_A * rSpindleCurrent_Iw_A);
rHeatLoss_StatorJoule_W := (SPINDLE_STATOR_RES_OHM * (1.0 + 0.00393 * (rNodeTemp_Stator_degC - 20.0))) * rTempSum;

(* Stator Core Magnetic Hysteresis and Eddy Current Iron Losses *)
rTempSum := (REAL_TO_INT(SPINDLE_POLE_PAIRS) * rVotedSpindleSpeed_rpm) / 60.0; (* Electrical Frequency f_e [Hz] *)
rHeatLoss_StatorIron_W := (0.85 * rTempSum) + (0.0038 * rTempSum * rTempSum);

(* Palmgren Bearing Viscous Friction Loss Formulations *)
rTempSum := (rVotedSpindleSpeed_rpm * 2.0 * 3.14159265) / 60.0; (* Mechanical omega [rad/s] *)
rHeatLoss_BearingFront_W := (0.000185 * (BEARING_PITCH_DIAMETER_M * BEARING_PITCH_DIAMETER_M * BEARING_PITCH_DIAMETER_M)) *
                            (rTempSum * rTempSum) + (0.0012 * BEARING_NOM_PRELOAD_N * BEARING_PITCH_DIAMETER_M * rTempSum);
rHeatLoss_BearingRear_W := 0.65 * rHeatLoss_BearingFront_W;

(* Closed-Loop Glycol Chiller Jacket Heat Extraction Rate *)
IF rChillerCoolantFlow_lmin > 0.5 THEN
    rHeatRemoval_Chiller_W := (rChillerCoolantFlow_lmin / 60.0) * 3850.0 * (rVotedStatorTemp_degC - rChillerInletTemp_degC);
    IF rHeatRemoval_Chiller_W < 0.0 THEN
        rHeatRemoval_Chiller_W := 0.0;
    END_IF;
ELSE
    rHeatRemoval_Chiller_W := 0.0;
END_IF;

(* Continuous Thermal State Numerical Integration across 5 Physical Nodes *)
(* Node 1: Spindle Rotor Core & Shaft Assembly *)
rNodeTemp_Rotor_degC := rNodeTemp_Rotor_degC + (T_CYCLE_SEC / C_TH_ROTOR_J_K) *
    ( (0.35 * rHeatLoss_StatorIron_W) -
      G_TH_ROTOR_TO_FRONT_W_K * (rNodeTemp_Rotor_degC - rNodeTemp_FrontBrg_degC) -
      G_TH_ROTOR_TO_REAR_W_K * (rNodeTemp_Rotor_degC - rNodeTemp_RearBrg_degC) );

(* Node 2: Stator Winding & Laminated Core Pack *)
rNodeTemp_Stator_degC := rNodeTemp_Stator_degC + (T_CYCLE_SEC / C_TH_STATOR_J_K) *
    ( rHeatLoss_StatorJoule_W + (0.65 * rHeatLoss_StatorIron_W) -
      G_TH_STATOR_TO_CHILLER_W_K * (rNodeTemp_Stator_degC - rChillerInletTemp_degC) -
      45.0 * (rNodeTemp_Stator_degC - rNodeTemp_Housing_degC) );

(* Node 3: Front Fixed Datum Ceramic Bearing Pack *)
rNodeTemp_FrontBrg_degC := rNodeTemp_FrontBrg_degC + (T_CYCLE_SEC / C_TH_FRONT_BRG_J_K) *
    ( rHeatLoss_BearingFront_W +
      G_TH_ROTOR_TO_FRONT_W_K * (rNodeTemp_Rotor_degC - rNodeTemp_FrontBrg_degC) -
      G_TH_FRONT_TO_HOUSING_W_K * (rNodeTemp_FrontBrg_degC - rNodeTemp_Housing_degC) );

(* Node 4: Rear Floating Ceramic Bearing Pack *)
rNodeTemp_RearBrg_degC := rNodeTemp_RearBrg_degC + (T_CYCLE_SEC / C_TH_REAR_BRG_J_K) *
    ( rHeatLoss_BearingRear_W +
      G_TH_ROTOR_TO_REAR_W_K * (rNodeTemp_Rotor_degC - rNodeTemp_RearBrg_degC) -
      G_TH_REAR_TO_HOUSING_W_K * (rNodeTemp_RearBrg_degC - rNodeTemp_Housing_degC) );

(* Node 5: Meehanite Cast Iron Ram Housing Carrier *)
rNodeTemp_Housing_degC := rNodeTemp_Housing_degC + (T_CYCLE_SEC / C_TH_HOUSING_J_K) *
    ( 45.0 * (rNodeTemp_Stator_degC - rNodeTemp_Housing_degC) +
      G_TH_FRONT_TO_HOUSING_W_K * (rNodeTemp_FrontBrg_degC - rNodeTemp_Housing_degC) +
      G_TH_REAR_TO_HOUSING_W_K * (rNodeTemp_RearBrg_degC - rNodeTemp_Housing_degC) -
      G_TH_HOUSING_TO_AIR_W_K * (rNodeTemp_Housing_degC - rAmbientTemp_degC) );

(* Resultant Cumulative Spindle Axial Thermal Growth Delta_Lz [um] *)
rThermalGrowth_Z_um := (ALPHA_STEEL_SHAFT_PER_K * ROTOR_ACTIVE_LENGTH_M * (rNodeTemp_Rotor_degC - rRefDatumTemp_degC) * 1.0E6) +
                       (ALPHA_CERAMIC_BRG_PER_K * 0.085 * (rNodeTemp_FrontBrg_degC - rRefDatumTemp_degC) * 1.0E6) -
                       (ALPHA_CAST_IRON_PER_K * RAM_EFFECTIVE_LENGTH_M * (rNodeTemp_Housing_degC - rRefDatumTemp_degC) * 1.0E6) -
                       (K_CENTRIFUGAL_CONTRACTION_UM * (rVotedSpindleSpeed_rpm * rVotedSpindleSpeed_rpm));

(* Spindle Nose Thermal Angular Pitch Tilt (A-Axis) and Yaw Tilt (C-Axis) [urad] *)
rThermalTilt_A_urad := ((rVotedFrontBearingTemp_degC - rVotedRearBearingTemp_degC) * 2.85) +
                       ((rNodeTemp_Housing_degC - rAmbientTemp_degC) * 1.15);
rThermalTilt_C_urad := ((rVotedStatorTemp_degC - rChillerInletTemp_degC) * 0.75);

(* Thermally Induced Dynamic Bearing Preload Variation [N] *)
rBearingPreloadDelta_N := (K_BEARING_PRELOAD_TEMP_N_K * (rNodeTemp_Rotor_degC - rVotedFrontBearingTemp_degC)) +
                          (K_BEARING_PRELOAD_SPEED_N_RPM * rVotedSpindleSpeed_rpm);

(* ---------------------------------------------------------------------------------------------------- *)
(* 2.2: Dynamic Cutting Force & Tool Tip Cantilever Deflection Observer                                 *)
(* ---------------------------------------------------------------------------------------------------- *)
(* Reconstruct Motor Electromagnetic Air-Gap Torque T_em [Nm] *)
rMotorTorque_EM_Nm := 1.5 * REAL_TO_INT(SPINDLE_POLE_PAIRS) * SPINDLE_PM_FLUX_WB *
                      (rSpindleCurrent_Iu_A * SIN(rVotedSpindleAngle_deg * 0.0174533) +
                       rSpindleCurrent_Iv_A * SIN((rVotedSpindleAngle_deg - 120.0) * 0.0174533) +
                       rSpindleCurrent_Iw_A * SIN((rVotedSpindleAngle_deg + 120.0) * 0.0174533));

(* Spindle Bearing and Windage Parasitic Torque Loss *)
rMotorTorque_Loss_Nm := 0.85 + (0.00035 * rVotedSpindleSpeed_rpm);

(* Tangential Cutting Force Component F_t [N] *)
IF rToolDiameter_mm > 1.0 THEN
    rTangentialCutForce_N := (rMotorTorque_EM_Nm - rMotorTorque_Loss_Nm) / (0.5 * rToolDiameter_mm * 1.0E-3);
    IF rTangentialCutForce_N < 0.0 THEN
        rTangentialCutForce_N := 0.0;
    END_IF;
ELSE
    rTangentialCutForce_N := 0.0;
END_IF;

(* Radial and Axial Proportional Cutting Force Components *)
rRadialCutForce_N := 0.380 * rTangentialCutForce_N;
rAxialCutForce_N  := 0.220 * rTangentialCutForce_N;

(* 3D Cutting Force Vector Components Resolved in Tool Coordinate Frame *)
rCuttingForce_Fx_N := (rTangentialCutForce_N * COS(rVotedSpindleAngle_deg * 0.0174533)) +
                      (rRadialCutForce_N * SIN(rVotedSpindleAngle_deg * 0.0174533));
rCuttingForce_Fy_N := (rTangentialCutForce_N * SIN(rVotedSpindleAngle_deg * 0.0174533)) -
                      (rRadialCutForce_N * COS(rVotedSpindleAngle_deg * 0.0174533));
rCuttingForce_Fz_N := rAxialCutForce_N;

(* Reconstructed Cutting Force Magnitude [N] *)
rCuttingForce_Magnitude_N := SQRT((rCuttingForce_Fx_N * rCuttingForce_Fx_N) +
                                  (rCuttingForce_Fy_N * rCuttingForce_Fy_N) +
                                  (rCuttingForce_Fz_N * rCuttingForce_Fz_N));

(* Tool Assembly Area Moment of Inertia I_tool = pi * D^4 / 64 [m4] *)
IF rToolDiameter_mm > 1.0 THEN
    rToolCantileverInertia_m4 := (3.14159265 * (rToolDiameter_mm * 1.0E-3) *
                                  (rToolDiameter_mm * 1.0E-3) *
                                  (rToolDiameter_mm * 1.0E-3) *
                                  (rToolDiameter_mm * 1.0E-3)) / 64.0;
ELSE
    rToolCantileverInertia_m4 := 1.0E-12;
END_IF;

(* Cantilever Beam Elastic Deflection delta = F * L^3 / (3 * E * I) [um] *)
rToolOverhang_m := rToolLength_mm * 1.0E-3;
IF rToolCantileverInertia_m4 > 1.0E-14 THEN
    rTempSum := (rToolOverhang_m * rToolOverhang_m * rToolOverhang_m) /
                (3.0 * TOOL_CARBIDE_YOUNGS_MOD_PA * rToolCantileverInertia_m4);
    rDeflectionCompOffset_X_um := -(rCuttingForce_Fx_N * rTempSum * 1.0E6 + (rSpindleNoseTiltAngle_Y_rad * rToolOverhang_m * 1.0E6));
    rDeflectionCompOffset_Y_um := -(rCuttingForce_Fy_N * rTempSum * 1.0E6 + (rSpindleNoseTiltAngle_X_rad * rToolOverhang_m * 1.0E6));
    rToolTipDeflection_um := SQRT((rDeflectionCompOffset_X_um * rDeflectionCompOffset_X_um) +
                                  (rDeflectionCompOffset_Y_um * rDeflectionCompOffset_Y_um));
ELSE
    rDeflectionCompOffset_X_um := 0.0;
    rDeflectionCompOffset_Y_um := 0.0;
    rToolTipDeflection_um := 0.0;
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* 2.3: Gantry Dual-Drive Synchronization & Cross-Coupling Yaw Decoupling                               *)
(* ---------------------------------------------------------------------------------------------------- *)
(* Calculate Dual-Drive Linear Scale Skew Differential (Master X1 vs Slave X2) *)
rGantryYaw_SkewError_mm := rLinearScale_X_ChA_mm - rLinearScale_X_ChB_mm;
rGantryCrossCouplingYaw_um := rGantryYaw_SkewError_mm * 1000.0;

(* Skew Derivative and Integral Dynamic Calculations *)
rGantryYaw_SkewVel_mms := (rGantryYaw_SkewError_mm - rGantryYaw_PrevSkew_mm) / T_CYCLE_SEC;
rGantryYaw_PrevSkew_mm := rGantryYaw_SkewError_mm;
rGantryYaw_SkewIntegral_mms := rGantryYaw_SkewIntegral_mms + (rGantryYaw_SkewError_mm * T_CYCLE_SEC);

(* Anti-Windup Clamping on Skew Integrator *)
IF rGantryYaw_SkewIntegral_mms > 25.0 THEN
    rGantryYaw_SkewIntegral_mms := 25.0;
ELSIF rGantryYaw_SkewIntegral_mms < -25.0 THEN
    rGantryYaw_SkewIntegral_mms := -25.0;
END_IF;

(* PID Electronic Line-Shafting Dynamic Yaw Restoring Force Command [N] *)
rGantryYawRestoringForce_N := (rKp_Yaw * rGantryYaw_SkewError_mm) +
                              (rKd_Yaw * rGantryYaw_SkewVel_mms) +
                              (rKi_Yaw * rGantryYaw_SkewIntegral_mms);

(* ---------------------------------------------------------------------------------------------------- *)
(* 2.4: 5-Axis Forward Kinematics Tool Center Point (TCP) Jacobian Transformation                       *)
(* ---------------------------------------------------------------------------------------------------- *)
rAngle_A_rad := rCmdPos_A_deg * 0.0174532925;
rAngle_C_rad := rCmdPos_C_deg * 0.0174532925;

(* Rotation Matrix R_A around X-Axis *)
rRotMat_A11 := 1.0;  rRotMat_A12 := 0.0;                 rRotMat_A13 := 0.0;
rRotMat_A21 := 0.0;  rRotMat_A22 := COS(rAngle_A_rad);   rRotMat_A23 := -SIN(rAngle_A_rad);
rRotMat_A31 := 0.0;  rRotMat_A32 := SIN(rAngle_A_rad);   rRotMat_A33 := COS(rAngle_A_rad);

(* Rotation Matrix R_C around Z-Axis *)
rRotMat_C11 := COS(rAngle_C_rad);   rRotMat_C12 := -SIN(rAngle_C_rad);  rRotMat_C13 := 0.0;
rRotMat_C21 := SIN(rAngle_C_rad);   rRotMat_C22 := COS(rAngle_C_rad);   rRotMat_C23 := 0.0;
rRotMat_C31 := 0.0;                 rRotMat_C32 := 0.0;                 rRotMat_C33 := 1.0;

(* Matrix Multiplication: R_total = R_C * R_A * [0, 0, -rToolLength_mm]^T *)
rToolVector_X_mm := -(rRotMat_C12 * rRotMat_A23 + rRotMat_C13 * rRotMat_A33) * rToolLength_mm;
rToolVector_Y_mm := -(rRotMat_C22 * rRotMat_A23 + rRotMat_C23 * rRotMat_A33) * rToolLength_mm;
rToolVector_Z_mm := -(rRotMat_C32 * rRotMat_A23 + rRotMat_C33 * rRotMat_A33) * rToolLength_mm;

(* Additive Dynamic Z-Axis Thermal Offset Compensation *)
IF bThermalCompEnable THEN
    rThermalCompOffset_Z_um := rThermalGrowth_Z_um;
ELSE
    rThermalCompOffset_Z_um := 0.0;
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* 2.5: Full 10-State Discrete State Propagation & Luenberger Observer Correction                       *)
(* ---------------------------------------------------------------------------------------------------- *)
(* Assemble Measured Observation Vector y_meas [1..10] *)
y_meas[1] := (rCmdPos_X_mm - rVotedPos_X_mm) * 1000.0; (* TCP X Position Error [um] *)
y_meas[2] := (rCmdPos_Y_mm - rVotedPos_Y_mm) * 1000.0; (* TCP Y Position Error [um] *)
y_meas[3] := (rCmdPos_Z_mm - rVotedPos_Z_mm) * 1000.0; (* TCP Z Position Error [um] *)
y_meas[4] := rVotedSpindleAccel_X_ms2 * T_CYCLE_SEC * 1000.0; (* Integrated Modal Velocity X [mm/s] *)
y_meas[5] := rVotedSpindleAccel_Y_ms2 * T_CYCLE_SEC * 1000.0; (* Integrated Modal Velocity Y [mm/s] *)
y_meas[6] := rVotedSpindleAccel_Z_ms2 * T_CYCLE_SEC * 1000.0; (* Integrated Modal Velocity Z [mm/s] *)
y_meas[7] := rThermalGrowth_Z_um;                      (* Spindle Axial Thermal Growth [um] *)
y_meas[8] := rBearingPreloadDelta_N;                   (* Bearing Preload Dynamic Delta [N] *)
y_meas[9] := rCuttingForce_Magnitude_N;                (* Cutting Force Vector Magnitude [N] *)
y_meas[10]:= x_state[10];                              (* Proof-mass internal displacement *)

(* State Propagation: x_next = A * x_state + B * u_ctrl *)
FOR idx_i := 1 TO 10 DO
    rTempSum := 0.0;
    FOR idx_j := 1 TO 10 DO
        rTempSum := rTempSum + (a_mat[idx_i, idx_j] * x_state[idx_j]);
    END_FOR;
    FOR idx_k := 1 TO 6 DO
        rTempSum := rTempSum + (b_mat[idx_i, idx_k] * u_ctrl[idx_k]);
    END_FOR;
    x_next[idx_i] := rTempSum;
END_FOR;

(* Innovation Vector: e_innov = y_meas - C * x_state *)
FOR idx_i := 1 TO 10 DO
    rTempSum := 0.0;
    FOR idx_j := 1 TO 10 DO
        rTempSum := rTempSum + (c_mat[idx_i, idx_j] * x_state[idx_j]);
    END_FOR;
    y_pred[idx_i] := rTempSum;
    (* Luenberger State Correction *)
    x_state[idx_i] := x_next[idx_i] + (k_obs[idx_i] * (y_meas[idx_i] - y_pred[idx_i]));
END_FOR;
"""
