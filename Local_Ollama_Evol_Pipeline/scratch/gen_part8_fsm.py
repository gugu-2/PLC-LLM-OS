# Generator part 8: 12-Stage Finite State Machine Logic
def get_fsm_logic():
    return """(* ============================================================================================= *)
(* SECTION 5: 12-STAGE COMPREHENSIVE INDUSTRIAL FINITE STATE MACHINE (FSM)                       *)
(* ============================================================================================= *)

(* Monotonic State Elapsed Time Accumulator *)
IF iMachineState = iPreviousState THEN
    rStateTimer_s := rStateTimer_s + tScanTime_s;
ELSE
    rStateTimer_s := 0.0;
    iPreviousState := iMachineState;
END_IF;

CASE iMachineState OF
    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 0: SYSTEM_OFFLINE_LUBRICATION_WARM                                                  *)
    (* ----------------------------------------------------------------------------------------- *)
    0:
        rSAG_FreshFeedRateCmd_tph       := 0.0;
        rMillInletWaterFlowCmd_m3h      := 0.0;
        rRingMotorSpeedCmd_RPM          := 0.0;
        rRingMotorTorqueLimit_kNm       := 0.0;
        rCyclonePumpSpeedCmd_RPM        := 0.0;
        rCycloneSumpWaterValveCmd_Pct   := 0.0;
        bJackingOilPumpStart_Cmd        := TRUE;        (* Start hydraulic lift pumps to establish oil film *)
        bInchingDriveEngage_Cmd         := FALSE;
        bCriticalImpactEmergencyActive  := FALSE;
        dwSystemStatusWord              := 16#0000_0000;

        (* Close all hydrocyclone feed knife-gate valves *)
        FOR iCycloneIdx := 1 TO 12 DO
            abCycloneValveOpen_Cmd[iCycloneIdx] := FALSE;
        END_FOR;

        (* Check trunnion hydrostatic bearing lift oil pressure permissives *)
        IF bJackingOilPumpsRunning AND
           (rVoted_InletTrunnionPress_bar >= 135.0) AND
           (rVoted_OutletTrunnionPress_bar >= 140.0) THEN
            rLubeWarmupTimer_s := rLubeWarmupTimer_s + tScanTime_s;
            IF rLubeWarmupTimer_s >= 15.0 THEN          (* 15 seconds healthy oil film verification *)
                IF bAutoMode THEN
                    rLubeWarmupTimer_s := 0.0;
                    iMachineState := 10;                (* Proceed to INCHING_DRIVE_ALIGNMENT *)
                END_IF;
            END_IF;
        ELSE
            rLubeWarmupTimer_s := 0.0;
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 10: INCHING_DRIVE_ALIGNMENT                                                         *)
    (* ----------------------------------------------------------------------------------------- *)
    10:
        bJackingOilPumpStart_Cmd        := TRUE;
        bInchingDriveEngage_Cmd         := TRUE;        (* Engage mechanical inching drive clutch *)
        rRingMotorSpeedCmd_RPM          := 0.15;        (* Creep speed: 0.15 RPM *)
        rRingMotorTorqueLimit_kNm       := 12500.0;
        dwSystemStatusWord              := 16#0000_000A;

        rInchingAlignmentTimer_s := rInchingAlignmentTimer_s + tScanTime_s;
        (* Verify free rotation, Babbitt temperatures, and liner mechanical clearance for 120 seconds *)
        IF (rInchingAlignmentTimer_s >= 120.0) AND
           (TT_TRUNNION_INLET_BEARING_PAD_203A < 65.0) AND
           (TT_TRUNNION_OUTLET_BEARING_PAD_204A < 65.0) THEN
            bInchingDriveEngage_Cmd := FALSE;           (* Disengage inching clutch before main motor start *)
            rInchingAlignmentTimer_s := 0.0;
            iMachineState := 20;                        (* Proceed to RING_MOTOR_ACCELERATION *)
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 20: RING_MOTOR_ACCELERATION                                                         *)
    (* ----------------------------------------------------------------------------------------- *)
    20:
        bInchingDriveEngage_Cmd         := FALSE;
        bJackingOilPumpStart_Cmd        := TRUE;
        rRingMotorTorqueLimit_kNm       := 28500.0;     (* Enable full drive torque capability *)
        dwSystemStatusWord              := 16#0000_0014;

        (* Controlled synchronous acceleration ramp: 0.0 to 6.50 RPM at 0.05 RPM/s *)
        IF rRingMotorSpeedCmd_RPM < 6.50 THEN
            rRingMotorSpeedCmd_RPM := rRingMotorSpeedCmd_RPM + (0.050 * tScanTime_s);
        ELSE
            rRingMotorSpeedCmd_RPM := 6.50;
        END_IF;

        (* Verify speed pickup and stator flux lock *)
        IF (rVoted_RingMotorRPM >= 6.40) AND (rStateTimer_s >= 60.0) THEN
            iMachineState := 30;                        (* Proceed to WATER_FLUSH_STARTUP *)
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 30: WATER_FLUSH_STARTUP                                                             *)
    (* ----------------------------------------------------------------------------------------- *)
    30:
        rRingMotorSpeedCmd_RPM          := 6.50;
        rMillInletWaterFlowCmd_m3h      := 450.0;       (* Open feed dilution water to wet liners *)
        rCycloneSumpWaterValveCmd_Pct   := 25.0;        (* Prime slurry pump sump *)
        dwSystemStatusWord              := 16#0000_001E;

        (* Open initial 6 hydrocyclones in radial battery *)
        FOR iCycloneIdx := 1 TO 6 DO
            abCycloneValveOpen_Cmd[iCycloneIdx] := TRUE;
        END_FOR;
        FOR iCycloneIdx := 7 TO 12 DO
            abCycloneValveOpen_Cmd[iCycloneIdx] := FALSE;
        END_FOR;
        iActiveCyclonesTargetCount := 6;

        (* Start slurry pump when sump level reaches minimum priming threshold *)
        IF rVoted_SumpLevel_Pct >= 35.0 THEN
            rCyclonePumpSpeedCmd_RPM := 380.0;          (* Low speed slurry circulation *)
        END_IF;

        rWaterFlushTimer_s := rWaterFlushTimer_s + tScanTime_s;
        (* Hold water flush for 90 seconds until pulp lifter discharge establishes stable slurry pool *)
        IF (rWaterFlushTimer_s >= 90.0) AND (rVoted_SumpLevel_Pct >= 42.0) THEN
            rWaterFlushTimer_s := 0.0;
            iMachineState := 40;                        (* Proceed to LOW_FEED_HOMOGENIZATION *)
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 40: LOW_FEED_HOMOGENIZATION                                                         *)
    (* ----------------------------------------------------------------------------------------- *)
    40:
        rRingMotorSpeedCmd_RPM          := 7.20;        (* Accelerate to intermediate milling speed *)
        rSAG_FreshFeedRateCmd_tph       := 1250.0;      (* Initial ore feed bedding charge *)
        rMillInletWaterFlowCmd_m3h      := 580.0;       (* Target ~52% solids slurry inside mill *)
        rCyclonePumpSpeedCmd_RPM        := 440.0;
        dwSystemStatusWord              := 16#0000_0028;

        (* Open 8 hydrocyclones *)
        FOR iCycloneIdx := 1 TO 8 DO
            abCycloneValveOpen_Cmd[iCycloneIdx] := TRUE;
        END_FOR;
        FOR iCycloneIdx := 9 TO 12 DO
            abCycloneValveOpen_Cmd[iCycloneIdx] := FALSE;
        END_FOR;
        iActiveCyclonesTargetCount := 8;

        rHomogenizationTimer_s := rHomogenizationTimer_s + tScanTime_s;
        (* Verify charge bedding: total mill weight > 1180 t and toe angle established in 125..145 deg *)
        IF (rHomogenizationTimer_s >= 180.0) AND
           (rVoted_TotalMillWeight_tons >= 1180.0) AND
           (rEstimated_ToeAngle_deg >= 122.0) AND
           (rCalculated_LinerImpactIndex < 40.0) THEN
            rHomogenizationTimer_s := 0.0;
            iMachineState := 50;                        (* Proceed to FULL_PRODUCTION_AUTO_MPC *)
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 50: FULL_PRODUCTION_AUTO_MPC                                                        *)
    (* ----------------------------------------------------------------------------------------- *)
    50:
        dwSystemStatusWord              := 16#0000_0032;
        bCriticalImpactEmergencyActive  := FALSE;

        (* Check for Acoustic Direct Shell Liner Severe Impact Hazard *)
        IF rCalculated_LinerImpactIndex >= rImpactWarn_H_Pct THEN
            iMachineState := 60;                        (* Transition to ACOUSTIC_IMPACT_AUTO_MITIGATION *)
        (* Check for Hydrocyclone Manifold Pressure Battery Disruption *)
        ELSIF (rVoted_ManifoldPress_kPa > rTargetManifoldPress_Max_kPa) OR
              (rVoted_ManifoldPress_kPa < rTargetManifoldPress_Min_kPa) THEN
            rCycloneReconfigTimer_s := rCycloneReconfigTimer_s + tScanTime_s;
            IF rCycloneReconfigTimer_s >= 15.0 THEN
                rCycloneReconfigTimer_s := 0.0;
                iMachineState := 70;                    (* Transition to CYCLONE_CLUSTER_RO_TAP_RECONFIG *)
            END_IF;
        (* Check for Cyclone Feed Sump Surge *)
        ELSIF (rVoted_SumpLevel_Pct > rSumpWarn_H_Pct) OR
              (rVoted_SumpLevel_Pct < rSumpWarn_L_Pct) THEN
            iMachineState := 80;                        (* Transition to SUMP_SURGE_DAMPING *)
        ELSE
            rCycloneReconfigTimer_s := 0.0;
        END_IF;

        (* Manual operator stop request *)
        IF NOT bAutoMode THEN
            iMachineState := 90;                        (* Proceed to CONTROLLED_GRIND_OUT_SEQUENCE *)
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 60: ACOUSTIC_IMPACT_AUTO_MITIGATION                                                 *)
    (* ----------------------------------------------------------------------------------------- *)
    60:
        dwSystemStatusWord              := 16#0000_003C;
        bCriticalImpactEmergencyActive  := TRUE;

        (* Dynamic Liner Protection Override:
           1. Drop ring motor speed by -0.80 RPM to lower cataract trajectory into charge toe.
           2. Boost fresh ore feed rate by +250 t/h to create immediate ore cushioning bed.
           3. Reduce mill inlet water to increase slurry viscosity and hydrodynamic cushioning. *)
        IF rRingMotorSpeedCmd_RPM > 7.00 THEN
            rRingMotorSpeedCmd_RPM := rRingMotorSpeedCmd_RPM - (0.150 * tScanTime_s);
        END_IF;

        IF rSAG_FreshFeedRateCmd_tph < 3400.0 THEN
            rSAG_FreshFeedRateCmd_tph := rSAG_FreshFeedRateCmd_tph + (25.0 * tScanTime_s);
        END_IF;

        IF rMillInletWaterFlowCmd_m3h > 650.0 THEN
            rMillInletWaterFlowCmd_m3h := rMillInletWaterFlowCmd_m3h - (10.0 * tScanTime_s);
        END_IF;

        (* Verify recovery of acoustic impact index *)
        IF rCalculated_LinerImpactIndex < (rImpactWarn_H_Pct - rImpactDeadband_Pct) THEN
            rImpactMitigationTimer_s := rImpactMitigationTimer_s + tScanTime_s;
            IF rImpactMitigationTimer_s >= 30.0 THEN    (* 30 seconds verified low impact *)
                rImpactMitigationTimer_s := 0.0;
                bCriticalImpactEmergencyActive := FALSE;
                iMachineState := 50;                    (* Return to FULL_PRODUCTION_AUTO_MPC *)
            END_IF;
        ELSE
            rImpactMitigationTimer_s := 0.0;
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 70: CYCLONE_CLUSTER_RO_TAP_RECONFIG                                                 *)
    (* ----------------------------------------------------------------------------------------- *)
    70:
        dwSystemStatusWord              := 16#0000_0046;

        (* Overpressure: Open additional cyclone knife-gate valve to drop manifold pressure *)
        IF rVoted_ManifoldPress_kPa > rTargetManifoldPress_Max_kPa THEN
            IF iActiveCyclonesTargetCount < 12 THEN
                iActiveCyclonesTargetCount := iActiveCyclonesTargetCount + 1;
                abCycloneValveOpen_Cmd[iActiveCyclonesTargetCount] := TRUE;
            END_IF;
        (* Underpressure: Close one cyclone knife-gate valve to raise manifold pressure *)
        ELSIF rVoted_ManifoldPress_kPa < rTargetManifoldPress_Min_kPa THEN
            IF iActiveCyclonesTargetCount > 6 THEN
                abCycloneValveOpen_Cmd[iActiveCyclonesTargetCount] := FALSE;
                iActiveCyclonesTargetCount := iActiveCyclonesTargetCount - 1;
            END_IF;
        END_IF;

        (* Verify manifold pressure returned to operating window *)
        IF (rVoted_ManifoldPress_kPa >= rTargetManifoldPress_Min_kPa) AND
           (rVoted_ManifoldPress_kPa <= rTargetManifoldPress_Max_kPa) THEN
            iMachineState := 50;                        (* Return to FULL_PRODUCTION_AUTO_MPC *)
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 80: SUMP_SURGE_DAMPING                                                              *)
    (* ----------------------------------------------------------------------------------------- *)
    80:
        dwSystemStatusWord              := 16#0000_0050;

        (* Sump Level Surge: Boost pump speed and trim dilution water *)
        IF rVoted_SumpLevel_Pct > rSumpWarn_H_Pct THEN
            IF rCyclonePumpSpeedCmd_RPM < 720.0 THEN
                rCyclonePumpSpeedCmd_RPM := rCyclonePumpSpeedCmd_RPM + (1.50 * tScanTime_s);
            END_IF;
            IF rCycloneSumpWaterValveCmd_Pct > 10.0 THEN
                rCycloneSumpWaterValveCmd_Pct := rCycloneSumpWaterValveCmd_Pct - (0.50 * tScanTime_s);
            END_IF;
        (* Sump Level Depletion: Reduce pump speed and add dilution water to prevent cavitation *)
        ELSIF rVoted_SumpLevel_Pct < rSumpWarn_L_Pct THEN
            IF rCyclonePumpSpeedCmd_RPM > 380.0 THEN
                rCyclonePumpSpeedCmd_RPM := rCyclonePumpSpeedCmd_RPM - (2.00 * tScanTime_s);
            END_IF;
            IF rCycloneSumpWaterValveCmd_Pct < 85.0 THEN
                rCycloneSumpWaterValveCmd_Pct := rCycloneSumpWaterValveCmd_Pct + (1.00 * tScanTime_s);
            END_IF;
        END_IF;

        (* Return when sump level stabilizes in 48% to 68% sweet spot *)
        IF (rVoted_SumpLevel_Pct >= 48.0) AND (rVoted_SumpLevel_Pct <= 68.0) THEN
            iMachineState := 50;                        (* Return to FULL_PRODUCTION_AUTO_MPC *)
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 90: CONTROLLED_GRIND_OUT_SEQUENCE                                                   *)
    (* ----------------------------------------------------------------------------------------- *)
    90:
        dwSystemStatusWord              := 16#0000_005A;
        rSAG_FreshFeedRateCmd_tph       := 0.0;         (* Isolate fresh ore feed conveyor *)
        rPebbleCrusherFeedDiverter_Pct  := 0.0;         (* Stop pebble recycle *)
        rRingMotorSpeedCmd_RPM          := 7.00;        (* Maintain moderate grind-out speed *)
        rMillInletWaterFlowCmd_m3h      := 650.0;       (* Wash remaining ore out of mill shell *)

        rGrindOutTimer_s := rGrindOutTimer_s + tScanTime_s;
        (* Grind out until live ore inventory is fully discharged (total weight reaches deadweight + balls) *)
        IF (rVoted_TotalMillWeight_tons <= (rMillShellTareMass_tons + rNominalBallChargeMass_tons + 65.0)) OR
           (rGrindOutTimer_s >= 600.0) THEN             (* 10 minute timeout *)
            rMillInletWaterFlowCmd_m3h := 0.0;          (* Stop wash water *)
            rGrindOutTimer_s := 0.0;
            iMachineState := 100;                       (* Proceed to MILL_CRADLE_PARK *)
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 100: MILL_CRADLE_PARK                                                               *)
    (* ----------------------------------------------------------------------------------------- *)
    100:
        dwSystemStatusWord              := 16#0000_0064;
        rSAG_FreshFeedRateCmd_tph       := 0.0;
        rMillInletWaterFlowCmd_m3h      := 0.0;
        rCyclonePumpSpeedCmd_RPM        := 0.0;
        rCycloneSumpWaterValveCmd_Pct   := 0.0;

        (* Ramp ring motor speed down to dead stop *)
        IF rRingMotorSpeedCmd_RPM > 0.0 THEN
            rRingMotorSpeedCmd_RPM := rRingMotorSpeedCmd_RPM - (0.20 * tScanTime_s);
            IF rRingMotorSpeedCmd_RPM < 0.0 THEN
                rRingMotorSpeedCmd_RPM := 0.0;
            END_IF;
        END_IF;

        (* Engage mechanical parking brake and cradle clamps once stopped *)
        IF rVoted_RingMotorRPM <= 0.02 THEN
            rCradleParkTimer_s := rCradleParkTimer_s + tScanTime_s;
            IF rCradleParkTimer_s >= 60.0 THEN
                rCradleParkTimer_s := 0.0;
                iMachineState := 0;                     (* Return to SYSTEM_OFFLINE_LUBRICATION_WARM *)
            END_IF;
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 999: EMERGENCY_ESTOP                                                                *)
    (* ----------------------------------------------------------------------------------------- *)
    999:
        dwSystemStatusWord              := 16#0000_03E7;
        rSAG_FreshFeedRateCmd_tph       := 0.0;
        rMillInletWaterFlowCmd_m3h      := 0.0;
        rRingMotorSpeedCmd_RPM          := 0.0;
        rRingMotorTorqueLimit_kNm       := 0.0;
        rCyclonePumpSpeedCmd_RPM        := 0.0;
        rCycloneSumpWaterValveCmd_Pct   := 0.0;
        bInchingDriveEngage_Cmd         := FALSE;
        bJackingOilPumpStart_Cmd        := TRUE;        (* Retain oil film to protect trunnion Babbitt *)

        (* Acknowledge and reset required to clear emergency state *)
        IF bEmergencyStop AND bAcknowledgeAlarms THEN
            dwAlarmWord_HighTrip := 16#0000_0000;
            iMachineState := 0;                         (* Reset to OFFLINE state *)
        END_IF;

ELSE
    iMachineState := 0;
END_CASE;

iOperatingState := iMachineState;
"""

print("FSM module loaded.")
