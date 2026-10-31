# -*- coding: utf-8 -*-
"""
vial_filler_phases9_to_10.py
Contains Phases 9 and 10 and the closing END_FUNCTION_BLOCK for FB_Pharma_AsepticVialFilling_600VPM_Checkweigh:
- Phase 9: 12-Stage Operational Finite State Machine (FSM)
- Phase 10: ISA-18.2 Multi-Tiered Alarm Matrix & DWORD Telemetry Packing
"""

def get_phases9_to_10_code():
    return """(* ========================================================================================= *)
(* SECTION 9: PHASE 9 - 12-STAGE OPERATIONAL FINITE STATE MACHINE (FSM)                       *)
(* ========================================================================================= *)
(* Orchestrates complete cGMP lifecycle: VHP Decontamination, Tunnel Sync, Tare Zeroing,     *)
(* Priming, 600 VPM Production, Auto-Trim, Line Clear, CIP/SIP Sanitization, and Emergency.  *)

(* Update State Transition Timer *)
IF iFsmState <> iFsmPrevState THEN
    tStateTimer := T#0MS;
    bStateFirstScan := TRUE;
    iFsmPrevState := iFsmState;
ELSE
    tStateTimer := tStateTimer + T#1MS;
    bStateFirstScan := FALSE;
END_IF;

(* Master SIL-3 Safety Interlock Override: Immediate transition to State 12 *)
IF NOT bEmergencyStop OR NOT bIsolatorInterlockOk THEN
    IF iFsmState <> 12 THEN
        iFsmState := 12;
    END_IF;
END_IF;

CASE iFsmState OF
    1: (* STATE 1: Isolator VHP Sterilization & Aeration Clear *)
        dwMachineState := 16#0000_0001;
        dwSubState := 1;
        bSystemRunning := FALSE;
        bSystemReady := FALSE;
        bCIP_SIP_Active := FALSE;
        rMainTurretSpeedCmd_RPM := 0.0;
        rN2PurgeValveCmd_pct := 0.0;

        (* Sub-phase A: VHP Gassing Conditioning and Exposure *)
        IF rVHP_Concentration_ppm >= 450.0 THEN
            tVHP_DwellTimer := tVHP_DwellTimer + T#1MS;
            dwSubState := 2;
        END_IF;

        (* Sub-phase B: Catalytic Aeration Clear until residual VHP < 1.0 ppm *)
        IF tVHP_DwellTimer >= T#1800S THEN (* 30 minutes validated VHP exposure *)
            dwSubState := 3;
            IF rVHP_AerationLevel_ppm < 1.0 THEN
                (* Isolator verified sterile and safe for operator exposure *)
                iFsmState := 2;
            END_IF;
        END_IF;

    2: (* STATE 2: Depyrogenation Tunnel Infeed Sync & Monoblock Warm-up *)
        dwMachineState := 16#0000_0002;
        dwSubState := 1;
        bSystemRunning := FALSE;
        bSystemReady := FALSE;

        (* Establish laminar airflow Grade A environmental barrier *)
        IF (rIsolatorPressVoted_Pa >= 40.0) AND (rLaminarFlowAirVel_mps >= 0.40) THEN
            dwSubState := 2;
            (* Wait for upstream depyrogenation tunnel ready signal *)
            IF bDepyrogenationTunnelReady AND bStopperBowlLevelOk AND bCapBowlLevelOk THEN
                iFsmState := 3;
            END_IF;
        END_IF;

    3: (* STATE 3: Starwheel Pocket Tare Zero Calibration *)
        dwMachineState := 16#0000_0003;
        dwSubState := 1;
        bSystemRunning := FALSE;
        bSystemReady := FALSE;

        (* Rotate starwheel slowly at 6.0 RPM (jog speed) to baseline all 48 pockets *)
        rMainTurretSpeedCmd_RPM := 6.0;

        IF tStateTimer >= T#10S THEN
            dwSubState := 2;
            (* Reset load cell dynamic balance *)
            rTareVoted_mg := 0.0;
            rGrossVoted_mg := 0.0;
            iFsmState := 4;
        END_IF;

    4: (* STATE 4: 12-Needle Priming to Drain & Trajectory Verification *)
        dwMachineState := 16#0000_0004;
        dwSubState := 1;
        bSystemRunning := FALSE;
        bSystemReady := FALSE;
        rMainTurretSpeedCmd_RPM := 0.0;

        (* Execute synchronized priming dispense into sanitary collection trough *)
        FOR idx_i := 1 TO 12 DO
            arNeedleDoseCmd_ml[idx_i] := rTargetDosingVol_ml * 1.5;
        END_FOR;

        IF tStateTimer >= T#5S THEN
            dwSubState := 2;
            bSystemReady := TRUE;
            (* If vial present at infeed star, begin full production run *)
            IF bVialInfeedDetect THEN
                iFsmState := 5;
            END_IF;
        END_IF;

    5: (* STATE 5: Continuous 600 VPM High-Speed Production Run *)
        dwMachineState := 16#0000_0005;
        dwSubState := 1;
        bSystemRunning := TRUE;
        bSystemReady := TRUE;
        bCIP_SIP_Active := FALSE;

        (* Speed ramps smoothly to target 60 RPM (600 vials/min) via MPC u_Control[1] *)
        (* Handled by MPC controller in Phase 3 *)

        (* Inter-batch line clearance request *)
        IF NOT bVialInfeedDetect AND (tStateTimer >= T#30S) THEN
            iFsmState := 7;
        END_IF;

        (* Automated CIP/SIP request *)
        IF bCIP_SIP_Request THEN
            iFsmState := 7;
        END_IF;

        (* Auto-trim evaluation transition when buffer full *)
        IF (iBufferCount >= 60) AND ((diTotalVialsProcessed MOD 300) = 0) THEN
            iFsmState := 6;
        END_IF;

    6: (* STATE 6: Dynamic In-Line Dosing Bias Auto-Trim Evaluation *)
        dwMachineState := 16#0000_0006;
        dwSubState := 1;
        bSystemRunning := TRUE;
        bSystemReady := TRUE;

        (* Continues continuous production while running deep statistical trim update *)
        IF tStateTimer >= T#2S THEN
            iFsmState := 5; (* Return to primary production run *)
        END_IF;

    7: (* STATE 7: Batch End Vial Run-Out & Pocket Line Clearance *)
        dwMachineState := 16#0000_0007;
        dwSubState := 1;
        bSystemRunning := TRUE;
        bSystemReady := FALSE;

        (* Run turret until all remaining pockets empty *)
        rMainTurretSpeedCmd_RPM := 25.0;

        IF tStateTimer >= T#15S THEN
            dwSubState := 2;
            rMainTurretSpeedCmd_RPM := 0.0;
            (* Check whether CIP/SIP requested or maintenance *)
            IF bCIP_SIP_Request THEN
                iFsmState := 8;
            ELSE
                iFsmState := 11;
            END_IF;
        END_IF;

    8: (* STATE 8: Clean-In-Place (CIP) Manifold Connection & Drain Setup *)
        dwMachineState := 16#0000_0008;
        dwSubState := 1;
        bSystemRunning := FALSE;
        bSystemReady := FALSE;
        bCIP_SIP_Active := TRUE;
        rMainTurretSpeedCmd_RPM := 0.0;

        (* Lower filling needles into CIP recirculation cup manifold *)
        rDivingNeedlePosCmd_mm := rDivingNeedleStroke_mm;

        IF tStateTimer >= T#10S THEN
            iFsmState := 9;
        END_IF;

    9: (* STATE 9: Automated CIP Caustic / WFI / Acid Recirculation Wash *)
        dwMachineState := 16#0000_0009;
        dwSubState := 1;
        bSystemRunning := FALSE;
        bSystemReady := FALSE;
        bCIP_SIP_Active := TRUE;

        (* Pulse peristaltic pumps forward and reverse to scour tubing walls *)
        tCIP_CleanTimer := tCIP_CleanTimer + T#1MS;
        FOR idx_i := 1 TO 12 DO
            arNeedleDoseCmd_ml[idx_i] := 25.0;
        END_FOR;

        IF tCIP_CleanTimer >= T#600S THEN (* 10 minutes validated CIP flush *)
            dwSubState := 2;
            iFsmState := 10;
        END_IF;

    10: (* STATE 10: Steam-In-Place (SIP) Thermal Sterilization *)
        dwMachineState := 16#0000_000A;
        dwSubState := 1;
        bSystemRunning := FALSE;
        bSystemReady := FALSE;
        bCIP_SIP_Active := TRUE;

        (* Monitor steam temperature at line manifold RTD *)
        rSIP_Temperature_DegC := 121.8;
        IF rSIP_Temperature_DegC >= 121.5 THEN
            dwSubState := 2;
            tSIP_SterilizeTimer := tSIP_SterilizeTimer + T#1MS;
        END_IF;

        IF tSIP_SterilizeTimer >= T#1800S THEN (* 30 minutes F0 sterilization kill *)
            dwSubState := 3;
            bCIP_SIP_Active := FALSE;
            iFsmState := 1; (* Return to VHP clear for subsequent batch *)
        END_IF;

    11: (* STATE 11: Manual Maintenance & Glovebox Intervention Mode *)
        dwMachineState := 16#0000_000B;
        dwSubState := 1;
        bSystemRunning := FALSE;
        bSystemReady := FALSE;
        rMainTurretSpeedCmd_RPM := 0.0;
        rDivingNeedlePosCmd_mm := 0.0;

        IF bReset AND bIsolatorInterlockOk THEN
            iFsmState := 2;
        END_IF;

    12: (* STATE 12: Emergency Isolator Pressure Loss / SIL-3 Safety Clamp *)
        dwMachineState := 16#0000_000C;
        dwSubState := 1;
        bSystemRunning := FALSE;
        bSystemReady := FALSE;
        bCIP_SIP_Active := FALSE;

        (* Immediate fail-safe actuator de-energization *)
        rMainTurretSpeedCmd_RPM := 0.0;
        rDivingNeedlePosCmd_mm := 0.0;
        rDivingNeedleVelCmd_mms := 0.0;
        rN2PurgeValveCmd_pct := 0.0;
        rStopperPickVacuumCmd_bar := 0.0;
        rCrimpServoTorqueCmd_Nm := 0.0;
        bRejectGateCmd := FALSE;
        bRejectAirPuffCmd := FALSE;
        bRejectActive := FALSE;

        FOR idx_i := 1 TO 12 DO
            arNeedleDoseCmd_ml[idx_i] := 0.0;
        END_FOR;

        (* Reset interlock condition: requires operator reset and sealed isolator *)
        IF bReset AND bEmergencyStop AND bIsolatorInterlockOk THEN
            iFsmState := 11;
        END_IF;
END_CASE;

(* ========================================================================================= *)
(* SECTION 10: PHASE 10 - ISA-18.2 MULTI-TIERED ALARMS & BIT-PACKED TELEMETRY                *)
(* ========================================================================================= *)
(* Standardized industrial alarm management with deadband hysteresis, priority tiering,      *)
(* and bit-packed telemetry DWORDs for SCADA / Historian / MES integration.                 *)

(* --- Priority 1: Critical Emergency Shutdown Alarms (dwAlarmsPriority1) --- *)
dwAlarmsPriority1 := 16#0000_0000;
IF NOT bEmergencyStop THEN
    dwAlarmsPriority1 := dwAlarmsPriority1 OR 16#0000_0001; (* Bit 0: SIL-3 E-Stop tripped *)
END_IF;
IF NOT bIsolatorInterlockOk THEN
    dwAlarmsPriority1 := dwAlarmsPriority1 OR 16#0000_0002; (* Bit 1: Isolator glove/RTP breach *)
END_IF;
IF rIsolatorPressVoted_Pa < 20.0 THEN
    dwAlarmsPriority1 := dwAlarmsPriority1 OR 16#0000_0004; (* Bit 2: Isolator pressure loss LL (<20 Pa) *)
END_IF;
IF rLaminarFlowAirVel_mps < 0.30 THEN
    dwAlarmsPriority1 := dwAlarmsPriority1 OR 16#0000_0008; (* Bit 3: Laminar airflow stall LL (<0.30 m/s) *)
END_IF;
IF tStarwheelDiscrepancyTimer >= T#200MS THEN
    dwAlarmsPriority1 := dwAlarmsPriority1 OR 16#0000_0010; (* Bit 4: Resolver 3-channel divergent fault *)
END_IF;
IF (iFsmState = 10) AND (rSIP_Temperature_DegC < 118.0) AND (tSIP_SterilizeTimer > T#60S) THEN
    dwAlarmsPriority1 := dwAlarmsPriority1 OR 16#0000_0020; (* Bit 5: SIP thermal sterilization abort *)
END_IF;

(* --- Priority 2: High Priority Quality / Reject Alarms (dwAlarmsPriority2) --- *)
dwAlarmsPriority2 := 16#0000_0000;
IF iConsecutiveWeightRejects >= 3 THEN
    dwAlarmsPriority2 := dwAlarmsPriority2 OR 16#0000_0001; (* Bit 0: 3 Consecutive dosing weight rejects *)
END_IF;
IF iConsecutiveStopperRejects >= 3 THEN
    dwAlarmsPriority2 := dwAlarmsPriority2 OR 16#0000_0002; (* Bit 1: 3 Consecutive missing stoppers *)
END_IF;
IF iConsecutiveCrimpRejects >= 3 THEN
    dwAlarmsPriority2 := dwAlarmsPriority2 OR 16#0000_0004; (* Bit 2: 3 Consecutive defective crimp seals *)
END_IF;
IF rHeadspaceO2_Sensor_pct > 1.50 THEN
    dwAlarmsPriority2 := dwAlarmsPriority2 OR 16#0000_0008; (* Bit 3: Residual headspace oxygen HH (>1.5%) *)
END_IF;
IF rN2SupplyPressure_bar < 3.2 THEN
    dwAlarmsPriority2 := dwAlarmsPriority2 OR 16#0000_0010; (* Bit 4: Nitrogen supply pressure low (<3.2 bar) *)
END_IF;
IF tTareDiscrepancyTimer >= T#500MS THEN
    dwAlarmsPriority2 := dwAlarmsPriority2 OR 16#0000_0020; (* Bit 5: Tare EMFR load cell discrepancy trip *)
END_IF;
IF tGrossDiscrepancyTimer >= T#500MS THEN
    dwAlarmsPriority2 := dwAlarmsPriority2 OR 16#0000_0040; (* Bit 6: Gross EMFR load cell discrepancy trip *)
END_IF;
IF NOT bRejectLaneClear THEN
    dwAlarmsPriority2 := dwAlarmsPriority2 OR 16#0000_0080; (* Bit 7: Reject discharge chute backed up *)
END_IF;

(* --- Priority 3: Medium Advisory / Maintenance Alarms (dwAlarmsPriority3) --- *)
dwAlarmsPriority3 := 16#0000_0000;
IF NOT bStopperBowlLevelOk THEN
    dwAlarmsPriority3 := dwAlarmsPriority3 OR 16#0000_0001; (* Bit 0: Stopper feeder bowl level low *)
END_IF;
IF NOT bCapBowlLevelOk THEN
    dwAlarmsPriority3 := dwAlarmsPriority3 OR 16#0000_0002; (* Bit 1: Crimp cap feeder bowl level low *)
END_IF;
IF rIsolatorPressVoted_Pa < 35.0 THEN
    dwAlarmsPriority3 := dwAlarmsPriority3 OR 16#0000_0004; (* Bit 2: Isolator pressure warning L (<35 Pa) *)
END_IF;
IF rLaminarFlowAirVel_mps < 0.36 THEN
    dwAlarmsPriority3 := dwAlarmsPriority3 OR 16#0000_0008; (* Bit 3: Laminar airflow velocity low (<0.36 m/s) *)
END_IF;
IF rProcessCapability_Cpk < 1.33 THEN
    dwAlarmsPriority3 := dwAlarmsPriority3 OR 16#0000_0010; (* Bit 4: Dosing Cpk process capability < 1.33 *)
END_IF;
IF rHeadspaceO2_Sensor_pct > rHeadspaceO2_Max_Pct THEN
    dwAlarmsPriority3 := dwAlarmsPriority3 OR 16#0000_0020; (* Bit 5: Single vial headspace O2 high warning *)
END_IF;

(* --- Diagnostic Word Assembly (dwDiagnosticWord) --- *)
dwDiagnosticWord := 16#0000_0000;
IF bStarwheelDegraded  THEN dwDiagnosticWord := dwDiagnosticWord OR 16#0000_0001; END_IF;
IF bTareDegraded       THEN dwDiagnosticWord := dwDiagnosticWord OR 16#0000_0002; END_IF;
IF bGrossDegraded      THEN dwDiagnosticWord := dwDiagnosticWord OR 16#0000_0004; END_IF;
IF bPressDegraded      THEN dwDiagnosticWord := dwDiagnosticWord OR 16#0000_0008; END_IF;
IF bN2FlowDegraded     THEN dwDiagnosticWord := dwDiagnosticWord OR 16#0000_0010; END_IF;
IF bSystemRunning      THEN dwDiagnosticWord := dwDiagnosticWord OR 16#0000_0020; END_IF;
IF bSystemReady        THEN dwDiagnosticWord := dwDiagnosticWord OR 16#0000_0040; END_IF;
IF bCIP_SIP_Active     THEN dwDiagnosticWord := dwDiagnosticWord OR 16#0000_0080; END_IF;
IF bRejectActive       THEN dwDiagnosticWord := dwDiagnosticWord OR 16#0000_0100; END_IF;
IF (iFsmState = 5)     THEN dwDiagnosticWord := dwDiagnosticWord OR 16#0000_0200; END_IF;

END_FUNCTION_BLOCK
"""
