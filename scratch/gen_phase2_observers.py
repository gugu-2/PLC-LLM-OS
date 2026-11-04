# Phase 2: Cyber-Physical Observers for FB_Mining_SAG_BallMill_GrindingCircuit

def get_phase2():
    return """(* === PHASE 2: CYBER-PHYSICAL OBSERVERS, RHEOLOGY & COMMINUTION ESTIMATORS === *)

(* 2.1 Hydrostatic Trunnion Bearing Oil Film & Dynamic Mass Observer *)
rBearingOilTempAvg_degC := (TT_FEED_BEARING_BABBITT_103A + TT_DISCH_BEARING_BABBITT_104A) * 0.50;

(* Temperature-dependent Reynolds viscosity compensation: mu = mu0 * exp(-b*(T - T0)) *)
IF rBearingOilTempAvg_degC > 10.0 AND rBearingOilTempAvg_degC < 95.0 THEN
    rOilDynamicViscosity_Pa_s := 0.320 * EXP(-0.038 * (rBearingOilTempAvg_degC - 40.0));
ELSE
    rOilDynamicViscosity_Pa_s := 0.085;
END_IF;

(* Dynamic oil film thickness calculation (Reynolds slot flow approximation) *)
IF rVoted_FeedTrunnionLift_bar > 10.0 THEN
    rDynamicFilmThickness_Feed_um := 135.0 * EXPT((180.0 / rVoted_FeedTrunnionLift_bar), 0.333) *
                                     (1.0 + 0.005 * (rVoted_MotorSpeed_rpm / rSagCriticalSpeed_rpm));
ELSE
    rDynamicFilmThickness_Feed_um := 0.0;
END_IF;

IF rVoted_DischTrunnionLift_bar > 10.0 THEN
    rDynamicFilmThickness_Disch_um := 138.0 * EXPT((190.0 / rVoted_DischTrunnionLift_bar), 0.333) *
                                      (1.0 + 0.005 * (rVoted_MotorSpeed_rpm / rSagCriticalSpeed_rpm));
ELSE
    rDynamicFilmThickness_Disch_um := 0.0;
END_IF;
rEstimatedOilFilmThickness_um := (rDynamicFilmThickness_Feed_um + rDynamicFilmThickness_Disch_um) * 0.50;

(* Dynamic Live Mill Mass Observer: subtract tare and speed-dependent hydrodynamic wedge *)
rRawEstimatedMass_tons := (rVoted_FeedTrunnionLift_bar * rFeedLiftFactor_tons_per_bar) +
                          (rVoted_DischTrunnionLift_bar * rDischLiftFactor_tons_per_bar) -
                          rTrunnionTareOffset_tons -
                          (rHydrodynamicLiftWedgeSlope * rVoted_MotorSpeed_rpm);

(* Low-pass filter for smooth 0.1 ton resolution weight telemetry *)
rEstimatedChargeWeight_tons := (0.050 * rRawEstimatedMass_tons) + (0.950 * rEstimatedChargeWeight_tons);

(* Slurry Liquid-Solid Volume Hold-Up Decomposition *)
rScratchSum := rEstimatedChargeWeight_tons - rSagShellTareMass_tons - rSagNominalBallCharge_tons;
IF rScratchSum < 100.0 THEN
    rScratchSum := 100.0;
END_IF;

(* Reconstruct internal ore mass and water hold-up based on target solid fraction *)
rScratchTerm := (rScratchSum * 0.285); (* Water mass hold-up [t] = volume [m3] *)
rEstimatedSlurryVolume_m3 := rScratchTerm + ((rScratchSum - rScratchTerm) * 0.420 / 2.750);

(* 2.2 Shell Acoustic Ear Trajectory & Direct Impact Observer *)
rAcousticImpactSeverity_dB := rVoted_ShellAcousticHighFreq_dB;

(* Direct shell liner impact severity index (%): spikes when high-frequency impact exceeds churning *)
IF rVoted_ShellAcousticLowFreq_dB > 10.0 THEN
    rDirectLinerImpactEnergy_pct := (rVoted_ShellAcousticHighFreq_dB / (rVoted_ShellAcousticLowFreq_dB + 5.0)) *
                                    (rVoted_MotorSpeed_rpm / rSagCriticalSpeed_rpm) * 115.0;
ELSE
    rDirectLinerImpactEnergy_pct := 0.0;
END_IF;

IF rDirectLinerImpactEnergy_pct > 100.0 THEN
    rDirectLinerImpactEnergy_pct := 100.0;
ELSIF rDirectLinerImpactEnergy_pct < 0.0 THEN
    rDirectLinerImpactEnergy_pct := 0.0;
END_IF;

(* Reconstruct dynamic charge toe impact angle (nominal 40.0 to 45.0 deg from BDC) *)
rReconstructedToeAngle_deg := 36.5 + (12.5 * (rVoted_MotorSpeed_rpm / rSagCriticalSpeed_rpm)) +
                              (0.008 * (rEstimatedChargeWeight_tons - 1285.0)) -
                              ((rVoted_ShellAcousticToe_dB - 74.0) * 0.085);

IF rReconstructedToeAngle_deg < 25.0 THEN
    rReconstructedToeAngle_deg := 25.0;
ELSIF rReconstructedToeAngle_deg > 65.0 THEN
    rReconstructedToeAngle_deg := 65.0;
END_IF;
rEstimatedToeAngle_deg := (0.080 * rReconstructedToeAngle_deg) + (0.920 * rEstimatedToeAngle_deg);

(* Reconstruct dynamic charge departure shoulder angle (nominal 315.0 to 325.0 deg) *)
rReconstructedShoulderAngle_deg := 305.0 + (18.5 * (rVoted_MotorSpeed_rpm / rSagCriticalSpeed_rpm)) -
                                   (0.006 * (rEstimatedChargeWeight_tons - 1285.0));
IF rReconstructedShoulderAngle_deg < 285.0 THEN
    rReconstructedShoulderAngle_deg := 285.0;
ELSIF rReconstructedShoulderAngle_deg > 345.0 THEN
    rReconstructedShoulderAngle_deg := 345.0;
END_IF;
rEstimatedShoulderAngle_deg := (0.080 * rReconstructedShoulderAngle_deg) + (0.920 * rEstimatedShoulderAngle_deg);

(* Ball Cataracting Parabolic Trajectory Kinematics *)
rBallTrajectoryInitialVel_ms := (rVoted_MotorSpeed_rpm * 2.0 * 3.14159265 / 60.0) * (rSagDiameterInsideLiners_m * 0.50);
(* Theoretical impact velocity into toe charge bed *)
rBallImpactVelocity_ms := SQRT((rBallTrajectoryInitialVel_ms * rBallTrajectoryInitialVel_ms) +
                               (2.0 * 9.81 * rSagDiameterInsideLiners_m * 0.65));
rEstimatedImpactVelocity_ms := rBallImpactVelocity_ms;

(* Grinding Efficiency Index based on Austin comminution specific rate of breakage *)
IF rVoted_MotorPower_MW > 2.0 AND rEstimatedChargeWeight_tons > 500.0 THEN
    rGrindingEfficiencyIndex_pct := ((rVoted_MotorPower_MW / 28.0) * 0.55 +
                                     (1.0 - (ABS(rEstimatedToeAngle_deg - 42.5) / 20.0)) * 0.45) * 100.0;
ELSE
    rGrindingEfficiencyIndex_pct := 0.0;
END_IF;

(* 2.3 Frozen Charge Detection & Catastrophic Slump Trip Engine *)
IF ST_SAG_MOTOR_SPEED_RPM_106A > 0.10 THEN
    (* Integrate angular displacement *)
    rMillRotationalDisplacement_deg := rMillRotationalDisplacement_deg +
                                       (rVoted_MotorSpeed_rpm * 360.0 / 60.0 * tExecutionScanTime_s);
    (* Integrate torque work *)
    rAccumulatedTorqueWork_kJ := rAccumulatedTorqueWork_kJ +
                                 (rVoted_MotorTorque_pct * 29500.0 / 100.0 *
                                  (rVoted_MotorSpeed_rpm * 2.0 * 3.14159265 / 60.0) * tExecutionScanTime_s);
ELSE
    rMillRotationalDisplacement_deg := 0.0;
    rAccumulatedTorqueWork_kJ := 0.0;
END_IF;

(* Frozen charge criterion: mill rotated past 35 degrees with high torque but no tumbling acoustic noise *)
IF (rMillRotationalDisplacement_deg > 35.0) AND (rMillRotationalDisplacement_deg < 85.0) AND
   (rVoted_MotorTorque_pct > 115.0) AND (rVoted_ShellAcousticToe_dB < 25.0) THEN
    bFrozenChargePotentialDetected := TRUE;
    tFrozenChargeScanTimer_s := tFrozenChargeScanTimer_s + tExecutionScanTime_s;
    IF tFrozenChargeScanTimer_s >= 0.150 THEN (* 150 ms persistence trip *)
        bFrozenChargeTrip := TRUE;
    END_IF;
ELSE
    tFrozenChargeScanTimer_s := 0.0;
    bFrozenChargePotentialDetected := FALSE;
END_IF;

(* 2.4 Plitt Hydrocyclone Cluster Hydraulic & Classification Model *)
(* Slurry Volumetric Solids Concentration fraction C_v *)
IF rVoted_CycloneFeedDensity_SG > 1.000 THEN
    rSlurryVolumetricSolids_Cv := (rVoted_CycloneFeedDensity_SG - 1.000) / (2.750 - 1.000);
ELSE
    rSlurryVolumetricSolids_Cv := 0.200;
END_IF;
IF rSlurryVolumetricSolids_Cv > 0.55 THEN
    rSlurryVolumetricSolids_Cv := 0.55;
ELSIF rSlurryVolumetricSolids_Cv < 0.10 THEN
    rSlurryVolumetricSolids_Cv := 0.10;
END_IF;

(* Slurry Apparent Viscosity (cP) via Thomas suspension rheology *)
rSlurryDynamicViscosity_cP := 1.00 * (1.0 + (2.5 * rSlurryVolumetricSolids_Cv) +
                                      (10.05 * rSlurryVolumetricSolids_Cv * rSlurryVolumetricSolids_Cv) +
                                      (0.00273 * EXP(16.6 * rSlurryVolumetricSolids_Cv)));

(* Predicted cluster manifold pressure (kPa) based on flow and active cyclone count *)
IF iActiveCycloneValvesCount >= 4 THEN
    rPredictedManifoldPress_kPa := 2.85 * EXPT((FT_CYCLONE_FEED_SLURRY_FLOW_M3H_203A / INT_TO_REAL(iActiveCycloneValvesCount)), 1.82) *
                                   (rVoted_CycloneFeedDensity_SG / 1.50) * 0.010;
ELSE
    rPredictedManifoldPress_kPa := 250.0;
END_IF;

(* Plitt corrected cut size d50c (microns) *)
IF FT_CYCLONE_FEED_SLURRY_FLOW_M3H_203A > 500.0 AND iActiveCycloneValvesCount >= 4 THEN
    rPlittCutSize_d50c_um := (50.5 * EXPT(0.650, 0.46) * EXPT(0.180, 0.60) * EXPT(0.220, 1.21) *
                              EXP(0.063 * (rSlurryVolumetricSolids_Cv * 100.0))) /
                             (EXPT(0.140, 0.71) * EXPT(1.850, 0.38) *
                              EXPT((FT_CYCLONE_FEED_SLURRY_FLOW_M3H_203A / INT_TO_REAL(iActiveCycloneValvesCount)), 0.45) *
                              SQRT(2.750 - 1.000));
ELSE
    rPlittCutSize_d50c_um := 75.0;
END_IF;

(* Water recovery to underflow fraction R_f *)
rPlittWaterSplitRecovery_Rf := 0.285 + (0.125 * (rVoted_CycloneManifoldPress_kPa / 100.0)) +
                               (0.150 * rSlurryVolumetricSolids_Cv);

(* Circulating load ratio (% of fresh feed) *)
IF (WT_FEEDER_1_ORE_TONS_HR_114 + WT_FEEDER_2_ORE_TONS_HR_115) > 500.0 THEN
    rCirculatingLoadRatio_pct := ((WT_BALLMILL_1_FEED_TONS_HR_303 + WT_BALLMILL_2_FEED_TONS_HR_304) /
                                  (WT_FEEDER_1_ORE_TONS_HR_114 + WT_FEEDER_2_ORE_TONS_HR_115)) * 100.0;
ELSE
    rCirculatingLoadRatio_pct := 250.0;
END_IF;

(* 2.5 In-Line Ultrasonic Attenuation Particle Size Spectrometer Inversion *)
(* Attenuation multi-frequency spectra (ECAH viscous + scattering loss inversion) *)
rAttenuationCoeff_2MHz_dB_cm := 0.85 + (0.015 * rVoted_ProductP80_um) + (1.20 * (rVoted_ProductDensity_SG - 1.0));
rAttenuationCoeff_10MHz_dB_cm := 2.45 + (0.045 * rVoted_ProductP80_um) + (2.80 * (rVoted_ProductDensity_SG - 1.0));
rAttenuationCoeff_30MHz_dB_cm := 6.20 + (0.125 * rVoted_ProductP80_um) + (6.50 * (rVoted_ProductDensity_SG - 1.0));

(* Reconstructed cumulative PSD metrics *)
rCalculatedP80_microns := (0.10 * rVoted_ProductP80_um) +
                          (0.90 * (38.5 + (12.2 * (rAttenuationCoeff_10MHz_dB_cm / (rAttenuationCoeff_2MHz_dB_cm + 0.1)))));
rEstimatedP80_microns := rCalculatedP80_microns;

(* 2.6 Pebble Crusher Circuit Mass Balance & Trommel Extraction *)
rPebbleMassExtractionRate_tph := WT_PEBBLE_RECYCLE_TONS_HR_118;
(* Surge bin mass accumulation *)
rPebbleSurgeBinLevel_pct := rPebbleSurgeBinLevel_pct +
                            ((rPebbleMassExtractionRate_tph - rPebbleCrusherFeedSp_tph) / 250.0 * (tExecutionScanTime_s / 3600.0) * 100.0);
IF rPebbleSurgeBinLevel_pct > 100.0 THEN
    rPebbleSurgeBinLevel_pct := 100.0;
ELSIF rPebbleSurgeBinLevel_pct < 0.0 THEN
    rPebbleSurgeBinLevel_pct := 0.0;
END_IF;
"""
