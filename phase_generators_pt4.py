# phase_generators_pt4.py
# Phase 7: ISA-18.2 Process Alarms, Telemetry Bit-Packing & Actuator Mapping

def generate_phase7():
    return """
(* ==================================================================================================== *)
(* PHASE 7: ISA-18.2 MULTI-TIER PROCESS ALARMS, DEAD-BAND HYSTERESIS & 32-BIT TELEMETRY                *)
(* Alarm Tier Architecture:                                                                             *)
(*   Tier 1 (HH / LL Trips): Immediate Actuator Dump, FSM State 13 Safety Depressurization.             *)
(*   Tier 2 (H / L Warnings): Continuous Operator Advisory with Deadband Clearance Hysteresis.          *)
(* Bit-Packed 32-Bit Telemetry DWORDs:                                                                  *)
(*   dwStatusWord1: Primary Operating Flags and Safety Gate Interlocks                                  *)
(*   dwStatusWord2: Subsystems, Valve Gates, and Servo Drive Readiness Registers                         *)
(*   dwAlarmWord1 : Critical Emergency Trips and First-Out Trigger Latches                              *)
(*   dwAlarmWord2 : Process Limit Warnings, Sensor Discrepancies, and Quality Out-of-Spec Flags         *)
(*   dwFirstOutWord: Root Cause First-Out Alarm Register                                                *)
(* ==================================================================================================== *)

(* 1. ISA-18.2 Process Warning Supervision with Clearance Deadband Hysteresis *)
(* Nozzle High Pressure Warning *)
IF rVoted_PT101_bar >= rSp_NozzlePress_H_bar THEN
    bAlarmWarn_NozzlePressH := TRUE;
ELSIF rVoted_PT101_bar <= (rSp_NozzlePress_H_bar - rSp_NozzlePress_H_Deadband_bar) THEN
    bAlarmWarn_NozzlePressH := FALSE;
END_IF;

(* Cavity 1 High Pressure Warning *)
IF rVoted_PT201_bar >= rSp_CavityPress_H_bar THEN
    bAlarmWarn_CavityPressH := TRUE;
ELSIF rVoted_PT201_bar <= (rSp_CavityPress_H_bar - rSp_CavityPress_H_Deadband_bar) THEN
    bAlarmWarn_CavityPressH := FALSE;
END_IF;

(* Tie-Bar Asymmetry Imbalance Warning *)
IF rMaxTieBarDelta_kN >= rSp_TieBarImbalance_H_kN THEN
    bAlarmWarn_TieBarImbalanceH := TRUE;
ELSIF rMaxTieBarDelta_kN <= (rSp_TieBarImbalance_H_kN - 50.0) THEN
    bAlarmWarn_TieBarImbalanceH := FALSE;
END_IF;

(* Mold Parting Line Separation Deflection Warning *)
IF rMoldSeparation_um >= rSp_PartingSeparation_H_um THEN
    bAlarmWarn_PartingSeparationH := TRUE;
ELSIF rMoldSeparation_um <= (rSp_PartingSeparation_H_um - 2.5) THEN
    bAlarmWarn_PartingSeparationH := FALSE;
END_IF;

(* Mold Temperature High/Low Warnings *)
IF rVoted_TT501_degC >= rSp_MoldTemp_H_degC THEN
    bAlarmWarn_MoldTempH := TRUE;
ELSIF rVoted_TT501_degC <= (rSp_MoldTemp_H_degC - 3.0) THEN
    bAlarmWarn_MoldTempH := FALSE;
END_IF;

IF rVoted_TT501_degC <= rSp_MoldTemp_L_degC THEN
    bAlarmWarn_MoldTempL := TRUE;
ELSIF rVoted_TT501_degC >= (rSp_MoldTemp_L_degC + 3.0) THEN
    bAlarmWarn_MoldTempL := FALSE;
END_IF;

(* Screw Minimum Cushion Warning & Trip *)
IF (nFsmState = 6) AND (rVoted_ST301_mm <= rSp_Cushion_L_mm) THEN
    bAlarmWarn_CushionL := TRUE;
    IF rVoted_ST301_mm <= rSp_Cushion_LL_mm THEN
        bAlarmLatched_CushionLL := TRUE;
        nFsmNextState := 13;
        IF nFirstOutAlarmCode = 0 THEN
            nFirstOutAlarmCode := 107; (* Cushion LL Bottoming Out *)
        END_IF;
    END_IF;
ELSIF rVoted_ST301_mm > (rSp_Cushion_L_mm + 1.5) THEN
    bAlarmWarn_CushionL := FALSE;
END_IF;

(* Gate Freeze Delay Warning *)
IF (nFsmState = 6) AND (rPackStageStopwatch_sec >= rSp_GateFreezeTimeout_sec) AND
   (x_state[7] < (rGateHalfThickness_um * 0.90)) THEN
    bAlarmWarn_GateFreezeDelay := TRUE;
ELSE
    bAlarmWarn_GateFreezeDelay := FALSE;
END_IF;

(* Clamping Tonnage High-High & Low-Low Supervision during Closed Mold *)
IF (nFsmState >= 3 AND nFsmState <= 9) THEN
    IF rVoted_WT401_kN >= rSp_Tonnage_HH_kN THEN
        bAlarmLatched_ClampTonnageHH := TRUE;
        nFsmNextState := 13;
        IF nFirstOutAlarmCode = 0 THEN
            nFirstOutAlarmCode := 108; (* Clamp Tonnage HH *)
        END_IF;
    ELSIF rVoted_WT401_kN <= rSp_Tonnage_LL_kN THEN
        bAlarmLatched_ClampTonnageLL := TRUE;
        nFsmNextState := 13;
        IF nFirstOutAlarmCode = 0 THEN
            nFirstOutAlarmCode := 109; (* Clamp Tonnage Loss LL *)
        END_IF;
    END_IF;
END_IF;

(* 2. Bit-Packing of 32-Bit Telemetry Registers *)
(* dwStatusWord1: Primary Operating Status *)
dwStatusWord1 := 16#00000000;
IF (nFsmState = 0)                   THEN dwStatusWord1 := dwStatusWord1 OR 16#00000001; END_IF; (* Bit 0: Machine Idle *)
IF bSafetyGateClosed                 THEN dwStatusWord1 := dwStatusWord1 OR 16#00000002; END_IF; (* Bit 1: Front Safety Gate Closed *)
IF bRearSafetyGateClosed             THEN dwStatusWord1 := dwStatusWord1 OR 16#00000004; END_IF; (* Bit 2: Rear Safety Gate Closed *)
IF bEmergencyStop                    THEN dwStatusWord1 := dwStatusWord1 OR 16#00000008; END_IF; (* Bit 3: E-Stop Healthy *)
IF (nFsmState = 2)                   THEN dwStatusWord1 := dwStatusWord1 OR 16#00000010; END_IF; (* Bit 4: Tonnage Building *)
IF (nFsmState >= 3 AND nFsmState <= 9)THEN dwStatusWord1 := dwStatusWord1 OR 16#00000020; END_IF; (* Bit 5: Mold Locked Up *)
IF (nFsmState = 3)                   THEN dwStatusWord1 := dwStatusWord1 OR 16#00000040; END_IF; (* Bit 6: Carriage Touch *)
IF (nFsmState = 4)                   THEN dwStatusWord1 := dwStatusWord1 OR 16#00000080; END_IF; (* Bit 7: Fast Injection Fill *)
IF bVP_TransferTriggered             THEN dwStatusWord1 := dwStatusWord1 OR 16#00000100; END_IF; (* Bit 8: V/P Switch Active *)
IF (nFsmState = 6)                   THEN dwStatusWord1 := dwStatusWord1 OR 16#00000200; END_IF; (* Bit 9: Multi-Stage Pack *)
IF bGateFreezeOffAchieved            THEN dwStatusWord1 := dwStatusWord1 OR 16#00000400; END_IF; (* Bit 10: Gate Freeze Off *)
IF (nFsmState = 8)                   THEN dwStatusWord1 := dwStatusWord1 OR 16#00000800; END_IF; (* Bit 11: Plasticizing Recovery *)
IF (nFsmState = 9)                   THEN dwStatusWord1 := dwStatusWord1 OR 16#00001000; END_IF; (* Bit 12: Melt Suckback *)
IF (nFsmState = 11)                  THEN dwStatusWord1 := dwStatusWord1 OR 16#00002000; END_IF; (* Bit 13: Mold Opening *)
IF (nFsmState = 12)                  THEN dwStatusWord1 := dwStatusWord1 OR 16#00004000; END_IF; (* Bit 14: Ejection Active *)
IF (nFsmState = 13)                  THEN dwStatusWord1 := dwStatusWord1 OR 16#00008000; END_IF; (* Bit 15: Emergency Trip *)
IF bAutoCycleStart                   THEN dwStatusWord1 := dwStatusWord1 OR 16#00010000; END_IF; (* Bit 16: Auto Mode Enabled *)
IF bPartDropVerified                 THEN dwStatusWord1 := dwStatusWord1 OR 16#00020000; END_IF; (* Bit 17: Part Demolded OK *)
IF bCycleCompletePulse               THEN dwStatusWord1 := dwStatusWord1 OR 16#00040000; END_IF; (* Bit 18: Shot Complete Pulse *)
IF (bDegraded_PT101 OR bDegraded_PT201 OR bDegraded_ST301 OR bDegraded_WT401 OR bDegraded_TT501) THEN
    dwStatusWord1 := dwStatusWord1 OR 16#00080000;                                             (* Bit 19: Degraded Sensor Mode *)
END_IF;

(* dwStatusWord2: Subsystem Readiness & Valve Gate Status *)
dwStatusWord2 := 16#00000000;
IF bCmd_HotRunnerValveGatesOpen      THEN dwStatusWord2 := dwStatusWord2 OR 16#00000001; END_IF; (* Bit 0: Valve Gates Open *)
IF bHydraulicPumpsReady              THEN dwStatusWord2 := dwStatusWord2 OR 16#00000002; END_IF; (* Bit 1: Hydraulic Core-Pull Ready *)
IF bElectricServosReady              THEN dwStatusWord2 := dwStatusWord2 OR 16#00000004; END_IF; (* Bit 2: Electric Servos Ready *)
IF (nHoldingProfileSubStage = 1)     THEN dwStatusWord2 := dwStatusWord2 OR 16#00000010; END_IF; (* Bit 4: Hold Stage 1 Active *)
IF (nHoldingProfileSubStage = 2)     THEN dwStatusWord2 := dwStatusWord2 OR 16#00000020; END_IF; (* Bit 5: Hold Stage 2 Active *)
IF (nHoldingProfileSubStage = 3)     THEN dwStatusWord2 := dwStatusWord2 OR 16#00000040; END_IF; (* Bit 6: Hold Stage 3 Active *)
IF (nHoldingProfileSubStage = 4)     THEN dwStatusWord2 := dwStatusWord2 OR 16#00000080; END_IF; (* Bit 7: Hold Stage 4 Active *)
IF (nHoldingProfileSubStage = 5)     THEN dwStatusWord2 := dwStatusWord2 OR 16#00000100; END_IF; (* Bit 8: Hold Stage 5 Active *)

(* dwAlarmWord1: Critical Emergency Safety Trips *)
dwAlarmWord1 := 16#00000000;
IF (NOT bEmergencyStop)              THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000001; END_IF; (* Bit 0: E-Stop Tripped *)
IF bAlarmLatched_FlashTrip           THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000002; END_IF; (* Bit 1: Parting Line Separation HH *)
IF bAlarmLatched_TieBarTrip          THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000004; END_IF; (* Bit 2: Tie-Bar Asymmetry HH *)
IF bAlarmLatched_NozzlePressHH       THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000008; END_IF; (* Bit 3: Nozzle Overpressure HH *)
IF bAlarmLatched_CavityPressHH       THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000010; END_IF; (* Bit 4: Cavity Overpressure HH *)
IF bAlarmLatched_ClampTonnageHH      THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000020; END_IF; (* Bit 5: Clamp Tonnage HH *)
IF bAlarmLatched_ClampTonnageLL      THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000040; END_IF; (* Bit 6: Clamp Tonnage Loss LL *)
IF bAlarmLatched_MoldProtectTrip     THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000080; END_IF; (* Bit 7: Mold Protect Obstruction *)
IF bAlarmLatched_CushionLL           THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000100; END_IF; (* Bit 8: Cushion Bottoming LL *)
IF bAlarmLatched_FillTimeout         THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000200; END_IF; (* Bit 9: Fill Watchdog Timeout *)

(* dwAlarmWord2: Process Warnings & Sensor Discordances *)
dwAlarmWord2 := 16#00000000;
IF bAlarmWarn_NozzlePressH           THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000001; END_IF; (* Bit 0: Nozzle Pressure High Warning *)
IF bAlarmWarn_CavityPressH           THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000002; END_IF; (* Bit 1: Cavity Pressure High Warning *)
IF bAlarmWarn_TieBarImbalanceH       THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000004; END_IF; (* Bit 2: Tie-Bar Asymmetry Warning *)
IF bAlarmWarn_PartingSeparationH     THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000008; END_IF; (* Bit 3: Mold Separation Warning *)
IF bAlarmWarn_MoldTempH              THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000010; END_IF; (* Bit 4: Mold Temperature High Warning *)
IF bAlarmWarn_MoldTempL              THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000020; END_IF; (* Bit 5: Mold Temperature Low Warning *)
IF bAlarmWarn_CushionL               THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000040; END_IF; (* Bit 6: Screw Cushion Low Warning *)
IF bAlarmWarn_GateFreezeDelay        THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000080; END_IF; (* Bit 7: Gate Freeze Delay Warning *)
IF bDiscrepancy_PT101                THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000100; END_IF; (* Bit 8: TMR Discrepancy PT-101 *)
IF bDiscrepancy_PT201                THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000200; END_IF; (* Bit 9: TMR Discrepancy PT-201 *)
IF bDiscrepancy_ST301                THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000400; END_IF; (* Bit 10: TMR Discrepancy ST-301 *)
IF bDiscrepancy_WT401                THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000800; END_IF; (* Bit 11: TMR Discrepancy WT-401 *)
IF bDiscrepancy_TT501                THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00001000; END_IF; (* Bit 12: TMR Discrepancy TT-501 *)

(* dwFirstOutWord: Root Cause First-Out Identifier *)
dwFirstOutWord := DINT_TO_DWORD(nFirstOutAlarmCode);

(* Assign Individual Discrete Alarm Outputs *)
bAlarm_DieFlashMoldSeparationTrip := bAlarmLatched_FlashTrip;
bAlarm_TieBarImbalanceTrip        := bAlarmLatched_TieBarTrip;
bAlarm_OverpressureNozzle_HH      := bAlarmLatched_NozzlePressHH;
bAlarm_OverpressureCavity_HH      := bAlarmLatched_CavityPressHH;
bAlarm_LowCushionWarning_L        := bAlarmWarn_CushionL;
bAlarm_GateFreezeTimeout          := bAlarmWarn_GateFreezeDelay;
bAlarm_TmrSensorFault             := bDiscrepancy_PT101 OR bDiscrepancy_PT201 OR bDiscrepancy_ST301 OR
                                     bDiscrepancy_WT401 OR bDiscrepancy_TT501;

(* ==================================================================================================== *)
(* ACTUATOR COMMAND FINAL CLAMPING & SAFETY HARDWARE INTERLOCK OVERRIDES                                 *)
(* ==================================================================================================== *)
rCmd_InjectionServoCurrent_pct := LIMIT(-100.0, rCmd_InjectionServoCurrent_pct, 100.0);
rCmd_HoldingPressure_bar       := LIMIT(0.0,    rCmd_HoldingPressure_bar,       2200.0);
rCmd_ScrewRotationSpeed_rpm    := LIMIT(0.0,    rCmd_ScrewRotationSpeed_rpm,    350.0);
rCmd_BackpressureValve_bar     := LIMIT(0.0,    rCmd_BackpressureValve_bar,     250.0);
rCmd_MoldCoolingValve_pct      := LIMIT(0.0,    rCmd_MoldCoolingValve_pct,      100.0);
rCmd_ClampingToggleServo_pct   := LIMIT(0.0,    rCmd_ClampingToggleServo_pct,   100.0);
rCmd_EjectorServoSpeed_pct     := LIMIT(-100.0, rCmd_EjectorServoSpeed_pct,     100.0);
rCmd_CarriageServoSpeed_pct    := LIMIT(-100.0, rCmd_CarriageServoSpeed_pct,    100.0);

(* Master Hardware Safety Overrides *)
IF (nFsmState = 13) OR NOT bEmergencyStop THEN
    rCmd_InjectionServoCurrent_pct := 0.0;
    rCmd_HoldingPressure_bar       := 0.0;
    rCmd_ScrewRotationSpeed_rpm    := 0.0;
    rCmd_BackpressureValve_bar     := 0.0;
    rCmd_EjectorServoSpeed_pct     := 0.0;
    rCmd_CarriageServoSpeed_pct    := 0.0;
    bCmd_HotRunnerValveGatesOpen   := FALSE;
END_IF;

nScanCounter := nScanCounter + 1;

END_FUNCTION_BLOCK
"""
