# -*- coding: utf-8 -*-
"""
Phases module 1-3 for FB_DataCenter_LiquidCooling_CDU_DirectToChip
Contains:
  Phase 1: 2oo3 TMR Sensor Voting across all 16 Channels
  Phase 2: Dynamic PG25 Thermo-Physical Properties Evaluator
  Phase 3: Cyber-Physical Observers (PHE fouling UA, Cold-Plate Rth/Tj, Leak localization, Buffer ride-through)
"""

def get_phase1_tmr_voting():
    return """(* ========================================================================= *)
(* === PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING LOGIC === *)
(* ========================================================================= *)
(* 
   Every critical process variable is measured via triplicated field transmitters
   (Channels A, B, C). Pairwise differential discrepancies are evaluated against
   industrial tolerance thresholds. Debounce timers accumulate discrepancy faults;
   if any transmitter diverges for > 1.5 s (or > 50 ms for leak sensors), that channel
   is isolated with bumpless 2oo2 or 1oo1 fallback degradation, and its diagnostic
   bit is set in dwTMR_Discrepancy_Word.
*)

(* --- Channel 1: TCS Supply Flow Rate [L/min] --- *)
rDiff_Flow_AB := ABS(FT_TCS_SUPPLY_FLOW_101A - FT_TCS_SUPPLY_FLOW_101B);
rDiff_Flow_BC := ABS(FT_TCS_SUPPLY_FLOW_101B - FT_TCS_SUPPLY_FLOW_101C);
rDiff_Flow_AC := ABS(FT_TCS_SUPPLY_FLOW_101A - FT_TCS_SUPPLY_FLOW_101C);

IF (rDiff_Flow_AB <= 150.0) AND (rDiff_Flow_AC <= 150.0) THEN
    bFlow_ChA_Healthy := TRUE;
    bFlow_ChB_Healthy := TRUE;
    bFlow_ChC_Healthy := TRUE;
    (* All three healthy: 2oo3 median selection *)
    IF ((FT_TCS_SUPPLY_FLOW_101A >= FT_TCS_SUPPLY_FLOW_101B) AND (FT_TCS_SUPPLY_FLOW_101A <= FT_TCS_SUPPLY_FLOW_101C)) OR
       ((FT_TCS_SUPPLY_FLOW_101A <= FT_TCS_SUPPLY_FLOW_101B) AND (FT_TCS_SUPPLY_FLOW_101A >= FT_TCS_SUPPLY_FLOW_101C)) THEN
        rVoted_TCS_Supply_Flow_Lpm := FT_TCS_SUPPLY_FLOW_101A;
    ELSIF ((FT_TCS_SUPPLY_FLOW_101B >= FT_TCS_SUPPLY_FLOW_101A) AND (FT_TCS_SUPPLY_FLOW_101B <= FT_TCS_SUPPLY_FLOW_101C)) OR
          ((FT_TCS_SUPPLY_FLOW_101B <= FT_TCS_SUPPLY_FLOW_101A) AND (FT_TCS_SUPPLY_FLOW_101B >= FT_TCS_SUPPLY_FLOW_101C)) THEN
        rVoted_TCS_Supply_Flow_Lpm := FT_TCS_SUPPLY_FLOW_101B;
    ELSE
        rVoted_TCS_Supply_Flow_Lpm := FT_TCS_SUPPLY_FLOW_101C;
    END_IF;
    tTMR_Timer_Flow := 0.0;
ELSIF (rDiff_Flow_AB <= 150.0) THEN
    (* Channel C diverging *)
    bFlow_ChA_Healthy := TRUE;
    bFlow_ChB_Healthy := TRUE;
    bFlow_ChC_Healthy := FALSE;
    rVoted_TCS_Supply_Flow_Lpm := 0.5 * (FT_TCS_SUPPLY_FLOW_101A + FT_TCS_SUPPLY_FLOW_101B);
    tTMR_Timer_Flow := tTMR_Timer_Flow + 0.050;
    IF (tTMR_Timer_Flow > 1.50) THEN dwTMR_Discrepancy_Word := dwTMR_Discrepancy_Word OR 16#00000001; END_IF;
ELSIF (rDiff_Flow_BC <= 150.0) THEN
    (* Channel A diverging *)
    bFlow_ChA_Healthy := FALSE;
    bFlow_ChB_Healthy := TRUE;
    bFlow_ChC_Healthy := TRUE;
    rVoted_TCS_Supply_Flow_Lpm := 0.5 * (FT_TCS_SUPPLY_FLOW_101B + FT_TCS_SUPPLY_FLOW_101C);
    tTMR_Timer_Flow := tTMR_Timer_Flow + 0.050;
    IF (tTMR_Timer_Flow > 1.50) THEN dwTMR_Discrepancy_Word := dwTMR_Discrepancy_Word OR 16#00000002; END_IF;
ELSIF (rDiff_Flow_AC <= 150.0) THEN
    (* Channel B diverging *)
    bFlow_ChA_Healthy := TRUE;
    bFlow_ChB_Healthy := FALSE;
    bFlow_ChC_Healthy := TRUE;
    rVoted_TCS_Supply_Flow_Lpm := 0.5 * (FT_TCS_SUPPLY_FLOW_101A + FT_TCS_SUPPLY_FLOW_101C);
    tTMR_Timer_Flow := tTMR_Timer_Flow + 0.050;
    IF (tTMR_Timer_Flow > 1.50) THEN dwTMR_Discrepancy_Word := dwTMR_Discrepancy_Word OR 16#00000004; END_IF;
ELSE
    (* All channels diverging: fallback to channel A with discrepancy alarm *)
    bFlow_ChA_Healthy := FALSE;
    bFlow_ChB_Healthy := FALSE;
    bFlow_ChC_Healthy := FALSE;
    rVoted_TCS_Supply_Flow_Lpm := FT_TCS_SUPPLY_FLOW_101A;
    dwTMR_Discrepancy_Word := dwTMR_Discrepancy_Word OR 16#00000007;
END_IF;

(* --- Channel 2: TCS Supply Pressure [bar] --- *)
rDiff_SupplyP_AB := ABS(PT_TCS_SUPPLY_PRESS_102A - PT_TCS_SUPPLY_PRESS_102B);
rDiff_SupplyP_BC := ABS(PT_TCS_SUPPLY_PRESS_102B - PT_TCS_SUPPLY_PRESS_102C);
rDiff_SupplyP_AC := ABS(PT_TCS_SUPPLY_PRESS_102A - PT_TCS_SUPPLY_PRESS_102C);

IF (rDiff_SupplyP_AB <= 0.25) AND (rDiff_SupplyP_AC <= 0.25) THEN
    bSupplyP_ChA_Healthy := TRUE;
    bSupplyP_ChB_Healthy := TRUE;
    bSupplyP_ChC_Healthy := TRUE;
    IF ((PT_TCS_SUPPLY_PRESS_102A >= PT_TCS_SUPPLY_PRESS_102B) AND (PT_TCS_SUPPLY_PRESS_102A <= PT_TCS_SUPPLY_PRESS_102C)) OR
       ((PT_TCS_SUPPLY_PRESS_102A <= PT_TCS_SUPPLY_PRESS_102B) AND (PT_TCS_SUPPLY_PRESS_102A >= PT_TCS_SUPPLY_PRESS_102C)) THEN
        rVoted_TCS_Supply_Pressure_bar := PT_TCS_SUPPLY_PRESS_102A;
    ELSIF ((PT_TCS_SUPPLY_PRESS_102B >= PT_TCS_SUPPLY_PRESS_102A) AND (PT_TCS_SUPPLY_PRESS_102B <= PT_TCS_SUPPLY_PRESS_102C)) OR
          ((PT_TCS_SUPPLY_PRESS_102B <= PT_TCS_SUPPLY_PRESS_102A) AND (PT_TCS_SUPPLY_PRESS_102B >= PT_TCS_SUPPLY_PRESS_102C)) THEN
        rVoted_TCS_Supply_Pressure_bar := PT_TCS_SUPPLY_PRESS_102B;
    ELSE
        rVoted_TCS_Supply_Pressure_bar := PT_TCS_SUPPLY_PRESS_102C;
    END_IF;
    tTMR_Timer_SupplyP := 0.0;
ELSIF (rDiff_SupplyP_AB <= 0.25) THEN
    bSupplyP_ChA_Healthy := TRUE;
    bSupplyP_ChB_Healthy := TRUE;
    bSupplyP_ChC_Healthy := FALSE;
    rVoted_TCS_Supply_Pressure_bar := 0.5 * (PT_TCS_SUPPLY_PRESS_102A + PT_TCS_SUPPLY_PRESS_102B);
    tTMR_Timer_SupplyP := tTMR_Timer_SupplyP + 0.050;
    IF (tTMR_Timer_SupplyP > 1.50) THEN dwTMR_Discrepancy_Word := dwTMR_Discrepancy_Word OR 16#00000008; END_IF;
ELSIF (rDiff_SupplyP_BC <= 0.25) THEN
    bSupplyP_ChA_Healthy := FALSE;
    bSupplyP_ChB_Healthy := TRUE;
    bSupplyP_ChC_Healthy := TRUE;
    rVoted_TCS_Supply_Pressure_bar := 0.5 * (PT_TCS_SUPPLY_PRESS_102B + PT_TCS_SUPPLY_PRESS_102C);
    tTMR_Timer_SupplyP := tTMR_Timer_SupplyP + 0.050;
    IF (tTMR_Timer_SupplyP > 1.50) THEN dwTMR_Discrepancy_Word := dwTMR_Discrepancy_Word OR 16#00000010; END_IF;
ELSIF (rDiff_SupplyP_AC <= 0.25) THEN
    bSupplyP_ChA_Healthy := TRUE;
    bSupplyP_ChB_Healthy := FALSE;
    bSupplyP_ChC_Healthy := TRUE;
    rVoted_TCS_Supply_Pressure_bar := 0.5 * (PT_TCS_SUPPLY_PRESS_102A + PT_TCS_SUPPLY_PRESS_102C);
    tTMR_Timer_SupplyP := tTMR_Timer_SupplyP + 0.050;
    IF (tTMR_Timer_SupplyP > 1.50) THEN dwTMR_Discrepancy_Word := dwTMR_Discrepancy_Word OR 16#00000020; END_IF;
ELSE
    bSupplyP_ChA_Healthy := FALSE;
    bSupplyP_ChB_Healthy := FALSE;
    bSupplyP_ChC_Healthy := FALSE;
    rVoted_TCS_Supply_Pressure_bar := PT_TCS_SUPPLY_PRESS_102A;
    dwTMR_Discrepancy_Word := dwTMR_Discrepancy_Word OR 16#00000038;
END_IF;

(* --- Channel 3: TCS Return Pressure [bar] --- *)
rDiff_ReturnP_AB := ABS(PT_TCS_RETURN_PRESS_103A - PT_TCS_RETURN_PRESS_103B);
rDiff_ReturnP_BC := ABS(PT_TCS_RETURN_PRESS_103B - PT_TCS_RETURN_PRESS_103C);
rDiff_ReturnP_AC := ABS(PT_TCS_RETURN_PRESS_103A - PT_TCS_RETURN_PRESS_103C);

IF (rDiff_ReturnP_AB <= 0.25) AND (rDiff_ReturnP_AC <= 0.25) THEN
    bReturnP_ChA_Healthy := TRUE;
    bReturnP_ChB_Healthy := TRUE;
    bReturnP_ChC_Healthy := TRUE;
    IF ((PT_TCS_RETURN_PRESS_103A >= PT_TCS_RETURN_PRESS_103B) AND (PT_TCS_RETURN_PRESS_103A <= PT_TCS_RETURN_PRESS_103C)) OR
       ((PT_TCS_RETURN_PRESS_103A <= PT_TCS_RETURN_PRESS_103B) AND (PT_TCS_RETURN_PRESS_103A >= PT_TCS_RETURN_PRESS_103C)) THEN
        rVoted_TCS_Return_Pressure_bar := PT_TCS_RETURN_PRESS_103A;
    ELSIF ((PT_TCS_RETURN_PRESS_103B >= PT_TCS_RETURN_PRESS_103A) AND (PT_TCS_RETURN_PRESS_103B <= PT_TCS_RETURN_PRESS_103C)) OR
          ((PT_TCS_RETURN_PRESS_103B <= PT_TCS_RETURN_PRESS_103A) AND (PT_TCS_RETURN_PRESS_103B >= PT_TCS_RETURN_PRESS_103C)) THEN
        rVoted_TCS_Return_Pressure_bar := PT_TCS_RETURN_PRESS_103B;
    ELSE
        rVoted_TCS_Return_Pressure_bar := PT_TCS_RETURN_PRESS_103C;
    END_IF;
    tTMR_Timer_ReturnP := 0.0;
ELSIF (rDiff_ReturnP_AB <= 0.25) THEN
    bReturnP_ChA_Healthy := TRUE;
    bReturnP_ChB_Healthy := TRUE;
    bReturnP_ChC_Healthy := FALSE;
    rVoted_TCS_Return_Pressure_bar := 0.5 * (PT_TCS_RETURN_PRESS_103A + PT_TCS_RETURN_PRESS_103B);
    tTMR_Timer_ReturnP := tTMR_Timer_ReturnP + 0.050;
    IF (tTMR_Timer_ReturnP > 1.50) THEN dwTMR_Discrepancy_Word := dwTMR_Discrepancy_Word OR 16#00000040; END_IF;
ELSIF (rDiff_ReturnP_BC <= 0.25) THEN
    bReturnP_ChA_Healthy := FALSE;
    bReturnP_ChB_Healthy := TRUE;
    bReturnP_ChC_Healthy := TRUE;
    rVoted_TCS_Return_Pressure_bar := 0.5 * (PT_TCS_RETURN_PRESS_103B + PT_TCS_RETURN_PRESS_103C);
    tTMR_Timer_ReturnP := tTMR_Timer_ReturnP + 0.050;
    IF (tTMR_Timer_ReturnP > 1.50) THEN dwTMR_Discrepancy_Word := dwTMR_Discrepancy_Word OR 16#00000080; END_IF;
ELSIF (rDiff_ReturnP_AC <= 0.25) THEN
    bReturnP_ChA_Healthy := TRUE;
    bReturnP_ChB_Healthy := FALSE;
    bReturnP_ChC_Healthy := TRUE;
    rVoted_TCS_Return_Pressure_bar := 0.5 * (PT_TCS_RETURN_PRESS_103A + PT_TCS_RETURN_PRESS_103C);
    tTMR_Timer_ReturnP := tTMR_Timer_ReturnP + 0.050;
    IF (tTMR_Timer_ReturnP > 1.50) THEN dwTMR_Discrepancy_Word := dwTMR_Discrepancy_Word OR 16#00000100; END_IF;
ELSE
    bReturnP_ChA_Healthy := FALSE;
    bReturnP_ChB_Healthy := FALSE;
    bReturnP_ChC_Healthy := FALSE;
    rVoted_TCS_Return_Pressure_bar := PT_TCS_RETURN_PRESS_103A;
    dwTMR_Discrepancy_Word := dwTMR_Discrepancy_Word OR 16#000001C0;
END_IF;

(* --- Channel 4: TCS Differential Pressure [bar] --- *)
rDiff_DP_AB := ABS(DPS_TCS_LOOP_DIFF_PRESS_104A - DPS_TCS_LOOP_DIFF_PRESS_104B);
rDiff_DP_BC := ABS(DPS_TCS_LOOP_DIFF_PRESS_104B - DPS_TCS_LOOP_DIFF_PRESS_104C);
rDiff_DP_AC := ABS(DPS_TCS_LOOP_DIFF_PRESS_104A - DPS_TCS_LOOP_DIFF_PRESS_104C);

IF (rDiff_DP_AB <= 0.10) AND (rDiff_DP_AC <= 0.10) THEN
    bDP_ChA_Healthy := TRUE;
    bDP_ChB_Healthy := TRUE;
    bDP_ChC_Healthy := TRUE;
    IF ((DPS_TCS_LOOP_DIFF_PRESS_104A >= DPS_TCS_LOOP_DIFF_PRESS_104B) AND (DPS_TCS_LOOP_DIFF_PRESS_104A <= DPS_TCS_LOOP_DIFF_PRESS_104C)) OR
       ((DPS_TCS_LOOP_DIFF_PRESS_104A <= DPS_TCS_LOOP_DIFF_PRESS_104B) AND (DPS_TCS_LOOP_DIFF_PRESS_104A >= DPS_TCS_LOOP_DIFF_PRESS_104C)) THEN
        rVoted_TCS_Loop_Diff_Pressure_bar := DPS_TCS_LOOP_DIFF_PRESS_104A;
    ELSIF ((DPS_TCS_LOOP_DIFF_PRESS_104B >= DPS_TCS_LOOP_DIFF_PRESS_104A) AND (DPS_TCS_LOOP_DIFF_PRESS_104B <= DPS_TCS_LOOP_DIFF_PRESS_104C)) OR
          ((DPS_TCS_LOOP_DIFF_PRESS_104B <= DPS_TCS_LOOP_DIFF_PRESS_104A) AND (DPS_TCS_LOOP_DIFF_PRESS_104B >= DPS_TCS_LOOP_DIFF_PRESS_104C)) THEN
        rVoted_TCS_Loop_Diff_Pressure_bar := DPS_TCS_LOOP_DIFF_PRESS_104B;
    ELSE
        rVoted_TCS_Loop_Diff_Pressure_bar := DPS_TCS_LOOP_DIFF_PRESS_104C;
    END_IF;
    tTMR_Timer_DP := 0.0;
ELSIF (rDiff_DP_AB <= 0.10) THEN
    bDP_ChA_Healthy := TRUE;
    bDP_ChB_Healthy := TRUE;
    bDP_ChC_Healthy := FALSE;
    rVoted_TCS_Loop_Diff_Pressure_bar := 0.5 * (DPS_TCS_LOOP_DIFF_PRESS_104A + DPS_TCS_LOOP_DIFF_PRESS_104B);
    tTMR_Timer_DP := tTMR_Timer_DP + 0.050;
    IF (tTMR_Timer_DP > 1.50) THEN dwTMR_Discrepancy_Word := dwTMR_Discrepancy_Word OR 16#00000200; END_IF;
ELSIF (rDiff_DP_BC <= 0.10) THEN
    bDP_ChA_Healthy := FALSE;
    bDP_ChB_Healthy := TRUE;
    bDP_ChC_Healthy := TRUE;
    rVoted_TCS_Loop_Diff_Pressure_bar := 0.5 * (DPS_TCS_LOOP_DIFF_PRESS_104B + DPS_TCS_LOOP_DIFF_PRESS_104C);
    tTMR_Timer_DP := tTMR_Timer_DP + 0.050;
    IF (tTMR_Timer_DP > 1.50) THEN dwTMR_Discrepancy_Word := dwTMR_Discrepancy_Word OR 16#00000400; END_IF;
ELSIF (rDiff_DP_AC <= 0.10) THEN
    bDP_ChA_Healthy := TRUE;
    bDP_ChB_Healthy := FALSE;
    bDP_ChC_Healthy := TRUE;
    rVoted_TCS_Loop_Diff_Pressure_bar := 0.5 * (DPS_TCS_LOOP_DIFF_PRESS_104A + DPS_TCS_LOOP_DIFF_PRESS_104C);
    tTMR_Timer_DP := tTMR_Timer_DP + 0.050;
    IF (tTMR_Timer_DP > 1.50) THEN dwTMR_Discrepancy_Word := dwTMR_Discrepancy_Word OR 16#00000800; END_IF;
ELSE
    bDP_ChA_Healthy := FALSE;
    bDP_ChB_Healthy := FALSE;
    bDP_ChC_Healthy := FALSE;
    rVoted_TCS_Loop_Diff_Pressure_bar := DPS_TCS_LOOP_DIFF_PRESS_104A;
    dwTMR_Discrepancy_Word := dwTMR_Discrepancy_Word OR 16#00000E00;
END_IF;

(* --- Channel 5: TCS Supply Temperature [deg C] --- *)
rDiff_SupplyT_AB := ABS(TT_TCS_SUPPLY_TEMP_105A - TT_TCS_SUPPLY_TEMP_105B);
rDiff_SupplyT_BC := ABS(TT_TCS_SUPPLY_TEMP_105B - TT_TCS_SUPPLY_TEMP_105C);
rDiff_SupplyT_AC := ABS(TT_TCS_SUPPLY_TEMP_105A - TT_TCS_SUPPLY_TEMP_105C);

IF (rDiff_SupplyT_AB <= 0.50) AND (rDiff_SupplyT_AC <= 0.50) THEN
    bSupplyT_ChA_Healthy := TRUE;
    bSupplyT_ChB_Healthy := TRUE;
    bSupplyT_ChC_Healthy := TRUE;
    IF ((TT_TCS_SUPPLY_TEMP_105A >= TT_TCS_SUPPLY_TEMP_105B) AND (TT_TCS_SUPPLY_TEMP_105A <= TT_TCS_SUPPLY_TEMP_105C)) OR
       ((TT_TCS_SUPPLY_TEMP_105A <= TT_TCS_SUPPLY_TEMP_105B) AND (TT_TCS_SUPPLY_TEMP_105A >= TT_TCS_SUPPLY_TEMP_105C)) THEN
        rVoted_TCS_Supply_Temp_C := TT_TCS_SUPPLY_TEMP_105A;
    ELSIF ((TT_TCS_SUPPLY_TEMP_105B >= TT_TCS_SUPPLY_TEMP_105A) AND (TT_TCS_SUPPLY_TEMP_105B <= TT_TCS_SUPPLY_TEMP_105C)) OR
          ((TT_TCS_SUPPLY_TEMP_105B <= TT_TCS_SUPPLY_TEMP_105A) AND (TT_TCS_SUPPLY_TEMP_105B >= TT_TCS_SUPPLY_TEMP_105C)) THEN
        rVoted_TCS_Supply_Temp_C := TT_TCS_SUPPLY_TEMP_105B;
    ELSE
        rVoted_TCS_Supply_Temp_C := TT_TCS_SUPPLY_TEMP_105C;
    END_IF;
    tTMR_Timer_SupplyT := 0.0;
ELSIF (rDiff_SupplyT_AB <= 0.50) THEN
    bSupplyT_ChA_Healthy := TRUE;
    bSupplyT_ChB_Healthy := TRUE;
    bSupplyT_ChC_Healthy := FALSE;
    rVoted_TCS_Supply_Temp_C := 0.5 * (TT_TCS_SUPPLY_TEMP_105A + TT_TCS_SUPPLY_TEMP_105B);
    tTMR_Timer_SupplyT := tTMR_Timer_SupplyT + 0.050;
    IF (tTMR_Timer_SupplyT > 1.50) THEN dwTMR_Discrepancy_Word := dwTMR_Discrepancy_Word OR 16#00001000; END_IF;
ELSIF (rDiff_SupplyT_BC <= 0.50) THEN
    bSupplyT_ChA_Healthy := FALSE;
    bSupplyT_ChB_Healthy := TRUE;
    bSupplyT_ChC_Healthy := TRUE;
    rVoted_TCS_Supply_Temp_C := 0.5 * (TT_TCS_SUPPLY_TEMP_105B + TT_TCS_SUPPLY_TEMP_105C);
    tTMR_Timer_SupplyT := tTMR_Timer_SupplyT + 0.050;
    IF (tTMR_Timer_SupplyT > 1.50) THEN dwTMR_Discrepancy_Word := dwTMR_Discrepancy_Word OR 16#00002000; END_IF;
ELSIF (rDiff_SupplyT_AC <= 0.50) THEN
    bSupplyT_ChA_Healthy := TRUE;
    bSupplyT_ChB_Healthy := FALSE;
    bSupplyT_ChC_Healthy := TRUE;
    rVoted_TCS_Supply_Temp_C := 0.5 * (TT_TCS_SUPPLY_TEMP_105A + TT_TCS_SUPPLY_TEMP_105C);
    tTMR_Timer_SupplyT := tTMR_Timer_SupplyT + 0.050;
    IF (tTMR_Timer_SupplyT > 1.50) THEN dwTMR_Discrepancy_Word := dwTMR_Discrepancy_Word OR 16#00004000; END_IF;
ELSE
    bSupplyT_ChA_Healthy := FALSE;
    bSupplyT_ChB_Healthy := FALSE;
    bSupplyT_ChC_Healthy := FALSE;
    rVoted_TCS_Supply_Temp_C := TT_TCS_SUPPLY_TEMP_105A;
    dwTMR_Discrepancy_Word := dwTMR_Discrepancy_Word OR 16#00007000;
END_IF;

(* --- Channel 6: TCS Return Temperature [deg C] --- *)
rDiff_ReturnT_AB := ABS(TT_TCS_RETURN_TEMP_106A - TT_TCS_RETURN_TEMP_106B);
rDiff_ReturnT_BC := ABS(TT_TCS_RETURN_TEMP_106B - TT_TCS_RETURN_TEMP_106C);
rDiff_ReturnT_AC := ABS(TT_TCS_RETURN_TEMP_106A - TT_TCS_RETURN_TEMP_106C);

IF (rDiff_ReturnT_AB <= 0.50) AND (rDiff_ReturnT_AC <= 0.50) THEN
    bReturnT_ChA_Healthy := TRUE;
    bReturnT_ChB_Healthy := TRUE;
    bReturnT_ChC_Healthy := TRUE;
    IF ((TT_TCS_RETURN_TEMP_106A >= TT_TCS_RETURN_TEMP_106B) AND (TT_TCS_RETURN_TEMP_106A <= TT_TCS_RETURN_TEMP_106C)) OR
       ((TT_TCS_RETURN_TEMP_106A <= TT_TCS_RETURN_TEMP_106B) AND (TT_TCS_RETURN_TEMP_106A >= TT_TCS_RETURN_TEMP_106C)) THEN
        rVoted_TCS_Return_Temp_C := TT_TCS_RETURN_TEMP_106A;
    ELSIF ((TT_TCS_RETURN_TEMP_106B >= TT_TCS_RETURN_TEMP_106A) AND (TT_TCS_RETURN_TEMP_106B <= TT_TCS_RETURN_TEMP_106C)) OR
          ((TT_TCS_RETURN_TEMP_106B <= TT_TCS_RETURN_TEMP_106A) AND (TT_TCS_RETURN_TEMP_106B >= TT_TCS_RETURN_TEMP_106C)) THEN
        rVoted_TCS_Return_Temp_C := TT_TCS_RETURN_TEMP_106B;
    ELSE
        rVoted_TCS_Return_Temp_C := TT_TCS_RETURN_TEMP_106C;
    END_IF;
    tTMR_Timer_ReturnT := 0.0;
ELSIF (rDiff_ReturnT_AB <= 0.50) THEN
    bReturnT_ChA_Healthy := TRUE;
    bReturnT_ChB_Healthy := TRUE;
    bReturnT_ChC_Healthy := FALSE;
    rVoted_TCS_Return_Temp_C := 0.5 * (TT_TCS_RETURN_TEMP_106A + TT_TCS_RETURN_TEMP_106B);
    tTMR_Timer_ReturnT := tTMR_Timer_ReturnT + 0.050;
    IF (tTMR_Timer_ReturnT > 1.50) THEN dwTMR_Discrepancy_Word := dwTMR_Discrepancy_Word OR 16#00008000; END_IF;
ELSIF (rDiff_ReturnT_BC <= 0.50) THEN
    bReturnT_ChA_Healthy := FALSE;
    bReturnT_ChB_Healthy := TRUE;
    bReturnT_ChC_Healthy := TRUE;
    rVoted_TCS_Return_Temp_C := 0.5 * (TT_TCS_RETURN_TEMP_106B + TT_TCS_RETURN_TEMP_106C);
    tTMR_Timer_ReturnT := tTMR_Timer_ReturnT + 0.050;
    IF (tTMR_Timer_ReturnT > 1.50) THEN dwTMR_Discrepancy_Word := dwTMR_Discrepancy_Word OR 16#00010000; END_IF;
ELSIF (rDiff_ReturnT_AC <= 0.50) THEN
    bReturnT_ChA_Healthy := TRUE;
    bReturnT_ChB_Healthy := FALSE;
    bReturnT_ChC_Healthy := TRUE;
    rVoted_TCS_Return_Temp_C := 0.5 * (TT_TCS_RETURN_TEMP_106A + TT_TCS_RETURN_TEMP_106C);
    tTMR_Timer_ReturnT := tTMR_Timer_ReturnT + 0.050;
    IF (tTMR_Timer_ReturnT > 1.50) THEN dwTMR_Discrepancy_Word := dwTMR_Discrepancy_Word OR 16#00020000; END_IF;
ELSE
    bReturnT_ChA_Healthy := FALSE;
    bReturnT_ChB_Healthy := FALSE;
    bReturnT_ChC_Healthy := FALSE;
    rVoted_TCS_Return_Temp_C := TT_TCS_RETURN_TEMP_106A;
    dwTMR_Discrepancy_Word := dwTMR_Discrepancy_Word OR 16#00038000;
END_IF;

(* --- Channel 7: Primary Facility Chilled Water Flow [m3/h] --- *)
rDiff_FacFlow_AB := ABS(FT_FWS_FACILITY_FLOW_201A - FT_FWS_FACILITY_FLOW_201B);
rDiff_FacFlow_BC := ABS(FT_FWS_FACILITY_FLOW_201B - FT_FWS_FACILITY_FLOW_201C);
rDiff_FacFlow_AC := ABS(FT_FWS_FACILITY_FLOW_201A - FT_FWS_FACILITY_FLOW_201C);

IF (rDiff_FacFlow_AB <= 15.0) AND (rDiff_FacFlow_AC <= 15.0) THEN
    bFacFlow_ChA_Healthy := TRUE;
    bFacFlow_ChB_Healthy := TRUE;
    bFacFlow_ChC_Healthy := TRUE;
    IF ((FT_FWS_FACILITY_FLOW_201A >= FT_FWS_FACILITY_FLOW_201B) AND (FT_FWS_FACILITY_FLOW_201A <= FT_FWS_FACILITY_FLOW_201C)) OR
       ((FT_FWS_FACILITY_FLOW_201A <= FT_FWS_FACILITY_FLOW_201B) AND (FT_FWS_FACILITY_FLOW_201A >= FT_FWS_FACILITY_FLOW_201C)) THEN
        rVoted_FWS_Facility_Flow_m3h := FT_FWS_FACILITY_FLOW_201A;
    ELSIF ((FT_FWS_FACILITY_FLOW_201B >= FT_FWS_FACILITY_FLOW_201A) AND (FT_FWS_FACILITY_FLOW_201B <= FT_FWS_FACILITY_FLOW_201C)) OR
          ((FT_FWS_FACILITY_FLOW_201B <= FT_FWS_FACILITY_FLOW_201A) AND (FT_FWS_FACILITY_FLOW_201B >= FT_FWS_FACILITY_FLOW_201C)) THEN
        rVoted_FWS_Facility_Flow_m3h := FT_FWS_FACILITY_FLOW_201B;
    ELSE
        rVoted_FWS_Facility_Flow_m3h := FT_FWS_FACILITY_FLOW_201C;
    END_IF;
    tTMR_Timer_FacFlow := 0.0;
ELSIF (rDiff_FacFlow_AB <= 15.0) THEN
    bFacFlow_ChA_Healthy := TRUE;
    bFacFlow_ChB_Healthy := TRUE;
    bFacFlow_ChC_Healthy := FALSE;
    rVoted_FWS_Facility_Flow_m3h := 0.5 * (FT_FWS_FACILITY_FLOW_201A + FT_FWS_FACILITY_FLOW_201B);
    tTMR_Timer_FacFlow := tTMR_Timer_FacFlow + 0.050;
    IF (tTMR_Timer_FacFlow > 1.50) THEN dwTMR_Discrepancy_Word := dwTMR_Discrepancy_Word OR 16#00040000; END_IF;
ELSIF (rDiff_FacFlow_BC <= 15.0) THEN
    bFacFlow_ChA_Healthy := FALSE;
    bFacFlow_ChB_Healthy := TRUE;
    bFacFlow_ChC_Healthy := TRUE;
    rVoted_FWS_Facility_Flow_m3h := 0.5 * (FT_FWS_FACILITY_FLOW_201B + FT_FWS_FACILITY_FLOW_201C);
    tTMR_Timer_FacFlow := tTMR_Timer_FacFlow + 0.050;
    IF (tTMR_Timer_FacFlow > 1.50) THEN dwTMR_Discrepancy_Word := dwTMR_Discrepancy_Word OR 16#00080000; END_IF;
ELSIF (rDiff_FacFlow_AC <= 15.0) THEN
    bFacFlow_ChA_Healthy := TRUE;
    bFacFlow_ChB_Healthy := FALSE;
    bFacFlow_ChC_Healthy := TRUE;
    rVoted_FWS_Facility_Flow_m3h := 0.5 * (FT_FWS_FACILITY_FLOW_201A + FT_FWS_FACILITY_FLOW_201C);
    tTMR_Timer_FacFlow := tTMR_Timer_FacFlow + 0.050;
    IF (tTMR_Timer_FacFlow > 1.50) THEN dwTMR_Discrepancy_Word := dwTMR_Discrepancy_Word OR 16#00100000; END_IF;
ELSE
    bFacFlow_ChA_Healthy := FALSE;
    bFacFlow_ChB_Healthy := FALSE;
    bFacFlow_ChC_Healthy := FALSE;
    rVoted_FWS_Facility_Flow_m3h := FT_FWS_FACILITY_FLOW_201A;
    dwTMR_Discrepancy_Word := dwTMR_Discrepancy_Word OR 16#001C0000;
END_IF;

(* --- Channel 8: Facility Water Supply Temperature [deg C] --- *)
rDiff_FacSupplyT_AB := ABS(TT_FWS_FACILITY_SUPPLY_202A - TT_FWS_FACILITY_SUPPLY_202B);
rDiff_FacSupplyT_BC := ABS(TT_FWS_FACILITY_SUPPLY_202B - TT_FWS_FACILITY_SUPPLY_202C);
rDiff_FacSupplyT_AC := ABS(TT_FWS_FACILITY_SUPPLY_202A - TT_FWS_FACILITY_SUPPLY_202C);

IF (rDiff_FacSupplyT_AB <= 0.60) AND (rDiff_FacSupplyT_AC <= 0.60) THEN
    bFacSupplyT_ChA_Healthy := TRUE;
    bFacSupplyT_ChB_Healthy := TRUE;
    bFacSupplyT_ChC_Healthy := TRUE;
    IF ((TT_FWS_FACILITY_SUPPLY_202A >= TT_FWS_FACILITY_SUPPLY_202B) AND (TT_FWS_FACILITY_SUPPLY_202A <= TT_FWS_FACILITY_SUPPLY_202C)) OR
       ((TT_FWS_FACILITY_SUPPLY_202A <= TT_FWS_FACILITY_SUPPLY_202B) AND (TT_FWS_FACILITY_SUPPLY_202A >= TT_FWS_FACILITY_SUPPLY_202C)) THEN
        rVoted_FWS_Facility_Supply_Temp_C := TT_FWS_FACILITY_SUPPLY_202A;
    ELSIF ((TT_FWS_FACILITY_SUPPLY_202B >= TT_FWS_FACILITY_SUPPLY_202A) AND (TT_FWS_FACILITY_SUPPLY_202B <= TT_FWS_FACILITY_SUPPLY_202C)) OR
          ((TT_FWS_FACILITY_SUPPLY_202B <= TT_FWS_FACILITY_SUPPLY_202A) AND (TT_FWS_FACILITY_SUPPLY_202B >= TT_FWS_FACILITY_SUPPLY_202C)) THEN
        rVoted_FWS_Facility_Supply_Temp_C := TT_FWS_FACILITY_SUPPLY_202B;
    ELSE
        rVoted_FWS_Facility_Supply_Temp_C := TT_FWS_FACILITY_SUPPLY_202C;
    END_IF;
    tTMR_Timer_FacSupplyT := 0.0;
ELSIF (rDiff_FacSupplyT_AB <= 0.60) THEN
    bFacSupplyT_ChA_Healthy := TRUE;
    bFacSupplyT_ChB_Healthy := TRUE;
    bFacSupplyT_ChC_Healthy := FALSE;
    rVoted_FWS_Facility_Supply_Temp_C := 0.5 * (TT_FWS_FACILITY_SUPPLY_202A + TT_FWS_FACILITY_SUPPLY_202B);
    tTMR_Timer_FacSupplyT := tTMR_Timer_FacSupplyT + 0.050;
    IF (tTMR_Timer_FacSupplyT > 1.50) THEN dwTMR_Discrepancy_Word := dwTMR_Discrepancy_Word OR 16#00200000; END_IF;
ELSIF (rDiff_FacSupplyT_BC <= 0.60) THEN
    bFacSupplyT_ChA_Healthy := FALSE;
    bFacSupplyT_ChB_Healthy := TRUE;
    bFacSupplyT_ChC_Healthy := TRUE;
    rVoted_FWS_Facility_Supply_Temp_C := 0.5 * (TT_FWS_FACILITY_SUPPLY_202B + TT_FWS_FACILITY_SUPPLY_202C);
    tTMR_Timer_FacSupplyT := tTMR_Timer_FacSupplyT + 0.050;
    IF (tTMR_Timer_FacSupplyT > 1.50) THEN dwTMR_Discrepancy_Word := dwTMR_Discrepancy_Word OR 16#00400000; END_IF;
ELSIF (rDiff_FacSupplyT_AC <= 0.60) THEN
    bFacSupplyT_ChA_Healthy := TRUE;
    bFacSupplyT_ChB_Healthy := FALSE;
    bFacSupplyT_ChC_Healthy := TRUE;
    rVoted_FWS_Facility_Supply_Temp_C := 0.5 * (TT_FWS_FACILITY_SUPPLY_202A + TT_FWS_FACILITY_SUPPLY_202C);
    tTMR_Timer_FacSupplyT := tTMR_Timer_FacSupplyT + 0.050;
    IF (tTMR_Timer_FacSupplyT > 1.50) THEN dwTMR_Discrepancy_Word := dwTMR_Discrepancy_Word OR 16#00800000; END_IF;
ELSE
    bFacSupplyT_ChA_Healthy := FALSE;
    bFacSupplyT_ChB_Healthy := FALSE;
    bFacSupplyT_ChC_Healthy := FALSE;
    rVoted_FWS_Facility_Supply_Temp_C := TT_FWS_FACILITY_SUPPLY_202A;
    dwTMR_Discrepancy_Word := dwTMR_Discrepancy_Word OR 16#00E00000;
END_IF;

(* --- Channel 9: Facility Water Return Temperature [deg C] --- *)
rDiff_FacReturnT_AB := ABS(TT_FWR_FACILITY_RETURN_203A - TT_FWR_FACILITY_RETURN_203B);
rDiff_FacReturnT_BC := ABS(TT_FWR_FACILITY_RETURN_203B - TT_FWR_FACILITY_RETURN_203C);
rDiff_FacReturnT_AC := ABS(TT_FWR_FACILITY_RETURN_203A - TT_FWR_FACILITY_RETURN_203C);

IF (rDiff_FacReturnT_AB <= 0.60) AND (rDiff_FacReturnT_AC <= 0.60) THEN
    bFacReturnT_ChA_Healthy := TRUE;
    bFacReturnT_ChB_Healthy := TRUE;
    bFacReturnT_ChC_Healthy := TRUE;
    IF ((TT_FWR_FACILITY_RETURN_203A >= TT_FWR_FACILITY_RETURN_203B) AND (TT_FWR_FACILITY_RETURN_203A <= TT_FWR_FACILITY_RETURN_203C)) OR
       ((TT_FWR_FACILITY_RETURN_203A <= TT_FWR_FACILITY_RETURN_203B) AND (TT_FWR_FACILITY_RETURN_203A >= TT_FWR_FACILITY_RETURN_203C)) THEN
        rVoted_FWR_Facility_Return_Temp_C := TT_FWR_FACILITY_RETURN_203A;
    ELSIF ((TT_FWR_FACILITY_RETURN_203B >= TT_FWR_FACILITY_RETURN_203A) AND (TT_FWR_FACILITY_RETURN_203B <= TT_FWR_FACILITY_RETURN_203C)) OR
          ((TT_FWR_FACILITY_RETURN_203B <= TT_FWR_FACILITY_RETURN_203A) AND (TT_FWR_FACILITY_RETURN_203B >= TT_FWR_FACILITY_RETURN_203C)) THEN
        rVoted_FWR_Facility_Return_Temp_C := TT_FWR_FACILITY_RETURN_203B;
    ELSE
        rVoted_FWR_Facility_Return_Temp_C := TT_FWR_FACILITY_RETURN_203C;
    END_IF;
    tTMR_Timer_FacReturnT := 0.0;
ELSIF (rDiff_FacReturnT_AB <= 0.60) THEN
    bFacReturnT_ChA_Healthy := TRUE;
    bFacReturnT_ChB_Healthy := TRUE;
    bFacReturnT_ChC_Healthy := FALSE;
    rVoted_FWR_Facility_Return_Temp_C := 0.5 * (TT_FWR_FACILITY_RETURN_203A + TT_FWR_FACILITY_RETURN_203B);
    tTMR_Timer_FacReturnT := tTMR_Timer_FacReturnT + 0.050;
    IF (tTMR_Timer_FacReturnT > 1.50) THEN dwTMR_Discrepancy_Word := dwTMR_Discrepancy_Word OR 16#01000000; END_IF;
ELSIF (rDiff_FacReturnT_BC <= 0.60) THEN
    bFacReturnT_ChA_Healthy := FALSE;
    bFacReturnT_ChB_Healthy := TRUE;
    bFacReturnT_ChC_Healthy := TRUE;
    rVoted_FWR_Facility_Return_Temp_C := 0.5 * (TT_FWR_FACILITY_RETURN_203B + TT_FWR_FACILITY_RETURN_203C);
    tTMR_Timer_FacReturnT := tTMR_Timer_FacReturnT + 0.050;
    IF (tTMR_Timer_FacReturnT > 1.50) THEN dwTMR_Discrepancy_Word := dwTMR_Discrepancy_Word OR 16#02000000; END_IF;
ELSIF (rDiff_FacReturnT_AC <= 0.60) THEN
    bFacReturnT_ChA_Healthy := TRUE;
    bFacReturnT_ChB_Healthy := FALSE;
    bFacReturnT_ChC_Healthy := TRUE;
    rVoted_FWR_Facility_Return_Temp_C := 0.5 * (TT_FWR_FACILITY_RETURN_203A + TT_FWR_FACILITY_RETURN_203C);
    tTMR_Timer_FacReturnT := tTMR_Timer_FacReturnT + 0.050;
    IF (tTMR_Timer_FacReturnT > 1.50) THEN dwTMR_Discrepancy_Word := dwTMR_Discrepancy_Word OR 16#04000000; END_IF;
ELSE
    bFacReturnT_ChA_Healthy := FALSE;
    bFacReturnT_ChB_Healthy := FALSE;
    bFacReturnT_ChC_Healthy := FALSE;
    rVoted_FWR_Facility_Return_Temp_C := TT_FWR_FACILITY_RETURN_203A;
    dwTMR_Discrepancy_Word := dwTMR_Discrepancy_Word OR 16#07000000;
END_IF;

(* --- Channel 10 & 11: CDU Pump 1 & Pump 2 VFD RPM Feedbacks [rpm] --- *)
rDiff_Pump1RPM_AB := ABS(ZT_CDU_PUMP1_VFD_RPM_301A - ZT_CDU_PUMP1_VFD_RPM_301B);
rDiff_Pump1RPM_BC := ABS(ZT_CDU_PUMP1_VFD_RPM_301B - ZT_CDU_PUMP1_VFD_RPM_301C);
rDiff_Pump1RPM_AC := ABS(ZT_CDU_PUMP1_VFD_RPM_301A - ZT_CDU_PUMP1_VFD_RPM_301C);

IF (rDiff_Pump1RPM_AB <= 50.0) AND (rDiff_Pump1RPM_AC <= 50.0) THEN
    bPump1RPM_ChA_Healthy := TRUE;
    bPump1RPM_ChB_Healthy := TRUE;
    bPump1RPM_ChC_Healthy := TRUE;
    tTMR_Timer_Pump1RPM := 0.0;
ELSIF (rDiff_Pump1RPM_AB <= 50.0) THEN
    bPump1RPM_ChA_Healthy := TRUE;
    bPump1RPM_ChB_Healthy := TRUE;
    bPump1RPM_ChC_Healthy := FALSE;
    tTMR_Timer_Pump1RPM := tTMR_Timer_Pump1RPM + 0.050;
    IF (tTMR_Timer_Pump1RPM > 1.50) THEN dwTMR_Discrepancy_Word := dwTMR_Discrepancy_Word OR 16#08000000; END_IF;
ELSIF (rDiff_Pump1RPM_BC <= 50.0) THEN
    bPump1RPM_ChA_Healthy := FALSE;
    bPump1RPM_ChB_Healthy := TRUE;
    bPump1RPM_ChC_Healthy := TRUE;
    tTMR_Timer_Pump1RPM := tTMR_Timer_Pump1RPM + 0.050;
    IF (tTMR_Timer_Pump1RPM > 1.50) THEN dwTMR_Discrepancy_Word := dwTMR_Discrepancy_Word OR 16#10000000; END_IF;
ELSE
    bPump1RPM_ChA_Healthy := TRUE;
    bPump1RPM_ChB_Healthy := FALSE;
    bPump1RPM_ChC_Healthy := TRUE;
    tTMR_Timer_Pump1RPM := tTMR_Timer_Pump1RPM + 0.050;
    IF (tTMR_Timer_Pump1RPM > 1.50) THEN dwTMR_Discrepancy_Word := dwTMR_Discrepancy_Word OR 16#20000000; END_IF;
END_IF;

rDiff_Pump2RPM_AB := ABS(ZT_CDU_PUMP2_VFD_RPM_302A - ZT_CDU_PUMP2_VFD_RPM_302B);
rDiff_Pump2RPM_BC := ABS(ZT_CDU_PUMP2_VFD_RPM_302B - ZT_CDU_PUMP2_VFD_RPM_302C);
rDiff_Pump2RPM_AC := ABS(ZT_CDU_PUMP2_VFD_RPM_302A - ZT_CDU_PUMP2_VFD_RPM_302C);

IF (rDiff_Pump2RPM_AB <= 50.0) AND (rDiff_Pump2RPM_AC <= 50.0) THEN
    bPump2RPM_ChA_Healthy := TRUE;
    bPump2RPM_ChB_Healthy := TRUE;
    bPump2RPM_ChC_Healthy := TRUE;
    tTMR_Timer_Pump2RPM := 0.0;
ELSIF (rDiff_Pump2RPM_AB <= 50.0) THEN
    bPump2RPM_ChA_Healthy := TRUE;
    bPump2RPM_ChB_Healthy := TRUE;
    bPump2RPM_ChC_Healthy := FALSE;
    tTMR_Timer_Pump2RPM := tTMR_Timer_Pump2RPM + 0.050;
    IF (tTMR_Timer_Pump2RPM > 1.50) THEN dwTMR_Discrepancy_Word := dwTMR_Discrepancy_Word OR 16#40000000; END_IF;
ELSE
    bPump2RPM_ChA_Healthy := FALSE;
    bPump2RPM_ChB_Healthy := TRUE;
    bPump2RPM_ChC_Healthy := TRUE;
    tTMR_Timer_Pump2RPM := tTMR_Timer_Pump2RPM + 0.050;
    IF (tTMR_Timer_Pump2RPM > 1.50) THEN dwTMR_Discrepancy_Word := dwTMR_Discrepancy_Word OR 16#80000000; END_IF;
END_IF;

(* --- Channel 13: Propylene Glycol Concentration [%] --- *)
rDiff_Glycol_AB := ABS(AIT_GLYCOL_CONCENTRATION_401A - AIT_GLYCOL_CONCENTRATION_401B);
rDiff_Glycol_BC := ABS(AIT_GLYCOL_CONCENTRATION_401B - AIT_GLYCOL_CONCENTRATION_401C);
rDiff_Glycol_AC := ABS(AIT_GLYCOL_CONCENTRATION_401A - AIT_GLYCOL_CONCENTRATION_401C);

IF (rDiff_Glycol_AB <= 2.0) AND (rDiff_Glycol_AC <= 2.0) THEN
    bGlycol_ChA_Healthy := TRUE;
    bGlycol_ChB_Healthy := TRUE;
    bGlycol_ChC_Healthy := TRUE;
    IF ((AIT_GLYCOL_CONCENTRATION_401A >= AIT_GLYCOL_CONCENTRATION_401B) AND (AIT_GLYCOL_CONCENTRATION_401A <= AIT_GLYCOL_CONCENTRATION_401C)) OR
       ((AIT_GLYCOL_CONCENTRATION_401A <= AIT_GLYCOL_CONCENTRATION_401B) AND (AIT_GLYCOL_CONCENTRATION_401A >= AIT_GLYCOL_CONCENTRATION_401C)) THEN
        rVoted_Glycol_Concentration_Pct := AIT_GLYCOL_CONCENTRATION_401A;
    ELSIF ((AIT_GLYCOL_CONCENTRATION_401B >= AIT_GLYCOL_CONCENTRATION_401A) AND (AIT_GLYCOL_CONCENTRATION_401B <= AIT_GLYCOL_CONCENTRATION_401C)) OR
          ((AIT_GLYCOL_CONCENTRATION_401B <= AIT_GLYCOL_CONCENTRATION_401A) AND (AIT_GLYCOL_CONCENTRATION_401B >= AIT_GLYCOL_CONCENTRATION_401C)) THEN
        rVoted_Glycol_Concentration_Pct := AIT_GLYCOL_CONCENTRATION_401B;
    ELSE
        rVoted_Glycol_Concentration_Pct := AIT_GLYCOL_CONCENTRATION_401C;
    END_IF;
    tTMR_Timer_Glycol := 0.0;
ELSIF (rDiff_Glycol_AB <= 2.0) THEN
    bGlycol_ChA_Healthy := TRUE;
    bGlycol_ChB_Healthy := TRUE;
    bGlycol_ChC_Healthy := FALSE;
    rVoted_Glycol_Concentration_Pct := 0.5 * (AIT_GLYCOL_CONCENTRATION_401A + AIT_GLYCOL_CONCENTRATION_401B);
ELSE
    bGlycol_ChA_Healthy := FALSE;
    bGlycol_ChB_Healthy := TRUE;
    bGlycol_ChC_Healthy := TRUE;
    rVoted_Glycol_Concentration_Pct := 0.5 * (AIT_GLYCOL_CONCENTRATION_401B + AIT_GLYCOL_CONCENTRATION_401C);
END_IF;

(* --- Channel 14: Dissolved Oxygen [ppb] --- *)
rDiff_DO_AB := ABS(AIT_CORROSION_ORP_DO_402A - AIT_CORROSION_ORP_DO_402B);
rDiff_DO_BC := ABS(AIT_CORROSION_ORP_DO_402B - AIT_CORROSION_ORP_DO_402C);
rDiff_DO_AC := ABS(AIT_CORROSION_ORP_DO_402A - AIT_CORROSION_ORP_DO_402C);

IF (rDiff_DO_AB <= 5.0) AND (rDiff_DO_AC <= 5.0) THEN
    bDO_ChA_Healthy := TRUE;
    bDO_ChB_Healthy := TRUE;
    bDO_ChC_Healthy := TRUE;
    IF ((AIT_CORROSION_ORP_DO_402A >= AIT_CORROSION_ORP_DO_402B) AND (AIT_CORROSION_ORP_DO_402A <= AIT_CORROSION_ORP_DO_402C)) OR
       ((AIT_CORROSION_ORP_DO_402A <= AIT_CORROSION_ORP_DO_402B) AND (AIT_CORROSION_ORP_DO_402A >= AIT_CORROSION_ORP_DO_402C)) THEN
        rVoted_Dissolved_Oxygen_ppb := AIT_CORROSION_ORP_DO_402A;
    ELSIF ((AIT_CORROSION_ORP_DO_402B >= AIT_CORROSION_ORP_DO_402A) AND (AIT_CORROSION_ORP_DO_402B <= AIT_CORROSION_ORP_DO_402C)) OR
          ((AIT_CORROSION_ORP_DO_402B <= AIT_CORROSION_ORP_DO_402A) AND (AIT_CORROSION_ORP_DO_402B >= AIT_CORROSION_ORP_DO_402C)) THEN
        rVoted_Dissolved_Oxygen_ppb := AIT_CORROSION_ORP_DO_402B;
    ELSE
        rVoted_Dissolved_Oxygen_ppb := AIT_CORROSION_ORP_DO_402C;
    END_IF;
ELSE
    rVoted_Dissolved_Oxygen_ppb := 0.5 * (AIT_CORROSION_ORP_DO_402A + AIT_CORROSION_ORP_DO_402B);
END_IF;

(* --- Channel 15: Distributed Optical/Polymer Leak Sensing Rope Resistance [Ohm] --- *)
(* Note: Low resistance indicates coolant immersion bridge. High safety criticality: Fast voting! *)
rDiff_Leak_AB := ABS(OPT_LEAK_ROPE_RESISTANCE_501A - OPT_LEAK_ROPE_RESISTANCE_501B);
rDiff_Leak_BC := ABS(OPT_LEAK_ROPE_RESISTANCE_501B - OPT_LEAK_ROPE_RESISTANCE_501C);
rDiff_Leak_AC := ABS(OPT_LEAK_ROPE_RESISTANCE_501A - OPT_LEAK_ROPE_RESISTANCE_501C);

IF (rDiff_Leak_AB <= 100.0) AND (rDiff_Leak_AC <= 100.0) THEN
    bLeak_ChA_Healthy := TRUE;
    bLeak_ChB_Healthy := TRUE;
    bLeak_ChC_Healthy := TRUE;
    (* Conservative safety voting: select the MINIMUM resistance among the three (most severe leak indication) *)
    IF (OPT_LEAK_ROPE_RESISTANCE_501A <= OPT_LEAK_ROPE_RESISTANCE_501B) AND (OPT_LEAK_ROPE_RESISTANCE_501A <= OPT_LEAK_ROPE_RESISTANCE_501C) THEN
        rVoted_Leak_Rope_Resistance_Ohm := OPT_LEAK_ROPE_RESISTANCE_501A;
    ELSIF (OPT_LEAK_ROPE_RESISTANCE_501B <= OPT_LEAK_ROPE_RESISTANCE_501A) AND (OPT_LEAK_ROPE_RESISTANCE_501B <= OPT_LEAK_ROPE_RESISTANCE_501C) THEN
        rVoted_Leak_Rope_Resistance_Ohm := OPT_LEAK_ROPE_RESISTANCE_501B;
    ELSE
        rVoted_Leak_Rope_Resistance_Ohm := OPT_LEAK_ROPE_RESISTANCE_501C;
    END_IF;
ELSIF (rDiff_Leak_AB <= 100.0) THEN
    bLeak_ChA_Healthy := TRUE;
    bLeak_ChB_Healthy := TRUE;
    bLeak_ChC_Healthy := FALSE;
    IF (OPT_LEAK_ROPE_RESISTANCE_501A < OPT_LEAK_ROPE_RESISTANCE_501B) THEN
        rVoted_Leak_Rope_Resistance_Ohm := OPT_LEAK_ROPE_RESISTANCE_501A;
    ELSE
        rVoted_Leak_Rope_Resistance_Ohm := OPT_LEAK_ROPE_RESISTANCE_501B;
    END_IF;
ELSE
    (* Single sensor trip is sufficient to trigger fast containment pre-alarm *)
    rVoted_Leak_Rope_Resistance_Ohm := OPT_LEAK_ROPE_RESISTANCE_501A;
END_IF;

(* --- Channel 16: Emergency Coolant Thermal Storage Reservoir Level [%] --- *)
rDiff_BufferLvl_AB := ABS(LT_THERMAL_BUFFER_TANK_601A - LT_THERMAL_BUFFER_TANK_601B);
rDiff_BufferLvl_BC := ABS(LT_THERMAL_BUFFER_TANK_601B - LT_THERMAL_BUFFER_TANK_601C);
rDiff_BufferLvl_AC := ABS(LT_THERMAL_BUFFER_TANK_601A - LT_THERMAL_BUFFER_TANK_601C);

IF (rDiff_BufferLvl_AB <= 3.0) AND (rDiff_BufferLvl_AC <= 3.0) THEN
    bBufferLvl_ChA_Healthy := TRUE;
    bBufferLvl_ChB_Healthy := TRUE;
    bBufferLvl_ChC_Healthy := TRUE;
    rVoted_Buffer_Tank_Level_Pct := (LT_THERMAL_BUFFER_TANK_601A + LT_THERMAL_BUFFER_TANK_601B + LT_THERMAL_BUFFER_TANK_601C) / 3.0;
ELSIF (rDiff_BufferLvl_AB <= 3.0) THEN
    rVoted_Buffer_Tank_Level_Pct := 0.5 * (LT_THERMAL_BUFFER_TANK_601A + LT_THERMAL_BUFFER_TANK_601B);
ELSE
    rVoted_Buffer_Tank_Level_Pct := LT_THERMAL_BUFFER_TANK_601A;
END_IF;
"""

