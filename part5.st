(* ==================================================================================================== *)
(* PHASE 4A: DETERMINISTIC PRODUCTION FINITE STATE MACHINE (STAGES 1 TO 7)                               *)
(* ==================================================================================================== *)
(* FSM EXECUTION & STATE TRANSITION SUPERVISOR:                                                         *)
(* Implements an ANSI/ISA-88.01 compliant deterministic sequential state engine governing pre-forming,   *)
(* robotic loading, ultra-high vacuum chamber evacuation, thermal optical validation, ram rapid approach,*)
(* and contact touch-down calibration squeeze for Titanium Ti-6Al-4V turbine disc forging.              *)
(* ==================================================================================================== *)

(* Global Master Cycle Start / Enable Permissive Check *)
IF (NOT b_EnableMasterSys) OR b_EmergencyStopDualCh_PL_e OR (NOT b_SafetyShieldInterlockClosed) THEN
    n_FSM_State := 1; (* Return to Safe Standby / Unload Stage *)
    b_AutoCycleActive := FALSE;
    b_CycleCompleteStrobe := FALSE;
    r_MainPumpSwashplateCmd_Pct := 0.0;
    b_PreFillValvesEnergized := FALSE;
    r_ActiveDecompressValveCmd_Pct := 100.0; (* Vent hydraulic header to tank *)
    r_CounterbalanceValveCmd_Pct := 100.0; (* Lock counterbalance to support ram mass *)
    r_InductionPowerCmd_kW := 0.0;
    b_InductionInverterRunEnable := FALSE;
    b_RobotLoadSequenceStartCmd := FALSE;
    b_RobotExtractForgedPartCmd := FALSE;
    b_LaserMetrologyScanTriggerCmd := FALSE;
    t_FSM_StateTimer_ms := 0.0;
    n_ActiveFSMStage := 1;
    r_CurrentStageElapsed_s := 0.0;
