# lyophilizer_builder/build_st_phase1_tmr.py

def get_phase1_tmr():
    return """(* === PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING SUITE === *)
(* ---------------------------------------------------------------------------------------------------- *)
(* SENSOR BANK 1: CHAMBER PIRANI VACUUM GAUGES (PT-101A / PT-101B / PT-101C) [mbar]                    *)
(* ---------------------------------------------------------------------------------------------------- *)
rDeltaAB := ABS(rChamberPirani_A - rChamberPirani_B);
rDeltaBC := ABS(rChamberPirani_B - rChamberPirani_C);
rDeltaCA := ABS(rChamberPirani_C - rChamberPirani_A);

(* Pairwise Discrepancy Debounce Timers *)
IF rDeltaAB > rToler_Pirani_mbar THEN
    tPiraniDiscTimer_AB := tPiraniDiscTimer_AB + tScanInterval_s;
ELSE
    tPiraniDiscTimer_AB := MAX(0.0, tPiraniDiscTimer_AB - (tScanInterval_s * 2.0));
END_IF;

IF rDeltaBC > rToler_Pirani_mbar THEN
    tPiraniDiscTimer_BC := tPiraniDiscTimer_BC + tScanInterval_s;
ELSE
    tPiraniDiscTimer_BC := MAX(0.0, tPiraniDiscTimer_BC - (tScanInterval_s * 2.0));
END_IF;

IF rDeltaCA > rToler_Pirani_mbar THEN
    tPiraniDiscTimer_CA := tPiraniDiscTimer_CA + tScanInterval_s;
ELSE
    tPiraniDiscTimer_CA := MAX(0.0, tPiraniDiscTimer_CA - (tScanInterval_s * 2.0));
END_IF;

(* Channel Fault Discrimination via Pairwise Intersection *)
IF (tPiraniDiscTimer_AB >= rDiscrepancyLimit_s) AND (tPiraniDiscTimer_CA >= rDiscrepancyLimit_s) THEN
    bPiraniFault_A := TRUE;
END_IF;
IF (tPiraniDiscTimer_AB >= rDiscrepancyLimit_s) AND (tPiraniDiscTimer_BC >= rDiscrepancyLimit_s) THEN
    bPiraniFault_B := TRUE;
END_IF;
IF (tPiraniDiscTimer_BC >= rDiscrepancyLimit_s) AND (tPiraniDiscTimer_CA >= rDiscrepancyLimit_s) THEN
    bPiraniFault_C := TRUE;
END_IF;

(* Alarm Acknowledge Clearing *)
IF bAcknowledgeAlarms THEN
    IF (tPiraniDiscTimer_AB < rDiscrepancyLimit_s) AND (tPiraniDiscTimer_CA < rDiscrepancyLimit_s) THEN
        bPiraniFault_A := FALSE;
    END_IF;
    IF (tPiraniDiscTimer_AB < rDiscrepancyLimit_s) AND (tPiraniDiscTimer_BC < rDiscrepancyLimit_s) THEN
        bPiraniFault_B := FALSE;
    END_IF;
    IF (tPiraniDiscTimer_BC < rDiscrepancyLimit_s) AND (tPiraniDiscTimer_CA < rDiscrepancyLimit_s) THEN
        bPiraniFault_C := FALSE;
    END_IF;
END_IF;

(* Voting State Resolution *)
IF NOT bPiraniFault_A AND NOT bPiraniFault_B AND NOT bPiraniFault_C THEN
    (* Full 2oo3 Median Voting *)
    nPiraniHealthMode := 3;
    IF ((rChamberPirani_A >= rChamberPirani_B) AND (rChamberPirani_B >= rChamberPirani_C)) OR
       ((rChamberPirani_C >= rChamberPirani_B) AND (rChamberPirani_B >= rChamberPirani_A)) THEN
        rVotedPirani := rChamberPirani_B;
    ELSIF ((rChamberPirani_B >= rChamberPirani_A) AND (rChamberPirani_A >= rChamberPirani_C)) OR
          ((rChamberPirani_C >= rChamberPirani_A) AND (rChamberPirani_A >= rChamberPirani_B)) THEN
        rVotedPirani := rChamberPirani_A;
    ELSE
        rVotedPirani := rChamberPirani_C;
    END_IF;
ELSIF bPiraniFault_A AND NOT bPiraniFault_B AND NOT bPiraniFault_C THEN
    (* Degraded 1oo2 Average of B and C *)
    nPiraniHealthMode := 2;
    rVotedPirani := (rChamberPirani_B + rChamberPirani_C) * 0.50;
ELSIF NOT bPiraniFault_A AND bPiraniFault_B AND NOT bPiraniFault_C THEN
    (* Degraded 1oo2 Average of A and C *)
    nPiraniHealthMode := 2;
    rVotedPirani := (rChamberPirani_A + rChamberPirani_C) * 0.50;
ELSIF NOT bPiraniFault_A AND NOT bPiraniFault_B AND bPiraniFault_C THEN
    (* Degraded 1oo2 Average of A and B *)
    nPiraniHealthMode := 2;
    rVotedPirani := (rChamberPirani_A + rChamberPirani_B) * 0.50;
ELSIF NOT bPiraniFault_A AND bPiraniFault_B AND bPiraniFault_C THEN
    (* Degraded 1oo1 Single Channel A *)
    nPiraniHealthMode := 1;
    rVotedPirani := rChamberPirani_A;
ELSIF bPiraniFault_A AND NOT bPiraniFault_B AND bPiraniFault_C THEN
    (* Degraded 1oo1 Single Channel B *)
    nPiraniHealthMode := 1;
    rVotedPirani := rChamberPirani_B;
ELSIF bPiraniFault_A AND bPiraniFault_B AND NOT bPiraniFault_C THEN
    (* Degraded 1oo1 Single Channel C *)
    nPiraniHealthMode := 1;
    rVotedPirani := rChamberPirani_C;
ELSE
    (* Total Sensor Bank Failure *)
    nPiraniHealthMode := 0;
    rVotedPirani := vecX_hat[4]; (* Hold last known observer estimate *)
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* SENSOR BANK 2: CHAMBER CAPACITANCE DIAPHRAGM MANOMETERS (PT-102A / PT-102B / PT-102C) [mbar]        *)
(* ---------------------------------------------------------------------------------------------------- *)
rDeltaAB := ABS(rChamberCap_A - rChamberCap_B);
rDeltaBC := ABS(rChamberCap_B - rChamberCap_C);
rDeltaCA := ABS(rChamberCap_C - rChamberCap_A);

IF rDeltaAB > rToler_Cap_mbar THEN
    tCapDiscTimer_AB := tCapDiscTimer_AB + tScanInterval_s;
ELSE
    tCapDiscTimer_AB := MAX(0.0, tCapDiscTimer_AB - (tScanInterval_s * 2.0));
END_IF;

IF rDeltaBC > rToler_Cap_mbar THEN
    tCapDiscTimer_BC := tCapDiscTimer_BC + tScanInterval_s;
ELSE
    tCapDiscTimer_BC := MAX(0.0, tCapDiscTimer_BC - (tScanInterval_s * 2.0));
END_IF;

IF rDeltaCA > rToler_Cap_mbar THEN
    tCapDiscTimer_CA := tCapDiscTimer_CA + tScanInterval_s;
ELSE
    tCapDiscTimer_CA := MAX(0.0, tCapDiscTimer_CA - (tScanInterval_s * 2.0));
END_IF;

IF (tCapDiscTimer_AB >= rDiscrepancyLimit_s) AND (tCapDiscTimer_CA >= rDiscrepancyLimit_s) THEN
    bCapFault_A := TRUE;
END_IF;
IF (tCapDiscTimer_AB >= rDiscrepancyLimit_s) AND (tCapDiscTimer_BC >= rDiscrepancyLimit_s) THEN
    bCapFault_B := TRUE;
END_IF;
IF (tCapDiscTimer_BC >= rDiscrepancyLimit_s) AND (tCapDiscTimer_CA >= rDiscrepancyLimit_s) THEN
    bCapFault_C := TRUE;
END_IF;

IF bAcknowledgeAlarms THEN
    IF (tCapDiscTimer_AB < rDiscrepancyLimit_s) AND (tCapDiscTimer_CA < rDiscrepancyLimit_s) THEN
        bCapFault_A := FALSE;
    END_IF;
    IF (tCapDiscTimer_AB < rDiscrepancyLimit_s) AND (tCapDiscTimer_BC < rDiscrepancyLimit_s) THEN
        bCapFault_B := FALSE;
    END_IF;
    IF (tCapDiscTimer_BC < rDiscrepancyLimit_s) AND (tCapDiscTimer_CA < rDiscrepancyLimit_s) THEN
        bCapFault_C := FALSE;
    END_IF;
END_IF;

IF NOT bCapFault_A AND NOT bCapFault_B AND NOT bCapFault_C THEN
    nCapHealthMode := 3;
    IF ((rChamberCap_A >= rChamberCap_B) AND (rChamberCap_B >= rChamberCap_C)) OR
       ((rChamberCap_C >= rChamberCap_B) AND (rChamberCap_B >= rChamberCap_A)) THEN
        rVotedCap := rChamberCap_B;
    ELSIF ((rChamberCap_B >= rChamberCap_A) AND (rChamberCap_A >= rChamberCap_C)) OR
          ((rChamberCap_C >= rChamberCap_A) AND (rChamberCap_A >= rChamberCap_B)) THEN
        rVotedCap := rChamberCap_A;
    ELSE
        rVotedCap := rChamberCap_C;
    END_IF;
ELSIF bCapFault_A AND NOT bCapFault_B AND NOT bCapFault_C THEN
    nCapHealthMode := 2;
    rVotedCap := (rChamberCap_B + rChamberCap_C) * 0.50;
ELSIF NOT bCapFault_A AND bCapFault_B AND NOT bCapFault_C THEN
    nCapHealthMode := 2;
    rVotedCap := (rChamberCap_A + rChamberCap_C) * 0.50;
ELSIF NOT bCapFault_A AND NOT bCapFault_B AND bCapFault_C THEN
    nCapHealthMode := 2;
    rVotedCap := (rChamberCap_A + rChamberCap_B) * 0.50;
ELSIF NOT bCapFault_A AND bCapFault_B AND bCapFault_C THEN
    nCapHealthMode := 1;
    rVotedCap := rChamberCap_A;
ELSIF bCapFault_A AND NOT bCapFault_B AND bCapFault_C THEN
    nCapHealthMode := 1;
    rVotedCap := rChamberCap_B;
ELSIF bCapFault_A AND bCapFault_B AND NOT bCapFault_C THEN
    nCapHealthMode := 1;
    rVotedCap := rChamberCap_C;
ELSE
    nCapHealthMode := 0;
    rVotedCap := vecX_hat[4];
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* SENSOR BANK 3: SHELF SILICONE FLUID SUPPLY RTDs (TT-201A / TT-201B / TT-201C) [deg C]                *)
(* ---------------------------------------------------------------------------------------------------- *)
rDeltaAB := ABS(rShelfFluidTemp_A - rShelfFluidTemp_B);
rDeltaBC := ABS(rShelfFluidTemp_B - rShelfFluidTemp_C);
rDeltaCA := ABS(rShelfFluidTemp_C - rShelfFluidTemp_A);

IF rDeltaAB > rToler_ShelfTemp_degC THEN
    tShelfTempDiscTimer_AB := tShelfTempDiscTimer_AB + tScanInterval_s;
ELSE
    tShelfTempDiscTimer_AB := MAX(0.0, tShelfTempDiscTimer_AB - (tScanInterval_s * 2.0));
END_IF;

IF rDeltaBC > rToler_ShelfTemp_degC THEN
    tShelfTempDiscTimer_BC := tShelfTempDiscTimer_BC + tScanInterval_s;
ELSE
    tShelfTempDiscTimer_BC := MAX(0.0, tShelfTempDiscTimer_BC - (tScanInterval_s * 2.0));
END_IF;

IF rDeltaCA > rToler_ShelfTemp_degC THEN
    tShelfTempDiscTimer_CA := tShelfTempDiscTimer_CA + tScanInterval_s;
ELSE
    tShelfTempDiscTimer_CA := MAX(0.0, tShelfTempDiscTimer_CA - (tScanInterval_s * 2.0));
END_IF;

IF (tShelfTempDiscTimer_AB >= rDiscrepancyLimit_s) AND (tShelfTempDiscTimer_CA >= rDiscrepancyLimit_s) THEN
    bShelfTempFault_A := TRUE;
END_IF;
IF (tShelfTempDiscTimer_AB >= rDiscrepancyLimit_s) AND (tShelfTempDiscTimer_BC >= rDiscrepancyLimit_s) THEN
    bShelfTempFault_B := TRUE;
END_IF;
IF (tShelfTempDiscTimer_BC >= rDiscrepancyLimit_s) AND (tShelfTempDiscTimer_CA >= rDiscrepancyLimit_s) THEN
    bShelfTempFault_C := TRUE;
END_IF;

IF bAcknowledgeAlarms THEN
    IF (tShelfTempDiscTimer_AB < rDiscrepancyLimit_s) AND (tShelfTempDiscTimer_CA < rDiscrepancyLimit_s) THEN
        bShelfTempFault_A := FALSE;
    END_IF;
    IF (tShelfTempDiscTimer_AB < rDiscrepancyLimit_s) AND (tShelfTempDiscTimer_BC < rDiscrepancyLimit_s) THEN
        bShelfTempFault_B := FALSE;
    END_IF;
    IF (tShelfTempDiscTimer_BC < rDiscrepancyLimit_s) AND (tShelfTempDiscTimer_CA < rDiscrepancyLimit_s) THEN
        bShelfTempFault_C := FALSE;
    END_IF;
END_IF;

IF NOT bShelfTempFault_A AND NOT bShelfTempFault_B AND NOT bShelfTempFault_C THEN
    nShelfTempHealthMode := 3;
    IF ((rShelfFluidTemp_A >= rShelfFluidTemp_B) AND (rShelfFluidTemp_B >= rShelfFluidTemp_C)) OR
       ((rShelfFluidTemp_C >= rShelfFluidTemp_B) AND (rShelfFluidTemp_B >= rShelfFluidTemp_A)) THEN
        rVotedShelfFluidTemp := rShelfFluidTemp_B;
    ELSIF ((rShelfFluidTemp_B >= rShelfFluidTemp_A) AND (rShelfFluidTemp_A >= rShelfFluidTemp_C)) OR
          ((rShelfFluidTemp_C >= rShelfFluidTemp_A) AND (rShelfFluidTemp_A >= rShelfFluidTemp_B)) THEN
        rVotedShelfFluidTemp := rShelfFluidTemp_A;
    ELSE
        rVotedShelfFluidTemp := rShelfFluidTemp_C;
    END_IF;
ELSIF bShelfTempFault_A AND NOT bShelfTempFault_B AND NOT bShelfTempFault_C THEN
    nShelfTempHealthMode := 2;
    rVotedShelfFluidTemp := (rShelfFluidTemp_B + rShelfFluidTemp_C) * 0.50;
ELSIF NOT bShelfTempFault_A AND bShelfTempFault_B AND NOT bShelfTempFault_C THEN
    nShelfTempHealthMode := 2;
    rVotedShelfFluidTemp := (rShelfFluidTemp_A + rShelfFluidTemp_C) * 0.50;
ELSIF NOT bShelfTempFault_A AND NOT bShelfTempFault_B AND bShelfTempFault_C THEN
    nShelfTempHealthMode := 2;
    rVotedShelfFluidTemp := (rShelfFluidTemp_A + rShelfFluidTemp_B) * 0.50;
ELSIF NOT bShelfTempFault_A AND bShelfTempFault_B AND bShelfTempFault_C THEN
    nShelfTempHealthMode := 1;
    rVotedShelfFluidTemp := rShelfFluidTemp_A;
ELSIF bShelfTempFault_A AND NOT bShelfTempFault_B AND bShelfTempFault_C THEN
    nShelfTempHealthMode := 1;
    rVotedShelfFluidTemp := rShelfFluidTemp_B;
ELSIF bShelfTempFault_A AND bShelfTempFault_B AND NOT bShelfTempFault_C THEN
    nShelfTempHealthMode := 1;
    rVotedShelfFluidTemp := rShelfFluidTemp_C;
ELSE
    nShelfTempHealthMode := 0;
    rVotedShelfFluidTemp := vecX_hat[1];
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* SENSOR BANK 4: PRODUCT VIAL CORE TEMPERATURE RTDs (TT-301A / TT-301B / TT-301C) [deg C]              *)
(* ---------------------------------------------------------------------------------------------------- *)
rDeltaAB := ABS(rProductVialTemp_A - rProductVialTemp_B);
rDeltaBC := ABS(rProductVialTemp_B - rProductVialTemp_C);
rDeltaCA := ABS(rProductVialTemp_C - rProductVialTemp_A);

IF rDeltaAB > rToler_VialTemp_degC THEN
    tVialTempDiscTimer_AB := tVialTempDiscTimer_AB + tScanInterval_s;
ELSE
    tVialTempDiscTimer_AB := MAX(0.0, tVialTempDiscTimer_AB - (tScanInterval_s * 2.0));
END_IF;

IF rDeltaBC > rToler_VialTemp_degC THEN
    tVialTempDiscTimer_BC := tVialTempDiscTimer_BC + tScanInterval_s;
ELSE
    tVialTempDiscTimer_BC := MAX(0.0, tVialTempDiscTimer_BC - (tScanInterval_s * 2.0));
END_IF;

IF rDeltaCA > rToler_VialTemp_degC THEN
    tVialTempDiscTimer_CA := tVialTempDiscTimer_CA + tScanInterval_s;
ELSE
    tVialTempDiscTimer_CA := MAX(0.0, tVialTempDiscTimer_CA - (tScanInterval_s * 2.0));
END_IF;

IF (tVialTempDiscTimer_AB >= rDiscrepancyLimit_s) AND (tVialTempDiscTimer_CA >= rDiscrepancyLimit_s) THEN
    bVialTempFault_A := TRUE;
END_IF;
IF (tVialTempDiscTimer_AB >= rDiscrepancyLimit_s) AND (tVialTempDiscTimer_BC >= rDiscrepancyLimit_s) THEN
    bVialTempFault_B := TRUE;
END_IF;
IF (tVialTempDiscTimer_BC >= rDiscrepancyLimit_s) AND (tVialTempDiscTimer_CA >= rDiscrepancyLimit_s) THEN
    bVialTempFault_C := TRUE;
END_IF;

IF bAcknowledgeAlarms THEN
    IF (tVialTempDiscTimer_AB < rDiscrepancyLimit_s) AND (tVialTempDiscTimer_CA < rDiscrepancyLimit_s) THEN
        bVialTempFault_A := FALSE;
    END_IF;
    IF (tVialTempDiscTimer_AB < rDiscrepancyLimit_s) AND (tVialTempDiscTimer_BC < rDiscrepancyLimit_s) THEN
        bVialTempFault_B := FALSE;
    END_IF;
    IF (tVialTempDiscTimer_BC < rDiscrepancyLimit_s) AND (tVialTempDiscTimer_CA < rDiscrepancyLimit_s) THEN
        bVialTempFault_C := FALSE;
    END_IF;
END_IF;

IF NOT bVialTempFault_A AND NOT bVialTempFault_B AND NOT bVialTempFault_C THEN
    nVialTempHealthMode := 3;
    IF ((rProductVialTemp_A >= rProductVialTemp_B) AND (rProductVialTemp_B >= rProductVialTemp_C)) OR
       ((rProductVialTemp_C >= rProductVialTemp_B) AND (rProductVialTemp_B >= rProductVialTemp_A)) THEN
        rVotedProductVialTemp := rProductVialTemp_B;
    ELSIF ((rProductVialTemp_B >= rProductVialTemp_A) AND (rProductVialTemp_A >= rProductVialTemp_C)) OR
          ((rProductVialTemp_C >= rProductVialTemp_A) AND (rProductVialTemp_A >= rProductVialTemp_B)) THEN
        rVotedProductVialTemp := rProductVialTemp_A;
    ELSE
        rVotedProductVialTemp := rProductVialTemp_C;
    END_IF;
ELSIF bVialTempFault_A AND NOT bVialTempFault_B AND NOT bVialTempFault_C THEN
    nVialTempHealthMode := 2;
    rVotedProductVialTemp := (rProductVialTemp_B + rProductVialTemp_C) * 0.50;
ELSIF NOT bVialTempFault_A AND bVialTempFault_B AND NOT bVialTempFault_C THEN
    nVialTempHealthMode := 2;
    rVotedProductVialTemp := (rProductVialTemp_A + rProductVialTemp_C) * 0.50;
ELSIF NOT bVialTempFault_A AND NOT bVialTempFault_B AND bVialTempFault_C THEN
    nVialTempHealthMode := 2;
    rVotedProductVialTemp := (rProductVialTemp_A + rProductVialTemp_B) * 0.50;
ELSIF NOT bVialTempFault_A AND bVialTempFault_B AND bVialTempFault_C THEN
    nVialTempHealthMode := 1;
    rVotedProductVialTemp := rProductVialTemp_A;
ELSIF bVialTempFault_A AND NOT bVialTempFault_B AND bVialTempFault_C THEN
    nVialTempHealthMode := 1;
    rVotedProductVialTemp := rProductVialTemp_B;
ELSIF bVialTempFault_A AND bVialTempFault_B AND NOT bVialTempFault_C THEN
    nVialTempHealthMode := 1;
    rVotedProductVialTemp := rProductVialTemp_C;
ELSE
    nVialTempHealthMode := 0;
    rVotedProductVialTemp := vecX_hat[2];
END_IF;
"""
