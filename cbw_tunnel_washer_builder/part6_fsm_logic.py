# cbw_tunnel_washer_builder/part6_fsm_logic.py
# Deterministic 14-Stage Production Finite State Machine (FSM)

def get_part6_fsm_logic():
    return """(* ==================================================================================================== *)
(* PHASE 4: DETERMINISTIC 14-STAGE PRODUCTION FINITE STATE MACHINE (FSM)                                *)
(* ==================================================================================================== *)

(* -------------------------------------------------------------------------------------------------- *)
(* MASTER EMERGENCY TRIP & FAULT OVERRIDE INTERLOCKS                                                  *)
(* -------------------------------------------------------------------------------------------------- *)
IF NOT bEmergencyStop THEN
    (* Immediate Safety Shutoff upon Hardwired E-Stop Break *)
    bSystemRunning := FALSE;
    bSystemReady := FALSE;
    bSequenceFault := TRUE;
    nFsmState := 0; (* Reset to Standby *)
    rMainWashSteamValveCmd_pct := 0.0;
    rBleachSteamValveCmd_pct := 0.0;
    rFreshwaterMakeupValveCmd_pct := 0.0;
    rCounterFlowRecircPumpCmd_pct := 0.0;
    rPressHydraulicServoCmd_bar := 0.0;
    rPressRamDirectionCmd := -1; (* Retract Ram to TDC *)
    rDrumDriveSpeedCmd_rpm := 0.0;
    rAlkaliDosingPumpCmd_ml := 0.0;
    rDetergentDosingPumpCmd_ml := 0.0;
    rBleachDosingPumpCmd_ml := 0.0;
    rAcidSouringDosingPumpCmd_ml := 0.0;
    bSteamHeaderIsolationValveCmd := FALSE; (* Trip Steam Off *)
    bEmergencyWaterDumpValveCmd := TRUE;    (* Open Emergency Water Dump *)
ELSIF bSequenceFault THEN
    (* Process Fault Latched: Require Operator Reset *)
    bSystemRunning := FALSE;
    rMainWashSteamValveCmd_pct := 0.0;
    rBleachSteamValveCmd_pct := 0.0;
    rFreshwaterMakeupValveCmd_pct := 0.0;
    rCounterFlowRecircPumpCmd_pct := 0.0;
    rPressHydraulicServoCmd_bar := 0.0;
    rDrumDriveSpeedCmd_rpm := 0.0;
    bSteamHeaderIsolationValveCmd := FALSE;
    IF bResetFault THEN
        bSequenceFault := FALSE;
        nFsmState := 0;
        tStateTimer := T#0MS;
    END_IF;
ELSE
    (* Normal Automated Sequence Execution *)
    tStateTimer := tStateTimer + tTaskCycleTime;
    bSteamHeaderIsolationValveCmd := TRUE;  (* Steam Permissive Healthy *)
    bEmergencyWaterDumpValveCmd := FALSE;   (* Dump Valve Closed *)

    CASE nFsmState OF
        (* ------------------------------------------------------------------------------------------ *)
        (* STAGE 0: STANDBY & READY INITIALIZATION                                                    *)
        (* Permissives: Drum at Home, Press at TDC, Water Buffer Level Ok, E-Stop Healthy             *)
        (* ------------------------------------------------------------------------------------------ *)
        0:
            bSystemReady := bDrumHomePosition_LS101 AND
                            bPressRamTopDeadCenter_LS301 AND
                            (rLT_901_PressRecoveryTankLvl_pct >= 20.0) AND
                            (rPT_801_SteamHeaderPress_bar >= 4.0) AND
                            NOT bDegradedSensorMode;
            bSystemRunning := FALSE;
            bDrumTransferCycleActive := FALSE;
            bDewateringPressActive := FALSE;

            (* Zero Actuator Demands in Standby *)
            rMainWashSteamValveCmd_pct := 0.0;
            rBleachSteamValveCmd_pct := 0.0;
            rFreshwaterMakeupValveCmd_pct := 0.0;
            rCounterFlowRecircPumpCmd_pct := 0.0;
            rPressHydraulicServoCmd_bar := 0.0;
            rPressRamDirectionCmd := 0;
            rDrumDriveSpeedCmd_rpm := 0.0;
            bDrumOscillateDirection := FALSE;
            rAlkaliDosingPumpCmd_ml := 0.0;
            rDetergentDosingPumpCmd_ml := 0.0;
            rBleachDosingPumpCmd_ml := 0.0;
            rAcidSouringDosingPumpCmd_ml := 0.0;
            bPressCakeEjectCmd := FALSE;
            bShuttleConveyorRunCmd := FALSE;
            bLintFilterBackwashValveCmd := FALSE;

            (* Cycle Start Trigger *)
            IF bEnable AND bStartCycle AND bSystemReady THEN
                nPrevFsmState := 0;
                nFsmState := 1; (* Advance to Cold Pre-Fill *)
                tStateTimer := T#0MS;
                bSystemRunning := TRUE;
            END_IF;

        (* ------------------------------------------------------------------------------------------ *)
        (* STAGE 1: COLD PRE-FILL & WATER NETWORK HYDRAULIC CHARGE                                    *)
        (* Fill pre-wash compartments #1-3 to baseline operating level with cold fresh water          *)
        (* ------------------------------------------------------------------------------------------ *)
        1:
            bSystemRunning := TRUE;
            rFreshwaterMakeupValveCmd_pct := 75.0;  (* Fast Fill Valve Opening *)
            rCounterFlowRecircPumpCmd_pct := 25.0;  (* Low-rate wetting purge *)
            rDrumDriveSpeedCmd_rpm := 4.5;          (* Gentle tumble wetting *)
            
            (* Drum Oscillation Logic: Alternate Direction Every 8 Seconds *)
            tOscillationTimer := tOscillationTimer + tTaskCycleTime;
            IF tOscillationTimer >= T#8000MS THEN
                bDrumOscillateDirection := NOT bDrumOscillateDirection;
                tOscillationTimer := T#0MS;
            END_IF;

            (* Transition Condition: 25 Seconds Pre-Fill Dwell or Flow Volumetric Target Met *)
            IF (tStateTimer >= T#25000MS) OR (rVotedFreshwaterFlow_m3h >= 12.0 AND tStateTimer >= T#15000MS) THEN
                nPrevFsmState := 1;
                nFsmState := 2; (* Advance to Recirculation Prime *)
                tStateTimer := T#0MS;
            END_IF;

        (* ------------------------------------------------------------------------------------------ *)
        (* STAGE 2: COUNTER-CURRENT RECIRCULATION PRIME & LINT FILTER PRE-PURGE                       *)
        (* Start high-flow counter-current cascade from rinse zone through rotary lint screen         *)
        (* ------------------------------------------------------------------------------------------ *)
        2:
            rFreshwaterMakeupValveCmd_pct := 30.0;
            rCounterFlowRecircPumpCmd_pct := 80.0;  (* High-volume cascade circulation *)
            rDrainHeatExchangerBypass_pct := 0.0;   (* Route through heat exchanger *)
            rDrumDriveSpeedCmd_rpm := 6.0;

            tOscillationTimer := tOscillationTimer + tTaskCycleTime;
            IF tOscillationTimer >= T#7000MS THEN
                bDrumOscillateDirection := NOT bDrumOscillateDirection;
                tOscillationTimer := T#0MS;
            END_IF;

            (* Check for Rotary Lint Screen Differential Pressure *)
            IF rPDT_902_LintFilterDiffPress_bar > rTrip_PDT902_H THEN
                bLintFilterBackwashValveCmd := TRUE;
            ELSE
                bLintFilterBackwashValveCmd := FALSE;
            END_IF;

            (* Transition Condition: 18 Seconds Recirculation Stabilization *)
            IF tStateTimer >= T#18000MS THEN
                nPrevFsmState := 2;
                nFsmState := 3; (* Advance to Bath Steaming Ramp *)
                tStateTimer := T#0MS;
            END_IF;

        (* ------------------------------------------------------------------------------------------ *)
        (* STAGE 3: COMPARTMENT BATH TEMPERATURE STEAMING RAMP                                        *)
        (* Direct live steam injection to reach 85 C main wash and 70 C bleach profiles              *)
        (* ------------------------------------------------------------------------------------------ *)
        3:
            (* Direct Steam Injection Proportional Valve Modulation *)
            IF rVotedMainWashTemp_degC < 84.0 THEN
                (* Proportional Ramp with Soft-Start Anti-Hammer Rate Limiting *)
                rScratchSum := (85.0 - rVotedMainWashTemp_degC) * 8.5;
                rMainWashSteamValveCmd_pct := LIMIT(10.0, rScratchSum, 95.0);
            ELSE
                (* MPC Fine Tuning in Temperature Approach Band *)
                rMainWashSteamValveCmd_pct := LIMIT(0.0, vecU_target[1], 45.0);
            END_IF;

            IF rTT_103_BleachTemp_degC < 68.0 THEN
                rScratchSum := (70.0 - rTT_103_BleachTemp_degC) * 7.0;
                rBleachSteamValveCmd_pct := LIMIT(5.0, rScratchSum, 80.0);
            ELSE
                rBleachSteamValveCmd_pct := LIMIT(0.0, vecU_target[2], 35.0);
            END_IF;

            rDrumDriveSpeedCmd_rpm := 8.0; (* Active tumbling for thermal mixing *)
            tOscillationTimer := tOscillationTimer + tTaskCycleTime;
            IF tOscillationTimer >= T#6000MS THEN
                bDrumOscillateDirection := NOT bDrumOscillateDirection;
                tOscillationTimer := T#0MS;
            END_IF;

            (* Transition Condition: Main Wash >= 84.0 C and Bleach >= 68.0 C or Timeout *)
            IF ((rVotedMainWashTemp_degC >= 84.0) AND (rTT_103_BleachTemp_degC >= 68.0)) OR (tStateTimer >= T#45000MS) THEN
                nPrevFsmState := 3;
                nFsmState := 4; (* Advance to Chemical Dosing Synchronization *)
                tStateTimer := T#0MS;
                tDosingPulseTimer := T#0MS;
            END_IF;

        (* ------------------------------------------------------------------------------------------ *)
        (* STAGE 4: CHEMICAL DOSING PULSE SYNCHRONIZATION                                             *)
        (* Micro-peristaltic injection of alkali, surfactant detergent, and emulsifiers               *)
        (* ------------------------------------------------------------------------------------------ *)
        4:
            tDosingPulseTimer := tDosingPulseTimer + tTaskCycleTime;
            
            (* Dosing Pulse Delivery Proportional to Ingested Linen Batch Weight *)
            rScratchSum := rCurrentBatchWeight_kg / 60.0; (* Scale Factor *)
            rAlkaliDosingPumpCmd_ml := 280.0 * rScratchSum;    (* Sodium Hydroxide / Silicate Solution *)
            rDetergentDosingPumpCmd_ml := 160.0 * rScratchSum; (* Non-ionic / Anionic Surfactant *)
            rBleachDosingPumpCmd_ml := 0.0;                    (* Bleach held until stage 6 *)
            rAcidSouringDosingPumpCmd_ml := 0.0;

            (* Maintain Main Wash Bath Temperature *)
            rMainWashSteamValveCmd_pct := LIMIT(0.0, vecU_target[1], 50.0);
            rDrumDriveSpeedCmd_rpm := 7.5;

            tOscillationTimer := tOscillationTimer + tTaskCycleTime;
            IF tOscillationTimer >= T#6000MS THEN
                bDrumOscillateDirection := NOT bDrumOscillateDirection;
                tOscillationTimer := T#0MS;
            END_IF;

            (* Dosing Pulse Duration: 15 Seconds Injection Phase *)
            IF tDosingPulseTimer >= T#15000MS THEN
                rAlkaliDosingPumpCmd_ml := 0.0;
                rDetergentDosingPumpCmd_ml := 0.0;
                nPrevFsmState := 4;
                nFsmState := 5; (* Advance to Main Detergent Soak *)
                tStateTimer := T#0MS;
            END_IF;

        (* ------------------------------------------------------------------------------------------ *)
        (* STAGE 5: MAIN DETERGENT SOAK & SAPONIFICATION                                              *)
        (* Thermal disinfection soak at 85 C, saponification of greases, particle soil dispersion     *)
        (* ------------------------------------------------------------------------------------------ *)
        5:
            (* Strict Thermal Disinfection Tracking via MPC Engine *)
            rMainWashSteamValveCmd_pct := vecU_target[1];
            rBleachSteamValveCmd_pct := vecU_target[2];
            rFreshwaterMakeupValveCmd_pct := 5.0; (* Minimal water makeup to prevent cooling *)
            rCounterFlowRecircPumpCmd_pct := 35.0;

            rDrumDriveSpeedCmd_rpm := 8.5; (* High mechanical action *)
            tOscillationTimer := tOscillationTimer + tTaskCycleTime;
            IF tOscillationTimer >= T#5500MS THEN
                bDrumOscillateDirection := NOT bDrumOscillateDirection;
                tOscillationTimer := T#0MS;
            END_IF;

            (* Transition Condition: 35 Seconds Main Wash Cycle Dwell Time *)
            IF tStateTimer >= T#35000MS THEN
                nPrevFsmState := 5;
                nFsmState := 6; (* Advance to Bleach Disinfection *)
                tStateTimer := T#0MS;
                tDosingPulseTimer := T#0MS;
            END_IF;

        (* ------------------------------------------------------------------------------------------ *)
        (* STAGE 6: OXYGEN BLEACH ACTIVATION & BIO-SANITIZATION                                       *)
        (* Peracetic acid / Hydrogen peroxide dosing into compartment #9, dwell at 70 C               *)
        (* ------------------------------------------------------------------------------------------ *)
        6:
            tDosingPulseTimer := tDosingPulseTimer + tTaskCycleTime;
            IF tDosingPulseTimer <= T#10000MS THEN
                rBleachDosingPumpCmd_ml := 190.0 * (rCurrentBatchWeight_kg / 60.0);
            ELSE
                rBleachDosingPumpCmd_ml := 0.0;
            END_IF;

            rMainWashSteamValveCmd_pct := vecU_target[1];
            rBleachSteamValveCmd_pct := vecU_target[2];
            rDrumDriveSpeedCmd_rpm := 7.0;

            tOscillationTimer := tOscillationTimer + tTaskCycleTime;
            IF tOscillationTimer >= T#6000MS THEN
                bDrumOscillateDirection := NOT bDrumOscillateDirection;
                tOscillationTimer := T#0MS;
            END_IF;

            (* Transition Condition: 25 Seconds Bleach Contact Period *)
            IF tStateTimer >= T#25000MS THEN
                rBleachDosingPumpCmd_ml := 0.0;
                nPrevFsmState := 6;
                nFsmState := 7; (* Advance to High-Rate Counter-Flow Rinse *)
                tStateTimer := T#0MS;
            END_IF;

        (* ------------------------------------------------------------------------------------------ *)
        (* STAGE 7: HIGH-RATE COUNTER-FLOW RINSE                                                      *)
        (* Counter-current cascade from comp 14 to comp 11, diluting alkalinity and residual soil     *)
        (* ------------------------------------------------------------------------------------------ *)
        7:
            rMainWashSteamValveCmd_pct := 0.0;
            rBleachSteamValveCmd_pct := 0.0;
            rFreshwaterMakeupValveCmd_pct := vecU_target[3];
            rCounterFlowRecircPumpCmd_pct := vecU_target[4];
            rDrainHeatExchangerBypass_pct := 0.0; (* Maximum thermal recovery to incoming water *)

            rDrumDriveSpeedCmd_rpm := 9.0; (* Intensive rinsing agitation *)
            tOscillationTimer := tOscillationTimer + tTaskCycleTime;
            IF tOscillationTimer >= T#5000MS THEN
                bDrumOscillateDirection := NOT bDrumOscillateDirection;
                tOscillationTimer := T#0MS;
            END_IF;

            (* Transition Condition: 30 Seconds Rinse Time and Conductivity Approaching Setpoint *)
            IF (tStateTimer >= T#30000MS) AND (rVotedRinseConductivity_mS <= 0.35) THEN
                nPrevFsmState := 7;
                nFsmState := 8; (* Advance to Acid Souring Rinse *)
                tStateTimer := T#0MS;
                tDosingPulseTimer := T#0MS;
            ELSIF tStateTimer >= T#42000MS THEN
                (* Souring forced on timeout even if conductivity slightly elevated *)
                nPrevFsmState := 7;
                nFsmState := 8;
                tStateTimer := T#0MS;
                tDosingPulseTimer := T#0MS;
            END_IF;

        (* ------------------------------------------------------------------------------------------ *)
        (* STAGE 8: ACID NEUTRALIZER SOURING RINSE                                                    *)
        (* Micro-injection of formic / citric acid sour into comp 15-16 to reach target pH 5.5 - 6.5  *)
        (* ------------------------------------------------------------------------------------------ *)
        8:
            tDosingPulseTimer := tDosingPulseTimer + tTaskCycleTime;
            IF tDosingPulseTimer <= T#12000MS THEN
                (* Acid souring dose proportional to pH deviation above 6.0 *)
                IF rAT_202_RinseBathPH > 6.5 THEN
                    rAcidSouringDosingPumpCmd_ml := 140.0 * (rAT_202_RinseBathPH - 6.0);
                ELSE
                    rAcidSouringDosingPumpCmd_ml := 45.0;
                END_IF;
                rSoftenerDosingPumpCmd_ml := 85.0; (* Textile softening agent *)
            ELSE
                rAcidSouringDosingPumpCmd_ml := 0.0;
                rSoftenerDosingPumpCmd_ml := 0.0;
            END_IF;

            rFreshwaterMakeupValveCmd_pct := 15.0;
            rCounterFlowRecircPumpCmd_pct := 20.0;
            rDrumDriveSpeedCmd_rpm := 6.5;

            tOscillationTimer := tOscillationTimer + tTaskCycleTime;
            IF tOscillationTimer >= T#6000MS THEN
                bDrumOscillateDirection := NOT bDrumOscillateDirection;
                tOscillationTimer := T#0MS;
            END_IF;

            (* Transition Condition: 20 Seconds Souring Dwell *)
            IF tStateTimer >= T#20000MS THEN
                rAcidSouringDosingPumpCmd_ml := 0.0;
                rSoftenerDosingPumpCmd_ml := 0.0;
                nPrevFsmState := 8;
                nFsmState := 9; (* Advance to Archimedian Screw Transfer *)
                tStateTimer := T#0MS;
                nTransferSequenceStep := 0;
            END_IF;

        (* ------------------------------------------------------------------------------------------ *)
        (* STAGE 9: ARCHIMEDIAN SCREW LINEN TRANSFER INDEXING                                         *)
        (* Continuous 360-degree rotation indexing all 16 batches forward by one compartment          *)
        (* ------------------------------------------------------------------------------------------ *)
        9:
            bDrumTransferCycleActive := TRUE;
            rMainWashSteamValveCmd_pct := 0.0;
            rBleachSteamValveCmd_pct := 0.0;
            rFreshwaterMakeupValveCmd_pct := 0.0;
            rCounterFlowRecircPumpCmd_pct := 10.0; (* Keep seals lubricated *)

            CASE nTransferSequenceStep OF
                0:
                    (* Align and Accelerate Drum in Unidirectional Transfer Rotation *)
                    bDrumOscillateDirection := FALSE; (* Forward Transfer Direction *)
                    rDrumDriveSpeedCmd_rpm := 11.5;    (* Transfer Indexing Speed *)
                    IF tStateTimer >= T#3000MS THEN
                        nTransferSequenceStep := 1;
                    END_IF;

                1:
                    (* Wait for 360-Degree Rotation & Proximity Home Switch Edge *)
                    rDrumDriveSpeedCmd_rpm := 11.5;
                    IF bDrumHomePosition_LS101 AND (tStateTimer >= T#8000MS) THEN
                        rDrumDriveSpeedCmd_rpm := 2.0; (* Decelerate *)
                        nTransferSequenceStep := 2;
                    END_IF;

                2:
                    (* Settle at Home Position *)
                    rDrumDriveSpeedCmd_rpm := 0.0;
                    IF tStateTimer >= T#12000MS THEN
                        nTransferSequenceStep := 3;
                    END_IF;

                3:
                    (* Transfer Sequence Complete *)
                    bDrumTransferCycleActive := FALSE;
                    nPrevFsmState := 9;
                    nFsmState := 10; (* Advance to Hydraulic Press Basket Load *)
                    tStateTimer := T#0MS;
            END_CASE;

            (* Safety Watchdog for Transfer Jam: Drum Torque HH Trip *)
            IF rVotedDrumTorque_Nm > rTrip_ST501_HH THEN
                bSequenceFault := TRUE;
                rDrumDriveSpeedCmd_rpm := 0.0;
            END_IF;

        (* ------------------------------------------------------------------------------------------ *)
        (* STAGE 10: HYDRAULIC CAKE PRESS EXTRACTOR TRANSFER & BASKET LOAD                            *)
        (* Discharge batch #16 linen cake into press basket, verify ram at top dead center           *)
        (* ------------------------------------------------------------------------------------------ *)
        10:
            bDrumTransferCycleActive := FALSE;
            bDewateringPressActive := TRUE;
            rDrumDriveSpeedCmd_rpm := 0.0;
            rPressRamDirectionCmd := 0; (* Hold Ram at TDC *)
            rPressHydraulicServoCmd_bar := 0.0;

            (* Verify Interlocks: Press Ram at TDC and Shuttle Conveyor Docked *)
            IF bPressRamTopDeadCenter_LS301 AND bShuttleConveyorInPosition_LS601 THEN
                (* Allow 6 Seconds for Linen Cake Gravity Chute Fall into Basket *)
                IF tStateTimer >= T#6000MS THEN
                    nPrevFsmState := 10;
                    nFsmState := 11; (* Advance to Multi-Stage High Pressure Dewatering *)
                    tStateTimer := T#0MS;
                    nDewaterSequenceStep := 0;
                    tPressRampTimer := T#0MS;
                END_IF;
            ELSE
                (* Interlock Wait: Ensure Ram is Retracted *)
                rPressRamDirectionCmd := -1; (* Retract Ram *)
            END_IF;

        (* ------------------------------------------------------------------------------------------ *)
        (* STAGE 11: MULTI-STAGE HIGH-PRESSURE DEWATERING (UP TO 50 BAR)                              *)
        (* Phase A: Low Pressure 0-5 bar air purge, Phase B: 20 bar bulk squeeze, Phase C: 50 bar max *)
        (* ------------------------------------------------------------------------------------------ *)
        11:
            bDewateringPressActive := TRUE;
            tPressRampTimer := tPressRampTimer + tTaskCycleTime;

            CASE nDewaterSequenceStep OF
                0:
                    (* Ram Rapid Advance Downward until Cake Contact *)
                    rPressRamDirectionCmd := 1; (* Extend Ram Down *)
                    rPressHydraulicServoCmd_bar := 5.0;
                    IF rVotedPressPressure_bar >= 4.5 THEN
                        nDewaterSequenceStep := 1;
                        tPressRampTimer := T#0MS;
                    ELSIF bPressRamBottomSafety_LS302 THEN
                        (* Empty Basket Over-Travel Trip *)
                        bSequenceFault := TRUE;
                        rPressRamDirectionCmd := -1;
                    END_IF;

                1:
                    (* Phase B: Medium-Pressure Compaction Ramp (Linear ramp to 20 bar) *)
                    rPressRamDirectionCmd := 1;
                    rScratchSum := 5.0 + ((tPressRampTimer / 1000.0) * 1.5);
                    rPressHydraulicServoCmd_bar := LIMIT(5.0, rScratchSum, 20.0);
                    IF tPressRampTimer >= T#10000MS THEN
                        nDewaterSequenceStep := 2;
                        tPressRampTimer := T#0MS;
                    END_IF;

                2:
                    (* Phase C: High-Pressure Extraction Ramp (Linear ramp to 50 bar) *)
                    rPressRamDirectionCmd := 1;
                    rScratchSum := 20.0 + ((tPressRampTimer / 1000.0) * 2.0);
                    rPressHydraulicServoCmd_bar := LIMIT(20.0, rScratchSum, 50.0);
                    IF (tPressRampTimer >= T#15000MS) OR (rVotedPressPressure_bar >= 49.0) THEN
                        nDewaterSequenceStep := 3;
                        tPressRampTimer := T#0MS;
                    END_IF;

                3:
                    (* Phase D: High-Pressure Dwell Hold (50.0 bar for residual moisture target) *)
                    rPressRamDirectionCmd := 1;
                    rPressHydraulicServoCmd_bar := 50.0;
                    (* Hold dwell for 22 seconds *)
                    IF tPressRampTimer >= T#22000MS THEN
                        nDewaterSequenceStep := 4;
                        tPressRampTimer := T#0MS;
                    END_IF;

                4:
                    (* Phase E: Decompression & Ram Retract to Top Dead Center *)
                    rPressHydraulicServoCmd_bar := 0.0;
                    rPressRamDirectionCmd := -1; (* Retract Ram *)
                    IF bPressRamTopDeadCenter_LS301 THEN
                        nDewaterSequenceStep := 5;
                    END_IF;

                5:
                    (* Dewatering Step Complete *)
                    nPrevFsmState := 11;
                    nFsmState := 12; (* Advance to Cake Shuttle Conveyor Egress *)
                    tStateTimer := T#0MS;
            END_CASE;

            (* Safety Interlock: Overpressure High-High Trip *)
            IF rVotedPressPressure_bar > rTrip_PT301_HH THEN
                bSequenceFault := TRUE;
                rPressRamDirectionCmd := -1; (* Retract immediately *)
                rPressHydraulicServoCmd_bar := 0.0;
            END_IF;

        (* ------------------------------------------------------------------------------------------ *)
        (* STAGE 12: CAKE SHUTTLE CONVEYOR EGRESS & MOISTURE AUDIT                                    *)
        (* Pneumatic bottom ring ejector push, shuttle conveyor advance to tumble dryer hopper        *)
        (* ------------------------------------------------------------------------------------------ *)
        12:
            rPressRamDirectionCmd := 0; (* Parked at TDC *)
            rPressHydraulicServoCmd_bar := 0.0;

            IF tStateTimer <= T#5000MS THEN
                bPressCakeEjectCmd := TRUE;     (* Engage Pneumatic Pusher Ring *)
            ELSE
                bPressCakeEjectCmd := FALSE;
            END_IF;

            IF (tStateTimer >= T#3000MS) AND bDryerStagingAvailable_DI602 THEN
                bShuttleConveyorRunCmd := TRUE; (* Transfer Cake to Dryer *)
            ELSE
                bShuttleConveyorRunCmd := FALSE;
            END_IF;

            (* Transition Condition: 14 Seconds Cake Discharge Sequence *)
            IF tStateTimer >= T#14000MS THEN
                bShuttleConveyorRunCmd := FALSE;
                bPressCakeEjectCmd := FALSE;
                bDewateringPressActive := FALSE;

                (* Increment Batch Accounting Registers *)
                nBatchCycleCounter := nBatchCycleCounter + 1;
                rAccumulatedLinenProcessed_kg := rAccumulatedLinenProcessed_kg + rCurrentBatchWeight_kg;

                nPrevFsmState := 12;
                nFsmState := 13; (* Advance to Lint Filter Backwash & Energy Recovery *)
                tStateTimer := T#0MS;
            END_IF;

        (* ------------------------------------------------------------------------------------------ *)
        (* STAGE 13: AUTOMATED LINT FILTER BACKWASH & ENERGY RECOVERY RECLAMATION                     *)
        (* Reverse-pulse high-pressure backwash of rotary screen, divert dirty wash liquor to sewer   *)
        (* ------------------------------------------------------------------------------------------ *)
        13:
            tBackwashTimer := tBackwashTimer + tTaskCycleTime;

            (* Backwash Valve Trigger if Delta P elevated or every 5th batch *)
            IF (rPDT_902_LintFilterDiffPress_bar >= rTrip_PDT902_H) OR ((nBatchCycleCounter MOD 5) = 0) THEN
                bLintFilterBackwashValveCmd := TRUE;
                rCounterFlowRecircPumpCmd_pct := 90.0; (* High flow purge *)
            ELSE
                bLintFilterBackwashValveCmd := FALSE;
                rCounterFlowRecircPumpCmd_pct := 30.0;
            END_IF;

            (* Heat Exchanger Reclaimed Thermal Duty Audit *)
            rDrainHeatExchangerBypass_pct := 0.0;

            (* Transition Condition: 12 Seconds Backwash & Reclamation Complete *)
            IF tStateTimer >= T#12000MS THEN
                bLintFilterBackwashValveCmd := FALSE;

                (* Check if Continuous Batching is Commanded to Continue or Stop *)
                IF bEnable AND NOT bStopCycle THEN
                    nPrevFsmState := 13;
                    nFsmState := 1; (* Loop back to Cold Pre-Fill for Next Batch *)
                    tStateTimer := T#0MS;
                ELSE
                    nPrevFsmState := 13;
                    nFsmState := 0; (* Return to Standby *)
                    tStateTimer := T#0MS;
                    bSystemRunning := FALSE;
                END_IF;
            END_IF;

    ELSE
        (* Invalid State Recovery Trap *)
        nFsmState := 0;
        tStateTimer := T#0MS;
    END_CASE;
END_IF;

(* Surface Active Stage to Output Interface *)
nActiveFSMStage := nFsmState;
"""
