# cmp_polisher_builder/part6_fsm.py

def get_part6():
    return """(*
========================================================================================================================
  PHASE 4: DETERMINISTIC 14-STAGE PRODUCTION FINITE STATE MACHINE (FSM)
  AUTOMATED 300MM CMP RECIPE EXECUTION WITH PRESTONIAN ENDPOINT TRACKING & SAFETY RECOVERY
========================================================================================================================
*)
(* Update State Dwell Timer *)
rStateTimer_s := rStateTimer_s + T_CYCLE_SEC;

(* Safety Supervisory Override: Hardwired E-Stop or Vacuum Loss Trip *)
IF (NOT bEmergencyStop) THEN
    nFsmCurrentState := STATE_CMP_EMERGENCY_TRIP_VAC_LOSS;
    bEmergencyTripActive := TRUE;
ELSIF (nOperationalState >= STATE_CMP_LOW_PRESSURE_TOUCHDOWN) AND (nOperationalState <= STATE_CMP_SOFT_LANDING_OVERPOLISH) THEN
    (* Instantaneous Vacuum Loss Detection during active polish *)
    IF (rCarrierVacuum_kPa > rCarrierVac_Limit_LL_kPa) AND (NOT bWaferChucked_Carrier) THEN
        nFsmCurrentState := STATE_CMP_EMERGENCY_TRIP_VAC_LOSS;
        bEmergencyTripActive := TRUE;
    END_IF;
END_IF;

(* Main FSM State Execution *)
CASE nFsmCurrentState OF

    (* -------------------------------------------------------------------------------------------------------------- *)
    (* STATE 0: IDLE / STANDBY READY                                                                                  *)
    (* -------------------------------------------------------------------------------------------------------------- *)
    STATE_CMP_IDLE_STANDBY:
        bSystemReady := bSystemEnable AND bEmergencyStop AND (NOT bEmergencyTripActive);
        bProductionActive := FALSE;
        bWaferPolishedComplete := FALSE;
        bEndpointDetected := FALSE;
        bOpticalEndpointLatched := FALSE;
        bEddyCurrentEndpointLatched := FALSE;
        rOverpolishTimer_s := 0.0;
        
        (* Motion & Pneumatic Safe Standby Command *)
        x_ref[1] := 0.0;    (* Platen Stop *)
        x_ref[2] := 0.0;    (* Carrier Stop *)
        rCarrierZAxisDriveCmd_pct := 0.0;
        rCarrierSweepVelocityCmd_mmps := 0.0;
        bCarrierVacuumSolenoidCmd := FALSE;
        
        (* Transition: Operator Start / SECS-GEM Command with Wafer in Load Cup *)
        IF bSystemReady AND bProductionRunCmd AND bRecipeStartCmd AND bWaferPresent_LoadCup THEN
            nFsmCurrentState := STATE_CMP_WAFER_LOAD_CUP_HANDSHAKE;
            rStateTimer_s := 0.0;
            bStateFirstScan := TRUE;
        END_IF;

    (* -------------------------------------------------------------------------------------------------------------- *)
    (* STATE 1: WAFER LOAD CUP HANDSHAKE & VACUUM CHUCKING SEAL                                                       *)
    (* -------------------------------------------------------------------------------------------------------------- *)
    STATE_CMP_WAFER_LOAD_CUP_HANDSHAKE:
        bProductionActive := TRUE;
        bCarrierVacuumSolenoidCmd := TRUE;      (* Engage Venturi Chucking Vacuum *)
        rCarrierZAxisDriveCmd_pct := -15.0;     (* Slow Descent onto Load Cup *)
        
        (* Handshake Transition: Vacuum Reaches Minimum Chucking Level & Capacitive Sensor Active *)
        IF (rCarrierVacuum_kPa <= -75.0) AND bWaferChucked_Carrier AND (rStateTimer_s >= 2.0) THEN
            nFsmCurrentState := STATE_CMP_PLATEN_SWEEP_AND_DESCENT;
            rStateTimer_s := 0.0;
            bStateFirstScan := TRUE;
        ELSIF rStateTimer_s > 12.0 THEN
            (* Load Handshake Timeout Abort *)
            nFsmCurrentState := STATE_CMP_IDLE_STANDBY;
            rStateTimer_s := 0.0;
        END_IF;

    (* -------------------------------------------------------------------------------------------------------------- *)
    (* STATE 2: PLATEN SWEEP & CARRIER DESCENT APPROACH                                                               *)
    (* -------------------------------------------------------------------------------------------------------------- *)
    STATE_CMP_PLATEN_SWEEP_AND_DESCENT:
        (* Accelerate Platen and Carrier Spindles towards initial sync speed *)
        x_ref[1] := 65.0;   (* Platen Initial Ramp [rpm] *)
        x_ref[2] := 60.0;   (* Carrier Initial Ramp [rpm] *)
        rCarrierZAxisDriveCmd_pct := -45.0;     (* Controlled Z-Descent toward Pad *)
        rCarrierSweepVelocityCmd_mmps := 25.0;  (* Sweep Carrier over Platen Track *)
        
        (* Transition: Carrier reaches Pad Proximity Height (1.5 mm above pad) and speeds synchronized *)
        IF (rCarrierZAxisPosition_mm <= 1.5) AND (rPlatenSpeed_PV_rpm >= 60.0) AND (rCarrierSpeed_PV_rpm >= 55.0) THEN
            nFsmCurrentState := STATE_CMP_LOW_PRESSURE_TOUCHDOWN;
            rStateTimer_s := 0.0;
            bStateFirstScan := TRUE;
        ELSIF rStateTimer_s > 15.0 THEN
            nFsmCurrentState := STATE_CMP_EMERGENCY_TRIP_VAC_LOSS;
            rStateTimer_s := 0.0;
        END_IF;

    (* -------------------------------------------------------------------------------------------------------------- *)
    (* STATE 3: LOW-PRESSURE TOUCH-DOWN & SLURRY PRE-WET                                                              *)
    (* -------------------------------------------------------------------------------------------------------------- *)
    STATE_CMP_LOW_PRESSURE_TOUCHDOWN:
        (* Engage Slurry Pre-Wet Film and Apply Low Initial Seating Pressure *)
        rSlurryFlowTarget_mLpm := 280.0;
        bSlurryDeliveryValveCmd := TRUE;
        x_ref[1] := 80.0;
        x_ref[2] := 75.0;
        x_ref[3] := 1.20;   (* Soft Touchdown Pressure: 1.2 psi *)
        rCarrierZAxisDriveCmd_pct := -5.0;  (* Gentle compliance descent *)
        
        (* Transition: Contact confirmed via Platen Reaction Torque Rise & Pad Pre-Wet Timer elapsed *)
        IF (rVotedPlatenTorque_Nm >= 25.0) AND (rStateTimer_s >= 3.5) THEN
            nFsmCurrentState := STATE_CMP_MULTI_ZONE_BULK_RAMP;
            rStateTimer_s := 0.0;
            bStateFirstScan := TRUE;
        ELSIF rStateTimer_s > 10.0 THEN
            nFsmCurrentState := STATE_CMP_EMERGENCY_TRIP_VAC_LOSS;
            rStateTimer_s := 0.0;
        END_IF;

    (* -------------------------------------------------------------------------------------------------------------- *)
    (* STATE 4: MULTI-ZONE BULK COPPER POLISH RAMP                                                                    *)
    (* -------------------------------------------------------------------------------------------------------------- *)
    STATE_CMP_MULTI_ZONE_BULK_RAMP:
        (* Ramp kinematic velocities and downforce pressures to full recipe setpoints *)
        x_ref[1] := 93.0;   (* Recipe Nominal Platen Speed [rpm] *)
        x_ref[2] := 87.0;   (* Recipe Nominal Carrier Speed [rpm] *)
        x_ref[3] := 2.95;   (* Bulk Removal Mean Downforce [psi] *)
        rSlurryFlowTarget_mLpm := 250.0;
        
        (* Transition: Operating velocities reached and stable contact established *)
        IF (rPlatenSpeed_PV_rpm >= 90.0) AND (rCarrierSpeed_PV_rpm >= 84.0) AND (rStateTimer_s >= 5.0) THEN
            nFsmCurrentState := STATE_CMP_STEADY_STATE_POLISH;
            rStateTimer_s := 0.0;
            bStateFirstScan := TRUE;
        END_IF;

    (* -------------------------------------------------------------------------------------------------------------- *)
    (* STATE 5: STEADY-STATE POLISH & HIGH-FREQUENCY EDDY CURRENT MONITORING                                          *)
    (* -------------------------------------------------------------------------------------------------------------- *)
    STATE_CMP_STEADY_STATE_POLISH:
        (* In-situ continuous pad conditioning engaged concurrently *)
        bCondArmInService := TRUE;
        
        (* Monitor Eddy Current Copper Film Thickness reduction towards Soft-Landing Threshold *)
        IF (x_state[4] <= rEpdThresholdThickness_Angstrom) OR (rVotedFilmThickness_Angstrom <= rEpdThresholdThickness_Angstrom) THEN
            bEddyCurrentEndpointLatched := TRUE;
            nFsmCurrentState := STATE_CMP_OPTICAL_EPD_LOCK;
            rStateTimer_s := 0.0;
            bStateFirstScan := TRUE;
        ELSIF rStateTimer_s > 180.0 THEN
            (* Maximum Bulk Polish Time Exceeded: Recipe Safeguard *)
            nFsmCurrentState := STATE_CMP_SOFT_LANDING_OVERPOLISH;
            rStateTimer_s := 0.0;
        END_IF;

    (* -------------------------------------------------------------------------------------------------------------- *)
    (* STATE 6: OPTICAL REFLECTANCE ENDPOINT DETECTION (EPD) LOCK & BARRIER CROSSING                                 *)
    (* -------------------------------------------------------------------------------------------------------------- *)
    STATE_CMP_OPTICAL_EPD_LOCK:
        (* Disengage pad conditioner to stabilize optical window signal *)
        bCondArmInService := FALSE;
        
        (* Detect Optical Interference Step Inflection Slope indicating Copper Clearance *)
        IF (rOpticalSlope_pctps <= rEpdOpticalInflectionSlope) OR (x_state[4] <= rEpdFinalTargetThickness_Angstrom) THEN
            bOpticalEndpointLatched := TRUE;
            bEndpointDetected := TRUE;
            nFsmCurrentState := STATE_CMP_SOFT_LANDING_OVERPOLISH;
            rStateTimer_s := 0.0;
            bStateFirstScan := TRUE;
        ELSIF rStateTimer_s > 30.0 THEN
            (* Optical Lock Timeout Fallback *)
            bEndpointDetected := TRUE;
            nFsmCurrentState := STATE_CMP_SOFT_LANDING_OVERPOLISH;
            rStateTimer_s := 0.0;
        END_IF;

    (* -------------------------------------------------------------------------------------------------------------- *)
    (* STATE 7: SOFT LANDING CONTROLLED OVER-POLISH & CLEARANCE                                                       *)
    (* -------------------------------------------------------------------------------------------------------------- *)
    STATE_CMP_SOFT_LANDING_OVERPOLISH:
        (* Reduce downforce pressure to minimize dishing and erosion into dielectric oxide *)
        x_ref[1] := 75.0;
        x_ref[2] := 70.0;
        x_ref[3] := 1.45;   (* Soft Landing Pressure: 1.45 psi *)
        rOverpolishTimer_s := rOverpolishTimer_s + T_CYCLE_SEC;
        
        (* Transition: Recipe Over-Polish Duration Completed *)
        IF rOverpolishTimer_s >= rRecipeOverpolishTarget_s THEN
            bWaferPolishedComplete := TRUE;
            nFsmCurrentState := STATE_CMP_DIW_HIGH_PRESSURE_FLUSH;
            rStateTimer_s := 0.0;
            bStateFirstScan := TRUE;
        END_IF;

    (* -------------------------------------------------------------------------------------------------------------- *)
    (* STATE 8: DE-IONIZED WATER (DIW) HIGH-PRESSURE FLUSH & POLISH STOP                                             *)
    (* -------------------------------------------------------------------------------------------------------------- *)
    STATE_CMP_DIW_HIGH_PRESSURE_FLUSH:
        (* Cut Slurry Delivery, Flood Pad with DIW to Quench Chemical Etching *)
        bSlurryDeliveryValveCmd := FALSE;
        bDIW_FlushValveCmd := TRUE;
        bHighPressurePadRinseCmd := TRUE;
        
        (* Depressurize carrier membrane bladders completely *)
        x_ref[3] := 0.0;
        
        (* Transition: DIW flush quenches residual chemicals and cools pad *)
        IF rStateTimer_s >= 6.0 THEN
            nFsmCurrentState := STATE_CMP_CARRIER_VACUUM_DECHUCK;
            rStateTimer_s := 0.0;
            bStateFirstScan := TRUE;
        END_IF;

    (* -------------------------------------------------------------------------------------------------------------- *)
    (* STATE 9: CARRIER VACUUM DECHUCK & HIGH LIFT RETRACT                                                            *)
    (* -------------------------------------------------------------------------------------------------------------- *)
    STATE_CMP_CARRIER_VACUUM_DECHUCK:
        (* Engage Low Vacuum or Wafer Retain Membrane Pressure to Hold Wafer during Lift *)
        rCarrierZAxisDriveCmd_pct := 65.0;      (* Rapid Z-Axis High Lift *)
        x_ref[1] := 30.0;   (* Slow platen spin *)
        x_ref[2] := 0.0;    (* Stop carrier spin *)
        
        (* Transition: Carrier reaches Full Lift Retract Position (120 mm above pad) *)
        IF (rCarrierZAxisPosition_mm >= 115.0) AND (rStateTimer_s >= 4.0) THEN
            nFsmCurrentState := STATE_CMP_UNLOAD_CUP_TRANSFER;
            rStateTimer_s := 0.0;
            bStateFirstScan := TRUE;
        END_IF;

    (* -------------------------------------------------------------------------------------------------------------- *)
    (* STATE 10: UNLOAD CUP TRANSFER & CASSETTE RETURN                                                                *)
    (* -------------------------------------------------------------------------------------------------------------- *)
    STATE_CMP_UNLOAD_CUP_TRANSFER:
        (* Sweep Carrier to Clean Unload Cup Position *)
        rCarrierSweepVelocityCmd_mmps := -45.0;
        
        (* Once positioned over Unload Cup, release vacuum chuck and pulse DIW blow-off *)
        IF (rCarrierSweepPosition_mm <= 15.0) THEN
            bCarrierVacuumSolenoidCmd := FALSE;  (* De-chuck Wafer *)
            IF rStateTimer_s >= 5.0 THEN
                nFsmCurrentState := STATE_CMP_IN_SITU_PAD_CONDITIONING;
                rStateTimer_s := 0.0;
                bStateFirstScan := TRUE;
            END_IF;
        END_IF;

    (* -------------------------------------------------------------------------------------------------------------- *)
    (* STATE 11: IN-SITU PAD DIAMOND CONDITIONER SWEEP & TEXTURING                                                    *)
    (* -------------------------------------------------------------------------------------------------------------- *)
    STATE_CMP_IN_SITU_PAD_CONDITIONING:
        (* Full Platen Conditioning Sweep with DIW Lubrication *)
        x_ref[1] := 85.0;
        bCondArmInService := TRUE;
        rCondNominalDownforce_lbf := 10.5;
        rCondNominalSpeed_rpm := 105.0;
        bHighPressurePadRinseCmd := TRUE;
        
        (* Transition: Prescribed pad conditioning cycle time completed (18 s) *)
        IF rStateTimer_s >= 18.0 THEN
            nFsmCurrentState := STATE_CMP_POST_CONDITION_AE_AUDIT;
            rStateTimer_s := 0.0;
            bStateFirstScan := TRUE;
        END_IF;

    (* -------------------------------------------------------------------------------------------------------------- *)
    (* STATE 12: POST-CONDITION ACOUSTIC EMISSION PAD TEXTURE AUDIT                                                   *)
    (* -------------------------------------------------------------------------------------------------------------- *)
    STATE_CMP_POST_CONDITION_AE_AUDIT:
        (* Audit Pad Surface Asperity Health via AE signal *)
        bCondArmInService := FALSE;
        x_ref[1] := 0.0;
        bHighPressurePadRinseCmd := FALSE;
        
        (* Transition: Pad Texture Verified and Ready for Next Wafer *)
        IF (rCondAcousticRMS_Filtered_mV >= 30.0) AND (rPadGlazeIndex <= 0.25) AND (rStateTimer_s >= 3.0) THEN
            nFsmCurrentState := STATE_CMP_RECIPE_STEP_TRANSITION;
            rStateTimer_s := 0.0;
            bStateFirstScan := TRUE;
        ELSIF rStateTimer_s >= 5.0 THEN
            (* Degraded Pad Glaze Warning but proceed *)
            nFsmCurrentState := STATE_CMP_RECIPE_STEP_TRANSITION;
            rStateTimer_s := 0.0;
            bStateFirstScan := TRUE;
        END_IF;

    (* -------------------------------------------------------------------------------------------------------------- *)
    (* STATE 13: RECIPE STEP TRANSITION / MULTI-STEP COMPLETION                                                       *)
    (* -------------------------------------------------------------------------------------------------------------- *)
    STATE_CMP_RECIPE_STEP_TRANSITION:
        bProductionActive := FALSE;
        nFsmCurrentState := STATE_CMP_IDLE_STANDBY;
        rStateTimer_s := 0.0;
        bStateFirstScan := TRUE;

    (* -------------------------------------------------------------------------------------------------------------- *)
    (* STATE 14: EMERGENCY TRIP / VACUUM LOSS RECOVERY / WAFER SLIPPAGE TRIP                                          *)
    (* -------------------------------------------------------------------------------------------------------------- *)
    STATE_CMP_EMERGENCY_TRIP_VAC_LOSS:
        bProductionActive := FALSE;
        bEmergencyTripActive := TRUE;
        
        (* Immediate Safe Hardware Abort Actions *)
        rPlatenMotorTorqueCmd_pct := 0.0;
        rCarrierMotorTorqueCmd_pct := 0.0;
        x_ref[1] := 0.0;
        x_ref[2] := 0.0;
        
        (* Instantly dump membrane downforces to prevent wafer shattering *)
        rZonePressCmd_01_psi := 0.0;
        rZonePressCmd_02_psi := 0.0;
        rZonePressCmd_03_psi := 0.0;
        rZonePressCmd_04_psi := 0.0;
        rZonePressCmd_05_psi := 0.0;
        rRetainingRingPressCmd_psi := 0.0;
        
        (* Isolate chemical slurry and flood with DIW *)
        bSlurryDeliveryValveCmd := FALSE;
        bDIW_FlushValveCmd := TRUE;
        
        (* Conditioner Safe Park *)
        bCondArmInService := FALSE;
        rCondDownforceCmd_lbf := 0.0;
        rCondHeadSpeedCmd_rpm := 0.0;
        
        (* Retract Carrier Head slowly if vacuum still holding *)
        IF bWaferChucked_Carrier THEN
            rCarrierZAxisDriveCmd_pct := 20.0;
        ELSE
            rCarrierZAxisDriveCmd_pct := 0.0;  (* Wafer loose on pad: do NOT move carrier *)
        END_IF;
        
        (* Reset Condition: Operator Acknowledge and Alarm Reset *)
        IF bAlarmReset AND bEmergencyStop AND (NOT bAlarmCarrierVac_LL) THEN
            bEmergencyTripActive := FALSE;
            nFsmCurrentState := STATE_CMP_IDLE_STANDBY;
            rStateTimer_s := 0.0;
            bStateFirstScan := TRUE;
        END_IF;

END_CASE;

(* Update Output State Code *)
nOperationalState := nFsmCurrentState;
"""
