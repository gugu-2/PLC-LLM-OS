# scratch/gen_phase1.py

def get_channel_tmr_code(ch_tag, var_prefix, min_lim, max_lim, tol, max_rate, out_var, default_val, unit_str):
    code = f"""
    (* ------------------------------------------------------------------------- *)
    (* 2oo3 TMR REDUNDANCY PROCESSING: {ch_tag} [{unit_str}]                     *)
    (* ------------------------------------------------------------------------- *)
    (* Step 1: Physical Boundary & Transmitter Health Validation *)
    IF (f{var_prefix}A < {min_lim}) OR (f{var_prefix}A > {max_lim}) OR (NOT b{var_prefix}A_Valid) THEN
        bChA_Healthy_{var_prefix[:-1]} := FALSE;
    ELSE
        bChA_Healthy_{var_prefix[:-1]} := TRUE;
    END_IF;

    IF (f{var_prefix}B < {min_lim}) OR (f{var_prefix}B > {max_lim}) OR (NOT b{var_prefix}B_Valid) THEN
        bChB_Healthy_{var_prefix[:-1]} := FALSE;
    ELSE
        bChB_Healthy_{var_prefix[:-1]} := TRUE;
    END_IF;

    IF (f{var_prefix}C < {min_lim}) OR (f{var_prefix}C > {max_lim}) OR (NOT b{var_prefix}C_Valid) THEN
        bChC_Healthy_{var_prefix[:-1]} := FALSE;
    ELSE
        bChC_Healthy_{var_prefix[:-1]} := TRUE;
    END_IF;

    (* Step 2: Rate-of-Change Sanity Checks to detect freeze or impulse noise *)
    IF bChA_Healthy_{var_prefix[:-1]} THEN
        IF ABS(f{var_prefix}A - fPrevVal_{var_prefix}A) / fCycleTime_Ts > {max_rate} THEN
            bChA_Healthy_{var_prefix[:-1]} := FALSE;
        END_IF;
    END_IF;
    fPrevVal_{var_prefix}A := f{var_prefix}A;

    IF bChB_Healthy_{var_prefix[:-1]} THEN
        IF ABS(f{var_prefix}B - fPrevVal_{var_prefix}B) / fCycleTime_Ts > {max_rate} THEN
            bChB_Healthy_{var_prefix[:-1]} := FALSE;
        END_IF;
    END_IF;
    fPrevVal_{var_prefix}B := f{var_prefix}B;

    IF bChC_Healthy_{var_prefix[:-1]} THEN
        IF ABS(f{var_prefix}C - fPrevVal_{var_prefix}C) / fCycleTime_Ts > {max_rate} THEN
            bChC_Healthy_{var_prefix[:-1]} := FALSE;
        END_IF;
    END_IF;
    fPrevVal_{var_prefix}C := f{var_prefix}C;

    (* Step 3: Pairwise Deviation Calculations *)
    fDev_{var_prefix}AB := ABS(f{var_prefix}A - f{var_prefix}B);
    fDev_{var_prefix}BC := ABS(f{var_prefix}B - f{var_prefix}C);
    fDev_{var_prefix}CA := ABS(f{var_prefix}C - f{var_prefix}A);

    (* Step 4: Discrepancy Integration Accumulation Timers (500 ms Trip Window) *)
    IF fDev_{var_prefix}AB > {tol} THEN
        tDiscrep_{var_prefix}AB := tDiscrep_{var_prefix}AB + fCycleTime_Ts;
    ELSE
        IF tDiscrep_{var_prefix}AB > (2.0 * fCycleTime_Ts) THEN
            tDiscrep_{var_prefix}AB := tDiscrep_{var_prefix}AB - (2.0 * fCycleTime_Ts);
        ELSE
            tDiscrep_{var_prefix}AB := 0.0;
        END_IF;
    END_IF;

    IF fDev_{var_prefix}BC > {tol} THEN
        tDiscrep_{var_prefix}BC := tDiscrep_{var_prefix}BC + fCycleTime_Ts;
    ELSE
        IF tDiscrep_{var_prefix}BC > (2.0 * fCycleTime_Ts) THEN
            tDiscrep_{var_prefix}BC := tDiscrep_{var_prefix}BC - (2.0 * fCycleTime_Ts);
        ELSE
            tDiscrep_{var_prefix}BC := 0.0;
        END_IF;
    END_IF;

    IF fDev_{var_prefix}CA > {tol} THEN
        tDiscrep_{var_prefix}CA := tDiscrep_{var_prefix}CA + fCycleTime_Ts;
    ELSE
        IF tDiscrep_{var_prefix}CA > (2.0 * fCycleTime_Ts) THEN
            tDiscrep_{var_prefix}CA := tDiscrep_{var_prefix}CA - (2.0 * fCycleTime_Ts);
        ELSE
            tDiscrep_{var_prefix}CA := 0.0;
        END_IF;
    END_IF;

    bDiscrep_{var_prefix}AB := (tDiscrep_{var_prefix}AB >= 0.500);
    bDiscrep_{var_prefix}BC := (tDiscrep_{var_prefix}BC >= 0.500);
    bDiscrep_{var_prefix}CA := (tDiscrep_{var_prefix}CA >= 0.500);

    (* Step 5: Tri-Channel Isolation Logic *)
    IF bDiscrep_{var_prefix}AB AND bDiscrep_{var_prefix}CA THEN
        bChA_Healthy_{var_prefix[:-1]} := FALSE;
    END_IF;
    IF bDiscrep_{var_prefix}AB AND bDiscrep_{var_prefix}BC THEN
        bChB_Healthy_{var_prefix[:-1]} := FALSE;
    END_IF;
    IF bDiscrep_{var_prefix}BC AND bDiscrep_{var_prefix}CA THEN
        bChC_Healthy_{var_prefix[:-1]} := FALSE;
    END_IF;

    (* Step 6: Count Healthy Available Channels *)
    nHealthyCount_{var_prefix[:-1]} := 0;
    IF bChA_Healthy_{var_prefix[:-1]} THEN
        nHealthyCount_{var_prefix[:-1]} := nHealthyCount_{var_prefix[:-1]} + 1;
    END_IF;
    IF bChB_Healthy_{var_prefix[:-1]} THEN
        nHealthyCount_{var_prefix[:-1]} := nHealthyCount_{var_prefix[:-1]} + 1;
    END_IF;
    IF bChC_Healthy_{var_prefix[:-1]} THEN
        nHealthyCount_{var_prefix[:-1]} := nHealthyCount_{var_prefix[:-1]} + 1;
    END_IF;

    (* Step 7: Redundancy Voting and Bumpless Degradation Mode Selection *)
    IF nHealthyCount_{var_prefix[:-1]} = 3 THEN
        (* All three healthy: True Median Selection *)
        IF ((f{var_prefix}A >= f{var_prefix}B) AND (f{var_prefix}A <= f{var_prefix}C)) OR 
           ((f{var_prefix}A <= f{var_prefix}B) AND (f{var_prefix}A >= f{var_prefix}C)) THEN
            {out_var} := f{var_prefix}A;
        ELSIF ((f{var_prefix}B >= f{var_prefix}A) AND (f{var_prefix}B <= f{var_prefix}C)) OR 
              ((f{var_prefix}B <= f{var_prefix}A) AND (f{var_prefix}B >= f{var_prefix}C)) THEN
            {out_var} := f{var_prefix}B;
        ELSE
            {out_var} := f{var_prefix}C;
        END_IF;
    ELSIF nHealthyCount_{var_prefix[:-1]} = 2 THEN
        (* 1oo2 Degraded Mode: Average of two surviving healthy channels *)
        bDegradedTMR := TRUE;
        IF bChA_Healthy_{var_prefix[:-1]} AND bChB_Healthy_{var_prefix[:-1]} THEN
            {out_var} := (f{var_prefix}A + f{var_prefix}B) * 0.50000000;
        ELSIF bChB_Healthy_{var_prefix[:-1]} AND bChC_Healthy_{var_prefix[:-1]} THEN
            {out_var} := (f{var_prefix}B + f{var_prefix}C) * 0.50000000;
        ELSE
            {out_var} := (f{var_prefix}A + f{var_prefix}C) * 0.50000000;
        END_IF;
    ELSIF nHealthyCount_{var_prefix[:-1]} = 1 THEN
        (* 1oo1 Degraded Mode: Single channel tracking with severe diagnostic alert *)
        bDegradedTMR := TRUE;
        bAlert_TMR_Discrepancy := TRUE;
        IF bChA_Healthy_{var_prefix[:-1]} THEN
            {out_var} := f{var_prefix}A;
        ELSIF bChB_Healthy_{var_prefix[:-1]} THEN
            {out_var} := f{var_prefix}B;
        ELSE
            {out_var} := f{var_prefix}C;
        END_IF;
    ELSE
        (* Total Channel Failure (0oo3): Hold safe default value & trigger fatal trip *)
        {out_var} := {default_val};
        bTrip_SensorLoss_Fatal := TRUE;
        bSystemHealthy := FALSE;
    END_IF;
"""
    return code

