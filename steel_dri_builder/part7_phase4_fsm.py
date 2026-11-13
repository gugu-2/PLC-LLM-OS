# steel_dri_builder/part7_phase4_fsm.py
"""
Part 7: Phase 4 - Deterministic 14-Stage Steelmaking Production Finite State Machine (FSM)
"""

def get_phase4_fsm():
    return """(* ==================================================================================================== *)
(* PHASE 4: DETERMINISTIC 14-STAGE STEELMAKING PRODUCTION FINITE STATE MACHINE (FSM)                    *)
(* ==================================================================================================== *)

(* 4.1 Update State Machine Dwell Timer *)
IF iState = iPrevState THEN
    tCurrentStateDwell := tCurrentStateDwell + tSampleTime;
ELSE
    tCurrentStateDwell := T#0ms;
    iPrevState := iState;
    iFSM_SubPhase := 0;
END_IF;

(* 4.2 Super-Priority Safety Instrumented Interlocks (SIL-3 Fast Gas Trip & Snort Dump) *)
IF bEmergencyStop OR bO2_Ingress_InterlockTripped OR (rPV_BustleTemp_Voted > rLimit_Bustle_HH) OR bTMR_CriticalFailureAlarm THEN
    IF iState <> 13 THEN
        iState := 13; (* SIL-3 Double Block & Bleed Gas Emergency Trip *)
        tCurrentStateDwell := T#0ms;
        IF bO2_Ingress_InterlockTripped THEN
            dwFirstOutWord := 16#00000001; (* Oxygen Ingress Fast Trip *)
        ELSIF bEmergencyStop THEN
            dwFirstOutWord := 16#00000002; (* Hardwired E-Stop Pushbutton *)
        ELSIF (rPV_BustleTemp_Voted > rLimit_Bustle_HH) THEN
            dwFirstOutWord := 16#00000004; (* Bustle Pipe Refractory Overheat HH *)
        ELSIF bTMR_CriticalFailureAlarm THEN
            dwFirstOutWord := 16#00000008; (* TMR Critical Sensor Array Loss *)
        END_IF;
    END_IF;
ELSIF bManualSnortDump OR (rPV_ShaftDP_Voted > rLimit_ShaftDP_HH) THEN
    IF (iState <> 12) AND (iState <> 13) THEN
        iState := 12; (* Emergency Nitrogen Snort Dump *)
        tCurrentStateDwell := T#0ms;
        IF (rPV_ShaftDP_Voted > rLimit_ShaftDP_HH) THEN
            dwFirstOutWord := 16#00000010; (* Shaft Differential Pressure Severe Overpressure HH *)
        ELSE
            dwFirstOutWord := 16#00000020; (* Operator Manual Snort Dump Initiated *)
        END_IF;
    END_IF;
END_IF;

(* 4.3 14-Stage Deterministic FSM Execution Logic *)
CASE iState OF

    (* ------------------------------------------------------------------------------------------------ *)
    (* STAGE 0: FURNACE COLD NITROGEN INERT STANDBY                                                     *)
    (* ------------------------------------------------------------------------------------------------ *)
    0:
        bESD_GasTrip_SlamShut := FALSE;
        bESD_Vent_Bleed_Open := FALSE;
        bRoof_Snort_Dump_Open := FALSE;
        bNitrogen_Purge_Valve_Cmd := TRUE;
        bCluster_Breaker_Vibrator_Cmd := FALSE;
        bPellet_Feed_Permissive := FALSE;
        bDischarge_Feeder_Permissive := FALSE;
        bHeater_Ignition_Permissive := FALSE;
        bFurnaceReady := FALSE;

        (* Actuators Parked in Safe Neutral Positions *)
        u_Act[1] := 0.0; (* Green H2 Valve 0% *)
        u_Act[2] := 0.0; (* Reformed Syngas 0% *)
        u_Act[3] := 0.0; (* Preheater Fuel 0% *)
        u_Act[4] := 0.0; (* NatGas Trim 0% *)
        u_Act[5] := 15.0;(* Cooling Blower Minimum Idle Purge *)
        u_Act[6] := 0.0; (* Discharge Feeder Stopped *)

        rFSM_HeaterRampSP := 25.0;
        rFSM_H2FractionRamp := 0.0;

        IF bEnable AND bStartWarmup AND (NOT bEmergencyStop) AND (NOT bO2_Ingress_InterlockTripped) THEN
            iState := 1; (* Advance to Process Gas Heater Warmup *)
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STAGE 1: PROCESS GAS HEATER WARMUP RAMP (to 950 deg C)                                           *)
    (* ------------------------------------------------------------------------------------------------ *)
    1:
        bHeater_Ignition_Permissive := TRUE;
        bNitrogen_Purge_Valve_Cmd := TRUE;
        bPellet_Feed_Permissive := FALSE;
        bDischarge_Feeder_Permissive := FALSE;

        (* Linear Temperature Ramp Generator at Controlled Heat-up Rate (Max 45 deg C / h) *)
        IF rFSM_HeaterRampSP < 950.0 THEN
            rFSM_HeaterRampSP := rFSM_HeaterRampSP + (0.0125 * rTs_Seconds * 20.0);
        ELSE
            rFSM_HeaterRampSP := 950.0;
        END_IF;

        (* Proportional Burner Modulation to Track Refractory Heating Profile *)
        u_Act[1] := 0.0;
        u_Act[2] := 0.0;
        u_Act[3] := 18.0 + ((rFSM_HeaterRampSP - 25.0) / 925.0) * 48.0;
        u_Act[4] := 0.0;
        u_Act[5] := 35.0;
        u_Act[6] := 0.0;

        IF (rPV_BustleTemp_Voted >= 920.0) AND (tCurrentStateDwell >= T#5s) THEN
            iState := 2; (* Advance to Reducing Gas Injection *)
        ELSIF NOT bEnable THEN
            iState := 0;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STAGE 2: REDUCING GAS INJECTION AND HEAVY PURGE                                                  *)
    (* ------------------------------------------------------------------------------------------------ *)
    2:
        bHeater_Ignition_Permissive := TRUE;
        bNitrogen_Purge_Valve_Cmd := FALSE; (* Terminate Nitrogen Blanketing *)
        bPellet_Feed_Permissive := FALSE;
        bDischarge_Feeder_Permissive := FALSE;

        (* Smoothly Introduce Reformed Syngas to Displace Inerts through Flare Offtake *)
        u_Act[1] := 0.0;
        IF u_Act[2] < 42.0 THEN
            u_Act[2] := u_Act[2] + (0.85 * rTs_Seconds);
        ELSE
            u_Act[2] := 42.0;
        END_IF;
        u_Act[3] := 58.0; (* Maintain Preheater Duty *)
        u_Act[4] := 0.0;
        u_Act[5] := 40.0;
        u_Act[6] := 0.0;

        IF (rPV_TopGasH2CO_Voted >= 1.65) AND (u_Act[2] >= 40.0) AND (tCurrentStateDwell >= T#6s) THEN
            iState := 3; (* Advance to Pellet Charging *)
        ELSIF NOT bEnable THEN
            iState := 0;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STAGE 3: IRON ORE PELLET GRAVITY CHARGING INIT                                                   *)
    (* ------------------------------------------------------------------------------------------------ *)
    3:
        bPellet_Feed_Permissive := TRUE;
        bDischarge_Feeder_Permissive := FALSE;

        u_Act[1] := 0.0;
        u_Act[2] := 45.0;
        u_Act[3] := 62.0;
        u_Act[4] := 0.0;
        u_Act[5] := 45.0;
        u_Act[6] := 0.0;

        (* Wait until Burden Surface Level Reaches Nominal Working Bed Height (18.5 m) *)
        IF (rPV_BurdenLevel_Voted >= 18.2) AND (tCurrentStateDwell >= T#8s) THEN
            iState := 4; (* Advance to Thermal Equilibrium Bed Heating *)
        ELSIF NOT bEnable THEN
            iState := 0;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STAGE 4: THERMAL EQUILIBRIUM AND BED HEATING                                                     *)
    (* ------------------------------------------------------------------------------------------------ *)
    4:
        bPellet_Feed_Permissive := TRUE;
        bDischarge_Feeder_Permissive := FALSE;

        u_Act[1] := 0.0;
        u_Act[2] := 52.0;
        u_Act[3] := 66.0;
        u_Act[4] := 0.0;
        u_Act[5] := 50.0;
        u_Act[6] := 0.0;

        (* Confirm Core Reduction Zone Reaches Metallization Initiation Temperature (>850 deg C) *)
        IF (rPV_Estimated_InternalThermalBed >= 850.0) AND (rPV_Estimated_Metallization >= 48.0) AND (tCurrentStateDwell >= T#10s) THEN
            IF bStartHydrogenRamp THEN
                iState := 5; (* Advance to Green Hydrogen Ramp-Up *)
            ELSE
                iState := 6; (* Direct to Syngas Reduction MPC *)
            END_IF;
        ELSIF NOT bEnable THEN
            iState := 0;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STAGE 5: GREEN HYDROGEN ENRICHMENT RAMPUP (to 70% H2)                                            *)
    (* ------------------------------------------------------------------------------------------------ *)
    5:
        bPellet_Feed_Permissive := TRUE;
        bDischarge_Feeder_Permissive := TRUE;

        (* Coordinated Ramp: Increase H2 while Decreasing Syngas and Boosting Preheater *)
        IF rFSM_H2FractionRamp < 50.0 THEN
            rFSM_H2FractionRamp := rFSM_H2FractionRamp + (0.45 * rTs_Seconds);
        ELSE
            rFSM_H2FractionRamp := 50.0;
        END_IF;

        u_Act[1] := rFSM_H2FractionRamp;
        u_Act[2] := 55.0 - (rFSM_H2FractionRamp * 0.35);
        u_Act[3] := 65.0 + (rFSM_H2FractionRamp * 0.25);
        u_Act[4] := 5.0;
        u_Act[5] := 60.0;
        u_Act[6] := 30.0; (* Slow Initial Feeder Speed *)

        IF (u_Act[1] >= 48.0) AND (rPV_TopGasH2CO_Voted >= 2.60) AND (tCurrentStateDwell >= T#12s) THEN
            iState := 6; (* Advance to Optimal MPC Reduction Run *)
        ELSIF NOT bEnable THEN
            iState := 11;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STAGE 6: FULL METALLIZATION OPTIMAL MPC RUN (>94% Fe)                                            *)
    (* ------------------------------------------------------------------------------------------------ *)
    6:
        bFurnaceReady := TRUE;
        bPellet_Feed_Permissive := TRUE;
        bDischarge_Feeder_Permissive := TRUE;
        bHeater_Ignition_Permissive := TRUE;

        (* Actuators Dynamically Driven by Receding Horizon MPC with PGD in Phase 3 *)
        IF bClusterStickingWarning OR (rPV_ShaftDP_Voted > 76.0) THEN
            iState := 10; (* Detect Burden Clustering: Trigger Vibration Pulse *)
        ELSIF bInitiateHold THEN
            iState := 11; (* Process Gas Turndown Hold *)
        ELSIF (rPV_Estimated_Metallization >= 94.5) AND (tCurrentStateDwell >= T#15s) THEN
            iState := 7; (* Advance to Carbon Control Enrichment *)
        ELSIF NOT bEnable THEN
            iState := 11;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STAGE 7: PRODUCT CARBON CONTROL ENRICHMENT                                                       *)
    (* ------------------------------------------------------------------------------------------------ *)
    7:
        bFurnaceReady := TRUE;
        bPellet_Feed_Permissive := TRUE;
        bDischarge_Feeder_Permissive := TRUE;

        (* Modulate Natural Gas Carburization Injection into Lower Reduction Transition Cone *)
        IF bClusterStickingWarning OR (rPV_ShaftDP_Voted > 76.0) THEN
            iState := 10;
        ELSIF bInitiateHold THEN
            iState := 11;
        ELSIF (x_Hat[6] >= 2.10) AND (tCurrentStateDwell >= T#10s) THEN
            iState := 8; (* Advance to Bottom Cooling Gas Recycle Lock *)
        ELSIF NOT bEnable THEN
            iState := 11;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STAGE 8: BOTTOM COOLING GAS RECYCLE LOCK                                                         *)
    (* ------------------------------------------------------------------------------------------------ *)
    8:
        bFurnaceReady := TRUE;
        bPellet_Feed_Permissive := TRUE;
        bDischarge_Feeder_Permissive := TRUE;

        (* Establish Hermetic Cooling Circuit & Maintain Differential Seal Overpressure *)
        u_Act[5] := 78.0; (* Blower Inverter Nominal Speed *)

        IF (rPT_CoolingGas_701 >= 165.0) AND (rPV_DRITemp_Voted <= 720.0) AND (tCurrentStateDwell >= T#8s) THEN
            iState := 9; (* Advance to Continuous Pneumatic Discharge *)
        ELSIF bClusterStickingWarning THEN
            iState := 10;
        ELSIF bInitiateHold OR (NOT bEnable) THEN
            iState := 11;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STAGE 9: HOT DRI CONTINUOUS PNEUMATIC DISCHARGE                                                  *)
    (* ------------------------------------------------------------------------------------------------ *)
    9:
        bFurnaceReady := TRUE;
        bPellet_Feed_Permissive := TRUE;
        bDischarge_Feeder_Permissive := TRUE;

        (* Full Production: 150 t/h Discharge Output Under Full Closed-Loop MPC Coordination *)
        IF bClusterStickingWarning OR (rPV_ShaftDP_Voted > 78.0) THEN
            iState := 10; (* Burden Sticking Cluster Remediation *)
        ELSIF bInitiateHold OR (NOT bEnable) THEN
            iState := 11;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STAGE 10: BURDEN STICKING CHUNKING VIBRATION PULSE                                               *)
    (* ------------------------------------------------------------------------------------------------ *)
    10:
        bPellet_Feed_Permissive := TRUE;
        bDischarge_Feeder_Permissive := TRUE;

        (* Fire High-Pressure Pneumatic Shock Blasters & Dither Feeder Speed to Break Clinkers *)
        bCluster_Breaker_Vibrator_Cmd := TRUE;
        tClusterPulseTimer := tClusterPulseTimer + tSampleTime;
        udiClusterPulseCounter := udiClusterPulseCounter + 1;

        (* Relieve Reduction Zone Thermal Burden: Lower Preheater Duty and Speed Up Feeder *)
        u_Act[1] := u_Act[1] * 0.90;
        u_Act[3] := u_Act[3] - (0.45 * rTs_Seconds);
        IF u_Act[3] < 45.0 THEN u_Act[3] := 45.0; END_IF;
        u_Act[6] := 85.0; (* Agitate Lower Bed *)

        IF (rPV_ShaftDP_Voted <= 58.0) AND (tClusterPulseTimer >= T#3s) THEN
            bCluster_Breaker_Vibrator_Cmd := FALSE;
            tClusterPulseTimer := T#0ms;
            bClusterStickingWarning := FALSE;
            iState := 6; (* Return to Optimal MPC Reduction Run *)
        ELSIF tClusterPulseTimer >= T#30s THEN
            (* Unresolved Cluster Hanging: Turndown Furnace to Prevent Catastrophic Channeling *)
            bCluster_Breaker_Vibrator_Cmd := FALSE;
            tClusterPulseTimer := T#0ms;
            iState := 11;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STAGE 11: PROCESS GAS TURNDOWN RECYCLE HOLD                                                      *)
    (* ------------------------------------------------------------------------------------------------ *)
    11:
        bFurnaceReady := FALSE;
        bPellet_Feed_Permissive := FALSE;
        bDischarge_Feeder_Permissive := FALSE;
        bCluster_Breaker_Vibrator_Cmd := FALSE;

        (* Turndown Process Gas Flow and Lower Temperature to 750 deg C to Inhibit Solid-State Sintering *)
        IF u_Act[1] > 12.0 THEN u_Act[1] := u_Act[1] - (0.85 * rTs_Seconds); ELSE u_Act[1] := 12.0; END_IF;
        IF u_Act[2] > 28.0 THEN u_Act[2] := u_Act[2] - (0.85 * rTs_Seconds); ELSE u_Act[2] := 28.0; END_IF;
        IF u_Act[3] > 42.0 THEN u_Act[3] := u_Act[3] - (0.65 * rTs_Seconds); ELSE u_Act[3] := 42.0; END_IF;
        u_Act[4] := 0.0;
        u_Act[5] := 30.0;
        u_Act[6] := 0.0;

        IF bEnable AND bStartDischarge AND (NOT bInitiateHold) THEN
            iState := 6; (* Resume Full Production MPC *)
        ELSIF bReset AND (NOT bEnable) THEN
            iState := 0; (* Return to Cold Inert Standby *)
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STAGE 12: EMERGENCY NITROGEN SNORT DUMP (<50 ms)                                                 *)
    (* ------------------------------------------------------------------------------------------------ *)
    12:
        bFurnaceReady := FALSE;
        bPellet_Feed_Permissive := FALSE;
        bDischarge_Feeder_Permissive := FALSE;
        bCluster_Breaker_Vibrator_Cmd := FALSE;

        (* Fast Depressurization: Slam Open Roof Snort Valve & Blast Heavy Inert Nitrogen Blanket *)
        bRoof_Snort_Dump_Open := TRUE;
        bNitrogen_Purge_Valve_Cmd := TRUE;

        (* Slam Close All Combustible Process Gas Lines *)
        u_Act[1] := 0.0; (* Immediate H2 Cutoff *)
        u_Act[2] := 0.0; (* Syngas Cutoff *)
        u_Act[3] := 0.0; (* Preheater Fuel Cutoff *)
        u_Act[4] := 0.0; (* NatGas Cutoff *)
        u_Act[5] := 0.0;
        u_Act[6] := 0.0;

        tSnortDumpDuration := tSnortDumpDuration + tSampleTime;

        IF (rPV_ShaftDP_Voted <= 12.0) AND (tSnortDumpDuration >= T#6s) AND (NOT bManualSnortDump) AND (NOT (rPV_ShaftDP_Voted > rLimit_ShaftDP_HH)) THEN
            bRoof_Snort_Dump_Open := FALSE;
            tSnortDumpDuration := T#0ms;
            iState := 0; (* Return to Inert Standby for Inspection *)
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STAGE 13: SIL-3 DOUBLE BLOCK BLEED GAS TRIP (<20 ms)                                             *)
    (* ------------------------------------------------------------------------------------------------ *)
    13:
        bFurnaceReady := FALSE;
        bPellet_Feed_Permissive := FALSE;
        bDischarge_Feeder_Permissive := FALSE;
        bCluster_Breaker_Vibrator_Cmd := FALSE;
        bHeater_Ignition_Permissive := FALSE;

        (* Safety Instrumented Function (SIF) Trip: Slam Shut Fast Double-Block Valves *)
        bESD_GasTrip_SlamShut := TRUE;
        bESD_Vent_Bleed_Open := TRUE; (* Open Vent to Flare Bleed Header *)
        bRoof_Snort_Dump_Open := TRUE;
        bNitrogen_Purge_Valve_Cmd := TRUE;

        (* Zero All Control Outputs Instantly *)
        u_Act[1] := 0.0;
        u_Act[2] := 0.0;
        u_Act[3] := 0.0;
        u_Act[4] := 0.0;
        u_Act[5] := 0.0;
        u_Act[6] := 0.0;

        tDoubleBlockBleedTimer := tDoubleBlockBleedTimer + tSampleTime;

        (* Trip Can ONLY Be Cleared By Explicit Operator Master Reset With Safe Conditions *)
        IF bReset AND (NOT bEmergencyStop) AND (NOT bO2_Ingress_InterlockTripped) AND (rPV_BustleTemp_Voted <= (rLimit_Bustle_HH - rHyst_Bustle)) AND (NOT bTMR_CriticalFailureAlarm) THEN
            bESD_GasTrip_SlamShut := FALSE;
            bESD_Vent_Bleed_Open := FALSE;
            bRoof_Snort_Dump_Open := FALSE;
            tDoubleBlockBleedTimer := T#0ms;
            dwFirstOutWord := 16#00000000;
            iState := 0; (* Reset to Cold Inert Standby *)
        END_IF;

    ELSE
        iState := 0;
END_CASE;

eFurnaceState := iState;
"""
