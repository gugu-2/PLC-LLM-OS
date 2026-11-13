# Phase 3 Builder for FB_Pharma_Bioprocess_TFF_Ultrafiltration_Diafiltration
import os, sys

def get_phase3_code():
    lines = []
    lines.append("""(*
====================================================================================================
PHASE 3: RECEDING-HORIZON MPC OPTIMIZATION WITH PROJECTED GRADIENT DESCENT (PGD) & SLEW LIMITS
Cyber-Physical Control Highlights:
  - Prediction Horizon N = 5 steps (50.0 [ms] lookahead)
  - 6 Unrolled Iterations of Projected Gradient Descent (PGD)
  - Dynamic TMP & Wall Shear Decoupling: feed pump servo speed dynamically controls wall shear
    rate while the retentate proportional pinch/diaphragm valve simultaneously modulates TMP
    without fouling or shearing delicate proteins
  - Multi-Objective Quadratic Cost Functional J = sum(e_x^T * Q * e_x + e_u^T * R * e_u) + e_N^T * P * e_N
  - Backward Adjoint Costate Vector lambda[k] Propagation via Transpose System Adjoint
  - Dynamic Slew-Rate Clamping & Hard Physical Actuator Saturation Box Projections
====================================================================================================
*)

(* -------------------------------------------------------------------------------------------------
 * 1. Dynamic State-Space Setpoint Reference Trajectory Formulation
 * ------------------------------------------------------------------------------------------------- *)
arrX_Ref[1] := rTarget_TMP_bar;             (* Recipe Transmembrane Pressure Setpoint [bar] *)
arrX_Ref[2] := 45.0;                        (* Target Sustainable Permeate Flux [LMH] *)
IF nState = 4 THEN
    arrX_Ref[3] := rTarget_UF1_Conc_gL;     (* Target Intermediate Concentration [g/L] *)
ELSIF nState = 6 THEN
    arrX_Ref[3] := rTarget_Final_Conc_gL;   (* Target Bulk Drug Substance Final Concentration [g/L] *)
ELSE
    arrX_Ref[3] := arrX_State[3];           (* Hold Current Concentration *)
END_IF;
arrX_Ref[4] := 0.20;                        (* Target Minimal Gel Polarization Resistance [10^11 m-1] *)
arrX_Ref[5] := rTarget_WallShearRate_s1;    (* Target Cassette Retentate Wall Shear Rate [s-1] *)
arrX_Ref[6] := rTarget_Diafiltration_DV;    (* Recipe Target Diafiltration Volume Exchange [DV] *)
IF nState = 7 THEN
    arrX_Ref[7] := rTarget_ChilldownTemp_degC; (* Active Chilldown Target: 4.0 [deg C] *)
ELSIF nState = 10 THEN
    arrX_Ref[7] := rTarget_CIP_Temp_degC;      (* Caustic CIP Wash Target: 45.0 [deg C] *)
ELSE
    arrX_Ref[7] := rTarget_ProcessTemp_degC;   (* Active Bioprocess Recirculation Target: 12.0 [deg C] *)
END_IF;
arrX_Ref[8] := 0.0;                         (* Sump Mass Balance Target: Exactly 0.0 [g] Deviation *)

(* Nominal Actuator Reference Offsets *)
arrU_Ref[1] := 1850.0;                      (* Nominal Feed Pump Speed [rpm] *)
arrU_Ref[2] := 45.0;                        (* Nominal Retentate Backpressure Valve [%] *)
arrU_Ref[3] := 35.0;                        (* Nominal Diafiltration Buffer Pump [%] *)
arrU_Ref[4] := 60.0;                        (* Nominal Permeate Valve [%] *)
arrU_Ref[5] := 25.0;                        (* Nominal Chiller Valve [%] *)
arrU_Ref[6] := 0.0;                         (* Nominal Divert Valve: Closed (0.0%) *)

(* Initialize Horizon Actuators with Previous Solution (Warm-Start) *)
FOR kStepIndex := 0 TO 4 DO
    FOR jLoopIndex := 1 TO 6 DO
        arrU_Horizon[kStepIndex, jLoopIndex] := arrU_Act[jLoopIndex];
    END_FOR;
END_FOR;

(* Initialize Horizon Initial State with Current Observer Estimate *)
FOR jLoopIndex := 1 TO 8 DO
    arrX_Horizon[0, jLoopIndex] := arrX_State[jLoopIndex];
END_FOR;

(* -------------------------------------------------------------------------------------------------
 * 2. Unrolled 6-Iteration Projected Gradient Descent (PGD) Optimization Loop
 * ------------------------------------------------------------------------------------------------- *)
FOR iterIndex := 1 TO 6 DO
    (* Step 2A: Forward Simulation Across Prediction Horizon N = 5 *)
    FOR kStepIndex := 0 TO 4 DO
        (* Nonlinear Dynamic Decoupling Feedforward Compensation *)
        (* Feed pump speed dynamically compensates for retentate valve restriction *)
        rDecoupledFeedPump_rpm := arrU_Horizon[kStepIndex, 1] + 
                                  (rCrossflowDecoupleGain * (60.0 - arrU_Horizon[kStepIndex, 2]));
        IF rDecoupledFeedPump_rpm > 3000.0 THEN
            rDecoupledFeedPump_rpm := 3000.0;
        ELSIF rDecoupledFeedPump_rpm < 200.0 THEN
            rDecoupledFeedPump_rpm := 200.0;
        END_IF;

        FOR iLoopIndex := 1 TO 8 DO
            arrX_Horizon[kStepIndex + 1, iLoopIndex] := 0.0;
            (* State Transition Multiplication: A * x[k] *)
            FOR jLoopIndex := 1 TO 8 DO
                arrX_Horizon[kStepIndex + 1, iLoopIndex] := arrX_Horizon[kStepIndex + 1, iLoopIndex] + 
                    (arrA_Matrix[iLoopIndex, jLoopIndex] * arrX_Horizon[kStepIndex, jLoopIndex]);
            END_FOR;
            (* Control Coupling Multiplication: B * u[k] *)
            arrX_Horizon[kStepIndex + 1, iLoopIndex] := arrX_Horizon[kStepIndex + 1, iLoopIndex] + 
                (arrB_Matrix[iLoopIndex, 1] * rDecoupledFeedPump_rpm);
            FOR jLoopIndex := 2 TO 6 DO
                arrX_Horizon[kStepIndex + 1, iLoopIndex] := arrX_Horizon[kStepIndex + 1, iLoopIndex] + 
                    (arrB_Matrix[iLoopIndex, jLoopIndex] * arrU_Horizon[kStepIndex, jLoopIndex]);
            END_FOR;
        END_FOR;
    END_FOR;

    (* Step 2B: Backward Adjoint Costate Backpropagation: lambda[N] = P * (x[N] - x_ref) *)
    FOR iLoopIndex := 1 TO 8 DO
        arrLambda[5, iLoopIndex] := 0.0;
        FOR jLoopIndex := 1 TO 8 DO
            arrLambda[5, iLoopIndex] := arrLambda[5, iLoopIndex] + 
                (arrP_Terminal[iLoopIndex, jLoopIndex] * (arrX_Horizon[5, jLoopIndex] - arrX_Ref[jLoopIndex]));
        END_FOR;
    END_FOR;

    (* Backpropagate Costate: lambda[k] = Q * (x[k] - x_ref) + A^T * lambda[k+1] *)
    FOR kStepIndex := 4 TO 0 BY -1 DO
        FOR iLoopIndex := 1 TO 8 DO
            arrLambda[kStepIndex, iLoopIndex] := 0.0;
            FOR jLoopIndex := 1 TO 8 DO
                arrLambda[kStepIndex, iLoopIndex] := arrLambda[kStepIndex, iLoopIndex] + 
                    (arrQ_Weight[iLoopIndex, jLoopIndex] * (arrX_Horizon[kStepIndex, jLoopIndex] - arrX_Ref[jLoopIndex])) + 
                    (arrA_Matrix[jLoopIndex, iLoopIndex] * arrLambda[kStepIndex + 1, jLoopIndex]);
            END_FOR;
        END_FOR;
    END_FOR;

    (* Step 2C: Compute Unrolled Cost Gradients: grad_u[k] = R * (u[k] - u_ref) + B^T * lambda[k+1] *)
    FOR kStepIndex := 0 TO 4 DO
        FOR iLoopIndex := 1 TO 6 DO
            arrGrad_U[kStepIndex, iLoopIndex] := 0.0;
            FOR jLoopIndex := 1 TO 6 DO
                arrGrad_U[kStepIndex, iLoopIndex] := arrGrad_U[kStepIndex, iLoopIndex] + 
                    (arrR_Weight[iLoopIndex, jLoopIndex] * (arrU_Horizon[kStepIndex, jLoopIndex] - arrU_Ref[jLoopIndex]));
            END_FOR;
            FOR jLoopIndex := 1 TO 8 DO
                arrGrad_U[kStepIndex, iLoopIndex] := arrGrad_U[kStepIndex, iLoopIndex] + 
                    (arrB_Matrix[jLoopIndex, iLoopIndex] * arrLambda[kStepIndex + 1, jLoopIndex]);
            END_FOR;
        END_FOR;
    END_FOR;

    (* Step 2D: Gradient Descent Step, Slew-Rate Projection & Box Boundary Clamping *)
    FOR kStepIndex := 0 TO 4 DO
        FOR iLoopIndex := 1 TO 6 DO
            (* Gradient Descent Update *)
            arrU_Horizon[kStepIndex, iLoopIndex] := arrU_Horizon[kStepIndex, iLoopIndex] - 
                (rPGD_Alpha_Step * arrGrad_U[kStepIndex, iLoopIndex]);

            (* Dynamic Slew-Rate Limiter Projection *)
            IF kStepIndex = 0 THEN
                IF arrU_Horizon[0, iLoopIndex] > (arrU_Prev[iLoopIndex] + arrDeltaU_Max[iLoopIndex]) THEN
                    arrU_Horizon[0, iLoopIndex] := arrU_Prev[iLoopIndex] + arrDeltaU_Max[iLoopIndex];
                ELSIF arrU_Horizon[0, iLoopIndex] < (arrU_Prev[iLoopIndex] - arrDeltaU_Max[iLoopIndex]) THEN
                    arrU_Horizon[0, iLoopIndex] := arrU_Prev[iLoopIndex] - arrDeltaU_Max[iLoopIndex];
                END_IF;
            ELSE
                IF arrU_Horizon[kStepIndex, iLoopIndex] > (arrU_Horizon[kStepIndex - 1, iLoopIndex] + arrDeltaU_Max[iLoopIndex]) THEN
                    arrU_Horizon[kStepIndex, iLoopIndex] := arrU_Horizon[kStepIndex - 1, iLoopIndex] + arrDeltaU_Max[iLoopIndex];
                ELSIF arrU_Horizon[kStepIndex, iLoopIndex] < (arrU_Horizon[kStepIndex - 1, iLoopIndex] - arrDeltaU_Max[iLoopIndex]) THEN
                    arrU_Horizon[kStepIndex, iLoopIndex] := arrU_Horizon[kStepIndex - 1, iLoopIndex] - arrDeltaU_Max[iLoopIndex];
                END_IF;
            END_IF;

            (* Hard Actuator Physical Saturation Clamping *)
            IF arrU_Horizon[kStepIndex, iLoopIndex] > arrU_Max[iLoopIndex] THEN
                arrU_Horizon[kStepIndex, iLoopIndex] := arrU_Max[iLoopIndex];
            ELSIF arrU_Horizon[kStepIndex, iLoopIndex] < arrU_Min[iLoopIndex] THEN
                arrU_Horizon[kStepIndex, iLoopIndex] := arrU_Min[iLoopIndex];
            END_IF;
        END_FOR;
    END_FOR;
END_FOR;

(* -------------------------------------------------------------------------------------------------
 * 3. Extract Receding-Horizon Control Commands u[0] and Map to Skid Actuators
 * ------------------------------------------------------------------------------------------------- *)
IF bEnable AND (NOT bSystemTrip_Interlock) AND (NOT bEmergencyStop) THEN
    (* Feed Pump Speed Command [rpm] with Decoupling *)
    rFeedPump_Speed_Cmd_rpm := arrU_Horizon[0, 1] + (rCrossflowDecoupleGain * (60.0 - arrU_Horizon[0, 2]));
    IF rFeedPump_Speed_Cmd_rpm > 3000.0 THEN
        rFeedPump_Speed_Cmd_rpm := 3000.0;
    ELSIF rFeedPump_Speed_Cmd_rpm < 0.0 THEN
        rFeedPump_Speed_Cmd_rpm := 0.0;
    END_IF;

    (* Retentate Proportional Backpressure Valve [%] *)
    rRetValve_Pos_Cmd_pct := arrU_Horizon[0, 2];

    (* Diafiltration Buffer Metering Pump Command [%] *)
    rBufferPump_Speed_Cmd_pct := arrU_Horizon[0, 3];

    (* Permeate Line Modulating Control Valve Command [%] *)
    rPermValve_Pos_Cmd_pct := arrU_Horizon[0, 4];

    (* Heat Exchanger Chiller Glycol Valve Command [%] *)
    rChillerValve_Pos_Cmd_pct := arrU_Horizon[0, 5];

    (* Product Harvest Divert / Drain Valve Command [%] *)
    rFeedDivertValve_Pos_pct := arrU_Horizon[0, 6];

    (* Save State for Next Cycle Slew Calculation *)
    arrU_Act[1] := rFeedPump_Speed_Cmd_rpm;
    arrU_Act[2] := rRetValve_Pos_Cmd_pct;
    arrU_Act[3] := rBufferPump_Speed_Cmd_pct;
    arrU_Act[4] := rPermValve_Pos_Cmd_pct;
    arrU_Act[5] := rChillerValve_Pos_Cmd_pct;
    arrU_Act[6] := rFeedDivertValve_Pos_pct;

    FOR iLoopIndex := 1 TO 6 DO
        arrU_Prev[iLoopIndex] := arrU_Act[iLoopIndex];
    END_FOR;
ELSE
    (* Fail-Safe Shutdown State: All Pumps Cut Off, Valves Vented *)
    rFeedPump_Speed_Cmd_rpm := 0.0;
    rRetValve_Pos_Cmd_pct := 100.0;         (* Full Open to depressurize cassette *)
    rBufferPump_Speed_Cmd_pct := 0.0;
    rPermValve_Pos_Cmd_pct := 0.0;          (* Permeate line closed *)
    rChillerValve_Pos_Cmd_pct := 0.0;
    rFeedDivertValve_Pos_pct := 0.0;
    bFeedPump_Run_Enable := FALSE;
    bBufferPump_Run_Enable := FALSE;
    bPermeateIsolation_Open := FALSE;
    FOR iLoopIndex := 1 TO 6 DO
        arrU_Act[iLoopIndex] := 0.0;
        arrU_Prev[iLoopIndex] := 0.0;
    END_FOR;
END_IF;""")

    return "\n".join(lines)

print("Phase 3 builder ready")
