# build_st_phase4_fsm.py
# Section 7: Phase 4 - Deterministic 14-Stage Nuclear State Machine (FSM)

def get_phase4_fsm():
    code = []
    code.append("""(* =====================================================================================================================
 * PHASE 4: DETERMINISTIC 14-STAGE NUCLEAR FINITE STATE MACHINE (FSM)
 * Architecture: Class 1E Deterministic State Engine conforming to IEEE 603 / IEEE 7-4.3.2
 *
 * Operational State Mapping:
 *   0  : COLD_SHUTDOWN_HOT_STANDBY_TRANSFER (Filling, nitrogen blanket collapse, heat-up to 290 deg C)
 *   1  : STARTUP_LOW_POWER_BYPASS_CONTROL (<15% FP single-element bypass regulation)
 *   2  : MAIN_REGULATING_VALVE_TRANSFER_BUMPLESS (Equi-differential pressure cross-fading transfer)
 *   3  : AT_POWER_CASCADE_FEEDFORWARD_STABILIZED (15% - 50% FP 3-element cascade control)
 *   4  : FULL_POWER_OPTIMAL_MPC_TRACKING (50% - 100% FP Receding Horizon MPC with PGD)
 *   5  : RAPID_LOAD_REJECTION_TURBINE_RUNBACK (-5%/min or 50% step runback swell mitigation)
 *   6  : MAIN_STEAM_ISOLATION_VALVE_FAST_CLOSURE (MSIV fast trip closure < 3.0 s, pressure surge)
 *   7  : STEAM_GENERATOR_TUBE_RUPTURE_DIAGNOSTIC (SGTR N-16 gamma spike detection & isolation)
 *   8  : AUXILIARY_FEEDWATER_MOTOR_DRIVEN_START (Loss of normal feed, LL level recovery)
 *   9  : AUXILIARY_FEEDWATER_TURBINE_DRIVEN_AUTO_INIT (Station blackout / dual low-low initiation)
 *   10 : DRY_OUT_PROTECTION_RAPID_COOLDOWN (Severe level depression < tubesheet + 300 mm)
 *   11 : OVERFILL_PROTECTION_MAIN_FEEDWATER_ISOLATION (P-14 Level HH > 3250 mm rapid trip)
 *   12 : REACTOR_PROTECTION_SYSTEM_SCRAM_OVERRIDE (Class 1E SCRAM trip command override)
 *   13 : POST_SCRAM_DECAY_HEAT_THERMAL_EQUILIBRIUM (Decay heat cooling & natural circulation)
 * ===================================================================================================================== *)

(* Update state dwell timer *)
IF eCurrentState = ePreviousState THEN
    rState_Dwell_Timer := rState_Dwell_Timer + rScan_Period_Ts;
    bState_Entry_Flag := FALSE;
ELSE
    rState_Dwell_Timer := 0.0;
    bState_Entry_Flag := TRUE;
    ePreviousState := eCurrentState;
END_IF;

(* Master Safety Overrides (Highest Priority Transitions) *)
IF bDigital_RPS_Reactor_Scram OR bDemand_RPS_Reactor_Trip THEN
    IF eCurrentState <> 12 AND eCurrentState <> 13 THEN
        eCurrentState := 12; (* Jump immediately to RPS SCRAM OVERRIDE *)
    END_IF;
ELSIF rVoted_Level_NR >= rTrip_Level_NR_HighHigh_HH THEN
    IF eCurrentState <> 11 AND eCurrentState <> 12 AND eCurrentState <> 13 THEN
        eCurrentState := 11; (* Jump immediately to P-14 OVERFILL ISOLATION *)
    END_IF;
ELSIF (rRad_N16_SteamLine_ChA >= rTrip_N16_Radiation_SGTR_HH OR rRad_N16_SteamLine_ChB >= rTrip_N16_Radiation_SGTR_HH) THEN
    IF eCurrentState <> 7 AND eCurrentState <> 12 AND eCurrentState <> 13 THEN
        eCurrentState := 7; (* Jump immediately to SGTR DIAGNOSTIC & ISOLATION *)
    END_IF;
ELSIF bDigital_MSIV_Closed_Limit THEN
    IF eCurrentState <> 6 AND eCurrentState <> 12 AND eCurrentState <> 13 THEN
        eCurrentState := 6; (* Jump immediately to MSIV FAST CLOSURE *)
    END_IF;
ELSIF rVoted_Level_NR <= rTrip_Level_NR_LowLow_LL THEN
    IF eCurrentState <> 8 AND eCurrentState <> 9 AND eCurrentState <> 10 AND eCurrentState <> 12 AND eCurrentState <> 13 THEN
        eCurrentState := 8; (* Jump to MOTOR-DRIVEN AFW START *)
    END_IF;
END_IF;

(* State Machine Execution *)
CASE eCurrentState OF

    (* -----------------------------------------------------------------------------------------------------------------
     * STATE 0: COLD_SHUTDOWN_HOT_STANDBY_TRANSFER
     * ----------------------------------------------------------------------------------------------------------------- *)
    0:
        (* Maintain minimum wet layup inventory via low-power bypass *)
        rCommand_MFRV_Position := 0.0;
        rCommand_AFW_Motor_Pump_Speed := 0.0;
        rCommand_AFW_Turbine_Pump_Flow := 0.0;
        rCommand_Blowdown_Valve_Pos := 1.5; (* Continuous clean-up blowdown *)

        (* Proportional level control on low-power bypass valve *)
        IF rVoted_Level_WR < 3500.0 THEN
            rCommand_Bypass_Valve_Pos := 12.5; (* Infill flow *)
        ELSIF rVoted_Level_WR > 4500.0 THEN
            rCommand_Bypass_Valve_Pos := 0.0;  (* Stop filling *)
        ELSE
            rCommand_Bypass_Valve_Pos := 4.0;  (* Trickle flow *)
        END_IF;

        bDemand_RPS_Reactor_Trip := FALSE;
        bDemand_Turbine_Runback := FALSE;
        bDemand_MSIV_Fast_Closure := FALSE;
        bDemand_MFRV_Isolation_P14 := FALSE;
        bDemand_AFW_Motor_Pump_Start := FALSE;
        bDemand_AFW_Turbine_Pump_Start := FALSE;

        (* Transition to Startup Low Power Bypass when RCS temperature > 280 deg C and Drum Pressure > 30 bar *)
        IF rTemp_ColdLeg_Primary >= 280.0 AND rVoted_Press_SteamDrum >= 30.0 AND rReactor_Thermal_Power_Pct >= 1.5 THEN
            eCurrentState := 1; (* STARTUP_LOW_POWER_BYPASS_CONTROL *)
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STATE 1: STARTUP_LOW_POWER_BYPASS_CONTROL (<15% FP)
     * ----------------------------------------------------------------------------------------------------------------- *)
    1:
        (* Single-element narrow range level control through bypass valve *)
        rCommand_MFRV_Position := 0.0; (* Keep MFRV seated tight *)
        rCommand_AFW_Motor_Pump_Speed := 0.0;
        rCommand_AFW_Turbine_Pump_Flow := 0.0;
        rCommand_Blowdown_Valve_Pos := 2.0;

        (* Modulate bypass valve using dynamic feedforward plus level error *)
        rCommand_Bypass_Valve_Pos := 15.0 + (0.025 * (rOperator_Level_Setpoint_NR - rVoted_Level_NR)) + (rDynamic_Feedforward_Bias * 0.02);
        IF rCommand_Bypass_Valve_Pos > 45.0 THEN
            rCommand_Bypass_Valve_Pos := 45.0;
        ELSIF rCommand_Bypass_Valve_Pos < 0.0 THEN
            rCommand_Bypass_Valve_Pos := 0.0;
        END_IF;

        (* Transition to bumpless transfer when thermal power exceeds 14.5% RTP and level is stable *)
        IF rReactor_Thermal_Power_Pct >= 14.5 AND ABS(rVoted_Level_NR - rOperator_Level_Setpoint_NR) < 50.0 THEN
            rBumpless_Transition_Ramp := 0.0;
            eCurrentState := 2; (* MAIN_REGULATING_VALVE_TRANSFER_BUMPLESS *)
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STATE 2: MAIN_REGULATING_VALVE_TRANSFER_BUMPLESS
     * ----------------------------------------------------------------------------------------------------------------- *)
    2:
        (* Ramp cross-fading factor from 0.0 to 1.0 over 30 seconds (1200 cycles of 25 ms) *)
        rBumpless_Transition_Ramp := rBumpless_Transition_Ramp + (rScan_Period_Ts / 30.0);
        IF rBumpless_Transition_Ramp > 1.0 THEN
            rBumpless_Transition_Ramp := 1.0;
        END_IF;

        (* Compute baseline demand required for 15-20% thermal power *)
        rCommand_MFRV_Position := rBumpless_Transition_Ramp * (rMFRV_Auto_Demand_Unclamped + 18.0);
        rCommand_Bypass_Valve_Pos := (1.0 - rBumpless_Transition_Ramp) * (rBypass_Auto_Demand_Unclamped + 15.0);

        (* Clamp actuators within physical bounds *)
        IF rCommand_MFRV_Position > 40.0 THEN rCommand_MFRV_Position := 40.0; END_IF;
        IF rCommand_MFRV_Position < 0.0 THEN rCommand_MFRV_Position := 0.0; END_IF;
        IF rCommand_Bypass_Valve_Pos > 45.0 THEN rCommand_Bypass_Valve_Pos := 45.0; END_IF;
        IF rCommand_Bypass_Valve_Pos < 0.0 THEN rCommand_Bypass_Valve_Pos := 0.0; END_IF;

        (* Transition to at-power cascade feedforward once transfer completes *)
        IF rBumpless_Transition_Ramp >= 1.0 AND rState_Dwell_Timer >= 32.0 THEN
            rCommand_Bypass_Valve_Pos := 0.0; (* Fully isolate bypass valve *)
            eCurrentState := 3; (* AT_POWER_CASCADE_FEEDFORWARD_STABILIZED *)
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STATE 3: AT_POWER_CASCADE_FEEDFORWARD_STABILIZED (15% - 50% FP)
     * ----------------------------------------------------------------------------------------------------------------- *)
    3:
        rCommand_Bypass_Valve_Pos := 0.0;
        rCommand_AFW_Motor_Pump_Speed := 0.0;
        rCommand_AFW_Turbine_Pump_Flow := 0.0;
        rCommand_Blowdown_Valve_Pos := 3.0;

        (* 3-Element Classical Cascade: Level Error + (Steam Flow - Feed Flow) Feedforward *)
        rCommand_MFRV_Position := (rVoted_Flow_MainSteam / rSG_Full_Power_Feed_Flow_t_h * 100.0) +
                                  (0.035 * (rOperator_Level_Setpoint_NR - rVoted_Level_NR)) +
                                  (0.045 * (rVoted_Flow_MainSteam - rVoted_Flow_Feedwater)) +
                                  (rDynamic_Feedforward_Bias * 0.03);

        IF rCommand_MFRV_Position > 65.0 THEN rCommand_MFRV_Position := 65.0; END_IF;
        IF rCommand_MFRV_Position < 5.0 THEN rCommand_MFRV_Position := 5.0; END_IF;

        (* Transition to optimal MPC when power exceeds 48% RTP and level is tight *)
        IF rReactor_Thermal_Power_Pct >= 48.0 AND ABS(rVoted_Level_NR - rOperator_Level_Setpoint_NR) < 40.0 THEN
            eCurrentState := 4; (* FULL_POWER_OPTIMAL_MPC_TRACKING *)
        ELSIF rReactor_Thermal_Power_Pct < 14.0 THEN
            eCurrentState := 1; (* Drop back to bypass control *)
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STATE 4: FULL_POWER_OPTIMAL_MPC_TRACKING (50% - 100% FP)
     * ----------------------------------------------------------------------------------------------------------------- *)
    4:
        rCommand_Bypass_Valve_Pos := 0.0;
        rCommand_AFW_Motor_Pump_Speed := 0.0;
        rCommand_AFW_Turbine_Pump_Flow := 0.0;
        rCommand_Blowdown_Valve_Pos := 4.5;

        (* Full power MPC optimal command execution *)
        rCommand_MFRV_Position := rMFRV_Auto_Demand_Unclamped;

        (* Actuator limits *)
        IF rCommand_MFRV_Position > 100.0 THEN rCommand_MFRV_Position := 100.0; END_IF;
        IF rCommand_MFRV_Position < 15.0 THEN rCommand_MFRV_Position := 15.0; END_IF;

        (* Interlock triggers *)
        IF bDigital_Grid_Load_Drop_Alert THEN
            eCurrentState := 5; (* RAPID_LOAD_REJECTION_TURBINE_RUNBACK *)
        ELSIF rReactor_Thermal_Power_Pct < 45.0 THEN
            eCurrentState := 3; (* Transition back to cascade feedforward *)
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STATE 5: RAPID_LOAD_REJECTION_TURBINE_RUNBACK (-5%/min or 50% Step)
     * ----------------------------------------------------------------------------------------------------------------- *)
    5:
        bDemand_Turbine_Runback := TRUE;
        rCommand_Bypass_Valve_Pos := 0.0;
        rCommand_AFW_Motor_Pump_Speed := 0.0;
        rCommand_AFW_Turbine_Pump_Flow := 0.0;
        rCommand_Blowdown_Valve_Pos := 6.0;

        (* Dynamic swell mitigation: Rapidly pinch MFRV to match collapsing steam flow and avoid false swell P-14 trip *)
        rCommand_MFRV_Position := (rVoted_Flow_MainSteam / rSG_Full_Power_Feed_Flow_t_h * 100.0) -
                                  (0.085 * (rVoted_Level_NR - rOperator_Level_Setpoint_NR)) +
                                  (rDynamic_Feedforward_Bias * 0.06);

        IF rCommand_MFRV_Position > 80.0 THEN rCommand_MFRV_Position := 80.0; END_IF;
        IF rCommand_MFRV_Position < 10.0 THEN rCommand_MFRV_Position := 10.0; END_IF;

        (* Settle into stabilized state after 45 seconds of runback *)
        IF rState_Dwell_Timer >= 45.0 AND ABS(rMeasured_Level_Rate_mm_s) < 15.0 THEN
            bDemand_Turbine_Runback := FALSE;
            IF rReactor_Thermal_Power_Pct >= 48.0 THEN
                eCurrentState := 4;
            ELSE
                eCurrentState := 3;
            END_IF;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STATE 6: MAIN_STEAM_ISOLATION_VALVE_FAST_CLOSURE
     * ----------------------------------------------------------------------------------------------------------------- *)
    6:
        bDemand_MSIV_Fast_Closure := TRUE;
        bDemand_Turbine_Runback := TRUE;
        (* Isolate main feedwater immediately to prevent drum overpressure *)
        rCommand_MFRV_Position := 0.0;
        rCommand_Bypass_Valve_Pos := 0.0;
        rCommand_Blowdown_Valve_Pos := 0.0; (* Prevent radioactive release *)

        (* Maintain water level using low rate motor AFW if pressure allows *)
        IF rVoted_Press_SteamDrum < 75.0 AND rVoted_Level_NR < 2000.0 THEN
            rCommand_AFW_Motor_Pump_Speed := 25.0;
            bDemand_AFW_Motor_Pump_Start := TRUE;
        ELSE
            rCommand_AFW_Motor_Pump_Speed := 0.0;
        END_IF;

        (* Demand reactor trip if MSIV closed at power *)
        IF rReactor_Thermal_Power_Pct > 5.0 THEN
            bDemand_RPS_Reactor_Trip := TRUE;
            eCurrentState := 12; (* SCRAM *)
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STATE 7: STEAM_GENERATOR_TUBE_RUPTURE_DIAGNOSTIC (SGTR Leak Rate Radiation Check)
     * ----------------------------------------------------------------------------------------------------------------- *)
    7:
        bActive_Alarm_SGTR_Trip := TRUE;
        bDemand_RPS_Reactor_Trip := TRUE; (* Reactor Scram Demand *)
        bDemand_Turbine_Runback := TRUE;
        bDemand_MSIV_Fast_Closure := TRUE; (* Isolate ruptured steam generator *)
        bDemand_MFRV_Isolation_P14 := TRUE;

        (* Close all normal feed and blowdown lines immediately to prevent environmental radioactive release *)
        rCommand_MFRV_Position := 0.0;
        rCommand_Bypass_Valve_Pos := 0.0;
        rCommand_Blowdown_Valve_Pos := 0.0;

        (* Retain minimum tube covering using controlled AFW flow without overfilling ruptured SG *)
        IF rVoted_Level_NR < 2100.0 THEN
            rCommand_AFW_Motor_Pump_Speed := 15.0;
            bDemand_AFW_Motor_Pump_Start := TRUE;
        ELSE
            rCommand_AFW_Motor_Pump_Speed := 0.0;
            bDemand_AFW_Motor_Pump_Start := FALSE;
        END_IF;

        IF rState_Dwell_Timer >= 10.0 THEN
            eCurrentState := 12; (* Proceed to SCRAM state *)
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STATE 8: AUXILIARY_FEEDWATER_MOTOR_DRIVEN_START
     * ----------------------------------------------------------------------------------------------------------------- *)
    8:
        bDemand_AFW_Motor_Pump_Start := TRUE;
        rCommand_MFRV_Position := 0.0;
        rCommand_Bypass_Valve_Pos := 0.0;
        rCommand_Blowdown_Valve_Pos := 0.0;

        (* Ramp motor-driven AFW pump to 100% capacity *)
        rCommand_AFW_Motor_Pump_Speed := 100.0;
        rCommand_AFW_Turbine_Pump_Flow := 0.0;

        (* Check if recovery successful *)
        IF rVoted_Level_NR >= rAlarm_Level_NR_Low_L + rDeadband_Level_NR THEN
            bDemand_AFW_Motor_Pump_Start := FALSE;
            rCommand_AFW_Motor_Pump_Speed := 25.0;
            IF bDigital_RPS_Reactor_Scram THEN
                eCurrentState := 13; (* POST SCRAM DECAY HEAT *)
            ELSE
                eCurrentState := 3;  (* Return to at-power cascade *)
            END_IF;
        (* If level continues dropping below 1200 mm, initiate turbine-driven AFW and dryout protection *)
        ELSIF rVoted_Level_WR < 1200.0 OR rVoted_Level_NR < 1200.0 THEN
            eCurrentState := 9; (* Start turbine AFW *)
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STATE 9: AUXILIARY_FEEDWATER_TURBINE_DRIVEN_AUTO_INIT
     * ----------------------------------------------------------------------------------------------------------------- *)
    9:
        bDemand_AFW_Motor_Pump_Start := TRUE;
        bDemand_AFW_Turbine_Pump_Start := TRUE;
        rCommand_MFRV_Position := 0.0;
        rCommand_Bypass_Valve_Pos := 0.0;
        rCommand_Blowdown_Valve_Pos := 0.0;

        (* Full dual AFW train delivery: 100% motor speed + 120 t/h turbine delivery *)
        rCommand_AFW_Motor_Pump_Speed := 100.0;
        rCommand_AFW_Turbine_Pump_Flow := 120.0;

        (* If water level drops to tubesheet, escalate to dry out protection *)
        IF rVoted_Level_WR < 800.0 THEN
            eCurrentState := 10; (* DRY_OUT_PROTECTION_RAPID_COOLDOWN *)
        ELSIF rVoted_Level_NR >= rAlarm_Level_NR_Low_L THEN
            eCurrentState := 8; (* Downgrade to motor AFW *)
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STATE 10: DRY_OUT_PROTECTION_RAPID_COOLDOWN
     * ----------------------------------------------------------------------------------------------------------------- *)
    10:
        bDemand_RPS_Reactor_Trip := TRUE;
        bDemand_Turbine_Runback := TRUE;
        bDemand_AFW_Motor_Pump_Start := TRUE;
        bDemand_AFW_Turbine_Pump_Start := TRUE;

        (* Maximum emergency injection *)
        rCommand_MFRV_Position := 0.0;
        rCommand_Bypass_Valve_Pos := 0.0;
        rCommand_AFW_Motor_Pump_Speed := 100.0;
        rCommand_AFW_Turbine_Pump_Flow := 150.0;
        rCommand_Blowdown_Valve_Pos := 0.0;

        (* Transition to post-scram state once level recovers above 1500 mm *)
        IF rVoted_Level_WR >= 1500.0 THEN
            eCurrentState := 13; (* POST_SCRAM_DECAY_HEAT_THERMAL_EQUILIBRIUM *)
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STATE 11: OVERFILL_PROTECTION_MAIN_FEEDWATER_ISOLATION
     * ----------------------------------------------------------------------------------------------------------------- *)
    11:
        bDemand_MFRV_Isolation_P14 := TRUE;
        bDemand_Turbine_Runback := TRUE;

        (* Slam shut all feedwater supplies to prevent liquid carryover to steam lines *)
        rCommand_MFRV_Position := 0.0;
        rCommand_Bypass_Valve_Pos := 0.0;
        rCommand_AFW_Motor_Pump_Speed := 0.0;
        rCommand_AFW_Turbine_Pump_Flow := 0.0;

        (* Open blowdown to purge excess inventory *)
        rCommand_Blowdown_Valve_Pos := 10.0;

        (* Reset when level drops below high alarm deadband *)
        IF rVoted_Level_NR <= (rTrip_Level_NR_HighHigh_HH - rDeadband_Level_NR - 50.0) THEN
            bDemand_MFRV_Isolation_P14 := FALSE;
            rCommand_Blowdown_Valve_Pos := 3.0;
            IF bDigital_RPS_Reactor_Scram THEN
                eCurrentState := 13;
            ELSE
                eCurrentState := 3;
            END_IF;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STATE 12: REACTOR_PROTECTION_SYSTEM_SCRAM_OVERRIDE
     * ----------------------------------------------------------------------------------------------------------------- *)
    12:
        bDemand_RPS_Reactor_Trip := TRUE;
        bDemand_Turbine_Runback := TRUE;
        rCommand_MFRV_Position := 0.0; (* Trip MFRV *)
        rCommand_Bypass_Valve_Pos := 0.0;
        rCommand_Blowdown_Valve_Pos := 1.0;

        (* Moderate AFW flow to cushion void collapse shrink after scram *)
        rCommand_AFW_Motor_Pump_Speed := 35.0;
        bDemand_AFW_Motor_Pump_Start := TRUE;
        rCommand_AFW_Turbine_Pump_Flow := 0.0;

        (* Wait 20 seconds for control rod insertion and initial thermal flux collapse *)
        IF rState_Dwell_Timer >= 20.0 THEN
            eCurrentState := 13; (* POST_SCRAM_DECAY_HEAT_THERMAL_EQUILIBRIUM *)
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STATE 13: POST_SCRAM_DECAY_HEAT_THERMAL_EQUILIBRIUM
     * ----------------------------------------------------------------------------------------------------------------- *)
    13:
        bDemand_RPS_Reactor_Trip := FALSE; (* Trip already latched in plant RPS *)
        rCommand_MFRV_Position := 0.0;
        rCommand_Bypass_Valve_Pos := 0.0;
        rCommand_Blowdown_Valve_Pos := 1.0;

        (* Maintain narrow range level between 2100 mm and 2400 mm using motor AFW *)
        IF rVoted_Level_NR < 2100.0 THEN
            rCommand_AFW_Motor_Pump_Speed := 40.0;
            bDemand_AFW_Motor_Pump_Start := TRUE;
        ELSIF rVoted_Level_NR > 2400.0 THEN
            rCommand_AFW_Motor_Pump_Speed := 0.0;
            bDemand_AFW_Motor_Pump_Start := FALSE;
        ELSE
            rCommand_AFW_Motor_Pump_Speed := 15.0; (* Trickle feed for decay heat boil-off *)
            bDemand_AFW_Motor_Pump_Start := TRUE;
        END_IF;

        (* If operator resets trips and system re-enters cold shutdown *)
        IF bReset_Trip_Interlocks AND rReactor_Thermal_Power_Pct < 1.0 AND rTemp_ColdLeg_Primary < 200.0 THEN
            eCurrentState := 0; (* Return to cold shutdown *)
        END_IF;

    ELSE
        (* Failsafe default *)
        eCurrentState := 0;
END_CASE;

(* Export active state index *)
nActiveStateIndex := eCurrentState;
""")
    return "\n".join(code)

if __name__ == "__main__":
    s = get_phase4_fsm()
    print("Phase 4 FSM length:", len(s))
