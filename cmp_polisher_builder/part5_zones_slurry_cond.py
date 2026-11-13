# cmp_polisher_builder/part5_zones_slurry_cond.py

def get_part5():
    return """(*
========================================================================================================================
  PHASE 3B: 5-ZONE CONCENTRIC CARRIER HEAD DYNAMICS & SLURRY/CONDITIONER CASCADE LOOPS
  DYNAMIC EDGE ROLL-OFF (ERO) SUPPRESSION & HARMONIC DIAMOND CONDITIONER SWEEP
========================================================================================================================
*)
(* ------------------------------------------------------------------------------------------------------------------ *)
(* 1. 5-ZONE CARRIER HEAD DYNAMIC PRESSURE PROFILE & RETAINING RING COMPENSATION                                     *)
(* ------------------------------------------------------------------------------------------------------------------ *)
IF bProductionActive AND (nOperationalState >= STATE_CMP_LOW_PRESSURE_TOUCHDOWN) AND (nOperationalState <= STATE_CMP_SOFT_LANDING_OVERPOLISH) THEN
    (* Base downforce pressure from MPC controller u_ctrl[3] scaled to operating range 0.0 to 6.0 psi *)
    rTempPressAvg := (u_ctrl[3] / 100.0) * 6.0;
    
    (* Fine Zone Recipe Scaling Profile *)
    rZoneTarget_01_psi := rTempPressAvg * 0.965;    (* Zone 1 Center (0-40mm) *)
    rZoneTarget_02_psi := rTempPressAvg * 0.985;    (* Zone 2 Inner-Mid (40-80mm) *)
    rZoneTarget_03_psi := rTempPressAvg * 1.000;    (* Zone 3 Mid (80-115mm) *)
    rZoneTarget_04_psi := rTempPressAvg * 1.025;    (* Zone 4 Outer-Mid (115-140mm) *)
    rZoneTarget_05_psi := rTempPressAvg * 1.070;    (* Zone 5 Edge (140-150mm) *)
    
    (* Edge Roll-Off (ERO) Dynamic Retaining Ring Downforce Modulation *)
    (* High pad rebound requires elevated retaining ring pressure to suppress edge over-polishing *)
    rRetainingRingTarget_psi := rZoneTarget_05_psi * 1.28 + rEdgeRollOffFactor * (rZonePress_PV_05_psi - rZonePress_PV_01_psi);
    rRetainingRingTarget_psi := MAX(1.5, MIN(6.5, rRetainingRingTarget_psi));
    
    (* Zone 1 Center PI Pressure Regulator *)
    rZoneError_01_psi := rZoneTarget_01_psi - rZonePress_PV_01_psi;
    rZoneInt_01_psi := rZoneInt_01_psi + rZoneError_01_psi * T_CYCLE_SEC;
    rZoneInt_01_psi := MAX(-0.8, MIN(0.8, rZoneInt_01_psi));
    rZonePressCmd_01_psi := rZoneTarget_01_psi + rKp_ZonePressure * rZoneError_01_psi + rKi_ZonePressure * rZoneInt_01_psi;
    rZonePressCmd_01_psi := MAX(0.2, MIN(6.5, rZonePressCmd_01_psi));
    
    (* Zone 2 Inner-Mid PI Pressure Regulator *)
    rZoneError_02_psi := rZoneTarget_02_psi - rZonePress_PV_02_psi;
    rZoneInt_02_psi := rZoneInt_02_psi + rZoneError_02_psi * T_CYCLE_SEC;
    rZoneInt_02_psi := MAX(-0.8, MIN(0.8, rZoneInt_02_psi));
    rZonePressCmd_02_psi := rZoneTarget_02_psi + rKp_ZonePressure * rZoneError_02_psi + rKi_ZonePressure * rZoneInt_02_psi;
    rZonePressCmd_02_psi := MAX(0.2, MIN(6.5, rZonePressCmd_02_psi));
    
    (* Zone 3 Mid PI Pressure Regulator *)
    rZoneError_03_psi := rZoneTarget_03_psi - rZonePress_PV_03_psi;
    rZoneInt_03_psi := rZoneInt_03_psi + rZoneError_03_psi * T_CYCLE_SEC;
    rZoneInt_03_psi := MAX(-0.8, MIN(0.8, rZoneInt_03_psi));
    rZonePressCmd_03_psi := rZoneTarget_03_psi + rKp_ZonePressure * rZoneError_03_psi + rKi_ZonePressure * rZoneInt_03_psi;
    rZonePressCmd_03_psi := MAX(0.2, MIN(6.5, rZonePressCmd_03_psi));
    
    (* Zone 4 Outer-Mid PI Pressure Regulator *)
    rZoneError_04_psi := rZoneTarget_04_psi - rZonePress_PV_04_psi;
    rZoneInt_04_psi := rZoneInt_04_psi + rZoneError_04_psi * T_CYCLE_SEC;
    rZoneInt_04_psi := MAX(-0.8, MIN(0.8, rZoneInt_04_psi));
    rZonePressCmd_04_psi := rZoneTarget_04_psi + rKp_ZonePressure * rZoneError_04_psi + rKi_ZonePressure * rZoneInt_04_psi;
    rZonePressCmd_04_psi := MAX(0.2, MIN(6.5, rZonePressCmd_04_psi));
    
    (* Zone 5 Edge PI Pressure Regulator *)
    rZoneError_05_psi := rZoneTarget_05_psi - rZonePress_PV_05_psi;
    rZoneInt_05_psi := rZoneInt_05_psi + rZoneError_05_psi * T_CYCLE_SEC;
    rZoneInt_05_psi := MAX(-0.8, MIN(0.8, rZoneInt_05_psi));
    rZonePressCmd_05_psi := rZoneTarget_05_psi + rKp_ZonePressure * rZoneError_05_psi + rKi_ZonePressure * rZoneInt_05_psi;
    rZonePressCmd_05_psi := MAX(0.2, MIN(6.5, rZonePressCmd_05_psi));
    
    (* Retaining Ring PI Pressure Regulator *)
    rRetainingRingError_psi := rRetainingRingTarget_psi - rRetainingRingPress_PV_psi;
    rRetainingRingInt_psi := rRetainingRingInt_psi + rRetainingRingError_psi * T_CYCLE_SEC;
    rRetainingRingInt_psi := MAX(-1.2, MIN(1.2, rRetainingRingInt_psi));
    rRetainingRingPressCmd_psi := rRetainingRingTarget_psi + rKp_ZonePressure * 1.15 * rRetainingRingError_psi + rKi_ZonePressure * rRetainingRingInt_psi;
    rRetainingRingPressCmd_psi := MAX(0.5, MIN(7.5, rRetainingRingPressCmd_psi));
ELSE
    (* Depressurize membrane when not in active wafer contact *)
    rZonePressCmd_01_psi := 0.0;
    rZonePressCmd_02_psi := 0.0;
    rZonePressCmd_03_psi := 0.0;
    rZonePressCmd_04_psi := 0.0;
    rZonePressCmd_05_psi := 0.0;
    rRetainingRingPressCmd_psi := 0.0;
    rZoneInt_01_psi := 0.0;
    rZoneInt_02_psi := 0.0;
    rZoneInt_03_psi := 0.0;
    rZoneInt_04_psi := 0.0;
    rZoneInt_05_psi := 0.0;
    rRetainingRingInt_psi := 0.0;
END_IF;

(* ------------------------------------------------------------------------------------------------------------------ *)
(* 2. CHEMICAL SLURRY DELIVERY CASCADE & IN-LINE FLUID REGULATION                                                    *)
(* ------------------------------------------------------------------------------------------------------------------ *)
IF bProductionActive AND (nOperationalState >= STATE_CMP_LOW_PRESSURE_TOUCHDOWN) AND (nOperationalState <= STATE_CMP_SOFT_LANDING_OVERPOLISH) THEN
    bSlurryDeliveryValveCmd := TRUE;
    bDIW_FlushValveCmd := FALSE;
    
    (* Peristaltic Slurry Pump Closed-Loop Flow PI Regulator *)
    rSlurryFlowError_mLpm := rSlurryFlowTarget_mLpm - rSlurryFlow_PV_mLpm;
    rSlurryFlowInt_mLpm := rSlurryFlowInt_mLpm + rSlurryFlowError_mLpm * T_CYCLE_SEC;
    rSlurryFlowInt_mLpm := MAX(-40.0, MIN(40.0, rSlurryFlowInt_mLpm));
    rSlurryPumpFlowCmd_mLpm := rSlurryFlowTarget_mLpm + rKp_SlurryPump * rSlurryFlowError_mLpm + rKi_SlurryPump * rSlurryFlowInt_mLpm;
    rSlurryPumpFlowCmd_mLpm := MAX(150.0, MIN(400.0, rSlurryPumpFlowCmd_mLpm));
    
    (* Slurry Delivery Arm Radial Swing Angle Sweep to Prevent Dry Zones *)
    rSlurryArmSweepAngleCmd_deg := 42.0 + 8.5 * SIN(rCondSweepPhase_rad * 0.45);
ELSE
    bSlurryDeliveryValveCmd := FALSE;
    rSlurryPumpFlowCmd_mLpm := 0.0;
    rSlurryFlowInt_mLpm := 0.0;
    rSlurryArmSweepAngleCmd_deg := 30.0;    (* Parked Dispense Angle *)
END_IF;

(* High-Pressure DIW Flush Valve in Rinse State *)
IF (nOperationalState = STATE_CMP_DIW_HIGH_PRESSURE_FLUSH) OR (nOperationalState = STATE_CMP_IN_SITU_PAD_CONDITIONING) THEN
    bDIW_FlushValveCmd := TRUE;
    bHighPressurePadRinseCmd := TRUE;
ELSE
    bHighPressurePadRinseCmd := FALSE;
END_IF;

(* ------------------------------------------------------------------------------------------------------------------ *)
(* 3. DIAMOND CONDITIONER HARMONIC RECIPROCATING SWEEP & ACOUSTIC EMISSION MONITORING                                *)
(* ------------------------------------------------------------------------------------------------------------------ *)
IF (nOperationalState = STATE_CMP_STEADY_STATE_POLISH) OR (nOperationalState = STATE_CMP_IN_SITU_PAD_CONDITIONING) THEN
    bCondArmInService := TRUE;
    rCondHeadSpeedCmd_rpm := rCondNominalSpeed_rpm;
    
    (* Harmonic Phase Integration for Sinusoidal Radial Sweep *)
    rCondSweepPhase_rad := rCondSweepPhase_rad + 2.0 * 3.14159265 * rCondSweepFrequency_Hz * T_CYCLE_SEC;
    IF rCondSweepPhase_rad >= (2.0 * 3.14159265) THEN
        rCondSweepPhase_rad := rCondSweepPhase_rad - (2.0 * 3.14159265);
    END_IF;
    
    (* Radial Sweep Position Profile: Smooth sinusoidal motion from inner track to outer pad perimeter *)
    rCondSweepVelocityCmd_mmps := 45.0 * COS(rCondSweepPhase_rad);
    
    (* Closed-Loop Downforce PI Regulation for Conditioner Head *)
    rCondDownforceError_lbf := rCondNominalDownforce_lbf - rCondDownforce_PV_lbf;
    rCondDownforceInt_lbf := rCondDownforceInt_lbf + rCondDownforceError_lbf * T_CYCLE_SEC;
    rCondDownforceInt_lbf := MAX(-2.5, MIN(2.5, rCondDownforceInt_lbf));
    rCondDownforceCmd_lbf := rCondNominalDownforce_lbf + 0.35 * rCondDownforceError_lbf + 0.12 * rCondDownforceInt_lbf;
    rCondDownforceCmd_lbf := MAX(2.0, MIN(14.0, rCondDownforceCmd_lbf));
    
    (* Acoustic Emission (AE) High-Frequency Piezo Sensor Signal Conditioning *)
    rCondAcousticRMS_Filtered_mV := rCondAcousticRMS_Filtered_mV * 0.95 + rCondAcousticEmission_RMS_mV * 0.05;
    
    (* Pad Glaze Index Accumulation: Drop in AE energy correlates with pad pore clogging *)
    IF rCondAcousticRMS_Filtered_mV < 25.0 THEN
        rPadGlazeIndex := MIN(1.0, rPadGlazeIndex + 0.0002);
    ELSE
        rPadGlazeIndex := MAX(0.0, rPadGlazeIndex - 0.0005);
    END_IF;
    
    (* Cumulative Diamond Cutting Work Accumulator: Work = F_downforce * V_cutting * dt *)
    rDiamondWearAccumulator := rDiamondWearAccumulator + (rCondDownforce_PV_lbf * (rCondSpeed_PV_rpm * 0.1047 * 0.05) * T_CYCLE_SEC * 1.0E-4);
ELSE
    bCondArmInService := FALSE;
    rCondHeadSpeedCmd_rpm := 0.0;
    rCondDownforceCmd_lbf := 0.0;
    rCondSweepVelocityCmd_mmps := 0.0;
    rCondDownforceInt_lbf := 0.0;
END_IF;
"""
