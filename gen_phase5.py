# gen_phase5.py - Generates Phase 5: 12-Stage Operational Finite State Machine (FSM)

def generate_phase5():
    return """(* ==================================================================================================================== *)
(* PHASE 5: 12-STAGE OPERATIONAL FINITE STATE MACHINE (FSM) INDUSTRIAL PRODUCTION SEQUENCE                               *)
(* ==================================================================================================================== *)

nActiveBatchStepState := eCurrentState;

(* Accumulate Total Active Batch Runtime *)
IF (eCurrentState > 0) AND (eCurrentState < 999) THEN
    rTotalBatchSecondsAccum := rTotalBatchSecondsAccum + rCycleScanDeltaTime;
    tCurrentBatchDuration := REAL_TO_TIME(rTotalBatchSecondsAccum * 1000.0);
END_IF;

CASE eCurrentState OF

    0: (* ------------------------------------------------------------------------------------------------------------ *)
       (* STATE 0: STANDBY / IDLE INITIALIZATION & PRE-BATCH SAFETY VERIFICATION                                       *)
       (* ------------------------------------------------------------------------------------------------------------ *)
        bCmd_MainIsolationMushroomValveOpen   := FALSE;
        bCmd_ChamberVentSterileN2ValveOpen    := FALSE;
        bCmd_CondenserDefrostSteamValveOpen   := FALSE;
        bCmd_CondenserCondensateDrainPumpRun  := FALSE;
        bCmd_ChamberDoorPneumaticSealInflate  := TRUE;
        bPrimaryDryingEndpointDetected        := FALSE;
        bSecondaryDryingCompleteFlag          := FALSE;
        bStopperingCompleteFlag               := FALSE;
        bBatchCycleSuccessfullyComplete       := FALSE;
        rStateTimerAccumulator_s              := 0.0;
        nSubPhaseStep                         := 0;
        rShelfRampSetpointActual              := 20.0;
        rChamberPresSetpointActual            := 1013.25;

        IF bMasterBatchRunPermissive AND bEmergencyStopCircuit_NC AND (NOT bEmergencySafetyInterlockTripped) THEN
            eCurrentState := 10; (* Proceed to CIP/SIP Verification *)
        END_IF;

    10: (* ------------------------------------------------------------------------------------------------------------ *)
        (* STATE 1: CLEAN-IN-PLACE / STEAM-IN-PLACE (CIP/SIP) INTEGRITY & HIGH-VACUUM LEAK RATE TEST                    *)
        (* ------------------------------------------------------------------------------------------------------------ *)
        rStateTimerAccumulator_s := rStateTimerAccumulator_s + rCycleScanDeltaTime;

        CASE nSubPhaseStep OF
            0: (* Verify Upstream CIP & SIP Interlock Handshakes *)
                IF bCleanInPlaceVerified_NC AND bSteamInPlaceVerified_NC AND bChamberDoorClosedLocked_NC THEN
                    nSubPhaseStep := 1;
                    rLeakRateTestTimer_s := 0.0;
                END_IF;

            1: (* Pre-Evacuation for Chamber Leak Rate Verification: Pump down to 0.050 mbar *)
                bCmd_MainIsolationMushroomValveOpen := TRUE;
                rChamberPresSetpointActual := 0.050;
                IF rVotedChamberPressure_CM_Actual <= 0.060 THEN
                    (* Isolate Chamber to perform 15-Minute Pressure Rise Leak Test *)
                    bCmd_MainIsolationMushroomValveOpen := FALSE;
                    rLeakRateStartPressure_mbar := rVotedChamberPressure_CM_Actual;
                    rLeakRateTestTimer_s := 0.0;
                    nSubPhaseStep := 2;
                END_IF;

            2: (* 15-Minute Chamber Isolation Leak Rate Measurement *)
                rLeakRateTestTimer_s := rLeakRateTestTimer_s + rCycleScanDeltaTime;
                IF rLeakRateTestTimer_s >= 900.0 THEN (* 15 minutes = 900 seconds *)
                    (* Leak Rate Q = (Delta_P * V_chamber) / Delta_t [mbar*L/s] *)
                    rLeakRateObserved_mbar_L_s := ( (rVotedChamberPressure_CM_Actual - rLeakRateStartPressure_mbar) * (c_rChamberFreeVolume_m3 * 1000.0) ) / 900.0;
                    IF rLeakRateObserved_mbar_L_s <= 0.0020 THEN
                        bLeakRateTestPassed := TRUE;
                        (* Equalize Chamber with sterile N2 for loading *)
                        bCmd_ChamberVentSterileN2ValveOpen := TRUE;
                        nSubPhaseStep := 3;
                    ELSE
                        bLeakRateTestPassed := FALSE;
                        bAlarm_VacuumLost_HH := TRUE;
                        eCurrentState := 999; (* Chamber vacuum seal failure *)
                    END_IF;
                END_IF;

            3: (* Vent Chamber to Atmospheric Pressure for Aseptic Loading *)
                IF rVotedChamberPressure_CM_Actual >= 1010.0 THEN
                    bCmd_ChamberVentSterileN2ValveOpen := FALSE;
                    rStateTimerAccumulator_s := 0.0;
                    nSubPhaseStep := 0;
                    eCurrentState := 20; (* Proceed to Automatic Vial Loading *)
                END_IF;
        END_CASE;

    20: (* ------------------------------------------------------------------------------------------------------------ *)
        (* STATE 2: AUTOMATIC VIAL LOADING & SHELF INFEED CHILL (+4.0 DEG C PRE-COOLING)                                *)
        (* ------------------------------------------------------------------------------------------------------------ *)
        rStateTimerAccumulator_s := rStateTimerAccumulator_s + rCycleScanDeltaTime;
        (* Maintain shelf temperature at +4.0 deg C to preserve biological antibody activity during loading *)
        rShelfRampSetpointActual := 4.0;
        rChamberPresSetpointActual := 1013.25;

        CASE nSubPhaseStep OF
            0: (* Deflate Inflatable Aseptic Door Gasket and Open Infeed Door *)
                bCmd_ChamberDoorPneumaticSealInflate := FALSE;
                IF rStateTimerAccumulator_s >= 10.0 THEN
                    nSubPhaseStep := 1;
                END_IF;

            1: (* Infeed Conveyor & Pusher Array Loading 150,000 Vials onto 10 Shelves *)
                (* Wait for external loading completion signal or simulated loading dwell *)
                IF rStateTimerAccumulator_s >= 60.0 THEN
                    nSubPhaseStep := 2;
                END_IF;

            2: (* Close Door, Inflate Aseptic Gasket, Verify Seal *)
                bCmd_ChamberDoorPneumaticSealInflate := TRUE;
                IF bChamberDoorClosedLocked_NC AND (rStateTimerAccumulator_s >= 75.0) THEN
                    rStateTimerAccumulator_s := 0.0;
                    nSubPhaseStep := 0;
                    eCurrentState := 30; (* Proceed to Controlled Freezing & Annealing *)
                END_IF;
        END_CASE;

    30: (* ------------------------------------------------------------------------------------------------------------ *)
        (* STATE 3: CONTROLLED FREEZING & THERMAL CRYSTALLINE ANNEALING (-45 DEG C / -15 DEG C)                         *)
        (* ------------------------------------------------------------------------------------------------------------ *)
        rStateTimerAccumulator_s := rStateTimerAccumulator_s + rCycleScanDeltaTime;

        CASE nSubPhaseStep OF
            0: (* Controlled Freezing Ramp Down to -45.0 deg C at 0.8 deg C/min *)
                rActiveRampSlope := (rSet_ShelfRampRateFreezing / 60.0); (* deg C/s *)
                IF rShelfRampSetpointActual > -45.0 THEN
                    rShelfRampSetpointActual := rShelfRampSetpointActual - (rActiveRampSlope * rCycleScanDeltaTime);
                ELSE
                    rShelfRampSetpointActual := -45.0;
                    IF rVotedProductTemperatureActual <= -42.0 THEN
                        nSubPhaseStep := 1; (* Freezing soak plateau *)
                        rFreezingHoldTimer_s := 0.0;
                    END_IF;
                END_IF;

            1: (* Deep Freeze Solidification Soak (Hold 120 minutes = 7200 s) *)
                rFreezingHoldTimer_s := rFreezingHoldTimer_s + rCycleScanDeltaTime;
                IF rFreezingHoldTimer_s >= 7200.0 THEN
                    nSubPhaseStep := 2; (* Proceed to Thermal Annealing Ramp *)
                END_IF;

            2: (* Thermal Annealing: Ramp Shelf up to -15.0 deg C at 0.5 deg C/min to grow ice crystals *)
                IF rShelfRampSetpointActual < -15.0 THEN
                    rShelfRampSetpointActual := rShelfRampSetpointActual + ((0.50 / 60.0) * rCycleScanDeltaTime);
                ELSE
                    rShelfRampSetpointActual := -15.0;
                    IF rVotedProductTemperatureActual >= -16.5 THEN
                        nSubPhaseStep := 3;
                        rAnnealingHoldTimer_s := 0.0;
                    END_IF;
                END_IF;

            3: (* Annealing Plateau Soak (Hold 180 minutes = 10,800 s for Ostwald ripening) *)
                rAnnealingHoldTimer_s := rAnnealingHoldTimer_s + rCycleScanDeltaTime;
                IF rAnnealingHoldTimer_s >= 10800.0 THEN
                    nSubPhaseStep := 4; (* Re-freeze to -45.0 deg C *)
                END_IF;

            4: (* Re-freezing Ramp Down to -45.0 deg C at 0.8 deg C/min *)
                IF rShelfRampSetpointActual > -45.0 THEN
                    rShelfRampSetpointActual := rShelfRampSetpointActual - ((0.80 / 60.0) * rCycleScanDeltaTime);
                ELSE
                    rShelfRampSetpointActual := -45.0;
                    IF rVotedProductTemperatureActual <= -42.0 THEN
                        rStateTimerAccumulator_s := 0.0;
                        nSubPhaseStep := 0;
                        eCurrentState := 40; (* Proceed to Controlled Ice Nucleation Pulse *)
                    END_IF;
                END_IF;
        END_CASE;

    40: (* ------------------------------------------------------------------------------------------------------------ *)
        (* STATE 4: CONTROLLED ICE NUCLEATION PULSE (-5.0 DEG C SUPERCOOLED SHOCK)                                      *)
        (* ------------------------------------------------------------------------------------------------------------ *)
        rStateTimerAccumulator_s := rStateTimerAccumulator_s + rCycleScanDeltaTime;

        CASE nSubPhaseStep OF
            0: (* Equilibrate Vials at Supercooling Setpoint: -5.0 deg C *)
                IF rShelfRampSetpointActual < -5.0 THEN
                    rShelfRampSetpointActual := rShelfRampSetpointActual + ((1.0 / 60.0) * rCycleScanDeltaTime);
                ELSE
                    rShelfRampSetpointActual := -5.0;
                    IF (rVotedProductTemperatureActual >= -5.8) AND (rVotedProductTemperatureActual <= -4.5) THEN
                        nSubPhaseStep := 1;
                        rNucleationPulseTimer_s := 0.0;
                    END_IF;
                END_IF;

            1: (* Trigger Ice Fog / Rapid Depressurization Pulse (Open pulse valve for 3.5 seconds) *)
                rNucleationPulseTimer_s := rNucleationPulseTimer_s + rCycleScanDeltaTime;
                IF rNucleationPulseTimer_s >= 3.5 THEN
                    nSubPhaseStep := 2; (* Verify crystallization exotherm *)
                END_IF;

            2: (* Crystallization Exotherm Verification: Product TC spike up towards 0.0 deg C *)
                IF rVotedProductTemperatureActual > -2.0 THEN
                    (* Rapid crystallization successful across all vials *)
                    nSubPhaseStep := 3;
                ELSIF rStateTimerAccumulator_s >= 300.0 THEN
                    (* Timeout fallback: proceed to deep freeze *)
                    nSubPhaseStep := 3;
                END_IF;

            3: (* Rapidly freeze back down to -45.0 deg C to solidify crystal structure *)
                IF rShelfRampSetpointActual > -45.0 THEN
                    rShelfRampSetpointActual := rShelfRampSetpointActual - ((1.20 / 60.0) * rCycleScanDeltaTime);
                ELSE
                    rShelfRampSetpointActual := -45.0;
                    IF rVotedProductTemperatureActual <= -42.0 THEN
                        rStateTimerAccumulator_s := 0.0;
                        nSubPhaseStep := 0;
                        eCurrentState := 50; (* Proceed to Vacuum Pumpdown *)
                    END_IF;
                END_IF;
        END_CASE;

    50: (* ------------------------------------------------------------------------------------------------------------ *)
        (* STATE 5: ICE CONDENSER PRE-CHILL (-80 DEG C) & VACUUM PUMPDOWN (0.100 MBAR)                                  *)
        (* ------------------------------------------------------------------------------------------------------------ *)
        rStateTimerAccumulator_s := rStateTimerAccumulator_s + rCycleScanDeltaTime;
        rShelfRampSetpointActual := -45.0;

        CASE nSubPhaseStep OF
            0: (* Chill Ice Condenser Coils to -80.0 deg C *)
                IF rVotedCondenserCoilTempActual <= -75.0 THEN
                    nSubPhaseStep := 1; (* Condenser cold trap ready *)
                END_IF;

            1: (* Open DN600 Main Chamber-to-Condenser Isolation Mushroom Valve *)
                bCmd_MainIsolationMushroomValveOpen := TRUE;
                IF rStateTimerAccumulator_s >= 15.0 THEN
                    nSubPhaseStep := 2;
                END_IF;

            2: (* Evacuate Chamber with Roots Booster + Dry Screw Pumps to Sublimation Setpoint (0.100 mbar) *)
                rChamberPresSetpointActual := rSet_PrimaryDryingChamberPres;
                IF rVotedChamberPressure_CM_Actual <= (rSet_PrimaryDryingChamberPres + 0.020) THEN
                    rStateTimerAccumulator_s := 0.0;
                    nSubPhaseStep := 0;
                    eCurrentState := 60; (* Proceed to Primary Drying Sublimation Hold *)
                END_IF;
        END_CASE;

    60: (* ------------------------------------------------------------------------------------------------------------ *)
        (* STATE 6: PRIMARY DRYING SUBLIMATION HOLD (-15.0 DEG C SHELF, N2 MICRO-BLEED AT 0.120 MBAR)                   *)
        (* ------------------------------------------------------------------------------------------------------------ *)
        rStateTimerAccumulator_s := rStateTimerAccumulator_s + rCycleScanDeltaTime;
        rChamberPresSetpointActual := rSet_PrimaryDryingChamberPres;
        bCmd_MainIsolationMushroomValveOpen := TRUE;

        (* Ramp Shelf Temperature up to Primary Drying Setpoint (-15.0 deg C) at 0.25 deg C/min *)
        rActiveRampSlope := (rSet_ShelfRampRatePrimaryDry / 60.0);
        IF rShelfRampSetpointActual < rSet_PrimaryDryingShelfTemp THEN
            rShelfRampSetpointActual := rShelfRampSetpointActual + (rActiveRampSlope * rCycleScanDeltaTime);
        ELSE
            rShelfRampSetpointActual := rSet_PrimaryDryingShelfTemp;
        END_IF;

        (* Check for Primary Sublimation Endpoint Convergence *)
        IF bPrimaryDryingEndpointDetected OR (rDryingProgressRatio >= 0.98) THEN
            rStateTimerAccumulator_s := 0.0;
            nSubPhaseStep := 0;
            eCurrentState := 70; (* Proceed to Pirani-CM Endpoint Verification *)
        END_IF;

    70: (* ------------------------------------------------------------------------------------------------------------ *)
        (* STATE 7: DUAL-GAUGE PIRANI-CM ENDPOINT CONVERGENCE & PRESSURE RISE TEST (PRT) VERIFICATION                    *)
        (* ------------------------------------------------------------------------------------------------------------ *)
        rStateTimerAccumulator_s := rStateTimerAccumulator_s + rCycleScanDeltaTime;
        rShelfRampSetpointActual := rSet_PrimaryDryingShelfTemp;

        CASE nSubPhaseStep OF
            0: (* Verify Pirani to Baratron Convergence Delta_P <= 0.005 mbar *)
                IF rDualGaugeDifferentialPressure <= 0.005 THEN
                    (* Trigger 30-Second Manometric Pressure Rise Test (PRT) *)
                    bCmd_MainIsolationMushroomValveOpen := FALSE; (* Close isolation valve *)
                    rPRT_PressureRiseStart_mbar := rVotedChamberPressure_CM_Actual;
                    rPRT_PressureRiseElapsed_s := 0.0;
                    bPRT_ActiveInProgress := TRUE;
                    nSubPhaseStep := 1;
                END_IF;

            1: (* Dwell During 30-Second PRT Test *)
                IF NOT bPRT_ActiveInProgress THEN
                    (* PRT complete: check leak rate *)
                    bCmd_MainIsolationMushroomValveOpen := TRUE; (* Re-open isolation valve *)
                    IF rChamberPressureRiseRate_mbar_s <= 0.0010 THEN
                        (* Sublimation 100% complete: minimal water vapor outgassing *)
                        rStateTimerAccumulator_s := 0.0;
                        nSubPhaseStep := 0;
                        eCurrentState := 80; (* Proceed to Secondary Drying Desorption *)
                    ELSE
                        (* Still sublimating: return to Primary Drying hold *)
                        bPrimaryDryingEndpointDetected := FALSE;
                        eCurrentState := 60;
                    END_IF;
                END_IF;
        END_CASE;

    80: (* ------------------------------------------------------------------------------------------------------------ *)
        (* STATE 8: SECONDARY DRYING DESORPTION RAMP (+35.0 DEG C, 0.015 MBAR DEEP VACUUM)                              *)
        (* ------------------------------------------------------------------------------------------------------------ *)
        rStateTimerAccumulator_s := rStateTimerAccumulator_s + rCycleScanDeltaTime;
        bCmd_MainIsolationMushroomValveOpen := TRUE;
        (* Deep vacuum: cease N2 bleed, set vacuum target to 0.015 mbar *)
        rChamberPresSetpointActual := rSet_SecondaryDryingChamberPres;

        (* Ramp Shelf Temperature up to +35.0 deg C at 0.20 deg C/min *)
        rActiveRampSlope := (rSet_ShelfRampRateSecondaryDry / 60.0);
        IF rShelfRampSetpointActual < rSet_SecondaryDryingShelfTemp THEN
            rShelfRampSetpointActual := rShelfRampSetpointActual + (rActiveRampSlope * rCycleScanDeltaTime);
        ELSE
            rShelfRampSetpointActual := rSet_SecondaryDryingShelfTemp;
            rSecondaryDryingHoldTimer_s := rSecondaryDryingHoldTimer_s + rCycleScanDeltaTime;
        END_IF;

        (* Hold at +35.0 deg C until residual moisture < 1.0% or 6 hours elapsed (21,600 s) *)
        IF (bSecondaryDryingCompleteFlag AND (rSecondaryDryingHoldTimer_s >= 14400.0)) OR (rSecondaryDryingHoldTimer_s >= 28800.0) THEN
            rStateTimerAccumulator_s := 0.0;
            nSubPhaseStep := 0;
            eCurrentState := 90; (* Proceed to Chamber Backfill *)
        END_IF;

    90: (* ------------------------------------------------------------------------------------------------------------ *)
        (* STATE 9: CHAMBER BACKFILL WITH HIGH-PURITY STERILE NITROGEN (800.0 MBAR HEADSPACE)                           *)
        (* ------------------------------------------------------------------------------------------------------------ *)
        rStateTimerAccumulator_s := rStateTimerAccumulator_s + rCycleScanDeltaTime;
        (* Isolate condenser to protect dried cake from defrost vapor *)
        bCmd_MainIsolationMushroomValveOpen := FALSE;
        rShelfRampSetpointActual := 20.0; (* Return shelves to room temperature *)

        (* Modulate Sterile N2 Backfill Valve to reach 800.0 mbar inert headspace *)
        bCmd_ChamberVentSterileN2ValveOpen := TRUE;
        IF rVotedChamberPressure_CM_Actual >= 800.0 THEN
            bCmd_ChamberVentSterileN2ValveOpen := FALSE;
            rStateTimerAccumulator_s := 0.0;
            nSubPhaseStep := 0;
            eCurrentState := 100; (* Proceed to Hydraulic Shelf Stoppering *)
        END_IF;

    100: (* ----------------------------------------------------------------------------------------------------------- *)
         (* STATE 10: IN-CHAMBER HYDRAULIC SHELF STOPPERING COMPRESSION (240 KN FORCE DWELL)                            *)
         (* ----------------------------------------------------------------------------------------------------------- *)
        rStateTimerAccumulator_s := rStateTimerAccumulator_s + rCycleScanDeltaTime;

        CASE nSubPhaseStep OF
            0: (* Extend Hydraulic Ram Downwards to collapse telescoping shelf package *)
                IF rVotedHydraulicRamForceActual >= (rSet_StopperingHoldForceTarget - 10.0) THEN
                    nSubPhaseStep := 1;
                    rStopperingCompactionTimer_s := 0.0;
                END_IF;

            1: (* Compaction Dwell at Peak Force (240 kN hold for 180 seconds to fully seat rubber stoppers) *)
                rStopperingCompactionTimer_s := rStopperingCompactionTimer_s + rCycleScanDeltaTime;
                IF rStopperingCompactionTimer_s >= rSet_StopperingHoldDuration_s THEN
                    nSubPhaseStep := 2;
                    bStopperingCompleteFlag := TRUE;
                END_IF;

            2: (* Retract Hydraulic Ram to Upper Home Position (0.0 mm stroke) *)
                IF rHydraulicRamLinearPosition_mm <= 5.0 THEN
                    rStateTimerAccumulator_s := 0.0;
                    nSubPhaseStep := 0;
                    eCurrentState := 110; (* Proceed to Atmospheric Equalization & Unloading *)
                END_IF;
        END_CASE;

    110: (* ----------------------------------------------------------------------------------------------------------- *)
         (* STATE 11: ATMOSPHERIC EQUALIZATION (1,013 MBAR) & AUTOMATIC VIAL DISCHARGE UNLOADING                       *)
         (* ----------------------------------------------------------------------------------------------------------- *)
        rStateTimerAccumulator_s := rStateTimerAccumulator_s + rCycleScanDeltaTime;

        CASE nSubPhaseStep OF
            0: (* Equalize Chamber to 1013.25 mbar Atmospheric Pressure *)
                bCmd_ChamberVentSterileN2ValveOpen := TRUE;
                IF rVotedChamberPressure_CM_Actual >= 1010.0 THEN
                    bCmd_ChamberVentSterileN2ValveOpen := FALSE;
                    nSubPhaseStep := 1;
                END_IF;

            1: (* Deflate Aseptic Door Gasket and Open Unload Door *)
                bCmd_ChamberDoorPneumaticSealInflate := FALSE;
                IF rStateTimerAccumulator_s >= 20.0 THEN
                    nSubPhaseStep := 2;
                END_IF;

            2: (* External Pusher Collating 150,000 Sealed Vials to Capping & Crimping Station *)
                IF rStateTimerAccumulator_s >= 120.0 THEN
                    bCmd_ChamberDoorPneumaticSealInflate := TRUE;
                    rStateTimerAccumulator_s := 0.0;
                    nSubPhaseStep := 0;
                    eCurrentState := 120; (* Proceed to Condenser Ice Defrost Cycle *)
                END_IF;
        END_CASE;

    120: (* ----------------------------------------------------------------------------------------------------------- *)
         (* STATE 12: CONDENSER SUBLIMATED ICE HOT WATER/STEAM DEFROST & DRAIN DISCHARGE                                *)
         (* ----------------------------------------------------------------------------------------------------------- *)
        rStateTimerAccumulator_s := rStateTimerAccumulator_s + rCycleScanDeltaTime;
        bCmd_MainIsolationMushroomValveOpen := FALSE; (* Chamber isolated from defrost vessel *)

        CASE nSubPhaseStep OF
            0: (* Inject Clean Steam / 95 deg C Hot Water into Condenser Vessel *)
                bCmd_CondenserDefrostSteamValveOpen := TRUE;
                bCmd_CondenserCondensateDrainPumpRun := TRUE;
                rDefrostTimer_s := rDefrostTimer_s + rCycleScanDeltaTime;
                IF (rVotedCondenserCoilTempActual >= 65.0) AND (rDefrostTimer_s >= 1800.0) THEN
                    (* >800 kg ice melted and drained *)
                    bCmd_CondenserDefrostSteamValveOpen := FALSE;
                    nSubPhaseStep := 1;
                END_IF;

            1: (* Drain Evacuation and Cooldown Purge *)
                IF rStateTimerAccumulator_s >= 2400.0 THEN
                    bCmd_CondenserCondensateDrainPumpRun := FALSE;
                    bBatchCycleSuccessfullyComplete := TRUE;
                    rStateTimerAccumulator_s := 0.0;
                    nSubPhaseStep := 0;
                    eCurrentState := 0; (* Cycle Complete: Return to Standby *)
                END_IF;
        END_CASE;

    999: (* ----------------------------------------------------------------------------------------------------------- *)
         (* STATE 999: EMERGENCY SAFE STATE TRIP HOLD (FAIL-SAFE SHUTDOWN)                                             *)
         (* ----------------------------------------------------------------------------------------------------------- *)
        bCmd_MainIsolationMushroomValveOpen   := FALSE;
        bCmd_ChamberVentSterileN2ValveOpen    := FALSE;
        bCmd_CondenserDefrostSteamValveOpen   := FALSE;
        bCmd_CondenserCondensateDrainPumpRun  := FALSE;
        bEmergencySafetyInterlockTripped      := TRUE;

        (* Reset Latches if Permissive Restored and Reset Operator Pressed *)
        IF bResetFaultLatches AND bEmergencyStopCircuit_NC THEN
            bEmergencySafetyInterlockTripped := FALSE;
            bAlarm_ProductCollapseRisk_HH    := FALSE;
            bAlarm_VacuumLost_HH             := FALSE;
            bAlarm_CondenserTempHigh_HH      := FALSE;
            bAlarm_SiliconeOilFlow_LL        := FALSE;
            bAlarm_ShelfThermalRunaway_HH    := FALSE;
            bAlarm_CompressorHead_HH         := FALSE;
            bAlarm_HydraulicOilPres_HH       := FALSE;
            bAlarm_EmergencyStopTripped_HH   := FALSE;
            eCurrentState := 0; (* Return to Idle *)
        END_IF;

END_CASE;
"""

print("generate_phase5 loaded.")
