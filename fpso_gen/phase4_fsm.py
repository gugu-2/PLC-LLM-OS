# fpso_gen/phase4_fsm.py
def get_phase4():
    return """
(* =====================================================================================================================
 * PHASE 4: 14-STAGE DETERMINISTIC PRODUCTION FINITE STATE MACHINE (FSM)
 * Architected in accordance with API 617, API 521, and IEC 61508 SIL-3 deterministic safety sequence architecture.
 * Stages 10 to 140 execute complete lifecycle from nitrogen inerting to full MPC export, wave dampening, and SIL-3 EDP.
 * ===================================================================================================================== *)

(* Update state dwell timer *)
IF iFSM_State = iFSM_PrevState THEN
    rFSM_StateTimer := rFSM_StateTimer + rTs;
ELSE
    rFSM_StateTimer := 0.0;
    rFSM_SubTimer := 0.0;
    iFSM_PrevState := iFSM_State;
END_IF;

(* Master Safety Interlock Override: Immediate Transition to SIL-3 EDP or Mechanical Trip *)
IF bCmd_EmergencyDepress_In OR bTrip_EmergencyDepress_Manual THEN
    iFSM_State := 130; (* Force SIL-3 Emergency Depressurization *)
ELSIF bTrip_SuctionPres_HH OR bTrip_DischargePres_HH OR bTrip_ShaftVibration_HH OR
      bTrip_LubeOil_LL OR bTrip_SealGas_LL OR bTrip_Reboiler_HH OR bTrip_TMR_CriticalLoss THEN
    IF iFSM_State <> 130 AND iFSM_State <> 140 THEN
        iFSM_State := 130; (* Safety blowdown on catastrophic process containment threat *)
    END_IF;
END_IF;

CASE iFSM_State OF

    (* -----------------------------------------------------------------------------------------------------------------
     * STAGE 10: STATE_NITROGEN_INERT_TEST
     * Casing nitrogen pressurization to 15 bar, acoustic leak detection, and oxygen purge verification (< 0.5 vol%).
     * ----------------------------------------------------------------------------------------------------------------- *)
    10:
        (* Actuator Demand Outputs *)
        rAntiSurgeValve_Stg1_Cmd_Out := 100.0; (* Fail-open full recycle position *)
        rAntiSurgeValve_Stg2_Cmd_Out := 100.0;
        rAntiSurgeValve_Stg3_Cmd_Out := 100.0;
        rVFD_Speed_Demand_Out := 0.0;          (* Drive motor stationary *)
        rSuctionChoke_Cmd_Out := 0.0;          (* Infeed header closed *)
        rExportChoke_Cmd_Out := 0.0;           (* Pipeline export closed *)
        bEDP_HP_FlareValve_Open_Out := FALSE;
        bEDP_LP_FlareValve_Open_Out := FALSE;
        bInfeed_Isolation_Close_Out := FALSE;
        bExport_Isolation_Close_Out := FALSE;
        bVFD_EmergencyTrip_Out := FALSE;
        rTEG_Pump_Speed_Cmd_Out := 0.0;
        rTEG_Reboiler_Duty_Cmd_Out := 0.0;

        (* Status Telemetry *)
        bSystem_Ready_Out := FALSE;
        bTrain_Pressurized := FALSE;

        (* Transition Guards: Operator Start Pulse, Flare & Infeed Permissives, and 30s Inerting Dwell *)
        IF bCmd_Start_In AND bPermissive_InfeedGas_In AND bPermissive_FlareSystem_In THEN
            IF rFSM_StateTimer >= 30.0 THEN
                bTrain_Pressurized := TRUE;
                iFSM_State := 20; (* Transition to Lube Oil & Seal Gas Verification *)
            END_IF;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STAGE 20: STATE_LUBEOIL_SEALGAS_LOCK
     * Establishing pressurized lube oil film on hydrodynamic tilting-pad journal bearings and dry gas seal barrier DP.
     * ----------------------------------------------------------------------------------------------------------------- *)
    20:
        rAntiSurgeValve_Stg1_Cmd_Out := 100.0;
        rAntiSurgeValve_Stg2_Cmd_Out := 100.0;
        rAntiSurgeValve_Stg3_Cmd_Out := 100.0;
        rVFD_Speed_Demand_Out := 0.0;
        rSuctionChoke_Cmd_Out := 0.0;
        rExportChoke_Cmd_Out := 0.0;

        (* Start Auxiliary Lube Oil Skid if Header Pressure Below Permissive *)
        IF rLubeOilPres_PT601_In < 3.20 THEN
            bLubeOil_AuxPump_Start_Out := TRUE;
        ELSE
            bLubeOil_AuxPump_Start_Out := FALSE;
        END_IF;

        (* Verify Bearing Oil Pressure (> 3.5 bar), Temperature (38-55 °C), and Seal Gas DP (> 2.0 bar) *)
        IF (rLubeOilPres_PT601_In >= 3.50) AND
           (rLubeOilTemp_TT601_In >= 38.0 AND rLubeOilTemp_TT601_In <= 55.0) AND
           (rSealGasDP_PDT701_In >= 2.00) THEN
            rFSM_SubTimer := rFSM_SubTimer + rTs;
            IF rFSM_SubTimer >= 15.0 THEN
                bLubeOil_Normal := TRUE;
                bSealGas_Normal := TRUE;
                iFSM_State := 30; (* Transition to VFD Motor Warmup & Inching *)
            END_IF;
        ELSE
            rFSM_SubTimer := 0.0;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STAGE 30: STATE_VFD_WARMUP_INCH
     * 60 MW Drive pre-magnetization, slow mechanical inching at 300 rpm for 60s to prevent rotor thermal bow.
     * ----------------------------------------------------------------------------------------------------------------- *)
    30:
        rAntiSurgeValve_Stg1_Cmd_Out := 100.0;
        rAntiSurgeValve_Stg2_Cmd_Out := 100.0;
        rAntiSurgeValve_Stg3_Cmd_Out := 100.0;

        (* Inching Speed Demand: 300 rpm for initial 60 seconds, then ramp to 6,000 rpm idle *)
        IF rFSM_StateTimer < 60.0 THEN
            rVFD_Speed_Demand_Out := 300.0;
            (* Verify zero radial rubbing: Shaft vibration must stay below 18 um *)
            IF rVoted_ShaftVib_Out > 18.0 THEN
                bTrip_ShaftVibration_HH := TRUE;
            END_IF;
        ELSE
            (* Controlled Ramp to Minimum Governed Idle Speed (6,000 rpm at 35 rpm/s) *)
            rVFD_Speed_Demand_Out := 300.0 + ((rFSM_StateTimer - 60.0) * 35.0);
            IF rVFD_Speed_Demand_Out >= 6000.0 THEN
                rVFD_Speed_Demand_Out := 6000.0;
                bWarmup_Completed := TRUE;
                bCompressor_AtIdle := TRUE;
                iFSM_State := 40; (* Transition to Hydrocarbon Infeed Purge *)
            END_IF;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STAGE 40: STATE_HC_INFEED_PURGE
     * Controlled displacement of casing nitrogen by hydrocarbon feed gas from upstream slug catcher to flare header.
     * ----------------------------------------------------------------------------------------------------------------- *)
    40:
        rAntiSurgeValve_Stg1_Cmd_Out := 100.0;
        rAntiSurgeValve_Stg2_Cmd_Out := 100.0;
        rAntiSurgeValve_Stg3_Cmd_Out := 100.0;
        rVFD_Speed_Demand_Out := 6000.0;

        (* Crack Suction Choke Valve to 18.5% to admit process gas slowly *)
        rSuctionChoke_Cmd_Out := 18.5;

        (* Verify feed gas molecular weight and suction pressure building up to nominal *)
        IF (rVoted_SuctionPres_Out >= 21.5) AND (rGasMolecularWeight_In >= 16.0) THEN
            rFSM_SubTimer := rFSM_SubTimer + rTs;
            IF rFSM_SubTimer >= 40.0 THEN
                rSuctionChoke_Cmd_Out := 50.0;
                iFSM_State := 50; (* Transition to Anti-Surge Fast Valve Dynamic Prime *)
            END_IF;
        ELSE
            rFSM_SubTimer := 0.0;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STAGE 50: STATE_ANTISURGE_PRIME_OPEN
     * Dynamic verification of high-speed anti-surge valve actuators (< 1.2s stroke) and quench cooling line readiness.
     * ----------------------------------------------------------------------------------------------------------------- *)
    50:
        rVFD_Speed_Demand_Out := 6000.0;
        rSuctionChoke_Cmd_Out := 50.0;

        (* Verify full opening stroke and calibrate position feedback *)
        rAntiSurgeValve_Stg1_Cmd_Out := 100.0;
        rAntiSurgeValve_Stg2_Cmd_Out := 100.0;
        rAntiSurgeValve_Stg3_Cmd_Out := 100.0;

        (* Interstage cooler bypass modulation for anti-surge quench *)
        rInterstageCooler1_Bypass_Out := 25.0;
        rInterstageCooler2_Bypass_Out := 25.0;

        IF rFSM_StateTimer >= 15.0 THEN
            iFSM_State := 60; (* Transition to High-Pressure Compression Ramp *)
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STAGE 60: STATE_HP_COMPRESSION_RAMP
     * Ramping compressor shaft speed from 6,000 rpm idle to 9,800 rpm nominal export operating speed at 40 rpm/s.
     * ----------------------------------------------------------------------------------------------------------------- *)
    60:
        rSuctionChoke_Cmd_Out := 80.0;
        (* Maintain 85% recycle during acceleration to ensure massive surge margin *)
        rAntiSurgeValve_Stg1_Cmd_Out := 85.0;
        rAntiSurgeValve_Stg2_Cmd_Out := 85.0;
        rAntiSurgeValve_Stg3_Cmd_Out := 85.0;

        (* Speed Ramp Calculation *)
        rVFD_Speed_Demand_Out := 6000.0 + (rFSM_StateTimer * 40.0);
        IF rVFD_Speed_Demand_Out >= 9800.0 THEN
            rVFD_Speed_Demand_Out := 9800.0;
            (* Verify Discharge Pressure rises above 215 bar *)
            IF rVoted_DischargePres_Out >= 215.0 THEN
                bCompressor_AtFullSpeed := TRUE;
                iFSM_State := 70; (* Transition to TEG Dehydration Circulation Lock *)
            END_IF;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STAGE 70: STATE_TEG_CIRCULATION_LOCK
     * Start high-pressure triplex lean glycol pumps, establish absorption in 130 bar contactor, stabilize reboiler at 204 °C.
     * ----------------------------------------------------------------------------------------------------------------- *)
    70:
        rVFD_Speed_Demand_Out := 9800.0;
        rSuctionChoke_Cmd_Out := 100.0;
        rAntiSurgeValve_Stg1_Cmd_Out := 75.0;
        rAntiSurgeValve_Stg2_Cmd_Out := 75.0;
        rAntiSurgeValve_Stg3_Cmd_Out := 75.0;

        (* Engage Lean Glycol Circulation Pump to 70% Speed *)
        rTEG_Pump_Speed_Cmd_Out := 70.0;
        (* Modulate Reboiler Heating Duty to track 204.0 °C *)
        IF rTEG_ReboilerTemp_TT503_In < 203.0 THEN
            rTEG_Reboiler_Duty_Cmd_Out := 85.0;
        ELSIF rTEG_ReboilerTemp_TT503_In > 204.5 THEN
            rTEG_Reboiler_Duty_Cmd_Out := 40.0;
        ELSE
            rTEG_Reboiler_Duty_Cmd_Out := 65.0;
        END_IF;
        rTEG_StrippingGas_Cmd_Out := 35.0;

        (* Verify Export Gas Moisture Content drops below export pipeline specification (< 25.0 ppmv) *)
        IF (rVoted_ExportMoisture_Out <= 25.0) AND (rTEG_ReboilerTemp_TT503_In >= 202.0) THEN
            rFSM_SubTimer := rFSM_SubTimer + rTs;
            IF rFSM_SubTimer >= 25.0 THEN
                bTEG_SystemLocked := TRUE;
                iFSM_State := 80; (* Transition to Export Pipeline Flow Synchronization *)
            END_IF;
        ELSE
            rFSM_SubTimer := 0.0;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STAGE 80: STATE_EXPORT_SYNC_BALANCE
     * Equalize compressor discharge pressure with subsea pipeline backpressure and smoothly open export choke.
     * ----------------------------------------------------------------------------------------------------------------- *)
    80:
        rVFD_Speed_Demand_Out := 9800.0;
        rTEG_Pump_Speed_Cmd_Out := 75.0;
        rTEG_Reboiler_Duty_Cmd_Out := 68.0;

        (* Slowly crack export choke valve open *)
        rExportChoke_Cmd_Out := (rFSM_StateTimer / 30.0) * 45.0;
        IF rExportChoke_Cmd_Out > 45.0 THEN
            rExportChoke_Cmd_Out := 45.0;
        END_IF;

        (* Concurrently trim anti-surge valves down to 35% *)
        rAntiSurgeValve_Stg1_Cmd_Out := 75.0 - ((rFSM_StateTimer / 30.0) * 40.0);
        rAntiSurgeValve_Stg2_Cmd_Out := 75.0 - ((rFSM_StateTimer / 30.0) * 40.0);
        rAntiSurgeValve_Stg3_Cmd_Out := 75.0 - ((rFSM_StateTimer / 30.0) * 40.0);
        IF rAntiSurgeValve_Stg1_Cmd_Out < 35.0 THEN
            rAntiSurgeValve_Stg1_Cmd_Out := 35.0;
            rAntiSurgeValve_Stg2_Cmd_Out := 35.0;
            rAntiSurgeValve_Stg3_Cmd_Out := 35.0;
        END_IF;

        (* Verify pipeline permissive and pressure differential across choke < 3.0 bar *)
        IF bPermissive_ExportPipeline_In AND (ABS(rVoted_DischargePres_Out - rPipeline_BackPres_PT801_In) <= 3.0) THEN
            IF rFSM_StateTimer >= 35.0 THEN
                bExport_Synchronized := TRUE;
                bSystem_Ready_Out := TRUE;
                iFSM_State := 90; (* Transition to Normal Export Compression Closed-Loop MPC Mode *)
            END_IF;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STAGE 90: STATE_NORMAL_EXPORT_MPC
     * Full Closed-Loop Model Predictive Control Active: Optimizes ASV trim and VFD speed for maximum pipeline export.
     * ----------------------------------------------------------------------------------------------------------------- *)
    90:
        rSuctionChoke_Cmd_Out := 100.0;
        rExportChoke_Cmd_Out := 100.0;
        bSystem_Ready_Out := TRUE;

        (* Apply MPC Optimal Control Demands *)
        rAntiSurgeValve_Stg1_Cmd_Out := rVec_u[1];
        rAntiSurgeValve_Stg2_Cmd_Out := rVec_u[2];
        rAntiSurgeValve_Stg3_Cmd_Out := rVec_u[3];
        rVFD_Speed_Demand_Out := 9800.0 + rVec_u[4];

        (* Clamp Master VFD Speed Output to Certified Operating Envelope [7,200 rpm to 11,200 rpm] *)
        IF rVFD_Speed_Demand_Out < 7200.0 THEN
            rVFD_Speed_Demand_Out := 7200.0;
        ELSIF rVFD_Speed_Demand_Out > 11200.0 THEN
            rVFD_Speed_Demand_Out := 11200.0;
        END_IF;

        (* Closed-loop TEG Reboiler & Circulation Regulation *)
        rTEG_Pump_Speed_Cmd_Out := 75.0 + (0.55 * (rVoted_ExportMoisture_Out - 15.0));
        IF rTEG_Pump_Speed_Cmd_Out < 40.0 THEN
            rTEG_Pump_Speed_Cmd_Out := 40.0;
        ELSIF rTEG_Pump_Speed_Cmd_Out > 100.0 THEN
            rTEG_Pump_Speed_Cmd_Out := 100.0;
        END_IF;

        IF rTEG_ReboilerTemp_TT503_In < 203.5 THEN
            rTEG_Reboiler_Duty_Cmd_Out := 72.0;
        ELSIF rTEG_ReboilerTemp_TT503_In > 204.8 THEN
            rTEG_Reboiler_Duty_Cmd_Out := 52.0;
        ELSE
            rTEG_Reboiler_Duty_Cmd_Out := 64.0;
        END_IF;

        (* Dynamic Transitions to Degraded or Alternative Operational Modes *)
        IF bCmd_Stop_In THEN
            iFSM_State := 120; (* Controlled Train Derate & Hot Recycle Idle *)
        ELSIF rVessel_TiltAngle >= 5.50 OR ABS(rFPSO_HeaveAccel_In) >= 2.20 THEN
            iFSM_State := 110; (* Wave Motion & Marine Hull Dynamic Dampening Mode *)
        ELSIF rVoted_SuctionDP_Out < 55.0 THEN
            iFSM_State := 100; (* Severe Process Infeed Turndown Mode *)
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STAGE 100: STATE_QUENCH_TURNDOWN_RECYCLE
     * Low field production turndown (< 40%): Modulating ASVs and interstage quench cooling to prevent thermal buildup.
     * ----------------------------------------------------------------------------------------------------------------- *)
    100:
        (* Force minimum recycle valve openings to 45% to stay well clear of surge *)
        IF rVec_u[1] < 45.0 THEN
            rAntiSurgeValve_Stg1_Cmd_Out := 45.0;
        ELSE
            rAntiSurgeValve_Stg1_Cmd_Out := rVec_u[1];
        END_IF;
        IF rVec_u[2] < 45.0 THEN
            rAntiSurgeValve_Stg2_Cmd_Out := 45.0;
        ELSE
            rAntiSurgeValve_Stg2_Cmd_Out := rVec_u[2];
        END_IF;
        IF rVec_u[3] < 45.0 THEN
            rAntiSurgeValve_Stg3_Cmd_Out := 45.0;
        ELSE
            rAntiSurgeValve_Stg3_Cmd_Out := rVec_u[3];
        END_IF;

        (* Lower VFD Speed Demand to conserve 60 MW drive electric power *)
        rVFD_Speed_Demand_Out := 8500.0;
        (* Interstage cooler bypass modulation to reject recycle compression heat *)
        rInterstageCooler1_Bypass_Out := 0.0; (* Full cooling across heat exchangers *)
        rInterstageCooler2_Bypass_Out := 0.0;

        (* If gas flow recovers above 80 mbar for > 30 seconds, return to normal MPC *)
        IF rVoted_SuctionDP_Out >= 80.0 THEN
            rFSM_SubTimer := rFSM_SubTimer + rTs;
            IF rFSM_SubTimer >= 30.0 THEN
                iFSM_State := 90;
            END_IF;
        ELSE
            rFSM_SubTimer := 0.0;
        END_IF;

        IF bCmd_Stop_In THEN
            iFSM_State := 120;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STAGE 110: STATE_WAVE_CHOKE_DAMPENING
     * Severe FPSO pitch/roll wave dynamics: Dampens export choke, advances surge line safety bias, prevents TEG carryover.
     * ----------------------------------------------------------------------------------------------------------------- *)
    110:
        (* Add dynamic surge bias directly to anti-surge valves *)
        rAntiSurgeValve_Stg1_Cmd_Out := rVec_u[1] + (rDynamicSurgeBias_Wave * 100.0);
        rAntiSurgeValve_Stg2_Cmd_Out := rVec_u[2] + (rDynamicSurgeBias_Wave * 100.0);
        rAntiSurgeValve_Stg3_Cmd_Out := rVec_u[3] + (rDynamicSurgeBias_Wave * 100.0);
        IF rAntiSurgeValve_Stg1_Cmd_Out > 100.0 THEN rAntiSurgeValve_Stg1_Cmd_Out := 100.0; END_IF;
        IF rAntiSurgeValve_Stg2_Cmd_Out > 100.0 THEN rAntiSurgeValve_Stg2_Cmd_Out := 100.0; END_IF;
        IF rAntiSurgeValve_Stg3_Cmd_Out > 100.0 THEN rAntiSurgeValve_Stg3_Cmd_Out := 100.0; END_IF;

        rVFD_Speed_Demand_Out := 9400.0;
        (* Slightly throttle export choke to 75% to dampen marine riser slugging *)
        rExportChoke_Cmd_Out := 75.0;
        (* Derate TEG Glycol circulation by 15% to mitigate column tray foaming *)
        rTEG_Pump_Speed_Cmd_Out := 60.0;

        (* When vessel motions settle below 3.0° and heave < 1.0 m/s2 for > 45s, return to normal MPC *)
        IF (rVessel_TiltAngle <= 3.00) AND (ABS(rFPSO_HeaveAccel_In) <= 1.00) THEN
            rFSM_SubTimer := rFSM_SubTimer + rTs;
            IF rFSM_SubTimer >= 45.0 THEN
                iFSM_State := 90;
            END_IF;
        ELSE
            rFSM_SubTimer := 0.0;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STAGE 120: STATE_DERATE_HOT_RECYCLE_IDLE
     * Controlled ramp down to idle hot recycle: Decouples export pipeline while maintaining warm standby for fast re-start.
     * ----------------------------------------------------------------------------------------------------------------- *)
    120:
        bSystem_Ready_Out := FALSE;
        (* Ramp export choke closed over 25 seconds *)
        rExportChoke_Cmd_Out := 100.0 - ((rFSM_StateTimer / 25.0) * 100.0);
        IF rExportChoke_Cmd_Out < 0.0 THEN
            rExportChoke_Cmd_Out := 0.0;
        END_IF;

        (* Ramp ASVs open to 85% hot recycle *)
        rAntiSurgeValve_Stg1_Cmd_Out := 85.0;
        rAntiSurgeValve_Stg2_Cmd_Out := 85.0;
        rAntiSurgeValve_Stg3_Cmd_Out := 85.0;

        (* Derate VFD speed to 6,200 rpm idle *)
        rVFD_Speed_Demand_Out := 9800.0 - ((rFSM_StateTimer / 25.0) * 3600.0);
        IF rVFD_Speed_Demand_Out < 6200.0 THEN
            rVFD_Speed_Demand_Out := 6200.0;
        END_IF;

        rTEG_Pump_Speed_Cmd_Out := 35.0;
        rTEG_Reboiler_Duty_Cmd_Out := 45.0;

        (* Re-start permissive or manual safe shutdown transition *)
        IF bCmd_Start_In THEN
            iFSM_State := 60; (* Ramp back up to full compression *)
        ELSIF rFSM_StateTimer >= 180.0 THEN
            iFSM_State := 140; (* Automatic timeout to mechanical safe trip *)
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STAGE 130: STATE_SIL3_EMERGENCY_DEPRESS
     * Safety Instrumented System (SIS) SIL-3 Fast Emergency Depressurization (EDP) to High-Pressure Flare per API 521.
     * ----------------------------------------------------------------------------------------------------------------- *)
    130:
        bEDP_Active := TRUE;
        bSystem_Ready_Out := FALSE;
        bSystem_Trip_Latched_Out := TRUE;

        (* Fast Hardware Interlock Shutdowns *)
        bVFD_EmergencyTrip_Out := TRUE;        (* Kill 60 MW Drive Motor VFD *)
        rVFD_Speed_Demand_Out := 0.0;
        bInfeed_Isolation_Close_Out := TRUE;   (* Slam Upstream Suction ESD Valve Closed *)
        bExport_Isolation_Close_Out := TRUE;   (* Slam Subsea Export Pipeline ESD Valve Closed *)
        rSuctionChoke_Cmd_Out := 0.0;
        rExportChoke_Cmd_Out := 0.0;

        (* Open All Anti-Surge Valves 100% Instantly to Equalize Multi-Stage Pressures *)
        rAntiSurgeValve_Stg1_Cmd_Out := 100.0;
        rAntiSurgeValve_Stg2_Cmd_Out := 100.0;
        rAntiSurgeValve_Stg3_Cmd_Out := 100.0;

        (* Open SIL-3 High-Pressure Flare Blowdown Valve and LP Flare Scrubber Valve *)
        bEDP_HP_FlareValve_Open_Out := TRUE;
        bEDP_LP_FlareValve_Open_Out := TRUE;

        (* Shutdown TEG Glycol Circulation & Heaters *)
        rTEG_Pump_Speed_Cmd_Out := 0.0;
        rTEG_Reboiler_Duty_Cmd_Out := 0.0;
        rTEG_StrippingGas_Cmd_Out := 0.0;

        (* Ensure Auxiliary Lube Oil Skid Operates During Compressor Rotor Coastdown *)
        bLubeOil_AuxPump_Start_Out := TRUE;

        rEDP_RampTimer := rEDP_RampTimer + rTs;

        (* API 521 Depressurization Compliance: Train pressure reduced to < 6.9 bar within 15 minutes (900s) *)
        IF (rVoted_DischargePres_Out <= 6.50) OR (rEDP_RampTimer >= 900.0) THEN
            iFSM_State := 140; (* Transition to Mechanical Safe Standstill *)
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STAGE 140: STATE_SAFE_MECHANICAL_TRIP
     * Mechanical safe standstill, lube oil rundown tank supervision, nitrogen post-purge, and latched reset wait.
     * ----------------------------------------------------------------------------------------------------------------- *)
    140:
        bSystem_Ready_Out := FALSE;
        bSystem_Trip_Latched_Out := TRUE;
        bVFD_EmergencyTrip_Out := TRUE;
        rVFD_Speed_Demand_Out := 0.0;
        rSuctionChoke_Cmd_Out := 0.0;
        rExportChoke_Cmd_Out := 0.0;
        bInfeed_Isolation_Close_Out := TRUE;
        bExport_Isolation_Close_Out := TRUE;

        (* Fail-safe valve positions *)
        rAntiSurgeValve_Stg1_Cmd_Out := 100.0;
        rAntiSurgeValve_Stg2_Cmd_Out := 100.0;
        rAntiSurgeValve_Stg3_Cmd_Out := 100.0;

        (* Keep flare valves open until residual pressure drops below 1.5 bar, then close to prevent air ingress *)
        IF rVoted_DischargePres_Out > 1.50 THEN
            bEDP_HP_FlareValve_Open_Out := TRUE;
            bEDP_LP_FlareValve_Open_Out := TRUE;
        ELSE
            bEDP_HP_FlareValve_Open_Out := FALSE;
            bEDP_LP_FlareValve_Open_Out := FALSE;
        END_IF;

        (* Auxiliary Lube Oil Pump runs for 300 seconds of coastdown, then de-energizes *)
        IF rFSM_StateTimer < 300.0 THEN
            bLubeOil_AuxPump_Start_Out := TRUE;
        ELSE
            bLubeOil_AuxPump_Start_Out := FALSE;
        END_IF;

        (* Operator Reset Permissive: All critical process trips cleared and explicit reset command pulse *)
        IF bCmd_Reset_In AND (NOT bTrip_EmergencyDepress_Manual) AND
           (NOT bTrip_SuctionPres_HH) AND (NOT bTrip_DischargePres_HH) AND
           (NOT bTrip_ShaftVibration_HH) AND (NOT bTrip_LubeOil_LL) AND
           (NOT bTrip_SealGas_LL) AND (NOT bTrip_Reboiler_HH) AND (NOT bTrip_TMR_CriticalLoss) THEN
            bSystem_Trip_Latched_Out := FALSE;
            bEDP_Active := FALSE;
            rEDP_RampTimer := 0.0;
            iFSM_State := 10; (* Reset sequence back to Stage 10 *)
        END_IF;

END_CASE;
"""
