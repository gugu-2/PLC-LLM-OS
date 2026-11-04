# Generator part 5: 2oo3 TMR Sensor Voting
def get_tmr_logic():
    return """(* ============================================================================================= *)
(* SECTION 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING & DISCREPANCY ANALYSIS          *)
(* ============================================================================================= *)

(* 1.1 Inlet Trunnion Hydrostatic Bearing Lift Pressure (PT_TRUNNION_INLET_BEARING_201A/B/C) *)
(* Stuck/Frozen Sensor Check *)
IF PT_TRUNNION_INLET_BEARING_201A = rPrev_PT_Inlet_A THEN
    iStuck_PT_Inlet_A := iStuck_PT_Inlet_A + 1;
ELSE
    iStuck_PT_Inlet_A := 0;
END_IF;
rPrev_PT_Inlet_A := PT_TRUNNION_INLET_BEARING_201A;

IF PT_TRUNNION_INLET_BEARING_201B = rPrev_PT_Inlet_B THEN
    iStuck_PT_Inlet_B := iStuck_PT_Inlet_B + 1;
ELSE
    iStuck_PT_Inlet_B := 0;
END_IF;
rPrev_PT_Inlet_B := PT_TRUNNION_INLET_BEARING_201B;

IF PT_TRUNNION_INLET_BEARING_201C = rPrev_PT_Inlet_C THEN
    iStuck_PT_Inlet_C := iStuck_PT_Inlet_C + 1;
ELSE
    iStuck_PT_Inlet_C := 0;
END_IF;
rPrev_PT_Inlet_C := PT_TRUNNION_INLET_BEARING_201C;

bHealth_PT_Inlet_A := (PT_TRUNNION_INLET_BEARING_201A >= 10.0) AND (PT_TRUNNION_INLET_BEARING_201A <= 250.0) AND (iStuck_PT_Inlet_A < 500);
bHealth_PT_Inlet_B := (PT_TRUNNION_INLET_BEARING_201B >= 10.0) AND (PT_TRUNNION_INLET_BEARING_201B <= 250.0) AND (iStuck_PT_Inlet_B < 500);
bHealth_PT_Inlet_C := (PT_TRUNNION_INLET_BEARING_201C >= 10.0) AND (PT_TRUNNION_INLET_BEARING_201C <= 250.0) AND (iStuck_PT_Inlet_C < 500);

IF bHealth_PT_Inlet_A AND bHealth_PT_Inlet_B AND bHealth_PT_Inlet_C THEN
    bDegraded_PT_Inlet := FALSE;
    (* 2oo3 Median Selection *)
    IF ((PT_TRUNNION_INLET_BEARING_201A >= PT_TRUNNION_INLET_BEARING_201B) AND (PT_TRUNNION_INLET_BEARING_201A <= PT_TRUNNION_INLET_BEARING_201C)) OR
       ((PT_TRUNNION_INLET_BEARING_201A <= PT_TRUNNION_INLET_BEARING_201B) AND (PT_TRUNNION_INLET_BEARING_201A >= PT_TRUNNION_INLET_BEARING_201C)) THEN
        rVoted_InletTrunnionPress_bar := PT_TRUNNION_INLET_BEARING_201A;
    ELSIF ((PT_TRUNNION_INLET_BEARING_201B >= PT_TRUNNION_INLET_BEARING_201A) AND (PT_TRUNNION_INLET_BEARING_201B <= PT_TRUNNION_INLET_BEARING_201C)) OR
          ((PT_TRUNNION_INLET_BEARING_201B <= PT_TRUNNION_INLET_BEARING_201A) AND (PT_TRUNNION_INLET_BEARING_201B >= PT_TRUNNION_INLET_BEARING_201C)) THEN
        rVoted_InletTrunnionPress_bar := PT_TRUNNION_INLET_BEARING_201B;
    ELSE
        rVoted_InletTrunnionPress_bar := PT_TRUNNION_INLET_BEARING_201C;
    END_IF;
    (* Discrepancy checking *)
    IF (ABS(PT_TRUNNION_INLET_BEARING_201A - PT_TRUNNION_INLET_BEARING_201B) > rTol_TrunnionPress_bar) OR
       (ABS(PT_TRUNNION_INLET_BEARING_201B - PT_TRUNNION_INLET_BEARING_201C) > rTol_TrunnionPress_bar) OR
       (ABS(PT_TRUNNION_INLET_BEARING_201C - PT_TRUNNION_INLET_BEARING_201A) > rTol_TrunnionPress_bar) THEN
        dwTMR_Diagnostic_Weight := dwTMR_Diagnostic_Weight OR 16#0000_0001; (* Bit 0: INLET_PRESS_DISCREPANCY *)
    END_IF;
ELSIF bHealth_PT_Inlet_A AND bHealth_PT_Inlet_B THEN
    bDegraded_PT_Inlet := TRUE;
    rVoted_InletTrunnionPress_bar := (PT_TRUNNION_INLET_BEARING_201A + PT_TRUNNION_INLET_BEARING_201B) * 0.5;
    dwTMR_Diagnostic_Weight := dwTMR_Diagnostic_Weight OR 16#0000_0002; (* Bit 1: INLET_CH_C_FAILED *)
ELSIF bHealth_PT_Inlet_B AND bHealth_PT_Inlet_C THEN
    bDegraded_PT_Inlet := TRUE;
    rVoted_InletTrunnionPress_bar := (PT_TRUNNION_INLET_BEARING_201B + PT_TRUNNION_INLET_BEARING_201C) * 0.5;
    dwTMR_Diagnostic_Weight := dwTMR_Diagnostic_Weight OR 16#0000_0004; (* Bit 2: INLET_CH_A_FAILED *)
ELSIF bHealth_PT_Inlet_A AND bHealth_PT_Inlet_C THEN
    bDegraded_PT_Inlet := TRUE;
    rVoted_InletTrunnionPress_bar := (PT_TRUNNION_INLET_BEARING_201A + PT_TRUNNION_INLET_BEARING_201C) * 0.5;
    dwTMR_Diagnostic_Weight := dwTMR_Diagnostic_Weight OR 16#0000_0008; (* Bit 3: INLET_CH_B_FAILED *)
ELSIF bHealth_PT_Inlet_A THEN
    bDegraded_PT_Inlet := TRUE;
    rVoted_InletTrunnionPress_bar := PT_TRUNNION_INLET_BEARING_201A;
    dwTMR_Diagnostic_Weight := dwTMR_Diagnostic_Weight OR 16#0000_0010; (* Bit 4: INLET_1oo1_A_CRITICAL *)
ELSIF bHealth_PT_Inlet_B THEN
    bDegraded_PT_Inlet := TRUE;
    rVoted_InletTrunnionPress_bar := PT_TRUNNION_INLET_BEARING_201B;
    dwTMR_Diagnostic_Weight := dwTMR_Diagnostic_Weight OR 16#0000_0020; (* Bit 5: INLET_1oo1_B_CRITICAL *)
ELSIF bHealth_PT_Inlet_C THEN
    bDegraded_PT_Inlet := TRUE;
    rVoted_InletTrunnionPress_bar := PT_TRUNNION_INLET_BEARING_201C;
    dwTMR_Diagnostic_Weight := dwTMR_Diagnostic_Weight OR 16#0000_0040; (* Bit 6: INLET_1oo1_C_CRITICAL *)
ELSE
    dwTMR_Diagnostic_Weight := dwTMR_Diagnostic_Weight OR 16#0000_0080; (* Bit 7: INLET_ALL_FAILED_TRIP *)
END_IF;

(* 1.2 Outlet Trunnion Hydrostatic Bearing Lift Pressure (PT_TRUNNION_OUTLET_BEARING_202A/B/C) *)
IF PT_TRUNNION_OUTLET_BEARING_202A = rPrev_PT_Outlet_A THEN
    iStuck_PT_Outlet_A := iStuck_PT_Outlet_A + 1;
ELSE
    iStuck_PT_Outlet_A := 0;
END_IF;
rPrev_PT_Outlet_A := PT_TRUNNION_OUTLET_BEARING_202A;

IF PT_TRUNNION_OUTLET_BEARING_202B = rPrev_PT_Outlet_B THEN
    iStuck_PT_Outlet_B := iStuck_PT_Outlet_B + 1;
ELSE
    iStuck_PT_Outlet_B := 0;
END_IF;
rPrev_PT_Outlet_B := PT_TRUNNION_OUTLET_BEARING_202B;

IF PT_TRUNNION_OUTLET_BEARING_202C = rPrev_PT_Outlet_C THEN
    iStuck_PT_Outlet_C := iStuck_PT_Outlet_C + 1;
ELSE
    iStuck_PT_Outlet_C := 0;
END_IF;
rPrev_PT_Outlet_C := PT_TRUNNION_OUTLET_BEARING_202C;

bHealth_PT_Outlet_A := (PT_TRUNNION_OUTLET_BEARING_202A >= 10.0) AND (PT_TRUNNION_OUTLET_BEARING_202A <= 250.0) AND (iStuck_PT_Outlet_A < 500);
bHealth_PT_Outlet_B := (PT_TRUNNION_OUTLET_BEARING_202B >= 10.0) AND (PT_TRUNNION_OUTLET_BEARING_202B <= 250.0) AND (iStuck_PT_Outlet_B < 500);
bHealth_PT_Outlet_C := (PT_TRUNNION_OUTLET_BEARING_202C >= 10.0) AND (PT_TRUNNION_OUTLET_BEARING_202C <= 250.0) AND (iStuck_PT_Outlet_C < 500);

IF bHealth_PT_Outlet_A AND bHealth_PT_Outlet_B AND bHealth_PT_Outlet_C THEN
    bDegraded_PT_Outlet := FALSE;
    IF ((PT_TRUNNION_OUTLET_BEARING_202A >= PT_TRUNNION_OUTLET_BEARING_202B) AND (PT_TRUNNION_OUTLET_BEARING_202A <= PT_TRUNNION_OUTLET_BEARING_202C)) OR
       ((PT_TRUNNION_OUTLET_BEARING_202A <= PT_TRUNNION_OUTLET_BEARING_202B) AND (PT_TRUNNION_OUTLET_BEARING_202A >= PT_TRUNNION_OUTLET_BEARING_202C)) THEN
        rVoted_OutletTrunnionPress_bar := PT_TRUNNION_OUTLET_BEARING_202A;
    ELSIF ((PT_TRUNNION_OUTLET_BEARING_202B >= PT_TRUNNION_OUTLET_BEARING_202A) AND (PT_TRUNNION_OUTLET_BEARING_202B <= PT_TRUNNION_OUTLET_BEARING_202C)) OR
          ((PT_TRUNNION_OUTLET_BEARING_202B <= PT_TRUNNION_OUTLET_BEARING_202A) AND (PT_TRUNNION_OUTLET_BEARING_202B >= PT_TRUNNION_OUTLET_BEARING_202C)) THEN
        rVoted_OutletTrunnionPress_bar := PT_TRUNNION_OUTLET_BEARING_202B;
    ELSE
        rVoted_OutletTrunnionPress_bar := PT_TRUNNION_OUTLET_BEARING_202C;
    END_IF;
    IF (ABS(PT_TRUNNION_OUTLET_BEARING_202A - PT_TRUNNION_OUTLET_BEARING_202B) > rTol_TrunnionPress_bar) OR
       (ABS(PT_TRUNNION_OUTLET_BEARING_202B - PT_TRUNNION_OUTLET_BEARING_202C) > rTol_TrunnionPress_bar) OR
       (ABS(PT_TRUNNION_OUTLET_BEARING_202C - PT_TRUNNION_OUTLET_BEARING_202A) > rTol_TrunnionPress_bar) THEN
        dwTMR_Diagnostic_Weight := dwTMR_Diagnostic_Weight OR 16#0000_0100; (* Bit 8: OUTLET_PRESS_DISCREPANCY *)
    END_IF;
ELSIF bHealth_PT_Outlet_A AND bHealth_PT_Outlet_B THEN
    bDegraded_PT_Outlet := TRUE;
    rVoted_OutletTrunnionPress_bar := (PT_TRUNNION_OUTLET_BEARING_202A + PT_TRUNNION_OUTLET_BEARING_202B) * 0.5;
    dwTMR_Diagnostic_Weight := dwTMR_Diagnostic_Weight OR 16#0000_0200;
ELSIF bHealth_PT_Outlet_B AND bHealth_PT_Outlet_C THEN
    bDegraded_PT_Outlet := TRUE;
    rVoted_OutletTrunnionPress_bar := (PT_TRUNNION_OUTLET_BEARING_202B + PT_TRUNNION_OUTLET_BEARING_202C) * 0.5;
    dwTMR_Diagnostic_Weight := dwTMR_Diagnostic_Weight OR 16#0000_0400;
ELSIF bHealth_PT_Outlet_A AND bHealth_PT_Outlet_C THEN
    bDegraded_PT_Outlet := TRUE;
    rVoted_OutletTrunnionPress_bar := (PT_TRUNNION_OUTLET_BEARING_202A + PT_TRUNNION_OUTLET_BEARING_202C) * 0.5;
    dwTMR_Diagnostic_Weight := dwTMR_Diagnostic_Weight OR 16#0000_0800;
ELSIF bHealth_PT_Outlet_A THEN
    bDegraded_PT_Outlet := TRUE;
    rVoted_OutletTrunnionPress_bar := PT_TRUNNION_OUTLET_BEARING_202A;
    dwTMR_Diagnostic_Weight := dwTMR_Diagnostic_Weight OR 16#0000_1000;
ELSIF bHealth_PT_Outlet_B THEN
    bDegraded_PT_Outlet := TRUE;
    rVoted_OutletTrunnionPress_bar := PT_TRUNNION_OUTLET_BEARING_202B;
    dwTMR_Diagnostic_Weight := dwTMR_Diagnostic_Weight OR 16#0000_2000;
ELSIF bHealth_PT_Outlet_C THEN
    bDegraded_PT_Outlet := TRUE;
    rVoted_OutletTrunnionPress_bar := PT_TRUNNION_OUTLET_BEARING_202C;
    dwTMR_Diagnostic_Weight := dwTMR_Diagnostic_Weight OR 16#0000_4000;
ELSE
    dwTMR_Diagnostic_Weight := dwTMR_Diagnostic_Weight OR 16#0000_8000;
END_IF;

(* 1.3 Shell Acoustic Ear - Dynamic Grinding Toe Array (AIT_ACOUSTIC_EAR_TOE_301A/B/C) *)
IF AIT_ACOUSTIC_EAR_TOE_301A = rPrev_AIT_Toe_A THEN
    iStuck_AIT_Toe_A := iStuck_AIT_Toe_A + 1;
ELSE
    iStuck_AIT_Toe_A := 0;
END_IF;
rPrev_AIT_Toe_A := AIT_ACOUSTIC_EAR_TOE_301A;

IF AIT_ACOUSTIC_EAR_TOE_301B = rPrev_AIT_Toe_B THEN
    iStuck_AIT_Toe_B := iStuck_AIT_Toe_B + 1;
ELSE
    iStuck_AIT_Toe_B := 0;
END_IF;
rPrev_AIT_Toe_B := AIT_ACOUSTIC_EAR_TOE_301B;

IF AIT_ACOUSTIC_EAR_TOE_301C = rPrev_AIT_Toe_C THEN
    iStuck_AIT_Toe_C := iStuck_AIT_Toe_C + 1;
ELSE
    iStuck_AIT_Toe_C := 0;
END_IF;
rPrev_AIT_Toe_C := AIT_ACOUSTIC_EAR_TOE_301C;

bHealth_AIT_Toe_A := (AIT_ACOUSTIC_EAR_TOE_301A >= 0.0) AND (AIT_ACOUSTIC_EAR_TOE_301A <= 100.0) AND (iStuck_AIT_Toe_A < 500);
bHealth_AIT_Toe_B := (AIT_ACOUSTIC_EAR_TOE_301B >= 0.0) AND (AIT_ACOUSTIC_EAR_TOE_301B <= 100.0) AND (iStuck_AIT_Toe_B < 500);
bHealth_AIT_Toe_C := (AIT_ACOUSTIC_EAR_TOE_301C >= 0.0) AND (AIT_ACOUSTIC_EAR_TOE_301C <= 100.0) AND (iStuck_AIT_Toe_C < 500);

IF bHealth_AIT_Toe_A AND bHealth_AIT_Toe_B AND bHealth_AIT_Toe_C THEN
    bDegraded_AIT_Toe := FALSE;
    IF ((AIT_ACOUSTIC_EAR_TOE_301A >= AIT_ACOUSTIC_EAR_TOE_301B) AND (AIT_ACOUSTIC_EAR_TOE_301A <= AIT_ACOUSTIC_EAR_TOE_301C)) OR
       ((AIT_ACOUSTIC_EAR_TOE_301A <= AIT_ACOUSTIC_EAR_TOE_301B) AND (AIT_ACOUSTIC_EAR_TOE_301A >= AIT_ACOUSTIC_EAR_TOE_301C)) THEN
        rVoted_AcousticToe_Pct := AIT_ACOUSTIC_EAR_TOE_301A;
    ELSIF ((AIT_ACOUSTIC_EAR_TOE_301B >= AIT_ACOUSTIC_EAR_TOE_301A) AND (AIT_ACOUSTIC_EAR_TOE_301B <= AIT_ACOUSTIC_EAR_TOE_301C)) OR
          ((AIT_ACOUSTIC_EAR_TOE_301B <= AIT_ACOUSTIC_EAR_TOE_301A) AND (AIT_ACOUSTIC_EAR_TOE_301B >= AIT_ACOUSTIC_EAR_TOE_301C)) THEN
        rVoted_AcousticToe_Pct := AIT_ACOUSTIC_EAR_TOE_301B;
    ELSE
        rVoted_AcousticToe_Pct := AIT_ACOUSTIC_EAR_TOE_301C;
    END_IF;
    IF (ABS(AIT_ACOUSTIC_EAR_TOE_301A - AIT_ACOUSTIC_EAR_TOE_301B) > rTol_AcousticEar_Pct) OR
       (ABS(AIT_ACOUSTIC_EAR_TOE_301B - AIT_ACOUSTIC_EAR_TOE_301C) > rTol_AcousticEar_Pct) OR
       (ABS(AIT_ACOUSTIC_EAR_TOE_301C - AIT_ACOUSTIC_EAR_TOE_301A) > rTol_AcousticEar_Pct) THEN
        dwTMR_Diagnostic_Acoustic := dwTMR_Diagnostic_Acoustic OR 16#0000_0001;
    END_IF;
ELSIF bHealth_AIT_Toe_A AND bHealth_AIT_Toe_B THEN
    bDegraded_AIT_Toe := TRUE;
    rVoted_AcousticToe_Pct := (AIT_ACOUSTIC_EAR_TOE_301A + AIT_ACOUSTIC_EAR_TOE_301B) * 0.5;
    dwTMR_Diagnostic_Acoustic := dwTMR_Diagnostic_Acoustic OR 16#0000_0002;
ELSIF bHealth_AIT_Toe_B AND bHealth_AIT_Toe_C THEN
    bDegraded_AIT_Toe := TRUE;
    rVoted_AcousticToe_Pct := (AIT_ACOUSTIC_EAR_TOE_301B + AIT_ACOUSTIC_EAR_TOE_301C) * 0.5;
    dwTMR_Diagnostic_Acoustic := dwTMR_Diagnostic_Acoustic OR 16#0000_0004;
ELSIF bHealth_AIT_Toe_A AND bHealth_AIT_Toe_C THEN
    bDegraded_AIT_Toe := TRUE;
    rVoted_AcousticToe_Pct := (AIT_ACOUSTIC_EAR_TOE_301A + AIT_ACOUSTIC_EAR_TOE_301C) * 0.5;
    dwTMR_Diagnostic_Acoustic := dwTMR_Diagnostic_Acoustic OR 16#0000_0008;
ELSIF bHealth_AIT_Toe_A THEN
    bDegraded_AIT_Toe := TRUE;
    rVoted_AcousticToe_Pct := AIT_ACOUSTIC_EAR_TOE_301A;
    dwTMR_Diagnostic_Acoustic := dwTMR_Diagnostic_Acoustic OR 16#0000_0010;
ELSIF bHealth_AIT_Toe_B THEN
    bDegraded_AIT_Toe := TRUE;
    rVoted_AcousticToe_Pct := AIT_ACOUSTIC_EAR_TOE_301B;
    dwTMR_Diagnostic_Acoustic := dwTMR_Diagnostic_Acoustic OR 16#0000_0020;
ELSIF bHealth_AIT_Toe_C THEN
    bDegraded_AIT_Toe := TRUE;
    rVoted_AcousticToe_Pct := AIT_ACOUSTIC_EAR_TOE_301C;
    dwTMR_Diagnostic_Acoustic := dwTMR_Diagnostic_Acoustic OR 16#0000_0040;
ELSE
    dwTMR_Diagnostic_Acoustic := dwTMR_Diagnostic_Acoustic OR 16#0000_0080;
END_IF;

(* 1.4 Shell Acoustic Ear - Charge Shoulder Array (AIT_ACOUSTIC_EAR_SHOULDER_302A/B/C) *)
IF AIT_ACOUSTIC_EAR_SHOULDER_302A = rPrev_AIT_Shldr_A THEN
    iStuck_AIT_Shldr_A := iStuck_AIT_Shldr_A + 1;
ELSE
    iStuck_AIT_Shldr_A := 0;
END_IF;
rPrev_AIT_Shldr_A := AIT_ACOUSTIC_EAR_SHOULDER_302A;

IF AIT_ACOUSTIC_EAR_SHOULDER_302B = rPrev_AIT_Shldr_B THEN
    iStuck_AIT_Shldr_B := iStuck_AIT_Shldr_B + 1;
ELSE
    iStuck_AIT_Shldr_B := 0;
END_IF;
rPrev_AIT_Shldr_B := AIT_ACOUSTIC_EAR_SHOULDER_302B;

IF AIT_ACOUSTIC_EAR_SHOULDER_302C = rPrev_AIT_Shldr_C THEN
    iStuck_AIT_Shldr_C := iStuck_AIT_Shldr_C + 1;
ELSE
    iStuck_AIT_Shldr_C := 0;
END_IF;
rPrev_AIT_Shldr_C := AIT_ACOUSTIC_EAR_SHOULDER_302C;

bHealth_AIT_Shldr_A := (AIT_ACOUSTIC_EAR_SHOULDER_302A >= 0.0) AND (AIT_ACOUSTIC_EAR_SHOULDER_302A <= 100.0) AND (iStuck_AIT_Shldr_A < 500);
bHealth_AIT_Shldr_B := (AIT_ACOUSTIC_EAR_SHOULDER_302B >= 0.0) AND (AIT_ACOUSTIC_EAR_SHOULDER_302B <= 100.0) AND (iStuck_AIT_Shldr_B < 500);
bHealth_AIT_Shldr_C := (AIT_ACOUSTIC_EAR_SHOULDER_302C >= 0.0) AND (AIT_ACOUSTIC_EAR_SHOULDER_302C <= 100.0) AND (iStuck_AIT_Shldr_C < 500);

IF bHealth_AIT_Shldr_A AND bHealth_AIT_Shldr_B AND bHealth_AIT_Shldr_C THEN
    bDegraded_AIT_Shldr := FALSE;
    IF ((AIT_ACOUSTIC_EAR_SHOULDER_302A >= AIT_ACOUSTIC_EAR_SHOULDER_302B) AND (AIT_ACOUSTIC_EAR_SHOULDER_302A <= AIT_ACOUSTIC_EAR_SHOULDER_302C)) OR
       ((AIT_ACOUSTIC_EAR_SHOULDER_302A <= AIT_ACOUSTIC_EAR_SHOULDER_302B) AND (AIT_ACOUSTIC_EAR_SHOULDER_302A >= AIT_ACOUSTIC_EAR_SHOULDER_302C)) THEN
        rVoted_AcousticShoulder_Pct := AIT_ACOUSTIC_EAR_SHOULDER_302A;
    ELSIF ((AIT_ACOUSTIC_EAR_SHOULDER_302B >= AIT_ACOUSTIC_EAR_SHOULDER_302A) AND (AIT_ACOUSTIC_EAR_SHOULDER_302B <= AIT_ACOUSTIC_EAR_SHOULDER_302C)) OR
          ((AIT_ACOUSTIC_EAR_SHOULDER_302B <= AIT_ACOUSTIC_EAR_SHOULDER_302A) AND (AIT_ACOUSTIC_EAR_SHOULDER_302B >= AIT_ACOUSTIC_EAR_SHOULDER_302C)) THEN
        rVoted_AcousticShoulder_Pct := AIT_ACOUSTIC_EAR_SHOULDER_302B;
    ELSE
        rVoted_AcousticShoulder_Pct := AIT_ACOUSTIC_EAR_SHOULDER_302C;
    END_IF;
    IF (ABS(AIT_ACOUSTIC_EAR_SHOULDER_302A - AIT_ACOUSTIC_EAR_SHOULDER_302B) > rTol_AcousticEar_Pct) OR
       (ABS(AIT_ACOUSTIC_EAR_SHOULDER_302B - AIT_ACOUSTIC_EAR_SHOULDER_302C) > rTol_AcousticEar_Pct) OR
       (ABS(AIT_ACOUSTIC_EAR_SHOULDER_302C - AIT_ACOUSTIC_EAR_SHOULDER_302A) > rTol_AcousticEar_Pct) THEN
        dwTMR_Diagnostic_Acoustic := dwTMR_Diagnostic_Acoustic OR 16#0000_0100;
    END_IF;
ELSIF bHealth_AIT_Shldr_A AND bHealth_AIT_Shldr_B THEN
    bDegraded_AIT_Shldr := TRUE;
    rVoted_AcousticShoulder_Pct := (AIT_ACOUSTIC_EAR_SHOULDER_302A + AIT_ACOUSTIC_EAR_SHOULDER_302B) * 0.5;
    dwTMR_Diagnostic_Acoustic := dwTMR_Diagnostic_Acoustic OR 16#0000_0200;
ELSIF bHealth_AIT_Shldr_B AND bHealth_AIT_Shldr_C THEN
    bDegraded_AIT_Shldr := TRUE;
    rVoted_AcousticShoulder_Pct := (AIT_ACOUSTIC_EAR_SHOULDER_302B + AIT_ACOUSTIC_EAR_SHOULDER_302C) * 0.5;
    dwTMR_Diagnostic_Acoustic := dwTMR_Diagnostic_Acoustic OR 16#0000_0400;
ELSIF bHealth_AIT_Shldr_A AND bHealth_AIT_Shldr_C THEN
    bDegraded_AIT_Shldr := TRUE;
    rVoted_AcousticShoulder_Pct := (AIT_ACOUSTIC_EAR_SHOULDER_302A + AIT_ACOUSTIC_EAR_SHOULDER_302C) * 0.5;
    dwTMR_Diagnostic_Acoustic := dwTMR_Diagnostic_Acoustic OR 16#0000_0800;
ELSIF bHealth_AIT_Shldr_A THEN
    bDegraded_AIT_Shldr := TRUE;
    rVoted_AcousticShoulder_Pct := AIT_ACOUSTIC_EAR_SHOULDER_302A;
    dwTMR_Diagnostic_Acoustic := dwTMR_Diagnostic_Acoustic OR 16#0000_1000;
ELSIF bHealth_AIT_Shldr_B THEN
    bDegraded_AIT_Shldr := TRUE;
    rVoted_AcousticShoulder_Pct := AIT_ACOUSTIC_EAR_SHOULDER_302B;
    dwTMR_Diagnostic_Acoustic := dwTMR_Diagnostic_Acoustic OR 16#0000_2000;
ELSIF bHealth_AIT_Shldr_C THEN
    bDegraded_AIT_Shldr := TRUE;
    rVoted_AcousticShoulder_Pct := AIT_ACOUSTIC_EAR_SHOULDER_302C;
    dwTMR_Diagnostic_Acoustic := dwTMR_Diagnostic_Acoustic OR 16#0000_4000;
ELSE
    dwTMR_Diagnostic_Acoustic := dwTMR_Diagnostic_Acoustic OR 16#0000_8000;
END_IF;

(* 1.5 Cyclone Feed Slurry Nuclear Gamma Density Gauges (DT_CYCLONE_FEED_DENSITY_502A/B/C) *)
IF DT_CYCLONE_FEED_DENSITY_502A = rPrev_DT_Dens_A THEN
    iStuck_DT_Dens_A := iStuck_DT_Dens_A + 1;
ELSE
    iStuck_DT_Dens_A := 0;
END_IF;
rPrev_DT_Dens_A := DT_CYCLONE_FEED_DENSITY_502A;

IF DT_CYCLONE_FEED_DENSITY_502B = rPrev_DT_Dens_B THEN
    iStuck_DT_Dens_B := iStuck_DT_Dens_B + 1;
ELSE
    iStuck_DT_Dens_B := 0;
END_IF;
rPrev_DT_Dens_B := DT_CYCLONE_FEED_DENSITY_502B;

IF DT_CYCLONE_FEED_DENSITY_502C = rPrev_DT_Dens_C THEN
    iStuck_DT_Dens_C := iStuck_DT_Dens_C + 1;
ELSE
    iStuck_DT_Dens_C := 0;
END_IF;
rPrev_DT_Dens_C := DT_CYCLONE_FEED_DENSITY_502C;

bHealth_DT_Dens_A := (DT_CYCLONE_FEED_DENSITY_502A >= 1.050) AND (DT_CYCLONE_FEED_DENSITY_502A <= 2.200) AND (iStuck_DT_Dens_A < 500);
bHealth_DT_Dens_B := (DT_CYCLONE_FEED_DENSITY_502B >= 1.050) AND (DT_CYCLONE_FEED_DENSITY_502B <= 2.200) AND (iStuck_DT_Dens_B < 500);
bHealth_DT_Dens_C := (DT_CYCLONE_FEED_DENSITY_502C >= 1.050) AND (DT_CYCLONE_FEED_DENSITY_502C <= 2.200) AND (iStuck_DT_Dens_C < 500);

IF bHealth_DT_Dens_A AND bHealth_DT_Dens_B AND bHealth_DT_Dens_C THEN
    bDegraded_DT_Dens := FALSE;
    IF ((DT_CYCLONE_FEED_DENSITY_502A >= DT_CYCLONE_FEED_DENSITY_502B) AND (DT_CYCLONE_FEED_DENSITY_502A <= DT_CYCLONE_FEED_DENSITY_502C)) OR
       ((DT_CYCLONE_FEED_DENSITY_502A <= DT_CYCLONE_FEED_DENSITY_502B) AND (DT_CYCLONE_FEED_DENSITY_502A >= DT_CYCLONE_FEED_DENSITY_502C)) THEN
        rVoted_SlurryDensity_SG := DT_CYCLONE_FEED_DENSITY_502A;
    ELSIF ((DT_CYCLONE_FEED_DENSITY_502B >= DT_CYCLONE_FEED_DENSITY_502A) AND (DT_CYCLONE_FEED_DENSITY_502B <= DT_CYCLONE_FEED_DENSITY_502C)) OR
          ((DT_CYCLONE_FEED_DENSITY_502B <= DT_CYCLONE_FEED_DENSITY_502A) AND (DT_CYCLONE_FEED_DENSITY_502B >= DT_CYCLONE_FEED_DENSITY_502C)) THEN
        rVoted_SlurryDensity_SG := DT_CYCLONE_FEED_DENSITY_502B;
    ELSE
        rVoted_SlurryDensity_SG := DT_CYCLONE_FEED_DENSITY_502C;
    END_IF;
    IF (ABS(DT_CYCLONE_FEED_DENSITY_502A - DT_CYCLONE_FEED_DENSITY_502B) > rTol_SlurryDensity_SG) OR
       (ABS(DT_CYCLONE_FEED_DENSITY_502B - DT_CYCLONE_FEED_DENSITY_502C) > rTol_SlurryDensity_SG) OR
       (ABS(DT_CYCLONE_FEED_DENSITY_502C - DT_CYCLONE_FEED_DENSITY_502A) > rTol_SlurryDensity_SG) THEN
        dwTMR_Diagnostic_Density := dwTMR_Diagnostic_Density OR 16#0000_0001; (* DENSITY_DISCREPANCY *)
    END_IF;
ELSIF bHealth_DT_Dens_A AND bHealth_DT_Dens_B THEN
    bDegraded_DT_Dens := TRUE;
    rVoted_SlurryDensity_SG := (DT_CYCLONE_FEED_DENSITY_502A + DT_CYCLONE_FEED_DENSITY_502B) * 0.5;
    dwTMR_Diagnostic_Density := dwTMR_Diagnostic_Density OR 16#0000_0002;
ELSIF bHealth_DT_Dens_B AND bHealth_DT_Dens_C THEN
    bDegraded_DT_Dens := TRUE;
    rVoted_SlurryDensity_SG := (DT_CYCLONE_FEED_DENSITY_502B + DT_CYCLONE_FEED_DENSITY_502C) * 0.5;
    dwTMR_Diagnostic_Density := dwTMR_Diagnostic_Density OR 16#0000_0004;
ELSIF bHealth_DT_Dens_A AND bHealth_DT_Dens_C THEN
    bDegraded_DT_Dens := TRUE;
    rVoted_SlurryDensity_SG := (DT_CYCLONE_FEED_DENSITY_502A + DT_CYCLONE_FEED_DENSITY_502C) * 0.5;
    dwTMR_Diagnostic_Density := dwTMR_Diagnostic_Density OR 16#0000_0008;
ELSIF bHealth_DT_Dens_A THEN
    bDegraded_DT_Dens := TRUE;
    rVoted_SlurryDensity_SG := DT_CYCLONE_FEED_DENSITY_502A;
    dwTMR_Diagnostic_Density := dwTMR_Diagnostic_Density OR 16#0000_0010;
ELSIF bHealth_DT_Dens_B THEN
    bDegraded_DT_Dens := TRUE;
    rVoted_SlurryDensity_SG := DT_CYCLONE_FEED_DENSITY_502B;
    dwTMR_Diagnostic_Density := dwTMR_Diagnostic_Density OR 16#0000_0020;
ELSIF bHealth_DT_Dens_C THEN
    bDegraded_DT_Dens := TRUE;
    rVoted_SlurryDensity_SG := DT_CYCLONE_FEED_DENSITY_502C;
    dwTMR_Diagnostic_Density := dwTMR_Diagnostic_Density OR 16#0000_0040;
ELSE
    dwTMR_Diagnostic_Density := dwTMR_Diagnostic_Density OR 16#0000_0080;
END_IF;

(* 1.6 Cyclone Feed Sump Slurry Level Transmitters (LT_CYCLONE_SUMP_LEVEL_501A/B/C) *)
IF LT_CYCLONE_SUMP_LEVEL_501A = rPrev_LT_Sump_A THEN
    iStuck_LT_Sump_A := iStuck_LT_Sump_A + 1;
ELSE
    iStuck_LT_Sump_A := 0;
END_IF;
rPrev_LT_Sump_A := LT_CYCLONE_SUMP_LEVEL_501A;

IF LT_CYCLONE_SUMP_LEVEL_501B = rPrev_LT_Sump_B THEN
    iStuck_LT_Sump_B := iStuck_LT_Sump_B + 1;
ELSE
    iStuck_LT_Sump_B := 0;
END_IF;
rPrev_LT_Sump_B := LT_CYCLONE_SUMP_LEVEL_501B;

IF LT_CYCLONE_SUMP_LEVEL_501C = rPrev_LT_Sump_C THEN
    iStuck_LT_Sump_C := iStuck_LT_Sump_C + 1;
ELSE
    iStuck_LT_Sump_C := 0;
END_IF;
rPrev_LT_Sump_C := LT_CYCLONE_SUMP_LEVEL_501C;

bHealth_LT_Sump_A := (LT_CYCLONE_SUMP_LEVEL_501A >= 0.0) AND (LT_CYCLONE_SUMP_LEVEL_501A <= 100.0) AND (iStuck_LT_Sump_A < 500);
bHealth_LT_Sump_B := (LT_CYCLONE_SUMP_LEVEL_501B >= 0.0) AND (LT_CYCLONE_SUMP_LEVEL_501B <= 100.0) AND (iStuck_LT_Sump_B < 500);
bHealth_LT_Sump_C := (LT_CYCLONE_SUMP_LEVEL_501C >= 0.0) AND (LT_CYCLONE_SUMP_LEVEL_501C <= 100.0) AND (iStuck_LT_Sump_C < 500);

IF bHealth_LT_Sump_A AND bHealth_LT_Sump_B AND bHealth_LT_Sump_C THEN
    bDegraded_LT_Sump := FALSE;
    IF ((LT_CYCLONE_SUMP_LEVEL_501A >= LT_CYCLONE_SUMP_LEVEL_501B) AND (LT_CYCLONE_SUMP_LEVEL_501A <= LT_CYCLONE_SUMP_LEVEL_501C)) OR
       ((LT_CYCLONE_SUMP_LEVEL_501A <= LT_CYCLONE_SUMP_LEVEL_501B) AND (LT_CYCLONE_SUMP_LEVEL_501A >= LT_CYCLONE_SUMP_LEVEL_501C)) THEN
        rVoted_SumpLevel_Pct := LT_CYCLONE_SUMP_LEVEL_501A;
    ELSIF ((LT_CYCLONE_SUMP_LEVEL_501B >= LT_CYCLONE_SUMP_LEVEL_501A) AND (LT_CYCLONE_SUMP_LEVEL_501B <= LT_CYCLONE_SUMP_LEVEL_501C)) OR
          ((LT_CYCLONE_SUMP_LEVEL_501B <= LT_CYCLONE_SUMP_LEVEL_501A) AND (LT_CYCLONE_SUMP_LEVEL_501B >= LT_CYCLONE_SUMP_LEVEL_501C)) THEN
        rVoted_SumpLevel_Pct := LT_CYCLONE_SUMP_LEVEL_501B;
    ELSE
        rVoted_SumpLevel_Pct := LT_CYCLONE_SUMP_LEVEL_501C;
    END_IF;
ELSIF bHealth_LT_Sump_A AND bHealth_LT_Sump_B THEN
    bDegraded_LT_Sump := TRUE;
    rVoted_SumpLevel_Pct := (LT_CYCLONE_SUMP_LEVEL_501A + LT_CYCLONE_SUMP_LEVEL_501B) * 0.5;
ELSIF bHealth_LT_Sump_B AND bHealth_LT_Sump_C THEN
    bDegraded_LT_Sump := TRUE;
    rVoted_SumpLevel_Pct := (LT_CYCLONE_SUMP_LEVEL_501B + LT_CYCLONE_SUMP_LEVEL_501C) * 0.5;
ELSIF bHealth_LT_Sump_A AND bHealth_LT_Sump_C THEN
    bDegraded_LT_Sump := TRUE;
    rVoted_SumpLevel_Pct := (LT_CYCLONE_SUMP_LEVEL_501A + LT_CYCLONE_SUMP_LEVEL_501C) * 0.5;
ELSIF bHealth_LT_Sump_A THEN
    bDegraded_LT_Sump := TRUE;
    rVoted_SumpLevel_Pct := LT_CYCLONE_SUMP_LEVEL_501A;
ELSIF bHealth_LT_Sump_B THEN
    bDegraded_LT_Sump := TRUE;
    rVoted_SumpLevel_Pct := LT_CYCLONE_SUMP_LEVEL_501B;
ELSIF bHealth_LT_Sump_C THEN
    bDegraded_LT_Sump := TRUE;
    rVoted_SumpLevel_Pct := LT_CYCLONE_SUMP_LEVEL_501C;
END_IF;

(* 1.7 Cyclone Distributor Manifold Pressure (PT_CYCLONE_MANIFOLD_503A/B/C) *)
bHealth_PT_Manif_A := (PT_CYCLONE_MANIFOLD_503A >= 0.0) AND (PT_CYCLONE_MANIFOLD_503A <= 250.0);
bHealth_PT_Manif_B := (PT_CYCLONE_MANIFOLD_503B >= 0.0) AND (PT_CYCLONE_MANIFOLD_503B <= 250.0);
bHealth_PT_Manif_C := (PT_CYCLONE_MANIFOLD_503C >= 0.0) AND (PT_CYCLONE_MANIFOLD_503C <= 250.0);

IF bHealth_PT_Manif_A AND bHealth_PT_Manif_B AND bHealth_PT_Manif_C THEN
    bDegraded_PT_Manif := FALSE;
    IF ((PT_CYCLONE_MANIFOLD_503A >= PT_CYCLONE_MANIFOLD_503B) AND (PT_CYCLONE_MANIFOLD_503A <= PT_CYCLONE_MANIFOLD_503C)) OR
       ((PT_CYCLONE_MANIFOLD_503A <= PT_CYCLONE_MANIFOLD_503B) AND (PT_CYCLONE_MANIFOLD_503A >= PT_CYCLONE_MANIFOLD_503C)) THEN
        rVoted_ManifoldPress_kPa := PT_CYCLONE_MANIFOLD_503A;
    ELSIF ((PT_CYCLONE_MANIFOLD_503B >= PT_CYCLONE_MANIFOLD_503A) AND (PT_CYCLONE_MANIFOLD_503B <= PT_CYCLONE_MANIFOLD_503C)) OR
          ((PT_CYCLONE_MANIFOLD_503B <= PT_CYCLONE_MANIFOLD_503A) AND (PT_CYCLONE_MANIFOLD_503B >= PT_CYCLONE_MANIFOLD_503C)) THEN
        rVoted_ManifoldPress_kPa := PT_CYCLONE_MANIFOLD_503B;
    ELSE
        rVoted_ManifoldPress_kPa := PT_CYCLONE_MANIFOLD_503C;
    END_IF;
ELSIF bHealth_PT_Manif_A AND bHealth_PT_Manif_B THEN
    bDegraded_PT_Manif := TRUE;
    rVoted_ManifoldPress_kPa := (PT_CYCLONE_MANIFOLD_503A + PT_CYCLONE_MANIFOLD_503B) * 0.5;
ELSIF bHealth_PT_Manif_B AND bHealth_PT_Manif_C THEN
    bDegraded_PT_Manif := TRUE;
    rVoted_ManifoldPress_kPa := (PT_CYCLONE_MANIFOLD_503B + PT_CYCLONE_MANIFOLD_503C) * 0.5;
ELSIF bHealth_PT_Manif_A AND bHealth_PT_Manif_C THEN
    bDegraded_PT_Manif := TRUE;
    rVoted_ManifoldPress_kPa := (PT_CYCLONE_MANIFOLD_503A + PT_CYCLONE_MANIFOLD_503C) * 0.5;
ELSIF bHealth_PT_Manif_A THEN
    rVoted_ManifoldPress_kPa := PT_CYCLONE_MANIFOLD_503A;
ELSIF bHealth_PT_Manif_B THEN
    rVoted_ManifoldPress_kPa := PT_CYCLONE_MANIFOLD_503B;
ELSIF bHealth_PT_Manif_C THEN
    rVoted_ManifoldPress_kPa := PT_CYCLONE_MANIFOLD_503C;
END_IF;

(* 1.8 Gearless Ring Motor Rotational Speed (ST_SAG_RING_MOTOR_RPM_401A/B/C) *)
bHealth_ST_RPM_A := (ST_SAG_RING_MOTOR_RPM_401A >= 0.0) AND (ST_SAG_RING_MOTOR_RPM_401A <= 15.0);
bHealth_ST_RPM_B := (ST_SAG_RING_MOTOR_RPM_401B >= 0.0) AND (ST_SAG_RING_MOTOR_RPM_401B <= 15.0);
bHealth_ST_RPM_C := (ST_SAG_RING_MOTOR_RPM_401C >= 0.0) AND (ST_SAG_RING_MOTOR_RPM_401C <= 15.0);

IF bHealth_ST_RPM_A AND bHealth_ST_RPM_B AND bHealth_ST_RPM_C THEN
    bDegraded_ST_RPM := FALSE;
    IF ((ST_SAG_RING_MOTOR_RPM_401A >= ST_SAG_RING_MOTOR_RPM_401B) AND (ST_SAG_RING_MOTOR_RPM_401A <= ST_SAG_RING_MOTOR_RPM_401C)) OR
       ((ST_SAG_RING_MOTOR_RPM_401A <= ST_SAG_RING_MOTOR_RPM_401B) AND (ST_SAG_RING_MOTOR_RPM_401A >= ST_SAG_RING_MOTOR_RPM_401C)) THEN
        rVoted_RingMotorRPM := ST_SAG_RING_MOTOR_RPM_401A;
    ELSIF ((ST_SAG_RING_MOTOR_RPM_401B >= ST_SAG_RING_MOTOR_RPM_401A) AND (ST_SAG_RING_MOTOR_RPM_401B <= ST_SAG_RING_MOTOR_RPM_401C)) OR
          ((ST_SAG_RING_MOTOR_RPM_401B <= ST_SAG_RING_MOTOR_RPM_401A) AND (ST_SAG_RING_MOTOR_RPM_401B >= ST_SAG_RING_MOTOR_RPM_401C)) THEN
        rVoted_RingMotorRPM := ST_SAG_RING_MOTOR_RPM_401B;
    ELSE
        rVoted_RingMotorRPM := ST_SAG_RING_MOTOR_RPM_401C;
    END_IF;
ELSIF bHealth_ST_RPM_A AND bHealth_ST_RPM_B THEN
    bDegraded_ST_RPM := TRUE;
    rVoted_RingMotorRPM := (ST_SAG_RING_MOTOR_RPM_401A + ST_SAG_RING_MOTOR_RPM_401B) * 0.5;
ELSIF bHealth_ST_RPM_B AND bHealth_ST_RPM_C THEN
    bDegraded_ST_RPM := TRUE;
    rVoted_RingMotorRPM := (ST_SAG_RING_MOTOR_RPM_401B + ST_SAG_RING_MOTOR_RPM_401C) * 0.5;
ELSIF bHealth_ST_RPM_A AND bHealth_ST_RPM_C THEN
    bDegraded_ST_RPM := TRUE;
    rVoted_RingMotorRPM := (ST_SAG_RING_MOTOR_RPM_401A + ST_SAG_RING_MOTOR_RPM_401C) * 0.5;
ELSIF bHealth_ST_RPM_A THEN
    rVoted_RingMotorRPM := ST_SAG_RING_MOTOR_RPM_401A;
ELSIF bHealth_ST_RPM_B THEN
    rVoted_RingMotorRPM := ST_SAG_RING_MOTOR_RPM_401B;
ELSIF bHealth_ST_RPM_C THEN
    rVoted_RingMotorRPM := ST_SAG_RING_MOTOR_RPM_401C;
END_IF;

(* 1.9 Gearless Ring Motor Active Electrical Power (IT_SAG_MOTOR_POWER_402A/B/C) *)
bHealth_IT_MW_A := (IT_SAG_MOTOR_POWER_402A >= 0.0) AND (IT_SAG_MOTOR_POWER_402A <= 35.0);
bHealth_IT_MW_B := (IT_SAG_MOTOR_POWER_402B >= 0.0) AND (IT_SAG_MOTOR_POWER_402B <= 35.0);
bHealth_IT_MW_C := (IT_SAG_MOTOR_POWER_402C >= 0.0) AND (IT_SAG_MOTOR_POWER_402C <= 35.0);

IF bHealth_IT_MW_A AND bHealth_IT_MW_B AND bHealth_IT_MW_C THEN
    bDegraded_IT_MW := FALSE;
    IF ((IT_SAG_MOTOR_POWER_402A >= IT_SAG_MOTOR_POWER_402B) AND (IT_SAG_MOTOR_POWER_402A <= IT_SAG_MOTOR_POWER_402C)) OR
       ((IT_SAG_MOTOR_POWER_402A <= IT_SAG_MOTOR_POWER_402B) AND (IT_SAG_MOTOR_POWER_402A >= IT_SAG_MOTOR_POWER_402C)) THEN
        rVoted_RingMotorPower_MW := IT_SAG_MOTOR_POWER_402A;
    ELSIF ((IT_SAG_MOTOR_POWER_402B >= IT_SAG_MOTOR_POWER_402A) AND (IT_SAG_MOTOR_POWER_402B <= IT_SAG_MOTOR_POWER_402C)) OR
          ((IT_SAG_MOTOR_POWER_402B <= IT_SAG_MOTOR_POWER_402A) AND (IT_SAG_MOTOR_POWER_402B >= IT_SAG_MOTOR_POWER_402C)) THEN
        rVoted_RingMotorPower_MW := IT_SAG_MOTOR_POWER_402B;
    ELSE
        rVoted_RingMotorPower_MW := IT_SAG_MOTOR_POWER_402C;
    END_IF;
ELSIF bHealth_IT_MW_A AND bHealth_IT_MW_B THEN
    bDegraded_IT_MW := TRUE;
    rVoted_RingMotorPower_MW := (IT_SAG_MOTOR_POWER_402A + IT_SAG_MOTOR_POWER_402B) * 0.5;
ELSIF bHealth_IT_MW_B AND bHealth_IT_MW_C THEN
    bDegraded_IT_MW := TRUE;
    rVoted_RingMotorPower_MW := (IT_SAG_MOTOR_POWER_402B + IT_SAG_MOTOR_POWER_402C) * 0.5;
ELSIF bHealth_IT_MW_A AND bHealth_IT_MW_C THEN
    bDegraded_IT_MW := TRUE;
    rVoted_RingMotorPower_MW := (IT_SAG_MOTOR_POWER_402A + IT_SAG_MOTOR_POWER_402C) * 0.5;
ELSIF bHealth_IT_MW_A THEN
    rVoted_RingMotorPower_MW := IT_SAG_MOTOR_POWER_402A;
ELSIF bHealth_IT_MW_B THEN
    rVoted_RingMotorPower_MW := IT_SAG_MOTOR_POWER_402B;
ELSIF bHealth_IT_MW_C THEN
    rVoted_RingMotorPower_MW := IT_SAG_MOTOR_POWER_402C;
END_IF;

(* 1.10 Fresh SAG Feed Ore Conveyor Weightometers (WT_SAG_FEED_CONVEYOR_101A/B/C) *)
bHealth_WT_Feed_A := (WT_SAG_FEED_CONVEYOR_101A >= 0.0) AND (WT_SAG_FEED_CONVEYOR_101A <= 4200.0);
bHealth_WT_Feed_B := (WT_SAG_FEED_CONVEYOR_101B >= 0.0) AND (WT_SAG_FEED_CONVEYOR_101B <= 4200.0);
bHealth_WT_Feed_C := (WT_SAG_FEED_CONVEYOR_101C >= 0.0) AND (WT_SAG_FEED_CONVEYOR_101C <= 4200.0);

IF bHealth_WT_Feed_A AND bHealth_WT_Feed_B AND bHealth_WT_Feed_C THEN
    bDegraded_WT_Feed := FALSE;
    IF ((WT_SAG_FEED_CONVEYOR_101A >= WT_SAG_FEED_CONVEYOR_101B) AND (WT_SAG_FEED_CONVEYOR_101A <= WT_SAG_FEED_CONVEYOR_101C)) OR
       ((WT_SAG_FEED_CONVEYOR_101A <= WT_SAG_FEED_CONVEYOR_101B) AND (WT_SAG_FEED_CONVEYOR_101A >= WT_SAG_FEED_CONVEYOR_101C)) THEN
        rVoted_FreshFeedRate_tph := WT_SAG_FEED_CONVEYOR_101A;
    ELSIF ((WT_SAG_FEED_CONVEYOR_101B >= WT_SAG_FEED_CONVEYOR_101A) AND (WT_SAG_FEED_CONVEYOR_101B <= WT_SAG_FEED_CONVEYOR_101C)) OR
          ((WT_SAG_FEED_CONVEYOR_101B <= WT_SAG_FEED_CONVEYOR_101A) AND (WT_SAG_FEED_CONVEYOR_101B >= WT_SAG_FEED_CONVEYOR_101C)) THEN
        rVoted_FreshFeedRate_tph := WT_SAG_FEED_CONVEYOR_101B;
    ELSE
        rVoted_FreshFeedRate_tph := WT_SAG_FEED_CONVEYOR_101C;
    END_IF;
ELSIF bHealth_WT_Feed_A AND bHealth_WT_Feed_B THEN
    bDegraded_WT_Feed := TRUE;
    rVoted_FreshFeedRate_tph := (WT_SAG_FEED_CONVEYOR_101A + WT_SAG_FEED_CONVEYOR_101B) * 0.5;
ELSIF bHealth_WT_Feed_B AND bHealth_WT_Feed_C THEN
    bDegraded_WT_Feed := TRUE;
    rVoted_FreshFeedRate_tph := (WT_SAG_FEED_CONVEYOR_101B + WT_SAG_FEED_CONVEYOR_101C) * 0.5;
ELSIF bHealth_WT_Feed_A AND bHealth_WT_Feed_C THEN
    bDegraded_WT_Feed := TRUE;
    rVoted_FreshFeedRate_tph := (WT_SAG_FEED_CONVEYOR_101A + WT_SAG_FEED_CONVEYOR_101C) * 0.5;
ELSIF bHealth_WT_Feed_A THEN
    rVoted_FreshFeedRate_tph := WT_SAG_FEED_CONVEYOR_101A;
ELSIF bHealth_WT_Feed_B THEN
    rVoted_FreshFeedRate_tph := WT_SAG_FEED_CONVEYOR_101B;
ELSIF bHealth_WT_Feed_C THEN
    rVoted_FreshFeedRate_tph := WT_SAG_FEED_CONVEYOR_101C;
END_IF;

bGracefulDegradationActive := bDegraded_PT_Inlet OR bDegraded_PT_Outlet OR bDegraded_AIT_Toe OR bDegraded_AIT_Shldr OR
                              bDegraded_LT_Sump OR bDegraded_DT_Dens OR bDegraded_PT_Manif OR bDegraded_ST_RPM OR
                              bDegraded_IT_MW OR bDegraded_WT_Feed;
"""

print("TMR module loaded.")
