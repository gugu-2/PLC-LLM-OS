# lyophilizer_builder/build_st_phase7_alarms_telemetry.py

def get_phase7_alarms_telemetry():
    return """(* === PHASE 7: ISA-18.2 MULTI-TIER PROCESS ALARMS & 32-BIT BIT-PACKED TELEMETRY === *)
(* ---------------------------------------------------------------------------------------------------- *)
(* 1. PRODUCT CAKE COLLAPSE SAFETY ALARMS (CRITICAL CQA THRESHOLD: -28.5 deg C)                         *)
(* ---------------------------------------------------------------------------------------------------- *)
(* High-High Trip: Product moving boundary interface warming to collapse point *)
IF vecX_hat[3] >= rLimit_Collapse_TripHH THEN
    bAlarm_ProductCollapse_Trip := TRUE;
    IF dwFirstOutWord = 16#00000000 THEN
        dwFirstOutWord := 16#00000001; (* Code 1: Product Collapse Trip *)
    END_IF;
ELSIF vecX_hat[3] < (rLimit_Collapse_TripHH - rAlarmHysteresis_Temp) THEN
    IF bAcknowledgeAlarms THEN
        bAlarm_ProductCollapse_Trip := FALSE;
    END_IF;
END_IF;

(* High Warning: Approaching collapse threshold *)
IF vecX_hat[3] >= rLimit_Collapse_WarnH THEN
    bAlarm_ProductCollapse_Warn := TRUE;
ELSIF vecX_hat[3] < (rLimit_Collapse_WarnH - rAlarmHysteresis_Temp) THEN
    bAlarm_ProductCollapse_Warn := FALSE;
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* 2. CHAMBER VACUUM PROCESS ALARMS (DRYING PHASES 8, 9, 10)                                            *)
(* ---------------------------------------------------------------------------------------------------- *)
IF (nFsmState = 8) OR (nFsmState = 9) OR (nFsmState = 10) THEN
    (* Vacuum Loss High-High Trip *)
    IF rVotedCap >= rLimit_ChamberPress_TripHH THEN
        bAlarm_ChamberVacuum_Trip := TRUE;
        IF dwFirstOutWord = 16#00000000 THEN
            dwFirstOutWord := 16#00000002; (* Code 2: Chamber Vacuum Loss *)
        END_IF;
    ELSIF rVotedCap < (rLimit_ChamberPress_TripHH - rAlarmHysteresis_Press) THEN
        IF bAcknowledgeAlarms THEN
            bAlarm_ChamberVacuum_Trip := FALSE;
        END_IF;
    END_IF;

    (* Vacuum Elevated High Warning *)
    IF rVotedCap >= rLimit_ChamberPress_WarnH THEN
        bAlarm_ChamberVacuum_Warn := TRUE;
    ELSIF rVotedCap < (rLimit_ChamberPress_WarnH - rAlarmHysteresis_Press) THEN
        bAlarm_ChamberVacuum_Warn := FALSE;
    END_IF;
ELSE
    bAlarm_ChamberVacuum_Warn := FALSE;
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* 3. CONDENSER COIL SURFACE TEMPERATURE ALARMS                                                         *)
(* ---------------------------------------------------------------------------------------------------- *)
IF (nFsmState = 7) OR (nFsmState = 8) OR (nFsmState = 9) OR (nFsmState = 10) THEN
    IF rCondenserVotedTemp >= rLimit_CondenserTemp_TripHH THEN
        bAlarm_CondenserTemp_Trip := TRUE;
        IF dwFirstOutWord = 16#00000000 THEN
            dwFirstOutWord := 16#00000003; (* Code 3: Condenser Thermal Runaway *)
        END_IF;
    ELSIF rCondenserVotedTemp < (rLimit_CondenserTemp_TripHH - rAlarmHysteresis_Temp) THEN
        IF bAcknowledgeAlarms THEN
            bAlarm_CondenserTemp_Trip := FALSE;
        END_IF;
    END_IF;

    IF rCondenserVotedTemp >= rLimit_CondenserTemp_WarnH THEN
        bAlarm_CondenserTemp_Warn := TRUE;
    ELSIF rCondenserVotedTemp < (rLimit_CondenserTemp_WarnH - rAlarmHysteresis_Temp) THEN
        bAlarm_CondenserTemp_Warn := FALSE;
    END_IF;
ELSE
    bAlarm_CondenserTemp_Warn := FALSE;
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* 4. 16 SHELVES THERMAL UNIFORMITY ALARMS                                                              *)
(* ---------------------------------------------------------------------------------------------------- *)
IF rShelfTempUniformityDelta_degC >= rLimit_ShelfUniformity_TripHH THEN
    bAlarm_ShelfUniformity_Trip := TRUE;
    IF dwFirstOutWord = 16#00000000 THEN
        dwFirstOutWord := 16#00000005; (* Code 5: Shelf Hydraulic Imbalance *)
    END_IF;
ELSIF rShelfTempUniformityDelta_degC < (rLimit_ShelfUniformity_TripHH - rAlarmHysteresis_Temp) THEN
    IF bAcknowledgeAlarms THEN
        bAlarm_ShelfUniformity_Trip := FALSE;
    END_IF;
END_IF;

IF rShelfTempUniformityDelta_degC >= rLimit_ShelfUniformity_WarnH THEN
    bAlarm_ShelfUniformity_Warn := TRUE;
ELSIF rShelfTempUniformityDelta_degC < (rLimit_ShelfUniformity_WarnH - rAlarmHysteresis_Temp) THEN
    bAlarm_ShelfUniformity_Warn := FALSE;
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* 5. TMR INSTRUMENTATION DISCREPANCY & CRITICAL SENSOR LOSS ALARMS                                      *)
(* ---------------------------------------------------------------------------------------------------- *)
IF (nPiraniHealthMode < 3) OR (nCapHealthMode < 3) OR
   (nShelfTempHealthMode < 3) OR (nVialTempHealthMode < 3) THEN
    bAlarm_TMR_SensorDiscrepancy := TRUE;
ELSE
    bAlarm_TMR_SensorDiscrepancy := FALSE;
END_IF;

IF (nPiraniHealthMode = 0) OR (nCapHealthMode = 0) OR
   (nShelfTempHealthMode = 0) OR (nVialTempHealthMode = 0) THEN
    bAlarm_TMR_CriticalSensorLoss := TRUE;
    IF dwFirstOutWord = 16#00000000 THEN
        dwFirstOutWord := 16#00000006; (* Code 6: Redundancy Loss *)
    END_IF;
ELSE
    bAlarm_TMR_CriticalSensorLoss := FALSE;
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* 6. DOOR INTERLOCK & HARDWARE INTEGRITY SUPERVISION                                                   *)
(* ---------------------------------------------------------------------------------------------------- *)
IF ((rVotedCap < 900.0) OR (nFsmState = 2)) AND NOT bDoorInterlockClosed THEN
    bAlarm_DoorInterlockBreach := TRUE;
    IF dwFirstOutWord = 16#00000000 THEN
        dwFirstOutWord := 16#00000007; (* Code 7: Door Barrier Breach *)
    END_IF;
ELSE
    IF bAcknowledgeAlarms THEN
        bAlarm_DoorInterlockBreach := FALSE;
    END_IF;
END_IF;

(* Reset First-Out Latch upon operator acknowledgment if all trips clear *)
IF bAcknowledgeAlarms AND NOT bAlarm_ProductCollapse_Trip AND NOT bAlarm_ChamberVacuum_Trip AND
   NOT bAlarm_CondenserTemp_Trip AND NOT bAlarm_ShelfUniformity_Trip AND
   NOT bAlarm_TMR_CriticalSensorLoss AND NOT bAlarm_DoorInterlockBreach THEN
    dwFirstOutWord := 16#00000000;
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* ACTUATOR COMMAND MAPPING & HARDWARE SAFETY OVERRIDES                                                 *)
(* ---------------------------------------------------------------------------------------------------- *)
rCmd_ShelfHeaterThyristor_pct    := vecU[1];
rCmd_ShelfRefrigExpValve_pct     := vecU[2];
rCmd_CascadeStage2Suction_pct    := vecU[3];
rCmd_ChamberVacuumBleedValve_pct := vecU[4];
rCmd_ShelfCircPumpSpeed_pct      := vecU[5];

(* Store Previous Actuator Values for Slew Rate Derivation *)
vecU_prev[1] := vecU[1];
vecU_prev[2] := vecU[2];
vecU_prev[3] := vecU[3];
vecU_prev[4] := vecU[4];
vecU_prev[5] := vecU[5];

(* Master Emergency Failsafe Shutdown *)
IF (nFsmState = 13) OR NOT bEmergencyStop THEN
    rCmd_ShelfHeaterThyristor_pct    := 0.0;
    rCmd_ShelfRefrigExpValve_pct     := 0.0;
    rCmd_CascadeStage2Suction_pct    := 0.0;
    rCmd_ChamberVacuumBleedValve_pct := 0.0;
    rCmd_HydraulicStopperingValve_pct:= 0.0;
    bCmd_ChamberIsolationValve       := FALSE;
    bCmd_VacuumBackingPump           := FALSE;
    bCmd_VacuumRootsBlower           := FALSE;
    bCmd_CascadeStage1Compressor     := FALSE;
    bCmd_CascadeStage2Compressor     := FALSE;
    bCmd_CIP_SupplyPump              := FALSE;
    bCmd_SIP_PureSteamInletValve     := FALSE;
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* 32-BIT TELEMETRY BIT-PACKED STATUS & ALARM WORDS                                                     *)
(* ---------------------------------------------------------------------------------------------------- *)
(* Bit-Pack dwStatusWord1 *)
dwStatusWord1 := 16#00000000;
dwStatusWord1 := dwStatusWord1 OR INT_TO_DWORD(nFsmState AND 16#000F);
IF bAutoMode                        THEN dwStatusWord1 := dwStatusWord1 OR 16#00000010; END_IF;
IF bEmergencyStop                   THEN dwStatusWord1 := dwStatusWord1 OR 16#00000020; END_IF;
IF bDoorInterlockClosed             THEN dwStatusWord1 := dwStatusWord1 OR 16#00000040; END_IF;
IF bCmd_ChamberIsolationValve       THEN dwStatusWord1 := dwStatusWord1 OR 16#00000080; END_IF;
IF bCmd_VacuumBackingPump           THEN dwStatusWord1 := dwStatusWord1 OR 16#00000100; END_IF;
IF bCmd_VacuumRootsBlower           THEN dwStatusWord1 := dwStatusWord1 OR 16#00000200; END_IF;
IF bCmd_CascadeStage1Compressor     THEN dwStatusWord1 := dwStatusWord1 OR 16#00000400; END_IF;
IF bCmd_CascadeStage2Compressor     THEN dwStatusWord1 := dwStatusWord1 OR 16#00000800; END_IF;
IF bCmd_SterileN2AerationValve      THEN dwStatusWord1 := dwStatusWord1 OR 16#00001000; END_IF;
IF bCmd_CIP_SupplyPump              THEN dwStatusWord1 := dwStatusWord1 OR 16#00002000; END_IF;
IF bCmd_SIP_PureSteamInletValve     THEN dwStatusWord1 := dwStatusWord1 OR 16#00004000; END_IF;
IF bCmd_ChamberCondensateDrainValve THEN dwStatusWord1 := dwStatusWord1 OR 16#00008000; END_IF;
IF bPrimaryDryingComplete           THEN dwStatusWord1 := dwStatusWord1 OR 16#00010000; END_IF;
IF bSecondaryDryingComplete         THEN dwStatusWord1 := dwStatusWord1 OR 16#00020000; END_IF;
IF bStopperingComplete              THEN dwStatusWord1 := dwStatusWord1 OR 16#00040000; END_IF;
IF bPRT_Active                      THEN dwStatusWord1 := dwStatusWord1 OR 16#00080000; END_IF;
IF bDefrostActive                   THEN dwStatusWord1 := dwStatusWord1 OR 16#00100000; END_IF;
IF bStopperingHoldComplete          THEN dwStatusWord1 := dwStatusWord1 OR 16#00200000; END_IF;

(* Bit-Pack dwStatusWord2: Instrumentation Redundancy Health *)
dwStatusWord2 := 16#00000000;
dwStatusWord2 := dwStatusWord2 OR SHL(INT_TO_DWORD(nPiraniHealthMode AND 16#0007), 0);
dwStatusWord2 := dwStatusWord2 OR SHL(INT_TO_DWORD(nCapHealthMode AND 16#0007), 4);
dwStatusWord2 := dwStatusWord2 OR SHL(INT_TO_DWORD(nShelfTempHealthMode AND 16#0007), 8);
dwStatusWord2 := dwStatusWord2 OR SHL(INT_TO_DWORD(nVialTempHealthMode AND 16#0007), 12);
IF bCascadeStage1_Running           THEN dwStatusWord2 := dwStatusWord2 OR 16#00010000; END_IF;
IF bCascadeStage2_Running           THEN dwStatusWord2 := dwStatusWord2 OR 16#00020000; END_IF;
IF bPRT_Passed                      THEN dwStatusWord2 := dwStatusWord2 OR 16#00040000; END_IF;
IF bCondenserTempFault              THEN dwStatusWord2 := dwStatusWord2 OR 16#00080000; END_IF;

(* Bit-Pack dwAlarmWord1: Critical Process Trips *)
dwAlarmWord1 := 16#00000000;
IF bAlarm_ProductCollapse_Trip      THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000001; END_IF;
IF bAlarm_ChamberVacuum_Trip        THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000002; END_IF;
IF bAlarm_CondenserTemp_Trip        THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000004; END_IF;
IF bAlarm_ShelfUniformity_Trip      THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000008; END_IF;
IF bAlarm_TMR_CriticalSensorLoss    THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000010; END_IF;
IF bAlarm_DoorInterlockBreach       THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000020; END_IF;
IF bAlarm_SIP_TempFail              THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000040; END_IF;
IF NOT bEmergencyStop               THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000080; END_IF;

(* Bit-Pack dwAlarmWord2: Process Warnings & Redundancy Degradations *)
dwAlarmWord2 := 16#00000000;
IF bAlarm_ProductCollapse_Warn      THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000001; END_IF;
IF bAlarm_ChamberVacuum_Warn        THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000002; END_IF;
IF bAlarm_CondenserTemp_Warn        THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000004; END_IF;
IF bAlarm_ShelfUniformity_Warn      THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000008; END_IF;
IF bAlarm_TMR_SensorDiscrepancy     THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000010; END_IF;
IF bPiraniFault_A                   THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000100; END_IF;
IF bPiraniFault_B                   THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000200; END_IF;
IF bPiraniFault_C                   THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000400; END_IF;
IF bCapFault_A                      THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000800; END_IF;
IF bCapFault_B                      THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00001000; END_IF;
IF bCapFault_C                      THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00002000; END_IF;
IF bShelfTempFault_A                THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00004000; END_IF;
IF bShelfTempFault_B                THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00008000; END_IF;
IF bShelfTempFault_C                THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00010000; END_IF;
IF bVialTempFault_A                 THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00020000; END_IF;
IF bVialTempFault_B                 THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00040000; END_IF;
IF bVialTempFault_C                 THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00080000; END_IF;

(* Increment Master Execution Scan Counter and Elapsed Production Time *)
nScanCounter := nScanCounter + 1;
rElapsedCycleTime_s := rElapsedCycleTime_s + tScanInterval_s;

END_FUNCTION_BLOCK
"""
