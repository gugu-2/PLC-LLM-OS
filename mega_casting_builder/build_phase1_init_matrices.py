# mega_casting_builder/build_phase1_init_matrices.py

def get_phase1_init_matrices():
    return """(* =====================================================================================================================
 * PHASE 1: SYSTEM REBOOT COLD-START INITIALIZATION OF DISCRETE STATE-SPACE MATRICES & MPC WEIGHTS
 * One-shot execution on controller startup or reboot. All 6x6 matrices explicitly populated term-by-term.
 * ===================================================================================================================== *)
IF NOT bStateSpace_Initialized THEN

    (* --- Geometrical Cross-Sectional Areas & Hydrostatic Area Ratios --- *)
    rCylHead_Area_m2 := 3.1415926535 * (rCylHead_Diameter_m * rCylHead_Diameter_m) / 4.0; (* 0.080425 m2 *)
    rCylRod_Area_m2  := 3.1415926535 * ((rCylHead_Diameter_m * rCylHead_Diameter_m) - (rCylRod_Diameter_m * rCylRod_Diameter_m)) / 4.0; (* 0.054978 m2 *)
    rPlunger_Area_m2 := 3.1415926535 * (rPlunger_Diameter_m * rPlunger_Diameter_m) / 4.0; (* 0.015394 m2 *)

    (* Tie-Bar Column Structural Cross-Sectional Area *)
    rTieBar_Area_m2  := 3.1415926535 * (rTieBar_Diameter_m * rTieBar_Diameter_m) / 4.0; (* 0.152053 m2 *)

    (* Wave Crest Critical Velocity in Cold Chamber Sleeve (Phase 1 Wave Suppression) *)
    (* v_crit = SQRT(g * D_plunger * (1 - fill_ratio)) *)
    rCritical_Wave_Velocity_ms := SQRT(9.80665 * rPlunger_Diameter_m * (1.0 - rSleeve_Fill_Ratio)); (* approx 0.865 m/s *)

    (* --- DISCRETE STATE TRANSITION MATRIX A (6x6) --- *)
    (* Represents discrete dynamics at Ts = 0.001 s (1 kHz sample time):
     * Row 1: Plunger Stroke Position x_p [mm] (kinematic integration of velocity)
     * Row 2: Plunger Axial Velocity v_p [m/s] (hydraulic acceleration minus melt drag)
     * Row 3: Shot Cylinder Head Pressure P_head [bar] (compressibility & servo inflow)
     * Row 4: Molten Aluminum Cavity Pressure P_cavity [bar] (acoustic wave propagation & gate flow)
     * Row 5: Evacuation Chamber Absolute Pressure P_vac [mbar] (vacuum pump volumetric drawdown)
     * Row 6: Tie-Bar Dynamic Elastic Strain Stretch [um] (toggle lockup & cavity reaction force) *)

    (* Row 1: Plunger Position Dynamics *)
    rMatrix_A[1, 1] := 1.000000; (* Position persistence *)
    rMatrix_A[1, 2] := 0.001000; (* dx_p/dt = v_p * Ts (mm/s to mm conversion factor) *)
    rMatrix_A[1, 3] := 0.000000; (* Head pressure cross-coupling *)
    rMatrix_A[1, 4] := 0.000000; (* Cavity pressure cross-coupling *)
    rMatrix_A[1, 5] := 0.000000; (* Vacuum cross-coupling *)
    rMatrix_A[1, 6] := 0.000000; (* Tie-bar strain cross-coupling *)

    (* Row 2: Plunger Velocity Dynamics *)
    rMatrix_A[2, 1] := 0.000000; (* Coulomb position friction *)
    rMatrix_A[2, 2] := 0.965400; (* Plunger mass inertial damping & sleeve viscous shear drag *)
    rMatrix_A[2, 3] := 0.002840; (* Acceleration drive from head hydraulic pressure *)
    rMatrix_A[2, 4] := -0.000540;(* Backpressure deceleration reaction from molten cavity melt *)
    rMatrix_A[2, 5] := 0.000010; (* Minor sleeve back-aeration draft *)
    rMatrix_A[2, 6] := -0.000005;(* Platen platen deflection binding friction *)

    (* Row 3: Shot Cylinder Head Pressure Dynamics *)
    rMatrix_A[3, 1] := 0.000000; (* Position compliance *)
    rMatrix_A[3, 2] := -0.185000;(* Plunger forward displacement hydraulic chamber volumetric expansion *)
    rMatrix_A[3, 3] := 0.942000; (* Hydraulic oil compressibility and seal leakage decay *)
    rMatrix_A[3, 4] := 0.012500; (* Fluid-structural acoustic reflection from gate freeze *)
    rMatrix_A[3, 5] := 0.000000; (* Vacuum decoupling *)
    rMatrix_A[3, 6] := 0.000000; (* Clamping decoupling *)

    (* Row 4: Molten Aluminum In-Cavity Dynamic Pressure Dynamics *)
    rMatrix_A[4, 1] := 0.000000; (* Position coupling *)
    rMatrix_A[4, 2] := 0.320000; (* Inrush momentum dynamic pressure conversion at in-gate *)
    rMatrix_A[4, 3] := 0.045000; (* Direct Pascal transmission from shot cylinder head *)
    rMatrix_A[4, 4] := 0.885000; (* Liquid alloy bulk modulus and gate throttling decay *)
    rMatrix_A[4, 5] := -0.008500;(* Counter-pressure reduction from vacuum evacuation *)
    rMatrix_A[4, 6] := -0.002100;(* Die cavity parting line microscopic breathing compliance *)

    (* Row 5: Evacuation Chamber Absolute Pressure Dynamics *)
    rMatrix_A[5, 1] := 0.000000; (* Stroke position coupling *)
    rMatrix_A[5, 2] := -0.015000;(* Plunger sweeping gas column compression in sleeve *)
    rMatrix_A[5, 3] := 0.000000; (* Head pressure decoupling *)
    rMatrix_A[5, 4] := 0.000000; (* Cavity liquid pressure decoupling *)
    rMatrix_A[5, 5] := 0.925000; (* Dual roots pump evacuation drawdown rate decay *)
    rMatrix_A[5, 6] := 0.000450; (* Parting plane gap microscopic atmospheric ingress *)

    (* Row 6: Clamping Tie-Bar Dynamic Elastic Strain Dynamics *)
    rMatrix_A[6, 1] := 0.000000; (* Stroke decoupling *)
    rMatrix_A[6, 2] := 0.000000; (* Velocity decoupling *)
    rMatrix_A[6, 3] := 0.001200; (* Axial reaction force from shot cylinder frame mounts *)
    rMatrix_A[6, 4] := 0.085000; (* Separating force transmitted to platen by cavity pressure *)
    rMatrix_A[6, 5] := 0.000000; (* Vacuum decoupling *)
    rMatrix_A[6, 6] := 0.982000; (* Toggle mechanism stiffness and column structural viscoelasticity *)

    (* --- ACTUATOR INPUT COUPLING MATRIX B (6x6) --- *)
    (* Inputs:
     * u1: Ultra-Fast Servo Proportional Valve Spool [%] (-100% to +100%)
     * u2: Accumulator Discharge Cartridge Valve Trim [%] (0 to 100%)
     * u3: Phase 3 Intensification Booster Valve [%] (0 to 100%)
     * u4: Parting Plane Vacuum Throttle Valve [%] (0 to 100%)
     * u5: Mold Thermal Oil Circulation Valve Trim [%] (0 to 100%)
     * u6: Toggle Clamping Locking Pilot Pressure Trim [%] (0 to 100%) *)

    (* Row 1: Plunger Position Response *)
    rMatrix_B[1, 1] := 0.000500; (* Direct spool velocity feedforward *)
    rMatrix_B[1, 2] := 0.000100; (* Accumulator burst displacement *)
    rMatrix_B[1, 3] := 0.000000; (* Intensifier hold *)
    rMatrix_B[1, 4] := 0.000000; (* Vacuum *)
    rMatrix_B[1, 5] := 0.000000; (* Thermal *)
    rMatrix_B[1, 6] := 0.000000; (* Clamp *)

    (* Row 2: Plunger Velocity Response *)
    rMatrix_B[2, 1] := 0.082500; (* High-speed servo valve flow gain to plunger acceleration *)
    rMatrix_B[2, 2] := 0.045000; (* Accumulator cartridge valve discharge acceleration boost *)
    rMatrix_B[2, 3] := -0.012000;(* Intensification booster initial deceleration cushion *)
    rMatrix_B[2, 4] := 0.000500; (* Gas resistance reduction under vacuum *)
    rMatrix_B[2, 5] := 0.000000; (* Thermal *)
    rMatrix_B[2, 6] := 0.000000; (* Clamp *)

    (* Row 3: Shot Cylinder Head Pressure Response *)
    rMatrix_B[3, 1] := 0.250000; (* Servo valve spool opening pressure build *)
    rMatrix_B[3, 2] := 0.650000; (* Piston accumulator main discharge pressure drive *)
    rMatrix_B[3, 3] := 2.850000; (* Phase 3 Intensification booster cartridge massive pressure multiplication *)
    rMatrix_B[3, 4] := 0.000000; (* Vacuum *)
    rMatrix_B[3, 5] := 0.000000; (* Thermal *)
    rMatrix_B[3, 6] := 0.000000; (* Clamp *)

    (* Row 4: Molten Aluminum In-Cavity Pressure Response *)
    rMatrix_B[4, 1] := 0.035000; (* Servo valve dynamic flow influence *)
    rMatrix_B[4, 2] := 0.120000; (* Accumulator discharge pressure transmission *)
    rMatrix_B[4, 3] := 1.950000; (* Intensification multiplication through liquid aluminum runner *)
    rMatrix_B[4, 4] := -0.025000;(* Vacuum assist cavitation suppression *)
    rMatrix_B[4, 5] := 0.000000; (* Thermal *)
    rMatrix_B[4, 6] := 0.000000; (* Clamp *)

    (* Row 5: Evacuation Chamber Absolute Pressure Response *)
    rMatrix_B[5, 1] := 0.000000; (* Servo *)
    rMatrix_B[5, 2] := 0.000000; (* Accumulator *)
    rMatrix_B[5, 3] := 0.000000; (* Intensifier *)
    rMatrix_B[5, 4] := -0.750000;(* Vacuum proportional throttle valve drawdown opening rate *)
    rMatrix_B[5, 5] := 0.000000; (* Thermal *)
    rMatrix_B[5, 6] := -0.005000;(* Tight parting line lockup sealing vacuum enhancement *)

    (* Row 6: Clamping Tie-Bar Dynamic Elastic Strain Response *)
    rMatrix_B[6, 1] := 0.000000; (* Servo *)
    rMatrix_B[6, 2] := 0.002000; (* Accumulator shot shock *)
    rMatrix_B[6, 3] := 0.045000; (* Intensification separating force transmission *)
    rMatrix_B[6, 4] := 0.000000; (* Vacuum *)
    rMatrix_B[6, 5] := 0.001000; (* Die thermal expansion pre-load *)
    rMatrix_B[6, 6] := 0.420000; (* Toggle cylinder hydraulic locking pressure build *)

    (* --- EXOGENOUS DISTURBANCE COUPLING MATRIX Ew (6x6) --- *)
    (* Disturbances:
     * w1: Melt Flow Viscosity Anomaly / Pre-solidification Cold Flake Resistance
     * w2: Sleeve Fill Ratio Surge Wave Perturbation
     * w3: Acoustic Cavity In-Gate Shockwave Choking
     * w4: Parting Line Microscopic Flash Gapping
     * w5: Nitrogen Accumulator Polytropic Pressure Drop
     * w6: Mold Thermal Core Expansion Unbalance *)
    rMatrix_Ew[1, 1] := 0.00000; rMatrix_Ew[1, 2] := 0.00010; rMatrix_Ew[1, 3] := 0.00000; rMatrix_Ew[1, 4] := 0.00000; rMatrix_Ew[1, 5] := 0.00000; rMatrix_Ew[1, 6] := 0.00000;
    rMatrix_Ew[2, 1] := -0.0450; rMatrix_Ew[2, 2] := -0.0280; rMatrix_Ew[2, 3] := -0.0150; rMatrix_Ew[2, 4] := 0.00000; rMatrix_Ew[2, 5] := 0.00800; rMatrix_Ew[2, 6] := 0.00000;
    rMatrix_Ew[3, 1] := 0.08500; rMatrix_Ew[3, 2] := 0.02000; rMatrix_Ew[3, 3] := 0.15000; rMatrix_Ew[3, 4] := 0.00000; rMatrix_Ew[3, 5] := -0.2500; rMatrix_Ew[3, 6] := 0.00000;
    rMatrix_Ew[4, 1] := -0.1200; rMatrix_Ew[4, 2] := 0.05000; rMatrix_Ew[4, 3] := 0.35000; rMatrix_Ew[4, 4] := -0.2200; rMatrix_Ew[4, 5] := 0.00000; rMatrix_Ew[4, 6] := 0.01500;
    rMatrix_Ew[5, 1] := 0.00000; rMatrix_Ew[5, 2] := 0.01000; rMatrix_Ew[5, 3] := 0.00000; rMatrix_Ew[5, 4] := 0.85000; rMatrix_Ew[5, 5] := 0.00000; rMatrix_Ew[5, 6] := 0.00000;
    rMatrix_Ew[6, 1] := 0.00000; rMatrix_Ew[6, 2] := 0.00000; rMatrix_Ew[6, 3] := 0.05500; rMatrix_Ew[6, 4] := 0.12000; rMatrix_Ew[6, 5] := 0.00000; rMatrix_Ew[6, 6] := 0.08000;

    (* --- SENSOR OBSERVATION MATRIX C (6x6) --- *)
    (* Direct identity mapping with minor sensor cross-talk and calibration gains *)
    rMatrix_C[1, 1] := 1.0000; rMatrix_C[1, 2] := 0.0000; rMatrix_C[1, 3] := 0.0000; rMatrix_C[1, 4] := 0.0000; rMatrix_C[1, 5] := 0.0000; rMatrix_C[1, 6] := 0.0000;
    rMatrix_C[2, 1] := 0.0000; rMatrix_C[2, 2] := 1.0000; rMatrix_C[2, 3] := 0.0000; rMatrix_C[2, 4] := 0.0000; rMatrix_C[2, 5] := 0.0000; rMatrix_C[2, 6] := 0.0000;
    rMatrix_C[3, 1] := 0.0000; rMatrix_C[3, 2] := 0.0000; rMatrix_C[3, 3] := 1.0000; rMatrix_C[3, 4] := 0.0000; rMatrix_C[3, 5] := 0.0000; rMatrix_C[3, 6] := 0.0000;
    rMatrix_C[4, 1] := 0.0000; rMatrix_C[4, 2] := 0.0000; rMatrix_C[4, 3] := 0.0000; rMatrix_C[4, 4] := 1.0000; rMatrix_C[4, 5] := 0.0000; rMatrix_C[4, 6] := 0.0000;
    rMatrix_C[5, 1] := 0.0000; rMatrix_C[5, 2] := 0.0000; rMatrix_C[5, 3] := 0.0000; rMatrix_C[5, 4] := 0.0000; rMatrix_C[5, 5] := 1.0000; rMatrix_C[5, 6] := 0.0000;
    rMatrix_C[6, 1] := 0.0000; rMatrix_C[6, 2] := 0.0000; rMatrix_C[6, 3] := 0.0000; rMatrix_C[6, 4] := 0.0000; rMatrix_C[6, 5] := 0.0000; rMatrix_C[6, 6] := 1.0000;

    (* --- DIRECT FEEDTHROUGH MATRIX D (6x6) --- *)
    (* Strictly zero direct feedthrough for physical causality *)
    FOR i_idx := 1 TO 6 DO
        FOR j_idx := 1 TO 6 DO
            rMatrix_D[i_idx, j_idx] := 0.000000;
        END_FOR;
    END_FOR;

    (* --- STEADY-STATE KALMAN / LUENBERGER OBSERVER INNOVATION GAIN L (6x6) --- *)
    (* Synthesized from discrete algebraic Riccati equation balancing sensor noise vs plant disturbances *)
    rMatrix_L[1, 1] := 0.3540; rMatrix_L[1, 2] := 0.0012; rMatrix_L[1, 3] := 0.0000; rMatrix_L[1, 4] := 0.0000; rMatrix_L[1, 5] := 0.0000; rMatrix_L[1, 6] := 0.0000;
    rMatrix_L[2, 1] := 0.0125; rMatrix_L[2, 2] := 0.4280; rMatrix_L[2, 3] := 0.0015; rMatrix_L[2, 4] := 0.0008; rMatrix_L[2, 5] := 0.0000; rMatrix_L[2, 6] := 0.0000;
    rMatrix_L[3, 1] := 0.0000; rMatrix_L[3, 2] := 0.0035; rMatrix_L[3, 3] := 0.4850; rMatrix_L[3, 4] := 0.0120; rMatrix_L[3, 5] := 0.0000; rMatrix_L[3, 6] := 0.0000;
    rMatrix_L[4, 1] := 0.0000; rMatrix_L[4, 2] := 0.0018; rMatrix_L[4, 3] := 0.0095; rMatrix_L[4, 4] := 0.5120; rMatrix_L[4, 5] := 0.0000; rMatrix_L[4, 6] := 0.0015;
    rMatrix_L[5, 1] := 0.0000; rMatrix_L[5, 2] := 0.0000; rMatrix_L[5, 3] := 0.0000; rMatrix_L[5, 4] := 0.0000; rMatrix_L[5, 5] := 0.3850; rMatrix_L[5, 6] := 0.0000;
    rMatrix_L[6, 1] := 0.0000; rMatrix_L[6, 2] := 0.0000; rMatrix_L[6, 3] := 0.0005; rMatrix_L[6, 4] := 0.0025; rMatrix_L[6, 5] := 0.0000; rMatrix_L[6, 6] := 0.4450;

    (* --- MODEL PREDICTIVE CONTROL (MPC) PENALTY MATRICES (Q, R, P, S) --- *)
    (* State Tracking Error Weight Matrix Q (6x6 diagonal dominant) *)
    FOR i_idx := 1 TO 6 DO
        FOR j_idx := 1 TO 6 DO
            rMPC_Matrix_Q[i_idx, j_idx] := 0.0;
            rMPC_Matrix_R[i_idx, j_idx] := 0.0;
            rMPC_Matrix_P[i_idx, j_idx] := 0.0;
            rMPC_Matrix_S[i_idx, j_idx] := 0.0;
        END_FOR;
    END_FOR;

    (* Q Diagonal Penalties *)
    rMPC_Matrix_Q[1, 1] := 25.0;  (* Plunger position tracking weight *)
    rMPC_Matrix_Q[2, 2] := 150.0; (* Plunger velocity tracking weight (critical for 9.5 m/s Phase 2) *)
    rMPC_Matrix_Q[3, 3] := 5.0;   (* Head hydraulic pressure weight *)
    rMPC_Matrix_Q[4, 4] := 12.0;  (* In-cavity liquid pressure weight *)
    rMPC_Matrix_Q[5, 5] := 8.0;   (* Vacuum evacuation tracking weight *)
    rMPC_Matrix_Q[6, 6] := 35.0;  (* Clamping force & tie-bar stretch stability weight *)

    (* Actuator Control Energy Penalty Matrix R (6x6 diagonal) *)
    rMPC_Matrix_R[1, 1] := 0.25;  (* Servo injection valve spool penalty *)
    rMPC_Matrix_R[2, 2] := 0.15;  (* Accumulator cartridge trim penalty *)
    rMPC_Matrix_R[3, 3] := 0.10;  (* Intensifier booster valve penalty *)
    rMPC_Matrix_R[4, 4] := 0.05;  (* Vacuum throttle valve penalty *)
    rMPC_Matrix_R[5, 5] := 0.08;  (* Thermal oil flow trim penalty *)
    rMPC_Matrix_R[6, 6] := 0.20;  (* Clamping locking pilot trim penalty *)

    (* Terminal State Horizon Penalty Matrix P (6x6 diagonal: P = 2.5 * Q) *)
    FOR i_idx := 1 TO 6 DO
        rMPC_Matrix_P[i_idx, i_idx] := rMPC_Matrix_Q[i_idx, i_idx] * 2.5;
    END_FOR;

    (* Actuator Slew Rate Dynamic Smoothness Matrix S (6x6 diagonal) *)
    rMPC_Matrix_S[1, 1] := 0.85;  (* Dampen high-frequency spool flutter *)
    rMPC_Matrix_S[2, 2] := 0.50;  (* Dampen accumulator pilot chatter *)
    rMPC_Matrix_S[3, 3] := 0.40;  (* Smooth booster cartridge ramp *)
    rMPC_Matrix_S[4, 4] := 0.25;  (* Smooth vacuum valve motion *)
    rMPC_Matrix_S[5, 5] := 0.30;  (* Thermal valve slew limit *)
    rMPC_Matrix_S[6, 6] := 0.60;  (* Clamping pilot pressure rate limit *)

    (* Hard Actuator Saturation & Slew Constraints *)
    rMPC_u_Min[1] := -100.0; rMPC_u_Max[1] := 100.0; rMPC_Slew_Max[1] := 25.0; (* Moog servo spool: +/-100%, 25%/ms *)
    rMPC_u_Min[2] := 0.0;    rMPC_u_Max[2] := 100.0; rMPC_Slew_Max[2] := 15.0; (* Accumulator discharge: 0..100% *)
    rMPC_u_Min[3] := 0.0;    rMPC_u_Max[3] := 100.0; rMPC_Slew_Max[3] := 30.0; (* Intensification valve: 0..100%, fast *)
    rMPC_u_Min[4] := 0.0;    rMPC_u_Max[4] := 100.0; rMPC_Slew_Max[4] := 10.0; (* Vacuum throttle: 0..100% *)
    rMPC_u_Min[5] := 0.0;    rMPC_u_Max[5] := 100.0; rMPC_Slew_Max[5] := 5.0;  (* Thermal oil valve: 0..100% *)
    rMPC_u_Min[6] := 0.0;    rMPC_u_Max[6] := 100.0; rMPC_Slew_Max[6] := 8.0;  (* Toggle clamp pilot: 0..100% *)

    (* Initialize State and Estimator Vectors to Safe Quiescent State *)
    FOR i_idx := 1 TO 6 DO
        rState_x[i_idx]          := 0.0;
        rState_x_hat[i_idx]      := 0.0;
        rState_x_hat_next[i_idx] := 0.0;
        rInput_u[i_idx]          := 0.0;
        rInput_u_prev[i_idx]     := 0.0;
        rOutput_y[i_idx]         := 0.0;
        rOutput_y_hat[i_idx]     := 0.0;
        rDisturbance_w[i_idx]    := 0.0;
        rInnovation_Residual[i_idx] := 0.0;
        rMPC_Ref_x[i_idx]        := 0.0;
    END_FOR;

    (* Quiescent Initial Pressure Values *)
    rState_x[5]     := 1013.25; (* Ambient atmospheric starting pressure [mbar] *)
    rState_x_hat[5] := 1013.25;

    bStateSpace_Initialized := TRUE;
    bSystem_ColdBoot := FALSE;
END_IF;
"""
