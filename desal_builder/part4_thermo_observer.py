# desal_builder/part4_thermo_observer.py
# Phase 2: Cyber-Physical Thermodynamic, Membrane Hydraulic & Luenberger State-Space Observer

def get_part4_thermo_observer():
    return """
(* ====================================================================================================
   PHASE 2: FIRST-PRINCIPLES CYBER-PHYSICAL THERMODYNAMIC & HYDRAULIC OBSERVER
   Models Seawater Reverse Osmosis Darcy-Starling Flux, Arrhenius-Poiseuille Viscosity,
   Pitzer Osmotic Thermodynamics, Concentration Polarization, Isobaric ERD Efficiency,
   Stiff & Davis Scaling Index, and Full Luenberger Discrete State-Space Innovation Update.
   ==================================================================================================== *)

(* ----------------------------------------------------------------------------------------------------
   STEP 2.1: SEAWATER THERMODYNAMIC & TRANSPORT CORRECTION FACTORS
   ---------------------------------------------------------------------------------------------------- *)
(* Absolute Feed Temperature in Kelvin *)
rFeedWaterTemp_K := LIMIT(273.15 + 5.0, 273.15 + rRawSeawaterTemp_degC, 273.15 + 45.0);

(* Arrhenius-Poiseuille Temperature Correction Factor for Pure Water Viscosity (mu_25 = 0.890 mPa.s) *)
rWaterViscosityCorrectionFactor := EXP(rArrheniusEnergyWater_K * ((1.0 / rStandardTemp_K) - (1.0 / rFeedWaterTemp_K)));

(* Arrhenius Salt Diffusion Boundary Layer Temperature Correction Factor *)
rSaltDiffusionCorrectionFactor := EXP(rArrheniusEnergySalt_K * ((1.0 / rStandardTemp_K) - (1.0 / rFeedWaterTemp_K)));

(* Pitzer-van 't Hoff Osmotic Coefficient for Concentrated High-Salinity Marine Brine *)
rOsmoticCoeff_phi := 0.9150 + (0.00118 * (rRawSeawaterTds_ppm / 1000.0));

(* Bulk Feed Seawater Osmotic Pressure Pi_feed [bar] *)
(* Empirical Desalination Formulation: Pi = 0.0704 * T_K * phi * (TDS / 1000.0) / 1.05 *)
rFeedOsmoticPressure_bar := (0.0704 * rFeedWaterTemp_K * rOsmoticCoeff_phi * (rRawSeawaterTds_ppm / 1000.0)) / 1.05;
rFeedOsmoticPressure_bar := LIMIT(20.0, rFeedOsmoticPressure_bar, 48.0);

(* ----------------------------------------------------------------------------------------------------
   STEP 2.2: CONCENTRATION POLARIZATION & ACTIVE MEMBRANE SURFACE THERMODYNAMICS
   ---------------------------------------------------------------------------------------------------- *)
(* Current Estimated Volumetric Recovery Ratio Y_rec *)
IF (rObservedPermeateFlow_m3h + rVoted_FT401_ErdBrineFlow_m3h) > 500.0 THEN
    rVolumetricRecoveryRatio_calc := rObservedPermeateFlow_m3h / (rObservedPermeateFlow_m3h + rVoted_FT401_ErdBrineFlow_m3h);
ELSE
    rVolumetricRecoveryRatio_calc := 0.415; (* Baseline nominal 41.5% design recovery *)
END_IF;
rVolumetricRecoveryRatio_calc := LIMIT(0.300, rVolumetricRecoveryRatio_calc, 0.480);
rObservedRecoveryRatio_pct := rVolumetricRecoveryRatio_calc * 100.0;

(* Concentrate Brine Stream Osmotic Pressure Pi_conc [bar] *)
rConcentrateOsmoticPress_bar := rFeedOsmoticPressure_bar / MAX(0.50, 1.0 - rVolumetricRecoveryRatio_calc);
rConcentrateOsmoticPress_bar := LIMIT(35.0, rConcentrateOsmoticPress_bar, 75.0);

(* Concentration Polarization Beta Factor: beta = exp(k_cp * Y_rec) *)
rConcentrationPolarizationBeta := EXP(rConcentrationPolarizationConst * rVolumetricRecoveryRatio_calc);
rConcentrationPolarizationBeta := LIMIT(1.05, rConcentrationPolarizationBeta, 1.45);

(* Average Effective Osmotic Pressure Over Active Polyamide Barrier Layer [bar] *)
rAverageMembraneOsmotic_bar := 0.5 * (rFeedOsmoticPressure_bar + rConcentrateOsmoticPress_bar) * rConcentrationPolarizationBeta;
rAverageMembraneOsmotic_bar := LIMIT(25.0, rAverageMembraneOsmotic_bar, 60.0);
rObservedOsmoticPress_bar := rAverageMembraneOsmotic_bar;

(* ----------------------------------------------------------------------------------------------------
   STEP 2.3: MEMBRANE NET DRIVING PRESSURE (NDP) & PERMEATE WATER FLUX
   ---------------------------------------------------------------------------------------------------- *)
(* Pressure Drop Across High-Pressure Membrane Pressure Vessel Spacer Channels [bar] *)
rDynamicNetDrivingPressure_bar := rVoted_PT201_HpFeedPress_bar 
                                  - 1.45 (* Average Spacer Friction Drop / 2 *)
                                  - rPermeateBackPressure_bar 
                                  - rAverageMembraneOsmotic_bar;
rDynamicNetDrivingPressure_bar := LIMIT(0.0, rDynamicNetDrivingPressure_bar, 35.0);
rObservedNetDrivingPress_bar := rDynamicNetDrivingPressure_bar;

(* Water Permeate Flux J_w [LMH = L/(m2.h)] via Solution-Diffusion Mechanism *)
rDynamicMembraneFlux_LMH := x_state[8] * rWaterViscosityCorrectionFactor * rDynamicNetDrivingPressure_bar;
rDynamicMembraneFlux_LMH := LIMIT(0.0, rDynamicMembraneFlux_LMH, 30.0);
rObservedMembraneFlux_LMH := rDynamicMembraneFlux_LMH;

(* Total Clean Permeate Production Rate [m3/h] (Total Area = 125,000 m2) *)
rTotalPermeateVolumetricFlow := (rDynamicMembraneFlux_LMH * rTotalMembraneArea_m2) / 1000.0;
rObservedPermeateFlow_m3h := rTotalPermeateVolumetricFlow;

(* Total High Salinity Concentrate Reject Rate [m3/h] *)
rTotalBrineVolumetricFlow := rVoted_FT401_ErdBrineFlow_m3h;
rObservedBrineFlow_m3h := rTotalBrineVolumetricFlow;

(* ----------------------------------------------------------------------------------------------------
   STEP 2.4: SOLUTE MASS TRANSFER, PERMEATE TDS & SALT REJECTION RATIO
   ---------------------------------------------------------------------------------------------------- *)
(* Salt Passage Flux J_s [g/(m2.h)] *)
IF rDynamicMembraneFlux_LMH > 1.0 THEN
    (* Fickian Diffusion Across Dense Barrier Layer *)
    rDynamicPermeateTds_ppm := (rMembraneSaltPassingCoeff_B0 * rSaltDiffusionCorrectionFactor * rRawSeawaterTds_ppm * rConcentrationPolarizationBeta) 
                               / rDynamicMembraneFlux_LMH;
ELSE
    rDynamicPermeateTds_ppm := rRawSeawaterTds_ppm * 0.15;
END_IF;
rDynamicPermeateTds_ppm := LIMIT(10.0, rDynamicPermeateTds_ppm, 1200.0);

(* Permeate Electrical Conductivity Approximation (TDS to Conductivity Factor ~1.95 uS/cm per ppm) *)
rDynamicPermeateConductivity := rDynamicPermeateTds_ppm * 1.95;
rDynamicPermeateConductivity := LIMIT(20.0, rDynamicPermeateConductivity, 2500.0);

(* Polyamide Membrane Salt Rejection Efficiency [%] *)
IF rRawSeawaterTds_ppm > 1000.0 THEN
    rSaltPassageRatio_calc := rDynamicPermeateTds_ppm / rRawSeawaterTds_ppm;
    rObservedSaltRejection_pct := (1.0 - rSaltPassageRatio_calc) * 100.0;
ELSE
    rObservedSaltRejection_pct := 99.5;
END_IF;
rObservedSaltRejection_pct := LIMIT(90.0, rObservedSaltRejection_pct, 99.9);

(* ----------------------------------------------------------------------------------------------------
   STEP 2.5: ISOBARIC ENERGY RECOVERY DEVICE (PX) HYDRAULIC EFFICIENCY & MIXING
   ---------------------------------------------------------------------------------------------------- *)
(* Pressure Transfer Efficiency eta_PX = (P_PX_disch - P_LP_in) / (P_HP_brine - P_LP_out) * 100.0 *)
IF (rVoted_PT201_HpFeedPress_bar - rErdLpBrineOutPress_bar) > 10.0 THEN
    rErdHpPressureTransferCoeff := (rVoted_PT501_PxDischPress_bar - rVoted_PT101_IntakePress_bar) 
                                   / (rVoted_PT201_HpFeedPress_bar - rErdLpBrineOutPress_bar);
    rObservedErdEnergyRecovery_pct := LIMIT(85.0, rErdHpPressureTransferCoeff * 100.0, 98.5);
ELSE
    rObservedErdEnergyRecovery_pct := 96.5;
END_IF;

(* PX Ceramic Rotor Salinity Mixing & Volumetric Overflush Leak *)
(* Rotor Ducts carry tiny volumetric boundary layer: Delta_C_mix increases feed salinity by 150-400 ppm *)
rErdVolumetricOverflushRatio := 1.035; (* 3.5% Overflush baseline *)
rErdMixingSalinityLeak_ppm := (rRawSeawaterTds_ppm / (1.0 - rVolumetricRecoveryRatio_calc)) * 0.0055
                             * (1.0 + (0.02 * ABS(rVoted_PT201_HpFeedPress_bar - rVoted_PT501_PxDischPress_bar)));
rErdMixingSalinityLeak_ppm := LIMIT(50.0, rErdMixingSalinityLeak_ppm, 800.0);
rObservedErdMixingRatio_pct := (rErdMixingSalinityLeak_ppm / MAX(1000.0, rRawSeawaterTds_ppm)) * 100.0;

(* ----------------------------------------------------------------------------------------------------
   STEP 2.6: SPECIFIC ENERGY CONSUMPTION (SEC [kWh/m3])
   ---------------------------------------------------------------------------------------------------- *)
rTotalHydraulicPower_kW := rHppMotorPower_kW + rPxBpMotorPower_kW + rLpFeedPumpPower_kW;
IF rObservedPermeateFlow_m3h > 100.0 THEN
    rDynamicSpecificEnergy_kWh_m3 := rTotalHydraulicPower_kW / rObservedPermeateFlow_m3h;
ELSE
    rDynamicSpecificEnergy_kWh_m3 := 3.20; (* Baseline safe default *)
END_IF;
rDynamicSpecificEnergy_kWh_m3 := LIMIT(1.80, rDynamicSpecificEnergy_kWh_m3, 8.50);
rObservedSpecificEnergy_kWh_m3 := rDynamicSpecificEnergy_kWh_m3;

(* ----------------------------------------------------------------------------------------------------
   STEP 2.7: STIFF & DAVIS STABILITY INDEX (S&DSI) FOR HIGH-SALINITY SCALING RISK
   S&DSI = pH - pHs = pH - (K_sd + pCa + pAlk)
   ---------------------------------------------------------------------------------------------------- *)
(* Empirical K_sd parameter as function of temperature and ionic strength *)
rScalingIndex_S_DSI := rRawSeawaterPh - (2.75 + (0.012 * rRawSeawaterTemp_degC) + 2.10 + 2.30);
rObservedScalingIndex_Lsi := rScalingIndex_S_DSI;

(* Membrane Specific Permeability Output Assignment *)
rObservedMembranePermeability := x_state[8];

(* ----------------------------------------------------------------------------------------------------
   STEP 2.8: PREPARE INPUT, DISTURBANCE & MEASUREMENT VECTORS FOR DISCRETE STATE-SPACE
   ---------------------------------------------------------------------------------------------------- *)
(* Vector d: Exogenous Disturbances *)
d_dist[1] := rRawSeawaterTds_ppm;
d_dist[2] := rRawSeawaterTemp_degC;
d_dist[3] := rVoted_PT101_IntakePress_bar;
d_dist[4] := rVoted_AT102_FeedOrp_mV;
d_dist[5] := rRawSeawaterSdi15;
d_dist[6] := rRawSeawaterPh;

(* Vector u: Actuator Feedback / Applied Commands *)
u_ctrl[1] := rHppVfdOutputFreq_Hz;
u_ctrl[2] := rPxBpVfdOutputFreq_Hz;
u_ctrl[3] := rBrineThrottleValveCmd_pct;
u_ctrl[4] := rAntiscalantDosingStroke_pct;
u_ctrl[5] := rSbsDosingPumpStroke_pct;
u_ctrl[6] := rPermeateDivertValveCmd_pct;

(* Vector y_meas: Plant Instrumentation Feedback *)
y_meas[1] := rVoted_PT201_HpFeedPress_bar;
y_meas[2] := rObservedPermeateFlow_m3h;
y_meas[3] := rVoted_FT401_ErdBrineFlow_m3h;
y_meas[4] := rVoted_AT301_PermConduct_uS;
y_meas[5] := rVoted_PT201_HpFeedPress_bar - rVoted_PT501_PxDischPress_bar;
y_meas[6] := rObservedSpecificEnergy_kWh_m3;

(* ----------------------------------------------------------------------------------------------------
   STEP 2.9: STATE-SPACE PREDICTION ROLLOUT (x_pred = A*x + B*u + Bd*d)
   ---------------------------------------------------------------------------------------------------- *)
FOR i := 1 TO 8 DO
    rTempSum := 0.0;
    (* State transition contributions: A * x *)
    FOR j := 1 TO 8 DO
        rTempSum := rTempSum + (matA[i, j] * x_state[j]);
    END_FOR;
    (* Control input contributions: B * u *)
    FOR m := 1 TO 6 DO
        rTempSum := rTempSum + (matB[i, m] * u_ctrl[m]);
    END_FOR;
    (* Exogenous disturbance contributions: Bd * d *)
    FOR n := 1 TO 6 DO
        rTempSum := rTempSum + (matBd[i, n] * d_dist[n]);
    END_FOR;
    x_pred[i] := rTempSum;
END_FOR;

(* Physical State Clamping on Prior Predictions *)
x_pred[1] := LIMIT(0.0, x_pred[1], 100.0);   (* P_feed [bar] *)
x_pred[2] := LIMIT(0.0, x_pred[2], 40.0);    (* NDP [bar] *)
x_pred[3] := LIMIT(0.0, x_pred[3], 35.0);    (* Flux [LMH] *)
x_pred[4] := LIMIT(10.0, x_pred[4], 75.0);   (* Pi_bar [bar] *)
x_pred[5] := LIMIT(0.0, x_pred[5], 95.0);    (* P_erd [bar] *)
x_pred[6] := LIMIT(0.0, x_pred[6], 2000.0);  (* Delta_C_mix [ppm] *)
x_pred[7] := LIMIT(10.0, x_pred[7], 3000.0); (* Permeate Cond [uS/cm] *)
x_pred[8] := LIMIT(0.40, x_pred[8], 2.50);   (* Permeability Kw [LMH/bar] *)

(* ----------------------------------------------------------------------------------------------------
   STEP 2.10: ESTIMATED OUTPUT & INNOVATION RESIDUAL CALCULATION (e = y - (C*x_pred + D*u))
   ---------------------------------------------------------------------------------------------------- *)
FOR k := 1 TO 6 DO
    rTempSum := 0.0;
    FOR j := 1 TO 8 DO
        rTempSum := rTempSum + (matC[k, j] * x_pred[j]);
    END_FOR;
    FOR m := 1 TO 6 DO
        rTempSum := rTempSum + (matD[k, m] * u_ctrl[m]);
    END_FOR;
    y_est[k] := rTempSum;
    e_innov[k] := y_meas[k] - y_est[k];
END_FOR;

(* ----------------------------------------------------------------------------------------------------
   STEP 2.11: LUENBERGER STATE INNOVATION CORRECTION (x_hat = x_pred + L*e)
   ---------------------------------------------------------------------------------------------------- *)
FOR i := 1 TO 8 DO
    rTempSum := x_pred[i];
    FOR k := 1 TO 6 DO
        rTempSum := rTempSum + (matL[i, k] * e_innov[k]);
    END_FOR;
    x_hat[i] := rTempSum;
END_FOR;

(* Post-Innovation Bounds Enforcement and State Vector Update *)
x_hat[1] := LIMIT(0.0, x_hat[1], 100.0);
x_hat[2] := LIMIT(0.0, x_hat[2], 40.0);
x_hat[3] := LIMIT(0.0, x_hat[3], 35.0);
x_hat[4] := LIMIT(10.0, x_hat[4], 75.0);
x_hat[5] := LIMIT(0.0, x_hat[5], 95.0);
x_hat[6] := LIMIT(0.0, x_hat[6], 2000.0);
x_hat[7] := LIMIT(10.0, x_hat[7], 3000.0);
x_hat[8] := LIMIT(0.40, x_hat[8], 2.50);

FOR i := 1 TO 8 DO
    x_state[i] := x_hat[i];
END_FOR;
"""
