# fccu_builder/part5_phase4_fsm_logic.py

def get_part5_phase4_fsm_logic():
    lines = []
    lines.append("""(*
========================================================================================================================
  PHASE 4: 14-STAGE DETERMINISTIC REFINERY PRODUCTION & EMERGENCY QUENCH FINITE STATE MACHINE (FSM)
========================================================================================================================
*)
(* Update State Timer and Detect State Transitions *)
IF eState <> eState_Previous THEN
    rStateTimer_sec := 0.0;
    eState_Previous := eState;
ELSE
    rStateTimer_sec := rStateTimer_sec + rTs_sec;
END_IF;

(* Master Deterministic State Machine Execution *)
CASE eState OF
    (* -----------------------------------------------------------------------------------------------------------------
       STATE 0: COLD_REFRACTORY_DRYOUT_STANDBY
       - Unit is cold or refractory curing mode. Catalyst is slumped in regenerator/reactor.
       - Slide valves hydraulically locked closed (0.0%). Feed cutoff closed (0.0%).
       - Minimum air purge (12%) through air blower to prevent combustor flammability pockets.
       - Lift steam on low warming rate (15 t/h) to maintain line temperature and prevent condensables.
       - Flue gas slide valve open (45%) to establish natural draft through orifice chamber.
       ----------------------------------------------------------------------------------------------------------------- *)
    0:
        bSystemReady            := FALSE;
        bProductionActive       := FALSE;
        bEmergencyTripActive    := FALSE;
        bAntiReversalLockActive := FALSE;
        bAfterburnQuenchActive  := FALSE;
        bBlowerSurgeAlert       := FALSE;
        bTorchOilActive         := FALSE;
        bStateStepPermissive    := FALSE;

        rActuator_RCSV_Target_pct         := 0.0;
        rActuator_SCSV_Target_pct         := 0.0;
        rActuator_AirBlower_Target_pct    := 12.0;
        rActuator_TorchOil_Target_pct     := 0.0;
        rActuator_LiftSteam_Target_pct    := 20.0;
        rActuator_FlueGasValve_Target_pct := 45.0;
        rActuator_QuenchWater_Target_pct  := 0.0;
        rActuator_FeedCutoff_Target_pct   := 0.0;

        rStageRampFeed_th                 := 0.0;
        rStageRampAir_kgs                 := 12.5;
        rStageRampSteam_th                := 15.0;
        rTorchOilCombustionRate_kgh       := 0.0;

        (* Transition Criteria to State 1: AIR_PREHEATER_AND_BLOWER_STARTUP *)
        IF bSystemEnable AND NOT bEmergencyStop AND bSlideValveHydraulicOk AND (rStateTimer_sec >= 5.0) THEN
            bStateStepPermissive := TRUE;
            eState := 1;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
       STATE 1: AIR_PREHEATER_AND_BLOWER_STARTUP
       - Start direct-fired air preheater and ramp main air blower to establish minimal fluidization velocity.
       - Riser lift steam maintained at 25 t/h to purge reactor disengager cyclones.
       - Slide valves held locked closed (0.0%).
       - Blower discharge pressure must establish positive pressure gradient over atmosphere.
       ----------------------------------------------------------------------------------------------------------------- *)
    1:
        bSystemReady            := FALSE;
        bProductionActive       := FALSE;
        bEmergencyTripActive    := FALSE;
        bAntiReversalLockActive := FALSE;
        bAfterburnQuenchActive  := FALSE;
        bBlowerSurgeAlert       := FALSE;
        bTorchOilActive         := FALSE;
        bStateStepPermissive    := FALSE;

        (* Ramp air flow up to 35.0 kg/s *)
        IF rStageRampAir_kgs < 35.0 THEN
            rStageRampAir_kgs := rStageRampAir_kgs + (0.5 * rTs_sec);
        END_IF;

        rActuator_RCSV_Target_pct         := 0.0;
        rActuator_SCSV_Target_pct         := 0.0;
        rActuator_AirBlower_Target_pct    := (rStageRampAir_kgs / 90.0) * 100.0;
        rActuator_TorchOil_Target_pct     := 0.0;
        rActuator_LiftSteam_Target_pct    := 28.0;
        rActuator_FlueGasValve_Target_pct := 50.0;
        rActuator_QuenchWater_Target_pct  := 0.0;
        rActuator_FeedCutoff_Target_pct   := 0.0;

        (* Emergency Abort Check *)
        IF bEmergencyStop OR bAirBlowerTripFeedback THEN
            eState := 13;
        (* Transition Criteria to State 2: Bed preheated and blower air flow established *)
        ELSIF (rFT_COMBUSTION_AIR_kgs >= 32.0) AND (rPT_AIR_BLAST_kPa >= 140.0) AND bTorchOilPermissive AND (rStateTimer_sec >= 15.0) THEN
            bStateStepPermissive := TRUE;
            eState := 2;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
       STATE 2: TORCH_OIL_CATALYST_BED_LIGHTOFF (>370 deg C)
       - Regenerator dense bed must reach auto-ignition temperature (>370 deg C) before direct torch oil firing.
       - Auxiliary torch oil burners engaged to raise bed temperature up to 550 - 620 deg C.
       - Air blower modulated to provide stoichiometric combustion air with excess O2 buffer (3.0 - 5.0% O2).
       - Lift steam active to prevent condensation in riser line.
       ----------------------------------------------------------------------------------------------------------------- *)
    2:
        bSystemReady            := FALSE;
        bProductionActive       := FALSE;
        bEmergencyTripActive    := FALSE;
        bAntiReversalLockActive := FALSE;
        bAfterburnQuenchActive  := FALSE;
        bBlowerSurgeAlert       := FALSE;
        bTorchOilActive         := TRUE;
        bStateStepPermissive    := FALSE;

        (* Modulate Torch Oil Flow up to 2500 kg/h based on bed temperature trajectory *)
        IF rVoted_RegenBedTemp_degC < 400.0 THEN
            rTorchOilCombustionRate_kgh := 1200.0;
        ELSIF rVoted_RegenBedTemp_degC < 550.0 THEN
            rTorchOilCombustionRate_kgh := 2200.0;
        ELSE
            rTorchOilCombustionRate_kgh := 1600.0;
        END_IF;

        IF rStageRampAir_kgs < 52.0 THEN
            rStageRampAir_kgs := rStageRampAir_kgs + (0.35 * rTs_sec);
        END_IF;

        rActuator_RCSV_Target_pct         := 0.0;
        rActuator_SCSV_Target_pct         := 0.0;
        rActuator_AirBlower_Target_pct    := (rStageRampAir_kgs / 90.0) * 100.0;
        rActuator_TorchOil_Target_pct     := (rTorchOilCombustionRate_kgh / 3500.0) * 100.0;
        rActuator_LiftSteam_Target_pct    := 32.0;
        rActuator_FlueGasValve_Target_pct := 55.0;
        rActuator_QuenchWater_Target_pct  := 0.0;
        rActuator_FeedCutoff_Target_pct   := 0.0;

        (* Safety Trips *)
        IF bEmergencyStop OR NOT bTorchOilPermissive OR bAirBlowerTripFeedback THEN
            eState := 13;
        (* Transition Criteria to State 3: Bed temperature reaches 580 deg C with good combustion *)
        ELSIF (rVoted_RegenBedTemp_degC >= 580.0) AND (rVoted_FlueGasO2_pct >= 1.2) AND (rStateTimer_sec >= 30.0) THEN
            bStateStepPermissive := TRUE;
            eState := 3;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
       STATE 3: REGENERATOR_CATALYST_INVENTORY_FLUIDIZATION
       - Full catalyst inventory fluidization in Stage 1 and Stage 2 regenerator vessels.
       - Thermal soaking of refractory lining and catalyst inventory to 680 - 710 deg C.
       - Standpipe aeration activated to establish hydrostatic head for slide valve differential pressure seal.
       ----------------------------------------------------------------------------------------------------------------- *)
    3:
        bSystemReady            := FALSE;
        bProductionActive       := FALSE;
        bEmergencyTripActive    := FALSE;
        bAntiReversalLockActive := FALSE;
        bAfterburnQuenchActive  := FALSE;
        bBlowerSurgeAlert       := FALSE;
        bTorchOilActive         := TRUE;
        bStateStepPermissive    := FALSE;

        (* Bring bed to thermal equilibrium *)
        IF rVoted_RegenBedTemp_degC < 680.0 THEN
            rTorchOilCombustionRate_kgh := 1800.0;
        ELSE
            rTorchOilCombustionRate_kgh := 800.0;
        END_IF;

        IF rStageRampAir_kgs < 68.0 THEN
            rStageRampAir_kgs := rStageRampAir_kgs + (0.4 * rTs_sec);
        END_IF;

        rActuator_RCSV_Target_pct         := 0.0;
        rActuator_SCSV_Target_pct         := 0.0;
        rActuator_AirBlower_Target_pct    := (rStageRampAir_kgs / 90.0) * 100.0;
        rActuator_TorchOil_Target_pct     := (rTorchOilCombustionRate_kgh / 3500.0) * 100.0;
        rActuator_LiftSteam_Target_pct    := 38.0;
        rActuator_FlueGasValve_Target_pct := 60.0;
        rActuator_QuenchWater_Target_pct  := 0.0;
        rActuator_FeedCutoff_Target_pct   := 0.0;

        IF bEmergencyStop OR bAirBlowerTripFeedback THEN
            eState := 13;
        (* Transition Criteria to State 4: Dense bed >= 675 deg C, fluid bed levels established *)
        ELSIF (rVoted_RegenBedTemp_degC >= 675.0) AND (rLT_REGEN_STAGE1_m >= 3.5) AND (rStateTimer_sec >= 45.0) THEN
            bStateStepPermissive := TRUE;
            eState := 4;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
       STATE 4: SLIDE_VALVE_HYDRAULIC_DP_PRESSURE_LOCK (dP > 35 kPa)
       - CRITICAL PRESSURE SEAL STAGE: Catalyst circulation is strictly forbidden until both RCSV and SCSV
         demonstrate differential pressure exceeding 35.0 kPa.
       - Regenerator vessel backpressure is modulated via Flue Gas Slide Valve to build differential pressure.
       - Slide valves cracked open slightly (4..6%) under tight position control to confirm mechanical readiness.
       ----------------------------------------------------------------------------------------------------------------- *)
    4:
        bSystemReady            := FALSE;
        bProductionActive       := FALSE;
        bEmergencyTripActive    := FALSE;
        bAntiReversalLockActive := FALSE;
        bAfterburnQuenchActive  := FALSE;
        bBlowerSurgeAlert       := FALSE;
        bTorchOilActive         := TRUE;
        bStateStepPermissive    := FALSE;

        (* Maintain regenerator pressure seal *)
        rActuator_RCSV_Target_pct         := 5.0;
        rActuator_SCSV_Target_pct         := 5.0;
        rActuator_AirBlower_Target_pct    := (rStageRampAir_kgs / 90.0) * 100.0;
        rActuator_TorchOil_Target_pct     := 15.0;
        rActuator_LiftSteam_Target_pct    := 45.0;
        rActuator_FlueGasValve_Target_pct := 58.0;
        rActuator_QuenchWater_Target_pct  := 0.0;
        rActuator_FeedCutoff_Target_pct   := 0.0;

        IF bEmergencyStop THEN
            eState := 13;
        (* Reverse Flow Danger check *)
        ELSIF (rVoted_SCSV_dP_kPa < 20.0) OR (rVoted_RCSV_dP_kPa < 20.0) THEN
            eState := 10;
        (* Transition Criteria to State 5: Both slide valves exhibit solid dP >= 38.0 kPa *)
        ELSIF (rVoted_SCSV_dP_kPa >= 38.0) AND (rVoted_RCSV_dP_kPa >= 38.0) AND (rStateTimer_sec >= 20.0) THEN
            bStateStepPermissive := TRUE;
            eState := 5;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
       STATE 5: RISER_LIFT_STEAM_THERMAL_EQUILIBRIUM
       - Establish hot catalyst circulation loop under pure lift steam before introducing hydrocarbon oil.
       - RCSV opened to 15..25% to circulate 700 deg C regenerated solids into the riser.
       - SCSV modulated to return spent catalyst from stripper to regenerator, stabilizing stripper level.
       - Riser outlet temperature preheated to 495 - 515 deg C to prevent cold oil condensation/coking.
       ----------------------------------------------------------------------------------------------------------------- *)
    5:
        bSystemReady            := TRUE;
        bProductionActive       := FALSE;
        bEmergencyTripActive    := FALSE;
        bAntiReversalLockActive := FALSE;
        bAfterburnQuenchActive  := FALSE;
        bBlowerSurgeAlert       := FALSE;
        bTorchOilActive         := TRUE;
        bStateStepPermissive    := FALSE;

        rActuator_RCSV_Target_pct         := 22.0;
        rActuator_SCSV_Target_pct         := 20.0;
        rActuator_AirBlower_Target_pct    := 72.0;
        rActuator_TorchOil_Target_pct     := 10.0;
        rActuator_LiftSteam_Target_pct    := 55.0;
        rActuator_FlueGasValve_Target_pct := 62.0;
        rActuator_QuenchWater_Target_pct  := 0.0;
        rActuator_FeedCutoff_Target_pct   := 0.0;

        IF bEmergencyStop THEN
            eState := 13;
        ELSIF (rVoted_SCSV_dP_kPa < 25.0) OR (rVoted_RCSV_dP_kPa < 25.0) THEN
            eState := 10;
        (* Transition Criteria to State 6: Riser warmed to > 505 deg C, slide valve dP >= 40 kPa, feed permissive *)
        ELSIF (rVoted_RiserTemp_degC >= 505.0) AND (rVoted_SCSV_dP_kPa >= 40.0) AND (rVoted_RCSV_dP_kPa >= 40.0) AND bFeedCutPermissive AND (rStateTimer_sec >= 30.0) THEN
            bStateStepPermissive := TRUE;
            eState := 6;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
       STATE 6: GASOIL_FEED_INJECTION_RAMPUP (Bumpless Cut-in)
       - Main hydrocarbon feed emergency cutoff valve opened (100.0%).
       - Gasoil feed ramped smoothly from 15.0 t/h to target throughput (160..210 t/h) at 1.8 t/h per second.
       - RCSV modulated simultaneously to supply endothermic reaction heat, maintaining riser temp at setpoint (528 deg C).
       - Torch oil throttled back as coke on spent catalyst replaces torch oil as primary regenerator fuel.
       - Feed atomization dispersion steam active.
       ----------------------------------------------------------------------------------------------------------------- *)
    6:
        bSystemReady            := TRUE;
        bProductionActive       := FALSE;
        bEmergencyTripActive    := FALSE;
        bAntiReversalLockActive := FALSE;
        bAfterburnQuenchActive  := FALSE;
        bBlowerSurgeAlert       := FALSE;
        bTorchOilActive         := FALSE;
        bStateStepPermissive    := FALSE;

        (* Feed Flow Ramp Calculation *)
        IF rStageRampFeed_th < rTargetFeedRate_th THEN
            rStageRampFeed_th := rStageRampFeed_th + (1.8 * rTs_sec);
            IF rStageRampFeed_th > rTargetFeedRate_th THEN
                rStageRampFeed_th := rTargetFeedRate_th;
            END_IF;
        END_IF;

        (* Coordinate RCSV target with feed ramp *)
        rActuator_RCSV_Target_pct         := 22.0 + ((rStageRampFeed_th / 200.0) * 32.0);
        rActuator_SCSV_Target_pct         := 20.0 + ((rStageRampFeed_th / 200.0) * 30.0);
        rActuator_AirBlower_Target_pct    := 75.0 + ((rStageRampFeed_th / 200.0) * 15.0);
        rActuator_TorchOil_Target_pct     := 0.0; (* Torch oil cut off once feed cracking starts *)
        rActuator_LiftSteam_Target_pct    := 60.0;
        rActuator_FlueGasValve_Target_pct := 65.0;
        rActuator_QuenchWater_Target_pct  := 0.0;
        rActuator_FeedCutoff_Target_pct   := 100.0;

        IF bEmergencyStop THEN
            eState := 13;
        ELSIF (rVoted_SCSV_dP_kPa < 25.0) OR (rVoted_RCSV_dP_kPa < 25.0) THEN
            eState := 10;
        ELSIF NOT bFeedCutPermissive THEN
            eState := 11;
        (* Transition Criteria to State 7: Feed reaches >= 88% of target, riser temp stable within +/- 6 deg C *)
        ELSIF (rStageRampFeed_th >= (rTargetFeedRate_th * 0.88)) AND (ABS(rVoted_RiserTemp_degC - x_sp[1]) <= 6.0) AND (rStateTimer_sec >= 45.0) THEN
            bStateStepPermissive := TRUE;
            eState := 7;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
       STATE 7: FULL_CRACKING_OPTIMAL_MPC_COUPLED_RUN
       - FULL PRODUCTION STEADY STATE: Receding-Horizon Model Predictive Control (MPC) actively dictates all
         manipulated actuator commands (u_opt[1..6]).
       - Continuous decoupling of slide valve differential pressures (strictly held in 38..65 kPa window).
       - Real-time heat balance optimization between endothermic cracking and exothermic coke burn.
       ----------------------------------------------------------------------------------------------------------------- *)
    7:
        bSystemReady            := TRUE;
        bProductionActive       := TRUE;
        bEmergencyTripActive    := FALSE;
        bAntiReversalLockActive := FALSE;
        bAfterburnQuenchActive  := FALSE;
        bBlowerSurgeAlert       := FALSE;
        bTorchOilActive         := FALSE;
        bStateStepPermissive    := TRUE;

        (* Actuators Driven by Receding-Horizon MPC Optimization *)
        rActuator_RCSV_Target_pct         := u_opt[1];
        rActuator_SCSV_Target_pct         := u_opt[2];
        rActuator_AirBlower_Target_pct    := u_opt[3];
        rActuator_TorchOil_Target_pct     := 0.0; (* 100% self-sustaining coke combustion *)
        rActuator_LiftSteam_Target_pct    := u_opt[5];
        rActuator_FlueGasValve_Target_pct := u_opt[6];
        rActuator_QuenchWater_Target_pct  := 0.0;
        rActuator_FeedCutoff_Target_pct   := 100.0;

        (* Dynamic Transitions & Emergency Interlocks *)
        IF bEmergencyStop THEN
            eState := 13;
        (* Reverse Flow Hydraulic Lock Trip (< 22 kPa) *)
        ELSIF (rVoted_SCSV_dP_kPa < 22.0) OR (rVoted_RCSV_dP_kPa < 22.0) THEN
            eState := 10;
        (* Loss of Feed Permissive Trip *)
        ELSIF NOT bFeedCutPermissive THEN
            eState := 11;
        (* Severe Regenerator Dilute Phase Afterburn (> 25 deg C Delta-T) *)
        ELSIF rAfterburnDeltaT_degC > 25.0 THEN
            eState := 12;
        (* Blower Surge Alert Trigger *)
        ELSIF (rPT_AIR_BLAST_kPa > 210.0) AND (rFT_COMBUSTION_AIR_kgs < 55.0) THEN
            eState := 9;
        (* Operator Request for Heavy Slurry Recycle Mode *)
        ELSIF (rFT_OIL_FEED_th > 180.0) AND (rDensity_Feed_kgm3 > 940.0) THEN
            eState := 8;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
       STATE 8: HEAVY_SLURRY_RECYCLE_MAXIMIZATION
       - Heavy clarified slurry oil (CSO / decant oil) recycled to bottom of riser to maximize gasoline yield.
       - High CCR (Conradson Carbon Residue) increases coke production; MPC adjusts air blower to maintain excess O2.
       - Slide valve DP balance carefully monitored under high solid circulation rates.
       ----------------------------------------------------------------------------------------------------------------- *)
    8:
        bSystemReady            := TRUE;
        bProductionActive       := TRUE;
        bEmergencyTripActive    := FALSE;
        bAntiReversalLockActive := FALSE;
        bAfterburnQuenchActive  := FALSE;
        bBlowerSurgeAlert       := FALSE;
        bTorchOilActive         := FALSE;
        bStateStepPermissive    := TRUE;

        (* MPC continues to govern with adjusted air bias *)
        rActuator_RCSV_Target_pct         := u_opt[1];
        rActuator_SCSV_Target_pct         := u_opt[2];
        rActuator_AirBlower_Target_pct    := u_opt[3] + 2.5; (* Air boost for increased coke burn *)
        rActuator_TorchOil_Target_pct     := 0.0;
        rActuator_LiftSteam_Target_pct    := u_opt[5];
        rActuator_FlueGasValve_Target_pct := u_opt[6];
        rActuator_QuenchWater_Target_pct  := 0.0;
        rActuator_FeedCutoff_Target_pct   := 100.0;

        IF bEmergencyStop THEN
            eState := 13;
        ELSIF (rVoted_SCSV_dP_kPa < 22.0) OR (rVoted_RCSV_dP_kPa < 22.0) THEN
            eState := 10;
        ELSIF NOT bFeedCutPermissive THEN
            eState := 11;
        ELSIF rAfterburnDeltaT_degC > 25.0 THEN
            eState := 12;
        (* Return to Standard Cracking Mode if feed density normalizes *)
        ELSIF rDensity_Feed_kgm3 <= 930.0 THEN
            eState := 7;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
       STATE 9: AIR_BLOWER_SURGE_OR_O2_ENRICHMENT_CONTROL
       - Main air blower operates near aerodynamic surge limit or requiring O2 enrichment decoupling.
       - Anti-surge recirculation valve modulated, blower guide vanes adjusted to move operating point safely away
         from surge parabolic line while maintaining minimum dense bed fluidization.
       ----------------------------------------------------------------------------------------------------------------- *)
    9:
        bSystemReady            := TRUE;
        bProductionActive       := TRUE;
        bEmergencyTripActive    := FALSE;
        bAntiReversalLockActive := FALSE;
        bAfterburnQuenchActive  := FALSE;
        bBlowerSurgeAlert       := TRUE;
        bTorchOilActive         := FALSE;
        bStateStepPermissive    := FALSE;

        rActuator_RCSV_Target_pct         := u_opt[1];
        rActuator_SCSV_Target_pct         := u_opt[2];
        rActuator_AirBlower_Target_pct    := 82.0; (* Locked safe throttle *)
        rActuator_TorchOil_Target_pct     := 0.0;
        rActuator_LiftSteam_Target_pct    := u_opt[5];
        rActuator_FlueGasValve_Target_pct := u_opt[6] + 3.0; (* Relieve regenerator backpressure *)
        rActuator_QuenchWater_Target_pct  := 0.0;
        rActuator_FeedCutoff_Target_pct   := 100.0;

        IF bEmergencyStop THEN
            eState := 13;
        ELSIF (rVoted_SCSV_dP_kPa < 22.0) OR (rVoted_RCSV_dP_kPa < 22.0) THEN
            eState := 10;
        (* Return to State 7 once surge conditions clear *)
        ELSIF (rPT_AIR_BLAST_kPa <= 195.0) AND (rFT_COMBUSTION_AIR_kgs >= 62.0) AND (rStateTimer_sec >= 20.0) THEN
            eState := 7;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
       STATE 10: SLIDE_VALVE_DP_REVERSAL_EMERGENCY_ISOLATION (<20 kPa)
       - CRITICAL SIL-3 ANTI-DEFLAGRATION FAST INTERLOCK ACTIVATED!
       - RCSV and SCSV fast closed (0.0%) within <50 ms to prevent catastrophic reverse flow of hydrocarbon gases
         into oxygen-rich regenerator vessel.
       - Fresh feed immediately tripped (0.0%). Riser lift steam boosted to 100.0% to sweep hydrocarbons forward.
       ----------------------------------------------------------------------------------------------------------------- *)
    10:
        bSystemReady            := FALSE;
        bProductionActive       := FALSE;
        bEmergencyTripActive    := TRUE;
        bAntiReversalLockActive := TRUE;
        bAfterburnQuenchActive  := FALSE;
        bBlowerSurgeAlert       := FALSE;
        bTorchOilActive         := FALSE;
        bStateStepPermissive    := FALSE;

        (* Instantaneous SIL-3 Trip Commands *)
        rActuator_RCSV_Target_pct         := 0.0;
        rActuator_SCSV_Target_pct         := 0.0;
        rActuator_AirBlower_Target_pct    := 50.0; (* Maintain fluid bed preservation air *)
        rActuator_TorchOil_Target_pct     := 0.0;
        rActuator_LiftSteam_Target_pct    := 100.0; (* Full blast steam sweep of riser *)
        rActuator_FlueGasValve_Target_pct := 55.0;
        rActuator_QuenchWater_Target_pct  := 0.0;
        rActuator_FeedCutoff_Target_pct   := 0.0;  (* Immediate Feed Isolation *)

        rStageRampFeed_th                 := 0.0;

        (* Latch first-out trip reason if not already latched *)
        IF dwFirstOutWord = 16#00000000 THEN
            dwFirstOutWord := 16#00000001; (* Code 1: Reverse DP Lock Trip *)
        END_IF;

        (* After steam sweep established, progress to State 11 for controlled recovery *)
        IF rStateTimer_sec >= 15.0 THEN
            eState := 11;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
       STATE 11: FEED_CUT_EMERGENCY_STRIPPING_STEAM_PURGE
       - Feed cut-in recovery and stripping steam sweep.
       - Hydrocarbon feed isolated (0.0%). Riser and stripper continuously swept with maximum steam to clear oil vapors.
       - Slide valves remain closed (0.0%). Regenerator bed kept hot under low air flow.
       ----------------------------------------------------------------------------------------------------------------- *)
    11:
        bSystemReady            := FALSE;
        bProductionActive       := FALSE;
        bEmergencyTripActive    := TRUE;
        bAntiReversalLockActive := FALSE;
        bAfterburnQuenchActive  := FALSE;
        bBlowerSurgeAlert       := FALSE;
        bTorchOilActive         := FALSE;
        bStateStepPermissive    := FALSE;

        rActuator_RCSV_Target_pct         := 0.0;
        rActuator_SCSV_Target_pct         := 0.0;
        rActuator_AirBlower_Target_pct    := 45.0;
        rActuator_TorchOil_Target_pct     := 0.0;
        rActuator_LiftSteam_Target_pct    := 80.0;
        rActuator_FlueGasValve_Target_pct := 55.0;
        rActuator_QuenchWater_Target_pct  := 0.0;
        rActuator_FeedCutoff_Target_pct   := 0.0;

        rStageRampFeed_th                 := 0.0;

        IF bEmergencyStop THEN
            eState := 13;
        (* Operator Reset and Permissive Clearance allows return to Pressure Lock State 4 *)
        ELSIF bAlarmReset AND NOT bEmergencyStop AND bFeedCutPermissive AND (rVoted_SCSV_dP_kPa >= 35.0) AND (rVoted_RCSV_dP_kPa >= 35.0) AND (rStateTimer_sec >= 60.0) THEN
            bEmergencyTripActive := FALSE;
            dwFirstOutWord := 16#00000000;
            eState := 4;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
       STATE 12: REGENERATOR_AFTERBURNING_THERMAL_RUNAWAY_QUENCH
       - Afterburning detected: CO combustion occurring in cyclone dilute phase (Delta-T > 25 deg C).
       - Cyclone quench water/steam deployed proportionally to protect cyclone barrels and refractory liners.
       - Combustion air blower guide vanes throttled back to reduce excess O2 available for dilute phase burn.
       ----------------------------------------------------------------------------------------------------------------- *)
    12:
        bSystemReady            := TRUE;
        bProductionActive       := TRUE;
        bEmergencyTripActive    := FALSE;
        bAntiReversalLockActive := FALSE;
        bAfterburnQuenchActive  := TRUE;
        bBlowerSurgeAlert       := FALSE;
        bTorchOilActive         := FALSE;
        bStateStepPermissive    := FALSE;

        (* Proportional quench water injection based on Afterburn Delta-T *)
        rActuator_QuenchWater_Target_pct := (rAfterburnDeltaT_degC - 20.0) * 4.5;
        IF rActuator_QuenchWater_Target_pct > 100.0 THEN
            rActuator_QuenchWater_Target_pct := 100.0;
        ELSIF rActuator_QuenchWater_Target_pct < 20.0 THEN
            rActuator_QuenchWater_Target_pct := 20.0;
        END_IF;

        rActuator_RCSV_Target_pct         := u_opt[1];
        rActuator_SCSV_Target_pct         := u_opt[2];
        rActuator_AirBlower_Target_pct    := u_opt[3] - 8.0; (* Reduce excess oxygen *)
        rActuator_TorchOil_Target_pct     := 0.0;
        rActuator_LiftSteam_Target_pct    := u_opt[5];
        rActuator_FlueGasValve_Target_pct := u_opt[6] + 4.0;
        rActuator_FeedCutoff_Target_pct   := 100.0;

        IF bEmergencyStop THEN
            eState := 13;
        ELSIF (rVoted_SCSV_dP_kPa < 22.0) OR (rVoted_RCSV_dP_kPa < 22.0) THEN
            eState := 10;
        (* Extreme thermal runaway HH: Cyclone temp > 790 deg C -> Feed cut *)
        ELSIF rTT_REGEN_CYCLONE_degC >= 790.0 THEN
            eState := 11;
        (* Recovery: Afterburning Delta-T cooled below 15 deg C *)
        ELSIF (rAfterburnDeltaT_degC <= 14.0) AND (rStateTimer_sec >= 30.0) THEN
            bAfterburnQuenchActive := FALSE;
            eState := 7;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
       STATE 13: EMERGENCY_CATALYST_DUMP_AND_SAFE_PARK
       - SIL-3 Comprehensive Plant Trip & Safe Parking State.
       - All hydrocarbon feed and fuel sources isolated immediately (0.0%).
       - Slide valves closed (0.0%). Quench water active if high temperatures exist.
       - Air blower throttled to minimal preservation purge (10.0%).
       ----------------------------------------------------------------------------------------------------------------- *)
    13:
        bSystemReady            := FALSE;
        bProductionActive       := FALSE;
        bEmergencyTripActive    := TRUE;
        bAntiReversalLockActive := FALSE;
        bAfterburnQuenchActive  := FALSE;
        bBlowerSurgeAlert       := FALSE;
        bTorchOilActive         := FALSE;
        bStateStepPermissive    := FALSE;

        rActuator_RCSV_Target_pct         := 0.0;
        rActuator_SCSV_Target_pct         := 0.0;
        rActuator_AirBlower_Target_pct    := 10.0;
        rActuator_TorchOil_Target_pct     := 0.0;
        rActuator_LiftSteam_Target_pct    := 25.0;
        rActuator_FlueGasValve_Target_pct := 50.0;
        rActuator_FeedCutoff_Target_pct   := 0.0;
        rStageRampFeed_th                 := 0.0;

        IF rTT_REGEN_CYCLONE_degC > 740.0 THEN
            rActuator_QuenchWater_Target_pct := 50.0;
        ELSE
            rActuator_QuenchWater_Target_pct := 0.0;
        END_IF;

        IF dwFirstOutWord = 16#00000000 THEN
            dwFirstOutWord := 16#00000002; (* Code 2: Master Emergency Stop Trip *)
        END_IF;

        (* Safe Park Exit: Manual Operator Reset and Permit Return to Standby *)
        IF bAlarmReset AND NOT bEmergencyStop AND (rStateTimer_sec >= 60.0) THEN
            bEmergencyTripActive := FALSE;
            dwFirstOutWord := 16#00000000;
            eState := 0;
        END_IF;

    ELSE
        (* Trap Invalid States Safely to Safe Park *)
        eState := 13;
END_CASE;
""")
    return "\n".join(lines)
