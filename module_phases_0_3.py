# module_phases_0_3.py
# Contains Phase 0 (Safety), Phase 1 (2oo3 TMR), Phase 2 (Off-gas), Phase 3 (Hydrodynamics)

def get_phase0_safety():
    return """(* ================================================================================================== *)
(* === PHASE 0: CRITICAL SAFETY INTERLOCKS & MASTER HARDWARE PERMISSIVES ===                          *)
(* ================================================================================================== *)
IF NOT bEmergencyStopOk OR NOT bSterileBarrierOk THEN
    rCmd_MFC_O2_Micro_sLpm          := 0.0;
    rCmd_MFC_Air_Micro_sLpm         := 0.0;
    rCmd_MFC_Air_Macro_sLpm         := 0.0;
    rCmd_MFC_CO2_Macro_sLpm         := 0.0;
    rCmd_MFC_N2_Macro_sLpm          := 0.0;
    rCmd_AgitatorSpeed_rpm          := 0.0;
    rCmd_TCU_HeatingPower_kW        := 0.0;
    rCmd_TCU_CoolingValve_Pct       := 100.0; (* Fail-safe full cooling to quench exotherm *)
    rCmd_PerfusionFeedPump_Lph      := 0.0;
    rCmd_PermeateHarvestPump_Lph    := 0.0;
    rCmd_CellBleedPump_Lph          := 0.0;
    rCmd_BasePeristalticPump_mLph   := 0.0;
    bCmd_AntifoamDosePulse          := FALSE;
    bCmd_TFF_BackflushValve         := FALSE;
    bSystemHealthy                  := FALSE;
    bCriticalAlarmSummary           := TRUE;
    iActiveFSMState                 := 12;    (* Force transition to System Standby *)
    dwAlarmWord_1                   := dwAlarmWord_1 OR 16#80000000; (* Bit 31: Emergency Stop Trip *)
    RETURN;
END_IF;
"""