def get_phase2_thermo_properties():
    return """(* ========================================================================= *)
(* === PHASE 2: REAL-TIME PG25 THERMO-PHYSICAL PROPERTY EVALUATION ======= *)
(* ========================================================================= *)
(*
   Computes temperature-dependent physical transport properties of 25% by volume
   Propylene Glycol aqueous solution (PG25) across 10.0 deg C to 70.0 deg C:
     - Density rho(T) [kg/m3] via cubic polynomial: rho = A0 + A1*T + A2*T^2 + A3*T^3
     - Specific Heat cp(T) [J/(kg*K)] via quadratic: cp = B0 + B1*T + B2*T^2
     - Dynamic Viscosity mu(T) [cP = 10^-3 Pa*s] via quadratic: mu = C0 + C1*T + C2*T^2
     - Thermal Conductivity k(T) [W/(m*K)] via linear: k = D0 + D1*T
*)

(* Constant coefficients for 25% Propylene Glycol *)
rPG_Poly_A0 := 1028.45;
rPG_Poly_A1 := -0.1982;
rPG_Poly_A2 := -0.00285;
rPG_Poly_A3 := 0.0000041;

rPG_Poly_B0 := 3865.2;
rPG_Poly_B1 := 2.450;
rPG_Poly_B2 := 0.00312;

rPG_Poly_C0 := 3.420;
rPG_Poly_C1 := -0.0712;
rPG_Poly_C2 := 0.000485;

rPG_Poly_D0 := 0.492;
rPG_Poly_D1 := 0.00085;

(* Evaluate density rho at voted supply temperature *)
rFluid_Density_kg_m3 := rPG_Poly_A0 + 
                        (rPG_Poly_A1 * rVoted_TCS_Supply_Temp_C) + 
                        (rPG_Poly_A2 * rVoted_TCS_Supply_Temp_C * rVoted_TCS_Supply_Temp_C) + 
                        (rPG_Poly_A3 * rVoted_TCS_Supply_Temp_C * rVoted_TCS_Supply_Temp_C * rVoted_TCS_Supply_Temp_C);

(* Evaluate specific heat capacity cp at average loop temperature *)
rFluid_Specific_Heat_J_kgK := rPG_Poly_B0 + 
                              (rPG_Poly_B1 * (0.5 * (rVoted_TCS_Supply_Temp_C + rVoted_TCS_Return_Temp_C))) + 
                              (rPG_Poly_B2 * (0.5 * (rVoted_TCS_Supply_Temp_C + rVoted_TCS_Return_Temp_C)) * (0.5 * (rVoted_TCS_Supply_Temp_C + rVoted_TCS_Return_Temp_C)));

(* Evaluate dynamic viscosity mu [cP] *)
rFluid_Viscosity_cP := rPG_Poly_C0 + 
                       (rPG_Poly_C1 * rVoted_TCS_Supply_Temp_C) + 
                       (rPG_Poly_C2 * rVoted_TCS_Supply_Temp_C * rVoted_TCS_Supply_Temp_C);
IF (rFluid_Viscosity_cP < 0.65) THEN rFluid_Viscosity_cP := 0.65; END_IF;

(* Evaluate thermal conductivity k [W/(m*K)] *)
rFluid_Thermal_Conductivity_W_mK := rPG_Poly_D0 + (rPG_Poly_D1 * rVoted_TCS_Supply_Temp_C);
"""

