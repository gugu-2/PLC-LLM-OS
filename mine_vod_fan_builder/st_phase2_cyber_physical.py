# mine_vod_fan_builder/st_phase2_cyber_physical.py

def get_phase2_cyber_physical():
    return """(* ==================================================================================================== *)
(* PHASE 2: FIRST-PRINCIPLES CYBER-PHYSICAL MINE AERODYNAMIC, THERMODYNAMIC & DISPERSION OBSERVERS     *)
(* ==================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------- *)
(* SUB-PHASE 2.1: Hydrostatic Barometric Air Density Scaling Across 2,400 m Vertical Column             *)
(* ---------------------------------------------------------------------------------------------------- *)
(* Surface Collar Ambient Air Density via Ideal Gas Law [kg/m3] *)
IF (rSurfaceAirTemp_degC + 273.15) > 220.0 THEN
    rSurfaceAirDensity_kgm3 := (rSurfaceBaroPressure_kPa * 1000.0) / (rGasConstant_Air * (rSurfaceAirTemp_degC + 273.15));
ELSE
    rSurfaceAirDensity_kgm3 := 1.225;
END_IF;

(* 2,400 m Subterranean Level Hydrostatically Compressed Air Density [kg/m3] *)
IF (rShaftBottomAirTemp_degC + 273.15) > 220.0 THEN
    rSubterraneanAirDensity_kgm3 := (rShaftBottomBaroPressure_kPa * 1000.0) / (rGasConstant_Air * (rShaftBottomAirTemp_degC + 273.15));
ELSE
    rSubterraneanAirDensity_kgm3 := 1.385;
END_IF;

(* Integrated Mean Shaft Column Air Density [kg/m3] *)
rMeanAirwayDensity_kgm3 := 0.5 * (rSurfaceAirDensity_kgm3 + rSubterraneanAirDensity_kgm3);

(* Natural Ventilation Pressure (NVP) Buoyancy Drive [kPa] *)
(* NVP = g * H * (rho_intake - rho_exhaust) / 1000 *)
rNaturalVentilationPressure_kPa := (rGravity_Acc * rShaftDepth_m * (rMeanAirwayDensity_kgm3 - rSurfaceAirDensity_kgm3 * 0.945)) / 1000.0;
IF rNaturalVentilationPressure_kPa < -1.5 THEN
    rNaturalVentilationPressure_kPa := -1.5;
ELSIF rNaturalVentilationPressure_kPa > 2.5 THEN
    rNaturalVentilationPressure_kPa := 2.5;
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* SUB-PHASE 2.2: Total Subterranean Mass Flow & Dynamic Atkinson Airway Aerodynamic Resistance         *)
(* ---------------------------------------------------------------------------------------------------- *)
(* Volumetric Flow at Exhaust Shaft Collar [m3/s] *)
rTotalAirwayVolumeFlow_m3s := rAirVel_Voted * rExhaustShaftArea_m2;
IF rTotalAirwayVolumeFlow_m3s < 10.0 THEN
    rTotalAirwayVolumeFlow_m3s := 10.0;
END_IF;

(* Total Subterranean Mass Flow Exhausted [kg/s] *)
rTotalAirwayMassFlow_kgs := rTotalAirwayVolumeFlow_m3s * rSurfaceAirDensity_kgm3;

(* Dynamic Atkinson Aerodynamic Mine Resistance Equivalent [kPa.s2/m6] *)
(* R_mine = (Delta_P_fan + NVP) / (Q_vol^2) *)
IF rTotalAirwayVolumeFlow_m3s > 25.0 THEN
    rActiveMineAtkinsonResistance_kPas2_m6 := (rDP_Voted + rNaturalVentilationPressure_kPa) / (rTotalAirwayVolumeFlow_m3s * rTotalAirwayVolumeFlow_m3s);
ELSE
    rActiveMineAtkinsonResistance_kPas2_m6 := 0.00785;
END_IF;

(* Clamp Atkinson Resistance to Physically Feasible Mine Domain *)
IF rActiveMineAtkinsonResistance_kPas2_m6 < 0.00100 THEN
    rActiveMineAtkinsonResistance_kPas2_m6 := 0.00100;
ELSIF rActiveMineAtkinsonResistance_kPas2_m6 > 0.05000 THEN
    rActiveMineAtkinsonResistance_kPas2_m6 := 0.05000;
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* SUB-PHASE 2.3: Real-Time Aerodynamic Fan Stall Boundary Calculation & Distance-to-Stall Margin (SM)  *)
(* ---------------------------------------------------------------------------------------------------- *)
(* Select Active Lead Blade Pitch Feedback Angle [deg] *)
IF bLeadFanSelect THEN
    rSortTemp := rFan2_BladePitchFeedback_deg;
ELSE
    rSortTemp := rFan1_BladePitchFeedback_deg;
END_IF;

(* Clamp Blade Pitch for Polynomial Evaluation *)
IF rSortTemp < -12.0 THEN
    rSortTemp := -12.0;
ELSIF rSortTemp > 38.0 THEN
    rSortTemp := 38.0;
END_IF;

(* Rotating Stall Boundary Volumetric Flow Q_stall(DP, theta) [m3/s] *)
(* Q_stall = s0 + s1*DP + s2*DP^2 + s3*theta + s4*theta*DP *)
rCriticalStallFlow_m3s := rStallS0 
                        + (rStallS1 * rDP_Voted) 
                        + (rStallS2 * rDP_Voted * rDP_Voted) 
                        + (rStallS3 * rSortTemp) 
                        + (rStallS4 * rSortTemp * rDP_Voted);

IF rCriticalStallFlow_m3s < 50.0 THEN
    rCriticalStallFlow_m3s := 50.0;
END_IF;

(* Operating Point Volumetric Flow Assigned *)
rOperatingPointFlow_m3s := rTotalAirwayVolumeFlow_m3s;

(* Aerodynamic Distance-to-Stall Margin Index SM [%] *)
(* SM = ((Q_actual - Q_stall) / Q_stall) * 100.0 *)
rFanStallMargin_pct := ((rOperatingPointFlow_m3s - rCriticalStallFlow_m3s) / rCriticalStallFlow_m3s) * 100.0;

(* Dynamic Blade Tip Static Turbulence Fluctuations [Pa RMS] *)
(* Tip dynamic pressure = 0.5 * rho * (omega * R_tip)^2 *)
rDynamicPressureTip_Pa := 0.5 * rSurfaceAirDensity_kgm3 * (rFan1_MotorSpeed_RPM * 0.10472 * (0.5 * rFanRotorDiameter_m)) * (rFan1_MotorSpeed_RPM * 0.10472 * (0.5 * rFanRotorDiameter_m));
IF rFanStallMargin_pct < 20.0 THEN
    rTempDelta := (20.0 - rFanStallMargin_pct) * 6.85 + (rVib_Voted * 12.5);
ELSE
    rTempDelta := 25.0 + (rVib_Voted * 4.2);
END_IF;

(* First-Order Exponential Recursive Filter for Blade Tip Turbulence *)
rFilteredTipTurbulence_Pa := ((1.0 - rTurbulenceFilterAlpha) * rFilteredTipTurbulence_Pa) + (rTurbulenceFilterAlpha * rTempDelta);
rBladeTipTurbulenceRMS_Pa := rFilteredTipTurbulence_Pa;

(* Automatic Stall Relief Precursor Detection *)
IF (rFanStallMargin_pct < rStall_Warn_L) OR (rBladeTipTurbulenceRMS_Pa > rTurb_Warn_H) THEN
    bAntiStallActive := TRUE;
ELSE
    IF rFanStallMargin_pct > (rStall_Warn_L + rStall_Hysteresis) THEN
        bAntiStallActive := FALSE;
    END_IF;
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* SUB-PHASE 2.4: Dynamic Toxic Gas Dilution Kinetics & Post-Blast Clearance Estimator                  *)
(* ---------------------------------------------------------------------------------------------------- *)
(* Dynamic Airflow Requirement for Active Diesel Fleet (MSHA 0.06 m3/s per kW) *)
rTempSum := rTotalActiveDieselPower_kW * rDieselAirflowRequirement_m3s_kW;
IF rTempSum < 120.0 THEN
    rTempSum := 120.0;
END_IF;

(* Post-Blast Gas Dilution Integration: C(t) = C0 * exp(-eta * Q * t / V) *)
IF (iActiveBlastingZoneIndex >= 1) AND (iActiveBlastingZoneIndex <= 24) THEN
    rTempDelta := arrZoneAirflowDelivery_m3s[iActiveBlastingZoneIndex];
    IF rTempDelta < 5.0 THEN
        rTempDelta := 5.0;
    END_IF;
    (* Time constant tau = V / (eta * Q) *)
    rSortTemp := rHeadingVolume_m3 / (rPurgeMixingEfficiency_eta * rTempDelta);
    (* Purge time to dilute from initial blast concentration to safe 25 ppm CO *)
    IF rToxicGas_Voted > rCO_SafeReentryLimit_ppm THEN
        rPostBlastPurgeTimeRemaining_s := rSortTemp * LN(rToxicGas_Voted / rCO_SafeReentryLimit_ppm);
    ELSE
        rPostBlastPurgeTimeRemaining_s := 0.0;
    END_IF;
ELSE
    rPostBlastPurgeTimeRemaining_s := 0.0;
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* SUB-PHASE 2.5: Thomas-Heselden-Kennedy Critical Backlayering Smoke Reversal Prevention              *)
(* ---------------------------------------------------------------------------------------------------- *)
(* Critical velocity u_c = k * ((g * Q_dot_fire * H) / (rho_air * Cp * T_fire * A))^(1/3) *)
(* Approximated around T_fire ~ 850 K *)
IF rEstimatedFireHeatRelease_MW < 0.5 THEN
    rEstimatedFireHeatRelease_MW := 0.5;
END_IF;

rCriticalBacklayeringVel_Calc := rKennedyFactor_k * EXP(0.333333 * LN((rGravity_Acc * (rEstimatedFireHeatRelease_MW * 1.0E6) * rFirePlumeHeight_m) 
                                 / (rMeanAirwayDensity_kgm3 * rSpecificHeat_Cp * 850.0 * rFireDriftArea_m2)));

IF rCriticalBacklayeringVel_Calc < 1.25 THEN
    rCriticalBacklayeringVel_Calc := 1.25;
ELSIF rCriticalBacklayeringVel_Calc > 4.50 THEN
    rCriticalBacklayeringVel_Calc := 4.50;
END_IF;

rAirwayCriticalBacklayeringVelocity_mps := rCriticalBacklayeringVel_Calc;

(* Calculate Backlayering Safety Velocity Margin *)
IF rCriticalBacklayeringVel_Calc > 0.1 THEN
    rSmokeBacklayeringMargin_pct := ((rAir_Vel_Voted - rCriticalBacklayeringVel_Calc) / rCriticalBacklayeringVel_Calc) * 100.0;
ELSE
    rSmokeBacklayeringMargin_pct := 50.0;
END_IF;

(* Engage Anti-Reversal Safety Interlock if Velocity Drops Below Critical *)
IF bFireSmokeEmergencyTrip OR (iFireZoneIndex > 0) THEN
    IF rAir_Vel_Voted < (rCriticalBacklayeringVel_Calc + 0.25) THEN
        bSmokeReversalLockEngaged := TRUE;
    ELSE
        bSmokeReversalLockEngaged := FALSE;
    END_IF;
ELSE
    bSmokeReversalLockEngaged := FALSE;
END_IF;

(* Mine Thermal Wet-Bulb Equivalent Heat Stress *)
rMineThermalHeatStressIndex_degC := rUndergroundWBGT_degC + (0.05 * (35.0 - rShaftBottomAirTemp_degC));
"""
