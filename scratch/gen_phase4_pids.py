# Phase 4: Cascade PID Regulators & Cyclone Cluster Valve Sequencing for FB_Mining_SAG_BallMill_GrindingCircuit

def get_phase4():
    return """(* === PHASE 4: CASCADE PID REGULATORS & 16-CYCLONE KNIFE-GATE SEQUENCING === *)

(* 4.1 PID 1: Cyclone Feed Sump Level to Slurry Pump Speed PID *)
rPid1_Error := rVoted_SumpLevel_pct - 62.0; (* Setpoint = 62.0% *)
rPid1_Derivative := (rPid1_Error - rPid1_PrevError) / tExecutionScanTime_s;
rPid1_Integral := rPid1_Integral + (rPid1_Error * tExecutionScanTime_s / rPid1_Ti);

(* Anti-windup clamping on integral term *)
IF rPid1_Integral > 90.0 THEN
    rPid1_Integral := 90.0;
ELSIF rPid1_Integral < 35.0 THEN
    rPid1_Integral := 35.0;
END_IF;

rPid1_Output := (rPid1_Kp * rPid1_Error) + rPid1_Integral + (rPid1_Td * rPid1_Derivative);
IF rPid1_Output > 95.0 THEN
    rPid1_Output := 95.0;
ELSIF rPid1_Output < 40.0 THEN
    rPid1_Output := 40.0;
END_IF;
rPid1_PrevError := rPid1_Error;
rCyclonePumpSpeedRef_pct := rPid1_Output;

(* 4.2 PID 2: Cyclone Feed Slurry Density to Sump Dilution Water Valve PID *)
rPid2_Error := rVoted_CycloneFeedDensity_SG - 1.585; (* Target SG = 1.585 t/m3 *)
rPid2_Derivative := (rPid2_Error - rPid2_PrevError) / tExecutionScanTime_s;
rPid2_Integral := rPid2_Integral + (rPid2_Error * 50.0 * tExecutionScanTime_s / rPid2_Ti);

IF rPid2_Integral > 100.0 THEN
    rPid2_Integral := 100.0;
ELSIF rPid2_Integral < 0.0 THEN
    rPid2_Integral := 0.0;
END_IF;

rPid2_Output := (rPid2_Kp * rPid2_Error * 50.0) + rPid2_Integral + (rPid2_Td * rPid2_Derivative * 50.0);
IF rPid2_Output > 100.0 THEN
    rPid2_Output := 100.0;
ELSIF rPid2_Output < 0.0 THEN
    rPid2_Output := 0.0;
END_IF;
rPid2_PrevError := rPid2_Error;
rSumpDilutionValveCmd_pct := rPid2_Output;

(* 4.3 PID 3: In-Line Ultrasonic P80 to Cyclone Cluster Operating Pressure PID *)
rPid3_Error := rVoted_ProductP80_um - rTargetP80_microns; (* Target P80 = 75.0 um *)
rPid3_Derivative := (rPid3_Error - rPid3_PrevError) / tExecutionScanTime_s;
rPid3_Integral := rPid3_Integral + (rPid3_Error * tExecutionScanTime_s / rPid3_Ti);

IF rPid3_Integral > 140.0 THEN
    rPid3_Integral := 140.0;
ELSIF rPid3_Integral < 75.0 THEN
    rPid3_Integral := 75.0;
END_IF;

rPid3_Output := 105.0 + (rPid3_Kp * rPid3_Error) + rPid3_Integral + (rPid3_Td * rPid3_Derivative);
IF rPid3_Output > 145.0 THEN
    rPid3_Output := 145.0;
ELSIF rPid3_Output < 75.0 THEN
    rPid3_Output := 75.0;
END_IF;
rPid3_PrevError := rPid3_Error;

(* 4.4 PID 4: Shell Acoustic Toe Angle to SAG Mill Speed Trim PID *)
rPid4_Error := 42.5 - rEstimatedToeAngle_deg; (* Target Toe Angle = 42.5 deg *)
rPid4_Derivative := (rPid4_Error - rPid4_PrevError) / tExecutionScanTime_s;
rPid4_Integral := rPid4_Integral + (rPid4_Error * tExecutionScanTime_s / rPid4_Ti);

IF rPid4_Integral > 0.40 THEN
    rPid4_Integral := 0.40;
ELSIF rPid4_Integral < -0.40 THEN
    rPid4_Integral := -0.40;
END_IF;

rPid4_Output := (rPid4_Kp * rPid4_Error) + rPid4_Integral + (rPid4_Td * rPid4_Derivative);
IF rPid4_Output > 0.50 THEN
    rPid4_Output := 0.50;
ELSIF rPid4_Output < -0.50 THEN
    rPid4_Output := -0.50;
END_IF;
rPid4_PrevError := rPid4_Error;

(* 4.5 PID 5: SAG Mill Motor Power to Coarse Ore Feeder Demand Lead PID *)
rPid5_Error := 23.50 - rVoted_MotorPower_MW; (* Target Power = 23.5 MW *)
rPid5_Derivative := (rPid5_Error - rPid5_PrevError) / tExecutionScanTime_s;
rPid5_Integral := rPid5_Integral + (rPid5_Error * tExecutionScanTime_s / rPid5_Ti);

IF rPid5_Integral > 100.0 THEN
    rPid5_Integral := 100.0;
ELSIF rPid5_Integral < 30.0 THEN
    rPid5_Integral := 30.0;
END_IF;

rPid5_Output := (rPid5_Kp * rPid5_Error) + rPid5_Integral + (rPid5_Td * rPid5_Derivative);
IF rPid5_Output > 100.0 THEN
    rPid5_Output := 100.0;
ELSIF rPid5_Output < 30.0 THEN
    rPid5_Output := 30.0;
END_IF;
rPid5_PrevError := rPid5_Error;
rSagFeederTotalSpeedRef_pct := rPid5_Output;
rSagFeeder1SpeedCmd_pct := rSagFeederTotalSpeedRef_pct;
rSagFeeder2SpeedCmd_pct := rSagFeederTotalSpeedRef_pct;

(* 4.6 PID 6: Trunnion Live Charge Weight to Process Water Ratio Feed-Forward *)
IF rTargetSolidsFraction_pct > 50.0 AND rTargetSolidsFraction_pct < 85.0 THEN
    rSagFeedWaterFlowSp_m3h := (WT_FEEDER_1_ORE_TONS_HR_114 + WT_FEEDER_2_ORE_TONS_HR_115) *
                               ((100.0 - rTargetSolidsFraction_pct) / rTargetSolidsFraction_pct);
ELSE
    rSagFeedWaterFlowSp_m3h := 1150.0;
END_IF;

IF rSagFeedWaterFlowSp_m3h > 1800.0 THEN
    rSagFeedWaterFlowSp_m3h := 1800.0;
ELSIF rSagFeedWaterFlowSp_m3h < 400.0 THEN
    rSagFeedWaterFlowSp_m3h := 400.0;
END_IF;

(* 4.7 Secondary Twin Ball Mill #1 & #2 Feed Balancing *)
(* Balance slurry split to equalize motor power and trunnion lift *)
rPid7_Error := (JT_BALLMILL_2_POWER_MW_302 - JT_BALLMILL_1_POWER_MW_301) * 100.0;
rPid7_Integral := rPid7_Integral + (rPid7_Error * tExecutionScanTime_s / rPid7_Ti);

IF rPid7_Integral > 2200.0 THEN
    rPid7_Integral := 2200.0;
ELSIF rPid7_Integral < 1400.0 THEN
    rPid7_Integral := 1400.0;
END_IF;

rBallMill1FeedSp_tph := rPid7_Integral;
rBallMill2FeedSp_tph := 3700.00 - rBallMill1FeedSp_tph;

(* Ball mill water addition proportioned at 68% solids *)
rBallMill1WaterSp_m3h := rBallMill1FeedSp_tph * (0.32 / 0.68);
rBallMill2WaterSp_m3h := rBallMill2FeedSp_tph * (0.32 / 0.68);

(* 4.8 16-Hydrocyclone Cluster Knife-Gate Valve Sequencing & Wear-Leveling *)
rCycloneSwitchingDelayTimer_s := rCycloneSwitchingDelayTimer_s + tExecutionScanTime_s;

(* Compute recommended active cyclone count based on cluster manifold flow and pressure PID *)
IF FT_CYCLONE_FEED_SLURRY_FLOW_M3H_203A > 2000.0 THEN
    (* Target flow per cyclone ~ 380 m3/h for sharp 75 um cut *)
    iActiveCycloneValvesCount := REAL_TO_INT(FT_CYCLONE_FEED_SLURRY_FLOW_M3H_203A / 380.0);
    IF iActiveCycloneValvesCount > 16 THEN
        iActiveCycloneValvesCount := 16;
    ELSIF iActiveCycloneValvesCount < 6 THEN
        iActiveCycloneValvesCount := 6;
    END_IF;
ELSE
    iActiveCycloneValvesCount := 8;
END_IF;

(* Rotate valves every 120 seconds for equal wear leveling across 16 units *)
IF rCycloneSwitchingDelayTimer_s >= 120.0 THEN
    rCycloneSwitchingDelayTimer_s := 0.0;
    iCycloneRotationPointer := iCycloneRotationPointer + 1;
    IF iCycloneRotationPointer > 16 THEN
        iCycloneRotationPointer := 1;
    END_IF;
END_IF;

(* Generate 16-Bit Solenoid Word and Boolean Output Array *)
wCycloneValveMask := 16#0000;
FOR iCycloneIdx := 1 TO 16 DO
    (* Check if cyclone index falls within active window starting from rotation pointer *)
    IF iCycloneIdx <= iActiveCycloneValvesCount THEN
        abCycloneValveOpen_Cmd[iCycloneIdx] := TRUE;
        wCycloneValveMask := wCycloneValveMask OR SHL(WORD#16#0001, (iCycloneIdx - 1));
        arCycloneOperatingHours[iCycloneIdx] := arCycloneOperatingHours[iCycloneIdx] + (tExecutionScanTime_s / 3600.0);
    ELSE
        abCycloneValveOpen_Cmd[iCycloneIdx] := FALSE;
    END_IF;
END_FOR;
"""
