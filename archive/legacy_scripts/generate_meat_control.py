import json, uuid, os

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: High-Volume Commercial Meat Processing.
Task: Invent a highly complex control scenario for this domain (e.g., spiral freezer blast chilling zones, brine injection pressure curves, and automated packaging vacuum sealing).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O.
"""

code = """```iec-st
FUNCTION_BLOCK FB_MeatProcessing_MasterControl
TITLE = 'High-Volume Commercial Meat Processing Control'
// Controls brine injection, spiral blast freezing, and vacuum packaging

VAR_INPUT
    bStartProcess : BOOL;
    bEmergencyStop : BOOL;
    rActualBrinePressure : REAL; // bar
    rTargetBrinePressure : REAL; // bar
    rCoreMeatTemp : REAL; // Celsius
    rSpiralFreezerTempZone1 : REAL;
    rSpiralFreezerTempZone2 : REAL;
    bVacuumSealReady : BOOL;
    rActualVacuumLevel : REAL; // mbar
END_VAR

VAR_OUTPUT
    bBrinePumpActive : BOOL;
    rBrinePumpSpeed : REAL; // 0-100%
    bSpiralConveyorRun : BOOL;
    rSpiralConveyorSpeed : REAL; // m/min
    bBlastChillerZone1Active : BOOL;
    bBlastChillerZone2Active : BOOL;
    bVacuumPumpActive : BOOL;
    bSealBarActive : BOOL;
    iCurrentState : INT;
    bAlarmActive : BOOL;
    sAlarmMessage : STRING[50];
END_VAR

VAR
    TmrBrineInjection : TON;
    TmrFreezerDwell : TON;
    TmrVacuumHold : TON;
    TmrSealTime : TON;
    rBrineError : REAL;
    rBrineKp : REAL := 2.5;
    rBrineKi : REAL := 0.5;
    rBrineIntegral : REAL;
    iState : INT := 0;
END_VAR

// State Machine Constants
// 0: IDLE
// 10: BRINE_INJECTION
// 20: SPIRAL_FREEZING
// 30: VACUUM_PACKAGING
// 99: ERROR

// Main Logic
IF bEmergencyStop THEN
    bBrinePumpActive := FALSE;
    bSpiralConveyorRun := FALSE;
    bVacuumPumpActive := FALSE;
    bSealBarActive := FALSE;
    bBlastChillerZone1Active := FALSE;
    bBlastChillerZone2Active := FALSE;
    iState := 99;
    bAlarmActive := TRUE;
    sAlarmMessage := 'EMERGENCY STOP ACTIVATED';
END_IF;

CASE iState OF
    0: // IDLE
        bBrinePumpActive := FALSE;
        bSpiralConveyorRun := FALSE;
        IF bStartProcess AND NOT bEmergencyStop THEN
            iState := 10;
            rBrineIntegral := 0.0;
        END_IF;
        
    10: // BRINE_INJECTION
        // PI Control for Brine Injection Pressure
        rBrineError := rTargetBrinePressure - rActualBrinePressure;
        rBrineIntegral := rBrineIntegral + (rBrineError * 0.1); // Assuming 100ms cycle
        rBrinePumpSpeed := (rBrineKp * rBrineError) + (rBrineKi * rBrineIntegral);
        
        IF rBrinePumpSpeed > 100.0 THEN
            rBrinePumpSpeed := 100.0;
        ELSIF rBrinePumpSpeed < 0.0 THEN
            rBrinePumpSpeed := 0.0;
        END_IF;
        
        bBrinePumpActive := rBrinePumpSpeed > 5.0;
        
        TmrBrineInjection(IN := bBrinePumpActive, PT := T#15S);
        IF TmrBrineInjection.Q THEN
            bBrinePumpActive := FALSE;
            rBrinePumpSpeed := 0.0;
            iState := 20;
        END_IF;
        
    20: // SPIRAL_FREEZING
        bSpiralConveyorRun := TRUE;
        bBlastChillerZone1Active := rSpiralFreezerTempZone1 > -35.0;
        bBlastChillerZone2Active := rSpiralFreezerTempZone2 > -40.0;
        
        // Adjust conveyor speed based on core temp to ensure full freezing
        IF rCoreMeatTemp > 5.0 THEN
            rSpiralConveyorSpeed := 2.5; // Slow down to freeze more
        ELSE
            rSpiralConveyorSpeed := 5.0; // Normal speed
        END_IF;
        
        // Move to packaging when core temp is reached
        IF rCoreMeatTemp <= -18.0 THEN
            bSpiralConveyorRun := FALSE;
            bBlastChillerZone1Active := FALSE;
            bBlastChillerZone2Active := FALSE;
            iState := 30;
        END_IF;
        
    30: // VACUUM_PACKAGING
        IF bVacuumSealReady THEN
            bVacuumPumpActive := TRUE;
            // Target vacuum level < 10 mbar
            IF rActualVacuumLevel < 10.0 THEN
                TmrVacuumHold(IN := TRUE, PT := T#2S);
                IF TmrVacuumHold.Q THEN
                    bVacuumPumpActive := FALSE;
                    bSealBarActive := TRUE;
                    TmrSealTime(IN := bSealBarActive, PT := T#1500MS);
                    IF TmrSealTime.Q THEN
                        bSealBarActive := FALSE;
                        TmrVacuumHold(IN := FALSE, PT := T#0S);
                        TmrSealTime(IN := FALSE, PT := T#0S);
                        iState := 0; // Return to idle for next batch
                    END_IF;
                END_IF;
            END_IF;
        END_IF;
        
    99: // ERROR
        IF NOT bEmergencyStop THEN
            bAlarmActive := FALSE;
            sAlarmMessage := '';
            iState := 0;
        END_IF;
        
END_CASE;

iCurrentState := iState;

END_FUNCTION_BLOCK
```"""

record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
file_path = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(file_path, "w", encoding="utf-8") as f:
    json.dump(record, f, indent=4)
print(f"Saved to {file_path}")
