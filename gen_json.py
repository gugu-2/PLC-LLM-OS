import json
import uuid
import os

os.makedirs("data/swarm_raw", exist_ok=True)
os.makedirs("data", exist_ok=True)

code = """```iec-st
FUNCTION_BLOCK FB_RAS_CoreController
TITLE = 'Commercial RAS Master Controller'
// Includes Ozone Dosing, MBBR Ammonia tracking, Pure Oxygen Injection, and Degassing

VAR_INPUT
    rAmmoniaLevel         : REAL; // mg/L NH3-N (TAN)
    rWaterTemp            : REAL; // Celsius
    rDO_Level             : REAL; // mg/L Dissolved Oxygen
    rORP_Level            : REAL; // mV Oxidation-Reduction Potential
    rWaterFlowRate        : REAL; // m3/h
    rPH_Level             : REAL; // pH
    rCO2_Level            : REAL; // mg/L Dissolved CO2
    bSystemEnable         : BOOL; // Master enable
    bEmergencyStop        : BOOL; // E-Stop from safety relay
    bBackwashActive       : BOOL; // True if mechanical filter is in backwash
END_VAR

VAR_OUTPUT
    rOzoneDoseRate        : REAL; // g/h ozone generator setpoint
    rOxygenValvePosition  : REAL; // 0-100% position for O2 V-port ball valve
    bSkimmerPumpRun       : BOOL; // Foam Fractionation Pump contactor
    bDegassingFanRun      : BOOL; // CO2 stripping tower fan
    rAlkalinityDoseRate   : REAL; // mL/min for NaOH or NaHCO3 dosing
    bAlarmAmmoniaHigh     : BOOL; // Alarm flag
    bAlarmDOLow           : BOOL; // Alarm flag
    bAlarmOzoneHigh       : BOOL; // Alarm flag
    bAlarmPHLow           : BOOL; // Alarm flag
END_VAR

VAR
    rMBBR_Kinetics        : REAL; // Dynamic kinetics coefficient
    rTargetDO             : REAL := 8.5; // Target DO in mg/L
    rTargetORP            : REAL := 300.0; // Target ORP in mV
    rTargetPH             : REAL := 7.2; // Target pH
    rAmmoniaLimit         : REAL := 1.5; // mg/L max safe limit for TAN
    rOzoneMax             : REAL := 50.0; // g/h max limit
    rCO2Limit             : REAL := 15.0; // mg/L max CO2
    
    // Controllers
    rErrorDO              : REAL;
    rKp_Oxygen            : REAL := 15.0;
    rKi_Oxygen            : REAL := 0.5;
    rIntegralDO           : REAL;
    
    rErrorORP             : REAL;
    rKp_Ozone             : REAL := 2.5;
    rKi_Ozone             : REAL := 0.1;
    rIntegralORP          : REAL;
    
    rErrorPH              : REAL;
    rKp_PH                : REAL := 10.0;
    rKi_PH                : REAL := 0.2;
    rIntegralPH           : REAL;
    
    tCycleTime_ms         : REAL := 100.0; // Cycle time ms
END_VAR

// --- System Safety & State Management ---
IF bEmergencyStop OR NOT bSystemEnable THEN
    rOzoneDoseRate := 0.0;
    rOxygenValvePosition := 0.0;
    bSkimmerPumpRun := FALSE;
    bDegassingFanRun := FALSE;
    rAlkalinityDoseRate := 0.0;
    bAlarmAmmoniaHigh := FALSE;
    bAlarmDOLow := FALSE;
    bAlarmOzoneHigh := FALSE;
    bAlarmPHLow := FALSE;
    rIntegralDO := 0.0;
    rIntegralORP := 0.0;
    rIntegralPH := 0.0;
    RETURN;
END_IF;

// --- 1. MBBR Ammonia Tracking ---
// Base rate assumed at 20C. Growth rate modifier applied.
rMBBR_Kinetics := 1.047 ** (rWaterTemp - 20.0);
IF rAmmoniaLevel > (rAmmoniaLimit / rMBBR_Kinetics) THEN
    bAlarmAmmoniaHigh := TRUE;
ELSIF rAmmoniaLevel < (rAmmoniaLimit * 0.8) THEN
    bAlarmAmmoniaHigh := FALSE;
END_IF;

// --- 2. Pure Oxygen Injection Cascade (PI Controller) ---
rErrorDO := rTargetDO - rDO_Level;
IF rDO_Level < 5.0 THEN
    bAlarmDOLow := TRUE;
ELSE
    bAlarmDOLow := FALSE;
END_IF;

rIntegralDO := rIntegralDO + (rErrorDO * (tCycleTime_ms / 1000.0));
IF rIntegralDO > 50.0 THEN rIntegralDO := 50.0; END_IF;
IF rIntegralDO < -50.0 THEN rIntegralDO := -50.0; END_IF;

rOxygenValvePosition := (rKp_Oxygen * rErrorDO) + (rKi_Oxygen * rIntegralDO);
IF rOxygenValvePosition > 100.0 THEN rOxygenValvePosition := 100.0; END_IF;
IF rOxygenValvePosition < 0.0 THEN rOxygenValvePosition := 0.0; END_IF;

// --- 3. Ozone Foam Fractionation Dosing ---
rErrorORP := rTargetORP - rORP_Level;
IF rORP_Level > 400.0 THEN
    bAlarmOzoneHigh := TRUE;
    rOzoneDoseRate := 0.0; 
    rIntegralORP := 0.0;
ELSE
    bAlarmOzoneHigh := FALSE;
    rIntegralORP := rIntegralORP + (rErrorORP * (tCycleTime_ms / 1000.0));
    IF rIntegralORP > 20.0 THEN rIntegralORP := 20.0; END_IF;
    IF rIntegralORP < -20.0 THEN rIntegralORP := -20.0; END_IF;

    rOzoneDoseRate := (rKp_Ozone * rErrorORP) + (rKi_Ozone * rIntegralORP);
    IF rWaterFlowRate > 0.0 THEN
        rOzoneDoseRate := rOzoneDoseRate * (rWaterFlowRate / 500.0);
    ELSE
        rOzoneDoseRate := 0.0;
    END_IF;
    
    IF rOzoneDoseRate > rOzoneMax THEN rOzoneDoseRate := rOzoneMax; END_IF;
    IF rOzoneDoseRate < 0.0 THEN rOzoneDoseRate := 0.0; END_IF;
END_IF;

IF bBackwashActive OR rORP_Level < 150.0 THEN
    bSkimmerPumpRun := FALSE;
ELSE
    bSkimmerPumpRun := TRUE;
END_IF;

// --- 4. CO2 Degassing & Alkalinity Control ---
IF rCO2_Level > rCO2Limit THEN
    bDegassingFanRun := TRUE;
ELSIF rCO2_Level < (rCO2Limit - 3.0) THEN
    bDegassingFanRun := FALSE;
END_IF;

rErrorPH := rTargetPH - rPH_Level;
IF rPH_Level < 6.8 THEN
    bAlarmPHLow := TRUE;
ELSE
    bAlarmPHLow := FALSE;
END_IF;

IF rErrorPH > 0.0 THEN
    rIntegralPH := rIntegralPH + (rErrorPH * (tCycleTime_ms / 1000.0));
    IF rIntegralPH > 100.0 THEN rIntegralPH := 100.0; END_IF;
    
    rAlkalinityDoseRate := (rKp_PH * rErrorPH) + (rKi_PH * rIntegralPH);
    IF rAlkalinityDoseRate > 500.0 THEN rAlkalinityDoseRate := 500.0; END_IF;
ELSE
    rAlkalinityDoseRate := 0.0;
    IF rIntegralPH > 0.0 THEN rIntegralPH := rIntegralPH - 0.1; END_IF;
    IF rIntegralPH < 0.0 THEN rIntegralPH := 0.0; END_IF;
END_IF;

END_FUNCTION_BLOCK
```"""

prompt = "Create a highly complex IEC 61131-3 Structured Text FUNCTION_BLOCK for a Commercial Recirculating Aquaculture System (RAS). Include ozone foam fractionation dosing, moving bed biofilm reactor (MBBR) ammonia tracking, and pure oxygen injection cascades."

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": code}
    ]
}

# 1. Save JSON to a uniquely named file in the swarm directory (per user instruction)
file_name = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(file_name, "w", encoding="utf-8") as f:
    json.dump(record, f, indent=2)

# 2. Append this JSON object as a single line to data/synthetic_generation_v3_enterprise.jsonl (per system instruction)
with open("data/synthetic_generation_v3_enterprise.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(record) + "\n")
