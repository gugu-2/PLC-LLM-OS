# st_part3_logic_mpc_fsm.py

def get_logic_mpc_fsm():
    return """
(* ========================================================================================= *)
(* SEGMENT 8: COMPLETE STATE-SPACE MODEL PROPAGATION & OBSERVER UPDATE                       *)
(* ========================================================================================= *)
(* Prepare Current Process Measurement Vector y_meas *)
aY_Meas[1] := rVotedCavityTemp_degC;
aY_Meas[2] := rVotedWindowTemp_degC;
aY_Meas[3] := (rEstimatedZnVaporYield_mol_s * 65.38) / (rQuenchGasCurtainFlow_Nm3_h * 0.000277 + 0.001);
aY_Meas[4] := rVotedCavityTemp_degC - (rQuenchCoolingRate_K_s * 0.008);
IF aY_Meas[4] < 200.0 THEN aY_Meas[4] := 200.0; END_IF;

(* Prepare Current Actuator Vector u_ctrl *)
aU_Ctrl[1] := rAttenuatorPos_Actual_pct;
aU_Ctrl[2] := rQuenchValve_Actual_pct;
aU_Ctrl[3] := rWindowSweepValve_Actual_pct;

(* Prepare Disturbance Vector d_dist *)
aD_Dist[1] := rSolarDirectNormalIrradiance_W_m2 - 950.0;
aD_Dist[2] := rZnO_FeedRate_kg_h - 120.0;
aD_Dist[3] := 2.5; (* Nominal wind cooling speed [m/s] *)

(* Compute Estimated Process Output Vector y_hat = C_disc * x_hat *)
aY_Est[1] := aC_Disc[1, 1]*aX_Est[1] + aC_Disc[1, 2]*aX_Est[2] + aC_Disc[1, 3]*aX_Est[3] + aC_Disc[1, 4]*aX_Est[4];
aY_Est[2] := aC_Disc[2, 1]*aX_Est[1] + aC_Disc[2, 2]*aX_Est[2] + aC_Disc[2, 3]*aX_Est[3] + aC_Disc[2, 4]*aX_Est[4];
aY_Est[3] := aC_Disc[3, 1]*aX_Est[1] + aC_Disc[3, 2]*aX_Est[2] + aC_Disc[3, 3]*aX_Est[3] + aC_Disc[3, 4]*aX_Est[4];
aY_Est[4] := aC_Disc[4, 1]*aX_Est[1] + aC_Disc[4, 2]*aX_Est[2] + aC_Disc[4, 3]*aX_Est[3] + aC_Disc[4, 4]*aX_Est[4];

(* One-Step Ahead State Prediction: x_pred = A_disc * x_hat + B_disc * u + Bd_disc * d *)
aX_Pred[1] := (aA_Disc[1, 1]*aX_Est[1] + aA_Disc[1, 2]*aX_Est[2] + aA_Disc[1, 3]*aX_Est[3] + aA_Disc[1, 4]*aX_Est[4]) +
              (aB_Disc[1, 1]*aU_Ctrl[1] + aB_Disc[1, 2]*aU_Ctrl[2] + aB_Disc[1, 3]*aU_Ctrl[3]) +
              (aBd_Disc[1, 1]*aD_Dist[1] + aBd_Disc[1, 2]*aD_Dist[2] + aBd_Disc[1, 3]*aD_Dist[3]);

aX_Pred[2] := (aA_Disc[2, 1]*aX_Est[1] + aA_Disc[2, 2]*aX_Est[2] + aA_Disc[2, 3]*aX_Est[3] + aA_Disc[2, 4]*aX_Est[4]) +
              (aB_Disc[2, 1]*aU_Ctrl[1] + aB_Disc[2, 2]*aU_Ctrl[2] + aB_Disc[2, 3]*aU_Ctrl[3]) +
              (aBd_Disc[2, 1]*aD_Dist[1] + aBd_Disc[2, 2]*aD_Dist[2] + aBd_Disc[2, 3]*aD_Dist[3]);

aX_Pred[3] := (aA_Disc[3, 1]*aX_Est[1] + aA_Disc[3, 2]*aX_Est[2] + aA_Disc[3, 3]*aX_Est[3] + aA_Disc[3, 4]*aX_Est[4]) +
              (aB_Disc[3, 1]*aU_Ctrl[1] + aB_Disc[3, 2]*aU_Ctrl[2] + aB_Disc[3, 3]*aU_Ctrl[3]) +
              (aBd_Disc[3, 1]*aD_Dist[1] + aBd_Disc[3, 2]*aD_Dist[2] + aBd_Disc[3, 3]*aD_Dist[3]);

aX_Pred[4] := (aA_Disc[4, 1]*aX_Est[1] + aA_Disc[4, 2]*aX_Est[2] + aA_Disc[4, 3]*aX_Est[3] + aA_Disc[4, 4]*aX_Est[4]) +
              (aB_Disc[4, 1]*aU_Ctrl[1] + aB_Disc[4, 2]*aU_Ctrl[2] + aB_Disc[4, 3]*aU_Ctrl[3]) +
              (aBd_Disc[4, 1]*aD_Dist[1] + aBd_Disc[4, 2]*aD_Dist[2] + aBd_Disc[4, 3]*aD_Dist[3]);

(* Observer Measurement Innovation Update: x_hat = x_pred + L * (y_meas - y_est) *)
aX_Est[1] := aX_Pred[1] + aL_Obs[1, 1]*(aY_Meas[1] - aY_Est[1]) + aL_Obs[1, 2]*(aY_Meas[2] - aY_Est[2]) + aL_Obs[1, 3]*(aY_Meas[3] - aY_Est[3]) + aL_Obs[1, 4]*(aY_Meas[4] - aY_Est[4]);
aX_Est[2] := aX_Pred[2] + aL_Obs[2, 1]*(aY_Meas[1] - aY_Est[1]) + aL_Obs[2, 2]*(aY_Meas[2] - aY_Est[2]) + aL_Obs[2, 3]*(aY_Meas[3] - aY_Est[3]) + aL_Obs[2, 4]*(aY_Meas[4] - aY_Est[4]);
aX_Est[3] := aX_Pred[3] + aL_Obs[3, 1]*(aY_Meas[1] - aY_Est[1]) + aL_Obs[3, 2]*(aY_Meas[2] - aY_Est[2]) + aL_Obs[3, 3]*(aY_Meas[3] - aY_Est[3]) + aL_Obs[3, 4]*(aY_Meas[4] - aY_Est[4]);
aX_Est[4] := aX_Pred[4] + aL_Obs[4, 1]*(aY_Meas[1] - aY_Est[1]) + aL_Obs[4, 2]*(aY_Meas[2] - aY_Est[2]) + aL_Obs[4, 3]*(aY_Meas[3] - aY_Est[3]) + aL_Obs[4, 4]*(aY_Meas[4] - aY_Est[4]);

(* ========================================================================================= *)
(* SEGMENT 9: CONSTRAINED MODEL PREDICTIVE CONTROL (MPC) QUADRATIC PROGRAMMING SOLVER        *)
(* ========================================================================================= *)
(* Populate Condensed Hessian Matrix H (6x6) = S_u^T * Q_bar * S_u + R_bar                   *)
(* Diagonal terms dominate due to decoupled fast actuators *)
aHessian[1, 1] := aB_Disc[1, 1]*aQ_Weight[1, 1]*aB_Disc[1, 1] + aB_Disc[2, 1]*aQ_Weight[2, 2]*aB_Disc[2, 1] + aR_Weight[1, 1];
aHessian[1, 2] := aB_Disc[1, 1]*aQ_Weight[1, 1]*aB_Disc[1, 2] + aB_Disc[2, 1]*aQ_Weight[2, 2]*aB_Disc[2, 2];
aHessian[1, 3] := aB_Disc[1, 1]*aQ_Weight[1, 1]*aB_Disc[1, 3] + aB_Disc[2, 1]*aQ_Weight[2, 2]*aB_Disc[2, 3];
aHessian[1, 4] := 0.25 * aHessian[1, 1]; aHessian[1, 5] := 0.0; aHessian[1, 6] := 0.0;

aHessian[2, 1] := aHessian[1, 2];
aHessian[2, 2] := aB_Disc[4, 2]*aQ_Weight[4, 4]*aB_Disc[4, 2] + aB_Disc[3, 2]*aQ_Weight[3, 3]*aB_Disc[3, 2] + aR_Weight[2, 2];
aHessian[2, 3] := aB_Disc[4, 2]*aQ_Weight[4, 4]*aB_Disc[4, 3] + aB_Disc[3, 2]*aQ_Weight[3, 3]*aB_Disc[3, 3];
aHessian[2, 4] := 0.0; aHessian[2, 5] := 0.25 * aHessian[2, 2]; aHessian[2, 6] := 0.0;

aHessian[3, 1] := aHessian[1, 3];
aHessian[3, 2] := aHessian[2, 3];
aHessian[3, 3] := aB_Disc[2, 3]*aQ_Weight[2, 2]*aB_Disc[2, 3] + aR_Weight[3, 3];
aHessian[3, 4] := 0.0; aHessian[3, 5] := 0.0; aHessian[3, 6] := 0.25 * aHessian[3, 3];

aHessian[4, 4] := aHessian[1, 1]; aHessian[4, 5] := aHessian[1, 2]; aHessian[4, 6] := aHessian[1, 3];
aHessian[5, 4] := aHessian[2, 1]; aHessian[5, 5] := aHessian[2, 2]; aHessian[5, 6] := aHessian[2, 3];
aHessian[6, 4] := aHessian[3, 1]; aHessian[6, 5] := aHessian[3, 2]; aHessian[6, 6] := aHessian[3, 3];

(* Compute Linear Cost Gradient Vector g = S_u^T * Q_bar * (x_pred - y_ref) *)
aGrad[1] := aB_Disc[1, 1]*aQ_Weight[1, 1]*(aX_Est[1] - aY_Setpoint[1]) + aB_Disc[2, 1]*aQ_Weight[2, 2]*(aX_Est[2] - aY_Setpoint[2]);
aGrad[2] := aB_Disc[4, 2]*aQ_Weight[4, 4]*(aX_Est[4] - aY_Setpoint[4]) + aB_Disc[3, 2]*aQ_Weight[3, 3]*(aX_Est[3] - aY_Setpoint[3]);
aGrad[3] := aB_Disc[2, 3]*aQ_Weight[2, 2]*(aX_Est[2] - aY_Setpoint[2]);
aGrad[4] := 0.5 * aGrad[1];
aGrad[5] := 0.5 * aGrad[2];
aGrad[6] := 0.5 * aGrad[3];

(* Initialize Decision Vector DeltaU with previous warm start *)
aDeltaU_Opt[1] := aDeltaU_Prev[1] * 0.5;
aDeltaU_Opt[2] := aDeltaU_Prev[2] * 0.5;
aDeltaU_Opt[3] := aDeltaU_Prev[3] * 0.5;
aDeltaU_Opt[4] := 0.0;
aDeltaU_Opt[5] := 0.0;
aDeltaU_Opt[6] := 0.0;

(* Deterministic Projected Gradient Descent Iteration Loop *)
FOR iMPC_Iteration := 1 TO iMPC_MaxIter DO
    (* Gradient Descent Step: DeltaU := DeltaU - alpha * (H * DeltaU + g) *)
    aDeltaU_Opt[1] := aDeltaU_Opt[1] - rMPC_StepSize * (aHessian[1, 1]*aDeltaU_Opt[1] + aHessian[1, 2]*aDeltaU_Opt[2] + aHessian[1, 3]*aDeltaU_Opt[3] + aGrad[1]);
    aDeltaU_Opt[2] := aDeltaU_Opt[2] - rMPC_StepSize * (aHessian[2, 1]*aDeltaU_Opt[1] + aHessian[2, 2]*aDeltaU_Opt[2] + aHessian[2, 3]*aDeltaU_Opt[3] + aGrad[2]);
    aDeltaU_Opt[3] := aDeltaU_Opt[3] - rMPC_StepSize * (aHessian[3, 1]*aDeltaU_Opt[1] + aHessian[3, 2]*aDeltaU_Opt[2] + aHessian[3, 3]*aDeltaU_Opt[3] + aGrad[3]);

    (* Projection onto Slew Constraints [DeltaU_Min, DeltaU_Max] *)
    IF aDeltaU_Opt[1] < aDeltaU_Min[1] THEN aDeltaU_Opt[1] := aDeltaU_Min[1]; END_IF;
    IF aDeltaU_Opt[1] > aDeltaU_Max[1] THEN aDeltaU_Opt[1] := aDeltaU_Max[1]; END_IF;
    IF aDeltaU_Opt[2] < aDeltaU_Min[2] THEN aDeltaU_Opt[2] := aDeltaU_Min[2]; END_IF;
    IF aDeltaU_Opt[2] > aDeltaU_Max[2] THEN aDeltaU_Opt[2] := aDeltaU_Max[2]; END_IF;
    IF aDeltaU_Opt[3] < aDeltaU_Min[3] THEN aDeltaU_Opt[3] := aDeltaU_Min[3]; END_IF;
    IF aDeltaU_Opt[3] > aDeltaU_Max[3] THEN aDeltaU_Opt[3] := aDeltaU_Max[3]; END_IF;

    (* Projection onto Absolute Actuator Bounds [U_Min, U_Max] *)
    IF (aU_Ctrl[1] + aDeltaU_Opt[1]) < aU_Min[1] THEN aDeltaU_Opt[1] := aU_Min[1] - aU_Ctrl[1]; END_IF;
    IF (aU_Ctrl[1] + aDeltaU_Opt[1]) > aU_Max[1] THEN aDeltaU_Opt[1] := aU_Max[1] - aU_Ctrl[1]; END_IF;
    IF (aU_Ctrl[2] + aDeltaU_Opt[2]) < aU_Min[2] THEN aDeltaU_Opt[2] := aU_Min[2] - aU_Ctrl[2]; END_IF;
    IF (aU_Ctrl[2] + aDeltaU_Opt[2]) > aU_Max[2] THEN aDeltaU_Opt[2] := aU_Max[2] - aU_Ctrl[2]; END_IF;
    IF (aU_Ctrl[3] + aDeltaU_Opt[3]) < aU_Min[3] THEN aDeltaU_Opt[3] := aU_Min[3] - aU_Ctrl[3]; END_IF;
    IF (aU_Ctrl[3] + aDeltaU_Opt[3]) > aU_Max[3] THEN aDeltaU_Opt[3] := aU_Max[3] - aU_Ctrl[3]; END_IF;
END_FOR;

(* Store solution for next cycle warm start *)
aDeltaU_Prev[1] := aDeltaU_Opt[1];
aDeltaU_Prev[2] := aDeltaU_Opt[2];
aDeltaU_Prev[3] := aDeltaU_Opt[3];

(* ========================================================================================= *)
(* SEGMENT 10: HELIOSTAT AIMPOINT DISTRIBUTION & RADIANT HEAT BALANCING                      *)
(* ========================================================================================= *)
(* Fast cloud transient detection: d(DNI)/dt *)
rCloudTransientDropRate_pct_s := ((rPrevSolarIrradiance_W_m2 - rSolarDirectNormalIrradiance_W_m2) / (rCycleTime_s + 0.001)) / 10.0;
rPrevSolarIrradiance_W_m2 := rSolarDirectNormalIrradiance_W_m2;

IF rCloudTransientDropRate_pct_s > 15.0 THEN
    (* Severe Cloud Transient: Fast feedforward opening of attenuator to maintain temperature *)
    rAttenuatorFeedforwardCmd_pct := 18.0;
    wSystemWarningWord := wSystemWarningWord OR 16#0008; (* Cloud transient detected *)
ELSE
    rAttenuatorFeedforwardCmd_pct := 0.0;
END_IF;

(* Multi-faceted heliostat aimpoint trimming to mitigate circumferential hot-spots *)
(* Calculate aimpoint trimming offsets based on pyrometer channel deviations *)
IF bCavityTemp_A_Healthy AND bCavityTemp_B_Healthy AND bCavityTemp_C_Healthy THEN
    rHeliostatAimingTrim_X_mrad := (rCavityPyrometerTemp_A_degC - rCavityPyrometerTemp_B_degC) * 0.045;
    rHeliostatAimingTrim_Y_mrad := (rCavityPyrometerTemp_C_degC - rVotedCavityTemp_degC) * 0.035;
ELSE
    rHeliostatAimingTrim_X_mrad := 0.0;
    rHeliostatAimingTrim_Y_mrad := 0.0;
END_IF;

(* Clamp aimpoint trim vector to maximum safe focal offset of +/- 25 mrad *)
IF rHeliostatAimingTrim_X_mrad > 25.0 THEN rHeliostatAimingTrim_X_mrad := 25.0; END_IF;
IF rHeliostatAimingTrim_X_mrad < -25.0 THEN rHeliostatAimingTrim_X_mrad := -25.0; END_IF;
IF rHeliostatAimingTrim_Y_mrad > 25.0 THEN rHeliostatAimingTrim_Y_mrad := 25.0; END_IF;
IF rHeliostatAimingTrim_Y_mrad < -25.0 THEN rHeliostatAimingTrim_Y_mrad := -25.0; END_IF;

(* ========================================================================================= *)
(* SEGMENT 11: MULTI-STAGE DETERMINISTIC FINITE STATE MACHINE (FSM)                          *)
(* ========================================================================================= *)
iOperationalState := iState;
rStateTimer_s := rStateTimer_s + rCycleTime_s;

CASE iState OF

    0: (* STATE 0: COLD SHUTDOWN / SYSTEM IDLE *)
        bReactorOperational := FALSE;
        bFastOpticalShutterClose := TRUE;
        bHeliostatDefocusCommand := TRUE;
        rApertureAttenuatorPosition_pct := 0.0;
        rZnO_FeederSpeedCmd_pct := 0.0;
        rWindowPurgeValveCmd_pct := 0.0;
        rQuenchCurtainValveCmd_pct := 0.0;

        IF bSystemEnable AND (NOT bTripLatched) THEN
            rStateTimer_s := 0.0;
            iState := 10; (* Transition to Pre-Purge *)
        END_IF;

    10: (* STATE 10: PRE-PURGE & INERTIZATION *)
        (* Displace all atmospheric oxygen with high-purity argon (O2 target < 10 ppm) *)
        bReactorOperational := FALSE;
        bFastOpticalShutterClose := TRUE;
        bHeliostatDefocusCommand := TRUE;
        rWindowPurgeValveCmd_pct := 65.0;
        rQuenchCurtainValveCmd_pct := 40.0;
        rApertureAttenuatorPosition_pct := 0.0;
        rZnO_FeederSpeedCmd_pct := 0.0;

        IF rStateTimer_s >= 60.0 THEN
            (* Pre-purge complete, verify internal reactor pressure *)
            IF (rReactorInternalPress_bar >= 0.95) AND (rReactorInternalPress_bar <= 1.15) THEN
                rStateTimer_s := 0.0;
                iState := 20; (* Transition to Vortex Sweep Proof *)
            ELSE
                wSystemWarningWord := wSystemWarningWord OR 16#0010; (* Purge pressure mismatch *)
            END_IF;
        END_IF;

    20: (* STATE 20: QUARTZ SWEEP & AERODYNAMIC CURTAIN VALIDATION *)
        bReactorOperational := FALSE;
        bFastOpticalShutterClose := TRUE;
        bHeliostatDefocusCommand := TRUE;
        rWindowPurgeValveCmd_pct := 80.0;
        rQuenchCurtainValveCmd_pct := 85.0;

        (* Check supersonic quench curtain velocity > 180 m/s and swirl efficiency *)
        IF (rQuenchGasCurtainVelocity_m_s >= 180.0) AND (rWindowSweepGasFlow_Nm3_h >= 120.0) THEN
            IF rStateTimer_s >= 15.0 THEN
                rStateTimer_s := 0.0;
                iState := 30; (* Transition to Heliostat Alignment *)
            END_IF;
        END_IF;

    30: (* STATE 30: HELIOSTAT ALIGNMENT & APERTURE CALIBRATION *)
        bReactorOperational := FALSE;
        bFastOpticalShutterClose := FALSE; (* Open mechanical shutter *)
        bHeliostatDefocusCommand := FALSE; (* Allow heliostat tracking *)
        rApertureAttenuatorPosition_pct := 5.0; (* Slight beam admittance *)
        rWindowPurgeValveCmd_pct := 60.0;
        rQuenchCurtainValveCmd_pct := 60.0;

        IF bHeliostatFieldReady AND (rSolarDirectNormalIrradiance_W_m2 >= 450.0) THEN
            IF rStateTimer_s >= 20.0 THEN
                rStateTimer_s := 0.0;
                iState := 40; (* Transition to Controlled Thermal Ramp *)
            END_IF;
        END_IF;

    40: (* STATE 40: CONTROLLED THERMAL RAMPING (< 10 DEG C / MIN) *)
        bReactorOperational := TRUE;
        bFastOpticalShutterClose := FALSE;
        bHeliostatDefocusCommand := FALSE;
        rWindowPurgeValveCmd_pct := 60.0;
        rQuenchCurtainValveCmd_pct := 60.0;
        rZnO_FeederSpeedCmd_pct := 0.0; (* Feeder stopped during pre-heat *)

        (* Slew attenuator open gradually to ramp cavity temperature *)
        IF rVotedCavityTemp_degC < 1200.0 THEN
            rApertureAttenuatorPosition_pct := 10.0 + (rStateTimer_s * 0.05);
            IF rApertureAttenuatorPosition_pct > 45.0 THEN rApertureAttenuatorPosition_pct := 45.0; END_IF;
        ELSE
            rStateTimer_s := 0.0;
            iState := 50; (* Transition to Subcritical Redox Conditioning *)
        END_IF;

    50: (* STATE 50: SUBCRITICAL REDOX CONDITIONING (1,200 TO 1,650 DEG C) *)
        bReactorOperational := TRUE;
        bFastOpticalShutterClose := FALSE;
        bHeliostatDefocusCommand := FALSE;
        rWindowPurgeValveCmd_pct := 75.0;
        rQuenchCurtainValveCmd_pct := 75.0;
        rZnO_FeederSpeedCmd_pct := 15.0; (* Initial baseline seed feed *)

        IF rVotedCavityTemp_degC < 1650.0 THEN
            rApertureAttenuatorPosition_pct := 45.0 + (rStateTimer_s * 0.04);
            IF rApertureAttenuatorPosition_pct > 75.0 THEN rApertureAttenuatorPosition_pct := 75.0; END_IF;
        ELSE
            rStateTimer_s := 0.0;
            iState := 60; (* Transition to Supercritical Dissociation *)
        END_IF;

    60: (* STATE 60: SUPERCRITICAL DISSOCIATION TRANSITION (1,650 TO 1,800 DEG C) *)
        bReactorOperational := TRUE;
        bFastOpticalShutterClose := FALSE;
        bHeliostatDefocusCommand := FALSE;
        rWindowPurgeValveCmd_pct := 90.0;
        rQuenchCurtainValveCmd_pct := 95.0; (* Arm supersonic quench fully *)
        rZnO_FeederSpeedCmd_pct := 40.0;

        IF rVotedCavityTemp_degC >= 1750.0 THEN
            rStateTimer_s := 0.0;
            iState := 70; (* Transition to Full Steady-State Water Splitting *)
        END_IF;

    70: (* STATE 70: FULL-CAPACITY SOLAR WATER SPLITTING (1,800 DEG C STEADY-STATE) *)
        bReactorOperational := TRUE;
        bFastOpticalShutterClose := FALSE;
        bHeliostatDefocusCommand := FALSE;

        (* Enable MPC optimization control increments *)
        rApertureAttenuatorPosition_pct := aU_Ctrl[1] + aDeltaU_Opt[1] + rAttenuatorFeedforwardCmd_pct;
        rQuenchCurtainValveCmd_pct := aU_Ctrl[2] + aDeltaU_Opt[2];
        rWindowPurgeValveCmd_pct := aU_Ctrl[3] + aDeltaU_Opt[3];
        rZnO_FeederSpeedCmd_pct := 80.0;

        (* Check for rapid solar DNI drops or cloud occlusion *)
        IF rSolarDirectNormalIrradiance_W_m2 < 350.0 THEN
            rStateTimer_s := 0.0;
            iState := 80; (* Transition to Cloud Transient Attenuation *)
        END_IF;

    80: (* STATE 80: CLOUD TRANSIENT DYNAMIC ATTENUATION *)
        bReactorOperational := TRUE;
        bFastOpticalShutterClose := FALSE;
        bHeliostatDefocusCommand := FALSE;
        rZnO_FeederSpeedCmd_pct := 25.0; (* Throttled feed to avoid bed chilling *)
        rApertureAttenuatorPosition_pct := 100.0; (* Wide open to capture diffuse flux *)

        IF rSolarDirectNormalIrradiance_W_m2 >= 550.0 THEN
            rStateTimer_s := 0.0;
            iState := 70; (* Recover to Full Capacity *)
        ELSIF rStateTimer_s >= 180.0 THEN
            (* Sustained cloud cover > 3 minutes -> Controlled De-ramp *)
            rStateTimer_s := 0.0;
            iState := 90;
        END_IF;

    90: (* STATE 90: CONTROLLED THERMAL DE-RAMPING (< 15 DEG C / MIN) *)
        bReactorOperational := TRUE;
        bFastOpticalShutterClose := FALSE;
        bHeliostatDefocusCommand := FALSE;
        rZnO_FeederSpeedCmd_pct := 0.0; (* Stop powder feed *)
        rWindowPurgeValveCmd_pct := 70.0;
        rQuenchCurtainValveCmd_pct := 80.0;

        (* Gradually close attenuator to avoid thermal shock to SiC cavity *)
        IF rApertureAttenuatorPosition_pct > 5.0 THEN
            rApertureAttenuatorPosition_pct := rApertureAttenuatorPosition_pct - (rCycleTime_s * 1.5);
            IF rApertureAttenuatorPosition_pct < 0.0 THEN rApertureAttenuatorPosition_pct := 0.0; END_IF;
        END_IF;

        IF rVotedCavityTemp_degC <= 450.0 THEN
            rStateTimer_s := 0.0;
            iState := 0; (* Safe Cold Shutdown Reached *)
        END_IF;

    100: (* STATE 100: EMERGENCY BEAM DEFOCUS & FAST SHUTTER TRIP *)
        bReactorOperational := FALSE;
        bFastOpticalShutterClose := TRUE;  (* Sub-50ms pneumatic shut *)
        bHeliostatDefocusCommand := TRUE;  (* Emergency heliostat slew to stow *)
        rApertureAttenuatorPosition_pct := 0.0;
        rZnO_FeederSpeedCmd_pct := 0.0;
        rWindowPurgeValveCmd_pct := 100.0; (* Maximally purge window to prevent vapor deposit *)
        rQuenchCurtainValveCmd_pct := 100.0;(* Maximally quench reactor to freeze products *)

        IF rStateTimer_s >= 45.0 THEN
            rStateTimer_s := 0.0;
            iState := 110; (* Transition to Post-Trip Purge Containment *)
        END_IF;

    110: (* STATE 110: FAULT CONTAINMENT & POST-TRIP PURGE *)
        bReactorOperational := FALSE;
        bFastOpticalShutterClose := TRUE;
        bHeliostatDefocusCommand := TRUE;
        rApertureAttenuatorPosition_pct := 0.0;
        rZnO_FeederSpeedCmd_pct := 0.0;
        rWindowPurgeValveCmd_pct := 40.0;
        rQuenchCurtainValveCmd_pct := 30.0;

        (* Latch in fault containment until operator reset and permissive cleared *)
        IF NOT bTripLatched AND (rVotedCavityTemp_degC < 300.0) THEN
            rStateTimer_s := 0.0;
            iState := 0;
        END_IF;

END_CASE;

(* ========================================================================================= *)
(* SEGMENT 12: ACTUATOR RATE LIMITERS, ANTI-WINDUP & OUTPUT MAPPING                          *)
(* ========================================================================================= *)
(* Rate Limit Attenuator *)
IF (rApertureAttenuatorPosition_pct - rAttenuatorPos_Actual_pct) > (rMaxSlew_Attenuator_pct_s * rCycleTime_s) THEN
    rAttenuatorPos_Actual_pct := rAttenuatorPos_Actual_pct + (rMaxSlew_Attenuator_pct_s * rCycleTime_s);
ELSIF (rAttenuatorPos_Actual_pct - rApertureAttenuatorPosition_pct) > (rMaxSlew_Attenuator_pct_s * rCycleTime_s) THEN
    rAttenuatorPos_Actual_pct := rAttenuatorPos_Actual_pct - (rMaxSlew_Attenuator_pct_s * rCycleTime_s);
ELSE
    rAttenuatorPos_Actual_pct := rApertureAttenuatorPosition_pct;
END_IF;
IF rAttenuatorPos_Actual_pct < 0.0 THEN rAttenuatorPos_Actual_pct := 0.0; END_IF;
IF rAttenuatorPos_Actual_pct > 100.0 THEN rAttenuatorPos_Actual_pct := 100.0; END_IF;

(* Rate Limit Quench Valve *)
IF (rQuenchCurtainValveCmd_pct - rQuenchValve_Actual_pct) > (rMaxSlew_QuenchValve_pct_s * rCycleTime_s) THEN
    rQuenchValve_Actual_pct := rQuenchValve_Actual_pct + (rMaxSlew_QuenchValve_pct_s * rCycleTime_s);
ELSIF (rQuenchValve_Actual_pct - rQuenchCurtainValveCmd_pct) > (rMaxSlew_QuenchValve_pct_s * rCycleTime_s) THEN
    rQuenchValve_Actual_pct := rQuenchValve_Actual_pct - (rMaxSlew_QuenchValve_pct_s * rCycleTime_s);
ELSE
    rQuenchValve_Actual_pct := rQuenchCurtainValveCmd_pct;
END_IF;
IF rQuenchValve_Actual_pct < 0.0 THEN rQuenchValve_Actual_pct := 0.0; END_IF;
IF rQuenchValve_Actual_pct > 100.0 THEN rQuenchValve_Actual_pct := 100.0; END_IF;

(* Rate Limit Window Sweep Valve *)
IF (rWindowPurgeValveCmd_pct - rWindowSweepValve_Actual_pct) > (rMaxSlew_WindowValve_pct_s * rCycleTime_s) THEN
    rWindowSweepValve_Actual_pct := rWindowSweepValve_Actual_pct + (rMaxSlew_WindowValve_pct_s * rCycleTime_s);
ELSIF (rWindowSweepValve_Actual_pct - rWindowPurgeValveCmd_pct) > (rMaxSlew_WindowValve_pct_s * rCycleTime_s) THEN
    rWindowSweepValve_Actual_pct := rWindowSweepValve_Actual_pct - (rMaxSlew_WindowValve_pct_s * rCycleTime_s);
ELSE
    rWindowSweepValve_Actual_pct := rWindowPurgeValveCmd_pct;
END_IF;
IF rWindowSweepValve_Actual_pct < 0.0 THEN rWindowSweepValve_Actual_pct := 0.0; END_IF;
IF rWindowSweepValve_Actual_pct > 100.0 THEN rWindowSweepValve_Actual_pct := 100.0; END_IF;

(* Rate Limit ZnO Feeder *)
IF (rZnO_FeederSpeedCmd_pct - rZnO_Feeder_Actual_pct) > (rMaxSlew_Feeder_pct_s * rCycleTime_s) THEN
    rZnO_Feeder_Actual_pct := rZnO_Feeder_Actual_pct + (rMaxSlew_Feeder_pct_s * rCycleTime_s);
ELSIF (rZnO_Feeder_Actual_pct - rZnO_FeederSpeedCmd_pct) > (rMaxSlew_Feeder_pct_s * rCycleTime_s) THEN
    rZnO_Feeder_Actual_pct := rZnO_Feeder_Actual_pct - (rMaxSlew_Feeder_pct_s * rCycleTime_s);
ELSE
    rZnO_Feeder_Actual_pct := rZnO_FeederSpeedCmd_pct;
END_IF;
IF rZnO_Feeder_Actual_pct < 0.0 THEN rZnO_Feeder_Actual_pct := 0.0; END_IF;
IF rZnO_Feeder_Actual_pct > 100.0 THEN rZnO_Feeder_Actual_pct := 100.0; END_IF;

(* Map to Final Outputs *)
rApertureAttenuatorPosition_pct := rAttenuatorPos_Actual_pct;
rQuenchCurtainValveCmd_pct := rQuenchValve_Actual_pct;
rWindowPurgeValveCmd_pct := rWindowSweepValve_Actual_pct;
rZnO_FeederSpeedCmd_pct := rZnO_Feeder_Actual_pct;

(* ========================================================================================= *)
(* SEGMENT 13: ISA-18.2 ALARM PRIORITY MATRIX & FIRST-OUT TRIP LATCHING                      *)
(* ========================================================================================= *)
(* Alarm Priority 1: CRITICAL TRIPS (Immediate Shutter Drop & Heliostat Defocus) *)
IF rVotedCavityTemp_degC > 1880.0 THEN
    bTripLatched := TRUE;
    bFastOpticalShutterClose := TRUE;
    bHeliostatDefocusCommand := TRUE;
    IF NOT bFirstOutRecorded THEN
        dwAlarmWordFirstOut := 16#00000004; (* Bit 2: Cavity Over-temperature Trip > 1880 C *)
        bFirstOutRecorded := TRUE;
    END_IF;
    iState := 100;
END_IF;

IF rVotedWindowTemp_degC > 920.0 THEN
    bTripLatched := TRUE;
    bFastOpticalShutterClose := TRUE;
    bHeliostatDefocusCommand := TRUE;
    IF NOT bFirstOutRecorded THEN
        dwAlarmWordFirstOut := 16#00000008; (* Bit 3: Quartz Window Critical Overheat > 920 C *)
        bFirstOutRecorded := TRUE;
    END_IF;
    iState := 100;
END_IF;

IF rCeramicRefractoryStress_MPa > 88.0 THEN
    bTripLatched := TRUE;
    bFastOpticalShutterClose := TRUE;
    bHeliostatDefocusCommand := TRUE;
    IF NOT bFirstOutRecorded THEN
        dwAlarmWordFirstOut := 16#00000010; (* Bit 4: SiC Refractory Thermal Stress Breach > 88 MPa *)
        bFirstOutRecorded := TRUE;
    END_IF;
    iState := 100;
END_IF;

IF rQuartzWindowTransmissivity_pct < 65.0 THEN
    bTripLatched := TRUE;
    bFastOpticalShutterClose := TRUE;
    bHeliostatDefocusCommand := TRUE;
    IF NOT bFirstOutRecorded THEN
        dwAlarmWordFirstOut := 16#00000020; (* Bit 5: Quartz Transmissivity Critical Loss < 65% *)
        bFirstOutRecorded := TRUE;
    END_IF;
    iState := 100;
END_IF;

IF (rQuenchGasCurtainVelocity_m_s < 120.0) AND (iState >= 60) THEN
    bTripLatched := TRUE;
    bFastOpticalShutterClose := TRUE;
    bHeliostatDefocusCommand := TRUE;
    IF NOT bFirstOutRecorded THEN
        dwAlarmWordFirstOut := 16#00000040; (* Bit 6: Quench Gas Velocity Collapse < 120 m/s *)
        bFirstOutRecorded := TRUE;
    END_IF;
    iState := 100;
END_IF;

(* Pack Safety Status Word *)
wSafetyStatusWord := 16#0000;
IF bReactorOperational THEN wSafetyStatusWord := wSafetyStatusWord OR 16#0001; END_IF;
IF NOT bFastOpticalShutterClose THEN wSafetyStatusWord := wSafetyStatusWord OR 16#0002; END_IF;
IF NOT bHeliostatDefocusCommand THEN wSafetyStatusWord := wSafetyStatusWord OR 16#0004; END_IF;
IF bTripLatched THEN wSafetyStatusWord := wSafetyStatusWord OR 16#0008; END_IF;
IF bHeliostatFieldReady THEN wSafetyStatusWord := wSafetyStatusWord OR 16#0010; END_IF;

END_FUNCTION_BLOCK
"""

print("Logic MPC & FSM module ready.")
