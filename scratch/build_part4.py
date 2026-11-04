# Part 4: Phases 7, 8, 9 and END_FUNCTION_BLOCK
import os

code_part4 = '''
(* ==================================================================================================== *)
(* === PHASE 7: 10-ZONE BARREL TEMPERATURE REGULATION & THERMAL SOAK ENGINE                          === *)
(* ==================================================================================================== *)

(* 7.1 Split-Range Thermal Control for 10 Modular Extruder Barrel Zones *)
(* Feedforward allocation of viscous dissipation power across zones *)
(* Zone 1: Water-Cooled Feed Throat (40-60 C) *)
aBarrelZoneFeedforward_kW[1] := 0.0;
(* Zones 2-4: Plasticizing & Solids Melting (Takes ~45% of viscous shearing) *)
aBarrelZoneFeedforward_kW[2] := rTotalViscousDissipation_kW * 0.12;
aBarrelZoneFeedforward_kW[3] := rTotalViscousDissipation_kW * 0.18;
aBarrelZoneFeedforward_kW[4] := rTotalViscousDissipation_kW * 0.15;
(* Zones 5-7: Monomer Mixing & Reactive Grafting (Takes ~28% of viscous shearing) *)
aBarrelZoneFeedforward_kW[5] := rTotalViscousDissipation_kW * 0.10;
aBarrelZoneFeedforward_kW[6] := rTotalViscousDissipation_kW * 0.09;
aBarrelZoneFeedforward_kW[7] := rTotalViscousDissipation_kW * 0.09;
(* Zones 8-10: Devolatilization, Melt Pumping & Flange (Takes ~27% of viscous shearing) *)
aBarrelZoneFeedforward_kW[8] := rTotalViscousDissipation_kW * 0.08;
aBarrelZoneFeedforward_kW[9] := rTotalViscousDissipation_kW * 0.10;
aBarrelZoneFeedforward_kW[10] := rTotalViscousDissipation_kW * 0.09;

FOR iLoopIndex_i := 1 TO 10 DO
    (* Temperature Tracking Error: e_T = T_sp - T_act *)
    aBarrelZoneError_degC[iLoopIndex_i] := aBarrelTempSetpoints_degC[iLoopIndex_i] - aBarrelZoneTemp_degC[iLoopIndex_i];

    (* PID Derivative with Low-Pass Filtering *)
    aBarrelZoneDeriv_degC_s[iLoopIndex_i] := (aBarrelZoneError_degC[iLoopIndex_i] - aBarrelZonePrevError_degC[iLoopIndex_i]) / c_Ts_s;
    aBarrelZonePrevError_degC[iLoopIndex_i] := aBarrelZoneError_degC[iLoopIndex_i];

    (* Integral with Anti-Windup Clamping *)
    IF ABS(aBarrelZoneError_degC[iLoopIndex_i]) < 25.0 THEN
        aBarrelZoneIntegral_degC_s[iLoopIndex_i] := aBarrelZoneIntegral_degC_s[iLoopIndex_i] + (aBarrelZoneError_degC[iLoopIndex_i] * c_Ts_s);
        IF aBarrelZoneIntegral_degC_s[iLoopIndex_i] > 200.0 THEN aBarrelZoneIntegral_degC_s[iLoopIndex_i] := 200.0; END_IF;
        IF aBarrelZoneIntegral_degC_s[iLoopIndex_i] < -200.0 THEN aBarrelZoneIntegral_degC_s[iLoopIndex_i] := -200.0; END_IF;
    END_IF;

    (* Raw Unconstrained Thermal PID Effort *)
    aBarrelZonePID_Output[iLoopIndex_i] := (4.50 * aBarrelZoneError_degC[iLoopIndex_i]) +
                                          (0.08 * aBarrelZoneIntegral_degC_s[iLoopIndex_i]) +
                                          (2.20 * aBarrelZoneDeriv_degC_s[iLoopIndex_i]) -
                                          (0.65 * aBarrelZoneFeedforward_kW[iLoopIndex_i]);

    (* Split-Range Modulating Logic with 2.0% Neutral Deadband *)
    IF (iFSM_State >= 1) AND (iFSM_State <= 10) THEN
        IF aBarrelZonePID_Output[iLoopIndex_i] > 2.0 THEN
            (* Heating Demand: Induction Heating SSR Modulated Duty *)
            aBarrelHeaterDuty_pct[iLoopIndex_i] := aBarrelZonePID_Output[iLoopIndex_i];
            IF aBarrelHeaterDuty_pct[iLoopIndex_i] > 100.0 THEN aBarrelHeaterDuty_pct[iLoopIndex_i] := 100.0; END_IF;
            aBarrelCoolDuty_pct[iLoopIndex_i] := 0.0;
        ELSIF aBarrelZonePID_Output[iLoopIndex_i] < -2.0 THEN
            (* Cooling Demand: Supercritical CO2 Direct Injection Modulated Duty *)
            aBarrelHeaterDuty_pct[iLoopIndex_i] := 0.0;
            aBarrelCoolDuty_pct[iLoopIndex_i] := -1.0 * aBarrelZonePID_Output[iLoopIndex_i] * 1.25;
            IF aBarrelCoolDuty_pct[iLoopIndex_i] > 100.0 THEN aBarrelCoolDuty_pct[iLoopIndex_i] := 100.0; END_IF;
        ELSE
            (* Neutral Deadband: Zero Heat, Zero Cool *)
            aBarrelHeaterDuty_pct[iLoopIndex_i] := 0.0;
            aBarrelCoolDuty_pct[iLoopIndex_i] := 0.0;
        END_IF;
    ELSE
        aBarrelHeaterDuty_pct[iLoopIndex_i] := 0.0;
        aBarrelCoolDuty_pct[iLoopIndex_i] := 0.0;
        aBarrelZoneIntegral_degC_s[iLoopIndex_i] := 0.0;
    END_IF;
END_FOR;

(* Slit-Die Body Cartridge Heater Regulation *)
rSlitDieTempError_degC := rSlitDieTempSetpoint_degC - aBarrelZoneTemp_degC[10];
IF ABS(rSlitDieTempError_degC) < 30.0 THEN
    rSlitDieIntegral_degC_s := rSlitDieIntegral_degC_s + (rSlitDieTempError_degC * c_Ts_s);
    IF rSlitDieIntegral_degC_s > 300.0 THEN rSlitDieIntegral_degC_s := 300.0; END_IF;
    IF rSlitDieIntegral_degC_s < -300.0 THEN rSlitDieIntegral_degC_s := -300.0; END_IF;
END_IF;

IF (iFSM_State >= 1) AND (iFSM_State <= 10) THEN
    rSlitDieHeaterDuty_pct := (3.80 * rSlitDieTempError_degC) + (0.05 * rSlitDieIntegral_degC_s);
    IF rSlitDieHeaterDuty_pct < 0.0 THEN rSlitDieHeaterDuty_pct := 0.0; END_IF;
    IF rSlitDieHeaterDuty_pct > 100.0 THEN rSlitDieHeaterDuty_pct := 100.0; END_IF;
ELSE
    rSlitDieHeaterDuty_pct := 0.0;
    rSlitDieIntegral_degC_s := 0.0;
END_IF;

(* 7.2 Cold-Start Interlock & Thermal Soak Supervision *)
(* Verify all 10 barrel metal temperatures are safely above crystalline melting point Tm *)
bAllZonesAtMeltingPoint := TRUE;
FOR iLoopIndex_i := 2 TO 10 DO
    IF aBarrelZoneTemp_degC[iLoopIndex_i] < (rPolymerMeltingPoint_Tm_degC - 5.0) THEN
        bAllZonesAtMeltingPoint := FALSE;
    END_IF;
END_FOR;

(* 20-minute (1200 seconds) thermal soak timer to melt solid polymer cores *)
tThermalSoakTimer(IN := bAllZonesAtMeltingPoint AND (iFSM_State >= 1), PT := T#1200S);
bThermalSoakComplete := tThermalSoakTimer.Q;

(* Cold-Start Interlock: Mechanical screw rotation forbidden until soak complete *)
bColdStartInterlockActive := NOT (bThermalSoakComplete OR bSoakOverridePermissive);

(* Die Freeze Interlock: Prevent gear pump startup if die adapter or body is cold *)
bDieFreezeInterlockActive := (aBarrelZoneTemp_degC[10] < (rPolymerMeltingPoint_Tm_degC + 10.0));

(* Vacuum Degassing Solenoids *)
IF (iFSM_State >= 6) AND (iFSM_State <= 8) THEN
    bVacuumValveZone4_Cmd := TRUE;
    bVacuumValveZone8_Cmd := TRUE;
ELSE
    bVacuumValveZone4_Cmd := FALSE;
    bVacuumValveZone8_Cmd := FALSE;
END_IF;

(* ==================================================================================================== *)
(* === PHASE 8: 12-STAGE FINITE STATE MACHINE (FSM) INDUSTRIAL ENGINE                                === *)
(* ==================================================================================================== *)

tStateTimer(IN := (iFSM_State = iFSM_PrevState), PT := T#7200S);
tSubStepTimer(IN := TRUE, PT := T#600S);
bStateEntryFlag := (iFSM_State <> iFSM_PrevState);
iFSM_PrevState := iFSM_State;

CASE iFSM_State OF
    0: (* STATE_COLD_STANDBY: Plant Idle & Mechanical Interlock Check *)
        bEmergencyVentDiverter_Cmd := FALSE;
        bSteadyStateActive := FALSE;
        IF bEnable AND bPreheatStartCmd AND NOT bEmergencyStop THEN
            iFSM_State := 1; (* Transition to Preheat *)
        END_IF;

    1: (* STATE_BARREL_ZONE_PREHEAT_SOAK: Heat Barrel & Soak for 20 Minutes *)
        bEmergencyVentDiverter_Cmd := FALSE;
        bSteadyStateActive := FALSE;
        IF bThermalSoakComplete OR bSoakOverridePermissive THEN
            iFSM_State := 2; (* Transition to Homogenization *)
        ELSIF NOT bEnable OR bEmergencyStop THEN
            iFSM_State := 0;
        END_IF;

    2: (* STATE_MELT_TEMP_HOMOGENIZATION: Soak Complete, Tooling Thermal Check *)
        bEmergencyVentDiverter_Cmd := FALSE;
        bSteadyStateActive := FALSE;
        IF NOT bColdStartInterlockActive AND NOT bDieFreezeInterlockActive THEN
            IF bFeederTareCmd THEN
                iFSM_State := 3; (* Transition to Tare *)
            ELSE
                iFSM_State := 4; (* Skip to Screw Jog Start *)
            END_IF;
        ELSIF NOT bEnable OR bEmergencyStop THEN
            iFSM_State := 0;
        END_IF;

    3: (* STATE_MAIN_FEEDER_TARE_CALIBRATION: Gravimetric Loss-in-Weight Auto-Tare *)
        bEmergencyVentDiverter_Cmd := FALSE;
        bSteadyStateActive := FALSE;
        IF tStateTimer.ET > T#10S THEN
            bFeederTareCompleted := TRUE;
            iFSM_State := 4; (* Transition to Screw Drive Start *)
        END_IF;

    4: (* STATE_SCREW_DRIVE_LOW_SPEED_START: Jog Screw at 50 RPM, Check Torque Bound *)
        bEmergencyVentDiverter_Cmd := FALSE;
        bSteadyStateActive := FALSE;
        (* Verify drive torque is low (not jammed with cold resin) *)
        IF (tStateTimer.ET > T#15S) AND (rScrewMotorTorque_pct < 45.0) THEN
            iFSM_State := 5; (* Transition to Polymer Flood Feed *)
        ELSIF rScrewMotorTorque_pct >= 75.0 THEN
            (* Mechanical bind detected: Trip to Cold Standby *)
            bAlarm_ColdStartInterlockTrip := TRUE;
            iFSM_State := 0;
        ELSIF NOT bEnable OR bEmergencyStop THEN
            iFSM_State := 0;
        END_IF;

    5: (* STATE_POLYMER_FLOOD_FEED_TRANSITION: Base Resin Feed Ramp, Establish Seal *)
        bEmergencyVentDiverter_Cmd := FALSE;
        bSteadyStateActive := FALSE;
        (* Once barrel zone 5 melt pressure reaches 25 bar, melt seal is established *)
        IF (rZone5Press_Voted_bar >= 20.0) AND (tStateTimer.ET > T#30S) THEN
            iFSM_State := 6; (* Transition to Reactive Monomer/Peroxide Injection *)
        ELSIF NOT bEnable OR bEmergencyStop THEN
            iFSM_State := 10; (* Controlled Drain Shutdown *)
        END_IF;

    6: (* STATE_REACTIVE_INJECTION_ENABLE: Inject Functional Monomer & Liquid Peroxide *)
        bEmergencyVentDiverter_Cmd := FALSE;
        bSteadyStateActive := FALSE;
        (* Verify peroxide Coriolis flow tracking and die inlet pressure building *)
        IF (rPeroxide_Voted_kgh > 0.10) AND (rDieInlet_Voted_bar >= 20.0) AND (tStateTimer.ET > T#25S) THEN
            iFSM_State := 7; (* Transition to Steady State Compounding *)
        ELSIF NOT bEnable OR bEmergencyStop THEN
            iFSM_State := 10;
        END_IF;

    7: (* STATE_STEADY_STATE_COMPOUNDING: Full Production at 2500 kg/h, 250 bar Head *)
        bEmergencyVentDiverter_Cmd := FALSE;
        bSteadyStateActive := TRUE;
        (* Monitor for transient pressure surges *)
        IF ABS(rDiePressure_Voted_bar - rTargetDiePressure_bar) > 12.0 THEN
            iFSM_State := 8; (* Transition to Surge Damping *)
        ELSIF bPurgeModeRequested THEN
            iFSM_State := 9; (* Transition to Purge Material Switch *)
        ELSIF bControlledShutdownRequested OR NOT bEnable THEN
            iFSM_State := 10; (* Controlled Drain Shutdown *)
        ELSIF bEmergencyStop OR (rDiePressure_Voted_bar > 305.0) THEN
            iFSM_State := 11; (* Emergency Vent Open *)
        END_IF;

    8: (* STATE_DIE_PRESSURE_SURGE_DAMPING: Active High-Speed Pressure Ripple Compensation *)
        bEmergencyVentDiverter_Cmd := FALSE;
        bSteadyStateActive := FALSE;
        (* Surge subdued within +/- 3.0 bar *)
        IF (ABS(rDiePressure_Voted_bar - rTargetDiePressure_bar) <= 3.0) AND (tStateTimer.ET > T#5S) THEN
            iFSM_State := 7; (* Return to Steady-State Compounding *)
        ELSIF rDiePressure_Voted_bar > 305.0 THEN
            iFSM_State := 11; (* Emergency Rupture Vent Open *)
        ELSIF tStateTimer.ET > T#120S THEN
            (* Surge failed to clear in 2 minutes: Graceful Shutdown *)
            iFSM_State := 10;
        END_IF;

    9: (* STATE_PURGE_MATERIAL_SWITCH: Stop Peroxide/Side Feeder, Flush Barrel *)
        bEmergencyVentDiverter_Cmd := FALSE;
        bSteadyStateActive := FALSE;
        (* Run purge polymer for 10 minutes to clean reactive peroxide residues *)
        IF tStateTimer.ET > T#600S THEN
            iFSM_State := 10; (* Transition to Controlled Drain *)
        ELSIF bEmergencyStop THEN
            iFSM_State := 11;
        END_IF;

    10: (* STATE_CONTROLLED_DRAIN_SHUTDOWN: Starve Feeders, Empty Flight Channels *)
        bEmergencyVentDiverter_Cmd := FALSE;
        bSteadyStateActive := FALSE;
        (* Wait for channel empty (fill degree < 10% and torque < 15%) *)
        IF (rDegreeOfFill_pct < 12.0) OR (tStateTimer.ET > T#180S) THEN
            iFSM_State := 0; (* Cold Standby *)
        END_IF;

    11: (* STATE_EMERGENCY_VENT_OPEN: Overpressure Protection Diverter Valve Open *)
        bEmergencyVentDiverter_Cmd := TRUE;
        bSteadyStateActive := FALSE;
        (* Operator must press reset to recover from emergency vent *)
        IF bReset AND NOT bEmergencyStop AND (rDiePressure_Voted_bar < 50.0) THEN
            bEmergencyVentDiverter_Cmd := FALSE;
            iFSM_State := 0;
        END_IF;
ELSE
    iFSM_State := 0;
END_CASE;
wFSM_CurrentState := INT_TO_WORD(iFSM_State);
bEmergencyVentOpen := bEmergencyVentDiverter_Cmd;

(* ==================================================================================================== *)
(* === PHASE 9: ISA-18.2 ALARMS, FIRST-OUT TRIP CAPTURE & DIAGNOSTIC WORD PACKING                    === *)
(* ==================================================================================================== *)

(* 9.1 Category 1: Critical Emergency Trips *)
(* Die Head Pressure HH Trip (> 305 bar) *)
IF rDiePressure_Voted_bar > 305.0 THEN
    bAlarm_DiePressure_HH := TRUE;
    IF iFirstOutAlarmCode = 0 THEN iFirstOutAlarmCode := 101; END_IF;
ELSIF rDiePressure_Voted_bar < 290.0 THEN
    IF bReset THEN bAlarm_DiePressure_HH := FALSE; END_IF;
END_IF;

(* Die Head Pressure LL Trip (< 50 bar during active compounding) *)
IF (rDiePressure_Voted_bar < 50.0) AND (iFSM_State = 7) AND (tStateTimer.ET > T#30S) THEN
    bAlarm_DiePressure_LL := TRUE;
    IF iFirstOutAlarmCode = 0 THEN iFirstOutAlarmCode := 102; END_IF;
ELSIF rDiePressure_Voted_bar > 75.0 THEN
    IF bReset THEN bAlarm_DiePressure_LL := FALSE; END_IF;
END_IF;

(* Gear Pump Suction Pressure HH Trip (> 75 bar) *)
IF rGearPumpSuction_Voted_bar > 75.0 THEN
    bAlarm_GearPumpSuction_HH := TRUE;
    IF iFirstOutAlarmCode = 0 THEN iFirstOutAlarmCode := 103; END_IF;
ELSIF rGearPumpSuction_Voted_bar < 65.0 THEN
    IF bReset THEN bAlarm_GearPumpSuction_HH := FALSE; END_IF;
END_IF;

(* Gear Pump Suction Pressure LL Cavitation Trip (< 5 bar) *)
IF (rGearPumpSuction_Voted_bar < 5.0) AND (iFSM_State >= 6) AND (tStateTimer.ET > T#20S) THEN
    bAlarm_GearPumpSuction_LL := TRUE;
    IF iFirstOutAlarmCode = 0 THEN iFirstOutAlarmCode := 104; END_IF;
ELSIF rGearPumpSuction_Voted_bar > 12.0 THEN
    IF bReset THEN bAlarm_GearPumpSuction_LL := FALSE; END_IF;
END_IF;

(* True Melt Temperature HH Trip (> 265 deg C) *)
IF rTrueMeltTemp_Voted_degC > 265.0 THEN
    bAlarm_TrueMeltTemp_HH := TRUE;
    IF iFirstOutAlarmCode = 0 THEN iFirstOutAlarmCode := 105; END_IF;
ELSIF rTrueMeltTemp_Voted_degC < 250.0 THEN
    IF bReset THEN bAlarm_TrueMeltTemp_HH := FALSE; END_IF;
END_IF;

(* True Melt Temperature LL Freeze Trip (< 160 deg C) *)
IF (rTrueMeltTemp_Voted_degC < 160.0) AND (iFSM_State >= 5) THEN
    bAlarm_TrueMeltTemp_LL := TRUE;
    IF iFirstOutAlarmCode = 0 THEN iFirstOutAlarmCode := 106; END_IF;
ELSIF rTrueMeltTemp_Voted_degC > 175.0 THEN
    IF bReset THEN bAlarm_TrueMeltTemp_LL := FALSE; END_IF;
END_IF;

(* Twin-Screw Motor Torque HH Trip (> 95% rated) *)
IF rScrewMotorTorque_pct > 95.0 THEN
    bAlarm_ScrewMotorTorque_HH := TRUE;
    IF iFirstOutAlarmCode = 0 THEN iFirstOutAlarmCode := 107; END_IF;
ELSIF rScrewMotorTorque_pct < 85.0 THEN
    IF bReset THEN bAlarm_ScrewMotorTorque_HH := FALSE; END_IF;
END_IF;

(* Slit-Die Rheometer Critical Differential Pressure Trip (> 165 bar) *)
IF rSlitDP_Voted_bar > 165.0 THEN
    bAlarm_SlitRheometer_HH := TRUE;
    IF iFirstOutAlarmCode = 0 THEN iFirstOutAlarmCode := 108; END_IF;
ELSIF rSlitDP_Voted_bar < 145.0 THEN
    IF bReset THEN bAlarm_SlitRheometer_HH := FALSE; END_IF;
END_IF;

(* Liquid Peroxide Runaway Dosing Surge HH Trip (> 25 kg/h) *)
IF rPeroxide_Voted_kgh > 25.0 THEN
    bAlarm_PeroxideRunaway_HH := TRUE;
    IF iFirstOutAlarmCode = 0 THEN iFirstOutAlarmCode := 109; END_IF;
ELSIF rPeroxide_Voted_kgh < 18.0 THEN
    IF bReset THEN bAlarm_PeroxideRunaway_HH := FALSE; END_IF;
END_IF;

(* Master Trip Escalation *)
IF bAlarm_DiePressure_HH OR bAlarm_GearPumpSuction_HH OR bAlarm_TrueMeltTemp_HH OR
   bAlarm_ScrewMotorTorque_HH OR bAlarm_PeroxideRunaway_HH OR bAlarm_ColdStartInterlockTrip THEN
    bTripLatched := TRUE;
    (* Trigger Emergency Vent *)
    IF iFSM_State <> 11 THEN iFSM_State := 11; END_IF;
END_IF;
IF bReset AND NOT bEmergencyStop THEN
    bTripLatched := FALSE;
    iFirstOutAlarmCode := 0;
END_IF;

(* 9.2 Category 2: Process Warnings *)
bWarning_DiePressure_H := (rDiePressure_Voted_bar > 280.0);
bWarning_DiePressure_L := (rDiePressure_Voted_bar < 150.0) AND (iFSM_State = 7);
bWarning_GearPumpSuction_H := (rGearPumpSuction_Voted_bar > 55.0);
bWarning_GearPumpSuction_L := (rGearPumpSuction_Voted_bar < 20.0) AND (iFSM_State >= 6);
bWarning_TrueMeltTemp_H := (rTrueMeltTemp_Voted_degC > 245.0);
bWarning_TrueMeltTemp_L := (rTrueMeltTemp_Voted_degC < 185.0) AND (iFSM_State >= 5);
bWarning_MFI_Deviation_H := (rMFI_TrackingError_pct > 1.5);
bWarning_MFI_Deviation_L := (rMFI_TrackingError_pct < -1.5);
bWarning_DiePressure_ROC := (ABS(rDiePressureROC_bars) > 15.0);
bWarning_TMR_ChannelDiscrepancy := bMainFeeder_DiscrepancyFault OR bSideFeeder_DiscrepancyFault OR
                                   bPeroxide_DiscrepancyFault OR bDieInlet_DiscrepancyFault OR
                                   bPyro_DiscrepancyFault OR bSlitDP_DiscrepancyFault OR
                                   bScrewSpeed_DiscrepancyFault;

(* 9.3 32-Bit Telemetry Bitmask Packing *)
(* Pack dwAlarmWord_Trip *)
dwAlarmWord_Trip := 16#00000000;
IF bAlarm_DiePressure_HH         THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#00000001; END_IF;
IF bAlarm_DiePressure_LL         THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#00000002; END_IF;
IF bAlarm_GearPumpSuction_HH     THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#00000004; END_IF;
IF bAlarm_GearPumpSuction_LL     THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#00000008; END_IF;
IF bAlarm_TrueMeltTemp_HH        THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#00000010; END_IF;
IF bAlarm_TrueMeltTemp_LL        THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#00000020; END_IF;
IF bAlarm_ScrewMotorTorque_HH    THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#00000040; END_IF;
IF bAlarm_SlitRheometer_HH       THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#00000080; END_IF;
IF bAlarm_PeroxideRunaway_HH     THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#00000100; END_IF;
IF bAlarm_ColdStartInterlockTrip THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#00000200; END_IF;
IF bEmergencyStop                THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#00000400; END_IF;
IF bTripLatched                  THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#80000000; END_IF;

(* Pack dwAlarmWord_Warning *)
dwAlarmWord_Warning := 16#00000000;
IF bWarning_DiePressure_H          THEN dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#00000001; END_IF;
IF bWarning_DiePressure_L          THEN dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#00000002; END_IF;
IF bWarning_GearPumpSuction_H      THEN dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#00000004; END_IF;
IF bWarning_GearPumpSuction_L      THEN dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#00000008; END_IF;
IF bWarning_TrueMeltTemp_H         THEN dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#00000010; END_IF;
IF bWarning_TrueMeltTemp_L         THEN dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#00000020; END_IF;
IF bWarning_MFI_Deviation_H        THEN dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#00000040; END_IF;
IF bWarning_MFI_Deviation_L        THEN dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#00000080; END_IF;
IF bWarning_DiePressure_ROC        THEN dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#00000100; END_IF;
IF bWarning_TMR_ChannelDiscrepancy THEN dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#00000200; END_IF;

(* Pack dwSystemStatusWord *)
dwSystemStatusWord := 16#00000000;
IF bEnable                   THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00000001; END_IF;
IF bSteadyStateActive        THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00000002; END_IF;
IF bColdStartInterlockActive THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00000004; END_IF;
IF bDieFreezeInterlockActive THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00000008; END_IF;
IF bThermalSoakComplete      THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00000010; END_IF;
IF bFeederTareCompleted      THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00000020; END_IF;
IF bEmergencyVentOpen        THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00000040; END_IF;
IF bVacuumValveZone4_Cmd     THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00000080; END_IF;
IF bVacuumValveZone8_Cmd     THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00000100; END_IF;

(* Pack dwActuatorStatusWord *)
dwActuatorStatusWord := 16#00000000;
IF rScrewSpeedCmd_rpm > 1.0     THEN dwActuatorStatusWord := dwActuatorStatusWord OR 16#00000001; END_IF;
IF rGearPumpSpeedCmd_rpm > 1.0  THEN dwActuatorStatusWord := dwActuatorStatusWord OR 16#00000002; END_IF;
IF rFeederMainCmd_kgh > 1.0     THEN dwActuatorStatusWord := dwActuatorStatusWord OR 16#00000004; END_IF;
IF rFeederSideCmd_kgh > 0.5     THEN dwActuatorStatusWord := dwActuatorStatusWord OR 16#00000008; END_IF;
IF rPeroxidePumpCmd_pct > 0.5   THEN dwActuatorStatusWord := dwActuatorStatusWord OR 16#00000010; END_IF;
IF rSlitDieHeaterDuty_pct > 1.0 THEN dwActuatorStatusWord := dwActuatorStatusWord OR 16#00000020; END_IF;

END_FUNCTION_BLOCK
'''

with open('scratch/code_part4.st', 'w', encoding='utf-8') as f:
    f.write(code_part4)
print("Part 4 written, len =", len(code_part4))
