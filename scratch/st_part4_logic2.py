# -*- coding: utf-8 -*-

part4_logic2 = """(* ================================================================================================= *)
(* === PHASE 3: RECEDING-HORIZON MPC OPTIMIZATION & JERK-LIMITED S-CURVE MOTION PROFILING        === *)
(* ================================================================================================= *)

(* --- 3.1 7-PHASE JERK-LIMITED S-CURVE KINEMATIC TRAJECTORY GENERATOR --- *)
IF bSCurveProfileActive THEN
    rSCurveElapsedTimer_s := rSCurveElapsedTimer_s + c_rScanTime_Ts;
    rSCurveTraveledDist_mm := ABS(rVotedHoistPosition_mm - rSCurveStartPos_mm);
    rScratch1 := ABS(rSCurveTargetDistance_mm - rVotedHoistPosition_mm);

    CASE iSCurvePhase OF
        1: (* PHASE 1: CONCAVE POSITIVE JERK (ACCELERATION RAMP-UP) *)
            rProfileCurrentAccel_m_s2 := rProfileCurrentAccel_m_s2 + (c_rHoistMaxJerk_m_s3 * c_rScanTime_Ts);
            IF rProfileCurrentAccel_m_s2 >= c_rHoistMaxAccel_m_s2 THEN
                rProfileCurrentAccel_m_s2 := c_rHoistMaxAccel_m_s2;
                iSCurvePhase := 2;
            END_IF;
            rProfileCurrentVel_m_s := rProfileCurrentVel_m_s + (rProfileCurrentAccel_m_s2 * c_rScanTime_Ts);

        2: (* PHASE 2: CONSTANT MAXIMUM ACCELERATION *)
            rProfileCurrentVel_m_s := rProfileCurrentVel_m_s + (c_rHoistMaxAccel_m_s2 * c_rScanTime_Ts);
            (* Check if approaching cruise speed transition *)
            IF rProfileCurrentVel_m_s >= (c_rHoistMaxSpeed_m_s - (0.50 * c_rHoistMaxAccel_m_s2 * (c_rHoistMaxAccel_m_s2 / c_rHoistMaxJerk_m_s3))) THEN
                iSCurvePhase := 3;
            END_IF;

        3: (* PHASE 3: CONVEX NEGATIVE JERK (ACCELERATION RAMP-DOWN TO CRUISE) *)
            rProfileCurrentAccel_m_s2 := rProfileCurrentAccel_m_s2 - (c_rHoistMaxJerk_m_s3 * c_rScanTime_Ts);
            IF rProfileCurrentAccel_m_s2 <= 0.0 THEN
                rProfileCurrentAccel_m_s2 := 0.0;
                rProfileCurrentVel_m_s := c_rHoistMaxSpeed_m_s;
                iSCurvePhase := 4;
            END_IF;
            rProfileCurrentVel_m_s := rProfileCurrentVel_m_s + (rProfileCurrentAccel_m_s2 * c_rScanTime_Ts);

        4: (* PHASE 4: CONSTANT CRUISE VELOCITY *)
            rProfileCurrentAccel_m_s2 := 0.0;
            rProfileCurrentVel_m_s := c_rHoistMaxSpeed_m_s;
            (* Braking distance calculation: s_brake = v^2 / (2 * a) + transition buffer *)
            rScratch2 := ((c_rHoistMaxSpeed_m_s * c_rHoistMaxSpeed_m_s) / (2.0 * c_rHoistMaxAccel_m_s2)) * 1000.0 + 800.0;
            IF rScratch1 <= rScratch2 THEN
                iSCurvePhase := 5;
            END_IF;

        5: (* PHASE 5: CONCAVE NEGATIVE JERK (DECELERATION RAMP-UP) *)
            rProfileCurrentAccel_m_s2 := rProfileCurrentAccel_m_s2 - (c_rHoistMaxJerk_m_s3 * c_rScanTime_Ts);
            IF rProfileCurrentAccel_m_s2 <= -c_rHoistMaxAccel_m_s2 THEN
                rProfileCurrentAccel_m_s2 := -c_rHoistMaxAccel_m_s2;
                iSCurvePhase := 6;
            END_IF;
            rProfileCurrentVel_m_s := rProfileCurrentVel_m_s + (rProfileCurrentAccel_m_s2 * c_rScanTime_Ts);

        6: (* PHASE 6: CONSTANT MAXIMUM DECELERATION *)
            rProfileCurrentVel_m_s := rProfileCurrentVel_m_s + (-c_rHoistMaxAccel_m_s2 * c_rScanTime_Ts);
            IF rProfileCurrentVel_m_s <= c_rHoistLevelingSpeed_m_s THEN
                rProfileCurrentVel_m_s := c_rHoistLevelingSpeed_m_s;
                rProfileCurrentAccel_m_s2 := 0.0;
                iSCurvePhase := 7;
            END_IF;

        7: (* PHASE 7: SUB-MILLIMETER LEVELING CREEP APPROACH *)
            rProfileCurrentAccel_m_s2 := 0.0;
            rProfileCurrentVel_m_s := c_rHoistLevelingSpeed_m_s;
            
            (* Check sub-millimeter floor alignment window *)
            IF rScratch1 <= c_rFloorLevelTolerance_mm THEN
                rProfileCurrentVel_m_s := 0.0;
                rSubMillimeterCreepTimer_s := rSubMillimeterCreepTimer_s + c_rScanTime_Ts;
                IF rSubMillimeterCreepTimer_s >= 0.150 THEN
                    bFloorAlignedSubMillimeter := TRUE;
                    bSCurveProfileCompleted := TRUE;
                    bSCurveProfileActive := FALSE;
                    iSCurvePhase := 0;
                END_IF;
            ELSE
                rSubMillimeterCreepTimer_s := 0.0;
                bFloorAlignedSubMillimeter := FALSE;
            END_IF;
    END_CASE;

    (* Position Integration along Trajectory Direction *)
    IF rSCurveTargetDistance_mm >= rSCurveStartPos_mm THEN
        rRef_HoistVel_mm_s := rProfileCurrentVel_m_s * 1000.0;
        rProfileCurrentPos_mm := rProfileCurrentPos_mm + (rRef_HoistVel_mm_s * c_rScanTime_Ts);
    ELSE
        rRef_HoistVel_mm_s := -rProfileCurrentVel_m_s * 1000.0;
        rProfileCurrentPos_mm := rProfileCurrentPos_mm + (rRef_HoistVel_mm_s * c_rScanTime_Ts);
    END_IF;

    rRef_HoistPos_mm := rProfileCurrentPos_mm;
    rHoistVelocitySetpoint_m_s := rProfileCurrentVel_m_s;
ELSE
    rProfileCurrentVel_m_s := 0.0;
    rProfileCurrentAccel_m_s2 := 0.0;
    rRef_HoistVel_mm_s := 0.0;
    rHoistVelocitySetpoint_m_s := 0.0;
END_IF;

rHoistFloorLevelingError_mm := rVotedHoistPosition_mm - aFloorElevations_mm[iTargetLevelNumber];

(* --- 3.2 HORIZONTAL SHUTTLE AISLE MOTION PROFILER --- *)
IF bShuttleProfileActive THEN
    rScratch1 := ABS(rShuttleTargetDist_mm - rVotedShuttlePosition_mm);
    IF rScratch1 > c_rShuttleDockTolerance_mm THEN
        IF rShuttleTargetDist_mm > rVotedShuttlePosition_mm THEN
            rShuttleProfileVel_m_s := c_rShuttleMaxSpeed_m_s;
            rShuttleProfilePos_mm := rShuttleProfilePos_mm + (rShuttleProfileVel_m_s * 1000.0 * c_rScanTime_Ts);
        ELSE
            rShuttleProfileVel_m_s := -c_rShuttleMaxSpeed_m_s;
            rShuttleProfilePos_mm := rShuttleProfilePos_mm + (rShuttleProfileVel_m_s * 1000.0 * c_rScanTime_Ts);
        END_IF;
        bShuttleProfileCompleted := FALSE;
    ELSE
        rShuttleProfileVel_m_s := 0.0;
        bShuttleProfileCompleted := TRUE;
        bShuttleProfileActive := FALSE;
    END_IF;
    rRef_ShuttlePos_mm := rShuttleProfilePos_mm;
    rRef_ShuttleVel_mm_s := rShuttleProfileVel_m_s * 1000.0;
    rShuttleVelocitySetpoint_m_s := rShuttleProfileVel_m_s;
ELSE
    rShuttleProfileVel_m_s := 0.0;
    rShuttleVelocitySetpoint_m_s := 0.0;
END_IF;

(* --- 3.3 MPC QUADRATIC COST GRADIENT & HESSIAN EVALUATION --- *)
(* Analytical Gradient Elements g = Bd'*Q*(x_pred - x_ref) + R*u_prev + Rd*Delta_u *)
rGrad1_HoistTorque := (Bd_11 * rMPC_Q1_HoistPos * (x1_Pred - 0.0)) +
                      (Bd_21 * rMPC_Q2_HoistVel * (x2_Pred - 0.0)) +
                      (Bd_31 * rMPC_Q3_CableStretch * (x3_Pred - 0.0)) +
                      (Bd_41 * rMPC_Q4_CableRate * (x4_Pred - 0.0)) +
                      (Bd_51 * rMPC_Q5_ShuttlePos * (x5_Pred - 0.0)) +
                      (Bd_61 * rMPC_Q6_ShuttleVel * (x6_Pred - 0.0)) +
                      (Bd_71 * rMPC_Q7_Torque * (x7_Pred - 0.0)) +
                      (Bd_81 * rMPC_Q8_DCLink * (x8_Pred - 0.0)) +
                      (rMPC_R1_HoistTorque * rPrev_u1_HoistTorque) +
                      (rMPC_Rd1_dHoistTorque * rPrevDelta_u1);

rGrad2_ShuttleServo := (Bd_12 * rMPC_Q1_HoistPos * (x1_Pred - 0.0)) +
                       (Bd_22 * rMPC_Q2_HoistVel * (x2_Pred - 0.0)) +
                       (Bd_32 * rMPC_Q3_CableStretch * (x3_Pred - 0.0)) +
                       (Bd_42 * rMPC_Q4_CableRate * (x4_Pred - 0.0)) +
                       (Bd_52 * rMPC_Q5_ShuttlePos * (x5_Pred - 0.0)) +
                       (Bd_62 * rMPC_Q6_ShuttleVel * (x6_Pred - 0.0)) +
                       (Bd_72 * rMPC_Q7_Torque * (x7_Pred - 0.0)) +
                       (Bd_82 * rMPC_Q8_DCLink * (x8_Pred - 0.0)) +
                       (rMPC_R2_ShuttleServo * rPrev_u2_ShuttleServo) +
                       (rMPC_Rd2_dShuttleServo * rPrevDelta_u2);

rGrad3_VibrationDamp := (Bd_13 * rMPC_Q1_HoistPos * (x1_Pred - 0.0)) +
                        (Bd_23 * rMPC_Q2_HoistVel * (x2_Pred - 0.0)) +
                        (Bd_33 * rMPC_Q3_CableStretch * (x3_Pred - 0.0)) +
                        (Bd_43 * rMPC_Q4_CableRate * (x4_Pred - 0.0)) +
                        (Bd_53 * rMPC_Q5_ShuttlePos * (x5_Pred - 0.0)) +
                        (Bd_63 * rMPC_Q6_ShuttleVel * (x6_Pred - 0.0)) +
                        (Bd_73 * rMPC_Q7_Torque * (x7_Pred - 0.0)) +
                        (Bd_83 * rMPC_Q8_DCLink * (x8_Pred - 0.0)) +
                        (rMPC_R3_VibrationDamp * rPrev_u3_VibrationDamp) +
                        (rMPC_Rd3_dVibrationDamp * rPrevDelta_u3);

rGrad4_RegenChopper := (Bd_14 * rMPC_Q1_HoistPos * (x1_Pred - 0.0)) +
                       (Bd_24 * rMPC_Q2_HoistVel * (x2_Pred - 0.0)) +
                       (Bd_34 * rMPC_Q3_CableStretch * (x3_Pred - 0.0)) +
                       (Bd_44 * rMPC_Q4_CableRate * (x4_Pred - 0.0)) +
                       (Bd_54 * rMPC_Q5_ShuttlePos * (x5_Pred - 0.0)) +
                       (Bd_64 * rMPC_Q6_ShuttleVel * (x6_Pred - 0.0)) +
                       (Bd_74 * rMPC_Q7_Torque * (x7_Pred - 0.0)) +
                       (Bd_84 * rMPC_Q8_DCLink * (x8_Pred - 0.0)) +
                       (rMPC_R4_RegenChopper * rPrev_u4_RegenChopper) +
                       (rMPC_Rd4_dRegenChopper * rPrevDelta_u4);

(* Analytical Diagonal Hessian Elements H_ii = sum(Bd_ji^2 * Q_j) + R_i + Rd_i *)
rHess11_HoistTorque := (Bd_11 * Bd_11 * rMPC_Q1_HoistPos) + (Bd_21 * Bd_21 * rMPC_Q2_HoistVel) +
                       (Bd_31 * Bd_31 * rMPC_Q3_CableStretch) + (Bd_41 * Bd_41 * rMPC_Q4_CableRate) +
                       (Bd_51 * Bd_51 * rMPC_Q5_ShuttlePos) + (Bd_61 * Bd_61 * rMPC_Q6_ShuttleVel) +
                       (Bd_71 * Bd_71 * rMPC_Q7_Torque) + (Bd_81 * Bd_81 * rMPC_Q8_DCLink) +
                       rMPC_R1_HoistTorque + rMPC_Rd1_dHoistTorque;

rHess22_ShuttleServo := (Bd_12 * Bd_12 * rMPC_Q1_HoistPos) + (Bd_22 * Bd_22 * rMPC_Q2_HoistVel) +
                        (Bd_32 * Bd_32 * rMPC_Q3_CableStretch) + (Bd_42 * Bd_42 * rMPC_Q4_CableRate) +
                        (Bd_52 * Bd_52 * rMPC_Q5_ShuttlePos) + (Bd_62 * Bd_62 * rMPC_Q6_ShuttleVel) +
                        (Bd_72 * Bd_72 * rMPC_Q7_Torque) + (Bd_82 * Bd_82 * rMPC_Q8_DCLink) +
                        rMPC_R2_ShuttleServo + rMPC_Rd2_dShuttleServo;

rHess33_VibrationDamp := (Bd_13 * Bd_13 * rMPC_Q1_HoistPos) + (Bd_23 * Bd_23 * rMPC_Q2_HoistVel) +
                         (Bd_33 * Bd_33 * rMPC_Q3_CableStretch) + (Bd_43 * Bd_43 * rMPC_Q4_CableRate) +
                         (Bd_53 * Bd_53 * rMPC_Q5_ShuttlePos) + (Bd_63 * Bd_63 * rMPC_Q6_ShuttleVel) +
                         (Bd_73 * Bd_73 * rMPC_Q7_Torque) + (Bd_83 * Bd_83 * rMPC_Q8_DCLink) +
                         rMPC_R3_VibrationDamp + rMPC_Rd3_dVibrationDamp;

rHess44_RegenChopper := (Bd_14 * Bd_14 * rMPC_Q1_HoistPos) + (Bd_24 * Bd_24 * rMPC_Q2_HoistVel) +
                        (Bd_34 * Bd_34 * rMPC_Q3_CableStretch) + (Bd_44 * Bd_44 * rMPC_Q4_CableRate) +
                        (Bd_54 * Bd_54 * rMPC_Q5_ShuttlePos) + (Bd_64 * Bd_64 * rMPC_Q6_ShuttleVel) +
                        (Bd_74 * Bd_74 * rMPC_Q7_Torque) + (Bd_84 * Bd_84 * rMPC_Q8_DCLink) +
                        rMPC_R4_RegenChopper + rMPC_Rd4_dRegenChopper;

(* Prevent divide by zero in Hessians *)
IF rHess11_HoistTorque < 0.10 THEN rHess11_HoistTorque := 0.10; END_IF;
IF rHess22_ShuttleServo < 0.10 THEN rHess22_ShuttleServo := 0.10; END_IF;
IF rHess33_VibrationDamp < 0.10 THEN rHess33_VibrationDamp := 0.10; END_IF;
IF rHess44_RegenChopper < 0.10 THEN rHess44_RegenChopper := 0.10; END_IF;

(* Optimal Step Updates: Delta_u = - (g / H) *)
rDelta_u1_HoistTorque := - (rGrad1_HoistTorque / rHess11_HoistTorque);
rDelta_u2_ShuttleServo := - (rGrad2_ShuttleServo / rHess22_ShuttleServo);
rDelta_u3_VibrationDamp := - (rGrad3_VibrationDamp / rHess33_VibrationDamp);
rDelta_u4_RegenChopper := - (rGrad4_RegenChopper / rHess44_RegenChopper);

(* Apply Slew Rate Limiting on Control Changes *)
IF rDelta_u1_HoistTorque > 150.0 THEN rDelta_u1_HoistTorque := 150.0;
ELSIF rDelta_u1_HoistTorque < -150.0 THEN rDelta_u1_HoistTorque := -150.0; END_IF;

IF rDelta_u2_ShuttleServo > 45.0 THEN rDelta_u2_ShuttleServo := 45.0;
ELSIF rDelta_u2_ShuttleServo < -45.0 THEN rDelta_u2_ShuttleServo := -45.0; END_IF;

IF rDelta_u3_VibrationDamp > 60.0 THEN rDelta_u3_VibrationDamp := 60.0;
ELSIF rDelta_u3_VibrationDamp < -60.0 THEN rDelta_u3_VibrationDamp := -60.0; END_IF;

IF rDelta_u4_RegenChopper > 20.0 THEN rDelta_u4_RegenChopper := 20.0;
ELSIF rDelta_u4_RegenChopper < -20.0 THEN rDelta_u4_RegenChopper := -20.0; END_IF;

(* Update Actuator Controls with Box Saturation Constraints *)
rPrev_u1_HoistTorque := rPrev_u1_HoistTorque + rDelta_u1_HoistTorque;
IF rPrev_u1_HoistTorque > c_rMaxHoistTorque_Nm THEN rPrev_u1_HoistTorque := c_rMaxHoistTorque_Nm;
ELSIF rPrev_u1_HoistTorque < c_rMinHoistTorque_Nm THEN rPrev_u1_HoistTorque := c_rMinHoistTorque_Nm; END_IF;

rPrev_u2_ShuttleServo := rPrev_u2_ShuttleServo + rDelta_u2_ShuttleServo;
IF rPrev_u2_ShuttleServo > c_rMaxShuttleServo_Nm THEN rPrev_u2_ShuttleServo := c_rMaxShuttleServo_Nm;
ELSIF rPrev_u2_ShuttleServo < c_rMinShuttleServo_Nm THEN rPrev_u2_ShuttleServo := c_rMinShuttleServo_Nm; END_IF;

rPrev_u3_VibrationDamp := rPrev_u3_VibrationDamp + rDelta_u3_VibrationDamp;
IF rPrev_u3_VibrationDamp > c_rMaxDampTorque_Nm THEN rPrev_u3_VibrationDamp := c_rMaxDampTorque_Nm;
ELSIF rPrev_u3_VibrationDamp < c_rMinDampTorque_Nm THEN rPrev_u3_VibrationDamp := c_rMinDampTorque_Nm; END_IF;

rPrev_u4_RegenChopper := rPrev_u4_RegenChopper + rDelta_u4_RegenChopper;
IF rPrev_u4_RegenChopper > c_rMaxRegenPower_kW THEN rPrev_u4_RegenChopper := c_rMaxRegenPower_kW;
ELSIF rPrev_u4_RegenChopper < c_rMinRegenPower_kW THEN rPrev_u4_RegenChopper := c_rMinRegenPower_kW; END_IF;

rPrevDelta_u1 := rDelta_u1_HoistTorque;
rPrevDelta_u2 := rDelta_u2_ShuttleServo;
rPrevDelta_u3 := rDelta_u3_VibrationDamp;
rPrevDelta_u4 := rDelta_u4_RegenChopper;

(* Total Hoist Vector Torque Demand (MPC Baseline + Active Cable Vibration Damping) *)
rHoistTorqueDemand_Nm := rPrev_u1_HoistTorque + rActiveDampingTorque_Nm;

(* --- 3.4 DC LINK VOLTAGE REGULATION & REGENERATIVE BRAKING CHOPPER --- *)
IF rDCLinkVoltage_V > c_rDCLink_H_V THEN
    rChopperDutyCycle_Pct := ((rDCLinkVoltage_V - c_rDCLink_H_V) / (c_rDCLink_HH_V - c_rDCLink_H_V)) * 100.0;
    IF rChopperDutyCycle_Pct > 100.0 THEN rChopperDutyCycle_Pct := 100.0; END_IF;
    bRegenerativeBrakeChopperFire := TRUE;
ELSE
    rChopperDutyCycle_Pct := 0.0;
    bRegenerativeBrakeChopperFire := FALSE;
END_IF;

(* Real-Time Mechanical Power P = T * omega [kW] *)
rNetMechanicalPower_kW := (rHoistTorqueDemand_Nm * (rVotedHoistVelocity_m_s / c_rTractionSheaveRadius_m)) / 1000.0;

(* If motor operates in regenerating quadrant (negative mechanical power) *)
IF rNetMechanicalPower_kW < 0.0 THEN
    rCalculatedRegenPower_kW := ABS(rNetMechanicalPower_kW) * 0.92; (* 92% Inverter Conversion Efficiency *)
    rTotalRegenEnergy_kWh := rTotalRegenEnergy_kWh + (rCalculatedRegenPower_kW * (c_rScanTime_Ts / 3600.0));
    rRegenPowerFeedback_kW := rCalculatedRegenPower_kW;
ELSE
    rCalculatedRegenPower_kW := 0.0;
    rRegenPowerFeedback_kW := 0.0;
END_IF;

(* ================================================================================================= *)
(* === PHASE 4: THERMAL REPLICA & CABLE TENSION MONITORING                                       === *)
(* ================================================================================================= *)

(* --- 4.1 PMSM STATOR COPPER WINDING DYNAMIC THERMAL REPLICA --- *)
rScratch1 := (rTractionMotorCurrent_A / c_rMotorRatedCurrent_A) * (rTractionMotorCurrent_A / c_rMotorRatedCurrent_A);
rScratch2 := c_rCabinAmbientTemp_degC + (rScratch1 * c_rMotorRatedRise_degC);
rSimStatorTemp_degC := rSimStatorTemp_degC + ((rScratch2 - rSimStatorTemp_degC) * (c_rScanTime_Ts / c_rMotorThermalTimeConst_s));
rSimStatorWindingTemp_degC := rSimStatorTemp_degC;

(* --- 4.2 MECHANICAL BRAKE DISC FRICTION THERMAL REPLICA --- *)
IF NOT bHoistMechanicalBrakeRelease AND (ABS(rVotedHoistVelocity_m_s) > 0.05) THEN
    (* Mechanical brake slipping while carriage moving - kinetic energy absorption *)
    rScratch3 := 0.50 * (c_rHoistCarriageTareMass_kg + rVotedVehicleWeight_kg) * (rVotedHoistVelocity_m_s * rVotedHoistVelocity_m_s);
    rSimBrakeTemp_degC := rSimBrakeTemp_degC + (rScratch3 * 0.000045);
ELSE
    (* Natural convective cooling *)
    rSimBrakeTemp_degC := rSimBrakeTemp_degC - ((rSimBrakeTemp_degC - c_rCabinAmbientTemp_degC) * (c_rScanTime_Ts / c_rBrakeCoolingTimeConst_s));
END_IF;
rSimBrakeDiscTemp_degC := rSimBrakeTemp_degC;

(* --- 4.3 CABLE TENSION INTEGRITY & SLACK ROPE INTERLOCK --- *)
IF (rHoistCableTension_kN <= c_rCableTension_LL_kN) OR bSlackCableSwitchTripped THEN
    bAlarm_CableTension_LL := TRUE;
    bCriticalSafetyTrip := TRUE;
    bEmergencyClampDeployCmd := TRUE;
END_IF;
"""
