# -*- coding: utf-8 -*-
"""
Module: aluminum_potline_builder/mod_matrices_init.py
Initializes matrices A, B, C, D, L, Q, R, S, P and cyber-physical parameters for FB_Metals_Aluminum_HallHeroult_Potline_AnodeEffect_Resistance.
"""

def generate_matrices_init():
    return '''(* =====================================================================================================================
 * PHASE 0: SYSTEM INITIALIZATION & CYBER-PHYSICAL STATE-SPACE PARAMETER TUNING
 * ===================================================================================================================== *)

(* Task scan time capture and clamping *)
IF rCycleTime_sec > 0.005 AND rCycleTime_sec < 2.000 THEN
    rLocalDeltaT_s := rCycleTime_sec;
ELSE
    rLocalDeltaT_s := 0.100; (* Safe fallback execution period 100 ms *)
END_IF;

nScanCounter := nScanCounter + 1;

IF NOT bInitialized THEN
    (* -----------------------------------------------------------------------------------------------------------------
     * DISCRETE STATE TRANSITION MATRIX A (6x6) - Sampled at Ts = 0.100 s
     * States: [x1: dR_pot (uOhm), x2: C_Al2O3 (wt%), x3: T_bath (degC), x4: dACD (mm), x5: BubbleCov (%), x6: MetalPad (cm)]
     * ----------------------------------------------------------------------------------------------------------------- *)
    (* Row 1: dR_pot dynamics *)
    arrA[1, 1] := 0.98520; (* Natural ohmic relaxation decay *)
    arrA[1, 2] := -0.04210; (* Resistance drop with increasing alumina concentration *)
    arrA[1, 3] := -0.00185; (* Bath resistivity decrease with higher temperature *)
    arrA[1, 4] := 0.12870; (* Strong ohmic resistance gradient vs ACD: dR/dACD = rho / A_anode *)
    arrA[1, 5] := 0.03840; (* Resistance increase due to anode gas bubble screening *)
    arrA[1, 6] := -0.00210; (* Minor metal pad wave coupling *)

    (* Row 2: Dissolved Alumina Concentration C_Al2O3 dynamics *)
    arrA[2, 1] := 0.00000; (* No direct feedforward from resistance deviation *)
    arrA[2, 2] := 0.99840; (* Slow mass dissolution kinetic persistence *)
    arrA[2, 3] := 0.00035; (* Enhanced dissolution rate at elevated superheat *)
    arrA[2, 4] := 0.00000; (* Decoupled from ACD *)
    arrA[2, 5] := -0.00012; (* Bubble agitation mass transfer coupling *)
    arrA[2, 6] := 0.00000; (* Decoupled from metal pad *)

    (* Row 3: Electrolyte Bath Temperature T_bath dynamics *)
    arrA[3, 1] := 0.02450; (* Joule heating sensitivity: P_joule = I_line^2 * dR *)
    arrA[3, 2] := -0.01120; (* Endothermic alumina dissolution heat absorption *)
    arrA[3, 3] := 0.99720; (* Massive thermal inertia of 8.2-ton molten cryolite bath *)
    arrA[3, 4] := 0.00315; (* Slight heating increase at higher ACD *)
    arrA[3, 5] := 0.00085; (* Minor bubble insulation effect *)
    arrA[3, 6] := -0.00140; (* Heat sinking into cathode metal pad *)

    (* Row 4: Anode-Cathode Distance dACD dynamics *)
    arrA[4, 1] := 0.00000; (* Open-loop position persistence *)
    arrA[4, 2] := 0.00000;
    arrA[4, 3] := 0.00000;
    arrA[4, 4] := 0.99980; (* Anode carbon consumption erosion rate: ~1.5 mm/day *)
    arrA[4, 5] := 0.00000;
    arrA[4, 6] := -0.00015; (* Aluminum pad level rise reduces ACD *)

    (* Row 5: Anode Gas Bubble Coverage Fraction dynamics *)
    arrA[5, 1] := 0.08200; (* Potential-dependent gas release kinetics *)
    arrA[5, 2] := -0.04500; (* Low alumina causes gas polarization film coalescence *)
    arrA[5, 3] := -0.00550; (* Lower bath viscosity at high temp enhances bubble release *)
    arrA[5, 4] := -0.00210; (* Higher ACD promotes bubble escape path *)
    arrA[5, 5] := 0.89500; (* Rapid bubble formation/detachment dynamics *)
    arrA[5, 6] := 0.00000;

    (* Row 6: Cathode Metal Pad Liquid Level dynamics *)
    arrA[6, 1] := 0.00000;
    arrA[6, 2] := 0.00000;
    arrA[6, 3] := 0.00000;
    arrA[6, 4] := 0.00000;
    arrA[6, 5] := 0.00000;
    arrA[6, 6] := 0.99995; (* Slow Faradaic deposition accumulation of molten Al *)

    (* -----------------------------------------------------------------------------------------------------------------
     * DISCRETE ACTUATOR INPUT MATRIX B (6x5)
     * Inputs: [u1: HoistCmd (mm), u2: FeederRate (ppm), u3: AlF3Hopper (%), u4: ExhaustDamper (%), u5: RodTrim (mm)]
     * ----------------------------------------------------------------------------------------------------------------- *)
    (* Row 1: dR_pot response to actuators *)
    arrB[1, 1] := 0.12870; (* Direct hoist displacement alters ACD, instantaneously changing resistance *)
    arrB[1, 2] := -0.00850; (* Alumina feeding adds charge carriers, suppressing resistance *)
    arrB[1, 3] := 0.00120; (* AlF3 addition shifts liquidus and increases bath resistivity *)
    arrB[1, 4] := 0.00000; (* Exhaust damper has negligible immediate electrical impact *)
    arrB[1, 5] := 0.01540; (* Individual rod trimming balances localized anode current density *)

    (* Row 2: Dissolved Alumina C_Al2O3 response *)
    arrB[2, 1] := 0.00000;
    arrB[2, 2] := 0.01480; (* Volumetric point feeder shots inject 1.0 kg alumina per pulse *)
    arrB[2, 3] := -0.00080; (* Slight dilution effect *)
    arrB[2, 4] := 0.00000;
    arrB[2, 5] := 0.00000;

    (* Row 3: Electrolyte Bath Temperature T_bath response *)
    arrB[3, 1] := 0.00350; (* Raising beam increases voltage and Joule heat generation *)
    arrB[3, 2] := -0.00420; (* Cold alumina feed solids absorb sensible + dissolution heat *)
    arrB[3, 3] := -0.00680; (* AlF3 powder addition has strong localized cooling effect *)
    arrB[3, 4] := -0.02850; (* Opening exhaust damper extracts draft heat from cell hoods *)
    arrB[3, 5] := 0.00000;

    (* Row 4: dACD response *)
    arrB[4, 1] := 1.00000; (* Direct 1:1 electromechanical hoist beam movement *)
    arrB[4, 2] := 0.00000;
    arrB[4, 3] := 0.00000;
    arrB[4, 4] := 0.00000;
    arrB[4, 5] := 0.10000; (* Rod trim offset contribution *)

    (* Row 5: Bubble Coverage response *)
    arrB[5, 1] := -0.08500; (* Raising beam relieves bubble stagnation under anodes *)
    arrB[5, 2] := -0.06200; (* Alumina addition restores surface tension and bubble detachment *)
    arrB[5, 3] := 0.00000;
    arrB[5, 4] := 0.00000;
    arrB[5, 5] := -0.02100;

    (* Row 6: Metal Pad Level response *)
    arrB[6, 1] := 0.00000;
    arrB[6, 2] := 0.00020; (* Alumina feed enables aluminum deposition *)
    arrB[6, 3] := 0.00000;
    arrB[6, 4] := 0.00000;
    arrB[6, 5] := 0.00000;

    (* -----------------------------------------------------------------------------------------------------------------
     * DISCRETE OUTPUT OBSERVER MATRIX C (6x6)
     * Sensors: [y1: V_cell (V), y2: I_line (kA), y3: T_bath (degC), y4: Pos_beam (mm), y5: BubbleNoise, y6: PadLevel]
     * ----------------------------------------------------------------------------------------------------------------- *)
    (* y1: Cell Voltage: V = E_emf + I_line * R_pot *)
    arrC[1, 1] := 0.50000; (* Sensitivity: 500 kA * 1.0 uOhm = 0.500 V *)
    arrC[1, 2] := -0.02100;
    arrC[1, 3] := -0.00095;
    arrC[1, 4] := 0.06435; (* 0.500 V/uOhm * 0.1287 uOhm/mm = 0.06435 V/mm *)
    arrC[1, 5] := 0.01920;
    arrC[1, 6] := 0.00000;

    (* y2: Potline DC Current: Pot operates in constant-current series line *)
    arrC[2, 1] := 0.00000;
    arrC[2, 2] := 0.00000;
    arrC[2, 3] := 0.00000;
    arrC[2, 4] := 0.00000;
    arrC[2, 5] := 0.00000;
    arrC[2, 6] := 0.00000;

    (* y3: Bath Temperature Sensor *)
    arrC[3, 1] := 0.00000;
    arrC[3, 2] := 0.00000;
    arrC[3, 3] := 1.00000; (* Direct temperature measurement *)
    arrC[3, 4] := 0.00000;
    arrC[3, 5] := 0.00000;
    arrC[3, 6] := 0.00000;

    (* y4: Anode Beam Encoder Position *)
    arrC[4, 1] := 0.00000;
    arrC[4, 2] := 0.00000;
    arrC[4, 3] := 0.00000;
    arrC[4, 4] := 1.00000; (* Direct beam elevation measurement *)
    arrC[4, 5] := 0.00000;
    arrC[4, 6] := 0.00000;

    (* y5: Bubble Noise Spectral Variance *)
    arrC[5, 1] := 0.00000;
    arrC[5, 2] := -0.15000;
    arrC[5, 3] := 0.00000;
    arrC[5, 4] := 0.00000;
    arrC[5, 5] := 0.85000; (* Bubble noise strongly correlates with gas coverage fraction *)
    arrC[5, 6] := 0.00000;

    (* y6: Cathode Metal Pad Sounding Level *)
    arrC[6, 1] := 0.00000;
    arrC[6, 2] := 0.00000;
    arrC[6, 3] := 0.00000;
    arrC[6, 4] := 0.00000;
    arrC[6, 5] := 0.00000;
    arrC[6, 6] := 1.00000; (* Direct pad level measurement *)

    (* -----------------------------------------------------------------------------------------------------------------
     * DISCRETE DIRECT FEEDTHROUGH MATRIX D (6x5)
     * ----------------------------------------------------------------------------------------------------------------- *)
    FOR i := 1 TO 6 DO
        FOR j := 1 TO 5 DO
            arrD[i, j] := 0.00000;
        END_FOR;
    END_FOR;

    (* -----------------------------------------------------------------------------------------------------------------
     * LUENBERGER OBSERVER INNOVATION GAIN MATRIX L (6x6)
     * Computes state correction: x_hat[k+1] = A*x_hat[k] + B*u[k] + L*(y[k] - C*x_hat[k])
     * ----------------------------------------------------------------------------------------------------------------- *)
    arrL[1, 1] := 0.42000; arrL[1, 2] := 0.00000; arrL[1, 3] := 0.00500; arrL[1, 4] := 0.03500; arrL[1, 5] := 0.01500; arrL[1, 6] := 0.00000;
    arrL[2, 1] := -0.1850; arrL[2, 2] := 0.00000; arrL[2, 3] := 0.00250; arrL[2, 4] := 0.00000; arrL[2, 5] := -0.0450; arrL[2, 6] := 0.00000;
    arrL[3, 1] := 0.08500; arrL[3, 2] := 0.00000; arrL[3, 3] := 0.55000; arrL[3, 4] := 0.00000; arrL[3, 5] := 0.00000; arrL[3, 6] := -0.0100;
    arrL[4, 1] := 0.12500; arrL[4, 2] := 0.00000; arrL[4, 3] := 0.00000; arrL[4, 4] := 0.65000; arrL[4, 5] := 0.00000; arrL[4, 6] := -0.0500;
    arrL[5, 1] := 0.09500; arrL[5, 2] := 0.00000; arrL[5, 3] := -0.0100; arrL[5, 4] := 0.00000; arrL[5, 5] := 0.48000; arrL[5, 6] := 0.00000;
    arrL[6, 1] := 0.00000; arrL[6, 2] := 0.00000; arrL[6, 3] := -0.0050; arrL[6, 4] := 0.00000; arrL[6, 5] := 0.00000; arrL[6, 6] := 0.72000;

    (* -----------------------------------------------------------------------------------------------------------------
     * MPC QUADRATIC COST MATRICES: Q (6x6), R (5x5), S (5x5), P (6x6)
     * ----------------------------------------------------------------------------------------------------------------- *)
    FOR i := 1 TO 6 DO
        FOR j := 1 TO 6 DO
            arrQ[i, j] := 0.00000;
            arrP[i, j] := 0.00000;
        END_FOR;
    END_FOR;

    FOR i := 1 TO 5 DO
        FOR j := 1 TO 5 DO
            arrR[i, j] := 0.00000;
            arrS[i, j] := 0.00000;
        END_FOR;
    END_FOR;

    (* Q: State Tracking Penalty Weights *)
    arrQ[1, 1] := 185.00; (* Ultra-high penalty on pot pseudo-resistance deviation *)
    arrQ[2, 2] := 240.00; (* Severe penalty on alumina concentration deviation *)
    arrQ[3, 3] := 45.000; (* Thermal balance stability penalty *)
    arrQ[4, 4] := 80.000; (* ACD positioning penalty *)
    arrQ[5, 5] := 65.000; (* Anode gas bubble film coverage penalty *)
    arrQ[6, 6] := 15.000; (* Metal pad reservoir level drift penalty *)

    (* Cross-coupling penalties *)
    arrQ[1, 2] := -18.50; arrQ[2, 1] := -18.50; (* Resistance-Alumina cross penalty *)
    arrQ[1, 4] := 22.000; arrQ[4, 1] := 22.000; (* Resistance-ACD cross penalty *)

    (* R: Actuator Effort Penalty Weights *)
    arrR[1, 1] := 35.000; (* Anode beam hoist mechanical wear penalty *)
    arrR[2, 2] := 8.5000; (* Feeder valve cycle fatigue penalty *)
    arrR[3, 3] := 14.000; (* AlF3 chemical addition expense penalty *)
    arrR[4, 4] := 5.2000; (* Exhaust gas damper modulation penalty *)
    arrR[5, 5] := 25.000; (* Manual anode rod trim actuation penalty *)

    (* S: Actuator Slew Rate Damping Penalty (Delta U) *)
    arrS[1, 1] := 65.000; (* Damping beam jerk to prevent mechanical lash *)
    arrS[2, 2] := 12.000; (* Preventing abrupt alumina feed cycling *)
    arrS[3, 3] := 20.000; (* Damping chemical shocks *)
    arrS[4, 4] := 8.0000; (* Damping duct draft flutter *)
    arrS[5, 5] := 40.000; (* Damping rod adjustments *)

    (* P: Terminal Cost Matrix (Ricatti Solution Steady-State) *)
    arrP[1, 1] := 285.00; arrP[2, 2] := 360.00; arrP[3, 3] := 75.000;
    arrP[4, 4] := 130.00; arrP[5, 5] := 95.000; arrP[6, 6] := 28.000;
    arrP[1, 2] := -26.00; arrP[2, 1] := -26.00;
    arrP[1, 4] := 34.000; arrP[4, 1] := 34.000;

    (* -----------------------------------------------------------------------------------------------------------------
     * ACTUATOR HARDWARE LIMITS & SLEW CONSTRAINTS
     * ----------------------------------------------------------------------------------------------------------------- *)
    arrU_Min[1] := -4.000; (* Max hoist downward step per scan [mm] *)
    arrU_Max[1] :=  4.000; (* Max hoist upward step per scan [mm] *)
    arrDeltaU_Max[1] := 0.800; (* Max hoist slew rate delta [mm/s] *)

    arrU_Min[2] := 0.0000; (* Feeder minimum rate: 0 pulses/min *)
    arrU_Max[2] := 60.000; (* Feeder maximum rate: 60 pulses/min (1 pulse/sec) *)
    arrDeltaU_Max[2] := 5.000; (* Max pulse rate slew [ppm/s] *)

    arrU_Min[3] := 0.0000; (* AlF3 hopper min PWM duty [%] *)
    arrU_Max[3] := 100.00; (* AlF3 hopper max PWM duty [%] *)
    arrDeltaU_Max[3] := 10.00;

    arrU_Min[4] := 15.000; (* Exhaust damper minimum draft position [%] *)
    arrU_Max[4] := 100.00; (* Exhaust damper maximum draft position [%] *)
    arrDeltaU_Max[4] := 12.00;

    arrU_Min[5] := -8.000; (* Anode rod trim minimum [mm] *)
    arrU_Max[5] :=  8.000; (* Anode rod trim maximum [mm] *)
    arrDeltaU_Max[5] := 1.500;

    (* Initial Observer State Vector Seeds *)
    arrX_hat[1] := 0.000;  (* Initial resistance deviation = 0.0 uOhm *)
    arrX_hat[2] := 2.450;  (* Nominal alumina concentration = 2.45 wt% *)
    arrX_hat[3] := 955.00; (* Nominal electrolyte temperature = 955.0 deg C *)
    arrX_hat[4] := 42.000; (* Nominal ACD = 42.0 mm *)
    arrX_hat[5] := 20.000; (* Nominal bubble coverage = 20.0 % *)
    arrX_hat[6] := 20.000; (* Nominal metal pad level = 20.0 cm *)

    FOR i := 1 TO 6 DO
        arrX_hat_prev[i] := arrX_hat[i];
    END_FOR;

    FOR i := 0 TO 31 DO
        arrResRingBuffer[i] := 5.000;
    END_FOR;

    bInitialized := TRUE;
END_IF;
'''
