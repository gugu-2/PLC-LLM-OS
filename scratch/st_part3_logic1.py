# -*- coding: utf-8 -*-

part3_logic1 = """(* ================================================================================================= *)
(* === PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING & SENSOR DEGRADATION          === *)
(* ================================================================================================= *)

(* --- 1.1 GROUP 1: VERTICAL HOIST OPTICAL LASER DISTANCE SENSORS --- *)
rDiffAB := ABS(rHoistLaserDist_A_mm - rHoistLaserDist_B_mm);
rDiffBC := ABS(rHoistLaserDist_B_mm - rHoistLaserDist_C_mm);
rDiffCA := ABS(rHoistLaserDist_C_mm - rHoistLaserDist_A_mm);

IF (rDiffAB <= rHoistLaser_Tol_mm) AND (rDiffBC <= rHoistLaser_Tol_mm) AND (rDiffCA <= rHoistLaser_Tol_mm) THEN
    (* All three laser channels healthy - execute 2oo3 median selection *)
    bHoistLaser_Degraded := FALSE;
    bHoistLaser_Fault := FALSE;
    rTimer_HoistLaser_Discrep := 0.0;
    
    IF ((rHoistLaserDist_A_mm >= rHoistLaserDist_B_mm) AND (rHoistLaserDist_A_mm <= rHoistLaserDist_C_mm)) OR
       ((rHoistLaserDist_A_mm <= rHoistLaserDist_B_mm) AND (rHoistLaserDist_A_mm >= rHoistLaserDist_C_mm)) THEN
        rVotedHoistLaser_mm := rHoistLaserDist_A_mm;
    ELSIF ((rHoistLaserDist_B_mm >= rHoistLaserDist_A_mm) AND (rHoistLaserDist_B_mm <= rHoistLaserDist_C_mm)) OR
          ((rHoistLaserDist_B_mm <= rHoistLaserDist_A_mm) AND (rHoistLaserDist_B_mm >= rHoistLaserDist_C_mm)) THEN
        rVotedHoistLaser_mm := rHoistLaserDist_B_mm;
    ELSE
        rVotedHoistLaser_mm := rHoistLaserDist_C_mm;
    END_IF;

ELSIF (rDiffAB <= rHoistLaser_Tol_mm) THEN
    (* Channel C drifted - degrade to 1oo2 average of A and B *)
    rTimer_HoistLaser_Discrep := rTimer_HoistLaser_Discrep + c_rScanTime_Ts;
    IF rTimer_HoistLaser_Discrep >= c_rMaxSensorDiscrepTime_s THEN
        bHoistLaser_Degraded := TRUE;
        rVotedHoistLaser_mm := (rHoistLaserDist_A_mm + rHoistLaserDist_B_mm) * 0.50;
    ELSE
        (* Maintain median during transient filter window *)
        rVotedHoistLaser_mm := (rHoistLaserDist_A_mm + rHoistLaserDist_B_mm) * 0.50;
    END_IF;

ELSIF (rDiffBC <= rHoistLaser_Tol_mm) THEN
    (* Channel A drifted - degrade to 1oo2 average of B and C *)
    rTimer_HoistLaser_Discrep := rTimer_HoistLaser_Discrep + c_rScanTime_Ts;
    IF rTimer_HoistLaser_Discrep >= c_rMaxSensorDiscrepTime_s THEN
        bHoistLaser_Degraded := TRUE;
        rVotedHoistLaser_mm := (rHoistLaserDist_B_mm + rHoistLaserDist_C_mm) * 0.50;
    ELSE
        rVotedHoistLaser_mm := (rHoistLaserDist_B_mm + rHoistLaserDist_C_mm) * 0.50;
    END_IF;

ELSIF (rDiffCA <= rHoistLaser_Tol_mm) THEN
    (* Channel B drifted - degrade to 1oo2 average of C and A *)
    rTimer_HoistLaser_Discrep := rTimer_HoistLaser_Discrep + c_rScanTime_Ts;
    IF rTimer_HoistLaser_Discrep >= c_rMaxSensorDiscrepTime_s THEN
        bHoistLaser_Degraded := TRUE;
        rVotedHoistLaser_mm := (rHoistLaserDist_C_mm + rHoistLaserDist_A_mm) * 0.50;
    ELSE
        rVotedHoistLaser_mm := (rHoistLaserDist_C_mm + rHoistLaserDist_A_mm) * 0.50;
    END_IF;

ELSE
    (* Complete divergence across all three channels - persistent trip *)
    rTimer_HoistLaser_Discrep := rTimer_HoistLaser_Discrep + c_rScanTime_Ts;
    IF rTimer_HoistLaser_Discrep >= c_rMaxSensorDiscrepTime_s THEN
        bHoistLaser_Fault := TRUE;
        bAlarm_LaserSpread_Trip := TRUE;
    END_IF;
END_IF;

(* --- 1.2 GROUP 2: HOIST ROTARY TRACTION SHEAVE ABSOLUTE OPTICAL ENCODERS --- *)
rDiffAB := ABS(rHoistRotaryEncoder_A_mm - rHoistRotaryEncoder_B_mm);
rDiffBC := ABS(rHoistRotaryEncoder_B_mm - rHoistRotaryEncoder_C_mm);
rDiffCA := ABS(rHoistRotaryEncoder_C_mm - rHoistRotaryEncoder_A_mm);

IF (rDiffAB <= rHoistEncoder_Tol_mm) AND (rDiffBC <= rHoistEncoder_Tol_mm) AND (rDiffCA <= rHoistEncoder_Tol_mm) THEN
    bHoistEncoder_Degraded := FALSE;
    bHoistEncoder_Fault := FALSE;
    rTimer_HoistEncoder_Discrep := 0.0;
    
    IF ((rHoistRotaryEncoder_A_mm >= rHoistRotaryEncoder_B_mm) AND (rHoistRotaryEncoder_A_mm <= rHoistRotaryEncoder_C_mm)) OR
       ((rHoistRotaryEncoder_A_mm <= rHoistRotaryEncoder_B_mm) AND (rHoistRotaryEncoder_A_mm >= rHoistRotaryEncoder_C_mm)) THEN
        rVotedHoistEncoder_mm := rHoistRotaryEncoder_A_mm;
    ELSIF ((rHoistRotaryEncoder_B_mm >= rHoistRotaryEncoder_A_mm) AND (rHoistRotaryEncoder_B_mm <= rHoistRotaryEncoder_C_mm)) OR
          ((rHoistRotaryEncoder_B_mm <= rHoistRotaryEncoder_A_mm) AND (rHoistRotaryEncoder_B_mm >= rHoistRotaryEncoder_C_mm)) THEN
        rVotedHoistEncoder_mm := rHoistRotaryEncoder_B_mm;
    ELSE
        rVotedHoistEncoder_mm := rHoistRotaryEncoder_C_mm;
    END_IF;

ELSIF (rDiffAB <= rHoistEncoder_Tol_mm) THEN
    rTimer_HoistEncoder_Discrep := rTimer_HoistEncoder_Discrep + c_rScanTime_Ts;
    IF rTimer_HoistEncoder_Discrep >= c_rMaxSensorDiscrepTime_s THEN
        bHoistEncoder_Degraded := TRUE;
        rVotedHoistEncoder_mm := (rHoistRotaryEncoder_A_mm + rHoistRotaryEncoder_B_mm) * 0.50;
    ELSE
        rVotedHoistEncoder_mm := (rHoistRotaryEncoder_A_mm + rHoistRotaryEncoder_B_mm) * 0.50;
    END_IF;

ELSIF (rDiffBC <= rHoistEncoder_Tol_mm) THEN
    rTimer_HoistEncoder_Discrep := rTimer_HoistEncoder_Discrep + c_rScanTime_Ts;
    IF rTimer_HoistEncoder_Discrep >= c_rMaxSensorDiscrepTime_s THEN
        bHoistEncoder_Degraded := TRUE;
        rVotedHoistEncoder_mm := (rHoistRotaryEncoder_B_mm + rHoistRotaryEncoder_C_mm) * 0.50;
    ELSE
        rVotedHoistEncoder_mm := (rHoistRotaryEncoder_B_mm + rHoistRotaryEncoder_C_mm) * 0.50;
    END_IF;

ELSIF (rDiffCA <= rHoistEncoder_Tol_mm) THEN
    rTimer_HoistEncoder_Discrep := rTimer_HoistEncoder_Discrep + c_rScanTime_Ts;
    IF rTimer_HoistEncoder_Discrep >= c_rMaxSensorDiscrepTime_s THEN
        bHoistEncoder_Degraded := TRUE;
        rVotedHoistEncoder_mm := (rHoistRotaryEncoder_C_mm + rHoistRotaryEncoder_A_mm) * 0.50;
    ELSE
        rVotedHoistEncoder_mm := (rHoistRotaryEncoder_C_mm + rHoistRotaryEncoder_A_mm) * 0.50;
    END_IF;

ELSE
    rTimer_HoistEncoder_Discrep := rTimer_HoistEncoder_Discrep + c_rScanTime_Ts;
    IF rTimer_HoistEncoder_Discrep >= c_rMaxSensorDiscrepTime_s THEN
        bHoistEncoder_Fault := TRUE;
        bAlarm_EncoderSpread_Trip := TRUE;
    END_IF;
END_IF;

(* --- 1.3 CROSS-CORRELATION: OPTICAL LASER ELEVATION VS ROTARY SHEAVE FEEDBACK (ROPE SLIP) --- *)
rLaserVsEncoderDelta_mm := ABS(rVotedHoistLaser_mm - rVotedHoistEncoder_mm);
IF rLaserVsEncoderDelta_mm > c_rMaxRopeSlipDeviation_mm THEN
    rTimer_RopeSlip_Discrep := rTimer_RopeSlip_Discrep + c_rScanTime_Ts;
    IF rTimer_RopeSlip_Discrep >= 0.250 THEN
        bTractionRopeSlipWarning := TRUE;
        bAlarm_TractionRopeSlip := TRUE;
    END_IF;
ELSE
    rTimer_RopeSlip_Discrep := 0.0;
    bTractionRopeSlipWarning := FALSE;
END_IF;

(* Primary Position Selection: Use Laser Distance with Encoder Fallback *)
IF NOT bHoistLaser_Fault THEN
    rVotedHoistPosition_mm := rVotedHoistLaser_mm;
ELSIF NOT bHoistEncoder_Fault THEN
    rVotedHoistPosition_mm := rVotedHoistEncoder_mm;
ELSE
    (* Dual catastrophic loss of position sensing *)
    bCriticalSafetyTrip := TRUE;
END_IF;

(* --- 1.4 NUMERICAL 2ND-ORDER VELOCITY & ACCELERATION DIFFERENTIATION --- *)
rRawVelocity_m_s := ((3.0 * rVotedHoistPosition_mm) - (4.0 * rPosBuffer_k1) + rPosBuffer_k2) / (2.0 * c_rScanTime_Ts * 1000.0);
rFilteredVelocity_m_s := (c_rVelFilterAlpha * rRawVelocity_m_s) + ((1.0 - c_rVelFilterAlpha) * rFilteredVelocity_m_s);
rVotedHoistVelocity_m_s := rFilteredVelocity_m_s;

rRawAccel_m_s2 := (rFilteredVelocity_m_s - ((rPosBuffer_k1 - rPosBuffer_k2) / (c_rScanTime_Ts * 1000.0))) / c_rScanTime_Ts;
rFilteredAccel_m_s2 := (c_rVelFilterAlpha * rRawAccel_m_s2) + ((1.0 - c_rVelFilterAlpha) * rFilteredAccel_m_s2);

(* Update 5-point ring buffer *)
rPosBuffer_k4 := rPosBuffer_k3;
rPosBuffer_k3 := rPosBuffer_k2;
rPosBuffer_k2 := rPosBuffer_k1;
rPosBuffer_k1 := rVotedHoistPosition_mm;

(* --- 1.5 GROUP 3: HORIZONTAL RACK SHUTTLE OPTICAL LASERS --- *)
rDiffAB := ABS(rShuttleLaserDist_A_mm - rShuttleLaserDist_B_mm);
rDiffBC := ABS(rShuttleLaserDist_B_mm - rShuttleLaserDist_C_mm);
rDiffCA := ABS(rShuttleLaserDist_C_mm - rShuttleLaserDist_A_mm);

IF (rDiffAB <= rShuttleLaser_Tol_mm) AND (rDiffBC <= rShuttleLaser_Tol_mm) AND (rDiffCA <= rShuttleLaser_Tol_mm) THEN
    bShuttleLaser_Degraded := FALSE;
    bShuttleLaser_Fault := FALSE;
    rTimer_ShuttleLaser_Discrep := 0.0;
    
    IF ((rShuttleLaserDist_A_mm >= rShuttleLaserDist_B_mm) AND (rShuttleLaserDist_A_mm <= rShuttleLaserDist_C_mm)) OR
       ((rShuttleLaserDist_A_mm <= rShuttleLaserDist_B_mm) AND (rShuttleLaserDist_A_mm >= rShuttleLaserDist_C_mm)) THEN
        rVotedShuttleLaser_mm := rShuttleLaserDist_A_mm;
    ELSIF ((rShuttleLaserDist_B_mm >= rShuttleLaserDist_A_mm) AND (rShuttleLaserDist_B_mm <= rShuttleLaserDist_C_mm)) OR
          ((rShuttleLaserDist_B_mm <= rShuttleLaserDist_A_mm) AND (rShuttleLaserDist_B_mm >= rShuttleLaserDist_C_mm)) THEN
        rVotedShuttleLaser_mm := rShuttleLaserDist_B_mm;
    ELSE
        rVotedShuttleLaser_mm := rShuttleLaserDist_C_mm;
    END_IF;

ELSIF (rDiffAB <= rShuttleLaser_Tol_mm) THEN
    rTimer_ShuttleLaser_Discrep := rTimer_ShuttleLaser_Discrep + c_rScanTime_Ts;
    IF rTimer_ShuttleLaser_Discrep >= c_rMaxSensorDiscrepTime_s THEN
        bShuttleLaser_Degraded := TRUE;
        rVotedShuttleLaser_mm := (rShuttleLaserDist_A_mm + rShuttleLaserDist_B_mm) * 0.50;
    ELSE
        rVotedShuttleLaser_mm := (rShuttleLaserDist_A_mm + rShuttleLaserDist_B_mm) * 0.50;
    END_IF;

ELSIF (rDiffBC <= rShuttleLaser_Tol_mm) THEN
    rTimer_ShuttleLaser_Discrep := rTimer_ShuttleLaser_Discrep + c_rScanTime_Ts;
    IF rTimer_ShuttleLaser_Discrep >= c_rMaxSensorDiscrepTime_s THEN
        bShuttleLaser_Degraded := TRUE;
        rVotedShuttleLaser_mm := (rShuttleLaserDist_B_mm + rShuttleLaserDist_C_mm) * 0.50;
    ELSE
        rVotedShuttleLaser_mm := (rShuttleLaserDist_B_mm + rShuttleLaserDist_C_mm) * 0.50;
    END_IF;

ELSIF (rDiffCA <= rShuttleLaser_Tol_mm) THEN
    rTimer_ShuttleLaser_Discrep := rTimer_ShuttleLaser_Discrep + c_rScanTime_Ts;
    IF rTimer_ShuttleLaser_Discrep >= c_rMaxSensorDiscrepTime_s THEN
        bShuttleLaser_Degraded := TRUE;
        rVotedShuttleLaser_mm := (rShuttleLaserDist_C_mm + rShuttleLaserDist_A_mm) * 0.50;
    ELSE
        rVotedShuttleLaser_mm := (rShuttleLaserDist_C_mm + rShuttleLaserDist_A_mm) * 0.50;
    END_IF;

ELSE
    rTimer_ShuttleLaser_Discrep := rTimer_ShuttleLaser_Discrep + c_rScanTime_Ts;
    IF rTimer_ShuttleLaser_Discrep >= c_rMaxSensorDiscrepTime_s THEN
        bShuttleLaser_Fault := TRUE;
        bAlarm_ShuttleSpread_Trip := TRUE;
    END_IF;
END_IF;

rVotedShuttlePosition_mm := rVotedShuttleLaser_mm;

(* --- 1.6 GROUP 4: ENTRY CABIN PLATFORM WEIGH SCALE LOAD CELLS --- *)
rDiffAB := ABS(rPalletLoadCell_A_kg - rPalletLoadCell_B_kg);
rDiffBC := ABS(rPalletLoadCell_B_kg - rPalletLoadCell_C_kg);
rDiffCA := ABS(rPalletLoadCell_C_kg - rPalletLoadCell_A_kg);

IF (rDiffAB <= rLoadCell_Tol_kg) AND (rDiffBC <= rLoadCell_Tol_kg) AND (rDiffCA <= rLoadCell_Tol_kg) THEN
    bLoadCell_Degraded := FALSE;
    bLoadCell_Fault := FALSE;
    rTimer_LoadCell_Discrep := 0.0;
    
    IF ((rPalletLoadCell_A_kg >= rPalletLoadCell_B_kg) AND (rPalletLoadCell_A_kg <= rPalletLoadCell_C_kg)) OR
       ((rPalletLoadCell_A_kg <= rPalletLoadCell_B_kg) AND (rPalletLoadCell_A_kg >= rPalletLoadCell_C_kg)) THEN
        rVotedPlatformWeight_kg := rPalletLoadCell_A_kg;
    ELSIF ((rPalletLoadCell_B_kg >= rPalletLoadCell_A_kg) AND (rPalletLoadCell_B_kg <= rPalletLoadCell_C_kg)) OR
          ((rPalletLoadCell_B_kg <= rPalletLoadCell_A_kg) AND (rPalletLoadCell_B_kg >= rPalletLoadCell_C_kg)) THEN
        rVotedPlatformWeight_kg := rPalletLoadCell_B_kg;
    ELSE
        rVotedPlatformWeight_kg := rPalletLoadCell_C_kg;
    END_IF;

ELSIF (rDiffAB <= rLoadCell_Tol_kg) THEN
    rTimer_LoadCell_Discrep := rTimer_LoadCell_Discrep + c_rScanTime_Ts;
    IF rTimer_LoadCell_Discrep >= c_rMaxSensorDiscrepTime_s THEN
        bLoadCell_Degraded := TRUE;
        rVotedPlatformWeight_kg := (rPalletLoadCell_A_kg + rPalletLoadCell_B_kg) * 0.50;
    ELSE
        rVotedPlatformWeight_kg := (rPalletLoadCell_A_kg + rPalletLoadCell_B_kg) * 0.50;
    END_IF;

ELSIF (rDiffBC <= rLoadCell_Tol_kg) THEN
    rTimer_LoadCell_Discrep := rTimer_LoadCell_Discrep + c_rScanTime_Ts;
    IF rTimer_LoadCell_Discrep >= c_rMaxSensorDiscrepTime_s THEN
        bLoadCell_Degraded := TRUE;
        rVotedPlatformWeight_kg := (rPalletLoadCell_B_kg + rPalletLoadCell_C_kg) * 0.50;
    ELSE
        rVotedPlatformWeight_kg := (rPalletLoadCell_B_kg + rPalletLoadCell_C_kg) * 0.50;
    END_IF;

ELSIF (rDiffCA <= rLoadCell_Tol_kg) THEN
    rTimer_LoadCell_Discrep := rTimer_LoadCell_Discrep + c_rScanTime_Ts;
    IF rTimer_LoadCell_Discrep >= c_rMaxSensorDiscrepTime_s THEN
        bLoadCell_Degraded := TRUE;
        rVotedPlatformWeight_kg := (rPalletLoadCell_C_kg + rPalletLoadCell_A_kg) * 0.50;
    ELSE
        rVotedPlatformWeight_kg := (rPalletLoadCell_C_kg + rPalletLoadCell_A_kg) * 0.50;
    END_IF;

ELSE
    rTimer_LoadCell_Discrep := rTimer_LoadCell_Discrep + c_rScanTime_Ts;
    IF rTimer_LoadCell_Discrep >= c_rMaxSensorDiscrepTime_s THEN
        bLoadCell_Fault := TRUE;
        bAlarm_LoadCellSpread_Trip := TRUE;
    END_IF;
END_IF;

rVotedVehicleWeight_kg := rVotedPlatformWeight_kg;

(* Summary Degraded Sensor Flag *)
bDegradedSensorWarning := bHoistLaser_Degraded OR bHoistEncoder_Degraded OR bShuttleLaser_Degraded OR bLoadCell_Degraded;

(* ================================================================================================= *)
(* === PHASE 2: STATE-SPACE PREDICTION & CABLE ELASTICITY VIBRATION OBSERVER                     === *)
(* ================================================================================================= *)

(* --- 2.1 CABLE ELASTICITY DYNAMICS & OSCILLATION OBSERVER --- *)
rFreeCableLength_m := 38.0 - (rVotedHoistPosition_mm / 1000.0);
IF rFreeCableLength_m < 2.0 THEN
    rFreeCableLength_m := 2.0;
END_IF;

(* Load-dependent cable stiffness k = (E * A) / L *)
rDynamicCableStiffness_N_m := (c_rRopeElasticModulus_N_mm2 * c_rRopeCrossSection_mm2) / rFreeCableLength_m;
IF rDynamicCableStiffness_N_m < 50000.0 THEN
    rDynamicCableStiffness_N_m := 50000.0;
END_IF;

(* Observed dynamic stretch oscillation from cable tension transducer *)
rScratch1 := c_rHoistCarriageTareMass_kg + rVotedVehicleWeight_kg;
rScratch2 := (rHoistCableTension_kN * 1000.0) - (rScratch1 * c_rGravity_g);
rScratch3 := (rScratch2 / rDynamicCableStiffness_N_m) * 1000.0; (* Dynamic Stretch in mm *)

(* Low-pass filter observed stretch *)
rObservedStretch_mm := (0.22 * rScratch3) + (0.78 * rObservedStretch_mm);
rObservedStretchVelocity_mm_s := (rObservedStretch_mm - rPriorObservedStretch_mm) / c_rScanTime_Ts;
rPriorObservedStretch_mm := rObservedStretch_mm;
rCableVibrationAmplitude_mm := ABS(rObservedStretch_mm);

(* Active Vibration Damping Feedforward Torque Law *)
rActiveDampingTorque_Nm := - (rActiveDampingGain_Kp * rObservedStretch_mm) - (rActiveDampingGain_Kd * rObservedStretchVelocity_mm_s);
IF rActiveDampingTorque_Nm > c_rMaxDampTorque_Nm THEN
    rActiveDampingTorque_Nm := c_rMaxDampTorque_Nm;
ELSIF rActiveDampingTorque_Nm < c_rMinDampTorque_Nm THEN
    rActiveDampingTorque_Nm := c_rMinDampTorque_Nm;
END_IF;

(* --- 2.2 DISCRETE STATE DEVIATION VECTOR EVALUATION --- *)
x1_PosDev := rVotedHoistPosition_mm - rRef_HoistPos_mm;
x2_VelDev := (rVotedHoistVelocity_m_s * 1000.0) - rRef_HoistVel_mm_s;
x3_CableStretchDev := rObservedStretch_mm - rRef_CableStretch_mm;
x4_CableStretchRateDev := rObservedStretchVelocity_mm_s - rRef_CableStretchRate_mm_s;
x5_ShuttlePosDev := rVotedShuttlePosition_mm - rRef_ShuttlePos_mm;
x6_ShuttleVelDev := (rShuttleProfileVel_m_s * 1000.0) - rRef_ShuttleVel_mm_s;
x7_TorqueDev := rHoistTorqueDemand_Nm - rRef_Torque_Nm;
x8_DCLinkDev := rDCLinkVoltage_V - rRef_DCLink_V;

(* --- 2.3 8-STATE 1-STEP AHEAD PREDICTION (x_pred = Ad * x + Bd * u) --- *)
x1_Pred := (Ad_11 * x1_PosDev) + (Ad_12 * x2_VelDev) + (Ad_13 * x3_CableStretchDev) + (Ad_14 * x4_CableStretchRateDev) +
           (Ad_15 * x5_ShuttlePosDev) + (Ad_16 * x6_ShuttleVelDev) + (Ad_17 * x7_TorqueDev) + (Ad_18 * x8_DCLinkDev) +
           (Bd_11 * rPrev_u1_HoistTorque) + (Bd_12 * rPrev_u2_ShuttleServo) + (Bd_13 * rPrev_u3_VibrationDamp) + (Bd_14 * rPrev_u4_RegenChopper);

x2_Pred := (Ad_21 * x1_PosDev) + (Ad_22 * x2_VelDev) + (Ad_23 * x3_CableStretchDev) + (Ad_24 * x4_CableStretchRateDev) +
           (Ad_25 * x5_ShuttlePosDev) + (Ad_26 * x6_ShuttleVelDev) + (Ad_27 * x7_TorqueDev) + (Ad_28 * x8_DCLinkDev) +
           (Bd_21 * rPrev_u1_HoistTorque) + (Bd_22 * rPrev_u2_ShuttleServo) + (Bd_23 * rPrev_u3_VibrationDamp) + (Bd_24 * rPrev_u4_RegenChopper);

x3_Pred := (Ad_31 * x1_PosDev) + (Ad_32 * x2_VelDev) + (Ad_33 * x3_CableStretchDev) + (Ad_34 * x4_CableStretchRateDev) +
           (Ad_35 * x5_ShuttlePosDev) + (Ad_36 * x6_ShuttleVelDev) + (Ad_37 * x7_TorqueDev) + (Ad_38 * x8_DCLinkDev) +
           (Bd_31 * rPrev_u1_HoistTorque) + (Bd_32 * rPrev_u2_ShuttleServo) + (Bd_33 * rPrev_u3_VibrationDamp) + (Bd_34 * rPrev_u4_RegenChopper);

x4_Pred := (Ad_41 * x1_PosDev) + (Ad_42 * x2_VelDev) + (Ad_43 * x3_CableStretchDev) + (Ad_44 * x4_CableStretchRateDev) +
           (Ad_45 * x5_ShuttlePosDev) + (Ad_46 * x6_ShuttleVelDev) + (Ad_47 * x7_TorqueDev) + (Ad_48 * x8_DCLinkDev) +
           (Bd_41 * rPrev_u1_HoistTorque) + (Bd_42 * rPrev_u2_ShuttleServo) + (Bd_43 * rPrev_u3_VibrationDamp) + (Bd_44 * rPrev_u4_RegenChopper);

x5_Pred := (Ad_51 * x1_PosDev) + (Ad_52 * x2_VelDev) + (Ad_53 * x3_CableStretchDev) + (Ad_54 * x4_CableStretchRateDev) +
           (Ad_55 * x5_ShuttlePosDev) + (Ad_56 * x6_ShuttleVelDev) + (Ad_57 * x7_TorqueDev) + (Ad_58 * x8_DCLinkDev) +
           (Bd_51 * rPrev_u1_HoistTorque) + (Bd_52 * rPrev_u2_ShuttleServo) + (Bd_53 * rPrev_u3_VibrationDamp) + (Bd_54 * rPrev_u4_RegenChopper);

x6_Pred := (Ad_61 * x1_PosDev) + (Ad_62 * x2_VelDev) + (Ad_63 * x3_CableStretchDev) + (Ad_64 * x4_CableStretchRateDev) +
           (Ad_65 * x5_ShuttlePosDev) + (Ad_66 * x6_ShuttleVelDev) + (Ad_67 * x7_TorqueDev) + (Ad_68 * x8_DCLinkDev) +
           (Bd_61 * rPrev_u1_HoistTorque) + (Bd_62 * rPrev_u2_ShuttleServo) + (Bd_63 * rPrev_u3_VibrationDamp) + (Bd_64 * rPrev_u4_RegenChopper);

x7_Pred := (Ad_71 * x1_PosDev) + (Ad_72 * x2_VelDev) + (Ad_73 * x3_CableStretchDev) + (Ad_74 * x4_CableStretchRateDev) +
           (Ad_75 * x5_ShuttlePosDev) + (Ad_76 * x6_ShuttleVelDev) + (Ad_77 * x7_TorqueDev) + (Ad_78 * x8_DCLinkDev) +
           (Bd_71 * rPrev_u1_HoistTorque) + (Bd_72 * rPrev_u2_ShuttleServo) + (Bd_73 * rPrev_u3_VibrationDamp) + (Bd_74 * rPrev_u4_RegenChopper);

x8_Pred := (Ad_81 * x1_PosDev) + (Ad_82 * x2_VelDev) + (Ad_83 * x3_CableStretchDev) + (Ad_84 * x4_CableStretchRateDev) +
           (Ad_85 * x5_ShuttlePosDev) + (Ad_86 * x6_ShuttleVelDev) + (Ad_87 * x7_TorqueDev) + (Ad_88 * x8_DCLinkDev) +
           (Bd_81 * rPrev_u1_HoistTorque) + (Bd_82 * rPrev_u2_ShuttleServo) + (Bd_83 * rPrev_u3_VibrationDamp) + (Bd_84 * rPrev_u4_RegenChopper);

(* --- 2.4 4-OUTPUT MEASUREMENT PREDICTION (y_pred = Cd * x_pred + Dd * u) --- *)
y1_PredHoistPos := (Cd_11 * x1_Pred) + (Cd_12 * x2_Pred) + (Cd_13 * x3_Pred) + (Cd_14 * x4_Pred) +
                   (Cd_15 * x5_Pred) + (Cd_16 * x6_Pred) + (Cd_17 * x7_Pred) + (Cd_18 * x8_Pred) +
                   (Dd_11 * rPrev_u1_HoistTorque) + (Dd_12 * rPrev_u2_ShuttleServo) + (Dd_13 * rPrev_u3_VibrationDamp) + (Dd_14 * rPrev_u4_RegenChopper) +
                   rRef_HoistPos_mm;

y2_PredCableStretch := (Cd_21 * x1_Pred) + (Cd_22 * x2_Pred) + (Cd_23 * x3_Pred) + (Cd_24 * x4_Pred) +
                       (Cd_25 * x5_Pred) + (Cd_26 * x6_Pred) + (Cd_27 * x7_Pred) + (Cd_28 * x8_Pred) +
                       (Dd_21 * rPrev_u1_HoistTorque) + (Dd_22 * rPrev_u2_ShuttleServo) + (Dd_23 * rPrev_u3_VibrationDamp) + (Dd_24 * rPrev_u4_RegenChopper) +
                       rRef_CableStretch_mm;

y3_PredShuttlePos := (Cd_31 * x1_Pred) + (Cd_32 * x2_Pred) + (Cd_33 * x3_Pred) + (Cd_34 * x4_Pred) +
                     (Cd_35 * x5_Pred) + (Cd_36 * x6_Pred) + (Cd_37 * x7_Pred) + (Cd_38 * x8_Pred) +
                     (Dd_31 * rPrev_u1_HoistTorque) + (Dd_32 * rPrev_u2_ShuttleServo) + (Dd_33 * rPrev_u3_VibrationDamp) + (Dd_34 * rPrev_u4_RegenChopper) +
                     rRef_ShuttlePos_mm;

y4_PredDCLink := (Cd_41 * x1_Pred) + (Cd_42 * x2_Pred) + (Cd_43 * x3_Pred) + (Cd_44 * x4_Pred) +
                 (Cd_45 * x5_Pred) + (Cd_46 * x6_Pred) + (Cd_47 * x7_Pred) + (Cd_48 * x8_Pred) +
                 (Dd_41 * rPrev_u1_HoistTorque) + (Dd_42 * rPrev_u2_ShuttleServo) + (Dd_43 * rPrev_u3_VibrationDamp) + (Dd_44 * rPrev_u4_RegenChopper) +
                 rRef_DCLink_V;

rPredictedHoistPosition_mm := y1_PredHoistPos;
rPredictedCableStretch_mm := y2_PredCableStretch;
rPredictedDCLinkVoltage_V := y4_PredDCLink;
"""
