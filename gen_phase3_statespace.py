# -*- coding: utf-8 -*-
"""
Generator module: Phase 3 Discrete State-Space Propagation
"""

def get_phase3_statespace():
    return """(* =========================================================================================== *)
(* PHASE 3: DISCRETE STATE-SPACE MODEL PROPAGATION (x[k+1] = A*x[k] + B*u[k])                   *)
(* =========================================================================================== *)
(* Map Physical Measurements to State Perturbation Vector x[k] relative to Setpoint *)
arrX_State[1] := rVoted_BrothTemp_degC - arrX_Ref[1];
arrX_State[2] := rVoted_DissolvedOxygen_pct - arrX_Ref[2];
arrX_State[3] := rVoted_LiquidBroth_pH - arrX_Ref[3];
arrX_State[4] := AI_Capacitance_VCD_x10e6_per_mL - arrX_Ref[4];
arrX_State[5] := AI_Raman_Glucose_g_per_L - arrX_Ref[5];
arrX_State[6] := AI_Raman_Lactate_g_per_L - arrX_Ref[6];
arrX_State[7] := rEst_TransmembranePressure_bar - arrX_Ref[7];
arrX_State[8] := rEst_CO2_EvolutionRate_CER_mmol_Lh - arrX_Ref[8];

(* Active Actuator Inputs u[k] *)
arrU_Cmd[1] := AO_Sparger_O2_FlowCmd_SLPM;
arrU_Cmd[2] := AO_Sparger_CO2_FlowCmd_SLPM;
arrU_Cmd[3] := AO_PerfusionFeedPump_SpeedCmd_RPM;
arrU_Cmd[4] := AO_PermeateHarvestPump_SpeedCmd_RPM;
arrU_Cmd[5] := AO_Jacket_ChilledWaterValve_pct;
arrU_Cmd[6] := AO_BaseDosingPump_RateCmd_mLph;

(* Calculate State Tracking Error e[k] *)
FOR nIdx_i := 1 TO 8 DO
    arrX_Err[nIdx_i] := arrX_State[nIdx_i];
END_FOR;

(* Term-by-Term State-Space Propagation: x[k+1] = A * x[k] + B * u[k] *)
FOR nIdx_i := 1 TO 8 DO
    rAccumulator := 0.0;
    (* State Transition Contribution: Sum_j (arrA[i, j] * arrX_State[j]) *)
    FOR nIdx_j := 1 TO 8 DO
        rAccumulator := rAccumulator + (arrA[nIdx_i, nIdx_j] * arrX_State[nIdx_j]);
    END_FOR;
    (* Actuator Coupling Contribution: Sum_m (arrB[i, m] * arrU_Cmd[m]) *)
    FOR nIdx_m := 1 TO 6 DO
        rAccumulator := rAccumulator + (arrB[nIdx_i, nIdx_m] * arrU_Cmd[nIdx_m]);
    END_FOR;
    arrX_Next[nIdx_i] := rAccumulator;
END_FOR;

(* Sensor Observation Output Prediction: y[k] = C * x[k] + D * u[k] *)
FOR nIdx_p := 1 TO 8 DO
    rAccumulator := 0.0;
    FOR nIdx_j := 1 TO 8 DO
        rAccumulator := rAccumulator + (arrC[nIdx_p, nIdx_j] * arrX_State[nIdx_j]);
    END_FOR;
    FOR nIdx_m := 1 TO 6 DO
        rAccumulator := rAccumulator + (arrD[nIdx_p, nIdx_m] * arrU_Cmd[nIdx_m]);
    END_FOR;
    arrY_Obs[nIdx_p] := rAccumulator;
END_FOR;
"""

print("get_phase3_statespace ready.")
