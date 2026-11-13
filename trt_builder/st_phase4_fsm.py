# trt_builder/st_phase4_fsm.py
"""
Phase 4: Deterministic 14-Stage Production Finite State Machine
for FB_Steel_BlastFurnace_TopGas_TRT_PowerRecovery
"""

def get_phase4_fsm():
    return """(* ==================================================================================================== *)
(* PHASE 4: 14-STAGE DETERMINISTIC PRODUCTION FINITE STATE MACHINE (FSM)                                 *)
(* ==================================================================================================== *)

(* Monotonic State Timer Accumulation *)
IF eFsmCurrentState = eFsmPreviousState THEN
    nFsmStateTimer_ms := nFsmStateTimer_ms + 10;
ELSE
    nFsmStateTimer_ms := 0;
    nFsmStateStep := 0;
    eFsmPreviousState := eFsmCurrentState;
END_IF;

(* Runtime Scouring Clock Accumulation *)
IF bTRT_PowerRecoveryActive THEN
    IF (nCycleCounter MOD 100) = 0 THEN
        nScouringAccumulator_s := nScouringAccumulator_s + 1;
    END_IF;
END_IF;

(* Supervisory Master Precondition Interlock Verification *)
bSystemReadyToStart := bGoggleValveUpstream_Open AND bGoggleValveDownstream_Open
                       AND bLubeOilPumpsRunning AND (rLubeOilSupplyPress_PT801 > cLubeOilPress_AlarmL)
                       AND (rN2SealGasDiffPress_DPT901 > cN2SealDiffPress_AlarmL)
                       AND (rGasOxygenConcentration_AT101 < cOxygenConc_TripHH)
                       AND (rHydraulicSupplyPress_PT803 > 150.0)
                       AND (rFastBypassAccumPress_PT804 > 150.0)
                       AND bTurbineTripSolenoidsHealthy
                       AND (NOT bEmergencyMasterTripActive);

(* Active State Output *)
nActiveFSMState := eFsmCurrentState;

(* ---------------------------------------------------------------------------------------------------- *)
(* FSM STATE TRANSITION & EXECUTION ENGINE                                                              *)
(* ---------------------------------------------------------------------------------------------------- *)
CASE eFsmCurrentState OF

    (* ------------------------------------------------------------------------------------------------ *)
    (* STAGE 0: COLD SYSTEM ISOLATION & INTERLOCK STANDBY                                               *)
    (* ------------------------------------------------------------------------------------------------ *)
    0:
        (* Commanded Actuator Standby Configuration *)
        rVSV_Demand_RateClamped      := 0.0;
        rSeptumV1_Demand_RateClamped := 35.0;
        rSeptumV2_Demand_RateClamped := 25.0;
        rSeptumV3_Demand_RateClamped := 15.0;

        bFastBypassValve_TripOpen         := FALSE;
        bInletESV_TripClose               := TRUE;  (* Keep Inlet ESV Closed *)
        bBleederValves_EmergencyCrackOpen := FALSE;
        bGeneratorBreaker_TripOpen        := TRUE;  (* Keep 52G Breaker Disconnected *)
        bGeneratorBreaker_ClosePermissive := FALSE;
        bScouringSpraySolenoid_Open       := FALSE;
        bCasingN2Purge_Solenoid_Open      := FALSE;
        bTRT_PowerRecoveryActive          := FALSE;
        bClosedLoopPressureLocked         := FALSE;

        (* Transition: Initiate TRT Pre-Commissioning Start Sequence *)
        IF bStartSequence AND bSystemReadyToStart AND (NOT bEmergencyMasterTripActive) THEN
            eFsmCurrentState := 1; (* Advance to Nitrogen Inert Purge *)
        END_IF;


    (* ------------------------------------------------------------------------------------------------ *)
    (* STAGE 1: NITROGEN INERT CASING PURGE                                                             *)
    (* Purge oxygen and hazardous volatile pockets; verify O2 < 0.50 vol%                               *)
    (* ------------------------------------------------------------------------------------------------ *)
    1:
        bCasingN2Purge_Solenoid_Open := TRUE;
        bInletESV_TripClose          := TRUE;
        rVSV_Demand_RateClamped      := 0.0;
        nPurgeTimer_ms := nPurgeTimer_ms + 10;

        (* Keep Septum Valves Modulating on Base BF Gas Flow *)
        rSeptumV1_Demand_RateClamped := rSeptumV1_Demand_Unclamped;
        rSeptumV2_Demand_RateClamped := rSeptumV2_Demand_Unclamped;
        rSeptumV3_Demand_RateClamped := rSeptumV3_Demand_Unclamped;

        (* Verify 180s Casing Purge Dwell and Low Oxygen Concentration *)
        IF (nPurgeTimer_ms >= 180000) AND (rGasOxygenConcentration_AT101 < 0.50) THEN
            bCasingN2Purge_Solenoid_Open := FALSE;
            nPurgeTimer_ms := 0;
            eFsmCurrentState := 2; (* Advance to Bag Filter Qualifying *)
        ELSIF nPurgeTimer_ms > 300000 THEN
            (* Purge Timeout Alarm: Purge gas failed to eliminate oxygen *)
            bAlarm_Oxygen_HH := TRUE;
            eFsmCurrentState := 12; (* Emergency Trip *)
        END_IF;


    (* ------------------------------------------------------------------------------------------------ *)
    (* STAGE 2: DRY BAG FILTER DIFFERENTIAL PRESSURE & TEMPERATURE QUALIFYING                           *)
    (* Verify clean gas pathway, dust cake stability, and temperature safely above acid dew point       *)
    (* ------------------------------------------------------------------------------------------------ *)
    2:
        rVSV_Demand_RateClamped := 0.0;
        bInletESV_TripClose     := TRUE;

        (* Verify Bag Filter Operating Window *)
        IF (rVoted_BagFilterDiffPress >= 3.0) AND (rVoted_BagFilterDiffPress <= 7.5)
           AND (rTopGasInletTemp_TT102 >= cBagFilterTemp_AlarmL) AND (rTopGasInletTemp_TT102 <= cBagFilterTemp_AlarmH)
           AND bBagFilterPulseJet_Running THEN

            IF nFsmStateTimer_ms >= 5000 THEN
                eFsmCurrentState := 3; (* Advance to Septum Valve Pressure Lock *)
            END_IF;
        ELSE
            IF nFsmStateTimer_ms > 20000 THEN
                (* Gas condition not qualified for turbine admission *)
                eFsmCurrentState := 0; (* Fallback to Isolation *)
            END_IF;
        END_IF;


    (* ------------------------------------------------------------------------------------------------ *)
    (* STAGE 3: SEPTUM VALVE BANK THROTTLING PRESSURE LOCK                                              *)
    (* Establish 100% blast furnace top gas regulation via Septum Bank with +/- 2.0 kPa lock            *)
    (* ------------------------------------------------------------------------------------------------ *)
    3:
        rVSV_Demand_RateClamped := 0.0;
        bInletESV_TripClose     := TRUE;

        (* Septum Valves Actively Modulate to Hold 250.0 kPa *)
        rSeptumV1_Demand_RateClamped := rSeptumV1_Demand_Unclamped;
        rSeptumV2_Demand_RateClamped := rSeptumV2_Demand_Unclamped;
        rSeptumV3_Demand_RateClamped := rSeptumV3_Demand_Unclamped;

        (* Check Closed-Loop Top Pressure Stabilization *)
        IF ABS(rTopGasPressure_Deviation) <= rMaxAllowedPressureDev THEN
            IF nFsmStateTimer_ms >= 15000 THEN
                bClosedLoopPressureLocked := TRUE;
                IF bStartSequence THEN
                    eFsmCurrentState := 4; (* Advance to Lube Oil & Seal Gas *)
                END_IF;
            END_IF;
        ELSE
            bClosedLoopPressureLocked := FALSE;
        END_IF;


    (* ------------------------------------------------------------------------------------------------ *)
    (* STAGE 4: TRT LUBE OIL PRE-LUBRICATION, HYDROSTATIC JACKING & N2 SEAL GAS                         *)
    (* Lift shaft journals (> 40 um) and verify nitrogen labyrinth differential pressure > 18.0 kPa      *)
    (* ------------------------------------------------------------------------------------------------ *)
    4:
        bAuxLubeOilPump_StartCommand := TRUE;
        bJackingOilPump_StartCommand := TRUE;

        (* Verify Hydraulic Lubrication and Shaft Jacking Lift *)
        IF (rLubeOilSupplyPress_PT801 >= 2.6)
           AND (rJackingOilPress_PT802 >= 115.0)
           AND (rN2SealGasDiffPress_DPT901 >= 18.0)
           AND (rTurbineBearingTemp_TT502A < 65.0)
           AND (rTurbineBearingTemp_TT502B < 65.0) THEN

            IF nFsmStateTimer_ms >= 8000 THEN
                eFsmCurrentState := 5; (* Advance to ESV Open & Warmup *)
            END_IF;
        ELSE
            IF nFsmStateTimer_ms > 30000 THEN
                eFsmCurrentState := 0; (* Jacking/Seal Gas Timeout *)
            END_IF;
        END_IF;


    (* ------------------------------------------------------------------------------------------------ *)
    (* STAGE 5: TURBINE INLET EMERGENCY STOP VALVE (ESV) CRACK OPEN & WARMUP                            *)
    (* Slow thermal preheating of reaction turbine casing (< 2.5 deg C/min)                             *)
    (* ------------------------------------------------------------------------------------------------ *)
    5:
        bInletESV_TripClose := FALSE; (* Unlatch ESV Trip *)
        rVSV_Demand_RateClamped := 0.0;

        (* Maintain Septum Bank Holding Top Pressure *)
        rSeptumV1_Demand_RateClamped := rSeptumV1_Demand_Unclamped;
        rSeptumV2_Demand_RateClamped := rSeptumV2_Demand_Unclamped;
        rSeptumV3_Demand_RateClamped := rSeptumV3_Demand_Unclamped;

        nWarmupTimer_ms := nWarmupTimer_ms + 10;

        (* Check Warmup Dwell (60 seconds) and ESV Full Open Feedback *)
        IF (nWarmupTimer_ms >= 60000) AND (rInletESV_PositionFeedback > 95.0) THEN
            nWarmupTimer_ms := 0;
            eFsmCurrentState := 6; (* Advance to VSV Soft Acceleration *)
        ELSIF nWarmupTimer_ms > 120000 THEN
            (* ESV Failed to Open or Thermal Stress Exceeded *)
            eFsmCurrentState := 12; (* Emergency Trip *)
        END_IF;


    (* ------------------------------------------------------------------------------------------------ *)
    (* STAGE 6: VARIABLE STATOR VANE (VSV) SOFT ACCELERATION & CRITICAL SPEED TRANSIT                   *)
    (* Accelerate through critical resonant vibration zone (1,400 to 1,850 rpm) at > 150 rpm/s          *)
    (* ------------------------------------------------------------------------------------------------ *)
    6:
        (* Disengage Jacking Oil Pump Once Hydrodynamic Lift Formed (> 600 rpm) *)
        IF rTurbineSpeed_Filtered > 600.0 THEN
            bJackingOilPump_StartCommand := FALSE;
        END_IF;

        (* Controlled Stator Vane Opening to Accelerate Rotor *)
        IF rTurbineSpeed_Filtered < 1350.0 THEN
            (* Sub-Critical Acceleration Band *)
            rVSV_Demand_RateClamped := 16.5;
            nCriticalBandTimer_ms := 0;
        ELSIF (rTurbineSpeed_Filtered >= 1350.0) AND (rTurbineSpeed_Filtered <= 1900.0) THEN
            (* Critical Resonance Speed Band - Fast Transit Boost (+8% VSV) *)
            rVSV_Demand_RateClamped := 24.5;
            nCriticalBandTimer_ms := nCriticalBandTimer_ms + 10;

            (* Watchdog: Must Clear Resonance Band in Less than 12 Seconds *)
            IF nCriticalBandTimer_ms > 12000 THEN
                bAlarm_TurbineVib_HH := TRUE;
                eFsmCurrentState := 12; (* Trip: Critical Resonance Dwell Exceeded *)
            END_IF;
        ELSE
            (* Super-Critical Approach to Synchronous Speed *)
            nCriticalBandTimer_ms := 0;
            rVSV_Demand_RateClamped := 18.0;
        END_IF;

        (* Transition to Synchronizer at 2,900 rpm *)
        IF rTurbineSpeed_Filtered >= 2900.0 THEN
            eFsmCurrentState := 7; (* Advance to Grid Synchronization *)
        END_IF;


    (* ------------------------------------------------------------------------------------------------ *)
    (* STAGE 7: 3,000 RPM AUTOMATIC GRID SYNCHRONIZATION                                                *)
    (* Precision governor frequency trim (50.00 Hz +/- 0.05 Hz, slip < 0.1 Hz, phase < 5 deg)          *)
    (* ------------------------------------------------------------------------------------------------ *)
    7:
        nSyncWatchdog_ms := nSyncWatchdog_ms + 10;

        (* Fine Speed Governing via VSV Trim *)
        IF rTurbineSpeed_Filtered > 3005.0 THEN
            rVSV_Demand_RateClamped := rVSV_Demand_RateClamped - 0.045;
        ELSIF rTurbineSpeed_Filtered < 2995.0 THEN
            rVSV_Demand_RateClamped := rVSV_Demand_RateClamped + 0.045;
        END_IF;

        (* Check Synchronizer Permissive Interlock *)
        IF bSynchronizerPermissive AND (ABS(rTurbineSpeed_Filtered - rTurbineSpeed_Nominal) <= 3.0) THEN
            bGeneratorBreaker_ClosePermissive := TRUE;
            IF nFsmStateTimer_ms >= 2000 THEN
                eFsmCurrentState := 8; (* Advance to Generator Breaker Close *)
            END_IF;
        ELSE
            bGeneratorBreaker_ClosePermissive := FALSE;
            IF nSyncWatchdog_ms > 90000 THEN
                (* Synchronization Window Timeout *)
                nSyncWatchdog_ms := 0;
                eFsmCurrentState := 11; (* Controlled Unloading *)
            END_IF;
        END_IF;


    (* ------------------------------------------------------------------------------------------------ *)
    (* STAGE 8: 52G GENERATOR BREAKER CLOSE & INITIAL BASE LOAD PICKUP                                  *)
    (* Close 52G intertie breaker; immediately pickup > 1.5 MW to suppress reverse power motoring       *)
    (* ------------------------------------------------------------------------------------------------ *)
    8:
        bGeneratorBreaker_TripOpen        := FALSE;
        bGeneratorBreaker_ClosePermissive := TRUE;
        nBreakerCloseTimer_ms := nBreakerCloseTimer_ms + 10;

        (* Verify Breaker Closed Auxiliary Contact *)
        IF bGridBreakerClosed_Feedback THEN
            (* Rapidly Step VSV Open to Achieve 1.5 MW Base Load *)
            rVSV_Demand_RateClamped := 32.0;
            bTRT_PowerRecoveryActive := TRUE;

            IF (rVoted_GeneratorActivePower >= 1.5) AND (nFsmStateTimer_ms >= 3000) THEN
                nBreakerCloseTimer_ms := 0;
                eFsmCurrentState := 9; (* Advance to Parallel Coordinated MPC Tracking *)
            END_IF;
        ELSE
            IF nBreakerCloseTimer_ms > 5000 THEN
                (* Breaker Failed to Close *)
                bGeneratorBreaker_TripOpen := TRUE;
                eFsmCurrentState := 12; (* Trip *)
            END_IF;
        END_IF;


    (* ------------------------------------------------------------------------------------------------ *)
    (* STAGE 9: PARALLEL MULTI-VALVE TOP PRESSURE MPC TRACKING & 25 MW POWER RECOVERY                   *)
    (* High-Efficiency Power Recovery: VSV Takes Base Load; Septum Valve 3 Handles High-Speed Trim      *)
    (* ------------------------------------------------------------------------------------------------ *)
    9:
        bTRT_PowerRecoveryActive          := TRUE;
        bGeneratorBreaker_ClosePermissive := TRUE;
        bGeneratorBreaker_TripOpen        := FALSE;

        (* Slew-Rate Limited Actuator Output Commands from MPC Optimization *)
        rVSV_Demand_RateClamped      := rVSV_Demand_Unclamped;
        rSeptumV1_Demand_RateClamped := rSeptumV1_Demand_Unclamped;
        rSeptumV2_Demand_RateClamped := rSeptumV2_Demand_Unclamped;
        rSeptumV3_Demand_RateClamped := rSeptumV3_Demand_Unclamped;

        (* Periodic Rotor Dust Scouring Trigger (Every 8 Operating Hours) *)
        IF (nScouringAccumulator_s >= nScouringInterval_s) AND bScouringSprayHeader_PressOK THEN
            eFsmCurrentState := 10; (* Advance to Scouring Spray Sequence *)
        END_IF;

        (* Normal Stop Command Initiated by Operator *)
        IF bStopSequence THEN
            eFsmCurrentState := 11; (* Controlled Turbine Unloading *)
        END_IF;


    (* ------------------------------------------------------------------------------------------------ *)
    (* STAGE 10: AUTOMATED ROTOR BLADE DUST SCOURING SPRAY SEQUENCE                                     *)
    (* High-pressure atomized fluid wash of 1st/2nd reaction stages to prevent dust crust accretion     *)
    (* ------------------------------------------------------------------------------------------------ *)
    10:
        bScouringSpraySolenoid_Open := TRUE;
        nScouringCycleTimer_ms := nScouringCycleTimer_ms + 10;

        (* Hold VSV Constant during Washing to Avoid Thermal/Vibration Transients *)
        rVSV_Demand_RateClamped      := rVSV_Demand_Unclamped;
        rSeptumV1_Demand_RateClamped := rSeptumV1_Demand_Unclamped;
        rSeptumV2_Demand_RateClamped := rSeptumV2_Demand_Unclamped;
        rSeptumV3_Demand_RateClamped := rSeptumV3_Demand_Unclamped;

        (* 45-Second Washing Cycle Completed *)
        IF nScouringCycleTimer_ms >= 45000 THEN
            bScouringSpraySolenoid_Open := FALSE;
            nScouringCycleTimer_ms := 0;
            nScouringAccumulator_s := 0; (* Reset 8-Hour Clock *)
            eFsmCurrentState := 9;       (* Return to Coordinated MPC Tracking *)
        END_IF;

        (* Exhaust Temperature Drop Safety Interlock *)
        IF rTurbineExhaustTemp_TT202 < 72.0 THEN
            bScouringSpraySolenoid_Open := FALSE;
            eFsmCurrentState := 9; (* Abort wash to avoid low temperature dewpoint *)
        END_IF;


    (* ------------------------------------------------------------------------------------------------ *)
    (* STAGE 11: CONTROLLED TURBINE LOAD REJECTION & DESYNCHRONIZATION                                  *)
    (* Smooth load transfer to Septum Bank at 1.5 %/s, open 52G breaker, coast rotor                    *)
    (* ------------------------------------------------------------------------------------------------ *)
    11:
        nUnloadingRampTimer_ms := nUnloadingRampTimer_ms + 10;

        (* Gradually Ramp Down VSV while Opening Septum Valves *)
        IF rVSV_Demand_RateClamped > 5.0 THEN
            rVSV_Demand_RateClamped := rVSV_Demand_RateClamped - 0.015;
            rSeptumV3_Demand_RateClamped := rSeptumV3_Demand_RateClamped + 0.010;
            rSeptumV2_Demand_RateClamped := rSeptumV2_Demand_RateClamped + 0.005;
        ELSE
            rVSV_Demand_RateClamped := 0.0;
        END_IF;

        (* Once Power Drops Below 0.80 MW, Trip Open 52G Grid Breaker *)
        IF (rVoted_GeneratorActivePower <= 0.80) OR (rVSV_Demand_RateClamped <= 2.0) THEN
            bGeneratorBreaker_TripOpen := TRUE;
            bTRT_PowerRecoveryActive   := FALSE;
            bInletESV_TripClose        := TRUE;

            (* Re-engage Jacking Oil Pump as Speed Drops Below 600 rpm *)
            IF (rTurbineSpeed_Filtered < 600.0) AND (rTurbineSpeed_Filtered > 10.0) THEN
                bJackingOilPump_StartCommand := TRUE;
            END_IF;

            IF nUnloadingRampTimer_ms >= 45000 THEN
                nUnloadingRampTimer_ms := 0;
                eFsmCurrentState := 3; (* Return to Septum Throttling Pressure Lock *)
            END_IF;
        END_IF;


    (* ------------------------------------------------------------------------------------------------ *)
    (* STAGE 12: EMERGENCY FAST BYPASS TRIP (< 450 ms) & TRT HARDWARE ISOLATION                         *)
    (* Snap Fast Bypass Valve Open (< 450 ms); Slam Inlet ESV Shut (< 150 ms); Trip 52G Breaker         *)
    (* ------------------------------------------------------------------------------------------------ *)
    12:
        (* Critical SIL-3 Fast Actuation Commands *)
        bFastBypassValve_TripOpen         := TRUE;  (* Fast Bypass Valve Snaps 100% Open in < 450 ms *)
        bInletESV_TripClose               := TRUE;  (* TRT Inlet ESV Slams 100% Shut in < 150 ms *)
        bGeneratorBreaker_TripOpen        := TRUE;  (* Disconnect Generator Breaker Immediately *)
        bScouringSpraySolenoid_Open       := FALSE;
        bTRT_PowerRecoveryActive          := FALSE;
        rVSV_Demand_RateClamped           := 0.0;

        (* Slam Septum Valves Wide Open to Cushion BF Top Pressure Shockwave *)
        rSeptumV1_Demand_RateClamped := 85.0;
        rSeptumV2_Demand_RateClamped := 65.0;
        rSeptumV3_Demand_RateClamped := 50.0;

        (* Engage Jacking Oil Pump if Rotor Decelerates *)
        IF rTurbineSpeed_Filtered < 600.0 THEN
            bJackingOilPump_StartCommand := TRUE;
        END_IF;

        (* Check for Extreme Blast Furnace Top Overpressure Escaping to Bleeders *)
        IF rVoted_TopGasPressure >= cTopGasPress_TripHH THEN
            eFsmCurrentState := 13; (* Escalate to Bleeder Venting *)
        END_IF;

        (* Manual Trip Acknowledge and Reset Sequence *)
        IF bReset AND (NOT bHardwareMasterTripEngaged) AND (NOT bEmergencyTripManual) THEN
            nTripClearTimer_ms := nTripClearTimer_ms + 10;
            IF nTripClearTimer_ms >= 5000 THEN
                bEmergencyMasterTripActive := FALSE;
                bFastBypassValve_TripOpen  := FALSE;
                nTripClearTimer_ms := 0;
                eFsmCurrentState := 3; (* Return to Septum Pressure Lock *)
            END_IF;
        ELSE
            nTripClearTimer_ms := 0;
        END_IF;


    (* ------------------------------------------------------------------------------------------------ *)
    (* STAGE 13: FAILSAFE BLEEDER VENTING & BLAST FURNACE EMERGENCY RELIEF                              *)
    (* Hydraulic bleeder relief valves crack open to prevent catastrophic furnace structural rupture    *)
    (* ------------------------------------------------------------------------------------------------ *)
    13:
        bBleederValves_EmergencyCrackOpen := TRUE; (* Hydraulic Bleeder Valves Dump Gas to Atmosphere *)
        bFastBypassValve_TripOpen         := TRUE;
        bInletESV_TripClose               := TRUE;
        bGeneratorBreaker_TripOpen        := TRUE;
        rVSV_Demand_RateClamped           := 0.0;
        bTRT_PowerRecoveryActive          := FALSE;

        (* Open All Septum Valves to 100% Full Bore *)
        rSeptumV1_Demand_RateClamped := 100.0;
        rSeptumV2_Demand_RateClamped := 100.0;
        rSeptumV3_Demand_RateClamped := 100.0;

        (* De-escalate Bleeders Once Top Gas Pressure Drops into Safe Band *)
        IF (rVoted_TopGasPressure < (cTopGasPress_AlarmH - cTopGasPress_Hysteresis)) AND bReset THEN
            bBleederValves_EmergencyCrackOpen := FALSE;
            eFsmCurrentState := 12; (* Return to Emergency Bypass State *)
        END_IF;

ELSE
    eFsmCurrentState := 0; (* Failsafe State Trap *)
END_CASE;
"""