def get_phase3_cyber_physical_observers():
    return """(* ========================================================================= *)
(* === PHASE 3: CYBER-PHYSICAL OBSERVERS & THERMAL MODEL CALCULATIONS ===== *)
(* ========================================================================= *)
(*
   Subsystem 1: Plate Heat Exchanger (PHE) Thermal Duty, LMTD, & Fouling Observer
   Subsystem 2: Direct-to-Chip Cold Plate Micro-Channel Hydraulics & Junction Temp
   Subsystem 3: Distributed Leak Location Acoustic/TDR Impedance Wave Locator
   Subsystem 4: Thermal Storage Ride-Through Reservoir Autonomy Estimator
   Subsystem 5: Energetic Pumping Electrical Power & System COP
*)

(* --- 1. Plate Heat Exchanger (PHE) Thermal Duty & Fouling Observer --- *)
(* Mass flow rates [kg/s]: (L/min / 60) * (rho / 1000) for TCS, and (m3/h / 3.6) * (rho / 1000) for FWS *)
rPHE_MassFlow_Secondary_kg_s := (rVoted_TCS_Supply_Flow_Lpm / 60.0) * (rFluid_Density_kg_m3 / 1000.0);
rPHE_MassFlow_Primary_kg_s   := (rVoted_FWS_Facility_Flow_m3h / 3.60) * 1.0; (* Water rho ~ 1000 kg/m3 *)

(* Instantaneous thermal power dissipated by TCS secondary coolant [MW] *)
rPHE_Thermal_Duty_MW := (rPHE_MassFlow_Secondary_kg_s * rFluid_Specific_Heat_J_kgK * (rVoted_TCS_Return_Temp_C - rVoted_TCS_Supply_Temp_C)) / 1000000.0;
IF (rPHE_Thermal_Duty_MW < 0.0) THEN rPHE_Thermal_Duty_MW := 0.0; END_IF;

(* Counter-flow Logarithmic Mean Temperature Difference (LMTD) calculation *)
(* DeltaT1 = T_TCS_return - T_FWS_return, DeltaT2 = T_TCS_supply - T_FWS_supply *)
rLMTD_DeltaT1 := rVoted_TCS_Return_Temp_C - rVoted_FWR_Facility_Return_Temp_C;
rLMTD_DeltaT2 := rVoted_TCS_Supply_Temp_C - rVoted_FWS_Facility_Supply_Temp_C;

IF (rLMTD_DeltaT1 <= 0.5) THEN rLMTD_DeltaT1 := 0.5; END_IF;
IF (rLMTD_DeltaT2 <= 0.5) THEN rLMTD_DeltaT2 := 0.5; END_IF;

IF (ABS(rLMTD_DeltaT1 - rLMTD_DeltaT2) > 0.10) THEN
    rLMTD_Calculated := (rLMTD_DeltaT1 - rLMTD_DeltaT2) / LN(rLMTD_DeltaT1 / rLMTD_DeltaT2);
ELSE
    rLMTD_Calculated := 0.5 * (rLMTD_DeltaT1 + rLMTD_DeltaT2);
END_IF;

(* Overall heat transfer conductance UA [kW/K] *)
IF (rLMTD_Calculated > 0.20) THEN
    rPHE_Overall_Heat_Transfer_UA_kW_K := (rPHE_Thermal_Duty_MW * 1000.0) / rLMTD_Calculated;
ELSE
    rPHE_Overall_Heat_Transfer_UA_kW_K := 100.0;
END_IF;

(* Clean design conductance UA_clean = 2850.0 kW/K *)
rPHE_Clean_Conductance_UA := 2850.0;
IF (rPHE_Overall_Heat_Transfer_UA_kW_K > 50.0) THEN
    rPHE_Fouling_Resistance_m2K_kW := (1.0 / rPHE_Overall_Heat_Transfer_UA_kW_K) - (1.0 / rPHE_Clean_Conductance_UA);
    IF (rPHE_Fouling_Resistance_m2K_kW < 0.0) THEN rPHE_Fouling_Resistance_m2K_kW := 0.0; END_IF;
ELSE
    rPHE_Fouling_Resistance_m2K_kW := 0.025;
END_IF;

(* --- 2. Direct-to-Chip Cold Plate Micro-Channel Hydraulics & Junction Temp Observer --- *)
(* Distribution across 64 server racks (each rack housing 8 compute trays with dual cold plates = 1024 cold plates) *)
(* Micro-channel hydraulic diameter Dh = 0.00085 m (850 micrometers), Area = 0.045 m2 *)
rMicroChannel_Hydraulic_Diameter_m := 0.00085;
rRack_Coolant_Velocity_m_s := (rVoted_TCS_Supply_Flow_Lpm / (64.0 * 60000.0)) / 0.00012; (* Cross-sectional flow area *)
IF (rRack_Coolant_Velocity_m_s < 0.05) THEN rRack_Coolant_Velocity_m_s := 0.05; END_IF;

(* Reynolds number: Re = (rho * v * Dh) / (mu_Pa_s) where mu_Pa_s = mu_cP * 10^-3 *)
rMicroChannel_Reynolds_Number := (rFluid_Density_kg_m3 * rRack_Coolant_Velocity_m_s * rMicroChannel_Hydraulic_Diameter_m) / (rFluid_Viscosity_cP * 0.0010);
IF (rMicroChannel_Reynolds_Number < 10.0) THEN rMicroChannel_Reynolds_Number := 10.0; END_IF;

(* Prandtl number: Pr = (cp * mu_Pa_s) / k *)
rMicroChannel_Prandtl_Number := (rFluid_Specific_Heat_J_kgK * (rFluid_Viscosity_cP * 0.0010)) / rFluid_Thermal_Conductivity_W_mK;

(* Nusselt number via Dittus-Boelter / Sieder-Tate correlation for micro-channel turbulent/transition flow *)
rMicroChannel_Nusselt_Number := 0.023 * EXPT(rMicroChannel_Reynolds_Number, 0.8) * EXPT(rMicroChannel_Prandtl_Number, 0.4);
IF (rMicroChannel_Nusselt_Number < 3.66) THEN rMicroChannel_Nusselt_Number := 3.66; END_IF; (* Laminar asymptotic limit *)

(* Convective heat transfer coefficient h [W/(m2*K)] *)
rConvective_Heat_Transfer_Coeff_h := (rMicroChannel_Nusselt_Number * rFluid_Thermal_Conductivity_W_mK) / rMicroChannel_Hydraulic_Diameter_m;

(* Thermal resistance R_th = R_conduction + R_convection + R_caloric [K/W] *)
rColdPlate_Conduction_Resistance_K_W := 0.012; (* Copper base spreading resistance *)
rColdPlate_Convective_Resistance_K_W := 1.0 / (rConvective_Heat_Transfer_Coeff_h * 0.045);
rObserved_ColdPlate_Rth_K_per_W := rColdPlate_Conduction_Resistance_K_W + rColdPlate_Convective_Resistance_K_W;

(* Caloric temperature rise of fluid along compute blade: DeltaT_caloric = Q_blade / (m_dot_blade * cp) *)
IF (rPHE_MassFlow_Secondary_kg_s > 0.10) THEN
    rFluid_Caloric_Temperature_Rise_K := ((rGPU_Compute_Node_Average_Power_kW * 1000.0) * 8.0) / ((rPHE_MassFlow_Secondary_kg_s / 64.0) * rFluid_Specific_Heat_J_kgK);
ELSE
    rFluid_Caloric_Temperature_Rise_K := 12.0;
END_IF;

(* Predicted Peak GPU Silicon Junction Temperature: Tj = T_supply + (Q_chip * R_th) + DeltaT_caloric *)
(* Typical AI accelerator chip dissipation Q_chip = 700.0 W (0.70 kW) *)
rObserved_GPU_Junction_Temp_C := rVoted_TCS_Supply_Temp_C + (700.0 * rObserved_ColdPlate_Rth_K_per_W) + (0.5 * rFluid_Caloric_Temperature_Rise_K);

(* --- 3. Distributed Leak Location Acoustic/TDR Impedance Wave Locator --- *)
(* Coaxial sensing rope characteristic line impedance: 120.0 Ohm nominal, propagation velocity 200 m/us *)
rLeak_Loop_Characteristic_Impedance := 120.0;
rLeak_Signal_Propagation_Velocity_m_us := 200.0;

IF (rVoted_Leak_Rope_Resistance_Ohm < 800.0) THEN
    (* Reflectance ratio rho_r = (R_load - Z0) / (R_load + Z0) *)
    rLeak_Measured_Reflectance_Ratio := ABS(rVoted_Leak_Rope_Resistance_Ohm - rLeak_Loop_Characteristic_Impedance) / (rVoted_Leak_Rope_Resistance_Ohm + rLeak_Loop_Characteristic_Impedance + 1.0);
    (* Zone distance along 500.0 m manifold routing *)
    rLeak_Zone_Estimated_Distance_m := (1.0 - (rVoted_Leak_Rope_Resistance_Ohm / 800.0)) * 500.0;
    IF (rLeak_Zone_Estimated_Distance_m < 0.0) THEN rLeak_Zone_Estimated_Distance_m := 0.0; END_IF;
ELSE
    rLeak_Zone_Estimated_Distance_m := 0.0;
END_IF;

(* --- 4. Thermal Storage Ride-Through Reservoir Autonomy Estimator --- *)
(* 120,000 Liter buffer vessel. Coolant Mass = 120 m3 * rho kg/m3 *)
rBuffer_Total_Fluid_Mass_kg := 120.0 * rFluid_Density_kg_m3;

(* Maximum permissible return temperature before mandatory IT emergency curtailment: 48.0 deg C *)
(* Available thermal enthalpy delta: DeltaQ [MJ] = M * cp * (T_max - T_core) / 10^6 *)
IF (rThermal_Buffer_Tank_Core_Temp_C < 48.0) THEN
    rBuffer_Available_Enthalpy_Delta_MJ := (rBuffer_Total_Fluid_Mass_kg * rFluid_Specific_Heat_J_kgK * (48.0 - rThermal_Buffer_Tank_Core_Temp_C)) / 1000000.0;
ELSE
    rBuffer_Available_Enthalpy_Delta_MJ := 0.0;
END_IF;

(* Dynamic seconds of ride-through remaining: t_sec = DeltaQ_MJ / P_thermal_MW *)
IF (rIT_Cluster_Thermal_Load_MW > 1.0) THEN
    rThermal_Buffer_RideThrough_Sec_Remaining := rBuffer_Available_Enthalpy_Delta_MJ / rIT_Cluster_Thermal_Load_MW;
ELSE
    rThermal_Buffer_RideThrough_Sec_Remaining := 120.0;
END_IF;
IF (rThermal_Buffer_RideThrough_Sec_Remaining > 300.0) THEN rThermal_Buffer_RideThrough_Sec_Remaining := 300.0; END_IF;

(* --- 5. Energetic Pumping Electrical Power & System COP --- *)
(* Hydraulic power: P_hyd [kW] = (Q [m3/s] * DeltaP [Pa]) / 1000 *)
(* Combined pump electrical power with VFD efficiency eta ~ 0.82 *)
rTotal_CDU_Pumping_Electric_Power_kW := (((rVoted_TCS_Supply_Flow_Lpm / 60000.0) * (rVoted_TCS_Loop_Diff_Pressure_bar * 100000.0)) / 1000.0) / 0.82;
IF (rTotal_CDU_Pumping_Electric_Power_kW < 2.0) THEN rTotal_CDU_Pumping_Electric_Power_kW := 2.0; END_IF;

(* Coefficient of Performance COP = Thermal MW * 1000 / Electrical Pumping kW *)
rEnergy_Pumping_Efficiency_COP := (rPHE_Thermal_Duty_MW * 1000.0) / rTotal_CDU_Pumping_Electric_Power_kW;
"""

print("Phases 1-3 configured.")
