# phase_generators.py
# Sub-generators for each phase of FB_Plastics_AllElectric_IMM_VPTransfer_CavityPressure

def generate_phase0():
    lines = []
    lines.append("""
(* ==================================================================================================== *)
(* PHASE 0: ONE-SHOT SYSTEM INITIALIZATION & CYBER-PHYSICAL MATRIX ALLOCATION                           *)
(* Discrete Execution Task Cycle: Ts = 1.0 ms (0.001 s). Deterministic Synchronous PLC Task.             *)
(* State Vector x in R^8:                                                                               *)
(*   x[1]: Screw Linear Velocity [mm/s] (0.0 to 350.0)                                                  *)
(*   x[2]: Nozzle Melt Dynamic Pressure [bar] (0.0 to 2,200.0)                                          *)
(*   x[3]: Cavity 1 Direct Piezoelectric Pressure [bar] (0.0 to 1,200.0)                                *)
(*   x[4]: Cavity 4 Direct Piezoelectric Pressure [bar] (0.0 to 1,000.0)                                *)
(*   x[5]: Clamping Unit 4-Tie-Bar Total Tonnage [kN] (0.0 to 26,000.0)                                 *)
(*   x[6]: Mold Cavity Surface Temperature [deg C] (80.0 to 160.0)                                      *)
(*   x[7]: Gate Solidification Frozen Skin Thickness [um] (0.0 to 1,500.0)                              *)
(*   x[8]: Screw Hydraulic/Electric Backpressure [bar] (0.0 to 250.0)                                   *)
(* Control Vector u in R^6:                                                                             *)
(*   u[1]: Injection Servo Drive Current Command [-100.0..100.0] [%]                                    *)
(*   u[2]: Holding Pressure Servo Pressure Command [0.0..2200.0] [bar]                                  *)
(*   u[3]: Plasticizing Extruder Motor Speed [0.0..350.0] [rpm]                                         *)
(*   u[4]: Backpressure Proportional Valve Command [0.0..250.0] [bar]                                   *)
(*   u[5]: Mold Oil Temperature Valve Command [0.0..100.0] [%]                                          *)
(*   u[6]: Clamping Five-Point Toggle Servo Speed [0.0..100.0] [%]                                      *)
(* ==================================================================================================== *)

IF NOT bInitialized THEN
    (* ------------------------------------------------------------------------------------------------ *)
    (* MATRIX A: DISCRETE STATE TRANSITION MATRIX (8x8) at Ts = 1.0 ms                                  *)
    (* Physics: Linearized non-Newtonian shear-thinning melt dynamics, planetary roller screw inertia,  *)
    (* compressible melt column continuity, cavity flow hydraulic resistance, tie-bar elasticity, and   *)
    (* 1D Stefan thermal boundary layer gate skin conduction.                                           *)
    (* ------------------------------------------------------------------------------------------------ *)
    (* Row 1: Screw Linear Velocity x[1] [mm/s] *)
    matA[1, 1] := 0.942000;   (* Servomotor inertia and mechanical damping persistence *)
    matA[1, 2] := -0.014500;  (* Head melt pressure back-force deceleration coupling *)
    matA[1, 3] := -0.003200;  (* Cavity 1 hydraulic resistance reflected upstream *)
    matA[1, 4] := -0.001100;  (* Cavity 4 back-pressure hydraulic transmission *)
    matA[1, 5] := 0.000000;   (* Clamping force decoupled from screw kinematics *)
    matA[1, 6] := 0.002400;   (* Melt thermal expansion reducing viscous shear drag *)
    matA[1, 7] := -0.008500;  (* Gate skin restriction increasing back-pressure drag *)
    matA[1, 8] := -0.018500;  (* Electric backpressure opposing screw linear travel *)

    (* Row 2: Nozzle Melt Dynamic Pressure x[2] [bar] *)
    matA[2, 1] := 1.854000;   (* Screw velocity driving volumetric melt compression *)
    matA[2, 2] := 0.895000;   (* Melt compressibility bulk modulus column relaxation *)
    matA[2, 3] := -0.428000;  (* Melt forward flow into hot runner and cavity 1 *)
    matA[2, 4] := -0.115000;  (* Flow through runner branch into cavity 4 *)
    matA[2, 5] := 0.000000;   (* Mold clamping decoupled from nozzle barrel pressure *)
    matA[2, 6] := -0.112000;  (* Thermal expansion reducing melt effective viscosity *)
    matA[2, 7] := 0.165000;   (* Gate restriction building upstream hydraulic head *)
    matA[2, 8] := 0.045000;   (* Backpressure coupling during pre-decompression *)

    (* Row 3: Cavity 1 Direct Piezoelectric Pressure x[3] [bar] *)
    matA[3, 1] := 0.652000;   (* Volumetric melt delivery driving cavity 1 filling *)
    matA[3, 2] := 0.385000;   (* Upstream nozzle pressure transmission through gate *)
    matA[3, 3] := 0.912000;   (* Cavity volumetric elasticity and melt stiffness *)
    matA[3, 4] := -0.215000;  (* Flow redistribution between cavity branches *)
    matA[3, 5] := 0.004500;   (* Tooling deflection compliance reaction *)
    matA[3, 6] := 0.085000;   (* Mold wall temperature delaying skin formation *)
    matA[3, 7] := -0.245000;  (* Gate frozen skin layer throttling cavity pressure *)
    matA[3, 8] := 0.000000;   (* Backpressure decoupled from sealed cavity *)

    (* Row 4: Cavity 4 Direct Piezoelectric Pressure x[4] [bar] *)
    matA[4, 1] := 0.425000;   (* Screw motion propagating to furthest cavity 4 *)
    matA[4, 2] := 0.215000;   (* Upstream nozzle pressure hydraulic transmission *)
    matA[4, 3] := 0.285000;   (* Manifold cross-talk pressure transmission *)
    matA[4, 4] := 0.898000;   (* Cavity 4 melt compressibility and volume holding *)
    matA[4, 5] := 0.003800;   (* Platen bending elasticity reaction *)
    matA[4, 6] := 0.078000;   (* Mold core surface temperature effect *)
    matA[4, 7] := -0.185000;  (* Gate skin restriction in cavity 4 gate *)
    matA[4, 8] := 0.000000;   (* Backpressure decoupled *)

    (* Row 5: Clamping Unit 4-Tie-Bar Total Tonnage x[5] [kN] *)
    matA[5, 1] := 0.125000;   (* Screw injection surge mechanical reaction force *)
    matA[5, 2] := 0.850000;   (* Sprue nozzle push against stationary platen *)
    matA[5, 3] := 2.450000;   (* Cavity 1 projected area opening force reaction *)
    matA[5, 4] := 2.150000;   (* Cavity 4 projected area opening force reaction *)
    matA[5, 5] := 0.992000;   (* High-tensile alloy tie-bar structural stiffness *)
    matA[5, 6] := 0.320000;   (* Thermal expansion of mold steel blocks *)
    matA[5, 7] := 0.000000;   (* Gate skin thickness decoupled from macro clamp *)
    matA[5, 8] := 0.000000;   (* Backpressure decoupled *)

    (* Row 6: Mold Cavity Surface Temperature x[6] [deg C] *)
    matA[6, 1] := 0.001500;   (* Shear viscous dissipation thermal energy input *)
    matA[6, 2] := 0.003500;   (* High pressure contact conductance enhancement *)
    matA[6, 3] := 0.005200;   (* Cavity 1 hot melt thermal boundary layer flux *)
    matA[6, 4] := 0.004800;   (* Cavity 4 hot melt thermal boundary layer flux *)
    matA[6, 5] := 0.000100;   (* Clamping surface contact conductance coupling *)
    matA[6, 6] := 0.985000;   (* Mold tool steel thermal capacitance decay *)
    matA[6, 7] := -0.012500;  (* Insulating effect of solidified frozen skin layer *)
    matA[6, 8] := 0.000000;   (* Backpressure decoupled *)

    (* Row 7: Gate Solidification Frozen Skin Thickness x[7] [um] *)
    matA[7, 1] := -0.045000;  (* High melt shear velocity scours and melts skin layer *)
    matA[7, 2] := -0.015000;  (* High pressure increases shear stress boundary flow *)
    matA[7, 3] := -0.022000;  (* Flow through gate suppresses frozen layer buildup *)
    matA[7, 4] := -0.011000;  (* Downstream pressure gradient effect *)
    matA[7, 5] := 0.000000;   (* Clamping tonnage decoupled *)
    matA[7, 6] := -0.082000;  (* Higher mold temperature suppresses skin growth *)
    matA[7, 7] := 0.996000;   (* 1D Stefan thermal boundary layer self-persistence *)
    matA[7, 8] := 0.000000;   (* Backpressure decoupled *)

    (* Row 8: Screw Hydraulic/Electric Backpressure x[8] [bar] *)
    matA[8, 1] := 0.035000;   (* Screw reverse motion pumping melt against valve *)
    matA[8, 2] := 0.012000;   (* Melt pressure propagation back through screw flights *)
    matA[8, 3] := 0.000000;   (* Cavity decoupled during plasticizing *)
    matA[8, 4] := 0.000000;   (* Cavity decoupled *)
    matA[8, 5] := 0.000000;   (* Clamping decoupled *)
    matA[8, 6] := -0.005000;  (* Barrel temperature thermal expansion *)
    matA[8, 7] := 0.000000;   (* Gate skin decoupled *)
    matA[8, 8] := 0.945000;   (* Electric backpressure regulator closed-loop damping *)

    (* ------------------------------------------------------------------------------------------------ *)
    (* MATRIX B: MANIPULATED INPUT COUPLING MATRIX (8x6) at Ts = 1.0 ms                                 *)
    (* Inputs: u[1]=Inj Servo Current, u[2]=Hold Press Cmd, u[3]=Screw RPM, u[4]=Backpress Cmd,         *)
    (*         u[5]=Mold Cooling Valve, u[6]=Clamp Toggle Servo                                         *)
    (* ------------------------------------------------------------------------------------------------ *)
    (* Row 1: Screw Velocity x[1] *)
    matB[1, 1] := 2.450000;   (* Injection servo motor current produces direct acceleration *)
    matB[1, 2] := 0.018500;   (* Holding pressure regulator closed-loop velocity trim *)
    matB[1, 3] := -0.005000;  (* Screw rotation produces slight axial reaction torque *)
    matB[1, 4] := -0.012000;  (* Backpressure valve opposes screw linear retreat *)
    matB[1, 5] := 0.000000;   (* Mold cooling decoupled *)
    matB[1, 6] := 0.000000;   (* Clamp toggle decoupled *)

    (* Row 2: Nozzle Pressure x[2] *)
    matB[2, 1] := 4.850000;   (* Injection servo thrust generates rapid melt pressure rise *)
    matB[2, 2] := 0.850000;   (* Holding pressure closed-loop setpoint tracking *)
    matB[2, 3] := 0.120000;   (* Screw rotation shear pumping increases barrel pressure *)
    matB[2, 4] := 0.350000;   (* Backpressure valve directly throttles melt head *)
    matB[2, 5] := 0.000000;   (* Mold cooling decoupled *)
    matB[2, 6] := 0.000000;   (* Clamp toggle decoupled *)

    (* Row 3: Cavity 1 Pressure x[3] *)
    matB[3, 1] := 1.950000;   (* Injection servo thrust transmits into cavity 1 *)
    matB[3, 2] := 0.420000;   (* Holding pressure setpoint directly regulates cavity pack *)
    matB[3, 3] := 0.000000;   (* Screw rotation decoupled during injection/holding *)
    matB[3, 4] := 0.000000;   (* Backpressure valve decoupled *)
    matB[3, 5] := -0.015000;  (* Mold cooling increases melt contraction rate *)
    matB[3, 6] := 0.008000;   (* Clamping force pre-compression coupling *)

    (* Row 4: Cavity 4 Pressure x[4] *)
    matB[4, 1] := 1.250000;   (* Injection servo thrust transmits to cavity 4 *)
    matB[4, 2] := 0.360000;   (* Holding pressure setpoint transmits to cavity 4 *)
    matB[4, 3] := 0.000000;   (* Screw rotation decoupled *)
    matB[4, 4] := 0.000000;   (* Backpressure decoupled *)
    matB[4, 5] := -0.018000;  (* Mold cooling increases contraction *)
    matB[4, 6] := 0.006500;   (* Clamping toggle pre-compression *)

    (* Row 5: Clamping Tonnage x[5] *)
    matB[5, 1] := 0.050000;   (* Injection thrust platen reaction *)
    matB[5, 2] := 0.150000;   (* Holding pressure cavity reaction *)
    matB[5, 3] := 0.000000;   (* Screw rotation decoupled *)
    matB[5, 4] := 0.000000;   (* Backpressure decoupled *)
    matB[5, 5] := 0.050000;   (* Mold oil thermal expansion on tool base *)
    matB[5, 6] := 145.0000;   (* Clamping five-point toggle servo drives high tonnage *)

    (* Row 6: Mold Cavity Temp x[6] *)
    matB[6, 1] := 0.002500;   (* Viscous shear heating dissipation *)
    matB[6, 2] := 0.001200;   (* High pressure contact conductance *)
    matB[6, 3] := 0.000000;   (* Screw rotation decoupled *)
    matB[6, 4] := 0.000000;   (* Backpressure decoupled *)
    matB[6, 5] := -0.450000;  (* Mold oil proportional cooling valve lowers temperature *)
    matB[6, 6] := 0.000000;   (* Clamping toggle decoupled *)

    (* Row 7: Gate Skin Thickness x[7] *)
    matB[7, 1] := -0.085000;  (* Injection velocity shear scours frozen skin *)
    matB[7, 2] := -0.025000;  (* High holding pressure drives shear melt flow *)
    matB[7, 3] := 0.000000;   (* Screw rotation decoupled *)
    matB[7, 4] := 0.000000;   (* Backpressure decoupled *)
    matB[7, 5] := 0.180000;   (* Conformal cooling accelerates gate frozen skin growth *)
    matB[7, 6] := 0.000000;   (* Clamping toggle decoupled *)

    (* Row 8: Backpressure x[8] *)
    matB[8, 1] := 0.020000;   (* Screw axial motion coupling *)
    matB[8, 2] := 0.000000;   (* Holding pressure decoupled during plasticizing *)
    matB[8, 3] := 0.340000;   (* Screw rotation rpm drives melt against backpressure valve *)
    matB[8, 4] := 0.920000;   (* Proportional backpressure valve directly throttles pressure *)
    matB[8, 5] := 0.000000;   (* Mold cooling decoupled *)
    matB[8, 6] := 0.000000;   (* Clamping toggle decoupled *)

    (* ------------------------------------------------------------------------------------------------ *)
    (* MATRIX C: OBSERVATION MEASUREMENT MATRIX (6x8) at Ts = 1.0 ms                                    *)
    (* Outputs: y[1]=Screw Vel, y[2]=Nozzle Press, y[3]=Cavity 1, y[4]=Cavity 4, y[5]=Clamp, y[6]=Mold *)
    (* ------------------------------------------------------------------------------------------------ *)
    matC[1, 1] := 1.000000; matC[1, 2] := 0.000000; matC[1, 3] := 0.000000; matC[1, 4] := 0.000000; matC[1, 5] := 0.000000; matC[1, 6] := 0.000000; matC[1, 7] := 0.000000; matC[1, 8] := 0.000000;
    matC[2, 1] := 0.000000; matC[2, 2] := 1.000000; matC[2, 3] := 0.000000; matC[2, 4] := 0.000000; matC[2, 5] := 0.000000; matC[2, 6] := 0.000000; matC[2, 7] := 0.000000; matC[2, 8] := 0.000000;
    matC[3, 1] := 0.000000; matC[3, 2] := 0.000000; matC[3, 3] := 1.000000; matC[3, 4] := 0.000000; matC[3, 5] := 0.000000; matC[3, 6] := 0.000000; matC[3, 7] := 0.000000; matC[3, 8] := 0.000000;
    matC[4, 1] := 0.000000; matC[4, 2] := 0.000000; matC[4, 3] := 0.000000; matC[4, 4] := 1.000000; matC[4, 5] := 0.000000; matC[4, 6] := 0.000000; matC[4, 7] := 0.000000; matC[4, 8] := 0.000000;
    matC[5, 1] := 0.000000; matC[5, 2] := 0.000000; matC[5, 3] := 0.000000; matC[5, 4] := 0.000000; matC[5, 5] := 1.000000; matC[5, 6] := 0.000000; matC[5, 7] := 0.000000; matC[5, 8] := 0.000000;
    matC[6, 1] := 0.000000; matC[6, 2] := 0.000000; matC[6, 3] := 0.000000; matC[6, 4] := 0.000000; matC[6, 5] := 0.000000; matC[6, 6] := 1.000000; matC[6, 7] := 0.000000; matC[6, 8] := 0.000000;

    (* ------------------------------------------------------------------------------------------------ *)
    (* MATRIX D: DIRECT FEEDTHROUGH COUPLING MATRIX (6x6) at Ts = 1.0 ms                                *)
    (* ------------------------------------------------------------------------------------------------ *)
    matD[1, 1] := 0.015000; matD[1, 2] := 0.000000; matD[1, 3] := 0.000000; matD[1, 4] := 0.000000; matD[1, 5] := 0.000000; matD[1, 6] := 0.000000;
    matD[2, 1] := 0.025000; matD[2, 2] := 0.008000; matD[2, 3] := 0.000000; matD[2, 4] := 0.000000; matD[2, 5] := 0.000000; matD[2, 6] := 0.000000;
    matD[3, 1] := 0.000000; matD[3, 2] := 0.005000; matD[3, 3] := 0.000000; matD[3, 4] := 0.000000; matD[3, 5] := 0.000000; matD[3, 6] := 0.000000;
    matD[4, 1] := 0.000000; matD[4, 2] := 0.003000; matD[4, 3] := 0.000000; matD[4, 4] := 0.000000; matD[4, 5] := 0.000000; matD[4, 6] := 0.000000;
    matD[5, 1] := 0.000000; matD[5, 2] := 0.000000; matD[5, 3] := 0.000000; matD[5, 4] := 0.000000; matD[5, 5] := 0.000000; matD[5, 6] := 0.850000;
    matD[6, 1] := 0.000000; matD[6, 2] := 0.000000; matD[6, 3] := 0.000000; matD[6, 4] := 0.000000; matD[6, 5] := -0.005000; matD[6, 6] := 0.000000;

    (* ------------------------------------------------------------------------------------------------ *)
    (* MATRIX L: LUENBERGER OBSERVER KALMAN INNOVATION MATRIX (8x6) at Ts = 1.0 ms                      *)
    (* Designed via discrete algebraic Riccati pole placement for rapid sub-5 ms error convergence.     *)
    (* ------------------------------------------------------------------------------------------------ *)
    (* State x[1]: Screw Velocity *)
    matL[1, 1] := 0.285000; matL[1, 2] := -0.002500; matL[1, 3] := -0.000800; matL[1, 4] := -0.000300; matL[1, 5] := 0.000000; matL[1, 6] := 0.000500;
    (* State x[2]: Nozzle Pressure *)
    matL[2, 1] := 0.045000; matL[2, 2] := 0.345000; matL[2, 3] := -0.038000; matL[2, 4] := -0.012000; matL[2, 5] := 0.000000; matL[2, 6] := -0.004500;
    (* State x[3]: Cavity 1 Pressure *)
    matL[3, 1] := 0.012000; matL[3, 2] := 0.028000; matL[3, 3] := 0.385000; matL[3, 4] := -0.022000; matL[3, 5] := 0.000100; matL[3, 6] := 0.001800;
    (* State x[4]: Cavity 4 Pressure *)
    matL[4, 1] := 0.008000; matL[4, 2] := 0.015000; matL[4, 3] := 0.032000; matL[4, 4] := 0.365000; matL[4, 5] := 0.000100; matL[4, 6] := 0.001500;
    (* State x[5]: Clamping Tonnage *)
    matL[5, 1] := 0.002000; matL[5, 2] := 0.018000; matL[5, 3] := 0.085000; matL[5, 4] := 0.075000; matL[5, 5] := 0.420000; matL[5, 6] := 0.008500;
    (* State x[6]: Mold Cavity Temperature *)
    matL[6, 1] := 0.000100; matL[6, 2] := 0.000200; matL[6, 3] := 0.000500; matL[6, 4] := 0.000400; matL[6, 5] := 0.000000; matL[6, 6] := 0.295000;
    (* State x[7]: Gate Frozen Skin Thickness *)
    matL[7, 1] := -0.004500; matL[7, 2] := -0.001500; matL[7, 3] := -0.018500; matL[7, 4] := -0.009500; matL[7, 5] := 0.000000; matL[7, 6] := -0.025000;
    (* State x[8]: Screw Backpressure *)
    matL[8, 1] := 0.001500; matL[8, 2] := 0.002500; matL[8, 3] := 0.000000; matL[8, 4] := 0.000000; matL[8, 5] := 0.000000; matL[8, 6] := 0.000000;

    (* ------------------------------------------------------------------------------------------------ *)
    (* MODEL PREDICTIVE CONTROL (MPC) QUADRATIC PENALTY MATRICES (Q, R, S, P)                           *)
    (* ------------------------------------------------------------------------------------------------ *)
    (* Matrix Q (8x8): State Tracking Quadratic Cost Penalties *)
    matQ[1, 1] := 1.850000; matQ[1, 2] := 0.000000; matQ[1, 3] := 0.000000; matQ[1, 4] := 0.000000; matQ[1, 5] := 0.000000; matQ[1, 6] := 0.000000; matQ[1, 7] := 0.000000; matQ[1, 8] := 0.000000;
    matQ[2, 1] := 0.000000; matQ[2, 2] := 0.650000; matQ[2, 3] := 0.000000; matQ[2, 4] := 0.000000; matQ[2, 5] := 0.000000; matQ[2, 6] := 0.000000; matQ[2, 7] := 0.000000; matQ[2, 8] := 0.000000;
    matQ[3, 1] := 0.000000; matQ[3, 2] := 0.000000; matQ[3, 3] := 4.850000; matQ[3, 4] := 0.000000; matQ[3, 5] := 0.000000; matQ[3, 6] := 0.000000; matQ[3, 7] := 0.000000; matQ[3, 8] := 0.000000;
    matQ[4, 1] := 0.000000; matQ[4, 2] := 0.000000; matQ[4, 3] := 0.000000; matQ[4, 4] := 3.950000; matQ[4, 5] := 0.000000; matQ[4, 6] := 0.000000; matQ[4, 7] := 0.000000; matQ[4, 8] := 0.000000;
    matQ[5, 1] := 0.000000; matQ[5, 2] := 0.000000; matQ[5, 3] := 0.000000; matQ[5, 4] := 0.000000; matQ[5, 5] := 0.150000; matQ[5, 6] := 0.000000; matQ[5, 7] := 0.000000; matQ[5, 8] := 0.000000;
    matQ[6, 1] := 0.000000; matQ[6, 2] := 0.000000; matQ[6, 3] := 0.000000; matQ[6, 4] := 0.000000; matQ[6, 5] := 0.000000; matQ[6, 6] := 0.850000; matQ[6, 7] := 0.000000; matQ[6, 8] := 0.000000;
    matQ[7, 1] := 0.000000; matQ[7, 2] := 0.000000; matQ[7, 3] := 0.000000; matQ[7, 4] := 0.000000; matQ[7, 5] := 0.000000; matQ[7, 6] := 0.000000; matQ[7, 7] := 2.450000; matQ[7, 8] := 0.000000;
    matQ[8, 1] := 0.000000; matQ[8, 2] := 0.000000; matQ[8, 3] := 0.000000; matQ[8, 4] := 0.000000; matQ[8, 5] := 0.000000; matQ[8, 6] := 0.000000; matQ[8, 7] := 0.000000; matQ[8, 8] := 0.450000;

    (* Matrix R (6x6): Actuator Effort Quadratic Cost Penalties *)
    matR[1, 1] := 0.055000; matR[1, 2] := 0.000000; matR[1, 3] := 0.000000; matR[1, 4] := 0.000000; matR[1, 5] := 0.000000; matR[1, 6] := 0.000000;
    matR[2, 1] := 0.000000; matR[2, 2] := 0.025000; matR[2, 3] := 0.000000; matR[2, 4] := 0.000000; matR[2, 5] := 0.000000; matR[2, 6] := 0.000000;
    matR[3, 1] := 0.000000; matR[3, 2] := 0.000000; matR[3, 3] := 0.015000; matR[3, 4] := 0.000000; matR[3, 5] := 0.000000; matR[3, 6] := 0.000000;
    matR[4, 1] := 0.000000; matR[4, 2] := 0.000000; matR[4, 3] := 0.000000; matR[4, 4] := 0.035000; matR[4, 5] := 0.000000; matR[4, 6] := 0.000000;
    matR[5, 1] := 0.000000; matR[5, 2] := 0.000000; matR[5, 3] := 0.000000; matR[5, 4] := 0.000000; matR[5, 5] := 0.045000; matR[5, 6] := 0.000000;
    matR[6, 1] := 0.000000; matR[6, 2] := 0.000000; matR[6, 3] := 0.000000; matR[6, 4] := 0.000000; matR[6, 5] := 0.000000; matR[6, 6] := 0.010000;

    (* Matrix S (6x6): Actuator Slew Rate Penalties *)
    matS[1, 1] := 0.125000; matS[1, 2] := 0.000000; matS[1, 3] := 0.000000; matS[1, 4] := 0.000000; matS[1, 5] := 0.000000; matS[1, 6] := 0.000000;
    matS[2, 1] := 0.000000; matS[2, 2] := 0.085000; matS[2, 3] := 0.000000; matS[2, 4] := 0.000000; matS[2, 5] := 0.000000; matS[2, 6] := 0.000000;
    matS[3, 1] := 0.000000; matS[3, 2] := 0.000000; matS[3, 3] := 0.045000; matS[3, 4] := 0.000000; matS[3, 5] := 0.000000; matS[3, 6] := 0.000000;
    matS[4, 1] := 0.000000; matS[4, 2] := 0.000000; matS[4, 3] := 0.000000; matS[4, 4] := 0.065000; matS[4, 5] := 0.000000; matS[4, 6] := 0.000000;
    matS[5, 1] := 0.000000; matS[5, 2] := 0.000000; matS[5, 3] := 0.000000; matS[5, 4] := 0.000000; matS[5, 5] := 0.085000; matS[5, 6] := 0.000000;
    matS[6, 1] := 0.000000; matS[6, 2] := 0.000000; matS[6, 3] := 0.000000; matS[6, 4] := 0.000000; matS[6, 5] := 0.000000; matS[6, 6] := 0.025000;

    (* Matrix P (8x8): Terminal State Riccati Quadratic Penalty Matrix *)
    matP[1, 1] := 3.750000; matP[1, 2] := 0.000000; matP[1, 3] := 0.000000; matP[1, 4] := 0.000000; matP[1, 5] := 0.000000; matP[1, 6] := 0.000000; matP[1, 7] := 0.000000; matP[1, 8] := 0.000000;
    matP[2, 1] := 0.000000; matP[2, 2] := 1.450000; matP[2, 3] := 0.000000; matP[2, 4] := 0.000000; matP[2, 5] := 0.000000; matP[2, 6] := 0.000000; matP[2, 7] := 0.000000; matP[2, 8] := 0.000000;
    matP[3, 1] := 0.000000; matP[3, 2] := 0.000000; matP[3, 3] := 8.950000; matP[3, 4] := 0.000000; matP[3, 5] := 0.000000; matP[3, 6] := 0.000000; matP[3, 7] := 0.000000; matP[3, 8] := 0.000000;
    matP[4, 1] := 0.000000; matP[4, 2] := 0.000000; matP[4, 3] := 0.000000; matP[4, 4] := 7.550000; matP[4, 5] := 0.000000; matP[4, 6] := 0.000000; matP[4, 7] := 0.000000; matP[4, 8] := 0.000000;
    matP[5, 1] := 0.000000; matP[5, 2] := 0.000000; matP[5, 3] := 0.000000; matP[5, 4] := 0.000000; matP[5, 5] := 0.350000; matP[5, 6] := 0.000000; matP[5, 7] := 0.000000; matP[5, 8] := 0.000000;
    matP[6, 1] := 0.000000; matP[6, 2] := 0.000000; matP[6, 3] := 0.000000; matP[6, 4] := 0.000000; matP[6, 5] := 0.000000; matP[6, 6] := 1.750000; matP[6, 7] := 0.000000; matP[6, 8] := 0.000000;
    matP[7, 1] := 0.000000; matP[7, 2] := 0.000000; matP[7, 3] := 0.000000; matP[7, 4] := 0.000000; matP[7, 5] := 0.000000; matP[7, 6] := 0.000000; matP[7, 7] := 4.850000; matP[7, 8] := 0.000000;
    matP[8, 1] := 0.000000; matP[8, 2] := 0.000000; matP[8, 3] := 0.000000; matP[8, 4] := 0.000000; matP[8, 5] := 0.000000; matP[8, 6] := 0.000000; matP[8, 7] := 0.000000; matP[8, 8] := 0.950000;

    (* Actuator Hard Saturation Box Bounds [u_min, u_max] *)
    u_min[1] := -100.0;   u_max[1] := 100.0;    (* Injection Current Command [-100%..+100%] *)
    u_min[2] := 0.0;      u_max[2] := 2200.0;   (* Holding Pressure Command [0..2200 bar] *)
    u_min[3] := 0.0;      u_max[3] := 350.0;    (* Screw Rotation Motor Speed [0..350 rpm] *)
    u_min[4] := 0.0;      u_max[4] := 250.0;    (* Backpressure Valve Command [0..250 bar] *)
    u_min[5] := 0.0;      u_max[5] := 100.0;    (* Mold Oil Cooling Valve [0..100%] *)
    u_min[6] := 0.0;      u_max[6] := 100.0;    (* Clamping Toggle Servo Speed [0..100%] *)

    (* Actuator Maximum Slew Rates Per 1.0 ms Scan *)
    du_max[1] := 12.5;    (* Injection current maximum change: 12.5% per ms *)
    du_max[2] := 55.0;    (* Holding pressure maximum slew: 55.0 bar per ms *)
    du_max[3] := 10.0;    (* Screw motor speed maximum slew: 10.0 rpm per ms *)
    du_max[4] := 15.0;    (* Backpressure valve maximum slew: 15.0 bar per ms *)
    du_max[5] := 2.5;     (* Mold cooling valve maximum slew: 2.5% per ms *)
    du_max[6] := 5.0;     (* Clamping toggle servo maximum slew: 5.0% per ms *)

    (* State Vector Baseline Initialization *)
    x_state[1] := 0.0;    (* Screw linear speed [mm/s] *)
    x_state[2] := 0.0;    (* Nozzle melt pressure [bar] *)
    x_state[3] := 0.0;    (* Cavity 1 piezo pressure [bar] *)
    x_state[4] := 0.0;    (* Cavity 4 piezo pressure [bar] *)
    x_state[5] := 0.0;    (* Clamping tonnage [kN] *)
    x_state[6] := 120.0;  (* Mold tooling surface temperature [deg C] *)
    x_state[7] := 0.0;    (* Gate frozen skin thickness [um] *)
    x_state[8] := 0.0;    (* Backpressure [bar] *)

    FOR i := 1 TO 8 DO
        x_pred[i] := x_state[i];
        x_hat[i]  := x_state[i];
        x_ref[i]  := x_state[i];
    END_FOR;

    FOR j := 1 TO 6 DO
        u_ctrl[j]    := 0.0;
        u_prev[j]    := 0.0;
        u_mpc_opt[j] := 0.0;
    END_FOR;

    bInitialized := TRUE;
END_IF;
""")
    return "".join(lines)
