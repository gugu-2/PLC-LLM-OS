# build_st_phase5_alarms_telemetry.py
# Section 8: Phase 5 - ISA-18.2 Process Alarms, Bit-Packed Telemetry, Actuator Limits & Final Block Termination

def get_phase5_alarms_telemetry():
    code = []
    code.append("""(* =====================================================================================================================
 * PHASE 5: ISA-18.2 MULTI-TIER PROCESS ALARMS, BIT-PACKED TELEMETRY & ACTUATOR SAFEGUARDS
 * Architecture:
 *   - ISA-18.2 Alarm Qualification with Configurable Debounce Timers & Deadbands
 *   - Class 1E First-Out Forensic Latch Engine for Reactor Trip Sequence-of-Events
 *   - IEEE 603 Slew Rate Limiter and Manual/Auto Station Bump-Free Transfer
 *   - 32-Bit Bit-Packed Telemetry Status and Alarm Words
 * ===================================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------------------------
 * SECTION 5.1: ISA-18.2 PROCESS ALARM QUALIFICATION & DEBOUNCE EVALUATION
 * --------------------------------------------------------------------------------------------------------------------- *)
(* Reset latched alarms on operator acknowledge and trip reset *)
IF bReset_Trip_Interlocks AND bAcknowledge_Alarms THEN
    IF rVoted_Level_NR < (rTrip_Level_NR_HighHigh_HH - rDeadband_Level_NR) THEN
        bActive_Alarm_Level_HH := FALSE;
    END_IF;
    IF rVoted_Level_NR > (rTrip_Level_NR_LowLow_LL + rDeadband_Level_NR) THEN
        bActive_Alarm_Level_LL := FALSE;
    END_IF;
    IF rVoted_Press_SteamDrum < (rTrip_Press_SteamDrum_HH - rDeadband_Press_SteamDrum) THEN
        bActive_Alarm_Press_HH := FALSE;
    END_IF;
    IF rVoted_Press_SteamDrum > (rTrip_Press_SteamDrum_LL + rDeadband_Press_SteamDrum) THEN
        bActive_Alarm_Press_LL := FALSE;
    END_IF;
    IF (rRad_N16_SteamLine_ChA < rTrip_N16_Radiation_SGTR_HH * 0.5) AND (rRad_N16_SteamLine_ChB < rTrip_N16_Radiation_SGTR_HH * 0.5) THEN
        bActive_Alarm_SGTR_Trip := FALSE;
    END_IF;
END_IF;

(* 1) High-High Narrow Range Level Trip (P-14) *)
IF rVoted_Level_NR >= rTrip_Level_NR_HighHigh_HH THEN
    rTimer_Alarm_Level_HH := rTimer_Alarm_Level_HH + rScan_Period_Ts;
    IF rTimer_Alarm_Level_HH >= 0.100 THEN (* 100 ms hard qualification *)
        bActive_Alarm_Level_HH := TRUE;
        bDemand_MFRV_Isolation_P14 := TRUE;
        (* First-Out Latching *)
        IF dwFirstOutWord = 16#00000000 THEN
            dwFirstOutWord := 16#00000001; (* Bit 0: Level High-High First Out *)
        END_IF;
    END_IF;
ELSE
    rTimer_Alarm_Level_HH := 0.0;
    IF rVoted_Level_NR <= (rTrip_Level_NR_HighHigh_HH - rDeadband_Level_NR) THEN
        IF NOT bActive_Alarm_Level_HH THEN
            bDemand_MFRV_Isolation_P14 := FALSE;
        END_IF;
    END_IF;
END_IF;

(* 2) High Narrow Range Level Warning *)
IF rVoted_Level_NR >= rAlarm_Level_NR_High_H THEN
    rTimer_Alarm_Level_H := rTimer_Alarm_Level_H + rScan_Period_Ts;
    IF rTimer_Alarm_Level_H >= 0.500 THEN
        bActive_Alarm_Level_H := TRUE;
    END_IF;
ELSIF rVoted_Level_NR <= (rAlarm_Level_NR_High_H - rDeadband_Level_NR) THEN
    rTimer_Alarm_Level_H := 0.0;
    bActive_Alarm_Level_H := FALSE;
END_IF;

(* 3) Low Narrow Range Level Warning *)
IF rVoted_Level_NR <= rAlarm_Level_NR_Low_L THEN
    rTimer_Alarm_Level_L := rTimer_Alarm_Level_L + rScan_Period_Ts;
    IF rTimer_Alarm_Level_L >= 0.500 THEN
        bActive_Alarm_Level_L := TRUE;
    END_IF;
ELSIF rVoted_Level_NR >= (rAlarm_Level_NR_Low_L + rDeadband_Level_NR) THEN
    rTimer_Alarm_Level_L := 0.0;
    bActive_Alarm_Level_L := FALSE;
END_IF;

(* 4) Low-Low Narrow Range Level Trip (SCRAM / AFW) *)
IF rVoted_Level_NR <= rTrip_Level_NR_LowLow_LL THEN
    rTimer_Alarm_Level_LL := rTimer_Alarm_Level_LL + rScan_Period_Ts;
    IF rTimer_Alarm_Level_LL >= 0.100 THEN
        bActive_Alarm_Level_LL := TRUE;
        bDemand_RPS_Reactor_Trip := TRUE;
        bDemand_AFW_Motor_Pump_Start := TRUE;
        (* First-Out Latching *)
        IF dwFirstOutWord = 16#00000000 THEN
            dwFirstOutWord := 16#00000002; (* Bit 1: Level Low-Low First Out *)
        END_IF;
    END_IF;
ELSE
    rTimer_Alarm_Level_LL := 0.0;
END_IF;

(* 5) Steam Drum High-High Pressure Trip *)
IF rVoted_Press_SteamDrum >= rTrip_Press_SteamDrum_HH THEN
    rTimer_Alarm_Press_HH := rTimer_Alarm_Press_HH + rScan_Period_Ts;
    IF rTimer_Alarm_Press_HH >= 0.075 THEN
        bActive_Alarm_Press_HH := TRUE;
        bDemand_Turbine_Runback := TRUE;
        IF dwFirstOutWord = 16#00000000 THEN
            dwFirstOutWord := 16#00000004; (* Bit 2: Drum Pressure High-High First Out *)
        END_IF;
    END_IF;
ELSE
    rTimer_Alarm_Press_HH := 0.0;
END_IF;

(* 6) Steam Drum Low-Low Pressure Trip (Steam Line Break) *)
IF rVoted_Press_SteamDrum <= rTrip_Press_SteamDrum_LL THEN
    rTimer_Alarm_Press_LL := rTimer_Alarm_Press_LL + rScan_Period_Ts;
    IF rTimer_Alarm_Press_LL >= 0.100 THEN
        bActive_Alarm_Press_LL := TRUE;
        bDemand_MSIV_Fast_Closure := TRUE;
        bDemand_RPS_Reactor_Trip := TRUE;
        IF dwFirstOutWord = 16#00000000 THEN
            dwFirstOutWord := 16#00000008; (* Bit 3: Drum Pressure Low-Low First Out *)
        END_IF;
    END_IF;
ELSE
    rTimer_Alarm_Press_LL := 0.0;
END_IF;

(* 7) Steam / Feedwater Mass Flow Mismatch Alarm *)
IF ABS(rVoted_Flow_MainSteam - rVoted_Flow_Feedwater) >= rAlarm_Flow_Mismatch_Limit THEN
    rTimer_Alarm_FlowMismatch := rTimer_Alarm_FlowMismatch + rScan_Period_Ts;
    IF rTimer_Alarm_FlowMismatch >= 2.000 THEN (* 2 s qualification to allow swell transients *)
        bActive_Alarm_FlowMismatch := TRUE;
    END_IF;
ELSE
    rTimer_Alarm_FlowMismatch := 0.0;
    bActive_Alarm_FlowMismatch := FALSE;
END_IF;

(* 8) Steam Generator Tube Rupture (SGTR) Radiation Trip *)
IF (rRad_N16_SteamLine_ChA >= rTrip_N16_Radiation_SGTR_HH OR rRad_N16_SteamLine_ChB >= rTrip_N16_Radiation_SGTR_HH) THEN
    rTimer_Alarm_SGTR_Activity := rTimer_Alarm_SGTR_Activity + rScan_Period_Ts;
    IF rTimer_Alarm_SGTR_Activity >= 0.250 THEN
        bActive_Alarm_SGTR_Trip := TRUE;
        bDemand_MSIV_Fast_Closure := TRUE;
        bDemand_RPS_Reactor_Trip := TRUE;
        IF dwFirstOutWord = 16#00000000 THEN
            dwFirstOutWord := 16#00000010; (* Bit 4: SGTR First Out *)
        END_IF;
    END_IF;
ELSE
    rTimer_Alarm_SGTR_Activity := 0.0;
END_IF;

(* First-Out Latching for External Discrete RPS Scram and Turbine Trip *)
IF bDigital_RPS_Reactor_Scram AND dwFirstOutWord = 16#00000000 THEN
    dwFirstOutWord := 16#00000020; (* Bit 5: External RPS Scram First Out *)
END_IF;
IF bDigital_Turbine_Trip AND dwFirstOutWord = 16#00000000 THEN
    dwFirstOutWord := 16#00000040; (* Bit 6: Turbine Trip First Out *)
END_IF;
IF bDigital_MSIV_Closed_Limit AND dwFirstOutWord = 16#00000000 THEN
    dwFirstOutWord := 16#00000080; (* Bit 7: MSIV Closed First Out *)
END_IF;

(* Reset First-Out word when operator resets interlocks *)
IF bReset_Trip_Interlocks AND bAcknowledge_Alarms THEN
    dwFirstOutWord := 16#00000000;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * SECTION 5.2: MANUAL CONTROL OVERRIDE & HARD SAFETY INTERLOCK ENFORCEMENT
 * --------------------------------------------------------------------------------------------------------------------- *)
IF bSelect_Manual_Control_Mode THEN
    rCommand_MFRV_Position := rOperator_MFRV_Manual_Demand;
    rCommand_Bypass_Valve_Pos := rOperator_Bypass_Manual_Demand;
END_IF;

(* Overriding Class 1E Safety Trips (Hardware Overrides Software Manual Demands) *)
IF bDemand_MFRV_Isolation_P14 OR bActive_Alarm_Level_HH THEN
    rCommand_MFRV_Position := 0.0;
    rCommand_Bypass_Valve_Pos := 0.0;
END_IF;

IF bDemand_RPS_Reactor_Trip OR bDigital_RPS_Reactor_Scram THEN
    rCommand_MFRV_Position := 0.0;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * SECTION 5.3: ACTUATOR RATE LIMITING & SLEW-RATE DAMPING (5.0 %/s Max Slew)
 * --------------------------------------------------------------------------------------------------------------------- *)
IF (rCommand_MFRV_Position - rMFRV_Rate_Clamped_Prev) > rMax_Slew_Per_Cycle THEN
    rCommand_MFRV_Position := rMFRV_Rate_Clamped_Prev + rMax_Slew_Per_Cycle;
ELSIF (rCommand_MFRV_Position - rMFRV_Rate_Clamped_Prev) < -rMax_Slew_Per_Cycle THEN
    rCommand_MFRV_Position := rMFRV_Rate_Clamped_Prev - rMax_Slew_Per_Cycle;
END_IF;
rMFRV_Rate_Clamped_Prev := rCommand_MFRV_Position;

IF (rCommand_Bypass_Valve_Pos - rBypass_Rate_Clamped_Prev) > rMax_Slew_Per_Cycle THEN
    rCommand_Bypass_Valve_Pos := rBypass_Rate_Clamped_Prev + rMax_Slew_Per_Cycle;
ELSIF (rCommand_Bypass_Valve_Pos - rBypass_Rate_Clamped_Prev) < -rMax_Slew_Per_Cycle THEN
    rCommand_Bypass_Valve_Pos := rBypass_Rate_Clamped_Prev - rMax_Slew_Per_Cycle;
END_IF;
rBypass_Rate_Clamped_Prev := rCommand_Bypass_Valve_Pos;

(* Hard clamp outputs to valid hardware span [0.0 % .. 100.0 %] *)
IF rCommand_MFRV_Position > 100.0 THEN rCommand_MFRV_Position := 100.0; END_IF;
IF rCommand_MFRV_Position < 0.0 THEN rCommand_MFRV_Position := 0.0; END_IF;
IF rCommand_Bypass_Valve_Pos > 100.0 THEN rCommand_Bypass_Valve_Pos := 100.0; END_IF;
IF rCommand_Bypass_Valve_Pos < 0.0 THEN rCommand_Bypass_Valve_Pos := 0.0; END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * SECTION 5.4: BIT-PACKED TELEMETRY SYNTHESIS (DWORD STATUS & ALARM WORDS)
 * --------------------------------------------------------------------------------------------------------------------- *)
(* Synthesis of dwStatusWord1: System Operational State & Active Controls *)
dwStatusWord1 := 16#00000000;
IF bInitialized THEN dwStatusWord1 := dwStatusWord1 OR 16#00000001; END_IF;
IF bSelect_Manual_Control_Mode THEN dwStatusWord1 := dwStatusWord1 OR 16#00000002; END_IF;
IF eCurrentState = 4 THEN dwStatusWord1 := dwStatusWord1 OR 16#00000004; END_IF; (* MPC Full Power *)
IF eCurrentState = 3 THEN dwStatusWord1 := dwStatusWord1 OR 16#00000008; END_IF; (* Cascade 3-Element *)
IF eCurrentState = 1 OR eCurrentState = 2 THEN dwStatusWord1 := dwStatusWord1 OR 16#00000010; END_IF; (* Bypass Mode *)
IF eCurrentState = 2 THEN dwStatusWord1 := dwStatusWord1 OR 16#00000020; END_IF; (* Transferring *)
IF eCurrentState = 5 OR bDemand_Turbine_Runback THEN dwStatusWord1 := dwStatusWord1 OR 16#00000040; END_IF;
IF bDigital_MSIV_Closed_Limit THEN dwStatusWord1 := dwStatusWord1 OR 16#00000080; END_IF;
IF rCommand_AFW_Motor_Pump_Speed > 5.0 THEN dwStatusWord1 := dwStatusWord1 OR 16#00000100; END_IF;
IF rCommand_AFW_Turbine_Pump_Flow > 5.0 THEN dwStatusWord1 := dwStatusWord1 OR 16#00000200; END_IF;
IF rCommand_Blowdown_Valve_Pos > 0.5 THEN dwStatusWord1 := dwStatusWord1 OR 16#00000400; END_IF;
IF bDemand_RPS_Reactor_Trip THEN dwStatusWord1 := dwStatusWord1 OR 16#00000800; END_IF;
IF bDemand_MFRV_Isolation_P14 THEN dwStatusWord1 := dwStatusWord1 OR 16#00001000; END_IF;
IF eCurrentState = 7 THEN dwStatusWord1 := dwStatusWord1 OR 16#00002000; END_IF; (* SGTR *)
IF eCurrentState = 10 THEN dwStatusWord1 := dwStatusWord1 OR 16#00004000; END_IF; (* Dryout *)
IF eCurrentState = 13 THEN dwStatusWord1 := dwStatusWord1 OR 16#00008000; END_IF; (* Post-Scram *)
(* Pack state index into bits 16..19 *)
dwStatusWord1 := dwStatusWord1 OR SHL(INT_TO_DWORD(eCurrentState AND 16#000F), 16);

(* Synthesis of dwStatusWord2: 2oo3 TMR Triplet Health & Degradation Tiers *)
dwStatusWord2 := 16#00000000;
dwStatusWord2 := dwStatusWord2 OR (INT_TO_DWORD(nHealth_TMR_Level_NR AND 16#03));
IF bTMR_NR_Failed_ChA THEN dwStatusWord2 := dwStatusWord2 OR 16#00000004; END_IF;
IF bTMR_NR_Failed_ChB THEN dwStatusWord2 := dwStatusWord2 OR 16#00000008; END_IF;
IF bTMR_NR_Failed_ChC THEN dwStatusWord2 := dwStatusWord2 OR 16#00000010; END_IF;

dwStatusWord2 := dwStatusWord2 OR SHL(INT_TO_DWORD(nHealth_TMR_Level_WR AND 16#03), 5);
IF bTMR_WR_Failed_ChA THEN dwStatusWord2 := dwStatusWord2 OR 16#00000080; END_IF;
IF bTMR_WR_Failed_ChB THEN dwStatusWord2 := dwStatusWord2 OR 16#00000100; END_IF;
IF bTMR_WR_Failed_ChC THEN dwStatusWord2 := dwStatusWord2 OR 16#00000200; END_IF;

dwStatusWord2 := dwStatusWord2 OR SHL(INT_TO_DWORD(nHealth_TMR_Press_MS AND 16#03), 10);
IF bTMR_Press_Failed_ChA THEN dwStatusWord2 := dwStatusWord2 OR 16#00001000; END_IF;
IF bTMR_Press_Failed_ChB THEN dwStatusWord2 := dwStatusWord2 OR 16#00002000; END_IF;
IF bTMR_Press_Failed_ChC THEN dwStatusWord2 := dwStatusWord2 OR 16#00004000; END_IF;

dwStatusWord2 := dwStatusWord2 OR SHL(INT_TO_DWORD(nHealth_TMR_Flow_MS AND 16#03), 15);
IF bTMR_FlowMS_Failed_ChA THEN dwStatusWord2 := dwStatusWord2 OR 16#00020000; END_IF;
IF bTMR_FlowMS_Failed_ChB THEN dwStatusWord2 := dwStatusWord2 OR 16#00040000; END_IF;
IF bTMR_FlowMS_Failed_ChC THEN dwStatusWord2 := dwStatusWord2 OR 16#00080000; END_IF;

dwStatusWord2 := dwStatusWord2 OR SHL(INT_TO_DWORD(nHealth_TMR_Flow_FW AND 16#03), 20);
IF bTMR_FlowFW_Failed_ChA THEN dwStatusWord2 := dwStatusWord2 OR 16#00400000; END_IF;
IF bTMR_FlowFW_Failed_ChB THEN dwStatusWord2 := dwStatusWord2 OR 16#00800000; END_IF;
IF bTMR_FlowFW_Failed_ChC THEN dwStatusWord2 := dwStatusWord2 OR 16#01000000; END_IF;

IF (nHealth_TMR_Level_NR < 3 OR nHealth_TMR_Level_WR < 3 OR nHealth_TMR_Press_MS < 3 OR
    nHealth_TMR_Flow_MS < 3 OR nHealth_TMR_Flow_FW < 3) THEN
    dwStatusWord2 := dwStatusWord2 OR 16#02000000; (* Any TMR Degraded *)
END_IF;
IF (nHealth_TMR_Level_NR = 0 OR nHealth_TMR_Press_MS = 0) THEN
    dwStatusWord2 := dwStatusWord2 OR 16#04000000; (* Critical TMR Failed *)
END_IF;

(* Synthesis of dwAlarmWord1: ISA-18.2 Process Advisory & Limit Warnings *)
dwAlarmWord1 := 16#00000000;
IF bActive_Alarm_Level_H THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000001; END_IF;
IF bActive_Alarm_Level_L THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000002; END_IF;
IF rVoted_Press_SteamDrum >= rAlarm_Press_SteamDrum_H THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000004; END_IF;
IF rVoted_Press_SteamDrum <= rAlarm_Press_SteamDrum_L THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000008; END_IF;
IF bActive_Alarm_FlowMismatch THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000010; END_IF;
IF (rRad_N16_SteamLine_ChA >= rAlarm_N16_Radiation_SGTR_H OR rRad_N16_SteamLine_ChB >= rAlarm_N16_Radiation_SGTR_H) THEN
    dwAlarmWord1 := dwAlarmWord1 OR 16#00000020;
END_IF;
IF rMeasured_Level_Rate_mm_s >= rAlarm_Level_Rate_Of_Change_Lim THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000040; END_IF; (* Rapid Swell *)
IF rMeasured_Level_Rate_mm_s <= -rAlarm_Level_Rate_Of_Change_Lim THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000080; END_IF; (* Rapid Shrink *)
IF rTemp_ColdLeg_Primary >= 300.0 THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000100; END_IF;
IF ABS(rCommand_MFRV_Position - x_hat[7]) > 10.0 THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000200; END_IF;

(* Synthesis of dwAlarmWord2: Class 1E Process Safety Trips & Hard Scram Demands *)
dwAlarmWord2 := 16#00000000;
IF bActive_Alarm_Level_HH THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000001; END_IF;
IF bActive_Alarm_Level_LL THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000002; END_IF;
IF bActive_Alarm_Press_HH THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000004; END_IF;
IF bActive_Alarm_Press_LL THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000008; END_IF;
IF bActive_Alarm_SGTR_Trip THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000010; END_IF;
IF bDigital_RPS_Reactor_Scram THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000020; END_IF;
IF bDigital_Turbine_Trip THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000040; END_IF;
IF bDigital_SIAS_Active THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000080; END_IF;
IF nHealth_TMR_Level_NR = 0 THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000100; END_IF;

(* Real-Time Cyclic Execution Integrity Watchdog Pulse *)
bExecution_Valid_Tick := NOT bExecution_Valid_Tick;

END_FUNCTION_BLOCK
""")
    return "\n".join(code)

if __name__ == "__main__":
    s = get_phase5_alarms_telemetry()
    print("Phase 5 Alarms & Telemetry length:", len(s))
