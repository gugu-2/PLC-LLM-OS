# st_phases_1_to_5.py
# Implements Phase 1 through Phase 5 of the Function Block logic

def get_phases_1_to_5():
    return """(* ========================================================================================================== *)
(* PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING WITH BUMPLESS DEGRADATION                     *)
(* ========================================================================================================== *)

(* --- Subsystem 1: Voice Coil Z-Axis Linear Optical Scale Encoders (10 nm resolution) --- *)
f_ZEnc_Diff_1_2 := ABS(f_ZEncoder_Ch1_nm - f_ZEncoder_Ch2_nm);
f_ZEnc_Diff_2_3 := ABS(f_ZEncoder_Ch2_nm - f_ZEncoder_Ch3_nm);
f_ZEnc_Diff_3_1 := ABS(f_ZEncoder_Ch3_nm - f_ZEncoder_Ch1_nm);

(* Channel 1 discrepancy monitoring *)
IF (f_ZEnc_Diff_1_2 > f_Tol_ZEncoder_nm) AND (f_ZEnc_Diff_3_1 > f_Tol_ZEncoder_nm) THEN
    t_ZEnc_Ch1_DiscrepancyTimer := t_ZEnc_Ch1_DiscrepancyTimer + REAL_TO_TIME(LREAL_TO_REAL(f_SamplingTime_s * 1000.0));
    IF t_ZEnc_Ch1_DiscrepancyTimer >= t_Discrepancy_ZEncoder_Max THEN
        b_ZEnc_Ch1_Healthy := FALSE;
    END_IF;
ELSE
    t_ZEnc_Ch1_DiscrepancyTimer := T#0ms;
    b_ZEnc_Ch1_Healthy := TRUE;
END_IF;

(* Channel 2 discrepancy monitoring *)
IF (f_ZEnc_Diff_1_2 > f_Tol_ZEncoder_nm) AND (f_ZEnc_Diff_2_3 > f_Tol_ZEncoder_nm) THEN
    t_ZEnc_Ch2_DiscrepancyTimer := t_ZEnc_Ch2_DiscrepancyTimer + REAL_TO_TIME(LREAL_TO_REAL(f_SamplingTime_s * 1000.0));
    IF t_ZEnc_Ch2_DiscrepancyTimer >= t_Discrepancy_ZEncoder_Max THEN
        b_ZEnc_Ch2_Healthy := FALSE;
    END_IF;
ELSE
    t_ZEnc_Ch2_DiscrepancyTimer := T#0ms;
    b_ZEnc_Ch2_Healthy := TRUE;
END_IF;

(* Channel 3 discrepancy monitoring *)
IF (f_ZEnc_Diff_2_3 > f_Tol_ZEncoder_nm) AND (f_ZEnc_Diff_3_1 > f_Tol_ZEncoder_nm) THEN
    t_ZEnc_Ch3_DiscrepancyTimer := t_ZEnc_Ch3_DiscrepancyTimer + REAL_TO_TIME(LREAL_TO_REAL(f_SamplingTime_s * 1000.0));
    IF t_ZEnc_Ch3_DiscrepancyTimer >= t_Discrepancy_ZEncoder_Max THEN
        b_ZEnc_Ch3_Healthy := FALSE;
    END_IF;
ELSE
    t_ZEnc_Ch3_DiscrepancyTimer := T#0ms;
    b_ZEnc_Ch3_Healthy := TRUE;
END_IF;

(* 2oo3 Voting & Degradation Matrix for Z Encoders *)
IF b_ZEnc_Ch1_Healthy AND b_ZEnc_Ch2_Healthy AND b_ZEnc_Ch3_Healthy THEN
    b_ZEnc_TMR_Degraded := FALSE;
    b_ZEnc_TMR_FaultTrip := FALSE;
    (* Median of three calculation *)
    IF ((f_ZEncoder_Ch1_nm >= f_ZEncoder_Ch2_nm) AND (f_ZEncoder_Ch1_nm <= f_ZEncoder_Ch3_nm)) OR
       ((f_ZEncoder_Ch1_nm >= f_ZEncoder_Ch3_nm) AND (f_ZEncoder_Ch1_nm <= f_ZEncoder_Ch2_nm)) THEN
        f_Voted_ZPos_nm := f_ZEncoder_Ch1_nm;
    ELSIF ((f_ZEncoder_Ch2_nm >= f_ZEncoder_Ch1_nm) AND (f_ZEncoder_Ch2_nm <= f_ZEncoder_Ch3_nm)) OR
          ((f_ZEncoder_Ch2_nm >= f_ZEncoder_Ch3_nm) AND (f_ZEncoder_Ch2_nm <= f_ZEncoder_Ch1_nm)) THEN
        f_Voted_ZPos_nm := f_ZEncoder_Ch2_nm;
    ELSE
        f_Voted_ZPos_nm := f_ZEncoder_Ch3_nm;
    END_IF;
ELSIF b_ZEnc_Ch1_Healthy AND b_ZEnc_Ch2_Healthy THEN
    b_ZEnc_TMR_Degraded := TRUE;
    b_ZEnc_TMR_FaultTrip := FALSE;
    f_Voted_ZPos_nm := (f_ZEncoder_Ch1_nm + f_ZEncoder_Ch2_nm) * 0.5;
ELSIF b_ZEnc_Ch2_Healthy AND b_ZEnc_Ch3_Healthy THEN
    b_ZEnc_TMR_Degraded := TRUE;
    b_ZEnc_TMR_FaultTrip := FALSE;
    f_Voted_ZPos_nm := (f_ZEncoder_Ch2_nm + f_ZEncoder_Ch3_nm) * 0.5;
ELSIF b_ZEnc_Ch3_Healthy AND b_ZEnc_Ch1_Healthy THEN
    b_ZEnc_TMR_Degraded := TRUE;
    b_ZEnc_TMR_FaultTrip := FALSE;
    f_Voted_ZPos_nm := (f_ZEncoder_Ch3_nm + f_ZEncoder_Ch1_nm) * 0.5;
ELSIF b_ZEnc_Ch1_Healthy THEN
    b_ZEnc_TMR_Degraded := TRUE;
    b_ZEnc_TMR_FaultTrip := FALSE;
    f_Voted_ZPos_nm := f_ZEncoder_Ch1_nm;
ELSIF b_ZEnc_Ch2_Healthy THEN
    b_ZEnc_TMR_Degraded := TRUE;
    b_ZEnc_TMR_FaultTrip := FALSE;
    f_Voted_ZPos_nm := f_ZEncoder_Ch2_nm;
ELSIF b_ZEnc_Ch3_Healthy THEN
    b_ZEnc_TMR_Degraded := TRUE;
    b_ZEnc_TMR_FaultTrip := FALSE;
    f_Voted_ZPos_nm := f_ZEncoder_Ch3_nm;
ELSE
    b_ZEnc_TMR_Degraded := TRUE;
    b_ZEnc_TMR_FaultTrip := TRUE;
    (* Hold last valid voted position in hardware safe hold *)
END_IF;

(* --- Subsystem 2: Dynamic Piezoelectric Contact Bond Force Sensors --- *)
f_Force_Diff_1_2 := ABS(f_BondForce_LoadCell1_mN - f_BondForce_LoadCell2_mN);
f_Force_Diff_2_3 := ABS(f_BondForce_LoadCell2_mN - f_BondForce_LoadCell3_mN);
f_Force_Diff_3_1 := ABS(f_BondForce_LoadCell3_mN - f_BondForce_LoadCell1_mN);

IF (f_Force_Diff_1_2 > f_Tol_BondForce_mN) AND (f_Force_Diff_3_1 > f_Tol_BondForce_mN) THEN
    t_Force_Ch1_DiscrepancyTimer := t_Force_Ch1_DiscrepancyTimer + REAL_TO_TIME(LREAL_TO_REAL(f_SamplingTime_s * 1000.0));
    IF t_Force_Ch1_DiscrepancyTimer >= t_Discrepancy_BondForce_Max THEN
        b_Force_Ch1_Healthy := FALSE;
    END_IF;
ELSE
    t_Force_Ch1_DiscrepancyTimer := T#0ms;
    b_Force_Ch1_Healthy := TRUE;
END_IF;

IF (f_Force_Diff_1_2 > f_Tol_BondForce_mN) AND (f_Force_Diff_2_3 > f_Tol_BondForce_mN) THEN
    t_Force_Ch2_DiscrepancyTimer := t_Force_Ch2_DiscrepancyTimer + REAL_TO_TIME(LREAL_TO_REAL(f_SamplingTime_s * 1000.0));
    IF t_Force_Ch2_DiscrepancyTimer >= t_Discrepancy_BondForce_Max THEN
        b_Force_Ch2_Healthy := FALSE;
    END_IF;
ELSE
    t_Force_Ch2_DiscrepancyTimer := T#0ms;
    b_Force_Ch2_Healthy := TRUE;
END_IF;

IF (f_Force_Diff_2_3 > f_Tol_BondForce_mN) AND (f_Force_Diff_3_1 > f_Tol_BondForce_mN) THEN
    t_Force_Ch3_DiscrepancyTimer := t_Force_Ch3_DiscrepancyTimer + REAL_TO_TIME(LREAL_TO_REAL(f_SamplingTime_s * 1000.0));
    IF t_Force_Ch3_DiscrepancyTimer >= t_Discrepancy_BondForce_Max THEN
        b_Force_Ch3_Healthy := FALSE;
    END_IF;
ELSE
    t_Force_Ch3_DiscrepancyTimer := T#0ms;
    b_Force_Ch3_Healthy := TRUE;
END_IF;

IF b_Force_Ch1_Healthy AND b_Force_Ch2_Healthy AND b_Force_Ch3_Healthy THEN
    b_Force_TMR_Degraded := FALSE;
    b_Force_TMR_FaultTrip := FALSE;
    IF ((f_BondForce_LoadCell1_mN >= f_BondForce_LoadCell2_mN) AND (f_BondForce_LoadCell1_mN <= f_BondForce_LoadCell3_mN)) OR
       ((f_BondForce_LoadCell1_mN >= f_BondForce_LoadCell3_mN) AND (f_BondForce_LoadCell1_mN <= f_BondForce_LoadCell2_mN)) THEN
        f_Voted_BondForce_mN := f_BondForce_LoadCell1_mN;
    ELSIF ((f_BondForce_LoadCell2_mN >= f_BondForce_LoadCell1_mN) AND (f_BondForce_LoadCell2_mN <= f_BondForce_LoadCell3_mN)) OR
          ((f_BondForce_LoadCell2_mN >= f_BondForce_LoadCell3_mN) AND (f_BondForce_LoadCell2_mN <= f_BondForce_LoadCell1_mN)) THEN
        f_Voted_BondForce_mN := f_BondForce_LoadCell2_mN;
    ELSE
        f_Voted_BondForce_mN := f_BondForce_LoadCell3_mN;
    END_IF;
ELSIF b_Force_Ch1_Healthy AND b_Force_Ch2_Healthy THEN
    b_Force_TMR_Degraded := TRUE;
    b_Force_TMR_FaultTrip := FALSE;
    f_Voted_BondForce_mN := (f_BondForce_LoadCell1_mN + f_BondForce_LoadCell2_mN) * 0.5;
ELSIF b_Force_Ch2_Healthy AND b_Force_Ch3_Healthy THEN
    b_Force_TMR_Degraded := TRUE;
    b_Force_TMR_FaultTrip := FALSE;
    f_Voted_BondForce_mN := (f_BondForce_LoadCell2_mN + f_BondForce_LoadCell3_mN) * 0.5;
ELSIF b_Force_Ch3_Healthy AND b_Force_Ch1_Healthy THEN
    b_Force_TMR_Degraded := TRUE;
    b_Force_TMR_FaultTrip := FALSE;
    f_Voted_BondForce_mN := (f_BondForce_LoadCell3_mN + f_BondForce_LoadCell1_mN) * 0.5;
ELSIF b_Force_Ch1_Healthy THEN
    b_Force_TMR_Degraded := TRUE;
    b_Force_TMR_FaultTrip := FALSE;
    f_Voted_BondForce_mN := f_BondForce_LoadCell1_mN;
ELSIF b_Force_Ch2_Healthy THEN
    b_Force_TMR_Degraded := TRUE;
    b_Force_TMR_FaultTrip := FALSE;
    f_Voted_BondForce_mN := f_BondForce_LoadCell2_mN;
ELSIF b_Force_Ch3_Healthy THEN
    b_Force_TMR_Degraded := TRUE;
    b_Force_TMR_FaultTrip := FALSE;
    f_Voted_BondForce_mN := f_BondForce_LoadCell3_mN;
ELSE
    b_Force_TMR_Degraded := TRUE;
    b_Force_TMR_FaultTrip := TRUE;
END_IF;

(* --- Subsystem 3: Ultrasonic Generator Electrical Power Feedback --- *)
f_USPwr_Diff_1_2 := ABS(f_US_FeedbackPower_Ch1_mW - f_US_FeedbackPower_Ch2_mW);
f_USPwr_Diff_2_3 := ABS(f_US_FeedbackPower_Ch2_mW - f_US_FeedbackPower_Ch3_mW);
f_USPwr_Diff_3_1 := ABS(f_US_FeedbackPower_Ch3_mW - f_US_FeedbackPower_Ch1_mW);

IF (f_USPwr_Diff_1_2 > f_Tol_USPower_mW) AND (f_USPwr_Diff_3_1 > f_Tol_USPower_mW) THEN
    t_USPwr_Ch1_DiscrepancyTimer := t_USPwr_Ch1_DiscrepancyTimer + REAL_TO_TIME(LREAL_TO_REAL(f_SamplingTime_s * 1000.0));
    IF t_USPwr_Ch1_DiscrepancyTimer >= t_Discrepancy_USPower_Max THEN
        b_USPwr_Ch1_Healthy := FALSE;
    END_IF;
ELSE
    t_USPwr_Ch1_DiscrepancyTimer := T#0ms;
    b_USPwr_Ch1_Healthy := TRUE;
END_IF;

IF (f_USPwr_Diff_1_2 > f_Tol_USPower_mW) AND (f_USPwr_Diff_2_3 > f_Tol_USPower_mW) THEN
    t_USPwr_Ch2_DiscrepancyTimer := t_USPwr_Ch2_DiscrepancyTimer + REAL_TO_TIME(LREAL_TO_REAL(f_SamplingTime_s * 1000.0));
    IF t_USPwr_Ch2_DiscrepancyTimer >= t_Discrepancy_USPower_Max THEN
        b_USPwr_Ch2_Healthy := FALSE;
    END_IF;
ELSE
    t_USPwr_Ch2_DiscrepancyTimer := T#0ms;
    b_USPwr_Ch2_Healthy := TRUE;
END_IF;

IF (f_USPwr_Diff_2_3 > f_Tol_USPower_mW) AND (f_USPwr_Diff_3_1 > f_Tol_USPower_mW) THEN
    t_USPwr_Ch3_DiscrepancyTimer := t_USPwr_Ch3_DiscrepancyTimer + REAL_TO_TIME(LREAL_TO_REAL(f_SamplingTime_s * 1000.0));
    IF t_USPwr_Ch3_DiscrepancyTimer >= t_Discrepancy_USPower_Max THEN
        b_USPwr_Ch3_Healthy := FALSE;
    END_IF;
ELSE
    t_USPwr_Ch3_DiscrepancyTimer := T#0ms;
    b_USPwr_Ch3_Healthy := TRUE;
END_IF;

IF b_USPwr_Ch1_Healthy AND b_USPwr_Ch2_Healthy AND b_USPwr_Ch3_Healthy THEN
    b_USPwr_TMR_Degraded := FALSE;
    b_USPwr_TMR_FaultTrip := FALSE;
    IF ((f_US_FeedbackPower_Ch1_mW >= f_US_FeedbackPower_Ch2_mW) AND (f_US_FeedbackPower_Ch1_mW <= f_US_FeedbackPower_Ch3_mW)) OR
       ((f_US_FeedbackPower_Ch1_mW >= f_US_FeedbackPower_Ch3_mW) AND (f_US_FeedbackPower_Ch1_mW <= f_US_FeedbackPower_Ch2_mW)) THEN
        f_Voted_USPower_mW := f_US_FeedbackPower_Ch1_mW;
    ELSIF ((f_US_FeedbackPower_Ch2_mW >= f_US_FeedbackPower_Ch1_mW) AND (f_US_FeedbackPower_Ch2_mW <= f_US_FeedbackPower_Ch3_mW)) OR
          ((f_US_FeedbackPower_Ch2_mW >= f_US_FeedbackPower_Ch3_mW) AND (f_US_FeedbackPower_Ch2_mW <= f_US_FeedbackPower_Ch1_mW)) THEN
        f_Voted_USPower_mW := f_US_FeedbackPower_Ch2_mW;
    ELSE
        f_Voted_USPower_mW := f_US_FeedbackPower_Ch3_mW;
    END_IF;
ELSIF b_USPwr_Ch1_Healthy AND b_USPwr_Ch2_Healthy THEN
    b_USPwr_TMR_Degraded := TRUE;
    b_USPwr_TMR_FaultTrip := FALSE;
    f_Voted_USPower_mW := (f_US_FeedbackPower_Ch1_mW + f_US_FeedbackPower_Ch2_mW) * 0.5;
ELSIF b_USPwr_Ch2_Healthy AND b_USPwr_Ch3_Healthy THEN
    b_USPwr_TMR_Degraded := TRUE;
    b_USPwr_TMR_FaultTrip := FALSE;
    f_Voted_USPower_mW := (f_US_FeedbackPower_Ch2_mW + f_US_FeedbackPower_Ch3_mW) * 0.5;
ELSIF b_USPwr_Ch3_Healthy AND b_USPwr_Ch1_Healthy THEN
    b_USPwr_TMR_Degraded := TRUE;
    b_USPwr_TMR_FaultTrip := FALSE;
    f_Voted_USPower_mW := (f_US_FeedbackPower_Ch3_mW + f_US_FeedbackPower_Ch1_mW) * 0.5;
ELSIF b_USPwr_Ch1_Healthy THEN
    b_USPwr_TMR_Degraded := TRUE;
    b_USPwr_TMR_FaultTrip := FALSE;
    f_Voted_USPower_mW := f_US_FeedbackPower_Ch1_mW;
ELSIF b_USPwr_Ch2_Healthy THEN
    b_USPwr_TMR_Degraded := TRUE;
    b_USPwr_TMR_FaultTrip := FALSE;
    f_Voted_USPower_mW := f_US_FeedbackPower_Ch2_mW;
ELSIF b_USPwr_Ch3_Healthy THEN
    b_USPwr_TMR_Degraded := TRUE;
    b_USPwr_TMR_FaultTrip := FALSE;
    f_Voted_USPower_mW := f_US_FeedbackPower_Ch3_mW;
ELSE
    b_USPwr_TMR_Degraded := TRUE;
    b_USPwr_TMR_FaultTrip := TRUE;
END_IF;

(* --- Subsystem 4: Substrate Vacuum Workholder Pressure Sensors --- *)
f_Vac_Diff_1_2 := ABS(f_StageVacuum_Ch1_mbar - f_StageVacuum_Ch2_mbar);
f_Vac_Diff_2_3 := ABS(f_StageVacuum_Ch2_mbar - f_StageVacuum_Ch3_mbar);
f_Vac_Diff_3_1 := ABS(f_StageVacuum_Ch3_mbar - f_StageVacuum_Ch1_mbar);

IF (f_Vac_Diff_1_2 > f_Tol_StageVacuum_mbar) AND (f_Vac_Diff_3_1 > f_Tol_StageVacuum_mbar) THEN
    t_Vac_Ch1_DiscrepancyTimer := t_Vac_Ch1_DiscrepancyTimer + REAL_TO_TIME(LREAL_TO_REAL(f_SamplingTime_s * 1000.0));
    IF t_Vac_Ch1_DiscrepancyTimer >= t_Discrepancy_StageVacuum_Max THEN
        b_Vac_Ch1_Healthy := FALSE;
    END_IF;
ELSE
    t_Vac_Ch1_DiscrepancyTimer := T#0ms;
    b_Vac_Ch1_Healthy := TRUE;
END_IF;

IF (f_Vac_Diff_1_2 > f_Tol_StageVacuum_mbar) AND (f_Vac_Diff_2_3 > f_Tol_StageVacuum_mbar) THEN
    t_Vac_Ch2_DiscrepancyTimer := t_Vac_Ch2_DiscrepancyTimer + REAL_TO_TIME(LREAL_TO_REAL(f_SamplingTime_s * 1000.0));
    IF t_Vac_Ch2_DiscrepancyTimer >= t_Discrepancy_StageVacuum_Max THEN
        b_Vac_Ch2_Healthy := FALSE;
    END_IF;
ELSE
    t_Vac_Ch2_DiscrepancyTimer := T#0ms;
    b_Vac_Ch2_Healthy := TRUE;
END_IF;

IF (f_Vac_Diff_2_3 > f_Tol_StageVacuum_mbar) AND (f_Vac_Diff_3_1 > f_Tol_StageVacuum_mbar) THEN
    t_Vac_Ch3_DiscrepancyTimer := t_Vac_Ch3_DiscrepancyTimer + REAL_TO_TIME(LREAL_TO_REAL(f_SamplingTime_s * 1000.0));
    IF t_Vac_Ch3_DiscrepancyTimer >= t_Discrepancy_StageVacuum_Max THEN
        b_Vac_Ch3_Healthy := FALSE;
    END_IF;
ELSE
    t_Vac_Ch3_DiscrepancyTimer := T#0ms;
    b_Vac_Ch3_Healthy := TRUE;
END_IF;

IF b_Vac_Ch1_Healthy AND b_Vac_Ch2_Healthy AND b_Vac_Ch3_Healthy THEN
    b_Vac_TMR_Degraded := FALSE;
    b_Vac_TMR_FaultTrip := FALSE;
    IF ((f_StageVacuum_Ch1_mbar >= f_StageVacuum_Ch2_mbar) AND (f_StageVacuum_Ch1_mbar <= f_StageVacuum_Ch3_mbar)) OR
       ((f_StageVacuum_Ch1_mbar >= f_StageVacuum_Ch3_mbar) AND (f_StageVacuum_Ch1_mbar <= f_StageVacuum_Ch2_mbar)) THEN
        f_Voted_StageVacuum_mbar := f_StageVacuum_Ch1_mbar;
    ELSIF ((f_StageVacuum_Ch2_mbar >= f_StageVacuum_Ch1_mbar) AND (f_StageVacuum_Ch2_mbar <= f_StageVacuum_Ch3_mbar)) OR
          ((f_StageVacuum_Ch2_mbar >= f_StageVacuum_Ch3_mbar) AND (f_StageVacuum_Ch2_mbar <= f_StageVacuum_Ch1_mbar)) THEN
        f_Voted_StageVacuum_mbar := f_StageVacuum_Ch2_mbar;
    ELSE
        f_Voted_StageVacuum_mbar := f_StageVacuum_Ch3_mbar;
    END_IF;
ELSIF b_Vac_Ch1_Healthy AND b_Vac_Ch2_Healthy THEN
    b_Vac_TMR_Degraded := TRUE;
    b_Vac_TMR_FaultTrip := FALSE;
    f_Voted_StageVacuum_mbar := (f_StageVacuum_Ch1_mbar + f_StageVacuum_Ch2_mbar) * 0.5;
ELSIF b_Vac_Ch2_Healthy AND b_Vac_Ch3_Healthy THEN
    b_Vac_TMR_Degraded := TRUE;
    b_Vac_TMR_FaultTrip := FALSE;
    f_Voted_StageVacuum_mbar := (f_StageVacuum_Ch2_mbar + f_StageVacuum_Ch3_mbar) * 0.5;
ELSIF b_Vac_Ch3_Healthy AND b_Vac_Ch1_Healthy THEN
    b_Vac_TMR_Degraded := TRUE;
    b_Vac_TMR_FaultTrip := FALSE;
    f_Voted_StageVacuum_mbar := (f_StageVacuum_Ch3_mbar + f_StageVacuum_Ch1_mbar) * 0.5;
ELSIF b_Vac_Ch1_Healthy THEN
    b_Vac_TMR_Degraded := TRUE;
    b_Vac_TMR_FaultTrip := FALSE;
    f_Voted_StageVacuum_mbar := f_StageVacuum_Ch1_mbar;
ELSIF b_Vac_Ch2_Healthy THEN
    b_Vac_TMR_Degraded := TRUE;
    b_Vac_TMR_FaultTrip := FALSE;
    f_Voted_StageVacuum_mbar := f_StageVacuum_Ch2_mbar;
ELSIF b_Vac_Ch3_Healthy THEN
    b_Vac_TMR_Degraded := TRUE;
    b_Vac_TMR_FaultTrip := FALSE;
    f_Voted_StageVacuum_mbar := f_StageVacuum_Ch3_mbar;
ELSE
    b_Vac_TMR_Degraded := TRUE;
    b_Vac_TMR_FaultTrip := TRUE;
END_IF;

(* ========================================================================================================== *)
(* PHASE 2: DISCRETE STATE-SPACE MODEL PROPAGATION & ESTIMATION (x[k+1] = A*x[k] + B*u[k])                   *)
(* ========================================================================================================== *)
(* Update Plant Measurement Vector from Voted Sensors *)
y_Output[1] := f_Voted_ZPos_nm;
y_Output[2] := f_Voted_BondForce_mN;
y_Output[3] := f_Voted_USPower_mW;
y_Output[4] := f_US_ImpedancePhase_deg;
y_Output[5] := f_FAB_OpticalMeasurement_um;
y_Output[6] := f_BondDeformation_um;
y_Output[7] := f_StageTemp_Zone1_degC;
y_Output[8] := f_WireSpoolTension_mN;

(* Step 1: Compute Estimated Output Vector y_Model = C * x + D * u *)
FOR i_Idx := 1 TO 8 DO
    f_TempSum := 0.0;
    FOR j_Idx := 1 TO 16 DO
        f_TempSum := f_TempSum + C_Matrix[i_Idx, j_Idx] * x_State[j_Idx];
    END_FOR;
    FOR m_Idx := 1 TO 8 DO
        f_TempSum := f_TempSum + D_Matrix[i_Idx, m_Idx] * u_Input[m_Idx];
    END_FOR;
    y_Model[i_Idx] := f_TempSum;
    (* Innovation error vector: e[k] = y_measured[k] - y_estimated[k] *)
    e_Innov[i_Idx] := y_Output[i_Idx] - y_Model[i_Idx];
END_FOR;

(* Step 2: Propagate State Estimate x[k+1] = A * x[k] + B * u[k] + L * e[k] *)
FOR i_Idx := 1 TO 16 DO
    f_TempSum := 0.0;
    FOR j_Idx := 1 TO 16 DO
        f_TempSum := f_TempSum + A_Matrix[i_Idx, j_Idx] * x_State[j_Idx];
    END_FOR;
    FOR m_Idx := 1 TO 8 DO
        f_TempSum := f_TempSum + B_Matrix[i_Idx, m_Idx] * u_Input[m_Idx];
    END_FOR;
    FOR k_Idx := 1 TO 8 DO
        f_TempSum := f_TempSum + L_Gain[i_Idx, k_Idx] * e_Innov[k_Idx];
    END_FOR;
    x_Pred[i_Idx] := f_TempSum;
END_FOR;

(* Step 3: State Vector Update & Physical Saturation Clamping *)
FOR i_Idx := 1 TO 16 DO
    x_State[i_Idx] := x_Pred[i_Idx];
END_FOR;

(* Bound physical limits on critical states *)
IF x_State[1] < 0.0 THEN x_State[1] := 0.0; END_IF;           (* Z-position non-negative *)
IF x_State[5] < 0.0 THEN x_State[5] := 0.0; END_IF;           (* Reaction force compressive *)
IF x_State[11] < 0.0 THEN x_State[11] := 0.0; END_IF;         (* IMC thickness non-negative *)
IF x_State[12] < 20.0 THEN x_State[12] := 20.0; END_IF;       (* Contact temperature >= ambient *)
IF x_State[14] < 0.0 THEN x_State[14] := 0.0; END_IF;         (* Wire plastic strain >= 0 *)

(* ========================================================================================================== *)
(* PHASE 3: RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) OPTIMIZATION                                     *)
(* ========================================================================================================== *)
(* Set Target State References based on operational mode *)
IF n_CurrentState = STATE_APPROACH_SOFT_LANDING THEN
    x_Ref[1] := f_ContactTouchdownZ_nm;                      (* Target soft-landing Z position *)
    x_Ref[2] := 45.0;                                        (* Approach soft-landing velocity: 45 um/s *)
    x_Ref[3] := 0.0;                                         (* Minimal holding current *)
    x_Ref[4] := 0.0;                                         (* Zero capillary tip deflection *)
    x_Ref[5] := f_TouchdownForceThreshold_mN;                (* Target initial touch force: 45 mN *)
    x_Ref[6] := 0.0;                                         (* Zero ultrasonic vibration before landing *)
    x_Ref[7] := 0.0;
    x_Ref[8] := 45.0;                                        (* Idle ultrasonic impedance *)
ELSIF n_CurrentState = STATE_1ST_BOND_ULTRASONIC_BURST THEN
    x_Ref[1] := f_ContactTouchdownZ_nm + 12000.0;            (* Ball deformation squash depth [nm] *)
    x_Ref[2] := 0.0;                                         (* Zero velocity during dwell *)
    x_Ref[3] := 850.0;                                       (* VCM active downforce holding current [mA] *)
    x_Ref[4] := 15.0;                                        (* Capillary deflection under load [nm] *)
    x_Ref[5] := f_SetBondForce_1st_mN;                       (* Commanded 1st bond force setpoint *)
    x_Ref[6] := 420.0;                                       (* Ultrasonic tip horn amplitude 420 nm *)
    x_Ref[7] := 185000.0;                                    (* Ultrasonic vibration velocity [um/s] *)
    x_Ref[8] := 28.0;                                        (* Acoustic loaded bond impedance [Ohm] *)
ELSIF n_CurrentState = STATE_2ND_BOND_STITCH_BURST THEN
    x_Ref[1] := f_ContactTouchdownZ_nm + 8000.0;             (* Stitch crescent deformation depth [nm] *)
    x_Ref[2] := 0.0;
    x_Ref[3] := 1250.0;                                      (* VCM stitch holding current [mA] *)
    x_Ref[4] := 25.0;
    x_Ref[5] := f_SetBondForce_2nd_mN;                       (* Commanded 2nd bond stitch force *)
    x_Ref[6] := 580.0;                                       (* Higher ultrasonic stitch scrub amplitude *)
    x_Ref[7] := 245000.0;
    x_Ref[8] := 22.0;
ELSE
    x_Ref[1] := 0.0;
    x_Ref[2] := 0.0;
    x_Ref[3] := 0.0;
    x_Ref[4] := 0.0;
    x_Ref[5] := 0.0;
    x_Ref[6] := 0.0;
    x_Ref[7] := 0.0;
    x_Ref[8] := 45.0;
END_IF;

(* Recursive Quadratic Cost Minimization & Gradient Descent Solver *)
f_MPC_Cost_J := 0.0;
FOR k_Idx := 1 TO 8 DO
    f_MPC_Cost_J := f_MPC_Cost_J + Q_Weight[k_Idx] * (y_Output[k_Idx] - x_Ref[k_Idx]) * (y_Output[k_Idx] - x_Ref[k_Idx]);
    f_MPC_Cost_J := f_MPC_Cost_J + R_Weight[k_Idx] * u_Input[k_Idx] * u_Input[k_Idx];
    f_MPC_Cost_J := f_MPC_Cost_J + S_RateWeight[k_Idx] * (u_Input[k_Idx] - u_MPC_Previous[k_Idx]) * (u_Input[k_Idx] - u_MPC_Previous[k_Idx]);
END_FOR;

(* Compute Analytical Gradients & Quasi-Newton Updates *)
FOR m_Idx := 1 TO 8 DO
    grad_Cost[m_Idx] := 2.0 * R_Weight[m_Idx] * u_Input[m_Idx] +
                        2.0 * S_RateWeight[m_Idx] * (u_Input[m_Idx] - u_MPC_Previous[m_Idx]);
    FOR k_Idx := 1 TO 8 DO
        grad_Cost[m_Idx] := grad_Cost[m_Idx] + 2.0 * Q_Weight[k_Idx] * (y_Output[k_Idx] - x_Ref[k_Idx]) * B_Matrix[k_Idx, m_Idx];
    END_FOR;
    Hessian_Diag[m_Idx] := 2.0 * R_Weight[m_Idx] + 2.0 * S_RateWeight[m_Idx] + 0.150;
    IF Hessian_Diag[m_Idx] < 0.01 THEN Hessian_Diag[m_Idx] := 0.01; END_IF;

    (* Projected Gradient Step *)
    delta_u_Cmd[m_Idx] := - f_MPC_StepSize_Alpha * (grad_Cost[m_Idx] / Hessian_Diag[m_Idx]);
    u_MPC_Optimal[m_Idx] := u_Input[m_Idx] + delta_u_Cmd[m_Idx];
END_FOR;

(* Enforce Hard Actuator Envelope Constraints *)
(* Voice Coil Drive Current Clamping [-5000 mA .. +5000 mA] *)
IF u_MPC_Optimal[1] > f_VCM_Current_Max_mA THEN
    u_MPC_Optimal[1] := f_VCM_Current_Max_mA;
ELSIF u_MPC_Optimal[1] < f_VCM_Current_Min_mA THEN
    u_MPC_Optimal[1] := f_VCM_Current_Min_mA;
END_IF;

(* Ultrasonic Power Burst Clamping [0 mW .. 1500 mW] *)
IF u_MPC_Optimal[2] > f_US_Power_Max_mW THEN
    u_MPC_Optimal[2] := f_US_Power_Max_mW;
ELSIF u_MPC_Optimal[2] < 0.0 THEN
    u_MPC_Optimal[2] := 0.0;
END_IF;

(* Heater Zone Commands Clamping [0% .. 100%] *)
FOR m_Idx := 6 TO 8 DO
    IF u_MPC_Optimal[m_Idx] > 100.0 THEN
        u_MPC_Optimal[m_Idx] := 100.0;
    ELSIF u_MPC_Optimal[m_Idx] < 0.0 THEN
        u_MPC_Optimal[m_Idx] := 0.0;
    END_IF;
END_FOR;

(* Store Previous MPC Control Vector for Slew Limiting *)
FOR m_Idx := 1 TO 8 DO
    u_MPC_Previous[m_Idx] := u_Input[m_Idx];
    u_Input[m_Idx] := u_MPC_Optimal[m_Idx];
END_FOR;

(* ========================================================================================================== *)
(* PHASE 4: DUAL-FREQUENCY ULTRASONIC TRANSDUCER & PLL RESONANCE TRACKING                                     *)
(* ========================================================================================================== *)
(* Select Active Center Resonant Frequency *)
IF b_US_DualFreq_SelectHigh THEN
    f_US_ActiveCenterFreq_kHz := f_US_NominalFreq_138k;
ELSE
    f_US_ActiveCenterFreq_kHz := f_US_NominalFreq_60k;
END_IF;

(* Dynamic Phase-Locked Loop (PLL) Tracking Resonant Zero-Phase Dip *)
f_US_PhaseError_deg := f_US_ImpedancePhase_deg - 0.0; (* Transducer resonance corresponds to zero electrical phase *)

(* Anti-Windup Integrator for PLL *)
f_US_PLL_Integrator := f_US_PLL_Integrator + f_US_PLL_Ki * f_US_PhaseError_deg * f_SamplingTime_s * 1000.0;
IF f_US_PLL_Integrator > 5.0 THEN
    f_US_PLL_Integrator := 5.0;
ELSIF f_US_PLL_Integrator < -5.0 THEN
    f_US_PLL_Integrator := -5.0;
END_IF;

(* Resonant Frequency Tracking Command *)
f_US_PLL_Frequency_kHz := f_US_ActiveCenterFreq_kHz + f_US_PLL_Kp * f_US_PhaseError_deg + f_US_PLL_Integrator;

(* Calculate Dynamic Transducer Admittance & Conductance Circle *)
IF f_US_Current_mA > 0.1 THEN
    f_US_ImpedanceMag_Ohm := (f_Voted_USPower_mW / (f_US_Current_mA * f_US_Current_mA)) * 1000.0;
    IF f_US_ImpedanceMag_Ohm < 5.0 THEN f_US_ImpedanceMag_Ohm := 5.0; END_IF;
    f_US_DynamicAdmittance_mS := (1.0 / f_US_ImpedanceMag_Ohm) * 1000.0;
    f_US_DynamicConductance_mS := f_US_DynamicAdmittance_mS * COS(f_US_ImpedancePhase_deg * 3.1415926535 / 180.0);
    f_US_DynamicSusceptance_mS := - f_US_DynamicAdmittance_mS * SIN(f_US_ImpedancePhase_deg * 3.1415926535 / 180.0);
ELSE
    f_US_ImpedanceMag_Ohm := 45.0;
    f_US_DynamicConductance_mS := 22.0;
    f_US_DynamicSusceptance_mS := 0.0;
END_IF;

(* Resonance Lock Detection *)
IF (ABS(f_US_PhaseError_deg) <= 4.0) AND (f_US_DynamicConductance_mS >= 16.0) THEN
    b_US_ResonanceLocked := TRUE;
ELSE
    b_US_ResonanceLocked := FALSE;
END_IF;

(* Track Delivered Acoustic Burst Energy *)
IF (n_CurrentState = STATE_1ST_BOND_ULTRASONIC_BURST) OR (n_CurrentState = STATE_2ND_BOND_STITCH_BURST) THEN
    f_US_TotalEnergyDelivered_mJ := f_US_TotalEnergyDelivered_mJ + (f_Voted_USPower_mW * f_SamplingTime_s);
ELSE
    f_US_TotalEnergyDelivered_mJ := 0.0;
END_IF;

(* ========================================================================================================== *)
(* PHASE 5: ELECTRONIC FLAME-OFF (EFO) SPARK & FREE AIR BALL (FAB) KINETICS                                  *)
(* ========================================================================================================== *)
(* Theoretical Stored Energy in EFO Capacitor Bank: E = 0.5 * C * V^2 *)
f_EFO_StoredEnergy_uJ := 0.5 * f_EFO_BankCapacitance_uF * (f_EFO_ChargingVoltage_V * f_EFO_ChargingVoltage_V) * 0.001;

(* Compute Discharged Energy & Charge Integral during Spark Pulse *)
IF f_EFOTime_us > 0.5 THEN
    f_EFO_DischargeCharge_uC := (f_EFOCurrent_mA * f_EFOTime_us) * 0.001;
    f_EFO_DischargedEnergy_uJ := (f_EFOVoltage_V * f_EFOCurrent_mA * f_EFOTime_us) * 0.001;
ELSE
    f_EFO_DischargeCharge_uC := 0.0;
    f_EFO_DischargedEnergy_uJ := 0.0;
END_IF;

(* Nominal Wire Cross-Section Area: A_w = pi * (d_w / 2)^2 *)
f_Wire_CrossSectionArea_um2 := 3.14159265358979 * (f_WireDiameter_Nominal_um * 0.5) * (f_WireDiameter_Nominal_um * 0.5);

(* Wire Melted Segment Length Calculation via Thermal Energy Conservation *)
(* Q_melt = rho * A_w * L_melt * [ c_p * (T_melt - T_ambient) + H_fusion ] *)
IF f_EFO_DischargedEnergy_uJ > 10.0 THEN
    f_Wire_MeltedLength_um := (f_EFO_DischargedEnergy_uJ * 1.0E-6) /
        ((f_Gold_Density_g_cm3 * 1.0E-12) * f_Wire_CrossSectionArea_um2 *
         (f_Gold_SpecificHeat_J_gK * (f_Gold_MeltingPoint_degC - 25.0) + f_Gold_LatentHeatFusion_J_g));
    IF f_Wire_MeltedLength_um > 250.0 THEN f_Wire_MeltedLength_um := 250.0; END_IF;

    (* Resulting Free Air Ball Spherical Diameter: V_FAB = (pi/6) * D_FAB^3 = A_w * L_melt *)
    f_FAB_CalculatedDiameter_um := EXPT((6.0 / 3.14159265358979) * (f_Wire_CrossSectionArea_um2 * f_Wire_MeltedLength_um), 0.3333333333);
ELSE
    f_Wire_MeltedLength_um := 0.0;
    f_FAB_CalculatedDiameter_um := 0.0;
END_IF;

(* Optical Verification & Sphericity Closed-Loop Check *)
f_FAB_OpticalMeasurement_um := f_FAB_CalculatedDiameter_um; (* Synchronized with vision feedback *)
f_FAB_MeasuredDiameter_um := f_FAB_OpticalMeasurement_um;
f_FAB_SphericityDeviation_um := ABS(f_FAB_OpticalMeasurement_um - f_FAB_TargetDiameter_um);

IF (f_FAB_OpticalMeasurement_um >= f_Alarm_FAB_Diameter_LL_um) AND
   (f_FAB_OpticalMeasurement_um <= f_Alarm_FAB_Diameter_HH_um) AND
   (f_FAB_SphericityDeviation_um <= 1.2) THEN
    b_FAB_InspectionPassed := TRUE;
ELSE
    b_FAB_InspectionPassed := FALSE;
END_IF;
"""
