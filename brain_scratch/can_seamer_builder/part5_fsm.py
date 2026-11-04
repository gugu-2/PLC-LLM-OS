# brain_scratch/can_seamer_builder/part5_fsm.py

PART5_FSM = """
(* ==========================================================================================
 * PHASE 6: 12-STAGE OPERATIONAL FINITE STATE MACHINE (FSM)
 * Full industrial cycle sequence governing steam pre-sterilization, cryogenic chill-down,
 * electronic cam synchronization, micro-dosing, double-seam operations, metrology,
 * acoustic leak rejection, CIP wash, and emergency jam retraction.
 * ========================================================================================== *)

(* State Timer Accumulation *)
IF NOT bState_First_Scan THEN
    rState_Timer_s := rState_Timer_s + rDeltaT;
ELSE
    rState_Timer_s := 0.0;
    bState_First_Scan := FALSE;
END_IF;

(* Master Safety E-Stop Override to State 12 *)
IF NOT bEStop_Ok OR bAlarm_TurretJam_Fault OR bDischarge_Jam_Sensor THEN
    IF iState <> 12 THEN
        iNextState := 12; (* Force Emergency Retract State *)
    END_IF;
END_IF;

(* Synchronous State Transition Handling *)
IF iNextState <> iState THEN
    iState := iNextState;
    bState_First_Scan := TRUE;
    rState_Timer_s := 0.0;
END_IF;

iCurrent_FSM_State := iState;

CASE iState OF
    (* --------------------------------------------------------------------------------------
     * STATE 1: STATE_STEAM_BARRIER_PURGE_125C
     * Pre-sterilization saturated steam purge of the rotary labyrinth turret enclosure.
     * Brings enclosure temperature to >= 125.0 deg C before opening product paths.
     * -------------------------------------------------------------------------------------- *)
    1:
        bSystem_Ready := FALSE;
        bIn_Production := FALSE;
        bEStop_Tripped := FALSE;
        rTurret_Speed_Command_RPM := 0.0;
        bCan_Lifter_ChamberPneumatic_Up := FALSE;
        bLN2_Dosing_Valve_Trigger := FALSE;
        bAcoustic_Ping_Exciter_Trigger := FALSE;
        bReject_Gate_Actuator_Pulse := FALSE;

        (* Modulate Saturated Steam Valve to warm up enclosure *)
        IF rVoted_SteamBarrier_Temp_degC < 125.0 THEN
            rSteamBarrier_Valve_Position_Pct := MIN(100.0, 65.0 + (125.0 - rVoted_SteamBarrier_Temp_degC) * 2.5);
        ELSE
            rSteamBarrier_Valve_Position_Pct := 35.0 + au_Control[4];
        END_IF;

        (* Transition check: Temperature attained and dwell time satisfied *)
        IF bEnable AND bSterileSteam_Permissive THEN
            IF rVoted_SteamBarrier_Temp_degC >= 124.5 AND rState_Timer_s >= tDwell_SteamPurge_Target_s THEN
                iNextState := 2; (* Advance to Cryogenic Chill-Down *)
            END_IF;
        END_IF;

        (* CIP Request Branch *)
        IF bCIP_Wash_Request THEN
            iNextState := 11;
        END_IF;

    (* --------------------------------------------------------------------------------------
     * STATE 2: STATE_LN2_CHILLDOWN_MINUS196C
     * Cryogenic liquid nitrogen line vacuum jacket sub-cooling down to -196 deg C.
     * Stabilizes cryogenic supply manifold pressure to 1.8 - 3.2 bar.
     * -------------------------------------------------------------------------------------- *)
    2:
        bSystem_Ready := FALSE;
        bIn_Production := FALSE;
        rTurret_Speed_Command_RPM := 0.0;
        bCan_Lifter_ChamberPneumatic_Up := FALSE;
        bLN2_Dosing_Valve_Trigger := FALSE;

        (* Maintain Steam Barrier *)
        rSteamBarrier_Valve_Position_Pct := 35.0 + au_Control[4];

        (* Cryogenic Nitrogen Venting & Pressure Regulation *)
        IF bLN2_Dosing_Permissive THEN
            (* Check Manifold Temperature reaches cryogenic saturation point *)
            IF rLN2_ManifoldTemp_degC <= -190.0 AND rVoted_LN2_Pressure_bar >= 1.80 AND 
               rState_Timer_s >= tDwell_LN2Chill_Target_s THEN
                iNextState := 3; (* Advance to Infeed Synchronization Inching *)
            END_IF;
        ELSE
            (* Hold state until cryogenic permissive is granted *)
            rState_Timer_s := 0.0;
        END_IF;

    (* --------------------------------------------------------------------------------------
     * STATE 3: STATE_INFEED_TURRET_SYNC_INCHING
     * Low-speed jog / inching (10.0 RPM) to home electronic cams and phase align the infeed
     * timing worm screw, container transfer starwheel, and 18-head rotary seaming chucks.
     * -------------------------------------------------------------------------------------- *)
    3:
        bSystem_Ready := FALSE;
        bIn_Production := FALSE;
        rTurret_Speed_Command_RPM := 10.0; (* Inching crawl speed *)
        bCan_Lifter_ChamberPneumatic_Up := FALSE;
        bLN2_Dosing_Valve_Trigger := FALSE;

        (* Phase Alignment Gearing Control *)
        rInfeed_Phase_Trim_Deg := (rInfeed_WormScrew_Phase_Deg - rTurret_Angular_Pos_Deg);
        WHILE rInfeed_Phase_Trim_Deg > 180.0 DO
            rInfeed_Phase_Trim_Deg := rInfeed_Phase_Trim_Deg - 360.0;
        END_WHILE;
        WHILE rInfeed_Phase_Trim_Deg < -180.0 DO
            rInfeed_Phase_Trim_Deg := rInfeed_Phase_Trim_Deg + 360.0;
        END_WHILE;

        (* Starwheel pocket phase trim *)
        rInfeed_Starwheel_Phase_Trim_Deg := au_Control[5] * 0.05729578; (* Convert mrad to deg *)

        (* Transition check: Phase error minimized and dwell timer expired *)
        IF ABS(rInfeed_Phase_Trim_Deg) < 1.50 AND rState_Timer_s >= tDwell_SyncInching_Target_s THEN
            bSystem_Ready := TRUE;
            IF bEnable THEN
                iNextState := 4; (* Advance to Container Infeed & Production Ramp *)
            END_IF;
        END_IF;

    (* --------------------------------------------------------------------------------------
     * STATE 4: STATE_CAN_INFEED_LID_FEED_GATE
     * High-speed production indexing (ramp to 66.67 RPM = 1200 cans/min).
     * Can body detected by optical sensor; lid / end downstack knife gate releases end.
     * -------------------------------------------------------------------------------------- *)
    4:
        bSystem_Ready := TRUE;
        bIn_Production := TRUE;
        rTurret_Speed_Command_RPM := rSP_Turret_Speed_RPM + au_Control[1];
        rInfeed_Phase_Trim_Deg := au_Control[5] * 0.05729578;

        (* End Downstack Rotary Knife Release Solenoid *)
        IF bCan_Present_Infeed AND bEnd_Present_Chute THEN
            bLid_Separator_Release_Solenoid := TRUE;
            (* Register infeed shift register *)
            abPocket_HasCan[1] := TRUE;
            abPocket_HasEnd[1] := TRUE;
            aiPocket_HeadOrigin[1] := iActive_Head_ID;
        ELSE
            bLid_Separator_Release_Solenoid := FALSE;
            abPocket_HasCan[1] := FALSE;
            abPocket_HasEnd[1] := FALSE;
        END_IF;

        (* Transition to Liquid Nitrogen Headspace Dosing *)
        iNextState := 5;

    (* --------------------------------------------------------------------------------------
     * STATE 5: STATE_LN2_HEADSPACE_MICRODOSING
     * Precise millisecond cryogenic micro-valve pulsed dosing into open can headspace
     * immediately before lid placement to displace oxygen and provide structural rigidity.
     * -------------------------------------------------------------------------------------- *)
    5:
        bSystem_Ready := TRUE;
        bIn_Production := TRUE;
        rTurret_Speed_Command_RPM := rSP_Turret_Speed_RPM + au_Control[1];

        (* Compute speed-proportional pulse width with MPC trim *)
        rLN2_InjectorPulse_ms := (rSP_LN2_DosingPulse_ms + au_Control[3]) * 
                                 (rTurret_Speed_Actual_RPM / MAX(10.0, rSP_Turret_Speed_RPM));
        rLN2_InjectorPulse_ms := MAX(3.0, MIN(30.0, rLN2_InjectorPulse_ms));

        (* Micro-Valve Pulse Generation *)
        IF abPocket_HasCan[2] AND bLN2_Dosing_Permissive THEN
            bLN2_Dosing_Valve_Trigger := TRUE;
            rLN2_Pulse_Timer_s := rLN2_Pulse_Timer_s + rDeltaT;
            IF rLN2_Pulse_Timer_s >= (rLN2_InjectorPulse_ms / 1000.0) THEN
                bLN2_Dosing_Valve_Trigger := FALSE;
                abPocket_DosedLN2[2] := TRUE;
                rLN2_Pulse_Timer_s := 0.0;
                iNextState := 6; (* Advance to 1st Operation Roll Engage *)
            END_IF;
        ELSE
            bLN2_Dosing_Valve_Trigger := FALSE;
            rLN2_Pulse_Timer_s := 0.0;
            iNextState := 6;
        END_IF;

    (* --------------------------------------------------------------------------------------
     * STATE 6: STATE_1ST_OP_CURL_ROLL_ENGAGE
     * Lifter table raises container against seaming chuck (axial force 3.5 to 8.0 kN).
     * 1st Operation Curl Roll servo cam engages to interlock can body hook and cover hook.
     * -------------------------------------------------------------------------------------- *)
    6:
        bSystem_Ready := TRUE;
        bIn_Production := TRUE;
        rTurret_Speed_Command_RPM := rSP_Turret_Speed_RPM + au_Control[1];

        (* Engage pneumatic lifter chuck preload *)
        bCan_Lifter_ChamberPneumatic_Up := TRUE;

        (* Calculate dynamic 1st operation roll cam depth trim *)
        rSeamingRoll_1stOp_CamTrim_mm := au_Control[6] + aHead_CalibOffset_1stOp_mm[iActive_Head_ID];
        rSeamingRoll_1stOp_CamTrim_mm := MAX(-0.45, MIN(0.45, rSeamingRoll_1stOp_CamTrim_mm));

        (* Verify Axial Chuck Preload is within hermetic threshold *)
        IF rVoted_Chuck_AxialLoad_kN < rTrip_AxialLoad_L_kN THEN
            bAlarm_AxialLoad_L := TRUE;
        ELSE
            bAlarm_AxialLoad_L := FALSE;
        END_IF;

        (* Advance to 2nd Operation Flattening Roll *)
        iNextState := 7;

    (* --------------------------------------------------------------------------------------
     * STATE 7: STATE_2ND_OP_FLATTENING_IRON_DWELL
     * 2nd Operation Flattening / Ironing Roll engages to compress the 5 layers of metal
     * and compound into a hermetic double seam.
     * -------------------------------------------------------------------------------------- *)
    7:
        bSystem_Ready := TRUE;
        bIn_Production := TRUE;
        rTurret_Speed_Command_RPM := rSP_Turret_Speed_RPM + au_Control[1];
        bCan_Lifter_ChamberPneumatic_Up := TRUE;

        (* Calculate dynamic 2nd operation roll cam depth trim *)
        rSeamingRoll_2ndOp_CamTrim_mm := (au_Control[6] * 0.75) + aHead_CalibOffset_2ndOp_mm[iActive_Head_ID];
        rSeamingRoll_2ndOp_CamTrim_mm := MAX(-0.30, MIN(0.30, rSeamingRoll_2ndOp_CamTrim_mm));

        (* Retract roll and advance to Laser Gauging *)
        abPocket_SeamedOK[4] := TRUE;
        iNextState := 8;

    (* --------------------------------------------------------------------------------------
     * STATE 8: STATE_LASER_SEAM_GAUGING_ONLINE
     * Online non-contact laser triangulation profiling of double seam thickness,
     * seam height, and countersink depth on the rotating container.
     * -------------------------------------------------------------------------------------- *)
    8:
        bSystem_Ready := TRUE;
        bIn_Production := TRUE;
        rTurret_Speed_Command_RPM := rSP_Turret_Speed_RPM + au_Control[1];

        (* Seam Metrology Quality Bounds Verification *)
        IF (rLaser_SeamThickness_mm > rTrip_Thickness_HH_mm) OR 
           (rLaser_SeamThickness_mm < rTrip_Thickness_LL_mm) OR 
           (rSeam_TheoreticalOverlap_Pct < 60.0) THEN
            abPocket_RejectPending[5] := TRUE;
            bAlarm_SeamThickness_Fault := TRUE;
        ELSE
            bAlarm_SeamThickness_Fault := FALSE;
        END_IF;

        (* Advance to Acoustic Leak Inspection *)
        iNextState := 9;

    (* --------------------------------------------------------------------------------------
     * STATE 9: STATE_ACOUSTIC_PING_LEAK_INSPECT
     * Piezoelectric impulse striker excites can end dome; sound pressure sensor array
     * measures resonant frequency spectrum to detect micro-leaks, bulges, or missing N2.
     * -------------------------------------------------------------------------------------- *)
    9:
        bSystem_Ready := TRUE;
        bIn_Production := TRUE;
        rTurret_Speed_Command_RPM := rSP_Turret_Speed_RPM + au_Control[1];

        (* Fire Acoustic Striker Hammer Impulse Pulse *)
        bAcoustic_Ping_Exciter_Trigger := TRUE;
        rAcoustic_Pulse_Timer_s := rAcoustic_Pulse_Timer_s + rDeltaT;

        IF rAcoustic_Pulse_Timer_s >= 0.005 THEN (* 5 millisecond pulse *)
            bAcoustic_Ping_Exciter_Trigger := FALSE;
            rAcoustic_Pulse_Timer_s := 0.0;

            (* Evaluate Acoustic Resonance & Residual Oxygen Integrity *)
            IF bAcoustic_Defect_Detected OR (rVoted_AcousticResonance_kHz < rTrip_Acoustic_LL_kHz) OR
               (rResidual_Oxygen_Pct > rTrip_ResidualO2_HH_Pct) THEN
                abPocket_RejectPending[6] := TRUE;
                bAlarm_Acoustic_Leak_Fault := TRUE;
            ELSE
                abPocket_AcousticPass[6] := TRUE;
                bAlarm_Acoustic_Leak_Fault := FALSE;
            END_IF;

            (* Advance to Rejection Gate *)
            iNextState := 10;
        END_IF;

    (* --------------------------------------------------------------------------------------
     * STATE 10: STATE_REJECTION_GATE_ACTUATION
     * High-speed pneumatic reject gate diverts out-of-spec or unpressurized containers
     * into reject bin while good containers pass to downstream aseptic packaging.
     * -------------------------------------------------------------------------------------- *)
    10:
        bSystem_Ready := TRUE;
        bIn_Production := TRUE;
        rTurret_Speed_Command_RPM := rSP_Turret_Speed_RPM + au_Control[1];

        (* Discharge Starwheel Diverter Gate Decision *)
        IF abPocket_RejectPending[7] THEN
            bReject_Gate_Actuator_Pulse := TRUE;
            rReject_Pulse_Timer_s := rReject_Pulse_Timer_s + rDeltaT;
            IF rReject_Pulse_Timer_s >= 0.025 THEN (* 25 ms blow-off pulse *)
                bReject_Gate_Actuator_Pulse := FALSE;
                rReject_Pulse_Timer_s := 0.0;
                diTotal_Cans_Rejected := diTotal_Cans_Rejected + 1;
                IF aiPocket_HeadOrigin[7] >= 1 AND aiPocket_HeadOrigin[7] <= 18 THEN
                    aHead_RejectCount[aiPocket_HeadOrigin[7]] := aHead_RejectCount[aiPocket_HeadOrigin[7]] + 1;
                END_IF;
                abPocket_RejectPending[7] := FALSE;
            END_IF;
        ELSE
            bReject_Gate_Actuator_Pulse := FALSE;
            rReject_Pulse_Timer_s := 0.0;
            diTotal_Cans_Processed := diTotal_Cans_Processed + 1;
        END_IF;

        (* Loop back to container indexing for continuous rotary flow *)
        iNextState := 4;

    (* --------------------------------------------------------------------------------------
     * STATE 11: STATE_ROTARY_CIP_SIP_SANITIZATION
     * Rotary Clean-In-Place / Steam-In-Place sequence: slow rotation, direct chemical
     * spray wash, saturated steam barrier soaking at 130 deg C, sterile air purge.
     * -------------------------------------------------------------------------------------- *)
    11:
        bSystem_Ready := FALSE;
        bIn_Production := FALSE;
        rTurret_Speed_Command_RPM := 15.0; (* Slow wash rotation *)
        bCan_Lifter_ChamberPneumatic_Up := FALSE;
        bLN2_Dosing_Valve_Trigger := FALSE;
        bAcoustic_Ping_Exciter_Trigger := FALSE;
        bReject_Gate_Actuator_Pulse := FALSE;

        (* High Temperature Steam Barrier Soaking *)
        rSteamBarrier_Valve_Position_Pct := 85.0;

        (* Dwell check *)
        IF rState_Timer_s >= tDwell_CIP_Target_s AND NOT bCIP_Wash_Request THEN
            iNextState := 1; (* Return to Pre-Sterilization Warmup *)
        END_IF;

    (* --------------------------------------------------------------------------------------
     * STATE 12: STATE_JAM_ESTOP_CLAMP_RETRACT
     * Critical safety abort: drive motor torque disabled, seaming chuck lifters dropped,
     * seaming rolls retracted, cryogenic valve isolated.
     * -------------------------------------------------------------------------------------- *)
    12:
        bSystem_Ready := FALSE;
        bIn_Production := FALSE;
        bEStop_Tripped := TRUE;
        rTurret_Speed_Command_RPM := 0.0;
        bCan_Lifter_ChamberPneumatic_Up := FALSE;
        bLN2_Dosing_Valve_Trigger := FALSE;
        bAcoustic_Ping_Exciter_Trigger := FALSE;
        bReject_Gate_Actuator_Pulse := FALSE;
        bLid_Separator_Release_Solenoid := FALSE;
        rSeamingRoll_1stOp_CamTrim_mm := 0.0;
        rSeamingRoll_2ndOp_CamTrim_mm := 0.0;

        (* Maintain Steam Barrier to preserve aseptic zone *)
        rSteamBarrier_Valve_Position_Pct := 40.0;

        (* Reset Interlock Handling *)
        IF bReset_Faults AND bEStop_Ok AND NOT bDischarge_Jam_Sensor THEN
            bAlarm_TurretJam_Fault := FALSE;
            bAlarm_Discharge_Jam := FALSE;
            bAlarm_AxialLoad_HH := FALSE;
            bAlarm_AxialLoad_LL := FALSE;
            iNextState := 1; (* Return to State 1 after reset *)
        END_IF;

    ELSE
        iNextState := 1;
END_CASE;
"""
