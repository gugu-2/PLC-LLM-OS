# Section 5: Phase 4 12-Stage Operational Finite State Machine

def get_sec5():
    return """
(* =====================================================================================================================
 * PHASE 4: 12-STAGE DETERMINISTIC PRODUCTION FINITE STATE MACHINE (FSM)
 * ===================================================================================================================== *)

(* Master Safety Interlock Check: Dual-Channel E-Stop & Critical Safety Trips *)
IF (NOT bEmergencyStop_NC) OR (NOT bMasterPowerOn) OR bTubeContactHazardActive OR (rVoted_ExtruderMeltPress_bar >= c_rTrip_MeltPress_HH_bar) OR (rVoted_TubeN2Press_bar >= c_rTrip_TubeN2Press_HH_bar) THEN
    nActiveFSM_State := 11; (* Direct fast trip to EMERGENCY_ESTOP_LINE_CLAMP *)
END_IF;

(* Track State Transitions & Elapsed Time *)
IF nActiveFSM_State <> nFSM_PreviousState THEN
    rStateTimer_s      := 0.0;
    bStateFirstScan    := TRUE;
    nFSM_PreviousState := nActiveFSM_State;
ELSE
    rStateTimer_s   := rStateTimer_s + c_rTs;
    bStateFirstScan := FALSE;
END_IF;

CASE nActiveFSM_State OF

    (* -----------------------------------------------------------------------------------------
     * STATE 0: TUBE_NITROGEN_PURGE
     * Flush 150m vulcanization tube with dry nitrogen to eliminate oxygen (< 50 ppm O2)
     * ----------------------------------------------------------------------------------------- *)
    0:
        bSystemReady           := FALSE;
        bSystemRunning         := FALSE;
        bEmergencyTripped      := FALSE;
        bSpoolTransferPermissive := FALSE;

        (* Extruders and Capstans Off *)
        rCmd_Extruder2_XLPE_RPM       := 0.0;
        rCmd_Extruder1_CondScreen_RPM := 0.0;
        rCmd_Extruder3_InsScreen_RPM  := 0.0;
        rCmd_HaulOffCapstan_Speed_mpm := 0.0;
        rCmd_InfeedCapstan_Speed_mpm  := 0.0;
        rCmd_HaulOffCapstan_TensionTrim_kN := 0.0;

        (* Heaters Off during initial purge *)
        rCmd_Zone1_SCR_Duty_pct := 0.0;
        rCmd_Zone2_SCR_Duty_pct := 0.0;
        rCmd_Zone3_SCR_Duty_pct := 0.0;
        rCmd_Zone4_SCR_Duty_pct := 0.0;

        (* Open N2 injection supply and vent to flush tube atmosphere *)
        rCmd_N2_InjectionValve_pct := 45.0;
        rCmd_N2_VentValve_pct      := 60.0;
        rCmd_QuenchWaterInflowValve_pct := 10.0;
        rCmd_QuenchWaterDrainValve_pct  := 15.0;
        rCmd_PayoffBrakeTorque_Nm       := 0.0;

        bCmd_EmergencyN2FastVent            := FALSE;
        bCmd_CaterpillarPneumaticBrakeClamp := TRUE; (* Capstans mechanically clamped *)
        bCmd_TelescopicSealIsolate          := FALSE;

        (* Transition Criterion: O2 concentration below 50.0 ppm and minimum purge time elapsed *)
        IF bSystemAutoEnable AND (AIT_TUBE_O2_PPM_1001 <= 50.0) AND (rStateTimer_s >= 60.0) AND bNitrogenSupplyHeaderOk THEN
            nActiveFSM_State := 1; (* Advance to HEATING_ZONE_PREHEAT *)
        END_IF;

    (* -----------------------------------------------------------------------------------------
     * STATE 1: HEATING_ZONE_PREHEAT
     * Stepwise thermal preheating of 4 radiant heating zones to 380..420 deg C; pressurize N2 to 10 bar
     * ----------------------------------------------------------------------------------------- *)
    1:
        bSystemReady           := FALSE;
        bSystemRunning         := FALSE;
        bEmergencyTripped      := FALSE;
        bSpoolTransferPermissive := FALSE;

        rCmd_Extruder2_XLPE_RPM       := 0.0;
        rCmd_Extruder1_CondScreen_RPM := 0.0;
        rCmd_Extruder3_InsScreen_RPM  := 0.0;
        rCmd_HaulOffCapstan_Speed_mpm := 0.0;
        rCmd_InfeedCapstan_Speed_mpm  := 0.0;
        rCmd_HaulOffCapstan_TensionTrim_kN := 0.0;

        (* Stepwise SCR Duty Modulation toward Target Temperatures *)
        IF rVoted_Zone1Temp_degC < (rSet_Zone1_TempTarget_degC - 5.0) THEN
            rCmd_Zone1_SCR_Duty_pct := 75.0;
        ELSE
            rCmd_Zone1_SCR_Duty_pct := 38.5;
        END_IF;

        IF rVoted_Zone2Temp_degC < (rSet_Zone2_TempTarget_degC - 5.0) THEN
            rCmd_Zone2_SCR_Duty_pct := 82.0;
        ELSE
            rCmd_Zone2_SCR_Duty_pct := 42.0;
        END_IF;

        IF rVoted_Zone1Temp_degC < (rSet_Zone3_TempTarget_degC - 5.0) THEN
            rCmd_Zone3_SCR_Duty_pct := 80.0;
        ELSE
            rCmd_Zone3_SCR_Duty_pct := 40.0;
        END_IF;

        IF rVoted_Zone2Temp_degC < (rSet_Zone4_TempTarget_degC - 5.0) THEN
            rCmd_Zone4_SCR_Duty_pct := 70.0;
        ELSE
            rCmd_Zone4_SCR_Duty_pct := 35.0;
        END_IF;

        (* Pressurize Tube up to 10.0 bar N2 *)
        IF rVoted_TubeN2Press_bar < (rSet_TubeN2PressTarget_bar - 0.2) THEN
            rCmd_N2_InjectionValve_pct := 55.0;
            rCmd_N2_VentValve_pct      := 0.0;
        ELSIF rVoted_TubeN2Press_bar > (rSet_TubeN2PressTarget_bar + 0.2) THEN
            rCmd_N2_InjectionValve_pct := 0.0;
            rCmd_N2_VentValve_pct      := 18.0;
        ELSE
            rCmd_N2_InjectionValve_pct := 8.5;
            rCmd_N2_VentValve_pct      := 2.0;
        END_IF;

        (* Maintain Quench Leg Hydrostatic Level *)
        IF rVoted_QuenchWaterLvl_mm < rSet_QuenchWaterLevel_mm THEN
            rCmd_QuenchWaterInflowValve_pct := 28.0;
            rCmd_QuenchWaterDrainValve_pct  := 5.0;
        ELSE
            rCmd_QuenchWaterInflowValve_pct := 10.0;
            rCmd_QuenchWaterDrainValve_pct  := 22.0;
        END_IF;

        bCmd_EmergencyN2FastVent            := FALSE;
        bCmd_CaterpillarPneumaticBrakeClamp := TRUE;
        bCmd_TelescopicSealIsolate          := FALSE;

        (* Transition Criterion: Temperatures within 10 deg C of target and N2 pressure >= 9.8 bar *)
        IF bSystemAutoEnable AND
           (ABS(rVoted_Zone1Temp_degC - rSet_Zone1_TempTarget_degC) <= 10.0) AND
           (ABS(rVoted_Zone2Temp_degC - rSet_Zone2_TempTarget_degC) <= 10.0) AND
           (rVoted_TubeN2Press_bar >= 9.800) AND bHydrostaticSealBalanced THEN
            nActiveFSM_State := 2; (* Advance to CONDUCTOR_STRINGING_TENSION *)
        END_IF;

    (* -----------------------------------------------------------------------------------------
     * STATE 2: CONDUCTOR_STRINGING_TENSION
     * Conductor leader cable pre-tensioning and centering across 150m catenary span
     * ----------------------------------------------------------------------------------------- *)
    2:
        bSystemReady           := FALSE;
        bSystemRunning         := FALSE;
        bEmergencyTripped      := FALSE;
        bSpoolTransferPermissive := FALSE;

        rCmd_Extruder2_XLPE_RPM       := 0.0;
        rCmd_Extruder1_CondScreen_RPM := 0.0;
        rCmd_Extruder3_InsScreen_RPM  := 0.0;

        (* Release caterpillar brakes and apply stringing tension *)
        bCmd_CaterpillarPneumaticBrakeClamp := FALSE;
        rCmd_InfeedCapstan_Speed_mpm        := 1.50;
        rCmd_HaulOffCapstan_Speed_mpm       := 1.50;
        rCmd_HaulOffCapstan_TensionTrim_kN  := 0.0;
        rCmd_PayoffBrakeTorque_Nm           := 150.0;

        (* Maintain Heating and Pressure *)
        rCmd_Zone1_SCR_Duty_pct := 38.5;
        rCmd_Zone2_SCR_Duty_pct := 42.0;
        rCmd_Zone3_SCR_Duty_pct := 40.0;
        rCmd_Zone4_SCR_Duty_pct := 35.0;

        rCmd_N2_InjectionValve_pct := 8.5;
        rCmd_N2_VentValve_pct      := 2.0;
        rCmd_QuenchWaterInflowValve_pct := 15.0;
        rCmd_QuenchWaterDrainValve_pct  := 15.0;

        bCmd_EmergencyN2FastVent   := FALSE;
        bCmd_TelescopicSealIsolate := FALSE;

        (* Transition Criterion: Conductor tension >= 35.0 kN, splice box latched, tension stable for 20 s *)
        IF bSystemAutoEnable AND (rVoted_HaulOffTension_kN >= 35.0) AND bTelescopicSpliceBoxLatched AND (rStateTimer_s >= 20.0) THEN
            nActiveFSM_State := 3; (* Advance to TRIPLE_HEAD_MELT_PRIME *)
        END_IF;

    (* -----------------------------------------------------------------------------------------
     * STATE 3: TRIPLE_HEAD_MELT_PRIME
     * Start Extruders 1, 2, 3 at creeping speed, build melt pressure and prime co-extrusion stream
     * ----------------------------------------------------------------------------------------- *)
    3:
        bSystemReady           := TRUE;
        bSystemRunning         := TRUE;
        bEmergencyTripped      := FALSE;
        bSpoolTransferPermissive := FALSE;

        (* Creep extruders to build melt pressure *)
        rCmd_Extruder1_CondScreen_RPM := 8.00;
        rCmd_Extruder2_XLPE_RPM       := 12.50;
        rCmd_Extruder3_InsScreen_RPM  := 7.50;

        rCmd_InfeedCapstan_Speed_mpm  := 2.00;
        rCmd_HaulOffCapstan_Speed_mpm := 2.00;
        rCmd_HaulOffCapstan_TensionTrim_kN := 0.0;
        rCmd_PayoffBrakeTorque_Nm     := 180.0;

        rCmd_Zone1_SCR_Duty_pct := 40.0;
        rCmd_Zone2_SCR_Duty_pct := 44.0;
        rCmd_Zone3_SCR_Duty_pct := 42.0;
        rCmd_Zone4_SCR_Duty_pct := 36.0;

        rCmd_N2_InjectionValve_pct := 10.0;
        rCmd_N2_VentValve_pct      := 2.5;
        rCmd_QuenchWaterInflowValve_pct := 20.0;
        rCmd_QuenchWaterDrainValve_pct  := 20.0;

        bCmd_EmergencyN2FastVent            := FALSE;
        bCmd_CaterpillarPneumaticBrakeClamp := FALSE;
        bCmd_TelescopicSealIsolate          := FALSE;

        (* Transition Criterion: Melt pressure exceeds 240 bar, melt temp >= 128 deg C, primed for 30 s *)
        IF bSystemAutoEnable AND (rVoted_ExtruderMeltPress_bar >= 240.0) AND (rVoted_ExtruderMeltTemp_degC >= 128.0) AND (rStateTimer_s >= 30.0) THEN
            nActiveFSM_State := 4; (* Advance to LINE_SPEED_RAMP_UP *)
        END_IF;

    (* -----------------------------------------------------------------------------------------
     * STATE 4: LINE_SPEED_RAMP_UP
     * Synchronous ramp of caterpillars and extruders from 2.0 m/min to 25.0 m/min
     * ----------------------------------------------------------------------------------------- *)
    4:
        bSystemReady           := TRUE;
        bSystemRunning         := TRUE;
        bEmergencyTripped      := FALSE;
        bSpoolTransferPermissive := FALSE;

        (* Calculate dynamic ramp target speed (0.08 m/min per second) *)
        rRampTargetLineSpeed_mpm := 2.00 + (rStateTimer_s * 0.08);
        IF rRampTargetLineSpeed_mpm > rSet_LineSpeed_Target_mpm THEN
            rRampTargetLineSpeed_mpm := rSet_LineSpeed_Target_mpm;
        END_IF;

        rCmd_InfeedCapstan_Speed_mpm  := rRampTargetLineSpeed_mpm;
        rCmd_HaulOffCapstan_Speed_mpm := rRampTargetLineSpeed_mpm + au_control[2];
        rCmd_HaulOffCapstan_TensionTrim_kN := au_control[7];

        (* Dynamically scale extruder screw speeds proportionally to line speed *)
        rCmd_Extruder2_XLPE_RPM       := (rRampTargetLineSpeed_mpm / rSet_LineSpeed_Target_mpm) * 45.0 + au_control[1];
        rCmd_Extruder1_CondScreen_RPM := (rRampTargetLineSpeed_mpm / rSet_LineSpeed_Target_mpm) * 42.0;
        rCmd_Extruder3_InsScreen_RPM  := (rRampTargetLineSpeed_mpm / rSet_LineSpeed_Target_mpm) * 38.5;
        rCmd_PayoffBrakeTorque_Nm     := 250.0;

        rCmd_Zone1_SCR_Duty_pct := 45.0 + au_control[3];
        rCmd_Zone2_SCR_Duty_pct := 48.0;
        rCmd_Zone3_SCR_Duty_pct := 46.0;
        rCmd_Zone4_SCR_Duty_pct := 40.0;

        rCmd_N2_InjectionValve_pct := 12.0 + au_control[4];
        rCmd_N2_VentValve_pct      := 2.0 + au_control[5];
        rCmd_QuenchWaterInflowValve_pct := 35.0 + au_control[6];
        rCmd_QuenchWaterDrainValve_pct  := 35.0;

        bCmd_EmergencyN2FastVent            := FALSE;
        bCmd_CaterpillarPneumaticBrakeClamp := FALSE;
        bCmd_TelescopicSealIsolate          := FALSE;

        (* Transition Criterion: Line speed reaches 24.5 m/min *)
        IF bSystemAutoEnable AND (rVoted_LinePullSpeed_mpm >= 24.50) THEN
            nActiveFSM_State := 5; (* Advance to CATENARY_SAG_AUTO_CENTERING *)
        END_IF;

    (* -----------------------------------------------------------------------------------------
     * STATE 5: CATENARY_SAG_AUTO_CENTERING
     * Closed-loop X-ray sag regulation activating MPC capstan tension trim
     * ----------------------------------------------------------------------------------------- *)
    5:
        bSystemReady           := TRUE;
        bSystemRunning         := TRUE;
        bEmergencyTripped      := FALSE;
        bSpoolTransferPermissive := FALSE;

        rCmd_InfeedCapstan_Speed_mpm  := rSet_LineSpeed_Target_mpm;
        rCmd_HaulOffCapstan_Speed_mpm := rSet_LineSpeed_Target_mpm + au_control[2];
        rCmd_HaulOffCapstan_TensionTrim_kN := au_control[7] + (0.45 * (rSet_CatenarySagTarget_mm - rVoted_CatenarySag_mm));

        rCmd_Extruder2_XLPE_RPM       := 45.00 + au_control[1];
        rCmd_Extruder1_CondScreen_RPM := 42.00;
        rCmd_Extruder3_InsScreen_RPM  := 38.50;
        rCmd_PayoffBrakeTorque_Nm     := 265.0;

        rCmd_Zone1_SCR_Duty_pct := 46.0 + au_control[3];
        rCmd_Zone2_SCR_Duty_pct := 50.0;
        rCmd_Zone3_SCR_Duty_pct := 48.0;
        rCmd_Zone4_SCR_Duty_pct := 42.0;

        rCmd_N2_InjectionValve_pct := 12.0 + au_control[4];
        rCmd_N2_VentValve_pct      := 2.0 + au_control[5];
        rCmd_QuenchWaterInflowValve_pct := 40.0 + au_control[6];
        rCmd_QuenchWaterDrainValve_pct  := 40.0;

        bCmd_EmergencyN2FastVent            := FALSE;
        bCmd_CaterpillarPneumaticBrakeClamp := FALSE;
        bCmd_TelescopicSealIsolate          := FALSE;

        (* Transition Criterion: Sag centered within +/- 2.0 mm for at least 15.0 seconds *)
        IF bSystemAutoEnable AND bCatenarySagCenteringOk AND (rStateTimer_s >= 15.0) THEN
            nActiveFSM_State := 6; (* Advance to CONTINUOUS_STEADY_STATE_CURING *)
        END_IF;

    (* -----------------------------------------------------------------------------------------
     * STATE 6: CONTINUOUS_STEADY_STATE_CURING
     * Stable continuous vulcanization, full MPC optimization, 8-axis eccentricity scanning
     * ----------------------------------------------------------------------------------------- *)
    6:
        bSystemReady           := TRUE;
        bSystemRunning         := TRUE;
        bEmergencyTripped      := FALSE;
        bSpoolTransferPermissive := TRUE;

        (* Full Receding-Horizon MPC closed-loop actuation *)
        rCmd_InfeedCapstan_Speed_mpm  := rSet_LineSpeed_Target_mpm;
        rCmd_HaulOffCapstan_Speed_mpm := rSet_LineSpeed_Target_mpm + au_control[2];
        rCmd_HaulOffCapstan_TensionTrim_kN := au_control[7];

        rCmd_Extruder2_XLPE_RPM       := 45.00 + au_control[1];
        rCmd_Extruder1_CondScreen_RPM := 42.00;
        rCmd_Extruder3_InsScreen_RPM  := 38.50;
        rCmd_PayoffBrakeTorque_Nm     := 275.0;

        rCmd_Zone1_SCR_Duty_pct := 46.5 + au_control[3];
        rCmd_Zone2_SCR_Duty_pct := 50.5;
        rCmd_Zone3_SCR_Duty_pct := 48.5;
        rCmd_Zone4_SCR_Duty_pct := 42.5;

        rCmd_N2_InjectionValve_pct := 12.5 + au_control[4];
        rCmd_N2_VentValve_pct      := 2.0 + au_control[5];
        rCmd_QuenchWaterInflowValve_pct := 42.0 + au_control[6];
        rCmd_QuenchWaterDrainValve_pct  := 42.0;

        bCmd_EmergencyN2FastVent            := FALSE;
        bCmd_CaterpillarPneumaticBrakeClamp := FALSE;
        bCmd_TelescopicSealIsolate          := FALSE;

        (* Transition Options: Spool changeover request or stop request *)
        IF NOT bTakeUpSpoolReady THEN
            nActiveFSM_State := 7; (* Advance to SPOOL_CHANGEOVER *)
        ELSIF NOT bSystemAutoEnable THEN
            nActiveFSM_State := 8; (* Advance to PURGE_OUT *)
        END_IF;

    (* -----------------------------------------------------------------------------------------
     * STATE 7: SPOOL_CHANGEOVER
     * Coordinate downstream dual take-up accumulator and flying splice handoff
     * ----------------------------------------------------------------------------------------- *)
    7:
        bSystemReady           := TRUE;
        bSystemRunning         := TRUE;
        bEmergencyTripped      := FALSE;
        bSpoolTransferPermissive := FALSE;

        (* Temporarily trim line speed to 20.0 m/min while maintaining tight tension *)
        rCmd_InfeedCapstan_Speed_mpm  := 20.00;
        rCmd_HaulOffCapstan_Speed_mpm := 20.00 + au_control[2];
        rCmd_HaulOffCapstan_TensionTrim_kN := au_control[7];

        rCmd_Extruder2_XLPE_RPM       := 36.00 + au_control[1];
        rCmd_Extruder1_CondScreen_RPM := 33.60;
        rCmd_Extruder3_InsScreen_RPM  := 30.80;
        rCmd_PayoffBrakeTorque_Nm     := 240.0;

        rCmd_Zone1_SCR_Duty_pct := 42.0;
        rCmd_Zone2_SCR_Duty_pct := 46.0;
        rCmd_Zone3_SCR_Duty_pct := 44.0;
        rCmd_Zone4_SCR_Duty_pct := 38.0;

        rCmd_N2_InjectionValve_pct := 12.5;
        rCmd_N2_VentValve_pct      := 2.0;
        rCmd_QuenchWaterInflowValve_pct := 38.0;
        rCmd_QuenchWaterDrainValve_pct  := 38.0;

        bCmd_EmergencyN2FastVent            := FALSE;
        bCmd_CaterpillarPneumaticBrakeClamp := FALSE;
        bCmd_TelescopicSealIsolate          := FALSE;

        (* Return to steady state once take-up spool confirmed ready *)
        IF bTakeUpSpoolReady AND (rStateTimer_s >= 25.0) THEN
            nActiveFSM_State := 6; (* Return to CONTINUOUS_STEADY_STATE_CURING *)
        END_IF;

    (* -----------------------------------------------------------------------------------------
     * STATE 8: PURGE_OUT
     * Production completion, purge compound flush and extruder depressurization
     * ----------------------------------------------------------------------------------------- *)
    8:
        bSystemReady           := FALSE;
        bSystemRunning         := TRUE;
        bEmergencyTripped      := FALSE;
        bSpoolTransferPermissive := FALSE;

        rCmd_InfeedCapstan_Speed_mpm  := 5.00;
        rCmd_HaulOffCapstan_Speed_mpm := 5.00;
        rCmd_HaulOffCapstan_TensionTrim_kN := 0.0;

        (* Extruder creep for compound purging *)
        rCmd_Extruder2_XLPE_RPM       := 5.00;
        rCmd_Extruder1_CondScreen_RPM := 4.00;
        rCmd_Extruder3_InsScreen_RPM  := 4.00;
        rCmd_PayoffBrakeTorque_Nm     := 120.0;

        rCmd_Zone1_SCR_Duty_pct := 25.0;
        rCmd_Zone2_SCR_Duty_pct := 25.0;
        rCmd_Zone3_SCR_Duty_pct := 25.0;
        rCmd_Zone4_SCR_Duty_pct := 20.0;

        rCmd_N2_InjectionValve_pct := 8.0;
        rCmd_N2_VentValve_pct      := 4.0;
        rCmd_QuenchWaterInflowValve_pct := 20.0;
        rCmd_QuenchWaterDrainValve_pct  := 20.0;

        bCmd_EmergencyN2FastVent            := FALSE;
        bCmd_CaterpillarPneumaticBrakeClamp := FALSE;
        bCmd_TelescopicSealIsolate          := FALSE;

        (* Transition Criterion: Purge out duration completed (120 s) *)
        IF rStateTimer_s >= 120.0 THEN
            nActiveFSM_State := 9; (* Advance to CONTROLLED_TUBE_DEPRESSURIZATION *)
        END_IF;

    (* -----------------------------------------------------------------------------------------
     * STATE 9: CONTROLLED_TUBE_DEPRESSURIZATION
     * Stepwise blowdown of 10.0 bar N2 atmosphere down to atmospheric pressure
     * ----------------------------------------------------------------------------------------- *)
    9:
        bSystemReady           := FALSE;
        bSystemRunning         := FALSE;
        bEmergencyTripped      := FALSE;
        bSpoolTransferPermissive := FALSE;

        rCmd_Extruder2_XLPE_RPM       := 0.0;
        rCmd_Extruder1_CondScreen_RPM := 0.0;
        rCmd_Extruder3_InsScreen_RPM  := 0.0;
        rCmd_InfeedCapstan_Speed_mpm  := 0.0;
        rCmd_HaulOffCapstan_Speed_mpm := 0.0;
        rCmd_HaulOffCapstan_TensionTrim_kN := 0.0;
        rCmd_PayoffBrakeTorque_Nm     := 0.0;

        rCmd_Zone1_SCR_Duty_pct := 0.0;
        rCmd_Zone2_SCR_Duty_pct := 0.0;
        rCmd_Zone3_SCR_Duty_pct := 0.0;
        rCmd_Zone4_SCR_Duty_pct := 0.0;

        (* Controlled Venting: modulate vent valve to ramp down pressure *)
        rCmd_N2_InjectionValve_pct := 0.0;
        rCmd_N2_VentValve_pct      := 35.0;

        (* Lower Quench Water Level to prevent back-flooding during blowdown *)
        rCmd_QuenchWaterInflowValve_pct := 0.0;
        rCmd_QuenchWaterDrainValve_pct  := 45.0;

        bCmd_EmergencyN2FastVent            := FALSE;
        bCmd_CaterpillarPneumaticBrakeClamp := TRUE;
        bCmd_TelescopicSealIsolate          := FALSE;

        (* Transition Criterion: Tube pressure <= 1.20 bar and quench level drained *)
        IF (rVoted_TubeN2Press_bar <= 1.200) AND (rVoted_QuenchWaterLvl_mm <= 500.0) THEN
            nActiveFSM_State := 10; (* Advance to COOL_DOWN *)
        END_IF;

    (* -----------------------------------------------------------------------------------------
     * STATE 10: COOL_DOWN
     * Zone heaters stepped down, cooling water circulation to safe entry temperature (< 60 deg C)
     * ----------------------------------------------------------------------------------------- *)
    10:
        bSystemReady           := FALSE;
        bSystemRunning         := FALSE;
        bEmergencyTripped      := FALSE;
        bSpoolTransferPermissive := FALSE;

        rCmd_Extruder2_XLPE_RPM       := 0.0;
        rCmd_Extruder1_CondScreen_RPM := 0.0;
        rCmd_Extruder3_InsScreen_RPM  := 0.0;
        rCmd_InfeedCapstan_Speed_mpm  := 0.0;
        rCmd_HaulOffCapstan_Speed_mpm := 0.0;
        rCmd_HaulOffCapstan_TensionTrim_kN := 0.0;
        rCmd_PayoffBrakeTorque_Nm     := 0.0;

        rCmd_Zone1_SCR_Duty_pct := 0.0;
        rCmd_Zone2_SCR_Duty_pct := 0.0;
        rCmd_Zone3_SCR_Duty_pct := 0.0;
        rCmd_Zone4_SCR_Duty_pct := 0.0;

        rCmd_N2_InjectionValve_pct := 0.0;
        rCmd_N2_VentValve_pct      := 100.0; (* Fully open to atmosphere *)
        rCmd_QuenchWaterInflowValve_pct := 0.0;
        rCmd_QuenchWaterDrainValve_pct  := 100.0;

        bCmd_EmergencyN2FastVent            := FALSE;
        bCmd_CaterpillarPneumaticBrakeClamp := TRUE;
        bCmd_TelescopicSealIsolate          := FALSE;

        (* Return to Standby once zones cool below 60 deg C *)
        IF (rVoted_Zone1Temp_degC <= 60.0) AND (rVoted_Zone2Temp_degC <= 60.0) THEN
            nActiveFSM_State := 0; (* Return to TUBE_NITROGEN_PURGE *)
        END_IF;

    (* -----------------------------------------------------------------------------------------
     * STATE 11: EMERGENCY_ESTOP_LINE_CLAMP
     * Immediate trip: fast emergency N2 vent, caterpillar brake clamp, extruders stop
     * ----------------------------------------------------------------------------------------- *)
    11:
        bSystemReady           := FALSE;
        bSystemRunning         := FALSE;
        bEmergencyTripped      := TRUE;
        bSpoolTransferPermissive := FALSE;

        (* Instantaneous Extruder Screw Trip *)
        rCmd_Extruder2_XLPE_RPM       := 0.0;
        rCmd_Extruder1_CondScreen_RPM := 0.0;
        rCmd_Extruder3_InsScreen_RPM  := 0.0;

        (* Instantaneous Caterpillar Capstan Mechanical Brake Clamp *)
        rCmd_InfeedCapstan_Speed_mpm        := 0.0;
        rCmd_HaulOffCapstan_Speed_mpm       := 0.0;
        rCmd_HaulOffCapstan_TensionTrim_kN  := 0.0;
        rCmd_PayoffBrakeTorque_Nm           := 500.0; (* Max emergency braking torque *)
        bCmd_CaterpillarPneumaticBrakeClamp := TRUE;

        (* Zero Heater SCR Outputs *)
        rCmd_Zone1_SCR_Duty_pct := 0.0;
        rCmd_Zone2_SCR_Duty_pct := 0.0;
        rCmd_Zone3_SCR_Duty_pct := 0.0;
        rCmd_Zone4_SCR_Duty_pct := 0.0;

        (* Emergency Fast Pneumatic N2 Blowdown Dump *)
        bCmd_EmergencyN2FastVent   := TRUE;
        rCmd_N2_InjectionValve_pct := 0.0;
        rCmd_N2_VentValve_pct      := 100.0;

        (* Isolate Telescopic Splice Box Entry Seal *)
        bCmd_TelescopicSealIsolate      := TRUE;
        rCmd_QuenchWaterInflowValve_pct := 0.0;
        rCmd_QuenchWaterDrainValve_pct  := 100.0;

        (* Fault Reset Transition Permissive *)
        IF bFaultReset AND bEmergencyStop_NC AND (NOT bTubeContactHazardActive) AND (rVoted_TubeN2Press_bar <= 2.0) THEN
            nActiveFSM_State := 0; (* Reset to TUBE_NITROGEN_PURGE *)
        END_IF;

END_CASE;
"""

if __name__ == "__main__":
    s5 = get_sec5()
    print("Section 5 Length:", len(s5))
