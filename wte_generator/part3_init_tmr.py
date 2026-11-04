# part3_init_tmr.py

def get_part3_init_tmr():
    return """(* =====================================================================================================================
 * PHASE 0: SYSTEM RESET, SAFETY PERMISSIVES SUPERVISION & FIRST-SCAN 8x8 MATRIX INITIALIZATION
 * ===================================================================================================================== *)

(* Master Safety Relay E-Stop Interlock Verification *)
IF NOT bEmergencyStop_NC THEN
    wFSM_CurrentState := 16#000B; (* Force to EMERGENCY_FEED_CUT_SMOKE_STOP *)
    iFSM_State := 11;
    rGrateSpeedCmd_Zone1_strokes_h := 0.0;
    rGrateSpeedCmd_Zone2_strokes_h := 0.0;
    rGrateSpeedCmd_Zone3_strokes_h := 0.0;
    rGrateSpeedCmd_Zone4_strokes_h := 0.0;
    rPrimaryAirDamperCmd_pct := 10.0; (* Minimum purge air *)
    rSecondaryAirDamperCmd_pct := 0.0;
    rPrimaryAirFanRPMCmd_rpm := 250.0;
    rSecondaryAirFanRPMCmd_rpm := 0.0;
    rUreaDosingPumpSpeedCmd_pct := 0.0;
    rLimeSlurryFeedPumpCmd_pct := 15.0; (* Keep absorber wet *)
    rActivatedCarbonFeederCmd_kgh := 0.0;
    rAuxiliaryBurnerFiringRate_pct := 0.0;
    bSystemReady := FALSE;
    bLegalEmissionBreachTrip := FALSE;
    dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#8000_0000; (* Bit 31: HARDWARE_EMERGENCY_STOP *)
    dwSystemStatusWord := 16#0000_000B;
    RETURN;
END_IF;

(* Master Functional Execution Disabled *)
IF NOT bEnable THEN
    wFSM_CurrentState := 16#0001; (* Cold Standby / Offline *)
    iFSM_State := 1;
    rGrateSpeedCmd_Zone1_strokes_h := 0.0;
    rGrateSpeedCmd_Zone2_strokes_h := 0.0;
    rGrateSpeedCmd_Zone3_strokes_h := 0.0;
    rGrateSpeedCmd_Zone4_strokes_h := 0.0;
    rPrimaryAirDamperCmd_pct := 0.0;
    rSecondaryAirDamperCmd_pct := 0.0;
    rPrimaryAirFanRPMCmd_rpm := 0.0;
    rSecondaryAirFanRPMCmd_rpm := 0.0;
    rUreaDosingPumpSpeedCmd_pct := 0.0;
    rLimeSlurryFeedPumpCmd_pct := 0.0;
    rActivatedCarbonFeederCmd_kgh := 0.0;
    rAuxiliaryBurnerFiringRate_pct := 0.0;
    rIDF_FanSpeedCmd_rpm := 0.0;
    bSystemReady := FALSE;
    bEU_Directive_2010_75_Compliant := FALSE;
    dwSystemStatusWord := 16#0000_0000;
    RETURN;
END_IF;

(* First-Scan State-Space and MPC Penalty Matrix Initialization *)
IF NOT bStateSpaceInitialized THEN
    (* 8x8 Discrete State-Space System Matrix A (Ts = 50 ms) *)
    (* Row 1: Bed Moisture Deficit Delta X_moist *)
    aA[1, 1] := 0.9850; aA[1, 2] := -0.0025; aA[1, 3] := 0.0000; aA[1, 4] := 0.0000; aA[1, 5] := 0.0000; aA[1, 6] := 0.0000; aA[1, 7] := 0.0000; aA[1, 8] := 0.0000;
    (* Row 2: Pyrolysis & Char Bed Temperature Delta T_bed *)
    aA[2, 1] := 0.0120; aA[2, 2] := 0.9780; aA[2, 3] := 0.0085; aA[2, 4] := 0.0000; aA[2, 5] := -0.0045; aA[2, 6] := 0.0000; aA[2, 7] := 0.0000; aA[2, 8] := 0.0000;
    (* Row 3: Primary Combustion Chamber Gas Temperature Delta T_comb *)
    aA[3, 1] := 0.0000; aA[3, 2] := 0.0340; aA[3, 3] := 0.9620; aA[3, 4] := 0.0125; aA[3, 5] := -0.0180; aA[3, 6] := 0.0000; aA[3, 7] := 0.0000; aA[3, 8] := 0.0000;
    (* Row 4: Post-Combustion 2-Second Temperature Delta T_post *)
    aA[4, 1] := 0.0000; aA[4, 2] := 0.0000; aA[4, 3] := 0.0480; aA[4, 4] := 0.9480; aA[4, 5] := -0.0120; aA[4, 6] := 0.0000; aA[4, 7] := 0.0000; aA[4, 8] := 0.0000;
    (* Row 5: Boiler Steam Evaporation Delta m_steam *)
    aA[5, 1] := 0.0000; aA[5, 2] := 0.0015; aA[5, 3] := 0.0085; aA[5, 4] := 0.0240; aA[5, 5] := 0.9820; aA[5, 6] := 0.0000; aA[5, 7] := 0.0000; aA[5, 8] := 0.0000;
    (* Row 6: First-Pass Raw Flue Gas NOx Delta C_NOx *)
    aA[6, 1] := 0.0000; aA[6, 2] := 0.0085; aA[6, 3] := 0.0350; aA[6, 4] := 0.0180; aA[6, 5] := 0.0000; aA[6, 6] := 0.9250; aA[6, 7] := 0.0000; aA[6, 8] := 0.0000;
    (* Row 7: Acid Gas Concentration Delta C_acid *)
    aA[7, 1] := 0.0012; aA[7, 2] := 0.0045; aA[7, 3] := 0.0020; aA[7, 4] := 0.0000; aA[7, 5] := 0.0000; aA[7, 6] := 0.0000; aA[7, 7] := 0.9450; aA[7, 8] := -0.0850;
    (* Row 8: Semi-Dry Absorber Neutralization Yield Delta eta_scrub *)
    aA[8, 1] := 0.0000; aA[8, 2] := 0.0000; aA[8, 3] := 0.0000; aA[8, 4] := 0.0000; aA[8, 5] := 0.0000; aA[8, 6] := 0.0000; aA[8, 7] := -0.0120; aA[8, 8] := 0.9150;

    (* 8x8 Input Coupling Matrix B *)
    (* Col 1: u_Zone1 | Col 2: u_Zone23 | Col 3: u_Zone4 | Col 4: u_PrimAir | Col 5: u_SecAir | Col 6: u_Urea | Col 7: u_Lime | Col 8: u_PAC *)
    aB[1, 1] := 0.0350; aB[1, 2] := 0.0000; aB[1, 3] := 0.0000; aB[1, 4] := 0.0015; aB[1, 5] := 0.0000; aB[1, 6] := 0.0000; aB[1, 7] := 0.0000; aB[1, 8] := 0.0000;
    aB[2, 1] := -0.0080; aB[2, 2] := 0.0450; aB[2, 3] := 0.0000; aB[2, 4] := 0.0280; aB[2, 5] := 0.0000; aB[2, 6] := 0.0000; aB[2, 7] := 0.0000; aB[2, 8] := 0.0000;
    aB[3, 1] := 0.0000; aB[3, 2] := 0.0220; aB[3, 3] := 0.0050; aB[3, 4] := 0.0420; aB[3, 5] := -0.0150; aB[3, 6] := 0.0000; aB[3, 7] := 0.0000; aB[3, 8] := 0.0000;
    aB[4, 1] := 0.0000; aB[4, 2] := 0.0000; aB[4, 3] := 0.0080; aB[4, 4] := 0.0180; aB[4, 5] := 0.0550; aB[4, 6] := 0.0000; aB[4, 7] := 0.0000; aB[4, 8] := 0.0000;
    aB[5, 1] := 0.0000; aB[5, 2] := 0.0120; aB[5, 3] := 0.0040; aB[5, 4] := 0.0320; aB[5, 5] := 0.0240; aB[5, 6] := 0.0000; aB[5, 7] := 0.0000; aB[5, 8] := 0.0000;
    aB[6, 1] := 0.0000; aB[6, 2] := 0.0180; aB[6, 3] := 0.0000; aB[6, 4] := 0.0650; aB[6, 5] := -0.0450; aB[6, 6] := -0.1450; aB[6, 7] := 0.0000; aB[6, 8] := 0.0000;
    aB[7, 1] := 0.0025; aB[7, 2] := 0.0150; aB[7, 3] := 0.0050; aB[7, 4] := 0.0080; aB[7, 5] := 0.0000; aB[7, 6] := 0.0000; aB[7, 7] := -0.1850; aB[7, 8] := -0.0250;
    aB[8, 1] := 0.0000; aB[8, 2] := 0.0000; aB[8, 3] := 0.0000; aB[8, 4] := 0.0000; aB[8, 5] := 0.0000; aB[8, 6] := 0.0000; aB[8, 7] := 0.2200; aB[8, 8] := 0.0450;

    (* 8x8 Output Matrix C (Identity Mapping) *)
    FOR iIdx_i := 1 TO 8 DO
        FOR iIdx_j := 1 TO 8 DO
            IF iIdx_i = iIdx_j THEN aC[iIdx_i, iIdx_j] := 1.0; ELSE aC[iIdx_i, iIdx_j] := 0.0; END_IF;
            aD[iIdx_i, iIdx_j] := 0.0;
        END_FOR;
    END_FOR;

    (* Model Predictive Control (MPC) Cost Penalty Diagonals *)
    aWeightQ[1] := 1.50;  (* Bed moisture error weight *)
    aWeightQ[2] := 2.20;  (* Bed pyrolysis temp weight *)
    aWeightQ[3] := 5.80;  (* Flame core temp weight *)
    aWeightQ[4] := 14.50; (* Post-combustion statutory 2-second temp weight *)
    aWeightQ[5] := 8.20;  (* Steam production stability weight *)
    aWeightQ[6] := 18.00; (* Raw NOx emission weight *)
    aWeightQ[7] := 16.50; (* Acid gas concentration weight *)
    aWeightQ[8] := 12.00; (* Absorber neutralization yield weight *)

    aWeightR[1] := 0.25;  (* Grate Zone 1 stroke effort *)
    aWeightR[2] := 0.35;  (* Grate Zone 2/3 stroke effort *)
    aWeightR[3] := 0.20;  (* Grate Zone 4 stroke effort *)
    aWeightR[4] := 0.08;  (* Primary air fan effort *)
    aWeightR[5] := 0.12;  (* Secondary air fan effort *)
    aWeightR[6] := 0.45;  (* Urea injection cost *)
    aWeightR[7] := 0.38;  (* Lime slurry reagent cost *)
    aWeightR[8] := 0.55;  (* Activated carbon cost *)

    FOR iIdx_i := 1 TO 8 DO
        aS_Weight[iIdx_i] := aWeightR[iIdx_i] * 2.5; (* Actuator slew rate penalty *)
        aP_TerminalWeight[iIdx_i] := aWeightQ[iIdx_i] * 3.0; (* Terminal horizon cost *)
    END_FOR;

    (* Hard Dynamic Actuator Limits *)
    au_min[1] := -10.0; au_max[1] := 10.0;     (* Zone 1 Stroke Speed Delta [strokes/h] *)
    au_min[2] := -12.0; au_max[2] := 12.0;     (* Zone 2/3 Stroke Speed Delta [strokes/h] *)
    au_min[3] := -8.0;  au_max[3] := 8.0;      (* Zone 4 Stroke Speed Delta [strokes/h] *)
    au_min[4] := -5000.0; au_max[4] := 5000.0; (* Primary Air Delta [Nm3/h] *)
    au_min[5] := -3500.0; au_max[5] := 3500.0; (* Secondary Air Delta [Nm3/h] *)
    au_min[6] := -50.0; au_max[6] := 50.0;     (* Urea Injection Delta [kg/h] *)
    au_min[7] := -80.0; au_max[7] := 80.0;     (* Lime Slurry Delta [kg/h] *)
    au_min[8] := -10.0; au_max[8] := 10.0;     (* PAC Feeder Delta [kg/h] *)

    adelta_u_max[1] := 0.50; (* Max stroke slew per 50 ms *)
    adelta_u_max[2] := 0.60;
    adelta_u_max[3] := 0.40;
    adelta_u_max[4] := 150.0;
    adelta_u_max[5] := 120.0;
    adelta_u_max[6] := 2.50;
    adelta_u_max[7] := 3.50;
    adelta_u_max[8] := 0.50;

    bStateSpaceInitialized := TRUE;
END_IF;

(* Master Operator Fault Reset Command *)
IF bResetFault THEN
    bTripLatch_PostComb_LO_LO := FALSE;
    bTripLatch_PostComb_HI_HI := FALSE;
    bTripLatch_StackNOx_HI_HI := FALSE;
    bTripLatch_StackNH3_HI_HI := FALSE;
    bTripLatch_StackSO2_HI_HI := FALSE;
    bTripLatch_StackHCl_HI_HI := FALSE;
    bTripLatch_Draft_HI_HI := FALSE;
    bTripLatch_Draft_LO_LO := FALSE;
    bTripLatch_Superheater_LO_LO := FALSE;
    bTripLatch_GrateJam_Zone1 := FALSE;
    bTripLatch_GrateJam_Zone2 := FALSE;
    bTripLatch_GrateJam_Zone3 := FALSE;
    bTripLatch_GrateJam_Zone4 := FALSE;
    bLegalEmissionBreachTrip := FALSE;
    rBreachAccumulator_NOx_s := 0.0;
    rBreachAccumulator_SO2_s := 0.0;
    rBreachAccumulator_HCl_s := 0.0;
    rBreachAccumulator_NH3_s := 0.0;
    rBreachAccumulator_Temp_s := 0.0;
    dwAlarmWord_Trip := 16#0000_0000;
END_IF;

(* =====================================================================================================================
 * PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING ENGINES
 * ===================================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------------------------
 * Bank 1: Flame Core Combustion Temperature TT_COMBUSTION_CHAMBER_101A/B/C [deg C]
 * --------------------------------------------------------------------------------------------------------------------- *)
rDiff_12 := ABS(TT_COMBUSTION_CHAMBER_101A - TT_COMBUSTION_CHAMBER_101B);
rDiff_23 := ABS(TT_COMBUSTION_CHAMBER_101B - TT_COMBUSTION_CHAMBER_101C);
rDiff_13 := ABS(TT_COMBUSTION_CHAMBER_101A - TT_COMBUSTION_CHAMBER_101C);
bMatch_12 := (rDiff_12 <= c_rTol_CombustionTemp_degC) AND NOT bIso_CombTemp_A AND NOT bIso_CombTemp_B;
bMatch_23 := (rDiff_23 <= c_rTol_CombustionTemp_degC) AND NOT bIso_CombTemp_B AND NOT bIso_CombTemp_C;
bMatch_13 := (rDiff_13 <= c_rTol_CombustionTemp_degC) AND NOT bIso_CombTemp_A AND NOT bIso_CombTemp_C;

IF bMatch_12 AND bMatch_23 AND bMatch_13 THEN
    rCombustionChamberTempVoted_degC := (TT_COMBUSTION_CHAMBER_101A + TT_COMBUSTION_CHAMBER_101B + TT_COMBUSTION_CHAMBER_101C) / 3.0;
    rTimer_TMR_CombTemp_s := 0.0;
ELSIF bMatch_12 THEN
    rCombustionChamberTempVoted_degC := (TT_COMBUSTION_CHAMBER_101A + TT_COMBUSTION_CHAMBER_101B) / 2.0;
    bIso_CombTemp_C := TRUE;
ELSIF bMatch_23 THEN
    rCombustionChamberTempVoted_degC := (TT_COMBUSTION_CHAMBER_101B + TT_COMBUSTION_CHAMBER_101C) / 2.0;
    bIso_CombTemp_A := TRUE;
ELSIF bMatch_13 THEN
    rCombustionChamberTempVoted_degC := (TT_COMBUSTION_CHAMBER_101A + TT_COMBUSTION_CHAMBER_101C) / 2.0;
    bIso_CombTemp_B := TRUE;
ELSE
    rTimer_TMR_CombTemp_s := rTimer_TMR_CombTemp_s + c_rTs;
    rCombustionChamberTempVoted_degC := TT_COMBUSTION_CHAMBER_101B; (* Fallback to median channel B *)
    IF rTimer_TMR_CombTemp_s >= c_rTMR_PersistencyTimeout_s THEN
        bWarnLatch_TMR_Discrepancy := TRUE;
        dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0001; (* Bit 0: CombTemp TMR Discrepancy *)
    END_IF;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * Bank 2: Post-Combustion 2-Second Residence Plane Temperature TT_POST_COMBUSTION_2SEC_102A/B/C [deg C] (15.0 °C Tol)
 * --------------------------------------------------------------------------------------------------------------------- *)
(* Stuck-Sensor Flatline Supervision *)
IF ABS(TT_POST_COMBUSTION_2SEC_102A - rPrev_PostCombTemp_A) < 0.01 THEN iStuckCount_PostComb_A := iStuckCount_PostComb_A + 1; ELSE iStuckCount_PostComb_A := 0; END_IF;
IF ABS(TT_POST_COMBUSTION_2SEC_102B - rPrev_PostCombTemp_B) < 0.01 THEN iStuckCount_PostComb_B := iStuckCount_PostComb_B + 1; ELSE iStuckCount_PostComb_B := 0; END_IF;
IF ABS(TT_POST_COMBUSTION_2SEC_102C - rPrev_PostCombTemp_C) < 0.01 THEN iStuckCount_PostComb_C := iStuckCount_PostComb_C + 1; ELSE iStuckCount_PostComb_C := 0; END_IF;
rPrev_PostCombTemp_A := TT_POST_COMBUSTION_2SEC_102A;
rPrev_PostCombTemp_B := TT_POST_COMBUSTION_2SEC_102B;
rPrev_PostCombTemp_C := TT_POST_COMBUSTION_2SEC_102C;

IF iStuckCount_PostComb_A > 60 THEN bIso_PostComb_A := TRUE; END_IF;
IF iStuckCount_PostComb_B > 60 THEN bIso_PostComb_B := TRUE; END_IF;
IF iStuckCount_PostComb_C > 60 THEN bIso_PostComb_C := TRUE; END_IF;

rDiff_12 := ABS(TT_POST_COMBUSTION_2SEC_102A - TT_POST_COMBUSTION_2SEC_102B);
rDiff_23 := ABS(TT_POST_COMBUSTION_2SEC_102B - TT_POST_COMBUSTION_2SEC_102C);
rDiff_13 := ABS(TT_POST_COMBUSTION_2SEC_102A - TT_POST_COMBUSTION_2SEC_102C);
bMatch_12 := (rDiff_12 <= c_rTol_PostCombTemp_degC) AND NOT bIso_PostComb_A AND NOT bIso_PostComb_B;
bMatch_23 := (rDiff_23 <= c_rTol_PostCombTemp_degC) AND NOT bIso_PostComb_B AND NOT bIso_PostComb_C;
bMatch_13 := (rDiff_13 <= c_rTol_PostCombTemp_degC) AND NOT bIso_PostComb_A AND NOT bIso_PostComb_C;

IF bMatch_12 AND bMatch_23 AND bMatch_13 THEN
    rPostCombustion2SecTempVoted_degC := (TT_POST_COMBUSTION_2SEC_102A + TT_POST_COMBUSTION_2SEC_102B + TT_POST_COMBUSTION_2SEC_102C) / 3.0;
    rTimer_TMR_PostCombTemp_s := 0.0;
ELSIF bMatch_12 THEN
    rPostCombustion2SecTempVoted_degC := (TT_POST_COMBUSTION_2SEC_102A + TT_POST_COMBUSTION_2SEC_102B) / 2.0;
    bIso_PostComb_C := TRUE;
ELSIF bMatch_23 THEN
    rPostCombustion2SecTempVoted_degC := (TT_POST_COMBUSTION_2SEC_102B + TT_POST_COMBUSTION_2SEC_102C) / 2.0;
    bIso_PostComb_A := TRUE;
ELSIF bMatch_13 THEN
    rPostCombustion2SecTempVoted_degC := (TT_POST_COMBUSTION_2SEC_102A + TT_POST_COMBUSTION_2SEC_102C) / 2.0;
    bIso_PostComb_B := TRUE;
ELSE
    rTimer_TMR_PostCombTemp_s := rTimer_TMR_PostCombTemp_s + c_rTs;
    rPostCombustion2SecTempVoted_degC := TT_POST_COMBUSTION_2SEC_102B;
    IF rTimer_TMR_PostCombTemp_s >= c_rTMR_PersistencyTimeout_s THEN
        bWarnLatch_TMR_Discrepancy := TRUE;
        dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0002; (* Bit 1: PostComb TMR Discrepancy *)
    END_IF;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * Bank 3: Zone 1 Solid Bed Drying Grate Stoker Stroke Speed ZT_GRATE_ZONE1_STROKE_201A/B/C [strokes/h]
 * --------------------------------------------------------------------------------------------------------------------- *)
rDiff_12 := ABS(ZT_GRATE_ZONE1_STROKE_201A - ZT_GRATE_ZONE1_STROKE_201B);
rDiff_23 := ABS(ZT_GRATE_ZONE1_STROKE_201B - ZT_GRATE_ZONE1_STROKE_201C);
rDiff_13 := ABS(ZT_GRATE_ZONE1_STROKE_201A - ZT_GRATE_ZONE1_STROKE_201C);
bMatch_12 := (rDiff_12 <= c_rTol_GrateStroke_strokes_h) AND NOT bIso_Zone1_A AND NOT bIso_Zone1_B;
bMatch_23 := (rDiff_23 <= c_rTol_GrateStroke_strokes_h) AND NOT bIso_Zone1_B AND NOT bIso_Zone1_C;
bMatch_13 := (rDiff_13 <= c_rTol_GrateStroke_strokes_h) AND NOT bIso_Zone1_A AND NOT bIso_Zone1_C;

IF bMatch_12 AND bMatch_23 AND bMatch_13 THEN
    rMathTemp_A := (ZT_GRATE_ZONE1_STROKE_201A + ZT_GRATE_ZONE1_STROKE_201B + ZT_GRATE_ZONE1_STROKE_201C) / 3.0;
    rTimer_TMR_Zone1Stroke_s := 0.0;
ELSIF bMatch_12 THEN
    rMathTemp_A := (ZT_GRATE_ZONE1_STROKE_201A + ZT_GRATE_ZONE1_STROKE_201B) / 2.0;
    bIso_Zone1_C := TRUE;
ELSIF bMatch_23 THEN
    rMathTemp_A := (ZT_GRATE_ZONE1_STROKE_201B + ZT_GRATE_ZONE1_STROKE_201C) / 2.0;
    bIso_Zone1_A := TRUE;
ELSIF bMatch_13 THEN
    rMathTemp_A := (ZT_GRATE_ZONE1_STROKE_201A + ZT_GRATE_ZONE1_STROKE_201C) / 2.0;
    bIso_Zone1_B := TRUE;
ELSE
    rTimer_TMR_Zone1Stroke_s := rTimer_TMR_Zone1Stroke_s + c_rTs;
    rMathTemp_A := ZT_GRATE_ZONE1_STROKE_201B;
    IF rTimer_TMR_Zone1Stroke_s >= c_rTMR_PersistencyTimeout_s THEN
        dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0004; (* Bit 2: Zone 1 Stroke Discrepancy *)
    END_IF;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * Bank 4: Zone 4 Char Burnout Grate Stoker Stroke Speed ZT_GRATE_ZONE4_STROKE_204A/B/C [strokes/h]
 * --------------------------------------------------------------------------------------------------------------------- *)
rDiff_12 := ABS(ZT_GRATE_ZONE4_STROKE_204A - ZT_GRATE_ZONE4_STROKE_204B);
rDiff_23 := ABS(ZT_GRATE_ZONE4_STROKE_204B - ZT_GRATE_ZONE4_STROKE_204C);
rDiff_13 := ABS(ZT_GRATE_ZONE4_STROKE_204A - ZT_GRATE_ZONE4_STROKE_204C);
bMatch_12 := (rDiff_12 <= c_rTol_GrateStroke_strokes_h) AND NOT bIso_Zone4_A AND NOT bIso_Zone4_B;
bMatch_23 := (rDiff_23 <= c_rTol_GrateStroke_strokes_h) AND NOT bIso_Zone4_B AND NOT bIso_Zone4_C;
bMatch_13 := (rDiff_13 <= c_rTol_GrateStroke_strokes_h) AND NOT bIso_Zone4_A AND NOT bIso_Zone4_C;

IF bMatch_12 AND bMatch_23 AND bMatch_13 THEN
    rMathTemp_B := (ZT_GRATE_ZONE4_STROKE_204A + ZT_GRATE_ZONE4_STROKE_204B + ZT_GRATE_ZONE4_STROKE_204C) / 3.0;
    rTimer_TMR_Zone4Stroke_s := 0.0;
ELSIF bMatch_12 THEN
    rMathTemp_B := (ZT_GRATE_ZONE4_STROKE_204A + ZT_GRATE_ZONE4_STROKE_204B) / 2.0;
    bIso_Zone4_C := TRUE;
ELSIF bMatch_23 THEN
    rMathTemp_B := (ZT_GRATE_ZONE4_STROKE_204B + ZT_GRATE_ZONE4_STROKE_204C) / 2.0;
    bIso_Zone4_A := TRUE;
ELSIF bMatch_13 THEN
    rMathTemp_B := (ZT_GRATE_ZONE4_STROKE_204A + ZT_GRATE_ZONE4_STROKE_204C) / 2.0;
    bIso_Zone4_B := TRUE;
ELSE
    rTimer_TMR_Zone4Stroke_s := rTimer_TMR_Zone4Stroke_s + c_rTs;
    rMathTemp_B := ZT_GRATE_ZONE4_STROKE_204B;
    IF rTimer_TMR_Zone4Stroke_s >= c_rTMR_PersistencyTimeout_s THEN
        dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0008; (* Bit 3: Zone 4 Stroke Discrepancy *)
    END_IF;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * Bank 5: Primary Underfire Air Flow FT_PRIMARY_AIR_FLOW_301A/B/C [Nm3/h]
 * --------------------------------------------------------------------------------------------------------------------- *)
rDiff_12 := ABS(FT_PRIMARY_AIR_FLOW_301A - FT_PRIMARY_AIR_FLOW_301B);
rDiff_23 := ABS(FT_PRIMARY_AIR_FLOW_301B - FT_PRIMARY_AIR_FLOW_301C);
rDiff_13 := ABS(FT_PRIMARY_AIR_FLOW_301A - FT_PRIMARY_AIR_FLOW_301C);
bMatch_12 := (rDiff_12 <= c_rTol_PrimaryAir_Nm3h) AND NOT bIso_PrimAir_A AND NOT bIso_PrimAir_B;
bMatch_23 := (rDiff_23 <= c_rTol_PrimaryAir_Nm3h) AND NOT bIso_PrimAir_B AND NOT bIso_PrimAir_C;
bMatch_13 := (rDiff_13 <= c_rTol_PrimaryAir_Nm3h) AND NOT bIso_PrimAir_A AND NOT bIso_PrimAir_C;

IF bMatch_12 AND bMatch_23 AND bMatch_13 THEN
    rPrimaryAirFlowVoted_Nm3h := (FT_PRIMARY_AIR_FLOW_301A + FT_PRIMARY_AIR_FLOW_301B + FT_PRIMARY_AIR_FLOW_301C) / 3.0;
    rTimer_TMR_PrimAir_s := 0.0;
ELSIF bMatch_12 THEN
    rPrimaryAirFlowVoted_Nm3h := (FT_PRIMARY_AIR_FLOW_301A + FT_PRIMARY_AIR_FLOW_301B) / 2.0;
    bIso_PrimAir_C := TRUE;
ELSIF bMatch_23 THEN
    rPrimaryAirFlowVoted_Nm3h := (FT_PRIMARY_AIR_FLOW_301B + FT_PRIMARY_AIR_FLOW_301C) / 2.0;
    bIso_PrimAir_A := TRUE;
ELSIF bMatch_13 THEN
    rPrimaryAirFlowVoted_Nm3h := (FT_PRIMARY_AIR_FLOW_301A + FT_PRIMARY_AIR_FLOW_301C) / 2.0;
    bIso_PrimAir_B := TRUE;
ELSE
    rTimer_TMR_PrimAir_s := rTimer_TMR_PrimAir_s + c_rTs;
    rPrimaryAirFlowVoted_Nm3h := FT_PRIMARY_AIR_FLOW_301B;
    IF rTimer_TMR_PrimAir_s >= c_rTMR_PersistencyTimeout_s THEN
        dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0010; (* Bit 4: PrimAir Discrepancy *)
    END_IF;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * Bank 6: Secondary Overfire Air Flow FT_SECONDARY_AIR_FLOW_302A/B/C [Nm3/h]
 * --------------------------------------------------------------------------------------------------------------------- *)
rDiff_12 := ABS(FT_SECONDARY_AIR_FLOW_302A - FT_SECONDARY_AIR_FLOW_302B);
rDiff_23 := ABS(FT_SECONDARY_AIR_FLOW_302B - FT_SECONDARY_AIR_FLOW_302C);
rDiff_13 := ABS(FT_SECONDARY_AIR_FLOW_302A - FT_SECONDARY_AIR_FLOW_302C);
bMatch_12 := (rDiff_12 <= c_rTol_SecondaryAir_Nm3h) AND NOT bIso_SecAir_A AND NOT bIso_SecAir_B;
bMatch_23 := (rDiff_23 <= c_rTol_SecondaryAir_Nm3h) AND NOT bIso_SecAir_B AND NOT bIso_SecAir_C;
bMatch_13 := (rDiff_13 <= c_rTol_SecondaryAir_Nm3h) AND NOT bIso_SecAir_A AND NOT bIso_SecAir_C;

IF bMatch_12 AND bMatch_23 AND bMatch_13 THEN
    rSecondaryAirFlowVoted_Nm3h := (FT_SECONDARY_AIR_FLOW_302A + FT_SECONDARY_AIR_FLOW_302B + FT_SECONDARY_AIR_FLOW_302C) / 3.0;
    rTimer_TMR_SecAir_s := 0.0;
ELSIF bMatch_12 THEN
    rSecondaryAirFlowVoted_Nm3h := (FT_SECONDARY_AIR_FLOW_302A + FT_SECONDARY_AIR_FLOW_302B) / 2.0;
    bIso_SecAir_C := TRUE;
ELSIF bMatch_23 THEN
    rSecondaryAirFlowVoted_Nm3h := (FT_SECONDARY_AIR_FLOW_302B + FT_SECONDARY_AIR_FLOW_302C) / 2.0;
    bIso_SecAir_A := TRUE;
ELSIF bMatch_13 THEN
    rSecondaryAirFlowVoted_Nm3h := (FT_SECONDARY_AIR_FLOW_302A + FT_SECONDARY_AIR_FLOW_302C) / 2.0;
    bIso_SecAir_B := TRUE;
ELSE
    rTimer_TMR_SecAir_s := rTimer_TMR_SecAir_s + c_rTs;
    rSecondaryAirFlowVoted_Nm3h := FT_SECONDARY_AIR_FLOW_302B;
    IF rTimer_TMR_SecAir_s >= c_rTMR_PersistencyTimeout_s THEN
        dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0020; (* Bit 5: SecAir Discrepancy *)
    END_IF;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * Bank 7: Boiler Raw Flue Gas NOx Inlet AIT_FLUEGAS_NOX_INLET_401A/B/C [mg/Nm3]
 * --------------------------------------------------------------------------------------------------------------------- *)
rDiff_12 := ABS(AIT_FLUEGAS_NOX_INLET_401A - AIT_FLUEGAS_NOX_INLET_401B);
rDiff_23 := ABS(AIT_FLUEGAS_NOX_INLET_401B - AIT_FLUEGAS_NOX_INLET_401C);
rDiff_13 := ABS(AIT_FLUEGAS_NOX_INLET_401A - AIT_FLUEGAS_NOX_INLET_401C);
bMatch_12 := (rDiff_12 <= c_rTol_NOx_mgNm3) AND NOT bIso_RawNOx_A AND NOT bIso_RawNOx_B;
bMatch_23 := (rDiff_23 <= c_rTol_NOx_mgNm3) AND NOT bIso_RawNOx_B AND NOT bIso_RawNOx_C;
bMatch_13 := (rDiff_13 <= c_rTol_NOx_mgNm3) AND NOT bIso_RawNOx_A AND NOT bIso_RawNOx_C;

IF bMatch_12 AND bMatch_23 AND bMatch_13 THEN
    rMathTemp_C := (AIT_FLUEGAS_NOX_INLET_401A + AIT_FLUEGAS_NOX_INLET_401B + AIT_FLUEGAS_NOX_INLET_401C) / 3.0;
    rTimer_TMR_RawNOx_s := 0.0;
ELSIF bMatch_12 THEN
    rMathTemp_C := (AIT_FLUEGAS_NOX_INLET_401A + AIT_FLUEGAS_NOX_INLET_401B) / 2.0;
    bIso_RawNOx_C := TRUE;
ELSIF bMatch_23 THEN
    rMathTemp_C := (AIT_FLUEGAS_NOX_INLET_401B + AIT_FLUEGAS_NOX_INLET_401C) / 2.0;
    bIso_RawNOx_A := TRUE;
ELSIF bMatch_13 THEN
    rMathTemp_C := (AIT_FLUEGAS_NOX_INLET_401A + AIT_FLUEGAS_NOX_INLET_401C) / 2.0;
    bIso_RawNOx_B := TRUE;
ELSE
    rTimer_TMR_RawNOx_s := rTimer_TMR_RawNOx_s + c_rTs;
    rMathTemp_C := AIT_FLUEGAS_NOX_INLET_401B;
    IF rTimer_TMR_RawNOx_s >= c_rTMR_PersistencyTimeout_s THEN
        dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0040; (* Bit 6: Raw NOx Discrepancy *)
    END_IF;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * Bank 8: CEMS Clean Gas Stack NOx Outlet AIT_STACK_NOX_OUTLET_402A/B/C [mg/Nm3] (3.0 mg/Nm3 Discrepancy Tol)
 * --------------------------------------------------------------------------------------------------------------------- *)
(* Stuck-Sensor Flatline Check *)
IF ABS(AIT_STACK_NOX_OUTLET_402A - rPrev_StackNOx_A) < 0.005 THEN iStuckCount_StackNOx_A := iStuckCount_StackNOx_A + 1; ELSE iStuckCount_StackNOx_A := 0; END_IF;
IF ABS(AIT_STACK_NOX_OUTLET_402B - rPrev_StackNOx_B) < 0.005 THEN iStuckCount_StackNOx_B := iStuckCount_StackNOx_B + 1; ELSE iStuckCount_StackNOx_B := 0; END_IF;
IF ABS(AIT_STACK_NOX_OUTLET_402C - rPrev_StackNOx_C) < 0.005 THEN iStuckCount_StackNOx_C := iStuckCount_StackNOx_C + 1; ELSE iStuckCount_StackNOx_C := 0; END_IF;
rPrev_StackNOx_A := AIT_STACK_NOX_OUTLET_402A;
rPrev_StackNOx_B := AIT_STACK_NOX_OUTLET_402B;
rPrev_StackNOx_C := AIT_STACK_NOX_OUTLET_402C;

IF iStuckCount_StackNOx_A > 60 THEN bIso_StackNOx_A := TRUE; END_IF;
IF iStuckCount_StackNOx_B > 60 THEN bIso_StackNOx_B := TRUE; END_IF;
IF iStuckCount_StackNOx_C > 60 THEN bIso_StackNOx_C := TRUE; END_IF;

rDiff_12 := ABS(AIT_STACK_NOX_OUTLET_402A - AIT_STACK_NOX_OUTLET_402B);
rDiff_23 := ABS(AIT_STACK_NOX_OUTLET_402B - AIT_STACK_NOX_OUTLET_402C);
rDiff_13 := ABS(AIT_STACK_NOX_OUTLET_402A - AIT_STACK_NOX_OUTLET_402C);
bMatch_12 := (rDiff_12 <= c_rTol_StackNOx_mgNm3) AND NOT bIso_StackNOx_A AND NOT bIso_StackNOx_B;
bMatch_23 := (rDiff_23 <= c_rTol_StackNOx_mgNm3) AND NOT bIso_StackNOx_B AND NOT bIso_StackNOx_C;
bMatch_13 := (rDiff_13 <= c_rTol_StackNOx_mgNm3) AND NOT bIso_StackNOx_A AND NOT bIso_StackNOx_C;

IF bMatch_12 AND bMatch_23 AND bMatch_13 THEN
    rStackNOxVoted_mgNm3 := (AIT_STACK_NOX_OUTLET_402A + AIT_STACK_NOX_OUTLET_402B + AIT_STACK_NOX_OUTLET_402C) / 3.0;
    rTimer_TMR_StackNOx_s := 0.0;
ELSIF bMatch_12 THEN
    rStackNOxVoted_mgNm3 := (AIT_STACK_NOX_OUTLET_402A + AIT_STACK_NOX_OUTLET_402B) / 2.0;
    bIso_StackNOx_C := TRUE;
ELSIF bMatch_23 THEN
    rStackNOxVoted_mgNm3 := (AIT_STACK_NOX_OUTLET_402B + AIT_STACK_NOX_OUTLET_402C) / 2.0;
    bIso_StackNOx_A := TRUE;
ELSIF bMatch_13 THEN
    rStackNOxVoted_mgNm3 := (AIT_STACK_NOX_OUTLET_402A + AIT_STACK_NOX_OUTLET_402C) / 2.0;
    bIso_StackNOx_B := TRUE;
ELSE
    rTimer_TMR_StackNOx_s := rTimer_TMR_StackNOx_s + c_rTs;
    rStackNOxVoted_mgNm3 := AIT_STACK_NOX_OUTLET_402B;
    IF rTimer_TMR_StackNOx_s >= c_rTMR_PersistencyTimeout_s THEN
        bWarnLatch_TMR_Discrepancy := TRUE;
        dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0080; (* Bit 7: Stack NOx Discrepancy *)
    END_IF;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * Bank 9: TDLAS Stack Unreacted Ammonia Slip AIT_STACK_NH3_SLIP_403A/B/C [mg/Nm3]
 * --------------------------------------------------------------------------------------------------------------------- *)
rDiff_12 := ABS(AIT_STACK_NH3_SLIP_403A - AIT_STACK_NH3_SLIP_403B);
rDiff_23 := ABS(AIT_STACK_NH3_SLIP_403B - AIT_STACK_NH3_SLIP_403C);
rDiff_13 := ABS(AIT_STACK_NH3_SLIP_403A - AIT_STACK_NH3_SLIP_403C);
bMatch_12 := (rDiff_12 <= c_rTol_StackNH3_mgNm3) AND NOT bIso_StackNH3_A AND NOT bIso_StackNH3_B;
bMatch_23 := (rDiff_23 <= c_rTol_StackNH3_mgNm3) AND NOT bIso_StackNH3_B AND NOT bIso_StackNH3_C;
bMatch_13 := (rDiff_13 <= c_rTol_StackNH3_mgNm3) AND NOT bIso_StackNH3_A AND NOT bIso_StackNH3_C;

IF bMatch_12 AND bMatch_23 AND bMatch_13 THEN
    rStackNH3SlipVoted_mgNm3 := (AIT_STACK_NH3_SLIP_403A + AIT_STACK_NH3_SLIP_403B + AIT_STACK_NH3_SLIP_403C) / 3.0;
    rTimer_TMR_StackNH3_s := 0.0;
ELSIF bMatch_12 THEN
    rStackNH3SlipVoted_mgNm3 := (AIT_STACK_NH3_SLIP_403A + AIT_STACK_NH3_SLIP_403B) / 2.0;
    bIso_StackNH3_C := TRUE;
ELSIF bMatch_23 THEN
    rStackNH3SlipVoted_mgNm3 := (AIT_STACK_NH3_SLIP_403B + AIT_STACK_NH3_SLIP_403C) / 2.0;
    bIso_StackNH3_A := TRUE;
ELSIF bMatch_13 THEN
    rStackNH3SlipVoted_mgNm3 := (AIT_STACK_NH3_SLIP_403A + AIT_STACK_NH3_SLIP_403C) / 2.0;
    bIso_StackNH3_B := TRUE;
ELSE
    rTimer_TMR_StackNH3_s := rTimer_TMR_StackNH3_s + c_rTs;
    rStackNH3SlipVoted_mgNm3 := AIT_STACK_NH3_SLIP_403B;
    IF rTimer_TMR_StackNH3_s >= c_rTMR_PersistencyTimeout_s THEN
        dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0100; (* Bit 8: NH3 Slip Discrepancy *)
    END_IF;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * Bank 10: SNCR Aqueous Urea Injection Delivery Flow FT_UREA_INJECTION_501A/B/C [kg/h]
 * --------------------------------------------------------------------------------------------------------------------- *)
rDiff_12 := ABS(FT_UREA_INJECTION_501A - FT_UREA_INJECTION_501B);
rDiff_23 := ABS(FT_UREA_INJECTION_501B - FT_UREA_INJECTION_501C);
rDiff_13 := ABS(FT_UREA_INJECTION_501A - FT_UREA_INJECTION_501C);
bMatch_12 := (rDiff_12 <= c_rTol_UreaFlow_kgh) AND NOT bIso_UreaFlow_A AND NOT bIso_UreaFlow_B;
bMatch_23 := (rDiff_23 <= c_rTol_UreaFlow_kgh) AND NOT bIso_UreaFlow_B AND NOT bIso_UreaFlow_C;
bMatch_13 := (rDiff_13 <= c_rTol_UreaFlow_kgh) AND NOT bIso_UreaFlow_A AND NOT bIso_UreaFlow_C;

IF bMatch_12 AND bMatch_23 AND bMatch_13 THEN
    rMathTemp_A := (FT_UREA_INJECTION_501A + FT_UREA_INJECTION_501B + FT_UREA_INJECTION_501C) / 3.0;
    rTimer_TMR_UreaFlow_s := 0.0;
ELSIF bMatch_12 THEN
    rMathTemp_A := (FT_UREA_INJECTION_501A + FT_UREA_INJECTION_501B) / 2.0;
    bIso_UreaFlow_C := TRUE;
ELSIF bMatch_23 THEN
    rMathTemp_A := (FT_UREA_INJECTION_501B + FT_UREA_INJECTION_501C) / 2.0;
    bIso_UreaFlow_A := TRUE;
ELSIF bMatch_13 THEN
    rMathTemp_A := (FT_UREA_INJECTION_501A + FT_UREA_INJECTION_501C) / 2.0;
    bIso_UreaFlow_B := TRUE;
ELSE
    rTimer_TMR_UreaFlow_s := rTimer_TMR_UreaFlow_s + c_rTs;
    rMathTemp_A := FT_UREA_INJECTION_501B;
    IF rTimer_TMR_UreaFlow_s >= c_rTMR_PersistencyTimeout_s THEN
        dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0200; (* Bit 9: Urea Flow Discrepancy *)
    END_IF;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * Bank 11: Absorber Inlet Raw HCl Concentration AIT_FLUEGAS_HCL_601A/B/C [mg/Nm3]
 * --------------------------------------------------------------------------------------------------------------------- *)
rDiff_12 := ABS(AIT_FLUEGAS_HCL_601A - AIT_FLUEGAS_HCL_601B);
rDiff_23 := ABS(AIT_FLUEGAS_HCL_601B - AIT_FLUEGAS_HCL_601C);
rDiff_13 := ABS(AIT_FLUEGAS_HCL_601A - AIT_FLUEGAS_HCL_601C);
bMatch_12 := (rDiff_12 <= c_rTol_AbsorberHCl_mgNm3) AND NOT bIso_RawHCl_A AND NOT bIso_RawHCl_B;
bMatch_23 := (rDiff_23 <= c_rTol_AbsorberHCl_mgNm3) AND NOT bIso_RawHCl_B AND NOT bIso_RawHCl_C;
bMatch_13 := (rDiff_13 <= c_rTol_AbsorberHCl_mgNm3) AND NOT bIso_RawHCl_A AND NOT bIso_RawHCl_C;

IF bMatch_12 AND bMatch_23 AND bMatch_13 THEN
    rFlueGasHClVoted_mgNm3 := (AIT_FLUEGAS_HCL_601A + AIT_FLUEGAS_HCL_601B + AIT_FLUEGAS_HCL_601C) / 3.0;
    rTimer_TMR_RawHCl_s := 0.0;
ELSIF bMatch_12 THEN
    rFlueGasHClVoted_mgNm3 := (AIT_FLUEGAS_HCL_601A + AIT_FLUEGAS_HCL_601B) / 2.0;
    bIso_RawHCl_C := TRUE;
ELSIF bMatch_23 THEN
    rFlueGasHClVoted_mgNm3 := (AIT_FLUEGAS_HCL_601B + AIT_FLUEGAS_HCL_601C) / 2.0;
    bIso_RawHCl_A := TRUE;
ELSIF bMatch_13 THEN
    rFlueGasHClVoted_mgNm3 := (AIT_FLUEGAS_HCL_601A + AIT_FLUEGAS_HCL_601C) / 2.0;
    bIso_RawHCl_B := TRUE;
ELSE
    rTimer_TMR_RawHCl_s := rTimer_TMR_RawHCl_s + c_rTs;
    rFlueGasHClVoted_mgNm3 := AIT_FLUEGAS_HCL_601B;
    IF rTimer_TMR_RawHCl_s >= c_rTMR_PersistencyTimeout_s THEN
        dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0400; (* Bit 10: Raw HCl Discrepancy *)
    END_IF;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * Bank 12: Absorber Inlet Raw SO2 Concentration AIT_FLUEGAS_SO2_602A/B/C [mg/Nm3] (3.0 mg/Nm3 Discrepancy Tol)
 * --------------------------------------------------------------------------------------------------------------------- *)
rDiff_12 := ABS(AIT_FLUEGAS_SO2_602A - AIT_FLUEGAS_SO2_602B);
rDiff_23 := ABS(AIT_FLUEGAS_SO2_602B - AIT_FLUEGAS_SO2_602C);
rDiff_13 := ABS(AIT_FLUEGAS_SO2_602A - AIT_FLUEGAS_SO2_602C);
bMatch_12 := (rDiff_12 <= c_rTol_AbsorberSO2_mgNm3) AND NOT bIso_RawSO2_A AND NOT bIso_RawSO2_B;
bMatch_23 := (rDiff_23 <= c_rTol_AbsorberSO2_mgNm3) AND NOT bIso_RawSO2_B AND NOT bIso_RawSO2_C;
bMatch_13 := (rDiff_13 <= c_rTol_AbsorberSO2_mgNm3) AND NOT bIso_RawSO2_A AND NOT bIso_RawSO2_C;

IF bMatch_12 AND bMatch_23 AND bMatch_13 THEN
    rStackSO2Voted_mgNm3 := (AIT_FLUEGAS_SO2_602A + AIT_FLUEGAS_SO2_602B + AIT_FLUEGAS_SO2_602C) / 3.0;
    rTimer_TMR_RawSO2_s := 0.0;
ELSIF bMatch_12 THEN
    rStackSO2Voted_mgNm3 := (AIT_FLUEGAS_SO2_602A + AIT_FLUEGAS_SO2_602B) / 2.0;
    bIso_RawSO2_C := TRUE;
ELSIF bMatch_23 THEN
    rStackSO2Voted_mgNm3 := (AIT_FLUEGAS_SO2_602B + AIT_FLUEGAS_SO2_602C) / 2.0;
    bIso_RawSO2_A := TRUE;
ELSIF bMatch_13 THEN
    rStackSO2Voted_mgNm3 := (AIT_FLUEGAS_SO2_602A + AIT_FLUEGAS_SO2_602C) / 2.0;
    bIso_RawSO2_B := TRUE;
ELSE
    rTimer_TMR_RawSO2_s := rTimer_TMR_RawSO2_s + c_rTs;
    rStackSO2Voted_mgNm3 := AIT_FLUEGAS_SO2_602B;
    IF rTimer_TMR_RawSO2_s >= c_rTMR_PersistencyTimeout_s THEN
        bWarnLatch_TMR_Discrepancy := TRUE;
        dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0800; (* Bit 11: Raw SO2 Discrepancy *)
    END_IF;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * Bank 13: Rotary Atomizer Slaked Lime Slurry Feed FT_LIME_SLURRY_FEED_701A/B/C [kg/h]
 * --------------------------------------------------------------------------------------------------------------------- *)
rDiff_12 := ABS(FT_LIME_SLURRY_FEED_701A - FT_LIME_SLURRY_FEED_701B);
rDiff_23 := ABS(FT_LIME_SLURRY_FEED_701B - FT_LIME_SLURRY_FEED_701C);
rDiff_13 := ABS(FT_LIME_SLURRY_FEED_701A - FT_LIME_SLURRY_FEED_701C);
bMatch_12 := (rDiff_12 <= c_rTol_LimeSlurryFlow_kgh) AND NOT bIso_LimeFlow_A AND NOT bIso_LimeFlow_B;
bMatch_23 := (rDiff_23 <= c_rTol_LimeSlurryFlow_kgh) AND NOT bIso_LimeFlow_B AND NOT bIso_LimeFlow_C;
bMatch_13 := (rDiff_13 <= c_rTol_LimeSlurryFlow_kgh) AND NOT bIso_LimeFlow_A AND NOT bIso_LimeFlow_C;

IF bMatch_12 AND bMatch_23 AND bMatch_13 THEN
    rMathTemp_A := (FT_LIME_SLURRY_FEED_701A + FT_LIME_SLURRY_FEED_701B + FT_LIME_SLURRY_FEED_701C) / 3.0;
    rTimer_TMR_LimeFlow_s := 0.0;
ELSIF bMatch_12 THEN
    rMathTemp_A := (FT_LIME_SLURRY_FEED_701A + FT_LIME_SLURRY_FEED_701B) / 2.0;
    bIso_LimeFlow_C := TRUE;
ELSIF bMatch_23 THEN
    rMathTemp_A := (FT_LIME_SLURRY_FEED_701B + FT_LIME_SLURRY_FEED_701C) / 2.0;
    bIso_LimeFlow_A := TRUE;
ELSIF bMatch_13 THEN
    rMathTemp_A := (FT_LIME_SLURRY_FEED_701A + FT_LIME_SLURRY_FEED_701C) / 2.0;
    bIso_LimeFlow_B := TRUE;
ELSE
    rTimer_TMR_LimeFlow_s := rTimer_TMR_LimeFlow_s + c_rTs;
    rMathTemp_A := FT_LIME_SLURRY_FEED_701B;
    IF rTimer_TMR_LimeFlow_s >= c_rTMR_PersistencyTimeout_s THEN
        dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_1000; (* Bit 12: Lime Slurry Discrepancy *)
    END_IF;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * Bank 14: Powdered Activated Carbon (PAC) Dosing Flow FT_ACTIVATED_CARBON_702A/B/C [kg/h]
 * --------------------------------------------------------------------------------------------------------------------- *)
rDiff_12 := ABS(FT_ACTIVATED_CARBON_702A - FT_ACTIVATED_CARBON_702B);
rDiff_23 := ABS(FT_ACTIVATED_CARBON_702B - FT_ACTIVATED_CARBON_702C);
rDiff_13 := ABS(FT_ACTIVATED_CARBON_702A - FT_ACTIVATED_CARBON_702C);
bMatch_12 := (rDiff_12 <= c_rTol_PACFlow_kgh) AND NOT bIso_PACFlow_A AND NOT bIso_PACFlow_B;
bMatch_23 := (rDiff_23 <= c_rTol_PACFlow_kgh) AND NOT bIso_PACFlow_B AND NOT bIso_PACFlow_C;
bMatch_13 := (rDiff_13 <= c_rTol_PACFlow_kgh) AND NOT bIso_PACFlow_A AND NOT bIso_PACFlow_C;

IF bMatch_12 AND bMatch_23 AND bMatch_13 THEN
    rMathTemp_B := (FT_ACTIVATED_CARBON_702A + FT_ACTIVATED_CARBON_702B + FT_ACTIVATED_CARBON_702C) / 3.0;
    rTimer_TMR_PACFlow_s := 0.0;
ELSIF bMatch_12 THEN
    rMathTemp_B := (FT_ACTIVATED_CARBON_702A + FT_ACTIVATED_CARBON_702B) / 2.0;
    bIso_PACFlow_C := TRUE;
ELSIF bMatch_23 THEN
    rMathTemp_B := (FT_ACTIVATED_CARBON_702B + FT_ACTIVATED_CARBON_702C) / 2.0;
    bIso_PACFlow_A := TRUE;
ELSIF bMatch_13 THEN
    rMathTemp_B := (FT_ACTIVATED_CARBON_702A + FT_ACTIVATED_CARBON_702C) / 2.0;
    bIso_PACFlow_B := TRUE;
ELSE
    rTimer_TMR_PACFlow_s := rTimer_TMR_PACFlow_s + c_rTs;
    rMathTemp_B := FT_ACTIVATED_CARBON_702B;
    IF rTimer_TMR_PACFlow_s >= c_rTMR_PersistencyTimeout_s THEN
        dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_2000; (* Bit 13: PAC Flow Discrepancy *)
    END_IF;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * Bank 15: Convection Superheater Tube Acoustic Thickness ACOU_SUPERHEATER_CORROSION_801A/B/C [mm]
 * --------------------------------------------------------------------------------------------------------------------- *)
rDiff_12 := ABS(ACOU_SUPERHEATER_CORROSION_801A - ACOU_SUPERHEATER_CORROSION_801B);
rDiff_23 := ABS(ACOU_SUPERHEATER_CORROSION_801B - ACOU_SUPERHEATER_CORROSION_801C);
rDiff_13 := ABS(ACOU_SUPERHEATER_CORROSION_801A - ACOU_SUPERHEATER_CORROSION_801C);
bMatch_12 := (rDiff_12 <= c_rTol_SuperheaterAcoustic_mm) AND NOT bIso_Superheater_A AND NOT bIso_Superheater_B;
bMatch_23 := (rDiff_23 <= c_rTol_SuperheaterAcoustic_mm) AND NOT bIso_Superheater_B AND NOT bIso_Superheater_C;
bMatch_13 := (rDiff_13 <= c_rTol_SuperheaterAcoustic_mm) AND NOT bIso_Superheater_A AND NOT bIso_Superheater_C;

IF bMatch_12 AND bMatch_23 AND bMatch_13 THEN
    rSuperheaterThicknessVoted_mm := (ACOU_SUPERHEATER_CORROSION_801A + ACOU_SUPERHEATER_CORROSION_801B + ACOU_SUPERHEATER_CORROSION_801C) / 3.0;
    rTimer_TMR_Superheater_s := 0.0;
ELSIF bMatch_12 THEN
    rSuperheaterThicknessVoted_mm := (ACOU_SUPERHEATER_CORROSION_801A + ACOU_SUPERHEATER_CORROSION_801B) / 2.0;
    bIso_Superheater_C := TRUE;
ELSIF bMatch_23 THEN
    rSuperheaterThicknessVoted_mm := (ACOU_SUPERHEATER_CORROSION_801B + ACOU_SUPERHEATER_CORROSION_801C) / 2.0;
    bIso_Superheater_A := TRUE;
ELSIF bMatch_13 THEN
    rSuperheaterThicknessVoted_mm := (ACOU_SUPERHEATER_CORROSION_801A + ACOU_SUPERHEATER_CORROSION_801C) / 2.0;
    bIso_Superheater_B := TRUE;
ELSE
    rTimer_TMR_Superheater_s := rTimer_TMR_Superheater_s + c_rTs;
    rSuperheaterThicknessVoted_mm := ACOU_SUPERHEATER_CORROSION_801B;
    IF rTimer_TMR_Superheater_s >= c_rTMR_PersistencyTimeout_s THEN
        dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_4000; (* Bit 14: Superheater Acoustic Discrepancy *)
    END_IF;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * Bank 16: Furnace Draft Negative Pressure PT_FURNACE_DRAFT_103A/B/C [mbar]
 * --------------------------------------------------------------------------------------------------------------------- *)
rDiff_12 := ABS(PT_FURNACE_DRAFT_103A - PT_FURNACE_DRAFT_103B);
rDiff_23 := ABS(PT_FURNACE_DRAFT_103B - PT_FURNACE_DRAFT_103C);
rDiff_13 := ABS(PT_FURNACE_DRAFT_103A - PT_FURNACE_DRAFT_103C);
bMatch_12 := (rDiff_12 <= c_rTol_FurnaceDraft_mbar) AND NOT bIso_Draft_A AND NOT bIso_Draft_B;
bMatch_23 := (rDiff_23 <= c_rTol_FurnaceDraft_mbar) AND NOT bIso_Draft_B AND NOT bIso_Draft_C;
bMatch_13 := (rDiff_13 <= c_rTol_FurnaceDraft_mbar) AND NOT bIso_Draft_A AND NOT bIso_Draft_C;

IF bMatch_12 AND bMatch_23 AND bMatch_13 THEN
    rMathTemp_C := (PT_FURNACE_DRAFT_103A + PT_FURNACE_DRAFT_103B + PT_FURNACE_DRAFT_103C) / 3.0;
    rTimer_TMR_Draft_s := 0.0;
ELSIF bMatch_12 THEN
    rMathTemp_C := (PT_FURNACE_DRAFT_103A + PT_FURNACE_DRAFT_103B) / 2.0;
    bIso_Draft_C := TRUE;
ELSIF bMatch_23 THEN
    rMathTemp_C := (PT_FURNACE_DRAFT_103B + PT_FURNACE_DRAFT_103C) / 2.0;
    bIso_Draft_A := TRUE;
ELSIF bMatch_13 THEN
    rMathTemp_C := (PT_FURNACE_DRAFT_103A + PT_FURNACE_DRAFT_103C) / 2.0;
    bIso_Draft_B := TRUE;
ELSE
    rTimer_TMR_Draft_s := rTimer_TMR_Draft_s + c_rTs;
    rMathTemp_C := PT_FURNACE_DRAFT_103B;
    IF rTimer_TMR_Draft_s >= c_rTMR_PersistencyTimeout_s THEN
        dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_8000; (* Bit 15: Draft Discrepancy *)
    END_IF;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * Bank 17: Boiler Superheated Steam Flow FT_BOILER_STEAM_FLOW_901A/B/C [t/h]
 * --------------------------------------------------------------------------------------------------------------------- *)
rDiff_12 := ABS(FT_BOILER_STEAM_FLOW_901A - FT_BOILER_STEAM_FLOW_901B);
rDiff_23 := ABS(FT_BOILER_STEAM_FLOW_901B - FT_BOILER_STEAM_FLOW_901C);
rDiff_13 := ABS(FT_BOILER_STEAM_FLOW_901A - FT_BOILER_STEAM_FLOW_901C);
bMatch_12 := (rDiff_12 <= c_rTol_SteamFlow_th) AND NOT bIso_Steam_A AND NOT bIso_Steam_B;
bMatch_23 := (rDiff_23 <= c_rTol_SteamFlow_th) AND NOT bIso_Steam_B AND NOT bIso_Steam_C;
bMatch_13 := (rDiff_13 <= c_rTol_SteamFlow_th) AND NOT bIso_Steam_A AND NOT bIso_Steam_C;

IF bMatch_12 AND bMatch_23 AND bMatch_13 THEN
    rSteamFlowVoted_th := (FT_BOILER_STEAM_FLOW_901A + FT_BOILER_STEAM_FLOW_901B + FT_BOILER_STEAM_FLOW_901C) / 3.0;
    rTimer_TMR_SteamFlow_s := 0.0;
ELSIF bMatch_12 THEN
    rSteamFlowVoted_th := (FT_BOILER_STEAM_FLOW_901A + FT_BOILER_STEAM_FLOW_901B) / 2.0;
    bIso_Steam_C := TRUE;
ELSIF bMatch_23 THEN
    rSteamFlowVoted_th := (FT_BOILER_STEAM_FLOW_901B + FT_BOILER_STEAM_FLOW_901C) / 2.0;
    bIso_Steam_A := TRUE;
ELSIF bMatch_13 THEN
    rSteamFlowVoted_th := (FT_BOILER_STEAM_FLOW_901A + FT_BOILER_STEAM_FLOW_901C) / 2.0;
    bIso_Steam_B := TRUE;
ELSE
    rTimer_TMR_SteamFlow_s := rTimer_TMR_SteamFlow_s + c_rTs;
    rSteamFlowVoted_th := FT_BOILER_STEAM_FLOW_901B;
    IF rTimer_TMR_SteamFlow_s >= c_rTMR_PersistencyTimeout_s THEN
        dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0001_0000; (* Bit 16: Steam Flow Discrepancy *)
    END_IF;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * Bank 18: Stack Clean Gas Residual Oxygen Analyzer AIT_STACK_O2_404A/B/C [vol%]
 * --------------------------------------------------------------------------------------------------------------------- *)
rDiff_12 := ABS(AIT_STACK_O2_404A - AIT_STACK_O2_404B);
rDiff_23 := ABS(AIT_STACK_O2_404B - AIT_STACK_O2_404C);
rDiff_13 := ABS(AIT_STACK_O2_404A - AIT_STACK_O2_404C);
bMatch_12 := (rDiff_12 <= c_rTol_StackO2_pct) AND NOT bIso_StackO2_A AND NOT bIso_StackO2_B;
bMatch_23 := (rDiff_23 <= c_rTol_StackO2_pct) AND NOT bIso_StackO2_B AND NOT bIso_StackO2_C;
bMatch_13 := (rDiff_13 <= c_rTol_StackO2_pct) AND NOT bIso_StackO2_A AND NOT bIso_StackO2_C;

IF bMatch_12 AND bMatch_23 AND bMatch_13 THEN
    rMathTemp_A := (AIT_STACK_O2_404A + AIT_STACK_O2_404B + AIT_STACK_O2_404C) / 3.0;
    rTimer_TMR_StackO2_s := 0.0;
ELSIF bMatch_12 THEN
    rMathTemp_A := (AIT_STACK_O2_404A + AIT_STACK_O2_404B) / 2.0;
    bIso_StackO2_C := TRUE;
ELSIF bMatch_23 THEN
    rMathTemp_A := (AIT_STACK_O2_404B + AIT_STACK_O2_404C) / 2.0;
    bIso_StackO2_A := TRUE;
ELSIF bMatch_13 THEN
    rMathTemp_A := (AIT_STACK_O2_404A + AIT_STACK_O2_404C) / 2.0;
    bIso_StackO2_B := TRUE;
ELSE
    rTimer_TMR_StackO2_s := rTimer_TMR_StackO2_s + c_rTs;
    rMathTemp_A := AIT_STACK_O2_404B;
    IF rTimer_TMR_StackO2_s >= c_rTMR_PersistencyTimeout_s THEN
        dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0002_0000; (* Bit 17: Stack O2 Discrepancy *)
    END_IF;
END_IF;
"""
