(* ==================================================================================================== *)
(* PHASE 2: DISCRETE 6TH-ORDER STATE-SPACE OBSERVER, KALMAN FILTERING & SELLARS-TEGART CONSTITUTIVE KINETICS *)
(* ==================================================================================================== *)
(* MATHEMATICAL STATE-SPACE FORMULATION:                                                                *)
(* Continuous-time physical model: dx/dt = A_c * x(t) + B_c * u(t) + w(t)                               *)
(* Discrete-time observer (Dt = 1.0 ms):                                                                *)
(*   x_{k+1|k} = A * x_{k|k} + B * u_k                                                                  *)
(*   y_innov_k = y_meas_k - (C * x_{k+1|k} + D * u_k)                                                   *)
(*   x_{k+1|k+1} = x_{k+1|k} + L * y_innov_k                                                            *)
(*   P_{k+1|k} = A * P_{k|k} * A^T + Q_obs                                                             *)
(*   P_{k+1|k+1} = (I - L * C) * P_{k+1|k}                                                             *)
(*                                                                                                      *)
(* STATE DEFINITIONS:                                                                                   *)
(*   x1: Ram Vertical Position / Instantaneous Billet Height h(t) [mm]                                  *)
(*   x2: Ram Downward Forging Velocity v(t) = dh/dt [mm/s]                                              *)
(*   x3: Effective True Workpiece Flow Stress Sigma_f [MPa]                                             *)
(*   x4: Dynamically Recrystallized Prior Beta / Equiaxed Alpha Grain Size d_gs [um]                    *)
(*   x5: Die-Workpiece Contact Interface Temperature T_die [deg C]                                      *)
(*   x6: Ram Dynamic Leveling Angular Skew Deflection Theta_skew [um]                                   *)
(*                                                                                                      *)
(* CONTROL INPUTS:                                                                                      *)
(*   u1: Variable Displacement Servo Pump Swashplate Command [%] (0 to 100%)                             *)
(*   u2: Dynamic Servo Leveling Differential Spool Flow [L/min] (-120 to +120 L/min)                    *)
(*   u3: Multi-Zone Induction Power Generator Master Output [kW] (0 to 1500 kW)                         *)
(*   u4: High-Vacuum Bleed / Chamber Argon Backpressure Valve [mbar] (0.001 to 1.0 mbar)                *)
(*   u5: Dynamic Proportional Counterbalance Backpressure Valve [%] (0 to 100%)                         *)
(*                                                                                                      *)
(* MEASURED OUTPUTS (from Phase 1 2oo3 TMR Engine):                                                     *)
(*   y1: Total Ram Axial Forging Tonnage [kN]                                                           *)
(*   y2: Cylinder Manifold High-Pressure Hydraulic Header [bar]                                         *)
(*   y3: Upper Die Induction Core Surface Temperature [deg C]                                           *)
(*   y4: 4-Corner Ram Dynamic Leveling Tilt Skew Deviation [um]                                         *)
(* ==================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------- *)
(* 2.1 ASSIGN MEASURED PROCESS VECTORS FROM 2oo3 VOTED SIGNALS                                          *)
(* ---------------------------------------------------------------------------------------------------- *)
y_meas[1] := r_TMR_VotedTonnage_kN;
y_meas[2] := r_TMR_VotedHydPressure_bar;
y_meas[3] := r_TMR_VotedDieTemp_DegC;
y_meas[4] := r_TMR_VotedTiltSkew_um;

(* ---------------------------------------------------------------------------------------------------- *)
(* 2.2 DISCRETE STATE ESTIMATION PREDICTION STEP: x_pred = A * x_est + B * u_cmd                        *)
(* Explicit 6x6 Matrix-Vector Multiplication:                                                          *)
(* ---------------------------------------------------------------------------------------------------- *)
x_pred[1] := ((A_mat[1, 1] * x_est[1]) + (A_mat[1, 2] * x_est[2]) + (A_mat[1, 3] * x_est[3]) + (A_mat[1, 4] * x_est[4]) + (A_mat[1, 5] * x_est[5]) + (A_mat[1, 6] * x_est[6])) + ((B_mat[1, 1] * u_cmd[1]) + (B_mat[1, 2] * u_cmd[2]) + (B_mat[1, 3] * u_cmd[3]) + (B_mat[1, 4] * u_cmd[4]) + (B_mat[1, 5] * u_cmd[5]));
x_pred[2] := ((A_mat[2, 1] * x_est[1]) + (A_mat[2, 2] * x_est[2]) + (A_mat[2, 3] * x_est[3]) + (A_mat[2, 4] * x_est[4]) + (A_mat[2, 5] * x_est[5]) + (A_mat[2, 6] * x_est[6])) + ((B_mat[2, 1] * u_cmd[1]) + (B_mat[2, 2] * u_cmd[2]) + (B_mat[2, 3] * u_cmd[3]) + (B_mat[2, 4] * u_cmd[4]) + (B_mat[2, 5] * u_cmd[5]));
x_pred[3] := ((A_mat[3, 1] * x_est[1]) + (A_mat[3, 2] * x_est[2]) + (A_mat[3, 3] * x_est[3]) + (A_mat[3, 4] * x_est[4]) + (A_mat[3, 5] * x_est[5]) + (A_mat[3, 6] * x_est[6])) + ((B_mat[3, 1] * u_cmd[1]) + (B_mat[3, 2] * u_cmd[2]) + (B_mat[3, 3] * u_cmd[3]) + (B_mat[3, 4] * u_cmd[4]) + (B_mat[3, 5] * u_cmd[5]));
x_pred[4] := ((A_mat[4, 1] * x_est[1]) + (A_mat[4, 2] * x_est[2]) + (A_mat[4, 3] * x_est[3]) + (A_mat[4, 4] * x_est[4]) + (A_mat[4, 5] * x_est[5]) + (A_mat[4, 6] * x_est[6])) + ((B_mat[4, 1] * u_cmd[1]) + (B_mat[4, 2] * u_cmd[2]) + (B_mat[4, 3] * u_cmd[3]) + (B_mat[4, 4] * u_cmd[4]) + (B_mat[4, 5] * u_cmd[5]));
x_pred[5] := ((A_mat[5, 1] * x_est[1]) + (A_mat[5, 2] * x_est[2]) + (A_mat[5, 3] * x_est[3]) + (A_mat[5, 4] * x_est[4]) + (A_mat[5, 5] * x_est[5]) + (A_mat[5, 6] * x_est[6])) + ((B_mat[5, 1] * u_cmd[1]) + (B_mat[5, 2] * u_cmd[2]) + (B_mat[5, 3] * u_cmd[3]) + (B_mat[5, 4] * u_cmd[4]) + (B_mat[5, 5] * u_cmd[5]));
x_pred[6] := ((A_mat[6, 1] * x_est[1]) + (A_mat[6, 2] * x_est[2]) + (A_mat[6, 3] * x_est[3]) + (A_mat[6, 4] * x_est[4]) + (A_mat[6, 5] * x_est[5]) + (A_mat[6, 6] * x_est[6])) + ((B_mat[6, 1] * u_cmd[1]) + (B_mat[6, 2] * u_cmd[2]) + (B_mat[6, 3] * u_cmd[3]) + (B_mat[6, 4] * u_cmd[4]) + (B_mat[6, 5] * u_cmd[5]));

(* ---------------------------------------------------------------------------------------------------- *)
(* 2.3 OBSERVER OUTPUT PREDICTION & INNOVATION RESIDUAL: y_innov = y_meas - (C * x_pred + D * u_cmd)   *)
(* Explicit 4x6 Measurement Matrix Product:                                                             *)
(* ---------------------------------------------------------------------------------------------------- *)
y_est[1] := ((C_mat[1, 1] * x_pred[1]) + (C_mat[1, 2] * x_pred[2]) + (C_mat[1, 3] * x_pred[3]) + (C_mat[1, 4] * x_pred[4]) + (C_mat[1, 5] * x_pred[5]) + (C_mat[1, 6] * x_pred[6])) + ((D_mat[1, 1] * u_cmd[1]) + (D_mat[1, 2] * u_cmd[2]) + (D_mat[1, 3] * u_cmd[3]) + (D_mat[1, 4] * u_cmd[4]) + (D_mat[1, 5] * u_cmd[5]));
y_innov[1] := y_meas[1] - y_est[1];
y_est[2] := ((C_mat[2, 1] * x_pred[1]) + (C_mat[2, 2] * x_pred[2]) + (C_mat[2, 3] * x_pred[3]) + (C_mat[2, 4] * x_pred[4]) + (C_mat[2, 5] * x_pred[5]) + (C_mat[2, 6] * x_pred[6])) + ((D_mat[2, 1] * u_cmd[1]) + (D_mat[2, 2] * u_cmd[2]) + (D_mat[2, 3] * u_cmd[3]) + (D_mat[2, 4] * u_cmd[4]) + (D_mat[2, 5] * u_cmd[5]));
y_innov[2] := y_meas[2] - y_est[2];
y_est[3] := ((C_mat[3, 1] * x_pred[1]) + (C_mat[3, 2] * x_pred[2]) + (C_mat[3, 3] * x_pred[3]) + (C_mat[3, 4] * x_pred[4]) + (C_mat[3, 5] * x_pred[5]) + (C_mat[3, 6] * x_pred[6])) + ((D_mat[3, 1] * u_cmd[1]) + (D_mat[3, 2] * u_cmd[2]) + (D_mat[3, 3] * u_cmd[3]) + (D_mat[3, 4] * u_cmd[4]) + (D_mat[3, 5] * u_cmd[5]));
y_innov[3] := y_meas[3] - y_est[3];
y_est[4] := ((C_mat[4, 1] * x_pred[1]) + (C_mat[4, 2] * x_pred[2]) + (C_mat[4, 3] * x_pred[3]) + (C_mat[4, 4] * x_pred[4]) + (C_mat[4, 5] * x_pred[5]) + (C_mat[4, 6] * x_pred[6])) + ((D_mat[4, 1] * u_cmd[1]) + (D_mat[4, 2] * u_cmd[2]) + (D_mat[4, 3] * u_cmd[3]) + (D_mat[4, 4] * u_cmd[4]) + (D_mat[4, 5] * u_cmd[5]));
y_innov[4] := y_meas[4] - y_est[4];

(* ---------------------------------------------------------------------------------------------------- *)
(* 2.4 KALMAN STATE ESTIMATE INNOVATION UPDATE: x_est = x_pred + L * y_innov                            *)
(* Explicit 6x4 Kalman Innovation Matrix Product:                                                       *)
(* ---------------------------------------------------------------------------------------------------- *)
x_est[1] := x_pred[1] + ((L_mat[1, 1] * y_innov[1]) + (L_mat[1, 2] * y_innov[2]) + (L_mat[1, 3] * y_innov[3]) + (L_mat[1, 4] * y_innov[4]));
x_est[2] := x_pred[2] + ((L_mat[2, 1] * y_innov[1]) + (L_mat[2, 2] * y_innov[2]) + (L_mat[2, 3] * y_innov[3]) + (L_mat[2, 4] * y_innov[4]));
x_est[3] := x_pred[3] + ((L_mat[3, 1] * y_innov[1]) + (L_mat[3, 2] * y_innov[2]) + (L_mat[3, 3] * y_innov[3]) + (L_mat[3, 4] * y_innov[4]));
x_est[4] := x_pred[4] + ((L_mat[4, 1] * y_innov[1]) + (L_mat[4, 2] * y_innov[2]) + (L_mat[4, 3] * y_innov[3]) + (L_mat[4, 4] * y_innov[4]));
x_est[5] := x_pred[5] + ((L_mat[5, 1] * y_innov[1]) + (L_mat[5, 2] * y_innov[2]) + (L_mat[5, 3] * y_innov[3]) + (L_mat[5, 4] * y_innov[4]));
x_est[6] := x_pred[6] + ((L_mat[6, 1] * y_innov[1]) + (L_mat[6, 2] * y_innov[2]) + (L_mat[6, 3] * y_innov[3]) + (L_mat[6, 4] * y_innov[4]));

(* Physical State Value Anti-Windup Clamping *)
IF x_est[1] < 10.0 THEN
    x_est[1] := 10.0; (* Hard physical lower die stop [mm] *)
ELSIF x_est[1] > 600.0 THEN
    x_est[1] := 600.0; (* Top dead center limit [mm] *)
END_IF;
IF x_est[3] < 0.0 THEN
    x_est[3] := 0.0; (* Flow stress cannot be negative [MPa] *)
END_IF;
IF x_est[4] < 2.0 THEN
    x_est[4] := 2.0; (* Minimum grain size threshold [um] *)
END_IF;
IF x_est[5] < 20.0 THEN
    x_est[5] := 20.0; (* Ambient thermal lower limit [deg C] *)
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* 2.5 FIRST-PRINCIPLES SELLARS-TEGART HYPERBOLIC SINE CONSTITUTIVE FLOW STRESS MODEL                   *)
(* ---------------------------------------------------------------------------------------------------- *)
(* WORKPIECE METALLURGY: Titanium Alloy Ti-6Al-4V (ELI Aerospace Grade AMS 4928)                        *)
(* True Axial Logarithmic Deformation Strain: Epsilon(t) = -ln(h(t) / h0)                               *)
(* True Axial Deformation Strain Rate: dEpsilon/dt = -v(t) / h(t) [s^-1]                                *)
(* ---------------------------------------------------------------------------------------------------- *)
IF (x_est[1] > 0.0) AND (r_InitialBilletHeight_mm > 0.0) THEN
    IF x_est[1] < r_InitialBilletHeight_mm THEN
        r_InstantaneousTrueStrain := -1.0 * LN(x_est[1] / r_InitialBilletHeight_mm);
    ELSE
        r_InstantaneousTrueStrain := 0.0;
    END_IF;
    r_InstantaneousStrainRate_s_inv := ABS(x_est[2]) / x_est[1];
ELSE
    r_InstantaneousTrueStrain := 0.0;
    r_InstantaneousStrainRate_s_inv := 0.0;
END_IF;

