# lyophilizer_builder/build_st_phase2_sublimation.py

def get_phase2_sublimation():
    return """(* === PHASE 2: FIRST-PRINCIPLES SUBLIMATION KINETICS & THERMAL FLUID BALANCING === *)
(* ---------------------------------------------------------------------------------------------------- *)
(* CLAUSIUS-CLAPEYRON / GOFF-GRATCH ICE SATURATION VAPOR PRESSURE                                       *)
(* Calculates equilibrium vapor pressure of pure ice at moving boundary interface temperature x3       *)
(* ---------------------------------------------------------------------------------------------------- *)
IF vecX_hat[3] < 0.01 THEN
    (* Formula: P_ice = 6.1121 * EXP((22.587 * T_p) / (273.86 + T_p)) [mbar] *)
    rTempExpArg := (22.5870 * vecX_hat[3]) / (273.860 + vecX_hat[3]);
    (* Numerical bounding to prevent float overflow/underflow *)
    IF rTempExpArg < -25.0 THEN
        rTempExpArg := -25.0;
    ELSIF rTempExpArg > 5.0 THEN
        rTempExpArg := 5.0;
    END_IF;
    rTempExpVal := EXP(rTempExpArg);
    rP_ice_sat := 6.11210 * rTempExpVal;
ELSE
    rP_ice_sat := 6.11210; (* Liquid / triple-point boundary clamp *)
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* DYNAMIC CAKE DRIED LAYER RESISTANCE (R_p) & TOTAL FLOW IMPEDANCE (R_total)                           *)
(* ---------------------------------------------------------------------------------------------------- *)
rR_p_dyn := rCake_R0 + ((rCake_A * vecX_hat[6]) / (1.00 + (rCake_B * vecX_hat[6])));
rR_total := rR_p_dyn + rStopper_Rs;

(* Sublimation Vapor Mass Flux [kg/(m2*s)] *)
IF (rP_ice_sat > rVotedCap) AND (rVotedCap > 0.001) AND (rR_total > 1000.0) THEN
    rSublimationFlux_kgm2s := (rP_ice_sat - rVotedCap) / rR_total;
ELSE
    rSublimationFlux_kgm2s := 0.0;
END_IF;

(* Batch Sublimation Flow Rate [kg/s] and [kg/h] *)
rSublimationRate_kg_s := rSublimationFlux_kgm2s * rCakeArea_m2;
rCalculatedSublimationRate_kgh := rSublimationRate_kg_s * 3600.0;

(* Dynamic Cake Dried Layer Growth Integration *)
IF (nFsmState = 8) OR (nFsmState = 9) OR (nFsmState = 10) THEN
    rCumulativeSublimedMass_kg := MIN(rTotalCakeMassInitial_kg, rCumulativeSublimedMass_kg + (rSublimationRate_kg_s * tScanInterval_s));
    IF rTotalCakeMassInitial_kg > 0.1 THEN
        vecX_hat[6] := (rCumulativeSublimedMass_kg / rTotalCakeMassInitial_kg) * rCakeThicknessMax_mm;
    END_IF;
END_IF;
rEstimatedCakeDryLayer_mm := vecX_hat[6];

(* ---------------------------------------------------------------------------------------------------- *)
(* PIKAL OVERALL VIAL HEAT TRANSFER COEFFICIENT (K_v)                                                   *)
(* Combines glass contact conduction and rarefied gas molecular conduction                              *)
(* ---------------------------------------------------------------------------------------------------- *)
IF rVotedCap > 0.0 THEN
    rKv_heat_transfer := (rPikal_av + ((rPikal_bv * rVotedCap) / (1.00 + (rPikal_cv * rVotedCap)))) * 10000.0; (* [W/(m2*K)] *)
ELSE
    rKv_heat_transfer := rPikal_av * 10000.0;
END_IF;

(* Sublimation Interface Energy Balance Update *)
rEstimatedProductInterfaceTemp := vecX_hat[3];

(* ---------------------------------------------------------------------------------------------------- *)
(* 16 SHELVES SILICONE OIL THERMAL UNIFORMITY PROFILES                                                  *)
(* ---------------------------------------------------------------------------------------------------- *)
rShelfAvgInletTemp := 0.0;
rShelfAvgOutletTemp := 0.0;
rShelfMinTemp := 150.0;
rShelfMaxTemp := -100.0;

FOR iShelf := 1 TO 16 DO
    rShelfAvgInletTemp := rShelfAvgInletTemp + rShelfInletTemps[iShelf];
    rShelfAvgOutletTemp := rShelfAvgOutletTemp + rShelfOutletTemps[iShelf];

    IF rShelfInletTemps[iShelf] < rShelfMinTemp THEN
        rShelfMinTemp := rShelfInletTemps[iShelf];
    END_IF;
    IF rShelfInletTemps[iShelf] > rShelfMaxTemp THEN
        rShelfMaxTemp := rShelfInletTemps[iShelf];
    END_IF;
END_FOR;

rShelfAvgInletTemp := rShelfAvgInletTemp / 16.0;
rShelfAvgOutletTemp := rShelfAvgOutletTemp / 16.0;

(* Calculate Shelf Temperature Variance and Standard Deviation *)
rShelfTempVariance := 0.0;
FOR iShelf := 1 TO 16 DO
    rTempShelfDiff := rShelfInletTemps[iShelf] - rShelfAvgInletTemp;
    rShelfTempVariance := rShelfTempVariance + (rTempShelfDiff * rTempShelfDiff);
END_FOR;
rShelfTempVariance := rShelfTempVariance / 16.0;
IF rShelfTempVariance > 0.00001 THEN
    rShelfTempStdDev := SQRT(rShelfTempVariance);
ELSE
    rShelfTempStdDev := 0.0;
END_IF;

rShelfTempUniformityDelta_degC := rShelfMaxTemp - rShelfMinTemp;

(* ---------------------------------------------------------------------------------------------------- *)
(* PIRANI VS. CAPACITANCE MANOMETER RATIO (ENDPOINT PROXY ALGORITHM)                                    *)
(* During sublimation, water vapor causes Pirani to read ~1.55 - 1.65x higher than Capacitance.        *)
(* Upon primary drying completion, water vapor ceases, ratio converges towards 1.00 (<= 1.05).         *)
(* ---------------------------------------------------------------------------------------------------- *)
IF rVotedCap > 0.005 THEN
    rFilteredPiraniCapRatio := ((1.00 - rPiraniCapAlpha) * rFilteredPiraniCapRatio) +
                               (rPiraniCapAlpha * (rVotedPirani / rVotedCap));
ELSE
    rFilteredPiraniCapRatio := 1.0;
END_IF;
rPiraniCapPressureRatio := rFilteredPiraniCapRatio;

(* ---------------------------------------------------------------------------------------------------- *)
(* MANOMETRIC TEMPERATURE MEASUREMENT (MTM) / PRESSURE RISE TEST (PRT)                                  *)
(* ---------------------------------------------------------------------------------------------------- *)
IF (nFsmState = 8) AND NOT bPRT_Active THEN
    (* Check for periodic PRT trigger *)
    IF rElapsedCycleTime_s >= tPRT_NextTrigger_s THEN
        bPRT_Trigger := TRUE;
    END_IF;
END_IF;

IF bPRT_Active THEN
    tPRT_Timer_s := tPRT_Timer_s + tScanInterval_s;
    IF tPRT_Timer_s >= 30.0 THEN
        (* 30-Second Measurement Window Reached *)
        rPRT_EndPress_mbar := rVotedCap;
        rPRT_DeltaPress_mbar := MAX(0.0, rPRT_EndPress_mbar - rPRT_StartPress_mbar);
        rPRT_LeakRate_mbar_s := rPRT_DeltaPress_mbar / 30.0;

        (* Sublimation endpoint qualification: rise rate <= 0.0005 mbar/s *)
        IF rPRT_LeakRate_mbar_s <= 0.0005 THEN
            bPRT_Passed := TRUE;
        ELSE
            bPRT_Passed := FALSE;
        END_IF;

        (* Re-open chamber isolation valve *)
        bCmd_ChamberIsolationValve := TRUE;
        bPRT_Active := FALSE;
        tPRT_Timer_s := 0.0;
        tPRT_NextTrigger_s := rElapsedCycleTime_s + tPRT_Interval_s;
    END_IF;
END_IF;
"""
