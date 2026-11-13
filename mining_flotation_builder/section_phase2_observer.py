# mining_flotation_builder/section_phase2_observer.py
"""
Section: Phase 2 - First-Principles Flotation Kinetics & State-Space Observer
Function Block: FB_Mining_Flotation_RougherScavenger_FrothDepth_ReagentDosing
"""

def get_phase2_code():
    return """(* ========================================================================= *)
(* === PHASE 2: FIRST-PRINCIPLES CYBER-PHYSICAL FLOTATION KINETICS       === *)
(* ===          MULTIPHASE HYDRODYNAMICS & STATE-SPACE OBSERVER          === *)
(* ========================================================================= *)

(* ------------------------------------------------------------------------- *)
(* SUB-SECTION 2.1: MULTIPHASE HYDRODYNAMICS & BUBBLE SURFACE AREA FLUX     *)
(* ------------------------------------------------------------------------- *)
(* Physical conversions to SI base units *)
IF rMeanBubbleDiameter_Vision > 0.1 THEN
    rMeanBubbleDiameter_M := rMeanBubbleDiameter_Vision * 0.001; (* [mm] -> [m] *)
ELSE
    rMeanBubbleDiameter_M := 0.0018; (* Fallback Sauter mean diameter: 1.8 mm *)
END_IF;

(* Reconcile Superficial Gas Velocity Jg [m/s] from blower mass flow and cell area *)
IF rCellCrossSectionArea_M2 > 1.0 THEN
    (* Jg = Q_air / (3600 * Area) *)
    rSuperficialGasVelocity_M_S := (rAirMassFlow / 3600.0) / rCellCrossSectionArea_M2;
ELSE
    rSuperficialGasVelocity_M_S := 0.015;
END_IF;

(* Clamp superficial gas velocity to realistic physical operating limits [m/s] *)
IF rSuperficialGasVelocity_M_S < 0.002 THEN
    rSuperficialGasVelocity_M_S := 0.002;
ELSIF rSuperficialGasVelocity_M_S > 0.045 THEN
    rSuperficialGasVelocity_M_S := 0.045;
END_IF;
rCalculated_SuperficialGas_Jg := rSuperficialGasVelocity_M_S * 100.0; (* [m/s] -> [cm/s] *)

(* Bubble Surface Area Flux: Sb = 6 * Jg / d32 [1/s] (Gorain, Franzidis & Manlapig) *)
IF rMeanBubbleDiameter_M > 0.0001 THEN
    rBubbleSurfaceAreaFlux_Sb := (6.0 * rSuperficialGasVelocity_M_S) / rMeanBubbleDiameter_M;
ELSE
    rBubbleSurfaceAreaFlux_Sb := 45.0;
END_IF;
rCalculated_BubbleAreaFlux_Sb := rBubbleSurfaceAreaFlux_Sb;

(* Slurry Inflow & Density Conversions *)
rSlurryDensity_SI := rVoted_SlurryDensity; (* [kg/m3] *)
IF rFeedVolumetricFlow > 10.0 THEN
    rSlurryVolumetricFlow_M3_S := rFeedVolumetricFlow / 3600.0; (* [m3/h] -> [m3/s] *)
ELSE
    rSlurryVolumetricFlow_M3_S := 0.25; (* Fallback 900 m3/h *)
END_IF;

(* Impeller Reynolds Number: Re = (rho * N * D^2) / mu *)
rSlurryReynoldsNumber := (rSlurryDensity_SI * (rAgitatorSpeed_Actual / 60.0) * (rRotorDiameter_M * rRotorDiameter_M)) / rSlurryApparentViscosity_PaS;

(* Bubble Slip Reynolds Number: Re_b = (rho * v_slip * d_b) / mu *)
rBubbleReynoldsNumber := (rSlurryDensity_SI * 0.22 * rMeanBubbleDiameter_M) / rSlurryApparentViscosity_PaS;
IF rBubbleReynoldsNumber < 0.1 THEN rBubbleReynoldsNumber := 0.1; END_IF;

(* ------------------------------------------------------------------------- *)
(* SUB-SECTION 2.2: PROBABILISTIC MINERAL FLOTATION SUB-PROCESS KINETICS     *)
(* ------------------------------------------------------------------------- *)
(* 1. Collision Probability Pc (Weber-Paddock intermediate Reynolds model) *)
(* Pc = (3/2) * (dp / db)^2 * [ 1 + (3/16) * Reb / (1 + 0.249 * Reb^0.56) ] *)
rTempDelta := (rMineralParticleDiameter_M / rMeanBubbleDiameter_M);
IF rTempDelta > 0.005 THEN rTempDelta := 0.005; END_IF;

rTempSum := 1.0 + ((0.1875 * rBubbleReynoldsNumber) / (1.0 + (0.249 * SQRT(rBubbleReynoldsNumber))));
rProbabilityCollision_Pc := 1.5 * (rTempDelta * rTempDelta) * rTempSum * 1800.0;
IF rProbabilityCollision_Pc < 0.02 THEN rProbabilityCollision_Pc := 0.02;
ELSIF rProbabilityCollision_Pc > 0.85 THEN rProbabilityCollision_Pc := 0.85; END_IF;
rCalculated_CollisionProb_Pc := rProbabilityCollision_Pc;

(* 2. Attachment Probability Pa (Contact angle & collector coverage model) *)
(* Pa increases with xanthate dosage and alkaline lime pH activation *)
rTempSum := (u_act[3] / 100.0) * 1.85; (* Collector stroke contribution *)
rTempDelta := (rVoted_PulpPH - 9.0) * 0.45; (* Lime alkalinity activation *)
IF rTempDelta < 0.0 THEN rTempDelta := 0.0; END_IF;
rProbabilityAttachment_Pa := 0.35 + (0.42 * (rTempSum / (1.0 + rTempSum))) + (0.15 * (rTempDelta / (1.0 + rTempDelta)));
IF rProbabilityAttachment_Pa < 0.10 THEN rProbabilityAttachment_Pa := 0.10;
ELSIF rProbabilityAttachment_Pa > 0.95 THEN rProbabilityAttachment_Pa := 0.95; END_IF;
rCalculated_AttachmentProb_Pa := rProbabilityAttachment_Pa;

(* 3. Froth Zone Recovery Factor Rf = (1.0 - Ed) (Savassi / Finch Froth Model) *)
(* Deeper froth increases residence time of mineralized bubbles, promoting drainage *)
(* Rf = 1.0 / (1.0 + beta * H_froth / v_air) *)
rFrothResidenceTime_Sec := (rVoted_FrothThickness * 0.001) / (rSuperficialGasVelocity_M_S + 0.001);
rProbabilityDetachment_Ed := 1.0 - (1.0 / (1.0 + (0.045 * rFrothResidenceTime_Sec)));
IF rProbabilityDetachment_Ed < 0.05 THEN rProbabilityDetachment_Ed := 0.05;
ELSIF rProbabilityDetachment_Ed > 0.75 THEN rProbabilityDetachment_Ed := 0.75; END_IF;

rFrothDropBackFactor_Rf := 1.0 - rProbabilityDetachment_Ed;
rCalculated_FrothRecovery_Rf := rFrothDropBackFactor_Rf;

(* 4. Overall Flotation Rate Constant: k = Sb * Pc * Pa * Rf [1/s] *)
rFlotationRateConstant_k := rBubbleSurfaceAreaFlux_Sb * rProbabilityCollision_Pc * rProbabilityAttachment_Pa * rFrothDropBackFactor_Rf * 0.0125;
IF rFlotationRateConstant_k < 0.0005 THEN rFlotationRateConstant_k := 0.0005;
ELSIF rFlotationRateConstant_k > 0.0850 THEN rFlotationRateConstant_k := 0.0850; END_IF;

rFlotationRateConstant_k_Min := rFlotationRateConstant_k * 60.0; (* [1/min] *)
rCalculated_FlotationRate_k := rFlotationRateConstant_k_Min;

(* 5. Dynamic Hydrodynamic Slurry Residence Time Tres *)
(* V_active = Area * (PulpLevel / 1000) * (1 - AirHoldup) *)
rTempSum := (rCellCrossSectionArea_M2 * (rVoted_PulpLevel * 0.001)) * (1.0 - (x_hat[6] * 0.01));
IF rSlurryVolumetricFlow_M3_S > 0.05 THEN
    rHydrodynamicResTime_Sec := rTempSum / rSlurryVolumetricFlow_M3_S;
ELSE
    rHydrodynamicResTime_Sec := 600.0;
END_IF;
rHydrodynamicResTime_Min := rHydrodynamicResTime_Sec / 60.0;
rCalculated_HydrodynamicResTime := rHydrodynamicResTime_Min;

(* 6. Theoretical Recovery: R = Rmax * (1.0 - exp(-k * Tres)) *)
rTempDelta := -1.0 * rFlotationRateConstant_k * rHydrodynamicResTime_Sec;
IF rTempDelta < -8.0 THEN rTempDelta := -8.0; END_IF;
rModelCalculatedRecovery := rMaxTheoreticalRecovery_Rmax * (1.0 - EXP(rTempDelta)) * 100.0;
IF rModelCalculatedRecovery < 5.0 THEN rModelCalculatedRecovery := 5.0;
ELSIF rModelCalculatedRecovery > 98.5 THEN rModelCalculatedRecovery := 98.5; END_IF;

(* ------------------------------------------------------------------------- *)
(* SUB-SECTION 2.3: INTER-CELL DART VALVE TORRICELLI HYDRAULIC DISCHARGE     *)
(* ------------------------------------------------------------------------- *)
(* Torricelli equation: Q = Cv * (u / 100) * sqrt(2 * g * Delta_H) *)
rTempSum := MAX(50.0, rVoted_PulpLevel - 2000.0) * 0.001; (* Available hydrostatic head in meters *)
rTempDelta := SQRT(2.0 * 9.80665 * rTempSum); (* Velocity head sqrt(2*g*h) *)

rDartValve1_FlowM3H := rDartValve1_CvMax * (rDartValve1_Position_FB * 0.01) * rTempDelta * 0.2778;
rDartValve2_FlowM3H := rDartValve2_CvMax * (rDartValve2_Position_FB * 0.01) * rTempDelta * 0.2778;
rTotalTailingsDischargeFlow := rDartValve1_FlowM3H + rDartValve2_FlowM3H;
rNetHydraulicMassBalanceDelta := rFeedVolumetricFlow - rTotalTailingsDischargeFlow;

(* ------------------------------------------------------------------------- *)
(* SUB-SECTION 2.4: MACHINE VISION FROTH SPECTRAL PROCESSING & GRADE MODEL   *)
(* ------------------------------------------------------------------------- *)
(* Spectral copper index: (Red - Blue) / (Red + Blue + 0.001) *)
rSpectralCopperIndex := (rFrothColor_Red - rFrothColor_Blue) / (rFrothColor_Red + rFrothColor_Blue + 0.001);

(* Optical Cu grade regression: Grade = f(SpectralIndex, BubbleCollapse, FrothBed, Velocity) *)
rVisionEstimatedGrade_Cu := 14.50 +
                            (18.25 * rSpectralCopperIndex) +
                            (0.045 * rVoted_FrothThickness) -
                            (0.125 * rFrothVelocity_Vision) -
                            (0.085 * rBubbleCollapseRate_Vision);
IF rVisionEstimatedGrade_Cu < 5.0 THEN rVisionEstimatedGrade_Cu := 5.0;
ELSIF rVisionEstimatedGrade_Cu > 42.0 THEN rVisionEstimatedGrade_Cu := 42.0; END_IF;

(* ------------------------------------------------------------------------- *)
(* SUB-SECTION 2.5: REAGENT DOSING FEEDFORWARD RATIO CONTROLLERS            *)
(* ------------------------------------------------------------------------- *)
(* 1. Potassium Amyl Xanthate (PAX) Collector Dynamic Cascade *)
(* Specific dosage [g/t dry ore] modulated by feed Cu grade and throughput *)
rTempSum := 1.0 + (0.45 * ((rFeedGrade_Cu - 1.20) / 1.20));
IF rTempSum < 0.60 THEN rTempSum := 0.60; ELSIF rTempSum > 2.20 THEN rTempSum := 2.20; END_IF;
rPAX_TonnageRatio_Dynamic := rPAX_BaseRatio_SP * rTempSum;
rCalculated_PAX_SpecificDose := rPAX_TonnageRatio_Dynamic;
rPAX_MassFlowTarget_KgH := (rPAX_TonnageRatio_Dynamic * rFeedDryTonnage) * 0.001;

(* 2. Methyl Isobutyl Carbinol (MIBC) Frother Dynamic Cascade *)
(* Specific dosage [g/t dry ore] modulated by superficial gas velocity and bubble collapse *)
rTempSum := 1.0 + (0.35 * ((rCalculated_SuperficialGas_Jg - 1.50) / 1.50)) + (0.25 * ((rBubbleCollapseRate_Vision - 15.0) / 50.0));
IF rTempSum < 0.50 THEN rTempSum := 0.50; ELSIF rTempSum > 2.50 THEN rTempSum := 2.50; END_IF;
rMIBC_TonnageRatio_Dynamic := rMIBC_BaseRatio_SP * rTempSum;
rCalculated_MIBC_SpecificDose := rMIBC_TonnageRatio_Dynamic;
rMIBC_MassFlowTarget_KgH := (rMIBC_TonnageRatio_Dynamic * rFeedDryTonnage) * 0.001;

(* 3. Milk of Lime Neutralization Slurry Flow *)
(* Non-linear acid-base titration mapping for pyrite suppression *)
rTempDelta := MAX(0.0, rTargetPH_SP - rVoted_PulpPH);
rLimeVolumetricDose_LPH := (rTempDelta * rLimeTitrationGain) * (1.0 + (0.65 * (rFeedPyriteContent_Pct / 15.0))) * (rFeedDryTonnage / 1000.0);
rCalculated_Lime_SlurryFlow := rLimeVolumetricDose_LPH * 0.001; (* [m3/h] *)

(* ------------------------------------------------------------------------- *)
(* SUB-SECTION 2.6: DISCRETE STATE-SPACE OBSERVER INNOVATION & PROPAGATION   *)
(* y_meas = [PulpLevel, FrothDepth, pH, ModelRecovery, VisionGrade, AirHoldup]*)
(* ------------------------------------------------------------------------- *)
y_meas[1] := rVoted_PulpLevel;
y_meas[2] := rVoted_FrothThickness;
y_meas[3] := rVoted_PulpPH;
y_meas[4] := rModelCalculatedRecovery;
y_meas[5] := rVisionEstimatedGrade_Cu;
y_meas[6] := (rCalculated_SuperficialGas_Jg * 5.85) / (rCalculated_SuperficialGas_Jg + 1.25);

(* 1. Compute Output Estimation y_est = C * x_hat + D * u *)
y_est[1] := (C_Matrix[1, 1] * x_hat[1]) + (C_Matrix[1, 2] * x_hat[2]) + (C_Matrix[1, 3] * x_hat[3]) + (C_Matrix[1, 4] * x_hat[4]) + (C_Matrix[1, 5] * x_hat[5]) + (C_Matrix[1, 6] * x_hat[6]) +
            (D_Matrix[1, 1] * u_act[1]) + (D_Matrix[1, 2] * u_act[2]) + (D_Matrix[1, 3] * u_act[3]) + (D_Matrix[1, 4] * u_act[4]) + (D_Matrix[1, 5] * u_act[5]);

y_est[2] := (C_Matrix[2, 1] * x_hat[1]) + (C_Matrix[2, 2] * x_hat[2]) + (C_Matrix[2, 3] * x_hat[3]) + (C_Matrix[2, 4] * x_hat[4]) + (C_Matrix[2, 5] * x_hat[5]) + (C_Matrix[2, 6] * x_hat[6]) +
            (D_Matrix[2, 1] * u_act[1]) + (D_Matrix[2, 2] * u_act[2]) + (D_Matrix[2, 3] * u_act[3]) + (D_Matrix[2, 4] * u_act[4]) + (D_Matrix[2, 5] * u_act[5]);

y_est[3] := (C_Matrix[3, 1] * x_hat[1]) + (C_Matrix[3, 2] * x_hat[2]) + (C_Matrix[3, 3] * x_hat[3]) + (C_Matrix[3, 4] * x_hat[4]) + (C_Matrix[3, 5] * x_hat[5]) + (C_Matrix[3, 6] * x_hat[6]) +
            (D_Matrix[3, 1] * u_act[1]) + (D_Matrix[3, 2] * u_act[2]) + (D_Matrix[3, 3] * u_act[3]) + (D_Matrix[3, 4] * u_act[4]) + (D_Matrix[3, 5] * u_act[5]);

y_est[4] := (C_Matrix[4, 1] * x_hat[1]) + (C_Matrix[4, 2] * x_hat[2]) + (C_Matrix[4, 3] * x_hat[3]) + (C_Matrix[4, 4] * x_hat[4]) + (C_Matrix[4, 5] * x_hat[5]) + (C_Matrix[4, 6] * x_hat[6]) +
            (D_Matrix[4, 1] * u_act[1]) + (D_Matrix[4, 2] * u_act[2]) + (D_Matrix[4, 3] * u_act[3]) + (D_Matrix[4, 4] * u_act[4]) + (D_Matrix[4, 5] * u_act[5]);

y_est[5] := (C_Matrix[5, 1] * x_hat[1]) + (C_Matrix[5, 2] * x_hat[2]) + (C_Matrix[5, 3] * x_hat[3]) + (C_Matrix[5, 4] * x_hat[4]) + (C_Matrix[5, 5] * x_hat[5]) + (C_Matrix[5, 6] * x_hat[6]) +
            (D_Matrix[5, 1] * u_act[1]) + (D_Matrix[5, 2] * u_act[2]) + (D_Matrix[5, 3] * u_act[3]) + (D_Matrix[5, 4] * u_act[4]) + (D_Matrix[5, 5] * u_act[5]);

y_est[6] := (C_Matrix[6, 1] * x_hat[1]) + (C_Matrix[6, 2] * x_hat[2]) + (C_Matrix[6, 3] * x_hat[3]) + (C_Matrix[6, 4] * x_hat[4]) + (C_Matrix[6, 5] * x_hat[5]) + (C_Matrix[6, 6] * x_hat[6]) +
            (D_Matrix[6, 1] * u_act[1]) + (D_Matrix[6, 2] * u_act[2]) + (D_Matrix[6, 3] * u_act[3]) + (D_Matrix[6, 4] * u_act[4]) + (D_Matrix[6, 5] * u_act[5]);

(* 2. Compute Innovation Residual y_innov = y_meas - y_est *)
y_innov[1] := y_meas[1] - y_est[1];
y_innov[2] := y_meas[2] - y_est[2];
y_innov[3] := y_meas[3] - y_est[3];
y_innov[4] := y_meas[4] - y_est[4];
y_innov[5] := y_meas[5] - y_est[5];
y_innov[6] := y_meas[6] - y_est[6];

(* 3. Compute Innovation Corrected State Vector x_corr = x_hat + L * y_innov *)
x_corr[1] := x_hat[1] + (L_Gain[1, 1] * y_innov[1]) + (L_Gain[1, 2] * y_innov[2]) + (L_Gain[1, 3] * y_innov[3]) + (L_Gain[1, 4] * y_innov[4]) + (L_Gain[1, 5] * y_innov[5]) + (L_Gain[1, 6] * y_innov[6]);
x_corr[2] := x_hat[2] + (L_Gain[2, 1] * y_innov[1]) + (L_Gain[2, 2] * y_innov[2]) + (L_Gain[2, 3] * y_innov[3]) + (L_Gain[2, 4] * y_innov[4]) + (L_Gain[2, 5] * y_innov[5]) + (L_Gain[2, 6] * y_innov[6]);
x_corr[3] := x_hat[3] + (L_Gain[3, 1] * y_innov[1]) + (L_Gain[3, 2] * y_innov[2]) + (L_Gain[3, 3] * y_innov[3]) + (L_Gain[3, 4] * y_innov[4]) + (L_Gain[3, 5] * y_innov[5]) + (L_Gain[3, 6] * y_innov[6]);
x_corr[4] := x_hat[4] + (L_Gain[4, 1] * y_innov[1]) + (L_Gain[4, 2] * y_innov[2]) + (L_Gain[4, 3] * y_innov[3]) + (L_Gain[4, 4] * y_innov[4]) + (L_Gain[4, 5] * y_innov[5]) + (L_Gain[4, 6] * y_innov[6]);
x_corr[5] := x_hat[5] + (L_Gain[5, 1] * y_innov[1]) + (L_Gain[5, 2] * y_innov[2]) + (L_Gain[5, 3] * y_innov[3]) + (L_Gain[5, 4] * y_innov[4]) + (L_Gain[5, 5] * y_innov[5]) + (L_Gain[5, 6] * y_innov[6]);
x_corr[6] := x_hat[6] + (L_Gain[6, 1] * y_innov[1]) + (L_Gain[6, 2] * y_innov[2]) + (L_Gain[6, 3] * y_innov[3]) + (L_Gain[6, 4] * y_innov[4]) + (L_Gain[6, 5] * y_innov[5]) + (L_Gain[6, 6] * y_innov[6]);

(* 4. State Propagation to Next Scan: x_hat_next = A * x_corr + B * u *)
x_hat_next[1] := (A_Matrix[1, 1] * x_corr[1]) + (A_Matrix[1, 2] * x_corr[2]) + (A_Matrix[1, 3] * x_corr[3]) + (A_Matrix[1, 4] * x_corr[4]) + (A_Matrix[1, 5] * x_corr[5]) + (A_Matrix[1, 6] * x_corr[6]) +
                 (B_Matrix[1, 1] * u_act[1]) + (B_Matrix[1, 2] * u_act[2]) + (B_Matrix[1, 3] * u_act[3]) + (B_Matrix[1, 4] * u_act[4]) + (B_Matrix[1, 5] * u_act[5]);

x_hat_next[2] := (A_Matrix[2, 1] * x_corr[1]) + (A_Matrix[2, 2] * x_corr[2]) + (A_Matrix[2, 3] * x_corr[3]) + (A_Matrix[2, 4] * x_corr[4]) + (A_Matrix[2, 5] * x_corr[5]) + (A_Matrix[2, 6] * x_corr[6]) +
                 (B_Matrix[2, 1] * u_act[1]) + (B_Matrix[2, 2] * u_act[2]) + (B_Matrix[2, 3] * u_act[3]) + (B_Matrix[2, 4] * u_act[4]) + (B_Matrix[2, 5] * u_act[5]);

x_hat_next[3] := (A_Matrix[3, 1] * x_corr[1]) + (A_Matrix[3, 2] * x_corr[2]) + (A_Matrix[3, 3] * x_corr[3]) + (A_Matrix[3, 4] * x_corr[4]) + (A_Matrix[3, 5] * x_corr[5]) + (A_Matrix[3, 6] * x_corr[6]) +
                 (B_Matrix[3, 1] * u_act[1]) + (B_Matrix[3, 2] * u_act[2]) + (B_Matrix[3, 3] * u_act[3]) + (B_Matrix[3, 4] * u_act[4]) + (B_Matrix[3, 5] * u_act[5]);

x_hat_next[4] := (A_Matrix[4, 1] * x_corr[1]) + (A_Matrix[4, 2] * x_corr[2]) + (A_Matrix[4, 3] * x_corr[3]) + (A_Matrix[4, 4] * x_corr[4]) + (A_Matrix[4, 5] * x_corr[5]) + (A_Matrix[4, 6] * x_corr[6]) +
                 (B_Matrix[4, 1] * u_act[1]) + (B_Matrix[4, 2] * u_act[2]) + (B_Matrix[4, 3] * u_act[3]) + (B_Matrix[4, 4] * u_act[4]) + (B_Matrix[4, 5] * u_act[5]);

x_hat_next[5] := (A_Matrix[5, 1] * x_corr[1]) + (A_Matrix[5, 2] * x_corr[2]) + (A_Matrix[5, 3] * x_corr[3]) + (A_Matrix[5, 4] * x_corr[4]) + (A_Matrix[5, 5] * x_corr[5]) + (A_Matrix[5, 6] * x_corr[6]) +
                 (B_Matrix[5, 1] * u_act[1]) + (B_Matrix[5, 2] * u_act[2]) + (B_Matrix[5, 3] * u_act[3]) + (B_Matrix[5, 4] * u_act[4]) + (B_Matrix[5, 5] * u_act[5]);

x_hat_next[6] := (A_Matrix[6, 1] * x_corr[1]) + (A_Matrix[6, 2] * x_corr[2]) + (A_Matrix[6, 3] * x_corr[3]) + (A_Matrix[6, 4] * x_corr[4]) + (A_Matrix[6, 5] * x_corr[5]) + (A_Matrix[6, 6] * x_corr[6]) +
                 (B_Matrix[6, 1] * u_act[1]) + (B_Matrix[6, 2] * u_act[2]) + (B_Matrix[6, 3] * u_act[3]) + (B_Matrix[6, 4] * u_act[4]) + (B_Matrix[6, 5] * u_act[5]);

(* Clamp states to physical boundaries *)
IF x_hat_next[1] < 1000.0 THEN x_hat_next[1] := 1000.0; ELSIF x_hat_next[1] > 4400.0 THEN x_hat_next[1] := 4400.0; END_IF;
IF x_hat_next[2] < 20.0 THEN x_hat_next[2] := 20.0; ELSIF x_hat_next[2] > 800.0 THEN x_hat_next[2] := 800.0; END_IF;
IF x_hat_next[3] < 4.0 THEN x_hat_next[3] := 4.0; ELSIF x_hat_next[3] > 13.5 THEN x_hat_next[3] := 13.5; END_IF;
IF x_hat_next[4] < 5.0 THEN x_hat_next[4] := 5.0; ELSIF x_hat_next[4] > 99.0 THEN x_hat_next[4] := 99.0; END_IF;
IF x_hat_next[5] < 3.0 THEN x_hat_next[5] := 3.0; ELSIF x_hat_next[5] > 45.0 THEN x_hat_next[5] := 45.0; END_IF;
IF x_hat_next[6] < 1.0 THEN x_hat_next[6] := 1.0; ELSIF x_hat_next[6] > 32.0 THEN x_hat_next[6] := 32.0; END_IF;

(* Update persistent state estimate for next scan *)
x_hat[1] := x_hat_next[1];
x_hat[2] := x_hat_next[2];
x_hat[3] := x_hat_next[3];
x_hat[4] := x_hat_next[4];
x_hat[5] := x_hat_next[5];
x_hat[6] := x_hat_next[6];

(* Assign observer outputs to block interface *)
rEstimated_Cu_Recovery := x_corr[4];
rEstimated_Cu_Grade := x_corr[5];
rEstimated_AirHoldup_Pct := x_corr[6];

(* Gold Co-Recovery Estimation: Chalcopyrite and electrum gold association *)
rEstimated_Au_Recovery := x_corr[4] * (0.885 + (0.015 * (x_corr[3] - 10.0)) + (0.0025 * (x_corr[5] - 25.0)));
IF rEstimated_Au_Recovery < 5.0 THEN rEstimated_Au_Recovery := 5.0;
ELSIF rEstimated_Au_Recovery > 96.0 THEN rEstimated_Au_Recovery := 96.0; END_IF;
"""
