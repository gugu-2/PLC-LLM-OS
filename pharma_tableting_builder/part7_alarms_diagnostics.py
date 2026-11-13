# pharma_tableting_builder/part7_alarms_diagnostics.py

def get_part7():
    return """(* === PHASE 6: ISA-18.2 MULTI-TIER ALARMS & 32-BIT BIT-PACKED STATUS WORDS === *)

(* 1. Rate-of-Change (RoC) Calculations *)
rMainCompForce_RoC_kNps := ABS(rVotedMainCompForce_kN - rPrevMainCompForce_kN) / T_CYCLE_SEC;
rPrevMainCompForce_kN := rVotedMainCompForce_kN;

rMoistLOD_RoC_pctps := ABS(rVotedMoistureLOD_pct - rPrevMoistLOD_pct) / T_CYCLE_SEC;
rPrevMoistLOD_pct := rVotedMoistureLOD_pct;

(* 2. Main Compression Punch Force Alarms with Deadband Hysteresis *)
IF rVotedMainCompForce_kN >= rSP_MainForce_HH_kN THEN
    bAlarmHighHighMainForce := TRUE;
    bTripLatched_MainForce_HH := TRUE; (* Critical mechanical overload latch *)
ELSIF rVotedMainCompForce_kN <= (rSP_MainForce_HH_kN - rDB_MainForce_kN) THEN
    bAlarmHighHighMainForce := FALSE;
END_IF;

IF rVotedMainCompForce_kN <= rSP_MainForce_LL_kN THEN
    bAlarmLowLowMainForce := TRUE;
    bTripLatched_MainForce_LL := TRUE;
ELSIF rVotedMainCompForce_kN >= (rSP_MainForce_LL_kN + rDB_MainForce_kN) THEN
    bAlarmLowLowMainForce := FALSE;
END_IF;

(* 3. Fluid Bed Residual Moisture Content (% LOD) Alarms *)
IF rVotedMoistureLOD_pct >= rSP_MoistLOD_H_pct THEN
    bAlarmHighMoistureLOD := TRUE;
    IF rVotedMoistureLOD_pct >= rSP_MoistLOD_HH_pct THEN
        bTripLatched_Moist_HH := TRUE;
    END_IF;
ELSIF rVotedMoistureLOD_pct <= (rSP_MoistLOD_H_pct - rDB_MoistLOD_pct) THEN
    bAlarmHighMoistureLOD := FALSE;
END_IF;

IF rVotedMoistureLOD_pct <= rSP_MoistLOD_L_pct THEN
    bAlarmLowMoistureLOD := TRUE;
    IF rVotedMoistureLOD_pct <= rSP_MoistLOD_LL_pct THEN
        bTripLatched_Moist_LL := TRUE;
    END_IF;
ELSIF rVotedMoistureLOD_pct >= (rSP_MoistLOD_L_pct + rDB_MoistLOD_pct) THEN
    bAlarmLowMoistureLOD := FALSE;
END_IF;

(* 4. Twin-Screw Granulator Barrel Torque & Viscous Dough Trip *)
IF (rGranulatorScrewTorque_Nm >= 48.0) OR (rObservedLiquidSolidRatio_pct >= rSP_LS_Ratio_HH_pct) THEN
    bAlarmHighGranulatorTorque := TRUE;
    bTripLatched_GranulatorTorque := TRUE;
ELSIF (rGranulatorScrewTorque_Nm <= 38.0) AND (rObservedLiquidSolidRatio_pct <= (rSP_LS_Ratio_HH_pct - rDB_LS_Ratio_pct)) THEN
    bAlarmHighGranulatorTorque := FALSE;
END_IF;

(* 5. Feeder Starvation Alarm *)
IF bProductionActive AND (rVotedFeederFlow_kgh < (rRecipeTargetFeederFlow_kgh * 0.70)) THEN
    bAlarmFeederStarvation := TRUE;
ELSIF rVotedFeederFlow_kgh >= (rRecipeTargetFeederFlow_kgh * 0.85) THEN
    bAlarmFeederStarvation := FALSE;
END_IF;

(* 6. Rotary Press Turret Speed Following Deviation *)
IF bProductionActive AND (ABS(rVotedTurretSpeed_rpm - rRecipeTargetTurretSpeed_rpm) > 2.50) THEN
    bAlarmTurretSpeedDeviation := TRUE;
ELSIF ABS(rVotedTurretSpeed_rpm - rRecipeTargetTurretSpeed_rpm) <= 1.00 THEN
    bAlarmTurretSpeedDeviation := FALSE;
END_IF;

(* 7. Tablet Ejection Friction & Die Wall Binding *)
IF rTabletEjectionForce_N >= 250.0 THEN
    bAlarmEjectionForceHigh := TRUE;
ELSIF rTabletEjectionForce_N <= 200.0 THEN
    bAlarmEjectionForceHigh := FALSE;
END_IF;

(* 8. Operator Alarm Reset Permissive Logic *)
IF bAlarmReset THEN
    IF rVotedMainCompForce_kN < (rSP_MainForce_HH_kN - rDB_MainForce_kN) THEN
        bTripLatched_MainForce_HH := FALSE;
    END_IF;
    IF rVotedMainCompForce_kN > (rSP_MainForce_LL_kN + rDB_MainForce_kN) THEN
        bTripLatched_MainForce_LL := FALSE;
    END_IF;
    IF rVotedMoistureLOD_pct < (rSP_MoistLOD_HH_pct - rDB_MoistLOD_pct) THEN
        bTripLatched_Moist_HH := FALSE;
    END_IF;
    IF rGranulatorScrewTorque_Nm < 38.0 THEN
        bTripLatched_GranulatorTorque := FALSE;
    END_IF;
END_IF;

(* 9. Assemble 32-Bit Bit-Packed Tableting Status Word (dwTabletingStatusWord) *)
dwTabletingStatusWord := 16#00000000;
IF bSystemEnable THEN dwTabletingStatusWord := dwTabletingStatusWord OR 16#00000001; END_IF;
IF bProductionActive THEN dwTabletingStatusWord := dwTabletingStatusWord OR 16#00000002; END_IF;
IF bEmergencyStop THEN dwTabletingStatusWord := dwTabletingStatusWord OR 16#00000004; END_IF;
IF bSystemReady THEN dwTabletingStatusWord := dwTabletingStatusWord OR 16#00000008; END_IF;
IF bBatchDrainingActive THEN dwTabletingStatusWord := dwTabletingStatusWord OR 16#00000010; END_IF;
IF bBatchDrainComplete THEN dwTabletingStatusWord := dwTabletingStatusWord OR 16#00000020; END_IF;
IF bWarmupComplete THEN dwTabletingStatusWord := dwTabletingStatusWord OR 16#00000040; END_IF;
IF bDryBlendEquilibrated THEN dwTabletingStatusWord := dwTabletingStatusWord OR 16#00000080; END_IF;
IF bNucleationEstablished THEN dwTabletingStatusWord := dwTabletingStatusWord OR 16#00000100; END_IF;
IF bMoistureStabilized THEN dwTabletingStatusWord := dwTabletingStatusWord OR 16#00000200; END_IF;
IF bFeederShoeFilled THEN dwTabletingStatusWord := dwTabletingStatusWord OR 16#00000400; END_IF;
IF bTurretSpeedSynchronized THEN dwTabletingStatusWord := dwTabletingStatusWord OR 16#00000800; END_IF;
IF bContinuousTabletingSteady THEN dwTabletingStatusWord := dwTabletingStatusWord OR 16#00001000; END_IF;
IF bRejectValveActive THEN dwTabletingStatusWord := dwTabletingStatusWord OR 16#00002000; END_IF;
IF bFeeder_ChA_Valid THEN dwTabletingStatusWord := dwTabletingStatusWord OR 16#00004000; END_IF;
IF bFeeder_ChB_Valid THEN dwTabletingStatusWord := dwTabletingStatusWord OR 16#00008000; END_IF;
IF bFeeder_ChC_Valid THEN dwTabletingStatusWord := dwTabletingStatusWord OR 16#00010000; END_IF;
IF bMoist_ChA_Valid THEN dwTabletingStatusWord := dwTabletingStatusWord OR 16#00020000; END_IF;
IF bMoist_ChB_Valid THEN dwTabletingStatusWord := dwTabletingStatusWord OR 16#00040000; END_IF;
IF bMoist_ChC_Valid THEN dwTabletingStatusWord := dwTabletingStatusWord OR 16#00080000; END_IF;
IF bMainComp_ChA_Valid THEN dwTabletingStatusWord := dwTabletingStatusWord OR 16#00100000; END_IF;
IF bMainComp_ChB_Valid THEN dwTabletingStatusWord := dwTabletingStatusWord OR 16#00200000; END_IF;
IF bMainComp_ChC_Valid THEN dwTabletingStatusWord := dwTabletingStatusWord OR 16#00400000; END_IF;
(* Encode 4-bit operational state in bits 24 to 27 *)
dwTabletingStatusWord := dwTabletingStatusWord OR SHL(INT_TO_DWORD(nOperationalState AND 16#0F), 24);

(* 10. Assemble 32-Bit Bit-Packed Tableting Diagnostic Word (dwTabletingDiagnosticWord) *)
dwTabletingDiagnosticWord := 16#00000000;
IF bAlarmHighHighMainForce THEN dwTabletingDiagnosticWord := dwTabletingDiagnosticWord OR 16#00000001; END_IF;
IF bAlarmLowLowMainForce THEN dwTabletingDiagnosticWord := dwTabletingDiagnosticWord OR 16#00000002; END_IF;
IF bAlarmHighMoistureLOD THEN dwTabletingDiagnosticWord := dwTabletingDiagnosticWord OR 16#00000004; END_IF;
IF bAlarmLowMoistureLOD THEN dwTabletingDiagnosticWord := dwTabletingDiagnosticWord OR 16#00000008; END_IF;
IF bAlarmHighGranulatorTorque THEN dwTabletingDiagnosticWord := dwTabletingDiagnosticWord OR 16#00000010; END_IF;
IF bAlarmFeederStarvation THEN dwTabletingDiagnosticWord := dwTabletingDiagnosticWord OR 16#00000020; END_IF;
IF bAlarmTurretSpeedDeviation THEN dwTabletingDiagnosticWord := dwTabletingDiagnosticWord OR 16#00000040; END_IF;
IF bAlarmEjectionForceHigh THEN dwTabletingDiagnosticWord := dwTabletingDiagnosticWord OR 16#00000080; END_IF;
IF bTripLatched_EmergencyStop THEN dwTabletingDiagnosticWord := dwTabletingDiagnosticWord OR 16#00000100; END_IF;
IF bTripLatched_MainForce_HH THEN dwTabletingDiagnosticWord := dwTabletingDiagnosticWord OR 16#00000200; END_IF;
IF bTripLatched_Moist_HH THEN dwTabletingDiagnosticWord := dwTabletingDiagnosticWord OR 16#00000400; END_IF;
IF nFeeder_VotingMode < 3 THEN dwTabletingDiagnosticWord := dwTabletingDiagnosticWord OR 16#00000800; END_IF;
IF nMoist_VotingMode < 3 THEN dwTabletingDiagnosticWord := dwTabletingDiagnosticWord OR 16#00001000; END_IF;
IF nMainComp_VotingMode < 3 THEN dwTabletingDiagnosticWord := dwTabletingDiagnosticWord OR 16#00002000; END_IF;
IF nTurret_VotingMode < 3 THEN dwTabletingDiagnosticWord := dwTabletingDiagnosticWord OR 16#00004000; END_IF;
IF nFBDiff_VotingMode < 3 THEN dwTabletingDiagnosticWord := dwTabletingDiagnosticWord OR 16#00008000; END_IF;
IF rMainCompForce_RoC_kNps > rSP_MainForce_RoC_Max_kNps THEN dwTabletingDiagnosticWord := dwTabletingDiagnosticWord OR 16#00010000; END_IF;

END_FUNCTION_BLOCK
"""
