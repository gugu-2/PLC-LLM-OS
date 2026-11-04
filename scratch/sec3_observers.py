# Section 3: Cyber-Physical Observers & Modeling

def get_sec3():
    return """
(* =====================================================================================================================
 * PHASE 2: CYBER-PHYSICAL OBSERVERS, KINEMATIC & THERMODYNAMIC EQUATIONS
 * ===================================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------------------------
 * 2.1 Catenary Trajectory Mechanics & Tube Wall Clearance Observer
 * --------------------------------------------------------------------------------------------------------------------- *)
(* Calculate continuous linear cable mass per unit length [kg/m]:
 * w_cable = (A_cond * rho_Cu) + (A_insul * rho_XLPE) + (A_screens * rho_semi) *)
rObs_CableLinearMass_kgm := (rConductorCoreCrossSection_mm2 * 1.0e-6 * c_rCopperDensity_kg_m3) +
                            (c_rPi * ((c_rCableOuterDiameter_mm * 1.0e-3 * 0.5)**2.0 - ((c_rCableOuterDiameter_mm - 2.0 * rVoted_WallThickness_mm) * 1.0e-3 * 0.5)**2.0) * c_rXLPEDensity_kg_m3) +
                            (c_rPi * (((c_rCableOuterDiameter_mm - 2.0 * rVoted_WallThickness_mm) * 1.0e-3 * 0.5)**2.0 - (SQRT(rConductorCoreCrossSection_mm2 / c_rPi) * 1.0e-3)**2.0) * c_rSemiConDensity_kg_m3);

IF rObs_CableLinearMass_kgm < 15.0 THEN
    rObs_CableLinearMass_kgm := 21.840; (* Safe physical lower bound clamp [kg/m] *)
END_IF;

rCalculated_CableUnitWeight_kgm := rObs_CableLinearMass_kgm;

(* Calculate Catenary Parameter a = H / (w_cable * g) [m] *)
IF rVoted_HaulOffTension_kN > 5.0 THEN
    rObs_CatenaryParameter_a_m := (rVoted_HaulOffTension_kN * 1000.0) / (rObs_CableLinearMass_kgm * c_rGravity);
ELSE
    rObs_CatenaryParameter_a_m := (50.0 * 1000.0) / (rObs_CableLinearMass_kgm * c_rGravity);
END_IF;

(* Parabolic Series Expansion with Higher-Order Terms for Catenary Sag at X-Ray Sensor (x = 28.5 m):
 * y(x) = a * (cosh(x/a) - 1) approx (x^2) / (2*a) + (x^4) / (24*a^3) *)
rCatenaryTerm := c_rXRaySensorDistance_m / rObs_CatenaryParameter_a_m;
rObs_CatenarySagAtSensor_mm := ((c_rXRaySensorDistance_m**2.0) / (2.0 * rObs_CatenaryParameter_a_m) +
                               (c_rXRaySensorDistance_m**4.0) / (24.0 * (rObs_CatenaryParameter_a_m**3.0))) * 1000.0;

(* Dynamic Thermal Elongation inside 150m Heating Tube:
 * Delta_L = Integral [ alpha_th * Delta_T ] dx *)
rObs_ThermalElongation_m := c_rHeatingZoneLength_m * (1.7e-5 * (rVoted_ExtruderMeltTemp_degC - rAmbientTemperature_degC) +
                                                      1.5e-4 * (rVoted_Zone1Temp_degC - rAmbientTemperature_degC) * 0.15);

(* Upper and Lower Radial Clearances to 250 mm Inner Diameter Stainless Steel Tube Liner [mm] *)
rCalculated_CatenaryClearance_Top_mm := (c_rTubeInnerDiameter_mm * 0.5) - (rVoted_CatenarySag_mm - rSet_CatenarySagTarget_mm) - (c_rCableOuterDiameter_mm * 0.5);
rCalculated_CatenaryClearance_Bot_mm := (c_rTubeInnerDiameter_mm * 0.5) + (rVoted_CatenarySag_mm - rSet_CatenarySagTarget_mm) - (c_rCableOuterDiameter_mm * 0.5);

rObs_ClearanceTop_mm    := rCalculated_CatenaryClearance_Top_mm;
rObs_ClearanceBottom_mm := rCalculated_CatenaryClearance_Bot_mm;

(* Critical Tube Liner Contact Hazard Trip (if clearance drops below 12.0 mm) *)
IF (rCalculated_CatenaryClearance_Top_mm <= 12.0) OR (rCalculated_CatenaryClearance_Bot_mm <= 12.0) THEN
    bTubeContactHazardActive := TRUE;
ELSE
    bTubeContactHazardActive := FALSE;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * 2.2 XLPE Peroxide Cross-Linking Kinetics & Gel Fraction Observer
 * --------------------------------------------------------------------------------------------------------------------- *)
(* Residence Time inside the 75-Meter Radiant Heating Section [s] *)
IF rVoted_LinePullSpeed_mpm > 0.5 THEN
    rObs_ResidenceTimeInHeatZone_s := (c_rHeatingZoneLength_m / (rVoted_LinePullSpeed_mpm / 60.0));
ELSE
    rObs_ResidenceTimeInHeatZone_s := 3600.0;
END_IF;

(* Arrhenius Reaction Rate Constant: k_rxn = k_0 * EXP(-E_a / (R * T_kelvin)) [s^-1] *)
rObs_ArrheniusRateConstant_s1 := c_rDCP_PreExponential_s1 *
    EXP(-c_rDCP_ActivationEnergy_Jmol / (c_rUniversalGasConstant_R * (0.5 * (rVoted_Zone1Temp_degC + rVoted_Zone2Temp_degC) + 273.15)));

(* Rate of Conversion d_alpha/dt = k_rxn * (1.0 - alpha) *)
rCalculated_InstantCrosslinkRate := rObs_ArrheniusRateConstant_s1 * (1.0 - (rObs_CumulativeGelFraction_pct / 100.0));
IF rCalculated_InstantCrosslinkRate < 0.0 THEN
    rCalculated_InstantCrosslinkRate := 0.0;
END_IF;

(* Numerical Integration of Gel Fraction along Curing Zone:
 * alpha(t) = 1.0 - EXP(-k_rxn * t_res) *)
IF rVoted_LinePullSpeed_mpm >= 1.0 THEN
    rObs_CumulativeGelFraction_pct := (1.0 - EXP(-rObs_ArrheniusRateConstant_s1 * rObs_ResidenceTimeInHeatZone_s)) * 100.0;
ELSE
    rObs_CumulativeGelFraction_pct := 0.0;
END_IF;

rCalculated_GelFraction_pct := rObs_CumulativeGelFraction_pct;

IF rCalculated_GelFraction_pct >= rSet_MinGelFraction_pct THEN
    bCrossLinkingTargetAchieved := TRUE;
ELSE
    bCrossLinkingTargetAchieved := FALSE;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * 2.3 Nitrogen Atmosphere Mass Balance & Micro-Void Suppression Observer
 * --------------------------------------------------------------------------------------------------------------------- *)
(* Ideal Gas Law Mass Inventory of N2 inside 150m Tube: m = (P * V * M) / (R * T_mean) [kg] *)
rObs_TotalN2Inventory_kg := ((rVoted_TubeN2Press_bar * 1.0e5) * c_rCVTubeInternalVolume_m3 * c_rNitrogenMolarMass_kgmol) /
                            (c_rUniversalGasConstant_R * (0.5 * (rVoted_Zone1Temp_degC + rAmbientTemperature_degC) + 273.15));

(* Saturation Vapor Pressure of Volatile DCP Byproducts (Acetophenone + Cumyl Alcohol + Methane)
 * Modelled via Antoine-type Exponential Relation [bar]:
 * P_vap = 0.015 * EXP(0.0135 * T_melt) *)
rObs_ByproductVaporPressure_bar := 0.015 * EXP(0.0135 * rVoted_ExtruderMeltTemp_degC) + 0.120;

(* Dynamic Suppression Overpressure Margin [bar] *)
rCalculated_SuppressionMargin_bar := rVoted_TubeN2Press_bar - rObs_ByproductVaporPressure_bar;
rObs_DynamicSuppressionMargin_bar := rCalculated_SuppressionMargin_bar;

(* Estimated Mechanical Seal Leakage Mass Flow [kg/h] *)
rCalculated_N2MassFlowLeak_kgh := 0.125 * SQRT(MAX(0.0, rVoted_TubeN2Press_bar - 1.013));
rObs_CalculatedSealLeakRate_kgh := rCalculated_N2MassFlowLeak_kgh;

(* ---------------------------------------------------------------------------------------------------------------------
 * 2.4 Hydrostatic Quench Seal Boundary & Forced Convection Heat Transfer Observer
 * --------------------------------------------------------------------------------------------------------------------- *)
(* Hydrostatic Boundary Balance Check: Delta_P_seal = P_water - P_N2 *)
IF (rVoted_SealDiffPress_bar >= 0.150) AND (rVoted_SealDiffPress_bar <= 0.350) THEN
    bHydrostaticSealBalanced := TRUE;
ELSE
    bHydrostaticSealBalanced := FALSE;
END_IF;

(* Thermal Heat Removal Duty in Quench Cooling Leg [kW]:
 * Q_quench = m_dot_cable * (C_p_Cu * Delta_T_Cu + C_p_XLPE * Delta_T_XLPE) *)
IF rVoted_LinePullSpeed_mpm > 0.1 THEN
    rObs_QuenchWaterHeatDuty_kW := ((rObs_CableLinearMass_kgm * (rVoted_LinePullSpeed_mpm / 60.0)) *
                                    (0.40 * c_rCopperSpecificHeat_J_kgK + 0.60 * c_rXLPE_SpecificHeat_J_kgK) *
                                    (rVoted_ExtruderMeltTemp_degC - 45.0)) / 1000.0;
ELSE
    rObs_QuenchWaterHeatDuty_kW := 0.0;
END_IF;

rCalculated_QuenchCoolingDuty_kW := rObs_QuenchWaterHeatDuty_kW;

(* ---------------------------------------------------------------------------------------------------------------------
 * 2.5 In-Line 8-Axis Ultrasonic Scanner & Eccentricity Vector Observer
 * --------------------------------------------------------------------------------------------------------------------- *)
(* Temperature-Compensated Speed of Sound in XLPE [m/s]:
 * c_XLPE(T) = c_0 - beta_T * (T_insul - 20.0) *)
rUS_SpeedOfSound_mps := c_rXLPE_AcousticVelocity_c0 - (c_rXLPE_AcousticTempSlope_beta * (rVoted_ExtruderMeltTemp_degC - 20.0));
IF rUS_SpeedOfSound_mps < 1350.0 THEN
    rUS_SpeedOfSound_mps := 1350.0; (* Physical acoustic velocity lower bound *)
END_IF;

(* Compute 8 Radial Wall Thicknesses from Ultrasonic Pulse Time-of-Flight [mm]:
 * d_i = 0.5 * c_XLPE * Delta_t_i *)
aUS_WallThickness_mm[0] := 0.5 * rUS_SpeedOfSound_mps * (rUS_TransitTime_000deg_us * 1.0e-6) * 1000.0;
aUS_WallThickness_mm[1] := 0.5 * rUS_SpeedOfSound_mps * (rUS_TransitTime_045deg_us * 1.0e-6) * 1000.0;
aUS_WallThickness_mm[2] := 0.5 * rUS_SpeedOfSound_mps * (rUS_TransitTime_090deg_us * 1.0e-6) * 1000.0;
aUS_WallThickness_mm[3] := 0.5 * rUS_SpeedOfSound_mps * (rUS_TransitTime_135deg_us * 1.0e-6) * 1000.0;
aUS_WallThickness_mm[4] := 0.5 * rUS_SpeedOfSound_mps * (rUS_TransitTime_180deg_us * 1.0e-6) * 1000.0;
aUS_WallThickness_mm[5] := 0.5 * rUS_SpeedOfSound_mps * (rUS_TransitTime_225deg_us * 1.0e-6) * 1000.0;
aUS_WallThickness_mm[6] := 0.5 * rUS_SpeedOfSound_mps * (rUS_TransitTime_270deg_us * 1.0e-6) * 1000.0;
aUS_WallThickness_mm[7] := 0.5 * rUS_SpeedOfSound_mps * (rUS_TransitTime_315deg_us * 1.0e-6) * 1000.0;

(* Statistical Evaluation: Min, Max, Arithmetic Mean *)
rUS_MinWallThickness_mm := aUS_WallThickness_mm[0];
rUS_MaxWallThickness_mm := aUS_WallThickness_mm[0];
rTempSum := 0.0;

FOR nLoop_i := 0 TO 7 DO
    IF aUS_WallThickness_mm[nLoop_i] < rUS_MinWallThickness_mm THEN
        rUS_MinWallThickness_mm := aUS_WallThickness_mm[nLoop_i];
    END_IF;
    IF aUS_WallThickness_mm[nLoop_i] > rUS_MaxWallThickness_mm THEN
        rUS_MaxWallThickness_mm := aUS_WallThickness_mm[nLoop_i];
    END_IF;
    rTempSum := rTempSum + aUS_WallThickness_mm[nLoop_i];
END_FOR;

rUS_MeanWallThickness_mm := rTempSum / 8.0;

(* Spatial Eccentricity Vector (e_x, e_y) Evaluation via Trigonometric Projection:
 * e_x = (1/4) * Sum [ d_i * cos(theta_i) ]
 * e_y = (1/4) * Sum [ d_i * sin(theta_i) ] *)
rUS_EccentricityVector_X_mm := 0.25 * (
    (aUS_WallThickness_mm[0] * 1.0000) +
    (aUS_WallThickness_mm[1] * 0.7071) +
    (aUS_WallThickness_mm[2] * 0.0000) +
    (aUS_WallThickness_mm[3] * -0.7071) +
    (aUS_WallThickness_mm[4] * -1.0000) +
    (aUS_WallThickness_mm[5] * -0.7071) +
    (aUS_WallThickness_mm[6] * 0.0000) +
    (aUS_WallThickness_mm[7] * 0.7071)
);

rUS_EccentricityVector_Y_mm := 0.25 * (
    (aUS_WallThickness_mm[0] * 0.0000) +
    (aUS_WallThickness_mm[1] * 0.7071) +
    (aUS_WallThickness_mm[2] * 1.0000) +
    (aUS_WallThickness_mm[3] * 0.7071) +
    (aUS_WallThickness_mm[4] * 0.0000) +
    (aUS_WallThickness_mm[5] * -0.7071) +
    (aUS_WallThickness_mm[6] * -1.0000) +
    (aUS_WallThickness_mm[7] * -0.7071)
);

rCalculated_EccentricityVector_X_mm := rUS_EccentricityVector_X_mm;
rCalculated_EccentricityVector_Y_mm := rUS_EccentricityVector_Y_mm;

(* Eccentricity Ratio E_pct = ((d_max - d_min) / d_max) * 100.0 % *)
IF rUS_MaxWallThickness_mm > 0.1 THEN
    rUS_EccentricityRatio_pct := ((rUS_MaxWallThickness_mm - rUS_MinWallThickness_mm) / rUS_MaxWallThickness_mm) * 100.0;
ELSE
    rUS_EccentricityRatio_pct := 0.0;
END_IF;

rCalculated_WallEccentricity_pct := rUS_EccentricityRatio_pct;

IF rCalculated_WallEccentricity_pct > rSet_MaxAllowableEccentricity_pct THEN
    bEccentricityAlarmActive := TRUE;
ELSE
    bEccentricityAlarmActive := FALSE;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * 2.6 Dual Caterpillar Capstan Tension & Electronic Line Shaft Synchronization
 * --------------------------------------------------------------------------------------------------------------------- *)
rCapstan_InfeedActualSpeed_mpm  := rVoted_LinePullSpeed_mpm;
rCapstan_HaulOffActualSpeed_mpm := rVoted_LinePullSpeed_mpm;
rCapstan_ElectronicShaftError_mpm := rCapstan_HaulOffActualSpeed_mpm - rCapstan_InfeedActualSpeed_mpm;

(* Capstan Electronic Line Shaft Tension Closed-Loop Trim:
 * Delta_H = K_p * (H_ref - H_act) + K_i * Integral(H_ref - H_act) *)
rCapstan_TensionIntegralAccum_kN := rCapstan_TensionIntegralAccum_kN + (rSet_HaulOffTension_kN - rVoted_HaulOffTension_kN) * c_rTs;
IF rCapstan_TensionIntegralAccum_kN > 25.0 THEN
    rCapstan_TensionIntegralAccum_kN := 25.0;
ELSIF rCapstan_TensionIntegralAccum_kN < -25.0 THEN
    rCapstan_TensionIntegralAccum_kN := -25.0;
END_IF;
"""

if __name__ == "__main__":
    s3 = get_sec3()
    print("Section 3 Length:", len(s3))
