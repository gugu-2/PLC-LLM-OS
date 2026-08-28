import json, uuid, os

prompt = "Invent a highly complex control scenario for an Offshore Floating Production Storage and Offloading (FPSO) Vessel (e.g., turret mooring dynamic positioning, thruster allocation matrices, and slop tank three-phase separation). Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."

st_code = """FUNCTION_BLOCK FB_FPSO_IntegratedControl
TITLE = 'FPSO Turret Mooring DP and Slop Tank Separation Control'
// Highly complex FPSO integrated control system handling Turret Mooring DP, 
// Thruster Allocation Matrices, and Slop Tank 3-Phase Separation.

VAR_INPUT
    // DP & Mooring Inputs
    rVesselHeading          : REAL;         // Current vessel heading (degrees)
    rTargetHeading          : REAL;         // Target vessel heading (degrees)
    rWindSpeed              : REAL;         // Current wind speed (m/s)
    rWindDirection          : REAL;         // Current wind direction (degrees)
    rWaveHeight             : REAL;         // Significant wave height (m)
    rWaveDirection          : REAL;         // Wave direction (degrees)
    rCurrentSpeed           : REAL;         // Ocean current speed (m/s)
    rCurrentDirection       : REAL;         // Ocean current direction (degrees)
    bEnableDP               : BOOL;         // Enable Dynamic Positioning
    
    // Slop Tank Inputs
    rTankLevelOil           : REAL;         // Oil interface level (m)
    rTankLevelWater         : REAL;         // Water interface level (m)
    rEmulsionThickness      : REAL;         // Emulsion layer thickness (m)
    rInletFlowRate          : REAL;         // Inflow rate (m3/h)
    rInletTemperature       : REAL;         // Inlet temperature (C)
    bStartSeparation        : BOOL;         // Start separation sequence
END_VAR

VAR_OUTPUT
    // Thruster Allocation Outputs (6 Thrusters)
    arThrusterSpeedCmd      : ARRAY[1..6] OF REAL; // Speed command for thrusters (RPM)
    arThrusterPitchCmd      : ARRAY[1..6] OF REAL; // Pitch command for thrusters (%)
    arThrusterAzimuthCmd    : ARRAY[1..6] OF REAL; // Azimuth angle (degrees)
    
    // Slop Tank Outputs
    rOilValvePos            : REAL;         // Oil discharge valve position (%)
    rWaterValvePos          : REAL;         // Water discharge valve position (%)
    rHeaterPower            : REAL;         // Heater output power (kW)
    rChemicalInjectRate     : REAL;         // Demulsifier injection rate (L/h)
    bSystemAlarm            : BOOL;         // Integrated system alarm
END_VAR

VAR
    // Internal States for DP
    rHeadingError           : REAL;
    rIntegralError          : REAL;
    rDerivativeError        : REAL;
    rPreviousError          : REAL;
    rKp                     : REAL := 1.5;
    rKi                     : REAL := 0.05;
    rKd                     : REAL := 0.8;
    
    rTotalSurgeForce        : REAL;
    rTotalSwayForce         : REAL;
    rTotalYawMoment         : REAL;
    
    // Internal States for Thruster Allocation Matrix
    iIdx                    : INT;
    rMaxThrusterCapacity    : REAL := 5000.0; // kW
    
    // Internal States for Separation
    rTargetOilLevel         : REAL := 5.0;
    rTargetWaterLevel       : REAL := 2.5;
    rHeaterPID_Kp           : REAL := 2.0;
    bSeparationActive       : BOOL;
    
    // Timers
    tHeaterDelay            : TON;
    tDPCycleTimer           : TON;
END_VAR

// --- 1. TURRET MOORING DYNAMIC POSITIONING (DP) ---
IF bEnableDP THEN
    // Calculate Heading Error (Shortest path)
    rHeadingError := rTargetHeading - rVesselHeading;
    IF rHeadingError > 180.0 THEN
        rHeadingError := rHeadingError - 360.0;
    ELSIF rHeadingError < -180.0 THEN
        rHeadingError := rHeadingError + 360.0;
    END_IF;
    
    // PID for Yaw Moment
    rIntegralError := rIntegralError + rHeadingError;
    // Anti-windup
    IF rIntegralError > 1000.0 THEN rIntegralError := 1000.0; END_IF;
    IF rIntegralError < -1000.0 THEN rIntegralError := -1000.0; END_IF;
    
    rDerivativeError := rHeadingError - rPreviousError;
    rTotalYawMoment := (rKp * rHeadingError) + (rKi * rIntegralError) + (rKd * rDerivativeError);
    rPreviousError := rHeadingError;
    
    // Feedforward Environmental Forces (Simplified)
    rTotalSurgeForce := rWindSpeed * 10.0 * COS(rWindDirection) + rCurrentSpeed * 50.0 * COS(rCurrentDirection);
    rTotalSwayForce  := rWindSpeed * 10.0 * SIN(rWindDirection) + rCurrentSpeed * 50.0 * SIN(rCurrentDirection);
    
    // --- 2. THRUSTER ALLOCATION MATRIX ---
    // Distribute required surge, sway, and yaw to 6 azimuth thrusters
    // Assuming symmetrical layout for simplification
    FOR iIdx := 1 TO 6 DO
        // Simplified allocation logic
        arThrusterAzimuthCmd[iIdx] := ATAN2(rTotalSwayForce, rTotalSurgeForce) * 180.0 / 3.14159;
        
        IF iIdx <= 3 THEN
            // Forward thrusters handle positive yaw moment
            arThrusterSpeedCmd[iIdx] := LIMIT(0.0, SQRT(ABS(rTotalSurgeForce/6.0) + ABS(rTotalYawMoment/3.0)) * 10.0, 1000.0);
        ELSE
            // Aft thrusters handle negative yaw moment
            arThrusterSpeedCmd[iIdx] := LIMIT(0.0, SQRT(ABS(rTotalSurgeForce/6.0) - ABS(rTotalYawMoment/3.0)) * 10.0, 1000.0);
        END_IF;
        arThrusterPitchCmd[iIdx] := 80.0; // Fixed nominal pitch
    END_FOR;
ELSE
    rIntegralError := 0.0;
    FOR iIdx := 1 TO 6 DO
        arThrusterSpeedCmd[iIdx] := 0.0;
        arThrusterPitchCmd[iIdx] := 0.0;
    END_FOR;
END_IF;

// --- 3. SLOP TANK THREE-PHASE SEPARATION ---
IF bStartSeparation THEN
    bSeparationActive := TRUE;
ELSE
    bSeparationActive := FALSE;
END_IF;

IF bSeparationActive THEN
    // Demulsifier injection based on emulsion thickness and inlet flow
    IF rEmulsionThickness > 0.5 THEN
        rChemicalInjectRate := rInletFlowRate * 0.05 * rEmulsionThickness; // L/h
    ELSE
        rChemicalInjectRate := rInletFlowRate * 0.01;
    END_IF;
    
    // Heater Control to maintain separation temp (target 65C)
    IF rInletTemperature < 65.0 THEN
        rHeaterPower := LIMIT(0.0, (65.0 - rInletTemperature) * rHeaterPID_Kp * 100.0, 5000.0); // max 5MW
    ELSE
        rHeaterPower := 0.0;
    END_IF;
    
    // Interface Level Control
    // Oil Discharge
    IF rTankLevelOil > rTargetOilLevel + 0.2 THEN
        rOilValvePos := LIMIT(0.0, rOilValvePos + 5.0, 100.0); // Open valve gradually
    ELSIF rTankLevelOil < rTargetOilLevel - 0.2 THEN
        rOilValvePos := LIMIT(0.0, rOilValvePos - 5.0, 100.0); // Close valve gradually
    END_IF;
    
    // Water Discharge
    IF rTankLevelWater > rTargetWaterLevel + 0.1 THEN
        rWaterValvePos := LIMIT(0.0, rWaterValvePos + 5.0, 100.0);
    ELSIF rTankLevelWater < rTargetWaterLevel - 0.1 THEN
        rWaterValvePos := LIMIT(0.0, rWaterValvePos - 5.0, 100.0);
    END_IF;
    
    // System Alarms
    IF rTankLevelOil > 8.0 OR rTankLevelWater > 4.0 OR rEmulsionThickness > 2.0 THEN
        bSystemAlarm := TRUE;
    ELSE
        bSystemAlarm := FALSE;
    END_IF;
ELSE
    rHeaterPower := 0.0;
    rChemicalInjectRate := 0.0;
    rOilValvePos := 0.0;
    rWaterValvePos := 0.0;
    bSystemAlarm := FALSE;
END_IF;
END_FUNCTION_BLOCK
"""

msg = f"```iec-st\n{st_code}\n```"

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": msg}
    ]
}

os.makedirs("data/swarm_raw", exist_ok=True)
filename_raw = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename_raw, "w", encoding="utf-8") as f:
    json.dump(record, f)

with open("data/synthetic_generation_v3_enterprise.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(record) + "\\n")
