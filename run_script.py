import os
import json
import uuid

os.makedirs('data/swarm_raw', exist_ok=True)
os.makedirs('data', exist_ok=True)

prompt = '''You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: Continuous Galvanizing Line (CGL).
Task: Invent a highly complex control scenario for this domain (e.g., zinc pot induction heating, air knife zinc thickness blow-off profiling, and molten metal level tracking).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O.'''

st_code = '''`iec-st
FUNCTION_BLOCK FB_CGL_ZincCoatingControl
TITLE = 'Continuous Galvanizing Line Advanced Control'
VERSION : '2.1'
AUTHOR : 'Lumina Swarm Architect'

// ==============================================================================
//  INPUT VARIABLES (Physical & HMI)
// ==============================================================================
VAR_INPUT
    Enable : BOOL; // Master enable for the coating process
    LineSpeed : REAL; // Current strip speed in m/min
    StripWidth : REAL; // Strip width in mm
    StripThickness : REAL; // Strip thickness in mm
    TargetCoatingWeight : REAL; // Target zinc coating weight in g/m^2
    ActualCoatingWeight : REAL; // Measured coating weight from x-ray gauge (g/m^2)
    ZincPotTemp : REAL; // Actual temperature of zinc pot in degC
    TargetPotTemp : REAL; // Target temperature of zinc pot in degC
    PotLevelActual : REAL; // Actual molten zinc level in mm
    PotLevelTarget : REAL; // Target molten zinc level in mm
    AirBlowerPressureAct : REAL; // Actual air knife header pressure in kPa
END_VAR

// ==============================================================================
//  OUTPUT VARIABLES (Control Commands)
// ==============================================================================
VAR_OUTPUT
    InductorPowerCMD : REAL; // Command to zinc pot induction heater (0-100%)
    AirKnifePressureCMD : REAL; // Command to air knife pressure regulator (kPa)
    AirKnifeDistanceCMD : REAL; // Command to air knife lip distance (mm)
    AirKnifeAngleCMD : REAL; // Command to air knife angle (degrees)
    IngotFeedRateCMD : REAL; // Command to zinc ingot feeder (kg/h)
    DrossPumpEnable : BOOL; // Enable signal for dross removal pump
    SystemReady : BOOL;
    AlarmActive : BOOL;
    AlarmCode : INT;
END_VAR

// ==============================================================================
//  INTERNAL VARIABLES (State, PID, Config)
// ==============================================================================
VAR
    // Zinc Pot Temp PID variables
    PID_TempError : REAL;
    PID_TempIntegral : REAL;
    PID_TempDerivative : REAL;
    PID_TempPrevError : REAL;
    TempKp : REAL := 5.5;
    TempKi : REAL := 0.15;
    TempKd : REAL := 1.2;

    // Coating Weight PID variables
    PID_CoatingError : REAL;
    PID_CoatingIntegral : REAL;
    PID_CoatingPrevError : REAL;
    CoatingKp : REAL := 0.8;
    CoatingKi : REAL := 0.05;

    // Level Control variables
    LevelError : REAL;
    IngotBaseFeed : REAL;

    // Timing and Filtering
    CycleCount : DINT;
    SmoothingFactor : REAL := 0.2;
    FilteredCoatingWeight : REAL;

    // Operating Limits
    MaxInductorPower : REAL := 100.0;
    MinInductorPower : REAL := 0.0;
    MaxKnifePressure : REAL := 80.0; // kPa
    MinKnifePressure : REAL := 10.0; // kPa
    MaxFeedRate : REAL := 5000.0; // kg/h
    AirKnifeBaseDist : REAL := 10.0; // mm
END_VAR

// ==============================================================================
//  MAIN CONTROL LOGIC
// ==============================================================================

// 0. Safety and Enable Check
IF NOT Enable THEN
    InductorPowerCMD := 0.0;
    AirKnifePressureCMD := 0.0;
    AirKnifeDistanceCMD := AirKnifeBaseDist;
    AirKnifeAngleCMD := 0.0;
    IngotFeedRateCMD := 0.0;
    DrossPumpEnable := FALSE;
    SystemReady := FALSE;
    AlarmActive := FALSE;
    AlarmCode := 0;
    
    // Reset Integrals
    PID_TempIntegral := 0.0;
    PID_CoatingIntegral := 0.0;
    RETURN;
END_IF;

SystemReady := TRUE;
AlarmActive := FALSE;
AlarmCode := 0;

// ==============================================================================
// 1. Zinc Pot Induction Heating Control (PID)
// ==============================================================================
PID_TempError := TargetPotTemp - ZincPotTemp;
PID_TempIntegral := PID_TempIntegral + (PID_TempError * 0.1); 
PID_TempDerivative := (PID_TempError - PID_TempPrevError) / 0.1;

// Anti-windup for Temp
IF PID_TempIntegral > 500.0 THEN PID_TempIntegral := 500.0; END_IF;
IF PID_TempIntegral < -500.0 THEN PID_TempIntegral := -500.0; END_IF;

InductorPowerCMD := (TempKp * PID_TempError) + (TempKi * PID_TempIntegral) + (TempKd * PID_TempDerivative);

IF InductorPowerCMD > MaxInductorPower THEN
    InductorPowerCMD := MaxInductorPower;
ELSIF InductorPowerCMD < MinInductorPower THEN
    InductorPowerCMD := MinInductorPower;
END_IF;

PID_TempPrevError := PID_TempError;

// ==============================================================================
// 2. Air Knife Zinc Thickness Blow-off Profiling (Feedforward + Feedback)
// ==============================================================================
FilteredCoatingWeight := (ActualCoatingWeight * SmoothingFactor) + (FilteredCoatingWeight * (1.0 - SmoothingFactor));

PID_CoatingError := FilteredCoatingWeight - TargetCoatingWeight;
PID_CoatingIntegral := PID_CoatingIntegral + (PID_CoatingError * 0.1);

// Anti-windup for Coating
IF PID_CoatingIntegral > 20.0 THEN PID_CoatingIntegral := 20.0; END_IF;
IF PID_CoatingIntegral < -20.0 THEN PID_CoatingIntegral := -20.0; END_IF;

// Feedforward base pressure model
AirKnifePressureCMD := (LineSpeed * 0.5) + (200.0 / TargetCoatingWeight) + (CoatingKp * PID_CoatingError) + (CoatingKi * PID_CoatingIntegral);

IF AirKnifePressureCMD > MaxKnifePressure THEN AirKnifePressureCMD := MaxKnifePressure; END_IF;
IF AirKnifePressureCMD < MinKnifePressure THEN AirKnifePressureCMD := MinKnifePressure; END_IF;

// Dynamic Knife Position based on strip thickness and speed
AirKnifeDistanceCMD := AirKnifeBaseDist + (StripThickness * 0.5) + (LineSpeed * 0.01);
AirKnifeAngleCMD := 2.5; // Slight downward angle for optimal wiping

// ==============================================================================
// 3. Molten Metal Level Tracking and Ingot Feed Control
// ==============================================================================
LevelError := PotLevelTarget - PotLevelActual;

// Formula: Feed (kg/h) = Speed(m/min) * 60 * Width(m) * TargetWeight(g/m2) * 2 / 1000
IngotBaseFeed := (LineSpeed * 60.0 * (StripWidth / 1000.0) * TargetCoatingWeight * 2.0) / 1000.0;
IngotFeedRateCMD := IngotBaseFeed + (LevelError * 10.0);

IF IngotFeedRateCMD < 0.0 THEN IngotFeedRateCMD := 0.0; END_IF;
IF IngotFeedRateCMD > MaxFeedRate THEN IngotFeedRateCMD := MaxFeedRate; END_IF;

// ==============================================================================
// 4. Auxiliary Control (Dross Removal)
// ==============================================================================
CycleCount := CycleCount + 1;
IF CycleCount MOD 36000 = 0 THEN
    DrossPumpEnable := TRUE; // Start pump every hour
END_IF;

IF CycleCount MOD 36000 > 3000 THEN
    DrossPumpEnable := FALSE; // Stop pump after 5 minutes
END_IF;

// ==============================================================================
// 5. Diagnostics and Alarms
// ==============================================================================
IF ZincPotTemp > (TargetPotTemp + 20.0) THEN
    AlarmActive := TRUE;
    AlarmCode := 101; // E_HIGH_POT_TEMP
END_IF;

IF PotLevelActual < (PotLevelTarget - 50.0) THEN
    AlarmActive := TRUE;
    AlarmCode := 201; // E_LOW_POT_LEVEL
END_IF;

END_FUNCTION_BLOCK
`'''

record = {
    'messages': [
        {'role': 'user', 'content': prompt},
        {'role': 'assistant', 'content': st_code}
    ]
}

file_name = f'data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json'
with open(file_name, 'w', encoding='utf-8') as f:
    json.dump(record, f, indent=4)

with open('data/synthetic_generation_v3_enterprise.jsonl', 'a', encoding='utf-8') as f:
    f.write(json.dumps(record) + '\\n')

print(f"EVOLUTION COMPLETE: Continuous Galvanizing Line (CGL)")
print(f"Data saved to {file_name} and appended to JSONL file.")
