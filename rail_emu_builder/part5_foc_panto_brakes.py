# rail_emu_builder/part5_foc_panto_brakes.py

def get_part5():
    return '''(* ============================================================================================== *)
(* PHASE 5: 4-QUADRANT AC/DC CONVERTER & DYNAMIC INDUCTION MOTOR VECTOR CONTROL (FOC)              *)
(* Decoupled d-q Stator Flux & Torque Current Regulators with Field Weakening Above 120 km/h      *)
(* ============================================================================================== *)

(* 1. Rotor Mechanical Speed and Field Weakening Trajectory *)
rRotorMechanicalSpeed_rads := (rVotedAxleSpeed_A1_rpm * 2.0 * 3.14159265 / 60.0) * GEAR_RATIO;

IF rVotedTrainSpeed_kmh > MOTOR_BASE_SPEED_KMH THEN
    (* Field Weakening: Attenuate rotor flux inversely with speed up to 350 km/h *)
    rRotorFluxTarget_Wb := 1.250 * (MOTOR_BASE_SPEED_KMH / rVotedTrainSpeed_kmh);
    rRotorFluxTarget_Wb := MAX(0.420, rRotorFluxTarget_Wb);
ELSE
    rRotorFluxTarget_Wb := 1.250; (* Rated nominal rotor flux linkage [Wb] *)
END_IF;

(* 2. Rotor Flux Linkage Observer Integration *)
rFluxCurrentCommand_Isd_A := u_ctrl[1];
rScratchDiff := (MOTOR_MUTUAL_IND_H * rFluxCurrentCommand_Isd_A) - rRotorFluxEstimate_Wb;
rRotorFluxEstimate_Wb := rRotorFluxEstimate_Wb + ((MOTOR_ROTOR_RES_OHM / MOTOR_ROTOR_IND_H) * rScratchDiff * T_CYCLE_SEC);
rRotorFluxEstimate_Wb := MAX(0.350, MIN(1.450, rRotorFluxEstimate_Wb));

(* 3. Rotor Slip Angular Frequency & Stator Fundamental Frequency Calculation *)
rTorqueCurrentCommand_Isq_A := u_ctrl[2];
rSlipAngularFreq_rads := (MOTOR_ROTOR_RES_OHM * MOTOR_MUTUAL_IND_H * rTorqueCurrentCommand_Isq_A) / 
                         (MOTOR_ROTOR_IND_H * MAX(0.20, rRotorFluxEstimate_Wb));

rElectricalStatorFreq_rads := (INT_TO_REAL(MOTOR_POLE_PAIRS) * rRotorMechanicalSpeed_rads) + rSlipAngularFreq_rads;
rInverterFundamentalFreq_Hz := ABS(rElectricalStatorFreq_rads) / (2.0 * 3.14159265);
rInverterFundamentalFreq_Hz := MIN(220.0, rInverterFundamentalFreq_Hz);

(* Electrical Angle Integration theta_e = integral(omega_e * dt) *)
rStatorElectricalAngle_rad := rStatorElectricalAngle_rad + (rElectricalStatorFreq_rads * T_CYCLE_SEC);
IF rStatorElectricalAngle_rad > (2.0 * 3.14159265) THEN
    rStatorElectricalAngle_rad := rStatorElectricalAngle_rad - (2.0 * 3.14159265);
ELSIF rStatorElectricalAngle_rad < 0.0 THEN
    rStatorElectricalAngle_rad := rStatorElectricalAngle_rad + (2.0 * 3.14159265);
END_IF;

(* 4. Direct Axis (Flux) Current PI Regulator with Cross-Coupling Decoupling *)
rScratchDiff := rFluxCurrentCommand_Isd_A - (rRotorFluxEstimate_Wb / MOTOR_MUTUAL_IND_H);
rIsd_IntegralError := rIsd_IntegralError + (rScratchDiff * T_CYCLE_SEC);
rIsd_IntegralError := MAX(-500.0, MIN(500.0, rIsd_IntegralError));

rVsd_Decoupled_V := (rKp_Isd * rScratchDiff) + (rKi_Isd * rIsd_IntegralError) - 
                    (rElectricalStatorFreq_rads * MOTOR_SIGMA_LEAKAGE * MOTOR_STATOR_IND_H * rTorqueCurrentCommand_Isq_A);

(* 5. Quadrature Axis (Torque) Current PI Regulator with Cross-Coupling Decoupling *)
rScratchDiff := rTorqueCurrentCommand_Isq_A - (x_state[6] * 1000.0 / (1.5 * INT_TO_REAL(MOTOR_POLE_PAIRS) * (MOTOR_MUTUAL_IND_H / MOTOR_ROTOR_IND_H) * rRotorFluxEstimate_Wb));
rIsq_IntegralError := rIsq_IntegralError + (rScratchDiff * T_CYCLE_SEC);
rIsq_IntegralError := MAX(-800.0, MIN(800.0, rIsq_IntegralError));

rVsq_Decoupled_V := (rKp_Isq * rScratchDiff) + (rKi_Isq * rIsq_IntegralError) + 
                    (rElectricalStatorFreq_rads * MOTOR_STATOR_IND_H * rFluxCurrentCommand_Isd_A);

(* Decoupled Electromagnetic Torque Output Command [kNm] *)
rTractionTorqueCommand_kNm := 1.5 * INT_TO_REAL(MOTOR_POLE_PAIRS) * 
                              (MOTOR_MUTUAL_IND_H / MOTOR_ROTOR_IND_H) * 
                              rRotorFluxEstimate_Wb * rTorqueCurrentCommand_Isq_A * 0.001;

(* 6. 4-Quadrant Converter (4QC) DC Link Bus Voltage PI Stabilization *)
rDCLink_VoltageError := rDCLink_VoltageTarget_V - rVotedDCLinkVoltage_V;
rDCLink_IntegralError := rDCLink_IntegralError + (rDCLink_VoltageError * T_CYCLE_SEC);
rDCLink_IntegralError := MAX(-2000.0, MIN(2000.0, rDCLink_IntegralError));

rInverterModulationIndex_pct := 85.0 + (rKp_DCLink * rDCLink_VoltageError * 0.05) + (rKi_DCLink * rDCLink_IntegralError * 0.005);
rInverterModulationIndex_pct := MAX(15.0, MIN(100.0, rInverterModulationIndex_pct));

(* ============================================================================================== *)
(* PHASE 6: ACTIVE PNEUMATIC PANTOGRAPH CATENARY CONTACT FORCE REGULATION                          *)
(* Aerodynamic Uplift Feedforward & Closed-Loop Bellows Pressure Actuation (EN 50367 / TSI)       *)
(* ============================================================================================== *)

(* 1. High-Speed Dynamic Contact Force Setpoint Target [N] *)
(* At 0 km/h: 120 N; At 350 km/h: 120 + 0.00035 * 350^2 = 162.8 N *)
rPantoTargetForce_N := 120.0 + (0.000350 * rVotedTrainSpeed_kmh * rVotedTrainSpeed_kmh);
rPantoTargetForce_N := MIN(180.0, rPantoTargetForce_N);

(* 2. High-Speed Aerodynamic Uplift Force Estimation *)
(* F_aero = 0.5 * rho * C_lift * A_drag * (v_train / 3.6)^2 *)
rPantoAeroUplift_N := 0.5 * AIR_DENSITY_KG_M3 * PANTO_AERO_LIFT_COEFF * PANTO_AERO_DRAG_AREA_M2 * 
                      (rTrainSpeed_ms * rTrainSpeed_ms);

(* 3. Closed-Loop Contact Force Error & PI Integrator *)
rPantoForceError_N := rPantoTargetForce_N - rVotedPantoForce_N;
rPantoForceIntegral_Ns := rPantoForceIntegral_Ns + (rPantoForceError_N * T_CYCLE_SEC);
rPantoForceIntegral_Ns := MAX(-150.0, MIN(150.0, rPantoForceIntegral_Ns));

(* 4. Active Pneumatic Pressure Command Generation *)
(* P_bellows = (F_target - F_aero + PI_feedback + F_static_balance) / A_bellows *)
rScratchAccum := rPantoTargetForce_N - rPantoAeroUplift_N + (rKp_PantoForce * rPantoForceError_N) + (rKi_PantoForce * rPantoForceIntegral_Ns) + 70.0;
rPantoOutputPressure_bar := (rScratchAccum / (PANTO_BELLOWS_AREA_M2 * 100000.0));
rPantoBellowsPressure_bar := MAX(1.20, MIN(4.50, rPantoOutputPressure_bar));

(* ============================================================================================== *)
(* PHASE 7: BLENDED REGENERATIVE / ELECTRO-PNEUMATIC BRAKING & DYNAMIC AXLE LOAD REDISTRIBUTION   *)
(* Inertial Weight Transfer Pitch Moment Balancing & Regenerative Priority Management             *)
(* ============================================================================================== *)

(* 1. Master Trainset Deceleration Force Demand [kN] *)
IF bBrakingEnableCmd OR (rDriverBrakeNotch_pct > 0.5) THEN
    rTotalBrakingDemand_kN := (rDriverBrakeNotch_pct / 100.0) * (TRAIN_MASS_FULL_KG * 0.001 * 1.20);
ELSE
    rTotalBrakingDemand_kN := 0.0;
END_IF;

(* 2. Dynamic Longitudinal Axle Load Shift (Weight Transfer Pitch Moment) *)
(* Delta_Fz = (M_car / 2) * abs(a_train) * (h_cg / L_wheelbase) *)
rAxleWeightShift_kN := (TRAIN_MASS_FULL_KG / 8.0) * ABS(rTrainAcceleration_ms2) * (CARBODY_CG_HEIGHT_M / BOGIE_WHEELBASE_M) * 0.001;
rAxleWeightShift_kN := MIN(45.0, rAxleWeightShift_kN);

IF rTrainAcceleration_ms2 < -0.05 THEN
    (* Train Decelerating: Leading axle pitch down (loaded), trailing axle pitch up (unloaded) *)
    rAxle1_DynamicLoad_kN := BOGIE_AXLE_LOAD_STAT_KN + rAxleWeightShift_kN;
    rAxle2_DynamicLoad_kN := MAX(45.0, BOGIE_AXLE_LOAD_STAT_KN - rAxleWeightShift_kN);
ELSIF rTrainAcceleration_ms2 > 0.05 THEN
    (* Train Accelerating: Leading axle pitch up (unloaded), trailing axle pitch down (loaded) *)
    rAxle1_DynamicLoad_kN := MAX(45.0, BOGIE_AXLE_LOAD_STAT_KN - rAxleWeightShift_kN);
    rAxle2_DynamicLoad_kN := BOGIE_AXLE_LOAD_STAT_KN + rAxleWeightShift_kN;
ELSE
    rAxle1_DynamicLoad_kN := BOGIE_AXLE_LOAD_STAT_KN;
    rAxle2_DynamicLoad_kN := BOGIE_AXLE_LOAD_STAT_KN;
END_IF;

(* 3. Priority 1: Regenerative Electro-Dynamic (ED) Braking Allocation *)
IF rTrainSpeed_ms > 1.5 THEN
    (* Maximum regenerative inverter power = 4x 1200 kW = 4800 kW *)
    rED_BrakeAvailable_kN := MIN(rTotalBrakingDemand_kN, 4800.0 / rTrainSpeed_ms);
ELSE
    (* Fade dynamic brake linearly below 5.4 km/h to avoid zero-crossing inverter cogging *)
    rED_BrakeAvailable_kN := rTotalBrakingDemand_kN * (rTrainSpeed_ms / 1.5);
END_IF;

(* Constrain ED braking to available adhesion envelope *)
rED_BrakeAvailable_kN := MIN(rED_BrakeAvailable_kN, rObservedAdhesionCoeff * (rAxle1_DynamicLoad_kN + rAxle2_DynamicLoad_kN));
rED_BrakeDelivered_kN := MAX(0.0, rED_BrakeAvailable_kN);
rRegenerativeBrakeTorque_kNm := (rED_BrakeDelivered_kN * WHEEL_RADIUS_NOM_M) / GEAR_RATIO;

(* 4. Priority 2: Electro-Pneumatic (EP) Friction Braking Shortfall Supplement *)
rEP_BrakeRequired_kN := MAX(0.0, rTotalBrakingDemand_kN - rED_BrakeDelivered_kN);

(* Dynamic Normal Load Proportional Allocation per Axle to Prevent Premature Skid *)
rScratchAccum := rAxle1_DynamicLoad_kN + rAxle2_DynamicLoad_kN;
IF rScratchAccum > 10.0 THEN
    rAxle1_BrakeForce_Target_kN := rEP_BrakeRequired_kN * (rAxle1_DynamicLoad_kN / rScratchAccum);
    rAxle2_BrakeForce_Target_kN := rEP_BrakeRequired_kN * (rAxle2_DynamicLoad_kN / rScratchAccum);
ELSE
    rAxle1_BrakeForce_Target_kN := rEP_BrakeRequired_kN * 0.5;
    rAxle2_BrakeForce_Target_kN := rEP_BrakeRequired_kN * 0.5;
END_IF;

(* Convert Target Braking Force to Bogie Brake Cylinder Pneumatic Pressures [bar] *)
(* Max cylinder pressure 3.80 bar produces ~38 kN per axle *)
rBrakeCylinder_SP_Axle1_bar := (rAxle1_BrakeForce_Target_kN / 38.0) * 3.80;
rBrakeCylinder_SP_Axle1_bar := MAX(0.0, MIN(3.80, rBrakeCylinder_SP_Axle1_bar));

rBrakeCylinder_SP_Axle2_bar := (rAxle2_BrakeForce_Target_kN / 38.0) * 3.80;
rBrakeCylinder_SP_Axle2_bar := MAX(0.0, MIN(3.80, rBrakeCylinder_SP_Axle2_bar));

rPneumaticBrakePressure_SP_bar := MAX(rBrakeCylinder_SP_Axle1_bar, rBrakeCylinder_SP_Axle2_bar);
'''
