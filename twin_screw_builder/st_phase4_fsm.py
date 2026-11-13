(* =====================================================================================================================
 * PHASE 4: 14-STAGE DETERMINISTIC PRODUCTION FINITE STATE MACHINE (FSM)
 * Controls full automated extrusion lifecycle from cold barrel pre-heat to high-rate compounding and shutdown.
 * ===================================================================================================================== *)

(* Master Safety Line & Protective Trip Immediate Override *)
IF (NOT bSafetyLine_Healthy_In) OR (NOT bRuptureDisc_Intact_In) OR bTripInterlocked_Out THEN
    uiCurrentState := STATE_EMERGENCY_OVERLOAD;
END_IF;

(* Advance Universal State Execution Dwell Timer *)
tStateDwellTimer := tStateDwellTimer + T_SAMPLE;

CASE uiCurrentState OF

    (* -----------------------------------------------------------------------------------------------------------------
     * STATE 0: MACHINE OFFLINE & SAFETY INTERLOCK VERIFICATION
     * ----------------------------------------------------------------------------------------------------------------- *)
    STATE_IDLE_INTERLOCKS:
        uiCurrentSubState := 0;
        rScrewSpeedTarget := 0.0;
        rGearPumpSpeedTarget := 0.0;
        rSideFeederSpeed_Cmd_Out := 0.0;
        rPelletCutterSpeed_Cmd_Out := 0.0;
        rFeeder_CmdFlow_01_Out := 0.0;
        rFeeder_CmdFlow_02_Out := 0.0;
        rFeeder_CmdFlow_03_Out := 0.0;
        rFeeder_CmdFlow_04_Out := 0.0;
        rFeeder_CmdFlow_05_Out := 0.0;
        bVacuumPump_Run_Out := FALSE;
        rVacuumThrottle_Cmd_Out := 0.0;
        bWaterBox_Clamp_Out := FALSE;
        bWaterBox_Diverter_Out := FALSE;
        bWaterCircPump_Run_Out := FALSE;
        rWaterTrimHeat_Cmd_Out := 0.0;
        bDieFastDump_Valve_Out := FALSE;

        (* Verify Plant Readiness Criteria *)
        IF bSafetyLine_Healthy_In AND bRuptureDisc_Intact_In AND bMasterEnable_In AND (NOT bTripInterlocked_Out) THEN
            bExtruderReady_Out := TRUE;
            IF bAutoMode_Cmd_In THEN
                uiCurrentState := STATE_BARREL_COLD_SOAK;
                tStateDwellTimer := 0.0;
                uiCurrentSubState := 1;
            END_IF;
        ELSE
            bExtruderReady_Out := FALSE;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STATE 1: 12-ZONE BARREL COLD SOAK PRE-HEATING CASCADE
     * Progressively warms all 12 zones to target soak recipes to minimize differential thermal expansion stresses.
     * ----------------------------------------------------------------------------------------------------------------- *)
    STATE_BARREL_COLD_SOAK:
        bExtruderReady_Out := FALSE;
        rScrewSpeedTarget := 0.0;
        rGearPumpSpeedTarget := 0.0;
        bDieFastDump_Valve_Out := FALSE;

        (* Verify whether all 12 zones have reached within 5.0 °C of target setpoints *)
        rCalc_TempA := 0.0;
        FOR idx_z := 2 TO 12 DO (* Zone 1 is water-cooled feed throat, maintained cold *)
            IF ABS(rPID_Zone_Err[idx_z]) > 5.0 THEN
                rCalc_TempA := rCalc_TempA + 1.0;
            END_IF;
        END_FOR;

        (* If all heated zones (Zones 2..12) have reached target soak temperatures, proceed to soak hold *)
        IF (rCalc_TempA = 0.0) AND (tStateDwellTimer >= 60.0) THEN
            uiCurrentState := STATE_THERMAL_EQUILIBRIUM;
            tStateDwellTimer := 0.0;
            tSoakHoldTimer := 0.0;
            uiCurrentSubState := 1;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STATE 2: DEEP CORE THERMAL EQUILIBRIUM SOAK HOLD (1800 s DWELL)
     * Critical safety dwell ensuring 133mm alloy screw core and heavy barrel walls achieve complete thermal penetration.
     * ----------------------------------------------------------------------------------------------------------------- *)
    STATE_THERMAL_EQUILIBRIUM:
        tSoakHoldTimer := tSoakHoldTimer + T_SAMPLE;
        uiCurrentSubState := 2;

        (* Verify no zone has experienced thermal runaway *)
        rCalc_TempA := 0.0;
        FOR idx_z := 2 TO 12 DO
            IF ABS(rPID_Zone_Err[idx_z]) > 8.0 THEN
                rCalc_TempA := rCalc_TempA + 1.0;
            END_IF;
        END_FOR;

        (* 1800.0 seconds (30 minutes) mandatory core soak hold *)
        IF (tSoakHoldTimer >= 1800.0) AND (rCalc_TempA = 0.0) THEN
            uiCurrentState := STATE_FEEDER_CALIBRATION;
            tStateDwellTimer := 0.0;
            uiCurrentSubState := 1;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STATE 3: GRAVIMETRIC LOSS-IN-WEIGHT (LIW) FEEDER TARE & CALIBRATION CHECK
     * Verifies load cell tare stability, hopper slide gates, and refill valves prior to screw rotation.
     * ----------------------------------------------------------------------------------------------------------------- *)
    STATE_FEEDER_CALIBRATION:
        uiCurrentSubState := 3;
        rScrewSpeedTarget := 0.0;
        rGearPumpSpeedTarget := 0.0;

        (* 15-second diagnostic self-check period for all 5 gravimetric feeders *)
        IF tStateDwellTimer >= 15.0 THEN
            uiCurrentState := STATE_SCREW_INCHING_PURGE;
            tStateDwellTimer := 0.0;
            tInchingVerifyTimer := 0.0;
            uiCurrentSubState := 1;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STATE 4: SCREW LOW-SPEED INCHING & COLD PURGE VERIFICATION
     * Inching screw at 15.0 rpm to detect any un-melted solid cold polymer slugs or mechanical binding before feed.
     * ----------------------------------------------------------------------------------------------------------------- *)
    STATE_SCREW_INCHING_PURGE:
        uiCurrentSubState := 4;
        rScrewSpeedTarget := 15.0; (* 15.0 rpm inching speed *)
        rGearPumpSpeedTarget := 0.0;
        tInchingVerifyTimer := tInchingVerifyTimer + T_SAMPLE;

        (* Inching torque safety clamp: If torque exceeds 1,800 Nm at 15 rpm, abort to protect screw flights *)
        IF (rVoted_ScrewTorque_Out > 1800.0) AND (tInchingVerifyTimer > 5.0) THEN
            uiCurrentState := STATE_EMERGENCY_OVERLOAD;
        END_IF;

        (* 30 seconds of free inching with torque below 1,200 Nm confirms drive train is unobstructed *)
        IF (tInchingVerifyTimer >= 30.0) AND (rVoted_ScrewTorque_Out <= 1200.0) THEN
            uiCurrentState := STATE_RAW_POLYMER_RAMP;
            tStateDwellTimer := 0.0;
            rFeedRampScalar := 0.0;
            uiCurrentSubState := 1;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STATE 5: PRIMARY POLYMER RESIN GRAVIMETRIC FEED RAMP (RAMP TO 30% RATE)
     * Starts Feeder 1 (primary resin) and ramps screw speed synchronously to establish uniform melt seal.
     * ----------------------------------------------------------------------------------------------------------------- *)
    STATE_RAW_POLYMER_RAMP:
        uiCurrentSubState := 5;
        (* Ramp feed scalar smoothly from 0.0 to 0.30 over 120 seconds *)
        IF rFeedRampScalar < 0.30 THEN
            rFeedRampScalar := rFeedRampScalar + (0.30 / 120.0) * T_SAMPLE;
        ELSE
            rFeedRampScalar := 0.30;
        END_IF;

        (* Master flow commands for polymer base components (Feeders 1, 2, 3, 4) *)
        rFeeder_CmdFlow_01_Out := rFeeder_SP_Flow_01_In * rFeedRampScalar;
        rFeeder_CmdFlow_02_Out := rFeeder_SP_Flow_02_In * rFeedRampScalar;
        rFeeder_CmdFlow_03_Out := rFeeder_SP_Flow_03_In * rFeedRampScalar;
        rFeeder_CmdFlow_04_Out := rFeeder_SP_Flow_04_In * rFeedRampScalar;
        rFeeder_CmdFlow_05_Out := 0.0; (* Side-feeder glass fiber held OFF until melt pool established *)

        (* Synchronize screw speed linearly with feed rate (target 180 rpm at 30% feed) *)
        rScrewSpeedTarget := 15.0 + (165.0 * (rFeedRampScalar / 0.30));

        (* Transition once feed scalar reaches 30% and screw torque confirms steady polymer plasticization (> 1,500 Nm) *)
        IF (rFeedRampScalar >= 0.30) AND (tStateDwellTimer >= 140.0) AND (rVoted_ScrewTorque_Out >= 1500.0) THEN
            uiCurrentState := STATE_SIDE_FEEDER_GLASS;
            tStateDwellTimer := 0.0;
            rSideFeederRatioScalar := 0.0;
            uiCurrentSubState := 1;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STATE 6: GLASS FIBER DOWNSTREAM SIDE-FEEDER INTRODUCTION
     * Gradually introduces glass fibers into Zone 5 port once molten polymer matrix is fully fluid.
     * ----------------------------------------------------------------------------------------------------------------- *)
    STATE_SIDE_FEEDER_GLASS:
        uiCurrentSubState := 6;
        (* Ramp glass fiber side feeder from 0.0 to 1.0 of recipe ratio over 90 seconds *)
        IF rSideFeederRatioScalar < 1.0 THEN
            rSideFeederRatioScalar := rSideFeederRatioScalar + (1.0 / 90.0) * T_SAMPLE;
        ELSE
            rSideFeederRatioScalar := 1.0;
        END_IF;

        rFeeder_CmdFlow_05_Out := rFeeder_SP_Flow_05_In * rFeedRampScalar * rSideFeederRatioScalar;
        (* Proportional side-feeder drive speed matching glass fiber mass delivery *)
        rSideFeederSpeed_Cmd_Out := (rFeeder_CmdFlow_05_Out / 900.0) * 350.0;

        IF (rSideFeederRatioScalar >= 1.0) AND (tStateDwellTimer >= 100.0) THEN
            uiCurrentState := STATE_VACUUM_DEGASSING_PULL;
            tStateDwellTimer := 0.0;
            uiCurrentSubState := 1;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STATE 7: ZONE 9 HIGH-VACUUM VENT SKID EVACUATION PULL
     * Starts liquid ring & Roots vacuum pump skid, pulling chamber pressure to -0.85 bar.
     * ----------------------------------------------------------------------------------------------------------------- *)
    STATE_VACUUM_DEGASSING_PULL:
        uiCurrentSubState := 7;
        bVacuumPump_Run_Out := TRUE;
        rVacuumThrottle_Cmd_Out := 85.0; (* 85% open throttle *)

        (* Verify vacuum level drops below -0.65 bar within 45 seconds *)
        IF (rVacuumPres_FB_In <= -0.65) AND (tStateDwellTimer >= 30.0) THEN
            uiCurrentState := STATE_DIE_HEAD_BUILDUP;
            tStateDwellTimer := 0.0;
            uiCurrentSubState := 1;
        ELSIF tStateDwellTimer >= 90.0 THEN
            (* Degassing pull timeout warning *)
            bAlm_VAC_H_Active := TRUE;
            uiCurrentState := STATE_DIE_HEAD_BUILDUP;
            tStateDwellTimer := 0.0;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STATE 8: DIE HEAD MELT FLOW & DIE PRESSURE BUILD-UP
     * Pre-fills screen changer and adapter head, stabilizing die melt pressure towards 60.0 bar.
     * ----------------------------------------------------------------------------------------------------------------- *)
    STATE_DIE_HEAD_BUILDUP:
        uiCurrentSubState := 8;
        bDieFastDump_Valve_Out := FALSE;

        (* Pressure ramp check: Wait until die head melt pressure builds past 35.0 bar *)
        IF (rVoted_DieMeltPres_Out >= 35.0) AND (tStateDwellTimer >= 40.0) THEN
            uiCurrentState := STATE_GEAR_PUMP_SYNC;
            tStateDwellTimer := 0.0;
            uiCurrentSubState := 1;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STATE 9: MELT GEAR PUMP SYNCHRONIZATION & SUCTION PRESSURE LOCK
     * Starts melt pump servo, locking suction pressure at 45.0 bar to guarantee bubble-free gear teeth filling.
     * ----------------------------------------------------------------------------------------------------------------- *)
    STATE_GEAR_PUMP_SYNC:
        uiCurrentSubState := 9;
        (* Start gear pump speed at matched volumetric throughput speed *)
        rGearPumpSpeedTarget := (rOnline_TotalThroughput / (GEAR_PUMP_DISP_M3_REV * POLYMER_MELT_DENSITY * 3600.0 * GEAR_PUMP_VOL_EFFICIENCY));

        (* Check that suction pressure stabilizes in the 40.0 to 50.0 bar operating corridor *)
        IF (rGearPump_SuctPres_In >= 38.0) AND (rGearPump_SuctPres_In <= 52.0) AND (tStateDwellTimer >= 30.0) THEN
            uiCurrentState := STATE_PELLETIZER_SPIN_CLOSE;
            tStateDwellTimer := 0.0;
            tWaterBoxPrimeTimer := 0.0;
            uiCurrentSubState := 1;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STATE 10: UNDERWATER PELLETIZER HUB SPIN & HYDRAULIC WATER BOX CLAMP
     * Spins cutter hub to 2,500 rpm, brings tempered water loop to 65 °C, clamps water box, and switches diverter valve.
     * ----------------------------------------------------------------------------------------------------------------- *)
    STATE_PELLETIZER_SPIN_CLOSE:
        uiCurrentSubState := 10;
        tWaterBoxPrimeTimer := tWaterBoxPrimeTimer + T_SAMPLE;

        (* Step 10.1: Start water circulation pump and trim heating to reach 60-70 °C *)
        bWaterCircPump_Run_Out := TRUE;
        IF rVoted_PelletWaterTemp_Out < 65.0 THEN
            rWaterTrimHeat_Cmd_Out := 80.0;
        ELSE
            rWaterTrimHeat_Cmd_Out := 10.0;
        END_IF;

        (* Step 10.2: Accelerate cutter motor *)
        rPelletCutterSpeed_Cmd_Out := 2500.0;

        (* Step 10.3: Engage hydraulic water box clamp once water temp is >= 58.0 °C *)
        IF (rVoted_PelletWaterTemp_Out >= 58.0) AND (tWaterBoxPrimeTimer >= 15.0) THEN
            bWaterBox_Clamp_Out := TRUE;
        END_IF;

        (* Step 10.4: Switch 3-way diverter valve to direct water flow across die face *)
        IF bWaterBox_Clamp_Out AND (tWaterBoxPrimeTimer >= 25.0) THEN
            bWaterBox_Diverter_Out := TRUE; (* True = Process Flow, False = Bypass *)
            uiCurrentState := STATE_CONTINUOUS_COMPOUND;
            tStateDwellTimer := 0.0;
            uiCurrentSubState := 1;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STATE 11: CONTINUOUS HIGH-RATE STEADY-STATE COMPOUNDING
     * Full industrial production rate (2,200 kg/h). Active MPC closed-loop suction pressure & screw torque optimization.
     * ----------------------------------------------------------------------------------------------------------------- *)
    STATE_CONTINUOUS_COMPOUND:
        uiCurrentSubState := 11;
        (* Gradually ramp master feed scalar from 0.30 to 1.00 (full recipe throughput) *)
        IF rFeedRampScalar < 1.00 THEN
            rFeedRampScalar := rFeedRampScalar + (0.70 / 180.0) * T_SAMPLE;
        ELSE
            rFeedRampScalar := 1.00;
        END_IF;

        (* Update All Gravimetric Feeder Master Setpoints *)
        rFeeder_CmdFlow_01_Out := rFeeder_SP_Flow_01_In * rFeedRampScalar;
        rFeeder_CmdFlow_02_Out := rFeeder_SP_Flow_02_In * rFeedRampScalar;
        rFeeder_CmdFlow_03_Out := rFeeder_SP_Flow_03_In * rFeedRampScalar;
        rFeeder_CmdFlow_04_Out := rFeeder_SP_Flow_04_In * rFeedRampScalar;
        rFeeder_CmdFlow_05_Out := rFeeder_SP_Flow_05_In * rFeedRampScalar;
        rSideFeederSpeed_Cmd_Out := (rFeeder_CmdFlow_05_Out / 900.0) * 480.0;

        (* Cutter speed proportional to total throughput (maintains uniform 2.5 mm pellet geometry) *)
        rPelletCutterSpeed_Cmd_Out := 1800.0 + ((rOnline_TotalThroughput / 2500.0) * 2200.0);
        IF rPelletCutterSpeed_Cmd_Out > 4200.0 THEN
            rPelletCutterSpeed_Cmd_Out := 4200.0;
        END_IF;

        (* Continuous Water Temperature Closed-Loop Regulation *)
        IF rVoted_PelletWaterTemp_Out < 65.0 THEN
            rWaterTrimHeat_Cmd_Out := (65.0 - rVoted_PelletWaterTemp_Out) * 8.0;
            IF rWaterTrimHeat_Cmd_Out > 100.0 THEN
                rWaterTrimHeat_Cmd_Out := 100.0;
            END_IF;
        ELSE
            rWaterTrimHeat_Cmd_Out := 0.0;
        END_IF;

        (* Check operator transition requests *)
        IF bPurgeMode_Cmd_In THEN
            uiCurrentState := STATE_DIE_FLUSH_PURGE;
            tStateDwellTimer := 0.0;
            uiCurrentSubState := 1;
        ELSIF bControlledStop_Cmd_In THEN
            uiCurrentState := STATE_BARREL_COOLING_RAMP;
            tStateDwellTimer := 0.0;
            uiCurrentSubState := 1;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STATE 12: DIE FLUSH & HIGH-MFR PURGE COMPOUND TRANSITION
     * Material changeover sequence: cuts additives/glass fibers, flushes die head with high-MFR purging resin.
     * ----------------------------------------------------------------------------------------------------------------- *)
    STATE_DIE_FLUSH_PURGE:
        uiCurrentSubState := 12;
        bPurgeSequenceActive := TRUE;

        (* Immediately halt glass fiber side feeder and additives *)
        rFeeder_CmdFlow_02_Out := 0.0;
        rFeeder_CmdFlow_03_Out := 0.0;
        rFeeder_CmdFlow_04_Out := 0.0;
        rFeeder_CmdFlow_05_Out := 0.0;
        rSideFeederSpeed_Cmd_Out := 0.0;

        (* Switch water box diverter valve to bypass to prevent cutter chamber contamination during purge *)
        bWaterBox_Diverter_Out := FALSE;

        (* Run Feeder 1 with purge compound at 250 kg/h and screw speed at 120 rpm *)
        rFeeder_CmdFlow_01_Out := 250.0;
        rScrewSpeedTarget := 120.0;

        (* Purge flush cycle runs for 300 seconds *)
        IF tStateDwellTimer >= 300.0 THEN
            bPurgeSequenceActive := FALSE;
            uiCurrentState := STATE_BARREL_COOLING_RAMP;
            tStateDwellTimer := 0.0;
            uiCurrentSubState := 1;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STATE 13: ORDERLY CONTROLLED BARREL GRADIENT COOLING
     * Orderly plant ramp-down: stops drives, closes water box, and manages cooling gradients to prevent shrink lockup.
     * ----------------------------------------------------------------------------------------------------------------- *)
    STATE_BARREL_COOLING_RAMP:
        uiCurrentSubState := 13;
        rScrewSpeedTarget := 0.0;
        rGearPumpSpeedTarget := 0.0;
        rSideFeederSpeed_Cmd_Out := 0.0;
        rPelletCutterSpeed_Cmd_Out := 0.0;
        rFeeder_CmdFlow_01_Out := 0.0;
        bVacuumPump_Run_Out := FALSE;
        rVacuumThrottle_Cmd_Out := 0.0;
        bWaterBox_Clamp_Out := FALSE;
        bWaterBox_Diverter_Out := FALSE;

        (* Set barrel temperature setpoints down towards safe standby/cooldown (140.0 °C) *)
        rCalc_TempA := 0.0;
        FOR idx_z := 2 TO 12 DO
            IF rZoneTemp_Act_Z01_In > 150.0 THEN
                rCalc_TempA := rCalc_TempA + 1.0;
            END_IF;
        END_FOR;

        (* Once cooled below 150.0 °C, return to Idle *)
        IF (rCalc_TempA = 0.0) AND (tStateDwellTimer >= 180.0) THEN
            uiCurrentState := STATE_IDLE_INTERLOCKS;
            tStateDwellTimer := 0.0;
            uiCurrentSubState := 0;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STATE 14: EMERGENCY MOTOR TORQUE / RUPTURE OVERPRESSURE PROTECTIVE TRIP
     * Zero-latency safety trip: halts all drives, triggers die fast dump valve, unclamps water box, latches safety trip.
     * ----------------------------------------------------------------------------------------------------------------- *)
    STATE_EMERGENCY_OVERLOAD:
        uiCurrentSubState := 14;
        bTripInterlocked_Out := TRUE;
        bExtruderReady_Out := FALSE;

        (* Immediate Hardware Actuator Safety Inhibits *)
        rScrewSpeed_Cmd_Out := 0.0;
        rGearPumpSpeed_Cmd_Out := 0.0;
        rSideFeederSpeed_Cmd_Out := 0.0;
        rPelletCutterSpeed_Cmd_Out := 0.0;
        rFeeder_CmdFlow_01_Out := 0.0;
        rFeeder_CmdFlow_02_Out := 0.0;
        rFeeder_CmdFlow_03_Out := 0.0;
        rFeeder_CmdFlow_04_Out := 0.0;
        rFeeder_CmdFlow_05_Out := 0.0;
        bVacuumPump_Run_Out := FALSE;
        rVacuumThrottle_Cmd_Out := 0.0;
        bWaterBox_Diverter_Out := FALSE;
        rWaterTrimHeat_Cmd_Out := 0.0;

        (* Fast Die Depressurization: Open hydraulic dump valve if die melt pressure exceeds 260 bar *)
        IF rVoted_DieMeltPres_Out >= 260.0 THEN
            bDieFastDump_Valve_Out := TRUE;
        END_IF;

        (* Operator Acknowledge and Safety Line Reset Sequence *)
        IF bAlarmReset_Cmd_In AND bSafetyLine_Healthy_In AND bRuptureDisc_Intact_In THEN
            IF (rVoted_ScrewTorque_Out < 1000.0) AND (rVoted_DieMeltPres_Out < 100.0) THEN
                bTripInterlocked_Out := FALSE;
                bDieFastDump_Valve_Out := FALSE;
                uiCurrentState := STATE_IDLE_INTERLOCKS;
                tStateDwellTimer := 0.0;
                uiCurrentSubState := 0;
            END_IF;
        END_IF;

    ELSE
        (* Unhandled State Trap - Fallback to Emergency Offline Safe State *)
        uiCurrentState := STATE_IDLE_INTERLOCKS;
        tStateDwellTimer := 0.0;
        uiCurrentSubState := 0;
END_CASE;

(* Export Active FSM Tracking Registers *)
uiExtruderFSM_State_Out := uiCurrentState;
uiExtruderFSM_SubState_Out := uiCurrentSubState;
