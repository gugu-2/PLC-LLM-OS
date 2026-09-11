import json
import uuid
import os

os.makedirs("data/swarm_raw", exist_ok=True)
os.makedirs("data", exist_ok=True)

prompt = "You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.\nYour specific domain is: Fiberglass Pultrusion Line.\nTask: Invent a highly complex control scenario for this domain (e.g., resin bath impregnation viscosity tracking, Radio Frequency (RF) pre-heating thermal zones, and caterpillar puller synchronization).\nWrite a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."

st_code = """```iec-st
FUNCTION_BLOCK FB_PultrusionLineSync
TITLE = 'Fiberglass Pultrusion Line Synchronization and Thermal Control'
VERSION : '1.0'
AUTHOR : 'Lumina AI Cloud Swarm'

VAR_INPUT
    // Resin Bath Impregnation
    rResinTemp_C : REAL; // Current resin temperature in degrees C
    rResinLevel_mm : REAL; // Resin level in the bath
    rAmbientTemp_C : REAL; // Ambient environment temperature
    rTargetViscosity_cP : REAL; // Target resin viscosity in centipoise
    
    // RF Pre-heating Thermal Zones
    arRFZoneTemps_C : ARRAY[1..4] OF REAL; // Actual temperatures of RF zones
    arRFZoneTargets_C : ARRAY[1..4] OF REAL; // Target temperatures of RF zones
    bEnableRFHeating : BOOL; // Enable RF heating system
    
    // Caterpillar Puller Synchronization
    rPuller1Speed_mmin : REAL; // Caterpillar 1 actual speed (m/min)
    rPuller2Speed_mmin : REAL; // Caterpillar 2 actual speed (m/min)
    rLineTension_N : REAL; // Measured line tension (Newtons)
    rTargetTension_N : REAL; // Desired line tension (Newtons)
    rMasterSpeedRef_mmin : REAL; // Master line speed reference
    bStartLine : BOOL; // Command to start the pultrusion line
    bStopLine : BOOL; // Command to stop the pultrusion line
END_VAR

VAR_OUTPUT
    // Resin Bath Control
    rResinHeaterOutput_pct : REAL; // 0-100% output to resin bath heater
    rResinMixerSpeed_RPM : REAL; // Speed reference for resin mixer
    bResinLevelLowAlarm : BOOL;
    
    // RF Pre-heating Output
    arRFZoneOutputs_pct : ARRAY[1..4] OF REAL; // 0-100% output to RF generators
    
    // Puller Drive Commands
    rPuller1DriveRef_mmin : REAL;
    rPuller2DriveRef_mmin : REAL;
    bPullerSyncError : BOOL;
    
    // Global
    bSystemReady : BOOL;
    bEmergencyStop : BOOL;
END_VAR

VAR
    // Internal State
    iState : INT := 0; 
    
    // PID Controllers internal states
    rTensionError : REAL;
    rTensionIntegral : REAL;
    rTensionDerivative : REAL;
    rLastTensionError : REAL;
    
    rResinViscosityEstimate : REAL;
    rResinTempTarget : REAL;
    
    // Timers
    tRFHeatingDelay : TON;
    tStartupDelay : TON;
    
    i : INT; // Loop counter
    
    // Constants
    Kp_Tension : REAL := 0.05;
    Ki_Tension : REAL := 0.01;
    Kd_Tension : REAL := 0.005;
    
    Kp_RF : REAL := 2.5;
END_VAR

// ==============================================================================
// LOGIC EXECUTION
// ==============================================================================

// 1. Resin Bath Impregnation Viscosity Tracking
// Viscosity is inversely proportional to temperature. Estimate current viscosity.
// Base viscosity calculation (empirical model)
rResinViscosityEstimate := 10000.0 / (rResinTemp_C + 1.0) * (rAmbientTemp_C / 25.0);

// Calculate required temperature to hit target viscosity
rResinTempTarget := (10000.0 / rTargetViscosity_cP) - 1.0;

// Simple Proportional control for Resin Heater
IF rResinTemp_C < rResinTempTarget THEN
    rResinHeaterOutput_pct := (rResinTempTarget - rResinTemp_C) * 5.0;
    IF rResinHeaterOutput_pct > 100.0 THEN
        rResinHeaterOutput_pct := 100.0;
    END_IF;
ELSE
    rResinHeaterOutput_pct := 0.0;
END_IF;

// Resin Level monitoring
bResinLevelLowAlarm := (rResinLevel_mm < 50.0);
IF bResinLevelLowAlarm THEN
    rResinMixerSpeed_RPM := 10.0; // Slow mix if level is low
ELSE
    rResinMixerSpeed_RPM := 60.0; // Nominal mix speed
END_IF;

// 2. Radio Frequency (RF) Pre-heating Thermal Zones
// Loop through 4 zones and calculate proportional heating demand
FOR i := 1 TO 4 DO
    IF bEnableRFHeating THEN
        IF arRFZoneTemps_C[i] < arRFZoneTargets_C[i] THEN
            arRFZoneOutputs_pct[i] := (arRFZoneTargets_C[i] - arRFZoneTemps_C[i]) * Kp_RF;
            // Clamp to 100%
            IF arRFZoneOutputs_pct[i] > 100.0 THEN
                arRFZoneOutputs_pct[i] := 100.0;
            END_IF;
        ELSE
            arRFZoneOutputs_pct[i] := 0.0;
        END_IF;
    ELSE
        arRFZoneOutputs_pct[i] := 0.0;
    END_IF;
END_FOR;

// 3. Caterpillar Puller Synchronization & Tension Control
// Tension PID Control
rTensionError := rTargetTension_N - rLineTension_N;
rTensionIntegral := rTensionIntegral + rTensionError;
// Anti-windup
IF rTensionIntegral > 1000.0 THEN rTensionIntegral := 1000.0; END_IF;
IF rTensionIntegral < -1000.0 THEN rTensionIntegral := -1000.0; END_IF;

rTensionDerivative := rTensionError - rLastTensionError;
rLastTensionError := rTensionError;

// State Machine for Line Start/Stop
CASE iState OF
    0: // STOPPED
        rPuller1DriveRef_mmin := 0.0;
        rPuller2DriveRef_mmin := 0.0;
        IF bStartLine AND NOT bResinLevelLowAlarm THEN
            iState := 1;
        END_IF;
        
    1: // RAMPING UP
        rPuller1DriveRef_mmin := rPuller1DriveRef_mmin + 0.1;
        IF rPuller1DriveRef_mmin >= rMasterSpeedRef_mmin THEN
            iState := 2;
        END_IF;
        // Puller 2 follows Puller 1 exactly during ramp
        rPuller2DriveRef_mmin := rPuller1DriveRef_mmin;
        IF bStopLine THEN iState := 0; END_IF;
        
    2: // RUNNING & SYNCHRONIZED
        rPuller1DriveRef_mmin := rMasterSpeedRef_mmin;
        
        // Puller 2 trims speed based on tension PID to maintain line tension between caterpillars
        rPuller2DriveRef_mmin := rMasterSpeedRef_mmin + 
                                 (rTensionError * Kp_Tension) + 
                                 (rTensionIntegral * Ki_Tension) + 
                                 (rTensionDerivative * Kd_Tension);
                                 
        IF bStopLine THEN iState := 0; END_IF;
END_CASE;

// Check for sync error
IF ABS(rPuller1Speed_mmin - rPuller2Speed_mmin) > 2.0 AND iState = 2 THEN
    bPullerSyncError := TRUE;
ELSE
    bPullerSyncError := FALSE;
END_IF;

// Ready signal
bSystemReady := (rResinTemp_C >= (rResinTempTarget * 0.95)) AND NOT bResinLevelLowAlarm;

// Safety
IF bEmergencyStop THEN
    rPuller1DriveRef_mmin := 0.0;
    rPuller2DriveRef_mmin := 0.0;
    rResinHeaterOutput_pct := 0.0;
    iState := 0;
END_IF;

END_FUNCTION_BLOCK
```"""

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": st_code}
    ]
}

file_name = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(file_name, "w", encoding="utf-8") as f:
    json.dump(record, f, indent=2)

with open("data/synthetic_generation_v3_enterprise.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(record) + "\n")
