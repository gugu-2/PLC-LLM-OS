# -*- coding: utf-8 -*-
"""
cement_kiln_builder/part4_state_space_observer.py
Part 4: Phase 2 - First-Principles Cyber-Physical State-Space Estimation & Observer Innovation
Thermodynamic calculations, calcination kinetics, sintering exotherm,
rotary kiln mechanical torque, grate cooler heat recuperation, and full 6x6 Luenberger observer.
"""

def get_part4_state_space_observer():
    return """
(* ========================================================================================================= *)
(* === PHASE 2: FIRST-PRINCIPLES CYBER-PHYSICAL STATE-SPACE ESTIMATION & OBSERVER INNOVATION             === *)
(* ========================================================================================================= *)

(* --------------------------------------------------------------------------------------------------------- *)
(* SUBSECTION 2.1: RAW MEAL CALCINATION THERMOCHEMICAL KINETICS & ENTHALPY BALANCE                           *)
(* Reaction: CaCO3 (solid) -> CaO (solid) + CO2 (gas)  [Delta H_r = +178.2 kJ/mol = +1,782 kJ/kg CaCO3]      *)
(* --------------------------------------------------------------------------------------------------------- *)
(* Estimated hourly clinker production based on raw meal feed (typical raw mix to clinker ratio ~ 1.55) *)
IF rKiln_RawMealFeed_Rate_tph > 10.0 THEN
    rHourlyClinkerProduction_tph := rKiln_RawMealFeed_Rate_tph / 1.550;
ELSE
    rHourlyClinkerProduction_tph := 0.0;
END_IF;

(* Mass flow rate of limestone CaCO3 entering pyroprocessing loop (typically 76.5 wt% of raw mix) *)
(* Endothermic heat absorption rate: Q_decarb [kW] = m_dot_CaCO3 [kg/s] * Delta_H_calc [kJ/kg] * DecarbDegree *)
IF (rHourlyClinkerProduction_tph > 1.0) AND (rVoted_Calciner_Temp > 600.0) THEN
    rEnthalpyDecarbonation_kW := (rKiln_RawMealFeed_Rate_tph * 0.765 * 1000.0 / 3600.0) * 1782.0 * (rState_x_hat[4] / 100.0);
ELSE
    rEnthalpyDecarbonation_kW := 0.0;
END_IF;

(* Process CO2 mass release from CaCO3 chemical decomposition (0.440 kg CO2 per kg CaCO3) *)
rCalculated_CO2_Emission_tph := (rKiln_RawMealFeed_Rate_tph * 0.765) * 0.440 * (rState_x_hat[4] / 100.0);

(* --------------------------------------------------------------------------------------------------------- *)
(* SUBSECTION 2.2: SINTERING ZONE RADIATIVE HEAT TRANSFER & EXOTHERMIC CLINKERIZATION                       *)
(* Stefan-Boltzmann flame radiation to clinker bed and exothermic alite/belite crystallization                *)
(* --------------------------------------------------------------------------------------------------------- *)
(* Effective flame temperature proxy based on coal feed rate and primary combustion air *)
rStefanBoltzmann_Radiation_kW := 5.67037E-8 * 0.88 * 38.5 * (EXPT((rVoted_BurnZone_Temp + 273.15 + 450.0), 4) - EXPT((rVoted_BurnZone_Temp + 273.15), 4)) / 1000.0;

(* Exothermic enthalpy release during C3S and C2S crystal formation: ~420 kJ/kg clinker *)
IF (rVoted_BurnZone_Temp >= 1350.0) AND (rHourlyClinkerProduction_tph > 5.0) THEN
    rEnthalpyClinkerExotherm_kW := (rHourlyClinkerProduction_tph * 1000.0 / 3600.0) * 420.0;
ELSE
    rEnthalpyClinkerExotherm_kW := 0.0;
END_IF;

(* --------------------------------------------------------------------------------------------------------- *)
(* SUBSECTION 2.3: GRATE COOLER RECUPERATION ENTHALPY & SPECIFIC HEAT CONSUMPTION                            *)
(* Heat recuperation: Secondary air (to main burner) and Tertiary air (to precalciner furnace)               *)
(* --------------------------------------------------------------------------------------------------------- *)
(* Secondary air mass flow estimation (typically ~0.85 Nm3/kg clinker, cp_air ~ 1.25 kJ/Nm3.K) *)
IF (rHourlyClinkerProduction_tph > 5.0) AND (rCooler_SecondaryAir_Temp_degC > 150.0) THEN
    rRecuperatedSecondaryAirEnthalpy_kW := (rHourlyClinkerProduction_tph * 1000.0 * 0.85 / 3600.0) * 1.25 * (rCooler_SecondaryAir_Temp_degC - 25.0);
ELSE
    rRecuperatedSecondaryAirEnthalpy_kW := 0.0;
END_IF;

(* Tertiary air mass flow estimation (typically ~0.95 Nm3/kg clinker, cp_air ~ 1.22 kJ/Nm3.K) *)
IF (rHourlyClinkerProduction_tph > 5.0) AND (rCooler_TertiaryAir_Temp_degC > 150.0) THEN
    rRecuperatedTertiaryAirEnthalpy_kW := (rHourlyClinkerProduction_tph * 1000.0 * 0.95 / 3600.0) * 1.22 * (rCooler_TertiaryAir_Temp_degC - 25.0);
ELSE
    rRecuperatedTertiaryAirEnthalpy_kW := 0.0;
END_IF;

(* Total fuel energy input: Coal LHV ~ 26.5 GJ/ton, Calciner fuel LHV ~ 24.0 GJ/ton, Tires/RDF ~ 28.0 GJ/ton *)
rTotalFuelHeatInput_GJ_per_h := (rActuator_u[1] * 26.5) + (rActuator_u[2] * 24.0) + (rAltFuel_TireRDF_Feed_tph * 28.0);

(* Real-Time Specific Heat Consumption: Target 2,950 - 3,150 MJ/ton clinker (2.95 - 3.15 MJ/kg clinker) *)
IF rHourlyClinkerProduction_tph > 10.0 THEN
    rCalculated_SpecificHeat_MJ_per_kg := (rTotalFuelHeatInput_GJ_per_h * 1000.0) / (rHourlyClinkerProduction_tph * 1000.0);
ELSE
    rCalculated_SpecificHeat_MJ_per_kg := 3.100; (* Baseline nominal placeholder during startup *)
END_IF;

(* --------------------------------------------------------------------------------------------------------- *)
(* SUBSECTION 2.4: KILN MECHANICAL ROTATIONAL RESISTANCE & BED VOLUMETRIC FILL                               *)
(* Bed volume loading percent (% Fill) and resistance torque model                                           *)
(* --------------------------------------------------------------------------------------------------------- *)
(* Volumetric fill degree: % Fill = (F_meal / (rho_bulk * pi/4 * D^2 * v_axial)) * 100 *)
IF (rActuator_u[3] > 0.1) AND (rKiln_RawMealFeed_Rate_tph > 5.0) THEN
    (* Bulk density rho ~ 1.45 t/m3, Kiln diameter D = 5.6 m, Axial velocity proportional to RPM * Slope *)
    rCalculated_KilnFillDegree_pct := (rKiln_RawMealFeed_Rate_tph / (1.45 * 3.14159 * 2.8 * 2.8 * (rActuator_u[3] * 0.035 * 60.0))) * 100.0;
    rCalculated_KilnFillDegree_pct := LIMIT(5.0, rCalculated_KilnFillDegree_pct, 22.0);
ELSE
    rCalculated_KilnFillDegree_pct := 0.0;
END_IF;

(* Kiln Shell Exterior Convection and Radiation Losses (D = 5.6 m, L = 88 m, Area = 1,548 m2) *)
rShellConvectiveLoss_kW := (15.5 * 1548.0 * (rState_x_hat[3] - 25.0) + 5.67037E-8 * 0.90 * 1548.0 * (EXPT(rState_x_hat[3] + 273.15, 4) - EXPT(298.15, 4))) / 1000.0;

(* --------------------------------------------------------------------------------------------------------- *)
(* SUBSECTION 2.5: MEASUREMENT VECTOR FORMATION FROM VOTED SENSORS                                           *)
(* --------------------------------------------------------------------------------------------------------- *)
rState_y_meas[1] := rVoted_BurnZone_Temp;
rState_y_meas[2] := rVoted_Calciner_Temp;
rState_y_meas[3] := rKilnShell_MaxHotSpot_degC;
rState_y_meas[4] := rPrecalciner_Calcination_Offline_pct;
rState_y_meas[5] := rKilnDrive_ActualTorque_kNm;
rState_y_meas[6] := rVoted_KilnInlet_CO;

(* --------------------------------------------------------------------------------------------------------- *)
(* SUBSECTION 2.6: DISCRETE STATE PREDICTION x_pred[k+1] = A * x_hat[k] + B * u[k]                           *)
(* Explicitly unrolled 6x6 matrix multiplication                                                             *)
(* --------------------------------------------------------------------------------------------------------- *)
rState_x_pred[1] := (A[1, 1] * rState_x_hat[1]) + (A[1, 2] * rState_x_hat[2]) + (A[1, 3] * rState_x_hat[3]) +
                    (A[1, 4] * rState_x_hat[4]) + (A[1, 5] * rState_x_hat[5]) + (A[1, 6] * rState_x_hat[6]) +
                    (B[1, 1] * rActuator_u[1])  + (B[1, 2] * rActuator_u[2])  + (B[1, 3] * rActuator_u[3])  +
                    (B[1, 4] * rActuator_u[4])  + (B[1, 5] * rActuator_u[5]);

rState_x_pred[2] := (A[2, 1] * rState_x_hat[1]) + (A[2, 2] * rState_x_hat[2]) + (A[2, 3] * rState_x_hat[3]) +
                    (A[2, 4] * rState_x_hat[4]) + (A[2, 5] * rState_x_hat[5]) + (A[2, 6] * rState_x_hat[6]) +
                    (B[2, 1] * rActuator_u[1])  + (B[2, 2] * rActuator_u[2])  + (B[2, 3] * rActuator_u[3])  +
                    (B[2, 4] * rActuator_u[4])  + (B[2, 5] * rActuator_u[5]);

rState_x_pred[3] := (A[3, 1] * rState_x_hat[1]) + (A[3, 2] * rState_x_hat[2]) + (A[3, 3] * rState_x_hat[3]) +
                    (A[3, 4] * rState_x_hat[4]) + (A[3, 5] * rState_x_hat[5]) + (A[3, 6] * rState_x_hat[6]) +
                    (B[3, 1] * rActuator_u[1])  + (B[3, 2] * rActuator_u[2])  + (B[3, 3] * rActuator_u[3])  +
                    (B[3, 4] * rActuator_u[4])  + (B[3, 5] * rActuator_u[5]);

rState_x_pred[4] := (A[4, 1] * rState_x_hat[1]) + (A[4, 2] * rState_x_hat[2]) + (A[4, 3] * rState_x_hat[3]) +
                    (A[4, 4] * rState_x_hat[4]) + (A[4, 5] * rState_x_hat[5]) + (A[4, 6] * rState_x_hat[6]) +
                    (B[4, 1] * rActuator_u[1])  + (B[4, 2] * rActuator_u[2])  + (B[4, 3] * rActuator_u[3])  +
                    (B[4, 4] * rActuator_u[4])  + (B[4, 5] * rActuator_u[5]);

rState_x_pred[5] := (A[5, 1] * rState_x_hat[1]) + (A[5, 2] * rState_x_hat[2]) + (A[5, 3] * rState_x_hat[3]) +
                    (A[5, 4] * rState_x_hat[4]) + (A[5, 5] * rState_x_hat[5]) + (A[5, 6] * rState_x_hat[6]) +
                    (B[5, 1] * rActuator_u[1])  + (B[5, 2] * rActuator_u[2])  + (B[5, 3] * rActuator_u[3])  +
                    (B[5, 4] * rActuator_u[4])  + (B[5, 5] * rActuator_u[5]);

rState_x_pred[6] := (A[6, 1] * rState_x_hat[1]) + (A[6, 2] * rState_x_hat[2]) + (A[6, 3] * rState_x_hat[3]) +
                    (A[6, 4] * rState_x_hat[4]) + (A[6, 5] * rState_x_hat[5]) + (A[6, 6] * rState_x_hat[6]) +
                    (B[6, 1] * rActuator_u[1])  + (B[6, 2] * rActuator_u[2])  + (B[6, 3] * rActuator_u[3])  +
                    (B[6, 4] * rActuator_u[4])  + (B[6, 5] * rActuator_u[5]);

(* --------------------------------------------------------------------------------------------------------- *)
(* SUBSECTION 2.7: INNOVATION RESIDUAL CALCULATION y_innov = y_meas - C * x_pred                             *)
(* --------------------------------------------------------------------------------------------------------- *)
FOR rLoop_idx_i := 1 TO 6 DO
    rState_y_innov[rLoop_idx_i] := rState_y_meas[rLoop_idx_i] - rState_x_pred[rLoop_idx_i];
END_FOR;

(* --------------------------------------------------------------------------------------------------------- *)
(* SUBSECTION 2.8: LUENBERGER OBSERVER UPDATE x_hat[k+1] = x_pred + L * y_innov                              *)
(* Full 6x6 innovation correction                                                                            *)
(* --------------------------------------------------------------------------------------------------------- *)
rState_x_hat[1] := rState_x_pred[1] + (L[1, 1] * rState_y_innov[1]) + (L[1, 2] * rState_y_innov[2]) +
                   (L[1, 3] * rState_y_innov[3]) + (L[1, 4] * rState_y_innov[4]) +
                   (L[1, 5] * rState_y_innov[5]) + (L[1, 6] * rState_y_innov[6]);

rState_x_hat[2] := rState_x_pred[2] + (L[2, 1] * rState_y_innov[1]) + (L[2, 2] * rState_y_innov[2]) +
                   (L[2, 3] * rState_y_innov[3]) + (L[2, 4] * rState_y_innov[4]) +
                   (L[2, 5] * rState_y_innov[5]) + (L[2, 6] * rState_y_innov[6]);

rState_x_hat[3] := rState_x_pred[3] + (L[3, 1] * rState_y_innov[1]) + (L[3, 2] * rState_y_innov[2]) +
                   (L[3, 3] * rState_y_innov[3]) + (L[3, 4] * rState_y_innov[4]) +
                   (L[3, 5] * rState_y_innov[5]) + (L[3, 6] * rState_y_innov[6]);

rState_x_hat[4] := rState_x_pred[4] + (L[4, 1] * rState_y_innov[1]) + (L[4, 2] * rState_y_innov[2]) +
                   (L[4, 3] * rState_y_innov[3]) + (L[4, 4] * rState_y_innov[4]) +
                   (L[4, 5] * rState_y_innov[5]) + (L[4, 6] * rState_y_innov[6]);

rState_x_hat[5] := rState_x_pred[5] + (L[5, 1] * rState_y_innov[1]) + (L[5, 2] * rState_y_innov[2]) +
                   (L[5, 3] * rState_y_innov[3]) + (L[5, 4] * rState_y_innov[4]) +
                   (L[5, 5] * rState_y_innov[5]) + (L[5, 6] * rState_y_innov[6]);

rState_x_hat[6] := rState_x_pred[6] + (L[6, 1] * rState_y_innov[1]) + (L[6, 2] * rState_y_innov[2]) +
                   (L[6, 3] * rState_y_innov[3]) + (L[6, 4] * rState_y_innov[4]) +
                   (L[6, 5] * rState_y_innov[5]) + (L[6, 6] * rState_y_innov[6]);

(* Physical Clamping of Estimated States to Plausible Thermodynamic Bounds *)
rState_x_hat[1] := LIMIT(900.0, rState_x_hat[1], 1650.0);   (* Burning zone clinkering temperature [deg C] *)
rState_x_hat[2] := LIMIT(500.0, rState_x_hat[2], 1150.0);   (* Precalciner bottom exit gas temperature [deg C] *)
rState_x_hat[3] := LIMIT(50.0,  rState_x_hat[3], 500.0);    (* Kiln shell peak temperature [deg C] *)
rState_x_hat[4] := LIMIT(60.0,  rState_x_hat[4], 100.0);    (* Precalciner decarbonation degree [%] *)
rState_x_hat[5] := LIMIT(100.0, rState_x_hat[5], 650.0);    (* Kiln drive torque [kNm] *)
rState_x_hat[6] := LIMIT(0.00,  rState_x_hat[6], 2.50);     (* Kiln inlet CO [%] *)

(* Transfer Observer Estimates to Functional Block Outputs *)
rEst_BurningZone_Temp_degC   := rState_x_hat[1];
rEst_Precalciner_Temp_degC   := rState_x_hat[2];
rEst_KilnShell_HotSpot_degC  := rState_x_hat[3];
rEst_DecarbonationDegree_pct := rState_x_hat[4];
rEst_KilnDriveTorque_kNm     := rState_x_hat[5];
rEst_KilnInletCO_pct         := rState_x_hat[6];
"""
