# semiconductor_tcb_builder/build_st_phase6_alarms_diagnostics.py

def get_phase6_alarms_diagnostics():
    return """(*
====================================================================================================
PHASE 6: ISA-18.2 MULTI-TIERED ALARMS, STATISTICAL QUALITY CONTROL & BIT-PACKED TELEMETRY
Standardized Alarm Annunciation:
  - High-High (HH) Emergency Trips : Cause immediate fail-safe state transition (State 13)
  - High (H) & Low (L) Warnings    : Alert operator and MES host without aborting cycle
  - Low-Low (LL) Critical Trips     : Annunciate process failure (loss of contact / starvation)
  - Deadband Hysteresis            : Eliminates chattering at boundary conditions

Bit-Packed Industrial Telemetry Architecture:
  - dwAlarmWord1_SafetyTrips       : 32-bit critical trips & E-stop hardware lines
  - dwAlarmWord2_Discrepancies     : 32-bit TMR degradation & process warnings
  - dwStatusWord1_Operational      : 32-bit FSM execution milestones & quality pass/fail
  - dwStatusWord2_Subsystems       : 32-bit actuator energization & 4-bit state nibble
====================================================================================================
*)

(* ---------------------------------------------------------------------------------------------- *)
(* BOND FORCE ISA-18.2 ALARM ENGINE [N]                                                           *)
(* ---------------------------------------------------------------------------------------------- *)
(* High-High Trip (475.0 N) *)
IF rVotedBondForce_N >= rTrip_Force_HH_N THEN
    bAlarm_Force_HH := TRUE;
    bInternalHaltRequested := TRUE;
ELSIF rVotedBondForce_N <= (rTrip_Force_HH_N - rDeadband_Force_N) THEN
    bAlarm_Force_HH := FALSE;
END_IF;

(* High Warning (455.0 N) *)
IF rVotedBondForce_N >= rTrip_Force_H_N THEN
    bAlarm_Force_H := TRUE;
ELSIF rVotedBondForce_N <= (rTrip_Force_H_N - rDeadband_Force_N) THEN
    bAlarm_Force_H := FALSE;
END_IF;

(* Low-Low Trip during Eutectic Bonding Hold (State 8) *)
IF (iCurrentFsmState = 8) AND (rVotedBondForce_N <= rTrip_Force_LL_N) AND (rStateTimeAccum_ms >= 50.0) THEN
    bAlarm_Force_LL := TRUE;
    bInternalHaltRequested := TRUE;
ELSIF rVotedBondForce_N >= (rTrip_Force_LL_N + rDeadband_Force_N) THEN
    bAlarm_Force_LL := FALSE;
END_IF;

(* Low Warning during Touch Landing (State 6) *)
IF (iCurrentFsmState = 6) AND (rVotedBondForce_N < rTrip_Force_L_N) AND (rStateTimeAccum_ms >= 40.0) THEN
    bAlarm_Force_L := TRUE;
ELSIF rVotedBondForce_N >= (rTrip_Force_L_N + rDeadband_Force_N) THEN
    bAlarm_Force_L := FALSE;
END_IF;

(* ---------------------------------------------------------------------------------------------- *)
(* CERAMIC HEATER TEMPERATURE ISA-18.2 ALARM ENGINE [deg C]                                      *)
(* ---------------------------------------------------------------------------------------------- *)
(* High-High Thermal Runaway Trip (440.0 deg C) *)
IF rVotedInterfaceTemp_degC >= rTrip_Temp_HH_degC THEN
    bAlarm_Temp_HH := TRUE;
    bInternalHaltRequested := TRUE;
ELSIF rVotedInterfaceTemp_degC <= (rTrip_Temp_HH_degC - rDeadband_Temp_degC) THEN
    bAlarm_Temp_HH := FALSE;
END_IF;

(* High Warning (425.0 deg C) *)
IF rVotedInterfaceTemp_degC >= rTrip_Temp_H_degC THEN
    bAlarm_Temp_H := TRUE;
ELSIF rVotedInterfaceTemp_degC <= (rTrip_Temp_H_degC - rDeadband_Temp_degC) THEN
    bAlarm_Temp_H := FALSE;
END_IF;

(* Low-Low Heater Failure Trip during Eutectic Hold (State 8) *)
IF (iCurrentFsmState = 8) AND (rVotedInterfaceTemp_degC <= rTrip_Temp_LL_degC) THEN
    bAlarm_Temp_LL := TRUE;
    bInternalHaltRequested := TRUE;
ELSIF rVotedInterfaceTemp_degC >= (rTrip_Temp_LL_degC + rDeadband_Temp_degC) THEN
    bAlarm_Temp_LL := FALSE;
END_IF;

(* ---------------------------------------------------------------------------------------------- *)
(* SOLDER MICRO-BUMP COLLAPSE DEPTH ALARM ENGINE [um]                                             *)
(* ---------------------------------------------------------------------------------------------- *)
(* High-High Squeeze-Out Short Circuit Trip (22.0 um) *)
IF rEstimatedSolderCollapse_um >= rTrip_Collapse_HH_um THEN
    bAlarm_Collapse_HH := TRUE;
    bInternalHaltRequested := TRUE;
ELSIF rEstimatedSolderCollapse_um <= (rTrip_Collapse_HH_um - rDeadband_Collapse_um) THEN
    bAlarm_Collapse_HH := FALSE;
END_IF;

(* High Warning (16.5 um) *)
IF rEstimatedSolderCollapse_um >= rTrip_Collapse_H_um THEN
    bAlarm_Collapse_H := TRUE;
ELSIF rEstimatedSolderCollapse_um <= (rTrip_Collapse_H_um - rDeadband_Collapse_um) THEN
    bAlarm_Collapse_H := FALSE;
END_IF;

(* Low-Low Non-Wet Insufficient Collapse Trip at end of State 8 *)
IF (iCurrentFsmState = 8) AND (rStateTimeAccum_ms >= rRecipeEutecticHoldTime_ms) AND (rEstimatedSolderCollapse_um <= rTrip_Collapse_LL_um) THEN
    bAlarm_Collapse_LL := TRUE;
    bInternalHaltRequested := TRUE;
ELSIF rEstimatedSolderCollapse_um >= (rTrip_Collapse_LL_um + rDeadband_Collapse_um) THEN
    bAlarm_Collapse_LL := FALSE;
END_IF;

(* ---------------------------------------------------------------------------------------------- *)
(* SUBSTRATE VACUUM CHUCK HOLDING ALARM ENGINE [kPa]                                              *)
(* ---------------------------------------------------------------------------------------------- *)
(* High-High Vacuum Loss Trip (>-25.0 kPa) *)
IF rVotedChuckVacuum_kPa >= rTrip_Vac_HH_kPa THEN
    bAlarm_Vac_HH := TRUE;
    IF bCycleBusy THEN
        bInternalHaltRequested := TRUE;
    END_IF;
ELSIF rVotedChuckVacuum_kPa <= (rTrip_Vac_HH_kPa - rDeadband_Vac_kPa) THEN
    bAlarm_Vac_HH := FALSE;
END_IF;

(* High Vacuum Degradation Warning (>-65.0 kPa) *)
IF rVotedChuckVacuum_kPa >= rTrip_Vac_H_kPa THEN
    bAlarm_Vac_H := TRUE;
ELSIF rVotedChuckVacuum_kPa <= (rTrip_Vac_H_kPa - rDeadband_Vac_kPa) THEN
    bAlarm_Vac_H := FALSE;
END_IF;

(* ---------------------------------------------------------------------------------------------- *)
(* 6-AXIS CHUCK CO-PLANARITY TILT ALARM ENGINE [urad]                                             *)
(* ---------------------------------------------------------------------------------------------- *)
(* High-High Critical Tilt Trip (12.0 urad) *)
IF (ABS(rChuckTilt_Rx) >= rTrip_Tilt_HH_urad) OR (ABS(rChuckTilt_Ry) >= rTrip_Tilt_HH_urad) THEN
    bAlarm_Tilt_HH := TRUE;
    IF (iCurrentFsmState >= 6) AND (iCurrentFsmState <= 9) THEN
        bInternalHaltRequested := TRUE;
    END_IF;
ELSIF (ABS(rChuckTilt_Rx) <= (rTrip_Tilt_HH_urad - rDeadband_Tilt_urad)) AND (ABS(rChuckTilt_Ry) <= (rTrip_Tilt_HH_urad - rDeadband_Tilt_urad)) THEN
    bAlarm_Tilt_HH := FALSE;
END_IF;

(* High Tilt Warning (6.0 urad) *)
IF (ABS(rChuckTilt_Rx) >= rTrip_Tilt_H_urad) OR (ABS(rChuckTilt_Ry) >= rTrip_Tilt_H_urad) THEN
    bAlarm_Tilt_H := TRUE;
ELSIF (ABS(rChuckTilt_Rx) <= (rTrip_Tilt_H_urad - rDeadband_Tilt_urad)) AND (ABS(rChuckTilt_Ry) <= (rTrip_Tilt_H_urad - rDeadband_Tilt_urad)) THEN
    bAlarm_Tilt_H := FALSE;
END_IF;

(* ---------------------------------------------------------------------------------------------- *)
(* PROCESS ATMOSPHERE OXYGEN & FORMIC VAPOR ALARM ENGINE                                          *)
(* ---------------------------------------------------------------------------------------------- *)
(* Oxygen High-High Ingress Trip (80.0 ppm) *)
IF rChamber_O2_PPM >= rTrip_O2_HH_PPM THEN
    bAlarm_O2_HH := TRUE;
    IF iCurrentFsmState = 3 THEN
        bInternalHaltRequested := TRUE;
    END_IF;
ELSIF rChamber_O2_PPM <= (rTrip_O2_HH_PPM - 5.0) THEN
    bAlarm_O2_HH := FALSE;
END_IF;

(* Oxygen High Warning (40.0 ppm) *)
IF rChamber_O2_PPM >= rTrip_O2_H_PPM THEN
    bAlarm_O2_H := TRUE;
ELSIF rChamber_O2_PPM <= (rTrip_O2_H_PPM - 5.0) THEN
    bAlarm_O2_H := FALSE;
END_IF;

(* Formic Acid Flammability High-High Trip (5.0%) *)
IF rFormicAcid_Conc_Pct >= rTrip_Formic_HH_Pct THEN
    bAlarm_Formic_HH := TRUE;
    bInternalHaltRequested := TRUE;
ELSIF rFormicAcid_Conc_Pct <= (rTrip_Formic_HH_Pct - 0.20) THEN
    bAlarm_Formic_HH := FALSE;
END_IF;

(* Formic Acid Insufficient Concentration Low-Low Trip during Deox (State 3) *)
IF (iCurrentFsmState = 3) AND (rStateTimeAccum_ms >= 500.0) AND (rFormicAcid_Conc_Pct <= rTrip_Formic_LL_Pct) THEN
    bAlarm_Formic_LL := TRUE;
ELSIF rFormicAcid_Conc_Pct >= (rTrip_Formic_LL_Pct + 0.20) THEN
    bAlarm_Formic_LL := FALSE;
END_IF;

(* ---------------------------------------------------------------------------------------------- *)
(* ISA-18.2 BIT-PACKED TELEMETRY REGISTERS                                                        *)
(* ---------------------------------------------------------------------------------------------- *)

(* 1. dwAlarmWord1_SafetyTrips (Critical Safety Trips) *)
dwAlarmWord1_SafetyTrips := 16#00000000;
IF NOT bEmergencyStopOk             THEN dwAlarmWord1_SafetyTrips := dwAlarmWord1_SafetyTrips OR 16#00000001; END_IF;
IF NOT bSafetyShieldInterlock       THEN dwAlarmWord1_SafetyTrips := dwAlarmWord1_SafetyTrips OR 16#00000002; END_IF;
IF NOT bExhaustAbatementReady       THEN dwAlarmWord1_SafetyTrips := dwAlarmWord1_SafetyTrips OR 16#00000004; END_IF;
IF bAlarm_Force_HH                  THEN dwAlarmWord1_SafetyTrips := dwAlarmWord1_SafetyTrips OR 16#00000008; END_IF;
IF bAlarm_Force_LL                  THEN dwAlarmWord1_SafetyTrips := dwAlarmWord1_SafetyTrips OR 16#00000010; END_IF;
IF bAlarm_Temp_HH                   THEN dwAlarmWord1_SafetyTrips := dwAlarmWord1_SafetyTrips OR 16#00000020; END_IF;
IF bAlarm_Temp_LL                   THEN dwAlarmWord1_SafetyTrips := dwAlarmWord1_SafetyTrips OR 16#00000040; END_IF;
IF bAlarm_Collapse_HH               THEN dwAlarmWord1_SafetyTrips := dwAlarmWord1_SafetyTrips OR 16#00000080; END_IF;
IF bAlarm_Collapse_LL               THEN dwAlarmWord1_SafetyTrips := dwAlarmWord1_SafetyTrips OR 16#00000100; END_IF;
IF bAlarm_Vac_HH                    THEN dwAlarmWord1_SafetyTrips := dwAlarmWord1_SafetyTrips OR 16#00000200; END_IF;
IF bAlarm_Tilt_HH                   THEN dwAlarmWord1_SafetyTrips := dwAlarmWord1_SafetyTrips OR 16#00000400; END_IF;
IF bAlarm_O2_HH                     THEN dwAlarmWord1_SafetyTrips := dwAlarmWord1_SafetyTrips OR 16#00000800; END_IF;
IF bAlarm_Formic_HH                 THEN dwAlarmWord1_SafetyTrips := dwAlarmWord1_SafetyTrips OR 16#00001000; END_IF;
IF (iForce_VotingMode = 4)          THEN dwAlarmWord1_SafetyTrips := dwAlarmWord1_SafetyTrips OR 16#00002000; END_IF;
IF (iTemp_VotingMode = 4)           THEN dwAlarmWord1_SafetyTrips := dwAlarmWord1_SafetyTrips OR 16#00004000; END_IF;
IF (iZPos_VotingMode = 4)           THEN dwAlarmWord1_SafetyTrips := dwAlarmWord1_SafetyTrips OR 16#00008000; END_IF;
IF (iChuckVac_VotingMode = 4)       THEN dwAlarmWord1_SafetyTrips := dwAlarmWord1_SafetyTrips OR 16#00010000; END_IF;
IF bInternalHaltRequested           THEN dwAlarmWord1_SafetyTrips := dwAlarmWord1_SafetyTrips OR 16#80000000; END_IF;

(* 2. dwAlarmWord2_Discrepancies (TMR Degradations & Process Warnings) *)
dwAlarmWord2_Discrepancies := 16#00000000;
IF NOT bForce_Ch1_Healthy           THEN dwAlarmWord2_Discrepancies := dwAlarmWord2_Discrepancies OR 16#00000001; END_IF;
IF NOT bForce_Ch2_Healthy           THEN dwAlarmWord2_Discrepancies := dwAlarmWord2_Discrepancies OR 16#00000002; END_IF;
IF NOT bForce_Ch3_Healthy           THEN dwAlarmWord2_Discrepancies := dwAlarmWord2_Discrepancies OR 16#00000004; END_IF;
IF NOT bTemp_Ch1_Healthy            THEN dwAlarmWord2_Discrepancies := dwAlarmWord2_Discrepancies OR 16#00000008; END_IF;
IF NOT bTemp_Ch2_Healthy            THEN dwAlarmWord2_Discrepancies := dwAlarmWord2_Discrepancies OR 16#00000010; END_IF;
IF NOT bTemp_Ch3_Healthy            THEN dwAlarmWord2_Discrepancies := dwAlarmWord2_Discrepancies OR 16#00000020; END_IF;
IF NOT bZPos_Ch1_Healthy            THEN dwAlarmWord2_Discrepancies := dwAlarmWord2_Discrepancies OR 16#00000040; END_IF;
IF NOT bZPos_Ch2_Healthy            THEN dwAlarmWord2_Discrepancies := dwAlarmWord2_Discrepancies OR 16#00000080; END_IF;
IF NOT bZPos_Ch3_Healthy            THEN dwAlarmWord2_Discrepancies := dwAlarmWord2_Discrepancies OR 16#00000100; END_IF;
IF NOT bChuckVac_Ch1_Healthy        THEN dwAlarmWord2_Discrepancies := dwAlarmWord2_Discrepancies OR 16#00000200; END_IF;
IF NOT bChuckVac_Ch2_Healthy        THEN dwAlarmWord2_Discrepancies := dwAlarmWord2_Discrepancies OR 16#00000400; END_IF;
IF NOT bChuckVac_Ch3_Healthy        THEN dwAlarmWord2_Discrepancies := dwAlarmWord2_Discrepancies OR 16#00000800; END_IF;
IF bAlarm_Force_H                   THEN dwAlarmWord2_Discrepancies := dwAlarmWord2_Discrepancies OR 16#00001000; END_IF;
IF bAlarm_Force_L                   THEN dwAlarmWord2_Discrepancies := dwAlarmWord2_Discrepancies OR 16#00002000; END_IF;
IF bAlarm_Temp_H                    THEN dwAlarmWord2_Discrepancies := dwAlarmWord2_Discrepancies OR 16#00004000; END_IF;
IF bAlarm_Temp_L                    THEN dwAlarmWord2_Discrepancies := dwAlarmWord2_Discrepancies OR 16#00008000; END_IF;
IF bAlarm_Collapse_H                THEN dwAlarmWord2_Discrepancies := dwAlarmWord2_Discrepancies OR 16#00010000; END_IF;
IF bAlarm_Collapse_L                THEN dwAlarmWord2_Discrepancies := dwAlarmWord2_Discrepancies OR 16#00020000; END_IF;
IF bAlarm_Vac_H                     THEN dwAlarmWord2_Discrepancies := dwAlarmWord2_Discrepancies OR 16#00040000; END_IF;
IF bAlarm_Tilt_H                    THEN dwAlarmWord2_Discrepancies := dwAlarmWord2_Discrepancies OR 16#00080000; END_IF;
IF bAlarm_O2_H                      THEN dwAlarmWord2_Discrepancies := dwAlarmWord2_Discrepancies OR 16#00100000; END_IF;
IF bAlarm_Formic_LL                 THEN dwAlarmWord2_Discrepancies := dwAlarmWord2_Discrepancies OR 16#00200000; END_IF;

(* 3. dwStatusWord1_Operational (System Operational State & Milestones) *)
dwStatusWord1_Operational := 16#00000000;
IF bEnable                          THEN dwStatusWord1_Operational := dwStatusWord1_Operational OR 16#00000001; END_IF;
IF bCycleBusy                       THEN dwStatusWord1_Operational := dwStatusWord1_Operational OR 16#00000002; END_IF;
IF bCycleComplete                   THEN dwStatusWord1_Operational := dwStatusWord1_Operational OR 16#00000004; END_IF;
IF bCycleAborted                    THEN dwStatusWord1_Operational := dwStatusWord1_Operational OR 16#00000008; END_IF;
IF (dwAlarmWord1_SafetyTrips = 0)   THEN dwStatusWord1_Operational := dwStatusWord1_Operational OR 16#00000010; END_IF;
IF bBondZ_DatumLatched              THEN dwStatusWord1_Operational := dwStatusWord1_Operational OR 16#00000020; END_IF;
IF bChuckLevelingSettled            THEN dwStatusWord1_Operational := dwStatusWord1_Operational OR 16#00000040; END_IF;
IF bDeoxidationAtmosphereReady      THEN dwStatusWord1_Operational := dwStatusWord1_Operational OR 16#00000080; END_IF;
IF bBondQualityPass                 THEN dwStatusWord1_Operational := dwStatusWord1_Operational OR 16#00000100; END_IF;
IF bPostBondAcousticComplete        THEN dwStatusWord1_Operational := dwStatusWord1_Operational OR 16#00000200; END_IF;
IF bVisionFiducialLocked            THEN dwStatusWord1_Operational := dwStatusWord1_Operational OR 16#00000400; END_IF;

(* 4. dwStatusWord2_Subsystems (Actuators & FSM State Nibble) *)
dwStatusWord2_Subsystems := INT_TO_DWORD(iCurrentFsmState) AND 16#0000000F;
IF bHeadVacuumSolenoid              THEN dwStatusWord2_Subsystems := dwStatusWord2_Subsystems OR 16#00000010; END_IF;
IF bHeadPurgePuffSolenoid           THEN dwStatusWord2_Subsystems := dwStatusWord2_Subsystems OR 16#00000020; END_IF;
IF bChuckVacuumSolenoid             THEN dwStatusWord2_Subsystems := dwStatusWord2_Subsystems OR 16#00000040; END_IF;
IF bExhaustDiverterValve            THEN dwStatusWord2_Subsystems := dwStatusWord2_Subsystems OR 16#00000080; END_IF;
IF (rCeramicHeaterDuty_Cmd_Pct > 0.0) THEN dwStatusWord2_Subsystems := dwStatusWord2_Subsystems OR 16#00000100; END_IF;
IF (rN2QuenchValve_Cmd_Pct > 0.0)   THEN dwStatusWord2_Subsystems := dwStatusWord2_Subsystems OR 16#00000200; END_IF;
IF (rFormicPurgeValve_Cmd_Pct > 0.0)THEN dwStatusWord2_Subsystems := dwStatusWord2_Subsystems OR 16#00000400; END_IF;
IF (ABS(rVoiceCoilCurrent_Cmd_A) > 0.1) THEN dwStatusWord2_Subsystems := dwStatusWord2_Subsystems OR 16#00000800; END_IF;
IF (ABS(rPiezoZ_Trim_Cmd_um) > 0.05)THEN dwStatusWord2_Subsystems := dwStatusWord2_Subsystems OR 16#00001000; END_IF;

(* Master System Healthy Assessment *)
bSystemHealthy := (dwAlarmWord1_SafetyTrips = 16#00000000);

END_FUNCTION_BLOCK
"""
