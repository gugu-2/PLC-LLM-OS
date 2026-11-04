# part2_tmr_voting.py
# Generates Phase 1 (Cold Initialization & Watchdogs) and Phase 2 (2oo3 TMR Voting for 6 Channels)

def get_part2():
    return '''(* ==========================================================================================
 * PHASE 1: COLD INITIALIZATION, WATCHDOG CHECKS & SUPERVISORY PERMISSIVES
 * ========================================================================================== *)
(* Scan cycle delta time sanity bounding [0.005 s to 0.100 s] *)
IF rDeltaTime_s <= 0.005 THEN
    rDeltaTime_s := 0.020; (* Default to standard 20 ms industrial cyclic task *)
ELSIF rDeltaTime_s >= 0.100 THEN
    rDeltaTime_s := 0.100; (* Clamp maximum execution step to prevent integration blowout *)
END_IF;

(* First-Scan Cold Initialization of Model Parameters, Matrices & Baselines *)
IF NOT bInitialized THEN
    (* 1. Initialize Discrete State Transition Matrix matA (8x8) for 20 ms discretization *)
    (* x1: PreWash Temp [deg C] *)
    matA[1,1] := 0.9850; matA[1,2] := 0.0040; matA[1,3] := 0.0000; matA[1,4] := 0.0080;
    matA[1,5] := 0.0000; matA[1,6] := 0.0000; matA[1,7] := 0.0000; matA[1,8] := 0.0000;
    (* x2: MainWash Zone 1 Temp [deg C] *)
    matA[2,1] := 0.0020; matA[2,2] := 0.9820; matA[2,3] := 0.0120; matA[2,4] := 0.0000;
    matA[2,5] := 0.0000; matA[2,6] := 0.0000; matA[2,7] := 0.0000; matA[2,8] := 0.0000;
    (* x3: MainWash Zone 2 Temp [deg C] *)
    matA[3,1] := 0.0000; matA[3,2] := 0.0080; matA[3,3] := 0.9840; matA[3,4] := 0.0030;
    matA[3,5] := 0.0000; matA[3,6] := 0.0000; matA[3,7] := 0.0000; matA[3,8] := 0.0000;
    (* x4: Counter-Flow Rinse Temp [deg C] *)
    matA[4,1] := 0.0000; matA[4,2] := 0.0000; matA[4,3] := 0.0060; matA[4,4] := 0.9890;
    matA[4,5] := 0.0000; matA[4,6] := 0.0000; matA[4,7] := 0.0000; matA[4,8] := 0.0000;
    (* x5: Reclaim Tank Level [%] *)
    matA[5,1] := 0.0000; matA[5,2] := 0.0000; matA[5,3] := 0.0000; matA[5,4] := 0.0000;
    matA[5,5] := 0.9995; matA[5,6] := 0.0000; matA[5,7] := 0.0000; matA[5,8] := 0.0000;
    (* x6: Wash Bath Conductivity [uS/cm] *)
    matA[6,1] := 0.0000; matA[6,2] := 0.0000; matA[6,3] := 0.0000; matA[6,4] := 0.0000;
    matA[6,5] := 0.0000; matA[6,6] := 0.9920; matA[6,7] := 0.0000; matA[6,8] := 0.0000;
    (* x7: Press Ram Displacement [mm] *)
    matA[7,1] := 0.0000; matA[7,2] := 0.0000; matA[7,3] := 0.0000; matA[7,4] := 0.0000;
    matA[7,5] := 0.0000; matA[7,6] := 0.0000; matA[7,7] := 0.9900; matA[7,8] := 0.0000;
    (* x8: Textile Cake Moisture [%] *)
    matA[8,1] := 0.0000; matA[8,2] := 0.0000; matA[8,3] := 0.0000; matA[8,4] := 0.0000;
    matA[8,5] := 0.0000; matA[8,6] := 0.0000; matA[8,7] := -0.0150; matA[8,8] := 0.9780;

    (* 2. Initialize Discrete Input Control Matrix matB (8x6) *)
    (* u1: Steam [%], u2: Fresh [%], u3: Reclaim [%], u4: Alkali [L/min], u5: Sour [L/min], u6: Press [bar] *)
    matB[1,1] := 0.0015; matB[1,2] := -0.0025; matB[1,3] :=  0.0040; matB[1,4] := 0.0000; matB[1,5] := 0.0000; matB[1,6] := 0.0000;
    matB[2,1] := 0.0240; matB[2,2] := -0.0010; matB[2,3] :=  0.0015; matB[2,4] := 0.0005; matB[2,5] := 0.0000; matB[2,6] := 0.0000;
    matB[3,1] := 0.0195; matB[3,2] := -0.0005; matB[3,3] :=  0.0010; matB[3,4] := 0.0005; matB[3,5] := 0.0000; matB[3,6] := 0.0000;
    matB[4,1] := 0.0005; matB[4,2] := -0.0035; matB[4,3] :=  0.0065; matB[4,4] := 0.0000; matB[4,5] := 0.0000; matB[4,6] := 0.0000;
    matB[5,1] := 0.0002; matB[5,2] :=  0.0045; matB[5,3] := -0.0070; matB[5,4] := 0.0002; matB[5,5] := 0.0001; matB[5,6] := 0.0012;
    matB[6,1] := 0.0000; matB[6,2] := -1.2500; matB[6,3] :=  0.1500; matB[6,4] := 14.500; matB[6,5] :=-8.2000; matB[6,6] := 0.0000;
    matB[7,1] := 0.0000; matB[7,2] :=  0.0000; matB[7,3] :=  0.0000; matB[7,4] := 0.0000; matB[7,5] := 0.0000; matB[7,6] := 0.3200;
    matB[8,1] := 0.0000; matB[8,2] :=  0.0000; matB[8,3] :=  0.0000; matB[8,4] := 0.0000; matB[8,5] := 0.0000; matB[8,6] := -0.0850;

    (* 3. Initialize Identity Measurement Matrix matC (8x8) and Feedthrough matD (8x6) *)
    FOR iLoopIndexI := 1 TO 8 DO
        FOR iLoopIndexJ := 1 TO 8 DO
            IF iLoopIndexI = iLoopIndexJ THEN
                matC[iLoopIndexI, iLoopIndexJ] := 1.0;
            ELSE
                matC[iLoopIndexI, iLoopIndexJ] := 0.0;
            END_IF;
        END_FOR;
        FOR iLoopIndexK := 1 TO 6 DO
            matD[iLoopIndexI, iLoopIndexK] := 0.0;
        END_FOR;
    END_FOR;

    (* 4. Initialize Model Predictive Control (MPC) Cost Weight Matrices Q (8x8) and R (6x6) *)
    FOR iLoopIndexI := 1 TO 8 DO
        FOR iLoopIndexJ := 1 TO 8 DO
            matQ[iLoopIndexI, iLoopIndexJ] := 0.0;
            matP[iLoopIndexI, iLoopIndexJ] := 0.0;
        END_FOR;
    END_FOR;
    (* Diagonal Penalties for Tracking Deviations: Q *)
    matQ[1,1] := 2.5;   (* Pre-Wash Temperature error weight *)
    matQ[2,2] := 12.0;  (* Main Wash Zone 1 Temperature error weight *)
    matQ[3,3] := 15.0;  (* Main Wash Zone 2 Disinfection error weight *)
    matQ[4,4] := 4.0;   (* Rinse Water Temperature error weight *)
    matQ[5,5] := 1.5;   (* Reclaim Tank Level error weight *)
    matQ[6,6] := 0.08;  (* Wash Bath Conductivity error weight *)
    matQ[7,7] := 0.50;  (* Ram Position error weight *)
    matQ[8,8] := 25.0;  (* Cake Moisture Target deviation weight *)

    (* Terminal Lyapunov Penalty Matrix P (approx. 2.5 * Q for Riccati boundary stability) *)
    FOR iLoopIndexI := 1 TO 8 DO
        matP[iLoopIndexI, iLoopIndexI] := matQ[iLoopIndexI, iLoopIndexI] * 2.5;
    END_FOR;

    (* Actuation Effort Penalty Matrix R (6x6) *)
    FOR iLoopIndexI := 1 TO 6 DO
        FOR iLoopIndexJ := 1 TO 6 DO
            matR[iLoopIndexI, iLoopIndexJ] := 0.0;
        END_FOR;
    END_FOR;
    matR[1,1] := 0.15;  (* Steam injection valve throttling penalty *)
    matR[2,2] := 0.45;  (* Fresh water conservation cost penalty *)
    matR[3,3] := 0.05;  (* Reclaim pump VFD wear penalty *)
    matR[4,4] := 1.20;  (* Caustic alkali chemical cost penalty *)
    matR[5,5] := 1.50;  (* Organic sour acid chemical cost penalty *)
    matR[6,6] := 0.25;  (* Hydraulic pump high-pressure power penalty *)

    (* 5. Initialize Luenberger / Kalman Observer Correction Gains *)
    rKalmanGain[1] := 0.12;
    rKalmanGain[2] := 0.18;
    rKalmanGain[3] := 0.20;
    rKalmanGain[4] := 0.10;
    rKalmanGain[5] := 0.08;
    rKalmanGain[6] := 0.22;
    rKalmanGain[7] := 0.15;
    rKalmanGain[8] := 0.25;

    (* 6. Initialize Terzaghi, Darcy & Cake Dewatering Physical Parameters *)
    rCake_InitialHeight_mm   := 850.0;
    rCake_InitialMoisture    := 220.0;
    rCake_CurrentMoisture    := 220.0;
    rCake_WaterMass_kg       := 110.0;
    rCake_FiltrateVol_L      := 0.0;
    rCake_Permeability_m2    := 1.25E-11;
    rCake_SpecificResistance := 4.50E+10;
    rCake_ConsolidationCoeff := 2.80E-04;
    rCake_CompressionStrain  := 0.0;
    rCake_FiltrateFlow_Lps   := 0.0;

    (* 7. Initialize Plate Heat Exchanger Thermal Constants *)
    rPHE_CleanU_Benchmark    := 3850.0; (* Clean baseline overall U-value [W/(m2*K)] *)
    rPHE_HeatTransferCoeff_U := 3850.0;
    rPHE_FoulingResistance   := 0.0;

    (* 8. Initialize Inductive Conductivity & Alkali Coefficients *)
    rCond_RefTemp_degC       := 25.0;
    rCond_TempCoeff_pct_K    := 2.15;

    (* 9. Initialize Peristaltic Tube Fatigue Life *)
    rPeristaltic_MaxRevLife  := 5000000.0; (* 5 Million revolutions rated service life *)
    FOR iLoopIndexI := 1 TO 12 DO
        rPeristaltic_TotalRev[iLoopIndexI]  := 0.0;
        rPeristaltic_Volume_L[iLoopIndexI]  := 0.0;
        rPeristaltic_WearRatio[iLoopIndexI] := 0.0;
    END_FOR;

    (* 10. Alarm Threshold Constants with Hysteresis Deadbands *)
    rHydraulicPress_HH_Trip  := 53.0;
    rHydraulicPress_H_Trip   := 48.0;
    rHydraulicPress_Deadband := 1.5;
    rWashTemp_HH_Trip        := 93.0;
    rWashTemp_H_Trip         := 88.0;
    rWashTemp_L_Trip         := 72.0;
    rWashTemp_LL_Trip        := 45.0;
    rWashTemp_Deadband       := 1.5;
    rReclaimLvl_HH_Trip      := 95.0;
    rReclaimLvl_H_Trip       := 88.0;
    rReclaimLvl_L_Trip       := 25.0;
    rReclaimLvl_LL_Trip      := 10.0;
    rReclaimLvl_Deadband     := 2.0;
    rTurbidity_Severe_Trip   := 150.0;
    rTurbidity_High_Trip     := 80.0;
    rTurbidity_Deadband      := 5.0;

    (* 11. Actuator Slew Limits *)
    rValve_Steam_SlewLimit   := 10.0; (* 10% per second *)
    rPress_Hyd_SlewLimit     := 15.0; (* 15 bar per second *)
    rMpcStepSize             := 0.012;

    (* Initialize State Machine to STANDBY_IDLE *)
    iState := 1;
    iPrevState := 1;
    tStateTimer_s := 0.0;
    tCycleTotalTimer_s := 0.0;
    bStateFirstScan := TRUE;

    bInitialized := TRUE;
END_IF;

(* Master Hardware Emergency Stop & Enable Supervisory Interlock Check *)
IF NOT bEmergencyStop OR NOT bEnable THEN
    (* Immediate Abort Transition to Safe Hydraulic Dump State *)
    IF iState <> 12 THEN
        iPrevState := iState;
        iState := 12; (* CBW_STATE_EMERGENCY_PRESS_DUMP_SAFE *)
        tStateTimer_s := 0.0;
        bStateFirstScan := TRUE;
    END_IF;
END_IF;

(* Global Fault & Alarm Reset Logic *)
IF bReset THEN
    bTMR1_FaultA := FALSE; bTMR1_FaultB := FALSE; bTMR1_FaultC := FALSE;
    tTMR1_TimerA := 0.0;   tTMR1_TimerB := 0.0;   tTMR1_TimerC := 0.0;
    bTMR2_FaultA := FALSE; bTMR2_FaultB := FALSE; bTMR2_FaultC := FALSE;
    tTMR2_TimerA := 0.0;   tTMR2_TimerB := 0.0;   tTMR2_TimerC := 0.0;
    bTMR3_FaultA := FALSE; bTMR3_FaultB := FALSE; bTMR3_FaultC := FALSE;
    tTMR3_TimerA := 0.0;   tTMR3_TimerB := 0.0;   tTMR3_TimerC := 0.0;
    bTMR4_FaultA := FALSE; bTMR4_FaultB := FALSE; bTMR4_FaultC := FALSE;
    tTMR4_TimerA := 0.0;   tTMR4_TimerB := 0.0;   tTMR4_TimerC := 0.0;
    bTMR5_FaultA := FALSE; bTMR5_FaultB := FALSE; bTMR5_FaultC := FALSE;
    tTMR5_TimerA := 0.0;   tTMR5_TimerB := 0.0;   tTMR5_TimerC := 0.0;
    bTMR6_FaultA := FALSE; bTMR6_FaultB := FALSE; bTMR6_FaultC := FALSE;
    tTMR6_TimerA := 0.0;   tTMR6_TimerB := 0.0;   tTMR6_TimerC := 0.0;
    dwISAAlarmWord_Critical := 16#00000000;
    dwISAAlarmWord_Warning  := 16#00000000;
    dwISAAlarmWord_Advisory := 16#00000000;
    bAlarm_AnyCritical := FALSE;
    bAlarm_AnyWarning := FALSE;
END_IF;


(* ==========================================================================================
 * PHASE 2: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING & DISCREPANCY TIMERS
 * ========================================================================================== *)

(* ------------------------------------------------------------------------------------------
 * TMR GROUP 1: MAIN WASH ZONE DIRECT STEAM INJECTION TEMPERATURE (TE101A, TE101B, TE101C) [deg C]
 * Discrepancy Tolerance: 2.5 deg C | Persistence Trip Time: 2.0 s
 * ------------------------------------------------------------------------------------------ *)
rTMR1_DiffAB := ABS(rTemp_MainWash_TE101A - rTemp_MainWash_TE101B);
rTMR1_DiffBC := ABS(rTemp_MainWash_TE101B - rTemp_MainWash_TE101C);
rTMR1_DiffCA := ABS(rTemp_MainWash_TE101C - rTemp_MainWash_TE101A);

(* Channel A Discrepancy Timer: Active if A deviates from both B and C *)
IF (rTMR1_DiffAB > 2.5) AND (rTMR1_DiffCA > 2.5) THEN
    tTMR1_TimerA := tTMR1_TimerA + rDeltaTime_s;
    IF tTMR1_TimerA >= 2.0 THEN
        bTMR1_FaultA := TRUE;
    END_IF;
ELSE
    tTMR1_TimerA := MAX(0.0, tTMR1_TimerA - (2.0 * rDeltaTime_s));
END_IF;

(* Channel B Discrepancy Timer: Active if B deviates from both A and C *)
IF (rTMR1_DiffAB > 2.5) AND (rTMR1_DiffBC > 2.5) THEN
    tTMR1_TimerB := tTMR1_TimerB + rDeltaTime_s;
    IF tTMR1_TimerB >= 2.0 THEN
        bTMR1_FaultB := TRUE;
    END_IF;
ELSE
    tTMR1_TimerB := MAX(0.0, tTMR1_TimerB - (2.0 * rDeltaTime_s));
END_IF;

(* Channel C Discrepancy Timer: Active if C deviates from both A and B *)
IF (rTMR1_DiffBC > 2.5) AND (rTMR1_DiffCA > 2.5) THEN
    tTMR1_TimerC := tTMR1_TimerC + rDeltaTime_s;
    IF tTMR1_TimerC >= 2.0 THEN
        bTMR1_FaultC := TRUE;
    END_IF;
ELSE
    tTMR1_TimerC := MAX(0.0, tTMR1_TimerC - (2.0 * rDeltaTime_s));
END_IF;

(* Group 1 Voting Synthesis & Degradation Handling *)
IF NOT bTMR1_FaultA AND NOT bTMR1_FaultB AND NOT bTMR1_FaultC THEN
    (* 3 Channels Healthy: Strict Median Selection *)
    iTMR1_HealthGrade := 3;
    IF (rTemp_MainWash_TE101A >= rTemp_MainWash_TE101B AND rTemp_MainWash_TE101A <= rTemp_MainWash_TE101C) OR
       (rTemp_MainWash_TE101A >= rTemp_MainWash_TE101C AND rTemp_MainWash_TE101A <= rTemp_MainWash_TE101B) THEN
        rTMR1_VotedVal := rTemp_MainWash_TE101A;
    ELSIF (rTemp_MainWash_TE101B >= rTemp_MainWash_TE101A AND rTemp_MainWash_TE101B <= rTemp_MainWash_TE101C) OR
          (rTemp_MainWash_TE101B >= rTemp_MainWash_TE101C AND rTemp_MainWash_TE101B <= rTemp_MainWash_TE101A) THEN
        rTMR1_VotedVal := rTemp_MainWash_TE101B;
    ELSE
        rTMR1_VotedVal := rTemp_MainWash_TE101C;
    END_IF;
ELSIF bTMR1_FaultA AND NOT bTMR1_FaultB AND NOT bTMR1_FaultC THEN
    (* Channel A Degraded: Bumpless Fallback to Mean of B and C *)
    iTMR1_HealthGrade := 2;
    rTMR1_VotedVal := (rTemp_MainWash_TE101B + rTemp_MainWash_TE101C) * 0.5;
ELSIF bTMR1_FaultB AND NOT bTMR1_FaultA AND NOT bTMR1_FaultC THEN
    (* Channel B Degraded: Bumpless Fallback to Mean of A and C *)
    iTMR1_HealthGrade := 2;
    rTMR1_VotedVal := (rTemp_MainWash_TE101A + rTemp_MainWash_TE101C) * 0.5;
ELSIF bTMR1_FaultC AND NOT bTMR1_FaultA AND NOT bTMR1_FaultB THEN
    (* Channel C Degraded: Bumpless Fallback to Mean of A and B *)
    iTMR1_HealthGrade := 2;
    rTMR1_VotedVal := (rTemp_MainWash_TE101A + rTemp_MainWash_TE101B) * 0.5;
ELSIF NOT bTMR1_FaultA AND bTMR1_FaultB AND bTMR1_FaultC THEN
    (* Dual Sensor Failure: Fallback to Sole Surviving Channel A *)
    iTMR1_HealthGrade := 1;
    rTMR1_VotedVal := rTemp_MainWash_TE101A;
ELSIF NOT bTMR1_FaultB AND bTMR1_FaultA AND bTMR1_FaultC THEN
    (* Dual Sensor Failure: Fallback to Sole Surviving Channel B *)
    iTMR1_HealthGrade := 1;
    rTMR1_VotedVal := rTemp_MainWash_TE101B;
ELSIF NOT bTMR1_FaultC AND bTMR1_FaultA AND bTMR1_FaultB THEN
    (* Dual Sensor Failure: Fallback to Sole Surviving Channel C *)
    iTMR1_HealthGrade := 1;
    rTMR1_VotedVal := rTemp_MainWash_TE101C;
ELSE
    (* Total Sensor Group Failure (0 Channels Healthy): Clamp to Conservative Safe Disinfection Baseline *)
    iTMR1_HealthGrade := 0;
    rTMR1_VotedVal := 85.0; (* Failsafe wash temperature setpoint *)
END_IF;


(* ------------------------------------------------------------------------------------------
 * TMR GROUP 2: GREYWATER HEAT RECOVERY RECLAIM TANK LEVEL (LT201A, LT201B, LT201C) [%]
 * Discrepancy Tolerance: 3.5 % | Persistence Trip Time: 1.5 s
 * ------------------------------------------------------------------------------------------ *)
rTMR2_DiffAB := ABS(rLevel_ReclaimTank_LT201A - rLevel_ReclaimTank_LT201B);
rTMR2_DiffBC := ABS(rLevel_ReclaimTank_LT201B - rLevel_ReclaimTank_LT201C);
rTMR2_DiffCA := ABS(rLevel_ReclaimTank_LT201C - rLevel_ReclaimTank_LT201A);

IF (rTMR2_DiffAB > 3.5) AND (rTMR2_DiffCA > 3.5) THEN
    tTMR2_TimerA := tTMR2_TimerA + rDeltaTime_s;
    IF tTMR2_TimerA >= 1.5 THEN
        bTMR2_FaultA := TRUE;
    END_IF;
ELSE
    tTMR2_TimerA := MAX(0.0, tTMR2_TimerA - (2.0 * rDeltaTime_s));
END_IF;

IF (rTMR2_DiffAB > 3.5) AND (rTMR2_DiffBC > 3.5) THEN
    tTMR2_TimerB := tTMR2_TimerB + rDeltaTime_s;
    IF tTMR2_TimerB >= 1.5 THEN
        bTMR2_FaultB := TRUE;
    END_IF;
ELSE
    tTMR2_TimerB := MAX(0.0, tTMR2_TimerB - (2.0 * rDeltaTime_s));
END_IF;

IF (rTMR2_DiffBC > 3.5) AND (rTMR2_DiffCA > 3.5) THEN
    tTMR2_TimerC := tTMR2_TimerC + rDeltaTime_s;
    IF tTMR2_TimerC >= 1.5 THEN
        bTMR2_FaultC := TRUE;
    END_IF;
ELSE
    tTMR2_TimerC := MAX(0.0, tTMR2_TimerC - (2.0 * rDeltaTime_s));
END_IF;

IF NOT bTMR2_FaultA AND NOT bTMR2_FaultB AND NOT bTMR2_FaultC THEN
    iTMR2_HealthGrade := 3;
    IF (rLevel_ReclaimTank_LT201A >= rLevel_ReclaimTank_LT201B AND rLevel_ReclaimTank_LT201A <= rLevel_ReclaimTank_LT201C) OR
       (rLevel_ReclaimTank_LT201A >= rLevel_ReclaimTank_LT201C AND rLevel_ReclaimTank_LT201A <= rLevel_ReclaimTank_LT201B) THEN
        rTMR2_VotedVal := rLevel_ReclaimTank_LT201A;
    ELSIF (rLevel_ReclaimTank_LT201B >= rLevel_ReclaimTank_LT201A AND rLevel_ReclaimTank_LT201B <= rLevel_ReclaimTank_LT201C) OR
          (rLevel_ReclaimTank_LT201B >= rLevel_ReclaimTank_LT201C AND rLevel_ReclaimTank_LT201B <= rLevel_ReclaimTank_LT201A) THEN
        rTMR2_VotedVal := rLevel_ReclaimTank_LT201B;
    ELSE
        rTMR2_VotedVal := rLevel_ReclaimTank_LT201C;
    END_IF;
ELSIF bTMR2_FaultA AND NOT bTMR2_FaultB AND NOT bTMR2_FaultC THEN
    iTMR2_HealthGrade := 2;
    rTMR2_VotedVal := (rLevel_ReclaimTank_LT201B + rLevel_ReclaimTank_LT201C) * 0.5;
ELSIF bTMR2_FaultB AND NOT bTMR2_FaultA AND NOT bTMR2_FaultC THEN
    iTMR2_HealthGrade := 2;
    rTMR2_VotedVal := (rLevel_ReclaimTank_LT201A + rLevel_ReclaimTank_LT201C) * 0.5;
ELSIF bTMR2_FaultC AND NOT bTMR2_FaultA AND NOT bTMR2_FaultB THEN
    iTMR2_HealthGrade := 2;
    rTMR2_VotedVal := (rLevel_ReclaimTank_LT201A + rLevel_ReclaimTank_LT201B) * 0.5;
ELSIF NOT bTMR2_FaultA AND bTMR2_FaultB AND bTMR2_FaultC THEN
    iTMR2_HealthGrade := 1;
    rTMR2_VotedVal := rLevel_ReclaimTank_LT201A;
ELSIF NOT bTMR2_FaultB AND bTMR2_FaultA AND bTMR2_FaultC THEN
    iTMR2_HealthGrade := 1;
    rTMR2_VotedVal := rLevel_ReclaimTank_LT201B;
ELSIF NOT bTMR2_FaultC AND bTMR2_FaultA AND bTMR2_FaultB THEN
    iTMR2_HealthGrade := 1;
    rTMR2_VotedVal := rLevel_ReclaimTank_LT201C;
ELSE
    iTMR2_HealthGrade := 0;
    rTMR2_VotedVal := 50.0; (* Safe mid-level default *)
END_IF;


(* ------------------------------------------------------------------------------------------
 * TMR GROUP 3: MAIN WASH BATH INDUCTIVE CONDUCTIVITY (AT301A, AT301B, AT301C) [uS/cm]
 * Discrepancy Tolerance: 400.0 uS/cm | Persistence Trip Time: 2.5 s
 * ------------------------------------------------------------------------------------------ *)
rTMR3_DiffAB := ABS(rCond_MainWash_AT301A - rCond_MainWash_AT301B);
rTMR3_DiffBC := ABS(rCond_MainWash_AT301B - rCond_MainWash_AT301C);
rTMR3_DiffCA := ABS(rCond_MainWash_AT301C - rCond_MainWash_AT301A);

IF (rTMR3_DiffAB > 400.0) AND (rTMR3_DiffCA > 400.0) THEN
    tTMR3_TimerA := tTMR3_TimerA + rDeltaTime_s;
    IF tTMR3_TimerA >= 2.5 THEN
        bTMR3_FaultA := TRUE;
    END_IF;
ELSE
    tTMR3_TimerA := MAX(0.0, tTMR3_TimerA - (2.0 * rDeltaTime_s));
END_IF;

IF (rTMR3_DiffAB > 400.0) AND (rTMR3_DiffBC > 400.0) THEN
    tTMR3_TimerB := tTMR3_TimerB + rDeltaTime_s;
    IF tTMR3_TimerB >= 2.5 THEN
        bTMR3_FaultB := TRUE;
    END_IF;
ELSE
    tTMR3_TimerB := MAX(0.0, tTMR3_TimerB - (2.0 * rDeltaTime_s));
END_IF;

IF (rTMR3_DiffBC > 400.0) AND (rTMR3_DiffCA > 400.0) THEN
    tTMR3_TimerC := tTMR3_TimerC + rDeltaTime_s;
    IF tTMR3_TimerC >= 2.5 THEN
        bTMR3_FaultC := TRUE;
    END_IF;
ELSE
    tTMR3_TimerC := MAX(0.0, tTMR3_TimerC - (2.0 * rDeltaTime_s));
END_IF;

IF NOT bTMR3_FaultA AND NOT bTMR3_FaultB AND NOT bTMR3_FaultC THEN
    iTMR3_HealthGrade := 3;
    IF (rCond_MainWash_AT301A >= rCond_MainWash_AT301B AND rCond_MainWash_AT301A <= rCond_MainWash_AT301C) OR
       (rCond_MainWash_AT301A >= rCond_MainWash_AT301C AND rCond_MainWash_AT301A <= rCond_MainWash_AT301B) THEN
        rTMR3_VotedVal := rCond_MainWash_AT301A;
    ELSIF (rCond_MainWash_AT301B >= rCond_MainWash_AT301A AND rCond_MainWash_AT301B <= rCond_MainWash_AT301C) OR
          (rCond_MainWash_AT301B >= rCond_MainWash_AT301C AND rCond_MainWash_AT301B <= rCond_MainWash_AT301A) THEN
        rTMR3_VotedVal := rCond_MainWash_AT301B;
    ELSE
        rTMR3_VotedVal := rCond_MainWash_AT301C;
    END_IF;
ELSIF bTMR3_FaultA AND NOT bTMR3_FaultB AND NOT bTMR3_FaultC THEN
    iTMR3_HealthGrade := 2;
    rTMR3_VotedVal := (rCond_MainWash_AT301B + rCond_MainWash_AT301C) * 0.5;
ELSIF bTMR3_FaultB AND NOT bTMR3_FaultA AND NOT bTMR3_FaultC THEN
    iTMR3_HealthGrade := 2;
    rTMR3_VotedVal := (rCond_MainWash_AT301A + rCond_MainWash_AT301C) * 0.5;
ELSIF bTMR3_FaultC AND NOT bTMR3_FaultA AND NOT bTMR3_FaultB THEN
    iTMR3_HealthGrade := 2;
    rTMR3_VotedVal := (rCond_MainWash_AT301A + rCond_MainWash_AT301B) * 0.5;
ELSIF NOT bTMR3_FaultA AND bTMR3_FaultB AND bTMR3_FaultC THEN
    iTMR3_HealthGrade := 1;
    rTMR3_VotedVal := rCond_MainWash_AT301A;
ELSIF NOT bTMR3_FaultB AND bTMR3_FaultA AND bTMR3_FaultC THEN
    iTMR3_HealthGrade := 1;
    rTMR3_VotedVal := rCond_MainWash_AT301B;
ELSIF NOT bTMR3_FaultC AND bTMR3_FaultA AND bTMR3_FaultB THEN
    iTMR3_HealthGrade := 1;
    rTMR3_VotedVal := rCond_MainWash_AT301C;
ELSE
    iTMR3_HealthGrade := 0;
    rTMR3_VotedVal := 12500.0; (* Safe standard recipe baseline *)
END_IF;


(* ------------------------------------------------------------------------------------------
 * TMR GROUP 4: 50-BAR HYDRAULIC PRESS RAM CYLINDER PRESSURE (PT401A, PT401B, PT401C) [bar]
 * Discrepancy Tolerance: 2.0 bar | Persistence Trip Time: 0.5 s (Fast Safety Critical)
 * ------------------------------------------------------------------------------------------ *)
rTMR4_DiffAB := ABS(rPress_Hydraulic_PT401A - rPress_Hydraulic_PT401B);
rTMR4_DiffBC := ABS(rPress_Hydraulic_PT401B - rPress_Hydraulic_PT401C);
rTMR4_DiffCA := ABS(rPress_Hydraulic_PT401C - rPress_Hydraulic_PT401A);

IF (rTMR4_DiffAB > 2.0) AND (rTMR4_DiffCA > 2.0) THEN
    tTMR4_TimerA := tTMR4_TimerA + rDeltaTime_s;
    IF tTMR4_TimerA >= 0.5 THEN
        bTMR4_FaultA := TRUE;
    END_IF;
ELSE
    tTMR4_TimerA := MAX(0.0, tTMR4_TimerA - (3.0 * rDeltaTime_s));
END_IF;

IF (rTMR4_DiffAB > 2.0) AND (rTMR4_DiffBC > 2.0) THEN
    tTMR4_TimerB := tTMR4_TimerB + rDeltaTime_s;
    IF tTMR4_TimerB >= 0.5 THEN
        bTMR4_FaultB := TRUE;
    END_IF;
ELSE
    tTMR4_TimerB := MAX(0.0, tTMR4_TimerB - (3.0 * rDeltaTime_s));
END_IF;

IF (rTMR4_DiffBC > 2.0) AND (rTMR4_DiffCA > 2.0) THEN
    tTMR4_TimerC := tTMR4_TimerC + rDeltaTime_s;
    IF tTMR4_TimerC >= 0.5 THEN
        bTMR4_FaultC := TRUE;
    END_IF;
ELSE
    tTMR4_TimerC := MAX(0.0, tTMR4_TimerC - (3.0 * rDeltaTime_s));
END_IF;

IF NOT bTMR4_FaultA AND NOT bTMR4_FaultB AND NOT bTMR4_FaultC THEN
    iTMR4_HealthGrade := 3;
    IF (rPress_Hydraulic_PT401A >= rPress_Hydraulic_PT401B AND rPress_Hydraulic_PT401A <= rPress_Hydraulic_PT401C) OR
       (rPress_Hydraulic_PT401A >= rPress_Hydraulic_PT401C AND rPress_Hydraulic_PT401A <= rPress_Hydraulic_PT401B) THEN
        rTMR4_VotedVal := rPress_Hydraulic_PT401A;
    ELSIF (rPress_Hydraulic_PT401B >= rPress_Hydraulic_PT401A AND rPress_Hydraulic_PT401B <= rPress_Hydraulic_PT401C) OR
          (rPress_Hydraulic_PT401B >= rPress_Hydraulic_PT401C AND rPress_Hydraulic_PT401B <= rPress_Hydraulic_PT401A) THEN
        rTMR4_VotedVal := rPress_Hydraulic_PT401B;
    ELSE
        rTMR4_VotedVal := rPress_Hydraulic_PT401C;
    END_IF;
ELSIF bTMR4_FaultA AND NOT bTMR4_FaultB AND NOT bTMR4_FaultC THEN
    iTMR4_HealthGrade := 2;
    (* Safety Critical: When 1 channel fails, select the MAXIMUM of the 2 healthy to prevent overpressure under-reading *)
    rTMR4_VotedVal := MAX(rPress_Hydraulic_PT401B, rPress_Hydraulic_PT401C);
ELSIF bTMR4_FaultB AND NOT bTMR4_FaultA AND NOT bTMR4_FaultC THEN
    iTMR4_HealthGrade := 2;
    rTMR4_VotedVal := MAX(rPress_Hydraulic_PT401A, rPress_Hydraulic_PT401C);
ELSIF bTMR4_FaultC AND NOT bTMR4_FaultA AND NOT bTMR4_FaultB THEN
    iTMR4_HealthGrade := 2;
    rTMR4_VotedVal := MAX(rPress_Hydraulic_PT401A, rPress_Hydraulic_PT401B);
ELSIF NOT bTMR4_FaultA AND bTMR4_FaultB AND bTMR4_FaultC THEN
    iTMR4_HealthGrade := 1;
    rTMR4_VotedVal := rPress_Hydraulic_PT401A;
ELSIF NOT bTMR4_FaultB AND bTMR4_FaultA AND bTMR4_FaultC THEN
    iTMR4_HealthGrade := 1;
    rTMR4_VotedVal := rPress_Hydraulic_PT401B;
ELSIF NOT bTMR4_FaultC AND bTMR4_FaultA AND bTMR4_FaultB THEN
    iTMR4_HealthGrade := 1;
    rTMR4_VotedVal := rPress_Hydraulic_PT401C;
ELSE
    iTMR4_HealthGrade := 0;
    rTMR4_VotedVal := 55.0; (* Trip safety immediately if all pressure sensors lost *)
END_IF;


(* ------------------------------------------------------------------------------------------
 * TMR GROUP 5: PLATE HEAT EXCHANGER (PHE) WARM FRESH OUTLET TEMP (TE501A, TE501B, TE501C) [deg C]
 * Discrepancy Tolerance: 2.0 deg C | Persistence Trip Time: 2.0 s
 * ------------------------------------------------------------------------------------------ *)
rTMR5_DiffAB := ABS(rTemp_HEX_PHE_TE501A - rTemp_HEX_PHE_TE501B);
rTMR5_DiffBC := ABS(rTemp_HEX_PHE_TE501B - rTemp_HEX_PHE_TE501C);
rTMR5_DiffCA := ABS(rTemp_HEX_PHE_TE501C - rTemp_HEX_PHE_TE501A);

IF (rTMR5_DiffAB > 2.0) AND (rTMR5_DiffCA > 2.0) THEN
    tTMR5_TimerA := tTMR5_TimerA + rDeltaTime_s;
    IF tTMR5_TimerA >= 2.0 THEN
        bTMR5_FaultA := TRUE;
    END_IF;
ELSE
    tTMR5_TimerA := MAX(0.0, tTMR5_TimerA - (2.0 * rDeltaTime_s));
END_IF;

IF (rTMR5_DiffAB > 2.0) AND (rTMR5_DiffBC > 2.0) THEN
    tTMR5_TimerB := tTMR5_TimerB + rDeltaTime_s;
    IF tTMR5_TimerB >= 2.0 THEN
        bTMR5_FaultB := TRUE;
    END_IF;
ELSE
    tTMR5_TimerB := MAX(0.0, tTMR5_TimerB - (2.0 * rDeltaTime_s));
END_IF;

IF (rTMR5_DiffBC > 2.0) AND (rTMR5_DiffCA > 2.0) THEN
    tTMR5_TimerC := tTMR5_TimerC + rDeltaTime_s;
    IF tTMR5_TimerC >= 2.0 THEN
        bTMR5_FaultC := TRUE;
    END_IF;
ELSE
    tTMR5_TimerC := MAX(0.0, tTMR5_TimerC - (2.0 * rDeltaTime_s));
END_IF;

IF NOT bTMR5_FaultA AND NOT bTMR5_FaultB AND NOT bTMR5_FaultC THEN
    iTMR5_HealthGrade := 3;
    IF (rTemp_HEX_PHE_TE501A >= rTemp_HEX_PHE_TE501B AND rTemp_HEX_PHE_TE501A <= rTemp_HEX_PHE_TE501C) OR
       (rTemp_HEX_PHE_TE501A >= rTemp_HEX_PHE_TE501C AND rTemp_HEX_PHE_TE501A <= rTemp_HEX_PHE_TE501B) THEN
        rTMR5_VotedVal := rTemp_HEX_PHE_TE501A;
    ELSIF (rTemp_HEX_PHE_TE501B >= rTemp_HEX_PHE_TE501A AND rTemp_HEX_PHE_TE501B <= rTemp_HEX_PHE_TE501C) OR
          (rTemp_HEX_PHE_TE501B >= rTemp_HEX_PHE_TE501C AND rTemp_HEX_PHE_TE501B <= rTemp_HEX_PHE_TE501A) THEN
        rTMR5_VotedVal := rTemp_HEX_PHE_TE501B;
    ELSE
        rTMR5_VotedVal := rTemp_HEX_PHE_TE501C;
    END_IF;
ELSIF bTMR5_FaultA AND NOT bTMR5_FaultB AND NOT bTMR5_FaultC THEN
    iTMR5_HealthGrade := 2;
    rTMR5_VotedVal := (rTemp_HEX_PHE_TE501B + rTemp_HEX_PHE_TE501C) * 0.5;
ELSIF bTMR5_FaultB AND NOT bTMR5_FaultA AND NOT bTMR5_FaultC THEN
    iTMR5_HealthGrade := 2;
    rTMR5_VotedVal := (rTemp_HEX_PHE_TE501A + rTemp_HEX_PHE_TE501C) * 0.5;
ELSIF bTMR5_FaultC AND NOT bTMR5_FaultA AND NOT bTMR5_FaultB THEN
    iTMR5_HealthGrade := 2;
    rTMR5_VotedVal := (rTemp_HEX_PHE_TE501A + rTemp_HEX_PHE_TE501B) * 0.5;
ELSIF NOT bTMR5_FaultA AND bTMR5_FaultB AND bTMR5_FaultC THEN
    iTMR5_HealthGrade := 1;
    rTMR5_VotedVal := rTemp_HEX_PHE_TE501A;
ELSIF NOT bTMR5_FaultB AND bTMR5_FaultA AND bTMR5_FaultC THEN
    iTMR5_HealthGrade := 1;
    rTMR5_VotedVal := rTemp_HEX_PHE_TE501B;
ELSIF NOT bTMR5_FaultC AND bTMR5_FaultA AND bTMR5_FaultB THEN
    iTMR5_HealthGrade := 1;
    rTMR5_VotedVal := rTemp_HEX_PHE_TE501C;
ELSE
    iTMR5_HealthGrade := 0;
    rTMR5_VotedVal := 45.0;
END_IF;


(* ------------------------------------------------------------------------------------------
 * TMR GROUP 6: RECLAIMED GREYWATER OPTICAL TURBIDITY (AT601A, AT601B, AT601C) [NTU]
 * Discrepancy Tolerance: 10.0 NTU | Persistence Trip Time: 3.0 s
 * ------------------------------------------------------------------------------------------ *)
rTMR6_DiffAB := ABS(rTurbidity_Reclaim_AT601A - rTurbidity_Reclaim_AT601B);
rTMR6_DiffBC := ABS(rTurbidity_Reclaim_AT601B - rTurbidity_Reclaim_AT601C);
rTMR6_DiffCA := ABS(rTurbidity_Reclaim_AT601C - rTurbidity_Reclaim_AT601A);

IF (rTMR6_DiffAB > 10.0) AND (rTMR6_DiffCA > 10.0) THEN
    tTMR6_TimerA := tTMR6_TimerA + rDeltaTime_s;
    IF tTMR6_TimerA >= 3.0 THEN
        bTMR6_FaultA := TRUE;
    END_IF;
ELSE
    tTMR6_TimerA := MAX(0.0, tTMR6_TimerA - (2.0 * rDeltaTime_s));
END_IF;

IF (rTMR6_DiffAB > 10.0) AND (rTMR6_DiffBC > 10.0) THEN
    tTMR6_TimerB := tTMR6_TimerB + rDeltaTime_s;
    IF tTMR6_TimerB >= 3.0 THEN
        bTMR6_FaultB := TRUE;
    END_IF;
ELSE
    tTMR6_TimerB := MAX(0.0, tTMR6_TimerB - (2.0 * rDeltaTime_s));
END_IF;

IF (rTMR6_DiffBC > 10.0) AND (rTMR6_DiffCA > 10.0) THEN
    tTMR6_TimerC := tTMR6_TimerC + rDeltaTime_s;
    IF tTMR6_TimerC >= 3.0 THEN
        bTMR6_FaultC := TRUE;
    END_IF;
ELSE
    tTMR6_TimerC := MAX(0.0, tTMR6_TimerC - (2.0 * rDeltaTime_s));
END_IF;

IF NOT bTMR6_FaultA AND NOT bTMR6_FaultB AND NOT bTMR6_FaultC THEN
    iTMR6_HealthGrade := 3;
    IF (rTurbidity_Reclaim_AT601A >= rTurbidity_Reclaim_AT601B AND rTurbidity_Reclaim_AT601A <= rTurbidity_Reclaim_AT601C) OR
       (rTurbidity_Reclaim_AT601A >= rTurbidity_Reclaim_AT601C AND rTurbidity_Reclaim_AT601A <= rTurbidity_Reclaim_AT601B) THEN
        rTMR6_VotedVal := rTurbidity_Reclaim_AT601A;
    ELSIF (rTurbidity_Reclaim_AT601B >= rTurbidity_Reclaim_AT601A AND rTurbidity_Reclaim_AT601B <= rTurbidity_Reclaim_AT601C) OR
          (rTurbidity_Reclaim_AT601B >= rTurbidity_Reclaim_AT601C AND rTurbidity_Reclaim_AT601B <= rTurbidity_Reclaim_AT601A) THEN
        rTMR6_VotedVal := rTurbidity_Reclaim_AT601B;
    ELSE
        rTMR6_VotedVal := rTurbidity_Reclaim_AT601C;
    END_IF;
ELSIF bTMR6_FaultA AND NOT bTMR6_FaultB AND NOT bTMR6_FaultC THEN
    iTMR6_HealthGrade := 2;
    rTMR6_VotedVal := (rTurbidity_Reclaim_AT601B + rTurbidity_Reclaim_AT601C) * 0.5;
ELSIF bTMR6_FaultB AND NOT bTMR6_FaultA AND NOT bTMR6_FaultC THEN
    iTMR6_HealthGrade := 2;
    rTMR6_VotedVal := (rTurbidity_Reclaim_AT601A + rTurbidity_Reclaim_AT601C) * 0.5;
ELSIF bTMR6_FaultC AND NOT bTMR6_FaultA AND NOT bTMR6_FaultB THEN
    iTMR6_HealthGrade := 2;
    rTMR6_VotedVal := (rTurbidity_Reclaim_AT601A + rTurbidity_Reclaim_AT601B) * 0.5;
ELSIF NOT bTMR6_FaultA AND bTMR6_FaultB AND bTMR6_FaultC THEN
    iTMR6_HealthGrade := 1;
    rTMR6_VotedVal := rTurbidity_Reclaim_AT601A;
ELSIF NOT bTMR6_FaultB AND bTMR6_FaultA AND bTMR6_FaultC THEN
    iTMR6_HealthGrade := 1;
    rTMR6_VotedVal := rTurbidity_Reclaim_AT601B;
ELSIF NOT bTMR6_FaultC AND bTMR6_FaultA AND bTMR6_FaultB THEN
    iTMR6_HealthGrade := 1;
    rTMR6_VotedVal := rTurbidity_Reclaim_AT601C;
ELSE
    iTMR6_HealthGrade := 0;
    rTMR6_VotedVal := 160.0; (* Failsafe high turbidity: force diversion to sewer *)
END_IF;
'''

if __name__ == "__main__":
    p2 = get_part2()
    print(f"Part 2 length: {len(p2)} characters")
