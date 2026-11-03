# -*- coding: utf-8 -*-
"""
Part 2 of CCR Platforming Function Block:
Phase 1: 2oo3 TMR Voting Logic for all 11 sensor trios with bumpless degradation.
Phase 2: Thermodynamic properties, Arrhenius reaction kinetics, heat balances, WABT, RON, C5+ Yield, H2/HC ratio.
"""

def get_phase1_and_phase2():
    return """
(* ====================================================================================================== *)
(* === PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING & FAULT-TOLERANT DEGRADATION      === *)
(* ====================================================================================================== *)

(* --- 1.1: REACTOR BED 1 INLET TEMPERATURE 2oo3 VOTING --- *)
rTempDiff := ABS(rT_Bed1_In_Ch1 - rT_Bed1_In_Ch2);
IF rTempDiff > rTMR_TempDiscrepancyLimit_degC THEN
    tBed1_In_DiscTimer_12 := tBed1_In_DiscTimer_12 + 1.0;
ELSE
    tBed1_In_DiscTimer_12 := 0.0;
END_IF;

rTempDiff := ABS(rT_Bed1_In_Ch2 - rT_Bed1_In_Ch3);
IF rTempDiff > rTMR_TempDiscrepancyLimit_degC THEN
    tBed1_In_DiscTimer_23 := tBed1_In_DiscTimer_23 + 1.0;
ELSE
    tBed1_In_DiscTimer_23 := 0.0;
END_IF;

rTempDiff := ABS(rT_Bed1_In_Ch3 - rT_Bed1_In_Ch1);
IF rTempDiff > rTMR_TempDiscrepancyLimit_degC THEN
    tBed1_In_DiscTimer_31 := tBed1_In_DiscTimer_31 + 1.0;
ELSE
    tBed1_In_DiscTimer_31 := 0.0;
END_IF;

bBed1_In_Ch1_Fault := (tBed1_In_DiscTimer_12 > rTMR_DiscrepancyTripTime_s AND tBed1_In_DiscTimer_31 > rTMR_DiscrepancyTripTime_s)
                      OR (rT_Bed1_In_Ch1 < 300.0 OR rT_Bed1_In_Ch1 > 650.0);
bBed1_In_Ch2_Fault := (tBed1_In_DiscTimer_12 > rTMR_DiscrepancyTripTime_s AND tBed1_In_DiscTimer_23 > rTMR_DiscrepancyTripTime_s)
                      OR (rT_Bed1_In_Ch2 < 300.0 OR rT_Bed1_In_Ch2 > 650.0);
bBed1_In_Ch3_Fault := (tBed1_In_DiscTimer_23 > rTMR_DiscrepancyTripTime_s AND tBed1_In_DiscTimer_31 > rTMR_DiscrepancyTripTime_s)
                      OR (rT_Bed1_In_Ch3 < 300.0 OR rT_Bed1_In_Ch3 > 650.0);

IF NOT bBed1_In_Ch1_Fault AND NOT bBed1_In_Ch2_Fault AND NOT bBed1_In_Ch3_Fault THEN
    (* 3 Channels Healthy: Exact Median Selection *)
    IF (rT_Bed1_In_Ch1 >= rT_Bed1_In_Ch2 AND rT_Bed1_In_Ch1 <= rT_Bed1_In_Ch3)
       OR (rT_Bed1_In_Ch1 >= rT_Bed1_In_Ch3 AND rT_Bed1_In_Ch1 <= rT_Bed1_In_Ch2) THEN
        rVoted_Bed1_In_degC := rT_Bed1_In_Ch1;
    ELSIF (rT_Bed1_In_Ch2 >= rT_Bed1_In_Ch1 AND rT_Bed1_In_Ch2 <= rT_Bed1_In_Ch3)
       OR (rT_Bed1_In_Ch2 >= rT_Bed1_In_Ch3 AND rT_Bed1_In_Ch2 <= rT_Bed1_In_Ch1) THEN
        rVoted_Bed1_In_degC := rT_Bed1_In_Ch2;
    ELSE
        rVoted_Bed1_In_degC := rT_Bed1_In_Ch3;
    END_IF;
ELSIF NOT bBed1_In_Ch1_Fault AND NOT bBed1_In_Ch2_Fault THEN
    rVoted_Bed1_In_degC := (rT_Bed1_In_Ch1 + rT_Bed1_In_Ch2) * 0.5;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000001;
ELSIF NOT bBed1_In_Ch2_Fault AND NOT bBed1_In_Ch3_Fault THEN
    rVoted_Bed1_In_degC := (rT_Bed1_In_Ch2 + rT_Bed1_In_Ch3) * 0.5;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000001;
ELSIF NOT bBed1_In_Ch1_Fault AND NOT bBed1_In_Ch3_Fault THEN
    rVoted_Bed1_In_degC := (rT_Bed1_In_Ch1 + rT_Bed1_In_Ch3) * 0.5;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000001;
ELSIF NOT bBed1_In_Ch1_Fault THEN
    rVoted_Bed1_In_degC := rT_Bed1_In_Ch1;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000002;
ELSIF NOT bBed1_In_Ch2_Fault THEN
    rVoted_Bed1_In_degC := rT_Bed1_In_Ch2;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000002;
ELSIF NOT bBed1_In_Ch3_Fault THEN
    rVoted_Bed1_In_degC := rT_Bed1_In_Ch3;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000002;
ELSE
    rVoted_Bed1_In_degC := 500.0; (* Failsafe Default *)
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000004;
END_IF;

(* --- 1.2: REACTOR BED 1 OUTLET TEMPERATURE 2oo3 VOTING --- *)
rTempDiff := ABS(rT_Bed1_Out_Ch1 - rT_Bed1_Out_Ch2);
IF rTempDiff > rTMR_TempDiscrepancyLimit_degC THEN
    tBed1_Out_DiscTimer_12 := tBed1_Out_DiscTimer_12 + 1.0;
ELSE
    tBed1_Out_DiscTimer_12 := 0.0;
END_IF;

rTempDiff := ABS(rT_Bed1_Out_Ch2 - rT_Bed1_Out_Ch3);
IF rTempDiff > rTMR_TempDiscrepancyLimit_degC THEN
    tBed1_Out_DiscTimer_23 := tBed1_Out_DiscTimer_23 + 1.0;
ELSE
    tBed1_Out_DiscTimer_23 := 0.0;
END_IF;

rTempDiff := ABS(rT_Bed1_Out_Ch3 - rT_Bed1_Out_Ch1);
IF rTempDiff > rTMR_TempDiscrepancyLimit_degC THEN
    tBed1_Out_DiscTimer_31 := tBed1_Out_DiscTimer_31 + 1.0;
ELSE
    tBed1_Out_DiscTimer_31 := 0.0;
END_IF;

bBed1_Out_Ch1_Fault := (tBed1_Out_DiscTimer_12 > rTMR_DiscrepancyTripTime_s AND tBed1_Out_DiscTimer_31 > rTMR_DiscrepancyTripTime_s)
                       OR (rT_Bed1_Out_Ch1 < 300.0 OR rT_Bed1_Out_Ch1 > 650.0);
bBed1_Out_Ch2_Fault := (tBed1_Out_DiscTimer_12 > rTMR_DiscrepancyTripTime_s AND tBed1_Out_DiscTimer_23 > rTMR_DiscrepancyTripTime_s)
                       OR (rT_Bed1_Out_Ch2 < 300.0 OR rT_Bed1_Out_Ch2 > 650.0);
bBed1_Out_Ch3_Fault := (tBed1_Out_DiscTimer_23 > rTMR_DiscrepancyTripTime_s AND tBed1_Out_DiscTimer_31 > rTMR_DiscrepancyTripTime_s)
                       OR (rT_Bed1_Out_Ch3 < 300.0 OR rT_Bed1_Out_Ch3 > 650.0);

IF NOT bBed1_Out_Ch1_Fault AND NOT bBed1_Out_Ch2_Fault AND NOT bBed1_Out_Ch3_Fault THEN
    IF (rT_Bed1_Out_Ch1 >= rT_Bed1_Out_Ch2 AND rT_Bed1_Out_Ch1 <= rT_Bed1_Out_Ch3)
       OR (rT_Bed1_Out_Ch1 >= rT_Bed1_Out_Ch3 AND rT_Bed1_Out_Ch1 <= rT_Bed1_Out_Ch2) THEN
        rVoted_Bed1_Out_degC := rT_Bed1_Out_Ch1;
    ELSIF (rT_Bed1_Out_Ch2 >= rT_Bed1_Out_Ch1 AND rT_Bed1_Out_Ch2 <= rT_Bed1_Out_Ch3)
       OR (rT_Bed1_Out_Ch2 >= rT_Bed1_Out_Ch3 AND rT_Bed1_Out_Ch2 <= rT_Bed1_Out_Ch1) THEN
        rVoted_Bed1_Out_degC := rT_Bed1_Out_Ch2;
    ELSE
        rVoted_Bed1_Out_degC := rT_Bed1_Out_Ch3;
    END_IF;
ELSIF NOT bBed1_Out_Ch1_Fault AND NOT bBed1_Out_Ch2_Fault THEN
    rVoted_Bed1_Out_degC := (rT_Bed1_Out_Ch1 + rT_Bed1_Out_Ch2) * 0.5;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000001;
ELSIF NOT bBed1_Out_Ch2_Fault AND NOT bBed1_Out_Ch3_Fault THEN
    rVoted_Bed1_Out_degC := (rT_Bed1_Out_Ch2 + rT_Bed1_Out_Ch3) * 0.5;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000001;
ELSIF NOT bBed1_Out_Ch1_Fault AND NOT bBed1_Out_Ch3_Fault THEN
    rVoted_Bed1_Out_degC := (rT_Bed1_Out_Ch1 + rT_Bed1_Out_Ch3) * 0.5;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000001;
ELSIF NOT bBed1_Out_Ch1_Fault THEN
    rVoted_Bed1_Out_degC := rT_Bed1_Out_Ch1;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000002;
ELSIF NOT bBed1_Out_Ch2_Fault THEN
    rVoted_Bed1_Out_degC := rT_Bed1_Out_Ch2;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000002;
ELSIF NOT bBed1_Out_Ch3_Fault THEN
    rVoted_Bed1_Out_degC := rT_Bed1_Out_Ch3;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000002;
ELSE
    rVoted_Bed1_Out_degC := 450.0;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000004;
END_IF;

(* --- 1.3: REACTOR BED 2 INLET TEMPERATURE 2oo3 VOTING --- *)
rTempDiff := ABS(rT_Bed2_In_Ch1 - rT_Bed2_In_Ch2);
IF rTempDiff > rTMR_TempDiscrepancyLimit_degC THEN
    tBed2_In_DiscTimer_12 := tBed2_In_DiscTimer_12 + 1.0;
ELSE
    tBed2_In_DiscTimer_12 := 0.0;
END_IF;

rTempDiff := ABS(rT_Bed2_In_Ch2 - rT_Bed2_In_Ch3);
IF rTempDiff > rTMR_TempDiscrepancyLimit_degC THEN
    tBed2_In_DiscTimer_23 := tBed2_In_DiscTimer_23 + 1.0;
ELSE
    tBed2_In_DiscTimer_23 := 0.0;
END_IF;

rTempDiff := ABS(rT_Bed2_In_Ch3 - rT_Bed2_In_Ch1);
IF rTempDiff > rTMR_TempDiscrepancyLimit_degC THEN
    tBed2_In_DiscTimer_31 := tBed2_In_DiscTimer_31 + 1.0;
ELSE
    tBed2_In_DiscTimer_31 := 0.0;
END_IF;

bBed2_In_Ch1_Fault := (tBed2_In_DiscTimer_12 > rTMR_DiscrepancyTripTime_s AND tBed2_In_DiscTimer_31 > rTMR_DiscrepancyTripTime_s)
                      OR (rT_Bed2_In_Ch1 < 300.0 OR rT_Bed2_In_Ch1 > 650.0);
bBed2_In_Ch2_Fault := (tBed2_In_DiscTimer_12 > rTMR_DiscrepancyTripTime_s AND tBed2_In_DiscTimer_23 > rTMR_DiscrepancyTripTime_s)
                      OR (rT_Bed2_In_Ch2 < 300.0 OR rT_Bed2_In_Ch2 > 650.0);
bBed2_In_Ch3_Fault := (tBed2_In_DiscTimer_23 > rTMR_DiscrepancyTripTime_s AND tBed2_In_DiscTimer_31 > rTMR_DiscrepancyTripTime_s)
                      OR (rT_Bed2_In_Ch3 < 300.0 OR rT_Bed2_In_Ch3 > 650.0);

IF NOT bBed2_In_Ch1_Fault AND NOT bBed2_In_Ch2_Fault AND NOT bBed2_In_Ch3_Fault THEN
    IF (rT_Bed2_In_Ch1 >= rT_Bed2_In_Ch2 AND rT_Bed2_In_Ch1 <= rT_Bed2_In_Ch3)
       OR (rT_Bed2_In_Ch1 >= rT_Bed2_In_Ch3 AND rT_Bed2_In_Ch1 <= rT_Bed2_In_Ch2) THEN
        rVoted_Bed2_In_degC := rT_Bed2_In_Ch1;
    ELSIF (rT_Bed2_In_Ch2 >= rT_Bed2_In_Ch1 AND rT_Bed2_In_Ch2 <= rT_Bed2_In_Ch3)
       OR (rT_Bed2_In_Ch2 >= rT_Bed2_In_Ch3 AND rT_Bed2_In_Ch2 <= rT_Bed2_In_Ch1) THEN
        rVoted_Bed2_In_degC := rT_Bed2_In_Ch2;
    ELSE
        rVoted_Bed2_In_degC := rT_Bed2_In_Ch3;
    END_IF;
ELSIF NOT bBed2_In_Ch1_Fault AND NOT bBed2_In_Ch2_Fault THEN
    rVoted_Bed2_In_degC := (rT_Bed2_In_Ch1 + rT_Bed2_In_Ch2) * 0.5;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000001;
ELSIF NOT bBed2_In_Ch2_Fault AND NOT bBed2_In_Ch3_Fault THEN
    rVoted_Bed2_In_degC := (rT_Bed2_In_Ch2 + rT_Bed2_In_Ch3) * 0.5;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000001;
ELSIF NOT bBed2_In_Ch1_Fault AND NOT bBed2_In_Ch3_Fault THEN
    rVoted_Bed2_In_degC := (rT_Bed2_In_Ch1 + rT_Bed2_In_Ch3) * 0.5;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000001;
ELSIF NOT bBed2_In_Ch1_Fault THEN
    rVoted_Bed2_In_degC := rT_Bed2_In_Ch1;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000002;
ELSIF NOT bBed2_In_Ch2_Fault THEN
    rVoted_Bed2_In_degC := rT_Bed2_In_Ch2;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000002;
ELSIF NOT bBed2_In_Ch3_Fault THEN
    rVoted_Bed2_In_degC := rT_Bed2_In_Ch3;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000002;
ELSE
    rVoted_Bed2_In_degC := 510.0;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000004;
END_IF;

(* --- 1.4: REACTOR BED 2 OUTLET TEMPERATURE 2oo3 VOTING --- *)
rTempDiff := ABS(rT_Bed2_Out_Ch1 - rT_Bed2_Out_Ch2);
IF rTempDiff > rTMR_TempDiscrepancyLimit_degC THEN
    tBed2_Out_DiscTimer_12 := tBed2_Out_DiscTimer_12 + 1.0;
ELSE
    tBed2_Out_DiscTimer_12 := 0.0;
END_IF;

rTempDiff := ABS(rT_Bed2_Out_Ch2 - rT_Bed2_Out_Ch3);
IF rTempDiff > rTMR_TempDiscrepancyLimit_degC THEN
    tBed2_Out_DiscTimer_23 := tBed2_Out_DiscTimer_23 + 1.0;
ELSE
    tBed2_Out_DiscTimer_23 := 0.0;
END_IF;

rTempDiff := ABS(rT_Bed2_Out_Ch3 - rT_Bed2_Out_Ch1);
IF rTempDiff > rTMR_TempDiscrepancyLimit_degC THEN
    tBed2_Out_DiscTimer_31 := tBed2_Out_DiscTimer_31 + 1.0;
ELSE
    tBed2_Out_DiscTimer_31 := 0.0;
END_IF;

bBed2_Out_Ch1_Fault := (tBed2_Out_DiscTimer_12 > rTMR_DiscrepancyTripTime_s AND tBed2_Out_DiscTimer_31 > rTMR_DiscrepancyTripTime_s)
                       OR (rT_Bed2_Out_Ch1 < 300.0 OR rT_Bed2_Out_Ch1 > 650.0);
bBed2_Out_Ch2_Fault := (tBed2_Out_DiscTimer_12 > rTMR_DiscrepancyTripTime_s AND tBed2_Out_DiscTimer_23 > rTMR_DiscrepancyTripTime_s)
                       OR (rT_Bed2_Out_Ch2 < 300.0 OR rT_Bed2_Out_Ch2 > 650.0);
bBed2_Out_Ch3_Fault := (tBed2_Out_DiscTimer_23 > rTMR_DiscrepancyTripTime_s AND tBed2_Out_DiscTimer_31 > rTMR_DiscrepancyTripTime_s)
                       OR (rT_Bed2_Out_Ch3 < 300.0 OR rT_Bed2_Out_Ch3 > 650.0);

IF NOT bBed2_Out_Ch1_Fault AND NOT bBed2_Out_Ch2_Fault AND NOT bBed2_Out_Ch3_Fault THEN
    IF (rT_Bed2_Out_Ch1 >= rT_Bed2_Out_Ch2 AND rT_Bed2_Out_Ch1 <= rT_Bed2_Out_Ch3)
       OR (rT_Bed2_Out_Ch1 >= rT_Bed2_Out_Ch3 AND rT_Bed2_Out_Ch1 <= rT_Bed2_Out_Ch2) THEN
        rVoted_Bed2_Out_degC := rT_Bed2_Out_Ch1;
    ELSIF (rT_Bed2_Out_Ch2 >= rT_Bed2_Out_Ch1 AND rT_Bed2_Out_Ch2 <= rT_Bed2_Out_Ch3)
       OR (rT_Bed2_Out_Ch2 >= rT_Bed2_Out_Ch3 AND rT_Bed2_Out_Ch2 <= rT_Bed2_Out_Ch1) THEN
        rVoted_Bed2_Out_degC := rT_Bed2_Out_Ch2;
    ELSE
        rVoted_Bed2_Out_degC := rT_Bed2_Out_Ch3;
    END_IF;
ELSIF NOT bBed2_Out_Ch1_Fault AND NOT bBed2_Out_Ch2_Fault THEN
    rVoted_Bed2_Out_degC := (rT_Bed2_Out_Ch1 + rT_Bed2_Out_Ch2) * 0.5;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000001;
ELSIF NOT bBed2_Out_Ch2_Fault AND NOT bBed2_Out_Ch3_Fault THEN
    rVoted_Bed2_Out_degC := (rT_Bed2_Out_Ch2 + rT_Bed2_Out_Ch3) * 0.5;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000001;
ELSIF NOT bBed2_Out_Ch1_Fault AND NOT bBed2_Out_Ch3_Fault THEN
    rVoted_Bed2_Out_degC := (rT_Bed2_Out_Ch1 + rT_Bed2_Out_Ch3) * 0.5;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000001;
ELSIF NOT bBed2_Out_Ch1_Fault THEN
    rVoted_Bed2_Out_degC := rT_Bed2_Out_Ch1;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000002;
ELSIF NOT bBed2_Out_Ch2_Fault THEN
    rVoted_Bed2_Out_degC := rT_Bed2_Out_Ch2;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000002;
ELSIF NOT bBed2_Out_Ch3_Fault THEN
    rVoted_Bed2_Out_degC := rT_Bed2_Out_Ch3;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000002;
ELSE
    rVoted_Bed2_Out_degC := 480.0;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000004;
END_IF;

(* --- 1.5: REACTOR BED 3 INLET TEMPERATURE 2oo3 VOTING --- *)
rTempDiff := ABS(rT_Bed3_In_Ch1 - rT_Bed3_In_Ch2);
IF rTempDiff > rTMR_TempDiscrepancyLimit_degC THEN
    tBed3_In_DiscTimer_12 := tBed3_In_DiscTimer_12 + 1.0;
ELSE
    tBed3_In_DiscTimer_12 := 0.0;
END_IF;

rTempDiff := ABS(rT_Bed3_In_Ch2 - rT_Bed3_In_Ch3);
IF rTempDiff > rTMR_TempDiscrepancyLimit_degC THEN
    tBed3_In_DiscTimer_23 := tBed3_In_DiscTimer_23 + 1.0;
ELSE
    tBed3_In_DiscTimer_23 := 0.0;
END_IF;

rTempDiff := ABS(rT_Bed3_In_Ch3 - rT_Bed3_In_Ch1);
IF rTempDiff > rTMR_TempDiscrepancyLimit_degC THEN
    tBed3_In_DiscTimer_31 := tBed3_In_DiscTimer_31 + 1.0;
ELSE
    tBed3_In_DiscTimer_31 := 0.0;
END_IF;

bBed3_In_Ch1_Fault := (tBed3_In_DiscTimer_12 > rTMR_DiscrepancyTripTime_s AND tBed3_In_DiscTimer_31 > rTMR_DiscrepancyTripTime_s)
                      OR (rT_Bed3_In_Ch1 < 300.0 OR rT_Bed3_In_Ch1 > 650.0);
bBed3_In_Ch2_Fault := (tBed3_In_DiscTimer_12 > rTMR_DiscrepancyTripTime_s AND tBed3_In_DiscTimer_23 > rTMR_DiscrepancyTripTime_s)
                      OR (rT_Bed3_In_Ch2 < 300.0 OR rT_Bed3_In_Ch2 > 650.0);
bBed3_In_Ch3_Fault := (tBed3_In_DiscTimer_23 > rTMR_DiscrepancyTripTime_s AND tBed3_In_DiscTimer_31 > rTMR_DiscrepancyTripTime_s)
                      OR (rT_Bed3_In_Ch3 < 300.0 OR rT_Bed3_In_Ch3 > 650.0);

IF NOT bBed3_In_Ch1_Fault AND NOT bBed3_In_Ch2_Fault AND NOT bBed3_In_Ch3_Fault THEN
    IF (rT_Bed3_In_Ch1 >= rT_Bed3_In_Ch2 AND rT_Bed3_In_Ch1 <= rT_Bed3_In_Ch3)
       OR (rT_Bed3_In_Ch1 >= rT_Bed3_In_Ch3 AND rT_Bed3_In_Ch1 <= rT_Bed3_In_Ch2) THEN
        rVoted_Bed3_In_degC := rT_Bed3_In_Ch1;
    ELSIF (rT_Bed3_In_Ch2 >= rT_Bed3_In_Ch1 AND rT_Bed3_In_Ch2 <= rT_Bed3_In_Ch3)
       OR (rT_Bed3_In_Ch2 >= rT_Bed3_In_Ch3 AND rT_Bed3_In_Ch2 <= rT_Bed3_In_Ch1) THEN
        rVoted_Bed3_In_degC := rT_Bed3_In_Ch2;
    ELSE
        rVoted_Bed3_In_degC := rT_Bed3_In_Ch3;
    END_IF;
ELSIF NOT bBed3_In_Ch1_Fault AND NOT bBed3_In_Ch2_Fault THEN
    rVoted_Bed3_In_degC := (rT_Bed3_In_Ch1 + rT_Bed3_In_Ch2) * 0.5;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000001;
ELSIF NOT bBed3_In_Ch2_Fault AND NOT bBed3_In_Ch3_Fault THEN
    rVoted_Bed3_In_degC := (rT_Bed3_In_Ch2 + rT_Bed3_In_Ch3) * 0.5;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000001;
ELSIF NOT bBed3_In_Ch1_Fault AND NOT bBed3_In_Ch3_Fault THEN
    rVoted_Bed3_In_degC := (rT_Bed3_In_Ch1 + rT_Bed3_In_Ch3) * 0.5;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000001;
ELSIF NOT bBed3_In_Ch1_Fault THEN
    rVoted_Bed3_In_degC := rT_Bed3_In_Ch1;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000002;
ELSIF NOT bBed3_In_Ch2_Fault THEN
    rVoted_Bed3_In_degC := rT_Bed3_In_Ch2;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000002;
ELSIF NOT bBed3_In_Ch3_Fault THEN
    rVoted_Bed3_In_degC := rT_Bed3_In_Ch3;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000002;
ELSE
    rVoted_Bed3_In_degC := 520.0;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000004;
END_IF;

(* --- 1.6: REACTOR BED 3 OUTLET TEMPERATURE 2oo3 VOTING --- *)
rTempDiff := ABS(rT_Bed3_Out_Ch1 - rT_Bed3_Out_Ch2);
IF rTempDiff > rTMR_TempDiscrepancyLimit_degC THEN
    tBed3_Out_DiscTimer_12 := tBed3_Out_DiscTimer_12 + 1.0;
ELSE
    tBed3_Out_DiscTimer_12 := 0.0;
END_IF;

rTempDiff := ABS(rT_Bed3_Out_Ch2 - rT_Bed3_Out_Ch3);
IF rTempDiff > rTMR_TempDiscrepancyLimit_degC THEN
    tBed3_Out_DiscTimer_23 := tBed3_Out_DiscTimer_23 + 1.0;
ELSE
    tBed3_Out_DiscTimer_23 := 0.0;
END_IF;

rTempDiff := ABS(rT_Bed3_Out_Ch3 - rT_Bed3_Out_Ch1);
IF rTempDiff > rTMR_TempDiscrepancyLimit_degC THEN
    tBed3_Out_DiscTimer_31 := tBed3_Out_DiscTimer_31 + 1.0;
ELSE
    tBed3_Out_DiscTimer_31 := 0.0;
END_IF;

bBed3_Out_Ch1_Fault := (tBed3_Out_DiscTimer_12 > rTMR_DiscrepancyTripTime_s AND tBed3_Out_DiscTimer_31 > rTMR_DiscrepancyTripTime_s)
                       OR (rT_Bed3_Out_Ch1 < 300.0 OR rT_Bed3_Out_Ch1 > 650.0);
bBed3_Out_Ch2_Fault := (tBed3_Out_DiscTimer_12 > rTMR_DiscrepancyTripTime_s AND tBed3_Out_DiscTimer_23 > rTMR_DiscrepancyTripTime_s)
                       OR (rT_Bed3_Out_Ch2 < 300.0 OR rT_Bed3_Out_Ch2 > 650.0);
bBed3_Out_Ch3_Fault := (tBed3_Out_DiscTimer_23 > rTMR_DiscrepancyTripTime_s AND tBed3_Out_DiscTimer_31 > rTMR_DiscrepancyTripTime_s)
                       OR (rT_Bed3_Out_Ch3 < 300.0 OR rT_Bed3_Out_Ch3 > 650.0);

IF NOT bBed3_Out_Ch1_Fault AND NOT bBed3_Out_Ch2_Fault AND NOT bBed3_Out_Ch3_Fault THEN
    IF (rT_Bed3_Out_Ch1 >= rT_Bed3_Out_Ch2 AND rT_Bed3_Out_Ch1 <= rT_Bed3_Out_Ch3)
       OR (rT_Bed3_Out_Ch1 >= rT_Bed3_Out_Ch3 AND rT_Bed3_Out_Ch1 <= rT_Bed3_Out_Ch2) THEN
        rVoted_Bed3_Out_degC := rT_Bed3_Out_Ch1;
    ELSIF (rT_Bed3_Out_Ch2 >= rT_Bed3_Out_Ch1 AND rT_Bed3_Out_Ch2 <= rT_Bed3_Out_Ch3)
       OR (rT_Bed3_Out_Ch2 >= rT_Bed3_Out_Ch3 AND rT_Bed3_Out_Ch2 <= rT_Bed3_Out_Ch1) THEN
        rVoted_Bed3_Out_degC := rT_Bed3_Out_Ch2;
    ELSE
        rVoted_Bed3_Out_degC := rT_Bed3_Out_Ch3;
    END_IF;
ELSIF NOT bBed3_Out_Ch1_Fault AND NOT bBed3_Out_Ch2_Fault THEN
    rVoted_Bed3_Out_degC := (rT_Bed3_Out_Ch1 + rT_Bed3_Out_Ch2) * 0.5;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000001;
ELSIF NOT bBed3_Out_Ch2_Fault AND NOT bBed3_Out_Ch3_Fault THEN
    rVoted_Bed3_Out_degC := (rT_Bed3_Out_Ch2 + rT_Bed3_Out_Ch3) * 0.5;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000001;
ELSIF NOT bBed3_Out_Ch1_Fault AND NOT bBed3_Out_Ch3_Fault THEN
    rVoted_Bed3_Out_degC := (rT_Bed3_Out_Ch1 + rT_Bed3_Out_Ch3) * 0.5;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000001;
ELSIF NOT bBed3_Out_Ch1_Fault THEN
    rVoted_Bed3_Out_degC := rT_Bed3_Out_Ch1;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000002;
ELSIF NOT bBed3_Out_Ch2_Fault THEN
    rVoted_Bed3_Out_degC := rT_Bed3_Out_Ch2;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000002;
ELSIF NOT bBed3_Out_Ch3_Fault THEN
    rVoted_Bed3_Out_degC := rT_Bed3_Out_Ch3;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000002;
ELSE
    rVoted_Bed3_Out_degC := 500.0;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000004;
END_IF;

(* --- 1.7: REACTOR BED 4 INLET TEMPERATURE 2oo3 VOTING --- *)
rTempDiff := ABS(rT_Bed4_In_Ch1 - rT_Bed4_In_Ch2);
IF rTempDiff > rTMR_TempDiscrepancyLimit_degC THEN
    tBed4_In_DiscTimer_12 := tBed4_In_DiscTimer_12 + 1.0;
ELSE
    tBed4_In_DiscTimer_12 := 0.0;
END_IF;

rTempDiff := ABS(rT_Bed4_In_Ch2 - rT_Bed4_In_Ch3);
IF rTempDiff > rTMR_TempDiscrepancyLimit_degC THEN
    tBed4_In_DiscTimer_23 := tBed4_In_DiscTimer_23 + 1.0;
ELSE
    tBed4_In_DiscTimer_23 := 0.0;
END_IF;

rTempDiff := ABS(rT_Bed4_In_Ch3 - rT_Bed4_In_Ch1);
IF rTempDiff > rTMR_TempDiscrepancyLimit_degC THEN
    tBed4_In_DiscTimer_31 := tBed4_In_DiscTimer_31 + 1.0;
ELSE
    tBed4_In_DiscTimer_31 := 0.0;
END_IF;

bBed4_In_Ch1_Fault := (tBed4_In_DiscTimer_12 > rTMR_DiscrepancyTripTime_s AND tBed4_In_DiscTimer_31 > rTMR_DiscrepancyTripTime_s)
                      OR (rT_Bed4_In_Ch1 < 300.0 OR rT_Bed4_In_Ch1 > 650.0);
bBed4_In_Ch2_Fault := (tBed4_In_DiscTimer_12 > rTMR_DiscrepancyTripTime_s AND tBed4_In_DiscTimer_23 > rTMR_DiscrepancyTripTime_s)
                      OR (rT_Bed4_In_Ch2 < 300.0 OR rT_Bed4_In_Ch2 > 650.0);
bBed4_In_Ch3_Fault := (tBed4_In_DiscTimer_23 > rTMR_DiscrepancyTripTime_s AND tBed4_In_DiscTimer_31 > rTMR_DiscrepancyTripTime_s)
                      OR (rT_Bed4_In_Ch3 < 300.0 OR rT_Bed4_In_Ch3 > 650.0);

IF NOT bBed4_In_Ch1_Fault AND NOT bBed4_In_Ch2_Fault AND NOT bBed4_In_Ch3_Fault THEN
    IF (rT_Bed4_In_Ch1 >= rT_Bed4_In_Ch2 AND rT_Bed4_In_Ch1 <= rT_Bed4_In_Ch3)
       OR (rT_Bed4_In_Ch1 >= rT_Bed4_In_Ch3 AND rT_Bed4_In_Ch1 <= rT_Bed4_In_Ch2) THEN
        rVoted_Bed4_In_degC := rT_Bed4_In_Ch1;
    ELSIF (rT_Bed4_In_Ch2 >= rT_Bed4_In_Ch1 AND rT_Bed4_In_Ch2 <= rT_Bed4_In_Ch3)
       OR (rT_Bed4_In_Ch2 >= rT_Bed4_In_Ch3 AND rT_Bed4_In_Ch2 <= rT_Bed4_In_Ch1) THEN
        rVoted_Bed4_In_degC := rT_Bed4_In_Ch2;
    ELSE
        rVoted_Bed4_In_degC := rT_Bed4_In_Ch3;
    END_IF;
ELSIF NOT bBed4_In_Ch1_Fault AND NOT bBed4_In_Ch2_Fault THEN
    rVoted_Bed4_In_degC := (rT_Bed4_In_Ch1 + rT_Bed4_In_Ch2) * 0.5;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000001;
ELSIF NOT bBed4_In_Ch2_Fault AND NOT bBed4_In_Ch3_Fault THEN
    rVoted_Bed4_In_degC := (rT_Bed4_In_Ch2 + rT_Bed4_In_Ch3) * 0.5;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000001;
ELSIF NOT bBed4_In_Ch1_Fault AND NOT bBed4_In_Ch3_Fault THEN
    rVoted_Bed4_In_degC := (rT_Bed4_In_Ch1 + rT_Bed4_In_Ch3) * 0.5;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000001;
ELSIF NOT bBed4_In_Ch1_Fault THEN
    rVoted_Bed4_In_degC := rT_Bed4_In_Ch1;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000002;
ELSIF NOT bBed4_In_Ch2_Fault THEN
    rVoted_Bed4_In_degC := rT_Bed4_In_Ch2;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000002;
ELSIF NOT bBed4_In_Ch3_Fault THEN
    rVoted_Bed4_In_degC := rT_Bed4_In_Ch3;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000002;
ELSE
    rVoted_Bed4_In_degC := 525.0;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000004;
END_IF;

(* --- 1.8: REACTOR BED 4 OUTLET TEMPERATURE 2oo3 VOTING --- *)
rTempDiff := ABS(rT_Bed4_Out_Ch1 - rT_Bed4_Out_Ch2);
IF rTempDiff > rTMR_TempDiscrepancyLimit_degC THEN
    tBed4_Out_DiscTimer_12 := tBed4_Out_DiscTimer_12 + 1.0;
ELSE
    tBed4_Out_DiscTimer_12 := 0.0;
END_IF;

rTempDiff := ABS(rT_Bed4_Out_Ch2 - rT_Bed4_Out_Ch3);
IF rTempDiff > rTMR_TempDiscrepancyLimit_degC THEN
    tBed4_Out_DiscTimer_23 := tBed4_Out_DiscTimer_23 + 1.0;
ELSE
    tBed4_Out_DiscTimer_23 := 0.0;
END_IF;

rTempDiff := ABS(rT_Bed4_Out_Ch3 - rT_Bed4_Out_Ch1);
IF rTempDiff > rTMR_TempDiscrepancyLimit_degC THEN
    tBed4_Out_DiscTimer_31 := tBed4_Out_DiscTimer_31 + 1.0;
ELSE
    tBed4_Out_DiscTimer_31 := 0.0;
END_IF;

bBed4_Out_Ch1_Fault := (tBed4_Out_DiscTimer_12 > rTMR_DiscrepancyTripTime_s AND tBed4_Out_DiscTimer_31 > rTMR_DiscrepancyTripTime_s)
                       OR (rT_Bed4_Out_Ch1 < 300.0 OR rT_Bed4_Out_Ch1 > 650.0);
bBed4_Out_Ch2_Fault := (tBed4_Out_DiscTimer_12 > rTMR_DiscrepancyTripTime_s AND tBed4_Out_DiscTimer_23 > rTMR_DiscrepancyTripTime_s)
                       OR (rT_Bed4_Out_Ch2 < 300.0 OR rT_Bed4_Out_Ch2 > 650.0);
bBed4_Out_Ch3_Fault := (tBed4_Out_DiscTimer_23 > rTMR_DiscrepancyTripTime_s AND tBed4_Out_DiscTimer_31 > rTMR_DiscrepancyTripTime_s)
                       OR (rT_Bed4_Out_Ch3 < 300.0 OR rT_Bed4_Out_Ch3 > 650.0);

IF NOT bBed4_Out_Ch1_Fault AND NOT bBed4_Out_Ch2_Fault AND NOT bBed4_Out_Ch3_Fault THEN
    IF (rT_Bed4_Out_Ch1 >= rT_Bed4_Out_Ch2 AND rT_Bed4_Out_Ch1 <= rT_Bed4_Out_Ch3)
       OR (rT_Bed4_Out_Ch1 >= rT_Bed4_Out_Ch3 AND rT_Bed4_Out_Ch1 <= rT_Bed4_Out_Ch2) THEN
        rVoted_Bed4_Out_degC := rT_Bed4_Out_Ch1;
    ELSIF (rT_Bed4_Out_Ch2 >= rT_Bed4_Out_Ch1 AND rT_Bed4_Out_Ch2 <= rT_Bed4_Out_Ch3)
       OR (rT_Bed4_Out_Ch2 >= rT_Bed4_Out_Ch3 AND rT_Bed4_Out_Ch2 <= rT_Bed4_Out_Ch1) THEN
        rVoted_Bed4_Out_degC := rT_Bed4_Out_Ch2;
    ELSE
        rVoted_Bed4_Out_degC := rT_Bed4_Out_Ch3;
    END_IF;
ELSIF NOT bBed4_Out_Ch1_Fault AND NOT bBed4_Out_Ch2_Fault THEN
    rVoted_Bed4_Out_degC := (rT_Bed4_Out_Ch1 + rT_Bed4_Out_Ch2) * 0.5;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000001;
ELSIF NOT bBed4_Out_Ch2_Fault AND NOT bBed4_Out_Ch3_Fault THEN
    rVoted_Bed4_Out_degC := (rT_Bed4_Out_Ch2 + rT_Bed4_Out_Ch3) * 0.5;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000001;
ELSIF NOT bBed4_Out_Ch1_Fault AND NOT bBed4_Out_Ch3_Fault THEN
    rVoted_Bed4_Out_degC := (rT_Bed4_Out_Ch1 + rT_Bed4_Out_Ch3) * 0.5;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000001;
ELSIF NOT bBed4_Out_Ch1_Fault THEN
    rVoted_Bed4_Out_degC := rT_Bed4_Out_Ch1;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000002;
ELSIF NOT bBed4_Out_Ch2_Fault THEN
    rVoted_Bed4_Out_degC := rT_Bed4_Out_Ch2;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000002;
ELSIF NOT bBed4_Out_Ch3_Fault THEN
    rVoted_Bed4_Out_degC := rT_Bed4_Out_Ch3;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000002;
ELSE
    rVoted_Bed4_Out_degC := 515.0;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000004;
END_IF;

(* --- 1.9: FURNACE FUEL GAS MANIFOLD PRESSURE 2oo3 VOTING --- *)
rTempDiff := ABS(rP_FuelGas_Ch1 - rP_FuelGas_Ch2);
IF rTempDiff > rTMR_PressDiscrepancyLimit_bar THEN
    tFuelGas_P_DiscTimer_12 := tFuelGas_P_DiscTimer_12 + 1.0;
ELSE
    tFuelGas_P_DiscTimer_12 := 0.0;
END_IF;

rTempDiff := ABS(rP_FuelGas_Ch2 - rP_FuelGas_Ch3);
IF rTempDiff > rTMR_PressDiscrepancyLimit_bar THEN
    tFuelGas_P_DiscTimer_23 := tFuelGas_P_DiscTimer_23 + 1.0;
ELSE
    tFuelGas_P_DiscTimer_23 := 0.0;
END_IF;

rTempDiff := ABS(rP_FuelGas_Ch3 - rP_FuelGas_Ch1);
IF rTempDiff > rTMR_PressDiscrepancyLimit_bar THEN
    tFuelGas_P_DiscTimer_31 := tFuelGas_P_DiscTimer_31 + 1.0;
ELSE
    tFuelGas_P_DiscTimer_31 := 0.0;
END_IF;

bFuelGas_P_Ch1_Fault := (tFuelGas_P_DiscTimer_12 > rTMR_DiscrepancyTripTime_s AND tFuelGas_P_DiscTimer_31 > rTMR_DiscrepancyTripTime_s)
                        OR (rP_FuelGas_Ch1 < 0.20 OR rP_FuelGas_Ch1 > 6.0);
bFuelGas_P_Ch2_Fault := (tFuelGas_P_DiscTimer_12 > rTMR_DiscrepancyTripTime_s AND tFuelGas_P_DiscTimer_23 > rTMR_DiscrepancyTripTime_s)
                        OR (rP_FuelGas_Ch2 < 0.20 OR rP_FuelGas_Ch2 > 6.0);
bFuelGas_P_Ch3_Fault := (tFuelGas_P_DiscTimer_23 > rTMR_DiscrepancyTripTime_s AND tFuelGas_P_DiscTimer_31 > rTMR_DiscrepancyTripTime_s)
                        OR (rP_FuelGas_Ch3 < 0.20 OR rP_FuelGas_Ch3 > 6.0);

IF NOT bFuelGas_P_Ch1_Fault AND NOT bFuelGas_P_Ch2_Fault AND NOT bFuelGas_P_Ch3_Fault THEN
    IF (rP_FuelGas_Ch1 >= rP_FuelGas_Ch2 AND rP_FuelGas_Ch1 <= rP_FuelGas_Ch3)
       OR (rP_FuelGas_Ch1 >= rP_FuelGas_Ch3 AND rP_FuelGas_Ch1 <= rP_FuelGas_Ch2) THEN
        rVoted_FuelGas_P_bar := rP_FuelGas_Ch1;
    ELSIF (rP_FuelGas_Ch2 >= rP_FuelGas_Ch1 AND rP_FuelGas_Ch2 <= rP_FuelGas_Ch3)
       OR (rP_FuelGas_Ch2 >= rP_FuelGas_Ch3 AND rP_FuelGas_Ch2 <= rP_FuelGas_Ch1) THEN
        rVoted_FuelGas_P_bar := rP_FuelGas_Ch2;
    ELSE
        rVoted_FuelGas_P_bar := rP_FuelGas_Ch3;
    END_IF;
ELSIF NOT bFuelGas_P_Ch1_Fault AND NOT bFuelGas_P_Ch2_Fault THEN
    rVoted_FuelGas_P_bar := (rP_FuelGas_Ch1 + rP_FuelGas_Ch2) * 0.5;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000010;
ELSIF NOT bFuelGas_P_Ch2_Fault AND NOT bFuelGas_P_Ch3_Fault THEN
    rVoted_FuelGas_P_bar := (rP_FuelGas_Ch2 + rP_FuelGas_Ch3) * 0.5;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000010;
ELSIF NOT bFuelGas_P_Ch1_Fault AND NOT bFuelGas_P_Ch3_Fault THEN
    rVoted_FuelGas_P_bar := (rP_FuelGas_Ch1 + rP_FuelGas_Ch3) * 0.5;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000010;
ELSIF NOT bFuelGas_P_Ch1_Fault THEN
    rVoted_FuelGas_P_bar := rP_FuelGas_Ch1;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000020;
ELSIF NOT bFuelGas_P_Ch2_Fault THEN
    rVoted_FuelGas_P_bar := rP_FuelGas_Ch2;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000020;
ELSIF NOT bFuelGas_P_Ch3_Fault THEN
    rVoted_FuelGas_P_bar := rP_FuelGas_Ch3;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000020;
ELSE
    rVoted_FuelGas_P_bar := 0.50; (* Trips Burner Low Pressure Interlock *)
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000040;
END_IF;

(* --- 1.10: FURNACE FUEL GAS TOTAL HEADER FLOW 2oo3 VOTING --- *)
rTempDiff := ABS(rF_FuelGas_Ch1 - rF_FuelGas_Ch2);
IF rTempDiff > rTMR_FlowDiscrepancyLimit_Nm3h THEN
    tFuelGas_F_DiscTimer_12 := tFuelGas_F_DiscTimer_12 + 1.0;
ELSE
    tFuelGas_F_DiscTimer_12 := 0.0;
END_IF;

rTempDiff := ABS(rF_FuelGas_Ch2 - rF_FuelGas_Ch3);
IF rTempDiff > rTMR_FlowDiscrepancyLimit_Nm3h THEN
    tFuelGas_F_DiscTimer_23 := tFuelGas_F_DiscTimer_23 + 1.0;
ELSE
    tFuelGas_F_DiscTimer_23 := 0.0;
END_IF;

rTempDiff := ABS(rF_FuelGas_Ch3 - rF_FuelGas_Ch1);
IF rTempDiff > rTMR_FlowDiscrepancyLimit_Nm3h THEN
    tFuelGas_F_DiscTimer_31 := tFuelGas_F_DiscTimer_31 + 1.0;
ELSE
    tFuelGas_F_DiscTimer_31 := 0.0;
END_IF;

bFuelGas_F_Ch1_Fault := (tFuelGas_F_DiscTimer_12 > rTMR_DiscrepancyTripTime_s AND tFuelGas_F_DiscTimer_31 > rTMR_DiscrepancyTripTime_s)
                        OR (rF_FuelGas_Ch1 < 100.0 OR rF_FuelGas_Ch1 > 20000.0);
bFuelGas_F_Ch2_Fault := (tFuelGas_F_DiscTimer_12 > rTMR_DiscrepancyTripTime_s AND tFuelGas_F_DiscTimer_23 > rTMR_DiscrepancyTripTime_s)
                        OR (rF_FuelGas_Ch2 < 100.0 OR rF_FuelGas_Ch2 > 20000.0);
bFuelGas_F_Ch3_Fault := (tFuelGas_F_DiscTimer_23 > rTMR_DiscrepancyTripTime_s AND tFuelGas_F_DiscTimer_31 > rTMR_DiscrepancyTripTime_s)
                        OR (rF_FuelGas_Ch3 < 100.0 OR rF_FuelGas_Ch3 > 20000.0);

IF NOT bFuelGas_F_Ch1_Fault AND NOT bFuelGas_F_Ch2_Fault AND NOT bFuelGas_F_Ch3_Fault THEN
    IF (rF_FuelGas_Ch1 >= rF_FuelGas_Ch2 AND rF_FuelGas_Ch1 <= rF_FuelGas_Ch3)
       OR (rF_FuelGas_Ch1 >= rF_FuelGas_Ch3 AND rF_FuelGas_Ch1 <= rF_FuelGas_Ch2) THEN
        rVoted_FuelGas_Flow_Nm3h := rF_FuelGas_Ch1;
    ELSIF (rF_FuelGas_Ch2 >= rF_FuelGas_Ch1 AND rF_FuelGas_Ch2 <= rF_FuelGas_Ch3)
       OR (rF_FuelGas_Ch2 >= rF_FuelGas_Ch3 AND rF_FuelGas_Ch2 <= rF_FuelGas_Ch1) THEN
        rVoted_FuelGas_Flow_Nm3h := rF_FuelGas_Ch2;
    ELSE
        rVoted_FuelGas_Flow_Nm3h := rF_FuelGas_Ch3;
    END_IF;
ELSIF NOT bFuelGas_F_Ch1_Fault AND NOT bFuelGas_F_Ch2_Fault THEN
    rVoted_FuelGas_Flow_Nm3h := (rF_FuelGas_Ch1 + rF_FuelGas_Ch2) * 0.5;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000010;
ELSIF NOT bFuelGas_F_Ch2_Fault AND NOT bFuelGas_F_Ch3_Fault THEN
    rVoted_FuelGas_Flow_Nm3h := (rF_FuelGas_Ch2 + rF_FuelGas_Ch3) * 0.5;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000010;
ELSIF NOT bFuelGas_F_Ch1_Fault AND NOT bFuelGas_F_Ch3_Fault THEN
    rVoted_FuelGas_Flow_Nm3h := (rF_FuelGas_Ch1 + rF_FuelGas_Ch3) * 0.5;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000010;
ELSIF NOT bFuelGas_F_Ch1_Fault THEN
    rVoted_FuelGas_Flow_Nm3h := rF_FuelGas_Ch1;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000020;
ELSIF NOT bFuelGas_F_Ch2_Fault THEN
    rVoted_FuelGas_Flow_Nm3h := rF_FuelGas_Ch2;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000020;
ELSIF NOT bFuelGas_F_Ch3_Fault THEN
    rVoted_FuelGas_Flow_Nm3h := rF_FuelGas_Ch3;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000020;
ELSE
    rVoted_FuelGas_Flow_Nm3h := 0.0;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000040;
END_IF;

(* --- 1.11: RECYCLE COMPRESSOR SUCTION DRUM LIQUID LEVEL 2oo3 VOTING --- *)
rTempDiff := ABS(rSuctionDrum_Level_Ch1 - rSuctionDrum_Level_Ch2);
IF rTempDiff > rTMR_LevelDiscrepancyLimit_Pct THEN
    tSuctionDrum_L_DiscTimer_12 := tSuctionDrum_L_DiscTimer_12 + 1.0;
ELSE
    tSuctionDrum_L_DiscTimer_12 := 0.0;
END_IF;

rTempDiff := ABS(rSuctionDrum_Level_Ch2 - rSuctionDrum_Level_Ch3);
IF rTempDiff > rTMR_LevelDiscrepancyLimit_Pct THEN
    tSuctionDrum_L_DiscTimer_23 := tSuctionDrum_L_DiscTimer_23 + 1.0;
ELSE
    tSuctionDrum_L_DiscTimer_23 := 0.0;
END_IF;

rTempDiff := ABS(rSuctionDrum_Level_Ch3 - rSuctionDrum_Level_Ch1);
IF rTempDiff > rTMR_LevelDiscrepancyLimit_Pct THEN
    tSuctionDrum_L_DiscTimer_31 := tSuctionDrum_L_DiscTimer_31 + 1.0;
ELSE
    tSuctionDrum_L_DiscTimer_31 := 0.0;
END_IF;

bSuctionDrum_L_Ch1_Fault := (tSuctionDrum_L_DiscTimer_12 > rTMR_DiscrepancyTripTime_s AND tSuctionDrum_L_DiscTimer_31 > rTMR_DiscrepancyTripTime_s)
                            OR (rSuctionDrum_Level_Ch1 < -5.0 OR rSuctionDrum_Level_Ch1 > 105.0);
bSuctionDrum_L_Ch2_Fault := (tSuctionDrum_L_DiscTimer_12 > rTMR_DiscrepancyTripTime_s AND tSuctionDrum_L_DiscTimer_23 > rTMR_DiscrepancyTripTime_s)
                            OR (rSuctionDrum_Level_Ch2 < -5.0 OR rSuctionDrum_Level_Ch2 > 105.0);
bSuctionDrum_L_Ch3_Fault := (tSuctionDrum_L_DiscTimer_23 > rTMR_DiscrepancyTripTime_s AND tSuctionDrum_L_DiscTimer_31 > rTMR_DiscrepancyTripTime_s)
                            OR (rSuctionDrum_Level_Ch3 < -5.0 OR rSuctionDrum_Level_Ch3 > 105.0);

IF NOT bSuctionDrum_L_Ch1_Fault AND NOT bSuctionDrum_L_Ch2_Fault AND NOT bSuctionDrum_L_Ch3_Fault THEN
    IF (rSuctionDrum_Level_Ch1 >= rSuctionDrum_Level_Ch2 AND rSuctionDrum_Level_Ch1 <= rSuctionDrum_Level_Ch3)
       OR (rSuctionDrum_Level_Ch1 >= rSuctionDrum_Level_Ch3 AND rSuctionDrum_Level_Ch1 <= rSuctionDrum_Level_Ch2) THEN
        rVoted_SuctionDrum_Level_Pct := rSuctionDrum_Level_Ch1;
    ELSIF (rSuctionDrum_Level_Ch2 >= rSuctionDrum_Level_Ch1 AND rSuctionDrum_Level_Ch2 <= rSuctionDrum_Level_Ch3)
       OR (rSuctionDrum_Level_Ch2 >= rSuctionDrum_Level_Ch3 AND rSuctionDrum_Level_Ch2 <= rSuctionDrum_Level_Ch1) THEN
        rVoted_SuctionDrum_Level_Pct := rSuctionDrum_Level_Ch2;
    ELSE
        rVoted_SuctionDrum_Level_Pct := rSuctionDrum_Level_Ch3;
    END_IF;
ELSIF NOT bSuctionDrum_L_Ch1_Fault AND NOT bSuctionDrum_L_Ch2_Fault THEN
    (* Conservative High Selection During Degraded 2-Channel Mode to Protect 15 MW Compressor *)
    IF rSuctionDrum_Level_Ch1 >= rSuctionDrum_Level_Ch2 THEN
        rVoted_SuctionDrum_Level_Pct := rSuctionDrum_Level_Ch1;
    ELSE
        rVoted_SuctionDrum_Level_Pct := rSuctionDrum_Level_Ch2;
    END_IF;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000080;
ELSIF NOT bSuctionDrum_L_Ch2_Fault AND NOT bSuctionDrum_L_Ch3_Fault THEN
    IF rSuctionDrum_Level_Ch2 >= rSuctionDrum_Level_Ch3 THEN
        rVoted_SuctionDrum_Level_Pct := rSuctionDrum_Level_Ch2;
    ELSE
        rVoted_SuctionDrum_Level_Pct := rSuctionDrum_Level_Ch3;
    END_IF;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000080;
ELSIF NOT bSuctionDrum_L_Ch1_Fault AND NOT bSuctionDrum_L_Ch3_Fault THEN
    IF rSuctionDrum_Level_Ch1 >= rSuctionDrum_Level_Ch3 THEN
        rVoted_SuctionDrum_Level_Pct := rSuctionDrum_Level_Ch1;
    ELSE
        rVoted_SuctionDrum_Level_Pct := rSuctionDrum_Level_Ch3;
    END_IF;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000080;
ELSIF NOT bSuctionDrum_L_Ch1_Fault THEN
    rVoted_SuctionDrum_Level_Pct := rSuctionDrum_Level_Ch1;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000100;
ELSIF NOT bSuctionDrum_L_Ch2_Fault THEN
    rVoted_SuctionDrum_Level_Pct := rSuctionDrum_Level_Ch2;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000100;
ELSIF NOT bSuctionDrum_L_Ch3_Fault THEN
    rVoted_SuctionDrum_Level_Pct := rSuctionDrum_Level_Ch3;
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000100;
ELSE
    rVoted_SuctionDrum_Level_Pct := 100.0; (* Trips Compressor on Slug Prevention *)
    dwSystemDiagnostics := dwSystemDiagnostics OR 16#00000200;
END_IF;


(* ====================================================================================================== *)
(* === PHASE 2: THERMODYNAMICS, ARRHENIUS KINETICS, MASS/HEAT BALANCES & YIELD MODELS                 === *)
(* ====================================================================================================== *)

(* --- 2.1: BED TEMPERATURE DROPS (DELTA T) --- *)
rBed1_DeltaT_degC := rVoted_Bed1_In_degC - rVoted_Bed1_Out_degC;
rBed2_DeltaT_degC := rVoted_Bed2_In_degC - rVoted_Bed2_Out_degC;
rBed3_DeltaT_degC := rVoted_Bed3_In_degC - rVoted_Bed3_Out_degC;
rBed4_DeltaT_degC := rVoted_Bed4_In_degC - rVoted_Bed4_Out_degC;

(* --- 2.2: WEIGHTED AVERAGE BED TEMPERATURE (WABT) CALCULATION --- *)
(* WABT = sum(w_i * (T_in,i + 2 * T_out,i) / 3.0) for beds i = 1..4 *)
rCalculated_WABT_degC := rw1_Bed * ((rVoted_Bed1_In_degC + 2.0 * rVoted_Bed1_Out_degC) / 3.0)
                       + rw2_Bed * ((rVoted_Bed2_In_degC + 2.0 * rVoted_Bed2_Out_degC) / 3.0)
                       + rw3_Bed * ((rVoted_Bed3_In_degC + 2.0 * rVoted_Bed3_Out_degC) / 3.0)
                       + rw4_Bed * ((rVoted_Bed4_In_degC + 2.0 * rVoted_Bed4_Out_degC) / 3.0);

(* --- 2.3: FEED FLUID PHYSICAL PROPERTIES & MOLAR FLOWS --- *)
(* Hydrocarbon Mass Flow Rate [kg/h] *)
rTempCalc := rFeedFlow_m3h * rFeedDensity_kgm3;

(* Hydrocarbon Molar Flow Rate [kmol/h] *)
rTempDiff := rTempCalc / rMw_Naphtha_kgkmol;

(* Recycle Gas Hydrogen Molar Flow Rate [kmol/h] *)
(* F_recycle [Nm3/h] / 22.414 [Nm3/kmol] * (mol% H2 / 100.0) *)
rCompressor_VolFlow_m3h := (rRecycleCompressor_Flow_Nm3h / 22.414) * (rRecycleGas_H2Purity_molPct / 100.0);

(* Combined Feed Hydrogen / Hydrocarbon Mole Ratio [mol/mol] *)
IF rTempDiff > 0.01 THEN
    rH2_HC_MoleRatio := rCompressor_VolFlow_m3h / rTempDiff;
ELSE
    rH2_HC_MoleRatio := 0.0;
END_IF;

(* Liquid Hourly Space Velocity (LHSV) [1/h] *)
IF rTotalCatalystVolume_m3 > 0.1 THEN
    rTempCalc := rFeedFlow_m3h / rTotalCatalystVolume_m3;
ELSE
    rTempCalc := 1.60;
END_IF;

(* --- 2.4: REACTION KINETICS & ENDOTHERMIC REACTION DUTY --- *)
(* Bed 1 Mean Absolute Temperature [K] *)
rTempDiff := (rVoted_Bed1_In_degC + rVoted_Bed1_Out_degC) * 0.5 + 273.15;

(* Arrhenius Dehydrogenation Rate Constant: k_naph = k0 * exp(-Ea / (R * T)) *)
(* Approximated numerically to avoid runtime floating overflow in embedded PLCs *)
rTempCalc := -rEa_Naph_Jmol / (rR_GasConstant * rTempDiff);
IF rTempCalc > -50.0 AND rTempCalc < 0.0 THEN
    (* 4th order Taylor expansion approximation of exp(x) around x0 = -20.0 *)
    rTempCalc := rk0_Naph * 2.06115E-9 * (1.0 + (rTempCalc + 20.0) + 0.5 * (rTempCalc + 20.0)*(rTempCalc + 20.0));
ELSE
    rTempCalc := 0.10;
END_IF;

(* Total Reactor Train Endothermic Duty Absorbance [MW] *)
(* Duty = FeedMassFlow [kg/s] * Cp_mix * sum(Delta T_beds) *)
rTotalReactionsDuty_MW := ((rFeedFlow_m3h * rFeedDensity_kgm3 / 3600.0) * rCp_NaphthaVapor_kJkgK
                          + (rRecycleCompressor_Flow_Nm3h * 0.08988 / 3600.0) * rCp_RecycleGas_kJkgK)
                          * (rBed1_DeltaT_degC + rBed2_DeltaT_degC + rBed3_DeltaT_degC + rBed4_DeltaT_degC) / 1000.0;

(* --- 2.5: REFORMATE RESEARCH OCTANE NUMBER (RON) EMPIRICAL PREDICTION MODEL --- *)
(* Multivariable model calibrated against laboratory knock-engine testing *)
(* RON = f(WABT, Feed N+2A, LHSV, Separator P, H2/HC ratio) *)
rPredicted_RON := 71.50
                + 0.1185 * (rCalculated_WABT_degC - 480.0)
                + 0.3350 * (rFeed_N2A_VolPct - 50.0)
                - 0.0420 * (rTempCalc - 1.60)
                - 0.0280 * (rSeparator_P_bar - 5.0)
                + 0.0720 * (rH2_HC_MoleRatio - 4.5);

(* Clamp RON prediction to realistic physical bounds *)
IF rPredicted_RON > 106.0 THEN
    rPredicted_RON := 106.0;
ELSIF rPredicted_RON < 90.0 THEN
    rPredicted_RON := 90.0;
END_IF;

(* --- 2.6: C5+ LIQUID REFORMATE PRODUCT YIELD MODEL [wt %] --- *)
(* Yield decreases as WABT increases due to paraffin hydrocracking *)
rPredicted_C5Plus_Yield_wtPct := 93.20
                               - 0.0890 * (rCalculated_WABT_degC - 480.0)
                               - 0.0380 * (rFeed_N2A_VolPct - 50.0)
                               - 0.4500 * (rSeparator_P_bar - 5.0)
                               + 0.1250 * (rH2_HC_MoleRatio - 4.5);

IF rPredicted_C5Plus_Yield_wtPct > 96.0 THEN
    rPredicted_C5Plus_Yield_wtPct := 96.0;
ELSIF rPredicted_C5Plus_Yield_wtPct < 75.0 THEN
    rPredicted_C5Plus_Yield_wtPct := 75.0;
END_IF;

(* --- 2.7: REGENERATOR COKE COMBUSTION RATE OBSERVER --- *)
(* Based on differential O2 consumption across regenerator flue gas *)
(* Coke combustion stoichiometry: 1 kg carbonaceous coke requires ~1.28 Nm3 O2 *)
IF rRegen_FlueGas_O2_molPct < 15.0 THEN
    rCatalyst_CokeBurnRate_kgh := rCatalyst_CirculationRate_kgh * 0.052 * (1.0 - (rRegen_FlueGas_O2_molPct / 21.0));
ELSE
    rCatalyst_CokeBurnRate_kgh := 0.0;
END_IF;
"""
