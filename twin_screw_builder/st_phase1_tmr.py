(* =====================================================================================================================
 * PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) VOTING WITH DISCREPANCY TIMERS & BUMPLESS DEGRADATION
 * ===================================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------------------------
 * CHANNEL 1: DIE HEAD MELT PRESSURE PT-101 (A, B, C)
 * Range: 0.0 to 350.0 bar | Permissible Discrepancy: 8.0 bar | Persistence Filter Timeout: 150 ms
 * --------------------------------------------------------------------------------------------------------------------- *)
(* Step 1.1: Calculate Pairwise Absolute Deviations *)
rDiff_DMP_AB := ABS(rDieMeltPres_SensA_In - rDieMeltPres_SensB_In);
rDiff_DMP_BC := ABS(rDieMeltPres_SensB_In - rDieMeltPres_SensC_In);
rDiff_DMP_CA := ABS(rDieMeltPres_SensC_In - rDieMeltPres_SensA_In);

(* Step 1.2: Integrate Discrepancy Persistence Timers with Leaky Bucket Hysteresis *)
IF rDiff_DMP_AB > rTol_DieMeltPres THEN
    tTimer_DMP_AB := tTimer_DMP_AB + T_SAMPLE;
ELSE
    IF tTimer_DMP_AB > 0.0 THEN
        tTimer_DMP_AB := tTimer_DMP_AB - (0.5 * T_SAMPLE);
    ELSE
        tTimer_DMP_AB := 0.0;
    END_IF;
END_IF;

IF rDiff_DMP_BC > rTol_DieMeltPres THEN
    tTimer_DMP_BC := tTimer_DMP_BC + T_SAMPLE;
ELSE
    IF tTimer_DMP_BC > 0.0 THEN
        tTimer_DMP_BC := tTimer_DMP_BC - (0.5 * T_SAMPLE);
    ELSE
        tTimer_DMP_BC := 0.0;
    END_IF;
END_IF;

IF rDiff_DMP_CA > rTol_DieMeltPres THEN
    tTimer_DMP_CA := tTimer_DMP_CA + T_SAMPLE;
ELSE
    IF tTimer_DMP_CA > 0.0 THEN
        tTimer_DMP_CA := tTimer_DMP_CA - (0.5 * T_SAMPLE);
    ELSE
        tTimer_DMP_CA := 0.0;
    END_IF;
END_IF;

(* Step 1.3: Electrical Hardware Range & Wire-Break Plausibility Verification *)
IF (rDieMeltPres_SensA_In < -5.0) OR (rDieMeltPres_SensA_In > 350.0) THEN
    bHealth_DMP_A := FALSE;
END_IF;

IF (rDieMeltPres_SensB_In < -5.0) OR (rDieMeltPres_SensB_In > 350.0) THEN
    bHealth_DMP_B := FALSE;
END_IF;

IF (rDieMeltPres_SensC_In < -5.0) OR (rDieMeltPres_SensC_In > 350.0) THEN
    bHealth_DMP_C := FALSE;
END_IF;

(* Step 1.4: Cross-Channel Persistent Divergence Isolation *)
IF (tTimer_DMP_AB >= tTimeout_DieMeltPres) AND (tTimer_DMP_CA >= tTimeout_DieMeltPres) THEN
    bHealth_DMP_A := FALSE;
END_IF;

IF (tTimer_DMP_AB >= tTimeout_DieMeltPres) AND (tTimer_DMP_BC >= tTimeout_DieMeltPres) THEN
    bHealth_DMP_B := FALSE;
END_IF;

IF (tTimer_DMP_BC >= tTimeout_DieMeltPres) AND (tTimer_DMP_CA >= tTimeout_DieMeltPres) THEN
    bHealth_DMP_C := FALSE;
END_IF;

