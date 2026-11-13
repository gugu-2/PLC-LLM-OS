# subsea_boosting_builder/st_phase1_tmr.py

def get_phase1_tmr():
    return """(* ==================================================================================================== *)
(* PHASE 0: SYSTEM INITIALIZATION & DISCRETE CYBER-PHYSICAL STATE-SPACE MATRIX INITIALIZATION           *)
(* Discrete Sample Time Ts = 20 [ms], 6x6 Full Coupled System Dynamics, Observer L & MPC Cost Matrices   *)
(* ==================================================================================================== *)
IF NOT bFirstScanDone THEN
    (* ------------------------------------------------------------------------------------------------ *)
    (* Step 0A: Discrete State Transition Matrix A (6x6) Initialization                                  *)
    (* States: P_suc [bar], P_dis [bar], GVF [%], c_acoustic [m/s], Delta_P [bar], Torque [kNm]         *)
    (* Physics: Fluid capacitance, gas compressibility, slip dynamics, helico-axial pressure build      *)
    (* ------------------------------------------------------------------------------------------------ *)
    matA[0, 0] := 0.9650; matA[0, 1] := 0.0125; matA[0, 2] := -0.0450; matA[0, 3] := 0.0080; matA[0, 4] := -0.0150; matA[0, 5] := 0.0020;
    matA[1, 0] := 0.0210; matA[1, 1] := 0.9480; matA[1, 2] := 0.0820; matA[1, 3] := -0.0120; matA[1, 4] := 0.0750; matA[1, 5] := 0.0140;
    matA[2, 0] := -0.0050; matA[2, 1] := 0.0085; matA[2, 2] := 0.9120; matA[2, 3] := -0.0350; matA[2, 4] := 0.0180; matA[2, 5] := -0.0060;
    matA[3, 0] := 0.0320; matA[3, 1] := -0.0240; matA[3, 2] := -0.1450; matA[3, 3] := 0.8850; matA[3, 4] := -0.0420; matA[3, 5] := 0.0085;
    matA[4, 0] := -0.0420; matA[4, 1] := 0.0650; matA[4, 2] := 0.0950; matA[4, 3] := -0.0180; matA[4, 4] := 0.9320; matA[4, 5] := 0.0280;
    matA[5, 0] := 0.0080; matA[5, 1] := 0.0180; matA[5, 2] := -0.0750; matA[5, 3] := 0.0040; matA[5, 4] := 0.0620; matA[5, 5] := 0.9540;

    (* ------------------------------------------------------------------------------------------------ *)
    (* Step 0B: Discrete Control Input Matrix B (6x6) Initialization                                     *)
    (* Controls: VFD [RPM], Kickback [%], MEG [%], Barrier [%], Choke [%], MistCooling [%]              *)
    (* ------------------------------------------------------------------------------------------------ *)
    matB[0, 0] := -0.0035; matB[0, 1] := 0.0480; matB[0, 2] := 0.0012; matB[0, 3] := 0.0000; matB[0, 4] := 0.0650; matB[0, 5] := 0.0045;
    matB[1, 0] := 0.0185; matB[1, 1] := -0.0920; matB[1, 2] := 0.0025; matB[1, 3] := 0.0000; matB[1, 4] := -0.0820; matB[1, 5] := -0.0080;
    matB[2, 0] := -0.0012; matB[2, 1] := -0.0150; matB[2, 2] := -0.0085; matB[2, 3] := 0.0000; matB[2, 4] := 0.0040; matB[2, 5] := -0.0250;
    matB[3, 0] := 0.0045; matB[3, 1] := 0.0280; matB[3, 2] := 0.0120; matB[3, 3] := 0.0000; matB[3, 4] := -0.0060; matB[3, 5] := 0.0380;
    matB[4, 0] := 0.0220; matB[4, 1] := -0.1400; matB[4, 2] := 0.0013; matB[4, 3] := 0.0000; matB[4, 4] := -0.1470; matB[4, 5] := -0.0125;
    matB[5, 0] := 0.0065; matB[5, 1] := -0.0380; matB[5, 2] := 0.0008; matB[5, 3] := 0.0000; matB[5, 4] := -0.0250; matB[5, 5] := 0.0185;

    (* ------------------------------------------------------------------------------------------------ *)
    (* Step 0C: Discrete Output Measurement Matrix C (6x6) Initialization                               *)
    (* Direct Scaled State Sensing: Direct Observation on Primary Diagonals                              *)
    (* ------------------------------------------------------------------------------------------------ *)
    matC[0, 0] := 1.0000; matC[0, 1] := 0.0000; matC[0, 2] := 0.0000; matC[0, 3] := 0.0000; matC[0, 4] := 0.0000; matC[0, 5] := 0.0000;
    matC[1, 0] := 0.0000; matC[1, 1] := 1.0000; matC[1, 2] := 0.0000; matC[1, 3] := 0.0000; matC[1, 4] := 0.0000; matC[1, 5] := 0.0000;
    matC[2, 0] := 0.0000; matC[2, 1] := 0.0000; matC[2, 2] := 1.0000; matC[2, 3] := 0.0000; matC[2, 4] := 0.0000; matC[2, 5] := 0.0000;
    matC[3, 0] := 0.0000; matC[3, 1] := 0.0000; matC[3, 2] := 0.0000; matC[3, 3] := 1.0000; matC[3, 4] := 0.0000; matC[3, 5] := 0.0000;
    matC[4, 0] := 0.0000; matC[4, 1] := 0.0000; matC[4, 2] := 0.0000; matC[4, 3] := 0.0000; matC[4, 4] := 1.0000; matC[4, 5] := 0.0000;
    matC[5, 0] := 0.0000; matC[5, 1] := 0.0000; matC[5, 2] := 0.0000; matC[5, 3] := 0.0000; matC[5, 4] := 0.0000; matC[5, 5] := 1.0000;

    (* ------------------------------------------------------------------------------------------------ *)
    (* Step 0D: Discrete Feedthrough Matrix D (6x6) Initialization (Strictly Proper Dynamics)           *)
    (* ------------------------------------------------------------------------------------------------ *)
    FOR mIdx := 0 TO 5 DO
        FOR nIdx := 0 TO 5 DO
            matD[mIdx, nIdx] := 0.0;
        END_FOR;
    END_FOR;

    (* ------------------------------------------------------------------------------------------------ *)
    (* Step 0E: Luenberger State Observer Innovation Gain Matrix L (6x6)                                 *)
    (* ------------------------------------------------------------------------------------------------ *)
    matL[0, 0] := 0.2850; matL[0, 1] := 0.0080; matL[0, 2] := -0.0120; matL[0, 3] := 0.0020; matL[0, 4] := -0.0050; matL[0, 5] := 0.0010;
    matL[1, 0] := 0.0120; matL[1, 1] := 0.3150; matL[1, 2] := 0.0240; matL[1, 3] := -0.0040; matL[1, 4] := 0.0180; matL[1, 5] := 0.0050;
    matL[2, 0] := -0.0020; matL[2, 1] := 0.0040; matL[2, 2] := 0.2950; matL[2, 3] := -0.0110; matL[2, 4] := 0.0060; matL[2, 5] := -0.0020;
    matL[3, 0] := 0.0090; matL[3, 1] := -0.0080; matL[3, 2] := -0.0450; matL[3, 3] := 0.2600; matL[3, 4] := -0.0120; matL[3, 5] := 0.0030;
    matL[4, 0] := -0.0140; matL[4, 1] := 0.0220; matL[4, 2] := 0.0310; matL[4, 3] := -0.0060; matL[4, 4] := 0.3200; matL[4, 5] := 0.0090;
    matL[5, 0] := 0.0030; matL[5, 1] := 0.0060; matL[5, 2] := -0.0220; matL[5, 3] := 0.0015; matL[5, 4] := 0.0190; matL[5, 5] := 0.2750;

    (* ------------------------------------------------------------------------------------------------ *)
    (* Step 0F: Model Predictive Control (MPC) Cost Functional Weighting Vectors                        *)
    (* ------------------------------------------------------------------------------------------------ *)
    vecQ_weight[0] := 14.50; (* Suction Pressure Regulation Penalty Q[0] *)
    vecQ_weight[1] := 18.00; (* Discharge Pressure Tracking Penalty Q[1] *)
    vecQ_weight[2] := 8.50;  (* Gas Volume Fraction Slugging Penalty Q[2] *)
    vecQ_weight[3] := 4.20;  (* Acoustic Velocity Damping Penalty Q[3] *)
    vecQ_weight[4] := 12.00; (* Twin-Screw Differential Pressure Penalty Q[4] *)
    vecQ_weight[5] := 6.80;  (* Absorbed Motor Shaft Torque Penalty Q[5] *)

    vecR_weight[0] := 0.45;  (* Subsea VFD Motor Speed Energy Penalty R[0] *)
    vecR_weight[1] := 1.85;  (* Anti-Surge Fast Kickback Recycling Penalty R[1] *)
    vecR_weight[2] := 0.95;  (* Chemical MEG Hydrate Inhibitor Dosing Penalty R[2] *)
    vecR_weight[3] := 0.35;  (* Barrier Fluid Charge Valve Action Penalty R[3] *)
    vecR_weight[4] := 1.20;  (* Production Export Choke Throttling Penalty R[4] *)
    vecR_weight[5] := 1.50;  (* Mist Cooling Liquid Recycle Penalty R[5] *)

    vecR_rate_weight[0] := 1.60; (* VFD Speed Slew Acceleration Penalty R_rate[0] *)
    vecR_rate_weight[1] := 0.85; (* Fast Kickback Valve Slew Penalty R_rate[1] *)
    vecR_rate_weight[2] := 1.40; (* MEG Metering Valve Slew Penalty R_rate[2] *)
    vecR_rate_weight[3] := 0.90; (* Barrier Charge Slew Penalty R_rate[3] *)
    vecR_rate_weight[4] := 2.10; (* Export Choke Slew Rate Penalty R_rate[4] *)
    vecR_rate_weight[5] := 1.80; (* Mist Cooling Valve Slew Penalty R_rate[5] *)

    vecP_terminal[0] := 38.00; (* Terminal Suction Pressure Lyapunov Weight P[0] *)
    vecP_terminal[1] := 45.00; (* Terminal Discharge Pressure Lyapunov Weight P[1] *)
    vecP_terminal[2] := 22.00; (* Terminal GVF Slugging Stability Weight P[2] *)
    vecP_terminal[3] := 12.50; (* Terminal Acoustic Sonic Stability Weight P[3] *)
    vecP_terminal[4] := 32.00; (* Terminal Differential Pressure Weight P[4] *)
    vecP_terminal[5] := 18.00; (* Terminal Hydraulic Torque Weight P[5] *)

    (* ------------------------------------------------------------------------------------------------ *)
    (* Step 0G: Physical Actuator Box Saturation Limits & Maximum Allowable Slew Rates                  *)
    (* ------------------------------------------------------------------------------------------------ *)
    vecU_min[0] := 1200.0; vecU_max[0] := 4500.0; vecU_slew_max[0] := 85.0;  (* VFD Motor Speed [RPM, RPM/s] *)
    vecU_min[1] := 0.0;    vecU_max[1] := 100.0;  vecU_slew_max[1] := 120.0; (* Kickback Recycle Valve [%, %/s] *)
    vecU_min[2] := 0.0;    vecU_max[2] := 100.0;  vecU_slew_max[2] := 15.0;  (* MEG Metering Valve [%, %/s] *)
    vecU_min[3] := 0.0;    vecU_max[3] := 100.0;  vecU_slew_max[3] := 25.0;  (* Barrier Accumulator Valve [%, %/s] *)
    vecU_min[4] := 0.0;    vecU_max[4] := 100.0;  vecU_slew_max[4] := 10.0;  (* Production Export Choke [%, %/s] *)
    vecU_min[5] := 0.0;    vecU_max[5] := 100.0;  vecU_slew_max[5] := 30.0;  (* Mist Cooling Liquid Valve [%, %/s] *)

    (* Nominal Operating Linearization Reference Setpoints *)
    vecX_nominal[0] := 45.0;  (* Suction Pressure Nominal [bar] *)
    vecX_nominal[1] := 115.0; (* Discharge Pressure Nominal [bar] *)
    vecX_nominal[2] := 65.0;  (* Multiphase GVF Nominal [%] *)
    vecX_nominal[3] := 185.0; (* Mixture Acoustic Velocity Nominal [m/s] *)
    vecX_nominal[4] := 70.0;  (* Twin-Screw DP Nominal [bar] *)
    vecX_nominal[5] := 12.5;  (* Shaft Hydraulic Torque Nominal [kNm] *)

    vecU_target[0] := 2850.0; (* Nominal VFD Speed [RPM] *)
    vecU_target[1] := 0.0;    (* Kickback Valve Closed in Normal Boosting [%] *)
    vecU_target[2] := 35.0;   (* Nominal MEG Injection Trim [%] *)
    vecU_target[3] := 15.0;   (* Barrier Accumulator Maintain Trim [%] *)
    vecU_target[4] := 80.0;   (* Production Choke Export Opening [%] *)
    vecU_target[5] := 0.0;    (* Mist Cooling Off in Nominal Liquid Fraction [%] *)

    FOR mIdx := 0 TO 5 DO
        vecX[mIdx] := vecX_nominal[mIdx];
        vecX_est[mIdx] := vecX_nominal[mIdx];
        vecX_ref[mIdx] := vecX_nominal[mIdx];
        vecU[mIdx] := vecU_target[mIdx];
        vecU_prev[mIdx] := vecU_target[mIdx];
        vecU_cmd[mIdx] := vecU_target[mIdx];
        vecU_rate[mIdx] := 0.0;
    END_FOR;

    bFirstScanDone := TRUE;
END_IF;

(* Continuous Task Timing Update *)
rTime_Accumulator_s := rTime_Accumulator_s + rCycleTime_s;

(* ==================================================================================================== *)
(* PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING WITH DISCREPANCY TIMERS                 *)
(* Channels: Suction Pressure (bar), Discharge Pressure (bar), GVF (%), Barrier Seal DP (bar)          *)
(* ==================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------- *)
(* 1.1: 2oo3 TMR Voting for Subsea Suction Manifold Quartz Pressure Transmitters (PT-101/102/103)       *)
(* ---------------------------------------------------------------------------------------------------- *)
rSuction_ChA_Val := rSuctionPress_PT1_bar;
rSuction_ChB_Val := rSuctionPress_PT2_bar;
rSuction_ChC_Val := rSuctionPress_PT3_bar;

(* Raw Transducer Plausibility & Out-of-Range Boundary Check *)
bSuction_ChA_Healthy := (rSuction_ChA_Val >= 0.5) AND (rSuction_ChA_Val <= 180.0);
bSuction_ChB_Healthy := (rSuction_ChB_Val >= 0.5) AND (rSuction_ChB_Val <= 180.0);
bSuction_ChC_Healthy := (rSuction_ChC_Val >= 0.5) AND (rSuction_ChC_Val <= 180.0);

(* Pairwise Sensor Discrepancy Calculations *)
IF bSuction_ChA_Healthy AND bSuction_ChB_Healthy THEN
    rSuction_Diff_AB := ABS(rSuction_ChA_Val - rSuction_ChB_Val);
ELSE
    rSuction_Diff_AB := 999.0;
END_IF;

IF bSuction_ChB_Healthy AND bSuction_ChC_Healthy THEN
    rSuction_Diff_BC := ABS(rSuction_ChB_Val - rSuction_ChC_Val);
ELSE
    rSuction_Diff_BC := 999.0;
END_IF;

IF bSuction_ChC_Healthy AND bSuction_ChA_Healthy THEN
    rSuction_Diff_CA := ABS(rSuction_ChC_Val - rSuction_ChA_Val);
ELSE
    rSuction_Diff_CA := 999.0;
END_IF;

(* Discrepancy Accumulation Timers *)
IF rSuction_Diff_AB > rSuction_DiscLimit_bar THEN
    tSuction_DiscTimer_AB_s := tSuction_DiscTimer_AB_s + rCycleTime_s;
ELSE
    IF tSuction_DiscTimer_AB_s > 0.0 THEN
        tSuction_DiscTimer_AB_s := tSuction_DiscTimer_AB_s - (rCycleTime_s * 2.0);
        IF tSuction_DiscTimer_AB_s < 0.0 THEN
            tSuction_DiscTimer_AB_s := 0.0;
        END_IF;
    END_IF;
END_IF;

IF rSuction_Diff_BC > rSuction_DiscLimit_bar THEN
    tSuction_DiscTimer_BC_s := tSuction_DiscTimer_BC_s + rCycleTime_s;
ELSE
    IF tSuction_DiscTimer_BC_s > 0.0 THEN
        tSuction_DiscTimer_BC_s := tSuction_DiscTimer_BC_s - (rCycleTime_s * 2.0);
        IF tSuction_DiscTimer_BC_s < 0.0 THEN
            tSuction_DiscTimer_BC_s := 0.0;
        END_IF;
    END_IF;
END_IF;

IF rSuction_Diff_CA > rSuction_DiscLimit_bar THEN
    tSuction_DiscTimer_CA_s := tSuction_DiscTimer_CA_s + rCycleTime_s;
ELSE
    IF tSuction_DiscTimer_CA_s > 0.0 THEN
        tSuction_DiscTimer_CA_s := tSuction_DiscTimer_CA_s - (rCycleTime_s * 2.0);
        IF tSuction_DiscTimer_CA_s < 0.0 THEN
            tSuction_DiscTimer_CA_s := 0.0;
        END_IF;
    END_IF;
END_IF;

(* Channel Fault & Degradation Isolation *)
IF (tSuction_DiscTimer_AB_s >= rSuction_DiscTripDelay_s) AND (tSuction_DiscTimer_CA_s >= rSuction_DiscTripDelay_s) THEN
    bSuction_ChA_Degraded := TRUE;
END_IF;

IF (tSuction_DiscTimer_AB_s >= rSuction_DiscTripDelay_s) AND (tSuction_DiscTimer_BC_s >= rSuction_DiscTripDelay_s) THEN
    bSuction_ChB_Degraded := TRUE;
END_IF;

IF (tSuction_DiscTimer_BC_s >= rSuction_DiscTripDelay_s) AND (tSuction_DiscTimer_CA_s >= rSuction_DiscTripDelay_s) THEN
    bSuction_ChC_Degraded := TRUE;
END_IF;

IF bReset THEN
    bSuction_ChA_Degraded := FALSE;
    bSuction_ChB_Degraded := FALSE;
    bSuction_ChC_Degraded := FALSE;
    tSuction_DiscTimer_AB_s := 0.0;
    tSuction_DiscTimer_BC_s := 0.0;
    tSuction_DiscTimer_CA_s := 0.0;
END_IF;

(* Determine Voting Operational Mode & Compute Raw Voted Value *)
IF (bSuction_ChA_Healthy AND NOT bSuction_ChA_Degraded) AND
   (bSuction_ChB_Healthy AND NOT bSuction_ChB_Degraded) AND
   (bSuction_ChC_Healthy AND NOT bSuction_ChC_Degraded) THEN
    (* Full 2oo3 Median Voting Architecture *)
    nSuction_VotingMode := 3;
    IF ((rSuction_ChA_Val >= rSuction_ChB_Val) AND (rSuction_ChA_Val <= rSuction_ChC_Val)) OR
       ((rSuction_ChA_Val >= rSuction_ChC_Val) AND (rSuction_ChA_Val <= rSuction_ChB_Val)) THEN
        rSuction_VotedRaw := rSuction_ChA_Val;
    ELSIF ((rSuction_ChB_Val >= rSuction_ChA_Val) AND (rSuction_ChB_Val <= rSuction_ChC_Val)) OR
          ((rSuction_ChB_Val >= rSuction_ChC_Val) AND (rSuction_ChB_Val <= rSuction_ChA_Val)) THEN
        rSuction_VotedRaw := rSuction_ChB_Val;
    ELSE
        rSuction_VotedRaw := rSuction_ChC_Val;
    END_IF;

ELSIF (bSuction_ChA_Healthy AND NOT bSuction_ChA_Degraded) AND
      (bSuction_ChB_Healthy AND NOT bSuction_ChB_Degraded) THEN
    (* Degraded 1oo2 Average Voting between A and B *)
    nSuction_VotingMode := 2;
    rSuction_VotedRaw := (rSuction_ChA_Val + rSuction_ChB_Val) * 0.5;

ELSIF (bSuction_ChB_Healthy AND NOT bSuction_ChB_Degraded) AND
      (bSuction_ChC_Healthy AND NOT bSuction_ChC_Degraded) THEN
    (* Degraded 1oo2 Average Voting between B and C *)
    nSuction_VotingMode := 2;
    rSuction_VotedRaw := (rSuction_ChB_Val + rSuction_ChC_Val) * 0.5;

ELSIF (bSuction_ChC_Healthy AND NOT bSuction_ChC_Degraded) AND
      (bSuction_ChA_Healthy AND NOT bSuction_ChA_Degraded) THEN
    (* Degraded 1oo2 Average Voting between C and A *)
    nSuction_VotingMode := 2;
    rSuction_VotedRaw := (rSuction_ChC_Val + rSuction_ChA_Val) * 0.5;

ELSIF (bSuction_ChA_Healthy AND NOT bSuction_ChA_Degraded) THEN
    (* Single Healthy Channel 1oo1 A *)
    nSuction_VotingMode := 1;
    rSuction_VotedRaw := rSuction_ChA_Val;

ELSIF (bSuction_ChB_Healthy AND NOT bSuction_ChB_Degraded) THEN
    (* Single Healthy Channel 1oo1 B *)
    nSuction_VotingMode := 1;
    rSuction_VotedRaw := rSuction_ChB_Val;

ELSIF (bSuction_ChC_Healthy AND NOT bSuction_ChC_Degraded) THEN
    (* Single Healthy Channel 1oo1 C *)
    nSuction_VotingMode := 1;
    rSuction_VotedRaw := rSuction_ChC_Val;

ELSE
    (* Complete TMR Voting Failure: Fallback to State Observer Model *)
    nSuction_VotingMode := 0;
    rSuction_VotedRaw := vecX_est[0];
END_IF;

(* Bumpless Slew Rate Limiter on Suction Pressure Output *)
IF ABS(rSuction_VotedRaw - rSuction_VotedFiltered) > (rBumplessSlewLimit_bar_s * rCycleTime_s) THEN
    IF rSuction_VotedRaw > rSuction_VotedFiltered THEN
        rSuction_VotedFiltered := rSuction_VotedFiltered + (rBumplessSlewLimit_bar_s * rCycleTime_s);
    ELSE
        rSuction_VotedFiltered := rSuction_VotedFiltered - (rBumplessSlewLimit_bar_s * rCycleTime_s);
    END_IF;
ELSE
    rSuction_VotedFiltered := rSuction_VotedRaw;
END_IF;
rVotedSuctionPress_bar := rSuction_VotedFiltered;

(* ---------------------------------------------------------------------------------------------------- *)
(* 1.2: 2oo3 TMR Voting for Subsea Discharge Manifold Quartz Pressure Transmitters (PT-201/202/203)     *)
(* ---------------------------------------------------------------------------------------------------- *)
rDischarge_ChA_Val := rDischargePress_PT1_bar;
rDischarge_ChB_Val := rDischargePress_PT2_bar;
rDischarge_ChC_Val := rDischargePress_PT3_bar;

bDischarge_ChA_Healthy := (rDischarge_ChA_Val >= 0.5) AND (rDischarge_ChA_Val <= 260.0);
bDischarge_ChB_Healthy := (rDischarge_ChB_Val >= 0.5) AND (rDischarge_ChB_Val <= 260.0);
bDischarge_ChC_Healthy := (rDischarge_ChC_Val >= 0.5) AND (rDischarge_ChC_Val <= 260.0);

IF bDischarge_ChA_Healthy AND bDischarge_ChB_Healthy THEN
    rDischarge_Diff_AB := ABS(rDischarge_ChA_Val - rDischarge_ChB_Val);
ELSE
    rDischarge_Diff_AB := 999.0;
END_IF;

IF bDischarge_ChB_Healthy AND bDischarge_ChC_Healthy THEN
    rDischarge_Diff_BC := ABS(rDischarge_ChB_Val - rDischarge_ChC_Val);
ELSE
    rDischarge_Diff_BC := 999.0;
END_IF;

IF bDischarge_ChC_Healthy AND bDischarge_ChA_Healthy THEN
    rDischarge_Diff_CA := ABS(rDischarge_ChC_Val - rDischarge_ChA_Val);
ELSE
    rDischarge_Diff_CA := 999.0;
END_IF;

IF rDischarge_Diff_AB > rDischarge_DiscLimit_bar THEN
    tDischarge_DiscTimer_AB_s := tDischarge_DiscTimer_AB_s + rCycleTime_s;
ELSE
    IF tDischarge_DiscTimer_AB_s > 0.0 THEN
        tDischarge_DiscTimer_AB_s := tDischarge_DiscTimer_AB_s - (rCycleTime_s * 2.0);
        IF tDischarge_DiscTimer_AB_s < 0.0 THEN
            tDischarge_DiscTimer_AB_s := 0.0;
        END_IF;
    END_IF;
END_IF;

IF rDischarge_Diff_BC > rDischarge_DiscLimit_bar THEN
    tDischarge_DiscTimer_BC_s := tDischarge_DiscTimer_BC_s + rCycleTime_s;
ELSE
    IF tDischarge_DiscTimer_BC_s > 0.0 THEN
        tDischarge_DiscTimer_BC_s := tDischarge_DiscTimer_BC_s - (rCycleTime_s * 2.0);
        IF tDischarge_DiscTimer_BC_s < 0.0 THEN
            tDischarge_DiscTimer_BC_s := 0.0;
        END_IF;
    END_IF;
END_IF;

IF rDischarge_Diff_CA > rDischarge_DiscLimit_bar THEN
    tDischarge_DiscTimer_CA_s := tDischarge_DiscTimer_CA_s + rCycleTime_s;
ELSE
    IF tDischarge_DiscTimer_CA_s > 0.0 THEN
        tDischarge_DiscTimer_CA_s := tDischarge_DiscTimer_CA_s - (rCycleTime_s * 2.0);
        IF tDischarge_DiscTimer_CA_s < 0.0 THEN
            tDischarge_DiscTimer_CA_s := 0.0;
        END_IF;
    END_IF;
END_IF;

IF (tDischarge_DiscTimer_AB_s >= rDischarge_DiscTripDelay_s) AND (tDischarge_DiscTimer_CA_s >= rDischarge_DiscTripDelay_s) THEN
    bDischarge_ChA_Degraded := TRUE;
END_IF;

IF (tDischarge_DiscTimer_AB_s >= rDischarge_DiscTripDelay_s) AND (tDischarge_DiscTimer_BC_s >= rDischarge_DiscTripDelay_s) THEN
    bDischarge_ChB_Degraded := TRUE;
END_IF;

IF (tDischarge_DiscTimer_BC_s >= rDischarge_DiscTripDelay_s) AND (tDischarge_DiscTimer_CA_s >= rDischarge_DiscTripDelay_s) THEN
    bDischarge_ChC_Degraded := TRUE;
END_IF;

IF bReset THEN
    bDischarge_ChA_Degraded := FALSE;
    bDischarge_ChB_Degraded := FALSE;
    bDischarge_ChC_Degraded := FALSE;
    tDischarge_DiscTimer_AB_s := 0.0;
    tDischarge_DiscTimer_BC_s := 0.0;
    tDischarge_DiscTimer_CA_s := 0.0;
END_IF;

IF (bDischarge_ChA_Healthy AND NOT bDischarge_ChA_Degraded) AND
   (bDischarge_ChB_Healthy AND NOT bDischarge_ChB_Degraded) AND
   (bDischarge_ChC_Healthy AND NOT bDischarge_ChC_Degraded) THEN
    nDischarge_VotingMode := 3;
    IF ((rDischarge_ChA_Val >= rDischarge_ChB_Val) AND (rDischarge_ChA_Val <= rDischarge_ChC_Val)) OR
       ((rDischarge_ChA_Val >= rDischarge_ChC_Val) AND (rDischarge_ChA_Val <= rDischarge_ChB_Val)) THEN
        rDischarge_VotedRaw := rDischarge_ChA_Val;
    ELSIF ((rDischarge_ChB_Val >= rDischarge_ChA_Val) AND (rDischarge_ChB_Val <= rDischarge_ChC_Val)) OR
          ((rDischarge_ChB_Val >= rDischarge_ChC_Val) AND (rDischarge_ChB_Val <= rDischarge_ChA_Val)) THEN
        rDischarge_VotedRaw := rDischarge_ChB_Val;
    ELSE
        rDischarge_VotedRaw := rDischarge_ChC_Val;
    END_IF;

ELSIF (bDischarge_ChA_Healthy AND NOT bDischarge_ChA_Degraded) AND
      (bDischarge_ChB_Healthy AND NOT bDischarge_ChB_Degraded) THEN
    nDischarge_VotingMode := 2;
    rDischarge_VotedRaw := (rDischarge_ChA_Val + rDischarge_ChB_Val) * 0.5;

ELSIF (bDischarge_ChB_Healthy AND NOT bDischarge_ChB_Degraded) AND
      (bDischarge_ChC_Healthy AND NOT bDischarge_ChC_Degraded) THEN
    nDischarge_VotingMode := 2;
    rDischarge_VotedRaw := (rDischarge_ChB_Val + rDischarge_ChC_Val) * 0.5;

ELSIF (bDischarge_ChC_Healthy AND NOT bDischarge_ChC_Degraded) AND
      (bDischarge_ChA_Healthy AND NOT bDischarge_ChA_Degraded) THEN
    nDischarge_VotingMode := 2;
    rDischarge_VotedRaw := (rDischarge_ChC_Val + rDischarge_ChA_Val) * 0.5;

ELSIF (bDischarge_ChA_Healthy AND NOT bDischarge_ChA_Degraded) THEN
    nDischarge_VotingMode := 1;
    rDischarge_VotedRaw := rDischarge_ChA_Val;

ELSIF (bDischarge_ChB_Healthy AND NOT bDischarge_ChB_Degraded) THEN
    nDischarge_VotingMode := 1;
    rDischarge_VotedRaw := rDischarge_ChB_Val;

ELSIF (bDischarge_ChC_Healthy AND NOT bDischarge_ChC_Degraded) THEN
    nDischarge_VotingMode := 1;
    rDischarge_VotedRaw := rDischarge_ChC_Val;

ELSE
    nDischarge_VotingMode := 0;
    rDischarge_VotedRaw := vecX_est[1];
END_IF;

IF ABS(rDischarge_VotedRaw - rDischarge_VotedFiltered) > (rBumplessSlewLimit_bar_s * rCycleTime_s) THEN
    IF rDischarge_VotedRaw > rDischarge_VotedFiltered THEN
        rDischarge_VotedFiltered := rDischarge_VotedFiltered + (rBumplessSlewLimit_bar_s * rCycleTime_s);
    ELSE
        rDischarge_VotedFiltered := rDischarge_VotedFiltered - (rBumplessSlewLimit_bar_s * rCycleTime_s);
    END_IF;
ELSE
    rDischarge_VotedFiltered := rDischarge_VotedRaw;
END_IF;
rVotedDischargePress_bar := rDischarge_VotedFiltered;

(* ---------------------------------------------------------------------------------------------------- *)
(* 1.3: 2oo3 TMR Voting for Inline Gamma-Ray Gas Volume Fraction (GVF) Meters (GVF-301/302/303)         *)
(* ---------------------------------------------------------------------------------------------------- *)
rGVF_ChA_Val := rGVF_Sensor1_pct;
rGVF_ChB_Val := rGVF_Sensor2_pct;
rGVF_ChC_Val := rGVF_Sensor3_pct;

bGVF_ChA_Healthy := (rGVF_ChA_Val >= 0.0) AND (rGVF_ChA_Val <= 100.0);
bGVF_ChB_Healthy := (rGVF_ChB_Val >= 0.0) AND (rGVF_ChB_Val <= 100.0);
bGVF_ChC_Healthy := (rGVF_ChC_Val >= 0.0) AND (rGVF_ChC_Val <= 100.0);

IF bGVF_ChA_Healthy AND bGVF_ChB_Healthy THEN
    rGVF_Diff_AB := ABS(rGVF_ChA_Val - rGVF_ChB_Val);
ELSE
    rGVF_Diff_AB := 999.0;
END_IF;

IF bGVF_ChB_Healthy AND bGVF_ChC_Healthy THEN
    rGVF_Diff_BC := ABS(rGVF_ChB_Val - rGVF_ChC_Val);
ELSE
    rGVF_Diff_BC := 999.0;
END_IF;

IF bGVF_ChC_Healthy AND bGVF_ChA_Healthy THEN
    rGVF_Diff_CA := ABS(rGVF_ChC_Val - rGVF_ChA_Val);
ELSE
    rGVF_Diff_CA := 999.0;
END_IF;

IF rGVF_Diff_AB > rGVF_DiscLimit_pct THEN
    tGVF_DiscTimer_AB_s := tGVF_DiscTimer_AB_s + rCycleTime_s;
ELSE
    IF tGVF_DiscTimer_AB_s > 0.0 THEN
        tGVF_DiscTimer_AB_s := tGVF_DiscTimer_AB_s - (rCycleTime_s * 2.0);
        IF tGVF_DiscTimer_AB_s < 0.0 THEN
            tGVF_DiscTimer_AB_s := 0.0;
        END_IF;
    END_IF;
END_IF;

IF rGVF_Diff_BC > rGVF_DiscLimit_pct THEN
    tGVF_DiscTimer_BC_s := tGVF_DiscTimer_BC_s + rCycleTime_s;
ELSE
    IF tGVF_DiscTimer_BC_s > 0.0 THEN
        tGVF_DiscTimer_BC_s := tGVF_DiscTimer_BC_s - (rCycleTime_s * 2.0);
        IF tGVF_DiscTimer_BC_s < 0.0 THEN
            tGVF_DiscTimer_BC_s := 0.0;
        END_IF;
    END_IF;
END_IF;

IF rGVF_Diff_CA > rGVF_DiscLimit_pct THEN
    tGVF_DiscTimer_CA_s := tGVF_DiscTimer_CA_s + rCycleTime_s;
ELSE
    IF tGVF_DiscTimer_CA_s > 0.0 THEN
        tGVF_DiscTimer_CA_s := tGVF_DiscTimer_CA_s - (rCycleTime_s * 2.0);
        IF tGVF_DiscTimer_CA_s < 0.0 THEN
            tGVF_DiscTimer_CA_s := 0.0;
        END_IF;
    END_IF;
END_IF;

IF (tGVF_DiscTimer_AB_s >= rGVF_DiscTripDelay_s) AND (tGVF_DiscTimer_CA_s >= rGVF_DiscTripDelay_s) THEN
    bGVF_ChA_Degraded := TRUE;
END_IF;

IF (tGVF_DiscTimer_AB_s >= rGVF_DiscTripDelay_s) AND (tGVF_DiscTimer_BC_s >= rGVF_DiscTripDelay_s) THEN
    bGVF_ChB_Degraded := TRUE;
END_IF;

IF (tGVF_DiscTimer_BC_s >= rGVF_DiscTripDelay_s) AND (tGVF_DiscTimer_CA_s >= rGVF_DiscTripDelay_s) THEN
    bGVF_ChC_Degraded := TRUE;
END_IF;

IF bReset THEN
    bGVF_ChA_Degraded := FALSE;
    bGVF_ChB_Degraded := FALSE;
    bGVF_ChC_Degraded := FALSE;
    tGVF_DiscTimer_AB_s := 0.0;
    tGVF_DiscTimer_BC_s := 0.0;
    tGVF_DiscTimer_CA_s := 0.0;
END_IF;

IF (bGVF_ChA_Healthy AND NOT bGVF_ChA_Degraded) AND
   (bGVF_ChB_Healthy AND NOT bGVF_ChB_Degraded) AND
   (bGVF_ChC_Healthy AND NOT bGVF_ChC_Degraded) THEN
    nGVF_VotingMode := 3;
    IF ((rGVF_ChA_Val >= rGVF_ChB_Val) AND (rGVF_ChA_Val <= rGVF_ChC_Val)) OR
       ((rGVF_ChA_Val >= rGVF_ChC_Val) AND (rGVF_ChA_Val <= rGVF_ChB_Val)) THEN
        rGVF_VotedRaw := rGVF_ChA_Val;
    ELSIF ((rGVF_ChB_Val >= rGVF_ChA_Val) AND (rGVF_ChB_Val <= rGVF_ChC_Val)) OR
          ((rGVF_ChB_Val >= rGVF_ChC_Val) AND (rGVF_ChB_Val <= rGVF_ChA_Val)) THEN
        rGVF_VotedRaw := rGVF_ChB_Val;
    ELSE
        rGVF_VotedRaw := rGVF_ChC_Val;
    END_IF;

ELSIF (bGVF_ChA_Healthy AND NOT bGVF_ChA_Degraded) AND
      (bGVF_ChB_Healthy AND NOT bGVF_ChB_Degraded) THEN
    nGVF_VotingMode := 2;
    rGVF_VotedRaw := (rGVF_ChA_Val + rGVF_ChB_Val) * 0.5;

ELSIF (bGVF_ChB_Healthy AND NOT bGVF_ChB_Degraded) AND
      (bGVF_ChC_Healthy AND NOT bGVF_ChC_Degraded) THEN
    nGVF_VotingMode := 2;
    rGVF_VotedRaw := (rGVF_ChB_Val + rGVF_ChC_Val) * 0.5;

ELSIF (bGVF_ChC_Healthy AND NOT bGVF_ChC_Degraded) AND
      (bGVF_ChA_Healthy AND NOT bGVF_ChA_Degraded) THEN
    nGVF_VotingMode := 2;
    rGVF_VotedRaw := (rGVF_ChC_Val + rGVF_ChA_Val) * 0.5;

ELSIF (bGVF_ChA_Healthy AND NOT bGVF_ChA_Degraded) THEN
    nGVF_VotingMode := 1;
    rGVF_VotedRaw := rGVF_ChA_Val;

ELSIF (bGVF_ChB_Healthy AND NOT bGVF_ChB_Degraded) THEN
    nGVF_VotingMode := 1;
    rGVF_VotedRaw := rGVF_ChB_Val;

ELSIF (bGVF_ChC_Healthy AND NOT bGVF_ChC_Degraded) THEN
    nGVF_VotingMode := 1;
    rGVF_VotedRaw := rGVF_ChC_Val;

ELSE
    nGVF_VotingMode := 0;
    rGVF_VotedRaw := vecX_est[2];
END_IF;

IF ABS(rGVF_VotedRaw - rGVF_VotedFiltered) > (rBumplessSlewLimit_pct_s * rCycleTime_s) THEN
    IF rGVF_VotedRaw > rGVF_VotedFiltered THEN
        rGVF_VotedFiltered := rGVF_VotedFiltered + (rBumplessSlewLimit_pct_s * rCycleTime_s);
    ELSE
        rGVF_VotedFiltered := rGVF_VotedFiltered - (rBumplessSlewLimit_pct_s * rCycleTime_s);
    END_IF;
ELSE
    rGVF_VotedFiltered := rGVF_VotedRaw;
END_IF;
rVotedGVF_pct := rGVF_VotedFiltered;

(* ---------------------------------------------------------------------------------------------------- *)
(* 1.4: 2oo3 TMR Voting for Subsea Barrier Fluid Seal Differential Pressure (PDT-401/402/403)           *)
(* ---------------------------------------------------------------------------------------------------- *)
rSealDP_ChA_Val := rSealDP_Sensor1_bar;
rSealDP_ChB_Val := rSealDP_Sensor2_bar;
rSealDP_ChC_Val := rSealDP_Sensor3_bar;

bSealDP_ChA_Healthy := (rSealDP_ChA_Val >= -5.0) AND (rSealDP_ChA_Val <= 110.0);
bSealDP_ChB_Healthy := (rSealDP_ChB_Val >= -5.0) AND (rSealDP_ChB_Val <= 110.0);
bSealDP_ChC_Healthy := (rSealDP_ChC_Val >= -5.0) AND (rSealDP_ChC_Val <= 110.0);

IF bSealDP_ChA_Healthy AND bSealDP_ChB_Healthy THEN
    rSealDP_Diff_AB := ABS(rSealDP_ChA_Val - rSealDP_ChB_Val);
ELSE
    rSealDP_Diff_AB := 999.0;
END_IF;

IF bSealDP_ChB_Healthy AND bSealDP_ChC_Healthy THEN
    rSealDP_Diff_BC := ABS(rSealDP_ChB_Val - rSealDP_ChC_Val);
ELSE
    rSealDP_Diff_BC := 999.0;
END_IF;

IF bSealDP_ChC_Healthy AND bSealDP_ChA_Healthy THEN
    rSealDP_Diff_CA := ABS(rSealDP_ChC_Val - rSealDP_ChA_Val);
ELSE
    rSealDP_Diff_CA := 999.0;
END_IF;

IF rSealDP_Diff_AB > rSealDP_DiscLimit_bar THEN
    tSealDP_DiscTimer_AB_s := tSealDP_DiscTimer_AB_s + rCycleTime_s;
ELSE
    IF tSealDP_DiscTimer_AB_s > 0.0 THEN
        tSealDP_DiscTimer_AB_s := tSealDP_DiscTimer_AB_s - (rCycleTime_s * 2.0);
        IF tSealDP_DiscTimer_AB_s < 0.0 THEN
            tSealDP_DiscTimer_AB_s := 0.0;
        END_IF;
    END_IF;
END_IF;

IF rSealDP_Diff_BC > rSealDP_DiscLimit_bar THEN
    tSealDP_DiscTimer_BC_s := tSealDP_DiscTimer_BC_s + rCycleTime_s;
ELSE
    IF tSealDP_DiscTimer_BC_s > 0.0 THEN
        tSealDP_DiscTimer_BC_s := tSealDP_DiscTimer_BC_s - (rCycleTime_s * 2.0);
        IF tSealDP_DiscTimer_BC_s < 0.0 THEN
            tSealDP_DiscTimer_BC_s := 0.0;
        END_IF;
    END_IF;
END_IF;

IF rSealDP_Diff_CA > rSealDP_DiscLimit_bar THEN
    tSealDP_DiscTimer_CA_s := tSealDP_DiscTimer_CA_s + rCycleTime_s;
ELSE
    IF tSealDP_DiscTimer_CA_s > 0.0 THEN
        tSealDP_DiscTimer_CA_s := tSealDP_DiscTimer_CA_s - (rCycleTime_s * 2.0);
        IF tSealDP_DiscTimer_CA_s < 0.0 THEN
            tSealDP_DiscTimer_CA_s := 0.0;
        END_IF;
    END_IF;
END_IF;

IF (tSealDP_DiscTimer_AB_s >= rSealDP_DiscTripDelay_s) AND (tSealDP_DiscTimer_CA_s >= rSealDP_DiscTripDelay_s) THEN
    bSealDP_ChA_Degraded := TRUE;
END_IF;

IF (tSealDP_DiscTimer_AB_s >= rSealDP_DiscTripDelay_s) AND (tSealDP_DiscTimer_BC_s >= rSealDP_DiscTripDelay_s) THEN
    bSealDP_ChB_Degraded := TRUE;
END_IF;

IF (tSealDP_DiscTimer_BC_s >= rSealDP_DiscTripDelay_s) AND (tSealDP_DiscTimer_CA_s >= rSealDP_DiscTripDelay_s) THEN
    bSealDP_ChC_Degraded := TRUE;
END_IF;

IF bReset THEN
    bSealDP_ChA_Degraded := FALSE;
    bSealDP_ChB_Degraded := FALSE;
    bSealDP_ChC_Degraded := FALSE;
    tSealDP_DiscTimer_AB_s := 0.0;
    tSealDP_DiscTimer_BC_s := 0.0;
    tSealDP_DiscTimer_CA_s := 0.0;
END_IF;

IF (bSealDP_ChA_Healthy AND NOT bSealDP_ChA_Degraded) AND
   (bSealDP_ChB_Healthy AND NOT bSealDP_ChB_Degraded) AND
   (bSealDP_ChC_Healthy AND NOT bSealDP_ChC_Degraded) THEN
    nSealDP_VotingMode := 3;
    IF ((rSealDP_ChA_Val >= rSealDP_ChB_Val) AND (rSealDP_ChA_Val <= rSealDP_ChC_Val)) OR
       ((rSealDP_ChA_Val >= rSealDP_ChC_Val) AND (rSealDP_ChA_Val <= rSealDP_ChB_Val)) THEN
        rSealDP_VotedRaw := rSealDP_ChA_Val;
    ELSIF ((rSealDP_ChB_Val >= rSealDP_ChA_Val) AND (rSealDP_ChB_Val <= rSealDP_ChC_Val)) OR
          ((rSealDP_ChB_Val >= rSealDP_ChC_Val) AND (rSealDP_ChB_Val <= rSealDP_ChA_Val)) THEN
        rSealDP_VotedRaw := rSealDP_ChB_Val;
    ELSE
        rSealDP_VotedRaw := rSealDP_ChC_Val;
    END_IF;

ELSIF (bSealDP_ChA_Healthy AND NOT bSealDP_ChA_Degraded) AND
      (bSealDP_ChB_Healthy AND NOT bSealDP_ChB_Degraded) THEN
    nSealDP_VotingMode := 2;
    rSealDP_VotedRaw := (rSealDP_ChA_Val + rSealDP_ChB_Val) * 0.5;

ELSIF (bSealDP_ChB_Healthy AND NOT bSealDP_ChB_Degraded) AND
      (bSealDP_ChC_Healthy AND NOT bSealDP_ChC_Degraded) THEN
    nSealDP_VotingMode := 2;
    rSealDP_VotedRaw := (rSealDP_ChB_Val + rSealDP_ChC_Val) * 0.5;

ELSIF (bSealDP_ChC_Healthy AND NOT bSealDP_ChC_Degraded) AND
      (bSealDP_ChA_Healthy AND NOT bSealDP_ChA_Degraded) THEN
    nSealDP_VotingMode := 2;
    rSealDP_VotedRaw := (rSealDP_ChC_Val + rSealDP_ChA_Val) * 0.5;

ELSIF (bSealDP_ChA_Healthy AND NOT bSealDP_ChA_Degraded) THEN
    nSealDP_VotingMode := 1;
    rSealDP_VotedRaw := rSealDP_ChA_Val;

ELSIF (bSealDP_ChB_Healthy AND NOT bSealDP_ChB_Degraded) THEN
    nSealDP_VotingMode := 1;
    rSealDP_VotedRaw := rSealDP_ChB_Val;

ELSIF (bSealDP_ChC_Healthy AND NOT bSealDP_ChC_Degraded) THEN
    nSealDP_VotingMode := 1;
    rSealDP_VotedRaw := rSealDP_ChC_Val;

ELSE
    nSealDP_VotingMode := 0;
    rSealDP_VotedRaw := 42.0; (* Safe fallback barrier pressure *)
END_IF;

IF ABS(rSealDP_VotedRaw - rSealDP_VotedFiltered) > (rBumplessSlewLimit_bar_s * rCycleTime_s) THEN
    IF rSealDP_VotedRaw > rSealDP_VotedFiltered THEN
        rSealDP_VotedFiltered := rSealDP_VotedFiltered + (rBumplessSlewLimit_bar_s * rCycleTime_s);
    ELSE
        rSealDP_VotedFiltered := rSealDP_VotedFiltered - (rBumplessSlewLimit_bar_s * rCycleTime_s);
    END_IF;
ELSE
    rSealDP_VotedFiltered := rSealDP_VotedRaw;
END_IF;
rVotedSealDP_bar := rSealDP_VotedFiltered;
"""
