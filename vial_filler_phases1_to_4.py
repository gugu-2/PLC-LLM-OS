# -*- coding: utf-8 -*-
"""
vial_filler_phases1_to_4.py
Contains Phases 1 to 4 for FB_Pharma_AsepticVialFilling_600VPM_Checkweigh:
- Phase 1: 2oo3 TMR Sensor Voting
- Phase 2: Discrete State-Space Model Prediction & Kalman Observer
- Phase 3: Receding-Horizon MPC Quadratic Optimization
- Phase 4: Multi-Channel Peristaltic Dosing & Bottom-Up Diving Trajectory
"""

def get_phases1_to_4_code():
    return """(* ========================================================================================= *)
(* SECTION 1: PHASE 1 - 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING LOGIC            *)
(* ========================================================================================= *)
(* Executes 2oo3 majority voting across all critical process parameters with pair-wise       *)
(* discrepancy evaluation, configurable persistence timers, and bumpless degradation.       *)

(* --- Bank 1: Starwheel Master Turret Optical Resolvers (ChA, ChB, ChC) [deg] --- *)
(* Allowable resolver discrepancy tolerance: 0.15 deg *)
IF (ABS(rStarwheelEncoder_ChA_deg - rStarwheelEncoder_ChB_deg) <= 0.15) AND
   (ABS(rStarwheelEncoder_ChB_deg - rStarwheelEncoder_ChC_deg) <= 0.15) AND
   (ABS(rStarwheelEncoder_ChA_deg - rStarwheelEncoder_ChC_deg) <= 0.15) THEN
    (* All three channels coherent - vote median value *)
    IF ((rStarwheelEncoder_ChA_deg >= rStarwheelEncoder_ChB_deg) AND (rStarwheelEncoder_ChA_deg <= rStarwheelEncoder_ChC_deg)) OR
       ((rStarwheelEncoder_ChA_deg <= rStarwheelEncoder_ChB_deg) AND (rStarwheelEncoder_ChA_deg >= rStarwheelEncoder_ChC_deg)) THEN
        rStarwheelVoted_deg := rStarwheelEncoder_ChA_deg;
    ELSIF ((rStarwheelEncoder_ChB_deg >= rStarwheelEncoder_ChA_deg) AND (rStarwheelEncoder_ChB_deg <= rStarwheelEncoder_ChC_deg)) OR
          ((rStarwheelEncoder_ChB_deg <= rStarwheelEncoder_ChA_deg) AND (rStarwheelEncoder_ChB_deg >= rStarwheelEncoder_ChC_deg)) THEN
        rStarwheelVoted_deg := rStarwheelEncoder_ChB_deg;
    ELSE
        rStarwheelVoted_deg := rStarwheelEncoder_ChC_deg;
    END_IF;
    bStarwheel_TMR_ChA_Valid := TRUE;
    bStarwheel_TMR_ChB_Valid := TRUE;
    bStarwheel_TMR_ChC_Valid := TRUE;
    tStarwheelDiscrepancyTimer := T#0MS;
    bStarwheelDegraded := FALSE;
ELSIF (ABS(rStarwheelEncoder_ChA_deg - rStarwheelEncoder_ChB_deg) <= 0.15) THEN
    (* Channel C deviating - vote average of A and B *)
    rStarwheelVoted_deg := 0.5 * (rStarwheelEncoder_ChA_deg + rStarwheelEncoder_ChB_deg);
    bStarwheel_TMR_ChA_Valid := TRUE;
    bStarwheel_TMR_ChB_Valid := TRUE;
    bStarwheel_TMR_ChC_Valid := FALSE;
    bStarwheelDegraded := TRUE;
ELSIF (ABS(rStarwheelEncoder_ChB_deg - rStarwheelEncoder_ChC_deg) <= 0.15) THEN
    (* Channel A deviating - vote average of B and C *)
    rStarwheelVoted_deg := 0.5 * (rStarwheelEncoder_ChB_deg + rStarwheelEncoder_ChC_deg);
    bStarwheel_TMR_ChA_Valid := FALSE;
    bStarwheel_TMR_ChB_Valid := TRUE;
    bStarwheel_TMR_ChC_Valid := TRUE;
    bStarwheelDegraded := TRUE;
ELSIF (ABS(rStarwheelEncoder_ChA_deg - rStarwheelEncoder_ChC_deg) <= 0.15) THEN
    (* Channel B deviating - vote average of A and C *)
    rStarwheelVoted_deg := 0.5 * (rStarwheelEncoder_ChA_deg + rStarwheelEncoder_ChC_deg);
    bStarwheel_TMR_ChA_Valid := TRUE;
    bStarwheel_TMR_ChB_Valid := FALSE;
    bStarwheel_TMR_ChC_Valid := TRUE;
    bStarwheelDegraded := TRUE;
ELSE
    (* All channels divergent - retain last known valid reading and accumulate discrepancy timer *)
    tStarwheelDiscrepancyTimer := tStarwheelDiscrepancyTimer + T#1MS;
    bStarwheel_TMR_ChA_Valid := FALSE;
    bStarwheel_TMR_ChB_Valid := FALSE;
    bStarwheel_TMR_ChC_Valid := FALSE;
    bStarwheelDegraded := TRUE;
END_IF;

(* --- Bank 2: In-Line Pre-Fill Dynamic EMFR Tare Load Cells (ChA, ChB, ChC) [mg] --- *)
(* Allowable tare discrepancy tolerance: 1.5 mg *)
IF (ABS(rTareLoadCell_ChA_mg - rTareLoadCell_ChB_mg) <= 1.5) AND
   (ABS(rTareLoadCell_ChB_mg - rTareLoadCell_ChC_mg) <= 1.5) AND
   (ABS(rTareLoadCell_ChA_mg - rTareLoadCell_ChC_mg) <= 1.5) THEN
    IF ((rTareLoadCell_ChA_mg >= rTareLoadCell_ChB_mg) AND (rTareLoadCell_ChA_mg <= rTareLoadCell_ChC_mg)) OR
       ((rTareLoadCell_ChA_mg <= rTareLoadCell_ChB_mg) AND (rTareLoadCell_ChA_mg >= rTareLoadCell_ChC_mg)) THEN
        rTareVoted_mg := rTareLoadCell_ChA_mg;
    ELSIF ((rTareLoadCell_ChB_mg >= rTareLoadCell_ChA_mg) AND (rTareLoadCell_ChB_mg <= rTareLoadCell_ChC_mg)) OR
          ((rTareLoadCell_ChB_mg <= rTareLoadCell_ChA_mg) AND (rTareLoadCell_ChB_mg >= rTareLoadCell_ChC_mg)) THEN
        rTareVoted_mg := rTareLoadCell_ChB_mg;
    ELSE
        rTareVoted_mg := rTareLoadCell_ChC_mg;
    END_IF;
    bTare_TMR_ChA_Valid := TRUE;
    bTare_TMR_ChB_Valid := TRUE;
    bTare_TMR_ChC_Valid := TRUE;
    tTareDiscrepancyTimer := T#0MS;
    bTareDegraded := FALSE;
ELSIF (ABS(rTareLoadCell_ChA_mg - rTareLoadCell_ChB_mg) <= 1.5) THEN
    rTareVoted_mg := 0.5 * (rTareLoadCell_ChA_mg + rTareLoadCell_ChB_mg);
    bTare_TMR_ChA_Valid := TRUE;
    bTare_TMR_ChB_Valid := TRUE;
    bTare_TMR_ChC_Valid := FALSE;
    bTareDegraded := TRUE;
ELSIF (ABS(rTareLoadCell_ChB_mg - rTareLoadCell_ChC_mg) <= 1.5) THEN
    rTareVoted_mg := 0.5 * (rTareLoadCell_ChB_mg + rTareLoadCell_ChC_mg);
    bTare_TMR_ChA_Valid := FALSE;
    bTare_TMR_ChB_Valid := TRUE;
    bTare_TMR_ChC_Valid := TRUE;
    bTareDegraded := TRUE;
ELSIF (ABS(rTareLoadCell_ChA_mg - rTareLoadCell_ChC_mg) <= 1.5) THEN
    rTareVoted_mg := 0.5 * (rTareLoadCell_ChA_mg + rTareLoadCell_ChC_mg);
    bTare_TMR_ChA_Valid := TRUE;
    bTare_TMR_ChB_Valid := FALSE;
    bTare_TMR_ChC_Valid := TRUE;
    bTareDegraded := TRUE;
ELSE
    tTareDiscrepancyTimer := tTareDiscrepancyTimer + T#1MS;
    bTare_TMR_ChA_Valid := FALSE;
    bTare_TMR_ChB_Valid := FALSE;
    bTare_TMR_ChC_Valid := FALSE;
    bTareDegraded := TRUE;
END_IF;

(* --- Bank 3: In-Line Post-Fill Dynamic EMFR Gross Load Cells (ChA, ChB, ChC) [mg] --- *)
(* Allowable gross discrepancy tolerance: 1.5 mg *)
IF (ABS(rGrossLoadCell_ChA_mg - rGrossLoadCell_ChB_mg) <= 1.5) AND
   (ABS(rGrossLoadCell_ChB_mg - rGrossLoadCell_ChC_mg) <= 1.5) AND
   (ABS(rGrossLoadCell_ChA_mg - rGrossLoadCell_ChC_mg) <= 1.5) THEN
    IF ((rGrossLoadCell_ChA_mg >= rGrossLoadCell_ChB_mg) AND (rGrossLoadCell_ChA_mg <= rGrossLoadCell_ChC_mg)) OR
       ((rGrossLoadCell_ChA_mg <= rGrossLoadCell_ChB_mg) AND (rGrossLoadCell_ChA_mg >= rGrossLoadCell_ChC_mg)) THEN
        rGrossVoted_mg := rGrossLoadCell_ChA_mg;
    ELSIF ((rGrossLoadCell_ChB_mg >= rGrossLoadCell_ChA_mg) AND (rGrossLoadCell_ChB_mg <= rGrossLoadCell_ChC_mg)) OR
          ((rGrossLoadCell_ChB_mg <= rGrossLoadCell_ChA_mg) AND (rGrossLoadCell_ChB_mg >= rGrossLoadCell_ChC_mg)) THEN
        rGrossVoted_mg := rGrossLoadCell_ChB_mg;
    ELSE
        rGrossVoted_mg := rGrossLoadCell_ChC_mg;
    END_IF;
    bGross_TMR_ChA_Valid := TRUE;
    bGross_TMR_ChB_Valid := TRUE;
    bGross_TMR_ChC_Valid := TRUE;
    tGrossDiscrepancyTimer := T#0MS;
    bGrossDegraded := FALSE;
ELSIF (ABS(rGrossLoadCell_ChA_mg - rGrossLoadCell_ChB_mg) <= 1.5) THEN
    rGrossVoted_mg := 0.5 * (rGrossLoadCell_ChA_mg + rGrossLoadCell_ChB_mg);
    bGross_TMR_ChA_Valid := TRUE;
    bGross_TMR_ChB_Valid := TRUE;
    bGross_TMR_ChC_Valid := FALSE;
    bGrossDegraded := TRUE;
ELSIF (ABS(rGrossLoadCell_ChB_mg - rGrossLoadCell_ChC_mg) <= 1.5) THEN
    rGrossVoted_mg := 0.5 * (rGrossLoadCell_ChB_mg + rGrossLoadCell_ChC_mg);
    bGross_TMR_ChA_Valid := FALSE;
    bGross_TMR_ChB_Valid := TRUE;
    bGross_TMR_ChC_Valid := TRUE;
    bGrossDegraded := TRUE;
ELSIF (ABS(rGrossLoadCell_ChA_mg - rGrossLoadCell_ChC_mg) <= 1.5) THEN
    rGrossVoted_mg := 0.5 * (rGrossLoadCell_ChA_mg + rGrossLoadCell_ChC_mg);
    bGross_TMR_ChA_Valid := TRUE;
    bGross_TMR_ChB_Valid := FALSE;
    bGross_TMR_ChC_Valid := TRUE;
    bGrossDegraded := TRUE;
ELSE
    tGrossDiscrepancyTimer := tGrossDiscrepancyTimer + T#1MS;
    bGross_TMR_ChA_Valid := FALSE;
    bGross_TMR_ChB_Valid := FALSE;
    bGross_TMR_ChC_Valid := FALSE;
    bGrossDegraded := TRUE;
END_IF;

(* --- Bank 4: Grade A Isolator Differential Pressure Transmitters (ChA, ChB, ChC) [Pa] --- *)
(* Allowable pressure discrepancy tolerance: 3.5 Pa *)
IF (ABS(rIsolatorPress_ChA_Pa - rIsolatorPress_ChB_Pa) <= 3.5) AND
   (ABS(rIsolatorPress_ChB_Pa - rIsolatorPress_ChC_Pa) <= 3.5) AND
   (ABS(rIsolatorPress_ChA_Pa - rIsolatorPress_ChC_Pa) <= 3.5) THEN
    IF ((rIsolatorPress_ChA_Pa >= rIsolatorPress_ChB_Pa) AND (rIsolatorPress_ChA_Pa <= rIsolatorPress_ChC_Pa)) OR
       ((rIsolatorPress_ChA_Pa <= rIsolatorPress_ChB_Pa) AND (rIsolatorPress_ChA_Pa >= rIsolatorPress_ChC_Pa)) THEN
        rIsolatorPressVoted_Pa := rIsolatorPress_ChA_Pa;
    ELSIF ((rIsolatorPress_ChB_Pa >= rIsolatorPress_ChA_Pa) AND (rIsolatorPress_ChB_Pa <= rIsolatorPress_ChC_Pa)) OR
          ((rIsolatorPress_ChB_Pa <= rIsolatorPress_ChA_Pa) AND (rIsolatorPress_ChB_Pa >= rIsolatorPress_ChC_Pa)) THEN
        rIsolatorPressVoted_Pa := rIsolatorPress_ChB_Pa;
    ELSE
        rIsolatorPressVoted_Pa := rIsolatorPress_ChC_Pa;
    END_IF;
    bPress_TMR_ChA_Valid := TRUE;
    bPress_TMR_ChB_Valid := TRUE;
    bPress_TMR_ChC_Valid := TRUE;
    tPressDiscrepancyTimer := T#0MS;
    bPressDegraded := FALSE;
ELSIF (ABS(rIsolatorPress_ChA_Pa - rIsolatorPress_ChB_Pa) <= 3.5) THEN
    rIsolatorPressVoted_Pa := 0.5 * (rIsolatorPress_ChA_Pa + rIsolatorPress_ChB_Pa);
    bPress_TMR_ChA_Valid := TRUE;
    bPress_TMR_ChB_Valid := TRUE;
    bPress_TMR_ChC_Valid := FALSE;
    bPressDegraded := TRUE;
ELSIF (ABS(rIsolatorPress_ChB_Pa - rIsolatorPress_ChC_Pa) <= 3.5) THEN
    rIsolatorPressVoted_Pa := 0.5 * (rIsolatorPress_ChB_Pa + rIsolatorPress_ChC_Pa);
    bPress_TMR_ChA_Valid := FALSE;
    bPress_TMR_ChB_Valid := TRUE;
    bPress_TMR_ChC_Valid := TRUE;
    bPressDegraded := TRUE;
ELSIF (ABS(rIsolatorPress_ChA_Pa - rIsolatorPress_ChC_Pa) <= 3.5) THEN
    rIsolatorPressVoted_Pa := 0.5 * (rIsolatorPress_ChA_Pa + rIsolatorPress_ChC_Pa);
    bPress_TMR_ChA_Valid := TRUE;
    bPress_TMR_ChB_Valid := FALSE;
    bPress_TMR_ChC_Valid := TRUE;
    bPressDegraded := TRUE;
ELSE
    tPressDiscrepancyTimer := tPressDiscrepancyTimer + T#1MS;
    bPress_TMR_ChA_Valid := FALSE;
    bPress_TMR_ChB_Valid := FALSE;
    bPress_TMR_ChC_Valid := FALSE;
    bPressDegraded := TRUE;
END_IF;

(* --- Bank 5: High-Purity Nitrogen Purge Mass Flowmeters (ChA, ChB, ChC) [L/min] --- *)
(* Allowable flow discrepancy tolerance: 1.2 L/min *)
IF (ABS(rN2Flow_ChA_lnpm - rN2Flow_ChB_lnpm) <= 1.2) AND
   (ABS(rN2Flow_ChB_lnpm - rN2Flow_ChC_lnpm) <= 1.2) AND
   (ABS(rN2Flow_ChA_lnpm - rN2Flow_ChC_lnpm) <= 1.2) THEN
    IF ((rN2Flow_ChA_lnpm >= rN2Flow_ChB_lnpm) AND (rN2Flow_ChA_lnpm <= rN2Flow_ChC_lnpm)) OR
       ((rN2Flow_ChA_lnpm <= rN2Flow_ChB_lnpm) AND (rN2Flow_ChA_lnpm >= rN2Flow_ChC_lnpm)) THEN
        rN2FlowVoted_lnpm := rN2Flow_ChA_lnpm;
    ELSIF ((rN2Flow_ChB_lnpm >= rN2Flow_ChA_lnpm) AND (rN2Flow_ChB_lnpm <= rN2Flow_ChC_lnpm)) OR
          ((rN2Flow_ChB_lnpm <= rN2Flow_ChA_lnpm) AND (rN2Flow_ChB_lnpm >= rN2Flow_ChC_lnpm)) THEN
        rN2FlowVoted_lnpm := rN2Flow_ChB_lnpm;
    ELSE
        rN2FlowVoted_lnpm := rN2Flow_ChC_lnpm;
    END_IF;
    bN2Flow_TMR_ChA_Valid := TRUE;
    bN2Flow_TMR_ChB_Valid := TRUE;
    bN2Flow_TMR_ChC_Valid := TRUE;
    tN2DiscrepancyTimer := T#0MS;
    bN2FlowDegraded := FALSE;
ELSIF (ABS(rN2Flow_ChA_lnpm - rN2Flow_ChB_lnpm) <= 1.2) THEN
    rN2FlowVoted_lnpm := 0.5 * (rN2Flow_ChA_lnpm + rN2Flow_ChB_lnpm);
    bN2Flow_TMR_ChA_Valid := TRUE;
    bN2Flow_TMR_ChB_Valid := TRUE;
    bN2Flow_TMR_ChC_Valid := FALSE;
    bN2FlowDegraded := TRUE;
ELSIF (ABS(rN2Flow_ChB_lnpm - rN2Flow_ChC_lnpm) <= 1.2) THEN
    rN2FlowVoted_lnpm := 0.5 * (rN2Flow_ChB_lnpm + rN2Flow_ChC_lnpm);
    bN2Flow_TMR_ChA_Valid := FALSE;
    bN2Flow_TMR_ChB_Valid := TRUE;
    bN2Flow_TMR_ChC_Valid := TRUE;
    bN2FlowDegraded := TRUE;
ELSIF (ABS(rN2Flow_ChA_lnpm - rN2Flow_ChC_lnpm) <= 1.2) THEN
    rN2FlowVoted_lnpm := 0.5 * (rN2Flow_ChA_lnpm + rN2Flow_ChC_lnpm);
    bN2Flow_TMR_ChA_Valid := TRUE;
    bN2Flow_TMR_ChB_Valid := FALSE;
    bN2Flow_TMR_ChC_Valid := TRUE;
    bN2FlowDegraded := TRUE;
ELSE
    tN2DiscrepancyTimer := tN2DiscrepancyTimer + T#1MS;
    bN2Flow_TMR_ChA_Valid := FALSE;
    bN2Flow_TMR_ChB_Valid := FALSE;
    bN2Flow_TMR_ChC_Valid := FALSE;
    bN2FlowDegraded := TRUE;
END_IF;

(* Assemble sensor measurement vector y_Measured[1..8] *)
y_Measured[1] := rStarwheelVoted_deg;
y_Measured[2] := rDivingNeedlePosCmd_mm;
y_Measured[3] := rPeristalticInletPress_bar;
y_Measured[4] := rTareVoted_mg;
y_Measured[5] := rGrossVoted_mg;
y_Measured[6] := rIsolatorPressVoted_Pa;
y_Measured[7] := rN2FlowVoted_lnpm;
y_Measured[8] := rCrimpForceSensor_N;

(* ========================================================================================= *)
(* SECTION 2: PHASE 2 - STATE-SPACE PREDICTION & KALMAN OBSERVER FILTERING                   *)
(* ========================================================================================= *)
(* Compute output prediction y_Predict = C * x_State + D * u_Control *)
FOR idx_i := 1 TO 8 DO
    rScratchAccum := 0.0;
    FOR idx_j := 1 TO 16 DO
        rScratchAccum := rScratchAccum + (C_Matrix[idx_i, idx_j] * x_State[idx_j]);
    END_FOR;
    FOR idx_k := 1 TO 8 DO
        rScratchAccum := rScratchAccum + (D_Matrix[idx_i, idx_k] * u_Control[idx_k]);
    END_FOR;
    y_Predict[idx_i] := rScratchAccum;
    y_Residual[idx_i] := y_Measured[idx_i] - y_Predict[idx_i];
END_FOR;

(* Kalman Observer Innovation Correction: x_State = x_State + L * y_Residual *)
FOR idx_i := 1 TO 16 DO
    rScratchAccum := 0.0;
    FOR idx_j := 1 TO 8 DO
        rScratchAccum := rScratchAccum + (arObserverGain_L[idx_i, idx_j] * y_Residual[idx_j]);
    END_FOR;
    x_State[idx_i] := x_State[idx_i] + rScratchAccum;
END_FOR;

(* State Forward Propagation: x_Predict = A * x_State + B * u_Control *)
FOR idx_i := 1 TO 16 DO
    rScratchAccum := 0.0;
    FOR idx_j := 1 TO 16 DO
        rScratchAccum := rScratchAccum + (A_Matrix[idx_i, idx_j] * x_State[idx_j]);
    END_FOR;
    FOR idx_k := 1 TO 8 DO
        rScratchAccum := rScratchAccum + (B_Matrix[idx_i, idx_k] * u_Control[idx_k]);
    END_FOR;
    x_Predict[idx_i] := rScratchAccum;
END_FOR;

(* ========================================================================================= *)
(* SECTION 3: PHASE 3 - RECEDING-HORIZON MPC QUADRATIC OPTIMIZATION                          *)
(* ========================================================================================= *)
(* Solves constrained convex quadratic program over horizon using projected gradient steps   *)
(* Objective: min 0.5 * u' * H * u + g' * u, s.t. u_min <= u <= u_max, |du| <= du_max        *)

(* Setpoint reference state assignment *)
x_Target[1] := 0.0;                       (* Target angular error is 0.0 deg *)
x_Target[2] := 0.0;                       (* Target angular velocity error is 0.0 deg/s *)
x_Target[3] := rDivingNeedlePosCmd_mm;    (* Synchronized bottom-up stroke *)
x_Target[4] := rDivingNeedleVelCmd_mms;   (* Synchronized dive velocity *)
x_Target[5] := 1.85;                      (* Target tubing pressure 1.85 bar *)
x_Target[6] := 185.0;                     (* Meniscus velocity 185 mm/s *)
x_Target[7] := rTargetDosingVol_ml;       (* Recipe dosing volume [ml] *)
x_Target[8] := rLiquidSurfaceVelocity_mms;(* Liquid surface rising rate *)
x_Target[9] := 0.0;                       (* Restoring beam equilibrium *)
x_Target[10] := 0.0;                      (* Voice-coil dynamic null current *)
x_Target[11] := 0.0;                      (* Gross beam equilibrium *)
x_Target[12] := 0.0;                      (* Gross voice-coil null current *)
x_Target[13] := rIsolatorDiffPress_Set_Pa;(* Grade A differential pressure 45 Pa *)
x_Target[14] := rN2SupplyPressure_bar;    (* N2 supply pressure 4.5 bar *)
x_Target[15] := -0.65;                    (* Stoppering vacuum level -0.65 bar *)
x_Target[16] := rNominalCrimpForce_N;     (* Crimp seal force 145 N *)

(* State Tracking Error Calculation *)
FOR idx_i := 1 TO 16 DO
    x_Error[idx_i] := x_Predict[idx_i] - x_Target[idx_i];
END_FOR;

(* Unrolled Gradient Projection Iterations (3 Iterations per Millisecond Task Cycle) *)
FOR idx_k := 1 TO 8 DO
    u_Optimal[idx_k] := u_Control[idx_k];
END_FOR;

(* Projected Gradient Iteration 1 *)
FOR idx_j := 1 TO 8 DO
    rScratchAccum := R_Weight[idx_j, idx_j] * u_Optimal[idx_j];
    FOR idx_i := 1 TO 16 DO
        rScratchAccum := rScratchAccum + (B_Matrix[idx_i, idx_j] * P_Weight[idx_i, idx_i] * x_Error[idx_i]);
    END_FOR;
    u_Optimal[idx_j] := u_Optimal[idx_j] - (rGradStep * rScratchAccum);
    (* Saturation box constraints *)
    IF u_Optimal[idx_j] < arU_Min[idx_j] THEN
        u_Optimal[idx_j] := arU_Min[idx_j];
    ELSIF u_Optimal[idx_j] > arU_Max[idx_j] THEN
        u_Optimal[idx_j] := arU_Max[idx_j];
    END_IF;
END_FOR;

(* Projected Gradient Iteration 2 *)
FOR idx_j := 1 TO 8 DO
    rScratchAccum := R_Weight[idx_j, idx_j] * u_Optimal[idx_j];
    FOR idx_i := 1 TO 16 DO
        rScratchAccum := rScratchAccum + (B_Matrix[idx_i, idx_j] * P_Weight[idx_i, idx_i] * x_Error[idx_i]);
    END_FOR;
    u_Optimal[idx_j] := u_Optimal[idx_j] - (rGradStep * rScratchAccum);
    IF u_Optimal[idx_j] < arU_Min[idx_j] THEN
        u_Optimal[idx_j] := arU_Min[idx_j];
    ELSIF u_Optimal[idx_j] > arU_Max[idx_j] THEN
        u_Optimal[idx_j] := arU_Max[idx_j];
    END_IF;
END_FOR;

(* Projected Gradient Iteration 3 *)
FOR idx_j := 1 TO 8 DO
    rScratchAccum := R_Weight[idx_j, idx_j] * u_Optimal[idx_j];
    FOR idx_i := 1 TO 16 DO
        rScratchAccum := rScratchAccum + (B_Matrix[idx_i, idx_j] * P_Weight[idx_i, idx_i] * x_Error[idx_i]);
    END_FOR;
    u_Optimal[idx_j] := u_Optimal[idx_j] - (rGradStep * rScratchAccum);
    IF u_Optimal[idx_j] < arU_Min[idx_j] THEN
        u_Optimal[idx_j] := arU_Min[idx_j];
    ELSIF u_Optimal[idx_j] > arU_Max[idx_j] THEN
        u_Optimal[idx_j] := arU_Max[idx_j];
    END_IF;
END_FOR;

(* Apply Slew Rate Bounds to Control Outputs *)
FOR idx_j := 1 TO 8 DO
    du_Delta[idx_j] := u_Optimal[idx_j] - u_Prev[idx_j];
    IF du_Delta[idx_j] > arDeltaU_Max[idx_j] THEN
        u_Control[idx_j] := u_Prev[idx_j] + arDeltaU_Max[idx_j];
    ELSIF du_Delta[idx_j] < -arDeltaU_Max[idx_j] THEN
        u_Control[idx_j] := u_Prev[idx_j] - arDeltaU_Max[idx_j];
    ELSE
        u_Control[idx_j] := u_Optimal[idx_j];
    END_IF;
    u_Prev[idx_j] := u_Control[idx_j];
END_FOR;

(* Map MPC Controls to Actuator Command Outputs *)
rMainTurretSpeedCmd_RPM := 60.0 + u_Control[1]; (* 600 VPM at 10 pockets = 60 RPM base *)
IF rMainTurretSpeedCmd_RPM < 0.0 THEN rMainTurretSpeedCmd_RPM := 0.0; END_IF;
IF rMainTurretSpeedCmd_RPM > 75.0 THEN rMainTurretSpeedCmd_RPM := 75.0; END_IF;

rN2PurgeValveCmd_pct := 50.0 + u_Control[7];
IF rN2PurgeValveCmd_pct < 0.0 THEN rN2PurgeValveCmd_pct := 0.0; END_IF;
IF rN2PurgeValveCmd_pct > 100.0 THEN rN2PurgeValveCmd_pct := 100.0; END_IF;

rStopperPickVacuumCmd_bar := -0.65 + (u_Control[1] * 0.002);
IF rStopperPickVacuumCmd_bar > -0.20 THEN rStopperPickVacuumCmd_bar := -0.20; END_IF;
IF rStopperPickVacuumCmd_bar < -0.85 THEN rStopperPickVacuumCmd_bar := -0.85; END_IF;

rCrimpServoTorqueCmd_Nm := 12.5 + (u_Control[8] * 0.15);
IF rCrimpServoTorqueCmd_Nm < 2.0 THEN rCrimpServoTorqueCmd_Nm := 2.0; END_IF;
IF rCrimpServoTorqueCmd_Nm > 25.0 THEN rCrimpServoTorqueCmd_Nm := 25.0; END_IF;

(* ========================================================================================= *)
(* SECTION 4: PHASE 4 - MULTI-CHANNEL PERISTALTIC DOSING & BOTTOM-UP DIVING TRAJECTORY       *)
(* ========================================================================================= *)
(* Realizes 5th-order jerk-limited polynomial trajectory for needle diving axis.             *)
(* Trajectory tracks rising liquid meniscus: MeniscusHeight = VolumeDispensed / VialArea     *)

(* Calculate modular angular position within active 30-degree starwheel pocket sector *)
rTurretIndexAngle_deg := rStarwheelVoted_deg;
WHILE rTurretIndexAngle_deg >= 30.0 DO
    rTurretIndexAngle_deg := rTurretIndexAngle_deg - 30.0;
END_WHILE;
WHILE rTurretIndexAngle_deg < 0.0 DO
    rTurretIndexAngle_deg := rTurretIndexAngle_deg + 30.0;
END_WHILE;

(* Dimensionless phase parameter tau in range [0.0, 1.0] *)
rDimensionlessPhase_tau := rTurretIndexAngle_deg / 30.0;
IF rDimensionlessPhase_tau < 0.0 THEN rDimensionlessPhase_tau := 0.0; END_IF;
IF rDimensionlessPhase_tau > 1.0 THEN rDimensionlessPhase_tau := 1.0; END_IF;

(* 5th-Order S-Curve Polynomial: S(tau) = 10*tau^3 - 15*tau^4 + 6*tau^5 *)
rPolynomialS_tau := (10.0 * rDimensionlessPhase_tau * rDimensionlessPhase_tau * rDimensionlessPhase_tau) -
                    (15.0 * rDimensionlessPhase_tau * rDimensionlessPhase_tau * rDimensionlessPhase_tau * rDimensionlessPhase_tau) +
                    (6.0 * rDimensionlessPhase_tau * rDimensionlessPhase_tau * rDimensionlessPhase_tau * rDimensionlessPhase_tau * rDimensionlessPhase_tau);

(* Derivative: V(tau) = 30*tau^2 - 60*tau^3 + 30*tau^4 *)
rPolynomialV_tau := (30.0 * rDimensionlessPhase_tau * rDimensionlessPhase_tau) -
                    (60.0 * rDimensionlessPhase_tau * rDimensionlessPhase_tau * rDimensionlessPhase_tau) +
                    (30.0 * rDimensionlessPhase_tau * rDimensionlessPhase_tau * rDimensionlessPhase_tau * rDimensionlessPhase_tau);

(* Calculate liquid surface rise dynamics based on nominal vial internal cross section *)
(* Vial cross-sectional area: A_vial = PI * (d_inner / 2)^2 *)
(* For 10R vial with d_inner = 12.6 mm: A_vial = 3.14159 * 6.3^2 = 124.69 mm2 *)
(* 1 ml = 1000 mm3 -> Liquid level rise per ml = 1000 / 124.69 = 8.02 mm/ml *)
rLiquidLevelRise_mm := (rTargetDosingVol_ml * rPolynomialS_tau) * 8.02;
rLiquidSurfaceVelocity_mms := (rTargetDosingVol_ml * rPolynomialV_tau * (600.0 / 60.0)) * 8.02;

(* Synchronized diving needle trajectory command: starts at bottom and retracts upward *)
(* Needle tip maintains rMeniscusOffsetDist_mm (2.5 mm) above rising liquid surface *)
IF (iFsmState = 5) OR (iFsmState = 4) THEN
    (* Production or Priming Active *)
    rDivingNeedlePosCmd_mm := (rDivingNeedleStroke_mm - rLiquidLevelRise_mm) - rMeniscusOffsetDist_mm;
    IF rDivingNeedlePosCmd_mm < 5.0 THEN
        rDivingNeedlePosCmd_mm := 5.0;
    ELSIF rDivingNeedlePosCmd_mm > rDivingNeedleStroke_mm THEN
        rDivingNeedlePosCmd_mm := rDivingNeedleStroke_mm;
    END_IF;
    rDivingNeedleVelCmd_mms := rLiquidSurfaceVelocity_mms;
ELSE
    (* Parked in high home position *)
    rDivingNeedlePosCmd_mm := 0.0;
    rDivingNeedleVelCmd_mms := 0.0;
END_IF;

(* Compute 12-Channel Peristaltic Dosing Setpoints with Individual Adaptive Trim *)
FOR idx_i := 1 TO 12 DO
    arNeedleDoseCmd_ml[idx_i] := rTargetDosingVol_ml + (arPumpOffsetTrim_ul[idx_i] * 0.001);
    (* Clamp individual needle dose within safety bounds (+/- 15% of target) *)
    IF arNeedleDoseCmd_ml[idx_i] < (rTargetDosingVol_ml * 0.85) THEN
        arNeedleDoseCmd_ml[idx_i] := rTargetDosingVol_ml * 0.85;
    ELSIF arNeedleDoseCmd_ml[idx_i] > (rTargetDosingVol_ml * 1.15) THEN
        arNeedleDoseCmd_ml[idx_i] := rTargetDosingVol_ml * 1.15;
    END_IF;
END_FOR;
"""
