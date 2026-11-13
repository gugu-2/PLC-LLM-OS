# stator_laser_welding_builder/part6_phase3_mpc.py

def get_phase3_mpc():
    return """(*
====================================================================================================
PHASE 3: RECEDING-HORIZON MPC OPTIMIZATION WITH PROJECTED GRADIENT DESCENT (PGD) & SLEW LIMITS
Prediction Horizon Np = 5 (10.0 [ms]), Control Horizon Nc = 3 (6.0 [ms]), Step Rate Ts = 2.0 [ms]
Unrolled Multi-Step Quadratic Objective:
  J = sum_{i=1..Np} ||x_{k+i} - x_ref||_Q^2 + sum_{j=1..Nc} ||u_{k+j} - u_ref||_R^2
    + sum_{j=1..Nc} ||delta_u_{k+j}||_{R_slew}^2 + ||x_{k+Np} - x_ref||_P^2
====================================================================================================
*)

(* -------------------------------------------------------------------------------------------------
   STEP 3.1: DYNAMIC REFERENCE TRAJECTORY GENERATION & GAP-ADAPTIVE PARAMETERS
   ------------------------------------------------------------------------------------------------- *)
IF iFSM_CurrentState = 6 THEN
    (* Stage 6: Active Laser Seam Welding Mode *)
    CASE iWeldSubPhase OF
        1: (* Subphase 1: Low-Reflectivity Thermal Pre-Heat Ramp *)
            arrX_Reference[1] := 950.0;     (* Target Solid-Phase Hot Pool Temp [deg C] *)
            arrX_Reference[2] := 450.0;     (* HAZ Warmup [deg C] *)
            arrX_Reference[3] := 120.0;     (* Pin Base Temp [deg C] *)
            arrX_Reference[4] := 0.000;     (* Zero Keyhole in Solid State [mm] *)
            arrX_Reference[5] := 0.100;     (* Incipient Nugget Formation [mm3] *)
            arrX_Reference[6] := 0.000;     (* Strict Chuck Alignment [mrad] *)
            arrX_Reference[7] := 0.000;     (* Zero Velocity [rad/s] *)
            arrX_Reference[8] := 98.50;     (* High N2 Shielding Purity [%] *)

            rTemp_Scalar1 := rPreheatPower_kW;
            rTemp_Scalar2 := 500.0;

        2: (* Subphase 2: Keyhole Deep Vapor Capillary Ignition *)
            arrX_Reference[1] := 2050.0;    (* Vapor Plume Ignition Temp [deg C] *)
            arrX_Reference[2] := 820.0;     (* HAZ Expansion [deg C] *)
            arrX_Reference[3] := 185.0;     (* Pin Bulk Temp [deg C] *)
            arrX_Reference[4] := 2.450;     (* Deep Penetration Capillary [mm] *)
            arrX_Reference[5] := 1.450;     (* Rapid Nugget Growth [mm3] *)
            arrX_Reference[6] := 0.000;
            arrX_Reference[7] := 0.000;
            arrX_Reference[8] := 99.00;

            rTemp_Scalar1 := rPenetrationPower_kW;
            rTemp_Scalar2 := 650.0;

        3: (* Subphase 3: Continuous High-Frequency Dynamic Wobble Fusion *)
            arrX_Reference[1] := 1850.0;    (* Equilibrium Molten Pool Temp [deg C] *)
            arrX_Reference[2] := 780.0;     (* HAZ Boundary [deg C] *)
            arrX_Reference[3] := 210.0;     (* Pin Bulk Temp [deg C] *)
            arrX_Reference[4] := 2.100;     (* Stable Keyhole Depth [mm] *)
            arrX_Reference[5] := 2.850;     (* Full Structural Nugget Volume [mm3] *)
            arrX_Reference[6] := 0.000;
            arrX_Reference[7] := 0.000;
            arrX_Reference[8] := 99.20;

            rTemp_Scalar1 := rMainWeldPower_kW;
            rTemp_Scalar2 := rWeldWobbleFreq_Hz;

        4: (* Subphase 4: Downslope Power Ramp & Solidification Crater Fill *)
            arrX_Reference[1] := 1250.0;    (* Controlled Solidification [deg C] *)
            arrX_Reference[2] := 620.0;     (* Thermal Decay [deg C] *)
            arrX_Reference[3] := 195.0;     (* Pin Temp [deg C] *)
            arrX_Reference[4] := 0.450;     (* Keyhole Gentle Collapse [mm] *)
            arrX_Reference[5] := 3.100;     (* Final Frozen Nugget Volume [mm3] *)
            arrX_Reference[6] := 0.000;
            arrX_Reference[7] := 0.000;
            arrX_Reference[8] := 98.80;

            rTemp_Scalar1 := rDownslopePower_kW;
            rTemp_Scalar2 := 450.0;
    ELSE
        (* Default / Transition Inactive Reference *)
        arrX_Reference[1] := 25.0;
        arrX_Reference[2] := 25.0;
        arrX_Reference[3] := 25.0;
        arrX_Reference[4] := 0.0;
        arrX_Reference[5] := 0.0;
        arrX_Reference[6] := 0.0;
        arrX_Reference[7] := 0.0;
        arrX_Reference[8] := 95.0;

        rTemp_Scalar1 := 0.0;
        rTemp_Scalar2 := 300.0;
    END_CASE;

    (* Gap-Adaptive Dynamic Power & Wobble Compensation *)
    IF rGap_Voted_mm > 0.025 THEN
        (* Broaden wobble amplitude and elevate baseline power to bridge copper gap *)
        rTemp_Scalar1 := rTemp_Scalar1 + (MIN(0.120, rGap_Voted_mm) * 6.50);
        rWeldWobbleAmp_mm := 0.85 + (MIN(0.120, rGap_Voted_mm) * 3.20);
    ELSE
        rWeldWobbleAmp_mm := 0.85;
    END_IF;
ELSE
    (* Non-Welding Stages: Standby References *)
    arrX_Reference[1] := 25.0;
    arrX_Reference[2] := 25.0;
    arrX_Reference[3] := 25.0;
    arrX_Reference[4] := 0.0;
    arrX_Reference[5] := 0.0;
    arrX_Reference[6] := 0.0;
    arrX_Reference[7] := 0.0;
    arrX_Reference[8] := 95.0;

    rTemp_Scalar1 := 0.0;
    rTemp_Scalar2 := 300.0;
    rWeldWobbleAmp_mm := 0.85;
END_IF;

(* Clamp Baseline Power Reference to Absolute Limits *)
rTemp_Scalar1 := MIN(rLaserPower_Max_kW, MAX(rLaserPower_Min_kW, rTemp_Scalar1));

(* -------------------------------------------------------------------------------------------------
   STEP 3.2: INITIALIZE MPC HORIZON TRAJECTORIES (Nc = 3 steps)
   ------------------------------------------------------------------------------------------------- *)
FOR iIndex_Loop1 := 1 TO 3 DO
    arrMPC_U_Horizon[iIndex_Loop1, 1] := rTemp_Scalar1;
    arrMPC_U_Horizon[iIndex_Loop1, 2] := rTemp_Scalar2;
    arrMPC_U_Horizon[iIndex_Loop1, 3] := 0.0;
    arrMPC_U_Horizon[iIndex_Loop1, 4] := 35.0;
END_FOR;

(* -------------------------------------------------------------------------------------------------
   STEP 3.3: UNROLLED PROJECTED GRADIENT DESCENT (PGD) OPTIMIZATION LOOP (3 ITERATIONS)
   ------------------------------------------------------------------------------------------------- *)
FOR iIndex_Loop3 := 1 TO 3 DO
    (* 3.3.1: Forward State Propagation across Prediction Horizon (Np = 5) *)
    (* Step 1 Horizon State (uses u1) *)
    FOR iIndex_Loop1 := 1 TO 8 DO
        arrMPC_X_Horizon[1, iIndex_Loop1] :=
            (arrA_Matrix[iIndex_Loop1, 1] * arrX_State[1]) +
            (arrA_Matrix[iIndex_Loop1, 2] * arrX_State[2]) +
            (arrA_Matrix[iIndex_Loop1, 3] * arrX_State[3]) +
            (arrA_Matrix[iIndex_Loop1, 4] * arrX_State[4]) +
            (arrA_Matrix[iIndex_Loop1, 5] * arrX_State[5]) +
            (arrA_Matrix[iIndex_Loop1, 6] * arrX_State[6]) +
            (arrA_Matrix[iIndex_Loop1, 7] * arrX_State[7]) +
            (arrA_Matrix[iIndex_Loop1, 8] * arrX_State[8]) +
            (arrB_Matrix[iIndex_Loop1, 1] * arrMPC_U_Horizon[1, 1]) +
            (arrB_Matrix[iIndex_Loop1, 2] * arrMPC_U_Horizon[1, 2]) +
            (arrB_Matrix[iIndex_Loop1, 3] * arrMPC_U_Horizon[1, 3]) +
            (arrB_Matrix[iIndex_Loop1, 4] * arrMPC_U_Horizon[1, 4]) +
            (arrEw_Matrix[iIndex_Loop1, 1] * arrW_Disturbance[1]) +
            (arrEw_Matrix[iIndex_Loop1, 2] * arrW_Disturbance[2]) +
            (arrEw_Matrix[iIndex_Loop1, 3] * arrW_Disturbance[3]);
    END_FOR;

    (* Step 2 Horizon State (uses u2) *)
    FOR iIndex_Loop1 := 1 TO 8 DO
        arrMPC_X_Horizon[2, iIndex_Loop1] :=
            (arrA_Matrix[iIndex_Loop1, 1] * arrMPC_X_Horizon[1, 1]) +
            (arrA_Matrix[iIndex_Loop1, 2] * arrMPC_X_Horizon[1, 2]) +
            (arrA_Matrix[iIndex_Loop1, 3] * arrMPC_X_Horizon[1, 3]) +
            (arrA_Matrix[iIndex_Loop1, 4] * arrMPC_X_Horizon[1, 4]) +
            (arrA_Matrix[iIndex_Loop1, 5] * arrMPC_X_Horizon[1, 5]) +
            (arrA_Matrix[iIndex_Loop1, 6] * arrMPC_X_Horizon[1, 6]) +
            (arrA_Matrix[iIndex_Loop1, 7] * arrMPC_X_Horizon[1, 7]) +
            (arrA_Matrix[iIndex_Loop1, 8] * arrMPC_X_Horizon[1, 8]) +
            (arrB_Matrix[iIndex_Loop1, 1] * arrMPC_U_Horizon[2, 1]) +
            (arrB_Matrix[iIndex_Loop1, 2] * arrMPC_U_Horizon[2, 2]) +
            (arrB_Matrix[iIndex_Loop1, 3] * arrMPC_U_Horizon[2, 3]) +
            (arrB_Matrix[iIndex_Loop1, 4] * arrMPC_U_Horizon[2, 4]) +
            (arrEw_Matrix[iIndex_Loop1, 1] * arrW_Disturbance[1]) +
            (arrEw_Matrix[iIndex_Loop1, 2] * arrW_Disturbance[2]) +
            (arrEw_Matrix[iIndex_Loop1, 3] * arrW_Disturbance[3]);
    END_FOR;

    (* Step 3 Horizon State (uses u3) *)
    FOR iIndex_Loop1 := 1 TO 8 DO
        arrMPC_X_Horizon[3, iIndex_Loop1] :=
            (arrA_Matrix[iIndex_Loop1, 1] * arrMPC_X_Horizon[2, 1]) +
            (arrA_Matrix[iIndex_Loop1, 2] * arrMPC_X_Horizon[2, 2]) +
            (arrA_Matrix[iIndex_Loop1, 3] * arrMPC_X_Horizon[2, 3]) +
            (arrA_Matrix[iIndex_Loop1, 4] * arrMPC_X_Horizon[2, 4]) +
            (arrA_Matrix[iIndex_Loop1, 5] * arrMPC_X_Horizon[2, 5]) +
            (arrA_Matrix[iIndex_Loop1, 6] * arrMPC_X_Horizon[2, 6]) +
            (arrA_Matrix[iIndex_Loop1, 7] * arrMPC_X_Horizon[2, 7]) +
            (arrA_Matrix[iIndex_Loop1, 8] * arrMPC_X_Horizon[2, 8]) +
            (arrB_Matrix[iIndex_Loop1, 1] * arrMPC_U_Horizon[3, 1]) +
            (arrB_Matrix[iIndex_Loop1, 2] * arrMPC_U_Horizon[3, 2]) +
            (arrB_Matrix[iIndex_Loop1, 3] * arrMPC_U_Horizon[3, 3]) +
            (arrB_Matrix[iIndex_Loop1, 4] * arrMPC_U_Horizon[3, 4]) +
            (arrEw_Matrix[iIndex_Loop1, 1] * arrW_Disturbance[1]) +
            (arrEw_Matrix[iIndex_Loop1, 2] * arrW_Disturbance[2]) +
            (arrEw_Matrix[iIndex_Loop1, 3] * arrW_Disturbance[3]);
    END_FOR;

    (* Step 4 Horizon State (control frozen at u3) *)
    FOR iIndex_Loop1 := 1 TO 8 DO
        arrMPC_X_Horizon[4, iIndex_Loop1] :=
            (arrA_Matrix[iIndex_Loop1, 1] * arrMPC_X_Horizon[3, 1]) +
            (arrA_Matrix[iIndex_Loop1, 2] * arrMPC_X_Horizon[3, 2]) +
            (arrA_Matrix[iIndex_Loop1, 3] * arrMPC_X_Horizon[3, 3]) +
            (arrA_Matrix[iIndex_Loop1, 4] * arrMPC_X_Horizon[3, 4]) +
            (arrA_Matrix[iIndex_Loop1, 5] * arrMPC_X_Horizon[3, 5]) +
            (arrA_Matrix[iIndex_Loop1, 6] * arrMPC_X_Horizon[3, 6]) +
            (arrA_Matrix[iIndex_Loop1, 7] * arrMPC_X_Horizon[3, 7]) +
            (arrA_Matrix[iIndex_Loop1, 8] * arrMPC_X_Horizon[3, 8]) +
            (arrB_Matrix[iIndex_Loop1, 1] * arrMPC_U_Horizon[3, 1]) +
            (arrB_Matrix[iIndex_Loop1, 2] * arrMPC_U_Horizon[3, 2]) +
            (arrB_Matrix[iIndex_Loop1, 3] * arrMPC_U_Horizon[3, 3]) +
            (arrB_Matrix[iIndex_Loop1, 4] * arrMPC_U_Horizon[3, 4]) +
            (arrEw_Matrix[iIndex_Loop1, 1] * arrW_Disturbance[1]) +
            (arrEw_Matrix[iIndex_Loop1, 2] * arrW_Disturbance[2]) +
            (arrEw_Matrix[iIndex_Loop1, 3] * arrW_Disturbance[3]);
    END_FOR;

    (* Step 5 Horizon State (terminal prediction step) *)
    FOR iIndex_Loop1 := 1 TO 8 DO
        arrMPC_X_Horizon[5, iIndex_Loop1] :=
            (arrA_Matrix[iIndex_Loop1, 1] * arrMPC_X_Horizon[4, 1]) +
            (arrA_Matrix[iIndex_Loop1, 2] * arrMPC_X_Horizon[4, 2]) +
            (arrA_Matrix[iIndex_Loop1, 3] * arrMPC_X_Horizon[4, 3]) +
            (arrA_Matrix[iIndex_Loop1, 4] * arrMPC_X_Horizon[4, 4]) +
            (arrA_Matrix[iIndex_Loop1, 5] * arrMPC_X_Horizon[4, 5]) +
            (arrA_Matrix[iIndex_Loop1, 6] * arrMPC_X_Horizon[4, 6]) +
            (arrA_Matrix[iIndex_Loop1, 7] * arrMPC_X_Horizon[4, 7]) +
            (arrA_Matrix[iIndex_Loop1, 8] * arrMPC_X_Horizon[4, 8]) +
            (arrB_Matrix[iIndex_Loop1, 1] * arrMPC_U_Horizon[3, 1]) +
            (arrB_Matrix[iIndex_Loop1, 2] * arrMPC_U_Horizon[3, 2]) +
            (arrB_Matrix[iIndex_Loop1, 3] * arrMPC_U_Horizon[3, 3]) +
            (arrB_Matrix[iIndex_Loop1, 4] * arrMPC_U_Horizon[3, 4]) +
            (arrEw_Matrix[iIndex_Loop1, 1] * arrW_Disturbance[1]) +
            (arrEw_Matrix[iIndex_Loop1, 2] * arrW_Disturbance[2]) +
            (arrEw_Matrix[iIndex_Loop1, 3] * arrW_Disturbance[3]);
    END_FOR;

    (* 3.3.2: Analytical Cost Gradient Calculation w.r.t Controls (arrMPC_Grad_U) *)
    (* Horizon Step 1 Control Input Gradients *)
    FOR iIndex_Loop2 := 1 TO 4 DO
        (* Control Effort Penalty Gradient: 2 * R * (u - u_ref) *)
        rTemp_SumReal1 := 2.0 * arrR_DiagWeights[iIndex_Loop2] * (arrMPC_U_Horizon[1, iIndex_Loop2] - arrU_Previous[iIndex_Loop2]);

        (* Slew Rate Penalty Gradient: 2 * R_slew * (u[1] - u_prev) - 2 * R_slew * (u[2] - u[1]) *)
        rTemp_SumReal1 := rTemp_SumReal1 + (2.0 * arrR_SlewWeights[iIndex_Loop2] * (arrMPC_U_Horizon[1, iIndex_Loop2] - arrU_Previous[iIndex_Loop2]));
        rTemp_SumReal1 := rTemp_SumReal1 - (2.0 * arrR_SlewWeights[iIndex_Loop2] * (arrMPC_U_Horizon[2, iIndex_Loop2] - arrMPC_U_Horizon[1, iIndex_Loop2]));

        (* State Tracking Error Backpropagation Gradient: sum_m 2 * Q_m * (x_m[1] - x_ref_m) * B_{m, j} *)
        FOR iIndex_Loop1 := 1 TO 8 DO
            rTemp_SumReal1 := rTemp_SumReal1 +
                (2.0 * arrQ_DiagWeights[iIndex_Loop1] * (arrMPC_X_Horizon[1, iIndex_Loop1] - arrX_Reference[iIndex_Loop1]) * arrB_Matrix[iIndex_Loop1, iIndex_Loop2]);
        END_FOR;

        arrMPC_Grad_U[1, iIndex_Loop2] := rTemp_SumReal1;
    END_FOR;

    (* Horizon Step 2 Control Input Gradients *)
    FOR iIndex_Loop2 := 1 TO 4 DO
        rTemp_SumReal1 := 2.0 * arrR_DiagWeights[iIndex_Loop2] * (arrMPC_U_Horizon[2, iIndex_Loop2] - arrU_Previous[iIndex_Loop2]);
        rTemp_SumReal1 := rTemp_SumReal1 + (2.0 * arrR_SlewWeights[iIndex_Loop2] * (arrMPC_U_Horizon[2, iIndex_Loop2] - arrMPC_U_Horizon[1, iIndex_Loop2]));
        rTemp_SumReal1 := rTemp_SumReal1 - (2.0 * arrR_SlewWeights[iIndex_Loop2] * (arrMPC_U_Horizon[3, iIndex_Loop2] - arrMPC_U_Horizon[2, iIndex_Loop2]));

        FOR iIndex_Loop1 := 1 TO 8 DO
            rTemp_SumReal1 := rTemp_SumReal1 +
                (2.0 * arrQ_DiagWeights[iIndex_Loop1] * (arrMPC_X_Horizon[2, iIndex_Loop1] - arrX_Reference[iIndex_Loop1]) * arrB_Matrix[iIndex_Loop1, iIndex_Loop2]);
        END_FOR;

        arrMPC_Grad_U[2, iIndex_Loop2] := rTemp_SumReal1;
    END_FOR;

    (* Horizon Step 3 Control Input Gradients (includes Terminal Cost Backprop) *)
    FOR iIndex_Loop2 := 1 TO 4 DO
        rTemp_SumReal1 := 2.0 * arrR_DiagWeights[iIndex_Loop2] * (arrMPC_U_Horizon[3, iIndex_Loop2] - arrU_Previous[iIndex_Loop2]);
        rTemp_SumReal1 := rTemp_SumReal1 + (2.0 * arrR_SlewWeights[iIndex_Loop2] * (arrMPC_U_Horizon[3, iIndex_Loop2] - arrMPC_U_Horizon[2, iIndex_Loop2]));

        FOR iIndex_Loop1 := 1 TO 8 DO
            rTemp_SumReal1 := rTemp_SumReal1 +
                (2.0 * arrQ_DiagWeights[iIndex_Loop1] * (arrMPC_X_Horizon[3, iIndex_Loop1] - arrX_Reference[iIndex_Loop1]) * arrB_Matrix[iIndex_Loop1, iIndex_Loop2]) +
                (2.0 * arrP_TerminalWeights[iIndex_Loop1] * (arrMPC_X_Horizon[5, iIndex_Loop1] - arrX_Reference[iIndex_Loop1]) * arrB_Matrix[iIndex_Loop1, iIndex_Loop2]);
        END_FOR;

        arrMPC_Grad_U[3, iIndex_Loop2] := rTemp_SumReal1;
    END_FOR;

    (* 3.3.3: Gradient Descent Update Step: u := u - alpha * Grad_U *)
    FOR iIndex_Loop1 := 1 TO 3 DO
        FOR iIndex_Loop2 := 1 TO 4 DO
            arrMPC_U_Horizon[iIndex_Loop1, iIndex_Loop2] :=
                arrMPC_U_Horizon[iIndex_Loop1, iIndex_Loop2] - (rPGD_StepSize * arrMPC_Grad_U[iIndex_Loop1, iIndex_Loop2]);
        END_FOR;
    END_FOR;

    (* 3.3.4: Box Constraint Projections *)
    FOR iIndex_Loop1 := 1 TO 3 DO
        (* Input 1: Laser Power Clamping [kW] *)
        arrMPC_U_Horizon[iIndex_Loop1, 1] := MIN(rLaserPower_Max_kW, MAX(rLaserPower_Min_kW, arrMPC_U_Horizon[iIndex_Loop1, 1]));

        (* Input 2: Wobble Frequency Clamping [Hz] *)
        arrMPC_U_Horizon[iIndex_Loop1, 2] := MIN(rWobbleFreq_Max_Hz, MAX(rWobbleFreq_Min_Hz, arrMPC_U_Horizon[iIndex_Loop1, 2]));

        (* Input 3: Chuck Torque Clamping [Nm] *)
        arrMPC_U_Horizon[iIndex_Loop1, 3] := MIN(25.0, MAX(-25.0, arrMPC_U_Horizon[iIndex_Loop1, 3]));

        (* Input 4: Shielding Gas Flow Clamping [L/min] *)
        arrMPC_U_Horizon[iIndex_Loop1, 4] := MIN(rGasFlow_Max_Lmin, MAX(rGasFlow_Min_Lmin, arrMPC_U_Horizon[iIndex_Loop1, 4]));
    END_FOR;
END_FOR;

(* -------------------------------------------------------------------------------------------------
   STEP 3.4: SLEW RATE LIMITER & ACTUATOR COMMAND COMMIT
   ------------------------------------------------------------------------------------------------- *)
(* Select First Horizon Step u[1] as the Active Control Command *)
arrU_Optimal[1] := arrMPC_U_Horizon[1, 1];
arrU_Optimal[2] := arrMPC_U_Horizon[1, 2];
arrU_Optimal[3] := arrMPC_U_Horizon[1, 3];
arrU_Optimal[4] := arrMPC_U_Horizon[1, 4];

(* Apply Hardware Slew Rate Limiters (Power max slew: 350.0 kW/s, Wobble max slew: 2500.0 Hz/s) *)
rTemp_Scalar1 := 350.0 * rScanTime_s; (* 0.70 kW per 2 ms scan *)
IF (arrU_Optimal[1] - arrU_Previous[1]) > rTemp_Scalar1 THEN
    arrU_Optimal[1] := arrU_Previous[1] + rTemp_Scalar1;
ELSIF (arrU_Previous[1] - arrU_Optimal[1]) > rTemp_Scalar1 THEN
    arrU_Optimal[1] := arrU_Previous[1] - rTemp_Scalar1;
END_IF;

rTemp_Scalar2 := 2500.0 * rScanTime_s; (* 5.0 Hz per 2 ms scan *)
IF (arrU_Optimal[2] - arrU_Previous[2]) > rTemp_Scalar2 THEN
    arrU_Optimal[2] := arrU_Previous[2] + rTemp_Scalar2;
ELSIF (arrU_Previous[2] - arrU_Optimal[2]) > rTemp_Scalar2 THEN
    arrU_Optimal[2] := arrU_Previous[2] - rTemp_Scalar2;
END_IF;

(* Inhibit Laser Power Output if Dry Run Mode or Emission Enable Flag False *)
IF bDryRunMode OR (NOT bLaserEmission_Enable) OR (iFSM_CurrentState <> 6) THEN
    arrU_Optimal[1] := 0.0;
END_IF;

(* Commit Physical Actuator Output Commands *)
rLaserPower_Cmd_kW       := arrU_Optimal[1];
rLaserWobble_Freq_Cmd_Hz := arrU_Optimal[2];
rShieldGas_Flow_Cmd_Lmin := arrU_Optimal[4];
rLaserWobble_Amp_Cmd_mm  := MIN(rWobbleAmp_Max_mm, MAX(rWobbleAmp_Min_mm, rWeldWobbleAmp_mm));

(* Store Previous Scan Actuator History for Slew Calculation *)
FOR iIndex_Loop2 := 1 TO 4 DO
    arrU_SlewRate[iIndex_Loop2] := (arrU_Optimal[iIndex_Loop2] - arrU_Previous[iIndex_Loop2]) / rScanTime_s;
    arrU_Previous[iIndex_Loop2] := arrU_Optimal[iIndex_Loop2];
END_FOR;
"""
