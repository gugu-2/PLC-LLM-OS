(* ==================================================================================================== *)
(* PHASE 4B: DETERMINISTIC PRODUCTION FINITE STATE MACHINE (STAGES 8 TO 14)                              *)
(* ==================================================================================================== *)
(* FSM EXECUTION & SUPERPLASTIC DEFORMATION ENGINE:                                                     *)
(* Executes closed-loop isothermal extrusion, 100 MN coining dwell, active hydraulic decompression,     *)
(* breakaway die retract, chamber argon vent, lower die ejector lift, and 3D optical laser metrology.   *)
(* ==================================================================================================== *)

        (* -------------------------------------------------------------------------------------------- *)
        (* STAGE 8: ISOTHERMAL SUPERPLASTIC SLOW EXTRUSION STROKE (MPC STRAIN-RATE CONTROL)             *)
        (* -------------------------------------------------------------------------------------------- *)
        8: (* Primary deformation phase: Ram velocity dynamically tracked via MPC to maintain 1.0e-3 s^-1 *)
            b_PreFillValvesEnergized := FALSE;
            r_ActiveDecompressValveCmd_Pct := 0.0;
            
            (* Enable full MPC authority over pump swashplate and 4-corner leveling servo valves *)
            (* The MPC optimizer in Phase 3 writes directly to r_MainPumpSwashplateCmd_Pct and leveling valves *)
            
            (* Monitor true strain rate and ram tilt limits during severe plastic extrusion *)
            IF r_MaxCornerTiltDev_um > r_MaxAllowableRamTilt_um THEN
                (* Emergency Leveling Correction: Reduce pump swashplate to avoid die jamming *)
                r_MainPumpSwashplateCmd_Pct := r_MainPumpSwashplateCmd_Pct * 0.75;
            END_IF;
            
            (* Completion Condition: Ram reaches final disc web thickness dimension (65.0 mm) *)
            IF (x_est[1] <= (r_FinalForgedWebThickness_mm + 0.15)) OR (r_TMR_VotedTonnage_kN >= 95000.0) THEN
                b_FSM_StageComplete := TRUE;
                n_FSM_State := 9; (* Transition to Final Coining Dwell *)
            END_IF;
            
            (* Stage 8 Superplastic Deformation Timeout Watchdog (180.0 seconds) *)
            IF t_FSM_StateTimer_ms > 180000.0 THEN
                b_FSM_StageFault := TRUE;
                b_GlobalFaultActive := TRUE;
            END_IF;
            
        (* -------------------------------------------------------------------------------------------- *)
        (* STAGE 9: FINAL COINING DWELL AT 100 MN NOMINAL FORCE (GRAIN BOUNDARY RELAXATION)             *)
        (* -------------------------------------------------------------------------------------------- *)
        9: (* Hold 100,000 kN (10,000 metric tons) for 45.0 seconds to achieve 100% blade root fill *)
            (* Intensifier pump holds maximum pressure (390.0 bar) *)
            r_MainPumpSwashplateCmd_Pct := 35.0;
            r_CounterbalanceValveCmd_Pct := 0.0;
            
            (* Maintain strict isothermal die heating during dwell *)
            r_InductionPowerCmd_kW := 380.0;
            
            (* Verify Tonnage Hold at Target Coining Level *)
            IF r_TMR_VotedTonnage_kN < (r_TargetForgingTonnage_kN * 0.95) THEN
                r_MainPumpSwashplateCmd_Pct := 48.0; (* Boost pump displacement to compensate seal slip *)
            END_IF;
            
            (* 45.0 Seconds Coining Dwell Completion *)
            IF t_FSM_StateTimer_ms >= 45000.0 THEN
                b_FSM_StageComplete := TRUE;
                r_DecompressStartPress_bar := r_TMR_VotedHydPressure_bar;
                n_FSM_State := 10; (* Transition to Hydraulic Active Decompression *)
            END_IF;
            
            (* Stage 9 Dwell Timeout Watchdog (60.0 seconds) *)
            IF t_FSM_StateTimer_ms > 60000.0 THEN
                b_FSM_StageFault := TRUE;
                b_GlobalFaultActive := TRUE;
            END_IF;
            
        (* -------------------------------------------------------------------------------------------- *)
        (* STAGE 10: HYDRAULIC ACTIVE PRESSURE DECOMPRESSION RAMP (< 10 BAR SAFE LEVEL)                 *)
        (* -------------------------------------------------------------------------------------------- *)
        10: (* Controlled linear release of hydraulic stored elastic energy (Beta_oil = 16,500 bar) *)
            (* Prevents hydraulic water-hammer shock, acoustic cavitation, and pipeline rupture *)
            r_MainPumpSwashplateCmd_Pct := 0.0;
            
            (* Linear Proportional Decompression Valve Ramp: 0% to 100% over 8.5 seconds *)
            IF t_FSM_StateTimer_ms < (r_DecompressionRampTime_s * 1000.0) THEN
                r_ActiveDecompressValveCmd_Pct := (t_FSM_StateTimer_ms / (r_DecompressionRampTime_s * 1000.0)) * 100.0;
            ELSE
                r_ActiveDecompressValveCmd_Pct := 100.0;
            END_IF;
            
            (* Decompression Verification: Cylinder pressure drops below safe threshold (10.0 bar) *)
            IF (r_TMR_VotedHydPressure_bar <= 10.0) AND (t_FSM_StateTimer_ms > 3500.0) THEN
                b_FSM_StageComplete := TRUE;
                n_FSM_State := 11; (* Transition to Ram Slow Breakaway Retract *)
            END_IF;
            
            (* Stage 10 Decompression Timeout Watchdog (15.0 seconds) *)
            IF t_FSM_StateTimer_ms > 15000.0 THEN
                b_FSM_StageFault := TRUE;
                b_GlobalFaultActive := TRUE;
            END_IF;
            
        (* -------------------------------------------------------------------------------------------- *)
        (* STAGE 11: RAM SLOW BREAKAWAY RETRACT & TOP DEAD CENTER PARK                                   *)
        (* -------------------------------------------------------------------------------------------- *)
        11: (* Strip upper die from forged blisk: Slow 5 mm/s breakaway then 120 mm/s fast retract *)
            b_PreFillValvesEnergized := TRUE; (* Open pre-fill to allow oil to suck back into header *)
            r_ActiveDecompressValveCmd_Pct := 0.0;
            r_CounterbalanceValveCmd_Pct := 100.0; (* Pressurize pullback lift cylinders *)
            r_MainPumpSwashplateCmd_Pct := 30.0;
            
            (* Verify Ram Reaches Top Dead Center (TDC = 420.0 mm stroke limit) *)
            IF x_est[1] >= (r_InitialBilletHeight_mm - 5.0) THEN
                r_MainPumpSwashplateCmd_Pct := 0.0;
                b_PreFillValvesEnergized := FALSE;
                b_FSM_StageComplete := TRUE;
                n_FSM_State := 12; (* Transition to Vacuum Chamber Vent Equalization *)
            END_IF;
            
            (* Stage 11 Retract Timeout Watchdog (18.0 seconds) *)
            IF t_FSM_StateTimer_ms > 18000.0 THEN
                b_FSM_StageFault := TRUE;
                b_GlobalFaultActive := TRUE;
            END_IF;
            
        (* -------------------------------------------------------------------------------------------- *)
        (* STAGE 12: VACUUM CHAMBER VENT EQUALIZATION WITH ULTRA-HIGH PURITY ARGON GAS                   *)
        (* -------------------------------------------------------------------------------------------- *)
        12: (* Backfill vacuum chamber with 99.999% argon to atmospheric pressure (1,013 mbar) *)
            b_VacuumHighVacGateValveOpen := FALSE; (* Isolate turbomolecular pump *)
            b_VacuumRoughingValveOpen := FALSE;    (* Isolate roughing pump *)
            b_ArgonBackfillVentValveOpen := TRUE;  (* Open argon equalization valve *)
            
            (* Chamber Equalization Check: Pressure reaches atmospheric (> 980 mbar) *)
            IF (r_VacuumChamberPressure_mbar >= 980.0) AND (t_FSM_StateTimer_ms > 4500.0) THEN
                b_VacuumChamberDoorOpenCmd := TRUE; (* Open vacuum lock door for robotic unload *)
                b_FSM_StageComplete := TRUE;
                n_FSM_State := 13; (* Transition to Lower Die Ejector Pin Lift *)
            END_IF;
            
            (* Stage 12 Equalization Timeout Watchdog (20.0 seconds) *)
            IF t_FSM_StateTimer_ms > 20000.0 THEN
                b_FSM_StageFault := TRUE;
                b_GlobalFaultActive := TRUE;
            END_IF;
            
        (* -------------------------------------------------------------------------------------------- *)
        (* STAGE 13: LOWER DIE EJECTOR PIN PART LIFT (SYNCHRONIZED 4-PIN HYDRAULIC LIFTER)              *)
        (* -------------------------------------------------------------------------------------------- *)
        13: (* Lift forged titanium turbine blisk out of lower die cavity by 75.0 mm *)
            r_LowerDieEjectorHydCmd_Pct := 45.0;
            
            (* Verify Ejector Extended Limit Switch and Stroke Dimension *)
            IF b_LowerDieEjectorExtendedLS OR (r_LowerDieEjectorStroke_mm >= 70.0) THEN
                r_LowerDieEjectorHydCmd_Pct := 10.0; (* Holding pressure to support forged blisk *)
                b_FSM_StageComplete := TRUE;
                n_FSM_State := 14; (* Transition to Robotic Extraction & Metrology Scan *)
            END_IF;
            
            (* Stage 13 Ejector Timeout Watchdog (10.0 seconds) *)
            IF t_FSM_StateTimer_ms > 10000.0 THEN
                b_FSM_StageFault := TRUE;
                b_GlobalFaultActive := TRUE;
            END_IF;
            
        (* -------------------------------------------------------------------------------------------- *)
        (* STAGE 14: ROBOTIC MANIPULATOR FORGED BLISK EXTRACTION & 3D OPTICAL LASER METROLOGY SCAN     *)
        (* -------------------------------------------------------------------------------------------- *)
        14: (* Gripper extracts hot forged blisk; In-line laser scan verifies final disc web thickness *)
            b_RobotExtractForgedPartCmd := TRUE;
            
            (* Trigger In-Situ 3D Laser Metrology Profilometer Scan once part cleared from die *)
            IF b_RoboticLoaderRetractedClear AND (t_FSM_StateTimer_ms > 3500.0) THEN
                b_LaserMetrologyScanTriggerCmd := TRUE;
                r_LowerDieEjectorHydCmd_Pct := 0.0; (* Retract ejector pins *)
            END_IF;
            
            (* Dimensional Quality Validation Gate: Web thickness within +/- 0.50 mm of recipe target *)
            IF b_LaserMetrologyScanComplete THEN
                b_LaserMetrologyScanTriggerCmd := FALSE;
                b_RobotExtractForgedPartCmd := FALSE;
                
                IF ABS(r_LaserMeasuredWebThick_mm - r_FinalForgedWebThickness_mm) <= 0.50 THEN
                    b_DiscDimensionQualityPassed := TRUE;
                ELSE
                    b_DiscDimensionQualityPassed := FALSE;
                END_IF;
                
                b_CycleCompleteStrobe := TRUE;
                b_AutoCycleActive := FALSE;
                b_FSM_StageComplete := TRUE;
                n_FSM_State := 1; (* Return to Stage 1 Standby for next aerospace billet *)
            END_IF;
            
            (* Stage 14 Extraction & Metrology Timeout Watchdog (30.0 seconds) *)
            IF t_FSM_StateTimer_ms > 30000.0 THEN
                b_FSM_StageFault := TRUE;
                b_GlobalFaultActive := TRUE;
            END_IF;
            
        ELSE
            (* Safe Default Fallback for Unrecognized State Index *)
            n_FSM_State := 1;
            b_AutoCycleActive := FALSE;
    END_CASE;
END_IF;
