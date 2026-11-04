# brain_scratch/can_seamer_builder/part7_alarms_clamp.py

PART7_ALARMS_CLAMP = """
(* ==========================================================================================
 * PHASE 10: ISA-18.2 MULTI-TIERED ALARM ENGINE & DIAGNOSTIC WORD PACKING
 * Multi-tiered alarm hierarchy structured according to ANSI/ISA-18.2:
 *   Priority 1: Critical Safety & Emergency Abort (Immediate Machine Stop / Lifter Retract)
 *   Priority 2: Process Out-of-Spec & Quality Rejection (Diverter Gate Actuation)
 *   Priority 3: Diagnostic, TMR Sensor Degradation & Predictive Maintenance Advisory
 * ========================================================================================== *)

(* Reset Master Alarm Registers *)
dwAlarm_Critical_Safety := DWORD#16#00000000;
dwAlarm_Process_Quality := DWORD#16#00000000;
dwAlarm_Diagnostic_Wear := DWORD#16#00000000;
dwSystem_Status_Word    := DWORD#16#00000000;

(* ------------------------------------------------------------------------------------------
 * Priority 1: Critical Safety Alarms Packing (dwAlarm_Critical_Safety)
 * ------------------------------------------------------------------------------------------ *)
IF NOT bEStop_Ok THEN
    dwAlarm_Critical_Safety := dwAlarm_Critical_Safety OR DWORD#16#00000001; (* Bit 0: Hardware Dual-Channel E-Stop Open *)
END_IF;
IF bAlarm_TurretJam_Fault THEN
    dwAlarm_Critical_Safety := dwAlarm_Critical_Safety OR DWORD#16#00000002; (* Bit 1: Turret Mechanical Jam Torque Trip *)
END_IF;
IF bDischarge_Jam_Sensor THEN
    dwAlarm_Critical_Safety := dwAlarm_Critical_Safety OR DWORD#16#00000004; (* Bit 2: Discharge Conveyor Container Backlog Jam *)
END_IF;
IF bAlarm_SteamTemp_LL THEN
    dwAlarm_Critical_Safety := dwAlarm_Critical_Safety OR DWORD#16#00000008; (* Bit 3: Aseptic Steam Barrier Loss (< 118 deg C) *)
END_IF;
IF bAlarm_AxialLoad_HH THEN
    dwAlarm_Critical_Safety := dwAlarm_Critical_Safety OR DWORD#16#00000010; (* Bit 4: Chuck Axial Mechanical Overload (> 8.5 kN) *)
END_IF;
IF bAlarm_AxialLoad_LL THEN
    dwAlarm_Critical_Safety := dwAlarm_Critical_Safety OR DWORD#16#00000020; (* Bit 5: Chuck Preload Collapse / Can Crushed (< 3.0 kN) *)
END_IF;
IF bAlarm_LN2Press_HH THEN
    dwAlarm_Critical_Safety := dwAlarm_Critical_Safety OR DWORD#16#00000040; (* Bit 6: Cryogenic LN2 Line Overpressure (> 3.8 bar) *)
END_IF;
IF bAlarm_LN2Press_LL THEN
    dwAlarm_Critical_Safety := dwAlarm_Critical_Safety OR DWORD#16#00000080; (* Bit 7: Cryogenic LN2 Supply Depleted (< 1.2 bar) *)
END_IF;

(* ------------------------------------------------------------------------------------------
 * Priority 2: Process & Quality Alarms Packing (dwAlarm_Process_Quality)
 * ------------------------------------------------------------------------------------------ *)
IF bAlarm_SeamThickness_Fault THEN
    dwAlarm_Process_Quality := dwAlarm_Process_Quality OR DWORD#16#00000001; (* Bit 0: Double Seam Thickness Out-of-Spec *)
END_IF;
IF bAlarm_Acoustic_Leak_Fault THEN
    dwAlarm_Process_Quality := dwAlarm_Process_Quality OR DWORD#16#00000002; (* Bit 1: Acoustic Resonance Micro-Leak / Flat Can *)
END_IF;
IF bAlarm_Oxygen_Elevated THEN
    dwAlarm_Process_Quality := dwAlarm_Process_Quality OR DWORD#16#00000004; (* Bit 2: Headspace Residual Oxygen Exceeds 0.8% *)
END_IF;
IF rSeam_TheoreticalOverlap_Pct < 65.0 THEN
    dwAlarm_Process_Quality := dwAlarm_Process_Quality OR DWORD#16#00000008; (* Bit 3: Double Seam Overlap Below 65% Minimum *)
END_IF;
IF rSeam_TightnessRating_Pct < 70.0 THEN
    dwAlarm_Process_Quality := dwAlarm_Process_Quality OR DWORD#16#00000010; (* Bit 4: Double Seam Tightness Rating Below 70% *)
END_IF;
IF ABS(rInfeed_Phase_Trim_Deg) > 4.50 THEN
    dwAlarm_Process_Quality := dwAlarm_Process_Quality OR DWORD#16#00000020; (* Bit 5: Infeed Worm Screw Phase Jitter Warning *)
END_IF;
IF NOT bEnd_Present_Chute THEN
    dwAlarm_Process_Quality := dwAlarm_Process_Quality OR DWORD#16#00000040; (* Bit 6: Can End / Lid Stack Starvation Chute Low *)
END_IF;

(* ------------------------------------------------------------------------------------------
 * Priority 3: Diagnostic & Predictive Wear Alarms Packing (dwAlarm_Diagnostic_Wear)
 * ------------------------------------------------------------------------------------------ *)
IF bAlarm_TMR_Axial_Discrep THEN
    dwAlarm_Diagnostic_Wear := dwAlarm_Diagnostic_Wear OR DWORD#16#00000001; (* Bit 0: Chuck Load 2oo3 Sensor Discrepancy *)
END_IF;
IF bAlarm_TMR_LN2_Discrep THEN
    dwAlarm_Diagnostic_Wear := dwAlarm_Diagnostic_Wear OR DWORD#16#00000002; (* Bit 1: LN2 Pressure 2oo3 Sensor Discrepancy *)
END_IF;
IF bAlarm_TMR_Steam_Discrep THEN
    dwAlarm_Diagnostic_Wear := dwAlarm_Diagnostic_Wear OR DWORD#16#00000004; (* Bit 2: Steam Temp 2oo3 Sensor Discrepancy *)
END_IF;
IF bAlarm_TMR_Acoustic_Discrep THEN
    dwAlarm_Diagnostic_Wear := dwAlarm_Diagnostic_Wear OR DWORD#16#00000008; (* Bit 3: Acoustic Sensor 2oo3 Discrepancy *)
END_IF;
IF bAlarm_IndividualHead_WearWarn THEN
    dwAlarm_Diagnostic_Wear := dwAlarm_Diagnostic_Wear OR DWORD#16#00000010; (* Bit 4: One or more seaming heads exceed 80% wear *)
END_IF;
IF ABS(rTorqueRipple_Harmonic1_Nm) > 18.0 THEN
    dwAlarm_Diagnostic_Wear := dwAlarm_Diagnostic_Wear OR DWORD#16#00000020; (* Bit 5: 18th Harmonic Torque Ripple Excessive *)
END_IF;
IF rF0_Lethality_Rate_min_s < 0.50 AND bIn_Production THEN
    dwAlarm_Diagnostic_Wear := dwAlarm_Diagnostic_Wear OR DWORD#16#00000040; (* Bit 6: F0 Sterilization Rate Depressed *)
END_IF;

(* Master System Operational Status Word Packing *)
IF bSystem_Ready THEN
    dwSystem_Status_Word := dwSystem_Status_Word OR DWORD#16#00000001; (* Bit 0: Ready *)
END_IF;
IF bIn_Production THEN
    dwSystem_Status_Word := dwSystem_Status_Word OR DWORD#16#00000002; (* Bit 1: In Production *)
END_IF;
IF bEStop_Tripped THEN
    dwSystem_Status_Word := dwSystem_Status_Word OR DWORD#16#00000004; (* Bit 2: E-Stop Tripped *)
END_IF;
dwSystem_Status_Word := dwSystem_Status_Word OR SHL(INT_TO_DWORD(iCurrent_FSM_State), 8); (* Bits 8..15: Active State Code *)

(* ==========================================================================================
 * PHASE 11: ACTUATOR OUTPUT SATURATION, SLEW-RATE LIMITING & SAFE CLAMPING
 * Rate limiters protect precision servo gearboxes, cryogenic valves, and steam valves
 * from destructive mechanical shock and thermal cavitation.
 * ========================================================================================== *)

(* 1. Turret Speed Servo Reference Slew Rate Limiter (Max 15.0 RPM/s) *)
IF (rTurret_Speed_Command_RPM - rLast_Turret_Speed_Cmd) > (rMaxRate_TurretSpeed_RPM_s * rDeltaT) THEN
    rTurret_Speed_Command_RPM := rLast_Turret_Speed_Cmd + (rMaxRate_TurretSpeed_RPM_s * rDeltaT);
ELSIF (rLast_Turret_Speed_Cmd - rTurret_Speed_Command_RPM) > (rMaxRate_TurretSpeed_RPM_s * rDeltaT) THEN
    rTurret_Speed_Command_RPM := rLast_Turret_Speed_Cmd - (rMaxRate_TurretSpeed_RPM_s * rDeltaT);
END_IF;
rTurret_Speed_Command_RPM := MAX(0.0, MIN(75.0, rTurret_Speed_Command_RPM));
rLast_Turret_Speed_Cmd := rTurret_Speed_Command_RPM;

(* 2. Saturated Steam Barrier Modulation Valve Slew Rate Limiter (Max 8.0 %/s) *)
IF (rSteamBarrier_Valve_Position_Pct - rLast_SteamValve_Cmd) > (rMaxRate_SteamValve_Pct_s * rDeltaT) THEN
    rSteamBarrier_Valve_Position_Pct := rLast_SteamValve_Cmd + (rMaxRate_SteamValve_Pct_s * rDeltaT);
ELSIF (rLast_SteamValve_Cmd - rSteamBarrier_Valve_Position_Pct) > (rMaxRate_SteamValve_Pct_s * rDeltaT) THEN
    rSteamBarrier_Valve_Position_Pct := rLast_SteamValve_Cmd - (rMaxRate_SteamValve_Pct_s * rDeltaT);
END_IF;
rSteamBarrier_Valve_Position_Pct := MAX(0.0, MIN(100.0, rSteamBarrier_Valve_Position_Pct));
rLast_SteamValve_Cmd := rSteamBarrier_Valve_Position_Pct;

(* 3. Cryogenic LN2 Injection Pulse Width Slew Rate Limiter (Max 25.0 ms/s) *)
IF (rLN2_InjectorPulse_ms - rLast_LN2Pulse_Cmd) > (rMaxRate_LN2Pulse_ms_s * rDeltaT) THEN
    rLN2_InjectorPulse_ms := rLast_LN2Pulse_Cmd + (rMaxRate_LN2Pulse_ms_s * rDeltaT);
ELSIF (rLast_LN2Pulse_Cmd - rLN2_InjectorPulse_ms) > (rMaxRate_LN2Pulse_ms_s * rDeltaT) THEN
    rLN2_InjectorPulse_ms := rLast_LN2Pulse_Cmd - (rMaxRate_LN2Pulse_ms_s * rDeltaT);
END_IF;
rLN2_InjectorPulse_ms := MAX(2.0, MIN(35.0, rLN2_InjectorPulse_ms));
rLast_LN2Pulse_Cmd := rLN2_InjectorPulse_ms;

(* 4. 1st & 2nd Operation Servo Cam Depth Trim Slew Rate Limiters (Max 1.20 mm/s) *)
IF (rSeamingRoll_1stOp_CamTrim_mm - rLast_1stOp_CamTrim) > (rMaxRate_CamDepth_mm_s * rDeltaT) THEN
    rSeamingRoll_1stOp_CamTrim_mm := rLast_1stOp_CamTrim + (rMaxRate_CamDepth_mm_s * rDeltaT);
ELSIF (rLast_1stOp_CamTrim - rSeamingRoll_1stOp_CamTrim_mm) > (rMaxRate_CamDepth_mm_s * rDeltaT) THEN
    rSeamingRoll_1stOp_CamTrim_mm := rLast_1stOp_CamTrim - (rMaxRate_CamDepth_mm_s * rDeltaT);
END_IF;
rSeamingRoll_1stOp_CamTrim_mm := MAX(-0.50, MIN(0.50, rSeamingRoll_1stOp_CamTrim_mm));
rLast_1stOp_CamTrim := rSeamingRoll_1stOp_CamTrim_mm;

IF (rSeamingRoll_2ndOp_CamTrim_mm - rLast_2ndOp_CamTrim) > (rMaxRate_CamDepth_mm_s * rDeltaT) THEN
    rSeamingRoll_2ndOp_CamTrim_mm := rLast_2ndOp_CamTrim + (rMaxRate_CamDepth_mm_s * rDeltaT);
ELSIF (rLast_2ndOp_CamTrim - rSeamingRoll_2ndOp_CamTrim_mm) > (rMaxRate_CamDepth_mm_s * rDeltaT) THEN
    rSeamingRoll_2ndOp_CamTrim_mm := rLast_2ndOp_CamTrim - (rMaxRate_CamDepth_mm_s * rDeltaT);
END_IF;
rSeamingRoll_2ndOp_CamTrim_mm := MAX(-0.35, MIN(0.35, rSeamingRoll_2ndOp_CamTrim_mm));
rLast_2ndOp_CamTrim := rSeamingRoll_2ndOp_CamTrim_mm;

(* 5. Emergency Interlock Fail-Safe Clamping *)
IF bEStop_Tripped OR NOT bEStop_Ok THEN
    rTurret_Speed_Command_RPM       := 0.0;
    rInfeed_Phase_Trim_Deg          := 0.0;
    rInfeed_Starwheel_Phase_Trim_Deg:= 0.0;
    rSeamingRoll_1stOp_CamTrim_mm   := 0.0;
    rSeamingRoll_2ndOp_CamTrim_mm   := 0.0;
    bCan_Lifter_ChamberPneumatic_Up := FALSE;
    bLid_Separator_Release_Solenoid := FALSE;
    bLN2_Dosing_Valve_Trigger       := FALSE;
    bAcoustic_Ping_Exciter_Trigger  := FALSE;
    bReject_Gate_Actuator_Pulse     := FALSE;
END_IF;

END_FUNCTION_BLOCK
"""
