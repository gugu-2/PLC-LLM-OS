import json
import uuid
import os

code = """```iec-st
FUNCTION_BLOCK FB_DrawTower_MasterControl
VAR_INPUT
    bEnable : BOOL; // System Enable
    rTargetDrawSpeed_mps : REAL; // Target drawing speed (m/s)
    rPreformDiameter_mm : REAL; // Initial preform diameter
    rTargetFiberDiameter_um : REAL; // Target fiber diameter (typically 125 um)
    rFurnaceTemp_PV : REAL; // Actual furnace temperature (deg C)
    rFurnaceTemp_SP : REAL; // Furnace temperature setpoint (deg C)
    rTension_PV : REAL; // Measured draw tension (g)
    rCoatingDiameter_PV : REAL; // Measured coated fiber diameter (um)
    rCoatingConcentricity_PV : REAL; // Measured concentricity offset (um)
END_VAR

VAR_OUTPUT
    rPreformFeedRate_mm_min : REAL; // Calculated preform downfeed speed
    rCapstanSpeed_mps : REAL; // Primary capstan speed control
    rUVPower_pct : REAL; // UV curing lamp power (%)
    rCoatingPressure_kPa : REAL; // Acrylate coating pressurization
    rTractorSpeed_mps : REAL; // Secondary capstan/tractor speed
    bSystemReady : BOOL;
    bAlarmActive : BOOL;
    iErrorCode : INT;
END_VAR

VAR
    // Internal States
    iState : INT := 0; 
    // State constants
    IDLE : INT := 0;
    RAMP_UP : INT := 1;
    STEADY_STATE : INT := 2;
    RAMP_DOWN : INT := 3;
    FAULT : INT := 99;
    
    // PID Controllers for Tension and Diameter
    PID_Tension : FB_PID_Advanced;
    PID_Diameter : FB_PID_Advanced;
    PID_Coating : FB_PID_Advanced;
    
    // Internal Variables
    rCurrentSpeed_mps : REAL := 0.0;
    rMassBalance_Feed : REAL;
    rDrawRatio : REAL;
    
    // Timers
    tStartupDelay : TON;
    tFaultTimer : TON;
    
    // Limits
    MAX_SPEED : REAL := 50.0; // 50 m/s max draw speed
    MIN_TENSION : REAL := 50.0; // 50 grams
    MAX_TENSION : REAL := 250.0; // 250 grams
END_VAR

// Mass Balance Calculation
rDrawRatio := (rTargetFiberDiameter_um * 0.001) / rPreformDiameter_mm;
rMassBalance_Feed := (rCurrentSpeed_mps * 60000.0) * (rDrawRatio * rDrawRatio);

CASE iState OF
    IDLE:
        bSystemReady := TRUE;
        rCurrentSpeed_mps := 0.0;
        rPreformFeedRate_mm_min := 0.0;
        rCapstanSpeed_mps := 0.0;
        rUVPower_pct := 0.0;
        bAlarmActive := FALSE;
        iErrorCode := 0;
        
        IF bEnable AND (rFurnaceTemp_PV >= rFurnaceTemp_SP * 0.99) THEN
            iState := RAMP_UP;
            bSystemReady := FALSE;
        END_IF
        
    RAMP_UP:
        rCurrentSpeed_mps := rCurrentSpeed_mps + 0.1;
        IF rCurrentSpeed_mps >= rTargetDrawSpeed_mps THEN
            rCurrentSpeed_mps := rTargetDrawSpeed_mps;
            iState := STEADY_STATE;
        END_IF
        
        IF (rTension_PV > MAX_TENSION) THEN
            iState := FAULT;
            iErrorCode := 101;
        END_IF
        
    STEADY_STATE:
        PID_Diameter(
            bEnable := TRUE,
            rSetpoint := rTargetFiberDiameter_um,
            rProcessValue := rTargetFiberDiameter_um,
            rKp := 0.5, rKi := 0.1, rKd := 0.01,
            rOutput => rCapstanSpeed_mps
        );
        rCapstanSpeed_mps := rCurrentSpeed_mps + PID_Diameter.rOutput;
        
        PID_Tension(
            bEnable := TRUE,
            rSetpoint := 120.0,
            rProcessValue := rTension_PV,
            rKp := 0.2, rKi := 0.05, rKd := 0.0,
            rOutput => rTractorSpeed_mps
        );
        rTractorSpeed_mps := rCapstanSpeed_mps + PID_Tension.rOutput;
        
        rUVPower_pct := (rCurrentSpeed_mps / MAX_SPEED) * 100.0;
        
        PID_Coating(
            bEnable := TRUE,
            rSetpoint := 250.0,
            rProcessValue := rCoatingDiameter_PV,
            rKp := 1.2, rKi := 0.3, rKd := 0.05,
            rOutput => rCoatingPressure_kPa
        );
        
        IF NOT bEnable THEN
            iState := RAMP_DOWN;
        ELSIF rTension_PV < MIN_TENSION OR rTension_PV > MAX_TENSION THEN
            iState := FAULT;
            iErrorCode := 102;
        END_IF
        
    RAMP_DOWN:
        rCurrentSpeed_mps := rCurrentSpeed_mps - 0.2;
        IF rCurrentSpeed_mps <= 0.0 THEN
            rCurrentSpeed_mps := 0.0;
            iState := IDLE;
        END_IF
        
    FAULT:
        bAlarmActive := TRUE;
        rCurrentSpeed_mps := 0.0;
        rPreformFeedRate_mm_min := 0.0;
        rCapstanSpeed_mps := 0.0;
        rTractorSpeed_mps := 0.0;
        rUVPower_pct := 0.0;
        rCoatingPressure_kPa := 0.0;
        
        IF NOT bEnable THEN
            iState := IDLE;
        END_IF
END_CASE

rPreformFeedRate_mm_min := rMassBalance_Feed;
END_FUNCTION_BLOCK

FUNCTION_BLOCK FB_PID_Advanced
VAR_INPUT
    bEnable : BOOL;
    rSetpoint : REAL;
    rProcessValue : REAL;
    rKp : REAL;
    rKi : REAL;
    rKd : REAL;
END_VAR
VAR_OUTPUT
    rOutput : REAL;
END_VAR
VAR
    rError : REAL;
    rLastError : REAL;
    rIntegral : REAL;
    rDerivative : REAL;
END_VAR
IF bEnable THEN
    rError := rSetpoint - rProcessValue;
    rIntegral := rIntegral + (rError * 0.01);
    rDerivative := (rError - rLastError) / 0.01;
    rOutput := (rKp * rError) + (rKi * rIntegral) + (rKd * rDerivative);
    rLastError := rError;
ELSE
    rOutput := 0.0;
    rIntegral := 0.0;
    rLastError := 0.0;
END_IF
END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
record = {
    "messages": [
        {"role": "user", "content": "You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.\nYour specific domain is: Optical Fiber Draw Tower.\nTask: Invent a highly complex control scenario for this domain (e.g., glass preform feed indexing, UV-cured acrylate coating concentricity, and dual capstan tension).\nWrite a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."},
        {"role": "assistant", "content": code}
    ]
}
with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
    json.dump(record, f)

# Also append to the data/synthetic_generation_v3_enterprise.jsonl as per system prompt
with open("data/synthetic_generation_v3_enterprise.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(record) + "\\n")
