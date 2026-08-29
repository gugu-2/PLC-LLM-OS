import os
import json
import uuid

os.makedirs("data/swarm_raw", exist_ok=True)
os.makedirs("data", exist_ok=True)

prompt = "Design an advanced Tunnel Pasteurizer control system in Structured Text (ST). Implement spray zone thermal gradient profiling, bottle breakage jam detection, and water loop heat energy recovery cascades. Include complete VAR declarations and physical I/O."

assistant_content = """```iec-st
FUNCTION_BLOCK FB_TunnelPasteurizer_Optimizer
TITLE = 'Advanced Tunnel Pasteurizer Control with Energy Recovery'
VERSION : '2.1'

VAR_INPUT
    // Physical I/O - Sensors
    rBeltSpeedActual       : REAL; // mm/s
    rZoneTempActual        : ARRAY[1..8] OF REAL; // Degrees Celsius (Zones 1-8)
    rWaterLevelTank        : ARRAY[1..8] OF REAL; // mm
    bBottleJamSensor       : ARRAY[1..8] OF BOOL; // Optical jam detectors
    uiBottleCountIn        : UINT; // Entry counter
    uiBottleCountOut       : UINT; // Exit counter
    rHeatExchangerTempIn   : REAL; // From cooling zone heat recovery
    bEmergencyStop         : BOOL; // Safety circuit
END_VAR

VAR_OUTPUT
    // Physical I/O - Actuators
    rSteamValveCmd         : ARRAY[1..8] OF REAL; // 0.0 to 100.0%
    rCoolingValveCmd       : ARRAY[1..8] OF REAL; // 0.0 to 100.0%
    rBeltSpeedSetpoint     : REAL; // mm/s command
    rHeatExchangerPumpCmd  : REAL; // 0.0 to 100.0%
    
    // System States
    bBottleBreakageAlarm   : BOOL;
    bThermalGradientAlarm  : BOOL;
    rEstimatedPU           : REAL; // Pasteurization Units accumulated
    rEnergyRecoveredKW     : REAL; // Kilowatts recovered
    bSystemReady           : BOOL;
END_VAR

VAR
    // Internal State
    rZoneTempSetpoint      : ARRAY[1..8] OF REAL := [30.0, 45.0, 60.0, 72.0, 72.0, 55.0, 40.0, 25.0];
    rZoneTempError         : ARRAY[1..8] OF REAL;
    rPID_Integral          : ARRAY[1..8] OF REAL;
    rPID_LastErr           : ARRAY[1..8] OF REAL;
    
    i                      : INT;
    uiCountMismatch        : UINT;
    tJamTimer              : TON;
    tPU_UpdateTimer        : TON;
    
    // Constants
    rKp                    : REAL := 2.5;
    rKi                    : REAL := 0.05;
    rKd                    : REAL := 0.1;
    rBaseTemp              : REAL := 60.0; // Base temp for PU calculation (e.g., beer)
    rZValue                : REAL := 6.94; // Z-value for PU calc
END_VAR

// --- Safety and Interlocks ---
IF bEmergencyStop THEN
    FOR i := 1 TO 8 DO
        rSteamValveCmd[i] := 0.0;
        rCoolingValveCmd[i] := 0.0;
    END_FOR;
    rBeltSpeedSetpoint := 0.0;
    rHeatExchangerPumpCmd := 0.0;
    bSystemReady := FALSE;
    RETURN;
END_IF;

bSystemReady := TRUE;

// --- Bottle Breakage and Jam Detection ---
// Detect mismatch between entry and exit counters indicating breakage
IF uiBottleCountIn > uiBottleCountOut THEN
    uiCountMismatch := uiBottleCountIn - uiBottleCountOut;
ELSE
    uiCountMismatch := 0;
END_IF;

// Trigger alarm if mismatch exceeds threshold (e.g., normal buffer + 10) or hard jam detected
bBottleBreakageAlarm := FALSE;
FOR i := 1 TO 8 DO
    IF bBottleJamSensor[i] THEN
        bBottleBreakageAlarm := TRUE;
    END_IF;
END_FOR;
IF uiCountMismatch > 500 THEN // Assuming typical belt capacity is known, simplified here
    bBottleBreakageAlarm := TRUE;
END_IF;

// --- Thermal Gradient Profiling and PID Control ---
bThermalGradientAlarm := FALSE;
FOR i := 1 TO 8 DO
    rZoneTempError[i] := rZoneTempSetpoint[i] - rZoneTempActual[i];
    
    // Alarm if temp deviates by more than 5 degrees
    IF ABS(rZoneTempError[i]) > 5.0 THEN
        bThermalGradientAlarm := TRUE;
    END_IF;
    
    // PID Calculation
    rPID_Integral[i] := rPID_Integral[i] + rZoneTempError[i];
    
    // Anti-windup
    IF rPID_Integral[i] > 1000.0 THEN rPID_Integral[i] := 1000.0; END_IF;
    IF rPID_Integral[i] < -1000.0 THEN rPID_Integral[i] := -1000.0; END_IF;
    
    // Valve commands based on heating or cooling zones
    IF i <= 5 THEN // Heating and Pasteurization Zones
        rSteamValveCmd[i] := (rKp * rZoneTempError[i]) + (rKi * rPID_Integral[i]) + (rKd * (rZoneTempError[i] - rPID_LastErr[i]));
        IF rSteamValveCmd[i] > 100.0 THEN rSteamValveCmd[i] := 100.0; END_IF;
        IF rSteamValveCmd[i] < 0.0 THEN rSteamValveCmd[i] := 0.0; END_IF;
        rCoolingValveCmd[i] := 0.0;
    ELSE // Cooling Zones
        rCoolingValveCmd[i] := -1.0 * ((rKp * rZoneTempError[i]) + (rKi * rPID_Integral[i]) + (rKd * (rZoneTempError[i] - rPID_LastErr[i])));
        IF rCoolingValveCmd[i] > 100.0 THEN rCoolingValveCmd[i] := 100.0; END_IF;
        IF rCoolingValveCmd[i] < 0.0 THEN rCoolingValveCmd[i] := 0.0; END_IF;
        rSteamValveCmd[i] := 0.0;
    END_IF;
    
    rPID_LastErr[i] := rZoneTempError[i];
END_FOR;

// --- Pasteurization Unit (PU) Accumulation ---
// PU = t * 10^((T - Tbase)/Z)
// Simplified continuous integration per scan cycle (assuming 1s cycle for logic)
IF rZoneTempActual[4] >= rBaseTemp THEN
    rEstimatedPU := rEstimatedPU + (1.0 / 60.0) * EXPT(10.0, ((rZoneTempActual[4] - rBaseTemp) / rZValue));
END_IF;
IF rZoneTempActual[5] >= rBaseTemp THEN
    rEstimatedPU := rEstimatedPU + (1.0 / 60.0) * EXPT(10.0, ((rZoneTempActual[5] - rBaseTemp) / rZValue));
END_IF;

// --- Water Loop Heat Energy Recovery Cascade ---
// Transfer heat from cooling zones (6-8) to pre-heating zones (1-2)
IF rHeatExchangerTempIn > (rZoneTempActual[1] + 5.0) THEN
    rHeatExchangerPumpCmd := 85.0; // Run heat recovery pump at 85%
    rEnergyRecoveredKW := (rHeatExchangerTempIn - rZoneTempActual[1]) * 4.18 * 10.0; // Approx Q = m*c*dT
ELSE
    rHeatExchangerPumpCmd := 20.0; // Idle circulation
    rEnergyRecoveredKW := 0.0;
END_IF;

// --- Belt Speed Regulation ---
// Slow down belt if PU is accumulating too slowly, or speed up if exceeding target
IF rEstimatedPU < 15.0 THEN
    rBeltSpeedSetpoint := 20.0; // Slow speed to increase residence time
ELSIF rEstimatedPU > 25.0 THEN
    rBeltSpeedSetpoint := 45.0; // High speed to prevent over-pasteurization
ELSE
    rBeltSpeedSetpoint := 35.0; // Nominal speed
END_IF;

// Stop belt entirely if jam detected
IF bBottleBreakageAlarm THEN
    rBeltSpeedSetpoint := 0.0;
END_IF;

END_FUNCTION_BLOCK
```"""

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": assistant_content}
    ]
}

filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, indent=2)

jsonl_filename = "data/synthetic_generation_v3_enterprise.jsonl"
with open(jsonl_filename, "a", encoding="utf-8") as f:
    f.write(json.dumps(record) + "\n")

print(f"MY Success: Wrote to {filename} and appended to {jsonl_filename}")
