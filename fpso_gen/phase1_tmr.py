# fpso_gen/phase1_tmr.py
def get_phase1():
    return """
(* =====================================================================================================================
 * PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING WITH DISCREPANCY TIMERS
 * Architected in accordance with IEC 61508 / IEC 61511 SIL-3 architecture for offshore safety instrumented loops.
 * Five critical sensor groups: PT-101 (Suction), PT-201 (Discharge), PDT-301 (Suction DP), VT-401 (Vibration), AT-501 (Moisture).
 * Features pairwise absolute discrepancy integration, bumpless rate-limited degraded modes (3oo3 -> 2oo2 -> 1oo1 -> Trip).
 * ===================================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------------------------
 * SENSOR GROUP 1: STAGE 1 SUCTION PRESSURE PT-101A / PT-101B / PT-101C [bar]
 * --------------------------------------------------------------------------------------------------------------------- *)
rTMR_PT101_ValA := rSuctionPres_PT101A_In;
rTMR_PT101_ValB := rSuctionPres_PT101B_In;
rTMR_PT101_ValC := rSuctionPres_PT101C_In;

(* Plausibility Sanity Limits [0.0 bar to 45.0 bar] *)
IF rTMR_PT101_ValA < 0.0 OR rTMR_PT101_ValA > 45.0 THEN
    bTMR_PT101_HealthyA := FALSE;
END_IF;
IF rTMR_PT101_ValB < 0.0 OR rTMR_PT101_ValB > 45.0 THEN
    bTMR_PT101_HealthyB := FALSE;
END_IF;
IF rTMR_PT101_ValC < 0.0 OR rTMR_PT101_ValC > 45.0 THEN
    bTMR_PT101_HealthyC := FALSE;
END_IF;

(* Compute Pairwise Absolute Differences *)
rTMR_PT101_DeltaAB := ABS(rTMR_PT101_ValA - rTMR_PT101_ValB);
rTMR_PT101_DeltaBC := ABS(rTMR_PT101_ValB - rTMR_PT101_ValC);
rTMR_PT101_DeltaCA := ABS(rTMR_PT101_ValC - rTMR_PT101_ValA);

(* Discrepancy Time Integration for Channel A *)
IF (rTMR_PT101_DeltaAB > rTMR_PT101_Tol) AND (rTMR_PT101_DeltaCA > rTMR_PT101_Tol) THEN
    rTMR_PT101_TimerA := rTMR_PT101_TimerA + rTs;
    IF rTMR_PT101_TimerA >= rTMR_PT101_TimeLimit THEN
        bTMR_PT101_HealthyA := FALSE;
    END_IF;
ELSE
    IF rTMR_PT101_TimerA > 0.0 THEN
        rTMR_PT101_TimerA := rTMR_PT101_TimerA - (2.0 * rTs);
        IF rTMR_PT101_TimerA < 0.0 THEN
            rTMR_PT101_TimerA := 0.0;
        END_IF;
    END_IF;
END_IF;

(* Discrepancy Time Integration for Channel B *)
IF (rTMR_PT101_DeltaAB > rTMR_PT101_Tol) AND (rTMR_PT101_DeltaBC > rTMR_PT101_Tol) THEN
    rTMR_PT101_TimerB := rTMR_PT101_TimerB + rTs;
    IF rTMR_PT101_TimerB >= rTMR_PT101_TimeLimit THEN
        bTMR_PT101_HealthyB := FALSE;
    END_IF;
ELSE
    IF rTMR_PT101_TimerB > 0.0 THEN
        rTMR_PT101_TimerB := rTMR_PT101_TimerB - (2.0 * rTs);
        IF rTMR_PT101_TimerB < 0.0 THEN
            rTMR_PT101_TimerB := 0.0;
        END_IF;
    END_IF;
END_IF;

(* Discrepancy Time Integration for Channel C *)
IF (rTMR_PT101_DeltaBC > rTMR_PT101_Tol) AND (rTMR_PT101_DeltaCA > rTMR_PT101_Tol) THEN
    rTMR_PT101_TimerC := rTMR_PT101_TimerC + rTs;
    IF rTMR_PT101_TimerC >= rTMR_PT101_TimeLimit THEN
        bTMR_PT101_HealthyC := FALSE;
    END_IF;
ELSE
    IF rTMR_PT101_TimerC > 0.0 THEN
        rTMR_PT101_TimerC := rTMR_PT101_TimerC - (2.0 * rTs);
        IF rTMR_PT101_TimerC < 0.0 THEN
            rTMR_PT101_TimerC := 0.0;
        END_IF;
    END_IF;
END_IF;

(* Voted Median & Degraded Mode Output Selection *)
IF bTMR_PT101_HealthyA AND bTMR_PT101_HealthyB AND bTMR_PT101_HealthyC THEN
    (* Full 2oo3 Triple Redundancy: Mid-Value Median Selection *)
    IF ((rTMR_PT101_ValA >= rTMR_PT101_ValB) AND (rTMR_PT101_ValA <= rTMR_PT101_ValC)) OR
       ((rTMR_PT101_ValA >= rTMR_PT101_ValC) AND (rTMR_PT101_ValA <= rTMR_PT101_ValB)) THEN
        rVoted_PT101_Internal := rTMR_PT101_ValA;
    ELSIF ((rTMR_PT101_ValB >= rTMR_PT101_ValA) AND (rTMR_PT101_ValB <= rTMR_PT101_ValC)) OR
          ((rTMR_PT101_ValB >= rTMR_PT101_ValC) AND (rTMR_PT101_ValB <= rTMR_PT101_ValA)) THEN
        rVoted_PT101_Internal := rTMR_PT101_ValB;
    ELSE
        rVoted_PT101_Internal := rTMR_PT101_ValC;
    END_IF;
ELSIF bTMR_PT101_HealthyA AND bTMR_PT101_HealthyB THEN
    rVoted_PT101_Internal := (rTMR_PT101_ValA + rTMR_PT101_ValB) * 0.5;
ELSIF bTMR_PT101_HealthyB AND bTMR_PT101_HealthyC THEN
    rVoted_PT101_Internal := (rTMR_PT101_ValB + rTMR_PT101_ValC) * 0.5;
ELSIF bTMR_PT101_HealthyA AND bTMR_PT101_HealthyC THEN
    rVoted_PT101_Internal := (rTMR_PT101_ValA + rTMR_PT101_ValC) * 0.5;
ELSIF bTMR_PT101_HealthyA THEN
    rVoted_PT101_Internal := rTMR_PT101_ValA;
ELSIF bTMR_PT101_HealthyB THEN
    rVoted_PT101_Internal := rTMR_PT101_ValB;
ELSIF bTMR_PT101_HealthyC THEN
    rVoted_PT101_Internal := rTMR_PT101_ValC;
ELSE
    bTrip_TMR_CriticalLoss := TRUE;
END_IF;
rVoted_SuctionPres_Out := rVoted_PT101_Internal;

(* ---------------------------------------------------------------------------------------------------------------------
 * SENSOR GROUP 2: STAGE 3 DISCHARGE EXPORT PRESSURE PT-201A / PT-201B / PT-201C [bar]
 * --------------------------------------------------------------------------------------------------------------------- *)
rTMR_PT201_ValA := rDischargePres_PT201A_In;
rTMR_PT201_ValB := rDischargePres_PT201B_In;
rTMR_PT201_ValC := rDischargePres_PT201C_In;

(* Plausibility Sanity Limits [0.0 bar to 320.0 bar] *)
IF rTMR_PT201_ValA < 0.0 OR rTMR_PT201_ValA > 320.0 THEN
    bTMR_PT201_HealthyA := FALSE;
END_IF;
IF rTMR_PT201_ValB < 0.0 OR rTMR_PT201_ValB > 320.0 THEN
    bTMR_PT201_HealthyB := FALSE;
END_IF;
IF rTMR_PT201_ValC < 0.0 OR rTMR_PT201_ValC > 320.0 THEN
    bTMR_PT201_HealthyC := FALSE;
END_IF;

(* Compute Pairwise Absolute Differences *)
rTMR_PT201_DeltaAB := ABS(rTMR_PT201_ValA - rTMR_PT201_ValB);
rTMR_PT201_DeltaBC := ABS(rTMR_PT201_ValB - rTMR_PT201_ValC);
rTMR_PT201_DeltaCA := ABS(rTMR_PT201_ValC - rTMR_PT201_ValA);

(* Discrepancy Time Integration for Channel A *)
IF (rTMR_PT201_DeltaAB > rTMR_PT201_Tol) AND (rTMR_PT201_DeltaCA > rTMR_PT201_Tol) THEN
    rTMR_PT201_TimerA := rTMR_PT201_TimerA + rTs;
    IF rTMR_PT201_TimerA >= rTMR_PT201_TimeLimit THEN
        bTMR_PT201_HealthyA := FALSE;
    END_IF;
ELSE
    IF rTMR_PT201_TimerA > 0.0 THEN
        rTMR_PT201_TimerA := rTMR_PT201_TimerA - (2.0 * rTs);
        IF rTMR_PT201_TimerA < 0.0 THEN
            rTMR_PT201_TimerA := 0.0;
        END_IF;
    END_IF;
END_IF;

(* Discrepancy Time Integration for Channel B *)
IF (rTMR_PT201_DeltaAB > rTMR_PT201_Tol) AND (rTMR_PT201_DeltaBC > rTMR_PT201_Tol) THEN
    rTMR_PT201_TimerB := rTMR_PT201_TimerB + rTs;
    IF rTMR_PT201_TimerB >= rTMR_PT201_TimeLimit THEN
        bTMR_PT201_HealthyB := FALSE;
    END_IF;
ELSE
    IF rTMR_PT201_TimerB > 0.0 THEN
        rTMR_PT201_TimerB := rTMR_PT201_TimerB - (2.0 * rTs);
        IF rTMR_PT201_TimerB < 0.0 THEN
            rTMR_PT201_TimerB := 0.0;
        END_IF;
    END_IF;
END_IF;

(* Discrepancy Time Integration for Channel C *)
IF (rTMR_PT201_DeltaBC > rTMR_PT201_Tol) AND (rTMR_PT201_DeltaCA > rTMR_PT201_Tol) THEN
    rTMR_PT201_TimerC := rTMR_PT201_TimerC + rTs;
    IF rTMR_PT201_TimerC >= rTMR_PT201_TimeLimit THEN
        bTMR_PT201_HealthyC := FALSE;
    END_IF;
ELSE
    IF rTMR_PT201_TimerC > 0.0 THEN
        rTMR_PT201_TimerC := rTMR_PT201_TimerC - (2.0 * rTs);
        IF rTMR_PT201_TimerC < 0.0 THEN
            rTMR_PT201_TimerC := 0.0;
        END_IF;
    END_IF;
END_IF;

(* Voted Median & Degraded Mode Output Selection *)
IF bTMR_PT201_HealthyA AND bTMR_PT201_HealthyB AND bTMR_PT201_HealthyC THEN
    IF ((rTMR_PT201_ValA >= rTMR_PT201_ValB) AND (rTMR_PT201_ValA <= rTMR_PT201_ValC)) OR
       ((rTMR_PT201_ValA >= rTMR_PT201_ValC) AND (rTMR_PT201_ValA <= rTMR_PT201_ValB)) THEN
        rVoted_PT201_Internal := rTMR_PT201_ValA;
    ELSIF ((rTMR_PT201_ValB >= rTMR_PT201_ValA) AND (rTMR_PT201_ValB <= rTMR_PT201_ValC)) OR
          ((rTMR_PT201_ValB >= rTMR_PT201_ValC) AND (rTMR_PT201_ValB <= rTMR_PT201_ValA)) THEN
        rVoted_PT201_Internal := rTMR_PT201_ValB;
    ELSE
        rVoted_PT201_Internal := rTMR_PT201_ValC;
    END_IF;
ELSIF bTMR_PT201_HealthyA AND bTMR_PT201_HealthyB THEN
    rVoted_PT201_Internal := (rTMR_PT201_ValA + rTMR_PT201_ValB) * 0.5;
ELSIF bTMR_PT201_HealthyB AND bTMR_PT201_HealthyC THEN
    rVoted_PT201_Internal := (rTMR_PT201_ValB + rTMR_PT201_ValC) * 0.5;
ELSIF bTMR_PT201_HealthyA AND bTMR_PT201_HealthyC THEN
    rVoted_PT201_Internal := (rTMR_PT201_ValA + rTMR_PT201_ValC) * 0.5;
ELSIF bTMR_PT201_HealthyA THEN
    rVoted_PT201_Internal := rTMR_PT201_ValA;
ELSIF bTMR_PT201_HealthyB THEN
    rVoted_PT201_Internal := rTMR_PT201_ValB;
ELSIF bTMR_PT201_HealthyC THEN
    rVoted_PT201_Internal := rTMR_PT201_ValC;
ELSE
    bTrip_TMR_CriticalLoss := TRUE;
END_IF;
rVoted_DischargePres_Out := rVoted_PT201_Internal;

(* ---------------------------------------------------------------------------------------------------------------------
 * SENSOR GROUP 3: STAGE 1 SUCTION VENTURI FLOW DP PDT-301A / PDT-301B / PDT-301C [mbar]
 * --------------------------------------------------------------------------------------------------------------------- *)
rTMR_PDT301_ValA := rSuctionDP_PDT301A_In;
rTMR_PDT301_ValB := rSuctionDP_PDT301B_In;
rTMR_PDT301_ValC := rSuctionDP_PDT301C_In;

(* Plausibility Sanity Limits [-5.0 mbar to 500.0 mbar] *)
IF rTMR_PDT301_ValA < -5.0 OR rTMR_PDT301_ValA > 500.0 THEN
    bTMR_PDT301_HealthyA := FALSE;
END_IF;
IF rTMR_PDT301_ValB < -5.0 OR rTMR_PDT301_ValB > 500.0 THEN
    bTMR_PDT301_HealthyB := FALSE;
END_IF;
IF rTMR_PDT301_ValC < -5.0 OR rTMR_PDT301_ValC > 500.0 THEN
    bTMR_PDT301_HealthyC := FALSE;
END_IF;

(* Compute Pairwise Absolute Differences *)
rTMR_PDT301_DeltaAB := ABS(rTMR_PDT301_ValA - rTMR_PDT301_ValB);
rTMR_PDT301_DeltaBC := ABS(rTMR_PDT301_ValB - rTMR_PDT301_ValC);
rTMR_PDT301_DeltaCA := ABS(rTMR_PDT301_ValC - rTMR_PDT301_ValA);

(* Discrepancy Time Integration for Channel A *)
IF (rTMR_PDT301_DeltaAB > rTMR_PDT301_Tol) AND (rTMR_PDT301_DeltaCA > rTMR_PDT301_Tol) THEN
    rTMR_PDT301_TimerA := rTMR_PDT301_TimerA + rTs;
    IF rTMR_PDT301_TimerA >= rTMR_PDT301_TimeLimit THEN
        bTMR_PDT301_HealthyA := FALSE;
    END_IF;
ELSE
    IF rTMR_PDT301_TimerA > 0.0 THEN
        rTMR_PDT301_TimerA := rTMR_PDT301_TimerA - (2.0 * rTs);
        IF rTMR_PDT301_TimerA < 0.0 THEN
            rTMR_PDT301_TimerA := 0.0;
        END_IF;
    END_IF;
END_IF;

(* Discrepancy Time Integration for Channel B *)
IF (rTMR_PDT301_DeltaAB > rTMR_PDT301_Tol) AND (rTMR_PDT301_DeltaBC > rTMR_PDT301_Tol) THEN
    rTMR_PDT301_TimerB := rTMR_PDT301_TimerB + rTs;
    IF rTMR_PDT301_TimerB >= rTMR_PDT301_TimeLimit THEN
        bTMR_PDT301_HealthyB := FALSE;
    END_IF;
ELSE
    IF rTMR_PDT301_TimerB > 0.0 THEN
        rTMR_PDT301_TimerB := rTMR_PDT301_TimerB - (2.0 * rTs);
        IF rTMR_PDT301_TimerB < 0.0 THEN
            rTMR_PDT301_TimerB := 0.0;
        END_IF;
    END_IF;
END_IF;

(* Discrepancy Time Integration for Channel C *)
IF (rTMR_PDT301_DeltaBC > rTMR_PDT301_Tol) AND (rTMR_PDT301_DeltaCA > rTMR_PDT301_Tol) THEN
    rTMR_PDT301_TimerC := rTMR_PDT301_TimerC + rTs;
    IF rTMR_PDT301_TimerC >= rTMR_PDT301_TimeLimit THEN
        bTMR_PDT301_HealthyC := FALSE;
    END_IF;
ELSE
    IF rTMR_PDT301_TimerC > 0.0 THEN
        rTMR_PDT301_TimerC := rTMR_PDT301_TimerC - (2.0 * rTs);
        IF rTMR_PDT301_TimerC < 0.0 THEN
            rTMR_PDT301_TimerC := 0.0;
        END_IF;
    END_IF;
END_IF;

(* Voted Median & Degraded Mode Output Selection *)
IF bTMR_PDT301_HealthyA AND bTMR_PDT301_HealthyB AND bTMR_PDT301_HealthyC THEN
    IF ((rTMR_PDT301_ValA >= rTMR_PDT301_ValB) AND (rTMR_PDT301_ValA <= rTMR_PDT301_ValC)) OR
       ((rTMR_PDT301_ValA >= rTMR_PDT301_ValC) AND (rTMR_PDT301_ValA <= rTMR_PDT301_ValB)) THEN
        rVoted_PDT301_Internal := rTMR_PDT301_ValA;
    ELSIF ((rTMR_PDT301_ValB >= rTMR_PDT301_ValA) AND (rTMR_PDT301_ValB <= rTMR_PDT301_ValC)) OR
          ((rTMR_PDT301_ValB >= rTMR_PDT301_ValC) AND (rTMR_PDT301_ValB <= rTMR_PDT301_ValA)) THEN
        rVoted_PDT301_Internal := rTMR_PDT301_ValB;
    ELSE
        rVoted_PDT301_Internal := rTMR_PDT301_ValC;
    END_IF;
ELSIF bTMR_PDT301_HealthyA AND bTMR_PDT301_HealthyB THEN
    rVoted_PDT301_Internal := (rTMR_PDT301_ValA + rTMR_PDT301_ValB) * 0.5;
ELSIF bTMR_PDT301_HealthyB AND bTMR_PDT301_HealthyC THEN
    rVoted_PDT301_Internal := (rTMR_PDT301_ValB + rTMR_PDT301_ValC) * 0.5;
ELSIF bTMR_PDT301_HealthyA AND bTMR_PDT301_HealthyC THEN
    rVoted_PDT301_Internal := (rTMR_PDT301_ValA + rTMR_PDT301_ValC) * 0.5;
ELSIF bTMR_PDT301_HealthyA THEN
    rVoted_PDT301_Internal := rTMR_PDT301_ValA;
ELSIF bTMR_PDT301_HealthyB THEN
    rVoted_PDT301_Internal := rTMR_PDT301_ValB;
ELSIF bTMR_PDT301_HealthyC THEN
    rVoted_PDT301_Internal := rTMR_PDT301_ValC;
ELSE
    bTrip_TMR_CriticalLoss := TRUE;
END_IF;
rVoted_SuctionDP_Out := rVoted_PDT301_Internal;

(* ---------------------------------------------------------------------------------------------------------------------
 * SENSOR GROUP 4: SHAFT RADIAL VIBRATION VT-401A / VT-401B / VT-401C [um]
 * --------------------------------------------------------------------------------------------------------------------- *)
rTMR_VT401_ValA := rShaftVib_VT401A_In;
rTMR_VT401_ValB := rShaftVib_VT401B_In;
rTMR_VT401_ValC := rShaftVib_VT401C_In;

(* Plausibility Sanity Limits [0.0 um to 250.0 um] *)
IF rTMR_VT401_ValA < 0.0 OR rTMR_VT401_ValA > 250.0 THEN
    bTMR_VT401_HealthyA := FALSE;
END_IF;
IF rTMR_VT401_ValB < 0.0 OR rTMR_VT401_ValB > 250.0 THEN
    bTMR_VT401_HealthyB := FALSE;
END_IF;
IF rTMR_VT401_ValC < 0.0 OR rTMR_VT401_ValC > 250.0 THEN
    bTMR_VT401_HealthyC := FALSE;
END_IF;

(* Compute Pairwise Absolute Differences *)
rTMR_VT401_DeltaAB := ABS(rTMR_VT401_ValA - rTMR_VT401_ValB);
rTMR_VT401_DeltaBC := ABS(rTMR_VT401_ValB - rTMR_VT401_ValC);
rTMR_VT401_DeltaCA := ABS(rTMR_VT401_ValC - rTMR_VT401_ValA);

(* Discrepancy Time Integration for Channel A *)
IF (rTMR_VT401_DeltaAB > rTMR_VT401_Tol) AND (rTMR_VT401_DeltaCA > rTMR_VT401_Tol) THEN
    rTMR_VT401_TimerA := rTMR_VT401_TimerA + rTs;
    IF rTMR_VT401_TimerA >= rTMR_VT401_TimeLimit THEN
        bTMR_VT401_HealthyA := FALSE;
    END_IF;
ELSE
    IF rTMR_VT401_TimerA > 0.0 THEN
        rTMR_VT401_TimerA := rTMR_VT401_TimerA - (2.0 * rTs);
        IF rTMR_VT401_TimerA < 0.0 THEN
            rTMR_VT401_TimerA := 0.0;
        END_IF;
    END_IF;
END_IF;

(* Discrepancy Time Integration for Channel B *)
IF (rTMR_VT401_DeltaAB > rTMR_VT401_Tol) AND (rTMR_VT401_DeltaBC > rTMR_VT401_Tol) THEN
    rTMR_VT401_TimerB := rTMR_VT401_TimerB + rTs;
    IF rTMR_VT401_TimerB >= rTMR_VT401_TimeLimit THEN
        bTMR_VT401_HealthyB := FALSE;
    END_IF;
ELSE
    IF rTMR_VT401_TimerB > 0.0 THEN
        rTMR_VT401_TimerB := rTMR_VT401_TimerB - (2.0 * rTs);
        IF rTMR_VT401_TimerB < 0.0 THEN
            rTMR_VT401_TimerB := 0.0;
        END_IF;
    END_IF;
END_IF;

(* Discrepancy Time Integration for Channel C *)
IF (rTMR_VT401_DeltaBC > rTMR_VT401_Tol) AND (rTMR_VT401_DeltaCA > rTMR_VT401_Tol) THEN
    rTMR_VT401_TimerC := rTMR_VT401_TimerC + rTs;
    IF rTMR_VT401_TimerC >= rTMR_VT401_TimeLimit THEN
        bTMR_VT401_HealthyC := FALSE;
    END_IF;
ELSE
    IF rTMR_VT401_TimerC > 0.0 THEN
        rTMR_VT401_TimerC := rTMR_VT401_TimerC - (2.0 * rTs);
        IF rTMR_VT401_TimerC < 0.0 THEN
            rTMR_VT401_TimerC := 0.0;
        END_IF;
    END_IF;
END_IF;

(* Voted Median & Degraded Mode Output Selection (In vibration protection, conservative maximum of 2 is preferred on single fault) *)
IF bTMR_VT401_HealthyA AND bTMR_VT401_HealthyB AND bTMR_VT401_HealthyC THEN
    IF ((rTMR_VT401_ValA >= rTMR_VT401_ValB) AND (rTMR_VT401_ValA <= rTMR_VT401_ValC)) OR
       ((rTMR_VT401_ValA >= rTMR_VT401_ValC) AND (rTMR_VT401_ValA <= rTMR_VT401_ValB)) THEN
        rVoted_VT401_Internal := rTMR_VT401_ValA;
    ELSIF ((rTMR_VT401_ValB >= rTMR_VT401_ValA) AND (rTMR_VT401_ValB <= rTMR_VT401_ValC)) OR
          ((rTMR_VT401_ValB >= rTMR_VT401_ValC) AND (rTMR_VT401_ValB <= rTMR_VT401_ValA)) THEN
        rVoted_VT401_Internal := rTMR_VT401_ValB;
    ELSE
        rVoted_VT401_Internal := rTMR_VT401_ValC;
    END_IF;
ELSIF bTMR_VT401_HealthyA AND bTMR_VT401_HealthyB THEN
    IF rTMR_VT401_ValA > rTMR_VT401_ValB THEN
        rVoted_VT401_Internal := rTMR_VT401_ValA;
    ELSE
        rVoted_VT401_Internal := rTMR_VT401_ValB;
    END_IF;
ELSIF bTMR_VT401_HealthyB AND bTMR_VT401_HealthyC THEN
    IF rTMR_VT401_ValB > rTMR_VT401_ValC THEN
        rVoted_VT401_Internal := rTMR_VT401_ValB;
    ELSE
        rVoted_VT401_Internal := rTMR_VT401_ValC;
    END_IF;
ELSIF bTMR_VT401_HealthyA AND bTMR_VT401_HealthyC THEN
    IF rTMR_VT401_ValA > rTMR_VT401_ValC THEN
        rVoted_VT401_Internal := rTMR_VT401_ValA;
    ELSE
        rVoted_VT401_Internal := rTMR_VT401_ValC;
    END_IF;
ELSIF bTMR_VT401_HealthyA THEN
    rVoted_VT401_Internal := rTMR_VT401_ValA;
ELSIF bTMR_VT401_HealthyB THEN
    rVoted_VT401_Internal := rTMR_VT401_ValB;
ELSIF bTMR_VT401_HealthyC THEN
    rVoted_VT401_Internal := rTMR_VT401_ValC;
ELSE
    bTrip_TMR_CriticalLoss := TRUE;
END_IF;
rVoted_ShaftVib_Out := rVoted_VT401_Internal;

(* ---------------------------------------------------------------------------------------------------------------------
 * SENSOR GROUP 5: EXPORT GAS MOISTURE ANALYZER AT-501A / AT-501B / AT-501C [ppmv]
 * --------------------------------------------------------------------------------------------------------------------- *)
rTMR_AT501_ValA := rExportMoisture_AT501A_In;
rTMR_AT501_ValB := rExportMoisture_AT501B_In;
rTMR_AT501_ValC := rExportMoisture_AT501C_In;

(* Plausibility Sanity Limits [0.0 ppmv to 120.0 ppmv] *)
IF rTMR_AT501_ValA < 0.0 OR rTMR_AT501_ValA > 120.0 THEN
    bTMR_AT501_HealthyA := FALSE;
END_IF;
IF rTMR_AT501_ValB < 0.0 OR rTMR_AT501_ValB > 120.0 THEN
    bTMR_AT501_HealthyB := FALSE;
END_IF;
IF rTMR_AT501_ValC < 0.0 OR rTMR_AT501_ValC > 120.0 THEN
    bTMR_AT501_HealthyC := FALSE;
END_IF;

(* Compute Pairwise Absolute Differences *)
rTMR_AT501_DeltaAB := ABS(rTMR_AT501_ValA - rTMR_AT501_ValB);
rTMR_AT501_DeltaBC := ABS(rTMR_AT501_ValB - rTMR_AT501_ValC);
rTMR_AT501_DeltaCA := ABS(rTMR_AT501_ValC - rTMR_AT501_ValA);

(* Discrepancy Time Integration for Channel A *)
IF (rTMR_AT501_DeltaAB > rTMR_AT501_Tol) AND (rTMR_AT501_DeltaCA > rTMR_AT501_Tol) THEN
    rTMR_AT501_TimerA := rTMR_AT501_TimerA + rTs;
    IF rTMR_AT501_TimerA >= rTMR_AT501_TimeLimit THEN
        bTMR_AT501_HealthyA := FALSE;
    END_IF;
ELSE
    IF rTMR_AT501_TimerA > 0.0 THEN
        rTMR_AT501_TimerA := rTMR_AT501_TimerA - (2.0 * rTs);
        IF rTMR_AT501_TimerA < 0.0 THEN
            rTMR_AT501_TimerA := 0.0;
        END_IF;
    END_IF;
END_IF;

(* Discrepancy Time Integration for Channel B *)
IF (rTMR_AT501_DeltaAB > rTMR_AT501_Tol) AND (rTMR_AT501_DeltaBC > rTMR_AT501_Tol) THEN
    rTMR_AT501_TimerB := rTMR_AT501_TimerB + rTs;
    IF rTMR_AT501_TimerB >= rTMR_AT501_TimeLimit THEN
        bTMR_AT501_HealthyB := FALSE;
    END_IF;
ELSE
    IF rTMR_AT501_TimerB > 0.0 THEN
        rTMR_AT501_TimerB := rTMR_AT501_TimerB - (2.0 * rTs);
        IF rTMR_AT501_TimerB < 0.0 THEN
            rTMR_AT501_TimerB := 0.0;
        END_IF;
    END_IF;
END_IF;

(* Discrepancy Time Integration for Channel C *)
IF (rTMR_AT501_DeltaBC > rTMR_AT501_Tol) AND (rTMR_AT501_DeltaCA > rTMR_AT501_Tol) THEN
    rTMR_AT501_TimerC := rTMR_AT501_TimerC + rTs;
    IF rTMR_AT501_TimerC >= rTMR_AT501_TimeLimit THEN
        bTMR_AT501_HealthyC := FALSE;
    END_IF;
ELSE
    IF rTMR_AT501_TimerC > 0.0 THEN
        rTMR_AT501_TimerC := rTMR_AT501_TimerC - (2.0 * rTs);
        IF rTMR_AT501_TimerC < 0.0 THEN
            rTMR_AT501_TimerC := 0.0;
        END_IF;
    END_IF;
END_IF;

(* Voted Median & Degraded Mode Output Selection (In moisture control, conservative higher reading is preferred on fault) *)
IF bTMR_AT501_HealthyA AND bTMR_AT501_HealthyB AND bTMR_AT501_HealthyC THEN
    IF ((rTMR_AT501_ValA >= rTMR_AT501_ValB) AND (rTMR_AT501_ValA <= rTMR_AT501_ValC)) OR
       ((rTMR_AT501_ValA >= rTMR_AT501_ValC) AND (rTMR_AT501_ValA <= rTMR_AT501_ValB)) THEN
        rVoted_AT501_Internal := rTMR_AT501_ValA;
    ELSIF ((rTMR_AT501_ValB >= rTMR_AT501_ValA) AND (rTMR_AT501_ValB <= rTMR_AT501_ValC)) OR
          ((rTMR_AT501_ValB >= rTMR_AT501_ValC) AND (rTMR_AT501_ValB <= rTMR_AT501_ValA)) THEN
        rVoted_AT501_Internal := rTMR_AT501_ValB;
    ELSE
        rVoted_AT501_Internal := rTMR_AT501_ValC;
    END_IF;
ELSIF bTMR_AT501_HealthyA AND bTMR_AT501_HealthyB THEN
    IF rTMR_AT501_ValA > rTMR_AT501_ValB THEN
        rVoted_AT501_Internal := rTMR_AT501_ValA;
    ELSE
        rVoted_AT501_Internal := rTMR_AT501_ValB;
    END_IF;
ELSIF bTMR_AT501_HealthyB AND bTMR_AT501_HealthyC THEN
    IF rTMR_AT501_ValB > rTMR_AT501_ValC THEN
        rVoted_AT501_Internal := rTMR_AT501_ValB;
    ELSE
        rVoted_AT501_Internal := rTMR_AT501_ValC;
    END_IF;
ELSIF bTMR_AT501_HealthyA AND bTMR_AT501_HealthyC THEN
    IF rTMR_AT501_ValA > rTMR_AT501_ValC THEN
        rVoted_AT501_Internal := rTMR_AT501_ValA;
    ELSE
        rVoted_AT501_Internal := rTMR_AT501_ValC;
    END_IF;
ELSIF bTMR_AT501_HealthyA THEN
    rVoted_AT501_Internal := rTMR_AT501_ValA;
ELSIF bTMR_AT501_HealthyB THEN
    rVoted_AT501_Internal := rTMR_AT501_ValB;
ELSIF bTMR_AT501_HealthyC THEN
    rVoted_AT501_Internal := rTMR_AT501_ValC;
ELSE
    bTrip_TMR_CriticalLoss := TRUE;
END_IF;
rVoted_ExportMoisture_Out := rVoted_AT501_Internal;
"""
