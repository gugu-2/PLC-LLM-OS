# rail_emu_builder/part7_alarms_diagnostics.py

def get_part7():
    return '''(* ============================================================================================== *)
(* PHASE 10: ISA-18.2 MULTI-TIERED ALARM MATRIX & 32-BIT BIT-PACKED DIAGNOSTIC REGISTERS         *)
(* High-High, High, Low, Low-Low Dynamic Trips with Deadband Hysteresis Clearance                 *)
(* ============================================================================================== *)

(* 1. DC Link Intermediate Bus Differential Voltage Hierarchy *)
IF rVotedDCLinkVoltage_V > ALARM_HH_DC_VOLTAGE_V THEN
    bAlarmGroupHighHigh_DCOvervoltage := TRUE;
ELSIF rVotedDCLinkVoltage_V < (ALARM_HH_DC_VOLTAGE_V - ALARM_HYST_DC_VOLTAGE_V) THEN
    IF bAlarmAcknowledge THEN
        bAlarmGroupHighHigh_DCOvervoltage := FALSE;
    END_IF;
END_IF;

IF rVotedDCLinkVoltage_V < ALARM_LL_DC_VOLTAGE_V THEN
    bAlarmGroupLowLow_DCUndervoltage := TRUE;
ELSIF rVotedDCLinkVoltage_V > (ALARM_LL_DC_VOLTAGE_V + ALARM_HYST_DC_VOLTAGE_V) THEN
    IF bAlarmAcknowledge THEN
        bAlarmGroupLowLow_DCUndervoltage := FALSE;
    END_IF;
END_IF;

(* 2. Traction Inverter Peak Stator Current Trip *)
IF (ABS(rTorqueCurrentCommand_Isq_A) > ALARM_HH_STATOR_CURRENT_A) OR 
   (rFluxCurrentCommand_Isd_A > ALARM_HH_STATOR_CURRENT_A) THEN
    bAlarmGroupHigh_InverterOvercurrent := TRUE;
ELSIF (ABS(rTorqueCurrentCommand_Isq_A) < ALARM_H_STATOR_CURRENT_A) AND 
      (rFluxCurrentCommand_Isd_A < ALARM_H_STATOR_CURRENT_A) THEN
    IF bAlarmAcknowledge THEN
        bAlarmGroupHigh_InverterOvercurrent := FALSE;
    END_IF;
END_IF;

(* 3. Traction Motor Stator Winding Temperature RTD Trip *)
rScratchAccum := MAX(rTractionMotorTemp_U_degC, MAX(rTractionMotorTemp_V_degC, rTractionMotorTemp_W_degC));
IF rScratchAccum > ALARM_HH_MOTOR_TEMP_DEGC THEN
    bAlarmGroupHigh_MotorOvertemp := TRUE;
ELSIF rScratchAccum < (ALARM_HH_MOTOR_TEMP_DEGC - ALARM_HYST_MOTOR_TEMP_DEGC) THEN
    IF bAlarmAcknowledge THEN
        bAlarmGroupHigh_MotorOvertemp := FALSE;
    END_IF;
END_IF;

(* 4. Pantograph Catenary Dynamic Contact Force Limits *)
IF rVotedPantoForce_N < ALARM_LL_PANTO_FORCE_N THEN
    bAlarmGroup_PantographContactLost := TRUE;
ELSIF rVotedPantoForce_N > (ALARM_LL_PANTO_FORCE_N + ALARM_HYST_PANTO_FORCE_N) THEN
    IF bAlarmAcknowledge THEN
        bAlarmGroup_PantographContactLost := FALSE;
    END_IF;
END_IF;

(* 5. Main Air Reservoir Pneumatics Depletion Trip *)
IF rMainReservoirPressure_bar < ALARM_LL_MAIN_RES_BAR THEN
    bAlarmGroup_BrakePneumaticDepleted := TRUE;
ELSIF rMainReservoirPressure_bar > (ALARM_LL_MAIN_RES_BAR + ALARM_HYST_MAIN_RES_BAR) THEN
    IF bAlarmAcknowledge THEN
        bAlarmGroup_BrakePneumaticDepleted := FALSE;
    END_IF;
END_IF;

(* 6. Wheel Slip-Slide Macro-Runaway Trip *)
IF (ABS(rEstimatedWheelSlip_A1_pct) > 15.0) OR (ABS(rEstimatedWheelSlip_A2_pct) > 15.0) THEN
    bAlarmGroup_WheelSlipSlideExcessive := TRUE;
ELSIF (ABS(rEstimatedWheelSlip_A1_pct) < 3.0) AND (ABS(rEstimatedWheelSlip_A2_pct) < 3.0) THEN
    IF bAlarmAcknowledge THEN
        bAlarmGroup_WheelSlipSlideExcessive := FALSE;
    END_IF;
END_IF;

(* ============================================================================================== *)
(* PHASE 11: 32-BIT BIT-PACKED STATUS & DIAGNOSTIC WORD ENCODING                                  *)
(* ============================================================================================== *)

(* 1. dwTractionStatusWord Packing *)
dwTractionStatusWord := 16#00000000;
IF bTCUReady THEN dwTractionStatusWord := dwTractionStatusWord OR 16#00000001; END_IF;
IF bTractionEnableCmd THEN dwTractionStatusWord := dwTractionStatusWord OR 16#00000002; END_IF;
IF rTractionTorqueCommand_kNm > 0.5 THEN dwTractionStatusWord := dwTractionStatusWord OR 16#00000004; END_IF;
IF rVotedTrainSpeed_kmh > MOTOR_BASE_SPEED_KMH THEN dwTractionStatusWord := dwTractionStatusWord OR 16#00000008; END_IF;
IF nFSM_CurrentState = 6 THEN dwTractionStatusWord := dwTractionStatusWord OR 16#00000010; END_IF;
IF bVCBCloseCommand THEN dwTractionStatusWord := dwTractionStatusWord OR 16#00000020; END_IF;
IF bPantographRaiseCommand THEN dwTractionStatusWord := dwTractionStatusWord OR 16#00000040; END_IF;
IF nFSM_CurrentState = 11 THEN dwTractionStatusWord := dwTractionStatusWord OR 16#00000080; END_IF;
dwTractionStatusWord := dwTractionStatusWord OR SHL(INT_TO_DWORD(nFSM_CurrentState), 8);
IF bRailheadSandingActive THEN dwTractionStatusWord := dwTractionStatusWord OR 16#00001000; END_IF;
IF nSpeed_DegradedVotingMode < 3 THEN dwTractionStatusWord := dwTractionStatusWord OR 16#00010000; END_IF;
IF nAxle1_DegradedVotingMode < 3 THEN dwTractionStatusWord := dwTractionStatusWord OR 16#00020000; END_IF;
IF nAxle2_DegradedVotingMode < 3 THEN dwTractionStatusWord := dwTractionStatusWord OR 16#00040000; END_IF;
IF nPanto_DegradedVotingMode < 3 THEN dwTractionStatusWord := dwTractionStatusWord OR 16#00080000; END_IF;
IF nDCLink_DegradedVotingMode < 3 THEN dwTractionStatusWord := dwTractionStatusWord OR 16#00100000; END_IF;
IF nBrakeCyl_DegradedVotingMode < 3 THEN dwTractionStatusWord := dwTractionStatusWord OR 16#00200000; END_IF;

(* 2. dwBrakingStatusWord Packing *)
dwBrakingStatusWord := 16#00000000;
IF bBCUReady THEN dwBrakingStatusWord := dwBrakingStatusWord OR 16#00000001; END_IF;
IF bBrakingEnableCmd THEN dwBrakingStatusWord := dwBrakingStatusWord OR 16#00000002; END_IF;
IF rTotalBrakingDemand_kN > 1.0 THEN dwBrakingStatusWord := dwBrakingStatusWord OR 16#00000004; END_IF;
IF rRegenerativeBrakeTorque_kNm > 0.5 THEN dwBrakingStatusWord := dwBrakingStatusWord OR 16#00000008; END_IF;
IF rPneumaticBrakePressure_SP_bar > 0.3 THEN dwBrakingStatusWord := dwBrakingStatusWord OR 16#00000010; END_IF;
IF nFSM_CurrentState = 10 THEN dwBrakingStatusWord := dwBrakingStatusWord OR 16#00000020; END_IF;
IF bEmergencyTripActive THEN dwBrakingStatusWord := dwBrakingStatusWord OR 16#00000040; END_IF;
IF rAxleWeightShift_kN > 5.0 THEN dwBrakingStatusWord := dwBrakingStatusWord OR 16#00000080; END_IF;

(* 3. dwWSSPStatusWord Packing *)
dwWSSPStatusWord := 16#00000000;
dwWSSPStatusWord := dwWSSPStatusWord OR INT_TO_DWORD(nWSSP_Phase_Axle1);
dwWSSPStatusWord := dwWSSPStatusWord OR SHL(INT_TO_DWORD(nWSSP_Phase_Axle2), 2);
IF bWSSPDumpValveCmd_A1 THEN dwWSSPStatusWord := dwWSSPStatusWord OR 16#00000010; END_IF;
IF bWSSPApplyValveCmd_A1 THEN dwWSSPStatusWord := dwWSSPStatusWord OR 16#00000020; END_IF;
IF bWSSPDumpValveCmd_A2 THEN dwWSSPStatusWord := dwWSSPStatusWord OR 16#00000040; END_IF;
IF bWSSPApplyValveCmd_A2 THEN dwWSSPStatusWord := dwWSSPStatusWord OR 16#00000080; END_IF;
IF rEstimatedWheelSlip_A1_pct > 3.0 THEN dwWSSPStatusWord := dwWSSPStatusWord OR 16#00000100; END_IF;
IF rEstimatedWheelSlip_A1_pct < -3.0 THEN dwWSSPStatusWord := dwWSSPStatusWord OR 16#00000200; END_IF;
IF rEstimatedWheelSlip_A2_pct > 3.0 THEN dwWSSPStatusWord := dwWSSPStatusWord OR 16#00000400; END_IF;
IF rEstimatedWheelSlip_A2_pct < -3.0 THEN dwWSSPStatusWord := dwWSSPStatusWord OR 16#00000800; END_IF;
IF bRailheadSandingActive THEN dwWSSPStatusWord := dwWSSPStatusWord OR 16#00001000; END_IF;
IF rLowAdhesionAccumulator_s > 0.50 THEN dwWSSPStatusWord := dwWSSPStatusWord OR 16#00002000; END_IF;

(* 4. dwAlarmDiagnostics_1 (Critical Priority 1 Trips) *)
dwAlarmDiagnostics_1 := 16#00000000;
IF bAlarmGroupHighHigh_DCOvervoltage THEN dwAlarmDiagnostics_1 := dwAlarmDiagnostics_1 OR 16#00000001; END_IF;
IF bAlarmGroupLowLow_DCUndervoltage THEN dwAlarmDiagnostics_1 := dwAlarmDiagnostics_1 OR 16#00000002; END_IF;
IF bAlarmGroupHigh_InverterOvercurrent THEN dwAlarmDiagnostics_1 := dwAlarmDiagnostics_1 OR 16#00000004; END_IF;
IF bAlarmGroupHigh_MotorOvertemp THEN dwAlarmDiagnostics_1 := dwAlarmDiagnostics_1 OR 16#00000008; END_IF;
IF bAlarmGroup_WheelSlipSlideExcessive THEN dwAlarmDiagnostics_1 := dwAlarmDiagnostics_1 OR 16#00000010; END_IF;
IF bAlarmGroup_PantographContactLost THEN dwAlarmDiagnostics_1 := dwAlarmDiagnostics_1 OR 16#00000020; END_IF;
IF bAlarmGroup_BrakePneumaticDepleted THEN dwAlarmDiagnostics_1 := dwAlarmDiagnostics_1 OR 16#00000040; END_IF;
IF NOT bEmergencyBrakeLoop THEN dwAlarmDiagnostics_1 := dwAlarmDiagnostics_1 OR 16#00000080; END_IF;

(* 5. dwAlarmDiagnostics_2 (Advisory Warnings & Sensor Degradation) *)
dwAlarmDiagnostics_2 := 16#00000000;
IF NOT bSpeed_ChannelA_Valid THEN dwAlarmDiagnostics_2 := dwAlarmDiagnostics_2 OR 16#00000001; END_IF;
IF NOT bSpeed_ChannelB_Valid THEN dwAlarmDiagnostics_2 := dwAlarmDiagnostics_2 OR 16#00000002; END_IF;
IF NOT bSpeed_ChannelC_Valid THEN dwAlarmDiagnostics_2 := dwAlarmDiagnostics_2 OR 16#00000004; END_IF;
IF NOT bAxle1_ChannelA_Valid THEN dwAlarmDiagnostics_2 := dwAlarmDiagnostics_2 OR 16#00000008; END_IF;
IF NOT bAxle1_ChannelB_Valid THEN dwAlarmDiagnostics_2 := dwAlarmDiagnostics_2 OR 16#00000010; END_IF;
IF NOT bAxle1_ChannelC_Valid THEN dwAlarmDiagnostics_2 := dwAlarmDiagnostics_2 OR 16#00000020; END_IF;
IF NOT bAxle2_ChannelA_Valid THEN dwAlarmDiagnostics_2 := dwAlarmDiagnostics_2 OR 16#00000040; END_IF;
IF NOT bAxle2_ChannelB_Valid THEN dwAlarmDiagnostics_2 := dwAlarmDiagnostics_2 OR 16#00000080; END_IF;
IF NOT bAxle2_ChannelC_Valid THEN dwAlarmDiagnostics_2 := dwAlarmDiagnostics_2 OR 16#00000100; END_IF;
IF NOT bPanto_ChannelA_Valid THEN dwAlarmDiagnostics_2 := dwAlarmDiagnostics_2 OR 16#00000200; END_IF;
IF NOT bPanto_ChannelB_Valid THEN dwAlarmDiagnostics_2 := dwAlarmDiagnostics_2 OR 16#00000400; END_IF;
IF NOT bPanto_ChannelC_Valid THEN dwAlarmDiagnostics_2 := dwAlarmDiagnostics_2 OR 16#00000800; END_IF;
IF NOT bDCLink_ChannelA_Valid THEN dwAlarmDiagnostics_2 := dwAlarmDiagnostics_2 OR 16#00001000; END_IF;
IF NOT bDCLink_ChannelB_Valid THEN dwAlarmDiagnostics_2 := dwAlarmDiagnostics_2 OR 16#00002000; END_IF;
IF NOT bDCLink_ChannelC_Valid THEN dwAlarmDiagnostics_2 := dwAlarmDiagnostics_2 OR 16#00004000; END_IF;
IF NOT bBrakeCyl_ChannelA_Valid THEN dwAlarmDiagnostics_2 := dwAlarmDiagnostics_2 OR 16#00008000; END_IF;
IF NOT bBrakeCyl_ChannelB_Valid THEN dwAlarmDiagnostics_2 := dwAlarmDiagnostics_2 OR 16#00010000; END_IF;
IF NOT bBrakeCyl_ChannelC_Valid THEN dwAlarmDiagnostics_2 := dwAlarmDiagnostics_2 OR 16#00020000; END_IF;

END_FUNCTION_BLOCK
'''
