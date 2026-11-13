# -*- coding: utf-8 -*-
"""
Module: retort_builder/mod_matrices_init.py
Implements Phase 0: Cold-Start Initialization of Discrete State-Space Matrices (A, B, C, D),
MPC Quadratic Cost Matrices (Q, R, S, P), and Actuator Saturation / Slew Rate Limits.
"""

def generate_matrices_init():
    return '''(* =====================================================================================================================
 * PHASE 0: FIRST-PRINCIPLES DISCRETE STATE-SPACE & MPC GAIN MATRICES INITIALIZATION
 * Execution: Cold-start one-shot initialization executed on first PLC scan cycle.
 * Sampling Interval: Ts = 100 ms (0.100 s).
 * State Dimension: n = 8 states; Control Input Dimension: m = 5 actuators; Output Dimension: p = 6 measurements.
 * ===================================================================================================================== *)

IF NOT bInitMatricesComplete THEN
    (* -------------------------------------------------------------------------
     * 1. STATE TRANSITION MATRIX A (8x8)
     * Discrete-time transition dynamics derived from continuous linearized Jacobian
     * expm(A_cont * Ts) for 316L pressure vessel, multiphase thermodynamic mixture,
     * transient conduction into can core, and cumulative microbial lethality kinetics.
     * ------------------------------------------------------------------------- *)
    (* Row 1: Vessel Temperature Tv [deg C] *)
    rA[1, 1] := 0.998450; (* Tv self-retention: thermal inertia of vessel steel and saturated steam-air mass *)
    rA[1, 2] := 0.001250; (* Tv coupling from vessel pressure Pv through Clausius-Clapeyron thermodynamic phase equilibrium *)
    rA[1, 3] := 0.000180; (* Tv feedback from product batch surface boundary layer enthalpy exchange *)
    rA[1, 4] := 0.000000; (* Tv decoupled from internal can pressure *)
    rA[1, 5] := 0.000000; (* Tv decoupled from differential pouch stress *)
    rA[1, 6] := 0.000000; (* Tv decoupled from microbial lethality rate *)
    rA[1, 7] := 0.000000; (* Tv decoupled from cumulative F0 *)
    rA[1, 8] := -0.000025;(* Tv thermal dissipation to bottom sump liquid pool *)

    (* Row 2: Vessel Absolute Pressure Pv [bar] *)
    rA[2, 1] := 0.003150; (* Pv coupling from vessel temperature (saturated steam vapor pressure rise dPsat/dT) *)
    rA[2, 2] := 0.993800; (* Pv self-retention: rapid gaseous expansion and compressibility in free volume *)
    rA[2, 3] := 0.000045; (* Pv minor convective backpressure from batch surface *)
    rA[2, 4] := 0.000000; (* Pv decoupled from internal can pressure *)
    rA[2, 5] := 0.000000; (* Pv decoupled from container wall differential *)
    rA[2, 6] := 0.000000; (* Pv decoupled from microbial kinetics *)
    rA[2, 7] := 0.000000; (* Pv decoupled from cumulative lethality *)
    rA[2, 8] := -0.000015;(* Pv slight volume displacement effect of liquid sump level *)

    (* Row 3: Product Cold-Spot Core Temperature Tcore [deg C] *)
    rA[3, 1] := 0.000425; (* Tcore convective/conductive heat transfer from vessel steam environment *)
    rA[3, 2] := 0.000010; (* Tcore minor heat transfer enhancement from higher ambient steam density *)
    rA[3, 3] := 0.999550; (* Tcore self-retention: high Biot number radial and axial thermal conduction lag *)
    rA[3, 4] := 0.000000; (* Tcore decoupled from container pressure *)
    rA[3, 5] := 0.000000; (* Tcore decoupled from pouch stress *)
    rA[3, 6] := 0.000000; (* Tcore decoupled from lethality rate *)
    rA[3, 7] := 0.000000; (* Tcore decoupled from cumulative F0 *)
    rA[3, 8] := 0.000000; (* Tcore isolated from vessel bottom sump *)

    (* Row 4: Container Internal Pressure Pcan [bar] *)
    rA[4, 1] := 0.000050; (* Pcan container shell radiant and convective heating *)
    rA[4, 2] := 0.000020; (* Pcan container elastic volumetric compliance feedback *)
    rA[4, 3] := 0.001920; (* Pcan internal aqueous product vaporization and headspace air Gay-Lussac expansion *)
    rA[4, 4] := 0.997850; (* Pcan internal pressure retention in hermetically sealed container *)
    rA[4, 5] := 0.000000; (* Pcan internal state dynamics *)
    rA[4, 6] := 0.000000; (* Pcan decoupled from lethality *)
    rA[4, 7] := 0.000000; (* Pcan decoupled from cumulative F0 *)
    rA[4, 8] := 0.000000; (* Pcan decoupled from sump *)

    (* Row 5: Container Differential Stress DeltaP = Pcan - Pv [bar] *)
    rA[5, 1] := -0.003100;(* DeltaP inverse coupling to vessel temperature (Pv rise reduces positive DeltaP) *)
    rA[5, 2] := -0.993780;(* DeltaP direct subtractive coupling to vessel pressure Pv *)
    rA[5, 3] := 0.001920; (* DeltaP additive coupling from internal product temperature heating *)
    rA[5, 4] := 0.997850; (* DeltaP direct additive coupling to internal can pressure Pcan *)
    rA[5, 5] := 0.995800; (* DeltaP structural elasticity stress relaxation of pouch laminate / tinplate *)
    rA[5, 6] := 0.000000; (* DeltaP decoupled from lethality *)
    rA[5, 7] := 0.000000; (* DeltaP decoupled from F0 *)
    rA[5, 8] := 0.000015; (* DeltaP minor hydrostatic impact *)

    (* Row 6: Microbial Lethality Rate L(Tcore) [-] *)
    rA[6, 1] := 0.000000; (* Lethality rate determined strictly by cold-spot temperature *)
    rA[6, 2] := 0.000000; (* Lethality rate independent of pressure *)
    rA[6, 3] := 0.000245; (* Lethality rate linearized sensitivity dL/dTcore around reference datum *)
    rA[6, 4] := 0.000000; (* Lethality rate independent of can pressure *)
    rA[6, 5] := 0.000000; (* Lethality rate independent of wall stress *)
    rA[6, 6] := 0.998950; (* Lethality rate first-order kinetic persistence *)
    rA[6, 7] := 0.000000; (* Lethality rate independent of accumulated integral *)
    rA[6, 8] := 0.000000; (* Lethality rate independent of sump *)

    (* Row 7: Cumulative Sterility Lethality Integral F0 [min] *)
    rA[7, 1] := 0.000000; (* F0 integral purely driven by lethal rate state *)
    rA[7, 2] := 0.000000; (* F0 integral independent of pressure *)
    rA[7, 3] := 0.000000; (* F0 integral driven via L(Tcore) *)
    rA[7, 4] := 0.000000; (* F0 integral independent of can pressure *)
    rA[7, 5] := 0.000000; (* F0 integral independent of pouch stress *)
    rA[7, 6] := 0.001667; (* F0 numerical quadrature integration step: Ts / 60.0 = 0.100 s / 60.0 s/min *)
    rA[7, 7] := 1.000000; (* F0 perfect discrete accumulation integrator *)
    rA[7, 8] := 0.000000; (* F0 independent of sump *)

    (* Row 8: Sump Liquid Water Level Hsump [mm] *)
    rA[8, 1] := 0.001500; (* Hsump steam condensate accumulation on vessel shell walls *)
    rA[8, 2] := 0.000500; (* Hsump minor vapor phase condensation under elevated pressure *)
    rA[8, 3] := 0.000000; (* Hsump decoupled from core temp *)
    rA[8, 4] := 0.000000; (* Hsump decoupled from can pressure *)
    rA[8, 5] := 0.000000; (* Hsump decoupled from pouch stress *)
    rA[8, 6] := 0.000000; (* Hsump decoupled from lethality *)
    rA[8, 7] := 0.000000; (* Hsump decoupled from F0 *)
    rA[8, 8] := 0.999820; (* Hsump liquid gravity pool surface retention *)

    (* -------------------------------------------------------------------------
     * 2. CONTROL INPUT COUPLING MATRIX B (8x5)
     * Actuator Inputs:
     * u[1]: Culinary Steam Modulating Control Valve [%]
     * u[2]: High-Pressure Compressed Air Overpressure Valve [%]
     * u[3]: Sterile Cooling Water Spray Modulating Valve [%]
     * u[4]: Atmospheric Exhaust / Vent Modulating Valve [%]
     * u[5]: Agitation Basket Rotary Drum VFD Speed [RPM]
     * ------------------------------------------------------------------------- *)
    (* State x[1]: Vessel Temperature Tv *)
    rB[1, 1] :=  0.001420; (* Steam valve enthalpy injection *)
    rB[1, 2] := -0.000110; (* Compressed air Joule-Thomson slight chilling effect *)
    rB[1, 3] := -0.003850; (* Cooling water spray rapid latent and sensible heat extraction *)
    rB[1, 4] := -0.000920; (* Vent valve steam exhaust thermal purge *)
    rB[1, 5] :=  0.000025; (* Agitation convective heat transfer coefficient enhancement *)

    (* State x[2]: Vessel Pressure Pv *)
    rB[2, 1] :=  0.001850; (* Steam valve mass inrush and vapor pressure addition *)
    rB[2, 2] :=  0.002650; (* Compressed air overpressure injection (Dalton partial pressure) *)
    rB[2, 3] := -0.004120; (* Cooling water spray causes instantaneous steam vapor collapse *)
    rB[2, 4] := -0.004850; (* Vent valve rapid vessel depressurization *)
    rB[2, 5] :=  0.000000; (* Agitation basket does not alter gas mass *)

    (* State x[3]: Product Core Temperature Tcore *)
    rB[3, 1] :=  0.000035; (* Indirect steam warming through boundary layer *)
    rB[3, 2] :=  0.000000; (* Compressed air does not directly heat product *)
    rB[3, 3] := -0.000120; (* Cold spray external container quenching *)
    rB[3, 4] :=  0.000000; (* Venting does not directly conduct to core *)
    rB[3, 5] :=  0.000055; (* Rotary agitation generates forced internal food convection currents *)

    (* State x[4]: Container Internal Pressure Pcan *)
    rB[4, 1] :=  0.000045; (* Steam heating increases can internal vapor *)
    rB[4, 2] :=  0.000000; (* Overpressure air is external to hermetic container *)
    rB[4, 3] := -0.000150; (* Cold spray causes container internal vapor condensation *)
    rB[4, 4] :=  0.000000; (* Venting external *)
    rB[4, 5] :=  0.000030; (* Agitation accelerates internal thermal equilibration *)

    (* State x[5]: Differential Pressure DeltaP = Pcan - Pv *)
    rB[5, 1] := -0.001805; (* Steam inrush reduces DeltaP by boosting external Pv faster than Pcan *)
    rB[5, 2] := -0.002650; (* Overpressure air reduces DeltaP, preventing can peaking/bursting *)
    rB[5, 3] :=  0.003970; (* Cold water causes steam collapse, causing positive DeltaP spike (BURST RISK!) *)
    rB[5, 4] :=  0.004850; (* Vent valve drops Pv, driving DeltaP positive (BURST RISK!) *)
    rB[5, 5] :=  0.000030; (* Agitation convective dynamic *)

    (* State x[6]: Microbial Lethality Rate L(Tcore) *)
    rB[6, 1] :=  0.000000; (* Lethality governed indirectly via Tcore *)
    rB[6, 2] :=  0.000000;
    rB[6, 3] :=  0.000000;
    rB[6, 4] :=  0.000000;
    rB[6, 5] :=  0.000012; (* Agitation accelerates core heating rate, enhancing kill kinetics *)

    (* State x[7]: Cumulative Lethality F0 *)
    rB[7, 1] :=  0.000000; (* Lethality integral integrated from state x[6] *)
    rB[7, 2] :=  0.000000;
    rB[7, 3] :=  0.000000;
    rB[7, 4] :=  0.000000;
    rB[7, 5] :=  0.000000;

    (* State x[8]: Sump Liquid Water Level Hsump *)
    rB[8, 1] :=  0.005200; (* Steam condensate accumulation in sump *)
    rB[8, 2] :=  0.000000; (* Compressed air is dry, no water addition *)
    rB[8, 3] :=  0.048500; (* Cooling water spray adds liquid volume directly into vessel *)
    rB[8, 4] := -0.001200; (* Vent steam carryover *)
    rB[8, 5] :=  0.000000; (* Rotary drum mechanical *)

    (* -------------------------------------------------------------------------
     * 3. MEASUREMENT MATRIX C (6x8)
     * Reconciled Outputs:
     * y[1]: Vessel Temperature Tv [deg C]
     * y[2]: Vessel Pressure Pv [bar]
     * y[3]: Product Core Temperature Tcore [deg C]
     * y[4]: Differential Pouch Pressure DeltaP [bar]
     * y[5]: Cumulative Sterility F0 [min]
     * y[6]: Sump Liquid Water Level Hsump [mm]
     * ------------------------------------------------------------------------- *)
    (* Initialize all C entries to 0.0 *)
    FOR iIdx1 := 1 TO 6 DO
        FOR iIdx2 := 1 TO 8 DO
            rC[iIdx1, iIdx2] := 0.0;
        END_FOR;
    END_FOR;
    rC[1, 1] := 1.0; (* y[1] measures x[1] *)
    rC[2, 2] := 1.0; (* y[2] measures x[2] *)
    rC[3, 3] := 1.0; (* y[3] measures x[3] *)
    rC[4, 5] := 1.0; (* y[4] measures x[5] (DeltaP) *)
    rC[5, 7] := 1.0; (* y[5] measures x[7] (F0) *)
    rC[6, 8] := 1.0; (* y[6] measures x[8] (Hsump) *)

    (* -------------------------------------------------------------------------
     * 4. DIRECT FEEDTHROUGH MATRIX D (6x5)
     * All direct feedthrough entries are zero (strictly proper cyber-physical system)
     * ------------------------------------------------------------------------- *)
    FOR iIdx1 := 1 TO 6 DO
        FOR iIdx2 := 1 TO 5 DO
            rD[iIdx1, iIdx2] := 0.0;
        END_FOR;
    END_FOR;

    (* -------------------------------------------------------------------------
     * 5. MPC QUADRATIC COST WEIGHTS (Q, R, S, P)
     * ------------------------------------------------------------------------- *)
    (* State Tracking Error Weights Q *)
    rQ_Weights[1] := 15.0;  (* x[1] Vessel Temp tracking penalty *)
    rQ_Weights[2] := 25.0;  (* x[2] Vessel Pressure tracking penalty *)
    rQ_Weights[3] := 8.0;   (* x[3] Can Core Temp tracking penalty *)
    rQ_Weights[4] := 5.0;   (* x[4] Can Internal Pressure penalty *)
    rQ_Weights[5] := 60.0;  (* x[5] CRITICAL: Differential Pouch Stress DeltaP penalty (buckle/burst prevention) *)
    rQ_Weights[6] := 2.0;   (* x[6] Microbial Lethality Rate penalty *)
    rQ_Weights[7] := 40.0;  (* x[7] Cumulative Lethality F0 achievement penalty *)
    rQ_Weights[8] := 3.0;   (* x[8] Sump liquid level penalty *)

    (* Actuator Effort Weights R *)
    rR_Weights[1] := 0.15;  (* u[1] Steam valve throttling penalty *)
    rR_Weights[2] := 0.20;  (* u[2] Compressed air consumption penalty *)
    rR_Weights[3] := 0.18;  (* u[3] Cooling water consumption penalty *)
    rR_Weights[4] := 0.25;  (* u[4] Vent valve opening penalty *)
    rR_Weights[5] := 0.05;  (* u[5] Agitation drum drive electrical energy penalty *)

    (* Actuator Slew Rate Weights S (Rate of Change Suppression) *)
    rS_Weights[1] := 0.45;  (* u[1] Steam valve rate limiter *)
    rS_Weights[2] := 0.35;  (* u[2] Air overpressure valve rate limiter *)
    rS_Weights[3] := 0.50;  (* u[3] Water valve water-hammer prevention *)
    rS_Weights[4] := 0.40;  (* u[4] Vent valve acoustic noise suppression *)
    rS_Weights[5] := 0.60;  (* u[5] Agitation drive mechanical torque slew rate *)

    (* Terminal Horizon Cost Weights P *)
    rP_TerminalWeights[1] := 30.0;
    rP_TerminalWeights[2] := 50.0;
    rP_TerminalWeights[3] := 15.0;
    rP_TerminalWeights[4] := 10.0;
    rP_TerminalWeights[5] := 120.0; (* Extreme terminal penalty on residual pouch stress *)
    rP_TerminalWeights[6] := 4.0;
    rP_TerminalWeights[7] := 80.0;  (* Extreme terminal penalty on F0 deficit *)
    rP_TerminalWeights[8] := 6.0;

    (* -------------------------------------------------------------------------
     * 6. ACTUATOR BOUNDS & SLEW LIMITS
     * ------------------------------------------------------------------------- *)
    rU_LowerBound_pct[1] := 0.0;   rU_UpperBound_pct[1] := 100.0; (* Steam Valve [%] *)
    rU_LowerBound_pct[2] := 0.0;   rU_UpperBound_pct[2] := 100.0; (* Air Valve [%] *)
    rU_LowerBound_pct[3] := 0.0;   rU_UpperBound_pct[3] := 100.0; (* Water Spray Valve [%] *)
    rU_LowerBound_pct[4] := 0.0;   rU_UpperBound_pct[4] := 100.0; (* Vent Valve [%] *)
    rU_LowerBound_pct[5] := 0.0;   rU_UpperBound_pct[5] :=  30.0; (* Agitation Basket [RPM] *)

    rU_SlewLimit_pct_per_s[1] := 5.0;  (* Steam: 5.0 %/s max rate of change *)
    rU_SlewLimit_pct_per_s[2] := 12.0; (* Air: 12.0 %/s rapid counter-pressure response *)
    rU_SlewLimit_pct_per_s[3] := 8.0;  (* Water: 8.0 %/s spray modulation *)
    rU_SlewLimit_pct_per_s[4] := 15.0; (* Vent: 15.0 %/s rapid venting *)
    rU_SlewLimit_pct_per_s[5] := 2.5;  (* Agitation: 2.5 RPM/s gentle acceleration *)

    (* Mark Cold-Start Initialization Complete *)
    bInitMatricesComplete := TRUE;
END_IF;
'''

if __name__ == "__main__":
    m = generate_matrices_init()
    print("Matrix Init length:", len(m))
    print(m[:300])
