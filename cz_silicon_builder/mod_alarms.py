# cz_silicon_builder/mod_alarms.py
# -*- coding: utf-8 -*-

def generate_alarms():
    return """(* ==========================================================================================
   PHASE 5: ISA-18.2 MULTI-TIER ALARMS & 32-BIT BIT-PACKED STATUS WORDS
   ==========================================================================================
   Implements multi-tiered alarm lifecycle:
     - High-High (HH) and Low-Low (LL): Critical safety trips requiring trip state transition
     - High (H) and Low (L): Supervisory process alarms with deadband hysteresis
     - Bit-packed 32-bit DWORDs for SCADA, DCS, and SEMI E30 (GEM) host telemetry:
         dwStatusWord1: System operational status bits & active FSM state byte
         dwStatusWord2: Crystallographic & process flags (Voronkov, Habit lines, etc.)
         dwAlarmWord1:  Hard safety trips and equipment protection trips
         dwAlarmWord2:  Process deviation warnings and degradation alarms
         dwFirstOutWord: Root-cause first-out latching trip identifier
   ========================================================================================== *)

(* ------------------------------------------------------------------------------------------
   1. MENISCUS TEMPERATURE ALARMS (ISA-18.2 WITH DEADBAND HYSTERESIS)
   ------------------------------------------------------------------------------------------ *)
(* Meniscus High-High Alarm (1435.0 deg C) *)
IF rVotedMeniscusTemp >= rMeniscusTemp_HH_Limit THEN
    bAlm_Meniscus_HH := TRUE;
ELSIF rVotedMeniscusTemp < (rMeniscusTemp_HH_Limit - rMeniscusTemp_Deadband) THEN
    bAlm_Meniscus_HH := FALSE;
END_IF;

(* Meniscus High Alarm (1425.0 deg C) *)
IF rVotedMeniscusTemp >= rMeniscusTemp_H_Limit THEN
    bAlm_Meniscus_H := TRUE;
ELSIF rVotedMeniscusTemp < (rMeniscusTemp_H_Limit - rMeniscusTemp_Deadband) THEN
    bAlm_Meniscus_H := FALSE;
END_IF;

(* Meniscus Low Alarm (1411.0 deg C) *)
IF (rVotedMeniscusTemp <= rMeniscusTemp_L_Limit) AND (iCurrentFSMState >= STATE_MELT_EQUILIBRIUM_AND_CUSP_MAGNETIC_LOCK) THEN
    bAlm_Meniscus_L := TRUE;
ELSIF rVotedMeniscusTemp > (rMeniscusTemp_L_Limit + rMeniscusTemp_Deadband) THEN
    bAlm_Meniscus_L := FALSE;
END_IF;

(* Meniscus Low-Low Alarm (1406.0 deg C - Freezing risk on seed/melt) *)
IF (rVotedMeniscusTemp <= rMeniscusTemp_LL_Limit) AND (iCurrentFSMState >= STATE_MELT_EQUILIBRIUM_AND_CUSP_MAGNETIC_LOCK) THEN
    bAlm_Meniscus_LL := TRUE;
ELSIF rVotedMeniscusTemp > (rMeniscusTemp_LL_Limit + rMeniscusTemp_Deadband) THEN
    bAlm_Meniscus_LL := FALSE;
END_IF;


(* ------------------------------------------------------------------------------------------
   2. INGOT DIAMETER TRACKING ALARMS (ACTIVE DURING BODY GROWTH)
   ------------------------------------------------------------------------------------------ *)
IF iCurrentFSMState = STATE_BODY_EQUAL_DIAMETER_GROWTH_MPC_ACTIVE THEN
    (* Diameter High-High Alarm (304.0 mm) *)
    IF rVotedIngotDiameter >= rDiameter_HH_Limit THEN
        bAlm_Diameter_HH := TRUE;
    ELSIF rVotedIngotDiameter < (rDiameter_HH_Limit - rDiameter_Deadband) THEN
        bAlm_Diameter_HH := FALSE;
    END_IF;

    (* Diameter High Alarm (301.2 mm) *)
    IF rVotedIngotDiameter >= rDiameter_H_Limit THEN
        bAlm_Diameter_H := TRUE;
    ELSIF rVotedIngotDiameter < (rDiameter_H_Limit - rDiameter_Deadband) THEN
        bAlm_Diameter_H := FALSE;
    END_IF;

    (* Diameter Low Alarm (298.8 mm) *)
    IF rVotedIngotDiameter <= rDiameter_L_Limit THEN
        bAlm_Diameter_L := TRUE;
    ELSIF rVotedIngotDiameter > (rDiameter_L_Limit + rDiameter_Deadband) THEN
        bAlm_Diameter_L := FALSE;
    END_IF;

    (* Diameter Low-Low Alarm (296.0 mm) *)
    IF rVotedIngotDiameter <= rDiameter_LL_Limit THEN
        bAlm_Diameter_LL := TRUE;
    ELSIF rVotedIngotDiameter > (rDiameter_LL_Limit + rDiameter_Deadband) THEN
        bAlm_Diameter_LL := FALSE;
    END_IF;
ELSE
    bAlm_Diameter_HH := FALSE;
    bAlm_Diameter_H := FALSE;
    bAlm_Diameter_L := FALSE;
    bAlm_Diameter_LL := FALSE;
END_IF;


(* ------------------------------------------------------------------------------------------
   3. CHAMBER VACUUM PRESSURE ALARMS [mbar]
   ------------------------------------------------------------------------------------------ *)
IF rChamberVacuumPressure >= rVacuum_HH_Limit THEN
    bAlm_Vacuum_HH := TRUE;
ELSIF rChamberVacuumPressure < (rVacuum_HH_Limit - rVacuum_Deadband) THEN
    bAlm_Vacuum_HH := FALSE;
END_IF;

IF rChamberVacuumPressure >= rVacuum_H_Limit THEN
    bAlm_Vacuum_H := TRUE;
ELSIF rChamberVacuumPressure < (rVacuum_H_Limit - rVacuum_Deadband) THEN
    bAlm_Vacuum_H := FALSE;
END_IF;

IF (rChamberVacuumPressure <= rVacuum_L_Limit) AND (iCurrentFSMState >= STATE_ARGON_MELT_PURGE_AND_PRESSURE_STABILIZE) THEN
    bAlm_Vacuum_L := TRUE;
ELSIF rChamberVacuumPressure > (rVacuum_L_Limit + rVacuum_Deadband) THEN
    bAlm_Vacuum_L := FALSE;
END_IF;

IF (rChamberVacuumPressure <= rVacuum_LL_Limit) AND (iCurrentFSMState >= STATE_ARGON_MELT_PURGE_AND_PRESSURE_STABILIZE) THEN
    bAlm_Vacuum_LL := TRUE;
ELSIF rChamberVacuumPressure > (rVacuum_LL_Limit + rVacuum_Deadband) THEN
    bAlm_Vacuum_LL := FALSE;
END_IF;


(* ------------------------------------------------------------------------------------------
   4. MAIN GRAPHITE HEATER TEMPERATURE ALARMS [deg C]
   ------------------------------------------------------------------------------------------ *)
IF rVotedHeaterTemp >= rHeater_HH_Limit THEN
    bAlm_Heater_HH := TRUE;
ELSIF rVotedHeaterTemp < (rHeater_HH_Limit - rHeater_Deadband) THEN
    bAlm_Heater_HH := FALSE;
END_IF;

IF rVotedHeaterTemp >= rHeater_H_Limit THEN
    bAlm_Heater_H := TRUE;
ELSIF rVotedHeaterTemp < (rHeater_H_Limit - rHeater_Deadband) THEN
    bAlm_Heater_H := FALSE;
END_IF;

IF (rVotedHeaterTemp <= rHeater_L_Limit) AND (iCurrentFSMState >= STATE_POLYSILICON_CHARGE_MELTDOWN_FULL_POWER)
   AND (iCurrentFSMState <= STATE_TAILOUT_END_CONE_THERMAL_SHOCK_TAPERING) THEN
    bAlm_Heater_L := TRUE;
ELSIF rVotedHeaterTemp > (rHeater_L_Limit + rHeater_Deadband) THEN
    bAlm_Heater_L := FALSE;
END_IF;

IF (rVotedHeaterTemp <= rHeater_LL_Limit) AND (iCurrentFSMState >= STATE_POLYSILICON_CHARGE_MELTDOWN_FULL_POWER)
   AND (iCurrentFSMState <= STATE_TAILOUT_END_CONE_THERMAL_SHOCK_TAPERING) THEN
    bAlm_Heater_LL := TRUE;
ELSIF rVotedHeaterTemp > (rHeater_LL_Limit + rHeater_Deadband) THEN
    bAlm_Heater_LL := FALSE;
END_IF;


(* ------------------------------------------------------------------------------------------
   5. CHAMBER COOLING WATER UTILITY ALARMS
   ------------------------------------------------------------------------------------------ *)
IF rCoolingWaterFlowPrimary <= rCoolingFlow_LL_Limit THEN
    bAlm_CoolingWater_FlowTrip := TRUE;
ELSIF rCoolingWaterFlowPrimary > (rCoolingFlow_LL_Limit + rCoolingFlow_Deadband) THEN
    bAlm_CoolingWater_FlowTrip := FALSE;
END_IF;

IF rCoolingWaterFlowPrimary <= rCoolingFlow_L_Limit THEN
    bAlm_CoolingWater_FlowLow := TRUE;
ELSIF rCoolingWaterFlowPrimary > (rCoolingFlow_L_Limit + rCoolingFlow_Deadband) THEN
    bAlm_CoolingWater_FlowLow := FALSE;
END_IF;

IF rCoolingWaterTempPrimary >= rCoolingTemp_HH_Limit THEN
    bAlm_CoolingWater_TempTrip := TRUE;
ELSIF rCoolingWaterTempPrimary < (rCoolingTemp_HH_Limit - rCoolingTemp_Deadband) THEN
    bAlm_CoolingWater_TempTrip := FALSE;
END_IF;

IF rCoolingWaterTempPrimary >= rCoolingTemp_H_Limit THEN
    bAlm_CoolingWater_TempHigh := TRUE;
ELSIF rCoolingWaterTempPrimary < (rCoolingTemp_H_Limit - rCoolingTemp_Deadband) THEN
    bAlm_CoolingWater_TempHigh := FALSE;
END_IF;


(* ------------------------------------------------------------------------------------------
   6. VORONKOV DEFECT RATIO & CRUCIBLE MELT LEAK DETECTION
   ------------------------------------------------------------------------------------------ *)
IF (iCurrentFSMState = STATE_BODY_EQUAL_DIAMETER_GROWTH_MPC_ACTIVE)
   AND ((rCurrentVoronkovRatio < 0.185) OR (rCurrentVoronkovRatio > 0.255)) THEN
    bAlm_VoronkovRatioTrip := TRUE;
ELSE
    bAlm_VoronkovRatioTrip := FALSE;
END_IF;

(* Melt leak detection: Abnormal bottom susceptor thermocouple spike or rapid weight loss *)
IF (rBottomCrucibleTC > 1465.0) AND (iCurrentFSMState >= STATE_MELT_EQUILIBRIUM_AND_CUSP_MAGNETIC_LOCK) THEN
    bAlm_CrucibleMeltLeakDetected := TRUE;
END_IF;

bAlm_EStopActive := bEmergencyStop;


(* ------------------------------------------------------------------------------------------
   7. 32-BIT BIT-PACKED TELEMETRY DWORDS
   ------------------------------------------------------------------------------------------ *)
(* dwStatusWord1: System Operational & Subsystem States *)
dwStatusWord1 := 16#00000000;
IF bSystemReady THEN dwStatusWord1 := dwStatusWord1 OR 16#00000001; END_IF;
IF bSequenceActive THEN dwStatusWord1 := dwStatusWord1 OR 16#00000002; END_IF;
IF bAutoMode THEN dwStatusWord1 := dwStatusWord1 OR 16#00000004; END_IF;
IF bEnable THEN dwStatusWord1 := dwStatusWord1 OR 16#00000008; END_IF;
IF bPyro_DegradedMode THEN dwStatusWord1 := dwStatusWord1 OR 16#00000010; END_IF;
IF bCCD_DegradedMode THEN dwStatusWord1 := dwStatusWord1 OR 16#00000020; END_IF;
IF bLoadCell_DegradedMode THEN dwStatusWord1 := dwStatusWord1 OR 16#00000040; END_IF;
IF bHeater_DegradedMode THEN dwStatusWord1 := dwStatusWord1 OR 16#00000080; END_IF;
IF rArgonMFCFlowCmd > 5.0 THEN dwStatusWord1 := dwStatusWord1 OR 16#00000100; END_IF;
IF rVacuumThrottleValveCmd > 5.0 THEN dwStatusWord1 := dwStatusWord1 OR 16#00000200; END_IF;
IF u_cmd[1] > 0.05 THEN dwStatusWord1 := dwStatusWord1 OR 16#00000400; END_IF;
IF u_cmd[2] > 5.0 THEN dwStatusWord1 := dwStatusWord1 OR 16#00000800; END_IF;
IF u_cmd[3] > 0.02 THEN dwStatusWord1 := dwStatusWord1 OR 16#00001000; END_IF;
IF u_cmd[4] > 10.0 THEN dwStatusWord1 := dwStatusWord1 OR 16#00002000; END_IF;
IF u_cmd[5] > 0.5 THEN dwStatusWord1 := dwStatusWord1 OR 16#00004000; END_IF;
IF rCrucibleRotationCmd <> 0.0 THEN dwStatusWord1 := dwStatusWord1 OR 16#00008000; END_IF;
(* Pack active FSM state index into Bits 16-23 *)
dwStatusWord1 := dwStatusWord1 OR SHL(INT_TO_DWORD(iCurrentFSMState), 16);

(* dwStatusWord2: Crystallographic & Process Flags *)
dwStatusWord2 := 16#00000000;
IF bDislocationFreeStructure THEN dwStatusWord2 := dwStatusWord2 OR 16#00000001; END_IF;
IF bHabitLinesDetected THEN dwStatusWord2 := dwStatusWord2 OR 16#00000002; END_IF;
IF bVoronkovCriterionSatisfied THEN dwStatusWord2 := dwStatusWord2 OR 16#00000004; END_IF;
IF rMeniscusHeight_calc > 3.0 THEN dwStatusWord2 := dwStatusWord2 OR 16#00000008; END_IF;
IF iCurrentFSMState = STATE_POLYSILICON_CHARGE_MELTDOWN_FULL_POWER THEN dwStatusWord2 := dwStatusWord2 OR 16#00000010; END_IF;
IF iCurrentFSMState = STATE_MELT_EQUILIBRIUM_AND_CUSP_MAGNETIC_LOCK THEN dwStatusWord2 := dwStatusWord2 OR 16#00000020; END_IF;
IF iCurrentFSMState = STATE_SEED_CRYSTAL_DIP_AND_MELT_WETTING THEN dwStatusWord2 := dwStatusWord2 OR 16#00000040; END_IF;
IF iCurrentFSMState = STATE_DASH_NECKING_DISLOCATION_ELIMINATION THEN dwStatusWord2 := dwStatusWord2 OR 16#00000080; END_IF;
IF iCurrentFSMState = STATE_CROWN_EXPANSION_CONE_ANGLE_RAMP THEN dwStatusWord2 := dwStatusWord2 OR 16#00000100; END_IF;
IF iCurrentFSMState = STATE_SHOULDER_RADIUS_ROLLOVER_TRANSITION THEN dwStatusWord2 := dwStatusWord2 OR 16#00000200; END_IF;
IF iCurrentFSMState = STATE_BODY_EQUAL_DIAMETER_GROWTH_MPC_ACTIVE THEN dwStatusWord2 := dwStatusWord2 OR 16#00000400; END_IF;
IF iCurrentFSMState = STATE_TAILOUT_END_CONE_THERMAL_SHOCK_TAPERING THEN dwStatusWord2 := dwStatusWord2 OR 16#00000800; END_IF;
IF iCurrentFSMState = STATE_CRYSTAL_SEPARATION_AND_LIFT_TO_COOL_CHAMBER THEN dwStatusWord2 := dwStatusWord2 OR 16#00001000; END_IF;
IF iCurrentFSMState = STATE_RESIDUAL_MELT_COOLDOWN_AND_CRUCIBLE_PURGE THEN dwStatusWord2 := dwStatusWord2 OR 16#00002000; END_IF;
IF iCurrentFSMState = STATE_EMERGENCY_MELT_LEAK_OR_VACUUM_COLLAPSE_TRIP THEN dwStatusWord2 := dwStatusWord2 OR 16#00004000; END_IF;

(* dwAlarmWord1: Hard Safety Trips & Equipment Interlocks *)
dwAlarmWord1 := 16#00000000;
IF bAlm_EStopActive THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000001; END_IF;
IF bAlm_CrucibleMeltLeakDetected THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000002; END_IF;
IF bAlm_QuartzCrucibleRupture THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000004; END_IF;
IF bAlm_CoolingWater_FlowTrip THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000008; END_IF;
IF bAlm_CoolingWater_TempTrip THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000010; END_IF;
IF bAlm_Vacuum_HH THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000020; END_IF;
IF bAlm_Heater_HH THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000040; END_IF;
IF bAlm_Meniscus_HH THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000080; END_IF;
IF bAlm_Meniscus_LL THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000100; END_IF;
IF bPyro_CriticalFailSafe THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000200; END_IF;
IF bCCD_CriticalFailSafe THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000400; END_IF;
IF bLoadCell_CriticalFailSafe THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000800; END_IF;
IF bHeater_CriticalFailSafe THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00001000; END_IF;

(* dwAlarmWord2: Process Deviation Warnings & Degradations *)
dwAlarmWord2 := 16#00000000;
IF bAlm_Meniscus_H THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000001; END_IF;
IF bAlm_Meniscus_L THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000002; END_IF;
IF bAlm_Diameter_H THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000004; END_IF;
IF bAlm_Diameter_L THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000008; END_IF;
IF bAlm_Diameter_HH THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000010; END_IF;
IF bAlm_Diameter_LL THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000020; END_IF;
IF bAlm_Vacuum_H THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000040; END_IF;
IF bAlm_Vacuum_L THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000080; END_IF;
IF bAlm_Vacuum_LL THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000100; END_IF;
IF bAlm_Heater_H THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000200; END_IF;
IF bAlm_Heater_L THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000400; END_IF;
IF bAlm_Heater_LL THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000800; END_IF;
IF bAlm_CoolingWater_FlowLow THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00001000; END_IF;
IF bAlm_CoolingWater_TempHigh THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00002000; END_IF;
IF bAlm_VoronkovRatioTrip THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00004000; END_IF;

(* dwFirstOutWord: Latching First-Out Register *)
dwFirstOutWord := INT_TO_DWORD(iFirstOutCode);


(* ------------------------------------------------------------------------------------------
   8. ACTUATOR OUTPUT MAPPING TO HARDWARE INTERFACES
   ------------------------------------------------------------------------------------------ *)
rCrystalPullSpeedCmd := u_cmd[1];
rMainHeaterPowerCmd := u_cmd[2];
rCrucibleLiftSpeedCmd := u_cmd[3];
rCuspCoilCurrentCmd := u_cmd[4];
rSeedRotationCmd := u_cmd[5];

END_FUNCTION_BLOCK"""
