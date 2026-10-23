import json, uuid, os

st_code = """FUNCTION_BLOCK FB_AmineRegenerationCCS
TITLE = 'CCS Amine Plant Regeneration Control'
VERSION : '1.1'
AUTHOR : 'Lumina Elite'

VAR_INPUT
    rRichAmineTemp : REAL; // Temperature of rich amine entering the regenerator [°C]
    rRegeneratorPressure : REAL; // Operating pressure of regenerator [bar]
    rReboilerTemp : REAL; // Temperature of reboiler [°C]
    rCO2CompressorSuctionPres : REAL; // Suction pressure of supercritical CO2 compressor [bar]
    rSteamFlowRate : REAL; // Flow rate of heating steam to reboiler [kg/s]
    rLeanAmineLevel : REAL; // Level of lean amine in the reboiler [%]
    bEmergencyShutdown : BOOL; // ESD signal
    bCompressorTrip : BOOL;
END_VAR

VAR_OUTPUT
    rSteamValveCmd : REAL; // Control valve command for reboiler steam [0-100%]
    rLeanAmineValveCmd : REAL; // Control valve command for lean amine flow [0-100%]
    rCO2CompressorSpeedCmd : REAL; // Speed command for CO2 compressor [0-100%]
    bReboilerHeaterEnable : BOOL; // Interlock for reboiler heater
    bVentValveOpen : BOOL; // Open vent valve during overpressure
    xSystemAlarm : BOOL; 
END_VAR

VAR
    // PID for Reboiler Temperature
    PID_ReboilerTemp : FB_PID_Controller;
    rReboilerTempSetpoint : REAL := 120.0; // Typical regeneration temp
    
    // PID for Lean Amine Level
    PID_LeanAmineLevel : FB_PID_Controller;
    rLeanLevelSetpoint : REAL := 50.0;
    
    // PID for CO2 Compressor Suction
    PID_CO2Compressor : FB_PID_Controller;
    rCO2SuctionSetpoint : REAL := 1.5;
    
    // Internal States
    rTempError : REAL;
    bTempHighHigh : BOOL;
    bPresHighHigh : BOOL;
    
    // Timers
    TON_StartDelay : TON;
    TON_ESD_Vent : TON;
END_VAR

// -----------------------------------------------------------------------------
// CONTROL LOGIC IMPLEMENTATION
// -----------------------------------------------------------------------------

// 1. Safety and Interlocks
bTempHighHigh := rReboilerTemp > 135.0;
bPresHighHigh := rRegeneratorPressure > 3.0;

IF bEmergencyShutdown OR bTempHighHigh OR bPresHighHigh THEN
    xSystemAlarm := TRUE;
    bReboilerHeaterEnable := FALSE;
    rSteamValveCmd := 0.0;
    rLeanAmineValveCmd := 0.0;
    rCO2CompressorSpeedCmd := 0.0;
    bVentValveOpen := bPresHighHigh;
    RETURN;
END_IF;

// Normal Operation Alarm Reset
xSystemAlarm := FALSE;
bVentValveOpen := FALSE;
bReboilerHeaterEnable := TRUE;

// 2. Cascade Control: Reboiler Steam Flow based on Temperature
PID_ReboilerTemp(
    rProcessValue := rReboilerTemp,
    rSetpoint := rReboilerTempSetpoint,
    rKp := 2.5,
    rTi := 60.0,
    rTd := 0.0,
    rOutMax := 100.0,
    rOutMin := 0.0
);
rSteamValveCmd := PID_ReboilerTemp.rControlOutput;

// 3. Lean Amine Level Control
PID_LeanAmineLevel(
    rProcessValue := rLeanAmineLevel,
    rSetpoint := rLeanLevelSetpoint,
    rKp := 1.2,
    rTi := 45.0,
    rTd := 5.0,
    rOutMax := 100.0,
    rOutMin := 0.0
);
rLeanAmineValveCmd := PID_LeanAmineLevel.rControlOutput;

// 4. Supercritical CO2 Compressor Control (Suction Pressure Control)
IF bCompressorTrip THEN
    rCO2CompressorSpeedCmd := 0.0;
    xSystemAlarm := TRUE;
ELSE
    PID_CO2Compressor(
        rProcessValue := rCO2CompressorSuctionPres,
        rSetpoint := rCO2SuctionSetpoint,
        rKp := -5.0, 
        rTi := 30.0,
        rTd := 0.0,
        rOutMax := 100.0,
        rOutMin := 20.0 
    );
    rCO2CompressorSpeedCmd := PID_CO2Compressor.rControlOutput;
END_IF;

END_FUNCTION_BLOCK
"""

content = "```iec-st\n" + st_code + "\n```"

record = {
    "messages": [
        {"role": "user", "content": "Generate a complex IEC 61131-3 Structured Text FUNCTION_BLOCK for a Carbon Capture and Storage (CCS) Amine Plant, specifically for amine solvent regeneration reboiler cascades, supercritical CO2 pipeline compression, and lean/rich amine heat exchange."},
        {"role": "assistant", "content": content}
    ]
}

os.makedirs("data/swarm_raw", exist_ok=True)
os.makedirs("data", exist_ok=True)

filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f)

with open("data/synthetic_generation_v3_enterprise.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(record) + "\n")
