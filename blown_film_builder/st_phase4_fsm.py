# blown_film_builder/st_phase4_fsm.py

def get_phase4_fsm():
    return """(* ==================================================================================================== *)
(* PHASE 4: DETERMINISTIC 14-STAGE BLOWN FILM PRODUCTION FINITE STATE MACHINE (FSM)                     *)
(* Complete Supervisory Coordination: Thermal Soak, Inception, IBC Lock, 128-Zone Tuning & Abort Logic  *)
(* ==================================================================================================== *)

    (* Master Emergency Stop & Critical Sensor Fault Interlock Override *)
    IF bEmergencyStop OR bCriticalTrip THEN
        eState_Current := 13; (* Force Immediate Transition to Emergency Stop *)
    END_IF;

    CASE eState_Current OF
        (* ---------------------------------------------------------------------------------------- *)
        (* STATE 0: LINE IDLE & SYSTEM PRE-FLIGHT STANDBY                                           *)
        (* ---------------------------------------------------------------------------------------- *)
        0:
            bSystemReady := NOT bCriticalTrip AND NOT bEmergencyStop;
            bInProduction := FALSE;
            rStateTimer_s := 0.0;
            rSteadyProductionTimer_s := 0.0;

            (* Actuator Output Safe Standby Presets *)
            vecU_target[0] := 50.0;   (* Thermal Bolts at 50% Neutral Expansion *)
            vecU_target[1] := 0.0;    (* IBC Supply Blower Stopped *)
            vecU_target[2] := 0.0;    (* IBC Exhaust Blower Stopped *)
            vecU_target[3] := 0.0;    (* Air Ring Flow Valve Closed *)
            vecU_target[4] := 0.0;    (* Extruder Screws Idle *)
            vecU_target[5] := 0.0;    (* Haul-Off Line Speed Zero *)

            IF bEnable AND bStartCycle AND bSystemReady THEN
                eState_Current := 1;
                rSoakTimer_s := 0.0;
            END_IF;

        (* ---------------------------------------------------------------------------------------- *)
        (* STATE 1: DIE TOOLING & 7-EXTRUDER BARREL THERMAL SOAK EQUILIBRIUM                       *)
        (* ---------------------------------------------------------------------------------------- *)
        1:
            bSystemReady := TRUE;
            bInProduction := FALSE;
            rStateTimer_s := rStateTimer_s + tScanCycleTime_s;
            rSoakTimer_s := rSoakTimer_s + tScanCycleTime_s;

            (* Hold Safe Standby Presets During Heat Soak *)
            vecU_target[0] := 50.0;
            vecU_target[1] := 0.0;
            vecU_target[2] := 0.0;
            vecU_target[3] := 0.0;
            vecU_target[4] := 0.0;
            vecU_target[5] := 0.0;

            (* Check Thermal Equilibrium: All 7 Extruders Within +/- 4.5 [deg C] of Recipe Target *)
            IF (ABS(rExtruder_MeltTemp_A_degC - rRecipe_DieTemp_Target_degC) < 4.5) AND
               (ABS(rExtruder_MeltTemp_B_degC - rRecipe_DieTemp_Target_degC) < 4.5) AND
               (ABS(rExtruder_MeltTemp_C_degC - rRecipe_DieTemp_Target_degC) < 4.5) AND
               (ABS(rExtruder_MeltTemp_D_degC - rRecipe_DieTemp_Target_degC) < 4.5) AND
               (ABS(rExtruder_MeltTemp_E_degC - rRecipe_DieTemp_Target_degC) < 4.5) AND
               (ABS(rExtruder_MeltTemp_F_degC - rRecipe_DieTemp_Target_degC) < 4.5) AND
               (ABS(rExtruder_MeltTemp_G_degC - rRecipe_DieTemp_Target_degC) < 4.5) AND
               (rSoakTimer_s >= 60.0) THEN
                eState_Current := 2;
                rStateTimer_s := 0.0;
            END_IF;

            IF bStopCycle THEN
                eState_Current := 12;
            END_IF;

        (* ---------------------------------------------------------------------------------------- *)
        (* STATE 2: EXTRUDER SCREW START & LOW-SPEED MELT PURGE                                     *)
        (* ---------------------------------------------------------------------------------------- *)
        2:
            bSystemReady := TRUE;
            bInProduction := FALSE;
            rStateTimer_s := rStateTimer_s + tScanCycleTime_s;

            (* Gentle Extruder Start: 12.0 [RPM] Creep Speed to Build Die Pressure & Purge Tooling *)
            vecU_target[0] := 50.0;
            vecU_target[1] := 0.0;
            vecU_target[2] := 0.0;
            vecU_target[3] := 15.0;   (* Minimal Lip Cooling to Prevent Melt Sag *)
            vecU_target[4] := 12.0;   (* Creep Extrusion Screw Speed *)
            vecU_target[5] := 0.0;

            (* Transition to Inception Once Melt Pressure Builds Across Die Lip *)
            IF (rMeltPress_Die_Voted > 75.0) AND (rStateTimer_s >= 20.0) THEN
                eState_Current := 3;
                rStateTimer_s := 0.0;
                rInceptionTimer_s := 0.0;
            END_IF;

            IF bStopCycle THEN
                eState_Current := 12;
            END_IF;

        (* ---------------------------------------------------------------------------------------- *)
        (* STATE 3: BUBBLE INCEPTION & MANUAL STRING-UP INFLATION                                    *)
        (* ---------------------------------------------------------------------------------------- *)
        3:
            bSystemReady := TRUE;
            bInProduction := FALSE;
            rStateTimer_s := rStateTimer_s + tScanCycleTime_s;
            rInceptionTimer_s := rInceptionTimer_s + tScanCycleTime_s;

            (* Establish Bubble Stalk: Low Haul-Off Creep & Air Ring Stalk Stabilization *)
            vecU_target[0] := 50.0;
            vecU_target[1] := 0.0;    (* IBC Isolated During Manual String-Up *)
            vecU_target[2] := 0.0;
            vecU_target[3] := 32.0;   (* Air Ring Stalk Air Flow *)
            vecU_target[4] := 18.0;   (* Screw Speed Moderate *)
            vecU_target[5] := 15.0;   (* Haul-Off Threading Speed [m/min] *)

            (* Transition When Bubble Reaches Haul-Off Nip & Traps Air Column *)
            IF (rWebTension_HaulOff_Voted > 180.0) AND (rIBC_Diameter_Voted > 1200.0) AND (rInceptionTimer_s >= 25.0) THEN
                eState_Current := 4;
                rStateTimer_s := 0.0;
            END_IF;

            IF bStopCycle THEN
                eState_Current := 12;
            END_IF;

        (* ---------------------------------------------------------------------------------------- *)
        (* STATE 4: IBC AUTOMATIC DIAMETER ACQUISITION & AIR BALANCE                                *)
        (* ---------------------------------------------------------------------------------------- *)
        4:
            bSystemReady := TRUE;
            bInProduction := FALSE;
            rStateTimer_s := rStateTimer_s + tScanCycleTime_s;

            (* Engage Internal Bubble Cooling Blowers Under Closed-Loop Diameter Coupling *)
            vecU_target[0] := 50.0;
            vecU_target[1] := 1450.0; (* IBC Supply Blower Nominal Inception RPM *)
            vecU_target[2] := 1420.0; (* IBC Exhaust Blower Nominal Inception RPM *)
            vecU_target[3] := 42.0;   (* Air Ring Main Flow *)
            vecU_target[4] := 25.0;   (* Extruder Output Ramp *)
            vecU_target[5] := 35.0;   (* Haul-Off Speed Ramp [m/min] *)

            (* Verify Bubble Diameter Locked Near Nominal Target (within 35 mm for 15 seconds) *)
            IF (ABS(rIBC_Diameter_Voted - (rRecipe_LayFlatWidth_mm * 0.63661977)) < 35.0) AND (rStateTimer_s >= 20.0) THEN
                eState_Current := 5;
                rStateTimer_s := 0.0;
                rStabilizationTimer_s := 0.0;
            END_IF;

            IF bStopCycle THEN
                eState_Current := 12;
            END_IF;

        (* ---------------------------------------------------------------------------------------- *)
        (* STATE 5: FROST-LINE SOLIDIFICATION HEIGHT (FLH) STABILIZATION RAMP                       *)
        (* ---------------------------------------------------------------------------------------- *)
        5:
            bSystemReady := TRUE;
            bInProduction := FALSE;
            rStateTimer_s := rStateTimer_s + tScanCycleTime_s;
            rStabilizationTimer_s := rStabilizationTimer_s + tScanCycleTime_s;

            (* Ramp Production Rate: Accelerate Line Speed & Cooling Air Simultaneously *)
            vecU_target[0] := 50.0;
            vecU_target[1] := 1750.0;
            vecU_target[2] := 1720.0;
            vecU_target[3] := 58.0;   (* Enhanced Lip Cooling *)
            vecU_target[4] := 52.0;   (* Extruder Screw Acceleration *)
            vecU_target[5] := 115.0;  (* Haul-Off Line Speed Approaching Nominal [m/min] *)

            (* Solidification Freeze-Line Stabilized Within Target Window *)
            IF (ABS(rFLH_Height_Voted - rRecipe_TargetFLH_mm) < 45.0) AND (rStabilizationTimer_s >= 30.0) THEN
                eState_Current := 6;
                rStateTimer_s := 0.0;
                rGaugeCalTimer_s := 0.0;
            END_IF;

            IF bStopCycle THEN
                eState_Current := 12;
            END_IF;

        (* ---------------------------------------------------------------------------------------- *)
        (* STATE 6: ROTATING THICKNESS GAUGE SENSOR CALIBRATION                                     *)
        (* ---------------------------------------------------------------------------------------- *)
        6:
            bSystemReady := TRUE;
            bInProduction := FALSE;
            rStateTimer_s := rStateTimer_s + tScanCycleTime_s;
            rGaugeCalTimer_s := rGaugeCalTimer_s + tScanCycleTime_s;

            (* Maintain Stable Bubble Dynamics While Thickness Scanner Completes Rotational Calibration *)
            vecU_target[0] := 50.0;
            vecU_target[1] := 1850.0;
            vecU_target[2] := 1820.0;
            vecU_target[3] := 65.0;
            vecU_target[4] := 68.0;
            vecU_target[5] := rRecipe_LineSpeed_mpm;

            (* Increment Completed Gauge Scans (Simulated 360-degree rotation period ~60s) *)
            IF rGaugeCalTimer_s >= 60.0 THEN
                rGaugeScanCount := rGaugeScanCount + 1;
                rGaugeCalTimer_s := 0.0;
            END_IF;

            IF (rGaugeScanCount >= 2) AND (rStateTimer_s >= 65.0) THEN
                eState_Current := 7;
                rStateTimer_s := 0.0;
                rProfileMappingTimer_s := 0.0;
            END_IF;

            IF bStopCycle THEN
                eState_Current := 12;
            END_IF;

        (* ---------------------------------------------------------------------------------------- *)
        (* STATE 7: INITIAL PROFILE MAPPING & SPATIAL CORRELATION MATRIX                            *)
        (* ---------------------------------------------------------------------------------------- *)
        7:
            bSystemReady := TRUE;
            bInProduction := FALSE;
            rStateTimer_s := rStateTimer_s + tScanCycleTime_s;
            rProfileMappingTimer_s := rProfileMappingTimer_s + tScanCycleTime_s;

            (* Synchronize Reversing Haul-Off Oscillation With Die Frame *)
            vecU_target[0] := 50.0;
            vecU_target[1] := 1850.0;
            vecU_target[2] := 1820.0;
            vecU_target[3] := 65.0;
            vecU_target[4] := 68.0;
            vecU_target[5] := rRecipe_LineSpeed_mpm;

            (* Baseline Circumferential Thickness Mapping Completed Over 1 Full Oscillation Cycle *)
            IF rProfileMappingTimer_s >= 90.0 THEN
                eState_Current := 8;
                rStateTimer_s := 0.0;
                rAirRingConvergenceTimer_s := 0.0;
            END_IF;

            IF bStopCycle THEN
                eState_Current := 12;
            END_IF;

        (* ---------------------------------------------------------------------------------------- *)
        (* STATE 8: CLOSED-LOOP 128-ZONE SEGMENTED AIR RING CONTROL                                 *)
        (* ---------------------------------------------------------------------------------------- *)
        8:
            bSystemReady := TRUE;
            bInProduction := FALSE;
            rStateTimer_s := rStateTimer_s + tScanCycleTime_s;
            rAirRingConvergenceTimer_s := rAirRingConvergenceTimer_s + tScanCycleTime_s;

            (* Engage Full 128 Thermal Bolt Closed-Loop Profile Flattening *)
            vecU_target[0] := 50.0;
            vecU_target[1] := 1850.0;
            vecU_target[2] := 1820.0;
            vecU_target[3] := 65.0;
            vecU_target[4] := 68.0;
            vecU_target[5] := rRecipe_LineSpeed_mpm;

            (* Verification of Gauge Convergence: 2-Sigma Variation Reduced Below 4.0% *)
            IF (rProfile_2SigmaThickness_pct < 4.0) AND (rAirRingConvergenceTimer_s >= 45.0) THEN
                eState_Current := 9;
                rStateTimer_s := 0.0;
            END_IF;

            IF bStopCycle THEN
                eState_Current := 12;
            END_IF;

        (* ---------------------------------------------------------------------------------------- *)
        (* STATE 9: NOMINAL HIGH-SPEED PRODUCTION STEADY STATE                                      *)
        (* ---------------------------------------------------------------------------------------- *)
        9:
            bSystemReady := TRUE;
            bInProduction := TRUE;
            rStateTimer_s := rStateTimer_s + tScanCycleTime_s;
            rSteadyProductionTimer_s := rSteadyProductionTimer_s + tScanCycleTime_s;

            (* Full Optimal Multi-Variable Coordination *)
            vecU_target[0] := 50.0;
            vecU_target[1] := 1850.0;
            vecU_target[2] := 1820.0;
            vecU_target[3] := 65.0;
            vecU_target[4] := 68.0;
            vecU_target[5] := rRecipe_LineSpeed_mpm;

            (* Dynamic Disturbances & Transition Triggers *)
            IF bRecipeChangePending THEN
                eState_Current := 10;
                rStateTimer_s := 0.0;
                rRecipeChangeTimer_s := 0.0;
            ELSIF ABS(rIBC_Diameter_Voted - (rRecipe_LayFlatWidth_mm * 0.63661977)) > 42.0 THEN
                (* Bubble Breathing Aerodynamic Resonance Detected *)
                eState_Current := 11;
                rStateTimer_s := 0.0;
                rBreatheDampingTimer_s := 0.0;
            ELSIF bStopCycle THEN
                eState_Current := 12;
                rStateTimer_s := 0.0;
                rRampdownTimer_s := 0.0;
            ELSIF (rWebTension_HaulOff_Voted < 140.0) OR (rMeltPress_Die_Voted < 25.0) THEN
                (* Web Severance or Catastrophic Bubble Tear *)
                eState_Current := 13;
            END_IF;

        (* ---------------------------------------------------------------------------------------- *)
        (* STATE 10: DYNAMIC RECIPE WIDTH OR THICKNESS TRANSITION                                   *)
        (* ---------------------------------------------------------------------------------------- *)
        10:
            bSystemReady := TRUE;
            bInProduction := FALSE;
            rStateTimer_s := rStateTimer_s + tScanCycleTime_s;
            rRecipeChangeTimer_s := rRecipeChangeTimer_s + tScanCycleTime_s;

            (* Slew Co-Extrusion Targets Smoothly Without Dropping Bubble *)
            vecU_target[0] := 50.0;
            vecU_target[1] := 1850.0;
            vecU_target[2] := 1820.0;
            vecU_target[3] := 65.0;
            vecU_target[4] := 68.0;
            vecU_target[5] := rRecipe_LineSpeed_mpm;

            IF (rRecipeChangeTimer_s >= 60.0) AND (rProfile_2SigmaThickness_pct < 4.5) THEN
                bRecipeChangePending := FALSE;
                eState_Current := 8; (* Return to Active Profile Convergence *)
                rStateTimer_s := 0.0;
            END_IF;

            IF bStopCycle THEN
                eState_Current := 12;
            END_IF;

        (* ---------------------------------------------------------------------------------------- *)
        (* STATE 11: BUBBLE BREATHE INSTABILITY ACTIVE AERODYNAMIC DAMPING                           *)
        (* ---------------------------------------------------------------------------------------- *)
        11:
            bSystemReady := TRUE;
            bInProduction := FALSE;
            rStateTimer_s := rStateTimer_s + tScanCycleTime_s;
            rBreatheDampingTimer_s := rBreatheDampingTimer_s + tScanCycleTime_s;

            (* Dynamic Active Anti-Hunting Pressure Modulation *)
            vecU_target[0] := 50.0;
            (* Modulate IBC Exhaust Relative to Supply to Quench Volume Breathing *)
            IF rIBC_DiffPressure_Sensor_Pa > rRecipe_IBC_DiffPress_Target_Pa THEN
                vecU_target[1] := 1720.0; (* Trim Supply Down *)
                vecU_target[2] := 1950.0; (* Boost Exhaust Up *)
            ELSE
                vecU_target[1] := 1950.0; (* Boost Supply Up *)
                vecU_target[2] := 1720.0; (* Trim Exhaust Down *)
            END_IF;
            vecU_target[3] := 72.0;       (* Stiffen External Air Ring Column *)
            vecU_target[4] := 68.0;
            vecU_target[5] := rRecipe_LineSpeed_mpm;

            (* Verify Bubble Diameter Resonance Quenched Below 15 mm Amplitude *)
            IF (ABS(rIBC_Diameter_Voted - (rRecipe_LayFlatWidth_mm * 0.63661977)) < 15.0) AND (rBreatheDampingTimer_s >= 25.0) THEN
                eState_Current := 9;      (* Return to Nominal High-Speed Steady Production *)
                rStateTimer_s := 0.0;
            END_IF;

            IF bStopCycle THEN
                eState_Current := 12;
            END_IF;

        (* ---------------------------------------------------------------------------------------- *)
        (* STATE 12: AUTOMATED COORDINATED PRODUCTION LINE RAMPDOWN                                 *)
        (* ---------------------------------------------------------------------------------------- *)
        12:
            bSystemReady := FALSE;
            bInProduction := FALSE;
            rStateTimer_s := rStateTimer_s + tScanCycleTime_s;
            rRampdownTimer_s := rRampdownTimer_s + tScanCycleTime_s;

            (* Orderly Deceleration of All Subsystems *)
            vecU_target[0] := 50.0;
            vecU_target[1] := MAX(0.0, 1850.0 - (rRampdownTimer_s * 40.0));
            vecU_target[2] := MAX(0.0, 1820.0 - (rRampdownTimer_s * 40.0));
            vecU_target[3] := MAX(15.0, 65.0 - (rRampdownTimer_s * 1.5));
            vecU_target[4] := MAX(0.0, 68.0 - (rRampdownTimer_s * 1.8));
            vecU_target[5] := MAX(0.0, rRecipe_LineSpeed_mpm - (rRampdownTimer_s * 3.5));

            IF (vecU_target[5] <= 0.0) AND (vecU_target[4] <= 0.0) THEN
                eState_Current := 0;      (* System Halted in Idle Standby *)
                rStateTimer_s := 0.0;
            END_IF;

        (* ---------------------------------------------------------------------------------------- *)
        (* STATE 13: BUBBLE COLLAPSE OR WEB TEAR EMERGENCY STOP SHUTDOWN                            *)
        (* ---------------------------------------------------------------------------------------- *)
        13:
            bSystemReady := FALSE;
            bInProduction := FALSE;
            rStateTimer_s := rStateTimer_s + tScanCycleTime_s;
            rBubbleCollapseTimer_s := rBubbleCollapseTimer_s + tScanCycleTime_s;

            (* Instant Safe De-energization of Extruder Drives & Blowers *)
            vecU_target[0] := 50.0;
            vecU_target[1] := 0.0;
            vecU_target[2] := 0.0;
            vecU_target[3] := 0.0;
            vecU_target[4] := 0.0;
            vecU_target[5] := 0.0;

            (* Operator Reset Required to Exit Abort State *)
            IF bResetAlarms AND NOT bEmergencyStop AND NOT bCriticalTrip THEN
                eState_Current := 0;
                rStateTimer_s := 0.0;
            END_IF;
    END_CASE;

    eState_Current := eState_Current;
"""
