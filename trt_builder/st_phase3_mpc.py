# trt_builder/st_phase3_mpc.py
"""
Phase 3: Receding-Horizon Model Predictive Control (MPC) with Projected Gradient Descent (PGD) & Slew Limits
for FB_Steel_BlastFurnace_TopGas_TRT_PowerRecovery
"""

def get_phase3_mpc():
    return """(* ==================================================================================================== *)
(* PHASE 3: RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) WITH PROJECTED GRADIENT DESCENT (PGD)        *)
(* ==================================================================================================== *)
(* ---------------------------------------------------------------------------------------------------- *)
(* 3.1 MPC OPTIMIZATION FORMULATION (Np = 5 Prediction Steps, Nc = 3 Control Steps)                      *)
(* Decouples Top Gas Pressure Regulation from Power Generation & Prevents Safety Bleeder Lifting        *)
(* ---------------------------------------------------------------------------------------------------- *)

IF bAutoMode AND (NOT bEmergencyMasterTripActive) THEN
    (* Reset Candidate Move Perturbations *)
    FOR kIdx := 1 TO 3 DO
        FOR pIdx := 1 TO 5 DO
            aMpcDeltaU[kIdx, pIdx] := 0.0;
            aMpcGradU[kIdx, pIdx] := 0.0;
        END_FOR;
    END_FOR;

    (* ------------------------------------------------------------------------------------------------ *)
    (* UNROLLED PROJECTED GRADIENT DESCENT (PGD) SOLVER - 6 ITERATIONS PER PLC CYCLE                     *)
    (* ------------------------------------------------------------------------------------------------ *)
    FOR nIter := 1 TO 6 DO
        (* Step A: Forward Trajectory Rollout over Prediction Horizon Np = 5 *)
        FOR kIdx := 1 TO 5 DO
            FOR iIdx := 1 TO 8 DO
                rTempSum := 0.0;
                (* State transition contribution from prior step *)
                IF kIdx = 1 THEN
                    FOR jIdx := 1 TO 8 DO
                        rTempSum := rTempSum + (mA[iIdx, jIdx] * aStateEst[jIdx]);
                    END_FOR;
                ELSE
                    FOR jIdx := 1 TO 8 DO
                        rTempSum := rTempSum + (mA[iIdx, jIdx] * aMpcPredState[kIdx - 1, jIdx]);
                    END_FOR;
                END_IF;

                (* Actuator contribution *)
                IF kIdx <= 3 THEN
                    FOR pIdx := 1 TO 5 DO
                        rTempSum := rTempSum + (mB[iIdx, pIdx] * (aControlPrev[pIdx] + aMpcDeltaU[kIdx, pIdx]));
                    END_FOR;
                ELSE
                    FOR pIdx := 1 TO 5 DO
                        rTempSum := rTempSum + (mB[iIdx, pIdx] * (aControlPrev[pIdx] + aMpcDeltaU[3, pIdx]));
                    END_FOR;
                END_IF;

                aMpcPredState[kIdx, iIdx] := rTempSum;
            END_FOR;
        END_FOR;

        (* Step B: Quadratic Objective Cost Functional Assessment *)
        rMpcStateCost := 0.0;
        rMpcInputCost := 0.0;
        rMpcTerminalCost := 0.0;

        FOR kIdx := 1 TO 5 DO
            FOR iIdx := 1 TO 8 DO
                rMpcStateCost := rMpcStateCost + (mQ[iIdx, iIdx] * aMpcPredState[kIdx, iIdx] * aMpcPredState[kIdx, iIdx]);
            END_FOR;
        END_FOR;

        FOR kIdx := 1 TO 3 DO
            FOR pIdx := 1 TO 5 DO
                rMpcInputCost := rMpcInputCost + (mR[pIdx, pIdx] * aMpcDeltaU[kIdx, pIdx] * aMpcDeltaU[kIdx, pIdx]);
            END_FOR;
        END_FOR;

        FOR iIdx := 1 TO 8 DO
            rMpcTerminalCost := rMpcTerminalCost + (mP[iIdx, iIdx] * aMpcPredState[5, iIdx] * aMpcPredState[5, iIdx]);
        END_FOR;

        rMpcObjectiveCost := rMpcStateCost + rMpcInputCost + rMpcTerminalCost;

        (* Step C: Backward Adjoint Sensitivity & Analytical Gradient Computation *)
        FOR kIdx := 1 TO 3 DO
            FOR pIdx := 1 TO 5 DO
                (* Actuator effort gradient: 2 * R * delta_u *)
                rTempGrad := 2.0 * mR[pIdx, pIdx] * aMpcDeltaU[kIdx, pIdx];

                (* Forward sensitivity backpropagation through state tracking penalties *)
                FOR iIdx := 1 TO 8 DO
                    rTempGrad := rTempGrad + (mB[iIdx, pIdx] * (2.0 * mQ[iIdx, iIdx] * aMpcPredState[kIdx, iIdx]));
                END_FOR;

                (* Terminal horizon boundary contribution at final control step *)
                IF kIdx = 3 THEN
                    FOR iIdx := 1 TO 8 DO
                        rTempGrad := rTempGrad + (mB[iIdx, pIdx] * (2.0 * mP[iIdx, iIdx] * aMpcPredState[5, iIdx]));
                    END_FOR;
                END_IF;

                aMpcGradU[kIdx, pIdx] := rTempGrad;
            END_FOR;
        END_FOR;

        (* Step D: Projected Gradient Descent Update with Slew and Position Clamps *)
        FOR kIdx := 1 TO 3 DO
            FOR pIdx := 1 TO 5 DO
                (* Gradient Step *)
                aMpcDeltaU[kIdx, pIdx] := aMpcDeltaU[kIdx, pIdx] - (aMpcStepSize[pIdx] * aMpcGradU[kIdx, pIdx]);

                (* Dynamic Slew Rate Limit Projection [-delta_u_max, +delta_u_max] *)
                IF aMpcDeltaU[kIdx, pIdx] > aActuatorMaxSlewRate[pIdx] THEN
                    aMpcDeltaU[kIdx, pIdx] := aActuatorMaxSlewRate[pIdx];
                ELSIF aMpcDeltaU[kIdx, pIdx] < -aActuatorMaxSlewRate[pIdx] THEN
                    aMpcDeltaU[kIdx, pIdx] := -aActuatorMaxSlewRate[pIdx];
                END_IF;

                (* Absolute Position Clamp Projection [u_min, u_max] *)
                IF (aControlPrev[pIdx] + aMpcDeltaU[kIdx, pIdx]) > aActuatorMaxLimit[pIdx] THEN
                    aMpcDeltaU[kIdx, pIdx] := aActuatorMaxLimit[pIdx] - aControlPrev[pIdx];
                ELSIF (aControlPrev[pIdx] + aMpcDeltaU[kIdx, pIdx]) < aActuatorMinLimit[pIdx] THEN
                    aMpcDeltaU[kIdx, pIdx] := aActuatorMinLimit[pIdx] - aControlPrev[pIdx];
                END_IF;
            END_FOR;
        END_FOR;
    END_FOR;

    (* Extract Receding Step 1 Optimal Control Adjustments *)
    rVSV_Demand_Unclamped      := aControlPrev[1] + aMpcDeltaU[1, 1];
    rSeptumV1_Demand_Unclamped := aControlPrev[2] + aMpcDeltaU[1, 2];
    rSeptumV2_Demand_Unclamped := aControlPrev[3] + aMpcDeltaU[1, 3];
    rSeptumV3_Demand_Unclamped := aControlPrev[4] + aMpcDeltaU[1, 4];

ELSE
    (* Fallback / Manual Operating Mode - Smoothly Track Previous Setpoints *)
    rVSV_Demand_Unclamped      := aControlPrev[1];
    rSeptumV1_Demand_Unclamped := aControlPrev[2];
    rSeptumV2_Demand_Unclamped := aControlPrev[3];
    rSeptumV3_Demand_Unclamped := aControlPrev[4];
END_IF;


(* ---------------------------------------------------------------------------------------------------- *)
(* 3.2 COUPLING & DECOUPLING COORDINATOR: BLAST FURNACE SLIP SURGE ABSORPTION                           *)
(* High-Speed Trim Feedforward from Septum Valve 3 to Buffer Furnace Slips without Bleeder Lift         *)
(* ---------------------------------------------------------------------------------------------------- *)
IF rTopGasPressure_ROC > 12.0 THEN
    (* Severe Blast Furnace Slip Surge Detected: Force Fast Trim Open *)
    rSeptumV3_Demand_Unclamped := rSeptumV3_Demand_Unclamped + (rTopGasPressure_ROC * 0.35);
    IF rTopGasPressure_ROC > 20.0 THEN
        rSeptumV2_Demand_Unclamped := rSeptumV2_Demand_Unclamped + ((rTopGasPressure_ROC - 20.0) * 0.45);
    END_IF;
ELSIF rTopGasPressure_ROC < -12.0 THEN
    (* Sudden Negative Pressure Dip (Blower Scram or Burden Collapse): Choke Trim *)
    rSeptumV3_Demand_Unclamped := rSeptumV3_Demand_Unclamped + (rTopGasPressure_ROC * 0.25);
END_IF;

(* Clamp Septum Valve Position Demands to Physical Envelope [0.0..100.0%] *)
IF rSeptumV1_Demand_Unclamped > 100.0 THEN rSeptumV1_Demand_Unclamped := 100.0; END_IF;
IF rSeptumV1_Demand_Unclamped < 0.0 THEN rSeptumV1_Demand_Unclamped := 0.0; END_IF;

IF rSeptumV2_Demand_Unclamped > 100.0 THEN rSeptumV2_Demand_Unclamped := 100.0; END_IF;
IF rSeptumV2_Demand_Unclamped < 0.0 THEN rSeptumV2_Demand_Unclamped := 0.0; END_IF;

IF rSeptumV3_Demand_Unclamped > 100.0 THEN rSeptumV3_Demand_Unclamped := 100.0; END_IF;
IF rSeptumV3_Demand_Unclamped < 0.0 THEN rSeptumV3_Demand_Unclamped := 0.0; END_IF;

IF rVSV_Demand_Unclamped > 100.0 THEN rVSV_Demand_Unclamped := 100.0; END_IF;
IF rVSV_Demand_Unclamped < 0.0 THEN rVSV_Demand_Unclamped := 0.0; END_IF;
"""
