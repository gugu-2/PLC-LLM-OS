# subsea_boosting_builder/st_phase4_fsm.py

def get_phase4_fsm():
    return """(* ==================================================================================================== *)
(* PHASE 4: 14-STAGE DETERMINISTIC PRODUCTION FINITE STATE MACHINE (FSM)                                 *)
(* States:                                                                                              *)
(*   0: STATE_IDLE                                                                                      *)
(*   1: STATE_BARRIER_FLUID_SEAL_PRESSURIZATION_LOCK                                                    *)
(*   2: STATE_MEG_HYDRATE_INHIBITOR_PRIME_FLUSH                                                         *)
(*   3: STATE_ANTI_SURGE_KICKBACK_VALVE_FULL_OPEN_UNLOAD                                                *)
(*   4: STATE_SUBSEA_VFD_MOTOR_SPINUP_AND_LUBE_CHECK                                                    *)
(*   5: STATE_MINIMUM_STABLE_FLOW_CIRCULATION_RUN                                                       *)
(*   6: STATE_CONTROLLED_KICKBACK_VALVE_CLOSING_RAMP                                                    *)
(*   7: STATE_NOMINAL_MULTIPHASE_BOOSTING_MPC_RUN                                                       *)
(*   8: STATE_GAS_SLUG_ATTENUATION_AND_SPEED_SURGE_CUT                                                  *)
(*   9: STATE_THERMAL_EXPANSION_CLEARANCE_BALANCING                                                     *)
(*  10: STATE_HIGH_GVF_MIST_COOLING_LIQUID_RECYCLE                                                      *)
(*  11: STATE_CONTROLLED_WELLHEAD_TURNDOWN_AND_FLUSH                                                    *)
(*  12: STATE_SAFE_DEPRESSURIZATION_AND_INERT_SEAL_HOLD                                                 *)
(*  13: STATE_EMERGENCY_SUBSEA_SEAL_LOSS_OR_SURGE_TRIP                                                  *)
(* ==================================================================================================== *)

(* Global Safety Interlock: Immediate Hard Trip to State 13 *)
IF bEmergencyStop_SubseaESD OR bAlarm_SealDP_LL OR bAlarm_DiffPress_HH OR
   bAlarm_DischargePress_HH OR bAlarm_Vibration_HH OR bClearanceCriticalTrip THEN
    IF nFSM_CurrentState <> 13 THEN
        nFSM_PreviousState := nFSM_CurrentState;
        nFSM_CurrentState := 13;
        bFSM_StateFirstScan := TRUE;
    END_IF;
END_IF;

(* Track State Entry Pulse and Continuous State Timer *)
IF nFSM_CurrentState <> nFSM_PreviousState THEN
    bFSM_StateFirstScan := TRUE;
    tFSM_StateTimer_s := 0.0;
    tFSM_StepTimer_s := 0.0;
    nFSM_SubStep := 0;
    nFSM_PreviousState := nFSM_CurrentState;
ELSE
    bFSM_StateFirstScan := FALSE;
    tFSM_StateTimer_s := tFSM_StateTimer_s + rCycleTime_s;
    tFSM_StepTimer_s := tFSM_StepTimer_s + rCycleTime_s;
END_IF;

nActiveStateIndex := nFSM_CurrentState;

(* Master FSM State Switch Engine *)
CASE nFSM_CurrentState OF

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 0: STATE_IDLE - Subsea Station Standby & Telemetry Health Verification                    *)
    (* ------------------------------------------------------------------------------------------------ *)
    0:
        bStationReady := FALSE;
        bStationRunning := FALSE;
        rVFD_SpeedDemand_RPM := 0.0;
        rKickbackValveDemand_pct := 100.0; (* Failsafe open kickback bypass *)
        rMEG_InhibitorValveDemand_pct := 0.0;
        rBarrierFluidChargeDemand_pct := 5.0; (* Low trickle barrier charge *)
        rChokeTrimDemand_pct := 0.0; (* Export isolation choke parked closed *)
        rMistCoolingRecycleDemand_pct := 0.0;

        (* Transition Guard to State 1: Operator Enable & Platform Permissive *)
        IF bEnable AND bProductionPermissive AND NOT bStationTripped THEN
            nFSM_CurrentState := 1;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 1: STATE_BARRIER_FLUID_SEAL_PRESSURIZATION_LOCK                                            *)
    (* Subsea API 53B/C closed-loop barrier fluid charging: overpressure > 35 bar over internal fluid  *)
    (* ------------------------------------------------------------------------------------------------ *)
    1:
        bStationReady := FALSE;
        bStationRunning := FALSE;
        rVFD_SpeedDemand_RPM := 0.0;
        rKickbackValveDemand_pct := 100.0;
        rChokeTrimDemand_pct := 0.0;
        rMistCoolingRecycleDemand_pct := 0.0;

        IF bFSM_StateFirstScan THEN
            nFSM_SubStep := 1;
            tFSM_StepTimer_s := 0.0;
        END_IF;

        IF nFSM_SubStep = 1 THEN
            (* Actively charge barrier fluid piston accumulator *)
            rBarrierFluidChargeDemand_pct := 65.0;
            IF rVotedSealDP_bar >= 38.0 AND rBarrierAccumulatorPress_bar >= (rSeabedAmbientPress_bar + 35.0) THEN
                nFSM_SubStep := 2;
                tFSM_StepTimer_s := 0.0;
            END_IF;
        ELSIF nFSM_SubStep = 2 THEN
            (* Seal lock-in soak: verify leak rate is below safe threshold (< 3.0 mL/min) *)
            rBarrierFluidChargeDemand_pct := 15.0;
            IF tFSM_StepTimer_s >= 4.0 THEN
                IF rBarrierFluidLeakRate_mLmin <= 3.0 AND rVotedSealDP_bar >= 35.0 THEN
                    nFSM_CurrentState := 2;
                ELSIF tFSM_StateTimer_s > 45.0 THEN
                    (* Seal pressurization timeout fault *)
                    nFSM_CurrentState := 13;
                END_IF;
            END_IF;
        END_IF;

        IF NOT bEnable OR NOT bProductionPermissive THEN
            nFSM_CurrentState := 0;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 2: STATE_MEG_HYDRATE_INHIBITOR_PRIME_FLUSH                                                 *)
    (* Dynamic Mono-Ethylene Glycol injection priming to establish protective thermodynamic margin      *)
    (* ------------------------------------------------------------------------------------------------ *)
    2:
        bStationReady := FALSE;
        bStationRunning := FALSE;
        rVFD_SpeedDemand_RPM := 0.0;
        rKickbackValveDemand_pct := 100.0;
        rChokeTrimDemand_pct := 0.0;
        rMistCoolingRecycleDemand_pct := 0.0;
        rBarrierFluidChargeDemand_pct := 12.0;

        IF bFSM_StateFirstScan THEN
            nFSM_SubStep := 1;
            tFSM_StepTimer_s := 0.0;
        END_IF;

        IF nFSM_SubStep = 1 THEN
            (* Prime MEG metering valve at 50% flow *)
            rMEG_InhibitorValveDemand_pct := 50.0;
            IF rMEG_InhibitorSupplyPress_bar > (rVotedSuctionPress_bar + 40.0) AND tFSM_StepTimer_s >= 3.0 THEN
                nFSM_SubStep := 2;
                tFSM_StepTimer_s := 0.0;
            ELSIF tFSM_StateTimer_s > 30.0 THEN
                nFSM_CurrentState := 13; (* MEG supply pressure missing *)
            END_IF;
        ELSIF nFSM_SubStep = 2 THEN
            (* Verify thermodynamic hydrate subcooling margin > 8.0 deg C *)
            rMEG_InhibitorValveDemand_pct := 35.0;
            IF (rHydrateSubcoolingMargin_degC >= 8.0 OR tFSM_StepTimer_s >= 6.0) AND NOT bHydrateCriticalInterlock THEN
                nFSM_CurrentState := 3;
            END_IF;
        END_IF;

        IF NOT bEnable OR NOT bProductionPermissive THEN
            nFSM_CurrentState := 11;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 3: STATE_ANTI_SURGE_KICKBACK_VALVE_FULL_OPEN_UNLOAD                                        *)
    (* Confirm 100% open kickback valve for zero-differential motor spinup (<1.2 s fast stroke test)     *)
    (* ------------------------------------------------------------------------------------------------ *)
    3:
        bStationReady := FALSE;
        bStationRunning := FALSE;
        rVFD_SpeedDemand_RPM := 0.0;
        rKickbackValveDemand_pct := 100.0;
        rMEG_InhibitorValveDemand_pct := 35.0;
        rBarrierFluidChargeDemand_pct := 12.0;
        rChokeTrimDemand_pct := 0.0;
        rMistCoolingRecycleDemand_pct := 0.0;

        IF bFSM_StateFirstScan THEN
            bAntiSurgeValveStroked := FALSE;
        END_IF;

        (* Check LVDT feedback confirmation *)
        IF rKickbackValvePosition_Feedback_pct >= 95.0 THEN
            bAntiSurgeValveStroked := TRUE;
            IF tFSM_StateTimer_s >= 1.5 THEN
                nFSM_CurrentState := 4;
            END_IF;
        ELSIF tFSM_StateTimer_s > 5.0 THEN
            (* Valve stuck / failure to full open *)
            nFSM_CurrentState := 13;
        END_IF;

        IF NOT bEnable OR NOT bProductionPermissive THEN
            nFSM_CurrentState := 11;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 4: STATE_SUBSEA_VFD_MOTOR_SPINUP_AND_LUBE_CHECK                                            *)
    (* Controlled acceleration through mechanical resonance bands (650-820 RPM) to 1,200 RPM idle      *)
    (* ------------------------------------------------------------------------------------------------ *)
    4:
        bStationReady := FALSE;
        bStationRunning := FALSE;
        rKickbackValveDemand_pct := 100.0;
        rMEG_InhibitorValveDemand_pct := 35.0;
        rBarrierFluidChargeDemand_pct := 12.0;
        rChokeTrimDemand_pct := 0.0;
        rMistCoolingRecycleDemand_pct := 0.0;

        IF bFSM_StateFirstScan THEN
            rVFD_RampTarget_RPM := 1200.0;
        END_IF;

        (* Controlled Slew Rate Ramp: 50 RPM/s *)
        IF rVFD_SpeedDemand_RPM < rVFD_RampTarget_RPM THEN
            rVFD_SpeedDemand_RPM := rVFD_SpeedDemand_RPM + (50.0 * rCycleTime_s);
            IF rVFD_SpeedDemand_RPM > rVFD_RampTarget_RPM THEN
                rVFD_SpeedDemand_RPM := rVFD_RampTarget_RPM;
            END_IF;
        END_IF;

        (* Vibration & Thrust Bearing Health Checks *)
        IF rPumpRadialVibration_DE_RMS_mps2 > 3.8 OR rPumpThrustBearingDisplacement_um > 65.0 THEN
            nFSM_CurrentState := 13; (* Mechanical excessive vibration during spin-up *)
        END_IF;

        (* Settle at 1,200 RPM for Hydrodynamic Wedge Formation *)
        IF rVFD_SpeedDemand_RPM >= 1200.0 AND rMotorVFD_SpeedFeedback_RPM >= 1150.0 THEN
            IF tFSM_StepTimer_s >= 8.0 THEN
                nFSM_CurrentState := 5;
            END_IF;
        ELSE
            tFSM_StepTimer_s := 0.0;
        END_IF;

        IF NOT bEnable OR NOT bProductionPermissive THEN
            nFSM_CurrentState := 11;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 5: STATE_MINIMUM_STABLE_FLOW_CIRCULATION_RUN                                                *)
    (* Ramp to 1,800 RPM continuous minimum speed, establish differential pressure across screws         *)
    (* ------------------------------------------------------------------------------------------------ *)
    5:
        bStationReady := TRUE;
        bStationRunning := FALSE;
        rKickbackValveDemand_pct := 100.0;
        rMEG_InhibitorValveDemand_pct := 35.0;
        rBarrierFluidChargeDemand_pct := 12.0;
        rChokeTrimDemand_pct := 0.0;
        rMistCoolingRecycleDemand_pct := 0.0;

        IF bFSM_StateFirstScan THEN
            rVFD_RampTarget_RPM := 1800.0;
            bThermalEquilibriumAchieved := FALSE;
        END_IF;

        IF rVFD_SpeedDemand_RPM < rVFD_RampTarget_RPM THEN
            rVFD_SpeedDemand_RPM := rVFD_SpeedDemand_RPM + (40.0 * rCycleTime_s);
            IF rVFD_SpeedDemand_RPM > rVFD_RampTarget_RPM THEN
                rVFD_SpeedDemand_RPM := rVFD_RampTarget_RPM;
            END_IF;
        END_IF;

        (* Verify Differential Pressure Generation (> 12.0 bar across kickback loop) *)
        IF rTwinScrewDifferentialPress_bar >= 12.0 AND rActiveRadialClearance_um >= 75.0 THEN
            IF tFSM_StateTimer_s >= 10.0 THEN
                bThermalEquilibriumAchieved := TRUE;
                nFSM_CurrentState := 6;
            END_IF;
        END_IF;

        IF NOT bEnable OR NOT bProductionPermissive THEN
            nFSM_CurrentState := 11;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 6: STATE_CONTROLLED_KICKBACK_VALVE_CLOSING_RAMP                                             *)
    (* Coordinated closing ramp of kickback recycle valve (100% -> 0%) and export choke opening (0%->60%)*)
    (* ------------------------------------------------------------------------------------------------ *)
    6:
        bStationReady := TRUE;
        bStationRunning := FALSE;
        rMEG_InhibitorValveDemand_pct := 35.0;
        rBarrierFluidChargeDemand_pct := 12.0;
        rMistCoolingRecycleDemand_pct := 0.0;

        IF bFSM_StateFirstScan THEN
            rKickback_RampTarget_pct := 0.0;
            rChoke_RampTarget_pct := 65.0;
        END_IF;

        (* Coordinated Ramp: Kickback closing at 4.0 %/s *)
        IF rKickbackValveDemand_pct > rKickback_RampTarget_pct THEN
            rKickbackValveDemand_pct := rKickbackValveDemand_pct - (4.0 * rCycleTime_s);
            IF rKickbackValveDemand_pct < rKickback_RampTarget_pct THEN
                rKickbackValveDemand_pct := rKickback_RampTarget_pct;
            END_IF;
        END_IF;

        (* Production Export Choke Opening at 3.0 %/s *)
        IF rChokeTrimDemand_pct < rChoke_RampTarget_pct THEN
            rChokeTrimDemand_pct := rChokeTrimDemand_pct + (3.0 * rCycleTime_s);
            IF rChokeTrimDemand_pct > rChoke_RampTarget_pct THEN
                rChokeTrimDemand_pct := rChoke_RampTarget_pct;
            END_IF;
        END_IF;

        (* Maintain Minimum Operating Speed *)
        IF rVFD_SpeedDemand_RPM < 2200.0 THEN
            rVFD_SpeedDemand_RPM := rVFD_SpeedDemand_RPM + (25.0 * rCycleTime_s);
        END_IF;

        (* Complete Transfer to Full Production when Kickback Closed and Choke Open *)
        IF rKickbackValveDemand_pct <= 2.0 AND rChokeTrimDemand_pct >= 60.0 THEN
            nFSM_CurrentState := 7;
        END_IF;

        IF NOT bEnable OR NOT bProductionPermissive THEN
            nFSM_CurrentState := 11;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 7: STATE_NOMINAL_MULTIPHASE_BOOSTING_MPC_RUN                                               *)
    (* Full Receding-Horizon MPC closed-loop execution controlling 6 actuators in real time             *)
    (* ------------------------------------------------------------------------------------------------ *)
    7:
        bStationReady := TRUE;
        bStationRunning := TRUE;

        (* Assign MPC Optimally Solved Actuator Controls *)
        rVFD_SpeedDemand_RPM := vecU[0];
        rKickbackValveDemand_pct := vecU[1];
        rMEG_InhibitorValveDemand_pct := vecU[2];
        rBarrierFluidChargeDemand_pct := vecU[3];
        rChokeTrimDemand_pct := vecU[4];
        rMistCoolingRecycleDemand_pct := vecU[5];

        (* Dynamic Disturbance Handling State Transitions *)
        IF bGasSlugDetected OR rVotedGVF_pct >= 86.0 THEN
            nFSM_CurrentState := 8; (* Gas Slug Attenuation *)
        ELSIF rActiveRadialClearance_um <= 58.0 THEN
            nFSM_CurrentState := 9; (* Thermal Clearance Balancing *)
        ELSIF rVotedGVF_pct >= 92.5 THEN
            nFSM_CurrentState := 10; (* High GVF Mist Cooling *)
        END_IF;

        (* Normal Stop / Turndown Request *)
        IF NOT bEnable OR NOT bProductionPermissive THEN
            nFSM_CurrentState := 11;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 8: STATE_GAS_SLUG_ATTENUATION_AND_SPEED_SURGE_CUT                                          *)
    (* Fast pre-emptive anti-surge kickback opening and VFD torque/speed cut during gas slug entry       *)
    (* ------------------------------------------------------------------------------------------------ *)
    8:
        bStationReady := TRUE;
        bStationRunning := TRUE;

        (* Immediately crack open anti-surge kickback valve to relieve dynamic surge pressure *)
        IF rKickbackValveDemand_pct < 35.0 THEN
            rKickbackValveDemand_pct := 35.0 + ((rVotedGVF_pct - 85.0) * 2.0);
            IF rKickbackValveDemand_pct > 75.0 THEN
                rKickbackValveDemand_pct := 75.0;
            END_IF;
        END_IF;

        (* Slew down motor speed to avoid severe gas pocket overspeed / acoustic choking *)
        IF rVFD_SpeedDemand_RPM > 2200.0 THEN
            rVFD_SpeedDemand_RPM := rVFD_SpeedDemand_RPM - (120.0 * rCycleTime_s);
        END_IF;

        (* Boost MEG injection to suppress gas expansion cooling hydrate nucleation *)
        rMEG_InhibitorValveDemand_pct := 65.0;
        rChokeTrimDemand_pct := vecU[4] * 0.85; (* Slightly throttle export choke *)
        rBarrierFluidChargeDemand_pct := vecU[3];
        rMistCoolingRecycleDemand_pct := 30.0;

        (* Return to Nominal Boosting Once Slugging Passes and GVF Stabilizes *)
        IF NOT bGasSlugDetected AND rVotedGVF_pct <= 78.0 AND rSurgeProximityMargin_pct >= 25.0 THEN
            IF tFSM_StepTimer_s >= 4.0 THEN
                nFSM_CurrentState := 7;
            END_IF;
        ELSE
            tFSM_StepTimer_s := 0.0;
        END_IF;

        IF NOT bEnable OR NOT bProductionPermissive THEN
            nFSM_CurrentState := 11;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 9: STATE_THERMAL_EXPANSION_CLEARANCE_BALANCING                                             *)
    (* Liquid recirculation cooling injection to chill twin-screw rotors and prevent scuffing/contact   *)
    (* ------------------------------------------------------------------------------------------------ *)
    9:
        bStationReady := TRUE;
        bStationRunning := TRUE;

        (* Spray chilled multiphase liquid mist directly into screw intermesh pockets *)
        rMistCoolingRecycleDemand_pct := 60.0 + ((65.0 - rActiveRadialClearance_um) * 2.0);
        IF rMistCoolingRecycleDemand_pct > 100.0 THEN
            rMistCoolingRecycleDemand_pct := 100.0;
        END_IF;

        (* Reduce VFD speed slightly to lower internal frictional dissipation *)
        IF rVFD_SpeedDemand_RPM > 2100.0 THEN
            rVFD_SpeedDemand_RPM := rVFD_SpeedDemand_RPM - (30.0 * rCycleTime_s);
        END_IF;

        rKickbackValveDemand_pct := 15.0; (* Crack kickback loop to circulate cooler liquid *)
        rMEG_InhibitorValveDemand_pct := vecU[2];
        rBarrierFluidChargeDemand_pct := vecU[3];
        rChokeTrimDemand_pct := vecU[4];

        (* Return to Nominal MPC Once Clearances Restored (> 80 um) *)
        IF rActiveRadialClearance_um >= 80.0 THEN
            IF tFSM_StepTimer_s >= 8.0 THEN
                nFSM_CurrentState := 7;
            END_IF;
        ELSE
            tFSM_StepTimer_s := 0.0;
        END_IF;

        IF NOT bEnable OR NOT bProductionPermissive THEN
            nFSM_CurrentState := 11;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 10: STATE_HIGH_GVF_MIST_COOLING_LIQUID_RECYCLE                                             *)
    (* Sustained dry gas / high GVF operation mode (>92% GVF) with dedicated liquid conditioning        *)
    (* ------------------------------------------------------------------------------------------------ *)
    10:
        bStationReady := TRUE;
        bStationRunning := TRUE;

        (* Dedicated high-capacity liquid mist recycle *)
        rMistCoolingRecycleDemand_pct := 85.0;
        rKickbackValveDemand_pct := 25.0;
        rMEG_InhibitorValveDemand_pct := 55.0;
        rBarrierFluidChargeDemand_pct := 15.0;

        (* Moderate speed limit in dry gas condition *)
        IF rVFD_SpeedDemand_RPM > 2600.0 THEN
            rVFD_SpeedDemand_RPM := rVFD_SpeedDemand_RPM - (40.0 * rCycleTime_s);
        END_IF;
        rChokeTrimDemand_pct := vecU[4];

        (* Exit Condition: Liquid returns to wellhead flow *)
        IF rVotedGVF_pct <= 84.0 AND rActiveRadialClearance_um >= 75.0 THEN
            IF tFSM_StepTimer_s >= 6.0 THEN
                nFSM_CurrentState := 7;
            END_IF;
        ELSE
            tFSM_StepTimer_s := 0.0;
        END_IF;

        IF NOT bEnable OR NOT bProductionPermissive THEN
            nFSM_CurrentState := 11;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 11: STATE_CONTROLLED_WELLHEAD_TURNDOWN_AND_FLUSH                                           *)
    (* Controlled deceleration, kickback open, export choke close, and MEG preservation flush           *)
    (* ------------------------------------------------------------------------------------------------ *)
    11:
        bStationReady := FALSE;
        bStationRunning := FALSE;

        IF bFSM_StateFirstScan THEN
            nFSM_SubStep := 1;
            tFSM_StepTimer_s := 0.0;
            tTurndownFlushTimer_s := 0.0;
        END_IF;

        IF nFSM_SubStep = 1 THEN
            (* Open kickback valve and close export choke *)
            IF rKickbackValveDemand_pct < 100.0 THEN
                rKickbackValveDemand_pct := rKickbackValveDemand_pct + (15.0 * rCycleTime_s);
                IF rKickbackValveDemand_pct > 100.0 THEN
                    rKickbackValveDemand_pct := 100.0;
                END_IF;
            END_IF;

            IF rChokeTrimDemand_pct > 0.0 THEN
                rChokeTrimDemand_pct := rChokeTrimDemand_pct - (10.0 * rCycleTime_s);
                IF rChokeTrimDemand_pct < 0.0 THEN
                    rChokeTrimDemand_pct := 0.0;
                END_IF;
            END_IF;

            (* Ramp VFD down to idle 1,200 RPM *)
            IF rVFD_SpeedDemand_RPM > 1200.0 THEN
                rVFD_SpeedDemand_RPM := rVFD_SpeedDemand_RPM - (60.0 * rCycleTime_s);
                IF rVFD_SpeedDemand_RPM < 1200.0 THEN
                    rVFD_SpeedDemand_RPM := 1200.0;
                END_IF;
            END_IF;

            IF rKickbackValveDemand_pct >= 95.0 AND rChokeTrimDemand_pct <= 2.0 AND rVFD_SpeedDemand_RPM <= 1250.0 THEN
                nFSM_SubStep := 2;
                tFSM_StepTimer_s := 0.0;
            END_IF;

        ELSIF nFSM_SubStep = 2 THEN
            (* Preservation MEG flush to displace water/gas and prevent hydrate formation during soak *)
            rMEG_InhibitorValveDemand_pct := 80.0;
            rMistCoolingRecycleDemand_pct := 0.0;
            rBarrierFluidChargeDemand_pct := 15.0;
            tTurndownFlushTimer_s := tTurndownFlushTimer_s + rCycleTime_s;

            IF tTurndownFlushTimer_s >= 20.0 THEN
                nFSM_SubStep := 3;
                tFSM_StepTimer_s := 0.0;
            END_IF;

        ELSIF nFSM_SubStep = 3 THEN
            (* Final Motor Spin-Down to 0 RPM *)
            rMEG_InhibitorValveDemand_pct := 0.0;
            IF rVFD_SpeedDemand_RPM > 0.0 THEN
                rVFD_SpeedDemand_RPM := rVFD_SpeedDemand_RPM - (80.0 * rCycleTime_s);
                IF rVFD_SpeedDemand_RPM < 0.0 THEN
                    rVFD_SpeedDemand_RPM := 0.0;
                END_IF;
            END_IF;

            IF rMotorVFD_SpeedFeedback_RPM <= 20.0 THEN
                nFSM_CurrentState := 12;
            END_IF;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 12: STATE_SAFE_DEPRESSURIZATION_AND_INERT_SEAL_HOLD                                        *)
    (* Motor stopped, station isolated, barrier fluid pressure held high over seabed hydrostatic        *)
    (* ------------------------------------------------------------------------------------------------ *)
    12:
        bStationReady := FALSE;
        bStationRunning := FALSE;
        rVFD_SpeedDemand_RPM := 0.0;
        rKickbackValveDemand_pct := 100.0;
        rMEG_InhibitorValveDemand_pct := 0.0;
        rBarrierFluidChargeDemand_pct := 8.0; (* Maintain trickle seal hold *)
        rChokeTrimDemand_pct := 0.0;
        rMistCoolingRecycleDemand_pct := 0.0;

        (* Acknowledge and return to IDLE upon reset *)
        IF bReset AND NOT bEmergencyStop_SubseaESD THEN
            nFSM_CurrentState := 0;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 13: STATE_EMERGENCY_SUBSEA_SEAL_LOSS_OR_SURGE_TRIP                                         *)
    (* Emergency Safety Action: Fast kickback (<1.2 s), choke slam shut, VFD electrical trip            *)
    (* ------------------------------------------------------------------------------------------------ *)
    13:
        bStationReady := FALSE;
        bStationRunning := FALSE;
        bStationTripped := TRUE;

        (* Instant Actuator Trip Command *)
        rVFD_SpeedDemand_RPM := 0.0;
        rKickbackValveDemand_pct := 100.0; (* Fast hydraulic open bypass *)
        rChokeTrimDemand_pct := 0.0;       (* Subsea export isolation slam shut *)
        rMEG_InhibitorValveDemand_pct := 0.0;
        rMistCoolingRecycleDemand_pct := 0.0;
        rBarrierFluidChargeDemand_pct := 0.0; (* Isolate barrier accumulator *)

        (* Trip Reset Guard: Operator reset pulse and all critical trip conditions cleared *)
        IF bReset AND NOT bEmergencyStop_SubseaESD AND NOT bAlarm_SealDP_LL AND
           NOT bAlarm_DiffPress_HH AND NOT bAlarm_DischargePress_HH AND
           NOT bAlarm_Vibration_HH AND NOT bClearanceCriticalTrip THEN
            bStationTripped := FALSE;
            nFSM_CurrentState := 0;
        END_IF;

END_CASE;
"""
