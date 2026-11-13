# scratch/gen_phase4.py

def get_phase4():
    lines = []
    lines.append("""
(* ============================================================================== *)
(* PHASE 4: DETERMINISTIC 14-STAGE NUCLEAR FINITE STATE MACHINE (FSM)            *)
(* ============================================================================== *)
(* Fully deterministic state transitions governing thermo-hydraulic operational   *)
(* and emergency safety-critical regimes for Class 1E Nuclear Steam Generation.    *)
(* ------------------------------------------------------------------------------ *)

fStateElapsedTime := fStateElapsedTime + fCycleTime_Ts;

CASE eCurrentState OF

    0: (* ---------------------------------------------------------------------- *)
       (* STAGE 0: COLD_SHUTDOWN_HOT_STANDBY_TRANSFER                           *)
       (* RCS Temperature warming up from cold shutdown (< 150 C) to Hot Standby *)
       (* ---------------------------------------------------------------------- *)
        nActiveFSMStateID := 0;
        (* MFRV and BPV kept isolated until hot standby parameters established *)
        fMFRV_PositionDemand := 0.00000000;
        bMFRV_FastTripClosureCmd := FALSE;
        bBPV_FastTripClosureCmd := FALSE;

        (* Maintain Wide Range level at 10,500 mm via auxiliary filling *)
        IF fVotedWideRangeLevel_mm < 9500.00000000 THEN
            fAFW_MotorPump1_SpeedDemand := 25.00000000;
            bAFW_MotorPump1_AutoStartCmd := TRUE;
        ELSIF fVotedWideRangeLevel_mm > 10800.00000000 THEN
            fAFW_MotorPump1_SpeedDemand := 0.00000000;
            bAFW_MotorPump1_AutoStartCmd := FALSE;
        END_IF;

        (* Transition to Low Power Bypass Control once Hot Standby achieved *)
        IF (fVotedColdLegTemp_degC >= 280.00000000) AND 
           (fVotedDrumPressure_bar >= 60.00000000) AND 
           (fVotedWideRangeLevel_mm >= 10000.00000000) AND 
           (fNI_ReactorThermalPower >= 1.00000000) THEN
            ePreviousState := eCurrentState;
            eCurrentState := 1; (* STARTUP_LOW_POWER_BYPASS_CONTROL *)
            fStateElapsedTime := 0.00000000;
            bStateFirstScan := TRUE;
        END_IF;

    1: (* ---------------------------------------------------------------------- *)
       (* STAGE 1: STARTUP_LOW_POWER_BYPASS_CONTROL (<15% FP)                    *)
       (* Low power operation: MFRV closed, small BPV valve modulates level      *)
       (* ---------------------------------------------------------------------- *)
        nActiveFSMStateID := 1;
        fMFRV_PositionDemand := 0.00000000; (* Main valve closed *)
        bMFRV_FastTripClosureCmd := FALSE;

        (* Low-Power Bypass Valve modulates water inventory *)
        (* High shrink/swell susceptibility: anti-swell feedforward active *)
        fBPV_PositionDemand := u_mpc_horiz[1, 2] + (0.50000000 * fAntiSwellBias);
        IF fBPV_PositionDemand < 0.00000000 THEN
            fBPV_PositionDemand := 0.00000000;
        ELSIF fBPV_PositionDemand > 100.00000000 THEN
            fBPV_PositionDemand := 100.00000000;
        END_IF;

        (* Shutdown AFW motor pumps once secondary steaming begins *)
        bAFW_MotorPump1_AutoStartCmd := FALSE;
        fAFW_MotorPump1_SpeedDemand := 0.00000000;

        (* Transfer Condition: Thermal power reaches 15% and BPV demand reaches 80% *)
        IF (fNI_ReactorThermalPower >= 15.00000000) AND 
           (fBPV_PositionDemand >= 75.00000000) AND 
           (fStateElapsedTime >= 10.00000000) THEN
            ePreviousState := eCurrentState;
            eCurrentState := 2; (* MAIN_REGULATING_VALVE_TRANSFER_BUMPLESS *)
            fStateElapsedTime := 0.00000000;
            bStateFirstScan := TRUE;
            fBypassValveHoldPosition := fBPV_PositionDemand;
            fMainValveHoldPosition := 0.00000000;
        END_IF;

    2: (* ---------------------------------------------------------------------- *)
       (* STAGE 2: MAIN_REGULATING_VALVE_TRANSFER_BUMPLESS                       *)
       (* Smooth cross-over ramp from BPV to MFRV to prevent secondary pressure  *)
       (* and level surge oscillations (30 second controlled ramp)               *)
       (* ---------------------------------------------------------------------- *)
        nActiveFSMStateID := 2;
        IF bStateFirstScan THEN
            fBumplessTransferTimer := 0.00000000;
            bStateFirstScan := FALSE;
        END_IF;

        fBumplessTransferTimer := fBumplessTransferTimer + fCycleTime_Ts;
        fTransferRampRate := fBumplessTransferTimer / 30.00000000;
        IF fTransferRampRate > 1.00000000 THEN
            fTransferRampRate := 1.00000000;
        END_IF;

        (* Cross-fade MFRV and BPV position demands *)
        fMFRV_PositionDemand := (fTransferRampRate * 25.00000000) + (u_mpc_horiz[1, 1] * fTransferRampRate);
        fBPV_PositionDemand := fBypassValveHoldPosition * (1.00000000 - fTransferRampRate);

        (* Clamp valve positions *)
        IF fMFRV_PositionDemand < 0.00000000 THEN
            fMFRV_PositionDemand := 0.00000000;
        ELSIF fMFRV_PositionDemand > 100.00000000 THEN
            fMFRV_PositionDemand := 100.00000000;
        END_IF;

        IF fBPV_PositionDemand < 0.00000000 THEN
            fBPV_PositionDemand := 0.00000000;
        END_IF;

        (* Transfer Complete after 30 seconds *)
        IF fBumplessTransferTimer >= 30.00000000 THEN
            fBPV_PositionDemand := 0.00000000;
            ePreviousState := eCurrentState;
            eCurrentState := 3; (* AT_POWER_CASCADE_FEEDFORWARD_STABILIZED *)
            fStateElapsedTime := 0.00000000;
            bStateFirstScan := TRUE;
        END_IF;

    3: (* ---------------------------------------------------------------------- *)
       (* STAGE 3: AT_POWER_CASCADE_FEEDFORWARD_STABILIZED (15% - 50% FP)        *)
       (* MFRV active with 3-element cascade: level error + steam/FW mass balance *)
       (* ---------------------------------------------------------------------- *)
        nActiveFSMStateID := 3;
        fBPV_PositionDemand := 0.00000000;

        (* 3-Element Control calculation: MFRV tracks steam flow with level trim *)
        fMFRV_PositionDemand := ((fVotedSteamFlow_t_h / 2500.00000000) * 100.00000000) + 
                                ((fProgrammedLevelTarget - fVotedNarrowRangeLevel_mm) * 0.08500000) + 
                                fAntiSwellBias;

        IF fMFRV_PositionDemand < 0.00000000 THEN
            fMFRV_PositionDemand := 0.00000000;
        ELSIF fMFRV_PositionDemand > 100.00000000 THEN
            fMFRV_PositionDemand := 100.00000000;
        END_IF;

        (* Advance to full MPC tracking when thermal power exceeds 50% *)
        IF (fNI_ReactorThermalPower >= 50.00000000) AND (fStateElapsedTime >= 15.00000000) THEN
            ePreviousState := eCurrentState;
            eCurrentState := 4; (* FULL_POWER_OPTIMAL_MPC_TRACKING *)
            fStateElapsedTime := 0.00000000;
            bStateFirstScan := TRUE;
        (* Regress to BPV if power drops below 12% *)
        ELSIF fNI_ReactorThermalPower < 12.00000000 THEN
            ePreviousState := eCurrentState;
            eCurrentState := 1; (* STARTUP_LOW_POWER_BYPASS_CONTROL *)
            fStateElapsedTime := 0.00000000;
            bStateFirstScan := TRUE;
        END_IF;

    4: (* ---------------------------------------------------------------------- *)
       (* STAGE 4: FULL_POWER_OPTIMAL_MPC_TRACKING (50% - 100% FP)               *)
       (* State-space multivariable MPC fully active with PGD optimization       *)
       (* ---------------------------------------------------------------------- *)
        nActiveFSMStateID := 4;
        fBPV_PositionDemand := 0.00000000;

        (* Output computed from Phase 3 MPC Receding Horizon Optimization *)
        fMFRV_PositionDemand := u_mpc_horiz[1, 1] + fAntiSwellBias;
        IF fMFRV_PositionDemand < 0.00000000 THEN
            fMFRV_PositionDemand := 0.00000000;
        ELSIF fMFRV_PositionDemand > 100.00000000 THEN
            fMFRV_PositionDemand := 100.00000000;
        END_IF;

        (* Detect rapid load rejection (-5%/min or turbine runback flag) *)
        IF (fDerivSteamFlow <= -25.00000000) OR bTurbineTripActive THEN
            ePreviousState := eCurrentState;
            eCurrentState := 5; (* RAPID_LOAD_REJECTION_TURBINE_RUNBACK *)
            fStateElapsedTime := 0.00000000;
            bStateFirstScan := TRUE;
        (* Regress to 3-Element cascade if power drops below 45% *)
        ELSIF fNI_ReactorThermalPower < 45.00000000 THEN
            ePreviousState := eCurrentState;
            eCurrentState := 3; (* AT_POWER_CASCADE_FEEDFORWARD_STABILIZED *)
            fStateElapsedTime := 0.00000000;
            bStateFirstScan := TRUE;
        END_IF;

    5: (* ---------------------------------------------------------------------- *)
       (* STAGE 5: RAPID_LOAD_REJECTION_TURBINE_RUNBACK (-5%/min)                *)
       (* Extreme thermal swell anticipated: throttle MFRV while steam dumps open*)
       (* ---------------------------------------------------------------------- *)
        nActiveFSMStateID := 5;

        (* Rapidly adjust MFRV to match collapsing steam demand without waiting for level plunge *)
        fMFRV_PositionDemand := ((fVotedSteamFlow_t_h / 2500.00000000) * 100.00000000) + 
                                ((fProgrammedLevelTarget - fVotedNarrowRangeLevel_mm) * 0.04500000) + 
                                (1.50000000 * fAntiSwellBias);

        IF fMFRV_PositionDemand < 5.00000000 THEN
            fMFRV_PositionDemand := 5.00000000; (* Maintain minimum feedwater flow *)
        ELSIF fMFRV_PositionDemand > 100.00000000 THEN
            fMFRV_PositionDemand := 100.00000000;
        END_IF;

        (* Once transient stabilizes (> 45s elapsed and flow derivative near zero), return to State 4 or 3 *)
        IF (fStateElapsedTime >= 45.00000000) AND (ABS(fDerivSteamFlow) < 5.00000000) THEN
            ePreviousState := eCurrentState;
            IF fNI_ReactorThermalPower >= 50.00000000 THEN
                eCurrentState := 4; (* FULL_POWER_OPTIMAL_MPC_TRACKING *)
            ELSE
                eCurrentState := 3; (* AT_POWER_CASCADE_FEEDFORWARD_STABILIZED *)
            END_IF;
            fStateElapsedTime := 0.00000000;
            bStateFirstScan := TRUE;
        END_IF;

    6: (* ---------------------------------------------------------------------- *)
       (* STAGE 6: MAIN_STEAM_ISOLATION_VALVE_FAST_CLOSURE                       *)
       (* MSIV fast trip closure (< 5s). Secondary side isolated from turbine    *)
       (* ---------------------------------------------------------------------- *)
        nActiveFSMStateID := 6;
        (* Fast trip MFRV and BPV to prevent over-pressurization & overfill *)
        bMFRV_FastTripClosureCmd := TRUE;
        bBPV_FastTripClosureCmd := TRUE;
        fMFRV_PositionDemand := 0.00000000;
        fBPV_PositionDemand := 0.00000000;
        bMSIV_SG_IsolationReq := TRUE;
        bBlowdownIsolationCmd := TRUE;

        (* Transition to Post-Scram Equilibrium or Dry-Out Protection *)
        IF fVotedNarrowRangeLevel_mm < -450.00000000 THEN
            ePreviousState := eCurrentState;
            eCurrentState := 8; (* AUXILIARY_FEEDWATER_MOTOR_DRIVEN_START *)
            fStateElapsedTime := 0.00000000;
            bStateFirstScan := TRUE;
        ELSIF bReactorScramActive THEN
            ePreviousState := eCurrentState;
            eCurrentState := 12; (* REACTOR_PROTECTION_SYSTEM_SCRAM_OVERRIDE *)
            fStateElapsedTime := 0.00000000;
            bStateFirstScan := TRUE;
        END_IF;

    7: (* ---------------------------------------------------------------------- *)
       (* STAGE 7: STEAM_GENERATOR_TUBE_RUPTURE_DIAGNOSTIC (SGTR)                *)
       (* Primary-to-secondary tube leak detected via N-16 radiation & level drift*)
       (* ---------------------------------------------------------------------- *)
        nActiveFSMStateID := 7;
        (* SGTR Emergency Mitigation Protocol *)
        bReactorScramSG_TripReq := TRUE;
        bTurbineTripSG_Req := TRUE;
        bMSIV_SG_IsolationReq := TRUE;
        bBlowdownIsolationCmd := TRUE;

        (* Fast close MFRV and BPV to isolate faulted steam generator *)
        bMFRV_FastTripClosureCmd := TRUE;
        bBPV_FastTripClosureCmd := TRUE;
        fMFRV_PositionDemand := 0.00000000;
        fBPV_PositionDemand := 0.00000000;

        (* Isolate AFW to faulted SG to prevent overfill & radiological release *)
        bAFW_MotorPump1_AutoStartCmd := FALSE;
        bAFW_MotorPump2_AutoStartCmd := FALSE;
        bAFW_TurbinePump_AutoStartCmd := FALSE;
        fAFW_MotorPump1_SpeedDemand := 0.00000000;
        fAFW_MotorPump2_SpeedDemand := 0.00000000;
        fAFW_TurbinePump_GovernorDemand := 0.00000000;

        (* Stay latched in SGTR mitigation state until master reset *)
        IF bMasterResetTrip THEN
            ePreviousState := eCurrentState;
            eCurrentState := 0; (* COLD_SHUTDOWN_HOT_STANDBY_TRANSFER *)
            fStateElapsedTime := 0.00000000;
            bStateFirstScan := TRUE;
        END_IF;

    8: (* ---------------------------------------------------------------------- *)
       (* STAGE 8: AUXILIARY_FEEDWATER_MOTOR_DRIVEN_START                        *)
       (* Level Low-Low (-450 mm) or loss of MFW: Auto-start motor AFW pumps     *)
       (* ---------------------------------------------------------------------- *)
        nActiveFSMStateID := 8;
        bAFW_MotorPump1_AutoStartCmd := TRUE;
        bAFW_MotorPump2_AutoStartCmd := TRUE;

        (* Modulate MDAFW pump injection flow based on Narrow Range level error *)
        fAFW_MotorPump1_SpeedDemand := 50.00000000 + ((-200.00000000 - fVotedNarrowRangeLevel_mm) * 0.15000000);
        IF fAFW_MotorPump1_SpeedDemand < 20.00000000 THEN
            fAFW_MotorPump1_SpeedDemand := 20.00000000;
        ELSIF fAFW_MotorPump1_SpeedDemand > 100.00000000 THEN
            fAFW_MotorPump1_SpeedDemand := 100.00000000;
        END_IF;
        fAFW_MotorPump2_SpeedDemand := fAFW_MotorPump1_SpeedDemand;

        (* If water level restored above -100 mm and MFW restored, return to State 3 or 12 *)
        IF fVotedNarrowRangeLevel_mm >= -100.00000000 THEN
            ePreviousState := eCurrentState;
            IF bReactorScramActive THEN
                eCurrentState := 13; (* POST_SCRAM_DECAY_HEAT_THERMAL_EQUILIBRIUM *)
            ELSE
                eCurrentState := 3; (* AT_POWER_CASCADE_FEEDFORWARD_STABILIZED *)
            END_IF;
            fStateElapsedTime := 0.00000000;
            bStateFirstScan := TRUE;
        (* If level continues dropping below -650 mm or SBO, initiate Turbine AFW *)
        ELSIF (fVotedNarrowRangeLevel_mm <= -650.00000000) OR bStationBlackoutSignal THEN
            ePreviousState := eCurrentState;
            eCurrentState := 9; (* AUXILIARY_FEEDWATER_TURBINE_DRIVEN_AUTO_INIT *)
            fStateElapsedTime := 0.00000000;
            bStateFirstScan := TRUE;
        END_IF;

    9: (* ---------------------------------------------------------------------- *)
       (* STAGE 9: AUXILIARY_FEEDWATER_TURBINE_DRIVEN_AUTO_INIT                  *)
       (* Station Blackout (SBO) or extreme Low-Low: steam turbine pump auto-init*)
       (* ---------------------------------------------------------------------- *)
        nActiveFSMStateID := 9;
        bAFW_TurbinePump_AutoStartCmd := TRUE;
        fAFW_TurbinePump_GovernorDemand := 100.00000000; (* Full steam admission *)

        (* If Wide Range level drops critically below 1500 mm, initiate Dry-Out Cooldown *)
        IF fVotedWideRangeLevel_mm <= 1500.00000000 THEN
            ePreviousState := eCurrentState;
            eCurrentState := 10; (* DRY_OUT_PROTECTION_RAPID_COOLDOWN *)
            fStateElapsedTime := 0.00000000;
            bStateFirstScan := TRUE;
        (* If level recovers above -300 mm NR, transition back to MDAFW control *)
        ELSIF fVotedNarrowRangeLevel_mm >= -300.00000000 THEN
            ePreviousState := eCurrentState;
            eCurrentState := 8; (* AUXILIARY_FEEDWATER_MOTOR_DRIVEN_START *)
            fStateElapsedTime := 0.00000000;
            bStateFirstScan := TRUE;
        END_IF;

    10: (* --------------------------------------------------------------------- *)
        (* STAGE 10: DRY_OUT_PROTECTION_RAPID_COOLDOWN                          *)
        (* Emergency secondary depressurization via ARVs to maximize injection  *)
        (* --------------------------------------------------------------------- *)
        nActiveFSMStateID := 10;
        bTrip_DryoutRisk := TRUE;
        bReactorScramSG_TripReq := TRUE;
        bTurbineTripSG_Req := TRUE;
        bAFW_TurbinePump_AutoStartCmd := TRUE;
        bAFW_MotorPump1_AutoStartCmd := TRUE;
        bAFW_MotorPump2_AutoStartCmd := TRUE;
        fAFW_TurbinePump_GovernorDemand := 100.00000000;
        fAFW_MotorPump1_SpeedDemand := 100.00000000;
        fAFW_MotorPump2_SpeedDemand := 100.00000000;

        (* Cooldown verification: level recovers above 3500 mm WR *)
        IF fVotedWideRangeLevel_mm >= 3500.00000000 THEN
            bTrip_DryoutRisk := FALSE;
            ePreviousState := eCurrentState;
            eCurrentState := 13; (* POST_SCRAM_DECAY_HEAT_THERMAL_EQUILIBRIUM *)
            fStateElapsedTime := 0.00000000;
            bStateFirstScan := TRUE;
        END_IF;

    11: (* --------------------------------------------------------------------- *)
        (* STAGE 11: OVERFILL_PROTECTION_MAIN_FEEDWATER_ISOLATION                *)
        (* Level High-High (+450 mm): Fast hydraulic isolation of MFRV & BPV     *)
        (* --------------------------------------------------------------------- *)
        nActiveFSMStateID := 11;
        bTrip_OverfillRisk := TRUE;
        bMFRV_FastTripClosureCmd := TRUE;
        bBPV_FastTripClosureCmd := TRUE;
        bTurbineTripSG_Req := TRUE;
        fMFRV_PositionDemand := 0.00000000;
        fBPV_PositionDemand := 0.00000000;

        (* Hold isolation until level drops below +150 mm and master reset pressed *)
        IF (fVotedNarrowRangeLevel_mm <= 150.00000000) AND bMasterResetTrip THEN
            bTrip_OverfillRisk := FALSE;
            bMFRV_FastTripClosureCmd := FALSE;
            bBPV_FastTripClosureCmd := FALSE;
            ePreviousState := eCurrentState;
            IF bReactorScramActive THEN
                eCurrentState := 13; (* POST_SCRAM_DECAY_HEAT_THERMAL_EQUILIBRIUM *)
            ELSE
                eCurrentState := 3; (* AT_POWER_CASCADE_FEEDFORWARD_STABILIZED *)
            END_IF;
            fStateElapsedTime := 0.00000000;
            bStateFirstScan := TRUE;
        END_IF;

    12: (* --------------------------------------------------------------------- *)
        (* STAGE 12: REACTOR_PROTECTION_SYSTEM_SCRAM_OVERRIDE                    *)
        (* Hardwired RPS trip: control rods drop, level setpoint shifts to -200 mm*)
        (* --------------------------------------------------------------------- *)
        nActiveFSMStateID := 12;
        bTurbineTripSG_Req := TRUE;

        (* Level setpoint ramps to post-trip shrinkage target: -200 mm *)
        fProgrammedLevelTarget := -200.00000000;

        (* Cutback MFRV to match collapsing core power *)
        fMFRV_PositionDemand := ((fVotedSteamFlow_t_h / 2500.00000000) * 100.00000000) + 
                                ((-200.00000000 - fVotedNarrowRangeLevel_mm) * 0.05000000);
        IF fMFRV_PositionDemand < 0.00000000 THEN
            fMFRV_PositionDemand := 0.00000000;
        ELSIF fMFRV_PositionDemand > 30.00000000 THEN
            fMFRV_PositionDemand := 30.00000000;
        END_IF;

        (* Transition to steady post-scram decay heat removal after 60 seconds *)
        IF fStateElapsedTime >= 60.00000000 THEN
            ePreviousState := eCurrentState;
            eCurrentState := 13; (* POST_SCRAM_DECAY_HEAT_THERMAL_EQUILIBRIUM *)
            fStateElapsedTime := 0.00000000;
            bStateFirstScan := TRUE;
        END_IF;

    13: (* --------------------------------------------------------------------- *)
        (* STAGE 13: POST_SCRAM_DECAY_HEAT_THERMAL_EQUILIBRIUM                   *)
        (* Long-term decay heat removal via natural circulation cooling          *)
        (* ASME Section III cooldown rate strictly limited to < 55 C/hr          *)
        (* --------------------------------------------------------------------- *)
        nActiveFSMStateID := 13;
        fMFRV_PositionDemand := 0.00000000;
        bMFRV_FastTripClosureCmd := FALSE;

        (* Modulate auxiliary feedwater to maintain water level at -150 mm *)
        IF fVotedNarrowRangeLevel_mm < -250.00000000 THEN
            bAFW_MotorPump1_AutoStartCmd := TRUE;
            fAFW_MotorPump1_SpeedDemand := 35.00000000 + ((-150.00000000 - fVotedNarrowRangeLevel_mm) * 0.10000000);
            IF fAFW_MotorPump1_SpeedDemand > 75.00000000 THEN
                fAFW_MotorPump1_SpeedDemand := 75.00000000;
            END_IF;
        ELSIF fVotedNarrowRangeLevel_mm > -50.00000000 THEN
            fAFW_MotorPump1_SpeedDemand := 0.00000000;
            bAFW_MotorPump1_AutoStartCmd := FALSE;
        END_IF;

        (* Continuous monitoring of cooldown rate (deg C / hr) *)
        fDecayHeatCooldownRate := (3600.00000000 / fCycleTime_Ts) * ABS(fVotedColdLegTemp_degC - fPrevVal_TE_CL_A);
        IF fDecayHeatCooldownRate > 55.00000000 THEN
            (* Cooldown rate exceeding ASME Section III limit: throttle AFW *)
            fAFW_MotorPump1_SpeedDemand := fAFW_MotorPump1_SpeedDemand * 0.80000000;
        END_IF;

        (* Exit only on manual reset after plant reaches cold shutdown *)
        IF bMasterResetTrip AND (fVotedColdLegTemp_degC < 100.00000000) THEN
            ePreviousState := eCurrentState;
            eCurrentState := 0; (* COLD_SHUTDOWN_HOT_STANDBY_TRANSFER *)
            fStateElapsedTime := 0.00000000;
            bStateFirstScan := TRUE;
        END_IF;

END_CASE;

(* ----------------------------------------------------------------------------- *)
(* SAFETY TRIP OVERRIDE INTERLOCKS EVALUATED EVERY SCAN CYCLE                    *)
(* ----------------------------------------------------------------------------- *)
(* Overfill Protection Priority Override *)
IF (fVotedNarrowRangeLevel_mm >= 450.00000000) AND (eCurrentState <> 11) THEN
    ePreviousState := eCurrentState;
    eCurrentState := 11; (* OVERFILL_PROTECTION_MAIN_FEEDWATER_ISOLATION *)
    fStateElapsedTime := 0.00000000;
    bStateFirstScan := TRUE;
END_IF;

(* SGTR Tube Rupture Priority Override *)
IF (fVotedSGTR_Rad_Bq_m3 >= 1850000.00000000) AND (eCurrentState <> 7) THEN
    ePreviousState := eCurrentState;
    eCurrentState := 7; (* STEAM_GENERATOR_TUBE_RUPTURE_DIAGNOSTIC *)
    fStateElapsedTime := 0.00000000;
    bStateFirstScan := TRUE;
END_IF;

(* MSIV Fast Closure Priority Override *)
IF bMSIV_ClosureActive AND (eCurrentState <> 6) AND (eCurrentState <> 7) THEN
    ePreviousState := eCurrentState;
    eCurrentState := 6; (* MAIN_STEAM_ISOLATION_VALVE_FAST_CLOSURE *)
    fStateElapsedTime := 0.00000000;
    bStateFirstScan := TRUE;
END_IF;

(* Reactor Scram Priority Override *)
IF bReactorScramActive AND (eCurrentState <> 12) AND (eCurrentState <> 13) AND 
   (eCurrentState <> 7) AND (eCurrentState <> 11) THEN
    ePreviousState := eCurrentState;
    eCurrentState := 12; (* REACTOR_PROTECTION_SYSTEM_SCRAM_OVERRIDE *)
    fStateElapsedTime := 0.00000000;
    bStateFirstScan := TRUE;
END_IF;
""")
    return "".join(lines)

if __name__ == "__main__":
    p4 = get_phase4()
    print(f"Phase 4 generated. Length: {len(p4)} characters.")
