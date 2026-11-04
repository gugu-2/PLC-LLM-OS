# -*- coding: utf-8 -*-
"""
Part 4: Phase 3 (Cyber-Physical Observers) and Phase 4 (Discrete State-Space Prediction)
for FB_Chemicals_Hydrocracker_TrickleBed_HydrogenQuench
"""

def get_observers_and_statespace_block():
    return """(* ==========================================================================================
 * PHASE 3: CYBER-PHYSICAL REACTION KINETIC, THERMODYNAMIC & HYDRODYNAMIC OBSERVERS
 * ========================================================================================== *)

(* --- 3.1 REAL-TIME TEMPERATURE DERIVATIVES & RUNAWAY HOTSPOT DETECTION --- *)
(* Shift rolling history circular buffers for five consecutive scans *)
rTempBed1_Hist[5] := rTempBed1_Hist[4];
rTempBed1_Hist[4] := rTempBed1_Hist[3];
rTempBed1_Hist[3] := rTempBed1_Hist[2];
rTempBed1_Hist[2] := rTempBed1_Hist[1];
rTempBed1_Hist[1] := rTMR1_VotedVal;

rTempBed2_Hist[5] := rTempBed2_Hist[4];
rTempBed2_Hist[4] := rTempBed2_Hist[3];
rTempBed2_Hist[3] := rTempBed2_Hist[2];
rTempBed2_Hist[2] := rTempBed2_Hist[1];
rTempBed2_Hist[1] := rTMR2_VotedVal;

rTempBed3_Hist[5] := rTempBed3_Hist[4];
rTempBed3_Hist[4] := rTempBed3_Hist[3];
rTempBed3_Hist[3] := rTempBed3_Hist[2];
rTempBed3_Hist[2] := rTempBed3_Hist[1];
rTempBed3_Hist[1] := rTMR3_VotedVal;

rTempBed4_Hist[5] := rTempBed4_Hist[4];
rTempBed4_Hist[4] := rTempBed4_Hist[3];
rTempBed4_Hist[3] := rTempBed4_Hist[2];
rTempBed4_Hist[2] := rTempBed4_Hist[1];
rTempBed4_Hist[1] := rTMR4_VotedVal;

rPressInlet_Hist[5] := rPressInlet_Hist[4];
rPressInlet_Hist[4] := rPressInlet_Hist[3];
rPressInlet_Hist[3] := rPressInlet_Hist[2];
rPressInlet_Hist[2] := rPressInlet_Hist[1];
rPressInlet_Hist[1] := rTMR7_VotedVal;

(* Calculate first-order finite-difference temperature rate of change [deg C/min] *)
IF rDeltaTime_s > 0.001 THEN
    rObserved_Bed1_dTdt_degCmin := ((rTMR1_VotedVal - rTempBed1_Hist[5]) / (4.0 * rDeltaTime_s)) * 60.0;
    rObserved_Bed2_dTdt_degCmin := ((rTMR2_VotedVal - rTempBed2_Hist[5]) / (4.0 * rDeltaTime_s)) * 60.0;
    rObserved_Bed3_dTdt_degCmin := ((rTMR3_VotedVal - rTempBed3_Hist[5]) / (4.0 * rDeltaTime_s)) * 60.0;
    rObserved_Bed4_dTdt_degCmin := ((rTMR4_VotedVal - rTempBed4_Hist[5]) / (4.0 * rDeltaTime_s)) * 60.0;
    rDepressurizationRate_bar_min := ((rPressInlet_Hist[5] - rTMR7_VotedVal) / (4.0 * rDeltaTime_s)) * 60.0;
ELSE
    rObserved_Bed1_dTdt_degCmin := 0.0;
    rObserved_Bed2_dTdt_degCmin := 0.0;
    rObserved_Bed3_dTdt_degCmin := 0.0;
    rObserved_Bed4_dTdt_degCmin := 0.0;
    rDepressurizationRate_bar_min := 0.0;
END_IF;

(* Identify instantaneous maximum hotspot temperature across all 4 beds *)
rMathMax := rTMR1_VotedVal;
IF rTMR2_VotedVal > rMathMax THEN rMathMax := rTMR2_VotedVal; END_IF;
IF rTMR3_VotedVal > rMathMax THEN rMathMax := rTMR3_VotedVal; END_IF;
IF rTMR4_VotedVal > rMathMax THEN rMathMax := rTMR4_VotedVal; END_IF;
rObserved_PeakCatalystTemp_degC := rMathMax;

(* --- 3.2 REACTION THERMODYNAMICS & EXOTHERM HEAT RELEASE OBSERVER --- *)
rFeedMassFlow_kgs := (rFeedFlow_m3h * rFeedDensity_kgm3) / 3600.0;
IF rFeedMassFlow_kgs < 0.0 THEN rFeedMassFlow_kgs := 0.0; END_IF;

(* Individual Catalyst Bed Temperature Differential [deg C] *)
rDeltaT_Bed1 := rTMR1_VotedVal - rTemp_FurnaceOutlet_degC;
rDeltaT_Bed2 := rTMR2_VotedVal - (rTMR1_VotedVal - (rValve_QuenchBed1_pct * 0.22));
rDeltaT_Bed3 := rTMR3_VotedVal - (rTMR2_VotedVal - (rValve_QuenchBed2_pct * 0.25));
rDeltaT_Bed4 := rTMR4_VotedVal - (rTMR3_VotedVal - (rValve_QuenchBed3_pct * 0.28));

rTotalReactor_DeltaT := rDeltaT_Bed1 + rDeltaT_Bed2 + rDeltaT_Bed3 + rDeltaT_Bed4;
IF rTotalReactor_DeltaT < 0.0 THEN rTotalReactor_DeltaT := 0.0; END_IF;

(* Net Exothermic Reaction Heat Release Rate [MW thermal] *)
(* Q_rx = m_dot * Cp * DeltaT_total *)
rObserved_ReactionHeatRelease_MW := (rFeedMassFlow_kgs * rSpecificHeat_Oil_kJkgK * rTotalReactor_DeltaT) / 1000.0;
IF rObserved_ReactionHeatRelease_MW < 0.0 THEN rObserved_ReactionHeatRelease_MW := 0.0; END_IF;

(* Chemical Hydrogen Consumption Estimation [Nm3 H2 / m3 Feed] *)
(* Based on Stoichiometric S, N removal and aromatic saturation kinetics *)
rSpecificHydrogenConsumption := 140.0 + (rFeedSulfur_wtPct * 45.0) + (rFeedNitrogen_ppm * 0.035) + (rTotalReactor_DeltaT * 1.85);
IF rSpecificHydrogenConsumption < 50.0 THEN rSpecificHydrogenConsumption := 50.0; END_IF;
IF rSpecificHydrogenConsumption > 350.0 THEN rSpecificHydrogenConsumption := 350.0; END_IF;
rObserved_H2Consumption_Nm3m3 := rSpecificHydrogenConsumption;

(* Zeolitic Acid-Site Kinetic Hydrocracking Conversion Estimation [%] *)
rEstimatedConversion_pct := 35.0 + (0.18 * (rObserved_PeakCatalystTemp_degC - 380.0)) + (0.04 * (rTMR7_VotedVal - 160.0));
IF rEstimatedConversion_pct < 0.0 THEN rEstimatedConversion_pct := 0.0; END_IF;
IF rEstimatedConversion_pct > 100.0 THEN rEstimatedConversion_pct := 100.0; END_IF;

(* --- 3.3 TWO-PHASE TRICKLE-BED HYDRODYNAMICS & LIQUID HOLDUP --- *)
(* Reactor Vessel Cross-Sectional Area (ID = 3.2 m -> A = 8.042 m2) *)
rLiquid_SuperficialVelocity_ms := (rFeedFlow_m3h / 3600.0) / 8.042;
IF rLiquid_SuperficialVelocity_ms < 0.0001 THEN rLiquid_SuperficialVelocity_ms := 0.0001; END_IF;

(* Gas Superficial Velocity under 180 bar operating conditions *)
rGas_SuperficialVelocity_ms := ((rFlow_RecycleGas_Nm3h + rFlow_MakeUpHydrogen_Nm3h) / 3600.0) *
                               (1.01325 / 180.0) * ((rTMR1_VotedVal + 273.15) / 273.15) / 8.042;
IF rGas_SuperficialVelocity_ms < 0.001 THEN rGas_SuperficialVelocity_ms := 0.001; END_IF;

(* Hydrodynamic Dynamic Liquid Holdup (fraction of void space occupied by liquid oil) *)
rObserved_TrickleLiquidHoldup := 0.120 + (0.350 * rLiquid_SuperficialVelocity_ms) - (0.045 * rGas_SuperficialVelocity_ms);
IF rObserved_TrickleLiquidHoldup < 0.05 THEN rObserved_TrickleLiquidHoldup := 0.05; END_IF;
IF rObserved_TrickleLiquidHoldup > 0.65 THEN rObserved_TrickleLiquidHoldup := 0.65; END_IF;

rObserved_ReactorDeltaP_bar := rTMR6_VotedVal;

(* --- 3.4 SOUR GAS AMINE SCRUBBER ABSORPTION MASS TRANSFER --- *)
IF rFlow_RecycleGas_Nm3h > 1000.0 THEN
    rAmine_LiquidGas_Ratio := rFlow_LeanAmine_m3h / (rFlow_RecycleGas_Nm3h / 1000.0);
ELSE
    rAmine_LiquidGas_Ratio := 0.50;
END_IF;
rAmine_LeanLoading_mol_mol := 0.025; (* Standard regenerated lean MDEA loading *)
rAmine_RichLoading_mol_mol := rAmine_LeanLoading_mol_mol + (rTMR8_VotedVal * 0.0018) + (rFeedSulfur_wtPct * 0.08);

(* --- 3.5 ATMOSPHERIC FRACTIONATION DISTILLATION PROFILE --- *)
rFractionator_RefluxRatio := 1.75 + (rValve_DynamicReflux_pct * 0.015);
rFractionator_ReboilerDuty_MW := 18.5 * (rValve_FractionatorReboiler_pct / 100.0);
rOverhead_CondenserDuty_MW := 14.0 * (rValve_DynamicReflux_pct / 100.0);


(* ==========================================================================================
 * PHASE 4: DISCRETE STATE-SPACE PREDICTION & KALMAN FILTER OBSERVER UPDATE
 * ========================================================================================== *)

(* Map voted sensor measurements into output vector y_meas[1..8] *)
y_meas[1] := rTMR1_VotedVal;
y_meas[2] := rTMR2_VotedVal;
y_meas[3] := rTMR3_VotedVal;
y_meas[4] := rTMR4_VotedVal;
y_meas[5] := (rValve_QuenchBed1_pct + rValve_QuenchBed2_pct + rValve_QuenchBed3_pct) * 85.0;
y_meas[6] := rTMR6_VotedVal;
y_meas[7] := rTMR5_VotedVal;
y_meas[8] := rTMR8_VotedVal;

(* Active Control Action Vector u_ctrl[1..6] mapping from previous cycle *)
u_ctrl[1] := rValve_QuenchBed1_pct;
u_ctrl[2] := rValve_QuenchBed2_pct;
u_ctrl[3] := rValve_QuenchBed3_pct;
u_ctrl[4] := rValve_ChargeFurnaceFuel_pct;
u_ctrl[5] := rValve_HPSep_LetdownA_pct;
u_ctrl[6] := rPump_LeanAmine_Speed_pct;

(* Compute One-Step Ahead State Prediction: x_pred = A * x_state + B * u_ctrl *)
FOR iIdxI := 1 TO 8 DO
    rMathSum := 0.0;
    FOR iIdxJ := 1 TO 8 DO
        rMathSum := rMathSum + (matA[iIdxI, iIdxJ] * x_state[iIdxJ]);
    END_FOR;
    FOR iIdxK := 1 TO 6 DO
        rMathSum := rMathSum + (matB[iIdxI, iIdxK] * u_ctrl[iIdxK]);
    END_FOR;
    x_pred[iIdxI] := rMathSum;
END_FOR;

(* Innovation Error Calculation: x_err = y_meas - C * x_pred *)
FOR iIdxI := 1 TO 8 DO
    rMathSum := 0.0;
    FOR iIdxJ := 1 TO 8 DO
        rMathSum := rMathSum + (matC[iIdxI, iIdxJ] * x_pred[iIdxJ]);
    END_FOR;
    y_est[iIdxI] := rMathSum;
    x_err[iIdxI] := y_meas[iIdxI] - y_est[iIdxI];
END_FOR;

(* Luenberger / Kalman Observer State Correction: x_state = x_pred + K * x_err *)
FOR iIdxI := 1 TO 8 DO
    x_state[iIdxI] := x_pred[iIdxI] + (rKalmanGain[iIdxI] * x_err[iIdxI]);
    x_prev[iIdxI]  := x_state[iIdxI];
END_FOR;
"""
