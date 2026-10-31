# gen_phase2.py - Generates Phase 2: Bioprocess Observers & Endpoint Metrology

def generate_phase2():
    return """(* ==================================================================================================================== *)
(* PHASE 2: CYBER-PHYSICAL BIOPROCESS OBSERVERS, SUBLIMATION KINETICS & ENDPOINT METROLOGY                             *)
(* ==================================================================================================================== *)

(* --- 2.1: Vial Heat Transfer Coefficient (Kv) Dynamic Modeling --- *)
(* Kv accounts for contact conduction, gas conduction, and radiation: Kv = A_v + (B_v * P_ch) / (1 + C_v * P_ch) *)
IF rVotedChamberPressure_CM_Actual > 0.001 THEN
    rKv_VialHeatTransferCoeff := 12.5 + ( (28.4 * rVotedChamberPressure_CM_Actual) / (1.0 + (0.185 * rVotedChamberPressure_CM_Actual)) );
ELSE
    rKv_VialHeatTransferCoeff := 12.5; (* High-vacuum radiation & direct glass contact baseline *)
END_IF;

(* Estimated Vial Outer Base Glass Temperature from Shelf Oil Convective Heat Transfer *)
rVialBaseTemperatureEstimate := rVotedShelfTemperatureActual - ( (rVotedShelfTemperatureActual - rVotedProductTemperatureActual) * 0.35 );

(* --- 2.2: Dry Product Cake Mass Transfer Resistance (Rp) Modeling --- *)
(* Rp increases nonlinearly with dried cake layer thickness: Rp = R0 + (A_p * L_dry) / (1 + B_p * L_dry) *)
IF (c_rInitialCakeFillDepth_mm - rRemainingIceCakeThickness_mm) > 0.0 THEN
    rRp_CakeMassTransferResistance := 85000.0 + ( (420000.0 * (c_rInitialCakeFillDepth_mm - rRemainingIceCakeThickness_mm)) /
                                                 (1.0 + (0.085 * (c_rInitialCakeFillDepth_mm - rRemainingIceCakeThickness_mm))) );
ELSE
    rRp_CakeMassTransferResistance := 85000.0; (* Initial formulation dry skin resistance *)
END_IF;

(* --- 2.3: Ice Sublimation Front Saturation Vapor Pressure via Clausius-Clapeyron Approximation --- *)
(* Goff-Gratch / Antoine formulation: P_ice(T) = 6.1115 * 10^( (9.5 * T_front) / (T_front + 265.5) ) [mbar] *)
rClausiusExponent := (9.5 * rVotedProductTemperatureActual) / (rVotedProductTemperatureActual + 265.5);
(* Convert base-10 exponent to natural exponent: z = rClausiusExponent * ln(10) = rClausiusExponent * 2.302585 *)
rTempLogCalc := rClausiusExponent * 2.302585;

(* 5th-Order Taylor Series Polynomial for e^z: e^z = 1 + z + z^2/2 + z^3/6 + z^4/24 + z^5/120 *)
rExpSeriesTerm := 1.0 + rTempLogCalc
                  + (0.50000 * rTempLogCalc * rTempLogCalc)
                  + (0.16667 * rTempLogCalc * rTempLogCalc * rTempLogCalc)
                  + (0.04167 * rTempLogCalc * rTempLogCalc * rTempLogCalc * rTempLogCalc)
                  + (0.00833 * rTempLogCalc * rTempLogCalc * rTempLogCalc * rTempLogCalc * rTempLogCalc);

IF rExpSeriesTerm > 0.0001 THEN
    rSaturationVaporPressure_Pice := 6.1115 * rExpSeriesTerm;
ELSE
    rSaturationVaporPressure_Pice := 0.0001;
END_IF;

(* Sublimation Vapor Driving Pressure Gradient (P_ice - P_chamber) *)
rSublimationDrivingForce := rSaturationVaporPressure_Pice - rVotedChamberPressure_CM_Actual;
IF rSublimationDrivingForce < 0.0 THEN
    rSublimationDrivingForce := 0.0; (* No condensation back onto cake *)
END_IF;

(* --- 2.4: Instantaneous Sublimation Mass Flux & Enthalpy Demand --- *)
(* mdot_sub = N_vials * ( A_vial * (P_ice - P_ch) * 100 Pa/mbar ) / Rp * 3600 s/h [kg/h] *)
IF rRp_CakeMassTransferResistance > 1000.0 THEN
    rSublimationRateInstantaneous := (c_rVialCount * c_rVialCrossSectionArea_m2 * (rSublimationDrivingForce * 100.0) / rRp_CakeMassTransferResistance) * 3600.0;
ELSE
    rSublimationRateInstantaneous := 0.0;
END_IF;

(* Sublimation Heat Demand (Watts = J/s): Q_sub = mdot [kg/s] * Delta_H_sub [J/kg] *)
rSublimationHeatFluxWatts := (rSublimationRateInstantaneous / 3600.0) * (c_rLatentHeatSublimation_J_g * 1000.0);

(* Silicone Oil Thermal Energy Inflow to Shelves *)
rShelfDeltaT_InletOutlet := rShelfTempInlet_ChA - rShelfTempOutlet_ChA;
(* Q_oil = m_dot_oil * c_p * Delta_T (Syltherm XLT density ~ 850 kg/m3, cp ~ 1700 J/kg*K) *)
rShelfOilEnergyFluxWatts := ( (rSiliconeOilCirculationFlowRate / 60000.0) * 850.0 ) * 1700.0 * rShelfDeltaT_InletOutlet;

(* Cumulative Sublimated Mass Integration & Remaining Frozen Cake Thickness *)
IF (eCurrentState = 60) OR (eCurrentState = 70) THEN
    rCumulativeSublimatedIceMass := rCumulativeSublimatedIceMass + ( (rSublimationRateInstantaneous / 3600.0) * rCycleScanDeltaTime );
    (* Total initial water in 150,000 vials = 150,000 * 3.0 mL = 450 kg water *)
    IF rCumulativeSublimatedIceMass < 450.0 THEN
        rRemainingIceCakeThickness_mm := c_rInitialCakeFillDepth_mm * (1.0 - (rCumulativeSublimatedIceMass / 450.0));
        rDryingProgressRatio := rCumulativeSublimatedIceMass / 450.0;
    ELSE
        rRemainingIceCakeThickness_mm := 0.0;
        rDryingProgressRatio := 1.0;
    END_IF;
END_IF;

(* --- 2.5: Ice Condenser Frost Layer Thickness & Thermal Resistance --- *)
IF c_rCondenserTotalArea_m2 > 1.0 THEN
    rCondenserFrostThickness_mm := (rCumulativeSublimatedIceMass / (c_rCondenserTotalArea_m2 * c_rIceDensity_kg_m3)) * 1000.0;
    (* Thermal temperature drop across ice cake: Delta_T = Q_sub * (delta_ice / (k_ice * A_cond)) *)
    rCondenserFrostThermalDeltaT := rSublimationHeatFluxWatts * ( (rCondenserFrostThickness_mm / 1000.0) / (c_rIceThermalConductivity_W_mK * c_rCondenserTotalArea_m2) );
ELSE
    rCondenserFrostThickness_mm := 0.0;
    rCondenserFrostThermalDeltaT := 0.0;
END_IF;

(* --- 2.6: Dual-Gauge Pirani vs Capacitance Manometer Endpoint Metrology --- *)
(* Pirani thermal conductivity sensor reads higher than Baratron capacitance gauge when water vapor is present *)
rDualGaugeDifferentialPressure := rVotedChamberPressure_Pirani_Actual - rVotedChamberPressure_CM_Actual;
IF rDualGaugeDifferentialPressure < 0.0 THEN
    rDualGaugeDifferentialPressure := 0.0;
END_IF;

(* Critical Formulation Collapse Headroom *)
rProductCollapseMarginActual := rSet_ProductCollapseTemp_Tc - rVotedProductTemperatureActual;

(* Primary Drying Endpoint Detection: Convergence of Pirani to Baratron (Delta_P <= 0.005 mbar) *)
IF (eCurrentState = 60) OR (eCurrentState = 70) THEN
    IF (rDualGaugeDifferentialPressure <= 0.005) AND (rRemainingIceCakeThickness_mm <= 0.35) THEN
        rEndpointConvergenceTimer_s := rEndpointConvergenceTimer_s + rCycleScanDeltaTime;
        IF rEndpointConvergenceTimer_s >= 2700.0 THEN (* 45 minutes persistent convergence *)
            bPrimaryDryingEndpointDetected := TRUE;
        END_IF;
    ELSE
        rEndpointConvergenceTimer_s := 0.0;
    END_IF;
END_IF;

(* --- 2.7: Chamber Automated Pressure Rise Test (PRT) / Manometric Temperature Measurement --- *)
IF bPRT_ActiveInProgress THEN
    rPRT_PressureRiseElapsed_s := rPRT_PressureRiseElapsed_s + rCycleScanDeltaTime;
    IF rPRT_PressureRiseElapsed_s >= 30.0 THEN
        (* End of 30-second isolation test: evaluate slope *)
        rChamberPressureRiseRate_mbar_s := (rVotedChamberPressure_CM_Actual - rPRT_PressureRiseStart_mbar) / 30.0;
        bPRT_ActiveInProgress := FALSE;
        rPRT_PressureRiseElapsed_s := 0.0;
    END_IF;
END_IF;

(* Secondary Drying Desorption Residual Moisture Estimator *)
IF eCurrentState = 80 THEN
    (* Desorption kinetics: dC/dt = -k_desorb * (C - C_equilibrium) *)
    rDesorptionDrivingForce := rDesorptionMoistureEstimate_Pct - 0.40;
    IF rDesorptionDrivingForce > 0.0 THEN
        rDesorptionMoistureEstimate_Pct := rDesorptionMoistureEstimate_Pct - (0.00015 * rDesorptionDrivingForce * rCycleScanDeltaTime);
    END_IF;
    IF rDesorptionMoistureEstimate_Pct <= 0.85 THEN
        bSecondaryDryingCompleteFlag := TRUE;
    END_IF;
ELSE
    IF eCurrentState < 80 THEN
        rDesorptionMoistureEstimate_Pct := 6.50; (* Bound moisture in amorphous cake at end of primary drying *)
    END_IF;
END_IF;
"""

print("generate_phase2 loaded.")
