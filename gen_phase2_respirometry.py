# -*- coding: utf-8 -*-
"""
Generator module: Phase 2 Respirometry and Biokinetic Observers
"""

def get_phase2_respirometry():
    return """(* =========================================================================================== *)
(* PHASE 2: RESPIROMETRIC GAS BALANCE, DARCY FILTRATION & BIOKINETIC ESTIMATORS                *)
(* =========================================================================================== *)
(* ------------------------------------------------------------------------------------------- *)
(* 1.0 HYDRODYNAMIC TRANSMEMBRANE PRESSURE (TMP) & MEMBRANE FOULING OBSERVER                   *)
(* ------------------------------------------------------------------------------------------- *)
rEst_TransmembranePressure_bar := rVoted_ATF_RetentatePress_bar - rVoted_ATF_PermeatePress_bar;

(* Dynamic TMP Rate-of-Change Monitoring [bar / min] *)
IF AI_ControllerCycleTime_s > 0.001 THEN
    rTMP_RoC_bar_per_min := (rEst_TransmembranePressure_bar - rTMP_Prev_bar) / (AI_ControllerCycleTime_s / 60.0);
    rTMP_Prev_bar := rEst_TransmembranePressure_bar;
END_IF;

(* Darcy Hollow-Fiber Hydraulic Resistance Calculation *)
(* Permeate Flux J_v = Q_perm / A_membrane [m^3 / (m^2 * s)] *)
IF (rMembraneArea_m2 > 1.0) AND (AI_PermeateHarvest_Flow_Lph > 0.1) THEN
    (* Convert L/h to m3/s: 1 L/h = 1.0E-3 / 3600 m3/s *)
    rAccumulator := (AI_PermeateHarvest_Flow_Lph * 1.0E-3) / (3600.0 * rMembraneArea_m2);
    IF (rAccumulator > 1.0E-8) AND (rPermeateViscosity_Pa_s > 1.0E-5) THEN
        (* R_total = Delta_P / (mu * J_v) where Delta_P is in Pascals (1 bar = 100,000 Pa) *)
        rEst_MembraneFoulingResistance_Rm := (rEst_TransmembranePressure_bar * 100000.0) / (rPermeateViscosity_Pa_s * rAccumulator);
    END_IF;
ELSE
    rEst_MembraneFoulingResistance_Rm := rMembraneCleanResistance_per_m;
END_IF;

(* ------------------------------------------------------------------------------------------- *)
(* 2.0 RESPIROMETRIC OFF-GAS MASS BALANCE (OUR, CER, RQ, qO2, kLa)                             *)
(* ------------------------------------------------------------------------------------------- *)
(* Total Inflow Gas Volumetric Sparge Rate [SLPM] *)
rAccumulator := AI_Sparger_Air_FlowFeedback_SLPM + AI_Sparger_O2_FlowFeedback_SLPM +
                AI_Sparger_CO2_FlowFeedback_SLPM + AI_Sparger_N2_FlowFeedback_SLPM;

IF rAccumulator > 1.0 THEN
    (* Inlet Mole Fractions *)
    rStateError := (AI_Sparger_Air_FlowFeedback_SLPM * rInletO2Fraction_Air + AI_Sparger_O2_FlowFeedback_SLPM) / rAccumulator; (* y_in_O2 *)
    rInputDiff := (AI_Sparger_Air_FlowFeedback_SLPM * rInletCO2Fraction_Air + AI_Sparger_CO2_FlowFeedback_SLPM) / rAccumulator; (* y_in_CO2 *)
    
    (* Inert Nitrogen Molar Invariance Ratio (N2 Balance Factor) *)
    (* N2_in = 1.0 - y_in_O2 - y_in_CO2; N2_out = 1.0 - y_out_O2 - y_out_CO2 *)
    IF (1.0 - (AI_OffGas_O2_MoleFraction_pct * 0.01) - (AI_OffGas_CO2_MoleFraction_pct * 0.01)) > 0.05 THEN
        rBrothDensity_kg_per_L := (1.0 - rStateError - rInputDiff) /
                                  (1.0 - (AI_OffGas_O2_MoleFraction_pct * 0.01) - (AI_OffGas_CO2_MoleFraction_pct * 0.01));
    ELSE
        rBrothDensity_kg_per_L := 1.0;
    END_IF;

    (* Molar Conversion Factor: (60 min/h * 1000 mmol/mol) / (22.414 NL/mol * V_working_L) *)
    IF rVesselWorkingVolume_L > 100.0 THEN
        rMolarVolumeGas_L_per_mol := (rAccumulator * 60.0 * 1000.0) / (22.414 * rVesselWorkingVolume_L);
        
        (* Oxygen Uptake Rate OUR [mmol/(L*h)] *)
        rEst_OxygenUptakeRate_OUR_mmol_Lh := rMolarVolumeGas_L_per_mol *
            (rStateError - rBrothDensity_kg_per_L * (AI_OffGas_O2_MoleFraction_pct * 0.01));
        IF rEst_OxygenUptakeRate_OUR_mmol_Lh < 0.1 THEN
            rEst_OxygenUptakeRate_OUR_mmol_Lh := 0.1; (* Positive definite bound *)
        END_IF;

        (* Carbon Dioxide Evolution Rate CER [mmol/(L*h)] *)
        rEst_CO2_EvolutionRate_CER_mmol_Lh := rMolarVolumeGas_L_per_mol *
            (rBrothDensity_kg_per_L * (AI_OffGas_CO2_MoleFraction_pct * 0.01) - rInputDiff);
        IF rEst_CO2_EvolutionRate_CER_mmol_Lh < 0.1 THEN
            rEst_CO2_EvolutionRate_CER_mmol_Lh := 0.1;
        END_IF;

        (* Respiratory Quotient RQ = CER / OUR [-] *)
        rEst_RespiratoryQuotient_RQ := rEst_CO2_EvolutionRate_CER_mmol_Lh / rEst_OxygenUptakeRate_OUR_mmol_Lh;

        (* Specific Cellular Oxygen Uptake Rate qO2 [pmol / (cell * h)] *)
        (* qO2 = (OUR [mmol/(L*h)] * 10^9 pmol/mmol) / (VCD [10^6 cells/mL] * 10^6 cells/mL * 1000 mL/L) *)
        IF AI_Capacitance_VCD_x10e6_per_mL > 1.0 THEN
            rEst_SpecificOxygenUptake_qO2_pmol := (rEst_OxygenUptakeRate_OUR_mmol_Lh * 1.0E9) /
                (AI_Capacitance_VCD_x10e6_per_mL * 1.0E9);
        ELSE
            rEst_SpecificOxygenUptake_qO2_pmol := rqO2_max_pmol_per_cell_h;
        END_IF;

        (* In-Situ Dynamic Oxygen Transfer Mass Coefficient kLa [1/h] *)
        (* Henry's Equilibrium Oxygen Saturation C* ~ 1.08 mmol/L at 1050 mbar, 37 C *)
        rAccumulator := 1.080 * (AI_Headspace_Pressure_mbar / 1013.25);
        rStateError := rAccumulator * (rVoted_DissolvedOxygen_pct * 0.01); (* C_L in liquid *)
        IF (rAccumulator - rStateError) > 0.05 THEN
            rEst_VolumetricMassTransfer_kLa := rEst_OxygenUptakeRate_OUR_mmol_Lh / (rAccumulator - rStateError);
        ELSE
            rEst_VolumetricMassTransfer_kLa := 35.0;
        END_IF;
    END_IF;
END_IF;

(* ------------------------------------------------------------------------------------------- *)
(* 3.0 EXTENDED MONOD CELLULAR GROWTH KINETICS & PERFUSION VOLUME INTEGRATION                  *)
(* ------------------------------------------------------------------------------------------- *)
(* Substrate limitation & product inhibition factors *)
rStateError := (AI_Raman_Glucose_g_per_L / (rKs_glc_g_per_L + AI_Raman_Glucose_g_per_L));
rInputDiff := (rKi_lac_g_per_L / (rKi_lac_g_per_L + AI_Raman_Lactate_g_per_L));
rAccumulator := (AI_Raman_Glutamine_mmol_per_L / (rKs_gln_mmol_per_L + AI_Raman_Glutamine_mmol_per_L)) *
                (rKi_amm_mmol_per_L / (rKi_amm_mmol_per_L + AI_Raman_Ammonium_mmol_per_L));

(* Specific Growth Rate mu [1/h] *)
rEst_SpecificGrowthRate_mu_per_h := (rMuMax_per_h * rStateError * rInputDiff * rAccumulator) - rK_death_per_h;
IF rEst_SpecificGrowthRate_mu_per_h < 0.0 THEN
    rEst_SpecificGrowthRate_mu_per_h := 0.0;
END_IF;

(* Total Integrated Vessel Biomass Dry Cell Weight [kg] *)
(* Assuming CHO average dry cell weight = 3.2 x 10^-13 kg/cell *)
rEst_VesselBiomassTotal_kg := (AI_Capacitance_VCD_x10e6_per_mL * 1.0E6 * 1000.0 * rVesselWorkingVolume_L * 3.2E-13);

(* Cumulative Sterile Perfusion Volume Exchanged [L] *)
IF AI_PermeateHarvest_Flow_Lph > 0.0 THEN
    rEst_CumulativePerfusionVolume_L := rEst_CumulativePerfusionVolume_L +
        (AI_PermeateHarvest_Flow_Lph * AI_ControllerCycleTime_s / 3600.0);
END_IF;
"""

print("get_phase2_respirometry ready.")