def get_phase1_tmr():
    return """(* ================================================================================================== *)
(* === PHASE 1: TRIPLE MODULAR REDUNDANCY (2oo3 TMR) SENSOR VOTING ALGORITHMS ===                    *)
(* ================================================================================================== *)
(* 1.1 Dissolved Oxygen Optical Probes 2oo3 Voting *)
tTimer_DO_Discrep1(IN := (ABS(rDO_Probe1_Pct - rDO_Probe2_Pct) > c_rTMR_DO_Tol_Pct) AND (ABS(rDO_Probe1_Pct - rDO_Probe3_Pct) > c_rTMR_DO_Tol_Pct), PT := T#5S);
tTimer_DO_Discrep2(IN := (ABS(rDO_Probe2_Pct - rDO_Probe1_Pct) > c_rTMR_DO_Tol_Pct) AND (ABS(rDO_Probe2_Pct - rDO_Probe3_Pct) > c_rTMR_DO_Tol_Pct), PT := T#5S);
tTimer_DO_Discrep3(IN := (ABS(rDO_Probe3_Pct - rDO_Probe1_Pct) > c_rTMR_DO_Tol_Pct) AND (ABS(rDO_Probe3_Pct - rDO_Probe2_Pct) > c_rTMR_DO_Tol_Pct), PT := T#5S);

IF tTimer_DO_Discrep1.Q THEN bDO_Probe1_Degraded := TRUE; END_IF;
IF tTimer_DO_Discrep2.Q THEN bDO_Probe2_Degraded := TRUE; END_IF;
IF tTimer_DO_Discrep3.Q THEN bDO_Probe3_Degraded := TRUE; END_IF;

IF NOT bDO_Probe1_Degraded AND NOT bDO_Probe2_Degraded AND NOT bDO_Probe3_Degraded THEN
    (* All 3 probes healthy: Exact Median Selection *)
    IF (rDO_Probe1_Pct >= rDO_Probe2_Pct AND rDO_Probe1_Pct <= rDO_Probe3_Pct) OR (rDO_Probe1_Pct <= rDO_Probe2_Pct AND rDO_Probe1_Pct >= rDO_Probe3_Pct) THEN
        rVoted_DO_Pct := rDO_Probe1_Pct;
    ELSIF (rDO_Probe2_Pct >= rDO_Probe1_Pct AND rDO_Probe2_Pct <= rDO_Probe3_Pct) OR (rDO_Probe2_Pct <= rDO_Probe1_Pct AND rDO_Probe2_Pct >= rDO_Probe3_Pct) THEN
        rVoted_DO_Pct := rDO_Probe2_Pct;
    ELSE
        rVoted_DO_Pct := rDO_Probe3_Pct;
    END_IF;
    bDO_SystemFault := FALSE;
ELSIF bDO_Probe1_Degraded AND NOT bDO_Probe2_Degraded AND NOT bDO_Probe3_Degraded THEN
    rVoted_DO_Pct := (rDO_Probe2_Pct + rDO_Probe3_Pct) / 2.0;
ELSIF bDO_Probe2_Degraded AND NOT bDO_Probe1_Degraded AND NOT bDO_Probe3_Degraded THEN
    rVoted_DO_Pct := (rDO_Probe1_Pct + rDO_Probe3_Pct) / 2.0;
ELSIF bDO_Probe3_Degraded AND NOT bDO_Probe1_Degraded AND NOT bDO_Probe2_Degraded THEN
    rVoted_DO_Pct := (rDO_Probe1_Pct + rDO_Probe2_Pct) / 2.0;
ELSE
    (* Two or more probes failed: Trip 2oo3 Critical Sensor Fault *)
    bDO_SystemFault := TRUE;
    dwAlarmWord_2 := dwAlarmWord_2 OR 16#00000001; (* Bit 0: DO TMR Triple Failure *)
END_IF;

(* 1.2 Broth pH Combined Optical/Electrochemical Probes 2oo3 Voting *)
tTimer_PH_Discrep1(IN := (ABS(rPH_Probe1_pH - rPH_Probe2_pH) > c_rTMR_PH_Tol_pH) AND (ABS(rPH_Probe1_pH - rPH_Probe3_pH) > c_rTMR_PH_Tol_pH), PT := T#5S);
tTimer_PH_Discrep2(IN := (ABS(rPH_Probe2_pH - rPH_Probe1_pH) > c_rTMR_PH_Tol_pH) AND (ABS(rPH_Probe2_pH - rPH_Probe3_pH) > c_rTMR_PH_Tol_pH), PT := T#5S);
tTimer_PH_Discrep3(IN := (ABS(rPH_Probe3_pH - rPH_Probe1_pH) > c_rTMR_PH_Tol_pH) AND (ABS(rPH_Probe3_pH - rPH_Probe2_pH) > c_rTMR_PH_Tol_pH), PT := T#5S);

IF tTimer_PH_Discrep1.Q THEN bPH_Probe1_Degraded := TRUE; END_IF;
IF tTimer_PH_Discrep2.Q THEN bPH_Probe2_Degraded := TRUE; END_IF;
IF tTimer_PH_Discrep3.Q THEN bPH_Probe3_Degraded := TRUE; END_IF;

IF NOT bPH_Probe1_Degraded AND NOT bPH_Probe2_Degraded AND NOT bPH_Probe3_Degraded THEN
    IF (rPH_Probe1_pH >= rPH_Probe2_pH AND rPH_Probe1_pH <= rPH_Probe3_pH) OR (rPH_Probe1_pH <= rPH_Probe2_pH AND rPH_Probe1_pH >= rPH_Probe3_pH) THEN
        rVoted_PH := rPH_Probe1_pH;
    ELSIF (rPH_Probe2_pH >= rPH_Probe1_pH AND rPH_Probe2_pH <= rPH_Probe3_pH) OR (rPH_Probe2_pH <= rPH_Probe1_pH AND rPH_Probe2_pH >= rPH_Probe3_pH) THEN
        rVoted_PH := rPH_Probe2_pH;
    ELSE
        rVoted_PH := rPH_Probe3_pH;
    END_IF;
    bPH_SystemFault := FALSE;
ELSIF bPH_Probe1_Degraded AND NOT bPH_Probe2_Degraded AND NOT bPH_Probe3_Degraded THEN
    rVoted_PH := (rPH_Probe2_pH + rPH_Probe3_pH) / 2.0;
ELSIF bPH_Probe2_Degraded AND NOT bPH_Probe1_Degraded AND NOT bPH_Probe3_Degraded THEN
    rVoted_PH := (rPH_Probe1_pH + rPH_Probe3_pH) / 2.0;
ELSIF bPH_Probe3_Degraded AND NOT bPH_Probe1_Degraded AND NOT bPH_Probe2_Degraded THEN
    rVoted_PH := (rPH_Probe1_pH + rPH_Probe2_pH) / 2.0;
ELSE
    bPH_SystemFault := TRUE;
    dwAlarmWord_2 := dwAlarmWord_2 OR 16#00000002; (* Bit 1: pH TMR Triple Failure *)
END_IF;

(* 1.3 Skid Load Cell Weight Transmitters 2oo3 Voting *)
tTimer_Weight_Discrep1(IN := (ABS(rVesselWeight1_kg - rVesselWeight2_kg) > c_rTMR_Weight_Tol_kg) AND (ABS(rVesselWeight1_kg - rVesselWeight3_kg) > c_rTMR_Weight_Tol_kg), PT := T#5S);
tTimer_Weight_Discrep2(IN := (ABS(rVesselWeight2_kg - rVesselWeight1_kg) > c_rTMR_Weight_Tol_kg) AND (ABS(rVesselWeight2_kg - rVesselWeight3_kg) > c_rTMR_Weight_Tol_kg), PT := T#5S);
tTimer_Weight_Discrep3(IN := (ABS(rVesselWeight3_kg - rVesselWeight1_kg) > c_rTMR_Weight_Tol_kg) AND (ABS(rVesselWeight3_kg - rVesselWeight2_kg) > c_rTMR_Weight_Tol_kg), PT := T#5S);

IF tTimer_Weight_Discrep1.Q THEN bWeight_Cell1_Degraded := TRUE; END_IF;
IF tTimer_Weight_Discrep2.Q THEN bWeight_Cell2_Degraded := TRUE; END_IF;
IF tTimer_Weight_Discrep3.Q THEN bWeight_Cell3_Degraded := TRUE; END_IF;

IF NOT bWeight_Cell1_Degraded AND NOT bWeight_Cell2_Degraded AND NOT bWeight_Cell3_Degraded THEN
    IF (rVesselWeight1_kg >= rVesselWeight2_kg AND rVesselWeight1_kg <= rVesselWeight3_kg) OR (rVesselWeight1_kg <= rVesselWeight2_kg AND rVesselWeight1_kg >= rVesselWeight3_kg) THEN
        rVoted_Weight_kg := rVesselWeight1_kg;
    ELSIF (rVesselWeight2_kg >= rVesselWeight1_kg AND rVesselWeight2_kg <= rVesselWeight3_kg) OR (rVesselWeight2_kg <= rVesselWeight1_kg AND rVesselWeight2_kg >= rVesselWeight3_kg) THEN
        rVoted_Weight_kg := rVesselWeight2_kg;
    ELSE
        rVoted_Weight_kg := rVesselWeight3_kg;
    END_IF;
    bWeight_SystemFault := FALSE;
ELSIF bWeight_Cell1_Degraded AND NOT bWeight_Cell2_Degraded AND NOT bWeight_Cell3_Degraded THEN
    rVoted_Weight_kg := (rVesselWeight2_kg + rVesselWeight3_kg) / 2.0;
ELSIF bWeight_Cell2_Degraded AND NOT bWeight_Cell1_Degraded AND NOT bWeight_Cell3_Degraded THEN
    rVoted_Weight_kg := (rVesselWeight1_kg + rVesselWeight3_kg) / 2.0;
ELSIF bWeight_Cell3_Degraded AND NOT bWeight_Cell1_Degraded AND NOT bWeight_Cell2_Degraded THEN
    rVoted_Weight_kg := (rVesselWeight1_kg + rVesselWeight2_kg) / 2.0;
ELSE
    bWeight_SystemFault := TRUE;
    dwAlarmWord_2 := dwAlarmWord_2 OR 16#00000004; (* Bit 2: Weight TMR Triple Failure *)
END_IF;

(* 1.4 Permeate Pressure Transducers 2oo3 Voting *)
tTimer_Perm_Discrep1(IN := (ABS(rPermeatePress1_mbar - rPermeatePress2_mbar) > c_rTMR_Press_Tol_mbar) AND (ABS(rPermeatePress1_mbar - rPermeatePress3_mbar) > c_rTMR_Press_Tol_mbar), PT := T#5S);
tTimer_Perm_Discrep2(IN := (ABS(rPermeatePress2_mbar - rPermeatePress1_mbar) > c_rTMR_Press_Tol_mbar) AND (ABS(rPermeatePress2_mbar - rPermeatePress3_mbar) > c_rTMR_Press_Tol_mbar), PT := T#5S);
tTimer_Perm_Discrep3(IN := (ABS(rPermeatePress3_mbar - rPermeatePress1_mbar) > c_rTMR_Press_Tol_mbar) AND (ABS(rPermeatePress3_mbar - rPermeatePress2_mbar) > c_rTMR_Press_Tol_mbar), PT := T#5S);

IF tTimer_Perm_Discrep1.Q THEN bPerm_Trans1_Degraded := TRUE; END_IF;
IF tTimer_Perm_Discrep2.Q THEN bPerm_Trans2_Degraded := TRUE; END_IF;
IF tTimer_Perm_Discrep3.Q THEN bPerm_Trans3_Degraded := TRUE; END_IF;

IF NOT bPerm_Trans1_Degraded AND NOT bPerm_Trans2_Degraded AND NOT bPerm_Trans3_Degraded THEN
    IF (rPermeatePress1_mbar >= rPermeatePress2_mbar AND rPermeatePress1_mbar <= rPermeatePress3_mbar) OR (rPermeatePress1_mbar <= rPermeatePress2_mbar AND rPermeatePress1_mbar >= rPermeatePress3_mbar) THEN
        rVoted_PermPress_mbar := rPermeatePress1_mbar;
    ELSIF (rPermeatePress2_mbar >= rPermeatePress1_mbar AND rPermeatePress2_mbar <= rPermeatePress3_mbar) OR (rPermeatePress2_mbar <= rPermeatePress1_mbar AND rPermeatePress2_mbar >= rPermeatePress3_mbar) THEN
        rVoted_PermPress_mbar := rPermeatePress2_mbar;
    ELSE
        rVoted_PermPress_mbar := rPermeatePress3_mbar;
    END_IF;
    bPerm_SystemFault := FALSE;
ELSIF bPerm_Trans1_Degraded AND NOT bPerm_Trans2_Degraded AND NOT bPerm_Trans3_Degraded THEN
    rVoted_PermPress_mbar := (rPermeatePress2_mbar + rPermeatePress3_mbar) / 2.0;
ELSIF bPerm_Trans2_Degraded AND NOT bPerm_Trans1_Degraded AND NOT bPerm_Trans3_Degraded THEN
    rVoted_PermPress_mbar := (rPermeatePress1_mbar + rPermeatePress3_mbar) / 2.0;
ELSIF bPerm_Trans3_Degraded AND NOT bPerm_Trans1_Degraded AND NOT bPerm_Trans2_Degraded THEN
    rVoted_PermPress_mbar := (rPermeatePress1_mbar + rPermeatePress2_mbar) / 2.0;
ELSE
    bPerm_SystemFault := TRUE;
    dwAlarmWord_2 := dwAlarmWord_2 OR 16#00000008; (* Bit 3: Permeate Press TMR Triple Failure *)
END_IF;
"""

