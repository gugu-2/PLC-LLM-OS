# -*- coding: utf-8 -*-
"""
Part 3 of CCR Platforming Function Block:
Phase 3: Discrete State-Space Formulation & Kalman Observer Update.
Phase 4: Model Predictive Control (MPC) Receding Horizon Quadratic Cost Optimization.
Phase 5: Recycle Gas Centrifugal Compressor Polytropic Head & Anti-Surge Controller.
"""

def get_phase3_phase4_phase5():
    return """
(* ====================================================================================================== *)
(* === PHASE 3: DISCRETE STATE-SPACE PREDICTION & KALMAN OBSERVER INNOVATION UPDATE                   === *)
(* ====================================================================================================== *)

(* --- 3.1: MATRIX INITIALIZATION ON FIRST SCAN --- *)
IF NOT bInitialized THEN
    (* Matrix A (8x8): Discrete State Transition at 1.0 s sampling *)
    (* States: [Delta_T1, Delta_T2, Delta_T3, Delta_T4, Delta_xiNaph, Delta_xiParaff, Delta_RH2, Delta_TMT] *)
    aA[1, 1] := 0.942; aA[1, 2] := 0.000; aA[1, 3] := 0.000; aA[1, 4] := 0.000;
    aA[1, 5] := -3.85; aA[1, 6] := 0.000; aA[1, 7] := 0.012; aA[1, 8] := 0.008;

    aA[2, 1] := 0.045; aA[2, 2] := 0.938; aA[2, 3] := 0.000; aA[2, 4] := 0.000;
    aA[2, 5] := -1.25; aA[2, 6] := -2.45; aA[2, 7] := 0.010; aA[2, 8] := 0.009;

    aA[3, 1] := 0.000; aA[3, 2] := 0.038; aA[3, 3] := 0.945; aA[3, 4] := 0.000;
    aA[3, 5] := 0.000; aA[3, 6] := -2.15; aA[3, 7] := 0.008; aA[3, 8] := 0.011;

    aA[4, 1] := 0.000; aA[4, 2] := 0.000; aA[4, 3] := 0.032; aA[4, 4] := 0.952;
    aA[4, 5] := 0.000; aA[4, 6] := -0.95; aA[4, 7] := 0.006; aA[4, 8] := 0.012;

    aA[5, 1] := 0.0018; aA[5, 2] := 0.0000; aA[5, 3] := 0.0000; aA[5, 4] := 0.0000;
    aA[5, 5] := 0.8850; aA[5, 6] := 0.0000; aA[5, 7] := 0.0000; aA[5, 8] := 0.0000;

    aA[6, 1] := 0.0000; aA[6, 2] := 0.0012; aA[6, 3] := 0.0019; aA[6, 4] := 0.0008;
    aA[6, 5] := 0.0000; aA[6, 6] := 0.9120; aA[6, 7] := 0.0000; aA[6, 8] := 0.0000;

    aA[7, 1] := 0.0008; aA[7, 2] := 0.0007; aA[7, 3] := 0.0011; aA[7, 4] := 0.0005;
    aA[7, 5] := 0.0350; aA[7, 6] := 0.0420; aA[7, 7] := 0.9780; aA[7, 8] := 0.0000;

    aA[8, 1] := 0.0150; aA[8, 2] := 0.0180; aA[8, 3] := 0.0210; aA[8, 4] := 0.0250;
    aA[8, 5] := 0.0000; aA[8, 6] := 0.0000; aA[8, 7] := 0.0000; aA[8, 8] := 0.9320;

    (* Matrix B (8x4): Control Coupling Matrix *)
    (* Inputs: [Delta_Fuel_F101, Delta_Fuel_F102, Delta_Fuel_F103, Delta_Fuel_F104] *)
    aB[1, 1] := 0.0315; aB[1, 2] := 0.0000; aB[1, 3] := 0.0000; aB[1, 4] := 0.0000;
    aB[2, 1] := 0.0015; aB[2, 2] := 0.0295; aB[2, 3] := 0.0000; aB[2, 4] := 0.0000;
    aB[3, 1] := 0.0000; aB[3, 2] := 0.0012; aB[3, 3] := 0.0275; aB[3, 4] := 0.0000;
    aB[4, 1] := 0.0000; aB[4, 2] := 0.0000; aB[4, 3] := 0.0011; aB[4, 4] := 0.0245;
    aB[5, 1] := 0.0002; aB[5, 2] := 0.0000; aB[5, 3] := 0.0000; aB[5, 4] := 0.0000;
    aB[6, 1] := 0.0000; aB[6, 2] := 0.0001; aB[6, 3] := 0.0002; aB[6, 4] := 0.0001;
    aB[7, 1] := 0.0001; aB[7, 2] := 0.0001; aB[7, 3] := 0.0001; aB[7, 4] := 0.0001;
    aB[8, 1] := 0.0480; aB[8, 2] := 0.0450; aB[8, 3] := 0.0420; aB[8, 4] := 0.0390;

    (* Matrix C (4x8): Measurement Matrix *)
    (* Outputs: [Delta_WABT, Delta_RON, Delta_YieldC5Plus, Delta_PeakTMT] *)
    aC[1, 1] := 0.100; aC[1, 2] := 0.150; aC[1, 3] := 0.300; aC[1, 4] := 0.450;
    aC[1, 5] := 0.000; aC[1, 6] := 0.000; aC[1, 7] := 0.000; aC[1, 8] := 0.000;

    aC[2, 1] := 0.012; aC[2, 2] := 0.018; aC[2, 3] := 0.035; aC[2, 4] := 0.054;
    aC[2, 5] := 1.250; aC[2, 6] := 2.450; aC[2, 7] := 0.072; aC[2, 8] := 0.000;

    aC[3, 1] := -0.009; aC[3, 2] := -0.014; aC[3, 3] := -0.026; aC[3, 4] := -0.040;
    aC[3, 5] := -0.850; aC[3, 6] := -1.650; aC[3, 7] := 0.125; aC[3, 8] := 0.000;

    aC[4, 1] := 0.000; aC[4, 2] := 0.000; aC[4, 3] := 0.000; aC[4, 4] := 0.000;
    aC[4, 5] := 0.000; aC[4, 6] := 0.000; aC[4, 7] := 0.000; aC[4, 8] := 1.000;

    (* Matrix D (4x4): Direct Feedthrough *)
    FOR i := 1 TO 4 DO
        FOR j := 1 TO 4 DO
            aD_matrix[i, j] := 0.0;
        END_FOR;
    END_FOR;

    (* Disturbance Coupling Matrix E (8x2) *)
    (* Disturbances: [Delta_FeedFlow, Delta_FeedN2A] *)
    aE_dist[1, 1] := -0.042; aE_dist[1, 2] := 0.018;
    aE_dist[2, 1] := -0.038; aE_dist[2, 2] := 0.015;
    aE_dist[3, 1] := -0.032; aE_dist[3, 2] := 0.012;
    aE_dist[4, 1] := -0.028; aE_dist[4, 2] := 0.009;
    aE_dist[5, 1] := -0.001; aE_dist[5, 2] := 0.005;
    aE_dist[6, 1] := -0.001; aE_dist[6, 2] := 0.004;
    aE_dist[7, 1] := -0.005; aE_dist[7, 2] := 0.000;
    aE_dist[8, 1] := 0.025;  aE_dist[8, 2] := 0.000;

    (* Kalman Observer Innovation Gain Matrix L (8x4) *)
    aL_Kalman[1, 1] := 0.285; aL_Kalman[1, 2] := 0.042; aL_Kalman[1, 3] := -0.035; aL_Kalman[1, 4] := 0.012;
    aL_Kalman[2, 1] := 0.272; aL_Kalman[2, 2] := 0.051; aL_Kalman[2, 3] := -0.040; aL_Kalman[2, 4] := 0.014;
    aL_Kalman[3, 1] := 0.255; aL_Kalman[3, 2] := 0.068; aL_Kalman[3, 3] := -0.052; aL_Kalman[3, 4] := 0.016;
    aL_Kalman[4, 1] := 0.240; aL_Kalman[4, 2] := 0.082; aL_Kalman[4, 3] := -0.065; aL_Kalman[4, 4] := 0.019;
    aL_Kalman[5, 1] := 0.018; aL_Kalman[5, 2] := 0.125; aL_Kalman[5, 3] := -0.085; aL_Kalman[5, 4] := 0.001;
    aL_Kalman[6, 1] := 0.022; aL_Kalman[6, 2] := 0.145; aL_Kalman[6, 3] := -0.098; aL_Kalman[6, 4] := 0.002;
    aL_Kalman[7, 1] := 0.008; aL_Kalman[7, 2] := 0.035; aL_Kalman[7, 3] := 0.065;  aL_Kalman[7, 4] := 0.000;
    aL_Kalman[8, 1] := 0.045; aL_Kalman[8, 2] := 0.015; aL_Kalman[8, 3] := 0.000;  aL_Kalman[8, 4] := 0.350;

    (* MPC Quadratic Penalty Weights *)
    (* State Penalty Diagonal Q *)
    aQ[1] := 4.50;  (* Bed 1 Temp Deviation Penalty *)
    aQ[2] := 4.00;  (* Bed 2 Temp Deviation Penalty *)
    aQ[3] := 3.50;  (* Bed 3 Temp Deviation Penalty *)
    aQ[4] := 3.00;  (* Bed 4 Temp Deviation Penalty *)
    aQ[5] := 25.0;  (* Naphthene Conversion Deviation *)
    aQ[6] := 30.0;  (* Paraffin Dehydrocyclization Deviation *)
    aQ[7] := 15.0;  (* H2/HC Ratio Deviation *)
    aQ[8] := 55.0;  (* Furnace Tube Metal Temp (TMT) Creep Penalty *)

    (* Control Effort Diagonal Penalty R *)
    aR[1] := 0.85; aR[2] := 0.75; aR[3] := 0.65; aR[4] := 0.55;

    (* Slew Rate Diagonal Penalty S *)
    aS[1] := 2.50; aS[2] := 2.20; aS[3] := 2.00; aS[4] := 1.80;

    (* Terminal State Error Diagonal Penalty P *)
    aP_term[1] := 8.50; aP_term[2] := 7.80; aP_term[3] := 7.20; aP_term[4] := 6.50;
    aP_term[5] := 50.0; aP_term[6] := 65.0; aP_term[7] := 28.0; aP_term[8] := 95.0;

    (* Hessian Diagonal Approximations (2 * R + 2 * S + 2 * B'*Q*B) *)
    FOR m := 1 TO 4 DO
        aHessianDiag[m] := 2.0 * aR[m] + 2.0 * aS[m];
        FOR i := 1 TO 8 DO
            aHessianDiag[m] := aHessianDiag[m] + 2.0 * aQ[i] * aB[i, m] * aB[i, m];
        END_FOR;
        IF aHessianDiag[m] < 1.0 THEN
            aHessianDiag[m] := 1.0;
        END_IF;
    END_FOR;

    (* Initialize State Vector to Zero Deviations *)
    FOR i := 1 TO 8 DO
        aX[i] := 0.0;
        aX_pred[i] := 0.0;
    END_FOR;

    FOR m := 1 TO 4 DO
        aU[m] := 0.0;
        aU_prev[m] := 0.0;
    END_FOR;

    bInitialized := TRUE;
END_IF;

(* --- 3.2: DISTURBANCE VECTOR EVALUATION --- *)
aDist[1] := rFeedFlow_m3h - rFeedFlow_Base_m3h;
aDist[2] := rFeed_N2A_VolPct - rFeedN2A_Base_volPct;

(* --- 3.3: STATE-SPACE ONE-STEP A-PRIORI PREDICTION (x_pred = A*x + B*u + E*d) --- *)
FOR i := 1 TO 8 DO
    aX_pred[i] := 0.0;
    FOR j := 1 TO 8 DO
        aX_pred[i] := aX_pred[i] + aA[i, j] * aX[j];
    END_FOR;
    FOR m := 1 TO 4 DO
        aX_pred[i] := aX_pred[i] + aB[i, m] * aU[m];
    END_FOR;
    FOR k := 1 TO 2 DO
        aX_pred[i] := aX_pred[i] + aE_dist[i, k] * aDist[k];
    END_FOR;
END_FOR;

(* --- 3.4: OUTPUT PREDICTION (y_pred = C*x_pred + D*u) --- *)
FOR p := 1 TO 4 DO
    aY_pred[p] := 0.0;
    FOR j := 1 TO 8 DO
        aY_pred[p] := aY_pred[p] + aC[p, j] * aX_pred[j];
    END_FOR;
    FOR m := 1 TO 4 DO
        aY_pred[p] := aY_pred[p] + aD_matrix[p, m] * aU[m];
    END_FOR;
END_FOR;

(* --- 3.5: KALMAN OBSERVER INNOVATION RESIDUAL & STATE UPDATE --- *)
(* Compute measurement deviations from base operating points *)
aInnov[1] := (rCalculated_WABT_degC - rWABT_Base_degC) - aY_pred[1];
aInnov[2] := (rPredicted_RON - rRON_Base) - aY_pred[2];
aInnov[3] := (rPredicted_C5Plus_Yield_wtPct - rYield_Base_wtPct) - aY_pred[3];

(* Peak TMT measurement deviation *)
rTempCalc := rF101_MaxTMT;
IF rF102_MaxTMT > rTempCalc THEN rTempCalc := rF102_MaxTMT; END_IF;
IF rF103_MaxTMT > rTempCalc THEN rTempCalc := rF103_MaxTMT; END_IF;
IF rF104_MaxTMT > rTempCalc THEN rTempCalc := rF104_MaxTMT; END_IF;
aInnov[4] := (rTempCalc - rTMT_Base_degC) - aY_pred[4];

(* Update estimated state: x = x_pred + L * Innov *)
FOR i := 1 TO 8 DO
    aX[i] := aX_pred[i];
    FOR p := 1 TO 4 DO
        aX[i] := aX[i] + aL_Kalman[i, p] * aInnov[p];
    END_FOR;
    (* Numerical State Bound Clamping to prevent numerical instability *)
    IF aX[i] > 80.0 THEN aX[i] := 80.0; END_IF;
    IF aX[i] < -80.0 THEN aX[i] := -80.0; END_IF;
END_FOR;


(* ====================================================================================================== *)
(* === PHASE 4: RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) OPTIMIZATION                           === *)
(* ====================================================================================================== *)

(* --- 4.1: REFERENCE TRAJECTORY GENERATION --- *)
(* Determine target WABT based on Octane command or manual override *)
IF bManualWABT_Select THEN
    rActiveTargetWABT_degC := rTargetWABT_Manual_degC;
ELSE
    (* Invert the RON model to solve for required WABT target *)
    (* RON = 71.50 + 0.1185 * (WABT - 480.0) + 0.3350 * (N2A - 50.0) ... *)
    rActiveTargetWABT_degC := 480.0 + (rTargetRON - 71.50 - 0.3350 * (rFeed_N2A_VolPct - 50.0)) / 0.1185;
END_IF;

(* Safety clamp target WABT between 495.0 and 535.0 deg C *)
IF rActiveTargetWABT_degC > 535.0 THEN
    rActiveTargetWABT_degC := 535.0;
ELSIF rActiveTargetWABT_degC < 495.0 THEN
    rActiveTargetWABT_degC := 495.0;
END_IF;

(* Formulate state reference deviations relative to nominal equilibrium *)
rTempDiff := rActiveTargetWABT_degC - rWABT_Base_degC;
aRef[1] := rTempDiff - 4.5; (* Bed 1 Inlet-Outlet Ref *)
aRef[2] := rTempDiff - 1.5; (* Bed 2 Ref *)
aRef[3] := rTempDiff + 2.0; (* Bed 3 Ref *)
aRef[4] := rTempDiff + 4.0; (* Bed 4 Ref *)
aRef[5] := 0.05 * rTempDiff; (* Target Naphthene Conversion Deviation *)
aRef[6] := 0.08 * rTempDiff; (* Target Paraffin Dehydrocyclization Deviation *)
aRef[7] := 0.0;             (* H2/HC target ratio at design 4.5 *)
aRef[8] := 0.0;             (* Target zero excess TMT deviation *)

(* --- 4.2: EVALUATE OBJECTIVE COST FUNCTION J --- *)
rMPC_CurrentCost := 0.0;
FOR i := 1 TO 8 DO
    rTempCalc := aX[i] - aRef[i];
    rMPC_CurrentCost := rMPC_CurrentCost + aQ[i] * rTempCalc * rTempCalc;
    rTempDiff := aX_pred[i] - aRef[i];
    rMPC_CurrentCost := rMPC_CurrentCost + aP_term[i] * rTempDiff * rTempDiff;
END_FOR;

FOR m := 1 TO 4 DO
    rMPC_CurrentCost := rMPC_CurrentCost + aR[m] * aU[m] * aU[m];
    rTempCalc := aU[m] - aU_prev[m];
    rMPC_CurrentCost := rMPC_CurrentCost + aS[m] * rTempCalc * rTempCalc;
END_FOR;

(* Metallurgical Creep Penalty: Quadratic surge penalty if TMT exceeds 590 deg C *)
rTempCalc := rF101_MaxTMT;
IF rF102_MaxTMT > rTempCalc THEN rTempCalc := rF102_MaxTMT; END_IF;
IF rF103_MaxTMT > rTempCalc THEN rTempCalc := rF103_MaxTMT; END_IF;
IF rF104_MaxTMT > rTempCalc THEN rTempCalc := rF104_MaxTMT; END_IF;

IF rTempCalc > 590.0 THEN
    rTempDiff := rTempCalc - 590.0;
    rMPC_CurrentCost := rMPC_CurrentCost + 120.0 * rTempDiff * rTempDiff;
END_IF;

(* --- 4.3: PROJECTED GRADIENT DESCENT ITERATIONS --- *)
FOR iter := 1 TO 5 DO
    (* Compute Analytical Gradient: grad_m = 2*R*u + 2*S*(u - u_prev) + 2*B'*Q*(x - ref) + 2*B'*P*(x_pred - ref) *)
    FOR m := 1 TO 4 DO
        aGrad[m] := 2.0 * aR[m] * aU[m] + 2.0 * aS[m] * (aU[m] - aU_prev[m]);
        FOR i := 1 TO 8 DO
            aGrad[m] := aGrad[m] + 2.0 * aQ[i] * (aX[i] - aRef[i]) * aB[i, m];
            aGrad[m] := aGrad[m] + 2.0 * aP_term[i] * (aX_pred[i] - aRef[i]) * aB[i, m];
        END_FOR;

        (* Additional steep gradient pushback if tube metal temperature exceeds threshold *)
        IF rTempCalc > 590.0 THEN
            aGrad[m] := aGrad[m] + 240.0 * (rTempCalc - 590.0) * aB[8, m];
        END_IF;

        (* Projected Newton-Gradient Step *)
        aStep[m] := aGrad[m] / aHessianDiag[m];
        aU_cand[m] := aU[m] - rMPC_Alpha * aStep[m];

        (* Enforce Actuator Slew Rate Constraints [+/- 1.5 %/s] *)
        rTempDiff := aU_cand[m] - aU_prev[m];
        IF rTempDiff > rMaxSlewRate_PctPerSec THEN
            aU_cand[m] := aU_prev[m] + rMaxSlewRate_PctPerSec;
        ELSIF rTempDiff < -rMaxSlewRate_PctPerSec THEN
            aU_cand[m] := aU_prev[m] - rMaxSlewRate_PctPerSec;
        END_IF;

        (* Hard Furnace Thermal Capability Constraints [8.0 .. 95.0 %] *)
        IF aU_cand[m] > rMaxFuelDemand_Pct THEN
            aU_cand[m] := rMaxFuelDemand_Pct;
            iMPC_SolverStatus := 1; (* Constrained *)
        ELSIF aU_cand[m] < rMinFuelDemand_Pct THEN
            aU_cand[m] := rMinFuelDemand_Pct;
            iMPC_SolverStatus := 1; (* Constrained *)
        END_IF;

        (* Update working control candidate *)
        aU[m] := aU_cand[m];
    END_FOR;
END_FOR;

(* Store u for next cycle slew rate calculations *)
FOR m := 1 TO 4 DO
    aDeltaU[m] := aU[m] - aU_prev[m];
    aU_prev[m] := aU[m];
END_FOR;

(* --- 4.4: MAP CONTROL INPUTS TO PHYSICAL VALVE DEMANDS --- *)
rDemand_F101_FuelGas_Pct := aU[1];
rDemand_F102_FuelGas_Pct := aU[2];
rDemand_F103_FuelGas_Pct := aU[3];
rDemand_F104_FuelGas_Pct := aU[4];


(* ====================================================================================================== *)
(* === PHASE 5: RECYCLE GAS COMPRESSOR POLYTROPIC HEAD & ANTI-SURGE CONTROLLER                        === *)
(* ====================================================================================================== *)

(* --- 5.1: POLYTROPIC HEAD & SURGE LINE CALCULATION --- *)
(* Absolute Suction & Discharge Pressures [bar a] *)
rTempCalc := rRecycleCompressor_SuctionP_bar + 1.01325;
rTempDiff := rRecycleCompressor_DischargeP_bar + 1.01325;

(* Pressure Ratio r_p *)
IF rTempCalc > 0.5 THEN
    rTempDiff := rTempDiff / rTempCalc;
ELSE
    rTempDiff := 2.50;
END_IF;

(* Polytropic Exponent (n-1)/n for Hydrogen-rich gas ~ 0.285 *)
(* Head = (Z * R * T_suct / (Mw * 0.285)) * (r_p^0.285 - 1) *)
(* Approximated r_p^0.285 via 1st order Taylor series around r_p0 = 2.5 *)
rCompressor_PolytropicHead_m := (1.02 * 8314.46 * (rSeparator_T_degC + 273.15) / (rMw_Hydrogen_kgkmol * 0.285))
                                * (0.298 + 0.119 * (rTempDiff - 2.50));

(* Normalized Volumetric Suction Flow Index *)
rTempCalc := (rRecycleCompressor_Flow_Nm3h / 100000.0) * (rTempCalc / 5.813);

(* Parabolic Surge Limit Flow Index: Flow_surge = k_surge * sqrt(Head) *)
rTempDiff := 0.685 * (rCompressor_PolytropicHead_m / 12000.0);

(* Distance-to-Surge Deviation Margin [%] *)
IF rTempDiff > 0.05 THEN
    rCompressor_SurgeMargin_Pct := ((rTempCalc - rTempDiff) / rTempDiff) * 100.0;
ELSE
    rCompressor_SurgeMargin_Pct := 25.0;
END_IF;

(* --- 5.2: ANTI-SURGE PID CONTROLLER WITH RAPID OPENING DECOUPLING --- *)
rTempCalc := rAntiSurge_TargetMargin_Pct - rCompressor_SurgeMargin_Pct; (* Error: positive when approaching surge *)

(* Proportional Term *)
rTempDiff := rAntiSurge_Kp * rTempCalc;

(* Integral Term with Anti-Windup *)
rAntiSurge_IntegralAccum := rAntiSurge_IntegralAccum + rAntiSurge_Ki * rTempCalc * 1.0;
IF rAntiSurge_IntegralAccum > 100.0 THEN
    rAntiSurge_IntegralAccum := 100.0;
ELSIF rAntiSurge_IntegralAccum < 0.0 THEN
    rAntiSurge_IntegralAccum := 0.0;
END_IF;

(* Derivative Term *)
rDemand_RecycleAntiSurge_Pct := rTempDiff + rAntiSurge_IntegralAccum
                              + rAntiSurge_Kd * (rTempCalc - rAntiSurge_PrevError);
rAntiSurge_PrevError := rTempCalc;

(* Rapid Surge Countermeasure: Instantaneous Valve Boost if Margin < 10% *)
IF rCompressor_SurgeMargin_Pct < 10.0 THEN
    rDemand_RecycleAntiSurge_Pct := rDemand_RecycleAntiSurge_Pct + (10.0 - rCompressor_SurgeMargin_Pct) * 4.5;
END_IF;

(* Clamp Anti-Surge Valve Demand [0.0 .. 100.0 %] *)
IF rDemand_RecycleAntiSurge_Pct > 100.0 THEN
    rDemand_RecycleAntiSurge_Pct := 100.0;
ELSIF rDemand_RecycleAntiSurge_Pct < 0.0 THEN
    rDemand_RecycleAntiSurge_Pct := 0.0;
END_IF;

(* Speed Demand to Maintain Constant Recycle Circulation Rate *)
IF rH2_HC_MoleRatio < 4.2 THEN
    rDemand_RecycleCompressor_Speed_RPM := rRecycleCompressor_Speed_RPM + 25.0;
ELSIF rH2_HC_MoleRatio > 5.2 THEN
    rDemand_RecycleCompressor_Speed_RPM := rRecycleCompressor_Speed_RPM - 15.0;
ELSE
    rDemand_RecycleCompressor_Speed_RPM := rRecycleCompressor_Speed_RPM;
END_IF;

IF rDemand_RecycleCompressor_Speed_RPM > 11500.0 THEN
    rDemand_RecycleCompressor_Speed_RPM := 11500.0;
ELSIF rDemand_RecycleCompressor_Speed_RPM < 6000.0 THEN
    rDemand_RecycleCompressor_Speed_RPM := 6000.0;
END_IF;
"""
