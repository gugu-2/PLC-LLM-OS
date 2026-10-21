# Section 6: Multi-Stage FSM, Degradation, Alarm Encoding & Function Block Termination
def get_sec6_fsm_alarms():
    return """(* ========================================================================================= *)
(* 8.0 MULTI-STAGE FINITE STATE MACHINE (FSM) GOVERNOR                                      *)
(* ========================================================================================= *)
(* Deterministic state machine governing sequential warm-up, calibration, sparge purging,    *)
(* coarse beryllium exposure, fine hydrogen trimming, fission gas stripping, and MPC.       *)

(* Detect state transitions *)
IF iState <> iPreviousState THEN
    bStateFirstScan := TRUE;
    iPreviousState := iState;
ELSE
    bStateFirstScan := FALSE;
END_IF;

CASE iState OF
    0: (* FSM_COLD_INHIBIT: System Standby / De-energized Safe Inhibit *)
        bSystemReady             := FALSE;
        rBeRodPositionCmd_mm     := 0.0;
        rH2MassFlowCmd_sccm      := 0.0;
        rHeStrippingFlowCmd_sccm := 0.0;
        rCycloneThrottleCmd_pct  := 0.0;
        rTraceHeatingTarget_kW   := 0.0;
        bBeRodFastEjectionActive := FALSE;
        bH2SupplyIsolated        := TRUE;
        bDegradedModeActive      := FALSE;

        IF bMasterSystemEnable AND (NOT bEmergencyTripActive) THEN
            iState := 10; (* Transition to Preheating *)
        END_IF;

    10: (* FSM_ISOTHERMAL_PREHEAT: Salt Bypass Pre-Warming to 650°C Liquidus Margin *)
        bSystemReady             := FALSE;
        rBeRodPositionCmd_mm     := 0.0;
        rH2MassFlowCmd_sccm      := 0.0;
        rHeStrippingFlowCmd_sccm := 50.0; (* Slight inert helium trickle *)
        rCycloneThrottleCmd_pct  := 15.0;
        rTraceHeatingTarget_kW   := 55.0; (* Engage bypass line trace heaters *)
        bH2SupplyIsolated        := TRUE;

        (* Evaluate isothermal temperature stabilization dwell *)
        tPreheatDwellTimer(IN := (rBypassLoopTemp_degC >= 640.0) AND (rVotedSaltCoreTemp_degC >= 640.0),
                           PT := T#30S);
        
        IF tPreheatDwellTimer.Q THEN
            tPreheatDwellTimer(IN := FALSE);
            iState := 20; (* Transition to Sensor Health Alignment *)
        END_IF;

        IF NOT bMasterSystemEnable THEN iState := 0; END_IF;

    20: (* FSM_TMR_CALIBRATION_CHECK: 2oo3 Sensor Health & EIS Baseline Alignment *)
        bSystemReady             := FALSE;
        rBeRodPositionCmd_mm     := 0.0;
        rH2MassFlowCmd_sccm      := 0.0;
        rHeStrippingFlowCmd_sccm := 100.0;
        rCycloneThrottleCmd_pct  := 25.0;
        rTraceHeatingTarget_kW   := 35.0; (* Maintain thermal equilibrium *)
        bH2SupplyIsolated        := TRUE;

        (* Dwell timer to verify stable open-circuit electrochemical potential *)
        tCalibrationDwellTimer(IN := (iPot_Healthy_Count >= 2) AND (iTemp_Healthy_Count >= 2),
                               PT := T#20S);

        IF tCalibrationDwellTimer.Q THEN
            tCalibrationDwellTimer(IN := FALSE);
            iState := 30; (* Transition to Inert Gas Purging *)
        END_IF;

        IF NOT bMasterSystemEnable THEN iState := 0; END_IF;

    30: (* FSM_INERT_PURGE_BLANKETING: Helium Sweep Gas Purge of Spargers & Separator *)
        bSystemReady             := FALSE;
        rBeRodPositionCmd_mm     := 0.0;
        rH2MassFlowCmd_sccm      := 0.0;
        rHeStrippingFlowCmd_sccm := 1200.0; (* High flow inert helium purge *)
        rCycloneThrottleCmd_pct  := 45.0;
        rTraceHeatingTarget_kW   := 30.0;
        bH2SupplyIsolated        := TRUE;

        (* Verify sparger line pressure integrity and sweep duration *)
        tInertPurgeDwellTimer(IN := (rSpargerInletPress_A_bar >= 1.80), PT := T#25S);

        IF tInertPurgeDwellTimer.Q THEN
            tInertPurgeDwellTimer(IN := FALSE);
            iState := 40; (* Transition to Redox Baseline Acquisition *)
        END_IF;

        IF NOT bMasterSystemEnable THEN iState := 0; END_IF;

    40: (* FSM_REDOX_BASELINE_ACQUISITION: Unperturbed Fuel Salt Potential Evaluation *)
        bSystemReady             := FALSE;
        rBeRodPositionCmd_mm     := 0.0;
        rH2MassFlowCmd_sccm      := 0.0;
        rHeStrippingFlowCmd_sccm := 800.0;
        rCycloneThrottleCmd_pct  := 45.0;
        rTraceHeatingTarget_kW   := 25.0;
        bH2SupplyIsolated        := TRUE;

        tBaselineAcqTimer(IN := TRUE, PT := T#15S);

        IF tBaselineAcqTimer.Q THEN
            tBaselineAcqTimer(IN := FALSE);
            (* Decision branching based on acquired U4+/U3+ redox ratio *)
            IF rCalculatedU4U3Ratio > 125.0 THEN
                iState := 50; (* Fuel salt heavily oxidizing: Engaged Coarse Beryllium *)
            ELSIF rCalculatedU4U3Ratio > 105.0 THEN
                iState := 60; (* Moderate oxidation: Fine Hydrogen sparging trim *)
            ELSE
                iState := 70; (* Salt already in optimal redox envelope: Start bubble stripping *)
            END_IF;
        END_IF;

        IF NOT bMasterSystemEnable THEN iState := 0; END_IF;

    50: (* FSM_COARSE_BE_REDUCTION: Metallic Beryllium Immersion Rod Coarse Reduction *)
        bSystemReady             := FALSE;
        bH2SupplyIsolated        := TRUE;
        rH2MassFlowCmd_sccm      := 0.0;
        rHeStrippingFlowCmd_sccm := 1000.0;
        rCycloneThrottleCmd_pct  := 55.0;
        rTraceHeatingTarget_kW   := 25.0;

        (* Drive Beryllium rod to calculated immersion depth with rate-limiting *)
        rBeRodPositionCmd_mm := rBeImmersionTarget_mm;
        IF rBeRodPositionCmd_mm > 180.0 THEN rBeRodPositionCmd_mm := 180.0; END_IF;

        (* When redox potential approaches target envelope (ratio <= 110.0), transition to fine trim *)
        IF rCalculatedU4U3Ratio <= 110.0 THEN
            iState := 60; (* Transition to Fine Hydrogen Sparging Trim *)
        END_IF;

        IF NOT bMasterSystemEnable THEN iState := 0; END_IF;

    60: (* FSM_FINE_H2_SPARGING_TRIM: Active Hydrogen / Helium Reductant Gas Sparging *)
        bSystemReady             := FALSE;
        bH2SupplyIsolated        := FALSE; (* Open hydrogen supply permissive *)
        
        (* Retract Beryllium rod to shallow standby depth *)
        rBeRodPositionCmd_mm := 10.0;
        rH2MassFlowCmd_sccm  := rH2FlowTarget_sccm;
        IF rH2MassFlowCmd_sccm > 600.0 THEN rH2MassFlowCmd_sccm := 600.0; END_IF;
        
        rHeStrippingFlowCmd_sccm := 1500.0;
        rCycloneThrottleCmd_pct  := 65.0;
        rTraceHeatingTarget_kW   := 25.0;

        (* When error is within narrow stabilization band, advance to bubble stripping *)
        IF (ABS(rRedoxError) <= 0.12) AND (rCalculatedU4U3Ratio >= 70.0) AND (rCalculatedU4U3Ratio <= 110.0) THEN
            iState := 70; (* Transition to Bubble Stripping & Extraction *)
        END_IF;

        IF NOT bMasterSystemEnable THEN iState := 0; END_IF;

    70: (* FSM_BUBBLE_STRIPPING_EXTRACTION: Noble Gas (Xe/Kr) Extraction Alignment *)
        bSystemReady             := FALSE;
        bH2SupplyIsolated        := FALSE;
        rBeRodPositionCmd_mm     := u_ctrl[1];
        rH2MassFlowCmd_sccm      := u_ctrl[2];
        rHeStrippingFlowCmd_sccm := u_ctrl[3];
        rCycloneThrottleCmd_pct  := u_ctrl[4];
        rTraceHeatingTarget_kW   := 25.0;

        (* Verify bubble stripping efficiency and low gas void carryunder *)
        IF (rXeExtractionEfficiency_pct >= 92.0) AND (rCalculatedVoidFraction_pct <= 0.075) THEN
            iState := 80; (* Transition to Fully Autonomous Closed-Loop MPC *)
        END_IF;

        IF NOT bMasterSystemEnable THEN iState := 0; END_IF;

    80: (* FSM_CLOSED_LOOP_MPC_CORE_STABLE: Full Multivariable Cyber-Physical Regulation *)
        bSystemReady             := TRUE;
        bDegradedModeActive      := FALSE;
        bH2SupplyIsolated        := FALSE;

        (* Full actuation authority assigned to MPC optimization engine *)
        rBeRodPositionCmd_mm     := u_ctrl[1];
        rH2MassFlowCmd_sccm      := u_ctrl[2];
        rHeStrippingFlowCmd_sccm := u_ctrl[3];
        rCycloneThrottleCmd_pct  := u_ctrl[4];
        rTraceHeatingTarget_kW   := 25.0;

        (* Degraded condition supervision: drop to State 90 if critical redundancy is lost *)
        IF (iPot_Healthy_Count < 2) OR (iTemp_Healthy_Count < 2) THEN
            iState := 90; (* Fallback to Degraded Mode *)
        END_IF;

        IF NOT bMasterSystemEnable THEN iState := 0; END_IF;

    90: (* FSM_GRACEFUL_DEGRADATION: Fault-Tolerant Degraded Control Governor *)
        bSystemReady             := TRUE;
        bDegradedModeActive      := TRUE;

        (* Conservative Actuator Clamps in Degraded Mode *)
        rBeRodPositionCmd_mm     := 15.0;   (* Fixed conservative immersion *)
        rH2MassFlowCmd_sccm      := 120.0;  (* Low-rate continuous hydrogen trimming *)
        rHeStrippingFlowCmd_sccm := 2500.0; (* Elevated helium stripping to ensure gas sweep *)
        rCycloneThrottleCmd_pct  := 75.0;   (* Elevated separator exhaust throttle *)
        rTraceHeatingTarget_kW   := 28.0;

        (* Self-healing recovery: If 2oo3 health is fully restored, resume closed-loop MPC *)
        IF (iPot_Healthy_Count >= 2) AND (iTemp_Healthy_Count >= 2) AND (NOT bEmergencyTripActive) THEN
            iState := 80;
        END_IF;

        IF NOT bMasterSystemEnable THEN iState := 0; END_IF;

    100: (* FSM_EMERGENCY_SCRAM_DRAIN: Hardwired SIL-3 Safety Lockdown & Salt Isolation *)
        bSystemReady             := FALSE;
        bEmergencyTripActive     := TRUE;
        bBeRodFastEjectionActive := TRUE;
        rBeRodPositionCmd_mm     := 0.0;    (* Retract Beryllium rod fully *)
        bH2SupplyIsolated        := TRUE;
        rH2MassFlowCmd_sccm      := 0.0;    (* Isolate hydrogen supply lines immediately *)
        rHeStrippingFlowCmd_sccm := 150.0;  (* Minimum sweep to prevent salt back-siphon *)
        rCycloneThrottleCmd_pct  := 100.0;  (* Max open to vent separator *)
        rTraceHeatingTarget_kW   := 0.0;

        (* Latch safety lockdown: Requires clearing trip conditions and toggling master enable *)
        IF (NOT bEmergencyTripActive) AND (NOT bMasterSystemEnable) THEN
            iState := 0; (* Return to Cold Inhibit *)
        END_IF;

END_CASE;


(* ========================================================================================= *)
(* 9.0 GRACEFUL DEGRADATION, SENSOR FAULT MITIGATION & ACTUATOR DERATING                     *)
(* ========================================================================================= *)
(* Real-time fault tolerance: dynamic redundancy reconfiguration and actuator derating.     *)

(* Potentiometry degradation management *)
IF iPot_Healthy_Count = 2 THEN
    (* Derate Beryllium actuator speed by 25% *)
    delta_u_max[1] := 1.875;
ELSIF iPot_Healthy_Count = 1 THEN
    (* Severe degradation: Derate Beryllium speed by 60%, bias H2 flow slightly *)
    delta_u_max[1] := 1.000;
    delta_u_max[2] := 15.0;
ELSE
    (* Loss of all potentiometry: Freeze Beryllium rod at current position, isolate H2 *)
    rBeRodPositionCmd_mm := 0.0;
    bH2SupplyIsolated    := TRUE;
    rH2MassFlowCmd_sccm  := 0.0;
END_IF;

(* Off-gas radiation sensor degradation *)
IF iXe_Healthy_Count < 2 THEN
    dwWarningWord := dwWarningWord OR 16#0000_0200; (* Warning: Off-gas radiation monitor degraded *)
    (* Fix cyclone throttle to conservative baseline (70%) *)
    IF iState = 80 THEN
        rCycloneThrottleCmd_pct := 70.0;
    END_IF;
END_IF;

(* High leached chromium degradation bias *)
IF rDissolvedChromium_ppm > 85.0 THEN
    dwWarningWord := dwWarningWord OR 16#0000_0400; (* Warning: High leached chromium in salt *)
    (* Automatically bias target redox ratio 10% more reducing to protect structural alloy *)
    IF rRedoxRatioTarget_mol_mol > 60.0 THEN
        rRedoxRatioTarget_mol_mol := rRedoxRatioTarget_mol_mol - 0.050;
    END_IF;
END_IF;


(* ========================================================================================= *)
(* 10.0 DETERMINISTIC BIT-PACKED STATUS WORDS & HIERARCHICAL ALARM ENCODING                  *)
(* ========================================================================================= *)
(* Assembles 32-bit status, warning, critical alarm, and FSM words for cyber-physical SCADA. *)

(* --- 10.1 System Status Word (dwSystemStatusWord) --- *)
dwSystemStatusWord := 16#0000_0000;
IF bMasterSystemEnable THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0001; END_IF;
IF bSystemReady THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0002; END_IF;
IF iPot_Healthy_Count = 3 THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0004; END_IF;
IF iTemp_Healthy_Count = 3 THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0008; END_IF;
IF (NOT bH2SupplyIsolated) THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0010; END_IF;
IF (rBeRodPositionCmd_mm > 0.5) THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0020; END_IF;
IF (rXeExtractionEfficiency_pct >= 90.0) THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0040; END_IF;
IF (rCalculatedVoidFraction_pct <= 0.080) THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0080; END_IF;
IF (rCorrosionRate_um_yr <= 10.0) THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0100; END_IF;
IF bDegradedModeActive THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0200; END_IF;
IF bMatricesInitialized THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0400; END_IF;
IF bSafetyFreezePlugHealthy THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0800; END_IF;

(* --- 10.2 FSM State Word (dwFSMStateWord) --- *)
dwFSMStateWord := INT_TO_DWORD(iState);

(* Track cumulative operating hours (T_s = 0.200 s) *)
rTotalOperatingHours := rTotalOperatingHours + (tSampleTaskInterval_s / 3600.0);

END_FUNCTION_BLOCK
"""

if __name__ == "__main__":
    s = get_sec6_fsm_alarms()
    print("Section 6 Length:", len(s))
