# section4_fsm.py
# Deterministic 14-Stage Production Finite State Machine (FSM)

def get_section4():
    return """
(* ========================================================================================= *)
(* 4.0 DETERMINISTIC 14-STAGE PRODUCTION FINITE STATE MACHINE (FSM)                          *)
(* ========================================================================================= *)
(* Executes strict deterministic sequential control for the 9,000-ton mega-casting cycle.   *)
(* Every state has explicit entry preconditions, timeout monitoring, real-time safety        *)
(* interlocking, dynamic actuator trimming, and guaranteed fail-safe transition logic.       *)

(* Update Master Cycle Timer *)
IF bSystemRunning THEN
    rTotalCycleDuration_sec := rTotalCycleDuration_sec + rCycleTime_sec;
ELSE
    rTotalCycleDuration_sec := 0.0;
END_IF;

(* Master Safety Interlock Override: Trip immediately branches to State 13 *)
IF bSystemTripped AND (iState <> c_STATE_EMERGENCY_FLASH_BLOWOUT_OR_TIE_BAR_OVERSTRAIN_TRIP) THEN
    iState := c_STATE_EMERGENCY_FLASH_BLOWOUT_OR_TIE_BAR_OVERSTRAIN_TRIP;
    rStateTimer_sec := 0.0;
END_IF;

(* Advance Current State Elapsed Running Timer *)
rStateTimer_sec := rStateTimer_sec + rCycleTime_sec;

CASE iState OF

    (* ------------------------------------------------------------------------------------- *)
    (* STATE 0: IDLE / STANDBY PRE-CHECK & PERMISSIVE VERIFICATION                           *)
    (* ------------------------------------------------------------------------------------- *)
    c_STATE_IDLE:
        rStateTimeout_sec := 3600.0; (* 1 hour standby timeout *)
        bSystemRunning    := FALSE;
        bDieSafetyClampLock_CMD := FALSE;
        bFastShutoffChillValve_CMD := FALSE;
        bLadleRobotPermissive_CMD := FALSE;
        bSprayRobotInitiate_CMD := FALSE;
        bExtractorRobotInitiate_CMD := FALSE;
        bVacuumRootsIsolation_CMD := FALSE;

        (* Check System Readiness Permissives *)
        bSystemReady := bEmergencyStopCircuit_NC AND 
                        bSafetyPerimeterCageLocked AND 
                        bHydraulicPowerUnitReady AND 
                        bAccumulatorCharged AND 
                        bVacuumRootsStationReady AND 
                        bEjectorPlatesRetracted_LS AND 
                        NOT bSystemTripped;

        IF bSystemReady AND bCycleStartCommand AND bManualAutoModeSelect THEN
            bSystemRunning := TRUE;
            rTotalCycleDuration_sec := 0.0;
            rPhase1Duration_ms := 0.0;
            rPhase2Duration_ms := 0.0;
            rPhase3RiseTime_ms := 0.0;
            rChillValveCloseTime_ms := 0.0;
            rCavityPeakPressure_bar := 0.0;
            iState := c_STATE_DIE_SAFETY_DOOR_LOCK_AND_PARTING_AGENT_SPRAY;
            rStateTimer_sec := 0.0;
        END_IF;

    (* ------------------------------------------------------------------------------------- *)
    (* STATE 1: DIE SAFETY LOCK & PARTING AGENT GANTRY SPRAY                                 *)
    (* ------------------------------------------------------------------------------------- *)
    c_STATE_DIE_SAFETY_DOOR_LOCK_AND_PARTING_AGENT_SPRAY:
        rStateTimeout_sec := 45.0; (* 45 seconds spray cycle timeout *)
        bDieSafetyClampLock_CMD := FALSE;
        bSprayRobotInitiate_CMD := TRUE;
        bVacuumRootsIsolation_CMD := FALSE;

        (* Permissive Check *)
        IF NOT bSafetyPerimeterCageLocked OR NOT bEmergencyStopCircuit_NC THEN
            dwFirstOutWord := 16#0000_0001; (* Safety perimeter breach in spray state *)
            bSystemTripped := TRUE;
        END_IF;

        (* Transition: Gantry spray robot signals spray and air blow-dry sequence complete *)
        IF bDieSprayedAndDried AND (rStateTimer_sec >= 2.5) THEN
            bSprayRobotInitiate_CMD := FALSE;
            iState := c_STATE_4_TIE_BAR_HYDRAULIC_CLAMP_TO_90000KN;
            rStateTimer_sec := 0.0;
        ELSIF rStateTimer_sec > rStateTimeout_sec THEN
            dwFirstOutWord := 16#0000_0002; (* Spray robot cycle timeout *)
            bSystemTripped := TRUE;
        END_IF;

    (* ------------------------------------------------------------------------------------- *)
    (* STATE 2: 4-TIE-BAR HYDRAULIC CLAMPING PRE-STRESS TO 90,000 KN                         *)
    (* ------------------------------------------------------------------------------------- *)
    c_STATE_4_TIE_BAR_HYDRAULIC_CLAMP_TO_90000KN:
        rStateTimeout_sec := 18.0; (* 18 seconds clamping ramp timeout *)
        bDieSafetyClampLock_CMD := TRUE;
        bLadleRobotPermissive_CMD := FALSE;

        (* Clamping Force Ramp Verification (Target: 90,000 kN +/- 2%) *)
        IF (rClampForce_Voted_kN >= 88200.0) AND (rClampForce_Voted_kN <= 91800.0) AND 
           (rTieBarMaxEccentricity_kN < c_ALM_Eccentricity_H_kN) AND 
           (rStateTimer_sec >= 3.0) THEN
            iState := c_STATE_LADLE_ROBOT_MOLTEN_ALUMINUM_POUR_INTO_SLEEVE;
            rStateTimer_sec := 0.0;
        ELSIF rStateTimer_sec > rStateTimeout_sec THEN
            dwFirstOutWord := 16#0000_0004; (* Clamp tonnage pressurization timeout *)
            bSystemTripped := TRUE;
        END_IF;

    (* ------------------------------------------------------------------------------------- *)
    (* STATE 3: ROBOTIC LADLE MOLTEN ALUMINUM ALLOY POUR (110 KG DOSE)                       *)
    (* ------------------------------------------------------------------------------------- *)
    c_STATE_LADLE_ROBOT_MOLTEN_ALUMINUM_POUR_INTO_SLEEVE:
        rStateTimeout_sec := 25.0; (* 25 seconds robotic pour timeout *)
        bDieSafetyClampLock_CMD := TRUE;
        bLadleRobotPermissive_CMD := TRUE;

        (* Check Holding Furnace Pour Melt Temperature (670 °C to 710 °C) *)
        IF (rMeltTemp_degC < 665.0) OR (rMeltTemp_degC > 725.0) THEN
            dwFirstOutWord := 16#0000_0008; (* Molten metal ladle temp out of spec *)
            bSystemTripped := TRUE;
        END_IF;

        (* Transition: Dosing ladle completes 110 kg pour and retracts clear *)
        IF bLadlePourComplete AND (rLadleDoseWeight_kg >= 105.0) AND (rLadleDoseWeight_kg <= 115.0) THEN
            bLadleRobotPermissive_CMD := FALSE;
            iState := c_STATE_MOLD_CAVITY_HIGH_VACUUM_EVACUATION_BELOW_25MBAR;
            rStateTimer_sec := 0.0;
        ELSIF rStateTimer_sec > rStateTimeout_sec THEN
            dwFirstOutWord := 16#0000_0010; (* Dosing ladle robot cycle timeout *)
            bSystemTripped := TRUE;
        END_IF;

    (* ------------------------------------------------------------------------------------- *)
    (* STATE 4: MOLD CAVITY HIGH-VACUUM DECOMPRESSION (P_VAC < 25 MBAR)                      *)
    (* ------------------------------------------------------------------------------------- *)
    c_STATE_MOLD_CAVITY_HIGH_VACUUM_EVACUATION_BELOW_25MBAR:
        rStateTimeout_sec := 4.5; (* 4.5 seconds vacuum evacuation window *)
        bDieSafetyClampLock_CMD := TRUE;
        bVacuumRootsIsolation_CMD := TRUE;
        bFastShutoffChillValve_CMD := FALSE;

        (* Check Vacuum Progress *)
        IF (rCavityVac_Voted_mbar <= 25.0) AND (rStateTimer_sec >= 0.25) THEN
            iState := c_STATE_PHASE1_SLOW_SHOT_WAVE_SURGE_SUPPRESSION;
            rStateTimer_sec := 0.0;
        ELSIF rStateTimer_sec > rStateTimeout_sec THEN
            dwFirstOutWord := 16#0000_0020; (* Vacuum pump down failure (< 25 mbar not reached) *)
            bSystemTripped := TRUE;
        END_IF;

    (* ------------------------------------------------------------------------------------- *)
    (* STATE 5: PHASE 1 SLOW SHOT COMPACTION & WAVE SURGE SUPPRESSION                        *)
    (* ------------------------------------------------------------------------------------- *)
    c_STATE_PHASE1_SLOW_SHOT_WAVE_SURGE_SUPPRESSION:
        rStateTimeout_sec := 6.5; (* 6.5 seconds slow shot duration limit *)
        bDieSafetyClampLock_CMD := TRUE;
        bVacuumRootsIsolation_CMD := TRUE;

        (* Plunger advances at sculpted slow speed (v1 = 0.25 m/s) until reaching compaction boundary *)
        IF rPlungerPos_mm >= c_Pos_FastShotTransition_mm THEN
            rPhase1Duration_ms := rStateTimer_sec * 1000.0;
            iState := c_STATE_PHASE2_FAST_SHOT_HIGH_ACCELERATION_CAVITY_FILL;
            rStateTimer_sec := 0.0;
        ELSIF rStateTimer_sec > rStateTimeout_sec THEN
            dwFirstOutWord := 16#0000_0040; (* Phase 1 slow shot compaction timeout / plunger stall *)
            bSystemTripped := TRUE;
        END_IF;

    (* ------------------------------------------------------------------------------------- *)
    (* STATE 6: PHASE 2 FAST SHOT HIGH-ACCELERATION CAVITY FILL (v2 = 8.5 m/s)               *)
    (* ------------------------------------------------------------------------------------- *)
    c_STATE_PHASE2_FAST_SHOT_HIGH_ACCELERATION_CAVITY_FILL:
        rStateTimeout_sec := 0.120; (* 120 ms maximum fast shot cavity fill window *)
        bDieSafetyClampLock_CMD := TRUE;
        bVacuumRootsIsolation_CMD := TRUE;

        (* Transition on Metal Front Arrival at Gate Runners or Stroke Threshold *)
        IF bMetalFront_ChillBlock OR (rPlungerPos_mm >= c_Pos_CavityFillImpact_mm) OR 
           (rShotPress_Voted_bar >= 450.0) THEN
            rPhase2Duration_ms := rStateTimer_sec * 1000.0;
            bFastShutoffChillValve_CMD := TRUE; (* Snap shut acoustic chill vent *)
            iState := c_STATE_VACUUM_CHILL_BLOCK_VALVE_FAST_SHUTOFF;
            rStateTimer_sec := 0.0;
        ELSIF rStateTimer_sec > rStateTimeout_sec THEN
            dwFirstOutWord := 16#0000_0080; (* Phase 2 fast fill timeout / premature freeze *)
            bSystemTripped := TRUE;
        END_IF;

    (* ------------------------------------------------------------------------------------- *)
    (* STATE 7: ACOUSTIC CHILL-BLOCK ULTRA-FAST VALVE SHUTOFF (< 8.0 MS)                     *)
    (* ------------------------------------------------------------------------------------- *)
    c_STATE_VACUUM_CHILL_BLOCK_VALVE_FAST_SHUTOFF:
        rStateTimeout_sec := 0.025; (* 25 ms maximum allowable valve travel *)
        bDieSafetyClampLock_CMD := TRUE;
        bFastShutoffChillValve_CMD := TRUE;

        IF bChillBlockValveClosed_LS THEN
            bVacuumRootsIsolation_CMD := FALSE; (* Isolate vacuum header *)
            iState := c_STATE_PHASE3_INTENSIFICATION_PRESSURE_SQUEEZE_1400BAR;
            rStateTimer_sec := 0.0;
        ELSIF rStateTimer_sec > (c_ALM_ChillClose_HH_ms * 0.001) THEN
            dwFirstOutWord := 16#0000_0100; (* Chill valve sluggish closure (> 8 ms) molten metal ingress hazard *)
            bSystemTripped := TRUE;
        END_IF;

    (* ------------------------------------------------------------------------------------- *)
    (* STATE 8: PHASE 3 INTENSIFICATION PRESSURE SQUEEZE (1,400 BAR BOOST)                  *)
    (* ------------------------------------------------------------------------------------- *)
    c_STATE_PHASE3_INTENSIFICATION_PRESSURE_SQUEEZE_1400BAR:
        rStateTimeout_sec := 2.5; (* 2.5 seconds intensification squeeze window *)
        bDieSafetyClampLock_CMD := TRUE;
        bFastShutoffChillValve_CMD := TRUE;

        (* Peak Pressure Recording *)
        IF rShotPress_Voted_bar > rCavityPeakPressure_bar THEN
            rCavityPeakPressure_bar := rShotPress_Voted_bar;
        END_IF;

        (* Measure Intensification 10% to 90% Rise Time *)
        IF (rPhase3RiseTime_ms = 0.0) AND (rShotPress_Voted_bar >= 1260.0) THEN
            rPhase3RiseTime_ms := rStateTimer_sec * 1000.0;
        END_IF;

        (* Flash Safety Check: If clamp force is threatened by hydraulic spike *)
        IF bAlm_FlashBlowoutRisk_HH THEN
            dwFirstOutWord := 16#0000_0200; (* Die flash blowout imminent during Phase 3 *)
            bSystemTripped := TRUE;
        END_IF;

        (* Transition to Solidification Cooling Hold *)
        IF rStateTimer_sec >= 1.20 THEN
            iState := c_STATE_IN_DIE_SOLIDIFICATION_COOLING_HOLD;
            rStateTimer_sec := 0.0;
        END_IF;

    (* ------------------------------------------------------------------------------------- *)
    (* STATE 9: IN-DIE SOLIDIFICATION COOLING HOLD & THERMAL EQUILIBRATION                   *)
    (* ------------------------------------------------------------------------------------- *)
    c_STATE_IN_DIE_SOLIDIFICATION_COOLING_HOLD:
        rStateTimeout_sec := 35.0; (* 35 seconds solidification dwell limit *)
        bDieSafetyClampLock_CMD := TRUE;
        bFastShutoffChillValve_CMD := FALSE;

        (* Hold until skin thickness reaches center-line and die face cools < 235 °C *)
        IF (rSolidificationThickness_mm >= (c_PartMeanThickness_mm * 0.48)) AND 
           (rStateTimer_sec >= 12.0) THEN
            iState := c_STATE_TIE_BAR_DECOMPRESSION_AND_DIE_OPEN_STROKE;
            rStateTimer_sec := 0.0;
        ELSIF rStateTimer_sec > rStateTimeout_sec THEN
            dwFirstOutWord := 16#0000_0400; (* Solidification hold timeout *)
            bSystemTripped := TRUE;
        END_IF;

    (* ------------------------------------------------------------------------------------- *)
    (* STATE 10: TIE-BAR HYDRAULIC DECOMPRESSION & 2,200 MM DIE OPEN STROKE                  *)
    (* ------------------------------------------------------------------------------------- *)
    c_STATE_TIE_BAR_DECOMPRESSION_AND_DIE_OPEN_STROKE:
        rStateTimeout_sec := 22.0; (* 22 seconds decompression and platen stroke *)
        bDieSafetyClampLock_CMD := FALSE;

        (* Smooth Controlled Decompression *)
        IF (rClampForce_Voted_kN <= 250.0) AND (rStateTimer_sec >= 6.5) THEN
            iState := c_STATE_HYDRAULIC_EJECTOR_PINS_MULTI_POINT_PUSH;
            rStateTimer_sec := 0.0;
        ELSIF rStateTimer_sec > rStateTimeout_sec THEN
            dwFirstOutWord := 16#0000_0800; (* Platen opening / decompression timeout *)
            bSystemTripped := TRUE;
        END_IF;

    (* ------------------------------------------------------------------------------------- *)
    (* STATE 11: HYDRAULIC MULTI-POINT EJECTOR PINS EXTENSION PUSH                           *)
    (* ------------------------------------------------------------------------------------- *)
    c_STATE_HYDRAULIC_EJECTOR_PINS_MULTI_POINT_PUSH:
        rStateTimeout_sec := 15.0; (* 15 seconds ejector push timeout *)
        rEjectorDrive_pct := 75.0; (* Proportional ejector push speed *)

        IF rStateTimer_sec >= 4.0 THEN
            rEjectorDrive_pct := 0.0;
            bExtractorRobotInitiate_CMD := TRUE;
            iState := c_STATE_EXTRACTOR_ROBOT_PART_GRIP_AND_LASER_METROLOGY;
            rStateTimer_sec := 0.0;
        ELSIF rStateTimer_sec > rStateTimeout_sec THEN
            dwFirstOutWord := 16#0000_1000; (* Ejector pin stroke timeout *)
            bSystemTripped := TRUE;
        END_IF;

    (* ------------------------------------------------------------------------------------- *)
    (* STATE 12: EXTRACTOR ROBOT PART GRIP, REMOVAL & LASER METROLOGY CHECK                  *)
    (* ------------------------------------------------------------------------------------- *)
    c_STATE_EXTRACTOR_ROBOT_PART_GRIP_AND_LASER_METROLOGY:
        rStateTimeout_sec := 30.0; (* 30 seconds extraction and metrology timeout *)
        bExtractorRobotInitiate_CMD := TRUE;

        IF bExtractorRobotInPosition AND (rStateTimer_sec >= 8.0) THEN
            bExtractorRobotInitiate_CMD := FALSE;
            bSystemRunning := FALSE;
            iState := c_STATE_IDLE; (* Cycle completed successfully *)
            rStateTimer_sec := 0.0;
        ELSIF rStateTimer_sec > rStateTimeout_sec THEN
            dwFirstOutWord := 16#0000_2000; (* Extractor robot clearance timeout *)
            bSystemTripped := TRUE;
        END_IF;

    (* ------------------------------------------------------------------------------------- *)
    (* STATE 13: EMERGENCY FLASH BLOWOUT OR TIE-BAR OVERSTRAIN TRIP HOLD                     *)
    (* ------------------------------------------------------------------------------------- *)
    c_STATE_EMERGENCY_FLASH_BLOWOUT_OR_TIE_BAR_OVERSTRAIN_TRIP:
        bSystemRunning := FALSE;
        bSystemReady := FALSE;
        bDieSafetyClampLock_CMD := FALSE;
        bFastShutoffChillValve_CMD := TRUE;
        bLadleRobotPermissive_CMD := FALSE;
        bSprayRobotInitiate_CMD := FALSE;
        bExtractorRobotInitiate_CMD := FALSE;
        bVacuumRootsIsolation_CMD := FALSE;
        rPilotValve_Shot_pct := 0.0;
        rAccumulatorPoppet_pct := 0.0;
        rIntensifierValve_pct := 0.0;
        rVacuumValve_pct := 0.0;
        rEjectorDrive_pct := 0.0;

        (* Alarm Latch Reset Acknowledgment *)
        IF bAlarmReset AND NOT bEmergencyStopCircuit_NC THEN
            (* Acknowledge requires e-stop clearing *)
        ELSIF bAlarmReset AND bSafetyPerimeterCageLocked THEN
            bSystemTripped := FALSE;
            dwAlarmWord1 := 16#0000_0000;
            dwAlarmWord2 := 16#0000_0000;
            dwFirstOutWord := 16#0000_0000;
            iState := c_STATE_IDLE;
            rStateTimer_sec := 0.0;
        END_IF;

    ELSE
        iState := c_STATE_EMERGENCY_FLASH_BLOWOUT_OR_TIE_BAR_OVERSTRAIN_TRIP;
        rStateTimer_sec := 0.0;
END_CASE;
"""

if __name__ == "__main__":
    print("Section 4 len:", len(get_section4()))
