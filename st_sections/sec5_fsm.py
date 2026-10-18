# Section 5: Logic Part 3 - Alarms, Multi-Stage FSM, Actuator Slew Rate, and Telemetry
def get_sec5_fsm():
    return """(* === 9. COMPREHENSIVE SIL-3 SAFETY ALARM TREE & TRIP LATCHING === *)
(* 9.1 Evaluation of Critical Process Trips into dwAlarmWord1 *)
IF NOT bEStopTripped THEN
    dwAlarmWord1 := dwAlarmWord1 OR 16#00000001; (* Bit 0: Emergency Stop Tripped *)
END_IF;

IF rVibrationRadialDE_X_mms >= 18.0 OR rVibrationRadialDE_Y_mms >= 18.0 THEN
    dwAlarmWord1 := dwAlarmWord1 OR 16#00000040; (* Bit 6: DE Radial Vibration High-High Trip *)
ELSIF rVibrationRadialDE_X_mms >= 9.0 OR rVibrationRadialDE_Y_mms >= 9.0 THEN
    dwWarningWord1 := dwWarningWord1 OR 16#00000080; (* Bit 7: DE Radial Vibration Warning *)
END_IF;

IF rVibrationRadialNDE_X_mms >= 18.0 OR rVibrationRadialNDE_Y_mms >= 18.0 THEN
    dwAlarmWord1 := dwAlarmWord1 OR 16#00000080; (* Bit 7: NDE Radial Vibration High-High Trip *)
ELSIF rVibrationRadialNDE_X_mms >= 9.0 OR rVibrationRadialNDE_Y_mms >= 9.0 THEN
    dwWarningWord1 := dwWarningWord1 OR 16#00000100; (* Bit 8: NDE Radial Vibration Warning *)
END_IF;

IF ABS(rShaftAxialThrust_um) >= 120.0 THEN
    dwAlarmWord1 := dwAlarmWord1 OR 16#00000100; (* Bit 8: Axial Thrust High-High Trip *)
ELSIF ABS(rShaftAxialThrust_um) >= 75.0 THEN
    dwWarningWord1 := dwWarningWord1 OR 16#00000200; (* Bit 9: Axial Thrust Warning *)
END_IF;

IF rDischTemp_Voted_K >= 430.0 THEN
    dwAlarmWord1 := dwAlarmWord1 OR 16#00004000; (* Bit 14: Discharge Gas Temp High-High Trip *)
ELSIF rDischTemp_Voted_K >= 405.0 THEN
    dwWarningWord1 := dwWarningWord1 OR 16#00000040; (* Bit 6: Discharge Gas Temp Warning *)
END_IF;

IF rAcousticPulsationRMS_mbar >= 4500.0 THEN
    dwAlarmWord1 := dwAlarmWord1 OR 16#00002000; (* Bit 13: Pipeline Acoustic Pulsation High-High Trip *)
ELSIF rAcousticPulsationRMS_mbar >= 2200.0 THEN
    dwWarningWord1 := dwWarningWord1 OR 16#00000010; (* Bit 4: Acoustic Pulsation High Warning *)
END_IF;

(* 9.2 Evaluation of Operating Boundary Trips into dwAlarmWord2 *)
IF rDischPress_Voted_bar >= c_rMaxDischargePressure_bar THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#00000001; (* Bit 0: Discharge Pressure MAOP High-High *)
END_IF;

IF rSuctPress_Voted_bar <= c_rMinSuctionPressure_bar THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#00000002; (* Bit 1: Suction Pressure Low-Low *)
END_IF;

IF rDriverPower_kW >= 26500.0 THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#00000004; (* Bit 2: Drive Motor Overpower Trip *)
END_IF;

IF rGasPurityH2_pct <= 95.0 AND rGasPurityH2_pct > 0.0 THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#00000010; (* Bit 4: Gas Purity Contamination Trip *)
END_IF;

IF ABS(rGasMolecularWeight_gmol - c_rNominalMolecularWeight_H2) >= c_rMaxAllowableMW_Deviation THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#00000020; (* Bit 5: Gas Molecular Weight Shift Trip *)
END_IF;

IF bEmergencyDepressurizeReq THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#00000200; (* Bit 9: Pipeline ESD Depressurization Request *)
END_IF;

(* 9.3 Deep Surge Cycle Accumulator within 60s Sliding Window *)
IF (rDistanceToSCL_pct < -8.0) AND (rFlowDP_Voted_mbar < 10.0) AND NOT bSurgeCycleLatched THEN
    bSurgeCycleLatched := TRUE;
    uiSurgeCycleCount := uiSurgeCycleCount + 1;
    dwWarningWord1 := dwWarningWord1 OR 16#00000020; (* Bit 5: Single Surge Cycle Detected *)
ELSIF rDistanceToSCL_pct > 5.0 THEN
    bSurgeCycleLatched := FALSE;
END_IF;

tSurgeCycleTimer(IN := (uiSurgeCycleCount > 0), PT := T#60S);
IF tSurgeCycleTimer.Q THEN
    tSurgeCycleTimer(IN := FALSE);
    uiSurgeCycleCount := 0; (* Reset window counter if 60s expires without lock *)
END_IF;

IF uiSurgeCycleCount >= 3 THEN
    dwAlarmWord1 := dwAlarmWord1 OR 16#00000020; (* Bit 5: Deep Surge Cycle Lockout Trip *)
END_IF;

(* 9.4 Master Trip Determination *)
IF (dwAlarmWord1 <> 16#00000000) OR (dwAlarmWord2 <> 16#00000000) OR (dwAlarmWord3 <> 16#00000000) THEN
    bCompressorTrip := TRUE;
    bSystemReady := FALSE;
    iState := 99; (* Force transition to Emergency Shutdown *)
ELSE
    bCompressorTrip := FALSE;
END_IF;

(* Alarm Reset Logic *)
IF bResetAlarms AND NOT bCompressorTrip THEN
    dwAlarmWord1 := 16#00000000;
    dwAlarmWord2 := 16#00000000;
    dwAlarmWord3 := 16#00000000;
    uiSurgeCycleCount := 0;
END_IF;

(* System Ready Permissive Evaluation *)
IF (dwAlarmWord1 = 16#00000000) AND (dwAlarmWord2 = 16#00000000) AND (dwAlarmWord3 = 16#00000000) AND
   bEStopTripped AND (rSuctPress_Voted_bar >= 40.0) AND bSealVacuumHealthy THEN
    bSystemReady := TRUE;
ELSE
    bSystemReady := FALSE;
END_IF;

(* === 10. MULTI-STAGE OPERATIONAL FINITE STATE MACHINE (FSM) === *)
CASE iState OF
    0: (* FSM_IDLE_STANDBY: Plant Safe Depressurized Standby *)
        bAntiSurgeValveFullOpen  := TRUE;
        rAntiSurgeValveActual_pct:= 100.0;
        rSpeedRefActual_rpm      := 0.0;
        rBlowdownValveCmd_pct    := 0.0;
        bMPCActive               := FALSE;
        bAcousticDampingEngaged  := FALSE;
        rASV_PID_Integral        := 100.0;

        IF bEnableSystem AND bSystemReady AND bAutoModeRequest THEN
            iState := 10; (* Transition to Inert Purge *)
        END_IF;

    10: (* FSM_N2_INERT_PURGE: Nitrogen Displacement Purge *)
        bAntiSurgeValveFullOpen  := TRUE;
        rAntiSurgeValveActual_pct:= 100.0;
        rSpeedRefActual_rpm      := 0.0;

        tPurgeTimer(IN := TRUE, PT := T#30S);
        IF tPurgeTimer.Q THEN
            tPurgeTimer(IN := FALSE);
            iState := 20; (* Transition to H2 Pressurization & Vacuum Extraction *)
        END_IF;

    20: (* FSM_H2_PRESSURIZATION_AND_SEAL_VACUUM: Introduce H2, Engage Vacuum Loop *)
        bAntiSurgeValveFullOpen  := TRUE;
        rAntiSurgeValveActual_pct:= 100.0;
        rSpeedRefActual_rpm      := 0.0;

        (* Engage vacuum extraction control valve *)
        rVacValveActual_pct := rVacExtractionValveRaw_pct;

        IF bSealVacuumHealthy AND (rPrimarySealDP_bar >= c_rMinPrimarySealDP_bar) AND (rSuctPress_Voted_bar >= 45.0) THEN
            iState := 30; (* Transition to Magnetic Bearing Permissive *)
        END_IF;

    30: (* FSM_BEARING_LEVITATION_AND_LUBE_PERMISSIVE: Active Magnetic Bearing Verification *)
        bAntiSurgeValveFullOpen  := TRUE;
        rAntiSurgeValveActual_pct:= 100.0;
        rSpeedRefActual_rpm      := 0.0;

        IF ABS(rShaftAxialThrust_um) < 25.0 AND (rBearingMetalTempMax_K < 340.0) THEN
            iState := 40; (* Transition to Slow Roll Warmup *)
        END_IF;

    40: (* FSM_SLOW_ROLL_WARMUP: Rotor Unbowing at 1,200 rpm *)
        bAntiSurgeValveFullOpen  := TRUE;
        rAntiSurgeValveActual_pct:= 100.0;
        rSpeedRefActual_rpm      := 1200.0;

        tWarmupTimer(IN := TRUE, PT := T#45S);
        IF tWarmupTimer.Q AND (rVibrationRadialDE_X_mms < 4.0) THEN
            tWarmupTimer(IN := FALSE);
            iState := 50; (* Transition to Critical Speed Acceleration *)
        END_IF;

    50: (* FSM_ACCELERATION_THROUGH_CRITICALS: Rapid Ramp Through 3,500 - 8,200 rpm *)
        bAntiSurgeValveFullOpen  := TRUE;
        rAntiSurgeValveActual_pct:= 100.0;
        rSpeedRefActual_rpm      := 12500.0; (* Accelerate directly to minimum governor speed *)

        IF rShaftSpeed_Voted_rpm >= 12400.0 THEN
            iState := 60; (* Transition to Pipeline Packing & Recycle *)
        END_IF;

    60: (* FSM_PIPELINE_PACKING_AND_RECYCLE: Modulate ASV to Build Pressure *)
        rSpeedRefActual_rpm := 12500.0;
        (* Slowly close ASV from 100% towards 35% *)
        IF rAntiSurgeValveActual_pct > 35.0 THEN
            rAntiSurgeValveActual_pct := rAntiSurgeValveActual_pct - (1.5 * rDt);
        END_IF;

        IF (rDischPress_Voted_bar >= (rDischargeHeaderPress_bar - 2.0)) AND (rSurgeMargin_pct >= 18.0) THEN
            iState := 70; (* Transition to Online Closed-Loop MPC Mode *)
        END_IF;

    70: (* FSM_ONLINE_MPC_ANTISURGE_AND_ACOUSTIC_DAMPING: Full Pipeline Transmission *)
        bAntiSurgeValveFullOpen := FALSE;
        rSpeedRefActual_rpm := 18500.0; (* Nominal 100-bar pipeline cruise speed *)

        (* Anti-surge actuator command from MPC or Fallback PID *)
        IF bMPCActive THEN
            rAntiSurgeValveActual_pct := rAntiSurgeValveActual_pct + arrDeltaU_Opt[1];
        ELSE
            rAntiSurgeValveActual_pct := rASV_PID_Output;
        END_IF;

        (* Inject open-loop rate kick and acoustic pulsation micro-dither *)
        rAntiSurgeValveActual_pct := rAntiSurgeValveActual_pct + rValveKickBias_pct + rAcousticDitherModulation;

        (* Check for surge boundary violation *)
        IF rDistanceToSCL_pct < -4.0 THEN
            iState := 80; (* Transition to Fast Surge Decoupling Kick *)
        ELSIF NOT bEnableSystem THEN
            iState := 90; (* Normal Stop Requested *)
        END_IF;

    80: (* FSM_RAPID_SURGE_DECOUPLING_AND_KICK: Emergency Aerodynamic Recovery *)
        (* Force ASV opening at maximum rate *)
        rAntiSurgeValveActual_pct := rAntiSurgeValveActual_pct + (c_rASV_MaxOpenRate_pct_s * rDt);
        rSpeedRefActual_rpm := MAX(12500.0, rSpeedRefActual_rpm - (500.0 * rDt));

        IF rSurgeMargin_pct >= 20.0 THEN
            iState := 70; (* Recovered, return to online MPC *)
        END_IF;

    90: (* FSM_CONTROLLED_DECELERATION_COOLDOWN: Controlled Pipeline Unloading *)
        bAntiSurgeValveFullOpen := FALSE;
        (* Ramp open ASV to 100% *)
        IF rAntiSurgeValveActual_pct < 100.0 THEN
            rAntiSurgeValveActual_pct := rAntiSurgeValveActual_pct + (8.0 * rDt);
        END_IF;

        (* Decelerate speed *)
        IF rSpeedRefActual_rpm > 1200.0 THEN
            rSpeedRefActual_rpm := rSpeedRefActual_rpm - (150.0 * rDt);
        ELSE
            rSpeedRefActual_rpm := 0.0;
            iState := 0; (* Returned to safe idle *)
        END_IF;

    99: (* FSM_EMERGENCY_SHUTDOWN_TRIP_DEPRESSURIZE: SIL-3 Trip & Flare Isolation *)
        bAntiSurgeValveFullOpen   := TRUE;
        rAntiSurgeValveActual_pct := 100.0;
        rSpeedRefActual_rpm       := 0.0;
        bMPCActive                := FALSE;
        bAcousticDampingEngaged   := FALSE;

        IF bEmergencyDepressurizeReq THEN
            rBlowdownValveCmd_pct := 100.0; (* Dump high-pressure H2 to flare header *)
        ELSE
            rBlowdownValveCmd_pct := 0.0;
        END_IF;

        tDepressurizeTimer(IN := TRUE, PT := T#60S);
        IF tDepressurizeTimer.Q AND bResetAlarms AND NOT bCompressorTrip AND bEStopTripped THEN
            tDepressurizeTimer(IN := FALSE);
            iState := 0; (* Reset to Idle after depressurization cooldown *)
        END_IF;

END_CASE;

(* === 11. ACTUATOR COMMAND CONDITIONING & ASYMMETRIC RATE LIMITING === *)
(* Clamp Anti-Surge Valve position between 0.0% and 100.0% *)
rAntiSurgeValveActual_pct := MAX(0.0, MIN(100.0, rAntiSurgeValveActual_pct));
rAntiSurgeValveCmd_pct    := rAntiSurgeValveActual_pct;

(* Clamp Speed Reference between 0 and 24,000 rpm *)
rSpeedRefActual_rpm       := MAX(0.0, MIN(24000.0, rSpeedRefActual_rpm));
rSpeedReference_rpm       := rSpeedRefActual_rpm;

(* Clamp Vacuum Extraction Valve Command *)
rVacuumExtractionValveCmd_pct := MAX(0.0, MIN(100.0, rVacExtractionValveRaw_pct));

(* === 12. TELEMETRY, ANALYTICS & DIAGNOSTIC UPDATES === *)
(* Update Sequence Status *)
wCompressorState := INT_TO_WORD(iState);

(* Real-Time Polytropic Efficiency Evaluation *)
IF rSuctTemp_Voted_K > 10.0 AND rDischTemp_Voted_K > rSuctTemp_Voted_K AND rCompressionRatio > 1.05 THEN
    rPolytropicEfficiency_pct := (((rGamma - 1.0) / rGamma) * LN(rCompressionRatio)) /
                                 LN(rDischTemp_Voted_K / rSuctTemp_Voted_K) * 100.0;
    rPolytropicEfficiency_pct := MAX(40.0, MIN(92.0, rPolytropicEfficiency_pct));
ELSE
    rPolytropicEfficiency_pct := 82.5;
END_IF;

(* Store previous cycle variables for next scan derivative evaluation *)
rPrevSurgeMargin_pct := rSurgeMargin_pct;
rPrevShaftSpeed_rpm  := rShaftSpeed_Voted_rpm;
rPrevSuctPress_bar   := rSuctPress_Voted_bar;
rPrevDischPress_bar  := rDischPress_Voted_bar;
rPrevFlowDP_mbar     := rFlowDP_Voted_mbar;
rPrevASVPosition_pct := rAntiSurgeValveActual_pct;

END_FUNCTION_BLOCK
"""
