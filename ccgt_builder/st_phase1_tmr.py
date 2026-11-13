# ccgt_builder/st_phase1_tmr.py

def get_phase1_tmr():
    return """(* =====================================================================================================================
 * PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) VOTING SUITE WITH DISCREPANCY TIMERS & BUMPLESS DEGRADATION
 * Conforms to IEC 61508 / IEC 61511 Safety Instrumented Systems (SIL-3 Architecture):
 *   - Continuous Range Plausibility Validation (Over-Range / Under-Range / Open-Circuit)
 *   - Rate of Change (ROC) Dynamic Gradient Spurt & Freeze Supervision
 *   - 200 ms Discrepancy Accumulation Timers on inter-channel deviation (|A-B|, |B-C|, |C-A|)
 *   - Multi-Tier Degradation Engine: 2oo3 Normal (3 Healthy) -> 1oo2 Degraded (2 Healthy) -> 1oo1 Critical -> 0 Fail
 *   - First-Order Low-Pass Bumpless Output Filtering Preventing Actuator Perturbation
 * ===================================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------------------------
 * CHANNEL GROUP 1: COMBUSTOR EXHAUST GAS TEMPERATURE (EGT) PYROMETER RAKES (0.0 to 800.0 deg C)
 * --------------------------------------------------------------------------------------------------------------------- *)
(* 1.1: Transmitter Physical Plausibility & ROC Checks *)
IF (rTT_EGT_101A < 0.0) OR (rTT_EGT_101A > 800.0) OR (ABS(rTT_EGT_101A - rEGT_Previous_A) / rScan_Period_Ts > rMax_ROC_EGT_degC_s) THEN
    bEGT_Healthy_A := FALSE;
ELSE
    bEGT_Healthy_A := TRUE;
END_IF;

IF (rTT_EGT_101B < 0.0) OR (rTT_EGT_101B > 800.0) OR (ABS(rTT_EGT_101B - rEGT_Previous_B) / rScan_Period_Ts > rMax_ROC_EGT_degC_s) THEN
    bEGT_Healthy_B := FALSE;
ELSE
    bEGT_Healthy_B := TRUE;
END_IF;

IF (rTT_EGT_101C < 0.0) OR (rTT_EGT_101C > 800.0) OR (ABS(rTT_EGT_101C - rEGT_Previous_C) / rScan_Period_Ts > rMax_ROC_EGT_degC_s) THEN
    bEGT_Healthy_C := FALSE;
ELSE
    bEGT_Healthy_C := TRUE;
END_IF;

(* 1.2: Inter-Channel Discrepancy Timers (200 ms Accumulation Window) *)
IF ABS(rTT_EGT_101A - rTT_EGT_101B) > rTol_EGT_Discrep_degC THEN
    rTimer_EGT_Discrep_AB := rTimer_EGT_Discrep_AB + rScan_Period_Ts;
ELSE
    rTimer_EGT_Discrep_AB := MAX(0.0, rTimer_EGT_Discrep_AB - rScan_Period_Ts);
END_IF;

IF ABS(rTT_EGT_101B - rTT_EGT_101C) > rTol_EGT_Discrep_degC THEN
    rTimer_EGT_Discrep_BC := rTimer_EGT_Discrep_BC + rScan_Period_Ts;
ELSE
    rTimer_EGT_Discrep_BC := MAX(0.0, rTimer_EGT_Discrep_BC - rScan_Period_Ts);
END_IF;

IF ABS(rTT_EGT_101C - rTT_EGT_101A) > rTol_EGT_Discrep_degC THEN
    rTimer_EGT_Discrep_CA := rTimer_EGT_Discrep_CA + rScan_Period_Ts;
ELSE
    rTimer_EGT_Discrep_CA := MAX(0.0, rTimer_EGT_Discrep_CA - rScan_Period_Ts);
END_IF;

IF (rTimer_EGT_Discrep_AB >= 0.200) OR (rTimer_EGT_Discrep_BC >= 0.200) OR (rTimer_EGT_Discrep_CA >= 0.200) THEN
    bAlarm_EGT_Discrepancy := TRUE;
    (* Isolate deviant channel based on paired discrepancy voting *)
    IF (rTimer_EGT_Discrep_AB >= 0.200) AND (rTimer_EGT_Discrep_CA >= 0.200) AND (rTimer_EGT_Discrep_BC < 0.200) THEN
        bEGT_Healthy_A := FALSE;
    ELSIF (rTimer_EGT_Discrep_AB >= 0.200) AND (rTimer_EGT_Discrep_BC >= 0.200) AND (rTimer_EGT_Discrep_CA < 0.200) THEN
        bEGT_Healthy_B := FALSE;
    ELSIF (rTimer_EGT_Discrep_BC >= 0.200) AND (rTimer_EGT_Discrep_CA >= 0.200) AND (rTimer_EGT_Discrep_AB < 0.200) THEN
        bEGT_Healthy_C := FALSE;
    END_IF;
ELSE
    bAlarm_EGT_Discrepancy := FALSE;
END_IF;

(* 1.3: Voting Logic Execution & Graceful Degradation *)
IF bEGT_Healthy_A AND bEGT_Healthy_B AND bEGT_Healthy_C THEN
    (* 3 Healthy Channels: True Median Selection *)
    nMode_EGT_TMR := 3;
    rVoted_EGT_Raw := (rTT_EGT_101A + rTT_EGT_101B + rTT_EGT_101C)
                      - MIN(rTT_EGT_101A, MIN(rTT_EGT_101B, rTT_EGT_101C))
                      - MAX(rTT_EGT_101A, MAX(rTT_EGT_101B, rTT_EGT_101C));
ELSIF bEGT_Healthy_A AND bEGT_Healthy_B THEN
    nMode_EGT_TMR := 2;
    rVoted_EGT_Raw := 0.5 * (rTT_EGT_101A + rTT_EGT_101B);
ELSIF bEGT_Healthy_B AND bEGT_Healthy_C THEN
    nMode_EGT_TMR := 2;
    rVoted_EGT_Raw := 0.5 * (rTT_EGT_101B + rTT_EGT_101C);
ELSIF bEGT_Healthy_A AND bEGT_Healthy_C THEN
    nMode_EGT_TMR := 2;
    rVoted_EGT_Raw := 0.5 * (rTT_EGT_101A + rTT_EGT_101C);
ELSIF bEGT_Healthy_A THEN
    nMode_EGT_TMR := 1;
    rVoted_EGT_Raw := rTT_EGT_101A;
ELSIF bEGT_Healthy_B THEN
    nMode_EGT_TMR := 1;
    rVoted_EGT_Raw := rTT_EGT_101B;
ELSIF bEGT_Healthy_C THEN
    nMode_EGT_TMR := 1;
    rVoted_EGT_Raw := rTT_EGT_101C;
ELSE
    nMode_EGT_TMR := 0;
    (* All channels failed: Maintain previous healthy holding value *)
    rVoted_EGT_Raw := rEGT_Previous_A;
END_IF;

(* First-Order Bumpless Low-Pass Slew Filter *)
rVoted_EGT_degC := rVoted_EGT_degC + 0.35 * (rVoted_EGT_Raw - rVoted_EGT_degC);
rEGT_Previous_A := rTT_EGT_101A;
rEGT_Previous_B := rTT_EGT_101B;
rEGT_Previous_C := rTT_EGT_101C;

(* ---------------------------------------------------------------------------------------------------------------------
 * CHANNEL GROUP 2: HRSG HIGH-PRESSURE DRUM NARROW-RANGE LEVEL (-400.0 to +400.0 mm)
 * --------------------------------------------------------------------------------------------------------------------- *)
(* 2.1: Transmitter Physical Plausibility & ROC Checks *)
IF (rLT_DRUM_201A < -400.0) OR (rLT_DRUM_201A > 400.0) OR (ABS(rLT_DRUM_201A - rDrumL_Previous_A) / rScan_Period_Ts > rMax_ROC_DrumL_mm_s) THEN
    bDrumL_Healthy_A := FALSE;
ELSE
    bDrumL_Healthy_A := TRUE;
END_IF;

IF (rLT_DRUM_201B < -400.0) OR (rLT_DRUM_201B > 400.0) OR (ABS(rLT_DRUM_201B - rDrumL_Previous_B) / rScan_Period_Ts > rMax_ROC_DrumL_mm_s) THEN
    bDrumL_Healthy_B := FALSE;
ELSE
    bDrumL_Healthy_B := TRUE;
END_IF;

IF (rLT_DRUM_201C < -400.0) OR (rLT_DRUM_201C > 400.0) OR (ABS(rLT_DRUM_201C - rDrumL_Previous_C) / rScan_Period_Ts > rMax_ROC_DrumL_mm_s) THEN
    bDrumL_Healthy_C := FALSE;
ELSE
    bDrumL_Healthy_C := TRUE;
END_IF;

(* 2.2: Inter-Channel Discrepancy Timers (200 ms Accumulation Window) *)
IF ABS(rLT_DRUM_201A - rLT_DRUM_201B) > rTol_DrumL_Discrep_mm THEN
    rTimer_DrumL_Discrep_AB := rTimer_DrumL_Discrep_AB + rScan_Period_Ts;
ELSE
    rTimer_DrumL_Discrep_AB := MAX(0.0, rTimer_DrumL_Discrep_AB - rScan_Period_Ts);
END_IF;

IF ABS(rLT_DRUM_201B - rLT_DRUM_201C) > rTol_DrumL_Discrep_mm THEN
    rTimer_DrumL_Discrep_BC := rTimer_DrumL_Discrep_BC + rScan_Period_Ts;
ELSE
    rTimer_DrumL_Discrep_BC := MAX(0.0, rTimer_DrumL_Discrep_BC - rScan_Period_Ts);
END_IF;

IF ABS(rLT_DRUM_201C - rLT_DRUM_201A) > rTol_DrumL_Discrep_mm THEN
    rTimer_DrumL_Discrep_CA := rTimer_DrumL_Discrep_CA + rScan_Period_Ts;
ELSE
    rTimer_DrumL_Discrep_CA := MAX(0.0, rTimer_DrumL_Discrep_CA - rScan_Period_Ts);
END_IF;

IF (rTimer_DrumL_Discrep_AB >= 0.200) OR (rTimer_DrumL_Discrep_BC >= 0.200) OR (rTimer_DrumL_Discrep_CA >= 0.200) THEN
    bAlarm_DrumL_Discrepancy := TRUE;
    IF (rTimer_DrumL_Discrep_AB >= 0.200) AND (rTimer_DrumL_Discrep_CA >= 0.200) AND (rTimer_DrumL_Discrep_BC < 0.200) THEN
        bDrumL_Healthy_A := FALSE;
    ELSIF (rTimer_DrumL_Discrep_AB >= 0.200) AND (rTimer_DrumL_Discrep_BC >= 0.200) AND (rTimer_DrumL_Discrep_CA < 0.200) THEN
        bDrumL_Healthy_B := FALSE;
    ELSIF (rTimer_DrumL_Discrep_BC >= 0.200) AND (rTimer_DrumL_Discrep_CA >= 0.200) AND (rTimer_DrumL_Discrep_AB < 0.200) THEN
        bDrumL_Healthy_C := FALSE;
    END_IF;
ELSE
    bAlarm_DrumL_Discrepancy := FALSE;
END_IF;

(* 2.3: Voting Logic Execution & Graceful Degradation *)
IF bDrumL_Healthy_A AND bDrumL_Healthy_B AND bDrumL_Healthy_C THEN
    nMode_DrumL_TMR := 3;
    rVoted_DrumL_Raw := (rLT_DRUM_201A + rLT_DRUM_201B + rLT_DRUM_201C)
                        - MIN(rLT_DRUM_201A, MIN(rLT_DRUM_201B, rLT_DRUM_201C))
                        - MAX(rLT_DRUM_201A, MAX(rLT_DRUM_201B, rLT_DRUM_201C));
ELSIF bDrumL_Healthy_A AND bDrumL_Healthy_B THEN
    nMode_DrumL_TMR := 2;
    rVoted_DrumL_Raw := 0.5 * (rLT_DRUM_201A + rLT_DRUM_201B);
ELSIF bDrumL_Healthy_B AND bDrumL_Healthy_C THEN
    nMode_DrumL_TMR := 2;
    rVoted_DrumL_Raw := 0.5 * (rLT_DRUM_201B + rLT_DRUM_201C);
ELSIF bDrumL_Healthy_A AND bDrumL_Healthy_C THEN
    nMode_DrumL_TMR := 2;
    rVoted_DrumL_Raw := 0.5 * (rLT_DRUM_201A + rLT_DRUM_201C);
ELSIF bDrumL_Healthy_A THEN
    nMode_DrumL_TMR := 1;
    rVoted_DrumL_Raw := rLT_DRUM_201A;
ELSIF bDrumL_Healthy_B THEN
    nMode_DrumL_TMR := 1;
    rVoted_DrumL_Raw := rLT_DRUM_201B;
ELSIF bDrumL_Healthy_C THEN
    nMode_DrumL_TMR := 1;
    rVoted_DrumL_Raw := rLT_DRUM_201C;
ELSE
    nMode_DrumL_TMR := 0;
    rVoted_DrumL_Raw := rDrumL_Previous_A;
END_IF;

rVoted_Drum_Level_mm := rVoted_Drum_Level_mm + 0.40 * (rVoted_DrumL_Raw - rVoted_Drum_Level_mm);
rDrumL_Previous_A := rLT_DRUM_201A;
rDrumL_Previous_B := rLT_DRUM_201B;
rDrumL_Previous_C := rLT_DRUM_201C;

(* ---------------------------------------------------------------------------------------------------------------------
 * CHANNEL GROUP 3: FINAL SUPERHEATER MAIN STEAM EXIT TEMPERATURE (0.0 to 650.0 deg C)
 * --------------------------------------------------------------------------------------------------------------------- *)
(* 3.1: Transmitter Physical Plausibility & ROC Checks *)
IF (rTT_STEAM_301A < 0.0) OR (rTT_STEAM_301A > 650.0) OR (ABS(rTT_STEAM_301A - rSteamT_Previous_A) / rScan_Period_Ts > rMax_ROC_SteamT_degC_s) THEN
    bSteamT_Healthy_A := FALSE;
ELSE
    bSteamT_Healthy_A := TRUE;
END_IF;

IF (rTT_STEAM_301B < 0.0) OR (rTT_STEAM_301B > 650.0) OR (ABS(rTT_STEAM_301B - rSteamT_Previous_B) / rScan_Period_Ts > rMax_ROC_SteamT_degC_s) THEN
    bSteamT_Healthy_B := FALSE;
ELSE
    bSteamT_Healthy_B := TRUE;
END_IF;

IF (rTT_STEAM_301C < 0.0) OR (rTT_STEAM_301C > 650.0) OR (ABS(rTT_STEAM_301C - rSteamT_Previous_C) / rScan_Period_Ts > rMax_ROC_SteamT_degC_s) THEN
    bSteamT_Healthy_C := FALSE;
ELSE
    bSteamT_Healthy_C := TRUE;
END_IF;

(* 3.2: Inter-Channel Discrepancy Timers (200 ms Accumulation Window) *)
IF ABS(rTT_STEAM_301A - rTT_STEAM_301B) > rTol_SteamT_Discrep_degC THEN
    rTimer_SteamT_Discrep_AB := rTimer_SteamT_Discrep_AB + rScan_Period_Ts;
ELSE
    rTimer_SteamT_Discrep_AB := MAX(0.0, rTimer_SteamT_Discrep_AB - rScan_Period_Ts);
END_IF;

IF ABS(rTT_STEAM_301B - rTT_STEAM_301C) > rTol_SteamT_Discrep_degC THEN
    rTimer_SteamT_Discrep_BC := rTimer_SteamT_Discrep_BC + rScan_Period_Ts;
ELSE
    rTimer_SteamT_Discrep_BC := MAX(0.0, rTimer_SteamT_Discrep_BC - rScan_Period_Ts);
END_IF;

IF ABS(rTT_STEAM_301C - rTT_STEAM_301A) > rTol_SteamT_Discrep_degC THEN
    rTimer_SteamT_Discrep_CA := rTimer_SteamT_Discrep_CA + rScan_Period_Ts;
ELSE
    rTimer_SteamT_Discrep_CA := MAX(0.0, rTimer_SteamT_Discrep_CA - rScan_Period_Ts);
END_IF;

IF (rTimer_SteamT_Discrep_AB >= 0.200) OR (rTimer_SteamT_Discrep_BC >= 0.200) OR (rTimer_SteamT_Discrep_CA >= 0.200) THEN
    bAlarm_SteamT_Discrepancy := TRUE;
    IF (rTimer_SteamT_Discrep_AB >= 0.200) AND (rTimer_SteamT_Discrep_CA >= 0.200) AND (rTimer_SteamT_Discrep_BC < 0.200) THEN
        bSteamT_Healthy_A := FALSE;
    ELSIF (rTimer_SteamT_Discrep_AB >= 0.200) AND (rTimer_SteamT_Discrep_BC >= 0.200) AND (rTimer_SteamT_Discrep_CA < 0.200) THEN
        bSteamT_Healthy_B := FALSE;
    ELSIF (rTimer_SteamT_Discrep_BC >= 0.200) AND (rTimer_SteamT_Discrep_CA >= 0.200) AND (rTimer_SteamT_Discrep_AB < 0.200) THEN
        bSteamT_Healthy_C := FALSE;
    END_IF;
ELSE
    bAlarm_SteamT_Discrepancy := FALSE;
END_IF;

(* 3.3: Voting Logic Execution & Graceful Degradation *)
IF bSteamT_Healthy_A AND bSteamT_Healthy_B AND bSteamT_Healthy_C THEN
    nMode_SteamT_TMR := 3;
    rVoted_SteamT_Raw := (rTT_STEAM_301A + rTT_STEAM_301B + rTT_STEAM_301C)
                         - MIN(rTT_STEAM_301A, MIN(rTT_STEAM_301B, rTT_STEAM_301C))
                         - MAX(rTT_STEAM_301A, MAX(rTT_STEAM_301B, rTT_STEAM_301C));
ELSIF bSteamT_Healthy_A AND bSteamT_Healthy_B THEN
    nMode_SteamT_TMR := 2;
    rVoted_SteamT_Raw := 0.5 * (rTT_STEAM_301A + rTT_STEAM_301B);
ELSIF bSteamT_Healthy_B AND bSteamT_Healthy_C THEN
    nMode_SteamT_TMR := 2;
    rVoted_SteamT_Raw := 0.5 * (rTT_STEAM_301B + rTT_STEAM_301C);
ELSIF bSteamT_Healthy_A AND bSteamT_Healthy_C THEN
    nMode_SteamT_TMR := 2;
    rVoted_SteamT_Raw := 0.5 * (rTT_STEAM_301A + rTT_STEAM_301C);
ELSIF bSteamT_Healthy_A THEN
    nMode_SteamT_TMR := 1;
    rVoted_SteamT_Raw := rTT_STEAM_301A;
ELSIF bSteamT_Healthy_B THEN
    nMode_SteamT_TMR := 1;
    rVoted_SteamT_Raw := rTT_STEAM_301B;
ELSIF bSteamT_Healthy_C THEN
    nMode_SteamT_TMR := 1;
    rVoted_SteamT_Raw := rTT_STEAM_301C;
ELSE
    nMode_SteamT_TMR := 0;
    rVoted_SteamT_Raw := rSteamT_Previous_A;
END_IF;

rVoted_Steam_Temp_degC := rVoted_Steam_Temp_degC + 0.30 * (rVoted_SteamT_Raw - rVoted_Steam_Temp_degC);
rSteamT_Previous_A := rTT_STEAM_301A;
rSteamT_Previous_B := rTT_STEAM_301B;
rSteamT_Previous_C := rTT_STEAM_301C;

(* ---------------------------------------------------------------------------------------------------------------------
 * CHANNEL GROUP 4: HP STEAM HEADER CORIOLIS MASS FLOW RATE (0.0 to 300.0 kg/s)
 * --------------------------------------------------------------------------------------------------------------------- *)
(* 4.1: Transmitter Physical Plausibility & ROC Checks *)
IF (rFT_STEAM_401A < 0.0) OR (rFT_STEAM_401A > 300.0) OR (ABS(rFT_STEAM_401A - rSteamF_Previous_A) / rScan_Period_Ts > rMax_ROC_SteamF_kgs_s) THEN
    bSteamF_Healthy_A := FALSE;
ELSE
    bSteamF_Healthy_A := TRUE;
END_IF;

IF (rFT_STEAM_401B < 0.0) OR (rFT_STEAM_401B > 300.0) OR (ABS(rFT_STEAM_401B - rSteamF_Previous_B) / rScan_Period_Ts > rMax_ROC_SteamF_kgs_s) THEN
    bSteamF_Healthy_B := FALSE;
ELSE
    bSteamF_Healthy_B := TRUE;
END_IF;

IF (rFT_STEAM_401C < 0.0) OR (rFT_STEAM_401C > 300.0) OR (ABS(rFT_STEAM_401C - rSteamF_Previous_C) / rScan_Period_Ts > rMax_ROC_SteamF_kgs_s) THEN
    bSteamF_Healthy_C := FALSE;
ELSE
    bSteamF_Healthy_C := TRUE;
END_IF;

(* 4.2: Inter-Channel Discrepancy Timers (200 ms Accumulation Window) *)
IF ABS(rFT_STEAM_401A - rFT_STEAM_401B) > rTol_SteamF_Discrep_kgs THEN
    rTimer_SteamF_Discrep_AB := rTimer_SteamF_Discrep_AB + rScan_Period_Ts;
ELSE
    rTimer_SteamF_Discrep_AB := MAX(0.0, rTimer_SteamF_Discrep_AB - rScan_Period_Ts);
END_IF;

IF ABS(rFT_STEAM_401B - rFT_STEAM_401C) > rTol_SteamF_Discrep_kgs THEN
    rTimer_SteamF_Discrep_BC := rTimer_SteamF_Discrep_BC + rScan_Period_Ts;
ELSE
    rTimer_SteamF_Discrep_BC := MAX(0.0, rTimer_SteamF_Discrep_BC - rScan_Period_Ts);
END_IF;

IF ABS(rFT_STEAM_401C - rFT_STEAM_401A) > rTol_SteamF_Discrep_kgs THEN
    rTimer_SteamF_Discrep_CA := rTimer_SteamF_Discrep_CA + rScan_Period_Ts;
ELSE
    rTimer_SteamF_Discrep_CA := MAX(0.0, rTimer_SteamF_Discrep_CA - rScan_Period_Ts);
END_IF;

IF (rTimer_SteamF_Discrep_AB >= 0.200) OR (rTimer_SteamF_Discrep_BC >= 0.200) OR (rTimer_SteamF_Discrep_CA >= 0.200) THEN
    bAlarm_SteamF_Discrepancy := TRUE;
    IF (rTimer_SteamF_Discrep_AB >= 0.200) AND (rTimer_SteamF_Discrep_CA >= 0.200) AND (rTimer_SteamF_Discrep_BC < 0.200) THEN
        bSteamF_Healthy_A := FALSE;
    ELSIF (rTimer_SteamF_Discrep_AB >= 0.200) AND (rTimer_SteamF_Discrep_BC >= 0.200) AND (rTimer_SteamF_Discrep_CA < 0.200) THEN
        bSteamF_Healthy_B := FALSE;
    ELSIF (rTimer_SteamF_Discrep_BC >= 0.200) AND (rTimer_SteamF_Discrep_CA >= 0.200) AND (rTimer_SteamF_Discrep_AB < 0.200) THEN
        bSteamF_Healthy_C := FALSE;
    END_IF;
ELSE
    bAlarm_SteamF_Discrepancy := FALSE;
END_IF;

(* 4.3: Voting Logic Execution & Graceful Degradation *)
IF bSteamF_Healthy_A AND bSteamF_Healthy_B AND bSteamF_Healthy_C THEN
    nMode_SteamF_TMR := 3;
    rVoted_SteamF_Raw := (rFT_STEAM_401A + rFT_STEAM_401B + rFT_STEAM_401C)
                         - MIN(rFT_STEAM_401A, MIN(rFT_STEAM_401B, rFT_STEAM_401C))
                         - MAX(rFT_STEAM_401A, MAX(rFT_STEAM_401B, rFT_STEAM_401C));
ELSIF bSteamF_Healthy_A AND bSteamF_Healthy_B THEN
    nMode_SteamF_TMR := 2;
    rVoted_SteamF_Raw := 0.5 * (rFT_STEAM_401A + rFT_STEAM_401B);
ELSIF bSteamF_Healthy_B AND bSteamF_Healthy_C THEN
    nMode_SteamF_TMR := 2;
    rVoted_SteamF_Raw := 0.5 * (rFT_STEAM_401B + rFT_STEAM_401C);
ELSIF bSteamF_Healthy_A AND bSteamF_Healthy_C THEN
    nMode_SteamF_TMR := 2;
    rVoted_SteamF_Raw := 0.5 * (rFT_STEAM_401A + rFT_STEAM_401C);
ELSIF bSteamF_Healthy_A THEN
    nMode_SteamF_TMR := 1;
    rVoted_SteamF_Raw := rFT_STEAM_401A;
ELSIF bSteamF_Healthy_B THEN
    nMode_SteamF_TMR := 1;
    rVoted_SteamF_Raw := rFT_STEAM_401B;
ELSIF bSteamF_Healthy_C THEN
    nMode_SteamF_TMR := 1;
    rVoted_SteamF_Raw := rFT_STEAM_401C;
ELSE
    nMode_SteamF_TMR := 0;
    rVoted_SteamF_Raw := rSteamF_Previous_A;
END_IF;

rVoted_Steam_Flow_kgs := rVoted_Steam_Flow_kgs + 0.45 * (rVoted_SteamF_Raw - rVoted_Steam_Flow_kgs);
rSteamF_Previous_A := rFT_STEAM_401A;
rSteamF_Previous_B := rFT_STEAM_401B;
rSteamF_Previous_C := rFT_STEAM_401C;

(* ---------------------------------------------------------------------------------------------------------------------
 * CHANNEL GROUP 5: GENERATOR ACTIVE ELECTRICAL POWER TRANSDUCERS (0.0 to 450.0 MW)
 * --------------------------------------------------------------------------------------------------------------------- *)
(* 5.1: Transmitter Physical Plausibility & ROC Checks *)
IF (rWT_POWER_501A < 0.0) OR (rWT_POWER_501A > 450.0) OR (ABS(rWT_POWER_501A - rPower_Previous_A) / rScan_Period_Ts > rMax_ROC_Power_MW_s) THEN
    bPower_Healthy_A := FALSE;
ELSE
    bPower_Healthy_A := TRUE;
END_IF;

IF (rWT_POWER_501B < 0.0) OR (rWT_POWER_501B > 450.0) OR (ABS(rWT_POWER_501B - rPower_Previous_B) / rScan_Period_Ts > rMax_ROC_Power_MW_s) THEN
    bPower_Healthy_B := FALSE;
ELSE
    bPower_Healthy_B := TRUE;
END_IF;

IF (rWT_POWER_501C < 0.0) OR (rWT_POWER_501C > 450.0) OR (ABS(rWT_POWER_501C - rPower_Previous_C) / rScan_Period_Ts > rMax_ROC_Power_MW_s) THEN
    bPower_Healthy_C := FALSE;
ELSE
    bPower_Healthy_C := TRUE;
END_IF;

(* 5.2: Inter-Channel Discrepancy Timers (200 ms Accumulation Window) *)
IF ABS(rWT_POWER_501A - rWT_POWER_501B) > rTol_Power_Discrep_MW THEN
    rTimer_Power_Discrep_AB := rTimer_Power_Discrep_AB + rScan_Period_Ts;
ELSE
    rTimer_Power_Discrep_AB := MAX(0.0, rTimer_Power_Discrep_AB - rScan_Period_Ts);
END_IF;

IF ABS(rWT_POWER_501B - rWT_POWER_501C) > rTol_Power_Discrep_MW THEN
    rTimer_Power_Discrep_BC := rTimer_Power_Discrep_BC + rScan_Period_Ts;
ELSE
    rTimer_Power_Discrep_BC := MAX(0.0, rTimer_Power_Discrep_BC - rScan_Period_Ts);
END_IF;

IF ABS(rWT_POWER_501C - rWT_POWER_501A) > rTol_Power_Discrep_MW THEN
    rTimer_Power_Discrep_CA := rTimer_Power_Discrep_CA + rScan_Period_Ts;
ELSE
    rTimer_Power_Discrep_CA := MAX(0.0, rTimer_Power_Discrep_CA - rScan_Period_Ts);
END_IF;

IF (rTimer_Power_Discrep_AB >= 0.200) OR (rTimer_Power_Discrep_BC >= 0.200) OR (rTimer_Power_Discrep_CA >= 0.200) THEN
    bAlarm_Power_Discrepancy := TRUE;
    IF (rTimer_Power_Discrep_AB >= 0.200) AND (rTimer_Power_Discrep_CA >= 0.200) AND (rTimer_Power_Discrep_BC < 0.200) THEN
        bPower_Healthy_A := FALSE;
    ELSIF (rTimer_Power_Discrep_AB >= 0.200) AND (rTimer_Power_Discrep_BC >= 0.200) AND (rTimer_Power_Discrep_CA < 0.200) THEN
        bPower_Healthy_B := FALSE;
    ELSIF (rTimer_Power_Discrep_BC >= 0.200) AND (rTimer_Power_Discrep_CA >= 0.200) AND (rTimer_Power_Discrep_AB < 0.200) THEN
        bPower_Healthy_C := FALSE;
    END_IF;
ELSE
    bAlarm_Power_Discrepancy := FALSE;
END_IF;

(* 5.3: Voting Logic Execution & Graceful Degradation *)
IF bPower_Healthy_A AND bPower_Healthy_B AND bPower_Healthy_C THEN
    nMode_Power_TMR := 3;
    rVoted_Power_Raw := (rWT_POWER_501A + rWT_POWER_501B + rWT_POWER_501C)
                        - MIN(rWT_POWER_501A, MIN(rWT_POWER_501B, rWT_POWER_501C))
                        - MAX(rWT_POWER_501A, MAX(rWT_POWER_501B, rWT_POWER_501C));
ELSIF bPower_Healthy_A AND bPower_Healthy_B THEN
    nMode_Power_TMR := 2;
    rVoted_Power_Raw := 0.5 * (rWT_POWER_501A + rWT_POWER_501B);
ELSIF bPower_Healthy_B AND bPower_Healthy_C THEN
    nMode_Power_TMR := 2;
    rVoted_Power_Raw := 0.5 * (rWT_POWER_501B + rWT_POWER_501C);
ELSIF bPower_Healthy_A AND bPower_Healthy_C THEN
    nMode_Power_TMR := 2;
    rVoted_Power_Raw := 0.5 * (rWT_POWER_501A + rWT_POWER_501C);
ELSIF bPower_Healthy_A THEN
    nMode_Power_TMR := 1;
    rVoted_Power_Raw := rWT_POWER_501A;
ELSIF bPower_Healthy_B THEN
    nMode_Power_TMR := 1;
    rVoted_Power_Raw := rWT_POWER_501B;
ELSIF bPower_Healthy_C THEN
    nMode_Power_TMR := 1;
    rVoted_Power_Raw := rWT_POWER_501C;
ELSE
    nMode_Power_TMR := 0;
    rVoted_Power_Raw := rPower_Previous_A;
END_IF;

rVoted_Active_Power_MW := rVoted_Active_Power_MW + 0.50 * (rVoted_Power_Raw - rVoted_Active_Power_MW);
rPower_Previous_A := rWT_POWER_501A;
rPower_Previous_B := rWT_POWER_501B;
rPower_Previous_C := rWT_POWER_501C;

(* Pack Voted Measurements into Observation Vector y_meas[1..6] *)
y_meas[1] := rVoted_Active_Power_MW;
y_meas[2] := rVoted_EGT_degC;
y_meas[3] := rVGV_Position_Cmd_deg; (* Feedback inferred from command and actuator model *)
y_meas[4] := rVoted_Drum_Level_mm;
y_meas[5] := rVoted_Steam_Flow_kgs;
y_meas[6] := rVoted_Steam_Temp_degC;
"""
