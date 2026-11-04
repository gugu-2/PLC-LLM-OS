# st_phase2_3.py
# Contains Phase 2 (Electrochemical & Crossover Observers) and Phase 3 (State-Space & MPC)

def get_phase2_3():
    return """
(* ===================================================================================================================
 * PHASE 2: CYBER-PHYSICAL ELECTROCHEMICAL & GAS CROSSOVER OBSERVERS
 * =================================================================================================================== *)
(* 2.1 Thermodynamic Temperature & Equilibrium Potential (Nernst Model) *)
rCalc_AbsoluteTemp_K := rVoted_CoolingOutletTemp_degC + 273.15;
IF rCalc_AbsoluteTemp_K < 273.15 THEN
    rCalc_AbsoluteTemp_K := 298.15;
END_IF;

(* Standard reversible cell potential E_0(T) *)
rCalc_NernstPotential_V := 1.229 - 0.00085 * (rCalc_AbsoluteTemp_K - 298.15);

(* Nernst Pressure correction term: (R * T / (2 * F)) * LN( (a_H2 * a_O2^0.5) / a_H2O ) *)
IF rVoted_CathodePressure_bar > 1.0 AND rVoted_AnodePressure_bar > 1.0 THEN
    rCalc_NernstPotential_V := rCalc_NernstPotential_V + ( (c_rGasConstR * rCalc_AbsoluteTemp_K) / (2.0 * c_rFaradayConst) ) *
        LN( ( (rVoted_CathodePressure_bar / c_rStandardAtmPressure_bar) * SQRT(rVoted_AnodePressure_bar / c_rStandardAtmPressure_bar) ) / 1.0 );
END_IF;

(* 2.2 Facility Average Current Density & Butler-Volmer Activation Overpotentials *)
(* Average stack current from voted total *)
IF rActiveStacksCount > 0.5 THEN
    rSpecificStackCurrent := (rFacilityTotalPower_MW * 1000000.0) / (rActiveStacksCount * 1000.0); (* Approx stack current [A] *)
ELSE
    rSpecificStackCurrent := 0.0;
END_IF;

IF rSpecificStackCurrent < 100.0 THEN
    rSpecificStackCurrent := 100.0; (* Minimum non-zero for logarithmic stability *)
END_IF;

aStackCurrentDensity_A_cm2[1] := rSpecificStackCurrent / c_rCellActiveArea_cm2;
IF aStackCurrentDensity_A_cm2[1] < 0.001 THEN
    aStackCurrentDensity_A_cm2[1] := 0.001;
END_IF;

(* Anode Oxygen Evolution Reaction (OER) Overpotential eta_act,a *)
rCalc_AnodeOverpotential_V := ( (c_rGasConstR * rCalc_AbsoluteTemp_K) / (c_rAlphaAnode * c_rFaradayConst) ) *
    LN( aStackCurrentDensity_A_cm2[1] / c_rExchangeCurrentDensity_OER );
IF rCalc_AnodeOverpotential_V < 0.05 THEN
    rCalc_AnodeOverpotential_V := 0.05;
ELSIF rCalc_AnodeOverpotential_V > 0.65 THEN
    rCalc_AnodeOverpotential_V := 0.65;
END_IF;

(* Cathode Hydrogen Evolution Reaction (HER) Overpotential eta_act,c *)
rCalc_CathodeOverpotential_V := ( (c_rGasConstR * rCalc_AbsoluteTemp_K) / (c_rAlphaCathode * c_rFaradayConst) ) *
    LN( aStackCurrentDensity_A_cm2[1] / c_rExchangeCurrentDensity_HER );
IF rCalc_CathodeOverpotential_V < 0.01 THEN
    rCalc_CathodeOverpotential_V := 0.01;
ELSIF rCalc_CathodeOverpotential_V > 0.25 THEN
    rCalc_CathodeOverpotential_V := 0.25;
END_IF;

(* 2.3 Nafion 117 Proton Conductivity & Ohmic Area Resistance *)
(* sigma_PEM = (0.005139 * lambda - 0.00326) * EXP( 1268.0 * (1/303.15 - 1/T) ) [S/cm] *)
rCalc_ProtonConductivity_S_cm := (0.005139 * c_rMembraneHydrationLambda - 0.00326) *
    EXP( 1268.0 * ( (1.0 / 303.15) - (1.0 / rCalc_AbsoluteTemp_K) ) );
IF rCalc_ProtonConductivity_S_cm < 0.020 THEN
    rCalc_ProtonConductivity_S_cm := 0.020;
END_IF;

(* Area Specific Resistance r_PEM = t_mem / sigma_PEM [Ohm*cm2] *)
rCalc_MembraneAreaResistance_Ohmcm2 := c_rMembraneThickness_cm / rCalc_ProtonConductivity_S_cm;
rCalc_OhmicOverpotential_V := aStackCurrentDensity_A_cm2[1] * rCalc_MembraneAreaResistance_Ohmcm2;

(* Single Cell Operating Voltage Model *)
rCalc_SingleCellVoltage_V := rCalc_NernstPotential_V + rCalc_AnodeOverpotential_V + rCalc_CathodeOverpotential_V + rCalc_OhmicOverpotential_V;

(* 2.4 Fick's Law Diffusive Gas Crossover Observer *)
(* Molecular diffusion flux through polymer electrolyte *)
rCalc_H2CrossoverFlux_mol_cm2_s := ( c_rPreExpCrossoverH2 * EXP( -c_rActivationEnergyH2_over_R / rCalc_AbsoluteTemp_K ) *
    (rVoted_CathodePressure_bar / c_rMembraneThickness_cm) ) +
    ( 0.00000000015 * (rVoted_MembraneDiffPressure_bar / c_rMembraneThickness_cm) );

IF rCalc_H2CrossoverFlux_mol_cm2_s < 0.0 THEN
    rCalc_H2CrossoverFlux_mol_cm2_s := 0.0;
END_IF;

(* Oxygen Faradaic production flux at anode *)
rCalc_FaradaicEfficiency := 0.995 - (0.015 / (aStackCurrentDensity_A_cm2[1] + 0.05));
IF rCalc_FaradaicEfficiency < 0.85 THEN
    rCalc_FaradaicEfficiency := 0.85;
ELSIF rCalc_FaradaicEfficiency > 0.999 THEN
    rCalc_FaradaicEfficiency := 0.999;
END_IF;

rCalc_O2ProductionFlux_mol_cm2_s := (aStackCurrentDensity_A_cm2[1] * rCalc_FaradaicEfficiency) / (4.0 * c_rFaradayConst);
IF rCalc_O2ProductionFlux_mol_cm2_s < 0.00000001 THEN
    rCalc_O2ProductionFlux_mol_cm2_s := 0.00000001;
END_IF;

(* Predicted H2 in O2 concentration in anode gas phase [% vol] *)
rCalc_H2inO2_Predicted_pct := ( rCalc_H2CrossoverFlux_mol_cm2_s /
    (2.0 * rCalc_O2ProductionFlux_mol_cm2_s + rCalc_H2CrossoverFlux_mol_cm2_s) ) * 100.0;

(* 2.5 Facility Mass & Energy Production Rates *)
(* Hydrogen generation rate in Nm3/h *)
IF rFacilityTotalPower_MW > 0.1 AND rCalc_SingleCellVoltage_V > 1.2 THEN
    rTotalH2ProductionRate_Nm3h := ( (rFacilityTotalPower_MW * 1000000.0) / (rCalc_SingleCellVoltage_V * c_nCellsPerStack) ) *
        ( (c_nCellsPerStack * rCalc_FaradaicEfficiency) / (2.0 * c_rFaradayConst) ) *
        c_rMolarVolumeH2_Nm3_mol * 3600.0;
    rTotalO2ProductionRate_Nm3h := rTotalH2ProductionRate_Nm3h * 0.50;
    
    (* Specific Energy Consumption kWh / Nm3 *)
    IF rTotalH2ProductionRate_Nm3h > 10.0 THEN
        rSpecificEnergyConsumption_kWh_Nm3 := (rFacilityTotalPower_MW * 1000.0) / rTotalH2ProductionRate_Nm3h;
    ELSE
        rSpecificEnergyConsumption_kWh_Nm3 := 4.50;
    END_IF;
    
    (* Efficiency on Lower Heating Value (LHV) Basis *)
    rFacilityEfficiency_LHV_pct := ( (rTotalH2ProductionRate_Nm3h / 3600.0) / c_rMolarVolumeH2_Nm3_mol * c_rLHV_H2_kJ_mol ) /
        (rFacilityTotalPower_MW * 1000.0) * 100.0;
ELSE
    rTotalH2ProductionRate_Nm3h := 0.0;
    rTotalO2ProductionRate_Nm3h := 0.0;
    rSpecificEnergyConsumption_kWh_Nm3 := 0.0;
    rFacilityEfficiency_LHV_pct := 0.0;
END_IF;

(* ===================================================================================================================
 * PHASE 3: 8x8 DISCRETE STATE-SPACE PREDICTION & RECEDING-HORIZON MPC
 * =================================================================================================================== *)
(* 3.1 Construct State Vector from Observer Deviations *)
ax_state[1] := rCalc_AnodeOverpotential_V + rCalc_CathodeOverpotential_V - 0.435; (* Delta Overpotential *)
ax_state[2] := rVoted_MembraneDiffPressure_bar;                                  (* Delta Membrane DP *)
ax_state[3] := rVoted_H2_in_O2_Crossover_pct - 0.40;                             (* Delta Crossover *)
ax_state[4] := rVoted_CoolingOutletTemp_degC - 70.0;                             (* Delta Temperature *)
ax_state[5] := rVoted_AnodePressure_bar - 30.0;                                  (* Delta Anode Pressure *)
ax_state[6] := rVoted_CathodePressure_bar - 30.0;                                (* Delta Cathode Pressure *)
ax_state[7] := rVoted_DI_WaterFeedFlow_m3h - 15.0;                               (* Delta DI Flow *)
ax_state[8] := (rVoted_ProductH2_Dewpoint_degC - (-70.0)) * 0.1;                 (* Delta Moisture Indicator *)

(* Reference Target State Vector (All Desired Deviations = 0.0) *)
FOR iIdx := 1 TO 8 DO
    ax_ref[iIdx] := 0.0;
END_FOR;

(* 3.2 Discrete State-Space Prediction: x[k+1] = A * x[k] + B * u[k] *)
FOR iIdx := 1 TO 8 DO
    rTempSum := 0.0;
    FOR jIdx := 1 TO 8 DO
        rTempSum := rTempSum + aA[iIdx, jIdx] * ax_state[jIdx];
    END_FOR;
    FOR jIdx := 1 TO 4 DO
        rTempSum := rTempSum + aB[iIdx, jIdx] * au_control[jIdx];
    END_FOR;
    ax_next[iIdx] := rTempSum;
    aPredictedState[iIdx] := rTempSum;
END_FOR;

(* 3.3 Receding-Horizon Quadratic Cost Objective Function Evaluation *)
(* J = sum (x_pred - r)^T * (Q + P) * (x_pred - r) + u^T * R * u + Delta_u^T * S * Delta_u *)
rMPC_QuadraticCost := 0.0;
FOR iIdx := 1 TO 8 DO
    rMPC_QuadraticCost := rMPC_QuadraticCost + (aQ_Weight[iIdx] + aP_TerminalWeight[iIdx]) *
        (aPredictedState[iIdx] - ax_ref[iIdx]) * (aPredictedState[iIdx] - ax_ref[iIdx]);
END_FOR;
FOR jIdx := 1 TO 4 DO
    rMPC_QuadraticCost := rMPC_QuadraticCost + aR_Weight[jIdx] * au_control[jIdx] * au_control[jIdx] +
        aS_Weight[jIdx] * (au_control[jIdx] - au_prev[jIdx]) * (au_control[jIdx] - au_prev[jIdx]);
END_FOR;

(* 3.4 Fast Projected Gradient Descent (PGD) 3-Pass Optimization *)
FOR kIdx := 1 TO 3 DO
    (* Calculate Gradient dJ/du for each actuator *)
    FOR jIdx := 1 TO 4 DO
        rTempSum := 0.0;
        FOR iIdx := 1 TO 8 DO
            rTempSum := rTempSum + aB[iIdx, jIdx] * (aQ_Weight[iIdx] + aP_TerminalWeight[iIdx]) *
                (aPredictedState[iIdx] - ax_ref[iIdx]);
        END_FOR;
        rTempSum := rTempSum + aR_Weight[jIdx] * au_control[jIdx] +
            aS_Weight[jIdx] * (au_control[jIdx] - au_prev[jIdx]);
        aGrad_u[jIdx] := rTempSum;
    END_FOR;

    (* Update Control Inputs via Gradient Descent Step *)
    FOR jIdx := 1 TO 4 DO
        au_control[jIdx] := au_control[jIdx] - c_rPGD_Alpha * aGrad_u[jIdx];

        (* Hard Saturation Projection [u_min, u_max] *)
        IF au_control[jIdx] < au_min[jIdx] THEN
            au_control[jIdx] := au_min[jIdx];
        ELSIF au_control[jIdx] > au_max[jIdx] THEN
            au_control[jIdx] := au_max[jIdx];
        END_IF;

        (* Slew Rate Boundary Clamping *)
        au_delta[jIdx] := au_control[jIdx] - au_prev[jIdx];
        IF au_delta[jIdx] > adelta_u_max[jIdx] THEN
            au_control[jIdx] := au_prev[jIdx] + adelta_u_max[jIdx];
        ELSIF au_delta[jIdx] < -adelta_u_max[jIdx] THEN
            au_control[jIdx] := au_prev[jIdx] - adelta_u_max[jIdx];
        END_IF;
    END_FOR;

    (* Recompute Predicted State for next gradient iteration *)
    FOR iIdx := 1 TO 8 DO
        rTempSum := 0.0;
        FOR jIdx := 1 TO 8 DO
            rTempSum := rTempSum + aA[iIdx, jIdx] * ax_state[jIdx];
        END_FOR;
        FOR jIdx := 1 TO 4 DO
            rTempSum := rTempSum + aB[iIdx, jIdx] * au_control[jIdx];
        END_FOR;
        aPredictedState[iIdx] := rTempSum;
    END_FOR;
END_FOR;

(* Store Prior Controls for Slew Regularization *)
FOR jIdx := 1 TO 4 DO
    au_prev[jIdx] := au_control[jIdx];
END_FOR;

(* 3.5 Dispatch MPC Actuator Trim Setpoints to Process Regulators *)
(* u[2]: Differential Backpressure Trim Valve CV-203 *)
rValveCmd_MembraneDiffPressure_pct := 50.0 + au_control[2];
IF rValveCmd_MembraneDiffPressure_pct < 0.0 THEN
    rValveCmd_MembraneDiffPressure_pct := 0.0;
ELSIF rValveCmd_MembraneDiffPressure_pct > 100.0 THEN
    rValveCmd_MembraneDiffPressure_pct := 100.0;
END_IF;

(* u[3]: Anode DI Water Circulating Pump P-501 Speed *)
rPumpCmd_DI_WaterCirculation_pct := 65.0 + au_control[3];
IF rPumpCmd_DI_WaterCirculation_pct < 20.0 THEN
    rPumpCmd_DI_WaterCirculation_pct := 20.0;
ELSIF rPumpCmd_DI_WaterCirculation_pct > 100.0 THEN
    rPumpCmd_DI_WaterCirculation_pct := 100.0;
END_IF;

(* u[4]: Secondary Cooling Bypass Trim Valve CV-401 *)
rValveCmd_CoolingTowerBypass_pct := 25.0 + au_control[4];
IF rValveCmd_CoolingTowerBypass_pct < 0.0 THEN
    rValveCmd_CoolingTowerBypass_pct := 0.0;
ELSIF rValveCmd_CoolingTowerBypass_pct > 100.0 THEN
    rValveCmd_CoolingTowerBypass_pct := 100.0;
END_IF;
"""
