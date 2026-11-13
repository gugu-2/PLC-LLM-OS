# mine_vod_fan_builder/st_phase5_fsm.py

def get_phase5_fsm():
    return """(* ==================================================================================================== *)
(* PHASE 5: DETERMINISTIC 14-STAGE PRODUCTION FINITE STATE MACHINE (FSM)                                *)
(* ==================================================================================================== *)

(* Update State Transition Timer *)
IF eState = ePrevState THEN
    tStateTimer_s := tStateTimer_s + rCycleTime_s;
ELSE
    tStateTimer_s := 0.0;
    tSubStepTimer_s := 0.0;
    iStateStep := 0;
    ePrevState := eState;
END_IF;

(* Master Hardwired Emergency Stop & Trip Override *)
IF bEmergencyStop OR (bTripGeneral AND (eState <> 13)) THEN
    eState := 13; (* Immediate transition to Emergency Fire / Smoke Isolation Trip *)
END_IF;

CASE eState OF

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 0: IDLE STANDBY                                                                            *)
    (* Surface fans stationary, blades feathered, hydraulic and lube systems off, louvers in safe rest *)
    (* ------------------------------------------------------------------------------------------------ *)
    0:
        bFan1_RunCmd := FALSE;
        bFan2_RunCmd := FALSE;
        rFan1_VFD_SpeedCmd_RPM := 0.0;
        rFan2_VFD_SpeedCmd_RPM := 0.0;
        rFan1_BladePitchCmd_deg := -12.0;
        rFan2_BladePitchCmd_deg := -12.0;
        bFanAntiStallBypassDamperOpenCmd := FALSE;
        rSurfaceFanLubePumpRunCmd := FALSE;
        rSurfaceFanHydraulicPumpRunCmd := FALSE;
        rIntakeCollarHeaterValveCmd_pct := 0.0;

        (* Set 24 Louvers to Safe Natural Circulation Rest Position (25%) *)
        FOR iLoopIdx := 1 TO 24 DO
            arrLouverCmd_pct[iLoopIdx] := 25.0;
            arrAuxBoosterFanCmd_pct[iLoopIdx] := 0.0;
        END_FOR;

        (* Reset Progression Flags *)
        bLubeOilPressureEstablished := FALSE;
        bBladePitchAtZeroReturn := FALSE;
        bMotorSoftStartCompleted := FALSE;
        bBladePitchMinimumLoadRamped := FALSE;
        bLouverSweepCompleted := FALSE;

        (* Transition to Lube Oil Pressure Lock on Master Enable *)
        IF bEnable AND NOT bEmergencyStop AND NOT bTripGeneral THEN
            eState := 1;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 1: SURFACE FAN LUBE OIL PRESSURE LOCK                                                      *)
    (* Start forced lubrication and hydraulic power units, verify hydrodynamic oil film pressure        *)
    (* ------------------------------------------------------------------------------------------------ *)
    1:
        rSurfaceFanLubePumpRunCmd := TRUE;
        rSurfaceFanHydraulicPumpRunCmd := TRUE;

        (* Check Lube Oil Pressure on Active Fans *)
        IF bDualFanParallelMode THEN
            bLubeOilPressureEstablished := (rFan1_LubeOilPressure_bar >= 3.2) AND (rFan2_LubeOilPressure_bar >= 3.2);
        ELSIF bLeadFanSelect THEN
            bLubeOilPressureEstablished := (rFan2_LubeOilPressure_bar >= 3.2);
        ELSE
            bLubeOilPressureEstablished := (rFan1_LubeOilPressure_bar >= 3.2);
        END_IF;

        (* Permissive Verification with 10.0 s Stabilization Timer *)
        IF bLubeOilPressureEstablished THEN
            tSubStepTimer_s := tSubStepTimer_s + rCycleTime_s;
            IF tSubStepTimer_s >= 10.0 THEN
                eState := 2; (* Advance to Blade Pitch Zero Return *)
            END_IF;
        ELSE
            tSubStepTimer_s := 0.0;
            (* Timeout Fault: If pressure fails to build within 45 seconds *)
            IF tStateTimer_s > 45.0 THEN
                bTripGeneral := TRUE;
                eState := 11;
            END_IF;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 2: HYDRAULIC BLADE PITCH ZERO RETURN                                                       *)
    (* Feather axial fan impeller blades to -12 deg zero-torque position prior to motor spin-up         *)
    (* ------------------------------------------------------------------------------------------------ *)
    2:
        rFan1_BladePitchCmd_deg := -12.0;
        rFan2_BladePitchCmd_deg := -12.0;

        (* Verify Blade Pitch Feedback within Tolerance of Feathered Position *)
        IF bDualFanParallelMode THEN
            bBladePitchAtZeroReturn := (rFan1_BladePitchFeedback_deg <= -10.5) AND (rFan2_BladePitchFeedback_deg <= -10.5);
        ELSIF bLeadFanSelect THEN
            bBladePitchAtZeroReturn := (rFan2_BladePitchFeedback_deg <= -10.5);
        ELSE
            bBladePitchAtZeroReturn := (rFan1_BladePitchFeedback_deg <= -10.5);
        END_IF;

        IF bBladePitchAtZeroReturn THEN
            tSubStepTimer_s := tSubStepTimer_s + rCycleTime_s;
            IF tSubStepTimer_s >= 5.0 THEN
                eState := 3; (* Advance to Motor Soft-Start Spinup *)
            END_IF;
        ELSE
            tSubStepTimer_s := 0.0;
            IF tStateTimer_s > 60.0 THEN
                bTripGeneral := TRUE;
                eState := 11;
            END_IF;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 3: SURFACE MAIN MOTOR SOFT-START SPINUP                                                    *)
    (* Accelerate 3.5 MW induction motor from 0 to 990 RPM via VFD ramp with vibration monitoring       *)
    (* ------------------------------------------------------------------------------------------------ *)
    3:
        IF bDualFanParallelMode THEN
            bFan1_RunCmd := TRUE;
            bFan2_RunCmd := TRUE;
            rFan1_VFD_SpeedCmd_RPM := MIN(990.0, tStateTimer_s * 16.5);
            rFan2_VFD_SpeedCmd_RPM := MIN(990.0, tStateTimer_s * 16.5);
            bMotorSoftStartCompleted := (rFan1_MotorSpeed_RPM >= 960.0) AND (rFan2_MotorSpeed_RPM >= 960.0);
        ELSIF bLeadFanSelect THEN
            bFan2_RunCmd := TRUE;
            bFan1_RunCmd := FALSE;
            rFan2_VFD_SpeedCmd_RPM := MIN(990.0, tStateTimer_s * 16.5);
            rFan1_VFD_SpeedCmd_RPM := 0.0;
            bMotorSoftStartCompleted := (rFan2_MotorSpeed_RPM >= 960.0);
        ELSE
            bFan1_RunCmd := TRUE;
            bFan2_RunCmd := FALSE;
            rFan1_VFD_SpeedCmd_RPM := MIN(990.0, tStateTimer_s * 16.5);
            rFan2_VFD_SpeedCmd_RPM := 0.0;
            bMotorSoftStartCompleted := (rFan1_MotorSpeed_RPM >= 960.0);
        END_IF;

        (* Abort Spin-Up on Excessive Bearing Vibration *)
        IF rVib_Voted >= rVib_Trip_HH THEN
            bTripGeneral := TRUE;
            eState := 11;
        END_IF;

        IF bMotorSoftStartCompleted THEN
            tSubStepTimer_s := tSubStepTimer_s + rCycleTime_s;
            IF tSubStepTimer_s >= 8.0 THEN
                eState := 4; (* Advance to Blade Pitch Minimum Load Ramp *)
            END_IF;
        ELSE
            tSubStepTimer_s := 0.0;
            IF tStateTimer_s > 90.0 THEN
                bTripGeneral := TRUE;
                eState := 11;
            END_IF;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 4: AERODYNAMIC BLADE PITCH MINIMUM LOAD RAMP                                               *)
    (* Slowly ramp blade pitch from -12 deg feather to +8 deg base load, establish initial mine draw    *)
    (* ------------------------------------------------------------------------------------------------ *)
    4:
        rTempDelta := -12.0 + (tStateTimer_s * 0.85);
        IF rTempDelta > 8.0 THEN rTempDelta := 8.0; END_IF;

        IF bDualFanParallelMode THEN
            rFan1_BladePitchCmd_deg := rTempDelta;
            rFan2_BladePitchCmd_deg := rTempDelta;
            bBladePitchMinimumLoadRamped := (rFan1_BladePitchFeedback_deg >= 7.2) AND (rFan2_BladePitchFeedback_deg >= 7.2);
        ELSIF bLeadFanSelect THEN
            rFan2_BladePitchCmd_deg := rTempDelta;
            bBladePitchMinimumLoadRamped := (rFan2_BladePitchFeedback_deg >= 7.2);
        ELSE
            rFan1_BladePitchCmd_deg := rTempDelta;
            bBladePitchMinimumLoadRamped := (rFan1_BladePitchFeedback_deg >= 7.2);
        END_IF;

        (* Verify Positive Exhaust Airflow Established *)
        IF bBladePitchMinimumLoadRamped AND (rTotalAirwayVolumeFlow_m3s >= 80.0) THEN
            tSubStepTimer_s := tSubStepTimer_s + rCycleTime_s;
            IF tSubStepTimer_s >= 6.0 THEN
                eState := 5; (* Advance to Louver Initial Calibration Sweep *)
            END_IF;
        ELSE
            tSubStepTimer_s := 0.0;
            IF tStateTimer_s > 45.0 THEN
                bTripGeneral := TRUE;
                eState := 11;
            END_IF;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 5: UNDERGROUND LOUVER INITIAL CALIBRATION SWEEP                                            *)
    (* Perform automated diagnostic travel stroke across all 24 branch louvers                          *)
    (* ------------------------------------------------------------------------------------------------ *)
    5:
        IF tStateTimer_s < 15.0 THEN
            (* Step 5.1: Stroke Louvers to 85% Open *)
            FOR iLoopIdx := 1 TO 24 DO
                arrLouverCmd_pct[iLoopIdx] := 85.0;
            END_FOR;
        ELSIF tStateTimer_s < 30.0 THEN
            (* Step 5.2: Stroke Louvers to 15% Choke *)
            FOR iLoopIdx := 1 TO 24 DO
                arrLouverCmd_pct[iLoopIdx] := 15.0;
            END_FOR;
        ELSE
            (* Step 5.3: Return to Nominal VOD Working Positions (45%) *)
            FOR iLoopIdx := 1 TO 24 DO
                arrLouverCmd_pct[iLoopIdx] := 45.0;
            END_FOR;
            bLouverSweepCompleted := TRUE;
        END_IF;

        IF bLouverSweepCompleted AND (tStateTimer_s >= 35.0) THEN
            eState := 6; (* Advance to Nominal VOD Closed-Loop MPC Run *)
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 6: NOMINAL VOD CLOSED-LOOP MPC RUN                                                         *)
    (* Fully autonomous closed-loop optimization balancing fan RPM, blade pitch, and 24 branch louvers  *)
    (* ------------------------------------------------------------------------------------------------ *)
    6:
        (* Ensure Run Commands Active *)
        IF bDualFanParallelMode THEN
            bFan1_RunCmd := TRUE;
            bFan2_RunCmd := TRUE;
        ELSIF bLeadFanSelect THEN
            bFan2_RunCmd := TRUE;
            bFan1_RunCmd := FALSE;
        ELSE
            bFan1_RunCmd := TRUE;
            bFan2_RunCmd := FALSE;
        END_IF;
        bFanAntiStallBypassDamperOpenCmd := FALSE;

        (* State Machine Dynamic Transitions from Nominal Operation *)
        IF bFireSmokeEmergencyTrip OR (iFireZoneIndex > 0) THEN
            eState := 13; (* Emergency Fire / Smoke Isolation Trip *)
        ELSIF bAntiStallActive OR (rFanStallMargin_pct < rStall_Warn_L) THEN
            eState := 9; (* Aerodynamic Stall Warning Pitch Relief *)
        ELSIF bPostBlastPurgeRequest OR (iActiveBlastingZoneIndex > 0) THEN
            eState := 7; (* Post-Blast Clearance Maximum Airflow Purge *)
        ELSIF bDieselHaulageBoostRequest THEN
            eState := 8; (* Heavy Diesel Haulage Local Boost Mode *)
        ELSIF bIcePreventionEnable AND (rSurfaceAirTemp_degC < rIntakeTemp_Warn_L) THEN
            eState := 10; (* Airway Ice Prevention Intake Coil Heat *)
        ELSIF NOT bEnable THEN
            eState := 11; (* Controlled Airway Rampdown and Float *)
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 7: POST-BLAST CLEARANCE MAXIMUM AIRFLOW PURGE                                              *)
    (* Deliver maximum airflow to blasting heading to rapidly purge toxic CO and NO2 fumes              *)
    (* ------------------------------------------------------------------------------------------------ *)
    7:
        tBlastPurgeElapsed_s := tBlastPurgeElapsed_s + rCycleTime_s;

        (* Command Maximum Aerodynamic Pitch and Rated Motor RPM *)
        IF bDualFanParallelMode THEN
            rFan1_BladePitchCmd_deg := 26.5;
            rFan1_VFD_SpeedCmd_RPM := 1015.0;
            rFan2_BladePitchCmd_deg := 26.5;
            rFan2_VFD_SpeedCmd_RPM := 1015.0;
        ELSIF bLeadFanSelect THEN
            rFan2_BladePitchCmd_deg := 28.0;
            rFan2_VFD_SpeedCmd_RPM := 1025.0;
        ELSE
            rFan1_BladePitchCmd_deg := 28.0;
            rFan1_VFD_SpeedCmd_RPM := 1025.0;
        END_IF;

        (* Check Blast Clearance Termination Criteria *)
        IF (rToxicGas_Voted <= rCO_SafeReentryLimit_ppm) AND (tBlastPurgeElapsed_s >= 180.0) THEN
            bPostBlastPurgeCompleted := TRUE;
            tBlastPurgeElapsed_s := 0.0;
            eState := 6; (* Return to Nominal VOD MPC Run *)
        END_IF;

        (* Abort on Emergency Interlocks *)
        IF bFireSmokeEmergencyTrip THEN
            eState := 13;
        ELSIF bAntiStallActive THEN
            eState := 9;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 8: HEAVY DIESEL HAULAGE LOCAL BOOST MODE                                                   *)
    (* Dynamically prioritize ventilation along active heavy diesel trucking decline routes             *)
    (* ------------------------------------------------------------------------------------------------ *)
    8:
        (* Boost Surface Fan Speed by +65 RPM to overcome ramp friction *)
        IF bDualFanParallelMode THEN
            rFan1_VFD_SpeedCmd_RPM := MIN(1020.0, arrU_opt[2] + 45.0);
            rFan2_VFD_SpeedCmd_RPM := MIN(1020.0, arrU_opt[2] + 45.0);
        ELSIF bLeadFanSelect THEN
            rFan2_VFD_SpeedCmd_RPM := MIN(1035.0, arrU_opt[2] + 65.0);
        ELSE
            rFan1_VFD_SpeedCmd_RPM := MIN(1035.0, arrU_opt[2] + 65.0);
        END_IF;

        (* Transition Back to Nominal when Fleet Boost Request Clears *)
        IF NOT bDieselHaulageBoostRequest THEN
            eState := 6;
        ELSIF bFireSmokeEmergencyTrip THEN
            eState := 13;
        ELSIF bAntiStallActive THEN
            eState := 9;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 9: AERODYNAMIC STALL WARNING PITCH RELIEF                                                  *)
    (* Fast pitch reduction, speed compensation and bypass damper venting to avert fan rotating stall   *)
    (* ------------------------------------------------------------------------------------------------ *)
    9:
        (* Rapid Pitch Relief: Reduce pitch angle by 8.5 deg *)
        IF bDualFanParallelMode THEN
            rFan1_BladePitchCmd_deg := MAX(-6.0, rFan1_BladePitchFeedback_deg - (rBladePitchRateMax_deg_s * rCycleTime_s));
            rFan2_BladePitchCmd_deg := MAX(-6.0, rFan2_BladePitchFeedback_deg - (rBladePitchRateMax_deg_s * rCycleTime_s));
        ELSIF bLeadFanSelect THEN
            rFan2_BladePitchCmd_deg := MAX(-6.0, rFan2_BladePitchFeedback_deg - (rBladePitchRateMax_deg_s * rCycleTime_s));
        ELSE
            rFan1_BladePitchCmd_deg := MAX(-6.0, rFan1_BladePitchFeedback_deg - (rBladePitchRateMax_deg_s * rCycleTime_s));
        END_IF;

        (* Open Surface Substation Anti-Stall Bypass Damper if Stall Margin Critical *)
        IF rFanStallMargin_pct < rStall_Trip_LL THEN
            bFanAntiStallBypassDamperOpenCmd := TRUE;
        END_IF;

        (* Open Underground Louvers to Relieve System Aerodynamic Resistance *)
        FOR iLoopIdx := 1 TO 24 DO
            arrLouverCmd_pct[iLoopIdx] := MIN(100.0, arrLouverCmd_pct[iLoopIdx] + 0.85);
        END_FOR;

        (* Check Recovery of Aerodynamic Stall Margin *)
        IF (rFanStallMargin_pct >= (rStall_Warn_L + rStall_Hysteresis)) AND (rBladeTipTurbulenceRMS_Pa <= (rTurb_Warn_H - rTurb_Hysteresis)) THEN
            tSubStepTimer_s := tSubStepTimer_s + rCycleTime_s;
            IF tSubStepTimer_s >= 12.0 THEN
                bFanAntiStallBypassDamperOpenCmd := FALSE;
                bAntiStallActive := FALSE;
                eState := 6; (* Return to Nominal VOD Closed-Loop *)
            END_IF;
        ELSE
            tSubStepTimer_s := 0.0;
            (* If stall persists > 30 s without recovery, trip to avoid blade flutter failure *)
            IF tStateTimer_s > 30.0 THEN
                bTripGeneral := TRUE;
                eState := 11;
            END_IF;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 10: AIRWAY ICE PREVENTION INTAKE COIL HEAT                                                 *)
    (* Modulate hot water glycol thermal coils to protect collar concrete and shaft conveyance guides   *)
    (* ------------------------------------------------------------------------------------------------ *)
    10:
        (* Modulate Valve Proportional to Freezing Margin *)
        rTempDelta := (rIntakeTemp_Warn_L + 2.0 - rSurfaceAirTemp_degC) * 35.0;
        IF rTempDelta < 15.0 THEN rTempDelta := 15.0; ELSIF rTempDelta > 100.0 THEN rTempDelta := 100.0; END_IF;
        rIntakeCollarHeaterValveCmd_pct := rTempDelta;

        IF rSurfaceAirTemp_degC >= (rIntakeTemp_Warn_L + 2.5) THEN
            eState := 6; (* Ambient warmed above freeze threshold *)
        ELSIF bFireSmokeEmergencyTrip THEN
            eState := 13;
        ELSIF bAntiStallActive THEN
            eState := 9;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 11: CONTROLLED AIRWAY RAMPDOWN AND FLOAT                                                   *)
    (* Controlled de-pitching and VFD deceleration of surface axial fans to prevent duct pressure surges*)
    (* ------------------------------------------------------------------------------------------------ *)
    11:
        (* Ramp Pitch Down to Feathered Position *)
        IF bDualFanParallelMode THEN
            rFan1_BladePitchCmd_deg := MAX(-12.0, rFan1_BladePitchCmd_deg - (1.5 * rCycleTime_s));
            rFan2_BladePitchCmd_deg := MAX(-12.0, rFan2_BladePitchCmd_deg - (1.5 * rCycleTime_s));
            rFan1_VFD_SpeedCmd_RPM := MAX(0.0, rFan1_VFD_SpeedCmd_RPM - (12.0 * rCycleTime_s));
            rFan2_VFD_SpeedCmd_RPM := MAX(0.0, rFan2_VFD_SpeedCmd_RPM - (12.0 * rCycleTime_s));
        ELSIF bLeadFanSelect THEN
            rFan2_BladePitchCmd_deg := MAX(-12.0, rFan2_BladePitchCmd_deg - (1.5 * rCycleTime_s));
            rFan2_VFD_SpeedCmd_RPM := MAX(0.0, rFan2_VFD_SpeedCmd_RPM - (12.0 * rCycleTime_s));
        ELSE
            rFan1_BladePitchCmd_deg := MAX(-12.0, rFan1_BladePitchCmd_deg - (1.5 * rCycleTime_s));
            rFan1_VFD_SpeedCmd_RPM := MAX(0.0, rFan1_VFD_SpeedCmd_RPM - (12.0 * rCycleTime_s));
        END_IF;

        (* When Fans Dropped Below 100 RPM, Advance to Standby Cooldown *)
        IF (rFan1_MotorSpeed_RPM < 100.0) AND (rFan2_MotorSpeed_RPM < 100.0) THEN
            bFan1_RunCmd := FALSE;
            bFan2_RunCmd := FALSE;
            eState := 12;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 12: SURFACE FAN STANDBY COOLDOWN PURGE                                                     *)
    (* Maintain lubrication oil circulation for 10 minutes to cool motor journal sleeve bearings       *)
    (* ------------------------------------------------------------------------------------------------ *)
    12:
        rSurfaceFanLubePumpRunCmd := TRUE;
        rSurfaceFanHydraulicPumpRunCmd := FALSE;

        IF tStateTimer_s >= 600.0 THEN
            bStandbyPurgeCompleted := TRUE;
            rSurfaceFanLubePumpRunCmd := FALSE;
            eState := 0; (* Return to Idle State *)
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 13: EMERGENCY UNDERGROUND FIRE SMOKE ISOLATION TRIP                                        *)
    (* Contain fire smoke plume, enforce critical velocity lock to prevent upstream backlayering       *)
    (* ------------------------------------------------------------------------------------------------ *)
    13:
        bEmergencyTripLatched := TRUE;

        (* Maintain High Airway Intake Velocity to Prevent Smoke Rollback *)
        IF bDualFanParallelMode THEN
            bFan1_RunCmd := TRUE;
            bFan2_RunCmd := TRUE;
            rFan1_VFD_SpeedCmd_RPM := 1020.0;
            rFan2_VFD_SpeedCmd_RPM := 1020.0;
            rFan1_BladePitchCmd_deg := 22.0;
            rFan2_BladePitchCmd_deg := 22.0;
        ELSIF bLeadFanSelect THEN
            bFan2_RunCmd := TRUE;
            rFan2_VFD_SpeedCmd_RPM := 1040.0;
            rFan2_BladePitchCmd_deg := 24.0;
        ELSE
            bFan1_RunCmd := TRUE;
            rFan1_VFD_SpeedCmd_RPM := 1040.0;
            rFan1_BladePitchCmd_deg := 24.0;
        END_IF;

        (* Choke Fire Zone Louvers to 10% to Starve Oxygen and Seal Inactive Branches *)
        FOR iLoopIdx := 1 TO 24 DO
            IF (iLoopIdx = iFireZoneIndex) OR arrZoneFireAlarm[iLoopIdx] THEN
                arrLouverCmd_pct[iLoopIdx] := 10.0; (* Choke fire heading *)
                arrAuxBoosterFanCmd_pct[iLoopIdx] := 0.0; (* Trip booster in fire heading *)
            ELSE
                (* Maintain Airflow along Primary Escape Routes *)
                arrLouverCmd_pct[iLoopIdx] := 65.0;
                arrAuxBoosterFanCmd_pct[iLoopIdx] := 50.0;
            END_IF;
        END_FOR;

        (* Manual Reset Permissive: Only exit when fire cleared and manual reset pressed *)
        IF bReset AND NOT bFireSmokeEmergencyTrip AND (iFireZoneIndex = 0) AND NOT bEmergencyStop THEN
            bEmergencyTripLatched := FALSE;
            bTripGeneral := FALSE;
            eState := 6; (* Return to Closed-Loop Run *)
        END_IF;

END_CASE;

(* Update Current State Index Output *)
iCurrentState := eState;
"""
