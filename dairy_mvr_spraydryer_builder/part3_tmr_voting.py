# dairy_mvr_spraydryer_builder/part3_tmr_voting.py
# Lumina Cyber-Physical Systems Chair - V7 Max-Persona
# Part 3: Phase 1 - 2oo3 TMR Voting Logic with 400 ms Discrepancy Accumulation Timers for 8 Sensor Groups

def get_part3_tmr_voting():
    return """(* === PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING SUITE === *)
(* Increments monotonic real-time execution counter *)
nCycleCounter := nCycleCounter + 1;

(* ------------------------------------------------------------------------------------------------- *)
(* SENSOR GROUP 1: CALANDRIA 1ST EFFECT SUMP LIQUID LEVEL (LT-101A/B/C) [mm]                         *)
(* Calibrated Range: 0.0 to 3000.0 [mm]. Tolerance: 35.0 [mm]. Debounce Limit: 400.0 [ms]           *)
(* ------------------------------------------------------------------------------------------------- *)
rDev_LT101_AB := ABS(rLT_101A_CalandriaLevel_mm - rLT_101B_CalandriaLevel_mm);
rDev_LT101_BC := ABS(rLT_101B_CalandriaLevel_mm - rLT_101C_CalandriaLevel_mm);
rDev_LT101_CA := ABS(rLT_101C_CalandriaLevel_mm - rLT_101A_CalandriaLevel_mm);

(* Pairwise Discrepancy Accumulation Timers *)
IF rDev_LT101_AB > rTol_LT101_mm THEN
    tTimer_LT101_AB := tTimer_LT101_AB + rCycleTime_s;
    IF tTimer_LT101_AB >= 0.400 THEN
        bDiscrepancy_LT101_AB := TRUE;
    END_IF;
ELSE
    tTimer_LT101_AB := 0.0;
    bDiscrepancy_LT101_AB := FALSE;
END_IF;

IF rDev_LT101_BC > rTol_LT101_mm THEN
    tTimer_LT101_BC := tTimer_LT101_BC + rCycleTime_s;
    IF tTimer_LT101_BC >= 0.400 THEN
        bDiscrepancy_LT101_BC := TRUE;
    END_IF;
ELSE
    tTimer_LT101_BC := 0.0;
    bDiscrepancy_LT101_BC := FALSE;
END_IF;

IF rDev_LT101_CA > rTol_LT101_mm THEN
    tTimer_LT101_CA := tTimer_LT101_CA + rCycleTime_s;
    IF tTimer_LT101_CA >= 0.400 THEN
        bDiscrepancy_LT101_CA := TRUE;
    END_IF;
ELSE
    tTimer_LT101_CA := 0.0;
    bDiscrepancy_LT101_CA := FALSE;
END_IF;

(* 2oo3 Voting & Fault Isolation Decision Matrix *)
IF (NOT bDiscrepancy_LT101_AB) AND (NOT bDiscrepancy_LT101_BC) AND (NOT bDiscrepancy_LT101_CA) THEN
    (* All three channels fully concordant: Median calculation *)
    IF (rLT_101A_CalandriaLevel_mm >= rLT_101B_CalandriaLevel_mm AND rLT_101A_CalandriaLevel_mm <= rLT_101C_CalandriaLevel_mm) OR
       (rLT_101A_CalandriaLevel_mm <= rLT_101B_CalandriaLevel_mm AND rLT_101A_CalandriaLevel_mm >= rLT_101C_CalandriaLevel_mm) THEN
        rVoted_CalandriaLevel_mm := rLT_101A_CalandriaLevel_mm;
    ELSIF (rLT_101B_CalandriaLevel_mm >= rLT_101A_CalandriaLevel_mm AND rLT_101B_CalandriaLevel_mm <= rLT_101C_CalandriaLevel_mm) OR
          (rLT_101B_CalandriaLevel_mm <= rLT_101A_CalandriaLevel_mm AND rLT_101B_CalandriaLevel_mm >= rLT_101C_CalandriaLevel_mm) THEN
        rVoted_CalandriaLevel_mm := rLT_101B_CalandriaLevel_mm;
    ELSE
        rVoted_CalandriaLevel_mm := rLT_101C_CalandriaLevel_mm;
    END_IF;
    nDegradedMode_LT101 := 0; (* Healthy 2oo3 *)
    wTmrHealth_LT101 := 16#0007;
ELSIF bDiscrepancy_LT101_AB AND bDiscrepancy_LT101_CA AND (NOT bDiscrepancy_LT101_BC) THEN
    (* Channel A has diverged: Degrade to 1oo2 average of B and C *)
    rVoted_CalandriaLevel_mm := (rLT_101B_CalandriaLevel_mm + rLT_101C_CalandriaLevel_mm) * 0.500;
    nDegradedMode_LT101 := 1; (* Degraded 1oo2 *)
    wTmrHealth_LT101 := 16#0006; (* Channel A Faulty *)
ELSIF bDiscrepancy_LT101_AB AND bDiscrepancy_LT101_BC AND (NOT bDiscrepancy_LT101_CA) THEN
    (* Channel B has diverged: Degrade to 1oo2 average of A and C *)
    rVoted_CalandriaLevel_mm := (rLT_101A_CalandriaLevel_mm + rLT_101C_CalandriaLevel_mm) * 0.500;
    nDegradedMode_LT101 := 1; (* Degraded 1oo2 *)
    wTmrHealth_LT101 := 16#0005; (* Channel B Faulty *)
ELSIF bDiscrepancy_LT101_BC AND bDiscrepancy_LT101_CA AND (NOT bDiscrepancy_LT101_AB) THEN
    (* Channel C has diverged: Degrade to 1oo2 average of A and B *)
    rVoted_CalandriaLevel_mm := (rLT_101A_CalandriaLevel_mm + rLT_101B_CalandriaLevel_mm) * 0.500;
    nDegradedMode_LT101 := 1; (* Degraded 1oo2 *)
    wTmrHealth_LT101 := 16#0003; (* Channel C Faulty *)
ELSIF bDiscrepancy_LT101_AB AND (NOT bDiscrepancy_LT101_BC) AND (NOT bDiscrepancy_LT101_CA) THEN
    (* Single Pair Discrepancy AB, but C confirms B and A within tolerance: Average of B and C *)
    rVoted_CalandriaLevel_mm := (rLT_101B_CalandriaLevel_mm + rLT_101C_CalandriaLevel_mm) * 0.500;
    nDegradedMode_LT101 := 1;
    wTmrHealth_LT101 := 16#0006;
ELSIF bDiscrepancy_LT101_BC AND (NOT bDiscrepancy_LT101_AB) AND (NOT bDiscrepancy_LT101_CA) THEN
    (* Single Pair Discrepancy BC: Average of A and C *)
    rVoted_CalandriaLevel_mm := (rLT_101A_CalandriaLevel_mm + rLT_101C_CalandriaLevel_mm) * 0.500;
    nDegradedMode_LT101 := 1;
    wTmrHealth_LT101 := 16#0005;
ELSIF bDiscrepancy_LT101_CA AND (NOT bDiscrepancy_LT101_AB) AND (NOT bDiscrepancy_LT101_BC) THEN
    (* Single Pair Discrepancy CA: Average of A and B *)
    rVoted_CalandriaLevel_mm := (rLT_101A_CalandriaLevel_mm + rLT_101B_CalandriaLevel_mm) * 0.500;
    nDegradedMode_LT101 := 1;
    wTmrHealth_LT101 := 16#0003;
ELSE
    (* All pairs mutually discrepant: Failover to freeze previous voted value & latch critical fault *)
    nDegradedMode_LT101 := 3; (* Tripped *)
    wTmrHealth_LT101 := 16#0000;
END_IF;

(* ------------------------------------------------------------------------------------------------- *)
(* SENSOR GROUP 2: IN-LINE OPTICAL BRIX / SOLIDS REFRACTOMETER (DT-201A/B/C) [% TS]                  *)
(* Calibrated Range: 0.0 to 65.0 [% TS]. Tolerance: 0.85 [% TS]. Debounce Limit: 400.0 [ms]         *)
(* ------------------------------------------------------------------------------------------------- *)
rDev_DT201_AB := ABS(rDT_201A_SolidsBrix_pct - rDT_201B_SolidsBrix_pct);
rDev_DT201_BC := ABS(rDT_201B_SolidsBrix_pct - rDT_201C_SolidsBrix_pct);
rDev_DT201_CA := ABS(rDT_201C_SolidsBrix_pct - rDT_201A_SolidsBrix_pct);

IF rDev_DT201_AB > rTol_DT201_pct THEN
    tTimer_DT201_AB := tTimer_DT201_AB + rCycleTime_s;
    IF tTimer_DT201_AB >= 0.400 THEN
        bDiscrepancy_DT201_AB := TRUE;
    END_IF;
ELSE
    tTimer_DT201_AB := 0.0;
    bDiscrepancy_DT201_AB := FALSE;
END_IF;

IF rDev_DT201_BC > rTol_DT201_pct THEN
    tTimer_DT201_BC := tTimer_DT201_BC + rCycleTime_s;
    IF tTimer_DT201_BC >= 0.400 THEN
        bDiscrepancy_DT201_BC := TRUE;
    END_IF;
ELSE
    tTimer_DT201_BC := 0.0;
    bDiscrepancy_DT201_BC := FALSE;
END_IF;

IF rDev_DT201_CA > rTol_DT201_pct THEN
    tTimer_DT201_CA := tTimer_DT201_CA + rCycleTime_s;
    IF tTimer_DT201_CA >= 0.400 THEN
        bDiscrepancy_DT201_CA := TRUE;
    END_IF;
ELSE
    tTimer_DT201_CA := 0.0;
    bDiscrepancy_DT201_CA := FALSE;
END_IF;

IF (NOT bDiscrepancy_DT201_AB) AND (NOT bDiscrepancy_DT201_BC) AND (NOT bDiscrepancy_DT201_CA) THEN
    IF (rDT_201A_SolidsBrix_pct >= rDT_201B_SolidsBrix_pct AND rDT_201A_SolidsBrix_pct <= rDT_201C_SolidsBrix_pct) OR
       (rDT_201A_SolidsBrix_pct <= rDT_201B_SolidsBrix_pct AND rDT_201A_SolidsBrix_pct >= rDT_201C_SolidsBrix_pct) THEN
        rVoted_SolidsBrix_pct := rDT_201A_SolidsBrix_pct;
    ELSIF (rDT_201B_SolidsBrix_pct >= rDT_201A_SolidsBrix_pct AND rDT_201B_SolidsBrix_pct <= rDT_201C_SolidsBrix_pct) OR
          (rDT_201B_SolidsBrix_pct <= rDT_201A_SolidsBrix_pct AND rDT_201B_SolidsBrix_pct >= rDT_201C_SolidsBrix_pct) THEN
        rVoted_SolidsBrix_pct := rDT_201B_SolidsBrix_pct;
    ELSE
        rVoted_SolidsBrix_pct := rDT_201C_SolidsBrix_pct;
    END_IF;
    nDegradedMode_DT201 := 0;
    wTmrHealth_DT201 := 16#0007;
ELSIF bDiscrepancy_DT201_AB AND bDiscrepancy_DT201_CA AND (NOT bDiscrepancy_DT201_BC) THEN
    rVoted_SolidsBrix_pct := (rDT_201B_SolidsBrix_pct + rDT_201C_SolidsBrix_pct) * 0.500;
    nDegradedMode_DT201 := 1;
    wTmrHealth_DT201 := 16#0006;
ELSIF bDiscrepancy_DT201_AB AND bDiscrepancy_DT201_BC AND (NOT bDiscrepancy_DT201_CA) THEN
    rVoted_SolidsBrix_pct := (rDT_201A_SolidsBrix_pct + rDT_201C_SolidsBrix_pct) * 0.500;
    nDegradedMode_DT201 := 1;
    wTmrHealth_DT201 := 16#0005;
ELSIF bDiscrepancy_DT201_BC AND bDiscrepancy_DT201_CA AND (NOT bDiscrepancy_DT201_AB) THEN
    rVoted_SolidsBrix_pct := (rDT_201A_SolidsBrix_pct + rDT_201B_SolidsBrix_pct) * 0.500;
    nDegradedMode_DT201 := 1;
    wTmrHealth_DT201 := 16#0003;
ELSIF bDiscrepancy_DT201_AB AND (NOT bDiscrepancy_DT201_BC) AND (NOT bDiscrepancy_DT201_CA) THEN
    rVoted_SolidsBrix_pct := (rDT_201B_SolidsBrix_pct + rDT_201C_SolidsBrix_pct) * 0.500;
    nDegradedMode_DT201 := 1;
    wTmrHealth_DT201 := 16#0006;
ELSIF bDiscrepancy_DT201_BC AND (NOT bDiscrepancy_DT201_AB) AND (NOT bDiscrepancy_DT201_CA) THEN
    rVoted_SolidsBrix_pct := (rDT_201A_SolidsBrix_pct + rDT_201C_SolidsBrix_pct) * 0.500;
    nDegradedMode_DT201 := 1;
    wTmrHealth_DT201 := 16#0005;
ELSIF bDiscrepancy_DT201_CA AND (NOT bDiscrepancy_DT201_AB) AND (NOT bDiscrepancy_DT201_BC) THEN
    rVoted_SolidsBrix_pct := (rDT_201A_SolidsBrix_pct + rDT_201B_SolidsBrix_pct) * 0.500;
    nDegradedMode_DT201 := 1;
    wTmrHealth_DT201 := 16#0003;
ELSE
    nDegradedMode_DT201 := 3;
    wTmrHealth_DT201 := 16#0000;
END_IF;

(* ------------------------------------------------------------------------------------------------- *)
(* SENSOR GROUP 3: MVR COMPRESSOR DIFFERENTIAL PRESSURE (PDT-301A/B/C) [kPa]                         *)
(* Calibrated Range: 0.0 to 80.0 [kPa]. Tolerance: 2.50 [kPa]. Debounce Limit: 400.0 [ms]           *)
(* ------------------------------------------------------------------------------------------------- *)
rDev_PDT301_AB := ABS(rPDT_301A_MvrDiffPress_kPa - rPDT_301B_MvrDiffPress_kPa);
rDev_PDT301_BC := ABS(rPDT_301B_MvrDiffPress_kPa - rPDT_301C_MvrDiffPress_kPa);
rDev_PDT301_CA := ABS(rPDT_301C_MvrDiffPress_kPa - rPDT_301A_MvrDiffPress_kPa);

IF rDev_PDT301_AB > rTol_PDT301_kPa THEN
    tTimer_PDT301_AB := tTimer_PDT301_AB + rCycleTime_s;
    IF tTimer_PDT301_AB >= 0.400 THEN
        bDiscrepancy_PDT301_AB := TRUE;
    END_IF;
ELSE
    tTimer_PDT301_AB := 0.0;
    bDiscrepancy_PDT301_AB := FALSE;
END_IF;

IF rDev_PDT301_BC > rTol_PDT301_kPa THEN
    tTimer_PDT301_BC := tTimer_PDT301_BC + rCycleTime_s;
    IF tTimer_PDT301_BC >= 0.400 THEN
        bDiscrepancy_PDT301_BC := TRUE;
    END_IF;
ELSE
    tTimer_PDT301_BC := 0.0;
    bDiscrepancy_PDT301_BC := FALSE;
END_IF;

IF rDev_PDT301_CA > rTol_PDT301_kPa THEN
    tTimer_PDT301_CA := tTimer_PDT301_CA + rCycleTime_s;
    IF tTimer_PDT301_CA >= 0.400 THEN
        bDiscrepancy_PDT301_CA := TRUE;
    END_IF;
ELSE
    tTimer_PDT301_CA := 0.0;
    bDiscrepancy_PDT301_CA := FALSE;
END_IF;

IF (NOT bDiscrepancy_PDT301_AB) AND (NOT bDiscrepancy_PDT301_BC) AND (NOT bDiscrepancy_PDT301_CA) THEN
    IF (rPDT_301A_MvrDiffPress_kPa >= rPDT_301B_MvrDiffPress_kPa AND rPDT_301A_MvrDiffPress_kPa <= rPDT_301C_MvrDiffPress_kPa) OR
       (rPDT_301A_MvrDiffPress_kPa <= rPDT_301B_MvrDiffPress_kPa AND rPDT_301A_MvrDiffPress_kPa >= rPDT_301C_MvrDiffPress_kPa) THEN
        rVoted_MvrDiffPress_kPa := rPDT_301A_MvrDiffPress_kPa;
    ELSIF (rPDT_301B_MvrDiffPress_kPa >= rPDT_301A_MvrDiffPress_kPa AND rPDT_301B_MvrDiffPress_kPa <= rPDT_301C_MvrDiffPress_kPa) OR
          (rPDT_301B_MvrDiffPress_kPa <= rPDT_301A_MvrDiffPress_kPa AND rPDT_301B_MvrDiffPress_kPa >= rPDT_301C_MvrDiffPress_kPa) THEN
        rVoted_MvrDiffPress_kPa := rPDT_301B_MvrDiffPress_kPa;
    ELSE
        rVoted_MvrDiffPress_kPa := rPDT_301C_MvrDiffPress_kPa;
    END_IF;
    nDegradedMode_PDT301 := 0;
    wTmrHealth_PDT301 := 16#0007;
ELSIF bDiscrepancy_PDT301_AB AND bDiscrepancy_PDT301_CA AND (NOT bDiscrepancy_PDT301_BC) THEN
    rVoted_MvrDiffPress_kPa := (rPDT_301B_MvrDiffPress_kPa + rPDT_301C_MvrDiffPress_kPa) * 0.500;
    nDegradedMode_PDT301 := 1;
    wTmrHealth_PDT301 := 16#0006;
ELSIF bDiscrepancy_PDT301_AB AND bDiscrepancy_PDT301_BC AND (NOT bDiscrepancy_DT201_CA) THEN
    rVoted_MvrDiffPress_kPa := (rPDT_301A_MvrDiffPress_kPa + rPDT_301C_MvrDiffPress_kPa) * 0.500;
    nDegradedMode_PDT301 := 1;
    wTmrHealth_PDT301 := 16#0005;
ELSIF bDiscrepancy_PDT301_BC AND bDiscrepancy_PDT301_CA AND (NOT bDiscrepancy_PDT301_AB) THEN
    rVoted_MvrDiffPress_kPa := (rPDT_301A_MvrDiffPress_kPa + rPDT_301B_MvrDiffPress_kPa) * 0.500;
    nDegradedMode_PDT301 := 1;
    wTmrHealth_PDT301 := 16#0003;
ELSIF bDiscrepancy_PDT301_AB AND (NOT bDiscrepancy_PDT301_BC) AND (NOT bDiscrepancy_PDT301_CA) THEN
    rVoted_MvrDiffPress_kPa := (rPDT_301B_MvrDiffPress_kPa + rPDT_301C_MvrDiffPress_kPa) * 0.500;
    nDegradedMode_PDT301 := 1;
    wTmrHealth_PDT301 := 16#0006;
ELSIF bDiscrepancy_PDT301_BC AND (NOT bDiscrepancy_PDT301_AB) AND (NOT bDiscrepancy_PDT301_CA) THEN
    rVoted_MvrDiffPress_kPa := (rPDT_301A_MvrDiffPress_kPa + rPDT_301C_MvrDiffPress_kPa) * 0.500;
    nDegradedMode_PDT301 := 1;
    wTmrHealth_PDT301 := 16#0005;
ELSIF bDiscrepancy_PDT301_CA AND (NOT bDiscrepancy_PDT301_AB) AND (NOT bDiscrepancy_PDT301_BC) THEN
    rVoted_MvrDiffPress_kPa := (rPDT_301A_MvrDiffPress_kPa + rPDT_301B_MvrDiffPress_kPa) * 0.500;
    nDegradedMode_PDT301 := 1;
    wTmrHealth_PDT301 := 16#0003;
ELSE
    nDegradedMode_PDT301 := 3;
    wTmrHealth_PDT301 := 16#0000;
END_IF;

(* ------------------------------------------------------------------------------------------------- *)
(* SENSOR GROUP 4: SPRAY DRYER EXHAUST AIR TEMPERATURE (TT-401A/B/C) [deg C]                         *)
(* Calibrated Range: 0.0 to 150.0 [deg C]. Tolerance: 2.00 [deg C]. Debounce Limit: 400.0 [ms]       *)
(* ------------------------------------------------------------------------------------------------- *)
rDev_TT401_AB := ABS(rTT_401A_ExhaustTemp_degC - rTT_401B_ExhaustTemp_degC);
rDev_TT401_BC := ABS(rTT_401B_ExhaustTemp_degC - rTT_401C_ExhaustTemp_degC);
rDev_TT401_CA := ABS(rTT_401C_ExhaustTemp_degC - rTT_401A_ExhaustTemp_degC);

IF rDev_TT401_AB > rTol_TT401_degC THEN
    tTimer_TT401_AB := tTimer_TT401_AB + rCycleTime_s;
    IF tTimer_TT401_AB >= 0.400 THEN
        bDiscrepancy_TT401_AB := TRUE;
    END_IF;
ELSE
    tTimer_TT401_AB := 0.0;
    bDiscrepancy_TT401_AB := FALSE;
END_IF;

IF rDev_TT401_BC > rTol_TT401_degC THEN
    tTimer_TT401_BC := tTimer_TT401_BC + rCycleTime_s;
    IF tTimer_TT401_BC >= 0.400 THEN
        bDiscrepancy_TT401_BC := TRUE;
    END_IF;
ELSE
    tTimer_TT401_BC := 0.0;
    bDiscrepancy_TT401_BC := FALSE;
END_IF;

IF rDev_TT401_CA > rTol_TT401_degC THEN
    tTimer_TT401_CA := tTimer_TT401_CA + rCycleTime_s;
    IF tTimer_TT401_CA >= 0.400 THEN
        bDiscrepancy_TT401_CA := TRUE;
    END_IF;
ELSE
    tTimer_TT401_CA := 0.0;
    bDiscrepancy_TT401_CA := FALSE;
END_IF;

IF (NOT bDiscrepancy_TT401_AB) AND (NOT bDiscrepancy_TT401_BC) AND (NOT bDiscrepancy_TT401_CA) THEN
    IF (rTT_401A_ExhaustTemp_degC >= rTT_401B_ExhaustTemp_degC AND rTT_401A_ExhaustTemp_degC <= rTT_401C_ExhaustTemp_degC) OR
       (rTT_401A_ExhaustTemp_degC <= rTT_401B_ExhaustTemp_degC AND rTT_401A_ExhaustTemp_degC >= rTT_401C_ExhaustTemp_degC) THEN
        rVoted_ExhaustTemp_degC := rTT_401A_ExhaustTemp_degC;
    ELSIF (rTT_401B_ExhaustTemp_degC >= rTT_401A_ExhaustTemp_degC AND rTT_401B_ExhaustTemp_degC <= rTT_401C_ExhaustTemp_degC) OR
          (rTT_401B_ExhaustTemp_degC <= rTT_401A_ExhaustTemp_degC AND rTT_401B_ExhaustTemp_degC >= rTT_401C_ExhaustTemp_degC) THEN
        rVoted_ExhaustTemp_degC := rTT_401B_ExhaustTemp_degC;
    ELSE
        rVoted_ExhaustTemp_degC := rTT_401C_ExhaustTemp_degC;
    END_IF;
    nDegradedMode_TT401 := 0;
    wTmrHealth_TT401 := 16#0007;
ELSIF bDiscrepancy_TT401_AB AND bDiscrepancy_TT401_CA AND (NOT bDiscrepancy_TT401_BC) THEN
    rVoted_ExhaustTemp_degC := (rTT_401B_ExhaustTemp_degC + rTT_401C_ExhaustTemp_degC) * 0.500;
    nDegradedMode_TT401 := 1;
    wTmrHealth_TT401 := 16#0006;
ELSIF bDiscrepancy_TT401_AB AND bDiscrepancy_TT401_BC AND (NOT bDiscrepancy_TT401_CA) THEN
    rVoted_ExhaustTemp_degC := (rTT_401A_ExhaustTemp_degC + rTT_401C_ExhaustTemp_degC) * 0.500;
    nDegradedMode_TT401 := 1;
    wTmrHealth_TT401 := 16#0005;
ELSIF bDiscrepancy_TT401_BC AND bDiscrepancy_TT401_CA AND (NOT bDiscrepancy_TT401_AB) THEN
    rVoted_ExhaustTemp_degC := (rTT_401A_ExhaustTemp_degC + rTT_401B_ExhaustTemp_degC) * 0.500;
    nDegradedMode_TT401 := 1;
    wTmrHealth_TT401 := 16#0003;
ELSIF bDiscrepancy_TT401_AB AND (NOT bDiscrepancy_TT401_BC) AND (NOT bDiscrepancy_TT401_CA) THEN
    rVoted_ExhaustTemp_degC := (rTT_401B_ExhaustTemp_degC + rTT_401C_ExhaustTemp_degC) * 0.500;
    nDegradedMode_TT401 := 1;
    wTmrHealth_TT401 := 16#0006;
ELSIF bDiscrepancy_TT401_BC AND (NOT bDiscrepancy_TT401_AB) AND (NOT bDiscrepancy_TT401_CA) THEN
    rVoted_ExhaustTemp_degC := (rTT_401A_ExhaustTemp_degC + rTT_401C_ExhaustTemp_degC) * 0.500;
    nDegradedMode_TT401 := 1;
    wTmrHealth_TT401 := 16#0005;
ELSIF bDiscrepancy_TT401_CA AND (NOT bDiscrepancy_TT401_AB) AND (NOT bDiscrepancy_TT401_BC) THEN
    rVoted_ExhaustTemp_degC := (rTT_401A_ExhaustTemp_degC + rTT_401B_ExhaustTemp_degC) * 0.500;
    nDegradedMode_TT401 := 1;
    wTmrHealth_TT401 := 16#0003;
ELSE
    nDegradedMode_TT401 := 3;
    wTmrHealth_TT401 := 16#0000;
END_IF;

(* ------------------------------------------------------------------------------------------------- *)
(* SENSOR GROUP 5: BAGHOUSE IR OPTICAL SPARK DETECTORS (IRT-501A/B/C) [counts/s]                     *)
(* Calibrated Range: 0.0 to 5000.0 [counts/s]. Tolerance: 15.0 [counts/s]. Max Voting for Safety     *)
(* ------------------------------------------------------------------------------------------------- *)
rDev_IRT501_AB := ABS(rIRT_501A_SparkDetector_cps - rIRT_501B_SparkDetector_cps);
rDev_IRT501_BC := ABS(rIRT_501B_SparkDetector_cps - rIRT_501C_SparkDetector_cps);
rDev_IRT501_CA := ABS(rIRT_501C_SparkDetector_cps - rIRT_501A_SparkDetector_cps);

IF rDev_IRT501_AB > rTol_IRT501_cps THEN
    tTimer_IRT501_AB := tTimer_IRT501_AB + rCycleTime_s;
    IF tTimer_IRT501_AB >= 0.400 THEN
        bDiscrepancy_IRT501_AB := TRUE;
    END_IF;
ELSE
    tTimer_IRT501_AB := 0.0;
    bDiscrepancy_IRT501_AB := FALSE;
END_IF;

IF rDev_IRT501_BC > rTol_IRT501_cps THEN
    tTimer_IRT501_BC := tTimer_IRT501_BC + rCycleTime_s;
    IF tTimer_IRT501_BC >= 0.400 THEN
        bDiscrepancy_IRT501_BC := TRUE;
    END_IF;
ELSE
    tTimer_IRT501_BC := 0.0;
    bDiscrepancy_IRT501_BC := FALSE;
END_IF;

IF rDev_IRT501_CA > rTol_IRT501_cps THEN
    tTimer_IRT501_CA := tTimer_IRT501_CA + rCycleTime_s;
    IF tTimer_IRT501_CA >= 0.400 THEN
        bDiscrepancy_IRT501_CA := TRUE;
    END_IF;
ELSE
    tTimer_IRT501_CA := 0.0;
    bDiscrepancy_IRT501_CA := FALSE;
END_IF;

(* For Optical Spark Fire Detection, Safety Mandates 2-out-of-3 High-Select Logic *)
IF (rIRT_501A_SparkDetector_cps >= rIRT_501B_SparkDetector_cps AND rIRT_501A_SparkDetector_cps <= rIRT_501C_SparkDetector_cps) OR
   (rIRT_501A_SparkDetector_cps <= rIRT_501B_SparkDetector_cps AND rIRT_501A_SparkDetector_cps >= rIRT_501C_SparkDetector_cps) THEN
    rVoted_SparkDetector_cps := rIRT_501A_SparkDetector_cps;
ELSIF (rIRT_501B_SparkDetector_cps >= rIRT_501A_SparkDetector_cps AND rIRT_501B_SparkDetector_cps <= rIRT_501C_SparkDetector_cps) OR
      (rIRT_501B_SparkDetector_cps <= rIRT_501A_SparkDetector_cps AND rIRT_501B_SparkDetector_cps >= rIRT_501C_SparkDetector_cps) THEN
    rVoted_SparkDetector_cps := rIRT_501B_SparkDetector_cps;
ELSE
    rVoted_SparkDetector_cps := rIRT_501C_SparkDetector_cps;
END_IF;

(* If ANY two channels detect sparks exceeding high threshold, escalate voted value immediately *)
IF (rIRT_501A_SparkDetector_cps >= rH_SparkDetector_cps AND rIRT_501B_SparkDetector_cps >= rH_SparkDetector_cps) OR
   (rIRT_501B_SparkDetector_cps >= rH_SparkDetector_cps AND rIRT_501C_SparkDetector_cps >= rH_SparkDetector_cps) OR
   (rIRT_501C_SparkDetector_cps >= rH_SparkDetector_cps AND rIRT_501A_SparkDetector_cps >= rH_SparkDetector_cps) THEN
    rVoted_SparkDetector_cps := MAX(rIRT_501A_SparkDetector_cps, MAX(rIRT_501B_SparkDetector_cps, rIRT_501C_SparkDetector_cps));
END_IF;
nDegradedMode_IRT501 := 0;
wTmrHealth_IRT501 := 16#0007;

(* ------------------------------------------------------------------------------------------------- *)
(* SENSOR GROUP 6: DRYING CHAMBER INLET AIR TEMPERATURE (TT-601A/B/C) [deg C]                        *)
(* Calibrated Range: 0.0 to 260.0 [deg C]. Tolerance: 3.00 [deg C]. Debounce Limit: 400.0 [ms]       *)
(* ------------------------------------------------------------------------------------------------- *)
rDev_TT601_AB := ABS(rTT_601A_InletAirTemp_degC - rTT_601B_InletAirTemp_degC);
rDev_TT601_BC := ABS(rTT_601B_InletAirTemp_degC - rTT_601C_InletAirTemp_degC);
rDev_TT601_CA := ABS(rTT_601C_InletAirTemp_degC - rTT_601A_InletAirTemp_degC);

IF rDev_TT601_AB > rTol_TT601_degC THEN
    tTimer_TT601_AB := tTimer_TT601_AB + rCycleTime_s;
    IF tTimer_TT601_AB >= 0.400 THEN
        bDiscrepancy_TT601_AB := TRUE;
    END_IF;
ELSE
    tTimer_TT601_AB := 0.0;
    bDiscrepancy_TT601_AB := FALSE;
END_IF;

IF rDev_TT601_BC > rTol_TT601_degC THEN
    tTimer_TT601_BC := tTimer_TT601_BC + rCycleTime_s;
    IF tTimer_TT601_BC >= 0.400 THEN
        bDiscrepancy_TT601_BC := TRUE;
    END_IF;
ELSE
    tTimer_TT601_BC := 0.0;
    bDiscrepancy_TT601_BC := FALSE;
END_IF;

IF rDev_TT601_CA > rTol_TT601_degC THEN
    tTimer_TT601_CA := tTimer_TT601_CA + rCycleTime_s;
    IF tTimer_TT601_CA >= 0.400 THEN
        bDiscrepancy_TT601_CA := TRUE;
    END_IF;
ELSE
    tTimer_TT601_CA := 0.0;
    bDiscrepancy_TT601_CA := FALSE;
END_IF;

IF (NOT bDiscrepancy_TT601_AB) AND (NOT bDiscrepancy_TT601_BC) AND (NOT bDiscrepancy_TT601_CA) THEN
    IF (rTT_601A_InletAirTemp_degC >= rTT_601B_InletAirTemp_degC AND rTT_601A_InletAirTemp_degC <= rTT_601C_InletAirTemp_degC) OR
       (rTT_601A_InletAirTemp_degC <= rTT_601B_InletAirTemp_degC AND rTT_601A_InletAirTemp_degC >= rTT_601C_InletAirTemp_degC) THEN
        rVoted_InletAirTemp_degC := rTT_601A_InletAirTemp_degC;
    ELSIF (rTT_601B_InletAirTemp_degC >= rTT_601A_InletAirTemp_degC AND rTT_601B_InletAirTemp_degC <= rTT_601C_InletAirTemp_degC) OR
          (rTT_601B_InletAirTemp_degC <= rTT_601A_InletAirTemp_degC AND rTT_601B_InletAirTemp_degC >= rTT_601C_InletAirTemp_degC) THEN
        rVoted_InletAirTemp_degC := rTT_601B_InletAirTemp_degC;
    ELSE
        rVoted_InletAirTemp_degC := rTT_601C_InletAirTemp_degC;
    END_IF;
    nDegradedMode_TT601 := 0;
    wTmrHealth_TT601 := 16#0007;
ELSIF bDiscrepancy_TT601_AB AND bDiscrepancy_TT601_CA AND (NOT bDiscrepancy_TT601_BC) THEN
    rVoted_InletAirTemp_degC := (rTT_601B_InletAirTemp_degC + rTT_601C_InletAirTemp_degC) * 0.500;
    nDegradedMode_TT601 := 1;
    wTmrHealth_TT601 := 16#0006;
ELSIF bDiscrepancy_TT601_AB AND bDiscrepancy_TT601_BC AND (NOT bDiscrepancy_TT601_CA) THEN
    rVoted_InletAirTemp_degC := (rTT_601A_InletAirTemp_degC + rTT_601C_InletAirTemp_degC) * 0.500;
    nDegradedMode_TT601 := 1;
    wTmrHealth_TT601 := 16#0005;
ELSIF bDiscrepancy_TT601_BC AND bDiscrepancy_TT601_CA AND (NOT bDiscrepancy_TT601_AB) THEN
    rVoted_InletAirTemp_degC := (rTT_601A_InletAirTemp_degC + rTT_601B_InletAirTemp_degC) * 0.500;
    nDegradedMode_TT601 := 1;
    wTmrHealth_TT601 := 16#0003;
ELSIF bDiscrepancy_TT601_AB AND (NOT bDiscrepancy_TT601_BC) AND (NOT bDiscrepancy_TT601_CA) THEN
    rVoted_InletAirTemp_degC := (rTT_601B_InletAirTemp_degC + rTT_601C_InletAirTemp_degC) * 0.500;
    nDegradedMode_TT601 := 1;
    wTmrHealth_TT601 := 16#0006;
ELSIF bDiscrepancy_TT601_BC AND (NOT bDiscrepancy_TT601_AB) AND (NOT bDiscrepancy_TT601_CA) THEN
    rVoted_InletAirTemp_degC := (rTT_601A_InletAirTemp_degC + rTT_601C_InletAirTemp_degC) * 0.500;
    nDegradedMode_TT601 := 1;
    wTmrHealth_TT601 := 16#0005;
ELSIF bDiscrepancy_TT601_CA AND (NOT bDiscrepancy_TT601_AB) AND (NOT bDiscrepancy_TT601_BC) THEN
    rVoted_InletAirTemp_degC := (rTT_601A_InletAirTemp_degC + rTT_601B_InletAirTemp_degC) * 0.500;
    nDegradedMode_TT601 := 1;
    wTmrHealth_TT601 := 16#0003;
ELSE
    nDegradedMode_TT601 := 3;
    wTmrHealth_TT601 := 16#0000;
END_IF;

(* ------------------------------------------------------------------------------------------------- *)
(* SENSOR GROUP 7: FINAL MILK POWDER MOISTURE CONTENT (MT-701A/B/C) [% w/w]                          *)
(* Calibrated Range: 0.0 to 10.0 [% w/w]. Tolerance: 0.15 [% w/w]. Debounce Limit: 400.0 [ms]        *)
(* ------------------------------------------------------------------------------------------------- *)
rDev_MT701_AB := ABS(rMT_701A_PowderMoisture_pct - rMT_701B_PowderMoisture_pct);
rDev_MT701_BC := ABS(rMT_701B_PowderMoisture_pct - rMT_701C_PowderMoisture_pct);
rDev_MT701_CA := ABS(rMT_701C_PowderMoisture_pct - rMT_701A_PowderMoisture_pct);

IF rDev_MT701_AB > rTol_MT701_pct THEN
    tTimer_MT701_AB := tTimer_MT701_AB + rCycleTime_s;
    IF tTimer_MT701_AB >= 0.400 THEN
        bDiscrepancy_MT701_AB := TRUE;
    END_IF;
ELSE
    tTimer_MT701_AB := 0.0;
    bDiscrepancy_MT701_AB := FALSE;
END_IF;

IF rDev_MT701_BC > rTol_MT701_pct THEN
    tTimer_MT701_BC := tTimer_MT701_BC + rCycleTime_s;
    IF tTimer_MT701_BC >= 0.400 THEN
        bDiscrepancy_MT701_BC := TRUE;
    END_IF;
ELSE
    tTimer_MT701_BC := 0.0;
    bDiscrepancy_MT701_BC := FALSE;
END_IF;

IF rDev_MT701_CA > rTol_MT701_pct THEN
    tTimer_MT701_CA := tTimer_MT701_CA + rCycleTime_s;
    IF tTimer_MT701_CA >= 0.400 THEN
        bDiscrepancy_MT701_CA := TRUE;
    END_IF;
ELSE
    tTimer_MT701_CA := 0.0;
    bDiscrepancy_MT701_CA := FALSE;
END_IF;

IF (NOT bDiscrepancy_MT701_AB) AND (NOT bDiscrepancy_MT701_BC) AND (NOT bDiscrepancy_MT701_CA) THEN
    IF (rMT_701A_PowderMoisture_pct >= rMT_701B_PowderMoisture_pct AND rMT_701A_PowderMoisture_pct <= rMT_701C_PowderMoisture_pct) OR
       (rMT_701A_PowderMoisture_pct <= rMT_701B_PowderMoisture_pct AND rMT_701A_PowderMoisture_pct >= rMT_701C_PowderMoisture_pct) THEN
        rVoted_PowderMoisture_pct := rMT_701A_PowderMoisture_pct;
    ELSIF (rMT_701B_PowderMoisture_pct >= rMT_701A_PowderMoisture_pct AND rMT_701B_PowderMoisture_pct <= rMT_701C_PowderMoisture_pct) OR
          (rMT_701B_PowderMoisture_pct <= rMT_701A_PowderMoisture_pct AND rMT_701B_PowderMoisture_pct >= rMT_701C_PowderMoisture_pct) THEN
        rVoted_PowderMoisture_pct := rMT_701B_PowderMoisture_pct;
    ELSE
        rVoted_PowderMoisture_pct := rMT_701C_PowderMoisture_pct;
    END_IF;
    nDegradedMode_MT701 := 0;
    wTmrHealth_MT701 := 16#0007;
ELSIF bDiscrepancy_MT701_AB AND bDiscrepancy_MT701_CA AND (NOT bDiscrepancy_MT701_BC) THEN
    rVoted_PowderMoisture_pct := (rMT_701B_PowderMoisture_pct + rMT_701C_PowderMoisture_pct) * 0.500;
    nDegradedMode_MT701 := 1;
    wTmrHealth_MT701 := 16#0006;
ELSIF bDiscrepancy_MT701_AB AND bDiscrepancy_MT701_BC AND (NOT bDiscrepancy_MT701_CA) THEN
    rVoted_PowderMoisture_pct := (rMT_701A_PowderMoisture_pct + rMT_701C_PowderMoisture_pct) * 0.500;
    nDegradedMode_MT701 := 1;
    wTmrHealth_MT701 := 16#0005;
ELSIF bDiscrepancy_MT701_BC AND bDiscrepancy_MT701_CA AND (NOT bDiscrepancy_MT701_AB) THEN
    rVoted_PowderMoisture_pct := (rMT_701A_PowderMoisture_pct + rMT_701B_PowderMoisture_pct) * 0.500;
    nDegradedMode_MT701 := 1;
    wTmrHealth_MT701 := 16#0003;
ELSIF bDiscrepancy_MT701_AB AND (NOT bDiscrepancy_MT701_BC) AND (NOT bDiscrepancy_MT701_CA) THEN
    rVoted_PowderMoisture_pct := (rMT_701B_PowderMoisture_pct + rMT_701C_PowderMoisture_pct) * 0.500;
    nDegradedMode_MT701 := 1;
    wTmrHealth_MT701 := 16#0006;
ELSIF bDiscrepancy_MT701_BC AND (NOT bDiscrepancy_MT701_AB) AND (NOT bDiscrepancy_MT701_CA) THEN
    rVoted_PowderMoisture_pct := (rMT_701A_PowderMoisture_pct + rMT_701C_PowderMoisture_pct) * 0.500;
    nDegradedMode_MT701 := 1;
    wTmrHealth_MT701 := 16#0005;
ELSIF bDiscrepancy_MT701_CA AND (NOT bDiscrepancy_MT701_AB) AND (NOT bDiscrepancy_MT701_BC) THEN
    rVoted_PowderMoisture_pct := (rMT_701A_PowderMoisture_pct + rMT_701B_PowderMoisture_pct) * 0.500;
    nDegradedMode_MT701 := 1;
    wTmrHealth_MT701 := 16#0003;
ELSE
    nDegradedMode_MT701 := 3;
    wTmrHealth_MT701 := 16#0000;
END_IF;

(* ------------------------------------------------------------------------------------------------- *)
(* SENSOR GROUP 8: FALLING FILM RECIRCULATION VELOCITY (FT-801A/B/C) [m/s]                           *)
(* Calibrated Range: 0.0 to 5.0 [m/s]. Tolerance: 0.12 [m/s]. Debounce Limit: 400.0 [ms]             *)
(* ------------------------------------------------------------------------------------------------- *)
rDev_FT801_AB := ABS(rFT_801A_RecircVelocity_ms - rFT_801B_RecircVelocity_ms);
rDev_FT801_BC := ABS(rFT_801B_RecircVelocity_ms - rFT_801C_RecircVelocity_ms);
rDev_FT801_CA := ABS(rFT_801C_RecircVelocity_ms - rFT_801A_RecircVelocity_ms);

IF rDev_FT801_AB > rTol_FT801_ms THEN
    tTimer_FT801_AB := tTimer_FT801_AB + rCycleTime_s;
    IF tTimer_FT801_AB >= 0.400 THEN
        bDiscrepancy_FT801_AB := TRUE;
    END_IF;
ELSE
    tTimer_FT801_AB := 0.0;
    bDiscrepancy_FT801_AB := FALSE;
END_IF;

IF rDev_FT801_BC > rTol_FT801_ms THEN
    tTimer_FT801_BC := tTimer_FT801_BC + rCycleTime_s;
    IF tTimer_FT801_BC >= 0.400 THEN
        bDiscrepancy_FT801_BC := TRUE;
    END_IF;
ELSE
    tTimer_FT801_BC := 0.0;
    bDiscrepancy_FT801_BC := FALSE;
END_IF;

IF rDev_FT801_CA > rTol_FT801_ms THEN
    tTimer_FT801_CA := tTimer_FT801_CA + rCycleTime_s;
    IF tTimer_FT801_CA >= 0.400 THEN
        bDiscrepancy_FT801_CA := TRUE;
    END_IF;
ELSE
    tTimer_FT801_CA := 0.0;
    bDiscrepancy_FT801_CA := FALSE;
END_IF;

IF (NOT bDiscrepancy_FT801_AB) AND (NOT bDiscrepancy_FT801_BC) AND (NOT bDiscrepancy_FT801_CA) THEN
    IF (rFT_801A_RecircVelocity_ms >= rFT_801B_RecircVelocity_ms AND rFT_801A_RecircVelocity_ms <= rFT_801C_RecircVelocity_ms) OR
       (rFT_801A_RecircVelocity_ms <= rFT_801B_RecircVelocity_ms AND rFT_801A_RecircVelocity_ms >= rFT_801C_RecircVelocity_ms) THEN
        rVoted_RecircVelocity_ms := rFT_801A_RecircVelocity_ms;
    ELSIF (rFT_801B_RecircVelocity_ms >= rFT_801A_RecircVelocity_ms AND rFT_801B_RecircVelocity_ms <= rFT_801C_RecircVelocity_ms) OR
          (rFT_801B_RecircVelocity_ms <= rFT_801A_RecircVelocity_ms AND rFT_801B_RecircVelocity_ms >= rFT_801C_RecircVelocity_ms) THEN
        rVoted_RecircVelocity_ms := rFT_801B_RecircVelocity_ms;
    ELSE
        rVoted_RecircVelocity_ms := rFT_801C_RecircVelocity_ms;
    END_IF;
    nDegradedMode_FT801 := 0;
    wTmrHealth_FT801 := 16#0007;
ELSIF bDiscrepancy_FT801_AB AND bDiscrepancy_FT801_CA AND (NOT bDiscrepancy_FT801_BC) THEN
    rVoted_RecircVelocity_ms := (rFT_801B_RecircVelocity_ms + rFT_801C_RecircVelocity_ms) * 0.500;
    nDegradedMode_FT801 := 1;
    wTmrHealth_FT801 := 16#0006;
ELSIF bDiscrepancy_FT801_AB AND bDiscrepancy_FT801_BC AND (NOT bDiscrepancy_FT801_CA) THEN
    rVoted_RecircVelocity_ms := (rFT_801A_RecircVelocity_ms + rFT_801C_RecircVelocity_ms) * 0.500;
    nDegradedMode_FT801 := 1;
    wTmrHealth_FT801 := 16#0005;
ELSIF bDiscrepancy_FT801_BC AND bDiscrepancy_FT801_CA AND (NOT bDiscrepancy_FT801_AB) THEN
    rVoted_RecircVelocity_ms := (rFT_801A_RecircVelocity_ms + rFT_801B_RecircVelocity_ms) * 0.500;
    nDegradedMode_FT801 := 1;
    wTmrHealth_FT801 := 16#0003;
ELSIF bDiscrepancy_FT801_AB AND (NOT bDiscrepancy_FT801_BC) AND (NOT bDiscrepancy_FT801_CA) THEN
    rVoted_RecircVelocity_ms := (rFT_801B_RecircVelocity_ms + rFT_801C_RecircVelocity_ms) * 0.500;
    nDegradedMode_FT801 := 1;
    wTmrHealth_FT801 := 16#0006;
ELSIF bDiscrepancy_FT801_BC AND (NOT bDiscrepancy_FT801_AB) AND (NOT bDiscrepancy_FT801_CA) THEN
    rVoted_RecircVelocity_ms := (rFT_801A_RecircVelocity_ms + rFT_801C_RecircVelocity_ms) * 0.500;
    nDegradedMode_FT801 := 1;
    wTmrHealth_FT801 := 16#0005;
ELSIF bDiscrepancy_FT801_CA AND (NOT bDiscrepancy_FT801_AB) AND (NOT bDiscrepancy_FT801_BC) THEN
    rVoted_RecircVelocity_ms := (rFT_801A_RecircVelocity_ms + rFT_801B_RecircVelocity_ms) * 0.500;
    nDegradedMode_FT801 := 1;
    wTmrHealth_FT801 := 16#0003;
ELSE
    nDegradedMode_FT801 := 3;
    wTmrHealth_FT801 := 16#0000;
END_IF;
"""