def get_phase2_offgas():
    return """(* ================================================================================================== *)
(* === PHASE 2: OFF-GAS SPECTROMETRY & METABOLIC RATE TRACKING (OUR, CER, RQ) ===                     *)
(* ================================================================================================== *)
rTotalInletGas_sLpm := rCmd_MFC_O2_Micro_sLpm + rCmd_MFC_Air_Micro_sLpm + rCmd_MFC_Air_Macro_sLpm + rCmd_MFC_CO2_Macro_sLpm + rCmd_MFC_N2_Macro_sLpm;
IF rTotalInletGas_sLpm < 0.10 THEN
    rTotalInletGas_sLpm := 0.10; (* Prevent division by zero during minimal gas purge *)
END_IF;

rFraction_O2_In  := (rCmd_MFC_O2_Micro_sLpm + (0.20946 * (rCmd_MFC_Air_Micro_sLpm + rCmd_MFC_Air_Macro_sLpm))) / rTotalInletGas_sLpm;
rFraction_CO2_In := (rCmd_MFC_CO2_Macro_sLpm + (0.00042 * (rCmd_MFC_Air_Micro_sLpm + rCmd_MFC_Air_Macro_sLpm))) / rTotalInletGas_sLpm;
rFraction_N2_In  := (rCmd_MFC_N2_Macro_sLpm + (0.78084 * (rCmd_MFC_Air_Micro_sLpm + rCmd_MFC_Air_Macro_sLpm))) / rTotalInletGas_sLpm;

rFraction_O2_Out  := rOffGas_O2_Pct / 100.0;
rFraction_CO2_Out := rOffGas_CO2_Pct / 100.0;
rFraction_N2_Out  := 1.0 - (rFraction_O2_Out + rFraction_CO2_Out);
IF rFraction_N2_Out < 0.10 THEN
    rFraction_N2_Out := 0.10;
END_IF;

(* Inert gas (N2) balance correction factor *)
rInertGasRatio := rFraction_N2_In / rFraction_N2_Out;

(* Reconcile working broth liquid volume from voted skid gross mass *)
rCalc_VesselVolume_L := (rVoted_Weight_kg - 65.0) / (c_rBrothDensity_kg_m3 / 1000.0);
IF rCalc_VesselVolume_L < 50.0 THEN
    rCalc_VesselVolume_L := 50.0; (* Physical heel limit *)
END_IF;

(* Molar sparge gas inlet flow rate [mol/h] *)
rMolarInletGas_mol_h := (rTotalInletGas_sLpm * 60.0) / c_rMolarGasVol_L_mol;

(* Oxygen Uptake Rate (OUR) & Carbon Dioxide Evolution Rate (CER) in [mmol/(L*h)] *)
rCalc_OUR_mmol_L_h := (rMolarInletGas_mol_h / rCalc_VesselVolume_L) * (rFraction_O2_In - (rFraction_O2_Out * rInertGasRatio)) * 1000.0;
rCalc_CER_mmol_L_h := (rMolarInletGas_mol_h / rCalc_VesselVolume_L) * ((rFraction_CO2_Out * rInertGasRatio) - rFraction_CO2_In) * 1000.0;

IF rCalc_OUR_mmol_L_h < 0.0 THEN rCalc_OUR_mmol_L_h := 0.0; END_IF;
IF rCalc_CER_mmol_L_h < 0.0 THEN rCalc_CER_mmol_L_h := 0.0; END_IF;

(* Metabolic Respiratory Quotient (RQ) *)
IF rCalc_OUR_mmol_L_h > 0.05 THEN
    rCalc_RQ := rCalc_CER_mmol_L_h / rCalc_OUR_mmol_L_h;
ELSE
    rCalc_RQ := 1.00;
END_IF;

(* Biomass Viable Cell Density (VCD) multi-frequency observer *)
rCalc_VCD_Estimated := (rBiomassPermittivity_pF_cm * 1.95) + ((rCalc_OUR_mmol_L_h * 24.0) / (c_rMuMax_h_inv * 0.220 + 0.005)) * 0.15;
IF rCalc_VCD_Estimated < 0.10 THEN
    rCalc_VCD_Estimated := 0.10;
END_IF;

(* Cell-Specific metabolic rates [pmol/(cell*day)] *)
rSpecific_qO2_pmol_cell_d  := (rCalc_OUR_mmol_L_h * 24.0) / rCalc_VCD_Estimated;
rSpecific_qCO2_pmol_cell_d := (rCalc_CER_mmol_L_h * 24.0) / rCalc_VCD_Estimated;
"""

