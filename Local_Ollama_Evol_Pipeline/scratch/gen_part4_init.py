# Generator part 4: First scan initialization and E-Stop
def get_init_logic():
    return """(* ============================================================================================= *)
(* SECTION 0: MASTER SIL-3 HARDWIRED SAFETY INTERLOCKS & FIRST-SCAN MATRIX ALLOCATION             *)
(* ============================================================================================= *)
(* 0.1 Master Emergency Stop Supervision (Hardwired Relay Input, Active-Low) *)
IF NOT bEmergencyStop THEN
    iMachineState                   := 999;             (* Force state machine into EMERGENCY_ESTOP *)
    rSAG_FreshFeedRateCmd_tph       := 0.0;             (* Instantaneous cutoff of fresh feed conveyor *)
    rMillInletWaterFlowCmd_m3h      := 0.0;             (* Isolate mill feed dilution water valve *)
    rRingMotorSpeedCmd_RPM          := 0.0;             (* Trip gearless synchronous ring motor excitation *)
    rRingMotorTorqueLimit_kNm       := 0.0;             (* Zero drive active torque demand *)
    rCyclonePumpSpeedCmd_RPM        := 0.0;             (* Stop cyclone feed slurry pump *)
    rCycloneSumpWaterValveCmd_Pct   := 0.0;             (* Close sump dilution water valve *)
    rPebbleCrusherFeedDiverter_Pct  := 0.0;             (* Divert pebbles away from SAG mill *)
    bJackingOilPumpStart_Cmd        := TRUE;            (* Maintain bearing jacking oil lift to protect Babbitt pads *)
    bInchingDriveEngage_Cmd         := FALSE;           (* Inhibit inching drive engagement *)
    bCriticalImpactEmergencyActive  := FALSE;
    bMillOverfillingSlurrySpillTrip := FALSE;
    bSumpCavitationProtectionActive := FALSE;
    bMPC_ControllerActive           := FALSE;
    dwAlarmWord_HighTrip            := dwAlarmWord_HighTrip OR 16#8000_0000; (* Bit 31: HARDWIRED_ESTOP_TRIP *)
    dwSystemStatusWord              := 16#0000_03E7;    (* 999 in HEX *)
    FOR iCycloneIdx := 1 TO 12 DO
        abCycloneValveOpen_Cmd[iCycloneIdx] := FALSE;   (* Isolate hydrocyclone feed knife-gate valves *)
    END_FOR;
    RETURN;                                             (* Halt cyclic execution immediately *)
END_IF;

(* 0.2 Master Block Enable Check *)
IF NOT bEnable THEN
    iMachineState                   := 0;               (* Hold system in OFFLINE state *)
    rSAG_FreshFeedRateCmd_tph       := 0.0;
    rMillInletWaterFlowCmd_m3h      := 0.0;
    rRingMotorSpeedCmd_RPM          := 0.0;
    rRingMotorTorqueLimit_kNm       := 0.0;
    rCyclonePumpSpeedCmd_RPM        := 0.0;
    rCycloneSumpWaterValveCmd_Pct   := 0.0;
    bMPC_ControllerActive           := FALSE;
    dwSystemStatusWord              := 16#0000_0000;
    RETURN;
END_IF;

(* 0.3 First-Scan Discrete State-Space (8x8) Matrix Allocation & Constant Preconditioning *)
IF NOT bFirstScanDone THEN
    (* ----------------------------------------------------------------------------------------- *)
    (* Discrete State Transition Matrix A (8x8) evaluated at Ts = 0.010 s (10 ms cycle)          *)
    (* States:                                                                                   *)
    (* x0: Delta M_ore_coarse [t]                                                                *)
    (* x1: Delta M_ore_fine [t]                                                                  *)
    (* x2: Delta V_water [m3]                                                                    *)
    (* x3: Delta theta_toe [deg]                                                                 *)
    (* x4: Delta E_impact [%]                                                                    *)
    (* x5: Delta V_sump [m3]                                                                     *)
    (* x6: Delta rho_sump [SG]                                                                   *)
    (* x7: Delta omega_m [RPM]                                                                   *)
    (* ----------------------------------------------------------------------------------------- *)
    aMatrix_A[0,0] := 0.9978; aMatrix_A[0,1] := 0.0000; aMatrix_A[0,2] := 0.0000; aMatrix_A[0,3] :=-0.0012; aMatrix_A[0,4] := 0.0000; aMatrix_A[0,5] := 0.0000; aMatrix_A[0,6] := 0.0000; aMatrix_A[0,7] :=-0.0045;
    aMatrix_A[1,0] := 0.0021; aMatrix_A[1,1] := 0.9962; aMatrix_A[1,2] := 0.0008; aMatrix_A[1,3] := 0.0000; aMatrix_A[1,4] := 0.0000; aMatrix_A[1,5] := 0.0000; aMatrix_A[1,6] := 0.0000; aMatrix_A[1,7] :=-0.0022;
    aMatrix_A[2,0] := 0.0000; aMatrix_A[2,1] := 0.0000; aMatrix_A[2,2] := 0.9955; aMatrix_A[2,3] := 0.0000; aMatrix_A[2,4] := 0.0000; aMatrix_A[2,5] := 0.0000; aMatrix_A[2,6] := 0.0000; aMatrix_A[2,7] :=-0.0015;
    aMatrix_A[3,0] := 0.0125; aMatrix_A[3,1] := 0.0045; aMatrix_A[3,2] :=-0.0085; aMatrix_A[3,3] := 0.9820; aMatrix_A[3,4] :=-0.0150; aMatrix_A[3,5] := 0.0000; aMatrix_A[3,6] := 0.0000; aMatrix_A[3,7] := 0.0850;
    aMatrix_A[4,0] :=-0.0450; aMatrix_A[4,1] :=-0.0150; aMatrix_A[4,2] :=-0.0220; aMatrix_A[4,3] :=-0.0650; aMatrix_A[4,4] := 0.9650; aMatrix_A[4,5] := 0.0000; aMatrix_A[4,6] := 0.0000; aMatrix_A[4,7] := 0.1450;
    aMatrix_A[5,0] := 0.0000; aMatrix_A[5,1] := 0.0035; aMatrix_A[5,2] := 0.0042; aMatrix_A[5,3] := 0.0000; aMatrix_A[5,4] := 0.0000; aMatrix_A[5,5] := 0.9920; aMatrix_A[5,6] := 0.0000; aMatrix_A[5,7] := 0.0000;
    aMatrix_A[6,0] := 0.0000; aMatrix_A[6,1] := 0.0012; aMatrix_A[6,2] :=-0.0028; aMatrix_A[6,3] := 0.0000; aMatrix_A[6,4] := 0.0000; aMatrix_A[6,5] :=-0.0015; aMatrix_A[6,6] := 0.9880; aMatrix_A[6,7] := 0.0000;
    aMatrix_A[7,0] :=-0.0008; aMatrix_A[7,1] :=-0.0004; aMatrix_A[7,2] :=-0.0002; aMatrix_A[7,3] :=-0.0035; aMatrix_A[7,4] := 0.0000; aMatrix_A[7,5] := 0.0000; aMatrix_A[7,6] := 0.0000; aMatrix_A[7,7] := 0.9780;

    (* ----------------------------------------------------------------------------------------- *)
    (* Discrete Input Coupling Matrix B (8x6)                                                    *)
    (* Inputs:                                                                                   *)
    (* u0: Delta W_feed [t/h]                                                                    *)
    (* u1: Delta Q_water [m3/h]                                                                  *)
    (* u2: Delta N_mill [RPM]                                                                    *)
    (* u3: Delta N_pump [RPM]                                                                    *)
    (* u4: Delta V_water_sump [%]                                                                *)
    (* u5: Delta N_cyc [count]                                                                   *)
    (* ----------------------------------------------------------------------------------------- *)
    aMatrix_B[0,0] := 0.00278; aMatrix_B[0,1] := 0.00000; aMatrix_B[0,2] :=-0.0450; aMatrix_B[0,3] := 0.0000; aMatrix_B[0,4] := 0.0000; aMatrix_B[0,5] := 0.0000;
    aMatrix_B[1,0] := 0.00000; aMatrix_B[1,1] := 0.00000; aMatrix_B[1,2] := 0.0380; aMatrix_B[1,3] := 0.0000; aMatrix_B[1,4] := 0.0000; aMatrix_B[1,5] := 0.0000;
    aMatrix_B[2,0] := 0.00000; aMatrix_B[2,1] := 0.00278; aMatrix_B[2,2] :=-0.0150; aMatrix_B[2,3] := 0.0000; aMatrix_B[2,4] := 0.0000; aMatrix_B[2,5] := 0.0000;
    aMatrix_B[3,0] := 0.00450; aMatrix_B[3,1] :=-0.00250; aMatrix_B[3,2] := 0.1250; aMatrix_B[3,3] := 0.0000; aMatrix_B[3,4] := 0.0000; aMatrix_B[3,5] := 0.0000;
    aMatrix_B[4,0] :=-0.00850; aMatrix_B[4,1] :=-0.00350; aMatrix_B[4,2] := 0.1850; aMatrix_B[4,3] := 0.0000; aMatrix_B[4,4] := 0.0000; aMatrix_B[4,5] := 0.0000;
    aMatrix_B[5,0] := 0.00000; aMatrix_B[5,1] := 0.00000; aMatrix_B[5,2] := 0.0000; aMatrix_B[5,3] :=-0.0042; aMatrix_B[5,4] := 0.0035; aMatrix_B[5,5] := 0.0000;
    aMatrix_B[6,0] := 0.00000; aMatrix_B[6,1] := 0.00000; aMatrix_B[6,2] := 0.0000; aMatrix_B[6,3] := 0.0018; aMatrix_B[6,4] :=-0.0045; aMatrix_B[6,5] :=-0.0012;
    aMatrix_B[7,0] :=-0.00025; aMatrix_B[7,1] := 0.00000; aMatrix_B[7,2] := 0.0850; aMatrix_B[7,3] := 0.0000; aMatrix_B[7,4] := 0.0000; aMatrix_B[7,5] := 0.0000;

    (* ----------------------------------------------------------------------------------------- *)
    (* Output Mapping Matrix C (8x8 Identity / Linear Mapping)                                    *)
    (* ----------------------------------------------------------------------------------------- *)
    FOR iIdx := 0 TO 7 DO
        FOR jIdx := 0 TO 7 DO
            IF iIdx = jIdx THEN
                aMatrix_C[iIdx, jIdx] := 1.0;
            ELSE
                aMatrix_C[iIdx, jIdx] := 0.0;
            END_IF;
        END_FOR;
    END_FOR;

    (* ----------------------------------------------------------------------------------------- *)
    (* Direct Feedthrough Matrix D (8x6 All Zeros for Strictly Proper Plant)                     *)
    (* ----------------------------------------------------------------------------------------- *)
    FOR iIdx := 0 TO 7 DO
        FOR jIdx := 0 TO 5 DO
            aMatrix_D[iIdx, jIdx] := 0.0;
        END_FOR;
    END_FOR;

    (* ----------------------------------------------------------------------------------------- *)
    (* Disturbance Coupling Matrix E (8x3)                                                       *)
    (* Disturbances: d0: Hardness Delta A*b, d1: Pebble recycle Delta W_peb, d2: Top size Delta F80*)
    (* ----------------------------------------------------------------------------------------- *)
    aMatrix_E[0,0] :=-0.0450; aMatrix_E[0,1] := 0.00278; aMatrix_E[0,2] := 0.0185;
    aMatrix_E[1,0] := 0.0380; aMatrix_E[1,1] := 0.00000; aMatrix_E[1,2] :=-0.0120;
    aMatrix_E[2,0] := 0.0000; aMatrix_E[2,1] := 0.00000; aMatrix_E[2,2] := 0.0000;
    aMatrix_E[3,0] := 0.0850; aMatrix_E[3,1] := 0.00450; aMatrix_E[3,2] := 0.0240;
    aMatrix_E[4,0] := 0.1250; aMatrix_E[4,1] :=-0.00850; aMatrix_E[4,2] := 0.0650;
    aMatrix_E[5,0] := 0.0000; aMatrix_E[5,1] := 0.00000; aMatrix_E[5,2] := 0.0000;
    aMatrix_E[6,0] := 0.0000; aMatrix_E[6,1] := 0.00000; aMatrix_E[6,2] := 0.0000;
    aMatrix_E[7,0] :=-0.0045; aMatrix_E[7,1] :=-0.00050; aMatrix_E[7,2] :=-0.0018;

    (* ----------------------------------------------------------------------------------------- *)
    (* Kalman Observer Innovation Gain Matrix K_obs (8x8 Diagonal Pre-Filtered Form)             *)
    (* ----------------------------------------------------------------------------------------- *)
    FOR iIdx := 0 TO 7 DO
        FOR jIdx := 0 TO 7 DO
            IF iIdx = jIdx THEN
                CASE iIdx OF
                    0: aMatrix_K_obs[iIdx, jIdx] := 0.0850;
                    1: aMatrix_K_obs[iIdx, jIdx] := 0.0750;
                    2: aMatrix_K_obs[iIdx, jIdx] := 0.0920;
                    3: aMatrix_K_obs[iIdx, jIdx] := 0.1450;
                    4: aMatrix_K_obs[iIdx, jIdx] := 0.1850;
                    5: aMatrix_K_obs[iIdx, jIdx] := 0.1100;
                    6: aMatrix_K_obs[iIdx, jIdx] := 0.1250;
                    7: aMatrix_K_obs[iIdx, jIdx] := 0.0650;
                END_CASE;
            ELSE
                aMatrix_K_obs[iIdx, jIdx] := 0.0;
            END_IF;
        END_FOR;
    END_FOR;

    (* ----------------------------------------------------------------------------------------- *)
    (* Terminal Riccati Cost Matrix P (8x8 Diagonal Solution)                                    *)
    (* ----------------------------------------------------------------------------------------- *)
    FOR iIdx := 0 TO 7 DO
        FOR jIdx := 0 TO 7 DO
            IF iIdx = jIdx THEN
                CASE iIdx OF
                    0: aMatrix_P[iIdx, jIdx] := 3.450;
                    1: aMatrix_P[iIdx, jIdx] := 2.850;
                    2: aMatrix_P[iIdx, jIdx] := 4.200;
                    3: aMatrix_P[iIdx, jIdx] := 8.500;
                    4: aMatrix_P[iIdx, jIdx] := 28.50;
                    5: aMatrix_P[iIdx, jIdx] := 4.800;
                    6: aMatrix_P[iIdx, jIdx] := 16.50;
                    7: aMatrix_P[iIdx, jIdx] := 6.200;
                END_CASE;
            ELSE
                aMatrix_P[iIdx, jIdx] := 0.0;
            END_IF;
        END_FOR;
    END_FOR;

    bFirstScanDone := TRUE;
END_IF;
"""

print("Init module loaded.")
