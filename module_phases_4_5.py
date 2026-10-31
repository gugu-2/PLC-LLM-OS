# module_phases_4_5.py
# Contains Phase 4 (State-Space & Monod Kinetics) and Phase 5 (Receding-Horizon MPC)

def get_phase4_statespace():
    return """(* ================================================================================================== *)
(* === PHASE 4: STATE-SPACE PREDICTION & MONOD METABOLIC KINETICS ===                                *)
(* ================================================================================================== *)
IF NOT bMatricesInitialized THEN
    (* Initialize State Transition Matrix A (12x12) *)
    FOR idx_i := 1 TO 12 DO
        FOR idx_j := 1 TO 12 DO
            arrA[idx_i, idx_j] := 0.0;
        END_FOR;
    END_FOR;
    arrA[1, 1] := 0.9985; (* VCD autologous cell persistence *)
    arrA[1, 3] := 0.0012; (* Glucose growth coupling *)
    arrA[1, 4] := 0.0008; (* Glutamine growth coupling *)
    arrA[1, 5] := -0.0006; (* Lactate growth inhibition *)
    arrA[1, 6] := -0.0009; (* Ammonia growth inhibition *)
    arrA[2, 2] := 0.9970; (* Non-viable cell persistence *)
    arrA[2, 5] := 0.0004; (* Lactate induced death *)
    arrA[2, 6] := 0.0007; (* Ammonia induced death *)
    arrA[3, 3] := 0.9950; (* Glucose maintenance decay *)
    arrA[3, 1] := -0.0028; (* Glucose cellular consumption *)
    arrA[4, 4] := 0.9940; (* Glutamine decay *)
    arrA[4, 1] := -0.0006; (* Glutamine cellular consumption *)
    arrA[5, 5] := 0.9960; (* Lactate clearance *)
    arrA[5, 1] := 0.0020; (* Lactate cellular production *)
    arrA[6, 6] := 0.9955; (* Ammonia clearance *)
    arrA[6, 1] := 0.0003; (* Ammonia cellular production *)
    arrA[7, 7] := 0.9990; (* mAb titre persistence *)
    arrA[7, 1] := 0.0016; (* mAb specific productivity *)
    arrA[8, 8] := 0.9150; (* DO dynamic dissolution *)
    arrA[8, 1] := -0.0042; (* Cellular oxygen consumption OUR *)
    arrA[9, 9] := 0.9850; (* pH dynamic buffering *)
    arrA[9, 5] := -0.0015; (* Lactic acid acidification *)
    arrA[10, 10] := 0.9750; (* Broth temperature thermal inertia *)
    arrA[10, 1] := 0.0002; (* Cellular metabolic heat dissipation *)
    arrA[11, 11] := 1.0000; (* Liquid broth mass conservation *)
    arrA[12, 12] := 0.9920; (* Membrane fouling resistance dynamics *)
    arrA[12, 1] := 0.0005; (* Cell density polarization deposition *)

    (* Initialize Input Coupling Matrix B (12x8) *)
    FOR idx_i := 1 TO 12 DO
        FOR idx_j := 1 TO 8 DO
            arrB[idx_i, idx_j] := 0.0;
        END_FOR;
    END_FOR;
    arrB[8, 1] := 0.3800; (* Micro O2 sparge -> DO *)
    arrB[8, 2] := 0.0750; (* Micro Air sparge -> DO *)
    arrB[9, 3] := -0.0160; (* Macro CO2 sparge -> pH acidification *)
    arrB[9, 4] := 0.00042; (* Base NaHCO3 pump -> pH alkalization *)
    arrB[3, 5] := 0.0125; (* Fresh media feed -> Glucose supplement *)
    arrB[4, 5] := 0.0035; (* Fresh media feed -> Glutamine supplement *)
    arrB[11, 5] := 0.0002778; (* Feed pump -> Liquid Volume (L/h to L/s) *)
    arrB[11, 6] := -0.0002778; (* Permeate harvest pump -> Liquid Volume *)
    arrB[11, 7] := -0.0002778; (* Cell bleed pump -> Liquid Volume *)
    arrB[1, 7] := -0.0035; (* Cell bleed pump -> VCD reduction *)
    arrB[7, 6] := -0.00015; (* Permeate harvest pump -> mAb recovery *)
    arrB[10, 8] := 0.0385; (* TCU heating/cooling net kW -> Broth Temp *)
    arrB[12, 6] := 0.0018; (* Permeate flux -> Membrane cake resistance *)

    (* Initialize Output Matrix C (8x12) *)
    FOR idx_i := 1 TO 8 DO
        FOR idx_j := 1 TO 12 DO
            arrC[idx_i, idx_j] := 0.0;
        END_FOR;
    END_FOR;
    arrC[1, 1] := 1.0; (* y1 = VCD *)
    arrC[2, 3] := 1.0; (* y2 = Glucose *)
    arrC[3, 5] := 1.0; (* y3 = Lactate *)
    arrC[4, 7] := 1.0; (* y4 = mAb Titre *)
    arrC[5, 8] := 1.0; (* y5 = DO *)
    arrC[6, 9] := 1.0; (* y6 = pH *)
    arrC[7, 10] := 1.0; (* y7 = Broth Temp *)
    arrC[8, 11] := 1.0; (* y8 = Broth Volume *)

    (* Initialize Direct Feedthrough Matrix D (8x8) *)
    FOR idx_i := 1 TO 8 DO
        FOR idx_j := 1 TO 8 DO
            arrD[idx_i, idx_j] := 0.0;
        END_FOR;
    END_FOR;

    (* Initialize State Error Weighting Vector Q (12) *)
    arrQ_Weights[1] := 5.0;  (* VCD penalty *)
    arrQ_Weights[2] := 0.5;  (* NCD penalty *)
    arrQ_Weights[3] := 2.0;  (* Glucose penalty *)
    arrQ_Weights[4] := 1.5;  (* Glutamine penalty *)
    arrQ_Weights[5] := 1.0;  (* Lactate penalty *)
    arrQ_Weights[6] := 1.0;  (* Ammonia penalty *)
    arrQ_Weights[7] := 3.0;  (* mAb Titre penalty *)
    arrQ_Weights[8] := 12.0; (* DO penalty *)
    arrQ_Weights[9] := 20.0; (* pH penalty *)
    arrQ_Weights[10] := 15.0; (* Broth Temp penalty *)
    arrQ_Weights[11] := 8.0; (* Liquid Volume penalty *)
    arrQ_Weights[12] := 4.0; (* Membrane fouling penalty *)

    (* Initialize Actuator Slew Rate Penalties R (8) *)
    arrR_Weights[1] := 0.50; (* Micro O2 move penalty *)
    arrR_Weights[2] := 0.20; (* Micro Air move penalty *)
    arrR_Weights[3] := 0.35; (* Macro CO2 move penalty *)
    arrR_Weights[4] := 0.80; (* Base pump move penalty *)
    arrR_Weights[5] := 1.20; (* Perfusion feed pump move penalty *)
    arrR_Weights[6] := 1.00; (* Permeate pump move penalty *)
    arrR_Weights[7] := 1.50; (* Cell bleed pump move penalty *)
    arrR_Weights[8] := 0.60; (* TCU thermal power move penalty *)

    (* Initialize Terminal State Penalties P (12) *)
    FOR idx_i := 1 TO 12 DO
        arrP_Terminal[idx_i] := arrQ_Weights[idx_i] * 2.5;
    END_FOR;

    (* Actuator Physical Saturation Limits *)
    arrU_Min[1] := 0.0;   arrU_Max[1] := 15.0;  arrDeltaU_Max[1] := 0.50; (* Micro O2: 0-15 sL/min *)
    arrU_Min[2] := 0.0;   arrU_Max[2] := 25.0;  arrDeltaU_Max[2] := 1.00; (* Micro Air: 0-25 sL/min *)
    arrU_Min[3] := 0.0;   arrU_Max[3] := 8.0;   arrDeltaU_Max[3] := 0.30; (* Macro CO2: 0-8 sL/min *)
    arrU_Min[4] := 0.0;   arrU_Max[4] := 350.0; arrDeltaU_Max[4] := 15.0; (* Base pump: 0-350 mL/h *)
    arrU_Min[5] := 0.0;   arrU_Max[5] := 65.0;  arrDeltaU_Max[5] := 2.50; (* Feed pump: 0-65 L/h *)
    arrU_Min[6] := 0.0;   arrU_Max[6] := 60.0;  arrDeltaU_Max[6] := 2.00; (* Permeate pump: 0-60 L/h *)
    arrU_Min[7] := 0.0;   arrU_Max[7] := 15.0;  arrDeltaU_Max[7] := 0.80; (* Bleed pump: 0-15 L/h *)
    arrU_Min[8] := -5.0;  arrU_Max[8] := 6.0;   arrDeltaU_Max[8] := 0.40; (* TCU net: -5kW cooling to +6kW heat *)

    bMatricesInitialized := TRUE;
END_IF;

(* Assign measured states into state vector *)
arrX_State[1] := rCalc_VCD_Estimated;
arrX_State[8] := rVoted_DO_Pct;
arrX_State[9] := rVoted_PH;
arrX_State[10] := rBrothTemp_degC;
arrX_State[11] := rCalc_VesselVolume_L;
arrX_State[12] := rCalc_MembraneResistance_1e11;

(* Setpoint vector tracking *)
arrSP[1] := rSet_VCD_Target_1e6;
arrSP[2] := 2.0; (* Target non-viable < 2.0 *)
arrSP[3] := 4.5; (* Glucose setpoint 4.5 g/L *)
arrSP[4] := 2.0; (* Glutamine setpoint 2.0 mmol/L *)
arrSP[5] := 1.5; (* Lactate low *)
arrSP[6] := 1.0; (* Ammonia low *)
arrSP[7] := 8.5; (* High mAb titre *)
arrSP[8] := rSet_DO_Pct;
arrSP[9] := rSet_PH;
arrSP[10] := rSet_Temperature_degC;
arrSP[11] := rSet_WorkingVolume_L;
arrSP[12] := c_rCleanMembraneRes_1e11;

(* Temperature and pH kinetic scaling factors *)
rFactor_Temp := EXP(-1.0 * (((arrX_State[10] - c_rOptTemp_degC) / 2.20) * ((arrX_State[10] - c_rOptTemp_degC) / 2.20)));
rFactor_PH := EXP(-1.0 * (((arrX_State[9] - c_rOptPH) / 0.35) * ((arrX_State[9] - c_rOptPH) / 0.35)));

(* Substrate Monod affinity factors *)
rMonod_Glc := arrX_State[3] / (c_rKsGlc_g_L + arrX_State[3]);
rMonod_Gln := arrX_State[4] / (c_rKsGln_mmol_L + arrX_State[4]);

(* Byproduct non-competitive metabolic inhibition *)
rInhib_Lac := c_rKiLac_g_L / (c_rKiLac_g_L + arrX_State[5]);
rInhib_Amm := c_rKiAmm_mmol_L / (c_rKiAmm_mmol_L + arrX_State[6]);

(* Coupled specific growth and death rates *)
rMu_Gross := c_rMuMax_h_inv * rMonod_Glc * rMonod_Gln * rInhib_Lac * rInhib_Amm * rFactor_Temp * rFactor_PH;
rKd_Total := c_rKd0_h_inv + (c_rKdLac * arrX_State[5]) + (c_rKdAmm * arrX_State[6]);
rMu_Net := rMu_Gross - rKd_Total;

(* Metabolic consumption and production rates *)
rRate_qGlc := (rMu_Gross / c_rYxGlc_cells_g) * 1.0E6 + 0.000045;
rRate_qGln := (rMu_Gross / c_rYxGln_cells_mmol) * 1.0E6 + 0.0000085;
rRate_qLac := c_rYlacGlc_g_g * rRate_qGlc;
rRate_qAmm := c_rYammGln_mmol_mmol * rRate_qGln;
rRate_qp   := c_rAlphaMAb * rMu_Gross + c_rBetaMAb;

(* Dilution rates in h^-1 *)
rPerfusionDilution_h_inv := rCmd_PerfusionFeedPump_Lph / arrX_State[11];
rPermeateDilution_h_inv  := rCmd_PermeateHarvestPump_Lph / arrX_State[11];
rBleedDilution_h_inv     := rCmd_CellBleedPump_Lph / arrX_State[11];

(* Discrete State Propagation x[k+1] = A*x[k] + B*u[k] + dt*f_Monod *)
FOR idx_i := 1 TO 12 DO
    rPredStateSum := 0.0;
    FOR idx_j := 1 TO 12 DO
        rPredStateSum := rPredStateSum + (arrA[idx_i, idx_j] * arrX_State[idx_j]);
    END_FOR;
    FOR idx_k := 1 TO 8 DO
        rPredStateSum := rPredStateSum + (arrB[idx_i, idx_k] * arrU_Actuators[idx_k]);
    END_FOR;
    arrX_Next[idx_i] := rPredStateSum;
END_FOR;

(* Inject continuous biochemical rate corrections *)
arrX_Next[1] := arrX_Next[1] + ((rMu_Net - rBleedDilution_h_inv) * arrX_State[1] * tTaskCycleTime_s / 3600.0);
arrX_Next[2] := arrX_Next[2] + ((rKd_Total * arrX_State[1] - (rBleedDilution_h_inv * arrX_State[2])) * tTaskCycleTime_s / 3600.0);
arrX_Next[3] := arrX_Next[3] + (((rPerfusionDilution_h_inv * 25.0) - (rPerfusionDilution_h_inv * arrX_State[3]) - (rRate_qGlc * arrX_State[1])) * tTaskCycleTime_s / 3600.0);
arrX_Next[4] := arrX_Next[4] + (((rPerfusionDilution_h_inv * 8.0) - (rPerfusionDilution_h_inv * arrX_State[4]) - (rRate_qGln * arrX_State[1])) * tTaskCycleTime_s / 3600.0);
arrX_Next[5] := arrX_Next[5] + (((rRate_qLac * arrX_State[1]) - (rPermeateDilution_h_inv * arrX_State[5])) * tTaskCycleTime_s / 3600.0);
arrX_Next[6] := arrX_Next[6] + (((rRate_qAmm * arrX_State[1]) - (rPermeateDilution_h_inv * arrX_State[6])) * tTaskCycleTime_s / 3600.0);
arrX_Next[7] := arrX_Next[7] + (((rRate_qp * arrX_State[1]) - (rPermeateDilution_h_inv * arrX_State[7])) * tTaskCycleTime_s / 3600.0);
"""

