# semiconductor_tcb_builder/build_st_phase1_tmr.py

def get_phase1_tmr():
    return """(*
====================================================================================================
PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING WITH DYNAMIC DISCREPANCY TIMERS
Fault-Tolerant Voting Architecture Across 4 Critical High-Integrity Sensor Banks:
  - Bank 1: Multi-Axis Piezo Quartz Bond Force Load Cells [N] (Ch1, Ch2, Ch3)
  - Bank 2: Pulse Ceramic Heater Thin-Film Thermocouples [deg C] (Ch1, Ch2, Ch3)
  - Bank 3: Bond Head Linear Optical Glass Scale Encoders [um] (Ch1, Ch2, Ch3)
  - Bank 4: Substrate Vacuum Chuck Capacitance Diaphragm Gauges [kPa] (Ch1, Ch2, Ch3)

Degradation Hierarchy:
  Mode 1 (2oo3): All 3 channels healthy -> Median selection
  Mode 2 (1oo2): One channel degraded   -> Bumpless arithmetic mean of two healthy channels
  Mode 3 (1oo1): Two channels degraded  -> Fallback single-channel observation with Level 2 alert
  Mode 4 (TRIP): All channels failed    -> Safe default, emergency process latch, FSM trip
====================================================================================================
*)

(* Execute Cyclic Timing & Scan Interval Calculation *)
IF TIME_TO_REAL(tCycleScanTime) > 0.00001 THEN
    dt_s := TIME_TO_REAL(tCycleScanTime) / 1000.0;
ELSE
    dt_s := 0.0010; (* Default nominal 1.0 ms scan interval *)
END_IF;

iExecutionCycleCounter := iExecutionCycleCounter + 1;

(* ---------------------------------------------------------------------------------------------- *)
(* BANK 1: PIEZO QUARTZ BOND HEAD FORCE LOAD CELLS [N]                                            *)
(* ---------------------------------------------------------------------------------------------- *)
rForce_Diff_12 := ABS(rForceSensor_Ch1 - rForceSensor_Ch2);
rForce_Diff_23 := ABS(rForceSensor_Ch2 - rForceSensor_Ch3);
rForce_Diff_31 := ABS(rForceSensor_Ch3 - rForceSensor_Ch1);

(* Channel 1 Outlier Analysis & Discrepancy Integration *)
IF (rForce_Diff_12 > rForce_Tolerance_N) AND (rForce_Diff_31 > rForce_Tolerance_N) THEN
    rForce_DiscrepancyTimer_Ch1 := rForce_DiscrepancyTimer_Ch1 + dt_s;
    IF rForce_DiscrepancyTimer_Ch1 >= rForce_DiscrepancyTripTime_s THEN
        bForce_Ch1_Healthy := FALSE;
    END_IF;
ELSE
    IF rForce_DiscrepancyTimer_Ch1 > 0.0 THEN
        rForce_DiscrepancyTimer_Ch1 := rForce_DiscrepancyTimer_Ch1 - (dt_s * 2.0);
        IF rForce_DiscrepancyTimer_Ch1 < 0.0 THEN
            rForce_DiscrepancyTimer_Ch1 := 0.0;
        END_IF;
    END_IF;
END_IF;

(* Channel 2 Outlier Analysis & Discrepancy Integration *)
IF (rForce_Diff_12 > rForce_Tolerance_N) AND (rForce_Diff_23 > rForce_Tolerance_N) THEN
    rForce_DiscrepancyTimer_Ch2 := rForce_DiscrepancyTimer_Ch2 + dt_s;
    IF rForce_DiscrepancyTimer_Ch2 >= rForce_DiscrepancyTripTime_s THEN
        bForce_Ch2_Healthy := FALSE;
    END_IF;
ELSE
    IF rForce_DiscrepancyTimer_Ch2 > 0.0 THEN
        rForce_DiscrepancyTimer_Ch2 := rForce_DiscrepancyTimer_Ch2 - (dt_s * 2.0);
        IF rForce_DiscrepancyTimer_Ch2 < 0.0 THEN
            rForce_DiscrepancyTimer_Ch2 := 0.0;
        END_IF;
    END_IF;
END_IF;

(* Channel 3 Outlier Analysis & Discrepancy Integration *)
IF (rForce_Diff_23 > rForce_Tolerance_N) AND (rForce_Diff_31 > rForce_Tolerance_N) THEN
    rForce_DiscrepancyTimer_Ch3 := rForce_DiscrepancyTimer_Ch3 + dt_s;
    IF rForce_DiscrepancyTimer_Ch3 >= rForce_DiscrepancyTripTime_s THEN
        bForce_Ch3_Healthy := FALSE;
    END_IF;
ELSE
    IF rForce_DiscrepancyTimer_Ch3 > 0.0 THEN
        rForce_DiscrepancyTimer_Ch3 := rForce_DiscrepancyTimer_Ch3 - (dt_s * 2.0);
        IF rForce_DiscrepancyTimer_Ch3 < 0.0 THEN
            rForce_DiscrepancyTimer_Ch3 := 0.0;
        END_IF;
    END_IF;
END_IF;

(* Bank 1 Voted Selection Engine *)
IF bForce_Ch1_Healthy AND bForce_Ch2_Healthy AND bForce_Ch3_Healthy THEN
    (* Full 2oo3 Median Selection *)
    rVotedBondForce_N := (rForceSensor_Ch1 + rForceSensor_Ch2 + rForceSensor_Ch3)
                       - MIN(MIN(rForceSensor_Ch1, rForceSensor_Ch2), rForceSensor_Ch3)
                       - MAX(MAX(rForceSensor_Ch1, rForceSensor_Ch2), rForceSensor_Ch3);
    iForce_VotingMode := 1;
    bAlarm_TMR_ForceDiscrepancy := FALSE;
ELSIF bForce_Ch1_Healthy AND bForce_Ch2_Healthy THEN
    rVotedBondForce_N := 0.5 * (rForceSensor_Ch1 + rForceSensor_Ch2);
    iForce_VotingMode := 2;
    bAlarm_TMR_ForceDiscrepancy := TRUE;
ELSIF bForce_Ch2_Healthy AND bForce_Ch3_Healthy THEN
    rVotedBondForce_N := 0.5 * (rForceSensor_Ch2 + rForceSensor_Ch3);
    iForce_VotingMode := 2;
    bAlarm_TMR_ForceDiscrepancy := TRUE;
ELSIF bForce_Ch1_Healthy AND bForce_Ch3_Healthy THEN
    rVotedBondForce_N := 0.5 * (rForceSensor_Ch1 + rForceSensor_Ch3);
    iForce_VotingMode := 2;
    bAlarm_TMR_ForceDiscrepancy := TRUE;
ELSIF bForce_Ch1_Healthy THEN
    rVotedBondForce_N := rForceSensor_Ch1;
    iForce_VotingMode := 3;
    bAlarm_TMR_ForceDiscrepancy := TRUE;
ELSIF bForce_Ch2_Healthy THEN
    rVotedBondForce_N := rForceSensor_Ch2;
    iForce_VotingMode := 3;
    bAlarm_TMR_ForceDiscrepancy := TRUE;
ELSIF bForce_Ch3_Healthy THEN
    rVotedBondForce_N := rForceSensor_Ch3;
    iForce_VotingMode := 3;
    bAlarm_TMR_ForceDiscrepancy := TRUE;
ELSE
    rVotedBondForce_N := 0.0;
    iForce_VotingMode := 4;
    bAlarm_TMR_ForceDiscrepancy := TRUE;
    bInternalHaltRequested := TRUE;
END_IF;

(* ---------------------------------------------------------------------------------------------- *)
(* BANK 2: PULSE CERAMIC HEATER THIN-FILM THERMOCOUPLES [deg C]                                   *)
(* ---------------------------------------------------------------------------------------------- *)
rTemp_Diff_12 := ABS(rTempSensor_Ch1 - rTempSensor_Ch2);
rTemp_Diff_23 := ABS(rTempSensor_Ch2 - rTempSensor_Ch3);
rTemp_Diff_31 := ABS(rTempSensor_Ch3 - rTempSensor_Ch1);

(* Channel 1 Outlier Analysis & Discrepancy Integration *)
IF (rTemp_Diff_12 > rTemp_Tolerance_degC) AND (rTemp_Diff_31 > rTemp_Tolerance_degC) THEN
    rTemp_DiscrepancyTimer_Ch1 := rTemp_DiscrepancyTimer_Ch1 + dt_s;
    IF rTemp_DiscrepancyTimer_Ch1 >= rTemp_DiscrepancyTripTime_s THEN
        bTemp_Ch1_Healthy := FALSE;
    END_IF;
ELSE
    IF rTemp_DiscrepancyTimer_Ch1 > 0.0 THEN
        rTemp_DiscrepancyTimer_Ch1 := rTemp_DiscrepancyTimer_Ch1 - (dt_s * 2.0);
        IF rTemp_DiscrepancyTimer_Ch1 < 0.0 THEN
            rTemp_DiscrepancyTimer_Ch1 := 0.0;
        END_IF;
    END_IF;
END_IF;

(* Channel 2 Outlier Analysis & Discrepancy Integration *)
IF (rTemp_Diff_12 > rTemp_Tolerance_degC) AND (rTemp_Diff_23 > rTemp_Tolerance_degC) THEN
    rTemp_DiscrepancyTimer_Ch2 := rTemp_DiscrepancyTimer_Ch2 + dt_s;
    IF rTemp_DiscrepancyTimer_Ch2 >= rTemp_DiscrepancyTripTime_s THEN
        bTemp_Ch2_Healthy := FALSE;
    END_IF;
ELSE
    IF rTemp_DiscrepancyTimer_Ch2 > 0.0 THEN
        rTemp_DiscrepancyTimer_Ch2 := rTemp_DiscrepancyTimer_Ch2 - (dt_s * 2.0);
        IF rTemp_DiscrepancyTimer_Ch2 < 0.0 THEN
            rTemp_DiscrepancyTimer_Ch2 := 0.0;
        END_IF;
    END_IF;
END_IF;

(* Channel 3 Outlier Analysis & Discrepancy Integration *)
IF (rTemp_Diff_23 > rTemp_Tolerance_degC) AND (rTemp_Diff_31 > rTemp_Tolerance_degC) THEN
    rTemp_DiscrepancyTimer_Ch3 := rTemp_DiscrepancyTimer_Ch3 + dt_s;
    IF rTemp_DiscrepancyTimer_Ch3 >= rTemp_DiscrepancyTripTime_s THEN
        bTemp_Ch3_Healthy := FALSE;
    END_IF;
ELSE
    IF rTemp_DiscrepancyTimer_Ch3 > 0.0 THEN
        rTemp_DiscrepancyTimer_Ch3 := rTemp_DiscrepancyTimer_Ch3 - (dt_s * 2.0);
        IF rTemp_DiscrepancyTimer_Ch3 < 0.0 THEN
            rTemp_DiscrepancyTimer_Ch3 := 0.0;
        END_IF;
    END_IF;
END_IF;

(* Bank 2 Voted Selection Engine *)
IF bTemp_Ch1_Healthy AND bTemp_Ch2_Healthy AND bTemp_Ch3_Healthy THEN
    rVotedInterfaceTemp_degC := (rTempSensor_Ch1 + rTempSensor_Ch2 + rTempSensor_Ch3)
                              - MIN(MIN(rTempSensor_Ch1, rTempSensor_Ch2), rTempSensor_Ch3)
                              - MAX(MAX(rTempSensor_Ch1, rTempSensor_Ch2), rTempSensor_Ch3);
    iTemp_VotingMode := 1;
    bAlarm_TMR_TempDiscrepancy := FALSE;
ELSIF bTemp_Ch1_Healthy AND bTemp_Ch2_Healthy THEN
    rVotedInterfaceTemp_degC := 0.5 * (rTempSensor_Ch1 + rTempSensor_Ch2);
    iTemp_VotingMode := 2;
    bAlarm_TMR_TempDiscrepancy := TRUE;
ELSIF bTemp_Ch2_Healthy AND bTemp_Ch3_Healthy THEN
    rVotedInterfaceTemp_degC := 0.5 * (rTempSensor_Ch2 + rTempSensor_Ch3);
    iTemp_VotingMode := 2;
    bAlarm_TMR_TempDiscrepancy := TRUE;
ELSIF bTemp_Ch1_Healthy AND bTemp_Ch3_Healthy THEN
    rVotedInterfaceTemp_degC := 0.5 * (rTempSensor_Ch1 + rTempSensor_Ch3);
    iTemp_VotingMode := 2;
    bAlarm_TMR_TempDiscrepancy := TRUE;
ELSIF bTemp_Ch1_Healthy THEN
    rVotedInterfaceTemp_degC := rTempSensor_Ch1;
    iTemp_VotingMode := 3;
    bAlarm_TMR_TempDiscrepancy := TRUE;
ELSIF bTemp_Ch2_Healthy THEN
    rVotedInterfaceTemp_degC := rTempSensor_Ch2;
    iTemp_VotingMode := 3;
    bAlarm_TMR_TempDiscrepancy := TRUE;
ELSIF bTemp_Ch3_Healthy THEN
    rVotedInterfaceTemp_degC := rTempSensor_Ch3;
    iTemp_VotingMode := 3;
    bAlarm_TMR_TempDiscrepancy := TRUE;
ELSE
    rVotedInterfaceTemp_degC := 25.0;
    iTemp_VotingMode := 4;
    bAlarm_TMR_TempDiscrepancy := TRUE;
    bInternalHaltRequested := TRUE;
END_IF;

(* ---------------------------------------------------------------------------------------------- *)
(* BANK 3: BOND HEAD LINEAR OPTICAL GLASS SCALE ENCODERS [um]                                     *)
(* ---------------------------------------------------------------------------------------------- *)
rZPos_Diff_12 := ABS(rZPosSensor_Ch1 - rZPosSensor_Ch2);
rZPos_Diff_23 := ABS(rZPosSensor_Ch2 - rZPosSensor_Ch3);
rZPos_Diff_31 := ABS(rZPosSensor_Ch3 - rZPosSensor_Ch1);

(* Channel 1 Outlier Analysis & Discrepancy Integration *)
IF (rZPos_Diff_12 > rZPos_Tolerance_um) AND (rZPos_Diff_31 > rZPos_Tolerance_um) THEN
    rZPos_DiscrepancyTimer_Ch1 := rZPos_DiscrepancyTimer_Ch1 + dt_s;
    IF rZPos_DiscrepancyTimer_Ch1 >= rZPos_DiscrepancyTripTime_s THEN
        bZPos_Ch1_Healthy := FALSE;
    END_IF;
ELSE
    IF rZPos_DiscrepancyTimer_Ch1 > 0.0 THEN
        rZPos_DiscrepancyTimer_Ch1 := rZPos_DiscrepancyTimer_Ch1 - (dt_s * 2.0);
        IF rZPos_DiscrepancyTimer_Ch1 < 0.0 THEN
            rZPos_DiscrepancyTimer_Ch1 := 0.0;
        END_IF;
    END_IF;
END_IF;

(* Channel 2 Outlier Analysis & Discrepancy Integration *)
IF (rZPos_Diff_12 > rZPos_Tolerance_um) AND (rZPos_Diff_23 > rZPos_Tolerance_um) THEN
    rZPos_DiscrepancyTimer_Ch2 := rZPos_DiscrepancyTimer_Ch2 + dt_s;
    IF rZPos_DiscrepancyTimer_Ch2 >= rZPos_DiscrepancyTripTime_s THEN
        bZPos_Ch2_Healthy := FALSE;
    END_IF;
ELSE
    IF rZPos_DiscrepancyTimer_Ch2 > 0.0 THEN
        rZPos_DiscrepancyTimer_Ch2 := rZPos_DiscrepancyTimer_Ch2 - (dt_s * 2.0);
        IF rZPos_DiscrepancyTimer_Ch2 < 0.0 THEN
            rZPos_DiscrepancyTimer_Ch2 := 0.0;
        END_IF;
    END_IF;
END_IF;

(* Channel 3 Outlier Analysis & Discrepancy Integration *)
IF (rZPos_Diff_23 > rZPos_Tolerance_um) AND (rZPos_Diff_31 > rZPos_Tolerance_um) THEN
    rZPos_DiscrepancyTimer_Ch3 := rZPos_DiscrepancyTimer_Ch3 + dt_s;
    IF rZPos_DiscrepancyTimer_Ch3 >= rZPos_DiscrepancyTripTime_s THEN
        bZPos_Ch3_Healthy := FALSE;
    END_IF;
ELSE
    IF rZPos_DiscrepancyTimer_Ch3 > 0.0 THEN
        rZPos_DiscrepancyTimer_Ch3 := rZPos_DiscrepancyTimer_Ch3 - (dt_s * 2.0);
        IF rZPos_DiscrepancyTimer_Ch3 < 0.0 THEN
            rZPos_DiscrepancyTimer_Ch3 := 0.0;
        END_IF;
    END_IF;
END_IF;

(* Bank 3 Voted Selection Engine *)
IF bZPos_Ch1_Healthy AND bZPos_Ch2_Healthy AND bZPos_Ch3_Healthy THEN
    rVotedZPosition_um := (rZPosSensor_Ch1 + rZPosSensor_Ch2 + rZPosSensor_Ch3)
                        - MIN(MIN(rZPosSensor_Ch1, rZPosSensor_Ch2), rZPosSensor_Ch3)
                        - MAX(MAX(rZPosSensor_Ch1, rZPosSensor_Ch2), rZPosSensor_Ch3);
    iZPos_VotingMode := 1;
    bAlarm_TMR_ZPosDiscrepancy := FALSE;
ELSIF bZPos_Ch1_Healthy AND bZPos_Ch2_Healthy THEN
    rVotedZPosition_um := 0.5 * (rZPosSensor_Ch1 + rZPosSensor_Ch2);
    iZPos_VotingMode := 2;
    bAlarm_TMR_ZPosDiscrepancy := TRUE;
ELSIF bZPos_Ch2_Healthy AND bZPos_Ch3_Healthy THEN
    rVotedZPosition_um := 0.5 * (rZPosSensor_Ch2 + rZPosSensor_Ch3);
    iZPos_VotingMode := 2;
    bAlarm_TMR_ZPosDiscrepancy := TRUE;
ELSIF bZPos_Ch1_Healthy AND bZPos_Ch3_Healthy THEN
    rVotedZPosition_um := 0.5 * (rZPosSensor_Ch1 + rZPosSensor_Ch3);
    iZPos_VotingMode := 2;
    bAlarm_TMR_ZPosDiscrepancy := TRUE;
ELSIF bZPos_Ch1_Healthy THEN
    rVotedZPosition_um := rZPosSensor_Ch1;
    iZPos_VotingMode := 3;
    bAlarm_TMR_ZPosDiscrepancy := TRUE;
ELSIF bZPos_Ch2_Healthy THEN
    rVotedZPosition_um := rZPosSensor_Ch2;
    iZPos_VotingMode := 3;
    bAlarm_TMR_ZPosDiscrepancy := TRUE;
ELSIF bZPos_Ch3_Healthy THEN
    rVotedZPosition_um := rZPosSensor_Ch3;
    iZPos_VotingMode := 3;
    bAlarm_TMR_ZPosDiscrepancy := TRUE;
ELSE
    rVotedZPosition_um := 0.0;
    iZPos_VotingMode := 4;
    bAlarm_TMR_ZPosDiscrepancy := TRUE;
    bInternalHaltRequested := TRUE;
END_IF;

(* ---------------------------------------------------------------------------------------------- *)
(* BANK 4: SUBSTRATE VACUUM CHUCK CAPACITANCE DIAPHRAGM GAUGES [kPa]                              *)
(* ---------------------------------------------------------------------------------------------- *)
rChuckVac_Diff_12 := ABS(rChuckVacSensor_Ch1 - rChuckVacSensor_Ch2);
rChuckVac_Diff_23 := ABS(rChuckVacSensor_Ch2 - rChuckVacSensor_Ch3);
rChuckVac_Diff_31 := ABS(rChuckVacSensor_Ch3 - rChuckVacSensor_Ch1);

(* Channel 1 Outlier Analysis & Discrepancy Integration *)
IF (rChuckVac_Diff_12 > rChuckVac_Tolerance_kPa) AND (rChuckVac_Diff_31 > rChuckVac_Tolerance_kPa) THEN
    rChuckVac_DiscrepancyTimer_Ch1 := rChuckVac_DiscrepancyTimer_Ch1 + dt_s;
    IF rChuckVac_DiscrepancyTimer_Ch1 >= rChuckVac_DiscrepancyTripTime_s THEN
        bChuckVac_Ch1_Healthy := FALSE;
    END_IF;
ELSE
    IF rChuckVac_DiscrepancyTimer_Ch1 > 0.0 THEN
        rChuckVac_DiscrepancyTimer_Ch1 := rChuckVac_DiscrepancyTimer_Ch1 - (dt_s * 2.0);
        IF rChuckVac_DiscrepancyTimer_Ch1 < 0.0 THEN
            rChuckVac_DiscrepancyTimer_Ch1 := 0.0;
        END_IF;
    END_IF;
END_IF;

(* Channel 2 Outlier Analysis & Discrepancy Integration *)
IF (rChuckVac_Diff_12 > rChuckVac_Tolerance_kPa) AND (rChuckVac_Diff_23 > rChuckVac_Tolerance_kPa) THEN
    rChuckVac_DiscrepancyTimer_Ch2 := rChuckVac_DiscrepancyTimer_Ch2 + dt_s;
    IF rChuckVac_DiscrepancyTimer_Ch2 >= rChuckVac_DiscrepancyTripTime_s THEN
        bChuckVac_Ch2_Healthy := FALSE;
    END_IF;
ELSE
    IF rChuckVac_DiscrepancyTimer_Ch2 > 0.0 THEN
        rChuckVac_DiscrepancyTimer_Ch2 := rChuckVac_DiscrepancyTimer_Ch2 - (dt_s * 2.0);
        IF rChuckVac_DiscrepancyTimer_Ch2 < 0.0 THEN
            rChuckVac_DiscrepancyTimer_Ch2 := 0.0;
        END_IF;
    END_IF;
END_IF;

(* Channel 3 Outlier Analysis & Discrepancy Integration *)
IF (rChuckVac_Diff_23 > rChuckVac_Tolerance_kPa) AND (rChuckVac_Diff_31 > rChuckVac_Tolerance_kPa) THEN
    rChuckVac_DiscrepancyTimer_Ch3 := rChuckVac_DiscrepancyTimer_Ch3 + dt_s;
    IF rChuckVac_DiscrepancyTimer_Ch3 >= rChuckVac_DiscrepancyTripTime_s THEN
        bChuckVac_Ch3_Healthy := FALSE;
    END_IF;
ELSE
    IF rChuckVac_DiscrepancyTimer_Ch3 > 0.0 THEN
        rChuckVac_DiscrepancyTimer_Ch3 := rChuckVac_DiscrepancyTimer_Ch3 - (dt_s * 2.0);
        IF rChuckVac_DiscrepancyTimer_Ch3 < 0.0 THEN
            rChuckVac_DiscrepancyTimer_Ch3 := 0.0;
        END_IF;
    END_IF;
END_IF;

(* Bank 4 Voted Selection Engine *)
IF bChuckVac_Ch1_Healthy AND bChuckVac_Ch2_Healthy AND bChuckVac_Ch3_Healthy THEN
    rVotedChuckVacuum_kPa := (rChuckVacSensor_Ch1 + rChuckVacSensor_Ch2 + rChuckVacSensor_Ch3)
                           - MIN(MIN(rChuckVacSensor_Ch1, rChuckVacSensor_Ch2), rChuckVacSensor_Ch3)
                           - MAX(MAX(rChuckVacSensor_Ch1, rChuckVacSensor_Ch2), rChuckVacSensor_Ch3);
    iChuckVac_VotingMode := 1;
    bAlarm_TMR_VacDiscrepancy := FALSE;
ELSIF bChuckVac_Ch1_Healthy AND bChuckVac_Ch2_Healthy THEN
    rVotedChuckVacuum_kPa := 0.5 * (rChuckVacSensor_Ch1 + rChuckVacSensor_Ch2);
    iChuckVac_VotingMode := 2;
    bAlarm_TMR_VacDiscrepancy := TRUE;
ELSIF bChuckVac_Ch2_Healthy AND bChuckVac_Ch3_Healthy THEN
    rVotedChuckVacuum_kPa := 0.5 * (rChuckVacSensor_Ch2 + rChuckVacSensor_Ch3);
    iChuckVac_VotingMode := 2;
    bAlarm_TMR_VacDiscrepancy := TRUE;
ELSIF bChuckVac_Ch1_Healthy AND bChuckVac_Ch3_Healthy THEN
    rVotedChuckVacuum_kPa := 0.5 * (rChuckVacSensor_Ch1 + rChuckVacSensor_Ch3);
    iChuckVac_VotingMode := 2;
    bAlarm_TMR_VacDiscrepancy := TRUE;
ELSIF bChuckVac_Ch1_Healthy THEN
    rVotedChuckVacuum_kPa := rChuckVacSensor_Ch1;
    iChuckVac_VotingMode := 3;
    bAlarm_TMR_VacDiscrepancy := TRUE;
ELSIF bChuckVac_Ch2_Healthy THEN
    rVotedChuckVacuum_kPa := rChuckVacSensor_Ch2;
    iChuckVac_VotingMode := 3;
    bAlarm_TMR_VacDiscrepancy := TRUE;
ELSIF bChuckVac_Ch3_Healthy THEN
    rVotedChuckVacuum_kPa := rChuckVacSensor_Ch3;
    iChuckVac_VotingMode := 3;
    bAlarm_TMR_VacDiscrepancy := TRUE;
ELSE
    rVotedChuckVacuum_kPa := 0.0;
    iChuckVac_VotingMode := 4;
    bAlarm_TMR_VacDiscrepancy := TRUE;
    bInternalHaltRequested := TRUE;
END_IF;
"""
