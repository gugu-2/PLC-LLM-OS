# blown_film_builder/st_phase3_mpc.py

def get_phase3_mpc():
    return """(* ==================================================================================================== *)
(* PHASE 3: RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) WITH PROJECTED GRADIENT DESCENT (PGD)       *)
(* 10 Unrolled PGD Iterations, Horizon N = 5 (100 [ms]), 128-Zone Air Ring Spatial Gaussian Decoupling   *)
(* ==================================================================================================== *)

    (* ------------------------------------------------------------------------------------------------ *)
    (* Step 3A: Dynamic State Reference Target Adaptation Across FSM Production States                 *)
    (* ------------------------------------------------------------------------------------------------ *)
    IF eState_Current = 5 THEN
        (* State 5: Frost-Line Stabilization Ramp - Tighter FLH and Controlled Bubble Velocity *)
        vecX_target[0] := 0.0;   (* Target Zero Thickness Deviation [um] *)
        vecX_target[1] := 0.0;   (* Nominal Bubble Diameter [mm] *)
        vecX_target[2] := 0.0;   (* Standard IBC Differential Pressure [Pa] *)
        vecX_target[3] := -25.0; (* Pull FLH Slightly Lower to Establish Stalk Freeze Line [mm] *)
        vecX_target[4] := 0.0;   (* Nominal Melt Temperature [deg C] *)
        vecX_target[5] := -15.0; (* Slightly Reduced Tension During Initial Nip Acquisition [N] *)
    ELSIF eState_Current = 10 THEN
        (* State 10: Dynamic Recipe Width or Thickness Transition *)
        vecX_target[0] := 0.0;   (* Target Rapid Gauge Convergence [um] *)
        vecX_target[1] := 0.0;   (* Diameter Trajectory Tracking [mm] *)
        vecX_target[2] := 0.0;   (* Differential Air Exchange Balance [Pa] *)
        vecX_target[3] := 0.0;   (* Maintain Steady Frost-Line Height [mm] *)
        vecX_target[4] := 0.0;   (* Hold Constant Tooling Temperature [deg C] *)
        vecX_target[5] := 0.0;   (* Maintain Stable Nip Roll Web Tension [N] *)
    ELSIF eState_Current = 11 THEN
        (* State 11: Bubble Breathe Instability Damping Mode *)
        vecX_target[0] := 0.0;   (* Suppress Gauge Pulsations [um] *)
        vecX_target[1] := 0.0;   (* Clamp Diameter Breathing Perturbation [mm] *)
        vecX_target[2] := 0.0;   (* Drive Differential Pressure Fluctuations to Zero [Pa] *)
        vecX_target[3] := 10.0;  (* Elevate FLH Slightly to Soften Bubble Aerodynamic Coupling [mm] *)
        vecX_target[4] := 0.0;   (* Melt Temperature Held Constant [deg C] *)
        vecX_target[5] := 10.0;  (* Elevate Tension to Stiffen Bubble Column [N] *)
    ELSE
        (* State 8 & 9: Nominal High-Speed Steady Production *)
        vecX_target[0] := 0.0;   (* Zero 2-Sigma Thickness Error [um] *)
        vecX_target[1] := 0.0;   (* Zero Bubble Diameter Error [mm] *)
        vecX_target[2] := 0.0;   (* Zero IBC Differential Pressure Error [Pa] *)
        vecX_target[3] := 0.0;   (* Zero Frost-Line Height Error [mm] *)
        vecX_target[4] := 0.0;   (* Zero Melt Temperature Error [deg C] *)
        vecX_target[5] := 0.0;   (* Zero Haul-Off Web Tension Error [N] *)
    END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* Step 3B: Initialize Prediction Horizon State & Control Trajectories                             *)
    (* ------------------------------------------------------------------------------------------------ *)
    FOR iIdx := 0 TO 5 DO
        trajX_mpc[0, iIdx] := vecX_hat[iIdx];
    END_FOR;

    FOR kStep := 0 TO 4 DO
        FOR mIdx := 0 TO 5 DO
            trajU_mpc[kStep, mIdx] := vecU[mIdx];
        END_FOR;
    END_FOR;

    (* ------------------------------------------------------------------------------------------------ *)
    (* Step 3C: Unrolled Projected Gradient Descent (PGD) Solver Core (10 Fixed Iterations)            *)
    (* ------------------------------------------------------------------------------------------------ *)
    FOR iIter := 1 TO 10 DO
        (* Sub-step C1: Forward State Simulation Over Horizon N = 5 (Sample Time Ts = 20 [ms]) *)
        FOR kStep := 0 TO 4 DO
            FOR iIdx := 0 TO 5 DO
                rTempSum := 0.0;
                FOR jIdx := 0 TO 5 DO
                    rTempSum := rTempSum + (matA[iIdx, jIdx] * trajX_mpc[kStep, jIdx]);
                END_FOR;
                FOR mIdx := 0 TO 5 DO
                    rTempSum := rTempSum + (matB[iIdx, mIdx] * (trajU_mpc[kStep, mIdx] - vecU_target[mIdx]));
                END_FOR;
                trajX_mpc[kStep + 1, iIdx] := rTempSum;
            END_FOR;
        END_FOR;

        (* Sub-step C2: Forward Quadratic Objective Cost Functional Evaluation J *)
        rMpc_AccumulatedCost := 0.0;
        FOR kStep := 1 TO 4 DO
            FOR iIdx := 0 TO 5 DO
                rTempDiff := trajX_mpc[kStep, iIdx] - vecX_target[iIdx];
                rMpc_AccumulatedCost := rMpc_AccumulatedCost + (vecQ_weight[iIdx] * rTempDiff * rTempDiff);
            END_FOR;
        END_FOR;

        (* Terminal State Penalty at Horizon Step k = 5 *)
        FOR iIdx := 0 TO 5 DO
            rTempDiff := trajX_mpc[5, iIdx] - vecX_target[iIdx];
            rMpc_AccumulatedCost := rMpc_AccumulatedCost + (vecP_terminal[iIdx] * rTempDiff * rTempDiff);
        END_FOR;

        (* Actuator Energy & Slew Rate Penalties *)
        FOR kStep := 0 TO 4 DO
            FOR mIdx := 0 TO 5 DO
                rTempDiff := trajU_mpc[kStep, mIdx] - vecU_target[mIdx];
                rMpc_AccumulatedCost := rMpc_AccumulatedCost + (vecR_weight[mIdx] * rTempDiff * rTempDiff);

                IF kStep = 0 THEN
                    rTempDiff := trajU_mpc[0, mIdx] - vecU_prev[mIdx];
                ELSE
                    rTempDiff := trajU_mpc[kStep, mIdx] - trajU_mpc[kStep - 1, mIdx];
                END_IF;
                rMpc_AccumulatedCost := rMpc_AccumulatedCost + (vecR_rate_weight[mIdx] * rTempDiff * rTempDiff);
            END_FOR;
        END_FOR;

        (* Sub-step C3: Backward Adjoint Costate Vector Recursion (Pontryagin Maximum Principle) *)
        (* Terminal Costate Condition at Horizon Step k = 5: lambda[5] = 2 * P * (x[5] - x_target) *)
        FOR iIdx := 0 TO 5 DO
            adjointLambda[5, iIdx] := 2.0 * vecP_terminal[iIdx] * (trajX_mpc[5, iIdx] - vecX_target[iIdx]);
        END_FOR;

        (* Backward Propagation: lambda[k] = 2 * Q * (x[k] - x_target) + A^T * lambda[k+1] *)
        adjointLambda[4, 0] := 2.0 * vecQ_weight[0] * (trajX_mpc[4, 0] - vecX_target[0]) + (matA[0, 0]*adjointLambda[5, 0] + matA[1, 0]*adjointLambda[5, 1] + matA[2, 0]*adjointLambda[5, 2] + matA[3, 0]*adjointLambda[5, 3] + matA[4, 0]*adjointLambda[5, 4] + matA[5, 0]*adjointLambda[5, 5]);
        adjointLambda[4, 1] := 2.0 * vecQ_weight[1] * (trajX_mpc[4, 1] - vecX_target[1]) + (matA[0, 1]*adjointLambda[5, 0] + matA[1, 1]*adjointLambda[5, 1] + matA[2, 1]*adjointLambda[5, 2] + matA[3, 1]*adjointLambda[5, 3] + matA[4, 1]*adjointLambda[5, 4] + matA[5, 1]*adjointLambda[5, 5]);
        adjointLambda[4, 2] := 2.0 * vecQ_weight[2] * (trajX_mpc[4, 2] - vecX_target[2]) + (matA[0, 2]*adjointLambda[5, 0] + matA[1, 2]*adjointLambda[5, 1] + matA[2, 2]*adjointLambda[5, 2] + matA[3, 2]*adjointLambda[5, 3] + matA[4, 2]*adjointLambda[5, 4] + matA[5, 2]*adjointLambda[5, 5]);
        adjointLambda[4, 3] := 2.0 * vecQ_weight[3] * (trajX_mpc[4, 3] - vecX_target[3]) + (matA[0, 3]*adjointLambda[5, 0] + matA[1, 3]*adjointLambda[5, 1] + matA[2, 3]*adjointLambda[5, 2] + matA[3, 3]*adjointLambda[5, 3] + matA[4, 3]*adjointLambda[5, 4] + matA[5, 3]*adjointLambda[5, 5]);
        adjointLambda[4, 4] := 2.0 * vecQ_weight[4] * (trajX_mpc[4, 4] - vecX_target[4]) + (matA[0, 4]*adjointLambda[5, 0] + matA[1, 4]*adjointLambda[5, 1] + matA[2, 4]*adjointLambda[5, 2] + matA[3, 4]*adjointLambda[5, 3] + matA[4, 4]*adjointLambda[5, 4] + matA[5, 4]*adjointLambda[5, 5]);
        adjointLambda[4, 5] := 2.0 * vecQ_weight[5] * (trajX_mpc[4, 5] - vecX_target[5]) + (matA[0, 5]*adjointLambda[5, 0] + matA[1, 5]*adjointLambda[5, 1] + matA[2, 5]*adjointLambda[5, 2] + matA[3, 5]*adjointLambda[5, 3] + matA[4, 5]*adjointLambda[5, 4] + matA[5, 5]*adjointLambda[5, 5]);

        adjointLambda[3, 0] := 2.0 * vecQ_weight[0] * (trajX_mpc[3, 0] - vecX_target[0]) + (matA[0, 0]*adjointLambda[4, 0] + matA[1, 0]*adjointLambda[4, 1] + matA[2, 0]*adjointLambda[4, 2] + matA[3, 0]*adjointLambda[4, 3] + matA[4, 0]*adjointLambda[4, 4] + matA[5, 0]*adjointLambda[4, 5]);
        adjointLambda[3, 1] := 2.0 * vecQ_weight[1] * (trajX_mpc[3, 1] - vecX_target[1]) + (matA[0, 1]*adjointLambda[4, 0] + matA[1, 1]*adjointLambda[4, 1] + matA[2, 1]*adjointLambda[4, 2] + matA[3, 1]*adjointLambda[4, 3] + matA[4, 1]*adjointLambda[4, 4] + matA[5, 1]*adjointLambda[4, 5]);
        adjointLambda[3, 2] := 2.0 * vecQ_weight[2] * (trajX_mpc[3, 2] - vecX_target[2]) + (matA[0, 2]*adjointLambda[4, 0] + matA[1, 2]*adjointLambda[4, 1] + matA[2, 2]*adjointLambda[4, 2] + matA[3, 2]*adjointLambda[4, 3] + matA[4, 2]*adjointLambda[4, 4] + matA[5, 2]*adjointLambda[4, 5]);
        adjointLambda[3, 3] := 2.0 * vecQ_weight[3] * (trajX_mpc[3, 3] - vecX_target[3]) + (matA[0, 3]*adjointLambda[4, 0] + matA[1, 3]*adjointLambda[4, 1] + matA[2, 3]*adjointLambda[4, 2] + matA[3, 3]*adjointLambda[4, 3] + matA[4, 3]*adjointLambda[4, 4] + matA[5, 3]*adjointLambda[4, 5]);
        adjointLambda[3, 4] := 2.0 * vecQ_weight[4] * (trajX_mpc[3, 4] - vecX_target[4]) + (matA[0, 4]*adjointLambda[4, 0] + matA[1, 4]*adjointLambda[4, 1] + matA[2, 4]*adjointLambda[4, 2] + matA[3, 4]*adjointLambda[4, 3] + matA[4, 4]*adjointLambda[4, 4] + matA[5, 4]*adjointLambda[4, 5]);
        adjointLambda[3, 5] := 2.0 * vecQ_weight[5] * (trajX_mpc[3, 5] - vecX_target[5]) + (matA[0, 5]*adjointLambda[4, 0] + matA[1, 5]*adjointLambda[4, 1] + matA[2, 5]*adjointLambda[4, 2] + matA[3, 5]*adjointLambda[4, 3] + matA[4, 5]*adjointLambda[4, 4] + matA[5, 5]*adjointLambda[4, 5]);

        adjointLambda[2, 0] := 2.0 * vecQ_weight[0] * (trajX_mpc[2, 0] - vecX_target[0]) + (matA[0, 0]*adjointLambda[3, 0] + matA[1, 0]*adjointLambda[3, 1] + matA[2, 0]*adjointLambda[3, 2] + matA[3, 0]*adjointLambda[3, 3] + matA[4, 0]*adjointLambda[3, 4] + matA[5, 0]*adjointLambda[3, 5]);
        adjointLambda[2, 1] := 2.0 * vecQ_weight[1] * (trajX_mpc[2, 1] - vecX_target[1]) + (matA[0, 1]*adjointLambda[3, 0] + matA[1, 1]*adjointLambda[3, 1] + matA[2, 1]*adjointLambda[3, 2] + matA[3, 1]*adjointLambda[3, 3] + matA[4, 1]*adjointLambda[3, 4] + matA[5, 1]*adjointLambda[3, 5]);
        adjointLambda[2, 2] := 2.0 * vecQ_weight[2] * (trajX_mpc[2, 2] - vecX_target[2]) + (matA[0, 2]*adjointLambda[3, 0] + matA[1, 2]*adjointLambda[3, 1] + matA[2, 2]*adjointLambda[3, 2] + matA[3, 2]*adjointLambda[3, 3] + matA[4, 2]*adjointLambda[3, 4] + matA[5, 2]*adjointLambda[3, 5]);
        adjointLambda[2, 3] := 2.0 * vecQ_weight[3] * (trajX_mpc[2, 3] - vecX_target[3]) + (matA[0, 3]*adjointLambda[3, 0] + matA[1, 3]*adjointLambda[3, 1] + matA[2, 3]*adjointLambda[3, 2] + matA[3, 3]*adjointLambda[3, 3] + matA[4, 3]*adjointLambda[3, 4] + matA[5, 3]*adjointLambda[3, 5]);
        adjointLambda[2, 4] := 2.0 * vecQ_weight[4] * (trajX_mpc[2, 4] - vecX_target[4]) + (matA[0, 4]*adjointLambda[3, 0] + matA[1, 4]*adjointLambda[3, 1] + matA[2, 4]*adjointLambda[3, 2] + matA[3, 4]*adjointLambda[3, 3] + matA[4, 4]*adjointLambda[3, 4] + matA[5, 4]*adjointLambda[3, 5]);
        adjointLambda[2, 5] := 2.0 * vecQ_weight[5] * (trajX_mpc[2, 5] - vecX_target[5]) + (matA[0, 5]*adjointLambda[3, 0] + matA[1, 5]*adjointLambda[3, 1] + matA[2, 5]*adjointLambda[3, 2] + matA[3, 5]*adjointLambda[3, 3] + matA[4, 5]*adjointLambda[3, 4] + matA[5, 5]*adjointLambda[3, 5]);

        adjointLambda[1, 0] := 2.0 * vecQ_weight[0] * (trajX_mpc[1, 0] - vecX_target[0]) + (matA[0, 0]*adjointLambda[2, 0] + matA[1, 0]*adjointLambda[2, 1] + matA[2, 0]*adjointLambda[2, 2] + matA[3, 0]*adjointLambda[2, 3] + matA[4, 0]*adjointLambda[2, 4] + matA[5, 0]*adjointLambda[2, 5]);
        adjointLambda[1, 1] := 2.0 * vecQ_weight[1] * (trajX_mpc[1, 1] - vecX_target[1]) + (matA[0, 1]*adjointLambda[2, 0] + matA[1, 1]*adjointLambda[2, 1] + matA[2, 1]*adjointLambda[2, 2] + matA[3, 1]*adjointLambda[2, 3] + matA[4, 1]*adjointLambda[2, 4] + matA[5, 1]*adjointLambda[2, 5]);
        adjointLambda[1, 2] := 2.0 * vecQ_weight[2] * (trajX_mpc[1, 2] - vecX_target[2]) + (matA[0, 2]*adjointLambda[2, 0] + matA[1, 2]*adjointLambda[2, 1] + matA[2, 2]*adjointLambda[2, 2] + matA[3, 2]*adjointLambda[2, 3] + matA[4, 2]*adjointLambda[2, 4] + matA[5, 2]*adjointLambda[2, 5]);
        adjointLambda[1, 3] := 2.0 * vecQ_weight[3] * (trajX_mpc[1, 3] - vecX_target[3]) + (matA[0, 3]*adjointLambda[2, 0] + matA[1, 3]*adjointLambda[2, 1] + matA[2, 3]*adjointLambda[2, 2] + matA[3, 3]*adjointLambda[2, 3] + matA[4, 3]*adjointLambda[2, 4] + matA[5, 3]*adjointLambda[2, 5]);
        adjointLambda[1, 4] := 2.0 * vecQ_weight[4] * (trajX_mpc[1, 4] - vecX_target[4]) + (matA[0, 4]*adjointLambda[2, 0] + matA[1, 4]*adjointLambda[2, 1] + matA[2, 4]*adjointLambda[2, 2] + matA[3, 4]*adjointLambda[2, 3] + matA[4, 4]*adjointLambda[2, 4] + matA[5, 4]*adjointLambda[2, 5]);
        adjointLambda[1, 5] := 2.0 * vecQ_weight[5] * (trajX_mpc[1, 5] - vecX_target[5]) + (matA[0, 5]*adjointLambda[2, 0] + matA[1, 5]*adjointLambda[2, 1] + matA[2, 5]*adjointLambda[2, 2] + matA[3, 5]*adjointLambda[2, 3] + matA[4, 5]*adjointLambda[2, 4] + matA[5, 5]*adjointLambda[2, 5]);

        (* Sub-step C4: Projected Gradient Descent Step with Actuator Slew & Box Projections *)
        FOR kStep := 0 TO 4 DO
            FOR mIdx := 0 TO 5 DO
                (* Gradient Computation: grad = 2*R*(u - u_target) + 2*R_rate*(u - u_prior) + B^T * lambda[k+1] *)
                rTempSum := (matB[0, mIdx] * adjointLambda[kStep + 1, 0]) +
                            (matB[1, mIdx] * adjointLambda[kStep + 1, 1]) +
                            (matB[2, mIdx] * adjointLambda[kStep + 1, 2]) +
                            (matB[3, mIdx] * adjointLambda[kStep + 1, 3]) +
                            (matB[4, mIdx] * adjointLambda[kStep + 1, 4]) +
                            (matB[5, mIdx] * adjointLambda[kStep + 1, 5]);

                rTempGrad := (2.0 * vecR_weight[mIdx] * (trajU_mpc[kStep, mIdx] - vecU_target[mIdx])) + rTempSum;

                IF kStep = 0 THEN
                    rTempGrad := rTempGrad + (2.0 * vecR_rate_weight[mIdx] * (trajU_mpc[0, mIdx] - vecU_prev[mIdx]));
                ELSE
                    rTempGrad := rTempGrad + (2.0 * vecR_rate_weight[mIdx] * (trajU_mpc[kStep, mIdx] - trajU_mpc[kStep - 1, mIdx]));
                END_IF;

                gradU_mpc[kStep, mIdx] := rTempGrad;

                (* Gradient Descent Update *)
                rTempStep := trajU_mpc[kStep, mIdx] - (rMpc_StepSizeAlpha * rTempGrad);

                (* Physical Box Saturation Projection *)
                IF rTempStep < vecU_min[mIdx] THEN
                    rTempStep := vecU_min[mIdx];
                ELSIF rTempStep > vecU_max[mIdx] THEN
                    rTempStep := vecU_max[mIdx];
                END_IF;

                (* Slew Rate Limit Projection *)
                IF kStep = 0 THEN
                    IF (rTempStep - vecU_prev[mIdx]) > vecU_slew_max[mIdx] THEN
                        rTempStep := vecU_prev[mIdx] + vecU_slew_max[mIdx];
                    ELSIF (rTempStep - vecU_prev[mIdx]) < -vecU_slew_max[mIdx] THEN
                        rTempStep := vecU_prev[mIdx] - vecU_slew_max[mIdx];
                    END_IF;
                ELSE
                    IF (rTempStep - trajU_mpc[kStep - 1, mIdx]) > vecU_slew_max[mIdx] THEN
                        rTempStep := trajU_mpc[kStep - 1, mIdx] + vecU_slew_max[mIdx];
                    ELSIF (rTempStep - trajU_mpc[kStep - 1, mIdx]) < -vecU_slew_max[mIdx] THEN
                        rTempStep := trajU_mpc[kStep - 1, mIdx] - vecU_slew_max[mIdx];
                    END_IF;
                END_IF;

                trajU_mpc[kStep, mIdx] := rTempStep;
            END_FOR;
        END_FOR;
    END_FOR;

    (* ------------------------------------------------------------------------------------------------ *)
    (* Step 3D: Apply Receding Horizon Principle - Commit Step 0 Optimal Control Vector                 *)
    (* ------------------------------------------------------------------------------------------------ *)
    FOR mIdx := 0 TO 5 DO
        vecU[mIdx] := trajU_mpc[0, mIdx];
        vecU_rate[mIdx] := (vecU[mIdx] - vecU_prev[mIdx]) / tScanCycleTime_s;
        vecU_prev[mIdx] := vecU[mIdx];
    END_FOR;

    rMPC_CurrentCost_J := rMpc_AccumulatedCost;

    (* ------------------------------------------------------------------------------------------------ *)
    (* Step 3E: 128-Zone Segmented Dual-Lip Air Ring Spatial Thermal Optimization Core                  *)
    (* Haul-Off Nip Oscillation Phase Lag Integration & Spatial Gaussian Decoupling Convolution        *)
    (* ------------------------------------------------------------------------------------------------ *)
    (* Polymer melt transit delay tau = H_nip / V_line (nominally 12.5 s at 150 m/min) *)
    IF rRecipe_LineSpeed_mpm > 10.0 THEN
        rBubbleTransitTime_s := 31.25 / (rRecipe_LineSpeed_mpm / 60.0);
    ELSE
        rBubbleTransitTime_s := 12.5;
    END_IF;

    (* Effective Nip Angle Phase Lag Computation *)
    IF bHaulOff_OscillatingDirRev THEN
        rNipEffectiveAngle_deg := rHaulOff_OscillatingAngle_deg - (1.00 * rBubbleTransitTime_s);
    ELSE
        rNipEffectiveAngle_deg := rHaulOff_OscillatingAngle_deg + (1.00 * rBubbleTransitTime_s);
    END_IF;

    (* Wrap Effective Angle to [0..360) Circle *)
    IF rNipEffectiveAngle_deg < 0.0 THEN
        rNipEffectiveAngle_deg := rNipEffectiveAngle_deg + 360.0;
    ELSIF rNipEffectiveAngle_deg >= 360.0 THEN
        rNipEffectiveAngle_deg := rNipEffectiveAngle_deg - 360.0;
    END_IF;

    (* Discretize Net Angular Offset Into 128 Discrete Circumferential Air Ring Zones *)
    iPhaseShiftZones := REAL_TO_INT(rNipEffectiveAngle_deg * 128.0 / 360.0) MOD 128;

    (* Map Rotating Gauge Measurements Into Stationary Die Orifice Frame *)
    FOR zIdx := 0 TO 127 DO
        arrThicknessError_um[zIdx] := arrFilteredProfile_um[zIdx] - rRecipe_TargetThickness_um;
        iMappedZone := (zIdx + iPhaseShiftZones + 128) MOD 128;
        arrMappedBoltError_um[iMappedZone] := arrThicknessError_um[zIdx];
    END_FOR;

    (* Execute Spatial Gaussian Influence Convolution & Individual Bolt Power Trim *)
    FOR zIdx := 0 TO 127 DO
        rConvolvedError := 0.0;
        FOR kKernel := -4 TO 4 DO
            iMappedZone := (zIdx + kKernel + 128) MOD 128;
            rConvolvedError := rConvolvedError + (arrGaussianKernel[ABS(kKernel)] * arrMappedBoltError_um[iMappedZone]);
        END_FOR;

        (* Physics: Positive error = film too thick -> heat bolt -> expansion narrows gap -> cools slower -> draws thinner *)
        rTempStep := arrBoltThermalPower_Prev[zIdx] + (rAirRing_SpatialMappingGain_Kp * rConvolvedError * rBoltThermalExpansionGain_um_pct);

        (* Superimpose Global Thermal Bias From MPC Channel u[0] *)
        rTempStep := rTempStep + ((vecU[0] - 50.0) * 0.120);

        (* Slew Rate Saturation: Protect Thermal Expansion Rod From Thermal Shock *)
        rTempGrad := rBoltPowerSlewRate_pct_s * tScanCycleTime_s;
        IF (rTempStep - arrBoltThermalPower_Prev[zIdx]) > rTempGrad THEN
            rTempStep := arrBoltThermalPower_Prev[zIdx] + rTempGrad;
        ELSIF (rTempStep - arrBoltThermalPower_Prev[zIdx]) < -rTempGrad THEN
            rTempStep := arrBoltThermalPower_Prev[zIdx] - rTempGrad;
        END_IF;

        (* Clamp Thermal Bolt Duty Cycle to Safe Electric Operating Band [10..95%] *)
        IF rTempStep < 10.0 THEN
            rTempStep := 10.0;
        ELSIF rTempStep > 95.0 THEN
            rTempStep := 95.0;
        END_IF;

        arrBoltThermalPower_Target[zIdx] := rTempStep;
        arrAirRing_ThermalBoltPower_pct[zIdx] := rTempStep;
        arrBoltThermalPower_Prev[zIdx] := rTempStep;

        (* Simulated Bolt Heater Continuity Current Diagnostic Monitor [A] *)
        arrBoltHeaterCurrent_A[zIdx] := 0.0430 * rTempStep;
        arrBoltZoneHealthy[zIdx] := (arrBoltHeaterCurrent_A[zIdx] >= 0.35) AND (arrBoltHeaterCurrent_A[zIdx] <= 4.45);
    END_FOR;
"""
