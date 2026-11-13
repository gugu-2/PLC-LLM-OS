# rail_emu_builder/part6_wssp_fsm.py

def get_part6():
    return '''(* ============================================================================================== *)
(* PHASE 8: WHEEL SLIP-SLIDE PROTECTION (WSSP) 4-PHASE CYCLE PER AXLE (UIC 541-05 / EN 15595)     *)
(* Deceleration and Velocity Difference Anti-Skid Intervention with Automatic Railhead Sanding    *)
(* ============================================================================================== *)

(* ---------------------------------------------------------------------------------------------- *)
(* Axle 1 WSSP Valve Cycle State Machine                                                          *)
(* Phase 0: Normal Adhesion | Phase 1: Pressure Hold | Phase 2: Rapid Dump | Phase 3: Stepped Re-Apply*)
(* ---------------------------------------------------------------------------------------------- *)
rWSSP_PhaseTimer_A1_s := rWSSP_PhaseTimer_A1_s + T_CYCLE_SEC;

CASE nWSSP_Phase_Axle1 OF
    0: (* Normal Adhesion *)
        bWSSPDumpValveCmd_A1 := FALSE;
        bWSSPApplyValveCmd_A1 := FALSE;
        rWSSP_PhaseTimer_A1_s := 0.0;
        
        (* Detection Criteria: Deceleration exceeds 3.8 m/s2 OR Slip velocity exceeds 1.8 m/s *)
        IF (rAxle1_LinearDecel_ms2 > rAxle1_DecelThreshold_ms2) OR 
           (rAxle1_SlipVelocity_ms < -rAxle1_SlipThreshold_ms) OR
           (rAxle1_SlipRatio > 0.085) THEN
            nWSSP_Phase_Axle1 := 1; (* Transition to Phase 1: Pressure Hold *)
            nWSSP_InterventionCount_A1 := nWSSP_InterventionCount_A1 + 1;
        END_IF;

    1: (* Phase 1: Pressure Hold - Prevent further pneumatic pressure rise *)
        bWSSPDumpValveCmd_A1 := FALSE;
        bWSSPApplyValveCmd_A1 := TRUE; (* Close inlet valve to hold pressure *)
        
        IF (rAxle1_LinearDecel_ms2 > (rAxle1_DecelThreshold_ms2 * 1.25)) OR 
           (rAxle1_SlipVelocity_ms < -(rAxle1_SlipThreshold_ms * 1.30)) OR
           (rWSSP_PhaseTimer_A1_s > 0.060) THEN
            nWSSP_Phase_Axle1 := 2; (* Transition to Phase 2: Rapid Pressure Dump *)
            rWSSP_PhaseTimer_A1_s := 0.0;
        ELSIF (rAxle1_LinearDecel_ms2 < 1.50) AND (rAxle1_SlipVelocity_ms > -0.50) THEN
            nWSSP_Phase_Axle1 := 3; (* Recovery detected: proceed to soft apply *)
            rWSSP_PhaseTimer_A1_s := 0.0;
        END_IF;

    2: (* Phase 2: Rapid Pressure Dump - Exhaust brake cylinder to free locked wheel *)
        bWSSPDumpValveCmd_A1 := TRUE;  (* Energize exhaust dump valve *)
        bWSSPApplyValveCmd_A1 := TRUE; (* Keep inlet valve closed *)
        
        (* Check if wheel speed is re-accelerating toward train ground velocity *)
        IF (rAxle1_LinearDecel_ms2 < -0.80) OR 
           (rAxle1_SlipVelocity_ms > -0.65) OR 
           (rWSSP_PhaseTimer_A1_s > 0.140) THEN
            nWSSP_Phase_Axle1 := 3; (* Transition to Phase 3: Stepped Re-Apply *)
            rWSSP_PhaseTimer_A1_s := 0.0;
        END_IF;

    3: (* Phase 3: Stepped Soft Re-Apply - Pulse pressure back up toward adhesion boundary *)
        bWSSPDumpValveCmd_A1 := FALSE;
        (* 30% PWM modulation for soft pressure re-application *)
        IF (rWSSP_PhaseTimer_A1_s - (DINT_TO_REAL(REAL_TO_DINT(rWSSP_PhaseTimer_A1_s / 0.050)) * 0.050)) < 0.015 THEN
            bWSSPApplyValveCmd_A1 := FALSE; (* Pulse inlet valve open *)
        ELSE
            bWSSPApplyValveCmd_A1 := TRUE;  (* Hold inlet valve closed *)
        END_IF;
        
        IF rWSSP_PhaseTimer_A1_s > 0.220 THEN
            nWSSP_Phase_Axle1 := 0; (* Restore normal pneumatic control *)
            rWSSP_PhaseTimer_A1_s := 0.0;
        ELSIF (rAxle1_LinearDecel_ms2 > rAxle1_DecelThreshold_ms2) THEN
            nWSSP_Phase_Axle1 := 1; (* Re-slip triggered: immediate hold *)
            rWSSP_PhaseTimer_A1_s := 0.0;
        END_IF;
ELSE
    nWSSP_Phase_Axle1 := 0;
END_CASE;

(* ---------------------------------------------------------------------------------------------- *)
(* Axle 2 WSSP Valve Cycle State Machine                                                          *)
(* ---------------------------------------------------------------------------------------------- *)
rWSSP_PhaseTimer_A2_s := rWSSP_PhaseTimer_A2_s + T_CYCLE_SEC;

CASE nWSSP_Phase_Axle2 OF
    0: (* Normal Adhesion *)
        bWSSPDumpValveCmd_A2 := FALSE;
        bWSSPApplyValveCmd_A2 := FALSE;
        rWSSP_PhaseTimer_A2_s := 0.0;
        
        IF (rAxle2_LinearDecel_ms2 > rAxle1_DecelThreshold_ms2) OR 
           (rAxle2_SlipVelocity_ms < -rAxle1_SlipThreshold_ms) OR
           (rAxle2_SlipRatio > 0.085) THEN
            nWSSP_Phase_Axle2 := 1;
            nWSSP_InterventionCount_A2 := nWSSP_InterventionCount_A2 + 1;
        END_IF;

    1: (* Phase 1: Pressure Hold *)
        bWSSPDumpValveCmd_A2 := FALSE;
        bWSSPApplyValveCmd_A2 := TRUE;
        
        IF (rAxle2_LinearDecel_ms2 > (rAxle1_DecelThreshold_ms2 * 1.25)) OR 
           (rAxle2_SlipVelocity_ms < -(rAxle1_SlipThreshold_ms * 1.30)) OR
           (rWSSP_PhaseTimer_A2_s > 0.060) THEN
            nWSSP_Phase_Axle2 := 2;
            rWSSP_PhaseTimer_A2_s := 0.0;
        ELSIF (rAxle2_LinearDecel_ms2 < 1.50) AND (rAxle2_SlipVelocity_ms > -0.50) THEN
            nWSSP_Phase_Axle2 := 3;
            rWSSP_PhaseTimer_A2_s := 0.0;
        END_IF;

    2: (* Phase 2: Rapid Pressure Dump *)
        bWSSPDumpValveCmd_A2 := TRUE;
        bWSSPApplyValveCmd_A2 := TRUE;
        
        IF (rAxle2_LinearDecel_ms2 < -0.80) OR 
           (rAxle2_SlipVelocity_ms > -0.65) OR 
           (rWSSP_PhaseTimer_A2_s > 0.140) THEN
            nWSSP_Phase_Axle2 := 3;
            rWSSP_PhaseTimer_A2_s := 0.0;
        END_IF;

    3: (* Phase 3: Stepped Soft Re-Apply *)
        bWSSPDumpValveCmd_A2 := FALSE;
        IF (rWSSP_PhaseTimer_A2_s - (DINT_TO_REAL(REAL_TO_DINT(rWSSP_PhaseTimer_A2_s / 0.050)) * 0.050)) < 0.015 THEN
            bWSSPApplyValveCmd_A2 := FALSE;
        ELSE
            bWSSPApplyValveCmd_A2 := TRUE;
        END_IF;
        
        IF rWSSP_PhaseTimer_A2_s > 0.220 THEN
            nWSSP_Phase_Axle2 := 0;
            rWSSP_PhaseTimer_A2_s := 0.0;
        ELSIF (rAxle2_LinearDecel_ms2 > rAxle1_DecelThreshold_ms2) THEN
            nWSSP_Phase_Axle2 := 1;
            rWSSP_PhaseTimer_A2_s := 0.0;
        END_IF;
ELSE
    nWSSP_Phase_Axle2 := 0;
END_CASE;

(* Persistent Low Adhesion Integrator for Automatic Railhead Quartz Sand Injection *)
IF (nWSSP_Phase_Axle1 > 0) OR (nWSSP_Phase_Axle2 > 0) OR (rObservedAdhesionCoeff < 0.10) THEN
    rLowAdhesionAccumulator_s := rLowAdhesionAccumulator_s + T_CYCLE_SEC;
ELSE
    rLowAdhesionAccumulator_s := MAX(0.0, rLowAdhesionAccumulator_s - (T_CYCLE_SEC * 0.25));
END_IF;

IF (rLowAdhesionAccumulator_s > 0.850) OR bTrackSandingManualCmd THEN
    bRailheadSandingActive := TRUE;
ELSE
    bRailheadSandingActive := FALSE;
END_IF;

(* ============================================================================================== *)
(* PHASE 9: DETERMINISTIC 14-STAGE PRODUCTION FINITE STATE MACHINE (FSM)                          *)
(* Full Operational Envelope from Power-On Diagnostics to High-Speed Cruise & Failsafe E-Stop      *)
(* ============================================================================================== *)
rFSM_StateTimer_s := rFSM_StateTimer_s + T_CYCLE_SEC;

(* Safety Pre-Emption: Check SIL-4 Emergency Brake Hardware Loop *)
IF NOT bEmergencyBrakeLoop THEN
    nFSM_CurrentState := 12; (* Jump immediately to Emergency Brake Failsafe Trip *)
END_IF;

CASE nFSM_CurrentState OF
    0: (* STATE 0: INIT_COLD_BOOT_DIAGNOSTICS *)
        bTCUReady := FALSE;
        bBCUReady := FALSE;
        bVCBCloseCommand := FALSE;
        bPantographRaiseCommand := FALSE;
        bEmergencyTripActive := FALSE;
        
        IF bSystemEnable AND (rFSM_StateTimer_s > 1.00) THEN
            nFSM_CurrentState := 1;
            rFSM_StateTimer_s := 0.0;
        END_IF;

    1: (* STATE 1: PANTOGRAPH_RAISE_LINE_VOLTAGE_DETECT *)
        bPantographRaiseCommand := TRUE;
        bVCBCloseCommand := FALSE;
        
        (* Verify pantograph has made solid contact and 25 kV AC line voltage is detected *)
        IF (rVotedPantoForce_N >= 90.0) AND (rCatenaryLineVoltage_kV >= 19.0) AND (rCatenaryLineVoltage_kV <= 29.5) THEN
            IF rFSM_StateTimer_s > 1.50 THEN
                nFSM_CurrentState := 2;
                rFSM_StateTimer_s := 0.0;
            END_IF;
        ELSIF rFSM_StateTimer_s > 8.00 THEN
            (* Timeout raising pantograph or no catenary voltage *)
            nFSM_CurrentState := 13; (* Lower pantograph and isolate *)
            rFSM_StateTimer_s := 0.0;
        END_IF;

    2: (* STATE 2: VCB_CLOSE_DC_LINK_PRECHARGE *)
        bPantographRaiseCommand := TRUE;
        bVCBCloseCommand := TRUE; (* Close 25 kV Vacuum Circuit Breaker *)
        
        (* Pre-charge DC link filter capacitor bank through current-limiting resistors *)
        IF (rVotedDCLinkVoltage_V >= 2650.0) AND (rFSM_StateTimer_s > 0.80) THEN
            nFSM_CurrentState := 3;
            rFSM_StateTimer_s := 0.0;
        ELSIF rFSM_StateTimer_s > 5.00 THEN
            (* Pre-charge timeout or short circuit in DC bus *)
            bVCBCloseCommand := FALSE;
            nFSM_CurrentState := 13;
            rFSM_StateTimer_s := 0.0;
        END_IF;

    3: (* STATE 3: TRACTION_STANDBY_INVERTER_READY *)
        bTCUReady := TRUE;
        bBCUReady := TRUE;
        bPantographRaiseCommand := TRUE;
        bVCBCloseCommand := TRUE;
        
        IF bNeutralSectionBeaconDetected THEN
            nFSM_CurrentState := 11; (* Approach neutral section *)
            rFSM_StateTimer_s := 0.0;
        ELSIF bBrakingEnableCmd OR (rDriverBrakeNotch_pct > 1.0) THEN
            nFSM_CurrentState := 8; (* Enter service braking *)
            rFSM_StateTimer_s := 0.0;
        ELSIF bTractionEnableCmd AND (rDriverTractionNotch_pct > 1.0) THEN
            nFSM_CurrentState := 4; (* Enter acceleration *)
            rFSM_StateTimer_s := 0.0;
        END_IF;

    4: (* STATE 4: ATO_TRACTION_TORQUE_RAMP_ACCELERATION *)
        bTCUReady := TRUE;
        bBCUReady := TRUE;
        bPantographRaiseCommand := TRUE;
        bVCBCloseCommand := TRUE;
        
        (* Check if macro-slip occurs *)
        IF (nWSSP_Phase_Axle1 > 0) OR (nWSSP_Phase_Axle2 > 0) OR (rEstimatedWheelSlip_A1_pct > 6.0) THEN
            nFSM_CurrentState := 7; (* Divert to slip mitigation *)
            rFSM_StateTimer_s := 0.0;
        ELSIF bNeutralSectionBeaconDetected THEN
            nFSM_CurrentState := 11;
            rFSM_StateTimer_s := 0.0;
        ELSIF bBrakingEnableCmd OR (rDriverBrakeNotch_pct > 1.0) THEN
            nFSM_CurrentState := 8;
            rFSM_StateTimer_s := 0.0;
        ELSIF rVotedTrainSpeed_kmh >= MOTOR_BASE_SPEED_KMH THEN
            nFSM_CurrentState := 5; (* Transition to high-speed field weakening *)
            rFSM_StateTimer_s := 0.0;
        ELSIF (rDriverTractionNotch_pct <= 0.5) AND NOT bTractionEnableCmd THEN
            nFSM_CurrentState := 3; (* Return to standby *)
            rFSM_StateTimer_s := 0.0;
        END_IF;

    5: (* STATE 5: HIGH_SPEED_FIELD_WEAKENING_CRUISE *)
        bTCUReady := TRUE;
        bBCUReady := TRUE;
        bPantographRaiseCommand := TRUE;
        bVCBCloseCommand := TRUE;
        
        (* In field weakening regime (120 to 350 km/h) *)
        IF (rObservedAdhesionCoeff < 0.14) AND (rEstimatedWheelSlip_A1_pct > 2.5) THEN
            nFSM_CurrentState := 6; (* Enter micro-slip search *)
            rFSM_StateTimer_s := 0.0;
        ELSIF (nWSSP_Phase_Axle1 > 0) OR (nWSSP_Phase_Axle2 > 0) THEN
            nFSM_CurrentState := 7;
            rFSM_StateTimer_s := 0.0;
        ELSIF bNeutralSectionBeaconDetected THEN
            nFSM_CurrentState := 11;
            rFSM_StateTimer_s := 0.0;
        ELSIF bBrakingEnableCmd OR (rDriverBrakeNotch_pct > 1.0) THEN
            nFSM_CurrentState := 8;
            rFSM_StateTimer_s := 0.0;
        ELSIF rVotedTrainSpeed_kmh < (MOTOR_BASE_SPEED_KMH - 5.0) THEN
            nFSM_CurrentState := 4;
            rFSM_StateTimer_s := 0.0;
        END_IF;

    6: (* STATE 6: CURTIUS_KNIFFLER_MICRO_SLIP_OPTIMIZATION *)
        bTCUReady := TRUE;
        bBCUReady := TRUE;
        bPantographRaiseCommand := TRUE;
        bVCBCloseCommand := TRUE;
        
        (* Dither torque to seek peak dMu/ds = 0 *)
        IF (nWSSP_Phase_Axle1 > 0) OR (nWSSP_Phase_Axle2 > 0) THEN
            nFSM_CurrentState := 7;
            rFSM_StateTimer_s := 0.0;
        ELSIF bBrakingEnableCmd OR (rDriverBrakeNotch_pct > 1.0) THEN
            nFSM_CurrentState := 8;
            rFSM_StateTimer_s := 0.0;
        ELSIF (rObservedAdhesionCoeff >= 0.20) AND (rFSM_StateTimer_s > 0.50) THEN
            IF rVotedTrainSpeed_kmh >= MOTOR_BASE_SPEED_KMH THEN
                nFSM_CurrentState := 5;
            ELSE
                nFSM_CurrentState := 4;
            END_IF;
            rFSM_StateTimer_s := 0.0;
        END_IF;

    7: (* STATE 7: WSSP_ACTIVE_SLIP_SLIDE_RECOVERY *)
        bTCUReady := TRUE;
        bBCUReady := TRUE;
        bPantographRaiseCommand := TRUE;
        bVCBCloseCommand := TRUE;
        
        (* In active slip recovery, derate motoring torque by 50% *)
        IF (nWSSP_Phase_Axle1 = 0) AND (nWSSP_Phase_Axle2 = 0) AND 
           (ABS(rEstimatedWheelSlip_A1_pct) < 2.0) AND (ABS(rEstimatedWheelSlip_A2_pct) < 2.0) THEN
            IF rFSM_StateTimer_s > 0.40 THEN
                IF bBrakingEnableCmd OR (rDriverBrakeNotch_pct > 1.0) THEN
                    nFSM_CurrentState := 8;
                ELSIF rVotedTrainSpeed_kmh >= MOTOR_BASE_SPEED_KMH THEN
                    nFSM_CurrentState := 5;
                ELSE
                    nFSM_CurrentState := 4;
                END_IF;
                rFSM_StateTimer_s := 0.0;
            END_IF;
        END_IF;

    8: (* STATE 8: SERVICE_BRAKING_REGENERATIVE_ED *)
        bTCUReady := TRUE;
        bBCUReady := TRUE;
        bPantographRaiseCommand := TRUE;
        bVCBCloseCommand := TRUE;
        
        IF (nWSSP_Phase_Axle1 > 0) OR (nWSSP_Phase_Axle2 > 0) THEN
            nFSM_CurrentState := 7;
            rFSM_StateTimer_s := 0.0;
        ELSIF rVotedTrainSpeed_kmh < 45.0 THEN
            nFSM_CurrentState := 9; (* Blend in friction brake at lower speeds *)
            rFSM_StateTimer_s := 0.0;
        ELSIF (rDriverBrakeNotch_pct <= 0.5) AND NOT bBrakingEnableCmd THEN
            nFSM_CurrentState := 3; (* Return to standby *)
            rFSM_StateTimer_s := 0.0;
        END_IF;

    9: (* STATE 9: BLENDED_EP_PNEUMATIC_DECELERATION *)
        bTCUReady := TRUE;
        bBCUReady := TRUE;
        bPantographRaiseCommand := TRUE;
        bVCBCloseCommand := TRUE;
        
        IF (nWSSP_Phase_Axle1 > 0) OR (nWSSP_Phase_Axle2 > 0) THEN
            nFSM_CurrentState := 7;
            rFSM_StateTimer_s := 0.0;
        ELSIF rVotedTrainSpeed_kmh < 0.25 THEN
            nFSM_CurrentState := 10; (* Full standstill stop *)
            rFSM_StateTimer_s := 0.0;
        ELSIF (rDriverBrakeNotch_pct <= 0.5) AND NOT bBrakingEnableCmd THEN
            nFSM_CurrentState := 3;
            rFSM_StateTimer_s := 0.0;
        END_IF;

    10: (* STATE 10: STANDSTILL_ELECTRO_PNEUMATIC_HOLD_PARK *)
        bTCUReady := TRUE;
        bBCUReady := TRUE;
        bPantographRaiseCommand := TRUE;
        bVCBCloseCommand := TRUE;
        
        (* Apply maximum cylinder holding pressure at standstill *)
        rPneumaticBrakePressure_SP_bar := 3.80;
        rTractionTorqueCommand_kNm := 0.0;
        rRegenerativeBrakeTorque_kNm := 0.0;
        
        IF (rDriverTractionNotch_pct > 1.0) AND bTractionEnableCmd AND (rDriverBrakeNotch_pct <= 0.5) THEN
            nFSM_CurrentState := 4; (* Start tractive ramp *)
            rFSM_StateTimer_s := 0.0;
        ELSIF NOT bSystemEnable THEN
            nFSM_CurrentState := 13;
            rFSM_StateTimer_s := 0.0;
        END_IF;

    11: (* STATE 11: NEUTRAL_SECTION_PHASE_BREAK_COASTING *)
        bTCUReady := FALSE;
        bBCUReady := TRUE;
        bPantographRaiseCommand := TRUE;
        bVCBCloseCommand := FALSE; (* Open VCB to isolate from phase break *)
        
        rTractionTorqueCommand_kNm := 0.0;
        rRegenerativeBrakeTorque_kNm := 0.0;
        
        (* Coast through unpowered section *)
        IF NOT bNeutralSectionBeaconDetected AND (rFSM_StateTimer_s > 4.50) THEN
            nFSM_CurrentState := 2; (* Re-close VCB and restore traction *)
            rFSM_StateTimer_s := 0.0;
        END_IF;

    12: (* STATE 12: EMERGENCY_BRAKE_FAILSAFE_DE_ENERGIZE *)
        bTCUReady := FALSE;
        bBCUReady := TRUE;
        bVCBCloseCommand := FALSE; (* Trip main circuit breaker *)
        bPantographRaiseCommand := TRUE;
        bEmergencyTripActive := TRUE;
        
        (* Maximum Emergency Braking: Inverter torque zeroed, maximum friction pressure applied *)
        rTractionTorqueCommand_kNm := 0.0;
        rRegenerativeBrakeTorque_kNm := 0.0;
        rPneumaticBrakePressure_SP_bar := 3.80;
        
        IF bEmergencyBrakeLoop AND bAlarmReset AND (rVotedTrainSpeed_kmh < 0.20) THEN
            bEmergencyTripActive := FALSE;
            nFSM_CurrentState := 0; (* Reset back to initialization *)
            rFSM_StateTimer_s := 0.0;
        END_IF;

    13: (* STATE 13: SAFE_SHUTDOWN_PANTOGRAPH_LOWER *)
        bTCUReady := FALSE;
        bBCUReady := FALSE;
        bVCBCloseCommand := FALSE;
        bPantographRaiseCommand := FALSE; (* Lower pantograph *)
        rPneumaticBrakePressure_SP_bar := 3.80;
        rTractionTorqueCommand_kNm := 0.0;
        rRegenerativeBrakeTorque_kNm := 0.0;
        
        IF bSystemEnable AND (rFSM_StateTimer_s > 5.00) THEN
            nFSM_CurrentState := 0;
            rFSM_StateTimer_s := 0.0;
        END_IF;
ELSE
    nFSM_CurrentState := 0;
END_CASE;

nOperationalState := nFSM_CurrentState;
'''
