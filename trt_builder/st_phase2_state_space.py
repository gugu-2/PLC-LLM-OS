# trt_builder/st_phase2_state_space.py
"""
Phase 2: First-Principles Cyber-Physical State-Space Estimation & Thermodynamic Expansion Engine
for FB_Steel_BlastFurnace_TopGas_TRT_PowerRecovery
"""

def get_phase2_state_space():
    return """(* ==================================================================================================== *)
(* PHASE 2: FIRST-PRINCIPLES CYBER-PHYSICAL STATE-SPACE ESTIMATION & THERMODYNAMIC EXPANSION ENGINE    *)
(* ==================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------- *)
(* 2.1 FIRST-PRINCIPLES GAS THERMODYNAMICS & REAL-GAS EXPANSION FORMULATIONS                            *)
(* ---------------------------------------------------------------------------------------------------- *)
(* Absolute Pressures & Temperature [Pa, K] *)
rGasAbsolutePressInlet_Pa := (rVoted_TurbineInletPressure * 1000.0) + rAtmosphericPressure_Pa;
rGasAbsolutePressBack_Pa  := (rCleanGasHeaderPress_PT302 * 1000.0) + rAtmosphericPressure_Pa;
rGasAbsoluteTempInlet_K   := rTopGasInletTemp_TT102 + 273.15;

(* Real Gas Supercompressibility Z-Factor Evaluation (Redlich-Kwong Peng-Robinson Approximation) *)
rGasCompressibilityZ := 1.0 - (rGasAbsolutePressInlet_Pa / (rGasAbsoluteTempInlet_K * 450000.0));
IF rGasCompressibilityZ < 0.85 THEN
    rGasCompressibilityZ := 0.85;
ELSIF rGasCompressibilityZ > 1.05 THEN
    rGasCompressibilityZ := 1.05;
END_IF;

(* Upstream Gas Density rho = P / (Z * R_spec * T) [kg/m3] *)
rGasDensity_Inlet := rGasAbsolutePressInlet_Pa / (rGasCompressibilityZ * rGasConstantSpecific * rGasAbsoluteTempInlet_K);
IF rGasDensity_Inlet < 1.2 THEN
    rGasDensity_Inlet := 1.2;
END_IF;

(* Total Expansion Pressure Ratio Pi = P_in / P_out *)
IF rGasAbsolutePressBack_Pa > 80000.0 THEN
    rPressureRatio_Total := rGasAbsolutePressInlet_Pa / rGasAbsolutePressBack_Pa;
ELSE
    rPressureRatio_Total := rGasAbsolutePressInlet_Pa / 101325.0;
END_IF;

IF rPressureRatio_Total < 1.05 THEN
    rPressureRatio_Total := 1.05;
END_IF;

(* Thermodynamic Isentropic Enthalpy Drop delta_hs = Cp * T_in * [1 - (1/Pi)^((kappa-1)/kappa)] [J/kg] *)
(* (kappa - 1) / kappa = (1.363 - 1.0) / 1.363 = 0.266324 *)
rTempRatio := 1.0 / rPressureRatio_Total;
rTempTerm := 1.0 - EXPT(rTempRatio, 0.266324);
rIsentropicEnthalpyDrop := rGasSpecificHeat_Cp * rGasAbsoluteTempInlet_K * rTempTerm;

(* Polytropic Stage Efficiency Correction with Blade Dust Erosion Factor *)
rExpansionPolytropicEfficiency := 0.865 - (0.0005 * (rVoted_BagFilterDiffPress - 5.0)) - (0.0008 * (rVoted_TurbineVibration - 12.0));
IF rExpansionPolytropicEfficiency > 0.89 THEN
    rExpansionPolytropicEfficiency := 0.89;
ELSIF rExpansionPolytropicEfficiency < 0.72 THEN
    rExpansionPolytropicEfficiency := 0.72;
END_IF;

rPolytropicEnthalpyDrop := rIsentropicEnthalpyDrop * rExpansionPolytropicEfficiency;

(* Theoretical Aerodynamic Mechanical Power Yield [MW] *)
rCalculated_TRTFlow_kgs := rVoted_TopGasMassFlow * (rVSV_PositionDemand / 100.0) * 0.92;
IF rCalculated_TRTFlow_kgs < 0.0 THEN
    rCalculated_TRTFlow_kgs := 0.0;
END_IF;
rCalculatedAerodynamicPower := (rCalculated_TRTFlow_kgs * rPolytropicEnthalpyDrop) / 1000000.0;

(* Aerodynamic Driving Shaft Torque T_aero = P_aero / omega [N*m] *)
IF rTurbineSpeed_Filtered > 120.0 THEN
    rAerodynamicTorque_Nm := (rCalculatedAerodynamicPower * 1000000.0) / (rTurbineSpeed_Filtered * 0.104719755);
ELSE
    rAerodynamicTorque_Nm := 0.0;
END_IF;

(* Septum Parallel Valve Bank Subcritical Flow Synthesis *)
rCalculated_SeptumFlow_kgs := (rSeptumV1_MaxFlowCap_kgs * (rSeptumV1_PositionDemand / 100.0))
                            + (rSeptumV2_MaxFlowCap_kgs * (rSeptumV2_PositionDemand / 100.0))
                            + (rSeptumV3_MaxFlowCap_kgs * (rSeptumV3_PositionDemand / 100.0));

(* Cumulative Recovered Thermal Energy Integration [MWh] *)
IF bTRT_PowerRecoveryActive AND (rVoted_GeneratorActivePower > 0.0) THEN
    rTurbineRecoveredEnergy_MWh := rTurbineRecoveredEnergy_MWh + (rVoted_GeneratorActivePower * (rSamplingTime_s / 3600.0));
END_IF;


(* ---------------------------------------------------------------------------------------------------- *)
(* 2.2 LUENBERGER STATE OBSERVER INNOVATION & FULL DYNAMIC FILTERING (Ts = 10 ms)                        *)
(* ---------------------------------------------------------------------------------------------------- *)
(* Form Measurement Vector y_meas[6] relative to equilibrium targets *)
aStateMeas[1] := rVoted_TopGasPressure - rTopGasPressure_Setpoint;
aStateMeas[2] := rVoted_TurbineInletPressure - rTopGasPressure_Setpoint;
aStateMeas[3] := rVoted_TopGasMassFlow;
aStateMeas[4] := rVoted_GeneratorActivePower;
aStateMeas[5] := rVoted_TurbineVibration;
aStateMeas[6] := rVoted_BagFilterDiffPress;

(* Compute Predicted Measurement Vector y_hat = mC * aStateEst + mD * aControlPrev *)
FOR iIdx := 1 TO 6 DO
    rTempSum := 0.0;
    FOR jIdx := 1 TO 8 DO
        rTempSum := rTempSum + (mC[iIdx, jIdx] * aStateEst[jIdx]);
    END_FOR;
    FOR pIdx := 1 TO 5 DO
        rTempSum := rTempSum + (mD[iIdx, pIdx] * aControlPrev[pIdx]);
    END_FOR;
    aObsInnovation[iIdx] := aStateMeas[iIdx] - rTempSum;
END_FOR;

(* Innovation State Correction: aStateEst = aStateEst + mK * aObsInnovation *)
FOR iIdx := 1 TO 8 DO
    rTempSum := 0.0;
    FOR jIdx := 1 TO 6 DO
        rTempSum := rTempSum + (mK[iIdx, jIdx] * aObsInnovation[jIdx]);
    END_FOR;
    aStateEst[iIdx] := aStateEst[iIdx] + rTempSum;
END_FOR;

(* Dynamic State Transition Prediction: aStatePred = mA * aStateEst + mB * aControlDemand *)
FOR iIdx := 1 TO 8 DO
    rTempSum := 0.0;
    FOR jIdx := 1 TO 8 DO
        rTempSum := rTempSum + (mA[iIdx, jIdx] * aStateEst[jIdx]);
    END_FOR;
    FOR pIdx := 1 TO 5 DO
        rTempSum := rTempSum + (mB[iIdx, pIdx] * aControlDemand[pIdx]);
    END_FOR;
    aStatePred[iIdx] := rTempSum;
END_FOR;
"""
