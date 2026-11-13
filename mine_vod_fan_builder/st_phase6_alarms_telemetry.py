# mine_vod_fan_builder/st_phase6_alarms_telemetry.py

def get_phase6_alarms_telemetry():
    return """(* ==================================================================================================== *)
(* PHASE 6: ISA-18.2 MULTI-TIER ALARMS, BIT-PACKED STATUS WORDS & ACTUATOR CLAMPING                      *)
(* ==================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------- *)
(* SUB-PHASE 6.1: ISA-18.2 Multi-Tier Process Alarm Evaluation                                         *)
(* ---------------------------------------------------------------------------------------------------- *)
(* Reset Temporary Bit Fields *)
dwAlarmWord1 := 16#00000000;
dwAlarmWord2 := 16#00000000;
dwStatusWord1 := 16#00000000;
dwStatusWord2 := 16#00000000;

(* --- High-High (HH) and Low-Low (LL) Critical Trips (dwAlarmWord1) --- *)

(* Bit 0: Fan Differential Pressure High-High Trip (> 6.2 kPa) *)
IF rDP_Voted >= rDP_Trip_HH THEN
    dwAlarmWord1 := dwAlarmWord1 OR 16#00000001;
    bTripGeneral := TRUE;
END_IF;

(* Bit 1: Fan Differential Pressure Low-Low Trip (< 0.8 kPa) *)
IF (eState >= 4) AND (rDP_Voted <= rDP_Trip_LL) THEN
    dwAlarmWord1 := dwAlarmWord1 OR 16#00000002;
    bTripGeneral := TRUE;
END_IF;

(* Bit 2: Stall Margin Low-Low Critical Trip (< 8.0 %) *)
IF (eState >= 4) AND (rFanStallMargin_pct <= rStall_Trip_LL) THEN
    dwAlarmWord1 := dwAlarmWord1 OR 16#00000004;
    bTripGeneral := TRUE;
END_IF;

(* Bit 3: Blade Tip Dynamic Turbulence High-High Trip (> 180 Pa RMS) *)
IF (eState >= 4) AND (rBladeTipTurbulenceRMS_Pa >= rTurb_Trip_HH) THEN
    dwAlarmWord1 := dwAlarmWord1 OR 16#00000008;
    bTripGeneral := TRUE;
END_IF;

(* Bit 4: Heading Toxic Gas Carbon Monoxide High-High Trip (> 50 ppm) *)
IF rToxicGas_Voted >= rCO_Trip_HH THEN
    dwAlarmWord1 := dwAlarmWord1 OR 16#00000010;
END_IF;

(* Bit 5: Heading Toxic Gas Nitrogen Dioxide High-High Trip (> 6.0 ppm) *)
IF (rToxicGas_Voted * 0.125) >= (rNO2_SafeReentryLimit_ppm * 2.0) THEN
    dwAlarmWord1 := dwAlarmWord1 OR 16#00000020;
END_IF;

(* Bit 6: Diesel Particulate Matter (DPM) High-High Trip (> 320 ug/m3) *)
IF (rToxicGas_Voted * 8.5) >= (rDPM_SafeReentryLimit_ug_m3 * 2.0) THEN
    dwAlarmWord1 := dwAlarmWord1 OR 16#00000040;
END_IF;

(* Bit 7: Fan Bearing Vibration Velocity High-High Trip (> 7.5 mm/s RMS) *)
IF rVib_Voted >= rVib_Trip_HH THEN
    dwAlarmWord1 := dwAlarmWord1 OR 16#00000080;
    bTripGeneral := TRUE;
END_IF;

(* Bit 8: Fan 1 Motor Winding Temperature High-High Trip (> 135 deg C) *)
IF rFan1_MotorWindingTemp_degC >= rWindingTemp_Trip_HH THEN
    dwAlarmWord1 := dwAlarmWord1 OR 16#00000100;
    bTripGeneral := TRUE;
END_IF;

(* Bit 9: Fan 2 Motor Winding Temperature High-High Trip (> 135 deg C) *)
IF rFan2_MotorWindingTemp_degC >= rWindingTemp_Trip_HH THEN
    dwAlarmWord1 := dwAlarmWord1 OR 16#00000200;
    bTripGeneral := TRUE;
END_IF;

(* Bit 10: Fan 1 Lube Oil Pressure Low-Low Trip (< 2.1 bar) *)
IF (eState >= 2) AND (rFan1_LubeOilPressure_bar <= rLubeOil_Trip_LL) AND (bDualFanParallelMode OR NOT bLeadFanSelect) THEN
    dwAlarmWord1 := dwAlarmWord1 OR 16#00000400;
    bTripGeneral := TRUE;
END_IF;

(* Bit 11: Fan 2 Lube Oil Pressure Low-Low Trip (< 2.1 bar) *)
IF (eState >= 2) AND (rFan2_LubeOilPressure_bar <= rLubeOil_Trip_LL) AND (bDualFanParallelMode OR bLeadFanSelect) THEN
    dwAlarmWord1 := dwAlarmWord1 OR 16#00000800;
    bTripGeneral := TRUE;
END_IF;

(* Bit 12: Intake Shaft Collar Temperature Low-Low Freeze Trip (< -2.0 deg C) *)
IF rSurfaceAirTemp_degC <= rIntakeTemp_Trip_LL THEN
    dwAlarmWord1 := dwAlarmWord1 OR 16#00001000;
END_IF;

(* Bit 13: Emergency Smoke Backlayering Velocity Lock Violation *)
IF bSmokeReversalLockEngaged AND (rAir_Vel_Voted < rCriticalBacklayeringVel_Calc) THEN
    dwAlarmWord1 := dwAlarmWord1 OR 16#00002000;
END_IF;

(* Bit 14: Hardwired Emergency Stop Active *)
IF bEmergencyStop THEN
    dwAlarmWord1 := dwAlarmWord1 OR 16#00004000;
END_IF;

(* Bit 15: General Trip Summary Master Flag *)
IF bTripGeneral THEN
    dwAlarmWord1 := dwAlarmWord1 OR 16#00008000;
END_IF;

(* --- High (H) and Low (L) Advisory Warnings (dwAlarmWord2) --- *)

(* Bit 0: Fan Differential Pressure High Warning (> 5.2 kPa) *)
IF rDP_Voted >= rDP_Warn_H THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#00000001;
    bWarningGeneral := TRUE;
END_IF;

(* Bit 1: Fan Differential Pressure Low Warning (< 1.8 kPa) *)
IF (eState >= 4) AND (rDP_Voted <= rDP_Warn_L) THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#00000002;
    bWarningGeneral := TRUE;
END_IF;

(* Bit 2: Stall Margin Low Advisory Warning (< 18.0 %) *)
IF (eState >= 4) AND (rFanStallMargin_pct <= rStall_Warn_L) THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#00000004;
    bWarningGeneral := TRUE;
END_IF;

(* Bit 3: Blade Tip Dynamic Turbulence High Warning (> 95 Pa RMS) *)
IF (eState >= 4) AND (rBladeTipTurbulenceRMS_Pa >= rTurb_Warn_H) THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#00000008;
    bWarningGeneral := TRUE;
END_IF;

(* Bit 4: Heading Toxic Gas Carbon Monoxide High Warning (> 25 ppm) *)
IF rToxicGas_Voted >= rCO_Warn_H THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#00000010;
    bWarningGeneral := TRUE;
END_IF;

(* Bit 5: Heading Toxic Gas Nitrogen Dioxide High Warning (> 3.0 ppm) *)
IF (rToxicGas_Voted * 0.125) >= rNO2_SafeReentryLimit_ppm THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#00000020;
    bWarningGeneral := TRUE;
END_IF;

(* Bit 6: Diesel Particulate Matter High Warning (> 160 ug/m3) *)
IF (rToxicGas_Voted * 8.5) >= rDPM_SafeReentryLimit_ug_m3 THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#00000040;
    bWarningGeneral := TRUE;
END_IF;

(* Bit 7: Fan Bearing Vibration Velocity High Warning (> 4.5 mm/s RMS) *)
IF rVib_Voted >= rVib_Warn_H THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#00000080;
    bWarningGeneral := TRUE;
END_IF;

(* Bit 8: Fan 1 Motor Winding Temperature High Warning (> 115 deg C) *)
IF rFan1_MotorWindingTemp_degC >= rWindingTemp_Warn_H THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#00000100;
    bWarningGeneral := TRUE;
END_IF;

(* Bit 9: Fan 2 Motor Winding Temperature High Warning (> 115 deg C) *)
IF rFan2_MotorWindingTemp_degC >= rWindingTemp_Warn_H THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#00000200;
    bWarningGeneral := TRUE;
END_IF;

(* Bit 10: Fan 1 Lube Oil Pressure Low Warning (< 2.8 bar) *)
IF (eState >= 2) AND (rFan1_LubeOilPressure_bar <= rLubeOil_Warn_L) AND (bDualFanParallelMode OR NOT bLeadFanSelect) THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#00000400;
    bWarningGeneral := TRUE;
END_IF;

(* Bit 11: Fan 2 Lube Oil Pressure Low Warning (< 2.8 bar) *)
IF (eState >= 2) AND (rFan2_LubeOilPressure_bar <= rLubeOil_Warn_L) AND (bDualFanParallelMode OR bLeadFanSelect) THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#00000800;
    bWarningGeneral := TRUE;
END_IF;

(* Bit 12: Intake Shaft Collar Temperature Freeze Warning (< 1.5 deg C) *)
IF rSurfaceAirTemp_degC <= rIntakeTemp_Warn_L THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#00001000;
    bWarningGeneral := TRUE;
END_IF;

(* Bit 13: Fan DP TMR Channel Discrepancy Fault *)
IF bDP_Ch1_Fault OR bDP_Ch2_Fault OR bDP_Ch3_Fault THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#00002000;
    bWarningGeneral := TRUE;
END_IF;

(* Bit 14: Air Velocity TMR Channel Discrepancy Fault *)
IF bAirVel_Ch1_Fault OR bAirVel_Ch2_Fault OR bAirVel_Ch3_Fault THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#00004000;
    bWarningGeneral := TRUE;
END_IF;

(* Bit 15: Toxic Gas TMR Channel Discrepancy Fault *)
IF bToxicGas_Ch1_Fault OR bToxicGas_Ch2_Fault OR bToxicGas_Ch3_Fault THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#00008000;
    bWarningGeneral := TRUE;
END_IF;

(* Bit 16: Fan Vibration TMR Channel Discrepancy Fault *)
IF bVib_Ch1_Fault OR bVib_Ch2_Fault OR bVib_Ch3_Fault THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#00010000;
    bWarningGeneral := TRUE;
END_IF;

(* Bit 17: Master Warning Summary Flag *)
IF bWarningGeneral THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#00020000;
END_IF;

(* Reset Master Trip on Reset Command if Conditions Normal *)
IF bReset AND NOT bEmergencyStop THEN
    IF (rDP_Voted < rDP_Trip_HH) AND (rVib_Voted < rVib_Trip_HH) AND NOT bEmergencyTripLatched THEN
        bTripGeneral := FALSE;
    END_IF;
    bWarningGeneral := FALSE;
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* SUB-PHASE 6.2: Status Word Bit-Packing (dwStatusWord1 & dwStatusWord2)                               *)
(* ---------------------------------------------------------------------------------------------------- *)
(* dwStatusWord1: FSM State & Subsystem Operational Indicators *)
dwStatusWord1 := INT_TO_DWORD(eState) AND 16#0000000F; (* Bits 0..3: Current FSM State *)
IF bEnable THEN dwStatusWord1 := dwStatusWord1 OR 16#00000010; END_IF; (* Bit 4 *)
IF bAutoVOD_Mode THEN dwStatusWord1 := dwStatusWord1 OR 16#00000020; END_IF; (* Bit 5 *)
IF bDualFanParallelMode THEN dwStatusWord1 := dwStatusWord1 OR 16#00000040; END_IF; (* Bit 6 *)
IF NOT bLeadFanSelect THEN dwStatusWord1 := dwStatusWord1 OR 16#00000080; END_IF; (* Bit 7: Fan 1 Lead *)
IF bLeadFanSelect THEN dwStatusWord1 := dwStatusWord1 OR 16#00000100; END_IF; (* Bit 8: Fan 2 Lead *)
IF bFan1_RunCmd THEN dwStatusWord1 := dwStatusWord1 OR 16#00000200; END_IF; (* Bit 9 *)
IF bFan2_RunCmd THEN dwStatusWord1 := dwStatusWord1 OR 16#00000400; END_IF; (* Bit 10 *)
IF bFanAntiStallBypassDamperOpenCmd THEN dwStatusWord1 := dwStatusWord1 OR 16#00000800; END_IF; (* Bit 11 *)
IF rSurfaceFanLubePumpRunCmd THEN dwStatusWord1 := dwStatusWord1 OR 16#00001000; END_IF; (* Bit 12 *)
IF rSurfaceFanHydraulicPumpRunCmd THEN dwStatusWord1 := dwStatusWord1 OR 16#00002000; END_IF; (* Bit 13 *)
IF bPostBlastPurgeRequest OR (iActiveBlastingZoneIndex > 0) THEN dwStatusWord1 := dwStatusWord1 OR 16#00004000; END_IF; (* Bit 14 *)
IF bDieselHaulageBoostRequest THEN dwStatusWord1 := dwStatusWord1 OR 16#00008000; END_IF; (* Bit 15 *)
IF bAntiStallActive THEN dwStatusWord1 := dwStatusWord1 OR 16#00010000; END_IF; (* Bit 16 *)
IF bIcePreventionEnable AND (rSurfaceAirTemp_degC < 3.0) THEN dwStatusWord1 := dwStatusWord1 OR 16#00020000; END_IF; (* Bit 17 *)
IF bFireSmokeEmergencyTrip OR (iFireZoneIndex > 0) THEN dwStatusWord1 := dwStatusWord1 OR 16#00040000; END_IF; (* Bit 18 *)
IF bSmokeReversalLockEngaged THEN dwStatusWord1 := dwStatusWord1 OR 16#00080000; END_IF; (* Bit 19 *)

(* dwStatusWord2: TMR Degradation Modes & Active Louver Flow Deficit Flags *)
dwStatusWord2 := (INT_TO_DWORD(iDP_DegradationMode) AND 16#00000003); (* Bits 0..1 *)
dwStatusWord2 := dwStatusWord2 OR SHL((INT_TO_DWORD(iAirVel_DegradationMode) AND 16#00000003), 2); (* Bits 2..3 *)
dwStatusWord2 := dwStatusWord2 OR SHL((INT_TO_DWORD(iToxicGas_DegradationMode) AND 16#00000003), 4); (* Bits 4..5 *)
dwStatusWord2 := dwStatusWord2 OR SHL((INT_TO_DWORD(iVib_DegradationMode) AND 16#00000003), 6); (* Bits 6..7 *)

(* Bits 8..31: Louver 1..24 Flow Deficit Exceedance Flags *)
FOR iLoopIdx := 1 TO 24 DO
    IF arrZoneAirflowDeficit_m3s[iLoopIdx] > 2.0 THEN
        dwStatusWord2 := dwStatusWord2 OR SHL(16#00000001, (7 + iLoopIdx));
    END_IF;
END_FOR;

(* ---------------------------------------------------------------------------------------------------- *)
(* SUB-PHASE 6.3: Actuator Command Final Bounding & Bumpless Transfer Safeguards                         *)
(* ---------------------------------------------------------------------------------------------------- *)
(* Clamp Fan 1 Outputs *)
IF rFan1_BladePitchCmd_deg < -12.0 THEN rFan1_BladePitchCmd_deg := -12.0; ELSIF rFan1_BladePitchCmd_deg > 38.0 THEN rFan1_BladePitchCmd_deg := 38.0; END_IF;
IF rFan1_VFD_SpeedCmd_RPM < 0.0 THEN rFan1_VFD_SpeedCmd_RPM := 0.0; ELSIF rFan1_VFD_SpeedCmd_RPM > 1050.0 THEN rFan1_VFD_SpeedCmd_RPM := 1050.0; END_IF;

(* Clamp Fan 2 Outputs *)
IF rFan2_BladePitchCmd_deg < -12.0 THEN rFan2_BladePitchCmd_deg := -12.0; ELSIF rFan2_BladePitchCmd_deg > 38.0 THEN rFan2_BladePitchCmd_deg := 38.0; END_IF;
IF rFan2_VFD_SpeedCmd_RPM < 0.0 THEN rFan2_VFD_SpeedCmd_RPM := 0.0; ELSIF rFan2_VFD_SpeedCmd_RPM > 1050.0 THEN rFan2_VFD_SpeedCmd_RPM := 1050.0; END_IF;

(* Clamp Heating Valve Command [0..100%] *)
IF rIntakeCollarHeaterValveCmd_pct < 0.0 THEN rIntakeCollarHeaterValveCmd_pct := 0.0; ELSIF rIntakeCollarHeaterValveCmd_pct > 100.0 THEN rIntakeCollarHeaterValveCmd_pct := 100.0; END_IF;

END_FUNCTION_BLOCK
"""