(* Operator Requalification & Discrepancy Reset Command *)
IF bAlarmReset_Cmd_In THEN
    IF (rDieMeltPres_SensA_In >= -2.0) AND (rDieMeltPres_SensA_In <= 320.0) THEN
        bHealth_DMP_A := TRUE;
        tTimer_DMP_AB := 0.0;
        tTimer_DMP_CA := 0.0;
    END_IF;
    IF (rDieMeltPres_SensB_In >= -2.0) AND (rDieMeltPres_SensB_In <= 320.0) THEN
        bHealth_DMP_B := TRUE;
        tTimer_DMP_AB := 0.0;
        tTimer_DMP_BC := 0.0;
    END_IF;
    IF (rDieMeltPres_SensC_In >= -2.0) AND (rDieMeltPres_SensC_In <= 320.0) THEN
        bHealth_DMP_C := TRUE;
        tTimer_DMP_BC := 0.0;
        tTimer_DMP_CA := 0.0;
    END_IF;
END_IF;

(* Step 1.5: Determine Degradation Tier & Execute Bumpless Redundancy Vote *)
IF bHealth_DMP_A AND bHealth_DMP_B AND bHealth_DMP_C THEN
    (* Tier 3: 2oo3 Triple Modular Redundancy - Mid-Value Median Selector *)
    uiDegrade_DieMeltPres := 3;
    bAlm_TMR_MeltPres_Degraded := FALSE;
    IF ((rDieMeltPres_SensA_In >= rDieMeltPres_SensB_In) AND (rDieMeltPres_SensA_In <= rDieMeltPres_SensC_In)) OR
       ((rDieMeltPres_SensA_In <= rDieMeltPres_SensB_In) AND (rDieMeltPres_SensA_In >= rDieMeltPres_SensC_In)) THEN
        rVoted_DieMeltPres_Out := rDieMeltPres_SensA_In;
    ELSIF ((rDieMeltPres_SensB_In >= rDieMeltPres_SensA_In) AND (rDieMeltPres_SensB_In <= rDieMeltPres_SensC_In)) OR
          ((rDieMeltPres_SensB_In <= rDieMeltPres_SensA_In) AND (rDieMeltPres_SensB_In >= rDieMeltPres_SensC_In)) THEN
        rVoted_DieMeltPres_Out := rDieMeltPres_SensB_In;
    ELSE
        rVoted_DieMeltPres_Out := rDieMeltPres_SensC_In;
    END_IF;
ELSIF (bHealth_DMP_A AND bHealth_DMP_B) OR (bHealth_DMP_B AND bHealth_DMP_C) OR (bHealth_DMP_A AND bHealth_DMP_C) THEN
    (* Tier 2: Dual Channel Redundancy - Arithmetic Mean of Healthy Pair *)
    uiDegrade_DieMeltPres := 2;
    bAlm_TMR_MeltPres_Degraded := TRUE;
    IF bHealth_DMP_A AND bHealth_DMP_B THEN
        rVoted_DieMeltPres_Out := 0.5 * (rDieMeltPres_SensA_In + rDieMeltPres_SensB_In);
    ELSIF bHealth_DMP_B AND bHealth_DMP_C THEN
        rVoted_DieMeltPres_Out := 0.5 * (rDieMeltPres_SensB_In + rDieMeltPres_SensC_In);
    ELSE
        rVoted_DieMeltPres_Out := 0.5 * (rDieMeltPres_SensA_In + rDieMeltPres_SensC_In);
    END_IF;
ELSIF bHealth_DMP_A OR bHealth_DMP_B OR bHealth_DMP_C THEN
    (* Tier 1: Simplex Degraded Operation - Lone Surviving Channel Passthrough *)
    uiDegrade_DieMeltPres := 1;
    bAlm_TMR_MeltPres_Degraded := TRUE;
    IF bHealth_DMP_A THEN
        rVoted_DieMeltPres_Out := rDieMeltPres_SensA_In;
    ELSIF bHealth_DMP_B THEN
        rVoted_DieMeltPres_Out := rDieMeltPres_SensB_In;
    ELSE
        rVoted_DieMeltPres_Out := rDieMeltPres_SensC_In;
    END_IF;
