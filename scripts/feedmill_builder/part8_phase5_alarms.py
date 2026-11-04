# scripts/feedmill_builder/part8_phase5_alarms.py
# -*- coding: utf-8 -*-

def get_phase5_block():
    return """(* ====================================================================================================
   PHASE 5: ISA-18.2 MULTI-TIERED PROCESS ALARMS & DIAGNOSTIC WORD BIT-PACKING
   ==================================================================================================== *)

(* ----------------------------------------------------------------------------------------------------
   5.1 TIMED OVERCURRENT INTEGRATION (400 kW MOTOR CURRENT HH DEBOUNCE)
   ---------------------------------------------------------------------------------------------------- *)
IF rVoted_PressMotorCurrent_A >= rAlarmTrip_PressCurr_HH_Timed THEN
    tAlarmPressCurr_Timer_HH := tAlarmPressCurr_Timer_HH + 0.050;
ELSE
    tAlarmPressCurr_Timer_HH := MAX(0.0, tAlarmPressCurr_Timer_HH - 0.100);
END_IF;

(* Automatic Die Choke / Overload Detection *)
IF (rVoted_PressMotorCurrent_A >= rAlarmTrip_PressCurr_HH_Inst) 
   OR (tAlarmPressCurr_Timer_HH >= 3.0) 
   OR (rEst_RollerSlipRatio >= rAlarmTrip_RollerSlip_HH) THEN
    nFsm_DieChokeFaultLatch := TRUE;
    IF nFsm_CurrentState = 7 OR nFsm_CurrentState = 8 OR nFsm_CurrentState = 9 THEN
        nFsm_CurrentState := 11; (* Immediate Trip to Overload Bypass State *)
    END_IF;
END_IF;

(* ----------------------------------------------------------------------------------------------------
   5.2 PRIORITY 1 CRITICAL EMERGENCY ALARM WORD (DWORD dwAlarms_Critical_HH)
   ---------------------------------------------------------------------------------------------------- *)
dwAlarms_Critical_HH := 16#00000000;

(* Bit 0: Emergency Stop Safety Circuit Open *)
IF NOT bEmergStop_Circuit_OK THEN
    dwAlarms_Critical_HH := dwAlarms_Critical_HH OR 16#00000001;
END_IF;

(* Bit 1: Ring Die Inspection Door Safety Interlock Open *)
IF NOT bDieDoor_Closed_DI208 THEN
    dwAlarms_Critical_HH := dwAlarms_Critical_HH OR 16#00000002;
END_IF;

(* Bit 2: Main Shaft Mechanical Shear Pin Limit Switch Broken *)
IF NOT bShearPin_Intact_DI207 THEN
    dwAlarms_Critical_HH := dwAlarms_Critical_HH OR 16#00000004;
END_IF;

(* Bit 3: 400 kW Motor Instantaneous Overcurrent Trip (> 760 A) *)
IF rVoted_PressMotorCurrent_A >= rAlarmTrip_PressCurr_HH_Inst THEN
    dwAlarms_Critical_HH := dwAlarms_Critical_HH OR 16#00000008;
END_IF;

(* Bit 4: 400 kW Motor Timed Overcurrent Trip (> 720 A for 3.0 s) *)
IF tAlarmPressCurr_Timer_HH >= 3.0 THEN
    dwAlarms_Critical_HH := dwAlarms_Critical_HH OR 16#00000010;
END_IF;

(* Bit 5: Roller Traction Slip Critical Stall (Slip >= 35%) *)
IF rEst_RollerSlipRatio >= rAlarmTrip_RollerSlip_HH THEN
    dwAlarms_Critical_HH := dwAlarms_Critical_HH OR 16#00000020;
END_IF;

(* Bit 6: Ring Die Face Optical Temperature High-High Trip (>= 125 deg C) *)
IF rDieSurfaceTemp_TE203_degC >= rAlarmTrip_DieTemp_HH THEN
    dwAlarms_Critical_HH := dwAlarms_Critical_HH OR 16#00000040;
END_IF;

(* Bit 7: Roller Dynamic Hydraulic Gap Pressure Surge (>= 220 bar) *)
IF rVoted_HydGapPress_bar >= rAlarmTrip_HydPress_HH THEN
    dwAlarms_Critical_HH := dwAlarms_Critical_HH OR 16#00000080;
END_IF;

(* Bit 8: Conditioner Mash Under-Temperature Choke Risk (<= 65 deg C during steady pelleting) *)
IF (rVoted_CondMashTemp_degC <= rAlarmTrip_CondTemp_LL) AND (nFsm_CurrentState = 8) THEN
    dwAlarms_Critical_HH := dwAlarms_Critical_HH OR 16#00000100;
END_IF;

(* Bit 9: Conditioner Mash High-High Temperature Scorch (>= 98 deg C) *)
IF rVoted_CondMashTemp_degC >= rAlarmTrip_CondTemp_HH THEN
    dwAlarms_Critical_HH := dwAlarms_Critical_HH OR 16#00000200;
END_IF;

(* Bit 10: Conditioned Mash Moisture High-High Trip (>= 18.5%) *)
IF x_state[2] >= rAlarmTrip_MashMoist_HH THEN
    dwAlarms_Critical_HH := dwAlarms_Critical_HH OR 16#00000400;
END_IF;

(* Bit 11: Counterflow Cooler Bed Critical Overflow (>= 1420 mm) *)
IF rVoted_CoolerBedLevel_mm >= rAlarmTrip_CoolerBed_HH THEN
    dwAlarms_Critical_HH := dwAlarms_Critical_HH OR 16#00000800;
END_IF;

(* Bit 12: 2oo3 TMR Triplet 1 All-Channel Failure Trip (Mash Temp) *)
IF bTmr_CondTemp_Trip_0oo3 THEN
    dwAlarms_Critical_HH := dwAlarms_Critical_HH OR 16#00001000;
END_IF;

(* Bit 13: 2oo3 TMR Triplet 2 All-Channel Failure Trip (Motor Current) *)
IF bTmr_PressCurr_Trip_0oo3 THEN
    dwAlarms_Critical_HH := dwAlarms_Critical_HH OR 16#00002000;
END_IF;

(* Bit 14: 2oo3 TMR Triplet 3 All-Channel Failure Trip (Hydraulic Gap) *)
IF bTmr_HydGapPress_Trip_0oo3 THEN
    dwAlarms_Critical_HH := dwAlarms_Critical_HH OR 16#00004000;
END_IF;

(* Bit 15: 2oo3 TMR Triplet 4 All-Channel Failure Trip (Cooler Level) *)
IF bTmr_CoolerLevel_Trip_0oo3 THEN
    dwAlarms_Critical_HH := dwAlarms_Critical_HH OR 16#00008000;
END_IF;

(* ----------------------------------------------------------------------------------------------------
   5.3 PRIORITY 2 PROCESS WARNING & ADVISORY WORD (DWORD dwAlarms_Warning_H_L)
   ---------------------------------------------------------------------------------------------------- *)
dwAlarms_Warning_H_L := 16#00000000;

(* Bit 0: Conditioner Mash Temp High Warning (>= 94 deg C) *)
IF rVoted_CondMashTemp_degC >= rAlarmTrip_CondTemp_H THEN
    dwAlarms_Warning_H_L := dwAlarms_Warning_H_L OR 16#00000001;
END_IF;

(* Bit 1: Conditioner Mash Temp Low Warning (<= 82 deg C) *)
IF rVoted_CondMashTemp_degC <= rAlarmTrip_CondTemp_L THEN
    dwAlarms_Warning_H_L := dwAlarms_Warning_H_L OR 16#00000002;
END_IF;

(* Bit 2: Conditioned Mash Moisture High Warning (>= 17.2%) *)
IF x_state[2] >= rAlarmTrip_MashMoist_H THEN
    dwAlarms_Warning_H_L := dwAlarms_Warning_H_L OR 16#00000004;
END_IF;

(* Bit 3: Conditioned Mash Moisture Low Warning (<= 14.5%) *)
IF x_state[2] <= rAlarmTrip_MashMoist_L THEN
    dwAlarms_Warning_H_L := dwAlarms_Warning_H_L OR 16#00000008;
END_IF;

(* Bit 4: Pellet Mill Motor Current High Warning (>= 660 A) *)
IF rVoted_PressMotorCurrent_A >= rAlarmTrip_PressCurr_H THEN
    dwAlarms_Warning_H_L := dwAlarms_Warning_H_L OR 16#00000010;
END_IF;

(* Bit 5: Pellet Mill Motor Current Low Warning (<= 240 A during steady-state) *)
IF (rVoted_PressMotorCurrent_A <= rAlarmTrip_PressCurr_L) AND (nFsm_CurrentState = 8) THEN
    dwAlarms_Warning_H_L := dwAlarms_Warning_H_L OR 16#00000020;
END_IF;

(* Bit 6: Roller Dynamic Hydraulic Gap Pressure High Warning (>= 185 bar) *)
IF rVoted_HydGapPress_bar >= rAlarmTrip_HydPress_H THEN
    dwAlarms_Warning_H_L := dwAlarms_Warning_H_L OR 16#00000040;
END_IF;

(* Bit 7: Roller Dynamic Hydraulic Gap Pressure Low Warning (<= 45 bar) *)
IF rVoted_HydGapPress_bar <= rAlarmTrip_HydPress_L THEN
    dwAlarms_Warning_H_L := dwAlarms_Warning_H_L OR 16#00000080;
END_IF;

(* Bit 8: Ring Die Surface Temperature High Warning (>= 112 deg C) *)
IF rDieSurfaceTemp_TE203_degC >= rAlarmTrip_DieTemp_H THEN
    dwAlarms_Warning_H_L := dwAlarms_Warning_H_L OR 16#00000100;
END_IF;

(* Bit 9: Roller Dynamic Slip Factor High Warning (>= 18%) *)
IF rEst_RollerSlipRatio >= rAlarmTrip_RollerSlip_H THEN
    dwAlarms_Warning_H_L := dwAlarms_Warning_H_L OR 16#00000200;
END_IF;

(* Bit 10: Counterflow Cooler Bed Depth High Warning (>= 1250 mm) *)
IF rVoted_CoolerBedLevel_mm >= rAlarmTrip_CoolerBed_H THEN
    dwAlarms_Warning_H_L := dwAlarms_Warning_H_L OR 16#00000400;
END_IF;

(* Bit 11: Counterflow Cooler Bed Depth Low Warning (<= 500 mm) *)
IF rVoted_CoolerBedLevel_mm <= rAlarmTrip_CoolerBed_L THEN
    dwAlarms_Warning_H_L := dwAlarms_Warning_H_L OR 16#00000800;
END_IF;

(* Bit 12: Cooled Pellet Discharge Temperature High Warning (>= 38 deg C) *)
IF rCoolerDischargePelletTemp_degC >= 38.0 THEN
    dwAlarms_Warning_H_L := dwAlarms_Warning_H_L OR 16#00001000;
END_IF;

(* Bit 13: Vacuum Coater Pressure Deficient Vacuum Warning (>= -0.50 bar during evac) *)
IF (rCoaterVesselPress_PT401_bar >= -0.50) AND (nFsm_CurrentState = 9) AND (rFsm_StateTimeElapsed_s >= 16.0) THEN
    dwAlarms_Warning_H_L := dwAlarms_Warning_H_L OR 16#00002000;
END_IF;

(* Bit 14: Starch Gelatinization Extent Low Warning (<= 0.35 during steady pelleting) *)
IF (rEst_GelatinizationIndex <= 0.35) AND (nFsm_CurrentState = 8) THEN
    dwAlarms_Warning_H_L := dwAlarms_Warning_H_L OR 16#00004000;
END_IF;

(* Bit 15: Specific Mechanical Energy Consumption High (>= 14.5 kWh/t) *)
IF rEst_SpecificEnergy_kWh_ton >= 14.50 THEN
    dwAlarms_Warning_H_L := dwAlarms_Warning_H_L OR 16#00008000;
END_IF;

(* Bits 16-19: Degraded 1oo2 Sensor Mode Active *)
IF bTmr_CondTemp_Degraded_1oo2    THEN dwAlarms_Warning_H_L := dwAlarms_Warning_H_L OR 16#00010000; END_IF;
IF bTmr_PressCurr_Degraded_1oo2   THEN dwAlarms_Warning_H_L := dwAlarms_Warning_H_L OR 16#00020000; END_IF;
IF bTmr_HydGapPress_Degraded_1oo2 THEN dwAlarms_Warning_H_L := dwAlarms_Warning_H_L OR 16#00040000; END_IF;
IF bTmr_CoolerLevel_Degraded_1oo2 THEN dwAlarms_Warning_H_L := dwAlarms_Warning_H_L OR 16#00080000; END_IF;

(* ----------------------------------------------------------------------------------------------------
   5.4 FINITE STATE MACHINE DIAGNOSTIC BIT-PACKING (DWORD dwFSM_Diagnostic_Word)
   ---------------------------------------------------------------------------------------------------- *)
dwFSM_Diagnostic_Word := INT_TO_DWORD(nFsm_CurrentState);
IF bFsm_StateFirstScan         THEN dwFSM_Diagnostic_Word := dwFSM_Diagnostic_Word OR 16#00000100; END_IF;
IF bFsm_InterlockTripped       THEN dwFSM_Diagnostic_Word := dwFSM_Diagnostic_Word OR 16#00000200; END_IF;
IF nFsm_ShearPinTripLatch      THEN dwFSM_Diagnostic_Word := dwFSM_Diagnostic_Word OR 16#00000400; END_IF;
IF nFsm_DieChokeFaultLatch     THEN dwFSM_Diagnostic_Word := dwFSM_Diagnostic_Word OR 16#00000800; END_IF;
IF bCmdBypassFlap_Divert       THEN dwFSM_Diagnostic_Word := dwFSM_Diagnostic_Word OR 16#00001000; END_IF;
IF bAutoMode                   THEN dwFSM_Diagnostic_Word := dwFSM_Diagnostic_Word OR 16#00002000; END_IF;

(* ----------------------------------------------------------------------------------------------------
   5.5 ACTUATOR DRIVER COMMAND MAPPING & OUTPUT ASSIGNMENTS
   ---------------------------------------------------------------------------------------------------- *)
rCmdFeederSpeed_RPM     := u_ctrl[1];
rCmdSteamValve_pct      := u_ctrl[2];
rCmdShaftSpeed_RPM      := u_ctrl[3];
rCmdGapHydServo_pct     := u_ctrl[4];
rCmdCoolerDischarge_pct := u_ctrl[5];
rCmdCoolerFan_pct       := u_ctrl[6];

(* Bit-Packing Actuator Word *)
dwActuatorStatus_Word := 16#00000000;
IF u_ctrl[1] > 1.0  THEN dwActuatorStatus_Word := dwActuatorStatus_Word OR 16#00000001; END_IF; (* Feeder Active *)
IF u_ctrl[2] > 1.0  THEN dwActuatorStatus_Word := dwActuatorStatus_Word OR 16#00000002; END_IF; (* Steam Active *)
IF u_ctrl[3] > 10.0 THEN dwActuatorStatus_Word := dwActuatorStatus_Word OR 16#00000004; END_IF; (* Conditioner Active *)
IF u_ctrl[4] > 5.0  THEN dwActuatorStatus_Word := dwActuatorStatus_Word OR 16#00000008; END_IF; (* Gap Servo Active *)
IF u_ctrl[5] > 1.0  THEN dwActuatorStatus_Word := dwActuatorStatus_Word OR 16#00000010; END_IF; (* Cooler Grid Active *)
IF u_ctrl[6] > 10.0 THEN dwActuatorStatus_Word := dwActuatorStatus_Word OR 16#00000020; END_IF; (* Cooler Fan Active *)
IF bCmdCoaterVacuumPump    THEN dwActuatorStatus_Word := dwActuatorStatus_Word OR 16#00000040; END_IF;
IF bCmdCoaterFatSprayValve THEN dwActuatorStatus_Word := dwActuatorStatus_Word OR 16#00000080; END_IF;
IF bCmdCoaterEnzymeValve   THEN dwActuatorStatus_Word := dwActuatorStatus_Word OR 16#00000100; END_IF;
IF bCmdCoaterVentValve     THEN dwActuatorStatus_Word := dwActuatorStatus_Word OR 16#00000200; END_IF;
IF bCmdCoaterDischargeGate THEN dwActuatorStatus_Word := dwActuatorStatus_Word OR 16#00000400; END_IF;

(* Update previous control vector for rate limiting on next scan *)
FOR m := 1 TO 6 DO
    u_prev[m] := u_ctrl[m];
END_FOR;

END_FUNCTION_BLOCK
"""
