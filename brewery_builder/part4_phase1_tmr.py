# brewery_builder/part4_phase1_tmr.py

def get_part4():
    return """(* ============================================================================================== *)
(* PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING WITH DISCREPANCY TIMERS            *)
(* ============================================================================================== *)

(* ---------------------------------------------------------------------------------------------- *)
(* CHANNEL 1: LAUTER TUN GRAIN BED DIFFERENTIAL PRESSURE (DP) VOTING [mbar]                       *)
(* ---------------------------------------------------------------------------------------------- *)
fCh1_S1_Val := fLauterDP_Sensor1;
fCh1_S2_Val := fLauterDP_Sensor2;
fCh1_S3_Val := fLauterDP_Sensor3;

(* Sensor Range & Signal Validity Diagnostics (-2.0 to 95.0 mbar) *)
bCh1_S1_Valid := (fCh1_S1_Val >= -2.0) AND (fCh1_S1_Val <= 95.0) AND NOT bCh1_S1_FaultLatched;
bCh1_S2_Valid := (fCh1_S2_Val >= -2.0) AND (fCh1_S2_Val <= 95.0) AND NOT bCh1_S2_FaultLatched;
bCh1_S3_Valid := (fCh1_S3_Val >= -2.0) AND (fCh1_S3_Val <= 95.0) AND NOT bCh1_S3_FaultLatched;

(* Pairwise Discrepancy Detection *)
bCh1_Disc_12 := ABS(fCh1_S1_Val - fCh1_S2_Val) > fCh1_TolDelta;
bCh1_Disc_23 := ABS(fCh1_S2_Val - fCh1_S3_Val) > fCh1_TolDelta;
bCh1_Disc_13 := ABS(fCh1_S1_Val - fCh1_S3_Val) > fCh1_TolDelta;

(* Discrepancy Accumulation Filtering Timers *)
IF bCh1_Disc_12 AND bCh1_S1_Valid AND bCh1_S2_Valid THEN
    fCh1_DiscTimer_12 := fCh1_DiscTimer_12 + fCycleDeltaTimeSec;
ELSE
    fCh1_DiscTimer_12 := MAX(0.0, fCh1_DiscTimer_12 - 2.0 * fCycleDeltaTimeSec);
END_IF;

IF bCh1_Disc_23 AND bCh1_S2_Valid AND bCh1_S3_Valid THEN
    fCh1_DiscTimer_23 := fCh1_DiscTimer_23 + fCycleDeltaTimeSec;
ELSE
    fCh1_DiscTimer_23 := MAX(0.0, fCh1_DiscTimer_23 - 2.0 * fCycleDeltaTimeSec);
END_IF;

IF bCh1_Disc_13 AND bCh1_S1_Valid AND bCh1_S3_Valid THEN
    fCh1_DiscTimer_13 := fCh1_DiscTimer_13 + fCycleDeltaTimeSec;
ELSE
    fCh1_DiscTimer_13 := MAX(0.0, fCh1_DiscTimer_13 - 2.0 * fCycleDeltaTimeSec);
END_IF;

(* Fault Isolation & Sensor Latching Logic *)
IF (fCh1_DiscTimer_12 > fCh1_TripTimerThresh) AND (fCh1_DiscTimer_13 > fCh1_TripTimerThresh) THEN
    bCh1_S1_FaultLatched := TRUE;
    bCh1_S1_Valid := FALSE;
END_IF;

IF (fCh1_DiscTimer_12 > fCh1_TripTimerThresh) AND (fCh1_DiscTimer_23 > fCh1_TripTimerThresh) THEN
    bCh1_S2_FaultLatched := TRUE;
    bCh1_S2_Valid := FALSE;
END_IF;

IF (fCh1_DiscTimer_13 > fCh1_TripTimerThresh) AND (fCh1_DiscTimer_23 > fCh1_TripTimerThresh) THEN
    bCh1_S3_FaultLatched := TRUE;
    bCh1_S3_Valid := FALSE;
END_IF;

(* Count Healthy Sensors for Channel 1 *)
iCh1_HealthySensors := 0;
IF bCh1_S1_Valid THEN iCh1_HealthySensors := iCh1_HealthySensors + 1; END_IF;
IF bCh1_S2_Valid THEN iCh1_HealthySensors := iCh1_HealthySensors + 1; END_IF;
IF bCh1_S3_Valid THEN iCh1_HealthySensors := iCh1_HealthySensors + 1; END_IF;

(* 2oo3 Synthesized Voting Execution *)
IF iCh1_HealthySensors = 3 THEN
    (* Three-Way Median Selection *)
    fMedianArray[1] := fCh1_S1_Val;
    fMedianArray[2] := fCh1_S2_Val;
    fMedianArray[3] := fCh1_S3_Val;
    IF fMedianArray[1] > fMedianArray[2] THEN
        fTempSort := fMedianArray[1]; fMedianArray[1] := fMedianArray[2]; fMedianArray[2] := fTempSort;
    END_IF;
    IF fMedianArray[2] > fMedianArray[3] THEN
        fTempSort := fMedianArray[2]; fMedianArray[2] := fMedianArray[3]; fMedianArray[3] := fTempSort;
    END_IF;
    IF fMedianArray[1] > fMedianArray[2] THEN
        fTempSort := fMedianArray[1]; fMedianArray[1] := fMedianArray[2]; fMedianArray[2] := fTempSort;
    END_IF;
    fCh1_VotedVal := fMedianArray[2];
    fCh1_LastGoodVal := fCh1_VotedVal;
    bAlarmTMR_DP_Degraded := FALSE;
ELSIF iCh1_HealthySensors = 2 THEN
    (* Two-Sensor Degraded Mean Voting *)
    IF bCh1_S1_Valid AND bCh1_S2_Valid THEN
        fCh1_VotedVal := (fCh1_S1_Val + fCh1_S2_Val) * 0.500;
    ELSIF bCh1_S2_Valid AND bCh1_S3_Valid THEN
        fCh1_VotedVal := (fCh1_S2_Val + fCh1_S3_Val) * 0.500;
    ELSE
        fCh1_VotedVal := (fCh1_S1_Val + fCh1_S3_Val) * 0.500;
    END_IF;
    fCh1_LastGoodVal := fCh1_VotedVal;
    bAlarmTMR_DP_Degraded := TRUE;
ELSIF iCh1_HealthySensors = 1 THEN
    (* Single Surviving Sensor Mode *)
    IF bCh1_S1_Valid THEN fCh1_VotedVal := fCh1_S1_Val;
    ELSIF bCh1_S2_Valid THEN fCh1_VotedVal := fCh1_S2_Val;
    ELSE fCh1_VotedVal := fCh1_S3_Val;
    END_IF;
    fCh1_LastGoodVal := fCh1_VotedVal;
    bAlarmTMR_DP_Degraded := TRUE;
ELSE
    (* Triple Sensor Failure - Safe Failsafe Clamping *)
    fCh1_VotedVal := fCh1_LastGoodVal;
    bAlarmTMR_DP_Degraded := TRUE;
    bError := TRUE;
END_IF;
fVotedGrainBedDP := fCh1_VotedVal;

(* ---------------------------------------------------------------------------------------------- *)
(* CHANNEL 2: VORLAUF RUNOFF WORT TURBIDITY VOTING [EBC]                                          *)
(* ---------------------------------------------------------------------------------------------- *)
fCh2_S1_Val := fVorlaufTurb_Sensor1;
fCh2_S2_Val := fVorlaufTurb_Sensor2;
fCh2_S3_Val := fVorlaufTurb_Sensor3;

(* Sensor Range & Signal Validity Diagnostics (0.0 to 350.0 EBC) *)
bCh2_S1_Valid := (fCh2_S1_Val >= 0.0) AND (fCh2_S1_Val <= 350.0) AND NOT bCh2_S1_FaultLatched;
bCh2_S2_Valid := (fCh2_S2_Val >= 0.0) AND (fCh2_S2_Val <= 350.0) AND NOT bCh2_S2_FaultLatched;
bCh2_S3_Valid := (fCh2_S3_Val >= 0.0) AND (fCh2_S3_Val <= 350.0) AND NOT bCh2_S3_FaultLatched;

(* Pairwise Discrepancy Detection *)
bCh2_Disc_12 := ABS(fCh2_S1_Val - fCh2_S2_Val) > fCh2_TolDelta;
bCh2_Disc_23 := ABS(fCh2_S2_Val - fCh2_S3_Val) > fCh2_TolDelta;
bCh2_Disc_13 := ABS(fCh2_S1_Val - fCh2_S3_Val) > fCh2_TolDelta;

(* Discrepancy Accumulation Filtering Timers *)
IF bCh2_Disc_12 AND bCh2_S1_Valid AND bCh2_S2_Valid THEN
    fCh2_DiscTimer_12 := fCh2_DiscTimer_12 + fCycleDeltaTimeSec;
ELSE
    fCh2_DiscTimer_12 := MAX(0.0, fCh2_DiscTimer_12 - 2.0 * fCycleDeltaTimeSec);
END_IF;

IF bCh2_Disc_23 AND bCh2_S2_Valid AND bCh2_S3_Valid THEN
    fCh2_DiscTimer_23 := fCh2_DiscTimer_23 + fCycleDeltaTimeSec;
ELSE
    fCh2_DiscTimer_23 := MAX(0.0, fCh2_DiscTimer_23 - 2.0 * fCycleDeltaTimeSec);
END_IF;

IF bCh2_Disc_13 AND bCh2_S1_Valid AND bCh2_S3_Valid THEN
    fCh2_DiscTimer_13 := fCh2_DiscTimer_13 + fCycleDeltaTimeSec;
ELSE
    fCh2_DiscTimer_13 := MAX(0.0, fCh2_DiscTimer_13 - 2.0 * fCycleDeltaTimeSec);
END_IF;

(* Fault Isolation & Sensor Latching Logic *)
IF (fCh2_DiscTimer_12 > fCh2_TripTimerThresh) AND (fCh2_DiscTimer_13 > fCh2_TripTimerThresh) THEN
    bCh2_S1_FaultLatched := TRUE;
    bCh2_S1_Valid := FALSE;
END_IF;

IF (fCh2_DiscTimer_12 > fCh2_TripTimerThresh) AND (fCh2_DiscTimer_23 > fCh2_TripTimerThresh) THEN
    bCh2_S2_FaultLatched := TRUE;
    bCh2_S2_Valid := FALSE;
END_IF;

IF (fCh2_DiscTimer_13 > fCh2_TripTimerThresh) AND (fCh2_DiscTimer_23 > fCh2_TripTimerThresh) THEN
    bCh2_S3_FaultLatched := TRUE;
    bCh2_S3_Valid := FALSE;
END_IF;

(* Count Healthy Sensors for Channel 2 *)
iCh2_HealthySensors := 0;
IF bCh2_S1_Valid THEN iCh2_HealthySensors := iCh2_HealthySensors + 1; END_IF;
IF bCh2_S2_Valid THEN iCh2_HealthySensors := iCh2_HealthySensors + 1; END_IF;
IF bCh2_S3_Valid THEN iCh2_HealthySensors := iCh2_HealthySensors + 1; END_IF;

(* 2oo3 Synthesized Voting Execution *)
IF iCh2_HealthySensors = 3 THEN
    fMedianArray[1] := fCh2_S1_Val;
    fMedianArray[2] := fCh2_S2_Val;
    fMedianArray[3] := fCh2_S3_Val;
    IF fMedianArray[1] > fMedianArray[2] THEN
        fTempSort := fMedianArray[1]; fMedianArray[1] := fMedianArray[2]; fMedianArray[2] := fTempSort;
    END_IF;
    IF fMedianArray[2] > fMedianArray[3] THEN
        fTempSort := fMedianArray[2]; fMedianArray[2] := fMedianArray[3]; fMedianArray[3] := fTempSort;
    END_IF;
    IF fMedianArray[1] > fMedianArray[2] THEN
        fTempSort := fMedianArray[1]; fMedianArray[1] := fMedianArray[2]; fMedianArray[2] := fTempSort;
    END_IF;
    fCh2_VotedVal := fMedianArray[2];
    fCh2_LastGoodVal := fCh2_VotedVal;
    bAlarmTMR_Turb_Degraded := FALSE;
ELSIF iCh2_HealthySensors = 2 THEN
    IF bCh2_S1_Valid AND bCh2_S2_Valid THEN
        fCh2_VotedVal := (fCh2_S1_Val + fCh2_S2_Val) * 0.500;
    ELSIF bCh2_S2_Valid AND bCh2_S3_Valid THEN
        fCh2_VotedVal := (fCh2_S2_Val + fCh2_S3_Val) * 0.500;
    ELSE
        fCh2_VotedVal := (fCh2_S1_Val + fCh2_S3_Val) * 0.500;
    END_IF;
    fCh2_LastGoodVal := fCh2_VotedVal;
    bAlarmTMR_Turb_Degraded := TRUE;
ELSIF iCh2_HealthySensors = 1 THEN
    IF bCh2_S1_Valid THEN fCh2_VotedVal := fCh2_S1_Val;
    ELSIF bCh2_S2_Valid THEN fCh2_VotedVal := fCh2_S2_Val;
    ELSE fCh2_VotedVal := fCh2_S3_Val;
    END_IF;
    fCh2_LastGoodVal := fCh2_VotedVal;
    bAlarmTMR_Turb_Degraded := TRUE;
ELSE
    fCh2_VotedVal := fCh2_LastGoodVal;
    bAlarmTMR_Turb_Degraded := TRUE;
    bError := TRUE;
END_IF;
fVotedWortTurbidity := fCh2_VotedVal;

(* ---------------------------------------------------------------------------------------------- *)
(* CHANNEL 3: WORT KETTLE BOILING TEMPERATURE RTD VOTING [deg C]                                 *)
(* ---------------------------------------------------------------------------------------------- *)
fCh3_S1_Val := fKettleTemp_Sensor1;
fCh3_S2_Val := fKettleTemp_Sensor2;
fCh3_S3_Val := fKettleTemp_Sensor3;

(* Sensor Range & Signal Validity Diagnostics (5.0 to 125.0 deg C) *)
bCh3_S1_Valid := (fCh3_S1_Val >= 5.0) AND (fCh3_S1_Val <= 125.0) AND NOT bCh3_S1_FaultLatched;
bCh3_S2_Valid := (fCh3_S2_Val >= 5.0) AND (fCh3_S2_Val <= 125.0) AND NOT bCh3_S2_FaultLatched;
bCh3_S3_Valid := (fCh3_S3_Val >= 5.0) AND (fCh3_S3_Val <= 125.0) AND NOT bCh3_S3_FaultLatched;

(* Pairwise Discrepancy Detection *)
bCh3_Disc_12 := ABS(fCh3_S1_Val - fCh3_S2_Val) > fCh3_TolDelta;
bCh3_Disc_23 := ABS(fCh3_S2_Val - fCh3_S3_Val) > fCh3_TolDelta;
bCh3_Disc_13 := ABS(fCh3_S1_Val - fCh3_S3_Val) > fCh3_TolDelta;

(* Discrepancy Accumulation Filtering Timers *)
IF bCh3_Disc_12 AND bCh3_S1_Valid AND bCh3_S2_Valid THEN
    fCh3_DiscTimer_12 := fCh3_DiscTimer_12 + fCycleDeltaTimeSec;
ELSE
    fCh3_DiscTimer_12 := MAX(0.0, fCh3_DiscTimer_12 - 2.0 * fCycleDeltaTimeSec);
END_IF;

IF bCh3_Disc_23 AND bCh3_S2_Valid AND bCh3_S3_Valid THEN
    fCh3_DiscTimer_23 := fCh3_DiscTimer_23 + fCycleDeltaTimeSec;
ELSE
    fCh3_DiscTimer_23 := MAX(0.0, fCh3_DiscTimer_23 - 2.0 * fCycleDeltaTimeSec);
END_IF;

IF bCh3_Disc_13 AND bCh3_S1_Valid AND bCh3_S3_Valid THEN
    fCh3_DiscTimer_13 := fCh3_DiscTimer_13 + fCycleDeltaTimeSec;
ELSE
    fCh3_DiscTimer_13 := MAX(0.0, fCh3_DiscTimer_13 - 2.0 * fCycleDeltaTimeSec);
END_IF;

(* Fault Isolation & Sensor Latching Logic *)
IF (fCh3_DiscTimer_12 > fCh3_TripTimerThresh) AND (fCh3_DiscTimer_13 > fCh3_TripTimerThresh) THEN
    bCh3_S1_FaultLatched := TRUE;
    bCh3_S1_Valid := FALSE;
END_IF;

IF (fCh3_DiscTimer_12 > fCh3_TripTimerThresh) AND (fCh3_DiscTimer_23 > fCh3_TripTimerThresh) THEN
    bCh3_S2_FaultLatched := TRUE;
    bCh3_S2_Valid := FALSE;
END_IF;

IF (fCh3_DiscTimer_13 > fCh3_TripTimerThresh) AND (fCh3_DiscTimer_23 > fCh3_TripTimerThresh) THEN
    bCh3_S3_FaultLatched := TRUE;
    bCh3_S3_Valid := FALSE;
END_IF;

(* Count Healthy Sensors for Channel 3 *)
iCh3_HealthySensors := 0;
IF bCh3_S1_Valid THEN iCh3_HealthySensors := iCh3_HealthySensors + 1; END_IF;
IF bCh3_S2_Valid THEN iCh3_HealthySensors := iCh3_HealthySensors + 1; END_IF;
IF bCh3_S3_Valid THEN iCh3_HealthySensors := iCh3_HealthySensors + 1; END_IF;

(* 2oo3 Synthesized Voting Execution *)
IF iCh3_HealthySensors = 3 THEN
    fMedianArray[1] := fCh3_S1_Val;
    fMedianArray[2] := fCh3_S2_Val;
    fMedianArray[3] := fCh3_S3_Val;
    IF fMedianArray[1] > fMedianArray[2] THEN
        fTempSort := fMedianArray[1]; fMedianArray[1] := fMedianArray[2]; fMedianArray[2] := fTempSort;
    END_IF;
    IF fMedianArray[2] > fMedianArray[3] THEN
        fTempSort := fMedianArray[2]; fMedianArray[2] := fMedianArray[3]; fMedianArray[3] := fTempSort;
    END_IF;
    IF fMedianArray[1] > fMedianArray[2] THEN
        fTempSort := fMedianArray[1]; fMedianArray[1] := fMedianArray[2]; fMedianArray[2] := fTempSort;
    END_IF;
    fCh3_VotedVal := fMedianArray[2];
    fCh3_LastGoodVal := fCh3_VotedVal;
    bAlarmTMR_Temp_Degraded := FALSE;
ELSIF iCh3_HealthySensors = 2 THEN
    IF bCh3_S1_Valid AND bCh3_S2_Valid THEN
        fCh3_VotedVal := (fCh3_S1_Val + fCh3_S2_Val) * 0.500;
    ELSIF bCh3_S2_Valid AND bCh3_S3_Valid THEN
        fCh3_VotedVal := (fCh3_S2_Val + fCh3_S3_Val) * 0.500;
    ELSE
        fCh3_VotedVal := (fCh3_S1_Val + fCh3_S3_Val) * 0.500;
    END_IF;
    fCh3_LastGoodVal := fCh3_VotedVal;
    bAlarmTMR_Temp_Degraded := TRUE;
ELSIF iCh3_HealthySensors = 1 THEN
    IF bCh3_S1_Valid THEN fCh3_VotedVal := fCh3_S1_Val;
    ELSIF bCh3_S2_Valid THEN fCh3_VotedVal := fCh3_S2_Val;
    ELSE fCh3_VotedVal := fCh3_S3_Val;
    END_IF;
    fCh3_LastGoodVal := fCh3_VotedVal;
    bAlarmTMR_Temp_Degraded := TRUE;
ELSE
    fCh3_VotedVal := fCh3_LastGoodVal;
    bAlarmTMR_Temp_Degraded := TRUE;
    bError := TRUE;
END_IF;
fVotedKettleTemp := fCh3_VotedVal;

(* ---------------------------------------------------------------------------------------------- *)
(* CHANNEL 4: WORT KETTLE RADAR HYDROSTATIC LEVEL VOTING [%]                                      *)
(* ---------------------------------------------------------------------------------------------- *)
fCh4_S1_Val := fKettleLevel_Sensor1;
fCh4_S2_Val := fKettleLevel_Sensor2;
fCh4_S3_Val := fKettleLevel_Sensor3;

(* Sensor Range & Signal Validity Diagnostics (-1.0 to 105.0 %) *)
bCh4_S1_Valid := (fCh4_S1_Val >= -1.0) AND (fCh4_S1_Val <= 105.0) AND NOT bCh4_S1_FaultLatched;
bCh4_S2_Valid := (fCh4_S2_Val >= -1.0) AND (fCh4_S2_Val <= 105.0) AND NOT bCh4_S2_FaultLatched;
bCh4_S3_Valid := (fCh4_S3_Val >= -1.0) AND (fCh4_S3_Val <= 105.0) AND NOT bCh4_S3_FaultLatched;

(* Pairwise Discrepancy Detection *)
bCh4_Disc_12 := ABS(fCh4_S1_Val - fCh4_S2_Val) > fCh4_TolDelta;
bCh4_Disc_23 := ABS(fCh4_S2_Val - fCh4_S3_Val) > fCh4_TolDelta;
bCh4_Disc_13 := ABS(fCh4_S1_Val - fCh4_S3_Val) > fCh4_TolDelta;

(* Discrepancy Accumulation Filtering Timers *)
IF bCh4_Disc_12 AND bCh4_S1_Valid AND bCh4_S2_Valid THEN
    fCh4_DiscTimer_12 := fCh4_DiscTimer_12 + fCycleDeltaTimeSec;
ELSE
    fCh4_DiscTimer_12 := MAX(0.0, fCh4_DiscTimer_12 - 2.0 * fCycleDeltaTimeSec);
END_IF;

IF bCh4_Disc_23 AND bCh4_S2_Valid AND bCh4_S3_Valid THEN
    fCh4_DiscTimer_23 := fCh4_DiscTimer_23 + fCycleDeltaTimeSec;
ELSE
    fCh4_DiscTimer_23 := MAX(0.0, fCh4_DiscTimer_23 - 2.0 * fCycleDeltaTimeSec);
END_IF;

IF bCh4_Disc_13 AND bCh4_S1_Valid AND bCh4_S3_Valid THEN
    fCh4_DiscTimer_13 := fCh4_DiscTimer_13 + fCycleDeltaTimeSec;
ELSE
    fCh4_DiscTimer_13 := MAX(0.0, fCh4_DiscTimer_13 - 2.0 * fCycleDeltaTimeSec);
END_IF;

(* Fault Isolation & Sensor Latching Logic *)
IF (fCh4_DiscTimer_12 > fCh4_TripTimerThresh) AND (fCh4_DiscTimer_13 > fCh4_TripTimerThresh) THEN
    bCh4_S1_FaultLatched := TRUE;
    bCh4_S1_Valid := FALSE;
END_IF;

IF (fCh4_DiscTimer_12 > fCh4_TripTimerThresh) AND (fCh4_DiscTimer_23 > fCh4_TripTimerThresh) THEN
    bCh4_S2_FaultLatched := TRUE;
    bCh4_S2_Valid := FALSE;
END_IF;

IF (fCh4_DiscTimer_13 > fCh4_TripTimerThresh) AND (fCh4_DiscTimer_23 > fCh4_TripTimerThresh) THEN
    bCh4_S3_FaultLatched := TRUE;
    bCh4_S3_Valid := FALSE;
END_IF;

(* Count Healthy Sensors for Channel 4 *)
iCh4_HealthySensors := 0;
IF bCh4_S1_Valid THEN iCh4_HealthySensors := iCh4_HealthySensors + 1; END_IF;
IF bCh4_S2_Valid THEN iCh4_HealthySensors := iCh4_HealthySensors + 1; END_IF;
IF bCh4_S3_Valid THEN iCh4_HealthySensors := iCh4_HealthySensors + 1; END_IF;

(* 2oo3 Synthesized Voting Execution *)
IF iCh4_HealthySensors = 3 THEN
    fMedianArray[1] := fCh4_S1_Val;
    fMedianArray[2] := fCh4_S2_Val;
    fMedianArray[3] := fCh4_S3_Val;
    IF fMedianArray[1] > fMedianArray[2] THEN
        fTempSort := fMedianArray[1]; fMedianArray[1] := fMedianArray[2]; fMedianArray[2] := fTempSort;
    END_IF;
    IF fMedianArray[2] > fMedianArray[3] THEN
        fTempSort := fMedianArray[2]; fMedianArray[2] := fMedianArray[3]; fMedianArray[3] := fTempSort;
    END_IF;
    IF fMedianArray[1] > fMedianArray[2] THEN
        fTempSort := fMedianArray[1]; fMedianArray[1] := fMedianArray[2]; fMedianArray[2] := fTempSort;
    END_IF;
    fCh4_VotedVal := fMedianArray[2];
    fCh4_LastGoodVal := fCh4_VotedVal;
    bAlarmTMR_Level_Degraded := FALSE;
ELSIF iCh4_HealthySensors = 2 THEN
    IF bCh4_S1_Valid AND bCh4_S2_Valid THEN
        fCh4_VotedVal := (fCh4_S1_Val + fCh4_S2_Val) * 0.500;
    ELSIF bCh4_S2_Valid AND bCh4_S3_Valid THEN
        fCh4_VotedVal := (fCh4_S2_Val + fCh4_S3_Val) * 0.500;
    ELSE
        fCh4_VotedVal := (fCh4_S1_Val + fCh4_S3_Val) * 0.500;
    END_IF;
    fCh4_LastGoodVal := fCh4_VotedVal;
    bAlarmTMR_Level_Degraded := TRUE;
ELSIF iCh4_HealthySensors = 1 THEN
    IF bCh4_S1_Valid THEN fCh4_VotedVal := fCh4_S1_Val;
    ELSIF bCh4_S2_Valid THEN fCh4_VotedVal := fCh4_S2_Val;
    ELSE fCh4_VotedVal := fCh4_S3_Val;
    END_IF;
    fCh4_LastGoodVal := fCh4_VotedVal;
    bAlarmTMR_Level_Degraded := TRUE;
ELSE
    fCh4_VotedVal := fCh4_LastGoodVal;
    bAlarmTMR_Level_Degraded := TRUE;
    bError := TRUE;
END_IF;
fVotedKettleLevel := fCh4_VotedVal;

(* ---------------------------------------------------------------------------------------------- *)
(* CHANNEL 5: CALANDRIA STEAM HEADER SUPPLY PRESSURE VOTING [bar]                                 *)
(* ---------------------------------------------------------------------------------------------- *)
fCh5_S1_Val := fCalandriaSteamP_Sensor1;
fCh5_S2_Val := fCalandriaSteamP_Sensor2;
fCh5_S3_Val := fCalandriaSteamP_Sensor3;

(* Sensor Range & Signal Validity Diagnostics (-0.2 to 8.0 bar) *)
bCh5_S1_Valid := (fCh5_S1_Val >= -0.2) AND (fCh5_S1_Val <= 8.0) AND NOT bCh5_S1_FaultLatched;
bCh5_S2_Valid := (fCh5_S2_Val >= -0.2) AND (fCh5_S2_Val <= 8.0) AND NOT bCh5_S2_FaultLatched;
bCh5_S3_Valid := (fCh5_S3_Val >= -0.2) AND (fCh5_S3_Val <= 8.0) AND NOT bCh5_S3_FaultLatched;

(* Pairwise Discrepancy Detection *)
bCh5_Disc_12 := ABS(fCh5_S1_Val - fCh5_S2_Val) > fCh5_TolDelta;
bCh5_Disc_23 := ABS(fCh5_S2_Val - fCh5_S3_Val) > fCh5_TolDelta;
bCh5_Disc_13 := ABS(fCh5_S1_Val - fCh5_S3_Val) > fCh5_TolDelta;

(* Discrepancy Accumulation Filtering Timers *)
IF bCh5_Disc_12 AND bCh5_S1_Valid AND bCh5_S2_Valid THEN
    fCh5_DiscTimer_12 := fCh5_DiscTimer_12 + fCycleDeltaTimeSec;
ELSE
    fCh5_DiscTimer_12 := MAX(0.0, fCh5_DiscTimer_12 - 2.0 * fCycleDeltaTimeSec);
END_IF;

IF bCh5_Disc_23 AND bCh5_S2_Valid AND bCh5_S3_Valid THEN
    fCh5_DiscTimer_23 := fCh5_DiscTimer_23 + fCycleDeltaTimeSec;
ELSE
    fCh5_DiscTimer_23 := MAX(0.0, fCh5_DiscTimer_23 - 2.0 * fCycleDeltaTimeSec);
END_IF;

IF bCh5_Disc_13 AND bCh5_S1_Valid AND bCh5_S3_Valid THEN
    fCh5_DiscTimer_13 := fCh5_DiscTimer_13 + fCycleDeltaTimeSec;
ELSE
    fCh5_DiscTimer_13 := MAX(0.0, fCh5_DiscTimer_13 - 2.0 * fCycleDeltaTimeSec);
END_IF;

(* Fault Isolation & Sensor Latching Logic *)
IF (fCh5_DiscTimer_12 > fCh5_TripTimerThresh) AND (fCh5_DiscTimer_13 > fCh5_TripTimerThresh) THEN
    bCh5_S1_FaultLatched := TRUE;
    bCh5_S1_Valid := FALSE;
END_IF;

IF (fCh5_DiscTimer_12 > fCh5_TripTimerThresh) AND (fCh5_DiscTimer_23 > fCh5_TripTimerThresh) THEN
    bCh5_S2_FaultLatched := TRUE;
    bCh5_S2_Valid := FALSE;
END_IF;

IF (fCh5_DiscTimer_13 > fCh5_TripTimerThresh) AND (fCh5_DiscTimer_23 > fCh5_TripTimerThresh) THEN
    bCh5_S3_FaultLatched := TRUE;
    bCh5_S3_Valid := FALSE;
END_IF;

(* Count Healthy Sensors for Channel 5 *)
iCh5_HealthySensors := 0;
IF bCh5_S1_Valid THEN iCh5_HealthySensors := iCh5_HealthySensors + 1; END_IF;
IF bCh5_S2_Valid THEN iCh5_HealthySensors := iCh5_HealthySensors + 1; END_IF;
IF bCh5_S3_Valid THEN iCh5_HealthySensors := iCh5_HealthySensors + 1; END_IF;

(* 2oo3 Synthesized Voting Execution *)
IF iCh5_HealthySensors = 3 THEN
    fMedianArray[1] := fCh5_S1_Val;
    fMedianArray[2] := fCh5_S2_Val;
    fMedianArray[3] := fCh5_S3_Val;
    IF fMedianArray[1] > fMedianArray[2] THEN
        fTempSort := fMedianArray[1]; fMedianArray[1] := fMedianArray[2]; fMedianArray[2] := fTempSort;
    END_IF;
    IF fMedianArray[2] > fMedianArray[3] THEN
        fTempSort := fMedianArray[2]; fMedianArray[2] := fMedianArray[3]; fMedianArray[3] := fTempSort;
    END_IF;
    IF fMedianArray[1] > fMedianArray[2] THEN
        fTempSort := fMedianArray[1]; fMedianArray[1] := fMedianArray[2]; fMedianArray[2] := fTempSort;
    END_IF;
    fCh5_VotedVal := fMedianArray[2];
    fCh5_LastGoodVal := fCh5_VotedVal;
    bAlarmTMR_SteamP_Degraded := FALSE;
ELSIF iCh5_HealthySensors = 2 THEN
    IF bCh5_S1_Valid AND bCh5_S2_Valid THEN
        fCh5_VotedVal := (fCh5_S1_Val + fCh5_S2_Val) * 0.500;
    ELSIF bCh5_S2_Valid AND bCh5_S3_Valid THEN
        fCh5_VotedVal := (fCh5_S2_Val + fCh5_S3_Val) * 0.500;
    ELSE
        fCh5_VotedVal := (fCh5_S1_Val + fCh5_S3_Val) * 0.500;
    END_IF;
    fCh5_LastGoodVal := fCh5_VotedVal;
    bAlarmTMR_SteamP_Degraded := TRUE;
ELSIF iCh5_HealthySensors = 1 THEN
    IF bCh5_S1_Valid THEN fCh5_VotedVal := fCh5_S1_Val;
    ELSIF bCh5_S2_Valid THEN fCh5_VotedVal := fCh5_S2_Val;
    ELSE fCh5_VotedVal := fCh5_S3_Val;
    END_IF;
    fCh5_LastGoodVal := fCh5_VotedVal;
    bAlarmTMR_SteamP_Degraded := TRUE;
ELSE
    fCh5_VotedVal := fCh5_LastGoodVal;
    bAlarmTMR_SteamP_Degraded := TRUE;
    bError := TRUE;
END_IF;
fVotedCalandriaSteamP := fCh5_VotedVal;

(* ---------------------------------------------------------------------------------------------- *)
(* CHANNEL 6: LAUTER RUNOFF VOLUMETRIC FLOWMETER VOTING [hL/h]                                    *)
(* ---------------------------------------------------------------------------------------------- *)
fCh6_S1_Val := fRunoffFlow_Sensor1;
fCh6_S2_Val := fRunoffFlow_Sensor2;
fCh6_S3_Val := fRunoffFlow_Sensor3;

(* Sensor Range & Signal Validity Diagnostics (-5.0 to 450.0 hL/h) *)
bCh6_S1_Valid := (fCh6_S1_Val >= -5.0) AND (fCh6_S1_Val <= 450.0) AND NOT bCh6_S1_FaultLatched;
bCh6_S2_Valid := (fCh6_S2_Val >= -5.0) AND (fCh6_S2_Val <= 450.0) AND NOT bCh6_S2_FaultLatched;
bCh6_S3_Valid := (fCh6_S3_Val >= -5.0) AND (fCh6_S3_Val <= 450.0) AND NOT bCh6_S3_FaultLatched;

(* Pairwise Discrepancy Detection *)
bCh6_Disc_12 := ABS(fCh6_S1_Val - fCh6_S2_Val) > fCh6_TolDelta;
bCh6_Disc_23 := ABS(fCh6_S2_Val - fCh6_S3_Val) > fCh6_TolDelta;
bCh6_Disc_13 := ABS(fCh6_S1_Val - fCh6_S3_Val) > fCh6_TolDelta;

(* Discrepancy Accumulation Filtering Timers *)
IF bCh6_Disc_12 AND bCh6_S1_Valid AND bCh6_S2_Valid THEN
    fCh6_DiscTimer_12 := fCh6_DiscTimer_12 + fCycleDeltaTimeSec;
ELSE
    fCh6_DiscTimer_12 := MAX(0.0, fCh6_DiscTimer_12 - 2.0 * fCycleDeltaTimeSec);
END_IF;

IF bCh6_Disc_23 AND bCh6_S2_Valid AND bCh6_S3_Valid THEN
    fCh6_DiscTimer_23 := fCh6_DiscTimer_23 + fCycleDeltaTimeSec;
ELSE
    fCh6_DiscTimer_23 := MAX(0.0, fCh6_DiscTimer_23 - 2.0 * fCycleDeltaTimeSec);
END_IF;

IF bCh6_Disc_13 AND bCh6_S1_Valid AND bCh6_S3_Valid THEN
    fCh6_DiscTimer_13 := fCh6_DiscTimer_13 + fCycleDeltaTimeSec;
ELSE
    fCh6_DiscTimer_13 := MAX(0.0, fCh6_DiscTimer_13 - 2.0 * fCycleDeltaTimeSec);
END_IF;

(* Fault Isolation & Sensor Latching Logic *)
IF (fCh6_DiscTimer_12 > fCh6_TripTimerThresh) AND (fCh6_DiscTimer_13 > fCh6_TripTimerThresh) THEN
    bCh6_S1_FaultLatched := TRUE;
    bCh6_S1_Valid := FALSE;
END_IF;

IF (fCh6_DiscTimer_12 > fCh6_TripTimerThresh) AND (fCh6_DiscTimer_23 > fCh6_TripTimerThresh) THEN
    bCh6_S2_FaultLatched := TRUE;
    bCh6_S2_Valid := FALSE;
END_IF;

IF (fCh6_DiscTimer_13 > fCh6_TripTimerThresh) AND (fCh6_DiscTimer_23 > fCh6_TripTimerThresh) THEN
    bCh6_S3_FaultLatched := TRUE;
    bCh6_S3_Valid := FALSE;
END_IF;

(* Count Healthy Sensors for Channel 6 *)
iCh6_HealthySensors := 0;
IF bCh6_S1_Valid THEN iCh6_HealthySensors := iCh6_HealthySensors + 1; END_IF;
IF bCh6_S2_Valid THEN iCh6_HealthySensors := iCh6_HealthySensors + 1; END_IF;
IF bCh6_S3_Valid THEN iCh6_HealthySensors := iCh6_HealthySensors + 1; END_IF;

(* 2oo3 Synthesized Voting Execution *)
IF iCh6_HealthySensors = 3 THEN
    fMedianArray[1] := fCh6_S1_Val;
    fMedianArray[2] := fCh6_S2_Val;
    fMedianArray[3] := fCh6_S3_Val;
    IF fMedianArray[1] > fMedianArray[2] THEN
        fTempSort := fMedianArray[1]; fMedianArray[1] := fMedianArray[2]; fMedianArray[2] := fTempSort;
    END_IF;
    IF fMedianArray[2] > fMedianArray[3] THEN
        fTempSort := fMedianArray[2]; fMedianArray[2] := fMedianArray[3]; fMedianArray[3] := fTempSort;
    END_IF;
    IF fMedianArray[1] > fMedianArray[2] THEN
        fTempSort := fMedianArray[1]; fMedianArray[1] := fMedianArray[2]; fMedianArray[2] := fTempSort;
    END_IF;
    fCh6_VotedVal := fMedianArray[2];
    fCh6_LastGoodVal := fCh6_VotedVal;
    bAlarmTMR_Flow_Degraded := FALSE;
ELSIF iCh6_HealthySensors = 2 THEN
    IF bCh6_S1_Valid AND bCh6_S2_Valid THEN
        fCh6_VotedVal := (fCh6_S1_Val + fCh6_S2_Val) * 0.500;
    ELSIF bCh6_S2_Valid AND bCh6_S3_Valid THEN
        fCh6_VotedVal := (fCh6_S2_Val + fCh6_S3_Val) * 0.500;
    ELSE
        fCh6_VotedVal := (fCh6_S1_Val + fCh6_S3_Val) * 0.500;
    END_IF;
    fCh6_LastGoodVal := fCh6_VotedVal;
    bAlarmTMR_Flow_Degraded := TRUE;
ELSIF iCh6_HealthySensors = 1 THEN
    IF bCh6_S1_Valid THEN fCh6_VotedVal := fCh6_S1_Val;
    ELSIF bCh6_S2_Valid THEN fCh6_VotedVal := fCh6_S2_Val;
    ELSE fCh6_VotedVal := fCh6_S3_Val;
    END_IF;
    fCh6_LastGoodVal := fCh6_VotedVal;
    bAlarmTMR_Flow_Degraded := TRUE;
ELSE
    fCh6_VotedVal := fCh6_LastGoodVal;
    bAlarmTMR_Flow_Degraded := TRUE;
    bError := TRUE;
END_IF;
fVotedRunoffFlow := fCh6_VotedVal;

(* Common TMR Degradation Flag *)
bDegradedTMRMode := bAlarmTMR_DP_Degraded OR bAlarmTMR_Turb_Degraded OR bAlarmTMR_Temp_Degraded OR
                    bAlarmTMR_Level_Degraded OR bAlarmTMR_SteamP_Degraded OR bAlarmTMR_Flow_Degraded;
"""
