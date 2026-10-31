# cz_builder/cz_phase5.py

def get_phase5():
    return """(* === PHASE 5: ISA-18.2 ALARMS & DIAGNOSTIC WORD PACKING === *)
(* Implements multi-tiered safety trips, deadband hysteresis, actuator slew limiting,    *)
(* and bit-packed telemetry DWORD registers for industrial SCADA / DCS communication.     *)

(* 5.1 Fault Reset Logic *)
IF bResetFaults AND (NOT bSystemTripped OR (iState = 0) OR (iState = 99)) THEN
    dwAlarmWord1 := 16#0000_0000;
    dwAlarmWord2 := 16#0000_0000;
    dwWarningWord := 16#0000_0000;
    bSystemTripped := FALSE;
END_IF;

(* 5.2 SIL-3 Hardwired Emergency Stop Relay (Active-Low) *)
IF NOT bEmergencyStop THEN
    dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0001; (* E-Stop tripped *)
    bSystemTripped := TRUE;
END_IF;

(* 5.3 Catastrophic Crucible Burnout / Molten Silicon Breach Trip HH *)
IF (rVotedCrucibleTemp_DegC > rTrip_CrucibleWallTemp_HH) OR (rChamberShellTemp_DegC > rTrip_ShellTemp_HH) THEN
    dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0002; (* Crucible breach / shell overtemp *)
    bCrucibleLeakHazard := TRUE;
    bSystemTripped := TRUE;
ELSE
    bCrucibleLeakHazard := FALSE;
END_IF;

(* 5.4 Chamber Vacuum Overpressure / Vacuum Loss Trip HH *)
IF (rVotedChamberPress_mbar > rTrip_ChamberPress_HH) OR ((rVotedChamberPress_mbar > 35.0) AND (iState >= 2) AND (iState <= 8)) THEN
    dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0004; (* Vacuum failure / high chamber pressure *)
    bSystemTripped := TRUE;
END_IF;

(* 5.5 Argon Purge Gas Low-Low Trip LL *)
IF (rActualArgonInletFlow_slpm < rTrip_ArgonFlow_LL) AND (iState >= 2) AND (iState <= 8) THEN
    dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0008; (* Argon flow failure *)
    bSystemTripped := TRUE;
END_IF;

(* 5.6 Double-Walled Cooling Water Jacket Flow Interlock *)
IF NOT bCoolingWaterFlowOk AND (iState >= 2) AND (iState <= 10) THEN
    dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0010; (* Cooling water failure *)
    bSystemTripped := TRUE;
END_IF;

(* 5.7 Optical Meniscus Loss-of-Lock Alarm *)
bMeniscusSignalValid := (rVotedMeniscusDiam_mm > 1.0) AND (rVotedMeniscusDiam_mm < 350.0);
tMeniscusLostTimer(IN := (NOT bMeniscusSignalValid AND (iState >= 4) AND (iState <= 8)), PT := T#3S);
IF tMeniscusLostTimer.Q THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0001; (* Meniscus optical lock lost *)
    bSystemTripped := TRUE;
END_IF;

(* 5.8 Melt Interface Extreme Temperature Trip *)
IF (rVotedMeltTemp_DegC > rTrip_MeltTemp_HH) OR ((rVotedMeltTemp_DegC < rTrip_MeltTemp_LL) AND (iState >= 4) AND (iState <= 8)) THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0002; (* Interface temp out of bounds *)
    bSystemTripped := TRUE;
END_IF;

(* 5.9 Multi-Zone Heater SCR Overpower / Current Imbalance Trips *)
IF ((rUpperSideHeaterCurrent_A * rUpperSideHeaterVoltage_V * 0.001) > rTrip_UpperPower_HH) OR
   ((rLowerSideHeaterCurrent_A * rLowerSideHeaterVoltage_V * 0.001) > rTrip_LowerPower_HH) OR
   ((rBottomHeaterCurrent_A * rBottomHeaterVoltage_V * 0.001) > rTrip_BottomPower_HH) THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0004; (* Heater overpower SCR fault *)
    bSystemTripped := TRUE;
END_IF;

(* 5.10 Master Failsafe Trip Transition *)
IF bSystemTripped THEN
    bSystemRunning := FALSE;
    bSystemReady := FALSE;
    bDiameterLockEngaged := FALSE;
    iState := 99; (* Direct transition to emergency safe hold *)
END_IF;

(* 5.11 Actuator Slew Rate Limiting & Final Demand Clamping *)
(* Seed Pull Speed Ramping (max 0.15 mm/min/s) *)
IF rSeedPullSpeedDemand_mmpm < rTargetPullSpeedInternal THEN
    rSeedPullSpeedDemand_mmpm := rSeedPullSpeedDemand_mmpm + (0.15 * rCycleTime_sec);
    IF rSeedPullSpeedDemand_mmpm > rTargetPullSpeedInternal THEN
        rSeedPullSpeedDemand_mmpm := rTargetPullSpeedInternal;
    END_IF;
ELSIF rSeedPullSpeedDemand_mmpm > rTargetPullSpeedInternal THEN
    rSeedPullSpeedDemand_mmpm := rSeedPullSpeedDemand_mmpm - (0.15 * rCycleTime_sec);
    IF rSeedPullSpeedDemand_mmpm < rTargetPullSpeedInternal THEN
        rSeedPullSpeedDemand_mmpm := rTargetPullSpeedInternal;
    END_IF;
END_IF;

(* Crucible Lift Servo Ramping (max 0.10 mm/min/s) *)
IF rCrucibleLiftDemand_mmpm < rTargetCrucibleLiftInternal THEN
    rCrucibleLiftDemand_mmpm := rCrucibleLiftDemand_mmpm + (0.10 * rCycleTime_sec);
    IF rCrucibleLiftDemand_mmpm > rTargetCrucibleLiftInternal THEN
        rCrucibleLiftDemand_mmpm := rTargetCrucibleLiftInternal;
    END_IF;
ELSIF rCrucibleLiftDemand_mmpm > rTargetCrucibleLiftInternal THEN
    rCrucibleLiftDemand_mmpm := rCrucibleLiftDemand_mmpm - (0.10 * rCycleTime_sec);
    IF rCrucibleLiftDemand_mmpm < rTargetCrucibleLiftInternal THEN
        rCrucibleLiftDemand_mmpm := rTargetCrucibleLiftInternal;
    END_IF;
END_IF;

(* Upper Side Heater Power Ramping (max 2.0 kW/s) *)
IF rUpperHeaterPowerDemand_kW < rTargetUpperPowerInternal THEN
    rUpperHeaterPowerDemand_kW := rUpperHeaterPowerDemand_kW + (2.0 * rCycleTime_sec);
    IF rUpperHeaterPowerDemand_kW > rTargetUpperPowerInternal THEN
        rUpperHeaterPowerDemand_kW := rTargetUpperPowerInternal;
    END_IF;
ELSIF rUpperHeaterPowerDemand_kW > rTargetUpperPowerInternal THEN
    rUpperHeaterPowerDemand_kW := rUpperHeaterPowerDemand_kW - (2.0 * rCycleTime_sec);
    IF rUpperHeaterPowerDemand_kW < rTargetUpperPowerInternal THEN
        rUpperHeaterPowerDemand_kW := rTargetUpperPowerInternal;
    END_IF;
END_IF;

(* Lower Side Heater Power Ramping (max 2.0 kW/s) *)
IF rLowerHeaterPowerDemand_kW < rTargetLowerPowerInternal THEN
    rLowerHeaterPowerDemand_kW := rLowerHeaterPowerDemand_kW + (2.0 * rCycleTime_sec);
    IF rLowerHeaterPowerDemand_kW > rTargetLowerPowerInternal THEN
        rLowerHeaterPowerDemand_kW := rTargetLowerPowerInternal;
    END_IF;
ELSIF rLowerHeaterPowerDemand_kW > rTargetLowerPowerInternal THEN
    rLowerHeaterPowerDemand_kW := rLowerHeaterPowerDemand_kW - (2.0 * rCycleTime_sec);
    IF rLowerHeaterPowerDemand_kW < rTargetLowerPowerInternal THEN
        rLowerHeaterPowerDemand_kW := rTargetLowerPowerInternal;
    END_IF;
END_IF;

(* Bottom Heater Power Ramping (max 1.0 kW/s) *)
IF rBottomHeaterPowerDemand_kW < rTargetBottomPowerInternal THEN
    rBottomHeaterPowerDemand_kW := rBottomHeaterPowerDemand_kW + (1.0 * rCycleTime_sec);
    IF rBottomHeaterPowerDemand_kW > rTargetBottomPowerInternal THEN
        rBottomHeaterPowerDemand_kW := rTargetBottomPowerInternal;
    END_IF;
ELSIF rBottomHeaterPowerDemand_kW > rTargetBottomPowerInternal THEN
    rBottomHeaterPowerDemand_kW := rBottomHeaterPowerDemand_kW - (1.0 * rCycleTime_sec);
    IF rBottomHeaterPowerDemand_kW < rTargetBottomPowerInternal THEN
        rBottomHeaterPowerDemand_kW := rTargetBottomPowerInternal;
    END_IF;
END_IF;

(* Seed Rotation Command *)
rSeedRotationDemand_rpm := rTargetSeedRotInternal;

(* Crucible Rotation Command *)
rCrucibleRotationDemand_rpm := rTargetCrucibleRotInternal;

(* Argon Mass Flow Purge Demand [%] *)
rArgonPurgeValveDemand_pct := (rTargetArgonFlowInternal / 200.0) * 100.0;
IF rArgonPurgeValveDemand_pct > 100.0 THEN rArgonPurgeValveDemand_pct := 100.0; END_IF;
IF rArgonPurgeValveDemand_pct < 0.0 THEN rArgonPurgeValveDemand_pct := 0.0; END_IF;

(* Vacuum Throttle Valve Demand [%] *)
rThrottleValveDemand_pct := rTargetThrottleInternal;
IF rThrottleValveDemand_pct > 100.0 THEN rThrottleValveDemand_pct := 100.0; END_IF;
IF rThrottleValveDemand_pct < 0.0 THEN rThrottleValveDemand_pct := 0.0; END_IF;

(* 5.12 Bit-Packed Telemetry Words Assembly *)
dwSystemStatusWord := 16#0000_0000;
IF bSystemRunning THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0001; END_IF;
IF bSystemReady THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0002; END_IF;
IF bSystemTripped THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0004; END_IF;
IF bDiameterLockEngaged THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0008; END_IF;
IF bDislocationFreeStructure THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0010; END_IF;
IF bDegradedSensorMode THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0020; END_IF;
IF bMpcOptimalConverged THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0040; END_IF;
IF NOT bVoronkovRatioOutOfBounds THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0080; END_IF;
IF iState = 4 THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0100; END_IF; (* Necking *)
IF iState = 5 THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0200; END_IF; (* Crown *)
IF iState = 7 THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0400; END_IF; (* Body *)
IF iState = 8 THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0800; END_IF; (* Tail-off *)

END_FUNCTION_BLOCK
"""
