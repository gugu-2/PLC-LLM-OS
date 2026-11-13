# mine_vod_fan_builder/st_phase1_tmr.py

def get_phase1_tmr():
    return """(* ==================================================================================================== *)
(* PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING SUITE WITH DISCREPANCY TIMERS            *)
(* ==================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------- *)
(* SUB-PHASE 1.1: Surface Main Fan Differential Pressure Transmitters (Fan_DP: Ch1, Ch2, Ch3) [kPa]    *)
(* ---------------------------------------------------------------------------------------------------- *)
(* Step 1.1.1: Mid-Value Selection Median Sort across 3 channels *)
arrSortedValues[1] := rFan_DP_Ch1;
arrSortedValues[2] := rFan_DP_Ch2;
arrSortedValues[3] := rFan_DP_Ch3;

IF arrSortedValues[1] > arrSortedValues[2] THEN
    rSortTemp := arrSortedValues[1];
    arrSortedValues[1] := arrSortedValues[2];
    arrSortedValues[2] := rSortTemp;
END_IF;

IF arrSortedValues[2] > arrSortedValues[3] THEN
    rSortTemp := arrSortedValues[2];
    arrSortedValues[2] := arrSortedValues[3];
    arrSortedValues[3] := rSortTemp;
END_IF;

IF arrSortedValues[1] > arrSortedValues[2] THEN
    rSortTemp := arrSortedValues[1];
    arrSortedValues[1] := arrSortedValues[2];
    arrSortedValues[2] := rSortTemp;
END_IF;

(* Step 1.1.2: Channel Discrepancy Monitoring against Median arrSortedValues[2] *)
rDP_Ch1_Delta := ABS(rFan_DP_Ch1 - arrSortedValues[2]);
rDP_Ch2_Delta := ABS(rFan_DP_Ch2 - arrSortedValues[2]);
rDP_Ch3_Delta := ABS(rFan_DP_Ch3 - arrSortedValues[2]);

IF rDP_Ch1_Delta > rDP_Tolerance THEN
    tDP_Ch1_DiscrepancyTimer := tDP_Ch1_DiscrepancyTimer + rCycleTime_s;
    IF tDP_Ch1_DiscrepancyTimer >= tDiscrepancyLimit_s THEN
        bDP_Ch1_Fault := TRUE;
    END_IF;
ELSE
    IF tDP_Ch1_DiscrepancyTimer > 0.0 THEN
        tDP_Ch1_DiscrepancyTimer := tDP_Ch1_DiscrepancyTimer - (0.5 * rCycleTime_s);
        IF tDP_Ch1_DiscrepancyTimer < 0.0 THEN
            tDP_Ch1_DiscrepancyTimer := 0.0;
        END_IF;
    END_IF;
    IF bReset AND (tDP_Ch1_DiscrepancyTimer = 0.0) THEN
        bDP_Ch1_Fault := FALSE;
    END_IF;
END_IF;

IF rDP_Ch2_Delta > rDP_Tolerance THEN
    tDP_Ch2_DiscrepancyTimer := tDP_Ch2_DiscrepancyTimer + rCycleTime_s;
    IF tDP_Ch2_DiscrepancyTimer >= tDiscrepancyLimit_s THEN
        bDP_Ch2_Fault := TRUE;
    END_IF;
ELSE
    IF tDP_Ch2_DiscrepancyTimer > 0.0 THEN
        tDP_Ch2_DiscrepancyTimer := tDP_Ch2_DiscrepancyTimer - (0.5 * rCycleTime_s);
        IF tDP_Ch2_DiscrepancyTimer < 0.0 THEN
            tDP_Ch2_DiscrepancyTimer := 0.0;
        END_IF;
    END_IF;
    IF bReset AND (tDP_Ch2_DiscrepancyTimer = 0.0) THEN
        bDP_Ch2_Fault := FALSE;
    END_IF;
END_IF;

IF rDP_Ch3_Delta > rDP_Tolerance THEN
    tDP_Ch3_DiscrepancyTimer := tDP_Ch3_DiscrepancyTimer + rCycleTime_s;
    IF tDP_Ch3_DiscrepancyTimer >= tDiscrepancyLimit_s THEN
        bDP_Ch3_Fault := TRUE;
    END_IF;
ELSE
    IF tDP_Ch3_DiscrepancyTimer > 0.0 THEN
        tDP_Ch3_DiscrepancyTimer := tDP_Ch3_DiscrepancyTimer - (0.5 * rCycleTime_s);
        IF tDP_Ch3_DiscrepancyTimer < 0.0 THEN
            tDP_Ch3_DiscrepancyTimer := 0.0;
        END_IF;
    END_IF;
    IF bReset AND (tDP_Ch3_DiscrepancyTimer = 0.0) THEN
        bDP_Ch3_Fault := FALSE;
    END_IF;
END_IF;

(* Step 1.1.3: Healthy Channel Accounting & Bumpless Degradation Mode Selection *)
iDP_HealthyCount := 0;
IF NOT bDP_Ch1_Fault THEN iDP_HealthyCount := iDP_HealthyCount + 1; END_IF;
IF NOT bDP_Ch2_Fault THEN iDP_HealthyCount := iDP_HealthyCount + 1; END_IF;
IF NOT bDP_Ch3_Fault THEN iDP_HealthyCount := iDP_HealthyCount + 1; END_IF;

IF iDP_HealthyCount = 3 THEN
    iDP_DegradationMode := 0; (* Nominal 2oo3 Mid-Value *)
    rDP_Voted := arrSortedValues[2];
ELSIF iDP_HealthyCount = 2 THEN
    iDP_DegradationMode := 1; (* Degraded 1oo2 Average of 2 Healthy Channels *)
    IF bDP_Ch1_Fault THEN
        rDP_Voted := 0.5 * (rFan_DP_Ch2 + rFan_DP_Ch3);
    ELSIF bDP_Ch2_Fault THEN
        rDP_Voted := 0.5 * (rFan_DP_Ch1 + rFan_DP_Ch3);
    ELSE
        rDP_Voted := 0.5 * (rFan_DP_Ch1 + rFan_DP_Ch2);
    END_IF;
ELSIF iDP_HealthyCount = 1 THEN
    iDP_DegradationMode := 2; (* Degraded 1oo1 Single Healthy Channel *)
    IF NOT bDP_Ch1_Fault THEN
        rDP_Voted := rFan_DP_Ch1;
    ELSIF NOT bDP_Ch2_Fault THEN
        rDP_Voted := rFan_DP_Ch2;
    ELSE
        rDP_Voted := rFan_DP_Ch3;
    END_IF;
ELSE
    iDP_DegradationMode := 3; (* Failsafe Trip State - All Channels Faulted *)
    bTripGeneral := TRUE;
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* SUB-PHASE 1.2: Ultrasonic Multi-Path Airway Velocity Flowmeters (Air_Vel: Ch1, Ch2, Ch3) [m/s]       *)
(* ---------------------------------------------------------------------------------------------------- *)
arrSortedValues[1] := rAir_Vel_Ch1;
arrSortedValues[2] := rAir_Vel_Ch2;
arrSortedValues[3] := rAir_Vel_Ch3;

IF arrSortedValues[1] > arrSortedValues[2] THEN
    rSortTemp := arrSortedValues[1];
    arrSortedValues[1] := arrSortedValues[2];
    arrSortedValues[2] := rSortTemp;
END_IF;

IF arrSortedValues[2] > arrSortedValues[3] THEN
    rSortTemp := arrSortedValues[2];
    arrSortedValues[2] := arrSortedValues[3];
    arrSortedValues[3] := rSortTemp;
END_IF;

IF arrSortedValues[1] > arrSortedValues[2] THEN
    rSortTemp := arrSortedValues[1];
    arrSortedValues[1] := arrSortedValues[2];
    arrSortedValues[2] := rSortTemp;
END_IF;

rAirVel_Ch1_Delta := ABS(rAir_Vel_Ch1 - arrSortedValues[2]);
rAirVel_Ch2_Delta := ABS(rAir_Vel_Ch2 - arrSortedValues[2]);
rAirVel_Ch3_Delta := ABS(rAir_Vel_Ch3 - arrSortedValues[2]);

IF rAirVel_Ch1_Delta > rAirVel_Tolerance THEN
    tAirVel_Ch1_DiscrepancyTimer := tAirVel_Ch1_DiscrepancyTimer + rCycleTime_s;
    IF tAirVel_Ch1_DiscrepancyTimer >= tDiscrepancyLimit_s THEN
        bAirVel_Ch1_Fault := TRUE;
    END_IF;
ELSE
    IF tAirVel_Ch1_DiscrepancyTimer > 0.0 THEN
        tAirVel_Ch1_DiscrepancyTimer := tAirVel_Ch1_DiscrepancyTimer - (0.5 * rCycleTime_s);
        IF tAirVel_Ch1_DiscrepancyTimer < 0.0 THEN
            tAirVel_Ch1_DiscrepancyTimer := 0.0;
        END_IF;
    END_IF;
    IF bReset AND (tAirVel_Ch1_DiscrepancyTimer = 0.0) THEN
        bAirVel_Ch1_Fault := FALSE;
    END_IF;
END_IF;

IF rAirVel_Ch2_Delta > rAirVel_Tolerance THEN
    tAirVel_Ch2_DiscrepancyTimer := tAirVel_Ch2_DiscrepancyTimer + rCycleTime_s;
    IF tAirVel_Ch2_DiscrepancyTimer >= tDiscrepancyLimit_s THEN
        bAirVel_Ch2_Fault := TRUE;
    END_IF;
ELSE
    IF tAirVel_Ch2_DiscrepancyTimer > 0.0 THEN
        tAirVel_Ch2_DiscrepancyTimer := tAirVel_Ch2_DiscrepancyTimer - (0.5 * rCycleTime_s);
        IF tAirVel_Ch2_DiscrepancyTimer < 0.0 THEN
            tAirVel_Ch2_DiscrepancyTimer := 0.0;
        END_IF;
    END_IF;
    IF bReset AND (tAirVel_Ch2_DiscrepancyTimer = 0.0) THEN
        bAirVel_Ch2_Fault := FALSE;
    END_IF;
END_IF;

IF rAirVel_Ch3_Delta > rAirVel_Tolerance THEN
    tAirVel_Ch3_DiscrepancyTimer := tAirVel_Ch3_DiscrepancyTimer + rCycleTime_s;
    IF tAirVel_Ch3_DiscrepancyTimer >= tDiscrepancyLimit_s THEN
        bAirVel_Ch3_Fault := TRUE;
    END_IF;
ELSE
    IF tAirVel_Ch3_DiscrepancyTimer > 0.0 THEN
        tAirVel_Ch3_DiscrepancyTimer := tAirVel_Ch3_DiscrepancyTimer - (0.5 * rCycleTime_s);
        IF tAirVel_Ch3_DiscrepancyTimer < 0.0 THEN
            tAirVel_Ch3_DiscrepancyTimer := 0.0;
        END_IF;
    END_IF;
    IF bReset AND (tAirVel_Ch3_DiscrepancyTimer = 0.0) THEN
        bAirVel_Ch3_Fault := FALSE;
    END_IF;
END_IF;

iAirVel_HealthyCount := 0;
IF NOT bAirVel_Ch1_Fault THEN iAirVel_HealthyCount := iAirVel_HealthyCount + 1; END_IF;
IF NOT bAirVel_Ch2_Fault THEN iAirVel_HealthyCount := iAirVel_HealthyCount + 1; END_IF;
IF NOT bAirVel_Ch3_Fault THEN iAirVel_HealthyCount := iAirVel_HealthyCount + 1; END_IF;

IF iAirVel_HealthyCount = 3 THEN
    iAirVel_DegradationMode := 0;
    rAirVel_Voted := arrSortedValues[2];
ELSIF iAirVel_HealthyCount = 2 THEN
    iAirVel_DegradationMode := 1;
    IF bAirVel_Ch1_Fault THEN
        rAirVel_Voted := 0.5 * (rAir_Vel_Ch2 + rAir_Vel_Ch3);
    ELSIF bAirVel_Ch2_Fault THEN
        rAirVel_Voted := 0.5 * (rAir_Vel_Ch1 + rAir_Vel_Ch3);
    ELSE
        rAirVel_Voted := 0.5 * (rAir_Vel_Ch1 + rAir_Vel_Ch2);
    END_IF;
ELSIF iAirVel_HealthyCount = 1 THEN
    iAirVel_DegradationMode := 2;
    IF NOT bAirVel_Ch1_Fault THEN
        rAirVel_Voted := rAir_Vel_Ch1;
    ELSIF NOT bAirVel_Ch2_Fault THEN
        rAirVel_Voted := rAir_Vel_Ch2;
    ELSE
        rAirVel_Voted := rAir_Vel_Ch3;
    END_IF;
ELSE
    iAirVel_DegradationMode := 3;
    bTripGeneral := TRUE;
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* SUB-PHASE 1.3: Borehole Electrochemical Toxic Gas Telemetry Sensors (Toxic_Gas: 1, 2, 3) [ppm CO]    *)
(* ---------------------------------------------------------------------------------------------------- *)
arrSortedValues[1] := rToxic_Gas_Ch1;
arrSortedValues[2] := rToxic_Gas_Ch2;
arrSortedValues[3] := rToxic_Gas_Ch3;

IF arrSortedValues[1] > arrSortedValues[2] THEN
    rSortTemp := arrSortedValues[1];
    arrSortedValues[1] := arrSortedValues[2];
    arrSortedValues[2] := rSortTemp;
END_IF;

IF arrSortedValues[2] > arrSortedValues[3] THEN
    rSortTemp := arrSortedValues[2];
    arrSortedValues[2] := arrSortedValues[3];
    arrSortedValues[3] := rSortTemp;
END_IF;

IF arrSortedValues[1] > arrSortedValues[2] THEN
    rSortTemp := arrSortedValues[1];
    arrSortedValues[1] := arrSortedValues[2];
    arrSortedValues[2] := rSortTemp;
END_IF;

rToxicGas_Ch1_Delta := ABS(rToxic_Gas_Ch1 - arrSortedValues[2]);
rToxicGas_Ch2_Delta := ABS(rToxic_Gas_Ch2 - arrSortedValues[2]);
rToxicGas_Ch3_Delta := ABS(rToxic_Gas_Ch3 - arrSortedValues[2]);

IF rToxicGas_Ch1_Delta > rToxicGas_Tolerance THEN
    tToxicGas_Ch1_DiscrepancyTimer := tToxicGas_Ch1_DiscrepancyTimer + rCycleTime_s;
    IF tToxicGas_Ch1_DiscrepancyTimer >= tDiscrepancyLimit_s THEN
        bToxicGas_Ch1_Fault := TRUE;
    END_IF;
ELSE
    IF tToxicGas_Ch1_DiscrepancyTimer > 0.0 THEN
        tToxicGas_Ch1_DiscrepancyTimer := tToxicGas_Ch1_DiscrepancyTimer - (0.5 * rCycleTime_s);
        IF tToxicGas_Ch1_DiscrepancyTimer < 0.0 THEN
            tToxicGas_Ch1_DiscrepancyTimer := 0.0;
        END_IF;
    END_IF;
    IF bReset AND (tToxicGas_Ch1_DiscrepancyTimer = 0.0) THEN
        bToxicGas_Ch1_Fault := FALSE;
    END_IF;
END_IF;

IF rToxicGas_Ch2_Delta > rToxicGas_Tolerance THEN
    tToxicGas_Ch2_DiscrepancyTimer := tToxicGas_Ch2_DiscrepancyTimer + rCycleTime_s;
    IF tToxicGas_Ch2_DiscrepancyTimer >= tDiscrepancyLimit_s THEN
        bToxicGas_Ch2_Fault := TRUE;
    END_IF;
ELSE
    IF tToxicGas_Ch2_DiscrepancyTimer > 0.0 THEN
        tToxicGas_Ch2_DiscrepancyTimer := tToxicGas_Ch2_DiscrepancyTimer - (0.5 * rCycleTime_s);
        IF tToxicGas_Ch2_DiscrepancyTimer < 0.0 THEN
            tToxicGas_Ch2_DiscrepancyTimer := 0.0;
        END_IF;
    END_IF;
    IF bReset AND (tToxicGas_Ch2_DiscrepancyTimer = 0.0) THEN
        bToxicGas_Ch2_Fault := FALSE;
    END_IF;
END_IF;

IF rToxicGas_Ch3_Delta > rToxicGas_Tolerance THEN
    tToxicGas_Ch3_DiscrepancyTimer := tToxicGas_Ch3_DiscrepancyTimer + rCycleTime_s;
    IF tToxicGas_Ch3_DiscrepancyTimer >= tDiscrepancyLimit_s THEN
        bToxicGas_Ch3_Fault := TRUE;
    END_IF;
ELSE
    IF tToxicGas_Ch3_DiscrepancyTimer > 0.0 THEN
        tToxicGas_Ch3_DiscrepancyTimer := tToxicGas_Ch3_DiscrepancyTimer - (0.5 * rCycleTime_s);
        IF tToxicGas_Ch3_DiscrepancyTimer < 0.0 THEN
            tToxicGas_Ch3_DiscrepancyTimer := 0.0;
        END_IF;
    END_IF;
    IF bReset AND (tToxicGas_Ch3_DiscrepancyTimer = 0.0) THEN
        bToxicGas_Ch3_Fault := FALSE;
    END_IF;
END_IF;

iToxicGas_HealthyCount := 0;
IF NOT bToxicGas_Ch1_Fault THEN iToxicGas_HealthyCount := iToxicGas_HealthyCount + 1; END_IF;
IF NOT bToxicGas_Ch2_Fault THEN iToxicGas_HealthyCount := iToxicGas_HealthyCount + 1; END_IF;
IF NOT bToxicGas_Ch3_Fault THEN iToxicGas_HealthyCount := iToxicGas_HealthyCount + 1; END_IF;

IF iToxicGas_HealthyCount = 3 THEN
    iToxicGas_DegradationMode := 0;
    rToxicGas_Voted := arrSortedValues[2];
ELSIF iToxicGas_HealthyCount = 2 THEN
    iToxicGas_DegradationMode := 1;
    IF bToxicGas_Ch1_Fault THEN
        rToxicGas_Voted := 0.5 * (rToxic_Gas_Ch2 + rToxic_Gas_Ch3);
    ELSIF bToxicGas_Ch2_Fault THEN
        rToxicGas_Voted := 0.5 * (rToxic_Gas_Ch1 + rToxic_Gas_Ch3);
    ELSE
        rToxicGas_Voted := 0.5 * (rToxic_Gas_Ch1 + rToxic_Gas_Ch2);
    END_IF;
ELSIF iToxicGas_HealthyCount = 1 THEN
    iToxicGas_DegradationMode := 2;
    IF NOT bToxicGas_Ch1_Fault THEN
        rToxicGas_Voted := rToxic_Gas_Ch1;
    ELSIF NOT bToxicGas_Ch2_Fault THEN
        rToxicGas_Voted := rToxic_Gas_Ch2;
    ELSE
        rToxicGas_Voted := rToxic_Gas_Ch3;
    END_IF;
ELSE
    iToxicGas_DegradationMode := 3;
    bTripGeneral := TRUE;
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* SUB-PHASE 1.4: Surface Main Fan Bearing Triaxial Vibration Transducers (Fan_Vib: 1, 2, 3) [mm/s RMS]  *)
(* ---------------------------------------------------------------------------------------------------- *)
arrSortedValues[1] := rFan_Vib_Ch1;
arrSortedValues[2] := rFan_Vib_Ch2;
arrSortedValues[3] := rFan_Vib_Ch3;

IF arrSortedValues[1] > arrSortedValues[2] THEN
    rSortTemp := arrSortedValues[1];
    arrSortedValues[1] := arrSortedValues[2];
    arrSortedValues[2] := rSortTemp;
END_IF;

IF arrSortedValues[2] > arrSortedValues[3] THEN
    rSortTemp := arrSortedValues[2];
    arrSortedValues[2] := arrSortedValues[3];
    arrSortedValues[3] := rSortTemp;
END_IF;

IF arrSortedValues[1] > arrSortedValues[2] THEN
    rSortTemp := arrSortedValues[1];
    arrSortedValues[1] := arrSortedValues[2];
    arrSortedValues[2] := rSortTemp;
END_IF;

rVib_Ch1_Delta := ABS(rFan_Vib_Ch1 - arrSortedValues[2]);
rVib_Ch2_Delta := ABS(rFan_Vib_Ch2 - arrSortedValues[2]);
rVib_Ch3_Delta := ABS(rFan_Vib_Ch3 - arrSortedValues[2]);

IF rVib_Ch1_Delta > rVib_Tolerance THEN
    tVib_Ch1_DiscrepancyTimer := tVib_Ch1_DiscrepancyTimer + rCycleTime_s;
    IF tVib_Ch1_DiscrepancyTimer >= tDiscrepancyLimit_s THEN
        bVib_Ch1_Fault := TRUE;
    END_IF;
ELSE
    IF tVib_Ch1_DiscrepancyTimer > 0.0 THEN
        tVib_Ch1_DiscrepancyTimer := tVib_Ch1_DiscrepancyTimer - (0.5 * rCycleTime_s);
        IF tVib_Ch1_DiscrepancyTimer < 0.0 THEN
            tVib_Ch1_DiscrepancyTimer := 0.0;
        END_IF;
    END_IF;
    IF bReset AND (tVib_Ch1_DiscrepancyTimer = 0.0) THEN
        bVib_Ch1_Fault := FALSE;
    END_IF;
END_IF;

IF rVib_Ch2_Delta > rVib_Tolerance THEN
    tVib_Ch2_DiscrepancyTimer := tVib_Ch2_DiscrepancyTimer + rCycleTime_s;
    IF tVib_Ch2_DiscrepancyTimer >= tDiscrepancyLimit_s THEN
        bVib_Ch2_Fault := TRUE;
    END_IF;
ELSE
    IF tVib_Ch2_DiscrepancyTimer > 0.0 THEN
        tVib_Ch2_DiscrepancyTimer := tVib_Ch2_DiscrepancyTimer - (0.5 * rCycleTime_s);
        IF tVib_Ch2_DiscrepancyTimer < 0.0 THEN
            tVib_Ch2_DiscrepancyTimer := 0.0;
        END_IF;
    END_IF;
    IF bReset AND (tVib_Ch2_DiscrepancyTimer = 0.0) THEN
        bVib_Ch2_Fault := FALSE;
    END_IF;
END_IF;

IF rVib_Ch3_Delta > rVib_Tolerance THEN
    tVib_Ch3_DiscrepancyTimer := tVib_Ch3_DiscrepancyTimer + rCycleTime_s;
    IF tVib_Ch3_DiscrepancyTimer >= tDiscrepancyLimit_s THEN
        bVib_Ch3_Fault := TRUE;
    END_IF;
ELSE
    IF tVib_Ch3_DiscrepancyTimer > 0.0 THEN
        tVib_Ch3_DiscrepancyTimer := tVib_Ch3_DiscrepancyTimer - (0.5 * rCycleTime_s);
        IF tVib_Ch3_DiscrepancyTimer < 0.0 THEN
            tVib_Ch3_DiscrepancyTimer := 0.0;
        END_IF;
    END_IF;
    IF bReset AND (tVib_Ch3_DiscrepancyTimer = 0.0) THEN
        bVib_Ch3_Fault := FALSE;
    END_IF;
END_IF;

iVib_HealthyCount := 0;
IF NOT bVib_Ch1_Fault THEN iVib_HealthyCount := iVib_HealthyCount + 1; END_IF;
IF NOT bVib_Ch2_Fault THEN iVib_HealthyCount := iVib_HealthyCount + 1; END_IF;
IF NOT bVib_Ch3_Fault THEN iVib_HealthyCount := iVib_HealthyCount + 1; END_IF;

IF iVib_HealthyCount = 3 THEN
    iVib_DegradationMode := 0;
    rVib_Voted := arrSortedValues[2];
ELSIF iVib_HealthyCount = 2 THEN
    iVib_DegradationMode := 1;
    IF bVib_Ch1_Fault THEN
        rVib_Voted := 0.5 * (rFan_Vib_Ch2 + rFan_Vib_Ch3);
    ELSIF bVib_Ch2_Fault THEN
        rVib_Voted := 0.5 * (rFan_Vib_Ch1 + rFan_Vib_Ch3);
    ELSE
        rVib_Voted := 0.5 * (rFan_Vib_Ch1 + rFan_Vib_Ch2);
    END_IF;
ELSIF iVib_HealthyCount = 1 THEN
    iVib_DegradationMode := 2;
    IF NOT bVib_Ch1_Fault THEN
        rVib_Voted := rFan_Vib_Ch1;
    ELSIF NOT bVib_Ch2_Fault THEN
        rVib_Voted := rFan_Vib_Ch2;
    ELSE
        rVib_Voted := rFan_Vib_Ch3;
    END_IF;
ELSE
    iVib_DegradationMode := 3;
    bTripGeneral := TRUE;
END_IF;
"""
