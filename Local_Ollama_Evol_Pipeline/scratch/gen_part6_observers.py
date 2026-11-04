# Generator part 6: Cyber-Physical Observers and Mathematical Estimators
def get_observers_logic():
    return """(* ============================================================================================= *)
(* SECTION 2: CYBER-PHYSICAL OBSERVERS, RHEOLOGY & AUSTIN-HERBST COMMINUTION ESTIMATORS         *)
(* ============================================================================================= *)

(* 2.1 Trunnion Bearing Hydrostatic Lift Total Live Mill Weight (0.1 Ton Precision) *)
rTmpVal := (rVoted_InletTrunnionPress_bar * rHydraulicLiftForceFactor_Inlet) +
           (rVoted_OutletTrunnionPress_bar * rHydraulicLiftForceFactor_Outlet) -
           rTrunnionHydraulicTareOffset_tons;

(* Low-pass filter for smooth 0.1 ton resolution weight telemetry *)
rVoted_TotalMillWeight_tons := (0.050 * rTmpVal) + (0.950 * rVoted_TotalMillWeight_tons);

(* 2.2 Live Ore, Water and Slurry Hold-up Inventory Separation *)
rTmpSum := rVoted_TotalMillWeight_tons - rMillShellTareMass_tons - rNominalBallChargeMass_tons;
IF rTmpSum < 50.0 THEN
    rTmpSum := 50.0;
END_IF;

(* Slurry Volumetric Fraction Decomposition *)
rSlurryDensity_kgm3 := rVoted_SlurryDensity_SG * 1000.0;
rEstimated_WaterHoldUp_m3 := (rTmpSum * 0.320) / rWaterSpecificGravity;
rEstimated_OreHoldUp_tons := rTmpSum - (rEstimated_WaterHoldUp_m3 * rWaterSpecificGravity);
rEstimated_SlurryHoldUp_m3 := rEstimated_WaterHoldUp_m3 + (rEstimated_OreHoldUp_tons * 0.450 / rSolidSpecificGravity_Ore);

(* Total Mill Volumetric Charge Filling Fraction Jc [% of shell volume] *)
rSlurryVolumetricFilling_Jpz := ((rNominalBallChargeMass_tons / 7.850 / 0.60) + rEstimated_SlurryHoldUp_m3) / rMillInternalVolume_m3 * 100.0;

(* 2.3 Shell Acoustic Microphone Array Signal Processing & Toe Position Tracking *)
(* Dynamic Grinding Toe Position: function of rotational speed, charge volume, and high-frequency acoustic peak *)
rDynamicToeEstimated_deg := 115.0 + (32.5 * (rVoted_RingMotorRPM / rMillCriticalSpeed_RPM)) +
                            (0.018 * (rVoted_TotalMillWeight_tons - 1250.0)) +
                            ((rVoted_AcousticToe_Pct - 25.0) * 0.150);

IF rDynamicToeEstimated_deg < 100.0 THEN
    rDynamicToeEstimated_deg := 100.0;
ELSIF rDynamicToeEstimated_deg > 165.0 THEN
    rDynamicToeEstimated_deg := 165.0;
END_IF;
rEstimated_ToeAngle_deg := (0.080 * rDynamicToeEstimated_deg) + (0.920 * rEstimated_ToeAngle_deg);

(* Dynamic Grinding Shoulder Position *)
rDynamicShoulderEstimated_deg := 300.0 + (28.0 * (rVoted_RingMotorRPM / rMillCriticalSpeed_RPM)) -
                                 (0.012 * (rVoted_TotalMillWeight_tons - 1250.0));
IF rDynamicShoulderEstimated_deg < 280.0 THEN
    rDynamicShoulderEstimated_deg := 280.0;
ELSIF rDynamicShoulderEstimated_deg > 350.0 THEN
    rDynamicShoulderEstimated_deg := 350.0;
END_IF;
rEstimated_ShoulderAngle_deg := (0.080 * rDynamicShoulderEstimated_deg) + (0.920 * rEstimated_ShoulderAngle_deg);

(* Direct Shell Liner Impact Severity Index Calculation *)
(* E_impact spikes when toe angle recedes and high-frequency sound exceeds low-frequency bed noise *)
IF rVoted_AcousticShoulder_Pct > 5.0 THEN
    rAcousticDirectImpactRaw := (rVoted_AcousticToe_Pct / (rVoted_AcousticShoulder_Pct + 8.5)) *
                                (rVoted_RingMotorRPM / rMillCriticalSpeed_RPM) * 88.5;
ELSE
    rAcousticDirectImpactRaw := rVoted_AcousticToe_Pct;
END_IF;

IF rAcousticDirectImpactRaw < 0.0 THEN
    rAcousticDirectImpactRaw := 0.0;
ELSIF rAcousticDirectImpactRaw > 100.0 THEN
    rAcousticDirectImpactRaw := 100.0;
END_IF;
rCalculated_LinerImpactIndex := (0.120 * rAcousticDirectImpactRaw) + (0.880 * rCalculated_LinerImpactIndex);

(* 2.4 Specific Comminution Energy Consumption (kWh/t) *)
rTotalFeedRate_tph := rVoted_FreshFeedRate_tph + WT_PEBBLE_RECYCLE_CONVEYOR_102A;
IF rTotalFeedRate_tph > 100.0 THEN
    rCalculated_SpecificEnergy_kWh_t := (rVoted_RingMotorPower_MW * 1000.0) / rTotalFeedRate_tph;
ELSE
    rCalculated_SpecificEnergy_kWh_t := 0.0;
END_IF;

(* 2.5 Austin-Herbst Breakage Kinetics & Pulp Lifter Slurry Discharge Transport *)
(* Austin specific breakage rate for critical top-size particles *)
rTmpVal := rAustin_SpecificBreakage_S0 *
           (rVoted_RingMotorRPM / rMillCriticalSpeed_RPM) *
           (1.0 / (1.0 + (0.065 / rAustin_CriticalSize_dcrit_m)));

(* Slurry discharge capacity through grate pulp lifters *)
IF rEstimated_SlurryHoldUp_m3 > 20.0 THEN
    rCalculatedGrateDischarge_m3h := rGrateDischargeCoeff * rGrateDischargeArea_m2 *
                                     SQRT(2.0 * 9.81 * (rEstimated_SlurryHoldUp_m3 / 185.0)) * 3600.0 *
                                     rPulpLifterEfficiency_eta * (rVoted_RingMotorRPM / rMillCriticalSpeed_RPM);
ELSE
    rCalculatedGrateDischarge_m3h := 0.0;
END_IF;

(* 2.6 Plitt Hydrocyclone Classification Model & Ro-Tap d50c Prediction *)
(* Volumetric slurry flow through active cyclones *)
IF iActiveCyclonesTargetCount > 0 THEN
    rTmpVal := FT_CYCLONE_FEED_FLOW_504A / INT_TO_REAL(iActiveCyclonesTargetCount); (* m3/h per cyclone *)
ELSE
    rTmpVal := FT_CYCLONE_FEED_FLOW_504A / 9.0;
END_IF;

IF rTmpVal < 100.0 THEN
    rTmpVal := 100.0;
END_IF;

(* Plitt corrected cut size d50c [um]:
   d50c = 50.5 * Dc^0.46 * Di^0.60 * Do^1.21 * exp(0.063 * Cv) / (Du^0.71 * h^0.38 * Q^0.45 * (rhos - rhol)^0.5) *)
rPlitt_VolumetricSolids_Cv := (rVoted_SlurryDensity_SG - 1.0) / (rSolidSpecificGravity_Ore - 1.0);
IF rPlitt_VolumetricSolids_Cv < 0.10 THEN
    rPlitt_VolumetricSolids_Cv := 0.10;
ELSIF rPlitt_VolumetricSolids_Cv > 0.55 THEN
    rPlitt_VolumetricSolids_Cv := 0.55;
END_IF;

rCalculated_Plitt_d50c_um := (50.5 * 0.819 * 0.332 * 0.160 * EXP(6.3 * rPlitt_VolumetricSolids_Cv)) /
                             (0.229 * 1.150 * SQRT(SQRT(rTmpVal)) * SQRT(rSolidSpecificGravity_Ore - 1.0)) * 14.5;

IF rCalculated_Plitt_d50c_um < 45.0 THEN
    rCalculated_Plitt_d50c_um := 45.0;
ELSIF rCalculated_Plitt_d50c_um > 350.0 THEN
    rCalculated_Plitt_d50c_um := 350.0;
END_IF;

(* Circulating load estimate from density mass-balance *)
IF (rVoted_SlurryDensity_SG > 1.25) AND (rVoted_FreshFeedRate_tph > 500.0) THEN
    rCalculated_CirculatingLoad_Pct := ((2.85 * (rVoted_SlurryDensity_SG - 1.0)) /
                                        (rVoted_SlurryDensity_SG * (2.85 - 1.0))) *
                                       (FT_CYCLONE_FEED_FLOW_504A * rVoted_SlurryDensity_SG / rVoted_FreshFeedRate_tph) * 100.0;
ELSE
    rCalculated_CirculatingLoad_Pct := 200.0;
END_IF;
"""

print("Observers module loaded.")
