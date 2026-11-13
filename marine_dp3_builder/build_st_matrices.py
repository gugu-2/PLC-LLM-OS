# marine_dp3_builder/build_st_matrices.py

def get_matrices_initialization():
    lines = []
    def emit(s=""):
        lines.append(s)

    emit("(* ==================================================================================================================== *)")
    emit("(* PHASE 0: COLD START INITIALIZATION OF CYBER-PHYSICAL MATRICES, GEOMETRY & COEFFICIENTS                             *)")
    emit("(* ==================================================================================================================== *)")
    emit("IF NOT bInitialized THEN")
    emit("    (* ---------------------------------------------------------------------------------------------------------------- *)")
    emit("    (* A-MATRIX: DISCRETE HYDRODYNAMIC STATE TRANSITION (8x8) Ts = 0.025 s                                            *)")
    emit("    (* States: 1:Surge[m], 2:Sway[m], 3:Yaw[deg], 4:u[m/s], 5:v[m/s], 6:r[deg/s], 7:Roll[deg], 8:Pitch[deg]            *)")
    emit("    (* ---------------------------------------------------------------------------------------------------------------- *)")
    
    # 8x8 A Matrix values
    # Row 1: Surge position
    a_matrix = [
        [1.000000, 0.000000, 0.000000, 0.025000, 0.000000, 0.000000, 0.000000, 0.000000],
        [0.000000, 1.000000, 0.000000, 0.000000, 0.025000, 0.000000, 0.000000, 0.000000],
        [0.000000, 0.000000, 1.000000, 0.000000, 0.000000, 0.025000, 0.000000, 0.000000],
        [0.000000, 0.000000, 0.000000, 0.999150, 0.000000, 0.000025, 0.000000, -0.000185],
        [0.000000, 0.000000, 0.000000, 0.000000, 0.998820, -0.000315, 0.000420, 0.000000],
        [0.000000, 0.000000, 0.000000, 0.000015, -0.000280, 0.997540, 0.000000, 0.000000],
        [0.000000, 0.000000, 0.000000, 0.000000, 0.000550, 0.000000, 0.996250, 0.000000],
        [0.000000, 0.000000, 0.000000, -0.000320, 0.000000, 0.000000, 0.000000, 0.996800]
    ]
    for r in range(8):
        for c in range(8):
            emit(f"    matA[{r+1}, {c+1}] := {a_matrix[r][c]:.6f};")

    emit("")
    emit("    (* ---------------------------------------------------------------------------------------------------------------- *)")
    emit("    (* B-MATRIX: DISCRETE INPUT COUPLING / FORCE TO ACCELERATION (8x8) Ts = 0.025 s                                    *)")
    emit("    (* Inputs: 1:Fx[kN], 2:Fy[kN], 3:Mz[kNm], 4:Q_heel[m3/h], 5:Q_trim[m3/h], 6:Bias[%], 7:PMS_Cap[kW], 8:Mx_stab[kNm]*)")
    emit("    (* ---------------------------------------------------------------------------------------------------------------- *)")
    b_matrix = [
        [0.000005, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000],
        [0.000000, 0.000005, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000],
        [0.000000, 0.000000, 0.000008, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000],
        [0.000417, 0.000000, 0.000000, 0.000000, 0.000002, 0.000000, 0.000000, 0.000000],
        [0.000000, 0.000385, -0.000012, 0.000003, 0.000000, 0.000000, 0.000000, 0.000005],
        [0.000000, -0.000018, 0.000625, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000],
        [0.000000, 0.000085, 0.000000, -0.000450, 0.000000, 0.000000, 0.000000, 0.000320],
        [-0.000065, 0.000000, 0.000000, 0.000000, -0.000380, 0.000000, 0.000000, 0.000000]
    ]
    for r in range(8):
        for c in range(8):
            emit(f"    matB[{r+1}, {c+1}] := {b_matrix[r][c]:.6f};")

    emit("")
    emit("    (* ---------------------------------------------------------------------------------------------------------------- *)")
    emit("    (* C-MATRIX: SENSOR MEASUREMENT OBSERVATION PROJECTION (8x8)                                                        *)")
    emit("    (* ---------------------------------------------------------------------------------------------------------------- *)")
    for r in range(8):
        for c in range(8):
            val = 1.0 if r == c else 0.0
            emit(f"    matC[{r+1}, {c+1}] := {val:.6f};")

    emit("")
    emit("    (* ---------------------------------------------------------------------------------------------------------------- *)")
    emit("    (* D-MATRIX: DIRECT DIRECT FEEDTHROUGH TRANSMISSION (8x8 = 0.0)                                                    *)")
    emit("    (* ---------------------------------------------------------------------------------------------------------------- *)")
    for r in range(8):
        for c in range(8):
            emit(f"    matD[{r+1}, {c+1}] := 0.000000;")

    emit("")
    emit("    (* ---------------------------------------------------------------------------------------------------------------- *)")
    emit("    (* MPC WEIGHT MATRICES: Q (State Tracking Penalty), R (Actuator Effort), S (Slew), P (Terminal)                      *)")
    emit("    (* ---------------------------------------------------------------------------------------------------------------- *)")
    q_diag = [150.0, 150.0, 320.0, 45.0, 45.0, 80.0, 220.0, 220.0]
    r_diag = [0.012, 0.012, 0.008, 0.025, 0.025, 0.050, 0.001, 0.015]
    s_diag = [0.085, 0.085, 0.065, 0.120, 0.120, 0.150, 0.010, 0.045]
    p_diag = [350.0, 350.0, 750.0, 95.0, 95.0, 180.0, 480.0, 480.0]

    for r in range(8):
        for c in range(8):
            valQ = q_diag[r] if r == c else 0.0
            valR = r_diag[r] if r == c else 0.0
            valS = s_diag[r] if r == c else 0.0
            valP = p_diag[r] if r == c else 0.0
            emit(f"    matQ[{r+1}, {c+1}] := {valQ:.6f};")
            emit(f"    matR[{r+1}, {c+1}] := {valR:.6f};")
            emit(f"    matS[{r+1}, {c+1}] := {valS:.6f};")
            emit(f"    matP[{r+1}, {c+1}] := {valP:.6f};")

    emit("")
    emit("    (* ---------------------------------------------------------------------------------------------------------------- *)")
    emit("    (* EKF MATRICES: P_cov (Covariance), Q_noise (Process Noise), R_noise (Sensor Noise), K_gain (Steady Kalman Gain)    *)")
    emit("    (* ---------------------------------------------------------------------------------------------------------------- *)")
    p_cov_diag = [0.050, 0.050, 0.020, 0.010, 0.010, 0.005, 0.015, 0.015]
    q_noise_diag = [0.002, 0.002, 0.001, 0.005, 0.005, 0.002, 0.003, 0.003]
    r_noise_diag = [0.040, 0.040, 0.015, 0.020, 0.020, 0.008, 0.010, 0.010]
    k_gain_diag = [0.350, 0.350, 0.420, 0.280, 0.280, 0.310, 0.390, 0.390]

    for r in range(8):
        for c in range(8):
            valP = p_cov_diag[r] if r == c else 0.0
            valQn = q_noise_diag[r] if r == c else 0.0
            valRn = r_noise_diag[r] if r == c else 0.0
            valK = k_gain_diag[r] if r == c else 0.0
            emit(f"    matP_cov[{r+1}, {c+1}] := {valP:.6f};")
            emit(f"    matQ_noise[{r+1}, {c+1}] := {valQn:.6f};")
            emit(f"    matR_noise[{r+1}, {c+1}] := {valRn:.6f};")
            emit(f"    matK_gain[{r+1}, {c+1}] := {valK:.6f};")

    emit("")
    emit("    (* ---------------------------------------------------------------------------------------------------------------- *)")
    emit("    (* 8-AZIMUTH THRUSTER PHYSICAL GEOMETRIC COORDINATES (VESSEL BODY-FRAME: x=fwd, y=stbd) [m]                         *)")
    emit("    (* ---------------------------------------------------------------------------------------------------------------- *)")
    th_x = [42.0, 42.0, 18.0, 18.0, -18.0, -18.0, -42.0, -42.0]
    th_y = [-26.0, 26.0, -31.0, 31.0, -31.0, 31.0, -26.0, 26.0]
    for i in range(8):
        emit(f"    rThruster_X_pos[{i+1}] := {th_x[i]:.2f}; (* T{i+1} Longitudinal Arm from Vessel Origin [m] *)")
        emit(f"    rThruster_Y_pos[{i+1}] := {th_y[i]:.2f}; (* T{i+1} Transverse Arm from Vessel Origin [m] *)")
        emit(f"    rThruster_MaxThrust_kN[{i+1}] := 650.0; (* T{i+1} Continuous Maximum Bollard Pull [kN] *)")
        emit(f"    rThruster_MinThrust_kN[{i+1}] := 15.0;  (* T{i+1} Minimum Hydrodynamic Bias Floor [kN] *)")
        emit(f"    rThruster_MaxSlew_dps[{i+1}] := 16.0;   (* T{i+1} Maximum Azimuth Steering Slew Rate [deg/s] *)")
        emit(f"    rThruster_MaxRamp_kNps[{i+1}] := 25.0;  (* T{i+1} Maximum Thrust Ramp Rate of Change [kN/s] *)")
        emit(f"    rThruster_LossCoeff[{i+1}] := 1.00;     (* T{i+1} Clean Water Hydrodynamic Efficiency Factor *)")

    emit("")
    emit("    (* ---------------------------------------------------------------------------------------------------------------- *)")
    emit("    (* THRUSTER FORBIDDEN AZIMUTH BARRING SECTORS (PONTOON WAKE & MOONPOOL WASH AVOIDANCE) [deg]                       *)")
    emit("    (* ---------------------------------------------------------------------------------------------------------------- *)")
    barred_sectors = [
        # T1 (Bow-Port): sector 1: 340-360, sector 2: 80-110
        (340.0, 360.0, 80.0, 110.0),
        # T2 (Bow-Stbd): sector 1: 0-20, sector 2: 250-280
        (0.0, 20.0, 250.0, 280.0),
        # T3 (Mid-Port-Fwd): sector 1: 170-190, sector 2: 75-105
        (170.0, 190.0, 75.0, 105.0),
        # T4 (Mid-Stbd-Fwd): sector 1: 170-190, sector 2: 255-285
        (170.0, 190.0, 255.0, 285.0),
        # T5 (Mid-Port-Aft): sector 1: 350-10, sector 2: 75-105
        (350.0, 370.0, 75.0, 105.0),
        # T6 (Mid-Stbd-Aft): sector 1: 350-10, sector 2: 255-285
        (350.0, 370.0, 255.0, 285.0),
        # T7 (Stern-Port): sector 1: 160-200, sector 2: 70-100
        (160.0, 200.0, 70.0, 100.0),
        # T8 (Stern-Stbd): sector 1: 160-200, sector 2: 260-290
        (160.0, 200.0, 260.0, 290.0),
    ]
    for i in range(8):
        s1_min, s1_max, s2_min, s2_max = barred_sectors[i]
        emit(f"    rBarredMin_deg[{i+1}, 1] := {s1_min:.1f}; rBarredMax_deg[{i+1}, 1] := {s1_max:.1f}; (* T{i+1} Sector 1 *)")
        emit(f"    rBarredMin_deg[{i+1}, 2] := {s2_min:.1f}; rBarredMax_deg[{i+1}, 2] := {s2_max:.1f}; (* T{i+1} Sector 2 *)")
        emit(f"    bBarredActive[{i+1}] := FALSE;")

    emit("")
    emit("    (* ---------------------------------------------------------------------------------------------------------------- *)")
    emit("    (* BALLAST WING TANK GEOMETRIC RESTORING ARMS & CAPACITIES (8 TANKS) [m], [m3]                                      *)")
    emit("    (* ---------------------------------------------------------------------------------------------------------------- *)")
    tk_x = [38.0, 38.0, 14.0, 14.0, -14.0, -14.0, -38.0, -38.0]
    tk_y = [-28.0, 28.0, -32.0, 32.0, -32.0, 32.0, -28.0, 28.0]
    for i in range(8):
        emit(f"    rTank_X_arm_m[{i+1}] := {tk_x[i]:.2f}; (* Tank {i+1} Longitudinal Moment Arm [m] *)")
        emit(f"    rTank_Y_arm_m[{i+1}] := {tk_y[i]:.2f}; (* Tank {i+1} Transverse Moment Arm [m] *)")
        emit(f"    rTank_Volume_m3[{i+1}] := 1850.0; (* Tank {i+1} Total Volume Capacity [m3] *)")
        emit(f"    rTank_CurrentMass_kg[{i+1}] := 925000.0; (* Tank {i+1} Nominal 50% Water Mass [kg] *)")
        emit(f"    rBallast_DiscrepTimer_s[{i+1}] := 0.0;")
        emit(f"    bBallast_TankFault[{i+1}] := FALSE;")

    emit("")
    emit("    bInitialized := TRUE; (* Initialization Scan Completed *)")
    emit("END_IF;")
    return "\n".join(lines)

if __name__ == "__main__":
    print(get_matrices_initialization()[:500])
