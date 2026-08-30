import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: Meltblown Nonwoven Fabric Line.
Task: Invent a highly complex control scenario for this domain (e.g., polymer extruder melt pump synchronization, hot air attenuation jet velocity, and drum collector suction).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O.
"""

st_code = """
FUNCTION_BLOCK FB_MeltblownLineControl
VAR_INPUT
    rExtruderPressure_bar       : REAL; // Polymer pressure at extruder outlet
    rExtruderTemp_C             : REAL; // Polymer temperature at extruder outlet
    rMeltPumpSpeed_rpm          : REAL; // Actual speed of the melt pump
    rTargetThroughput_kgh       : REAL; // Setpoint for polymer throughput
    rHotAirVelocity_ms          : REAL; // Actual velocity of attenuation hot air
    rHotAirTemp_C               : REAL; // Actual temperature of attenuation hot air
    rHotAirTargetVelocity_ms    : REAL; // Setpoint for hot air velocity
    rDrumCollectorSuction_Pa    : REAL; // Actual vacuum pressure in the collection drum
    rTargetFabricWeight_gsm     : REAL; // Target basis weight (grams per square meter)
    rLineSpeed_mpm              : REAL; // Current collector line speed
    bEnableLine                 : BOOL; // Master enable signal
    bEmergencyStop              : BOOL; // Emergency stop active low
END_VAR

VAR_OUTPUT
    rMeltPumpCommandSpeed       : REAL; // Commanded speed to the melt pump VFD
    rHotAirCommandValvePos      : REAL; // Commanded position (0-100%) for hot air bypass/control valve
    rDrumSuctionCommandSpeed    : REAL; // Commanded speed for the suction fan VFD
    bLineRunning                : BOOL; // Status flag indicating line is active
    bAlarmPolymerPressure       : BOOL; // Alarm for abnormal polymer pressure
    bAlarmHotAirTemp            : BOOL; // Alarm for hot air temperature out of bounds
    bAlarmSuctionLoss           : BOOL; // Alarm for loss of collection vacuum
    rCalculatedWebWeight        : REAL; // Estimated current web weight based on process parameters
END_VAR

VAR
    // PID Controller for Melt Pump
    rMeltPumpKp                 : REAL := 1.25;
    rMeltPumpKi                 : REAL := 0.45;
    rMeltPumpKd                 : REAL := 0.05;
    rMeltPumpError              : REAL := 0.0;
    rMeltPumpIntegral           : REAL := 0.0;
    rMeltPumpPrevError          : REAL := 0.0;
    rMeltPumpDerivative         : REAL := 0.0;
    
    // PID Controller for Hot Air Jet
    rAirVelocityKp              : REAL := 2.50;
    rAirVelocityKi              : REAL := 0.80;
    rAirVelocityError           : REAL := 0.0;
    rAirVelocityIntegral        : REAL := 0.0;
    
    // Limits and Constants
    rMaxPressure_bar            : REAL := 250.0;
    rMinPressure_bar            : REAL := 50.0;
    rMaxHotAirTemp_C            : REAL := 350.0;
    rMinSuction_Pa              : REAL := 500.0;
    
    // Internal States
    rCycleTime_s                : REAL := 0.01; // 10ms cycle time
    bInitDone                   : BOOL := FALSE;
END_VAR

// Initialization
IF NOT bInitDone THEN
    rMeltPumpIntegral := 0.0;
    rAirVelocityIntegral := 0.0;
    bInitDone := TRUE;
END_IF;

// Safety and Emergency Interlocks
IF NOT bEmergencyStop OR NOT bEnableLine THEN
    rMeltPumpCommandSpeed := 0.0;
    rHotAirCommandValvePos := 0.0;
    rDrumSuctionCommandSpeed := 0.0;
    bLineRunning := FALSE;
    bAlarmPolymerPressure := FALSE;
    bAlarmHotAirTemp := FALSE;
    bAlarmSuctionLoss := FALSE;
    RETURN;
END_IF;

bLineRunning := TRUE;