ELSE
    (* Tier 0: Complete Sensor Failure - Fallback to Cyber-Physical Observer Estimated State *)
    uiDegrade_DieMeltPres := 0;
    bAlm_TMR_MeltPres_Degraded := TRUE;
    rVoted_DieMeltPres_Out := x_state[14];
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * CHANNEL 2: ADAPTER POLYMER MELT TEMPERATURE TT-201 (A, B, C)
 * Range: 0.0 to 400.0 °C | Permissible Discrepancy: 5.0 °C | Persistence Filter Timeout: 300 ms
 * --------------------------------------------------------------------------------------------------------------------- *)
(* Step 2.1: Calculate Pairwise Absolute Deviations *)
rDiff_MT_AB := ABS(rMeltTemp_SensA_In - rMeltTemp_SensB_In);
rDiff_MT_BC := ABS(rMeltTemp_SensB_In - rMeltTemp_SensC_In);
rDiff_MT_CA := ABS(rMeltTemp_SensC_In - rMeltTemp_SensA_In);

(* Step 2.2: Integrate Discrepancy Persistence Timers *)
IF rDiff_MT_AB > rTol_MeltTemp THEN
    tTimer_MT_AB := tTimer_MT_AB + T_SAMPLE;
ELSE
    IF tTimer_MT_AB > 0.0 THEN
        tTimer_MT_AB := tTimer_MT_AB - (0.5 * T_SAMPLE);
    ELSE
        tTimer_MT_AB := 0.0;
    END_IF;
END_IF;

IF rDiff_MT_BC > rTol_MeltTemp THEN
    tTimer_MT_BC := tTimer_MT_BC + T_SAMPLE;
ELSE
    IF tTimer_MT_BC > 0.0 THEN
        tTimer_MT_BC := tTimer_MT_BC - (0.5 * T_SAMPLE);
    ELSE
        tTimer_MT_BC := 0.0;
    END_IF;
END_IF;

IF rDiff_MT_CA > rTol_MeltTemp THEN
    tTimer_MT_CA := tTimer_MT_CA + T_SAMPLE;
ELSE
    IF tTimer_MT_CA > 0.0 THEN
        tTimer_MT_CA := tTimer_MT_CA - (0.5 * T_SAMPLE);
    ELSE
        tTimer_MT_CA := 0.0;
    END_IF;
END_IF;

(* Step 2.3: Electrical Hardware Range & Wire-Break Plausibility Verification *)
IF (rMeltTemp_SensA_In < 0.0) OR (rMeltTemp_SensA_In > 420.0) THEN
    bHealth_MT_A := FALSE;
END_IF;

IF (rMeltTemp_SensB_In < 0.0) OR (rMeltTemp_SensB_In > 420.0) THEN
    bHealth_MT_B := FALSE;
END_IF;

IF (rMeltTemp_SensC_In < 0.0) OR (rMeltTemp_SensC_In > 420.0) THEN
    bHealth_MT_C := FALSE;
END_IF;

(* Step 2.4: Cross-Channel Persistent Divergence Isolation *)
IF (tTimer_MT_AB >= tTimeout_MeltTemp) AND (tTimer_MT_CA >= tTimeout_MeltTemp) THEN
    bHealth_MT_A := FALSE;
END_IF;

IF (tTimer_MT_AB >= tTimeout_MeltTemp) AND (tTimer_MT_BC >= tTimeout_MeltTemp) THEN
    bHealth_MT_B := FALSE;
END_IF;

IF (tTimer_MT_BC >= tTimeout_MeltTemp) AND (tTimer_MT_CA >= tTimeout_MeltTemp) THEN
    bHealth_MT_C := FALSE;
END_IF;

