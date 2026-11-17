# section5_6_7.py
# Section 5 (Thermal PID), Section 6 (ISA-18.2 Alarms & DWORD Packing), Section 7 (Actuator Output Assignment)

def get_section5_6_7():
    return """
(* ========================================================================================= *)
(* 5.0 MULTI-CHANNEL PRESSURIZED DIE THERMAL BALANCING PID CONTROLLERS                       *)
(* ========================================================================================= *)
(* Regulates die surface temperatures (220 °C to 280 °C) across Cover Die, Ejector Die,      *)
(* and critical structural Core Inserts via closed-loop PID thermal oil modulation.          *)

(* --- 5.1 Fixed Cover Platen Cavity Face PID Loop --- *)
rCoverDie_Error_degC := 250.0 - rDieTemp_Cover_degC;
rCoverDie_Integral   := rCoverDie_Integral + (rCoverDie_Error_degC * 0.015 * rCycleTime_sec);
IF rCoverDie_Integral > 25.0 THEN rCoverDie_Integral := 25.0; END_IF;
IF rCoverDie_Integral < -25.0 THEN rCoverDie_Integral := -25.0; END_IF;
rCoverDie_Derivative := (rDieTemp_Cover_degC - rCoverDie_PrevTemp_degC) / rCycleTime_sec;
rCoverDie_PrevTemp_degC := rDieTemp_Cover_degC;

(* --- 5.2 Moving Ejector Platen Cavity Face PID Loop --- *)
rEjectorDie_Error_degC := 245.0 - rDieTemp_Ejector_degC;
rEjectorDie_Integral   := rEjectorDie_Integral + (rEjectorDie_Error_degC * 0.015 * rCycleTime_sec);
IF rEjectorDie_Integral > 25.0 THEN rEjectorDie_Integral := 25.0; END_IF;
IF rEjectorDie_Integral < -25.0 THEN rEjectorDie_Integral := -25.0; END_IF;
rEjectorDie_Derivative := (rDieTemp_Ejector_degC - rEjectorDie_PrevTemp_degC) / rCycleTime_sec;
rEjectorDie_PrevTemp_degC := rDieTemp_Ejector_degC;

(* --- 5.3 Thin-Walled Structural Core Insert PID Loop --- *)
rCoreInsert_Error_degC := 265.0 - rDieTemp_CoreInsert_degC;
rCoreInsert_Integral   := rCoreInsert_Integral + (rCoreInsert_Error_degC * 0.020 * rCycleTime_sec);
IF rCoreInsert_Integral > 30.0 THEN rCoreInsert_Integral := 30.0; END_IF;
IF rCoreInsert_Integral < -30.0 THEN rCoreInsert_Integral := -30.0; END_IF;
rCoreInsert_Derivative := (rDieTemp_CoreInsert_degC - rCoreInsert_PrevTemp_degC) / rCycleTime_sec;
rCoreInsert_PrevTemp_degC := rDieTemp_CoreInsert_degC;

(* Modulate Tempering Oil Circulating Pump Speed (u5 Feedforward + Trim) *)
IF NOT bSystemTripped THEN
    u_mpc[5] := 50.0 - (0.35 * rCoverDie_Error_degC) - (0.35 * rEjectorDie_Error_degC) - (0.45 * rCoreInsert_Error_degC);
    IF u_mpc[5] < 15.0 THEN u_mpc[5] := 15.0; END_IF;
    IF u_mpc[5] > 100.0 THEN u_mpc[5] := 100.0; END_IF;
ELSE
    u_mpc[5] := 20.0; (* Minimum cooling circulation in trip standby *)
END_IF;


(* ========================================================================================= *)
(* 6.0 ISA-18.2 MULTI-TIER ALARMS, FIRST-OUT ROOT CAUSE CAPTURE & TELEMETRY PACKING          *)
(* ========================================================================================= *)
dwAlarmWord1 := 16#0000_0000;
dwAlarmWord2 := 16#0000_0000;

(* --- 6.1 Injection Velocity Multi-Tier Alarms with Hysteresis Deadbands --- *)
(* High-High Velocity Trip *)
IF rPlungerVel_Voted_ms >= c_ALM_Vel_HH_ms THEN
    bAlm_Vel_HH := TRUE;
ELSIF rPlungerVel_Voted_ms <= (c_ALM_Vel_HH_ms - c_DB_Vel_ms) THEN
    bAlm_Vel_HH := FALSE;
END_IF;

(* High Velocity Warning *)
IF rPlungerVel_Voted_ms >= c_ALM_Vel_H_ms THEN
    bAlm_Vel_H := TRUE;
ELSIF rPlungerVel_Voted_ms <= (c_ALM_Vel_H_ms - c_DB_Vel_ms) THEN
    bAlm_Vel_H := FALSE;
END_IF;

(* Low Velocity Warning during Phase 1 *)
IF (iState = c_STATE_PHASE1_SLOW_SHOT_WAVE_SURGE_SUPPRESSION) AND (rPlungerVel_Voted_ms <= c_ALM_Vel_L_ms) THEN
    bAlm_Vel_L := TRUE;
ELSIF rPlungerVel_Voted_ms >= (c_ALM_Vel_L_ms + c_DB_Vel_ms) THEN
    bAlm_Vel_L := FALSE;
END_IF;

(* Low-Low Velocity Stall Trip *)
IF (iState = c_STATE_PHASE2_FAST_SHOT_HIGH_ACCELERATION_CAVITY_FILL) AND 
   (rPlungerVel_Voted_ms <= c_ALM_Vel_LL_ms) AND (rStateTimer_sec >= 0.020) THEN
    bAlm_Vel_LL := TRUE;
ELSIF rPlungerVel_Voted_ms >= (c_ALM_Vel_LL_ms + c_DB_Vel_ms) THEN
    bAlm_Vel_LL := FALSE;
END_IF;

(* --- 6.2 Shot Cylinder Hydraulic Pressure Alarms --- *)
(* High-High Intensification Pressure Trip *)
IF rShotPress_Voted_bar >= c_ALM_ShotPress_HH_bar THEN
    bAlm_ShotPress_HH := TRUE;
ELSIF rShotPress_Voted_bar <= (c_ALM_ShotPress_HH_bar - c_DB_ShotPress_bar) THEN
    bAlm_ShotPress_HH := FALSE;
END_IF;

(* High Shot Pressure Warning *)
IF rShotPress_Voted_bar >= c_ALM_ShotPress_H_bar THEN
    bAlm_ShotPress_H := TRUE;
ELSIF rShotPress_Voted_bar <= (c_ALM_ShotPress_H_bar - c_DB_ShotPress_bar) THEN
    bAlm_ShotPress_H := FALSE;
END_IF;

(* Low-Low Pressure Stall Trip in Phase 3 *)
IF (iState = c_STATE_PHASE3_INTENSIFICATION_PRESSURE_SQUEEZE_1400BAR) AND 
   (rShotPress_Voted_bar <= c_ALM_ShotPress_LL_bar) AND (rStateTimer_sec >= 0.350) THEN
    bAlm_ShotPress_LL := TRUE;
ELSIF rShotPress_Voted_bar >= (c_ALM_ShotPress_LL_bar + c_DB_ShotPress_bar) THEN
    bAlm_ShotPress_LL := FALSE;
END_IF;

(* --- 6.3 Mold Cavity High-Vacuum Alarms --- *)
(* High-High Vacuum Failure Trip (Severe Gas Porosity Hazard) *)
IF (iState >= c_STATE_PHASE1_SLOW_SHOT_WAVE_SURGE_SUPPRESSION) AND 
   (iState <= c_STATE_PHASE2_FAST_SHOT_HIGH_ACCELERATION_CAVITY_FILL) AND 
   (rCavityVac_Voted_mbar >= c_ALM_Vac_HH_mbar) THEN
    bAlm_Vac_HH := TRUE;
ELSIF rCavityVac_Voted_mbar <= (c_ALM_Vac_HH_mbar - c_DB_Vac_mbar) THEN
    bAlm_Vac_HH := FALSE;
END_IF;

(* High Vacuum Level Warning *)
IF (rCavityVac_Voted_mbar >= c_ALM_Vac_H_mbar) AND (iState = c_STATE_MOLD_CAVITY_HIGH_VACUUM_EVACUATION_BELOW_25MBAR) THEN
    bAlm_Vac_H := TRUE;
ELSIF rCavityVac_Voted_mbar <= (c_ALM_Vac_H_mbar - c_DB_Vac_mbar) THEN
    bAlm_Vac_H := FALSE;
END_IF;

(* --- 6.4 4-Tie-Bar Clamping Force & Structural Safety Alarms --- *)
(* High-High Tie-Bar Yield Overstrain Trip *)
IF rClampForce_Voted_kN >= c_ALM_Clamp_HH_kN THEN
    bAlm_Clamp_HH := TRUE;
ELSIF rClampForce_Voted_kN <= (c_ALM_Clamp_HH_kN - c_DB_Clamp_kN) THEN
    bAlm_Clamp_HH := FALSE;
END_IF;

(* Low-Low Clamping Force Flash Blowout Trip *)
IF (iState >= c_STATE_PHASE1_SLOW_SHOT_WAVE_SURGE_SUPPRESSION) AND 
   (iState <= c_STATE_PHASE3_INTENSIFICATION_PRESSURE_SQUEEZE_1400BAR) AND 
   (rClampForce_Voted_kN <= c_ALM_Clamp_LL_kN) THEN
    bAlm_Clamp_LL := TRUE;
ELSIF rClampForce_Voted_kN >= (c_ALM_Clamp_LL_kN + c_DB_Clamp_kN) THEN
    bAlm_Clamp_LL := FALSE;
END_IF;

(* High-High Platen Eccentricity / Bending Overstrain Trip *)
IF rTieBarMaxEccentricity_kN >= c_ALM_Eccentricity_HH_kN THEN
    bAlm_Eccentricity_HH := TRUE;
ELSIF rTieBarMaxEccentricity_kN <= (c_ALM_Eccentricity_HH_kN - c_DB_Eccentricity_kN) THEN
    bAlm_Eccentricity_HH := FALSE;
END_IF;

(* High Platen Tilting Warning *)
IF rTieBarMaxEccentricity_kN >= c_ALM_Eccentricity_H_kN THEN
    bAlm_Eccentricity_H := TRUE;
ELSIF rTieBarMaxEccentricity_kN <= (c_ALM_Eccentricity_H_kN - c_DB_Eccentricity_kN) THEN
    bAlm_Eccentricity_H := FALSE;
END_IF;

(* --- 6.5 Acoustic Chill-Block Fast Shutoff Latency Alarm --- *)
IF (rChillValveCloseTime_ms >= c_ALM_ChillClose_HH_ms) THEN
    bAlm_ChillClose_HH := TRUE;
ELSE
    bAlm_ChillClose_HH := FALSE;
END_IF;

(* --- 6.6 Die Cavity Surface Temperature Alarms --- *)
IF (rDieTemp_Cover_degC >= c_ALM_DieTemp_HH_degC) OR 
   (rDieTemp_Ejector_degC >= c_ALM_DieTemp_HH_degC) OR 
   (rDieTemp_CoreInsert_degC >= c_ALM_DieTemp_HH_degC) THEN
    bAlm_DieTemp_HH := TRUE;
ELSE
    bAlm_DieTemp_HH := FALSE;
END_IF;

IF (rDieTemp_Cover_degC <= c_ALM_DieTemp_LL_degC) AND (iState >= c_STATE_PHASE1_SLOW_SHOT_WAVE_SURGE_SUPPRESSION) THEN
    bAlm_DieTemp_LL := TRUE;
ELSE
    bAlm_DieTemp_LL := FALSE;
END_IF;

(* ========================================================================================= *)
(* 6.7 ISA-18.2 TELEMETRY BIT-PACKING (ALARM & STATUS WORDS)                                 *)
(* ========================================================================================= *)
(* Pack Priority 1 & 2 Process Trip Alarms into dwAlarmWord1 *)
IF bAlm_Vel_HH              THEN dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0001; END_IF;
IF bAlm_Vel_LL              THEN dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0002; END_IF;
IF bAlm_ShotPress_HH        THEN dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0004; END_IF;
IF bAlm_ShotPress_LL        THEN dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0008; END_IF;
IF bAlm_Vac_HH              THEN dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0010; END_IF;
IF bAlm_Clamp_HH            THEN dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0020; END_IF;
IF bAlm_Clamp_LL            THEN dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0040; END_IF;
IF bAlm_Eccentricity_HH     THEN dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0080; END_IF;
IF bAlm_ChillClose_HH       THEN dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0100; END_IF;
IF bAlm_FlashBlowoutRisk_HH THEN dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0200; END_IF;
IF bAlm_DieTemp_HH          THEN dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0400; END_IF;
IF bAlm_DieTemp_LL          THEN dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0800; END_IF;
IF bVel_Failed_Trip         THEN dwAlarmWord1 := dwAlarmWord1 OR 16#0000_1000; END_IF;
IF bPress_Failed_Trip       THEN dwAlarmWord1 := dwAlarmWord1 OR 16#0000_2000; END_IF;
IF bVac_Failed_Trip         THEN dwAlarmWord1 := dwAlarmWord1 OR 16#0000_4000; END_IF;
IF bClamp_Failed_Trip       THEN dwAlarmWord1 := dwAlarmWord1 OR 16#0000_8000; END_IF;

(* Pack Priority 3 & 4 Advisory Warnings into dwAlarmWord2 *)
IF bAlm_Vel_H               THEN dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0001; END_IF;
IF bAlm_Vel_L               THEN dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0002; END_IF;
IF bAlm_ShotPress_H         THEN dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0004; END_IF;
IF bAlm_Vac_H               THEN dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0008; END_IF;
IF bAlm_Clamp_H             THEN dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0010; END_IF;
IF bAlm_Clamp_L             THEN dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0020; END_IF;
IF bAlm_Eccentricity_H      THEN dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0040; END_IF;
IF bAlm_DieTemp_H           THEN dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0080; END_IF;
IF bAlm_DieTemp_L           THEN dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0100; END_IF;
IF bVel_Degraded_1oo2       THEN dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0200; END_IF;
IF bPress_Degraded_1oo2     THEN dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0400; END_IF;
IF bVac_Degraded_1oo2       THEN dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0800; END_IF;
IF bClamp_Degraded_1oo2     THEN dwAlarmWord2 := dwAlarmWord2 OR 16#0000_1000; END_IF;

(* Automatic Latching Trip Command *)
IF (dwAlarmWord1 <> 16#0000_0000) THEN
    bSystemTripped := TRUE;
    IF dwFirstOutWord = 16#0000_0000 THEN
        dwFirstOutWord := dwAlarmWord1; (* Capture first-out root cause *)
    END_IF;
END_IF;

bWarningActive := (dwAlarmWord2 <> 16#0000_0000);

(* Pack Production Status Word 1 *)
dwStatusWord1 := 16#0000_0000;
dwStatusWord1 := dwStatusWord1 OR INT_TO_DWORD(iState);
IF bSystemRunning                 THEN dwStatusWord1 := dwStatusWord1 OR 16#0000_0020; END_IF;
IF bSystemReady                   THEN dwStatusWord1 := dwStatusWord1 OR 16#0000_0040; END_IF;
IF bSystemTripped                 THEN dwStatusWord1 := dwStatusWord1 OR 16#0000_0080; END_IF;
IF bWarningActive                 THEN dwStatusWord1 := dwStatusWord1 OR 16#0000_0100; END_IF;
IF bDieSafetyClampLock_CMD        THEN dwStatusWord1 := dwStatusWord1 OR 16#0000_0200; END_IF;
IF bFastShutoffChillValve_CMD     THEN dwStatusWord1 := dwStatusWord1 OR 16#0000_0400; END_IF;
IF bVacuumRootsIsolation_CMD      THEN dwStatusWord1 := dwStatusWord1 OR 16#0000_0800; END_IF;
IF bLadleRobotPermissive_CMD      THEN dwStatusWord1 := dwStatusWord1 OR 16#0000_1000; END_IF;
IF bSprayRobotInitiate_CMD        THEN dwStatusWord1 := dwStatusWord1 OR 16#0000_2000; END_IF;
IF bExtractorRobotInitiate_CMD    THEN dwStatusWord1 := dwStatusWord1 OR 16#0000_4000; END_IF;
IF bMpcInOptimization             THEN dwStatusWord1 := dwStatusWord1 OR 16#0000_8000; END_IF;


(* ========================================================================================= *)
(* 7.0 HARDWARE ACTUATOR COMMAND ASSIGNMENT & OUTPUT SATURATION CLAMPING                     *)
(* ========================================================================================= *)
IF NOT bSystemTripped THEN
    rPilotValve_Shot_pct   := u_mpc[1];
    rAccumulatorPoppet_pct := u_mpc[2];
    rIntensifierValve_pct  := u_mpc[3];
    rVacuumValve_pct       := u_mpc[4];
    rTemperingPump_pct     := u_mpc[5];
ELSE
    rPilotValve_Shot_pct   := 0.0;
    rAccumulatorPoppet_pct := 0.0;
    rIntensifierValve_pct  := 0.0;
    rVacuumValve_pct       := 0.0;
    rTemperingPump_pct     := 20.0;
    rTieBar1_HydNut_pct    := 0.0;
    rTieBar2_HydNut_pct    := 0.0;
    rTieBar3_HydNut_pct    := 0.0;
    rTieBar4_HydNut_pct    := 0.0;
END_IF;

(* Final Safety Hard Clamping on Actuator Outputs *)
IF rPilotValve_Shot_pct < 0.0 THEN rPilotValve_Shot_pct := 0.0; END_IF;
IF rPilotValve_Shot_pct > 100.0 THEN rPilotValve_Shot_pct := 100.0; END_IF;
IF rAccumulatorPoppet_pct < 0.0 THEN rAccumulatorPoppet_pct := 0.0; END_IF;
IF rAccumulatorPoppet_pct > 100.0 THEN rAccumulatorPoppet_pct := 100.0; END_IF;
IF rIntensifierValve_pct < 0.0 THEN rIntensifierValve_pct := 0.0; END_IF;
IF rIntensifierValve_pct > 100.0 THEN rIntensifierValve_pct := 100.0; END_IF;
IF rVacuumValve_pct < 0.0 THEN rVacuumValve_pct := 0.0; END_IF;
IF rVacuumValve_pct > 100.0 THEN rVacuumValve_pct := 100.0; END_IF;
IF rTemperingPump_pct < 0.0 THEN rTemperingPump_pct := 0.0; END_IF;
IF rTemperingPump_pct > 100.0 THEN rTemperingPump_pct := 100.0; END_IF;

(* Output Previous Commands Latch for Slew Damping *)
FOR iIdx1 := 1 TO 5 DO
    u_prev[iIdx1] := u_mpc[iIdx1];
END_FOR;

END_FUNCTION_BLOCK
"""

if __name__ == "__main__":
    print("Section 5_6_7 len:", len(get_section5_6_7()))
