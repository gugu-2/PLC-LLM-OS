# -*- coding: utf-8 -*-
"""
Part 3: Phase 1 (Cold Initialization & Permissives) and
Phase 2 (2oo3 Triple Modular Redundancy Sensor Voting Engine)
for FB_Chemicals_Hydrocracker_TrickleBed_HydrogenQuench
"""

def get_init_and_tmr_block():
    return """(* ==========================================================================================
 * PHASE 1: COLD INITIALIZATION, WATCHDOG CHECKS & SUPERVISORY PERMISSIVES
 * ========================================================================================== *)

(* Cyclic execution scan delta time sanity validation and bounding [5 ms .. 100 ms] *)
IF rDeltaTime_s <= 0.005 THEN
    rDeltaTime_s := 0.020; (* Force standard 20 ms deterministic industrial PLC scan cycle *)
ELSIF rDeltaTime_s >= 0.100 THEN
    rDeltaTime_s := 0.100; (* Clamp upper execution threshold to prevent numerical divergence *)
END_IF;

(* First-Scan Cold Initialization of Model Parameters, Matrices & Baselines *)
IF NOT bColdInitDone THEN
    (* 1. Initialize Discrete System Transition Matrix matA (8x8) for Ts = 0.020 s *)
    (* State 1: Bed 1 Core Temperature [deg C] *)
    matA[1,1] := 0.9880; matA[1,2] := 0.0035; matA[1,3] := 0.0000; matA[1,4] := 0.0000;
    matA[1,5] :=-0.0028; matA[1,6] := 0.0005; matA[1,7] := 0.0000; matA[1,8] := 0.0000;
    (* State 2: Bed 2 Core Temperature [deg C] *)
    matA[2,1] := 0.0085; matA[2,2] := 0.9840; matA[2,3] := 0.0040; matA[2,4] := 0.0000;
    matA[2,5] :=-0.0035; matA[2,6] := 0.0008; matA[2,7] := 0.0000; matA[2,8] := 0.0000;
    (* State 3: Bed 3 Core Temperature [deg C] *)
    matA[3,1] := 0.0000; matA[3,2] := 0.0090; matA[3,3] := 0.9830; matA[3,4] := 0.0045;
    matA[3,5] :=-0.0042; matA[3,6] := 0.0010; matA[3,7] := 0.0000; matA[3,8] := 0.0000;
    (* State 4: Bed 4 Core Temperature [deg C] *)
    matA[4,1] := 0.0000; matA[4,2] := 0.0000; matA[4,3] := 0.0095; matA[4,4] := 0.9820;
    matA[4,5] :=-0.0048; matA[4,6] := 0.0012; matA[4,7] := 0.0000; matA[4,8] := 0.0000;
    (* State 5: Quench Header Mass Flow [kg/h] *)
    matA[5,1] := 0.0000; matA[5,2] := 0.0000; matA[5,3] := 0.0000; matA[5,4] := 0.0000;
    matA[5,5] := 0.9650; matA[5,6] := 0.0000; matA[5,7] := 0.0000; matA[5,8] := 0.0000;
    (* State 6: Reactor Hydraulic Delta P [bar] *)
    matA[6,1] := 0.0004; matA[6,2] := 0.0005; matA[6,3] := 0.0006; matA[6,4] := 0.0006;
    matA[6,5] := 0.0001; matA[6,6] := 0.9950; matA[6,7] := 0.0000; matA[6,8] := 0.0000;
    (* State 7: HP Separator Level [%] *)
    matA[7,1] := 0.0000; matA[7,2] := 0.0000; matA[7,3] := 0.0000; matA[7,4] := 0.0000;
    matA[7,5] := 0.0000; matA[7,6] := 0.0000; matA[7,7] := 0.9985; matA[7,8] := 0.0000;
    (* State 8: Amine Absorber Overhead H2S [ppm] *)
    matA[8,1] := 0.0020; matA[8,2] := 0.0035; matA[8,3] := 0.0045; matA[8,4] := 0.0050;
    matA[8,5] := 0.0000; matA[8,6] := 0.0000; matA[8,7] := 0.0000; matA[8,8] := 0.9750;

    (* 2. Initialize Discrete Control Input Coupling Matrix matB (8x6) *)
    (* Inputs: u1:Quench1, u2:Quench2, u3:Quench3, u4:FurnaceDuty, u5:SepLetdown, u6:LeanAmine *)
    matB[1,1] :=-0.0380; matB[1,2] := 0.0000; matB[1,3] := 0.0000; matB[1,4] := 0.0450; matB[1,5] := 0.0000; matB[1,6] := 0.0000;
    matB[2,1] :=-0.0120; matB[2,2] :=-0.0420; matB[2,3] := 0.0000; matB[2,4] := 0.0220; matB[2,5] := 0.0000; matB[2,6] := 0.0000;
    matB[3,1] := 0.0000; matB[3,2] :=-0.0150; matB[3,3] :=-0.0460; matB[3,4] := 0.0120; matB[3,5] := 0.0000; matB[3,6] := 0.0000;
    matB[4,1] := 0.0000; matB[4,2] := 0.0000; matB[4,3] :=-0.0180; matB[4,4] := 0.0060; matB[4,5] := 0.0000; matB[4,6] := 0.0000;
    matB[5,1] := 1.2500; matB[5,2] := 1.3500; matB[5,3] := 1.4500; matB[5,4] := 0.0000; matB[5,5] := 0.0000; matB[5,6] := 0.0000;
    matB[6,1] := 0.0025; matB[6,2] := 0.0028; matB[6,3] := 0.0030; matB[6,4] := 0.0015; matB[6,5] := 0.0000; matB[6,6] := 0.0000;
    matB[7,1] := 0.0000; matB[7,2] := 0.0000; matB[7,3] := 0.0000; matB[7,4] := 0.0000; matB[7,5] :=-0.0650; matB[7,6] := 0.0000;
    matB[8,1] := 0.0000; matB[8,2] := 0.0000; matB[8,3] := 0.0000; matB[8,4] := 0.0180; matB[8,5] := 0.0000; matB[8,6] :=-0.2850;

    (* 3. Initialize Identity Observation Matrix matC (8x8) and Feedthrough matD (8x6) *)
    FOR iIdxI := 1 TO 8 DO
        FOR iIdxJ := 1 TO 8 DO
            IF iIdxI = iIdxJ THEN
                matC[iIdxI, iIdxJ] := 1.0;
            ELSE
                matC[iIdxI, iIdxJ] := 0.0;
            END_IF;
        END_FOR;
        FOR iIdxK := 1 TO 6 DO
            matD[iIdxI, iIdxK] := 0.0;
        END_FOR;
    END_FOR;

    (* 4. Initialize Model Predictive Control (MPC) Weight Matrices Q (8x8) and R (6x6) *)
    FOR iIdxI := 1 TO 8 DO
        FOR iIdxJ := 1 TO 8 DO
            matQ[iIdxI, iIdxJ] := 0.0;
            matP[iIdxI, iIdxJ] := 0.0;
        END_FOR;
    END_FOR;
    matQ[1,1] := 15.0;  (* Bed 1 Temperature Deviation Weight *)
    matQ[2,2] := 18.0;  (* Bed 2 Temperature Deviation Weight *)
    matQ[3,3] := 22.0;  (* Bed 3 Temperature Deviation Weight *)
    matQ[4,4] := 28.0;  (* Bed 4 Temperature Deviation Weight (Highest Risk of Runaway) *)
    matQ[5,5] := 0.05;  (* Quench Gas Flow Variation Weight *)
    matQ[6,6] := 12.0;  (* Reactor Delta P Hydraulic Stress Weight *)
    matQ[7,7] := 16.0;  (* HP Separator Level Stability Weight *)
    matQ[8,8] := 8.5;   (* Amine Absorber H2S Breakthrough Weight *)

    (* Terminal Riccati Lyapunov Stability Matrix P (P ~ 2.5 * Q) *)
    FOR iIdxI := 1 TO 8 DO
        matP[iIdxI, iIdxI] := matQ[iIdxI, iIdxI] * 2.50;
    END_FOR;

    (* Control Effort / Valve Slew Penalty Matrix R (6x6) *)
    FOR iIdxI := 1 TO 6 DO
        FOR iIdxJ := 1 TO 6 DO
            matR[iIdxI, iIdxJ] := 0.0;
        END_FOR;
    END_FOR;
    matR[1,1] := 0.35;  (* Quench Valve 1 Actuation Slew Penalty *)
    matR[2,2] := 0.35;  (* Quench Valve 2 Actuation Slew Penalty *)
    matR[3,3] := 0.40;  (* Quench Valve 3 Actuation Slew Penalty *)
    matR[4,4] := 0.85;  (* Charge Heater Fired Duty Fuel Consumption Penalty *)
    matR[5,5] := 0.50;  (* HP Separator Letdown Valve Wear & Cavitation Penalty *)
    matR[6,6] := 0.25;  (* Lean Amine Circulation Pump Energy Penalty *)

    (* 5. Initialize Diagonal Kalman Filter Observer Innovation Gains *)
    rKalmanGain[1] := 0.16;
    rKalmanGain[2] := 0.18;
    rKalmanGain[3] := 0.20;
    rKalmanGain[4] := 0.22;
    rKalmanGain[5] := 0.08;
    rKalmanGain[6] := 0.12;
    rKalmanGain[7] := 0.15;
    rKalmanGain[8] := 0.25;

    (* 6. Initialize Chemical & Hydrodynamic Baselines *)
    rCatalystBed_VoidFraction      := 0.380;
    rCatalyst_ParticleDia_m        := 0.0016; (* 1.6 mm trilobe extrudate *)
    rSpecificHeat_Oil_kJkgK        := 2.450;
    rMpcStepSize                   := 0.015;

    (* 7. Alarm Thresholds & Safety Limits *)
    rBedTemp_Runaway_Rate_Trip     := 15.0;  (* 15.0 deg C/min SIL-3 Runaway Limit *)
    rBedTemp_HH_Trip               := 435.0; (* 435.0 deg C High-High Hotspot Trip *)
    rBedTemp_H_Trip                := 425.0;
    rBedTemp_L_Trip                := 360.0;
    rBedTemp_LL_Trip               := 320.0;
    rBedTemp_Deadband              := 2.0;
    rReactorPress_HH_Trip          := 198.0; (* 198.0 bar Safety Depressurization Slam *)
    rReactorPress_H_Trip           := 190.0;
    rReactorPress_L_Trip           := 160.0;
    rReactorPress_LL_Trip          := 130.0;
    rReactorPress_Deadband         := 1.5;
    rReactorDP_HH_Trip             := 12.0;  (* 12.0 bar Bed Crushing Trip *)
    rReactorDP_H_Trip              := 8.5;
    rReactorDP_Deadband            := 0.5;
    rHPSepLevel_HH_Trip            := 85.0;
    rHPSepLevel_H_Trip             := 72.0;
    rHPSepLevel_L_Trip             := 30.0;
    rHPSepLevel_LL_Trip            := 15.0;
    rHPSepLevel_Deadband           := 2.5;
    rAmineH2S_HH_Trip              := 150.0;
    rAmineH2S_H_Trip               := 50.0;
    rAmineH2S_Deadband             := 5.0;

    (* Initialize State Machine to 0: Nitrogen Purge & Leak Test *)
    iState := 0;
    iPrevState := 0;
    tStateTimer_s := 0.0;
    tStageTotalTimer_s := 0.0;
    bStateFirstScan := TRUE;
    iSulfidingStage := 1;
    tSulfidingHoldTimer_s := 0.0;

    bColdInitDone := TRUE;
END_IF;

(* Master Hardware Emergency Stop & Automation Enable Interlock Check *)
IF NOT bEmergencyStop OR NOT bEnable THEN
    (* Immediate Forced Trip Transition to High-Pressure Emergency Depressurization (State 8) *)
    IF iState <> 8 THEN
        iPrevState := iState;
        iState := 8; (* STATE_EMERGENCY_DEPRESSURIZATION *)
        tStateTimer_s := 0.0;
        bStateFirstScan := TRUE;
    END_IF;
END_IF;

(* Master Reset Logic for Sensor Latches & Interlocks *)
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
    bTMR7_FaultA := FALSE; bTMR7_FaultB := FALSE; bTMR7_FaultC := FALSE;
    tTMR7_TimerA := 0.0;   tTMR7_TimerB := 0.0;   tTMR7_TimerC := 0.0;
    bTMR8_FaultA := FALSE; bTMR8_FaultB := FALSE; bTMR8_FaultC := FALSE;
    tTMR8_TimerA := 0.0;   tTMR8_TimerB := 0.0;   tTMR8_TimerC := 0.0;
    dwAlarmWord1_Critical := 16#00000000;
    dwAlarmWord2_Process  := 16#00000000;
    dwAlarmWord3_TMR      := 16#00000000;
    bAlarm_RunawayTripActive := FALSE;
    bAlarm_AnyCritical := FALSE;
    bAlarm_AnyWarning := FALSE;
END_IF;


(* ==========================================================================================
 * PHASE 2: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING (8 GROUPS)
 * ========================================================================================== *)

(* --- TMR GROUP 1: BED 1 CORE TEMPERATURE MULTIPOINT THERMOCOUPLES [deg C] --- *)
rTMR1_DiffAB := ABS(rTemp_Bed1_TE101A - rTemp_Bed1_TE101B);
rTMR1_DiffBC := ABS(rTemp_Bed1_TE101B - rTemp_Bed1_TE101C);
rTMR1_DiffCA := ABS(rTemp_Bed1_TE101C - rTemp_Bed1_TE101A);

IF (rTMR1_DiffAB > 8.0) AND (rTMR1_DiffCA > 8.0) THEN
    tTMR1_TimerA := tTMR1_TimerA + rDeltaTime_s;
ELSE
    IF tTMR1_TimerA > 0.0 THEN tTMR1_TimerA := tTMR1_TimerA - (rDeltaTime_s * 2.0); END_IF;
    IF tTMR1_TimerA < 0.0 THEN tTMR1_TimerA := 0.0; END_IF;
END_IF;

IF (rTMR1_DiffAB > 8.0) AND (rTMR1_DiffBC > 8.0) THEN
    tTMR1_TimerB := tTMR1_TimerB + rDeltaTime_s;
ELSE
    IF tTMR1_TimerB > 0.0 THEN tTMR1_TimerB := tTMR1_TimerB - (rDeltaTime_s * 2.0); END_IF;
    IF tTMR1_TimerB < 0.0 THEN tTMR1_TimerB := 0.0; END_IF;
END_IF;

IF (rTMR1_DiffBC > 8.0) AND (rTMR1_DiffCA > 8.0) THEN
    tTMR1_TimerC := tTMR1_TimerC + rDeltaTime_s;
ELSE
    IF tTMR1_TimerC > 0.0 THEN tTMR1_TimerC := tTMR1_TimerC - (rDeltaTime_s * 2.0); END_IF;
    IF tTMR1_TimerC < 0.0 THEN tTMR1_TimerC := 0.0; END_IF;
END_IF;

IF tTMR1_TimerA >= 2.0 THEN bTMR1_FaultA := TRUE; END_IF;
IF tTMR1_TimerB >= 2.0 THEN bTMR1_FaultB := TRUE; END_IF;
IF tTMR1_TimerC >= 2.0 THEN bTMR1_FaultC := TRUE; END_IF;

IF NOT bTMR1_FaultA AND NOT bTMR1_FaultB AND NOT bTMR1_FaultC THEN
    (* 2oo3 Median Selection *)
    IF (rTemp_Bed1_TE101A >= rTemp_Bed1_TE101B AND rTemp_Bed1_TE101A <= rTemp_Bed1_TE101C) OR
       (rTemp_Bed1_TE101A >= rTemp_Bed1_TE101C AND rTemp_Bed1_TE101A <= rTemp_Bed1_TE101B) THEN
        rTMR1_VotedVal := rTemp_Bed1_TE101A;
    ELSIF (rTemp_Bed1_TE101B >= rTemp_Bed1_TE101A AND rTemp_Bed1_TE101B <= rTemp_Bed1_TE101C) OR
          (rTemp_Bed1_TE101B >= rTemp_Bed1_TE101C AND rTemp_Bed1_TE101B <= rTemp_Bed1_TE101A) THEN
        rTMR1_VotedVal := rTemp_Bed1_TE101B;
    ELSE
        rTMR1_VotedVal := rTemp_Bed1_TE101C;
    END_IF;
    iTMR1_HealthGrade := 3;
ELSIF bTMR1_FaultA AND NOT bTMR1_FaultB AND NOT bTMR1_FaultC THEN
    rTMR1_VotedVal := (rTemp_Bed1_TE101B + rTemp_Bed1_TE101C) * 0.5;
    iTMR1_HealthGrade := 2;
ELSIF bTMR1_FaultB AND NOT bTMR1_FaultA AND NOT bTMR1_FaultC THEN
    rTMR1_VotedVal := (rTemp_Bed1_TE101A + rTemp_Bed1_TE101C) * 0.5;
    iTMR1_HealthGrade := 2;
ELSIF bTMR1_FaultC AND NOT bTMR1_FaultA AND NOT bTMR1_FaultB THEN
    rTMR1_VotedVal := (rTemp_Bed1_TE101A + rTemp_Bed1_TE101B) * 0.5;
    iTMR1_HealthGrade := 2;
ELSIF NOT bTMR1_FaultA THEN
    rTMR1_VotedVal := rTemp_Bed1_TE101A;
    iTMR1_HealthGrade := 1;
ELSIF NOT bTMR1_FaultB THEN
    rTMR1_VotedVal := rTemp_Bed1_TE101B;
    iTMR1_HealthGrade := 1;
ELSIF NOT bTMR1_FaultC THEN
    rTMR1_VotedVal := rTemp_Bed1_TE101C;
    iTMR1_HealthGrade := 1;
ELSE
    iTMR1_HealthGrade := 0; (* Triple Fail: Hold Last Voted Value *)
END_IF;

(* --- TMR GROUP 2: BED 2 CORE TEMPERATURE MULTIPOINT THERMOCOUPLES [deg C] --- *)
rTMR2_DiffAB := ABS(rTemp_Bed2_TE102A - rTemp_Bed2_TE102B);
rTMR2_DiffBC := ABS(rTemp_Bed2_TE102B - rTemp_Bed2_TE102C);
rTMR2_DiffCA := ABS(rTemp_Bed2_TE102C - rTemp_Bed2_TE102A);

IF (rTMR2_DiffAB > 8.0) AND (rTMR2_DiffCA > 8.0) THEN
    tTMR2_TimerA := tTMR2_TimerA + rDeltaTime_s;
ELSE
    IF tTMR2_TimerA > 0.0 THEN tTMR2_TimerA := tTMR2_TimerA - (rDeltaTime_s * 2.0); END_IF;
    IF tTMR2_TimerA < 0.0 THEN tTMR2_TimerA := 0.0; END_IF;
END_IF;

IF (rTMR2_DiffAB > 8.0) AND (rTMR2_DiffBC > 8.0) THEN
    tTMR2_TimerB := tTMR2_TimerB + rDeltaTime_s;
ELSE
    IF tTMR2_TimerB > 0.0 THEN tTMR2_TimerB := tTMR2_TimerB - (rDeltaTime_s * 2.0); END_IF;
    IF tTMR2_TimerB < 0.0 THEN tTMR2_TimerB := 0.0; END_IF;
END_IF;

IF (rTMR2_DiffBC > 8.0) AND (rTMR2_DiffCA > 8.0) THEN
    tTMR2_TimerC := tTMR2_TimerC + rDeltaTime_s;
ELSE
    IF tTMR2_TimerC > 0.0 THEN tTMR2_TimerC := tTMR2_TimerC - (rDeltaTime_s * 2.0); END_IF;
    IF tTMR2_TimerC < 0.0 THEN tTMR2_TimerC := 0.0; END_IF;
END_IF;

IF tTMR2_TimerA >= 2.0 THEN bTMR2_FaultA := TRUE; END_IF;
IF tTMR2_TimerB >= 2.0 THEN bTMR2_FaultB := TRUE; END_IF;
IF tTMR2_TimerC >= 2.0 THEN bTMR2_FaultC := TRUE; END_IF;

IF NOT bTMR2_FaultA AND NOT bTMR2_FaultB AND NOT bTMR2_FaultC THEN
    IF (rTemp_Bed2_TE102A >= rTemp_Bed2_TE102B AND rTemp_Bed2_TE102A <= rTemp_Bed2_TE102C) OR
       (rTemp_Bed2_TE102A >= rTemp_Bed2_TE102C AND rTemp_Bed2_TE102A <= rTemp_Bed2_TE102B) THEN
        rTMR2_VotedVal := rTemp_Bed2_TE102A;
    ELSIF (rTemp_Bed2_TE102B >= rTemp_Bed2_TE102A AND rTemp_Bed2_TE102B <= rTemp_Bed2_TE102C) OR
          (rTemp_Bed2_TE102B >= rTemp_Bed2_TE102C AND rTemp_Bed2_TE102B <= rTemp_Bed2_TE102A) THEN
        rTMR2_VotedVal := rTemp_Bed2_TE102B;
    ELSE
        rTMR2_VotedVal := rTemp_Bed2_TE102C;
    END_IF;
    iTMR2_HealthGrade := 3;
ELSIF bTMR2_FaultA AND NOT bTMR2_FaultB AND NOT bTMR2_FaultC THEN
    rTMR2_VotedVal := (rTemp_Bed2_TE102B + rTemp_Bed2_TE102C) * 0.5;
    iTMR2_HealthGrade := 2;
ELSIF bTMR2_FaultB AND NOT bTMR2_FaultA AND NOT bTMR2_FaultC THEN
    rTMR2_VotedVal := (rTemp_Bed2_TE102A + rTemp_Bed2_TE102C) * 0.5;
    iTMR2_HealthGrade := 2;
ELSIF bTMR2_FaultC AND NOT bTMR2_FaultA AND NOT bTMR2_FaultB THEN
    rTMR2_VotedVal := (rTemp_Bed2_TE102A + rTemp_Bed2_TE102B) * 0.5;
    iTMR2_HealthGrade := 2;
ELSIF NOT bTMR2_FaultA THEN
    rTMR2_VotedVal := rTemp_Bed2_TE102A;
    iTMR2_HealthGrade := 1;
ELSIF NOT bTMR2_FaultB THEN
    rTMR2_VotedVal := rTemp_Bed2_TE102B;
    iTMR2_HealthGrade := 1;
ELSIF NOT bTMR2_FaultC THEN
    rTMR2_VotedVal := rTemp_Bed2_TE102C;
    iTMR2_HealthGrade := 1;
ELSE
    iTMR2_HealthGrade := 0;
END_IF;

(* --- TMR GROUP 3: BED 3 CORE TEMPERATURE MULTIPOINT THERMOCOUPLES [deg C] --- *)
rTMR3_DiffAB := ABS(rTemp_Bed3_TE103A - rTemp_Bed3_TE103B);
rTMR3_DiffBC := ABS(rTemp_Bed3_TE103B - rTemp_Bed3_TE103C);
rTMR3_DiffCA := ABS(rTemp_Bed3_TE103C - rTemp_Bed3_TE103A);

IF (rTMR3_DiffAB > 8.0) AND (rTMR3_DiffCA > 8.0) THEN
    tTMR3_TimerA := tTMR3_TimerA + rDeltaTime_s;
ELSE
    IF tTMR3_TimerA > 0.0 THEN tTMR3_TimerA := tTMR3_TimerA - (rDeltaTime_s * 2.0); END_IF;
    IF tTMR3_TimerA < 0.0 THEN tTMR3_TimerA := 0.0; END_IF;
END_IF;

IF (rTMR3_DiffAB > 8.0) AND (rTMR3_DiffBC > 8.0) THEN
    tTMR3_TimerB := tTMR3_TimerB + rDeltaTime_s;
ELSE
    IF tTMR3_TimerB > 0.0 THEN tTMR3_TimerB := tTMR3_TimerB - (rDeltaTime_s * 2.0); END_IF;
    IF tTMR3_TimerB < 0.0 THEN tTMR3_TimerB := 0.0; END_IF;
END_IF;

IF (rTMR3_DiffBC > 8.0) AND (rTMR3_DiffCA > 8.0) THEN
    tTMR3_TimerC := tTMR3_TimerC + rDeltaTime_s;
ELSE
    IF tTMR3_TimerC > 0.0 THEN tTMR3_TimerC := tTMR3_TimerC - (rDeltaTime_s * 2.0); END_IF;
    IF tTMR3_TimerC < 0.0 THEN tTMR3_TimerC := 0.0; END_IF;
END_IF;

IF tTMR3_TimerA >= 2.0 THEN bTMR3_FaultA := TRUE; END_IF;
IF tTMR3_TimerB >= 2.0 THEN bTMR3_FaultB := TRUE; END_IF;
IF tTMR3_TimerC >= 2.0 THEN bTMR3_FaultC := TRUE; END_IF;

IF NOT bTMR3_FaultA AND NOT bTMR3_FaultB AND NOT bTMR3_FaultC THEN
    IF (rTemp_Bed3_TE103A >= rTemp_Bed3_TE103B AND rTemp_Bed3_TE103A <= rTemp_Bed3_TE103C) OR
       (rTemp_Bed3_TE103A >= rTemp_Bed3_TE103C AND rTemp_Bed3_TE103A <= rTemp_Bed3_TE103B) THEN
        rTMR3_VotedVal := rTemp_Bed3_TE103A;
    ELSIF (rTemp_Bed3_TE103B >= rTemp_Bed3_TE103A AND rTemp_Bed3_TE103B <= rTemp_Bed3_TE103C) OR
          (rTemp_Bed3_TE103B >= rTemp_Bed3_TE103C AND rTemp_Bed3_TE103B <= rTemp_Bed3_TE103A) THEN
        rTMR3_VotedVal := rTemp_Bed3_TE103B;
    ELSE
        rTMR3_VotedVal := rTemp_Bed3_TE103C;
    END_IF;
    iTMR3_HealthGrade := 3;
ELSIF bTMR3_FaultA AND NOT bTMR3_FaultB AND NOT bTMR3_FaultC THEN
    rTMR3_VotedVal := (rTemp_Bed3_TE103B + rTemp_Bed3_TE103C) * 0.5;
    iTMR3_HealthGrade := 2;
ELSIF bTMR3_FaultB AND NOT bTMR3_FaultA AND NOT bTMR3_FaultC THEN
    rTMR3_VotedVal := (rTemp_Bed3_TE103A + rTemp_Bed3_TE103C) * 0.5;
    iTMR3_HealthGrade := 2;
ELSIF bTMR3_FaultC AND NOT bTMR3_FaultA AND NOT bTMR3_FaultB THEN
    rTMR3_VotedVal := (rTemp_Bed3_TE103A + rTemp_Bed3_TE103B) * 0.5;
    iTMR3_HealthGrade := 2;
ELSIF NOT bTMR3_FaultA THEN
    rTMR3_VotedVal := rTemp_Bed3_TE103A;
    iTMR3_HealthGrade := 1;
ELSIF NOT bTMR3_FaultB THEN
    rTMR3_VotedVal := rTemp_Bed3_TE103B;
    iTMR3_HealthGrade := 1;
ELSIF NOT bTMR3_FaultC THEN
    rTMR3_VotedVal := rTemp_Bed3_TE103C;
    iTMR3_HealthGrade := 1;
ELSE
    iTMR3_HealthGrade := 0;
END_IF;

(* --- TMR GROUP 4: BED 4 CORE TEMPERATURE MULTIPOINT THERMOCOUPLES [deg C] --- *)
rTMR4_DiffAB := ABS(rTemp_Bed4_TE104A - rTemp_Bed4_TE104B);
rTMR4_DiffBC := ABS(rTemp_Bed4_TE104B - rTemp_Bed4_TE104C);
rTMR4_DiffCA := ABS(rTemp_Bed4_TE104C - rTemp_Bed4_TE104A);

IF (rTMR4_DiffAB > 8.0) AND (rTMR4_DiffCA > 8.0) THEN
    tTMR4_TimerA := tTMR4_TimerA + rDeltaTime_s;
ELSE
    IF tTMR4_TimerA > 0.0 THEN tTMR4_TimerA := tTMR4_TimerA - (rDeltaTime_s * 2.0); END_IF;
    IF tTMR4_TimerA < 0.0 THEN tTMR4_TimerA := 0.0; END_IF;
END_IF;

IF (rTMR4_DiffAB > 8.0) AND (rTMR4_DiffBC > 8.0) THEN
    tTMR4_TimerB := tTMR4_TimerB + rDeltaTime_s;
ELSE
    IF tTMR4_TimerB > 0.0 THEN tTMR4_TimerB := tTMR4_TimerB - (rDeltaTime_s * 2.0); END_IF;
    IF tTMR4_TimerB < 0.0 THEN tTMR4_TimerB := 0.0; END_IF;
END_IF;

IF (rTMR4_DiffBC > 8.0) AND (rTMR4_DiffCA > 8.0) THEN
    tTMR4_TimerC := tTMR4_TimerC + rDeltaTime_s;
ELSE
    IF tTMR4_TimerC > 0.0 THEN tTMR4_TimerC := tTMR4_TimerC - (rDeltaTime_s * 2.0); END_IF;
    IF tTMR4_TimerC < 0.0 THEN tTMR4_TimerC := 0.0; END_IF;
END_IF;

IF tTMR4_TimerA >= 2.0 THEN bTMR4_FaultA := TRUE; END_IF;
IF tTMR4_TimerB >= 2.0 THEN bTMR4_FaultB := TRUE; END_IF;
IF tTMR4_TimerC >= 2.0 THEN bTMR4_FaultC := TRUE; END_IF;

IF NOT bTMR4_FaultA AND NOT bTMR4_FaultB AND NOT bTMR4_FaultC THEN
    IF (rTemp_Bed4_TE104A >= rTemp_Bed4_TE104B AND rTemp_Bed4_TE104A <= rTemp_Bed4_TE104C) OR
       (rTemp_Bed4_TE104A >= rTemp_Bed4_TE104C AND rTemp_Bed4_TE104A <= rTemp_Bed4_TE104B) THEN
        rTMR4_VotedVal := rTemp_Bed4_TE104A;
    ELSIF (rTemp_Bed4_TE104B >= rTemp_Bed4_TE104A AND rTemp_Bed4_TE104B <= rTemp_Bed4_TE104C) OR
          (rTemp_Bed4_TE104B >= rTemp_Bed4_TE104C AND rTemp_Bed4_TE104B <= rTemp_Bed4_TE104A) THEN
        rTMR4_VotedVal := rTemp_Bed4_TE104B;
    ELSE
        rTMR4_VotedVal := rTemp_Bed4_TE104C;
    END_IF;
    iTMR4_HealthGrade := 3;
ELSIF bTMR4_FaultA AND NOT bTMR4_FaultB AND NOT bTMR4_FaultC THEN
    rTMR4_VotedVal := (rTemp_Bed4_TE104B + rTemp_Bed4_TE104C) * 0.5;
    iTMR4_HealthGrade := 2;
ELSIF bTMR4_FaultB AND NOT bTMR4_FaultA AND NOT bTMR4_FaultC THEN
    rTMR4_VotedVal := (rTemp_Bed4_TE104A + rTemp_Bed4_TE104C) * 0.5;
    iTMR4_HealthGrade := 2;
ELSIF bTMR4_FaultC AND NOT bTMR4_FaultA AND NOT bTMR4_FaultB THEN
    rTMR4_VotedVal := (rTemp_Bed4_TE104A + rTemp_Bed4_TE104B) * 0.5;
    iTMR4_HealthGrade := 2;
ELSIF NOT bTMR4_FaultA THEN
    rTMR4_VotedVal := rTemp_Bed4_TE104A;
    iTMR4_HealthGrade := 1;
ELSIF NOT bTMR4_FaultB THEN
    rTMR4_VotedVal := rTemp_Bed4_TE104B;
    iTMR4_HealthGrade := 1;
ELSIF NOT bTMR4_FaultC THEN
    rTMR4_VotedVal := rTemp_Bed4_TE104C;
    iTMR4_HealthGrade := 1;
ELSE
    iTMR4_HealthGrade := 0;
END_IF;

(* --- TMR GROUP 5: HIGH-PRESSURE SEPARATOR NUCLEAR LEVEL TRANSMITTERS [%] --- *)
rTMR5_DiffAB := ABS(rLevel_HPSep_LT201A - rLevel_HPSep_LT201B);
rTMR5_DiffBC := ABS(rLevel_HPSep_LT201B - rLevel_HPSep_LT201C);
rTMR5_DiffCA := ABS(rLevel_HPSep_LT201C - rLevel_HPSep_LT201A);

IF (rTMR5_DiffAB > 5.0) AND (rTMR5_DiffCA > 5.0) THEN
    tTMR5_TimerA := tTMR5_TimerA + rDeltaTime_s;
ELSE
    IF tTMR5_TimerA > 0.0 THEN tTMR5_TimerA := tTMR5_TimerA - (rDeltaTime_s * 2.0); END_IF;
    IF tTMR5_TimerA < 0.0 THEN tTMR5_TimerA := 0.0; END_IF;
END_IF;

IF (rTMR5_DiffAB > 5.0) AND (rTMR5_DiffBC > 5.0) THEN
    tTMR5_TimerB := tTMR5_TimerB + rDeltaTime_s;
ELSE
    IF tTMR5_TimerB > 0.0 THEN tTMR5_TimerB := tTMR5_TimerB - (rDeltaTime_s * 2.0); END_IF;
    IF tTMR5_TimerB < 0.0 THEN tTMR5_TimerB := 0.0; END_IF;
END_IF;

IF (rTMR5_DiffBC > 5.0) AND (rTMR5_DiffCA > 5.0) THEN
    tTMR5_TimerC := tTMR5_TimerC + rDeltaTime_s;
ELSE
    IF tTMR5_TimerC > 0.0 THEN tTMR5_TimerC := tTMR5_TimerC - (rDeltaTime_s * 2.0); END_IF;
    IF tTMR5_TimerC < 0.0 THEN tTMR5_TimerC := 0.0; END_IF;
END_IF;

IF tTMR5_TimerA >= 1.5 THEN bTMR5_FaultA := TRUE; END_IF;
IF tTMR5_TimerB >= 1.5 THEN bTMR5_FaultB := TRUE; END_IF;
IF tTMR5_TimerC >= 1.5 THEN bTMR5_FaultC := TRUE; END_IF;

IF NOT bTMR5_FaultA AND NOT bTMR5_FaultB AND NOT bTMR5_FaultC THEN
    IF (rLevel_HPSep_LT201A >= rLevel_HPSep_LT201B AND rLevel_HPSep_LT201A <= rLevel_HPSep_LT201C) OR
       (rLevel_HPSep_LT201A >= rLevel_HPSep_LT201C AND rLevel_HPSep_LT201A <= rLevel_HPSep_LT201B) THEN
        rTMR5_VotedVal := rLevel_HPSep_LT201A;
    ELSIF (rLevel_HPSep_LT201B >= rLevel_HPSep_LT201A AND rLevel_HPSep_LT201B <= rLevel_HPSep_LT201C) OR
          (rLevel_HPSep_LT201B >= rLevel_HPSep_LT201C AND rLevel_HPSep_LT201B <= rLevel_HPSep_LT201A) THEN
        rTMR5_VotedVal := rLevel_HPSep_LT201B;
    ELSE
        rTMR5_VotedVal := rLevel_HPSep_LT201C;
    END_IF;
    iTMR5_HealthGrade := 3;
ELSIF bTMR5_FaultA AND NOT bTMR5_FaultB AND NOT bTMR5_FaultC THEN
    rTMR5_VotedVal := (rLevel_HPSep_LT201B + rLevel_HPSep_LT201C) * 0.5;
    iTMR5_HealthGrade := 2;
ELSIF bTMR5_FaultB AND NOT bTMR5_FaultA AND NOT bTMR5_FaultC THEN
    rTMR5_VotedVal := (rLevel_HPSep_LT201A + rLevel_HPSep_LT201C) * 0.5;
    iTMR5_HealthGrade := 2;
ELSIF bTMR5_FaultC AND NOT bTMR5_FaultA AND NOT bTMR5_FaultB THEN
    rTMR5_VotedVal := (rLevel_HPSep_LT201A + rLevel_HPSep_LT201B) * 0.5;
    iTMR5_HealthGrade := 2;
ELSIF NOT bTMR5_FaultA THEN
    rTMR5_VotedVal := rLevel_HPSep_LT201A;
    iTMR5_HealthGrade := 1;
ELSIF NOT bTMR5_FaultB THEN
    rTMR5_VotedVal := rLevel_HPSep_LT201B;
    iTMR5_HealthGrade := 1;
ELSIF NOT bTMR5_FaultC THEN
    rTMR5_VotedVal := rLevel_HPSep_LT201C;
    iTMR5_HealthGrade := 1;
ELSE
    iTMR5_HealthGrade := 0;
END_IF;

(* --- TMR GROUP 6: REACTOR TOTAL DIFFERENTIAL PRESSURE CELLS [bar] --- *)
rTMR6_DiffAB := ABS(rDP_Reactor_DPT301A - rDP_Reactor_DPT301B);
rTMR6_DiffBC := ABS(rDP_Reactor_DPT301B - rDP_Reactor_DPT301C);
rTMR6_DiffCA := ABS(rDP_Reactor_DPT301C - rDP_Reactor_DPT301A);

IF (rTMR6_DiffAB > 0.6) AND (rTMR6_DiffCA > 0.6) THEN
    tTMR6_TimerA := tTMR6_TimerA + rDeltaTime_s;
ELSE
    IF tTMR6_TimerA > 0.0 THEN tTMR6_TimerA := tTMR6_TimerA - (rDeltaTime_s * 2.0); END_IF;
    IF tTMR6_TimerA < 0.0 THEN tTMR6_TimerA := 0.0; END_IF;
END_IF;

IF (rTMR6_DiffAB > 0.6) AND (rTMR6_DiffBC > 0.6) THEN
    tTMR6_TimerB := tTMR6_TimerB + rDeltaTime_s;
ELSE
    IF tTMR6_TimerB > 0.0 THEN tTMR6_TimerB := tTMR6_TimerB - (rDeltaTime_s * 2.0); END_IF;
    IF tTMR6_TimerB < 0.0 THEN tTMR6_TimerB := 0.0; END_IF;
END_IF;

IF (rTMR6_DiffBC > 0.6) AND (rTMR6_DiffCA > 0.6) THEN
    tTMR6_TimerC := tTMR6_TimerC + rDeltaTime_s;
ELSE
    IF tTMR6_TimerC > 0.0 THEN tTMR6_TimerC := tTMR6_TimerC - (rDeltaTime_s * 2.0); END_IF;
    IF tTMR6_TimerC < 0.0 THEN tTMR6_TimerC := 0.0; END_IF;
END_IF;

IF tTMR6_TimerA >= 1.5 THEN bTMR6_FaultA := TRUE; END_IF;
IF tTMR6_TimerB >= 1.5 THEN bTMR6_FaultB := TRUE; END_IF;
IF tTMR6_TimerC >= 1.5 THEN bTMR6_FaultC := TRUE; END_IF;

IF NOT bTMR6_FaultA AND NOT bTMR6_FaultB AND NOT bTMR6_FaultC THEN
    IF (rDP_Reactor_DPT301A >= rDP_Reactor_DPT301B AND rDP_Reactor_DPT301A <= rDP_Reactor_DPT301C) OR
       (rDP_Reactor_DPT301A >= rDP_Reactor_DPT301C AND rDP_Reactor_DPT301A <= rDP_Reactor_DPT301B) THEN
        rTMR6_VotedVal := rDP_Reactor_DPT301A;
    ELSIF (rDP_Reactor_DPT301B >= rDP_Reactor_DPT301A AND rDP_Reactor_DPT301B <= rDP_Reactor_DPT301C) OR
          (rDP_Reactor_DPT301B >= rDP_Reactor_DPT301C AND rDP_Reactor_DPT301B <= rDP_Reactor_DPT301A) THEN
        rTMR6_VotedVal := rDP_Reactor_DPT301B;
    ELSE
        rTMR6_VotedVal := rDP_Reactor_DPT301C;
    END_IF;
    iTMR6_HealthGrade := 3;
ELSIF bTMR6_FaultA AND NOT bTMR6_FaultB AND NOT bTMR6_FaultC THEN
    rTMR6_VotedVal := (rDP_Reactor_DPT301B + rDP_Reactor_DPT301C) * 0.5;
    iTMR6_HealthGrade := 2;
ELSIF bTMR6_FaultB AND NOT bTMR6_FaultA AND NOT bTMR6_FaultC THEN
    rTMR6_VotedVal := (rDP_Reactor_DPT301A + rDP_Reactor_DPT301C) * 0.5;
    iTMR6_HealthGrade := 2;
ELSIF bTMR6_FaultC AND NOT bTMR6_FaultA AND NOT bTMR6_FaultB THEN
    rTMR6_VotedVal := (rDP_Reactor_DPT301A + rDP_Reactor_DPT301B) * 0.5;
    iTMR6_HealthGrade := 2;
ELSIF NOT bTMR6_FaultA THEN
    rTMR6_VotedVal := rDP_Reactor_DPT301A;
    iTMR6_HealthGrade := 1;
ELSIF NOT bTMR6_FaultB THEN
    rTMR6_VotedVal := rDP_Reactor_DPT301B;
    iTMR6_HealthGrade := 1;
ELSIF NOT bTMR6_FaultC THEN
    rTMR6_VotedVal := rDP_Reactor_DPT301C;
    iTMR6_HealthGrade := 1;
ELSE
    iTMR6_HealthGrade := 0;
END_IF;

(* --- TMR GROUP 7: REACTOR INLET HEAD PRESSURE TRANSMITTERS [bar] --- *)
rTMR7_DiffAB := ABS(rPress_Inlet_PT401A - rPress_Inlet_PT401B);
rTMR7_DiffBC := ABS(rPress_Inlet_PT401B - rPress_Inlet_PT401C);
rTMR7_DiffCA := ABS(rPress_Inlet_PT401C - rPress_Inlet_PT401A);

IF (rTMR7_DiffAB > 3.0) AND (rTMR7_DiffCA > 3.0) THEN
    tTMR7_TimerA := tTMR7_TimerA + rDeltaTime_s;
ELSE
    IF tTMR7_TimerA > 0.0 THEN tTMR7_TimerA := tTMR7_TimerA - (rDeltaTime_s * 2.0); END_IF;
    IF tTMR7_TimerA < 0.0 THEN tTMR7_TimerA := 0.0; END_IF;
END_IF;

IF (rTMR7_DiffAB > 3.0) AND (rTMR7_DiffBC > 3.0) THEN
    tTMR7_TimerB := tTMR7_TimerB + rDeltaTime_s;
ELSE
    IF tTMR7_TimerB > 0.0 THEN tTMR7_TimerB := tTMR7_TimerB - (rDeltaTime_s * 2.0); END_IF;
    IF tTMR7_TimerB < 0.0 THEN tTMR7_TimerB := 0.0; END_IF;
END_IF;

IF (rTMR7_DiffBC > 3.0) AND (rTMR7_DiffCA > 3.0) THEN
    tTMR7_TimerC := tTMR7_TimerC + rDeltaTime_s;
ELSE
    IF tTMR7_TimerC > 0.0 THEN tTMR7_TimerC := tTMR7_TimerC - (rDeltaTime_s * 2.0); END_IF;
    IF tTMR7_TimerC < 0.0 THEN tTMR7_TimerC := 0.0; END_IF;
END_IF;

IF tTMR7_TimerA >= 1.0 THEN bTMR7_FaultA := TRUE; END_IF;
IF tTMR7_TimerB >= 1.0 THEN bTMR7_FaultB := TRUE; END_IF;
IF tTMR7_TimerC >= 1.0 THEN bTMR7_FaultC := TRUE; END_IF;

IF NOT bTMR7_FaultA AND NOT bTMR7_FaultB AND NOT bTMR7_FaultC THEN
    IF (rPress_Inlet_PT401A >= rPress_Inlet_PT401B AND rPress_Inlet_PT401A <= rPress_Inlet_PT401C) OR
       (rPress_Inlet_PT401A >= rPress_Inlet_PT401C AND rPress_Inlet_PT401A <= rPress_Inlet_PT401B) THEN
        rTMR7_VotedVal := rPress_Inlet_PT401A;
    ELSIF (rPress_Inlet_PT401B >= rPress_Inlet_PT401A AND rPress_Inlet_PT401B <= rPress_Inlet_PT401C) OR
          (rPress_Inlet_PT401B >= rPress_Inlet_PT401C AND rPress_Inlet_PT401B <= rPress_Inlet_PT401A) THEN
        rTMR7_VotedVal := rPress_Inlet_PT401B;
    ELSE
        rTMR7_VotedVal := rPress_Inlet_PT401C;
    END_IF;
    iTMR7_HealthGrade := 3;
ELSIF bTMR7_FaultA AND NOT bTMR7_FaultB AND NOT bTMR7_FaultC THEN
    rTMR7_VotedVal := (rPress_Inlet_PT401B + rPress_Inlet_PT401C) * 0.5;
    iTMR7_HealthGrade := 2;
ELSIF bTMR7_FaultB AND NOT bTMR7_FaultA AND NOT bTMR7_FaultC THEN
    rTMR7_VotedVal := (rPress_Inlet_PT401A + rPress_Inlet_PT401C) * 0.5;
    iTMR7_HealthGrade := 2;
ELSIF bTMR7_FaultC AND NOT bTMR7_FaultA AND NOT bTMR7_FaultB THEN
    rTMR7_VotedVal := (rPress_Inlet_PT401A + rPress_Inlet_PT401B) * 0.5;
    iTMR7_HealthGrade := 2;
ELSIF NOT bTMR7_FaultA THEN
    rTMR7_VotedVal := rPress_Inlet_PT401A;
    iTMR7_HealthGrade := 1;
ELSIF NOT bTMR7_FaultB THEN
    rTMR7_VotedVal := rPress_Inlet_PT401B;
    iTMR7_HealthGrade := 1;
ELSIF NOT bTMR7_FaultC THEN
    rTMR7_VotedVal := rPress_Inlet_PT401C;
    iTMR7_HealthGrade := 1;
ELSE
    iTMR7_HealthGrade := 0;
END_IF;

(* --- TMR GROUP 8: AMINE ABSORBER OVERHEAD ACID GAS H2S ANALYZERS [ppm] --- *)
rTMR8_DiffAB := ABS(rConc_OverheadH2S_AT501A - rConc_OverheadH2S_AT501B);
rTMR8_DiffBC := ABS(rConc_OverheadH2S_AT501B - rConc_OverheadH2S_AT501C);
rTMR8_DiffCA := ABS(rConc_OverheadH2S_AT501C - rConc_OverheadH2S_AT501A);

IF (rTMR8_DiffAB > 10.0) AND (rTMR8_DiffCA > 10.0) THEN
    tTMR8_TimerA := tTMR8_TimerA + rDeltaTime_s;
ELSE
    IF tTMR8_TimerA > 0.0 THEN tTMR8_TimerA := tTMR8_TimerA - (rDeltaTime_s * 2.0); END_IF;
    IF tTMR8_TimerA < 0.0 THEN tTMR8_TimerA := 0.0; END_IF;
END_IF;

IF (rTMR8_DiffAB > 10.0) AND (rTMR8_DiffBC > 10.0) THEN
    tTMR8_TimerB := tTMR8_TimerB + rDeltaTime_s;
ELSE
    IF tTMR8_TimerB > 0.0 THEN tTMR8_TimerB := tTMR8_TimerB - (rDeltaTime_s * 2.0); END_IF;
    IF tTMR8_TimerB < 0.0 THEN tTMR8_TimerB := 0.0; END_IF;
END_IF;

IF (rTMR8_DiffBC > 10.0) AND (rTMR8_DiffCA > 10.0) THEN
    tTMR8_TimerC := tTMR8_TimerC + rDeltaTime_s;
ELSE
    IF tTMR8_TimerC > 0.0 THEN tTMR8_TimerC := tTMR8_TimerC - (rDeltaTime_s * 2.0); END_IF;
    IF tTMR8_TimerC < 0.0 THEN tTMR8_TimerC := 0.0; END_IF;
END_IF;

IF tTMR8_TimerA >= 2.0 THEN bTMR8_FaultA := TRUE; END_IF;
IF tTMR8_TimerB >= 2.0 THEN bTMR8_FaultB := TRUE; END_IF;
IF tTMR8_TimerC >= 2.0 THEN bTMR8_FaultC := TRUE; END_IF;

IF NOT bTMR8_FaultA AND NOT bTMR8_FaultB AND NOT bTMR8_FaultC THEN
    IF (rConc_OverheadH2S_AT501A >= rConc_OverheadH2S_AT501B AND rConc_OverheadH2S_AT501A <= rConc_OverheadH2S_AT501C) OR
       (rConc_OverheadH2S_AT501A >= rConc_OverheadH2S_AT501C AND rConc_OverheadH2S_AT501A <= rConc_OverheadH2S_AT501B) THEN
        rTMR8_VotedVal := rConc_OverheadH2S_AT501A;
    ELSIF (rConc_OverheadH2S_AT501B >= rConc_OverheadH2S_AT501A AND rConc_OverheadH2S_AT501B <= rConc_OverheadH2S_AT501C) OR
          (rConc_OverheadH2S_AT501B >= rConc_OverheadH2S_AT501C AND rConc_OverheadH2S_AT501B <= rConc_OverheadH2S_AT501A) THEN
        rTMR8_VotedVal := rConc_OverheadH2S_AT501B;
    ELSE
        rTMR8_VotedVal := rConc_OverheadH2S_AT501C;
    END_IF;
    iTMR8_HealthGrade := 3;
ELSIF bTMR8_FaultA AND NOT bTMR8_FaultB AND NOT bTMR8_FaultC THEN
    rTMR8_VotedVal := (rConc_OverheadH2S_AT501B + rConc_OverheadH2S_AT501C) * 0.5;
    iTMR8_HealthGrade := 2;
ELSIF bTMR8_FaultB AND NOT bTMR8_FaultA AND NOT bTMR8_FaultC THEN
    rTMR8_VotedVal := (rConc_OverheadH2S_AT501A + rConc_OverheadH2S_AT501C) * 0.5;
    iTMR8_HealthGrade := 2;
ELSIF bTMR8_FaultC AND NOT bTMR8_FaultA AND NOT bTMR8_FaultB THEN
    rTMR8_VotedVal := (rConc_OverheadH2S_AT501A + rConc_OverheadH2S_AT501B) * 0.5;
    iTMR8_HealthGrade := 2;
ELSIF NOT bTMR8_FaultA THEN
    rTMR8_VotedVal := rConc_OverheadH2S_AT501A;
    iTMR8_HealthGrade := 1;
ELSIF NOT bTMR8_FaultB THEN
    rTMR8_VotedVal := rConc_OverheadH2S_AT501B;
    iTMR8_HealthGrade := 1;
ELSIF NOT bTMR8_FaultC THEN
    rTMR8_VotedVal := rConc_OverheadH2S_AT501C;
    iTMR8_HealthGrade := 1;
ELSE
    iTMR8_HealthGrade := 0;
END_IF;
"""