(* Operator Requalification & Discrepancy Reset Command *)
IF bAlarmReset_Cmd_In THEN
    IF (rMeltTemp_SensA_In >= 15.0) AND (rMeltTemp_SensA_In <= 380.0) THEN
        bHealth_MT_A := TRUE;
        tTimer_MT_AB := 0.0;
        tTimer_MT_CA := 0.0;
    END_IF;
    IF (rMeltTemp_SensB_In >= 15.0) AND (rMeltTemp_SensB_In <= 380.0) THEN
        bHealth_MT_B := TRUE;
        tTimer_MT_AB := 0.0;
        tTimer_MT_BC := 0.0;
    END_IF;
    IF (rMeltTemp_SensC_In >= 15.0) AND (rMeltTemp_SensC_In <= 380.0) THEN
        bHealth_MT_C := TRUE;
        tTimer_MT_BC := 0.0;
        tTimer_MT_CA := 0.0;
    END_IF;
END_IF;

(* Step 2.5: Determine Degradation Tier & Execute Bumpless Redundancy Vote *)
IF bHealth_MT_A AND bHealth_MT_B AND bHealth_MT_C THEN
    (* Tier 3: 2oo3 Triple Modular Redundancy - Mid-Value Median Selector *)
    uiDegrade_MeltTemp := 3;
    bAlm_TMR_MeltTemp_Degraded := FALSE;
    IF ((rMeltTemp_SensA_In >= rMeltTemp_SensB_In) AND (rMeltTemp_SensA_In <= rMeltTemp_SensC_In)) OR
       ((rMeltTemp_SensA_In <= rMeltTemp_SensB_In) AND (rMeltTemp_SensA_In >= rMeltTemp_SensC_In)) THEN
        rVoted_MeltTemp_Out := rMeltTemp_SensA_In;
    ELSIF ((rMeltTemp_SensB_In >= rMeltTemp_SensA_In) AND (rMeltTemp_SensB_In <= rMeltTemp_SensC_In)) OR
          ((rMeltTemp_SensB_In <= rMeltTemp_SensA_In) AND (rMeltTemp_SensB_In >= rMeltTemp_SensC_In)) THEN
        rVoted_MeltTemp_Out := rMeltTemp_SensB_In;
    ELSE
        rVoted_MeltTemp_Out := rMeltTemp_SensC_In;
    END_IF;
ELSIF (bHealth_MT_A AND bHealth_MT_B) OR (bHealth_MT_B AND bHealth_MT_C) OR (bHealth_MT_A AND bHealth_MT_C) THEN
    (* Tier 2: Dual Channel Redundancy - Arithmetic Mean of Healthy Pair *)
    uiDegrade_MeltTemp := 2;
    bAlm_TMR_MeltTemp_Degraded := TRUE;
    IF bHealth_MT_A AND bHealth_MT_B THEN
        rVoted_MeltTemp_Out := 0.5 * (rMeltTemp_SensA_In + rMeltTemp_SensB_In);
    ELSIF bHealth_MT_B AND bHealth_MT_C THEN
        rVoted_MeltTemp_Out := 0.5 * (rMeltTemp_SensB_In + rMeltTemp_SensC_In);
    ELSE
        rVoted_MeltTemp_Out := 0.5 * (rMeltTemp_SensA_In + rMeltTemp_SensC_In);
    END_IF;
ELSIF bHealth_MT_A OR bHealth_MT_B OR bHealth_MT_C THEN
    (* Tier 1: Simplex Degraded Operation - Lone Surviving Channel Passthrough *)
    uiDegrade_MeltTemp := 1;
    bAlm_TMR_MeltTemp_Degraded := TRUE;
    IF bHealth_MT_A THEN
        rVoted_MeltTemp_Out := rMeltTemp_SensA_In;
    ELSIF bHealth_MT_B THEN
        rVoted_MeltTemp_Out := rMeltTemp_SensB_In;
    ELSE
        rVoted_MeltTemp_Out := rMeltTemp_SensC_In;
    END_IF;