def get_phase5_mpc():
    return """(* ================================================================================================== *)
(* === PHASE 5: RECEDING-HORIZON MODEL PREDICTIVE CONTROL OPTIMIZER ===                              *)
(* ================================================================================================== *)
(* Initialize predicted horizon with current state *)
FOR idx_i := 1 TO 12 DO
    arrX_Pred[idx_i] := arrX_State[idx_i];
END_FOR;

(* Projected Gradient Descent Loop (12 Iterations) *)
FOR idx_iter := 1 TO 12 DO
    (* 1. Simulate forward trajectory over Np = 5 steps *)
    FOR idx_step := 1 TO 5 DO
        FOR idx_i := 1 TO 12 DO
            rPredStateSum := 0.0;
            FOR idx_j := 1 TO 12 DO
                rPredStateSum := rPredStateSum + (arrA[idx_i, idx_j] * arrX_Pred[idx_j]);
            END_FOR;
            FOR idx_k := 1 TO 8 DO
                rPredStateSum := rPredStateSum + (arrB[idx_i, idx_k] * (arrU_Actuators[idx_k] + arrU_Delta[idx_k]));
            END_FOR;
            arrX_Horizon[idx_step, idx_i] := rPredStateSum;
            arrX_Pred[idx_i] := rPredStateSum;
        END_FOR;
    END_FOR;

    (* 2. Evaluate performance index J & cost gradient wrt each actuator move *)
    rCostJ := 0.0;
    FOR idx_k := 1 TO 8 DO
        arrGradJ[idx_k] := 2.0 * arrR_Weights[idx_k] * arrU_Delta[idx_k];
    END_FOR;

    FOR idx_step := 1 TO 5 DO
        FOR idx_i := 1 TO 12 DO
            rCostJ := rCostJ + (arrQ_Weights[idx_i] * (arrX_Horizon[idx_step, idx_i] - arrSP[idx_i]) * (arrX_Horizon[idx_step, idx_i] - arrSP[idx_i]));
            FOR idx_k := 1 TO 8 DO
                arrGradJ[idx_k] := arrGradJ[idx_k] + (2.0 * arrQ_Weights[idx_i] * (arrX_Horizon[idx_step, idx_i] - arrSP[idx_i]) * arrB[idx_i, idx_k]);
            END_FOR;
        END_FOR;
    END_FOR;

    (* Terminal state cost penalty *)
    FOR idx_i := 1 TO 12 DO
        rCostJ := rCostJ + (arrP_Terminal[idx_i] * (arrX_Horizon[5, idx_i] - arrSP[idx_i]) * (arrX_Horizon[5, idx_i] - arrSP[idx_i]));
        FOR idx_k := 1 TO 8 DO
            arrGradJ[idx_k] := arrGradJ[idx_k] + (2.0 * arrP_Terminal[idx_i] * (arrX_Horizon[5, idx_i] - arrSP[idx_i]) * arrB[idx_i, idx_k]);
        END_FOR;
    END_FOR;

    (* 3. Update actuator slew rates with projected bounds *)
    FOR idx_k := 1 TO 8 DO
        arrU_Delta[idx_k] := arrU_Delta[idx_k] - (rAlphaStep * arrGradJ[idx_k]);

        (* Clamp slew rate within maximum allowable delta *)
        IF arrU_Delta[idx_k] > arrDeltaU_Max[idx_k] THEN
            arrU_Delta[idx_k] := arrDeltaU_Max[idx_k];
        ELSIF arrU_Delta[idx_k] < (-1.0 * arrDeltaU_Max[idx_k]) THEN
            arrU_Delta[idx_k] := -1.0 * arrDeltaU_Max[idx_k];
        END_IF;

        (* Enforce physical saturation boundaries on absolute actuator command *)
        IF (arrU_Actuators[idx_k] + arrU_Delta[idx_k]) > arrU_Max[idx_k] THEN
            arrU_Delta[idx_k] := arrU_Max[idx_k] - arrU_Actuators[idx_k];
        ELSIF (arrU_Actuators[idx_k] + arrU_Delta[idx_k]) < arrU_Min[idx_k] THEN
            arrU_Delta[idx_k] := arrU_Min[idx_k] - arrU_Actuators[idx_k];
        END_IF;
    END_FOR;
END_FOR;

(* Store optimal predicted moves *)
FOR idx_k := 1 TO 8 DO
    arrU_Optimal[idx_k] := arrU_Actuators[idx_k] + arrU_Delta[idx_k];
END_FOR;
"""
