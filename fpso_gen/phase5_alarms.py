# fpso_gen/phase5_alarms.py
def get_phase5():
    return """
(* =====================================================================================================================
 * PHASE 5: ISA-18.2 MULTI-TIER ALARMS, DEADBANDS & 32-BIT BIT-PACKED STATUS WORDS
 * Standardized alarm engine incorporating High-High (HH), High (H), Low (L), Low-Low (LL) trip/warning states,
 * deadband hysteresis filtering, priority escalation management, and bit-packed DWORD diagnostic registers.
 * ===================================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------------------------
 * SUBSECTION 5.1: SUCTION & DISCHARGE PRESSURE ISA-18.2 ALARMS WITH HYSTERESIS DEADBANDS
 * --------------------------------------------------------------------------------------------------------------------- *)
(* PT-101 Suction Pressure High-High (HH) Trip *)
IF rVoted_SuctionPres_Out >= rSet_PT101_HH THEN
    bTrip_SuctionPres_HH := TRUE;
ELSIF rVoted_SuctionPres_Out <= (rSet_PT101_HH - rDB_PT101) THEN
    bTrip_SuctionPres_HH := FALSE;
END_IF;

(* PT-101 Suction Pressure Low-Low (LL) Trip *)
IF rVoted_SuctionPres_Out <= rSet_PT101_LL THEN
    bTrip_SuctionPres_LL := TRUE;
ELSIF rVoted_SuctionPres_Out >= (rSet_PT101_LL + rDB_PT101) THEN
    bTrip_SuctionPres_LL := FALSE;
END_IF;

(* PT-201 Discharge Pressure High-High (HH) Trip *)
IF rVoted_DischargePres_Out >= rSet_PT201_HH THEN
    bTrip_DischargePres_HH := TRUE;
ELSIF rVoted_DischargePres_Out <= (rSet_PT201_HH - rDB_PT201) THEN
    bTrip_DischargePres_HH := FALSE;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * SUBSECTION 5.2: SURGE PROXIMITY, SHAFT VIBRATION & EXPORT MOISTURE CRITICAL TRIPS
 * --------------------------------------------------------------------------------------------------------------------- *)
(* Surge Incursion SIL-3 Trip: Any stage surge margin dropping below critical limit (Ss < 1.03) *)
IF (rSurgeMargin_Stg1 <= rSet_Surge_LL) OR
   (rSurgeMargin_Stg2 <= rSet_Surge_LL) OR
   (rSurgeMargin_Stg3 <= rSet_Surge_LL) THEN
    bTrip_SurgeIncursion := TRUE;
ELSIF (rSurgeMargin_Stg1 >= (rSet_Surge_LL + rDB_Surge)) AND
      (rSurgeMargin_Stg2 >= (rSet_Surge_LL + rDB_Surge)) AND
      (rSurgeMargin_Stg3 >= (rSet_Surge_LL + rDB_Surge)) THEN
    bTrip_SurgeIncursion := FALSE;
END_IF;

(* VT-401 Shaft Radial Vibration High-High (HH) Trip *)
IF rVoted_ShaftVib_Out >= rSet_VT401_HH THEN
    bTrip_ShaftVibration_HH := TRUE;
ELSIF rVoted_ShaftVib_Out <= (rSet_VT401_HH - rDB_VT401) THEN
    bTrip_ShaftVibration_HH := FALSE;
END_IF;

(* AT-501 Export Gas Moisture High-High (HH) Off-Spec Divert Trip *)
IF rVoted_ExportMoisture_Out >= rSet_AT501_HH THEN
    bTrip_ExportMoisture_HH := TRUE;
ELSIF rVoted_ExportMoisture_Out <= (rSet_AT501_HH - rDB_AT501) THEN
    bTrip_ExportMoisture_HH := FALSE;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * SUBSECTION 5.3: MECHANICAL AUXILIARY, REBOILER & TEG CONTACTOR SAFETY TRIPS
 * --------------------------------------------------------------------------------------------------------------------- *)
(* PT-601 Lube Oil Header Pressure Low-Low (LL) Mechanical Protection Trip *)
IF rLubeOilPres_PT601_In <= rSet_PT601_LL THEN
    bTrip_LubeOil_LL := TRUE;
ELSIF rLubeOilPres_PT601_In >= (rSet_PT601_LL + rDB_PT601) THEN
    bTrip_LubeOil_LL := FALSE;
END_IF;

(* PDT-701 Dry Gas Seal Primary Differential Low-Low (LL) Trip *)
IF rSealGasDP_PDT701_In <= rSet_PDT701_LL THEN
    bTrip_SealGas_LL := TRUE;
ELSIF rSealGasDP_PDT701_In >= (rSet_PDT701_LL + rDB_PDT701) THEN
    bTrip_SealGas_LL := FALSE;
END_IF;

(* TT-503 TEG Regeneration Reboiler Glycol Thermal Degradation High-High (HH) Trip *)
IF rTEG_ReboilerTemp_TT503_In >= rSet_TT503_HH THEN
    bTrip_Reboiler_HH := TRUE;
ELSIF rTEG_ReboilerTemp_TT503_In <= (rSet_TT503_HH - rDB_TT503) THEN
    bTrip_Reboiler_HH := FALSE;
END_IF;

(* TEG Contactor Column Foaming High-High (HH) Trip *)
IF rContactor_FoamIndex >= rSet_Foam_HH THEN
    bTrip_Foam_HH := TRUE;
ELSIF rContactor_FoamIndex <= (rSet_Foam_HH - rDB_Foam) THEN
    bTrip_Foam_HH := FALSE;
END_IF;

(* Manual Operator SIL-3 Emergency Depressurization Request *)
IF bCmd_EmergencyDepress_In THEN
    bTrip_EmergencyDepress_Manual := TRUE;
END_IF;

(* Latch Master Safety Trip Signal *)
IF bTrip_SuctionPres_HH OR bTrip_SuctionPres_LL OR bTrip_DischargePres_HH OR
   bTrip_SurgeIncursion OR bTrip_ShaftVibration_HH OR bTrip_ExportMoisture_HH OR
   bTrip_LubeOil_LL OR bTrip_SealGas_LL OR bTrip_Reboiler_HH OR bTrip_Foam_HH OR
   bTrip_TMR_CriticalLoss OR bTrip_EmergencyDepress_Manual THEN
    bSystem_Trip_Latched_Out := TRUE;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * SUBSECTION 5.4: 32-BIT BIT-PACKED ISA-18.2 CRITICAL TRIP DWORD TELEMETRY
 * --------------------------------------------------------------------------------------------------------------------- *)
dwAlarm_Trip_Critical_Out := 16#00000000;
IF bTrip_SuctionPres_HH          THEN dwAlarm_Trip_Critical_Out := dwAlarm_Trip_Critical_Out OR 16#00000001; END_IF;
IF bTrip_SuctionPres_LL          THEN dwAlarm_Trip_Critical_Out := dwAlarm_Trip_Critical_Out OR 16#00000002; END_IF;
IF bTrip_DischargePres_HH        THEN dwAlarm_Trip_Critical_Out := dwAlarm_Trip_Critical_Out OR 16#00000004; END_IF;
IF bTrip_SurgeIncursion          THEN dwAlarm_Trip_Critical_Out := dwAlarm_Trip_Critical_Out OR 16#00000008; END_IF;
IF bTrip_ShaftVibration_HH       THEN dwAlarm_Trip_Critical_Out := dwAlarm_Trip_Critical_Out OR 16#00000010; END_IF;
IF bTrip_ExportMoisture_HH       THEN dwAlarm_Trip_Critical_Out := dwAlarm_Trip_Critical_Out OR 16#00000020; END_IF;
IF bTrip_LubeOil_LL              THEN dwAlarm_Trip_Critical_Out := dwAlarm_Trip_Critical_Out OR 16#00000040; END_IF;
IF bTrip_SealGas_LL              THEN dwAlarm_Trip_Critical_Out := dwAlarm_Trip_Critical_Out OR 16#00000080; END_IF;
IF bTrip_Reboiler_HH             THEN dwAlarm_Trip_Critical_Out := dwAlarm_Trip_Critical_Out OR 16#00000100; END_IF;
IF (rTEG_ReboilerTemp_TT503_In <= rSet_TT503_LL) THEN
                                      dwAlarm_Trip_Critical_Out := dwAlarm_Trip_Critical_Out OR 16#00000200; END_IF;
IF bTrip_Foam_HH                 THEN dwAlarm_Trip_Critical_Out := dwAlarm_Trip_Critical_Out OR 16#00000400; END_IF;
IF bTrip_TMR_CriticalLoss        THEN dwAlarm_Trip_Critical_Out := dwAlarm_Trip_Critical_Out OR 16#00000800; END_IF;
IF bTrip_EmergencyDepress_Manual THEN dwAlarm_Trip_Critical_Out := dwAlarm_Trip_Critical_Out OR 16#00001000; END_IF;
IF bVFD_EmergencyTrip_Out        THEN dwAlarm_Trip_Critical_Out := dwAlarm_Trip_Critical_Out OR 16#00002000; END_IF;
IF (rPipeline_BackPres_PT801_In >= 265.0) THEN
                                      dwAlarm_Trip_Critical_Out := dwAlarm_Trip_Critical_Out OR 16#00004000; END_IF;
IF (NOT bPermissive_InfeedGas_In) AND (iFSM_State >= 40) THEN
                                      dwAlarm_Trip_Critical_Out := dwAlarm_Trip_Critical_Out OR 16#00008000; END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * SUBSECTION 5.5: 32-BIT BIT-PACKED ISA-18.2 HIGH WARNING ALARM DWORD TELEMETRY
 * --------------------------------------------------------------------------------------------------------------------- *)
dwAlarm_Warnings_High_Out := 16#00000000;
IF (rVoted_SuctionPres_Out >= rSet_PT101_H) THEN
    dwAlarm_Warnings_High_Out := dwAlarm_Warnings_High_Out OR 16#00000001; END_IF;
IF (rVoted_DischargePres_Out >= rSet_PT201_H) THEN
    dwAlarm_Warnings_High_Out := dwAlarm_Warnings_High_Out OR 16#00000002; END_IF;
IF (rVoted_ShaftVib_Out >= rSet_VT401_H) THEN
    dwAlarm_Warnings_High_Out := dwAlarm_Warnings_High_Out OR 16#00000004; END_IF;
IF (rVoted_ExportMoisture_Out >= rSet_AT501_H) THEN
    dwAlarm_Warnings_High_Out := dwAlarm_Warnings_High_Out OR 16#00000008; END_IF;
IF (rTEG_ReboilerTemp_TT503_In >= rSet_TT503_H) THEN
    dwAlarm_Warnings_High_Out := dwAlarm_Warnings_High_Out OR 16#00000010; END_IF;
IF (rContactor_FoamIndex >= rSet_Foam_H) THEN
    dwAlarm_Warnings_High_Out := dwAlarm_Warnings_High_Out OR 16#00000020; END_IF;
IF (rInterstageTemp_TT102_In >= 52.0) THEN
    dwAlarm_Warnings_High_Out := dwAlarm_Warnings_High_Out OR 16#00000040; END_IF;
IF (rStage3DischargeTemp_TT201_In >= 148.0) THEN
    dwAlarm_Warnings_High_Out := dwAlarm_Warnings_High_Out OR 16#00000080; END_IF;
IF (rVessel_TiltAngle >= 5.0) THEN
    dwAlarm_Warnings_High_Out := dwAlarm_Warnings_High_Out OR 16#00000100; END_IF;
IF (ABS(rFPSO_HeaveAccel_In) >= 2.0) THEN
    dwAlarm_Warnings_High_Out := dwAlarm_Warnings_High_Out OR 16#00000200; END_IF;
IF (rDemister_CarryoverRisk >= 1.50) THEN
    dwAlarm_Warnings_High_Out := dwAlarm_Warnings_High_Out OR 16#00000400; END_IF;
IF (rGyro_PrecessionBearingLoad >= 15.0) THEN
    dwAlarm_Warnings_High_Out := dwAlarm_Warnings_High_Out OR 16#00000800; END_IF;
IF (NOT bTMR_PT101_HealthyA) OR (NOT bTMR_PT101_HealthyB) OR (NOT bTMR_PT101_HealthyC) THEN
    dwAlarm_Warnings_High_Out := dwAlarm_Warnings_High_Out OR 16#00001000; END_IF;
IF (NOT bTMR_PT201_HealthyA) OR (NOT bTMR_PT201_HealthyB) OR (NOT bTMR_PT201_HealthyC) THEN
    dwAlarm_Warnings_High_Out := dwAlarm_Warnings_High_Out OR 16#00002000; END_IF;
IF (NOT bTMR_PDT301_HealthyA) OR (NOT bTMR_PDT301_HealthyB) OR (NOT bTMR_PDT301_HealthyC) THEN
    dwAlarm_Warnings_High_Out := dwAlarm_Warnings_High_Out OR 16#00004000; END_IF;
IF (NOT bTMR_VT401_HealthyA) OR (NOT bTMR_VT401_HealthyB) OR (NOT bTMR_VT401_HealthyC) THEN
    dwAlarm_Warnings_High_Out := dwAlarm_Warnings_High_Out OR 16#00008000; END_IF;
IF (NOT bTMR_AT501_HealthyA) OR (NOT bTMR_AT501_HealthyB) OR (NOT bTMR_AT501_HealthyC) THEN
    dwAlarm_Warnings_High_Out := dwAlarm_Warnings_High_Out OR 16#00010000; END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * SUBSECTION 5.6: 32-BIT BIT-PACKED ISA-18.2 LOW WARNING ALARM DWORD TELEMETRY
 * --------------------------------------------------------------------------------------------------------------------- *)
dwAlarm_Warnings_Low_Out := 16#00000000;
IF (rVoted_SuctionPres_Out <= rSet_PT101_L) THEN
    dwAlarm_Warnings_Low_Out := dwAlarm_Warnings_Low_Out OR 16#00000001; END_IF;
IF (rVoted_DischargePres_Out <= rSet_PT201_L) THEN
    dwAlarm_Warnings_Low_Out := dwAlarm_Warnings_Low_Out OR 16#00000002; END_IF;
IF (rSurgeMargin_Stg1 <= rSet_Surge_L) THEN
    dwAlarm_Warnings_Low_Out := dwAlarm_Warnings_Low_Out OR 16#00000004; END_IF;
IF (rSurgeMargin_Stg2 <= rSet_Surge_L) THEN
    dwAlarm_Warnings_Low_Out := dwAlarm_Warnings_Low_Out OR 16#00000008; END_IF;
IF (rSurgeMargin_Stg3 <= rSet_Surge_L) THEN
    dwAlarm_Warnings_Low_Out := dwAlarm_Warnings_Low_Out OR 16#00000010; END_IF;
IF (rLubeOilPres_PT601_In <= rSet_PT601_L) THEN
    dwAlarm_Warnings_Low_Out := dwAlarm_Warnings_Low_Out OR 16#00000020; END_IF;
IF (rSealGasDP_PDT701_In <= rSet_PDT701_L) THEN
    dwAlarm_Warnings_Low_Out := dwAlarm_Warnings_Low_Out OR 16#00000040; END_IF;
IF (rTEG_ReboilerTemp_TT503_In <= rSet_TT503_L) THEN
    dwAlarm_Warnings_Low_Out := dwAlarm_Warnings_Low_Out OR 16#00000080; END_IF;
IF (rTEG_ContactorPres_PT502_In <= 110.0) THEN
    dwAlarm_Warnings_Low_Out := dwAlarm_Warnings_Low_Out OR 16#00000100; END_IF;
IF (rTEG_LeanFlow_FT501_In <= 12.0) THEN
    dwAlarm_Warnings_Low_Out := dwAlarm_Warnings_Low_Out OR 16#00000200; END_IF;
IF (rVoted_SuctionDP_Out <= 60.0) THEN
    dwAlarm_Warnings_Low_Out := dwAlarm_Warnings_Low_Out OR 16#00000400; END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * SUBSECTION 5.7: 32-BIT BIT-PACKED FSM & TMR HEALTH STATUS WORDS
 * --------------------------------------------------------------------------------------------------------------------- *)
(* FSM Telemetry: Lower 16 bits = State Number; Upper 16 bits = Lifecycle Booleans *)
dwStatus_FSM_State_Out := INT_TO_DWORD(iFSM_State);
IF bTrain_Pressurized      THEN dwStatus_FSM_State_Out := dwStatus_FSM_State_Out OR 16#00010000; END_IF;
IF bWarmup_Completed       THEN dwStatus_FSM_State_Out := dwStatus_FSM_State_Out OR 16#00020000; END_IF;
IF bLubeOil_Normal         THEN dwStatus_FSM_State_Out := dwStatus_FSM_State_Out OR 16#00040000; END_IF;
IF bSealGas_Normal         THEN dwStatus_FSM_State_Out := dwStatus_FSM_State_Out OR 16#00080000; END_IF;
IF bCompressor_AtIdle      THEN dwStatus_FSM_State_Out := dwStatus_FSM_State_Out OR 16#00100000; END_IF;
IF bCompressor_AtFullSpeed THEN dwStatus_FSM_State_Out := dwStatus_FSM_State_Out OR 16#00200000; END_IF;
IF bTEG_SystemLocked       THEN dwStatus_FSM_State_Out := dwStatus_FSM_State_Out OR 16#00400000; END_IF;
IF bExport_Synchronized    THEN dwStatus_FSM_State_Out := dwStatus_FSM_State_Out OR 16#00800000; END_IF;
IF bEDP_Active             THEN dwStatus_FSM_State_Out := dwStatus_FSM_State_Out OR 16#01000000; END_IF;
IF bSystem_Trip_Latched_Out THEN dwStatus_FSM_State_Out := dwStatus_FSM_State_Out OR 16#02000000; END_IF;

(* 2oo3 Sensor Group Health Bitmask (15 individual channels) *)
dwStatus_TMR_Health_Out := 16#00000000;
IF bTMR_PT101_HealthyA  THEN dwStatus_TMR_Health_Out := dwStatus_TMR_Health_Out OR 16#00000001; END_IF;
IF bTMR_PT101_HealthyB  THEN dwStatus_TMR_Health_Out := dwStatus_TMR_Health_Out OR 16#00000002; END_IF;
IF bTMR_PT101_HealthyC  THEN dwStatus_TMR_Health_Out := dwStatus_TMR_Health_Out OR 16#00000004; END_IF;
IF bTMR_PT201_HealthyA  THEN dwStatus_TMR_Health_Out := dwStatus_TMR_Health_Out OR 16#00000008; END_IF;
IF bTMR_PT201_HealthyB  THEN dwStatus_TMR_Health_Out := dwStatus_TMR_Health_Out OR 16#00000010; END_IF;
IF bTMR_PT201_HealthyC  THEN dwStatus_TMR_Health_Out := dwStatus_TMR_Health_Out OR 16#00000020; END_IF;
IF bTMR_PDT301_HealthyA THEN dwStatus_TMR_Health_Out := dwStatus_TMR_Health_Out OR 16#00000040; END_IF;
IF bTMR_PDT301_HealthyB THEN dwStatus_TMR_Health_Out := dwStatus_TMR_Health_Out OR 16#00000080; END_IF;
IF bTMR_PDT301_HealthyC THEN dwStatus_TMR_Health_Out := dwStatus_TMR_Health_Out OR 16#00000100; END_IF;
IF bTMR_VT401_HealthyA  THEN dwStatus_TMR_Health_Out := dwStatus_TMR_Health_Out OR 16#00000200; END_IF;
IF bTMR_VT401_HealthyB  THEN dwStatus_TMR_Health_Out := dwStatus_TMR_Health_Out OR 16#00000400; END_IF;
IF bTMR_VT401_HealthyC  THEN dwStatus_TMR_Health_Out := dwStatus_TMR_Health_Out OR 16#00000800; END_IF;
IF bTMR_AT501_HealthyA  THEN dwStatus_TMR_Health_Out := dwStatus_TMR_Health_Out OR 16#00001000; END_IF;
IF bTMR_AT501_HealthyB  THEN dwStatus_TMR_Health_Out := dwStatus_TMR_Health_Out OR 16#00002000; END_IF;
IF bTMR_AT501_HealthyC  THEN dwStatus_TMR_Health_Out := dwStatus_TMR_Health_Out OR 16#00004000; END_IF;

(* Actuator & Solenoid Telemetry Word *)
dwStatus_Actuator_Flags_Out := 16#00000000;
IF bEDP_HP_FlareValve_Open_Out THEN dwStatus_Actuator_Flags_Out := dwStatus_Actuator_Flags_Out OR 16#00000001; END_IF;
IF bEDP_LP_FlareValve_Open_Out THEN dwStatus_Actuator_Flags_Out := dwStatus_Actuator_Flags_Out OR 16#00000002; END_IF;
IF bInfeed_Isolation_Close_Out THEN dwStatus_Actuator_Flags_Out := dwStatus_Actuator_Flags_Out OR 16#00000004; END_IF;
IF bExport_Isolation_Close_Out THEN dwStatus_Actuator_Flags_Out := dwStatus_Actuator_Flags_Out OR 16#00000008; END_IF;
IF bVFD_EmergencyTrip_Out      THEN dwStatus_Actuator_Flags_Out := dwStatus_Actuator_Flags_Out OR 16#00000010; END_IF;
IF bLubeOil_AuxPump_Start_Out  THEN dwStatus_Actuator_Flags_Out := dwStatus_Actuator_Flags_Out OR 16#00000020; END_IF;

END_FUNCTION_BLOCK
"""