ELSE
    (* Tier 0: Complete Sensor Failure - Fallback to Cyber-Physical Observer Estimated State *)
    uiDegrade_MeltTemp := 0;
    bAlm_TMR_MeltTemp_Degraded := TRUE;
    rVoted_MeltTemp_Out := x_state[13];
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * CHANNEL 3: EXTRUDER SCREW DRIVE SHAFT TORQUE TT-301 (A, B, C)
 * Range: 0.0 to 12000.0 Nm | Permissible Discrepancy: 280.0 Nm | Persistence Filter Timeout: 100 ms
 * --------------------------------------------------------------------------------------------------------------------- *)
(* Step 3.1: Calculate Pairwise Absolute Deviations *)
rDiff_ST_AB := ABS(rScrewTorque_SensA_In - rScrewTorque_SensB_In);
rDiff_ST_BC := ABS(rScrewTorque_SensB_In - rScrewTorque_SensC_In);
rDiff_ST_CA := ABS(rScrewTorque_SensC_In - rScrewTorque_SensA_In);

(* Step 3.2: Integrate Discrepancy Persistence Timers *)
IF rDiff_ST_AB > rTol_ScrewTorque THEN
    tTimer_ST_AB := tTimer_ST_AB + T_SAMPLE;
ELSE
    IF tTimer_ST_AB > 0.0 THEN
        tTimer_ST_AB := tTimer_ST_AB - (0.5 * T_SAMPLE);
    ELSE
        tTimer_ST_AB := 0.0;
    END_IF;
END_IF;

IF rDiff_ST_BC > rTol_ScrewTorque THEN
    tTimer_ST_BC := tTimer_ST_BC + T_SAMPLE;
ELSE
    IF tTimer_ST_BC > 0.0 THEN
        tTimer_ST_BC := tTimer_ST_BC - (0.5 * T_SAMPLE);
    ELSE
        tTimer_ST_BC := 0.0;
    END_IF;
END_IF;

IF rDiff_ST_CA > rTol_ScrewTorque THEN
    tTimer_ST_CA := tTimer_ST_CA + T_SAMPLE;
ELSE
    IF tTimer_ST_CA > 0.0 THEN
        tTimer_ST_CA := tTimer_ST_CA - (0.5 * T_SAMPLE);
    ELSE
        tTimer_ST_CA := 0.0;
    END_IF;
END_IF;

(* Step 3.3: Electrical Hardware Range & Wire-Break Plausibility Verification *)
IF (rScrewTorque_SensA_In < -100.0) OR (rScrewTorque_SensA_In > 12500.0) THEN
    bHealth_ST_A := FALSE;
END_IF;

IF (rScrewTorque_SensB_In < -100.0) OR (rScrewTorque_SensB_In > 12500.0) THEN
    bHealth_ST_B := FALSE;
END_IF;

IF (rScrewTorque_SensC_In < -100.0) OR (rScrewTorque_SensC_In > 12500.0) THEN
    bHealth_ST_C := FALSE;
END_IF;

(* Step 3.4: Cross-Channel Persistent Divergence Isolation *)
IF (tTimer_ST_AB >= tTimeout_ScrewTorque) AND (tTimer_ST_CA >= tTimeout_ScrewTorque) THEN
    bHealth_ST_A := FALSE;
END_IF;

IF (tTimer_ST_AB >= tTimeout_ScrewTorque) AND (tTimer_ST_BC >= tTimeout_ScrewTorque) THEN
    bHealth_ST_B := FALSE;
END_IF;

IF (tTimer_ST_BC >= tTimeout_ScrewTorque) AND (tTimer_ST_CA >= tTimeout_ScrewTorque) THEN
    bHealth_ST_C := FALSE;
END_IF;

(* Operator Requalification & Discrepancy Reset Command *)
IF bAlarmReset_Cmd_In THEN
    IF (rScrewTorque_SensA_In >= -50.0) AND (rScrewTorque_SensA_In <= 11000.0) THEN
        bHealth_ST_A := TRUE;
        tTimer_ST_AB := 0.0;
        tTimer_ST_CA := 0.0;
    END_IF;
    IF (rScrewTorque_SensB_In >= -50.0) AND (rScrewTorque_SensB_In <= 11000.0) THEN
        bHealth_ST_B := TRUE;
        tTimer_ST_AB := 0.0;
        tTimer_ST_BC := 0.0;
    END_IF;
    IF (rScrewTorque_SensC_In >= -50.0) AND (rScrewTorque_SensC_In <= 11000.0) THEN
        bHealth_ST_C := TRUE;
        tTimer_ST_BC := 0.0;
        tTimer_ST_CA := 0.0;
    END_IF;
