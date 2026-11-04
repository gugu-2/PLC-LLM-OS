# -*- coding: utf-8 -*-
"""
Builder module for FB_Fertilizer_AmmoniumNitrate_Granulation_Scrubber
Part 5: Phase 4 - 12-Stage Operational Finite State Machine (FSM)
"""

def get_phase4_fsm():
    code = """(* ============================================================================================================== *)
(* PHASE 4: 12-STAGE OPERATIONAL PRODUCTION FINITE STATE MACHINE (FSM)                                            *)
(* ============================================================================================================== *)

rStateDwellTimer_s := rStateDwellTimer_s + c_rTs;

CASE iFSM_CurrentState OF

    0: (* ------------------------------------------------------------------------------------------------------ *)
       (* STATE 0: PLANT_STANDBY_INERT_PURGE                                                                     *)
       (* ------------------------------------------------------------------------------------------------------ *)
       bPlantInProduction := FALSE;
       rOut_SlurrySprayValve_pct := 0.0;
       rOut_AtomizingSteamValve_pct := 0.0;
       rOut_BurnerGasThrottle_pct := 0.0;
       rOut_CombustionAirDamper_pct := 20.0;
       rOut_DryerInducedDraftFan_pct := 15.0;
       rOut_CoolerChamber1AirFan_pct := 0.0;
       rOut_CoolerChilledAirFan_pct := 0.0;
       rOut_VenturiThroatDamper_pct := 25.0;
       rOut_ScrubberRecircPumpHz := 0.0;
       rOut_NitricAcidTrimValve_pct := 0.0;
       rOut_RecycleDragConveyorSpeed_pct := 0.0;
       rOut_OversizeCageMillSpeed_RPM := 0.0;
       bOut_EmergencyDelugeFloodActuate := FALSE;
       bOut_SlurryEmergencyDumpValve := FALSE;
       bOut_BurnerSafetyShutoffValve_Trip := FALSE;
       bOut_NitrogenPurgeFloodValve := FALSE;

       (* Purge chronometer execution *)
       rPurgeSequenceTimer_s := rPurgeSequenceTimer_s + c_rTs;

       (* Permissive validation for sequence advance *)
       IF bMasterAutoEnable AND bSafetyCircuitHealthy_NC AND bNitrogenPurgePermissive AND 
          bBoilerSteamHeaderReady AND bNaturalGasHeaderReady AND bDelugeWaterSupplyReady AND 
          (rPurgeSequenceTimer_s >= 45.0) THEN
           rPurgeSequenceTimer_s := 0.0;
           rStateDwellTimer_s := 0.0;
           iFSM_CurrentState := 1; (* Advance to SCRUBBER_CIRCULATION_PH_STABILIZE *)
       END_IF;

    1: (* ------------------------------------------------------------------------------------------------------ *)
       (* STATE 1: SCRUBBER_CIRCULATION_PH_STABILIZE                                                             *)
       (* ------------------------------------------------------------------------------------------------------ *)
       bPlantInProduction := FALSE;
       rOut_DryerInducedDraftFan_pct := 40.0;
       rOut_VenturiThroatDamper_pct := 40.0;
       rOut_ScrubberRecircPumpHz := 50.0;

       (* Sump liquor pH stabilization *)
       IF rVoted_Scrubber_pH > 4.20 THEN
           rOut_NitricAcidTrimValve_pct := 30.0;
       ELSIF rVoted_Scrubber_pH < 3.80 THEN
           rOut_NitricAcidTrimValve_pct := 0.0;
       ELSE
           rOut_NitricAcidTrimValve_pct := 15.0;
       END_IF;

       (* Advance when scrubber Delta P and pH reach steady baseline *)
       IF (rVoted_VenturiDeltaP_mbar >= 30.0) AND (rVoted_Scrubber_pH >= 3.80) AND 
          (rVoted_Scrubber_pH <= 4.40) AND (rStateDwellTimer_s >= 30.0) THEN
           rStateDwellTimer_s := 0.0;
           iFSM_CurrentState := 2; (* Advance to DRYER_BURNER_PREHEAT_RAMP *)
       END_IF;

       IF NOT bMasterAutoEnable OR NOT bSafetyCircuitHealthy_NC THEN
           iFSM_CurrentState := 0;
       END_IF;

    2: (* ------------------------------------------------------------------------------------------------------ *)
       (* STATE 2: DRYER_BURNER_PREHEAT_RAMP                                                                     *)
       (* ------------------------------------------------------------------------------------------------------ *)
       bPlantInProduction := FALSE;
       rPreheatRampTimer_s := rPreheatRampTimer_s + c_rTs;
       rOut_DryerInducedDraftFan_pct := 55.0;

       (* Controlled firing rate ramp: 15% to 45% over 180 seconds *)
       IF rPreheatRampTimer_s < 180.0 THEN
           rOut_BurnerGasThrottle_pct := 15.0 + ((rPreheatRampTimer_s / 180.0) * 30.0);
       ELSE
           rOut_BurnerGasThrottle_pct := 45.0;
       END_IF;

       (* Flame safeguard interlock *)
       IF (rVoted_BurnerFlameIntensity_pct < c_rTrip_BurnerFlameLoss_Trip) AND (rPreheatRampTimer_s > 15.0) THEN
           bAlarm_BurnerFlameLoss_Trip := TRUE;
           bOut_BurnerSafetyShutoffValve_Trip := TRUE;
           iFSM_CurrentState := 0; (* Trip to Standby *)
       END_IF;

       (* Advance when dryer flue gas inlet reaches preheat soak temperature (140 deg C) *)
       IF (rVoted_DryerInletTemp_degC >= 140.0) AND (rPreheatRampTimer_s >= 180.0) THEN
           rPreheatRampTimer_s := 0.0;
           rStateDwellTimer_s := 0.0;
           iFSM_CurrentState := 3; (* Advance to COOLER_FLUIDIZATION_AERATION_START *)
       END_IF;

       IF NOT bMasterAutoEnable OR NOT bSafetyCircuitHealthy_NC THEN
           iFSM_CurrentState := 0;
       END_IF;

    3: (* ------------------------------------------------------------------------------------------------------ *)
       (* STATE 3: COOLER_FLUIDIZATION_AERATION_START                                                            *)
       (* ------------------------------------------------------------------------------------------------------ *)
       bPlantInProduction := FALSE;
       rCoolerAerationTimer_s := rCoolerAerationTimer_s + c_rTs;

       (* Start fluidizing blowers *)
       rOut_CoolerChamber1AirFan_pct := 45.0;
       rOut_CoolerChilledAirFan_pct := 35.0;

       (* Confirm deck aeration differential pressure within proper fluidization window (15..35 mbar) *)
       IF (rVoted_CoolerPlenumPress_mbar >= 18.0) AND (rVoted_CoolerPlenumPress_mbar <= 35.0) AND 
          (rCoolerAerationTimer_s >= 25.0) THEN
           rCoolerAerationTimer_s := 0.0;
           rStateDwellTimer_s := 0.0;
           iFSM_CurrentState := 4; (* Advance to RECYCLE_SEED_LOOP_CIRCULATION *)
       END_IF;

       IF NOT bMasterAutoEnable OR NOT bSafetyCircuitHealthy_NC THEN
           iFSM_CurrentState := 0;
       END_IF;

    4: (* ------------------------------------------------------------------------------------------------------ *)
       (* STATE 4: RECYCLE_SEED_LOOP_CIRCULATION                                                                 *)
       (* ------------------------------------------------------------------------------------------------------ *)
       bPlantInProduction := FALSE;
       rSeedLoopTimer_s := rSeedLoopTimer_s + c_rTs;

       (* Start solid transport machinery *)
       rOut_RecycleDragConveyorSpeed_pct := 55.0;
       rOut_OversizeCageMillSpeed_RPM := 650.0;
       rOut_DryerInducedDraftFan_pct := 65.0;

       (* Check recycle seed mass flow establishment and drum bed temperature warmup *)
       IF (rVoted_RecycleMassFlow_tph >= 180.0) AND (rVoted_DrumBedTemp_degC >= 85.0) AND 
          (rSeedLoopTimer_s >= 60.0) THEN
           rSeedLoopTimer_s := 0.0;
           rStateDwellTimer_s := 0.0;
           iFSM_CurrentState := 5; (* Advance to SLURRY_NOZZLE_ATOMIZATION_PRIME *)
       END_IF;

       IF NOT bMasterAutoEnable OR NOT bSafetyCircuitHealthy_NC THEN
           iFSM_CurrentState := 0;
       END_IF;

    5: (* ------------------------------------------------------------------------------------------------------ *)
       (* STATE 5: SLURRY_NOZZLE_ATOMIZATION_PRIME                                                               *)
       (* ------------------------------------------------------------------------------------------------------ *)
       bPlantInProduction := FALSE;
       rNozzlePrimeTimer_s := rNozzlePrimeTimer_s + c_rTs;

       (* Pre-heat nozzles with superheated steam *)
       rOut_AtomizingSteamValve_pct := 65.0;

       (* Verify molten slurry header temperature and pressure ready *)
       IF (rVoted_SlurryFeedTemp_degC >= 170.0) AND (rVoted_SlurryFeedPress_bar >= 5.80) THEN
           (* Crack open slurry valve to prime granulation *)
           rOut_SlurrySprayValve_pct := 30.0;
       END_IF;

       (* Advance to continuous steady-state granulation when bed temperature >= 95 deg C *)
       IF (rVoted_DrumBedTemp_degC >= 95.0) AND (rVoted_ProductMassFlow_tph >= 45.0) AND 
          (rNozzlePrimeTimer_s >= 45.0) THEN
           rNozzlePrimeTimer_s := 0.0;
           rStateDwellTimer_s := 0.0;
           iFSM_CurrentState := 6; (* Advance to CONTINUOUS_STEADY_STATE_GRANULATION *)
       END_IF;

       IF NOT bMasterAutoEnable OR NOT bSafetyCircuitHealthy_NC THEN
           iFSM_CurrentState := 0;
       END_IF;

    6: (* ------------------------------------------------------------------------------------------------------ *)
       (* STATE 6: CONTINUOUS_STEADY_STATE_GRANULATION                                                           *)
       (* ------------------------------------------------------------------------------------------------------ *)
       bPlantInProduction := TRUE;

       (* MPC outputs are actively driving process actuators (handled in Phase 3) *)
       (* Check for operator grade change request *)
       IF nRecipeFertilizerGradeID <> 3350 THEN
           rStateDwellTimer_s := 0.0;
           iFSM_CurrentState := 7; (* Branch to PRODUCT_GRADE_SPEC_ADJUSTMENT *)
       END_IF;

       (* Check for nozzle clogging indicator (pressure rise with flow restriction) *)
       IF (rVoted_SlurryFeedPress_bar >= 7.60) AND (rOut_SlurrySprayValve_pct >= 70.0) THEN
           rStateDwellTimer_s := 0.0;
           iFSM_CurrentState := 8; (* Branch to NOZZLE_STEAM_CLEANOUT_RODDING *)
       END_IF;

       (* Normal shutdown command *)
       IF NOT bMasterAutoEnable THEN
           rStateDwellTimer_s := 0.0;
           iFSM_CurrentState := 9; (* Branch to CONTROLLED_EMPTYING_RAMP_DOWN *)
       END_IF;

    7: (* ------------------------------------------------------------------------------------------------------ *)
       (* STATE 7: PRODUCT_GRADE_SPEC_ADJUSTMENT                                                                 *)
       (* ------------------------------------------------------------------------------------------------------ *)
       bPlantInProduction := TRUE;

       (* Slew setpoints smoothly toward new fertilizer grade targets *)
       IF nRecipeFertilizerGradeID = 2700 THEN
           (* CAN 27% N formulation: slightly higher bed moisture, lower bed temp *)
           rSet_TargetBedTemperature_degC := 98.0;
           rSet_TargetGranuleMoisture_pct := 1.65;
           rSet_TargetRecycleRatio := 3.20;
       ELSIF nRecipeFertilizerGradeID = 201010 THEN
           (* NPK 20-10-10 complex grade *)
           rSet_TargetBedTemperature_degC := 94.0;
           rSet_TargetGranuleMoisture_pct := 1.80;
           rSet_TargetRecycleRatio := 3.50;
       ELSE
           (* Standard AN 33.5% N *)
           rSet_TargetBedTemperature_degC := 102.0;
           rSet_TargetGranuleMoisture_pct := 1.45;
           rSet_TargetRecycleRatio := 3.00;
       END_IF;

       (* Return to steady-state once transitioned for 60 seconds *)
       IF rStateDwellTimer_s >= 60.0 THEN
           rStateDwellTimer_s := 0.0;
           iFSM_CurrentState := 6; (* Return to CONTINUOUS_STEADY_STATE_GRANULATION *)
       END_IF;

    8: (* ------------------------------------------------------------------------------------------------------ *)
       (* STATE 8: NOZZLE_STEAM_CLEANOUT_RODDING                                                                 *)
       (* ------------------------------------------------------------------------------------------------------ *)
       bPlantInProduction := TRUE;
       rNozzleCleanoutTimer_s := rNozzleCleanoutTimer_s + c_rTs;

       (* Cut back slurry feed temporarily *)
       rOut_SlurrySprayValve_pct := 35.0;

       (* High-pressure steam burst to clear nozzle orifice encrustations *)
       rOut_AtomizingSteamValve_pct := 95.0;

       (* After 20 seconds of steam rodding, verify pressure normalizes *)
       IF rNozzleCleanoutTimer_s >= 20.0 THEN
           rNozzleCleanoutTimer_s := 0.0;
           rStateDwellTimer_s := 0.0;
           iFSM_CurrentState := 6; (* Return to CONTINUOUS_STEADY_STATE_GRANULATION *)
       END_IF;

    9: (* ------------------------------------------------------------------------------------------------------ *)
       (* STATE 9: CONTROLLED_EMPTYING_RAMP_DOWN                                                                 *)
       (* ------------------------------------------------------------------------------------------------------ *)
       bPlantInProduction := FALSE;
       rRampDownTimer_s := rRampDownTimer_s + c_rTs;

       (* Step 1: Ramp down and close slurry spray valve *)
       IF rRampDownTimer_s < 60.0 THEN
           rOut_SlurrySprayValve_pct := MAX(0.0, 50.0 - ((rRampDownTimer_s / 60.0) * 50.0));
           rOut_AtomizingSteamValve_pct := 40.0;
       ELSE
           rOut_SlurrySprayValve_pct := 0.0;
           rOut_AtomizingSteamValve_pct := 0.0;
       END_IF;

       (* Step 2: Keep solids moving to clear drum and dryer hold-up *)
       rOut_RecycleDragConveyorSpeed_pct := 65.0;
       rOut_OversizeCageMillSpeed_RPM := 500.0;
       rOut_BurnerGasThrottle_pct := 20.0; (* Low fire *)

       (* When plant empty (< 5 t/h product flow) and ramp timer >= 120s, complete shutdown *)
       IF (rVoted_ProductMassFlow_tph < 5.0) AND (rRampDownTimer_s >= 120.0) THEN
           rRampDownTimer_s := 0.0;
           rStateDwellTimer_s := 0.0;
           iFSM_CurrentState := 0; (* Return to PLANT_STANDBY_INERT_PURGE *)
       END_IF;

    10: (* ----------------------------------------------------------------------------------------------------- *)
        (* STATE 10: HOT_HOLD_RECIRCULATION                                                                     *)
        (* ----------------------------------------------------------------------------------------------------- *)
        bPlantInProduction := FALSE;
        rOut_SlurrySprayValve_pct := 0.0;
        rOut_AtomizingSteamValve_pct := 15.0; (* Thermal seal bleed *)
        rOut_BurnerGasThrottle_pct := 18.0; (* Low fire refractory maintenance *)
        rOut_CombustionAirDamper_pct := 25.0;
        rOut_DryerInducedDraftFan_pct := 30.0;
        rOut_RecycleDragConveyorSpeed_pct := 30.0; (* Slow seed turnover *)
        rOut_OversizeCageMillSpeed_RPM := 400.0;

        (* Resume production upon operator command *)
        IF bMasterAutoEnable AND bSafetyCircuitHealthy_NC THEN
            rStateDwellTimer_s := 0.0;
            iFSM_CurrentState := 5; (* Resume via NOZZLE_ATOMIZATION_PRIME *)
        END_IF;

    11: (* ----------------------------------------------------------------------------------------------------- *)
        (* STATE 11: EMERGENCY_DELUGE_FLOOD_SHUTDOWN                                                            *)
        (* ----------------------------------------------------------------------------------------------------- *)
        bPlantInProduction := FALSE;
        rDelugeHoldTimer_s := rDelugeHoldTimer_s + c_rTs;

        (* Actuate maximum safety counter-measures *)
        bOut_EmergencyDelugeFloodActuate := TRUE;
        bOut_SlurryEmergencyDumpValve := TRUE;
        bOut_BurnerSafetyShutoffValve_Trip := TRUE;
        bOut_NitrogenPurgeFloodValve := TRUE;
        bEmergencyDelugeActive := TRUE;

        rOut_SlurrySprayValve_pct := 0.0;
        rOut_AtomizingSteamValve_pct := 0.0;
        rOut_BurnerGasThrottle_pct := 0.0;
        rOut_RecycleDragConveyorSpeed_pct := 0.0;
        rOut_OversizeCageMillSpeed_RPM := 0.0;

        (* Maximize tail-gas scrubbing to knock down decomposition gas releases *)
        rOut_DryerInducedDraftFan_pct := 100.0;
        rOut_VenturiThroatDamper_pct := 90.0;
        rOut_ScrubberRecircPumpHz := 60.0;
        rOut_NitricAcidTrimValve_pct := 0.0; (* Cut acid to prevent further sensitizing *)

        (* Fault unlatch criteria: Bed cooled below 60 deg C, deluge applied >= 180s, and operator reset *)
        IF bFaultReset AND (rVoted_DrumBedTemp_degC <= 60.0) AND (rDelugeHoldTimer_s >= 180.0) THEN
            bRunawayDecompositionTripped := FALSE;
            bEmergencyDelugeActive := FALSE;
            bOut_EmergencyDelugeFloodActuate := FALSE;
            bOut_SlurryEmergencyDumpValve := FALSE;
            bOut_BurnerSafetyShutoffValve_Trip := FALSE;
            bOut_NitrogenPurgeFloodValve := FALSE;
            rDelugeHoldTimer_s := 0.0;
            rStateDwellTimer_s := 0.0;
            iFSM_CurrentState := 0; (* Reset to PLANT_STANDBY_INERT_PURGE *)
        END_IF;

END_CASE;

iActiveFSM_State := iFSM_CurrentState;
"""
    return code
