# mine_vod_fan_builder/st_phase4_mpc.py

def get_phase4_mpc():
    return """(* ==================================================================================================== *)
(* PHASE 4: RECEDING-HORIZON MPC VIA 10 UNROLLED PROJECTED GRADIENT DESCENT (PGD) ITERATIONS            *)
(* ==================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------- *)
(* SUB-PHASE 4.1: Dynamic Operational Target State Trajectory Synthesis                                 *)
(* ---------------------------------------------------------------------------------------------------- *)
arrX_target[1] := 3.8;  (* Nominal Surface Fan Differential Pressure Target [kPa] *)
arrX_target[2] := 295.0; (* Nominal Subterranean Mass Flow Target [kg/s] *)
arrX_target[3] := 32.5; (* Nominal Aerodynamic Stall Margin Target [%] *)
arrX_target[4] := 35.0; (* Nominal Dynamic Blade Tip Turbulence Target [Pa RMS] *)
arrX_target[5] := 10.0; (* Nominal Heading Toxic Gas Residual Target [ppm] *)
arrX_target[6] := 30.0; (* Nominal Shaft Bottom Barometric Differential Target [kPa] *)

(* Mode-Adaptive Target Adjustments *)
IF bPostBlastPurgeRequest OR (iActiveBlastingZoneIndex > 0) THEN
    arrX_target[2] := 420.0; (* High-Volume Blast Clearance Purge Mass Flow Target [kg/s] *)
    arrX_target[5] := 5.0;   (* Deep Fume Evacuation Target [ppm] *)
    arrX_target[1] := 4.6;   (* Compensating Static Pressure Rise [kPa] *)
ELSIF bDieselHaulageBoostRequest THEN
    arrX_target[2] := 365.0; (* Heavy Diesel Fleet Airflow Compensation [kg/s] *)
    arrX_target[5] := 15.0;
END_IF;

IF bFireSmokeEmergencyTrip THEN
    arrX_target[2] := 380.0; (* Smoke Reversal Prevention High-Velocity Intake Target [kg/s] *)
    arrX_target[3] := 25.0;  (* Controlled Stall Safety during Emergency Evacuation *)
END_IF;

(* Initialize Optimization Vector with Previous Cycle Control *)
FOR iLoopIdx := 1 TO 6 DO
    arrU_opt[iLoopIdx] := arrU_prev[iLoopIdx];
END_FOR;

(* ---------------------------------------------------------------------------------------------------- *)
(* SUB-PHASE 4.2: 10 Unrolled Receding-Horizon Projected Gradient Descent Iterations                    *)
(* ---------------------------------------------------------------------------------------------------- *)
FOR kPGD_Iter := 1 TO 10 DO
    (* 1. Compute State Prediction Tracking Errors from Current Optimization Candidate *)
    FOR iLoopIdx := 1 TO 6 DO
        rTempSum := 0.0;
        FOR jLoopIdx := 1 TO 6 DO
            rTempSum := rTempSum + (arrA[iLoopIdx, jLoopIdx] * arrX_hat[jLoopIdx]) + (arrB[iLoopIdx, jLoopIdx] * arrU_opt[jLoopIdx]);
        END_FOR;
        arrY_err[iLoopIdx] := rTempSum - arrX_target[iLoopIdx];
    END_FOR;

    (* 2. Backpropagate Tracking Gradient via Transpose Input Matrix B^T * Q * Error *)
    FOR iLoopIdx := 1 TO 6 DO
        rTempSum := 0.0;
        FOR jLoopIdx := 1 TO 6 DO
            rTempSum := rTempSum + (arrB[jLoopIdx, iLoopIdx] * arrQ_weights[jLoopIdx] * arrY_err[jLoopIdx]);
        END_FOR;
        (* Add Actuator Control Energy Penalty Term R * u *)
        rTempSum := rTempSum + (arrR_weights[iLoopIdx] * arrU_opt[iLoopIdx]);
        (* Add Actuator Slew Rate Smoothness Penalty Term S * (u - u_prev) *)
        rTempSum := rTempSum + (arrS_weights[iLoopIdx] * (arrU_opt[iLoopIdx] - arrU_prev[iLoopIdx]));
        arrGrad[iLoopIdx] := rTempSum;
    END_FOR;

    (* 3. Non-Linear Aerodynamic Anti-Stall Safety Barrier Potential Gradient *)
    IF arrX_hat[3] < 22.0 THEN
        rTempDelta := 22.0 - arrX_hat[3];
        IF rTempDelta > 15.0 THEN rTempDelta := 15.0; END_IF;
        (* Severe stall risk: pitch relief (reduce pitch), fan speed boost (increase RPM), open louvers *)
        arrGrad_AntiStall[1] := rAntiStallBarrierWeight * rTempDelta * 0.45; (* Positive gradient pushes pitch down *)
        arrGrad_AntiStall[2] := -rAntiStallBarrierWeight * rTempDelta * 0.85; (* Negative gradient boosts RPM up *)
        arrGrad_AntiStall[3] := -rAntiStallBarrierWeight * rTempDelta * 0.65; (* Negative gradient forces louvers open *)
    ELSE
        arrGrad_AntiStall[1] := 0.0;
        arrGrad_AntiStall[2] := 0.0;
        arrGrad_AntiStall[3] := 0.0;
    END_IF;
    arrGrad_AntiStall[4] := 0.0;
    arrGrad_AntiStall[5] := 0.0;
    arrGrad_AntiStall[6] := 0.0;

    (* 4. Critical Smoke Backlayering Reversal Prevention Barrier Gradient *)
    IF bSmokeReversalLockEngaged THEN
        arrGrad_SmokeLock[1] := -rSmokeLockBarrierWeight * 0.35; (* Increase pitch to push mass flow *)
        arrGrad_SmokeLock[2] := -rSmokeLockBarrierWeight * 0.75; (* Increase VFD RPM *)
        arrGrad_SmokeLock[3] := -rSmokeLockBarrierWeight * 0.50; (* Open louvers to clear airway smoke path *)
    ELSE
        arrGrad_SmokeLock[1] := 0.0;
        arrGrad_SmokeLock[2] := 0.0;
        arrGrad_SmokeLock[3] := 0.0;
    END_IF;
    arrGrad_SmokeLock[4] := 0.0;
    arrGrad_SmokeLock[5] := 0.0;
    arrGrad_SmokeLock[6] := 0.0;

    (* 5. Gradient Descent Step: u_cand = u - step * (Grad + Grad_Stall + Grad_Smoke) *)
    FOR iLoopIdx := 1 TO 6 DO
        arrU_opt[iLoopIdx] := arrU_opt[iLoopIdx] - (rPGD_StepSize * (arrGrad[iLoopIdx] + arrGrad_AntiStall[iLoopIdx] + arrGrad_SmokeLock[iLoopIdx]));
    END_FOR;

    (* 6. Actuator Slew Rate Slew Constraints Projection *)
    FOR iLoopIdx := 1 TO 6 DO
        IF (arrU_opt[iLoopIdx] - arrU_prev[iLoopIdx]) > arrDeltaU_max[iLoopIdx] THEN
            arrU_opt[iLoopIdx] := arrU_prev[iLoopIdx] + arrDeltaU_max[iLoopIdx];
        ELSIF (arrU_opt[iLoopIdx] - arrU_prev[iLoopIdx]) < -arrDeltaU_max[iLoopIdx] THEN
            arrU_opt[iLoopIdx] := arrU_prev[iLoopIdx] - arrDeltaU_max[iLoopIdx];
        END_IF;
    END_FOR;

    (* 7. Physical Box Saturation Bounds Projection *)
    FOR iLoopIdx := 1 TO 6 DO
        IF arrU_opt[iLoopIdx] < arrU_min[iLoopIdx] THEN
            arrU_opt[iLoopIdx] := arrU_min[iLoopIdx];
        ELSIF arrU_opt[iLoopIdx] > arrU_max[iLoopIdx] THEN
            arrU_opt[iLoopIdx] := arrU_max[iLoopIdx];
        END_IF;
    END_FOR;
END_FOR;

(* Store Solution for Slew Tracking in Next Scan *)
FOR iLoopIdx := 1 TO 6 DO
    arrU_prev[iLoopIdx] := arrU_opt[iLoopIdx];
END_FOR;

(* ---------------------------------------------------------------------------------------------------- *)
(* SUB-PHASE 4.3: Surface Fan Substation Actuator Command Distribution                                  *)
(* ---------------------------------------------------------------------------------------------------- *)
IF bDualFanParallelMode THEN
    (* Dual 3.5 MW Fan Parallel Operation (50/50 Load Share) *)
    rFan1_BladePitchCmd_deg := arrU_opt[1];
    rFan1_VFD_SpeedCmd_RPM := arrU_opt[2];
    rFan2_BladePitchCmd_deg := arrU_opt[1];
    rFan2_VFD_SpeedCmd_RPM := arrU_opt[2];
ELSE
    (* Lead/Lag Duty Rotation Mode *)
    IF bLeadFanSelect THEN
        (* Fan 2 is Lead, Fan 1 is Idle Standby *)
        rFan2_BladePitchCmd_deg := arrU_opt[1];
        rFan2_VFD_SpeedCmd_RPM := arrU_opt[2];
        rFan1_BladePitchCmd_deg := -12.0; (* Feathered *)
        rFan1_VFD_SpeedCmd_RPM := 0.0;
    ELSE
        (* Fan 1 is Lead, Fan 2 is Idle Standby *)
        rFan1_BladePitchCmd_deg := arrU_opt[1];
        rFan1_VFD_SpeedCmd_RPM := arrU_opt[2];
        rFan2_BladePitchCmd_deg := -12.0; (* Feathered *)
        rFan2_VFD_SpeedCmd_RPM := 0.0;
    END_IF;
END_IF;

(* Surface Intake Collar Thermal Freeze Protection Valve Command *)
IF bIcePreventionEnable AND (rSurfaceAirTemp_degC < 3.0) THEN
    (* Modulate coil heating valve to prevent shaft icing (freeze risk below 0 deg C) *)
    rTempDelta := (3.0 - rSurfaceAirTemp_degC) * 22.5;
    IF rTempDelta > 100.0 THEN rTempDelta := 100.0; END_IF;
    rIntakeCollarHeaterValveCmd_pct := rTempDelta;
ELSE
    rIntakeCollarHeaterValveCmd_pct := arrU_opt[5];
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* SUB-PHASE 4.4: 24 Underground Automated Branch Louvers Closed-Loop Distribution                      *)
(* Balances dynamic regulatory airflow demand, diesel fleet distribution, blast purge and fire locks    *)
(* ---------------------------------------------------------------------------------------------------- *)
FOR iLoopIdx := 1 TO 24 DO
    (* Calculate Dynamic Branch Airflow Demand from Active Diesel Engine Power (0.06 m3/s per kW) *)
    rTempSum := arrBranchRegulatoryFlowMin_m3s[iLoopIdx] + (arrZoneDieselFleet_kW[iLoopIdx] * rDieselAirflowRequirement_m3s_kW);

    (* Priority Override 1: Active Post-Blast Purge Heading Priority Boost *)
    IF arrZoneBlastActive[iLoopIdx] OR (iActiveBlastingZoneIndex = iLoopIdx) THEN
        rTempSum := rTempSum * 2.25; (* 225% Airflow Boost for Fast Toxic Gas Clearance *)
    END_IF;

    (* Priority Override 2: Fire Smoke Reversal Prevention Isolation *)
    IF arrZoneFireAlarm[iLoopIdx] OR (iFireZoneIndex = iLoopIdx) THEN
        (* If fire detected in this heading, seal louver to 10% to starve fire of fresh oxygen *)
        rTempSum := 4.5;
    END_IF;

    (* Calculate Real-Time Volumetric Airflow Delivered to Branch [m3/s] *)
    arrZoneAirflowDelivery_m3s[iLoopIdx] := arrZoneVelocity_mps[iLoopIdx] * arrBranchCrossSection_m2[iLoopIdx];

    (* Calculate Flow Deficit *)
    arrZoneAirflowDeficit_m3s[iLoopIdx] := rTempSum - arrZoneAirflowDelivery_m3s[iLoopIdx];

    (* Proportional-Integral Branch Louver Damper Command Synthesis *)
    rTempDelta := arrLouverPosFeedback_pct[iLoopIdx] + (arrZoneAirflowDeficit_m3s[iLoopIdx] * 2.85);

    (* Apply Base Optimizer Modulation Bias from arrU_opt[3] *)
    rTempDelta := rTempDelta + (0.15 * (arrU_opt[3] - 50.0));

    (* Fire Smoke Damper Interlock Override *)
    IF arrZoneFireAlarm[iLoopIdx] OR (iFireZoneIndex = iLoopIdx) THEN
        rTempDelta := 10.0; (* Choke to 10% containment position *)
    END_IF;

    (* Clamp Branch Louver Command [5% to 100%] to prevent complete deadhead *)
    IF rTempDelta < 5.0 THEN
        rTempDelta := 5.0;
    ELSIF rTempDelta > 100.0 THEN
        rTempDelta := 100.0;
    END_IF;
    arrLouverCmd_pct[iLoopIdx] := rTempDelta;

    (* Heading Auxiliary Booster Fan Command Synthesis *)
    IF arrZoneBlastActive[iLoopIdx] OR (iActiveBlastingZoneIndex = iLoopIdx) THEN
        arrAuxBoosterFanCmd_pct[iLoopIdx] := 100.0; (* Full speed auxiliary booster purge *)
    ELSIF arrZoneDieselFleet_kW[iLoopIdx] > 250.0 THEN
        arrAuxBoosterFanCmd_pct[iLoopIdx] := 75.0 + (arrZoneDieselFleet_kW[iLoopIdx] * 0.035);
        IF arrAuxBoosterFanCmd_pct[iLoopIdx] > 100.0 THEN arrAuxBoosterFanCmd_pct[iLoopIdx] := 100.0; END_IF;
    ELSIF arrZoneFireAlarm[iLoopIdx] OR (iFireZoneIndex = iLoopIdx) THEN
        arrAuxBoosterFanCmd_pct[iLoopIdx] := 0.0; (* Trip booster in fire heading to halt smoke spread *)
    ELSE
        arrAuxBoosterFanCmd_pct[iLoopIdx] := 35.0; (* Baseline heading sweep *)
    END_IF;

    (* Check Personnel Evacuation Requirement for Excessive Gas Levels *)
    IF (arrZoneCO_ppm[iLoopIdx] > rCO_Trip_HH) OR (arrZoneNO2_ppm[iLoopIdx] > rNO2_SafeReentryLimit_ppm * 2.0) THEN
        arrZoneEvacuationRequired[iLoopIdx] := TRUE;
    ELSE
        IF (arrZoneCO_ppm[iLoopIdx] < rCO_Warn_H) AND (arrZoneNO2_ppm[iLoopIdx] < rNO2_SafeReentryLimit_ppm) THEN
            arrZoneEvacuationRequired[iLoopIdx] := FALSE;
        END_IF;
    END_IF;
END_FOR;
"""
