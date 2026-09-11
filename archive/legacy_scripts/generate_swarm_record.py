import json
import uuid
import os

prompt = "Write a deterministic Structured Text (ST) FUNCTION_BLOCK for an Industrial Pet Food Extrusion Line. The control scenario should cover pre-conditioner steam injection profiling, twin-screw extruder die pressure regulation, and enrobing fat coating vacuum cascades. Include complete VAR declarations and physical I/O."

st_code = """```iec-st
FUNCTION_BLOCK FB_PetFoodExtrusionLineControl
VAR_INPUT
    // Pre-conditioner inputs
    bStartSteamInjection : BOOL; // Command to start steam injection
    rTargetMoisturePct : REAL; // Target moisture percentage (0.0 to 100.0)
    rCurrentMoisturePct : REAL; // Current moisture percentage reading
    rSteamPressureIn : REAL; // Incoming steam pressure (bar)
    rMaterialFeedRate : REAL; // Rate of raw material entering (kg/hr)

    // Extruder inputs
    bEnableExtruder : BOOL; // Enable twin-screw extruder
    rScrewSpeedFeedback : REAL; // Current screw speed (RPM)
    rDiePressureSensor : REAL; // Pressure at the die (bar)
    rTargetDiePressure : REAL; // Desired die pressure (bar)
    rBarrelTempSensor_Zone1 : REAL; // Temperature of barrel zone 1 (deg C)
    rBarrelTempSensor_Zone2 : REAL; // Temperature of barrel zone 2 (deg C)
    rBarrelTempSensor_Zone3 : REAL; // Temperature of barrel zone 3 (deg C)
    
    // Enrobing inputs
    bEnableEnrobing : BOOL; // Enable fat coating system
    rVacuumLevelFeedback : REAL; // Current vacuum level (mbar)
    rFatFlowRateFeedback : REAL; // Current fat flow rate (L/min)
    rTargetVacuumCascade : ARRAY[1..3] OF REAL; // Target vacuum levels for cascades
END_VAR

VAR_OUTPUT
    // Pre-conditioner outputs
    rSteamValveCmd : REAL; // Command to steam control valve (0.0 to 100.0%)
    bPreConditionerReady : BOOL; // Status flag indicating readiness
    
    // Extruder outputs
    rScrewSpeedCmd : REAL; // Command to extruder screw drive (RPM)
    rBarrelHeaterCmd_Zone1 : REAL; // Heater command zone 1 (0.0 to 100.0%)
    rBarrelHeaterCmd_Zone2 : REAL; // Heater command zone 2 (0.0 to 100.0%)
    rBarrelHeaterCmd_Zone3 : REAL; // Heater command zone 3 (0.0 to 100.0%)
    bExtruderFault : BOOL; // Extruder fault condition indicator
    
    // Enrobing outputs
    rVacuumPumpCmd : REAL; // Command to vacuum pump VFD (0.0 to 100.0%)
    rFatPumpCmd : REAL; // Command to fat dosing pump (0.0 to 100.0%)
    bEnrobingActive : BOOL; // Indicates enrobing process is currently running
    
    // General Outputs
    wSystemStatusWord : WORD; // System status bitmask
    bEmergencyStopActive : BOOL; // Indicates an active emergency stop
END_VAR

VAR
    // Internal state and PI controllers
    rSteamError : REAL;
    rSteamIntegral : REAL;
    rSteamKp : REAL := 2.5;
    rSteamKi : REAL := 0.1;
    
    rDiePressureError : REAL;
    rDiePressureIntegral : REAL;
    rDiePressureKp : REAL := 1.8;
    rDiePressureKi : REAL := 0.05;
    
    rVacuumError : REAL;
    iCurrentCascadeStage : INT := 1;
    tCascadeTimer : TON; // Timer for vacuum cascade stages
    
    // Safety limits
    rMaxDiePressure : REAL := 150.0; // Maximum allowable die pressure in bar
    rMinSteamPressure : REAL := 2.0; // Minimum required steam pressure in bar
END_VAR

// 1. Pre-Conditioner Steam Injection Profiling
IF bStartSteamInjection AND (rSteamPressureIn >= rMinSteamPressure) THEN
    rSteamError := rTargetMoisturePct - rCurrentMoisturePct;
    rSteamIntegral := rSteamIntegral + rSteamError * 0.1; // Simple integration step (assuming 100ms cycle)
    
    // Anti-windup
    IF rSteamIntegral > 100.0 THEN rSteamIntegral := 100.0; END_IF;
    IF rSteamIntegral < 0.0 THEN rSteamIntegral := 0.0; END_IF;
    
    rSteamValveCmd := (rSteamKp * rSteamError) + (rSteamKi * rSteamIntegral);
    
    IF rSteamValveCmd > 100.0 THEN rSteamValveCmd := 100.0; END_IF;
    IF rSteamValveCmd < 0.0 THEN rSteamValveCmd := 0.0; END_IF;
    
    bPreConditionerReady := (ABS(rSteamError) < 1.0);
ELSE
    rSteamValveCmd := 0.0;
    rSteamIntegral := 0.0;
    bPreConditionerReady := FALSE;
END_IF;

// 2. Twin-Screw Extruder Die Pressure Regulation
IF bEnableExtruder AND bPreConditionerReady THEN
    IF rDiePressureSensor > rMaxDiePressure THEN
        bExtruderFault := TRUE;
        rScrewSpeedCmd := 0.0; // Stop immediately on over-pressure
    ELSE
        bExtruderFault := FALSE;
        rDiePressureError := rTargetDiePressure - rDiePressureSensor;
        rDiePressureIntegral := rDiePressureIntegral + rDiePressureError * 0.1;
        
        // Anti-windup for extruder
        IF rDiePressureIntegral > 500.0 THEN rDiePressureIntegral := 500.0; END_IF;
        IF rDiePressureIntegral < 0.0 THEN rDiePressureIntegral := 0.0; END_IF;
        
        rScrewSpeedCmd := (rDiePressureKp * rDiePressureError) + (rDiePressureKi * rDiePressureIntegral);
        
        IF rScrewSpeedCmd > 1200.0 THEN rScrewSpeedCmd := 1200.0; END_IF; // Max 1200 RPM
        IF rScrewSpeedCmd < 100.0 THEN rScrewSpeedCmd := 100.0; END_IF; // Min 100 RPM
    END_IF;
ELSE
    rScrewSpeedCmd := 0.0;
    rDiePressureIntegral := 0.0;
END_IF;

// 3. Enrobing Fat Coating Vacuum Cascades
IF bEnableEnrobing AND bEnableExtruder AND NOT bExtruderFault THEN
    bEnrobingActive := TRUE;
    
    // Run cascade timer
    tCascadeTimer(IN := TRUE, PT := T#30S);
    
    IF tCascadeTimer.Q THEN
        tCascadeTimer(IN := FALSE); // Reset timer
        iCurrentCascadeStage := iCurrentCascadeStage + 1;
        IF iCurrentCascadeStage > 3 THEN
            iCurrentCascadeStage := 3; // Hold at final stage
        END_IF;
    END_IF;
    
    rVacuumError := rTargetVacuumCascade[iCurrentCascadeStage] - rVacuumLevelFeedback;
    
    // Proportional control for vacuum pump
    rVacuumPumpCmd := rVacuumError * 2.0;
    IF rVacuumPumpCmd > 100.0 THEN rVacuumPumpCmd := 100.0; END_IF;
    IF rVacuumPumpCmd < 0.0 THEN rVacuumPumpCmd := 0.0; END_IF;
    
    // Fat dosing proportional to material feed rate
    rFatPumpCmd := rMaterialFeedRate * 0.05; // 5% fat addition ratio
    IF rFatPumpCmd > 100.0 THEN rFatPumpCmd := 100.0; END_IF;
    
ELSE
    bEnrobingActive := FALSE;
    rVacuumPumpCmd := 0.0;
    rFatPumpCmd := 0.0;
    iCurrentCascadeStage := 1;
    tCascadeTimer(IN := FALSE);
END_IF;

// Status Word Aggregation
wSystemStatusWord.0 := bPreConditionerReady;
wSystemStatusWord.1 := bExtruderFault;
wSystemStatusWord.2 := bEnrobingActive;

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
    json.dump(record, f, indent=2)

print(filename)
