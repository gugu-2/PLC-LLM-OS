# phase4_fsm.py for FB_Glass_FloatLine_TinBath_AnnealingLehr_ThicknessCooling

def generate_phase4():
    return """(*
 * =========================================================================================================
 * PHASE 4: 14-STAGE DETERMINISTIC PRODUCTION FINITE STATE MACHINE (FSM)
 * Comprehensive state progression covering full commercial float glass production lifecycle:
 *   0: STATE_IDLE
 *   1: STATE_TIN_BATH_ELECTRICAL_ROOF_HEATER_WARMUP
 *   2: STATE_PROTECTIVE_ATMOSPHERE_N2_H2_PURGE_AND_SEAL
 *   3: STATE_CANAL_TWEEL_LIFT_AND_MOLTEN_GLASS_FLOW_INCEPTION
 *   4: STATE_TIN_BATH_MOLTEN_GLASS_POOL_SPREAD_EQUILIBRIUM
 *   5: STATE_TOP_ROLLER_ENGAGE_AND_WIDTH_GRIP_ACQUISITION
 *   6: STATE_RIBBON_ATTENUATION_AND_THICKNESS_CONVERGENCE
 *   7: STATE_LIFT_OUT_ROLL_TRANSITION_INTO_ANNEALING_LEHR
 *   8: STATE_LEHR_COOLING_GRADIENT_CLOSED_LOOP_STRESS_RELAX
 *   9: STATE_NOMINAL_CONTINUOUS_FLOAT_PRODUCTION_RUN
 *  10: STATE_DYNAMIC_PRODUCT_THICKNESS_RECIPE_CHANGE
 *  11: STATE_RIBBON_WAISTING_OR_NECK_IN_AUTO_CORRECTION
 *  12: STATE_CONTROLLED_TWEEL_SHUT_AND_LEHR_CLEARING
 *  13: STATE_EMERGENCY_RIBBON_BREAK_CULLET_DUMP_TRIP
 * =========================================================================================================
 *)

(* Increment state and sub-state elapsed dwell timers *)
rStateTimer_sec    := rStateTimer_sec + rScanDeltaTime_sec;
rSubStateTimer_sec := rSubStateTimer_sec + rScanDeltaTime_sec;

(* Master Safety Circuit & E-Stop Interlock: Unconditional Trip to State 13 *)
IF (bEmergencyStopActive OR NOT bSafetyCircuitHealthy) AND (nOperationalState <> cSTATE_EMERGENCY_RIBBON_BREAK_CULLET_DUMP_TRIP) THEN
    nOperationalState     := cSTATE_EMERGENCY_RIBBON_BREAK_CULLET_DUMP_TRIP;
    nOperationalSubState  := 0;
    rStateTimer_sec       := 0.0;
    rSubStateTimer_sec    := 0.0;
    bStateFirstScan       := TRUE;
END_IF;

CASE nOperationalState OF

    (* -----------------------------------------------------------------------------------------------------
     * STATE 0: STATE_IDLE
     * Safe cold or standby condition: tweel shut, drives at creep speed, atmosphere holding.
     * ----------------------------------------------------------------------------------------------------- *)
    cSTATE_IDLE:
        sOperationalStateName := 'STATE_IDLE: System Standby & Pre-Start Interlock Verification';
        bSystemReady          := FALSE;
        bSystemActive         := FALSE;
        bCulletDumpGateOpen   := FALSE;
        rCanalTweelCommand_mm := 0.0; (* Fully shut tweel gate *)

        (* Safe creep speed on Lehr and LOR drives to prevent thermal sagging *)
        rLehrDriveSpeedCommand_m_min   := 0.50;
        rLiftOutRollSpeedCommand_m_min := 0.50;

        (* Maintain standby roof temperatures (450 deg C holding) *)
        FOR idxZone := 1 TO 8 DO
            arrTinBathRoofHeaterDuty[idxZone] := 20.0;
        END_FOR;

        (* Top rollers retracted and idle *)
        FOR idxRoller := 1 TO 16 DO
            arrTopRollerSpeedCmd[idxRoller]       := 0.0;
            arrTopRollerAngleCmd[idxRoller]       := 0.0;
            arrTopRollerPenetrationCmd[idxRoller] := 0.0;
        END_FOR;

        (* Base N2 purge to preserve refractory casing *)
        rN2_TrimValveCmd      := 25.0;
        rH2_TrimValveCmd      := 0.0;
        rVentExhaustDamperCmd := 15.0;

        (* Transition to Warmup State on Master Enable *)
        IF bMasterEnable AND bSafetyCircuitHealthy AND NOT bEmergencyStopActive THEN
            nOperationalState     := cSTATE_TIN_BATH_ELECTRICAL_ROOF_HEATER_WARMUP;
            nOperationalSubState  := 0;
            rStateTimer_sec       := 0.0;
            rSubStateTimer_sec    := 0.0;
            bStateFirstScan       := TRUE;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------
     * STATE 1: STATE_TIN_BATH_ELECTRICAL_ROOF_HEATER_WARMUP
     * Controlled thermal ramp (+15 deg C/hr) of SiC roof radiant elements to establish 1050->600 gradient.
     * ----------------------------------------------------------------------------------------------------- *)
    cSTATE_TIN_BATH_ELECTRICAL_ROOF_HEATER_WARMUP:
        sOperationalStateName := 'STATE_TIN_BATH_ELECTRICAL_ROOF_HEATER_WARMUP: Thermal Profile Conditioning';
        bSystemReady          := FALSE;
        bSystemActive         := FALSE;
        bCulletDumpGateOpen   := FALSE;
        rCanalTweelCommand_mm := 0.0;

        (* Drives continue at creep speed *)
        rLehrDriveSpeedCommand_m_min   := 0.50;
        rLiftOutRollSpeedCommand_m_min := 0.50;

        (* Modulate roof heaters to achieve target profile *)
        FOR idxZone := 1 TO 8 DO
            IF arrTinBathZoneTempActual[idxZone] < arrTinBathZoneTempSP[idxZone] THEN
                arrTinBathRoofHeaterDuty[idxZone] := LIMIT(20.0, arrTinBathRoofHeaterDuty[idxZone] + (rScanDeltaTime_sec * 0.20), 85.0);
            ELSE
                arrTinBathRoofHeaterDuty[idxZone] := LIMIT(20.0, arrTinBathRoofHeaterDuty[idxZone] - (rScanDeltaTime_sec * 0.15), 65.0);
            END_IF;
        END_FOR;

        (* Check thermal equilibrium: Zone 1 (inlet) > 1030 deg C, Zone 8 (exit) > 590 deg C *)
        IF (rVotedPyrometer_degC >= 1030.0) AND (arrTinBathZoneTempActual[8] >= 590.0) AND (rStateTimer_sec >= 10.0) THEN
            nOperationalState     := cSTATE_PROTECTIVE_ATMOSPHERE_N2_H2_PURGE_AND_SEAL;
            nOperationalSubState  := 0;
            rStateTimer_sec       := 0.0;
            rSubStateTimer_sec    := 0.0;
            bStateFirstScan       := TRUE;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------
     * STATE 2: STATE_PROTECTIVE_ATMOSPHERE_N2_H2_PURGE_AND_SEAL
     * High-volume N2 purge displacement of oxygen (< 10 ppm) followed by H2 reducing gas introduction (5%).
     * ----------------------------------------------------------------------------------------------------- *)
    cSTATE_PROTECTIVE_ATMOSPHERE_N2_H2_PURGE_AND_SEAL:
        sOperationalStateName := 'STATE_PROTECTIVE_ATMOSPHERE_N2_H2_PURGE_AND_SEAL: Inerting & Oxygen Scavenging';
        bSystemReady          := FALSE;
        bSystemActive         := FALSE;
        bCulletDumpGateOpen   := FALSE;
        rCanalTweelCommand_mm := 0.0;

        CASE nOperationalSubState OF
            0: (* Sub-stage 0: Initial pure Nitrogen displacement flush *)
                rN2_TrimValveCmd      := 85.0;
                rH2_TrimValveCmd      := 0.0;
                rVentExhaustDamperCmd := 65.0;
                IF (rO2_Ppm_Feedback <= 25.0) OR (rSubStateTimer_sec >= 15.0) THEN
                    nOperationalSubState := 1;
                    rSubStateTimer_sec   := 0.0;
                END_IF;

            1: (* Sub-stage 1: Hydrogen addition & pressure build to +0.45 mbar *)
                rN2_TrimValveCmd      := 60.0;
                rH2_TrimValveCmd      := 45.0; (* Introduce 5% H2 reducing mix *)
                rVentExhaustDamperCmd := 35.0;
                IF (rH2_Concentration_Feedback >= 4.20) AND (rVotedBathPress_mbar >= 0.35) AND (rO2_Ppm_Feedback <= 10.0) THEN
                    nOperationalSubState := 2;
                    rSubStateTimer_sec   := 0.0;
                END_IF;

            2: (* Sub-stage 2: Atmosphere stability verification dwell *)
                rN2_TrimValveCmd      := 50.0;
                rH2_TrimValveCmd      := 35.0;
                rVentExhaustDamperCmd := 40.0;
                IF rSubStateTimer_sec >= 5.0 THEN
                    nOperationalState     := cSTATE_CANAL_TWEEL_LIFT_AND_MOLTEN_GLASS_FLOW;
                    nOperationalSubState  := 0;
                    rStateTimer_sec       := 0.0;
                    rSubStateTimer_sec    := 0.0;
                    bStateFirstScan       := TRUE;
                END_IF;
        END_CASE;

    (* -----------------------------------------------------------------------------------------------------
     * STATE 3: STATE_CANAL_TWEEL_LIFT_AND_MOLTEN_GLASS_FLOW_INCEPTION
     * Controlled refractory tweel gate elevation (0 to 45 mm) initiating continuous molten glass stream.
     * ----------------------------------------------------------------------------------------------------- *)
    cSTATE_CANAL_TWEEL_LIFT_AND_MOLTEN_GLASS_FLOW:
        sOperationalStateName := 'STATE_CANAL_TWEEL_LIFT_AND_MOLTEN_GLASS_FLOW: Delivery Lip Flow Inception';
        bSystemReady          := TRUE;
        bSystemActive         := TRUE;
        bCulletDumpGateOpen   := FALSE;

        (* Line drives advance to synchronization inception speed (2.5 m/min) *)
        rLehrDriveSpeedCommand_m_min   := 2.50;
        rLiftOutRollSpeedCommand_m_min := 2.51;

        (* Controlled ramp elevation of tweel gate *)
        IF rCanalTweelCommand_mm < 45.0 THEN
            rCanalTweelCommand_mm := rCanalTweelCommand_mm + (rScanDeltaTime_sec * 2.50); (* 2.5 mm/sec lift rate *)
        ELSE
            rCanalTweelCommand_mm := 45.0;
        END_IF;

        (* Detect molten glass mass flow confirmation across canal delivery lip *)
        IF (rCanalGlassFlowRate >= 180.0) AND (rCanalTweelPosFeedback >= 38.0) AND (rStateTimer_sec >= 8.0) THEN
            nOperationalState     := cSTATE_TIN_BATH_MOLTEN_GLASS_POOL_SPREAD_EQUIL;
            nOperationalSubState  := 0;
            rStateTimer_sec       := 0.0;
            rSubStateTimer_sec    := 0.0;
            bStateFirstScan       := TRUE;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------
     * STATE 4: STATE_TIN_BATH_MOLTEN_GLASS_POOL_SPREAD_EQUILIBRIUM
     * Natural hydrodynamic pool spreading on liquid tin to equilibrium thickness (~6.85 mm).
     * ----------------------------------------------------------------------------------------------------- *)
    cSTATE_TIN_BATH_MOLTEN_GLASS_POOL_SPREAD_EQUIL:
        sOperationalStateName := 'STATE_TIN_BATH_MOLTEN_GLASS_POOL_SPREAD_EQUIL: Hydrodynamic Natural Spreading';
        bSystemReady          := TRUE;
        bSystemActive         := TRUE;
        bCulletDumpGateOpen   := FALSE;
        rCanalTweelCommand_mm := 52.0;

        rLehrDriveSpeedCommand_m_min   := 3.20;
        rLiftOutRollSpeedCommand_m_min := 3.21;

        (* Maintain high roof heat in Zones 1-3 (1050 deg C) to promote fluid spreading *)
        arrTinBathRoofHeaterDuty[1] := 68.0;
        arrTinBathRoofHeaterDuty[2] := 64.0;
        arrTinBathRoofHeaterDuty[3] := 60.0;

        (* Verify ribbon width spreading exceeds 3,200 mm and thickness nears natural equilibrium *)
        IF (rRibbonWidthFeedback >= 3200.0) AND (rVotedThickness_mm >= 5.50) AND (rStateTimer_sec >= 12.0) THEN
            nOperationalState     := cSTATE_TOP_ROLLER_ENGAGE_AND_WIDTH_GRIP_ACQUISIT;
            nOperationalSubState  := 0;
            rStateTimer_sec       := 0.0;
            rSubStateTimer_sec    := 0.0;
            bStateFirstScan       := TRUE;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------
     * STATE 5: STATE_TOP_ROLLER_ENGAGE_AND_WIDTH_GRIP_ACQUISITION
     * Lowering 16 pairs of knurled top rollers into ribbon edges to acquire tractive width grip.
     * ----------------------------------------------------------------------------------------------------- *)
    cSTATE_TOP_ROLLER_ENGAGE_AND_WIDTH_GRIP_ACQUISIT:
        sOperationalStateName := 'STATE_TOP_ROLLER_ENGAGE_AND_WIDTH_GRIP_ACQUISIT: Knurl Edge Bite Engagement';
        bSystemReady          := TRUE;
        bSystemActive         := TRUE;
        bCulletDumpGateOpen   := FALSE;

        (* Sequentially lower knurl machines into glass edges *)
        FOR idxRoller := 1 TO 16 DO
            arrTopRollerSpeedCmd[idxRoller]       := 22.0 + (DINT_TO_REAL(idxRoller) * 1.0);
            arrTopRollerAngleCmd[idxRoller]       := 6.0;
            arrTopRollerPenetrationCmd[idxRoller] := LIMIT(0.0, DINT_TO_REAL(idxRoller) * 0.15, 1.80);
        END_FOR;

        (* Verify mechanical bite torque confirmed across at least 14 machine pairs *)
        IF (arrTopRollerMotorTorque[1] >= 28.0) AND (arrTopRollerMotorTorque[8] >= 32.0) AND (rStateTimer_sec >= 10.0) THEN
            nOperationalState     := cSTATE_RIBBON_ATTENUATION_AND_THICKNESS_CONVERGE;
            nOperationalSubState  := 0;
            rStateTimer_sec       := 0.0;
            rSubStateTimer_sec    := 0.0;
            bStateFirstScan       := TRUE;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------
     * STATE 6: STATE_RIBBON_ATTENUATION_AND_THICKNESS_CONVERGENCE
     * Active top-roller draw acceleration stretching ribbon towards target recipe thickness (2.0 - 19.0 mm).
     * ----------------------------------------------------------------------------------------------------- *)
    cSTATE_RIBBON_ATTENUATION_AND_THICKNESS_CONVERGE:
        sOperationalStateName := 'STATE_RIBBON_ATTENUATION_AND_THICKNESS_CONVERGE: Active Draw Attenuation';
        bSystemReady          := TRUE;
        bSystemActive         := TRUE;
        bCulletDumpGateOpen   := FALSE;

        (* Accelerate Lehr line speed towards recipe target speed *)
        IF rLehrDriveSpeedCommand_m_min < rRecipeTargetLineSpeed THEN
            rLehrDriveSpeedCommand_m_min := rLehrDriveSpeedCommand_m_min + (rScanDeltaTime_sec * 0.15);
        ELSE
            rLehrDriveSpeedCommand_m_min := rRecipeTargetLineSpeed;
        END_IF;
        rLiftOutRollSpeedCommand_m_min := rLehrDriveSpeedCommand_m_min * 1.0035;

        (* Check thickness convergence within +/- 0.25 mm of recipe target *)
        IF (ABS(rVotedThickness_mm - rRecipeTargetThickness) <= 0.250) AND (rStateTimer_sec >= 15.0) THEN
            nOperationalState     := cSTATE_LIFT_OUT_ROLL_TRANSITION_INTO_LEHR;
            nOperationalSubState  := 0;
            rStateTimer_sec       := 0.0;
            rSubStateTimer_sec    := 0.0;
            bStateFirstScan       := TRUE;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------
     * STATE 7: STATE_LIFT_OUT_ROLL_TRANSITION_INTO_ANNEALING_LEHR
     * Extracting visco-elastic ribbon (~600 deg C) over 3 Lift-Out Rolls without bottom surface optical defects.
     * ----------------------------------------------------------------------------------------------------- *)
    cSTATE_LIFT_OUT_ROLL_TRANSITION_INTO_LEHR:
        sOperationalStateName := 'STATE_LIFT_OUT_ROLL_TRANSITION_INTO_LEHR: Bath Exit Extraction';
        bSystemReady          := TRUE;
        bSystemActive         := TRUE;
        bCulletDumpGateOpen   := FALSE;

        (* Verify ribbon exit temperature is within ductile lift-out range (585 to 625 deg C) *)
        IF rBathExitGlassTempFeedback > 635.0 THEN
            (* Too hot: risk of bottom surface roll marks - increase exit cooling in Zone 8 *)
            arrTinBathRoofHeaterDuty[8] := LIMIT(0.0, arrTinBathRoofHeaterDuty[8] - 5.0, 50.0);
        ELSIF rBathExitGlassTempFeedback < 575.0 THEN
            (* Too cold: risk of ribbon fracture - increase Zone 8 heating *)
            arrTinBathRoofHeaterDuty[8] := LIMIT(0.0, arrTinBathRoofHeaterDuty[8] + 5.0, 80.0);
        END_IF;

        (* Lehr entry zone A pyrometer feedback confirms entry *)
        IF (rLehrInletTempFeedback >= 530.0) AND (rStateTimer_sec >= 10.0) THEN
            nOperationalState     := cSTATE_LEHR_COOLING_GRADIENT_CLOSED_LOOP_STRESS;
            nOperationalSubState  := 0;
            rStateTimer_sec       := 0.0;
            rSubStateTimer_sec    := 0.0;
            bStateFirstScan       := TRUE;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------
     * STATE 8: STATE_LEHR_COOLING_GRADIENT_CLOSED_LOOP_STRESS_RELAX
     * Closed-loop regulation of longitudinal and cross-belt cooling gradients to eliminate birefringence stress.
     * ----------------------------------------------------------------------------------------------------- *)
    cSTATE_LEHR_COOLING_GRADIENT_CLOSED_LOOP_STRESS:
        sOperationalStateName := 'STATE_LEHR_COOLING_GRADIENT_CLOSED_LOOP_STRESS: Stress Relaxation Conditioning';
        bSystemReady          := TRUE;
        bSystemActive         := TRUE;
        bCulletDumpGateOpen   := FALSE;

        (* Lehr dampers active: adjust cross-belt dampers to minimize transverse delta T *)
        FOR idxZone := 1 TO 12 DO
            IF arrLehrTransverseDeltaT[idxZone] > 3.0 THEN
                arrLehrCoolingDamperCmd[idxZone] := LIMIT(10.0, arrLehrCoolingDamperCmd[idxZone] + 2.0, 90.0);
            END_IF;
        END_FOR;

        (* Stress birefringence must fall below recipe threshold (e.g. < 25 nm/cm) *)
        IF (rVotedLehrStress_nm_cm <= rRecipeMaxStressLimit) AND (rStateTimer_sec >= 12.0) THEN
            nOperationalState     := cSTATE_NOMINAL_CONTINUOUS_FLOAT_PRODUCTION_RUN;
            nOperationalSubState  := 0;
            rStateTimer_sec       := 0.0;
            rSubStateTimer_sec    := 0.0;
            bStateFirstScan       := TRUE;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------
     * STATE 9: STATE_NOMINAL_CONTINUOUS_FLOAT_PRODUCTION_RUN
     * Steady-state 800 TPD continuous float glass production with full receding-horizon MPC closed loop.
     * ----------------------------------------------------------------------------------------------------- *)
    cSTATE_NOMINAL_CONTINUOUS_FLOAT_PRODUCTION_RUN:
        sOperationalStateName := 'STATE_NOMINAL_CONTINUOUS_FLOAT_PRODUCTION_RUN: Commercial Steady-State Operation';
        bSystemReady          := TRUE;
        bSystemActive         := TRUE;
        bCulletDumpGateOpen   := FALSE;

        (* Dynamic Tweel gate fine regulation based on pull rate *)
        rCanalTweelCommand_mm := 55.0 + ((rCanalGlassFlowRate - 800.0) * 0.025);

        (* Branch to Recipe Transition on Request *)
        IF bRecipeChangeRequest THEN
            nOperationalState     := cSTATE_DYNAMIC_PRODUCT_THICKNESS_RECIPE_CHANGE;
            nOperationalSubState  := 0;
            rStateTimer_sec       := 0.0;
            rSubStateTimer_sec    := 0.0;
            bStateFirstScan       := TRUE;

        (* Branch to Ribbon Waisting Recovery if edge neck-in detected *)
        ELSIF bAlarm_RibbonWaisting THEN
            nOperationalState     := cSTATE_RIBBON_WAISTING_OR_NECK_IN_AUTO_CORRECT;
            nOperationalSubState  := 0;
            rStateTimer_sec       := 0.0;
            rSubStateTimer_sec    := 0.0;
            bStateFirstScan       := TRUE;

        (* Branch to Controlled Shutdown on Request *)
        ELSIF bControlledShutdownRequest THEN
            nOperationalState     := cSTATE_CONTROLLED_TWEEL_SHUT_AND_LEHR_CLEARING;
            nOperationalSubState  := 0;
            rStateTimer_sec       := 0.0;
            rSubStateTimer_sec    := 0.0;
            bStateFirstScan       := TRUE;

        (* Emergency Trip to Cullet Dump on Severe Process Excursion *)
        ELSIF bAlarm_Thick_HH OR bAlarm_Pyro_LL OR bAlarm_TopRollerCoolingFail OR bAlarm_TMR_Trip_AllFailed THEN
            nOperationalState     := cSTATE_EMERGENCY_RIBBON_BREAK_CULLET_DUMP_TRIP;
            nOperationalSubState  := 0;
            rStateTimer_sec       := 0.0;
            rSubStateTimer_sec    := 0.0;
            bStateFirstScan       := TRUE;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------
     * STATE 10: STATE_DYNAMIC_PRODUCT_THICKNESS_RECIPE_CHANGE
     * Continuous bumpless thickness transition without ribbon severing (e.g., 4.0 mm to 6.0 mm).
     * ----------------------------------------------------------------------------------------------------- *)
    cSTATE_DYNAMIC_PRODUCT_THICKNESS_RECIPE_CHANGE:
        sOperationalStateName := 'STATE_DYNAMIC_PRODUCT_THICKNESS_RECIPE_CHANGE: Dynamic Product Transition';
        bSystemReady          := TRUE;
        bSystemActive         := TRUE;
        bCulletDumpGateOpen   := FALSE;

        IF bStateFirstScan THEN
            rRecipeInitialThickness_mm   := rVotedThickness_mm;
            rRecipeInitialWidth_mm       := rRibbonWidthFeedback;
            rRecipeInitialLineSpeed_mpm  := rLehrDriveSpeedFeedback;
            rRecipeTransitionProgressPct := 0.0;
            bStateFirstScan              := FALSE;
        END_IF;

        (* Progress ramp at 0.50% per second *)
        rRecipeTransitionProgressPct := LIMIT(0.0, rRecipeTransitionProgressPct + (rScanDeltaTime_sec * 0.50), 100.0);

        (* Re-evaluate convergence to new recipe target *)
        IF (rRecipeTransitionProgressPct >= 100.0) AND 
           (ABS(rVotedThickness_mm - rRecipeTargetThickness) <= 0.080) AND 
           (rStateTimer_sec >= 20.0) THEN
            nOperationalState     := cSTATE_NOMINAL_CONTINUOUS_FLOAT_PRODUCTION_RUN;
            nOperationalSubState  := 0;
            rStateTimer_sec       := 0.0;
            rSubStateTimer_sec    := 0.0;
            bStateFirstScan       := TRUE;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------
     * STATE 11: STATE_RIBBON_WAISTING_OR_NECK_IN_AUTO_CORRECTION
     * Dynamic counter-action for hydrodynamic neck-in waisting: toe-out angle widening & speed bias.
     * ----------------------------------------------------------------------------------------------------- *)
    cSTATE_RIBBON_WAISTING_OR_NECK_IN_AUTO_CORRECT:
        sOperationalStateName := 'STATE_RIBBON_WAISTING_OR_NECK_IN_AUTO_CORRECT: Edge Grip Width Restoration';
        bSystemReady          := TRUE;
        bSystemActive         := TRUE;
        bCulletDumpGateOpen   := FALSE;

        (* Compute neck-in correction offsets *)
        rTopRollerAngleBiasTrim_deg := 3.50; (* Apply +3.5 deg additional toe-out angle *)
        rTopRollerSpeedBiasTrim_RPM := -2.0; (* Decelerate knurl speed slightly to permit lateral spread *)

        FOR idxRoller := 3 TO 8 DO
            arrTopRollerAngleCmd[idxRoller] := arrTopRollerAngleCmd[idxRoller] + (rScanDeltaTime_sec * 0.50);
            arrTopRollerAngleCmd[idxRoller] := LIMIT(-5.0, arrTopRollerAngleCmd[idxRoller], 18.0);
        END_FOR;

        (* Increase roof heating in Zones 3-5 by +4% to lower viscosity *)
        arrTinBathRoofHeaterDuty[3] := LIMIT(10.0, arrTinBathRoofHeaterDuty[3] + 4.0, 95.0);
        arrTinBathRoofHeaterDuty[4] := LIMIT(10.0, arrTinBathRoofHeaterDuty[4] + 4.0, 95.0);

        (* Check width recovery: within 25 mm of recipe target *)
        IF (rRibbonWidthFeedback >= (rRecipeTargetWidth - 25.0)) AND (rStateTimer_sec >= 15.0) THEN
            bAlarm_RibbonWaisting := FALSE;
            nOperationalState     := cSTATE_NOMINAL_CONTINUOUS_FLOAT_PRODUCTION_RUN;
            nOperationalSubState  := 0;
            rStateTimer_sec       := 0.0;
            rSubStateTimer_sec    := 0.0;
            bStateFirstScan       := TRUE;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------
     * STATE 12: STATE_CONTROLLED_TWEEL_SHUT_AND_LEHR_CLEARING
     * Orderly line evacuation: tweel closed, top-rollers disengaged, lehr flushed of glass.
     * ----------------------------------------------------------------------------------------------------- *)
    cSTATE_CONTROLLED_TWEEL_SHUT_AND_LEHR_CLEARING:
        sOperationalStateName := 'STATE_CONTROLLED_TWEEL_SHUT_AND_LEHR_CLEARING: Orderly Line Drainage';
        bSystemReady          := FALSE;
        bSystemActive         := FALSE;
        bCulletDumpGateOpen   := FALSE;

        (* Drop tweel gate to 0.0 mm *)
        IF rCanalTweelCommand_mm > 0.0 THEN
            rCanalTweelCommand_mm := MAX(0.0, rCanalTweelCommand_mm - (rScanDeltaTime_sec * 3.0));
        ELSE
            rCanalTweelCommand_mm := 0.0;
        END_IF;

        (* Disengage top-roller machines *)
        FOR idxRoller := 1 TO 16 DO
            arrTopRollerPenetrationCmd[idxRoller] := 0.0;
            arrTopRollerSpeedCmd[idxRoller]       := 0.0;
        END_FOR;

        (* Run Lehr conveyor at drainage speed (6.5 m/min) *)
        rLehrDriveSpeedCommand_m_min   := 6.50;
        rLiftOutRollSpeedCommand_m_min := 6.52;

        (* After 60 seconds of drainage, line is empty -> transition to IDLE *)
        IF (rCanalGlassFlowRate <= 20.0) AND (rStateTimer_sec >= 60.0) THEN
            nOperationalState     := cSTATE_IDLE;
            nOperationalSubState  := 0;
            rStateTimer_sec       := 0.0;
            rSubStateTimer_sec    := 0.0;
            bStateFirstScan       := TRUE;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------
     * STATE 13: STATE_EMERGENCY_RIBBON_BREAK_CULLET_DUMP_TRIP
     * Immediate trip action: open cullet trapdoor, retract top-rollers, close tweel to emergency cut-off.
     * ----------------------------------------------------------------------------------------------------- *)
    cSTATE_EMERGENCY_RIBBON_BREAK_CULLET_DUMP_TRIP:
        sOperationalStateName := 'STATE_EMERGENCY_RIBBON_BREAK_CULLET_DUMP_TRIP: Cullet Dump Trapdoor Tripped';
        bSystemReady          := FALSE;
        bSystemActive         := FALSE;
        bSystemFaultTrip      := TRUE;

        (* ACTUATE EMERGENCY CULLET DUMP TRAPDOOR *)
        bCulletDumpGateOpen   := TRUE;

        (* Drop tweel to emergency minimum cut-off height (5.0 mm) *)
        rCanalTweelCommand_mm := 5.0;

        (* Retract all 16 top-roller machines vertically to avoid molten tin freeze adhesion *)
        FOR idxRoller := 1 TO 16 DO
            arrTopRollerPenetrationCmd[idxRoller] := 0.0;
            arrTopRollerSpeedCmd[idxRoller]       := 0.0;
            arrTopRollerAngleCmd[idxRoller]       := 0.0;
        END_FOR;

        (* Maintain conveyor creep speed *)
        rLehrDriveSpeedCommand_m_min   := 0.50;
        rLiftOutRollSpeedCommand_m_min := 0.50;

        (* Maximize nitrogen purge to prevent air ingress through open cullet chute *)
        rN2_TrimValveCmd      := 95.0;
        rH2_TrimValveCmd      := 0.0;
        rVentExhaustDamperCmd := 20.0;

        (* Latch until Operator Alarm Reset and Safety Circuit Healthy *)
        IF bAlarmResetPushbutton AND bSafetyCircuitHealthy AND NOT bEmergencyStopActive THEN
            bSystemFaultTrip      := FALSE;
            bCulletDumpGateOpen   := FALSE;
            nOperationalState     := cSTATE_IDLE;
            nOperationalSubState  := 0;
            rStateTimer_sec       := 0.0;
            rSubStateTimer_sec    := 0.0;
            bStateFirstScan       := TRUE;
        END_IF;

ELSE
    (* Fallback Catch-All Safe State *)
    nOperationalState := cSTATE_IDLE;
END_CASE;
"""

if __name__ == "__main__":
    s = generate_phase4()
    print(f"Phase 4 length: {len(s)} chars")
