import json, os, uuid

os.makedirs('data/swarm_raw', exist_ok=True)
prompt = '''You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: Continuous Rubber Vulcanization (UHF).
Task: Invent a highly complex control scenario for this domain (e.g., microwave/hot air curing profile logic, caterpillar haul-off tensioning, and extrudate geometry measurement).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O.'''

code = """```iec-st
FUNCTION_BLOCK FB_UHF_VulcanizationControl
VAR_INPUT
    bEnable : BOOL; // System enable
    rLineSpeedCmd : REAL; // Line speed command [m/min]
    rTargetTension : REAL; // Target tension for haul-off [N]
    rActualTension : REAL; // Measured tension from load cell [N]
    rUHFPowerSet : REAL; // Microwave power setpoint [kW]
    rHotAirTempSet : REAL; // Hot air tunnel temperature setpoint [degC]
    rHotAirTempAct : REAL; // Actual hot air temperature [degC]
    rProfileThicknessAct : REAL; // Measured profile thickness [mm]
    rProfileThicknessTarget : REAL; // Target profile thickness [mm]
    rUHFZone1Temp : REAL; // Measured temperature zone 1 [degC]
    rUHFZone2Temp : REAL; // Measured temperature zone 2 [degC]
    bEStop : BOOL; // Emergency stop
    rPID_Kp : REAL := 2.5;
    rPID_Ki : REAL := 0.5;
    rPID_Kd : REAL := 0.1;
END_VAR

VAR_OUTPUT
    bSystemReady : BOOL;
    rExtruderSpeedRef : REAL; // Extruder speed reference [rpm]
    rCaterpillarSpeedRef : REAL; // Haul-off speed reference [m/min]
    rUHFPowerOut : REAL; // Commanded UHF power [kW]
    rHeaterOutput : REAL; // Commanded heater output [0-100%]
    bAlarmActive : BOOL;
    sAlarmMessage : STRING(50);
END_VAR

VAR
    // Internal state variables
    eState : (INIT, HEATING, RUNNING, FAULT, STOPPING);
    rTensionError : REAL;
    rTensionIntegral : REAL;
    rTensionDerivative : REAL;
    rTensionPrevError : REAL;
    
    rTempError : REAL;
    rTempIntegral : REAL;
    
    rThicknessError : REAL;
    rThicknessIntegral : REAL;
    
    tDelayTimer : TON;
    tUHFCooldown : TOF;
    bInitialize : BOOL := TRUE;
    
    // Limits
    MAX_TENSION_INT : REAL := 50.0;
    MAX_HEATER_OUT : REAL := 100.0;
    MAX_SPEED : REAL := 30.0;
    
    // Cycle time
    rDt : REAL := 0.01; // 10ms cycle
END_VAR

// Implementation
IF bEStop THEN
    eState := FAULT;
    sAlarmMessage := 'Emergency Stop Active';
    rExtruderSpeedRef := 0.0;
    rCaterpillarSpeedRef := 0.0;
    rUHFPowerOut := 0.0;
    rHeaterOutput := 0.0;
    bSystemReady := FALSE;
    bAlarmActive := TRUE;
    RETURN;
END_IF;

CASE eState OF
    INIT:
        bSystemReady := FALSE;
        bAlarmActive := FALSE;
        sAlarmMessage := 'Initializing System';
        rExtruderSpeedRef := 0.0;
        rCaterpillarSpeedRef := 0.0;
        rUHFPowerOut := 0.0;
        rHeaterOutput := 0.0;
        
        // Reset PIDs
        rTensionIntegral := 0.0;
        rTempIntegral := 0.0;
        rThicknessIntegral := 0.0;
        
        IF bEnable THEN
            eState := HEATING;
        END_IF;
        
    HEATING:
        sAlarmMessage := 'Heating Tunnels';
        
        // Temperature Control (PI)
        rTempError := rHotAirTempSet - rHotAirTempAct;
        rTempIntegral := rTempIntegral + (rTempError * rDt);
        IF rTempIntegral > 100.0 THEN rTempIntegral := 100.0; END_IF;
        IF rTempIntegral < 0.0 THEN rTempIntegral := 0.0; END_IF;
        
        rHeaterOutput := (2.0 * rTempError) + (0.05 * rTempIntegral);
        
        IF rHeaterOutput > MAX_HEATER_OUT THEN
            rHeaterOutput := MAX_HEATER_OUT;
        ELSIF rHeaterOutput < 0.0 THEN
            rHeaterOutput := 0.0;
        END_IF;
        
        // Check if heated
        IF ABS(rTempError) < 5.0 THEN
            bSystemReady := TRUE;
            eState := RUNNING;
        END_IF;
        
        IF NOT bEnable THEN
            eState := STOPPING;
        END_IF;

    RUNNING:
        sAlarmMessage := 'System Running';
        
        // Maintain Temperature
        rTempError := rHotAirTempSet - rHotAirTempAct;
        rTempIntegral := rTempIntegral + (rTempError * rDt);
        rHeaterOutput := (2.0 * rTempError) + (0.05 * rTempIntegral);
        IF rHeaterOutput > MAX_HEATER_OUT THEN rHeaterOutput := MAX_HEATER_OUT; END_IF;
        IF rHeaterOutput < 0.0 THEN rHeaterOutput := 0.0; END_IF;
        
        // UHF Power Profile Control
        IF rUHFZone1Temp > 250.0 OR rUHFZone2Temp > 250.0 THEN
            bAlarmActive := TRUE;
            sAlarmMessage := 'UHF Overtemp Fault';
            eState := FAULT;
        ELSE
            rUHFPowerOut := rUHFPowerSet;
        END_IF;
        
        // Tension Control (PID for Caterpillar Speed)
        rTensionError := rTargetTension - rActualTension;
        rTensionIntegral := rTensionIntegral + (rTensionError * rDt);
        IF rTensionIntegral > MAX_TENSION_INT THEN rTensionIntegral := MAX_TENSION_INT; END_IF;
        IF rTensionIntegral < -MAX_TENSION_INT THEN rTensionIntegral := -MAX_TENSION_INT; END_IF;
        rTensionDerivative := (rTensionError - rTensionPrevError) / rDt;
        rTensionPrevError := rTensionError;
        
        // Base speed plus tension trim
        rCaterpillarSpeedRef := rLineSpeedCmd + (rPID_Kp * rTensionError) + (rPID_Ki * rTensionIntegral) + (rPID_Kd * rTensionDerivative);
        IF rCaterpillarSpeedRef > MAX_SPEED THEN rCaterpillarSpeedRef := MAX_SPEED; END_IF;
        IF rCaterpillarSpeedRef < 0.0 THEN rCaterpillarSpeedRef := 0.0; END_IF;
        
        // Geometry Control (Thickness) - Adjusts Extruder Speed
        rThicknessError := rProfileThicknessTarget - rProfileThicknessAct;
        rThicknessIntegral := rThicknessIntegral + (rThicknessError * rDt);
        
        // Inverse relationship: if thickness is too low, increase extruder speed
        rExtruderSpeedRef := (rLineSpeedCmd * 5.0) + (10.0 * rThicknessError) + (2.0 * rThicknessIntegral);
        IF rExtruderSpeedRef > 150.0 THEN rExtruderSpeedRef := 150.0; END_IF;
        IF rExtruderSpeedRef < 0.0 THEN rExtruderSpeedRef := 0.0; END_IF;
        
        IF NOT bEnable THEN
            eState := STOPPING;
        END_IF;
        
    STOPPING:
        sAlarmMessage := 'System Stopping';
        bSystemReady := FALSE;
        rExtruderSpeedRef := 0.0;
        rCaterpillarSpeedRef := 0.0;
        rUHFPowerOut := 0.0;
        rHeaterOutput := 0.0;
        eState := INIT;
        
    FAULT:
        bSystemReady := FALSE;
        rExtruderSpeedRef := 0.0;
        rCaterpillarSpeedRef := 0.0;
        rUHFPowerOut := 0.0;
        rHeaterOutput := 0.0;
        IF NOT bEStop AND NOT bAlarmActive THEN
            eState := INIT;
        END_IF;
END_CASE;
END_FUNCTION_BLOCK
```"""

record = {'messages': [{'role': 'user', 'content': prompt}, {'role': 'assistant', 'content': code}]}
with open(f'data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json', 'w', encoding='utf-8') as f:
    json.dump(record, f)
print('Successfully saved.')
