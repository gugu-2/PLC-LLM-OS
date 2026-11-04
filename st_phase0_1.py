# st_phase0_1.py
# Contains Phase 0 (Matrix Initialization) and Phase 1 (2oo3 TMR Voting)

def get_phase0_1():
    return """
(* ===================================================================================================================
 * PHASE 0: COLD-BOOT INITIALIZATION OF 8x8 STATE-SPACE MATRICES & MPC WEIGHTS
 * =================================================================================================================== *)
IF NOT bMatricesInitialized THEN
    (* ---------------------------------------------------------------------------------------------------------------
     * Discrete System Transition Matrix A (8x8) Discretized at Ts = 5.0 ms
     * States:
     *   x[1]: Cell Active Overpotential Deviation Delta_eta_act [V]
     *   x[2]: Membrane Differential Pressure Deviation Delta_DP_mem [bar]
     *   x[3]: H2-in-O2 Gas Crossover Permeation Deviation Delta_Phi_cross [% vol]
     *   x[4]: Stack Core Thermal Temperature Deviation Delta_T_stack [deg C]
     *   x[5]: Anode O2 Separator Dome Pressure Deviation Delta_P_anode [bar]
     *   x[6]: Cathode H2 Separator Dome Pressure Deviation Delta_P_cathode [bar]
     *   x[7]: Anode DI Water Circulating Loop Flow Deviation Delta_F_DI [m3/h]
     *   x[8]: TSA Adsorber Product Moisture Deviation Delta_C_H2O [ppmv]
     * --------------------------------------------------------------------------------------------------------------- *)
    (* Row 1: Active Overpotential dynamics *)
    aA[1, 1] := 0.9650; aA[1, 2] := 0.0000; aA[1, 3] := 0.0000; aA[1, 4] := -0.0018; aA[1, 5] := 0.0004; aA[1, 6] := 0.0000; aA[1, 7] := -0.0008; aA[1, 8] := 0.0000;
    (* Row 2: Membrane Differential Pressure dynamics *)
    aA[2, 1] := 0.0000; aA[2, 2] := 0.9420; aA[2, 3] := 0.0000; aA[2, 4] := 0.0005; aA[2, 5] := -0.0150; aA[2, 6] := 0.0185; aA[2, 7] := 0.0025; aA[2, 8] := 0.0000;
    (* Row 3: H2-in-O2 Gas Crossover Permeation dynamics *)
    aA[3, 1] := -0.0250; aA[3, 2] := 0.0385; aA[3, 3] := 0.9820; aA[3, 4] := 0.0042; aA[3, 5] := -0.0020; aA[3, 6] := 0.0065; aA[3, 7] := -0.0015; aA[3, 8] := 0.0000;
    (* Row 4: Stack Thermal Temperature dynamics *)
    aA[4, 1] := 0.1250; aA[4, 2] := 0.0000; aA[4, 3] := 0.0000; aA[4, 4] := 0.9880; aA[4, 5] := 0.0000; aA[4, 6] := 0.0000; aA[4, 7] := -0.0120; aA[4, 8] := 0.0000;
    (* Row 5: Anode O2 Separator Dome Pressure dynamics *)
    aA[5, 1] := 0.0150; aA[5, 2] := -0.0085; aA[5, 3] := 0.0000; aA[5, 4] := 0.0020; aA[5, 5] := 0.9750; aA[5, 6] := 0.0000; aA[5, 7] := 0.0050; aA[5, 8] := 0.0000;
    (* Row 6: Cathode H2 Separator Dome Pressure dynamics *)
    aA[6, 1] := 0.0280; aA[6, 2] := 0.0120; aA[6, 3] := 0.0000; aA[6, 4] := 0.0025; aA[6, 5] := 0.0000; aA[6, 6] := 0.9720; aA[6, 7] := 0.0000; aA[6, 8] := 0.0000;
    (* Row 7: Anode DI Water Loop Flow dynamics *)
    aA[7, 1] := 0.0000; aA[7, 2] := 0.0015; aA[7, 3] := 0.0000; aA[7, 4] := -0.0050; aA[7, 5] := -0.0080; aA[7, 6] := 0.0000; aA[7, 7] := 0.9550; aA[7, 8] := 0.0000;
    (* Row 8: TSA Adsorber Product Moisture dynamics *)
    aA[8, 1] := 0.0000; aA[8, 2] := 0.0000; aA[8, 3] := 0.0000; aA[8, 4] := 0.0015; aA[8, 5] := 0.0000; aA[8, 6] := 0.0020; aA[8, 7] := 0.0000; aA[8, 8] := 0.9650;

    (* ---------------------------------------------------------------------------------------------------------------
     * Discrete Input Coupling Matrix B (8x4)
     * Controls:
     *   u[1]: Aggregate Thyristor Rectifier Power Command Trim Delta_P_rect [MW]
     *   u[2]: Membrane Differential Backpressure Valve Modulation Delta_theta_DP [%]
     *   u[3]: Anode DI Water Circulating Pump Speed Trim Delta_omega_pump [%]
     *   u[4]: Secondary Cooling Heat Exchanger Bypass Valve Trim Delta_theta_cool [%]
     * --------------------------------------------------------------------------------------------------------------- *)
    (* Col 1: Delta_P_rect | Col 2: Delta_theta_DP | Col 3: Delta_omega_pump | Col 4: Delta_theta_cool *)
    aB[1, 1] := 0.04500; aB[1, 2] := 0.00000; aB[1, 3] := -0.00250; aB[1, 4] := 0.00000;
    aB[2, 1] := 0.00120; aB[2, 2] := -0.02450; aB[2, 3] := 0.00180; aB[2, 4] := 0.00000;
    aB[3, 1] := -0.00850; aB[3, 2] := 0.00520; aB[3, 3] := -0.00120; aB[3, 4] := 0.00000;
    aB[4, 1] := 0.01850; aB[4, 2] := 0.00000; aB[4, 3] := -0.00650; aB[4, 4] := -0.03800;
    aB[5, 1] := 0.00820; aB[5, 2] := 0.01250; aB[5, 3] := 0.00350; aB[5, 4] := 0.00000;
    aB[6, 1] := 0.01650; aB[6, 2] := -0.01450; aB[6, 3] := 0.00000; aB[6, 4] := 0.00000;
    aB[7, 1] := 0.00000; aB[7, 2] := 0.00000; aB[7, 3] := 0.04500; aB[7, 4] := 0.00000;
    aB[8, 1] := 0.00250; aB[8, 2] := 0.00000; aB[8, 3] := 0.00000; aB[8, 4] := 0.00000;

    (* ---------------------------------------------------------------------------------------------------------------
     * Output Observation Matrix C (8x8) Identity Mapping
     * --------------------------------------------------------------------------------------------------------------- *)
    FOR iIdx := 1 TO 8 DO
        FOR jIdx := 1 TO 8 DO
            IF iIdx = jIdx THEN
                aC[iIdx, jIdx] := 1.0;
            ELSE
                aC[iIdx, jIdx] := 0.0;
            END_IF;
        END_FOR;
    END_FOR;

    (* ---------------------------------------------------------------------------------------------------------------
     * Feedthrough Transmission Matrix D (8x4) Zero Transmission
     * --------------------------------------------------------------------------------------------------------------- *)
    FOR iIdx := 1 TO 8 DO
        FOR jIdx := 1 TO 4 DO
            aD[iIdx, jIdx] := 0.0;
        END_FOR;
    END_FOR;

    (* ---------------------------------------------------------------------------------------------------------------
     * Model Predictive Control (MPC) Weighting Matrices & Hard Saturation Bounds
     * --------------------------------------------------------------------------------------------------------------- *)
    (* State Tracking Error Penalty Matrix Diag(Q) *)
    aQ_Weight[1] := 2.50;   (* Overpotential Deviation Penalty *)
    aQ_Weight[2] := 18.50;  (* Membrane Differential Pressure Penalty (Critical Cell Rupture Safeguard) *)
    aQ_Weight[3] := 45.00;  (* H2-in-O2 Gas Crossover Penalty (Explosion Flammability Safeguard) *)
    aQ_Weight[4] := 8.00;   (* Stack Core Thermal Deviation Penalty (Degradation Safeguard) *)
    aQ_Weight[5] := 3.20;   (* Anode Separator Dome Pressure Penalty *)
    aQ_Weight[6] := 3.50;   (* Cathode Separator Dome Pressure Penalty *)
    aQ_Weight[7] := 1.50;   (* Anode DI Water Flow Penalty *)
    aQ_Weight[8] := 2.00;   (* Product Gas Moisture Penalty *)

    (* Actuator Control Effort Penalty Matrix Diag(R) *)
    aR_Weight[1] := 0.0150; (* Power Modulation Effort Penalty *)
    aR_Weight[2] := 0.0450; (* Differential Valve Modulation Penalty *)
    aR_Weight[3] := 0.0250; (* DI Water Pump RPM Penalty *)
    aR_Weight[4] := 0.0200; (* Cooling Heat Exchanger Valve Penalty *)

    (* Actuator Slew Rate Penalty Matrix Diag(S) *)
    aS_Weight[1] := 0.0850; (* Rectifier Fast Slew Penalty *)
    aS_Weight[2] := 0.1500; (* Differential Valve Slew Penalty *)
    aS_Weight[3] := 0.0650; (* Pump Slew Penalty *)
    aS_Weight[4] := 0.0500; (* Cooling Valve Slew Penalty *)

    (* Terminal Prediction Cost Matrix Diag(P) *)
    FOR iIdx := 1 TO 8 DO
        aP_TerminalWeight[iIdx] := aQ_Weight[iIdx] * 2.80;
    END_FOR;

    (* Hard Actuator Authority Constraints *)
    au_min[1] := -15.0; au_max[1] := 15.0;   (* Power Setpoint Trim Delta_P_rect [MW] *)
    au_min[2] := -25.0; au_max[2] := 25.0;   (* Differential Valve Trim Delta_theta_DP [%] *)
    au_min[3] := -20.0; au_max[3] := 20.0;   (* DI Pump Trim Delta_omega_pump [%] *)
    au_min[4] := -30.0; au_max[4] := 30.0;   (* Cooling Valve Trim Delta_theta_cool [%] *)

    (* Slew Bounds per 5.0 ms Execution Cycle *)
    adelta_u_max[1] := 0.100; (* Max 20.0 MW/s Ramp Rate Limit *)
    adelta_u_max[2] := 0.500; (* Max 100.0 %/s Valve Slew Rate *)
    adelta_u_max[3] := 0.250; (* Max 50.0 %/s Pump VFD Slew Rate *)
    adelta_u_max[4] := 0.350; (* Max 70.0 %/s Heat Exchanger Valve Slew *)

    bMatricesInitialized := TRUE;
END_IF;

(* ===================================================================================================================
 * PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING ENGINES
 * =================================================================================================================== *)
dwSensorDegradationWord := 16#0000_0000;

(* --- 1.1 Membrane Differential Pressure (DP_MEMBRANE_DIFF_PRESS_203) 2oo3 Voting --- *)
rDiff12 := ABS(DP_MEMBRANE_DIFF_PRESS_203A - DP_MEMBRANE_DIFF_PRESS_203B);
rDiff23 := ABS(DP_MEMBRANE_DIFF_PRESS_203B - DP_MEMBRANE_DIFF_PRESS_203C);
rDiff13 := ABS(DP_MEMBRANE_DIFF_PRESS_203A - DP_MEMBRANE_DIFF_PRESS_203C);
bAgree12 := (rDiff12 <= c_rDP_DiscrepancyThreshold_bar);
bAgree23 := (rDiff23 <= c_rDP_DiscrepancyThreshold_bar);
bAgree13 := (rDiff13 <= c_rDP_DiscrepancyThreshold_bar);

IF bAgree12 AND bAgree23 AND bAgree13 THEN
    rVoted_MembraneDiffPressure_bar := (DP_MEMBRANE_DIFF_PRESS_203A + DP_MEMBRANE_DIFF_PRESS_203B + DP_MEMBRANE_DIFF_PRESS_203C) / 3.0;
    bDP_ChA_Isolated := FALSE; bDP_ChB_Isolated := FALSE; bDP_ChC_Isolated := FALSE;
    rDP_DiscrepancyTimer_s := 0.0;
ELSIF bAgree12 THEN
    rVoted_MembraneDiffPressure_bar := (DP_MEMBRANE_DIFF_PRESS_203A + DP_MEMBRANE_DIFF_PRESS_203B) / 2.0;
    bDP_ChA_Isolated := FALSE; bDP_ChB_Isolated := FALSE; bDP_ChC_Isolated := TRUE;
    dwSensorDegradationWord := dwSensorDegradationWord OR 16#0000_0001; (* Bit 0: DP Ch C Isolated *)
ELSIF bAgree23 THEN
    rVoted_MembraneDiffPressure_bar := (DP_MEMBRANE_DIFF_PRESS_203B + DP_MEMBRANE_DIFF_PRESS_203C) / 2.0;
    bDP_ChA_Isolated := TRUE; bDP_ChB_Isolated := FALSE; bDP_ChC_Isolated := FALSE;
    dwSensorDegradationWord := dwSensorDegradationWord OR 16#0000_0002; (* Bit 1: DP Ch A Isolated *)
ELSIF bAgree13 THEN
    rVoted_MembraneDiffPressure_bar := (DP_MEMBRANE_DIFF_PRESS_203A + DP_MEMBRANE_DIFF_PRESS_203C) / 2.0;
    bDP_ChA_Isolated := FALSE; bDP_ChB_Isolated := TRUE; bDP_ChC_Isolated := FALSE;
    dwSensorDegradationWord := dwSensorDegradationWord OR 16#0000_0004; (* Bit 2: DP Ch B Isolated *)
ELSE
    rDP_DiscrepancyTimer_s := rDP_DiscrepancyTimer_s + c_rTs;
    rVoted_MembraneDiffPressure_bar := DP_MEMBRANE_DIFF_PRESS_203B; (* Fallback to mid-channel *)
    IF rDP_DiscrepancyTimer_s >= c_rTMR_PersistencyTimeout_s THEN
        bAlarm_TMR_Degraded := TRUE;
        dwSensorDegradationWord := dwSensorDegradationWord OR 16#0000_0008; (* Bit 3: DP Total Disagreement *)
    END_IF;
END_IF;

(* --- 1.2 Anode O2 Degasser H2 Crossover Analyzer (AIT_H2_IN_O2_CROSSOVER_301) 2oo3 Voting --- *)
rDiff12 := ABS(AIT_H2_IN_O2_CROSSOVER_301A - AIT_H2_IN_O2_CROSSOVER_301B);
rDiff23 := ABS(AIT_H2_IN_O2_CROSSOVER_301B - AIT_H2_IN_O2_CROSSOVER_301C);
rDiff13 := ABS(AIT_H2_IN_O2_CROSSOVER_301A - AIT_H2_IN_O2_CROSSOVER_301C);
bAgree12 := (rDiff12 <= c_rH2Cross_DiscrepancyThreshold);
bAgree23 := (rDiff23 <= c_rH2Cross_DiscrepancyThreshold);
bAgree13 := (rDiff13 <= c_rH2Cross_DiscrepancyThreshold);

IF bAgree12 AND bAgree23 AND bAgree13 THEN
    rVoted_H2_in_O2_Crossover_pct := (AIT_H2_IN_O2_CROSSOVER_301A + AIT_H2_IN_O2_CROSSOVER_301B + AIT_H2_IN_O2_CROSSOVER_301C) / 3.0;
    bH2Cross_ChA_Isolated := FALSE; bH2Cross_ChB_Isolated := FALSE; bH2Cross_ChC_Isolated := FALSE;
    rH2Cross_DiscrepancyTimer_s := 0.0;
ELSIF bAgree12 THEN
    rVoted_H2_in_O2_Crossover_pct := (AIT_H2_IN_O2_CROSSOVER_301A + AIT_H2_IN_O2_CROSSOVER_301B) / 2.0;
    bH2Cross_ChA_Isolated := FALSE; bH2Cross_ChB_Isolated := FALSE; bH2Cross_ChC_Isolated := TRUE;
    dwSensorDegradationWord := dwSensorDegradationWord OR 16#0000_0010; (* Bit 4: H2Cross Ch C Isolated *)
ELSIF bAgree23 THEN
    rVoted_H2_in_O2_Crossover_pct := (AIT_H2_IN_O2_CROSSOVER_301B + AIT_H2_IN_O2_CROSSOVER_301C) / 2.0;
    bH2Cross_ChA_Isolated := TRUE; bH2Cross_ChB_Isolated := FALSE; bH2Cross_ChC_Isolated := FALSE;
    dwSensorDegradationWord := dwSensorDegradationWord OR 16#0000_0020; (* Bit 5: H2Cross Ch A Isolated *)
ELSIF bAgree13 THEN
    rVoted_H2_in_O2_Crossover_pct := (AIT_H2_IN_O2_CROSSOVER_301A + AIT_H2_IN_O2_CROSSOVER_301C) / 2.0;
    bH2Cross_ChA_Isolated := FALSE; bH2Cross_ChB_Isolated := TRUE; bH2Cross_ChC_Isolated := FALSE;
    dwSensorDegradationWord := dwSensorDegradationWord OR 16#0000_0040; (* Bit 6: H2Cross Ch B Isolated *)
ELSE
    rH2Cross_DiscrepancyTimer_s := rH2Cross_DiscrepancyTimer_s + c_rTs;
    rVoted_H2_in_O2_Crossover_pct := AIT_H2_IN_O2_CROSSOVER_301B;
    IF rH2Cross_DiscrepancyTimer_s >= c_rTMR_PersistencyTimeout_s THEN
        bAlarm_TMR_Degraded := TRUE;
        dwSensorDegradationWord := dwSensorDegradationWord OR 16#0000_0080; (* Bit 7: H2Cross Total Disagreement *)
    END_IF;
END_IF;

(* --- 1.3 Cathode H2 Product O2 Contamination (AIT_O2_IN_H2_CROSSOVER_302) 2oo3 Voting --- *)
rDiff12 := ABS(AIT_O2_IN_H2_CROSSOVER_302A - AIT_O2_IN_H2_CROSSOVER_302B);
rDiff23 := ABS(AIT_O2_IN_H2_CROSSOVER_302B - AIT_O2_IN_H2_CROSSOVER_302C);
rDiff13 := ABS(AIT_O2_IN_H2_CROSSOVER_302A - AIT_O2_IN_H2_CROSSOVER_302C);
bAgree12 := (rDiff12 <= c_rO2Cross_DiscrepancyThreshold);
bAgree23 := (rDiff23 <= c_rO2Cross_DiscrepancyThreshold);
bAgree13 := (rDiff13 <= c_rO2Cross_DiscrepancyThreshold);

IF bAgree12 AND bAgree23 AND bAgree13 THEN
    rVoted_O2_in_H2_Crossover_pct := (AIT_O2_IN_H2_CROSSOVER_302A + AIT_O2_IN_H2_CROSSOVER_302B + AIT_O2_IN_H2_CROSSOVER_302C) / 3.0;
    bO2Cross_ChA_Isolated := FALSE; bO2Cross_ChB_Isolated := FALSE; bO2Cross_ChC_Isolated := FALSE;
    rO2Cross_DiscrepancyTimer_s := 0.0;
ELSIF bAgree12 THEN
    rVoted_O2_in_H2_Crossover_pct := (AIT_O2_IN_H2_CROSSOVER_302A + AIT_O2_IN_H2_CROSSOVER_302B) / 2.0;
    bO2Cross_ChA_Isolated := FALSE; bO2Cross_ChB_Isolated := FALSE; bO2Cross_ChC_Isolated := TRUE;
    dwSensorDegradationWord := dwSensorDegradationWord OR 16#0000_0100; (* Bit 8: O2Cross Ch C Isolated *)
ELSIF bAgree23 THEN
    rVoted_O2_in_H2_Crossover_pct := (AIT_O2_IN_H2_CROSSOVER_302B + AIT_O2_IN_H2_CROSSOVER_302C) / 2.0;
    bO2Cross_ChA_Isolated := TRUE; bO2Cross_ChB_Isolated := FALSE; bO2Cross_ChC_Isolated := FALSE;
    dwSensorDegradationWord := dwSensorDegradationWord OR 16#0000_0200; (* Bit 9: O2Cross Ch A Isolated *)
ELSIF bAgree13 THEN
    rVoted_O2_in_H2_Crossover_pct := (AIT_O2_IN_H2_CROSSOVER_302A + AIT_O2_IN_H2_CROSSOVER_302C) / 2.0;
    bO2Cross_ChA_Isolated := FALSE; bO2Cross_ChB_Isolated := TRUE; bO2Cross_ChC_Isolated := FALSE;
    dwSensorDegradationWord := dwSensorDegradationWord OR 16#0000_0400; (* Bit 10: O2Cross Ch B Isolated *)
ELSE
    rO2Cross_DiscrepancyTimer_s := rO2Cross_DiscrepancyTimer_s + c_rTs;
    rVoted_O2_in_H2_Crossover_pct := AIT_O2_IN_H2_CROSSOVER_302B;
    IF rO2Cross_DiscrepancyTimer_s >= c_rTMR_PersistencyTimeout_s THEN
        bAlarm_TMR_Degraded := TRUE;
        dwSensorDegradationWord := dwSensorDegradationWord OR 16#0000_0800; (* Bit 11: O2Cross Total Disagreement *)
    END_IF;
END_IF;

(* --- 1.4 Anode O2 Separator Dome Pressure (PT_ANODE_O2_SEPARATOR_201) 2oo3 Voting --- *)
rDiff12 := ABS(PT_ANODE_O2_SEPARATOR_201A - PT_ANODE_O2_SEPARATOR_201B);
rDiff23 := ABS(PT_ANODE_O2_SEPARATOR_201B - PT_ANODE_O2_SEPARATOR_201C);
rDiff13 := ABS(PT_ANODE_O2_SEPARATOR_201A - PT_ANODE_O2_SEPARATOR_201C);
bAgree12 := (rDiff12 <= c_rAnodePress_Discrepancy_bar);
bAgree23 := (rDiff23 <= c_rAnodePress_Discrepancy_bar);
bAgree13 := (rDiff13 <= c_rAnodePress_Discrepancy_bar);

IF bAgree12 AND bAgree23 AND bAgree13 THEN
    rVoted_AnodePressure_bar := (PT_ANODE_O2_SEPARATOR_201A + PT_ANODE_O2_SEPARATOR_201B + PT_ANODE_O2_SEPARATOR_201C) / 3.0;
    bAnodePress_ChA_Isolated := FALSE; bAnodePress_ChB_Isolated := FALSE; bAnodePress_ChC_Isolated := FALSE;
    rAnodePress_DiscrepancyTimer_s := 0.0;
ELSIF bAgree12 THEN
    rVoted_AnodePressure_bar := (PT_ANODE_O2_SEPARATOR_201A + PT_ANODE_O2_SEPARATOR_201B) / 2.0;
    bAnodePress_ChA_Isolated := FALSE; bAnodePress_ChB_Isolated := FALSE; bAnodePress_ChC_Isolated := TRUE;
    dwSensorDegradationWord := dwSensorDegradationWord OR 16#0000_1000; (* Bit 12: Anode Press Ch C Isolated *)
ELSIF bAgree23 THEN
    rVoted_AnodePressure_bar := (PT_ANODE_O2_SEPARATOR_201B + PT_ANODE_O2_SEPARATOR_201C) / 2.0;
    bAnodePress_ChA_Isolated := TRUE; bAnodePress_ChB_Isolated := FALSE; bAnodePress_ChC_Isolated := FALSE;
    dwSensorDegradationWord := dwSensorDegradationWord OR 16#0000_2000; (* Bit 13: Anode Press Ch A Isolated *)
ELSIF bAgree13 THEN
    rVoted_AnodePressure_bar := (PT_ANODE_O2_SEPARATOR_201A + PT_ANODE_O2_SEPARATOR_201C) / 2.0;
    bAnodePress_ChA_Isolated := FALSE; bAnodePress_ChB_Isolated := TRUE; bAnodePress_ChC_Isolated := FALSE;
    dwSensorDegradationWord := dwSensorDegradationWord OR 16#0000_4000; (* Bit 14: Anode Press Ch B Isolated *)
ELSE
    rAnodePress_DiscrepancyTimer_s := rAnodePress_DiscrepancyTimer_s + c_rTs;
    rVoted_AnodePressure_bar := PT_ANODE_O2_SEPARATOR_201B;
    IF rAnodePress_DiscrepancyTimer_s >= c_rTMR_PersistencyTimeout_s THEN
        bAlarm_TMR_Degraded := TRUE;
        dwSensorDegradationWord := dwSensorDegradationWord OR 16#0000_8000; (* Bit 15: Anode Press Total Disagreement *)
    END_IF;
END_IF;

(* --- 1.5 Cathode H2 Separator Dome Pressure (PT_CATHODE_H2_SEPARATOR_202) 2oo3 Voting --- *)
rDiff12 := ABS(PT_CATHODE_H2_SEPARATOR_202A - PT_CATHODE_H2_SEPARATOR_202B);
rDiff23 := ABS(PT_CATHODE_H2_SEPARATOR_202B - PT_CATHODE_H2_SEPARATOR_202C);
rDiff13 := ABS(PT_CATHODE_H2_SEPARATOR_202A - PT_CATHODE_H2_SEPARATOR_202C);
bAgree12 := (rDiff12 <= c_rCathodePress_Discrepancy_bar);
bAgree23 := (rDiff23 <= c_rCathodePress_Discrepancy_bar);
bAgree13 := (rDiff13 <= c_rCathodePress_Discrepancy_bar);

IF bAgree12 AND bAgree23 AND bAgree13 THEN
    rVoted_CathodePressure_bar := (PT_CATHODE_H2_SEPARATOR_202A + PT_CATHODE_H2_SEPARATOR_202B + PT_CATHODE_H2_SEPARATOR_202C) / 3.0;
    bCathodePress_ChA_Isolated := FALSE; bCathodePress_ChB_Isolated := FALSE; bCathodePress_ChC_Isolated := FALSE;
    rCathodePress_DiscrepancyTimer_s := 0.0;
ELSIF bAgree12 THEN
    rVoted_CathodePressure_bar := (PT_CATHODE_H2_SEPARATOR_202A + PT_CATHODE_H2_SEPARATOR_202B) / 2.0;
    bCathodePress_ChA_Isolated := FALSE; bCathodePress_ChB_Isolated := FALSE; bCathodePress_ChC_Isolated := TRUE;
    dwSensorDegradationWord := dwSensorDegradationWord OR 16#0001_0000; (* Bit 16: Cathode Press Ch C Isolated *)
ELSIF bAgree23 THEN
    rVoted_CathodePressure_bar := (PT_CATHODE_H2_SEPARATOR_202B + PT_CATHODE_H2_SEPARATOR_202C) / 2.0;
    bCathodePress_ChA_Isolated := TRUE; bCathodePress_ChB_Isolated := FALSE; bCathodePress_ChC_Isolated := FALSE;
    dwSensorDegradationWord := dwSensorDegradationWord OR 16#0002_0000; (* Bit 17: Cathode Press Ch A Isolated *)
ELSIF bAgree13 THEN
    rVoted_CathodePressure_bar := (PT_CATHODE_H2_SEPARATOR_202A + PT_CATHODE_H2_SEPARATOR_202C) / 2.0;
    bCathodePress_ChA_Isolated := FALSE; bCathodePress_ChB_Isolated := TRUE; bCathodePress_ChC_Isolated := FALSE;
    dwSensorDegradationWord := dwSensorDegradationWord OR 16#0004_0000; (* Bit 18: Cathode Press Ch B Isolated *)
ELSE
    rCathodePress_DiscrepancyTimer_s := rCathodePress_DiscrepancyTimer_s + c_rTs;
    rVoted_CathodePressure_bar := PT_CATHODE_H2_SEPARATOR_202B;
    IF rCathodePress_DiscrepancyTimer_s >= c_rTMR_PersistencyTimeout_s THEN
        bAlarm_TMR_Degraded := TRUE;
        dwSensorDegradationWord := dwSensorDegradationWord OR 16#0008_0000; (* Bit 19: Cathode Press Total Disagreement *)
    END_IF;
END_IF;

(* --- 1.6 Secondary Cooling Loop Inlet Temperature (TT_STACK_COOLING_INLET_401) 2oo3 Voting --- *)
rDiff12 := ABS(TT_STACK_COOLING_INLET_401A - TT_STACK_COOLING_INLET_401B);
rDiff23 := ABS(TT_STACK_COOLING_INLET_401B - TT_STACK_COOLING_INLET_401C);
rDiff13 := ABS(TT_STACK_COOLING_INLET_401A - TT_STACK_COOLING_INLET_401C);
bAgree12 := (rDiff12 <= c_rCoolingTemp_Discrepancy_degC);
bAgree23 := (rDiff23 <= c_rCoolingTemp_Discrepancy_degC);
bAgree13 := (rDiff13 <= c_rCoolingTemp_Discrepancy_degC);

IF bAgree12 AND bAgree23 AND bAgree13 THEN
    rVoted_CoolingInletTemp_degC := (TT_STACK_COOLING_INLET_401A + TT_STACK_COOLING_INLET_401B + TT_STACK_COOLING_INLET_401C) / 3.0;
    bCoolingInlet_ChA_Isolated := FALSE; bCoolingInlet_ChB_Isolated := FALSE; bCoolingInlet_ChC_Isolated := FALSE;
    rCoolingInlet_DiscrepancyTimer_s := 0.0;
ELSIF bAgree12 THEN
    rVoted_CoolingInletTemp_degC := (TT_STACK_COOLING_INLET_401A + TT_STACK_COOLING_INLET_401B) / 2.0;
    bCoolingInlet_ChA_Isolated := FALSE; bCoolingInlet_ChB_Isolated := FALSE; bCoolingInlet_ChC_Isolated := TRUE;
    dwSensorDegradationWord := dwSensorDegradationWord OR 16#0010_0000; (* Bit 20: Cooling In Ch C Isolated *)
ELSIF bAgree23 THEN
    rVoted_CoolingInletTemp_degC := (TT_STACK_COOLING_INLET_401B + TT_STACK_COOLING_INLET_401C) / 2.0;
    bCoolingInlet_ChA_Isolated := TRUE; bCoolingInlet_ChB_Isolated := FALSE; bCoolingInlet_ChC_Isolated := FALSE;
    dwSensorDegradationWord := dwSensorDegradationWord OR 16#0020_0000; (* Bit 21: Cooling In Ch A Isolated *)
ELSIF bAgree13 THEN
    rVoted_CoolingInletTemp_degC := (TT_STACK_COOLING_INLET_401A + TT_STACK_COOLING_INLET_401C) / 2.0;
    bCoolingInlet_ChA_Isolated := FALSE; bCoolingInlet_ChB_Isolated := TRUE; bCoolingInlet_ChC_Isolated := FALSE;
    dwSensorDegradationWord := dwSensorDegradationWord OR 16#0040_0000; (* Bit 22: Cooling In Ch B Isolated *)
ELSE
    rCoolingInlet_DiscrepancyTimer_s := rCoolingInlet_DiscrepancyTimer_s + c_rTs;
    rVoted_CoolingInletTemp_degC := TT_STACK_COOLING_INLET_401B;
    IF rCoolingInlet_DiscrepancyTimer_s >= c_rTMR_PersistencyTimeout_s THEN
        bAlarm_TMR_Degraded := TRUE;
    END_IF;
END_IF;

(* --- 1.7 Secondary Cooling Loop Outlet Temperature (TT_STACK_COOLING_OUTLET_402) 2oo3 Voting --- *)
rDiff12 := ABS(TT_STACK_COOLING_OUTLET_402A - TT_STACK_COOLING_OUTLET_402B);
rDiff23 := ABS(TT_STACK_COOLING_OUTLET_402B - TT_STACK_COOLING_OUTLET_402C);
rDiff13 := ABS(TT_STACK_COOLING_OUTLET_402A - TT_STACK_COOLING_OUTLET_402C);
bAgree12 := (rDiff12 <= c_rCoolingTemp_Discrepancy_degC);
bAgree23 := (rDiff23 <= c_rCoolingTemp_Discrepancy_degC);
bAgree13 := (rDiff13 <= c_rCoolingTemp_Discrepancy_degC);

IF bAgree12 AND bAgree23 AND bAgree13 THEN
    rVoted_CoolingOutletTemp_degC := (TT_STACK_COOLING_OUTLET_402A + TT_STACK_COOLING_OUTLET_402B + TT_STACK_COOLING_OUTLET_402C) / 3.0;
    bCoolingOutlet_ChA_Isolated := FALSE; bCoolingOutlet_ChB_Isolated := FALSE; bCoolingOutlet_ChC_Isolated := FALSE;
    rCoolingOutlet_DiscrepancyTimer_s := 0.0;
ELSIF bAgree12 THEN
    rVoted_CoolingOutletTemp_degC := (TT_STACK_COOLING_OUTLET_402A + TT_STACK_COOLING_OUTLET_402B) / 2.0;
    bCoolingOutlet_ChA_Isolated := FALSE; bCoolingOutlet_ChB_Isolated := FALSE; bCoolingOutlet_ChC_Isolated := TRUE;
ELSIF bAgree23 THEN
    rVoted_CoolingOutletTemp_degC := (TT_STACK_COOLING_OUTLET_402B + TT_STACK_COOLING_OUTLET_402C) / 2.0;
    bCoolingOutlet_ChA_Isolated := TRUE; bCoolingOutlet_ChB_Isolated := FALSE; bCoolingOutlet_ChC_Isolated := FALSE;
ELSIF bAgree13 THEN
    rVoted_CoolingOutletTemp_degC := (TT_STACK_COOLING_OUTLET_402A + TT_STACK_COOLING_OUTLET_402C) / 2.0;
    bCoolingOutlet_ChA_Isolated := FALSE; bCoolingOutlet_ChB_Isolated := TRUE; bCoolingOutlet_ChC_Isolated := FALSE;
ELSE
    rCoolingOutlet_DiscrepancyTimer_s := rCoolingOutlet_DiscrepancyTimer_s + c_rTs;
    rVoted_CoolingOutletTemp_degC := TT_STACK_COOLING_OUTLET_402B;
    IF rCoolingOutlet_DiscrepancyTimer_s >= c_rTMR_PersistencyTimeout_s THEN
        bAlarm_TMR_Degraded := TRUE;
    END_IF;
END_IF;

(* --- 1.8 Demineralized Deionized Water Make-Up Coriolis Flow (FT_DI_WATER_FEED_501) 2oo3 Voting --- *)
rDiff12 := ABS(FT_DI_WATER_FEED_501A - FT_DI_WATER_FEED_501B);
rDiff23 := ABS(FT_DI_WATER_FEED_501B - FT_DI_WATER_FEED_501C);
rDiff13 := ABS(FT_DI_WATER_FEED_501A - FT_DI_WATER_FEED_501C);
bAgree12 := (rDiff12 <= c_rDI_Flow_Discrepancy_m3h);
bAgree23 := (rDiff23 <= c_rDI_Flow_Discrepancy_m3h);
bAgree13 := (rDiff13 <= c_rDI_Flow_Discrepancy_m3h);

IF bAgree12 AND bAgree23 AND bAgree13 THEN
    rVoted_DI_WaterFeedFlow_m3h := (FT_DI_WATER_FEED_501A + FT_DI_WATER_FEED_501B + FT_DI_WATER_FEED_501C) / 3.0;
    bDI_Flow_ChA_Isolated := FALSE; bDI_Flow_ChB_Isolated := FALSE; bDI_Flow_ChC_Isolated := FALSE;
    rDI_Flow_DiscrepancyTimer_s := 0.0;
ELSIF bAgree12 THEN
    rVoted_DI_WaterFeedFlow_m3h := (FT_DI_WATER_FEED_501A + FT_DI_WATER_FEED_501B) / 2.0;
    bDI_Flow_ChA_Isolated := FALSE; bDI_Flow_ChB_Isolated := FALSE; bDI_Flow_ChC_Isolated := TRUE;
ELSIF bAgree23 THEN
    rVoted_DI_WaterFeedFlow_m3h := (FT_DI_WATER_FEED_501B + FT_DI_WATER_FEED_501C) / 2.0;
    bDI_Flow_ChA_Isolated := TRUE; bDI_Flow_ChB_Isolated := FALSE; bDI_Flow_ChC_Isolated := FALSE;
ELSIF bAgree13 THEN
    rVoted_DI_WaterFeedFlow_m3h := (FT_DI_WATER_FEED_501A + FT_DI_WATER_FEED_501C) / 2.0;
    bDI_Flow_ChA_Isolated := FALSE; bDI_Flow_ChB_Isolated := TRUE; bDI_Flow_ChC_Isolated := FALSE;
ELSE
    rDI_Flow_DiscrepancyTimer_s := rDI_Flow_DiscrepancyTimer_s + c_rTs;
    rVoted_DI_WaterFeedFlow_m3h := FT_DI_WATER_FEED_501B;
    IF rDI_Flow_DiscrepancyTimer_s >= c_rTMR_PersistencyTimeout_s THEN
        bAlarm_TMR_Degraded := TRUE;
    END_IF;
END_IF;

(* --- 1.9 Anode Water Electrical Conductivity (AIT_DI_WATER_CONDUCTIVITY_502) 2oo3 Voting --- *)
rDiff12 := ABS(AIT_DI_WATER_CONDUCTIVITY_502A - AIT_DI_WATER_CONDUCTIVITY_502B);
rDiff23 := ABS(AIT_DI_WATER_CONDUCTIVITY_502B - AIT_DI_WATER_CONDUCTIVITY_502C);
rDiff13 := ABS(AIT_DI_WATER_CONDUCTIVITY_502A - AIT_DI_WATER_CONDUCTIVITY_502C);
bAgree12 := (rDiff12 <= c_rConductivity_Discrepancy_uScm);
bAgree23 := (rDiff23 <= c_rConductivity_Discrepancy_uScm);
bAgree13 := (rDiff13 <= c_rConductivity_Discrepancy_uScm);

IF bAgree12 AND bAgree23 AND bAgree13 THEN
    rVoted_DI_WaterConductivity_uScm := (AIT_DI_WATER_CONDUCTIVITY_502A + AIT_DI_WATER_CONDUCTIVITY_502B + AIT_DI_WATER_CONDUCTIVITY_502C) / 3.0;
    bConductivity_ChA_Isolated := FALSE; bConductivity_ChB_Isolated := FALSE; bConductivity_ChC_Isolated := FALSE;
    rConductivity_DiscrepancyTimer_s := 0.0;
ELSIF bAgree12 THEN
    rVoted_DI_WaterConductivity_uScm := (AIT_DI_WATER_CONDUCTIVITY_502A + AIT_DI_WATER_CONDUCTIVITY_502B) / 2.0;
    bConductivity_ChA_Isolated := FALSE; bConductivity_ChB_Isolated := FALSE; bConductivity_ChC_Isolated := TRUE;
ELSIF bAgree23 THEN
    rVoted_DI_WaterConductivity_uScm := (AIT_DI_WATER_CONDUCTIVITY_502B + AIT_DI_WATER_CONDUCTIVITY_502C) / 2.0;
    bConductivity_ChA_Isolated := TRUE; bConductivity_ChB_Isolated := FALSE; bConductivity_ChC_Isolated := FALSE;
ELSIF bAgree13 THEN
    rVoted_DI_WaterConductivity_uScm := (AIT_DI_WATER_CONDUCTIVITY_502A + AIT_DI_WATER_CONDUCTIVITY_502C) / 2.0;
    bConductivity_ChA_Isolated := FALSE; bConductivity_ChB_Isolated := TRUE; bConductivity_ChC_Isolated := FALSE;
ELSE
    rConductivity_DiscrepancyTimer_s := rConductivity_DiscrepancyTimer_s + c_rTs;
    rVoted_DI_WaterConductivity_uScm := AIT_DI_WATER_CONDUCTIVITY_502B;
    IF rConductivity_DiscrepancyTimer_s >= c_rTMR_PersistencyTimeout_s THEN
        bAlarm_TMR_Degraded := TRUE;
    END_IF;
END_IF;

(* --- 1.10 TSA Deoxo / Dryer Bed 1 & Bed 2 Pressures 2oo3 Voting --- *)
(* Bed 1 *)
rDiff12 := ABS(PT_TSA_DRYER_BED1_601A - PT_TSA_DRYER_BED1_601B);
rDiff23 := ABS(PT_TSA_DRYER_BED1_601B - PT_TSA_DRYER_BED1_601C);
rDiff13 := ABS(PT_TSA_DRYER_BED1_601A - PT_TSA_DRYER_BED1_601C);
bAgree12 := (rDiff12 <= c_rTSA_Press_Discrepancy_bar);
bAgree23 := (rDiff23 <= c_rTSA_Press_Discrepancy_bar);
bAgree13 := (rDiff13 <= c_rTSA_Press_Discrepancy_bar);
IF bAgree12 AND bAgree23 AND bAgree13 THEN
    rVoted_TSA_Bed1_Pressure_bar := (PT_TSA_DRYER_BED1_601A + PT_TSA_DRYER_BED1_601B + PT_TSA_DRYER_BED1_601C) / 3.0;
ELSIF bAgree12 THEN
    rVoted_TSA_Bed1_Pressure_bar := (PT_TSA_DRYER_BED1_601A + PT_TSA_DRYER_BED1_601B) / 2.0;
ELSIF bAgree23 THEN
    rVoted_TSA_Bed1_Pressure_bar := (PT_TSA_DRYER_BED1_601B + PT_TSA_DRYER_BED1_601C) / 2.0;
ELSE
    rVoted_TSA_Bed1_Pressure_bar := PT_TSA_DRYER_BED1_601B;
END_IF;

(* Bed 2 *)
rDiff12 := ABS(PT_TSA_DRYER_BED2_602A - PT_TSA_DRYER_BED2_602B);
rDiff23 := ABS(PT_TSA_DRYER_BED2_602B - PT_TSA_DRYER_BED2_602C);
rDiff13 := ABS(PT_TSA_DRYER_BED2_602A - PT_TSA_DRYER_BED2_602C);
bAgree12 := (rDiff12 <= c_rTSA_Press_Discrepancy_bar);
bAgree23 := (rDiff23 <= c_rTSA_Press_Discrepancy_bar);
bAgree13 := (rDiff13 <= c_rTSA_Press_Discrepancy_bar);
IF bAgree12 AND bAgree23 AND bAgree13 THEN
    rVoted_TSA_Bed2_Pressure_bar := (PT_TSA_DRYER_BED2_602A + PT_TSA_DRYER_BED2_602B + PT_TSA_DRYER_BED2_602C) / 3.0;
ELSIF bAgree12 THEN
    rVoted_TSA_Bed2_Pressure_bar := (PT_TSA_DRYER_BED2_602A + PT_TSA_DRYER_BED2_602B) / 2.0;
ELSIF bAgree23 THEN
    rVoted_TSA_Bed2_Pressure_bar := (PT_TSA_DRYER_BED2_602B + PT_TSA_DRYER_BED2_602C) / 2.0;
ELSE
    rVoted_TSA_Bed2_Pressure_bar := PT_TSA_DRYER_BED2_602B;
END_IF;

(* --- 1.11 Final Product Hydrogen Moisture Dew Point (AIT_PRODUCT_H2_DEWPOINT_701) 2oo3 Voting --- *)
rDiff12 := ABS(AIT_PRODUCT_H2_DEWPOINT_701A - AIT_PRODUCT_H2_DEWPOINT_701B);
rDiff23 := ABS(AIT_PRODUCT_H2_DEWPOINT_701B - AIT_PRODUCT_H2_DEWPOINT_701C);
rDiff13 := ABS(AIT_PRODUCT_H2_DEWPOINT_701A - AIT_PRODUCT_H2_DEWPOINT_701C);
bAgree12 := (rDiff12 <= c_rDewpoint_Discrepancy_degC);
bAgree23 := (rDiff23 <= c_rDewpoint_Discrepancy_degC);
bAgree13 := (rDiff13 <= c_rDewpoint_Discrepancy_degC);
IF bAgree12 AND bAgree23 AND bAgree13 THEN
    rVoted_ProductH2_Dewpoint_degC := (AIT_PRODUCT_H2_DEWPOINT_701A + AIT_PRODUCT_H2_DEWPOINT_701B + AIT_PRODUCT_H2_DEWPOINT_701C) / 3.0;
ELSIF bAgree12 THEN
    rVoted_ProductH2_Dewpoint_degC := (AIT_PRODUCT_H2_DEWPOINT_701A + AIT_PRODUCT_H2_DEWPOINT_701B) / 2.0;
ELSIF bAgree23 THEN
    rVoted_ProductH2_Dewpoint_degC := (AIT_PRODUCT_H2_DEWPOINT_701B + AIT_PRODUCT_H2_DEWPOINT_701C) / 2.0;
ELSE
    rVoted_ProductH2_Dewpoint_degC := AIT_PRODUCT_H2_DEWPOINT_701B;
END_IF;
"""
