# cmp_polisher_builder/part7_alarms_diagnostics.py

def get_part7():
    return """(*
========================================================================================================================
  PHASE 5: ISA-18.2 MULTI-TIER ALARMS, 32-BIT BIT-PACKED STATUS WORDS & DIAGNOSTICS
  DEADBAND HYSTERESIS, PRIORITY ESCALATION, BITMASK SERIALIZATION & SHUTDOWN TRIP MAPPING
========================================================================================================================
*)
(* ------------------------------------------------------------------------------------------------------------------ *)
(* 1. ISA-18.2 MULTI-TIERED ALARM EVALUATION WITH CLEARING DEADBANDS                                                  *)
(* ------------------------------------------------------------------------------------------------------------------ *)
(* Pad Surface Temperature Alarm Tier *)
IF rVotedPadTemp_degC >= rPadTemp_Limit_HH_degC THEN
    bAlarmPadTemp_HH := TRUE;
ELSIF rVotedPadTemp_degC <= (rPadTemp_Limit_HH_degC - rPadTemp_Deadband_degC) THEN
    bAlarmPadTemp_HH := FALSE;
END_IF;

IF rVotedPadTemp_degC >= rPadTemp_Limit_H_degC THEN
    bAlarmPadTemp_H := TRUE;
ELSIF rVotedPadTemp_degC <= (rPadTemp_Limit_H_degC - rPadTemp_Deadband_degC) THEN
    bAlarmPadTemp_H := FALSE;
END_IF;

(* Platen Friction Torque Alarm Tier *)
IF rVotedPlatenTorque_Nm >= rPlatenTorque_Limit_HH_Nm THEN
    bAlarmPlatenTorque_HH := TRUE;
ELSIF rVotedPlatenTorque_Nm <= (rPlatenTorque_Limit_HH_Nm - rPlatenTorque_Deadband_Nm) THEN
    bAlarmPlatenTorque_HH := FALSE;
END_IF;

IF rVotedPlatenTorque_Nm >= rPlatenTorque_Limit_H_Nm THEN
    bAlarmPlatenTorque_H := TRUE;
ELSIF rVotedPlatenTorque_Nm <= (rPlatenTorque_Limit_H_Nm - rPlatenTorque_Deadband_Nm) THEN
    bAlarmPlatenTorque_H := FALSE;
END_IF;

(* Carrier Chucking Vacuum Alarm Tier *)
IF (rCarrierVacuum_kPa > rCarrierVac_Limit_LL_kPa) AND (bWaferChucked_Carrier OR (nOperationalState >= STATE_CMP_WAFER_LOAD_CUP_HANDSHAKE)) THEN
    bAlarmCarrierVac_LL := TRUE;
ELSIF rCarrierVacuum_kPa <= (rCarrierVac_Limit_LL_kPa - rCarrierVac_Deadband_kPa) THEN
    bAlarmCarrierVac_LL := FALSE;
END_IF;

IF (rCarrierVacuum_kPa > rCarrierVac_Limit_L_kPa) AND (bWaferChucked_Carrier) THEN
    bAlarmCarrierVac_L := TRUE;
ELSIF rCarrierVacuum_kPa <= (rCarrierVac_Limit_L_kPa - rCarrierVac_Deadband_kPa) THEN
    bAlarmCarrierVac_L := FALSE;
END_IF;

(* Chemical Slurry Delivery Alarm Tier *)
IF bProductionActive AND (nOperationalState >= STATE_CMP_LOW_PRESSURE_TOUCHDOWN) AND (nOperationalState <= STATE_CMP_SOFT_LANDING_OVERPOLISH) THEN
    IF rSlurryFlow_PV_mLpm <= rSlurryFlow_Limit_LL_mLpm THEN
        bAlarmSlurryFlow_LL := TRUE;
    ELSIF rSlurryFlow_PV_mLpm >= (rSlurryFlow_Limit_LL_mLpm + 30.0) THEN
        bAlarmSlurryFlow_LL := FALSE;
    END_IF;
    
    IF (rSlurryPH_PV_pH >= rSlurryPH_Limit_HH) OR (rSlurryPH_PV_pH <= rSlurryPH_Limit_LL) THEN
        bAlarmSlurryPH_Excursion := TRUE;
    ELSIF (rSlurryPH_PV_pH <= (rSlurryPH_Limit_HH - 0.2)) AND (rSlurryPH_PV_pH >= (rSlurryPH_Limit_LL + 0.2)) THEN
        bAlarmSlurryPH_Excursion := FALSE;
    END_IF;
ELSE
    bAlarmSlurryFlow_LL := FALSE;
    bAlarmSlurryPH_Excursion := FALSE;
END_IF;

(* Pad Conditioner Acoustic Emission Alarm Tier *)
IF bCondArmInService AND (rStateTimer_s >= 4.0) THEN
    IF (rCondAcousticRMS_Filtered_mV <= rCondAE_Limit_LL_mV) OR (rCondAcousticRMS_Filtered_mV >= rCondAE_Limit_HH_mV) THEN
        bAlarmConditioner_AE_Fault := TRUE;
    ELSIF (rCondAcousticRMS_Filtered_mV >= (rCondAE_Limit_LL_mV + 4.0)) AND (rCondAcousticRMS_Filtered_mV <= (rCondAE_Limit_HH_mV - 6.0)) THEN
        bAlarmConditioner_AE_Fault := FALSE;
    END_IF;
ELSE
    bAlarmConditioner_AE_Fault := FALSE;
END_IF;

(* TMR Sensor Discrepancy Aggregator *)
bAlarmGroup_TMR_SensorDiscrepancy := (nOpt_DegradedVotingMode < 3) OR 
                                     (nEddy_DegradedVotingMode < 3) OR 
                                     (nTorq_DegradedVotingMode < 3) OR 
                                     (nZ1P_DegradedVotingMode < 3) OR 
                                     (nPadT_DegradedVotingMode < 3);

(* Primary Alarm Group Aggregations *)
bAlarmGroup_CriticalEStop       := (NOT bEmergencyStop) OR bEmergencyTripActive;
bAlarmGroup_WaferSlipLoss       := bAlarmCarrierVac_LL;
bAlarmGroup_OverTorque          := bAlarmPlatenTorque_HH;
bAlarmGroup_SlurryDeliveryFault := bAlarmSlurryFlow_LL OR bAlarmSlurryPH_Excursion;
bAlarmGroup_ConditionerFault    := bAlarmConditioner_AE_Fault;
bAlarmGroup_ThermalExcursion    := bAlarmPadTemp_HH;

(* ------------------------------------------------------------------------------------------------------------------ *)
(* 2. BIT-PACKED 32-BIT DWORD SERIALIZATION (SECS/GEM SCADA INTERFACE)                                                *)
(* ------------------------------------------------------------------------------------------------------------------ *)
(* dwCMP_StatusWord: Operational and Kinematic State Flags *)
dwCMP_StatusWord := 16#00000000;
IF bSystemReady                     THEN dwCMP_StatusWord := dwCMP_StatusWord OR 16#00000001; END_IF;
IF bProductionActive                THEN dwCMP_StatusWord := dwCMP_StatusWord OR 16#00000002; END_IF;
IF bWaferChucked_Carrier            THEN dwCMP_StatusWord := dwCMP_StatusWord OR 16#00000004; END_IF;
IF rPlatenSpeed_PV_rpm > 5.0        THEN dwCMP_StatusWord := dwCMP_StatusWord OR 16#00000008; END_IF;
IF rCarrierSpeed_PV_rpm > 5.0       THEN dwCMP_StatusWord := dwCMP_StatusWord OR 16#00000010; END_IF;
IF bSlurryDeliveryValveCmd          THEN dwCMP_StatusWord := dwCMP_StatusWord OR 16#00000020; END_IF;
IF bCondArmInService                THEN dwCMP_StatusWord := dwCMP_StatusWord OR 16#00000040; END_IF;
IF bDIW_FlushValveCmd               THEN dwCMP_StatusWord := dwCMP_StatusWord OR 16#00000080; END_IF;
IF (nOperationalState >= STATE_CMP_LOW_PRESSURE_TOUCHDOWN) THEN dwCMP_StatusWord := dwCMP_StatusWord OR 16#00000100; END_IF;
IF (nOperationalState = STATE_CMP_MULTI_ZONE_BULK_RAMP)   THEN dwCMP_StatusWord := dwCMP_StatusWord OR 16#00000200; END_IF;
IF bEddyCurrentEndpointLatched      THEN dwCMP_StatusWord := dwCMP_StatusWord OR 16#00000400; END_IF;
IF bOpticalEndpointLatched          THEN dwCMP_StatusWord := dwCMP_StatusWord OR 16#00000800; END_IF;
IF (nOperationalState = STATE_CMP_SOFT_LANDING_OVERPOLISH) THEN dwCMP_StatusWord := dwCMP_StatusWord OR 16#00001000; END_IF;
IF bWaferPolishedComplete           THEN dwCMP_StatusWord := dwCMP_StatusWord OR 16#00002000; END_IF;
IF (nOperationalState = STATE_CMP_UNLOAD_CUP_TRANSFER)     THEN dwCMP_StatusWord := dwCMP_StatusWord OR 16#00004000; END_IF;
IF (nOperationalState = STATE_CMP_IN_SITU_PAD_CONDITIONING) THEN dwCMP_StatusWord := dwCMP_StatusWord OR 16#00008000; END_IF;

(* Encode Recipe ID in Bits 16-19 *)
dwCMP_StatusWord := dwCMP_StatusWord OR SHL(INT_TO_DWORD(nActiveRecipeID AND 16#0F), 16);

(* Encode FSM State in Bits 20-23 *)
dwCMP_StatusWord := dwCMP_StatusWord OR SHL(INT_TO_DWORD(nOperationalState AND 16#0F), 20);

IF (NOT bEmergencyTripActive)       THEN dwCMP_StatusWord := dwCMP_StatusWord OR 16#01000000; END_IF; (* MPC Active *)
IF (rRetainingRingPressCmd_psi > 1.0) THEN dwCMP_StatusWord := dwCMP_StatusWord OR 16#02000000; END_IF; (* ERO Active *)
IF bHighPressurePadRinseCmd         THEN dwCMP_StatusWord := dwCMP_StatusWord OR 16#04000000; END_IF;
IF rCarrierZAxisPosition_mm > 50.0  THEN dwCMP_StatusWord := dwCMP_StatusWord OR 16#08000000; END_IF; (* Head Lifted *)
IF bRecipeStartCmd                  THEN dwCMP_StatusWord := dwCMP_StatusWord OR 16#10000000; END_IF;
IF bAlarmAcknowledge                THEN dwCMP_StatusWord := dwCMP_StatusWord OR 16#20000000; END_IF;
IF bAlarmGroup_TMR_SensorDiscrepancy THEN dwCMP_StatusWord := dwCMP_StatusWord OR 16#40000000; END_IF;
IF bEmergencyStop                   THEN dwCMP_StatusWord := dwCMP_StatusWord OR 16#80000000; END_IF;

(* dwCMP_DiagnosticWord: Detailed Fault and Degradation Bitmask *)
dwCMP_DiagnosticWord := 16#00000000;
IF bAlarmPadTemp_H                  THEN dwCMP_DiagnosticWord := dwCMP_DiagnosticWord OR 16#00000001; END_IF;
IF bAlarmPadTemp_HH                 THEN dwCMP_DiagnosticWord := dwCMP_DiagnosticWord OR 16#00000002; END_IF;
IF bAlarmPlatenTorque_H             THEN dwCMP_DiagnosticWord := dwCMP_DiagnosticWord OR 16#00000004; END_IF;
IF bAlarmPlatenTorque_HH            THEN dwCMP_DiagnosticWord := dwCMP_DiagnosticWord OR 16#00000008; END_IF;
IF bAlarmCarrierVac_L               THEN dwCMP_DiagnosticWord := dwCMP_DiagnosticWord OR 16#00000010; END_IF;
IF bAlarmCarrierVac_LL              THEN dwCMP_DiagnosticWord := dwCMP_DiagnosticWord OR 16#00000020; END_IF;
IF (rSlurryFlow_PV_mLpm < rSlurryFlow_Limit_L_mLpm) THEN dwCMP_DiagnosticWord := dwCMP_DiagnosticWord OR 16#00000040; END_IF;
IF bAlarmSlurryFlow_LL              THEN dwCMP_DiagnosticWord := dwCMP_DiagnosticWord OR 16#00000080; END_IF;
IF (rSlurryPH_PV_pH >= rSlurryPH_Limit_HH) THEN dwCMP_DiagnosticWord := dwCMP_DiagnosticWord OR 16#00000100; END_IF;
IF (rSlurryPH_PV_pH <= rSlurryPH_Limit_LL) THEN dwCMP_DiagnosticWord := dwCMP_DiagnosticWord OR 16#00000200; END_IF;
IF (rSlurrySupplyPressure_bar < 1.2) THEN dwCMP_DiagnosticWord := dwCMP_DiagnosticWord OR 16#00000400; END_IF;
IF (rCondAcousticRMS_Filtered_mV <= rCondAE_Limit_LL_mV) THEN dwCMP_DiagnosticWord := dwCMP_DiagnosticWord OR 16#00000800; END_IF;
IF (rCondAcousticRMS_Filtered_mV >= rCondAE_Limit_HH_mV) THEN dwCMP_DiagnosticWord := dwCMP_DiagnosticWord OR 16#00001000; END_IF;
IF (ABS(rCondDownforceError_lbf) > 3.0) THEN dwCMP_DiagnosticWord := dwCMP_DiagnosticWord OR 16#00002000; END_IF;
IF (nOpt_DegradedVotingMode < 3)    THEN dwCMP_DiagnosticWord := dwCMP_DiagnosticWord OR 16#00004000; END_IF;
IF (nEddy_DegradedVotingMode < 3)   THEN dwCMP_DiagnosticWord := dwCMP_DiagnosticWord OR 16#00008000; END_IF;
IF (nTorq_DegradedVotingMode < 3)   THEN dwCMP_DiagnosticWord := dwCMP_DiagnosticWord OR 16#00010000; END_IF;
IF (nZ1P_DegradedVotingMode < 3)    THEN dwCMP_DiagnosticWord := dwCMP_DiagnosticWord OR 16#00020000; END_IF;
IF (nPadT_DegradedVotingMode < 3)   THEN dwCMP_DiagnosticWord := dwCMP_DiagnosticWord OR 16#00040000; END_IF;
IF (ABS(rZoneError_02_psi) > 0.8)   THEN dwCMP_DiagnosticWord := dwCMP_DiagnosticWord OR 16#00080000; END_IF;
IF (ABS(rZoneError_03_psi) > 0.8)   THEN dwCMP_DiagnosticWord := dwCMP_DiagnosticWord OR 16#00100000; END_IF;
IF (ABS(rZoneError_04_psi) > 0.8)   THEN dwCMP_DiagnosticWord := dwCMP_DiagnosticWord OR 16#00200000; END_IF;
IF (ABS(rZoneError_05_psi) > 0.8)   THEN dwCMP_DiagnosticWord := dwCMP_DiagnosticWord OR 16#00400000; END_IF;
IF (ABS(rRetainingRingError_psi) > 1.2) THEN dwCMP_DiagnosticWord := dwCMP_DiagnosticWord OR 16#00800000; END_IF;
IF (rDIW_SupplyPressure_bar < 2.5)  THEN dwCMP_DiagnosticWord := dwCMP_DiagnosticWord OR 16#01000000; END_IF;
IF (rPneumaticSupplyPressure_bar < 5.0) THEN dwCMP_DiagnosticWord := dwCMP_DiagnosticWord OR 16#02000000; END_IF;
IF (rExhaustNegativePressure_Pa > -80.0) THEN dwCMP_DiagnosticWord := dwCMP_DiagnosticWord OR 16#04000000; END_IF;
IF (rCleanroomAmbientTemp_degC > 24.5)   THEN dwCMP_DiagnosticWord := dwCMP_DiagnosticWord OR 16#08000000; END_IF;
IF (rStateTimer_s > rStateTimeout_s) THEN dwCMP_DiagnosticWord := dwCMP_DiagnosticWord OR 16#10000000; END_IF;
IF (NOT bSystemEnable)              THEN dwCMP_DiagnosticWord := dwCMP_DiagnosticWord OR 16#20000000; END_IF;
IF (NOT bEmergencyStop)             THEN dwCMP_DiagnosticWord := dwCMP_DiagnosticWord OR 16#40000000; END_IF;
IF bEmergencyTripActive             THEN dwCMP_DiagnosticWord := dwCMP_DiagnosticWord OR 16#80000000; END_IF;

(* Master Alarm Acknowledge and Clear Handshake *)
IF bAlarmAcknowledge THEN
    (* Operator acknowledges visible alarms *)
END_IF;

IF bAlarmReset AND (NOT bEmergencyTripActive) THEN
    bAlarmPadTemp_HH := FALSE;
    bAlarmPadTemp_H := FALSE;
    bAlarmPlatenTorque_HH := FALSE;
    bAlarmPlatenTorque_H := FALSE;
    bAlarmCarrierVac_LL := FALSE;
    bAlarmCarrierVac_L := FALSE;
    bAlarmSlurryFlow_LL := FALSE;
    bAlarmSlurryPH_Excursion := FALSE;
    bAlarmConditioner_AE_Fault := FALSE;
END_IF;

(* Clear One-Shot Rising Edge Trigger *)
bStateFirstScan := FALSE;

END_FUNCTION_BLOCK
"""
