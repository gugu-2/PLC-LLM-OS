# dairy_mvr_spraydryer_builder/part6_fsm_logic.py
# Lumina Cyber-Physical Systems Chair - V7 Max-Persona
# Part 6: Phase 4 - Deterministic 14-Stage Commercial Dairy Production Finite State Machine (FSM)

def get_part6_fsm_logic():
    return """(* === PHASE 4: DETERMINISTIC 14-STAGE COMMERCIAL DAIRY PRODUCTION FSM === *)

(* State dwell timer accumulation *)
IF eState = eState_prev THEN
    tStateTimer_s := tStateTimer_s + rCycleTime_s;
ELSE
    tStateTimer_s := 0.0;
    nSubStepIndex := 0;
    eState_prev := eState;
END_IF;

(* Master Safety Interlock Override: Critical E-Stop or Suppression Trigger Forces Immediate Abort *)
IF (NOT bEmergencyStop) OR bFireDelugeManualTrigger OR (rVoted_SparkDetector_cps >= rHH_SparkDetector_cps) OR (rPT_901_ChamberPressure_Pa >= rHH_ChamberPressure_Pa) THEN
    eState := 13; (* Immediate Transition to Explosion / Fire Interlock *)
END_IF;

CASE eState OF
    (* --------------------------------------------------------------------------------------------- *)
    (* STATE 0: SANITARY IDLE PRECHECK                                                               *)
    (* Initial state: all process valves closed, calandrias empty, checking permissives              *)
    (* --------------------------------------------------------------------------------------------- *)
    0:
        nActiveState := 0;
        bConcentrateOnSpec := FALSE;
        bPowderMoistureOnSpec := FALSE;

        (* Idle Actuator Command Safeties *)
        rCV_FeedRateValve_pct           := 0.0;
        rSPD_MvrCompressor_rpm          := 0.0;
        rCV_SteamInjectionValve_pct     := 0.0;
        rCV_AtomizerNozzlePress_bar     := 0.0;
        rCV_BurnerGasModulation_pct     := 0.0;
        rCV_ExhaustDamper_pct           := 10.0; (* Minimum draft for chamber ventilation *)
        rCV_AntiSurgeBypassValve_pct    := 100.0; (* Fully open bypass *)
        rCV_WaterBalanceDivert_pct      := 100.0;
        rCV_SlurryDivertValve_pct       := 100.0;
        rCV_FluidBedSupplyFan_pct       := 0.0;
        rCV_FluidBedHeaterSteam_pct     := 0.0;
        rCV_DensePhaseConveyAir_pct     := 0.0;

        bHRD_ExplosionCannonsFire       := FALSE;
        bExplosionIsolationValvesClose  := FALSE;
        bFireDelugeActive               := FALSE;
        bEmergencyShutdownTripped       := FALSE;

        (* Check System Permissives for Sequence Start *)
        IF bEnableSystem AND bEmergencyStop THEN
            bSystemHealthy := TRUE;
            IF bCipVerificationRequest THEN
                eState := 1; (* Move to CIP verification *)
            ELSIF bWaterBalanceRequest OR bStartProduction THEN
                eState := 2; (* Advance directly to Water Balance Thermal Preheat *)
            END_IF;
        ELSE
            bSystemHealthy := FALSE;
        END_IF;

    (* --------------------------------------------------------------------------------------------- *)
    (* STATE 1: CIP CAUSTIC & ACID PREWASH SANITIZATION VERIFICATION                                 *)
    (* Verifies caustic/acid clean-in-place cycles and final neutral water rinse conductivity        *)
    (* --------------------------------------------------------------------------------------------- *)
    1:
        nActiveState := 1;
        (* Maintain valves in sanitary flush alignment *)
        rCV_FeedRateValve_pct           := 0.0;
        rSPD_MvrCompressor_rpm          := 0.0;
        rCV_SteamInjectionValve_pct     := 0.0;
        rCV_AtomizerNozzlePress_bar     := 0.0;
        rCV_BurnerGasModulation_pct     := 0.0;
        rCV_ExhaustDamper_pct           := 20.0;
        rCV_WaterBalanceDivert_pct      := 100.0;
        rCV_SlurryDivertValve_pct       := 100.0;

        (* Verify pure RO water rinse conductivity (< 0.10 mS/cm indicates complete chemical removal) *)
        IF (rQT_905_CipConductivity_mScm <= 0.100) AND (tStateTimer_s >= 5.0) THEN
            (* CIP verified sanitized; return to Idle or advance to Water Balance *)
            IF bStartProduction OR bWaterBalanceRequest THEN
                eState := 2;
            ELSE
                eState := 0;
            END_IF;
        ELSIF tStateTimer_s > 60.0 THEN
            (* Timeout waiting for neutral conductivity; abort to idle *)
            eState := 0;
        END_IF;

    (* --------------------------------------------------------------------------------------------- *)
    (* STATE 2: WATER BALANCE THERMAL PREHEAT RECIRCULATION                                          *)
    (* Circulate demineralized water through falling film calandrias, establish thermal vacuum       *)
    (* --------------------------------------------------------------------------------------------- *)
    2:
        nActiveState := 2;
        rCV_WaterBalanceDivert_pct      := 100.0; (* 100% Water Balance Infeed *)
        rCV_SlurryDivertValve_pct       := 100.0; (* Recirculate back to balance tank *)
        rCV_AtomizerNozzlePress_bar     := 0.0;
        rCV_BurnerGasModulation_pct     := 0.0;
        rCV_ExhaustDamper_pct           := 20.0;

        (* Calandria level fill and auxiliary steam heating *)
        IF rVoted_CalandriaLevel_mm < 1150.0 THEN
            rCV_FeedRateValve_pct := 65.0; (* Fill sump with water *)
        ELSIF rVoted_CalandriaLevel_mm > 1350.0 THEN
            rCV_FeedRateValve_pct := 25.0;
        ELSE
            rCV_FeedRateValve_pct := 45.0; (* Sump level stabilized *)
        END_IF;

        (* Auxiliary live steam warms calandria to boiling temperature *)
        IF rTT_902_CompressorSuction_degC < 60.0 THEN
            rCV_SteamInjectionValve_pct := 50.0;
        ELSE
            rCV_SteamInjectionValve_pct := 25.0;
        END_IF;

        (* Recirculation velocity verification *)
        IF (rVoted_RecircVelocity_ms >= 1.80) AND 
           (rVoted_CalandriaLevel_mm >= 1100.0) AND 
           (rTT_902_CompressorSuction_degC >= 58.0) AND 
           (tStateTimer_s >= 25.0) THEN
            (* Water balance established and thermal vacuum stable *)
            IF bStartProduction THEN
                eState := 3; (* Advance to Milk Feed Introduction *)
            END_IF;
        END_IF;

        IF NOT bEnableSystem THEN
            eState := 0;
        END_IF;

    (* --------------------------------------------------------------------------------------------- *)
    (* STATE 3: MILK FEED INTRODUCTION & BUMPLESS SWITCH                                             *)
    (* Transition feed from water balance to standardized raw whole milk (8.8% TS)                   *)
    (* --------------------------------------------------------------------------------------------- *)
    3:
        nActiveState := 3;
        (* Bumplessly ramp 3-way divert valve from 100% water to 0% water (100% raw milk) *)
        IF rCV_WaterBalanceDivert_pct > 0.0 THEN
            rCV_WaterBalanceDivert_pct := MAX(0.0, 100.0 - (tStateTimer_s * 5.0));
        ELSE
            rCV_WaterBalanceDivert_pct := 0.0;
        END_IF;

        (* Keep slurry diverted to rework tank until Brix concentration builds up *)
        rCV_SlurryDivertValve_pct := 100.0;

        (* Feed valve modulated by MPC closed-loop level control *)
        rCV_FeedRateValve_pct := vec_uCmd[1];
        rCV_SteamInjectionValve_pct := 40.0; (* Maintain thermal heat input during displacement *)

        (* Sump Brix begins rising as milk displaces water in falling film tubes *)
        IF (rVoted_SolidsBrix_pct >= 14.0) AND (tStateTimer_s >= 30.0) AND (rCV_WaterBalanceDivert_pct = 0.0) THEN
            eState := 4; (* Advance to Concentration Rampup *)
        END_IF;

        IF NOT bEnableSystem THEN
            eState := 11; (* Flush and empty if aborted *)
        END_IF;

    (* --------------------------------------------------------------------------------------------- *)
    (* STATE 4: CONCENTRATION RAMPUP ACROSS EFFECTS 1, 2, 3                                          *)
    (* Build solid concentration gradient in calandrias; vapor production begins                     *)
    (* --------------------------------------------------------------------------------------------- *)
    4:
        nActiveState := 4;
        rCV_WaterBalanceDivert_pct  := 0.0;
        rCV_SlurryDivertValve_pct   := 100.0; (* Concentrate still building; recycle *)
        rCV_FeedRateValve_pct       := vec_uCmd[1];
        rCV_SteamInjectionValve_pct := 55.0; (* Higher steam duty to drive initial evaporation *)
        rSPD_MvrCompressor_rpm      := 3000.0; (* Idle spinup *)
        rCV_AntiSurgeBypassValve_pct := 100.0;

        (* Check for minimum tube wetting velocity to prevent scorching *)
        IF rVoted_RecircVelocity_ms < 1.40 THEN
            (* Sump recirculation velocity low; risk of film drying *)
            rCV_FeedRateValve_pct := MIN(100.0, rCV_FeedRateValve_pct + 15.0);
        END_IF;

        (* When vapor generation is confirmed and Brix reaches 35.0% TS, engage MVR turbo-compressor *)
        IF (rVoted_SolidsBrix_pct >= 32.0) AND (rTT_902_CompressorSuction_degC >= 60.0) AND (tStateTimer_s >= 40.0) THEN
            eState := 5; (* Advance to MVR Compressor Coupling *)
        END_IF;

        IF NOT bEnableSystem THEN
            eState := 11;
        END_IF;

    (* --------------------------------------------------------------------------------------------- *)
    (* STATE 5: MVR COMPRESSOR SPINUP AND VAPOR COUPLING                                             *)
    (* Ramp turbo-compressor from 3,000 to operating speed (8,500 - 10,500 rpm) & decouple steam    *)
    (* --------------------------------------------------------------------------------------------- *)
    5:
        nActiveState := 5;
        rCV_WaterBalanceDivert_pct := 0.0;
        rCV_SlurryDivertValve_pct  := 100.0;
        rCV_FeedRateValve_pct      := vec_uCmd[1];

        (* MVR Speed Ramp: Accelerate by 150 rpm per second *)
        IF rSPD_MvrCompressor_rpm < 9200.0 THEN
            rSPD_MvrCompressor_rpm := MIN(9200.0, 3000.0 + (tStateTimer_s * 150.0));
        ELSE
            rSPD_MvrCompressor_rpm := vec_uCmd[2]; (* Transfer to MPC control *)
        END_IF;

        (* As MVR pressure climbs, taper off auxiliary live steam *)
        IF rVoted_MvrDiffPress_kPa >= 25.0 THEN
            rCV_SteamInjectionValve_pct := MAX(5.0, 40.0 - ((rVoted_MvrDiffPress_kPa - 25.0) * 2.50));
            rCV_AntiSurgeBypassValve_pct := rAntiSurgePidOutput; (* Active anti-surge modulation *)
        ELSE
            rCV_SteamInjectionValve_pct := 35.0;
            rCV_AntiSurgeBypassValve_pct := 80.0;
        END_IF;

        (* Check if concentrate reaches 48.0% TS and MVR is thermally stable *)
        IF (rVoted_SolidsBrix_pct >= 48.0) AND (rVoted_MvrDiffPress_kPa >= 32.0) AND (tStateTimer_s >= 50.0) THEN
            bConcentrateOnSpec := TRUE;
            eState := 6; (* Advance to Spray Tower Burner Preheat *)
        END_IF;

        IF NOT bEnableSystem THEN
            eState := 11;
        END_IF;

    (* --------------------------------------------------------------------------------------------- *)
    (* STATE 6: SPRAY DRYER BURNER & AIR INTAKE PREHEAT (INLET 190.0 DEG C)                          *)
    (* Establish chamber draft (-120 Pa) and ramp direct-fired gas burner to 195.0 deg C             *)
    (* --------------------------------------------------------------------------------------------- *)
    6:
        nActiveState := 6;
        (* Keep evaporator operating steadily at setpoint with MPC *)
        rCV_FeedRateValve_pct       := vec_uCmd[1];
        rSPD_MvrCompressor_rpm      := vec_uCmd[2];
        rCV_SteamInjectionValve_pct := vec_uCmd[3];
        rCV_AntiSurgeBypassValve_pct := rAntiSurgePidOutput;

        (* Concentrate continues circulating to rework balance tank while dryer preheats *)
        rCV_SlurryDivertValve_pct := 100.0;

        (* Dryer ventilation fan draft balance *)
        rCV_ExhaustDamper_pct := 55.0;
        IF rPT_901_ChamberPressure_Pa > -80.0 THEN
            rCV_ExhaustDamper_pct := 65.0; (* Pull more draft *)
        ELSIF rPT_901_ChamberPressure_Pa < -180.0 THEN
            rCV_ExhaustDamper_pct := 45.0; (* Reduce suction *)
        END_IF;

        (* Burner modulation ramps inlet air temperature toward 195.0 deg C *)
        IF rVoted_InletAirTemp_degC < 190.0 THEN
            rCV_BurnerGasModulation_pct := MIN(75.0, 20.0 + (tStateTimer_s * 1.25));
        ELSE
            rCV_BurnerGasModulation_pct := vec_uCmd[5]; (* Transfer to MPC *)
        END_IF;

        (* Fluid bed preconditioning *)
        rCV_FluidBedSupplyFan_pct   := 40.0;
        rCV_FluidBedHeaterSteam_pct := 30.0;

        (* Once inlet temp reaches >= 190 deg C and exhaust temp >= 82 deg C, advance to atomization *)
        IF (rVoted_InletAirTemp_degC >= 190.0) AND 
           (rVoted_ExhaustTemp_degC >= 82.0) AND 
           (rVoted_SolidsBrix_pct >= 48.0) AND 
           (tStateTimer_s >= 45.0) THEN
            eState := 7; (* Advance to Atomization Slurry Feed *)
        END_IF;

        IF NOT bEnableSystem THEN
            eState := 11;
        END_IF;

    (* --------------------------------------------------------------------------------------------- *)
    (* STATE 7: HIGH-PRESSURE ATOMIZATION SLURRY FEED                                                *)
    (* Energize homogenizer nozzle pump (210 bar) and switch concentrate into drying chamber        *)
    (* --------------------------------------------------------------------------------------------- *)
    7:
        nActiveState := 7;
        (* Full MPC closed-loop control of evaporator *)
        rCV_FeedRateValve_pct       := vec_uCmd[1];
        rSPD_MvrCompressor_rpm      := vec_uCmd[2];
        rCV_SteamInjectionValve_pct := vec_uCmd[3];
        rCV_AntiSurgeBypassValve_pct := rAntiSurgePidOutput;

        (* Spin up atomizer nozzle pressure to 210 bar *)
        IF rCV_AtomizerNozzlePress_bar < 200.0 THEN
            rCV_AtomizerNozzlePress_bar := MIN(210.0, 150.0 + (tStateTimer_s * 5.0));
        ELSE
            rCV_AtomizerNozzlePress_bar := vec_uCmd[4];
        END_IF;

        (* Bumplessly switch 3-way divert valve from rework tank to drying chamber *)
        IF (rCV_AtomizerNozzlePress_bar >= 190.0) AND (rCV_SlurryDivertValve_pct > 0.0) THEN
            rCV_SlurryDivertValve_pct := MAX(0.0, 100.0 - ((tStateTimer_s - 10.0) * 10.0));
        ELSIF rCV_AtomizerNozzlePress_bar >= 190.0 THEN
            rCV_SlurryDivertValve_pct := 0.0; (* 100% feed to tower atomizer *)
        END_IF;

        rCV_BurnerGasModulation_pct := vec_uCmd[5];
        rCV_ExhaustDamper_pct       := vec_uCmd[6];

        (* Check if drying tower is operating stably and exhaust temp is within [84..92 deg C] *)
        IF (rCV_SlurryDivertValve_pct = 0.0) AND 
           (rVoted_ExhaustTemp_degC >= 84.0) AND 
           (rVoted_ExhaustTemp_degC <= 92.0) AND 
           (tStateTimer_s >= 35.0) THEN
            eState := 8; (* Advance to Fluidized Bed Conditioning *)
        END_IF;

        IF NOT bEnableSystem THEN
            eState := 11;
        END_IF;

    (* --------------------------------------------------------------------------------------------- *)
    (* STATE 8: FLUIDIZED BED SECONDARY DRYING & CONDITIONING                                        *)
    (* Two-stage vibrating fluid bed (VFB): Zone 1 secondary drying (76 deg C), Zone 2 cooling (21 deg C) *)
    (* --------------------------------------------------------------------------------------------- *)
    8:
        nActiveState := 8;
        (* All core MPC actuators modulating *)
        rCV_FeedRateValve_pct       := vec_uCmd[1];
        rSPD_MvrCompressor_rpm      := vec_uCmd[2];
        rCV_SteamInjectionValve_pct := vec_uCmd[3];
        rCV_AtomizerNozzlePress_bar := vec_uCmd[4];
        rCV_BurnerGasModulation_pct := vec_uCmd[5];
        rCV_ExhaustDamper_pct       := vec_uCmd[6];
        rCV_WaterBalanceDivert_pct  := 0.0;
        rCV_SlurryDivertValve_pct   := 0.0;
        rCV_AntiSurgeBypassValve_pct := rAntiSurgePidOutput;

        (* Fluid bed Zone 1 Agglomeration & Zone 2 Conditioning active *)
        rCV_FluidBedSupplyFan_pct   := 65.0;
        IF rTT_908_FluidBedZone1Temp_degC < 75.0 THEN
            rCV_FluidBedHeaterSteam_pct := 55.0;
        ELSE
            rCV_FluidBedHeaterSteam_pct := 35.0;
        END_IF;

        (* Check final milk powder moisture NIR reading *)
        IF (rVoted_PowderMoisture_pct >= 3.40) AND (rVoted_PowderMoisture_pct <= 4.10) AND (tStateTimer_s >= 25.0) THEN
            bPowderMoistureOnSpec := TRUE;
            eState := 9; (* Advance to Continuous Dense-Phase Pneumatic Conveying *)
        END_IF;

        IF NOT bEnableSystem THEN
            eState := 11;
        END_IF;

    (* --------------------------------------------------------------------------------------------- *)
    (* STATE 9: POWDER DENSE-PHASE PNEUMATIC CONVEYING & CONTINUOUS PRODUCTION                       *)
    (* Full commercial production: 50,000 kg/h milk -> 5,500 kg/h premium dry milk powder           *)
    (* --------------------------------------------------------------------------------------------- *)
    9:
        nActiveState := 9;
        bConcentrateOnSpec := TRUE;
        bPowderMoistureOnSpec := TRUE;

        (* Fully autonomous closed-loop cyber-physical MPC control *)
        rCV_FeedRateValve_pct       := vec_uCmd[1];
        rSPD_MvrCompressor_rpm      := vec_uCmd[2];
        rCV_SteamInjectionValve_pct := vec_uCmd[3];
        rCV_AtomizerNozzlePress_bar := vec_uCmd[4];
        rCV_BurnerGasModulation_pct := vec_uCmd[5];
        rCV_ExhaustDamper_pct       := vec_uCmd[6];
        rCV_WaterBalanceDivert_pct  := 0.0;
        rCV_SlurryDivertValve_pct   := 0.0;
        rCV_AntiSurgeBypassValve_pct := rAntiSurgePidOutput;

        rCV_FluidBedSupplyFan_pct   := 70.0;
        rCV_FluidBedHeaterSteam_pct := 38.0;
        rCV_DensePhaseConveyAir_pct := 80.0; (* Dense phase nitrogen/dry air conveying active *)

        (* Quality Supervision: If solids drop or moisture strays out of spec, trigger divert *)
        IF (rVoted_SolidsBrix_pct < rL_SolidsBrix_pct) OR (rVoted_PowderMoisture_pct > rH_PowderMoisture_pct) OR bConcentrateDivertManual THEN
            bConcentrateOnSpec := FALSE;
            bPowderMoistureOnSpec := FALSE;
            eState := 10; (* Divert out of spec *)
        END_IF;

        (* Graceful Stop Request *)
        IF bStopProduction OR (NOT bEnableSystem) THEN
            eState := 11; (* Flush and Empty Sequence *)
        END_IF;

    (* --------------------------------------------------------------------------------------------- *)
    (* STATE 10: FLASH CONCENTRATE DIVERT OUT OF SPEC                                                *)
    (* Total solids < 46.0% or moisture > 4.5%: instantly switch concentrate to rework balance tank  *)
    (* --------------------------------------------------------------------------------------------- *)
    10:
        nActiveState := 10;
        bConcentrateOnSpec := FALSE;
        bPowderMoistureOnSpec := FALSE;

        (* Instantly divert slurry from spray dryer to rework tank *)
        rCV_SlurryDivertValve_pct := 100.0;

        (* Flush atomizer with water to prevent nozzle caking and scorch *)
        rCV_AtomizerNozzlePress_bar := 160.0;

        (* Keep evaporator operating with MPC to rebuild solids concentration *)
        rCV_FeedRateValve_pct       := MAX(10.0, vec_uCmd[1] - 15.0); (* Reduce feed to concentrate *)
        rSPD_MvrCompressor_rpm      := vec_uCmd[2];
        rCV_SteamInjectionValve_pct := vec_uCmd[3] + 10.0;
        rCV_AntiSurgeBypassValve_pct := rAntiSurgePidOutput;

        (* Turn down burner slightly while slurry is diverted *)
        rCV_BurnerGasModulation_pct := 35.0;
        rCV_ExhaustDamper_pct       := 40.0;
        rCV_DensePhaseConveyAir_pct := 30.0;

        (* If solids recover >= 48.5% TS for 30 consecutive seconds, return to Atomization / Production *)
        IF (rVoted_SolidsBrix_pct >= 48.5) AND (NOT bConcentrateDivertManual) AND (tStateTimer_s >= 30.0) THEN
            bConcentrateOnSpec := TRUE;
            eState := 7; (* Resume spray drying *)
        END_IF;

        (* Timeout on out of spec divert: if not recovered in 300 s, initiate flush shutdown *)
        IF tStateTimer_s > 300.0 THEN
            eState := 11;
        END_IF;

    (* --------------------------------------------------------------------------------------------- *)
    (* STATE 11: WATER FLUSH & SYSTEM EMPTY SEQUENCE                                                 *)
    (* Controlled end of campaign: push milk concentrate out with water, sweep drying tower          *)
    (* --------------------------------------------------------------------------------------------- *)
    11:
        nActiveState := 11;
        bConcentrateOnSpec := FALSE;
        bPowderMoistureOnSpec := FALSE;

        (* Switch feed to deaerated water balance *)
        rCV_WaterBalanceDivert_pct := 100.0;
        rCV_FeedRateValve_pct      := 50.0;

        (* Push concentrate into rework tank *)
        rCV_SlurryDivertValve_pct  := 100.0;

        (* Controlled rampdown of MVR compressor *)
        IF rSPD_MvrCompressor_rpm > 3200.0 THEN
            rSPD_MvrCompressor_rpm := MAX(3000.0, rSPD_MvrCompressor_rpm - (rCycleTime_s * 200.0));
        ELSE
            rSPD_MvrCompressor_rpm := 0.0;
        END_IF;
        rCV_AntiSurgeBypassValve_pct := 100.0;
        rCV_SteamInjectionValve_pct  := 0.0;

        (* Ramp down burner and cool chamber *)
        rCV_AtomizerNozzlePress_bar := 0.0;
        IF rCV_BurnerGasModulation_pct > 0.0 THEN
            rCV_BurnerGasModulation_pct := MAX(0.0, rCV_BurnerGasModulation_pct - (rCycleTime_s * 5.0));
        END_IF;
        rCV_ExhaustDamper_pct := 30.0;

        (* Sweep powder from fluid bed and blow lines *)
        rCV_FluidBedSupplyFan_pct   := 35.0;
        rCV_FluidBedHeaterSteam_pct := 0.0;
        rCV_DensePhaseConveyAir_pct := 50.0;

        (* Once calandria is flushed and chamber cooled below 65 deg C, return to Idle *)
        IF (rVoted_SolidsBrix_pct <= 9.5) AND (rVoted_ExhaustTemp_degC <= 65.0) AND (tStateTimer_s >= 60.0) THEN
            eState := 0; (* Ready for CIP sanitization *)
        END_IF;

    (* --------------------------------------------------------------------------------------------- *)
    (* STATE 12: FOULING BURNOUT OR UNRECOVERABLE PROCESS EMERGENCY SHUTDOWN                         *)
    (* Rapid shutdown: vacuum collapse, severe tube heat transfer fouling, or mechanical trip       *)
    (* --------------------------------------------------------------------------------------------- *)
    12:
        nActiveState := 12;
        bEmergencyShutdownTripped := TRUE;
        bConcentrateOnSpec := FALSE;
        bPowderMoistureOnSpec := FALSE;

        (* Immediate cutoff of thermal heat sources *)
        rCV_FeedRateValve_pct           := 0.0;
        rCV_SteamInjectionValve_pct     := 0.0;
        rCV_BurnerGasModulation_pct     := 0.0;
        rCV_AtomizerNozzlePress_bar     := 0.0;
        rCV_SlurryDivertValve_pct       := 100.0;
        rCV_WaterBalanceDivert_pct      := 100.0;

        (* Rapid MVR compressor deceleration *)
        rSPD_MvrCompressor_rpm          := 0.0;
        rCV_AntiSurgeBypassValve_pct    := 100.0;

        (* Maintain exhaust draft to purge vapors *)
        rCV_ExhaustDamper_pct           := 50.0;
        rCV_FluidBedSupplyFan_pct       := 0.0;
        rCV_FluidBedHeaterSteam_pct     := 0.0;
        rCV_DensePhaseConveyAir_pct     := 0.0;

        (* Requires manual operator fault reset and acknowledge to clear *)
        IF bAcknowledgeFault AND bResetTrips AND bEmergencyStop THEN
            eState := 0;
        END_IF;

    (* --------------------------------------------------------------------------------------------- *)
    (* STATE 13: NFPA 68/69 EXPLOSION ISOLATION & FIRE DELUGE INTERLOCK                              *)
    (* Critical Deflagration / Ember Fire Event: <10 ms HRD Cannons, Knife Valves, Deluge Active   *)
    (* --------------------------------------------------------------------------------------------- *)
    13:
        nActiveState := 13;
        bEmergencyShutdownTripped       := TRUE;
        bConcentrateOnSpec              := FALSE;
        bPowderMoistureOnSpec           := FALSE;

        (* <10 ms Critical Safety Action *)
        bHRD_ExplosionCannonsFire       := TRUE;  (* Fire sodium bicarbonate suppression canisters *)
        bExplosionIsolationValvesClose  := TRUE;  (* Slam shut fast-acting knife gate valves *)
        bFireDelugeActive               := TRUE;  (* High-pressure water/steam fire deluge open *)

        (* Kill all prime movers and fuel sources *)
        rCV_FeedRateValve_pct           := 0.0;
        rSPD_MvrCompressor_rpm          := 0.0;
        rCV_SteamInjectionValve_pct     := 0.0;
        rCV_AtomizerNozzlePress_bar     := 0.0;
        rCV_BurnerGasModulation_pct     := 0.0;
        rCV_ExhaustDamper_pct           := 0.0;   (* Slam damper shut to starve fire of air *)
        rCV_AntiSurgeBypassValve_pct    := 100.0;
        rCV_WaterBalanceDivert_pct      := 100.0;
        rCV_SlurryDivertValve_pct       := 100.0;
        rCV_FluidBedSupplyFan_pct       := 0.0;
        rCV_FluidBedHeaterSteam_pct     := 0.0;
        rCV_DensePhaseConveyAir_pct     := 0.0;

        (* Hard lockout: requires full physical plant inspection and dual key reset *)
        IF bAcknowledgeFault AND bResetTrips AND bEmergencyStop AND (NOT bFireDelugeManualTrigger) AND (rVoted_SparkDetector_cps < rH_SparkDetector_cps) THEN
            bHRD_ExplosionCannonsFire := FALSE;
            bFireDelugeActive := FALSE;
            bExplosionIsolationValvesClose := FALSE;
            eState := 0;
        END_IF;

ELSE
    eState := 0;
END_CASE;
"""
