import os, json, uuid

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: Continuous Hot-Dip Aluminizing Line.
Task: Invent a highly complex control scenario for this domain (e.g., radiant tube annealing furnace zones, molten aluminum-silicon bath level control, and electromagnetic wiping).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."""

code = """```iec-st
FUNCTION_BLOCK FB_AluminizingLineControl
TITLE = 'Continuous Hot-Dip Aluminizing Line Main Control'
VERSION : '2.1'
AUTHOR  : 'Lumina Swarm'

VAR_INPUT
    // Radiant Tube Annealing Furnace
    rZone1_Temp_PV      : REAL; // Zone 1 Temperature Process Value (deg C)
    rZone2_Temp_PV      : REAL; // Zone 2 Temperature Process Value (deg C)
    rZone3_Temp_PV      : REAL; // Zone 3 Temperature Process Value (deg C)
    rStripSpeed         : REAL; // Line Strip Speed (m/min)
    rStripTension       : REAL; // Strip Tension (N)
    
    // Molten Al-Si Bath
    rBathLevel_PV       : REAL; // Bath Level Process Value (mm)
    rBathTemp_PV        : REAL; // Bath Temperature (deg C)
    rIngotFeedRate      : REAL; // Rate of ingot feeding (kg/h)
    
    // Electromagnetic Wiping (EMW)
    rCoatingWeight_SP   : REAL; // Target Coating Weight (g/m2)
    rStripThickness     : REAL; // Strip Thickness (mm)
    rAirKnifePress_PV   : REAL; // Backup Air Knife Pressure (bar)
    
    // System Status
    bEmergencyStop      : BOOL;
    bLineRunning        : BOOL;
END_VAR

VAR_OUTPUT
    // Furnace Control
    rZone1_GasValveOut  : REAL; // Gas valve position (0-100%)
    rZone2_GasValveOut  : REAL; // Gas valve position (0-100%)
    rZone3_GasValveOut  : REAL; // Gas valve position (0-100%)
    
    // Bath Control
    bIngotFeederStart   : BOOL; // Command to start ingot feeder
    bInductorHeaterCmd  : BOOL; // Inductor heater PWM command
    rInductorPowerOut   : REAL; // Inductor power level (0-100%)
    
    // EMW Control
    rEMW_CurrentOut     : REAL; // Electromagnetic wiper current output (A)
    rEMW_FreqOut        : REAL; // Electromagnetic wiper frequency (Hz)
    
    // Alarms
    bAlarm_TempHigh     : BOOL;
    bAlarm_BathLevelLow : BOOL;
    bAlarm_EMW_Fault    : BOOL;
END_VAR

VAR
    // PID Controllers for Furnace
    PID_Zone1 : FB_PID;
    PID_Zone2 : FB_PID;
    PID_Zone3 : FB_PID;
    
    // Target Setpoints (internal profiles based on strip speed and thickness)
    rZone1_Temp_SP : REAL;
    rZone2_Temp_SP : REAL;
    rZone3_Temp_SP : REAL;
    
    // Bath Control Variables
    rBathLevel_SP : REAL := 500.0; // Nominal bath level in mm
    rBathTemp_SP  : REAL := 660.0; // Nominal melting point of Al-Si alloy
    tonBathDelay  : TON;
    
    // EMW Variables
    rCalculatedFlux : REAL;
    rDynamicGain    : REAL;
END_VAR

// -----------------------------------------------------------------------------
// CONTROL LOGIC IMPLEMENTATION
// -----------------------------------------------------------------------------

// 1. Emergency Stop Handling
IF bEmergencyStop THEN
    rZone1_GasValveOut := 0.0;
    rZone2_GasValveOut := 0.0;
    rZone3_GasValveOut := 0.0;
    bIngotFeederStart  := FALSE;
    bInductorHeaterCmd := FALSE;
    rInductorPowerOut  := 0.0;
    rEMW_CurrentOut    := 0.0;
    rEMW_FreqOut       := 0.0;
    RETURN;
END_IF;

// 2. Radiant Tube Annealing Furnace Control
// Calculate dynamic setpoints based on strip speed and thickness
// Thicker or faster strips require higher zone temperatures to reach annealing temp
rZone1_Temp_SP := 750.0 + (rStripSpeed * 0.5) + (rStripThickness * 10.0);
rZone2_Temp_SP := 800.0 + (rStripSpeed * 0.6) + (rStripThickness * 12.0);
rZone3_Temp_SP := 850.0 + (rStripSpeed * 0.7) + (rStripThickness * 15.0);

// Zone 1 PID Execution
PID_Zone1(
    rPV := rZone1_Temp_PV,
    rSP := rZone1_Temp_SP,
    rKp := 2.5, rKi := 0.1, rKd := 0.05,
    rOut => rZone1_GasValveOut
);

// Zone 2 PID Execution
PID_Zone2(
    rPV := rZone2_Temp_PV,
    rSP := rZone2_Temp_SP,
    rKp := 2.8, rKi := 0.12, rKd := 0.06,
    rOut => rZone2_GasValveOut
);

// Zone 3 PID Execution
PID_Zone3(
    rPV := rZone3_Temp_PV,
    rSP := rZone3_Temp_SP,
    rKp := 3.0, rKi := 0.15, rKd := 0.08,
    rOut => rZone3_GasValveOut
);

// High Temperature Alarms
bAlarm_TempHigh := (rZone1_Temp_PV > 900.0) OR (rZone2_Temp_PV > 900.0) OR (rZone3_Temp_PV > 900.0);

// 3. Molten Aluminum-Silicon Bath Level & Temperature Control
// Ingot feeder control logic (On/Off with hysteresis)
IF rBathLevel_PV < (rBathLevel_SP - 20.0) THEN
    bIngotFeederStart := TRUE;
ELSIF rBathLevel_PV > (rBathLevel_SP + 5.0) THEN
    bIngotFeederStart := FALSE;
END_IF;

bAlarm_BathLevelLow := (rBathLevel_PV < 400.0);

// Inductor heating control (simplified proportional control)
IF rBathTemp_PV < rBathTemp_SP THEN
    rInductorPowerOut := (rBathTemp_SP - rBathTemp_PV) * 5.0; // P-Gain = 5.0
    IF rInductorPowerOut > 100.0 THEN
        rInductorPowerOut := 100.0;
    END_IF;
    bInductorHeaterCmd := TRUE;
ELSE
    rInductorPowerOut := 0.0;
    bInductorHeaterCmd := FALSE;
END_IF;

// 4. Electromagnetic Wiping (EMW) Control
// The wiping effect depends on strip speed, AC frequency, and current.
// Higher speeds require higher electromagnetic forces to wipe excess alloy.

IF bLineRunning AND (rStripSpeed > 0.0) THEN
    // Calculate dynamic gain based on desired coating weight
    rDynamicGain := 1000.0 / rCoatingWeight_SP;
    
    // Frequency formulation based on thickness and required skin depth
    rEMW_FreqOut := 400.0 + (1.5 / rStripThickness) * 100.0;
    IF rEMW_FreqOut > 1000.0 THEN
        rEMW_FreqOut := 1000.0;
    END_IF;
    
    // Current output proportional to strip speed and dynamic gain
    rEMW_CurrentOut := rStripSpeed * rDynamicGain * 0.8;
    IF rEMW_CurrentOut > 5000.0 THEN
        rEMW_CurrentOut := 5000.0; // Max 5000A
    END_IF;
ELSE
    rEMW_CurrentOut := 0.0;
    rEMW_FreqOut := 0.0;
END_IF;

// EMW Fault detection
bAlarm_EMW_Fault := (rEMW_CurrentOut > 4800.0) AND (rCoatingWeight_SP < 50.0);

END_FUNCTION_BLOCK
```"""

record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
filepath = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filepath, "w", encoding="utf-8") as f:
    json.dump(record, f)
print(f"Generated {filepath}")
