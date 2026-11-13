# cz_silicon_builder/mod_cyberphysical.py
# -*- coding: utf-8 -*-

def generate_cyberphysical():
    return """(* ==========================================================================================
   PHASE 2: FIRST-PRINCIPLES CYBER-PHYSICAL STATE-SPACE ESTIMATION & THERMODYNAMICS
   ==========================================================================================
   Governs:
     1. Stefan Boundary Solid-Liquid Interface Dynamics:
        k_s * (dT_s/dz) - k_l * (dT_l/dz) = rho_s * L_f * v_growth
     2. Capillary Meniscus Laplace-Young Equilibrium:
        h_m = SQRT( 2 * gamma_m / (rho_l * g) * (1 - SIN(theta_c)) )
     3. Electromagnetic Cusp Field Lorentz Damping:
        F_Lorentz = sigma_e * (v x B) x B
     4. Voronkov Point Defect Incorporation Criterion (v / G_0):
        xi = v_pull / G_0, Target Window: 0.200 to 0.240 mm2 / (min * K)
     5. Continuous Mass Continuity & Crucible Lift Kinematics
     6. Full 6x6 Discrete Luenberger Observer Innovation:
        x_hat[k+1] = A * x_hat[k] + B * u[k] + L * (y[k] - C * x_hat[k])
   ========================================================================================== *)

(* ------------------------------------------------------------------------------------------
   1. SENSOR MEASUREMENT PACKAGING FOR STATE-SPACE OBSERVER
   ------------------------------------------------------------------------------------------ *)
(* Measurement y1: Voted Meniscus Pyrometer Temperature [deg C] *)
y_meas[1] := rVotedMeniscusTemp;

(* Measurement y2: Voted High-Speed CCD Camera Diameter [mm] *)
y_meas[2] := rVotedIngotDiameter;

(* Measurement y3: Load Cell Dynamic Weight-Rate Inferred Diameter [mm]
   dM/dt = rho_s * Pi * (D_c / 2)^2 * v_pull
   D_c = 2 * SQRT( (dM/dt) / (rho_s * Pi * v_pull) ) *)
IF (rCrystalPullSpeedActual > 0.20) AND (rTotalProcessElapsedTime > 5.0) THEN
    (* Differential weight change per hour converted to kg/s *)
    rCrystalWeightRate_kg_hr := (rVotedCrystalWeight - rLastCrystalWeightSample) / (rCycleTimeSec / 3600.0);
    IF rCrystalWeightRate_kg_hr > 0.05 THEN
        (* D_equiv = 2 * SQRT( (rCrystalWeightRate_kg_hr / 3600.0) / (rho_s_solid * PI_VAL * (rCrystalPullSpeedActual / 60000.0)) ) * 1000.0 *)
        y_meas[3] := 2000.0 * SQRT( (rCrystalWeightRate_kg_hr / 3600.0) / (rho_s_solid * PI_VAL * (rCrystalPullSpeedActual / 60000.0) + 1.0E-9) );
    ELSE
        y_meas[3] := rVotedIngotDiameter;
    END_IF;
ELSE
    y_meas[3] := rVotedIngotDiameter;
    rCrystalWeightRate_kg_hr := 0.0;
END_IF;
rLastCrystalWeightSample := rVotedCrystalWeight;

(* Measurement y4: Voted Main Graphite Heater Temperature [deg C] *)
y_meas[4] := rVotedHeaterTemp;

(* Measurement y5: Molten Melt Convection Fluctuation Intensity [mm/s]
   Derived from optical pyrometer high-frequency thermal variance and cusp magnetic field *)
IF rCuspCoilCurrentActual > 10.0 THEN
    rLorentzDampingFactor := 1.0 / (1.0 + 0.0085 * rCuspCoilCurrentActual);
ELSE
    rLorentzDampingFactor := 1.0;
END_IF;
rBulkConvectionVelocity_RMS := (ABS(rPyrometer_Meniscus_ChA - rPyrometer_Meniscus_ChB) * 0.45 + 0.35) * rLorentzDampingFactor;
y_meas[5] := rBulkConvectionVelocity_RMS;

(* Measurement y6: Actual Crystal Pull Servo Encoder Speed [mm/min] *)
y_meas[6] := rCrystalPullSpeedActual;


(* ------------------------------------------------------------------------------------------
   2. STEFAN BOUNDARY SOLID-LIQUID SOLIDIFICATION RATE CALCULATION
   ------------------------------------------------------------------------------------------
   Stefan Energy Conservation:
     k_s * G_s - k_l * G_l = rho_s * L_f * v_growth
     v_growth = (k_s * G_s - k_l * G_l) / (rho_s * L_f)
   where:
     G_s = x_hat[3] (Solid crystal interface axial thermal gradient [K/mm]) -> * 1000.0 [K/m]
     G_l = rLiquidThermalGradient_Gl (Liquid melt thermal gradient near interface [K/mm]) -> * 1000.0 [K/m]
     k_s = 22.0 W/(m*K), k_l = 64.0 W/(m*K), rho_s = 2,330 kg/m3, L_f = 1.80e6 J/kg
   ------------------------------------------------------------------------------------------ *)
IF x_hat[3] > 0.50 THEN
    rInterfaceAxialGradient_G0 := x_hat[3];
ELSE
    rInterfaceAxialGradient_G0 := 3.45; (* Nominal default G_0 *)
END_IF;

(* Compute instantaneous solidification velocity [m/s] *)
rStefanPullRate_calc := ((k_s_solid * (rInterfaceAxialGradient_G0 * 1000.0)) - (k_l_liquid * (rLiquidThermalGradient_Gl * 1000.0)))
                        / (rho_s_solid * L_f_latent + 1.0E-9);

(* Convert [m/s] to [mm/min]: * 1000.0 mm/m * 60.0 s/min = * 60000.0 *)
rStefanPullRate_calc := rStefanPullRate_calc * 60000.0;

(* Bound calculated growth rate within physical crystal pull limits *)
IF rStefanPullRate_calc < 0.0 THEN
    rStefanPullRate_calc := 0.0;
ELSIF rStefanPullRate_calc > 16.0 THEN
    rStefanPullRate_calc := 16.0;
END_IF;
rEstimatedGrowthRate := rStefanPullRate_calc;


(* ------------------------------------------------------------------------------------------
   3. CAPILLARY MENISCUS HEIGHT & DYNAMIC CONTACT ANGLE (LAPLACE-YOUNG)
   ------------------------------------------------------------------------------------------
   h_m = SQRT( 2.0 * gamma_m / (rho_l * g) * (1.0 - SIN(theta_c)) )
   Capillary Constant: a = SQRT( 2.0 * gamma_m / (rho_l * g) ) = 7.56 mm
   Dynamic contact angle shifts with diameter tracking error:
     theta_c = theta_c_steady + K_theta * (rVotedIngotDiameter - rTargetIngotDiameter)
   ------------------------------------------------------------------------------------------ *)
rCalculatedContactAngle := theta_c_steady_deg + 1.25 * (rVotedIngotDiameter - rTargetIngotDiameter);
IF rCalculatedContactAngle < 2.0 THEN
    rCalculatedContactAngle := 2.0;
ELSIF rCalculatedContactAngle > 35.0 THEN
    rCalculatedContactAngle := 35.0;
END_IF;

(* Laplace-Young meniscus height [mm] *)
rMeniscusHeight_calc := rCapillaryConstant_mm * SQRT( ABS(1.0 - SIN(rCalculatedContactAngle * PI_VAL / 180.0)) );


(* ------------------------------------------------------------------------------------------
   4. VORONKOV POINT DEFECT (v / G_0) CRITERION EVALUATION
   ------------------------------------------------------------------------------------------
   xi = v_pull / G_0  [mm2 / (min * K)]
   Controls whether crystal grows vacancy-rich (COPs) or interstitial-rich (A-swirl loops).
   ------------------------------------------------------------------------------------------ *)
IF rInterfaceAxialGradient_G0 > 0.10 THEN
    rCurrentVoronkovRatio := rCrystalPullSpeedActual / rInterfaceAxialGradient_G0;
ELSE
    rCurrentVoronkovRatio := 0.0;
END_IF;

IF (rCurrentVoronkovRatio >= xi_window_min) AND (rCurrentVoronkovRatio <= xi_window_max) THEN
    bVoronkovCriterionSatisfied := TRUE;
ELSE
    bVoronkovCriterionSatisfied := FALSE;
END_IF;


(* ------------------------------------------------------------------------------------------
   5. MASS BALANCE & CRUCIBLE LIFT KINEMATICS
   ------------------------------------------------------------------------------------------
   As the cylindrical ingot is pulled upward, the melt level in the crucible drops:
     A_crystal = Pi * (D_voted / 2)^2
     A_crucible = Pi * R_crucible^2
     v_drop = v_pull * (rho_s / rho_l) * (A_crystal / (A_crucible - A_crystal))
   Crucible lift speed:
     v_crucible = v_drop + K_trim * (MeltLevelError)
   ------------------------------------------------------------------------------------------ *)
IF (rCrucibleCrossArea_mm2 > (PI_VAL * (rVotedIngotDiameter * 0.50) * (rVotedIngotDiameter * 0.50)))
   AND (rVotedIngotDiameter > 10.0) THEN
    rCrucibleMeltDropRate := rCrystalPullSpeedActual * (rho_s_solid / rho_l_liquid)
                             * ((PI_VAL * (rVotedIngotDiameter * 0.50) * (rVotedIngotDiameter * 0.50))
                             / (rCrucibleCrossArea_mm2 - (PI_VAL * (rVotedIngotDiameter * 0.50) * (rVotedIngotDiameter * 0.50))));
ELSE
    rCrucibleMeltDropRate := 0.0;
END_IF;

rCrucibleLiftKinematicSpeed := rCrucibleMeltDropRate;

(* Update accumulated ingot length and remaining melt mass *)
IF rCrystalPullSpeedActual > 0.01 THEN
    rTotalIngotLength_mm := rTotalIngotLength_mm + (rCrystalPullSpeedActual * (rCycleTimeSec / 60.0));
    rSiliconMeltMassRemaining_kg := rSiliconMeltMassRemaining_kg
                                    - (rho_s_solid * PI_VAL * (rVotedIngotDiameter * 0.0005) * (rVotedIngotDiameter * 0.0005)
                                    * (rCrystalPullSpeedActual * (rCycleTimeSec / 60000.0)));
    IF rSiliconMeltMassRemaining_kg < 0.0 THEN
        rSiliconMeltMassRemaining_kg := 0.0;
    END_IF;
END_IF;

rAccumulatedIngotLength := rTotalIngotLength_mm;
rResidualMeltMass := rSiliconMeltMassRemaining_kg;


(* ------------------------------------------------------------------------------------------
   6. LUENBERGER STATE OBSERVER INNOVATION PROPAGATION (6x6)
   ------------------------------------------------------------------------------------------
   Predict:
     y_est = C * x_hat + D * u_cmd
   Innovation:
     y_innov = y_meas - y_est
   Update:
     x_hat_next = A * x_hat + B * u_cmd + L * y_innov
   ------------------------------------------------------------------------------------------ *)
(* Step A: Measurement estimation (y_est = C * x_hat + D * u_cmd) *)
FOR iLoopIndex := 1 TO 6 DO
    y_est[iLoopIndex] := 0.0;
    FOR jLoopIndex := 1 TO 6 DO
        y_est[iLoopIndex] := y_est[iLoopIndex] + (C_mat[iLoopIndex, jLoopIndex] * x_hat[jLoopIndex]);
    END_FOR;
    FOR kLoopIndex := 1 TO 5 DO
        y_est[iLoopIndex] := y_est[iLoopIndex] + (D_mat[iLoopIndex, kLoopIndex] * u_cmd[kLoopIndex]);
    END_FOR;
    y_innov[iLoopIndex] := y_meas[iLoopIndex] - y_est[iLoopIndex];
END_FOR;

(* Step B: Next State Estimation Propagation (x_hat_next = A * x_hat + B * u_cmd + L * y_innov) *)
FOR iLoopIndex := 1 TO 6 DO
    x_hat_next[iLoopIndex] := 0.0;
    (* State transition term: A * x_hat *)
    FOR jLoopIndex := 1 TO 6 DO
        x_hat_next[iLoopIndex] := x_hat_next[iLoopIndex] + (A_mat[iLoopIndex, jLoopIndex] * x_hat[jLoopIndex]);
    END_FOR;
    (* Control input term: B * u_cmd *)
    FOR kLoopIndex := 1 TO 5 DO
        x_hat_next[iLoopIndex] := x_hat_next[iLoopIndex] + (B_mat[iLoopIndex, kLoopIndex] * u_cmd[kLoopIndex]);
    END_FOR;
    (* Innovation correction term: L * y_innov *)
    FOR jLoopIndex := 1 TO 6 DO
        x_hat_next[iLoopIndex] := x_hat_next[iLoopIndex] + (L_mat[iLoopIndex, jLoopIndex] * y_innov[jLoopIndex]);
    END_FOR;
END_FOR;

(* Step C: Copy updated observer estimates into active state vector *)
FOR iLoopIndex := 1 TO 6 DO
    x_hat[iLoopIndex] := x_hat_next[iLoopIndex];
    x_err[iLoopIndex] := x_hat[iLoopIndex] - x_ref[iLoopIndex];
END_FOR;"""
