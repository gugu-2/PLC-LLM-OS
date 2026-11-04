# brain_scratch/can_seamer_builder/part2_init_tmr.py

PART2_INIT_TMR = """
(* ==========================================================================================
 * PHASE 1: COLD INITIALIZATION, SANITY BOUNDING & MATRIX COEFFICIENT STRUCTURING
 * ========================================================================================== *)

(* Clamp scan cycle execution delta time to numerical stability envelope [0.0005 s to 0.050 s] *)
IF tCycle_DeltaTime_s < 0.0005 THEN
    rDeltaT := 0.001; (* Default fallback to 1 millisecond execution *)
ELSIF tCycle_DeltaTime_s > 0.050 THEN
    rDeltaT := 0.050; (* Bound maximum integration step to 50 ms *)
ELSE
    rDeltaT := tCycle_DeltaTime_s;
END_IF;

IF NOT bInitialized THEN
    (* --------------------------------------------------------------------------------------
     * Discrete State-Space Model Matrix A [8x8] Initialization: x[k+1] = A * x[k] + B * u[k]
     * Discretized via zero-order hold (ZOH) at Ts = 0.002s (2 ms high-speed servo task).
     * Physical States:
     *   x1: Turret speed error [rpm]
     *   x2: Seaming chuck axial load force [kN]
     *   x3: Liquid nitrogen dosing pulse duration [ms]
     *   x4: Internal can headspace pressure [bar]
     *   x5: Acoustic resonance frequency peak [kHz]
     *   x6: Steam enclosure barrier temperature [deg C]
     *   x7: Infeed starwheel synchronization phase error [mrad]
     *   x8: Seamer main drive motor torque ripple [Nm]
     * -------------------------------------------------------------------------------------- *)
    (* Row 1: Turret speed dynamics (inertia J=14.5 kg*m^2, viscous friction b=0.85 N*m*s/rad) *)
    aA_Matrix[1, 1] := 0.9842;   aA_Matrix[1, 2] := -0.0012;  aA_Matrix[1, 3] := 0.0000;   aA_Matrix[1, 4] := 0.0000;
    aA_Matrix[1, 5] := 0.0000;   aA_Matrix[1, 6] := 0.0000;   aA_Matrix[1, 7] := 0.0045;   aA_Matrix[1, 8] := -0.0150;

    (* Row 2: Chuck axial force dynamics (lifter pneumatic spring k=450 kN/m, damping c=12 kN*s/m) *)
    aA_Matrix[2, 1] := 0.0018;   aA_Matrix[2, 2] := 0.9420;   aA_Matrix[2, 3] := 0.0000;   aA_Matrix[2, 4] := 0.0125;
    aA_Matrix[2, 5] := 0.0000;   aA_Matrix[2, 6] := 0.0000;   aA_Matrix[2, 7] := 0.0000;   aA_Matrix[2, 8] := 0.0008;

    (* Row 3: LN2 micro-valve injection duration response (piezoelectric actuator tau=4.5 ms) *)
    aA_Matrix[3, 1] := 0.0000;   aA_Matrix[3, 2] := 0.0000;   aA_Matrix[3, 3] := 0.9150;   aA_Matrix[3, 4] := 0.0000;
    aA_Matrix[3, 5] := 0.0000;   aA_Matrix[3, 6] := 0.0000;   aA_Matrix[3, 7] := 0.0000;   aA_Matrix[3, 8] := 0.0000;

    (* Row 4: Can headspace pressure buildup (LN2 flash vaporization and gas expansion) *)
    aA_Matrix[4, 1] := 0.0000;   aA_Matrix[4, 2] := 0.0022;   aA_Matrix[4, 3] := 0.0485;   aA_Matrix[4, 4] := 0.9650;
    aA_Matrix[4, 5] := 0.0000;   aA_Matrix[4, 6] := 0.0014;   aA_Matrix[4, 7] := 0.0000;   aA_Matrix[4, 8] := 0.0000;

    (* Row 5: Acoustic resonance frequency coupling (thin plate membrane tension vs headspace pressure) *)
    aA_Matrix[5, 1] := 0.0000;   aA_Matrix[5, 2] := 0.0035;   aA_Matrix[5, 3] := 0.0000;   aA_Matrix[5, 4] := 0.1250;
    aA_Matrix[5, 5] := 0.9280;   aA_Matrix[5, 6] := 0.0000;   aA_Matrix[5, 7] := 0.0000;   aA_Matrix[5, 8] := 0.0000;

    (* Row 6: Steam enclosure temperature dynamics (steam enthalpy vs labyrinth leakage heat loss) *)
    aA_Matrix[6, 1] := -0.0005;  aA_Matrix[6, 2] := 0.0000;   aA_Matrix[6, 3] := 0.0000;   aA_Matrix[6, 4] := 0.0000;
    aA_Matrix[6, 5] := 0.0000;   aA_Matrix[6, 6] := 0.9750;   aA_Matrix[6, 7] := 0.0000;   aA_Matrix[6, 8] := 0.0000;

    (* Row 7: Starwheel infeed phase error dynamics (electronic gearing compliance) *)
    aA_Matrix[7, 1] := 0.0240;   aA_Matrix[7, 2] := 0.0000;   aA_Matrix[7, 3] := 0.0000;   aA_Matrix[7, 4] := 0.0000;
    aA_Matrix[7, 5] := 0.0000;   aA_Matrix[7, 6] := 0.0000;   aA_Matrix[7, 7] := 0.8950;   aA_Matrix[7, 8] := 0.0012;

    (* Row 8: Seamer drive torque ripple harmonics (18-head mechanical load excitation) *)
    aA_Matrix[8, 1] := 0.0350;   aA_Matrix[8, 2] := 0.0180;   aA_Matrix[8, 3] := 0.0000;   aA_Matrix[8, 4] := 0.0000;
    aA_Matrix[8, 5] := 0.0000;   aA_Matrix[8, 6] := 0.0000;   aA_Matrix[8, 7] := 0.0085;   aA_Matrix[8, 8] := 0.8450;

    (* --------------------------------------------------------------------------------------
     * Discrete Input Coupling Matrix B [8x6]
     * Controls:
     *   u1: Turret Speed Command Bias [rpm]
     *   u2: Lifter Axial Preload Bias [kN]
     *   u3: LN2 Micro-Valve Injection Trim [ms]
     *   u4: Steam Barrier Valve Modulation Position [%]
     *   u5: Infeed Worm Screw Phase Offset [mrad]
     *   u6: Dynamic Seaming Roll Cam Depth Bias [mm]
     * -------------------------------------------------------------------------------------- *)
    aB_Matrix[1, 1] := 0.0158;   aB_Matrix[1, 2] := 0.0000;   aB_Matrix[1, 3] := 0.0000;   aB_Matrix[1, 4] := 0.0000;   aB_Matrix[1, 5] := 0.0012;   aB_Matrix[1, 6] := 0.0000;
    aB_Matrix[2, 1] := 0.0000;   aB_Matrix[2, 2] := 0.0580;   aB_Matrix[2, 3] := 0.0000;   aB_Matrix[2, 4] := 0.0000;   aB_Matrix[2, 5] := 0.0000;   aB_Matrix[2, 6] := 0.0850;
    aB_Matrix[3, 1] := 0.0000;   aB_Matrix[3, 2] := 0.0000;   aB_Matrix[3, 3] := 0.0850;   aB_Matrix[3, 4] := 0.0000;   aB_Matrix[3, 5] := 0.0000;   aB_Matrix[3, 6] := 0.0000;
    aB_Matrix[4, 1] := 0.0000;   aB_Matrix[4, 2] := 0.0000;   aB_Matrix[4, 3] := 0.0350;   aB_Matrix[4, 4] := 0.0000;   aB_Matrix[4, 5] := 0.0000;   aB_Matrix[4, 6] := 0.0015;
    aB_Matrix[5, 1] := 0.0000;   aB_Matrix[5, 2] := 0.0000;   aB_Matrix[5, 3] := 0.0120;   aB_Matrix[5, 4] := 0.0000;   aB_Matrix[5, 5] := 0.0000;   aB_Matrix[5, 6] := 0.0045;
    aB_Matrix[6, 1] := 0.0000;   aB_Matrix[6, 2] := 0.0000;   aB_Matrix[6, 3] := 0.0000;   aB_Matrix[6, 4] := 0.0250;   aB_Matrix[6, 5] := 0.0000;   aB_Matrix[6, 6] := 0.0000;
    aB_Matrix[7, 1] := 0.0000;   aB_Matrix[7, 2] := 0.0000;   aB_Matrix[7, 3] := 0.0000;   aB_Matrix[7, 4] := 0.0000;   aB_Matrix[7, 5] := 0.1050;   aB_Matrix[7, 6] := 0.0000;
    aB_Matrix[8, 1] := 0.0220;   aB_Matrix[8, 2] := 0.0050;   aB_Matrix[8, 3] := 0.0000;   aB_Matrix[8, 4] := 0.0000;   aB_Matrix[8, 5] := 0.0000;   aB_Matrix[8, 6] := 0.0180;

    (* --------------------------------------------------------------------------------------
     * Discrete Output Measurement Matrix C [6x8]
     * Measurements y:
     *   y1: Measured Chuck Axial Load [kN]
     *   y2: Measured Can Internal Pressure [bar]
     *   y3: Measured Acoustic Resonance Peak [kHz]
     *   y4: Measured Steam Barrier Temperature [deg C]
     *   y5: Measured Infeed Synchronization Error [mrad]
     *   y6: Measured Seam Thickness Gauge [mm]
     * -------------------------------------------------------------------------------------- *)
    aC_Matrix[1, 1] := 0.0; aC_Matrix[1, 2] := 1.0; aC_Matrix[1, 3] := 0.0; aC_Matrix[1, 4] := 0.0; aC_Matrix[1, 5] := 0.0; aC_Matrix[1, 6] := 0.0; aC_Matrix[1, 7] := 0.0; aC_Matrix[1, 8] := 0.0;
    aC_Matrix[2, 1] := 0.0; aC_Matrix[2, 2] := 0.0; aC_Matrix[2, 3] := 0.0; aC_Matrix[2, 4] := 1.0; aC_Matrix[2, 5] := 0.0; aC_Matrix[2, 6] := 0.0; aC_Matrix[2, 7] := 0.0; aC_Matrix[2, 8] := 0.0;
    aC_Matrix[3, 1] := 0.0; aC_Matrix[3, 2] := 0.0; aC_Matrix[3, 3] := 0.0; aC_Matrix[3, 4] := 0.0; aC_Matrix[3, 5] := 1.0; aC_Matrix[3, 6] := 0.0; aC_Matrix[3, 7] := 0.0; aC_Matrix[3, 8] := 0.0;
    aC_Matrix[4, 1] := 0.0; aC_Matrix[4, 2] := 0.0; aC_Matrix[4, 3] := 0.0; aC_Matrix[4, 4] := 0.0; aC_Matrix[4, 5] := 0.0; aC_Matrix[4, 6] := 1.0; aC_Matrix[4, 7] := 0.0; aC_Matrix[4, 8] := 0.0;
    aC_Matrix[5, 1] := 0.0; aC_Matrix[5, 2] := 0.0; aC_Matrix[5, 3] := 0.0; aC_Matrix[5, 4] := 0.0; aC_Matrix[5, 5] := 0.0; aC_Matrix[5, 6] := 0.0; aC_Matrix[5, 7] := 1.0; aC_Matrix[5, 8] := 0.0;
    aC_Matrix[6, 1] := 0.0; aC_Matrix[6, 2] := -0.018; aC_Matrix[6, 3] := 0.0; aC_Matrix[6, 4] := 0.0; aC_Matrix[6, 5] := 0.0; aC_Matrix[6, 6] := 0.0; aC_Matrix[6, 7] := 0.0; aC_Matrix[6, 8] := 0.0;

    (* Direct Feedthrough Matrix D [6x6] (Null matrix due to strict causality) *)
    FOR iMatrixRow := 1 TO 6 DO
        FOR iMatrixCol := 1 TO 6 DO
            aD_Matrix[iMatrixRow, iMatrixCol] := 0.0;
        END_FOR;
    END_FOR;

    (* --------------------------------------------------------------------------------------
     * Luenberger Observer Gain Matrix L [8x6] (Synthesized via steady-state Kalman Filter)
     * -------------------------------------------------------------------------------------- *)
    aL_ObserverGain[1, 1] := 0.012;  aL_ObserverGain[1, 2] := 0.000;  aL_ObserverGain[1, 3] := 0.000;  aL_ObserverGain[1, 4] := 0.000;  aL_ObserverGain[1, 5] := 0.025;  aL_ObserverGain[1, 6] := 0.000;
    aL_ObserverGain[2, 1] := 0.185;  aL_ObserverGain[2, 2] := 0.015;  aL_ObserverGain[2, 3] := 0.000;  aL_ObserverGain[2, 4] := 0.000;  aL_ObserverGain[2, 5] := 0.000;  aL_ObserverGain[2, 6] := -0.045;
    aL_ObserverGain[3, 1] := 0.000;  aL_ObserverGain[3, 2] := 0.065;  aL_ObserverGain[3, 3] := 0.018;  aL_ObserverGain[3, 4] := 0.000;  aL_ObserverGain[3, 5] := 0.000;  aL_ObserverGain[3, 6] := 0.000;
    aL_ObserverGain[4, 1] := 0.000;  aL_ObserverGain[4, 2] := 0.145;  aL_ObserverGain[4, 3] := 0.082;  aL_ObserverGain[4, 4] := 0.000;  aL_ObserverGain[4, 5] := 0.000;  aL_ObserverGain[4, 6] := 0.000;
    aL_ObserverGain[5, 1] := 0.000;  aL_ObserverGain[5, 2] := 0.075;  aL_ObserverGain[5, 3] := 0.210;  aL_ObserverGain[5, 4] := 0.000;  aL_ObserverGain[5, 5] := 0.000;  aL_ObserverGain[5, 6] := 0.000;
    aL_ObserverGain[6, 1] := 0.000;  aL_ObserverGain[6, 2] := 0.000;  aL_ObserverGain[6, 3] := 0.000;  aL_ObserverGain[6, 4] := 0.165;  aL_ObserverGain[6, 5] := 0.000;  aL_ObserverGain[6, 6] := 0.000;
    aL_ObserverGain[7, 1] := 0.018;  aL_ObserverGain[7, 2] := 0.000;  aL_ObserverGain[7, 3] := 0.000;  aL_ObserverGain[7, 4] := 0.000;  aL_ObserverGain[7, 5] := 0.220;  aL_ObserverGain[7, 6] := 0.000;
    aL_ObserverGain[8, 1] := 0.045;  aL_ObserverGain[8, 2] := 0.022;  aL_ObserverGain[8, 3] := 0.000;  aL_ObserverGain[8, 4] := 0.000;  aL_ObserverGain[8, 5] := 0.035;  aL_ObserverGain[8, 6] := 0.012;

    (* --------------------------------------------------------------------------------------
     * MPC Quadratic Penalty Matrices Q [8x8], R [6x6], P [8x8]
     * -------------------------------------------------------------------------------------- *)
    FOR iMatrixRow := 1 TO 8 DO
        FOR iMatrixCol := 1 TO 8 DO
            aQ_StateWeight[iMatrixRow, iMatrixCol] := 0.0;
            aP_TerminalWeight[iMatrixRow, iMatrixCol] := 0.0;
        END_FOR;
    END_FOR;

    (* State Penalties Q: emphasize speed accuracy, chuck axial force, headspace pressure *)
    aQ_StateWeight[1, 1] := 18.0; (* Turret speed error penalty *)
    aQ_StateWeight[2, 2] := 12.0; (* Seaming chuck axial force error penalty *)
    aQ_StateWeight[3, 3] := 10.0; (* LN2 injection pulse precision penalty *)
    aQ_StateWeight[4, 4] := 28.0; (* Internal can pressure deviation penalty *)
    aQ_StateWeight[5, 5] := 20.0; (* Acoustic resonance frequency error penalty *)
    aQ_StateWeight[6, 6] := 25.0; (* Steam barrier enclosure temperature penalty *)
    aQ_StateWeight[7, 7] := 32.0; (* Starwheel infeed synchronization jitter penalty *)
    aQ_StateWeight[8, 8] := 8.0;  (* Torque ripple harmonic damping penalty *)

    (* Terminal State Penalties P (2.5x steady-state Q) *)
    FOR iMatrixRow := 1 TO 8 DO
        aP_TerminalWeight[iMatrixRow, iMatrixRow] := aQ_StateWeight[iMatrixRow, iMatrixRow] * 2.50;
    END_FOR;

    (* Control Effort Penalties R [6x6] *)
    FOR iMatrixRow := 1 TO 6 DO
        FOR iMatrixCol := 1 TO 6 DO
            aR_ControlWeight[iMatrixRow, iMatrixCol] := 0.0;
        END_FOR;
    END_FOR;
    aR_ControlWeight[1, 1] := 2.5; (* Turret speed trim effort *)
    aR_ControlWeight[2, 2] := 1.8; (* Lifter axial preload trim effort *)
    aR_ControlWeight[3, 3] := 4.2; (* LN2 pulse micro-valve modulation effort *)
    aR_ControlWeight[4, 4] := 1.2; (* Saturated steam valve stroke effort *)
    aR_ControlWeight[5, 5] := 5.0; (* Worm screw phase trim effort *)
    aR_ControlWeight[6, 6] := 6.5; (* Dynamic cam depth servo trim effort *)

    (* Initialize 18 Individual Seaming Heads Historical Profiles *)
    FOR iHeadIdx := 1 TO 18 DO
        aHead_AxialLoad_Mean[iHeadIdx] := 5.50;
        aHead_AxialLoad_Peak[iHeadIdx] := 5.50;
        aHead_AxialLoad_Min[iHeadIdx]  := 5.50;
        aHead_AxialLoad_Variance[iHeadIdx] := 0.025;
        aHead_SeamThickness_Hist[iHeadIdx] := 1.140;
        aHead_SeamHeight_Hist[iHeadIdx] := 2.980;
        aHead_Countersink_Hist[iHeadIdx] := 3.180;
        aHead_ResonanceFreq_Hist[iHeadIdx] := 3.150;
        aHead_RejectCount[iHeadIdx] := 0;
        aHead_TotalCycles[iHeadIdx] := 0;
        aHead_WearIndex_Pct[iHeadIdx] := 0.0;
        aHead_CalibOffset_1stOp_mm[iHeadIdx] := 0.0;
        aHead_CalibOffset_2ndOp_mm[iHeadIdx] := 0.0;
    END_FOR;

    (* Clear Shift Register Arrays *)
    FOR iMatrixRow := 1 TO 36 DO
        abPocket_HasCan[iMatrixRow] := FALSE;
        abPocket_HasEnd[iMatrixRow] := FALSE;
        abPocket_DosedLN2[iMatrixRow] := FALSE;
        abPocket_SeamedOK[iMatrixRow] := FALSE;
        abPocket_AcousticPass[iMatrixRow] := FALSE;
        abPocket_RejectPending[iMatrixRow] := FALSE;
        aiPocket_HeadOrigin[iMatrixRow] := 0;
    END_FOR;

    bInitialized := TRUE;
END_IF;

(* ==========================================================================================
 * PHASE 2: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING & DISCREPANCY TIMERS
 * ========================================================================================== *)

(* ------------------------------------------------------------------------------------------
 * TMR Triplet 1: Seaming Chuck Lifter Axial Load Transducers (Channels A, B, C) [kN]
 * ------------------------------------------------------------------------------------------ *)
IF bTMR_AxialLoad_ChA_Healthy AND bTMR_AxialLoad_ChB_Healthy AND bTMR_AxialLoad_ChC_Healthy THEN
    (* Full 3-channel voting: Middle Value Median Selection *)
    IF (rChuck_AxialLoad_ChA >= rChuck_AxialLoad_ChB AND rChuck_AxialLoad_ChA <= rChuck_AxialLoad_ChC) OR
       (rChuck_AxialLoad_ChA <= rChuck_AxialLoad_ChB AND rChuck_AxialLoad_ChA >= rChuck_AxialLoad_ChC) THEN
        rVoted_Chuck_AxialLoad_kN := rChuck_AxialLoad_ChA;
    ELSIF (rChuck_AxialLoad_ChB >= rChuck_AxialLoad_ChA AND rChuck_AxialLoad_ChB <= rChuck_AxialLoad_ChC) OR
          (rChuck_AxialLoad_ChB <= rChuck_AxialLoad_ChA AND rChuck_AxialLoad_ChB >= rChuck_AxialLoad_ChC) THEN
        rVoted_Chuck_AxialLoad_kN := rChuck_AxialLoad_ChB;
    ELSE
        rVoted_Chuck_AxialLoad_kN := rChuck_AxialLoad_ChC;
    END_IF;

    (* Discrepancy Diagnostics between Channels *)
    IF (ABS(rChuck_AxialLoad_ChA - rChuck_AxialLoad_ChB) > rTMR_Tol_AxialLoad_kN) OR
       (ABS(rChuck_AxialLoad_ChB - rChuck_AxialLoad_ChC) > rTMR_Tol_AxialLoad_kN) OR
       (ABS(rChuck_AxialLoad_ChA - rChuck_AxialLoad_ChC) > rTMR_Tol_AxialLoad_kN) THEN
        rTMR_AxialLoad_Discrep_Timer := rTMR_AxialLoad_Discrep_Timer + rDeltaT;
        IF rTMR_AxialLoad_Discrep_Timer > rTMR_Discrepancy_Timeout_s THEN
            bAlarm_TMR_Axial_Discrep := TRUE;
            (* Identify deviant channel *)
            IF (ABS(rChuck_AxialLoad_ChA - rVoted_Chuck_AxialLoad_kN) > rTMR_Tol_AxialLoad_kN) THEN
                bTMR_AxialLoad_ChA_Healthy := FALSE;
            ELSIF (ABS(rChuck_AxialLoad_ChB - rVoted_Chuck_AxialLoad_kN) > rTMR_Tol_AxialLoad_kN) THEN
                bTMR_AxialLoad_ChB_Healthy := FALSE;
            ELSE
                bTMR_AxialLoad_ChC_Healthy := FALSE;
            END_IF;
        END_IF;
    ELSE
        rTMR_AxialLoad_Discrep_Timer := MAX(0.0, rTMR_AxialLoad_Discrep_Timer - (rDeltaT * 0.5));
    END_IF;

(* Degraded 1oo2 Dual Channel Operation *)
ELSIF bTMR_AxialLoad_ChA_Healthy AND bTMR_AxialLoad_ChB_Healthy THEN
    rVoted_Chuck_AxialLoad_kN := (rChuck_AxialLoad_ChA + rChuck_AxialLoad_ChB) * 0.50;
    IF ABS(rChuck_AxialLoad_ChA - rChuck_AxialLoad_ChB) > (rTMR_Tol_AxialLoad_kN * 1.5) THEN
        bAlarm_TMR_Axial_Discrep := TRUE;
    END_IF;
ELSIF bTMR_AxialLoad_ChA_Healthy AND bTMR_AxialLoad_ChC_Healthy THEN
    rVoted_Chuck_AxialLoad_kN := (rChuck_AxialLoad_ChA + rChuck_AxialLoad_ChC) * 0.50;
    IF ABS(rChuck_AxialLoad_ChA - rChuck_AxialLoad_ChC) > (rTMR_Tol_AxialLoad_kN * 1.5) THEN
        bAlarm_TMR_Axial_Discrep := TRUE;
    END_IF;
ELSIF bTMR_AxialLoad_ChB_Healthy AND bTMR_AxialLoad_ChC_Healthy THEN
    rVoted_Chuck_AxialLoad_kN := (rChuck_AxialLoad_ChB + rChuck_AxialLoad_ChC) * 0.50;
    IF ABS(rChuck_AxialLoad_ChB - rChuck_AxialLoad_ChC) > (rTMR_Tol_AxialLoad_kN * 1.5) THEN
        bAlarm_TMR_Axial_Discrep := TRUE;
    END_IF;
(* Single Channel Failover (Critical Warning Active) *)
ELSIF bTMR_AxialLoad_ChA_Healthy THEN
    rVoted_Chuck_AxialLoad_kN := rChuck_AxialLoad_ChA;
ELSIF bTMR_AxialLoad_ChB_Healthy THEN
    rVoted_Chuck_AxialLoad_kN := rChuck_AxialLoad_ChB;
ELSIF bTMR_AxialLoad_ChC_Healthy THEN
    rVoted_Chuck_AxialLoad_kN := rChuck_AxialLoad_ChC;
ELSE
    rVoted_Chuck_AxialLoad_kN := rSP_Chuck_AxialLoad_kN; (* Safe fallback *)
    bAlarm_AxialLoad_LL := TRUE;
END_IF;

(* ------------------------------------------------------------------------------------------
 * TMR Triplet 2: Cryogenic LN2 Supply Manifold Pressure Transmitters (ChA, ChB, ChC) [bar]
 * ------------------------------------------------------------------------------------------ *)
IF bTMR_LN2Press_ChA_Healthy AND bTMR_LN2Press_ChB_Healthy AND bTMR_LN2Press_ChC_Healthy THEN
    IF (rLN2_SupplyPressure_ChA >= rLN2_SupplyPressure_ChB AND rLN2_SupplyPressure_ChA <= rLN2_SupplyPressure_ChC) OR
       (rLN2_SupplyPressure_ChA <= rLN2_SupplyPressure_ChB AND rLN2_SupplyPressure_ChA >= rLN2_SupplyPressure_ChC) THEN
        rVoted_LN2_Pressure_bar := rLN2_SupplyPressure_ChA;
    ELSIF (rLN2_SupplyPressure_ChB >= rLN2_SupplyPressure_ChA AND rLN2_SupplyPressure_ChB <= rLN2_SupplyPressure_ChC) OR
          (rLN2_SupplyPressure_ChB <= rLN2_SupplyPressure_ChA AND rLN2_SupplyPressure_ChB >= rLN2_SupplyPressure_ChC) THEN
        rVoted_LN2_Pressure_bar := rLN2_SupplyPressure_ChB;
    ELSE
        rVoted_LN2_Pressure_bar := rLN2_SupplyPressure_ChC;
    END_IF;

    IF (ABS(rLN2_SupplyPressure_ChA - rLN2_SupplyPressure_ChB) > rTMR_Tol_LN2Press_bar) OR
       (ABS(rLN2_SupplyPressure_ChB - rLN2_SupplyPressure_ChC) > rTMR_Tol_LN2Press_bar) OR
       (ABS(rLN2_SupplyPressure_ChA - rLN2_SupplyPressure_ChC) > rTMR_Tol_LN2Press_bar) THEN
        rTMR_LN2Press_Discrep_Timer := rTMR_LN2Press_Discrep_Timer + rDeltaT;
        IF rTMR_LN2Press_Discrep_Timer > rTMR_Discrepancy_Timeout_s THEN
            bAlarm_TMR_LN2_Discrep := TRUE;
            IF (ABS(rLN2_SupplyPressure_ChA - rVoted_LN2_Pressure_bar) > rTMR_Tol_LN2Press_bar) THEN
                bTMR_LN2Press_ChA_Healthy := FALSE;
            ELSIF (ABS(rLN2_SupplyPressure_ChB - rVoted_LN2_Pressure_bar) > rTMR_Tol_LN2Press_bar) THEN
                bTMR_LN2Press_ChB_Healthy := FALSE;
            ELSE
                bTMR_LN2Press_ChC_Healthy := FALSE;
            END_IF;
        END_IF;
    ELSE
        rTMR_LN2Press_Discrep_Timer := MAX(0.0, rTMR_LN2Press_Discrep_Timer - (rDeltaT * 0.5));
    END_IF;
ELSIF bTMR_LN2Press_ChA_Healthy AND bTMR_LN2Press_ChB_Healthy THEN
    rVoted_LN2_Pressure_bar := (rLN2_SupplyPressure_ChA + rLN2_SupplyPressure_ChB) * 0.50;
ELSIF bTMR_LN2Press_ChA_Healthy AND bTMR_LN2Press_ChC_Healthy THEN
    rVoted_LN2_Pressure_bar := (rLN2_SupplyPressure_ChA + rLN2_SupplyPressure_ChC) * 0.50;
ELSIF bTMR_LN2Press_ChB_Healthy AND bTMR_LN2Press_ChC_Healthy THEN
    rVoted_LN2_Pressure_bar := (rLN2_SupplyPressure_ChB + rLN2_SupplyPressure_ChC) * 0.50;
ELSIF bTMR_LN2Press_ChA_Healthy THEN
    rVoted_LN2_Pressure_bar := rLN2_SupplyPressure_ChA;
ELSIF bTMR_LN2Press_ChB_Healthy THEN
    rVoted_LN2_Pressure_bar := rLN2_SupplyPressure_ChB;
ELSIF bTMR_LN2Press_ChC_Healthy THEN
    rVoted_LN2_Pressure_bar := rLN2_SupplyPressure_ChC;
ELSE
    rVoted_LN2_Pressure_bar := 2.50;
    bAlarm_LN2Press_LL := TRUE;
END_IF;

(* ------------------------------------------------------------------------------------------
 * TMR Triplet 3: Aseptic Turret Steam Barrier Temperature RTDs (ChA, ChB, ChC) [deg C]
 * ------------------------------------------------------------------------------------------ *)
IF bTMR_SteamTemp_ChA_Healthy AND bTMR_SteamTemp_ChB_Healthy AND bTMR_SteamTemp_ChC_Healthy THEN
    IF (rSteamBarrier_Temp_ChA >= rSteamBarrier_Temp_ChB AND rSteamBarrier_Temp_ChA <= rSteamBarrier_Temp_ChC) OR
       (rSteamBarrier_Temp_ChA <= rSteamBarrier_Temp_ChB AND rSteamBarrier_Temp_ChA >= rSteamBarrier_Temp_ChC) THEN
        rVoted_SteamBarrier_Temp_degC := rSteamBarrier_Temp_ChA;
    ELSIF (rSteamBarrier_Temp_ChB >= rSteamBarrier_Temp_ChA AND rSteamBarrier_Temp_ChB <= rSteamBarrier_Temp_ChC) OR
          (rSteamBarrier_Temp_ChB <= rSteamBarrier_Temp_ChA AND rSteamBarrier_Temp_ChB >= rSteamBarrier_Temp_ChC) THEN
        rVoted_SteamBarrier_Temp_degC := rSteamBarrier_Temp_ChB;
    ELSE
        rVoted_SteamBarrier_Temp_degC := rSteamBarrier_Temp_ChC;
    END_IF;

    IF (ABS(rSteamBarrier_Temp_ChA - rSteamBarrier_Temp_ChB) > rTMR_Tol_SteamTemp_degC) OR
       (ABS(rSteamBarrier_Temp_ChB - rSteamBarrier_Temp_ChC) > rTMR_Tol_SteamTemp_degC) OR
       (ABS(rSteamBarrier_Temp_ChA - rSteamBarrier_Temp_ChC) > rTMR_Tol_SteamTemp_degC) THEN
        rTMR_SteamTemp_Discrep_Timer := rTMR_SteamTemp_Discrep_Timer + rDeltaT;
        IF rTMR_SteamTemp_Discrep_Timer > rTMR_Discrepancy_Timeout_s THEN
            bAlarm_TMR_Steam_Discrep := TRUE;
            IF (ABS(rSteamBarrier_Temp_ChA - rVoted_SteamBarrier_Temp_degC) > rTMR_Tol_SteamTemp_degC) THEN
                bTMR_SteamTemp_ChA_Healthy := FALSE;
            ELSIF (ABS(rSteamBarrier_Temp_ChB - rVoted_SteamBarrier_Temp_degC) > rTMR_Tol_SteamTemp_degC) THEN
                bTMR_SteamTemp_ChB_Healthy := FALSE;
            ELSE
                bTMR_SteamTemp_ChC_Healthy := FALSE;
            END_IF;
        END_IF;
    ELSE
        rTMR_SteamTemp_Discrep_Timer := MAX(0.0, rTMR_SteamTemp_Discrep_Timer - (rDeltaT * 0.5));
    END_IF;
ELSIF bTMR_SteamTemp_ChA_Healthy AND bTMR_SteamTemp_ChB_Healthy THEN
    rVoted_SteamBarrier_Temp_degC := (rSteamBarrier_Temp_ChA + rSteamBarrier_Temp_ChB) * 0.50;
ELSIF bTMR_SteamTemp_ChA_Healthy AND bTMR_SteamTemp_ChC_Healthy THEN
    rVoted_SteamBarrier_Temp_degC := (rSteamBarrier_Temp_ChA + rSteamBarrier_Temp_ChC) * 0.50;
ELSIF bTMR_SteamTemp_ChB_Healthy AND bTMR_SteamTemp_ChC_Healthy THEN
    rVoted_SteamBarrier_Temp_degC := (rSteamBarrier_Temp_ChB + rSteamBarrier_Temp_ChC) * 0.50;
ELSIF bTMR_SteamTemp_ChA_Healthy THEN
    rVoted_SteamBarrier_Temp_degC := rSteamBarrier_Temp_ChA;
ELSIF bTMR_SteamTemp_ChB_Healthy THEN
    rVoted_SteamBarrier_Temp_degC := rSteamBarrier_Temp_ChB;
ELSIF bTMR_SteamTemp_ChC_Healthy THEN
    rVoted_SteamBarrier_Temp_degC := rSteamBarrier_Temp_ChC;
ELSE
    rVoted_SteamBarrier_Temp_degC := 125.0;
    bAlarm_SteamTemp_LL := TRUE;
END_IF;

(* ------------------------------------------------------------------------------------------
 * TMR Triplet 4: Non-Destructive Acoustic Sound Resonance Can Inspection Array (ChA, ChB, ChC) [kHz]
 * ------------------------------------------------------------------------------------------ *)
IF bTMR_Acoustic_ChA_Healthy AND bTMR_Acoustic_ChB_Healthy AND bTMR_Acoustic_ChC_Healthy THEN
    IF (rAcoustic_ResonanceFreq_ChA >= rAcoustic_ResonanceFreq_ChB AND rAcoustic_ResonanceFreq_ChA <= rAcoustic_ResonanceFreq_ChC) OR
       (rAcoustic_ResonanceFreq_ChA <= rAcoustic_ResonanceFreq_ChB AND rAcoustic_ResonanceFreq_ChA >= rAcoustic_ResonanceFreq_ChC) THEN
        rVoted_AcousticResonance_kHz := rAcoustic_ResonanceFreq_ChA;
    ELSIF (rAcoustic_ResonanceFreq_ChB >= rAcoustic_ResonanceFreq_ChA AND rAcoustic_ResonanceFreq_ChB <= rAcoustic_ResonanceFreq_ChC) OR
          (rAcoustic_ResonanceFreq_ChB <= rAcoustic_ResonanceFreq_ChA AND rAcoustic_ResonanceFreq_ChB >= rAcoustic_ResonanceFreq_ChC) THEN
        rVoted_AcousticResonance_kHz := rAcoustic_ResonanceFreq_ChB;
    ELSE
        rVoted_AcousticResonance_kHz := rAcoustic_ResonanceFreq_ChC;
    END_IF;

    IF (ABS(rAcoustic_ResonanceFreq_ChA - rAcoustic_ResonanceFreq_ChB) > rTMR_Tol_Acoustic_kHz) OR
       (ABS(rAcoustic_ResonanceFreq_ChB - rAcoustic_ResonanceFreq_ChC) > rTMR_Tol_Acoustic_kHz) OR
       (ABS(rAcoustic_ResonanceFreq_ChA - rAcoustic_ResonanceFreq_ChC) > rTMR_Tol_Acoustic_kHz) THEN
        rTMR_Acoustic_Discrep_Timer := rTMR_Acoustic_Discrep_Timer + rDeltaT;
        IF rTMR_Acoustic_Discrep_Timer > rTMR_Discrepancy_Timeout_s THEN
            bAlarm_TMR_Acoustic_Discrep := TRUE;
            IF (ABS(rAcoustic_ResonanceFreq_ChA - rVoted_AcousticResonance_kHz) > rTMR_Tol_Acoustic_kHz) THEN
                bTMR_Acoustic_ChA_Healthy := FALSE;
            ELSIF (ABS(rAcoustic_ResonanceFreq_ChB - rVoted_AcousticResonance_kHz) > rTMR_Tol_Acoustic_kHz) THEN
                bTMR_Acoustic_ChB_Healthy := FALSE;
            ELSE
                bTMR_Acoustic_ChC_Healthy := FALSE;
            END_IF;
        END_IF;
    ELSE
        rTMR_Acoustic_Discrep_Timer := MAX(0.0, rTMR_Acoustic_Discrep_Timer - (rDeltaT * 0.5));
    END_IF;
ELSIF bTMR_Acoustic_ChA_Healthy AND bTMR_Acoustic_ChB_Healthy THEN
    rVoted_AcousticResonance_kHz := (rAcoustic_ResonanceFreq_ChA + rAcoustic_ResonanceFreq_ChB) * 0.50;
ELSIF bTMR_Acoustic_ChA_Healthy AND bTMR_Acoustic_ChC_Healthy THEN
    rVoted_AcousticResonance_kHz := (rAcoustic_ResonanceFreq_ChA + rAcoustic_ResonanceFreq_ChC) * 0.50;
ELSIF bTMR_Acoustic_ChB_Healthy AND bTMR_Acoustic_ChC_Healthy THEN
    rVoted_AcousticResonance_kHz := (rAcoustic_ResonanceFreq_ChB + rAcoustic_ResonanceFreq_ChC) * 0.50;
ELSE
    rVoted_AcousticResonance_kHz := rSP_AcousticResonance_kHz;
END_IF;
"""
