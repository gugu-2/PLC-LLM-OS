# biw_laser_brazing_builder/part6_phase3_mpc.py
"""
Part 6: Phase 3 - Receding-Horizon MPC Optimization with Projected Gradient Descent (PGD)
Function Block: FB_Automotive_BIW_LaserBrazing_StructuralAdhesive
"""

def get_phase3_mpc():
    return """(* ============================================================================================== *)
(* PHASE 3: RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) WITH PROJECTED GRADIENT DESCENT (PGD)  *)
(* Prediction Horizon N = 5 steps (10.0 ms predictive window), 6 Unrolled Iterations of PGD        *)
(* Multivariable Actuators:                                                                       *)
(*   u[1] = Fiber Laser Continuous Wave Power [0..5000 W]                                         *)
(*   u[2] = CuSi3 Filler Wire Linear Speed [0..150 mm/s]                                          *)
(*   u[3] = Seam Tracking Tactile/Optical Servo Correction [-25000..+25000 um]                     *)
(*   u[4] = Structural Adhesive Positive-Displacement Gear Pump [0..2500 rpm]                     *)
(*   u[5] = Adhesive Tip Heating Jacket PWM Duty [0..100 %]                                       *)
(*   u[6] = Robot Trajectory Contouring Speed Override [10..100 %]                                *)
(* ============================================================================================== *)

(* ---------------------------------------------------------------------------------------------- *)
(* STEP 3.1: WARM-START CONTROL TRAJECTORY BUFFER ROLLOVER                                        *)
(* Shift previous optimal solution forward: u_traj[k] := u_traj[k+1]                              *)
(* ---------------------------------------------------------------------------------------------- *)
FOR k := 1 TO 4 DO
    FOR j := 1 TO 6 DO
        a_u_traj[k, j] := a_u_traj[k + 1, j];
    END_FOR;
END_FOR;

(* Inject Decoupled Feedforward Targets into Horizon Tail (k=5) *)
a_u_traj[5, 1] := rDecoupledLaserPower;
a_u_traj[5, 2] := rDecoupledWireSpeed;
a_u_traj[5, 3] := a_x_ref[3];
a_u_traj[5, 4] := rDecoupledAdhPumpSpeed;
a_u_traj[5, 5] := a_u_ref[5];
a_u_traj[5, 6] := a_u_ref[6];

(* ---------------------------------------------------------------------------------------------- *)
(* STEP 3.2: 6 UNROLLED ITERATIONS OF PROJECTED GRADIENT DESCENT OPTIMIZATION                     *)
(* ---------------------------------------------------------------------------------------------- *)
FOR nPgdIterCount := 1 TO 6 DO

    (* ------------------------------------------------------------------------------------------ *)
    (* SUB-STEP 3.2.1: FORWARD TRAJECTORY PREDICTION ROLLOUT ACROSS HORIZON k=1..5                *)
    (* x_traj[k+1] = A * x_traj[k] + B * u_traj[k]                                                *)
    (* ------------------------------------------------------------------------------------------ *)
    (* Step k=1 (Originating from current filtered cyber-physical state estimate a_x) *)
    a_x_traj[1, 1] := (a_A[1, 1] * a_x[1]) + (a_A[1, 2] * a_x[2]) + (a_A[1, 3] * a_x[3]) + (a_A[1, 4] * a_x[4])
                    + (a_A[1, 5] * a_x[5]) + (a_A[1, 6] * a_x[6]) + (a_A[1, 7] * a_x[7]) + (a_A[1, 8] * a_x[8])
                    + (a_B[1, 1] * a_u_traj[1, 1]) + (a_B[1, 2] * a_u_traj[1, 2]) + (a_B[1, 3] * a_u_traj[1, 3])
                    + (a_B[1, 4] * a_u_traj[1, 4]) + (a_B[1, 5] * a_u_traj[1, 5]) + (a_B[1, 6] * a_u_traj[1, 6]);

    a_x_traj[1, 2] := (a_A[2, 1] * a_x[1]) + (a_A[2, 2] * a_x[2]) + (a_A[2, 3] * a_x[3]) + (a_A[2, 4] * a_x[4])
                    + (a_A[2, 5] * a_x[5]) + (a_A[2, 6] * a_x[6]) + (a_A[2, 7] * a_x[7]) + (a_A[2, 8] * a_x[8])
                    + (a_B[2, 1] * a_u_traj[1, 1]) + (a_B[2, 2] * a_u_traj[1, 2]) + (a_B[2, 3] * a_u_traj[1, 3])
                    + (a_B[2, 4] * a_u_traj[1, 4]) + (a_B[2, 5] * a_u_traj[1, 5]) + (a_B[2, 6] * a_u_traj[1, 6]);

    a_x_traj[1, 3] := (a_A[3, 1] * a_x[1]) + (a_A[3, 2] * a_x[2]) + (a_A[3, 3] * a_x[3]) + (a_A[3, 4] * a_x[4])
                    + (a_A[3, 5] * a_x[5]) + (a_A[3, 6] * a_x[6]) + (a_A[3, 7] * a_x[7]) + (a_A[3, 8] * a_x[8])
                    + (a_B[3, 1] * a_u_traj[1, 1]) + (a_B[3, 2] * a_u_traj[1, 2]) + (a_B[3, 3] * a_u_traj[1, 3])
                    + (a_B[3, 4] * a_u_traj[1, 4]) + (a_B[3, 5] * a_u_traj[1, 5]) + (a_B[3, 6] * a_u_traj[1, 6]);

    a_x_traj[1, 4] := (a_A[4, 1] * a_x[1]) + (a_A[4, 2] * a_x[2]) + (a_A[4, 3] * a_x[3]) + (a_A[4, 4] * a_x[4])
                    + (a_A[4, 5] * a_x[5]) + (a_A[4, 6] * a_x[6]) + (a_A[4, 7] * a_x[7]) + (a_A[4, 8] * a_x[8])
                    + (a_B[4, 1] * a_u_traj[1, 1]) + (a_B[4, 2] * a_u_traj[1, 2]) + (a_B[4, 3] * a_u_traj[1, 3])
                    + (a_B[4, 4] * a_u_traj[1, 4]) + (a_B[4, 5] * a_u_traj[1, 5]) + (a_B[4, 6] * a_u_traj[1, 6]);

    a_x_traj[1, 5] := (a_A[5, 1] * a_x[1]) + (a_A[5, 2] * a_x[2]) + (a_A[5, 3] * a_x[3]) + (a_A[5, 4] * a_x[4])
                    + (a_A[5, 5] * a_x[5]) + (a_A[5, 6] * a_x[6]) + (a_A[5, 7] * a_x[7]) + (a_A[5, 8] * a_x[8])
                    + (a_B[5, 1] * a_u_traj[1, 1]) + (a_B[5, 2] * a_u_traj[1, 2]) + (a_B[5, 3] * a_u_traj[1, 3])
                    + (a_B[5, 4] * a_u_traj[1, 4]) + (a_B[5, 5] * a_u_traj[1, 5]) + (a_B[5, 6] * a_u_traj[1, 6]);

    a_x_traj[1, 6] := (a_A[6, 1] * a_x[1]) + (a_A[6, 2] * a_x[2]) + (a_A[6, 3] * a_x[3]) + (a_A[6, 4] * a_x[4])
                    + (a_A[6, 5] * a_x[5]) + (a_A[6, 6] * a_x[6]) + (a_A[6, 7] * a_x[7]) + (a_A[6, 8] * a_x[8])
                    + (a_B[6, 1] * a_u_traj[1, 1]) + (a_B[6, 2] * a_u_traj[1, 2]) + (a_B[6, 3] * a_u_traj[1, 3])
                    + (a_B[6, 4] * a_u_traj[1, 4]) + (a_B[6, 5] * a_u_traj[1, 5]) + (a_B[6, 6] * a_u_traj[1, 6]);

    a_x_traj[1, 7] := (a_A[7, 1] * a_x[1]) + (a_A[7, 2] * a_x[2]) + (a_A[7, 3] * a_x[3]) + (a_A[7, 4] * a_x[4])
                    + (a_A[7, 5] * a_x[5]) + (a_A[7, 6] * a_x[6]) + (a_A[7, 7] * a_x[7]) + (a_A[7, 8] * a_x[8])
                    + (a_B[7, 1] * a_u_traj[1, 1]) + (a_B[7, 2] * a_u_traj[1, 2]) + (a_B[7, 3] * a_u_traj[1, 3])
                    + (a_B[7, 4] * a_u_traj[1, 4]) + (a_B[7, 5] * a_u_traj[1, 5]) + (a_B[7, 6] * a_u_traj[1, 6]);

    a_x_traj[1, 8] := (a_A[8, 1] * a_x[1]) + (a_A[8, 2] * a_x[2]) + (a_A[8, 3] * a_x[3]) + (a_A[8, 4] * a_x[4])
                    + (a_A[8, 5] * a_x[5]) + (a_A[8, 6] * a_x[6]) + (a_A[7, 7] * a_x[7]) + (a_A[8, 8] * a_x[8])
                    + (a_B[8, 1] * a_u_traj[1, 1]) + (a_B[8, 2] * a_u_traj[1, 2]) + (a_B[8, 3] * a_u_traj[1, 3])
                    + (a_B[8, 4] * a_u_traj[1, 4]) + (a_B[8, 5] * a_u_traj[1, 5]) + (a_B[8, 6] * a_u_traj[1, 6]);

    (* Steps k=2 TO 5 Rollout *)
    FOR k := 2 TO 5 DO
        FOR i := 1 TO 8 DO
            rTempSum := 0.0;
            FOR m := 1 TO 8 DO
                rTempSum := rTempSum + (a_A[i, m] * a_x_traj[k - 1, m]);
            END_FOR;
            FOR j := 1 TO 6 DO
                rTempSum := rTempSum + (a_B[i, j] * a_u_traj[k, j]);
            END_FOR;
            a_x_traj[k, i] := rTempSum;
        END_FOR;
    END_FOR;

    (* ------------------------------------------------------------------------------------------ *)
    (* SUB-STEP 3.2.2: QUADRATIC OBJECTIVE COST EVALUATION                                        *)
    (* J = sum( (x - x_ref)' Q (x - x_ref) + (u - u_ref)' R (u - u_ref) + du' S du ) + Terminal P *)
    (* ------------------------------------------------------------------------------------------ *)
    rMpcTrackingCost := 0.0;
    rMpcEffortCost := 0.0;

    FOR k := 1 TO 5 DO
        (* State tracking cost component *)
        FOR i := 1 TO 8 DO
            rTempDelta := a_x_traj[k, i] - a_x_ref[i];
            rMpcTrackingCost := rMpcTrackingCost + (a_Q[i] * rTempDelta * rTempDelta);
        END_FOR;
        
        (* Actuator control effort & slew cost component *)
        FOR j := 1 TO 6 DO
            rTempDelta := a_u_traj[k, j] - a_u_ref[j];
            rMpcEffortCost := rMpcEffortCost + (a_R[j] * rTempDelta * rTempDelta);
            
            IF k = 1 THEN
                rSlewDelta := a_u_traj[1, j] - a_u_prev[j];
            ELSE
                rSlewDelta := a_u_traj[k, j] - a_u_traj[k - 1, j];
            END_IF;
            rMpcEffortCost := rMpcEffortCost + (a_S[j] * rSlewDelta * rSlewDelta);
        END_FOR;
    END_FOR;

    (* Add Terminal State Cost at Horizon Boundary k=5 *)
    FOR i := 1 TO 8 DO
        rTempDelta := a_x_traj[5, i] - a_x_ref[i];
        rMpcTrackingCost := rMpcTrackingCost + (a_P[i] * rTempDelta * rTempDelta);
    END_FOR;

    rMpcTotalCost := rMpcTrackingCost + rMpcEffortCost;

    (* ------------------------------------------------------------------------------------------ *)
    (* SUB-STEP 3.2.3: ANALYTICAL BACKWARD GRADIENT COMPUTATION dJ/du[k, j]                       *)
    (* ------------------------------------------------------------------------------------------ *)
    FOR k := 1 TO 5 DO
        FOR j := 1 TO 6 DO
            (* Direct Actuator Effort Gradient Component *)
            rTempGrad := 2.0 * a_R[j] * (a_u_traj[k, j] - a_u_ref[j]);

            (* Direct Slew Rate Gradient Component *)
            IF k = 1 THEN
                rTempGrad := rTempGrad + 2.0 * a_S[j] * (a_u_traj[1, j] - a_u_prev[j]);
            ELSE
                rTempGrad := rTempGrad + 2.0 * a_S[j] * (a_u_traj[k, j] - a_u_traj[k - 1, j]);
            END_IF;

            IF k < 5 THEN
                rTempGrad := rTempGrad - 2.0 * a_S[j] * (a_u_traj[k + 1, j] - a_u_traj[k, j]);
            END_IF;

            (* Propagated State Tracking Error Gradient: sum_i (2 * Q_i * (x_i - x_ref_i) * B[i, j]) *)
            FOR i := 1 TO 8 DO
                rTempGrad := rTempGrad + (2.0 * a_Q[i] * (a_x_traj[k, i] - a_x_ref[i]) * a_B[i, j]);
            END_FOR;

            (* Terminal State Penalty Contribution for Horizon End (k=5) *)
            IF k = 5 THEN
                FOR i := 1 TO 8 DO
                    rTempGrad := rTempGrad + (2.0 * a_P[i] * (a_x_traj[5, i] - a_x_ref[i]) * a_B[i, j]);
                END_FOR;
            END_IF;

            a_grad[k, j] := rTempGrad;
        END_FOR;
    END_FOR;

    (* ------------------------------------------------------------------------------------------ *)
    (* SUB-STEP 3.2.4: GRADIENT UPDATE WITH PHYSICAL CONSTRAINT PROJECTION                        *)
    (* u_new = Project(u_old - alpha * grad)                                                      *)
    (* ------------------------------------------------------------------------------------------ *)
    FOR k := 1 TO 5 DO
        FOR j := 1 TO 6 DO
            (* Gradient Descent Step *)
            rCandidateVal := a_u_traj[k, j] - (rPgdStepSize * a_grad[k, j]);

            (* Dynamic Slew Rate Clamping vs Preceding Time Step *)
            IF k = 1 THEN
                IF (rCandidateVal - a_u_prev[j]) > a_du_max[j] THEN
                    rCandidateVal := a_u_prev[j] + a_du_max[j];
                ELSIF (rCandidateVal - a_u_prev[j]) < -a_du_max[j] THEN
                    rCandidateVal := a_u_prev[j] - a_du_max[j];
                END_IF;
            ELSE
                IF (rCandidateVal - a_u_traj[k - 1, j]) > a_du_max[j] THEN
                    rCandidateVal := a_u_traj[k - 1, j] + a_du_max[j];
                ELSIF (rCandidateVal - a_u_traj[k - 1, j]) < -a_du_max[j] THEN
                    rCandidateVal := a_u_traj[k - 1, j] - a_du_max[j];
                END_IF;
            END_IF;

            (* Hard Actuator Saturation Clamping [u_min .. u_max] *)
            IF rCandidateVal > a_u_max[j] THEN
                rCandidateVal := a_u_max[j];
            ELSIF rCandidateVal < a_u_min[j] THEN
                rCandidateVal := a_u_min[j];
            END_IF;

            a_u_traj[k, j] := rCandidateVal;
        END_FOR;
    END_FOR;

END_FOR; (* End of 6 Unrolled PGD Iterations *)

(* ---------------------------------------------------------------------------------------------- *)
(* STEP 3.3: EXTRACT RECEDING-HORIZON OPTIMAL FIRST CONTROL MOVE u*(k)                            *)
(* ---------------------------------------------------------------------------------------------- *)
FOR j := 1 TO 6 DO
    a_u[j] := a_u_traj[1, j];
    a_du[j] := a_u[j] - a_u_prev[j];
    a_u_prev[j] := a_u[j];
END_FOR;
"""
