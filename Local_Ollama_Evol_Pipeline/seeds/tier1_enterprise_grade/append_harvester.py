import json

prompt = """You are acting as a Lead Agricultural Engineer for an autonomous farming cooperative. Evolve a basic steering block into a Combine Harvester Autonomous Header Controller in IEC 61131-3 Structured Text. Technical Specs: 
1. Ground-penetrating radar terrain mapping for cut-height optimization. 
2. Threshing drum speed and concave clearance dynamic adjustment based on grain moisture sensors. 
3. Sieve loss acoustic monitoring."""

assistant_response = """(*
================================================================================================
  ENTERPRISE AUTOMATION LIBRARY - AUTONOMOUS HARVESTING SYSTEMS
================================================================================================
  Block:    FB_CombineHeaderController_Advanced
  Version:  3.1.4_ENTERPRISE
  Author:   Lumina Synthetic Data Architect
  
  Description:
  Advanced autonomous header and threshing controller for Combine Harvesters.
  Integrates multi-sensor fusion:
  1. Ground-penetrating radar (GPR) array for predictive terrain mapping & cut-height optimization.
  2. In-line grain moisture sensor telemetry for dynamic threshing drum speed & concave clearance.
  3. Acoustic sieve loss monitoring (grain impact detection) to regulate fan speed.

  Safety and robustness logic implemented as per ISO 25119 for agricultural machinery.
================================================================================================
*)
FUNCTION_BLOCK FB_CombineHeaderController_Advanced

VAR_INPUT
    bEnable                 : BOOL;   (* System Enable *)
    bEmergencyStop          : BOOL;   (* Safety Interlock *)
    
    (* Environmental & Machine Telemetry *)
    aRadarTerrainProfile    : ARRAY[0..31] OF REAL; (* Forward GPR terrain height predictions (mm) *)
    fGrainMoisture          : REAL;   (* Grain moisture content (%) *)
    fAcousticSieveLoss      : REAL;   (* Sieve loss sensor raw impact rate (hits/sec) *)
    
    (* Actuator Feedback *)
    fActHeaderHeight        : REAL;   (* Current header height (mm) *)
    fActDrumSpeed           : REAL;   (* Current threshing drum speed (RPM) *)
    fActConcaveClearance    : REAL;   (* Current concave clearance (mm) *)
    
    (* Operator Parameters *)
    fBaseCutHeight          : REAL;   (* Operator requested base cut height (mm) *)
    fMaxSieveLossLimit      : REAL;   (* Acceptable loss threshold *)
END_VAR

VAR_OUTPUT
    (* Actuator Commands *)
    fCmdHeaderHeight        : REAL;   (* Target header height (mm) *)
    fCmdDrumSpeed           : REAL;   (* Target threshing drum speed (RPM) *)
    fCmdConcaveClearance    : REAL;   (* Target concave clearance (mm) *)
    fCmdCleaningFanSpeed    : REAL;   (* Target cleaning fan speed (RPM) *)
    
    (* Status & Diagnostics *)
    bSieveLossAlarm         : BOOL;
    bMoistureWarning        : BOOL;
    iState                  : INT;    (* 0: Off, 1: Init, 2: Active, 99: Fault *)
    sDiagnosticMessage      : STRING(80);
END_VAR

VAR
    (* Internal State *)
    i                 : INT;
    fAvgTerrainOffset : REAL;
    fTerrainTrend     : REAL;
    fLossFiltered     : REAL;
    fAlphaFilter      : REAL := 0.2; (* Low pass filter coefficient *)
    
    (* Tuning Parameters - Threshing Curve *)
    fBaseDrumSpeed    : REAL := 750.0; (* RPM for standard dry crop *)
    fBaseConcave      : REAL := 15.0;  (* mm for standard dry crop *)
    
    fbLossDelay       : TON;
END_VAR

(* Implementation *)
IF bEmergencyStop THEN
    iState := 99;
    fCmdHeaderHeight := 800.0; (* Safe high position *)
    fCmdDrumSpeed := 0.0;
    fCmdConcaveClearance := 40.0; (* Fully open *)
    fCmdCleaningFanSpeed := 0.0;
    sDiagnosticMessage := 'EMERGENCY STOP ACTIVE - SAFE STATE FORCED';
    bSieveLossAlarm := FALSE;
    RETURN;
END_IF;

IF NOT bEnable THEN
    iState := 0;
    sDiagnosticMessage := 'SYSTEM DISABLED';
    RETURN;
END_IF;

IF iState = 0 THEN
    iState := 1;
    fLossFiltered := 0.0;
END_IF;

IF iState >= 1 THEN
    iState := 2;
    sDiagnosticMessage := 'AUTONOMOUS HARVESTING ACTIVE';

    (* ==============================================================================
       1. Ground-Penetrating Radar Terrain Mapping & Cut-Height Optimization
       ============================================================================== *)
    fAvgTerrainOffset := 0.0;
    fTerrainTrend := 0.0;
    
    (* Process forward GPR array to calculate optimal immediate height trajectory *)
    FOR i := 0 TO 15 DO
        fAvgTerrainOffset := fAvgTerrainOffset + aRadarTerrainProfile[i];
    END_FOR;
    fAvgTerrainOffset := fAvgTerrainOffset / 16.0;
    
    (* Simple gradient detection for upcoming large obstacles in far array (16-31) *)
    fTerrainTrend := (aRadarTerrainProfile[31] - aRadarTerrainProfile[15]) / 16.0;
    
    (* Dynamic Height Target: Base height + localized terrain offset + predictive raise for steep inclines *)
    fCmdHeaderHeight := fBaseCutHeight + fAvgTerrainOffset;
    IF fTerrainTrend > 10.0 THEN
        fCmdHeaderHeight := fCmdHeaderHeight + (fTerrainTrend * 1.5); 
    END_IF;
    
    (* Constraint to prevent ground strike *)
    IF fCmdHeaderHeight < 30.0 THEN
        fCmdHeaderHeight := 30.0;
    END_IF;

    (* ==============================================================================
       2. Dynamic Threshing Drum Speed & Concave Clearance Adjustment 
       (Based on Grain Moisture Sensors)
       ============================================================================== *)
    (* High moisture requires higher drum speed and tighter concave to thresh effectively. 
       Low moisture (dry) requires lower speed and wider concave to prevent grain cracking. *)
       
    IF fGrainMoisture > 22.0 THEN
        (* Very Wet Crop *)
        bMoistureWarning := TRUE;
        fCmdDrumSpeed := fBaseDrumSpeed + 150.0; 
        fCmdConcaveClearance := fBaseConcave - 5.0; 
    ELSIF fGrainMoisture > 14.0 THEN
        (* Normal/Transition Moisture *)
        bMoistureWarning := FALSE;
        (* Linear interpolation between dry and wet state *)
        fCmdDrumSpeed := fBaseDrumSpeed + ((fGrainMoisture - 14.0) * 18.75); 
        fCmdConcaveClearance := fBaseConcave - ((fGrainMoisture - 14.0) * 0.625);
    ELSE
        (* Very Dry Crop *)
        bMoistureWarning := FALSE;
        fCmdDrumSpeed := fBaseDrumSpeed - 100.0;
        fCmdConcaveClearance := fBaseConcave + 5.0;
    END_IF;

    (* ==============================================================================
       3. Sieve Loss Acoustic Monitoring
       ============================================================================== *)
    (* First-order low pass filter on acoustic impact sensor to prevent noisy actuation *)
    fLossFiltered := fLossFiltered + fAlphaFilter * (fAcousticSieveLoss - fLossFiltered);
    
    (* Fan Speed Adjustment: If losses are high, fan speed might be too high (blowing grain out) 
       or too low (sieve overloaded). Assume simple mapping for this block: decrease fan speed 
       and open sieve (implied) if aerodynamic loss detected. *)
       
    IF fLossFiltered > fMaxSieveLossLimit THEN
        fbLossDelay(IN:=TRUE, PT:=T#3S);
        IF fbLossDelay.Q THEN
            bSieveLossAlarm := TRUE;
            (* Reduce fan speed to mitigate blow-out losses *)
            fCmdCleaningFanSpeed := 850.0 - ((fLossFiltered - fMaxSieveLossLimit) * 2.0);
        END_IF;
    ELSE
        fbLossDelay(IN:=FALSE);
        bSieveLossAlarm := FALSE;
        fCmdCleaningFanSpeed := 900.0; (* Nominal speed *)
    END_IF;
    
    (* Hard limits on fan speed *)
    IF fCmdCleaningFanSpeed < 600.0 THEN fCmdCleaningFanSpeed := 600.0; END_IF;
    IF fCmdCleaningFanSpeed > 1050.0 THEN fCmdCleaningFanSpeed := 1050.0; END_IF;

END_IF;
"""

new_data = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": assistant_response}
    ]
}

target_file = r"C:\Users\majip\Downloads\LLM REASEARCH\Local_Ollama_Evol_Pipeline\seeds\tier1_enterprise_grade\synthetic_generation_v3_enterprise.jsonl"

with open(target_file, "a", encoding="utf-8") as f:
    f.write(json.dumps(new_data) + "\\n")