ELSE
    (* Accumulate State Execution Millisecond Timer *)
    t_FSM_StateTimer_ms := t_FSM_StateTimer_ms + r_CycleScanPeriod_ms;
    r_CurrentStageElapsed_s := t_FSM_StateTimer_ms * 0.001;
    n_ActiveFSMStage := n_FSM_State;
    
    (* State Transition Edge Detection *)
    IF n_FSM_State <> n_FSM_StatePrev THEN
        t_FSM_StateTimer_ms := 0.0;
        r_CurrentStageElapsed_s := 0.0;
        b_FSM_StageComplete := FALSE;
        b_FSM_StageFault := FALSE;
        n_FSM_StatePrev := n_FSM_State;
    END_IF;
    
    CASE n_FSM_State OF
        (* -------------------------------------------------------------------------------------------- *)
        (* STAGE 1: PRE-FORM ROBOTIC LOADING FROM 950 DEG C ROTARY HEARTH FURNACE                       *)
        (* -------------------------------------------------------------------------------------------- *)
        1: (* Await automatic cycle start command and verify all press entry clearances *)
            b_SystemReady := b_HydraulicPowerUnitRunning AND b_SafetyShieldInterlockClosed AND 
                             b_LowerDieEjectorRetractedLS AND b_RoboticLoaderRetractedClear AND 
                             (NOT b_GlobalFaultActive) AND (NOT b_EmergencyStopDualCh_PL_e);
            
            (* Keep Hydraulic Ram Counterbalance Locked at Top Dead Center *)
            r_CounterbalanceValveCmd_Pct := 100.0;
            r_MainPumpSwashplateCmd_Pct := 0.0;
            b_PreFillValvesEnergized := FALSE;
            r_ActiveDecompressValveCmd_Pct := 0.0;
            b_VacuumChamberDoorOpenCmd := TRUE;
            b_ArgonBackfillVentValveOpen := TRUE; (* Atmospheric pressure for robotic entry *)
            b_VacuumRoughingValveOpen := FALSE;
            b_VacuumHighVacGateValveOpen := FALSE;
            
            IF b_AutoCycleStartReq AND b_SystemReady AND b_FurnaceTransferClearance THEN
                b_AutoCycleActive := TRUE;
                b_FurnaceUnloadRequest := TRUE;
                b_RobotLoadSequenceStartCmd := TRUE;
                
                (* Check if Robot has placed heated pre-form onto lower die and cleared enclosure *)
                IF b_RoboticLoaderAtForgingPos AND (t_FSM_StateTimer_ms > 2500.0) THEN
                    b_FurnaceUnloadRequest := FALSE;
                END_IF;
                IF b_RoboticLoaderRetractedClear AND (t_FSM_StateTimer_ms > 8500.0) THEN
                    b_RobotLoadSequenceStartCmd := FALSE;
                    b_FSM_StageComplete := TRUE;
                    n_FSM_State := 2; (* Transition to Vacuum Chamber Lockup *)
                END_IF;
            ELSE
                b_FurnaceUnloadRequest := FALSE;
                b_RobotLoadSequenceStartCmd := FALSE;
            END_IF;
            
            (* Stage 1 Safety Timeout Watchdog (45.0 seconds) *)
            IF t_FSM_StateTimer_ms > 45000.0 THEN
                b_FSM_StageFault := TRUE;
                b_GlobalFaultActive := TRUE;
            END_IF;
            
        (* -------------------------------------------------------------------------------------------- *)
        (* STAGE 2: VACUUM TRANSFER CHAMBER LOCKUP & ROUGHING / TURBOMOLECULAR EVACUATION              *)
        (* -------------------------------------------------------------------------------------------- *)
        2: (* Seal vacuum lock door and evacuate chamber below 0.045 mbar to prevent Ti alpha-case *)
            b_VacuumChamberDoorOpenCmd := FALSE;
            b_ArgonBackfillVentValveOpen := FALSE;
            
            (* Allow 1.5 seconds for hydraulic mechanical door clamp seal *)
            IF t_FSM_StateTimer_ms > 1500.0 THEN
                b_VacuumRoughingValveOpen := TRUE;
            END_IF;
            
            (* Engage Turbomolecular High-Vacuum Stage once Roughing reaches 1.5 mbar *)
            IF (r_VacuumChamberPressure_mbar < 1.50) AND b_TurbomolecularPumpAtSpeed THEN
                b_VacuumHighVacGateValveOpen := TRUE;
            END_IF;
            
            (* Verify Vacuum Base Pressure Meets Aerospace Titanium AMS 4928 Spec *)
            IF (r_VacuumChamberPressure_mbar <= r_VacuumChamberTarget_mbar) AND (t_FSM_StateTimer_ms > 4000.0) THEN
                b_FSM_StageComplete := TRUE;
                n_FSM_State := 3; (* Transition to Optical Pyrometer Thermal Check *)
            END_IF;
            
            (* Stage 2 Vacuum Timeout Watchdog (25.0 seconds) *)
            IF t_FSM_StateTimer_ms > 25000.0 THEN
                b_FSM_StageFault := TRUE;
                b_GlobalFaultActive := TRUE;
            END_IF;
            
        (* -------------------------------------------------------------------------------------------- *)
        (* STAGE 3: OPTICAL PYROMETER BILLET SURFACE THERMAL UNIFORMITY VALIDATION                      *)
        (* -------------------------------------------------------------------------------------------- *)
        3: (* Measure multi-point titanium disc pre-form surface temperature prior to ram contact *)
            (* Ensure billet has not suffered excessive radiation chilling during vacuum transfer *)
            IF (r_BilletSurfacePyrometer_DegC >= 935.0) AND (r_BilletSurfacePyrometer_DegC <= 965.0) AND 
               (r_LowerDieTemp_DegC >= 940.0) AND (r_LowerDieTemp_DegC <= 960.0) THEN
                IF t_FSM_StateTimer_ms > 1200.0 THEN
                    b_FSM_StageComplete := TRUE;
                    n_FSM_State := 4; (* Transition to Induction Die Heating Power Ramp *)
                END_IF;
            ELSIF (t_FSM_StateTimer_ms > 5000.0) THEN
                (* Thermal abort: Billet out of superplastic isothermal temperature window *)
                b_FSM_StageFault := TRUE;
                b_GlobalFaultActive := TRUE;
            END_IF;
            
        (* -------------------------------------------------------------------------------------------- *)
        (* STAGE 4: UPPER DIE INDUCTION COIL MULTI-ZONE POWER RAMP & DIE STABILIZATION                  *)
        (* -------------------------------------------------------------------------------------------- *)
        4: (* Engage 1.5 MW IGBT induction inverter to bring upper die surface to exactly 950.0 deg C *)
            b_InductionInverterRunEnable := TRUE;
            
            (* Ramp induction power proportionally to thermal error *)
            IF r_TMR_VotedDieTemp_DegC < 948.0 THEN
                r_InductionPowerCmd_kW := 750.0 + ((950.0 - r_TMR_VotedDieTemp_DegC) * 50.0);
                IF r_InductionPowerCmd_kW > 1500.0 THEN
                    r_InductionPowerCmd_kW := 1500.0;
                END_IF;
            ELSIF r_TMR_VotedDieTemp_DegC > 952.0 THEN
                r_InductionPowerCmd_kW := 150.0;
            ELSE
                r_InductionPowerCmd_kW := 420.0; (* Steady-state radiation holding power [kW] *)
            END_IF;
            
            (* Verify Upper Die Isothermal Temperature Window (+/- 2.0 deg C) *)
            IF (ABS(r_TMR_VotedDieTemp_DegC - r_TargetIsothermalDieTemp_DegC) <= 2.0) AND (t_FSM_StateTimer_ms > 3000.0) THEN
                b_FSM_StageComplete := TRUE;
                n_FSM_State := 5; (* Transition to Ram Rapid Approach Stroke *)
            END_IF;
            
            (* Stage 4 Thermal Timeout Watchdog (60.0 seconds) *)
            IF t_FSM_StateTimer_ms > 60000.0 THEN
                b_FSM_StageFault := TRUE;
                b_GlobalFaultActive := TRUE;
            END_IF;
            
        (* -------------------------------------------------------------------------------------------- *)
        (* STAGE 5: RAM RAPID APPROACH STROKE (PRE-FILL VALVE GRAVITY DROP WITH COUNTERBALANCE)         *)
        (* -------------------------------------------------------------------------------------------- *)
        5: (* Open pre-fill valves, modulate counterbalance backpressure, descend ram at 180 mm/s *)
            b_PreFillValvesEnergized := TRUE;
            r_ActiveDecompressValveCmd_Pct := 0.0;
            r_MainPumpSwashplateCmd_Pct := 25.0;
            
            (* Controlled gravity drop with proportional counterbalance braking *)
            IF x_est[1] > (r_InitialBilletHeight_mm + 45.0) THEN
                (* Fast approach zone *)
                r_CounterbalanceValveCmd_Pct := 35.0;
            ELSE
                (* Deceleration approach cushion zone: soft landing buffer *)
                r_CounterbalanceValveCmd_Pct := 75.0;
                r_MainPumpSwashplateCmd_Pct := 10.0;
            END_IF;
            
            (* Transition to Contact Touch-Down Detection at 15 mm above nominal billet height *)
            IF x_est[1] <= (r_InitialBilletHeight_mm + 15.0) THEN
                b_FSM_StageComplete := TRUE;
                n_FSM_State := 6; (* Transition to Touch-Down Contact Detection *)
            END_IF;
            
            (* Stage 5 Motion Timeout Watchdog (12.0 seconds) *)
            IF t_FSM_StateTimer_ms > 12000.0 THEN
                b_FSM_StageFault := TRUE;
                b_GlobalFaultActive := TRUE;
            END_IF;
            
        (* -------------------------------------------------------------------------------------------- *)
        (* STAGE 6: TOUCH-DOWN CONTACT IMPACT DETECTION & AXIAL COORDINATE ZEROING                      *)
        (* -------------------------------------------------------------------------------------------- *)
        6: (* Close pre-fill valves, crawl ram downward at 2.5 mm/s until tonnage exceeds 150 kN *)
            b_PreFillValvesEnergized := FALSE; (* Lock main cylinders to high-pressure servo circuit *)
            r_CounterbalanceValveCmd_Pct := 65.0;
            r_MainPumpSwashplateCmd_Pct := 8.5;
            
            (* Physical Contact Threshold Detection: Tonnage > 150 kN *)
            IF (r_TMR_VotedTonnage_kN >= 150.0) OR (r_TMR_VotedHydPressure_bar >= 25.0) THEN
                (* Soft touch confirmed: Latch starting billet contact height *)
                r_ForgingStrokeStartPos_mm := x_est[1];
                b_FSM_StageComplete := TRUE;
                n_FSM_State := 7; (* Transition to Pre-Forming Calibration Squeeze *)
            END_IF;
            
            (* Stage 6 Contact Timeout Watchdog (8.0 seconds) *)
            IF t_FSM_StateTimer_ms > 8000.0 THEN
                b_FSM_StageFault := TRUE;
                b_GlobalFaultActive := TRUE;
            END_IF;
            
        (* -------------------------------------------------------------------------------------------- *)
        (* STAGE 7: PRE-FORMING CALIBRATION SQUEEZE (HUB UPSETTING TO 5,000 kN)                         *)
        (* -------------------------------------------------------------------------------------------- *)
        7: (* Initial hydraulic compression stroke: upsets central disc hub and establishes 4-point leveling *)
            b_PreFillValvesEnergized := FALSE;
            r_CounterbalanceValveCmd_Pct := 0.0; (* Full hydraulic pressing force on ram *)
            r_MainPumpSwashplateCmd_Pct := 18.0;
            
            (* Build axial tonnage up to initial hub seating force of 5,000 kN *)
            IF (r_TMR_VotedTonnage_kN >= 5000.0) AND (t_FSM_StateTimer_ms > 1500.0) THEN
                b_FSM_StageComplete := TRUE;
                n_FSM_State := 8; (* Hand off to Stage 8: Isothermal Superplastic Extrusion *)
            END_IF;
            
            (* Stage 7 Squeeze Timeout Watchdog (15.0 seconds) *)
            IF t_FSM_StateTimer_ms > 15000.0 THEN
                b_FSM_StageFault := TRUE;
                b_GlobalFaultActive := TRUE;
            END_IF;