END_IF;

(* Step 3.5: Determine Degradation Tier & Execute Bumpless Redundancy Vote *)
IF bHealth_ST_A AND bHealth_ST_B AND bHealth_ST_C THEN
    (* Tier 3: 2oo3 Triple Modular Redundancy - Mid-Value Median Selector *)
    uiDegrade_ScrewTorque := 3;
    bAlm_TMR_Torque_Degraded := FALSE;
    IF ((rScrewTorque_SensA_In >= rScrewTorque_SensB_In) AND (rScrewTorque_SensA_In <= rScrewTorque_SensC_In)) OR
       ((rScrewTorque_SensA_In <= rScrewTorque_SensB_In) AND (rScrewTorque_SensA_In >= rScrewTorque_SensC_In)) THEN
        rVoted_ScrewTorque_Out := rScrewTorque_SensA_In;
    ELSIF ((rScrewTorque_SensB_In >= rScrewTorque_SensA_In) AND (rScrewTorque_SensB_In <= rScrewTorque_SensC_In)) OR
          ((rScrewTorque_SensB_In <= rScrewTorque_SensA_In) AND (rScrewTorque_SensB_In >= rScrewTorque_SensC_In)) THEN
        rVoted_ScrewTorque_Out := rScrewTorque_SensB_In;
    ELSE
        rVoted_ScrewTorque_Out := rScrewTorque_SensC_In;
    END_IF;
ELSIF (bHealth_ST_A AND bHealth_ST_B) OR (bHealth_ST_B AND bHealth_ST_C) OR (bHealth_ST_A AND bHealth_ST_C) THEN
    (* Tier 2: Dual Channel Redundancy - Arithmetic Mean of Healthy Pair *)
    uiDegrade_ScrewTorque := 2;
    bAlm_TMR_Torque_Degraded := TRUE;
    IF bHealth_ST_A AND bHealth_ST_B THEN
        rVoted_ScrewTorque_Out := 0.5 * (rScrewTorque_SensA_In + rScrewTorque_SensB_In);
    ELSIF bHealth_ST_B AND bHealth_ST_C THEN
        rVoted_ScrewTorque_Out := 0.5 * (rScrewTorque_SensB_In + rScrewTorque_SensC_In);
    ELSE
        rVoted_ScrewTorque_Out := 0.5 * (rScrewTorque_SensA_In + rScrewTorque_SensC_In);
    END_IF;
ELSIF bHealth_ST_A OR bHealth_ST_B OR bHealth_ST_C THEN
    (* Tier 1: Simplex Degraded Operation - Lone Surviving Channel Passthrough *)
    uiDegrade_ScrewTorque := 1;
    bAlm_TMR_Torque_Degraded := TRUE;
    IF bHealth_ST_A THEN
        rVoted_ScrewTorque_Out := rScrewTorque_SensA_In;
    ELSIF bHealth_ST_B THEN
        rVoted_ScrewTorque_Out := rScrewTorque_SensB_In;
    ELSE
        rVoted_ScrewTorque_Out := rScrewTorque_SensC_In;
    END_IF;
ELSE
    (* Tier 0: Complete Sensor Failure - Fallback to Cyber-Physical Observer Estimated State *)
    uiDegrade_ScrewTorque := 0;
    bAlm_TMR_Torque_Degraded := TRUE;
    rVoted_ScrewTorque_Out := x_state[15];
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * CHANNEL 4: PELLETIZER SUPPLY WATER TEMPERATURE TT-401 (A, B, C)
 * Range: 0.0 to 120.0 °C | Permissible Discrepancy: 3.0 °C | Persistence Filter Timeout: 500 ms
 * --------------------------------------------------------------------------------------------------------------------- *)
