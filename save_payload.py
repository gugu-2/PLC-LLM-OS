import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: Municipal Solid Waste (MSW) Incinerator.
Task: Invent a highly complex control scenario for this domain (e.g., walking grate combustion sequencing, flue gas wet scrubber pH cascades, and Selective Non-Catalytic Reduction (SNCR)).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."""

iec_code = """```iec-st
FUNCTION_BLOCK FB_MSW_Incinerator_Control
VAR_INPUT
    bStart_Sequence         : BOOL; // Master start
    bEmergency_Stop         : BOOL;
    rFurnace_Temp           : REAL; // Current furnace temperature (C)
    rO2_Level               : REAL; // Oxygen level at boiler exit (%)
    rSteam_Flow             : REAL; // Main steam flow (t/h)
    rGrate_Speed_Ref        : REAL; // Operator reference for grate speed
    rScrubber_pH_PV         : REAL; // Process variable pH from wet scrubber
    rNOx_Emissions_PV       : REAL; // NOx emissions at stack (mg/Nm3)
    rAmmonia_Tank_Level     : REAL; // Ammonia storage tank level (%)
END_VAR

VAR_OUTPUT
    bSystem_Running         : BOOL;
    rGrate_Speed_Cmd        : REAL; // Command to grate hydraulic drives (mm/s)
    rPrimary_Air_Cmd        : REAL; // Primary air fan speed (%)
    rSecondary_Air_Cmd      : REAL; // Secondary air fan speed (%)
    rScrubber_Dosing_Cmd    : REAL; // Caustic dosing pump speed (%)
    rSNCR_Injection_Cmd     : REAL; // Ammonia injection rate (L/h)
    bAlarm_Temp_Low         : BOOL; // Furnace temp < 850C for 2 seconds (legal limit)
    bAlarm_NOx_High         : BOOL; // High NOx
END_VAR

VAR
    // Internal state machine
    iState                  : INT := 0; 
    
    // Combustion Control (ACC)
    fbPID_Temp              : PID;
    fbPID_O2                : PID;
    rTemp_Setpoint          : REAL := 950.0; // Target temp C
    rO2_Setpoint            : REAL := 6.0;   // Target O2 %
    
    // SNCR Control
    fbPID_SNCR              : PID;
    rNOx_Setpoint           : REAL := 150.0; // Target NOx mg/Nm3
    
    // Scrubber Control
    fbPID_Scrubber          : PID;
    rScrubber_pH_SP         : REAL := 7.5;   // Target pH
    
    // Timers
    tonTempLowAlert         : TON;
    tonGrateCycle           : TON;
    
    bInit                   : BOOL := FALSE;
END_VAR

// Initialization
IF NOT bInit THEN
    fbPID_Temp.KP := 2.5; fbPID_Temp.TN := T#120S; fbPID_Temp.TV := T#0S;
    fbPID_O2.KP := 1.2; fbPID_O2.TN := T#60S; fbPID_O2.TV := T#10S;
    fbPID_SNCR.KP := 0.8; fbPID_SNCR.TN := T#45S; fbPID_SNCR.TV := T#0S;
    fbPID_Scrubber.KP := 1.5; fbPID_Scrubber.TN := T#30S; fbPID_Scrubber.TV := T#0S;
    bInit := TRUE;
END_IF;

IF bEmergency_Stop THEN
    iState := 99; // Emergency Stop State
END_IF;

CASE iState OF
    0: // OFF
        bSystem_Running := FALSE;
        rGrate_Speed_Cmd := 0.0;
        rPrimary_Air_Cmd := 0.0;
        rSecondary_Air_Cmd := 0.0;
        rScrubber_Dosing_Cmd := 0.0;
        rSNCR_Injection_Cmd := 0.0;
        
        IF bStart_Sequence THEN
            iState := 10;
        END_IF;
        
    10: // PURGE AND STARTUP
        bSystem_Running := TRUE;
        rPrimary_Air_Cmd := 30.0; // Purge flow
        rSecondary_Air_Cmd := 20.0;
        IF rFurnace_Temp > 400.0 THEN // Auxiliary burners running
            iState := 20;
        END_IF;
        
    20: // NORMAL OPERATION (Advanced Combustion Control)
        // 1. Grate Speed calculation based on Steam Flow and Furnace Temp
        // Inverse relationship: if temp drops, speed up grate slightly to bring in new fuel
        fbPID_Temp(
            ACT := rFurnace_Temp,
            SET := rTemp_Setpoint,
            SUP := 0.0,
            INF := -100.0,
            ENABLE := TRUE
        );
        rGrate_Speed_Cmd := LIMIT(5.0, rGrate_Speed_Ref + (fbPID_Temp.OUT * 0.1), 100.0);
        
        // 2. Air Flow (O2 control)
        fbPID_O2(
            ACT := rO2_Level,
            SET := rO2_Setpoint,
            SUP := 100.0,
            INF := 0.0,
            ENABLE := TRUE
        );
        rPrimary_Air_Cmd := LIMIT(20.0, fbPID_O2.OUT * 0.7 + 20.0, 100.0);
        rSecondary_Air_Cmd := LIMIT(10.0, fbPID_O2.OUT * 0.3 + 10.0, 100.0);
        
        // 3. SNCR Ammonia Injection Control (NOx reduction)
        // Only inject if temp is in optimal window (850C - 1050C)
        IF rFurnace_Temp > 850.0 AND rFurnace_Temp < 1050.0 THEN
            fbPID_SNCR(
                ACT := rNOx_Emissions_PV,
                SET := rNOx_Setpoint,
                SUP := 100.0,
                INF := 0.0,
                ENABLE := TRUE
            );
            // Reverse acting: if NOx is high (above setpoint), increase ammonia
            rSNCR_Injection_Cmd := LIMIT(0.0, (rNOx_Emissions_PV - rNOx_Setpoint) * fbPID_SNCR.KP, 100.0);
        ELSE
            rSNCR_Injection_Cmd := 0.0;
        END_IF;
        
        // 4. Wet Scrubber pH Cascade Control
        fbPID_Scrubber(
            ACT := rScrubber_pH_PV,
            SET := rScrubber_pH_SP,
            SUP := 100.0,
            INF := 0.0,
            ENABLE := TRUE
        );
        rScrubber_Dosing_Cmd := LIMIT(0.0, fbPID_Scrubber.OUT, 100.0);
        
        IF NOT bStart_Sequence THEN
            iState := 0;
        END_IF;

    99: // EMERGENCY STOP
        bSystem_Running := FALSE;
        rGrate_Speed_Cmd := 0.0;
        rPrimary_Air_Cmd := 100.0; // Max air to cool down
        rSecondary_Air_Cmd := 100.0;
        rScrubber_Dosing_Cmd := 100.0; // Max dosing to neutralize any remaining acid gas
        rSNCR_Injection_Cmd := 0.0;
        IF NOT bEmergency_Stop AND NOT bStart_Sequence THEN
            iState := 0;
        END_IF;
END_CASE;

// Legal Compliance Monitoring (2 seconds delay for < 850C)
tonTempLowAlert(IN := (rFurnace_Temp < 850.0) AND (iState = 20), PT := T#2S);
bAlarm_Temp_Low := tonTempLowAlert.Q;

bAlarm_NOx_High := (rNOx_Emissions_PV > (rNOx_Setpoint * 1.2));

END_FUNCTION_BLOCK
```"""

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": iec_code}
    ]
}

os.makedirs("data/swarm_raw", exist_ok=True)
uid = uuid.uuid4().hex[:8]
with open(f"data/swarm_raw/agent_{uid}.json", "w", encoding="utf-8") as f:
    json.dump(record, f)
    
os.makedirs("data", exist_ok=True)
with open("data/synthetic_generation_v3_enterprise.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(record) + "\\n")
