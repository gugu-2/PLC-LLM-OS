import json
import uuid
import os

prompt = "Design an advanced Structured Text (ST) control block for a Power-to-Liquid (PtL) Synthetic Fuel Plant. The block must handle Fischer-Tropsch reactor catalyst cooling zones, syngas compressor mass flow mapping, and wax product separation. Ensure the code includes a FUNCTION_BLOCK definition with extensive VAR declarations for physical I/O and process variables."
st_code = """```iec-st
FUNCTION_BLOCK FB_PtLSynthFuel_Control
VAR_INPUT
    bEnable : BOOL; // Enable control
    bEmergencyStop : BOOL; // Emergency stop active low
    
    // Fischer-Tropsch Reactor Inputs
    rReactorTemp_Z1 : REAL; // Zone 1 Temperature (C)
    rReactorTemp_Z2 : REAL; // Zone 2 Temperature (C)
    rReactorTemp_Z3 : REAL; // Zone 3 Temperature (C)
    rReactorPressure : REAL; // Reactor Pressure (bar)
    rCoolantFlow_In : REAL; // Coolant mass flow (kg/s)
    
    // Syngas Compressor Inputs
    rSyngasInletPress : REAL; // Suction pressure (bar)
    rSyngasDischargePress : REAL; // Discharge pressure (bar)
    rSyngasCompressorSpeed : REAL; // Compressor speed (RPM)
    
    // Wax Product Separation Inputs
    rSeparatorLevel : REAL; // Wax separator level (%)
    rSeparatorTemp : REAL; // Separator temperature (C)
END_VAR
VAR_OUTPUT
    // Fischer-Tropsch Cooling Outputs
    rCoolingValve_Z1 : REAL; // Cooling valve position Z1 (%)
    rCoolingValve_Z2 : REAL; // Cooling valve position Z2 (%)
    rCoolingValve_Z3 : REAL; // Cooling valve position Z3 (%)
    
    // Syngas Compressor Outputs
    rCompressorGuideVane : REAL; // IGV position (%)
    bCompressorSurgeAlarm : BOOL; // Anti-surge alarm
    rSyngasMassFlow_Calc : REAL; // Calculated mass flow (kg/s)
    
    // Wax Separation Outputs
    rWaxDischargeValve : REAL; // Wax level control valve (%)
    rLightSyncGasBypass : REAL; // Off-gas bypass valve (%)
    
    // General
    bSystemReady : BOOL;
    bFault : BOOL;
    iErrorCode : INT;
END_VAR
VAR
    // PID Controllers for Zones
    PID_Zone1 : FB_PID;
    PID_Zone2 : FB_PID;
    PID_Zone3 : FB_PID;
    PID_WaxLevel : FB_PID;
    
    // Internal States and Timers
    tSurgeTimer : TON;
    rPressureRatio : REAL;
    rPolytropicHead : REAL;
    
    // Constants
    cMaxTemp : REAL := 240.0; // Max FT temp
    cSurgeLimit : REAL := 3.5; // PR surge limit
END_VAR

// Initialization and Safety
IF NOT bEnable OR NOT bEmergencyStop THEN
    rCoolingValve_Z1 := 100.0; // Fail-safe open
    rCoolingValve_Z2 := 100.0; // Fail-safe open
    rCoolingValve_Z3 := 100.0; // Fail-safe open
    rCompressorGuideVane := 0.0; // Close IGV
    rWaxDischargeValve := 0.0;
    bSystemReady := FALSE;
    bFault := NOT bEmergencyStop;
    RETURN;
END_IF;

bSystemReady := TRUE;

// Fischer-Tropsch Reactor Cooling Zones Control
// Target temperature for FT reaction is approx 220C
PID_Zone1(
    rSetpoint := 220.0,
    rActualValue := rReactorTemp_Z1,
    rKp := 2.5, rTi := 120.0, rTd := 5.0,
    rOutput => rCoolingValve_Z1
);

PID_Zone2(
    rSetpoint := 220.0,
    rActualValue := rReactorTemp_Z2,
    rKp := 2.5, rTi := 120.0, rTd := 5.0,
    rOutput => rCoolingValve_Z2
);

PID_Zone3(
    rSetpoint := 220.0,
    rActualValue := rReactorTemp_Z3,
    rKp := 2.5, rTi := 120.0, rTd := 5.0,
    rOutput => rCoolingValve_Z3
);

// High Temperature Safety Override
IF (rReactorTemp_Z1 > cMaxTemp) OR (rReactorTemp_Z2 > cMaxTemp) OR (rReactorTemp_Z3 > cMaxTemp) THEN
    bFault := TRUE;
    iErrorCode := 1001; // Reactor Temp High
    rCoolingValve_Z1 := 100.0;
    rCoolingValve_Z2 := 100.0;
    rCoolingValve_Z3 := 100.0;
END_IF;

// Syngas Compressor Mass Flow Mapping & Anti-Surge Control
IF rSyngasInletPress > 0.1 THEN
    rPressureRatio := rSyngasDischargePress / rSyngasInletPress;
ELSE
    rPressureRatio := 1.0;
END_IF;

// Calculate theoretical mass flow based on speed and pressure ratio (simplified map)
rSyngasMassFlow_Calc := (rSyngasCompressorSpeed * 0.05) - (rPressureRatio * 2.1);

// Anti-surge protection
IF rPressureRatio > cSurgeLimit THEN
    tSurgeTimer(IN := TRUE, PT := T#2S);
    IF tSurgeTimer.Q THEN
        bCompressorSurgeAlarm := TRUE;
        rCompressorGuideVane := 0.0; // Restrict input
    END_IF;
ELSE
    tSurgeTimer(IN := FALSE);
    bCompressorSurgeAlarm := FALSE;
    // Normal operation IGV control based on reactor pressure demand
    rCompressorGuideVane := LIMIT(0.0, (25.0 - rReactorPressure) * 10.0, 100.0);
END_IF;

// Wax Product Separation Control
// Level control using PID
PID_WaxLevel(
    rSetpoint := 50.0, // Maintain 50% level in separator
    rActualValue := rSeparatorLevel,
    rKp := 1.2, rTi := 60.0, rTd := 0.0,
    rOutput => rWaxDischargeValve
);

// Temperature compensation for wax viscosity
IF rSeparatorTemp < 150.0 THEN
    // Wax too cold, risk of solidification, throttle discharge
    rWaxDischargeValve := rWaxDischargeValve * 0.5;
END_IF;

// Light syngas bypass based on reactor pressure
rLightSyncGasBypass := LIMIT(0.0, (rReactorPressure - 25.0) * 5.0, 100.0);

END_FUNCTION_BLOCK
```"""

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": st_code}
    ]
}

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, indent=4)

with open("data/synthetic_generation_v3_enterprise.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(record) + "\\n")

print(f"Success: {filename}")
