# Section 2: Matrix Initialization and Phase 1 2oo3 TMR Voting Logic

def get_sec2():
    return """
(* =====================================================================================================================
 * INITIALIZATION: DISCRETE STATE-SPACE MATRICES & MPC PENALTY ARRAYS (FIRST SCAN DETERMINISTIC SETUP)
 * ===================================================================================================================== *)
IF NOT bMatricesInitialized THEN
    (* 1. Initialize Discrete System State Transition Matrix A (8x8) at T_s = 20 ms *)
    FOR nLoop_i := 1 TO 8 DO
        FOR nLoop_j := 1 TO 8 DO
            aA[nLoop_i, nLoop_j] := 0.0;
            aC[nLoop_i, nLoop_j] := 0.0;
        END_FOR;
    END_FOR;

    (* Diagonal entries representing open-loop stable discrete decay poles *)
    aA[1, 1] := 0.9620; (* x1: Extruder Melt Pressure relaxation time constant tau = 0.52 s *)
    aA[2, 2] := 0.9910; (* x2: Extruder Melt Temperature thermal inertia tau = 2.22 s *)
    aA[3, 3] := 0.9840; (* x3: Catenary Sag dynamic swing damping tau = 1.25 s *)
    aA[4, 4] := 0.9950; (* x4: Radiant Heating Zone 1 thermal inertia tau = 4.00 s *)
    aA[5, 5] := 0.9780; (* x5: Tube N2 Overpressure pneumatic buffer tau = 0.91 s *)
    aA[6, 6] := 0.9550; (* x6: Quench Leg Hydrostatic boundary seal fluidic level tau = 0.44 s *)
    aA[7, 7] := 0.9680; (* x7: Haul-Off Caterpillar line tension mechanical elasticity tau = 0.62 s *)
    aA[8, 8] := 0.9820; (* x8: Ultrasonic wall thickness crosshead volumetric relaxation tau = 1.11 s *)

    (* Off-diagonal cross-coupling physics *)
    aA[1, 2] := -0.0420; (* Melt temperature thermal thinning lowers melt pressure *)
    aA[3, 7] := -0.0035; (* Haul-off tension surge directly decreases catenary sag *)
    aA[3, 4] :=  0.0018; (* Radiant thermal expansion elongates cable, increasing sag *)
    aA[5, 6] := -0.0022; (* Hydrostatic quench water level rise compresses nitrogen gas volume *)
    aA[6, 5] :=  0.0045; (* Nitrogen pressure rise depresses quench water boundary level *)
    aA[8, 1] :=  0.0012; (* Extruder melt pressure surge increases die swell & wall thickness *)
    aA[8, 7] := -0.0016; (* Line tension pulling stretch draws down insulation wall thickness *)

    (* 2. Initialize Discrete Actuator Input Coupling Matrix B (8x7) *)
    FOR nLoop_i := 1 TO 8 DO
        FOR nLoop_j := 1 TO 7 DO
            aB[nLoop_i, nLoop_j] := 0.0;
            aD[nLoop_i, nLoop_j] := 0.0;
        END_FOR;
    END_FOR;

    (* Control coupling coefficients: B[state, control] *)
    aB[1, 1] :=  0.0840; (* u1: Extruder screw RPM directly builds melt pressure [bar/RPM] *)
    aB[2, 1] :=  0.0065; (* u1: Extruder screw shear dissipation heats polymer melt [deg C/RPM] *)
    aB[3, 2] := -0.0245; (* u2: Haul-off capstan speed trim tightens catenary line [mm/(m/min)] *)
    aB[3, 7] := -0.0480; (* u7: Capstan tension trim pulls out catenary sag [mm/kN] *)
    aB[4, 3] :=  0.0520; (* u3: Radiant heater SCR duty raises zone 1 curing temp [deg C/%] *)
    aB[5, 4] :=  0.0380; (* u4: N2 injection valve pressurizes 150m tube [bar/%] *)
    aB[5, 5] := -0.0410; (* u5: N2 exhaust blowdown valve depressurizes tube [bar/%] *)
    aB[6, 6] :=  0.0650; (* u6: Quench water inflow valve elevates hydrostatic seal [mm/%] *)
    aB[7, 2] :=  0.0920; (* u2: Haul-off speed increase elevates line tension [kN/(m/min)] *)
    aB[7, 7] :=  0.1450; (* u7: Capstan servo torque directly modulates line tension [kN/kN] *)
    aB[8, 1] :=  0.0085; (* u1: Extruder screw RPM elevates insulation wall thickness [mm/RPM] *)
    aB[8, 2] := -0.0150; (* u2: Line speed acceleration draws down wall thickness [mm/(m/min)] *)

    (* 3. Initialize Measurement Observation Matrix C (8x8) and Feedthrough D (8x7) *)
    FOR nLoop_i := 1 TO 8 DO
        aC[nLoop_i, nLoop_i] := 1.0; (* Direct unity state observation *)
    END_FOR;

    (* 4. Model Predictive Control (MPC) Cost Weighting Diagonals *)
    aQ_Weight[1] := 2.50;   (* x1: Melt pressure penalty *)
    aQ_Weight[2] := 1.80;   (* x2: Melt temperature penalty *)
    aQ_Weight[3] := 15.00;  (* x3: Catenary sag tracking error heavily penalized to avoid tube wall contact! *)
    aQ_Weight[4] := 4.20;   (* x4: Radiant curing temperature penalty *)
    aQ_Weight[5] := 8.50;   (* x5: Nitrogen tube overpressure penalty *)
    aQ_Weight[6] := 6.00;   (* x6: Hydrostatic quench water level boundary penalty *)
    aQ_Weight[7] := 12.00;  (* x7: Haul-off line tension oscillation penalty *)
    aQ_Weight[8] := 18.00;  (* x8: Insulation wall thickness dimensional tolerance penalty *)

    aR_Weight[1] := 0.45;   (* u1: Screw RPM command penalty *)
    aR_Weight[2] := 1.20;   (* u2: Line speed trim penalty *)
    aR_Weight[3] := 0.25;   (* u3: Heater SCR duty penalty *)
    aR_Weight[4] := 0.35;   (* u4: N2 injection valve penalty *)
    aR_Weight[5] := 0.35;   (* u5: N2 vent valve penalty *)
    aR_Weight[6] := 0.40;   (* u6: Quench water valve penalty *)
    aR_Weight[7] := 0.85;   (* u7: Capstan tension trim penalty *)

    aS_Weight[1] := 1.50;   (* Slew rate penalty for screw RPM *)
    aS_Weight[2] := 3.50;   (* Slew rate penalty for line speed trim *)
    aS_Weight[3] := 0.80;   (* Slew rate penalty for heater SCR *)
    aS_Weight[4] := 1.20;   (* Slew rate penalty for N2 injection *)
    aS_Weight[5] := 1.20;   (* Slew rate penalty for N2 exhaust *)
    aS_Weight[6] := 1.40;   (* Slew rate penalty for water inflow *)
    aS_Weight[7] := 2.80;   (* Slew rate penalty for tension trim *)

    FOR nLoop_i := 1 TO 8 DO
        aP_TerminalWeight[nLoop_i] := aQ_Weight[nLoop_i] * 3.20; (* Terminal horizon cost Lyapunov weighting *)
    END_FOR;

    (* 5. Actuator Hard Saturation & Slew Limits *)
    au_min[1] := 0.0;     au_max[1] := 75.0;    adelta_u_max[1] := 0.50;  (* Screw RPM [0..75 RPM] *)
    au_min[2] := -2.50;   au_max[2] := 2.50;    adelta_u_max[2] := 0.08;  (* Line speed trim [-2.5..+2.5 m/min] *)
    au_min[3] := 0.0;     au_max[3] := 100.0;   adelta_u_max[3] := 1.20;  (* SCR Duty [0..100%] *)
    au_min[4] := 0.0;     au_max[4] := 100.0;   adelta_u_max[4] := 2.50;  (* N2 Inj Valve [0..100%] *)
    au_min[5] := 0.0;     au_max[5] := 100.0;   adelta_u_max[5] := 2.50;  (* N2 Vent Valve [0..100%] *)
    au_min[6] := 0.0;     au_max[6] := 100.0;   adelta_u_max[6] := 2.00;  (* Water Valve [0..100%] *)
    au_min[7] := -15.0;   au_max[7] := 15.0;    adelta_u_max[7] := 0.60;  (* Tension Trim [-15..+15 kN] *)

    bMatricesInitialized := TRUE;
END_IF;

(* =====================================================================================================================
 * PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) VOTING & SENSOR HEALTH DIAGNOSTICS (11 FIELD GROUPS)
 * ===================================================================================================================== *)
(* Reset sensor health bitmasks *)
dwSensorHealthMask_Low  := 16#0000_0000;
dwSensorHealthMask_High := 16#0000_0000;

(* --- GROUP 1: PT_EXTRUDER_MELT_PRESS_101 (XLPE Melt Pressure at Die Adapter, 0..500 bar) --- *)
rTempDiffAB := ABS(PT_EXTRUDER_MELT_PRESS_101A - PT_EXTRUDER_MELT_PRESS_101B);
rTempDiffBC := ABS(PT_EXTRUDER_MELT_PRESS_101B - PT_EXTRUDER_MELT_PRESS_101C);
rTempDiffCA := ABS(PT_EXTRUDER_MELT_PRESS_101C - PT_EXTRUDER_MELT_PRESS_101A);

IF (rTempDiffAB > c_rTol_MeltPress_bar) OR (rTempDiffBC > c_rTol_MeltPress_bar) OR (rTempDiffCA > c_rTol_MeltPress_bar) THEN
    rTimer_MeltPress_Disc_s := rTimer_MeltPress_Disc_s + c_rTs;
    IF rTimer_MeltPress_Disc_s >= c_rTMR_PersistencyTimeout_s THEN
        IF (rTempDiffAB > c_rTol_MeltPress_bar) AND (rTempDiffCA > c_rTol_MeltPress_bar) THEN
            bIso_MeltPress_ChA := TRUE;
        END_IF;
        IF (rTempDiffAB > c_rTol_MeltPress_bar) AND (rTempDiffBC > c_rTol_MeltPress_bar) THEN
            bIso_MeltPress_ChB := TRUE;
        END_IF;
        IF (rTempDiffBC > c_rTol_MeltPress_bar) AND (rTempDiffCA > c_rTol_MeltPress_bar) THEN
            bIso_MeltPress_ChC := TRUE;
        END_IF;
    END_IF;
ELSE
    rTimer_MeltPress_Disc_s := 0.0;
END_IF;

IF bFaultReset THEN
    bIso_MeltPress_ChA := FALSE;
    bIso_MeltPress_ChB := FALSE;
    bIso_MeltPress_ChC := FALSE;
END_IF;

IF (NOT bIso_MeltPress_ChA) AND (NOT bIso_MeltPress_ChB) AND (NOT bIso_MeltPress_ChC) THEN
    (* All 3 channels healthy: take true median value *)
    IF ((PT_EXTRUDER_MELT_PRESS_101A >= PT_EXTRUDER_MELT_PRESS_101B) AND (PT_EXTRUDER_MELT_PRESS_101A <= PT_EXTRUDER_MELT_PRESS_101C)) OR
       ((PT_EXTRUDER_MELT_PRESS_101A <= PT_EXTRUDER_MELT_PRESS_101B) AND (PT_EXTRUDER_MELT_PRESS_101A >= PT_EXTRUDER_MELT_PRESS_101C)) THEN
        rVoted_ExtruderMeltPress_bar := PT_EXTRUDER_MELT_PRESS_101A;
    ELSIF ((PT_EXTRUDER_MELT_PRESS_101B >= PT_EXTRUDER_MELT_PRESS_101A) AND (PT_EXTRUDER_MELT_PRESS_101B <= PT_EXTRUDER_MELT_PRESS_101C)) OR
          ((PT_EXTRUDER_MELT_PRESS_101B <= PT_EXTRUDER_MELT_PRESS_101A) AND (PT_EXTRUDER_MELT_PRESS_101B >= PT_EXTRUDER_MELT_PRESS_101C)) THEN
        rVoted_ExtruderMeltPress_bar := PT_EXTRUDER_MELT_PRESS_101B;
    ELSE
        rVoted_ExtruderMeltPress_bar := PT_EXTRUDER_MELT_PRESS_101C;
    END_IF;
ELSIF bIso_MeltPress_ChA AND (NOT bIso_MeltPress_ChB) AND (NOT bIso_MeltPress_ChC) THEN
    rVoted_ExtruderMeltPress_bar := 0.5 * (PT_EXTRUDER_MELT_PRESS_101B + PT_EXTRUDER_MELT_PRESS_101C);
ELSIF bIso_MeltPress_ChB AND (NOT bIso_MeltPress_ChA) AND (NOT bIso_MeltPress_ChC) THEN
    rVoted_ExtruderMeltPress_bar := 0.5 * (PT_EXTRUDER_MELT_PRESS_101A + PT_EXTRUDER_MELT_PRESS_101C);
ELSIF bIso_MeltPress_ChC AND (NOT bIso_MeltPress_ChA) AND (NOT bIso_MeltPress_ChB) THEN
    rVoted_ExtruderMeltPress_bar := 0.5 * (PT_EXTRUDER_MELT_PRESS_101A + PT_EXTRUDER_MELT_PRESS_101B);
ELSIF (NOT bIso_MeltPress_ChA) THEN
    rVoted_ExtruderMeltPress_bar := PT_EXTRUDER_MELT_PRESS_101A;
ELSIF (NOT bIso_MeltPress_ChB) THEN
    rVoted_ExtruderMeltPress_bar := PT_EXTRUDER_MELT_PRESS_101B;
ELSIF (NOT bIso_MeltPress_ChC) THEN
    rVoted_ExtruderMeltPress_bar := PT_EXTRUDER_MELT_PRESS_101C;
ELSE
    bAlarm_TMR_MajorDivergence := TRUE;
END_IF;

IF bIso_MeltPress_ChA THEN dwSensorHealthMask_Low := dwSensorHealthMask_Low OR 16#0000_0001; END_IF;
IF bIso_MeltPress_ChB THEN dwSensorHealthMask_Low := dwSensorHealthMask_Low OR 16#0000_0002; END_IF;
IF bIso_MeltPress_ChC THEN dwSensorHealthMask_Low := dwSensorHealthMask_Low OR 16#0000_0004; END_IF;

(* --- GROUP 2: TT_EXTRUDER_MELT_TEMP_102 (XLPE Melt Temperature, 0..300 deg C) --- *)
rTempDiffAB := ABS(TT_EXTRUDER_MELT_TEMP_102A - TT_EXTRUDER_MELT_TEMP_102B);
rTempDiffBC := ABS(TT_EXTRUDER_MELT_TEMP_102B - TT_EXTRUDER_MELT_TEMP_102C);
rTempDiffCA := ABS(TT_EXTRUDER_MELT_TEMP_102C - TT_EXTRUDER_MELT_TEMP_102A);

IF (rTempDiffAB > c_rTol_MeltTemp_degC) OR (rTempDiffBC > c_rTol_MeltTemp_degC) OR (rTempDiffCA > c_rTol_MeltTemp_degC) THEN
    rTimer_MeltTemp_Disc_s := rTimer_MeltTemp_Disc_s + c_rTs;
    IF rTimer_MeltTemp_Disc_s >= c_rTMR_PersistencyTimeout_s THEN
        IF (rTempDiffAB > c_rTol_MeltTemp_degC) AND (rTempDiffCA > c_rTol_MeltTemp_degC) THEN
            bIso_MeltTemp_ChA := TRUE;
        END_IF;
        IF (rTempDiffAB > c_rTol_MeltTemp_degC) AND (rTempDiffBC > c_rTol_MeltTemp_degC) THEN
            bIso_MeltTemp_ChB := TRUE;
        END_IF;
        IF (rTempDiffBC > c_rTol_MeltTemp_degC) AND (rTempDiffCA > c_rTol_MeltTemp_degC) THEN
            bIso_MeltTemp_ChC := TRUE;
        END_IF;
    END_IF;
ELSE
    rTimer_MeltTemp_Disc_s := 0.0;
END_IF;

IF bFaultReset THEN
    bIso_MeltTemp_ChA := FALSE;
    bIso_MeltTemp_ChB := FALSE;
    bIso_MeltTemp_ChC := FALSE;
END_IF;

IF (NOT bIso_MeltTemp_ChA) AND (NOT bIso_MeltTemp_ChB) AND (NOT bIso_MeltTemp_ChC) THEN
    IF ((TT_EXTRUDER_MELT_TEMP_102A >= TT_EXTRUDER_MELT_TEMP_102B) AND (TT_EXTRUDER_MELT_TEMP_102A <= TT_EXTRUDER_MELT_TEMP_102C)) OR
       ((TT_EXTRUDER_MELT_TEMP_102A <= TT_EXTRUDER_MELT_TEMP_102B) AND (TT_EXTRUDER_MELT_TEMP_102A >= TT_EXTRUDER_MELT_TEMP_102C)) THEN
        rVoted_ExtruderMeltTemp_degC := TT_EXTRUDER_MELT_TEMP_102A;
    ELSIF ((TT_EXTRUDER_MELT_TEMP_102B >= TT_EXTRUDER_MELT_TEMP_102A) AND (TT_EXTRUDER_MELT_TEMP_102B <= TT_EXTRUDER_MELT_TEMP_102C)) OR
          ((TT_EXTRUDER_MELT_TEMP_102B <= TT_EXTRUDER_MELT_TEMP_102A) AND (TT_EXTRUDER_MELT_TEMP_102B >= TT_EXTRUDER_MELT_TEMP_102C)) THEN
        rVoted_ExtruderMeltTemp_degC := TT_EXTRUDER_MELT_TEMP_102B;
    ELSE
        rVoted_ExtruderMeltTemp_degC := TT_EXTRUDER_MELT_TEMP_102C;
    END_IF;
ELSIF bIso_MeltTemp_ChA AND (NOT bIso_MeltTemp_ChB) AND (NOT bIso_MeltTemp_ChC) THEN
    rVoted_ExtruderMeltTemp_degC := 0.5 * (TT_EXTRUDER_MELT_TEMP_102B + TT_EXTRUDER_MELT_TEMP_102C);
ELSIF bIso_MeltTemp_ChB AND (NOT bIso_MeltTemp_ChA) AND (NOT bIso_MeltTemp_ChC) THEN
    rVoted_ExtruderMeltTemp_degC := 0.5 * (TT_EXTRUDER_MELT_TEMP_102A + TT_EXTRUDER_MELT_TEMP_102C);
ELSIF bIso_MeltTemp_ChC AND (NOT bIso_MeltTemp_ChA) AND (NOT bIso_MeltTemp_ChB) THEN
    rVoted_ExtruderMeltTemp_degC := 0.5 * (TT_EXTRUDER_MELT_TEMP_102A + TT_EXTRUDER_MELT_TEMP_102B);
ELSIF (NOT bIso_MeltTemp_ChA) THEN
    rVoted_ExtruderMeltTemp_degC := TT_EXTRUDER_MELT_TEMP_102A;
ELSIF (NOT bIso_MeltTemp_ChB) THEN
    rVoted_ExtruderMeltTemp_degC := TT_EXTRUDER_MELT_TEMP_102B;
ELSIF (NOT bIso_MeltTemp_ChC) THEN
    rVoted_ExtruderMeltTemp_degC := TT_EXTRUDER_MELT_TEMP_102C;
ELSE
    bAlarm_TMR_MajorDivergence := TRUE;
END_IF;

IF bIso_MeltTemp_ChA THEN dwSensorHealthMask_Low := dwSensorHealthMask_Low OR 16#0000_0008; END_IF;
IF bIso_MeltTemp_ChB THEN dwSensorHealthMask_Low := dwSensorHealthMask_Low OR 16#0000_0010; END_IF;
IF bIso_MeltTemp_ChC THEN dwSensorHealthMask_Low := dwSensorHealthMask_Low OR 16#0000_0020; END_IF;

(* --- GROUP 3: ZT_CATENARY_SAG_XRAY_201 (Non-Contact X-Ray Sag Position, 100..200 mm) --- *)
rTempDiffAB := ABS(ZT_CATENARY_SAG_XRAY_201A - ZT_CATENARY_SAG_XRAY_201B);
rTempDiffBC := ABS(ZT_CATENARY_SAG_XRAY_201B - ZT_CATENARY_SAG_XRAY_201C);
rTempDiffCA := ABS(ZT_CATENARY_SAG_XRAY_201C - ZT_CATENARY_SAG_XRAY_201A);

IF (rTempDiffAB > c_rTol_CatenarySag_mm) OR (rTempDiffBC > c_rTol_CatenarySag_mm) OR (rTempDiffCA > c_rTol_CatenarySag_mm) THEN
    rTimer_CatenarySag_Disc_s := rTimer_CatenarySag_Disc_s + c_rTs;
    IF rTimer_CatenarySag_Disc_s >= c_rTMR_PersistencyTimeout_s THEN
        IF (rTempDiffAB > c_rTol_CatenarySag_mm) AND (rTempDiffCA > c_rTol_CatenarySag_mm) THEN
            bIso_CatenarySag_ChA := TRUE;
        END_IF;
        IF (rTempDiffAB > c_rTol_CatenarySag_mm) AND (rTempDiffBC > c_rTol_CatenarySag_mm) THEN
            bIso_CatenarySag_ChB := TRUE;
        END_IF;
        IF (rTempDiffBC > c_rTol_CatenarySag_mm) AND (rTempDiffCA > c_rTol_CatenarySag_mm) THEN
            bIso_CatenarySag_ChC := TRUE;
        END_IF;
    END_IF;
ELSE
    rTimer_CatenarySag_Disc_s := 0.0;
END_IF;

IF bFaultReset THEN
    bIso_CatenarySag_ChA := FALSE;
    bIso_CatenarySag_ChB := FALSE;
    bIso_CatenarySag_ChC := FALSE;
END_IF;

IF (NOT bIso_CatenarySag_ChA) AND (NOT bIso_CatenarySag_ChB) AND (NOT bIso_CatenarySag_ChC) THEN
    IF ((ZT_CATENARY_SAG_XRAY_201A >= ZT_CATENARY_SAG_XRAY_201B) AND (ZT_CATENARY_SAG_XRAY_201A <= ZT_CATENARY_SAG_XRAY_201C)) OR
       ((ZT_CATENARY_SAG_XRAY_201A <= ZT_CATENARY_SAG_XRAY_201B) AND (ZT_CATENARY_SAG_XRAY_201A >= ZT_CATENARY_SAG_XRAY_201C)) THEN
        rVoted_CatenarySag_mm := ZT_CATENARY_SAG_XRAY_201A;
    ELSIF ((ZT_CATENARY_SAG_XRAY_201B >= ZT_CATENARY_SAG_XRAY_201A) AND (ZT_CATENARY_SAG_XRAY_201B <= ZT_CATENARY_SAG_XRAY_201C)) OR
          ((ZT_CATENARY_SAG_XRAY_201B <= ZT_CATENARY_SAG_XRAY_201A) AND (ZT_CATENARY_SAG_XRAY_201B >= ZT_CATENARY_SAG_XRAY_201C)) THEN
        rVoted_CatenarySag_mm := ZT_CATENARY_SAG_XRAY_201B;
    ELSE
        rVoted_CatenarySag_mm := ZT_CATENARY_SAG_XRAY_201C;
    END_IF;
ELSIF bIso_CatenarySag_ChA AND (NOT bIso_CatenarySag_ChB) AND (NOT bIso_CatenarySag_ChC) THEN
    rVoted_CatenarySag_mm := 0.5 * (ZT_CATENARY_SAG_XRAY_201B + ZT_CATENARY_SAG_XRAY_201C);
ELSIF bIso_CatenarySag_ChB AND (NOT bIso_CatenarySag_ChA) AND (NOT bIso_CatenarySag_ChC) THEN
    rVoted_CatenarySag_mm := 0.5 * (ZT_CATENARY_SAG_XRAY_201A + ZT_CATENARY_SAG_XRAY_201C);
ELSIF bIso_CatenarySag_ChC AND (NOT bIso_CatenarySag_ChA) AND (NOT bIso_CatenarySag_ChB) THEN
    rVoted_CatenarySag_mm := 0.5 * (ZT_CATENARY_SAG_XRAY_201A + ZT_CATENARY_SAG_XRAY_201B);
ELSIF (NOT bIso_CatenarySag_ChA) THEN
    rVoted_CatenarySag_mm := ZT_CATENARY_SAG_XRAY_201A;
ELSIF (NOT bIso_CatenarySag_ChB) THEN
    rVoted_CatenarySag_mm := ZT_CATENARY_SAG_XRAY_201B;
ELSIF (NOT bIso_CatenarySag_ChC) THEN
    rVoted_CatenarySag_mm := ZT_CATENARY_SAG_XRAY_201C;
ELSE
    bAlarm_TMR_MajorDivergence := TRUE;
END_IF;

IF bIso_CatenarySag_ChA THEN dwSensorHealthMask_Low := dwSensorHealthMask_Low OR 16#0000_0040; END_IF;
IF bIso_CatenarySag_ChB THEN dwSensorHealthMask_Low := dwSensorHealthMask_Low OR 16#0000_0080; END_IF;
IF bIso_CatenarySag_ChC THEN dwSensorHealthMask_Low := dwSensorHealthMask_Low OR 16#0000_0100; END_IF;

(* --- GROUP 4: PT_TUBE_N2_PRESS_301 (150m Vulcanization Tube N2 Pressure, 0..16 bar) --- *)
rTempDiffAB := ABS(PT_TUBE_N2_PRESS_301A - PT_TUBE_N2_PRESS_301B);
rTempDiffBC := ABS(PT_TUBE_N2_PRESS_301B - PT_TUBE_N2_PRESS_301C);
rTempDiffCA := ABS(PT_TUBE_N2_PRESS_301C - PT_TUBE_N2_PRESS_301A);

IF (rTempDiffAB > c_rTol_TubeN2Press_bar) OR (rTempDiffBC > c_rTol_TubeN2Press_bar) OR (rTempDiffCA > c_rTol_TubeN2Press_bar) THEN
    rTimer_TubeN2Press_Disc_s := rTimer_TubeN2Press_Disc_s + c_rTs;
    IF rTimer_TubeN2Press_Disc_s >= c_rTMR_PersistencyTimeout_s THEN
        IF (rTempDiffAB > c_rTol_TubeN2Press_bar) AND (rTempDiffCA > c_rTol_TubeN2Press_bar) THEN
            bIso_TubeN2Press_ChA := TRUE;
        END_IF;
        IF (rTempDiffAB > c_rTol_TubeN2Press_bar) AND (rTempDiffBC > c_rTol_TubeN2Press_bar) THEN
            bIso_TubeN2Press_ChB := TRUE;
        END_IF;
        IF (rTempDiffBC > c_rTol_TubeN2Press_bar) AND (rTempDiffCA > c_rTol_TubeN2Press_bar) THEN
            bIso_TubeN2Press_ChC := TRUE;
        END_IF;
    END_IF;
ELSE
    rTimer_TubeN2Press_Disc_s := 0.0;
END_IF;

IF bFaultReset THEN
    bIso_TubeN2Press_ChA := FALSE;
    bIso_TubeN2Press_ChB := FALSE;
    bIso_TubeN2Press_ChC := FALSE;
END_IF;

IF (NOT bIso_TubeN2Press_ChA) AND (NOT bIso_TubeN2Press_ChB) AND (NOT bIso_TubeN2Press_ChC) THEN
    IF ((PT_TUBE_N2_PRESS_301A >= PT_TUBE_N2_PRESS_301B) AND (PT_TUBE_N2_PRESS_301A <= PT_TUBE_N2_PRESS_301C)) OR
       ((PT_TUBE_N2_PRESS_301A <= PT_TUBE_N2_PRESS_301B) AND (PT_TUBE_N2_PRESS_301A >= PT_TUBE_N2_PRESS_301C)) THEN
        rVoted_TubeN2Press_bar := PT_TUBE_N2_PRESS_301A;
    ELSIF ((PT_TUBE_N2_PRESS_301B >= PT_TUBE_N2_PRESS_301A) AND (PT_TUBE_N2_PRESS_301B <= PT_TUBE_N2_PRESS_301C)) OR
          ((PT_TUBE_N2_PRESS_301B <= PT_TUBE_N2_PRESS_301A) AND (PT_TUBE_N2_PRESS_301B >= PT_TUBE_N2_PRESS_301C)) THEN
        rVoted_TubeN2Press_bar := PT_TUBE_N2_PRESS_301B;
    ELSE
        rVoted_TubeN2Press_bar := PT_TUBE_N2_PRESS_301C;
    END_IF;
ELSIF bIso_TubeN2Press_ChA AND (NOT bIso_TubeN2Press_ChB) AND (NOT bIso_TubeN2Press_ChC) THEN
    rVoted_TubeN2Press_bar := 0.5 * (PT_TUBE_N2_PRESS_301B + PT_TUBE_N2_PRESS_301C);
ELSIF bIso_TubeN2Press_ChB AND (NOT bIso_TubeN2Press_ChA) AND (NOT bIso_TubeN2Press_ChC) THEN
    rVoted_TubeN2Press_bar := 0.5 * (PT_TUBE_N2_PRESS_301A + PT_TUBE_N2_PRESS_301C);
ELSIF bIso_TubeN2Press_ChC AND (NOT bIso_TubeN2Press_ChA) AND (NOT bIso_TubeN2Press_ChB) THEN
    rVoted_TubeN2Press_bar := 0.5 * (PT_TUBE_N2_PRESS_301A + PT_TUBE_N2_PRESS_301B);
ELSIF (NOT bIso_TubeN2Press_ChA) THEN
    rVoted_TubeN2Press_bar := PT_TUBE_N2_PRESS_301A;
ELSIF (NOT bIso_TubeN2Press_ChB) THEN
    rVoted_TubeN2Press_bar := PT_TUBE_N2_PRESS_301B;
ELSIF (NOT bIso_TubeN2Press_ChC) THEN
    rVoted_TubeN2Press_bar := PT_TUBE_N2_PRESS_301C;
ELSE
    bAlarm_TMR_MajorDivergence := TRUE;
END_IF;

IF bIso_TubeN2Press_ChA THEN dwSensorHealthMask_Low := dwSensorHealthMask_Low OR 16#0000_0200; END_IF;
IF bIso_TubeN2Press_ChB THEN dwSensorHealthMask_Low := dwSensorHealthMask_Low OR 16#0000_0400; END_IF;
IF bIso_TubeN2Press_ChC THEN dwSensorHealthMask_Low := dwSensorHealthMask_Low OR 16#0000_0800; END_IF;

(* --- GROUP 5: TE_TUBE_ZONE1_TEMP_401 (Radiant Heating Zone 1 Temp, 0..500 deg C) --- *)
rTempDiffAB := ABS(TE_TUBE_ZONE1_TEMP_401A - TE_TUBE_ZONE1_TEMP_401B);
rTempDiffBC := ABS(TE_TUBE_ZONE1_TEMP_401B - TE_TUBE_ZONE1_TEMP_401C);
rTempDiffCA := ABS(TE_TUBE_ZONE1_TEMP_401C - TE_TUBE_ZONE1_TEMP_401A);

IF (rTempDiffAB > c_rTol_Zone1Temp_degC) OR (rTempDiffBC > c_rTol_Zone1Temp_degC) OR (rTempDiffCA > c_rTol_Zone1Temp_degC) THEN
    rTimer_Zone1Temp_Disc_s := rTimer_Zone1Temp_Disc_s + c_rTs;
    IF rTimer_Zone1Temp_Disc_s >= c_rTMR_PersistencyTimeout_s THEN
        IF (rTempDiffAB > c_rTol_Zone1Temp_degC) AND (rTempDiffCA > c_rTol_Zone1Temp_degC) THEN
            bIso_Zone1Temp_ChA := TRUE;
        END_IF;
        IF (rTempDiffAB > c_rTol_Zone1Temp_degC) AND (rTempDiffBC > c_rTol_Zone1Temp_degC) THEN
            bIso_Zone1Temp_ChB := TRUE;
        END_IF;
        IF (rTempDiffBC > c_rTol_Zone1Temp_degC) AND (rTempDiffCA > c_rTol_Zone1Temp_degC) THEN
            bIso_Zone1Temp_ChC := TRUE;
        END_IF;
    END_IF;
ELSE
    rTimer_Zone1Temp_Disc_s := 0.0;
END_IF;

IF bFaultReset THEN
    bIso_Zone1Temp_ChA := FALSE;
    bIso_Zone1Temp_ChB := FALSE;
    bIso_Zone1Temp_ChC := FALSE;
END_IF;

IF (NOT bIso_Zone1Temp_ChA) AND (NOT bIso_Zone1Temp_ChB) AND (NOT bIso_Zone1Temp_ChC) THEN
    IF ((TE_TUBE_ZONE1_TEMP_401A >= TE_TUBE_ZONE1_TEMP_401B) AND (TE_TUBE_ZONE1_TEMP_401A <= TE_TUBE_ZONE1_TEMP_401C)) OR
       ((TE_TUBE_ZONE1_TEMP_401A <= TE_TUBE_ZONE1_TEMP_401B) AND (TE_TUBE_ZONE1_TEMP_401A >= TE_TUBE_ZONE1_TEMP_401C)) THEN
        rVoted_Zone1Temp_degC := TE_TUBE_ZONE1_TEMP_401A;
    ELSIF ((TE_TUBE_ZONE1_TEMP_401B >= TE_TUBE_ZONE1_TEMP_401A) AND (TE_TUBE_ZONE1_TEMP_401B <= TE_TUBE_ZONE1_TEMP_401C)) OR
          ((TE_TUBE_ZONE1_TEMP_401B <= TE_TUBE_ZONE1_TEMP_401A) AND (TE_TUBE_ZONE1_TEMP_401B >= TE_TUBE_ZONE1_TEMP_401C)) THEN
        rVoted_Zone1Temp_degC := TE_TUBE_ZONE1_TEMP_401B;
    ELSE
        rVoted_Zone1Temp_degC := TE_TUBE_ZONE1_TEMP_401C;
    END_IF;
ELSIF bIso_Zone1Temp_ChA AND (NOT bIso_Zone1Temp_ChB) AND (NOT bIso_Zone1Temp_ChC) THEN
    rVoted_Zone1Temp_degC := 0.5 * (TE_TUBE_ZONE1_TEMP_401B + TE_TUBE_ZONE1_TEMP_401C);
ELSIF bIso_Zone1Temp_ChB AND (NOT bIso_Zone1Temp_ChA) AND (NOT bIso_Zone1Temp_ChC) THEN
    rVoted_Zone1Temp_degC := 0.5 * (TE_TUBE_ZONE1_TEMP_401A + TE_TUBE_ZONE1_TEMP_401C);
ELSIF bIso_Zone1Temp_ChC AND (NOT bIso_Zone1Temp_ChA) AND (NOT bIso_Zone1Temp_ChB) THEN
    rVoted_Zone1Temp_degC := 0.5 * (TE_TUBE_ZONE1_TEMP_401A + TE_TUBE_ZONE1_TEMP_401B);
ELSIF (NOT bIso_Zone1Temp_ChA) THEN
    rVoted_Zone1Temp_degC := TE_TUBE_ZONE1_TEMP_401A;
ELSIF (NOT bIso_Zone1Temp_ChB) THEN
    rVoted_Zone1Temp_degC := TE_TUBE_ZONE1_TEMP_401B;
ELSIF (NOT bIso_Zone1Temp_ChC) THEN
    rVoted_Zone1Temp_degC := TE_TUBE_ZONE1_TEMP_401C;
ELSE
    bAlarm_TMR_MajorDivergence := TRUE;
END_IF;

IF bIso_Zone1Temp_ChA THEN dwSensorHealthMask_Low := dwSensorHealthMask_Low OR 16#0000_1000; END_IF;
IF bIso_Zone1Temp_ChB THEN dwSensorHealthMask_Low := dwSensorHealthMask_Low OR 16#0000_2000; END_IF;
IF bIso_Zone1Temp_ChC THEN dwSensorHealthMask_Low := dwSensorHealthMask_Low OR 16#0000_4000; END_IF;

(* --- GROUP 6: TE_TUBE_ZONE2_TEMP_402 (Radiant Heating Zone 2 Temp, 0..500 deg C) --- *)
rTempDiffAB := ABS(TE_TUBE_ZONE2_TEMP_402A - TE_TUBE_ZONE2_TEMP_402B);
rTempDiffBC := ABS(TE_TUBE_ZONE2_TEMP_402B - TE_TUBE_ZONE2_TEMP_402C);
rTempDiffCA := ABS(TE_TUBE_ZONE2_TEMP_402C - TE_TUBE_ZONE2_TEMP_402A);

IF (rTempDiffAB > c_rTol_Zone2Temp_degC) OR (rTempDiffBC > c_rTol_Zone2Temp_degC) OR (rTempDiffCA > c_rTol_Zone2Temp_degC) THEN
    rTimer_Zone2Temp_Disc_s := rTimer_Zone2Temp_Disc_s + c_rTs;
    IF rTimer_Zone2Temp_Disc_s >= c_rTMR_PersistencyTimeout_s THEN
        IF (rTempDiffAB > c_rTol_Zone2Temp_degC) AND (rTempDiffCA > c_rTol_Zone2Temp_degC) THEN
            bIso_Zone2Temp_ChA := TRUE;
        END_IF;
        IF (rTempDiffAB > c_rTol_Zone2Temp_degC) AND (rTempDiffBC > c_rTol_Zone2Temp_degC) THEN
            bIso_Zone2Temp_ChB := TRUE;
        END_IF;
        IF (rTempDiffBC > c_rTol_Zone2Temp_degC) AND (rTempDiffCA > c_rTol_Zone2Temp_degC) THEN
            bIso_Zone2Temp_ChC := TRUE;
        END_IF;
    END_IF;
ELSE
    rTimer_Zone2Temp_Disc_s := 0.0;
END_IF;

IF bFaultReset THEN
    bIso_Zone2Temp_ChA := FALSE;
    bIso_Zone2Temp_ChB := FALSE;
    bIso_Zone2Temp_ChC := FALSE;
END_IF;

IF (NOT bIso_Zone2Temp_ChA) AND (NOT bIso_Zone2Temp_ChB) AND (NOT bIso_Zone2Temp_ChC) THEN
    IF ((TE_TUBE_ZONE2_TEMP_402A >= TE_TUBE_ZONE2_TEMP_402B) AND (TE_TUBE_ZONE2_TEMP_402A <= TE_TUBE_ZONE2_TEMP_402C)) OR
       ((TE_TUBE_ZONE2_TEMP_402A <= TE_TUBE_ZONE2_TEMP_402B) AND (TE_TUBE_ZONE2_TEMP_402A >= TE_TUBE_ZONE2_TEMP_402C)) THEN
        rVoted_Zone2Temp_degC := TE_TUBE_ZONE2_TEMP_402A;
    ELSIF ((TE_TUBE_ZONE2_TEMP_402B >= TE_TUBE_ZONE2_TEMP_402A) AND (TE_TUBE_ZONE2_TEMP_402B <= TE_TUBE_ZONE2_TEMP_402C)) OR
          ((TE_TUBE_ZONE2_TEMP_402B <= TE_TUBE_ZONE2_TEMP_402A) AND (TE_TUBE_ZONE2_TEMP_402B >= TE_TUBE_ZONE2_TEMP_402C)) THEN
        rVoted_Zone2Temp_degC := TE_TUBE_ZONE2_TEMP_402B;
    ELSE
        rVoted_Zone2Temp_degC := TE_TUBE_ZONE2_TEMP_402C;
    END_IF;
ELSIF bIso_Zone2Temp_ChA AND (NOT bIso_Zone2Temp_ChB) AND (NOT bIso_Zone2Temp_ChC) THEN
    rVoted_Zone2Temp_degC := 0.5 * (TE_TUBE_ZONE2_TEMP_402B + TE_TUBE_ZONE2_TEMP_402C);
ELSIF bIso_Zone2Temp_ChB AND (NOT bIso_Zone2Temp_ChA) AND (NOT bIso_Zone2Temp_ChC) THEN
    rVoted_Zone2Temp_degC := 0.5 * (TE_TUBE_ZONE2_TEMP_402A + TE_TUBE_ZONE2_TEMP_402C);
ELSIF bIso_Zone2Temp_ChC AND (NOT bIso_Zone2Temp_ChA) AND (NOT bIso_Zone2Temp_ChB) THEN
    rVoted_Zone2Temp_degC := 0.5 * (TE_TUBE_ZONE2_TEMP_402A + TE_TUBE_ZONE2_TEMP_402B);
ELSIF (NOT bIso_Zone2Temp_ChA) THEN
    rVoted_Zone2Temp_degC := TE_TUBE_ZONE2_TEMP_402A;
ELSIF (NOT bIso_Zone2Temp_ChB) THEN
    rVoted_Zone2Temp_degC := TE_TUBE_ZONE2_TEMP_402B;
ELSIF (NOT bIso_Zone2Temp_ChC) THEN
    rVoted_Zone2Temp_degC := TE_TUBE_ZONE2_TEMP_402C;
ELSE
    bAlarm_TMR_MajorDivergence := TRUE;
END_IF;

IF bIso_Zone2Temp_ChA THEN dwSensorHealthMask_Low := dwSensorHealthMask_Low OR 16#0000_8000; END_IF;
IF bIso_Zone2Temp_ChB THEN dwSensorHealthMask_Low := dwSensorHealthMask_Low OR 16#0001_0000; END_IF;
IF bIso_Zone2Temp_ChC THEN dwSensorHealthMask_Low := dwSensorHealthMask_Low OR 16#0002_0000; END_IF;

(* --- GROUP 7: LT_WATER_QUENCH_LVL_501 (Hydrostatic Quench Water Level, 0..3000 mm) --- *)
rTempDiffAB := ABS(LT_WATER_QUENCH_LVL_501A - LT_WATER_QUENCH_LVL_501B);
rTempDiffBC := ABS(LT_WATER_QUENCH_LVL_501B - LT_WATER_QUENCH_LVL_501C);
rTempDiffCA := ABS(LT_WATER_QUENCH_LVL_501C - LT_WATER_QUENCH_LVL_501A);

IF (rTempDiffAB > c_rTol_QuenchWaterLvl_mm) OR (rTempDiffBC > c_rTol_QuenchWaterLvl_mm) OR (rTempDiffCA > c_rTol_QuenchWaterLvl_mm) THEN
    rTimer_QuenchWaterLvl_Disc_s := rTimer_QuenchWaterLvl_Disc_s + c_rTs;
    IF rTimer_QuenchWaterLvl_Disc_s >= c_rTMR_PersistencyTimeout_s THEN
        IF (rTempDiffAB > c_rTol_QuenchWaterLvl_mm) AND (rTempDiffCA > c_rTol_QuenchWaterLvl_mm) THEN
            bIso_QuenchWaterLvl_ChA := TRUE;
        END_IF;
        IF (rTempDiffAB > c_rTol_QuenchWaterLvl_mm) AND (rTempDiffBC > c_rTol_QuenchWaterLvl_mm) THEN
            bIso_QuenchWaterLvl_ChB := TRUE;
        END_IF;
        IF (rTempDiffBC > c_rTol_QuenchWaterLvl_mm) AND (rTempDiffCA > c_rTol_QuenchWaterLvl_mm) THEN
            bIso_QuenchWaterLvl_ChC := TRUE;
        END_IF;
    END_IF;
ELSE
    rTimer_QuenchWaterLvl_Disc_s := 0.0;
END_IF;

IF bFaultReset THEN
    bIso_QuenchWaterLvl_ChA := FALSE;
    bIso_QuenchWaterLvl_ChB := FALSE;
    bIso_QuenchWaterLvl_ChC := FALSE;
END_IF;

IF (NOT bIso_QuenchWaterLvl_ChA) AND (NOT bIso_QuenchWaterLvl_ChB) AND (NOT bIso_QuenchWaterLvl_ChC) THEN
    IF ((LT_WATER_QUENCH_LVL_501A >= LT_WATER_QUENCH_LVL_501B) AND (LT_WATER_QUENCH_LVL_501A <= LT_WATER_QUENCH_LVL_501C)) OR
       ((LT_WATER_QUENCH_LVL_501A <= LT_WATER_QUENCH_LVL_501B) AND (LT_WATER_QUENCH_LVL_501A >= LT_WATER_QUENCH_LVL_501C)) THEN
        rVoted_QuenchWaterLvl_mm := LT_WATER_QUENCH_LVL_501A;
    ELSIF ((LT_WATER_QUENCH_LVL_501B >= LT_WATER_QUENCH_LVL_501A) AND (LT_WATER_QUENCH_LVL_501B <= LT_WATER_QUENCH_LVL_501C)) OR
          ((LT_WATER_QUENCH_LVL_501B <= LT_WATER_QUENCH_LVL_501A) AND (LT_WATER_QUENCH_LVL_501B >= LT_WATER_QUENCH_LVL_501C)) THEN
        rVoted_QuenchWaterLvl_mm := LT_WATER_QUENCH_LVL_501B;
    ELSE
        rVoted_QuenchWaterLvl_mm := LT_WATER_QUENCH_LVL_501C;
    END_IF;
ELSIF bIso_QuenchWaterLvl_ChA AND (NOT bIso_QuenchWaterLvl_ChB) AND (NOT bIso_QuenchWaterLvl_ChC) THEN
    rVoted_QuenchWaterLvl_mm := 0.5 * (LT_WATER_QUENCH_LVL_501B + LT_WATER_QUENCH_LVL_501C);
ELSIF bIso_QuenchWaterLvl_ChB AND (NOT bIso_QuenchWaterLvl_ChA) AND (NOT bIso_QuenchWaterLvl_ChC) THEN
    rVoted_QuenchWaterLvl_mm := 0.5 * (LT_WATER_QUENCH_LVL_501A + LT_WATER_QUENCH_LVL_501C);
ELSIF bIso_QuenchWaterLvl_ChC AND (NOT bIso_QuenchWaterLvl_ChA) AND (NOT bIso_QuenchWaterLvl_ChB) THEN
    rVoted_QuenchWaterLvl_mm := 0.5 * (LT_WATER_QUENCH_LVL_501A + LT_WATER_QUENCH_LVL_501B);
ELSIF (NOT bIso_QuenchWaterLvl_ChA) THEN
    rVoted_QuenchWaterLvl_mm := LT_WATER_QUENCH_LVL_501A;
ELSIF (NOT bIso_QuenchWaterLvl_ChB) THEN
    rVoted_QuenchWaterLvl_mm := LT_WATER_QUENCH_LVL_501B;
ELSIF (NOT bIso_QuenchWaterLvl_ChC) THEN
    rVoted_QuenchWaterLvl_mm := LT_WATER_QUENCH_LVL_501C;
ELSE
    bAlarm_TMR_MajorDivergence := TRUE;
END_IF;

IF bIso_QuenchWaterLvl_ChA THEN dwSensorHealthMask_High := dwSensorHealthMask_High OR 16#0000_0001; END_IF;
IF bIso_QuenchWaterLvl_ChB THEN dwSensorHealthMask_High := dwSensorHealthMask_High OR 16#0000_0002; END_IF;
IF bIso_QuenchWaterLvl_ChC THEN dwSensorHealthMask_High := dwSensorHealthMask_High OR 16#0000_0004; END_IF;

(* --- GROUP 8: FT_HAULOFF_TENSION_601 (Haul-Off Capstan Line Tension, 0..150 kN) --- *)
rTempDiffAB := ABS(FT_HAULOFF_TENSION_601A - FT_HAULOFF_TENSION_601B);
rTempDiffBC := ABS(FT_HAULOFF_TENSION_601B - FT_HAULOFF_TENSION_601C);
rTempDiffCA := ABS(FT_HAULOFF_TENSION_601C - FT_HAULOFF_TENSION_601A);

IF (rTempDiffAB > c_rTol_HaulOffTension_kN) OR (rTempDiffBC > c_rTol_HaulOffTension_kN) OR (rTempDiffCA > c_rTol_HaulOffTension_kN) THEN
    rTimer_HaulOffTension_Disc_s := rTimer_HaulOffTension_Disc_s + c_rTs;
    IF rTimer_HaulOffTension_Disc_s >= c_rTMR_PersistencyTimeout_s THEN
        IF (rTempDiffAB > c_rTol_HaulOffTension_kN) AND (rTempDiffCA > c_rTol_HaulOffTension_kN) THEN
            bIso_HaulOffTension_ChA := TRUE;
        END_IF;
        IF (rTempDiffAB > c_rTol_HaulOffTension_kN) AND (rTempDiffBC > c_rTol_HaulOffTension_kN) THEN
            bIso_HaulOffTension_ChB := TRUE;
        END_IF;
        IF (rTempDiffBC > c_rTol_HaulOffTension_kN) AND (rTempDiffCA > c_rTol_HaulOffTension_kN) THEN
            bIso_HaulOffTension_ChC := TRUE;
        END_IF;
    END_IF;
ELSE
    rTimer_HaulOffTension_Disc_s := 0.0;
END_IF;

IF bFaultReset THEN
    bIso_HaulOffTension_ChA := FALSE;
    bIso_HaulOffTension_ChB := FALSE;
    bIso_HaulOffTension_ChC := FALSE;
END_IF;

IF (NOT bIso_HaulOffTension_ChA) AND (NOT bIso_HaulOffTension_ChB) AND (NOT bIso_HaulOffTension_ChC) THEN
    IF ((FT_HAULOFF_TENSION_601A >= FT_HAULOFF_TENSION_601B) AND (FT_HAULOFF_TENSION_601A <= FT_HAULOFF_TENSION_601C)) OR
       ((FT_HAULOFF_TENSION_601A <= FT_HAULOFF_TENSION_601B) AND (FT_HAULOFF_TENSION_601A >= FT_HAULOFF_TENSION_601C)) THEN
        rVoted_HaulOffTension_kN := FT_HAULOFF_TENSION_601A;
    ELSIF ((FT_HAULOFF_TENSION_601B >= FT_HAULOFF_TENSION_601A) AND (FT_HAULOFF_TENSION_601B <= FT_HAULOFF_TENSION_601C)) OR
          ((FT_HAULOFF_TENSION_601B <= FT_HAULOFF_TENSION_601A) AND (FT_HAULOFF_TENSION_601B >= FT_HAULOFF_TENSION_601C)) THEN
        rVoted_HaulOffTension_kN := FT_HAULOFF_TENSION_601B;
    ELSE
        rVoted_HaulOffTension_kN := FT_HAULOFF_TENSION_601C;
    END_IF;
ELSIF bIso_HaulOffTension_ChA AND (NOT bIso_HaulOffTension_ChB) AND (NOT bIso_HaulOffTension_ChC) THEN
    rVoted_HaulOffTension_kN := 0.5 * (FT_HAULOFF_TENSION_601B + FT_HAULOFF_TENSION_601C);
ELSIF bIso_HaulOffTension_ChB AND (NOT bIso_HaulOffTension_ChA) AND (NOT bIso_HaulOffTension_ChC) THEN
    rVoted_HaulOffTension_kN := 0.5 * (FT_HAULOFF_TENSION_601A + FT_HAULOFF_TENSION_601C);
ELSIF bIso_HaulOffTension_ChC AND (NOT bIso_HaulOffTension_ChA) AND (NOT bIso_HaulOffTension_ChB) THEN
    rVoted_HaulOffTension_kN := 0.5 * (FT_HAULOFF_TENSION_601A + FT_HAULOFF_TENSION_601B);
ELSIF (NOT bIso_HaulOffTension_ChA) THEN
    rVoted_HaulOffTension_kN := FT_HAULOFF_TENSION_601A;
ELSIF (NOT bIso_HaulOffTension_ChB) THEN
    rVoted_HaulOffTension_kN := FT_HAULOFF_TENSION_601B;
ELSIF (NOT bIso_HaulOffTension_ChC) THEN
    rVoted_HaulOffTension_kN := FT_HAULOFF_TENSION_601C;
ELSE
    bAlarm_TMR_MajorDivergence := TRUE;
END_IF;

IF bIso_HaulOffTension_ChA THEN dwSensorHealthMask_High := dwSensorHealthMask_High OR 16#0000_0008; END_IF;
IF bIso_HaulOffTension_ChB THEN dwSensorHealthMask_High := dwSensorHealthMask_High OR 16#0000_0010; END_IF;
IF bIso_HaulOffTension_ChC THEN dwSensorHealthMask_High := dwSensorHealthMask_High OR 16#0000_0020; END_IF;

(* --- GROUP 9: WT_WALL_THICKNESS_701 (Mean Insulation Wall Thickness, 0..40 mm) --- *)
rTempDiffAB := ABS(WT_WALL_THICKNESS_701A - WT_WALL_THICKNESS_701B);
rTempDiffBC := ABS(WT_WALL_THICKNESS_701B - WT_WALL_THICKNESS_701C);
rTempDiffCA := ABS(WT_WALL_THICKNESS_701C - WT_WALL_THICKNESS_701A);

IF (rTempDiffAB > c_rTol_WallThickness_mm) OR (rTempDiffBC > c_rTol_WallThickness_mm) OR (rTempDiffCA > c_rTol_WallThickness_mm) THEN
    rTimer_WallThickness_Disc_s := rTimer_WallThickness_Disc_s + c_rTs;
    IF rTimer_WallThickness_Disc_s >= c_rTMR_PersistencyTimeout_s THEN
        IF (rTempDiffAB > c_rTol_WallThickness_mm) AND (rTempDiffCA > c_rTol_WallThickness_mm) THEN
            bIso_WallThickness_ChA := TRUE;
        END_IF;
        IF (rTempDiffAB > c_rTol_WallThickness_mm) AND (rTempDiffBC > c_rTol_WallThickness_mm) THEN
            bIso_WallThickness_ChB := TRUE;
        END_IF;
        IF (rTempDiffBC > c_rTol_WallThickness_mm) AND (rTempDiffCA > c_rTol_WallThickness_mm) THEN
            bIso_WallThickness_ChC := TRUE;
        END_IF;
    END_IF;
ELSE
    rTimer_WallThickness_Disc_s := 0.0;
END_IF;

IF bFaultReset THEN
    bIso_WallThickness_ChA := FALSE;
    bIso_WallThickness_ChB := FALSE;
    bIso_WallThickness_ChC := FALSE;
END_IF;

IF (NOT bIso_WallThickness_ChA) AND (NOT bIso_WallThickness_ChB) AND (NOT bIso_WallThickness_ChC) THEN
    IF ((WT_WALL_THICKNESS_701A >= WT_WALL_THICKNESS_701B) AND (WT_WALL_THICKNESS_701A <= WT_WALL_THICKNESS_701C)) OR
       ((WT_WALL_THICKNESS_701A <= WT_WALL_THICKNESS_701B) AND (WT_WALL_THICKNESS_701A >= WT_WALL_THICKNESS_701C)) THEN
        rVoted_WallThickness_mm := WT_WALL_THICKNESS_701A;
    ELSIF ((WT_WALL_THICKNESS_701B >= WT_WALL_THICKNESS_701A) AND (WT_WALL_THICKNESS_701B <= WT_WALL_THICKNESS_701C)) OR
          ((WT_WALL_THICKNESS_701B <= WT_WALL_THICKNESS_701A) AND (WT_WALL_THICKNESS_701B >= WT_WALL_THICKNESS_701C)) THEN
        rVoted_WallThickness_mm := WT_WALL_THICKNESS_701B;
    ELSE
        rVoted_WallThickness_mm := WT_WALL_THICKNESS_701C;
    END_IF;
ELSIF bIso_WallThickness_ChA AND (NOT bIso_WallThickness_ChB) AND (NOT bIso_WallThickness_ChC) THEN
    rVoted_WallThickness_mm := 0.5 * (WT_WALL_THICKNESS_701B + WT_WALL_THICKNESS_701C);
ELSIF bIso_WallThickness_ChB AND (NOT bIso_WallThickness_ChA) AND (NOT bIso_WallThickness_ChC) THEN
    rVoted_WallThickness_mm := 0.5 * (WT_WALL_THICKNESS_701A + WT_WALL_THICKNESS_701C);
ELSIF bIso_WallThickness_ChC AND (NOT bIso_WallThickness_ChA) AND (NOT bIso_WallThickness_ChB) THEN
    rVoted_WallThickness_mm := 0.5 * (WT_WALL_THICKNESS_701A + WT_WALL_THICKNESS_701B);
ELSIF (NOT bIso_WallThickness_ChA) THEN
    rVoted_WallThickness_mm := WT_WALL_THICKNESS_701A;
ELSIF (NOT bIso_WallThickness_ChB) THEN
    rVoted_WallThickness_mm := WT_WALL_THICKNESS_701B;
ELSIF (NOT bIso_WallThickness_ChC) THEN
    rVoted_WallThickness_mm := WT_WALL_THICKNESS_701C;
ELSE
    bAlarm_TMR_MajorDivergence := TRUE;
END_IF;

IF bIso_WallThickness_ChA THEN dwSensorHealthMask_High := dwSensorHealthMask_High OR 16#0000_0040; END_IF;
IF bIso_WallThickness_ChB THEN dwSensorHealthMask_High := dwSensorHealthMask_High OR 16#0000_0080; END_IF;
IF bIso_WallThickness_ChC THEN dwSensorHealthMask_High := dwSensorHealthMask_High OR 16#0000_0100; END_IF;

(* --- GROUP 10: ST_LINE_PULL_SPEED_801 (Caterpillar Line Speed, 0..35 m/min) --- *)
rTempDiffAB := ABS(ST_LINE_PULL_SPEED_801A - ST_LINE_PULL_SPEED_801B);
rTempDiffBC := ABS(ST_LINE_PULL_SPEED_801B - ST_LINE_PULL_SPEED_801C);
rTempDiffCA := ABS(ST_LINE_PULL_SPEED_801C - ST_LINE_PULL_SPEED_801A);

IF (rTempDiffAB > c_rTol_LineSpeed_mpm) OR (rTempDiffBC > c_rTol_LineSpeed_mpm) OR (rTempDiffCA > c_rTol_LineSpeed_mpm) THEN
    rTimer_LineSpeed_Disc_s := rTimer_LineSpeed_Disc_s + c_rTs;
    IF rTimer_LineSpeed_Disc_s >= c_rTMR_PersistencyTimeout_s THEN
        IF (rTempDiffAB > c_rTol_LineSpeed_mpm) AND (rTempDiffCA > c_rTol_LineSpeed_mpm) THEN
            bIso_LineSpeed_ChA := TRUE;
        END_IF;
        IF (rTempDiffAB > c_rTol_LineSpeed_mpm) AND (rTempDiffBC > c_rTol_LineSpeed_mpm) THEN
            bIso_LineSpeed_ChB := TRUE;
        END_IF;
        IF (rTempDiffBC > c_rTol_LineSpeed_mpm) AND (rTempDiffCA > c_rTol_LineSpeed_mpm) THEN
            bIso_LineSpeed_ChC := TRUE;
        END_IF;
    END_IF;
ELSE
    rTimer_LineSpeed_Disc_s := 0.0;
END_IF;

IF bFaultReset THEN
    bIso_LineSpeed_ChA := FALSE;
    bIso_LineSpeed_ChB := FALSE;
    bIso_LineSpeed_ChC := FALSE;
END_IF;

IF (NOT bIso_LineSpeed_ChA) AND (NOT bIso_LineSpeed_ChB) AND (NOT bIso_LineSpeed_ChC) THEN
    IF ((ST_LINE_PULL_SPEED_801A >= ST_LINE_PULL_SPEED_801B) AND (ST_LINE_PULL_SPEED_801A <= ST_LINE_PULL_SPEED_801C)) OR
       ((ST_LINE_PULL_SPEED_801A <= ST_LINE_PULL_SPEED_801B) AND (ST_LINE_PULL_SPEED_801A >= ST_LINE_PULL_SPEED_801C)) THEN
        rVoted_LinePullSpeed_mpm := ST_LINE_PULL_SPEED_801A;
    ELSIF ((ST_LINE_PULL_SPEED_801B >= ST_LINE_PULL_SPEED_801A) AND (ST_LINE_PULL_SPEED_801B <= ST_LINE_PULL_SPEED_801C)) OR
          ((ST_LINE_PULL_SPEED_801B <= ST_LINE_PULL_SPEED_801A) AND (ST_LINE_PULL_SPEED_801B >= ST_LINE_PULL_SPEED_801C)) THEN
        rVoted_LinePullSpeed_mpm := ST_LINE_PULL_SPEED_801B;
    ELSE
        rVoted_LinePullSpeed_mpm := ST_LINE_PULL_SPEED_801C;
    END_IF;
ELSIF bIso_LineSpeed_ChA AND (NOT bIso_LineSpeed_ChB) AND (NOT bIso_LineSpeed_ChC) THEN
    rVoted_LinePullSpeed_mpm := 0.5 * (ST_LINE_PULL_SPEED_801B + ST_LINE_PULL_SPEED_801C);
ELSIF bIso_LineSpeed_ChB AND (NOT bIso_LineSpeed_ChA) AND (NOT bIso_LineSpeed_ChC) THEN
    rVoted_LinePullSpeed_mpm := 0.5 * (ST_LINE_PULL_SPEED_801A + ST_LINE_PULL_SPEED_801C);
ELSIF bIso_LineSpeed_ChC AND (NOT bIso_LineSpeed_ChA) AND (NOT bIso_LineSpeed_ChB) THEN
    rVoted_LinePullSpeed_mpm := 0.5 * (ST_LINE_PULL_SPEED_801A + ST_LINE_PULL_SPEED_801B);
ELSIF (NOT bIso_LineSpeed_ChA) THEN
    rVoted_LinePullSpeed_mpm := ST_LINE_PULL_SPEED_801A;
ELSIF (NOT bIso_LineSpeed_ChB) THEN
    rVoted_LinePullSpeed_mpm := ST_LINE_PULL_SPEED_801B;
ELSIF (NOT bIso_LineSpeed_ChC) THEN
    rVoted_LinePullSpeed_mpm := ST_LINE_PULL_SPEED_801C;
ELSE
    bAlarm_TMR_MajorDivergence := TRUE;
END_IF;

IF bIso_LineSpeed_ChA THEN dwSensorHealthMask_High := dwSensorHealthMask_High OR 16#0000_0200; END_IF;
IF bIso_LineSpeed_ChB THEN dwSensorHealthMask_High := dwSensorHealthMask_High OR 16#0000_0400; END_IF;
IF bIso_LineSpeed_ChC THEN dwSensorHealthMask_High := dwSensorHealthMask_High OR 16#0000_0800; END_IF;

(* --- GROUP 11: PT_SEAL_DIFF_PRESS_901 (Hydrostatic Quench Seal Diff Press, 0..2 bar) --- *)
rTempDiffAB := ABS(PT_SEAL_DIFF_PRESS_901A - PT_SEAL_DIFF_PRESS_901B);
rTempDiffBC := ABS(PT_SEAL_DIFF_PRESS_901B - PT_SEAL_DIFF_PRESS_901C);
rTempDiffCA := ABS(PT_SEAL_DIFF_PRESS_901C - PT_SEAL_DIFF_PRESS_901A);

IF (rTempDiffAB > c_rTol_SealDiffPress_bar) OR (rTempDiffBC > c_rTol_SealDiffPress_bar) OR (rTempDiffCA > c_rTol_SealDiffPress_bar) THEN
    rTimer_SealDiffPress_Disc_s := rTimer_SealDiffPress_Disc_s + c_rTs;
    IF rTimer_SealDiffPress_Disc_s >= c_rTMR_PersistencyTimeout_s THEN
        IF (rTempDiffAB > c_rTol_SealDiffPress_bar) AND (rTempDiffCA > c_rTol_SealDiffPress_bar) THEN
            bIso_SealDiffPress_ChA := TRUE;
        END_IF;
        IF (rTempDiffAB > c_rTol_SealDiffPress_bar) AND (rTempDiffBC > c_rTol_SealDiffPress_bar) THEN
            bIso_SealDiffPress_ChB := TRUE;
        END_IF;
        IF (rTempDiffBC > c_rTol_SealDiffPress_bar) AND (rTempDiffCA > c_rTol_SealDiffPress_bar) THEN
            bIso_SealDiffPress_ChC := TRUE;
        END_IF;
    END_IF;
ELSE
    rTimer_SealDiffPress_Disc_s := 0.0;
END_IF;

IF bFaultReset THEN
    bIso_SealDiffPress_ChA := FALSE;
    bIso_SealDiffPress_ChB := FALSE;
    bIso_SealDiffPress_ChC := FALSE;
END_IF;

IF (NOT bIso_SealDiffPress_ChA) AND (NOT bIso_SealDiffPress_ChB) AND (NOT bIso_SealDiffPress_ChC) THEN
    IF ((PT_SEAL_DIFF_PRESS_901A >= PT_SEAL_DIFF_PRESS_901B) AND (PT_SEAL_DIFF_PRESS_901A <= PT_SEAL_DIFF_PRESS_901C)) OR
       ((PT_SEAL_DIFF_PRESS_901A <= PT_SEAL_DIFF_PRESS_901B) AND (PT_SEAL_DIFF_PRESS_901A >= PT_SEAL_DIFF_PRESS_901C)) THEN
        rVoted_SealDiffPress_bar := PT_SEAL_DIFF_PRESS_901A;
    ELSIF ((PT_SEAL_DIFF_PRESS_901B >= PT_SEAL_DIFF_PRESS_901A) AND (PT_SEAL_DIFF_PRESS_901B <= PT_SEAL_DIFF_PRESS_901C)) OR
          ((PT_SEAL_DIFF_PRESS_901B <= PT_SEAL_DIFF_PRESS_901A) AND (PT_SEAL_DIFF_PRESS_901B >= PT_SEAL_DIFF_PRESS_901C)) THEN
        rVoted_SealDiffPress_bar := PT_SEAL_DIFF_PRESS_901B;
    ELSE
        rVoted_SealDiffPress_bar := PT_SEAL_DIFF_PRESS_901C;
    END_IF;
ELSIF bIso_SealDiffPress_ChA AND (NOT bIso_SealDiffPress_ChB) AND (NOT bIso_SealDiffPress_ChC) THEN
    rVoted_SealDiffPress_bar := 0.5 * (PT_SEAL_DIFF_PRESS_901B + PT_SEAL_DIFF_PRESS_901C);
ELSIF bIso_SealDiffPress_ChB AND (NOT bIso_SealDiffPress_ChA) AND (NOT bIso_SealDiffPress_ChC) THEN
    rVoted_SealDiffPress_bar := 0.5 * (PT_SEAL_DIFF_PRESS_901A + PT_SEAL_DIFF_PRESS_901C);
ELSIF bIso_SealDiffPress_ChC AND (NOT bIso_SealDiffPress_ChA) AND (NOT bIso_SealDiffPress_ChB) THEN
    rVoted_SealDiffPress_bar := 0.5 * (PT_SEAL_DIFF_PRESS_901A + PT_SEAL_DIFF_PRESS_901B);
ELSIF (NOT bIso_SealDiffPress_ChA) THEN
    rVoted_SealDiffPress_bar := PT_SEAL_DIFF_PRESS_901A;
ELSIF (NOT bIso_SealDiffPress_ChB) THEN
    rVoted_SealDiffPress_bar := PT_SEAL_DIFF_PRESS_901B;
ELSIF (NOT bIso_SealDiffPress_ChC) THEN
    rVoted_SealDiffPress_bar := PT_SEAL_DIFF_PRESS_901C;
ELSE
    bAlarm_TMR_MajorDivergence := TRUE;
END_IF;

IF bIso_SealDiffPress_ChA THEN dwSensorHealthMask_High := dwSensorHealthMask_High OR 16#0000_1000; END_IF;
IF bIso_SealDiffPress_ChB THEN dwSensorHealthMask_High := dwSensorHealthMask_High OR 16#0000_2000; END_IF;
IF bIso_SealDiffPress_ChC THEN dwSensorHealthMask_High := dwSensorHealthMask_High OR 16#0000_4000; END_IF;
"""

if __name__ == "__main__":
    s2 = get_sec2()
    print("Section 2 Length:", len(s2))
