# brewery_builder/part7_phase4_fsm.py

def get_part7():
    return """(* ============================================================================================== *)
(* PHASE 4: 14-STAGE DETERMINISTIC BREWHOUSE PRODUCTION FINITE STATE MACHINE (FSM)               *)
(* ============================================================================================== *)

(* ---------------------------------------------------------------------------------------------- *)
(* STEP 4.1: STATE TRANSITION TIMING & SUBSTEP CLOCK ACCUMULATORS                                 *)
(* ---------------------------------------------------------------------------------------------- *)
IF eState <> ePrevState THEN
    tStateTimer := 0.0;
    tSubStateTimer := 0.0;
    iSubStep := 0;
    ePrevState := eState;
ELSE
    tStateTimer := tStateTimer + fCycleDeltaTimeSec;
    tSubStateTimer := tSubStateTimer + fCycleDeltaTimeSec;
END_IF;

fMasterBatchTimeSeconds := fMasterBatchTimeSeconds + fCycleDeltaTimeSec;
fTotalBatchElapsedTimeMin := fMasterBatchTimeSeconds / 60.0;
fStateElapsedTimeSec := tStateTimer;
iCurrentState := eState;
iCurrentSubStep := iSubStep;

(* ---------------------------------------------------------------------------------------------- *)
(* STEP 4.2: 14-STAGE PRODUCTION EXECUTION STATE MACHINE                                         *)
(* ---------------------------------------------------------------------------------------------- *)
CASE eState OF

    (* ------------------------------------------------------------------------------------------ *)
    (* STATE 0: BREWHOUSE IDLE & VESSEL INTEGRITY STANDBY                                         *)
    (* ------------------------------------------------------------------------------------------ *)
    0:
        (* De-energize all continuous actuators and close isolation manifolds *)
        bRunoffPumpRun := FALSE;
        bRecircPumpRun := FALSE;
        bCalandriaCircPumpRun := FALSE;
        bSpentGrainDischargeDoorOpen := FALSE;
        bHopDoserValve1 := FALSE;
        bHopDoserValve2 := FALSE;
        bCIPSupplyValveOpen := FALSE;
        bVaporCondenserPumpRun := FALSE;

        fRunoffValveCommand := 0.0;
        fRecircValveCommand := 0.0;
        fCalandriaSteamValveCommand := 0.0;
        fSpargeValveCommand := 0.0;
        fWhirlpoolPumpCommand := 0.0;
        fRakeHeightCommand := 350.0; (* Park Rakes High *)
        fRakeSpeedCommand := 0.0;

        (* Reset Batch Yield Accumulators *)
        fFoundationWaterAccumVolume := 0.0;
        fMashTransferAccumVolume := 0.0;
        fRunoffAccumVolume := 0.0;
        fSpargeWaterAccumVolume := 0.0;
        fBoilTimerSeconds := 0.0;
        fWhirlpoolRestTimerSeconds := 0.0;
        fCIPStepTimerSeconds := 0.0;
        fCumulativeEvaporationPercent := 0.0;
        bDeepCutRequired := FALSE;
        iDeepCutCycleCount := 0;
        bHopAddition1Done := FALSE;
        bHopAddition2Done := FALSE;

        bActive := FALSE;

        (* Production Start Permissive Interlocks Verification *)
        IF bExecute AND bAutoMode AND NOT bError AND NOT bAlarmHighHigh AND bEmergencyStop THEN
            bActive := TRUE;
            eState := 1; (* Transition to Foundation Water Underletting *)
        END_IF;

    (* ------------------------------------------------------------------------------------------ *)
    (* STATE 1: PREFILL FOUNDATION WATER UNDERLETTING                                             *)
    (* Displaces air trapped beneath slotted false bottom screens with 78 deg C liquor             *)
    (* ------------------------------------------------------------------------------------------ *)
    1:
        bActive := TRUE;
        CASE iSubStep OF
            0: (* Initialize Underlet Foundation Flow *)
                fRakeHeightCommand := 250.0;
                fRakeSpeedCommand := 0.0;
                fSpargeValveCommand := 65.0; (* Open Hot Liquor Underlet Manifold *)
                bRunoffPumpRun := FALSE;
                bRecircPumpRun := FALSE;
                IF tSubStateTimer >= 5.0 THEN
                    iSubStep := 1;
                    tSubStateTimer := 0.0;
                END_IF;

            1: (* Accumulate Foundation Water Underletting Volume (Target 25 hL) *)
                fSpargeValveCommand := 80.0;
                (* Integrate Underlet Volumetric Inflow *)
                fFoundationWaterAccumVolume := fFoundationWaterAccumVolume +
                                               (fSpargeWaterFlow * fCycleDeltaTimeSec / 3600.0);
                (* Fallback volumetric accumulation if flowmeter disabled *)
                IF fSpargeWaterFlow < 10.0 THEN
                    fFoundationWaterAccumVolume := fFoundationWaterAccumVolume +
                                                   (180.0 * fCycleDeltaTimeSec / 3600.0);
                END_IF;

                (* Verify water level covers false bottom plates by 15-20 mm (Lauter head > 3.0 mbar) *)
                IF (fFoundationWaterAccumVolume >= 25.0) OR (fVotedGrainBedDP >= 3.5) THEN
                    fSpargeValveCommand := 0.0;
                    iSubStep := 2;
                    tSubStateTimer := 0.0;
                END_IF;

            2: (* Hydrostatic Equilibrium Soak & Air Bleed Venting (20 s) *)
                fSpargeValveCommand := 0.0;
                IF tSubStateTimer >= 20.0 THEN
                    eState := 2; (* Transition to Mash Transfer Inflow *)
                END_IF;
        END_CASE;

    (* ------------------------------------------------------------------------------------------ *)
    (* STATE 2: MASH TRANSFER INFLOW & BED LEVELING                                               *)
    (* Gentle bottom-side transfer of mash from Mash Tun with slow rake leveling                  *)
    (* ------------------------------------------------------------------------------------------ *)
    2:
        CASE iSubStep OF
            0: (* Mash Inflow Initiation & Rake Leveling Engagement *)
                fRakeHeightCommand := 180.0; (* Position knives at mid-bed height *)
                fRakeSpeedCommand := 0.8;    (* Slow leveling speed [RPM] *)
                fRunoffValveCommand := 0.0;  (* Ensure runoff locked shut *)
                bRunoffPumpRun := FALSE;
                IF tSubStateTimer >= 8.0 THEN
                    iSubStep := 1;
                    tSubStateTimer := 0.0;
                END_IF;

            1: (* Main Mash Transfer Inflow (Target 290 hL mash) *)
                fRakeHeightCommand := 180.0;
                fRakeSpeedCommand := 0.8;
                (* Integrate Mash Inflow Volume *)
                fMashTransferAccumVolume := fMashTransferAccumVolume + (285.0 * fCycleDeltaTimeSec / 3600.0);

                (* Progressive Rake Elevation as Mash Level Rises to Prevent Excessive Knife Drag *)
                IF fMashTransferAccumVolume > 150.0 THEN
                    fRakeHeightCommand := 220.0;
                END_IF;

                (* Transfer Completion Check *)
                IF (fMashTransferAccumVolume >= 290.0) OR (tSubStateTimer >= 1200.0) THEN
                    iSubStep := 2;
                    tSubStateTimer := 0.0;
                END_IF;

            2: (* Mash Leveling Smoothing & Rake Park Elevation *)
                fRakeHeightCommand := 280.0;
                fRakeSpeedCommand := 0.5;
                IF tSubStateTimer >= 30.0 THEN
                    fRakeSpeedCommand := 0.0;
                    eState := 3; (* Transition to Grain Bed Settling Rest *)
                END_IF;
        END_CASE;

    (* ------------------------------------------------------------------------------------------ *)
    (* STATE 3: GRAIN BED REST & NATURAL FILTER MATRIX SETTLING                                   *)
    (* Quiescent rest period allows malt husks to settle and form the primary filter cake         *)
    (* ------------------------------------------------------------------------------------------ *)
    3:
        fRakeHeightCommand := 300.0; (* Park Rakes completely above grain bed *)
        fRakeSpeedCommand := 0.0;
        bRunoffPumpRun := FALSE;
        bRecircPumpRun := FALSE;
        fRunoffValveCommand := 0.0;
        fRecircValveCommand := 0.0;

        (* 10-Minute Quiescent Settling Rest (600 s) *)
        IF tStateTimer >= 600.0 THEN
            eState := 4; (* Transition to Vorlauf Recirculation *)
        END_IF;

    (* ------------------------------------------------------------------------------------------ *)
    (* STATE 4: VORLAUF RECIRCULATION & TURBIDITY CLARIFICATION                                  *)
    (* Recirculates cloudy initial wort back over grain bed until optical turbidity drops < 25 EBC*)
    (* ------------------------------------------------------------------------------------------ *)
    4:
        CASE iSubStep OF
            0: (* Align Vorlauf Recirculation Valve Manifold *)
                fRecircValveCommand := 100.0; (* 100% Recirculation Diverter Open *)
                fRunoffValveCommand := 0.0;   (* Wort Kettle Valve Closed *)
                fRakeHeightCommand := 220.0;  (* Skim top surface of grain bed *)
                fRakeSpeedCommand := 0.4;     (* Gentle rotational speed *)
                bRecircPumpRun := TRUE;
                bRunoffPumpRun := FALSE;
                IF tSubStateTimer >= 10.0 THEN
                    iSubStep := 1;
                    tSubStateTimer := 0.0;
                END_IF;

            1: (* Runoff Pump Low-Speed Soft-Start Recirculation *)
                bRunoffPumpRun := TRUE;
                fRecircValveCommand := 100.0;
                fRunoffValveCommand := 0.0;
                (* Apply MPC bounded actuation on Vorlauf flow *)
                fRakeHeightCommand := vecU_active[1];
                fRakeSpeedCommand := vecU_active[2];

                (* Monitor Vorlauf Clarification Optical Turbidity *)
                IF (fVotedWortTurbidity <= fTargetWortTurbidity) AND (tSubStateTimer >= 60.0) THEN
                    iSubStep := 2;
                    tSubStateTimer := 0.0;
                ELSIF tSubStateTimer >= 900.0 THEN
                    (* Timeout override: Vorlauf maximum allowed recirculation duration reached *)
                    iSubStep := 2;
                    tSubStateTimer := 0.0;
                END_IF;

            2: (* Clarity Verification Dwell Period (30 s Continuous Stability) *)
                IF fVotedWortTurbidity <= (fTargetWortTurbidity + 2.0) THEN
                    IF tSubStateTimer >= 30.0 THEN
                        eState := 5; (* Transition to First Wort Runoff Optimization *)
                    END_IF;
                ELSE
                    (* Turbidity spiked: return to active Vorlauf recirculation *)
                    iSubStep := 1;
                    tSubStateTimer := 0.0;
                END_IF;
        END_CASE;

    (* ------------------------------------------------------------------------------------------ *)
    (* STATE 5: FIRST WORT RUNOFF & MPC DARCY HYDRAULIC OPTIMIZATION                             *)
    (* High-gravity first wort runoff to kettle, optimized for maximum flow without bed choking   *)
    (* ------------------------------------------------------------------------------------------ *)
    5:
        bRunoffPumpRun := TRUE;
        bRecircPumpRun := FALSE;
        fRecircValveCommand := 0.0; (* Shut Vorlauf Recirculation *)

        (* Execute Receding-Horizon MPC Actuator Outputs *)
        fRakeHeightCommand := vecU_active[1];
        fRakeSpeedCommand := vecU_active[2];
        fRunoffValveCommand := vecU_active[3];

        (* Integrate Transferred First Wort Volume *)
        fRunoffAccumVolume := fRunoffAccumVolume + (fVotedRunoffFlow * fCycleDeltaTimeSec / 3600.0);

        (* Calandria Pre-Heating: Pre-warm Calandria Jacket once Kettle Level > 25% *)
        IF fVotedKettleLevel > 25.0 THEN
            fCalandriaSteamValveCommand := 25.0; (* Low steam idle preheat *)
        ELSE
            fCalandriaSteamValveCommand := 0.0;
        END_IF;

        (* Check for Hydraulic Bed Compaction Choking Condition *)
        IF (fVotedGrainBedDP > fMaxAllowedGrainBedDP) OR bBedChokeDetected THEN
            bDeepCutRequired := TRUE;
            eState := 7; (* Divert to Emergency Rake Deep Cutting Sequence *)
        END_IF;

        (* Transition to Sparging when First Wort Runoff Nears Top of Grain Bed (220 hL) *)
        IF (fRunoffAccumVolume >= 220.0) OR (fLauterTunLevel <= 120.0) THEN
            eState := 6; (* Transition to Sparging Hot Water Distribution *)
        END_IF;

    (* ------------------------------------------------------------------------------------------ *)
    (* STATE 6: CONTINUOUS SPARGING HOT LIQUOR DISTRIBUTION                                      *)
    (* Continuous 78 deg C liquor distribution matching runoff flow; extracts remaining sugars    *)
    (* ------------------------------------------------------------------------------------------ *)
    6:
        bRunoffPumpRun := TRUE;
        bRecircPumpRun := FALSE;
        fRecircValveCommand := 0.0;

        (* Run MPC Actuator Outputs *)
        fRakeHeightCommand := vecU_active[1];
        fRakeSpeedCommand := vecU_active[2];
        fRunoffValveCommand := vecU_active[3];

        (* Regulate Sparging Hot Liquor Inflow Valve to Match Runoff Flow Rate *)
        fSpargeValveCommand := (fVotedRunoffFlow / 300.0) * 85.0;
        IF fSpargeValveCommand > 95.0 THEN fSpargeValveCommand := 95.0; END_IF;
        IF fSpargeValveCommand < 15.0 THEN fSpargeValveCommand := 15.0; END_IF;

        (* Accumulate Transferred Volumes *)
        fRunoffAccumVolume := fRunoffAccumVolume + (fVotedRunoffFlow * fCycleDeltaTimeSec / 3600.0);
        fSpargeWaterAccumVolume := fSpargeWaterAccumVolume + (fSpargeWaterFlow * fCycleDeltaTimeSec / 3600.0);

        (* Calandria Pre-Boil Temperature Ramp *)
        IF fVotedKettleLevel > 50.0 THEN
            fCalandriaSteamValveCommand := 45.0;
            bCalandriaCircPumpRun := TRUE;
        END_IF;

        (* Bed Compaction Protection Interlock *)
        IF (fVotedGrainBedDP > fMaxAllowedGrainBedDP) OR bBedChokeDetected THEN
            bDeepCutRequired := TRUE;
            eState := 7; (* Divert to Rake Deep Cutting *)
        END_IF;

        (* Sweet Water Extract Gravity Cutoff Check (< 1.8 deg Plato) *)
        IF (fWortGravityPlato <= fSweetWaterCutoffPlato) AND (fRunoffAccumVolume >= (fBatchVolumeTarget * 0.90)) THEN
            eState := 8; (* Transition to Sweet Water Cutoff *)
        ELSIF fRunoffAccumVolume >= fBatchVolumeTarget THEN
            eState := 8; (* Target Kettle Full Batch Volume Reached *)
        END_IF;

    (* ------------------------------------------------------------------------------------------ *)
    (* STATE 7: RAKE DEEP CUTTING RECOVERY SEQUENCE                                              *)
    (* Automatic deep bed slicing to restore collapsed Darcy permeability and relieve DP         *)
    (* ------------------------------------------------------------------------------------------ *)
    7:
        CASE iSubStep OF
            0: (* Decompress Bed: Throttle Runoff Flow *)
                fRunoffValveCommand := 20.0; (* Throttle suction under false bottom *)
                fSpargeValveCommand := 30.0;
                fRakeSpeedCommand := 1.5;
                fRakeHeightCommand := 45.0;  (* Lower knives into compacted bottom zone *)
                IF tSubStateTimer >= 10.0 THEN
                    iSubStep := 1;
                    tSubStateTimer := 0.0;
                END_IF;

            1: (* Deep Knife Slicing at Maximum Safe Cutting Depth (22 mm above false bottom) *)
                fRakeHeightCommand := 22.0;  (* Deepest cutting elevation *)
                fRakeSpeedCommand := 3.8;    (* High cutting RPM *)
                fRunoffValveCommand := 25.0;

                (* Monitor Differential Pressure Relief *)
                IF (fVotedGrainBedDP <= 18.0) AND (tSubStateTimer >= 60.0) THEN
                    iSubStep := 2;
                    tSubStateTimer := 0.0;
                ELSIF tSubStateTimer >= 180.0 THEN
                    (* Max deep cut duration timeout *)
                    iSubStep := 2;
                    tSubStateTimer := 0.0;
                END_IF;

            2: (* Elevate Rakes Back to Nominal Cutting Depth & Resume Production Flow *)
                fRakeHeightCommand := 75.0;
                fRakeSpeedCommand := 1.8;
                fRunoffValveCommand := 65.0;
                IF tSubStateTimer >= 20.0 THEN
                    bDeepCutRequired := FALSE;
                    iDeepCutCycleCount := iDeepCutCycleCount + 1;
                    eState := 6; (* Return to Sparging Hot Water Distribution *)
                END_IF;
        END_CASE;

    (* ------------------------------------------------------------------------------------------ *)
    (* STATE 8: SWEET WATER RUNOFF CUTOFF & LAUTER TUN DRAIN                                      *)
    (* Terminates wort collection to Kettle; diverts weak runnings to drain/weak wort recovery    *)
    (* ------------------------------------------------------------------------------------------ *)
    8:
        CASE iSubStep OF
            0: (* Close Kettle Inflow & Terminate Sparge *)
                fRunoffValveCommand := 0.0;  (* Close Kettle Isolation Valve *)
                fSpargeValveCommand := 0.0;  (* Shut Sparge Liquor *)
                fRakeHeightCommand := 150.0;
                fRakeSpeedCommand := 0.5;
                IF tSubStateTimer >= 10.0 THEN
                    iSubStep := 1;
                    tSubStateTimer := 0.0;
                END_IF;

            1: (* Drain Residual Bed Liquor Underlet to Weak Wort Sump *)
                fRunoffValveCommand := 15.0;
                bRunoffPumpRun := TRUE;
                IF (fLauterTunLevel <= 15.0) OR (tSubStateTimer >= 240.0) THEN
                    bRunoffPumpRun := FALSE;
                    fRunoffValveCommand := 0.0;
                    fRakeSpeedCommand := 0.0;
                    iSubStep := 2;
                    tSubStateTimer := 0.0;
                END_IF;

            2: (* Confirm Lauter Empty & Safe for Grain Evacuation *)
                IF tSubStateTimer >= 15.0 THEN
                    eState := 9; (* Transition to Spent Grain Evacuation *)
                END_IF;
        END_CASE;

    (* ------------------------------------------------------------------------------------------ *)
    (* STATE 9: SPENT GRAIN AUTOMATED DISCHARGE EVACUATION                                       *)
    (* Opens bottom discharge hatch and deploys rake plows to evacuate spent malt to silo         *)
    (* ------------------------------------------------------------------------------------------ *)
    9:
        CASE iSubStep OF
            0: (* Verify Vessel Depressurized & Open Grain Discharge Door *)
                fRakeHeightCommand := 80.0;
                fRakeSpeedCommand := 0.0;
                bSpentGrainDoorOpenPermissive := TRUE;
                bSpentGrainDischargeDoorOpen := TRUE;
                IF tSubStateTimer >= 15.0 THEN
                    iSubStep := 1;
                    tSubStateTimer := 0.0;
                END_IF;

            1: (* Deploy Discharge Plows & Ramp Rake Rotation to 4.2 RPM *)
                fRakeHeightCommand := 18.0; (* Plow elevation scraping false bottom *)
                fRakeSpeedCommand := 4.2;   (* Full grain discharge rotation *)
                bSpentGrainDischargeDoorOpen := TRUE;

                (* Evacuation Timer (480 s / 8 min nominal spent grain push) *)
                IF (fRakeMotorTorque < 250.0) AND (tSubStateTimer >= 360.0) THEN
                    iSubStep := 2;
                    tSubStateTimer := 0.0;
                ELSIF tSubStateTimer >= 600.0 THEN
                    iSubStep := 2;
                    tSubStateTimer := 0.0;
                END_IF;

            2: (* Complete Evacuation, Elevate Rakes & Close Grain Door *)
                fRakeSpeedCommand := 0.0;
                fRakeHeightCommand := 350.0; (* Park Rakes High *)
                bSpentGrainDischargeDoorOpen := FALSE;
                IF tSubStateTimer >= 25.0 THEN
                    bSpentGrainDoorOpenPermissive := FALSE;
                    eState := 10; (* Transition to Kettle Heating Calandria *)
                END_IF;
        END_CASE;

    (* ------------------------------------------------------------------------------------------ *)
    (* STATE 10: WORT KETTLE CALANDRIA FORCED-CIRCULATION HEATING                                 *)
    (* Ramps kettle thermal bulk to 100 deg C; initiates DMS cleavage and protein break formation *)
    (* ------------------------------------------------------------------------------------------ *)
    10:
        bCalandriaCircPumpRun := TRUE;    (* Forced Circulation Pump Active *)
        bVaporCondenserPumpRun := TRUE;   (* Vapor Condenser Active *)

        (* Execute MPC Steam Actuator Output *)
        fCalandriaSteamValveCommand := vecU_active[4];
        IF fCalandriaSteamValveCommand < 40.0 THEN
            fCalandriaSteamValveCommand := 75.0; (* Force High Heat Ramp *)
        END_IF;

        (* First Hop Charge Addition (Bittering Hops at 95 deg C) *)
        IF (fVotedKettleTemp >= 95.0) AND NOT bHopAddition1Done THEN
            bHopDoserValve1 := TRUE;
            IF tSubStateTimer >= 15.0 THEN
                bHopDoserValve1 := FALSE;
                bHopAddition1Done := TRUE;
            END_IF;
        END_IF;

        (* Transition to Vigorous Boil when Kettle Temp Reaches 99.8 deg C *)
        IF fVotedKettleTemp >= 99.8 THEN
            eState := 11; (* Transition to Vigorous Boil Evaporation *)
        END_IF;

    (* ------------------------------------------------------------------------------------------ *)
    (* STATE 11: VIGOROUS BOIL, CALANDRIA EVAPORATION & VOLATILE DMS STRIPPING                    *)
    (* Continuous 6.5 %/h boil-off, protein coagulation, isomerization & DMS stripping           *)
    (* ------------------------------------------------------------------------------------------ *)
    11:
        bCalandriaCircPumpRun := TRUE;
        bVaporCondenserPumpRun := TRUE;

        (* Active MPC Regulation of Calandria Steam to Track Evaporation Rate *)
        fCalandriaSteamValveCommand := vecU_active[4];

        (* Boiling Duration Accumulation *)
        fBoilTimerSeconds := fBoilTimerSeconds + fCycleDeltaTimeSec;

        (* Cumulative Evaporation Integration *)
        fCumulativeEvaporationPercent := fCumulativeEvaporationPercent +
                                         (vecX_hat[5] * fCycleDeltaTimeSec / 3600.0);

        (* Second Hop Charge Addition (Aroma Hops 10 minutes prior to flameout) *)
        IF (fBoilTimerSeconds >= ((fTargetBoilDurationMinutes - 10.0) * 60.0)) AND NOT bHopAddition2Done THEN
            bHopDoserValve2 := TRUE;
            IF tSubStateTimer >= 15.0 THEN
                bHopDoserValve2 := FALSE;
                bHopAddition2Done := TRUE;
            END_IF;
        END_IF;

        (* Boil Completion Criteria: Target Duration Elapsed & DMS Stripped Below 28 ppb *)
        IF (fBoilTimerSeconds >= (fTargetBoilDurationMinutes * 60.0)) AND
           (fEstimatedResidualDMS <= fTargetDMSConcentration) THEN
            (* Flameout: Cut Calandria Steam Supply *)
            fCalandriaSteamValveCommand := 0.0;
            bCalandriaCircPumpRun := FALSE;
            eState := 12; (* Transition to Whirlpool Tangential Inlet Rest *)
        END_IF;

    (* ------------------------------------------------------------------------------------------ *)
    (* STATE 12: WHIRLPOOL TANGENTIAL INLET TRANSFER & TRUB CONE REST                             *)
    (* Centripetal hydrodynamic trub cone formation via teacup effect followed by 20-min rest     *)
    (* ------------------------------------------------------------------------------------------ *)
    12:
        CASE iSubStep OF
            0: (* Tangential Whirlpool Transfer Pump Acceleration (4.2 m/s Nozzle Velocity) *)
                bVaporCondenserPumpRun := FALSE;
                fWhirlpoolPumpCommand := 85.0; (* Whirlpool Transfer Pump Running *)
                IF (fVotedKettleLevel <= 3.0) OR (tSubStateTimer >= 720.0) THEN
                    fWhirlpoolPumpCommand := 0.0; (* Transfer Complete *)
                    iSubStep := 1;
                    tSubStateTimer := 0.0;
                END_IF;

            1: (* Quiescent Trub Cone Settling Rest (1200 s / 20 min) *)
                fWhirlpoolPumpCommand := 0.0;
                fWhirlpoolRestTimerSeconds := fWhirlpoolRestTimerSeconds + fCycleDeltaTimeSec;

                IF fWhirlpoolRestTimerSeconds >= (fTargetWhirlpoolRestMinutes * 60.0) THEN
                    iSubStep := 2;
                    tSubStateTimer := 0.0;
                END_IF;

            2: (* Wort Knockout to Cellar Ready *)
                IF tSubStateTimer >= 10.0 THEN
                    eState := 13; (* Transition to CIP Caustic Sanitization *)
                END_IF;
        END_CASE;

    (* ------------------------------------------------------------------------------------------ *)
    (* STATE 13: AUTOMATED CIP CAUSTIC SANITIZATION LOOP                                         *)
    (* Multi-stage rotary spray ball wash across lauter tun, wort kettle, and calandria          *)
    (* ------------------------------------------------------------------------------------------ *)
    13:
        bCIPSupplyValveOpen := TRUE;
        fCIPStepTimerSeconds := fCIPStepTimerSeconds + fCycleDeltaTimeSec;

        CASE iSubStep OF
            0: (* Step 1: Warm Water Pre-Rinse (180 s) *)
                fRakeHeightCommand := 200.0;
                fRakeSpeedCommand := 1.0;
                IF fCIPStepTimerSeconds >= 180.0 THEN
                    iSubStep := 1;
                    fCIPStepTimerSeconds := 0.0;
                END_IF;

            1: (* Step 2: Hot Caustic Wash (1.8% NaOH at 80 deg C, 600 s) *)
                fRakeHeightCommand := 150.0;
                fRakeSpeedCommand := 1.5;
                bCalandriaCircPumpRun := TRUE;
                fCalandriaSteamValveCommand := 25.0; (* Maintain Caustic Temp *)
                IF fCIPStepTimerSeconds >= 600.0 THEN
                    iSubStep := 2;
                    fCIPStepTimerSeconds := 0.0;
                END_IF;

            2: (* Step 3: Intermediate Clear Water Rinse (240 s) *)
                fCalandriaSteamValveCommand := 0.0;
                bCalandriaCircPumpRun := FALSE;
                fRakeHeightCommand := 250.0;
                fRakeSpeedCommand := 0.8;
                IF fCIPStepTimerSeconds >= 240.0 THEN
                    iSubStep := 3;
                    fCIPStepTimerSeconds := 0.0;
                END_IF;

            3: (* Step 4: Sanitizer / Peracetic Acid (PAA) Disinfection (300 s) *)
                fRakeHeightCommand := 300.0;
                fRakeSpeedCommand := 0.5;
                IF fCIPStepTimerSeconds >= 300.0 THEN
                    iSubStep := 4;
                    fCIPStepTimerSeconds := 0.0;
                END_IF;

            4: (* CIP Complete: Drain & Park Vessels *)
                bCIPSupplyValveOpen := FALSE;
                fRakeHeightCommand := 350.0;
                fRakeSpeedCommand := 0.0;
                IF tSubStateTimer >= 30.0 THEN
                    eState := 0; (* Return to Brewhouse Standby Idle *)
                END_IF;
        END_CASE;

END_CASE;
"""
