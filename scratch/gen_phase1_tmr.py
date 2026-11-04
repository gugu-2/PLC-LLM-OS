# Phase 1: Matrix initialization & 2oo3 TMR Voting Engine for FB_Mining_SAG_BallMill_GrindingCircuit

def get_phase1():
    return """(* === PHASE 0: COLD-START CYBER-PHYSICAL MATRICES & CONTROL INITIALIZATION === *)
IF NOT bFirstScanInitialized THEN
    (* ----------------------------------------------------------------------------------------- *)
    (* DISCRETE SYSTEM DYNAMICS TRANSITION MATRIX A (8x8, Ts = 50 ms)                            *)
    (* States: [1] W_SAG, [2] V_slurry, [3] theta_toe, [4] P_SAG,                                *)
    (*         [5] L_sump, [6] rho_ovf, [7] W_BM_circ, [8] P80                                  *)
    (* ----------------------------------------------------------------------------------------- *)
    aMatrix_A[1,1] := 0.9982; aMatrix_A[1,2] := 0.0125; aMatrix_A[1,3] := 0.0000; aMatrix_A[1,4] := -0.0045;
    aMatrix_A[1,5] := 0.0000; aMatrix_A[1,6] := 0.0000; aMatrix_A[1,7] := 0.0035; aMatrix_A[1,8] := 0.0000;

    aMatrix_A[2,1] := 0.0015; aMatrix_A[2,2] := 0.9945; aMatrix_A[2,3] := 0.0000; aMatrix_A[2,4] := -0.0028;
    aMatrix_A[2,5] := 0.0000; aMatrix_A[2,6] := 0.0000; aMatrix_A[2,7] := 0.0018; aMatrix_A[2,8] := 0.0000;

    aMatrix_A[3,1] := 0.0042; aMatrix_A[3,2] := -0.0085; aMatrix_A[3,3] := 0.9820; aMatrix_A[3,4] := 0.0150;
    aMatrix_A[3,5] := 0.0000; aMatrix_A[3,6] := 0.0000; aMatrix_A[3,7] := 0.0000; aMatrix_A[3,8] := 0.0000;

    aMatrix_A[4,1] := 0.0085; aMatrix_A[4,2] := -0.0062; aMatrix_A[4,3] := 0.0245; aMatrix_A[4,4] := 0.9850;
    aMatrix_A[4,5] := 0.0000; aMatrix_A[4,6] := 0.0000; aMatrix_A[4,7] := 0.0000; aMatrix_A[4,8] := 0.0000;

    aMatrix_A[5,1] := 0.0000; aMatrix_A[5,2] := 0.0185; aMatrix_A[5,3] := 0.0000; aMatrix_A[5,4] := 0.0000;
    aMatrix_A[5,5] := 0.9910; aMatrix_A[5,6] := 0.0045; aMatrix_A[5,7] := 0.0092; aMatrix_A[5,8] := 0.0000;

    aMatrix_A[6,1] := 0.0000; aMatrix_A[6,2] := 0.0025; aMatrix_A[6,3] := 0.0000; aMatrix_A[6,4] := 0.0000;
    aMatrix_A[6,5] := 0.0035; aMatrix_A[6,6] := 0.9890; aMatrix_A[6,7] := 0.0055; aMatrix_A[6,8] := 0.0012;

    aMatrix_A[7,1] := 0.0045; aMatrix_A[7,2] := 0.0000; aMatrix_A[7,3] := 0.0000; aMatrix_A[7,4] := 0.0000;
    aMatrix_A[7,5] := 0.0125; aMatrix_A[7,6] := 0.0185; aMatrix_A[7,7] := 0.9860; aMatrix_A[7,8] := -0.0045;

    aMatrix_A[8,1] := 0.0018; aMatrix_A[8,2] := 0.0032; aMatrix_A[8,3] := -0.0025; aMatrix_A[8,4] := -0.0048;
    aMatrix_A[8,5] := 0.0000; aMatrix_A[8,6] := 0.0145; aMatrix_A[8,7] := 0.0085; aMatrix_A[8,8] := 0.9840;

    (* ----------------------------------------------------------------------------------------- *)
    (* DISCRETE ACTUATOR INPUT GAIN MATRIX B (8x8, Ts = 50 ms)                                   *)
    (* Inputs: [1] FeedRate, [2] WaterFlow, [3] MillSpeed, [4] PebbleFeed,                       *)
    (*         [5] PumpSpeed, [6] DilutionValve, [7] ActiveCyclones, [8] BM_FeedSplit            *)
    (* ----------------------------------------------------------------------------------------- *)
    aMatrix_B[1,1] := 0.0245; aMatrix_B[1,2] := 0.0000; aMatrix_B[1,3] := -0.0150; aMatrix_B[1,4] := 0.0185;
    aMatrix_B[1,5] := 0.0000; aMatrix_B[1,6] := 0.0000; aMatrix_B[1,7] := 0.0000; aMatrix_B[1,8] := 0.0000;

    aMatrix_B[2,1] := 0.0045; aMatrix_B[2,2] := 0.0285; aMatrix_B[2,3] := -0.0120; aMatrix_B[2,4] := 0.0000;
    aMatrix_B[2,5] := 0.0000; aMatrix_B[2,6] := 0.0000; aMatrix_B[2,7] := 0.0000; aMatrix_B[2,8] := 0.0000;

    aMatrix_B[3,1] := 0.0015; aMatrix_B[3,2] := -0.0045; aMatrix_B[3,3] := 0.0650; aMatrix_B[3,4] := 0.0000;
    aMatrix_B[3,5] := 0.0000; aMatrix_B[3,6] := 0.0000; aMatrix_B[3,7] := 0.0000; aMatrix_B[3,8] := 0.0000;

    aMatrix_B[4,1] := 0.0085; aMatrix_B[4,2] := -0.0025; aMatrix_B[4,3] := 0.0485; aMatrix_B[4,4] := 0.0055;
    aMatrix_B[4,5] := 0.0000; aMatrix_B[4,6] := 0.0000; aMatrix_B[4,7] := 0.0000; aMatrix_B[4,8] := 0.0000;

    aMatrix_B[5,1] := 0.0000; aMatrix_B[5,2] := 0.0000; aMatrix_B[5,3] := 0.0000; aMatrix_B[5,4] := 0.0000;
    aMatrix_B[5,5] := -0.0385; aMatrix_B[5,6] := 0.0245; aMatrix_B[5,7] := 0.0000; aMatrix_B[5,8] := 0.0000;

    aMatrix_B[6,1] := 0.0000; aMatrix_B[6,2] := 0.0000; aMatrix_B[6,3] := 0.0000; aMatrix_B[6,4] := 0.0000;
    aMatrix_B[6,5] := 0.0045; aMatrix_B[6,6] := -0.0285; aMatrix_B[6,7] := 0.0150; aMatrix_B[6,8] := 0.0000;

    aMatrix_B[7,1] := 0.0000; aMatrix_B[7,2] := 0.0000; aMatrix_B[7,3] := 0.0000; aMatrix_B[7,4] := 0.0000;
    aMatrix_B[7,5] := 0.0185; aMatrix_B[7,6] := 0.0000; aMatrix_B[7,7] := -0.0225; aMatrix_B[7,8] := 0.0350;

    aMatrix_B[8,1] := 0.0035; aMatrix_B[8,2] := -0.0015; aMatrix_B[8,3] := -0.0085; aMatrix_B[8,4] := 0.0000;
    aMatrix_B[8,5] := 0.0065; aMatrix_B[8,6] := -0.0145; aMatrix_B[8,7] := -0.0280; aMatrix_B[8,8] := -0.0185;

    (* ----------------------------------------------------------------------------------------- *)
    (* DISCRETE SENSOR OUTPUT MEASUREMENT MATRIX C (8x8 Identity Form)                           *)
    (* ----------------------------------------------------------------------------------------- *)
    FOR iLoopRow := 1 TO 8 DO
        FOR iLoopCol := 1 TO 8 DO
            IF iLoopRow = iLoopCol THEN
                aMatrix_C[iLoopRow, iLoopCol] := 1.0000;
            ELSE
                aMatrix_C[iLoopRow, iLoopCol] := 0.0000;
            END_IF;
            aMatrix_D[iLoopRow, iLoopCol] := 0.0000;
        END_FOR;
    END_FOR;

    (* ----------------------------------------------------------------------------------------- *)
    (* MPC QUADRATIC OBJECTIVE PENALTY WEIGHT VECTORS (Q, R, P)                                  *)
    (* ----------------------------------------------------------------------------------------- *)
    (* State penalty Q: high penalty on throughput W_SAG, toe angle, and product P80 *)
    aWeights_Q[1] := 2.50;  (* Charge mass error penalty *)
    aWeights_Q[2] := 1.80;  (* Slurry volume error penalty *)
    aWeights_Q[3] := 8.50;  (* Toe angle critical impact penalty *)
    aWeights_Q[4] := 1.50;  (* Motor power deviation penalty *)
    aWeights_Q[5] := 3.20;  (* Sump level surge penalty *)
    aWeights_Q[6] := 2.00;  (* Overflow density penalty *)
    aWeights_Q[7] := 1.20;  (* Ball mill recirculating load penalty *)
    aWeights_Q[8] := 12.00; (* Product P80 quality penalty (target: 75.0 um) *)

    (* Actuator slew rate penalty R: prevent aggressive actuator hunting *)
    aWeights_R[1] := 0.45;  (* Feed rate slew penalty *)
    aWeights_R[2] := 0.35;  (* Feed water slew penalty *)
    aWeights_R[3] := 4.50;  (* Ring motor speed slew penalty (high inertia) *)
    aWeights_R[4] := 0.25;  (* Pebble rate slew penalty *)
    aWeights_R[5] := 0.85;  (* Slurry pump speed slew penalty *)
    aWeights_R[6] := 0.30;  (* Sump dilution valve slew penalty *)
    aWeights_R[7] := 1.50;  (* Cyclone knife-gate switching penalty *)
    aWeights_R[8] := 0.40;  (* Ball mill split slew penalty *)

    (* Terminal penalty P: 2.5x of stage cost *)
    FOR iLoopRow := 1 TO 8 DO
        aWeights_P[iLoopRow] := aWeights_Q[iLoopRow] * 2.50;
    END_FOR;

    (* Physical Actuator Clamping Limits *)
    aMin_u[1] := 0.0;     aMax_u[1] := 4200.0;  aMaxSlewRate_u[1] := 15.0;  (* Fresh Feed [t/h] *)
    aMin_u[2] := 0.0;     aMax_u[2] := 1800.0;  aMaxSlewRate_u[2] := 10.0;  (* Feed Water [m3/h] *)
    aMin_u[3] := 6.5;     aMax_u[3] := 10.2;    aMaxSlewRate_u[3] := 0.02;  (* Motor Speed [rpm] *)
    aMin_u[4] := 0.0;     aMax_u[4] := 800.0;   aMaxSlewRate_u[4] := 5.0;   (* Pebble Feed [t/h] *)
    aMin_u[5] := 350.0;   aMax_u[5] := 750.0;   aMaxSlewRate_u[5] := 4.0;   (* Slurry Pump [rpm] *)
    aMin_u[6] := 0.0;     aMax_u[6] := 100.0;   aMaxSlewRate_u[6] := 2.0;   (* Sump Dilution [%] *)
    aMin_u[7] := 6.0;     aMax_u[7] := 16.0;    aMaxSlewRate_u[7] := 1.0;   (* Active Cyclones [cnt] *)
    aMin_u[8] := 1000.0;  aMax_u[8] := 2500.0;  aMaxSlewRate_u[8] := 10.0;  (* BM Split [t/h] *)

    (* Initialize State Vector Reference Targets *)
    aState_x_ref[1] := 1285.0; (* Nominal Charge Mass [t] *)
    aState_x_ref[2] := 265.0;  (* Nominal Slurry Volume [m3] *)
    aState_x_ref[3] := 42.5;   (* Nominal Toe Angle [deg] *)
    aState_x_ref[4] := 22.8;   (* Nominal Power Draw [MW] *)
    aState_x_ref[5] := 62.0;   (* Nominal Sump Level [%] *)
    aState_x_ref[6] := 1.285;  (* Nominal Overflow Density [t/m3] *)
    aState_x_ref[7] := 1850.0; (* Nominal Ball Mill Load [t/h] *)
    aState_x_ref[8] := 75.0;   (* Nominal Product P80 [um] *)

    FOR iLoopRow := 1 TO 8 DO
        aState_x[iLoopRow] := aState_x_ref[iLoopRow];
        aState_x_next[iLoopRow] := aState_x_ref[iLoopRow];
    END_FOR;

    bFirstScanInitialized := TRUE;
END_IF;

(* === PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) VOTING & FAULT DETECTION === *)

(* 1.1 Feed Trunnion Hydrostatic Lift Pressure Triplet (101A, 101B, 101C) *)
rDiff_FeedTrunnion_AB := ABS(PT_FEED_TRUNNION_LIFT_101A - PT_FEED_TRUNNION_LIFT_101B);
rDiff_FeedTrunnion_BC := ABS(PT_FEED_TRUNNION_LIFT_101B - PT_FEED_TRUNNION_LIFT_101C);
rDiff_FeedTrunnion_AC := ABS(PT_FEED_TRUNNION_LIFT_101A - PT_FEED_TRUNNION_LIFT_101C);

IF (rDiff_FeedTrunnion_AB > c_rTol_TrunnionLift_bar) OR
   (rDiff_FeedTrunnion_BC > c_rTol_TrunnionLift_bar) OR
   (rDiff_FeedTrunnion_AC > c_rTol_TrunnionLift_bar) THEN
    rTimer_FeedTrunnion_Disc := rTimer_FeedTrunnion_Disc + tExecutionScanTime_s;
    IF rTimer_FeedTrunnion_Disc >= c_rDiscrepancyTripTime_s THEN
        bFault_FeedTrunnion := TRUE;
        bGracefulDegradationActive := TRUE;
    END_IF;
ELSE
    rTimer_FeedTrunnion_Disc := 0.0;
    bFault_FeedTrunnion := FALSE;
END_IF;

(* Median Selection for Feed Trunnion Lift *)
IF (PT_FEED_TRUNNION_LIFT_101A >= PT_FEED_TRUNNION_LIFT_101B AND PT_FEED_TRUNNION_LIFT_101A <= PT_FEED_TRUNNION_LIFT_101C) OR
   (PT_FEED_TRUNNION_LIFT_101A <= PT_FEED_TRUNNION_LIFT_101B AND PT_FEED_TRUNNION_LIFT_101A >= PT_FEED_TRUNNION_LIFT_101C) THEN
    rVoted_FeedTrunnionLift_bar := PT_FEED_TRUNNION_LIFT_101A;
ELSIF (PT_FEED_TRUNNION_LIFT_101B >= PT_FEED_TRUNNION_LIFT_101A AND PT_FEED_TRUNNION_LIFT_101B <= PT_FEED_TRUNNION_LIFT_101C) OR
      (PT_FEED_TRUNNION_LIFT_101B <= PT_FEED_TRUNNION_LIFT_101A AND PT_FEED_TRUNNION_LIFT_101B >= PT_FEED_TRUNNION_LIFT_101C) THEN
    rVoted_FeedTrunnionLift_bar := PT_FEED_TRUNNION_LIFT_101B;
ELSE
    rVoted_FeedTrunnionLift_bar := PT_FEED_TRUNNION_LIFT_101C;
END_IF;

(* 1.2 Discharge Trunnion Hydrostatic Lift Pressure Triplet (102A, 102B, 102C) *)
rDiff_DischTrunnion_AB := ABS(PT_DISCH_TRUNNION_LIFT_102A - PT_DISCH_TRUNNION_LIFT_102B);
rDiff_DischTrunnion_BC := ABS(PT_DISCH_TRUNNION_LIFT_102B - PT_DISCH_TRUNNION_LIFT_102C);
rDiff_DischTrunnion_AC := ABS(PT_DISCH_TRUNNION_LIFT_102A - PT_DISCH_TRUNNION_LIFT_102C);

IF (rDiff_DischTrunnion_AB > c_rTol_TrunnionLift_bar) OR
   (rDiff_DischTrunnion_BC > c_rTol_TrunnionLift_bar) OR
   (rDiff_DischTrunnion_AC > c_rTol_TrunnionLift_bar) THEN
    rTimer_DischTrunnion_Disc := rTimer_DischTrunnion_Disc + tExecutionScanTime_s;
    IF rTimer_DischTrunnion_Disc >= c_rDiscrepancyTripTime_s THEN
        bFault_DischTrunnion := TRUE;
        bGracefulDegradationActive := TRUE;
    END_IF;
ELSE
    rTimer_DischTrunnion_Disc := 0.0;
    bFault_DischTrunnion := FALSE;
END_IF;

IF (PT_DISCH_TRUNNION_LIFT_102A >= PT_DISCH_TRUNNION_LIFT_102B AND PT_DISCH_TRUNNION_LIFT_102A <= PT_DISCH_TRUNNION_LIFT_102C) OR
   (PT_DISCH_TRUNNION_LIFT_102A <= PT_DISCH_TRUNNION_LIFT_102B AND PT_DISCH_TRUNNION_LIFT_102A >= PT_DISCH_TRUNNION_LIFT_102C) THEN
    rVoted_DischTrunnionLift_bar := PT_DISCH_TRUNNION_LIFT_102A;
ELSIF (PT_DISCH_TRUNNION_LIFT_102B >= PT_DISCH_TRUNNION_LIFT_102A AND PT_DISCH_TRUNNION_LIFT_102B <= PT_DISCH_TRUNNION_LIFT_102C) OR
      (PT_DISCH_TRUNNION_LIFT_102B <= PT_DISCH_TRUNNION_LIFT_102A AND PT_DISCH_TRUNNION_LIFT_102B >= PT_DISCH_TRUNNION_LIFT_102C) THEN
    rVoted_DischTrunnionLift_bar := PT_DISCH_TRUNNION_LIFT_102B;
ELSE
    rVoted_DischTrunnionLift_bar := PT_DISCH_TRUNNION_LIFT_102C;
END_IF;

(* 1.3 28 MW Gearless Ring Motor Active Power Triplet (105A, 105B, 105C) *)
rDiff_MotorPower_AB := ABS(JT_SAG_MOTOR_POWER_MW_105A - JT_SAG_MOTOR_POWER_MW_105B);
rDiff_MotorPower_BC := ABS(JT_SAG_MOTOR_POWER_MW_105B - JT_SAG_MOTOR_POWER_MW_105C);
rDiff_MotorPower_AC := ABS(JT_SAG_MOTOR_POWER_MW_105A - JT_SAG_MOTOR_POWER_MW_105C);

IF (rDiff_MotorPower_AB > c_rTol_MotorPower_MW) OR
   (rDiff_MotorPower_BC > c_rTol_MotorPower_MW) OR
   (rDiff_MotorPower_AC > c_rTol_MotorPower_MW) THEN
    rTimer_MotorPower_Disc := rTimer_MotorPower_Disc + tExecutionScanTime_s;
    IF rTimer_MotorPower_Disc >= c_rDiscrepancyTripTime_s THEN
        bFault_MotorPower := TRUE;
    END_IF;
ELSE
    rTimer_MotorPower_Disc := 0.0;
    bFault_MotorPower := FALSE;
END_IF;

IF (JT_SAG_MOTOR_POWER_MW_105A >= JT_SAG_MOTOR_POWER_MW_105B AND JT_SAG_MOTOR_POWER_MW_105A <= JT_SAG_MOTOR_POWER_MW_105C) OR
   (JT_SAG_MOTOR_POWER_MW_105A <= JT_SAG_MOTOR_POWER_MW_105B AND JT_SAG_MOTOR_POWER_MW_105A >= JT_SAG_MOTOR_POWER_MW_105C) THEN
    rVoted_MotorPower_MW := JT_SAG_MOTOR_POWER_MW_105A;
ELSIF (JT_SAG_MOTOR_POWER_MW_105B >= JT_SAG_MOTOR_POWER_MW_105A AND JT_SAG_MOTOR_POWER_MW_105B <= JT_SAG_MOTOR_POWER_MW_105C) OR
      (JT_SAG_MOTOR_POWER_MW_105B <= JT_SAG_MOTOR_POWER_MW_105A AND JT_SAG_MOTOR_POWER_MW_105B >= JT_SAG_MOTOR_POWER_MW_105C) THEN
    rVoted_MotorPower_MW := JT_SAG_MOTOR_POWER_MW_105B;
ELSE
    rVoted_MotorPower_MW := JT_SAG_MOTOR_POWER_MW_105C;
END_IF;

(* 1.4 Ring Motor Rotational Speed Triplet (106A, 106B, 106C) *)
rDiff_MotorSpeed_AB := ABS(ST_SAG_MOTOR_SPEED_RPM_106A - ST_SAG_MOTOR_SPEED_RPM_106B);
rDiff_MotorSpeed_BC := ABS(ST_SAG_MOTOR_SPEED_RPM_106B - ST_SAG_MOTOR_SPEED_RPM_106C);
rDiff_MotorSpeed_AC := ABS(ST_SAG_MOTOR_SPEED_RPM_106A - ST_SAG_MOTOR_SPEED_RPM_106C);

IF (rDiff_MotorSpeed_AB > c_rTol_MotorSpeed_rpm) OR
   (rDiff_MotorSpeed_BC > c_rTol_MotorSpeed_rpm) OR
   (rDiff_MotorSpeed_AC > c_rTol_MotorSpeed_rpm) THEN
    rTimer_MotorSpeed_Disc := rTimer_MotorSpeed_Disc + tExecutionScanTime_s;
    IF rTimer_MotorSpeed_Disc >= c_rDiscrepancyTripTime_s THEN
        bFault_MotorSpeed := TRUE;
    END_IF;
ELSE
    rTimer_MotorSpeed_Disc := 0.0;
    bFault_MotorSpeed := FALSE;
END_IF;

IF (ST_SAG_MOTOR_SPEED_RPM_106A >= ST_SAG_MOTOR_SPEED_RPM_106B AND ST_SAG_MOTOR_SPEED_RPM_106A <= ST_SAG_MOTOR_SPEED_RPM_106C) OR
   (ST_SAG_MOTOR_SPEED_RPM_106A <= ST_SAG_MOTOR_SPEED_RPM_106B AND ST_SAG_MOTOR_SPEED_RPM_106A >= ST_SAG_MOTOR_SPEED_RPM_106C) THEN
    rVoted_MotorSpeed_rpm := ST_SAG_MOTOR_SPEED_RPM_106A;
ELSIF (ST_SAG_MOTOR_SPEED_RPM_106B >= ST_SAG_MOTOR_SPEED_RPM_106A AND ST_SAG_MOTOR_SPEED_RPM_106B <= ST_SAG_MOTOR_SPEED_RPM_106C) OR
      (ST_SAG_MOTOR_SPEED_RPM_106B <= ST_SAG_MOTOR_SPEED_RPM_106A AND ST_SAG_MOTOR_SPEED_RPM_106B >= ST_SAG_MOTOR_SPEED_RPM_106C) THEN
    rVoted_MotorSpeed_rpm := ST_SAG_MOTOR_SPEED_RPM_106B;
ELSE
    rVoted_MotorSpeed_rpm := ST_SAG_MOTOR_SPEED_RPM_106C;
END_IF;

(* 1.5 Shell Acoustic Microphone Array Toe Station Triplet (110A, 110B, 110C) *)
rDiff_AcousticToe_AB := ABS(AT_SHELL_ACOUSTIC_TOE_DB_110A - AT_SHELL_ACOUSTIC_TOE_DB_110B);
rDiff_AcousticToe_BC := ABS(AT_SHELL_ACOUSTIC_TOE_DB_110B - AT_SHELL_ACOUSTIC_TOE_DB_110C);
rDiff_AcousticToe_AC := ABS(AT_SHELL_ACOUSTIC_TOE_DB_110A - AT_SHELL_ACOUSTIC_TOE_DB_110C);

IF (rDiff_AcousticToe_AB > c_rTol_ShellAcoustic_dB) OR
   (rDiff_AcousticToe_BC > c_rTol_ShellAcoustic_dB) OR
   (rDiff_AcousticToe_AC > c_rTol_ShellAcoustic_dB) THEN
    rTimer_AcousticToe_Disc := rTimer_AcousticToe_Disc + tExecutionScanTime_s;
    IF rTimer_AcousticToe_Disc >= c_rDiscrepancyTripTime_s THEN
        bFault_AcousticToe := TRUE;
    END_IF;
ELSE
    rTimer_AcousticToe_Disc := 0.0;
    bFault_AcousticToe := FALSE;
END_IF;

IF (AT_SHELL_ACOUSTIC_TOE_DB_110A >= AT_SHELL_ACOUSTIC_TOE_DB_110B AND AT_SHELL_ACOUSTIC_TOE_DB_110A <= AT_SHELL_ACOUSTIC_TOE_DB_110C) OR
   (AT_SHELL_ACOUSTIC_TOE_DB_110A <= AT_SHELL_ACOUSTIC_TOE_DB_110B AND AT_SHELL_ACOUSTIC_TOE_DB_110A >= AT_SHELL_ACOUSTIC_TOE_DB_110C) THEN
    rVoted_ShellAcousticToe_dB := AT_SHELL_ACOUSTIC_TOE_DB_110A;
ELSIF (AT_SHELL_ACOUSTIC_TOE_DB_110B >= AT_SHELL_ACOUSTIC_TOE_DB_110A AND AT_SHELL_ACOUSTIC_TOE_DB_110B <= AT_SHELL_ACOUSTIC_TOE_DB_110C) OR
      (AT_SHELL_ACOUSTIC_TOE_DB_110B <= AT_SHELL_ACOUSTIC_TOE_DB_110A AND AT_SHELL_ACOUSTIC_TOE_DB_110B >= AT_SHELL_ACOUSTIC_TOE_DB_110C) THEN
    rVoted_ShellAcousticToe_dB := AT_SHELL_ACOUSTIC_TOE_DB_110B;
ELSE
    rVoted_ShellAcousticToe_dB := AT_SHELL_ACOUSTIC_TOE_DB_110C;
END_IF;

(* 1.6 Shell Acoustic High-Frequency Direct Impact Band Triplet (111A, 111B, 111C) *)
rDiff_AcousticHighFreq_AB := ABS(AT_SHELL_ACOUSTIC_HIGH_FREQ_DB_111A - AT_SHELL_ACOUSTIC_HIGH_FREQ_DB_111B);
rDiff_AcousticHighFreq_BC := ABS(AT_SHELL_ACOUSTIC_HIGH_FREQ_DB_111B - AT_SHELL_ACOUSTIC_HIGH_FREQ_DB_111C);
rDiff_AcousticHighFreq_AC := ABS(AT_SHELL_ACOUSTIC_HIGH_FREQ_DB_111A - AT_SHELL_ACOUSTIC_HIGH_FREQ_DB_111C);

IF (rDiff_AcousticHighFreq_AB > c_rTol_ShellAcoustic_dB) OR
   (rDiff_AcousticHighFreq_BC > c_rTol_ShellAcoustic_dB) OR
   (rDiff_AcousticHighFreq_AC > c_rTol_ShellAcoustic_dB) THEN
    rTimer_AcousticHighFreq_Disc := rTimer_AcousticHighFreq_Disc + tExecutionScanTime_s;
    IF rTimer_AcousticHighFreq_Disc >= c_rDiscrepancyTripTime_s THEN
        bFault_AcousticHighFreq := TRUE;
    END_IF;
ELSE
    rTimer_AcousticHighFreq_Disc := 0.0;
    bFault_AcousticHighFreq := FALSE;
END_IF;

IF (AT_SHELL_ACOUSTIC_HIGH_FREQ_DB_111A >= AT_SHELL_ACOUSTIC_HIGH_FREQ_DB_111B AND AT_SHELL_ACOUSTIC_HIGH_FREQ_DB_111A <= AT_SHELL_ACOUSTIC_HIGH_FREQ_DB_111C) OR
   (AT_SHELL_ACOUSTIC_HIGH_FREQ_DB_111A <= AT_SHELL_ACOUSTIC_HIGH_FREQ_DB_111B AND AT_SHELL_ACOUSTIC_HIGH_FREQ_DB_111A >= AT_SHELL_ACOUSTIC_HIGH_FREQ_DB_111C) THEN
    rVoted_ShellAcousticHighFreq_dB := AT_SHELL_ACOUSTIC_HIGH_FREQ_DB_111A;
ELSIF (AT_SHELL_ACOUSTIC_HIGH_FREQ_DB_111B >= AT_SHELL_ACOUSTIC_HIGH_FREQ_DB_111A AND AT_SHELL_ACOUSTIC_HIGH_FREQ_DB_111B <= AT_SHELL_ACOUSTIC_HIGH_FREQ_DB_111C) OR
      (AT_SHELL_ACOUSTIC_HIGH_FREQ_DB_111B <= AT_SHELL_ACOUSTIC_HIGH_FREQ_DB_111A AND AT_SHELL_ACOUSTIC_HIGH_FREQ_DB_111B >= AT_SHELL_ACOUSTIC_HIGH_FREQ_DB_111C) THEN
    rVoted_ShellAcousticHighFreq_dB := AT_SHELL_ACOUSTIC_HIGH_FREQ_DB_111B;
ELSE
    rVoted_ShellAcousticHighFreq_dB := AT_SHELL_ACOUSTIC_HIGH_FREQ_DB_111C;
END_IF;

(* 1.7 Cyclone Feed Sump Level Triplet (201A, 201B, 201C) *)
rDiff_SumpLevel_AB := ABS(LT_CYCLONE_SUMP_LEVEL_PCT_201A - LT_CYCLONE_SUMP_LEVEL_PCT_201B);
rDiff_SumpLevel_BC := ABS(LT_CYCLONE_SUMP_LEVEL_PCT_201B - LT_CYCLONE_SUMP_LEVEL_PCT_201C);
rDiff_SumpLevel_AC := ABS(LT_CYCLONE_SUMP_LEVEL_PCT_201A - LT_CYCLONE_SUMP_LEVEL_PCT_201C);

IF (rDiff_SumpLevel_AB > c_rTol_SumpLevel_pct) OR
   (rDiff_SumpLevel_BC > c_rTol_SumpLevel_pct) OR
   (rDiff_SumpLevel_AC > c_rTol_SumpLevel_pct) THEN
    rTimer_SumpLevel_Disc := rTimer_SumpLevel_Disc + tExecutionScanTime_s;
    IF rTimer_SumpLevel_Disc >= c_rDiscrepancyTripTime_s THEN
        bFault_SumpLevel := TRUE;
    END_IF;
ELSE
    rTimer_SumpLevel_Disc := 0.0;
    bFault_SumpLevel := FALSE;
END_IF;

IF (LT_CYCLONE_SUMP_LEVEL_PCT_201A >= LT_CYCLONE_SUMP_LEVEL_PCT_201B AND LT_CYCLONE_SUMP_LEVEL_PCT_201A <= LT_CYCLONE_SUMP_LEVEL_PCT_201C) OR
   (LT_CYCLONE_SUMP_LEVEL_PCT_201A <= LT_CYCLONE_SUMP_LEVEL_PCT_201B AND LT_CYCLONE_SUMP_LEVEL_PCT_201A >= LT_CYCLONE_SUMP_LEVEL_PCT_201C) THEN
    rVoted_SumpLevel_pct := LT_CYCLONE_SUMP_LEVEL_PCT_201A;
ELSIF (LT_CYCLONE_SUMP_LEVEL_PCT_201B >= LT_CYCLONE_SUMP_LEVEL_PCT_201A AND LT_CYCLONE_SUMP_LEVEL_PCT_201B <= LT_CYCLONE_SUMP_LEVEL_PCT_201C) OR
      (LT_CYCLONE_SUMP_LEVEL_PCT_201B <= LT_CYCLONE_SUMP_LEVEL_PCT_201A AND LT_CYCLONE_SUMP_LEVEL_PCT_201B >= LT_CYCLONE_SUMP_LEVEL_PCT_201C) THEN
    rVoted_SumpLevel_pct := LT_CYCLONE_SUMP_LEVEL_PCT_201B;
ELSE
    rVoted_SumpLevel_pct := LT_CYCLONE_SUMP_LEVEL_PCT_201C;
END_IF;

(* 1.8 Cyclone Feed Slurry Nuclear Density Gauge Triplet (202A, 202B, 202C) *)
rDiff_FeedDensity_AB := ABS(DT_CYCLONE_FEED_DENSITY_SG_202A - DT_CYCLONE_FEED_DENSITY_SG_202B);
rDiff_FeedDensity_BC := ABS(DT_CYCLONE_FEED_DENSITY_SG_202B - DT_CYCLONE_FEED_DENSITY_SG_202C);
rDiff_FeedDensity_AC := ABS(DT_CYCLONE_FEED_DENSITY_SG_202A - DT_CYCLONE_FEED_DENSITY_SG_202C);

IF (rDiff_FeedDensity_AB > c_rTol_FeedDensity_SG) OR
   (rDiff_FeedDensity_BC > c_rTol_FeedDensity_SG) OR
   (rDiff_FeedDensity_AC > c_rTol_FeedDensity_SG) THEN
    rTimer_FeedDensity_Disc := rTimer_FeedDensity_Disc + tExecutionScanTime_s;
    IF rTimer_FeedDensity_Disc >= c_rDiscrepancyTripTime_s THEN
        bFault_FeedDensity := TRUE;
    END_IF;
ELSE
    rTimer_FeedDensity_Disc := 0.0;
    bFault_FeedDensity := FALSE;
END_IF;

IF (DT_CYCLONE_FEED_DENSITY_SG_202A >= DT_CYCLONE_FEED_DENSITY_SG_202B AND DT_CYCLONE_FEED_DENSITY_SG_202A <= DT_CYCLONE_FEED_DENSITY_SG_202C) OR
   (DT_CYCLONE_FEED_DENSITY_SG_202A <= DT_CYCLONE_FEED_DENSITY_SG_202B AND DT_CYCLONE_FEED_DENSITY_SG_202A >= DT_CYCLONE_FEED_DENSITY_SG_202C) THEN
    rVoted_CycloneFeedDensity_SG := DT_CYCLONE_FEED_DENSITY_SG_202A;
ELSIF (DT_CYCLONE_FEED_DENSITY_SG_202B >= DT_CYCLONE_FEED_DENSITY_SG_202A AND DT_CYCLONE_FEED_DENSITY_SG_202B <= DT_CYCLONE_FEED_DENSITY_SG_202C) OR
      (DT_CYCLONE_FEED_DENSITY_SG_202B <= DT_CYCLONE_FEED_DENSITY_SG_202A AND DT_CYCLONE_FEED_DENSITY_SG_202B >= DT_CYCLONE_FEED_DENSITY_SG_202C) THEN
    rVoted_CycloneFeedDensity_SG := DT_CYCLONE_FEED_DENSITY_SG_202B;
ELSE
    rVoted_CycloneFeedDensity_SG := DT_CYCLONE_FEED_DENSITY_SG_202C;
END_IF;

(* 1.9 In-Line Ultrasonic Attenuation Particle Size P80 Triplet (401A, 401B, 401C) *)
rDiff_ProductP80_AB := ABS(AT_OVERFLOW_P80_MICRONS_401A - AT_OVERFLOW_P80_MICRONS_401B);
rDiff_ProductP80_BC := ABS(AT_OVERFLOW_P80_MICRONS_401B - AT_OVERFLOW_P80_MICRONS_401C);
rDiff_ProductP80_AC := ABS(AT_OVERFLOW_P80_MICRONS_401A - AT_OVERFLOW_P80_MICRONS_401C);

IF (rDiff_ProductP80_AB > c_rTol_ProductP80_um) OR
   (rDiff_ProductP80_BC > c_rTol_ProductP80_um) OR
   (rDiff_ProductP80_AC > c_rTol_ProductP80_um) THEN
    rTimer_ProductP80_Disc := rTimer_ProductP80_Disc + tExecutionScanTime_s;
    IF rTimer_ProductP80_Disc >= c_rDiscrepancyTripTime_s THEN
        bFault_ProductP80 := TRUE;
    END_IF;
ELSE
    rTimer_ProductP80_Disc := 0.0;
    bFault_ProductP80 := FALSE;
END_IF;

IF (AT_OVERFLOW_P80_MICRONS_401A >= AT_OVERFLOW_P80_MICRONS_401B AND AT_OVERFLOW_P80_MICRONS_401A <= AT_OVERFLOW_P80_MICRONS_401C) OR
   (AT_OVERFLOW_P80_MICRONS_401A <= AT_OVERFLOW_P80_MICRONS_401B AND AT_OVERFLOW_P80_MICRONS_401A >= AT_OVERFLOW_P80_MICRONS_401C) THEN
    rVoted_ProductP80_um := AT_OVERFLOW_P80_MICRONS_401A;
ELSIF (AT_OVERFLOW_P80_MICRONS_401B >= AT_OVERFLOW_P80_MICRONS_401A AND AT_OVERFLOW_P80_MICRONS_401B <= AT_OVERFLOW_P80_MICRONS_401C) OR
      (AT_OVERFLOW_P80_MICRONS_401B <= AT_OVERFLOW_P80_MICRONS_401A AND AT_OVERFLOW_P80_MICRONS_401B >= AT_OVERFLOW_P80_MICRONS_401C) THEN
    rVoted_ProductP80_um := AT_OVERFLOW_P80_MICRONS_401B;
ELSE
    rVoted_ProductP80_um := AT_OVERFLOW_P80_MICRONS_401C;
END_IF;
"""
