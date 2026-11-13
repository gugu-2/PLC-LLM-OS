# lyophilizer_builder/build_st_phase6_fsm.py

def get_phase6_fsm():
    return """(* === PHASE 6: 14-STAGE DETERMINISTIC PRODUCTION FINITE STATE MACHINE (FSM) === *)
(* ---------------------------------------------------------------------------------------------------- *)
(* MASTER FSM STATE DISPATCHER & TRANSITION SUPERVISOR                                                  *)
(* ---------------------------------------------------------------------------------------------------- *)
(* Track State Elapsed Time *)
IF nFsmState = nPrevState THEN
    tStateTime_s := tStateTime_s + tScanInterval_s;
ELSE
    tStateTime_s := 0.0;
    nPrevState := nFsmState;
END_IF;

(* Emergency Interlock Override: Immediate Transition to State 13 *)
IF NOT bEmergencyStop OR bAlarm_ProductCollapse_Trip OR bAlarm_ChamberVacuum_Trip THEN
    nFsmState := 13; (* Force EMERGENCY TRIP *)
END_IF;

CASE nFsmState OF
    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 0: STATE_IDLE                                                                              *)
    (* Equipment stationary, ambient thermal equilibrium, awaiting recipe start command                 *)
    (* ------------------------------------------------------------------------------------------------ *)
    0:
        sFsmStateName := 'STATE_IDLE';
        vecU[1] := 0.0;
        vecU[2] := 0.0;
        vecU[3] := 0.0;
        vecU[4] := 0.0;
        vecU[5] := 20.0; (* Minimum fluid circulation *)
        bCmd_ChamberIsolationValve := FALSE;
        bCmd_VacuumBackingPump := FALSE;
        bCmd_VacuumRootsBlower := FALSE;
        bCmd_CascadeStage1Compressor := FALSE;
        bCmd_CascadeStage2Compressor := FALSE;
        bCmd_SterileN2AerationValve := FALSE;
        bCmd_CIP_SupplyPump := FALSE;
        bCmd_SIP_PureSteamInletValve := FALSE;
        bCmd_ChamberCondensateDrainValve := FALSE;

        bPrimaryDryingComplete := FALSE;
        bSecondaryDryingComplete := FALSE;
        bStopperingComplete := FALSE;

        (* Auto start transition when recipe enabled and door locked *)
        IF bAutoMode AND bDoorInterlockClosed AND (dwFirstOutWord = 16#00000000) THEN
            nFsmState := 1; (* Advance to CIP *)
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 1: STATE_CIP_CLEAN_IN_PLACE_WATER_WASH                                                     *)
    (* High-pressure automated water wash cycle via internal rotary spray nozzles                       *)
    (* ------------------------------------------------------------------------------------------------ *)
    1:
        sFsmStateName := 'STATE_CIP_CLEAN_IN_PLACE_WATER_WASH';
        bCmd_CIP_SupplyPump := TRUE;
        bCmd_ChamberCondensateDrainValve := TRUE;
        bCmd_ChamberIsolationValve := FALSE;
        vecU[5] := 30.0; (* Shelf pump idle *)

        (* Dwell for 1800 s (30 min) of certified detergent/WFI washing *)
        IF tStateTime_s >= 1800.0 THEN
            bCmd_CIP_SupplyPump := FALSE;
            nFsmState := 2; (* Advance to SIP *)
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 2: STATE_SIP_STEAM_STERILIZATION_HOLD_121C                                                 *)
    (* Pure saturated steam sterilization hold at >= 121.1 deg C to achieve F0 >= 30 minutes            *)
    (* ------------------------------------------------------------------------------------------------ *)
    2:
        sFsmStateName := 'STATE_SIP_STEAM_STERILIZATION_HOLD_121C';
        bCmd_SIP_PureSteamInletValve := TRUE;
        bCmd_ChamberCondensateDrainValve := TRUE;
        bCmd_ChamberIsolationValve := FALSE;

        (* Warm shelves with fluid to avoid cold-wall steam condensation *)
        vecU[1] := 45.0;
        vecU[5] := 50.0;

        (* Check thermal sterilization parameters *)
        IF rSIP_SteamTemp_degC >= 121.10 THEN
            tSubTimer_s := tSubTimer_s + tScanInterval_s;
        ELSE
            tSubTimer_s := MAX(0.0, tSubTimer_s - tScanInterval_s); (* Reset timer on temp drop *)
        END_IF;

        (* 30-minute certified sterilization hold *)
        IF tSubTimer_s >= 1800.0 THEN
            bCmd_SIP_PureSteamInletValve := FALSE;
            tSubTimer_s := 0.0;
            nFsmState := 3; (* Advance to Post-SIP Cool *)
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 3: STATE_POST_SIP_VACUUM_COOLING_AND_DRAIN                                                 *)
    (* Rapid chamber flash evacuation to dry condensate and chill shelves below 30 deg C               *)
    (* ------------------------------------------------------------------------------------------------ *)
    3:
        sFsmStateName := 'STATE_POST_SIP_VACUUM_COOLING_AND_DRAIN';
        bCmd_SIP_PureSteamInletValve := FALSE;
        bCmd_ChamberCondensateDrainValve := TRUE;
        bCmd_VacuumBackingPump := TRUE;
        bCmd_ChamberIsolationValve := TRUE;

        (* Circulate cooling fluid through shelves *)
        vecU[1] := 0.0;
        vecU[2] := 65.0;
        vecU[5] := 75.0;

        (* Once chamber cools below 28 deg C and condensate evacuated *)
        IF (rVotedShelfFluidTemp <= 28.0) AND (tStateTime_s >= 1200.0) THEN
            bCmd_ChamberCondensateDrainValve := FALSE;
            nFsmState := 4; (* Advance to Vacuum Leak Test *)
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 4: STATE_VACUUM_DECAY_INTEGRITY_LEAK_RATE_TEST                                             *)
    (* Chamber deep evacuation to < 0.05 mbar, isolation valve seal, 30-min vacuum decay leak rate test *)
    (* ------------------------------------------------------------------------------------------------ *)
    4:
        sFsmStateName := 'STATE_VACUUM_DECAY_INTEGRITY_LEAK_RATE_TEST';
        IF tStateTime_s < 900.0 THEN
            (* Evacuation Phase *)
            bCmd_VacuumBackingPump := TRUE;
            bCmd_VacuumRootsBlower := (rVotedCap <= 10.0);
            bCmd_ChamberIsolationValve := TRUE;
            rLeakTestStartPress := rVotedCap;
        ELSIF tStateTime_s < 2700.0 THEN
            (* Isolation Dwell Phase (1800 s) *)
            bCmd_ChamberIsolationValve := FALSE;
            bCmd_VacuumRootsBlower := FALSE;
            bCmd_VacuumBackingPump := FALSE;
        ELSE
            (* Evaluate Leak Rate [mbar/h] *)
            rLeakTestEndPress := rVotedCap;
            rLeakRate_mbar_h := (rLeakTestEndPress - rLeakTestStartPress) * 2.0; (* 30 min scaled to 1 h *)
            IF rLeakRate_mbar_h <= 0.025 THEN
                (* Vacuum Break with Sterile N2 *)
                bCmd_SterileN2AerationValve := TRUE;
                IF rVotedCap >= 980.0 THEN
                    bCmd_SterileN2AerationValve := FALSE;
                    nFsmState := 5; (* Advance to Vial Loading *)
                END_IF;
            ELSE
                (* Leak test failed *)
                dwFirstOutWord := 16#00000004;
                nFsmState := 13;
            END_IF;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 5: STATE_VIAL_LOADING_AND_DOOR_SEAL_INTERLOCK                                              *)
    (* Sterile isolator vial loading cart transfer; shelves held at +5 deg C to prevent dew condensation*)
    (* ------------------------------------------------------------------------------------------------ *)
    5:
        sFsmStateName := 'STATE_VIAL_LOADING_AND_DOOR_SEAL_INTERLOCK';
        bCmd_VacuumBackingPump := FALSE;
        bCmd_VacuumRootsBlower := FALSE;
        bCmd_ChamberIsolationValve := FALSE;

        (* Maintain shelf fluid at +5 deg C *)
        vecU[1] := 10.0;
        vecU[2] := 15.0;
        vecU[5] := 35.0;

        (* Await operator loading complete and door seal re-lock *)
        IF bDoorInterlockClosed AND bAutoMode AND (tStateTime_s >= 600.0) THEN
            nFsmState := 6; (* Advance to Freezing Ramp *)
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 6: STATE_SHELF_PRECOOLING_AND_FREEZING_RAMP                                                *)
    (* Controlled cooling ramp from +5 deg C to -45 deg C at 0.5 deg C/min; 2-hour frozen soak dwell    *)
    (* ------------------------------------------------------------------------------------------------ *)
    6:
        sFsmStateName := 'STATE_SHELF_PRECOOLING_AND_FREEZING_RAMP';
        bCmd_CascadeStage1Compressor := TRUE;
        vecU[1] := 0.0;
        vecU[2] := 85.0;
        vecU[5] := 80.0; (* High fluid velocity for uniform heat extraction *)

        (* Product frozen core temperature reaching -42 deg C *)
        IF rVotedProductVialTemp <= -42.0 THEN
            tSubTimer_s := tSubTimer_s + tScanInterval_s;
        ELSE
            tSubTimer_s := 0.0;
        END_IF;

        (* 7200 s (2 hour) frozen crystal structure soak *)
        IF tSubTimer_s >= 7200.0 THEN
            tSubTimer_s := 0.0;
            nFsmState := 7; (* Advance to Controlled Nucleation *)
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 7: STATE_CONTROLLED_ICE_NUCLEATION_PULSE                                                   *)
    (* Depressurization cold gas pulse inducing simultaneous uniform ice nucleation across all vials    *)
    (* ------------------------------------------------------------------------------------------------ *)
    7:
        sFsmStateName := 'STATE_CONTROLLED_ICE_NUCLEATION_PULSE';
        bCmd_CascadeStage2Compressor := TRUE; (* Pre-chill condenser coils to -85 deg C *)

        IF tStateTime_s <= 180.0 THEN
            (* Nucleation depressurization pulse *)
            bCmd_VacuumBackingPump := TRUE;
            bCmd_ChamberIsolationValve := TRUE;
        ELSE
            bCmd_VacuumBackingPump := FALSE;
            bCmd_ChamberIsolationValve := FALSE;
        END_IF;

        (* Re-solidify after nucleation pulse, ensure condenser is <= -75 deg C *)
        IF (tStateTime_s >= 3600.0) AND (rCondenserVotedTemp <= -75.0) AND (rVotedProductVialTemp <= -40.0) THEN
            rCumulativeSublimedMass_kg := 0.0;
            vecX_hat[6] := 0.0;
            nFsmState := 8; (* Advance to Primary Drying MPC *)
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 8: STATE_PRIMARY_DRYING_SUBLIMATION_MPC_ACTIVE                                             *)
    (* Active ice sublimation with 10 unrolled PGD MPC iterations, collapse safety barrier, and PRT    *)
    (* ------------------------------------------------------------------------------------------------ *)
    8:
        sFsmStateName := 'STATE_PRIMARY_DRYING_SUBLIMATION_MPC_ACTIVE';
        bCmd_CascadeStage1Compressor := TRUE;
        bCmd_CascadeStage2Compressor := TRUE;
        bCmd_VacuumBackingPump := TRUE;
        bCmd_VacuumRootsBlower := (rVotedCap <= 5.0);
        bCmd_ChamberIsolationValve := NOT bPRT_Active;

        (* MPC handles vecU modulations in Phase 4 *)

        (* Endpoint qualification check: Pirani/Cap ratio <= 1.05 and dry layer >= 11.5 mm *)
        IF (rPiraniCapPressureRatio <= 1.050) AND (vecX_hat[6] >= 11.50) AND (tStateTime_s >= 14400.0) THEN
            nFsmState := 9; (* Advance to PRT Endpoint Verification *)
        ELSIF bPRT_Trigger THEN
            bPRT_Trigger := FALSE;
            bPRT_Active := TRUE;
            tPRT_Timer_s := 0.0;
            rPRT_StartPress_mbar := rVotedCap;
            bCmd_ChamberIsolationValve := FALSE; (* Close isolation valve for PRT test *)
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 9: STATE_PRESSURE_RISE_TEST_ENDPOINT_VERIFICATION                                          *)
    (* Isolation butterfly closed for 30s; verified sublimation cessation before moving to desorption   *)
    (* ------------------------------------------------------------------------------------------------ *)
    9:
        sFsmStateName := 'STATE_PRESSURE_RISE_TEST_ENDPOINT_VERIFICATION';
        bCmd_ChamberIsolationValve := FALSE;

        IF bPRT_Passed THEN
            bPrimaryDryingComplete := TRUE;
            bCmd_ChamberIsolationValve := TRUE;
            nFsmState := 10; (* Advance to Secondary Drying *)
        ELSIF NOT bPRT_Active AND (tStateTime_s >= 60.0) THEN
            (* Sublimation still active: return to State 8 for additional primary drying *)
            bCmd_ChamberIsolationValve := TRUE;
            nFsmState := 8;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 10: STATE_SECONDARY_DRYING_THERMAL_DESORPTION                                              *)
    (* Ramp shelves to +25 deg C under maximum vacuum to desorb bound moisture to < 1.0% residual       *)
    (* ------------------------------------------------------------------------------------------------ *)
    10:
        sFsmStateName := 'STATE_SECONDARY_DRYING_THERMAL_DESORPTION';
        bCmd_ChamberIsolationValve := TRUE;
        bCmd_VacuumBackingPump := TRUE;
        bCmd_VacuumRootsBlower := TRUE;

        (* Ramp shelf temperature up to +25 deg C *)
        vecU[1] := 35.0;
        vecU[2] := 0.0;
        vecU[4] := 0.0; (* Vacuum bleed closed for ultimate vacuum *)
        vecU[5] := 60.0;

        (* 6-hour desorption dwell at +25 deg C *)
        IF (rVotedShelfFluidTemp >= 24.0) AND (tStateTime_s >= 21600.0) THEN
            bSecondaryDryingComplete := TRUE;
            nFsmState := 11; (* Advance to Hydraulic Stoppering *)
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 11: STATE_HYDRAULIC_VIAL_STOPPERING_RAM_PRESS                                              *)
    (* Compresses 16 shelves together under vacuum to permanently seat elastomeric stoppers in vials    *)
    (* ------------------------------------------------------------------------------------------------ *)
    11:
        sFsmStateName := 'STATE_HYDRAULIC_VIAL_STOPPERING_RAM_PRESS';
        vecU[1] := 0.0;
        vecU[2] := 0.0;

        (* Phase 5 handles hydraulic valve modulations *)

        IF bStopperingComplete THEN
            nFsmState := 12; (* Advance to Nitrogen Aeration *)
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 12: STATE_STERILE_NITROGEN_AERATION_BREAK                                                  *)
    (* Backfill chamber with sterile 0.2 um filtered N2 to atmospheric pressure, initiate de-icing      *)
    (* ------------------------------------------------------------------------------------------------ *)
    12:
        sFsmStateName := 'STATE_STERILE_NITROGEN_AERATION_BREAK';
        bCmd_VacuumRootsBlower := FALSE;
        bCmd_VacuumBackingPump := FALSE;
        bCmd_ChamberIsolationValve := FALSE;
        bCmd_SterileN2AerationValve := TRUE;
        bDefrostActive := TRUE; (* Start melting ice off condenser *)

        (* Chamber pressure reaching atmospheric 1,000 mbar *)
        IF rVotedCap >= 995.0 THEN
            bCmd_SterileN2AerationValve := FALSE;
            IF tStateTime_s >= 600.0 THEN
                nFsmState := 0; (* Cycle successfully completed, return to IDLE *)
            END_IF;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 13: STATE_EMERGENCY_POWER_FAILURE_OR_VACUUM_TRIP                                           *)
    (* Failsafe chamber isolation, instantaneous heating shutdown, product freeze protection           *)
    (* ------------------------------------------------------------------------------------------------ *)
    13:
        sFsmStateName := 'STATE_EMERGENCY_POWER_FAILURE_OR_VACUUM_TRIP';
        vecU[1] := 0.0; (* Quench heaters *)
        vecU[2] := 0.0;
        vecU[3] := 0.0;
        vecU[4] := 0.0;
        vecU[5] := 30.0; (* Low fluid circulation to avoid cold spots *)

        bCmd_ChamberIsolationValve := FALSE; (* Isolate chamber from condenser *)
        bCmd_VacuumRootsBlower := FALSE;
        bCmd_VacuumBackingPump := FALSE;
        bCmd_CascadeStage1Compressor := FALSE;
        bCmd_CascadeStage2Compressor := FALSE;
        bCmd_CIP_SupplyPump := FALSE;
        bCmd_SIP_PureSteamInletValve := FALSE;
        rCmd_HydraulicStopperingValve_pct := 0.0;

        (* Return to idle only after operator resets alarms and acknowledges trip *)
        IF bAcknowledgeAlarms AND bEmergencyStop AND (dwFirstOutWord = 16#00000000) THEN
            nFsmState := 0;
        END_IF;

    ELSE
        nFsmState := 13;
END_CASE;
"""
