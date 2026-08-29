import json
import uuid
import os

prompt = "You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.\nYour specific domain is: Battery Cathode Material Calcination Kiln.\nTask: Invent a highly complex control scenario for this domain (e.g., rotary kiln longitudinal thermal gradients, sagger tray servo indexing, and precise oxygen enrichment cascades).\nWrite a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."

st_code = """FUNCTION_BLOCK FB_Cathode_Calcination_Kiln
TITLE = 'Battery Cathode Material Calcination Kiln Control'
// Highly complex control for a rotary kiln processing battery cathode materials.
// Features: Longitudinal thermal gradients, sagger tray servo indexing, and precise O2 cascade.

VAR_INPUT
    bEnable : BOOL; // Enable Kiln Operation
    rTempSetpoint_Z1 : REAL; // Zone 1 Temperature Setpoint (C)
    rTempSetpoint_Z2 : REAL; // Zone 2 Temperature Setpoint (C)
    rTempSetpoint_Z3 : REAL; // Zone 3 Temperature Setpoint (C)
    rTempSetpoint_Z4 : REAL; // Zone 4 Temperature Setpoint (C)
    rActualTemp_Z1 : REAL; // Actual Temp Zone 1
    rActualTemp_Z2 : REAL; // Actual Temp Zone 2
    rActualTemp_Z3 : REAL; // Actual Temp Zone 3
    rActualTemp_Z4 : REAL; // Actual Temp Zone 4
    rO2_Setpoint : REAL; // Oxygen concentration setpoint (%)
    rActual_O2 : REAL; // Actual Oxygen concentration
    bSaggerIndexReq : BOOL; // Request to index the sagger tray
    bSaggerAtPos : BOOL; // Sagger tray is at the indexing position
    rKilnRotationSpeedReq : REAL; // Required Kiln Rotation Speed (RPM)
END_VAR

VAR_OUTPUT
    rHeaterCmd_Z1 : REAL; // 0-100% Heater Command Zone 1
    rHeaterCmd_Z2 : REAL; // 0-100% Heater Command Zone 2
    rHeaterCmd_Z3 : REAL; // 0-100% Heater Command Zone 3
    rHeaterCmd_Z4 : REAL; // 0-100% Heater Command Zone 4
    rO2_ValveCmd : REAL; // 0-100% O2 Enrichment Valve Command
    bSaggerServoIndex : BOOL; // Command to index sagger tray servo
    rKilnDriveCmd : REAL; // 0-100% Kiln Drive Command
    bSystemReady : BOOL; // System is at temperature and stable
    bAlarm : BOOL; // General Alarm flag
    iErrorCode : INT; // Error Code for diagnostics
END_VAR

VAR
    // PID Controllers for Temperature Zones
    PID_Z1 : FB_PID;
    PID_Z2 : FB_PID;
    PID_Z3 : FB_PID;
    PID_Z4 : FB_PID;
    
    // PID Controller for O2 Cascade
    PID_O2 : FB_PID;
    
    // Timers
    TMR_SaggerDelay : TON;
    TMR_TempStabilization : TON;
    
    // Internal state variables
    bGradientsOK : BOOL;
    rTempDev_Z1 : REAL;
    rTempDev_Z2 : REAL;
    rTempDev_Z3 : REAL;
    rTempDev_Z4 : REAL;
    
    // Constants
    rMaxTempDev : REAL := 5.0; // Max allowable temperature deviation
END_VAR

// --- IMPLEMENTATION ---
IF NOT bEnable THEN
    rHeaterCmd_Z1 := 0.0;
    rHeaterCmd_Z2 := 0.0;
    rHeaterCmd_Z3 := 0.0;
    rHeaterCmd_Z4 := 0.0;
    rO2_ValveCmd := 0.0;
    bSaggerServoIndex := FALSE;
    rKilnDriveCmd := 0.0;
    bSystemReady := FALSE;
    bAlarm := FALSE;
    iErrorCode := 0;
    RETURN;
END_IF;

// Calculate Temperature Deviations
rTempDev_Z1 := ABS(rTempSetpoint_Z1 - rActualTemp_Z1);
rTempDev_Z2 := ABS(rTempSetpoint_Z2 - rActualTemp_Z2);
rTempDev_Z3 := ABS(rTempSetpoint_Z3 - rActualTemp_Z3);
rTempDev_Z4 := ABS(rTempSetpoint_Z4 - rActualTemp_Z4);

// Evaluate Longitudinal Thermal Gradients
bGradientsOK := (rTempDev_Z1 < rMaxTempDev) AND 
                (rTempDev_Z2 < rMaxTempDev) AND 
                (rTempDev_Z3 < rMaxTempDev) AND 
                (rTempDev_Z4 < rMaxTempDev);

// Stabilization Timer
TMR_TempStabilization(IN := bGradientsOK, PT := T#5M);
bSystemReady := TMR_TempStabilization.Q;

// Temperature Control (PID execution)
PID_Z1(bEnable := TRUE, rSetpoint := rTempSetpoint_Z1, rProcessValue := rActualTemp_Z1, rOutput => rHeaterCmd_Z1);
PID_Z2(bEnable := TRUE, rSetpoint := rTempSetpoint_Z2, rProcessValue := rActualTemp_Z2, rOutput => rHeaterCmd_Z2);
PID_Z3(bEnable := TRUE, rSetpoint := rTempSetpoint_Z3, rProcessValue := rActualTemp_Z3, rOutput => rHeaterCmd_Z3);
PID_Z4(bEnable := TRUE, rSetpoint := rTempSetpoint_Z4, rProcessValue := rActualTemp_Z4, rOutput => rHeaterCmd_Z4);

// Oxygen Enrichment Cascade
PID_O2(bEnable := bSystemReady, rSetpoint := rO2_Setpoint, rProcessValue := rActual_O2, rOutput => rO2_ValveCmd);

// Sagger Tray Servo Indexing Logic
TMR_SaggerDelay(IN := bSaggerIndexReq AND bSystemReady, PT := T#2S);
IF TMR_SaggerDelay.Q AND bSaggerAtPos THEN
    bSaggerServoIndex := TRUE;
ELSE
    bSaggerServoIndex := FALSE;
END_IF;

// Kiln Rotation
// Basic mapping of RPM to drive command, assuming linear relationship max 10 RPM = 100%
rKilnDriveCmd := LIMIT(0.0, (rKilnRotationSpeedReq / 10.0) * 100.0, 100.0);

// Alarms
IF rActualTemp_Z1 > (rTempSetpoint_Z1 + 20.0) OR rActualTemp_Z4 > (rTempSetpoint_Z4 + 20.0) THEN
    bAlarm := TRUE;
    iErrorCode := 101; // Over temperature alarm
END_IF;

END_FUNCTION_BLOCK
"""

response_content = f"```iec-st\n{st_code}\n```"
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": response_content}]}

os.makedirs("data/swarm_raw", exist_ok=True)
os.makedirs("data", exist_ok=True)

filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f)

with open("data/synthetic_generation_v3_enterprise.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(record) + "\n")
