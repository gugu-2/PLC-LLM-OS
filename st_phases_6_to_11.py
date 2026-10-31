# st_phases_6_to_11.py
# Implements Phase 6 through Phase 11 of the Function Block logic

def get_phases_6_to_11():
    return """(* ========================================================================================================== *)
(* PHASE 6: VOICE COIL Z-DRIVE & DYNAMIC CONTACT SOFT-LANDING OBSERVER                                  *)
(* ========================================================================================================== *)
(* Instantaneous Velocity & Acceleration Estimator from 10 nm Optical Scales *)
f_VCM_ActualVelocity_um_s := (f_Voted_ZPos_nm - f_VCM_Z_PrevPos_nm) / (f_SamplingTime_s * 1000.0);
f_VCM_ActualAcc_mm_s2 := (f_VCM_ActualVelocity_um_s - f_VCM_Z_PrevVel_um_s) / (f_SamplingTime_s * 1000.0);
f_VCM_Z_PrevPos_nm := f_Voted_ZPos_nm;
f_VCM_Z_PrevVel_um_s := f_VCM_ActualVelocity_um_s;

(* Dynamic Dual-Criteria Contact Impact Observer *)
IF (n_CurrentState = STATE_APPROACH_SOFT_LANDING) OR (n_CurrentState = STATE_LOOPING_TRAJECTORY) THEN
    IF (f_VCM_ActualAcc_mm_s2 <= f_TouchdownDecelThreshold_mm_s2) AND
       (f_Voted_BondForce_mN >= f_TouchdownForceThreshold_mN) THEN
        IF NOT b_ContactEventDetected THEN
            b_ContactEventDetected := TRUE;
            f_ContactTouchdownZ_nm := f_Voted_ZPos_nm;
            f_ContactInitialImpactForce_mN := f_Voted_BondForce_mN;
        END_IF;
    END_IF;
END_IF;

(* Real-Time Ball / Stitch Plastic Squash Deformation *)
IF b_ContactEventDetected AND (f_Voted_ZPos_nm >= f_ContactTouchdownZ_nm) THEN
    f_BondDeformation_um := (f_Voted_ZPos_nm - f_ContactTouchdownZ_nm) * 0.001;
ELSE
    f_BondDeformation_um := 0.0;
END_IF;

(* ========================================================================================================== *)
(* PHASE 7: WIRE LOOPING TRAJECTORY GENERATION & OPTICAL PR ALIGNMENT                                    *)
(* ========================================================================================================== *)
(* 2D Affine Die Placement Compensation Mathematics *)
f_PR_SinTheta := SIN(f_PR_OffsetTheta_mrad * 0.001);
f_PR_CosTheta := COS(f_PR_OffsetTheta_mrad * 0.001);

(* Compensate 1st Bond Die Pad Coordinates *)
f_DiePad_CorrectedX_um := f_DiePad_NominalX_um + f_PR_OffsetX_um +
                          (f_DiePad_NominalX_um * (f_PR_CosTheta - 1.0) - f_DiePad_NominalY_um * f_PR_SinTheta);
f_DiePad_CorrectedY_um := f_DiePad_NominalY_um + f_PR_OffsetY_um +
                          (f_DiePad_NominalX_um * f_PR_SinTheta + f_DiePad_NominalY_um * (f_PR_CosTheta - 1.0));

(* Compensate 2nd Bond Leadframe Pad Coordinates *)
f_LeadPad_CorrectedX_um := f_LeadPad_NominalX_um +
                           (f_LeadPad_NominalX_um * (f_PR_CosTheta - 1.0) - f_LeadPad_NominalY_um * f_PR_SinTheta);
f_LeadPad_CorrectedY_um := f_LeadPad_NominalY_um +
                           (f_LeadPad_NominalX_um * f_PR_SinTheta + f_LeadPad_NominalY_um * (f_PR_CosTheta - 1.0));

(* Multi-Kink Trajectory Interpolator for 22 Wires/Sec (~45.45 ms cycle period) *)
IF n_CurrentState = STATE_LOOPING_TRAJECTORY THEN
    (* Segment 1: Reverse Motion Plastic Kink Forming [0.0 .. 0.18 progress] *)
    IF f_Loop_ProfileProgress <= 0.18 THEN
        f_Loop_CurrentTrajZ_um := f_ContactTouchdownZ_nm * 0.001 + (f_Loop_Kink1_ReverseZ_um * (f_Loop_ProfileProgress / 0.18));
        f_Loop_CurrentTrajX_um := f_DiePad_CorrectedX_um + (f_Loop_Kink1_ReverseX_um * (f_Loop_ProfileProgress / 0.18));
        b_AirTensioner_Active := TRUE;
    (* Segment 2: Forward Crease & Kink 2 Forming [0.18 .. 0.40 progress] *)
    ELSIF f_Loop_ProfileProgress <= 0.40 THEN
        f_Loop_CurrentTrajZ_um := (f_ContactTouchdownZ_nm * 0.001 + f_Loop_Kink1_ReverseZ_um) +
                                  ((f_Loop_Kink2_ForwardZ_um - f_Loop_Kink1_ReverseZ_um) * ((f_Loop_ProfileProgress - 0.18) / 0.22));
        f_Loop_CurrentTrajX_um := (f_DiePad_CorrectedX_um + f_Loop_Kink1_ReverseX_um) +
                                  ((f_Loop_Kink2_ForwardX_um - f_Loop_Kink1_ReverseX_um) * ((f_Loop_ProfileProgress - 0.18) / 0.22));
        b_AirTensioner_Active := TRUE;
    (* Segment 3: Apex Trajectory Rise & Span Traverse [0.40 .. 0.75 progress] *)
    ELSIF f_Loop_ProfileProgress <= 0.75 THEN
        f_Loop_CurrentTrajZ_um := f_Loop_ApexHeight_um * SIN(((f_Loop_ProfileProgress - 0.40) / 0.35) * (3.1415926535 * 0.5));
        f_Loop_CurrentTrajX_um := f_DiePad_CorrectedX_um +
                                  ((f_LeadPad_CorrectedX_um - f_DiePad_CorrectedX_um) * ((f_Loop_ProfileProgress - 0.40) / 0.35));
        b_AirTensioner_Active := FALSE;
    (* Segment 4: Deceleration & Leadframe Descent [0.75 .. 1.00 progress] *)
    ELSE
        f_Loop_CurrentTrajZ_um := f_Loop_ApexHeight_um * COS(((f_Loop_ProfileProgress - 0.75) / 0.25) * (3.1415926535 * 0.5));
        f_Loop_CurrentTrajX_um := f_LeadPad_CorrectedX_um;
        b_AirTensioner_Active := FALSE;
    END_IF;
ELSE
    f_Loop_ProfileProgress := 0.0;
    f_Loop_CurrentTrajX_um := f_DiePad_CorrectedX_um;
    f_Loop_CurrentTrajZ_um := 0.0;
END_IF;

(* ========================================================================================================== *)
(* PHASE 8: WORKHOLDER VACUUM STAGE MULTI-ZONE PID HEATING CONTROL                                     *)
(* ========================================================================================================== *)
(* Zone 1 Anti-Windup PID *)
f_PID_Z1_Error := f_SetStageTemp_degC - f_StageTemp_Zone1_degC;
f_PID_Z1_Derivative := (f_PID_Z1_Error - f_PID_Z1_PrevError) / f_SamplingTime_s;
f_PID_Z1_PrevError := f_PID_Z1_Error;
f_PID_Z1_Integral := f_PID_Z1_Integral + f_PID_Stage_Ki * f_PID_Z1_Error * f_SamplingTime_s;
IF f_PID_Z1_Integral > 35.0 THEN f_PID_Z1_Integral := 35.0; ELSIF f_PID_Z1_Integral < -10.0 THEN f_PID_Z1_Integral := -10.0; END_IF;

(* Zone 2 Anti-Windup PID *)
f_PID_Z2_Error := f_SetStageTemp_degC - f_StageTemp_Zone2_degC;
f_PID_Z2_Derivative := (f_PID_Z2_Error - f_PID_Z2_PrevError) / f_SamplingTime_s;
f_PID_Z2_PrevError := f_PID_Z2_Error;
f_PID_Z2_Integral := f_PID_Z2_Integral + f_PID_Stage_Ki * f_PID_Z2_Error * f_SamplingTime_s;
IF f_PID_Z2_Integral > 35.0 THEN f_PID_Z2_Integral := 35.0; ELSIF f_PID_Z2_Integral < -10.0 THEN f_PID_Z2_Integral := -10.0; END_IF;

(* Zone 3 Anti-Windup PID *)
f_PID_Z3_Error := f_SetStageTemp_degC - f_StageTemp_Zone3_degC;
f_PID_Z3_Derivative := (f_PID_Z3_Error - f_PID_Z3_PrevError) / f_SamplingTime_s;
f_PID_Z3_PrevError := f_PID_Z3_Error;
f_PID_Z3_Integral := f_PID_Z3_Integral + f_PID_Stage_Ki * f_PID_Z3_Error * f_SamplingTime_s;
IF f_PID_Z3_Integral > 35.0 THEN f_PID_Z3_Integral := 35.0; ELSIF f_PID_Z3_Integral < -10.0 THEN f_PID_Z3_Integral := -10.0; END_IF;

(* Multi-Zone Cross-Coupling Decoupling Network *)
f_WorkholderHeatPwr_Zone1_pct := K_ThermalCrossCoupling[1, 1] * (f_PID_Stage_Kp * f_PID_Z1_Error + f_PID_Z1_Integral + f_PID_Stage_Kd * f_PID_Z1_Derivative) +
                                 K_ThermalCrossCoupling[1, 2] * (f_PID_Stage_Kp * f_PID_Z2_Error + f_PID_Z2_Integral) +
                                 K_ThermalCrossCoupling[1, 3] * (f_PID_Stage_Kp * f_PID_Z3_Error + f_PID_Z3_Integral);

f_WorkholderHeatPwr_Zone2_pct := K_ThermalCrossCoupling[2, 1] * (f_PID_Stage_Kp * f_PID_Z1_Error + f_PID_Z1_Integral) +
                                 K_ThermalCrossCoupling[2, 2] * (f_PID_Stage_Kp * f_PID_Z2_Error + f_PID_Z2_Integral + f_PID_Stage_Kd * f_PID_Z2_Derivative) +
                                 K_ThermalCrossCoupling[2, 3] * (f_PID_Stage_Kp * f_PID_Z3_Error + f_PID_Z3_Integral);

f_WorkholderHeatPwr_Zone3_pct := K_ThermalCrossCoupling[3, 1] * (f_PID_Stage_Kp * f_PID_Z1_Error + f_PID_Z1_Integral) +
                                 K_ThermalCrossCoupling[3, 2] * (f_PID_Stage_Kp * f_PID_Z2_Error + f_PID_Z2_Integral) +
                                 K_ThermalCrossCoupling[3, 3] * (f_PID_Stage_Kp * f_PID_Z3_Error + f_PID_Z3_Integral + f_PID_Stage_Kd * f_PID_Z3_Derivative);

(* Vacuum Clamp Thermal Safety Interlock *)
IF f_Voted_StageVacuum_mbar < f_Alarm_StageVacuum_LL_mbar THEN
    (* Derate heating to prevent thermal damage if substrate vacuum is unsealed *)
    IF f_WorkholderHeatPwr_Zone1_pct > 25.0 THEN f_WorkholderHeatPwr_Zone1_pct := 25.0; END_IF;
    IF f_WorkholderHeatPwr_Zone2_pct > 25.0 THEN f_WorkholderHeatPwr_Zone2_pct := 25.0; END_IF;
    IF f_WorkholderHeatPwr_Zone3_pct > 25.0 THEN f_WorkholderHeatPwr_Zone3_pct := 25.0; END_IF;
END_IF;

(* Saturation Bounds [0.0 .. 100.0 %] *)
IF f_WorkholderHeatPwr_Zone1_pct > 100.0 THEN f_WorkholderHeatPwr_Zone1_pct := 100.0; ELSIF f_WorkholderHeatPwr_Zone1_pct < 0.0 THEN f_WorkholderHeatPwr_Zone1_pct := 0.0; END_IF;
IF f_WorkholderHeatPwr_Zone2_pct > 100.0 THEN f_WorkholderHeatPwr_Zone2_pct := 100.0; ELSIF f_WorkholderHeatPwr_Zone2_pct < 0.0 THEN f_WorkholderHeatPwr_Zone2_pct := 0.0; END_IF;
IF f_WorkholderHeatPwr_Zone3_pct > 100.0 THEN f_WorkholderHeatPwr_Zone3_pct := 100.0; ELSIF f_WorkholderHeatPwr_Zone3_pct < 0.0 THEN f_WorkholderHeatPwr_Zone3_pct := 0.0; END_IF;

(* ========================================================================================================== *)
(* PHASE 9: INTERMETALLIC COMPOUND (IMC) DIFFUSION & SHEAR STRENGTH KINETICS                           *)
(* ========================================================================================================== *)
(* Localized Acoustic Ultrasonic Friction Temperature Elevation *)
f_AcousticThermalBoost_degC := f_Voted_USPower_mW * 0.0425; (* Empirical acoustic dissipation factor *)
f_InterfaceAbsoluteTemp_K := f_StageTemp_Zone1_degC + f_AcousticThermalBoost_degC + 273.15;

(* Arrhenius Intermetallic Growth Velocity: k(T) = k0 * exp(-Ea / (R * T)) *)
f_IMC_InstantDiffusionRate := f_IMC_Arrhenius_k0 *
                              EXP(- f_IMC_ActivationEnergy_J_mol / (f_UniversalGasConstant_R * f_InterfaceAbsoluteTemp_K)) * 1.0E9;

(* Parabolic Kinetic Accumulation: d(delta) / dt = k(T) / (2 * delta + delta_0) *)
IF (n_CurrentState = STATE_1ST_BOND_ULTRASONIC_BURST) OR (n_CurrentState = STATE_2ND_BOND_STITCH_BURST) THEN
    f_IMC_TotalThickness_nm := f_IMC_TotalThickness_nm +
                               (f_IMC_InstantDiffusionRate / (2.0 * f_IMC_TotalThickness_nm + 0.12)) * f_SamplingTime_s;
    IF f_IMC_TotalThickness_nm > 250.0 THEN f_IMC_TotalThickness_nm := 250.0; END_IF;
END_IF;

f_IntermetallicGrowth_nm := f_IMC_TotalThickness_nm;

(* Asymptotic Ball Shear Strength Estimation (SEMI G45 compliance) *)
f_EstimatedShearStrength_gf := f_ShearStrengthScaling_gf * (1.0 - EXP(- f_IMC_TotalThickness_nm / 42.0));

(* ========================================================================================================== *)
(* PHASE 10: 12-STAGE OPERATIONAL FINITE STATE MACHINE (FSM)                                                  *)
(* ========================================================================================================== *)
(* Update State Timers *)
t_StateDurationTimer := t_StateDurationTimer + REAL_TO_TIME(LREAL_TO_REAL(f_SamplingTime_s * 1000.0));
t_CycleExecutionTimer := t_CycleExecutionTimer + REAL_TO_TIME(LREAL_TO_REAL(f_SamplingTime_s * 1000.0));
t_SingleWireTimer := t_SingleWireTimer + REAL_TO_TIME(LREAL_TO_REAL(f_SamplingTime_s * 1000.0));

(* Hardware E-Stop Priority Transition *)
IF NOT b_EmergencyStop THEN
    n_CurrentState := STATE_EMERGENCY_STOP_SAFE_STOP;
END_IF;

CASE n_CurrentState OF
    STATE_IDLE_STANDBY:
        b_Ready := TRUE;
        b_Active := FALSE;
        b_Done := FALSE;
        f_VCM_DriveCurrent_mA := 0.0;
        f_US_DrivePower_mW := 0.0;
        f_EFO_TriggerPulse_V := 0.0;
        b_WireClampSol_Open := TRUE;
        b_WireClampSol_Close := FALSE;
        b_AirTensioner_Active := FALSE;
        b_StageVacuumSol_Cmd := TRUE;
        b_LeadframeClamped := FALSE;
        b_LeadframeIndexPulse := FALSE;

        IF b_Enable AND b_EmergencyStop AND b_CycleStart THEN
            n_CurrentState := STATE_SUBSTRATE_INDEXING_CLAMP;
            t_StateDurationTimer := T#0ms;
            b_Ready := FALSE;
            b_Active := TRUE;
            n_CompletedWiresDie := 0;
            n_ActiveWireCounter := 1;
        END_IF;

    STATE_SUBSTRATE_INDEXING_CLAMP:
        (* Engage mechanical clamp & vacuum venturi chuck *)
        b_StageVacuumSol_Cmd := TRUE;
        b_LeadframeClamped := TRUE;
        b_LeadframeIndexPulse := FALSE;
        f_VCM_DriveCurrent_mA := 0.0;
        f_US_DrivePower_mW := 0.0;

        IF (f_Voted_StageVacuum_mbar >= f_Alarm_StageVacuum_LL_mbar) AND
           (t_StateDurationTimer >= T#15ms) THEN
            n_CurrentState := STATE_OPTICAL_PR_ALIGNMENT;
            t_StateDurationTimer := T#0ms;
        END_IF;

    STATE_OPTICAL_PR_ALIGNMENT:
        (* Perform vision correlation and update coordinate offsets *)
        IF b_PR_MatchValid AND (f_PR_CorrelationScore >= f_Alarm_PR_Correlation_Min) THEN
            n_CurrentState := STATE_EFO_SPARK_DISCHARGE;
            t_StateDurationTimer := T#0ms;
        ELSIF t_StateDurationTimer >= T#25ms THEN
            (* Timeout failure on optical PR match *)
            b_Error := TRUE;
            n_ErrorCode := 102; (* PR Alignment Timeout Error *)
        END_IF;

    STATE_EFO_SPARK_DISCHARGE:
        (* Retract capillary to EFO firing height & trigger capacitor spark *)
        f_VCM_DriveCurrent_mA := -850.0; (* Retract to spark clearance height *)
        b_WireClampSol_Open := FALSE;
        b_WireClampSol_Close := TRUE;    (* Clamp wire to maintain spark reference *)
        f_EFO_TriggerPulse_V := f_EFO_ChargingVoltage_V;

        IF (f_EFOCurrent_mA >= f_Alarm_EFO_Current_Min_mA) AND (t_StateDurationTimer >= T#2ms) THEN
            f_EFO_TriggerPulse_V := 0.0;
            n_CurrentState := STATE_FAB_OPTICAL_CHECK;
            t_StateDurationTimer := T#0ms;
        ELSIF t_StateDurationTimer >= T#8ms THEN
            f_EFO_TriggerPulse_V := 0.0;
            b_Error := TRUE;
            n_ErrorCode := 103; (* EFO Spark Breakdown Open-Circuit Failure *)
        END_IF;

    STATE_FAB_OPTICAL_CHECK:
        f_EFO_TriggerPulse_V := 0.0;
        b_WireClampSol_Open := TRUE;
        b_WireClampSol_Close := FALSE;

        IF b_FAB_InspectionPassed THEN
            n_CurrentState := STATE_APPROACH_SOFT_LANDING;
            t_StateDurationTimer := T#0ms;
            b_ContactEventDetected := FALSE;
            f_ContactTouchdownZ_nm := 0.0;
        ELSIF t_StateDurationTimer >= T#5ms THEN
            b_Error := TRUE;
            n_ErrorCode := 104; (* Free Air Ball Dimension Inspection Rejection *)
        END_IF;

    STATE_APPROACH_SOFT_LANDING:
        (* High-Speed Dive: 1.2 m/s dive followed by dynamic impact soft-landing *)
        IF NOT b_ContactEventDetected THEN
            f_VCM_DriveCurrent_mA := 1850.0; (* Forward dive driving current *)
            f_US_DrivePower_mW := 0.0;
        ELSE
            (* Impact confirmed: switch to force compliance dwell *)
            f_VCM_DriveCurrent_mA := 450.0;
            n_CurrentState := STATE_1ST_BOND_ULTRASONIC_BURST;
            t_StateDurationTimer := T#0ms;
            t_US_BurstTimer := T#0ms;
        END_IF;

        IF t_StateDurationTimer >= T#20ms THEN
            b_Error := TRUE;
            n_ErrorCode := 105; (* Soft Landing Over-Travel Missed Contact *)
        END_IF;

    STATE_1ST_BOND_ULTRASONIC_BURST:
        (* Deliver 1st Bond Ultrasonic Burst and Controlled Force Profile *)
        f_VCM_DriveCurrent_mA := 920.0; (* Apply commanded bond downforce *)
        f_US_DrivePower_mW := f_SetUSPower_1st_mW;
        t_US_BurstTimer := t_US_BurstTimer + REAL_TO_TIME(LREAL_TO_REAL(f_SamplingTime_s * 1000.0));

        IF t_US_BurstTimer >= REAL_TO_TIME(LREAL_TO_REAL(f_SetBondTime_1st_ms)) THEN
            f_US_DrivePower_mW := 0.0;
            n_CurrentState := STATE_LOOPING_TRAJECTORY;
            t_StateDurationTimer := T#0ms;
            f_Loop_ProfileProgress := 0.0;
        END_IF;

    STATE_LOOPING_TRAJECTORY:
        (* Progress wire loop trajectory generator: reverse motion kink, apex rise, lead descent *)
        f_Loop_ProfileProgress := f_Loop_ProfileProgress + (f_SamplingTime_s / 0.0125); (* 12.5 ms trajectory duration *)
        IF f_Loop_ProfileProgress > 1.0 THEN f_Loop_ProfileProgress := 1.0; END_IF;

        (* VCM Z-axis tracking trajectory command *)
        f_VCM_DriveCurrent_mA := -1200.0 * (1.0 - f_Loop_ProfileProgress) + 1450.0 * f_Loop_ProfileProgress;

        IF (f_Loop_ProfileProgress >= 1.0) AND (t_StateDurationTimer >= T#12ms) THEN
            n_CurrentState := STATE_2ND_BOND_STITCH_BURST;
            t_StateDurationTimer := T#0ms;
            t_US_BurstTimer := T#0ms;
            b_ContactEventDetected := FALSE;
        END_IF;

    STATE_2ND_BOND_STITCH_BURST:
        (* 2nd Bond Leadframe Crescent Scrub & Ultrasonic Stitch Burst *)
        f_VCM_DriveCurrent_mA := 1450.0; (* Higher stitch deformation force *)
        f_US_DrivePower_mW := f_SetUSPower_2nd_mW;
        t_US_BurstTimer := t_US_BurstTimer + REAL_TO_TIME(LREAL_TO_REAL(f_SamplingTime_s * 1000.0));

        IF t_US_BurstTimer >= REAL_TO_TIME(LREAL_TO_REAL(f_SetBondTime_2nd_ms)) THEN
            f_US_DrivePower_mW := 0.0;
            n_CurrentState := STATE_WIRE_CLAMP_TEAR_FEED;
            t_StateDurationTimer := T#0ms;
        END_IF;

    STATE_WIRE_CLAMP_TEAR_FEED:
        (* Close wire clamp & perform upward tear retract to separate wire tail *)
        b_WireClampSol_Open := FALSE;
        b_WireClampSol_Close := TRUE;
        f_VCM_DriveCurrent_mA := -2200.0; (* High acceleration tear retract *)
        b_AirTensioner_Active := TRUE;

        IF t_StateDurationTimer >= T#4ms THEN
            n_CurrentState := STATE_Z_RETRACT_TAIL_METROLOGY;
            t_StateDurationTimer := T#0ms;
            n_CompletedWiresDie := n_CompletedWiresDie + 1;
            n_TotalWiresAccumulated := n_TotalWiresAccumulated + 1;
        END_IF;

    STATE_Z_RETRACT_TAIL_METROLOGY:
        (* Capillary retract to spark position & laser tail length metrology *)
        f_VCM_DriveCurrent_mA := 0.0;
        b_WireClampSol_Open := TRUE;
        b_WireClampSol_Close := FALSE;

        (* Check if die mesh is complete or more wires remain *)
        IF n_CompletedWiresDie >= n_TargetBondCount THEN
            n_CurrentState := STATE_LEADFRAME_EGRESS_INDEX;
            t_StateDurationTimer := T#0ms;
        ELSE
            (* Loop back for next wire on same die *)
            n_ActiveWireCounter := n_ActiveWireCounter + 1;
            n_CurrentState := STATE_EFO_SPARK_DISCHARGE;
            t_StateDurationTimer := T#0ms;
            t_SingleWireTimer := T#0ms;
        END_IF;

    STATE_LEADFRAME_EGRESS_INDEX:
        (* Finished all wires on die unit: release clamps & index to next unit *)
        b_LeadframeClamped := FALSE;
        b_StageVacuumSol_Cmd := FALSE;
        b_LeadframeIndexPulse := TRUE;

        IF t_StateDurationTimer >= T#30ms THEN
            b_LeadframeIndexPulse := FALSE;
            b_Done := TRUE;
            b_Active := FALSE;
            n_CurrentState := STATE_IDLE_STANDBY;
            t_StateDurationTimer := T#0ms;
        END_IF;

    STATE_EMERGENCY_STOP_SAFE_STOP:
        (* Safe shutdown: immediate Z retract, cut ultrasonic power, lock clamp *)
        f_VCM_DriveCurrent_mA := -3500.0; (* Retract to hardware upper limit *)
        f_US_DrivePower_mW := 0.0;
        f_EFO_TriggerPulse_V := 0.0;
        b_WireClampSol_Open := FALSE;
        b_WireClampSol_Close := TRUE;
        b_AirTensioner_Active := FALSE;
        b_LeadframeIndexPulse := FALSE;
        b_Active := FALSE;
        b_Error := TRUE;
        n_ErrorCode := 999; (* Emergency E-Stop Active *)

        IF b_EmergencyStop AND b_ResetAlarms THEN
            n_CurrentState := STATE_IDLE_STANDBY;
            b_Error := FALSE;
            n_ErrorCode := 0;
            t_StateDurationTimer := T#0ms;
        END_IF;
ELSE
    n_CurrentState := STATE_IDLE_STANDBY;
END_CASE;

(* ========================================================================================================== *)
(* PHASE 11: ISA-18.2 MULTI-TIERED ALARMS & DIAGNOSTIC WORD BIT-PACKING                                      *)
(* ========================================================================================================== *)
(* Alarm Group 1: Critical Process Trip Alarms (Bit-Packed into dw_AlarmsGroup1) *)
(* Bit 0: Emergency Stop Hardware Circuit Open *)
IF NOT b_EmergencyStop THEN dw_AlarmsGroup1 := dw_AlarmsGroup1 OR 16#00000001; ELSE dw_AlarmsGroup1 := dw_AlarmsGroup1 AND NOT 16#00000001; END_IF;

(* Bit 1: EFO Spark Gap Breakdown Failure / Open-Circuit *)
IF (n_CurrentState = STATE_EFO_SPARK_DISCHARGE) AND (t_StateDurationTimer >= T#6ms) AND (f_EFOCurrent_mA < f_Alarm_EFO_Current_Min_mA) THEN
    dw_AlarmsGroup1 := dw_AlarmsGroup1 OR 16#00000002;
ELSE
    IF b_ResetAlarms THEN dw_AlarmsGroup1 := dw_AlarmsGroup1 AND NOT 16#00000002; END_IF;
END_IF;

(* Bit 2: Free Air Ball Diameter Critical High HH *)
IF f_FAB_OpticalMeasurement_um > f_Alarm_FAB_Diameter_HH_um THEN
    dw_AlarmsGroup1 := dw_AlarmsGroup1 OR 16#00000004;
ELSE
    IF b_ResetAlarms THEN dw_AlarmsGroup1 := dw_AlarmsGroup1 AND NOT 16#00000004; END_IF;
END_IF;

(* Bit 3: Free Air Ball Missing / Diameter Critical Low LL *)
IF (n_CurrentState = STATE_FAB_OPTICAL_CHECK) AND (f_FAB_OpticalMeasurement_um < f_Alarm_FAB_Diameter_LL_um) THEN
    dw_AlarmsGroup1 := dw_AlarmsGroup1 OR 16#00000008;
ELSE
    IF b_ResetAlarms THEN dw_AlarmsGroup1 := dw_AlarmsGroup1 AND NOT 16#00000008; END_IF;
END_IF;

(* Bit 4: Wire Drag / Broken Wire Sensor Tripped *)
IF b_WireDragSensor_Tripped THEN
    dw_AlarmsGroup1 := dw_AlarmsGroup1 OR 16#00000010;
ELSE
    IF b_ResetAlarms THEN dw_AlarmsGroup1 := dw_AlarmsGroup1 AND NOT 16#00000010; END_IF;
END_IF;

(* Bit 5: Ultrasonic Dynamic Impedance Phase Detuning HH/LL *)
IF (ABS(f_US_ImpedancePhase_deg) > f_Alarm_US_ImpedancePhase_HH_deg) AND ((n_CurrentState = STATE_1ST_BOND_ULTRASONIC_BURST) OR (n_CurrentState = STATE_2ND_BOND_STITCH_BURST)) THEN
    dw_AlarmsGroup1 := dw_AlarmsGroup1 OR 16#00000020;
ELSE
    IF b_ResetAlarms THEN dw_AlarmsGroup1 := dw_AlarmsGroup1 AND NOT 16#00000020; END_IF;
END_IF;

(* Bit 6: Substrate Vacuum Chuck Lost Trip LL *)
IF f_Voted_StageVacuum_mbar < f_Alarm_StageVacuum_LL_mbar THEN
    dw_AlarmsGroup1 := dw_AlarmsGroup1 OR 16#00000040;
ELSE
    IF b_ResetAlarms THEN dw_AlarmsGroup1 := dw_AlarmsGroup1 AND NOT 16#00000040; END_IF;
END_IF;

(* Bit 7: Excessive Soft-Landing Impact Force HH (> 0.15 N) *)
IF f_ContactInitialImpactForce_mN > f_Alarm_ContactForce_HH_mN THEN
    dw_AlarmsGroup1 := dw_AlarmsGroup1 OR 16#00000080;
ELSE
    IF b_ResetAlarms THEN dw_AlarmsGroup1 := dw_AlarmsGroup1 AND NOT 16#00000080; END_IF;
END_IF;

(* Bit 8: Z-Axis Optical Scale TMR Discrepancy Fault Trip *)
IF b_ZEnc_TMR_FaultTrip THEN dw_AlarmsGroup1 := dw_AlarmsGroup1 OR 16#00000100; ELSE dw_AlarmsGroup1 := dw_AlarmsGroup1 AND NOT 16#00000100; END_IF;

(* Bit 9: Bond Force Load Cell TMR Discrepancy Fault Trip *)
IF b_Force_TMR_FaultTrip THEN dw_AlarmsGroup1 := dw_AlarmsGroup1 OR 16#00000200; ELSE dw_AlarmsGroup1 := dw_AlarmsGroup1 AND NOT 16#00000200; END_IF;

(* Bit 10: Ultrasonic Power Feedback TMR Discrepancy Fault Trip *)
IF b_USPwr_TMR_FaultTrip THEN dw_AlarmsGroup1 := dw_AlarmsGroup1 OR 16#00000400; ELSE dw_AlarmsGroup1 := dw_AlarmsGroup1 AND NOT 16#00000400; END_IF;

(* Bit 11: Workholder Stage Vacuum TMR Discrepancy Fault Trip *)
IF b_Vac_TMR_FaultTrip THEN dw_AlarmsGroup1 := dw_AlarmsGroup1 OR 16#00000800; ELSE dw_AlarmsGroup1 := dw_AlarmsGroup1 AND NOT 16#00000800; END_IF;

(* Alarm Group 2: Warning & Degradation Alarms (Bit-Packed into dw_AlarmsGroup2) *)
(* Bit 0: Optical PR Vision Correlation Score Marginal *)
IF f_PR_CorrelationScore < f_Alarm_PR_Correlation_Min THEN dw_AlarmsGroup2 := dw_AlarmsGroup2 OR 16#00000001; ELSE dw_AlarmsGroup2 := dw_AlarmsGroup2 AND NOT 16#00000001; END_IF;

(* Bit 1: Workholder Stage Temperature High Warning H *)
IF f_StageTemp_Zone1_degC > (f_SetStageTemp_degC + 5.0) THEN dw_AlarmsGroup2 := dw_AlarmsGroup2 OR 16#00000002; ELSE dw_AlarmsGroup2 := dw_AlarmsGroup2 AND NOT 16#00000002; END_IF;

(* Bit 2: Workholder Stage Temperature Low Warning L *)
IF f_StageTemp_Zone1_degC < (f_SetStageTemp_degC - 5.0) THEN dw_AlarmsGroup2 := dw_AlarmsGroup2 OR 16#00000004; ELSE dw_AlarmsGroup2 := dw_AlarmsGroup2 AND NOT 16#00000004; END_IF;

(* Bit 3: Wire Spool Back-Tension Deviation *)
IF (f_WireSpoolTension_mN > 85.0) OR (f_WireSpoolTension_mN < 15.0) THEN dw_AlarmsGroup2 := dw_AlarmsGroup2 OR 16#00000008; ELSE dw_AlarmsGroup2 := dw_AlarmsGroup2 AND NOT 16#00000008; END_IF;

(* Bit 4: Wire Tail Length Short Warning *)
IF f_WireTailLength_Sensor_um < f_Alarm_TailLength_Min_um THEN dw_AlarmsGroup2 := dw_AlarmsGroup2 OR 16#00000010; ELSE dw_AlarmsGroup2 := dw_AlarmsGroup2 AND NOT 16#00000010; END_IF;

(* Bit 5: Wire Tail Length Long Warning *)
IF f_WireTailLength_Sensor_um > f_Alarm_TailLength_Max_um THEN dw_AlarmsGroup2 := dw_AlarmsGroup2 OR 16#00000020; ELSE dw_AlarmsGroup2 := dw_AlarmsGroup2 AND NOT 16#00000020; END_IF;

(* Bit 6: Intermetallic Compound (IMC) Thickness Marginal Warning *)
IF (f_IMC_TotalThickness_nm < f_IMC_TargetMinThickness_nm) AND (n_CompletedWiresDie > 0) THEN dw_AlarmsGroup2 := dw_AlarmsGroup2 OR 16#00000040; ELSE dw_AlarmsGroup2 := dw_AlarmsGroup2 AND NOT 16#00000040; END_IF;

(* Bit 7: Z-Axis Optical Scale TMR Degraded to 1oo2 or Single Channel *)
IF b_ZEnc_TMR_Degraded THEN dw_AlarmsGroup2 := dw_AlarmsGroup2 OR 16#00000080; ELSE dw_AlarmsGroup2 := dw_AlarmsGroup2 AND NOT 16#00000080; END_IF;

(* Bit 8: Bond Force Load Cell TMR Degraded *)
IF b_Force_TMR_Degraded THEN dw_AlarmsGroup2 := dw_AlarmsGroup2 OR 16#00000100; ELSE dw_AlarmsGroup2 := dw_AlarmsGroup2 AND NOT 16#00000100; END_IF;

(* Bit 9: Ultrasonic Power TMR Degraded *)
IF b_USPwr_TMR_Degraded THEN dw_AlarmsGroup2 := dw_AlarmsGroup2 OR 16#00000200; ELSE dw_AlarmsGroup2 := dw_AlarmsGroup2 AND NOT 16#00000200; END_IF;

(* Bit 10: Vacuum Workholder TMR Degraded *)
IF b_Vac_TMR_Degraded THEN dw_AlarmsGroup2 := dw_AlarmsGroup2 OR 16#00000400; ELSE dw_AlarmsGroup2 := dw_AlarmsGroup2 AND NOT 16#00000400; END_IF;

(* Diagnostic Status Telemetry Word (Bit-Packed into dw_DiagnosticsWord) *)
dw_DiagnosticsWord := 16#00000000;
IF b_Ready THEN dw_DiagnosticsWord := dw_DiagnosticsWord OR 16#00000001; END_IF;
IF b_Active THEN dw_DiagnosticsWord := dw_DiagnosticsWord OR 16#00000002; END_IF;
IF b_Done THEN dw_DiagnosticsWord := dw_DiagnosticsWord OR 16#00000004; END_IF;
IF b_Error THEN dw_DiagnosticsWord := dw_DiagnosticsWord OR 16#00000008; END_IF;
IF b_US_ResonanceLocked THEN dw_DiagnosticsWord := dw_DiagnosticsWord OR 16#00000010; END_IF;
IF b_FAB_InspectionPassed THEN dw_DiagnosticsWord := dw_DiagnosticsWord OR 16#00000020; END_IF;
IF b_ContactEventDetected THEN dw_DiagnosticsWord := dw_DiagnosticsWord OR 16#00000040; END_IF;
IF b_LeadframeClamped THEN dw_DiagnosticsWord := dw_DiagnosticsWord OR 16#00000080; END_IF;

(* Instantaneous Bonding Rate Filter (Target 22 Wires/Second) *)
IF t_SingleWireTimer > T#0ms THEN
    f_FilteredWirePeriod_s := 0.95 * f_FilteredWirePeriod_s + 0.05 * (TIME_TO_LREAL(t_SingleWireTimer) * 0.001);
    IF f_FilteredWirePeriod_s > 0.005 THEN
        f_CurrentBondRate_wps := 1.0 / f_FilteredWirePeriod_s;
    ELSE
        f_CurrentBondRate_wps := 22.0;
    END_IF;
ELSE
    f_CurrentBondRate_wps := 22.0;
END_IF;

(* Master Error Evaluation *)
IF (dw_AlarmsGroup1 <> 16#00000000) THEN
    b_Error := TRUE;
    IF n_ErrorCode = 0 THEN
        n_ErrorCode := 1001; (* ISA-18.2 Critical Trip Alarm Latched *)
    END_IF;
END_IF;

n_CurrentState := n_CurrentState;
"""