// 1. Melt Pump Synchronization & Throughput Control (PID)
// The goal is to match target throughput while maintaining stable pressure
rMeltPumpError := rTargetThroughput_kgh - (rMeltPumpSpeed_rpm * 0.15); // Assuming 0.15 kg/hr per rpm volumetric efficiency
rMeltPumpIntegral := rMeltPumpIntegral + (rMeltPumpError * rCycleTime_s);

// Anti-windup for Melt Pump Integral
IF rMeltPumpIntegral > 500.0 THEN rMeltPumpIntegral := 500.0; END_IF;
IF rMeltPumpIntegral < -500.0 THEN rMeltPumpIntegral := -500.0; END_IF;

rMeltPumpDerivative := (rMeltPumpError - rMeltPumpPrevError) / rCycleTime_s;
rMeltPumpCommandSpeed := (rMeltPumpKp * rMeltPumpError) + (rMeltPumpKi * rMeltPumpIntegral) + (rMeltPumpKd * rMeltPumpDerivative);

// Apply output limits to Melt Pump Speed (0 to 3000 RPM)
IF rMeltPumpCommandSpeed > 3000.0 THEN
    rMeltPumpCommandSpeed := 3000.0;
ELSIF rMeltPumpCommandSpeed < 0.0 THEN
    rMeltPumpCommandSpeed := 0.0;
END_IF;
rMeltPumpPrevError := rMeltPumpError;

// 2. Hot Air Attenuation Jet Velocity Control (PI)
// Controls fiber diameter (finer fibers require higher hot air velocity)
rAirVelocityError := rHotAirTargetVelocity_ms - rHotAirVelocity_ms;
rAirVelocityIntegral := rAirVelocityIntegral + (rAirVelocityError * rCycleTime_s);

// Anti-windup for Hot Air Integral
IF rAirVelocityIntegral > 100.0 THEN rAirVelocityIntegral := 100.0; END_IF;
IF rAirVelocityIntegral < 0.0 THEN rAirVelocityIntegral := 0.0; END_IF;

rHotAirCommandValvePos := (rAirVelocityKp * rAirVelocityError) + (rAirVelocityKi * rAirVelocityIntegral);

// Apply output limits to Valve Position (0 to 100%)
IF rHotAirCommandValvePos > 100.0 THEN
    rHotAirCommandValvePos := 100.0;
ELSIF rHotAirCommandValvePos < 0.0 THEN
    rHotAirCommandValvePos := 0.0;
END_IF;

// 3. Drum Collector Suction Control
// Suction needs to balance the hot air blast to ensure uniform web formation
// Suction command is proportional to hot air velocity with a base offset for pinning
rDrumSuctionCommandSpeed := 10.0 + (rHotAirVelocity_ms * 1.5); 
IF rDrumSuctionCommandSpeed > 100.0 THEN
    rDrumSuctionCommandSpeed := 100.0;
END_IF;

// 4. Diagnostic Alarms & Web Weight Estimation
IF rExtruderPressure_bar > rMaxPressure_bar OR rExtruderPressure_bar < rMinPressure_bar THEN
    bAlarmPolymerPressure := TRUE;
ELSE
    bAlarmPolymerPressure := FALSE;
END_IF;

IF rHotAirTemp_C > rMaxHotAirTemp_C THEN
    bAlarmHotAirTemp := TRUE;
ELSE
    bAlarmHotAirTemp := FALSE;
END_IF;

IF rDrumCollectorSuction_Pa < rMinSuction_Pa THEN
    bAlarmSuctionLoss := TRUE;
ELSE
    bAlarmSuctionLoss := FALSE;
END_IF;

// Feed-forward estimation of basis weight: 
// Throughput (kg/hr) divided by Line Speed (m/min) and effective width (assumed 1.6m)
// Convert kg/hr to g/min: * 1000 / 60
IF rLineSpeed_mpm > 0.0 THEN
    rCalculatedWebWeight := (rTargetThroughput_kgh * 1000.0 / 60.0) / (rLineSpeed_mpm * 1.6);
ELSE
    rCalculatedWebWeight := 0.0;
END_IF;

END_FUNCTION_BLOCK
"""

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": f"```iec-st\n{st_code}\n```"}
    ]
}

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, indent=2)

print(f"Saved to {filename}")
