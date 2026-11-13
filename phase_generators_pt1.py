# phase_generators_pt1.py
# Phase 1: 2oo3 TMR Voting
# Phase 2: First-Principles Rheology & Observers

def generate_phase1():
    return """
(* ==================================================================================================== *)
(* PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING SUITE WITH DISCREPANCY DEBOUNCE        *)
(* Hardware-Level Triple-Redundant Fault Tolerant Architecture:                                         *)
(*   Group 1: Nozzle Melt Pressure Transducers PT-101A/B/C [bar]                                        *)
(*   Group 2: Cavity 1 Direct Piezoelectric Quartz Sensors PT-201A/B/C [bar]                           *)
(*   Group 3: Injection Screw Absolute Optical Linear Scales ST-301A/B/C [mm]                           *)
(*   Group 4: Clamping Tie-Bar Piezoelectric Strain Gauges WT-401A/B/C [kN]                             *)
(*   Group 5: Mold Tooling Core Thermocouples TT-501A/B/C [deg C]                                      *)
(* Fault Logic:                                                                                         *)
(*   - Pairwise discrepancy timers evaluate ABS deviations against tolerance thresholds.                *)
(*   - If deviation persists > 100 ms (rTmrDebounceTimeLimit_sec), faulty channel is invalidated.       *)
(*   - Bumpless degradation: 3 healthy -> Median; 2 healthy -> Mean; 1 healthy -> Single; 0 -> Hold.  *)
(*   - Dynamic rate-of-change slew limiter prevents discontinuous step transitions on sensor fault.      *)
(* ==================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------- *)
(* GROUP 1: NOZZLE MELT PRESSURE TRANSDUCERS (PT-101A/B/C) [bar]                                        *)
(* ---------------------------------------------------------------------------------------------------- *)
IF ABS(rPT_Nozzle_101A - rPT_Nozzle_101B) > rDiscrepancyThreshold_PT_Nozzle_bar THEN
    rTimer_PT101_AB_sec := rTimer_PT101_AB_sec + rCycleTime_sec;
ELSE
    rTimer_PT101_AB_sec := MAX(0.0, rTimer_PT101_AB_sec - (rCycleTime_sec * 0.5));
END_IF;

IF ABS(rPT_Nozzle_101B - rPT_Nozzle_101C) > rDiscrepancyThreshold_PT_Nozzle_bar THEN
    rTimer_PT101_BC_sec := rTimer_PT101_BC_sec + rCycleTime_sec;
ELSE
    rTimer_PT101_BC_sec := MAX(0.0, rTimer_PT101_BC_sec - (rCycleTime_sec * 0.5));
END_IF;

IF ABS(rPT_Nozzle_101C - rPT_Nozzle_101A) > rDiscrepancyThreshold_PT_Nozzle_bar THEN
    rTimer_PT101_CA_sec := rTimer_PT101_CA_sec + rCycleTime_sec;
ELSE
    rTimer_PT101_CA_sec := MAX(0.0, rTimer_PT101_CA_sec - (rCycleTime_sec * 0.5));
END_IF;

bHealthy_PT101A := (rTimer_PT101_AB_sec <= rTmrDebounceTimeLimit_sec) OR (rTimer_PT101_CA_sec <= rTmrDebounceTimeLimit_sec);
bHealthy_PT101B := (rTimer_PT101_AB_sec <= rTmrDebounceTimeLimit_sec) OR (rTimer_PT101_BC_sec <= rTmrDebounceTimeLimit_sec);
bHealthy_PT101C := (rTimer_PT101_BC_sec <= rTmrDebounceTimeLimit_sec) OR (rTimer_PT101_CA_sec <= rTmrDebounceTimeLimit_sec);
bDiscrepancy_PT101 := (rTimer_PT101_AB_sec > 0.050) OR (rTimer_PT101_BC_sec > 0.050) OR (rTimer_PT101_CA_sec > 0.050);

IF bHealthy_PT101A AND bHealthy_PT101B AND bHealthy_PT101C THEN
    (* Full Triple Modular Redundancy 2oo3 Median Selection *)
    IF (rPT_Nozzle_101A >= rPT_Nozzle_101B AND rPT_Nozzle_101A <= rPT_Nozzle_101C) OR
       (rPT_Nozzle_101A <= rPT_Nozzle_101B AND rPT_Nozzle_101A >= rPT_Nozzle_101C) THEN
        rVoted_PT101_bar := rPT_Nozzle_101A;
    ELSIF (rPT_Nozzle_101B >= rPT_Nozzle_101A AND rPT_Nozzle_101B <= rPT_Nozzle_101C) OR
          (rPT_Nozzle_101B <= rPT_Nozzle_101A AND rPT_Nozzle_101B >= rPT_Nozzle_101C) THEN
        rVoted_PT101_bar := rPT_Nozzle_101B;
    ELSE
        rVoted_PT101_bar := rPT_Nozzle_101C;
    END_IF;
    bDegraded_PT101 := FALSE;
ELSIF bHealthy_PT101A AND bHealthy_PT101B THEN
    rVoted_PT101_bar := 0.5 * (rPT_Nozzle_101A + rPT_Nozzle_101B);
    bDegraded_PT101 := TRUE;
ELSIF bHealthy_PT101B AND bHealthy_PT101C THEN
    rVoted_PT101_bar := 0.5 * (rPT_Nozzle_101B + rPT_Nozzle_101C);
    bDegraded_PT101 := TRUE;
ELSIF bHealthy_PT101A AND bHealthy_PT101C THEN
    rVoted_PT101_bar := 0.5 * (rPT_Nozzle_101A + rPT_Nozzle_101C);
    bDegraded_PT101 := TRUE;
ELSIF bHealthy_PT101A THEN
    rVoted_PT101_bar := rPT_Nozzle_101A;
    bDegraded_PT101 := TRUE;
ELSIF bHealthy_PT101B THEN
    rVoted_PT101_bar := rPT_Nozzle_101B;
    bDegraded_PT101 := TRUE;
ELSIF bHealthy_PT101C THEN
    rVoted_PT101_bar := rPT_Nozzle_101C;
    bDegraded_PT101 := TRUE;
ELSE
    rVoted_PT101_bar := rVoted_PT101_Prev;
    bDegraded_PT101 := TRUE;
END_IF;
(* Bumpless Slew Rate Limiter on Voted Signal *)
rVoted_PT101_bar := rVoted_PT101_Prev + LIMIT(-75.0, rVoted_PT101_bar - rVoted_PT101_Prev, 75.0);
rVoted_PT101_Prev := rVoted_PT101_bar;

(* ---------------------------------------------------------------------------------------------------- *)
(* GROUP 2: CAVITY 1 DIRECT PIEZOELECTRIC QUARTZ SENSORS (PT-201A/B/C) [bar]                            *)
(* ---------------------------------------------------------------------------------------------------- *)
IF ABS(rPT_Cavity_201A - rPT_Cavity_201B) > rDiscrepancyThreshold_PT_Cavity_bar THEN
    rTimer_PT201_AB_sec := rTimer_PT201_AB_sec + rCycleTime_sec;
ELSE
    rTimer_PT201_AB_sec := MAX(0.0, rTimer_PT201_AB_sec - (rCycleTime_sec * 0.5));
END_IF;

IF ABS(rPT_Cavity_201B - rPT_Cavity_201C) > rDiscrepancyThreshold_PT_Cavity_bar THEN
    rTimer_PT201_BC_sec := rTimer_PT201_BC_sec + rCycleTime_sec;
ELSE
    rTimer_PT201_BC_sec := MAX(0.0, rTimer_PT201_BC_sec - (rCycleTime_sec * 0.5));
END_IF;

IF ABS(rPT_Cavity_201C - rPT_Cavity_201A) > rDiscrepancyThreshold_PT_Cavity_bar THEN
    rTimer_PT201_CA_sec := rTimer_PT201_CA_sec + rCycleTime_sec;
ELSE
    rTimer_PT201_CA_sec := MAX(0.0, rTimer_PT201_CA_sec - (rCycleTime_sec * 0.5));
END_IF;

bHealthy_PT201A := (rTimer_PT201_AB_sec <= rTmrDebounceTimeLimit_sec) OR (rTimer_PT201_CA_sec <= rTmrDebounceTimeLimit_sec);
bHealthy_PT201B := (rTimer_PT201_AB_sec <= rTmrDebounceTimeLimit_sec) OR (rTimer_PT201_BC_sec <= rTmrDebounceTimeLimit_sec);
bHealthy_PT201C := (rTimer_PT201_BC_sec <= rTmrDebounceTimeLimit_sec) OR (rTimer_PT201_CA_sec <= rTmrDebounceTimeLimit_sec);
bDiscrepancy_PT201 := (rTimer_PT201_AB_sec > 0.050) OR (rTimer_PT201_BC_sec > 0.050) OR (rTimer_PT201_CA_sec > 0.050);

IF bHealthy_PT201A AND bHealthy_PT201B AND bHealthy_PT201C THEN
    IF (rPT_Cavity_201A >= rPT_Cavity_201B AND rPT_Cavity_201A <= rPT_Cavity_201C) OR
       (rPT_Cavity_201A <= rPT_Cavity_201B AND rPT_Cavity_201A >= rPT_Cavity_201C) THEN
        rVoted_PT201_bar := rPT_Cavity_201A;
    ELSIF (rPT_Cavity_201B >= rPT_Cavity_201A AND rPT_Cavity_201B <= rPT_Cavity_201C) OR
          (rPT_Cavity_201B <= rPT_Cavity_201A AND rPT_Cavity_201B >= rPT_Cavity_201C) THEN
        rVoted_PT201_bar := rPT_Cavity_201B;
    ELSE
        rVoted_PT201_bar := rPT_Cavity_201C;
    END_IF;
    bDegraded_PT201 := FALSE;
ELSIF bHealthy_PT201A AND bHealthy_PT201B THEN
    rVoted_PT201_bar := 0.5 * (rPT_Cavity_201A + rPT_Cavity_201B);
    bDegraded_PT201 := TRUE;
ELSIF bHealthy_PT201B AND bHealthy_PT201C THEN
    rVoted_PT201_bar := 0.5 * (rPT_Cavity_201B + rPT_Cavity_201C);
    bDegraded_PT201 := TRUE;
ELSIF bHealthy_PT201A AND bHealthy_PT201C THEN
    rVoted_PT201_bar := 0.5 * (rPT_Cavity_201A + rPT_Cavity_201C);
    bDegraded_PT201 := TRUE;
ELSIF bHealthy_PT201A THEN
    rVoted_PT201_bar := rPT_Cavity_201A;
    bDegraded_PT201 := TRUE;
ELSIF bHealthy_PT201B THEN
    rVoted_PT201_bar := rPT_Cavity_201B;
    bDegraded_PT201 := TRUE;
ELSIF bHealthy_PT201C THEN
    rVoted_PT201_bar := rPT_Cavity_201C;
    bDegraded_PT201 := TRUE;
ELSE
    rVoted_PT201_bar := rVoted_PT201_Prev;
    bDegraded_PT201 := TRUE;
END_IF;
rVoted_PT201_bar := rVoted_PT201_Prev + LIMIT(-60.0, rVoted_PT201_bar - rVoted_PT201_Prev, 60.0);
rVoted_PT201_Prev := rVoted_PT201_bar;

(* ---------------------------------------------------------------------------------------------------- *)
(* GROUP 3: SCREW ABSOLUTE OPTICAL LINEAR SCALES (ST-301A/B/C) [mm]                                     *)
(* ---------------------------------------------------------------------------------------------------- *)
IF ABS(rST_ScrewPos_301A - rST_ScrewPos_301B) > rDiscrepancyThreshold_ST_Screw_mm THEN
    rTimer_ST301_AB_sec := rTimer_ST301_AB_sec + rCycleTime_sec;
ELSE
    rTimer_ST301_AB_sec := MAX(0.0, rTimer_ST301_AB_sec - (rCycleTime_sec * 0.5));
END_IF;

IF ABS(rST_ScrewPos_301B - rST_ScrewPos_301C) > rDiscrepancyThreshold_ST_Screw_mm THEN
    rTimer_ST301_BC_sec := rTimer_ST301_BC_sec + rCycleTime_sec;
ELSE
    rTimer_ST301_BC_sec := MAX(0.0, rTimer_ST301_BC_sec - (rCycleTime_sec * 0.5));
END_IF;

IF ABS(rST_ScrewPos_301C - rST_ScrewPos_301A) > rDiscrepancyThreshold_ST_Screw_mm THEN
    rTimer_ST301_CA_sec := rTimer_ST301_CA_sec + rCycleTime_sec;
ELSE
    rTimer_ST301_CA_sec := MAX(0.0, rTimer_ST301_CA_sec - (rCycleTime_sec * 0.5));
END_IF;

bHealthy_ST301A := (rTimer_ST301_AB_sec <= rTmrDebounceTimeLimit_sec) OR (rTimer_ST301_CA_sec <= rTmrDebounceTimeLimit_sec);
bHealthy_ST301B := (rTimer_ST301_AB_sec <= rTmrDebounceTimeLimit_sec) OR (rTimer_ST301_BC_sec <= rTmrDebounceTimeLimit_sec);
bHealthy_ST301C := (rTimer_ST301_BC_sec <= rTmrDebounceTimeLimit_sec) OR (rTimer_ST301_CA_sec <= rTmrDebounceTimeLimit_sec);
bDiscrepancy_ST301 := (rTimer_ST301_AB_sec > 0.050) OR (rTimer_ST301_BC_sec > 0.050) OR (rTimer_ST301_CA_sec > 0.050);

IF bHealthy_ST301A AND bHealthy_ST301B AND bHealthy_ST301C THEN
    IF (rST_ScrewPos_301A >= rST_ScrewPos_301B AND rST_ScrewPos_301A <= rST_ScrewPos_301C) OR
       (rST_ScrewPos_301A <= rST_ScrewPos_301B AND rST_ScrewPos_301A >= rST_ScrewPos_301C) THEN
        rVoted_ST301_mm := rST_ScrewPos_301A;
    ELSIF (rST_ScrewPos_301B >= rST_ScrewPos_301A AND rST_ScrewPos_301B <= rST_ScrewPos_301C) OR
          (rST_ScrewPos_301B <= rST_ScrewPos_301A AND rST_ScrewPos_301B >= rST_ScrewPos_301C) THEN
        rVoted_ST301_mm := rST_ScrewPos_301B;
    ELSE
        rVoted_ST301_mm := rST_ScrewPos_301C;
    END_IF;
    bDegraded_ST301 := FALSE;
ELSIF bHealthy_ST301A AND bHealthy_ST301B THEN
    rVoted_ST301_mm := 0.5 * (rST_ScrewPos_301A + rST_ScrewPos_301B);
    bDegraded_ST301 := TRUE;
ELSIF bHealthy_ST301B AND bHealthy_ST301C THEN
    rVoted_ST301_mm := 0.5 * (rST_ScrewPos_301B + rST_ScrewPos_301C);
    bDegraded_ST301 := TRUE;
ELSIF bHealthy_ST301A AND bHealthy_ST301C THEN
    rVoted_ST301_mm := 0.5 * (rST_ScrewPos_301A + rST_ScrewPos_301C);
    bDegraded_ST301 := TRUE;
ELSIF bHealthy_ST301A THEN
    rVoted_ST301_mm := rST_ScrewPos_301A;
    bDegraded_ST301 := TRUE;
ELSIF bHealthy_ST301B THEN
    rVoted_ST301_mm := rST_ScrewPos_301B;
    bDegraded_ST301 := TRUE;
ELSIF bHealthy_ST301C THEN
    rVoted_ST301_mm := rST_ScrewPos_301C;
    bDegraded_ST301 := TRUE;
ELSE
    rVoted_ST301_mm := rVoted_ST301_Prev;
    bDegraded_ST301 := TRUE;
END_IF;
rVoted_ST301_mm := rVoted_ST301_Prev + LIMIT(-10.0, rVoted_ST301_mm - rVoted_ST301_Prev, 10.0);
rVoted_ST301_Prev := rVoted_ST301_mm;

(* ---------------------------------------------------------------------------------------------------- *)
(* GROUP 4: TIE-BAR PIEZOELECTRIC STRAIN GAUGES (WT-401A/B/C) [kN]                                      *)
(* ---------------------------------------------------------------------------------------------------- *)
IF ABS(rWT_Tonnage_401A - rWT_Tonnage_401B) > rDiscrepancyThreshold_WT_Tonnage_kN THEN
    rTimer_WT401_AB_sec := rTimer_WT401_AB_sec + rCycleTime_sec;
ELSE
    rTimer_WT401_AB_sec := MAX(0.0, rTimer_WT401_AB_sec - (rCycleTime_sec * 0.5));
END_IF;

IF ABS(rWT_Tonnage_401B - rWT_Tonnage_401C) > rDiscrepancyThreshold_WT_Tonnage_kN THEN
    rTimer_WT401_BC_sec := rTimer_WT401_BC_sec + rCycleTime_sec;
ELSE
    rTimer_WT401_BC_sec := MAX(0.0, rTimer_WT401_BC_sec - (rCycleTime_sec * 0.5));
END_IF;

IF ABS(rWT_Tonnage_401C - rWT_Tonnage_401A) > rDiscrepancyThreshold_WT_Tonnage_kN THEN
    rTimer_WT401_CA_sec := rTimer_WT401_CA_sec + rCycleTime_sec;
ELSE
    rTimer_WT401_CA_sec := MAX(0.0, rTimer_WT401_CA_sec - (rCycleTime_sec * 0.5));
END_IF;

bHealthy_WT401A := (rTimer_WT401_AB_sec <= rTmrDebounceTimeLimit_sec) OR (rTimer_WT401_CA_sec <= rTmrDebounceTimeLimit_sec);
bHealthy_WT401B := (rTimer_WT401_AB_sec <= rTmrDebounceTimeLimit_sec) OR (rTimer_WT401_BC_sec <= rTmrDebounceTimeLimit_sec);
bHealthy_WT401C := (rTimer_WT401_BC_sec <= rTmrDebounceTimeLimit_sec) OR (rTimer_WT401_CA_sec <= rTmrDebounceTimeLimit_sec);
bDiscrepancy_WT401 := (rTimer_WT401_AB_sec > 0.050) OR (rTimer_WT401_BC_sec > 0.050) OR (rTimer_WT401_CA_sec > 0.050);

IF bHealthy_WT401A AND bHealthy_WT401B AND bHealthy_WT401C THEN
    IF (rWT_Tonnage_401A >= rWT_Tonnage_401B AND rWT_Tonnage_401A <= rWT_Tonnage_401C) OR
       (rWT_Tonnage_401A <= rWT_Tonnage_401B AND rWT_Tonnage_401A >= rWT_Tonnage_401C) THEN
        rVoted_WT401_kN := rWT_Tonnage_401A;
    ELSIF (rWT_Tonnage_401B >= rWT_Tonnage_401A AND rWT_Tonnage_401B <= rWT_Tonnage_401C) OR
          (rWT_Tonnage_401B <= rWT_Tonnage_401A AND rWT_Tonnage_401B >= rWT_Tonnage_401C) THEN
        rVoted_WT401_kN := rWT_Tonnage_401B;
    ELSE
        rVoted_WT401_kN := rWT_Tonnage_401C;
    END_IF;
    bDegraded_WT401 := FALSE;
ELSIF bHealthy_WT401A AND bHealthy_WT401B THEN
    rVoted_WT401_kN := 0.5 * (rWT_Tonnage_401A + rWT_Tonnage_401B);
    bDegraded_WT401 := TRUE;
ELSIF bHealthy_WT401B AND bHealthy_WT401C THEN
    rVoted_WT401_kN := 0.5 * (rWT_Tonnage_401B + rWT_Tonnage_401C);
    bDegraded_WT401 := TRUE;
ELSIF bHealthy_WT401A AND bHealthy_WT401C THEN
    rVoted_WT401_kN := 0.5 * (rWT_Tonnage_401A + rWT_Tonnage_401C);
    bDegraded_WT401 := TRUE;
ELSIF bHealthy_WT401A THEN
    rVoted_WT401_kN := rWT_Tonnage_401A;
    bDegraded_WT401 := TRUE;
ELSIF bHealthy_WT401B THEN
    rVoted_WT401_kN := rWT_Tonnage_401B;
    bDegraded_WT401 := TRUE;
ELSIF bHealthy_WT401C THEN
    rVoted_WT401_kN := rWT_Tonnage_401C;
    bDegraded_WT401 := TRUE;
ELSE
    rVoted_WT401_kN := rVoted_WT401_Prev;
    bDegraded_WT401 := TRUE;
END_IF;
rVoted_WT401_kN := rVoted_WT401_Prev + LIMIT(-500.0, rVoted_WT401_kN - rVoted_WT401_Prev, 500.0);
rVoted_WT401_Prev := rVoted_WT401_kN;

(* Dynamic Tie-Bar Load Distribution & Diagonal Asymmetry Engine *)
rTieBar1_kN := rWT_Tonnage_401A;
rTieBar2_kN := rWT_Tonnage_401B;
rTieBar3_kN := rWT_Tonnage_401C;
rTieBar4_kN := rWT_Tonnage_404_TB4;

(* Calculate Diagonal and Adjacent Corner Imbalances *)
rMaxTieBarDelta_kN := MAX(ABS(rTieBar1_kN - rTieBar2_kN), ABS(rTieBar2_kN - rTieBar3_kN));
rMaxTieBarDelta_kN := MAX(rMaxTieBarDelta_kN, ABS(rTieBar3_kN - rTieBar4_kN));
rMaxTieBarDelta_kN := MAX(rMaxTieBarDelta_kN, ABS(rTieBar4_kN - rTieBar1_kN));
rMaxTieBarDelta_kN := MAX(rMaxTieBarDelta_kN, ABS(rTieBar1_kN - rTieBar3_kN));
rMaxTieBarDelta_kN := MAX(rMaxTieBarDelta_kN, ABS(rTieBar2_kN - rTieBar4_kN));

(* ---------------------------------------------------------------------------------------------------- *)
(* GROUP 5: MOLD TOOLING CORE THERMOCOUPLES (TT-501A/B/C) [deg C]                                      *)
(* ---------------------------------------------------------------------------------------------------- *)
IF ABS(rTT_MoldTemp_501A - rTT_MoldTemp_501B) > rDiscrepancyThreshold_TT_Mold_degC THEN
    rTimer_TT501_AB_sec := rTimer_TT501_AB_sec + rCycleTime_sec;
ELSE
    rTimer_TT501_AB_sec := MAX(0.0, rTimer_TT501_AB_sec - (rCycleTime_sec * 0.5));
END_IF;

IF ABS(rTT_MoldTemp_501B - rTT_MoldTemp_501C) > rDiscrepancyThreshold_TT_Mold_degC THEN
    rTimer_TT501_BC_sec := rTimer_TT501_BC_sec + rCycleTime_sec;
ELSE
    rTimer_TT501_BC_sec := MAX(0.0, rTimer_TT501_BC_sec - (rCycleTime_sec * 0.5));
END_IF;

IF ABS(rTT_MoldTemp_501C - rTT_MoldTemp_501A) > rDiscrepancyThreshold_TT_Mold_degC THEN
    rTimer_TT501_CA_sec := rTimer_TT501_CA_sec + rCycleTime_sec;
ELSE
    rTimer_TT501_CA_sec := MAX(0.0, rTimer_TT501_CA_sec - (rCycleTime_sec * 0.5));
END_IF;

bHealthy_TT501A := (rTimer_TT501_AB_sec <= rTmrDebounceTimeLimit_sec) OR (rTimer_TT501_CA_sec <= rTmrDebounceTimeLimit_sec);
bHealthy_TT501B := (rTimer_TT501_AB_sec <= rTmrDebounceTimeLimit_sec) OR (rTimer_TT501_BC_sec <= rTmrDebounceTimeLimit_sec);
bHealthy_TT501C := (rTimer_TT501_BC_sec <= rTmrDebounceTimeLimit_sec) OR (rTimer_TT501_CA_sec <= rTmrDebounceTimeLimit_sec);
bDiscrepancy_TT501 := (rTimer_TT501_AB_sec > 0.050) OR (rTimer_TT501_BC_sec > 0.050) OR (rTimer_TT501_CA_sec > 0.050);

IF bHealthy_TT501A AND bHealthy_TT501B AND bHealthy_TT501C THEN
    IF (rTT_MoldTemp_501A >= rTT_MoldTemp_501B AND rTT_MoldTemp_501A <= rTT_MoldTemp_501C) OR
       (rTT_MoldTemp_501A <= rTT_MoldTemp_501B AND rTT_MoldTemp_501A >= rTT_MoldTemp_501C) THEN
        rVoted_TT501_degC := rTT_MoldTemp_501A;
    ELSIF (rTT_MoldTemp_501B >= rTT_MoldTemp_501A AND rTT_MoldTemp_501B <= rTT_MoldTemp_501C) OR
          (rTT_MoldTemp_501B <= rTT_MoldTemp_501A AND rTT_MoldTemp_501B >= rTT_MoldTemp_501C) THEN
        rVoted_TT501_degC := rTT_MoldTemp_501B;
    ELSE
        rVoted_TT501_degC := rTT_MoldTemp_501C;
    END_IF;
    bDegraded_TT501 := FALSE;
ELSIF bHealthy_TT501A AND bHealthy_TT501B THEN
    rVoted_TT501_degC := 0.5 * (rTT_MoldTemp_501A + rTT_MoldTemp_501B);
    bDegraded_TT501 := TRUE;
ELSIF bHealthy_TT501B AND bHealthy_TT501C THEN
    rVoted_TT501_degC := 0.5 * (rTT_MoldTemp_501B + rTT_MoldTemp_501C);
    bDegraded_TT501 := TRUE;
ELSIF bHealthy_TT501A AND bHealthy_TT501C THEN
    rVoted_TT501_degC := 0.5 * (rTT_MoldTemp_501A + rTT_MoldTemp_501C);
    bDegraded_TT501 := TRUE;
ELSIF bHealthy_TT501A THEN
    rVoted_TT501_degC := rTT_MoldTemp_501A;
    bDegraded_TT501 := TRUE;
ELSIF bHealthy_TT501B THEN
    rVoted_TT501_degC := rTT_MoldTemp_501B;
    bDegraded_TT501 := TRUE;
ELSIF bHealthy_TT501C THEN
    rVoted_TT501_degC := rTT_MoldTemp_501C;
    bDegraded_TT501 := TRUE;
ELSE
    rVoted_TT501_degC := rVoted_TT501_Prev;
    bDegraded_TT501 := TRUE;
END_IF;
rVoted_TT501_degC := rVoted_TT501_Prev + LIMIT(-0.5, rVoted_TT501_degC - rVoted_TT501_Prev, 0.5);
rVoted_TT501_Prev := rVoted_TT501_degC;
"""

