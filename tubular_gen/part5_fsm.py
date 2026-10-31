# part5_fsm.py
fsm_text = """(* ==========================================================================================================
   PHASE 4: 12-STAGE OPERATIONAL FINITE STATE MACHINE (FSM)
   ========================================================================================================== *)
(* Track State Transitions *)
IF iState <> iPrevState THEN
    bStateChanged := TRUE;
    iSubPhase := 0;
    iPrevState := iState;
ELSE
    bStateChanged := FALSE;
END_IF;

(* Master FSM Execution *)
CASE iState OF

    (* ------------------------------------------------------------------------------------------------------
       STATE 10: INERT GAS LEAK TEST & HYDRAULIC PRESSURE PRE-LOAD
       Pre-commissioning acoustic emission leak testing and hydraulic actuator tensioning
       ------------------------------------------------------------------------------------------------------ *)
    10:
        iFSM_State := 10;
        iFSM_SubState := iSubPhase;

        (* Actuator Defaults for Standby / Testing *)
        rCmd_HyperSpeed_rpm             := 0.0;
        rCmd_HyperSuctionValve_pct      := 0.0;
        rCmd_HPLDV_ServoPos_pct         := 25.0; (* Hold let-down valve at seating test position *)
        rCmd_PeroxidePump_Z1_Stroke_pct := 0.0;
        rCmd_PeroxidePump_Z2_Stroke_pct := 0.0;
        rCmd_PeroxidePump_Z3_Stroke_pct := 0.0;
        rCmd_PeroxidePump_Z4_Stroke_pct := 0.0;
        rCmd_CTA_DosingPump_pct         := 0.0;
        rCmd_VAM_InjectionPump_pct      := 0.0;
        rCmd_Jacket3WayValve_Z1_pct     := 10.0;
        rCmd_Jacket3WayValve_Z2_pct     := 10.0;
        rCmd_Jacket3WayValve_Z3_pct     := 10.0;
        rCmd_Jacket3WayValve_Z4_pct     := 10.0;

        (* Fast Dump Valves Closed and Armed *)
        bCmd_DumpValve_Z1_Fire      := FALSE;
        bCmd_DumpValve_Z2_Fire      := FALSE;
        bCmd_DumpValve_Z3_Fire      := FALSE;
        bCmd_DumpValve_Z4_Fire      := FALSE;
        bCmd_HyperTrip_FastStop     := FALSE;
        bCmd_HPS_IsolateValve_Close := FALSE;
        bCmd_FlareCatchTank_Deluge  := FALSE;
        bCmd_N2_QuenchBarrier_Open  := FALSE;

        (* Sub-phase progression *)
        CASE iSubPhase OF
            0: (* Check hydraulic dump accumulator pressure & flare header *)
                IF rPress_HydrDumpAccum_bar >= 180.0 AND rPress_FlareHeader_bar <= 2.5 THEN
                    iSubPhase := 1;
                END_IF;

            1: (* Verify Nitrogen Pressurization Hold at 350 bar *)
                tPurgeTimer(IN := TRUE, PT := T#30S);
                IF tPurgeTimer.Q THEN
                    tPurgeTimer(IN := FALSE);
                    IF rVoted_Press_Inlet_bar >= 300.0 AND rVoted_Press_Inlet_bar <= 380.0 THEN
                        iSubPhase := 2;
                    END_IF;
                END_IF;

            2: (* Await Master Enable and advance to Ethylene Flush *)
                IF bMasterEnable AND bEmergencyStop THEN
                    iState := 20;
                END_IF;
        END_CASE;

    (* ------------------------------------------------------------------------------------------------------
       STATE 20: ETHYLENE GAS FLUSH & RECYCLE LINE PRE-COOL
       Monomer displacement of nitrogen inerting gas and cold recycle loop thermal equilibration
       ------------------------------------------------------------------------------------------------------ *)
    20:
        iFSM_State := 20;
        iFSM_SubState := iSubPhase;

        rCmd_HyperSpeed_rpm        := 120.0; (* Low idle speed for gas sweeping *)
        rCmd_HyperSuctionValve_pct := 15.0;
        rCmd_HPLDV_ServoPos_pct    := 40.0; (* Wide let-down to sweep unreacted gas to HPS *)

        CASE iSubPhase OF
            0: (* Ethylene displacement sweep timer *)
                tPurgeTimer(IN := TRUE, PT := T#45S);
                IF tPurgeTimer.Q THEN
                    tPurgeTimer(IN := FALSE);
                    IF rFlow_EthyleneFeed_kg_h > 5000.0 THEN
                        iSubPhase := 1;
                    END_IF;
                END_IF;

            1: (* Verify Recycle Gas Cooler Temperature Equilibrium *)
                IF rPress_HPS_Separator_bar >= 200.0 AND rPress_HPS_Separator_bar <= 280.0 THEN
                    iState := 30; (* Advance to Hyper-Compressor Ramp-Up *)
                END_IF;
        END_CASE;

    (* ------------------------------------------------------------------------------------------------------
       STATE 30: HYPER-COMPRESSOR STAGED RAMP-UP TO 2,000 BAR
       Controlled speed ramp of plunger reciprocating compressor with crosshead vibration oversight
       ------------------------------------------------------------------------------------------------------ *)
    30:
        iFSM_State := 30;
        iFSM_SubState := iSubPhase;

        (* Controlled speed ramp: 120 rpm -> 650 rpm *)
        IF rRamp_HyperSpeed_rpm < 650.0 THEN
            rRamp_HyperSpeed_rpm := rRamp_HyperSpeed_rpm + (15.0 * rDeltaTime_s);
        END_IF;
        rCmd_HyperSpeed_rpm := rRamp_HyperSpeed_rpm;
        rCmd_HyperSuctionValve_pct := 60.0;

        (* Modulate HPLDV to build inlet pressure towards 2,000 bar *)
        IF rVoted_Press_Inlet_bar < 2000.0 THEN
            rCmd_HPLDV_ServoPos_pct := 32.0;
        ELSE
            rCmd_HPLDV_ServoPos_pct := 42.0;
        END_IF;

        (* Vibration and packing leak guard *)
        IF rVib_HyperCrosshead_RMS_mm_s > 14.0 OR rFlow_HyperPackingLeak_kg_h > 50.0 THEN
            (* Hold speed if mechanical stress detected *)
            rRamp_HyperSpeed_rpm := rRamp_HyperSpeed_rpm - (5.0 * rDeltaTime_s);
        END_IF;

        tStabilizeTimer(IN := (rVoted_Press_Inlet_bar >= 1950.0), PT := T#30S);
        IF tStabilizeTimer.Q THEN
            tStabilizeTimer(IN := FALSE);
            iState := 40; (* Proceed to Hot Water Jacket Thermal Preheat *)
        END_IF;

    (* ------------------------------------------------------------------------------------------------------
       STATE 40: HOT WATER JACKET THERMAL PREHEAT
       Pressurized hot water heating of tube wall to reach peroxide decomposition initiation threshold
       ------------------------------------------------------------------------------------------------------ *)
    40:
        iFSM_State := 40;
        iFSM_SubState := iSubPhase;

        (* Maintain baseline pressure around 2,000 bar *)
        rCmd_HyperSpeed_rpm     := 650.0;
        rCmd_HPLDV_ServoPos_pct := 40.0;

        (* Ramp jacket heating 3-way valves to supply 180 deg C hot water *)
        IF rRamp_JacketTemp_degC < 180.0 THEN
            rRamp_JacketTemp_degC := rRamp_JacketTemp_degC + (2.5 * rDeltaTime_s);
        END_IF;
        rCmd_Jacket3WayValve_Z1_pct := 85.0;
        rCmd_Jacket3WayValve_Z2_pct := 85.0;
        rCmd_Jacket3WayValve_Z3_pct := 80.0;
        rCmd_Jacket3WayValve_Z4_pct := 75.0;

        (* Check if reactor inner skin/process temperature has reached minimum light-off criteria *)
        tPreheatTimer(IN := (rVoted_Temp_Peak1_degC >= 165.0) AND (rVoted_Temp_Peak2_degC >= 165.0), PT := T#45S);
        IF tPreheatTimer.Q THEN
            tPreheatTimer(IN := FALSE);
            iState := 50; (* Proceed to Zone 1 Peroxide Cut-In *)
        END_IF;

    (* ------------------------------------------------------------------------------------------------------
       STATE 50: INITIATOR PEROXIDE ZONE 1 DOSING CUT-IN
       Micro-metering intensifier pump displacement startup with exotherm slope detection
       ------------------------------------------------------------------------------------------------------ *)
    50:
        iFSM_State := 50;
        iFSM_SubState := iSubPhase;

        (* Ramp Zone 1 peroxide pump stroke gently: 0% -> 18% *)
        IF rRamp_Peroxide_Z1_pct < 18.0 THEN
            rRamp_Peroxide_Z1_pct := rRamp_Peroxide_Z1_pct + (0.8 * rDeltaTime_s);
        END_IF;
        rCmd_PeroxidePump_Z1_Stroke_pct := rRamp_Peroxide_Z1_pct;
        rCmd_PeroxidePump_Z2_Stroke_pct := 0.0;
        rCmd_PeroxidePump_Z3_Stroke_pct := 0.0;
        rCmd_PeroxidePump_Z4_Stroke_pct := 0.0;

        (* Monitor exotherm light-off: Zone 1 peak temp rising above 210 deg C *)
        IF rVoted_Temp_Peak1_degC >= 210.0 THEN
            iState := 60; (* Light-off verified, advance to Zone Staging *)
        END_IF;

        (* Failsafe timeout if no exotherm detected within 90 seconds *)
        tLightOffTimer(IN := TRUE, PT := T#90S);
        IF tLightOffTimer.Q THEN
            tLightOffTimer(IN := FALSE);
            (* Abort peroxide dosing and fallback to preheat *)
            rRamp_Peroxide_Z1_pct := 0.0;
            rCmd_PeroxidePump_Z1_Stroke_pct := 0.0;
            iState := 40;
        END_IF;

    (* ------------------------------------------------------------------------------------------------------
       STATE 60: REACTION EXOTHERM LIGHT-OFF & ZONE STAGING
       Switch jacket water from heating to cooling and cut in Zones 2, 3 and 4 sequentially
       ------------------------------------------------------------------------------------------------------ *)
    60:
        iFSM_State := 60;
        iFSM_SubState := iSubPhase;

        (* Switch Zone 1 Jacket to Cooling Mode *)
        rCmd_Jacket3WayValve_Z1_pct := 35.0;

        (* Ramp Zone 2 Peroxide *)
        IF rVoted_Temp_Peak1_degC >= 240.0 AND rRamp_Peroxide_Z2_pct < 22.0 THEN
            rRamp_Peroxide_Z2_pct := rRamp_Peroxide_Z2_pct + (0.6 * rDeltaTime_s);
        END_IF;
        rCmd_PeroxidePump_Z2_Stroke_pct := rRamp_Peroxide_Z2_pct;

        (* Ramp Zone 3 Peroxide *)
        IF rVoted_Temp_Peak2_degC >= 250.0 AND rRamp_Peroxide_Z3_pct < 20.0 THEN
            rRamp_Peroxide_Z3_pct := rRamp_Peroxide_Z3_pct + (0.6 * rDeltaTime_s);
        END_IF;
        rCmd_PeroxidePump_Z3_Stroke_pct := rRamp_Peroxide_Z3_pct;

        (* Ramp Zone 4 Peroxide *)
        IF rVoted_Temp_Peak3_degC >= 255.0 AND rRamp_Peroxide_Z4_pct < 16.0 THEN
            rRamp_Peroxide_Z4_pct := rRamp_Peroxide_Z4_pct + (0.5 * rDeltaTime_s);
        END_IF;
        rCmd_PeroxidePump_Z4_Stroke_pct := rRamp_Peroxide_Z4_pct;

        (* Switch downstream jackets to cooling mode *)
        rCmd_Jacket3WayValve_Z2_pct := 40.0;
        rCmd_Jacket3WayValve_Z3_pct := 45.0;
        rCmd_Jacket3WayValve_Z4_pct := 45.0;

        (* Check if multi-zone profile is established *)
        IF rVoted_Temp_Peak1_degC >= 260.0 AND rVoted_Temp_Peak2_degC >= 275.0 AND rVoted_Temp_Peak3_degC >= 270.0 THEN
            iState := 70; (* Transition to Full-Rate Steady-State Polymerization *)
        END_IF;

    (* ------------------------------------------------------------------------------------------------------
       STATE 70: FULL-RATE STEADY-STATE 3,000 BAR POLYMERIZATION
       Closed-loop receding horizon MPC governing peroxide dosing, jacket cooling, and HPLDV modulation
       ------------------------------------------------------------------------------------------------------ *)
    70:
        iFSM_State := 70;
        iFSM_SubState := iSubPhase;

        (* Full Hyper-Compressor Speed for 3,000 bar throughput *)
        rCmd_HyperSpeed_rpm        := 820.0;
        rCmd_HyperSuctionValve_pct := 95.0;

        (* Connect MPC Optimal Manipulated Variables to Actuators *)
        rCmd_PeroxidePump_Z1_Stroke_pct := uControl_Opt[1];
        rCmd_PeroxidePump_Z2_Stroke_pct := uControl_Opt[2];
        rCmd_PeroxidePump_Z3_Stroke_pct := uControl_Opt[3];
        rCmd_PeroxidePump_Z4_Stroke_pct := uControl_Opt[4];
        rCmd_Jacket3WayValve_Z1_pct     := uControl_Opt[5];
        rCmd_Jacket3WayValve_Z2_pct     := uControl_Opt[6];
        rCmd_Jacket3WayValve_Z3_pct     := uControl_Opt[7];
        rCmd_HPLDV_ServoPos_pct         := uControl_Opt[8];

        (* Dynamic calculation of per-pass monomer conversion *)
        rMonomerConversion_pct := 14.5 + (0.042 * (rVoted_Temp_Peak1_degC - 200.0))
                                       + (0.051 * (rVoted_Temp_Peak2_degC - 200.0))
                                       + (0.045 * (rVoted_Temp_Peak3_degC - 200.0))
                                       + (0.0035 * (rVoted_Press_Inlet_bar - 2500.0));
        IF rMonomerConversion_pct < 5.0 THEN rMonomerConversion_pct := 5.0; END_IF;
        IF rMonomerConversion_pct > 36.5 THEN rMonomerConversion_pct := 36.5; END_IF;

        (* Instantaneous Production Rate in ton/h *)
        rProductionRate_ton_h := (rFlow_EthyleneFeed_kg_h + rFlow_RecycleSuction_kg_h) * (rMonomerConversion_pct / 100.0) * 0.001;

        (* Dynamic Melt Flow Index prediction *)
        rEst_MeltFlowIndex_g_10min := 2.0 * EXP(0.012 * (rVoted_Temp_Peak2_degC - 290.0) - 0.0008 * (rVoted_Press_Inlet_bar - 2950.0));
        IF rEst_MeltFlowIndex_g_10min < 0.1 THEN rEst_MeltFlowIndex_g_10min := 0.1; END_IF;

        (* State Transitions from Steady-State *)
        IF bEVA_ModeSelect THEN
            iState := 90; (* Transition to EVA Copolymer Production *)
        ELSIF ABS(rEst_MeltFlowIndex_g_10min - rSet_Target_MFI_g_10min) > 0.35 THEN
            iState := 80; (* Transition to CTA Trimming *)
        ELSIF NOT bMasterEnable THEN
            iState := 100; (* Controlled Rinse & Flush Run-Down *)
        END_IF;

    (* ------------------------------------------------------------------------------------------------------
       STATE 80: MOLECULAR WEIGHT REGULATOR (CTA) TRIMMING
       Fine adjustment of propionaldehyde chain transfer modifier to lock in Melt Flow Index
       ------------------------------------------------------------------------------------------------------ *)
    80:
        iFSM_State := 80;
        iFSM_SubState := iSubPhase;

        (* Base polymerizing actuators maintain MPC tracking *)
        rCmd_PeroxidePump_Z1_Stroke_pct := uControl_Opt[1];
        rCmd_PeroxidePump_Z2_Stroke_pct := uControl_Opt[2];
        rCmd_PeroxidePump_Z3_Stroke_pct := uControl_Opt[3];
        rCmd_PeroxidePump_Z4_Stroke_pct := uControl_Opt[4];
        rCmd_HPLDV_ServoPos_pct         := uControl_Opt[8];

        (* CTA Closed-Loop Trim Controller *)
        IF rEst_MeltFlowIndex_g_10min < rSet_Target_MFI_g_10min THEN
            (* MFI too low (chains too long) -> Increase CTA modifier flow *)
            rCmd_CTA_DosingPump_pct := rCmd_CTA_DosingPump_pct + (0.15 * rDeltaTime_s);
        ELSIF rEst_MeltFlowIndex_g_10min > rSet_Target_MFI_g_10min THEN
            (* MFI too high (chains too short) -> Decrease CTA modifier flow *)
            rCmd_CTA_DosingPump_pct := rCmd_CTA_DosingPump_pct - (0.15 * rDeltaTime_s);
        END_IF;
        IF rCmd_CTA_DosingPump_pct < 2.0 THEN rCmd_CTA_DosingPump_pct := 2.0; END_IF;
        IF rCmd_CTA_DosingPump_pct > 85.0 THEN rCmd_CTA_DosingPump_pct := 85.0; END_IF;

        (* Return to Steady State once MFI is within +/- 0.08 g/10min for 20 seconds *)
        tStabilizeTimer(IN := (ABS(rEst_MeltFlowIndex_g_10min - rSet_Target_MFI_g_10min) <= 0.08), PT := T#20S);
        IF tStabilizeTimer.Q THEN
            tStabilizeTimer(IN := FALSE);
            iState := 70;
        END_IF;

    (* ------------------------------------------------------------------------------------------------------
       STATE 90: TRANSITION TO EVA CO-MONOMER FEED
       Introduction of Vinyl Acetate Monomer (VAM) and thermal profile depression to avoid fouling
       ------------------------------------------------------------------------------------------------------ *)
    90:
        iFSM_State := 90;
        iFSM_SubState := iSubPhase;

        (* Ramp VAM injection pump stroke *)
        IF rCmd_VAM_InjectionPump_pct < (rSet_Target_VAM_wt_pct * 3.2) THEN
            rCmd_VAM_InjectionPump_pct := rCmd_VAM_InjectionPump_pct + (0.25 * rDeltaTime_s);
        END_IF;

        (* Lower peak temperatures by 15 deg C to prevent vinyl acetate gelation *)
        xState_Ref[1] := 265.0;
        xState_Ref[2] := 278.0;
        xState_Ref[3] := 272.0;
        xState_Ref[4] := 260.0;

        rCmd_PeroxidePump_Z1_Stroke_pct := uControl_Opt[1] * 0.92;
        rCmd_PeroxidePump_Z2_Stroke_pct := uControl_Opt[2] * 0.90;
        rCmd_PeroxidePump_Z3_Stroke_pct := uControl_Opt[3] * 0.90;
        rCmd_PeroxidePump_Z4_Stroke_pct := uControl_Opt[4] * 0.88;
        rCmd_HPLDV_ServoPos_pct         := uControl_Opt[8];

        rEst_VAM_Content_wt_pct := (rFlow_VAM_CoMonomer_kg_h / (rFlow_EthyleneFeed_kg_h + 1.0)) * 100.0;

        IF NOT bEVA_ModeSelect THEN
            rCmd_VAM_InjectionPump_pct := 0.0;
            iState := 70; (* Return to Homopolymer *)
        ELSIF NOT bMasterEnable THEN
            iState := 100; (* Shutdown *)
        END_IF;

    (* ------------------------------------------------------------------------------------------------------
       STATE 100: CONTROLLED REACTOR RINSE & FLUSH RUN-DOWN
       Immediate peroxide dosing cutoff, high-rate jacket cooling, and monomer sweeping of waxes
       ------------------------------------------------------------------------------------------------------ *)
    100:
        iFSM_State := 100;
        iFSM_SubState := iSubPhase;

        (* Immediately stop all free-radical initiator dosing *)
        rCmd_PeroxidePump_Z1_Stroke_pct := 0.0;
        rCmd_PeroxidePump_Z2_Stroke_pct := 0.0;
        rCmd_PeroxidePump_Z3_Stroke_pct := 0.0;
        rCmd_PeroxidePump_Z4_Stroke_pct := 0.0;
        rCmd_CTA_DosingPump_pct         := 0.0;
        rCmd_VAM_InjectionPump_pct      := 0.0;

        (* Maximize cooling jacket water to quench tube reaction exotherm *)
        rCmd_Jacket3WayValve_Z1_pct := 100.0;
        rCmd_Jacket3WayValve_Z2_pct := 100.0;
        rCmd_Jacket3WayValve_Z3_pct := 100.0;
        rCmd_Jacket3WayValve_Z4_pct := 100.0;

        (* Modulate HPLDV to maintain sweeping velocity while lowering pressure *)
        rCmd_HPLDV_ServoPos_pct := 55.0;
        rCmd_HyperSpeed_rpm     := 450.0;

        (* Once all peak temperatures fall below 145 deg C and conversion < 2% *)
        tFlushTimer(IN := (rVoted_Temp_Peak1_degC < 145.0) AND (rVoted_Temp_Peak2_degC < 145.0), PT := T#60S);
        IF tFlushTimer.Q THEN
            tFlushTimer(IN := FALSE);
            iState := 110; (* Advance to Recycle Gas Sweep *)
        END_IF;

    (* ------------------------------------------------------------------------------------------------------
       STATE 110: INACTIVE RECYCLE GAS SWEEPING
       Low-pressure cold gas sweeping, depressurization down to flare purge
       ------------------------------------------------------------------------------------------------------ *)
    110:
        iFSM_State := 110;
        iFSM_SubState := iSubPhase;

        rCmd_HyperSpeed_rpm        := 180.0;
        rCmd_HyperSuctionValve_pct := 20.0;
        rCmd_HPLDV_ServoPos_pct    := 80.0; (* Open letdown valve to drop pressure *)

        tFlushTimer(IN := (rVoted_Press_Inlet_bar < 200.0), PT := T#45S);
        IF tFlushTimer.Q THEN
            tFlushTimer(IN := FALSE);
            rCmd_HyperSpeed_rpm := 0.0;
            iState := 10; (* Return to Standby State 10 *)
        END_IF;

    (* ------------------------------------------------------------------------------------------------------
       STATE 120: EMERGENCY DECOMPOSITION SIL-3 FAST DUMP FLARE
       Catastrophic decomposition mitigation: <45 ms simultaneous actuation of 4 dump valves
       ------------------------------------------------------------------------------------------------------ *)
    120:
        iFSM_State := 120;
        iFSM_SubState := iSubPhase;

        (* Latched SIL-3 Emergency Dump Fire Commands *)
        bCmd_DumpValve_Z1_Fire          := TRUE;
        bCmd_DumpValve_Z2_Fire          := TRUE;
        bCmd_DumpValve_Z3_Fire          := TRUE;
        bCmd_DumpValve_Z4_Fire          := TRUE;
        bCmd_HyperTrip_FastStop         := TRUE;
        bCmd_HPS_IsolateValve_Close     := TRUE;
        bCmd_FlareCatchTank_Deluge      := TRUE;
        bCmd_N2_QuenchBarrier_Open      := TRUE;

        (* Zero out all actuator outputs *)
        rCmd_HyperSpeed_rpm             := 0.0;
        rCmd_HyperSuctionValve_pct      := 0.0;
        rCmd_PeroxidePump_Z1_Stroke_pct := 0.0;
        rCmd_PeroxidePump_Z2_Stroke_pct := 0.0;
        rCmd_PeroxidePump_Z3_Stroke_pct := 0.0;
        rCmd_PeroxidePump_Z4_Stroke_pct := 0.0;
        rCmd_CTA_DosingPump_pct         := 0.0;
        rCmd_VAM_InjectionPump_pct      := 0.0;
        rCmd_HPLDV_ServoPos_pct         := 100.0; (* Full open HPLDV to assist blowdown *)
        rCmd_Jacket3WayValve_Z1_pct     := 100.0;
        rCmd_Jacket3WayValve_Z2_pct     := 100.0;
        rCmd_Jacket3WayValve_Z3_pct     := 100.0;
        rCmd_Jacket3WayValve_Z4_pct     := 100.0;

        bSIL3_DumpTriggered := TRUE;

        (* Require operator manual reset push-button and pressure < 50 bar to clear dump latch *)
        IF bResetAlarms AND (rVoted_Press_Inlet_bar < 50.0) AND bEmergencyStop THEN
            bSIL3_DumpTriggered := FALSE;
            bCmd_DumpValve_Z1_Fire     := FALSE;
            bCmd_DumpValve_Z2_Fire     := FALSE;
            bCmd_DumpValve_Z3_Fire     := FALSE;
            bCmd_DumpValve_Z4_Fire     := FALSE;
            bCmd_HyperTrip_FastStop    := FALSE;
            bCmd_N2_QuenchBarrier_Open := FALSE;
            iState := 10; (* Return to Standby State *)
        END_IF;

    ELSE
        (* Failsafe unmapped state handling *)
        iState := 10;
END_CASE;
"""