(* Prevent Numerical Underflow in Arrhenius Activation Energy Exponential *)
IF x_est[5] > 700.0 THEN
    (* Convert Die Temperature to Kelvin: T_kelvin = T_degC + 273.15 *)
    r_TmpZ := C_Q_ACTIVATION_ENERGY_J_MOL / (C_R_GAS_CONST_J_MOL_K * (x_est[5] + 273.15));
    IF r_TmpZ > 80.0 THEN
        r_TmpZ := 80.0;
    END_IF;
    r_TmpExp := EXP(r_TmpZ);
    (* Zener-Hollomon Temperature-Compensated Strain Rate Parameter: Z = (dEps/dt) * exp(Q/(R*T)) *)
    r_ZenerHollomonParameter_Z := r_InstantaneousStrainRate_s_inv * r_TmpExp;
    IF r_ZenerHollomonParameter_Z < 1.0e5 THEN
        r_ZenerHollomonParameter_Z := 1.0e5; (* Minimum numerical lower bound *)
    ELSIF r_ZenerHollomonParameter_Z > 1.0e16 THEN
        r_ZenerHollomonParameter_Z := 1.0e16; (* Physical upper saturation bound *)
    END_IF;
    
    (* Compute Sellars-Tegart Flow Stress Sigma:                                                        *)
    (* Sigma = (1.0 / alpha_st) * asinh( (Z / A_st)^(1.0 / n_st) )                                      *)
    (* In IEC 61131-3: asinh(y) = ln(y + sqrt(y*y + 1.0))                                              *)
    r_TmpArg := (r_ZenerHollomonParameter_Z / C_ST_PRE_EXP_A_S_INV);
    IF r_TmpArg > 0.0 THEN
        r_TmpArg := EXP( (1.0 / C_ST_EXPONENT_N) * LN(r_TmpArg) );
    ELSE
        r_TmpArg := 0.0;
    END_IF;
    r_TmpSqrt := SQRT((r_TmpArg * r_TmpArg) + 1.0);
    r_TmpASinh := LN(r_TmpArg + r_TmpSqrt);
    r_Obs_FlowStress_MPa := (1.0 / C_ST_ALPHA_INV_MPA) * r_TmpASinh;
ELSE
    r_ZenerHollomonParameter_Z := 0.0;
    r_Obs_FlowStress_MPa := 0.0;
END_IF;

(* Dynamic Recrystallization (DRX) Avrami Kinetics & Grain Size Refinement *)
IF r_InstantaneousTrueStrain > 0.05 THEN
    (* Critical Strain for DRX Initiation: Epsilon_c = 0.0012 * Z^(0.125) *)
    r_TmpZ := 0.0012 * EXP(0.125 * LN(r_ZenerHollomonParameter_Z));
    (* Strain for 50% DRX: Epsilon_0.5 = 0.0035 * Z^(0.110) *)
    r_TmpArg := 0.0035 * EXP(0.110 * LN(r_ZenerHollomonParameter_Z));
    IF (r_InstantaneousTrueStrain > r_TmpZ) AND (r_TmpArg > 0.0) THEN
        r_TmpDeltaU := (r_InstantaneousTrueStrain - r_TmpZ) / r_TmpArg;
        IF r_TmpDeltaU > 0.0 THEN
            r_TmpExp := -1.0 * C_DRX_BETA * EXP(C_DRX_EXPONENT_M * LN(r_TmpDeltaU));
            IF r_TmpExp < -25.0 THEN
                r_TmpExp := -25.0;
            END_IF;
            r_DRX_RecrystallizedFraction := 1.0 - EXP(r_TmpExp);
        ELSE
            r_DRX_RecrystallizedFraction := 0.0;
        END_IF;
    ELSE
        r_DRX_RecrystallizedFraction := 0.0;
    END_IF;
    (* Steady-State Dynamically Recrystallized Grain Size: d_ss = 350.0 * Z^(-0.18) [um] *)
    r_TmpZ := 350.0 * EXP(-0.180 * LN(r_ZenerHollomonParameter_Z));
    IF r_TmpZ < 3.5 THEN
        r_TmpZ := 3.5;
    END_IF;
    (* Dynamic Composite Grain Size Evolution: d = d0 * (1 - X_drx) + d_ss * X_drx *)
    r_Obs_DRX_GrainSize_um := (C_INITIAL_GRAIN_SIZE_UM * (1.0 - r_DRX_RecrystallizedFraction)) + (r_TmpZ * r_DRX_RecrystallizedFraction);
