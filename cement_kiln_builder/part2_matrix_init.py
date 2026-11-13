# -*- coding: utf-8 -*-
"""
cement_kiln_builder/part2_matrix_init.py
Part 2: Phase 0 - Cold-Start Cyber-Physical State-Space Matrices & Coefficients Initialization
Cell-by-cell assignment of A, B, C, D, L, Q, R, S, P, actuator limits, and reference trajectories.
"""

def get_part2_matrix_init():
    return """
(* ========================================================================================================= *)
(* === PHASE 0: COLD-START CYBER-PHYSICAL STATE-SPACE MATRICES & COEFFICIENTS INITIALIZATION             === *)
(* ========================================================================================================= *)
IF NOT bMatricesInitialized THEN
    (* ----------------------------------------------------------------------------------------------------- *)
    (* SUBSECTION 0.1: DISCRETE STATE TRANSITION MATRIX A (6x6)                                              *)
    (* States:                                                                                               *)
    (*   x1: Burning zone clinkering temperature [deg C] (thermal inertia tau ~ 180 s)                       *)
    (*   x2: Precalciner bottom exit gas temperature [deg C] (fast suspension response tau ~ 25 s)           *)
    (*   x3: Kiln shell maximum hot-spot temperature [deg C] (slow refractory diffusion tau ~ 600 s)        *)
    (*   x4: Precalciner decarbonation degree [%] (strongly coupled with calciner temperature)               *)
    (*   x5: Kiln main drive torque [kNm] (viscous clinker bed hold-up and coating thickness drag)           *)
    (*   x6: Kiln inlet unburnt CO concentration [%] (combustion stoichiometry and flame oxygen balance)      *)
    (* Discretized at Ts = 0.050 s using zero-order hold matrix exponential: A = expm(A_cont * Ts)           *)
    (* ----------------------------------------------------------------------------------------------------- *)
    (* Row 1: Burning Zone Temperature Dynamics *)
    A[1, 1] := 0.997220; (* Self-decay due to radiant heat loss to clinker and kiln hood *)
    A[1, 2] := 0.001850; (* Thermal back-radiation and secondary air preheat carryover from calciner *)
    A[1, 3] := -0.000420; (* Shell thermal leakage sink effect *)
    A[1, 4] := 0.000180; (* Incoming pre-calcined feed enthalpy effect *)
    A[1, 5] := -0.000085; (* Bed thermal load dampening from high solid volume hold-up *)
    A[1, 6] := -0.004500; (* Local reducing conditions cool flame core temperature *)

    (* Row 2: Precalciner Bottom Exit Gas Temperature Dynamics *)
    A[2, 1] := 0.000320; (* Minor convective draft carryover from kiln inlet gas stream *)
    A[2, 2] := 0.991200; (* Rapid gas-suspension convective heat loss and residence time decay *)
    A[2, 3] := -0.000150; (* Precalciner vessel wall refractory transmission dissipation *)
    A[2, 4] := -0.012400; (* Endothermic calcination reaction heat sink (-178 kJ/mol CaCO3) *)
    A[2, 5] := 0.000000; (* Decoupled from rotary kiln mechanical drive torque *)
    A[2, 6] := -0.008500; (* Incomplete combustion quenching of tertiary air flame zone *)

    (* Row 3: Kiln Shell Maximum Hot-Spot Temperature Dynamics *)
    A[3, 1] := 0.000850; (* Thermal conduction through basic refractory lining from clinkering zone *)
    A[3, 2] := 0.000050; (* Kiln inlet gas conduction to upper shell boundary *)
    A[3, 3] := 0.999120; (* Immense thermal capacitance of kiln steel shell (5.6 m diameter x 88 m length) *)
    A[3, 4] := 0.000000; (* Decoupled from suspension decarbonation kinetics *)
    A[3, 5] := 0.000025; (* Frictional heating of tire riding rings and drive contact surfaces *)
    A[3, 6] := 0.000000; (* Zero direct coupling with flue gas CO *)

    (* Row 4: Precalciner Decarbonation Degree Dynamics *)
    A[4, 1] := 0.000120; (* Kiln back-end radiation assisting bottom calcination *)
    A[4, 2] := 0.008450; (* Exponential Arrhenius sensitivity to calciner temperature: k = k0 * exp(-E/RT) *)
    A[4, 3] := 0.000000; (* Independent of outer shell shell temperature *)
    A[4, 4] := 0.994200; (* Residence time washout and fresh raw meal inflow replacement *)
    A[4, 5] := 0.000000; (* Decoupled from mechanical drive torque *)
    A[4, 6] := -0.001200; (* Carbon monoxide inhibits complete oxygen diffusion into calciner fuel *)

    (* Row 5: Kiln Main Drive Mechanical Resistance Torque Dynamics *)
    A[5, 1] := 0.004800; (* Clinker liquid phase formation increases viscous adherence to shell coating *)
    A[5, 2] := 0.000210; (* Raw mix temperature affects inlet bed cascading angle of repose *)
    A[5, 3] := -0.000150; (* Elevated shell temperature causes slight radial thermal expansion *)
    A[5, 4] := -0.002800; (* Higher decarbonation lowers tumbling resistance of pre-sintered meal *)
    A[5, 5] := 0.998400; (* High mechanical rotational inertia of kiln tube and 1,800-ton clinker bed *)
    A[5, 6] := 0.000000; (* Decoupled from gas-phase chemical composition *)

    (* Row 6: Kiln Inlet Carbon Monoxide (CO) Concentration Dynamics *)
    A[6, 1] := -0.000150; (* High burning zone temperature accelerates soot and CO oxidation *)
    A[6, 2] := -0.000080; (* Calciner thermal draft oxidation *)
    A[6, 3] := 0.000000; (* Independent of shell hot spot *)
    A[6, 4] := 0.000000; (* Decoupled from calcite conversion percentage *)
    A[6, 5] := 0.000000; (* Decoupled from drive torque *)
    A[6, 6] := 0.985500; (* Fast atmospheric flue gas transit through kiln chamber (tau ~ 6 s) *)

    (* ----------------------------------------------------------------------------------------------------- *)
    (* SUBSECTION 0.2: ACTUATOR INPUT COUPLING MATRIX B (6x5)                                                *)
    (* Actuators:                                                                                            *)
    (*   u1: Main burner pulverized coal pneumatic feed rate [t/h]                                           *)
    (*   u2: Precalciner fuel feed rate [t/h]                                                                *)
    (*   u3: Kiln rotational drive VFD speed [RPM]                                                           *)
    (*   u4: Preheater Induced Draft (ID) exhaust fan damper [%]                                             *)
    (*   u5: Grate cooler hydraulic cross-bar stroke speed [strokes/min]                                     *)
    (* ----------------------------------------------------------------------------------------------------- *)
    (* Row 1: Effect on Burning Zone Temperature (T_bz) *)
    B[1, 1] := 0.054500; (* Main burner coal directly fuels sintering flame thermal release *)
    B[1, 2] := 0.001200; (* Precalciner fuel slightly preheats secondary air via draft carryover *)
    B[1, 3] := -0.024500; (* Higher RPM pushes cold meal into burning zone faster, depressing temperature *)
    B[1, 4] := 0.003500; (* ID fan draws secondary combustion air through clinker bed *)
    B[1, 5] := 0.008400; (* Faster cooler stroke increases secondary air recuperation temperature *)

    (* Row 2: Effect on Precalciner Bottom Exit Gas Temperature (T_calc) *)
    B[2, 1] := 0.000500; (* Minor kiln flue gas heat carryover to calciner inlet *)
    B[2, 2] := 0.082500; (* Precalciner fuel is primary heat source for suspension furnace *)
    B[2, 3] := -0.001800; (* RPM alters raw meal displacement into calciner discharge duct *)
    B[2, 4] := 0.012500; (* ID fan modulates tertiary air duct draft through calciner chamber *)
    B[2, 5] := 0.002100; (* Cooler stroke speed boosts tertiary air recuperation temperature *)

    (* Row 3: Effect on Kiln Shell Maximum Hot-Spot Temperature (T_shell) *)
    B[3, 1] := 0.003200; (* Excessive main burner fuel overheats refractory and thins coating *)
    B[3, 2] := 0.000100; (* Negligible direct effect from calciner fuel *)
    B[3, 3] := 0.000850; (* Rotation distributes clinker bed cooling around shell circumference *)
    B[3, 4] := 0.000200; (* Draft variations alter internal flame impingement geometry *)
    B[3, 5] := -0.000450; (* Cooler secondary air stabilization prevents flame licking on shell *)

    (* Row 4: Effect on Precalciner Decarbonation Degree (Decarb_pct) *)
    B[4, 1] := 0.000250; (* Slight auxiliary heat influx from kiln gas *)
    B[4, 2] := 0.068500; (* Primary thermal driver: higher calciner fuel yields higher decarbonation *)
    B[4, 3] := -0.014500; (* Higher RPM reduces material residence time in calciner-kiln transition *)
    B[4, 4] := 0.008200; (* ID fan optimizes combustion O2 and gas-solid suspension mixing *)
    B[4, 5] := 0.001800; (* Cooler tertiary air temperature enhances calcination kinetics *)

    (* Row 5: Effect on Kiln Main Drive Torque (Torque_kNm) *)
    B[5, 1] := 0.038500; (* Higher coal increases liquid phase clinker, making bed stickier and heavier *)
    B[5, 2] := -0.002500; (* Good calcination reduces bed density and stickiness at kiln inlet *)
    B[5, 3] := -0.065000; (* Higher rotational speed flattens the material cascade angle of repose *)
    B[5, 4] := 0.000000; (* Flue gas draft has negligible mechanical impact *)
    B[5, 5] := -0.004500; (* Proper cooler operation avoids clinker back-spill damming kiln nose *)

    (* Row 6: Effect on Kiln Inlet CO Concentration (CO_pct) *)
    B[6, 1] := 0.004200; (* Over-fueling main burner creates reducing zone and unburnt CO *)
    B[6, 2] := 0.000650; (* Calciner unburnt hydrocarbons carried into kiln hood draft *)
    B[6, 3] := 0.000000; (* Drive RPM has zero chemical stoichiometric effect *)
    B[6, 4] := -0.005500; (* Increasing ID fan damper draws more excess oxygen, burning out CO *)
    B[6, 5] := -0.000850; (* More recuperated air assists complete carbon burnout *)

    (* ----------------------------------------------------------------------------------------------------- *)
    (* SUBSECTION 0.3: MEASUREMENT OUTPUT MATRIX C (6x6) & DIRECT FEEDTHROUGH D (6x5)                        *)
    (* Direct state observation through voted pyrometers, thermocouples, gas analyzers, and transducers      *)
    (* ----------------------------------------------------------------------------------------------------- *)
    FOR rLoop_idx_i := 1 TO 6 DO
        FOR rLoop_idx_j := 1 TO 6 DO
            IF rLoop_idx_i = rLoop_idx_j THEN
                C[rLoop_idx_i, rLoop_idx_j] := 1.0; (* Direct unity mapping to sensor measurements *)
            ELSE
                C[rLoop_idx_i, rLoop_idx_j] := 0.0;
            END_IF;
        END_FOR;
    END_FOR;

    FOR rLoop_idx_i := 1 TO 6 DO
        FOR rLoop_idx_m := 1 TO 5 DO
            D[rLoop_idx_i, rLoop_idx_m] := 0.0; (* Purely strictly proper dynamical plant (zero direct feedthrough) *)
        END_FOR;
    END_FOR;

    (* ----------------------------------------------------------------------------------------------------- *)
    (* SUBSECTION 0.4: LUENBERGER OBSERVER INNOVATION GAIN MATRIX L (6x6)                                     *)
    (* Synthesized via steady-state Kalman-Bucy filter / pole placement: poles placed inside |z| < 0.85       *)
    (* ----------------------------------------------------------------------------------------------------- *)
    (* Row 1: Burning Zone Temperature Observer Gain *)
    L[1, 1] := 0.1850; (* Strong feedback from voted burning zone pyrometer *)
    L[1, 2] := 0.0085;
    L[1, 3] := -0.0025;
    L[1, 4] := 0.0040;
    L[1, 5] := -0.0012;
    L[1, 6] := -0.0150;

    (* Row 2: Precalciner Bottom Exit Gas Temperature Observer Gain *)
    L[2, 1] := 0.0045;
    L[2, 2] := 0.2200; (* Strong feedback from voted calciner thermocouples *)
    L[2, 3] := -0.0010;
    L[2, 4] := -0.0350;
    L[2, 5] := 0.0000;
    L[2, 6] := -0.0180;

    (* Row 3: Kiln Shell Maximum Hot-Spot Temperature Observer Gain *)
    L[3, 1] := 0.0120;
    L[3, 2] := 0.0015;
    L[3, 3] := 0.1450; (* Direct feedback from infrared shell thermal scanner *)
    L[3, 4] := 0.0000;
    L[3, 5] := 0.0008;
    L[3, 6] := 0.0000;

    (* Row 4: Precalciner Decarbonation Degree Observer Gain *)
    L[4, 1] := 0.0020;
    L[4, 2] := 0.0480; (* Calciner temperature is primary proxy for decarbonation degree *)
    L[4, 3] := 0.0000;
    L[4, 4] := 0.1650; (* Periodic offline lab / titration update feedback *)
    L[4, 5] := 0.0000;
    L[4, 6] := -0.0080;

    (* Row 5: Kiln Main Drive Mechanical Torque Observer Gain *)
    L[5, 1] := 0.0180;
    L[5, 2] := 0.0012;
    L[5, 3] := -0.0008;
    L[5, 4] := -0.0045;
    L[5, 5] := 0.1950; (* Direct feedback from drive motor shaft torque transducer *)
    L[5, 6] := 0.0000;

    (* Row 6: Kiln Inlet CO Concentration Observer Gain *)
    L[6, 1] := -0.0015;
    L[6, 2] := -0.0010;
    L[6, 3] := 0.0000;
    L[6, 4] := 0.0000;
    L[6, 5] := 0.0000;
    L[6, 6] := 0.2800; (* Fast feedback from laser gas analyzer *)

    (* ----------------------------------------------------------------------------------------------------- *)
    (* SUBSECTION 0.5: MODEL PREDICTIVE CONTROL QUADRATIC PENALTY MATRICES (Q, R, S, P)                      *)
    (* Cost Function: J = sum { (x - x_ref)' * Q * (x - x_ref) + u' * R * u + du' * S * du } + x_N' * P * x_N *)
    (* ----------------------------------------------------------------------------------------------------- *)
    FOR rLoop_idx_i := 1 TO 6 DO
        FOR rLoop_idx_j := 1 TO 6 DO
            Q[rLoop_idx_i, rLoop_idx_j] := 0.0;
            P[rLoop_idx_i, rLoop_idx_j] := 0.0;
        END_FOR;
    END_FOR;

    FOR rLoop_idx_i := 1 TO 5 DO
        FOR rLoop_idx_j := 1 TO 5 DO
            R[rLoop_idx_i, rLoop_idx_j] := 0.0;
            S[rLoop_idx_i, rLoop_idx_j] := 0.0;
        END_FOR;
    END_FOR;

    (* State Error Penalty Weights Q (Diagonal) *)
    Q[1, 1] := 4.5000;  (* Burning zone temperature error penalty (tight clinkering quality control) *)
    Q[2, 2] := 3.2000;  (* Precalciner exit temperature error penalty (fuel efficiency & stable draft) *)
    Q[3, 3] := 8.5000;  (* Shell hot spot penalty (immensely severe to protect refractory lining) *)
    Q[4, 4] := 5.0000;  (* Decarbonation degree penalty (strictly lock target between 92.0% - 95.0%) *)
    Q[5, 5] := 1.2000;  (* Kiln drive torque deviation penalty (prevent ring formation / clinker dam) *)
    Q[6, 6] := 15.0000; (* CO concentration penalty (harsh penalty to prevent preheater explosive deflagration) *)

    (* Terminal State Penalty Weights P = 2.5 * Q (Lyapunov Terminal Stability Guarantee) *)
    P[1, 1] := 11.250;
    P[2, 2] := 8.000;
    P[3, 3] := 21.250;
    P[4, 4] := 12.500;
    P[5, 5] := 3.000;
    P[6, 6] := 37.500;

    (* Actuator Control Energy Penalty Weights R (Diagonal) *)
    R[1, 1] := 0.2500;  (* Main burner coal feed cost penalty *)
    R[2, 2] := 0.2000;  (* Precalciner fuel feed cost penalty *)
    R[3, 3] := 0.4500;  (* Kiln RPM mechanical drive wear penalty *)
    R[4, 4] := 0.1500;  (* Preheater ID fan electrical power consumption penalty *)
    R[5, 5] := 0.1000;  (* Grate cooler hydraulic stroke wear penalty *)

    (* Actuator Slew Rate Suppression Weights S (Diagonal) *)
    S[1, 1] := 1.8500;  (* Slew suppression on main burner coal (prevent thermal shock to burner pipe) *)
    S[2, 2] := 1.5000;  (* Slew suppression on calciner fuel (prevent cyclone flame puffing) *)
    S[3, 3] := 4.2000;  (* Strict slew suppression on kiln RPM (protect massive girth gear & pinions) *)
    S[4, 4] := 1.1000;  (* Slew suppression on ID fan damper (prevent pressure shock in cyclone tower) *)
    S[5, 5] := 0.8500;  (* Slew suppression on cooler hydraulic pump stroke speed *)

    (* ----------------------------------------------------------------------------------------------------- *)
    (* SUBSECTION 0.6: ACTUATOR PHYSICAL BOUNDS & MAXIMUM SLEW LIMITS                                        *)
    (* --------------------------------------------------------------------------------------------------------- *)
    (* u1: Main burner pulverized coal pneumatic feed [t/h] *)
    rActuator_u_min[1] := 5.0;      (* Minimum turn-down flame stability limit [t/h] *)
    rActuator_u_max[1] := 28.0;     (* Maximum thermal burner design capacity [t/h] *)
    rActuator_du_max[1] := 0.15;    (* Maximum change per scan cycle (0.15 t/h per 50 ms = 3.0 t/h/s) *)

    (* u2: Precalciner fuel feed rate [t/h] *)
    rActuator_u_min[2] := 8.0;      (* Minimum calciner flame sustaining limit [t/h] *)
    rActuator_u_max[2] := 42.0;     (* Maximum precalciner firing capacity [t/h] *)
    rActuator_du_max[2] := 0.25;    (* Maximum change per scan cycle [t/h] *)

    (* u3: Kiln rotational drive speed [RPM] *)
    rActuator_u_min[3] := 0.5;      (* Minimum operational bed tumble speed [RPM] *)
    rActuator_u_max[3] := 5.2;      (* Maximum allowable VFD motor mechanical rating [RPM] *)
    rActuator_du_max[3] := 0.015;   (* Smooth speed acceleration limit [RPM] *)

    (* u4: Preheater ID exhaust fan damper position [%] *)
    rActuator_u_min[4] := 15.0;     (* Minimum draft damper travel to avoid motor surge [%] *)
    rActuator_u_max[4] := 98.0;     (* Full open exhaust flow [%] *)
    rActuator_du_max[4] := 0.50;    (* Hydraulic damper slew limit per cycle [%] *)

    (* u5: Grate cooler hydraulic cross-bar stroke speed [strokes/min] *)
    rActuator_u_min[5] := 4.0;      (* Minimum stroke to prevent clinker bed solidification [strokes/min] *)
    rActuator_u_max[5] := 24.0;     (* Maximum hydraulic pump discharge frequency [strokes/min] *)
    rActuator_du_max[5] := 0.20;    (* Slew limit per scan cycle [strokes/min] *)

    (* ----------------------------------------------------------------------------------------------------- *)
    (* SUBSECTION 0.7: NOMINAL STEADY-STATE SETPOINT TARGET REFERENCES                                       *)
    (* ----------------------------------------------------------------------------------------------------- *)
    rState_x_ref[1] := 1450.0;      (* Nominal burning zone clinkering temperature [deg C] *)
    rState_x_ref[2] := 890.0;       (* Nominal precalciner bottom exit gas temperature [deg C] *)
    rState_x_ref[3] := 280.0;       (* Safe continuous kiln shell equilibrium temperature [deg C] *)
    rState_x_ref[4] := 93.5;        (* Optimal hot meal CaCO3 calcination degree [%] *)
    rState_x_ref[5] := 410.0;       (* Nominal kiln main drive mechanical resistance torque [kNm] *)
    rState_x_ref[6] := 0.08;        (* Target kiln inlet residual CO concentration [%] *)

    (* Initial Observer State Vector Setup *)
    rState_x_hat[1] := 1445.0;
    rState_x_hat[2] := 888.0;
    rState_x_hat[3] := 275.0;
    rState_x_hat[4] := 93.0;
    rState_x_hat[5] := 405.0;
    rState_x_hat[6] := 0.07;

    (* Actuator Baseline Operating Points *)
    rActuator_u[1] := 18.5;         (* Main coal: 18.5 t/h *)
    rActuator_u[2] := 28.0;         (* Calciner fuel: 28.0 t/h *)
    rActuator_u[3] := 3.8;          (* Kiln drive: 3.8 RPM *)
    rActuator_u[4] := 72.0;         (* ID Fan: 72.0% damper *)
    rActuator_u[5] := 14.5;         (* Grate cooler: 14.5 strokes/min *)

    FOR rLoop_idx_m := 1 TO 5 DO
        rActuator_u_prev[rLoop_idx_m] := rActuator_u[rLoop_idx_m];
        rActuator_u_opt[rLoop_idx_m]  := rActuator_u[rLoop_idx_m];
    END_FOR;

    bMatricesInitialized := TRUE;
END_IF;
"""
