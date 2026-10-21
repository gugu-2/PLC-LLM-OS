# -*- coding: utf-8 -*-
"""
Part 4B: Sections 6-9 of implementation logic for FB_GeothermalKalina_AmmoniaWater_ExpansionTurbine
"""

part4_logic_b = """(* ----------------------------------------------------------------------------------------- *)
(* 6.0 VARIABLE-GEOMETRY RADIAL INFLOW TURBINE (VGRIT) GOVERNOR TUNING & VGV MODULATION     *)
(* Coordinates nozzle guide vanes and throttle governor for synchronous grid generation.    *)
(* ----------------------------------------------------------------------------------------- *)
(* 6.1 Aerodynamic Tip-to-Spouting Velocity Ratio (u / c0) Calculation *)
(* Isentropic Enthalpy Drop across Expander: *)
IF rVotedTurbineExhaustPress > 0.5 THEN
    rAerodynamicPressureRatio := rVotedTurbineInletPress / rVotedTurbineExhaustPress;
ELSE
    rAerodynamicPressureRatio := 6.5;
END_IF;

IF rAerodynamicPressureRatio > 1.2 THEN
    (* Ideal enthalpy drop approximation for zeotropic ammonia-water mixture: *)
    rIsentropicExhaustEnthalpy := rVaporEnthalpy_kJ_kg * (1.0 - (0.245 * (1.0 - (1.0 / EXPT(rAerodynamicPressureRatio, 0.285)))));
    rSpoutingVelocity_c0 := SQRT(2.0 * ABS(rVaporEnthalpy_kJ_kg - rIsentropicExhaustEnthalpy) * 1000.0);
ELSE
    rSpoutingVelocity_c0 := 300.0;
END_IF;

(* Impeller Tip Speed: u = pi * D_rotor * N / 60 *)
rRotorBladeTipSpeed_u := (3.14159265 * c_rTurbineRotorDiameter * rVotedTurbineSpeed) / 60.0;

IF rSpoutingVelocity_c0 > 10.0 THEN
    rTurbineVelocityRatio_u_c0 := rRotorBladeTipSpeed_u / rSpoutingVelocity_c0;
ELSE
    rTurbineVelocityRatio_u_c0 := 0.70;
END_IF;

(* Real-Time Isentropic Efficiency Estimation *)
IF (rVaporEnthalpy_kJ_kg - rIsentropicExhaustEnthalpy) > 1.0 THEN
    rTurbineIsentropicEff := ((rVaporEnthalpy_kJ_kg - rTurbineExhaustEnthalpy_kJ_kg) /
                             (rVaporEnthalpy_kJ_kg - rIsentropicExhaustEnthalpy)) * 100.0;
    IF rTurbineIsentropicEff > 91.5 THEN rTurbineIsentropicEff := 91.5; END_IF;
    IF rTurbineIsentropicEff < 40.0 THEN rTurbineIsentropicEff := 40.0; END_IF;
ELSE
    rTurbineIsentropicEff := 75.0;
END_IF;

(* 6.2 Aerodynamic Optimal Variable Guide Vane (VGV) Feedforward Schedule *)
(* Target velocity ratio is 0.705. VGV position adjusts throat area to maintain design u/c0 *)
rScheduledVanePosition := 42.0 + (3.8 * rAerodynamicPressureRatio) + (18.0 * (rTurbineVelocityRatio_u_c0 - rOptimalNozzleVelocityRatio));
IF rScheduledVanePosition > 100.0 THEN rScheduledVanePosition := 100.0; ELSIF rScheduledVanePosition < 15.0 THEN rScheduledVanePosition := 15.0; END_IF;

(* 6.3 Synchronous Speed Governor with 4.0% Grid Frequency Droop *)
IF bBypassGovernorDroop OR NOT bGridBreakerClosed THEN
    rDroopSpeedOffset_rpm := 0.0; (* Isochronous speed regulation prior to grid synchronization *)
ELSE
    (* Standard Droop: Delta_N = - Droop * (f_grid - f_nom) / f_nom * N_rated *)
    rDroopSpeedOffset_rpm := - (rDroopRegulationFactor * ((rGridFrequency_Hz - 50.0) / 50.0) * c_rRatedTurbineSpeed);
    IF rDroopSpeedOffset_rpm > 350.0 THEN rDroopSpeedOffset_rpm := 350.0; ELSIF rDroopSpeedOffset_rpm < -350.0 THEN rDroopSpeedOffset_rpm := -350.0; END_IF;
END_IF;

(* Compute Composite Speed Reference with Active Droop *)
IF iState = 70 THEN
    (* Accelerating from turning gear to rated synchronous speed *)
    IF rGovernorSpeedRef_rpm < c_rRatedTurbineSpeed THEN
        rGovernorSpeedRef_rpm := rGovernorSpeedRef_rpm + (25.0 * c_rScanTime_Ts * 20.0); (* 500 rpm/min ramp *)
    ELSE
        rGovernorSpeedRef_rpm := c_rRatedTurbineSpeed;
    END_IF;
ELSIF iState >= 80 THEN
    rGovernorSpeedRef_rpm := c_rRatedTurbineSpeed + rDroopSpeedOffset_rpm;
ELSE
    rGovernorSpeedRef_rpm := 0.0;
END_IF;

(* PID Error Calculation *)
rGovernorSpeedError_rpm := rGovernorSpeedRef_rpm - rVotedTurbineSpeed;

(* Derivative with 1st-Order Low-Pass Filter *)
rGovernorDerivativeFiltered := (0.80 * rGovernorDerivativeFiltered) +
                               (0.20 * ((rGovernorSpeedError_rpm - rGovernorDerivativePrevError) / c_rScanTime_Ts));
rGovernorDerivativePrevError := rGovernorSpeedError_rpm;

(* Integral with Anti-Windup Clamping *)
IF NOT bGovernorAntiWindupActive THEN
    rGovernorIntegralAccum := rGovernorIntegralAccum + (rGovernorSpeedError_rpm * c_rScanTime_Ts);
    IF rGovernorIntegralAccum > 3000.0 THEN rGovernorIntegralAccum := 3000.0; ELSIF rGovernorIntegralAccum < -3000.0 THEN rGovernorIntegralAccum := -3000.0; END_IF;
END_IF;

(* Unclamped PID Output *)
rGovernorPID_Out := (rGovernorKp * rGovernorSpeedError_rpm) +
                    (rGovernorKi * rGovernorIntegralAccum) +
                    (rGovernorKd * rGovernorDerivativeFiltered);

(* Check Anti-Windup Condition *)
IF (rGovernorPID_Out > 100.0 AND rGovernorSpeedError_rpm > 0.0) OR
   (rGovernorPID_Out < 0.0 AND rGovernorSpeedError_rpm < 0.0) THEN
    bGovernorAntiWindupActive := TRUE;
ELSE
    bGovernorAntiWindupActive := FALSE;
END_IF;

(* Apply Throttle Governor Output and Decouple Fast Bypass *)
IF iState >= 70 AND NOT bSystemTrip THEN
    IF rGovernorPID_Out > 100.0 THEN
        rTurbineThrottleValve_Cmd := 100.0;
    ELSIF rGovernorPID_Out < 0.0 THEN
        rTurbineThrottleValve_Cmd := 0.0;
    ELSE
        rTurbineThrottleValve_Cmd := rGovernorPID_Out;
    END_IF;
    (* Fast Bypass Closes Inversely as Throttle Opens to Protect Evaporator Pressure *)
    rTurbineBypassValve_Cmd := 100.0 - rTurbineThrottleValve_Cmd;
    bEmergencyStopValve_Trip := TRUE; (* Solenoid Energized / Valve Open *)
ELSE
    rTurbineThrottleValve_Cmd := 0.0;
    rTurbineBypassValve_Cmd := 100.0;
    bEmergencyStopValve_Trip := FALSE; (* Trip Solenoid De-Energized *)
END_IF;

(* Guide Vane Command Synthesis *)
IF bMPC_Active AND (iState = 90) THEN
    (* Guide Vane Commanded by MPC with Scheduled Feedforward *)
    rVanePitchAngle_Cmd := rScheduledVanePosition + rDelta_u1_Vane;
ELSIF iState >= 70 THEN
    rVanePitchAngle_Cmd := rScheduledVanePosition;
ELSE
    rVanePitchAngle_Cmd := 15.0; (* Minimum Opening for Purge/Warmup *)
END_IF;

IF rVanePitchAngle_Cmd > 100.0 THEN rVanePitchAngle_Cmd := 100.0; ELSIF rVanePitchAngle_Cmd < 15.0 THEN rVanePitchAngle_Cmd := 15.0; END_IF;

(* Governor Synchronized Flag Evaluation *)
IF (ABS(rVotedTurbineSpeed - c_rRatedTurbineSpeed) < 30.0) AND (iState >= 80) THEN
    bGovernorSynchronized := TRUE;
ELSE
    bGovernorSynchronized := FALSE;
END_IF;

(* ----------------------------------------------------------------------------------------- *)
(* 7.0 RECUPERATOR & PREHEATER CONDENSATION FLOAT BALANCE CONTROL                            *)
(* Multi-element float balance to prevent vapor blow-through and liquid carry-over.          *)
(* ----------------------------------------------------------------------------------------- *)
(* 7.1 High-Temperature Recuperator (HTR) Float Control *)
rHTR_LevelError := rVotedHTR_FloatLevel - 50.0;
rHTR_LevelIntegral := rHTR_LevelIntegral + (rHTR_LevelError * c_rScanTime_Ts);
IF rHTR_LevelIntegral > 200.0 THEN rHTR_LevelIntegral := 200.0; ELSIF rHTR_LevelIntegral < -200.0 THEN rHTR_LevelIntegral := -200.0; END_IF;

rHTR_DrainValveDemand := (rHTR_LevelKp * rHTR_LevelError) + (rHTR_LevelKi * rHTR_LevelIntegral) + 50.0;
IF rVotedHTR_FloatLevel < 15.0 THEN
    rHTR_DrainFloatValve_Cmd := 0.0; (* Anti-Vapor Blowthrough Cutoff *)
    dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0040; (* HTR Low-Low Level Alarm *)
ELSIF rVotedHTR_FloatLevel > 85.0 THEN
    rHTR_DrainFloatValve_Cmd := 100.0; (* High Level Flood Dump *)
    dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0080; (* HTR High-High Level Alarm *)
ELSE
    dwAlarmWord1 := dwAlarmWord1 AND NOT 16#0000_00C0;
    IF rHTR_DrainValveDemand > 100.0 THEN rHTR_DrainFloatValve_Cmd := 100.0;
    ELSIF rHTR_DrainValveDemand < 0.0 THEN rHTR_DrainFloatValve_Cmd := 0.0;
    ELSE rHTR_DrainFloatValve_Cmd := rHTR_DrainValveDemand; END_IF;
END_IF;

(* 7.2 Low-Temperature Recuperator (LTR) Float Control *)
rLTR_LevelError := rVotedLTR_FloatLevel - 50.0;
rLTR_LevelIntegral := rLTR_LevelIntegral + (rLTR_LevelError * c_rScanTime_Ts);
IF rLTR_LevelIntegral > 200.0 THEN rLTR_LevelIntegral := 200.0; ELSIF rLTR_LevelIntegral < -200.0 THEN rLTR_LevelIntegral := -200.0; END_IF;

rLTR_DrainValveDemand := (rLTR_LevelKp * rLTR_LevelError) + (rLTR_LevelKi * rLTR_LevelIntegral) + 50.0;
IF rVotedLTR_FloatLevel < 15.0 THEN
    rLTR_DrainFloatValve_Cmd := 0.0;
    dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0100; (* LTR Low-Low Level Alarm *)
ELSIF rVotedLTR_FloatLevel > 85.0 THEN
    rLTR_DrainFloatValve_Cmd := 100.0;
    dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0200; (* LTR High-High Level Alarm *)
ELSE
    dwAlarmWord1 := dwAlarmWord1 AND NOT 16#0000_0300;
    IF rLTR_DrainValveDemand > 100.0 THEN rLTR_DrainFloatValve_Cmd := 100.0;
    ELSIF rLTR_DrainValveDemand < 0.0 THEN rLTR_DrainFloatValve_Cmd := 0.0;
    ELSE rLTR_DrainFloatValve_Cmd := rLTR_DrainValveDemand; END_IF;
END_IF;

(* 7.3 Evaporator Preheater Condensate Float Control *)
rPreheaterLevelError := rVotedPreheaterFloatLevel - 50.0;
rPreheaterLevelIntegral := rPreheaterLevelIntegral + (rPreheaterLevelError * c_rScanTime_Ts);
IF rPreheaterLevelIntegral > 200.0 THEN rPreheaterLevelIntegral := 200.0; ELSIF rPreheaterLevelIntegral < -200.0 THEN rPreheaterLevelIntegral := -200.0; END_IF;

rPreheaterDrainValveDemand := (rPreheaterLevelKp * rPreheaterLevelError) + (rPreheaterLevelKi * rPreheaterLevelIntegral) + 50.0;
IF rVotedPreheaterFloatLevel < 15.0 THEN
    rPreheaterDrainValve_Cmd := 0.0;
    dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0400; (* Preheater Low-Low Level Alarm *)
ELSIF rVotedPreheaterFloatLevel > 85.0 THEN
    rPreheaterDrainValve_Cmd := 100.0;
    dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0800; (* Preheater High-High Level Alarm *)
ELSE
    dwAlarmWord1 := dwAlarmWord1 AND NOT 16#0000_0C00;
    IF rPreheaterDrainValveDemand > 100.0 THEN rPreheaterDrainValve_Cmd := 100.0;
    ELSIF rPreheaterDrainValveDemand < 0.0 THEN rPreheaterDrainValve_Cmd := 0.0;
    ELSE rPreheaterDrainValve_Cmd := rPreheaterDrainValveDemand; END_IF;
END_IF;

(* 7.4 Condenser Hotwell Condensate Float Control & Pump Speed Demand *)
rHotwellLevelError := rVotedHotwellFloatLevel - rTargetHotwellLevel;
rHotwellLevelIntegral := rHotwellLevelIntegral + (rHotwellLevelError * c_rScanTime_Ts);
IF rHotwellLevelIntegral > 300.0 THEN rHotwellLevelIntegral := 300.0; ELSIF rHotwellLevelIntegral < -300.0 THEN rHotwellLevelIntegral := -300.0; END_IF;

rHotwellPumpDemand := (rHotwellLevelKp * rHotwellLevelError) + (rHotwellLevelKi * rHotwellLevelIntegral) + 55.0;

IF bMPC_Active AND (iState = 90) THEN
    rCondensatePumpSpeed_Cmd := rHotwellPumpDemand + rDelta_u4_CondPump;
ELSE
    rCondensatePumpSpeed_Cmd := rHotwellPumpDemand;
END_IF;

IF rCondensatePumpSpeed_Cmd > 100.0 THEN rCondensatePumpSpeed_Cmd := 100.0;
ELSIF rCondensatePumpSpeed_Cmd < 20.0 THEN rCondensatePumpSpeed_Cmd := 20.0; END_IF;

(* ----------------------------------------------------------------------------------------- *)
(* 8.0 NON-CONDENSABLE GAS (NCG) PURGE VACUUM LOCK SEQUENCE CONTROLLER                       *)
(* Differential-pressure lock-hopper sub-state machine to evacuate incondensable gases.      *)
(* ----------------------------------------------------------------------------------------- *)
(* Calculate NCG Partial Pressure Fraction in Condenser Shell: *)
(* Saturation pressure of ammonia-water at condenser return temperature: *)
rCondenserSatTemp := rCoolingWaterReturnTemp + 4.5;
rAmmoniaPartialPressureEst := 125.0 + (10.5 * rCondenserSatTemp) + (0.28 * rCondenserSatTemp * rCondenserSatTemp);
rNCGPartialPressureDiff := rVotedCondenserPressure - rAmmoniaPartialPressureEst;

IF rVotedCondenserPressure > 10.0 THEN
    rNCGAccumulationIndex := (ABS(rNCGPartialPressureDiff) / rVotedCondenserPressure) * 100.0;
ELSE
    rNCGAccumulationIndex := 0.0;
END_IF;

(* Auto-Trigger NCG Purge when Incondensable Overpressure exceeds 35 kPa or Manual Command *)
IF (rNCGPartialPressureDiff > 35.0 OR bManualNCGPurgeTrigger) AND NOT bNCGPurgeCycleActive AND NOT bSystemTrip THEN
    bNCGPurgeCycleActive := TRUE;
    iNCG_State := 10; (* Start Isolation *)
    tNCG_Timer := 0.0;
END_IF;

CASE iNCG_State OF
    0: (* IDLE MONITORING *)
        rNCGLockInletValve_Cmd := 0.0;
        rNCGLockVentValve_Cmd := 0.0;
        bNCGVacuumPump_Run := FALSE;
        bNCGScrubberPump_Run := FALSE;
        tNCG_Timer := 0.0;

    10: (* ISOLATE LOCK CHAMBER *)
        (* Ensure inlet and vent valves are tightly sealed *)
        rNCGLockInletValve_Cmd := 0.0;
        rNCGLockVentValve_Cmd := 0.0;
        bNCGVacuumPump_Run := FALSE;
        bNCGScrubberPump_Run := TRUE; (* Start scrubber water recirculation spray *)
        tNCG_Timer := tNCG_Timer + c_rScanTime_Ts;
        IF tNCG_Timer >= 5.0 THEN
            iNCG_State := 20; (* Proceed to Chamber Evacuation *)
            tNCG_Timer := 0.0;
        END_IF;

    20: (* EVACUATE LOCK CHAMBER *)
        (* Run liquid-ring vacuum pump to pull chamber down below 8 kPa *)
        bNCGVacuumPump_Run := TRUE;
        tNCG_Timer := tNCG_Timer + c_rScanTime_Ts;
        IF (rVotedNCGLockPressure <= rLockChamberTargetVacuum) OR (tNCG_Timer >= 30.0) THEN
            bNCGVacuumPump_Run := FALSE;
            iNCG_State := 30; (* Open Condenser Vapor Pocket Intake *)
            tNCG_Timer := 0.0;
        END_IF;

    30: (* DRAW NCG POCKET INTO LOCK CHAMBER *)
        (* Open modulating intake valve to allow gas pocket to equalize into vacuum lock *)
        rNCGLockInletValve_Cmd := 100.0;
        tNCG_Timer := tNCG_Timer + c_rScanTime_Ts;
        IF (rVotedNCGLockPressure >= (rVotedCondenserPressure - 15.0)) OR (tNCG_Timer >= 20.0) THEN
            rNCGLockInletValve_Cmd := 0.0; (* Re-isolate Lock Intake *)
            iNCG_State := 40; (* Scrub Residual Ammonia *)
            tNCG_Timer := 0.0;
        END_IF;

    40: (* SCRUB RESIDUAL AMMONIA WITH COLD WATER SPRAY *)
        (* Intense water washing to dissolve and absorb any co-extracted NH3 vapor *)
        bNCGScrubberPump_Run := TRUE;
        tNCG_Timer := tNCG_Timer + c_rScanTime_Ts;
        IF (rNCGAmmoniaVaporPPM < c_rMaxAllowableAmmoniaPPM) AND (tNCG_Timer >= 15.0) THEN
            iNCG_State := 50; (* Safe to Vent Purified NCG *)
            tNCG_Timer := 0.0;
        ELSIF tNCG_Timer >= 45.0 THEN
            (* Scrubbing timeout: NH3 still above OSHA limit *)
            bNCGScrubberHighAmmoniaTrip := TRUE;
            dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0008; (* Scrubber NH3 Breakthrough *)
            iNCG_State := 60; (* Abort Vent and Recycle *)
            tNCG_Timer := 0.0;
        END_IF;

    50: (* VENT PURIFIED NCG TO ATMOSPHERE *)
        rNCGLockVentValve_Cmd := 65.0;
        tNCG_Timer := tNCG_Timer + c_rScanTime_Ts;
        IF (rVotedNCGLockPressure <= 105.0) OR (tNCG_Timer >= 15.0) THEN
            rNCGLockVentValve_Cmd := 0.0;
            iNCG_State := 60; (* Purge Cycle Complete *)
            tNCG_Timer := 0.0;
        END_IF;

    60: (* RESET & DWELL *)
        rNCGLockInletValve_Cmd := 0.0;
        rNCGLockVentValve_Cmd := 0.0;
        bNCGVacuumPump_Run := FALSE;
        bNCGScrubberPump_Run := FALSE;
        iPurgeCycleCount := iPurgeCycleCount + 1;
        bNCGPurgeCycleActive := FALSE;
        iNCG_State := 0; (* Return to Idle Monitoring *)
        tNCG_Timer := 0.0;

END_CASE;

(* ----------------------------------------------------------------------------------------- *)
(* 9.0 DISCRETE STATE-SPACE MODEL & MODEL PREDICTIVE CONTROL (MPC) OPTIMIZATION              *)
(* Solves 6-state, 4-control quadratic cost optimization via projected gradient descent.     *)
(* ----------------------------------------------------------------------------------------- *)
(* 9.1 Normalized State Deviation Vector Computation *)
x1_ConcDev         := rVotedVaporAmmoniaConc - rTargetVaporConc;
x2_PressDev        := rVotedSeparatorPress - rTargetSeparatorPress;
x3_SpeedDev        := (rVotedTurbineSpeed * 0.1047197) - rTargetTurbineSpeedRadS; (* rpm to rad/s *)
x4_SepLevelDev     := rVotedSeparatorFloatLevel - rTargetSeparatorLevel;
x5_CondPressDev    := rVotedCondenserPressure - rTargetCondenserPress;
x6_HotwellLevelDev := rVotedHotwellFloatLevel - rTargetHotwellLevel;

(* 9.2 One-Step Ahead State Prediction: x_pred = Ad * x + Bd * u *)
x1_Pred := (Ad_11 * x1_ConcDev) + (Ad_12 * x2_PressDev) + (Ad_13 * x3_SpeedDev) + (Ad_14 * x4_SepLevelDev) + (Ad_15 * x5_CondPressDev) + (Ad_16 * x6_HotwellLevelDev) + (Bd_11 * rDelta_u1_Vane) + (Bd_12 * rDelta_u2_Reflux) + (Bd_13 * rDelta_u3_Brine) + (Bd_14 * rDelta_u4_CondPump);
x2_Pred := (Ad_21 * x1_ConcDev) + (Ad_22 * x2_PressDev) + (Ad_23 * x3_SpeedDev) + (Ad_24 * x4_SepLevelDev) + (Ad_25 * x5_CondPressDev) + (Ad_26 * x6_HotwellLevelDev) + (Bd_21 * rDelta_u1_Vane) + (Bd_22 * rDelta_u2_Reflux) + (Bd_23 * rDelta_u3_Brine) + (Bd_24 * rDelta_u4_CondPump);
x3_Pred := (Ad_31 * x1_ConcDev) + (Ad_32 * x2_PressDev) + (Ad_33 * x3_SpeedDev) + (Ad_34 * x4_SepLevelDev) + (Ad_35 * x5_CondPressDev) + (Ad_36 * x6_HotwellLevelDev) + (Bd_31 * rDelta_u1_Vane) + (Bd_32 * rDelta_u2_Reflux) + (Bd_33 * rDelta_u3_Brine) + (Bd_34 * rDelta_u4_CondPump);
x4_Pred := (Ad_41 * x1_ConcDev) + (Ad_42 * x2_PressDev) + (Ad_43 * x3_SpeedDev) + (Ad_44 * x4_SepLevelDev) + (Ad_45 * x5_CondPressDev) + (Ad_46 * x6_HotwellLevelDev) + (Bd_41 * rDelta_u1_Vane) + (Bd_42 * rDelta_u2_Reflux) + (Bd_43 * rDelta_u3_Brine) + (Bd_44 * rDelta_u4_CondPump);
x5_Pred := (Ad_51 * x1_ConcDev) + (Ad_52 * x2_PressDev) + (Ad_53 * x3_SpeedDev) + (Ad_54 * x4_SepLevelDev) + (Ad_55 * x5_CondPressDev) + (Ad_56 * x6_HotwellLevelDev) + (Bd_51 * rDelta_u1_Vane) + (Bd_52 * rDelta_u2_Reflux) + (Bd_53 * rDelta_u3_Brine) + (Bd_54 * rDelta_u4_CondPump);
x6_Pred := (Ad_61 * x1_ConcDev) + (Ad_62 * x2_PressDev) + (Ad_63 * x3_SpeedDev) + (Ad_64 * x4_SepLevelDev) + (Ad_65 * x5_CondPressDev) + (Ad_66 * x6_HotwellLevelDev) + (Bd_61 * rDelta_u1_Vane) + (Bd_62 * rDelta_u2_Reflux) + (Bd_63 * rDelta_u3_Brine) + (Bd_64 * rDelta_u4_CondPump);

(* 9.3 Predicted Process Output Estimation: y_pred = Cd * x_pred + Dd * u *)
y1_PredPower     := (Cd_11 * x1_Pred) + (Cd_12 * x2_Pred) + (Cd_13 * x3_Pred) + (Cd_14 * x4_Pred) + (Cd_15 * x5_Pred) + (Cd_16 * x6_Pred) + (Dd_11 * rDelta_u1_Vane);
y2_PredPress     := (Cd_21 * x1_Pred) + (Cd_22 * x2_Pred) + (Cd_23 * x3_Pred) + (Cd_24 * x4_Pred) + (Cd_25 * x5_Pred) + (Cd_26 * x6_Pred);
y3_PredSpeed     := (Cd_31 * x1_Pred) + (Cd_32 * x2_Pred) + (Cd_33 * x3_Pred) + (Cd_34 * x4_Pred) + (Cd_35 * x5_Pred) + (Cd_36 * x6_Pred);
y4_PredCondPress := (Cd_41 * x1_Pred) + (Cd_42 * x2_Pred) + (Cd_43 * x3_Pred) + (Cd_44 * x4_Pred) + (Cd_45 * x5_Pred) + (Cd_46 * x6_Pred);

(* 9.4 Analytical Quadratic Cost Gradient Vector: g = Bd' * Q * x + R_Delta * Delta_u *)
rGrad1 := (Bd_11 * rMPC_Weight_Conc * x1_ConcDev) +
          (Bd_21 * rMPC_Weight_Press * x2_PressDev) +
          (Bd_31 * rMPC_Weight_Speed * x3_SpeedDev) +
          (Bd_41 * rMPC_Weight_SepLevel * x4_SepLevelDev) +
          (Bd_51 * rMPC_Weight_CondPress * x5_CondPressDev) +
          (rMPC_Weight_dVane * rDelta_u1_Vane);

rGrad2 := (Bd_12 * rMPC_Weight_Conc * x1_ConcDev) +
          (Bd_22 * rMPC_Weight_Press * x2_PressDev) +
          (Bd_32 * rMPC_Weight_Speed * x3_SpeedDev) +
          (Bd_42 * rMPC_Weight_SepLevel * x4_SepLevelDev) +
          (rMPC_Weight_dReflux * rDelta_u2_Reflux);

rGrad3 := (Bd_13 * rMPC_Weight_Conc * x1_ConcDev) +
          (Bd_23 * rMPC_Weight_Press * x2_PressDev) +
          (Bd_33 * rMPC_Weight_Speed * x3_SpeedDev) +
          (Bd_43 * rMPC_Weight_SepLevel * x4_SepLevelDev) +
          (rMPC_Weight_dBrine * rDelta_u3_Brine);

rGrad4 := (Bd_24 * rMPC_Weight_Press * x2_PressDev) +
          (Bd_54 * rMPC_Weight_CondPress * x5_CondPressDev) +
          (Bd_64 * rMPC_Weight_HotwellLevel * x6_HotwellLevelDev) +
          (rMPC_Weight_dCondPump * rDelta_u4_CondPump);

(* 9.5 Approximate Diagonal Hessian Elements H_ii = sum(Bd_ji^2 * Q_j) + R_Delta_i *)
rHess11 := (Bd_11 * Bd_11 * rMPC_Weight_Conc) + (Bd_21 * Bd_21 * rMPC_Weight_Press) + (Bd_31 * Bd_31 * rMPC_Weight_Speed) + (Bd_41 * Bd_41 * rMPC_Weight_SepLevel) + (Bd_51 * Bd_51 * rMPC_Weight_CondPress) + rMPC_Weight_dVane;
rHess22 := (Bd_12 * Bd_12 * rMPC_Weight_Conc) + (Bd_22 * Bd_22 * rMPC_Weight_Press) + (Bd_32 * Bd_32 * rMPC_Weight_Speed) + (Bd_42 * Bd_42 * rMPC_Weight_SepLevel) + rMPC_Weight_dReflux;
rHess33 := (Bd_13 * Bd_13 * rMPC_Weight_Conc) + (Bd_23 * Bd_23 * rMPC_Weight_Press) + (Bd_33 * Bd_33 * rMPC_Weight_Speed) + (Bd_43 * Bd_43 * rMPC_Weight_SepLevel) + rMPC_Weight_dBrine;
rHess44 := (Bd_24 * Bd_24 * rMPC_Weight_Press) + (Bd_54 * Bd_54 * rMPC_Weight_CondPress) + (Bd_64 * Bd_64 * rMPC_Weight_HotwellLevel) + rMPC_Weight_dCondPump;

(* 9.6 Projected Gradient Descent Optimization Step with Slew-Rate Limiting *)
IF rHess11 > 0.001 THEN rDelta_u1_Vane := rDelta_u1_Vane - (0.45 * (rGrad1 / rHess11)); END_IF;
IF rHess22 > 0.001 THEN rDelta_u2_Reflux := rDelta_u2_Reflux - (0.45 * (rGrad2 / rHess22)); END_IF;
IF rHess33 > 0.001 THEN rDelta_u3_Brine := rDelta_u3_Brine - (0.45 * (rGrad3 / rHess33)); END_IF;
IF rHess44 > 0.001 THEN rDelta_u4_CondPump := rDelta_u4_CondPump - (0.45 * (rGrad4 / rHess44)); END_IF;

(* Rate Limiting Enforcements (Slew Bounds) *)
IF rDelta_u1_Vane > (rMaxVaneSlewRate * c_rScanTime_Ts) THEN rDelta_u1_Vane := (rMaxVaneSlewRate * c_rScanTime_Ts);
ELSIF rDelta_u1_Vane < - (rMaxVaneSlewRate * c_rScanTime_Ts) THEN rDelta_u1_Vane := - (rMaxVaneSlewRate * c_rScanTime_Ts); END_IF;

IF rDelta_u2_Reflux > (rMaxRefluxSlewRate * c_rScanTime_Ts) THEN rDelta_u2_Reflux := (rMaxRefluxSlewRate * c_rScanTime_Ts);
ELSIF rDelta_u2_Reflux < - (rMaxRefluxSlewRate * c_rScanTime_Ts) THEN rDelta_u2_Reflux := - (rMaxRefluxSlewRate * c_rScanTime_Ts); END_IF;

IF rDelta_u3_Brine > (rMaxBrineSlewRate * c_rScanTime_Ts) THEN rDelta_u3_Brine := (rMaxBrineSlewRate * c_rScanTime_Ts);
ELSIF rDelta_u3_Brine < - (rMaxBrineSlewRate * c_rScanTime_Ts) THEN rDelta_u3_Brine := - (rMaxBrineSlewRate * c_rScanTime_Ts); END_IF;

IF rDelta_u4_CondPump > (rMaxCondPumpSlewRate * c_rScanTime_Ts) THEN rDelta_u4_CondPump := (rMaxCondPumpSlewRate * c_rScanTime_Ts);
ELSIF rDelta_u4_CondPump < - (rMaxCondPumpSlewRate * c_rScanTime_Ts) THEN rDelta_u4_CondPump := - (rMaxCondPumpSlewRate * c_rScanTime_Ts); END_IF;
"""

with open("scratch/part4_logic_b.txt", "w", encoding="utf-8") as f:
    f.write(part4_logic_b)

print("Part 4B written. Length:", len(part4_logic_b))
