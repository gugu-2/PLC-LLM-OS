import json
import uuid
import os

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: Carbon Nanotube (CNT) CVD Reactor.
Task: Invent a highly complex control scenario for this domain (e.g., Ethylene mass flow arrays, argon carrier gas purging limits, and inductive plasma heating zones).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."""

code = """```iec-st
FUNCTION_BLOCK CNT_CVD_Reactor_Control
VAR_INPUT
    bEnable                 : BOOL; // Enable the CVD process
    rTargetTempZone1        : REAL; // Target temperature for inductive plasma heating zone 1 (C)
    rTargetTempZone2        : REAL; // Target temperature for inductive plasma heating zone 2 (C)
    rEthyleneMassFlowSet    : REAL; // Target ethylene mass flow (sccm)
    rArgonCarrierFlowSet    : REAL; // Target argon carrier flow (sccm)
    rChamberPressureSet     : REAL; // Target chamber pressure (Torr)
    
    rCurrentTempZone1       : REAL; // Actual temperature zone 1
    rCurrentTempZone2       : REAL; // Actual temperature zone 2
    rCurrentEthyleneFlow    : REAL; // Actual ethylene flow
    rCurrentArgonFlow       : REAL; // Actual argon flow
    rCurrentChamberPressure : REAL; // Actual chamber pressure
    bPlasmaIgnited          : BOOL; // Plasma status sensor
    
    bEmergencyStop          : BOOL; // E-Stop
END_VAR

VAR_OUTPUT
    rHeaterOutputZone1      : REAL; // Control signal (0-100%) for Heater 1
    rHeaterOutputZone2      : REAL; // Control signal (0-100%) for Heater 2
    rEthyleneValveOut       : REAL; // Control signal for Ethylene MFC
    rArgonValveOut          : REAL; // Control signal for Argon MFC
    rVacuumPumpOut          : REAL; // Control signal for Vacuum Pump throttle
    bPlasmaIgniteCmd        : BOOL; // Command to ignite plasma generator
    
    iProcessState           : INT;  // Current state of the process
    bAlarmActive            : BOOL; // General alarm flag
    sAlarmMessage           : STRING(80); // Alarm description
END_VAR

VAR
    fbTempPID_Z1            : PID_Controller;
    fbTempPID_Z2            : PID_Controller;
    fbPressurePID           : PID_Controller;
    
    tStateTimer             : TON;
    tPurgeTimer             : TON;
    tGrowthTimer            : TON;
    
    bInitDone               : BOOL := FALSE;
    bPurgeComplete          : BOOL := FALSE;
    rTempTolerance          : REAL := 5.0;
    rPressureTolerance      : REAL := 0.5;
END_VAR

// Initialization
IF NOT bInitDone THEN
    fbTempPID_Z1.Kp := 2.5; fbTempPID_Z1.Ki := 0.1; fbTempPID_Z1.Kd := 0.05;
    fbTempPID_Z2.Kp := 2.5; fbTempPID_Z2.Ki := 0.1; fbTempPID_Z2.Kd := 0.05;
    fbPressurePID.Kp := 1.2; fbPressurePID.Ki := 0.05; fbPressurePID.Kd := 0.01;
    bInitDone := TRUE;
    iProcessState := 0;
END_IF

// Emergency Stop Logic
IF bEmergencyStop THEN
    rHeaterOutputZone1 := 0.0;
    rHeaterOutputZone2 := 0.0;
    rEthyleneValveOut := 0.0;
    rArgonValveOut := 100.0; // Max purge on E-Stop
    rVacuumPumpOut := 100.0; // Full vacuum
    bPlasmaIgniteCmd := FALSE;
    iProcessState := 99; // Error state
    bAlarmActive := TRUE;
    sAlarmMessage := 'EMERGENCY STOP ACTIVATED - SYSTEM PURGING';
    RETURN;
END_IF

// Process State Machine
CASE iProcessState OF
    0: // Idle
        rHeaterOutputZone1 := 0.0;
        rHeaterOutputZone2 := 0.0;
        rEthyleneValveOut := 0.0;
        rArgonValveOut := 0.0;
        rVacuumPumpOut := 0.0;
        bPlasmaIgniteCmd := FALSE;
        
        IF bEnable THEN
            iProcessState := 10;
            bAlarmActive := FALSE;
            sAlarmMessage := '';
        END_IF
        
    10: // Initial Vacuum and Argon Purge
        rVacuumPumpOut := 80.0; // Pull vacuum
        rArgonValveOut := 50.0; // Flow argon to purge
        
        tPurgeTimer(IN := TRUE, PT := T#5M);
        
        IF tPurgeTimer.Q THEN
            tPurgeTimer(IN := FALSE);
            iProcessState := 20;
        END_IF
        
    20: // Heating phase
        // Control Pressure
        fbPressurePID(SetPoint := rChamberPressureSet, ProcessValue := rCurrentChamberPressure);
        rVacuumPumpOut := fbPressurePID.Output;
        
        // Control Temperature
        fbTempPID_Z1(SetPoint := rTargetTempZone1, ProcessValue := rCurrentTempZone1);
        rHeaterOutputZone1 := fbTempPID_Z1.Output;
        
        fbTempPID_Z2(SetPoint := rTargetTempZone2, ProcessValue := rCurrentTempZone2);
        rHeaterOutputZone2 := fbTempPID_Z2.Output;
        
        IF (ABS(rTargetTempZone1 - rCurrentTempZone1) < rTempTolerance) AND
           (ABS(rTargetTempZone2 - rCurrentTempZone2) < rTempTolerance) THEN
           tStateTimer(IN := TRUE, PT := T#2M); // Wait for stabilization
           IF tStateTimer.Q THEN
               tStateTimer(IN := FALSE);
               iProcessState := 30;
           END_IF
        ELSE
           tStateTimer(IN := FALSE);
        END_IF
        
    30: // Plasma Ignition
        bPlasmaIgniteCmd := TRUE;
        rArgonValveOut := rArgonCarrierFlowSet; // Set operating argon flow
        
        tStateTimer(IN := TRUE, PT := T#10S);
        IF tStateTimer.Q THEN
            IF bPlasmaIgnited THEN
                tStateTimer(IN := FALSE);
                iProcessState := 40; // Proceed to growth
            ELSE
                // Failed to ignite
                iProcessState := 99;
                bAlarmActive := TRUE;
                sAlarmMessage := 'PLASMA IGNITION FAILURE';
            END_IF
        END_IF
        
    40: // CNT Growth (Ethylene introduction)
        rEthyleneValveOut := rEthyleneMassFlowSet; // Introduce carbon source
        
        tGrowthTimer(IN := TRUE, PT := T#30M); // 30 min growth phase
        
        // Maintain Temp and Pressure
        fbPressurePID(SetPoint := rChamberPressureSet, ProcessValue := rCurrentChamberPressure);
        rVacuumPumpOut := fbPressurePID.Output;
        fbTempPID_Z1(SetPoint := rTargetTempZone1, ProcessValue := rCurrentTempZone1);
        rHeaterOutputZone1 := fbTempPID_Z1.Output;
        fbTempPID_Z2(SetPoint := rTargetTempZone2, ProcessValue := rCurrentTempZone2);
        rHeaterOutputZone2 := fbTempPID_Z2.Output;
        
        IF tGrowthTimer.Q THEN
            tGrowthTimer(IN := FALSE);
            iProcessState := 50; // Cool down
        END_IF
        
    50: // Cooldown and Final Purge
        bPlasmaIgniteCmd := FALSE;
        rEthyleneValveOut := 0.0;
        rArgonValveOut := 50.0; // Maintain purge
        rHeaterOutputZone1 := 0.0;
        rHeaterOutputZone2 := 0.0;
        
        IF (rCurrentTempZone1 < 50.0) AND (rCurrentTempZone2 < 50.0) THEN
            iProcessState := 60; // Complete
        END_IF
        
    60: // Complete
        rArgonValveOut := 0.0;
        rVacuumPumpOut := 0.0;
        IF NOT bEnable THEN
            iProcessState := 0; // Reset
        END_IF
        
    99: // Error Handling
        rHeaterOutputZone1 := 0.0;
        rHeaterOutputZone2 := 0.0;
        rEthyleneValveOut := 0.0;
        bPlasmaIgniteCmd := FALSE;
        
        // Try to maintain safe state
        rArgonValveOut := 100.0; // High argon flow to clear explosive gases
        rVacuumPumpOut := 100.0; // Evacuate chamber
        
        IF NOT bEnable THEN
            // Acknowledge alarm
            bAlarmActive := FALSE;
            sAlarmMessage := '';
            iProcessState := 0;
        END_IF
        
END_CASE
END_FUNCTION_BLOCK
```"""

record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
    json.dump(record, f, indent=2)

with open("data/synthetic_generation_v3_enterprise.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(record) + "\\n")
