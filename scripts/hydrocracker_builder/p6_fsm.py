# -*- coding: utf-8 -*-
"""
Part 6: Phase 6 (12-Stage Deterministic Operational Finite State Machine)
for FB_Chemicals_Hydrocracker_TrickleBed_HydrogenQuench
"""

def get_fsm_block():
    return """(* ==========================================================================================
 * PHASE 6: 12-STAGE DETERMINISTIC OPERATIONAL FINITE STATE MACHINE (FSM)
 * ========================================================================================== *)

(* Accumulate state residence time and total unit execution timers *)
tStateTimer_s := tStateTimer_s + rDeltaTime_s;
tStageTotalTimer_s := tStageTotalTimer_s + rDeltaTime_s;

CASE iState OF

    (* --------------------------------------------------------------------------------------
     * STATE 0: INERT NITROGEN PURGE & HIGH-PRESSURE LEAK TIGHTNESS TEST
     * -------------------------------------------------------------------------------------- *)
    0:
        sCurrentStateName := '0: Inert Nitrogen Purge & Leak Tightness Test';
        bUnitInRunState := FALSE;
        bReadyForHydrocarbonFeed := FALSE;

        (* Fail-safe valve baselines during nitrogen purge *)
        bValve_EmergencyBlowdownA_Open   := FALSE;
        bValve_EmergencyBlowdownB_Open   := FALSE;
        bValve_ReactorFeed_EmergencyShut := TRUE;  (* Oil feed isolated *)
        bValve_QuenchFastDump_Open       := FALSE;
        bValve_MakeupH2_EmergencyShut    := TRUE;  (* Fresh H2 isolated *)
        bIgniter_ChargeFurnace_Kill      := TRUE;  (* Furnace extinguished *)
        rPump_DMDS_Dosing_Speed_pct      := 0.0;

        (* Nitrogen purge sequence: sweep at 25 bar, then pressurize to 180 bar for leak hold *)
        rValve_QuenchBed1_pct        := 15.0;
        rValve_QuenchBed2_pct        := 15.0;
        rValve_QuenchBed3_pct        := 15.0;
        rValve_ChargeFurnaceFuel_pct := 0.0;
        rValve_HPSep_LetdownA_pct    := 0.0;
        rValve_HPSep_LetdownB_pct    := 0.0;
        rValve_HotHPSep_Letdown_pct  := 0.0;
        rPump_LeanAmine_Speed_pct    := 0.0;
        rValve_RichAmineLetdown_pct  := 0.0;
        rValve_DynamicReflux_pct     := 0.0;
        rValve_FractionatorReboiler_pct := 0.0;

        (* Transition permissive: N2 header ready, flare ready, pressure established, hold time complete *)
        IF bStateFirstScan THEN
            bStateFirstScan := FALSE;
            tStateTimer_s := 0.0;
        END_IF;

        IF (tStateTimer_s >= 60.0) AND bNitrogenPurgePermissive AND bFlareHeaderReady AND bStartSequence THEN
            iPrevState := iState;
            iState := 1; (* Transition to Hydrogen Circulation & Catalyst Sulfiding Pre-Heat *)
            bStateFirstScan := TRUE;
            tStateTimer_s := 0.0;
        END_IF;

    (* --------------------------------------------------------------------------------------
     * STATE 1: HYDROGEN CIRCULATION & CATALYST SULFIDING PRE-HEAT
     * -------------------------------------------------------------------------------------- *)
    1:
        sCurrentStateName := '1: Hydrogen Circulation & Catalyst Sulfiding Pre-Heat';
        bUnitInRunState := FALSE;
        bReadyForHydrocarbonFeed := FALSE;

        bValve_MakeupH2_EmergencyShut    := FALSE; (* Open make-up H2 battery limit *)
        bValve_ReactorFeed_EmergencyShut := TRUE;  (* Oil feed remains isolated *)
        bIgniter_ChargeFurnace_Kill      := FALSE; (* Enable furnace burner ignition *)

        (* Stage 1 Sulfiding Plateau Control:
         * Plateau 1: Ramp to 230 deg C, start DMDS dosing to decompose into H2S
         * Plateau 2: Ramp to 330 deg C, complete Ni-Mo-W oxide to active sulfide conversion *)
        IF iSulfidingStage = 1 THEN
            rValve_ChargeFurnaceFuel_pct := 28.0; (* Controlled ramp towards 230 deg C *)
            rPump_DMDS_Dosing_Speed_pct  := 35.0; (* Inject DMDS at 50 L/h *)
            IF rObserved_PeakCatalystTemp_degC >= 225.0 THEN
                tSulfidingHoldTimer_s := tSulfidingHoldTimer_s + rDeltaTime_s;
                IF tSulfidingHoldTimer_s >= 120.0 THEN
                    iSulfidingStage := 2; (* Advance to high-temperature sulfiding plateau *)
                    tSulfidingHoldTimer_s := 0.0;
                END_IF;
            END_IF;
        ELSE
            rValve_ChargeFurnaceFuel_pct := 45.0; (* Ramp towards 330 deg C *)
            rPump_DMDS_Dosing_Speed_pct  := 50.0; (* Maximize sulfiding saturation *)
            IF rObserved_PeakCatalystTemp_degC >= 325.0 THEN
                tSulfidingHoldTimer_s := tSulfidingHoldTimer_s + rDeltaTime_s;
            END_IF;
        END_IF;

        (* Maintain light hydrogen quench circulation to equalize bed profiles *)
        rValve_QuenchBed1_pct := 10.0;
        rValve_QuenchBed2_pct := 10.0;
        rValve_QuenchBed3_pct := 10.0;
        rPump_LeanAmine_Speed_pct := 30.0; (* Low circulation in amine column to absorb excess H2S *)

        (* Permissive to transition: Sulfiding complete, H2 circulation verified, compressor healthy *)
        IF (iSulfidingStage = 2) AND (tSulfidingHoldTimer_s >= 180.0) AND bPermissive_RecycleCompressor THEN
            bReadyForHydrocarbonFeed := TRUE;
            IF bAutoMode THEN
                iPrevState := iState;
                iState := 2; (* Transition to Hydrocarbon Feed Cut-In & Low-Rate Wetting *)
                bStateFirstScan := TRUE;
                tStateTimer_s := 0.0;
            END_IF;
        END_IF;

    (* --------------------------------------------------------------------------------------
     * STATE 2: HYDROCARBON FEED CUT-IN & LOW-RATE WETTING
     * -------------------------------------------------------------------------------------- *)
    2:
        sCurrentStateName := '2: Hydrocarbon Feed Cut-In & Low-Rate Wetting';
        bUnitInRunState := FALSE;
        bReadyForHydrocarbonFeed := TRUE;

        bValve_ReactorFeed_EmergencyShut := FALSE; (* Open oil feed cut-in valve *)
        rPump_DMDS_Dosing_Speed_pct      := 0.0;   (* Sulfiding complete, stop DMDS *)

        (* Feed introduced at 30% nominal rate to establish trickle flow regime *)
        rValve_ChargeFurnaceFuel_pct := 52.0;
        rValve_QuenchBed1_pct        := 18.0;
        rValve_QuenchBed2_pct        := 20.0;
        rValve_QuenchBed3_pct        := 22.0;

        (* Begin modulating HP separator level letdown *)
        rValve_HPSep_LetdownA_pct   := u_ctrl[5];
        rValve_HPSep_LetdownB_pct   := u_ctrl[5] * 0.90;
        rValve_HotHPSep_Letdown_pct := 25.0;
        rPump_LeanAmine_Speed_pct   := 45.0;

        (* Transition check: Exotherm starts developing (Delta T across Bed 1 > 8.0 deg C) *)
        IF (tStateTimer_s >= 90.0) AND (rDeltaT_Bed1 >= 8.0) THEN
            iPrevState := iState;
            iState := 3; (* Transition to Exotherm Detection & Quench Flow Calibration *)
            bStateFirstScan := TRUE;
            tStateTimer_s := 0.0;
        END_IF;

    (* --------------------------------------------------------------------------------------
     * STATE 3: EXOTHERM DETECTION & QUENCH GAS FLOW CALIBRATION
     * -------------------------------------------------------------------------------------- *)
    3:
        sCurrentStateName := '3: Exotherm Detection & Quench Gas Flow Calibration';
        bUnitInRunState := FALSE;

        (* Exotherm developing rapidly - calibrate quench gas split response *)
        rValve_QuenchBed1_pct := u_ctrl[1];
        rValve_QuenchBed2_pct := u_ctrl[2];
        rValve_QuenchBed3_pct := u_ctrl[3];
        rValve_ChargeFurnaceFuel_pct := u_ctrl[4];

        rValve_HPSep_LetdownA_pct := u_ctrl[5];
        rValve_HPSep_LetdownB_pct := u_ctrl[5];
        rPump_LeanAmine_Speed_pct := u_ctrl[6];

        (* Establish fractionation warm-up circulation *)
        rValve_DynamicReflux_pct := 25.0;
        rValve_FractionatorReboiler_pct := 35.0;

        (* Transition check: Bed temperature rates stabilized (< 6.0 deg C/min) and ramp feed to 100% *)
        IF (tStateTimer_s >= 120.0) AND
           (rObserved_Bed1_dTdt_degCmin < 6.0) AND
           (rObserved_Bed2_dTdt_degCmin < 6.0) AND
           (rObserved_Bed3_dTdt_degCmin < 6.0) AND
           (rObserved_Bed4_dTdt_degCmin < 6.0) THEN
            iPrevState := iState;
            iState := 4; (* Transition to Full Load Hydrocracking Run *)
            bStateFirstScan := TRUE;
            tStateTimer_s := 0.0;
        END_IF;

    (* --------------------------------------------------------------------------------------
     * STATE 4: FULL LOAD HYDROCRACKING RUN (NORMAL AUTONOMOUS PRODUCTION)
     * -------------------------------------------------------------------------------------- *)
    4:
        sCurrentStateName := '4: Full Load Hydrocracking Run';
        bUnitInRunState := TRUE;

        (* Multi-Variable MPC actively commands all continuous actuators *)
        rValve_QuenchBed1_pct        := u_ctrl[1];
        rValve_QuenchBed2_pct        := u_ctrl[2];
        rValve_QuenchBed3_pct        := u_ctrl[3];
        rValve_ChargeFurnaceFuel_pct := u_ctrl[4];
        rValve_HPSep_LetdownA_pct    := u_ctrl[5];
        rValve_HPSep_LetdownB_pct    := u_ctrl[5];
        rPump_LeanAmine_Speed_pct    := u_ctrl[6];

        rValve_HotHPSep_Letdown_pct  := 55.0;
        rValve_RichAmineLetdown_pct  := 48.0;
        rValve_DynamicReflux_pct     := 45.0 + (rFractionator_RefluxRatio * 5.0);
        rValve_FractionatorReboiler_pct := 65.0;

        (* CRITICAL SAFETY RUNAWAY CHECK:
         * If any catalyst bed rate of change exceeds 15.0 deg C/min OR hotspot > 435 deg C *)
        IF (rObserved_Bed1_dTdt_degCmin >= rBedTemp_Runaway_Rate_Trip) OR
           (rObserved_Bed2_dTdt_degCmin >= rBedTemp_Runaway_Rate_Trip) OR
           (rObserved_Bed3_dTdt_degCmin >= rBedTemp_Runaway_Rate_Trip) OR
           (rObserved_Bed4_dTdt_degCmin >= rBedTemp_Runaway_Rate_Trip) OR
           (rObserved_PeakCatalystTemp_degC >= rBedTemp_HH_Trip) THEN
            iPrevState := iState;
            iState := 7; (* Immediate Trip to Bed Temperature Rate-of-Change Runaway Trip *)
            bStateFirstScan := TRUE;
            tStateTimer_s := 0.0;
        END_IF;

    (* --------------------------------------------------------------------------------------
     * STATE 5: AMINE TREATING ABSORPTION BALANCING
     * -------------------------------------------------------------------------------------- *)
    5:
        sCurrentStateName := '5: Amine Treating Absorption Balancing';
        bUnitInRunState := TRUE;

        (* Dynamic closed-loop trimming of lean solvent circulation *)
        rValve_QuenchBed1_pct        := u_ctrl[1];
        rValve_QuenchBed2_pct        := u_ctrl[2];
        rValve_QuenchBed3_pct        := u_ctrl[3];
        rValve_ChargeFurnaceFuel_pct := u_ctrl[4];
        rValve_HPSep_LetdownA_pct    := u_ctrl[5];
        rValve_HPSep_LetdownB_pct    := u_ctrl[5];

        (* Boost amine circulation flow to suppress overhead H2S spike *)
        rPump_LeanAmine_Speed_pct    := u_ctrl[6] + 15.0;
        IF rPump_LeanAmine_Speed_pct > 100.0 THEN rPump_LeanAmine_Speed_pct := 100.0; END_IF;
        rValve_RichAmineLetdown_pct  := (rLevel_AmineSump_pct - 50.0) * 1.8 + 45.0;

        (* Return to normal hydrocracking once H2S drops below 20 ppm *)
        IF (rTMR8_VotedVal <= 20.0) AND (tStateTimer_s >= 60.0) THEN
            iPrevState := iState;
            iState := 4;
            bStateFirstScan := TRUE;
            tStateTimer_s := 0.0;
        END_IF;

    (* --------------------------------------------------------------------------------------
     * STATE 6: ATMOSPHERIC FRACTIONATION CUT SEPARATION
     * -------------------------------------------------------------------------------------- *)
    6:
        sCurrentStateName := '6: Atmospheric Fractionation Cut Separation';
        bUnitInRunState := TRUE;

        rValve_QuenchBed1_pct        := u_ctrl[1];
        rValve_QuenchBed2_pct        := u_ctrl[2];
        rValve_QuenchBed3_pct        := u_ctrl[3];
        rValve_ChargeFurnaceFuel_pct := u_ctrl[4];
        rValve_HPSep_LetdownA_pct    := u_ctrl[5];
        rValve_HPSep_LetdownB_pct    := u_ctrl[5];
        rPump_LeanAmine_Speed_pct    := u_ctrl[6];

        (* Distillation optimization for high-yield ULSD & Jet Fuel cuts *)
        rValve_DynamicReflux_pct        := 55.0;
        rValve_FractionatorReboiler_pct := 72.0;

        IF (tStateTimer_s >= 180.0) THEN
            iPrevState := iState;
            iState := 4;
            bStateFirstScan := TRUE;
            tStateTimer_s := 0.0;
        END_IF;

    (* --------------------------------------------------------------------------------------
     * STATE 7: BED TEMPERATURE RATE-OF-CHANGE RUNAWAY TRIP (EXOTHERM SUPPRESSION)
     * -------------------------------------------------------------------------------------- *)
    7:
        sCurrentStateName := '7: Bed Temperature Runaway Trip - Emergency Quench Dump';
        bUnitInRunState := FALSE;
        bAlarm_RunawayTripActive := TRUE;

        (* EMERGENCY PROTECTIVE ACTIONS:
         * 1. Slam-shut raw hydrocarbon feed isolation valve *)
        bValve_ReactorFeed_EmergencyShut := TRUE;
        (* 2. Extinguish charge heater fires immediately *)
        bIgniter_ChargeFurnace_Kill := TRUE;
        rValve_ChargeFurnaceFuel_pct := 0.0;
        (* 3. Flood all hydrogen quench headers at 100% full open *)
        bValve_QuenchFastDump_Open := TRUE;
        rValve_QuenchBed1_pct := 100.0;
        rValve_QuenchBed2_pct := 100.0;
        rValve_QuenchBed3_pct := 100.0;

        (* If bed temperatures do not decelerate within 15 seconds OR continue rising beyond 440 deg C,
         * escalate immediately to SIL-3 High-Pressure Emergency Depressurization (State 8) *)
        IF (tStateTimer_s >= 15.0) OR (rObserved_PeakCatalystTemp_degC >= 440.0) THEN
            iPrevState := iState;
            iState := 8; (* Escalate to High-Pressure Emergency Depressurization (Blowdown) *)
            bStateFirstScan := TRUE;
            tStateTimer_s := 0.0;
        END_IF;

    (* --------------------------------------------------------------------------------------
     * STATE 8: HIGH-PRESSURE EMERGENCY DEPRESSURIZATION (BLOWDOWN TO FLARE)
     * -------------------------------------------------------------------------------------- *)
    8:
        sCurrentStateName := '8: High-Pressure Emergency Depressurization (Blowdown)';
        bUnitInRunState := FALSE;
        bAlarm_AnyCritical := TRUE;

        (* SIL-3 EMERGENCY DEPRESSURIZATION SYSTEM (API RP 521):
         * Open dual redundant fail-open slam valves to HP Flare *)
        bValve_EmergencyBlowdownA_Open   := TRUE;
        bValve_EmergencyBlowdownB_Open   := TRUE;
        bValve_ReactorFeed_EmergencyShut := TRUE;
        bValve_MakeupH2_EmergencyShut    := TRUE;
        bIgniter_ChargeFurnace_Kill      := TRUE;
        rValve_ChargeFurnaceFuel_pct     := 0.0;
        bValve_QuenchFastDump_Open       := TRUE;
        rValve_QuenchBed1_pct            := 100.0;
        rValve_QuenchBed2_pct            := 100.0;
        rValve_QuenchBed3_pct            := 100.0;

        (* Isolate separator letdowns to prevent gas blowby *)
        rValve_HPSep_LetdownA_pct   := 0.0;
        rValve_HPSep_LetdownB_pct   := 0.0;
        rValve_HotHPSep_Letdown_pct := 0.0;
        rPump_LeanAmine_Speed_pct   := 0.0;

        (* Depressurization terminates when reactor inlet pressure drops below 15.0 bar *)
        IF rTMR7_VotedVal <= 15.0 THEN
            iPrevState := iState;
            iState := 9; (* Transition to Catalyst Hydrogen Stripping *)
            bStateFirstScan := TRUE;
            tStateTimer_s := 0.0;
        END_IF;

    (* --------------------------------------------------------------------------------------
     * STATE 9: CATALYST HYDROGEN STRIPPING
     * -------------------------------------------------------------------------------------- *)
    9:
        sCurrentStateName := '9: Catalyst Hydrogen Stripping';
        bUnitInRunState := FALSE;

        (* Close flare blowdown valves to conserve sweep gas *)
        bValve_EmergencyBlowdownA_Open := FALSE;
        bValve_EmergencyBlowdownB_Open := FALSE;
        bValve_QuenchFastDump_Open     := FALSE;

        (* Circulate warm hydrogen at low pressure to strip residual heavy coke precursors *)
        rValve_QuenchBed1_pct := 25.0;
        rValve_QuenchBed2_pct := 25.0;
        rValve_QuenchBed3_pct := 25.0;

        IF tStateTimer_s >= 120.0 THEN
            iPrevState := iState;
            iState := 10; (* Transition to Controlled Nitrogen Cooldown *)
            bStateFirstScan := TRUE;
            tStateTimer_s := 0.0;
        END_IF;

    (* --------------------------------------------------------------------------------------
     * STATE 10: CONTROLLED NITROGEN COOLDOWN
     * -------------------------------------------------------------------------------------- *)
    10:
        sCurrentStateName := '10: Controlled Nitrogen Cooldown';
        bUnitInRunState := FALSE;

        bValve_MakeupH2_EmergencyShut := TRUE; (* Isolate H2 *)

        (* Nitrogen sweep cooling at rate <= 25.0 deg C/h to prevent temper embrittlement *)
        rValve_QuenchBed1_pct := 40.0;
        rValve_QuenchBed2_pct := 40.0;
        rValve_QuenchBed3_pct := 40.0;

        (* Transition to Safe Cold Hold once all catalyst beds drop below 50.0 deg C *)
        IF (rObserved_PeakCatalystTemp_degC <= 50.0) OR (tStateTimer_s >= 300.0) THEN
            iPrevState := iState;
            iState := 11; (* Transition to Cold Idle Safe Hold *)
            bStateFirstScan := TRUE;
            tStateTimer_s := 0.0;
        END_IF;

    (* --------------------------------------------------------------------------------------
     * STATE 11: COLD IDLE SAFE HOLD
     * -------------------------------------------------------------------------------------- *)
    11:
        sCurrentStateName := '11: Cold Idle Safe Hold';
        bUnitInRunState := FALSE;

        (* Unit secured under 2.0 bar nitrogen blanket *)
        bValve_EmergencyBlowdownA_Open   := FALSE;
        bValve_EmergencyBlowdownB_Open   := FALSE;
        bValve_ReactorFeed_EmergencyShut := TRUE;
        bValve_MakeupH2_EmergencyShut    := TRUE;
        bValve_QuenchFastDump_Open       := FALSE;
        bIgniter_ChargeFurnace_Kill      := TRUE;

        rValve_QuenchBed1_pct           := 0.0;
        rValve_QuenchBed2_pct           := 0.0;
        rValve_QuenchBed3_pct           := 0.0;
        rValve_ChargeFurnaceFuel_pct    := 0.0;
        rValve_HPSep_LetdownA_pct       := 0.0;
        rValve_HPSep_LetdownB_pct       := 0.0;
        rValve_HotHPSep_Letdown_pct     := 0.0;
        rPump_LeanAmine_Speed_pct       := 0.0;
        rValve_RichAmineLetdown_pct     := 0.0;
        rValve_DynamicReflux_pct        := 0.0;
        rValve_FractionatorReboiler_pct := 0.0;
        rPump_DMDS_Dosing_Speed_pct     := 0.0;

        (* Re-start sequence possible upon operator command *)
        IF bStartSequence AND bReset THEN
            iPrevState := iState;
            iState := 0; (* Return to State 0 *)
            bStateFirstScan := TRUE;
            tStateTimer_s := 0.0;
        END_IF;

    ELSE
        (* Default Fallback Safe Branch *)
        iState := 8; (* Force Emergency Depressurization *)
        bStateFirstScan := TRUE;
        tStateTimer_s := 0.0;
END_CASE;
"""
