import json, uuid, os

code = """FUNCTION_BLOCK FB_DoubleFacerControl
VAR_INPUT
    rLineSpeed : REAL; // Current machine speed [m/min]
    rTargetStarchTemp : REAL; // Desired gelatinization temp [C]
    rActualStarchTemp : REAL; // Measured starch temp [C]
    rMoistureContent_Top : REAL; // Top liner moisture [%]
    rMoistureContent_Bottom : REAL; // Bottom liner moisture [%]
    rBoardThickness : REAL; // Flute caliber + liners [mm]
    
    // Steam Chests (Zones 1 to 5)
    rSteamPress_In : ARRAY[1..5] OF REAL; // Inlet steam pressure [Bar]
    
    // Web Tension
    rTensionSetp_Upper : REAL; // Upper blanket tension SP [N/m]
    rTensionSetp_Lower : REAL; // Lower blanket tension SP [N/m]
    rTensionAct_Upper : REAL; 
    rTensionAct_Lower : REAL;
    
    xEnable : BOOL;
    xEmergencyStop : BOOL;
END_VAR

VAR_OUTPUT
    // Heating Control
    rSteamValves_Out : ARRAY[1..5] OF REAL; // Valve position 0-100%
    rCondensateBypass : ARRAY[1..5] OF BOOL;
    
    // Tension Control Drives
    rDriveTorque_Upper : REAL; // [%] torque ref
    rDriveTorque_Lower : REAL; // [%] torque ref
    
    // Status
    xGelatinizationReady : BOOL;
    xWarpWarning : BOOL;
    xFault : BOOL;
END_VAR

VAR
    // Internal States and Timers
    iZone : INT;
    rErrorTemp : REAL;
    rPropHeat : REAL;
    rIntegHeat : REAL;
    rDerivHeat : REAL;
    rLastTempError : REAL;
    
    rTensionError_Upper : REAL;
    rTensionError_Lower : REAL;
    rTensionInt_Upper : REAL;
    rTensionInt_Lower : REAL;
    
    // Tuning parameters (Hardcoded for this example)
    Kp_Heat : REAL := 2.5;
    Ki_Heat : REAL := 0.1;
    Kd_Heat : REAL := 0.5;
    
    Kp_Tens : REAL := 1.2;
    Ki_Tens : REAL := 0.05;
    
    // Warp calculation
    rMoistureDelta : REAL;
    
    // System Cycle Time (assumed 10ms)
    dtCycle : REAL := 0.01;
END_VAR

// Control Logic Execution
IF xEmergencyStop OR NOT xEnable THEN
    FOR iZone := 1 TO 5 DO
        rSteamValves_Out[iZone] := 0.0;
        rCondensateBypass[iZone] := TRUE;
    END_FOR;
    rDriveTorque_Upper := 0.0;
    rDriveTorque_Lower := 0.0;
    xGelatinizationReady := FALSE;
    xWarpWarning := FALSE;
    xFault := xEmergencyStop;
    RETURN;
END_IF;

// 1. Starch Adhesive Gelatinization Cascade & Steam Chest Heat Transfer
rErrorTemp := rTargetStarchTemp - rActualStarchTemp;
rPropHeat := Kp_Heat * rErrorTemp;
rIntegHeat := rIntegHeat + (rErrorTemp * dtCycle * Ki_Heat);
rDerivHeat := Kd_Heat * (rErrorTemp - rLastTempError) / dtCycle;
rLastTempError := rErrorTemp;

IF rIntegHeat > 50.0 THEN rIntegHeat := 50.0; END_IF;
IF rIntegHeat < -20.0 THEN rIntegHeat := -20.0; END_IF;

FOR iZone := 1 TO 5 DO
    IF iZone <= 3 THEN
        rSteamValves_Out[iZone] := rPropHeat + rIntegHeat + rDerivHeat + (rLineSpeed * 0.1) + (rBoardThickness * 2.0);
    ELSE
        rSteamValves_Out[iZone] := (rPropHeat + rIntegHeat) * 0.5 + (rLineSpeed * 0.05);
    END_IF;
    
    IF rSteamValves_Out[iZone] > 100.0 THEN
        rSteamValves_Out[iZone] := 100.0;
    ELSIF rSteamValves_Out[iZone] < 0.0 THEN
        rSteamValves_Out[iZone] := 0.0;
    END_IF;
    
    rCondensateBypass[iZone] := (rSteamPress_In[iZone] < 1.5);
END_FOR;

xGelatinizationReady := (rActualStarchTemp >= rTargetStarchTemp - 2.0);

// 2. Upper and Lower Blanket Tension Control Loops
rTensionError_Upper := rTensionSetp_Upper - rTensionAct_Upper;
rTensionInt_Upper := rTensionInt_Upper + (rTensionError_Upper * dtCycle * Ki_Tens);
IF rTensionInt_Upper > 20.0 THEN rTensionInt_Upper := 20.0; END_IF;
IF rTensionInt_Upper < -20.0 THEN rTensionInt_Upper := -20.0; END_IF;
rDriveTorque_Upper := (Kp_Tens * rTensionError_Upper) + rTensionInt_Upper + (rLineSpeed * 0.2);

rTensionError_Lower := rTensionSetp_Lower - rTensionAct_Lower;
rTensionInt_Lower := rTensionInt_Lower + (rTensionError_Lower * dtCycle * Ki_Tens);
IF rTensionInt_Lower > 20.0 THEN rTensionInt_Lower := 20.0; END_IF;
IF rTensionInt_Lower < -20.0 THEN rTensionInt_Lower := -20.0; END_IF;
rDriveTorque_Lower := (Kp_Tens * rTensionError_Lower) + rTensionInt_Lower + (rLineSpeed * 0.2);

IF rDriveTorque_Upper > 100.0 THEN rDriveTorque_Upper := 100.0; END_IF;
IF rDriveTorque_Upper < 0.0 THEN rDriveTorque_Upper := 0.0; END_IF;

IF rDriveTorque_Lower > 100.0 THEN rDriveTorque_Lower := 100.0; END_IF;
IF rDriveTorque_Lower < 0.0 THEN rDriveTorque_Lower := 0.0; END_IF;

// 3. Warp Control Monitoring
rMoistureDelta := ABS(rMoistureContent_Top - rMoistureContent_Bottom);
IF rMoistureDelta > 2.5 THEN
    xWarpWarning := TRUE;
ELSE
    xWarpWarning := FALSE;
END_IF;

END_FUNCTION_BLOCK
"""

prompt = "Invent a highly complex control scenario for this domain (e.g., steam chest heat transfer profiling, starch adhesive gelatinization cascades, and upper/lower blanket tension loops). Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": f"```iec-st\n{code}\n```"}
    ]
}

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, indent=2)

with open("data/synthetic_generation_v3_enterprise.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(record) + "\n")

print("Done")
