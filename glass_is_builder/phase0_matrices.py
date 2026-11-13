# Phase 0: Discrete State-Space & MPC Matrices Initialization Generator

def generate_phase0():
    lines = []
    def emit(text=""):
        lines.append(text)

    emit("(* ==================================================================================================== *)")
    emit("(* PHASE 0: 8x8 DISCRETE STATE-SPACE & MPC RECEDING-HORIZON MATRICES INITIALIZATION                     *)")
    emit("(* ==================================================================================================== *)")
    emit("IF NOT bMatricesInitialized THEN")
    emit("    (* --------------------------------------------------------------------------------------------- *)")
    emit("    (* 8x8 DISCRETE STATE TRANSITION MATRIX matA (Ts = 0.005 s = 5 ms)                               *)")
    emit("    (* Physical dynamics: molten glass thermodynamics, viscous orifice discharge, pneumatic shears,   *)")
    emit("    (* parison heat extraction, skin reheat, servo kinematics, and lehr viscoelastic stress relaxation*)")
    emit("    (* --------------------------------------------------------------------------------------------- *)")
    
    # 8x8 A matrix
    A_values = [
        [0.9982, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
        [0.0450, 0.8850, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
        [0.0000, 0.0000, 0.9200, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
        [0.0250, 0.0120, 0.0000, 0.9400, 0.0000, 0.0000, 0.0000, 0.0000],
        [0.0000, 0.0000, 0.0000, 0.0000, 0.8500, 0.0000, 0.0000, 0.0000],
        [0.0180, 0.0000, 0.0000, -0.0320, 0.0000, 0.9100, 0.0000, 0.0000],
        [0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.9650, 0.0000],
        [0.0080, 0.0000, 0.0000, 0.0050, 0.0000, 0.0150, 0.0000, 0.9920]
    ]

    for i in range(1, 9):
        for j in range(1, 9):
            val = A_values[i-1][j-1]
            emit(f"    matA[{i}, {j}] := {val:.4f};")

    emit("")
    emit("    (* --------------------------------------------------------------------------------------------- *)")
    emit("    (* 8x8 DISCRETE INPUT COUPLING MATRIX matB (Ts = 5 ms)                                          *)")
    emit("    (* Control inputs: burner throttle, plunger trim, shear velocity, blank cooling, final blow SP, *)")
    emit("    (* blow mold cooling, servo take-out torque, and lehr heating modulation                        *)")
    emit("    (* --------------------------------------------------------------------------------------------- *)")

    B_values = [
        [0.0380, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
        [0.0020, 1.8500, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
        [0.0000, 0.0000, 4.2000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
        [0.0000, 0.0000, 0.0000, 0.1250, 0.0000, 0.0000, 0.0000, 0.0000],
        [0.0000, 0.0000, 0.0000, 0.0000, 0.4500, 0.0000, 0.0000, 0.0000],
        [0.0000, 0.0000, 0.0000, -0.0150, 0.0000, -0.0850, 0.0000, 0.0000],
        [0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.1450, 0.0000],
        [0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, -0.0220]
    ]

    for i in range(1, 9):
        for j in range(1, 9):
            val = B_values[i-1][j-1]
            emit(f"    matB[{i}, {j}] := {val:.4f};")

    emit("")
    emit("    (* --------------------------------------------------------------------------------------------- *)")
    emit("    (* 8x8 MEASUREMENT OUTPUT MATRIX matC (Direct State Observations)                                *)")
    emit("    (* --------------------------------------------------------------------------------------------- *)")

    for i in range(1, 9):
        for j in range(1, 9):
            val = 1.0000 if i == j else 0.0000
            emit(f"    matC[{i}, {j}] := {val:.4f};")

    emit("")
    emit("    (* --------------------------------------------------------------------------------------------- *)")
    emit("    (* 8x8 DIRECT FEEDTHROUGH MATRIX matD (Zero Feedthrough in Continuous Physical Processes)       *)")
    emit("    (* --------------------------------------------------------------------------------------------- *)")

    for i in range(1, 9):
        for j in range(1, 9):
            emit(f"    matD[{i}, {j}] := 0.0000;")

    emit("")
    emit("    (* --------------------------------------------------------------------------------------------- *)")
    emit("    (* 8x8 LUENBERGER OBSERVER KALMAN GAIN MATRIX matL_Obs                                          *)")
    emit("    (* Drives fast state estimation convergence within 3 to 5 discrete sample times                 *)")
    emit("    (* --------------------------------------------------------------------------------------------- *)")

    L_values = [
        [0.1850, 0.0020, 0.0000, 0.0010, 0.0000, 0.0005, 0.0000, 0.0001],
        [0.0050, 0.3200, 0.0000, 0.0020, 0.0000, 0.0000, 0.0000, 0.0000],
        [0.0000, 0.0000, 0.2850, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
        [0.0020, 0.0010, 0.0000, 0.2150, 0.0000, 0.0015, 0.0000, 0.0002],
        [0.0000, 0.0000, 0.0000, 0.0000, 0.3400, 0.0000, 0.0000, 0.0000],
        [0.0015, 0.0000, 0.0000, 0.0025, 0.0000, 0.2500, 0.0000, 0.0008],
        [0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.3100, 0.0000],
        [0.0005, 0.0000, 0.0000, 0.0002, 0.0000, 0.0010, 0.0000, 0.1950]
    ]

    for i in range(1, 9):
        for j in range(1, 9):
            val = L_values[i-1][j-1]
            emit(f"    matL_Obs[{i}, {j}] := {val:.4f};")

    emit("")
    emit("    (* --------------------------------------------------------------------------------------------- *)")
    emit("    (* MPC RECEDING-HORIZON QUADRATIC COST FUNCTIONAL PENALTY MATRICES (Q, R, S, P)                  *)")
    emit("    (* --------------------------------------------------------------------------------------------- *)")

    Q_diag = [12.50, 25.00, 8.50, 4.20, 15.00, 6.80, 18.00, 35.00]
    R_diag = [1.20, 3.50, 0.85, 0.65, 1.40, 0.75, 2.10, 1.80]
    S_diag = [4.50, 8.20, 2.10, 1.90, 3.80, 2.40, 5.50, 6.20]
    P_diag = [28.00, 55.00, 18.00, 9.50, 32.00, 15.00, 38.00, 75.00]

    for i in range(1, 9):
        for j in range(1, 9):
            q_val = Q_diag[i-1] if i == j else 0.0000
            r_val = R_diag[i-1] if i == j else 0.0000
            s_val = S_diag[i-1] if i == j else 0.0000
            p_val = P_diag[i-1] if i == j else 0.0000
            emit(f"    matQ_StateWeights[{i}, {j}] := {q_val:.4f};")
            emit(f"    matR_InputWeights[{i}, {j}] := {r_val:.4f};")
            emit(f"    matS_SlewWeights[{i}, {j}] := {s_val:.4f};")
            emit(f"    matP_TerminalWeights[{i}, {j}] := {p_val:.4f};")

    emit("")
    emit("    (* --------------------------------------------------------------------------------------------- *)")
    emit("    (* ACTUATOR PHYSICAL BOX SATURATION & SLEW RATE LIMIT BOUNDS                                     *)")
    emit("    (* --------------------------------------------------------------------------------------------- *)")

    u_min = [0.0, -5.0, 0.0, 0.0, 1.0, 0.0, -80.0, -100.0]
    u_max = [100.0, 5.0, 100.0, 100.0, 5.0, 100.0, 80.0, 100.0]
    du_min = [-1.5, -0.25, -5.0, -2.5, -0.20, -3.0, -12.0, -4.0]
    du_max = [1.5, 0.25, 5.0, 2.5, 0.20, 3.0, 12.0, 4.0]

    for i in range(1, 9):
        emit(f"    vecU_MinBounds[{i}] := {u_min[i-1]:.4f};")
        emit(f"    vecU_MaxBounds[{i}] := {u_max[i-1]:.4f};")
        emit(f"    vecDeltaU_MinRate[{i}] := {du_min[i-1]:.4f};")
        emit(f"    vecDeltaU_MaxRate[{i}] := {du_max[i-1]:.4f};")

    emit("")
    emit("    (* --------------------------------------------------------------------------------------------- *)")
    emit("    (* 2oo3 TMR SENSOR TOLERANCES & DEBOUNCE LIMITS (CHANNELS 1..10)                                 *)")
    emit("    (* --------------------------------------------------------------------------------------------- *)")

    tmr_tol = [4.50, 6.00, 2.50, 45.0, 0.25, 0.20, 0.25, 1.20, 1.20, 0.35]
    tmr_debounce = [0.150, 0.100, 0.050, 0.050, 0.100, 0.100, 0.100, 0.050, 0.050, 0.250]

    for i in range(1, 11):
        emit(f"    arrTmrDiscrepancyThreshold[{i}] := {tmr_tol[i-1]:.4f};")
        emit(f"    arrTmrDebounceLimit_s[{i}] := {tmr_debounce[i-1]:.4f};")
        emit(f"    arrTmrTimer_AB_s[{i}] := 0.0;")
        emit(f"    arrTmrTimer_BC_s[{i}] := 0.0;")
        emit(f"    arrTmrTimer_AC_s[{i}] := 0.0;")
        emit(f"    arrTmrChannelFault_A[{i}] := FALSE;")
        emit(f"    arrTmrChannelFault_B[{i}] := FALSE;")
        emit(f"    arrTmrChannelFault_C[{i}] := FALSE;")
        emit(f"    arrTmrDegradationMode[{i}] := 0; (* Healthy 2oo3 *)")
        emit(f"    arrTmrStatusWord[{i}] := 16#0000;")

    emit("")
    emit("    (* --------------------------------------------------------------------------------------------- *)")
    emit("    (* 12-SECTION TIMING DRUM PHASE OFFSETS (30.0 DEGREE INTERVALS)                                  *)")
    emit("    (* --------------------------------------------------------------------------------------------- *)")

    for i in range(1, 13):
        offset = (i - 1) * 30.0
        emit(f"    arrSectionPhaseOffset_deg[{i}] := {offset:.1f};")
        emit(f"    arrSectionLocalAngle_deg[{i}] := 0.0;")
        emit(f"    arrSectionFsmState[{i}] := 0;")
        emit(f"    arrSectionBlankMoldClosed[{i}] := FALSE;")
        emit(f"    arrSectionBlowMoldClosed[{i}] := FALSE;")
        emit(f"    arrSectionInvertArmAtBlank[{i}] := TRUE;")
        emit(f"    arrSectionInvertArmAtBlow[{i}] := FALSE;")
        emit(f"    arrSectionTakeOutAtBlow[{i}] := FALSE;")
        emit(f"    arrSectionTakeOutAtDeadplate[{i}] := TRUE;")
        emit(f"    arrSectionGobWeightFeedback_g[{i}] := 325.0;")
        emit(f"    arrSectionCycleTime_ms[{i}] := 4500.0;")
        emit(f"    arrSectionEnabledPermissive[{i}] := TRUE;")

    emit("")
    emit("    (* --------------------------------------------------------------------------------------------- *)")
    emit("    (* ISA-18.2 MULTI-TIER ALARM TRIP LIMITS (CHANNELS 1..8)                                         *)")
    emit("    (* --------------------------------------------------------------------------------------------- *)")

    hh_limits = [1190.0, 345.0, 1600.0, 75.0, 4.80, 75.0, 195.0, 6.50]
    h_limits  = [1170.0, 335.0, 1450.0, 65.0, 4.20, 60.0, 185.0, 4.80]
    l_limits  = [1130.0, 315.0, 1050.0, 25.0, 1.50, 15.0, -5.0, 0.50]
    ll_limits = [1110.0, 305.0, 900.0, 15.0, 0.80, 5.0, -15.0, 0.10]
    deadbands = [3.50, 1.50, 25.0, 2.0, 0.15, 2.50, 1.00, 0.25]
    roc_limits= [15.0, 20.0, 350.0, 15.0, 5.0, 30.0, 120.0, 2.50]

    for i in range(1, 9):
        emit(f"    arrAlarmLimit_HH[{i}] := {hh_limits[i-1]:.2f};")
        emit(f"    arrAlarmLimit_H[{i}] := {h_limits[i-1]:.2f};")
        emit(f"    arrAlarmLimit_L[{i}] := {l_limits[i-1]:.2f};")
        emit(f"    arrAlarmLimit_LL[{i}] := {ll_limits[i-1]:.2f};")
        emit(f"    arrAlarmDeadband[{i}] := {deadbands[i-1]:.2f};")
        emit(f"    arrAlarmRateOfChangeLimit[{i}] := {roc_limits[i-1]:.2f};")
        emit(f"    arrAlarmPrevSampleValue[{i}] := 0.0;")
        emit(f"    arrAlarmActive_HH[{i}] := FALSE;")
        emit(f"    arrAlarmActive_H[{i}] := FALSE;")
        emit(f"    arrAlarmActive_L[{i}] := FALSE;")
        emit(f"    arrAlarmActive_LL[{i}] := FALSE;")
        emit(f"    arrAlarmActive_Roc[{i}] := FALSE;")
        emit(f"    arrAlarmTripLatched[{i}] := FALSE;")

    emit("")
    emit("    bMatricesInitialized := TRUE;")
    emit("END_IF;")
    emit("")

    return "\n".join(lines)

if __name__ == "__main__":
    s = generate_phase0()
    print("Phase 0 generated, lines:", len(s.splitlines()), "chars:", len(s))