ELSE
    r_DRX_RecrystallizedFraction := 0.0;
    r_Obs_DRX_GrainSize_um := C_INITIAL_GRAIN_SIZE_UM;
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* 2.6 KALMAN COVARIANCE PROPAGATION MATRIX EQUATIONS: P_pred = A * P * A^T + Q_obs                     *)
(* Unrolled Explicit 6x6 Matrix Product for Guaranteed Parity & Determinism:                           *)
(* ---------------------------------------------------------------------------------------------------- *)
(* Element P_pred[1, 1] *)
r_TmpSum := 0.0;
r_TmpSum := r_TmpSum + (A_mat[1, 1] * (
    (P_cov[1, 1] * A_mat[1, 1]) + (P_cov[1, 2] * A_mat[1, 2]) + (P_cov[1, 3] * A_mat[1, 3]) + (P_cov[1, 4] * A_mat[1, 4]) + (P_cov[1, 5] * A_mat[1, 5]) + (P_cov[1, 6] * A_mat[1, 6])
));
r_TmpSum := r_TmpSum + (A_mat[1, 2] * (
    (P_cov[2, 1] * A_mat[1, 1]) + (P_cov[2, 2] * A_mat[1, 2]) + (P_cov[2, 3] * A_mat[1, 3]) + (P_cov[2, 4] * A_mat[1, 4]) + (P_cov[2, 5] * A_mat[1, 5]) + (P_cov[2, 6] * A_mat[1, 6])
));
r_TmpSum := r_TmpSum + (A_mat[1, 3] * (
    (P_cov[3, 1] * A_mat[1, 1]) + (P_cov[3, 2] * A_mat[1, 2]) + (P_cov[3, 3] * A_mat[1, 3]) + (P_cov[3, 4] * A_mat[1, 4]) + (P_cov[3, 5] * A_mat[1, 5]) + (P_cov[3, 6] * A_mat[1, 6])
));
r_TmpSum := r_TmpSum + (A_mat[1, 4] * (
    (P_cov[4, 1] * A_mat[1, 1]) + (P_cov[4, 2] * A_mat[1, 2]) + (P_cov[4, 3] * A_mat[1, 3]) + (P_cov[4, 4] * A_mat[1, 4]) + (P_cov[4, 5] * A_mat[1, 5]) + (P_cov[4, 6] * A_mat[1, 6])
));
r_TmpSum := r_TmpSum + (A_mat[1, 5] * (
    (P_cov[5, 1] * A_mat[1, 1]) + (P_cov[5, 2] * A_mat[1, 2]) + (P_cov[5, 3] * A_mat[1, 3]) + (P_cov[5, 4] * A_mat[1, 4]) + (P_cov[5, 5] * A_mat[1, 5]) + (P_cov[5, 6] * A_mat[1, 6])
));
r_TmpSum := r_TmpSum + (A_mat[1, 6] * (
    (P_cov[6, 1] * A_mat[1, 1]) + (P_cov[6, 2] * A_mat[1, 2]) + (P_cov[6, 3] * A_mat[1, 3]) + (P_cov[6, 4] * A_mat[1, 4]) + (P_cov[6, 5] * A_mat[1, 5]) + (P_cov[6, 6] * A_mat[1, 6])
));
P_cov[1, 1] := r_TmpSum + Q_obs_diag[1];
(* Element P_pred[1, 2] *)
r_TmpSum := 0.0;
r_TmpSum := r_TmpSum + (A_mat[1, 1] * (
    (P_cov[1, 1] * A_mat[2, 1]) + (P_cov[1, 2] * A_mat[2, 2]) + (P_cov[1, 3] * A_mat[2, 3]) + (P_cov[1, 4] * A_mat[2, 4]) + (P_cov[1, 5] * A_mat[2, 5]) + (P_cov[1, 6] * A_mat[2, 6])
));
r_TmpSum := r_TmpSum + (A_mat[1, 2] * (
    (P_cov[2, 1] * A_mat[2, 1]) + (P_cov[2, 2] * A_mat[2, 2]) + (P_cov[2, 3] * A_mat[2, 3]) + (P_cov[2, 4] * A_mat[2, 4]) + (P_cov[2, 5] * A_mat[2, 5]) + (P_cov[2, 6] * A_mat[2, 6])
));
r_TmpSum := r_TmpSum + (A_mat[1, 3] * (
    (P_cov[3, 1] * A_mat[2, 1]) + (P_cov[3, 2] * A_mat[2, 2]) + (P_cov[3, 3] * A_mat[2, 3]) + (P_cov[3, 4] * A_mat[2, 4]) + (P_cov[3, 5] * A_mat[2, 5]) + (P_cov[3, 6] * A_mat[2, 6])
));
r_TmpSum := r_TmpSum + (A_mat[1, 4] * (
    (P_cov[4, 1] * A_mat[2, 1]) + (P_cov[4, 2] * A_mat[2, 2]) + (P_cov[4, 3] * A_mat[2, 3]) + (P_cov[4, 4] * A_mat[2, 4]) + (P_cov[4, 5] * A_mat[2, 5]) + (P_cov[4, 6] * A_mat[2, 6])
));
r_TmpSum := r_TmpSum + (A_mat[1, 5] * (
    (P_cov[5, 1] * A_mat[2, 1]) + (P_cov[5, 2] * A_mat[2, 2]) + (P_cov[5, 3] * A_mat[2, 3]) + (P_cov[5, 4] * A_mat[2, 4]) + (P_cov[5, 5] * A_mat[2, 5]) + (P_cov[5, 6] * A_mat[2, 6])
));
r_TmpSum := r_TmpSum + (A_mat[1, 6] * (
    (P_cov[6, 1] * A_mat[2, 1]) + (P_cov[6, 2] * A_mat[2, 2]) + (P_cov[6, 3] * A_mat[2, 3]) + (P_cov[6, 4] * A_mat[2, 4]) + (P_cov[6, 5] * A_mat[2, 5]) + (P_cov[6, 6] * A_mat[2, 6])
));
P_cov[1, 2] := r_TmpSum;
(* Element P_pred[1, 3] *)
r_TmpSum := 0.0;
r_TmpSum := r_TmpSum + (A_mat[1, 1] * (
    (P_cov[1, 1] * A_mat[3, 1]) + (P_cov[1, 2] * A_mat[3, 2]) + (P_cov[1, 3] * A_mat[3, 3]) + (P_cov[1, 4] * A_mat[3, 4]) + (P_cov[1, 5] * A_mat[3, 5]) + (P_cov[1, 6] * A_mat[3, 6])
));
r_TmpSum := r_TmpSum + (A_mat[1, 2] * (
    (P_cov[2, 1] * A_mat[3, 1]) + (P_cov[2, 2] * A_mat[3, 2]) + (P_cov[2, 3] * A_mat[3, 3]) + (P_cov[2, 4] * A_mat[3, 4]) + (P_cov[2, 5] * A_mat[3, 5]) + (P_cov[2, 6] * A_mat[3, 6])
));
r_TmpSum := r_TmpSum + (A_mat[1, 3] * (
    (P_cov[3, 1] * A_mat[3, 1]) + (P_cov[3, 2] * A_mat[3, 2]) + (P_cov[3, 3] * A_mat[3, 3]) + (P_cov[3, 4] * A_mat[3, 4]) + (P_cov[3, 5] * A_mat[3, 5]) + (P_cov[3, 6] * A_mat[3, 6])
));
r_TmpSum := r_TmpSum + (A_mat[1, 4] * (
    (P_cov[4, 1] * A_mat[3, 1]) + (P_cov[4, 2] * A_mat[3, 2]) + (P_cov[4, 3] * A_mat[3, 3]) + (P_cov[4, 4] * A_mat[3, 4]) + (P_cov[4, 5] * A_mat[3, 5]) + (P_cov[4, 6] * A_mat[3, 6])
));
r_TmpSum := r_TmpSum + (A_mat[1, 5] * (
    (P_cov[5, 1] * A_mat[3, 1]) + (P_cov[5, 2] * A_mat[3, 2]) + (P_cov[5, 3] * A_mat[3, 3]) + (P_cov[5, 4] * A_mat[3, 4]) + (P_cov[5, 5] * A_mat[3, 5]) + (P_cov[5, 6] * A_mat[3, 6])
));
r_TmpSum := r_TmpSum + (A_mat[1, 6] * (
    (P_cov[6, 1] * A_mat[3, 1]) + (P_cov[6, 2] * A_mat[3, 2]) + (P_cov[6, 3] * A_mat[3, 3]) + (P_cov[6, 4] * A_mat[3, 4]) + (P_cov[6, 5] * A_mat[3, 5]) + (P_cov[6, 6] * A_mat[3, 6])
));
P_cov[1, 3] := r_TmpSum;
(* Element P_pred[1, 4] *)
r_TmpSum := 0.0;
r_TmpSum := r_TmpSum + (A_mat[1, 1] * (
    (P_cov[1, 1] * A_mat[4, 1]) + (P_cov[1, 2] * A_mat[4, 2]) + (P_cov[1, 3] * A_mat[4, 3]) + (P_cov[1, 4] * A_mat[4, 4]) + (P_cov[1, 5] * A_mat[4, 5]) + (P_cov[1, 6] * A_mat[4, 6])
));
r_TmpSum := r_TmpSum + (A_mat[1, 2] * (
    (P_cov[2, 1] * A_mat[4, 1]) + (P_cov[2, 2] * A_mat[4, 2]) + (P_cov[2, 3] * A_mat[4, 3]) + (P_cov[2, 4] * A_mat[4, 4]) + (P_cov[2, 5] * A_mat[4, 5]) + (P_cov[2, 6] * A_mat[4, 6])
));
r_TmpSum := r_TmpSum + (A_mat[1, 3] * (
    (P_cov[3, 1] * A_mat[4, 1]) + (P_cov[3, 2] * A_mat[4, 2]) + (P_cov[3, 3] * A_mat[4, 3]) + (P_cov[3, 4] * A_mat[4, 4]) + (P_cov[3, 5] * A_mat[4, 5]) + (P_cov[3, 6] * A_mat[4, 6])
));
r_TmpSum := r_TmpSum + (A_mat[1, 4] * (
    (P_cov[4, 1] * A_mat[4, 1]) + (P_cov[4, 2] * A_mat[4, 2]) + (P_cov[4, 3] * A_mat[4, 3]) + (P_cov[4, 4] * A_mat[4, 4]) + (P_cov[4, 5] * A_mat[4, 5]) + (P_cov[4, 6] * A_mat[4, 6])
));
r_TmpSum := r_TmpSum + (A_mat[1, 5] * (
    (P_cov[5, 1] * A_mat[4, 1]) + (P_cov[5, 2] * A_mat[4, 2]) + (P_cov[5, 3] * A_mat[4, 3]) + (P_cov[5, 4] * A_mat[4, 4]) + (P_cov[5, 5] * A_mat[4, 5]) + (P_cov[5, 6] * A_mat[4, 6])
));
r_TmpSum := r_TmpSum + (A_mat[1, 6] * (
    (P_cov[6, 1] * A_mat[4, 1]) + (P_cov[6, 2] * A_mat[4, 2]) + (P_cov[6, 3] * A_mat[4, 3]) + (P_cov[6, 4] * A_mat[4, 4]) + (P_cov[6, 5] * A_mat[4, 5]) + (P_cov[6, 6] * A_mat[4, 6])
));
P_cov[1, 4] := r_TmpSum;
(* Element P_pred[1, 5] *)
r_TmpSum := 0.0;
r_TmpSum := r_TmpSum + (A_mat[1, 1] * (
    (P_cov[1, 1] * A_mat[5, 1]) + (P_cov[1, 2] * A_mat[5, 2]) + (P_cov[1, 3] * A_mat[5, 3]) + (P_cov[1, 4] * A_mat[5, 4]) + (P_cov[1, 5] * A_mat[5, 5]) + (P_cov[1, 6] * A_mat[5, 6])
));
r_TmpSum := r_TmpSum + (A_mat[1, 2] * (
    (P_cov[2, 1] * A_mat[5, 1]) + (P_cov[2, 2] * A_mat[5, 2]) + (P_cov[2, 3] * A_mat[5, 3]) + (P_cov[2, 4] * A_mat[5, 4]) + (P_cov[2, 5] * A_mat[5, 5]) + (P_cov[2, 6] * A_mat[5, 6])
));
r_TmpSum := r_TmpSum + (A_mat[1, 3] * (
    (P_cov[3, 1] * A_mat[5, 1]) + (P_cov[3, 2] * A_mat[5, 2]) + (P_cov[3, 3] * A_mat[5, 3]) + (P_cov[3, 4] * A_mat[5, 4]) + (P_cov[3, 5] * A_mat[5, 5]) + (P_cov[3, 6] * A_mat[5, 6])
));
r_TmpSum := r_TmpSum + (A_mat[1, 4] * (
    (P_cov[4, 1] * A_mat[5, 1]) + (P_cov[4, 2] * A_mat[5, 2]) + (P_cov[4, 3] * A_mat[5, 3]) + (P_cov[4, 4] * A_mat[5, 4]) + (P_cov[4, 5] * A_mat[5, 5]) + (P_cov[4, 6] * A_mat[5, 6])
));
r_TmpSum := r_TmpSum + (A_mat[1, 5] * (
    (P_cov[5, 1] * A_mat[5, 1]) + (P_cov[5, 2] * A_mat[5, 2]) + (P_cov[5, 3] * A_mat[5, 3]) + (P_cov[5, 4] * A_mat[5, 4]) + (P_cov[5, 5] * A_mat[5, 5]) + (P_cov[5, 6] * A_mat[5, 6])
));
r_TmpSum := r_TmpSum + (A_mat[1, 6] * (
    (P_cov[6, 1] * A_mat[5, 1]) + (P_cov[6, 2] * A_mat[5, 2]) + (P_cov[6, 3] * A_mat[5, 3]) + (P_cov[6, 4] * A_mat[5, 4]) + (P_cov[6, 5] * A_mat[5, 5]) + (P_cov[6, 6] * A_mat[5, 6])
));
P_cov[1, 5] := r_TmpSum;
(* Element P_pred[1, 6] *)
r_TmpSum := 0.0;
r_TmpSum := r_TmpSum + (A_mat[1, 1] * (
    (P_cov[1, 1] * A_mat[6, 1]) + (P_cov[1, 2] * A_mat[6, 2]) + (P_cov[1, 3] * A_mat[6, 3]) + (P_cov[1, 4] * A_mat[6, 4]) + (P_cov[1, 5] * A_mat[6, 5]) + (P_cov[1, 6] * A_mat[6, 6])
));
r_TmpSum := r_TmpSum + (A_mat[1, 2] * (
    (P_cov[2, 1] * A_mat[6, 1]) + (P_cov[2, 2] * A_mat[6, 2]) + (P_cov[2, 3] * A_mat[6, 3]) + (P_cov[2, 4] * A_mat[6, 4]) + (P_cov[2, 5] * A_mat[6, 5]) + (P_cov[2, 6] * A_mat[6, 6])
));
r_TmpSum := r_TmpSum + (A_mat[1, 3] * (
    (P_cov[3, 1] * A_mat[6, 1]) + (P_cov[3, 2] * A_mat[6, 2]) + (P_cov[3, 3] * A_mat[6, 3]) + (P_cov[3, 4] * A_mat[6, 4]) + (P_cov[3, 5] * A_mat[6, 5]) + (P_cov[3, 6] * A_mat[6, 6])
));
r_TmpSum := r_TmpSum + (A_mat[1, 4] * (
    (P_cov[4, 1] * A_mat[6, 1]) + (P_cov[4, 2] * A_mat[6, 2]) + (P_cov[4, 3] * A_mat[6, 3]) + (P_cov[4, 4] * A_mat[6, 4]) + (P_cov[4, 5] * A_mat[6, 5]) + (P_cov[4, 6] * A_mat[6, 6])
));
r_TmpSum := r_TmpSum + (A_mat[1, 5] * (
    (P_cov[5, 1] * A_mat[6, 1]) + (P_cov[5, 2] * A_mat[6, 2]) + (P_cov[5, 3] * A_mat[6, 3]) + (P_cov[5, 4] * A_mat[6, 4]) + (P_cov[5, 5] * A_mat[6, 5]) + (P_cov[5, 6] * A_mat[6, 6])
));
r_TmpSum := r_TmpSum + (A_mat[1, 6] * (
    (P_cov[6, 1] * A_mat[6, 1]) + (P_cov[6, 2] * A_mat[6, 2]) + (P_cov[6, 3] * A_mat[6, 3]) + (P_cov[6, 4] * A_mat[6, 4]) + (P_cov[6, 5] * A_mat[6, 5]) + (P_cov[6, 6] * A_mat[6, 6])
));
P_cov[1, 6] := r_TmpSum;
(* Element P_pred[2, 1] *)
r_TmpSum := 0.0;
r_TmpSum := r_TmpSum + (A_mat[2, 1] * (
    (P_cov[1, 1] * A_mat[1, 1]) + (P_cov[1, 2] * A_mat[1, 2]) + (P_cov[1, 3] * A_mat[1, 3]) + (P_cov[1, 4] * A_mat[1, 4]) + (P_cov[1, 5] * A_mat[1, 5]) + (P_cov[1, 6] * A_mat[1, 6])
));
r_TmpSum := r_TmpSum + (A_mat[2, 2] * (
    (P_cov[2, 1] * A_mat[1, 1]) + (P_cov[2, 2] * A_mat[1, 2]) + (P_cov[2, 3] * A_mat[1, 3]) + (P_cov[2, 4] * A_mat[1, 4]) + (P_cov[2, 5] * A_mat[1, 5]) + (P_cov[2, 6] * A_mat[1, 6])
));
r_TmpSum := r_TmpSum + (A_mat[2, 3] * (
    (P_cov[3, 1] * A_mat[1, 1]) + (P_cov[3, 2] * A_mat[1, 2]) + (P_cov[3, 3] * A_mat[1, 3]) + (P_cov[3, 4] * A_mat[1, 4]) + (P_cov[3, 5] * A_mat[1, 5]) + (P_cov[3, 6] * A_mat[1, 6])
));
r_TmpSum := r_TmpSum + (A_mat[2, 4] * (
    (P_cov[4, 1] * A_mat[1, 1]) + (P_cov[4, 2] * A_mat[1, 2]) + (P_cov[4, 3] * A_mat[1, 3]) + (P_cov[4, 4] * A_mat[1, 4]) + (P_cov[4, 5] * A_mat[1, 5]) + (P_cov[4, 6] * A_mat[1, 6])
));
r_TmpSum := r_TmpSum + (A_mat[2, 5] * (
    (P_cov[5, 1] * A_mat[1, 1]) + (P_cov[5, 2] * A_mat[1, 2]) + (P_cov[5, 3] * A_mat[1, 3]) + (P_cov[5, 4] * A_mat[1, 4]) + (P_cov[5, 5] * A_mat[1, 5]) + (P_cov[5, 6] * A_mat[1, 6])
));
r_TmpSum := r_TmpSum + (A_mat[2, 6] * (
    (P_cov[6, 1] * A_mat[1, 1]) + (P_cov[6, 2] * A_mat[1, 2]) + (P_cov[6, 3] * A_mat[1, 3]) + (P_cov[6, 4] * A_mat[1, 4]) + (P_cov[6, 5] * A_mat[1, 5]) + (P_cov[6, 6] * A_mat[1, 6])
));
P_cov[2, 1] := r_TmpSum;
(* Element P_pred[2, 2] *)
r_TmpSum := 0.0;
r_TmpSum := r_TmpSum + (A_mat[2, 1] * (
    (P_cov[1, 1] * A_mat[2, 1]) + (P_cov[1, 2] * A_mat[2, 2]) + (P_cov[1, 3] * A_mat[2, 3]) + (P_cov[1, 4] * A_mat[2, 4]) + (P_cov[1, 5] * A_mat[2, 5]) + (P_cov[1, 6] * A_mat[2, 6])
));
r_TmpSum := r_TmpSum + (A_mat[2, 2] * (
    (P_cov[2, 1] * A_mat[2, 1]) + (P_cov[2, 2] * A_mat[2, 2]) + (P_cov[2, 3] * A_mat[2, 3]) + (P_cov[2, 4] * A_mat[2, 4]) + (P_cov[2, 5] * A_mat[2, 5]) + (P_cov[2, 6] * A_mat[2, 6])
));
r_TmpSum := r_TmpSum + (A_mat[2, 3] * (
    (P_cov[3, 1] * A_mat[2, 1]) + (P_cov[3, 2] * A_mat[2, 2]) + (P_cov[3, 3] * A_mat[2, 3]) + (P_cov[3, 4] * A_mat[2, 4]) + (P_cov[3, 5] * A_mat[2, 5]) + (P_cov[3, 6] * A_mat[2, 6])
));
r_TmpSum := r_TmpSum + (A_mat[2, 4] * (
    (P_cov[4, 1] * A_mat[2, 1]) + (P_cov[4, 2] * A_mat[2, 2]) + (P_cov[4, 3] * A_mat[2, 3]) + (P_cov[4, 4] * A_mat[2, 4]) + (P_cov[4, 5] * A_mat[2, 5]) + (P_cov[4, 6] * A_mat[2, 6])
));
r_TmpSum := r_TmpSum + (A_mat[2, 5] * (
    (P_cov[5, 1] * A_mat[2, 1]) + (P_cov[5, 2] * A_mat[2, 2]) + (P_cov[5, 3] * A_mat[2, 3]) + (P_cov[5, 4] * A_mat[2, 4]) + (P_cov[5, 5] * A_mat[2, 5]) + (P_cov[5, 6] * A_mat[2, 6])
));
r_TmpSum := r_TmpSum + (A_mat[2, 6] * (
    (P_cov[6, 1] * A_mat[2, 1]) + (P_cov[6, 2] * A_mat[2, 2]) + (P_cov[6, 3] * A_mat[2, 3]) + (P_cov[6, 4] * A_mat[2, 4]) + (P_cov[6, 5] * A_mat[2, 5]) + (P_cov[6, 6] * A_mat[2, 6])
));
P_cov[2, 2] := r_TmpSum + Q_obs_diag[2];
(* Element P_pred[2, 3] *)
r_TmpSum := 0.0;
r_TmpSum := r_TmpSum + (A_mat[2, 1] * (
    (P_cov[1, 1] * A_mat[3, 1]) + (P_cov[1, 2] * A_mat[3, 2]) + (P_cov[1, 3] * A_mat[3, 3]) + (P_cov[1, 4] * A_mat[3, 4]) + (P_cov[1, 5] * A_mat[3, 5]) + (P_cov[1, 6] * A_mat[3, 6])
));
r_TmpSum := r_TmpSum + (A_mat[2, 2] * (
    (P_cov[2, 1] * A_mat[3, 1]) + (P_cov[2, 2] * A_mat[3, 2]) + (P_cov[2, 3] * A_mat[3, 3]) + (P_cov[2, 4] * A_mat[3, 4]) + (P_cov[2, 5] * A_mat[3, 5]) + (P_cov[2, 6] * A_mat[3, 6])
));
r_TmpSum := r_TmpSum + (A_mat[2, 3] * (
    (P_cov[3, 1] * A_mat[3, 1]) + (P_cov[3, 2] * A_mat[3, 2]) + (P_cov[3, 3] * A_mat[3, 3]) + (P_cov[3, 4] * A_mat[3, 4]) + (P_cov[3, 5] * A_mat[3, 5]) + (P_cov[3, 6] * A_mat[3, 6])
));
r_TmpSum := r_TmpSum + (A_mat[2, 4] * (
    (P_cov[4, 1] * A_mat[3, 1]) + (P_cov[4, 2] * A_mat[3, 2]) + (P_cov[4, 3] * A_mat[3, 3]) + (P_cov[4, 4] * A_mat[3, 4]) + (P_cov[4, 5] * A_mat[3, 5]) + (P_cov[4, 6] * A_mat[3, 6])
));
r_TmpSum := r_TmpSum + (A_mat[2, 5] * (
    (P_cov[5, 1] * A_mat[3, 1]) + (P_cov[5, 2] * A_mat[3, 2]) + (P_cov[5, 3] * A_mat[3, 3]) + (P_cov[5, 4] * A_mat[3, 4]) + (P_cov[5, 5] * A_mat[3, 5]) + (P_cov[5, 6] * A_mat[3, 6])
));
r_TmpSum := r_TmpSum + (A_mat[2, 6] * (
    (P_cov[6, 1] * A_mat[3, 1]) + (P_cov[6, 2] * A_mat[3, 2]) + (P_cov[6, 3] * A_mat[3, 3]) + (P_cov[6, 4] * A_mat[3, 4]) + (P_cov[6, 5] * A_mat[3, 5]) + (P_cov[6, 6] * A_mat[3, 6])
));
P_cov[2, 3] := r_TmpSum;
(* Element P_pred[2, 4] *)
r_TmpSum := 0.0;
r_TmpSum := r_TmpSum + (A_mat[2, 1] * (
    (P_cov[1, 1] * A_mat[4, 1]) + (P_cov[1, 2] * A_mat[4, 2]) + (P_cov[1, 3] * A_mat[4, 3]) + (P_cov[1, 4] * A_mat[4, 4]) + (P_cov[1, 5] * A_mat[4, 5]) + (P_cov[1, 6] * A_mat[4, 6])
));
r_TmpSum := r_TmpSum + (A_mat[2, 2] * (
    (P_cov[2, 1] * A_mat[4, 1]) + (P_cov[2, 2] * A_mat[4, 2]) + (P_cov[2, 3] * A_mat[4, 3]) + (P_cov[2, 4] * A_mat[4, 4]) + (P_cov[2, 5] * A_mat[4, 5]) + (P_cov[2, 6] * A_mat[4, 6])
));
r_TmpSum := r_TmpSum + (A_mat[2, 3] * (
    (P_cov[3, 1] * A_mat[4, 1]) + (P_cov[3, 2] * A_mat[4, 2]) + (P_cov[3, 3] * A_mat[4, 3]) + (P_cov[3, 4] * A_mat[4, 4]) + (P_cov[3, 5] * A_mat[4, 5]) + (P_cov[3, 6] * A_mat[4, 6])
));
r_TmpSum := r_TmpSum + (A_mat[2, 4] * (
    (P_cov[4, 1] * A_mat[4, 1]) + (P_cov[4, 2] * A_mat[4, 2]) + (P_cov[4, 3] * A_mat[4, 3]) + (P_cov[4, 4] * A_mat[4, 4]) + (P_cov[4, 5] * A_mat[4, 5]) + (P_cov[4, 6] * A_mat[4, 6])
));
r_TmpSum := r_TmpSum + (A_mat[2, 5] * (
    (P_cov[5, 1] * A_mat[4, 1]) + (P_cov[5, 2] * A_mat[4, 2]) + (P_cov[5, 3] * A_mat[4, 3]) + (P_cov[5, 4] * A_mat[4, 4]) + (P_cov[5, 5] * A_mat[4, 5]) + (P_cov[5, 6] * A_mat[4, 6])
));
r_TmpSum := r_TmpSum + (A_mat[2, 6] * (
    (P_cov[6, 1] * A_mat[4, 1]) + (P_cov[6, 2] * A_mat[4, 2]) + (P_cov[6, 3] * A_mat[4, 3]) + (P_cov[6, 4] * A_mat[4, 4]) + (P_cov[6, 5] * A_mat[4, 5]) + (P_cov[6, 6] * A_mat[4, 6])
));
P_cov[2, 4] := r_TmpSum;
(* Element P_pred[2, 5] *)
r_TmpSum := 0.0;
r_TmpSum := r_TmpSum + (A_mat[2, 1] * (
    (P_cov[1, 1] * A_mat[5, 1]) + (P_cov[1, 2] * A_mat[5, 2]) + (P_cov[1, 3] * A_mat[5, 3]) + (P_cov[1, 4] * A_mat[5, 4]) + (P_cov[1, 5] * A_mat[5, 5]) + (P_cov[1, 6] * A_mat[5, 6])
));
r_TmpSum := r_TmpSum + (A_mat[2, 2] * (
    (P_cov[2, 1] * A_mat[5, 1]) + (P_cov[2, 2] * A_mat[5, 2]) + (P_cov[2, 3] * A_mat[5, 3]) + (P_cov[2, 4] * A_mat[5, 4]) + (P_cov[2, 5] * A_mat[5, 5]) + (P_cov[2, 6] * A_mat[5, 6])
));
r_TmpSum := r_TmpSum + (A_mat[2, 3] * (
    (P_cov[3, 1] * A_mat[5, 1]) + (P_cov[3, 2] * A_mat[5, 2]) + (P_cov[3, 3] * A_mat[5, 3]) + (P_cov[3, 4] * A_mat[5, 4]) + (P_cov[3, 5] * A_mat[5, 5]) + (P_cov[3, 6] * A_mat[5, 6])
));
r_TmpSum := r_TmpSum + (A_mat[2, 4] * (
    (P_cov[4, 1] * A_mat[5, 1]) + (P_cov[4, 2] * A_mat[5, 2]) + (P_cov[4, 3] * A_mat[5, 3]) + (P_cov[4, 4] * A_mat[5, 4]) + (P_cov[4, 5] * A_mat[5, 5]) + (P_cov[4, 6] * A_mat[5, 6])
));
r_TmpSum := r_TmpSum + (A_mat[2, 5] * (
    (P_cov[5, 1] * A_mat[5, 1]) + (P_cov[5, 2] * A_mat[5, 2]) + (P_cov[5, 3] * A_mat[5, 3]) + (P_cov[5, 4] * A_mat[5, 4]) + (P_cov[5, 5] * A_mat[5, 5]) + (P_cov[5, 6] * A_mat[5, 6])
));
r_TmpSum := r_TmpSum + (A_mat[2, 6] * (
    (P_cov[6, 1] * A_mat[5, 1]) + (P_cov[6, 2] * A_mat[5, 2]) + (P_cov[6, 3] * A_mat[5, 3]) + (P_cov[6, 4] * A_mat[5, 4]) + (P_cov[6, 5] * A_mat[5, 5]) + (P_cov[6, 6] * A_mat[5, 6])
));
P_cov[2, 5] := r_TmpSum;
(* Element P_pred[2, 6] *)
r_TmpSum := 0.0;
r_TmpSum := r_TmpSum + (A_mat[2, 1] * (
    (P_cov[1, 1] * A_mat[6, 1]) + (P_cov[1, 2] * A_mat[6, 2]) + (P_cov[1, 3] * A_mat[6, 3]) + (P_cov[1, 4] * A_mat[6, 4]) + (P_cov[1, 5] * A_mat[6, 5]) + (P_cov[1, 6] * A_mat[6, 6])
));
r_TmpSum := r_TmpSum + (A_mat[2, 2] * (
    (P_cov[2, 1] * A_mat[6, 1]) + (P_cov[2, 2] * A_mat[6, 2]) + (P_cov[2, 3] * A_mat[6, 3]) + (P_cov[2, 4] * A_mat[6, 4]) + (P_cov[2, 5] * A_mat[6, 5]) + (P_cov[2, 6] * A_mat[6, 6])
));
r_TmpSum := r_TmpSum + (A_mat[2, 3] * (
    (P_cov[3, 1] * A_mat[6, 1]) + (P_cov[3, 2] * A_mat[6, 2]) + (P_cov[3, 3] * A_mat[6, 3]) + (P_cov[3, 4] * A_mat[6, 4]) + (P_cov[3, 5] * A_mat[6, 5]) + (P_cov[3, 6] * A_mat[6, 6])
));
r_TmpSum := r_TmpSum + (A_mat[2, 4] * (
    (P_cov[4, 1] * A_mat[6, 1]) + (P_cov[4, 2] * A_mat[6, 2]) + (P_cov[4, 3] * A_mat[6, 3]) + (P_cov[4, 4] * A_mat[6, 4]) + (P_cov[4, 5] * A_mat[6, 5]) + (P_cov[4, 6] * A_mat[6, 6])
));
r_TmpSum := r_TmpSum + (A_mat[2, 5] * (
    (P_cov[5, 1] * A_mat[6, 1]) + (P_cov[5, 2] * A_mat[6, 2]) + (P_cov[5, 3] * A_mat[6, 3]) + (P_cov[5, 4] * A_mat[6, 4]) + (P_cov[5, 5] * A_mat[6, 5]) + (P_cov[5, 6] * A_mat[6, 6])
));
r_TmpSum := r_TmpSum + (A_mat[2, 6] * (
    (P_cov[6, 1] * A_mat[6, 1]) + (P_cov[6, 2] * A_mat[6, 2]) + (P_cov[6, 3] * A_mat[6, 3]) + (P_cov[6, 4] * A_mat[6, 4]) + (P_cov[6, 5] * A_mat[6, 5]) + (P_cov[6, 6] * A_mat[6, 6])
));
P_cov[2, 6] := r_TmpSum;
(* Element P_pred[3, 1] *)
r_TmpSum := 0.0;
r_TmpSum := r_TmpSum + (A_mat[3, 1] * (
    (P_cov[1, 1] * A_mat[1, 1]) + (P_cov[1, 2] * A_mat[1, 2]) + (P_cov[1, 3] * A_mat[1, 3]) + (P_cov[1, 4] * A_mat[1, 4]) + (P_cov[1, 5] * A_mat[1, 5]) + (P_cov[1, 6] * A_mat[1, 6])
));
r_TmpSum := r_TmpSum + (A_mat[3, 2] * (
    (P_cov[2, 1] * A_mat[1, 1]) + (P_cov[2, 2] * A_mat[1, 2]) + (P_cov[2, 3] * A_mat[1, 3]) + (P_cov[2, 4] * A_mat[1, 4]) + (P_cov[2, 5] * A_mat[1, 5]) + (P_cov[2, 6] * A_mat[1, 6])
));
r_TmpSum := r_TmpSum + (A_mat[3, 3] * (
    (P_cov[3, 1] * A_mat[1, 1]) + (P_cov[3, 2] * A_mat[1, 2]) + (P_cov[3, 3] * A_mat[1, 3]) + (P_cov[3, 4] * A_mat[1, 4]) + (P_cov[3, 5] * A_mat[1, 5]) + (P_cov[3, 6] * A_mat[1, 6])
));
r_TmpSum := r_TmpSum + (A_mat[3, 4] * (
    (P_cov[4, 1] * A_mat[1, 1]) + (P_cov[4, 2] * A_mat[1, 2]) + (P_cov[4, 3] * A_mat[1, 3]) + (P_cov[4, 4] * A_mat[1, 4]) + (P_cov[4, 5] * A_mat[1, 5]) + (P_cov[4, 6] * A_mat[1, 6])
));
r_TmpSum := r_TmpSum + (A_mat[3, 5] * (
    (P_cov[5, 1] * A_mat[1, 1]) + (P_cov[5, 2] * A_mat[1, 2]) + (P_cov[5, 3] * A_mat[1, 3]) + (P_cov[5, 4] * A_mat[1, 4]) + (P_cov[5, 5] * A_mat[1, 5]) + (P_cov[5, 6] * A_mat[1, 6])
));
r_TmpSum := r_TmpSum + (A_mat[3, 6] * (
    (P_cov[6, 1] * A_mat[1, 1]) + (P_cov[6, 2] * A_mat[1, 2]) + (P_cov[6, 3] * A_mat[1, 3]) + (P_cov[6, 4] * A_mat[1, 4]) + (P_cov[6, 5] * A_mat[1, 5]) + (P_cov[6, 6] * A_mat[1, 6])
));
P_cov[3, 1] := r_TmpSum;
(* Element P_pred[3, 2] *)
r_TmpSum := 0.0;
r_TmpSum := r_TmpSum + (A_mat[3, 1] * (
    (P_cov[1, 1] * A_mat[2, 1]) + (P_cov[1, 2] * A_mat[2, 2]) + (P_cov[1, 3] * A_mat[2, 3]) + (P_cov[1, 4] * A_mat[2, 4]) + (P_cov[1, 5] * A_mat[2, 5]) + (P_cov[1, 6] * A_mat[2, 6])
));
r_TmpSum := r_TmpSum + (A_mat[3, 2] * (
    (P_cov[2, 1] * A_mat[2, 1]) + (P_cov[2, 2] * A_mat[2, 2]) + (P_cov[2, 3] * A_mat[2, 3]) + (P_cov[2, 4] * A_mat[2, 4]) + (P_cov[2, 5] * A_mat[2, 5]) + (P_cov[2, 6] * A_mat[2, 6])
));
r_TmpSum := r_TmpSum + (A_mat[3, 3] * (
    (P_cov[3, 1] * A_mat[2, 1]) + (P_cov[3, 2] * A_mat[2, 2]) + (P_cov[3, 3] * A_mat[2, 3]) + (P_cov[3, 4] * A_mat[2, 4]) + (P_cov[3, 5] * A_mat[2, 5]) + (P_cov[3, 6] * A_mat[2, 6])
));
r_TmpSum := r_TmpSum + (A_mat[3, 4] * (
    (P_cov[4, 1] * A_mat[2, 1]) + (P_cov[4, 2] * A_mat[2, 2]) + (P_cov[4, 3] * A_mat[2, 3]) + (P_cov[4, 4] * A_mat[2, 4]) + (P_cov[4, 5] * A_mat[2, 5]) + (P_cov[4, 6] * A_mat[2, 6])
));
r_TmpSum := r_TmpSum + (A_mat[3, 5] * (
    (P_cov[5, 1] * A_mat[2, 1]) + (P_cov[5, 2] * A_mat[2, 2]) + (P_cov[5, 3] * A_mat[2, 3]) + (P_cov[5, 4] * A_mat[2, 4]) + (P_cov[5, 5] * A_mat[2, 5]) + (P_cov[5, 6] * A_mat[2, 6])
));
r_TmpSum := r_TmpSum + (A_mat[3, 6] * (
    (P_cov[6, 1] * A_mat[2, 1]) + (P_cov[6, 2] * A_mat[2, 2]) + (P_cov[6, 3] * A_mat[2, 3]) + (P_cov[6, 4] * A_mat[2, 4]) + (P_cov[6, 5] * A_mat[2, 5]) + (P_cov[6, 6] * A_mat[2, 6])
));
P_cov[3, 2] := r_TmpSum;
(* Element P_pred[3, 3] *)
r_TmpSum := 0.0;
r_TmpSum := r_TmpSum + (A_mat[3, 1] * (
    (P_cov[1, 1] * A_mat[3, 1]) + (P_cov[1, 2] * A_mat[3, 2]) + (P_cov[1, 3] * A_mat[3, 3]) + (P_cov[1, 4] * A_mat[3, 4]) + (P_cov[1, 5] * A_mat[3, 5]) + (P_cov[1, 6] * A_mat[3, 6])
));
r_TmpSum := r_TmpSum + (A_mat[3, 2] * (
    (P_cov[2, 1] * A_mat[3, 1]) + (P_cov[2, 2] * A_mat[3, 2]) + (P_cov[2, 3] * A_mat[3, 3]) + (P_cov[2, 4] * A_mat[3, 4]) + (P_cov[2, 5] * A_mat[3, 5]) + (P_cov[2, 6] * A_mat[3, 6])
));
r_TmpSum := r_TmpSum + (A_mat[3, 3] * (
    (P_cov[3, 1] * A_mat[3, 1]) + (P_cov[3, 2] * A_mat[3, 2]) + (P_cov[3, 3] * A_mat[3, 3]) + (P_cov[3, 4] * A_mat[3, 4]) + (P_cov[3, 5] * A_mat[3, 5]) + (P_cov[3, 6] * A_mat[3, 6])
));
r_TmpSum := r_TmpSum + (A_mat[3, 4] * (
    (P_cov[4, 1] * A_mat[3, 1]) + (P_cov[4, 2] * A_mat[3, 2]) + (P_cov[4, 3] * A_mat[3, 3]) + (P_cov[4, 4] * A_mat[3, 4]) + (P_cov[4, 5] * A_mat[3, 5]) + (P_cov[4, 6] * A_mat[3, 6])
));
r_TmpSum := r_TmpSum + (A_mat[3, 5] * (
    (P_cov[5, 1] * A_mat[3, 1]) + (P_cov[5, 2] * A_mat[3, 2]) + (P_cov[5, 3] * A_mat[3, 3]) + (P_cov[5, 4] * A_mat[3, 4]) + (P_cov[5, 5] * A_mat[3, 5]) + (P_cov[5, 6] * A_mat[3, 6])
));
r_TmpSum := r_TmpSum + (A_mat[3, 6] * (
    (P_cov[6, 1] * A_mat[3, 1]) + (P_cov[6, 2] * A_mat[3, 2]) + (P_cov[6, 3] * A_mat[3, 3]) + (P_cov[6, 4] * A_mat[3, 4]) + (P_cov[6, 5] * A_mat[3, 5]) + (P_cov[6, 6] * A_mat[3, 6])
));
P_cov[3, 3] := r_TmpSum + Q_obs_diag[3];
(* Element P_pred[3, 4] *)
r_TmpSum := 0.0;
r_TmpSum := r_TmpSum + (A_mat[3, 1] * (
    (P_cov[1, 1] * A_mat[4, 1]) + (P_cov[1, 2] * A_mat[4, 2]) + (P_cov[1, 3] * A_mat[4, 3]) + (P_cov[1, 4] * A_mat[4, 4]) + (P_cov[1, 5] * A_mat[4, 5]) + (P_cov[1, 6] * A_mat[4, 6])
));
r_TmpSum := r_TmpSum + (A_mat[3, 2] * (
    (P_cov[2, 1] * A_mat[4, 1]) + (P_cov[2, 2] * A_mat[4, 2]) + (P_cov[2, 3] * A_mat[4, 3]) + (P_cov[2, 4] * A_mat[4, 4]) + (P_cov[2, 5] * A_mat[4, 5]) + (P_cov[2, 6] * A_mat[4, 6])
));
r_TmpSum := r_TmpSum + (A_mat[3, 3] * (
    (P_cov[3, 1] * A_mat[4, 1]) + (P_cov[3, 2] * A_mat[4, 2]) + (P_cov[3, 3] * A_mat[4, 3]) + (P_cov[3, 4] * A_mat[4, 4]) + (P_cov[3, 5] * A_mat[4, 5]) + (P_cov[3, 6] * A_mat[4, 6])
));
r_TmpSum := r_TmpSum + (A_mat[3, 4] * (
    (P_cov[4, 1] * A_mat[4, 1]) + (P_cov[4, 2] * A_mat[4, 2]) + (P_cov[4, 3] * A_mat[4, 3]) + (P_cov[4, 4] * A_mat[4, 4]) + (P_cov[4, 5] * A_mat[4, 5]) + (P_cov[4, 6] * A_mat[4, 6])
));
r_TmpSum := r_TmpSum + (A_mat[3, 5] * (
    (P_cov[5, 1] * A_mat[4, 1]) + (P_cov[5, 2] * A_mat[4, 2]) + (P_cov[5, 3] * A_mat[4, 3]) + (P_cov[5, 4] * A_mat[4, 4]) + (P_cov[5, 5] * A_mat[4, 5]) + (P_cov[5, 6] * A_mat[4, 6])
));
r_TmpSum := r_TmpSum + (A_mat[3, 6] * (
    (P_cov[6, 1] * A_mat[4, 1]) + (P_cov[6, 2] * A_mat[4, 2]) + (P_cov[6, 3] * A_mat[4, 3]) + (P_cov[6, 4] * A_mat[4, 4]) + (P_cov[6, 5] * A_mat[4, 5]) + (P_cov[6, 6] * A_mat[4, 6])
));
P_cov[3, 4] := r_TmpSum;
(* Element P_pred[3, 5] *)
r_TmpSum := 0.0;
r_TmpSum := r_TmpSum + (A_mat[3, 1] * (
    (P_cov[1, 1] * A_mat[5, 1]) + (P_cov[1, 2] * A_mat[5, 2]) + (P_cov[1, 3] * A_mat[5, 3]) + (P_cov[1, 4] * A_mat[5, 4]) + (P_cov[1, 5] * A_mat[5, 5]) + (P_cov[1, 6] * A_mat[5, 6])
));
r_TmpSum := r_TmpSum + (A_mat[3, 2] * (
    (P_cov[2, 1] * A_mat[5, 1]) + (P_cov[2, 2] * A_mat[5, 2]) + (P_cov[2, 3] * A_mat[5, 3]) + (P_cov[2, 4] * A_mat[5, 4]) + (P_cov[2, 5] * A_mat[5, 5]) + (P_cov[2, 6] * A_mat[5, 6])
));
r_TmpSum := r_TmpSum + (A_mat[3, 3] * (
    (P_cov[3, 1] * A_mat[5, 1]) + (P_cov[3, 2] * A_mat[5, 2]) + (P_cov[3, 3] * A_mat[5, 3]) + (P_cov[3, 4] * A_mat[5, 4]) + (P_cov[3, 5] * A_mat[5, 5]) + (P_cov[3, 6] * A_mat[5, 6])
));
r_TmpSum := r_TmpSum + (A_mat[3, 4] * (
    (P_cov[4, 1] * A_mat[5, 1]) + (P_cov[4, 2] * A_mat[5, 2]) + (P_cov[4, 3] * A_mat[5, 3]) + (P_cov[4, 4] * A_mat[5, 4]) + (P_cov[4, 5] * A_mat[5, 5]) + (P_cov[4, 6] * A_mat[5, 6])
));
r_TmpSum := r_TmpSum + (A_mat[3, 5] * (
    (P_cov[5, 1] * A_mat[5, 1]) + (P_cov[5, 2] * A_mat[5, 2]) + (P_cov[5, 3] * A_mat[5, 3]) + (P_cov[5, 4] * A_mat[5, 4]) + (P_cov[5, 5] * A_mat[5, 5]) + (P_cov[5, 6] * A_mat[5, 6])
));
r_TmpSum := r_TmpSum + (A_mat[3, 6] * (
    (P_cov[6, 1] * A_mat[5, 1]) + (P_cov[6, 2] * A_mat[5, 2]) + (P_cov[6, 3] * A_mat[5, 3]) + (P_cov[6, 4] * A_mat[5, 4]) + (P_cov[6, 5] * A_mat[5, 5]) + (P_cov[6, 6] * A_mat[5, 6])
));
P_cov[3, 5] := r_TmpSum;
(* Element P_pred[3, 6] *)
r_TmpSum := 0.0;
r_TmpSum := r_TmpSum + (A_mat[3, 1] * (
    (P_cov[1, 1] * A_mat[6, 1]) + (P_cov[1, 2] * A_mat[6, 2]) + (P_cov[1, 3] * A_mat[6, 3]) + (P_cov[1, 4] * A_mat[6, 4]) + (P_cov[1, 5] * A_mat[6, 5]) + (P_cov[1, 6] * A_mat[6, 6])
));
r_TmpSum := r_TmpSum + (A_mat[3, 2] * (
    (P_cov[2, 1] * A_mat[6, 1]) + (P_cov[2, 2] * A_mat[6, 2]) + (P_cov[2, 3] * A_mat[6, 3]) + (P_cov[2, 4] * A_mat[6, 4]) + (P_cov[2, 5] * A_mat[6, 5]) + (P_cov[2, 6] * A_mat[6, 6])
));
r_TmpSum := r_TmpSum + (A_mat[3, 3] * (
    (P_cov[3, 1] * A_mat[6, 1]) + (P_cov[3, 2] * A_mat[6, 2]) + (P_cov[3, 3] * A_mat[6, 3]) + (P_cov[3, 4] * A_mat[6, 4]) + (P_cov[3, 5] * A_mat[6, 5]) + (P_cov[3, 6] * A_mat[6, 6])
));
r_TmpSum := r_TmpSum + (A_mat[3, 4] * (
    (P_cov[4, 1] * A_mat[6, 1]) + (P_cov[4, 2] * A_mat[6, 2]) + (P_cov[4, 3] * A_mat[6, 3]) + (P_cov[4, 4] * A_mat[6, 4]) + (P_cov[4, 5] * A_mat[6, 5]) + (P_cov[4, 6] * A_mat[6, 6])
));
r_TmpSum := r_TmpSum + (A_mat[3, 5] * (
    (P_cov[5, 1] * A_mat[6, 1]) + (P_cov[5, 2] * A_mat[6, 2]) + (P_cov[5, 3] * A_mat[6, 3]) + (P_cov[5, 4] * A_mat[6, 4]) + (P_cov[5, 5] * A_mat[6, 5]) + (P_cov[5, 6] * A_mat[6, 6])
));
r_TmpSum := r_TmpSum + (A_mat[3, 6] * (
    (P_cov[6, 1] * A_mat[6, 1]) + (P_cov[6, 2] * A_mat[6, 2]) + (P_cov[6, 3] * A_mat[6, 3]) + (P_cov[6, 4] * A_mat[6, 4]) + (P_cov[6, 5] * A_mat[6, 5]) + (P_cov[6, 6] * A_mat[6, 6])
));
P_cov[3, 6] := r_TmpSum;
(* Element P_pred[4, 1] *)
r_TmpSum := 0.0;
r_TmpSum := r_TmpSum + (A_mat[4, 1] * (
    (P_cov[1, 1] * A_mat[1, 1]) + (P_cov[1, 2] * A_mat[1, 2]) + (P_cov[1, 3] * A_mat[1, 3]) + (P_cov[1, 4] * A_mat[1, 4]) + (P_cov[1, 5] * A_mat[1, 5]) + (P_cov[1, 6] * A_mat[1, 6])
));
r_TmpSum := r_TmpSum + (A_mat[4, 2] * (
    (P_cov[2, 1] * A_mat[1, 1]) + (P_cov[2, 2] * A_mat[1, 2]) + (P_cov[2, 3] * A_mat[1, 3]) + (P_cov[2, 4] * A_mat[1, 4]) + (P_cov[2, 5] * A_mat[1, 5]) + (P_cov[2, 6] * A_mat[1, 6])
));
r_TmpSum := r_TmpSum + (A_mat[4, 3] * (
    (P_cov[3, 1] * A_mat[1, 1]) + (P_cov[3, 2] * A_mat[1, 2]) + (P_cov[3, 3] * A_mat[1, 3]) + (P_cov[3, 4] * A_mat[1, 4]) + (P_cov[3, 5] * A_mat[1, 5]) + (P_cov[3, 6] * A_mat[1, 6])
));
r_TmpSum := r_TmpSum + (A_mat[4, 4] * (
    (P_cov[4, 1] * A_mat[1, 1]) + (P_cov[4, 2] * A_mat[1, 2]) + (P_cov[4, 3] * A_mat[1, 3]) + (P_cov[4, 4] * A_mat[1, 4]) + (P_cov[4, 5] * A_mat[1, 5]) + (P_cov[4, 6] * A_mat[1, 6])
));
r_TmpSum := r_TmpSum + (A_mat[4, 5] * (
    (P_cov[5, 1] * A_mat[1, 1]) + (P_cov[5, 2] * A_mat[1, 2]) + (P_cov[5, 3] * A_mat[1, 3]) + (P_cov[5, 4] * A_mat[1, 4]) + (P_cov[5, 5] * A_mat[1, 5]) + (P_cov[5, 6] * A_mat[1, 6])
));
r_TmpSum := r_TmpSum + (A_mat[4, 6] * (
    (P_cov[6, 1] * A_mat[1, 1]) + (P_cov[6, 2] * A_mat[1, 2]) + (P_cov[6, 3] * A_mat[1, 3]) + (P_cov[6, 4] * A_mat[1, 4]) + (P_cov[6, 5] * A_mat[1, 5]) + (P_cov[6, 6] * A_mat[1, 6])
));
P_cov[4, 1] := r_TmpSum;
(* Element P_pred[4, 2] *)
r_TmpSum := 0.0;
r_TmpSum := r_TmpSum + (A_mat[4, 1] * (
    (P_cov[1, 1] * A_mat[2, 1]) + (P_cov[1, 2] * A_mat[2, 2]) + (P_cov[1, 3] * A_mat[2, 3]) + (P_cov[1, 4] * A_mat[2, 4]) + (P_cov[1, 5] * A_mat[2, 5]) + (P_cov[1, 6] * A_mat[2, 6])
));
r_TmpSum := r_TmpSum + (A_mat[4, 2] * (
    (P_cov[2, 1] * A_mat[2, 1]) + (P_cov[2, 2] * A_mat[2, 2]) + (P_cov[2, 3] * A_mat[2, 3]) + (P_cov[2, 4] * A_mat[2, 4]) + (P_cov[2, 5] * A_mat[2, 5]) + (P_cov[2, 6] * A_mat[2, 6])
));
r_TmpSum := r_TmpSum + (A_mat[4, 3] * (
    (P_cov[3, 1] * A_mat[2, 1]) + (P_cov[3, 2] * A_mat[2, 2]) + (P_cov[3, 3] * A_mat[2, 3]) + (P_cov[3, 4] * A_mat[2, 4]) + (P_cov[3, 5] * A_mat[2, 5]) + (P_cov[3, 6] * A_mat[2, 6])
));
r_TmpSum := r_TmpSum + (A_mat[4, 4] * (
    (P_cov[4, 1] * A_mat[2, 1]) + (P_cov[4, 2] * A_mat[2, 2]) + (P_cov[4, 3] * A_mat[2, 3]) + (P_cov[4, 4] * A_mat[2, 4]) + (P_cov[4, 5] * A_mat[2, 5]) + (P_cov[4, 6] * A_mat[2, 6])
));
r_TmpSum := r_TmpSum + (A_mat[4, 5] * (
    (P_cov[5, 1] * A_mat[2, 1]) + (P_cov[5, 2] * A_mat[2, 2]) + (P_cov[5, 3] * A_mat[2, 3]) + (P_cov[5, 4] * A_mat[2, 4]) + (P_cov[5, 5] * A_mat[2, 5]) + (P_cov[5, 6] * A_mat[2, 6])
));
r_TmpSum := r_TmpSum + (A_mat[4, 6] * (
    (P_cov[6, 1] * A_mat[2, 1]) + (P_cov[6, 2] * A_mat[2, 2]) + (P_cov[6, 3] * A_mat[2, 3]) + (P_cov[6, 4] * A_mat[2, 4]) + (P_cov[6, 5] * A_mat[2, 5]) + (P_cov[6, 6] * A_mat[2, 6])
));
P_cov[4, 2] := r_TmpSum;
(* Element P_pred[4, 3] *)
r_TmpSum := 0.0;
r_TmpSum := r_TmpSum + (A_mat[4, 1] * (
    (P_cov[1, 1] * A_mat[3, 1]) + (P_cov[1, 2] * A_mat[3, 2]) + (P_cov[1, 3] * A_mat[3, 3]) + (P_cov[1, 4] * A_mat[3, 4]) + (P_cov[1, 5] * A_mat[3, 5]) + (P_cov[1, 6] * A_mat[3, 6])
));
r_TmpSum := r_TmpSum + (A_mat[4, 2] * (
    (P_cov[2, 1] * A_mat[3, 1]) + (P_cov[2, 2] * A_mat[3, 2]) + (P_cov[2, 3] * A_mat[3, 3]) + (P_cov[2, 4] * A_mat[3, 4]) + (P_cov[2, 5] * A_mat[3, 5]) + (P_cov[2, 6] * A_mat[3, 6])
));
r_TmpSum := r_TmpSum + (A_mat[4, 3] * (
    (P_cov[3, 1] * A_mat[3, 1]) + (P_cov[3, 2] * A_mat[3, 2]) + (P_cov[3, 3] * A_mat[3, 3]) + (P_cov[3, 4] * A_mat[3, 4]) + (P_cov[3, 5] * A_mat[3, 5]) + (P_cov[3, 6] * A_mat[3, 6])
));
r_TmpSum := r_TmpSum + (A_mat[4, 4] * (
    (P_cov[4, 1] * A_mat[3, 1]) + (P_cov[4, 2] * A_mat[3, 2]) + (P_cov[4, 3] * A_mat[3, 3]) + (P_cov[4, 4] * A_mat[3, 4]) + (P_cov[4, 5] * A_mat[3, 5]) + (P_cov[4, 6] * A_mat[3, 6])
));
r_TmpSum := r_TmpSum + (A_mat[4, 5] * (
    (P_cov[5, 1] * A_mat[3, 1]) + (P_cov[5, 2] * A_mat[3, 2]) + (P_cov[5, 3] * A_mat[3, 3]) + (P_cov[5, 4] * A_mat[3, 4]) + (P_cov[5, 5] * A_mat[3, 5]) + (P_cov[5, 6] * A_mat[3, 6])
));
r_TmpSum := r_TmpSum + (A_mat[4, 6] * (
    (P_cov[6, 1] * A_mat[3, 1]) + (P_cov[6, 2] * A_mat[3, 2]) + (P_cov[6, 3] * A_mat[3, 3]) + (P_cov[6, 4] * A_mat[3, 4]) + (P_cov[6, 5] * A_mat[3, 5]) + (P_cov[6, 6] * A_mat[3, 6])
));
P_cov[4, 3] := r_TmpSum;
(* Element P_pred[4, 4] *)
r_TmpSum := 0.0;
r_TmpSum := r_TmpSum + (A_mat[4, 1] * (
    (P_cov[1, 1] * A_mat[4, 1]) + (P_cov[1, 2] * A_mat[4, 2]) + (P_cov[1, 3] * A_mat[4, 3]) + (P_cov[1, 4] * A_mat[4, 4]) + (P_cov[1, 5] * A_mat[4, 5]) + (P_cov[1, 6] * A_mat[4, 6])
));
r_TmpSum := r_TmpSum + (A_mat[4, 2] * (
    (P_cov[2, 1] * A_mat[4, 1]) + (P_cov[2, 2] * A_mat[4, 2]) + (P_cov[2, 3] * A_mat[4, 3]) + (P_cov[2, 4] * A_mat[4, 4]) + (P_cov[2, 5] * A_mat[4, 5]) + (P_cov[2, 6] * A_mat[4, 6])
));
r_TmpSum := r_TmpSum + (A_mat[4, 3] * (
    (P_cov[3, 1] * A_mat[4, 1]) + (P_cov[3, 2] * A_mat[4, 2]) + (P_cov[3, 3] * A_mat[4, 3]) + (P_cov[3, 4] * A_mat[4, 4]) + (P_cov[3, 5] * A_mat[4, 5]) + (P_cov[3, 6] * A_mat[4, 6])
));
r_TmpSum := r_TmpSum + (A_mat[4, 4] * (
    (P_cov[4, 1] * A_mat[4, 1]) + (P_cov[4, 2] * A_mat[4, 2]) + (P_cov[4, 3] * A_mat[4, 3]) + (P_cov[4, 4] * A_mat[4, 4]) + (P_cov[4, 5] * A_mat[4, 5]) + (P_cov[4, 6] * A_mat[4, 6])
));
r_TmpSum := r_TmpSum + (A_mat[4, 5] * (
    (P_cov[5, 1] * A_mat[4, 1]) + (P_cov[5, 2] * A_mat[4, 2]) + (P_cov[5, 3] * A_mat[4, 3]) + (P_cov[5, 4] * A_mat[4, 4]) + (P_cov[5, 5] * A_mat[4, 5]) + (P_cov[5, 6] * A_mat[4, 6])
));
r_TmpSum := r_TmpSum + (A_mat[4, 6] * (
    (P_cov[6, 1] * A_mat[4, 1]) + (P_cov[6, 2] * A_mat[4, 2]) + (P_cov[6, 3] * A_mat[4, 3]) + (P_cov[6, 4] * A_mat[4, 4]) + (P_cov[6, 5] * A_mat[4, 5]) + (P_cov[6, 6] * A_mat[4, 6])
));
P_cov[4, 4] := r_TmpSum + Q_obs_diag[4];
(* Element P_pred[4, 5] *)
r_TmpSum := 0.0;
r_TmpSum := r_TmpSum + (A_mat[4, 1] * (
    (P_cov[1, 1] * A_mat[5, 1]) + (P_cov[1, 2] * A_mat[5, 2]) + (P_cov[1, 3] * A_mat[5, 3]) + (P_cov[1, 4] * A_mat[5, 4]) + (P_cov[1, 5] * A_mat[5, 5]) + (P_cov[1, 6] * A_mat[5, 6])
));
r_TmpSum := r_TmpSum + (A_mat[4, 2] * (
    (P_cov[2, 1] * A_mat[5, 1]) + (P_cov[2, 2] * A_mat[5, 2]) + (P_cov[2, 3] * A_mat[5, 3]) + (P_cov[2, 4] * A_mat[5, 4]) + (P_cov[2, 5] * A_mat[5, 5]) + (P_cov[2, 6] * A_mat[5, 6])
));
r_TmpSum := r_TmpSum + (A_mat[4, 3] * (
    (P_cov[3, 1] * A_mat[5, 1]) + (P_cov[3, 2] * A_mat[5, 2]) + (P_cov[3, 3] * A_mat[5, 3]) + (P_cov[3, 4] * A_mat[5, 4]) + (P_cov[3, 5] * A_mat[5, 5]) + (P_cov[3, 6] * A_mat[5, 6])
));
r_TmpSum := r_TmpSum + (A_mat[4, 4] * (
    (P_cov[4, 1] * A_mat[5, 1]) + (P_cov[4, 2] * A_mat[5, 2]) + (P_cov[4, 3] * A_mat[5, 3]) + (P_cov[4, 4] * A_mat[5, 4]) + (P_cov[4, 5] * A_mat[5, 5]) + (P_cov[4, 6] * A_mat[5, 6])
));
r_TmpSum := r_TmpSum + (A_mat[4, 5] * (
    (P_cov[5, 1] * A_mat[5, 1]) + (P_cov[5, 2] * A_mat[5, 2]) + (P_cov[5, 3] * A_mat[5, 3]) + (P_cov[5, 4] * A_mat[5, 4]) + (P_cov[5, 5] * A_mat[5, 5]) + (P_cov[5, 6] * A_mat[5, 6])
));
r_TmpSum := r_TmpSum + (A_mat[4, 6] * (
    (P_cov[6, 1] * A_mat[5, 1]) + (P_cov[6, 2] * A_mat[5, 2]) + (P_cov[6, 3] * A_mat[5, 3]) + (P_cov[6, 4] * A_mat[5, 4]) + (P_cov[6, 5] * A_mat[5, 5]) + (P_cov[6, 6] * A_mat[5, 6])
));
P_cov[4, 5] := r_TmpSum;
(* Element P_pred[4, 6] *)
r_TmpSum := 0.0;
r_TmpSum := r_TmpSum + (A_mat[4, 1] * (
    (P_cov[1, 1] * A_mat[6, 1]) + (P_cov[1, 2] * A_mat[6, 2]) + (P_cov[1, 3] * A_mat[6, 3]) + (P_cov[1, 4] * A_mat[6, 4]) + (P_cov[1, 5] * A_mat[6, 5]) + (P_cov[1, 6] * A_mat[6, 6])
));
r_TmpSum := r_TmpSum + (A_mat[4, 2] * (
    (P_cov[2, 1] * A_mat[6, 1]) + (P_cov[2, 2] * A_mat[6, 2]) + (P_cov[2, 3] * A_mat[6, 3]) + (P_cov[2, 4] * A_mat[6, 4]) + (P_cov[2, 5] * A_mat[6, 5]) + (P_cov[2, 6] * A_mat[6, 6])
));
r_TmpSum := r_TmpSum + (A_mat[4, 3] * (
    (P_cov[3, 1] * A_mat[6, 1]) + (P_cov[3, 2] * A_mat[6, 2]) + (P_cov[3, 3] * A_mat[6, 3]) + (P_cov[3, 4] * A_mat[6, 4]) + (P_cov[3, 5] * A_mat[6, 5]) + (P_cov[3, 6] * A_mat[6, 6])
));
r_TmpSum := r_TmpSum + (A_mat[4, 4] * (
    (P_cov[4, 1] * A_mat[6, 1]) + (P_cov[4, 2] * A_mat[6, 2]) + (P_cov[4, 3] * A_mat[6, 3]) + (P_cov[4, 4] * A_mat[6, 4]) + (P_cov[4, 5] * A_mat[6, 5]) + (P_cov[4, 6] * A_mat[6, 6])
));
r_TmpSum := r_TmpSum + (A_mat[4, 5] * (
    (P_cov[5, 1] * A_mat[6, 1]) + (P_cov[5, 2] * A_mat[6, 2]) + (P_cov[5, 3] * A_mat[6, 3]) + (P_cov[5, 4] * A_mat[6, 4]) + (P_cov[5, 5] * A_mat[6, 5]) + (P_cov[5, 6] * A_mat[6, 6])
));
r_TmpSum := r_TmpSum + (A_mat[4, 6] * (
    (P_cov[6, 1] * A_mat[6, 1]) + (P_cov[6, 2] * A_mat[6, 2]) + (P_cov[6, 3] * A_mat[6, 3]) + (P_cov[6, 4] * A_mat[6, 4]) + (P_cov[6, 5] * A_mat[6, 5]) + (P_cov[6, 6] * A_mat[6, 6])
));
P_cov[4, 6] := r_TmpSum;
(* Element P_pred[5, 1] *)
r_TmpSum := 0.0;
r_TmpSum := r_TmpSum + (A_mat[5, 1] * (
    (P_cov[1, 1] * A_mat[1, 1]) + (P_cov[1, 2] * A_mat[1, 2]) + (P_cov[1, 3] * A_mat[1, 3]) + (P_cov[1, 4] * A_mat[1, 4]) + (P_cov[1, 5] * A_mat[1, 5]) + (P_cov[1, 6] * A_mat[1, 6])
));
r_TmpSum := r_TmpSum + (A_mat[5, 2] * (
    (P_cov[2, 1] * A_mat[1, 1]) + (P_cov[2, 2] * A_mat[1, 2]) + (P_cov[2, 3] * A_mat[1, 3]) + (P_cov[2, 4] * A_mat[1, 4]) + (P_cov[2, 5] * A_mat[1, 5]) + (P_cov[2, 6] * A_mat[1, 6])
));
r_TmpSum := r_TmpSum + (A_mat[5, 3] * (
    (P_cov[3, 1] * A_mat[1, 1]) + (P_cov[3, 2] * A_mat[1, 2]) + (P_cov[3, 3] * A_mat[1, 3]) + (P_cov[3, 4] * A_mat[1, 4]) + (P_cov[3, 5] * A_mat[1, 5]) + (P_cov[3, 6] * A_mat[1, 6])
));
r_TmpSum := r_TmpSum + (A_mat[5, 4] * (
    (P_cov[4, 1] * A_mat[1, 1]) + (P_cov[4, 2] * A_mat[1, 2]) + (P_cov[4, 3] * A_mat[1, 3]) + (P_cov[4, 4] * A_mat[1, 4]) + (P_cov[4, 5] * A_mat[1, 5]) + (P_cov[4, 6] * A_mat[1, 6])
));
r_TmpSum := r_TmpSum + (A_mat[5, 5] * (
    (P_cov[5, 1] * A_mat[1, 1]) + (P_cov[5, 2] * A_mat[1, 2]) + (P_cov[5, 3] * A_mat[1, 3]) + (P_cov[5, 4] * A_mat[1, 4]) + (P_cov[5, 5] * A_mat[1, 5]) + (P_cov[5, 6] * A_mat[1, 6])
));
r_TmpSum := r_TmpSum + (A_mat[5, 6] * (
    (P_cov[6, 1] * A_mat[1, 1]) + (P_cov[6, 2] * A_mat[1, 2]) + (P_cov[6, 3] * A_mat[1, 3]) + (P_cov[6, 4] * A_mat[1, 4]) + (P_cov[6, 5] * A_mat[1, 5]) + (P_cov[6, 6] * A_mat[1, 6])
));
P_cov[5, 1] := r_TmpSum;
(* Element P_pred[5, 2] *)
r_TmpSum := 0.0;
r_TmpSum := r_TmpSum + (A_mat[5, 1] * (
    (P_cov[1, 1] * A_mat[2, 1]) + (P_cov[1, 2] * A_mat[2, 2]) + (P_cov[1, 3] * A_mat[2, 3]) + (P_cov[1, 4] * A_mat[2, 4]) + (P_cov[1, 5] * A_mat[2, 5]) + (P_cov[1, 6] * A_mat[2, 6])
));
r_TmpSum := r_TmpSum + (A_mat[5, 2] * (
    (P_cov[2, 1] * A_mat[2, 1]) + (P_cov[2, 2] * A_mat[2, 2]) + (P_cov[2, 3] * A_mat[2, 3]) + (P_cov[2, 4] * A_mat[2, 4]) + (P_cov[2, 5] * A_mat[2, 5]) + (P_cov[2, 6] * A_mat[2, 6])
));
r_TmpSum := r_TmpSum + (A_mat[5, 3] * (
    (P_cov[3, 1] * A_mat[2, 1]) + (P_cov[3, 2] * A_mat[2, 2]) + (P_cov[3, 3] * A_mat[2, 3]) + (P_cov[3, 4] * A_mat[2, 4]) + (P_cov[3, 5] * A_mat[2, 5]) + (P_cov[3, 6] * A_mat[2, 6])
));
r_TmpSum := r_TmpSum + (A_mat[5, 4] * (
    (P_cov[4, 1] * A_mat[2, 1]) + (P_cov[4, 2] * A_mat[2, 2]) + (P_cov[4, 3] * A_mat[2, 3]) + (P_cov[4, 4] * A_mat[2, 4]) + (P_cov[4, 5] * A_mat[2, 5]) + (P_cov[4, 6] * A_mat[2, 6])
));
r_TmpSum := r_TmpSum + (A_mat[5, 5] * (
    (P_cov[5, 1] * A_mat[2, 1]) + (P_cov[5, 2] * A_mat[2, 2]) + (P_cov[5, 3] * A_mat[2, 3]) + (P_cov[5, 4] * A_mat[2, 4]) + (P_cov[5, 5] * A_mat[2, 5]) + (P_cov[5, 6] * A_mat[2, 6])
));
r_TmpSum := r_TmpSum + (A_mat[5, 6] * (
    (P_cov[6, 1] * A_mat[2, 1]) + (P_cov[6, 2] * A_mat[2, 2]) + (P_cov[6, 3] * A_mat[2, 3]) + (P_cov[6, 4] * A_mat[2, 4]) + (P_cov[6, 5] * A_mat[2, 5]) + (P_cov[6, 6] * A_mat[2, 6])
));
P_cov[5, 2] := r_TmpSum;
(* Element P_pred[5, 3] *)
r_TmpSum := 0.0;
r_TmpSum := r_TmpSum + (A_mat[5, 1] * (
    (P_cov[1, 1] * A_mat[3, 1]) + (P_cov[1, 2] * A_mat[3, 2]) + (P_cov[1, 3] * A_mat[3, 3]) + (P_cov[1, 4] * A_mat[3, 4]) + (P_cov[1, 5] * A_mat[3, 5]) + (P_cov[1, 6] * A_mat[3, 6])
));
r_TmpSum := r_TmpSum + (A_mat[5, 2] * (
    (P_cov[2, 1] * A_mat[3, 1]) + (P_cov[2, 2] * A_mat[3, 2]) + (P_cov[2, 3] * A_mat[3, 3]) + (P_cov[2, 4] * A_mat[3, 4]) + (P_cov[2, 5] * A_mat[3, 5]) + (P_cov[2, 6] * A_mat[3, 6])
));
r_TmpSum := r_TmpSum + (A_mat[5, 3] * (
    (P_cov[3, 1] * A_mat[3, 1]) + (P_cov[3, 2] * A_mat[3, 2]) + (P_cov[3, 3] * A_mat[3, 3]) + (P_cov[3, 4] * A_mat[3, 4]) + (P_cov[3, 5] * A_mat[3, 5]) + (P_cov[3, 6] * A_mat[3, 6])
));
r_TmpSum := r_TmpSum + (A_mat[5, 4] * (
    (P_cov[4, 1] * A_mat[3, 1]) + (P_cov[4, 2] * A_mat[3, 2]) + (P_cov[4, 3] * A_mat[3, 3]) + (P_cov[4, 4] * A_mat[3, 4]) + (P_cov[4, 5] * A_mat[3, 5]) + (P_cov[4, 6] * A_mat[3, 6])
));
r_TmpSum := r_TmpSum + (A_mat[5, 5] * (
    (P_cov[5, 1] * A_mat[3, 1]) + (P_cov[5, 2] * A_mat[3, 2]) + (P_cov[5, 3] * A_mat[3, 3]) + (P_cov[5, 4] * A_mat[3, 4]) + (P_cov[5, 5] * A_mat[3, 5]) + (P_cov[5, 6] * A_mat[3, 6])
));
r_TmpSum := r_TmpSum + (A_mat[5, 6] * (
    (P_cov[6, 1] * A_mat[3, 1]) + (P_cov[6, 2] * A_mat[3, 2]) + (P_cov[6, 3] * A_mat[3, 3]) + (P_cov[6, 4] * A_mat[3, 4]) + (P_cov[6, 5] * A_mat[3, 5]) + (P_cov[6, 6] * A_mat[3, 6])
));
P_cov[5, 3] := r_TmpSum;
(* Element P_pred[5, 4] *)
r_TmpSum := 0.0;
r_TmpSum := r_TmpSum + (A_mat[5, 1] * (
    (P_cov[1, 1] * A_mat[4, 1]) + (P_cov[1, 2] * A_mat[4, 2]) + (P_cov[1, 3] * A_mat[4, 3]) + (P_cov[1, 4] * A_mat[4, 4]) + (P_cov[1, 5] * A_mat[4, 5]) + (P_cov[1, 6] * A_mat[4, 6])
));
r_TmpSum := r_TmpSum + (A_mat[5, 2] * (
    (P_cov[2, 1] * A_mat[4, 1]) + (P_cov[2, 2] * A_mat[4, 2]) + (P_cov[2, 3] * A_mat[4, 3]) + (P_cov[2, 4] * A_mat[4, 4]) + (P_cov[2, 5] * A_mat[4, 5]) + (P_cov[2, 6] * A_mat[4, 6])
));
r_TmpSum := r_TmpSum + (A_mat[5, 3] * (
    (P_cov[3, 1] * A_mat[4, 1]) + (P_cov[3, 2] * A_mat[4, 2]) + (P_cov[3, 3] * A_mat[4, 3]) + (P_cov[3, 4] * A_mat[4, 4]) + (P_cov[3, 5] * A_mat[4, 5]) + (P_cov[3, 6] * A_mat[4, 6])
));
r_TmpSum := r_TmpSum + (A_mat[5, 4] * (
    (P_cov[4, 1] * A_mat[4, 1]) + (P_cov[4, 2] * A_mat[4, 2]) + (P_cov[4, 3] * A_mat[4, 3]) + (P_cov[4, 4] * A_mat[4, 4]) + (P_cov[4, 5] * A_mat[4, 5]) + (P_cov[4, 6] * A_mat[4, 6])
));
r_TmpSum := r_TmpSum + (A_mat[5, 5] * (
    (P_cov[5, 1] * A_mat[4, 1]) + (P_cov[5, 2] * A_mat[4, 2]) + (P_cov[5, 3] * A_mat[4, 3]) + (P_cov[5, 4] * A_mat[4, 4]) + (P_cov[5, 5] * A_mat[4, 5]) + (P_cov[5, 6] * A_mat[4, 6])
));
r_TmpSum := r_TmpSum + (A_mat[5, 6] * (
    (P_cov[6, 1] * A_mat[4, 1]) + (P_cov[6, 2] * A_mat[4, 2]) + (P_cov[6, 3] * A_mat[4, 3]) + (P_cov[6, 4] * A_mat[4, 4]) + (P_cov[6, 5] * A_mat[4, 5]) + (P_cov[6, 6] * A_mat[4, 6])
));
P_cov[5, 4] := r_TmpSum;
(* Element P_pred[5, 5] *)
r_TmpSum := 0.0;
r_TmpSum := r_TmpSum + (A_mat[5, 1] * (
    (P_cov[1, 1] * A_mat[5, 1]) + (P_cov[1, 2] * A_mat[5, 2]) + (P_cov[1, 3] * A_mat[5, 3]) + (P_cov[1, 4] * A_mat[5, 4]) + (P_cov[1, 5] * A_mat[5, 5]) + (P_cov[1, 6] * A_mat[5, 6])
));
r_TmpSum := r_TmpSum + (A_mat[5, 2] * (
    (P_cov[2, 1] * A_mat[5, 1]) + (P_cov[2, 2] * A_mat[5, 2]) + (P_cov[2, 3] * A_mat[5, 3]) + (P_cov[2, 4] * A_mat[5, 4]) + (P_cov[2, 5] * A_mat[5, 5]) + (P_cov[2, 6] * A_mat[5, 6])
));
r_TmpSum := r_TmpSum + (A_mat[5, 3] * (
    (P_cov[3, 1] * A_mat[5, 1]) + (P_cov[3, 2] * A_mat[5, 2]) + (P_cov[3, 3] * A_mat[5, 3]) + (P_cov[3, 4] * A_mat[5, 4]) + (P_cov[3, 5] * A_mat[5, 5]) + (P_cov[3, 6] * A_mat[5, 6])
));
r_TmpSum := r_TmpSum + (A_mat[5, 4] * (
    (P_cov[4, 1] * A_mat[5, 1]) + (P_cov[4, 2] * A_mat[5, 2]) + (P_cov[4, 3] * A_mat[5, 3]) + (P_cov[4, 4] * A_mat[5, 4]) + (P_cov[4, 5] * A_mat[5, 5]) + (P_cov[4, 6] * A_mat[5, 6])
));
r_TmpSum := r_TmpSum + (A_mat[5, 5] * (
    (P_cov[5, 1] * A_mat[5, 1]) + (P_cov[5, 2] * A_mat[5, 2]) + (P_cov[5, 3] * A_mat[5, 3]) + (P_cov[5, 4] * A_mat[5, 4]) + (P_cov[5, 5] * A_mat[5, 5]) + (P_cov[5, 6] * A_mat[5, 6])
));
r_TmpSum := r_TmpSum + (A_mat[5, 6] * (
    (P_cov[6, 1] * A_mat[5, 1]) + (P_cov[6, 2] * A_mat[5, 2]) + (P_cov[6, 3] * A_mat[5, 3]) + (P_cov[6, 4] * A_mat[5, 4]) + (P_cov[6, 5] * A_mat[5, 5]) + (P_cov[6, 6] * A_mat[5, 6])
));
P_cov[5, 5] := r_TmpSum + Q_obs_diag[5];
(* Element P_pred[5, 6] *)
r_TmpSum := 0.0;
r_TmpSum := r_TmpSum + (A_mat[5, 1] * (
    (P_cov[1, 1] * A_mat[6, 1]) + (P_cov[1, 2] * A_mat[6, 2]) + (P_cov[1, 3] * A_mat[6, 3]) + (P_cov[1, 4] * A_mat[6, 4]) + (P_cov[1, 5] * A_mat[6, 5]) + (P_cov[1, 6] * A_mat[6, 6])
));
r_TmpSum := r_TmpSum + (A_mat[5, 2] * (
    (P_cov[2, 1] * A_mat[6, 1]) + (P_cov[2, 2] * A_mat[6, 2]) + (P_cov[2, 3] * A_mat[6, 3]) + (P_cov[2, 4] * A_mat[6, 4]) + (P_cov[2, 5] * A_mat[6, 5]) + (P_cov[2, 6] * A_mat[6, 6])
));
r_TmpSum := r_TmpSum + (A_mat[5, 3] * (
    (P_cov[3, 1] * A_mat[6, 1]) + (P_cov[3, 2] * A_mat[6, 2]) + (P_cov[3, 3] * A_mat[6, 3]) + (P_cov[3, 4] * A_mat[6, 4]) + (P_cov[3, 5] * A_mat[6, 5]) + (P_cov[3, 6] * A_mat[6, 6])
));
r_TmpSum := r_TmpSum + (A_mat[5, 4] * (
    (P_cov[4, 1] * A_mat[6, 1]) + (P_cov[4, 2] * A_mat[6, 2]) + (P_cov[4, 3] * A_mat[6, 3]) + (P_cov[4, 4] * A_mat[6, 4]) + (P_cov[4, 5] * A_mat[6, 5]) + (P_cov[4, 6] * A_mat[6, 6])
));
r_TmpSum := r_TmpSum + (A_mat[5, 5] * (
    (P_cov[5, 1] * A_mat[6, 1]) + (P_cov[5, 2] * A_mat[6, 2]) + (P_cov[5, 3] * A_mat[6, 3]) + (P_cov[5, 4] * A_mat[6, 4]) + (P_cov[5, 5] * A_mat[6, 5]) + (P_cov[5, 6] * A_mat[6, 6])
));
r_TmpSum := r_TmpSum + (A_mat[5, 6] * (
    (P_cov[6, 1] * A_mat[6, 1]) + (P_cov[6, 2] * A_mat[6, 2]) + (P_cov[6, 3] * A_mat[6, 3]) + (P_cov[6, 4] * A_mat[6, 4]) + (P_cov[6, 5] * A_mat[6, 5]) + (P_cov[6, 6] * A_mat[6, 6])
));
P_cov[5, 6] := r_TmpSum;
(* Element P_pred[6, 1] *)
r_TmpSum := 0.0;
r_TmpSum := r_TmpSum + (A_mat[6, 1] * (
    (P_cov[1, 1] * A_mat[1, 1]) + (P_cov[1, 2] * A_mat[1, 2]) + (P_cov[1, 3] * A_mat[1, 3]) + (P_cov[1, 4] * A_mat[1, 4]) + (P_cov[1, 5] * A_mat[1, 5]) + (P_cov[1, 6] * A_mat[1, 6])
));
r_TmpSum := r_TmpSum + (A_mat[6, 2] * (
    (P_cov[2, 1] * A_mat[1, 1]) + (P_cov[2, 2] * A_mat[1, 2]) + (P_cov[2, 3] * A_mat[1, 3]) + (P_cov[2, 4] * A_mat[1, 4]) + (P_cov[2, 5] * A_mat[1, 5]) + (P_cov[2, 6] * A_mat[1, 6])
));
r_TmpSum := r_TmpSum + (A_mat[6, 3] * (
    (P_cov[3, 1] * A_mat[1, 1]) + (P_cov[3, 2] * A_mat[1, 2]) + (P_cov[3, 3] * A_mat[1, 3]) + (P_cov[3, 4] * A_mat[1, 4]) + (P_cov[3, 5] * A_mat[1, 5]) + (P_cov[3, 6] * A_mat[1, 6])
));
r_TmpSum := r_TmpSum + (A_mat[6, 4] * (
    (P_cov[4, 1] * A_mat[1, 1]) + (P_cov[4, 2] * A_mat[1, 2]) + (P_cov[4, 3] * A_mat[1, 3]) + (P_cov[4, 4] * A_mat[1, 4]) + (P_cov[4, 5] * A_mat[1, 5]) + (P_cov[4, 6] * A_mat[1, 6])
));
r_TmpSum := r_TmpSum + (A_mat[6, 5] * (
    (P_cov[5, 1] * A_mat[1, 1]) + (P_cov[5, 2] * A_mat[1, 2]) + (P_cov[5, 3] * A_mat[1, 3]) + (P_cov[5, 4] * A_mat[1, 4]) + (P_cov[5, 5] * A_mat[1, 5]) + (P_cov[5, 6] * A_mat[1, 6])
));
r_TmpSum := r_TmpSum + (A_mat[6, 6] * (
    (P_cov[6, 1] * A_mat[1, 1]) + (P_cov[6, 2] * A_mat[1, 2]) + (P_cov[6, 3] * A_mat[1, 3]) + (P_cov[6, 4] * A_mat[1, 4]) + (P_cov[6, 5] * A_mat[1, 5]) + (P_cov[6, 6] * A_mat[1, 6])
));
P_cov[6, 1] := r_TmpSum;
(* Element P_pred[6, 2] *)
r_TmpSum := 0.0;
r_TmpSum := r_TmpSum + (A_mat[6, 1] * (
    (P_cov[1, 1] * A_mat[2, 1]) + (P_cov[1, 2] * A_mat[2, 2]) + (P_cov[1, 3] * A_mat[2, 3]) + (P_cov[1, 4] * A_mat[2, 4]) + (P_cov[1, 5] * A_mat[2, 5]) + (P_cov[1, 6] * A_mat[2, 6])
));
r_TmpSum := r_TmpSum + (A_mat[6, 2] * (
    (P_cov[2, 1] * A_mat[2, 1]) + (P_cov[2, 2] * A_mat[2, 2]) + (P_cov[2, 3] * A_mat[2, 3]) + (P_cov[2, 4] * A_mat[2, 4]) + (P_cov[2, 5] * A_mat[2, 5]) + (P_cov[2, 6] * A_mat[2, 6])
));
r_TmpSum := r_TmpSum + (A_mat[6, 3] * (
    (P_cov[3, 1] * A_mat[2, 1]) + (P_cov[3, 2] * A_mat[2, 2]) + (P_cov[3, 3] * A_mat[2, 3]) + (P_cov[3, 4] * A_mat[2, 4]) + (P_cov[3, 5] * A_mat[2, 5]) + (P_cov[3, 6] * A_mat[2, 6])
));
r_TmpSum := r_TmpSum + (A_mat[6, 4] * (
    (P_cov[4, 1] * A_mat[2, 1]) + (P_cov[4, 2] * A_mat[2, 2]) + (P_cov[4, 3] * A_mat[2, 3]) + (P_cov[4, 4] * A_mat[2, 4]) + (P_cov[4, 5] * A_mat[2, 5]) + (P_cov[4, 6] * A_mat[2, 6])
));
r_TmpSum := r_TmpSum + (A_mat[6, 5] * (
    (P_cov[5, 1] * A_mat[2, 1]) + (P_cov[5, 2] * A_mat[2, 2]) + (P_cov[5, 3] * A_mat[2, 3]) + (P_cov[5, 4] * A_mat[2, 4]) + (P_cov[5, 5] * A_mat[2, 5]) + (P_cov[5, 6] * A_mat[2, 6])
));
r_TmpSum := r_TmpSum + (A_mat[6, 6] * (
    (P_cov[6, 1] * A_mat[2, 1]) + (P_cov[6, 2] * A_mat[2, 2]) + (P_cov[6, 3] * A_mat[2, 3]) + (P_cov[6, 4] * A_mat[2, 4]) + (P_cov[6, 5] * A_mat[2, 5]) + (P_cov[6, 6] * A_mat[2, 6])
));
P_cov[6, 2] := r_TmpSum;
(* Element P_pred[6, 3] *)
r_TmpSum := 0.0;
r_TmpSum := r_TmpSum + (A_mat[6, 1] * (
    (P_cov[1, 1] * A_mat[3, 1]) + (P_cov[1, 2] * A_mat[3, 2]) + (P_cov[1, 3] * A_mat[3, 3]) + (P_cov[1, 4] * A_mat[3, 4]) + (P_cov[1, 5] * A_mat[3, 5]) + (P_cov[1, 6] * A_mat[3, 6])
));
r_TmpSum := r_TmpSum + (A_mat[6, 2] * (
    (P_cov[2, 1] * A_mat[3, 1]) + (P_cov[2, 2] * A_mat[3, 2]) + (P_cov[2, 3] * A_mat[3, 3]) + (P_cov[2, 4] * A_mat[3, 4]) + (P_cov[2, 5] * A_mat[3, 5]) + (P_cov[2, 6] * A_mat[3, 6])
));
r_TmpSum := r_TmpSum + (A_mat[6, 3] * (
    (P_cov[3, 1] * A_mat[3, 1]) + (P_cov[3, 2] * A_mat[3, 2]) + (P_cov[3, 3] * A_mat[3, 3]) + (P_cov[3, 4] * A_mat[3, 4]) + (P_cov[3, 5] * A_mat[3, 5]) + (P_cov[3, 6] * A_mat[3, 6])
));
r_TmpSum := r_TmpSum + (A_mat[6, 4] * (
    (P_cov[4, 1] * A_mat[3, 1]) + (P_cov[4, 2] * A_mat[3, 2]) + (P_cov[4, 3] * A_mat[3, 3]) + (P_cov[4, 4] * A_mat[3, 4]) + (P_cov[4, 5] * A_mat[3, 5]) + (P_cov[4, 6] * A_mat[3, 6])
));
r_TmpSum := r_TmpSum + (A_mat[6, 5] * (
    (P_cov[5, 1] * A_mat[3, 1]) + (P_cov[5, 2] * A_mat[3, 2]) + (P_cov[5, 3] * A_mat[3, 3]) + (P_cov[5, 4] * A_mat[3, 4]) + (P_cov[5, 5] * A_mat[3, 5]) + (P_cov[5, 6] * A_mat[3, 6])
));
r_TmpSum := r_TmpSum + (A_mat[6, 6] * (
    (P_cov[6, 1] * A_mat[3, 1]) + (P_cov[6, 2] * A_mat[3, 2]) + (P_cov[6, 3] * A_mat[3, 3]) + (P_cov[6, 4] * A_mat[3, 4]) + (P_cov[6, 5] * A_mat[3, 5]) + (P_cov[6, 6] * A_mat[3, 6])
));
P_cov[6, 3] := r_TmpSum;
(* Element P_pred[6, 4] *)
r_TmpSum := 0.0;
r_TmpSum := r_TmpSum + (A_mat[6, 1] * (
    (P_cov[1, 1] * A_mat[4, 1]) + (P_cov[1, 2] * A_mat[4, 2]) + (P_cov[1, 3] * A_mat[4, 3]) + (P_cov[1, 4] * A_mat[4, 4]) + (P_cov[1, 5] * A_mat[4, 5]) + (P_cov[1, 6] * A_mat[4, 6])
));
r_TmpSum := r_TmpSum + (A_mat[6, 2] * (
    (P_cov[2, 1] * A_mat[4, 1]) + (P_cov[2, 2] * A_mat[4, 2]) + (P_cov[2, 3] * A_mat[4, 3]) + (P_cov[2, 4] * A_mat[4, 4]) + (P_cov[2, 5] * A_mat[4, 5]) + (P_cov[2, 6] * A_mat[4, 6])
));
r_TmpSum := r_TmpSum + (A_mat[6, 3] * (
    (P_cov[3, 1] * A_mat[4, 1]) + (P_cov[3, 2] * A_mat[4, 2]) + (P_cov[3, 3] * A_mat[4, 3]) + (P_cov[3, 4] * A_mat[4, 4]) + (P_cov[3, 5] * A_mat[4, 5]) + (P_cov[3, 6] * A_mat[4, 6])
));
r_TmpSum := r_TmpSum + (A_mat[6, 4] * (
    (P_cov[4, 1] * A_mat[4, 1]) + (P_cov[4, 2] * A_mat[4, 2]) + (P_cov[4, 3] * A_mat[4, 3]) + (P_cov[4, 4] * A_mat[4, 4]) + (P_cov[4, 5] * A_mat[4, 5]) + (P_cov[4, 6] * A_mat[4, 6])
));
r_TmpSum := r_TmpSum + (A_mat[6, 5] * (
    (P_cov[5, 1] * A_mat[4, 1]) + (P_cov[5, 2] * A_mat[4, 2]) + (P_cov[5, 3] * A_mat[4, 3]) + (P_cov[5, 4] * A_mat[4, 4]) + (P_cov[5, 5] * A_mat[4, 5]) + (P_cov[5, 6] * A_mat[4, 6])
));
r_TmpSum := r_TmpSum + (A_mat[6, 6] * (
    (P_cov[6, 1] * A_mat[4, 1]) + (P_cov[6, 2] * A_mat[4, 2]) + (P_cov[6, 3] * A_mat[4, 3]) + (P_cov[6, 4] * A_mat[4, 4]) + (P_cov[6, 5] * A_mat[4, 5]) + (P_cov[6, 6] * A_mat[4, 6])
));
P_cov[6, 4] := r_TmpSum;
(* Element P_pred[6, 5] *)
r_TmpSum := 0.0;
r_TmpSum := r_TmpSum + (A_mat[6, 1] * (
    (P_cov[1, 1] * A_mat[5, 1]) + (P_cov[1, 2] * A_mat[5, 2]) + (P_cov[1, 3] * A_mat[5, 3]) + (P_cov[1, 4] * A_mat[5, 4]) + (P_cov[1, 5] * A_mat[5, 5]) + (P_cov[1, 6] * A_mat[5, 6])
));
r_TmpSum := r_TmpSum + (A_mat[6, 2] * (
    (P_cov[2, 1] * A_mat[5, 1]) + (P_cov[2, 2] * A_mat[5, 2]) + (P_cov[2, 3] * A_mat[5, 3]) + (P_cov[2, 4] * A_mat[5, 4]) + (P_cov[2, 5] * A_mat[5, 5]) + (P_cov[2, 6] * A_mat[5, 6])
));
r_TmpSum := r_TmpSum + (A_mat[6, 3] * (
    (P_cov[3, 1] * A_mat[5, 1]) + (P_cov[3, 2] * A_mat[5, 2]) + (P_cov[3, 3] * A_mat[5, 3]) + (P_cov[3, 4] * A_mat[5, 4]) + (P_cov[3, 5] * A_mat[5, 5]) + (P_cov[3, 6] * A_mat[5, 6])
));
r_TmpSum := r_TmpSum + (A_mat[6, 4] * (
    (P_cov[4, 1] * A_mat[5, 1]) + (P_cov[4, 2] * A_mat[5, 2]) + (P_cov[4, 3] * A_mat[5, 3]) + (P_cov[4, 4] * A_mat[5, 4]) + (P_cov[4, 5] * A_mat[5, 5]) + (P_cov[4, 6] * A_mat[5, 6])
));
r_TmpSum := r_TmpSum + (A_mat[6, 5] * (
    (P_cov[5, 1] * A_mat[5, 1]) + (P_cov[5, 2] * A_mat[5, 2]) + (P_cov[5, 3] * A_mat[5, 3]) + (P_cov[5, 4] * A_mat[5, 4]) + (P_cov[5, 5] * A_mat[5, 5]) + (P_cov[5, 6] * A_mat[5, 6])
));
r_TmpSum := r_TmpSum + (A_mat[6, 6] * (
    (P_cov[6, 1] * A_mat[5, 1]) + (P_cov[6, 2] * A_mat[5, 2]) + (P_cov[6, 3] * A_mat[5, 3]) + (P_cov[6, 4] * A_mat[5, 4]) + (P_cov[6, 5] * A_mat[5, 5]) + (P_cov[6, 6] * A_mat[5, 6])
));
P_cov[6, 5] := r_TmpSum;
(* Element P_pred[6, 6] *)
r_TmpSum := 0.0;
r_TmpSum := r_TmpSum + (A_mat[6, 1] * (
    (P_cov[1, 1] * A_mat[6, 1]) + (P_cov[1, 2] * A_mat[6, 2]) + (P_cov[1, 3] * A_mat[6, 3]) + (P_cov[1, 4] * A_mat[6, 4]) + (P_cov[1, 5] * A_mat[6, 5]) + (P_cov[1, 6] * A_mat[6, 6])
));
r_TmpSum := r_TmpSum + (A_mat[6, 2] * (
    (P_cov[2, 1] * A_mat[6, 1]) + (P_cov[2, 2] * A_mat[6, 2]) + (P_cov[2, 3] * A_mat[6, 3]) + (P_cov[2, 4] * A_mat[6, 4]) + (P_cov[2, 5] * A_mat[6, 5]) + (P_cov[2, 6] * A_mat[6, 6])
));
r_TmpSum := r_TmpSum + (A_mat[6, 3] * (
    (P_cov[3, 1] * A_mat[6, 1]) + (P_cov[3, 2] * A_mat[6, 2]) + (P_cov[3, 3] * A_mat[6, 3]) + (P_cov[3, 4] * A_mat[6, 4]) + (P_cov[3, 5] * A_mat[6, 5]) + (P_cov[3, 6] * A_mat[6, 6])
));
r_TmpSum := r_TmpSum + (A_mat[6, 4] * (
    (P_cov[4, 1] * A_mat[6, 1]) + (P_cov[4, 2] * A_mat[6, 2]) + (P_cov[4, 3] * A_mat[6, 3]) + (P_cov[4, 4] * A_mat[6, 4]) + (P_cov[4, 5] * A_mat[6, 5]) + (P_cov[4, 6] * A_mat[6, 6])
));
r_TmpSum := r_TmpSum + (A_mat[6, 5] * (
    (P_cov[5, 1] * A_mat[6, 1]) + (P_cov[5, 2] * A_mat[6, 2]) + (P_cov[5, 3] * A_mat[6, 3]) + (P_cov[5, 4] * A_mat[6, 4]) + (P_cov[5, 5] * A_mat[6, 5]) + (P_cov[5, 6] * A_mat[6, 6])
));
r_TmpSum := r_TmpSum + (A_mat[6, 6] * (
    (P_cov[6, 1] * A_mat[6, 1]) + (P_cov[6, 2] * A_mat[6, 2]) + (P_cov[6, 3] * A_mat[6, 3]) + (P_cov[6, 4] * A_mat[6, 4]) + (P_cov[6, 5] * A_mat[6, 5]) + (P_cov[6, 6] * A_mat[6, 6])
));
P_cov[6, 6] := r_TmpSum + Q_obs_diag[6];

(* Assign Observer Output Interface Variables *)
r_Obs_RamPosition_mm := x_est[1];
r_Obs_RamVelocity_mm_s := x_est[2];
r_Obs_DieInterfaceTemp_DegC := x_est[5];
r_Obs_CornerTiltDeviation_um := x_est[6];
