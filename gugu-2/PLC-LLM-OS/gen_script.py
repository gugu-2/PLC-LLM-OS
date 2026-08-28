import json
import uuid
import os

os.makedirs('data/swarm_raw', exist_ok=True)

prompt = "Invent a highly complex control scenario for a Geothermal Power Plant (e.g., steam flash separator pressure loop and brine reinjection). Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."

st_code = """
FUNCTION_BLOCK FB_Geothermal_Flash_Separator
VAR_INPUT
    rSeparatorPressure_bar : REAL; // Current pressure of the flash separator (bar)
    rSeparatorLevel_m      : REAL; // Brine level in the separator (meters)
    rInletTemperature_C    : REAL; // Two-phase fluid inlet temperature (Celsius)
    rSteamFlowRate_kgs     : REAL; // Steam flow rate to turbine (kg/s)
    bSystemEnable          : BOOL; // Master enable signal
    bEmergencyStop         : BOOL; // E-Stop condition (active high)
END_VAR
VAR_OUTPUT
    rSteamValveCmd_pct     : REAL; // Control valve command for steam to turbine (0-100%)
    rBrineValveCmd_pct     : REAL; // Control valve command for brine reinjection (0-100%)
    bHighPressureAlarm     : BOOL; // Alarm: Separator pressure critically high
    bHighLevelAlarm        : BOOL; // Alarm: Separator brine level critically high
    bLowLevelAlarm         : BOOL; // Alarm: Separator brine level critically low
    bReinjectionPumpCmd    : BOOL; // Command to start brine reinjection pump
    bSystemFault           : BOOL; // Fault flag active
END_VAR
VAR
    // PID parameters for Pressure Control
    kp_Press               : REAL := 1.25;
    ki_Press               : REAL := 0.05;
    kd_Press               : REAL := 0.01;
    rPressSetPoint         : REAL := 6.5; // Target pressure in bar
    rPressError            : REAL;
    rPressIntegral         : REAL := 0.0;
    rPressDerivative       : REAL;
    rPressLastError        : REAL := 0.0;
    
    // PID parameters for Level Control
    kp_Level               : REAL := 2.0;
    ki_Level               : REAL := 0.1;
    kd_Level               : REAL := 0.02;
    rLevelSetPoint         : REAL := 1.5; // Target level in meters
    rLevelError            : REAL;
    rLevelIntegral         : REAL := 0.0;
    rLevelDerivative       : REAL;
    rLevelLastError        : REAL := 0.0;
    
    // Internal States & Timers
    tCycleTime             : REAL := 0.1; // 100ms cycle time
    rPressOut              : REAL;
    rLevelOut              : REAL;
END_VAR

// Initialization and Safety Checks
IF bEmergencyStop THEN
    rSteamValveCmd_pct := 0.0;
    rBrineValveCmd_pct := 0.0;
    bReinjectionPumpCmd := FALSE;
    bSystemFault := TRUE;
    // Reset integrals
    rPressIntegral := 0.0;
    rLevelIntegral := 0.0;
    RETURN;
END_IF;

IF NOT bSystemEnable THEN
    rSteamValveCmd_pct := 0.0;
    rBrineValveCmd_pct := 0.0;
    bReinjectionPumpCmd := FALSE;
    bSystemFault := FALSE;
    rPressIntegral := 0.0;
    rLevelIntegral := 0.0;
    RETURN;
END_IF;

// Alarms Evaluation
bHighPressureAlarm := rSeparatorPressure_bar > 8.0;
bHighLevelAlarm := rSeparatorLevel_m > 2.5;
bLowLevelAlarm := rSeparatorLevel_m < 0.5;

IF bHighPressureAlarm OR bHighLevelAlarm THEN
    bSystemFault := TRUE;
ELSE
    bSystemFault := FALSE;
END_IF;

// Pressure Control Loop (PID)
rPressError := rPressSetPoint - rSeparatorPressure_bar;
rPressIntegral := rPressIntegral + (rPressError * tCycleTime);
rPressDerivative := (rPressError - rPressLastError) / tCycleTime;

// Anti-windup for pressure integral
IF rPressIntegral > 100.0 THEN rPressIntegral := 100.0; END_IF;
IF rPressIntegral < -100.0 THEN rPressIntegral := -100.0; END_IF;

rPressOut := (kp_Press * rPressError) + (ki_Press * rPressIntegral) + (kd_Press * rPressDerivative);
rPressLastError := rPressError;

// Map PID output to Valve Command (Reverse acting: if pressure high, open steam valve more? 
// No, if pressure high, open valve to turbine to relieve pressure)
rSteamValveCmd_pct := 50.0 - rPressOut; // Base 50%
IF rSteamValveCmd_pct > 100.0 THEN rSteamValveCmd_pct := 100.0; END_IF;
IF rSteamValveCmd_pct < 0.0 THEN rSteamValveCmd_pct := 0.0; END_IF;


// Level Control Loop (PID)
rLevelError := rLevelSetPoint - rSeparatorLevel_m;
rLevelIntegral := rLevelIntegral + (rLevelError * tCycleTime);
rLevelDerivative := (rLevelError - rLevelLastError) / tCycleTime;

// Anti-windup for level integral
IF rLevelIntegral > 100.0 THEN rLevelIntegral := 100.0; END_IF;
IF rLevelIntegral < -100.0 THEN rLevelIntegral := -100.0; END_IF;

rLevelOut := (kp_Level * rLevelError) + (ki_Level * rLevelIntegral) + (kd_Level * rLevelDerivative);
rLevelLastError := rLevelError;

// Map Level output to Brine valve (Direct acting: if level high, open valve more to dump brine)
rBrineValveCmd_pct := 50.0 - rLevelOut; 
IF rBrineValveCmd_pct > 100.0 THEN rBrineValveCmd_pct := 100.0; END_IF;
IF rBrineValveCmd_pct < 0.0 THEN rBrineValveCmd_pct := 0.0; END_IF;

// Reinjection Pump Control
IF rSeparatorLevel_m > 0.8 AND NOT bSystemFault THEN
    bReinjectionPumpCmd := TRUE;
ELSIF rSeparatorLevel_m < 0.5 THEN
    bReinjectionPumpCmd := FALSE;
END_IF;

END_FUNCTION_BLOCK
"""

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": f"```iec-st\n{st_code}\n```"}
    ]
}

filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, indent=2)

print(f"Saved to {filename}")
