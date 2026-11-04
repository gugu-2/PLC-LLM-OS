# -*- coding: utf-8 -*-
"""
Builder module for FB_Fertilizer_AmmoniumNitrate_Granulation_Scrubber
Part 3: Phase 2 - Cyber-Physical Observers & Thermochemical Balances
"""

def get_phase2_observers():
    code = """(* ============================================================================================================== *)
(* PHASE 2: CYBER-PHYSICAL STATE OBSERVERS & THERMOCHEMICAL MASS-ENERGY BALANCES                                  *)
(* ============================================================================================================== *)

(* -------------------------------------------------------------------------------------------------------------- *)
(* 2.1: GRANULE MOISTURE DESORPTION, DRYING KINETICS & DRUM BED INVENTORY OBSERVER                                *)
(* -------------------------------------------------------------------------------------------------------------- *)
(* Dynamic granular mass holdup balance inside rotary drum:                                                       *)
(* dM_bed/dt = (m_dot_slurry * X_solids + m_dot_recycle - m_dot_discharge)                                       *)
rBedHoldupEstimated_tons := rBedHoldupEstimated_tons + 
    (((rVoted_SlurryFeedPress_bar * 18.85 * 0.965) + rVoted_RecycleMassFlow_tph - (rVoted_ProductMassFlow_tph * 4.0)) * (c_rTs / 3600.0));

IF rBedHoldupEstimated_tons < 10.0 THEN
    rBedHoldupEstimated_tons := 10.0;
ELSIF rBedHoldupEstimated_tons > 75.0 THEN
    rBedHoldupEstimated_tons := 75.0;
END_IF;
rCalc_DrumGranuleHoldUp_tons := rBedHoldupEstimated_tons;

(* Non-linear Arrhenius moisture desorption rate in falling-rate drying zone *)
IF (rVoted_DrumBedTemp_degC + 273.15) > 280.0 THEN
    rArrheniusExp := -1850.0 / (rVoted_DrumBedTemp_degC + 273.15);
    rDesorptionRate := 0.0485 * EXP(rArrheniusExp) * MAX(0.0, (rGranuleMoistureInternal_pct - 0.20));
ELSE
    rDesorptionRate := 0.0;
END_IF;

(* Slurry moisture input vs evaporation integration *)
rGranuleMoistureInternal_pct := rGranuleMoistureInternal_pct + 
    ((((100.0 - 96.5) * 0.01 * rVoted_SlurryFeedPress_bar * 2.8) - (rDesorptionRate * 12.5)) * (c_rTs / 60.0));

IF rGranuleMoistureInternal_pct < 0.25 THEN
    rGranuleMoistureInternal_pct := 0.25;
ELSIF rGranuleMoistureInternal_pct > 3.80 THEN
    rGranuleMoistureInternal_pct := 3.80;
END_IF;
rCalc_EstimatedGranuleMoisture_pct := rGranuleMoistureInternal_pct;

(* -------------------------------------------------------------------------------------------------------------- *)
(* 2.2: GRANULE MECHANICAL CRUSH STRENGTH & INTERNAL VOID FRACTION (POROSITY) OBSERVER                           *)
(* -------------------------------------------------------------------------------------------------------------- *)
(* Porosity compaction model: consolidation under cascading rolling bed shear stress *)
rGranulePorosityInternal_frac := 0.035 + (0.018 * (rGranuleMoistureInternal_pct / 1.50)) + 
    (0.008 * MAX(0.0, (110.0 - rVoted_DrumBedTemp_degC) / 30.0));

IF rGranulePorosityInternal_frac < 0.020 THEN
    rGranulePorosityInternal_frac := 0.020;
ELSIF rGranulePorosityInternal_frac > 0.095 THEN
    rGranulePorosityInternal_frac := 0.095;
END_IF;
rCalc_GranulePorosity_pct := rGranulePorosityInternal_frac * 100.0;

(* Kendall / Rumpf mechanical tensile rupture strength model for spherical agglomerates:                        *)
(* F_crush = k_c * (1 - epsilon)^3 * (d^2 / (1 + 10 * omega^2))                                                  *)
rGranuleMeanDiameter_mm := rSet_TargetMeanDiameter_d50_mm;
rCalc_EstimatedCrushStrength_N := 4.85 * 
    ((1.0 - rGranulePorosityInternal_frac) * (1.0 - rGranulePorosityInternal_frac) * (1.0 - rGranulePorosityInternal_frac)) * 
    ((rGranuleMeanDiameter_mm * rGranuleMeanDiameter_mm) / (1.0 + (10.0 * (rGranuleMoistureInternal_pct * 0.01) * (rGranuleMoistureInternal_pct * 0.01))));

(* -------------------------------------------------------------------------------------------------------------- *)
(* 2.3: VIBRATORY SCREEN GRANULOMETRY & CLOSED-LOOP RECYCLE RATIO BALANCER                                       *)
(* -------------------------------------------------------------------------------------------------------------- *)
IF rVoted_ProductMassFlow_tph > 5.0 THEN
    rCalc_CalculatedRecycleRatio := rVoted_RecycleMassFlow_tph / rVoted_ProductMassFlow_tph;
ELSE
    rCalc_CalculatedRecycleRatio := rSet_TargetRecycleRatio;
END_IF;

(* First-order low-pass filtering of recycle ratio telemetry *)
rRecycleRatioFiltered := (0.92 * rRecycleRatioFiltered) + (0.08 * rCalc_CalculatedRecycleRatio);

(* Dynamic adjustment of recycle conveyor speed and cage mill crushing intensity *)
IF rRecycleRatioFiltered < rSet_TargetRecycleRatio THEN
    (* Fines depletion: increase cage mill speed to crush more oversize into seed nuclei *)
    rOut_OversizeCageMillSpeed_RPM := 850.0 + ((rSet_TargetRecycleRatio - rRecycleRatioFiltered) * 180.0);
    rOut_RecycleDragConveyorSpeed_pct := 70.0 + ((rSet_TargetRecycleRatio - rRecycleRatioFiltered) * 15.0);
ELSE
    (* Fines surplus: decelerate cage mill speed to preserve granule size spec *)
    rOut_OversizeCageMillSpeed_RPM := 850.0 - ((rRecycleRatioFiltered - rSet_TargetRecycleRatio) * 140.0);
    rOut_RecycleDragConveyorSpeed_pct := 70.0 - ((rRecycleRatioFiltered - rSet_TargetRecycleRatio) * 12.0);
END_IF;

IF rOut_OversizeCageMillSpeed_RPM > 1150.0 THEN
    rOut_OversizeCageMillSpeed_RPM := 1150.0;
ELSIF rOut_OversizeCageMillSpeed_RPM < 450.0 THEN
    rOut_OversizeCageMillSpeed_RPM := 450.0;
END_IF;

IF rOut_RecycleDragConveyorSpeed_pct > 100.0 THEN
    rOut_RecycleDragConveyorSpeed_pct := 100.0;
ELSIF rOut_RecycleDragConveyorSpeed_pct < 25.0 THEN
    rOut_RecycleDragConveyorSpeed_pct := 25.0;
END_IF;

(* -------------------------------------------------------------------------------------------------------------- *)
(* 2.4: DRYER BURNER STOICHIOMETRIC COMBUSTION & AIR-TO-FUEL RATIO (LAMBDA) CONTROL                              *)
(* -------------------------------------------------------------------------------------------------------------- *)
rCombustionStoichFlow := rVoted_BurnerGasFlow_Nm3h * c_rStoichAirToGasRatio;
IF rCombustionStoichFlow > 50.0 THEN
    rCalc_AirToFuelRatio_Lambda := rVoted_BurnerAirFlow_Nm3h / rCombustionStoichFlow;
ELSE
    rCalc_AirToFuelRatio_Lambda := c_rTargetAirFuelLambda;
END_IF;

(* Feedforward ratio control of forced draft combustion air damper *)
rCombustionAirDemand_Nm3h := rVoted_BurnerGasFlow_Nm3h * c_rStoichAirToGasRatio * c_rTargetAirFuelLambda;
IF rCombustionAirDemand_Nm3h > 18000.0 THEN
    rCombustionAirDemand_Nm3h := 18000.0;
ELSIF rCombustionAirDemand_Nm3h < 3500.0 THEN
    rCombustionAirDemand_Nm3h := 3500.0;
END_IF;

rOut_CombustionAirDamper_pct := (rCombustionAirDemand_Nm3h / 18000.0) * 100.0;
IF rOut_CombustionAirDamper_pct > 100.0 THEN rOut_CombustionAirDamper_pct := 100.0; END_IF;
IF rOut_CombustionAirDamper_pct < 20.0 THEN rOut_CombustionAirDamper_pct := 20.0; END_IF;

(* -------------------------------------------------------------------------------------------------------------- *)
(* 2.5: VENTURI SCRUBBER AEROSOL IMPACTION & 93% NITRIC ACID TRIM NEUTRALIZATION                                 *)
(* -------------------------------------------------------------------------------------------------------------- *)
(* Johnstone venturi throat inertial aerosol impaction efficiency:                                               *)
(* Psi = (C_c * rho_p * v_throat * d_p^2) / (18 * mu_g * D_throat)                                              *)
rVenturiPsiParam := (rVoted_VenturiDeltaP_mbar * 0.082) / (1.0 + (0.015 * rVoted_VenturiDeltaP_mbar));
IF rVenturiPsiParam > 0.01 THEN
    rVenturiCollectionEffEst_pct := 100.0 * (1.0 - EXP(-0.85 * SQRT(rVenturiPsiParam)));
ELSE
    rVenturiCollectionEffEst_pct := 90.0;
END_IF;

IF rVenturiCollectionEffEst_pct > 99.95 THEN
    rVenturiCollectionEffEst_pct := 99.95;
ELSIF rVenturiCollectionEffEst_pct < 85.0 THEN
    rVenturiCollectionEffEst_pct := 85.0;
END_IF;
rCalc_ScrubberAerosolCollectionEff := rVenturiCollectionEffEst_pct;

(* Hydraulic throat damper modulation to maintain target Delta P (50 mbar) *)
IF rVoted_VenturiDeltaP_mbar < rSet_TargetScrubberDeltaP_mbar THEN
    rOut_VenturiThroatDamper_pct := rOut_VenturiThroatDamper_pct + (0.45 * (rSet_TargetScrubberDeltaP_mbar - rVoted_VenturiDeltaP_mbar) * c_rTs);
ELSE
    rOut_VenturiThroatDamper_pct := rOut_VenturiThroatDamper_pct - (0.45 * (rVoted_VenturiDeltaP_mbar - rSet_TargetScrubberDeltaP_mbar) * c_rTs);
END_IF;

IF rOut_VenturiThroatDamper_pct > 95.0 THEN rOut_VenturiThroatDamper_pct := 95.0; END_IF;
IF rOut_VenturiThroatDamper_pct < 15.0 THEN rOut_VenturiThroatDamper_pct := 15.0; END_IF;

(* Non-linear acid neutralization feedback trim: NH3 + HNO3 -> NH4NO3 *)
IF rVoted_Scrubber_pH > rSet_TargetScrubber_pH THEN
    (* Alkaline ammonia slip: increase concentrated nitric acid metering *)
    rOut_NitricAcidTrimValve_pct := 35.0 + ((rVoted_Scrubber_pH - rSet_TargetScrubber_pH) * 55.0);
ELSIF rVoted_Scrubber_pH < (rSet_TargetScrubber_pH - 0.20) THEN
    (* Dangerous acidification: throttle acid trim to avoid runaway decomposition hazard *)
    rOut_NitricAcidTrimValve_pct := MAX(0.0, 35.0 - ((rSet_TargetScrubber_pH - rVoted_Scrubber_pH) * 110.0));
ELSE
    rOut_NitricAcidTrimValve_pct := 35.0;
END_IF;

IF rOut_NitricAcidTrimValve_pct > 100.0 THEN rOut_NitricAcidTrimValve_pct := 100.0; END_IF;
IF rOut_NitricAcidTrimValve_pct < 0.0 THEN rOut_NitricAcidTrimValve_pct := 0.0; END_IF;

(* -------------------------------------------------------------------------------------------------------------- *)
(* 2.6: SIL-3 SAFETY INSTRUMENTED SYSTEM (SIS) AUTOCATALYTIC RUNAWAY INTERLOCKS                                   *)
(* -------------------------------------------------------------------------------------------------------------- *)
(* Rate of rise (dT/dt) calculation with 100 ms discrete differentiator *)
rBedTempDerivFiltered_degCps := (0.75 * rBedTempDerivFiltered_degCps) + 
    (0.25 * ((rVoted_DrumBedTemp_degC - rBedTemperaturePriorCycle_degC) / c_rTs));
rBedTemperaturePriorCycle_degC := rVoted_DrumBedTemp_degC;
rCalc_ThermalRateOfRise_degCps := rBedTempDerivFiltered_degCps;
rCalc_ThermalRunawayMargin_degC := c_rCriticalRunawayTemp_degC - rVoted_DrumBedTemp_degC;

(* Fast Autocatalytic Runaway Decomposition Detection:                                                            *)
(* Criterion 1: Bed temp > 185 deg C AND dT/dt > 0.75 deg C/s (accelerating thermal runaway)                     *)
(* Criterion 2: Bed temp > 210 deg C (absolute critical runaway threshold)                                       *)
(* Criterion 3: Operator hardwired manual deluge trip                                                            *)
(* Criterion 4: Scrubber pH < 3.2 (explosive sensitizing acidification) AND Bed temp > 130 deg C                  *)
IF (rVoted_DrumBedTemp_degC >= c_rWarningRunawayTemp_degC AND rBedTempDerivFiltered_degCps >= c_rMaxAllowableRateOfRise_degCps) OR
   (rVoted_DrumBedTemp_degC >= c_rCriticalRunawayTemp_degC) OR
   (bEmergencyDelugeManualTrip) OR
   (rVoted_Scrubber_pH <= c_rTrip_Scrubber_pH_LO_LO AND rVoted_DrumBedTemp_degC >= 130.00) THEN

    bRunawayDecompositionTripped := TRUE;
    bEmergencyDelugeActive := TRUE;
    bOut_EmergencyDelugeFloodActuate := TRUE;
    bOut_SlurryEmergencyDumpValve := TRUE;
    bOut_BurnerSafetyShutoffValve_Trip := TRUE;
    bOut_NitrogenPurgeFloodValve := TRUE;
    rOut_SlurrySprayValve_pct := 0.0;
    rOut_BurnerGasThrottle_pct := 0.0;
    iFSM_CurrentState := 11; (* Direct branch to EMERGENCY_DELUGE_FLOOD_SHUTDOWN *)
END_IF;
"""
    return code
