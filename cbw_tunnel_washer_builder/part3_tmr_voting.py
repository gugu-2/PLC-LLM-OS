# cbw_tunnel_washer_builder/part3_tmr_voting.py
# 2oo3 Triple Modular Redundancy (TMR) Sensor Voting Suite

def get_part3_tmr_voting():
    return """(* ==================================================================================================== *)
(* PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANT (TMR) SENSOR VOTING WITH DISCREPANCY TIMERS                 *)
(* ==================================================================================================== *)

(* -------------------------------------------------------------------------------------------------- *)
(* CHANNEL GROUP 1: TT-101A/B/C MAIN WASH BATH TEMPERATURE (COMPARTMENT #6 CORE DISINFECTION)         *)
(* Sensor Range: 0.0 to 120.0 [deg C], Pairwise Discrepancy Limit: 3.5 [deg C], Debounce: 2,000 [ms]  *)
(* -------------------------------------------------------------------------------------------------- *)
bTT_101A_Valid := (rTT_101A_MainWashTemp_degC >= 0.0) AND (rTT_101A_MainWashTemp_degC <= 120.0);
bTT_101B_Valid := (rTT_101B_MainWashTemp_degC >= 0.0) AND (rTT_101B_MainWashTemp_degC <= 120.0);
bTT_101C_Valid := (rTT_101C_MainWashTemp_degC >= 0.0) AND (rTT_101C_MainWashTemp_degC <= 120.0);

(* Pairwise Absolute Discrepancies *)
IF bTT_101A_Valid AND bTT_101B_Valid THEN
    rTT_101_Diff_AB := ABS(rTT_101A_MainWashTemp_degC - rTT_101B_MainWashTemp_degC);
ELSE
    rTT_101_Diff_AB := 999.0;
END_IF;

IF bTT_101B_Valid AND bTT_101C_Valid THEN
    rTT_101_Diff_BC := ABS(rTT_101B_MainWashTemp_degC - rTT_101C_MainWashTemp_degC);
ELSE
    rTT_101_Diff_BC := 999.0;
END_IF;

IF bTT_101C_Valid AND bTT_101A_Valid THEN
    rTT_101_Diff_CA := ABS(rTT_101C_MainWashTemp_degC - rTT_101A_MainWashTemp_degC);
ELSE
    rTT_101_Diff_CA := 999.0;
END_IF;

(* Persistence Debounce Timers for Pairwise Discrepancies *)
IF (rTT_101_Diff_AB > 3.5) AND bTT_101A_Valid AND bTT_101B_Valid THEN
    tTT_101_DiscrepancyTimer_AB := tTT_101_DiscrepancyTimer_AB + tTaskCycleTime;
    IF (tTT_101_DiscrepancyTimer_AB >= T#2000MS) THEN
        bTT_101_DiscrepancyFault_AB := TRUE;
    END_IF;
ELSE
    tTT_101_DiscrepancyTimer_AB := T#0MS;
    IF bResetFault THEN
        bTT_101_DiscrepancyFault_AB := FALSE;
    END_IF;
END_IF;

IF (rTT_101_Diff_BC > 3.5) AND bTT_101B_Valid AND bTT_101C_Valid THEN
    tTT_101_DiscrepancyTimer_BC := tTT_101_DiscrepancyTimer_BC + tTaskCycleTime;
    IF (tTT_101_DiscrepancyTimer_BC >= T#2000MS) THEN
        bTT_101_DiscrepancyFault_BC := TRUE;
    END_IF;
ELSE
    tTT_101_DiscrepancyTimer_BC := T#0MS;
    IF bResetFault THEN
        bTT_101_DiscrepancyFault_BC := FALSE;
    END_IF;
END_IF;

IF (rTT_101_Diff_CA > 3.5) AND bTT_101C_Valid AND bTT_101A_Valid THEN
    tTT_101_DiscrepancyTimer_CA := tTT_101_DiscrepancyTimer_CA + tTaskCycleTime;
    IF (tTT_101_DiscrepancyTimer_CA >= T#2000MS) THEN
        bTT_101_DiscrepancyFault_CA := TRUE;
    END_IF;
ELSE
    tTT_101_DiscrepancyTimer_CA := T#0MS;
    IF bResetFault THEN
        bTT_101_DiscrepancyFault_CA := FALSE;
    END_IF;
END_IF;

(* 2oo3 Core Voting & Invalidation Engine for TT-101 *)
IF bTT_101A_Valid AND bTT_101B_Valid AND bTT_101C_Valid THEN
    (* All Three Channels Physically Healthy *)
    IF NOT bTT_101_DiscrepancyFault_AB AND NOT bTT_101_DiscrepancyFault_BC AND NOT bTT_101_DiscrepancyFault_CA THEN
        (* Pristine Median Selection *)
        IF ((rTT_101A_MainWashTemp_degC >= rTT_101B_MainWashTemp_degC) AND (rTT_101A_MainWashTemp_degC <= rTT_101C_MainWashTemp_degC)) OR
           ((rTT_101A_MainWashTemp_degC <= rTT_101B_MainWashTemp_degC) AND (rTT_101A_MainWashTemp_degC >= rTT_101C_MainWashTemp_degC)) THEN
            rScratchSum := rTT_101A_MainWashTemp_degC;
        ELSIF ((rTT_101B_MainWashTemp_degC >= rTT_101A_MainWashTemp_degC) AND (rTT_101B_MainWashTemp_degC <= rTT_101C_MainWashTemp_degC)) OR
              ((rTT_101B_MainWashTemp_degC <= rTT_101A_MainWashTemp_degC) AND (rTT_101B_MainWashTemp_degC >= rTT_101C_MainWashTemp_degC)) THEN
            rScratchSum := rTT_101B_MainWashTemp_degC;
        ELSE
            rScratchSum := rTT_101C_MainWashTemp_degC;
        END_IF;
    ELSIF bTT_101_DiscrepancyFault_AB AND bTT_101_DiscrepancyFault_CA THEN
        (* Channel A is the Outlier *)
        rScratchSum := (rTT_101B_MainWashTemp_degC + rTT_101C_MainWashTemp_degC) * 0.5;
        bTT_101A_Valid := FALSE;
    ELSIF bTT_101_DiscrepancyFault_AB AND bTT_101_DiscrepancyFault_BC THEN
        (* Channel B is the Outlier *)
        rScratchSum := (rTT_101A_MainWashTemp_degC + rTT_101C_MainWashTemp_degC) * 0.5;
        bTT_101B_Valid := FALSE;
    ELSIF bTT_101_DiscrepancyFault_BC AND bTT_101_DiscrepancyFault_CA THEN
        (* Channel C is the Outlier *)
        rScratchSum := (rTT_101A_MainWashTemp_degC + rTT_101B_MainWashTemp_degC) * 0.5;
        bTT_101C_Valid := FALSE;
    ELSE
        (* Single Pair Discrepancy -> Take Median *)
        IF ((rTT_101A_MainWashTemp_degC >= rTT_101B_MainWashTemp_degC) AND (rTT_101A_MainWashTemp_degC <= rTT_101C_MainWashTemp_degC)) OR
           ((rTT_101A_MainWashTemp_degC <= rTT_101B_MainWashTemp_degC) AND (rTT_101A_MainWashTemp_degC >= rTT_101C_MainWashTemp_degC)) THEN
            rScratchSum := rTT_101A_MainWashTemp_degC;
        ELSIF ((rTT_101B_MainWashTemp_degC >= rTT_101A_MainWashTemp_degC) AND (rTT_101B_MainWashTemp_degC <= rTT_101C_MainWashTemp_degC)) OR
              ((rTT_101B_MainWashTemp_degC <= rTT_101A_MainWashTemp_degC) AND (rTT_101B_MainWashTemp_degC >= rTT_101C_MainWashTemp_degC)) THEN
            rScratchSum := rTT_101B_MainWashTemp_degC;
        ELSE
            rScratchSum := rTT_101C_MainWashTemp_degC;
        END_IF;
    END_IF;
ELSIF bTT_101A_Valid AND bTT_101B_Valid THEN
    (* Channel C Failed Hardware Check *)
    rScratchSum := (rTT_101A_MainWashTemp_degC + rTT_101B_MainWashTemp_degC) * 0.5;
ELSIF bTT_101B_Valid AND bTT_101C_Valid THEN
    (* Channel A Failed Hardware Check *)
    rScratchSum := (rTT_101B_MainWashTemp_degC + rTT_101C_MainWashTemp_degC) * 0.5;
ELSIF bTT_101C_Valid AND bTT_101A_Valid THEN
    (* Channel B Failed Hardware Check *)
    rScratchSum := (rTT_101C_MainWashTemp_degC + rTT_101A_MainWashTemp_degC) * 0.5;
ELSIF bTT_101A_Valid THEN
    rScratchSum := rTT_101A_MainWashTemp_degC;
ELSIF bTT_101B_Valid THEN
    rScratchSum := rTT_101B_MainWashTemp_degC;
ELSIF bTT_101C_Valid THEN
    rScratchSum := rTT_101C_MainWashTemp_degC;
ELSE
    (* All Three Channels Failed -> Fail-Safe Hold *)
    rScratchSum := rTT_101_PrevVotedValue;
END_IF;

(* Slew-Rate Limiting Filter for Bumpless Sensor Transfer (Max 1.5 deg C per 100 ms) *)
IF (rScratchSum - rTT_101_PrevVotedValue > 1.5) THEN
    rVotedMainWashTemp_degC := rTT_101_PrevVotedValue + 1.5;
ELSIF (rTT_101_PrevVotedValue - rScratchSum > 1.5) THEN
    rVotedMainWashTemp_degC := rTT_101_PrevVotedValue - 1.5;
ELSE
    rVotedMainWashTemp_degC := rScratchSum;
END_IF;
rTT_101_PrevVotedValue := rVotedMainWashTemp_degC;


(* -------------------------------------------------------------------------------------------------- *)
(* CHANNEL GROUP 2: AT-201A/B/C COUNTER-FLOW RINSE CONDUCTIVITY (COMPARTMENT #14 RINSE ZONE)          *)
(* Sensor Range: 0.01 to 10.0 [mS/cm], Pairwise Discrepancy Limit: 0.15 [mS/cm], Debounce: 2,500 [ms] *)
(* -------------------------------------------------------------------------------------------------- *)
bAT_201A_Valid := (rAT_201A_RinseConductivity_mS >= 0.01) AND (rAT_201A_RinseConductivity_mS <= 10.0);
bAT_201B_Valid := (rAT_201B_RinseConductivity_mS >= 0.01) AND (rAT_201B_RinseConductivity_mS <= 10.0);
bAT_201C_Valid := (rAT_201C_RinseConductivity_mS >= 0.01) AND (rAT_201C_RinseConductivity_mS <= 10.0);

IF bAT_201A_Valid AND bAT_201B_Valid THEN
    rAT_201_Diff_AB := ABS(rAT_201A_RinseConductivity_mS - rAT_201B_RinseConductivity_mS);
ELSE
    rAT_201_Diff_AB := 999.0;
END_IF;

IF bAT_201B_Valid AND bAT_201C_Valid THEN
    rAT_201_Diff_BC := ABS(rAT_201B_RinseConductivity_mS - rAT_201C_RinseConductivity_mS);
ELSE
    rAT_201_Diff_BC := 999.0;
END_IF;

IF bAT_201C_Valid AND bAT_201A_Valid THEN
    rAT_201_Diff_CA := ABS(rAT_201C_RinseConductivity_mS - rAT_201A_RinseConductivity_mS);
ELSE
    rAT_201_Diff_CA := 999.0;
END_IF;

(* Persistence Debounce Timers for AT-201 Discrepancies *)
IF (rAT_201_Diff_AB > 0.15) AND bAT_201A_Valid AND bAT_201B_Valid THEN
    tAT_201_DiscrepancyTimer_AB := tAT_201_DiscrepancyTimer_AB + tTaskCycleTime;
    IF (tAT_201_DiscrepancyTimer_AB >= T#2500MS) THEN
        bAT_201_DiscrepancyFault_AB := TRUE;
    END_IF;
ELSE
    tAT_201_DiscrepancyTimer_AB := T#0MS;
    IF bResetFault THEN
        bAT_201_DiscrepancyFault_AB := FALSE;
    END_IF;
END_IF;

IF (rAT_201_Diff_BC > 0.15) AND bAT_201B_Valid AND bAT_201C_Valid THEN
    tAT_201_DiscrepancyTimer_BC := tAT_201_DiscrepancyTimer_BC + tTaskCycleTime;
    IF (tAT_201_DiscrepancyTimer_BC >= T#2500MS) THEN
        bAT_201_DiscrepancyFault_BC := TRUE;
    END_IF;
ELSE
    tAT_201_DiscrepancyTimer_BC := T#0MS;
    IF bResetFault THEN
        bAT_201_DiscrepancyFault_BC := FALSE;
    END_IF;
END_IF;

IF (rAT_201_Diff_CA > 0.15) AND bAT_201C_Valid AND bAT_201A_Valid THEN
    tAT_201_DiscrepancyTimer_CA := tAT_201_DiscrepancyTimer_CA + tTaskCycleTime;
    IF (tAT_201_DiscrepancyTimer_CA >= T#2500MS) THEN
        bAT_201_DiscrepancyFault_CA := TRUE;
    END_IF;
ELSE
    tAT_201_DiscrepancyTimer_CA := T#0MS;
    IF bResetFault THEN
        bAT_201_DiscrepancyFault_CA := FALSE;
    END_IF;
END_IF;

(* 2oo3 Voting Engine for AT-201 *)
IF bAT_201A_Valid AND bAT_201B_Valid AND bAT_201C_Valid THEN
    IF NOT bAT_201_DiscrepancyFault_AB AND NOT bAT_201_DiscrepancyFault_BC AND NOT bAT_201_DiscrepancyFault_CA THEN
        IF ((rAT_201A_RinseConductivity_mS >= rAT_201B_RinseConductivity_mS) AND (rAT_201A_RinseConductivity_mS <= rAT_201C_RinseConductivity_mS)) OR
           ((rAT_201A_RinseConductivity_mS <= rAT_201B_RinseConductivity_mS) AND (rAT_201A_RinseConductivity_mS >= rAT_201C_RinseConductivity_mS)) THEN
            rScratchSum := rAT_201A_RinseConductivity_mS;
        ELSIF ((rAT_201B_RinseConductivity_mS >= rAT_201A_RinseConductivity_mS) AND (rAT_201B_RinseConductivity_mS <= rAT_201C_RinseConductivity_mS)) OR
              ((rAT_201B_RinseConductivity_mS <= rAT_201A_RinseConductivity_mS) AND (rAT_201B_RinseConductivity_mS >= rAT_201C_RinseConductivity_mS)) THEN
            rScratchSum := rAT_201B_RinseConductivity_mS;
        ELSE
            rScratchSum := rAT_201C_RinseConductivity_mS;
        END_IF;
    ELSIF bAT_201_DiscrepancyFault_AB AND bAT_201_DiscrepancyFault_CA THEN
        rScratchSum := (rAT_201B_RinseConductivity_mS + rAT_201C_RinseConductivity_mS) * 0.5;
        bAT_201A_Valid := FALSE;
    ELSIF bAT_201_DiscrepancyFault_AB AND bAT_201_DiscrepancyFault_BC THEN
        rScratchSum := (rAT_201A_RinseConductivity_mS + rAT_201C_RinseConductivity_mS) * 0.5;
        bAT_201B_Valid := FALSE;
    ELSIF bAT_201_DiscrepancyFault_BC AND bAT_201_DiscrepancyFault_CA THEN
        rScratchSum := (rAT_201A_RinseConductivity_mS + rAT_201B_RinseConductivity_mS) * 0.5;
        bAT_201C_Valid := FALSE;
    ELSE
        IF ((rAT_201A_RinseConductivity_mS >= rAT_201B_RinseConductivity_mS) AND (rAT_201A_RinseConductivity_mS <= rAT_201C_RinseConductivity_mS)) OR
           ((rAT_201A_RinseConductivity_mS <= rAT_201B_RinseConductivity_mS) AND (rAT_201A_RinseConductivity_mS >= rAT_201C_RinseConductivity_mS)) THEN
            rScratchSum := rAT_201A_RinseConductivity_mS;
        ELSIF ((rAT_201B_RinseConductivity_mS >= rAT_201A_RinseConductivity_mS) AND (rAT_201B_RinseConductivity_mS <= rAT_201C_RinseConductivity_mS)) OR
              ((rAT_201B_RinseConductivity_mS <= rAT_201A_RinseConductivity_mS) AND (rAT_201B_RinseConductivity_mS >= rAT_201C_RinseConductivity_mS)) THEN
            rScratchSum := rAT_201B_RinseConductivity_mS;
        ELSE
            rScratchSum := rAT_201C_RinseConductivity_mS;
        END_IF;
    END_IF;
ELSIF bAT_201A_Valid AND bAT_201B_Valid THEN
    rScratchSum := (rAT_201A_RinseConductivity_mS + rAT_201B_RinseConductivity_mS) * 0.5;
ELSIF bAT_201B_Valid AND bAT_201C_Valid THEN
    rScratchSum := (rAT_201B_RinseConductivity_mS + rAT_201C_RinseConductivity_mS) * 0.5;
ELSIF bAT_201C_Valid AND bAT_201A_Valid THEN
    rScratchSum := (rAT_201C_RinseConductivity_mS + rAT_201A_RinseConductivity_mS) * 0.5;
ELSIF bAT_201A_Valid THEN
    rScratchSum := rAT_201A_RinseConductivity_mS;
ELSIF bAT_201B_Valid THEN
    rScratchSum := rAT_201B_RinseConductivity_mS;
ELSIF bAT_201C_Valid THEN
    rScratchSum := rAT_201C_RinseConductivity_mS;
ELSE
    rScratchSum := rAT_201_PrevVotedValue;
END_IF;

(* Rate of Change Filter (Max 0.05 mS/cm per 100 ms) *)
IF (rScratchSum - rAT_201_PrevVotedValue > 0.05) THEN
    rVotedRinseConductivity_mS := rAT_201_PrevVotedValue + 0.05;
ELSIF (rAT_201_PrevVotedValue - rScratchSum > 0.05) THEN
    rVotedRinseConductivity_mS := rAT_201_PrevVotedValue - 0.05;
ELSE
    rVotedRinseConductivity_mS := rScratchSum;
END_IF;
rAT_201_PrevVotedValue := rVotedRinseConductivity_mS;


(* -------------------------------------------------------------------------------------------------- *)
(* CHANNEL GROUP 3: PT-301A/B/C EXTRACTOR HYDRAULIC PRESSURE (DEWATERING PRESS RAM)                  *)
(* Sensor Range: -1.0 to 70.0 [bar], Pairwise Discrepancy Limit: 2.5 [bar], Debounce: 1,500 [ms]      *)
(* -------------------------------------------------------------------------------------------------- *)
bPT_301A_Valid := (rPT_301A_PressPressure_bar >= -1.0) AND (rPT_301A_PressPressure_bar <= 70.0);
bPT_301B_Valid := (rPT_301B_PressPressure_bar >= -1.0) AND (rPT_301B_PressPressure_bar <= 70.0);
bPT_301C_Valid := (rPT_301C_PressPressure_bar >= -1.0) AND (rPT_301C_PressPressure_bar <= 70.0);

IF bPT_301A_Valid AND bPT_301B_Valid THEN
    rPT_301_Diff_AB := ABS(rPT_301A_PressPressure_bar - rPT_301B_PressPressure_bar);
ELSE
    rPT_301_Diff_AB := 999.0;
END_IF;

IF bPT_301B_Valid AND bPT_301C_Valid THEN
    rPT_301_Diff_BC := ABS(rPT_301B_PressPressure_bar - rPT_301C_PressPressure_bar);
ELSE
    rPT_301_Diff_BC := 999.0;
END_IF;

IF bPT_301C_Valid AND bPT_301A_Valid THEN
    rPT_301_Diff_CA := ABS(rPT_301C_PressPressure_bar - rPT_301A_PressPressure_bar);
ELSE
    rPT_301_Diff_CA := 999.0;
END_IF;

(* Discrepancy Timers for PT-301 *)
IF (rPT_301_Diff_AB > 2.5) AND bPT_301A_Valid AND bPT_301B_Valid THEN
    tPT_301_DiscrepancyTimer_AB := tPT_301_DiscrepancyTimer_AB + tTaskCycleTime;
    IF (tPT_301_DiscrepancyTimer_AB >= T#1500MS) THEN
        bPT_301_DiscrepancyFault_AB := TRUE;
    END_IF;
ELSE
    tPT_301_DiscrepancyTimer_AB := T#0MS;
    IF bResetFault THEN
        bPT_301_DiscrepancyFault_AB := FALSE;
    END_IF;
END_IF;

IF (rPT_301_Diff_BC > 2.5) AND bPT_301B_Valid AND bPT_301C_Valid THEN
    tPT_301_DiscrepancyTimer_BC := tPT_301_DiscrepancyTimer_BC + tTaskCycleTime;
    IF (tPT_301_DiscrepancyTimer_BC >= T#1500MS) THEN
        bPT_301_DiscrepancyFault_BC := TRUE;
    END_IF;
ELSE
    tPT_301_DiscrepancyTimer_BC := T#0MS;
    IF bResetFault THEN
        bPT_301_DiscrepancyFault_BC := FALSE;
    END_IF;
END_IF;

IF (rPT_301_Diff_CA > 2.5) AND bPT_301C_Valid AND bPT_301A_Valid THEN
    tPT_301_DiscrepancyTimer_CA := tPT_301_DiscrepancyTimer_CA + tTaskCycleTime;
    IF (tPT_301_DiscrepancyTimer_CA >= T#1500MS) THEN
        bPT_301_DiscrepancyFault_CA := TRUE;
    END_IF;
ELSE
    tPT_301_DiscrepancyTimer_CA := T#0MS;
    IF bResetFault THEN
        bPT_301_DiscrepancyFault_CA := FALSE;
    END_IF;
END_IF;

(* 2oo3 Voting Engine for PT-301 *)
IF bPT_301A_Valid AND bPT_301B_Valid AND bPT_301C_Valid THEN
    IF NOT bPT_301_DiscrepancyFault_AB AND NOT bPT_301_DiscrepancyFault_BC AND NOT bPT_301_DiscrepancyFault_CA THEN
        IF ((rPT_301A_PressPressure_bar >= rPT_301B_PressPressure_bar) AND (rPT_301A_PressPressure_bar <= rPT_301C_PressPressure_bar)) OR
           ((rPT_301A_PressPressure_bar <= rPT_301B_PressPressure_bar) AND (rPT_301A_PressPressure_bar >= rPT_301C_PressPressure_bar)) THEN
            rScratchSum := rPT_301A_PressPressure_bar;
        ELSIF ((rPT_301B_PressPressure_bar >= rPT_301A_PressPressure_bar) AND (rPT_301B_PressPressure_bar <= rPT_301C_PressPressure_bar)) OR
              ((rPT_301B_PressPressure_bar <= rPT_301A_PressPressure_bar) AND (rPT_301B_PressPressure_bar >= rPT_301C_PressPressure_bar)) THEN
            rScratchSum := rPT_301B_PressPressure_bar;
        ELSE
            rScratchSum := rPT_301C_PressPressure_bar;
        END_IF;
    ELSIF bPT_301_DiscrepancyFault_AB AND bPT_301_DiscrepancyFault_CA THEN
        rScratchSum := (rPT_301B_PressPressure_bar + rPT_301C_PressPressure_bar) * 0.5;
        bPT_301A_Valid := FALSE;
    ELSIF bPT_301_DiscrepancyFault_AB AND bPT_301_DiscrepancyFault_BC THEN
        rScratchSum := (rPT_301A_PressPressure_bar + rPT_301C_PressPressure_bar) * 0.5;
        bPT_301B_Valid := FALSE;
    ELSIF bPT_301_DiscrepancyFault_BC AND bPT_301_DiscrepancyFault_CA THEN
        rScratchSum := (rPT_301A_PressPressure_bar + rPT_301B_PressPressure_bar) * 0.5;
        bPT_301C_Valid := FALSE;
    ELSE
        IF ((rPT_301A_PressPressure_bar >= rPT_301B_PressPressure_bar) AND (rPT_301A_PressPressure_bar <= rPT_301C_PressPressure_bar)) OR
           ((rPT_301A_PressPressure_bar <= rPT_301B_PressPressure_bar) AND (rPT_301A_PressPressure_bar >= rPT_301C_PressPressure_bar)) THEN
            rScratchSum := rPT_301A_PressPressure_bar;
        ELSIF ((rPT_301B_PressPressure_bar >= rPT_301A_PressPressure_bar) AND (rPT_301B_PressPressure_bar <= rPT_301C_PressPressure_bar)) OR
              ((rPT_301B_PressPressure_bar <= rPT_301A_PressPressure_bar) AND (rPT_301B_PressPressure_bar >= rPT_301C_PressPressure_bar)) THEN
            rScratchSum := rPT_301B_PressPressure_bar;
        ELSE
            rScratchSum := rPT_301C_PressPressure_bar;
        END_IF;
    END_IF;
ELSIF bPT_301A_Valid AND bPT_301B_Valid THEN
    rScratchSum := (rPT_301A_PressPressure_bar + rPT_301B_PressPressure_bar) * 0.5;
ELSIF bPT_301B_Valid AND bPT_301C_Valid THEN
    rScratchSum := (rPT_301B_PressPressure_bar + rPT_301C_PressPressure_bar) * 0.5;
ELSIF bPT_301C_Valid AND bPT_301A_Valid THEN
    rScratchSum := (rPT_301C_PressPressure_bar + rPT_301A_PressPressure_bar) * 0.5;
ELSIF bPT_301A_Valid THEN
    rScratchSum := rPT_301A_PressPressure_bar;
ELSIF bPT_301B_Valid THEN
    rScratchSum := rPT_301B_PressPressure_bar;
ELSIF bPT_301C_Valid THEN
    rScratchSum := rPT_301C_PressPressure_bar;
ELSE
    rScratchSum := rPT_301_PrevVotedValue;
END_IF;

(* Rate of Change Filter (Max 2.0 bar per 100 ms) *)
IF (rScratchSum - rPT_301_PrevVotedValue > 2.0) THEN
    rVotedPressPressure_bar := rPT_301_PrevVotedValue + 2.0;
ELSIF (rPT_301_PrevVotedValue - rScratchSum > 2.0) THEN
    rVotedPressPressure_bar := rPT_301_PrevVotedValue - 2.0;
ELSE
    rVotedPressPressure_bar := rScratchSum;
END_IF;
rPT_301_PrevVotedValue := rVotedPressPressure_bar;


(* -------------------------------------------------------------------------------------------------- *)
(* CHANNEL GROUP 4: FT-401A/B/C FRESHWATER MAKEUP FLOW RATE                                           *)
(* Sensor Range: 0.0 to 30.0 [m3/h], Pairwise Discrepancy Limit: 1.2 [m3/h], Debounce: 2,000 [ms]     *)
(* -------------------------------------------------------------------------------------------------- *)
bFT_401A_Valid := (rFT_401A_FreshwaterFlow_m3h >= 0.0) AND (rFT_401A_FreshwaterFlow_m3h <= 30.0);
bFT_401B_Valid := (rFT_401B_FreshwaterFlow_m3h >= 0.0) AND (rFT_401B_FreshwaterFlow_m3h <= 30.0);
bFT_401C_Valid := (rFT_401C_FreshwaterFlow_m3h >= 0.0) AND (rFT_401C_FreshwaterFlow_m3h <= 30.0);

IF bFT_401A_Valid AND bFT_401B_Valid THEN
    rFT_401_Diff_AB := ABS(rFT_401A_FreshwaterFlow_m3h - rFT_401B_FreshwaterFlow_m3h);
ELSE
    rFT_401_Diff_AB := 999.0;
END_IF;

IF bFT_401B_Valid AND bFT_401C_Valid THEN
    rFT_401_Diff_BC := ABS(rFT_401B_FreshwaterFlow_m3h - rFT_401C_FreshwaterFlow_m3h);
ELSE
    rFT_401_Diff_BC := 999.0;
END_IF;

IF bFT_401C_Valid AND bFT_401A_Valid THEN
    rFT_401_Diff_CA := ABS(rFT_401C_FreshwaterFlow_m3h - rFT_401A_FreshwaterFlow_m3h);
ELSE
    rFT_401_Diff_CA := 999.0;
END_IF;

(* Discrepancy Timers for FT-401 *)
IF (rFT_401_Diff_AB > 1.2) AND bFT_401A_Valid AND bFT_401B_Valid THEN
    tFT_401_DiscrepancyTimer_AB := tFT_401_DiscrepancyTimer_AB + tTaskCycleTime;
    IF (tFT_401_DiscrepancyTimer_AB >= T#2000MS) THEN
        bFT_401_DiscrepancyFault_AB := TRUE;
    END_IF;
ELSE
    tFT_401_DiscrepancyTimer_AB := T#0MS;
    IF bResetFault THEN
        bFT_401_DiscrepancyFault_AB := FALSE;
    END_IF;
END_IF;

IF (rFT_401_Diff_BC > 1.2) AND bFT_401B_Valid AND bFT_401C_Valid THEN
    tFT_401_DiscrepancyTimer_BC := tFT_401_DiscrepancyTimer_BC + tTaskCycleTime;
    IF (tFT_401_DiscrepancyTimer_BC >= T#2000MS) THEN
        bFT_401_DiscrepancyFault_BC := TRUE;
    END_IF;
ELSE
    tFT_401_DiscrepancyTimer_BC := T#0MS;
    IF bResetFault THEN
        bFT_401_DiscrepancyFault_BC := FALSE;
    END_IF;
END_IF;

IF (rFT_401_Diff_CA > 1.2) AND bFT_401C_Valid AND bFT_401A_Valid THEN
    tFT_401_DiscrepancyTimer_CA := tFT_401_DiscrepancyTimer_CA + tTaskCycleTime;
    IF (tFT_401_DiscrepancyTimer_CA >= T#2000MS) THEN
        bFT_401_DiscrepancyFault_CA := TRUE;
    END_IF;
ELSE
    tFT_401_DiscrepancyTimer_CA := T#0MS;
    IF bResetFault THEN
        bFT_401_DiscrepancyFault_CA := FALSE;
    END_IF;
END_IF;

(* 2oo3 Voting Engine for FT-401 *)
IF bFT_401A_Valid AND bFT_401B_Valid AND bFT_401C_Valid THEN
    IF NOT bFT_401_DiscrepancyFault_AB AND NOT bFT_401_DiscrepancyFault_BC AND NOT bFT_401_DiscrepancyFault_CA THEN
        IF ((rFT_401A_FreshwaterFlow_m3h >= rFT_401B_FreshwaterFlow_m3h) AND (rFT_401A_FreshwaterFlow_m3h <= rFT_401C_FreshwaterFlow_m3h)) OR
           ((rFT_401A_FreshwaterFlow_m3h <= rFT_401B_FreshwaterFlow_m3h) AND (rFT_401A_FreshwaterFlow_m3h >= rFT_401C_FreshwaterFlow_m3h)) THEN
            rScratchSum := rFT_401A_FreshwaterFlow_m3h;
        ELSIF ((rFT_401B_FreshwaterFlow_m3h >= rFT_401A_FreshwaterFlow_m3h) AND (rFT_401B_FreshwaterFlow_m3h <= rFT_401C_FreshwaterFlow_m3h)) OR
              ((rFT_401B_FreshwaterFlow_m3h <= rFT_401A_FreshwaterFlow_m3h) AND (rFT_401B_FreshwaterFlow_m3h >= rFT_401C_FreshwaterFlow_m3h)) THEN
            rScratchSum := rFT_401B_FreshwaterFlow_m3h;
        ELSE
            rScratchSum := rFT_401C_FreshwaterFlow_m3h;
        END_IF;
    ELSIF bFT_401_DiscrepancyFault_AB AND bFT_401_DiscrepancyFault_CA THEN
        rScratchSum := (rFT_401B_FreshwaterFlow_m3h + rFT_401C_FreshwaterFlow_m3h) * 0.5;
        bFT_401A_Valid := FALSE;
    ELSIF bFT_401_DiscrepancyFault_AB AND bFT_401_DiscrepancyFault_BC THEN
        rScratchSum := (rFT_401A_FreshwaterFlow_m3h + rFT_401C_FreshwaterFlow_m3h) * 0.5;
        bFT_401B_Valid := FALSE;
    ELSIF bFT_401_DiscrepancyFault_BC AND bFT_401_DiscrepancyFault_CA THEN
        rScratchSum := (rFT_401A_FreshwaterFlow_m3h + rFT_401B_FreshwaterFlow_m3h) * 0.5;
        bFT_401C_Valid := FALSE;
    ELSE
        IF ((rFT_401A_FreshwaterFlow_m3h >= rFT_401B_FreshwaterFlow_m3h) AND (rFT_401A_FreshwaterFlow_m3h <= rFT_401C_FreshwaterFlow_m3h)) OR
           ((rFT_401A_FreshwaterFlow_m3h <= rFT_401B_FreshwaterFlow_m3h) AND (rFT_401A_FreshwaterFlow_m3h >= rFT_401C_FreshwaterFlow_m3h)) THEN
            rScratchSum := rFT_401A_FreshwaterFlow_m3h;
        ELSIF ((rFT_401B_FreshwaterFlow_m3h >= rFT_401A_FreshwaterFlow_m3h) AND (rFT_401B_FreshwaterFlow_m3h <= rFT_401C_FreshwaterFlow_m3h)) OR
              ((rFT_401B_FreshwaterFlow_m3h <= rFT_401A_FreshwaterFlow_m3h) AND (rFT_401B_FreshwaterFlow_m3h >= rFT_401C_FreshwaterFlow_m3h)) THEN
            rScratchSum := rFT_401B_FreshwaterFlow_m3h;
        ELSE
            rScratchSum := rFT_401C_FreshwaterFlow_m3h;
        END_IF;
    END_IF;
ELSIF bFT_401A_Valid AND bFT_401B_Valid THEN
    rScratchSum := (rFT_401A_FreshwaterFlow_m3h + rFT_401B_FreshwaterFlow_m3h) * 0.5;
ELSIF bFT_401B_Valid AND bFT_401C_Valid THEN
    rScratchSum := (rFT_401B_FreshwaterFlow_m3h + rFT_401C_FreshwaterFlow_m3h) * 0.5;
ELSIF bFT_401C_Valid AND bFT_401A_Valid THEN
    rScratchSum := (rFT_401C_FreshwaterFlow_m3h + rFT_401A_FreshwaterFlow_m3h) * 0.5;
ELSIF bFT_401A_Valid THEN
    rScratchSum := rFT_401A_FreshwaterFlow_m3h;
ELSIF bFT_401B_Valid THEN
    rScratchSum := rFT_401B_FreshwaterFlow_m3h;
ELSIF bFT_401C_Valid THEN
    rScratchSum := rFT_401C_FreshwaterFlow_m3h;
ELSE
    rScratchSum := rFT_401_PrevVotedValue;
END_IF;

(* Rate of Change Filter (Max 0.8 m3/h per 100 ms) *)
IF (rScratchSum - rFT_401_PrevVotedValue > 0.8) THEN
    rVotedFreshwaterFlow_m3h := rFT_401_PrevVotedValue + 0.8;
ELSIF (rFT_401_PrevVotedValue - rScratchSum > 0.8) THEN
    rVotedFreshwaterFlow_m3h := rFT_401_PrevVotedValue - 0.8;
ELSE
    rVotedFreshwaterFlow_m3h := rScratchSum;
END_IF;
rFT_401_PrevVotedValue := rVotedFreshwaterFlow_m3h;


(* -------------------------------------------------------------------------------------------------- *)
(* AUXILIARY DUAL REDUNDANT SENSORS (ST-501, LT-601, TT-701)                                          *)
(* -------------------------------------------------------------------------------------------------- *)
(* ST-501A/B Drum Torque Discrepancy (Tolerance 350 N*m) *)
IF ABS(rST_501A_DrumTorque_Nm - rST_501B_DrumTorque_Nm) > 350.0 THEN
    bST_501_DiscrepancyFault := TRUE;
    rVotedDrumTorque_Nm := MAX(rST_501A_DrumTorque_Nm, rST_501B_DrumTorque_Nm);
ELSE
    bST_501_DiscrepancyFault := FALSE;
    rVotedDrumTorque_Nm := (rST_501A_DrumTorque_Nm + rST_501B_DrumTorque_Nm) * 0.5;
END_IF;

(* LT-601A/B Cake Height Laser Discrepancy (Tolerance 35 mm) *)
IF ABS(rLT_601A_CakeHeight_mm - rLT_601B_CakeHeight_mm) > 35.0 THEN
    bLT_601_DiscrepancyFault := TRUE;
    rVotedCakeHeight_mm := (rLT_601A_CakeHeight_mm + rLT_601B_CakeHeight_mm) * 0.5;
ELSE
    bLT_601_DiscrepancyFault := FALSE;
    rVotedCakeHeight_mm := (rLT_601A_CakeHeight_mm + rLT_601B_CakeHeight_mm) * 0.5;
END_IF;

(* TT-701A/B Heat Exchanger Effluent Temperature Discrepancy (Tolerance 3.0 deg C) *)
IF ABS(rTT_701A_ExchangerEffluent_degC - rTT_701B_ExchangerEffluent_degC) > 3.0 THEN
    bTT_701_DiscrepancyFault := TRUE;
    rVotedExchangerEffluent_degC := MIN(rTT_701A_ExchangerEffluent_degC, rTT_701B_ExchangerEffluent_degC);
ELSE
    bTT_701_DiscrepancyFault := FALSE;
    rVotedExchangerEffluent_degC := (rTT_701A_ExchangerEffluent_degC + rTT_701B_ExchangerEffluent_degC) * 0.5;
END_IF;

(* Degraded Sensor Flag Calculation *)
bDegradedSensorMode := NOT (bTT_101A_Valid AND bTT_101B_Valid AND bTT_101C_Valid) OR
                       NOT (bAT_201A_Valid AND bAT_201B_Valid AND bAT_201C_Valid) OR
                       NOT (bPT_301A_Valid AND bPT_301B_Valid AND bPT_301C_Valid) OR
                       NOT (bFT_401A_Valid AND bFT_401B_Valid AND bFT_401C_Valid) OR
                       bST_501_DiscrepancyFault OR bLT_601_DiscrepancyFault OR bTT_701_DiscrepancyFault;
"""
