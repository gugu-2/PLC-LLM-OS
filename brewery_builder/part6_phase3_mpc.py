# brewery_builder/part6_phase3_mpc.py

def get_part6():
    return """(* ============================================================================================== *)
(* PHASE 3: RECEDING-HORIZON MPC OPTIMIZATION WITH UNROLLED PROJECTED GRADIENT DESCENT (PGD)      *)
(* ============================================================================================== *)

(* ---------------------------------------------------------------------------------------------- *)
(* STEP 3.1: SETPOINT TRAJECTORY SYNTHESIS BASED ON ACTIVE BREWHOUSE PRODUCTION STATE             *)
(* ---------------------------------------------------------------------------------------------- *)
CASE eState OF
    0: (* STATE_IDLE *)
        vecX_Setpoint[1] := 0.0;    (* Lauter DP Target [mbar] *)
        vecX_Setpoint[2] := 0.0;    (* Turbidity Target [EBC] *)
        vecX_Setpoint[3] := 0.0;    (* Runoff Flow Target [hL/h] *)
        vecX_Setpoint[4] := 20.0;   (* Kettle Temp Target [deg C] *)
        vecX_Setpoint[5] := 0.0;    (* Evaporation Rate Target [%/h] *)
        vecX_Setpoint[6] := 100.0;  (* DMS Target [ppb] *)
        vecU_Target[1] := 350.0;    (* Rake Parked High [mm] *)
        vecU_Target[2] := 0.0;      (* Rake Stopped [RPM] *)
        vecU_Target[3] := 0.0;      (* Runoff Closed [%] *)
        vecU_Target[4] := 0.0;      (* Steam Off [bar] *)
        vecU_Target[5] := 0.0;      (* Recirc Closed [%] *)

    1: (* STATE_PREFILL_FOUNDATION_WATER *)
        vecX_Setpoint[1] := 3.5;    (* Foundation water head [mbar] *)
        vecX_Setpoint[2] := 5.0;    (* Clear water turbidity [EBC] *)
        vecX_Setpoint[3] := 0.0;    (* Zero runoff [hL/h] *)
        vecX_Setpoint[4] := 78.0;   (* Foundation water temp [deg C] *)
        vecX_Setpoint[5] := 0.0;    (* No boil [%/h] *)
        vecX_Setpoint[6] := 0.0;    (* No DMS [ppb] *)
        vecU_Target[1] := 250.0;    (* Rakes mid-height [mm] *)
        vecU_Target[2] := 0.0;      (* Rakes stationary [RPM] *)
        vecU_Target[3] := 0.0;      (* Runoff valve shut [%] *)
        vecU_Target[4] := 0.0;      (* Steam closed [bar] *)
        vecU_Target[5] := 0.0;      (* Recirc shut [%] *)

    2: (* STATE_MASH_TRANSFER_INFLOW *)
        vecX_Setpoint[1] := 12.0;   (* Rising mash hydrostatic head [mbar] *)
        vecX_Setpoint[2] := 180.0;  (* High mash turbidity [EBC] *)
        vecX_Setpoint[3] := 0.0;    (* Runoff closed [hL/h] *)
        vecX_Setpoint[4] := 72.0;   (* Mash temperature [deg C] *)
        vecX_Setpoint[5] := 0.0;    (* No boil [%/h] *)
        vecX_Setpoint[6] := 150.0;  (* Raw mash DMS pool [ppb] *)
        vecU_Target[1] := 180.0;    (* Rakes positioned for mash leveling [mm] *)
        vecU_Target[2] := 0.8;      (* Gentle mash leveling speed [RPM] *)
        vecU_Target[3] := 0.0;      (* Runoff valve shut [%] *)
        vecU_Target[4] := 0.0;      (* Steam shut [bar] *)
        vecU_Target[5] := 0.0;      (* Recirc shut [%] *)

    3: (* STATE_REST_GRAIN_BED_SETTLING *)
        vecX_Setpoint[1] := 14.5;   (* Settled static bed pressure [mbar] *)
        vecX_Setpoint[2] := 120.0;  (* Settling fines [EBC] *)
        vecX_Setpoint[3] := 0.0;    (* Quiescent rest [hL/h] *)
        vecX_Setpoint[4] := 74.0;   (* Mash rest temp [deg C] *)
        vecX_Setpoint[5] := 0.0;    (* No boil [%/h] *)
        vecX_Setpoint[6] := 140.0;  (* DMS pool [ppb] *)
        vecU_Target[1] := 300.0;    (* Rakes raised above bed [mm] *)
        vecU_Target[2] := 0.0;      (* Rakes stopped [RPM] *)
        vecU_Target[3] := 0.0;      (* Runoff closed [%] *)
        vecU_Target[4] := 0.0;      (* Steam closed [bar] *)
        vecU_Target[5] := 0.0;      (* Recirc closed [%] *)

    4: (* STATE_VORLAUF_RECIRCULATION *)
        vecX_Setpoint[1] := 18.0;   (* Gentle Vorlauf suction DP [mbar] *)
        vecX_Setpoint[2] := fTargetWortTurbidity; (* Target clarity threshold <= 25 EBC *)
        vecX_Setpoint[3] := 95.0;   (* Moderate recirculation flow rate [hL/h] *)
        vecX_Setpoint[4] := 75.0;   (* Wort temperature [deg C] *)
        vecX_Setpoint[5] := 0.0;    (* No boil [%/h] *)
        vecX_Setpoint[6] := 130.0;  (* DMS precursor present [ppb] *)
        vecU_Target[1] := 220.0;    (* Rakes shallow skimming bed top [mm] *)
        vecU_Target[2] := 0.4;      (* Slowest rake smoothing speed [RPM] *)
        vecU_Target[3] := 35.0;     (* Runoff control valve throttled [%] *)
        vecU_Target[4] := 0.0;      (* Steam shut [bar] *)
        vecU_Target[5] := 100.0;    (* 100% Vorlauf recirculation loop [%] *)

    5: (* STATE_FIRST_WORT_RUNOFF_OPTIMIZATION *)
        vecX_Setpoint[1] := 28.0;   (* Maximum safe Darcy pressure gradient [mbar] *)
        vecX_Setpoint[2] := 18.0;   (* High clarity sweet wort [EBC] *)
        vecX_Setpoint[3] := 260.0;  (* High-throughput first wort runoff [hL/h] *)
        vecX_Setpoint[4] := 74.5;   (* First wort temperature [deg C] *)
        vecX_Setpoint[5] := 0.0;    (* Calandria preheat standby [%/h] *)
        vecX_Setpoint[6] := 115.0;  (* DMS precursor transferred to kettle [ppb] *)
        vecU_Target[1] := 85.0;     (* Deep cutting rake knives [mm] *)
        vecU_Target[2] := 1.8;      (* Active rake bed cutting [RPM] *)
        vecU_Target[3] := 72.0;     (* Open runoff valve to Kettle [%] *)
        vecU_Target[4] := 0.8;      (* Pre-heating calandria steam jacket [bar] *)
        vecU_Target[5] := 0.0;      (* Vorlauf loop fully closed [%] *)

    6: (* STATE_SPARGING_HOT_WATER_DISTRIBUTION *)
        vecX_Setpoint[1] := 30.0;   (* Controlled sparge differential pressure [mbar] *)
        vecX_Setpoint[2] := 14.0;   (* Excellent filtered clarity [EBC] *)
        vecX_Setpoint[3] := 240.0;  (* Balanced sparge runoff throughput [hL/h] *)
        vecX_Setpoint[4] := 77.5;   (* Sparging temperature [deg C] *)
        vecX_Setpoint[5] := 0.0;    (* Kettle receiving weak wort [%/h] *)
        vecX_Setpoint[6] := 95.0;   (* Diluting DMS pool [ppb] *)
        vecU_Target[1] := 65.0;     (* Rakes operating in lower bed strata [mm] *)
        vecU_Target[2] := 2.2;      (* Moderate rake speed to prevent channeling [RPM] *)
        vecU_Target[3] := 68.0;     (* Runoff valve throttled for sparge balance [%] *)
        vecU_Target[4] := 1.2;      (* Calandria maintained at warm idle [bar] *)
        vecU_Target[5] := 0.0;      (* Recirc valve closed [%] *)

    7: (* STATE_RAKE_DEEP_CUTTING_SEQUENCE *)
        vecX_Setpoint[1] := 16.0;   (* Relieved bed compaction setpoint [mbar] *)
        vecX_Setpoint[2] := 35.0;   (* Permissible temporary turbidity blip [EBC] *)
        vecX_Setpoint[3] := 180.0;  (* Reduced runoff flow during deep cutting [hL/h] *)
        vecX_Setpoint[4] := 76.0;   (* Temperature [deg C] *)
        vecX_Setpoint[5] := 0.0;    (* Evap [%/h] *)
        vecX_Setpoint[6] := 85.0;   (* DMS [ppb] *)
        vecU_Target[1] := 22.0;     (* Deep cut knives 22 mm above false bottom [mm] *)
        vecU_Target[2] := 3.8;      (* High-torque deep cutting rotation [RPM] *)
        vecU_Target[3] := 40.0;     (* Throttled runoff to assist bed decompression [%] *)
        vecU_Target[4] := 1.0;      (* Calandria warm [bar] *)
        vecU_Target[5] := 0.0;      (* Recirc closed [%] *)

    8: (* STATE_SWEET_WATER_RUNOFF_CUTOFF *)
        vecX_Setpoint[1] := 8.0;    (* Draining bed head [mbar] *)
        vecX_Setpoint[2] := 20.0;   (* Turbidity [EBC] *)
        vecX_Setpoint[3] := 60.0;   (* Weak wort cutoff tailing flow [hL/h] *)
        vecX_Setpoint[4] := 78.0;   (* Temp [deg C] *)
        vecX_Setpoint[5] := 0.0;    (* Evap [%/h] *)
        vecX_Setpoint[6] := 65.0;   (* DMS [ppb] *)
        vecU_Target[1] := 150.0;    (* Raising rakes [mm] *)
        vecU_Target[2] := 1.0;      (* Slow rotation [RPM] *)
        vecU_Target[3] := 15.0;     (* Runoff shutting down [%] *)
        vecU_Target[4] := 1.5;      (* Calandria pre-boil ramp [bar] *)
        vecU_Target[5] := 0.0;      (* Recirc closed [%] *)

    9: (* STATE_SPENT_GRAIN_EVACUATION *)
        vecX_Setpoint[1] := 0.0;    (* Empty lauter bed [mbar] *)
        vecX_Setpoint[2] := 0.0;    (* Turbidity [EBC] *)
        vecX_Setpoint[3] := 0.0;    (* Runoff flow zero [hL/h] *)
        vecX_Setpoint[4] := 65.0;   (* Cooling bed [deg C] *)
        vecX_Setpoint[5] := 0.0;    (* Evap [%/h] *)
        vecX_Setpoint[6] := 45.0;   (* DMS [ppb] *)
        vecU_Target[1] := 18.0;     (* Discharge plow elevation [mm] *)
        vecU_Target[2] := 4.2;      (* Evacuation discharge plow speed [RPM] *)
        vecU_Target[3] := 0.0;      (* Runoff valve shut [%] *)
        vecU_Target[4] := 2.0;      (* Kettle boiling prep [bar] *)
        vecU_Target[5] := 0.0;      (* Recirc valve shut [%] *)

    10: (* STATE_KETTLE_HEATING_CALANDRIA *)
        vecX_Setpoint[1] := 0.0;    (* Lauter empty [mbar] *)
        vecX_Setpoint[2] := 0.0;    (* Turbidity [EBC] *)
        vecX_Setpoint[3] := 0.0;    (* Runoff zero [hL/h] *)
        vecX_Setpoint[4] := 99.5;   (* Ramp kettle to boiling threshold [deg C] *)
        vecX_Setpoint[5] := 1.2;    (* Incipient boiling simmer [%/h] *)
        vecX_Setpoint[6] := 75.0;   (* Thermal cleavage initiating [ppb] *)
        vecU_Target[1] := 380.0;    (* Rakes parked high [mm] *)
        vecU_Target[2] := 0.0;      (* Rakes stopped [RPM] *)
        vecU_Target[3] := 0.0;      (* Runoff shut [%] *)
        vecU_Target[4] := 3.2;      (* High-pressure steam heating [bar] *)
        vecU_Target[5] := 0.0;      (* Recirc shut [%] *)

    11: (* STATE_VIGOROUS_BOIL_EVAPORATION *)
        vecX_Setpoint[1] := 0.0;    (* Lauter empty [mbar] *)
        vecX_Setpoint[2] := 0.0;    (* Turbidity [EBC] *)
        vecX_Setpoint[3] := 0.0;    (* Runoff zero [hL/h] *)
        vecX_Setpoint[4] := 101.8;  (* Elevated atmospheric vigorous boil [deg C] *)
        vecX_Setpoint[5] := fTargetBoilEvaporationRate; (* 6.5 %/h continuous evaporation *)
        vecX_Setpoint[6] := fTargetDMSConcentration;   (* Target residual DMS <= 28 ppb *)
        vecU_Target[1] := 380.0;    (* Rakes parked [mm] *)
        vecU_Target[2] := 0.0;      (* Rakes stopped [RPM] *)
        vecU_Target[3] := 0.0;      (* Runoff shut [%] *)
        vecU_Target[4] := 3.6;      (* Vigorous calandria steam supply [bar] *)
        vecU_Target[5] := 0.0;      (* Recirc shut [%] *)

    12: (* STATE_WHIRLPOOL_TANGENTIAL_INLET_REST *)
        vecX_Setpoint[1] := 0.0;    (* Lauter empty [mbar] *)
        vecX_Setpoint[2] := 0.0;    (* Turbidity [EBC] *)
        vecX_Setpoint[3] := 0.0;    (* Runoff zero [hL/h] *)
        vecX_Setpoint[4] := 95.0;   (* Whirlpool trub separation temp [deg C] *)
        vecX_Setpoint[5] := 0.0;    (* Flameout - zero evaporation [%/h] *)
        vecX_Setpoint[6] := 24.0;   (* Stripped DMS [ppb] *)
        vecU_Target[1] := 380.0;    (* Rakes parked [mm] *)
        vecU_Target[2] := 0.0;      (* Rakes stopped [RPM] *)
        vecU_Target[3] := 0.0;      (* Runoff shut [%] *)
        vecU_Target[4] := 0.0;      (* Steam fully shut [bar] *)
        vecU_Target[5] := 0.0;      (* Recirc shut [%] *)

    13: (* STATE_CIP_CAUSTIC_SANITIZATION *)
        vecX_Setpoint[1] := 0.0;    (* Lauter empty [mbar] *)
        vecX_Setpoint[2] := 0.0;    (* Turbidity [EBC] *)
        vecX_Setpoint[3] := 0.0;    (* Runoff zero [hL/h] *)
        vecX_Setpoint[4] := 82.0;   (* Hot caustic wash temperature [deg C] *)
        vecX_Setpoint[5] := 0.0;    (* Evap zero [%/h] *)
        vecX_Setpoint[6] := 0.0;    (* DMS zero [ppb] *)
        vecU_Target[1] := 200.0;    (* Rakes mid-height for spray coverage [mm] *)
        vecU_Target[2] := 1.2;      (* Rake rotation for CIP distribution [RPM] *)
        vecU_Target[3] := 0.0;      (* Runoff shut [%] *)
        vecU_Target[4] := 1.5;      (* Calandria heat for caustic loop [bar] *)
        vecU_Target[5] := 0.0;      (* Recirc shut [%] *)
ELSE
    (* Fallback default safe setpoints *)
    FOR idxRow := 1 TO 6 DO
        vecX_Setpoint[idxRow] := vecX_hat[idxRow];
    END_FOR;
    FOR idxInput := 1 TO 5 DO
        vecU_Target[idxInput] := vecU_MinBox[idxInput];
    END_FOR;
END_CASE;

(* ---------------------------------------------------------------------------------------------- *)
(* STEP 3.2: INITIALIZE RECEDING-HORIZON TRAJECTORIES FOR UNROLLED OPTIMIZATION                   *)
(* ---------------------------------------------------------------------------------------------- *)
(* Horizon Step 0 Initial Condition: Current Estimated State x_hat[k] *)
FOR idxRow := 1 TO 6 DO
    arrX_Trajectory[0, idxRow] := vecX_hat[idxRow];
END_FOR;

(* Warm-Start Initial Control Trajectory with Previous Solution *)
FOR idxHorizon := 0 TO 3 DO
    FOR idxInput := 1 TO 5 DO
        arrU_Trajectory[idxHorizon, idxInput] := arrU_Trajectory_Best[idxHorizon + 1, idxInput];
    END_FOR;
END_FOR;
FOR idxInput := 1 TO 5 DO
    arrU_Trajectory[4, idxInput] := vecU_Target[idxInput];
END_FOR;

(* ---------------------------------------------------------------------------------------------- *)
(* STEP 3.3: 10 UNROLLED ITERATIONS OF PROJECTED GRADIENT DESCENT (PGD)                           *)
(* ---------------------------------------------------------------------------------------------- *)
FOR idxIter := 1 TO iMPC_MaxIter DO

    (* --- Sub-Step A: Forward State Trajectory Rollout x[k+1] = A * x[k] + B * u[k] --- *)
    FOR idxHorizon := 0 TO 4 DO
        FOR idxRow := 1 TO 6 DO
            fTempSum := 0.0;
            (* Dynamics Matrix Multiplications: A * x *)
            FOR idxCol := 1 TO 6 DO
                fTempSum := fTempSum + (matA[idxRow, idxCol] * arrX_Trajectory[idxHorizon, idxCol]);
            END_FOR;
            (* Input Coupling Matrix Multiplications: B * u *)
            FOR idxInput := 1 TO 5 DO
                fTempSum := fTempSum + (matB[idxRow, idxInput] * arrU_Trajectory[idxHorizon, idxInput]);
            END_FOR;
            arrX_Trajectory[idxHorizon + 1, idxRow] := fTempSum;
        END_FOR;
    END_FOR;

    (* --- Sub-Step B: Evaluate Quadratic Objective Cost J --- *)
    fCost_J_Current := 0.0;
    (* Running Stage Costs across Horizon Steps 0 to 4 *)
    FOR idxHorizon := 0 TO 4 DO
        (* State Error Quadratic Penalty: (x - x_sp)^T * Q * (x - x_sp) *)
        FOR idxRow := 1 TO 6 DO
            fTempStateError := arrX_Trajectory[idxHorizon, idxRow] - vecX_Setpoint[idxRow];
            fCost_J_Current := fCost_J_Current + (diagQ_StateCost[idxRow] * fTempStateError * fTempStateError);
        END_FOR;
        (* Actuator Effort Quadratic Penalty: (u - u_target)^T * R * (u - u_target) *)
        FOR idxInput := 1 TO 5 DO
            fTempControlError := arrU_Trajectory[idxHorizon, idxInput] - vecU_Target[idxInput];
            fCost_J_Current := fCost_J_Current + (diagR_ControlCost[idxInput] * fTempControlError * fTempControlError);
        END_FOR;
        (* Actuator Rate-of-Change Slew Penalty: Delta_u^T * R_slew * Delta_u *)
        FOR idxInput := 1 TO 5 DO
            IF idxHorizon = 0 THEN
                fTempDeltaControl := arrU_Trajectory[0, idxInput] - vecU_active_prev[idxInput];
            ELSE
                fTempDeltaControl := arrU_Trajectory[idxHorizon, idxInput] - arrU_Trajectory[idxHorizon - 1, idxInput];
            END_IF;
            fCost_J_Current := fCost_J_Current + (diagR_SlewCost[idxInput] * fTempDeltaControl * fTempDeltaControl);
        END_FOR;
    END_FOR;

    (* Terminal State Quadratic Penalty at Horizon Step 5: (x_N - x_sp)^T * P * (x_N - x_sp) *)
    FOR idxRow := 1 TO 6 DO
        fTempStateError := arrX_Trajectory[5, idxRow] - vecX_Setpoint[idxRow];
        fCost_J_Current := fCost_J_Current + (diagP_TerminalCost[idxRow] * fTempStateError * fTempStateError);
    END_FOR;

    (* Latch Best Solution Discovered along Iterations *)
    IF (idxIter = 1) OR (fCost_J_Current < fCost_J_Best) THEN
        fCost_J_Best := fCost_J_Current;
        FOR idxHorizon := 0 TO 4 DO
            FOR idxInput := 1 TO 5 DO
                arrU_Trajectory_Best[idxHorizon, idxInput] := arrU_Trajectory[idxHorizon, idxInput];
            END_FOR;
        END_FOR;
    END_IF;

    (* --- Sub-Step C: Backward Costate Adjoint Propagation --- *)
    (* Terminal Costate at Step 5: lambda[5] = 2 * P * (x[5] - x_sp) *)
    FOR idxRow := 1 TO 6 DO
        arrLambda_Costate[5, idxRow] := 2.0 * diagP_TerminalCost[idxRow] *
                                        (arrX_Trajectory[5, idxRow] - vecX_Setpoint[idxRow]);
    END_FOR;

    (* Backward Rollout: lambda[k] = 2 * Q * (x[k] - x_sp) + A^T * lambda[k+1] *)
    FOR idxHorizon := 4 TO 0 BY -1 DO
        FOR idxRow := 1 TO 6 DO
            fTempSum := 2.0 * diagQ_StateCost[idxRow] * (arrX_Trajectory[idxHorizon, idxRow] - vecX_Setpoint[idxRow]);
            (* Transpose Matrix Vector Multiplication: A^T * lambda[k+1] *)
            FOR idxCol := 1 TO 6 DO
                fTempSum := fTempSum + (matA[idxCol, idxRow] * arrLambda_Costate[idxHorizon + 1, idxCol]);
            END_FOR;
            arrLambda_Costate[idxHorizon, idxRow] := fTempSum;
        END_FOR;
    END_FOR;

    (* --- Sub-Step D: Gradient Synthesis & Projected Descent Update --- *)
    (* Gradient dJ/du[k] = 2 * R * (u[k] - u_target) + 2 * R_slew * Delta_u + B^T * lambda[k+1] *)
    FOR idxHorizon := 0 TO 4 DO
        FOR idxInput := 1 TO 5 DO
            (* Actuator Penalty Gradient *)
            fTempSum := 2.0 * diagR_ControlCost[idxInput] *
                        (arrU_Trajectory[idxHorizon, idxInput] - vecU_Target[idxInput]);

            (* Slew Rate Penalty Gradient *)
            IF idxHorizon = 0 THEN
                fTempDeltaControl := arrU_Trajectory[0, idxInput] - vecU_active_prev[idxInput];
            ELSE
                fTempDeltaControl := arrU_Trajectory[idxHorizon, idxInput] - arrU_Trajectory[idxHorizon - 1, idxInput];
            END_IF;
            fTempSum := fTempSum + (2.0 * diagR_SlewCost[idxInput] * fTempDeltaControl);

            (* Input Coupling Adjoint Gradient: B^T * lambda[k+1] *)
            FOR idxRow := 1 TO 6 DO
                fTempSum := fTempSum + (matB[idxRow, idxInput] * arrLambda_Costate[idxHorizon + 1, idxRow]);
            END_FOR;
            arrGrad_J[idxHorizon, idxInput] := fTempSum;

            (* Gradient Descent Update Step: u_cand = u - alpha * grad_J *)
            fCandidateU := arrU_Trajectory[idxHorizon, idxInput] - (fMPC_StepSizeAlpha * arrGrad_J[idxHorizon, idxInput]);

            (* Hard Physical Actuator Box Constraints Projection *)
            IF fCandidateU < vecU_MinBox[idxInput] THEN
                fCandidateU := vecU_MinBox[idxInput];
            ELSIF fCandidateU > vecU_MaxBox[idxInput] THEN
                fCandidateU := vecU_MaxBox[idxInput];
            END_IF;

            (* Actuator Maximum Slew Rate Enforcement *)
            IF idxHorizon = 0 THEN
                IF (fCandidateU - vecU_active_prev[idxInput]) > vecU_SlewLimit[idxInput] THEN
                    fCandidateU := vecU_active_prev[idxInput] + vecU_SlewLimit[idxInput];
                ELSIF (vecU_active_prev[idxInput] - fCandidateU) > vecU_SlewLimit[idxInput] THEN
                    fCandidateU := vecU_active_prev[idxInput] - vecU_SlewLimit[idxInput];
                END_IF;
            ELSE
                IF (fCandidateU - arrU_Trajectory[idxHorizon - 1, idxInput]) > vecU_SlewLimit[idxInput] THEN
                    fCandidateU := arrU_Trajectory[idxHorizon - 1, idxInput] + vecU_SlewLimit[idxInput];
                ELSIF (arrU_Trajectory[idxHorizon - 1, idxInput] - fCandidateU) > vecU_SlewLimit[idxInput] THEN
                    fCandidateU := arrU_Trajectory[idxHorizon - 1, idxInput] - vecU_SlewLimit[idxInput];
                END_IF;
            END_IF;

            arrU_Trajectory[idxHorizon, idxInput] := fCandidateU;
        END_FOR;
    END_FOR;

END_FOR;

(* ---------------------------------------------------------------------------------------------- *)
(* STEP 3.4: EXTRACT RECEDING-HORIZON OPTIMAL CONTROL ACTION u*[k]                                 *)
(* ---------------------------------------------------------------------------------------------- *)
FOR idxInput := 1 TO 5 DO
    vecU_active_prev[idxInput] := vecU_active[idxInput];
    vecU_active[idxInput] := arrU_Trajectory_Best[0, idxInput];
END_FOR;
"""
