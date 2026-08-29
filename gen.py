import json
import uuid
import os

user_prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: High-Speed Aluminum Can End Making Press.
Task: Invent a highly complex control scenario for this domain (e.g., compound liner extrusion nozzle indexing, progressive die punch tonnage signature monitoring, and vacuum scrap removal).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."""

assistant_response = """```iec-st
FUNCTION_BLOCK FB_HighSpeedCanEndPressControl
TITLE = 'High-Speed Aluminum Can End Press Controller'
VERSION : '1.5'
AUTHOR : 'Lumina AI Swarm'

// -----------------------------------------------------------------------------
// DESCRIPTION:
// This function block orchestrates the high-speed stamping, compound liner 
// extrusion, and scrap removal for a multi-lane aluminum can end making press.
// It features high-resolution tonnage signature monitoring, precision nozzle 
// indexing, and vacuum-assisted scrap ejection tracking.
// -----------------------------------------------------------------------------

VAR_INPUT
    bSystemEnable           : BOOL;     // Master enable for the press system
    bEmergencyStop          : BOOL;     // Active LOW Emergency Stop circuit
    bSafetyGuardsClosed     : BOOL;     // Door switches and light curtains
    rTargetSpeedCPM         : REAL;     // Desired operational speed (Cans Per Minute)
    rResolverAngle          : REAL;     // Absolute press angle (0.0 to 359.9 degrees)
    arrTonnageSensors       : ARRAY[1..8] OF REAL; // Analog tonnage from strain gauges (kN)
    bVacuumScrapSensor      : BOOL;     // Optical/Vacuum sensor for scrap clearance
    bCompoundLinerReady     : BOOL;     // Extrusion subsystem ready signal
    bResetFaults            : BOOL;     // Operator fault reset pushbutton
END_VAR

VAR_OUTPUT
    bPressClutchEngage      : BOOL;     // Output to main press clutch solenoid
    bPressBrakeEngage       : BOOL;     // Output to main press brake solenoid
    bVacuumValveControl     : BOOL;     // Output to scrap removal vacuum blast
    arrLinerNozzleTriggers  : ARRAY[1..8] OF BOOL; // High-speed outputs to extrusion nozzles
    arrTonnageAlarms        : ARRAY[1..8] OF BOOL; // Over-tonnage indicators per lane
    rTotalCalculatedTonnage : REAL;     // Summed instantaneous tonnage
    bSystemFaulted          : BOOL;     // General fault flag
    iActiveFaultCode        : INT;      // Diagnostic fault code
    rCurrentCPM             : REAL;     // Calculated actual machine speed
END_VAR

VAR
    iLaneIndex              : INT;
    rMaxTonnageLimit        : ARRAY[1..8] OF REAL := [45.5, 45.5, 45.5, 45.5, 45.5, 45.5, 45.5, 45.5]; 
    rMinTonnageLimit        : ARRAY[1..8] OF REAL := [30.0, 30.0, 30.0, 30.0, 30.0, 30.0, 30.0, 30.0];
    
    // Timing and Angle Windows
    rLinerStartAngle        : REAL := 110.5;
    rLinerEndAngle          : REAL := 145.0;
    rVacuumStartAngle       : REAL := 220.0;
    rVacuumEndAngle         : REAL := 310.0;
    rTonnageWindowStart     : REAL := 175.0;
    rTonnageWindowEnd       : REAL := 185.0;
    
    bInternalFaultActive    : BOOL;
    bTonnageSampleTaken     : BOOL;
    rPreviousAngle          : REAL;
    
    // Speed calculation variables
    tScanCycleTime          : TIME := T#5MS; // Assumed PLC scan time
    rDeltaAngle             : REAL;
END_VAR

// =============================================================================
// SAFETY AND ENABLE LOGIC
// =============================================================================
IF NOT bEmergencyStop OR NOT bSafetyGuardsClosed THEN
    bPressClutchEngage := FALSE;
    bPressBrakeEngage := TRUE;
    bVacuumValveControl := FALSE;
    bSystemFaulted := TRUE;
    bInternalFaultActive := TRUE;
    
    IF NOT bEmergencyStop THEN
        iActiveFaultCode := 9001; // E-Stop Activated
    ELSE
        iActiveFaultCode := 9002; // Safety Guard Open
    END_IF;
    
    FOR iLaneIndex := 1 TO 8 DO
        arrLinerNozzleTriggers[iLaneIndex] := FALSE;
    END_FOR;
    RETURN;
END_IF;

// Fault Reset Handling
IF bResetFaults AND bInternalFaultActive THEN
    bInternalFaultActive := FALSE;
    iActiveFaultCode := 0;
    FOR iLaneIndex := 1 TO 8 DO
        arrTonnageAlarms[iLaneIndex] := FALSE;
    END_FOR;
END_IF;

// System Not Enabled
IF NOT bSystemEnable OR bInternalFaultActive THEN
    bPressClutchEngage := FALSE;
    bPressBrakeEngage := TRUE;
    bSystemFaulted := bInternalFaultActive;
    RETURN;
END_IF;

// Normal Run Condition
bPressClutchEngage := TRUE;
bPressBrakeEngage := FALSE;
bSystemFaulted := FALSE;

// =============================================================================
// SPEED CALCULATION (Cans Per Minute)
// =============================================================================
rDeltaAngle := rResolverAngle - rPreviousAngle;
IF rDeltaAngle < 0.0 THEN
    rDeltaAngle := rDeltaAngle + 360.0; // Handle rollover
END_IF;
rPreviousAngle := rResolverAngle;

// (Degrees / ms) * (1000 ms / 1 s) * (60 s / 1 min) / (360 Degrees / 1 rev)
rCurrentCPM := (rDeltaAngle / 5.0) * 1000.0 * 60.0 / 360.0;

// =============================================================================
// PROGRESSIVE DIE PUNCH TONNAGE SIGNATURE MONITORING
// =============================================================================
rTotalCalculatedTonnage := 0.0;

IF (rResolverAngle >= rTonnageWindowStart) AND (rResolverAngle <= rTonnageWindowEnd) THEN
    bTonnageSampleTaken := TRUE;
    FOR iLaneIndex := 1 TO 8 DO
        rTotalCalculatedTonnage := rTotalCalculatedTonnage + arrTonnageSensors[iLaneIndex];
        
        // Check for Hard Over-Tonnage (Die Crash) or Under-Tonnage (Missing Material)
        IF arrTonnageSensors[iLaneIndex] > rMaxTonnageLimit[iLaneIndex] THEN
            arrTonnageAlarms[iLaneIndex] := TRUE;
            bInternalFaultActive := TRUE;
            iActiveFaultCode := 2000 + iLaneIndex; // Over-Tonnage Fault per lane
        ELSIF arrTonnageSensors[iLaneIndex] < rMinTonnageLimit[iLaneIndex] THEN
            arrTonnageAlarms[iLaneIndex] := TRUE;
            bInternalFaultActive := TRUE;
            iActiveFaultCode := 3000 + iLaneIndex; // Under-Tonnage Fault per lane
        END_IF;
    END_FOR;
ELSE
    // Reset sampling flag once outside the window
    IF rResolverAngle < rTonnageWindowStart THEN
        bTonnageSampleTaken := FALSE;
    END_IF;
END_IF;

// =============================================================================
// COMPOUND LINER EXTRUSION NOZZLE INDEXING
// =============================================================================
IF bCompoundLinerReady AND (rResolverAngle >= rLinerStartAngle) AND (rResolverAngle <= rLinerEndAngle) THEN
    FOR iLaneIndex := 1 TO 8 DO
        arrLinerNozzleTriggers[iLaneIndex] := TRUE;
    END_FOR;
ELSE
    FOR iLaneIndex := 1 TO 8 DO
        arrLinerNozzleTriggers[iLaneIndex] := FALSE;
    END_FOR;
END_IF;

IF (rResolverAngle >= rLinerStartAngle) AND NOT bCompoundLinerReady THEN
    bInternalFaultActive := TRUE;
    iActiveFaultCode := 4001; // Liner System Not Ready during cycle
END_IF;

// =============================================================================
// VACUUM SCRAP REMOVAL & CLEARANCE VERIFICATION
// =============================================================================
IF (rResolverAngle >= rVacuumStartAngle) AND (rResolverAngle <= rVacuumEndAngle) THEN
    bVacuumValveControl := TRUE;
    
    // Verify scrap clears at the end of the vacuum window
    IF (rResolverAngle >= (rVacuumEndAngle - 10.0)) AND NOT bVacuumScrapSensor THEN
        bInternalFaultActive := TRUE;
        iActiveFaultCode := 5001; // Scrap Clearance Failure (Die Protection)
    END_IF;
ELSE
    bVacuumValveControl := FALSE;
END_IF;

END_FUNCTION_BLOCK
```"""

record = {
    "messages": [
        {"role": "user", "content": user_prompt},
        {"role": "assistant", "content": assistant_response}
    ]
}

os.makedirs('data/swarm_raw', exist_ok=True)
os.makedirs('data', exist_ok=True)

with open('data/synthetic_generation_v3_enterprise.jsonl', 'a', encoding='utf-8') as f:
    f.write(json.dumps(record) + '\\n')
    
file_name = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(file_name, 'w', encoding='utf-8') as f:
    json.dump(record, f)

print(f"Success: {file_name}")
