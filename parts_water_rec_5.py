# parts_water_rec_5.py - PHASE 2: CYBER-PHYSICAL STATE ESTIMATORS & MEMBRANE MASS-TRANSFER OBSERVERS

def get_phase2_observers():
    code = []
    code.append("""(* =====================================================================================================================
 * PHASE 2: CYBER-PHYSICAL STATE ESTIMATORS & MEMBRANE MASS-TRANSFER OBSERVERS
 * Executes rigorous continuous transport physics for MABR bubbleless gas diffusion, submerged UF resistance-in-series,
 * high-pressure RO concentration polarization and osmotic pressure, isobaric ERD momentum, and UV fluence inactivation.
 * ===================================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------------------------
 * SUBSECTION 2.1: MABR BIOFILM DYNAMIC THICKNESS & BUBBLELESS OXYGEN MASS-FLUX OBSERVER
 * --------------------------------------------------------------------------------------------------------------------- *)
(* MABR gas lumen interfacial dissolved oxygen saturation based on Henry's law *)
rMABR_DO_Interface_mg_L := rMABR_Henry_O2 * (rPT_MABR_AIR_LUMEN_PRESS_104 + 1.013) * 32000.0 / (0.08206 * (rTT_WATER_INLET_TEMP_108 + 273.15));

(* Bubbleless oxygen mass transfer flux through hollow-fiber lumen wall into biofilm *)
rObs_MABR_O2_Mass_Flux_g_m2_d := rMABR_KL_Oxygen_Permeance * MAX(0.0, rMABR_DO_Interface_mg_L - rVoted_MABR_DO) * 86.4;

(* Temperature-compensated Monod nitrification rate for autotrophic nitrifiers (AOB/NOB) *)
rObs_MABR_Nitrification_Rate := rMABR_Mu_Max_AOB * EXPT(rMABR_Theta_Nitrif, (rTT_WATER_INLET_TEMP_108 - 20.0))
    * (rVoted_MABR_DO / MAX(0.01, (rMABR_K_DO_AOB + rVoted_MABR_DO)))
    * (rVoted_MABR_NH4 / MAX(0.05, (rMABR_K_NH4 + rVoted_MABR_NH4))) * 6.5;

(* Temperature-compensated Monod denitrification rate for heterotrophic denitrifiers in anoxic zone *)
rObs_MABR_Denitrification_Rate := rMABR_Mu_Max_DEN * EXPT(rMABR_Theta_Denitrif, (rTT_WATER_INLET_TEMP_108 - 20.0))
    * (rMABR_K_O2_Inhibit_DEN / MAX(0.01, (rMABR_K_O2_Inhibit_DEN + rVoted_MABR_DO)))
    * (rVoted_MABR_NO3 / MAX(0.05, (rMABR_K_NO3 + rVoted_MABR_NO3)))
    * (rAIT_MABR_COD_SOLUBLE_107 / MAX(1.0, (rMABR_K_COD + rAIT_MABR_COD_SOLUBLE_107))) * 8.0;

(* Dynamic biofilm growth, endogenous respiration decay, and crossflow shear detachment balance *)
rMABR_Lf_Deriv := (0.38 * rObs_MABR_Nitrification_Rate + 0.45 * rObs_MABR_Denitrification_Rate)
    - (rMABR_Biofilm_Decay_Rate * rMABR_Lf_Biofilm_Current_um)
    - (rMABR_Biofilm_Shear_Detach_Coeff * (rCmd_MABR_InternalRecycle_RPM / 1000.0) * rMABR_Lf_Biofilm_Current_um * rMABR_Lf_Biofilm_Current_um);

(* Numerical forward integration of biofilm boundary layer thickness *)
rMABR_Lf_Biofilm_Current_um := rMABR_Lf_Biofilm_Current_um + (rMABR_Lf_Deriv * rPar_SampleTime_Sec * 0.01);
rMABR_Lf_Biofilm_Current_um := LIMIT(50.0, rMABR_Lf_Biofilm_Current_um, 800.0);
rObs_MABR_Biofilm_Thickness_um := rMABR_Lf_Biofilm_Current_um;

(* Total Inorganic Nitrogen (TIN) in effluent *)
rObs_MABR_Total_Nitrogen_mg_L := rVoted_MABR_NH4 + rVoted_MABR_NO3;

(* ---------------------------------------------------------------------------------------------------------------------
 * SUBSECTION 2.2: SUBMERGED UF RESISTANCE-IN-SERIES MEMBRANE TRANSPORT OBSERVER
 * --------------------------------------------------------------------------------------------------------------------- *)
(* Water dynamic viscosity as a function of temperature [Pa*s] *)
rUF_Water_Viscosity_Pa_s := 0.001792 / (1.0 + (0.0337 * rTT_WATER_INLET_TEMP_108) + (0.000221 * rTT_WATER_INLET_TEMP_108 * rTT_WATER_INLET_TEMP_108));

(* Operational permeate flux calculations in LMH and m/s *)
rUF_Permeate_Flux_LMH := (rFT_UF_PERMEATE_FLOW_203 * 1000.0) / MAX(100.0, rUF_Membrane_Area_Total_m2);
rUF_Permeate_Flux_m_s := rUF_Permeate_Flux_LMH / 3600000.0;

(* Dynamic foulant cake layer resistance accumulation on outer hollow-fiber walls *)
rUF_Cake_Resistance_Accum := rUF_Cake_Resistance_Accum + (rPar_SampleTime_Sec * (
    (rUF_Specific_Cake_Resistivity * (rAIT_FEED_TSS_206 * 0.001) * rUF_Permeate_Flux_m_s * rUF_Permeate_Flux_m_s * 1.0E6)
    - (rUF_Air_Scour_Cleaning_Eff * rPT_UF_AIR_SCOUR_204 * rUF_Cake_Resistance_Accum * 0.02)
));
rUF_Cake_Resistance_Accum := LIMIT(0.0, rUF_Cake_Resistance_Accum, 1.0E13);

(* Intrinsic clean PVDF resistance and pore blocking resistance *)
rObs_UF_Intrinsic_Resistance_Rm := 1.45E12;
rObs_UF_Cake_Layer_Resistance_Rc := rUF_Cake_Resistance_Accum;
rObs_UF_Pore_Block_Resistance_Rp := 2.5E11 * (rVoted_UF_Turb / 0.05);

(* Temperature-normalized transmembrane pressure at reference 20 deg C *)
rObs_UF_Normalized_TMP_20C := rVoted_UF_TMP * (0.001002 / MAX(0.0004, rUF_Water_Viscosity_Pa_s));

(* Membrane dynamic permeability *)
rObs_UF_Dynamic_Permeability := rUF_Permeate_Flux_LMH / MAX(0.05, rObs_UF_Normalized_TMP_20C);

(* ---------------------------------------------------------------------------------------------------------------------
 * SUBSECTION 2.3: HIGH-PRESSURE RO CONCENTRATION POLARIZATION, OSMOTIC PRESSURE, & ERD MOMENTUM
 * --------------------------------------------------------------------------------------------------------------------- *)
(* Feed total dissolved solids concentration in g/L *)
rRO_TDS_Concentration_Feed_g_L := rAIT_RO_FEED_TDS_404 / 1000.0;

(* Van 't Hoff osmotic pressure calculation for feed and concentrate brine *)
rRO_Osmotic_Pressure_Feed_bar := 1.12 * rRO_TDS_Concentration_Feed_g_L * (rTT_WATER_INLET_TEMP_108 + 273.15) / 100.0;
rRO_Osmotic_Pressure_Conc_bar := rRO_Osmotic_Pressure_Feed_bar * (1.0 / MAX(0.10, 1.0 - (rSP_RO_Recovery_Rate / 100.0)));
rRO_Osmotic_Pressure_Avg_bar := 0.5 * (rRO_Osmotic_Pressure_Feed_bar + rRO_Osmotic_Pressure_Conc_bar);

(* RO permeate flux in LMH and m/s *)
rRO_Permeate_Flux_LMH := (rFT_RO_PERMEATE_FLOW_402 * 1000.0) / MAX(100.0, rRO_Membrane_Area_RO_m2);
rRO_Permeate_Flux_m_s := rRO_Permeate_Flux_LMH / 3600000.0;

(* Concentration polarization factor beta at polyamide active surface *)
rObs_RO_Concentration_Polar_Beta := EXP(rRO_Permeate_Flux_m_s / MAX(0.000005, rRO_Mass_Transfer_Coeff_k));
rObs_RO_Concentration_Polar_Beta := LIMIT(1.02, rObs_RO_Concentration_Polar_Beta, 2.50);

(* Effective Net Driving Pressure (NDP) across RO membranes *)
rObs_RO_Net_Driving_Pressure_NDP := (rVoted_RO_HP_Feed - 0.5 * (rVoted_RO_HP_Feed - rVoted_RO_Conc_Press) - 0.8)
    - (rObs_RO_Concentration_Polar_Beta * rRO_Osmotic_Pressure_Avg_bar - 0.15);
rObs_RO_Net_Driving_Pressure_NDP := MAX(1.0, rObs_RO_Net_Driving_Pressure_NDP);

(* Dynamic salt rejection percentage *)
rObs_RO_Salt_Rejection_Pct := (1.0 - (rVoted_RO_Cond / MAX(50.0, rAIT_RO_FEED_TDS_404 * 1.6))) * 100.0;
rObs_RO_Salt_Rejection_Pct := LIMIT(85.0, rObs_RO_Salt_Rejection_Pct, 99.85);

(* Isobaric Ceramic ERD Hydraulic Efficiency Calculation *)
rObs_ERD_Hydraulic_Recovery_Eff := (rPT_ERD_HP_OUT_502 * (rFT_RO_CONCENTRATE_FLOW_403 * 0.98))
    / MAX(1.0, (rVoted_ERD_HP_In * rFT_RO_CONCENTRATE_FLOW_403 + rPT_ERD_LP_IN_503 * (rFT_RO_CONCENTRATE_FLOW_403 * 0.98))) * 100.0;
rObs_ERD_Hydraulic_Recovery_Eff := LIMIT(75.0, rObs_ERD_Hydraulic_Recovery_Eff, 98.6);

(* ERD Ceramic Rotor Rotational Speed Tracking and Brine Carryover Mixing *)
rERD_Target_RPM := 2.65 * rFT_RO_CONCENTRATE_FLOW_403;
rObs_ERD_Volumetric_Brine_Mix := 1.25 + (0.0015 * rST_ERD_ROTOR_RPM_504) + (0.085 * MAX(0.0, rVoted_ERD_HP_In - rPT_ERD_HP_OUT_502));
rObs_ERD_Volumetric_Brine_Mix := LIMIT(0.5, rObs_ERD_Volumetric_Brine_Mix, 8.5);

(* Overall desalination specific energy consumption [kWh/m3] *)
rObs_RO_Specific_Energy_kWh_m3 := ((rVoted_RO_HP_Feed * (rFT_RO_PERMEATE_FLOW_402 + rFT_RO_CONCENTRATE_FLOW_403) * 100.0) / (36.0 * MAX(10.0, rFT_RO_PERMEATE_FLOW_402)))
    * (1.0 - (rObs_ERD_Hydraulic_Recovery_Eff * 0.0092));
rObs_RO_Specific_Energy_kWh_m3 := LIMIT(0.40, rObs_RO_Specific_Energy_kWh_m3, 4.50);

(* ---------------------------------------------------------------------------------------------------------------------
 * SUBSECTION 2.4: REAL-TIME SILT DENSITY INDEX (SDI-15) & UV DISINFECTION FLUENCE VALIDATION
 * --------------------------------------------------------------------------------------------------------------------- *)
(* Continuous Online Silt Density Index (SDI-15) dynamic estimator *)
rAIT_FEED_SDI15_505 := 1.85 + (14.2 * rVoted_UF_Turb) + (0.0000000000015 * rUF_Cake_Resistance_Accum);
rAIT_FEED_SDI15_505 := LIMIT(0.20, rAIT_FEED_SDI15_505, 8.50);

(* UV Transmittance at 254nm to Optical Absorbance conversion *)
rUV_Absorbance_254nm := -1.0 * (LN(MAX(0.05, rVoted_UV_Trans / 100.0)) / 2.302585);

(* Average fluence rate in annular water ring of UV reactor *)
rUV_Average_Fluence_Rate_mW_cm2 := rIIT_UV_INTENSITY_602 * (
    (1.0 - EXP(-2.302585 * rUV_Absorbance_254nm * 0.075))
    / MAX(0.005, (2.302585 * rUV_Absorbance_254nm * 0.075))
) * 0.94;

(* Hydraulic retention time in UV disinfection vessel *)
rUV_Hydraulic_Retention_Time_s := (rUV_Reactor_Volume_m3 * 3600.0) / MAX(20.0, rFT_RO_PERMEATE_FLOW_402);

(* Delivered In-Situ Fluence Dose [mJ/cm2] *)
rObs_UV_Delivered_Dose_mJ_cm2 := rUV_Average_Fluence_Rate_mW_cm2 * rUV_Hydraulic_Retention_Time_s * 0.1;
rObs_UV_Delivered_Dose_mJ_cm2 := LIMIT(0.0, rObs_UV_Delivered_Dose_mJ_cm2, 150.0);

(* EPA Long-Term 2 Enhanced Surface Water Treatment Rule Cryptosporidium/Giardia Log-Reduction *)
rObs_UV_Cryptosporidium_LogRed := 0.075 * rObs_UV_Delivered_Dose_mJ_cm2;
rObs_UV_Cryptosporidium_LogRed := LIMIT(0.0, rObs_UV_Cryptosporidium_LogRed, 5.50);
\n""")
    return "".join(code)
