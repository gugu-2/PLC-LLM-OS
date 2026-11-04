# Generator part 9: Decoupled control, Alarms and closing
def get_alarms_logic():
    return """(* ============================================================================================= *)
(* SECTION 6: DECOUPLED CYCLONE SUMP FLOW/DENSITY CASCADE & BATTERY STAGING                      *)
(* ============================================================================================= *)

(* In manual or non-MPC auto mode, decoupled PI loops maintain sump level and slurry density *)
IF NOT bMPC_ControllerActive AND (iMachineState = 50) THEN
    (* Loop 1: Sump Level Error -> Variable Speed Slurry Pump Speed (Warman 650 MCR VFD) *)
    rTmpVal := rVoted_SumpLevel_Pct - 58.0; (* Deviation from 58% target level *)
    IF ABS(rTmpVal) > 1.5 THEN
        rCyclonePumpSpeedCmd_RPM := rCyclonePumpSpeedCmd_RPM + (rTmpVal * 0.120 * tScanTime_s);
    END_IF;
    IF rCyclonePumpSpeedCmd_RPM < 350.0 THEN
        rCyclonePumpSpeedCmd_RPM := 350.0;
    ELSIF rCyclonePumpSpeedCmd_RPM > 750.0 THEN
        rCyclonePumpSpeedCmd_RPM := 750.0;
    END_IF;

    (* Loop 2: Slurry Density Error -> Sump Dilution Trim Water Valve Stroke *)
    rTmpVal := rVoted_SlurryDensity_SG - 1.540; (* Deviation from 1.540 SG target *)
    IF ABS(rTmpVal) > 0.008 THEN
        (* High density -> Open dilution water valve *)
        rCycloneSumpWaterValveCmd_Pct := rCycloneSumpWaterValveCmd_Pct + (rTmpVal * 45.0 * tScanTime_s);
    END_IF;
    IF rCycloneSumpWaterValveCmd_Pct < 5.0 THEN
        rCycloneSumpWaterValveCmd_Pct := 5.0;
    ELSIF rCycloneSumpWaterValveCmd_Pct > 95.0 THEN
        rCycloneSumpWaterValveCmd_Pct := 95.0;
    END_IF;

    (* Loop 3: Hydrocyclone Battery Staging to hold manifold pressure in 85..95 kPa *)
    IF rVoted_ManifoldPress_kPa > 105.0 THEN
        IF iActiveCyclonesTargetCount < 12 THEN
            iActiveCyclonesTargetCount := iActiveCyclonesTargetCount + 1;
            abCycloneValveOpen_Cmd[iActiveCyclonesTargetCount] := TRUE;
        END_IF;
    ELSIF rVoted_ManifoldPress_kPa < 78.0 THEN
        IF iActiveCyclonesTargetCount > 6 THEN
            abCycloneValveOpen_Cmd[iActiveCyclonesTargetCount] := FALSE;
            iActiveCyclonesTargetCount := iActiveCyclonesTargetCount - 1;
        END_IF;
    END_IF;
END_IF;

(* ============================================================================================= *)
(* SECTION 7: ISA-18.2 MULTI-TIERED ALARM LADDER & 32-BIT DIAGNOSTIC WORD PACKING               *)
(* ============================================================================================= *)

(* Reset warnings on operator acknowledge *)
IF bAcknowledgeAlarms THEN
    dwAlarmWord_LowWarning := 16#0000_0000;
END_IF;

(* 7.1 Total Mill Weight / Trunnion Jacking Lift Alarms *)
IF rVoted_TotalMillWeight_tons >= rWeightTrip_HH_tons THEN
    rDebounce_WeightHH_s := rDebounce_WeightHH_s + tScanTime_s;
    IF rDebounce_WeightHH_s >= 2.0 THEN         (* 2 second debounce *)
        bMillOverfillingSlurrySpillTrip := TRUE;
        dwAlarmWord_HighTrip := dwAlarmWord_HighTrip OR 16#0000_0001; (* Bit 0: WEIGHT_HI_HI_TRIP *)
        rSAG_FreshFeedRateCmd_tph := 0.0;       (* Fast cut feed conveyor *)
    END_IF;
ELSIF rVoted_TotalMillWeight_tons <= (rWeightTrip_HH_tons - rWeightDeadband_tons) THEN
    rDebounce_WeightHH_s := 0.0;
    bMillOverfillingSlurrySpillTrip := FALSE;
END_IF;

IF rVoted_TotalMillWeight_tons >= rWeightWarn_H_tons THEN
    dwAlarmWord_LowWarning := dwAlarmWord_LowWarning OR 16#0000_0001; (* Bit 0: WEIGHT_HIGH_WARN *)
END_IF;

IF (rVoted_TotalMillWeight_tons <= rWeightWarn_L_tons) AND (iMachineState = 50) THEN
    dwAlarmWord_LowWarning := dwAlarmWord_LowWarning OR 16#0000_0002; (* Bit 1: WEIGHT_LOW_WARN *)
END_IF;

IF (rVoted_TotalMillWeight_tons <= rWeightTrip_LL_tons) AND (iMachineState = 50) THEN
    dwAlarmWord_HighTrip := dwAlarmWord_HighTrip OR 16#0000_0002; (* Bit 1: WEIGHT_LO_LO_TRIP *)
END_IF;

(* 7.2 Shell Acoustic Ear Direct Liner Impact Alarms *)
IF rCalculated_LinerImpactIndex >= rImpactTrip_HH_Pct THEN
    rDebounce_ImpactHH_s := rDebounce_ImpactHH_s + tScanTime_s;
    IF rDebounce_ImpactHH_s >= 1.0 THEN
        dwAlarmWord_HighTrip := dwAlarmWord_HighTrip OR 16#0000_0004; (* Bit 2: ACOUSTIC_IMPACT_HH_TRIP *)
        bCriticalImpactEmergencyActive := TRUE;
    END_IF;
ELSIF rCalculated_LinerImpactIndex <= (rImpactTrip_HH_Pct - rImpactDeadband_Pct) THEN
    rDebounce_ImpactHH_s := 0.0;
END_IF;

IF rCalculated_LinerImpactIndex >= rImpactWarn_H_Pct THEN
    dwAlarmWord_LowWarning := dwAlarmWord_LowWarning OR 16#0000_0004; (* Bit 2: ACOUSTIC_IMPACT_H_WARN *)
END_IF;

(* 7.3 Cyclone Feed Sump Slurry Level Alarms *)
IF rVoted_SumpLevel_Pct >= rSumpTrip_HH_Pct THEN
    dwAlarmWord_HighTrip := dwAlarmWord_HighTrip OR 16#0000_0008; (* Bit 3: SUMP_LEVEL_HH_TRIP *)
END_IF;

IF rVoted_SumpLevel_Pct >= rSumpWarn_H_Pct THEN
    dwAlarmWord_LowWarning := dwAlarmWord_LowWarning OR 16#0000_0008; (* Bit 3: SUMP_LEVEL_H_WARN *)
END_IF;

IF rVoted_SumpLevel_Pct <= rSumpWarn_L_Pct THEN
    dwAlarmWord_LowWarning := dwAlarmWord_LowWarning OR 16#0000_0010; (* Bit 4: SUMP_LEVEL_L_WARN *)
END_IF;

IF rVoted_SumpLevel_Pct <= rSumpTrip_LL_Pct THEN
    rDebounce_SumpLL_s := rDebounce_SumpLL_s + tScanTime_s;
    IF rDebounce_SumpLL_s >= 1.5 THEN
        bSumpCavitationProtectionActive := TRUE;
        dwAlarmWord_HighTrip := dwAlarmWord_HighTrip OR 16#0000_0010; (* Bit 4: SUMP_LEVEL_LL_TRIP *)
        rCyclonePumpSpeedCmd_RPM := 0.0;        (* Fast trip pump to prevent cavitation destruction *)
    END_IF;
ELSIF rVoted_SumpLevel_Pct >= (rSumpTrip_LL_Pct + rSumpDeadband_Pct) THEN
    rDebounce_SumpLL_s := 0.0;
    bSumpCavitationProtectionActive := FALSE;
END_IF;

(* 7.4 Cyclone Feed Slurry Density Alarms *)
IF rVoted_SlurryDensity_SG >= rDensityTrip_HH_SG THEN
    dwAlarmWord_HighTrip := dwAlarmWord_HighTrip OR 16#0000_0020; (* Bit 5: SLURRY_DENSITY_HH_ROPING_TRIP *)
END_IF;

IF rVoted_SlurryDensity_SG >= rDensityWarn_H_SG THEN
    dwAlarmWord_LowWarning := dwAlarmWord_LowWarning OR 16#0000_0020; (* Bit 5: SLURRY_DENSITY_H_WARN *)
END_IF;

IF rVoted_SlurryDensity_SG <= rDensityWarn_L_SG THEN
    dwAlarmWord_LowWarning := dwAlarmWord_LowWarning OR 16#0000_0040; (* Bit 6: SLURRY_DENSITY_L_WARN *)
END_IF;

IF rVoted_SlurryDensity_SG <= rDensityTrip_LL_SG THEN
    dwAlarmWord_HighTrip := dwAlarmWord_HighTrip OR 16#0000_0040; (* Bit 6: SLURRY_DENSITY_LL_TRIP *)
END_IF;

(* 7.5 Cyclone Distributor Manifold Pressure Alarms *)
IF rVoted_ManifoldPress_kPa >= rManifoldTrip_HH_kPa THEN
    rDebounce_ManifoldHH_s := rDebounce_ManifoldHH_s + tScanTime_s;
    IF rDebounce_ManifoldHH_s >= 2.0 THEN
        dwAlarmWord_HighTrip := dwAlarmWord_HighTrip OR 16#0000_0080; (* Bit 7: MANIFOLD_PRESS_HH_TRIP *)
    END_IF;
ELSIF rVoted_ManifoldPress_kPa <= (rManifoldTrip_HH_kPa - rManifoldDeadband_kPa) THEN
    rDebounce_ManifoldHH_s := 0.0;
END_IF;

IF rVoted_ManifoldPress_kPa >= rManifoldWarn_H_kPa THEN
    dwAlarmWord_LowWarning := dwAlarmWord_LowWarning OR 16#0000_0080; (* Bit 7: MANIFOLD_PRESS_H_WARN *)
END_IF;

IF rVoted_ManifoldPress_kPa <= rManifoldWarn_L_kPa THEN
    dwAlarmWord_LowWarning := dwAlarmWord_LowWarning OR 16#0000_0100; (* Bit 8: MANIFOLD_PRESS_L_WARN *)
END_IF;

IF rVoted_ManifoldPress_kPa <= rManifoldTrip_LL_kPa THEN
    dwAlarmWord_HighTrip := dwAlarmWord_HighTrip OR 16#0000_0100; (* Bit 8: MANIFOLD_PRESS_LL_TRIP *)
END_IF;

(* 7.6 Ring Motor Active Electrical Power Alarms *)
IF rVoted_RingMotorPower_MW >= rPowerTrip_HH_MW THEN
    rDebounce_PowerHH_s := rDebounce_PowerHH_s + tScanTime_s;
    IF rDebounce_PowerHH_s >= 1.5 THEN
        dwAlarmWord_HighTrip := dwAlarmWord_HighTrip OR 16#0000_0200; (* Bit 9: MOTOR_POWER_HH_TRIP *)
        rRingMotorSpeedCmd_RPM := 6.50;         (* Drop motor speed immediately to unload drive *)
    END_IF;
ELSIF rVoted_RingMotorPower_MW <= (rPowerTrip_HH_MW - rPowerDeadband_MW) THEN
    rDebounce_PowerHH_s := 0.0;
END_IF;

IF rVoted_RingMotorPower_MW >= rPowerWarn_H_MW THEN
    dwAlarmWord_LowWarning := dwAlarmWord_LowWarning OR 16#0000_0200; (* Bit 9: MOTOR_POWER_H_WARN *)
END_IF;

(* 7.7 Pack Process and Diagnostics Status Word *)
dwSystemStatusWord := (INT_TO_DWORD(iMachineState) AND 16#0000_0FFF);
IF bMPC_ControllerActive THEN
    dwSystemStatusWord := dwSystemStatusWord OR 16#0001_0000; (* Bit 16: MPC_ACTIVE *)
END_IF;
IF bCriticalImpactEmergencyActive THEN
    dwSystemStatusWord := dwSystemStatusWord OR 16#0002_0000; (* Bit 17: IMPACT_MITIGATION_ACTIVE *)
END_IF;
IF bMillOverfillingSlurrySpillTrip THEN
    dwSystemStatusWord := dwSystemStatusWord OR 16#0004_0000; (* Bit 18: OVERFILL_TRIP_ACTIVE *)
END_IF;
IF bSumpCavitationProtectionActive THEN
    dwSystemStatusWord := dwSystemStatusWord OR 16#0008_0000; (* Bit 19: SUMP_CAVITATION_ACTIVE *)
END_IF;
IF bGracefulDegradationActive THEN
    dwSystemStatusWord := dwSystemStatusWord OR 16#0010_0000; (* Bit 20: TMR_DEGRADED_MODE *)
END_IF;
IF bAutoMode THEN
    dwSystemStatusWord := dwSystemStatusWord OR 16#0020_0000; (* Bit 21: DCS_AUTO_MODE *)
END_IF;

END_FUNCTION_BLOCK
"""

print("Alarms module loaded.")
