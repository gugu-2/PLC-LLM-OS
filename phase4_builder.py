# Phase 4 Builder for FB_Pharma_Bioprocess_TFF_Ultrafiltration_Diafiltration
import os, sys

def get_phase4_code():
    lines = []
    lines.append("""(*
====================================================================================================
PHASE 4: DETERMINISTIC 14-STAGE BIOPROCESS PRODUCTION FINITE STATE MACHINE (FSM)
Production Sequence States:
  State 0 : SANITARY_STANDBY_AND_INTEGRITY_CHECK (Cassette Air Diffusion Hold Test)
  State 1 : WFI_FLUSH_AND_INITIAL_NWP_BASE_WATER_TEST (Pre-Use Clean Water Permeability)
  State 2 : EQUILIBRATION_BUFFER_CONDITIONING_PRIME (Formulation Buffer Priming & UV Zero)
  State 3 : PROTEIN_BULK_FEED_INTRODUCTION_RAMP (Controlled Shear Feed Loading Ramp)
  State 4 : ULTRAFILTRATION_CONCENTRATION_PHASE_1 (Concentrate Bulk mAb to 60.0 [g/L])
  State 5 : AUTOMATED_CONSTANT_VOLUME_DIAFILTRATION (7.0 DV Continuous Buffer Exchange)
  State 6 : ULTRAFILTRATION_FINAL_TARGET_CONCENTRATION (Final Target to 150.0 [g/L])
  State 7 : PRODUCT_CHILLDOWN_AND_STABILIZATION (Cold Jacket Control to 4.0 [deg C])
  State 8 : RETENTATE_RECOVERY_DRAIN_AND_WFI_CHASE (Displacement Harvest Yield > 99%)
  State 9 : AIR_BLOWDOWN_FLUID_RECOVERY_CYCLE (Low-Pressure Sterile N2 Push)
  State 10: CAUSTIC_CIP_MEMBRANE_CLEANING_RECIRCULATION (0.5M NaOH at 45.0 [deg C] Wash)
  State 11: POST_CIP_NWP_MEMBRANE_RECOVERY_EVALUATION (Membrane Recovery >= 90.0%)
  State 12: PRESERVATIVE_STORAGE_FLUSH (0.1M NaOH Cassette Preservation Fill & Seal)
  State 13: EMERGENCY_OVERPRESSURE_RUPTURE_DISC_INTERLOCK (Cat-4 Fast Hydraulic Trip)
====================================================================================================
*)

(* Master Fast Emergency Interlock Override *)
IF bEmergencyStop OR bRuptureDisc_Burst_Sensor OR bAlarm_TMP_HH THEN
    nState := 13;
    bStateInit := TRUE;
END_IF;

IF bCycleAbort AND (nState <> 13) AND (nState <> 0) THEN
    nState := 8; (* Divert to product recovery drain immediately on abort *)
    bStateInit := TRUE;
END_IF;

(* Sequence Pause Handling *)
IF bPauseCycle THEN
    bSequencePaused := TRUE;
    (* Hold Retentate in Gentle Circulation while Paused *)
    rFeedPump_Speed_Cmd_rpm := 650.0;
    rRetValve_Pos_Cmd_pct := 80.0;
    rBufferPump_Speed_Cmd_pct := 0.0;
    rPermValve_Pos_Cmd_pct := 0.0;
    bPermeateIsolation_Open := FALSE;
    bBufferPump_Run_Enable := FALSE;
ELSE
    bSequencePaused := FALSE;
END_IF;

IF NOT bSequencePaused THEN
    rStateTimer_s := rStateTimer_s + rCycleTime_s;
    rSubStateTimer_s := rSubStateTimer_s + rCycleTime_s;

    CASE nState OF
        (* -----------------------------------------------------------------------------------------
         * State 0: SANITARY_STANDBY_AND_INTEGRITY_CHECK
         * ----------------------------------------------------------------------------------------- *)
        0:
            IF bStateInit THEN
                nSubState := 0;
                rStateTimer_s := 0.0;
                rSubStateTimer_s := 0.0;
                bFeedPump_Run_Enable := FALSE;
                bBufferPump_Run_Enable := FALSE;
                bPermeateIsolation_Open := FALSE;
                bWFI_SupplyValve_Open := FALSE;
                bCIP_SupplyValve_Open := FALSE;
                bCIP_ReturnValve_Open := FALSE;
                bAirBlowdown_Valve_Open := FALSE;
                bProductDrain_Valve_Open := FALSE;
                bCycleComplete := FALSE;
                bStateInit := FALSE;
            END_IF;

            CASE nSubState OF
                0: (* Waiting for Operator Integrity Test Request or Auto Cycle Start *)
                    IF bIntegrityTestStart OR bAutoCycleStart THEN
                        nSubState := 1;
                        rSubStateTimer_s := 0.0;
                        rIntegrityHold_StartPress_bar := rPDT_AirDiff_Pressure_bar;
                    END_IF;

                1: (* Pre-Use Forward Flow Air Diffusion Pressure Hold Test (180 s Dwell) *)
                    IF rSubStateTimer_s >= 180.0 THEN
                        rIntegrityHold_EndPress_bar := rPDT_AirDiff_Pressure_bar;
                        (* Decay rate in mbar/min = (Delta_bar * 1000) / (Time_s / 60) *)
                        rIntegrityDecayRate_mbar_min := ((rIntegrityHold_StartPress_bar - rIntegrityHold_EndPress_bar) * 1000.0) / 3.0;
                        IF rIntegrityDecayRate_mbar_min <= 1.25 THEN
                            (* Integrity Test Passed: Proceed to Initial NWP Benchmark *)
                            nState := 1;
                            bStateInit := TRUE;
                        ELSE
                            (* Membrane Integrity Failure: Pinhole / Seal Leak Detected *)
                            bAlarm_Flux_HH := TRUE;
                            nState := 13;
                            bStateInit := TRUE;
                        END_IF;
                    END_IF;
            END_CASE;

        (* -----------------------------------------------------------------------------------------
         * State 1: WFI_FLUSH_AND_INITIAL_NWP_BASE_WATER_TEST
         * ----------------------------------------------------------------------------------------- *)
        1:
            IF bStateInit THEN
                nSubState := 0;
                rStateTimer_s := 0.0;
                rSubStateTimer_s := 0.0;
                bWFI_SupplyValve_Open := TRUE;
                bFeedPump_Run_Enable := TRUE;
                bPermeateIsolation_Open := TRUE;
                bStateInit := FALSE;
            END_IF;

            CASE nSubState OF
                0: (* Displace Cassette Storage Solution with Pure WFI (90 s) *)
                    rFeedPump_Speed_Cmd_rpm := 1200.0;
                    rRetValve_Pos_Cmd_pct := 85.0;
                    rPermValve_Pos_Cmd_pct := 80.0;
                    IF rSubStateTimer_s >= 90.0 THEN
                        nSubState := 1;
                        rSubStateTimer_s := 0.0;
                    END_IF;

                1: (* Hydraulic Stabilization at TMP = 1.00 [bar] for Baseline NWP Calculation *)
                    rTarget_TMP_bar := 1.00;
                    IF rSubStateTimer_s >= 120.0 THEN
                        (* Capture Baseline Clean Water Permeability *)
                        rCleanWaterFlux_Baseline_LMH := arrX_State[2];
                        rBaseline_NWP_LMHbar := rCalc_Current_NWP_LMHbar;
                        bWFI_SupplyValve_Open := FALSE;
                        nState := 2;
                        bStateInit := TRUE;
                    END_IF;
            END_CASE;

        (* -----------------------------------------------------------------------------------------
         * State 2: EQUILIBRATION_BUFFER_CONDITIONING_PRIME
         * ----------------------------------------------------------------------------------------- *)
        2:
            IF bStateInit THEN
                nSubState := 0;
                rStateTimer_s := 0.0;
                rSubStateTimer_s := 0.0;
                bBufferPump_Run_Enable := TRUE;
                bStateInit := FALSE;
            END_IF;

            CASE nSubState OF
                0: (* Prime Retentate Loop with Formulation Buffer (20 mM Histidine, pH 6.0) *)
                    rBufferPump_Speed_Cmd_pct := 65.0;
                    rFeedPump_Speed_Cmd_rpm := 1400.0;
                    rRetValve_Pos_Cmd_pct := 70.0;
                    rPermValve_Pos_Cmd_pct := 50.0;
                    (* Verify Retentate pH and Conductivity Equilibrium *)
                    IF (rCT_Ret_Conductivity_mScm >= 2.2) AND (rCT_Ret_Conductivity_mScm <= 2.8) AND 
                       (rpH_Ret_Sensor_pH >= 5.85) AND (rpH_Ret_Sensor_pH <= 6.15) AND 
                       (rSubStateTimer_s >= 120.0) THEN
                        nSubState := 1;
                        rSubStateTimer_s := 0.0;
                    END_IF;

                1: (* Zero Optical UV-Vis 280 nm Sensor Photometer Baseline (30 s Dwell) *)
                    rBufferPump_Speed_Cmd_pct := 0.0;
                    IF rSubStateTimer_s >= 30.0 THEN
                        nState := 3;
                        bStateInit := TRUE;
                    END_IF;
            END_CASE;

        (* -----------------------------------------------------------------------------------------
         * State 3: PROTEIN_BULK_FEED_INTRODUCTION_RAMP
         * ----------------------------------------------------------------------------------------- *)
        3:
            IF bStateInit THEN
                nSubState := 0;
                rStateTimer_s := 0.0;
                rSubStateTimer_s := 0.0;
                bPermeateIsolation_Open := FALSE; (* Permeate Closed during Bulk Protein Loading *)
                bStateInit := FALSE;
            END_IF;

            CASE nSubState OF
                0: (* Gentle Feed Pump Speed Slew Ramp to Prevent Protein Shear Ingestion *)
                    rTarget_TMP_bar := 0.75;
                    rFeedPump_Speed_Cmd_rpm := 800.0 + (rSubStateTimer_s * 15.0);
                    IF rFeedPump_Speed_Cmd_rpm > 1650.0 THEN
                        rFeedPump_Speed_Cmd_rpm := 1650.0;
                    END_IF;
                    rRetValve_Pos_Cmd_pct := 85.0;

                    (* Detect Protein Arrival in Recirculation Loop via Inline UV-Vis 280 nm *)
                    IF (arrX_State[3] >= 8.5) AND (rWT_RecircTank_kg >= 140.0) AND (rSubStateTimer_s >= 60.0) THEN
                        rInitialRecircMass_kg := rWT_RecircTank_kg;
                        rInitialHoldUpVol_L := rWT_RecircTank_kg;
                        nState := 4;
                        bStateInit := TRUE;
                    END_IF;
            END_CASE;

        (* -----------------------------------------------------------------------------------------
         * State 4: ULTRAFILTRATION_CONCENTRATION_PHASE_1
         * ----------------------------------------------------------------------------------------- *)
        4:
            IF bStateInit THEN
                nSubState := 0;
                rStateTimer_s := 0.0;
                rSubStateTimer_s := 0.0;
                bPermeateIsolation_Open := TRUE; (* Open Permeate Line for Ultrafiltration *)
                bBufferPump_Run_Enable := FALSE; (* No Buffer Addition during Concentration *)
                rTarget_TMP_bar := 1.45;
                rTarget_WallShearRate_s1 := 5500.0;
                bStateInit := FALSE;
            END_IF;

            (* Receding-Horizon MPC Modulates Feed Pump and Retentate Valve to Control TMP and Shear *)
            (* Terminate Phase 1 when Retentate Reaches Intermediate Target: e.g. 60.0 [g/L] *)
            IF (arrX_State[3] >= rTarget_UF1_Conc_gL) AND (rStateTimer_s >= 180.0) THEN
                nState := 5;
                bStateInit := TRUE;
            END_IF;

        (* -----------------------------------------------------------------------------------------
         * State 5: AUTOMATED_CONSTANT_VOLUME_DIAFILTRATION (7 DV)
         * ----------------------------------------------------------------------------------------- *)
        5:
            IF bStateInit THEN
                nSubState := 0;
                rStateTimer_s := 0.0;
                rSubStateTimer_s := 0.0;
                bBufferPump_Run_Enable := TRUE; (* Activate Continuous Diafiltration Buffer Influx *)
                rTarget_TMP_bar := 1.55;
                rTarget_WallShearRate_s1 := 6200.0;
                bStateInit := FALSE;
            END_IF;

            (* Continuous Sump Mass Balance Closed-Loop: Buffer Pump Matches Permeate Extraction Rate *)
            (* Monitor Cumulative Diafiltration Exchange Counter: Target = 7.0 [DV] *)
            IF (arrX_State[6] >= rTarget_Diafiltration_DV) AND (rStateTimer_s >= 300.0) THEN
                bBufferPump_Run_Enable := FALSE;
                rBufferPump_Speed_Cmd_pct := 0.0;
                nState := 6;
                bStateInit := TRUE;
            END_IF;

        (* -----------------------------------------------------------------------------------------
         * State 6: ULTRAFILTRATION_FINAL_TARGET_CONCENTRATION
         * ----------------------------------------------------------------------------------------- *)
        6:
            IF bStateInit THEN
                nSubState := 0;
                rStateTimer_s := 0.0;
                rSubStateTimer_s := 0.0;
                bBufferPump_Run_Enable := FALSE;
                rTarget_TMP_bar := 1.85;
                rTarget_WallShearRate_s1 := 6800.0;
                bStateInit := FALSE;
            END_IF;

            (* High-Viscosity Regime: MPC Dynamic Decoupling Enforces Constant Shear Stress *)
            (* Terminate Final Concentration when Target Drug Substance Concentration Reached *)
            IF (arrX_State[3] >= rTarget_Final_Conc_gL) AND (rStateTimer_s >= 240.0) THEN
                bPermeateIsolation_Open := FALSE; (* Permeate Sealed *)
                rPermValve_Pos_Cmd_pct := 0.0;
                nState := 7;
                bStateInit := TRUE;
            END_IF;

        (* -----------------------------------------------------------------------------------------
         * State 7: PRODUCT_CHILLDOWN_AND_STABILIZATION (4 deg C)
         * ----------------------------------------------------------------------------------------- *)
        7:
            IF bStateInit THEN
                nSubState := 0;
                rStateTimer_s := 0.0;
                rSubStateTimer_s := 0.0;
                rTarget_TMP_bar := 0.60;
                rTarget_WallShearRate_s1 := 3200.0;
                bStateInit := FALSE;
            END_IF;

            (* Low-Shear Recirculation with Active Chiller Glycol Jacket Cooling to 4.0 [deg C] *)
            IF (arrX_State[7] <= (rTarget_ChilldownTemp_degC + 0.35)) AND (rStateTimer_s >= 180.0) THEN
                nState := 8;
                bStateInit := TRUE;
            END_IF;

        (* -----------------------------------------------------------------------------------------
         * State 8: RETENTATE_RECOVERY_DRAIN_AND_WFI_CHASE
         * ----------------------------------------------------------------------------------------- *)
        8:
            IF bStateInit THEN
                nSubState := 0;
                rStateTimer_s := 0.0;
                rSubStateTimer_s := 0.0;
                bProductDrain_Valve_Open := TRUE; (* Open 3-Way Harvest Divert Valve *)
                bStateInit := FALSE;
            END_IF;

            CASE nSubState OF
                0: (* Gravity & Low-Flow Pump Drain of Primary High-Concentration Retentate (90 s) *)
                    rFeedPump_Speed_Cmd_rpm := 600.0;
                    rRetValve_Pos_Cmd_pct := 90.0;
                    IF rWT_RecircTank_kg <= 4.5 THEN
                        nSubState := 1;
                        rSubStateTimer_s := 0.0;
                        bWFI_SupplyValve_Open := TRUE; (* Introduce WFI Chase *)
                    END_IF;

                1: (* Low-Pressure WFI Buffer Chase to Displace Cassette Channel Hold-Up (> 99% Yield) *)
                    rFeedPump_Speed_Cmd_rpm := 450.0;
                    (* Terminate Chase when Inline UV Concentration Drops below 0.85 [g/L] *)
                    IF (arrX_State[3] <= 0.85) AND (rSubStateTimer_s >= 60.0) THEN
                        bWFI_SupplyValve_Open := FALSE;
                        bProductDrain_Valve_Open := FALSE;
                        nState := 9;
                        bStateInit := TRUE;
                    END_IF;
            END_CASE;

        (* -----------------------------------------------------------------------------------------
         * State 9: AIR_BLOWDOWN_FLUID_RECOVERY_CYCLE
         * ----------------------------------------------------------------------------------------- *)
        9:
            IF bStateInit THEN
                nSubState := 0;
                rStateTimer_s := 0.0;
                rSubStateTimer_s := 0.0;
                bFeedPump_Run_Enable := FALSE;
                rFeedPump_Speed_Cmd_rpm := 0.0;
                bProductDrain_Valve_Open := TRUE;
                bAirBlowdown_Valve_Open := TRUE; (* Apply 0.30 [bar] Sterile N2 Pneumatic Sweep *)
                bStateInit := FALSE;
            END_IF;

            (* 45-Second Sterile Air Sweep of Feed, Screen, and Retentate Manifolds *)
            IF rStateTimer_s >= 45.0 THEN
                bAirBlowdown_Valve_Open := FALSE;
                bProductDrain_Valve_Open := FALSE;
                IF bCIPStart OR bAutoCycleStart THEN
                    nState := 10; (* Proceed to Caustic Clean-In-Place Cycle *)
                ELSE
                    nState := 0;  (* Return to Sanitary Standby *)
                END_IF;
                bStateInit := TRUE;
            END_IF;

        (* -----------------------------------------------------------------------------------------
         * State 10: CAUSTIC_CIP_MEMBRANE_CLEANING_RECIRCULATION
         * ----------------------------------------------------------------------------------------- *)
        10:
            IF bStateInit THEN
                nSubState := 0;
                rStateTimer_s := 0.0;
                rSubStateTimer_s := 0.0;
                bCIP_SupplyValve_Open := TRUE;
                bCIP_ReturnValve_Open := TRUE;
                bFeedPump_Run_Enable := TRUE;
                bPermeateIsolation_Open := TRUE;
                bStateInit := FALSE;
            END_IF;

            CASE nSubState OF
                0: (* Fill Skid with 0.5M Sodium Hydroxide (NaOH) and Thermal Ramp to 45.0 [deg C] *)
                    rFeedPump_Speed_Cmd_rpm := 1500.0;
                    rRetValve_Pos_Cmd_pct := 60.0;
                    rPermValve_Pos_Cmd_pct := 60.0;
                    IF (arrX_State[7] >= (rTarget_CIP_Temp_degC - 1.5)) AND (rSubStateTimer_s >= 120.0) THEN
                        nSubState := 1;
                        rSubStateTimer_s := 0.0;
                    END_IF;

                1: (* High-Shear Caustic Recirculation to Hydrolyze Protein Foulant Cake (300 s) *)
                    rFeedPump_Speed_Cmd_rpm := 2400.0; (* High Wall Shear Rate: ~9,500 [s-1] *)
                    rRetValve_Pos_Cmd_pct := 55.0;
                    rPermValve_Pos_Cmd_pct := 75.0;
                    IF rSubStateTimer_s >= 300.0 THEN
                        bCIP_SupplyValve_Open := FALSE;
                        bCIP_ReturnValve_Open := FALSE;
                        nState := 11;
                        bStateInit := TRUE;
                    END_IF;
            END_CASE;

        (* -----------------------------------------------------------------------------------------
         * State 11: POST_CIP_NWP_MEMBRANE_RECOVERY_EVALUATION
         * ----------------------------------------------------------------------------------------- *)
        11:
            IF bStateInit THEN
                nSubState := 0;
                rStateTimer_s := 0.0;
                rSubStateTimer_s := 0.0;
                bWFI_SupplyValve_Open := TRUE;
                bFeedPump_Run_Enable := TRUE;
                bPermeateIsolation_Open := TRUE;
                bStateInit := FALSE;
            END_IF;

            CASE nSubState OF
                0: (* Comprehensive WFI Rinse to Neutralize Residual Caustic (pH < 7.5) *)
                    rFeedPump_Speed_Cmd_rpm := 1600.0;
                    rRetValve_Pos_Cmd_pct := 75.0;
                    rPermValve_Pos_Cmd_pct := 75.0;
                    IF (rpH_Ret_Sensor_pH <= 7.4) AND (rCT_Ret_Conductivity_mScm <= 0.015) AND (rSubStateTimer_s >= 180.0) THEN
                        nSubState := 1;
                        rSubStateTimer_s := 0.0;
                    END_IF;

                1: (* Clean Water Permeability Re-Verification at TMP = 1.00 [bar] *)
                    rTarget_TMP_bar := 1.00;
                    IF rSubStateTimer_s >= 120.0 THEN
                        rPostCIP_WaterFlux_LMH := arrX_State[2];
                        rCalc_NWPFluxRecovery_pct := (rCalc_Current_NWP_LMHbar / MAX(0.1, rBaseline_NWP_LMHbar)) * 100.0;
                        bWFI_SupplyValve_Open := FALSE;

                        IF rCalc_NWPFluxRecovery_pct >= 90.0 THEN
                            (* Membrane Regeneration Validated: Cleanliness Benchmark Satisfied *)
                            nState := 12;
                        ELSE
                            (* Inadequate Recovery: Persistent Protein Gel Layer *)
                            bAlarm_Flux_LL := TRUE;
                            nState := 10; (* Re-cycle into Caustic Wash *)
                        END_IF;
                        bStateInit := TRUE;
                    END_IF;
            END_CASE;

        (* -----------------------------------------------------------------------------------------
         * State 12: PRESERVATIVE_STORAGE_FLUSH (0.1M NaOH)
         * ----------------------------------------------------------------------------------------- *)
        12:
            IF bStateInit THEN
                nSubState := 0;
                rStateTimer_s := 0.0;
                rSubStateTimer_s := 0.0;
                bStateInit := FALSE;
            END_IF;

            CASE nSubState OF
                0: (* Prime Cassette Screen Channels with 0.1M NaOH Preservative Agent *)
                    rFeedPump_Speed_Cmd_rpm := 1100.0;
                    rRetValve_Pos_Cmd_pct := 70.0;
                    rPermValve_Pos_Cmd_pct := 65.0;
                    IF rSubStateTimer_s >= 90.0 THEN
                        (* Cassette Sanitized and Preserved: De-energize Skid Actuators *)
                        rFeedPump_Speed_Cmd_rpm := 0.0;
                        rRetValve_Pos_Cmd_pct := 0.0;
                        rPermValve_Pos_Cmd_pct := 0.0;
                        bFeedPump_Run_Enable := FALSE;
                        bPermeateIsolation_Open := FALSE;
                        bCycleComplete := TRUE;
                        nState := 0;
                        bStateInit := TRUE;
                    END_IF;
            END_CASE;

        (* -----------------------------------------------------------------------------------------
         * State 13: EMERGENCY_OVERPRESSURE_RUPTURE_DISC_INTERLOCK (Cat-4 Fast Trip)
         * ----------------------------------------------------------------------------------------- *)
        13:
            (* Sub-10ms Fast Hardwired Safety Action: Kill Feed Pump, Vent Retentate Valve *)
            rFeedPump_Speed_Cmd_rpm := 0.0;
            bFeedPump_Run_Enable := FALSE;
            rRetValve_Pos_Cmd_pct := 100.0;         (* 100% Full Open to Depressurize Skid Manifold *)
            rBufferPump_Speed_Cmd_pct := 0.0;
            bBufferPump_Run_Enable := FALSE;
            rPermValve_Pos_Cmd_pct := 0.0;          (* Permeate Isolated to Protect Filtrate Line *)
            bPermeateIsolation_Open := FALSE;
            rChillerValve_Pos_Cmd_pct := 0.0;
            bProductDrain_Valve_Open := FALSE;
            bAirBlowdown_Valve_Open := FALSE;
            bSystemTrip_Interlock := TRUE;

            (* Latch First-Out Root Cause Diagnostic Code *)
            IF NOT bFirstOut_Latched THEN
                IF bAlarm_TMP_HH THEN
                    nFirstOut_Code := 101; (* High-High TMP Overpressure Trip *)
                ELSIF bRuptureDisc_Burst_Sensor THEN
                    nFirstOut_Code := 102; (* Sanitary Rupture Disc Burst Indicating Circuit Broken *)
                ELSIF bEmergencyStop THEN
                    nFirstOut_Code := 103; (* Operator Cat-4 E-Stop Depressed *)
                ELSIF bAlarm_Shear_HH THEN
                    nFirstOut_Code := 104; (* Extreme Wall Shear Rate Protein Denaturation Trip *)
                ELSIF bAlarm_Temp_HH THEN
                    nFirstOut_Code := 105; (* Retentate Temperature Denaturation Trip *)
                ELSE
                    nFirstOut_Code := 100; (* General Unspecified Hydraulic Safety Trip *)
                END_IF;
                bFirstOut_Latched := TRUE;
            END_IF;

            (* Operator Manual Reset Verification *)
            IF bResetFault AND (NOT bEmergencyStop) AND (NOT bRuptureDisc_Burst_Sensor) AND (arrX_State[1] < 1.0) THEN
                bSystemTrip_Interlock := FALSE;
                bFirstOut_Latched := FALSE;
                nFirstOut_Code := 0;
                nState := 0;
                bStateInit := TRUE;
            END_IF;
    END_CASE;
END_IF;""")

    return "\n".join(lines)

print("Phase 4 builder ready")
