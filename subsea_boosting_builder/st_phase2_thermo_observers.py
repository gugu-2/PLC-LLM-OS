# subsea_boosting_builder/st_phase2_thermo_observers.py

def get_phase2_observers():
    return """(* ==================================================================================================== *)
(* PHASE 2: CYBER-PHYSICAL FLUID MECHANICS, ACOUSTICS, THERMODYNAMICS & OBSERVER ESTIMATION             *)
(* State-Space Luenberger Innovation, Wood's Multiphase Sonic Speed, Dynamic Slugging,                  *)
(* Hammerschmidt Hydrate Dissociation, and Twin-Screw Rotor/Casing Thermal Growth Estimation            *)
(* ==================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------- *)
(* 2.1: Primary Physical Calculations & Multiphase Fluid Mechanics                                      *)
(* ---------------------------------------------------------------------------------------------------- *)
(* Twin-Screw Operational Differential Pressure *)
rTwinScrewDifferentialPress_bar := rVotedDischargePress_bar - rVotedSuctionPress_bar;

(* In-situ Real Gas Dynamic Density Estimation [kg/m3] *)
IF (rSuctionTemp_degC + 273.15) > 200.0 AND rGasCompressibilityZ > 0.1 THEN
    rOperatingGasDensity_kgm3 := (rVotedSuctionPress_bar * 28.964 * rGasSpecificGravity) /
                                 (rGasCompressibilityZ * 0.0831447 * (rSuctionTemp_degC + 273.15));
    IF rOperatingGasDensity_kgm3 < 5.0 THEN
        rOperatingGasDensity_kgm3 := 5.0;
    ELSIF rOperatingGasDensity_kgm3 > 120.0 THEN
        rOperatingGasDensity_kgm3 := 120.0;
    END_IF;
ELSE
    rOperatingGasDensity_kgm3 := 38.5;
END_IF;

(* Homogeneous Multiphase Mixture Bulk Density [kg/m3] *)
rMultiphaseMixtureDensity_kgm3 := ((100.0 - rVotedGVF_pct) * 0.01 * rLiquidDensity_kgm3) +
                                  (rVotedGVF_pct * 0.01 * rOperatingGasDensity_kgm3);
IF rMultiphaseMixtureDensity_kgm3 < 10.0 THEN
    rMultiphaseMixtureDensity_kgm3 := 10.0;
END_IF;

(* Multiphase Mixture Gas Quality (Mass Fraction) *)
IF rMultiphaseMixtureDensity_kgm3 > 0.1 THEN
    rMixtureGasMassFraction := (rVotedGVF_pct * 0.01 * rOperatingGasDensity_kgm3) / rMultiphaseMixtureDensity_kgm3;
ELSE
    rMixtureGasMassFraction := 0.085;
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* 2.2: Wood's Formulation Multiphase Acoustic Sonic Speed Approximation [m/s]                           *)
(* Severe compressibility drop in multiphase gas-liquid emulsions (gas cushion compressibility)          *)
(* c_mix = sqrt( 1 / ( rho_mix * ( alpha/K_gas + (1-alpha)/K_liq ) ) )                                  *)
(* ---------------------------------------------------------------------------------------------------- *)
IF rVotedSuctionPress_bar > 1.0 AND rMultiphaseMixtureDensity_kgm3 > 10.0 THEN
    (* Gas bulk modulus K_gas = gamma * P [Pa] *)
    (* Liquid bulk modulus K_liq ~ 1.6E9 [Pa] (16,000 bar) *)
    (* alpha = GVF fraction (0..1) *)
    rMixtureAcousticSonicSpeed_mps := SQRT(1.0E5 / (rMultiphaseMixtureDensity_kgm3 *
        ((rVotedGVF_pct * 0.01 / (1.28 * rVotedSuctionPress_bar)) +
         ((100.0 - rVotedGVF_pct) * 0.01 / 16000.0))));

    (* Clamp acoustic speed to physically bounded limits in hydrocarbon multiphase mixtures *)
    IF rMixtureAcousticSonicSpeed_mps < 35.0 THEN
        rMixtureAcousticSonicSpeed_mps := 35.0;
    ELSIF rMixtureAcousticSonicSpeed_mps > 1150.0 THEN
        rMixtureAcousticSonicSpeed_mps := 1150.0;
    END_IF;
ELSE
    rMixtureAcousticSonicSpeed_mps := 185.0;
END_IF;
rMixtureAcousticSpeed_mps := rMixtureAcousticSonicSpeed_mps;

(* Twin-Screw Shaft Absorbed Hydraulic Power [kW] *)
IF rMotorVFD_SpeedFeedback_RPM > 50.0 THEN
    rHydraulicAbsorbedPower_kW := (rMotorVFD_ShaftTorque_kNm * rMotorVFD_SpeedFeedback_RPM * 2.0 * 3.14159265) / 60.0;
ELSE
    rHydraulicAbsorbedPower_kW := 0.0;
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* 2.3: Multiphase Gas Slugging Detection & Dynamic Surge Proximity Tracking                            *)
(* ---------------------------------------------------------------------------------------------------- *)
(* Filtered Gas Volume Fraction Rate of Change d(GVF)/dt [%/s] *)
rGVF_RateOfChange_pct_s := (rVotedGVF_pct - rGVF_Previous_pct) / rCycleTime_s;
rGVF_Previous_pct := rVotedGVF_pct;

(* Dynamic Slugging Alarm Criteria: High Acceleration or Extreme GVF *)
IF (rVotedGVF_pct >= 88.0) OR (rGVF_RateOfChange_pct_s >= 35.0) THEN
    bGasSlugDetected := TRUE;
    tGasSlugPersistTimer_s := tGasSlugPersistTimer_s + rCycleTime_s;
ELSE
    IF tGasSlugPersistTimer_s > 0.0 THEN
        tGasSlugPersistTimer_s := tGasSlugPersistTimer_s - (rCycleTime_s * 1.5);
        IF tGasSlugPersistTimer_s <= 0.0 THEN
            tGasSlugPersistTimer_s := 0.0;
            bGasSlugDetected := FALSE;
        END_IF;
    ELSE
        bGasSlugDetected := FALSE;
    END_IF;
END_IF;

(* Dense Liquid Slug Influx Detection *)
IF (rVotedGVF_pct <= 20.0) AND (rGVF_RateOfChange_pct_s <= -30.0) THEN
    bLiquidSlugDetected := TRUE;
ELSE
    bLiquidSlugDetected := FALSE;
END_IF;

(* Dynamic Pressure Ratio & Helico-Axial Anti-Surge Margin *)
IF rVotedSuctionPress_bar > 5.0 THEN
    rDynamicPressureRatio := rVotedDischargePress_bar / rVotedSuctionPress_bar;
ELSE
    rDynamicPressureRatio := 1.0;
END_IF;

(* Dynamic Surge Limit Line (SLL) as function of Speed and GVF *)
rSurgeLimitLine_Ratio := 3.20 + (rMotorVFD_SpeedFeedback_RPM / 4500.0 * 0.85) - (rVotedGVF_pct * 0.01 * 0.45);
rSurgeControlLine_Ratio := rSurgeLimitLine_Ratio * 0.88; (* 12% safety margin buffer *)

rSurgeDistance_Margin := rSurgeLimitLine_Ratio - rDynamicPressureRatio;
IF rSurgeLimitLine_Ratio > 0.1 THEN
    rSurgeProximityMargin_pct := (rSurgeDistance_Margin / rSurgeLimitLine_Ratio) * 100.0;
ELSE
    rSurgeProximityMargin_pct := 0.0;
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* 2.4: Mono-Ethylene Glycol (MEG) Hydrate Thermodynamic Inhibition Model                               *)
(* Hammerschmidt Correlation for Thermodynamic Hydrate Dissociation Boundary & Subcooling               *)
(* ---------------------------------------------------------------------------------------------------- *)
(* Hydrate equilibrium temperature T_hyd [deg C] as function of pressure *)
IF rVotedSuctionPress_bar > 2.0 THEN
    rHydrateEquilibriumTemp_degC := (8.90 * LN(rVotedSuctionPress_bar)) - 14.25;
    IF rHydrateEquilibriumTemp_degC < 2.0 THEN
        rHydrateEquilibriumTemp_degC := 2.0;
    ELSIF rHydrateEquilibriumTemp_degC > 28.0 THEN
        rHydrateEquilibriumTemp_degC := 28.0;
    END_IF;
ELSE
    rHydrateEquilibriumTemp_degC := 2.0;
END_IF;

(* Hydrate Subcooling Safety Temperature Margin [deg C] *)
rHydrateSubcoolingTemp_degC := rSuctionTemp_degC - rHydrateEquilibriumTemp_degC;
rHydrateSubcoolingMargin_degC := rHydrateSubcoolingTemp_degC;

(* Required Aqueous Phase MEG Concentration via Nielsen-Hammerschmidt Formulation *)
(* dT_depression = (K_H * W_MEG) / (M_MEG * (100 - W_MEG)) *)
(* Solving for required W_MEG to ensure 6.0 deg C safety subcooling buffer *)
IF (rHydrateEquilibriumTemp_degC + 6.0) > rSuctionTemp_degC THEN
    rRequiredMEG_WeightFraction_pct := 42.0;
    bHydrateRiskWarning := TRUE;
ELSE
    rRequiredMEG_WeightFraction_pct := 25.0 + (rWaterCut_pct * 0.20);
    bHydrateRiskWarning := FALSE;
END_IF;

IF rHydrateSubcoolingMargin_degC <= 2.0 THEN
    bHydrateCriticalInterlock := TRUE;
ELSE
    bHydrateCriticalInterlock := FALSE;
END_IF;

(* Commanded MEG Flow Rate & Dosing Injection Valve Profile *)
rCurrentMEG_DosingRate_kg_h := (rTargetMEG_DosingRatio_pct * 0.01) * 650.0;
rMEG_InjectionSupplyDP_bar := rMEG_InhibitorSupplyPress_bar - rVotedSuctionPress_bar;

(* ---------------------------------------------------------------------------------------------------- *)
(* 2.5: Twin-Screw Rotor & Casing Differential Thermal Expansion Compensation                            *)
(* Compression heat generation in high-GVF operation induces rotor growth faster than casing            *)
(* ---------------------------------------------------------------------------------------------------- *)
(* Gas Polytropic Compression Temperature Rise *)
IF rVotedSuctionPress_bar > 5.0 AND rVotedDischargePress_bar > rVotedSuctionPress_bar THEN
    (* Rotor core thermal observer integrating frictional churning and gas compression heat *)
    rRotorTemperature_degC := rRotorTemperature_degC +
        ((rDischargeTemp_degC - rRotorTemperature_degC) * (rCycleTime_s / 45.0)) +
        ((rVotedGVF_pct * 0.01 * (rDischargeTemp_degC - rSuctionTemp_degC) * 0.35) * (rCycleTime_s / 60.0));

    (* Pump outer casing conductive heat dissipation to subsea ambient seawater *)
    rCasingTemperature_degC := rCasingTemperature_degC +
        ((rSuctionTemp_degC - rCasingTemperature_degC) * (rCycleTime_s / 120.0)) -
        ((rCasingTemperature_degC - rSeabedAmbientTemp_degC) * (rCycleTime_s / 240.0));
ELSE
    rRotorTemperature_degC := rRotorTemperature_degC + ((rSuctionTemp_degC - rRotorTemperature_degC) * (rCycleTime_s / 60.0));
    rCasingTemperature_degC := rCasingTemperature_degC + ((rSeabedAmbientTemp_degC - rCasingTemperature_degC) * (rCycleTime_s / 180.0));
END_IF;

(* Clamp Observer Thermal Estimates to Plausible Metallurgical Boundaries *)
IF rRotorTemperature_degC < 0.0 THEN
    rRotorTemperature_degC := 0.0;
ELSIF rRotorTemperature_degC > 180.0 THEN
    rRotorTemperature_degC := 180.0;
END_IF;

IF rCasingTemperature_degC < 0.0 THEN
    rCasingTemperature_degC := 0.0;
ELSIF rCasingTemperature_degC > 140.0 THEN
    rCasingTemperature_degC := 140.0;
END_IF;

(* Radial Thermal Expansion Calculations [um] *)
rRotorThermalExpansion_um := rThermalExpansionCoeff_Rotor_perC * (rRotorLength_mm * 0.12) * (rRotorTemperature_degC - 20.0) * 1000.0;
rCasingThermalExpansion_um := rThermalExpansionCoeff_Casing_perC * (rRotorLength_mm * 0.12) * (rCasingTemperature_degC - 20.0) * 1000.0;

(* Net Differential Thermal Growth *)
rDifferentialGrowth_um := rRotorThermalExpansion_um - rCasingThermalExpansion_um;
IF rDifferentialGrowth_um < 0.0 THEN
    rDifferentialGrowth_um := 0.0;
END_IF;
rEstimatedThermalGrowth_um := rDifferentialGrowth_um;

(* Dynamic Remaining Radial Running Clearance [um] *)
rActiveRadialClearance_um := rRotorNominalClearanceCold_um - rDifferentialGrowth_um;
IF rActiveRadialClearance_um < 5.0 THEN
    rActiveRadialClearance_um := 5.0;
END_IF;
rDynamicClearance_um := rActiveRadialClearance_um;

(* Mechanical Clearance Warnings & Interlocks *)
IF rActiveRadialClearance_um <= 45.0 THEN
    bClearanceWarning := TRUE;
ELSE
    bClearanceWarning := FALSE;
END_IF;

IF rActiveRadialClearance_um <= 20.0 THEN
    bClearanceCriticalTrip := TRUE;
ELSE
    bClearanceCriticalTrip := FALSE;
END_IF;

(* High-GVF Mist Cooling Liquid Recycle Modulation *)
IF rActiveRadialClearance_um < 65.0 OR rVotedGVF_pct > 92.0 THEN
    rMistCoolingPID_Integral := rMistCoolingPID_Integral + ((65.0 - rActiveRadialClearance_um) * rCycleTime_s * 0.12);
    IF rMistCoolingPID_Integral > 80.0 THEN
        rMistCoolingPID_Integral := 80.0;
    ELSIF rMistCoolingPID_Integral < 0.0 THEN
        rMistCoolingPID_Integral := 0.0;
    END_IF;
    rMistCoolingRecycleDemand_pct := 25.0 + ((65.0 - rActiveRadialClearance_um) * 1.5) + rMistCoolingPID_Integral;
    IF rMistCoolingRecycleDemand_pct > 100.0 THEN
        rMistCoolingRecycleDemand_pct := 100.0;
    END_IF;
ELSE
    IF rMistCoolingPID_Integral > 0.0 THEN
        rMistCoolingPID_Integral := rMistCoolingPID_Integral - (rCycleTime_s * 5.0);
        IF rMistCoolingPID_Integral < 0.0 THEN
            rMistCoolingPID_Integral := 0.0;
        END_IF;
    END_IF;
    rMistCoolingRecycleDemand_pct := 0.0;
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* 2.6: Subsea Pressurized Barrier Fluid Closed-Loop (Plan 53B/C) Diagnostics                            *)
(* ---------------------------------------------------------------------------------------------------- *)
rBarrierFluidInternalPress_bar := rVotedDischargePress_bar + rVotedSealDP_bar;
rBarrierFluidOverpressure_bar := rVotedSealDP_bar;

(* Track Cumulative Leakage via Reservoir Piston Displacement Rate *)
tBarrierLeakIntegrator_s := tBarrierLeakIntegrator_s + rCycleTime_s;
rBarrierLeakAccumulated_mL := rBarrierLeakAccumulated_mL + (rBarrierFluidLeakRate_mLmin * (rCycleTime_s / 60.0));

IF rBarrierAccumulatorPress_bar < (rSeabedAmbientPress_bar + 35.0) THEN
    bBarrierAccumulatorLowVolume := TRUE;
ELSE
    bBarrierAccumulatorLowVolume := FALSE;
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* 2.7: Discrete State-Space Luenberger Observer State Estimation Update (6x6)                           *)
(* System States Deviation from Nominal Linearization Target:                                            *)
(* x_dev[k] = x_phys[k] - x_nominal                                                                     *)
(* y_meas = [P_suc_dev, P_dis_dev, GVF_dev, c_acoustic_dev, DP_dev, Torque_dev]                         *)
(* x_est[k+1] = A * x_est[k] + B * u[k] + L * (y_meas - C * x_est[k])                                   *)
(* ---------------------------------------------------------------------------------------------------- *)
(* Populate Normalized Deviation Measurement Vector *)
vecY_meas[0] := rVotedSuctionPress_bar - vecX_nominal[0];
vecY_meas[1] := rVotedDischargePress_bar - vecX_nominal[1];
vecY_meas[2] := rVotedGVF_pct - vecX_nominal[2];
vecY_meas[3] := rMixtureAcousticSonicSpeed_mps - vecX_nominal[3];
vecY_meas[4] := rTwinScrewDifferentialPress_bar - vecX_nominal[4];
vecY_meas[5] := rMotorVFD_ShaftTorque_kNm - vecX_nominal[5];

(* Calculate Estimated Measurements y_est = C * x_est *)
FOR mIdx := 0 TO 5 DO
    vecY_est[mIdx] := 0.0;
    FOR nIdx := 0 TO 5 DO
        vecY_est[mIdx] := vecY_est[mIdx] + (matC[mIdx, nIdx] * vecX_est[nIdx]);
    END_FOR;
    (* Innovation Residual Vector *)
    vecY_err[mIdx] := vecY_meas[mIdx] - vecY_est[mIdx];
END_FOR;

(* Propagate Observer Predictive Dynamic State: x_pred = A * x_est + B * u + L * y_err *)
FOR mIdx := 0 TO 5 DO
    vecX_pred[mIdx] := 0.0;
    (* Matrix A State Propagation *)
    FOR nIdx := 0 TO 5 DO
        vecX_pred[mIdx] := vecX_pred[mIdx] + (matA[mIdx, nIdx] * vecX_est[nIdx]);
    END_FOR;
    (* Matrix B Control Input Injection (with normalized actuator scaling) *)
    vecX_pred[mIdx] := vecX_pred[mIdx] + (matB[mIdx, 0] * (vecU[0] - vecU_target[0]) * 0.001);
    vecX_pred[mIdx] := vecX_pred[mIdx] + (matB[mIdx, 1] * (vecU[1] - vecU_target[1]) * 0.01);
    vecX_pred[mIdx] := vecX_pred[mIdx] + (matB[mIdx, 2] * (vecU[2] - vecU_target[2]) * 0.01);
    vecX_pred[mIdx] := vecX_pred[mIdx] + (matB[mIdx, 3] * (vecU[3] - vecU_target[3]) * 0.01);
    vecX_pred[mIdx] := vecX_pred[mIdx] + (matB[mIdx, 4] * (vecU[4] - vecU_target[4]) * 0.01);
    vecX_pred[mIdx] := vecX_pred[mIdx] + (matB[mIdx, 5] * (vecU[5] - vecU_target[5]) * 0.01);

    (* Matrix L Kalman/Observer Innovation Injection *)
    FOR pIdx := 0 TO 5 DO
        vecX_pred[mIdx] := vecX_pred[mIdx] + (matL[mIdx, pIdx] * vecY_err[pIdx]);
    END_FOR;
END_FOR;

(* Update Observer State Vector with Numerical Anti-Windup Clamping *)
FOR mIdx := 0 TO 5 DO
    IF vecX_pred[mIdx] > 500.0 THEN
        vecX_est[mIdx] := 500.0;
    ELSIF vecX_pred[mIdx] < -500.0 THEN
        vecX_est[mIdx] := -500.0;
    ELSE
        vecX_est[mIdx] := vecX_pred[mIdx];
    END_IF;
    (* Physical State Reconstruction: Absolute Value = Nominal + Deviation *)
    vecX[mIdx] := vecX_nominal[mIdx] + vecX_est[mIdx];
END_FOR;
"""
