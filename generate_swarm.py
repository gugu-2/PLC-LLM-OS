import json
import uuid
import os

code = """```iec-st
FUNCTION_BLOCK FB_MDF_ContinuousPressControl
TITLE = 'MDF Continuous Wood Press Controller'
VERSION : '1.0'

VAR_INPUT
    bEnable : BOOL; // Enable press operation
    bEmergencyStop : BOOL; // E-stop active low
    
    // Line speed and position
    rLineSpeedCmd : REAL; // Commanded line speed [m/s]
    rActualLineSpeed : REAL; // Actual measured speed [m/s]
    rMatPosition : LREAL; // Position of mat [m]
    
    // Dielectric High-Frequency Pre-Heating
    rMatMoistureContent : REAL; // Input moisture %
    rTargetPreHeatTemp : REAL; // [degC]
    rActualMatTemp : REAL; // [degC]
    rHFGeneratorPowerMax : REAL; // Max power allowed [kW]
    
    // Hydraulic Platen Profiling (3 zones for simplicity)
    rTargetThickness : ARRAY[1..3] OF REAL; // [mm]
    rActualThickness : ARRAY[1..3] OF REAL; // [mm]
    rPlatenPressureMax : REAL; // [bar]
    
    // Resin Curing (Thermal oil heating)
    rTargetPlatenTemp : ARRAY[1..3] OF REAL; // [degC]
    rActualPlatenTemp : ARRAY[1..3] OF REAL; // [degC]
END_VAR

VAR_OUTPUT
    bPressReady : BOOL;
    bPressFault : BOOL;
    wFaultCode : WORD;
    
    // HF Generator commands
    bEnableHFGen : BOOL;
    rHFGenPowerSetpoint : REAL; // [kW]
    
    // Hydraulic Cylinders (Position/Pressure control)
    rHydraulicValveCmd : ARRAY[1..3] OF REAL; // -100.0 to 100.0 %
    rActualPressure : ARRAY[1..3] OF REAL; // [bar]
    
    // Thermal Oil Valves
    rThermalOilValveCmd : ARRAY[1..3] OF REAL; // 0.0 to 100.0 %
END_VAR

VAR
    // Internal state
    eState : INT := 0; // 0:INIT, 1:IDLE, 2:RAMP_UP, 3:RUNNING, 4:SHUTDOWN, 5:FAULT
    
    // PID controllers for thickness (conceptual)
    rKp_Thick : REAL := 2.5;
    rTi_Thick : REAL := 1.2;
    rTd_Thick : REAL := 0.05;
    
    // Feedforward for HF heating
    rPowerFeedForward : REAL;
    
    // Timers
    i : INT;
END_VAR

// Implementation
IF NOT bEmergencyStop THEN
    eState := 5; // FAULT
    wFaultCode := 16#FFFF; // E-Stop
    bPressFault := TRUE;
    bEnableHFGen := FALSE;
    rHFGenPowerSetpoint := 0.0;
    FOR i := 1 TO 3 DO
        rHydraulicValveCmd[i] := 0.0;
        rThermalOilValveCmd[i] := 0.0;
    END_FOR;
    RETURN;
END_IF;

CASE eState OF
    0: // INIT
        bPressReady := FALSE;
        bPressFault := FALSE;
        wFaultCode := 16#0000;
        eState := 1; // IDLE
        
    1: // IDLE
        bPressReady := TRUE;
        IF bEnable THEN
            eState := 2; // RAMP_UP
        END_IF;
        
    2: // RAMP_UP
        // Engage hydraulics slowly
        bEnableHFGen := TRUE;
        IF rActualLineSpeed > (rLineSpeedCmd * 0.9) THEN
            eState := 3; // RUNNING
        END_IF;
        
    3: // RUNNING
        // HF Pre-heating calculation (Feedforward + simple P correction)
        rPowerFeedForward := (rTargetPreHeatTemp - rActualMatTemp) * rLineSpeedCmd * rMatMoistureContent * 0.5;
        IF rPowerFeedForward < 0.0 THEN
            rHFGenPowerSetpoint := 0.0;
        ELSIF rPowerFeedForward > rHFGeneratorPowerMax THEN
            rHFGenPowerSetpoint := rHFGeneratorPowerMax;
        ELSE
            rHFGenPowerSetpoint := rPowerFeedForward;
        END_IF;
        
        // Hydraulic Platen Profiling (Thickness control P-only for brevity)
        FOR i := 1 TO 3 DO
            rHydraulicValveCmd[i] := (rTargetThickness[i] - rActualThickness[i]) * rKp_Thick;
            // Limit output
            IF rHydraulicValveCmd[i] > 100.0 THEN rHydraulicValveCmd[i] := 100.0; END_IF;
            IF rHydraulicValveCmd[i] < -100.0 THEN rHydraulicValveCmd[i] := -100.0; END_IF;
        END_FOR;
        
        // Resin Curing (Thermal Oil Temperature Control)
        FOR i := 1 TO 3 DO
            rThermalOilValveCmd[i] := (rTargetPlatenTemp[i] - rActualPlatenTemp[i]) * 1.5;
            IF rThermalOilValveCmd[i] > 100.0 THEN rThermalOilValveCmd[i] := 100.0; END_IF;
            IF rThermalOilValveCmd[i] < 0.0 THEN rThermalOilValveCmd[i] := 0.0; END_IF;
        END_FOR;
        
        IF NOT bEnable THEN
            eState := 4; // SHUTDOWN
        END_IF;
        
    4: // SHUTDOWN
        bEnableHFGen := FALSE;
        rHFGenPowerSetpoint := 0.0;
        FOR i := 1 TO 3 DO
            rHydraulicValveCmd[i] := 0.0;
            rThermalOilValveCmd[i] := 0.0;
        END_FOR;
        IF rActualLineSpeed < 0.01 THEN
            eState := 1; // IDLE
        END_IF;
        
    5: // FAULT
        bPressReady := FALSE;
        // Require manual reset outside this block
END_CASE;
END_FUNCTION_BLOCK
```"""

prompt = "Invent a highly complex control scenario for MDF Continuous Wood Press. Write a deterministic Structured Text (ST) FUNCTION_BLOCK."

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": code}
    ]
}

os.makedirs("data", exist_ok=True)
with open("data/synthetic_generation_v3_enterprise.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(record) + "\n")
print("Appended to jsonl")
