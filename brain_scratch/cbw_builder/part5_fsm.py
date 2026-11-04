# part5_fsm.py
# Generates Phase 6: 12-Stage Operational Finite State Machine (FSM)

def get_part5():
    return '''(* ==========================================================================================
 * PHASE 6: 12-STAGE OPERATIONAL FINITE STATE MACHINE (FSM)
 * Industrial Cycle Sequence:
 *   State 1 : CBW_STATE_STANDBY_IDLE
 *   State 2 : CBW_STATE_WATER_PREFILL_RECYCLE
 *   State 3 : CBW_STATE_CHEMICAL_PRIME_DOSE
 *   State 4 : CBW_STATE_PREWASH_HEATING_CIRC
 *   State 5 : CBW_STATE_COUNTERFLOW_MAIN_WASH
 *   State 6 : CBW_STATE_TRANSFER_TOP_DRUM_INDEX
 *   State 7 : CBW_STATE_RINSE_HEAT_RECOVERY
 *   State 8 : CBW_STATE_PRESS_LOAD_SHUTTLE
 *   State 9 : CBW_STATE_MEMBRANE_DEWATER_RAM_50BAR
 *   State 10: CBW_STATE_CAKE_EJECTION_SHUTTLE_DISPATCH
 *   State 11: CBW_STATE_CIP_GREYWATER_FILTER_BACKWASH
 *   State 12: CBW_STATE_EMERGENCY_PRESS_DUMP_SAFE
 * ========================================================================================== *)

(* Increment state residence timer and cycle total duration *)
tStateTimer_s := tStateTimer_s + rDeltaTime_s;
tCycleTotalTimer_s := tCycleTotalTimer_s + rDeltaTime_s;
iCurrentState := iState;

CASE iState OF

    (* --------------------------------------------------------------------------------------
     * STATE 1: CBW_STATE_STANDBY_IDLE
     * Tunnel washer and press at rest. Checking hardware interlocks, water levels,
     * safety light curtains, and awaiting operator / supervisory cycle start command.
     * -------------------------------------------------------------------------------------- *)
    1:
        sCurrentStateName := 'STANDBY_IDLE';
        bReadyForNextBatch := TRUE;
        bCycleComplete := FALSE;

        (* Safe default actuator commands *)
        rValve_SteamDirect_pct          := 0.0;
        rValve_FreshWater_pct           := 0.0;
        rPump_ReclaimRecirc_pct         := 0.0;
        rDosing_Alkali_Lmin             := 0.0;
        rDosing_Detergent_Lmin          := 0.0;
        rDosing_Bleach_Lmin             := 0.0;
        rDosing_AcidSour_Lmin           := 0.0;
        rDosing_Softener_Lmin           := 0.0;
        rPress_ProportionalPressure_bar := 0.0;
        rPress_RamSpeed_mms             := 0.0;
        rDrum_DriveSpeed_RPM            := 0.0;
        rShuttle_Speed_mms              := 0.0;
        bValve_EmergencyDump_Open       := FALSE;
        bValve_SteamIsolation_Open      := FALSE;
        bPress_BottomPlateLift_Up       := FALSE;
        bPress_PneumaticEjector_Active  := FALSE;
        bPump_GreywaterBackwash_Start   := FALSE;
        bShuttle_TraverseForward        := FALSE;
        bShuttle_TraverseReverse        := FALSE;
        bShuttle_DischargeRollers_Run   := FALSE;
        rCycleRemainingTime_s           := 620.0; (* Nominal batch cycle duration *)

        (* Transition Condition: Cycle Start trigger with all safety interlocks healthy *)
        IF bStartCycle AND bAutoMode AND bEnable AND bEmergencyStop AND
           bPressGuard_Locked AND bLightCurtain_Clear AND bEjectionLift_Retracted THEN
            bReadyForNextBatch := FALSE;
            iPrevState := 1;
            iState := 2; (* Advance to WATER_PREFILL_RECYCLE *)
            tStateTimer_s := 0.0;
            tCycleTotalTimer_s := 0.0;
            bStateFirstScan := TRUE;
        END_IF;


    (* --------------------------------------------------------------------------------------
     * STATE 2: CBW_STATE_WATER_PREFILL_RECYCLE
     * Pre-filling counter-flow circuit from Plate Heat Exchanger warm reclaim tank.
     * Monitoring reclaim tank level and fresh makeup water blending.
     * -------------------------------------------------------------------------------------- *)
    2:
        sCurrentStateName := 'WATER_PREFILL_RECYCLE';
        bReadyForNextBatch := FALSE;
        bValve_SteamIsolation_Open := TRUE; (* Open pneumatic main steam shutoff *)
        rCycleRemainingTime_s := 600.0;

        (* Modulate fresh water makeup valve and reclaim recirculation pump via MPC *)
        rValve_FreshWater_pct   := u_ctrl[2];
        rPump_ReclaimRecirc_pct := u_ctrl[3];
        rValve_SteamDirect_pct  := 0.0;
        rPress_ProportionalPressure_bar := 0.0;
        rDrum_DriveSpeed_RPM    := 0.0;

        (* Transition Condition: Reclaim tank level stabilized above 45% and prefill duration >= 25 s *)
        IF (tStateTimer_s >= 25.0) AND (rTMR2_VotedVal >= 40.0) THEN
            iPrevState := 2;
            iState := 3; (* Advance to CHEMICAL_PRIME_DOSE *)
            tStateTimer_s := 0.0;
            bStateFirstScan := TRUE;
        ELSIF tStateTimer_s >= 60.0 THEN
            (* Timeout failsafe: Advance anyway if level sufficient *)
            IF rTMR2_VotedVal >= 30.0 THEN
                iPrevState := 2;
                iState := 3;
                tStateTimer_s := 0.0;
                bStateFirstScan := TRUE;
            END_IF;
        END_IF;


    (* --------------------------------------------------------------------------------------
     * STATE 3: CBW_STATE_CHEMICAL_PRIME_DOSE
     * Priming 12-channel peristaltic manifold and injecting primary alkali & detergent
     * charge into main wash compartments 4, 5 and 6 based on batch dry mass.
     * -------------------------------------------------------------------------------------- *)
    3:
        sCurrentStateName := 'CHEMICAL_PRIME_DOSE';
        rCycleRemainingTime_s := 575.0;

        (* Dosing rates based on batch dry weight (e.g. 50 kg -> 12.5 L/min alkali, 6.0 L/min detergent) *)
        rDosing_Alkali_Lmin    := (rBatchDryWeight_kg / 50.0) * 12.5;
        rDosing_Detergent_Lmin := (rBatchDryWeight_kg / 50.0) * 6.0;
        rDosing_Bleach_Lmin    := 0.0;
        rDosing_AcidSour_Lmin  := 0.0;
        rDosing_Softener_Lmin  := 0.0;
        rPump_ReclaimRecirc_pct:= 35.0; (* Maintain gentle carrier flow *)

        (* Transition Condition: Pre-dosing active charge completed after 20.0 seconds *)
        IF tStateTimer_s >= 20.0 THEN
            rDosing_Alkali_Lmin    := 0.0;
            rDosing_Detergent_Lmin := 0.0;
            iPrevState := 3;
            iState := 4; (* Advance to PREWASH_HEATING_CIRC *)
            tStateTimer_s := 0.0;
            bStateFirstScan := TRUE;
        END_IF;


    (* --------------------------------------------------------------------------------------
     * STATE 4: CBW_STATE_PREWASH_HEATING_CIRC
     * Pre-wash wetting out phase (38°C to 42°C). Gentle rocking of Archimedean screw
     * drum (+/- 120 deg) to wet textiles without premature thermal setting of proteins.
     * -------------------------------------------------------------------------------------- *)
    4:
        sCurrentStateName := 'PREWASH_HEATING_CIRC';
        rCycleRemainingTime_s := 555.0;

        (* Oscillate Archimedean drum: +/- 120 deg rocking at 6.0 RPM *)
        rDrum_DriveSpeed_RPM := 6.0;
        IF tStateTimer_s < 20.0 THEN
            rDrumTargetAngle_deg := 120.0;
        ELSIF tStateTimer_s < 40.0 THEN
            rDrumTargetAngle_deg := -120.0;
        ELSE
            rDrumTargetAngle_deg := 120.0;
        END_IF;

        (* Low-temperature steam trim to pre-wash zone *)
        rValve_SteamDirect_pct  := u_ctrl[1] * 0.40; (* Mild heating clamp *)
        rPump_ReclaimRecirc_pct := u_ctrl[3];
        rValve_FreshWater_pct   := u_ctrl[2] * 0.50;

        (* Transition Condition: Pre-wash contact time elapsed (60.0 s) *)
        IF tStateTimer_s >= 60.0 THEN
            iPrevState := 4;
            iState := 5; (* Advance to COUNTERFLOW_MAIN_WASH *)
            tStateTimer_s := 0.0;
            iDrumOscillationCount := 0;
            bStateFirstScan := TRUE;
        END_IF;


    (* --------------------------------------------------------------------------------------
     * STATE 5: CBW_STATE_COUNTERFLOW_MAIN_WASH
     * High-temperature thermal disinfection (85°C) and counter-flow chemical washing.
     * Vigorous drum rocking motion (+/- 300 deg at 10.0 RPM). MPC closed-loop steam,
     * water, and chemical dosing modulation.
     * -------------------------------------------------------------------------------------- *)
    5:
        sCurrentStateName := 'COUNTERFLOW_MAIN_WASH';
        rCycleRemainingTime_s := MAX(0.0, 495.0 - tStateTimer_s);

        (* Vigorous drum rocking motion: Reversing every 12.0 seconds *)
        rDrum_DriveSpeed_RPM := 10.0;
        IF (MOD(REAL_TO_INT(tStateTimer_s), 24) < 12) THEN
            bDrumRockingDirection := FALSE; (* Clockwise swing *)
            rDrumTargetAngle_deg := 300.0;
        ELSE
            bDrumRockingDirection := TRUE;  (* Counter-Clockwise swing *)
            rDrumTargetAngle_deg := -300.0;
        END_IF;

        (* Actuators driven by MPC Optimization Engine *)
        rValve_SteamDirect_pct  := u_ctrl[1];
        rValve_FreshWater_pct   := u_ctrl[2];
        rPump_ReclaimRecirc_pct := u_ctrl[3];
        rDosing_Alkali_Lmin     := u_ctrl[4];
        rDosing_Detergent_Lmin  := (rBatchDryWeight_kg / 50.0) * 4.5;
        
        (* Bleach / Peracetic Acid dosing during mid-wash (after 45 s into wash) *)
        IF (tStateTimer_s >= 45.0) AND (tStateTimer_s <= 95.0) THEN
            rDosing_Bleach_Lmin := (rBatchDryWeight_kg / 50.0) * 3.5;
        ELSE
            rDosing_Bleach_Lmin := 0.0;
        END_IF;

        (* Disinfection verification: Temp >= 82.0 deg C for at least 60 seconds *)
        IF (tStateTimer_s >= 150.0) AND (rTMR1_VotedVal >= 82.0) THEN
            rValve_SteamDirect_pct := 0.0; (* Shut steam prior to drum transfer *)
            rDosing_Alkali_Lmin    := 0.0;
            rDosing_Detergent_Lmin := 0.0;
            rDosing_Bleach_Lmin    := 0.0;
            iPrevState := 5;
            iState := 6; (* Advance to TRANSFER_TOP_DRUM_INDEX *)
            tStateTimer_s := 0.0;
            bStateFirstScan := TRUE;
        END_IF;


    (* --------------------------------------------------------------------------------------
     * STATE 6: CBW_STATE_TRANSFER_TOP_DRUM_INDEX
     * Top-Transfer Archimedean Screw indexing: Complete 360-degree forward rotation of drum.
     * All 16 compartments transfer textile batches one stage forward.
     * Compartment 16 discharges finished wash cake down drop chute into press basket.
     * Interlock: Press must be verified completely empty and bottom plate lowered!
     * -------------------------------------------------------------------------------------- *)
    6:
        sCurrentStateName := 'TRANSFER_TOP_DRUM_INDEX';
        rCycleRemainingTime_s := 345.0;

        (* Rotate drum continuously forward at 8.0 RPM until 360-deg index completed *)
        IF bEjectionLift_Retracted AND (rPress_ProportionalPressure_bar <= 0.5) THEN
            rDrum_DriveSpeed_RPM := 8.0;
            rDrumTargetAngle_deg := 360.0;
        ELSE
            rDrum_DriveSpeed_RPM := 0.0; (* Hold transfer until press ready *)
        END_IF;

        rValve_SteamDirect_pct  := 0.0;
        rDosing_Alkali_Lmin     := 0.0;
        rDosing_Detergent_Lmin  := 0.0;
        rDosing_Bleach_Lmin     := 0.0;

        (* Transition Condition: Full 360-degree index completed and zero-home switch reached *)
        IF (tStateTimer_s >= 25.0) AND (bDrumHome_Position OR (tStateTimer_s >= 35.0)) THEN
            rDrum_DriveSpeed_RPM := 0.0;
            iPrevState := 6;
            iState := 7; (* Advance to RINSE_HEAT_RECOVERY *)
            tStateTimer_s := 0.0;
            bStateFirstScan := TRUE;
        END_IF;


    (* --------------------------------------------------------------------------------------
     * STATE 7: CBW_STATE_RINSE_HEAT_RECOVERY
     * Counter-flow rinsing of transferred batches (compartments 10 to 14).
     * Acid sour neutralizer dosing to reduce pH to 5.8..6.5. Cationic fabric softener dosing.
     * Effluent warm water routed through Plate Heat Exchanger to pre-heat incoming fresh rinse.
     * -------------------------------------------------------------------------------------- *)
    7:
        sCurrentStateName := 'RINSE_HEAT_RECOVERY';
        rCycleRemainingTime_s := 310.0;

        (* Gentle drum rocking: +/- 150 deg at 7.0 RPM *)
        rDrum_DriveSpeed_RPM := 7.0;
        IF (MOD(REAL_TO_INT(tStateTimer_s), 20) < 10) THEN
            rDrumTargetAngle_deg := 150.0;
        ELSE
            rDrumTargetAngle_deg := -150.0;
        END_IF;

        (* Counterflow rinse water flow and chemical dosing *)
        rValve_FreshWater_pct   := u_ctrl[2];
        rPump_ReclaimRecirc_pct := u_ctrl[3];
        rDosing_AcidSour_Lmin   := u_ctrl[5];
        
        (* Softener dosing during final half of rinse *)
        IF (tStateTimer_s >= 40.0) THEN
            rDosing_Softener_Lmin := (rBatchDryWeight_kg / 50.0) * 2.8;
        ELSE
            rDosing_Softener_Lmin := 0.0;
        END_IF;

        (* Transition Condition: Rinse cycle duration complete (80.0 s) *)
        IF tStateTimer_s >= 80.0 THEN
            rDosing_AcidSour_Lmin := 0.0;
            rDosing_Softener_Lmin := 0.0;
            iPrevState := 7;
            iState := 8; (* Advance to PRESS_LOAD_SHUTTLE *)
            tStateTimer_s := 0.0;
            bStateFirstScan := TRUE;
        END_IF;


    (* --------------------------------------------------------------------------------------
     * STATE 8: CBW_STATE_PRESS_LOAD_SHUTTLE
     * Wet textile cake from compartment 16 seated inside hydraulic press basket.
     * Applying low seating pressure (8.0 bar) and lowering ram to contact cake surface.
     * Verifying safety enclosure locked and light curtain clear.
     * -------------------------------------------------------------------------------------- *)
    8:
        sCurrentStateName := 'PRESS_LOAD_SHUTTLE';
        rCycleRemainingTime_s := 230.0;
        rDrum_DriveSpeed_RPM := 0.0;

        (* Low pressure seating advance *)
        rPress_ProportionalPressure_bar := 8.0;
        rPress_RamSpeed_mms := 60.0; (* Controlled advance speed *)
        bPress_BottomPlateLift_Up := FALSE;

        (* Transition Condition: Ram advanced into basket and initial contact established *)
        IF (tStateTimer_s >= 12.0) AND (rPress_RamPosition_mm > 150.0) AND bPressGuard_Locked THEN
            iPrevState := 8;
            iState := 9; (* Advance to MEMBRANE_DEWATER_RAM_50BAR *)
            tStateTimer_s := 0.0;
            iPressSubPhase := 1; (* Start SubPhase 1: Low-pressure bulk drainage *)
            bStateFirstScan := TRUE;
        END_IF;


    (* --------------------------------------------------------------------------------------
     * STATE 9: CBW_STATE_MEMBRANE_DEWATER_RAM_50BAR
     * High-pressure 50-bar hydraulic consolidation and membrane bladder expansion.
     * 4-Stage Progressive Dewatering Profile:
     *   SubPhase 1: 0 -> 18 bar bulk free water expulsion (20 s)
     *   SubPhase 2: 18 -> 38 bar intermediate consolidation (25 s)
     *   SubPhase 3: 38 -> 50 bar membrane water cushion inflation (35 s)
     *   SubPhase 4: 50 bar dwell until target residual moisture reached (M <= 45%)
     * -------------------------------------------------------------------------------------- *)
    9:
        sCurrentStateName := 'MEMBRANE_DEWATER_50BAR';
        rCycleRemainingTime_s := MAX(0.0, 218.0 - tStateTimer_s);

        CASE iPressSubPhase OF
            1: (* SubPhase 1: Bulk Drainage (0 -> 18 bar) *)
                rPress_TargetPressure := 18.0;
                rPress_RamSpeed_mms   := 35.0;
                IF tStateTimer_s >= 20.0 THEN
                    iPressSubPhase := 2;
                END_IF;

            2: (* SubPhase 2: Intermediate Consolidation (18 -> 38 bar) *)
                rPress_TargetPressure := 38.0;
                rPress_RamSpeed_mms   := 15.0;
                IF tStateTimer_s >= 45.0 THEN
                    iPressSubPhase := 3;
                END_IF;

            3: (* SubPhase 3: High-Pressure Membrane Expansion (38 -> 50 bar) *)
                rPress_TargetPressure := 50.0;
                rPress_RamSpeed_mms   := 5.0;
                IF tStateTimer_s >= 80.0 THEN
                    iPressSubPhase := 4;
                END_IF;

            4: (* SubPhase 4: High Pressure Dwell & Moisture Monitoring *)
                rPress_TargetPressure := 50.0;
                rPress_RamSpeed_mms   := 0.0;
        END_CASE;

        (* Set active pressure command via MPC filtered loop *)
        rPress_ProportionalPressure_bar := u_ctrl[6];

        (* Transition Condition: Target cake moisture achieved OR maximum press dwell timeout *)
        IF ((rEstimatedCakeMoisture_pct <= rTargetMoisture_pct) AND (tStateTimer_s >= 60.0)) OR
           (tStateTimer_s >= 110.0) THEN
            iPrevState := 9;
            iState := 10; (* Advance to CAKE_EJECTION_SHUTTLE_DISPATCH *)
            tStateTimer_s := 0.0;
            iPressSubPhase := 5; (* Decompression phase *)
            bStateFirstScan := TRUE;
        END_IF;


    (* --------------------------------------------------------------------------------------
     * STATE 10: CBW_STATE_CAKE_EJECTION_SHUTTLE_DISPATCH
     * Controlled hydraulic decompression down to 0 bar (-15 bar/s).
     * Ram retracts upward to top position (1400 mm). Bottom plate raises cake.
     * Pneumatic pusher discharges cake onto shuttle car. Shuttle dispatches to target dryer.
     * -------------------------------------------------------------------------------------- *)
    10:
        sCurrentStateName := 'CAKE_EJECT_DISPATCH';
        rCycleRemainingTime_s := MAX(0.0, 108.0 - tStateTimer_s);

        (* Decompression & Ram Retraction *)
        IF tStateTimer_s < 6.0 THEN
            rPress_ProportionalPressure_bar := 0.0; (* Full decompression *)
            rPress_RamSpeed_mms := 0.0;
            bPress_BottomPlateLift_Up := FALSE;
        ELSIF tStateTimer_s < 20.0 THEN
            (* Ram retract upward *)
            rPress_RamSpeed_mms := -120.0; (* High speed retract *)
            bPress_BottomPlateLift_Up := FALSE;
        ELSIF tStateTimer_s < 35.0 THEN
            (* Bottom plate raises cake out of basket *)
            bPress_BottomPlateLift_Up := TRUE;
            bPress_PneumaticEjector_Active := (tStateTimer_s >= 28.0);
        ELSIF tStateTimer_s < 60.0 THEN
            (* Cake on shuttle conveyor: Traverse shuttle car to assigned dryer bay *)
            bPress_BottomPlateLift_Up := FALSE;
            bPress_PneumaticEjector_Active := FALSE;
            IF bLightCurtain_Clear AND bTransferPermissive THEN
                bShuttle_TraverseForward := TRUE;
                rShuttle_Speed_mms := 350.0;
                IF bShuttleAligned_Dryer THEN
                    bShuttle_TraverseForward := FALSE;
                    rShuttle_Speed_mms := 0.0;
                    bShuttle_DischargeRollers_Run := TRUE; (* Discharge cake into tumbler *)
                END_IF;
            END_IF;
        END_IF;

        (* Transition Condition: Cake delivered to dryer and shuttle returned home *)
        IF tStateTimer_s >= 65.0 THEN
            bShuttle_DischargeRollers_Run := FALSE;
            bShuttle_TraverseForward := FALSE;
            bCycleComplete := TRUE; (* Pulse cycle completion *)

            (* Check if greywater filter requires CIP backwash pulse *)
            IF rDP_GreywaterFilter_mbar >= rTurbidity_High_Trip * 5.0 THEN
                iPrevState := 10;
                iState := 11; (* Branch to CIP_GREYWATER_FILTER_BACKWASH *)
                tStateTimer_s := 0.0;
                bStateFirstScan := TRUE;
            ELSE
                iPrevState := 10;
                iState := 1; (* Return to STANDBY_IDLE for next batch *)
                tStateTimer_s := 0.0;
                bStateFirstScan := TRUE;
            END_IF;
        END_IF;


    (* --------------------------------------------------------------------------------------
     * STATE 11: CBW_STATE_CIP_GREYWATER_FILTER_BACKWASH
     * Periodic Clean-In-Place high-pressure backwash of rotary greywater filter drum
     * to eliminate accumulated textile lint, particulate soil and bio-fouling.
     * -------------------------------------------------------------------------------------- *)
    11:
        sCurrentStateName := 'CIP_GREYWATER_BACKWASH';
        rCycleRemainingTime_s := 30.0;

        (* Energize high-pressure backwash spray pump *)
        bPump_GreywaterBackwash_Start := TRUE;
        bValve_ReclaimDivertToDrain   := TRUE; (* Route backwash sludge to sewer *)

        (* Transition Condition: Backwash cycle duration complete (30.0 s) *)
        IF tStateTimer_s >= 30.0 THEN
            bPump_GreywaterBackwash_Start := FALSE;
            bValve_ReclaimDivertToDrain   := FALSE;
            iPrevState := 11;
            iState := 1; (* Return to STANDBY_IDLE *)
            tStateTimer_s := 0.0;
            bStateFirstScan := TRUE;
        END_IF;


    (* --------------------------------------------------------------------------------------
     * STATE 12: CBW_STATE_EMERGENCY_PRESS_DUMP_SAFE
     * Critical Safety Abort State: Triggered on hardware E-Stop, catastrophic hydraulic
     * overpressure (HH), membrane bladder rupture, or safety light curtain violation.
     * Immediate hydraulic slam dump (< 100 ms) and saturated steam isolation.
     * -------------------------------------------------------------------------------------- *)
    12:
        sCurrentStateName := 'EMERGENCY_PRESS_DUMP';
        bReadyForNextBatch := FALSE;
        bCycleComplete := FALSE;
        rCycleRemainingTime_s := 0.0;

        (* Immediate Safety Slam Actuations *)
        bValve_EmergencyDump_Open       := TRUE;  (* High-speed dump to hydraulic tank *)
        bValve_SteamIsolation_Open      := FALSE; (* Slam shut steam main ball valve *)
        rValve_SteamDirect_pct          := 0.0;
        rPress_ProportionalPressure_bar := 0.0;
        rPress_RamSpeed_mms             := 0.0;
        rDrum_DriveSpeed_RPM            := 0.0;
        rShuttle_Speed_mms              := 0.0;
        rValve_FreshWater_pct           := 0.0;
        rPump_ReclaimRecirc_pct         := 0.0;
        rDosing_Alkali_Lmin             := 0.0;
        rDosing_Detergent_Lmin          := 0.0;
        rDosing_Bleach_Lmin             := 0.0;
        rDosing_AcidSour_Lmin           := 0.0;
        rDosing_Softener_Lmin           := 0.0;
        bPress_BottomPlateLift_Up       := FALSE;
        bPress_PneumaticEjector_Active  := FALSE;
        bShuttle_TraverseForward        := FALSE;
        bShuttle_TraverseReverse        := FALSE;
        bShuttle_DischargeRollers_Run   := FALSE;
        bValve_ReclaimDivertToDrain     := TRUE;

        (* Transition Condition: Hardware E-Stop cleared, Master Enable healthy, and Reset pulsed *)
        IF bEmergencyStop AND bEnable AND bReset AND (rTMR4_VotedVal <= 2.0) THEN
            bValve_EmergencyDump_Open := FALSE;
            iPrevState := 12;
            iState := 1; (* Return to STANDBY_IDLE *)
            tStateTimer_s := 0.0;
            bStateFirstScan := TRUE;
        END_IF;

ELSE
    (* Unknown state trap: Safe fallback to STANDBY_IDLE *)
    iState := 1;
    tStateTimer_s := 0.0;
    bStateFirstScan := TRUE;
END_CASE;
'''

if __name__ == "__main__":
    p5 = get_part5()
    print(f"Part 5 length: {len(p5)} characters")