def generate_phase2():
    return """
(* ==================================================================================================== *)
(* PHASE 2: FIRST-PRINCIPLES CYBER-PHYSICAL OBSERVERS & NON-NEWTONIAN RHEOLOGY                          *)
(* Online Evaluator for:                                                                                *)
(*   1. Apparent Shear Rate gamma_dot [1/s] and Cross-WLF Melt Dynamic Viscosity eta [Pa.s]              *)
(*   2. Real-Time Cavity Pressure Derivative d(P_cav1)/dt [bar/s] with 1st-Order Low-Pass Digital Filter*)
(*   3. Gate Freeze-Off Skin Solidification Stefan Boundary Layer Growth [um]                           *)
(*   4. Dynamic Mold Parting Line Separation Deflection Delta_z [um]                                    *)
(*   5. Screw Linear Velocity Derivative Differentiator [mm/s]                                          *)
(* ==================================================================================================== *)

(* 1. Numerical Differentiation of Screw Linear Position to Velocity *)
IF rCycleTime_sec > 0.0 THEN
    rCalculatedScrewVelocity_mms := (rVoted_ST301_mm - rPrevScrewPos_mm) / rCycleTime_sec;
ELSE
    rCalculatedScrewVelocity_mms := 0.0;
END_IF;
rPrevScrewPos_mm := rVoted_ST301_mm;

(* 2. Apparent Shear Rate & Cross-WLF Melt Rheology Evaluation *)
(* Volumetric Flow Rate Q = A_screw * v_screw [m3/s] *)
rMeltFlowRate_m3s := rScrewArea_m2 * (ABS(rCalculatedScrewVelocity_mms) * 0.001);

(* Apparent Shear Rate in Nozzle Tip: gamma_dot = 4*Q / (PI * R_nozzle^3) *)
IF rNozzleRadius_m > 0.0001 THEN
    rCalculatedShearRate_s1 := (4.0 * rMeltFlowRate_m3s) / (3.14159265 * EXPT(rNozzleRadius_m, 3.0));
ELSE
    rCalculatedShearRate_s1 := 1.0;
END_IF;
rCalculatedShearRate_s1 := MAX(1.0, rCalculatedShearRate_s1);

(* Absolute Melt Temperature [K] *)
rMeltTemp_Kelvin := rTT_BarrelMeltTemp_Zone1 + 273.15;

(* WLF Zero-Shear Viscosity: eta_0 = D1 * exp(- (A1 * (T - D2)) / (A2 + (T - D2))) *)
IF (rPolymer_A2_prime_K + (rMeltTemp_Kelvin - rPolymer_D2_K)) > 1.0 THEN
    rZeroShearViscosity_Pas := rPolymer_D1_Pas * EXP( - (rPolymer_A1 * (rMeltTemp_Kelvin - rPolymer_D2_K)) /
                               (rPolymer_A2_prime_K + (rMeltTemp_Kelvin - rPolymer_D2_K)) );
ELSE
    rZeroShearViscosity_Pas := 1250.0;
END_IF;
rZeroShearViscosity_Pas := LIMIT(100.0, rZeroShearViscosity_Pas, 1.0e8);

(* Cross-WLF Apparent Shear-Thinning Viscosity: eta = eta_0 / (1 + (eta_0 * gamma_dot / tau_star)^(1-n)) *)
rShearStressRatio := (rZeroShearViscosity_Pas * rCalculatedShearRate_s1) / rPolymer_TauStar_Pa;
IF rShearStressRatio > 0.00001 THEN
    rCalculatedViscosity_Pas := rZeroShearViscosity_Pas / (1.0 + EXPT(rShearStressRatio, (1.0 - rPolymer_PowerLaw_n)));
ELSE
    rCalculatedViscosity_Pas := rZeroShearViscosity_Pas;
END_IF;
rCalculatedViscosity_Pas := LIMIT(15.0, rCalculatedViscosity_Pas, 50000.0);

(* 3. Cavity 1 Pressure Numerical Derivative with Digital Low-Pass Filtering *)
IF rCycleTime_sec > 0.0 THEN
    rRaw_dPCav_dt := (rVoted_PT201_bar - rPrevCavity1Press_bar) / rCycleTime_sec;
ELSE
    rRaw_dPCav_dt := 0.0;
END_IF;
rPrevCavity1Press_bar := rVoted_PT201_bar;

(* 1st-Order Butterworth Discrete Filter (cutoff approx 50 Hz at Ts = 1 ms): alpha = 0.24 *)
rFiltered_dPCav_dt := (0.76 * rFiltered_dPCav_dt) + (0.24 * rRaw_dPCav_dt);

(* 4. Stefan Problem: Gate Solidification Frozen Skin Layer Growth *)
(* delta_skin(t) accumulates during packing when melt velocity drops below shear threshold *)
IF nFsmState = 6 THEN (* Holding Phase Active *)
    IF ABS(rCalculatedScrewVelocity_mms) < 5.0 THEN
        (* Conduction-driven skin growth rate: d(delta)/dt = alpha_th / delta *)
        IF x_state[7] > 10.0 THEN
            rSkinGrowthRate_ums := (rThermalDiffusivity_m2s * 1.0e12) / x_state[7];
        ELSE
            rSkinGrowthRate_ums := 45.0; (* Initial rapid flash quench rate [um/s] *)
        END_IF;
        x_state[7] := x_state[7] + (rSkinGrowthRate_ums * rCycleTime_sec);
    ELSE
        (* Shear scouring reduces skin layer *)
        x_state[7] := MAX(0.0, x_state[7] - (12.0 * rCycleTime_sec));
    END_IF;
ELSIF nFsmState = 4 OR nFsmState = 5 THEN (* Fast Volumetric Fill: High shear prevents frozen skin *)
    x_state[7] := 0.0;
END_IF;
x_state[7] := LIMIT(0.0, x_state[7], rGateHalfThickness_um);

(* 5. Mold Parting Line Deflection & Separation Mechanics *)
(* Total opening force generated by 4 cavities: F_open = P_avg * A_proj *)
(* 1 bar = 100 kN/m2. F_open [kN] = P_avg [bar] * 100 [kN/(m2*bar)] * A_proj [m2] *)
rMeltTotalOpeningForce_kN := (0.5 * (rVoted_PT201_bar + rPT_Cavity_204_EndFill)) * 100.0 * rProjectedArea_m2;

(* Parting Line Separation Deflection: Delta_z = (F_open - F_clamp) / K_mold [mm -> um] *)
IF (rMeltTotalOpeningForce_kN > rVoted_WT401_kN) AND (rMoldStiffness_kNmm > 1000.0) THEN
    rMoldSeparation_um := ((rMeltTotalOpeningForce_kN - rVoted_WT401_kN) / rMoldStiffness_kNmm) * 1000.0;
ELSE
    rMoldSeparation_um := 0.0;
END_IF;
"""
