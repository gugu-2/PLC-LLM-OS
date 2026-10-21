# Section 4: Logic Part 2 (Mass Transfer, Bubble Stripping, Corrosion Impedance)
def get_sec4_logic_p2():
    return """(* ========================================================================================= *)
(* 4.0 PYROCHEMICAL MASS TRANSFER & MULTI-PHASE SPARGER HYDRODYNAMICS                        *)
(* ========================================================================================= *)
(* Co-regulates coarse reduction via submerged metallic Beryllium (Be) rod convective flux   *)
(* and fine trimming via porous Hydrogen (H2) sparging into the bypass molten salt stream.   *)

(* --- 4.1 Beryllium Rod Dissolution Convective Mass Transfer --- *)
(* Calculate hydrodynamic Reynolds and Schmidt numbers for submerged cylinder cross-flow:   *)
(* Re_rod = (rho_salt * v_bypass * d_rod) / mu_salt                                          *)
(* Salt velocity in bypass duct: v_bypass = rSaltBypassVolFlow_m3_h / (3600.0 * Area_duct)   *)
(* With bypass duct area approx 0.015 m2 (0.138 m inner diameter)                            *)
IF rSaltBypassVolFlow_m3_h > 0.10 THEN
    rWorkVal1 := rSaltBypassVolFlow_m3_h / (3600.0 * 0.0150); (* v_bypass [m/s] *)
ELSE
    rWorkVal1 := 0.050; (* Minimum convective natural circulation [m/s] *)
END_IF;

(* Reynolds number of beryllium cylinder *)
rRe_rod := (4125.0 * rWorkVal1 * BE_ROD_DIAMETER_M) / 0.0062;
IF rRe_rod < 10.0 THEN rRe_rod := 10.0; END_IF;

(* Schmidt number for dissolved Be in fluoride eutectic: Sc = mu / (rho * D_Be) *)
rSc_Be := 0.0062 / (4125.0 * DIFFUSIVITY_BE_SALT_M2_S); (* Sc approx 289.0 *)

(* Sherwood number correlation (Churchill-Bernstein / Whitaker): *)
(* Sh_rod = 0.30 + [ 0.62 * Re^0.5 * Sc^(1/3) ] / [ 1.0 + (0.4 / Sc)^(2/3) ]^0.25 *)
rWorkVal2 := (0.62 * SQRT(rRe_rod) * 6.6115) / 1.0022; (* Sc^(1/3) approx 6.6115 *)
rSh_rod := 0.30 + rWorkVal2;

(* Convective liquid-phase mass transfer coefficient k_L_Be [m/s] *)
rk_L_Be := (rSh_rod * DIFFUSIVITY_BE_SALT_M2_S) / BE_ROD_DIAMETER_M;

(* Beryllium surface dissolution flux [mol/(m2*s)] *)
(* Dependent on fluorine oxidation potential driving force (proportional to redox error) *)
IF rRedoxError > 0.0 THEN
    rMassFlux_Be := rk_L_Be * (rRedoxError * 85.0); (* Scaling flux based on U4+ driving force *)
ELSE
    rMassFlux_Be := 0.0; (* In setpoint equilibrium or slightly reducing *)
END_IF;

(* Cumulative Beryllium mass consumption tracking [grams] *)
(* dM/dt = J_Be * Area_exposed * MW_Be (MW_Be = 9.01218 g/mol) *)
IF rBeRodPositionFeedback_mm > 1.0 THEN
    rWorkVal3 := PI_CONST * BE_ROD_DIAMETER_M * (rBeRodPositionFeedback_mm * 0.0010); (* Area [m2] *)
    rCumulativeBerylliumBurn_grams := rCumulativeBerylliumBurn_grams +
        (rMassFlux_Be * rWorkVal3 * 9.01218 * tSampleTaskInterval_s);
END_IF;

(* --- 4.2 Hydrogen Gas Sparger Two-Film Interfacial Mass Transfer --- *)
(* Gas sparging delivery: 3% H2 in He carrier gas.                                          *)
(* Reaction: 1/2 H2(g) + UF4(salt) <===> UF3(salt) + HF(g)                                  *)
(* Interfacial specific area: a = 6.0 * alpha_sparge / d32                                   *)
IF rH2SpargerFlowFeedback_sccm > 5.0 THEN
    (* Gas volume fraction in sparger mixing zone *)
    rWorkVal4 := (rH2SpargerFlowFeedback_sccm * 1.6667e-8) / (rWorkVal1 * 0.0150);
    IF rWorkVal4 > 0.15 THEN rWorkVal4 := 0.15; END_IF;
    ra_sparge := (6.0 * rWorkVal4) / SAUTER_BUBBLE_DIAM_M;
ELSE
    ra_sparge := 10.0; (* Minimum residual interfacial area *)
END_IF;

(* Mass transfer coefficient for dissolved hydrogen *)
rk_L_H2 := 1.450e-4; (* Characteristic k_L for H2 in molten fluorides at 650°C [m/s] *)
rFlux_H2 := rk_L_H2 * ra_sparge * (rH2SpargerFlowFeedback_sccm / 1200.0);


(* ========================================================================================= *)
(* 5.0 FISSION GAS (Xe/Kr) BUBBLE NUCLEATION, STRIPPING & CYCLONIC EXTRACTION               *)
(* ========================================================================================= *)
(* Models helium microbubble injection into the fuel salt slipstream, mass transfer of       *)
(* insoluble volatile fission products (Xe-135, Kr-88) into the bubbles, and subsequent      *)
(* centrifugal separation in an axial cyclone with strict gas void carryunder limits.        *)

(* Mass transfer coefficient for Xenon stripping: Higbie penetration model *)
(* k_L_Xe = 2.0 * SQRT( (D_Xe * v_bubble_slip) / (pi * d32) )                              *)
(* Characteristic slip velocity of 0.85 mm helium bubble in molten salt: v_slip approx 0.18 m/s *)
rk_L_Xe := 2.0 * SQRT( (DIFFUSIVITY_XE_SALT_M2_S * 0.180) / (PI_CONST * SAUTER_BUBBLE_DIAM_M) );

(* Specific bubble interfacial area for Helium stripping injection *)
IF rHeStrippingFlowFeedback_sccm > 50.0 THEN
    rWorkVal1 := (rHeStrippingFlowFeedback_sccm * 1.6667e-8) / (rWorkVal1 * 0.0150);
    IF rWorkVal1 > 0.12 THEN rWorkVal1 := 0.12; END_IF;
    ra_bubble := (6.0 * rWorkVal1) / SAUTER_BUBBLE_DIAM_M;
ELSE
    ra_bubble := 5.0;
END_IF;

(* Volumetric removal rate of Xenon: dC_Xe/dt = - k_L_Xe * a_bubble * (C_Xe - C_sat) *)
rXeRemovalRate := rk_L_Xe * ra_bubble;

(* Centrifugal Separator G-force and Separation Efficiency *)
(* Tangential velocity inside axial cyclone barrel: v_tangential = (Q_bypass / A_inlet)     *)
(* G = v_tangential^2 / (R_cyclone * 9.81)                                                  *)
IF rSaltBypassVolFlow_m3_h > 0.50 THEN
    rWorkVal2 := (rSaltBypassVolFlow_m3_h / 3600.0) / 0.0028; (* v_tangential [m/s] *)
    rCentrifugalG := (rWorkVal2 * rWorkVal2) / (CYCLONE_RADIUS_M * 9.80665);
    IF rCentrifugalG < 15.0 THEN rCentrifugalG := 15.0; END_IF;
    IF rCentrifugalG > 180.0 THEN rCentrifugalG := 180.0; END_IF;
ELSE
    rCentrifugalG := 15.0;
END_IF;

(* Cyclone bubble separation efficiency modeling *)
rSepEfficiency := 1.0 - EXP( - (rCentrifugalG * 0.0450) );
IF rSepEfficiency > 0.998 THEN rSepEfficiency := 0.998; END_IF;
IF rSepEfficiency < 0.750 THEN rSepEfficiency := 0.750; END_IF;

rXeExtractionEfficiency_pct := rSepEfficiency * 100.0;

(* Carryunder Gas Void Fraction returning to core loop *)
(* Void carryunder = injected gas void * (1.0 - rSepEfficiency) * throttle_factor *)
rWorkVal3 := (1.0 - rSepEfficiency) * (rHeStrippingFlowFeedback_sccm / 5000.0) * 0.85;
IF rCycloneThrottleCmd_pct > 10.0 THEN
    rGasVoidCalculated := rWorkVal3 * (100.0 / rCycloneThrottleCmd_pct);
ELSE
    rGasVoidCalculated := rWorkVal3 * 10.0;
END_IF;

(* Clamp and smooth void fraction *)
IF rGasVoidCalculated < 0.001 THEN rGasVoidCalculated := 0.001; END_IF;
IF rGasVoidCalculated > 0.500 THEN rGasVoidCalculated := 0.500; END_IF;

rFiltVoidFraction_pct := (alpha_VoidFilter * rGasVoidCalculated) +
                         ((1.0 - alpha_VoidFilter) * rFiltVoidFraction_pct);
rCalculatedVoidFraction_pct := rFiltVoidFraction_pct;

(* Void Fraction Alarm Boundaries *)
IF rCalculatedVoidFraction_pct > 0.120 THEN
    dwWarningWord := dwWarningWord OR 16#0000_0040; (* Warning: High gas void fraction *)
END_IF;


(* ========================================================================================= *)
(* 6.0 STRUCTURAL NICKEL ALLOY (HASTELLOY-N) CORROSION IMPEDANCE & MICROSTRAIN KINETICS     *)
(* ========================================================================================= *)
(* High-temperature in-situ Electrochemical Impedance Spectroscopy (EIS) evaluation:         *)
(* Extracts polarization resistance Rp, applies Stern-Geary to obtain corrosion current     *)
(* density i_corr, and computes Faradaic wall thinning rate CR [um/year].                    *)

(* Protect against zero/invalid polarization resistance *)
IF rEIS_PolarizationResist_Ohm > 100.0 THEN
    (* Polarization resistance corrected for solution resistance: Rp_corr = Rp - Rs *)
    rWorkVal1 := rEIS_PolarizationResist_Ohm - rEIS_SolutionResistance_Ohm;
    IF rWorkVal1 < 50.0 THEN rWorkVal1 := 50.0; END_IF;
    
    (* Stern-Geary equation for corrosion current density: i_corr = B / Rp [A/cm2] *)
    rI_corr_A_cm2 := STERN_GEARY_B_VOLT / rWorkVal1;
    rI_corr_uA_cm2 := rI_corr_A_cm2 * 1.0e6; (* Convert to uA/cm2 *)
    
    (* Faradaic corrosion rate: CR [um/year] = (i_corr * EW * 3.1536e7) / (rho * F) * 1.0e4 *)
    (* (EW * 3.1536e7 * 1.0e4) / (rho * F) for Hastelloy-N = (28.52 * 3.1536e11) / (8.86 * 96485.33) = 10515.6 *)
    rCorrosionRate_calc := rI_corr_A_cm2 * 10515.6 * 1.0e4;
ELSE
    (* Fallback estimation based on U4+/U3+ redox ratio and dissolved Cr *)
    rCorrosionRate_calc := 2.50 + (rCalculatedU4U3Ratio * 0.0850) + (rDissolvedChromium_ppm * 0.0350);
END_IF;

(* Bound and filter corrosion rate *)
IF rCorrosionRate_calc < 0.10 THEN rCorrosionRate_calc := 0.10; END_IF;
IF rCorrosionRate_calc > 120.0 THEN rCorrosionRate_calc := 120.0; END_IF;

rFiltCorrosionRate_um_yr := (alpha_CorrosionFilter * rCorrosionRate_calc) +
                            ((1.0 - alpha_CorrosionFilter) * rFiltCorrosionRate_um_yr);
rCorrosionRate_um_yr := rFiltCorrosionRate_um_yr;

(* High Corrosion Rate Warning *)
IF rCorrosionRate_um_yr > 15.0 THEN
    dwWarningWord := dwWarningWord OR 16#0000_0080; (* Warning: Hastelloy corrosion rate high *)
END_IF;

(* Filter and monitor reactor vessel wall hoop microstrain *)
rWorkVal2 := (rVesselWallMicrostrain_CH1 + rVesselWallMicrostrain_CH2) * 0.50;
rFiltVesselMicrostrain := (alpha_StrainFilter * rWorkVal2) +
                          ((1.0 - alpha_StrainFilter) * rFiltVesselMicrostrain);

IF rFiltVesselMicrostrain > 1200.0 THEN
    dwWarningWord := dwWarningWord OR 16#0000_0100; (* Warning: Vessel hoop microstrain elevated *)
END_IF;
"""

if __name__ == "__main__":
    s = get_sec4_logic_p2()
    print("Section 4 Length:", len(s))
