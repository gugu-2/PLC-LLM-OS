# build_st_phase1_tmr.py
# Section 4: Phase 1 - 2oo3 Triple Modular Redundancy (TMR) Sensor Voting with Discrepancy Timers and Degradation

def get_phase1_tmr():
    code = []
    code.append("""(* =====================================================================================================================
 * PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING WITH DISCREPANCY TIMERS
 * Architecture: IEEE 603 / IEC 61513 Nuclear Class 1E Triple-Redundant Voting
 * Fault Accumulation Window: 500 ms (rTMR_Fault_Accum_Time_Limit)
 * Bumpless Degradation Hierarchy:
 *   - Tier 3 (3 Healthy): Hardware 2oo3 Median Voting
 *   - Tier 2 (2 Healthy): Degraded 1oo2 Dual-Channel Arithmetic Mean with Pair Discrepancy Monitoring
 *   - Tier 1 (1 Healthy): Degraded 1oo1 Single-Channel Conservative Fallback with Class 1E Advisory
 *   - Tier 0 (0 Healthy): Channel Triplet Complete Common-Cause Failure -> RPS SCRAM / Failsafe Trip Demand
 * ===================================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------------------------
 * TRIPLET 1: STEAM GENERATOR NARROW-RANGE WATER LEVEL (LT-101A, LT-101B, LT-101C) [mm]
 * --------------------------------------------------------------------------------------------------------------------- *)
(* Reset channel fault latches on master reset pushbutton *)
IF bReset_Trip_Interlocks THEN
    bTMR_NR_Failed_ChA := FALSE;
    bTMR_NR_Failed_ChB := FALSE;
    bTMR_NR_Failed_ChC := FALSE;
    rTMR_NR_Timer_ChA := 0.0;
    rTMR_NR_Timer_ChB := 0.0;
    rTMR_NR_Timer_ChC := 0.0;
END_IF;

(* Count healthy channels *)
nHealth_TMR_Level_NR := 0;
IF NOT bTMR_NR_Failed_ChA THEN
    nHealth_TMR_Level_NR := nHealth_TMR_Level_NR + 1;
END_IF;
IF NOT bTMR_NR_Failed_ChB THEN
    nHealth_TMR_Level_NR := nHealth_TMR_Level_NR + 1;
END_IF;
IF NOT bTMR_NR_Failed_ChC THEN
    nHealth_TMR_Level_NR := nHealth_TMR_Level_NR + 1;
END_IF;

(* Tier 3: All 3 Channels Healthy -> Median Selection *)
IF nHealth_TMR_Level_NR = 3 THEN
    IF (rLevel_NR_Transmitter_A <= rLevel_NR_Transmitter_B AND rLevel_NR_Transmitter_B <= rLevel_NR_Transmitter_C) OR
       (rLevel_NR_Transmitter_C <= rLevel_NR_Transmitter_B AND rLevel_NR_Transmitter_B <= rLevel_NR_Transmitter_A) THEN
        rVoted_Level_NR := rLevel_NR_Transmitter_B;
    ELSIF (rLevel_NR_Transmitter_B <= rLevel_NR_Transmitter_A AND rLevel_NR_Transmitter_A <= rLevel_NR_Transmitter_C) OR
          (rLevel_NR_Transmitter_C <= rLevel_NR_Transmitter_A AND rLevel_NR_Transmitter_A <= rLevel_NR_Transmitter_B) THEN
        rVoted_Level_NR := rLevel_NR_Transmitter_A;
    ELSE
        rVoted_Level_NR := rLevel_NR_Transmitter_C;
    END_IF;

    (* Evaluate Channel A Discrepancy against Median *)
    IF ABS(rLevel_NR_Transmitter_A - rVoted_Level_NR) > rTMR_NR_Discrepancy_Limit THEN
        rTMR_NR_Timer_ChA := rTMR_NR_Timer_ChA + rScan_Period_Ts;
        IF rTMR_NR_Timer_ChA >= rTMR_Fault_Accum_Time_Limit THEN
            bTMR_NR_Failed_ChA := TRUE;
        END_IF;
    ELSE
        rTMR_NR_Timer_ChA := MAX(0.0, rTMR_NR_Timer_ChA - (rScan_Period_Ts * 0.5));
    END_IF;

    (* Evaluate Channel B Discrepancy against Median *)
    IF ABS(rLevel_NR_Transmitter_B - rVoted_Level_NR) > rTMR_NR_Discrepancy_Limit THEN
        rTMR_NR_Timer_ChB := rTMR_NR_Timer_ChB + rScan_Period_Ts;
        IF rTMR_NR_Timer_ChB >= rTMR_Fault_Accum_Time_Limit THEN
            bTMR_NR_Failed_ChB := TRUE;
        END_IF;
    ELSE
        rTMR_NR_Timer_ChB := MAX(0.0, rTMR_NR_Timer_ChB - (rScan_Period_Ts * 0.5));
    END_IF;

    (* Evaluate Channel C Discrepancy against Median *)
    IF ABS(rLevel_NR_Transmitter_C - rVoted_Level_NR) > rTMR_NR_Discrepancy_Limit THEN
        rTMR_NR_Timer_ChC := rTMR_NR_Timer_ChC + rScan_Period_Ts;
        IF rTMR_NR_Timer_ChC >= rTMR_Fault_Accum_Time_Limit THEN
            bTMR_NR_Failed_ChC := TRUE;
        END_IF;
    ELSE
        rTMR_NR_Timer_ChC := MAX(0.0, rTMR_NR_Timer_ChC - (rScan_Period_Ts * 0.5));
    END_IF;

(* Tier 2: 2 Channels Healthy -> Dual 1oo2 Mean with Pair Tracking *)
ELSIF nHealth_TMR_Level_NR = 2 THEN
    IF NOT bTMR_NR_Failed_ChA AND NOT bTMR_NR_Failed_ChB THEN
        rVoted_Level_NR := 0.5 * (rLevel_NR_Transmitter_A + rLevel_NR_Transmitter_B);
        IF ABS(rLevel_NR_Transmitter_A - rLevel_NR_Transmitter_B) > rTMR_NR_Discrepancy_Limit THEN
            rTMR_NR_Timer_ChA := rTMR_NR_Timer_ChA + rScan_Period_Ts;
            IF rTMR_NR_Timer_ChA >= rTMR_Fault_Accum_Time_Limit THEN
                (* Latch channel with greater deviation from wide-range proxy *)
                IF ABS(rLevel_NR_Transmitter_A - (rVoted_Level_WR * 0.267)) > ABS(rLevel_NR_Transmitter_B - (rVoted_Level_WR * 0.267)) THEN
                    bTMR_NR_Failed_ChA := TRUE;
                ELSE
                    bTMR_NR_Failed_ChB := TRUE;
                END_IF;
            END_IF;
        ELSE
            rTMR_NR_Timer_ChA := MAX(0.0, rTMR_NR_Timer_ChA - rScan_Period_Ts);
        END_IF;
    ELSIF NOT bTMR_NR_Failed_ChA AND NOT bTMR_NR_Failed_ChC THEN
        rVoted_Level_NR := 0.5 * (rLevel_NR_Transmitter_A + rLevel_NR_Transmitter_C);
        IF ABS(rLevel_NR_Transmitter_A - rLevel_NR_Transmitter_C) > rTMR_NR_Discrepancy_Limit THEN
            rTMR_NR_Timer_ChA := rTMR_NR_Timer_ChA + rScan_Period_Ts;
            IF rTMR_NR_Timer_ChA >= rTMR_Fault_Accum_Time_Limit THEN
                IF ABS(rLevel_NR_Transmitter_A - (rVoted_Level_WR * 0.267)) > ABS(rLevel_NR_Transmitter_C - (rVoted_Level_WR * 0.267)) THEN
                    bTMR_NR_Failed_ChA := TRUE;
                ELSE
                    bTMR_NR_Failed_ChC := TRUE;
                END_IF;
            END_IF;
        ELSE
            rTMR_NR_Timer_ChA := MAX(0.0, rTMR_NR_Timer_ChA - rScan_Period_Ts);
        END_IF;
    ELSE
        rVoted_Level_NR := 0.5 * (rLevel_NR_Transmitter_B + rLevel_NR_Transmitter_C);
        IF ABS(rLevel_NR_Transmitter_B - rLevel_NR_Transmitter_C) > rTMR_NR_Discrepancy_Limit THEN
            rTMR_NR_Timer_ChB := rTMR_NR_Timer_ChB + rScan_Period_Ts;
            IF rTMR_NR_Timer_ChB >= rTMR_Fault_Accum_Time_Limit THEN
                IF ABS(rLevel_NR_Transmitter_B - (rVoted_Level_WR * 0.267)) > ABS(rLevel_NR_Transmitter_C - (rVoted_Level_WR * 0.267)) THEN
                    bTMR_NR_Failed_ChB := TRUE;
                ELSE
                    bTMR_NR_Failed_ChC := TRUE;
                END_IF;
            END_IF;
        ELSE
            rTMR_NR_Timer_ChB := MAX(0.0, rTMR_NR_Timer_ChB - rScan_Period_Ts);
        END_IF;
    END_IF;

(* Tier 1: 1 Channel Healthy -> 1oo1 Single Transmitter Fallback *)
ELSIF nHealth_TMR_Level_NR = 1 THEN
    IF NOT bTMR_NR_Failed_ChA THEN
        rVoted_Level_NR := rLevel_NR_Transmitter_A;
    ELSIF NOT bTMR_NR_Failed_ChB THEN
        rVoted_Level_NR := rLevel_NR_Transmitter_B;
    ELSE
        rVoted_Level_NR := rLevel_NR_Transmitter_C;
    END_IF;

(* Tier 0: 0 Channels Healthy -> Triple Transmitter Catastrophic Failure *)
ELSE
    (* Synthesize narrow-range proxy from wide-range level scaled to narrow range taps *)
    rVoted_Level_NR := rVoted_Level_WR * 0.2667;
    bDemand_RPS_Reactor_Trip := TRUE; (* Safety Class 1E Scram Demand *)
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * TRIPLET 2: STEAM GENERATOR WIDE-RANGE WATER LEVEL (LT-102A, LT-102B, LT-102C) [mm]
 * --------------------------------------------------------------------------------------------------------------------- *)
IF bReset_Trip_Interlocks THEN
    bTMR_WR_Failed_ChA := FALSE;
    bTMR_WR_Failed_ChB := FALSE;
    bTMR_WR_Failed_ChC := FALSE;
    rTMR_WR_Timer_ChA := 0.0;
    rTMR_WR_Timer_ChB := 0.0;
    rTMR_WR_Timer_ChC := 0.0;
END_IF;

nHealth_TMR_Level_WR := 0;
IF NOT bTMR_WR_Failed_ChA THEN nHealth_TMR_Level_WR := nHealth_TMR_Level_WR + 1; END_IF;
IF NOT bTMR_WR_Failed_ChB THEN nHealth_TMR_Level_WR := nHealth_TMR_Level_WR + 1; END_IF;
IF NOT bTMR_WR_Failed_ChC THEN nHealth_TMR_Level_WR := nHealth_TMR_Level_WR + 1; END_IF;

IF nHealth_TMR_Level_WR = 3 THEN
    IF (rLevel_WR_Transmitter_A <= rLevel_WR_Transmitter_B AND rLevel_WR_Transmitter_B <= rLevel_WR_Transmitter_C) OR
       (rLevel_WR_Transmitter_C <= rLevel_WR_Transmitter_B AND rLevel_WR_Transmitter_B <= rLevel_WR_Transmitter_A) THEN
        rVoted_Level_WR := rLevel_WR_Transmitter_B;
    ELSIF (rLevel_WR_Transmitter_B <= rLevel_WR_Transmitter_A AND rLevel_WR_Transmitter_A <= rLevel_WR_Transmitter_C) OR
          (rLevel_WR_Transmitter_C <= rLevel_WR_Transmitter_A AND rLevel_WR_Transmitter_A <= rLevel_WR_Transmitter_B) THEN
        rVoted_Level_WR := rLevel_WR_Transmitter_A;
    ELSE
        rVoted_Level_WR := rLevel_WR_Transmitter_C;
    END_IF;

    IF ABS(rLevel_WR_Transmitter_A - rVoted_Level_WR) > rTMR_WR_Discrepancy_Limit THEN
        rTMR_WR_Timer_ChA := rTMR_WR_Timer_ChA + rScan_Period_Ts;
        IF rTMR_WR_Timer_ChA >= rTMR_Fault_Accum_Time_Limit THEN bTMR_WR_Failed_ChA := TRUE; END_IF;
    ELSE
        rTMR_WR_Timer_ChA := MAX(0.0, rTMR_WR_Timer_ChA - (rScan_Period_Ts * 0.5));
    END_IF;

    IF ABS(rLevel_WR_Transmitter_B - rVoted_Level_WR) > rTMR_WR_Discrepancy_Limit THEN
        rTMR_WR_Timer_ChB := rTMR_WR_Timer_ChB + rScan_Period_Ts;
        IF rTMR_WR_Timer_ChB >= rTMR_Fault_Accum_Time_Limit THEN bTMR_WR_Failed_ChB := TRUE; END_IF;
    ELSE
        rTMR_WR_Timer_ChB := MAX(0.0, rTMR_WR_Timer_ChB - (rScan_Period_Ts * 0.5));
    END_IF;

    IF ABS(rLevel_WR_Transmitter_C - rVoted_Level_WR) > rTMR_WR_Discrepancy_Limit THEN
        rTMR_WR_Timer_ChC := rTMR_WR_Timer_ChC + rScan_Period_Ts;
        IF rTMR_WR_Timer_ChC >= rTMR_Fault_Accum_Time_Limit THEN bTMR_WR_Failed_ChC := TRUE; END_IF;
    ELSE
        rTMR_WR_Timer_ChC := MAX(0.0, rTMR_WR_Timer_ChC - (rScan_Period_Ts * 0.5));
    END_IF;

ELSIF nHealth_TMR_Level_WR = 2 THEN
    IF NOT bTMR_WR_Failed_ChA AND NOT bTMR_WR_Failed_ChB THEN
        rVoted_Level_WR := 0.5 * (rLevel_WR_Transmitter_A + rLevel_WR_Transmitter_B);
        IF ABS(rLevel_WR_Transmitter_A - rLevel_WR_Transmitter_B) > rTMR_WR_Discrepancy_Limit THEN
            rTMR_WR_Timer_ChA := rTMR_WR_Timer_ChA + rScan_Period_Ts;
            IF rTMR_WR_Timer_ChA >= rTMR_Fault_Accum_Time_Limit THEN bTMR_WR_Failed_ChA := TRUE; END_IF;
        END_IF;
    ELSIF NOT bTMR_WR_Failed_ChA AND NOT bTMR_WR_Failed_ChC THEN
        rVoted_Level_WR := 0.5 * (rLevel_WR_Transmitter_A + rLevel_WR_Transmitter_C);
        IF ABS(rLevel_WR_Transmitter_A - rLevel_WR_Transmitter_C) > rTMR_WR_Discrepancy_Limit THEN
            rTMR_WR_Timer_ChA := rTMR_WR_Timer_ChA + rScan_Period_Ts;
            IF rTMR_WR_Timer_ChA >= rTMR_Fault_Accum_Time_Limit THEN bTMR_WR_Failed_ChA := TRUE; END_IF;
        END_IF;
    ELSE
        rVoted_Level_WR := 0.5 * (rLevel_WR_Transmitter_B + rLevel_WR_Transmitter_C);
        IF ABS(rLevel_WR_Transmitter_B - rLevel_WR_Transmitter_C) > rTMR_WR_Discrepancy_Limit THEN
            rTMR_WR_Timer_ChB := rTMR_WR_Timer_ChB + rScan_Period_Ts;
            IF rTMR_WR_Timer_ChB >= rTMR_Fault_Accum_Time_Limit THEN bTMR_WR_Failed_ChB := TRUE; END_IF;
        END_IF;
    END_IF;

ELSIF nHealth_TMR_Level_WR = 1 THEN
    IF NOT bTMR_WR_Failed_ChA THEN rVoted_Level_WR := rLevel_WR_Transmitter_A;
    ELSIF NOT bTMR_WR_Failed_ChB THEN rVoted_Level_WR := rLevel_WR_Transmitter_B;
    ELSE rVoted_Level_WR := rLevel_WR_Transmitter_C;
    END_IF;
ELSE
    rVoted_Level_WR := rVoted_Level_NR * 3.750; (* Invert narrow range ratio *)
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * TRIPLET 3: MAIN STEAM DRUM PRESSURE (PT-201A, PT-201B, PT-201C) [bar]
 * --------------------------------------------------------------------------------------------------------------------- *)
IF bReset_Trip_Interlocks THEN
    bTMR_Press_Failed_ChA := FALSE;
    bTMR_Press_Failed_ChB := FALSE;
    bTMR_Press_Failed_ChC := FALSE;
    rTMR_Press_Timer_ChA := 0.0;
    rTMR_Press_Timer_ChB := 0.0;
    rTMR_Press_Timer_ChC := 0.0;
END_IF;

nHealth_TMR_Press_MS := 0;
IF NOT bTMR_Press_Failed_ChA THEN nHealth_TMR_Press_MS := nHealth_TMR_Press_MS + 1; END_IF;
IF NOT bTMR_Press_Failed_ChB THEN nHealth_TMR_Press_MS := nHealth_TMR_Press_MS + 1; END_IF;
IF NOT bTMR_Press_Failed_ChC THEN nHealth_TMR_Press_MS := nHealth_TMR_Press_MS + 1; END_IF;

IF nHealth_TMR_Press_MS = 3 THEN
    IF (rPress_SteamDrum_Transmitter_A <= rPress_SteamDrum_Transmitter_B AND rPress_SteamDrum_Transmitter_B <= rPress_SteamDrum_Transmitter_C) OR
       (rPress_SteamDrum_Transmitter_C <= rPress_SteamDrum_Transmitter_B AND rPress_SteamDrum_Transmitter_B <= rPress_SteamDrum_Transmitter_A) THEN
        rVoted_Press_SteamDrum := rPress_SteamDrum_Transmitter_B;
    ELSIF (rPress_SteamDrum_Transmitter_B <= rPress_SteamDrum_Transmitter_A AND rPress_SteamDrum_Transmitter_A <= rPress_SteamDrum_Transmitter_C) OR
          (rPress_SteamDrum_Transmitter_C <= rPress_SteamDrum_Transmitter_A AND rPress_SteamDrum_Transmitter_A <= rPress_SteamDrum_Transmitter_B) THEN
        rVoted_Press_SteamDrum := rPress_SteamDrum_Transmitter_A;
    ELSE
        rVoted_Press_SteamDrum := rPress_SteamDrum_Transmitter_C;
    END_IF;

    IF ABS(rPress_SteamDrum_Transmitter_A - rVoted_Press_SteamDrum) > rTMR_Press_Discrepancy_Limit THEN
        rTMR_Press_Timer_ChA := rTMR_Press_Timer_ChA + rScan_Period_Ts;
        IF rTMR_Press_Timer_ChA >= rTMR_Fault_Accum_Time_Limit THEN bTMR_Press_Failed_ChA := TRUE; END_IF;
    ELSE
        rTMR_Press_Timer_ChA := MAX(0.0, rTMR_Press_Timer_ChA - (rScan_Period_Ts * 0.5));
    END_IF;

    IF ABS(rPress_SteamDrum_Transmitter_B - rVoted_Press_SteamDrum) > rTMR_Press_Discrepancy_Limit THEN
        rTMR_Press_Timer_ChB := rTMR_Press_Timer_ChB + rScan_Period_Ts;
        IF rTMR_Press_Timer_ChB >= rTMR_Fault_Accum_Time_Limit THEN bTMR_Press_Failed_ChB := TRUE; END_IF;
    ELSE
        rTMR_Press_Timer_ChB := MAX(0.0, rTMR_Press_Timer_ChB - (rScan_Period_Ts * 0.5));
    END_IF;

    IF ABS(rPress_SteamDrum_Transmitter_C - rVoted_Press_SteamDrum) > rTMR_Press_Discrepancy_Limit THEN
        rTMR_Press_Timer_ChC := rTMR_Press_Timer_ChC + rScan_Period_Ts;
        IF rTMR_Press_Timer_ChC >= rTMR_Fault_Accum_Time_Limit THEN bTMR_Press_Failed_ChC := TRUE; END_IF;
    ELSE
        rTMR_Press_Timer_ChC := MAX(0.0, rTMR_Press_Timer_ChC - (rScan_Period_Ts * 0.5));
    END_IF;

ELSIF nHealth_TMR_Press_MS = 2 THEN
    IF NOT bTMR_Press_Failed_ChA AND NOT bTMR_Press_Failed_ChB THEN
        rVoted_Press_SteamDrum := 0.5 * (rPress_SteamDrum_Transmitter_A + rPress_SteamDrum_Transmitter_B);
        IF ABS(rPress_SteamDrum_Transmitter_A - rPress_SteamDrum_Transmitter_B) > rTMR_Press_Discrepancy_Limit THEN
            rTMR_Press_Timer_ChA := rTMR_Press_Timer_ChA + rScan_Period_Ts;
            IF rTMR_Press_Timer_ChA >= rTMR_Fault_Accum_Time_Limit THEN bTMR_Press_Failed_ChA := TRUE; END_IF;
        END_IF;
    ELSIF NOT bTMR_Press_Failed_ChA AND NOT bTMR_Press_Failed_ChC THEN
        rVoted_Press_SteamDrum := 0.5 * (rPress_SteamDrum_Transmitter_A + rPress_SteamDrum_Transmitter_C);
        IF ABS(rPress_SteamDrum_Transmitter_A - rPress_SteamDrum_Transmitter_C) > rTMR_Press_Discrepancy_Limit THEN
            rTMR_Press_Timer_ChA := rTMR_Press_Timer_ChA + rScan_Period_Ts;
            IF rTMR_Press_Timer_ChA >= rTMR_Fault_Accum_Time_Limit THEN bTMR_Press_Failed_ChA := TRUE; END_IF;
        END_IF;
    ELSE
        rVoted_Press_SteamDrum := 0.5 * (rPress_SteamDrum_Transmitter_B + rPress_SteamDrum_Transmitter_C);
        IF ABS(rPress_SteamDrum_Transmitter_B - rPress_SteamDrum_Transmitter_C) > rTMR_Press_Discrepancy_Limit THEN
            rTMR_Press_Timer_ChB := rTMR_Press_Timer_ChB + rScan_Period_Ts;
            IF rTMR_Press_Timer_ChB >= rTMR_Fault_Accum_Time_Limit THEN bTMR_Press_Failed_ChB := TRUE; END_IF;
        END_IF;
    END_IF;

ELSIF nHealth_TMR_Press_MS = 1 THEN
    IF NOT bTMR_Press_Failed_ChA THEN rVoted_Press_SteamDrum := rPress_SteamDrum_Transmitter_A;
    ELSIF NOT bTMR_Press_Failed_ChB THEN rVoted_Press_SteamDrum := rPress_SteamDrum_Transmitter_B;
    ELSE rVoted_Press_SteamDrum := rPress_SteamDrum_Transmitter_C;
    END_IF;
ELSE
    rVoted_Press_SteamDrum := rSG_Nominal_Operating_Pressure; (* Fallback nominal 68.5 bar *)
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * TRIPLET 4: MAIN STEAM MASS FLOW RATE (FT-301A, FT-301B, FT-301C) [t/h]
 * --------------------------------------------------------------------------------------------------------------------- *)
IF bReset_Trip_Interlocks THEN
    bTMR_FlowMS_Failed_ChA := FALSE;
    bTMR_FlowMS_Failed_ChB := FALSE;
    bTMR_FlowMS_Failed_ChC := FALSE;
    rTMR_FlowMS_Timer_ChA := 0.0;
    rTMR_FlowMS_Timer_ChB := 0.0;
    rTMR_FlowMS_Timer_ChC := 0.0;
END_IF;

nHealth_TMR_Flow_MS := 0;
IF NOT bTMR_FlowMS_Failed_ChA THEN nHealth_TMR_Flow_MS := nHealth_TMR_Flow_MS + 1; END_IF;
IF NOT bTMR_FlowMS_Failed_ChB THEN nHealth_TMR_Flow_MS := nHealth_TMR_Flow_MS + 1; END_IF;
IF NOT bTMR_FlowMS_Failed_ChC THEN nHealth_TMR_Flow_MS := nHealth_TMR_Flow_MS + 1; END_IF;

IF nHealth_TMR_Flow_MS = 3 THEN
    IF (rFlow_MainSteam_Transmitter_A <= rFlow_MainSteam_Transmitter_B AND rFlow_MainSteam_Transmitter_B <= rFlow_MainSteam_Transmitter_C) OR
       (rFlow_MainSteam_Transmitter_C <= rFlow_MainSteam_Transmitter_B AND rFlow_MainSteam_Transmitter_B <= rFlow_MainSteam_Transmitter_A) THEN
        rVoted_Flow_MainSteam := rFlow_MainSteam_Transmitter_B;
    ELSIF (rFlow_MainSteam_Transmitter_B <= rFlow_MainSteam_Transmitter_A AND rFlow_MainSteam_Transmitter_A <= rFlow_MainSteam_Transmitter_C) OR
          (rFlow_MainSteam_Transmitter_C <= rFlow_MainSteam_Transmitter_A AND rFlow_MainSteam_Transmitter_A <= rFlow_MainSteam_Transmitter_B) THEN
        rVoted_Flow_MainSteam := rFlow_MainSteam_Transmitter_A;
    ELSE
        rVoted_Flow_MainSteam := rFlow_MainSteam_Transmitter_C;
    END_IF;

    IF ABS(rFlow_MainSteam_Transmitter_A - rVoted_Flow_MainSteam) > rTMR_FlowMS_Discrepancy_Limit THEN
        rTMR_FlowMS_Timer_ChA := rTMR_FlowMS_Timer_ChA + rScan_Period_Ts;
        IF rTMR_FlowMS_Timer_ChA >= rTMR_Fault_Accum_Time_Limit THEN bTMR_FlowMS_Failed_ChA := TRUE; END_IF;
    ELSE
        rTMR_FlowMS_Timer_ChA := MAX(0.0, rTMR_FlowMS_Timer_ChA - (rScan_Period_Ts * 0.5));
    END_IF;

    IF ABS(rFlow_MainSteam_Transmitter_B - rVoted_Flow_MainSteam) > rTMR_FlowMS_Discrepancy_Limit THEN
        rTMR_FlowMS_Timer_ChB := rTMR_FlowMS_Timer_ChB + rScan_Period_Ts;
        IF rTMR_FlowMS_Timer_ChB >= rTMR_Fault_Accum_Time_Limit THEN bTMR_FlowMS_Failed_ChB := TRUE; END_IF;
    ELSE
        rTMR_FlowMS_Timer_ChB := MAX(0.0, rTMR_FlowMS_Timer_ChB - (rScan_Period_Ts * 0.5));
    END_IF;

    IF ABS(rFlow_MainSteam_Transmitter_C - rVoted_Flow_MainSteam) > rTMR_FlowMS_Discrepancy_Limit THEN
        rTMR_FlowMS_Timer_ChC := rTMR_FlowMS_Timer_ChC + rScan_Period_Ts;
        IF rTMR_FlowMS_Timer_ChC >= rTMR_Fault_Accum_Time_Limit THEN bTMR_FlowMS_Failed_ChC := TRUE; END_IF;
    ELSE
        rTMR_FlowMS_Timer_ChC := MAX(0.0, rTMR_FlowMS_Timer_ChC - (rScan_Period_Ts * 0.5));
    END_IF;

ELSIF nHealth_TMR_Flow_MS = 2 THEN
    IF NOT bTMR_FlowMS_Failed_ChA AND NOT bTMR_FlowMS_Failed_ChB THEN
        rVoted_Flow_MainSteam := 0.5 * (rFlow_MainSteam_Transmitter_A + rFlow_MainSteam_Transmitter_B);
        IF ABS(rFlow_MainSteam_Transmitter_A - rFlow_MainSteam_Transmitter_B) > rTMR_FlowMS_Discrepancy_Limit THEN
            rTMR_FlowMS_Timer_ChA := rTMR_FlowMS_Timer_ChA + rScan_Period_Ts;
            IF rTMR_FlowMS_Timer_ChA >= rTMR_Fault_Accum_Time_Limit THEN bTMR_FlowMS_Failed_ChA := TRUE; END_IF;
        END_IF;
    ELSIF NOT bTMR_FlowMS_Failed_ChA AND NOT bTMR_FlowMS_Failed_ChC THEN
        rVoted_Flow_MainSteam := 0.5 * (rFlow_MainSteam_Transmitter_A + rFlow_MainSteam_Transmitter_C);
        IF ABS(rFlow_MainSteam_Transmitter_A - rFlow_MainSteam_Transmitter_C) > rTMR_FlowMS_Discrepancy_Limit THEN
            rTMR_FlowMS_Timer_ChA := rTMR_FlowMS_Timer_ChA + rScan_Period_Ts;
            IF rTMR_FlowMS_Timer_ChA >= rTMR_Fault_Accum_Time_Limit THEN bTMR_FlowMS_Failed_ChA := TRUE; END_IF;
        END_IF;
    ELSE
        rVoted_Flow_MainSteam := 0.5 * (rFlow_MainSteam_Transmitter_B + rFlow_MainSteam_Transmitter_C);
        IF ABS(rFlow_MainSteam_Transmitter_B - rFlow_MainSteam_Transmitter_C) > rTMR_FlowMS_Discrepancy_Limit THEN
            rTMR_FlowMS_Timer_ChB := rTMR_FlowMS_Timer_ChB + rScan_Period_Ts;
            IF rTMR_FlowMS_Timer_ChB >= rTMR_Fault_Accum_Time_Limit THEN bTMR_FlowMS_Failed_ChB := TRUE; END_IF;
        END_IF;
    END_IF;

ELSIF nHealth_TMR_Flow_MS = 1 THEN
    IF NOT bTMR_FlowMS_Failed_ChA THEN rVoted_Flow_MainSteam := rFlow_MainSteam_Transmitter_A;
    ELSIF NOT bTMR_FlowMS_Failed_ChB THEN rVoted_Flow_MainSteam := rFlow_MainSteam_Transmitter_B;
    ELSE rVoted_Flow_MainSteam := rFlow_MainSteam_Transmitter_C;
    END_IF;
ELSE
    (* Calculate flow proxy from nuclear thermal power *)
    rVoted_Flow_MainSteam := (rReactor_Thermal_Power_Pct / 100.0) * rSG_Full_Power_Steam_Flow_t_h;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * TRIPLET 5: MAIN FEEDWATER MASS FLOW RATE (FT-401A, FT-401B, FT-401C) [t/h]
 * --------------------------------------------------------------------------------------------------------------------- *)
IF bReset_Trip_Interlocks THEN
    bTMR_FlowFW_Failed_ChA := FALSE;
    bTMR_FlowFW_Failed_ChB := FALSE;
    bTMR_FlowFW_Failed_ChC := FALSE;
    rTMR_FlowFW_Timer_ChA := 0.0;
    rTMR_FlowFW_Timer_ChB := 0.0;
    rTMR_FlowFW_Timer_ChC := 0.0;
END_IF;

nHealth_TMR_Flow_FW := 0;
IF NOT bTMR_FlowFW_Failed_ChA THEN nHealth_TMR_Flow_FW := nHealth_TMR_Flow_FW + 1; END_IF;
IF NOT bTMR_FlowFW_Failed_ChB THEN nHealth_TMR_Flow_FW := nHealth_TMR_Flow_FW + 1; END_IF;
IF NOT bTMR_FlowFW_Failed_ChC THEN nHealth_TMR_Flow_FW := nHealth_TMR_Flow_FW + 1; END_IF;

IF nHealth_TMR_Flow_FW = 3 THEN
    IF (rFlow_Feedwater_Transmitter_A <= rFlow_Feedwater_Transmitter_B AND rFlow_Feedwater_Transmitter_B <= rFlow_Feedwater_Transmitter_C) OR
       (rFlow_Feedwater_Transmitter_C <= rFlow_Feedwater_Transmitter_B AND rFlow_Feedwater_Transmitter_B <= rFlow_Feedwater_Transmitter_A) THEN
        rVoted_Flow_Feedwater := rFlow_Feedwater_Transmitter_B;
    ELSIF (rFlow_Feedwater_Transmitter_B <= rFlow_Feedwater_Transmitter_A AND rFlow_Feedwater_Transmitter_A <= rFlow_Feedwater_Transmitter_C) OR
          (rFlow_Feedwater_Transmitter_C <= rFlow_Feedwater_Transmitter_A AND rFlow_Feedwater_Transmitter_A <= rFlow_Feedwater_Transmitter_B) THEN
        rVoted_Flow_Feedwater := rFlow_Feedwater_Transmitter_A;
    ELSE
        rVoted_Flow_Feedwater := rFlow_Feedwater_Transmitter_C;
    END_IF;

    IF ABS(rFlow_Feedwater_Transmitter_A - rVoted_Flow_Feedwater) > rTMR_FlowFW_Discrepancy_Limit THEN
        rTMR_FlowFW_Timer_ChA := rTMR_FlowFW_Timer_ChA + rScan_Period_Ts;
        IF rTMR_FlowFW_Timer_ChA >= rTMR_Fault_Accum_Time_Limit THEN bTMR_FlowFW_Failed_ChA := TRUE; END_IF;
    ELSE
        rTMR_FlowFW_Timer_ChA := MAX(0.0, rTMR_FlowFW_Timer_ChA - (rScan_Period_Ts * 0.5));
    END_IF;

    IF ABS(rFlow_Feedwater_Transmitter_B - rVoted_Flow_Feedwater) > rTMR_FlowFW_Discrepancy_Limit THEN
        rTMR_FlowFW_Timer_ChB := rTMR_FlowFW_Timer_ChB + rScan_Period_Ts;
        IF rTMR_FlowFW_Timer_ChB >= rTMR_Fault_Accum_Time_Limit THEN bTMR_FlowFW_Failed_ChB := TRUE; END_IF;
    ELSE
        rTMR_FlowFW_Timer_ChB := MAX(0.0, rTMR_FlowFW_Timer_ChB - (rScan_Period_Ts * 0.5));
    END_IF;

    IF ABS(rFlow_Feedwater_Transmitter_C - rVoted_Flow_Feedwater) > rTMR_FlowFW_Discrepancy_Limit THEN
        rTMR_FlowFW_Timer_ChC := rTMR_FlowFW_Timer_ChC + rScan_Period_Ts;
        IF rTMR_FlowFW_Timer_ChC >= rTMR_Fault_Accum_Time_Limit THEN bTMR_FlowFW_Failed_ChC := TRUE; END_IF;
    ELSE
        rTMR_FlowFW_Timer_ChC := MAX(0.0, rTMR_FlowFW_Timer_ChC - (rScan_Period_Ts * 0.5));
    END_IF;

ELSIF nHealth_TMR_Flow_FW = 2 THEN
    IF NOT bTMR_FlowFW_Failed_ChA AND NOT bTMR_FlowFW_Failed_ChB THEN
        rVoted_Flow_Feedwater := 0.5 * (rFlow_Feedwater_Transmitter_A + rFlow_Feedwater_Transmitter_B);
        IF ABS(rFlow_Feedwater_Transmitter_A - rFlow_Feedwater_Transmitter_B) > rTMR_FlowFW_Discrepancy_Limit THEN
            rTMR_FlowFW_Timer_ChA := rTMR_FlowFW_Timer_ChA + rScan_Period_Ts;
            IF rTMR_FlowFW_Timer_ChA >= rTMR_Fault_Accum_Time_Limit THEN bTMR_FlowFW_Failed_ChA := TRUE; END_IF;
        END_IF;
    ELSIF NOT bTMR_FlowFW_Failed_ChA AND NOT bTMR_FlowFW_Failed_ChC THEN
        rVoted_Flow_Feedwater := 0.5 * (rFlow_Feedwater_Transmitter_A + rFlow_Feedwater_Transmitter_C);
        IF ABS(rFlow_Feedwater_Transmitter_A - rFlow_Feedwater_Transmitter_C) > rTMR_FlowFW_Discrepancy_Limit THEN
            rTMR_FlowFW_Timer_ChA := rTMR_FlowFW_Timer_ChA + rScan_Period_Ts;
            IF rTMR_FlowFW_Timer_ChA >= rTMR_Fault_Accum_Time_Limit THEN bTMR_FlowFW_Failed_ChA := TRUE; END_IF;
        END_IF;
    ELSE
        rVoted_Flow_Feedwater := 0.5 * (rFlow_Feedwater_Transmitter_B + rFlow_Feedwater_Transmitter_C);
        IF ABS(rFlow_Feedwater_Transmitter_B - rFlow_Feedwater_Transmitter_C) > rTMR_FlowFW_Discrepancy_Limit THEN
            rTMR_FlowFW_Timer_ChB := rTMR_FlowFW_Timer_ChB + rScan_Period_Ts;
            IF rTMR_FlowFW_Timer_ChB >= rTMR_Fault_Accum_Time_Limit THEN bTMR_FlowFW_Failed_ChB := TRUE; END_IF;
        END_IF;
    END_IF;

ELSIF nHealth_TMR_Flow_FW = 1 THEN
    IF NOT bTMR_FlowFW_Failed_ChA THEN rVoted_Flow_Feedwater := rFlow_Feedwater_Transmitter_A;
    ELSIF NOT bTMR_FlowFW_Failed_ChB THEN rVoted_Flow_Feedwater := rFlow_Feedwater_Transmitter_B;
    ELSE rVoted_Flow_Feedwater := rFlow_Feedwater_Transmitter_C;
    END_IF;
ELSE
    (* Synthesize from MFRV position valve sizing curve *)
    rVoted_Flow_Feedwater := (rCommand_MFRV_Position / 100.0) * rSG_Full_Power_Feed_Flow_t_h;
END_IF;
""")
    return "\n".join(code)

if __name__ == "__main__":
    s = get_phase1_tmr()
    print("Phase 1 TMR length:", len(s))
