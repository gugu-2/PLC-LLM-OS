import os, json, uuid

os.makedirs("data/swarm_raw", exist_ok=True)
os.makedirs("data", exist_ok=True)

code = """FUNCTION_BLOCK FB_CSP_TroughController
TITLE = 'CSP Parabolic Trough Local Controller'
VERSION : '1.0'
AUTHOR : 'Lumina AI'

VAR_INPUT
    rDNI                : REAL;  // Direct Normal Irradiance (W/m2)
    rWindSpeed          : REAL;  // Local wind speed (m/s)
    rSunElevation       : REAL;  // Sun elevation angle (degrees)
    rSunAzimuth         : REAL;  // Sun azimuth angle (degrees)
    rHTFTempIn          : REAL;  // Heat Transfer Fluid inlet temp (deg C)
    rHTFTempOut         : REAL;  // Heat Transfer Fluid outlet temp (deg C)
    rHTFTempSetpoint    : REAL;  // Target outlet temperature (deg C)
    rExpVesselPressure  : REAL;  // Nitrogen blanket pressure (bar)
    rExpVesselLevel     : REAL;  // HTF level in expansion vessel (%)
    bSystemEnable       : BOOL;  // Main enable signal
    bEmergencyStop      : BOOL;  // Emergency stop
END_VAR

VAR_OUTPUT
    rTroughAngleCmd     : REAL;  // Target parabolic trough angle (degrees)
    rHTFPumpSpeedCmd    : REAL;  // HTF main pump speed command (0-100%)
    bN2FillValveOpen    : BOOL;  // Nitrogen fill valve command
    bN2VentValveOpen    : BOOL;  // Nitrogen vent valve command
    bAlarmWindStow      : BOOL;  // High wind stow active alarm
    bAlarmOverTemp      : BOOL;  // HTF over temperature alarm
    bAlarmPressure      : BOOL;  // Vessel pressure out of bounds
    bSystemFault        : BOOL;  // General system fault
END_VAR

VAR
    // Internal state and parameters
    rMaxWindSpeed       : REAL := 15.0;     // Max wind speed before stowing (m/s)
    rStowAngle          : REAL := 120.0;    // Safe stow angle for high wind
    rNightAngle         : REAL := 90.0;     // Angle for night time / low DNI
    rMinDNI             : REAL := 150.0;    // Minimum DNI to track (W/m2)
    
    // Pump PID variables
    rKp_Pump            : REAL := 0.5;
    rKi_Pump            : REAL := 0.05;
    rErrorTemp          : REAL;
    rIntegralTemp       : REAL;
    rMinPumpSpeed       : REAL := 15.0;
    rMaxPumpSpeed       : REAL := 100.0;
    
    // Pressure control
    rTargetPressure     : REAL := 12.0;     // Target N2 pressure (bar)
    rPressureDeadband   : REAL := 0.5;      // Deadband for pressure control (bar)
    
    // State machine
    nState              : INT := 0; 
    // 0=Init, 1=Standby, 2=Tracking, 3=Stow, 4=Fault
    
    // Math helpers
    rZenith             : REAL;
    rProfileAngle       : REAL;
    rTrackingError      : REAL;
END_VAR

// ==============================================================================
// MAIN CONTROL LOGIC
// ==============================================================================

// 1. Fault Handling and E-Stop
IF bEmergencyStop THEN
    nState := 4; // Fault state
    bSystemFault := TRUE;
ELSIF bSystemEnable AND nState = 4 AND NOT bEmergencyStop THEN
    nState := 0; // Reset fault if E-Stop cleared and system enabled
    bSystemFault := FALSE;
END_IF;

// 2. Wind Protection Override
IF rWindSpeed > rMaxWindSpeed THEN
    bAlarmWindStow := TRUE;
    nState := 3; // Force Stow
ELSE
    bAlarmWindStow := FALSE;
END_IF;

// 3. Over Temperature Protection
IF rHTFTempOut > (rHTFTempSetpoint + 30.0) THEN
    bAlarmOverTemp := TRUE;
    // Defocus slightly to reduce heat absorption
    rTrackingError := 15.0; 
ELSE
    bAlarmOverTemp := FALSE;
    rTrackingError := 0.0;
END_IF;

// 4. State Machine Execution
CASE nState OF
    0: // Init
        rTroughAngleCmd := rStowAngle;
        rHTFPumpSpeedCmd := 0.0;
        bN2FillValveOpen := FALSE;
        bN2VentValveOpen := FALSE;
        IF bSystemEnable THEN
            nState := 1;
        END_IF;
        
    1: // Standby
        rTroughAngleCmd := rNightAngle;
        rHTFPumpSpeedCmd := rMinPumpSpeed; // Minimum circulation
        IF rDNI >= rMinDNI AND NOT bAlarmWindStow THEN
            nState := 2; // Move to tracking
        END_IF;
        IF NOT bSystemEnable THEN
            nState := 0;
        END_IF;
        
    2: // Tracking (Normal Operation)
        // Calculate zenith angle
        rZenith := 90.0 - rSunElevation;
        
        // Simplified profile angle calculation for North-South aligned trough
        IF rSunElevation > 5.0 THEN
            rProfileAngle := rSunAzimuth - 180.0; // Normalized to South
            rTroughAngleCmd := (rZenith * 0.95) + rTrackingError;
        ELSE
            rTroughAngleCmd := rNightAngle; // Sun too low
        END_IF;
        
        // HTF Flow Control (PI Controller for Temperature)
        rErrorTemp := rHTFTempOut - rHTFTempSetpoint;
        rIntegralTemp := rIntegralTemp + (rErrorTemp * 0.1); 
        
        // Anti-windup
        IF rIntegralTemp > 50.0 THEN rIntegralTemp := 50.0; END_IF;
        IF rIntegralTemp < -50.0 THEN rIntegralTemp := -50.0; END_IF;
        
        rHTFPumpSpeedCmd := rMinPumpSpeed + (rKp_Pump * rErrorTemp) + (rKi_Pump * rIntegralTemp);
        
        // Clamp pump speed
        IF rHTFPumpSpeedCmd > rMaxPumpSpeed THEN
            rHTFPumpSpeedCmd := rMaxPumpSpeed;
        ELSIF rHTFPumpSpeedCmd < rMinPumpSpeed THEN
            rHTFPumpSpeedCmd := rMinPumpSpeed;
        END_IF;
        
        // Return to standby if DNI drops
        IF rDNI < (rMinDNI - 20.0) THEN
            nState := 1;
        END_IF;
        
    3: // Stow (Wind Protection)
        rTroughAngleCmd := rStowAngle;
        rHTFPumpSpeedCmd := rMinPumpSpeed; 
        IF NOT bAlarmWindStow AND rDNI >= rMinDNI THEN
            nState := 2; 
        ELSIF NOT bAlarmWindStow THEN
            nState := 1;
        END_IF;
        
    4: // Fault / E-Stop
        rTroughAngleCmd := rStowAngle;
        rHTFPumpSpeedCmd := 0.0; 
        
END_CASE;

// 5. Expansion Vessel Nitrogen Pressure Control
IF rExpVesselPressure < (rTargetPressure - rPressureDeadband) THEN
    bN2FillValveOpen := TRUE;
    bN2VentValveOpen := FALSE;
ELSIF rExpVesselPressure > (rTargetPressure + rPressureDeadband) THEN
    bN2FillValveOpen := FALSE;
    bN2VentValveOpen := TRUE;
ELSE
    bN2FillValveOpen := FALSE;
    bN2VentValveOpen := FALSE;
END_IF;

// Pressure Alarm Logic
IF rExpVesselPressure > (rTargetPressure + 2.0 * rPressureDeadband) OR 
   rExpVesselPressure < (rTargetPressure - 2.0 * rPressureDeadband) THEN
    bAlarmPressure := TRUE;
ELSE
    bAlarmPressure := FALSE;
END_IF;

END_FUNCTION_BLOCK"""

record = {
    "messages": [
        {
            "role": "user",
            "content": "You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.\\nYour specific domain is: CSP Parabolic Trough Solar Field.\\nTask: Invent a highly complex control scenario for this domain (e.g., synthetic heat transfer fluid (HTF) flow balancing, local solar tracking angle calculation, and expansion vessel nitrogen pressure).\\nWrite a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."
        },
        {
            "role": "assistant",
            "content": f"```iec-st\\n{code}\\n```"
        }
    ]
}

# 1. Save to unique UUID file in swarm_raw
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, indent=2)

# 2. Append to jsonl file
jsonl_file = "data/synthetic_generation_v3_enterprise.jsonl"
with open(jsonl_file, "a", encoding="utf-8") as f:
    f.write(json.dumps(record) + "\n")

print(f"Data written to {filename} and {jsonl_file}")