def get_phase3_hydrodynamics():
    return """(* ================================================================================================== *)
(* === PHASE 3: HYDRODYNAMICS & HOLLOW-FIBER MEMBRANE HYDRAULICS ===                                  *)
(* ================================================================================================== *)
rRevPerSec := rAgitatorSpeedFeedback_rpm / 60.0;
rCalc_TipSpeed_m_s := c_rPi * c_rImpellerDia_m * rRevPerSec;

(* Agitator Power Dissipation P = Np * rho * N^3 * Di^5 [W] *)
rAgitatorPower_W := c_rImpellerNp * c_rBrothDensity_kg_m3 * (rRevPerSec * rRevPerSec * rRevPerSec) * (c_rImpellerDia_m * c_rImpellerDia_m * c_rImpellerDia_m * c_rImpellerDia_m * c_rImpellerDia_m);
IF rAgitatorPower_W < 0.10 THEN
    rAgitatorPower_W := 0.10;
END_IF;

(* Specific power input P/V in [W/m^3] *)
rCalc_PowerPerVolume_W_m3 := rAgitatorPower_W / (rCalc_VesselVolume_L * 0.001);

(* Dynamic Reynolds Number & Turbulent Eddy Kolmogorov Microscale *)
rKinematicVisc_m2_s := c_rBrothViscosity_Pa_s / c_rBrothDensity_kg_m3;
rReynoldsNum := (c_rBrothDensity_kg_m3 * rRevPerSec * c_rImpellerDia_m * c_rImpellerDia_m) / c_rBrothViscosity_Pa_s;
rTurbulentDissipation_W_kg := rAgitatorPower_W / (rCalc_VesselVolume_L * c_rBrothDensity_kg_m3 * 0.001);

IF rTurbulentDissipation_W_kg > 0.00001 THEN
    rCalc_KolmogorovScale_um := (((rKinematicVisc_m2_s * rKinematicVisc_m2_s * rKinematicVisc_m2_s) / rTurbulentDissipation_W_kg) ** 0.25) * 1.0E6;
ELSE
    rCalc_KolmogorovScale_um := 150.0;
END_IF;

(* Superficial Gas Velocity vs [m/s] and Volumetric Oxygen Transfer Coefficient kLa [h^-1] *)
rSuperficialGasVel_m_s := (rTotalInletGas_sLpm * 0.001 / 60.0) / c_rVesselCrossSection_m2;
rCalc_kLa_h_inv := 0.0260 * (rCalc_PowerPerVolume_W_m3 ** 0.52) * ((rSuperficialGasVel_m_s * 1000.0) ** 0.65) * 3600.0;
IF rCalc_kLa_h_inv < 1.0 THEN
    rCalc_kLa_h_inv := 1.0;
END_IF;

(* TFF Hollow-Fiber Membrane Hydraulics & Transmembrane Pressure (TMP) *)
rCalc_TMP_mbar := ((rFeedPress_mbar + rRetentatePress_mbar) / 2.0) - rVoted_PermPress_mbar;
IF rCalc_TMP_mbar < 0.0 THEN
    rCalc_TMP_mbar := 0.0;
END_IF;

rPermeateFlux_LMH := rCmd_PermeateHarvestPump_Lph / c_rFilterArea_m2;
IF rPermeateFlux_LMH > 0.05 THEN
    rCalc_MembraneResistance_1e11 := (rCalc_TMP_mbar * 100.0) / (c_rBrothViscosity_Pa_s * (rPermeateFlux_LMH / 3.6E6)) * 1.0E-11;
ELSE
    rCalc_MembraneResistance_1e11 := c_rCleanMembraneRes_1e11;
END_IF;

(* Hollow-Fiber Lumen Wall Shear Rate gamma = 4*Q / (pi * r^3 * N_fibers) [s^-1] *)
rRetentateCircFlow_m3_s := (rRetentateCircFlow_Lph * 0.001) / 3600.0;
rLumenAreaTotal_m2 := c_rFilterFiberCount * c_rPi * (c_rFilterFiberRadius_m * c_rFilterFiberRadius_m);
rRetentateVelocity_m_s := rRetentateCircFlow_m3_s / rLumenAreaTotal_m2;
rCalc_ShearRate_s_inv := (4.0 * rRetentateCircFlow_m3_s) / (c_rPi * (c_rFilterFiberRadius_m * c_rFilterFiberRadius_m * c_rFilterFiberRadius_m) * c_rFilterFiberCount);
"""
