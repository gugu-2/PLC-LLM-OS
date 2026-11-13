# hpdc_megacasting_builder/build_st_matrices.py

def get_matrices_initialization():
    return """(* =====================================================================================================================
 * INITIALIZATION PHASE: DISCRETE STATE-SPACE MATRICES, KALMAN FILTER & THERMAL PID LOOPS
 * One-shot execution on controller cold-start or PLC warm reboot
 * ===================================================================================================================== *)
IF NOT bStateSpace_Initialized THEN

    (* --- Geometrical Areas & Fundamental Hydrostatic Physical Constants --- *)
    rCylHead_Area_m2 := 3.1415926535 * (rCylHead_Diameter_m * rCylHead_Diameter_m) / 4.0; (* 0.080425 m2 *)
    rCylRod_Area_m2  := 3.1415926535 * ((rCylHead_Diameter_m * rCylHead_Diameter_m) - (rCylRod_Diameter_m * rCylRod_Diameter_m)) / 4.0; (* 0.054978 m2 *)
    rPlunger_Area_m2 := 3.1415926535 * (rPlunger_Diameter_m * rPlunger_Diameter_m) / 4.0; (* 0.020106 m2 *)

    (* --- Phase 1 Fluid Dynamics: Wave Crest Height and Critical Surge Velocity --- *)
    rCritical_Wave_Velocity_ms := SQRT(9.80665 * rPlunger_Diameter_m * (1.0 - rSleeve_Fill_Ratio)); (* approx 0.954 m/s *)
    IF rRecipe_Phase2_Velocity_In > 0.01 THEN
        rTheoretical_FillTime_ms := (rCavity_Volume_m3 / (rPlunger_Area_m2 * rRecipe_Phase2_Velocity_In)) * 1000.0;
    ELSE
        rTheoretical_FillTime_ms := 45.0;
    END_IF;

    (* =============================================================================================================
     * DISCRETE STATE TRANSITION MATRIX A (8x8) at Ts = 0.001 s (1 kHz)
     * Continuous mechanics:
     * dx1/dt = x2 (velocity to position)
     * dx2/dt = (1/M) * (P_head*A_head - P_rod*A_rod - P_metal*A_plunger - B_fric*x2)
     * dx3/dt = (Beta / V_head) * (Q_valve_in - A_head*x2)
     * dx4/dt = (Beta / V_rod) * (A_rod*x2 - Q_valve_out)
     * dx5/dt = (K_metal / V_cavity) * (A_plunger*x2 - Q_solidification)
     * dx6/dt = (1 / Tau_vac) * (P_target_vac - x6)
     * dx7/dt = (1 / Tau_die) * (T_melt - x7) - (H_cool / C_steel) * Flow_cool
     * dx8/dt = (1 / Tau_accum) * (P_pump - x8) - Q_intens / C_hyd
     * ============================================================================================================= *)
    (* Row 1: x1 (Plunger Stroke Position [mm]) *)
    rMatrix_A[1, 1] := 1.000000;
    rMatrix_A[1, 2] := 0.001000; (* dt in seconds translated to mm *)
    rMatrix_A[1, 3] := 0.000000;
    rMatrix_A[1, 4] := 0.000000;
    rMatrix_A[1, 5] := 0.000000;
    rMatrix_A[1, 6] := 0.000000;
    rMatrix_A[1, 7] := 0.000000;
    rMatrix_A[1, 8] := 0.000000;

    (* Row 2: x2 (Plunger Velocity [m/s]) *)
    rMatrix_A[2, 1] := 0.000000;
    rMatrix_A[2, 2] := 0.985200; (* Viscous friction damping decay *)
    rMatrix_A[2, 3] := 0.001785; (* Forward head pressure acceleration coupling *)
    rMatrix_A[2, 4] := -0.001221; (* Opposing rod pressure deceleration coupling *)
    rMatrix_A[2, 5] := -0.000446; (* Molten metal cavity resistance drag *)
    rMatrix_A[2, 6] := 0.000012; (* Residual cavity gas backpressure *)
    rMatrix_A[2, 7] := 0.000000;
    rMatrix_A[2, 8] := 0.000312; (* Accumulator pressure feed assist *)

    (* Row 3: x3 (Shot Cylinder Head Pressure [bar]) *)
    rMatrix_A[3, 1] := 0.000000;
    rMatrix_A[3, 2] := -0.142500; (* Volume expansion decompression due to plunger velocity *)
    rMatrix_A[3, 3] := 0.962400; (* Hydraulic line capacitance decay *)
    rMatrix_A[3, 4] := 0.000000;
    rMatrix_A[3, 5] := 0.000000;
    rMatrix_A[3, 6] := 0.000000;
    rMatrix_A[3, 7] := 0.000000;
    rMatrix_A[3, 8] := 0.035100; (* Coupling to high-speed accumulator supply *)

    (* Row 4: x4 (Shot Cylinder Rod Pressure [bar]) *)
    rMatrix_A[4, 1] := 0.000000;
    rMatrix_A[4, 2] := 0.118200; (* Compression pressure rise in rod chamber as piston advances *)
    rMatrix_A[4, 3] := 0.000000;
    rMatrix_A[4, 4] := 0.954800; (* Proportional counter-pressure valve throttling *)
    rMatrix_A[4, 5] := 0.000000;
    rMatrix_A[4, 6] := 0.000000;
    rMatrix_A[4, 7] := 0.000000;
    rMatrix_A[4, 8] := 0.000000;

    (* Row 5: x5 (In-Cavity Molten Alloy Dynamic Pressure [bar]) *)
    rMatrix_A[5, 1] := 0.000000;
    rMatrix_A[5, 2] := 0.284500; (* Melt front hydrodynamic pressure build from velocity *)
    rMatrix_A[5, 3] := 0.015200;
    rMatrix_A[5, 4] := 0.000000;
    rMatrix_A[5, 5] := 0.912000; (* Hydrodynamic relaxation / alloy solidification shrinkage *)
    rMatrix_A[5, 6] := 0.001800;
    rMatrix_A[5, 7] := 0.002400; (* Thermal contraction coupling *)
    rMatrix_A[5, 8] := 0.068500; (* Intensifier multiplication effect *)

    (* Row 6: x6 (Cavity Evacuation Vacuum Absolute Pressure [mbar]) *)
    rMatrix_A[6, 1] := 0.000000;
    rMatrix_A[6, 2] := 0.041000; (* Compression of air volume during filling *)
    rMatrix_A[6, 3] := 0.000000;
    rMatrix_A[6, 4] := 0.000000;
    rMatrix_A[6, 5] := 0.000000;
    rMatrix_A[6, 6] := 0.978000; (* Vacuum decay due to mold parting line micro-leakage *)
    rMatrix_A[6, 7] := 0.000500; (* Thermal outgassing expansion *)
    rMatrix_A[6, 8] := 0.000000;

    (* Row 7: x7 (Average Die Steel Surface Temperature [deg C]) *)
    rMatrix_A[7, 1] := 0.000000;
    rMatrix_A[7, 2] := 0.000850; (* Convective heat transfer coefficient enhancement with flow *)
    rMatrix_A[7, 3] := 0.000000;
    rMatrix_A[7, 4] := 0.000000;
    rMatrix_A[7, 5] := 0.001200; (* Latent heat transfer during high-pressure compaction *)
    rMatrix_A[7, 6] := 0.000000;
    rMatrix_A[7, 7] := 0.998200; (* Die thermal inertia time constant (tau = 550 ms) *)
    rMatrix_A[7, 8] := 0.000000;

    (* Row 8: x8 (Intensifier Intermediate Pressure [bar]) *)
    rMatrix_A[8, 1] := 0.000000;
    rMatrix_A[8, 2] := 0.000000;
    rMatrix_A[8, 3] := 0.008400;
    rMatrix_A[8, 4] := 0.000000;
    rMatrix_A[8, 5] := 0.000000;
    rMatrix_A[8, 6] := 0.000000;
    rMatrix_A[8, 7] := 0.000000;
    rMatrix_A[8, 8] := 0.981000; (* Nitrogen piston accumulator discharge rate *)

    (* =============================================================================================================
     * ACTUATOR INPUT COUPLING MATRIX B (8x6)
     * u1: Main Shot Servo Spool Cmd [%]
     * u2: Fast Dump Cartridge [%]
     * u3: Intensifier Spool Cmd [%]
     * u4: Vacuum Assist Throttle [%]
     * u5: Clamping Hydraulic Pres [bar]
     * u6: Die Cooling Flow Rate [%]
     * ============================================================================================================= *)
    rMatrix_B[1, 1] := 0.000050; rMatrix_B[1, 2] := 0.000000; rMatrix_B[1, 3] := 0.000000; rMatrix_B[1, 4] := 0.000000; rMatrix_B[1, 5] := 0.000000; rMatrix_B[1, 6] := 0.000000;
    rMatrix_B[2, 1] := 0.085000; rMatrix_B[2, 2] := 0.065000; rMatrix_B[2, 3] := 0.012000; rMatrix_B[2, 4] := 0.000000; rMatrix_B[2, 5] := 0.000000; rMatrix_B[2, 6] := 0.000000;
    rMatrix_B[3, 1] := 2.850000; rMatrix_B[3, 2] := 1.950000; rMatrix_B[3, 3] := 0.450000; rMatrix_B[3, 4] := 0.000000; rMatrix_B[3, 5] := 0.000000; rMatrix_B[3, 6] := 0.000000;
    rMatrix_B[4, 1] := -0.650000; rMatrix_B[4, 2] := 0.000000; rMatrix_B[4, 3] := 0.000000; rMatrix_B[4, 4] := 0.000000; rMatrix_B[4, 5] := 0.000000; rMatrix_B[4, 6] := 0.000000;
    rMatrix_B[5, 1] := 0.120000; rMatrix_B[5, 2] := 0.085000; rMatrix_B[5, 3] := 4.250000; rMatrix_B[5, 4] := 0.000000; rMatrix_B[5, 5] := 0.000000; rMatrix_B[5, 6] := 0.000000;
    rMatrix_B[6, 1] := 0.000000; rMatrix_B[6, 2] := 0.000000; rMatrix_B[6, 3] := 0.000000; rMatrix_B[6, 4] := -1.850000; rMatrix_B[6, 5] := 0.000000; rMatrix_B[6, 6] := 0.000000;
    rMatrix_B[7, 1] := 0.000000; rMatrix_B[7, 2] := 0.000000; rMatrix_B[7, 3] := 0.000000; rMatrix_B[7, 4] := 0.000000; rMatrix_B[7, 5] := 0.000000; rMatrix_B[7, 6] := -0.054000;
    rMatrix_B[8, 1] := -0.045000; rMatrix_B[8, 2] := -0.125000; rMatrix_B[8, 3] := -0.320000; rMatrix_B[8, 4] := 0.000000; rMatrix_B[8, 5] := 0.000000; rMatrix_B[8, 6] := 0.000000;

    (* =============================================================================================================
     * EXOGENOUS DISTURBANCE COUPLING MATRIX Ew (8x3)
     * w1: Molten alloy viscosity / temperature variation
     * w2: Mold thermal fatigue / gate erosion
     * w3: Main hydraulic pump ripple
     * ============================================================================================================= *)
    rMatrix_Ew[1, 1] := 0.000000; rMatrix_Ew[1, 2] := 0.000000; rMatrix_Ew[1, 3] := 0.000000;
    rMatrix_Ew[2, 1] := -0.024000; rMatrix_Ew[2, 2] := -0.015000; rMatrix_Ew[2, 3] := 0.008000;
    rMatrix_Ew[3, 1] := 0.000000; rMatrix_Ew[3, 2] := 0.000000; rMatrix_Ew[3, 3] := 0.095000;
    rMatrix_Ew[4, 1] := 0.000000; rMatrix_Ew[4, 2] := 0.000000; rMatrix_Ew[4, 3] := 0.045000;
    rMatrix_Ew[5, 1] := -0.185000; rMatrix_Ew[5, 2] := 0.120000; rMatrix_Ew[5, 3] := 0.000000;
    rMatrix_Ew[6, 1] := 0.000000; rMatrix_Ew[6, 2] := 0.082000; rMatrix_Ew[6, 3] := 0.000000;
    rMatrix_Ew[7, 1] := 0.035000; rMatrix_Ew[7, 2] := 0.000000; rMatrix_Ew[7, 3] := 0.000000;
    rMatrix_Ew[8, 1] := 0.000000; rMatrix_Ew[8, 2] := 0.000000; rMatrix_Ew[8, 3] := 0.065000;

    (* =============================================================================================================
     * SENSOR OUTPUT OBSERVATION MATRIX C (6x8)
     * y1: Plunger Linear Position [mm] -> x1
     * y2: Plunger Velocity [m/s] -> x2
     * y3: Shot Cylinder Head Pressure [bar] -> x3
     * y4: Shot Cylinder Rod Pressure [bar] -> x4
     * y5: Cavity Vacuum Pressure [mbar] -> x6
     * y6: Die Steel Temperature [deg C] -> x7
     * ============================================================================================================= *)
    rMatrix_C[1, 1] := 1.0; rMatrix_C[1, 2] := 0.0; rMatrix_C[1, 3] := 0.0; rMatrix_C[1, 4] := 0.0; rMatrix_C[1, 5] := 0.0; rMatrix_C[1, 6] := 0.0; rMatrix_C[1, 7] := 0.0; rMatrix_C[1, 8] := 0.0;
    rMatrix_C[2, 1] := 0.0; rMatrix_C[2, 2] := 1.0; rMatrix_C[2, 3] := 0.0; rMatrix_C[2, 4] := 0.0; rMatrix_C[2, 5] := 0.0; rMatrix_C[2, 6] := 0.0; rMatrix_C[2, 7] := 0.0; rMatrix_C[2, 8] := 0.0;
    rMatrix_C[3, 1] := 0.0; rMatrix_C[3, 2] := 0.0; rMatrix_C[3, 3] := 1.0; rMatrix_C[3, 4] := 0.0; rMatrix_C[3, 5] := 0.0; rMatrix_C[3, 6] := 0.0; rMatrix_C[3, 7] := 0.0; rMatrix_C[3, 8] := 0.0;
    rMatrix_C[4, 1] := 0.0; rMatrix_C[4, 2] := 0.0; rMatrix_C[4, 3] := 0.0; rMatrix_C[4, 4] := 1.0; rMatrix_C[4, 5] := 0.0; rMatrix_C[4, 6] := 0.0; rMatrix_C[4, 7] := 0.0; rMatrix_C[4, 8] := 0.0;
    rMatrix_C[5, 1] := 0.0; rMatrix_C[5, 2] := 0.0; rMatrix_C[5, 3] := 0.0; rMatrix_C[5, 4] := 0.0; rMatrix_C[5, 5] := 0.0; rMatrix_C[5, 6] := 1.0; rMatrix_C[5, 7] := 0.0; rMatrix_C[5, 8] := 0.0;
    rMatrix_C[6, 1] := 0.0; rMatrix_C[6, 2] := 0.0; rMatrix_C[6, 3] := 0.0; rMatrix_C[6, 4] := 0.0; rMatrix_C[6, 5] := 0.0; rMatrix_C[6, 6] := 0.0; rMatrix_C[6, 7] := 1.0; rMatrix_C[6, 8] := 0.0;

    (* =============================================================================================================
     * DIRECT FEEDTHROUGH MATRIX D (6x6)
     * All zero for strictly proper hydraulic causal dynamics
     * ============================================================================================================= *)
    FOR iRow_Idx := 1 TO 6 DO
        FOR iCol_Idx := 1 TO 6 DO
            rMatrix_D[iRow_Idx, iCol_Idx] := 0.0;
        END_FOR;
    END_FOR;

    (* =============================================================================================================
     * STEADY-STATE KALMAN OBSERVER GAIN MATRIX K (8x6)
     * Derived via discrete Riccati equation algebraic solution with process covariance Q_cov and measurement R_cov
     * ============================================================================================================= *)
    rMatrix_K_Kalman[1, 1] := 0.2850; rMatrix_K_Kalman[1, 2] := 0.0120; rMatrix_K_Kalman[1, 3] := 0.0000; rMatrix_K_Kalman[1, 4] := 0.0000; rMatrix_K_Kalman[1, 5] := 0.0000; rMatrix_K_Kalman[1, 6] := 0.0000;
    rMatrix_K_Kalman[2, 1] := 0.0450; rMatrix_K_Kalman[2, 2] := 0.3150; rMatrix_K_Kalman[2, 3] := 0.0015; rMatrix_K_Kalman[2, 4] := -0.0010; rMatrix_K_Kalman[2, 5] := 0.0000; rMatrix_K_Kalman[2, 6] := 0.0000;
    rMatrix_K_Kalman[3, 1] := 0.0000; rMatrix_K_Kalman[3, 2] := -0.0250; rMatrix_K_Kalman[3, 3] := 0.3850; rMatrix_K_Kalman[3, 4] := 0.0000; rMatrix_K_Kalman[3, 5] := 0.0000; rMatrix_K_Kalman[3, 6] := 0.0000;
    rMatrix_K_Kalman[4, 1] := 0.0000; rMatrix_K_Kalman[4, 2] := 0.0180; rMatrix_K_Kalman[4, 3] := 0.0000; rMatrix_K_Kalman[4, 4] := 0.3650; rMatrix_K_Kalman[4, 5] := 0.0000; rMatrix_K_Kalman[4, 6] := 0.0000;
    rMatrix_K_Kalman[5, 1] := 0.0000; rMatrix_K_Kalman[5, 2] := 0.0850; rMatrix_K_Kalman[5, 3] := 0.0450; rMatrix_K_Kalman[5, 4] := -0.0220; rMatrix_K_Kalman[5, 5] := 0.0000; rMatrix_K_Kalman[5, 6] := 0.0010;
    rMatrix_K_Kalman[6, 1] := 0.0000; rMatrix_K_Kalman[6, 2] := 0.0050; rMatrix_K_Kalman[6, 3] := 0.0000; rMatrix_K_Kalman[6, 4] := 0.0000; rMatrix_K_Kalman[6, 5] := 0.4200; rMatrix_K_Kalman[6, 6] := 0.0000;
    rMatrix_K_Kalman[7, 1] := 0.0000; rMatrix_K_Kalman[7, 2] := 0.0000; rMatrix_K_Kalman[7, 3] := 0.0000; rMatrix_K_Kalman[7, 4] := 0.0000; rMatrix_K_Kalman[7, 5] := 0.0000; rMatrix_K_Kalman[7, 6] := 0.2950;
    rMatrix_K_Kalman[8, 1] := 0.0000; rMatrix_K_Kalman[8, 2] := 0.0000; rMatrix_K_Kalman[8, 3] := 0.0520; rMatrix_K_Kalman[8, 4] := 0.0000; rMatrix_K_Kalman[8, 5] := 0.0000; rMatrix_K_Kalman[8, 6] := 0.0000;

    (* =============================================================================================================
     * MPC PENALTY WEIGHTING VECTORS (Q, R, S)
     * Q: Output error penalties (Position, Velocity, Head Pres, Rod Pres, Vacuum, Die Temp)
     * R: Control effort penalties (Servo spool, Cartridge, Intensifier, Vacuum throttle, Clamp, Cooling)
     * S: Actuator slew rate jerk penalties
     * ============================================================================================================= *)
    rMPC_Weight_Q[1] := 15.0;  (* Position error weight *)
    rMPC_Weight_Q[2] := 45.0;  (* Velocity tracking weight (critical for Phase 2 filling speed stability) *)
    rMPC_Weight_Q[3] := 25.0;  (* Head pressure weight *)
    rMPC_Weight_Q[4] := 10.0;  (* Rod backpressure weight *)
    rMPC_Weight_Q[5] := 8.0;   (* Vacuum evacuation weight *)
    rMPC_Weight_Q[6] := 5.0;   (* Die temperature stability weight *)

    rMPC_Weight_R[1] := 0.080; (* Shot servo spool effort *)
    rMPC_Weight_R[2] := 0.050; (* High-speed cartridge effort *)
    rMPC_Weight_R[3] := 0.030; (* Intensifier effort *)
    rMPC_Weight_R[4] := 0.020; (* Vacuum valve effort *)
    rMPC_Weight_R[5] := 0.010; (* Clamp pressure effort *)
    rMPC_Weight_R[6] := 0.015; (* Die cooling effort *)

    rMPC_Weight_S[1] := 0.250; (* Slew jerk penalty on servo spool *)
    rMPC_Weight_S[2] := 0.180; (* Slew penalty on fast dump valve *)
    rMPC_Weight_S[3] := 0.120; (* Slew penalty on intensifier *)
    rMPC_Weight_S[4] := 0.050; (* Slew penalty on vacuum valve *)
    rMPC_Weight_S[5] := 0.040; (* Slew penalty on clamp *)
    rMPC_Weight_S[6] := 0.050; (* Slew penalty on cooling *)

    (* Actuator Box Limits & Maximum Millisecond Slew Rates *)
    rVec_u_MinLimit[1] := -100.0; rVec_u_MaxLimit[1] := 100.0; rVec_du_MaxRate[1] := 15.0; (* 15% per ms max stroke *)
    rVec_u_MinLimit[2] := 0.0;    rVec_u_MaxLimit[2] := 100.0; rVec_du_MaxRate[2] := 20.0;
    rVec_u_MinLimit[3] := 0.0;    rVec_u_MaxLimit[3] := 100.0; rVec_du_MaxRate[3] := 25.0; (* Fast intensifier cartridge *)
    rVec_u_MinLimit[4] := 0.0;    rVec_u_MaxLimit[4] := 100.0; rVec_du_MaxRate[4] := 10.0;
    rVec_u_MinLimit[5] := 0.0;    rVec_u_MaxLimit[5] := 350.0; rVec_du_MaxRate[5] := 25.0;
    rVec_u_MinLimit[6] := 0.0;    rVec_u_MaxLimit[6] := 100.0; rVec_du_MaxRate[6] := 10.0;

    (* =============================================================================================================
     * MULTI-ZONE THERMAL DIE BALANCING PID COEFFICIENTS & TEMPERATURE SETPOINTS (12 ZONES)
     * Fixed Die Half (Zones 1-6), Moving Die Half (Zones 7-12)
     * ============================================================================================================= *)
    (* Zone 1: Fixed Lower Runner *)
    rPID_Kp[1] := 1.85; rPID_Ki[1] := 0.025; rPID_Kd[1] := 0.45; rDieTemp_Setpoint[1] := 240.0;
    (* Zone 2: Fixed Ingate Region *)
    rPID_Kp[2] := 2.20; rPID_Ki[2] := 0.035; rPID_Kd[2] := 0.60; rDieTemp_Setpoint[2] := 260.0;
    (* Zone 3: Fixed Main Cavity Center *)
    rPID_Kp[3] := 1.95; rPID_Ki[3] := 0.030; rPID_Kd[3] := 0.50; rDieTemp_Setpoint[3] := 250.0;
    (* Zone 4: Fixed Upper Cavity Thin Wall *)
    rPID_Kp[4] := 1.70; rPID_Ki[4] := 0.020; rPID_Kd[4] := 0.40; rDieTemp_Setpoint[4] := 255.0;
    (* Zone 5: Fixed Shock-Tower Boss Node *)
    rPID_Kp[5] := 2.50; rPID_Ki[5] := 0.045; rPID_Kd[5] := 0.75; rDieTemp_Setpoint[5] := 235.0;
    (* Zone 6: Fixed Chill Vent Flange *)
    rPID_Kp[6] := 1.50; rPID_Ki[6] := 0.015; rPID_Kd[6] := 0.35; rDieTemp_Setpoint[6] := 210.0;

    (* Zone 7: Moving Biscuit Cup *)
    rPID_Kp[7] := 2.40; rPID_Ki[7] := 0.040; rPID_Kd[7] := 0.70; rDieTemp_Setpoint[7] := 230.0;
    (* Zone 8: Moving Lower Rib Area *)
    rPID_Kp[8] := 1.90; rPID_Ki[8] := 0.028; rPID_Kd[8] := 0.48; rDieTemp_Setpoint[8] := 245.0;
    (* Zone 9: Moving Core Slide Interlock Face A *)
    rPID_Kp[9] := 2.10; rPID_Ki[9] := 0.032; rPID_Kd[9] := 0.55; rDieTemp_Setpoint[9] := 225.0;
    (* Zone 10: Moving Core Slide Interlock Face B *)
    rPID_Kp[10] := 2.10; rPID_Ki[10] := 0.032; rPID_Kd[10] := 0.55; rDieTemp_Setpoint[10] := 225.0;
    (* Zone 11: Moving Center Ejector Cluster *)
    rPID_Kp[11] := 1.80; rPID_Ki[11] := 0.022; rPID_Kd[11] := 0.42; rDieTemp_Setpoint[11] := 240.0;
    (* Zone 12: Moving Chill Block & Vacuum Seal *)
    rPID_Kp[12] := 1.60; rPID_Ki[12] := 0.018; rPID_Kd[12] := 0.38; rDieTemp_Setpoint[12] := 195.0;

    FOR iZone_Loop := 1 TO 12 DO
        rDieTemp_Integral[iZone_Loop] := 0.0;
        rDieTemp_Prev[iZone_Loop] := rDieTemp_Setpoint[iZone_Loop];
    END_FOR;

    (* --- Initialize Statistical History Buffers with Nominal Baseline --- *)
    FOR iSPC_Loop := 1 TO 30 DO
        arrSPC_Biscuit_History[iSPC_Loop] := 25.0;
        arrSPC_PeakVel_History[iSPC_Loop] := 7.5;
        arrSPC_RiseTime_History[iSPC_Loop] := 12.0;
        arrSPC_PeakPres_History[iSPC_Loop] := 760.0;
    END_FOR;

    bStateSpace_Initialized := TRUE;
END_IF;
"""
