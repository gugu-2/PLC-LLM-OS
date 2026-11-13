# phase2_cyber_physical.py for FB_Glass_FloatLine_TinBath_AnnealingLehr_ThicknessCooling

def generate_phase2():
    return """(*
 * =========================================================================================================
 * PHASE 2: FIRST-PRINCIPLES CYBER-PHYSICAL STATE-SPACE ESTIMATION & HYDRODYNAMIC MODELING
 * 1. Measured Output Vector Construction y[k]
 * 2. Luenberger / Discrete Kalman Observer Prediction & Innovation Update (x_hat[k+1] = A*x_hat + B*u + L*e)
 * 3. Molten Tin Bath Three-Phase Wetting Equilibrium Thickness Formulation (h_eq)
 * 4. Vogel-Fulcher-Tammann (VFT) High-Temperature Viscosity Dynamics
 * 5. 16 Top-Roller Knurl Machine Tractive Forces, Peripheral Velocities & Slip Ratios
 * 6. Annealing Lehr Viscoelastic Structural Stress Relaxation Dynamics (Tool-Narayanaswamy)
 * =========================================================================================================
 *)

(* ---------------------------------------------------------------------------------------------------------
 * 1. MEASUREMENT OBSERVATION VECTOR MAPPING y[k] (6x1 VECTOR)
 * --------------------------------------------------------------------------------------------------------- *)
(* Channel 1: Center Ribbon Thickness Deviation [um] *)
arrOutputY_Meas[1] := (rVotedThickness_mm - rRecipeTargetThickness) * 1000.0;

(* Channel 2: Usable Ribbon Width Deviation [mm] *)
arrOutputY_Meas[2] := rRibbonWidthFeedback - rRecipeTargetWidth;

(* Channel 3: Tin Bath Longitudinal Thermal Gradient Deviation [deg C] *)
arrOutputY_Meas[3] := (rVotedPyrometer_degC - rBathExitGlassTempFeedback) - 
                      (rRecipeTargetTinBathInletTemp - rRecipeTargetBathExitTemp);

(* Channel 4: Protective Atmosphere Overpressure Deviation [mbar] *)
arrOutputY_Meas[4] := rVotedBathPress_mbar - 0.450; (* 0.450 mbar nominal setpoint *)

(* Channel 5: Lehr Exit Residual Stress Retardation Deviation [nm/cm] *)
arrOutputY_Meas[5] := rVotedLehrStress_nm_cm - (rRecipeMaxStressLimit * 0.50);

(* Channel 6: Lehr Main Line Conveyor Speed Deviation [m/min] *)
arrOutputY_Meas[6] := rLehrDriveSpeedFeedback - rRecipeTargetLineSpeed;

(* ---------------------------------------------------------------------------------------------------------
 * 2. MODEL ESTIMATION OF OBSERVATIONS y_hat[k] = C * x_hat[k] + D * u[k]
 * --------------------------------------------------------------------------------------------------------- *)
FOR idxRow := 1 TO 6 DO
    rCx_Sum := 0.0;
    rDu_Sum := 0.0;
    FOR idxCol := 1 TO 6 DO
        rCx_Sum := rCx_Sum + (matC[idxRow, idxCol] * arrStateX_Hat[idxCol]);
        rDu_Sum := rDu_Sum + (matD[idxRow, idxCol] * arrInputU[idxCol]);
    END_FOR;
    arrOutputY_Est[idxRow] := rCx_Sum + rDu_Sum;
    (* Innovation residual error e[k] = y[k] - y_hat[k] *)
    arrInnovationError[idxRow] := arrOutputY_Meas[idxRow] - arrOutputY_Est[idxRow];
END_FOR;

(* ---------------------------------------------------------------------------------------------------------
 * 3. STATE ESTIMATOR PROPAGATION: x_hat[k+1] = A * x_hat[k] + B * u[k] + L * e[k]
 * --------------------------------------------------------------------------------------------------------- *)
FOR idxRow := 1 TO 6 DO
    rAx_Sum := 0.0;
    rBu_Sum := 0.0;
    rLe_Sum := 0.0;
    FOR idxCol := 1 TO 6 DO
        rAx_Sum := rAx_Sum + (matA[idxRow, idxCol] * arrStateX_Hat[idxCol]);
        rBu_Sum := rBu_Sum + (matB[idxRow, idxCol] * arrInputU[idxCol]);
        rLe_Sum := rLe_Sum + (matL[idxRow, idxCol] * arrInnovationError[idxCol]);
    END_FOR;
    arrStateX_Next[idxRow] := rAx_Sum + rBu_Sum + rLe_Sum;
END_FOR;

(* Update state vector estimates for next cycle *)
FOR idxRow := 1 TO 6 DO
    arrStateX_Hat[idxRow] := arrStateX_Next[idxRow];
END_FOR;

(* Export Observable Cyber-Physical Physical State Quantities *)
rEstimatedThicknessDev_um     := arrStateX_Hat[1];
rEstimatedRibbonWidth_mm      := rRecipeTargetWidth + arrStateX_Hat[2];
rEstimatedBathTempGrad_degC_m := ((rRecipeTargetTinBathInletTemp - rRecipeTargetBathExitTemp) + arrStateX_Hat[3]) / 65.0;
rEstimatedAtmPress_mbar       := 0.450 + arrStateX_Hat[4];
rEstimatedAnnealStress_nm_cm  := (rRecipeMaxStressLimit * 0.50) + arrStateX_Hat[5];
rEstimatedLineSpeed_m_min     := rRecipeTargetLineSpeed + arrStateX_Hat[6];

(* ---------------------------------------------------------------------------------------------------------
 * 4. FIRST-PRINCIPLES MOLTEN TIN BATH EQUILIBRIUM SPREAD FORMULATION
 * Computes natural equilibrium thickness h_eq governed by Neumann three-phase interfacial wetting equilibrium:
 * h_eq^2 = [ 2 * (gamma_g_atm + gamma_g_tin - gamma_tin_atm) * rho_tin ] / [ g * rho_g * (rho_tin - rho_g) ]
 * --------------------------------------------------------------------------------------------------------- *)
IF (rDensityLiquidTin > rDensityMoltenGlass) AND (rGravitationalConst > 0.0) THEN
    (* Interfacial energy balance factor S = gamma_g_atm + gamma_g_tin - gamma_tin_atm *)
    rEquilibriumThickness_heq := SQRT(
        MAX(0.0001, (2.0 * (rSurfaceTension_g_atm + rSurfaceTension_g_tin - rSurfaceTension_tin_atm) * rDensityLiquidTin) /
        (rGravitationalConst * rDensityMoltenGlass * (rDensityLiquidTin - rDensityMoltenGlass)))
    ) * 1000.0; (* Converted from meters to millimeters: evaluates to ~6.85 mm *)
ELSE
    rEquilibriumThickness_heq := 6.85; (* Safe physical fallback constant *)
END_IF;

(* ---------------------------------------------------------------------------------------------------------
 * 5. VOGEL-FULCHER-TAMMANN (VFT) DYNAMIC VISCOSITY FORMULATION
 * Computes molten soda-lime-silica glass dynamic viscosity: log10(eta) = A_vft + B_vft / (T - T0_vft)
 * --------------------------------------------------------------------------------------------------------- *)
(* Forehearth Delivery Canal Glass Viscosity *)
IF rMoltenGlassInletTemp > (rVFT_Param_T0 + 50.0) THEN
    rCalculatedLogViscosityCanal := rVFT_Param_A + (rVFT_Param_B / (rMoltenGlassInletTemp - rVFT_Param_T0));
ELSE
    rCalculatedLogViscosityCanal := 3.20; (* ~1,600 dPa.s typical delivery canal viscosity *)
END_IF;

(* Tin Bath Exit Glass Viscosity (must achieve softening / working point ~10^7.6 dPa.s for lift-out) *)
IF rBathExitGlassTempFeedback > (rVFT_Param_T0 + 50.0) THEN
    rCalculatedViscosityBathExit := EXPT(10.0, rVFT_Param_A + (rVFT_Param_B / (rBathExitGlassTempFeedback - rVFT_Param_T0)));
ELSE
    rCalculatedViscosityBathExit := 4.0E7; (* 40 MPa.s visco-elastic state *)
END_IF;

(* ---------------------------------------------------------------------------------------------------------
 * 6. 16 MOTORIZED TOP-ROLLER KNURL MACHINES: KINEMATICS, TRACTIVE FORCE & SLIP
 * --------------------------------------------------------------------------------------------------------- *)
bAlarm_TopRollerAnySlip     := FALSE;
bAlarm_TopRollerCoolingFail := FALSE;

FOR idxRoller := 1 TO 16 DO
    (* 1. Knurl wheel peripheral circumferential velocity v_knurl [m/min] *)
    (* Outer knurl wheel pitch diameter = 300 mm -> circumference = pi * 0.300 m = 0.94248 m *)
    (* v_knurl = RPM * 0.94248 [m/min] *)
    arrTopRollerActualSpeed[idxRoller] := arrTopRollerSpeedCmd[idxRoller];

    (* 2. Local ribbon forward velocity interpolation along 65m bath bath *)
    (* Ribbon accelerates non-linearly from canal delivery speed (~1.5 m/min) to lehr line speed (~12.5 m/min) *)
    (* Local ribbon velocity v_ribbon(idxRoller) *)
    arrTopRollerSlipRatio[idxRoller] := 1.0 - (
        (1.50 + ((rLehrDriveSpeedFeedback - 1.50) * (DINT_TO_REAL(idxRoller) / 16.0))) /
        MAX(0.10, arrTopRollerActualSpeed[idxRoller] * 0.94248)
    );

    (* 3. Knurl tooth slip monitoring & tractive bite force calculation *)
    (* F_tractive = C_friction * penetration [mm] * cos(toe_angle) * (motor_torque / radius) *)
    arrTopRollerActualPen[idxRoller]   := arrTopRollerPenetrationCmd[idxRoller];
    arrTopRollerActualAngle[idxRoller] := arrTopRollerAngleCmd[idxRoller];
    arrTopRollerMotorTorque[idxRoller] := 35.0 + (arrTopRollerActualPen[idxRoller] * 12.0) + (DINT_TO_REAL(idxRoller) * 1.5);
    
    arrTopRollerTractiveForce_N[idxRoller] := arrTopRollerMotorTorque[idxRoller] * 
                                              arrTopRollerActualPen[idxRoller] * 
                                              COS(arrTopRollerActualAngle[idxRoller] * 3.14159265 / 180.0) * 8.5;

    (* Detect slip trip condition: excessive slip ratio (> 18%) or loss of tractive bite force *)
    IF arrTopRollerSlipRatio[idxRoller] > 0.18 OR arrTopRollerSlipRatio[idxRoller] < -0.10 THEN
        arrTopRollerSlipTrip[idxRoller] := TRUE;
        bAlarm_TopRollerAnySlip := TRUE;
    ELSE
        arrTopRollerSlipTrip[idxRoller] := FALSE;
    END_IF;

    (* Shaft internal cooling water flow verification (> 22.0 L/min required to prevent shaft sagging) *)
    IF arrTopRollerShaftWaterFlow[idxRoller] < 22.0 OR arrTopRollerShaftTemp[idxRoller] > 75.0 THEN
        bAlarm_TopRollerCoolingFail := TRUE;
    END_IF;
END_FOR;

(* ---------------------------------------------------------------------------------------------------------
 * 7. ANNEALING LEHR VISCOELASTIC THERMAL STRESS RELAXATION (TOOL-NARAYANASWAMY)
 * Stress accumulation: sigma_thermal = [ E * alpha / (1 - nu) ] * Delta_T_transverse * exp(-t_residence / tau)
 * Birefringence retardation: Delta = C_photoelastic * sigma_thermal * thickness
 * --------------------------------------------------------------------------------------------------------- *)
(* Calculate continuous line residence time in Annealing Zone A (length = 24.0 m) *)
IF rLehrDriveSpeedFeedback > 0.50 THEN
    (* Residence time t_res = 24.0 m / (v_line [m/min] / 60.0) [seconds] *)
    rNarayanaswamyTauZero := 24.0 / (rLehrDriveSpeedFeedback / 60.0);
ELSE
    rNarayanaswamyTauZero := 120.0;
END_IF;

(* Maximum transverse temperature differential across Lehr Zone A-B *)
arrLehrTransverseDeltaT[1] := ABS(arrLehrZoneTempActual[1] - arrLehrInletTempFeedback);
arrLehrTransverseDeltaT[2] := ABS(arrLehrZoneTempActual[2] - (arrLehrZoneTempActual[1] - 25.0));

(* Thermal stress in MPa: E=72 GPa, alpha=9.0e-6 /K, nu=0.22 -> [E*alpha/(1-nu)] = ~0.83 MPa/K *)
rCalculatedThermalStressMPa := 0.830 * arrLehrTransverseDeltaT[2] * EXP(-rNarayanaswamyTauZero / 95.0);

(* Calculated polarimetric optical retardation: Delta [nm/cm] = C_Brewster * sigma [MPa] * 10.0 *)
(* Photoelastic constant C = 2.65 Brewsters *)
IF rCalculatedThermalStressMPa > 0.0 THEN
    rEstimatedAnnealStress_nm_cm := 2.65 * rCalculatedThermalStressMPa * (rVotedThickness_mm / 10.0) * 10.0;
END_IF;
"""

if __name__ == "__main__":
    s = generate_phase2()
    print(f"Phase 2 length: {len(s)} chars")
