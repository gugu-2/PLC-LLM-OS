# section2_physics.py
# First-principles cyber-physical state-space observer & shot hydrodynamics

def get_section2():
    return """
(* ========================================================================================= *)
(* 2.0 FIRST-PRINCIPLES CYBER-PHYSICAL STATE-SPACE OBSERVER & PHYSICAL KINEMATICS            *)
(* ========================================================================================= *)
(* Executes full Luenberger / Kalman innovation updates for the 6-state dynamic model:       *)
(*   y_est[k]     = C * x_hat[k] + D * u[k]                                                  *)
(*   innov[k]     = y_meas[k] - y_est[k]                                                     *)
(*   x_hat[k+1]   = A * x_hat[k] + B * u[k] + L * innov[k]                                   *)

(* Assemble Raw Measurement Vector y_meas from 2oo3 Voted & Process Transducers *)
y_meas[1] := rPlungerVel_Voted_ms;
y_meas[2] := rShotPress_Voted_bar;
y_meas[3] := rCavityVac_Voted_mbar;
y_meas[4] := rClampForce_Voted_kN;
y_meas[5] := (rDieTemp_Cover_degC + rDieTemp_Ejector_degC + rDieTemp_CoreInsert_degC) / 3.0;
y_meas[6] := rSolidificationThickness_mm;

(* Compute Estimated Output: y_est = C * x_hat + D * u *)
FOR iIdx1 := 1 TO 6 DO
    rTempSum := 0.0;
    FOR iIdx2 := 1 TO 6 DO
        rTempSum := rTempSum + (C_mat[iIdx1, iIdx2] * x_hat[iIdx2]);
    END_FOR;
    FOR iIdx2 := 1 TO 5 DO
        rTempSum := rTempSum + (D_mat[iIdx1, iIdx2] * u_mpc[iIdx2]);
    END_FOR;
    y_est[iIdx1] := rTempSum;
    innov[iIdx1] := y_meas[iIdx1] - y_est[iIdx1];
END_FOR;

(* Innovation Gating & Plausibility Clamping *)
IF innov[1] > 2.50 THEN innov[1] := 2.50; END_IF;
IF innov[1] < -2.50 THEN innov[1] := -2.50; END_IF;
IF innov[2] > 120.0 THEN innov[2] := 120.0; END_IF;
IF innov[2] < -120.0 THEN innov[2] := -120.0; END_IF;
IF innov[3] > 85.0 THEN innov[3] := 85.0; END_IF;
IF innov[3] < -85.0 THEN innov[3] := -85.0; END_IF;

(* Compute One-Step-Ahead State Observer: x_hat_next = A * x_hat + B * u + L * innov *)
FOR iIdx1 := 1 TO 6 DO
    rTempSum := 0.0;
    (* State transition contribution *)
    FOR iIdx2 := 1 TO 6 DO
        rTempSum := rTempSum + (A_mat[iIdx1, iIdx2] * x_hat[iIdx2]);
    END_FOR;
    (* Control actuation contribution *)
    FOR iIdx2 := 1 TO 5 DO
        rTempSum := rTempSum + (B_mat[iIdx1, iIdx2] * u_mpc[iIdx2]);
    END_FOR;
    (* Observer Kalman innovation correction *)
    FOR iIdx2 := 1 TO 6 DO
        rTempSum := rTempSum + (L_obs[iIdx1, iIdx2] * innov[iIdx2]);
    END_FOR;
    x_hat_next[iIdx1] := rTempSum;
END_FOR;

(* State Physical Boundary Projection Clamping *)
IF x_hat_next[1] < 0.0 THEN x_hat_next[1] := 0.0; END_IF;       (* Velocity cannot be negative in forward shot *)
IF x_hat_next[1] > 12.0 THEN x_hat_next[1] := 12.0; END_IF;
IF x_hat_next[2] < 0.0 THEN x_hat_next[2] := 0.0; END_IF;       (* Pressure non-negative *)
IF x_hat_next[2] > 1600.0 THEN x_hat_next[2] := 1600.0; END_IF;
IF x_hat_next[3] < 0.1 THEN x_hat_next[3] := 0.1; END_IF;       (* Minimum absolute vacuum *)
IF x_hat_next[3] > 1050.0 THEN x_hat_next[3] := 1050.0; END_IF;
IF x_hat_next[4] < 0.0 THEN x_hat_next[4] := 0.0; END_IF;
IF x_hat_next[4] > 110000.0 THEN x_hat_next[4] := 110000.0; END_IF;
IF x_hat_next[5] < 20.0 THEN x_hat_next[5] := 20.0; END_IF;
IF x_hat_next[5] > 400.0 THEN x_hat_next[5] := 400.0; END_IF;
IF x_hat_next[6] < 0.0 THEN x_hat_next[6] := 0.0; END_IF;
IF x_hat_next[6] > (c_PartMeanThickness_mm * 0.5) THEN 
    x_hat_next[6] := (c_PartMeanThickness_mm * 0.5); 
END_IF;

(* Commit Updated Estimated States *)
FOR iIdx1 := 1 TO 6 DO
    x_hat[iIdx1]   := x_hat_next[iIdx1];
    x_state[iIdx1] := x_hat[iIdx1];
END_FOR;

(* ----------------------------------------------------------------------------------------- *)
(* 2.1 First-Principles Horizontal Shot Sleeve Wave Hydrodynamics                            *)
(* ----------------------------------------------------------------------------------------- *)
(* In Phase 1 (Slow Shot), 110 kg of molten alloy fills a fraction of the horizontal sleeve. *)
(* Plunger motion excites surface gravity waves. If plunger speed exceeds wave propagation   *)
(* celerity (Fr >= 1.0), the wave breaks forward, curling over and trapping large pockets    *)
(* of air and oxide skins, destroying tensile elongation in the structural casting.           *)

rFillFractionInSleeve := c_TotalShotDoseVolume_m3 / (c_SleeveArea_m2 * c_SleeveLength_m);
IF rFillFractionInSleeve > 0.95 THEN rFillFractionInSleeve := 0.95; END_IF;
IF rFillFractionInSleeve < 0.15 THEN rFillFractionInSleeve := 0.15; END_IF;

(* Effective Liquid Height: geometric approximation for circular sleeve cross-section *)
rLiquidMetalHeight_m := c_SleeveDiameter_m * (0.15 + (0.70 * rFillFractionInSleeve));

(* Gravity Wave Celerity: c_wave = sqrt(g * h_eff) [m/s] *)
rCriticalWaveVelocity_ms := SQRT(9.80665 * rLiquidMetalHeight_m);
IF rCriticalWaveVelocity_ms < 0.35 THEN rCriticalWaveVelocity_ms := 0.35; END_IF;

(* Dynamic Froude Number: Fr = v_plunger / c_wave *)
rFroudeNumber := x_state[1] / rCriticalWaveVelocity_ms;

(* Wave Surge Suppression Anti-Slosh Profile:                                               *)
(* Modulates plunger acceleration to maintain Froude number strictly <= 0.88 during Phase 1 *)
IF (rPlungerPos_mm >= c_Pos_PourHoleCovered_mm) AND (rPlungerPos_mm < c_Pos_SleeveCompaction_mm) THEN
    IF rFroudeNumber > 0.88 THEN
        rWaveProfileDampingGain := 0.88 / rFroudeNumber;
    ELSE
        rWaveProfileDampingGain := 1.0;
    END_IF;
ELSE
    rWaveProfileDampingGain := 1.0;
END_IF;

(* ----------------------------------------------------------------------------------------- *)
(* 2.2 Mold Cavity High-Vacuum Decompression Dynamics                                        *)
(* ----------------------------------------------------------------------------------------- *)
(* Decompression mass balance: dp/dt = - (S_roots / V_cavity) * p + Q_leak                   *)
IF (iState = c_STATE_MOLD_CAVITY_HIGH_VACUUM_EVACUATION_BELOW_25MBAR) OR
   (iState = c_STATE_PHASE1_SLOW_SHOT_WAVE_SURGE_SUPPRESSION) THEN
    (* Vacuum extraction active *)
    rDynamicVacuumEvacRate_mb_s := ((c_VacuumRootsSpeed_m3_s / c_TotalVacuumVolume_m3) * x_state[3] * (u_mpc[4] * 0.01)) - 4.50;
    IF rDynamicVacuumEvacRate_mb_s < 0.0 THEN rDynamicVacuumEvacRate_mb_s := 0.0; END_IF;
ELSE
    rDynamicVacuumEvacRate_mb_s := 0.0;
END_IF;

(* ----------------------------------------------------------------------------------------- *)
(* 2.3 Acoustic Chill-Block Fast Shutoff Valve Dynamic Response Latency                      *)
(* ----------------------------------------------------------------------------------------- *)
(* Fast shutoff valve must seat in < 8.0 ms upon molten metal arrival detection at vent      *)
IF bFastShutoffChillValve_CMD AND NOT bChillBlockValveClosed_LS THEN
    IF NOT bChillBlockTimerActive THEN
        bChillBlockTimerActive := TRUE;
        rChillBlockTimer_ms    := 0.0;
    ELSE
        rChillBlockTimer_ms := rChillBlockTimer_ms + (rCycleTime_sec * 1000.0);
    END_IF;
ELSIF bChillBlockValveClosed_LS AND bChillBlockTimerActive THEN
    (* Valve closure completed: record closure latency *)
    rChillValveCloseTime_ms := rChillBlockTimer_ms;
    bChillBlockTimerActive  := FALSE;
ELSE
    bChillBlockTimerActive := FALSE;
END_IF;

(* ----------------------------------------------------------------------------------------- *)
(* 2.4 Solidification Kinetics (Stefan-Chvorinov In-Die Freezing Model)                      *)
(* ----------------------------------------------------------------------------------------- *)
(* Heat conduction through solidified shell into die steel face:                             *)
(*   q_flux = k_alloy * (T_melt - T_die) / delta_x                                          *)
(*   ds/dt  = q_flux / (rho_alloy * LatentHeat_fusion)                                      *)
IF (iState >= c_STATE_PHASE3_INTENSIFICATION_PRESSURE_SQUEEZE_1400BAR) AND
   (iState <= c_STATE_IN_DIE_SOLIDIFICATION_COOLING_HOLD) THEN

    IF x_state[6] > 0.05 THEN
        rHeatFluxToDie_W_m2 := c_AlloyThermalConduct_W_mK * (c_LiquidusTemp_degC - x_state[5]) / (x_state[6] * 0.001);
    ELSE
        rHeatFluxToDie_W_m2 := c_AlloyThermalConduct_W_mK * (c_LiquidusTemp_degC - x_state[5]) / 0.00005;
    END_IF;

    IF rHeatFluxToDie_W_m2 > 1.8E6 THEN rHeatFluxToDie_W_m2 := 1.8E6; END_IF;
    IF rHeatFluxToDie_W_m2 < 0.0 THEN rHeatFluxToDie_W_m2 := 0.0; END_IF;

    rSolidificationRate_mm_s := (rHeatFluxToDie_W_m2 / (c_AlloySolidDensity_kg_m3 * c_AlloyLatentHeatFusion_J_kg)) * 1000.0;
    IF rSolidificationRate_mm_s > 45.0 THEN rSolidificationRate_mm_s := 45.0; END_IF;

    (* Integrate Solidification Skin Growth *)
    rSolidificationThickness_mm := rSolidificationThickness_mm + (rSolidificationRate_mm_s * rCycleTime_sec);
    IF rSolidificationThickness_mm > (c_PartMeanThickness_mm * 0.5) THEN
        rSolidificationThickness_mm := (c_PartMeanThickness_mm * 0.5); (* Solidification through center line *)
    END_IF;
ELSE
    rSolidificationRate_mm_s := 0.0;
    rHeatFluxToDie_W_m2      := 0.0;
    IF iState = c_STATE_IDLE THEN
        rSolidificationThickness_mm := 0.0;
    END_IF;
END_IF;

(* ----------------------------------------------------------------------------------------- *)
(* 2.5 Die Flash Blowout Protection & Dynamic Parting Line Separation Force                  *)
(* ----------------------------------------------------------------------------------------- *)
(* Liquid metal under 1,400 bar intensification generates colossal separating forces across  *)
(* the 1.85 m^2 projected area of the rear underbody die cavity.                             *)
(* If F_sep exceeds F_clamp_voted, the die parting line opens (flash blowout), creating      *)
(* an catastrophic foundry blast and spraying molten aluminum into the cell.                 *)

(* Effective hydrostatic cavity pressure derived from plunger head pressure *)
rCavityDynamicPressure_bar := x_state[2] * 0.82; (* 82% effective pressure transmission efficiency *)

(* Die Parting Separation Force [kN]: F_sep = P_cav [bar] * 100 [kPa/bar] * Area [m^2] *)
rDieSeparationForce_kN := (rCavityDynamicPressure_bar * 100.0) * c_PartingProjectedArea_m2;

(* Flash Blowout Reserve Safety Margin [kN] *)
rFlashBlowoutSafetyMargin_kN := rClampForce_Voted_kN - rDieSeparationForce_kN;

(* Flash Risk Alarm Evaluation *)
IF (rFlashBlowoutSafetyMargin_kN < 6000.0) AND (iState >= c_STATE_PHASE2_FAST_SHOT_HIGH_ACCELERATION_CAVITY_FILL) THEN
    bAlm_FlashBlowoutRisk_HH := TRUE;
ELSE
    bAlm_FlashBlowoutRisk_HH := FALSE;
END_IF;
"""

if __name__ == "__main__":
    print("Section 2 len:", len(get_section2()))
