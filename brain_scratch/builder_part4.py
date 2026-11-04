# -*- coding: utf-8 -*-
"""
Builder module for FB_Fertilizer_AmmoniumNitrate_Granulation_Scrubber
Part 4: Phase 3 - 8x8 Discrete State-Space Dynamics & Receding-Horizon MPC
"""

def get_phase3_mpc():
    code = """(* ============================================================================================================== *)
(* PHASE 3: 8x8 MULTIVARIABLE DISCRETE STATE-SPACE DYNAMICS & RECEDING-HORIZON MPC                               *)
(* ============================================================================================================== *)

(* -------------------------------------------------------------------------------------------------------------- *)
(* 3.1: FIRST-SCAN STATE-SPACE MATRICES & COST PENALTY INITIALIZATION                                             *)
(* -------------------------------------------------------------------------------------------------------------- *)
IF NOT bMatricesInitialized THEN
    (* Discrete State Transition Matrix A (8x8) representing discrete step Ts = 100 ms *)
    (* State x1: Drum Bed Temperature [deg C] *)
    aA[1, 1] := 0.9850; aA[1, 2] := -0.0120; aA[1, 3] := 0.0040; aA[1, 4] := 0.0000;
    aA[1, 5] := 0.0000; aA[1, 6] := 0.0000;  aA[1, 7] := 0.0000; aA[1, 8] := -0.0150;

    (* State x2: Drum Bed Moisture [wt %] *)
    aA[2, 1] := -0.0018; aA[2, 2] := 0.9780; aA[2, 3] := -0.0025; aA[2, 4] := 0.0000;
    aA[2, 5] := 0.0000;  aA[2, 6] := 0.0000; aA[2, 7] := 0.0000;  aA[2, 8] := 0.0085;

    (* State x3: Granule Mean Diameter d50 [mm] *)
    aA[3, 1] := 0.0008;  aA[3, 2] := 0.0140;  aA[3, 3] := 0.9920; aA[3, 4] := 0.0000;
    aA[3, 5] := 0.0000;  aA[3, 6] := 0.0000;  aA[3, 7] := 0.0000; aA[3, 8] := -0.0060;

    (* State x4: Dryer Outlet Granule Moisture [wt %] *)
    aA[4, 1] := -0.0022; aA[4, 2] := 0.1250;  aA[4, 3] := 0.0000; aA[4, 4] := 0.9650;
    aA[4, 5] := 0.0000;  aA[4, 6] := 0.0000;  aA[4, 7] := 0.0000; aA[4, 8] := 0.0000;

    (* State x5: Cooler Exit Granule Temperature [deg C] *)
    aA[5, 1] := 0.0065;  aA[5, 2] := 0.0000;  aA[5, 3] := 0.0015; aA[5, 4] := 0.0000;
    aA[5, 5] := 0.9620;  aA[5, 6] := 0.0000;  aA[5, 7] := 0.0000; aA[5, 8] := 0.0000;

    (* State x6: Venturi Scrubber Delta P [mbar] *)
    aA[6, 1] := 0.0000;  aA[6, 2] := 0.0000;  aA[6, 3] := 0.0000; aA[6, 4] := 0.0000;
    aA[6, 5] := 0.0000;  aA[6, 6] := 0.9550;  aA[6, 7] := 0.0000; aA[6, 8] := 0.0000;

    (* State x7: Scrubber Liquor pH [-] *)
    aA[7, 1] := 0.0000;  aA[7, 2] := 0.0000;  aA[7, 3] := 0.0000; aA[7, 4] := 0.0000;
    aA[7, 5] := 0.0000;  aA[7, 6] := 0.0000;  aA[7, 7] := 0.9700; aA[7, 8] := 0.0000;

    (* State x8: Solid Recycle Ratio [-] *)
    aA[8, 1] := -0.0012; aA[8, 2] := 0.0035;  aA[8, 3] := -0.0150; aA[8, 4] := 0.0000;
    aA[8, 5] := 0.0000;  aA[8, 6] := 0.0000;  aA[8, 7] := 0.0000;  aA[8, 8] := 0.9810;

    (* Discrete Input Coupling Matrix B (8x4) *)
    (* Inputs: u1 = Slurry Spray Valve [%], u2 = Burner Gas [%], u3 = Cooler Chilled Air [%], u4 = Venturi Damper [%] *)
    aB[1, 1] := 0.0450;  aB[1, 2] := 0.0000;  aB[1, 3] := 0.0000;  aB[1, 4] := 0.0000;
    aB[2, 1] := 0.0185;  aB[2, 2] := 0.0000;  aB[2, 3] := 0.0000;  aB[2, 4] := 0.0000;
    aB[3, 1] := 0.0062;  aB[3, 2] := 0.0000;  aB[3, 3] := 0.0000;  aB[3, 4] := 0.0000;
    aB[4, 1] := 0.0000;  aB[4, 2] := -0.0240; aB[4, 3] := 0.0000;  aB[4, 4] := 0.0000;
    aB[5, 1] := 0.0000;  aB[5, 2] := 0.0000;  aB[5, 3] := -0.0520; aB[5, 4] := 0.0000;
    aB[6, 1] := 0.0000;  aB[6, 2] := 0.0000;  aB[6, 3] := 0.0000;  aB[6, 4] := 0.0880;
    aB[7, 1] := 0.0000;  aB[7, 2] := 0.0000;  aB[7, 3] := 0.0000;  aB[7, 4] := 0.0000;
    aB[8, 1] := -0.0085; aB[8, 2] := 0.0000;  aB[8, 3] := 0.0000;  aB[8, 4] := 0.0000;

    (* Discrete Observation Matrix C (8x8) *)
    FOR idx_i := 1 TO 8 DO
        FOR idx_j := 1 TO 8 DO
            IF idx_i = idx_j THEN
                aC[idx_i, idx_j] := 1.0;
            ELSE
                aC[idx_i, idx_j] := 0.0;
            END_IF;
        END_FOR;
    END_FOR;

    (* Feedforward Matrix D (8x4) *)
    FOR idx_i := 1 TO 8 DO
        FOR idx_j := 1 TO 4 DO
            aD[idx_i, idx_j] := 0.0;
        END_FOR;
    END_FOR;

    (* MPC Diagonal State Error Penalty Matrix Q (8x8) *)
    aQ_Weight[1] := 2.50;   (* Bed Temp tracking penalty *)
    aQ_Weight[2] := 14.00;  (* Bed Moisture tracking penalty *)
    aQ_Weight[3] := 22.00;  (* Granule d50 tracking penalty *)
    aQ_Weight[4] := 35.00;  (* Dryer discharge moisture penalty *)
    aQ_Weight[5] := 12.00;  (* Cooler exit temp penalty *)
    aQ_Weight[6] := 1.80;   (* Scrubber Delta P penalty *)
    aQ_Weight[7] := 18.00;  (* Scrubber pH penalty *)
    aQ_Weight[8] := 8.50;   (* Recycle ratio penalty *)

    (* MPC Actuator Control Effort Energy Penalty R (4) *)
    aR_Weight[1] := 0.65;   (* Slurry valve modulation penalty *)
    aR_Weight[2] := 0.85;   (* Burner fuel throttle penalty *)
    aR_Weight[3] := 0.45;   (* Chilled air blower speed penalty *)
    aR_Weight[4] := 0.35;   (* Venturi throat damper penalty *)

    (* MPC Actuator Slew Rate Penalty S (4) *)
    aS_Weight[1] := 1.80;   (* Slurry valve rate penalty *)
    aS_Weight[2] := 2.50;   (* Burner fuel rate penalty *)
    aS_Weight[3] := 1.20;   (* Blower rate penalty *)
    aS_Weight[4] := 0.90;   (* Damper rate penalty *)

    (* MPC Terminal Horizon Stability Matrix P (8) *)
    aP_TerminalWeight[1] := 4.50;
    aP_TerminalWeight[2] := 25.00;
    aP_TerminalWeight[3] := 38.00;
    aP_TerminalWeight[4] := 55.00;
    aP_TerminalWeight[5] := 20.00;
    aP_TerminalWeight[6] := 3.20;
    aP_TerminalWeight[7] := 28.00;
    aP_TerminalWeight[8] := 15.00;

    (* Hard Box Actuator Bounds & Slew Limits *)
    au_min[1] := 0.0;   au_max[1] := 100.0;  adelta_u_max[1] := 3.50;
    au_min[2] := 15.0;  au_max[2] := 95.0;   adelta_u_max[2] := 2.00;
    au_min[3] := 20.0;  au_max[3] := 100.0;  adelta_u_max[3] := 4.00;
    au_min[4] := 15.0;  au_max[4] := 95.0;   adelta_u_max[4] := 5.00;

    (* Baseline Initial Actuator Commands *)
    au_control[1] := 65.0;
    au_control[2] := 52.0;
    au_control[3] := 60.0;
    au_control[4] := 48.0;

    au_prev[1] := 65.0;
    au_prev[2] := 52.0;
    au_prev[3] := 60.0;
    au_prev[4] := 48.0;

    bMatricesInitialized := TRUE;
END_IF;

(* -------------------------------------------------------------------------------------------------------------- *)
(* 3.2: DYNAMIC STATE VECTOR COMPILATION & REFERENCE TARGET SYNTHESIS                                             *)
(* -------------------------------------------------------------------------------------------------------------- *)
ax_state[1] := rVoted_DrumBedTemp_degC;
ax_state[2] := rCalc_EstimatedGranuleMoisture_pct;
ax_state[3] := rGranuleMeanDiameter_mm;
ax_state[4] := rGranuleMoistureInternal_pct * 0.22; (* Estimated dryer outlet moisture *)
ax_state[5] := rVoted_CoolerZone4Temp_degC;
ax_state[6] := rVoted_VenturiDeltaP_mbar;
ax_state[7] := rVoted_Scrubber_pH;
ax_state[8] := rRecycleRatioFiltered;

ax_ref[1] := rSet_TargetBedTemperature_degC;
ax_ref[2] := rSet_TargetGranuleMoisture_pct;
ax_ref[3] := rSet_TargetMeanDiameter_d50_mm;
ax_ref[4] := rSet_DryerOutletMoistureMax_pct * 0.85;
ax_ref[5] := rSet_CoolerDischargeTempMax_degC - 2.0;
ax_ref[6] := rSet_TargetScrubberDeltaP_mbar;
ax_ref[7] := rSet_TargetScrubber_pH;
ax_ref[8] := rSet_TargetRecycleRatio;

(* Compute Tracking Error Vector e[k] = x[k] - x_ref *)
FOR idx_i := 1 TO 8 DO
    ae_tracking[idx_i] := ax_state[idx_i] - ax_ref[idx_i];
END_FOR;

(* -------------------------------------------------------------------------------------------------------------- *)
(* 3.3: DISCRETE STATE PROPAGATION: x[k+1] = A * x[k] + B * u[k]                                                  *)
(* -------------------------------------------------------------------------------------------------------------- *)
FOR idx_i := 1 TO 8 DO
    rTempSum := 0.0;
    FOR idx_j := 1 TO 8 DO
        rTempSum := rTempSum + (aA[idx_i, idx_j] * ax_state[idx_j]);
    END_FOR;
    FOR idx_k := 1 TO 4 DO
        rTempSum := rTempSum + (aB[idx_i, idx_k] * au_control[idx_k]);
    END_FOR;
    ax_next[idx_i] := rTempSum;
END_FOR;

(* Output Observation Vector: y[k] = C * x[k] + D * u[k] *)
FOR idx_i := 1 TO 8 DO
    rTempSum := 0.0;
    FOR idx_j := 1 TO 8 DO
        rTempSum := rTempSum + (aC[idx_i, idx_j] * ax_state[idx_j]);
    END_FOR;
    FOR idx_k := 1 TO 4 DO
        rTempSum := rTempSum + (aD[idx_i, idx_k] * au_control[idx_k]);
    END_FOR;
    ay_output[idx_i] := rTempSum;
END_FOR;

(* -------------------------------------------------------------------------------------------------------------- *)
(* 3.4: RECEDING-HORIZON MPC ANALYTICAL GRADIENT & PROJECTED GRADIENT DESCENT (PGD)                               *)
(* -------------------------------------------------------------------------------------------------------------- *)
(* Analytical Cost Objective Gradient:                                                                           *)
(* dJ/du_m = sum_i [ B_im * Q_i * (x_next_i - x_ref_i) ] + R_m * u_m + S_m * (u_m - u_prev_m) + sum_i [ B_im * P_i * x_next_i ] *)
FOR idx_k := 1 TO 4 DO
    rTempSum := 0.0;
    FOR idx_i := 1 TO 8 DO
        rTempSum := rTempSum + (aB[idx_i, idx_k] * aQ_Weight[idx_i] * (ax_next[idx_i] - ax_ref[idx_i])) + 
                               (aB[idx_i, idx_k] * aP_TerminalWeight[idx_i] * ax_next[idx_i]);
    END_FOR;
    rTempSum := rTempSum + (aR_Weight[idx_k] * au_control[idx_k]) + 
                           (aS_Weight[idx_k] * (au_control[idx_k] - au_prev[idx_k]));
    aGrad_u[idx_k] := rTempSum;
END_FOR;

(* Update Actuator Demands via Gradient Step with Slew & Box Constraints *)
FOR idx_k := 1 TO 4 DO
    (* Gradient descent update *)
    au_delta[idx_k] := - c_rMPC_StepAlpha * aGrad_u[idx_k];

    (* Slew rate clamping *)
    IF au_delta[idx_k] > adelta_u_max[idx_k] THEN
        au_delta[idx_k] := adelta_u_max[idx_k];
    ELSIF au_delta[idx_k] < -adelta_u_max[idx_k] THEN
        au_delta[idx_k] := -adelta_u_max[idx_k];
    END_IF;

    (* Integrate prior actuator demand *)
    au_control[idx_k] := au_prev[idx_k] + au_delta[idx_k];

    (* Hard box saturation constraints *)
    IF au_control[idx_k] > au_max[idx_k] THEN
        au_control[idx_k] := au_max[idx_k];
    ELSIF au_control[idx_k] < au_min[idx_k] THEN
        au_control[idx_k] := au_min[idx_k];
    END_IF;

    au_prev[idx_k] := au_control[idx_k];
END_FOR;

(* Calculate Realized Quadratic MPC Cost Metric J *)
rMPC_QuadraticCostAccum := 0.0;
FOR idx_i := 1 TO 8 DO
    rMPC_QuadraticCostAccum := rMPC_QuadraticCostAccum + 
        (0.5 * aQ_Weight[idx_i] * (ax_next[idx_i] - ax_ref[idx_i]) * (ax_next[idx_i] - ax_ref[idx_i])) + 
        (0.5 * aP_TerminalWeight[idx_i] * ax_next[idx_i] * ax_next[idx_i]);
END_FOR;
FOR idx_k := 1 TO 4 DO
    rMPC_QuadraticCostAccum := rMPC_QuadraticCostAccum + 
        (0.5 * aR_Weight[idx_k] * au_control[idx_k] * au_control[idx_k]) + 
        (0.5 * aS_Weight[idx_k] * au_delta[idx_k] * au_delta[idx_k]);
END_FOR;
rCalc_MPC_OptimalCost_J := rMPC_QuadraticCostAccum;

(* Assign Optimal Actuator Demands to Process Output Registers if Not In Safety Trip *)
IF NOT bEmergencyDelugeActive AND NOT bRunawayDecompositionTripped THEN
    rOut_SlurrySprayValve_pct := au_control[1];
    rOut_BurnerGasThrottle_pct := au_control[2];
    rOut_CoolerChilledAirFan_pct := au_control[3];
    rOut_VenturiThroatDamper_pct := au_control[4];
    rOut_AtomizingSteamValve_pct := au_control[1] * (rSet_AtomizingSteamRatio / 0.082);
    IF rOut_AtomizingSteamValve_pct > 100.0 THEN rOut_AtomizingSteamValve_pct := 100.0; END_IF;
END_IF;
"""
    return code
