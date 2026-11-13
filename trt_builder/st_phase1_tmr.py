# trt_builder/st_phase1_tmr.py
"""
Phase 1: 2oo3 Triple Modular Redundancy (TMR) Sensor Voting Suite
for FB_Steel_BlastFurnace_TopGas_TRT_PowerRecovery
"""

def get_phase1_tmr():
    return """(* ==================================================================================================== *)
(* PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING WITH DISCREPANCY TIMERS & BUMPLESS FALLBACK*)
(* ==================================================================================================== *)
nCycleCounter := nCycleCounter + 1;

(* ---------------------------------------------------------------------------------------------------- *)
(* 2oo3 TMR CHANNEL 1: BLAST FURNACE TOP GAS PLENUM PRESSURE PT-101 [kPa]                                *)
(* Range Envelope: 100.0 to 350.0 kPa. Discrepancy Tolerance: 6.0 kPa.                                   *)
(* ---------------------------------------------------------------------------------------------------- *)
rCh1_ValA := rTopGasPressure_PT101A;
rCh1_ValB := rTopGasPressure_PT101B;
rCh1_ValC := rTopGasPressure_PT101C;

(* Out-of-Range Sensor Hardware Checks *)
IF (rCh1_ValA < 80.0) OR (rCh1_ValA > 380.0) THEN
    bCh1_HealthA := FALSE;
END_IF;
IF (rCh1_ValB < 80.0) OR (rCh1_ValB > 380.0) THEN
    bCh1_HealthB := FALSE;
END_IF;
IF (rCh1_ValC < 80.0) OR (rCh1_ValC > 380.0) THEN
    bCh1_HealthC := FALSE;
END_IF;

(* Discrepancy Evaluation among Active Channels *)
IF bCh1_HealthA AND bCh1_HealthB AND bCh1_HealthC THEN
    (* Evaluate Sensor A Discrepancy against B and C *)
    IF (ABS(rCh1_ValA - rCh1_ValB) > rTMR_TolPressTop) AND (ABS(rCh1_ValA - rCh1_ValC) > rTMR_TolPressTop) THEN
        nCh1_TimerA := nCh1_TimerA + 10;
        IF nCh1_TimerA >= nDiscrepancyTripDelay_ms THEN
            bCh1_HealthA := FALSE;
            bCh1_DegradedLatch := TRUE;
        END_IF;
    ELSE
        IF nCh1_TimerA > 0 THEN
            nCh1_TimerA := nCh1_TimerA - 10;
        END_IF;
    END_IF;

    (* Evaluate Sensor B Discrepancy against A and C *)
    IF (ABS(rCh1_ValB - rCh1_ValA) > rTMR_TolPressTop) AND (ABS(rCh1_ValB - rCh1_ValC) > rTMR_TolPressTop) THEN
        nCh1_TimerB := nCh1_TimerB + 10;
        IF nCh1_TimerB >= nDiscrepancyTripDelay_ms THEN
            bCh1_HealthB := FALSE;
            bCh1_DegradedLatch := TRUE;
        END_IF;
    ELSE
        IF nCh1_TimerB > 0 THEN
            nCh1_TimerB := nCh1_TimerB - 10;
        END_IF;
    END_IF;

    (* Evaluate Sensor C Discrepancy against A and B *)
    IF (ABS(rCh1_ValC - rCh1_ValA) > rTMR_TolPressTop) AND (ABS(rCh1_ValC - rCh1_ValB) > rTMR_TolPressTop) THEN
        nCh1_TimerC := nCh1_TimerC + 10;
        IF nCh1_TimerC >= nDiscrepancyTripDelay_ms THEN
            bCh1_HealthC := FALSE;
            bCh1_DegradedLatch := TRUE;
        END_IF;
    ELSE
        IF nCh1_TimerC > 0 THEN
            nCh1_TimerC := nCh1_TimerC - 10;
        END_IF;
    END_IF;
END_IF;

(* Count Healthy Sensors for Channel 1 *)
nCh1_HealthyCount := 0;
IF bCh1_HealthA THEN nCh1_HealthyCount := nCh1_HealthyCount + 1; END_IF;
IF bCh1_HealthB THEN nCh1_HealthyCount := nCh1_HealthyCount + 1; END_IF;
IF bCh1_HealthC THEN nCh1_HealthyCount := nCh1_HealthyCount + 1; END_IF;

(* Channel 1 Voting Execution *)
IF nCh1_HealthyCount = 3 THEN
    (* 3-Healthy: Mid-Value Median Selector *)
    rTempMin := MIN(rCh1_ValA, MIN(rCh1_ValB, rCh1_ValC));
    rTempMax := MAX(rCh1_ValA, MAX(rCh1_ValB, rCh1_ValC));
    rCh1_Voted := (rCh1_ValA + rCh1_ValB + rCh1_ValC) - rTempMin - rTempMax;
ELSIF nCh1_HealthyCount = 2 THEN
    (* 2-Healthy: Dual Arithmetic Mean Fallback *)
    bCh1_DegradedLatch := TRUE;
    IF bCh1_HealthA AND bCh1_HealthB THEN
        rCh1_Voted := (rCh1_ValA + rCh1_ValB) * 0.50;
    ELSIF bCh1_HealthB AND bCh1_HealthC THEN
        rCh1_Voted := (rCh1_ValB + rCh1_ValC) * 0.50;
    ELSE
        rCh1_Voted := (rCh1_ValA + rCh1_ValC) * 0.50;
    END_IF;
ELSIF nCh1_HealthyCount = 1 THEN
    (* 1-Healthy: Single Transmitter Degraded Tracking *)
    bCh1_DegradedLatch := TRUE;
    IF bCh1_HealthA THEN
        rCh1_Voted := rCh1_ValA;
    ELSIF bCh1_HealthB THEN
        rCh1_Voted := rCh1_ValB;
    ELSE
        rCh1_Voted := rCh1_ValC;
    END_IF;
ELSE
    (* 0-Healthy: Total Loss of Transmitters - Hold Last Valid & Latch Failure *)
    bCh1_TotalFailureLatch := TRUE;
    rCh1_Voted := rCh1_PrevVoted;
END_IF;

(* Filtered Rate-of-Change Calculation (Furnace Slip Surge Detection) *)
rCh1_FilteredROC := 0.85 * rCh1_FilteredROC + 0.15 * ((rCh1_Voted - rCh1_PrevVoted) / rSamplingTime_s);
rCh1_PrevVoted := rCh1_Voted;
rVoted_TopGasPressure := rCh1_Voted;
rTopGasPressure_ROC := rCh1_FilteredROC;
rTopGasPressure_Deviation := rVoted_TopGasPressure - rTopGasPressure_Setpoint;


(* ---------------------------------------------------------------------------------------------------- *)
(* 2oo3 TMR CHANNEL 2: TURBINE INLET NOZZLE BOX PRESSURE PT-201 [kPa]                                    *)
(* Range Envelope: 80.0 to 350.0 kPa. Discrepancy Tolerance: 6.0 kPa.                                    *)
(* ---------------------------------------------------------------------------------------------------- *)
rCh2_ValA := rTurbineInletPressure_PT201A;
rCh2_ValB := rTurbineInletPressure_PT201B;
rCh2_ValC := rTurbineInletPressure_PT201C;

IF (rCh2_ValA < 60.0) OR (rCh2_ValA > 380.0) THEN bCh2_HealthA := FALSE; END_IF;
IF (rCh2_ValB < 60.0) OR (rCh2_ValB > 380.0) THEN bCh2_HealthB := FALSE; END_IF;
IF (rCh2_ValC < 60.0) OR (rCh2_ValC > 380.0) THEN bCh2_HealthC := FALSE; END_IF;

IF bCh2_HealthA AND bCh2_HealthB AND bCh2_HealthC THEN
    IF (ABS(rCh2_ValA - rCh2_ValB) > rTMR_TolPressNozzle) AND (ABS(rCh2_ValA - rCh2_ValC) > rTMR_TolPressNozzle) THEN
        nCh2_TimerA := nCh2_TimerA + 10;
        IF nCh2_TimerA >= nDiscrepancyTripDelay_ms THEN
            bCh2_HealthA := FALSE;
            bCh2_DegradedLatch := TRUE;
        END_IF;
    ELSE
        IF nCh2_TimerA > 0 THEN nCh2_TimerA := nCh2_TimerA - 10; END_IF;
    END_IF;

    IF (ABS(rCh2_ValB - rCh2_ValA) > rTMR_TolPressNozzle) AND (ABS(rCh2_ValB - rCh2_ValC) > rTMR_TolPressNozzle) THEN
        nCh2_TimerB := nCh2_TimerB + 10;
        IF nCh2_TimerB >= nDiscrepancyTripDelay_ms THEN
            bCh2_HealthB := FALSE;
            bCh2_DegradedLatch := TRUE;
        END_IF;
    ELSE
        IF nCh2_TimerB > 0 THEN nCh2_TimerB := nCh2_TimerB - 10; END_IF;
    END_IF;

    IF (ABS(rCh2_ValC - rCh2_ValA) > rTMR_TolPressNozzle) AND (ABS(rCh2_ValC - rCh2_ValB) > rTMR_TolPressNozzle) THEN
        nCh2_TimerC := nCh2_TimerC + 10;
        IF nCh2_TimerC >= nDiscrepancyTripDelay_ms THEN
            bCh2_HealthC := FALSE;
            bCh2_DegradedLatch := TRUE;
        END_IF;
    ELSE
        IF nCh2_TimerC > 0 THEN nCh2_TimerC := nCh2_TimerC - 10; END_IF;
    END_IF;
END_IF;

nCh2_HealthyCount := 0;
IF bCh2_HealthA THEN nCh2_HealthyCount := nCh2_HealthyCount + 1; END_IF;
IF bCh2_HealthB THEN nCh2_HealthyCount := nCh2_HealthyCount + 1; END_IF;
IF bCh2_HealthC THEN nCh2_HealthyCount := nCh2_HealthyCount + 1; END_IF;

IF nCh2_HealthyCount = 3 THEN
    rTempMin := MIN(rCh2_ValA, MIN(rCh2_ValB, rCh2_ValC));
    rTempMax := MAX(rCh2_ValA, MAX(rCh2_ValB, rCh2_ValC));
    rCh2_Voted := (rCh2_ValA + rCh2_ValB + rCh2_ValC) - rTempMin - rTempMax;
ELSIF nCh2_HealthyCount = 2 THEN
    bCh2_DegradedLatch := TRUE;
    IF bCh2_HealthA AND bCh2_HealthB THEN
        rCh2_Voted := (rCh2_ValA + rCh2_ValB) * 0.50;
    ELSIF bCh2_HealthB AND bCh2_HealthC THEN
        rCh2_Voted := (rCh2_ValB + rCh2_ValC) * 0.50;
    ELSE
        rCh2_Voted := (rCh2_ValA + rCh2_ValC) * 0.50;
    END_IF;
ELSIF nCh2_HealthyCount = 1 THEN
    bCh2_DegradedLatch := TRUE;
    IF bCh2_HealthA THEN rCh2_Voted := rCh2_ValA;
    ELSIF bCh2_HealthB THEN rCh2_Voted := rCh2_ValB;
    ELSE rCh2_Voted := rCh2_ValC; END_IF;
ELSE
    bCh2_TotalFailureLatch := TRUE;
    rCh2_Voted := rCh2_PrevVoted;
END_IF;
rCh2_PrevVoted := rCh2_Voted;
rVoted_TurbineInletPressure := rCh2_Voted;


(* ---------------------------------------------------------------------------------------------------- *)
(* 2oo3 TMR CHANNEL 3: BLAST FURNACE TOP GAS MASS FLOW RATE FT-301 [kg/s]                                *)
(* Range Envelope: 20.0 to 320.0 kg/s. Discrepancy Tolerance: 15.0 kg/s.                                 *)
(* ---------------------------------------------------------------------------------------------------- *)
rCh3_ValA := rTopGasMassFlow_FT301A;
rCh3_ValB := rTopGasMassFlow_FT301B;
rCh3_ValC := rTopGasMassFlow_FT301C;

IF (rCh3_ValA < 10.0) OR (rCh3_ValA > 350.0) THEN bCh3_HealthA := FALSE; END_IF;
IF (rCh3_ValB < 10.0) OR (rCh3_ValB > 350.0) THEN bCh3_HealthB := FALSE; END_IF;
IF (rCh3_ValC < 10.0) OR (rCh3_ValC > 350.0) THEN bCh3_HealthC := FALSE; END_IF;

IF bCh3_HealthA AND bCh3_HealthB AND bCh3_HealthC THEN
    IF (ABS(rCh3_ValA - rCh3_ValB) > rTMR_TolFlow) AND (ABS(rCh3_ValA - rCh3_ValC) > rTMR_TolFlow) THEN
        nCh3_TimerA := nCh3_TimerA + 10;
        IF nCh3_TimerA >= nDiscrepancyTripDelay_ms THEN
            bCh3_HealthA := FALSE;
            bCh3_DegradedLatch := TRUE;
        END_IF;
    ELSE
        IF nCh3_TimerA > 0 THEN nCh3_TimerA := nCh3_TimerA - 10; END_IF;
    END_IF;

    IF (ABS(rCh3_ValB - rCh3_ValA) > rTMR_TolFlow) AND (ABS(rCh3_ValB - rCh3_ValC) > rTMR_TolFlow) THEN
        nCh3_TimerB := nCh3_TimerB + 10;
        IF nCh3_TimerB >= nDiscrepancyTripDelay_ms THEN
            bCh3_HealthB := FALSE;
            bCh3_DegradedLatch := TRUE;
        END_IF;
    ELSE
        IF nCh3_TimerB > 0 THEN nCh3_TimerB := nCh3_TimerB - 10; END_IF;
    END_IF;

    IF (ABS(rCh3_ValC - rCh3_ValA) > rTMR_TolFlow) AND (ABS(rCh3_ValC - rCh3_ValB) > rTMR_TolFlow) THEN
        nCh3_TimerC := nCh3_TimerC + 10;
        IF nCh3_TimerC >= nDiscrepancyTripDelay_ms THEN
            bCh3_HealthC := FALSE;
            bCh3_DegradedLatch := TRUE;
        END_IF;
    ELSE
        IF nCh3_TimerC > 0 THEN nCh3_TimerC := nCh3_TimerC - 10; END_IF;
    END_IF;
END_IF;

nCh3_HealthyCount := 0;
IF bCh3_HealthA THEN nCh3_HealthyCount := nCh3_HealthyCount + 1; END_IF;
IF bCh3_HealthB THEN nCh3_HealthyCount := nCh3_HealthyCount + 1; END_IF;
IF bCh3_HealthC THEN nCh3_HealthyCount := nCh3_HealthyCount + 1; END_IF;

IF nCh3_HealthyCount = 3 THEN
    rTempMin := MIN(rCh3_ValA, MIN(rCh3_ValB, rCh3_ValC));
    rTempMax := MAX(rCh3_ValA, MAX(rCh3_ValB, rCh3_ValC));
    rCh3_Voted := (rCh3_ValA + rCh3_ValB + rCh3_ValC) - rTempMin - rTempMax;
ELSIF nCh3_HealthyCount = 2 THEN
    bCh3_DegradedLatch := TRUE;
    IF bCh3_HealthA AND bCh3_HealthB THEN
        rCh3_Voted := (rCh3_ValA + rCh3_ValB) * 0.50;
    ELSIF bCh3_HealthB AND bCh3_HealthC THEN
        rCh3_Voted := (rCh3_ValB + rCh3_ValC) * 0.50;
    ELSE
        rCh3_Voted := (rCh3_ValA + rCh3_ValC) * 0.50;
    END_IF;
ELSIF nCh3_HealthyCount = 1 THEN
    bCh3_DegradedLatch := TRUE;
    IF bCh3_HealthA THEN rCh3_Voted := rCh3_ValA;
    ELSIF bCh3_HealthB THEN rCh3_Voted := rCh3_ValB;
    ELSE rCh3_Voted := rCh3_ValC; END_IF;
ELSE
    bCh3_TotalFailureLatch := TRUE;
    rCh3_Voted := rCh3_PrevVoted;
END_IF;
rCh3_PrevVoted := rCh3_Voted;
rVoted_TopGasMassFlow := rCh3_Voted;


(* ---------------------------------------------------------------------------------------------------- *)
(* 2oo3 TMR CHANNEL 4: GENERATOR ACTIVE ELECTRICAL POWER TRANSDUCERS WT-401 [MW]                         *)
(* Range Envelope: -2.0 to 32.0 MW. Discrepancy Tolerance: 1.2 MW.                                      *)
(* ---------------------------------------------------------------------------------------------------- *)
rCh4_ValA := rGeneratorPower_WT401A;
rCh4_ValB := rGeneratorPower_WT401B;
rCh4_ValC := rGeneratorPower_WT401C;

IF (rCh4_ValA < -5.0) OR (rCh4_ValA > 35.0) THEN bCh4_HealthA := FALSE; END_IF;
IF (rCh4_ValB < -5.0) OR (rCh4_ValB > 35.0) THEN bCh4_HealthB := FALSE; END_IF;
IF (rCh4_ValC < -5.0) OR (rCh4_ValC > 35.0) THEN bCh4_HealthC := FALSE; END_IF;

IF bCh4_HealthA AND bCh4_HealthB AND bCh4_HealthC THEN
    IF (ABS(rCh4_ValA - rCh4_ValB) > rTMR_TolPower) AND (ABS(rCh4_ValA - rCh4_ValC) > rTMR_TolPower) THEN
        nCh4_TimerA := nCh4_TimerA + 10;
        IF nCh4_TimerA >= nDiscrepancyTripDelay_ms THEN
            bCh4_HealthA := FALSE;
            bCh4_DegradedLatch := TRUE;
        END_IF;
    ELSE
        IF nCh4_TimerA > 0 THEN nCh4_TimerA := nCh4_TimerA - 10; END_IF;
    END_IF;

    IF (ABS(rCh4_ValB - rCh4_ValA) > rTMR_TolPower) AND (ABS(rCh4_ValB - rCh4_ValC) > rTMR_TolPower) THEN
        nCh4_TimerB := nCh4_TimerB + 10;
        IF nCh4_TimerB >= nDiscrepancyTripDelay_ms THEN
            bCh4_HealthB := FALSE;
            bCh4_DegradedLatch := TRUE;
        END_IF;
    ELSE
        IF nCh4_TimerB > 0 THEN nCh4_TimerB := nCh4_TimerB - 10; END_IF;
    END_IF;

    IF (ABS(rCh4_ValC - rCh4_ValA) > rTMR_TolPower) AND (ABS(rCh4_ValC - rCh4_ValB) > rTMR_TolPower) THEN
        nCh4_TimerC := nCh4_TimerC + 10;
        IF nCh4_TimerC >= nDiscrepancyTripDelay_ms THEN
            bCh4_HealthC := FALSE;
            bCh4_DegradedLatch := TRUE;
        END_IF;
    ELSE
        IF nCh4_TimerC > 0 THEN nCh4_TimerC := nCh4_TimerC - 10; END_IF;
    END_IF;
END_IF;

nCh4_HealthyCount := 0;
IF bCh4_HealthA THEN nCh4_HealthyCount := nCh4_HealthyCount + 1; END_IF;
IF bCh4_HealthB THEN nCh4_HealthyCount := nCh4_HealthyCount + 1; END_IF;
IF bCh4_HealthC THEN nCh4_HealthyCount := nCh4_HealthyCount + 1; END_IF;

IF nCh4_HealthyCount = 3 THEN
    rTempMin := MIN(rCh4_ValA, MIN(rCh4_ValB, rCh4_ValC));
    rTempMax := MAX(rCh4_ValA, MAX(rCh4_ValB, rCh4_ValC));
    rCh4_Voted := (rCh4_ValA + rCh4_ValB + rCh4_ValC) - rTempMin - rTempMax;
ELSIF nCh4_HealthyCount = 2 THEN
    bCh4_DegradedLatch := TRUE;
    IF bCh4_HealthA AND bCh4_HealthB THEN
        rCh4_Voted := (rCh4_ValA + rCh4_ValB) * 0.50;
    ELSIF bCh4_HealthB AND bCh4_HealthC THEN
        rCh4_Voted := (rCh4_ValB + rCh4_ValC) * 0.50;
    ELSE
        rCh4_Voted := (rCh4_ValA + rCh4_ValC) * 0.50;
    END_IF;
ELSIF nCh4_HealthyCount = 1 THEN
    bCh4_DegradedLatch := TRUE;
    IF bCh4_HealthA THEN rCh4_Voted := rCh4_ValA;
    ELSIF bCh4_HealthB THEN rCh4_Voted := rCh4_ValB;
    ELSE rCh4_Voted := rCh4_ValC; END_IF;
ELSE
    bCh4_TotalFailureLatch := TRUE;
    rCh4_Voted := rCh4_PrevVoted;
END_IF;
rCh4_PrevVoted := rCh4_Voted;
rVoted_GeneratorActivePower := rCh4_Voted;


(* ---------------------------------------------------------------------------------------------------- *)
(* 2oo3 TMR CHANNEL 5: TURBINE JOURNAL BEARING RADIAL VIBRATION VT-501 [um]                              *)
(* Range Envelope: 0.0 to 120.0 um. Discrepancy Tolerance: 5.0 um.                                       *)
(* ---------------------------------------------------------------------------------------------------- *)
rCh5_ValA := rTurbineVibration_VT501A;
rCh5_ValB := rTurbineVibration_VT501B;
rCh5_ValC := rTurbineVibration_VT501C;

IF (rCh5_ValA < 0.0) OR (rCh5_ValA > 150.0) THEN bCh5_HealthA := FALSE; END_IF;
IF (rCh5_ValB < 0.0) OR (rCh5_ValB > 150.0) THEN bCh5_HealthB := FALSE; END_IF;
IF (rCh5_ValC < 0.0) OR (rCh5_ValC > 150.0) THEN bCh5_HealthC := FALSE; END_IF;

IF bCh5_HealthA AND bCh5_HealthB AND bCh5_HealthC THEN
    IF (ABS(rCh5_ValA - rCh5_ValB) > rTMR_TolVib) AND (ABS(rCh5_ValA - rCh5_ValC) > rTMR_TolVib) THEN
        nCh5_TimerA := nCh5_TimerA + 10;
        IF nCh5_TimerA >= nDiscrepancyTripDelay_ms THEN
            bCh5_HealthA := FALSE;
            bCh5_DegradedLatch := TRUE;
        END_IF;
    ELSE
        IF nCh5_TimerA > 0 THEN nCh5_TimerA := nCh5_TimerA - 10; END_IF;
    END_IF;

    IF (ABS(rCh5_ValB - rCh5_ValA) > rTMR_TolVib) AND (ABS(rCh5_ValB - rCh5_ValC) > rTMR_TolVib) THEN
        nCh5_TimerB := nCh5_TimerB + 10;
        IF nCh5_TimerB >= nDiscrepancyTripDelay_ms THEN
            bCh5_HealthB := FALSE;
            bCh5_DegradedLatch := TRUE;
        END_IF;
    ELSE
        IF nCh5_TimerB > 0 THEN nCh5_TimerB := nCh5_TimerB - 10; END_IF;
    END_IF;

    IF (ABS(rCh5_ValC - rCh5_ValA) > rTMR_TolVib) AND (ABS(rCh5_ValC - rCh5_ValB) > rTMR_TolVib) THEN
        nCh5_TimerC := nCh5_TimerC + 10;
        IF nCh5_TimerC >= nDiscrepancyTripDelay_ms THEN
            bCh5_HealthC := FALSE;
            bCh5_DegradedLatch := TRUE;
        END_IF;
    ELSE
        IF nCh5_TimerC > 0 THEN nCh5_TimerC := nCh5_TimerC - 10; END_IF;
    END_IF;
END_IF;

nCh5_HealthyCount := 0;
IF bCh5_HealthA THEN nCh5_HealthyCount := nCh5_HealthyCount + 1; END_IF;
IF bCh5_HealthB THEN nCh5_HealthyCount := nCh5_HealthyCount + 1; END_IF;
IF bCh5_HealthC THEN nCh5_HealthyCount := nCh5_HealthyCount + 1; END_IF;

IF nCh5_HealthyCount = 3 THEN
    rTempMin := MIN(rCh5_ValA, MIN(rCh5_ValB, rCh5_ValC));
    rTempMax := MAX(rCh5_ValA, MAX(rCh5_ValB, rCh5_ValC));
    rCh5_Voted := (rCh5_ValA + rCh5_ValB + rCh5_ValC) - rTempMin - rTempMax;
ELSIF nCh5_HealthyCount = 2 THEN
    bCh5_DegradedLatch := TRUE;
    IF bCh5_HealthA AND bCh5_HealthB THEN
        rCh5_Voted := (rCh5_ValA + rCh5_ValB) * 0.50;
    ELSIF bCh5_HealthB AND bCh5_HealthC THEN
        rCh5_Voted := (rCh5_ValB + rCh5_ValC) * 0.50;
    ELSE
        rCh5_Voted := (rCh5_ValA + rCh5_ValC) * 0.50;
    END_IF;
ELSIF nCh5_HealthyCount = 1 THEN
    bCh5_DegradedLatch := TRUE;
    IF bCh5_HealthA THEN rCh5_Voted := rCh5_ValA;
    ELSIF bCh5_HealthB THEN rCh5_Voted := rCh5_ValB;
    ELSE rCh5_Voted := rCh5_ValC; END_IF;
ELSE
    bCh5_TotalFailureLatch := TRUE;
    rCh5_Voted := rCh5_PrevVoted;
END_IF;
rCh5_PrevVoted := rCh5_Voted;
rVoted_TurbineVibration := rCh5_Voted;


(* ---------------------------------------------------------------------------------------------------- *)
(* 2oo3 TMR CHANNEL 6: DRY BAG FILTER ARRAY DIFFERENTIAL PRESSURE DPT-601 [kPa]                          *)
(* Range Envelope: 0.5 to 15.0 kPa. Discrepancy Tolerance: 1.2 kPa.                                      *)
(* ---------------------------------------------------------------------------------------------------- *)
rCh6_ValA := rBagFilterDiffPress_DPT601A;
rCh6_ValB := rBagFilterDiffPress_DPT601B;
rCh6_ValC := rBagFilterDiffPress_DPT601C;

IF (rCh6_ValA < 0.2) OR (rCh6_ValA > 18.0) THEN bCh6_HealthA := FALSE; END_IF;
IF (rCh6_ValB < 0.2) OR (rCh6_ValB > 18.0) THEN bCh6_HealthB := FALSE; END_IF;
IF (rCh6_ValC < 0.2) OR (rCh6_ValC > 18.0) THEN bCh6_HealthC := FALSE; END_IF;

IF bCh6_HealthA AND bCh6_HealthB AND bCh6_HealthC THEN
    IF (ABS(rCh6_ValA - rCh6_ValB) > rTMR_TolDiffPress) AND (ABS(rCh6_ValA - rCh6_ValC) > rTMR_TolDiffPress) THEN
        nCh6_TimerA := nCh6_TimerA + 10;
        IF nCh6_TimerA >= nDiscrepancyTripDelay_ms THEN
            bCh6_HealthA := FALSE;
            bCh6_DegradedLatch := TRUE;
        END_IF;
    ELSE
        IF nCh6_TimerA > 0 THEN nCh6_TimerA := nCh6_TimerA - 10; END_IF;
    END_IF;

    IF (ABS(rCh6_ValB - rCh6_ValA) > rTMR_TolDiffPress) AND (ABS(rCh6_ValB - rCh6_ValC) > rTMR_TolDiffPress) THEN
        nCh6_TimerB := nCh6_TimerB + 10;
        IF nCh6_TimerB >= nDiscrepancyTripDelay_ms THEN
            bCh6_HealthB := FALSE;
            bCh6_DegradedLatch := TRUE;
        END_IF;
    ELSE
        IF nCh6_TimerB > 0 THEN nCh6_TimerB := nCh6_TimerB - 10; END_IF;
    END_IF;

    IF (ABS(rCh6_ValC - rCh6_ValA) > rTMR_TolDiffPress) AND (ABS(rCh6_ValC - rCh6_ValB) > rTMR_TolDiffPress) THEN
        nCh6_TimerC := nCh6_TimerC + 10;
        IF nCh6_TimerC >= nDiscrepancyTripDelay_ms THEN
            bCh6_HealthC := FALSE;
            bCh6_DegradedLatch := TRUE;
        END_IF;
    ELSE
        IF nCh6_TimerC > 0 THEN nCh6_TimerC := nCh6_TimerC - 10; END_IF;
    END_IF;
END_IF;

nCh6_HealthyCount := 0;
IF bCh6_HealthA THEN nCh6_HealthyCount := nCh6_HealthyCount + 1; END_IF;
IF bCh6_HealthB THEN nCh6_HealthyCount := nCh6_HealthyCount + 1; END_IF;
IF bCh6_HealthC THEN nCh6_HealthyCount := nCh6_HealthyCount + 1; END_IF;

IF nCh6_HealthyCount = 3 THEN
    rTempMin := MIN(rCh6_ValA, MIN(rCh6_ValB, rCh6_ValC));
    rTempMax := MAX(rCh6_ValA, MAX(rCh6_ValB, rCh6_ValC));
    rCh6_Voted := (rCh6_ValA + rCh6_ValB + rCh6_ValC) - rTempMin - rTempMax;
ELSIF nCh6_HealthyCount = 2 THEN
    bCh6_DegradedLatch := TRUE;
    IF bCh6_HealthA AND bCh6_HealthB THEN
        rCh6_Voted := (rCh6_ValA + rCh6_ValB) * 0.50;
    ELSIF bCh6_HealthB AND bCh6_HealthC THEN
        rCh6_Voted := (rCh6_ValB + rCh6_ValC) * 0.50;
    ELSE
        rCh6_Voted := (rCh6_ValA + rCh6_ValC) * 0.50;
    END_IF;
ELSIF nCh6_HealthyCount = 1 THEN
    bCh6_DegradedLatch := TRUE;
    IF bCh6_HealthA THEN rCh6_Voted := rCh6_ValA;
    ELSIF bCh6_HealthB THEN rCh6_Voted := rCh6_ValB;
    ELSE rCh6_Voted := rCh6_ValC; END_IF;
ELSE
    bCh6_TotalFailureLatch := TRUE;
    rCh6_Voted := rCh6_PrevVoted;
END_IF;
rCh6_PrevVoted := rCh6_Voted;
rVoted_BagFilterDiffPress := rCh6_Voted;


(* ---------------------------------------------------------------------------------------------------- *)
(* DUAL REDUNDANT TURBINE ROTOR SPEED SENSORS ST-101A/B [rpm]                                           *)
(* Discrepancy Tolerance: 45.0 rpm. High-Speed Rate Validation.                                          *)
(* ---------------------------------------------------------------------------------------------------- *)
rSpeed_RawA := rTurbineSpeed_ST101A;
rSpeed_RawB := rTurbineSpeed_ST101B;

IF (rSpeed_RawA < 0.0) OR (rSpeed_RawA > 3800.0) THEN bSpeed_SensorA_Healthy := FALSE; END_IF;
IF (rSpeed_RawB < 0.0) OR (rSpeed_RawB > 3800.0) THEN bSpeed_SensorB_Healthy := FALSE; END_IF;

IF bSpeed_SensorA_Healthy AND bSpeed_SensorB_Healthy THEN
    IF ABS(rSpeed_RawA - rSpeed_RawB) > rTMR_TolSpeed THEN
        nSpeed_DiscrepancyTimer_ms := nSpeed_DiscrepancyTimer_ms + 10;
        IF nSpeed_DiscrepancyTimer_ms >= 500 THEN
            (* Conservative Selection: Select Highest Speed for Overspeed Protection *)
            rSpeed_Voted := MAX(rSpeed_RawA, rSpeed_RawB);
        ELSE
            rSpeed_Voted := (rSpeed_RawA + rSpeed_RawB) * 0.50;
        END_IF;
    ELSE
        IF nSpeed_DiscrepancyTimer_ms > 0 THEN
            nSpeed_DiscrepancyTimer_ms := nSpeed_DiscrepancyTimer_ms - 10;
        END_IF;
        rSpeed_Voted := (rSpeed_RawA + rSpeed_RawB) * 0.50;
    END_IF;
ELSIF bSpeed_SensorA_Healthy THEN
    rSpeed_Voted := rSpeed_RawA;
ELSIF bSpeed_SensorB_Healthy THEN
    rSpeed_Voted := rSpeed_RawB;
ELSE
    rSpeed_Voted := rSpeed_Prev;
END_IF;

rSpeed_ROC := (rSpeed_Voted - rSpeed_Prev) / rSamplingTime_s;
rSpeed_Prev := rSpeed_Voted;
rTurbineSpeed_Filtered := rSpeed_Voted;
"""