(* Step 4.1: Calculate Pairwise Absolute Deviations *)
rDiff_WT_AB := ABS(rPelletWaterTemp_SensA_In - rPelletWaterTemp_SensB_In);
rDiff_WT_BC := ABS(rPelletWaterTemp_SensB_In - rPelletWaterTemp_SensC_In);
rDiff_WT_CA := ABS(rPelletWaterTemp_SensC_In - rPelletWaterTemp_SensA_In);

(* Step 4.2: Integrate Discrepancy Persistence Timers *)
IF rDiff_WT_AB > rTol_WaterTemp THEN
    tTimer_WT_AB := tTimer_WT_AB + T_SAMPLE;
ELSE
    IF tTimer_WT_AB > 0.0 THEN
        tTimer_WT_AB := tTimer_WT_AB - (0.5 * T_SAMPLE);
    ELSE
        tTimer_WT_AB := 0.0;
    END_IF;
END_IF;

IF rDiff_WT_BC > rTol_WaterTemp THEN
    tTimer_WT_BC := tTimer_WT_BC + T_SAMPLE;
ELSE
    IF tTimer_WT_BC > 0.0 THEN
        tTimer_WT_BC := tTimer_WT_BC - (0.5 * T_SAMPLE);
    ELSE
        tTimer_WT_BC := 0.0;
    END_IF;
END_IF;

IF rDiff_WT_CA > rTol_WaterTemp THEN
    tTimer_WT_CA := tTimer_WT_CA + T_SAMPLE;
ELSE
    IF tTimer_WT_CA > 0.0 THEN
        tTimer_WT_CA := tTimer_WT_CA - (0.5 * T_SAMPLE);
    ELSE
        tTimer_WT_CA := 0.0;
    END_IF;
END_IF;

(* Step 4.3: Electrical Hardware Range & Wire-Break Plausibility Verification *)
IF (rPelletWaterTemp_SensA_In < 0.0) OR (rPelletWaterTemp_SensA_In > 130.0) THEN
    bHealth_WT_A := FALSE;
END_IF;

IF (rPelletWaterTemp_SensB_In < 0.0) OR (rPelletWaterTemp_SensB_In > 130.0) THEN
    bHealth_WT_B := FALSE;
END_IF;

IF (rPelletWaterTemp_SensC_In < 0.0) OR (rPelletWaterTemp_SensC_In > 130.0) THEN
    bHealth_WT_C := FALSE;
END_IF;

(* Step 4.4: Cross-Channel Persistent Divergence Isolation *)
IF (tTimer_WT_AB >= tTimeout_WaterTemp) AND (tTimer_WT_CA >= tTimeout_WaterTemp) THEN
    bHealth_WT_A := FALSE;
END_IF;

IF (tTimer_WT_AB >= tTimeout_WaterTemp) AND (tTimer_WT_BC >= tTimeout_WaterTemp) THEN
    bHealth_WT_B := FALSE;
END_IF;

IF (tTimer_WT_BC >= tTimeout_WaterTemp) AND (tTimer_WT_CA >= tTimeout_WaterTemp) THEN
    bHealth_WT_C := FALSE;
END_IF;

(* Operator Requalification & Discrepancy Reset Command *)
IF bAlarmReset_Cmd_In THEN
    IF (rPelletWaterTemp_SensA_In >= 5.0) AND (rPelletWaterTemp_SensA_In <= 110.0) THEN
        bHealth_WT_A := TRUE;
        tTimer_WT_AB := 0.0;
        tTimer_WT_CA := 0.0;
    END_IF;
    IF (rPelletWaterTemp_SensB_In >= 5.0) AND (rPelletWaterTemp_SensB_In <= 110.0) THEN
        bHealth_WT_B := TRUE;
        tTimer_WT_AB := 0.0;
        tTimer_WT_BC := 0.0;
    END_IF;
    IF (rPelletWaterTemp_SensC_In >= 5.0) AND (rPelletWaterTemp_SensC_In <= 110.0) THEN
        bHealth_WT_C := TRUE;
        tTimer_WT_BC := 0.0;
        tTimer_WT_CA := 0.0;
    END_IF;
