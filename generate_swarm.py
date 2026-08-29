import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: High-Speed Cardboard Die Cutter.
Task: Invent a highly complex control scenario for this domain (e.g., stripping station waste ejection pin timing, cam-driven platen pressure profiling, and blanking tool synchronization).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."""

code = """```iec-st
FUNCTION_BLOCK FB_DieCutterMasterSync
TITLE = 'High-Speed Cardboard Die Cutter Master Control'
// -----------------------------------------------------------------------------
// Description:
// Master synchronization and control block for a high-speed cardboard die cutter.
// Handles platen pressure profiling, stripping station waste ejection pin timing,
// and blanking tool synchronization based on master virtual axis (encoder).
// -----------------------------------------------------------------------------

VAR_INPUT
    xEnable                  : BOOL; // Enable die cutter operations
    xResetFaults             : BOOL; // Reset active faults
    rMasterVelocity          : REAL; // Master line speed (sheets per minute)
    diMasterEncoderPos       : DINT; // Master machine angle (0 - 35999, hundredths of degree)
    
    // Physical I/O
    xSensorSheetEntry        : BOOL; // Sheet detected at entry
    xSensorPlatenClear       : BOOL; // Platen area clear
    xSensorStrippingJam      : BOOL; // Jam detected in stripping station
    rActualPlatenPressure    : REAL; // Hydraulic platen pressure feedback (bar)
    diEjectorPinPosition     : DINT; // Feedback from ejector pin servo
END_VAR

VAR_OUTPUT
    xReady                   : BOOL; // Machine is ready for production
    xRunning                 : BOOL; // Machine is actively processing
    xFault                   : BOOL; // General fault active
    diFaultCode              : DINT; // Specific fault code
    
    // Actuators / Outputs
    rCmdPlatenPressure       : REAL; // Command to platen hydraulic proportional valve
    xCmdEngageClutch         : BOOL; // Main drive clutch engagement
    xCmdFireEjectorPins      : BOOL; // High-speed solenoid command for waste stripping
    rCmdBlankingAxisVelocity : REAL; // Velocity command for blanking servo
    rCmdBlankingAxisPos      : REAL; // Position command for blanking servo
END_VAR

VAR
    eState                   : INT := 0; // State machine state
    
    // Cam Profile Data
    arPlatenCamProfile       : ARRAY[0..360] OF REAL; // Pressure profile vs angle
    rTargetPressure          : REAL;
    rPressureError           : REAL;
    rPressureIntegral        : REAL;
    
    // Timing calculations
    diStrippingFireAngleOn   : DINT := 12500; // 125.00 degrees
    diStrippingFireAngleOff  : DINT := 14000; // 140.00 degrees
    xSheetInPlaten           : BOOL;
    xSheetInStripping        : BOOL;
    xSheetInBlanking         : BOOL;
    
    // Tracking
    diSheetCounter           : DINT := 0;
    diLastEncoderPos         : DINT := 0;
    rBlankingSyncOffset      : REAL := 15.5; // Offset mm
    
    // Constants
    MAX_PRESSURE             : REAL := 350.0; // Bar
    MIN_PRESSURE             : REAL := 10.0;
    PRESSURE_KP              : REAL := 2.5;
    PRESSURE_KI              : REAL := 0.1;
    
    // Diagnostics
    tPlatenResponseTimer     : TON;
END_VAR

// =============================================================================
// Implementation
// =============================================================================

// 1. Fault Handling
IF xResetFaults THEN
    xFault := FALSE;
    diFaultCode := 0;
    eState := 0;
END_IF;

IF xSensorStrippingJam THEN
    xFault := TRUE;
    diFaultCode := 1001; // Stripping jam
END_IF;

IF rActualPlatenPressure > (MAX_PRESSURE + 20.0) THEN
    xFault := TRUE;
    diFaultCode := 1002; // Overpressure
END_IF;

IF xFault THEN
    xRunning := FALSE;
    xCmdEngageClutch := FALSE;
    xCmdFireEjectorPins := FALSE;
    rCmdPlatenPressure := 0.0;
    rCmdBlankingAxisVelocity := 0.0;
    RETURN;
END_IF;

// 2. Master State Machine
CASE eState OF
    0: // INIT
        xReady := TRUE;
        IF xEnable THEN
            eState := 10;
            xReady := FALSE;
        END_IF;
        
    10: // STARTUP
        xCmdEngageClutch := TRUE;
        IF rMasterVelocity > 10.0 THEN
            eState := 20; // RUNNING
            xRunning := TRUE;
        END_IF;
        
    20: // RUNNING
        IF NOT xEnable THEN
            eState := 30;
        END_IF;
        
        // --- Platen Pressure Cam Profiling ---
        // Calculate target pressure based on machine angle (modulo 360 degrees)
        rTargetPressure := arPlatenCamProfile[diMasterEncoderPos / 100];
        
        // Simple PI control for hydraulic pressure
        rPressureError := rTargetPressure - rActualPlatenPressure;
        rPressureIntegral := rPressureIntegral + (rPressureError * 0.001); // Assuming 1ms cycle
        
        // Anti-windup
        IF rPressureIntegral > MAX_PRESSURE THEN rPressureIntegral := MAX_PRESSURE; END_IF;
        IF rPressureIntegral < 0.0 THEN rPressureIntegral := 0.0; END_IF;
        
        rCmdPlatenPressure := (rPressureError * PRESSURE_KP) + (rPressureIntegral * PRESSURE_KI);
        IF rCmdPlatenPressure > MAX_PRESSURE THEN rCmdPlatenPressure := MAX_PRESSURE; END_IF;
        IF rCmdPlatenPressure < MIN_PRESSURE THEN rCmdPlatenPressure := MIN_PRESSURE; END_IF;
        
        // --- Stripping Station Waste Ejection Pin Timing ---
        // Fire pins accurately based on angle window
        IF (diMasterEncoderPos >= diStrippingFireAngleOn) AND (diMasterEncoderPos <= diStrippingFireAngleOff) THEN
            xCmdFireEjectorPins := TRUE;
        ELSE
            xCmdFireEjectorPins := FALSE;
        END_IF;
        
        // --- Blanking Tool Synchronization ---
        // Electronic gearing to master velocity with positional phase offset
        rCmdBlankingAxisVelocity := rMasterVelocity * 1.05; // 5% overspeed to catch sheet
        rCmdBlankingAxisPos := DINT_TO_REAL(diMasterEncoderPos) * 0.01 + rBlankingSyncOffset;
        
    30: // STOPPING
        xCmdEngageClutch := FALSE;
        xRunning := FALSE;
        IF rMasterVelocity < 1.0 THEN
            eState := 0;
        END_IF;
        
    ELSE
        eState := 0;
END_CASE;

// 3. Update memory variables
diLastEncoderPos := diMasterEncoderPos;

END_FUNCTION_BLOCK
```"""

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": code}
    ]
}

os.makedirs("data/swarm_raw", exist_ok=True)
file_id = uuid.uuid4().hex[:8]
swarm_file = f"data/swarm_raw/agent_{file_id}.json"
with open(swarm_file, "w", encoding="utf-8") as f:
    json.dump(record, f, indent=2)

os.makedirs("data", exist_ok=True)
jsonl_file = "data/synthetic_generation_v3_enterprise.jsonl"
with open(jsonl_file, "a", encoding="utf-8") as f:
    f.write(json.dumps(record) + "\n")

print(f"Successfully wrote data to {swarm_file} and {jsonl_file}")