def get_phase1():
    header = """
(* ============================================================================== *)
(* PHASE 1: 2oo3 TMR SENSOR VOTING WITH DISCREPANCY TIMERS & BUMPLESS DEGRADATION *)
(* ============================================================================== *)
"""
    ch1 = get_channel_tmr_code("LT_NR_101", "LT_NR_101", "-1000.0", "1000.0", "35.0", "150.0", "fVotedNarrowRangeLevel_mm", "0.0", "mm")
    ch2 = get_channel_tmr_code("LT_WR_102", "LT_WR_102", "0.0", "15000.0", "300.0", "500.0", "fVotedWideRangeLevel_mm", "10500.0", "mm")
    ch3 = get_channel_tmr_code("PT_MS_201", "PT_MS_201", "0.0", "100.0", "1.2", "5.0", "fVotedDrumPressure_bar", "68.5", "bar")
    ch4 = get_channel_tmr_code("FT_MS_301", "FT_MS_301", "0.0", "2500.0", "45.0", "300.0", "fVotedSteamFlow_t_h", "1850.0", "t/h")
    ch5 = get_channel_tmr_code("FT_FW_401", "FT_FW_401", "0.0", "2500.0", "45.0", "300.0", "fVotedFeedwaterFlow_t_h", "1850.0", "t/h")
    ch6 = get_channel_tmr_code("TE_CL_501", "TE_CL_501", "250.0", "330.0", "1.5", "3.0", "fVotedColdLegTemp_degC", "292.0", "deg C")
    ch7 = get_channel_tmr_code("RE_SGTR_601", "RE_SGTR_601", "0.0", "1.0E7", "50000.0", "1000000.0", "fVotedSGTR_Rad_Bq_m3", "120.0", "Bq/m3")
    
    return header + ch1 + ch2 + ch3 + ch4 + ch5 + ch6 + ch7

if __name__ == "__main__":
    p1 = get_phase1()
    print(f"Phase 1 generated. Length: {len(p1)} characters.")
