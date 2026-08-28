import json
import uuid
import os

st_code = """```iec-st
FUNCTION_BLOCK FB_Cleanroom_HVAC_IsoClass1
TITLE = 'ISO Class 1 Semiconductor Cleanroom HVAC Advanced Controller'
VERSION : '3.4.1'
(*
  Author: Lumina AI Cloud Swarm - Elite Synthetic Data Architect
  Domain: Semiconductor Cleanroom HVAC (ISO Class 1)
  Description:
    Provides highly complex deterministic control for an Air Makeup Unit (AMU).
    Features include:
    1. Cascaded PID loops for stringent Temperature (±0.05°C) and Dew Point regulation.
    2. Ultra-Low Penetration Air (ULPA) filter pressure drop continuous monitoring.
    3. Real-time differential pressure (DP) zone balancing.
    4. Fan energy optimization using Variable Frequency Drives (VFD).
*)

VAR_INPUT
    rRoomTempAct         : REAL; // Actual ISO Class 1 Room Temperature (°C)
    rSupplyAirTempAct    : REAL; // Actual Supply Air Temperature from AMU (°C)
    rRoomDewPointAct     : REAL; // Actual Room Dew Point (°C)
    rUlpaFilterDPAct     : REAL; // Actual Differential Pressure across ULPA (Pa)
    rRoomPressAct        : REAL; // Room Pressure relative to reference (Pa)
    bSystemEnable        : BOOL; // Master System Enable Signal
    bAcknowledgeAlarms   : BOOL; // Operator Alarm Reset
    rTimeStep            : REAL; // Execution time step for discrete PID (sec)
END_VAR

VAR_OUTPUT
    rChilledWaterValve   : REAL; // AMU Cooling Coil Valve Position (0.0 - 100.0%)
    rHotWaterValve       : REAL; // AMU Heating Coil Valve Position (0.0 - 100.0%)
    rSteamHumidifier     : REAL; // AMU Steam Injection Position (0.0 - 100.0%)
    rSupplyFanVFD        : REAL; // Supply Fan Speed Reference (0.0 - 100.0%)
    rReturnFanVFD        : REAL; // Return Fan Speed Reference (0.0 - 100.0%)
    bAlarmULPAWarning    : BOOL; // ULPA DP approaching limits - maintenance required
    bAlarmULPACritical   : BOOL; // ULPA DP exceeded critical limit
    bAlarmDewPointRange  : BOOL; // Dew Point deviated beyond stringent thresholds
    bAlarmTempRange      : BOOL; // Temperature deviated beyond ISO Class 1 limits
END_VAR

VAR
    // Constant Setpoints for ISO Class 1
    rRoomTempSP          : REAL := 19.50; // Stringent 19.5 °C setpoint
    rDewPointSP          : REAL := 4.50;  // 4.5 °C Dew Point for moisture control
    rRoomPressSP         : REAL := 25.0;  // 25 Pa positive pressure
    rUlpaWarningDP       : REAL := 200.0; // 200 Pa Warning Limit
    rUlpaCriticalDP      : REAL := 250.0; // 250 Pa Critical Limit

    // Cascaded PID: Room Temp -> Supply Air Temp
    rRoomTempError       : REAL;
    rRoomTempIntegral    : REAL := 0.0;
    rRoomTempDerivative  : REAL;
    rRoomTempLastError   : REAL := 0.0;
    rSupplyAirTempSP     : REAL; // Output of Primary PID, Input to Secondary PID

    rSupplyTempError     : REAL;
    rSupplyTempIntegral  : REAL := 0.0;
    rSupplyTempLastError : REAL := 0.0;

    // Dew Point PID
    rDewPointError       : REAL;
    rDewPointIntegral    : REAL := 0.0;

    // Room Pressure PID (Fan Tracking)
    rPressError          : REAL;
    rPressIntegral       : REAL := 0.0;

    // Tuning Constants (Proportional, Integral, Derivative)
    Kp_PrimaryTemp       : REAL := 2.75;
    Ki_PrimaryTemp       : REAL := 0.012;
    Kd_PrimaryTemp       : REAL := 0.85;

    Kp_SecondaryTemp     : REAL := 5.20;
    Ki_SecondaryTemp     : REAL := 0.15;

    Kp_DewPoint          : REAL := 3.50;
    Ki_DewPoint          : REAL := 0.04;

    Kp_Pressure          : REAL := 1.20;
    Ki_Pressure          : REAL := 0.05;

    // Internal Timers for Alarms (Simulated logic conceptually)
    tUlpaWarningTimer    : REAL := 0.0;
    tUlpaCriticalTimer   : REAL := 0.0;
    rAlarmDelayLimit     : REAL := 15.0; // 15 seconds delay for debouncing
END_VAR

// ==============================================================================
// MAIN CONTROL ALGORITHM
// ==============================================================================

IF NOT bSystemEnable THEN
    // Safe state when system is disabled
    rChilledWaterValve  := 0.0;
    rHotWaterValve      := 0.0;
    rSteamHumidifier    := 0.0;
    rSupplyFanVFD       := 0.0;
    rReturnFanVFD       := 0.0;
    rRoomTempIntegral   := 0.0;
    rSupplyTempIntegral := 0.0;
    rDewPointIntegral   := 0.0;
    rPressIntegral      := 0.0;
    RETURN;
END_IF;

// 1. PRIMARY TEMPERATURE PID (Room Temp -> Supply Air Temp Setpoint)
rRoomTempError := rRoomTempSP - rRoomTempAct;
rRoomTempIntegral := rRoomTempIntegral + (rRoomTempError * rTimeStep);

// Anti-windup for Primary Integral
IF rRoomTempIntegral > 15.0 THEN rRoomTempIntegral := 15.0;
ELSIF rRoomTempIntegral < -15.0 THEN rRoomTempIntegral := -15.0; END_IF;

rRoomTempDerivative := (rRoomTempError - rRoomTempLastError) / rTimeStep;
rRoomTempLastError := rRoomTempError;

// Output of Primary PID dictates the Supply Air Temperature Setpoint (Range: 12°C to 26°C)
rSupplyAirTempSP := rRoomTempSP + (Kp_PrimaryTemp * rRoomTempError) 
                                + (Ki_PrimaryTemp * rRoomTempIntegral) 
                                + (Kd_PrimaryTemp * rRoomTempDerivative);
                                
IF rSupplyAirTempSP > 26.0 THEN rSupplyAirTempSP := 26.0;
ELSIF rSupplyAirTempSP < 12.0 THEN rSupplyAirTempSP := 12.0; END_IF;

// 2. SECONDARY TEMPERATURE PID (Supply Air Temp Act -> Valves)
rSupplyTempError := rSupplyAirTempSP - rSupplyAirTempAct;
rSupplyTempIntegral := rSupplyTempIntegral + (rSupplyTempError * rTimeStep);

// Anti-windup for Secondary Integral
IF rSupplyTempIntegral > 100.0 THEN rSupplyTempIntegral := 100.0;
ELSIF rSupplyTempIntegral < -100.0 THEN rSupplyTempIntegral := -100.0; END_IF;

// Heating and Cooling sequencing based on split-range control
VAR
    rTempControlOutput : REAL;
END_VAR

rTempControlOutput := (Kp_SecondaryTemp * rSupplyTempError) + (Ki_SecondaryTemp * rSupplyTempIntegral);

IF rTempControlOutput > 0.0 THEN
    rHotWaterValve := rTempControlOutput;
    rChilledWaterValve := 0.0;
    IF rHotWaterValve > 100.0 THEN rHotWaterValve := 100.0; END_IF;
ELSE
    rChilledWaterValve := ABS(rTempControlOutput);
    rHotWaterValve := 0.0;
    IF rChilledWaterValve > 100.0 THEN rChilledWaterValve := 100.0; END_IF;
END_IF;

// 3. DEW POINT REGULATION (Moisture Control)
rDewPointError := rDewPointSP - rRoomDewPointAct;
rDewPointIntegral := rDewPointIntegral + (rDewPointError * rTimeStep);

// Anti-windup
IF rDewPointIntegral > 100.0 THEN rDewPointIntegral := 100.0;
ELSIF rDewPointIntegral < -100.0 THEN rDewPointIntegral := -100.0; END_IF;

// Humidification if Dew Point is too low, Dehumidification is handled by chilled water overcooling (simplified)
IF rDewPointError > 0.0 THEN
    rSteamHumidifier := (Kp_DewPoint * rDewPointError) + (Ki_DewPoint * rDewPointIntegral);
    IF rSteamHumidifier > 100.0 THEN rSteamHumidifier := 100.0; END_IF;
ELSE
    rSteamHumidifier := 0.0;
END_IF;

// 4. ROOM PRESSURE & FAN TRACKING CONTROL
rPressError := rRoomPressSP - rRoomPressAct;
rPressIntegral := rPressIntegral + (rPressError * rTimeStep);
IF rPressIntegral > 50.0 THEN rPressIntegral := 50.0;
ELSIF rPressIntegral < -50.0 THEN rPressIntegral := -50.0; END_IF;

// Base supply fan speed derived from makeup air requirements, adjusted by pressure PID
rSupplyFanVFD := 70.0 + (Kp_Pressure * rPressError) + (Ki_Pressure * rPressIntegral);
IF rSupplyFanVFD > 100.0 THEN rSupplyFanVFD := 100.0;
ELSIF rSupplyFanVFD < 30.0 THEN rSupplyFanVFD := 30.0; END_IF;

// Return fan tracks supply fan with a volumetric offset to maintain positive pressure
rReturnFanVFD := rSupplyFanVFD * 0.85; 

// 5. ULPA FILTER PRESSURE DROP MONITORING & ALARM DEBOUNCING
IF rUlpaFilterDPAct >= rUlpaCriticalDP THEN
    tUlpaCriticalTimer := tUlpaCriticalTimer + rTimeStep;
    IF tUlpaCriticalTimer >= rAlarmDelayLimit THEN
        bAlarmULPACritical := TRUE;
    END_IF;
ELSE
    tUlpaCriticalTimer := 0.0;
END_IF;

IF rUlpaFilterDPAct >= rUlpaWarningDP AND rUlpaFilterDPAct < rUlpaCriticalDP THEN
    tUlpaWarningTimer := tUlpaWarningTimer + rTimeStep;
    IF tUlpaWarningTimer >= rAlarmDelayLimit THEN
        bAlarmULPAWarning := TRUE;
    END_IF;
ELSE
    tUlpaWarningTimer := 0.0;
END_IF;

// 6. DEVIATION ALARMS
bAlarmTempRange := ABS(rRoomTempError) > 0.5;
bAlarmDewPointRange := ABS(rDewPointError) > 1.0;

// 7. ALARM RESET LOGIC
IF bAcknowledgeAlarms THEN
    bAlarmULPAWarning   := FALSE;
    bAlarmULPACritical  := FALSE;
    bAlarmTempRange     := FALSE;
    bAlarmDewPointRange := FALSE;
END_IF;

END_FUNCTION_BLOCK
```"""

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: Semiconductor Cleanroom HVAC (ISO Class 1).
Task: Invent a highly complex control scenario for this domain (e.g., air makeup unit PID cascades, ultra-low penetration air (ULPA) filter pressure drops, and stringent dew point regulation).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."""

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": st_code}
    ]
}

os.makedirs("data/swarm_raw", exist_ok=True)
file_id = uuid.uuid4().hex[:8]
file_name = f"data/swarm_raw/agent_{file_id}.json"
with open(file_name, "w", encoding="utf-8") as f:
    json.dump(record, f, indent=2)
print(f"Created file: {file_name}")

os.makedirs("data", exist_ok=True)
with open("data/synthetic_generation_v3_enterprise.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(record) + "\\n")
print("Appended to JSONL")
