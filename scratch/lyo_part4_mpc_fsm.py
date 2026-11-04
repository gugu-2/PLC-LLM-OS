# Module 4: Phase 4 (State-Space Model), Phase 5 (MPC Controller), Phase 6 (12-Stage FSM)
def get_part4():
    return '''(* ==========================================================================================
 * PHASE 4: DISCRETE STATE-SPACE PREDICTION & LUENBERGER OBSERVER UPDATE
 * ========================================================================================== *)
(* Update Sensor Measurement Vector from 2oo3 Voted & Process Analogs *)
y_meas[1] := rTMR4_VotedVal;                  (* Silicone oil supply temperature [deg C] *)
y_meas[2] := rTemp_OilReturn_degC;            (* Silicone oil return collector [deg C] *)
y_meas[3] := rCond_IceThickness_mm;           (* Condenser surface ice thickness [mm] *)
y_meas[4] := rTMR5_VotedVal - rTMR2_VotedVal; (* Differential Pirani - Baratron [mbar] *)
y_meas[5] := rPikal_SublimationVelocity_mm_h; (* Sublimation front recession velocity [mm/h] *)
y_meas[6] := rTMR1_VotedVal;                  (* Product vial core temperature [deg C] *)
y_meas[7] := rFlow_N2Bleed_sccm;              (* Nitrogen bleed mass flow rate [sccm] *)
y_meas[8] := rTMR6_VotedVal;                  (* Hydraulic stoppering cylinder pressure [bar] *)

(* Step 1: Model Output Estimation y_est[k] = C * x[k] *)
FOR iLoopI := 1 TO 8 DO
    rTempSum := 0.0;
    FOR iLoopJ := 1 TO 8 DO
        rTempSum := rTempSum + (matC[iLoopI, iLoopJ] * x_state[iLoopJ]);
    END_FOR;
    y_est[iLoopI] := rTempSum;
    (* Innovation Tracking Error *)
    x_err[iLoopI] := y_meas[iLoopI] - y_est[iLoopI];
END_FOR;

(* Step 2: Luenberger State Correction x_corr[k] = x_state[k] + K * (y_meas - y_est) *)
FOR iLoopI := 1 TO 8 DO
    x_state[iLoopI] := x_state[iLoopI] + (rKalmanGain[iLoopI] * x_err[iLoopI]);
END_FOR;

(* Step 3: State Propagation x[k+1] = A * x[k] + B * u[k] *)
FOR iLoopI := 1 TO 8 DO
    rTempSum := 0.0;
    (* State Transition Dynamics *)
    FOR iLoopJ := 1 TO 8 DO
        rTempSum := rTempSum + (matA[iLoopI, iLoopJ] * x_state[iLoopJ]);
    END_FOR;
    (* Control Input Coupling *)
    FOR iLoopK := 1 TO 6 DO
        rTempSum := rTempSum + (matB[iLoopI, iLoopK] * u_ctrl[iLoopK]);
    END_FOR;
    x_pred[iLoopI] := rTempSum;
END_FOR;

(* Store Historical State Vector *)
FOR iLoopI := 1 TO 8 DO
    x_prev[iLoopI] := x_state[iLoopI];
    x_state[iLoopI] := x_pred[iLoopI];
END_FOR;


(* ==========================================================================================
 * PHASE 5: RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) OPTIMIZATION
 * ========================================================================================== *)
(* Establish Dynamic Target Reference Vector x_ref based on Active Recipe Setpoints *)
CASE iState OF
    1: (* IDLE_STERILE_HOLD *)
        x_ref[1] := 20.0;                              (* Ambient shelf temp [deg C] *)
        x_ref[2] := 20.0;
        x_ref[3] := 0.0;                               (* Clean condenser *)
        x_ref[4] := 0.0;
        x_ref[5] := 0.0;
        x_ref[6] := 20.0;
        x_ref[7] := 0.0;
        x_ref[8] := 0.0;
    2: (* VIAL_LOADING_CHILLED_HOLD *)
        x_ref[1] := 4.0;                               (* Pre-chill shelves to +4.0 deg C *)
        x_ref[2] := 4.0;
        x_ref[3] := 0.0;
        x_ref[4] := 0.0;
        x_ref[5] := 0.0;
        x_ref[6] := 4.0;
        x_ref[7] := 0.0;
        x_ref[8] := 0.0;
    3: (* ATMOSPHERIC_FREEZING *)
        x_ref[1] := rRecipe_ShelfTemp_Freezing_degC;   (* Ramp to -45.0 deg C *)
        x_ref[2] := rRecipe_ShelfTemp_Freezing_degC;
        x_ref[3] := 0.0;
        x_ref[4] := 0.0;
        x_ref[5] := 0.0;
        x_ref[6] := rRecipe_ShelfTemp_Freezing_degC;
        x_ref[7] := 0.0;
        x_ref[8] := 0.0;
    4: (* ANNEALING_CRYSTALLIZATION *)
        x_ref[1] := -20.0;                             (* Annealing plateau at -20.0 deg C *)
        x_ref[2] := -20.0;
        x_ref[3] := 0.0;
        x_ref[4] := 0.0;
        x_ref[5] := 0.0;
        x_ref[6] := -20.0;
        x_ref[7] := 0.0;
        x_ref[8] := 0.0;
    5: (* DEEP_EVACUATION *)
        x_ref[1] := rRecipe_ShelfTemp_Freezing_degC;   (* Maintain frozen shelves *)
        x_ref[2] := rRecipe_ShelfTemp_Freezing_degC;
        x_ref[3] := 0.5;
        x_ref[4] := 0.005;
        x_ref[5] := 0.05;
        x_ref[6] := rRecipe_ShelfTemp_Freezing_degC;
        x_ref[7] := 0.0;
        x_ref[8] := 0.0;
    6: (* PRIMARY_SUBLIMATION *)
        x_ref[1] := rRecipe_ShelfTemp_Primary_degC;    (* Sublimation shelf temp (e.g. -15.0 deg C) *)
        x_ref[2] := rRecipe_ShelfTemp_Primary_degC - 1.5;
        x_ref[3] := 15.0;                              (* Ice growth on condenser *)
        x_ref[4] := 0.080;                             (* Pirani - Baratron differential *)
        x_ref[5] := 1.25;                              (* Active drying velocity 1.25 mm/h *)
        x_ref[6] := rRecipe_ShelfTemp_Primary_degC - 4.0;
        x_ref[7] := 85.0;                              (* N2 bleed flow [sccm] *)
        x_ref[8] := 0.0;
    7: (* COMPARATIVE_ENDPOINT_VERIFY *)
        x_ref[1] := rRecipe_ShelfTemp_Primary_degC;
        x_ref[2] := rRecipe_ShelfTemp_Primary_degC - 0.5;
        x_ref[3] := 25.0;
        x_ref[4] := 0.005;                             (* Pressure diff converges to 0 *)
        x_ref[5] := 0.05;                              (* Sublimation velocity drops to 0 *)
        x_ref[6] := rRecipe_ShelfTemp_Primary_degC - 1.0;
        x_ref[7] := 40.0;
        x_ref[8] := 0.0;
    8: (* SECONDARY_DESORPTION *)
        x_ref[1] := rRecipe_ShelfTemp_Secondary_degC;  (* Desorption shelf temp (+35.0 deg C) *)
        x_ref[2] := rRecipe_ShelfTemp_Secondary_degC - 0.5;
        x_ref[3] := 26.0;
        x_ref[4] := 0.001;
        x_ref[5] := 0.0;
        x_ref[6] := rRecipe_ShelfTemp_Secondary_degC - 0.2;
        x_ref[7] := 0.0;                               (* Pure vacuum, no bleed *)
        x_ref[8] := 0.0;
    9: (* HYDRAULIC_STOPPERING *)
        x_ref[1] := 20.0;
        x_ref[2] := 20.0;
        x_ref[3] := 26.0;
        x_ref[4] := 0.0;
        x_ref[5] := 0.0;
        x_ref[6] := 20.0;
        x_ref[7] := 0.0;
        x_ref[8] := (rRecipe_StopperingForce_kN / (rHyd_PistonArea_cm2 * 0.010)); (* Target Stoppering Bar *)
    10: (* CHAMBER_AERATION *)
        x_ref[1] := 20.0;
        x_ref[2] := 20.0;
        x_ref[3] := 26.0;
        x_ref[4] := 0.0;
        x_ref[5] := 0.0;
        x_ref[6] := 20.0;
        x_ref[7] := 250.0;
        x_ref[8] := 0.0;
    11: (* PRODUCT_UNLOADING *)
        x_ref[1] := 20.0;
        x_ref[2] := 20.0;
        x_ref[3] := 0.0;
        x_ref[4] := 0.0;
        x_ref[5] := 0.0;
        x_ref[6] := 20.0;
        x_ref[7] := 0.0;
        x_ref[8] := 0.0;
    12: (* CIP_SIP_STERILIZATION *)
        x_ref[1] := 121.1;                             (* Steam sterilization plateau *)
        x_ref[2] := 121.1;
        x_ref[3] := 0.0;
        x_ref[4] := 0.0;
        x_ref[5] := 0.0;
        x_ref[6] := 121.1;
        x_ref[7] := 0.0;
        x_ref[8] := 0.0;
ELSE
    FOR iLoopI := 1 TO 8 DO
        x_ref[iLoopI] := x_state[iLoopI];
    END_FOR;
END_CASE;

(* MPC Quadratic Cost Optimization via Projected Gradient Descent *)
(* J(u) = (x_pred - x_ref)^T * Q * (x_pred - x_ref) + u^T * R * u + (x_pred - x_ref)^T * P * (x_pred - x_ref) *)
(* Gradient dJ/du_k = 2 * R_k * u_k + 2 * sum_i( B[i,k] * (Q[i,i] + P[i,i]) * (x_pred[i] - x_ref[i]) ) *)
FOR iLoopK := 1 TO 6 DO
    rTempSum := 2.0 * matR[iLoopK, iLoopK] * u_ctrl[iLoopK];
    FOR iLoopI := 1 TO 8 DO
        rTempSum := rTempSum + (2.0 * matB[iLoopI, iLoopK] * (matQ[iLoopI, iLoopI] + matP[iLoopI, iLoopI]) * (x_pred[iLoopI] - x_ref[iLoopI]));
    END_FOR;
    rMpcGradient[iLoopK] := rTempSum;
    
    (* Projected Gradient Update Step with Learning Rate rMpcStepSize *)
    u_ctrl[iLoopK] := u_ctrl[iLoopK] - (rMpcStepSize * rMpcGradient[iLoopK]);
    
    (* Actuator Hard Saturation Constraint Bounding *)
    IF u_ctrl[iLoopK] < u_min[iLoopK] THEN
        u_ctrl[iLoopK] := u_min[iLoopK];
    ELSIF u_ctrl[iLoopK] > u_max[iLoopK] THEN
        u_ctrl[iLoopK] := u_max[iLoopK];
    END_IF;
    
    (* Actuator Delta Slew Rate Computation *)
    u_delta[iLoopK] := (u_ctrl[iLoopK] - u_prev[iLoopK]) / rDeltaTime_s;
    u_prev[iLoopK] := u_ctrl[iLoopK];
END_FOR;


(* ==========================================================================================
 * PHASE 6: 12-STAGE DETERMINISTIC FINITE STATE MACHINE (FSM)
 * ========================================================================================== *)
tStateTimer_s      := tStateTimer_s + rDeltaTime_s;
tTotalBatchTimer_s := tTotalBatchTimer_s + rDeltaTime_s;

CASE iState OF

    (* --------------------------------------------------------------------------------------
     * STAGE 1: IDLE / STERILE HOLD
     * -------------------------------------------------------------------------------------- *)
    1:
        sCurrentStateName := 'IDLE_STERILE_HOLD';
        rPhaseProgress_pct := 0.0;
        
        (* Safe Quiescent Actuator State *)
        rCmd_ShelfHeater_SCR_pct    := 0.0;
        rCmd_ShelfCooling_Valve_pct := 0.0;
        rCmd_N2MicroBleed_Piezo_pct := 0.0;
        rCmd_VacuumButterfly_pct    := 0.0;
        rCmd_RefrigCap_Comp1_pct    := 0.0;
        rCmd_RefrigCap_Comp2_pct    := 0.0;
        rCmd_HotGasDefrost_pct      := 0.0;
        rCmd_HydraulicPressure_bar  := 0.0;
        rCmd_HydraulicSpeed_mms     := 0.0;
        rCmd_SiliconePumpVFD_pct    := 20.0; (* Gentle trickle recirculation *)

        bCmd_IsolationValve_Close := TRUE;
        bCmd_IsolationValve_Open  := FALSE;
        bCmd_VacuumPump1_Start    := FALSE;
        bCmd_VacuumPump2_Start    := FALSE;
        bCmd_RootsBlower_Start    := FALSE;
        bCmd_PureSteam_Valve_Open := FALSE;
        bCmd_CondensateDrain_Open := FALSE;
        bCmd_CIP_SupplyPump_Start := FALSE;
        bCmd_N2_SterileVent_Open  := FALSE;
        bCmd_HydraulicDump_SlamOpen := FALSE;

        bReadyForLoading := TRUE;
        bCycleComplete   := FALSE;

        (* Transition to Vial Loading on Start Command & Door Permissive *)
        IF bAutoMode AND bStartCycle AND bDoorClosed_Locked AND bInflatableSeal_Pressurized THEN
            iPrevState := iState;
            iState := 2; (* LYO_STATE_VIAL_LOADING_CHILLED_HOLD *)
            tStateTimer_s := 0.0;
            bStateFirstScan := TRUE;
            bReadyForLoading := FALSE;
        END_IF;

    (* --------------------------------------------------------------------------------------
     * STAGE 2: VIAL LOADING / CHILLED SHELF HOLD (+4.0 deg C)
     * -------------------------------------------------------------------------------------- *)
    2:
        sCurrentStateName := 'VIAL_LOADING_CHILLED_HOLD';
        
        IF bStateFirstScan THEN
            bCmd_OilPump1_Start := TRUE;
            bCmd_OilPump2_Start := FALSE; (* Standby *)
            bStateFirstScan := FALSE;
        END_IF;

        rCmd_SiliconePumpVFD_pct := 75.0; (* Full turbulent oil flow for uniformity *)
        
        (* Maintain Shelves at +4.0 deg C to preserve formulation stability during loading *)
        IF rTMR4_VotedVal > 4.5 THEN
            rCmd_ShelfHeater_SCR_pct    := 0.0;
            rCmd_ShelfCooling_Valve_pct := 35.0;
        ELSIF rTMR4_VotedVal < 3.5 THEN
            rCmd_ShelfHeater_SCR_pct    := 25.0;
            rCmd_ShelfCooling_Valve_pct := 0.0;
        ELSE
            rCmd_ShelfHeater_SCR_pct    := 5.0;
            rCmd_ShelfCooling_Valve_pct := 5.0;
        END_IF;

        rPhaseProgress_pct := MIN(100.0, (tStateTimer_s / 3600.0) * 100.0);

        (* Transition to Freezing when Loading Completed and Transfer Permissive Revoked *)
        IF (tStateTimer_s >= 600.0) AND bDoorClosed_Locked AND bInflatableSeal_Pressurized AND NOT bTransferPermissive THEN
            iPrevState := iState;
            iState := 3; (* LYO_STATE_ATMOSPHERIC_FREEZING *)
            tStateTimer_s := 0.0;
            bStateFirstScan := TRUE;
        END_IF;

    (* --------------------------------------------------------------------------------------
     * STAGE 3: ATMOSPHERIC FREEZING (-45.0 deg C)
     * -------------------------------------------------------------------------------------- *)
    3:
        sCurrentStateName := 'ATMOSPHERIC_FREEZING';

        IF bStateFirstScan THEN
            bCmd_RefrigComp1_Start := TRUE; (* Start cascade high-stage *)
            bStateFirstScan := FALSE;
        END_IF;

        rCmd_SiliconePumpVFD_pct    := 100.0;
        rCmd_ShelfHeater_SCR_pct    := 0.0;
        rCmd_ShelfCooling_Valve_pct := 95.0; (* Full brine chiller circulation *)
        rCmd_RefrigCap_Comp1_pct    := 80.0;

        (* Track Freezing Progress: Ramp Down to -45.0 deg C + 120 min Solidification Soak *)
        IF rTMR1_VotedVal <= (rRecipe_ShelfTemp_Freezing_degC + 1.0) THEN
            rPhaseProgress_pct := 70.0 + MIN(30.0, (tStateTimer_s / 7200.0) * 30.0);
            (* Once soaked at -45.0 deg C for 2 hours (7200 s) *)
            IF tStateTimer_s >= 7200.0 THEN
                iPrevState := iState;
                iState := 4; (* LYO_STATE_ANNEALING_CRYSTALLIZATION *)
                tStateTimer_s := 0.0;
                bStateFirstScan := TRUE;
            END_IF;
        ELSE
            rPhaseProgress_pct := MIN(70.0, ABS((rTMR1_VotedVal - 4.0) / (rRecipe_ShelfTemp_Freezing_degC - 4.0)) * 70.0);
        END_IF;

    (* --------------------------------------------------------------------------------------
     * STAGE 4: ANNEALING / OSTWALD RIPENING STEP (-20.0 deg C)
     * -------------------------------------------------------------------------------------- *)
    4:
        sCurrentStateName := 'ANNEALING_CRYSTALLIZATION';

        (* Warm up to -20.0 deg C to enlarge ice crystal pore diameter and reduce dry cake resistance *)
        IF rTMR4_VotedVal < -20.5 THEN
            rCmd_ShelfHeater_SCR_pct    := 45.0;
            rCmd_ShelfCooling_Valve_pct := 0.0;
        ELSIF rTMR4_VotedVal > -19.5 THEN
            rCmd_ShelfHeater_SCR_pct    := 0.0;
            rCmd_ShelfCooling_Valve_pct := 30.0;
        ELSE
            rCmd_ShelfHeater_SCR_pct    := 10.0;
            rCmd_ShelfCooling_Valve_pct := 10.0;
        END_IF;

        (* Dwell at -20.0 deg C for 7200 s, then re-chill back to -45.0 deg C *)
        IF tStateTimer_s >= 7200.0 THEN
            (* Re-chill phase *)
            rCmd_ShelfHeater_SCR_pct    := 0.0;
            rCmd_ShelfCooling_Valve_pct := 90.0;
            IF (rTMR1_VotedVal <= (rRecipe_ShelfTemp_Freezing_degC + 1.5)) AND (tStateTimer_s >= 10800.0) THEN
                iPrevState := iState;
                iState := 5; (* LYO_STATE_DEEP_EVACUATION *)
                tStateTimer_s := 0.0;
                bStateFirstScan := TRUE;
            END_IF;
        END_IF;
        rPhaseProgress_pct := MIN(100.0, (tStateTimer_s / 10800.0) * 100.0);

    (* --------------------------------------------------------------------------------------
     * STAGE 5: DEEP EVACUATION (< 0.080 mbar)
     * -------------------------------------------------------------------------------------- *)
    5:
        sCurrentStateName := 'DEEP_EVACUATION';

        IF bStateFirstScan THEN
            (* Chill condenser coil to -80.0 deg C prior to opening isolation valve *)
            bCmd_RefrigComp1_Start := TRUE;
            bCmd_RefrigComp2_Start := TRUE; (* Low-stage cascade *)
            bCmd_VacuumPump1_Start := TRUE;
            bCmd_VacuumPump2_Start := TRUE;
            bStateFirstScan := FALSE;
        END_IF;

        rCmd_RefrigCap_Comp1_pct := 100.0;
        rCmd_RefrigCap_Comp2_pct := 100.0;

        (* Keep shelves frozen *)
        rCmd_ShelfHeater_SCR_pct    := 0.0;
        rCmd_ShelfCooling_Valve_pct := 40.0;

        (* Once condenser surface <= -75.0 deg C, start Roots blower and open main butterfly *)
        IF rTemp_CondenserSurface_degC <= -75.0 THEN
            bCmd_RootsBlower_Start   := TRUE;
            bCmd_IsolationValve_Open := TRUE;
            bCmd_IsolationValve_Close:= FALSE;
            rCmd_VacuumButterfly_pct := 100.0;
        END_IF;

        (* Evacuate chamber down below 0.080 mbar *)
        IF (rTMR2_VotedVal <= 0.080) AND bIsolationValve_Open_LS AND (tStateTimer_s >= 1800.0) THEN
            iPrevState := iState;
            iState := 6; (* LYO_STATE_PRIMARY_SUBLIMATION *)
            tStateTimer_s := 0.0;
            bStateFirstScan := TRUE;
        END_IF;
        rPhaseProgress_pct := MIN(100.0, MAX(0.0, (1.0 - (rTMR2_VotedVal / 1.0)) * 100.0));

    (* --------------------------------------------------------------------------------------
     * STAGE 6: PRIMARY SUBLIMATION DRYING
     * -------------------------------------------------------------------------------------- *)
    6:
        sCurrentStateName := 'PRIMARY_SUBLIMATION';

        (* Active Heating to Primary Drying Temperature (e.g. -15.0 deg C) *)
        rCmd_SiliconePumpVFD_pct := 100.0;

        (* Cascaded Heating PID Output with Latent Heat Feedforward *)
        rFeedforward_LatentHeat_pct := (rObs_SublimationRate_kgh / 45.0) * 35.0; (* Compensate sublimative cooling *)
        
        rPID_Shelf_Error := rRecipe_ShelfTemp_Primary_degC - rTMR4_VotedVal;
        rPID_Shelf_Integral := rPID_Shelf_Integral + (rPID_Shelf_Error * rDeltaTime_s);
        IF rPID_Shelf_Integral > 1000.0 THEN rPID_Shelf_Integral := 1000.0; ELSIF rPID_Shelf_Integral < -1000.0 THEN rPID_Shelf_Integral := -1000.0; END_IF;
        rPID_Shelf_Derivative := (rPID_Shelf_Error - rPID_Shelf_PrevError) / rDeltaTime_s;
        rPID_Shelf_PrevError := rPID_Shelf_Error;
        
        rPID_Shelf_Output_pct := (rPID_Shelf_Kp * rPID_Shelf_Error) + (rPID_Shelf_Ki * rPID_Shelf_Integral) + (rPID_Shelf_Kd * rPID_Shelf_Derivative) + rFeedforward_LatentHeat_pct;
        
        IF rPID_Shelf_Output_pct >= 0.0 THEN
            rCmd_ShelfHeater_SCR_pct    := MIN(100.0, rPID_Shelf_Output_pct);
            rCmd_ShelfCooling_Valve_pct := 0.0;
        ELSE
            rCmd_ShelfHeater_SCR_pct    := 0.0;
            rCmd_ShelfCooling_Valve_pct := MIN(100.0, ABS(rPID_Shelf_Output_pct));
        END_IF;

        (* Controlled Nitrogen Micro-Bleed Vacuum Regulation (Set to Recipe, e.g. 0.120 mbar) *)
        rPID_Vac_Error := rRecipe_ChamberPress_Primary_mbar - rTMR2_VotedVal;
        rPID_Vac_Integral := rPID_Vac_Integral + (rPID_Vac_Error * rDeltaTime_s);
        IF rPID_Vac_Integral > 500.0 THEN rPID_Vac_Integral := 500.0; ELSIF rPID_Vac_Integral < -500.0 THEN rPID_Vac_Integral := -500.0; END_IF;
        rPID_Vac_Derivative := (rPID_Vac_Error - rPID_Vac_PrevError) / rDeltaTime_s;
        rPID_Vac_PrevError := rPID_Vac_Error;

        rPID_Vac_Output_pct := (rPID_Vac_Kp * rPID_Vac_Error) + (rPID_Vac_Ki * rPID_Vac_Integral) + (rPID_Vac_Kd * rPID_Vac_Derivative);
        rCmd_N2MicroBleed_Piezo_pct := MAX(0.0, MIN(100.0, rPID_Vac_Output_pct));
        rCmd_VacuumButterfly_pct    := 90.0; (* Fixed throttle for steady convective flow *)

        (* Progress based on sublimated ice mass *)
        rPhaseProgress_pct := MIN(95.0, (rPikal_CumulativeSublimated_kg / (rPikal_TotalIceMass_kg + 0.001)) * 100.0);

        (* Check for Primary Sublimation Breakthrough:
         * 1. Product Core RTDs approach shelf temperature (within 2.5 deg C).
         * 2. Comparative Pressure Ratio drops below 1.15. *)
        IF (rTMR1_VotedVal >= (rRecipe_ShelfTemp_Primary_degC - 2.5)) AND (rComp_FilteredRatio <= 1.15) AND (tStateTimer_s >= 28800.0) THEN
            iPrevState := iState;
            iState := 7; (* LYO_STATE_COMPARATIVE_ENDPOINT_VERIFY *)
            tStateTimer_s := 0.0;
            bStateFirstScan := TRUE;
        END_IF;

    (* --------------------------------------------------------------------------------------
     * STAGE 7: COMPARATIVE PRESSURE END-POINT VERIFICATION
     * -------------------------------------------------------------------------------------- *)
    7:
        sCurrentStateName := 'COMPARATIVE_ENDPOINT_VERIFY';

        (* Hold Primary Shelf Temperature *)
        rCmd_ShelfHeater_SCR_pct    := 22.0;
        rCmd_ShelfCooling_Valve_pct := 0.0;

        (* Maintain N2 bleed for comparative thermal conductivity observation *)
        rCmd_N2MicroBleed_Piezo_pct := 25.0;
        rCmd_VacuumButterfly_pct    := 90.0;

        rPhaseProgress_pct := 95.0 + MIN(5.0, (tComp_ConvergenceTimer_s / 1800.0) * 5.0);

        (* Verification Criteria: Pirani / Baratron Ratio <= 1.05 for 30 minutes continuous *)
        IF bComp_EndpointMet AND (rTMR1_VotedVal >= (rRecipe_ShelfTemp_Primary_degC - 1.2)) THEN
            bPrimaryDryingComplete := TRUE;
            iPrevState := iState;
            iState := 8; (* LYO_STATE_SECONDARY_DESORPTION *)
            tStateTimer_s := 0.0;
            bStateFirstScan := TRUE;
        END_IF;

    (* --------------------------------------------------------------------------------------
     * STAGE 8: SECONDARY DESORPTION DRYING (+35.0 deg C, DEEP VACUUM)
     * -------------------------------------------------------------------------------------- *)
    8:
        sCurrentStateName := 'SECONDARY_DESORPTION';

        (* Turn off N2 bleed to pull maximum ultimate vacuum (< 0.020 mbar) *)
        rCmd_N2MicroBleed_Piezo_pct := 0.0;
        rCmd_VacuumButterfly_pct    := 100.0;

        (* Thermal Ramp to +35.0 deg C at controlled rate *)
        IF rTMR4_VotedVal < (rRecipe_ShelfTemp_Secondary_degC - 0.5) THEN
            rCmd_ShelfHeater_SCR_pct    := 65.0;
            rCmd_ShelfCooling_Valve_pct := 0.0;
        ELSIF rTMR4_VotedVal > (rRecipe_ShelfTemp_Secondary_degC + 0.5) THEN
            rCmd_ShelfHeater_SCR_pct    := 0.0;
            rCmd_ShelfCooling_Valve_pct := 20.0;
        ELSE
            rCmd_ShelfHeater_SCR_pct    := 15.0;
            rCmd_ShelfCooling_Valve_pct := 0.0;
        END_IF;

        (* Dwell at +35.0 deg C for 18000 s (5 hours) to desorb bound monolayer water *)
        IF (tStateTimer_s >= 18000.0) AND (rTMR1_VotedVal >= (rRecipe_ShelfTemp_Secondary_degC - 1.0)) AND (rTMR2_VotedVal <= rRecipe_ChamberPress_Secondary_mbar) THEN
            bSecondaryDryingComplete := TRUE;
            iPrevState := iState;
            iState := 9; (* LYO_STATE_HYDRAULIC_STOPPERING *)
            tStateTimer_s := 0.0;
            bStateFirstScan := TRUE;
        END_IF;
        rPhaseProgress_pct := MIN(100.0, (tStateTimer_s / 18000.0) * 100.0);

    (* --------------------------------------------------------------------------------------
     * STAGE 9: HYDRAULIC VIAL STOPPERING (DYNAMIC TONNAGE RAMP)
     * -------------------------------------------------------------------------------------- *)
    9:
        sCurrentStateName := 'HYDRAULIC_STOPPERING';

        (* Cool shelves to ambient 20 deg C prior to stoppering *)
        rCmd_ShelfHeater_SCR_pct    := 0.0;
        rCmd_ShelfCooling_Valve_pct := 30.0;

        (* Dynamic Tonnage Ramp Profile: Advance Ram & Increase Hydraulic Pressure *)
        IF rHyd_CalculatedForce_kN < rRecipe_StopperingForce_kN THEN
            rCmd_HydraulicSpeed_mms    := 8.0; (* Controlled advance speed *)
            rCmd_HydraulicPressure_bar := MIN(220.0, (rRecipe_StopperingForce_kN / (rHyd_PistonArea_cm2 * 0.010)) * 1.05);
            bHyd_TargetTonnageReached  := FALSE;
        ELSE
            (* Peak Force Reached: Hold Dwell *)
            rCmd_HydraulicSpeed_mms    := 0.0;
            rCmd_HydraulicPressure_bar := (rRecipe_StopperingForce_kN / (rHyd_PistonArea_cm2 * 0.010));
            bHyd_TargetTonnageReached  := TRUE;
            tHyd_TonnageHoldTimer_s    := tHyd_TonnageHoldTimer_s + rDeltaTime_s;
        END_IF;

        (* Once held for recipe dwell time (e.g. 180 s) *)
        IF bHyd_TargetTonnageReached AND (tHyd_TonnageHoldTimer_s >= rRecipe_StopperingHoldTime_s) THEN
            bStopperingComplete := TRUE;
            iPrevState := iState;
            iState := 10; (* LYO_STATE_CHAMBER_AERATION *)
            tStateTimer_s := 0.0;
            bStateFirstScan := TRUE;
        END_IF;
        rPhaseProgress_pct := MIN(100.0, (tHyd_TonnageHoldTimer_s / (rRecipe_StopperingHoldTime_s + 0.1)) * 100.0);

    (* --------------------------------------------------------------------------------------
     * STAGE 10: CHAMBER AERATION (STERILE 0.2 um N2 VENT)
     * -------------------------------------------------------------------------------------- *)
    10:
        sCurrentStateName := 'CHAMBER_AERATION';

        (* Close Vacuum Isolation Valve & Stop Pumps *)
        bCmd_IsolationValve_Close := TRUE;
        bCmd_IsolationValve_Open  := FALSE;
        rCmd_VacuumButterfly_pct  := 0.0;
        bCmd_RootsBlower_Start    := FALSE;
        bCmd_VacuumPump1_Start    := FALSE;
        bCmd_VacuumPump2_Start    := FALSE;

        (* Open Sterile Nitrogen Filtered Vent Valve *)
        bCmd_N2_SterileVent_Open := TRUE;

        (* Depressurize Hydraulic Ram *)
        rCmd_HydraulicPressure_bar := 0.0;
        rCmd_HydraulicSpeed_mms    := 0.0;

        (* Vent until chamber reaches atmospheric pressure 1000 mbar *)
        IF rTMR2_VotedVal >= 980.0 THEN
            bCmd_N2_SterileVent_Open := FALSE;
            iPrevState := iState;
            iState := 11; (* LYO_STATE_PRODUCT_UNLOADING *)
            tStateTimer_s := 0.0;
            bStateFirstScan := TRUE;
        END_IF;
        rPhaseProgress_pct := MIN(100.0, (rTMR2_VotedVal / 1000.0) * 100.0);

    (* --------------------------------------------------------------------------------------
     * STAGE 11: PRODUCT UNLOADING & POST-BATCH DEFROST
     * -------------------------------------------------------------------------------------- *)
    11:
        sCurrentStateName := 'PRODUCT_UNLOADING';

        (* Retract Hydraulic Ram *)
        rCmd_HydraulicPressure_bar := 50.0;
        rCmd_HydraulicSpeed_mms    := -15.0; (* Retract *)

        (* Condenser Defrost: Fire Hot-Gas Bypass Valve *)
        rCmd_HotGasDefrost_pct := 85.0;
        bCmd_CondensateDrain_Open := TRUE;

        (* Permissive to open chamber door and unload stoppered vials *)
        bTransferPermissive := TRUE;

        (* Transition to CIP/SIP once unloaded and door re-locked *)
        IF (tStateTimer_s >= 3600.0) AND bDoorClosed_Locked AND (rCond_IceThickness_mm <= 0.2) THEN
            iPrevState := iState;
            iState := 12; (* LYO_STATE_CIP_SIP_STERILIZATION *)
            tStateTimer_s := 0.0;
            bStateFirstScan := TRUE;
            bTransferPermissive := FALSE;
        END_IF;
        rPhaseProgress_pct := MIN(100.0, (tStateTimer_s / 3600.0) * 100.0);

    (* --------------------------------------------------------------------------------------
     * STAGE 12: CLEAN-IN-PLACE (CIP) & STEAM-IN-PLACE (SIP) STERILIZATION
     * -------------------------------------------------------------------------------------- *)
    12:
        sCurrentStateName := 'CIP_SIP_STERILIZATION';

        rCmd_HotGasDefrost_pct := 0.0;

        (* Sub-phase A: CIP Water Spray (First 1200 s) *)
        IF tStateTimer_s < 1200.0 THEN
            bCmd_CIP_SupplyPump_Start := TRUE;
            bCmd_CondensateDrain_Open := TRUE;
            bCmd_PureSteam_Valve_Open := FALSE;
            rPhaseProgress_pct := (tStateTimer_s / 1200.0) * 25.0;
        ELSE
            (* Sub-phase B: Pure Steam Injection at 121.1 deg C & F0 Accumulation *)
            bCmd_CIP_SupplyPump_Start := FALSE;
            bCmd_PureSteam_Valve_Open := TRUE;
            bCmd_CondensateDrain_Open := TRUE; (* Controlled trap drainage *)

            (* Modulate Pure Steam to Maintain 121.5 deg C *)
            IF rTemp_SIP_DrainTrap_degC < rRecipe_SIP_TargetTemp_degC THEN
                bCmd_PureSteam_Valve_Open := TRUE;
            ELSIF rTemp_SIP_DrainTrap_degC > (rRecipe_SIP_TargetTemp_degC + 2.0) THEN
                bCmd_PureSteam_Valve_Open := FALSE;
            END_IF;

            rPhaseProgress_pct := 25.0 + MIN(75.0, (rSIP_AccumulatedF0_min / rRecipe_SIP_MinF0_min) * 75.0);

            (* Sterilization Complete Criterion: F0 >= 30.0 min equivalent *)
            IF bSIP_SterilizationValid AND (tStateTimer_s >= 3600.0) THEN
                bSterilizationComplete := TRUE;
                bCycleComplete := TRUE;
                bCmd_PureSteam_Valve_Open := FALSE;
                bCmd_CondensateDrain_Open := FALSE;
                
                (* Return to Safe Sterile Hold *)
                iPrevState := iState;
                iState := 1; (* LYO_STATE_IDLE_STERILE_HOLD *)
                tStateTimer_s := 0.0;
                bStateFirstScan := TRUE;
            END_IF;
        END_IF;

END_CASE;

iCurrentState := iState;
'''

if __name__ == "__main__":
    print(f"Part 4 length: {len(get_part4())} characters")
