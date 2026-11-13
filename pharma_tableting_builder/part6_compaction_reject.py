# pharma_tableting_builder/part6_compaction_reject.py

def get_part6():
    return """(* === PHASE 5: DYNAMIC COMPACT HARDNESS, THICKNESS & POROSITY DE-COUPLING OBSERVER & HIGH-SPEED REJECT JET === *)

(* 1. First-Principles Heckel Compaction Mechanics *)
(* Punch face area: A = pi * (D/2)^2 = 78.5398 mm2 for 10 mm punch tip *)
rPunchArea_mm2 := PI_CONST * (rPunchDiameter_mm * 0.5) * (rPunchDiameter_mm * 0.5);

(* Compaction stress P_comp in MPa = (F_kN * 1000 N/kN) / Area_mm2 *)
rMainCompPressure_MPa := (rVotedMainCompForce_kN * 1000.0) / MAX(1.0, rPunchArea_mm2);

(* Heckel relative density: D = 1 - exp(-(K*P + A)) *)
(* Linearized series approximation around nominal compaction pressure P0 = 413 MPa *)
rRelativeDensity_D := 0.620 + (1.0 / rHeckelYieldPressure_MPa) * rMainCompPressure_MPa * 0.125;
IF rRelativeDensity_D > 0.985 THEN
    rRelativeDensity_D := 0.985;
ELSIF rRelativeDensity_D < 0.600 THEN
    rRelativeDensity_D := 0.600;
END_IF;

(* Tablet Porosity Calculation: epsilon = (1 - D) * 100% *)
rObservedTabletPorosity_pct := (1.0 - rRelativeDensity_D) * 100.0;

(* 2. Angular Turret Tracking & Punch Station Indexing (Stations 1 to 48) *)
IF (rTurretShaftResolverAngle_deg >= 0.0) AND (rTurretShaftResolverAngle_deg < 360.0) THEN
    nCurrentTurretPunchIndex := TRUNC(rTurretShaftResolverAngle_deg / rAngularStationStep_deg) + 1;
ELSE
    nCurrentTurretPunchIndex := 1;
END_IF;

IF nCurrentTurretPunchIndex > 48 THEN
    nCurrentTurretPunchIndex := 48;
ELSIF nCurrentTurretPunchIndex < 1 THEN
    nCurrentTurretPunchIndex := 1;
END_IF;

(* 3. Capture Peak Forces for Active Punch Station Under Rollers *)
arrStationPeakForce[nCurrentTurretPunchIndex] := rVotedMainCompForce_kN;
arrStationPreCompForce[nCurrentTurretPunchIndex] := rVotedPreCompForce_kN;

(* 4. Out-of-Specification Detection for Individual Tablet *)
IF bProductionActive THEN
    (* Evaluate Deviation Against Production Spec Limits (+- 10.0% Reject Gate Threshold) *)
    IF (ABS(rVotedMainCompForce_kN - rRecipeTargetMainCompForce_kN) > (rRecipeTargetMainCompForce_kN * 0.100)) OR
       (rVotedPreCompForce_kN < (rRecipeTargetPreCompForce_kN * 0.350)) OR
       (rVotedMoistureLOD_pct > rSP_MoistLOD_HH_pct) OR
       (rVotedMoistureLOD_pct < rSP_MoistLOD_LL_pct) THEN
        
        arrStationRejectFlag[nCurrentTurretPunchIndex] := TRUE;
        arrStationConsecutiveRejects[nCurrentTurretPunchIndex] := arrStationConsecutiveRejects[nCurrentTurretPunchIndex] + 1;
    ELSE
        arrStationRejectFlag[nCurrentTurretPunchIndex] := FALSE;
        arrStationConsecutiveRejects[nCurrentTurretPunchIndex] := 0;
        diTotalGoodTabletsProduced := diTotalGoodTabletsProduced + 1;
    END_IF;
END_IF;

(* 5. Predictive Downstream Punch Arrival at Reject Chute *)
(* The high-speed pneumatic blow-off jet is located 120 degrees downstream of main compaction (16 stations) *)
nRejectStationTargetIndex := nCurrentTurretPunchIndex - 16;
IF nRejectStationTargetIndex < 1 THEN
    nRejectStationTargetIndex := nRejectStationTargetIndex + 48;
END_IF;

(* 6. High-Speed Pneumatic Jet Actuation (< 10 ms fast pulse) *)
IF arrStationRejectFlag[nRejectStationTargetIndex] OR bRejectGateManualTestCmd THEN
    bRejectValveActive := TRUE;
    rRejectPulseTimer_s := 0.008; (* 8.0 ms precision pulse duration *)
    nActiveRejectPunchStation := nRejectStationTargetIndex;
    diTotalRejectedTabletsCount := diTotalRejectedTabletsCount + 1;
    arrStationRejectFlag[nRejectStationTargetIndex] := FALSE; (* Clear reject flag after dispatch *)
END_IF;

(* Pulse Timer Decay *)
IF rRejectPulseTimer_s > 0.0 THEN
    rRejectPulseTimer_s := rRejectPulseTimer_s - T_CYCLE_SEC;
    bHighSpeedRejectGateSolenoidCmd := TRUE;
ELSE
    bHighSpeedRejectGateSolenoidCmd := FALSE;
    bRejectValveActive := FALSE;
END_IF;

(* 7. Tooling Degradation Interlock: Check for Persistent Tooling Failure on Any Single Station *)
FOR i := 1 TO 48 DO
    IF arrStationConsecutiveRejects[i] >= 3 THEN
        (* 3 consecutive out-of-spec tablets on the same punch station indicates damaged punch tip or sticking *)
        bAlarmEjectionForceHigh := TRUE;
    END_IF;
END_FOR;
"""
