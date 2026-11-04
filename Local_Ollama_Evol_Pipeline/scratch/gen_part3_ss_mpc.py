# gen_part3_ss_mpc.py
def get_part3_ss_mpc():
    return """
(* ==================================================================================================================== *)
(* PHASE 2: DISCRETE STATE-SPACE PREDICTION & RECURSIVE ESTIMATION (x[k+1] = A*x[k] + B*u[k], y[k] = C*x[k] + D*u[k])  *)
(* 8x8 Continuous-to-Discrete State Matrix Formulation @ 250 microsecond execution cycle.                              *)
(* States:                                                                                                              *)
(*   x1: Seam Body Hook Fold Length [mm]                                                                                *)
(*   x2: Seam Cover Hook Curl Length [mm]                                                                               *)
(*   x3: Finished Seam Thickness Gauge [mm]                                                                             *)
(*   x4: Turret Spindle Electronic Cam Angular Error [rad]                                                              *)
(*   x5: Spindle Electronic Cam Angular Velocity Error [rad/s]                                                          *)
(*   x6: In-Can Headspace Gaseous Nitrogen Expansion Pressure [bar]                                                     *)
(*   x7: Can End Dome Fundamental Resonant Natural Frequency [Hz]                                                       *)
(*   x8: Acoustic Tap Impulse Vibration Envelope Amplitude [V]                                                         *)
(* Controls:                                                                                                            *)
(*   u1: 1st Operation Roll Servo Radial Position Offset [mm]                                                           *)
(*   u2: 2nd Operation Roll Servo Radial Crimp Offset [mm]                                                              *)
(*   u3: Direct-Drive Spindle Servo Torque Feedforward Correction [Nm]                                                  *)
(*   u4: High-Speed Cryogenic LN2 Solenoid Valve Dosing Pulse Duration [ms]                                             *)
(*   u5: Lifter Elevator Table Dynamic Pneumatic Cushion Pressure [bar]                                                 *)
(* ==================================================================================================================== *)

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 2.1: ONE-TIME INITIALIZATION OF DISCRETE MATRICES A, B, C, D, Q, R, S, P                                             *)
(* -------------------------------------------------------------------------------------------------------------------- *)
IF NOT bMatricesInitialized THEN
    (* Zero out all matrix entries *)
    FOR iRow := 1 TO 8 DO
        FOR iCol := 1 TO 8 DO
            matA[iRow, iCol] := 0.0;
            matC[iRow, iCol] := 0.0;
            matQ[iRow, iCol] := 0.0;
            matP[iRow, iCol] := 0.0;
        END_FOR;
        FOR iCol := 1 TO 5 DO
            matB[iRow, iCol] := 0.0;
            matD[iRow, iCol] := 0.0;
        END_FOR;
    END_FOR;

    FOR iRow := 1 TO 5 DO
        FOR iCol := 1 TO 5 DO
            matR[iRow, iCol] := 0.0;
            matS[iRow, iCol] := 0.0;
            matHessianApprox[iRow, iCol] := 0.0;
        END_FOR;
    END_FOR;

    (* System Transition Matrix A (8x8) Discrete @ Ts = 250 us *)
    matA[1, 1] := 0.9945;  (* Body Hook natural decay / compliance *)
    matA[1, 3] := -0.0120; (* Seam thickness coupling to body hook compression *)
    matA[2, 2] := 0.9950;  (* Cover Hook natural compliance *)
    matA[2, 3] := -0.0145; (* Seam thickness coupling to cover hook curl *)
    matA[3, 3] := 0.9880;  (* Seam thickness elastic recovery relaxation *)
    matA[3, 1] := 0.0035;  (* Body hook expansion reaction *)
    matA[3, 2] := 0.0042;  (* Cover hook expansion reaction *)
    matA[4, 4] := 0.9998;  (* Cam angular position integration: 1 - Ts*k_spindle *)
    matA[4, 5] := 0.000250;(* Ts = 250 us integration of angular velocity error *)
    matA[5, 4] := -1.8500; (* Torsional stiffness restoring force k_torsion / J_spindle * Ts *)
    matA[5, 5] := 0.9850;  (* Viscous friction bearing damping: 1 - Ts*c_damping / J_spindle *)
    matA[6, 6] := 0.9982;  (* Headspace gas micro-permeation decay *)
    matA[7, 6] := 185.40;  (* Dome resonance sensitivity to headspace pressure df/dP [Hz/bar] *)
    matA[7, 7] := 0.9965;  (* Acoustic resonance natural peak stability *)
    matA[8, 8] := 0.9650;  (* Acoustic tap oscillation logarithmic decay envelope *)

    (* Input Distribution Matrix B (8x5) *)
    matB[1, 1] := 0.0450;  (* 1st op roll radial position effect on body hook curling *)
    matB[1, 5] := 0.0085;  (* Lifter table base force effect on body hook folding *)
    matB[2, 1] := 0.0520;  (* 1st op roll radial position effect on cover hook curl *)
    matB[2, 2] := -0.0180; (* 2nd op roll radial position tightening effect *)
    matB[3, 2] := -0.0650; (* 2nd op roll radial crimp feed direct thickness reduction *)
    matB[3, 5] := -0.0045; (* Lifter cushion pressure effect on seam thickness *)
    matB[4, 3] := 0.000042;(* Spindle torque correction effect on angular error *)
    matB[5, 3] := 0.1680;  (* Direct spindle torque to angular acceleration [rad/(s*Nm)] *)
    matB[6, 4] := 0.0215;  (* Cryogenic LN2 pulse duration effect on headspace pressure [bar/ms] *)
    matB[7, 4] := 3.980;   (* Direct acoustic resonance frequency boost from cryogenic LN2 *)
    matB[8, 4] := 0.0120;  (* Acoustic tap amplitude excitation *)

    (* Measurement Matrix C (8x8) *)
    matC[1, 1] := 38.50;   (* Overlap sensitivity to body hook: d(Overlap%)/d(x1) *)
    matC[1, 2] := 38.20;   (* Overlap sensitivity to cover hook: d(Overlap%)/d(x2) *)
    matC[1, 3] := -24.80;  (* Overlap sensitivity to seam thickness: d(Overlap%)/d(x3) *)
    matC[2, 3] := 1.0000;  (* Direct seam thickness measurement *)
    matC[3, 4] := 1000.0;  (* Cam angular error in milliradians *)
    matC[4, 6] := 1.0000;  (* Internal headspace pressure direct observation *)
    matC[5, 7] := 1.0000;  (* Resonant frequency peak observation *)
    matC[6, 8] := 45.20;   (* Acoustic damping decay rate extraction *)
    matC[7, 1] := 145.0;   (* 1st op roll force from body hook deformation *)
    matC[8, 3] := 420.0;   (* 2nd op roll force from seam thickness compression *)

    (* Direct Feedthrough Matrix D (8x5) *)
    matD[7, 1] := 185.0;   (* Direct feedthrough: 1st op roll servo offset to reaction force *)
    matD[8, 2] := 520.0;   (* Direct feedthrough: 2nd op roll servo crimp offset to crimp force *)

    (* MPC Quadratic State Error Penalty Diagonal Matrix Q (8x8) *)
    matQ[1, 1] := 125.0;   (* Weight on Body Hook length accuracy *)
    matQ[2, 2] := 130.0;   (* Weight on Cover Hook length accuracy *)
    matQ[3, 3] := 350.0;   (* Critical weight on Seam Thickness gauge *)
    matQ[4, 4] := 45.0;    (* Weight on Electronic Cam angle error *)
    matQ[5, 5] := 12.0;    (* Weight on Electronic Cam velocity error *)
    matQ[6, 6] := 280.0;   (* Critical weight on Headspace LN2 Pressure *)
    matQ[7, 7] := 0.045;   (* Weight on Acoustic Resonance frequency *)
    matQ[8, 8] := 1.500;   (* Weight on Acoustic Oscillation decay envelope *)

    (* MPC Quadratic Control Effort Penalty Matrix R (5x5) *)
    matR[1, 1] := 8.50;    (* 1st op roll servo offset penalty *)
    matR[2, 2] := 12.00;   (* 2nd op roll servo crimp offset penalty *)
    matR[3, 3] := 0.25;    (* Spindle torque feedforward penalty *)
    matR[4, 4] := 15.00;   (* LN2 cryogenic dosing pulse duration penalty *)
    matR[5, 5] := 1.80;    (* Lifter cushion pressure adjustment penalty *)

    (* MPC Quadratic Slew Rate Delta_U Penalty Matrix S (5x5) *)
    matS[1, 1] := 45.0;    (* Strict slew limit on 1st op roll motion *)
    matS[2, 2] := 65.0;    (* Strict slew limit on 2nd op crimp motion *)
    matS[3, 3] := 2.50;    (* Slew rate penalty on spindle torque spikes *)
    matS[4, 4] := 85.0;    (* Slew rate penalty on cryogenic dosing variations *)
    matS[5, 5] := 18.0;    (* Slew rate penalty on pneumatic lifter adjustments *)

    (* Terminal Cost Riccati Approximation Matrix P (8x8) *)
    FOR iRow := 1 TO 8 DO
        matP[iRow, iRow] := matQ[iRow, iRow] * 2.5;
    END_FOR;

    (* Approximate Diagonal Hessian: H_mm = 2 * (sum_i B_im^2 * Q_ii + R_mm + S_mm) *)
    FOR iSub := 1 TO 5 DO
        rSumAccumulator := 0.0;
        FOR iRow := 1 TO 8 DO
            rSumAccumulator := rSumAccumulator + (matB[iRow, iSub] * matB[iRow, iSub] * matQ[iRow, iRow]);
        END_FOR;
        matHessianApprox[iSub, iSub] := 2.0 * (rSumAccumulator + matR[iSub, iSub] + matS[iSub, iSub]);
    END_FOR;

    (* Initialize State Vector to nominal operating point *)
    vecX[1] := 1.420;  (* Nominal Body Hook: 1.420 mm *)
    vecX[2] := 1.410;  (* Nominal Cover Hook: 1.410 mm *)
    vecX[3] := 1.020;  (* Nominal Seam Thickness: 1.020 mm *)
    vecX[4] := 0.000;  (* Nominal Cam Angle Error: 0.000 rad *)
    vecX[5] := 0.000;  (* Nominal Cam Vel Error: 0.000 rad/s *)
    vecX[6] := 1.850;  (* Nominal Headspace Pressure: 1.850 bar *)
    vecX[7] := 3250.0; (* Nominal Resonance Frequency: 3250.0 Hz *)
    vecX[8] := 0.000;  (* Nominal Envelope Amplitude: 0.000 V *)

    (* Initialize Control Vector *)
    vecU[1] := 1.450;  (* 1st Op Roll Base Radial Position: 1.450 mm *)
    vecU[2] := 1.020;  (* 2nd Op Roll Base Radial Position: 1.020 mm *)
    vecU[3] := 0.000;  (* Spindle Torque Correction: 0.000 Nm *)
    vecU[4] := 3.850;  (* LN2 Pulse Duration: 3.850 ms *)
    vecU[5] := 4.200;  (* Lifter Cushion Pressure: 4.200 bar *)

    FOR iSub := 1 TO 5 DO
        vecU_Prev[iSub] := vecU[iSub];
    END_FOR;

    bMatricesInitialized := TRUE;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 2.2: DYNAMIC STATE VECTOR CORRECTION USING 2oo3 VOTED SENSOR MEASUREMENTS                                           *)
(* State Observer Innovation Correction: Blend physical sensor feedback into state vector x[k]                         *)
(* -------------------------------------------------------------------------------------------------------------------- *)
(* Observe Seam Thickness from 2nd op force & metrology *)
vecX[3] := vecX[3] + 0.050 * (rSet_SeamNominalThickness_mm - (vecX[3] + (rVoted_Force2ndOp_N - rSet_Target2ndOpPeakForce_N) / 8500.0));
(* Observe Cam Angle Tracking Error from Turret Resolver Deviation *)
rDiffAbs := (rVoted_TurretResolver_deg - rCamAngle_Normalized_deg) * 0.01745329; (* Convert deg to rad *)
vecX[4] := vecX[4] + 0.120 * (rDiffAbs - vecX[4]);
(* Observe In-Can Headspace Pressure from Acoustic Tap Voted Pressure *)
vecX[6] := vecX[6] + 0.085 * (rVoted_AcousticPressure_bar - vecX[6]);
(* Observe Acoustic Resonance Natural Frequency *)
vecX[7] := vecX[7] + 0.150 * (rVoted_AcousticResonanceFreq_Hz - vecX[7]);

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 2.3: DISCRETE STATE-SPACE FORWARD PROPAGATION: x[k+1] = A*x[k] + B*u[k]                                             *)
(* Fully expanded matrix-vector product for 8 states and 5 inputs                                                       *)
(* -------------------------------------------------------------------------------------------------------------------- *)
FOR iRow := 1 TO 8 DO
    rSumAccumulator := 0.0;
    (* State transition A * x *)
    FOR iCol := 1 TO 8 DO
        rSumAccumulator := rSumAccumulator + (matA[iRow, iCol] * vecX[iCol]);
    END_FOR;
    (* Control input distribution B * u *)
    FOR iCol := 1 TO 5 DO
        rSumAccumulator := rSumAccumulator + (matB[iRow, iCol] * vecU[iCol]);
    END_FOR;
    vecX_Next[iRow] := rSumAccumulator;
END_FOR;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 2.4: OUTPUT MEASUREMENT VECTOR ESTIMATION: y[k] = C*x[k] + D*u[k]                                                    *)
(* -------------------------------------------------------------------------------------------------------------------- *)
FOR iRow := 1 TO 8 DO
    rSumAccumulator := 0.0;
    FOR iCol := 1 TO 8 DO
        rSumAccumulator := rSumAccumulator + (matC[iRow, iCol] * vecX[iCol]);
    END_FOR;
    FOR iCol := 1 TO 5 DO
        rSumAccumulator := rSumAccumulator + (matD[iRow, iCol] * vecU[iCol]);
    END_FOR;
    vecY[iRow] := rSumAccumulator;
END_FOR;

(* Assign Outputs to Function Block Interface *)
rEstimatedSeamOverlap_Pct         := vecY[1];
rEstimatedSeamThickness_mm        := vecY[2];
rCamElectronicTrackingError_mrad  := vecY[3];
rEstimatedInternalCanPressure_bar := vecY[4];
rFilteredResonantFrequency_Hz     := vecY[5];
rAcousticDampingDecayRate         := vecY[6];
rCalculatedBodyHookLength_mm      := vecX[1];
rCalculatedCoverHookLength_mm     := vecX[2];

(* ==================================================================================================================== *)
(* PHASE 3: RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) OPTIMIZATION                                                *)
(* Quadratic Cost: J = (x[k+1]-r)^T Q (x[k+1]-r) + u^T R u + Delta_u^T S Delta_u + x_N^T P x_N                          *)
(* Iterative Projected Gradient Descent with Box Constraints and Actuator Slew Rate Limiters                            *)
(* ==================================================================================================================== *)

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 3.1: DYNAMIC REFERENCE VECTOR TARGET ASSIGNMENT                                                                     *)
(* -------------------------------------------------------------------------------------------------------------------- *)
vecR[1] := 1.420;                         (* Target Body Hook: 1.420 mm *)
vecR[2] := 1.410;                         (* Target Cover Hook: 1.410 mm *)
vecR[3] := rSet_SeamNominalThickness_mm;  (* Target Seam Thickness: Recipe 1.020 mm *)
vecR[4] := 0.000;                         (* Target Cam Tracking Error: 0.0 rad *)
vecR[5] := 0.000;                         (* Target Cam Velocity Error: 0.0 rad/s *)
vecR[6] := rSet_TargetInternalPressure_bar;(* Target Can Pressure: 1.85 bar *)
vecR[7] := rSet_AcousticResonanceTarget_Hz;(* Target Acoustic Resonance: 3250.0 Hz *)
vecR[8] := 0.000;                         (* Target Oscillation Envelope: 0.0 V *)

(* Compute State Tracking Error Vector e = x[k+1] - r *)
FOR iRow := 1 TO 8 DO
    vecStateError[iRow] := vecX_Next[iRow] - vecR[iRow];
END_FOR;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 3.2: EVALUATE INSTANTANEOUS QUADRATIC COST COMPONENTS                                                                *)
(* -------------------------------------------------------------------------------------------------------------------- *)
rMPC_StatePenaltyCost := 0.0;
FOR iRow := 1 TO 8 DO
    rMPC_StatePenaltyCost := rMPC_StatePenaltyCost + (vecStateError[iRow] * matQ[iRow, iRow] * vecStateError[iRow]);
END_FOR;

rMPC_ActuatorEffortCost := 0.0;
FOR iSub := 1 TO 5 DO
    rMPC_ActuatorEffortCost := rMPC_ActuatorEffortCost + (vecU[iSub] * matR[iSub, iSub] * vecU[iSub]);
END_FOR;

rMPC_ActuatorSlewCost := 0.0;
FOR iSub := 1 TO 5 DO
    vecDeltaU[iSub] := vecU[iSub] - vecU_Prev[iSub];
    rMPC_ActuatorSlewCost := rMPC_ActuatorSlewCost + (vecDeltaU[iSub] * matS[iSub, iSub] * vecDeltaU[iSub]);
END_FOR;

rMPC_TotalCalculatedCost := rMPC_StatePenaltyCost + rMPC_ActuatorEffortCost + rMPC_ActuatorSlewCost;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 3.3: COMPUTATION OF COST FUNCTION ANALYTICAL GRADIENT: Grad_J = 2*B^T*Q*e + 2*R*u + 2*S*Delta_u                     *)
(* -------------------------------------------------------------------------------------------------------------------- *)
FOR iSub := 1 TO 5 DO
    rSumAccumulator := 0.0;
    FOR iRow := 1 TO 8 DO
        rSumAccumulator := rSumAccumulator + (matB[iRow, iSub] * matQ[iRow, iRow] * vecStateError[iRow]);
    END_FOR;
    vecCostGradient[iSub] := (2.0 * rSumAccumulator) + (2.0 * matR[iSub, iSub] * vecU[iSub]) + (2.0 * matS[iSub, iSub] * vecDeltaU[iSub]);
END_FOR;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 3.4: PROJECTED GRADIENT DESCENT ITERATIONS WITH BOX & SLEW CONSTRAINTS                                               *)
(* -------------------------------------------------------------------------------------------------------------------- *)
FOR iMPC_IterationCounter := 1 TO 4 DO
    (* Control 1: 1st Operation Roll Servo Radial Position Offset [mm] *)
    vecU[1] := vecU[1] - (rMPC_OptimizationLearningRate * vecCostGradient[1] / matHessianApprox[1, 1]);
    IF vecU[1] > 2.200 THEN vecU[1] := 2.200; END_IF;
    IF vecU[1] < 0.850 THEN vecU[1] := 0.850; END_IF;

    (* Control 2: 2nd Operation Roll Servo Radial Crimp Offset [mm] *)
    vecU[2] := vecU[2] - (rMPC_OptimizationLearningRate * vecCostGradient[2] / matHessianApprox[2, 2]);
    IF vecU[2] > 1.450 THEN vecU[2] := 1.450; END_IF;
    IF vecU[2] < 0.880 THEN vecU[2] := 0.880; END_IF;

    (* Control 3: Spindle Servo Direct Torque Correction [Nm] *)
    vecU[3] := vecU[3] - (rMPC_OptimizationLearningRate * vecCostGradient[3] / matHessianApprox[3, 3]);
    IF vecU[3] > 45.0 THEN vecU[3] := 45.0; END_IF;
    IF vecU[3] < -45.0 THEN vecU[3] := -45.0; END_IF;

    (* Control 4: Cryogenic LN2 Solenoid Valve Pulse Duration [ms] *)
    vecU[4] := vecU[4] - (rMPC_OptimizationLearningRate * vecCostGradient[4] / matHessianApprox[4, 4]);
    IF vecU[4] > 8.50 THEN vecU[4] := 8.50; END_IF;
    IF vecU[4] < 1.20 THEN vecU[4] := 1.20; END_IF;

    (* Control 5: Lifter Cushion Pneumatic Pressure [bar] *)
    vecU[5] := vecU[5] - (rMPC_OptimizationLearningRate * vecCostGradient[5] / matHessianApprox[5, 5]);
    IF vecU[5] > 6.00 THEN vecU[5] := 6.00; END_IF;
    IF vecU[5] < 2.50 THEN vecU[5] := 2.50; END_IF;
END_FOR;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 3.5: ACTUATOR SLEW RATE LIMITING & FEEDFORWARD COMMAND DISPATCH                                                      *)
(* Maximum allowable changes per 250 microsecond PLC cycle to prevent servo mechanical shock                           *)
(* -------------------------------------------------------------------------------------------------------------------- *)
(* Slew limit 1st Op Roll: max 0.005 mm per 250 us (= 20 mm/s) *)
IF (vecU[1] - vecU_Prev[1]) > 0.005 THEN vecU[1] := vecU_Prev[1] + 0.005; END_IF;
IF (vecU[1] - vecU_Prev[1]) < -0.005 THEN vecU[1] := vecU_Prev[1] - 0.005; END_IF;

(* Slew limit 2nd Op Roll: max 0.004 mm per 250 us (= 16 mm/s) *)
IF (vecU[2] - vecU_Prev[2]) > 0.004 THEN vecU[2] := vecU_Prev[2] + 0.004; END_IF;
IF (vecU[2] - vecU_Prev[2]) < -0.004 THEN vecU[2] := vecU_Prev[2] - 0.004; END_IF;

(* Slew limit Spindle Torque: max 1.5 Nm per 250 us (= 6,000 Nm/s) *)
IF (vecU[3] - vecU_Prev[3]) > 1.5 THEN vecU[3] := vecU_Prev[3] + 1.5; END_IF;
IF (vecU[3] - vecU_Prev[3]) < -1.5 THEN vecU[3] := vecU_Prev[3] - 1.5; END_IF;

(* Slew limit LN2 Pulse Duration: max 0.05 ms per 250 us *)
IF (vecU[4] - vecU_Prev[4]) > 0.05 THEN vecU[4] := vecU_Prev[4] + 0.05; END_IF;
IF (vecU[4] - vecU_Prev[4]) < -0.05 THEN vecU[4] := vecU_Prev[4] - 0.05; END_IF;

(* Slew limit Lifter Cushion Pressure: max 0.02 bar per 250 us *)
IF (vecU[5] - vecU_Prev[5]) > 0.02 THEN vecU[5] := vecU_Prev[5] + 0.02; END_IF;
IF (vecU[5] - vecU_Prev[5]) < -0.02 THEN vecU[5] := vecU_Prev[5] - 0.02; END_IF;

(* Transfer Control Inputs to Physical Output Commands *)
rCmd_1stOpServoRadialPosition_mm   := vecU[1];
rCmd_2ndOpServoRadialPosition_mm   := vecU[2];
rCmd_SpindleElectronicCamTorque_Nm := vecU[3];
rCmd_LN2InjectorPulseDuration_ms   := vecU[4];
rCmd_LifterPneumaticCushion_bar    := vecU[5];

(* Save Prior Controls for next execution cycle *)
FOR iSub := 1 TO 5 DO
    vecU_Prev[iSub] := vecU[iSub];
END_FOR;

(* State update for next cycle *)
FOR iRow := 1 TO 8 DO
    vecX[iRow] := vecX_Next[iRow];
END_FOR;
"""
