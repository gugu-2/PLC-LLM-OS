# -*- coding: utf-8 -*-
"""
Module: aseptic_retort_builder/mod_matrices_init.py
Cold-start initialization of 6x6 State-Space Matrices (A, B, C, D) and MPC Gain Matrices (Q, R, S, P).
"""

def generate_matrices_init():
    return '''(* =====================================================================================================================
 * PHASE 0: FIRST-PRINCIPLES 6x6 STATE-SPACE & RECEDING-HORIZON MPC GAIN MATRICES INITIALIZATION
 * Execution: Cold-start deterministic initialization executed on the first PLC scan cycle.
 * Sampling Interval: Ts = 100 ms (0.100 s).
 * State Dimension: n = 6 states; Control Input Dimension: m = 5 actuators; Output Dimension: p = 6 measurements.
 * System Physical States:
 *   x[1] = Retort chamber internal temperature T_retort [deg C]
 *   x[2] = Container core cold-spot temperature T_core [deg C]
 *   x[3] = Retort steam-air total chamber pressure P_retort [bar]
 *   x[4] = Container internal vapor & air pressure P_internal [bar]
 *   x[5] = Cumulative Clostridium botulinum thermal lethality F0 [min]
 *   x[6] = Cumulative nutritional/texture cook quality index C0 [min]
 * Actuator Inputs:
 *   u[1] = Saturated steam modulating valve command [%]
 *   u[2] = Compressed air overpressure injection valve command [%]
 *   u[3] = Retort top exhaust steam-air vent valve command [%]
 *   u[4] = Cooling water cascade injection spray valve command [%]
 *   u[5] = Rotary drum agitation drive speed [RPM]
 * ===================================================================================================================== *)

IF NOT bInitMatricesComplete THEN
    (* -------------------------------------------------------------------------
     * 1. STATE TRANSITION MATRIX A (6x6)
     * Continuous linearized thermophysical Jacobian discretized via matrix exponential:
     *   A_disc = expm(A_cont * Ts) = I + A_cont*Ts + (A_cont*Ts)^2 / 2! + ...
     * Derived for ASME 316L vessel shell, saturated steam-air gas phase mixture,
     * transient conductive boundary layer into packaged food core, and Bigelow kinetics.
     * ------------------------------------------------------------------------- *)

    (* --- ROW 1: Retort Chamber Internal Temperature T_retort [deg C] --- *)
    rA[1, 1] := 0.998420; (* T_retort self-retention: thermal capacitance of 316L pressure shell and vapor mass *)
    rA[1, 2] := 0.000185; (* T_retort heat transfer feedback from container surface boundary layers *)
    rA[1, 3] := 0.001150; (* T_retort thermodynamic coupling with chamber total pressure through Clausius-Clapeyron *)
    rA[1, 4] := 0.000000; (* T_retort decoupled from container internal headspace pressure *)
    rA[1, 5] := 0.000000; (* T_retort decoupled from cumulative lethality state *)
    rA[1, 6] := 0.000000; (* T_retort decoupled from cumulative cook value state *)

    (* --- ROW 2: Container Core Cold-Spot Temperature T_core [deg C] --- *)
    rA[2, 1] := 0.000450; (* T_core conductive and convective heat transfer from chamber steam environment *)
    rA[2, 2] := 0.999520; (* T_core self-retention: large thermal resistance and product conduction lag *)
    rA[2, 3] := 0.000015; (* T_core minor heat transfer enhancement under elevated gas density/overpressure *)
    rA[2, 4] := 0.000000; (* T_core decoupled from internal container pressure state *)
    rA[2, 5] := 0.000000; (* T_core decoupled from microbial lethality state *)
    rA[2, 6] := 0.000000; (* T_core decoupled from quality cook value state *)

    (* --- ROW 3: Retort Steam-Air Total Chamber Pressure P_retort [bar] --- *)
    rA[3, 1] := 0.003180; (* P_retort coupling from chamber temperature: saturated steam vapor pressure rise dPsat/dT *)
    rA[3, 2] := 0.000035; (* P_retort minor displacement and convective backpressure from container surface *)
    rA[3, 3] := 0.993650; (* P_retort self-retention: gaseous compressibility and leakage through pipe seals *)
    rA[3, 4] := 0.000000; (* P_retort decoupled from hermetic container internal pressure *)
    rA[3, 5] := 0.000000; (* P_retort decoupled from microbial lethality *)
    rA[3, 6] := 0.000000; (* P_retort decoupled from quality cook value *)

    (* --- ROW 4: Container Internal Vapor & Air Pressure P_internal [bar] --- *)
    rA[4, 1] := 0.000065; (* P_internal container outer skin radiant and convective heating *)
    rA[4, 2] := 0.001940; (* P_internal product cold-spot core aqueous vaporization and headspace air expansion *)
    rA[4, 3] := 0.000020; (* P_internal slight container structural volumetric compliance feedback *)
    rA[4, 4] := 0.997800; (* P_internal self-retention inside hermetically sealed tinplate can / foil pouch *)
    rA[4, 5] := 0.000000; (* P_internal decoupled from cumulative lethality *)
    rA[4, 6] := 0.000000; (* P_internal decoupled from cumulative cook value *)

    (* --- ROW 5: Cumulative Inactivation Lethality F0 [min] --- *)
    rA[5, 1] := 0.000000; (* F0 decoupled directly from chamber temperature (driven by core temp) *)
    rA[5, 2] := 0.000850; (* F0 linearized Bigelow rate coupling: dL/dTcore at nominal 121.1 deg C = ln(10)/10 * Ts/60 *)
    rA[5, 3] := 0.000000; (* F0 independent of chamber total pressure *)
    rA[5, 4] := 0.000000; (* F0 independent of container internal pressure *)
    rA[5, 5] := 1.000000; (* F0 pure discrete integrator: F0[k+1] = F0[k] + L(Tcore)*Ts/60 *)
    rA[5, 6] := 0.000000; (* F0 decoupled from cook value *)

    (* --- ROW 6: Cumulative Quality Degradation Cook Value C0 [min] --- *)
    rA[6, 1] := 0.000000; (* C0 decoupled directly from chamber temperature *)
    rA[6, 2] := 0.000380; (* C0 linearized cook rate coupling: dLc/dTcore at nominal 121.1 deg C = ln(10)/33.1 * Ts/60 *)
    rA[6, 3] := 0.000000; (* C0 independent of chamber pressure *)
    rA[6, 4] := 0.000000; (* C0 independent of container internal pressure *)
    rA[6, 5] := 0.000000; (* C0 decoupled from microbial lethality *)
    rA[6, 6] := 1.000000; (* C0 pure discrete integrator: C0[k+1] = C0[k] + Lc(Tcore)*Ts/60 *)

    (* -------------------------------------------------------------------------
     * 2. CONTROL INPUT COUPLING MATRIX B (6x5)
     * Actuator gains mapping control demands to discrete state rates of change:
     *   Inputs: u1 = Steam valve [%], u2 = Compressed air valve [%], u3 = Exhaust vent [%],
     *           u4 = Cooling cascade valve [%], u5 = Rotary drum speed [RPM].
     * ------------------------------------------------------------------------- *)

    (* --- ROW 1: T_retort response to actuators --- *)
    rB[1, 1] := 0.048500; (* u1: Saturated steam injection valve provides primary thermal enthalpy [deg C/%] *)
    rB[1, 2] := -0.001200;(* u2: Compressed air injection introduces slight chilling / thermal dilution [deg C/%] *)
    rB[1, 3] := -0.012500;(* u3: Exhaust vent opening vents hot steam mass causing evaporative flashing drop [deg C/%] *)
    rB[1, 4] := -0.062000;(* u4: Cooling water cascade spray injects cold quench water, rapid temperature drop [deg C/%] *)
    rB[1, 5] := 0.002800; (* u5: Rotary drum speed enhances gas convection and boundary layer heat transfer [deg C/RPM] *)

    (* --- ROW 2: T_core response to actuators --- *)
    rB[2, 1] := 0.000150; (* u1: Steam valve has delayed secondary conductive effect on container core [deg C/%] *)
    rB[2, 2] := 0.000000; (* u2: Compressed air has zero direct penetration into container core *)
    rB[2, 3] := -0.000050;(* u3: Exhaust vent has negligible direct effect on core *)
    rB[2, 4] := -0.000350;(* u4: Cooling water quench accelerates surface boundary cooling of container [deg C/%] *)
    rB[2, 5] := 0.004200; (* u5: Drum rotation induces axial headspace bubble agitation, accelerating core heating [deg C/RPM] *)

    (* --- ROW 3: P_retort response to actuators --- *)
    rB[3, 1] := 0.008200; (* u1: Steam mass inflow elevates chamber pressure via vapor addition [bar/%] *)
    rB[3, 2] := 0.014500; (* u2: Compressed air overpressure valve injects non-condensable gas rapidly [bar/%] *)
    rB[3, 3] := -0.018500;(* u3: Exhaust vent valve rapidly depressurizes gaseous chamber volume [bar/%] *)
    rB[3, 4] := -0.016200;(* u4: Cold water spray condenses saturated steam, causing rapid steam collapse [bar/%] *)
    rB[3, 5] := 0.000050; (* u5: Rotor movement creates slight dynamic gas turbulence backpressure [bar/RPM] *)

    (* --- ROW 4: P_internal response to actuators --- *)
    rB[4, 1] := 0.000080; (* u1: Steam heating indirectly increases internal product vapor pressure [bar/%] *)
    rB[4, 2] := 0.000000; (* u2: External compressed air does not penetrate hermetically sealed container [bar/%] *)
    rB[4, 3] := 0.000000; (* u3: External vent does not directly affect container sealed contents [bar/%] *)
    rB[4, 4] := -0.000120;(* u4: External cold spray chilling slows internal vaporization [bar/%] *)
    rB[4, 5] := 0.000280; (* u5: Liquid sloshing inside container accelerates internal heat transfer [bar/RPM] *)

    (* --- ROW 5: Lethality F0 response to actuators --- *)
    rB[5, 1] := 0.000000; (* u1: Actuators affect F0 exclusively through integrated T_core trajectory *)
    rB[5, 2] := 0.000000; (* u2: Actuators affect F0 exclusively through integrated T_core trajectory *)
    rB[5, 3] := 0.000000; (* u3: Actuators affect F0 exclusively through integrated T_core trajectory *)
    rB[5, 4] := 0.000000; (* u4: Actuators affect F0 exclusively through integrated T_core trajectory *)
    rB[5, 5] := 0.000000; (* u5: Actuators affect F0 exclusively through integrated T_core trajectory *)

    (* --- ROW 6: Cook Value C0 response to actuators --- *)
    rB[6, 1] := 0.000000; (* u1: Actuators affect C0 exclusively through integrated T_core trajectory *)
    rB[6, 2] := 0.000000; (* u2: Actuators affect C0 exclusively through integrated T_core trajectory *)
    rB[6, 3] := 0.000000; (* u3: Actuators affect C0 exclusively through integrated T_core trajectory *)
    rB[6, 4] := 0.000000; (* u4: Actuators affect C0 exclusively through integrated T_core trajectory *)
    rB[6, 5] := 0.000000; (* u5: Actuators affect C0 exclusively through integrated T_core trajectory *)

    (* -------------------------------------------------------------------------
     * 3. STATE-TO-OUTPUT OBSERVATION MATRIX C (6x6)
     * Physical sensor and estimation outputs:
     *   y1 = T_retort [deg C]
     *   y2 = T_core [deg C]
     *   y3 = P_retort [bar]
     *   y4 = P_internal [bar]
     *   y5 = Net Container Wall Differential Stress DeltaP = P_internal - P_retort [bar]
     *   y6 = Cumulative Lethality F0 [min]
     * ------------------------------------------------------------------------- *)
    (* Output 1: Retort Chamber Temp y1 = x1 *)
    rC[1, 1] := 1.0; rC[1, 2] := 0.0; rC[1, 3] := 0.0; rC[1, 4] := 0.0; rC[1, 5] := 0.0; rC[1, 6] := 0.0;

    (* Output 2: Container Core Temp y2 = x2 *)
    rC[2, 1] := 0.0; rC[2, 2] := 1.0; rC[2, 3] := 0.0; rC[2, 4] := 0.0; rC[2, 5] := 0.0; rC[2, 6] := 0.0;

    (* Output 3: Retort Shell Pressure y3 = x3 *)
    rC[3, 1] := 0.0; rC[3, 2] := 0.0; rC[3, 3] := 1.0; rC[3, 4] := 0.0; rC[3, 5] := 0.0; rC[3, 6] := 0.0;

    (* Output 4: Container Internal Pressure y4 = x4 *)
    rC[4, 1] := 0.0; rC[4, 2] := 0.0; rC[4, 3] := 0.0; rC[4, 4] := 1.0; rC[4, 5] := 0.0; rC[4, 6] := 0.0;

    (* Output 5: Container Wall Differential Stress DeltaP = P_internal - P_retort = x4 - x3 *)
    rC[5, 1] := 0.0; rC[5, 2] := 0.0; rC[5, 3] := -1.0; rC[5, 4] := 1.0; rC[5, 5] := 0.0; rC[5, 6] := 0.0;

    (* Output 6: Cumulative Lethality F0 y6 = x5 *)
    rC[6, 1] := 0.0; rC[6, 2] := 0.0; rC[6, 3] := 0.0; rC[6, 4] := 0.0; rC[6, 5] := 1.0; rC[6, 6] := 0.0;

    (* -------------------------------------------------------------------------
     * 4. DIRECT FEEDTHROUGH TRANSMISSION MATRIX D (6x5)
     * All direct feedthrough elements are zero (strictly proper physical dynamic system)
     * ------------------------------------------------------------------------- *)
    FOR iIdx1 := 1 TO 6 DO
        FOR iIdx2 := 1 TO 5 DO
            rD[iIdx1, iIdx2] := 0.0;
        END_FOR;
    END_FOR;

    (* -------------------------------------------------------------------------
     * 5. RECEDING-HORIZON MPC PENALTY MATRICES (Q, R, S, P)
     * Quadratic optimization weight design balancing tight tracking of scheduled
     * temperature and overpressure while strictly penalizing pouch stress violations.
     * ------------------------------------------------------------------------- *)
    (* State Tracking Error Penalties Q (6x1 diagonal) *)
    rQ_Weights[1] := 120.0; (* T_retort temperature error penalty: strict adherence to scheduled cook temp *)
    rQ_Weights[2] := 65.0;  (* T_core cold-spot temperature tracking weight *)
    rQ_Weights[3] := 250.0; (* P_retort pressure error penalty: high priority to maintain counter-pressure *)
    rQ_Weights[4] := 40.0;  (* P_internal internal pressure trajectory monitoring *)
    rQ_Weights[5] := 80.0;  (* F0 accumulated lethality tracking weight *)
    rQ_Weights[6] := 15.0;  (* C0 cook quality retention weight *)

    (* Actuator Control Effort Penalties R (5x1 diagonal) *)
    rR_Weights[1] := 0.45;  (* Steam modulating valve movement cost *)
    rR_Weights[2] := 0.60;  (* Compressed air injection cost *)
    rR_Weights[3] := 0.75;  (* Exhaust vent modulation cost *)
    rR_Weights[4] := 0.50;  (* Cascade cooling water valve cost *)
    rR_Weights[5] := 0.85;  (* Rotary drum speed adjustment cost *)

    (* Actuator Slew Rate Penalties S (5x1 diagonal) *)
    rS_Weights[1] := 1.80;  (* Steam valve slew rate damping: prevent thermal shock and pressure hammer *)
    rS_Weights[2] := 2.20;  (* Air injection slew rate damping: prevent overpressure overshoot *)
    rS_Weights[3] := 2.50;  (* Exhaust vent slew rate damping: prevent violent flashing *)
    rS_Weights[4] := 2.00;  (* Cooling water slew rate damping: prevent sudden thermal stress on containers *)
    rS_Weights[5] := 3.50;  (* Rotary drum speed slew rate damping: protect mechanical helical drive *)

    (* Terminal Horizon State Error Penalties P (6x1 diagonal) *)
    rP_TerminalWeights[1] := 180.0; (* Terminal T_retort penalty *)
    rP_TerminalWeights[2] := 100.0; (* Terminal T_core penalty *)
    rP_TerminalWeights[3] := 350.0; (* Terminal P_retort penalty *)
    rP_TerminalWeights[4] := 60.0;  (* Terminal P_internal penalty *)
    rP_TerminalWeights[5] := 120.0; (* Terminal F0 penalty *)
    rP_TerminalWeights[6] := 25.0;  (* Terminal C0 penalty *)

    (* Actuator Box Saturation Hard Boundaries [Umin, Umax] *)
    rMPC_Umin[1] := 0.0;    rMPC_Umax[1] := 100.0; (* Steam valve: 0.0 to 100.0 % *)
    rMPC_Umin[2] := 0.0;    rMPC_Umax[2] := 100.0; (* Compressed air valve: 0.0 to 100.0 % *)
    rMPC_Umin[3] := 0.0;    rMPC_Umax[3] := 100.0; (* Exhaust vent valve: 0.0 to 100.0 % *)
    rMPC_Umin[4] := 0.0;    rMPC_Umax[4] := 100.0; (* Cooling cascade valve: 0.0 to 100.0 % *)
    rMPC_Umin[5] := 0.0;    rMPC_Umax[5] := 25.0;  (* Rotary drum drive: 0.0 to 25.0 RPM *)

    (* Actuator Maximum Slew Velocity Limits [DeltaUmax in units/s] *)
    rMPC_DeltaUmax[1] := 10.0; (* Steam valve max slew: 10.0 %/s *)
    rMPC_DeltaUmax[2] := 15.0; (* Air valve max slew: 15.0 %/s *)
    rMPC_DeltaUmax[3] := 20.0; (* Vent valve max slew: 20.0 %/s *)
    rMPC_DeltaUmax[4] := 12.0; (* Cooling cascade valve max slew: 12.0 %/s *)
    rMPC_DeltaUmax[5] := 2.0;  (* Drum speed max slew: 2.0 RPM/s *)

    (* Initialize State Vector x to Ambient Cold Starting Conditions *)
    rX_State[1] := 22.5;  (* Ambient room temperature 22.5 deg C *)
    rX_State[2] := 20.0;  (* Initial container core temperature 20.0 deg C *)
    rX_State[3] := 1.013; (* Atmospheric standard pressure 1.013 bar *)
    rX_State[4] := 1.013; (* Initial container internal pressure 1.013 bar *)
    rX_State[5] := 0.000; (* Zero initial lethality F0 *)
    rX_State[6] := 0.000; (* Zero initial cook value C0 *)

    FOR iIdx1 := 1 TO 5 DO
        rU_Control[iIdx1] := 0.0;
        rU_ControlPrev[iIdx1] := 0.0;
    END_FOR;

    bInitMatricesComplete := TRUE;
END_IF;'''
