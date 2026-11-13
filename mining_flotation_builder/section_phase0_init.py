# mining_flotation_builder/section_phase0_init.py
"""
Section: Phase 0 - First-Scan Matrix & Controller Initialization
Function Block: FB_Mining_Flotation_RougherScavenger_FrothDepth_ReagentDosing
"""

def get_phase0_init():
    return """(* ========================================================================= *)
(* === PHASE 0: FIRST-SCAN HARDWARE INITIALIZATION & MATRIX POPULATION   === *)
(* ========================================================================= *)
IF NOT bInitDone THEN
    (* --------------------------------------------------------------------- *)
    (* DISCRETE STATE-SPACE MATRIX A (6x6) DISCRETIZED AT Ts = 20 ms        *)
    (* System States:                                                        *)
    (* x1: Pulp slurry level in rougher cell [mm]                            *)
    (* x2: Froth bed thickness / overflow lip elevation [mm]                 *)
    (* x3: Slurry pulp conditioning tank pH [pH]                             *)
    (* x4: Copper mineral recovery rate [%]                                  *)
    (* x5: Copper concentrate grade [% Cu]                                   *)
    (* x6: Dispersed air holdup gas volume fraction [%]                      *)
    (* --------------------------------------------------------------------- *)
    (* Row 1: Pulp Slurry Level Dynamics (Integrating mass balance with drainage decay) *)
    A_Matrix[1, 1] := 0.998420;  (* x1 -> x1: Hydrostatic level retention with cell underflow self-regulation *)
    A_Matrix[1, 2] := -0.012500; (* x2 -> x1: Hydrostatic backpressure of overlying froth bed on pulp surface *)
    A_Matrix[1, 3] := 0.000000;  (* x3 -> x1: Chemical pH decoupling to slurry level *)
    A_Matrix[1, 4] := 0.000000;  (* x4 -> x1: Mineral recovery rate has negligible direct mass coupling *)
    A_Matrix[1, 5] := 0.000000;  (* x5 -> x1: Concentrate grade mass pull negligible compared to cell volume *)
    A_Matrix[1, 6] := -0.045000; (* x6 -> x1: Gas holdup expansion displaces pulp volume upwards *)

    (* Row 2: Froth Bed Thickness Dynamics (Decoupled multiphase froth accumulation & collapse) *)
    A_Matrix[2, 1] := -0.004500; (* x1 -> x2: Rising pulp level crowds froth lip, decreasing froth bed thickness *)
    A_Matrix[2, 2] := 0.985200;  (* x2 -> x2: Froth bed structural stability and natural drainage retention *)
    A_Matrix[2, 3] := 0.001200;  (* x3 -> x2: pH affects zeta potential and froth stabilization *)
    A_Matrix[2, 4] := 0.002800;  (* x4 -> x2: Mineral loading of hydrophobic particles stabilizes bubbles *)
    A_Matrix[2, 5] := -0.001500; (* x5 -> x2: Heavy chalcopyrite grade loading increases bubble burst rate *)
    A_Matrix[2, 6] := 0.082000;  (* x6 -> x2: Bulk air holdup directly feeds bubble arrival rate at froth base *)

    (* Row 3: Conditioning Tank Slurry pH Neutralization Dynamics (First-order CSTR kinetics) *)
    A_Matrix[3, 1] := 0.000000;  (* x1 -> x3: Pulp level variation does not alter chemical pH *)
    A_Matrix[3, 2] := 0.000000;  (* x2 -> x3: Froth thickness decoupled from chemical titration *)
    A_Matrix[3, 3] := 0.994500;  (* x3 -> x3: Buffering capacity retention of limestone/pyrite matrix *)
    A_Matrix[3, 4] := 0.000000;  (* x4 -> x3: Recovery does not consume hydroxide ions directly *)
    A_Matrix[3, 5] := 0.000000;  (* x5 -> x3: Grade decoupled from solution equilibrium *)
    A_Matrix[3, 6] := 0.000000;  (* x6 -> x3: Aeration CO2 stripping negligible at high alkaline pH *)

    (* Row 4: Copper Mineral Recovery Rate Kinetics (Fast-floating kinetic rate propagation) *)
    A_Matrix[4, 1] := 0.000850;  (* x1 -> x4: Increased pulp level enhances residence time and collection *)
    A_Matrix[4, 2] := -0.003200; (* x2 -> x4: Deeper froth increases detachment drop-back, lowering recovery *)
    A_Matrix[4, 3] := 0.015200;  (* x3 -> x4: Alkaline pH depresses pyrite, promoting chalcopyrite floatability *)
    A_Matrix[4, 4] := 0.988600;  (* x4 -> x4: First-order recovery kinetic persistence *)
    A_Matrix[4, 5] := -0.024500; (* x5 -> x4: Grade-recovery Pareto trade-off coupling *)
    A_Matrix[4, 6] := 0.035400;  (* x6 -> x4: Increased air holdup provides larger bubble surface area flux *)

    (* Row 5: Concentrate Copper Grade Kinetics (Selectivity & entrainment dynamics) *)
    A_Matrix[5, 1] := -0.002100; (* x1 -> x5: Higher pulp level promotes hydraulic entrainment of barren fines *)
    A_Matrix[5, 2] := 0.018500;  (* x2 -> x5: Deeper froth bed provides enhanced drainage and upgrade cleaning *)
    A_Matrix[5, 3] := 0.012800;  (* x3 -> x5: Lime alkalinity prevents iron sulfide pyrite floating into con *)
    A_Matrix[5, 4] := -0.038500; (* x4 -> x5: Higher recovery aggressively pulls middlings, diluting grade *)
    A_Matrix[5, 5] := 0.991200;  (* x5 -> x5: Concentrate grade persistence in overflow launder *)
    A_Matrix[5, 6] := -0.019500; (* x6 -> x5: Excessive air causes turbulences and non-selective mechanical carryover *)

    (* Row 6: Dispersed Air Holdup Gas Fraction Dynamics (Two-phase bubbly flow equilibrium) *)
    A_Matrix[6, 1] := 0.000520;  (* x1 -> x6: Hydrostatic head increases bubble residence time in pulp *)
    A_Matrix[6, 2] := 0.000000;  (* x2 -> x6: Froth bed top thickness decoupled from bottom bubble dispersion *)
    A_Matrix[6, 3] := 0.000000;  (* x3 -> x6: pH ionic strength has minor effect on bubble coalescence *)
    A_Matrix[6, 4] := 0.000000;  (* x4 -> x6: Recovery decoupled from bulk air holdup *)
    A_Matrix[6, 5] := 0.000000;  (* x5 -> x6: Grade decoupled from hydrodynamic gas fraction *)
    A_Matrix[6, 6] := 0.965400;  (* x6 -> x6: Gas holdup dissipation rate via bubble rise and disengagement *)

    (* --------------------------------------------------------------------- *)
    (* DISCRETE INPUT MATRIX B (6x5) DISCRETIZED AT Ts = 20 ms               *)
    (* Actuators u:                                                          *)
    (* u1: Inter-cell pneumatic dart valve position [%]                      *)
    (* u2: Low-pressure aeration blower control damper [%]                   *)
    (* u3: Potassium Amyl Xanthate (PAX) collector pump stroke [%]           *)
    (* u4: MIBC frother metering pump stroke [%]                             *)
    (* u5: Milk of lime slurry modulating control valve [%]                  *)
    (* --------------------------------------------------------------------- *)
    (* Row 1: Pulp Level u-Coupling *)
    B_Matrix[1, 1] := -0.185000; (* u1 -> x1: Opening dart valve discharges slurry, lowering pulp level *)
    B_Matrix[1, 2] := 0.012000;  (* u2 -> x1: Increasing aeration expands pulp volume hydrodynamically *)
    B_Matrix[1, 3] := 0.000000;  (* u3 -> x1: Xanthate volume negligible *)
    B_Matrix[1, 4] := 0.000000;  (* u4 -> x1: Frother volume negligible *)
    B_Matrix[1, 5] := 0.001500;  (* u5 -> x1: Milk of lime slurry hydraulic addition volume *)

    (* Row 2: Froth Bed Thickness u-Coupling *)
    B_Matrix[2, 1] := 0.045000;  (* u1 -> x2: Dropping pulp level increases distance to weir crest, deepening froth *)
    B_Matrix[2, 2] := 0.088000;  (* u2 -> x2: Blower damper increases bubble generation rate, growing froth *)
    B_Matrix[2, 3] := 0.014500;  (* u3 -> x3: Collector hydrophobicity stabilizes mineralized froth layer *)
    B_Matrix[2, 4] := 0.092000;  (* u4 -> x2: MIBC surfactant directly reduces surface tension, building froth *)
    B_Matrix[2, 5] := 0.000000;  (* u5 -> x2: Lime has negligible direct frothing action *)

    (* Row 3: Slurry pH Neutralization u-Coupling *)
    B_Matrix[3, 1] := 0.000000;  (* u1 -> x3: Dart valve does not modulate pH *)
    B_Matrix[3, 2] := 0.000000;  (* u2 -> x3: Aeration does not alter pH significantly *)
    B_Matrix[3, 3] := 0.000000;  (* u3 -> x3: Xanthate collector neutral salt *)
    B_Matrix[3, 4] := 0.000000;  (* u4 -> x3: MIBC frother non-ionic alcohol *)
    B_Matrix[3, 5] := 0.076500;  (* u5 -> x3: Milk of lime Ca(OH)2 strongly drives solution pH alkaline *)

    (* Row 4: Copper Recovery u-Coupling *)
    B_Matrix[4, 1] := -0.004200; (* u1 -> x4: Dart valve discharge short-circuits slurry residence time *)
    B_Matrix[4, 2] := 0.038500;  (* u2 -> x4: Aeration provides gas flux for particle collection *)
    B_Matrix[4, 3] := 0.084500;  (* u3 -> x4: PAX collector chemically activates chalcopyrite hydrophobic float *)
    B_Matrix[4, 4] := 0.026000;  (* u4 -> x4: MIBC frother improves bubble dispersion and carrying capacity *)
    B_Matrix[4, 5] := 0.019500;  (* u5 -> x4: Lime suppresses pyrite competition for collector *)

    (* Row 5: Concentrate Cu Grade u-Coupling *)
    B_Matrix[5, 1] := 0.006800;  (* u1 -> x5: Lowering level creates deeper froth, upgrading concentrate *)
    B_Matrix[5, 2] := -0.042000; (* u2 -> x5: Excess aeration increases gangue hydraulic entrainment *)
    B_Matrix[5, 3] := -0.021000; (* u3 -> x5: Over-collecting floats marginal locked middlings, diluting grade *)
    B_Matrix[5, 4] := -0.018500; (* u4 -> x5: Over-frothing creates wet, watery froth carrying silica slime *)
    B_Matrix[5, 5] := 0.052000;  (* u5 -> x5: Lime addition cleanly drops iron sulfides, boosting Cu grade *)

    (* Row 6: Dispersed Air Holdup u-Coupling *)
    B_Matrix[6, 1] := 0.000000;  (* u1 -> x6: Dart valve decoupled from dispersed bubbly flow fraction *)
    B_Matrix[6, 2] := 0.125000;  (* u2 -> x6: Blower damper directly controls sparging gas holdup *)
    B_Matrix[6, 3] := 0.000000;  (* u3 -> x6: Collector has negligible effect on gas dispersion *)
    B_Matrix[6, 4] := 0.048000;  (* u4 -> x6: MIBC prevents bubble coalescence, creating smaller bubbles & higher holdup *)
    B_Matrix[6, 5] := 0.000000;  (* u5 -> x6: Lime decoupled from gas fraction *)

    (* --------------------------------------------------------------------- *)
    (* DISCRETE MEASUREMENT OUTPUT MATRIX C (6x6)                            *)
    (* Directly maps internal states to voted sensor outputs                 *)
    (* --------------------------------------------------------------------- *)
    C_Matrix[1, 1] := 1.0; C_Matrix[1, 2] := 0.0; C_Matrix[1, 3] := 0.0; C_Matrix[1, 4] := 0.0; C_Matrix[1, 5] := 0.0; C_Matrix[1, 6] := 0.0;
    C_Matrix[2, 1] := 0.0; C_Matrix[2, 2] := 1.0; C_Matrix[2, 3] := 0.0; C_Matrix[2, 4] := 0.0; C_Matrix[2, 5] := 0.0; C_Matrix[2, 6] := 0.0;
    C_Matrix[3, 1] := 0.0; C_Matrix[3, 2] := 0.0; C_Matrix[3, 3] := 1.0; C_Matrix[3, 4] := 0.0; C_Matrix[3, 5] := 0.0; C_Matrix[3, 6] := 0.0;
    C_Matrix[4, 1] := 0.0; C_Matrix[4, 2] := 0.0; C_Matrix[4, 3] := 0.0; C_Matrix[4, 4] := 1.0; C_Matrix[4, 5] := 0.0; C_Matrix[4, 6] := 0.0;
    C_Matrix[5, 1] := 0.0; C_Matrix[5, 2] := 0.0; C_Matrix[5, 3] := 0.0; C_Matrix[5, 4] := 0.0; C_Matrix[5, 5] := 1.0; C_Matrix[5, 6] := 0.0;
    C_Matrix[6, 1] := 0.0; C_Matrix[6, 2] := 0.0; C_Matrix[6, 3] := 0.0; C_Matrix[6, 4] := 0.0; C_Matrix[6, 5] := 0.0; C_Matrix[6, 6] := 1.0;

    (* --------------------------------------------------------------------- *)
    (* DIRECT FEEDTHROUGH MATRIX D (6x5) - ZERO FOR STRICT CAUSALITY         *)
    (* --------------------------------------------------------------------- *)
    D_Matrix[1, 1] := 0.0; D_Matrix[1, 2] := 0.0; D_Matrix[1, 3] := 0.0; D_Matrix[1, 4] := 0.0; D_Matrix[1, 5] := 0.0;
    D_Matrix[2, 1] := 0.0; D_Matrix[2, 2] := 0.0; D_Matrix[2, 3] := 0.0; D_Matrix[2, 4] := 0.0; D_Matrix[2, 5] := 0.0;
    D_Matrix[3, 1] := 0.0; D_Matrix[3, 2] := 0.0; D_Matrix[3, 3] := 0.0; D_Matrix[3, 4] := 0.0; D_Matrix[3, 5] := 0.0;
    D_Matrix[4, 1] := 0.0; D_Matrix[4, 2] := 0.0; D_Matrix[4, 3] := 0.0; D_Matrix[4, 4] := 0.0; D_Matrix[4, 5] := 0.0;
    D_Matrix[5, 1] := 0.0; D_Matrix[5, 2] := 0.0; D_Matrix[5, 3] := 0.0; D_Matrix[5, 4] := 0.0; D_Matrix[5, 5] := 0.0;
    D_Matrix[6, 1] := 0.0; D_Matrix[6, 2] := 0.0; D_Matrix[6, 3] := 0.0; D_Matrix[6, 4] := 0.0; D_Matrix[6, 5] := 0.0;

    (* --------------------------------------------------------------------- *)
    (* LUENBERGER OBSERVER INNOVATION GAIN MATRIX L (6x6)                    *)
    (* Synthesized via discrete Kalman filter algebraic Riccati equation     *)
    (* --------------------------------------------------------------------- *)
    L_Gain[1, 1] := 0.145000; L_Gain[1, 2] := -0.008500; L_Gain[1, 3] := 0.000000; L_Gain[1, 4] := 0.000000; L_Gain[1, 5] := 0.000000; L_Gain[1, 6] := -0.015000;
    L_Gain[2, 1] := -0.006500; L_Gain[2, 2] := 0.165000; L_Gain[2, 3] := 0.001000; L_Gain[2, 4] := 0.002000; L_Gain[2, 5] := -0.001500; L_Gain[2, 6] := 0.022000;
    L_Gain[3, 1] := 0.000000; L_Gain[3, 2] := 0.000000; L_Gain[3, 3] := 0.185000; L_Gain[3, 4] := 0.000000; L_Gain[3, 5] := 0.000000; L_Gain[3, 6] := 0.000000;
    L_Gain[4, 1] := 0.000450; L_Gain[4, 2] := -0.001200; L_Gain[4, 3] := 0.008500; L_Gain[4, 4] := 0.125000; L_Gain[4, 5] := -0.012500; L_Gain[4, 6] := 0.011000;
    L_Gain[5, 1] := -0.001200; L_Gain[5, 2] := 0.008200; L_Gain[5, 3] := 0.006500; L_Gain[5, 4] := -0.015000; L_Gain[5, 5] := 0.155000; L_Gain[5, 6] := -0.008500;
    L_Gain[6, 1] := 0.000300; L_Gain[6, 2] := 0.000000; L_Gain[6, 3] := 0.000000; L_Gain[6, 4] := 0.000000; L_Gain[6, 5] := 0.000000; L_Gain[6, 6] := 0.195000;

    (* --------------------------------------------------------------------- *)
    (* MPC QUADRATIC STATE TRACKING PENALTY MATRIX Q (6x6)                   *)
    (* Heavily penalizes level deviations and metallurgical recovery/grade   *)
    (* --------------------------------------------------------------------- *)
    Q_Weight[1, 1] := 0.045000; Q_Weight[1, 2] := 0.000000; Q_Weight[1, 3] := 0.000000; Q_Weight[1, 4] := 0.000000; Q_Weight[1, 5] := 0.000000; Q_Weight[1, 6] := 0.000000;
    Q_Weight[2, 1] := 0.000000; Q_Weight[2, 2] := 0.120000; Q_Weight[2, 3] := 0.000000; Q_Weight[2, 4] := 0.000000; Q_Weight[2, 5] := 0.000000; Q_Weight[2, 6] := 0.000000;
    Q_Weight[3, 1] := 0.000000; Q_Weight[3, 2] := 0.000000; Q_Weight[3, 3] := 4.500000; Q_Weight[3, 4] := 0.000000; Q_Weight[3, 5] := 0.000000; Q_Weight[3, 6] := 0.000000;
    Q_Weight[4, 1] := 0.000000; Q_Weight[4, 2] := 0.000000; Q_Weight[4, 3] := 0.000000; Q_Weight[4, 4] := 2.850000; Q_Weight[4, 5] := -0.650000; Q_Weight[4, 6] := 0.000000;
    Q_Weight[5, 1] := 0.000000; Q_Weight[5, 2] := 0.000000; Q_Weight[5, 3] := 0.000000; Q_Weight[5, 4] := -0.650000; Q_Weight[5, 5] := 3.650000; Q_Weight[5, 6] := 0.000000;
    Q_Weight[6, 1] := 0.000000; Q_Weight[6, 2] := 0.000000; Q_Weight[6, 3] := 0.000000; Q_Weight[6, 4] := 0.000000; Q_Weight[6, 5] := 0.000000; Q_Weight[6, 6] := 0.250000;

    (* --------------------------------------------------------------------- *)
    (* MPC ACTUATOR EFFORT PENALTY MATRIX R (5x5)                            *)
    (* Penalizes aggressive valve cycling and over-consumption of reagents  *)
    (* --------------------------------------------------------------------- *)
    R_Weight[1, 1] := 0.085000; R_Weight[1, 2] := 0.000000; R_Weight[1, 3] := 0.000000; R_Weight[1, 4] := 0.000000; R_Weight[1, 5] := 0.000000;
    R_Weight[2, 1] := 0.000000; R_Weight[2, 2] := 0.045000; R_Weight[2, 3] := 0.000000; R_Weight[2, 4] := 0.000000; R_Weight[2, 5] := 0.000000;
    R_Weight[3, 1] := 0.000000; R_Weight[3, 2] := 0.000000; R_Weight[3, 3] := 0.350000; R_Weight[3, 4] := 0.000000; R_Weight[3, 5] := 0.000000;
    R_Weight[4, 1] := 0.000000; R_Weight[4, 2] := 0.000000; R_Weight[4, 3] := 0.000000; R_Weight[4, 4] := 0.450000; R_Weight[4, 5] := 0.000000;
    R_Weight[5, 1] := 0.000000; R_Weight[5, 2] := 0.000000; R_Weight[5, 3] := 0.000000; R_Weight[5, 4] := 0.000000; R_Weight[5, 5] := 0.150000;

    (* --------------------------------------------------------------------- *)
    (* MPC SLEW RATE DAMPING PENALTY MATRIX S (5x5)                          *)
    (* Prevents hydraulic water hammer and pneumatic dart valve hunt         *)
    (* --------------------------------------------------------------------- *)
    S_Weight[1, 1] := 0.250000; S_Weight[1, 2] := 0.000000; S_Weight[1, 3] := 0.000000; S_Weight[1, 4] := 0.000000; S_Weight[1, 5] := 0.000000;
    S_Weight[2, 1] := 0.000000; S_Weight[2, 2] := 0.120000; S_Weight[2, 3] := 0.000000; S_Weight[2, 4] := 0.000000; S_Weight[2, 5] := 0.000000;
    S_Weight[3, 1] := 0.000000; S_Weight[3, 2] := 0.000000; S_Weight[3, 3] := 0.550000; S_Weight[3, 4] := 0.000000; S_Weight[3, 5] := 0.000000;
    S_Weight[4, 1] := 0.000000; S_Weight[4, 2] := 0.000000; S_Weight[4, 3] := 0.000000; S_Weight[4, 4] := 0.650000; S_Weight[4, 5] := 0.000000;
    S_Weight[5, 1] := 0.000000; S_Weight[5, 2] := 0.000000; S_Weight[5, 3] := 0.000000; S_Weight[5, 4] := 0.000000; S_Weight[5, 5] := 0.350000;

    (* --------------------------------------------------------------------- *)
    (* MPC TERMINAL STATE COST MATRIX P (6x6)                                *)
    (* Derived from steady-state Riccati solution P = A' * P * A + Q         *)
    (* --------------------------------------------------------------------- *)
    P_Weight[1, 1] := 0.095000; P_Weight[1, 2] := 0.000000; P_Weight[1, 3] := 0.000000; P_Weight[1, 4] := 0.000000; P_Weight[1, 5] := 0.000000; P_Weight[1, 6] := 0.000000;
    P_Weight[2, 1] := 0.000000; P_Weight[2, 2] := 0.285000; P_Weight[2, 3] := 0.000000; P_Weight[2, 4] := 0.000000; P_Weight[2, 5] := 0.000000; P_Weight[2, 6] := 0.000000;
    P_Weight[3, 1] := 0.000000; P_Weight[3, 2] := 0.000000; P_Weight[3, 3] := 8.250000; P_Weight[3, 4] := 0.000000; P_Weight[3, 5] := 0.000000; P_Weight[3, 6] := 0.000000;
    P_Weight[4, 1] := 0.000000; P_Weight[4, 2] := 0.000000; P_Weight[4, 3] := 0.000000; P_Weight[4, 4] := 5.450000; P_Weight[4, 5] := -1.150000; P_Weight[4, 6] := 0.000000;
    P_Weight[5, 1] := 0.000000; P_Weight[5, 2] := 0.000000; P_Weight[5, 3] := 0.000000; P_Weight[5, 4] := -1.150000; P_Weight[5, 5] := 7.150000; P_Weight[5, 6] := 0.000000;
    P_Weight[6, 1] := 0.000000; P_Weight[6, 2] := 0.000000; P_Weight[6, 3] := 0.000000; P_Weight[6, 4] := 0.000000; P_Weight[6, 5] := 0.000000; P_Weight[6, 6] := 0.520000;

    (* --------------------------------------------------------------------- *)
    (* ACTUATOR BOUNDS & MAXIMUM SLEW LIMITS                                 *)
    (* --------------------------------------------------------------------- *)
    u_min[1] := 5.0;   u_max[1] := 95.0;  (* u1 Dart Valve 1: Anti-stiction clamp [%] *)
    u_min[2] := 10.0;  u_max[2] := 95.0;  (* u2 Air Damper: Prevent blower stall [%] *)
    u_min[3] := 0.0;   u_max[3] := 100.0; (* u3 PAX Pump Stroke [%] *)
    u_min[4] := 0.0;   u_max[4] := 100.0; (* u4 MIBC Pump Stroke [%] *)
    u_min[5] := 0.0;   u_max[5] := 95.0;  (* u5 Lime Valve: Scale deposition prevention [%] *)

    du_min[1] := -1.50; du_max[1] := 1.50; (* Dart valve max slew +/- 1.5% per 20 ms scan (75%/sec) *)
    du_min[2] := -2.00; du_max[2] := 2.00; (* Air damper max slew +/- 2.0% per scan *)
    du_min[3] := -0.80; du_max[3] := 0.80; (* PAX pump max slew +/- 0.8% per scan *)
    du_min[4] := -0.80; du_max[4] := 0.80; (* MIBC pump max slew +/- 0.8% per scan *)
    du_min[5] := -1.20; du_max[5] := 1.20; (* Lime pinch valve max slew +/- 1.2% per scan *)

    (* --------------------------------------------------------------------- *)
    (* NOMINAL INITIAL STATE VECTOR ESTIMATE x_hat & ACTUATOR SEEDING        *)
    (* --------------------------------------------------------------------- *)
    x_hat[1] := 3200.0; (* x1: Pulp slurry level [mm] *)
    x_hat[2] := 180.0;  (* x2: Froth bed thickness [mm] *)
    x_hat[3] := 10.50;  (* x3: Pulp pH [pH] *)
    x_hat[4] := 88.50;  (* x4: Copper recovery [%] *)
    x_hat[5] := 28.00;  (* x5: Concentrate grade [% Cu] *)
    x_hat[6] := 14.50;  (* x6: Dispersed air holdup [%] *)

    u_act[1] := 45.0;   (* u1: Dart Valve 1 seed [%] *)
    u_act[2] := 55.0;   (* u2: Air Damper seed [%] *)
    u_act[3] := 35.0;   (* u3: PAX Pump seed [%] *)
    u_act[4] := 28.0;   (* u4: MIBC Pump seed [%] *)
    u_act[5] := 30.0;   (* u5: Lime Valve seed [%] *)

    u_prev[1] := 45.0;
    u_prev[2] := 55.0;
    u_prev[3] := 35.0;
    u_prev[4] := 28.0;
    u_prev[5] := 30.0;

    bInitDone := TRUE;
END_IF;
"""
