# -*- coding: utf-8 -*-
"""
Module: aluminum_potline_builder/mod_cyberphysical.py
Implements Phase 2: First-Principles Cyber-Physical State-Space Estimation,
Dynamic Pseudo-Resistance Modeling, Faradaic Mass/Energy Balances,
Early Anode Effect Slope/Curvature Observers, and Luenberger Innovation Observer.
"""

def generate_cyberphysical():
    return '''(* =====================================================================================================================
 * PHASE 2: FIRST-PRINCIPLES CYBER-PHYSICAL STATE-SPACE ESTIMATION & ELECTROCHEMICAL BALANCES
 * ===================================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------------------------
 * 1. DYNAMIC CELL PSEUDO-RESISTANCE & FILTERING
 * R_pot = (V_cell - E_emf) / I_line
 * Where E_emf = 1.650 V (pseudo-counter EMF: reversible decomposition + overpotential)
 * --------------------------------------------------------------------------------------------------------------------- *)
IF rPot_VotedLineCurrent_kA > 50.0 THEN
    (* Conversion: (V / kA) * 1000.0 = micro-Ohms *)
    rPot_CalculatedResistance_uOhm := ((rPot_VotedCellVoltage_V - c_Nominal_EMF_V) / rPot_VotedLineCurrent_kA) * 1000.0;
ELSE
    rPot_CalculatedResistance_uOhm := 5.000; (* Safe fallback when line current is tripped *)
END_IF;

(* 1st-Order Low-Pass Butterworth Filter (Cutoff ~ 1.5 Hz at 100 ms scan) *)
rPot_FilteredResistance_uOhm := (0.8650 * rPot_FilteredResistance_uOhm) + (0.1350 * rPot_CalculatedResistance_uOhm);

(* Physical Anode-Cathode Distance (ACD) Estimation based on bath resistivity and anode geometry *)
(* dR_pot / dACD = rho_bath / A_anode = 0.448 Ohm*cm / 34.80 m^2 = 0.1287 micro-Ohm/mm *)
rPot_EstAnodeCathodeDist_mm := 42.00 + ((rPot_FilteredResistance_uOhm - rSet_TargetResistance_uOhm) / c_ACD_Sensitivity_uOhm_mm);

(* Clamp estimated ACD within physical vessel limits [15.0 mm to 80.0 mm] *)
IF rPot_EstAnodeCathodeDist_mm < 15.0 THEN
    rPot_EstAnodeCathodeDist_mm := 15.0;
ELSIF rPot_EstAnodeCathodeDist_mm > 80.0 THEN
    rPot_EstAnodeCathodeDist_mm := 80.0;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * 2. CIRCULAR BUFFER & HIGH-FREQUENCY ANODE GAS BUBBLE NOISE VARIANCE
 * Captures 32 successive resistance samples to estimate CO/CO2 gas bubble coverage and polarization screening.
 * --------------------------------------------------------------------------------------------------------------------- *)
arrResRingBuffer[nRingBufferIdx] := rPot_CalculatedResistance_uOhm;
nRingBufferIdx := nRingBufferIdx + 1;
IF nRingBufferIdx >= 32 THEN
    nRingBufferIdx := 0;
    bRingBufferFilled := TRUE;
END_IF;

(* Compute rolling mean of resistance ring buffer *)
rResSum := 0.0;
FOR i := 0 TO 31 DO
    rResSum := rResSum + arrResRingBuffer[i];
END_FOR;
rResMean := rResSum / 32.0;

(* Compute sample variance (spectral signature of bubble layer in 0.5 - 2.0 Hz band) *)
rResVarianceSum := 0.0;
FOR i := 0 TO 31 DO
    rScratch1 := arrResRingBuffer[i] - rResMean;
    rResVarianceSum := rResVarianceSum + (rScratch1 * rScratch1);
END_FOR;
rResVariance := rResVarianceSum / 31.0;
rPot_BubbleNoiseVariance_uOhm2 := rResVariance;

(* Estimate bottom anode gas bubble coverage fraction [%] *)
rPot_EstGasBubbleCoverage_pct := 14.50 + (165.0 * rPot_BubbleNoiseVariance_uOhm2);
IF rPot_EstGasBubbleCoverage_pct < 5.0 THEN
    rPot_EstGasBubbleCoverage_pct := 5.0;
ELSIF rPot_EstGasBubbleCoverage_pct > 92.0 THEN
    rPot_EstGasBubbleCoverage_pct := 92.0;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * 3. ROLLING POLYNOMIAL EARLY ANODE EFFECT (AE) PREDICTIVE SLOPE OBSERVER
 * Calculates 1st derivative (dR/dt) and 2nd derivative (d2R/dt2) using a 5-point Savitzky-Golay finite difference filter.
 * --------------------------------------------------------------------------------------------------------------------- *)
rRes_k4 := rRes_k3;
rRes_k3 := rRes_k2;
rRes_k2 := rRes_k1;
rRes_k1 := rRes_k0;
rRes_k0 := rPot_FilteredResistance_uOhm;

(* 1st Derivative: dR/dt in [micro-Ohm/min] *)
IF rLocalDeltaT_s > 0.001 THEN
    rSlope_k1 := rSlope_k0;
    rSlope_k0 := (((2.0 * rRes_k0) + rRes_k1 - rRes_k3 - (2.0 * rRes_k4)) / (10.0 * rLocalDeltaT_s)) * 60.0;
    rPot_ResistanceSlope_uOhm_min := rSlope_k0;

    (* 2nd Derivative: d2R/dt2 in [micro-Ohm/s^2] (Curvature acceleration) *)
    rCurvature_k0 := (rRes_k0 - (2.0 * rRes_k1) + rRes_k2) / (rLocalDeltaT_s * rLocalDeltaT_s);
    rPot_ResistanceCurvature_uOhm_s2 := rCurvature_k0;
END_IF;

(* Early Predictive Anode Effect Detection Logic *)
IF (rPot_ResistanceSlope_uOhm_min > c_ResSlope_EarlyAE_Warn) AND (rPot_ResistanceCurvature_uOhm_s2 > c_ResCurv_EarlyAE_Warn) AND (arrX_hat[2] < 2.05) THEN
    bPot_EarlyAnodeEffectWarning := TRUE;
ELSE
    IF rPot_ResistanceSlope_uOhm_min < (c_ResSlope_EarlyAE_Warn * 0.40) AND arrX_hat[2] >= 2.20 THEN
        bPot_EarlyAnodeEffectWarning := FALSE;
    END_IF;
END_IF;

(* Critical Full-Flash Anode Effect Trip Check: Voltage spike > 7.50 V *)
IF rPot_VotedCellVoltage_V >= c_Volt_AnodeEffect_Threshold THEN
    bPot_InAnodeEffect := TRUE;
ELSE
    IF rPot_VotedCellVoltage_V < (c_Volt_Trip_HH - c_Volt_Hysteresis) THEN
        bPot_InAnodeEffect := FALSE;
    END_IF;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * 4. FARADAIC ALUMINA MASS BALANCE & CURRENT EFFICIENCY
 * Faraday's Law: m_dot_Al = (M_Al / (3 * F)) * I_line * CE
 * Alumina Consumed: m_dot_Al2O3 = (M_Al2O3 / (6 * F)) * I_line * CE
 * Constant: M_Al2O3 / (6 * F) = 0.1019613 / (6 * 96485.33) = 1.76126e-7 kg/C
 * At 500 kA = 500,000 C/s -> 0.088063 kg/s at 100% CE
 * --------------------------------------------------------------------------------------------------------------------- *)
(* Empirical Current Efficiency Model vs Temperature and Alumina Concentration *)
rInstantCurrentEfficiency := 0.9580 - (0.00065 * (rPot_VotedBathTemp_degC - 955.0)) - (0.0180 * (arrX_hat[2] - 2.45) * (arrX_hat[2] - 2.45));
IF rInstantCurrentEfficiency > 0.970 THEN
    rInstantCurrentEfficiency := 0.970;
ELSIF rInstantCurrentEfficiency < 0.820 THEN
    rInstantCurrentEfficiency := 0.820;
END_IF;
rPot_EstCurrentEfficiency_pct := rInstantCurrentEfficiency * 100.0;

(* Faradaic Alumina Consumption Rate [kg/s] *)
rAluminaConsumptionRate_kgs := 1.76126E-7 * (rPot_VotedLineCurrent_kA * 1000.0) * rInstantCurrentEfficiency;

(* Point Feeder Actual Mass Injection Rate [kg/s] *)
(* Each shot = 1.0 kg alumina; rCmd_PointFeederPulseRate_ppm in pulses/min *)
rAluminaFeedRate_kgs := (rCmd_PointFeederPulseRate_ppm * 1.000) / 60.0;

(* Net Mass Rate of Change [kg/s] *)
rNetAluminaMassRate_kgs := rAluminaFeedRate_kgs - rAluminaConsumptionRate_kgs;

(* ---------------------------------------------------------------------------------------------------------------------
 * 5. BATH CHEMISTRY EQUILIBRIUM, LIQUIDUS & SUPERHEAT ESTIMATOR
 * Solheim/Rolseth Empirical Formula for Cryolite Bath Liquidus Freezing Temperature
 * T_liq = 1011.0 + 0.50*(CR - 3.0) - 5.50*C_Al2O3 - 3.10*Excess_AlF3
 * --------------------------------------------------------------------------------------------------------------------- *)
rExcessAlF3_pct := 11.20 + (rSet_AlF3AdditionRatio_pct * 0.05);
rEstimatedLiquidus_degC := 968.50 - (5.420 * arrX_hat[2]) - (2.180 * (rExcessAlF3_pct - 10.0));
rPot_EstLiquidusTemp_degC := rEstimatedLiquidus_degC;

(* Superheat: Critical operating window is 8.0 to 18.0 deg C *)
rCalculatedSuperheat_degC := rPot_VotedBathTemp_degC - rEstimatedLiquidus_degC;
rPot_EstSuperheat_degC := rCalculatedSuperheat_degC;

(* ---------------------------------------------------------------------------------------------------------------------
 * 6. SIX-STATE DISCRETE LUENBERGER INNOVATION OBSERVER PROPAGATION
 * Model: x_hat[k+1] = A * x_hat[k] + B * u[k] + L * (y_meas - C * x_hat[k] - D * u[k])
 * Fully unrolled term-by-term matrix-vector product
 * --------------------------------------------------------------------------------------------------------------------- *)
(* Assemble Measurement Vector y_meas *)
arrY_meas[1] := rPot_VotedCellVoltage_V;
arrY_meas[2] := rPot_VotedLineCurrent_kA;
arrY_meas[3] := rPot_VotedBathTemp_degC;
arrY_meas[4] := rPot_VotedBeamPos_mm;
arrY_meas[5] := rPot_BubbleNoiseVariance_uOhm2;
arrY_meas[6] := rCathodeMetalLevel_cm;

(* Compute Synthetic Output y_est = C * x_hat + D * u *)
FOR i := 1 TO 6 DO
    arrY_est[i] := 0.0;
    FOR j := 1 TO 6 DO
        arrY_est[i] := arrY_est[i] + (arrC[i, j] * arrX_hat[j]);
    END_FOR;
    FOR j := 1 TO 5 DO
        arrY_est[i] := arrY_est[i] + (arrD[i, j] * arrU_Applied[j]);
    END_FOR;
END_FOR;

(* Compute Innovation Error: e = y_meas - y_est *)
FOR i := 1 TO 6 DO
    arrInnovation[i] := arrY_meas[i] - arrY_est[i];
END_FOR;

(* Store Previous State Vector *)
FOR i := 1 TO 6 DO
    arrX_hat_prev[i] := arrX_hat[i];
END_FOR;

(* Propagate Observer Equations Term-by-Term: arrX_hat[i] = Sum(A*x) + Sum(B*u) + Sum(L*e) *)
(* State 1: Pot Pseudo-Resistance Deviation [micro-Ohm] *)
arrX_hat[1] := (arrA[1, 1] * arrX_hat_prev[1]) + (arrA[1, 2] * arrX_hat_prev[2]) +
               (arrA[1, 3] * arrX_hat_prev[3]) + (arrA[1, 4] * arrX_hat_prev[4]) +
               (arrA[1, 5] * arrX_hat_prev[5]) + (arrA[1, 6] * arrX_hat_prev[6]) +
               (arrB[1, 1] * arrU_Applied[1])  + (arrB[1, 2] * arrU_Applied[2])  +
               (arrB[1, 3] * arrU_Applied[3])  + (arrB[1, 4] * arrU_Applied[4])  +
               (arrB[1, 5] * arrU_Applied[5])  +
               (arrL[1, 1] * arrInnovation[1]) + (arrL[1, 2] * arrInnovation[2]) +
               (arrL[1, 3] * arrInnovation[3]) + (arrL[1, 4] * arrInnovation[4]) +
               (arrL[1, 5] * arrInnovation[5]) + (arrL[1, 6] * arrInnovation[6]);

(* State 2: Dissolved Alumina Concentration [wt%] *)
arrX_hat[2] := (arrA[2, 1] * arrX_hat_prev[1]) + (arrA[2, 2] * arrX_hat_prev[2]) +
               (arrA[2, 3] * arrX_hat_prev[3]) + (arrA[2, 4] * arrX_hat_prev[4]) +
               (arrA[2, 5] * arrX_hat_prev[5]) + (arrA[2, 6] * arrX_hat_prev[6]) +
               (arrB[2, 1] * arrU_Applied[1])  + (arrB[2, 2] * arrU_Applied[2])  +
               (arrB[2, 3] * arrU_Applied[3])  + (arrB[2, 4] * arrU_Applied[4])  +
               (arrB[2, 5] * arrU_Applied[5])  +
               (arrL[2, 1] * arrInnovation[1]) + (arrL[2, 2] * arrInnovation[2]) +
               (arrL[2, 3] * arrInnovation[3]) + (arrL[2, 4] * arrInnovation[4]) +
               (arrL[2, 5] * arrInnovation[5]) + (arrL[2, 6] * arrInnovation[6]);

(* State 3: Electrolyte Bath Temperature [deg C] *)
arrX_hat[3] := (arrA[3, 1] * arrX_hat_prev[1]) + (arrA[3, 2] * arrX_hat_prev[2]) +
               (arrA[3, 3] * arrX_hat_prev[3]) + (arrA[3, 4] * arrX_hat_prev[4]) +
               (arrA[3, 5] * arrX_hat_prev[5]) + (arrA[3, 6] * arrX_hat_prev[6]) +
               (arrB[3, 1] * arrU_Applied[1])  + (arrB[3, 2] * arrU_Applied[2])  +
               (arrB[3, 3] * arrU_Applied[3])  + (arrB[3, 4] * arrU_Applied[4])  +
               (arrB[3, 5] * arrU_Applied[5])  +
               (arrL[3, 1] * arrInnovation[1]) + (arrL[3, 2] * arrInnovation[2]) +
               (arrL[3, 3] * arrInnovation[3]) + (arrL[3, 4] * arrInnovation[4]) +
               (arrL[3, 5] * arrInnovation[5]) + (arrL[3, 6] * arrInnovation[6]);

(* State 4: Anode-Cathode Distance Deviation [mm] *)
arrX_hat[4] := (arrA[4, 1] * arrX_hat_prev[1]) + (arrA[4, 2] * arrX_hat_prev[2]) +
               (arrA[4, 3] * arrX_hat_prev[3]) + (arrA[4, 4] * arrX_hat_prev[4]) +
               (arrA[4, 5] * arrX_hat_prev[5]) + (arrA[4, 6] * arrX_hat_prev[6]) +
               (arrB[4, 1] * arrU_Applied[1])  + (arrB[4, 2] * arrU_Applied[2])  +
               (arrB[4, 3] * arrU_Applied[3])  + (arrB[4, 4] * arrU_Applied[4])  +
               (arrB[4, 5] * arrU_Applied[5])  +
               (arrL[4, 1] * arrInnovation[1]) + (arrL[4, 2] * arrInnovation[2]) +
               (arrL[4, 3] * arrInnovation[3]) + (arrL[4, 4] * arrInnovation[4]) +
               (arrL[4, 5] * arrInnovation[5]) + (arrL[4, 6] * arrInnovation[6]);

(* State 5: Bottom Anode Gas Bubble Coverage Fraction [%] *)
arrX_hat[5] := (arrA[5, 1] * arrX_hat_prev[1]) + (arrA[5, 2] * arrX_hat_prev[2]) +
               (arrA[5, 3] * arrX_hat_prev[3]) + (arrA[5, 4] * arrX_hat_prev[4]) +
               (arrA[5, 5] * arrX_hat_prev[5]) + (arrA[5, 6] * arrX_hat_prev[6]) +
               (arrB[5, 1] * arrU_Applied[1])  + (arrB[5, 2] * arrU_Applied[2])  +
               (arrB[5, 3] * arrU_Applied[3])  + (arrB[5, 4] * arrU_Applied[4])  +
               (arrB[5, 5] * arrU_Applied[5])  +
               (arrL[5, 1] * arrInnovation[1]) + (arrL[5, 2] * arrInnovation[2]) +
               (arrL[5, 3] * arrInnovation[3]) + (arrL[5, 4] * arrInnovation[4]) +
               (arrL[5, 5] * arrInnovation[5]) + (arrL[5, 6] * arrInnovation[6]);

(* State 6: Liquid Metal Pad Reservoir Level [cm] *)
arrX_hat[6] := (arrA[6, 1] * arrX_hat_prev[1]) + (arrA[6, 2] * arrX_hat_prev[2]) +
               (arrA[6, 3] * arrX_hat_prev[3]) + (arrA[6, 4] * arrX_hat_prev[4]) +
               (arrA[6, 5] * arrX_hat_prev[5]) + (arrA[6, 6] * arrX_hat_prev[6]) +
               (arrB[6, 1] * arrU_Applied[1])  + (arrB[6, 2] * arrU_Applied[2])  +
               (arrB[6, 3] * arrU_Applied[3])  + (arrB[6, 4] * arrU_Applied[4])  +
               (arrB[6, 5] * arrU_Applied[5])  +
               (arrL[6, 1] * arrInnovation[1]) + (arrL[6, 2] * arrInnovation[2]) +
               (arrL[6, 3] * arrInnovation[3]) + (arrL[6, 4] * arrInnovation[4]) +
               (arrL[6, 5] * arrInnovation[5]) + (arrL[6, 6] * arrInnovation[6]);

(* Physical Saturation Clamping on Estimated States *)
IF arrX_hat[2] < 1.00 THEN arrX_hat[2] := 1.00; ELSIF arrX_hat[2] > 6.00 THEN arrX_hat[2] := 6.00; END_IF;
IF arrX_hat[3] < 880.0 THEN arrX_hat[3] := 880.0; ELSIF arrX_hat[3] > 1050.0 THEN arrX_hat[3] := 1050.0; END_IF;
IF arrX_hat[4] < 10.0 THEN arrX_hat[4] := 10.0; ELSIF arrX_hat[4] > 90.0 THEN arrX_hat[4] := 90.0; END_IF;
IF arrX_hat[5] < 2.00 THEN arrX_hat[5] := 2.00; ELSIF arrX_hat[5] > 95.0 THEN arrX_hat[5] := 95.0; END_IF;
IF arrX_hat[6] < 5.00 THEN arrX_hat[6] := 5.00; ELSIF arrX_hat[6] > 45.0 THEN arrX_hat[6] := 45.0; END_IF;

(* Route Estimated States to Block Outputs *)
rPot_EstAluminaConcentration_pct := arrX_hat[2];
rPot_EstMetalPadLevel_cm := arrX_hat[6];
'''
