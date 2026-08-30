import json
record = {
    "messages": [
        {
            "role": "user",
            "content": "You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.\nYour specific domain is: Green Hydrogen PEM Electrolyzer.\nTask: Invent a highly complex control scenario for this domain (e.g., Proton Exchange Membrane (PEM) cell voltage balancing, oxygen/hydrogen cross-permeation detection, and gas phase separator liquid levels).\nWrite a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."
        },
        {
            "role": "assistant",
            "content": """```iec-st
FUNCTION_BLOCK FB_PEM_Electrolyzer_MasterControl
TITLE = 'Green Hydrogen PEM Electrolyzer Master Control'
// -----------------------------------------------------------------------------
// This function block manages the critical operations of a Proton Exchange 
// Membrane (PEM) Electrolyzer. It encompasses cell voltage monitoring and 
// balancing, cross-permeation detection (H2 in O2, O2 in H2), thermal management,
// and gas phase separator liquid level control.
// -----------------------------------------------------------------------------

VAR_INPUT
    bEnable : BOOL; // System enable command
    bEmergencyStop : BOOL; // Emergency stop command, immediate shutdown
    rStackCurrent : REAL; // Operating current of the electrolyzer stack (Amps)
    arCellVoltages : ARRAY[1..100] OF REAL; // Individual cell voltages (V)
    rH2InO2_Concentration : REAL; // LEL measurement of H2 in O2 stream (%LEL)
    rO2InH2_Concentration : REAL; // LEL measurement of O2 in H2 stream (%LEL)
    rStackTemp : REAL; // Stack operating temperature (Celsius)
    rH2SeparatorLevel : REAL; // Liquid level in H2 separator (%)
    rO2SeparatorLevel : REAL; // Liquid level in O2 separator (%)
    rCoolingWaterTemp_In : REAL; // Inlet cooling water temperature (Celsius)
    rFeedWaterFlow : REAL; // Deionized feed water flow rate (L/min)
END_VAR

VAR_OUTPUT
    bSystemReady : BOOL; // System is ready to accept current
    bRunStatus : BOOL; // System is running
    bAlarm : BOOL; // General alarm active
    bCriticalFault : BOOL; // Critical fault, system tripped
    rCurrentSetpoint : REAL; // Command to DC power supply (Amps)
    rCoolingValvePos : REAL; // Command to cooling water control valve (0-100%)
    bH2DrainValve : BOOL; // Command to open H2 separator drain
    bO2DrainValve : BOOL; // Command to open O2 separator drain
    bN2PurgeValve : BOOL; // Command to open Nitrogen purge valve
    sStatusMessage : STRING[50]; // Textual status message
END_VAR

VAR
    i : INT;
    rMaxCellVoltage : REAL;
    rMinCellVoltage : REAL;
    rAvgCellVoltage : REAL;
    rVoltageSpread : REAL;
    
    // Timers
    tonStartDelay : TON;
    tonPurgeTimer : TON;
    tonH2Drain : TON;
    tonO2Drain : TON;
    
    // Internal States
    eState : (INIT, PURGING, READY, RAMPING, RUNNING, SHUTDOWN, FAULT);
    
    // Constants
    cMaxVoltageSpread : REAL := 0.15; // Max allowed V spread
    cCellOverVoltage : REAL := 2.45; // Max absolute cell V
    cCellUnderVoltage : REAL := 1.40; // Min absolute cell V
    cCrossPermeationAlarm : REAL := 2.0; // % LEL Alarm threshold
    cCrossPermeationTrip : REAL := 4.0; // % LEL Trip threshold
    cMaxTemp : REAL := 80.0; // Max stack temperature
    cTargetTemp : REAL := 65.0; // Optimal stack temperature
    cLevelHighDrain : REAL := 80.0; // % level to start drain
    cLevelLowStop : REAL := 20.0; // % level to stop drain
END_VAR

// -----------------------------------------------------------------------------
// MAIN LOGIC
// -----------------------------------------------------------------------------

// 1. Safety & Fault Interlocks
IF bEmergencyStop THEN
    bCriticalFault := TRUE;
    sStatusMessage := 'EMERGENCY STOP ACTIVATED';
    eState := FAULT;
END_IF;

// Cross-permeation monitoring
IF rH2InO2_Concentration >= cCrossPermeationTrip OR rO2InH2_Concentration >= cCrossPermeationTrip THEN
    bCriticalFault := TRUE;
    sStatusMessage := 'CROSS PERMEATION TRIP';
    eState := FAULT;
ELSIF rH2InO2_Concentration >= cCrossPermeationAlarm OR rO2InH2_Concentration >= cCrossPermeationAlarm THEN
    bAlarm := TRUE;
END_IF;

// Stack Temperature Monitoring
IF rStackTemp > cMaxTemp THEN
    bCriticalFault := TRUE;
    sStatusMessage := 'HIGH TEMPERATURE TRIP';
    eState := FAULT;
END_IF;

// Cell Voltage Analysis
rMaxCellVoltage := 0.0;
rMinCellVoltage := 10.0;
rAvgCellVoltage := 0.0;

FOR i := 1 TO 100 DO
    IF arCellVoltages[i] > rMaxCellVoltage THEN rMaxCellVoltage := arCellVoltages[i]; END_IF;
    IF arCellVoltages[i] < rMinCellVoltage THEN rMinCellVoltage := arCellVoltages[i]; END_IF;
    rAvgCellVoltage := rAvgCellVoltage + arCellVoltages[i];
END_FOR;
rAvgCellVoltage := rAvgCellVoltage / 100.0;
rVoltageSpread := rMaxCellVoltage - rMinCellVoltage;

IF rMaxCellVoltage > cCellOverVoltage OR rMinCellVoltage < cCellUnderVoltage THEN
    bCriticalFault := TRUE;
    sStatusMessage := 'CELL VOLTAGE OUT OF BOUNDS';
    eState := FAULT;
END_IF;

IF rVoltageSpread > cMaxVoltageSpread THEN
    bAlarm := TRUE;
    // Degrade performance to maintain safety
    IF rCurrentSetpoint > 100.0 THEN
        rCurrentSetpoint := rCurrentSetpoint - 10.0; // Derate
    END_IF;
END_IF;

// State Machine
CASE eState OF
    INIT:
        bSystemReady := FALSE;
        bRunStatus := FALSE;
        rCurrentSetpoint := 0.0;
        bN2PurgeValve := FALSE;
        IF bEnable AND NOT bCriticalFault THEN
            eState := PURGING;
            tonPurgeTimer(IN := FALSE);
        END_IF;
        
    PURGING:
        sStatusMessage := 'N2 PURGE IN PROGRESS';
        bN2PurgeValve := TRUE;
        tonPurgeTimer(IN := TRUE, PT := T#30S);
        IF tonPurgeTimer.Q THEN
            bN2PurgeValve := FALSE;
            eState := READY;
        END_IF;
        IF NOT bEnable THEN eState := SHUTDOWN; END_IF;
        
    READY:
        sStatusMessage := 'SYSTEM READY';
        bSystemReady := TRUE;
        IF rStackCurrent > 0.0 THEN
            eState := RAMPING;
        END_IF;
        IF NOT bEnable THEN eState := SHUTDOWN; END_IF;
        
    RAMPING:
        sStatusMessage := 'CURRENT RAMPING';
        bRunStatus := TRUE;
        rCurrentSetpoint := rCurrentSetpoint + 5.0; // Ramp rate
        IF rCurrentSetpoint >= rStackCurrent THEN
            rCurrentSetpoint := rStackCurrent;
            eState := RUNNING;
        END_IF;
        IF NOT bEnable THEN eState := SHUTDOWN; END_IF;
        
    RUNNING:
        sStatusMessage := 'NORMAL OPERATION';
        rCurrentSetpoint := rStackCurrent; // Track input request
        IF NOT bEnable THEN eState := SHUTDOWN; END_IF;
        
    SHUTDOWN:
        sStatusMessage := 'SYSTEM SHUTDOWN';
        bSystemReady := FALSE;
        bRunStatus := FALSE;
        rCurrentSetpoint := 0.0;
        bN2PurgeValve := TRUE; // Purge on shutdown
        tonStartDelay(IN := TRUE, PT := T#60S);
        IF tonStartDelay.Q THEN
            bN2PurgeValve := FALSE;
            eState := INIT;
            tonStartDelay(IN := FALSE);
        END_IF;
        
    FAULT:
        bSystemReady := FALSE;
        bRunStatus := FALSE;
        rCurrentSetpoint := 0.0;
        bN2PurgeValve := TRUE; // Emergency purge
        // Requires manual reset of bEmergencyStop and bEnable toggle
        IF NOT bEmergencyStop AND NOT bEnable THEN
            bCriticalFault := FALSE;
            bAlarm := FALSE;
            eState := INIT;
        END_IF;
END_CASE;

// Thermal Management (Simple P-Controller)
IF eState = RUNNING OR eState = RAMPING THEN
    rCoolingValvePos := (rStackTemp - cTargetTemp) * 5.0; 
    IF rCoolingValvePos > 100.0 THEN rCoolingValvePos := 100.0; END_IF;
    IF rCoolingValvePos < 0.0 THEN rCoolingValvePos := 0.0; END_IF;
ELSE
    rCoolingValvePos := 0.0;
END_IF;

// Gas Phase Separator Level Control
IF rH2SeparatorLevel > cLevelHighDrain THEN
    bH2DrainValve := TRUE;
ELSIF rH2SeparatorLevel < cLevelLowStop THEN
    bH2DrainValve := FALSE;
END_IF;

IF rO2SeparatorLevel > cLevelHighDrain THEN
    bO2DrainValve := TRUE;
ELSIF rO2SeparatorLevel < cLevelLowStop THEN
    bO2DrainValve := FALSE;
END_IF;

END_FUNCTION_BLOCK
```"""
        }
    ]
}
with open('data/synthetic_generation_v3_enterprise.jsonl', 'a', encoding='utf-8') as f:
    f.write(json.dumps(record) + "\n")
