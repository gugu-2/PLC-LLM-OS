# part4_physics_statespace.py

def get_part4_physics_statespace():
    return """(* =====================================================================================================================
 * PHASE 2: CYBER-PHYSICAL THERMODYNAMIC, KINETIC & MASS TRANSFER OBSERVERS
 * ===================================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------------------------
 * 2.1 Heterogeneous Solid Bed Waste Combustion & Heat Release
 * --------------------------------------------------------------------------------------------------------------------- *)
(* Total MSW Mass Flow Rate: 1,500 t/d = 62,500 kg/h *)
rSolidWasteMassFlow_kgh := 62500.0;
(* Total Thermal Power Released: P_th = (MassFlow * LHV) / 3600 [MW] *)
rNetThermalHeatRelease_MW := (rSolidWasteMassFlow_kgh * rWasteHeatingValue_LHV_MJkg) / 3600.0;

(* Aerodynamic Wet Flue Gas Production Rate [Nm3/h] *)
rCalculatedFlueGasFlow_Nm3h := rSolidWasteMassFlow_kgh * c_rNominalFlueGasSpecificVol_Nm3_kg * (1.0 + (rWasteMoistureContent_pct - 35.0) * 0.008);

(* Flue Gas Volumetric Expansion in Post-Combustion Chamber at Actual Temperature *)
rMathTemp_A := rCalculatedFlueGasFlow_Nm3h * ((rPostCombustion2SecTempVoted_degC + 273.15) / 273.15) / 3600.0; (* Actual m3/s *)
IF rMathTemp_A > 10.0 THEN
    rFlueGasMeanVelocity_ms := rMathTemp_A / 78.5; (* Based on 78.5 m2 cross section *)
    rResidenceTimeCalculated_s := c_rPostCombZoneVolume_m3 / rMathTemp_A;
ELSE
    rFlueGasMeanVelocity_ms := 4.25;
    rResidenceTimeCalculated_s := 2.45;
END_IF;
rCalculatedFlueGasResidenceTime_s := rResidenceTimeCalculated_s;

(* EU Directive 2010/75/EU Statutory Compliance Verification (>= 850.0 °C for >= 2.0 s at >= 6.0 % O2) *)
IF (rPostCombustion2SecTempVoted_degC >= 850.0) AND (rResidenceTimeCalculated_s >= 2.00) AND (AIT_STACK_O2_404A >= 6.00) THEN
    bEU_Directive_2010_75_Compliant := TRUE;
    rBreachAccumulator_Temp_s := 0.0;
ELSE
    bEU_Directive_2010_75_Compliant := FALSE;
    rBreachAccumulator_Temp_s := rBreachAccumulator_Temp_s + c_rTs;
    (* Automatic Auxiliary Low-NOx Support Burner Firing if Temperature Slumps Below 875 °C *)
    IF (rPostCombustion2SecTempVoted_degC < 875.0) AND bAuxiliaryBurnerAvailable THEN
        bAuxiliaryBurnerActive := TRUE;
        rAuxiliaryBurnerFiringRate_pct := LIMIT(0.0, (875.0 - rPostCombustion2SecTempVoted_degC) * 3.5, 100.0);
    ELSE
        bAuxiliaryBurnerActive := FALSE;
        rAuxiliaryBurnerFiringRate_pct := 0.0;
    END_IF;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * 2.2 Arrhenius Gas-Phase Thermal NOx (Zeldovich Mechanism) & Fuel NOx Kinetics
 * --------------------------------------------------------------------------------------------------------------------- *)
(* Thermal NOx Kinetics: Zeldovich Forward Reaction Rate d[NO]/dt = k0 * exp(-Ea / (R*T)) * [N2] * [O2]^0.5 *)
rMathTemp_B := rCombustionChamberTempVoted_degC + 273.15; (* Absolute Core Temperature [K] *)
IF rMathTemp_B > 800.0 THEN
    (* Taylor expansion / exponential calculation of Arrhenius term *)
    rMathTemp_C := -c_rZeldovich_Ea / (c_rGasConstant_R * rMathTemp_B);
    IF rMathTemp_C > -40.0 THEN
        rArrheniusReactionRate_NOx := c_rZeldovich_k0 * EXP(rMathTemp_C) * 0.76 * SQRT(MAX(0.01, AIT_STACK_O2_404A / 100.0));
    ELSE
        rArrheniusReactionRate_NOx := 0.0;
    END_IF;
ELSE
    rArrheniusReactionRate_NOx := 0.0;
END_IF;

(* Fuel-Bound Nitrogen Conversion into Fuel NOx *)
rMathTemp_A := (rSolidWasteMassFlow_kgh * c_rFuelNitrogenWeightFraction * c_rFuelNitrogenConversionRatio * (c_rMolarMass_NO2_kgkmol / 14.007)) * 1.0E6 / MAX(1000.0, rCalculatedFlueGasFlow_Nm3h);
rPredictedRawInletNOx_mgNm3 := LIMIT(150.0, rMathTemp_A + rArrheniusReactionRate_NOx * 45.0, 650.0);

(* ---------------------------------------------------------------------------------------------------------------------
 * 2.3 Selective Non-Catalytic Reduction (SNCR) Urea Kinetics & Ammonia Slip Selectivity Window
 * --------------------------------------------------------------------------------------------------------------------- *)
(* Temperature Window Kinetic Selectivity: Optimum at 965 °C (Gaussian window half-width 75 °C) *)
rMathTemp_A := (rPostCombustion2SecTempVoted_degC - c_rSNCR_OptimumTemp_degC) / c_rSNCR_WindowHalfWidth_degC;
rTempSelectivityFactor := EXP(-0.5 * rMathTemp_A * rMathTemp_A);

(* Chemical DeNOx Reduction Efficiency Across SNCR Injection Zone *)
(* Governing Stoichiometry: CO(NH2)2 + 2 NO + 0.5 O2 -> 2 N2 + CO2 + 2 H2O *)
rMathTemp_B := (FT_UREA_INJECTION_501A * 0.40 / c_rMolarMass_Urea_kgkmol) * 2.0; (* Moles NH2 delivered / h *)
rMathTemp_C := (rPredictedRawInletNOx_mgNm3 * rCalculatedFlueGasFlow_Nm3h / 1.0E6) / c_rMolarMass_NO2_kgkmol; (* Moles NOx / h *)
IF rMathTemp_C > 0.01 THEN
    rMathTemp_A := rMathTemp_B / rMathTemp_C; (* Current Normalized Stoichiometric Ratio NSR *)
ELSE
    rMathTemp_A := 1.0;
END_IF;

rPredictedDeNOxConversion_pct := LIMIT(0.0, rTempSelectivityFactor * (1.0 - EXP(-1.45 * rMathTemp_A)) * 88.0, 92.0);
rSNCR_DeNOxEfficiency_pct := rPredictedDeNOxConversion_pct;

(* Ammonia Slip Dynamics: Severe NH3 Surge Below 850 °C; Oxidation into NOx Above 1050 °C *)
IF rPostCombustion2SecTempVoted_degC < 850.0 THEN
    (* Low-temperature chemical freeze: unreacted urea flashes into stack ammonia slip *)
    rPredictedNH3Slip_mgNm3 := LIMIT(0.2, (850.0 - rPostCombustion2SecTempVoted_degC) * 0.18 + (rMathTemp_A * 1.5), 15.0);
ELSIF rPostCombustion2SecTempVoted_degC > 1050.0 THEN
    (* High-temperature urea oxidation: NH2 + O2 -> NOx + H2O *)
    rPredictedNH3Slip_mgNm3 := 0.25;
    rPredictedDeNOxConversion_pct := rPredictedDeNOxConversion_pct * 0.45; (* Severe deNOx penalty *)
ELSE
    (* Optimum window operation: low slip proportional to over-stoichiometric NSR *)
    rPredictedNH3Slip_mgNm3 := LIMIT(0.1, 0.45 + MAX(0.0, rMathTemp_A - 1.2) * 1.85, 3.5);
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * 2.4 Semi-Dry Spray Absorber Slaked Lime Ca(OH)2 Slurry Neutralization & Droplet Mass Transfer
 * --------------------------------------------------------------------------------------------------------------------- *)
(* Two-Film Theory Neutralization: Ca(OH)2 + 2 HCl -> CaCl2 + 2 H2O | Ca(OH)2 + SO2 + 0.5 O2 -> CaSO4 + H2O *)
(* Slurry Droplet Liquid Film Evaporation Time vs Approach to Saturation *)
rDropletEvaporationTime_s := 0.85 * (rSlurryDropletSauterMeanDiam_um / 42.0) * (rSlurryDropletSauterMeanDiam_um / 42.0);
rAbsorberApproachToSaturation_degC := LIMIT(10.0, 145.0 - (FT_LIME_SLURRY_FEED_701A * 0.08), 35.0);

(* Overall Acid Neutralization Conversion Efficiencies *)
rPredictedHClNeutralization_pct := LIMIT(80.0, 99.2 - (rAbsorberApproachToSaturation_degC - 15.0) * 0.25, 99.8);
rPredictedSO2Neutralization_pct := LIMIT(70.0, 92.5 - (rAbsorberApproachToSaturation_degC - 15.0) * 0.45, 96.5);
rAcidGasNeutralizationEfficiency_pct := (rPredictedHClNeutralization_pct + rPredictedSO2Neutralization_pct) * 0.5;

(* ---------------------------------------------------------------------------------------------------------------------
 * 2.5 Powdered Activated Carbon (PAC) Dioxin & Heavy Metal Adsorption Equilibrium
 * --------------------------------------------------------------------------------------------------------------------- *)
(* Paced Pneumatic PAC Injection Concentration [mg/Nm3] *)
IF rCalculatedFlueGasFlow_Nm3h > 1000.0 THEN
    rPAC_SpecificDosing_mg_Nm3 := (FT_ACTIVATED_CARBON_702A * 1.0E6) / rCalculatedFlueGasFlow_Nm3h;
ELSE
    rPAC_SpecificDosing_mg_Nm3 := 260.0;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * 2.6 Boiler Superheater Chlorine Eutectic Corrosion Acoustic Thickness Observer
 * --------------------------------------------------------------------------------------------------------------------- *)
(* High-Temperature Chlorine Corrosion: Fe + 2 HCl + 0.5 O2 -> FeCl2(s) + H2O; Eutectic melting with alkali chlorides *)
rMathTemp_A := 420.0 + 273.15; (* Superheated Steam Temperature [K] *)
rMathTemp_B := -c_rCorrosionChlorineEa / (c_rGasConstant_R * rMathTemp_A);
IF rMathTemp_B > -35.0 THEN
    rInstantaneousCorrosionRate_um_h := c_rCorrosionBaseRate_um_h * EXP(rMathTemp_B) * 5.2E6 * EXPT(MAX(0.1, rFlueGasHClVoted_mgNm3 / 500.0), 0.65);
ELSE
    rInstantaneousCorrosionRate_um_h := 0.038;
END_IF;
rCorrosionRate_um_per_1000h := rInstantaneousCorrosionRate_um_h * 1000.0;
rAccumulatedTubeLoss_um := rAccumulatedTubeLoss_um + (rInstantaneousCorrosionRate_um_h * (c_rTs / 3600.0));

(* =====================================================================================================================
 * PHASE 3: 8x8 MULTIVARIABLE DISCRETE STATE-SPACE MODEL PROPAGATION
 * ===================================================================================================================== *)

(* Formulate State Vector x[k] From Real-Time Telemetry Deviations *)
ax_state[1] := (rWasteMoistureContent_pct - 35.0);                  (* State 1: Bed Moisture Deficit [%] *)
ax_state[2] := (rCombustionChamberTempVoted_degC - 1000.0);         (* State 2: Bed Core Temp Dev [deg C] *)
ax_state[3] := (rCombustionChamberTempVoted_degC - rTargetCombustionTemp_degC); (* State 3: Flame Temp Dev [deg C] *)
ax_state[4] := (rPostCombustion2SecTempVoted_degC - rTargetPostCombTemp_degC);  (* State 4: 2-Sec Temp Dev [deg C] *)
ax_state[5] := (rSteamFlowVoted_th - rTargetSteamFlow_th);           (* State 5: Steam Evap Dev [t/h] *)
ax_state[6] := (rStackNOxVoted_mgNm3 - rTargetStackNOx_mgNm3);       (* State 6: Stack NOx Dev [mg/Nm3] *)
ax_state[7] := (rStackSO2Voted_mgNm3 - rTargetStackSO2_mgNm3);       (* State 7: Stack SO2 Dev [mg/Nm3] *)
ax_state[8] := (rAcidGasNeutralizationEfficiency_pct - 95.0);        (* State 8: Scrubbing Yield Dev [%] *)

(* Reference State Equilibrium Setpoint Vector r = 0 *)
FOR iIdx_i := 1 TO 8 DO
    ax_ref[iIdx_i] := 0.0;
END_FOR;

(* Discrete State Propagation: x[k+1] = A * x[k] + B * u[k] *)
FOR iIdx_i := 1 TO 8 DO
    rMathTemp_A := 0.0;
    FOR iIdx_j := 1 TO 8 DO
        rMathTemp_A := rMathTemp_A + aA[iIdx_i, iIdx_j] * ax_state[iIdx_j] + aB[iIdx_i, iIdx_j] * au_control[iIdx_j];
    END_FOR;
    ax_next[iIdx_i] := rMathTemp_A;
    aPredictedState[iIdx_i] := rMathTemp_A;
END_FOR;

(* Simulated Output Vector y[k] = C * x[k] + D * u[k] *)
FOR iIdx_i := 1 TO 8 DO
    rMathTemp_A := 0.0;
    FOR iIdx_j := 1 TO 8 DO
        rMathTemp_A := rMathTemp_A + aC[iIdx_i, iIdx_j] * ax_state[iIdx_j] + aD[iIdx_i, iIdx_j] * au_control[iIdx_j];
    END_FOR;
    ay_output[iIdx_i] := rMathTemp_A;
END_FOR;

(* =====================================================================================================================
 * PHASE 4: RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) OPTIMIZATION
 * ===================================================================================================================== *)

(* Compute Real-Time Analytical Gradient dJ/du *)
FOR iIdx_j := 1 TO 8 DO
    (* Actuator Magnitude and Slew Penalty Terms *)
    au_delta[iIdx_j] := au_control[iIdx_j] - au_prev[iIdx_j];
    rMathTemp_A := 2.0 * aWeightR[iIdx_j] * au_control[iIdx_j] + 2.0 * aS_Weight[iIdx_j] * au_delta[iIdx_j];

    (* Coupling with Predicted State Tracking Errors *)
    rMathTemp_B := 0.0;
    FOR iIdx_i := 1 TO 8 DO
        rMathTemp_B := rMathTemp_B + 2.0 * aWeightQ[iIdx_i] * (aPredictedState[iIdx_i] - ax_ref[iIdx_i]) * aB[iIdx_i, iIdx_j];
    END_FOR;
    aGrad_u[iIdx_j] := rMathTemp_A + rMathTemp_B;
END_FOR;

(* Projected Gradient Descent Optimization Step with Box Constraints *)
FOR iIdx_j := 1 TO 8 DO
    (* Gradient Descent Step *)
    rMathTemp_A := au_control[iIdx_j] - c_rPGD_Alpha * aGrad_u[iIdx_j];

    (* Slew Rate Clamping *)
    rMathTemp_B := LIMIT(au_prev[iIdx_j] - adelta_u_max[iIdx_j], rMathTemp_A, au_prev[iIdx_j] + adelta_u_max[iIdx_j]);

    (* Hard Actuator Saturation Clamping *)
    au_control[iIdx_j] := LIMIT(au_min[iIdx_j], rMathTemp_B, au_max[iIdx_j]);
    au_prev[iIdx_j] := au_control[iIdx_j];
END_FOR;

(* Compute Current MPC Objective Cost J *)
rMathTemp_A := 0.0;
FOR iIdx_i := 1 TO 8 DO
    rMathTemp_B := ax_state[iIdx_i] - ax_ref[iIdx_i];
    rMathTemp_A := rMathTemp_A + aWeightQ[iIdx_i] * rMathTemp_B * rMathTemp_B;
END_FOR;
FOR iIdx_j := 1 TO 8 DO
    rMathTemp_A := rMathTemp_A + aWeightR[iIdx_j] * au_control[iIdx_j] * au_control[iIdx_j] + aS_Weight[iIdx_j] * au_delta[iIdx_j] * au_delta[iIdx_j];
END_FOR;
rMPC_ObjectiveCost_J := rMathTemp_A;
"""
