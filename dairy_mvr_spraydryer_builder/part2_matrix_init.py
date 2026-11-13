# dairy_mvr_spraydryer_builder/part2_matrix_init.py
# Lumina Cyber-Physical Systems Chair - V7 Max-Persona
# Part 2: First-Scan Initialization of Discrete State-Space Matrices, Observer Gains, MPC Cost Weights & Parameters

def get_part2_matrix_init():
    return """(* === FIRST-SCAN COLD START INITIALIZATION OF CYBER-PHYSICAL MATRICES === *)
IF NOT bInitialized THEN
    (* --------------------------------------------------------------------------------------------- *)
    (* DISCRETE SYSTEM STATE TRANSITION MATRIX A (8x8) at Ts = 0.020 [s]                             *)
    (* Models coupled thin-film hydrodynamic sump, solids concentration, MVR vapor boost,          *)
    (* suction temperature boiling equilibrium, drying tower thermal flux, exhaust humidity,        *)
    (* powder moisture retention kinetics, and falling film recirculation flow momentum.            *)
    (* --------------------------------------------------------------------------------------------- *)
    matA[1, 1] := 0.998200;  matA[1, 2] := -0.000450; matA[1, 3] := -0.000280; matA[1, 4] := 0.000120;
    matA[1, 5] := 0.000000;  matA[1, 6] := 0.000000;  matA[1, 7] := 0.000000;  matA[1, 8] := 0.001250;

    matA[2, 1] := -0.000850; matA[2, 2] := 0.995200;  matA[2, 3] := 0.001150;  matA[2, 4] := 0.000620;
    matA[2, 5] := 0.000000;  matA[2, 6] := 0.000000;  matA[2, 7] := 0.000000;  matA[2, 8] := -0.000350;

    matA[3, 1] := -0.000150; matA[3, 2] := 0.000220;  matA[3, 3] := 0.982400;  matA[3, 4] := 0.012500;
    matA[3, 5] := 0.000000;  matA[3, 6] := 0.000000;  matA[3, 7] := 0.000000;  matA[3, 8] := 0.000080;

    matA[4, 1] := 0.000050;  matA[4, 2] := 0.001850;  matA[4, 3] := 0.003420;  matA[4, 4] := 0.989200;
    matA[4, 5] := 0.000000;  matA[4, 6] := 0.000000;  matA[4, 7] := 0.000000;  matA[4, 8] := 0.000110;

    matA[5, 1] := 0.000000;  matA[5, 2] := 0.000000;  matA[5, 3] := 0.000000;  matA[5, 4] := 0.000000;
    matA[5, 5] := 0.988500;  matA[5, 6] := -0.000820; matA[5, 7] := 0.000150;  matA[5, 8] := 0.000000;

    matA[6, 1] := 0.000000;  matA[6, 2] := -0.000750; matA[6, 3] := 0.000000;  matA[6, 4] := 0.000000;
    matA[6, 5] := -0.004520; matA[6, 6] := 0.978400;  matA[6, 7] := 0.012400;  matA[6, 8] := 0.000000;

    matA[7, 1] := 0.000000;  matA[7, 2] := 0.001520;  matA[7, 3] := 0.000000;  matA[7, 4] := 0.000000;
    matA[7, 5] := -0.002850; matA[7, 6] := 0.003550;  matA[7, 7] := 0.991200;  matA[7, 8] := 0.000000;

    matA[8, 1] := 0.002450;  matA[8, 2] := -0.000380; matA[8, 3] := 0.000120;  matA[8, 4] := 0.000000;
    matA[8, 5] := 0.000000;  matA[8, 6] := 0.000000;  matA[8, 7] := 0.000000;  matA[8, 8] := 0.985400;

    (* --------------------------------------------------------------------------------------------- *)
    (* DISCRETE INPUT CONTROL MATRIX B (8x6) at Ts = 0.020 [s]                                       *)
    (* Inputs: u1=FeedValve, u2=MvrSpeed, u3=SteamValve, u4=AtomizerPress, u5=BurnerGas, u6=ExhaustDamper *)
    (* --------------------------------------------------------------------------------------------- *)
    matB[1, 1] := 0.003450;  matB[1, 2] := -0.000012; matB[1, 3] := 0.000085;
    matB[1, 4] := 0.000000;  matB[1, 5] := 0.000000;  matB[1, 6] := 0.000000;

    matB[2, 1] := -0.004200; matB[2, 2] := 0.000045;  matB[2, 3] := 0.001850;
    matB[2, 4] := 0.000000;  matB[2, 5] := 0.000000;  matB[2, 6] := 0.000000;

    matB[3, 1] := -0.000180; matB[3, 2] := 0.000850;  matB[3, 3] := 0.000420;
    matB[3, 4] := 0.000000;  matB[3, 5] := 0.000000;  matB[3, 6] := 0.000000;

    matB[4, 1] := 0.000210;  matB[4, 2] := 0.000320;  matB[4, 3] := 0.002800;
    matB[4, 4] := 0.000000;  matB[4, 5] := 0.000000;  matB[4, 6] := 0.000000;

    matB[5, 1] := 0.000000;  matB[5, 2] := 0.000000;  matB[5, 3] := 0.000000;
    matB[5, 4] := 0.000000;  matB[5, 5] := 0.008450;  matB[5, 6] := -0.001250;

    matB[6, 1] := 0.000000;  matB[6, 2] := 0.000000;  matB[6, 3] := 0.000000;
    matB[6, 4] := 0.002450;  matB[6, 5] := -0.003600; matB[6, 6] := -0.004850;

    matB[7, 1] := 0.000000;  matB[7, 2] := 0.000000;  matB[7, 3] := 0.000000;
    matB[7, 4] := -0.001850; matB[7, 5] := -0.002150; matB[7, 6] := 0.001150;

    matB[8, 1] := 0.001150;  matB[8, 2] := 0.000008;  matB[8, 3] := 0.000025;
    matB[8, 4] := 0.000000;  matB[8, 5] := 0.000000;  matB[8, 6] := 0.000000;

    (* --------------------------------------------------------------------------------------------- *)
    (* DISCRETE MEASUREMENT MATRIX C (6x8)                                                           *)
    (* Maps 8 states to 6 primary measured transmitter telemetry outputs:                            *)
    (* y1 = Calandria Sump Level [m]                                                                 *)
    (* y2 = Calandria Solids Concentration [% TS]                                                    *)
    (* y3 = MVR Differential Pressure [kPa]                                                          *)
    (* y4 = Spray Chamber Inlet Air Temperature [deg C]                                              *)
    (* y5 = Spray Chamber Exhaust Air Relative Humidity [% RH]                                       *)
    (* y6 = Final Milk Powder Moisture Content [% w/w]                                               *)
    (* --------------------------------------------------------------------------------------------- *)
    matC[1, 1] := 1.000; matC[1, 2] := 0.000; matC[1, 3] := 0.000; matC[1, 4] := 0.000;
    matC[1, 5] := 0.000; matC[1, 6] := 0.000; matC[1, 7] := 0.000; matC[1, 8] := 0.000;

    matC[2, 1] := 0.000; matC[2, 2] := 1.000; matC[2, 3] := 0.000; matC[2, 4] := 0.000;
    matC[2, 5] := 0.000; matC[2, 6] := 0.000; matC[2, 7] := 0.000; matC[2, 8] := 0.000;

    matC[3, 1] := 0.000; matC[3, 2] := 0.000; matC[3, 3] := 1.000; matC[3, 4] := 0.000;
    matC[3, 5] := 0.000; matC[3, 6] := 0.000; matC[3, 7] := 0.000; matC[3, 8] := 0.000;

    matC[4, 1] := 0.000; matC[4, 2] := 0.000; matC[4, 3] := 0.000; matC[4, 4] := 0.000;
    matC[4, 5] := 1.000; matC[4, 6] := 0.000; matC[4, 7] := 0.000; matC[4, 8] := 0.000;

    matC[5, 1] := 0.000; matC[5, 2] := 0.000; matC[5, 3] := 0.000; matC[5, 4] := 0.000;
    matC[5, 5] := 0.000; matC[5, 6] := 1.000; matC[5, 7] := 0.000; matC[5, 8] := 0.000;

    matC[6, 1] := 0.000; matC[6, 2] := 0.000; matC[6, 3] := 0.000; matC[6, 4] := 0.000;
    matC[6, 5] := 0.000; matC[6, 6] := 0.000; matC[6, 7] := 1.000; matC[6, 8] := 0.000;

    (* --------------------------------------------------------------------------------------------- *)
    (* DIRECT FEEDTHROUGH MATRIX D (6x6) - STRICTLY PROPER SYSTEM (ALL ZERO COEFFICIENTS)           *)
    (* --------------------------------------------------------------------------------------------- *)
    FOR i := 1 TO 6 DO
        FOR j := 1 TO 6 DO
            matD[i, j] := 0.000000;
        END_FOR;
    END_FOR;

    (* --------------------------------------------------------------------------------------------- *)
    (* DISCRETE LUENBERGER OBSERVER GAIN MATRIX L (8x6)                                              *)
    (* Synthesized via steady-state discrete Kalman filter algebraic Riccati equation (DARE)         *)
    (* Provides optimal sensor fusion and fast convergence of unmeasured states (x4, x8)             *)
    (* --------------------------------------------------------------------------------------------- *)
    matL[1, 1] := 0.145000; matL[1, 2] := -0.002100; matL[1, 3] := 0.000850;
    matL[1, 4] := 0.000000; matL[1, 5] := 0.000000;  matL[1, 6] := 0.000000;

    matL[2, 1] := -0.003500; matL[2, 2] := 0.165000; matL[2, 3] := 0.004200;
    matL[2, 4] := 0.000000;  matL[2, 5] := 0.000000; matL[2, 6] := 0.000000;

    matL[3, 1] := 0.001200;  matL[3, 2] := 0.002800; matL[3, 3] := 0.225000;
    matL[3, 4] := 0.000000;  matL[3, 5] := 0.000000; matL[3, 6] := 0.000000;

    matL[4, 1] := 0.000650;  matL[4, 2] := 0.008500; matL[4, 3] := 0.045000;
    matL[4, 4] := 0.000000;  matL[4, 5] := 0.000000; matL[4, 6] := 0.000000;

    matL[5, 1] := 0.000000;  matL[5, 2] := 0.000000; matL[5, 3] := 0.000000;
    matL[5, 4] := 0.185000;  matL[5, 5] := -0.003200; matL[5, 6] := 0.000850;

    matL[6, 1] := 0.000000;  matL[6, 2] := -0.001500; matL[6, 3] := 0.000000;
    matL[6, 4] := -0.004800; matL[6, 5] := 0.210000;  matL[6, 6] := 0.015200;

    matL[7, 1] := 0.000000;  matL[7, 2] := 0.002200;  matL[7, 3] := 0.000000;
    matL[7, 4] := -0.002500; matL[7, 5] := 0.008400;  matL[7, 6] := 0.245000;

    matL[8, 1] := 0.045000;  matL[8, 2] := -0.001100; matL[8, 3] := 0.000950;
    matL[8, 4] := 0.000000;  matL[8, 5] := 0.000000;  matL[8, 6] := 0.000000;

    (* --------------------------------------------------------------------------------------------- *)
    (* MODEL PREDICTIVE CONTROL (MPC) COST PENALTY WEIGHTS & ACTUATOR LIMITS                         *)
    (* Diagonal state weights Q, actuator rate weights R, terminal weights P                         *)
    (* --------------------------------------------------------------------------------------------- *)
    vec_diagQ[1] := 12.0;    (* Sump Level Penalty (Tight holdup balance) *)
    vec_diagQ[2] := 45.0;    (* Solids Concentration Penalty (Brix specification critical) *)
    vec_diagQ[3] := 8.50;    (* MVR Boost Pressure Penalty *)
    vec_diagQ[4] := 6.00;    (* Suction Temperature Penalty *)
    vec_diagQ[5] := 35.0;    (* Chamber Inlet Hot Air Temperature Penalty *)
    vec_diagQ[6] := 15.0;    (* Exhaust Air Relative Humidity Penalty *)
    vec_diagQ[7] := 120.0;   (* Final Powder Moisture Penalty (Critical product quality) *)
    vec_diagQ[8] := 10.0;    (* Falling Film Recirculation Velocity Penalty (Prevents tube burnout) *)

    vec_diagR[1] := 2.50;    (* Feed Rate Valve Effort Penalty *)
    vec_diagR[2] := 0.085;   (* MVR Compressor VFD Speed Modulation Penalty *)
    vec_diagR[3] := 4.20;    (* Live Steam Header Valve Effort Penalty *)
    vec_diagR[4] := 0.85;    (* Atomizer Nozzle Delivery Pressure Effort Penalty *)
    vec_diagR[5] := 3.10;    (* Burner Gas Fuel Modulation Effort Penalty *)
    vec_diagR[6] := 1.80;    (* Exhaust Fan Damper Position Effort Penalty *)

    vec_diagP[1] := 24.0;    (* Terminal Sump Level Penalty *)
    vec_diagP[2] := 95.0;    (* Terminal Solids Concentration Penalty *)
    vec_diagP[3] := 18.0;    (* Terminal MVR Pressure Penalty *)
    vec_diagP[4] := 12.0;    (* Terminal Suction Temperature Penalty *)
    vec_diagP[5] := 75.0;    (* Terminal Chamber Inlet Air Temp Penalty *)
    vec_diagP[6] := 30.0;    (* Terminal Exhaust Air RH Penalty *)
    vec_diagP[7] := 260.0;   (* Terminal Powder Moisture Penalty *)
    vec_diagP[8] := 20.0;    (* Terminal Recirculation Velocity Penalty *)

    (* Actuator Box Constraints [uMin, uMax] *)
    vec_uMin[1] := 0.0;      vec_uMax[1] := 100.0;    (* Feed Valve [0.0..100.0 %] *)
    vec_uMin[2] := 3000.0;   vec_uMax[2] := 12000.0;  (* MVR Compressor VFD Speed [3000.0..12000.0 rpm] *)
    vec_uMin[3] := 0.0;      vec_uMax[3] := 100.0;    (* Live Steam Valve [0.0..100.0 %] *)
    vec_uMin[4] := 150.0;    vec_uMax[4] := 250.0;    (* Slurry Atomizer Pressure [150.0..250.0 bar] *)
    vec_uMin[5] := 0.0;      vec_uMax[5] := 100.0;    (* Burner Gas Modulation [0.0..100.0 %] *)
    vec_uMin[6] := 0.0;      vec_uMax[6] := 100.0;    (* Exhaust Damper [0.0..100.0 %] *)

    (* Actuator Dynamic Slew Rate Limiters duMax per 20 ms Cycle *)
    vec_duMax[1] := 0.100;   (* Feed Valve Max 5.0 %/s -> 0.100 % per 20 ms *)
    vec_duMax[2] := 5.000;   (* MVR Speed Max 250.0 rpm/s -> 5.000 rpm per 20 ms *)
    vec_duMax[3] := 0.200;   (* Steam Valve Max 10.0 %/s -> 0.200 % per 20 ms *)
    vec_duMax[4] := 0.300;   (* Atomizer Press Max 15.0 bar/s -> 0.300 bar per 20 ms *)
    vec_duMax[5] := 0.160;   (* Burner Gas Max 8.0 %/s -> 0.160 % per 20 ms *)
    vec_duMax[6] := 0.200;   (* Exhaust Damper Max 10.0 %/s -> 0.200 % per 20 ms *)

    (* Nominal Operating Cyber-Physical Setpoint References *)
    vec_xRef[1] := 1.250;    (* Calandria Sump Level Ref = 1.250 [m] *)
    vec_xRef[2] := 48.50;    (* Concentrated Solids Ref = 48.50 [% TS] *)
    vec_xRef[3] := 38.50;    (* MVR Centrifugal Turbo DP Ref = 38.50 [kPa] *)
    vec_xRef[4] := 62.40;    (* Vapor Suction Temp Ref = 62.40 [deg C] *)
    vec_xRef[5] := 195.00;   (* Tower Inlet Air Temp Ref = 195.00 [deg C] *)
    vec_xRef[6] := 22.40;    (* Exhaust Air RH Ref = 22.40 [% RH] *)
    vec_xRef[7] := 3.850;    (* Final Powder Moisture Ref = 3.850 [% w/w] *)
    vec_xRef[8] := 2.150;    (* Falling Film Recirc Velocity Ref = 2.150 [m/s] *)

    (* Initialize State Estimator with Nominal Operating Vector *)
    FOR i := 1 TO 8 DO
        vec_xEst[i] := vec_xRef[i];
        vec_xPred[i] := vec_xRef[i];
    END_FOR;

    (* Initialize Actuator Previous State Registers *)
    vec_uPrev[1] := 0.0;
    vec_uPrev[2] := 3000.0;
    vec_uPrev[3] := 0.0;
    vec_uPrev[4] := 150.0;
    vec_uPrev[5] := 0.0;
    vec_uPrev[6] := 0.0;

    bInitialized := TRUE;
END_IF;
"""
