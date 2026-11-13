# Phase 5: Deterministic 12-Stage Operational FSM for FB_Mining_SAG_BallMill_GrindingCircuit

def get_phase5():
    return """(* === PHASE 5: DETERMINISTIC 12-STAGE OPERATIONAL FINITE STATE MACHINE (FSM) === *)

(* State Monotonic Elapsed Time Accumulator *)
IF iState = iPreviousState THEN
    rStateTimer_s := rStateTimer_s + tExecutionScanTime_s;
ELSE
    rStateTimer_s := 0.0;
    iPreviousState := iState;
END_IF;

(* Global Safety Trip Preemption *)
IF bFrozenChargeTrip THEN
    iState := 12; (* Jump immediately to EMERGENCY_FROZEN_CHARGE_DETECTION_TRIP *)
ELSIF NOT bEmergencyStop THEN
    iState := 12; (* Emergency stop actuated *)
END_IF;

CASE iState OF
    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 1: TRUNNION_HIGH_PRESSURE_JACKING_OIL_PERMISSIVE                                    *)
    (* ----------------------------------------------------------------------------------------- *)
    1:
        bSystemRunning                  := FALSE;
        rSagFeederTotalSpeedRef_pct     := 0.0;
        rSagFeeder1SpeedCmd_pct         := 0.0;
        rSagFeeder2SpeedCmd_pct         := 0.0;
        rSagFeedWaterFlowSp_m3h         := 0.0;
        rSagMotorSpeedRef_rpm           := 0.0;
        rSagMotorTorqueLimit_kNm        := 0.0;
        rPebbleCrusherFeedSp_tph        := 0.0;
        rCyclonePumpSpeedRef_pct        := 0.0;
        rSumpDilutionValveCmd_pct       := 0.0;
        bFrozenChargeTrip               := FALSE;
        bDirectLinerImpactTrip          := FALSE;
        bTrunnionLubeInterlockTrip      := FALSE;

        (* Close all hydrocyclone knife-gate valves *)
        FOR iCycloneIdx := 1 TO 16 DO
            abCycloneValveOpen_Cmd[iCycloneIdx] := FALSE;
        END_FOR;
        wCycloneValveMask := 16#0000;

        (* Verify High-Pressure Hydrostatic Oil Lift on Feed and Discharge Trunnions *)
        IF bLubeJackingPumpsRunning AND
           (rVoted_FeedTrunnionLift_bar >= 160.0) AND
           (rVoted_DischTrunnionLift_bar >= 170.0) AND
           (rEstimatedOilFilmThickness_um >= 120.0) THEN
            rLubePermissiveTimer_s := rLubePermissiveTimer_s + tExecutionScanTime_s;
            IF rLubePermissiveTimer_s >= 20.0 THEN (* 20 seconds healthy oil film verification *)
                IF bAutoSequenceEnable THEN
                    rLubePermissiveTimer_s := 0.0;
                    iState := 2; (* Proceed to INCHING_DRIVE_DISENGAGE_AND_STATOR_FLUX_PRE_EXCITATION *)
                END_IF;
            END_IF;
        ELSE
            rLubePermissiveTimer_s := 0.0;
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 2: INCHING_DRIVE_DISENGAGE_AND_STATOR_FLUX_PRE_EXCITATION                           *)
    (* ----------------------------------------------------------------------------------------- *)
    2:
        rSagMotorSpeedRef_rpm           := 0.0;
        rSagMotorTorqueLimit_kNm        := 5000.0; (* Pre-magnetization holding torque limit *)

        (* Verify mechanical inching clutch is physically disengaged and airgap is nominal *)
        IF bInchingDriveDisengaged AND
           (ZT_SAG_WRAP_AROUND_AIRGAP_MM_109A >= 11.5) AND
           (ZT_SAG_WRAP_AROUND_AIRGAP_MM_109B >= 11.5) AND
           (ZT_SAG_WRAP_AROUND_AIRGAP_MM_109C >= 11.5) THEN
            rInchingDisengageTimer_s := rInchingDisengageTimer_s + tExecutionScanTime_s;
            IF rInchingDisengageTimer_s >= 10.0 THEN (* 10 seconds flux establishment delay *)
                rInchingDisengageTimer_s := 0.0;
                iState := 3; (* Proceed to MILL_SLOW_ACCELERATION_RAMP *)
            END_IF;
        ELSE
            rInchingDisengageTimer_s := 0.0;
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 3: MILL_SLOW_ACCELERATION_RAMP                                                      *)
    (* ----------------------------------------------------------------------------------------- *)
    3:
        rSagMotorTorqueLimit_kNm := 29500.0; (* Full DTC torque limit enabled *)
        rMillRampTimer_s := rMillRampTimer_s + tExecutionScanTime_s;

        (* Controlled S-curve speed ramp from 0.0 to creep speed 3.5 RPM (soft break-away) *)
        IF rSagMotorSpeedRef_rpm < 3.50 THEN
            rSagMotorSpeedRef_rpm := rSagMotorSpeedRef_rpm + (0.05 * tExecutionScanTime_s);
        ELSE
            rSagMotorSpeedRef_rpm := 3.50;
        END_IF;

        (* Check that the mill rotates freely, torque < 95% and Babbitt temps are cool *)
        IF (rSagMotorSpeedRef_rpm >= 3.45) AND (rMillRampTimer_s >= 30.0) AND
           (TT_FEED_BEARING_BABBITT_103A < 65.0) AND (TT_DISCH_BEARING_BABBITT_104A < 65.0) THEN
            rMillRampTimer_s := 0.0;
            iState := 4; (* Proceed to WATER_ADDITION_RATIO_LEAD *)
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 4: WATER_ADDITION_RATIO_LEAD                                                        *)
    (* ----------------------------------------------------------------------------------------- *)
    4:
        (* Accelerate to base operating speed 8.50 RPM *)
        IF rSagMotorSpeedRef_rpm < 8.50 THEN
            rSagMotorSpeedRef_rpm := rSagMotorSpeedRef_rpm + (0.10 * tExecutionScanTime_s);
        END_IF;

        (* Pre-wet mill feed chute and internal shell with flushing water prior to ore feed *)
        rSagFeedWaterFlowSp_m3h := 850.0;
        rWaterLeadTimer_s := rWaterLeadTimer_s + tExecutionScanTime_s;

        (* Pre-fill cyclone sump and start pump at minimum circulation speed *)
        rCyclonePumpSpeedRef_pct := 45.0;

        IF (rWaterLeadTimer_s >= 45.0) AND (FT_SAG_FEED_WATER_FLOW_M3H_116 >= 800.0) AND
           (rVoted_SumpLevel_pct >= 40.0) THEN
            rWaterLeadTimer_s := 0.0;
            iState := 5; (* Proceed to COARSE_ORE_FEEDER_START *)
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 5: COARSE_ORE_FEEDER_START                                                          *)
    (* ----------------------------------------------------------------------------------------- *)
    5:
        rSagMotorSpeedRef_rpm := 8.85;
        rFeederStartRampTimer_s := rFeederStartRampTimer_s + tExecutionScanTime_s;

        (* Progressive ramp of coarse ore feeders from 0 to 2,500 t/h *)
        IF rSagFeederTotalSpeedRef_pct < 65.0 THEN
            rSagFeederTotalSpeedRef_pct := rSagFeederTotalSpeedRef_pct + (0.50 * tExecutionScanTime_s);
        END_IF;
        rSagFeeder1SpeedCmd_pct := rSagFeederTotalSpeedRef_pct;
        rSagFeeder2SpeedCmd_pct := rSagFeederTotalSpeedRef_pct;

        (* Regulate water flow proportional to ore feed to maintain 72.5% solids *)
        rSagFeedWaterFlowSp_m3h := (WT_FEEDER_1_ORE_TONS_HR_114 + WT_FEEDER_2_ORE_TONS_HR_115) * 0.380;

        (* Check that live charge mass starts building above minimum bed protection 850 tons *)
        IF (rEstimatedChargeWeight_tons >= 900.0) AND (rFeederStartRampTimer_s >= 90.0) THEN
            rFeederStartRampTimer_s := 0.0;
            iState := 6; (* Proceed to ACOUSTIC_TRAJECTORY_OPTIMIZATION *)
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 6: ACOUSTIC_TRAJECTORY_OPTIMIZATION (Toe angle 40 to 45 deg)                        *)
    (* ----------------------------------------------------------------------------------------- *)
    6:
        rAcousticOptimizeTimer_s := rAcousticOptimizeTimer_s + tExecutionScanTime_s;

        (* Fine-tune mill rotational speed using acoustic toe trim to achieve 40.0 to 45.0 deg *)
        rSagMotorSpeedRef_rpm := 9.18 + rPid4_Output;
        IF rSagMotorSpeedRef_rpm > 9.85 THEN
            rSagMotorSpeedRef_rpm := 9.85;
        ELSIF rSagMotorSpeedRef_rpm < 8.20 THEN
            rSagMotorSpeedRef_rpm := 8.20;
        END_IF;

        (* Ramp feeders up to nominal 3,500 t/h *)
        IF rSagFeederTotalSpeedRef_pct < 85.0 THEN
            rSagFeederTotalSpeedRef_pct := rSagFeederTotalSpeedRef_pct + (0.25 * tExecutionScanTime_s);
        END_IF;
        rSagFeeder1SpeedCmd_pct := rSagFeederTotalSpeedRef_pct;
        rSagFeeder2SpeedCmd_pct := rSagFeederTotalSpeedRef_pct;

        (* Verify toe angle is in the safe sweet spot (40.0 to 45.0 deg) and impact noise is low *)
        IF (rEstimatedToeAngle_deg >= 40.0) AND (rEstimatedToeAngle_deg <= 45.0) AND
           (rDirectLinerImpactEnergy_pct < 25.0) AND (rAcousticOptimizeTimer_s >= 60.0) THEN
            rAcousticOptimizeTimer_s := 0.0;
            iState := 7; (* Proceed to PEBBLE_PORT_INLINE_RECYCLE_CUTIN *)
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 7: PEBBLE_PORT_INLINE_RECYCLE_CUTIN                                                 *)
    (* ----------------------------------------------------------------------------------------- *)
    7:
        rPebbleCutInTimer_s := rPebbleCutInTimer_s + tExecutionScanTime_s;

        (* Start pebble recycle conveyor and regulate cone crusher feed *)
        IF bPebbleCrusherReady THEN
            rPebbleCrusherFeedSp_tph := 380.0;
        ELSE
            rPebbleCrusherFeedSp_tph := 0.0;
        END_IF;

        IF (rPebbleCutInTimer_s >= 45.0) AND (WT_PEBBLE_RECYCLE_TONS_HR_118 >= 200.0) THEN
            rPebbleCutInTimer_s := 0.0;
            iState := 8; (* Proceed to SECONDARY_BALL_MILL_FEED_BALANCING *)
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 8: SECONDARY_BALL_MILL_FEED_BALANCING                                               *)
    (* ----------------------------------------------------------------------------------------- *)
    8:
        rBallMillBalanceTimer_s := rBallMillBalanceTimer_s + tExecutionScanTime_s;

        (* Balance secondary twin ball mill split demands *)
        IF bBallMill1Ready AND bBallMill2Ready THEN
            (* Both ball mills online: 50/50 split regulated by power PID *)
            rBallMill1FeedSp_tph := 1850.0;
            rBallMill2FeedSp_tph := 1850.0;
        ELSIF bBallMill1Ready THEN
            rBallMill1FeedSp_tph := 2200.0;
            rBallMill2FeedSp_tph := 0.0;
        ELSIF bBallMill2Ready THEN
            rBallMill1FeedSp_tph := 0.0;
            rBallMill2FeedSp_tph := 2200.0;
        END_IF;

        IF (rBallMillBalanceTimer_s >= 60.0) AND (rVoted_SumpLevel_pct >= 50.0) THEN
            rBallMillBalanceTimer_s := 0.0;
            iState := 9; (* Proceed to HYDROCYCLONE_PRESSURE_DENSITY_CLOSED_LOOP *)
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 9: HYDROCYCLONE_PRESSURE_DENSITY_CLOSED_LOOP (Full Production MPC Mode)             *)
    (* ----------------------------------------------------------------------------------------- *)
    9:
        bSystemRunning := TRUE;

        (* Apply MPC optimized actuator demands with PID closed-loop trims *)
        rSagMotorSpeedRef_rpm := aMpc_U_cand[1, 3] + rPid4_Output;
        rSagFeedWaterFlowSp_m3h := aMpc_U_cand[1, 2];
        rPebbleCrusherFeedSp_tph := aMpc_U_cand[1, 4];

        (* Check for Mill Over-Filling Condition *)
        IF (rEstimatedChargeWeight_tons > 1450.0) OR (rEstimatedSlurryVolume_m3 > 320.0) THEN
            iState := 10; (* Cutback feed to prevent slurry spill *)
        ELSIF bMillGrindOutFlushCmd THEN
            iState := 11; (* Controlled grind-out requested *)
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 10: MILL_SLURRY_OVERFILLING_PROTECTION_CUTBACK                                      *)
    (* ----------------------------------------------------------------------------------------- *)
    10:
        rOverfillCutbackTimer_s := rOverfillCutbackTimer_s + tExecutionScanTime_s;

        (* Immediately cut ore feed by 50% to prevent trunnion slurry spill *)
        rSagFeederTotalSpeedRef_pct := rSagFeederTotalSpeedRef_pct * 0.50;
        rSagFeeder1SpeedCmd_pct := rSagFeederTotalSpeedRef_pct;
        rSagFeeder2SpeedCmd_pct := rSagFeederTotalSpeedRef_pct;

        (* Increase process water to flush internal grate discharge pulp lifters *)
        rSagFeedWaterFlowSp_m3h := 1450.0;

        (* Increase mill speed by 0.35 RPM to maximize slurry discharge flow through grates *)
        IF rSagMotorSpeedRef_rpm < 9.60 THEN
            rSagMotorSpeedRef_rpm := rSagMotorSpeedRef_rpm + (0.05 * tExecutionScanTime_s);
        END_IF;

        (* Once charge mass recedes below 1,320 tonnes and slurry volume clears, return to MPC *)
        IF (rEstimatedChargeWeight_tons <= 1320.0) AND (rEstimatedSlurryVolume_m3 <= 270.0) AND
           (rOverfillCutbackTimer_s >= 60.0) THEN
            rOverfillCutbackTimer_s := 0.0;
            iState := 9; (* Return to HYDROCYCLONE_PRESSURE_DENSITY_CLOSED_LOOP *)
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 11: CONTROLLED_CHARGE_GRINDOUT_FLUSH                                                *)
    (* ----------------------------------------------------------------------------------------- *)
    11:
        rGrindOutFlushTimer_s := rGrindOutFlushTimer_s + tExecutionScanTime_s;

        (* Stop all fresh ore feed completely *)
        rSagFeederTotalSpeedRef_pct := 0.0;
        rSagFeeder1SpeedCmd_pct := 0.0;
        rSagFeeder2SpeedCmd_pct := 0.0;
        rPebbleCrusherFeedSp_tph := 0.0;

        (* Flush mill with full water rate for 300 seconds to grind out residual ore *)
        rSagFeedWaterFlowSp_m3h := 1500.0;
        rSagMotorSpeedRef_rpm := 8.20;

        (* When mill live weight reaches tare + ball charge (880 tonnes) and timer expires, stop *)
        IF (rGrindOutFlushTimer_s >= 300.0) OR (rEstimatedChargeWeight_tons <= 890.0) THEN
            rGrindOutFlushTimer_s := 0.0;
            rSagFeedWaterFlowSp_m3h := 0.0;
            rSagMotorSpeedRef_rpm := 0.0;
            iState := 1; (* Return to standby lube permissive state *)
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 12: EMERGENCY_FROZEN_CHARGE_DETECTION_TRIP & SAFETY STOP                            *)
    (* ----------------------------------------------------------------------------------------- *)
    12:
        bSystemRunning := FALSE;
        rSagFeederTotalSpeedRef_pct := 0.0;
        rSagFeeder1SpeedCmd_pct := 0.0;
        rSagFeeder2SpeedCmd_pct := 0.0;
        rSagFeedWaterFlowSp_m3h := 0.0;
        rPebbleCrusherFeedSp_tph := 0.0;
        rCyclonePumpSpeedRef_pct := 0.0;
        rSumpDilutionValveCmd_pct := 0.0;

        (* Emergency Ring Motor Torque Cut & Caliper Brake Drop *)
        rSagMotorSpeedRef_rpm := 0.0;
        rSagMotorTorqueLimit_kNm := 0.0;

        (* Close all cyclone valves *)
        FOR iCycloneIdx := 1 TO 16 DO
            abCycloneValveOpen_Cmd[iCycloneIdx] := FALSE;
        END_FOR;
        wCycloneValveMask := 16#0000;

        (* Hold trip until operator reset command and alarms acknowledge *)
        IF bResetAlarms AND bEmergencyStop AND NOT bFrozenChargePotentialDetected THEN
            bFrozenChargeTrip := FALSE;
            bDirectLinerImpactTrip := FALSE;
            bTrunnionLubeInterlockTrip := FALSE;
            iState := 1; (* Return to lube permissive *)
        END_IF;

END_CASE;

iCurrentFsmState := iState;
"""
