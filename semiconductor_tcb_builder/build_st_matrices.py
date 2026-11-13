# semiconductor_tcb_builder/build_st_matrices.py

def get_matrices_initialization():
    return """(*
====================================================================================================
CYBER-PHYSICAL MODEL INITIALIZATION & DISCRETE STATE-SPACE MATRICES
Discrete System Formulation at Sampling Interval Ts = 1.0 ms (dt = 0.001 s):
  x[k+1] = A * x[k] + B * u[k]
  y[k]   = C * x[k] + D * u[k]

State Vector Definitions:
  x[1] : Dynamic Bond Force Error (e_F = F_meas - F_target) [N]
  x[2] : Bond Head Collet Z-Axis Thermal Elongation (Delta_L_z) [um]
  x[3] : Solder Micro-Bump Viscoplastic Collapse Depth (h_collapse) [um]
  x[4] : Ceramic Heater Interface Temperature (T_interface) [deg C]
  x[5] : Substrate Vacuum Chuck Holding Differential Pressure (P_vac) [kPa]
  x[6] : 6-Axis Chuck Co-Planarity Tilt Pitch Error (Theta_Rx) [urad]

Actuator Input Definitions:
  u[1] : Z-Axis Piezo Micro-Actuator Fine Displacement Trim [um] (-10.0 to +10.0)
  u[2] : Voice Coil Linear Motor Drive Current [A] (-15.0 to +15.0)
  u[3] : Ceramic Pulse Heater PWM Firing Duty Cycle [%] (0.0 to 100.0)
  u[4] : Chilled Nitrogen Quench Proportional Cooling Valve [%] (0.0 to 100.0)
  u[5] : Formic Acid Vapor Purge Mass Flow Controller [%] (0.0 to 100.0)
====================================================================================================
*)

IF bFirstScan THEN
    (* ------------------------------------------------------------------------------------------ *)
    (* Initialize Discrete State Transition Matrix A (6x6)                                        *)
    (* Derived via zero-order hold (ZOH) discretization of coupled mechanical, thermal & fluid PDE*)
    (* ------------------------------------------------------------------------------------------ *)
    (* Row 1: Dynamic Force Error dynamics (Voice-coil mass-spring-damper coupled with bump contact) *)
    matA[1, 1] := 0.94120;   (* Force error persistence / mechanical damping decay *)
    matA[1, 2] := 1.84200;   (* Force coupling to bond head thermal expansion elongation *)
    matA[1, 3] := -0.62500;  (* Force relaxation due to molten solder viscoplastic collapse *)
    matA[1, 4] := 0.03850;   (* Force drift from ceramic tool thermal expansion *)
    matA[1, 5] := 0.00000;   (* Vacuum decoupling from bond force *)
    matA[1, 6] := -0.11400;  (* Force distribution asymmetry induced by chuck tilt *)

    (* Row 2: Bond Head Z-Axis Thermal Elongation (Delta_L = alpha * L * Delta_T) *)
    matA[2, 1] := 0.00000;   (* Mechanical stress decoupling from thermal expansion *)
    matA[2, 2] := 0.98560;   (* Collet thermal expansion transient time constant *)
    matA[2, 3] := 0.00000;   (* Solder collapse independence *)
    matA[2, 4] := 0.01240;   (* Heat conduction from pulse heater to ceramic collet body *)
    matA[2, 5] := 0.00000;   (* Vacuum decoupling *)
    matA[2, 6] := 0.00000;   (* Tilt decoupling *)

    (* Row 3: Micro-Bump Solder Viscoplastic Squeeze-Out Collapse Height (Stephan Lubrication Law) *)
    matA[3, 1] := 0.00485;   (* Incremental collapse rate driven by compressive bond force *)
    matA[3, 2] := -0.00120;  (* Apparent collapse offset caused by collet thermal expansion *)
    matA[3, 3] := 0.99120;   (* Solder collapse memory / strain hardening retention *)
    matA[3, 4] := 0.00840;   (* Viscosity reduction & eutectic melt acceleration above liquidus *)
    matA[3, 5] := 0.00000;   (* Vacuum decoupling *)
    matA[3, 6] := 0.00210;   (* Non-uniform squeeze-out due to angular tilt wedge effect *)

    (* Row 4: Pulse Ceramic Heater Interface Temperature (Conduction, Convection & Radiation) *)
    matA[4, 1] := 0.00000;   (* Mechanical force decoupling from heat generation *)
    matA[4, 2] := 0.00000;   (* Elongation decoupling *)
    matA[4, 3] := 0.00150;   (* Thermal contact resistance drop with solder joint collapse *)
    matA[4, 4] := 0.97200;   (* Substrate thermal dissipation & heat capacity time constant *)
    matA[4, 5] := 0.00050;   (* Thermal conductance modulation by chuck vacuum contact quality *)
    matA[4, 6] := 0.00000;   (* Tilt decoupling *)

    (* Row 5: Substrate Vacuum Chuck Holding Differential Pressure (Pneumatic Manifold Conductance) *)
    matA[5, 1] := 0.00000;   (* Force decoupling *)
    matA[5, 2] := 0.00000;   (* Elongation decoupling *)
    matA[5, 3] := 0.00000;   (* Solder collapse decoupling *)
    matA[5, 4] := -0.00320;  (* Thermal expansion seal leakage effect *)
    matA[5, 5] := 0.96500;   (* Vacuum manifold conductance & sealed cavity pump-down response *)
    matA[5, 6] := -0.00850;  (* Seal perimeter micro-gap leakage under co-planarity tilt *)

    (* Row 6: 6-Axis Chuck Co-Planarity Tilt Pitch Error (Hexapod Flexure Dynamics) *)
    matA[6, 1] := 0.00240;   (* Moment arm tilt induced by asymmetric die micro-bump forces *)
    matA[6, 2] := 0.00000;   (* Axial thermal expansion decoupling from pure angular tilt *)
    matA[6, 3] := -0.00180;  (* Tilt self-correction as solder collapses to uniform mechanical stop *)
    matA[6, 4] := 0.00110;   (* Asymmetric thermal expansion across large die footprint (30x30 mm) *)
    matA[6, 5] := 0.00000;   (* Vacuum decoupling *)
    matA[6, 6] := 0.93200;   (* Chuck mechanical flexure damping and piezo compliance *)

    (* ------------------------------------------------------------------------------------------ *)
    (* Initialize Discrete Control Input Matrix B (6x5)                                           *)
    (* Direct actuator transfer gains into each cyber-physical state                              *)
    (* ------------------------------------------------------------------------------------------ *)
    (* Row 1: Dynamic Force Error response to actuators *)
    matB[1, 1] := 4.25000;   (* Piezo trim displacement to force stiffness gain [N/um] *)
    matB[1, 2] := 28.6500;   (* Voice coil motor Lorentz force constant Kt [N/A] *)
    matB[1, 3] := 0.04200;   (* Rapid thermal expansion transient force push [N/%] *)
    matB[1, 4] := -0.01800;  (* Nitrogen quench thermal contraction force relief [N/%] *)
    matB[1, 5] := 0.00000;   (* Formic acid purge decoupling *)

    (* Row 2: Collet Thermal Elongation response *)
    matB[2, 1] := 0.00000;   (* Piezo trim decoupling *)
    matB[2, 2] := 0.00000;   (* Voice coil decoupling *)
    matB[2, 3] := 0.01450;   (* Ceramic pulse heater duty to collet elongation [um/%] *)
    matB[2, 4] := -0.00880;  (* Chilled N2 quench cooling contraction [um/%] *)
    matB[2, 5] := 0.00000;   (* Formic acid purge decoupling *)

    (* Row 3: Solder Micro-Bump Collapse response *)
    matB[3, 1] := 0.01620;   (* Piezo micro-squeeze actuator displacement [um/um] *)
    matB[3, 2] := 0.02450;   (* Voice coil compressive force accelerated squeeze [um/A] *)
    matB[3, 3] := 0.03800;   (* Heater melting liquefaction rate acceleration [um/%] *)
    matB[3, 4] := -0.04500;  (* Chilled quench immediate solder freezing arrest [um/%] *)
    matB[3, 5] := 0.00120;   (* Native oxide reduction facilitating solder wetting [um/%] *)

    (* Row 4: Pulse Heater Interface Temperature response *)
    matB[4, 1] := 0.00000;   (* Piezo trim decoupling *)
    matB[4, 2] := 0.00000;   (* Voice coil decoupling *)
    matB[4, 3] := 2.85000;   (* Pulse ceramic heater rapid ramp heating rate [deg C/%] *)
    matB[4, 4] := -1.45000;  (* High-velocity chilled N2 blast quench cooling [deg C/%] *)
    matB[4, 5] := -0.01200;  (* Carrier gas minor evaporative / convective heat loss [deg C/%] *)

    (* Row 5: Vacuum Chuck Holding Pressure response *)
    matB[5, 1] := 0.00000;   (* Piezo trim decoupling *)
    matB[5, 2] := 0.00000;   (* Voice coil decoupling *)
    matB[5, 3] := 0.00000;   (* Heater decoupling *)
    matB[5, 4] := 0.00000;   (* Quench decoupling *)
    matB[5, 5] := 0.00000;   (* Pure pneumatic valve control *)

    (* Row 6: 6-Axis Chuck Tilt Error response *)
    matB[6, 1] := 0.08500;   (* Piezo differential leveling actuator pitch trim [urad/um] *)
    matB[6, 2] := 0.01200;   (* Voice coil minor parasitic angular moment [urad/A] *)
    matB[6, 3] := 0.00400;   (* Asymmetric pulse heating thermal expansion tilt [urad/%] *)
    matB[6, 4] := -0.00200;  (* Quench cooling thermal gradient tilt [urad/%] *)
    matB[6, 5] := 0.00000;   (* Formic acid purge decoupling *)

    (* ------------------------------------------------------------------------------------------ *)
    (* Initialize Discrete Measurement Matrix C (6x6)                                             *)
    (* Direct mapping from state space to voted 2oo3 physical sensor observations                 *)
    (* ------------------------------------------------------------------------------------------ *)
    matC[1, 1] := 1.00000; matC[1, 2] := 0.00000; matC[1, 3] := 0.00000; matC[1, 4] := 0.00000; matC[1, 5] := 0.00000; matC[1, 6] := 0.00000;
    matC[2, 1] := 0.00000; matC[2, 2] := 1.00000; matC[2, 3] := 0.00000; matC[2, 4] := 0.00000; matC[2, 5] := 0.00000; matC[2, 6] := 0.00000;
    matC[3, 1] := 0.00000; matC[3, 2] := 0.00000; matC[3, 3] := 1.00000; matC[3, 4] := 0.00000; matC[3, 5] := 0.00000; matC[3, 6] := 0.00000;
    matC[4, 1] := 0.00000; matC[4, 2] := 0.00000; matC[4, 3] := 0.00000; matC[4, 4] := 1.00000; matC[4, 5] := 0.00000; matC[4, 6] := 0.00000;
    matC[5, 1] := 0.00000; matC[5, 2] := 0.00000; matC[5, 3] := 0.00000; matC[5, 4] := 0.00000; matC[5, 5] := 1.00000; matC[5, 6] := 0.00000;
    matC[6, 1] := 0.00000; matC[6, 2] := 0.00000; matC[6, 3] := 0.00000; matC[6, 4] := 0.00000; matC[6, 5] := 0.00000; matC[6, 6] := 1.00000;

    (* ------------------------------------------------------------------------------------------ *)
    (* Initialize Direct Feedthrough Matrix D (6x5) - Strictly proper dynamic model (all zeros)   *)
    (* ------------------------------------------------------------------------------------------ *)
    matD[1, 1] := 0.0; matD[1, 2] := 0.0; matD[1, 3] := 0.0; matD[1, 4] := 0.0; matD[1, 5] := 0.0;
    matD[2, 1] := 0.0; matD[2, 2] := 0.0; matD[2, 3] := 0.0; matD[2, 4] := 0.0; matD[2, 5] := 0.0;
    matD[3, 1] := 0.0; matD[3, 2] := 0.0; matD[3, 3] := 0.0; matD[3, 4] := 0.0; matD[3, 5] := 0.0;
    matD[4, 1] := 0.0; matD[4, 2] := 0.0; matD[4, 3] := 0.0; matD[4, 4] := 0.0; matD[4, 5] := 0.0;
    matD[5, 1] := 0.0; matD[5, 2] := 0.0; matD[5, 3] := 0.0; matD[5, 4] := 0.0; matD[5, 5] := 0.0;
    matD[6, 1] := 0.0; matD[6, 2] := 0.0; matD[6, 3] := 0.0; matD[6, 4] := 0.0; matD[6, 5] := 0.0;

    (* ------------------------------------------------------------------------------------------ *)
    (* Initialize Steady-State Kalman Filter Observer Gain Matrix L (6x6)                         *)
    (* Synthesized from discrete Algebraic Riccati Equation (DARE) with process noise Q_w & R_v   *)
    (* ------------------------------------------------------------------------------------------ *)
    matKalmanL[1, 1] := 0.2850; matKalmanL[1, 2] := 0.0120; matKalmanL[1, 3] := -0.0080; matKalmanL[1, 4] := 0.0015; matKalmanL[1, 5] := 0.0000; matKalmanL[1, 6] := -0.0040;
    matKalmanL[2, 1] := 0.0040; matKalmanL[2, 2] := 0.2100; matKalmanL[2, 3] := 0.0000;  matKalmanL[2, 4] := 0.0065; matKalmanL[2, 5] := 0.0000; matKalmanL[2, 6] := 0.0000;
    matKalmanL[3, 1] := 0.0065; matKalmanL[3, 2] := -0.0030;matKalmanL[3, 3] := 0.3200;  matKalmanL[3, 4] := 0.0045; matKalmanL[3, 5] := 0.0000; matKalmanL[3, 6] := 0.0015;
    matKalmanL[4, 1] := 0.0010; matKalmanL[4, 2] := 0.0025; matKalmanL[4, 3] := 0.0035;  matKalmanL[4, 4] := 0.3650; matKalmanL[4, 5] := 0.0010; matKalmanL[4, 6] := 0.0000;
    matKalmanL[5, 1] := 0.0000; matKalmanL[5, 2] := 0.0000; matKalmanL[5, 3] := 0.0000;  matKalmanL[5, 4] := 0.0000; matKalmanL[5, 5] := 0.2450; matKalmanL[5, 6] := -0.0020;
    matKalmanL[6, 1] := -0.0025;matKalmanL[6, 2] := 0.0000; matKalmanL[6, 3] := 0.0010;  matKalmanL[6, 4] := 0.0000; matKalmanL[6, 5] := 0.0000; matKalmanL[6, 6] := 0.2900;

    (* ------------------------------------------------------------------------------------------ *)
    (* Initialize Model Predictive Control (MPC) Cost Weight Matrices (Q, R, S, P)                *)
    (* ------------------------------------------------------------------------------------------ *)
    (* State Tracking Error Penalties Q: [Force, Elongation, Collapse, Temperature, Vacuum, Tilt] *)
    matQ_Diag[1] := 18.50;   (* High priority penalty on bond force tracking accuracy *)
    matQ_Diag[2] := 2.40;    (* Collet thermal expansion drift suppression *)
    matQ_Diag[3] := 24.00;   (* Critical micro-bump solder collapse target adherence *)
    matQ_Diag[4] := 8.50;    (* Ceramic heater temperature profile tracking *)
    matQ_Diag[5] := 1.20;    (* Substrate vacuum maintenance penalty *)
    matQ_Diag[6] := 15.00;   (* High penalty on chuck co-planarity tilt error *)

    (* Control Effort Penalties R: [PiezoTrim, VoiceCoilCurrent, HeaterDuty, QuenchValve, FormicFlow] *)
    matR_Diag[1] := 0.45;    (* Piezo displacement control effort penalty *)
    matR_Diag[2] := 0.65;    (* Voice coil motor current electrical power dissipation penalty *)
    matR_Diag[3] := 0.15;    (* Pulse heater electrical firing effort *)
    matR_Diag[4] := 0.25;    (* Nitrogen quench gas consumption penalty *)
    matR_Diag[5] := 0.10;    (* Formic acid carrier flow penalty *)

    (* Actuator Slew Rate Penalties S (Delta_U rate-of-change suppression for mechanical smoothness) *)
    matS_Diag[1] := 1.80;    (* Piezo stroke rate limit suppression *)
    matS_Diag[2] := 2.50;    (* Voice coil inductive di/dt surge dampening *)
    matS_Diag[3] := 0.85;    (* Pulse heater thermal shock ramp rate smoothing *)
    matS_Diag[4] := 1.20;    (* Quench valve pneumatic surge prevention *)
    matS_Diag[5] := 0.50;    (* Formic mass flow controller stability *)

    (* Terminal State Penalties P (Riccati algebraic terminal cost approximation) *)
    matP_Diag[1] := 32.00;
    matP_Diag[2] := 4.80;
    matP_Diag[3] := 48.00;
    matP_Diag[4] := 16.00;
    matP_Diag[5] := 2.50;
    matP_Diag[6] := 30.00;

    (* Actuator Hard Saturation Bounds (Lower & Upper) *)
    rU_LowerBound[1] := -10.0;  rU_UpperBound[1] := 10.0;   (* Piezo micro-trim [-10.0 um to +10.0 um] *)
    rU_LowerBound[2] := -15.0;  rU_UpperBound[2] := 15.0;   (* Voice coil current [-15.0 A to +15.0 A] *)
    rU_LowerBound[3] := 0.0;    rU_UpperBound[3] := 100.0;  (* Ceramic heater duty [0.0 % to 100.0 %] *)
    rU_LowerBound[4] := 0.0;    rU_UpperBound[4] := 100.0;  (* Chilled N2 valve [0.0 % to 100.0 %] *)
    rU_LowerBound[5] := 0.0;    rU_UpperBound[5] := 100.0;  (* Formic acid MFC [0.0 % to 100.0 %] *)

    (* Actuator Maximum Rate of Change per Scan Cycle (Slew Rate Limits) *)
    rDeltaU_MaxRate[1] := 1.20;  (* Max piezo displacement delta: 1.2 um/scan *)
    rDeltaU_MaxRate[2] := 2.50;  (* Max voice coil current delta: 2.5 A/scan *)
    rDeltaU_MaxRate[3] := 18.0;  (* Max pulse heater duty delta: 18 %/scan *)
    rDeltaU_MaxRate[4] := 22.0;  (* Max quench cooling valve delta: 22 %/scan *)
    rDeltaU_MaxRate[5] := 8.0;   (* Max formic acid MFC delta: 8 %/scan *)

    (* ------------------------------------------------------------------------------------------ *)
    (* Initialize 6-Axis Chuck Hexapod Decoupling Kinematics Matrix (6x6)                         *)
    (* Maps [Tx, Ty, Tz, Rx, Ry, Rz] target corrections into 3 vertical struts & 3 shear flexures *)
    (* ------------------------------------------------------------------------------------------ *)
    matChuckKinematics[1, 1] := 0.0000; matChuckKinematics[1, 2] := 0.0000; matChuckKinematics[1, 3] := 1.0000; matChuckKinematics[1, 4] := 0.0000;  matChuckKinematics[1, 5] := 0.0750; matChuckKinematics[1, 6] := 0.0000;
    matChuckKinematics[2, 1] := 0.0000; matChuckKinematics[2, 2] := 0.0000; matChuckKinematics[2, 3] := 1.0000; matChuckKinematics[2, 4] := -0.0650; matChuckKinematics[2, 5] := -0.0375;matChuckKinematics[2, 6] := 0.0000;
    matChuckKinematics[3, 1] := 0.0000; matChuckKinematics[3, 2] := 0.0000; matChuckKinematics[3, 3] := 1.0000; matChuckKinematics[3, 4] := 0.0650;  matChuckKinematics[3, 5] := -0.0375;matChuckKinematics[3, 6] := 0.0000;
    matChuckKinematics[4, 1] := 1.0000; matChuckKinematics[4, 2] := 0.0000; matChuckKinematics[4, 3] := 0.0000; matChuckKinematics[4, 4] := 0.0000;  matChuckKinematics[4, 5] := 0.0000; matChuckKinematics[4, 6] := -0.0820;
    matChuckKinematics[5, 1] := -0.5000;matChuckKinematics[5, 2] := 0.8660; matChuckKinematics[5, 3] := 0.0000; matChuckKinematics[5, 4] := 0.0000;  matChuckKinematics[5, 5] := 0.0000; matChuckKinematics[5, 6] := -0.0820;
    matChuckKinematics[6, 1] := -0.5000;matChuckKinematics[6, 2] := -0.8660;matChuckKinematics[6, 3] := 0.0000; matChuckKinematics[6, 4] := 0.0000;  matChuckKinematics[6, 5] := 0.0000; matChuckKinematics[6, 6] := -0.0820;

    (* Initial Zero Clears for State and Control Vectors *)
    FOR iStateIdx := 1 TO 6 DO
        vecX_State[iStateIdx] := 0.0;
        vecX_Hat[iStateIdx] := 0.0;
        vecX_Next[iStateIdx] := 0.0;
        vecY_Meas[iStateIdx] := 0.0;
        vecY_Hat[iStateIdx] := 0.0;
        vecInnovation[iStateIdx] := 0.0;
        vecX_Ref[iStateIdx] := 0.0;
    END_FOR;

    FOR iInputIdx := 1 TO 5 DO
        vecU_Active[iInputIdx] := 0.0;
        vecU_Prev[iInputIdx] := 0.0;
        vecDeltaU[iInputIdx] := 0.0;
    END_FOR;

    (* Clear MPC Horizon Buffers *)
    FOR iHorizStep := 0 TO 9 DO
        FOR iInputIdx := 1 TO 5 DO
            arrU_Horiz[iHorizStep, iInputIdx] := 0.0;
            arrGradU[iHorizStep, iInputIdx] := 0.0;
        END_FOR;
    END_FOR;

    FOR iHorizStep := 0 TO 10 DO
        FOR iStateIdx := 1 TO 6 DO
            arrX_Horiz[iHorizStep, iStateIdx] := 0.0;
            arrLambda[iHorizStep, iStateIdx] := 0.0;
        END_FOR;
    END_FOR;

    bFirstScan := FALSE;
END_IF;
"""
