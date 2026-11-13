# stator_laser_welding_builder/part8_phase5_alarms.py

def get_phase5_alarms():
    return """(*
====================================================================================================
PHASE 5: ISA-18.2 MULTI-TIER PROCESS ALARM MATRIX, PARTICLE TRIPS & 32-BIT STATUS WORDS
Alarm Hierarchy:
  - Priority 1 Critical: Optical Beam Dump, Emergency Fast Shutter & Safety Lockout
  - Priority 2 High:     Stator Crown Defect Quarantine, Micro-Ohmmeter Rejection
  - Priority 3 Warning:  Protective Slide Film Advance, Degradation Flags, Maintenance Alerts
Bit-Packed Status & Alarm Words:
  - dwStatusWord1:          Actuator Solenoids, Beam Modulation, FSM Phase Active Bits
  - dwStatusWord2:          Sensor Health, 2oo3 Degraded Modes, Quality Indices
  - dwAlarmWord1_Critical:  ISA-18.2 Priority 1 Fast Safety Shutdown Trip Bits
  - dwAlarmWord2_High:      ISA-18.2 Priority 2 Process Deviation & Expulsion Bits
  - dwAlarmWord3_Warning:   ISA-18.2 Priority 3 Advisory & Preventive Service Bits
====================================================================================================
*)

(* -------------------------------------------------------------------------------------------------
   STEP 5.1: ISA-18.2 PROCESS ALARM EVALUATION WITH DEADBAND HYSTERESIS
   ------------------------------------------------------------------------------------------------- *)
(* 5.1.1: Melt Pool Temperature Alarm Evaluation *)
IF rMeltPool_Voted_degC >= rTrip_MeltPool_HH_degC THEN
    dwAlarmWord1_Critical := dwAlarmWord1_Critical OR 16#00000001; (* Bit 0: Melt Pool Temp Critical High-High Trip *)
ELSIF rMeltPool_Voted_degC <= (rTrip_MeltPool_HH_degC - rDeadband_MeltPool_degC) THEN
    dwAlarmWord1_Critical := dwAlarmWord1_Critical AND 16#FFFFFFFE;
END_IF;

IF rMeltPool_Voted_degC >= rTrip_MeltPool_H_degC THEN
    dwAlarmWord2_High := dwAlarmWord2_High OR 16#00000001; (* Bit 0: Melt Pool Temp High Warning *)
ELSIF rMeltPool_Voted_degC <= (rTrip_MeltPool_H_degC - rDeadband_MeltPool_degC) THEN
    dwAlarmWord2_High := dwAlarmWord2_High AND 16#FFFFFFFE;
END_IF;

IF (rMeltPool_Voted_degC <= rTrip_MeltPool_LL_degC) AND (iFSM_CurrentState = 6) AND (iWeldSubPhase = 3) THEN
    dwAlarmWord1_Critical := dwAlarmWord1_Critical OR 16#00000002; (* Bit 1: Melt Pool Cold Weld Lack-of-Fusion Trip *)
ELSIF rMeltPool_Voted_degC >= (rTrip_MeltPool_LL_degC + rDeadband_MeltPool_degC) THEN
    dwAlarmWord1_Critical := dwAlarmWord1_Critical AND 16#FFFFFFFD;
END_IF;

IF (rMeltPool_Voted_degC <= rTrip_MeltPool_L_degC) AND (iFSM_CurrentState = 6) AND (iWeldSubPhase >= 2) THEN
    dwAlarmWord2_High := dwAlarmWord2_High OR 16#00000002; (* Bit 1: Melt Pool Low Temperature Warning *)
ELSIF rMeltPool_Voted_degC >= (rTrip_MeltPool_L_degC + rDeadband_MeltPool_degC) THEN
    dwAlarmWord2_High := dwAlarmWord2_High AND 16#FFFFFFFD;
END_IF;

(* 5.1.2: Hairpin Crown Pin Gap Alarm Evaluation *)
IF rGap_Voted_mm >= rTrip_PinGap_HH_mm THEN
    dwAlarmWord1_Critical := dwAlarmWord1_Critical OR 16#00000004; (* Bit 2: Pin Crown Gap Critical High-High Trip *)
ELSIF rGap_Voted_mm <= (rTrip_PinGap_HH_mm - rDeadband_PinGap_mm) THEN
    dwAlarmWord1_Critical := dwAlarmWord1_Critical AND 16#FFFFFFFB;
END_IF;

IF rGap_Voted_mm >= rTrip_PinGap_H_mm THEN
    dwAlarmWord2_High := dwAlarmWord2_High OR 16#00000004; (* Bit 2: Pin Crown Gap High Advisory *)
ELSIF rGap_Voted_mm <= (rTrip_PinGap_H_mm - rDeadband_PinGap_mm) THEN
    dwAlarmWord2_High := dwAlarmWord2_High AND 16#FFFFFFFB;
END_IF;

(* 5.1.3: Nitrogen Shielding Gas Flow Alarm Evaluation *)
IF (rShieldGas_Voted_Lmin <= rTrip_ShieldGas_LL_Lmin) AND (iFSM_CurrentState >= 4) AND (iFSM_CurrentState <= 6) THEN
    dwAlarmWord1_Critical := dwAlarmWord1_Critical OR 16#00000008; (* Bit 3: Shielding Gas Critical Low-Low Cutout Trip *)
ELSIF rShieldGas_Voted_Lmin >= (rTrip_ShieldGas_LL_Lmin + rDeadband_ShieldGas_Lmin) THEN
    dwAlarmWord1_Critical := dwAlarmWord1_Critical AND 16#FFFFFFF7;
END_IF;

IF (rShieldGas_Voted_Lmin <= rTrip_ShieldGas_L_Lmin) AND (iFSM_CurrentState >= 4) AND (iFSM_CurrentState <= 6) THEN
    dwAlarmWord2_High := dwAlarmWord2_High OR 16#00000008; (* Bit 3: Shielding Gas Low Flow Process Warning *)
ELSIF rShieldGas_Voted_Lmin >= (rTrip_ShieldGas_L_Lmin + rDeadband_ShieldGas_Lmin) THEN
    dwAlarmWord2_High := dwAlarmWord2_High AND 16#FFFFFFF7;
END_IF;

(* 5.1.4: Optics Protective Cover Glass Transmission Alarm Evaluation *)
IF rOptics_Transmission_pct <= rTrip_OpticsTransmission_LL_pct THEN
    dwAlarmWord1_Critical := dwAlarmWord1_Critical OR 16#00000010; (* Bit 4: Optics Transmission Critical Low-Low Trip *)
ELSIF rOptics_Transmission_pct >= (rTrip_OpticsTransmission_LL_pct + rDeadband_OpticsTransmission_pct) THEN
    dwAlarmWord1_Critical := dwAlarmWord1_Critical AND 16#FFFFFFEF;
END_IF;

IF rOptics_Transmission_pct <= rTrip_OpticsTransmission_L_pct THEN
    dwAlarmWord3_Warning := dwAlarmWord3_Warning OR 16#00000001; (* Bit 0: Cover Glass Clean/Advance Advisory *)
ELSIF rOptics_Transmission_pct >= (rTrip_OpticsTransmission_L_pct + rDeadband_OpticsTransmission_pct) THEN
    dwAlarmWord3_Warning := dwAlarmWord3_Warning AND 16#FFFFFFFE;
END_IF;

(* 5.1.5: In-Line 4-Wire Kelvin Joint Resistance Alarm Evaluation *)
IF rEddyCurrent_Resistance_uOhm >= rTrip_JointResistance_HH_uOhm THEN
    dwAlarmWord2_High := dwAlarmWord2_High OR 16#00000010; (* Bit 4: Joint Electrical Resistance High-High Defect *)
ELSIF rEddyCurrent_Resistance_uOhm <= (rTrip_JointResistance_HH_uOhm - rDeadband_JointResistance_uOhm) THEN
    dwAlarmWord2_High := dwAlarmWord2_High AND 16#FFFFFFEF;
END_IF;

IF rEddyCurrent_Resistance_uOhm >= rTrip_JointResistance_H_uOhm THEN
    dwAlarmWord3_Warning := dwAlarmWord3_Warning OR 16#00000002; (* Bit 1: Joint Resistance Elevated Warning *)
ELSIF rEddyCurrent_Resistance_uOhm <= (rTrip_JointResistance_H_uOhm - rDeadband_JointResistance_uOhm) THEN
    dwAlarmWord3_Warning := dwAlarmWord3_Warning AND 16#FFFFFFFD;
END_IF;

(* 5.1.6: Stator Slot Liner Aramid Paper (Nomex/PAI) Thermal Alarm Evaluation *)
IF rSlotLiner_ThermalAccum_degC >= rTrip_InsulationTemp_HH_degC THEN
    dwAlarmWord1_Critical := dwAlarmWord1_Critical OR 16#00000020; (* Bit 5: Insulation Thermal Runaway Over-Temp Trip *)
ELSIF rSlotLiner_ThermalAccum_degC <= (rTrip_InsulationTemp_HH_degC - 5.0) THEN
    dwAlarmWord1_Critical := dwAlarmWord1_Critical AND 16#FFFFFFDF;
END_IF;

IF rSlotLiner_ThermalAccum_degC >= rTrip_InsulationTemp_H_degC THEN
    dwAlarmWord2_High := dwAlarmWord2_High OR 16#00000020; (* Bit 5: Insulation High Temperature Advisory *)
ELSIF rSlotLiner_ThermalAccum_degC <= (rTrip_InsulationTemp_H_degC - 5.0) THEN
    dwAlarmWord2_High := dwAlarmWord2_High AND 16#FFFFFFDF;
END_IF;

(* 5.1.7: Direct-Drive Rotary Chuck Position Tracking Error Alarm Evaluation *)
rTemp_Scalar1 := ABS(rChuck_ActualPosition_deg - rChuck_TargetPosition_deg);
IF (rTemp_Scalar1 >= rTrip_ChuckPosError_HH_deg) AND (iFSM_CurrentState = 6) THEN
    dwAlarmWord1_Critical := dwAlarmWord1_Critical OR 16#00000040; (* Bit 6: Chuck Tracking Error Runaway Trip During Weld *)
ELSIF rTemp_Scalar1 <= (rTrip_ChuckPosError_HH_deg - 0.002) THEN
    dwAlarmWord1_Critical := dwAlarmWord1_Critical AND 16#FFFFFFBF;
END_IF;

IF rTemp_Scalar1 >= rTrip_ChuckPosError_H_deg THEN
    dwAlarmWord3_Warning := dwAlarmWord3_Warning OR 16#00000004; (* Bit 2: Chuck Motion Settle Lag Warning *)
ELSIF rTemp_Scalar1 <= (rTrip_ChuckPosError_H_deg - 0.001) THEN
    dwAlarmWord3_Warning := dwAlarmWord3_Warning AND 16#FFFFFFFB;
END_IF;

(* 5.1.8: 2oo3 Sensor Voting Failure Alarms (Critical Loss of 2+ Channels) *)
IF bGap_SensorVotingFailure THEN
    dwAlarmWord1_Critical := dwAlarmWord1_Critical OR 16#00000080; (* Bit 7: Pin Gap 2oo3 Sensor Bank Failure *)
END_IF;

IF bHeight_SensorVotingFailure THEN
    dwAlarmWord1_Critical := dwAlarmWord1_Critical OR 16#00000100; (* Bit 8: Pin Height 2oo3 Sensor Bank Failure *)
END_IF;

IF bMeltPool_SensorVotingFailure THEN
    dwAlarmWord1_Critical := dwAlarmWord1_Critical OR 16#00000200; (* Bit 9: Pyrometer 2oo3 Sensor Bank Failure *)
END_IF;

IF bLaserPwr_SensorVotingFailure THEN
    dwAlarmWord1_Critical := dwAlarmWord1_Critical OR 16#00000400; (* Bit 10: Laser Power 2oo3 Sensor Bank Failure *)
END_IF;

IF bShieldGas_SensorVotingFailure THEN
    dwAlarmWord1_Critical := dwAlarmWord1_Critical OR 16#00000800; (* Bit 11: Gas Flow 2oo3 Sensor Bank Failure *)
END_IF;

IF bHydClamp_SensorVotingFailure THEN
    dwAlarmWord1_Critical := dwAlarmWord1_Critical OR 16#00001000; (* Bit 12: Hydraulic Chuck 2oo3 Sensor Bank Failure *)
END_IF;

IF bStateTimeoutFault THEN
    dwAlarmWord1_Critical := dwAlarmWord1_Critical OR 16#00002000; (* Bit 13: FSM State Watchdog Timeout Fault *)
END_IF;

IF (iTotalSpatterEventsInStator >= 3) THEN
    dwAlarmWord2_High := dwAlarmWord2_High OR 16#00000040; (* Bit 6: Stator Excessive Spatter Defect Threshold *)
END_IF;

(* -------------------------------------------------------------------------------------------------
   STEP 5.2: 2oo3 DEGRADED OPERATIONAL WARNINGS (SINGLE CHANNEL DISCREPANCY)
   ------------------------------------------------------------------------------------------------- *)
IF bGap_DegradedMode THEN
    dwAlarmWord3_Warning := dwAlarmWord3_Warning OR 16#00000008; (* Bit 3: Gap Sensor Degraded Channel Failover *)
ELSE
    dwAlarmWord3_Warning := dwAlarmWord3_Warning AND 16#FFFFFFF7;
END_IF;

IF bHeight_DegradedMode THEN
    dwAlarmWord3_Warning := dwAlarmWord3_Warning OR 16#00000010; (* Bit 4: Height Sensor Degraded Mode *)
ELSE
    dwAlarmWord3_Warning := dwAlarmWord3_Warning AND 16#FFFFFFEF;
END_IF;

IF bMeltPool_DegradedMode THEN
    dwAlarmWord3_Warning := dwAlarmWord3_Warning OR 16#00000020; (* Bit 5: Pyrometer Photodiode Degraded Mode *)
ELSE
    dwAlarmWord3_Warning := dwAlarmWord3_Warning AND 16#FFFFFFDF;
END_IF;

IF bLaserPwr_DegradedMode THEN
    dwAlarmWord3_Warning := dwAlarmWord3_Warning OR 16#00000040; (* Bit 6: Laser Power Sensor Degraded Mode *)
ELSE
    dwAlarmWord3_Warning := dwAlarmWord3_Warning AND 16#FFFFFFBF;
END_IF;

IF bShieldGas_DegradedMode THEN
    dwAlarmWord3_Warning := dwAlarmWord3_Warning OR 16#00000080; (* Bit 7: Gas Flow Sensor Degraded Mode *)
ELSE
    dwAlarmWord3_Warning := dwAlarmWord3_Warning AND 16#FFFFFF7F;
END_IF;

IF bHydClamp_DegradedMode THEN
    dwAlarmWord3_Warning := dwAlarmWord3_Warning OR 16#00000100; (* Bit 8: Hydraulic Pressure Sensor Degraded Mode *)
ELSE
    dwAlarmWord3_Warning := dwAlarmWord3_Warning AND 16#FFFFFEFF;
END_IF;

(* -------------------------------------------------------------------------------------------------
   STEP 5.3: ASSEMBLE 32-BIT BIT-PACKED STATUS WORDS
   ------------------------------------------------------------------------------------------------- *)
(* 5.3.1: dwStatusWord1 - Master Operational Actuation & Hardware States *)
dwStatusWord1 := 16#00000000;
IF bEnable                     THEN dwStatusWord1 := dwStatusWord1 OR 16#00000001; END_IF; (* Bit 0: FB Enable *)
IF bAutoCycleStart             THEN dwStatusWord1 := dwStatusWord1 OR 16#00000002; END_IF; (* Bit 1: Auto Cycle Start *)
IF bLaserEmission_Enable       THEN dwStatusWord1 := dwStatusWord1 OR 16#00000004; END_IF; (* Bit 2: Laser Gate Active *)
IF bLaserFastShutter_Open      THEN dwStatusWord1 := dwStatusWord1 OR 16#00000008; END_IF; (* Bit 3: Fast Shutter Open *)
IF bLaserAimingBeam_On         THEN dwStatusWord1 := dwStatusWord1 OR 16#00000010; END_IF; (* Bit 4: Pilot Beam On *)
IF bChuck_MoveExecute          THEN dwStatusWord1 := dwStatusWord1 OR 16#00000020; END_IF; (* Bit 5: Chuck Indexing Active *)
IF bChuck_HoldBrakeRelease     THEN dwStatusWord1 := dwStatusWord1 OR 16#00000040; END_IF; (* Bit 6: Chuck Brake Released *)
IF bChuck_HydClamp_Sol         THEN dwStatusWord1 := dwStatusWord1 OR 16#00000080; END_IF; (* Bit 7: Chuck Clamp Solenoid *)
IF bChuck_HydUnclamp_Sol       THEN dwStatusWord1 := dwStatusWord1 OR 16#00000100; END_IF; (* Bit 8: Chuck Unclamp Solenoid *)
IF bDatumPin_Extend_Sol        THEN dwStatusWord1 := dwStatusWord1 OR 16#00000200; END_IF; (* Bit 9: Datum Pin Extend *)
IF bShieldGas_Purge_Valve      THEN dwStatusWord1 := dwStatusWord1 OR 16#00000400; END_IF; (* Bit 10: Shield Gas Valve *)
IF bCrossJet_AirKnife_Valve    THEN dwStatusWord1 := dwStatusWord1 OR 16#00000800; END_IF; (* Bit 11: Cross Jet Air Knife *)
IF bCoverGlass_MotorAdvance    THEN dwStatusWord1 := dwStatusWord1 OR 16#00001000; END_IF; (* Bit 12: Cover Glass Motor Advance *)
IF bFumeExtraction_FanOn       THEN dwStatusWord1 := dwStatusWord1 OR 16#00002000; END_IF; (* Bit 13: Fume Blower Fan On *)
IF bVision_CaptureStrobe       THEN dwStatusWord1 := dwStatusWord1 OR 16#00004000; END_IF; (* Bit 14: 3D Vision Capture *)
IF bEddyCurrent_ProbeExtend    THEN dwStatusWord1 := dwStatusWord1 OR 16#00008000; END_IF; (* Bit 15: Kelvin Probe Extend *)
IF bQuarantineDivert_Push      THEN dwStatusWord1 := dwStatusWord1 OR 16#00010000; END_IF; (* Bit 16: Defect Diverter Extend *)
IF bPartPresentInChuck         THEN dwStatusWord1 := dwStatusWord1 OR 16#00020000; END_IF; (* Bit 17: Part In Chuck *)
IF bPalletClampedInStation     THEN dwStatusWord1 := dwStatusWord1 OR 16#00040000; END_IF; (* Bit 18: Pallet Clamped *)
IF bChuck_InPositionFlag       THEN dwStatusWord1 := dwStatusWord1 OR 16#00080000; END_IF; (* Bit 19: Chuck In Position *)
IF bCellCycleCompleted         THEN dwStatusWord1 := dwStatusWord1 OR 16#00100000; END_IF; (* Bit 20: 96-Pair Cycle Done *)
IF bCellGeneralFault           THEN dwStatusWord1 := dwStatusWord1 OR 16#00200000; END_IF; (* Bit 21: General Cell Fault *)
IF bCellEmergencyTripped       THEN dwStatusWord1 := dwStatusWord1 OR 16#00400000; END_IF; (* Bit 22: Emergency Tripped *)
IF bDryRunMode                 THEN dwStatusWord1 := dwStatusWord1 OR 16#00800000; END_IF; (* Bit 23: Dry Run Mode *)
(* Bits 24..31: Encode Current FSM State Index *)
dwStatusWord1 := dwStatusWord1 OR SHL(INT_TO_DWORD(iFSM_CurrentState AND 16#00FF), 24);

(* 5.3.2: dwStatusWord2 - Subsystem Health, 2oo3 Status, Quality Indicators *)
dwStatusWord2 := 16#00000000;
IF bGap_ChA_Healthy            THEN dwStatusWord2 := dwStatusWord2 OR 16#00000001; END_IF; (* Bit 0: Gap 1A Healthy *)
IF bGap_ChB_Healthy            THEN dwStatusWord2 := dwStatusWord2 OR 16#00000002; END_IF; (* Bit 1: Gap 1B Healthy *)
IF bGap_ChC_Healthy            THEN dwStatusWord2 := dwStatusWord2 OR 16#00000004; END_IF; (* Bit 2: Gap 1C Healthy *)
IF bMeltPool_ChA_Healthy       THEN dwStatusWord2 := dwStatusWord2 OR 16#00000008; END_IF; (* Bit 3: Pyro 2A Healthy *)
IF bMeltPool_ChB_Healthy       THEN dwStatusWord2 := dwStatusWord2 OR 16#00000010; END_IF; (* Bit 4: Pyro 2B Healthy *)
IF bMeltPool_ChC_Healthy       THEN dwStatusWord2 := dwStatusWord2 OR 16#00000020; END_IF; (* Bit 5: Pyro 2C Healthy *)
IF bLaserPwr_ChA_Healthy       THEN dwStatusWord2 := dwStatusWord2 OR 16#00000040; END_IF; (* Bit 6: Laser Pwr 3A Healthy *)
IF bLaserPwr_ChB_Healthy       THEN dwStatusWord2 := dwStatusWord2 OR 16#00000080; END_IF; (* Bit 7: Laser Pwr 3B Healthy *)
IF bLaserPwr_ChC_Healthy       THEN dwStatusWord2 := dwStatusWord2 OR 16#00000100; END_IF; (* Bit 8: Laser Pwr 3C Healthy *)
IF bShieldGas_ChA_Healthy      THEN dwStatusWord2 := dwStatusWord2 OR 16#00000200; END_IF; (* Bit 9: Gas Flow 4A Healthy *)
IF bShieldGas_ChB_Healthy      THEN dwStatusWord2 := dwStatusWord2 OR 16#00000400; END_IF; (* Bit 10: Gas Flow 4B Healthy *)
IF bShieldGas_ChC_Healthy      THEN dwStatusWord2 := dwStatusWord2 OR 16#00000800; END_IF; (* Bit 11: Gas Flow 4C Healthy *)
IF bHydClamp_ChA_Healthy       THEN dwStatusWord2 := dwStatusWord2 OR 16#00001000; END_IF; (* Bit 12: Hyd Clamp 5A Healthy *)
IF bHydClamp_ChB_Healthy       THEN dwStatusWord2 := dwStatusWord2 OR 16#00002000; END_IF; (* Bit 13: Hyd Clamp 5B Healthy *)
IF bHydClamp_ChC_Healthy       THEN dwStatusWord2 := dwStatusWord2 OR 16#00004000; END_IF; (* Bit 14: Hyd Clamp 5C Healthy *)
IF bGap_DegradedMode           THEN dwStatusWord2 := dwStatusWord2 OR 16#00008000; END_IF; (* Bit 15: Gap Degraded *)
IF bHeight_DegradedMode        THEN dwStatusWord2 := dwStatusWord2 OR 16#00010000; END_IF; (* Bit 16: Height Degraded *)
IF bMeltPool_DegradedMode      THEN dwStatusWord2 := dwStatusWord2 OR 16#00020000; END_IF; (* Bit 17: Pyro Degraded *)
IF bLaserPwr_DegradedMode      THEN dwStatusWord2 := dwStatusWord2 OR 16#00040000; END_IF; (* Bit 18: Power Degraded *)
IF bShieldGas_DegradedMode     THEN dwStatusWord2 := dwStatusWord2 OR 16#00080000; END_IF; (* Bit 19: Gas Degraded *)
IF bHydClamp_DegradedMode      THEN dwStatusWord2 := dwStatusWord2 OR 16#00100000; END_IF; (* Bit 20: Hyd Degraded *)
IF bSpatterExpulsionDetected   THEN dwStatusWord2 := dwStatusWord2 OR 16#00200000; END_IF; (* Bit 21: Spatter Expulsion Active *)
(* Bits 24..31: Encode Current Active Hairpin Pair Index (1..96) *)
dwStatusWord2 := dwStatusWord2 OR SHL(INT_TO_DWORD(iCurrentWeldPairNumber AND 16#00FF), 24);

(* -------------------------------------------------------------------------------------------------
   STEP 5.4: MASTER ALARM SUMMARY & RESET HANDSHAKE
   ------------------------------------------------------------------------------------------------- *)
IF (dwAlarmWord1_Critical <> 16#00000000) OR (dwAlarmWord2_High <> 16#00000000) THEN
    bCellGeneralFault := TRUE;
END_IF;

IF bResetFault THEN
    IF dwAlarmWord1_Critical = 16#00000000 THEN
        bCellGeneralFault := FALSE;
    END_IF;
    IF bAckAlarm THEN
        dwAlarmWord2_High    := 16#00000000;
        dwAlarmWord3_Warning := 16#00000000;
    END_IF;
END_IF;

(* Master Cycle Run Time & Loop Counter Accumulation *)
udiScanCounter := udiScanCounter + 1;
rTotalElapsedRunTime_s := rTotalElapsedRunTime_s + rScanTime_s;

END_FUNCTION_BLOCK
"""