END_IF;

(* Step 4.5: Determine Degradation Tier & Execute Bumpless Redundancy Vote *)
IF bHealth_WT_A AND bHealth_WT_B AND bHealth_WT_C THEN
    (* Tier 3: 2oo3 Triple Modular Redundancy - Mid-Value Median Selector *)
    uiDegrade_WaterTemp := 3;
    bAlm_TMR_WaterTemp_Degraded := FALSE;
    IF ((rPelletWaterTemp_SensA_In >= rPelletWaterTemp_SensB_In) AND (rPelletWaterTemp_SensA_In <= rPelletWaterTemp_SensC_In)) OR
       ((rPelletWaterTemp_SensA_In <= rPelletWaterTemp_SensB_In) AND (rPelletWaterTemp_SensA_In >= rPelletWaterTemp_SensC_In)) THEN
        rVoted_PelletWaterTemp_Out := rPelletWaterTemp_SensA_In;
    ELSIF ((rPelletWaterTemp_SensB_In >= rPelletWaterTemp_SensA_In) AND (rPelletWaterTemp_SensB_In <= rPelletWaterTemp_SensC_In)) OR
          ((rPelletWaterTemp_SensB_In <= rPelletWaterTemp_SensA_In) AND (rPelletWaterTemp_SensB_In >= rPelletWaterTemp_SensC_In)) THEN
        rVoted_PelletWaterTemp_Out := rPelletWaterTemp_SensB_In;
    ELSE
        rVoted_PelletWaterTemp_Out := rPelletWaterTemp_SensC_In;
    END_IF;
ELSIF (bHealth_WT_A AND bHealth_WT_B) OR (bHealth_WT_B AND bHealth_WT_C) OR (bHealth_WT_A AND bHealth_WT_C) THEN
    (* Tier 2: Dual Channel Redundancy - Arithmetic Mean of Healthy Pair *)
    uiDegrade_WaterTemp := 2;
    bAlm_TMR_WaterTemp_Degraded := TRUE;
    IF bHealth_WT_A AND bHealth_WT_B THEN
        rVoted_PelletWaterTemp_Out := 0.5 * (rPelletWaterTemp_SensA_In + rPelletWaterTemp_SensB_In);
    ELSIF bHealth_WT_B AND bHealth_WT_C THEN
        rVoted_PelletWaterTemp_Out := 0.5 * (rPelletWaterTemp_SensB_In + rPelletWaterTemp_SensC_In);
    ELSE
        rVoted_PelletWaterTemp_Out := 0.5 * (rPelletWaterTemp_SensA_In + rPelletWaterTemp_SensC_In);
    END_IF;
ELSIF bHealth_WT_A OR bHealth_WT_B OR bHealth_WT_C THEN
    (* Tier 1: Simplex Degraded Operation - Lone Surviving Channel Passthrough *)
    uiDegrade_WaterTemp := 1;
    bAlm_TMR_WaterTemp_Degraded := TRUE;
    IF bHealth_WT_A THEN
        rVoted_PelletWaterTemp_Out := rPelletWaterTemp_SensA_In;
    ELSIF bHealth_WT_B THEN
        rVoted_PelletWaterTemp_Out := rPelletWaterTemp_SensB_In;
    ELSE
        rVoted_PelletWaterTemp_Out := rPelletWaterTemp_SensC_In;
    END_IF;
ELSE
    (* Tier 0: Complete Sensor Failure - Hold Safe Default Loop Operating Temperature (65.0 °C) *)
    uiDegrade_WaterTemp := 0;
    bAlm_TMR_WaterTemp_Degraded := TRUE;
    rVoted_PelletWaterTemp_Out := 65.0;
END_IF;
