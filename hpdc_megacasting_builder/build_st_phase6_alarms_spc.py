# hpdc_megacasting_builder/build_st_phase6_alarms_spc.py

def get_phase6_alarms_spc():
    return """(* =====================================================================================================================
 * PHASE 6: ISA-18.2 MULTI-TIER ALARMS, STATISTICAL PROCESS CONTROL (SPC) & BIT-PACKED TELEMETRY
 * ===================================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------------------------
 * 1. ISA-18.2 ALARM TRIP POINTS & CLEARANCE DEADBANDS
 * --------------------------------------------------------------------------------------------------------------------- *)
(* Shot Cylinder Head Pressure Alarms (PT-101) *)
IF rTMR_PT101_Voted >= rLim_PT101_HH THEN
    bAlarm_HeadPres_HH := TRUE;
ELSIF rTMR_PT101_Voted < (rLim_PT101_HH - rAlarm_Deadband_Pres) THEN
    bAlarm_HeadPres_HH := FALSE;
END_IF;

IF rTMR_PT101_Voted >= rLim_PT101_H THEN
    bAlarm_HeadPres_H := TRUE;
ELSIF rTMR_PT101_Voted < (rLim_PT101_H - rAlarm_Deadband_Pres) THEN
    bAlarm_HeadPres_H := FALSE;
END_IF;

IF (rTMR_PT101_Voted <= rLim_PT101_L) AND (iFSM_CurrentState >= 5) AND (iFSM_CurrentState <= 7) THEN
    bAlarm_HeadPres_L := TRUE;
ELSIF rTMR_PT101_Voted > (rLim_PT101_L + rAlarm_Deadband_Pres) THEN
    bAlarm_HeadPres_L := FALSE;
END_IF;

IF (rTMR_PT101_Voted <= rLim_PT101_LL) AND (iFSM_CurrentState >= 5) AND (iFSM_CurrentState <= 7) THEN
    bAlarm_HeadPres_LL := TRUE;
ELSIF rTMR_PT101_Voted > (rLim_PT101_LL + rAlarm_Deadband_Pres) THEN
    bAlarm_HeadPres_LL := FALSE;
END_IF;

(* Nitrogen Accumulator Pre-Charge Pressure (PT-501) *)
IF rTMR_PT501_Voted <= rLim_PT501_Accum_LL THEN
    bAlarm_AccumPres_LowTrip := TRUE;
ELSIF rTMR_PT501_Voted > (rLim_PT501_Accum_LL + rAlarm_Deadband_Pres) THEN
    bAlarm_AccumPres_LowTrip := FALSE;
END_IF;

(* Plunger Velocity Overshoot / Flashing Hazard *)
IF rFiltVelocity >= rLim_Vel_HH THEN
    bAlarm_Velocity_Overshoot := TRUE;
END_IF;

(* Thermal Die Steel Hot Spot Check across all 12 zones *)
bAlarm_Die_HotSpot := FALSE;
FOR iZone_Loop := 1 TO 12 DO
    IF rDieTemp_Current[iZone_Loop] >= rLim_DieTemp_HH THEN
        bAlarm_Die_HotSpot := TRUE;
    END_IF;
END_FOR;

(* Biscuit Thickness Out-of-Tolerance Evaluation *)
IF (rBiscuit_Thickness_mm > 0.0) AND ((rBiscuit_Thickness_mm < rSpec_Biscuit_LSL) OR (rBiscuit_Thickness_mm > rSpec_Biscuit_USL)) THEN
    bAlarm_Biscuit_OutRange := TRUE;
ELSE
    bAlarm_Biscuit_OutRange := FALSE;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * 2. STATISTICAL PROCESS CONTROL (SPC) ROLLING 30-SHOT METRIC EVALUATION
 * --------------------------------------------------------------------------------------------------------------------- *)
(* Trigger SPC Update on One-Shot Entry into State 13 (Spray / Part Verified Complete) *)
IF (iFSM_CurrentState = 13) AND bFSM_StateFirstScan THEN

    (* Insert Newest Shot Data into Circular Buffer Array *)
    arrSPC_Biscuit_History[iSPC_BufferIndex]  := rBiscuit_Thickness_mm;
    arrSPC_PeakVel_History[iSPC_BufferIndex]  := rPeakVelocityRecorded;
    arrSPC_RiseTime_History[iSPC_BufferIndex] := rIntensRiseTimeAchieved_ms;
    arrSPC_PeakPres_History[iSPC_BufferIndex] := rPeakIntensPresRecorded;

    iSPC_BufferIndex := iSPC_BufferIndex + 1;
    IF iSPC_BufferIndex > 30 THEN
        iSPC_BufferIndex := 1;
    END_IF;

    (* Compute Sample Mean for Solidified Biscuit Thickness *)
    rMatMul_Sum := 0.0;
    FOR iSPC_Loop := 1 TO 30 DO
        rMatMul_Sum := rMatMul_Sum + arrSPC_Biscuit_History[iSPC_Loop];
    END_FOR;
    rSPC_Biscuit_Mean := rMatMul_Sum / 30.0;

    (* Compute Sample Variance and Standard Deviation (Sigma) *)
    rMatMul_Sum := 0.0;
    FOR iSPC_Loop := 1 TO 30 DO
        rMatMul_Sum := rMatMul_Sum + ((arrSPC_Biscuit_History[iSPC_Loop] - rSPC_Biscuit_Mean)
                                      * (arrSPC_Biscuit_History[iSPC_Loop] - rSPC_Biscuit_Mean));
    END_FOR;
    rSPC_Biscuit_Variance := rMatMul_Sum / 29.0;
    IF rSPC_Biscuit_Variance > 0.0001 THEN
        rSPC_Biscuit_StdDev := SQRT(rSPC_Biscuit_Variance);
    ELSE
        rSPC_Biscuit_StdDev := 0.010;
    END_IF;

    (* Compute Process Capability Indices Cp and Cpk *)
    IF rSPC_Biscuit_StdDev > 0.0001 THEN
        rSPC_Biscuit_Cp := (rSpec_Biscuit_USL - rSpec_Biscuit_LSL) / (6.0 * rSPC_Biscuit_StdDev);

        (* Cpk = MIN((USL - Mean) / (3*Sigma), (Mean - LSL) / (3*Sigma)) *)
        IF ((rSpec_Biscuit_USL - rSPC_Biscuit_Mean) / (3.0 * rSPC_Biscuit_StdDev))
           < ((rSPC_Biscuit_Mean - rSpec_Biscuit_LSL) / (3.0 * rSPC_Biscuit_StdDev)) THEN
            rSPC_Biscuit_Cpk := (rSpec_Biscuit_USL - rSPC_Biscuit_Mean) / (3.0 * rSPC_Biscuit_StdDev);
        ELSE
            rSPC_Biscuit_Cpk := (rSPC_Biscuit_Mean - rSpec_Biscuit_LSL) / (3.0 * rSPC_Biscuit_StdDev);
        END_IF;
    END_IF;

    (* Determine Automotive Casting Quality Acceptance vs Scrap Reject *)
    IF (rBiscuit_Thickness_mm >= rSpec_Biscuit_LSL) AND (rBiscuit_Thickness_mm <= rSpec_Biscuit_USL)
       AND (rIntensRiseTimeAchieved_ms <= rSpec_RiseTime_Max)
       AND (rPeakIntensPresRecorded >= rSpec_PeakPres_Min)
       AND (rCavityVacuum_AtShot_Out <= rSpec_Vacuum_Max)
       AND (NOT bTieBar_TonnageImbalance) THEN
        bPartQuality_Accept_Out := TRUE;
        bPartQuality_Scrap_Out  := FALSE;
    ELSE
        bPartQuality_Accept_Out := FALSE;
        bPartQuality_Scrap_Out  := TRUE;
    END_IF;

END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * 3. 32-BIT BIT-PACKED DIAGNOSTIC & TELEMETRY REGISTERS
 * --------------------------------------------------------------------------------------------------------------------- *)
(* Register 1: dwStatus_FSM_Phase_Out *)
dwReg_FSM := 16#00000000;
dwReg_FSM := dwReg_FSM OR INT_TO_DWORD(iFSM_CurrentState AND 16#000F);
IF bCycleRunning THEN dwReg_FSM := dwReg_FSM OR 16#00000010; END_IF;
IF bVacuum_Pump_Start_Out THEN dwReg_FSM := dwReg_FSM OR 16#00000020; END_IF;
IF bChillVent_SealValve_Out THEN dwReg_FSM := dwReg_FSM OR 16#00000040; END_IF;
IF bCoreA_Extended_LS_In AND bCoreB_Extended_LS_In THEN dwReg_FSM := dwReg_FSM OR 16#00000080; END_IF;
IF bLadle_Robot_Home_In THEN dwReg_FSM := dwReg_FSM OR 16#00000100; END_IF;
IF bExtract_Robot_Clear_In THEN dwReg_FSM := dwReg_FSM OR 16#00000200; END_IF;
IF bSpray_Robot_Clear_In THEN dwReg_FSM := dwReg_FSM OR 16#00000400; END_IF;
IF bSafetyGate_Front_Closed_In AND bSafetyGate_Rear_Closed_In THEN dwReg_FSM := dwReg_FSM OR 16#00000800; END_IF;
IF rTMR_PT501_Voted >= rLim_PT501_Accum_L THEN dwReg_FSM := dwReg_FSM OR 16#00001000; END_IF;
dwStatus_FSM_Phase_Out := dwReg_FSM;

(* Register 2: dwStatus_Motion_State_Out *)
dwReg_Motion := 16#00000000;
IF ABS(rFiltVelocity) > 0.05 THEN dwReg_Motion := dwReg_Motion OR 16#00000001; END_IF;
IF iFSM_CurrentState = 3 THEN dwReg_Motion := dwReg_Motion OR 16#00000002; END_IF;
IF iFSM_CurrentState = 5 THEN dwReg_Motion := dwReg_Motion OR 16#00000004; END_IF;
IF iFSM_CurrentState = 6 THEN dwReg_Motion := dwReg_Motion OR 16#00000008; END_IF;
IF rEjector_Position_In > 5.0 THEN dwReg_Motion := dwReg_Motion OR 16#00000010; END_IF;
IF rTMR_LC601_Voted >= (rRecipe_TargetClampForce_In * 0.90) THEN dwReg_Motion := dwReg_Motion OR 16#00000020; END_IF;
IF NOT bTieBar_TonnageImbalance THEN dwReg_Motion := dwReg_Motion OR 16#00000040; END_IF;
IF (iPWM_CycleCounter_ms MOD 20) < 10 THEN dwReg_Motion := dwReg_Motion OR 16#00000080; END_IF;
dwStatus_Motion_State_Out := dwReg_Motion;

(* Register 3: dwAlarm_Critical_Trips_Out *)
dwReg_CritTrip := 16#00000000;
IF NOT bEmergency_Stop_OK_In THEN dwReg_CritTrip := dwReg_CritTrip OR 16#00000001; END_IF;
IF NOT bSafetyGate_Front_Closed_In THEN dwReg_CritTrip := dwReg_CritTrip OR 16#00000002; END_IF;
IF NOT bSafetyGate_Rear_Closed_In THEN dwReg_CritTrip := dwReg_CritTrip OR 16#00000004; END_IF;
IF bAlarm_HeadPres_HH THEN dwReg_CritTrip := dwReg_CritTrip OR 16#00000008; END_IF;
IF bAlarm_AccumPres_LowTrip THEN dwReg_CritTrip := dwReg_CritTrip OR 16#00000010; END_IF;
IF bAlarm_Velocity_Overshoot THEN dwReg_CritTrip := dwReg_CritTrip OR 16#00000020; END_IF;
IF bAlarm_TMR_MajorDegrade THEN dwReg_CritTrip := dwReg_CritTrip OR 16#00000040; END_IF;
IF bTieBar_TonnageImbalance THEN dwReg_CritTrip := dwReg_CritTrip OR 16#00000080; END_IF;
IF bAccumulator_Dump_Safe_Out THEN dwReg_CritTrip := dwReg_CritTrip OR 16#00000100; END_IF;
IF bAlarm_EmergencyStop_Active THEN dwReg_CritTrip := dwReg_CritTrip OR 16#00000200; END_IF;
dwAlarm_Critical_Trips_Out := dwReg_CritTrip;

(* Register 4: dwAlarm_Warnings_Out *)
dwReg_Warning := 16#00000000;
IF bAlarm_HeadPres_H THEN dwReg_Warning := dwReg_Warning OR 16#00000001; END_IF;
IF bAlarm_HeadPres_L THEN dwReg_Warning := dwReg_Warning OR 16#00000002; END_IF;
IF rTMR_PT501_Voted < rLim_PT501_Accum_L THEN dwReg_Warning := dwReg_Warning OR 16#00000004; END_IF;
IF bAlarm_Vacuum_NotAchieved THEN dwReg_Warning := dwReg_Warning OR 16#00000008; END_IF;
IF bAlarm_Intens_TooSlow THEN dwReg_Warning := dwReg_Warning OR 16#00000010; END_IF;
IF bAlarm_Die_HotSpot THEN dwReg_Warning := dwReg_Warning OR 16#00000020; END_IF;
IF bAlarm_Biscuit_OutRange THEN dwReg_Warning := dwReg_Warning OR 16#00000040; END_IF;
dwAlarm_Warnings_Out := dwReg_Warning;

(* Register 5: dwTMR_Sensor_Health_Out *)
dwReg_TMRHealth := 16#00000000;
IF bTMR_PT101_HealthyA THEN dwReg_TMRHealth := dwReg_TMRHealth OR 16#00000001; END_IF;
IF bTMR_PT101_HealthyB THEN dwReg_TMRHealth := dwReg_TMRHealth OR 16#00000002; END_IF;
IF bTMR_PT101_HealthyC THEN dwReg_TMRHealth := dwReg_TMRHealth OR 16#00000004; END_IF;
IF bTMR_PT201_HealthyA THEN dwReg_TMRHealth := dwReg_TMRHealth OR 16#00000008; END_IF;
IF bTMR_PT201_HealthyB THEN dwReg_TMRHealth := dwReg_TMRHealth OR 16#00000010; END_IF;
IF bTMR_PT201_HealthyC THEN dwReg_TMRHealth := dwReg_TMRHealth OR 16#00000020; END_IF;
IF bTMR_ENC301_HealthyA THEN dwReg_TMRHealth := dwReg_TMRHealth OR 16#00000040; END_IF;
IF bTMR_ENC301_HealthyB THEN dwReg_TMRHealth := dwReg_TMRHealth OR 16#00000080; END_IF;
IF bTMR_ENC301_HealthyC THEN dwReg_TMRHealth := dwReg_TMRHealth OR 16#00000100; END_IF;
IF bTMR_VPT401_HealthyA THEN dwReg_TMRHealth := dwReg_TMRHealth OR 16#00000200; END_IF;
IF bTMR_VPT401_HealthyB THEN dwReg_TMRHealth := dwReg_TMRHealth OR 16#00000400; END_IF;
IF bTMR_VPT401_HealthyC THEN dwReg_TMRHealth := dwReg_TMRHealth OR 16#00000800; END_IF;
IF bTMR_PT501_HealthyA THEN dwReg_TMRHealth := dwReg_TMRHealth OR 16#00001000; END_IF;
IF bTMR_PT501_HealthyB THEN dwReg_TMRHealth := dwReg_TMRHealth OR 16#00002000; END_IF;
IF bTMR_PT501_HealthyC THEN dwReg_TMRHealth := dwReg_TMRHealth OR 16#00004000; END_IF;
IF bTMR_LC601_HealthyA THEN dwReg_TMRHealth := dwReg_TMRHealth OR 16#00008000; END_IF;
IF bTMR_LC601_HealthyB THEN dwReg_TMRHealth := dwReg_TMRHealth OR 16#00010000; END_IF;
IF bTMR_LC601_HealthyC THEN dwReg_TMRHealth := dwReg_TMRHealth OR 16#00020000; END_IF;
IF bTMR_TT701_HealthyA THEN dwReg_TMRHealth := dwReg_TMRHealth OR 16#00040000; END_IF;
IF bTMR_TT701_HealthyB THEN dwReg_TMRHealth := dwReg_TMRHealth OR 16#00080000; END_IF;
IF bTMR_TT701_HealthyC THEN dwReg_TMRHealth := dwReg_TMRHealth OR 16#00100000; END_IF;
dwTMR_Sensor_Health_Out := dwReg_TMRHealth;

(* Register 6: dwSPC_Quality_Flags_Out *)
dwReg_Quality := 16#00000000;
IF bPartQuality_Accept_Out THEN dwReg_Quality := dwReg_Quality OR 16#00000001; END_IF;
IF bPartQuality_Scrap_Out THEN dwReg_Quality := dwReg_Quality OR 16#00000002; END_IF;
IF rBiscuit_Thickness_mm > rSpec_Biscuit_USL THEN dwReg_Quality := dwReg_Quality OR 16#00000004; END_IF;
IF (rBiscuit_Thickness_mm < rSpec_Biscuit_LSL) AND (rBiscuit_Thickness_mm > 0.0) THEN dwReg_Quality := dwReg_Quality OR 16#00000008; END_IF;
IF rPeakVelocityRecorded < (rRecipe_Phase2_Velocity_In * 0.85) THEN dwReg_Quality := dwReg_Quality OR 16#00000010; END_IF;
IF rIntensRiseTimeAchieved_ms > rSpec_RiseTime_Max THEN dwReg_Quality := dwReg_Quality OR 16#00000020; END_IF;
IF rPeakIntensPresRecorded < rSpec_PeakPres_Min THEN dwReg_Quality := dwReg_Quality OR 16#00000040; END_IF;
IF rCavityVacuum_AtShot_Out > rSpec_Vacuum_Max THEN dwReg_Quality := dwReg_Quality OR 16#00000080; END_IF;
IF rSPC_Biscuit_Cpk < 1.33 THEN dwReg_Quality := dwReg_Quality OR 16#00000100; END_IF;
dwSPC_Quality_Flags_Out := dwReg_Quality;

END_FUNCTION_BLOCK
"""
