# mega_casting_builder/build_phase6_thermal_porosity.py

def get_phase6_thermal_porosity():
    return """(* =====================================================================================================================
 * PHASE 6: MULTI-CIRCUIT THERMAL OIL PID REGULATION & CYBER-PHYSICAL POROSITY PREDICTION ENGINE
 * Dual-die half oil balancing + Weiler-Niyama multi-factor porosity risk index computation
 * ===================================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------------------------
 * 1. MULTI-CIRCUIT THERMAL OIL PARALLEL PID CONTROLLERS WITH ANTI-WINDUP
 * Regulates fixed and moving platen die inserts to setpoint rRecipe_DieTemp_Target_degC
 * --------------------------------------------------------------------------------------------------------------------- *)
(* Fixed Die Half PID Loop *)
rThermal_Integral_Fixed := rThermal_Integral_Fixed + ((rRecipe_DieTemp_Target_degC - rFixedDie_Temp_Actual) * rScanDeltaT);
(* Anti-windup clamping [-100.0, 100.0] *)
IF rThermal_Integral_Fixed > 100.0 THEN
    rThermal_Integral_Fixed := 100.0;
ELSIF rThermal_Integral_Fixed < -100.0 THEN
    rThermal_Integral_Fixed := -100.0;
END_IF;

IF rScanDeltaT > 0.00001 THEN
    rThermal_Oil_Fixed_Cmd := (rThermal_Kp * (rRecipe_DieTemp_Target_degC - rFixedDie_Temp_Actual)) +
                              (rThermal_Ki * rThermal_Integral_Fixed) +
                              (rThermal_Kd * ((rRecipe_DieTemp_Target_degC - rFixedDie_Temp_Actual) - rThermal_PrevError_Fixed) / rScanDeltaT);
END_IF;
rThermal_PrevError_Fixed := rRecipe_DieTemp_Target_degC - rFixedDie_Temp_Actual;

(* Moving Die Half PID Loop *)
rThermal_Integral_Moving := rThermal_Integral_Moving + ((rRecipe_DieTemp_Target_degC - rMovingDie_Temp_Actual) * rScanDeltaT);
IF rThermal_Integral_Moving > 100.0 THEN
    rThermal_Integral_Moving := 100.0;
ELSIF rThermal_Integral_Moving < -100.0 THEN
    rThermal_Integral_Moving := -100.0;
END_IF;

IF rScanDeltaT > 0.00001 THEN
    rThermal_Oil_Moving_Cmd := (rThermal_Kp * (rRecipe_DieTemp_Target_degC - rMovingDie_Temp_Actual)) +
                               (rThermal_Ki * rThermal_Integral_Moving) +
                               (rThermal_Kd * ((rRecipe_DieTemp_Target_degC - rMovingDie_Temp_Actual) - rThermal_PrevError_Moving) / rScanDeltaT);
END_IF;
rThermal_PrevError_Moving := rRecipe_DieTemp_Target_degC - rMovingDie_Temp_Actual;

(* Dynamic Thermal Cross-Balancing: Bias oil cooling to hotter die half *)
IF (rFixedDie_Temp_Actual - rMovingDie_Temp_Actual) > 8.0 THEN
    rThermal_Oil_Fixed_Cmd := rThermal_Oil_Fixed_Cmd + 15.0; (* Extra cooling to fixed die *)
ELSIF (rMovingDie_Temp_Actual - rFixedDie_Temp_Actual) > 8.0 THEN
    rThermal_Oil_Moving_Cmd := rThermal_Oil_Moving_Cmd + 15.0; (* Extra cooling to moving die *)
END_IF;

(* Average Thermal Oil Trim Command for State-Space & Actuator Output *)
rThermalOil_Valve_Cmd := (rThermal_Oil_Fixed_Cmd + rThermal_Oil_Moving_Cmd) * 0.5;
IF rThermalOil_Valve_Cmd < 0.0 THEN
    rThermalOil_Valve_Cmd := 0.0;
ELSIF rThermalOil_Valve_Cmd > 100.0 THEN
    rThermalOil_Valve_Cmd := 100.0;
END_IF;

(* Measure In-Die Solidification Cooling Rate [deg C/s] *)
IF rScanDeltaT > 0.00001 THEN
    rSolidification_CoolingRate_C_s := ABS(rFixedDie_Temp_Actual - rPrev_FixedDie_Temp) / rScanDeltaT;
END_IF;
rPrev_FixedDie_Temp := rFixedDie_Temp_Actual;

(* ---------------------------------------------------------------------------------------------------------------------
 * 2. CYBER-PHYSICAL POROSITY PREDICTION & QUALITY CLASSIFICATION ENGINE
 * Evaluates Gas Entrapment, Liquid-to-Solid Shrinkage Feeding, and Thermal Gradient
 * --------------------------------------------------------------------------------------------------------------------- *)

(* Factor 2.1: Gas Entrapment Porosity Factor (Driven by Parting Vacuum & Wave Break) *)
IF rVacPressure_Voted <= 25.0 THEN
    rPorosity_GasEntrap_Factor := 0.05; (* Clean vacuum fill: near-zero gas porosity *)
ELSIF rVacPressure_Voted <= 50.0 THEN
    rPorosity_GasEntrap_Factor := 0.05 + ((rVacPressure_Voted - 25.0) / 25.0) * 0.25;
ELSE
    rPorosity_GasEntrap_Factor := 0.30 + ((rVacPressure_Voted - 50.0) / 100.0) * 0.70;
END_IF;

(* Add sleeve wave-crest turbulence penalty if slow shot velocity was excessive *)
IF rPlungerVel_Filtered > (rCritical_Wave_Velocity_ms * 1.10) AND (iFSM_State = 5) THEN
    rPorosity_GasEntrap_Factor := rPorosity_GasEntrap_Factor + 0.25;
END_IF;

IF rPorosity_GasEntrap_Factor > 1.0 THEN
    rPorosity_GasEntrap_Factor := 1.0;
END_IF;

(* Factor 2.2: Solidification Shrinkage Porosity Factor (Driven by Intensification Rise Time & Pressure) *)
IF rIntensification_RiseTime_Actual_ms <= 15.0 THEN
    rPorosity_Shrinkage_Factor := 0.05; (* Perfect < 15 ms rise time feeds dendrite mushy zone *)
ELSIF rIntensification_RiseTime_Actual_ms <= 22.0 THEN
    rPorosity_Shrinkage_Factor := 0.05 + ((rIntensification_RiseTime_Actual_ms - 15.0) / 7.0) * 0.40;
ELSE
    rPorosity_Shrinkage_Factor := 0.45 + ((rIntensification_RiseTime_Actual_ms - 22.0) / 15.0) * 0.55;
END_IF;

(* Intensification Pressure Magnitude Attenuation *)
IF rHeadPress_Voted < (rRecipe_Intensification_Press * 0.85) AND (iFSM_State = 8) THEN
    rPorosity_Shrinkage_Factor := rPorosity_Shrinkage_Factor + 0.30;
END_IF;

(* Biscuit Thickness Cushion Evaluation *)
IF (rBiscuitThickness_Actual_mm < 16.0) THEN
    (* Metal starvation: gate freezes prematurely, massive centerline shrinkage *)
    rPorosity_Shrinkage_Factor := rPorosity_Shrinkage_Factor + 0.40;
ELSIF (rBiscuitThickness_Actual_mm > 28.0) THEN
    (* Excessive biscuit: thermal mass delays freeze-off, porosity moves toward gate *)
    rPorosity_Shrinkage_Factor := rPorosity_Shrinkage_Factor + 0.15;
END_IF;

IF rPorosity_Shrinkage_Factor > 1.0 THEN
    rPorosity_Shrinkage_Factor := 1.0;
END_IF;

(* Factor 2.3: Thermal Gradient Porosity Factor (Niyama Solidification Criterion Proxy) *)
rNiyama_Thermal_Gradient := ABS(rFixedDie_Temp_Actual - rMovingDie_Temp_Actual);
IF rNiyama_Thermal_Gradient <= 12.0 THEN
    rPorosity_Thermal_Factor := 0.05;
ELSIF rNiyama_Thermal_Gradient <= 25.0 THEN
    rPorosity_Thermal_Factor := 0.05 + ((rNiyama_Thermal_Gradient - 12.0) / 13.0) * 0.35;
ELSE
    rPorosity_Thermal_Factor := 0.40 + ((rNiyama_Thermal_Gradient - 25.0) / 25.0) * 0.60;
END_IF;

IF rPorosity_Thermal_Factor > 1.0 THEN
    rPorosity_Thermal_Factor := 1.0;
END_IF;

(* Composite Porosity Risk Index: Weighted Sum of Gas, Shrinkage, and Thermal Factors *)
rPorosity_Risk_Index := (0.45 * rPorosity_GasEntrap_Factor) +
                        (0.40 * rPorosity_Shrinkage_Factor) +
                        (0.15 * rPorosity_Thermal_Factor);

IF rPorosity_Risk_Index < 0.0 THEN
    rPorosity_Risk_Index := 0.0;
ELSIF rPorosity_Risk_Index > 1.0 THEN
    rPorosity_Risk_Index := 1.0;
END_IF;

(* Semi-Empirical Weiler Porosity Index *)
rWeiler_Porosity_Index := rPorosity_Risk_Index * 100.0;

(* ---------------------------------------------------------------------------------------------------------------------
 * 3. METALLURGICAL QUALITY TIER CLASSIFICATION
 * Class 1 = Prime Structural Rear Underbody (100% X-Ray Certified, Porosity < 0.20)
 * Class 2 = Non-Structural Cosmetic Grade (Porosity < 0.45)
 * Class 3 = Defective Scrap / Remelt
 * --------------------------------------------------------------------------------------------------------------------- *)
IF (rPorosity_Risk_Index <= 0.20) AND
   (rBiscuitThickness_Actual_mm >= 17.0) AND (rBiscuitThickness_Actual_mm <= 26.0) AND
   (rIntensification_RiseTime_Actual_ms <= 16.0) AND
   (rPlatenTilt_Parallelism_um <= 90.0) AND
   (NOT bAlarm_FlashBlowout_Detected) THEN

    iCasting_Quality_Grade := 1; (* Class A Structural *)
ELSIF (rPorosity_Risk_Index <= 0.45) AND
      (rBiscuitThickness_Actual_mm >= 14.0) AND (rBiscuitThickness_Actual_mm <= 30.0) AND
      (NOT bAlarm_FlashBlowout_Detected) THEN

    iCasting_Quality_Grade := 2; (* Class B Commercial *)
ELSE
    iCasting_Quality_Grade := 3; (* Class C Defective Scrap *)
END_IF;
"""
