# Phase 6: ISA-18.2 Multi-Tiered Alarms & Diagnostic Packing for FB_Mining_SAG_BallMill_GrindingCircuit

def get_phase6():
    return """(* === PHASE 6: ISA-18.2 MULTI-TIERED ALARMS & DIAGNOSTIC WORD PACKING === *)

(* Initialize 32-Bit Alarm Words *)
wAlarmWord1_Process    := 16#0000_0000;
wAlarmWord2_Mechanical := 16#0000_0000;
wAlarmWord3_Sensors    := 16#0000_0000;
wAlarmWord4_Trips      := 16#0000_0000;

(* 6.1 Process Alarms (Word 1) *)
(* Bit 0: Total Charge Mass LO_LO (< 780 t) *)
IF rEstimatedChargeWeight_tons < c_rChargeWeight_LL_tons THEN
    wAlarmWord1_Process := wAlarmWord1_Process OR 16#0000_0001;
END_IF;

(* Bit 1: Total Charge Mass LO (< 850 t) *)
IF rEstimatedChargeWeight_tons < c_rChargeWeight_L_tons THEN
    wAlarmWord1_Process := wAlarmWord1_Process OR 16#0000_0002;
END_IF;

(* Bit 2: Total Charge Mass HI (> 1450 t) *)
IF rEstimatedChargeWeight_tons > c_rChargeWeight_H_tons THEN
    wAlarmWord1_Process := wAlarmWord1_Process OR 16#0000_0004;
END_IF;

(* Bit 3: Total Charge Mass HI_HI (> 1550 t) *)
IF rEstimatedChargeWeight_tons > c_rChargeWeight_HH_tons THEN
    wAlarmWord1_Process := wAlarmWord1_Process OR 16#0000_0008;
END_IF;

(* Bit 4: Dynamic Toe Angle LO_LO (< 32.0 deg) *)
IF rEstimatedToeAngle_deg < c_rToeAngle_LL_deg THEN
    wAlarmWord1_Process := wAlarmWord1_Process OR 16#0000_0010;
END_IF;

(* Bit 5: Dynamic Toe Angle HI_HI (> 54.0 deg) *)
IF rEstimatedToeAngle_deg > c_rToeAngle_HH_deg THEN
    wAlarmWord1_Process := wAlarmWord1_Process OR 16#0000_0020;
END_IF;

(* Bit 6: Sump Level LO_LO (< 18.0%) *)
IF rVoted_SumpLevel_pct < c_rSumpLevel_LL_pct THEN
    wAlarmWord1_Process := wAlarmWord1_Process OR 16#0000_0040;
    bSumpCavitationInterlock := TRUE;
ELSE
    bSumpCavitationInterlock := FALSE;
END_IF;

(* Bit 7: Sump Level LO (< 30.0%) *)
IF rVoted_SumpLevel_pct < c_rSumpLevel_L_pct THEN
    wAlarmWord1_Process := wAlarmWord1_Process OR 16#0000_0080;
END_IF;

(* Bit 8: Sump Level HI (> 80.0%) *)
IF rVoted_SumpLevel_pct > c_rSumpLevel_H_pct THEN
    wAlarmWord1_Process := wAlarmWord1_Process OR 16#0000_0100;
END_IF;

(* Bit 9: Sump Level HI_HI (> 90.0%) *)
IF rVoted_SumpLevel_pct > c_rSumpLevel_HH_pct THEN
    wAlarmWord1_Process := wAlarmWord1_Process OR 16#0000_0200;
    bSumpOverflowAlarm := TRUE;
ELSE
    bSumpOverflowAlarm := FALSE;
END_IF;

(* Bit 10: Slurry Density LO (< 1.450 t/m3) *)
IF rVoted_CycloneFeedDensity_SG < c_rFeedDensity_L_SG THEN
    wAlarmWord1_Process := wAlarmWord1_Process OR 16#0000_0400;
END_IF;

(* Bit 11: Slurry Density HI (> 1.720 t/m3) *)
IF rVoted_CycloneFeedDensity_SG > c_rFeedDensity_H_SG THEN
    wAlarmWord1_Process := wAlarmWord1_Process OR 16#0000_0800;
END_IF;

(* Bit 12: Product P80 Coarse HI (> 85.0 um) *)
IF rVoted_ProductP80_um > c_rProductP80_H_um THEN
    wAlarmWord1_Process := wAlarmWord1_Process OR 16#0000_1000;
    bProductOffSpecAlarm := TRUE;
ELSE
    bProductOffSpecAlarm := FALSE;
END_IF;

(* Bit 13: Product P80 Coarse HI_HI (> 95.0 um) *)
IF rVoted_ProductP80_um > c_rProductP80_HH_um THEN
    wAlarmWord1_Process := wAlarmWord1_Process OR 16#0000_2000;
END_IF;

(* Bit 14: Product P80 Over-Grinding LO (< 65.0 um) *)
IF rVoted_ProductP80_um < c_rProductP80_L_um THEN
    wAlarmWord1_Process := wAlarmWord1_Process OR 16#0000_4000;
END_IF;

(* 6.2 Mechanical & Thermal Alarms (Word 2) *)
(* Bit 0: Feed Trunnion Jacking Lift LO_LO (< 140 bar) *)
IF rVoted_FeedTrunnionLift_bar < c_rTrunnionLift_LL_bar THEN
    wAlarmWord2_Mechanical := wAlarmWord2_Mechanical OR 16#0000_0001;
END_IF;

(* Bit 1: Discharge Trunnion Jacking Lift LO_LO (< 140 bar) *)
IF rVoted_DischTrunnionLift_bar < c_rTrunnionLift_LL_bar THEN
    wAlarmWord2_Mechanical := wAlarmWord2_Mechanical OR 16#0000_0002;
END_IF;

(* Bit 2: Bearing Babbitt Temp HI (> 68 deg C) *)
IF (TT_FEED_BEARING_BABBITT_103A > c_rBabbittTemp_H_degC) OR
   (TT_DISCH_BEARING_BABBITT_104A > c_rBabbittTemp_H_degC) THEN
    wAlarmWord2_Mechanical := wAlarmWord2_Mechanical OR 16#0000_0004;
END_IF;

(* Bit 3: Bearing Babbitt Temp HI_HI (> 76 deg C) *)
IF (TT_FEED_BEARING_BABBITT_103A > c_rBabbittTemp_HH_degC) OR
   (TT_DISCH_BEARING_BABBITT_104A > c_rBabbittTemp_HH_degC) THEN
    wAlarmWord2_Mechanical := wAlarmWord2_Mechanical OR 16#0000_0008;
    bTrunnionLubeInterlockTrip := TRUE;
END_IF;

(* Bit 4: Ring Motor Active Power HI (> 26.5 MW) *)
IF rVoted_MotorPower_MW > c_rMotorPower_H_MW THEN
    wAlarmWord2_Mechanical := wAlarmWord2_Mechanical OR 16#0000_0010;
END_IF;

(* Bit 5: Ring Motor Active Power HI_HI (> 28.5 MW) *)
IF rVoted_MotorPower_MW > c_rMotorPower_HH_MW THEN
    wAlarmWord2_Mechanical := wAlarmWord2_Mechanical OR 16#0000_0020;
END_IF;

(* Bit 6: Ring Motor Stator Winding Temp HI (> 105 deg C) *)
IF TT_SAG_STATOR_TEMP_MAX_108A > c_rStatorTemp_H_degC THEN
    wAlarmWord2_Mechanical := wAlarmWord2_Mechanical OR 16#0000_0040;
END_IF;

(* Bit 7: Ring Motor Stator Winding Temp HI_HI (> 125 deg C) *)
IF TT_SAG_STATOR_TEMP_MAX_108A > c_rStatorTemp_HH_degC THEN
    wAlarmWord2_Mechanical := wAlarmWord2_Mechanical OR 16#0000_0080;
END_IF;

(* Bit 8: Rotor-Stator Electromagnetic Airgap Eccentricity LO (< 11.5 mm) *)
IF (ZT_SAG_WRAP_AROUND_AIRGAP_MM_109A < c_rAirgap_L_mm) OR
   (ZT_SAG_WRAP_AROUND_AIRGAP_MM_109B < c_rAirgap_L_mm) OR
   (ZT_SAG_WRAP_AROUND_AIRGAP_MM_109C < c_rAirgap_L_mm) THEN
    wAlarmWord2_Mechanical := wAlarmWord2_Mechanical OR 16#0000_0100;
END_IF;

(* Bit 9: Rotor-Stator Electromagnetic Airgap Rub Hazard LO_LO (< 9.5 mm) *)
IF (ZT_SAG_WRAP_AROUND_AIRGAP_MM_109A < c_rAirgap_LL_mm) OR
   (ZT_SAG_WRAP_AROUND_AIRGAP_MM_109B < c_rAirgap_LL_mm) OR
   (ZT_SAG_WRAP_AROUND_AIRGAP_MM_109C < c_rAirgap_LL_mm) THEN
    wAlarmWord2_Mechanical := wAlarmWord2_Mechanical OR 16#0000_0200;
END_IF;

(* Bit 10: Shell Direct Ball Impact HI (> 40.0 dB) *)
IF rVoted_ShellAcousticHighFreq_dB > c_rShellImpact_H_dB THEN
    wAlarmWord2_Mechanical := wAlarmWord2_Mechanical OR 16#0000_0400;
END_IF;

(* Bit 11: Shell Direct Ball Impact HI_HI Destructive (> 50.0 dB) *)
IF rVoted_ShellAcousticHighFreq_dB > c_rShellImpact_HH_dB THEN
    wAlarmWord2_Mechanical := wAlarmWord2_Mechanical OR 16#0000_0800;
    bDirectLinerImpactTrip := TRUE;
END_IF;

(* 6.3 Sensor Health & 2oo3 Discrepancy Diagnostics (Word 3) *)
IF bFault_FeedTrunnion THEN wAlarmWord3_Sensors := wAlarmWord3_Sensors OR 16#0000_0001; END_IF;
IF bFault_DischTrunnion THEN wAlarmWord3_Sensors := wAlarmWord3_Sensors OR 16#0000_0002; END_IF;
IF bFault_MotorPower THEN wAlarmWord3_Sensors := wAlarmWord3_Sensors OR 16#0000_0004; END_IF;
IF bFault_MotorSpeed THEN wAlarmWord3_Sensors := wAlarmWord3_Sensors OR 16#0000_0008; END_IF;
IF bFault_AcousticToe THEN wAlarmWord3_Sensors := wAlarmWord3_Sensors OR 16#0000_0010; END_IF;
IF bFault_AcousticHighFreq THEN wAlarmWord3_Sensors := wAlarmWord3_Sensors OR 16#0000_0020; END_IF;
IF bFault_SumpLevel THEN wAlarmWord3_Sensors := wAlarmWord3_Sensors OR 16#0000_0040; END_IF;
IF bFault_FeedDensity THEN wAlarmWord3_Sensors := wAlarmWord3_Sensors OR 16#0000_0080; END_IF;
IF bFault_ProductP80 THEN wAlarmWord3_Sensors := wAlarmWord3_Sensors OR 16#0000_0100; END_IF;

(* 6.4 Safety Instrumented System Fast Trip Initiators (Word 4) *)
IF bFrozenChargeTrip THEN wAlarmWord4_Trips := wAlarmWord4_Trips OR 16#0000_0001; END_IF;
IF NOT bEmergencyStop THEN wAlarmWord4_Trips := wAlarmWord4_Trips OR 16#0000_0002; END_IF;
IF bDirectLinerImpactTrip THEN wAlarmWord4_Trips := wAlarmWord4_Trips OR 16#0000_0004; END_IF;
IF bTrunnionLubeInterlockTrip THEN wAlarmWord4_Trips := wAlarmWord4_Trips OR 16#0000_0008; END_IF;
IF bSumpCavitationInterlock THEN wAlarmWord4_Trips := wAlarmWord4_Trips OR 16#0000_0010; END_IF;
IF (rEstimatedChargeWeight_tons > c_rChargeWeight_HH_tons) THEN
    wAlarmWord4_Trips := wAlarmWord4_Trips OR 16#0000_0020;
END_IF;

(* Calculate Mill Percentage of Critical Centrifuging Speed N_c *)
IF rSagCriticalSpeed_rpm > 0.0 THEN
    rMillFractionCriticalSpeed_pct := (rVoted_MotorSpeed_rpm / rSagCriticalSpeed_rpm) * 100.0;
ELSE
    rMillFractionCriticalSpeed_pct := 0.0;
END_IF;

END_FUNCTION_BLOCK
"""
