import json, uuid, os

os.makedirs('data/swarm_raw', exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: High-Speed Web Cardboard Corrugator.
Task: Invent a highly complex control scenario for this domain (e.g., single-facer flute roll steam pressure profiling, starch adhesive gelatinization temperature, and double-backer hot plate zones).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."""

iec_code = """FUNCTION_BLOCK FB_Corrugator_Control
VAR_INPUT
    bEnable : BOOL; // System enable
    rLineSpeed_m_min : REAL; // Current web line speed
    rTargetStarchTemp_C : REAL; // Setpoint for starch gelatinization
    rSteamPressSP_Bar : REAL; // Single-facer flute roll steam pressure setpoint
    rHotPlateTempSP_C : REAL; // Double-backer hot plate setpoint
    
    // Physical AI
    AI_StarchTemp1_C : REAL;
    AI_StarchTemp2_C : REAL;
    AI_SteamPress1_Bar : REAL;
    AI_HotPlateTempZone1_C : REAL;
    AI_HotPlateTempZone2_C : REAL;
    AI_HotPlateTempZone3_C : REAL;
END_VAR

VAR_OUTPUT
    bSystemReady : BOOL;
    bAlarmActive : BOOL;
    iAlarmCode : INT;
    
    // Physical AO
    AO_StarchHeaterValve_Pct : REAL; // 0-100%
    AO_SteamValve_Pct : REAL; // 0-100%
    AO_HotPlateHeaterZone1_Pct : REAL; // 0-100%
    AO_HotPlateHeaterZone2_Pct : REAL; // 0-100%
    AO_HotPlateHeaterZone3_Pct : REAL; // 0-100%
END_VAR

VAR
    // PID Controllers for Starch
    stStarchPID : PID_T;
    rStarchTempAvg : REAL;
    
    // PID for Steam
    stSteamPID : PID_T;
    
    // PID for Hot Plates
    stHotPlatePID_Z1 : PID_T;
    stHotPlatePID_Z2 : PID_T;
    stHotPlatePID_Z3 : PID_T;
    
    // Timers
    tonStartupDelay : TON;
    tonAlarmDelay : TON;
    
    // Internal States
    iState : INT;
    bStarchOK : BOOL;
    bSteamOK : BOOL;
    bHotPlatesOK : BOOL;
    
    // Tuning params (static for this example)
    Kp_Starch : REAL := 2.5;
    Ti_Starch : REAL := 12.0;
    Kp_Steam : REAL := 1.8;
    Ti_Steam : REAL := 8.0;
END_VAR

// --- IMPLEMENTATION ---
IF NOT bEnable THEN
    bSystemReady := FALSE;
    bAlarmActive := FALSE;
    iAlarmCode := 0;
    AO_StarchHeaterValve_Pct := 0.0;
    AO_SteamValve_Pct := 0.0;
    AO_HotPlateHeaterZone1_Pct := 0.0;
    AO_HotPlateHeaterZone2_Pct := 0.0;
    AO_HotPlateHeaterZone3_Pct := 0.0;
    iState := 0;
    RETURN;
END_IF;

// Calculate averages
rStarchTempAvg := (AI_StarchTemp1_C + AI_StarchTemp2_C) / 2.0;

// Starch Temperature Control
stStarchPID.SP := rTargetStarchTemp_C;
stStarchPID.PV := rStarchTempAvg;
stStarchPID.Kp := Kp_Starch;
stStarchPID.Ti := Ti_Starch;
stStarchPID.EN := TRUE;
stStarchPID(); // Execute PID
AO_StarchHeaterValve_Pct := stStarchPID.OUT;

// Steam Pressure Control
stSteamPID.SP := rSteamPressSP_Bar;
stSteamPID.PV := AI_SteamPress1_Bar;
stSteamPID.Kp := Kp_Steam;
stSteamPID.Ti := Ti_Steam;
stSteamPID.EN := TRUE;
stSteamPID();
AO_SteamValve_Pct := stSteamPID.OUT;

// Hot Plate Zone 1 Control
stHotPlatePID_Z1.SP := rHotPlateTempSP_C;
stHotPlatePID_Z1.PV := AI_HotPlateTempZone1_C;
stHotPlatePID_Z1.Kp := 3.0;
stHotPlatePID_Z1.Ti := 15.0;
stHotPlatePID_Z1.EN := TRUE;
stHotPlatePID_Z1();
AO_HotPlateHeaterZone1_Pct := stHotPlatePID_Z1.OUT;

// Hot Plate Zone 2 Control (Offset by line speed influence)
stHotPlatePID_Z2.SP := rHotPlateTempSP_C + (rLineSpeed_m_min * 0.05);
stHotPlatePID_Z2.PV := AI_HotPlateTempZone2_C;
stHotPlatePID_Z2.Kp := 3.0;
stHotPlatePID_Z2.Ti := 15.0;
stHotPlatePID_Z2.EN := TRUE;
stHotPlatePID_Z2();
AO_HotPlateHeaterZone2_Pct := stHotPlatePID_Z2.OUT;

// Hot Plate Zone 3 Control (Further offset)
stHotPlatePID_Z3.SP := rHotPlateTempSP_C + (rLineSpeed_m_min * 0.1);
stHotPlatePID_Z3.PV := AI_HotPlateTempZone3_C;
stHotPlatePID_Z3.Kp := 3.0;
stHotPlatePID_Z3.Ti := 15.0;
stHotPlatePID_Z3.EN := TRUE;
stHotPlatePID_Z3();
AO_HotPlateHeaterZone3_Pct := stHotPlatePID_Z3.OUT;

// Readiness Checks
bStarchOK := ABS(rTargetStarchTemp_C - rStarchTempAvg) < 2.0;
bSteamOK := ABS(rSteamPressSP_Bar - AI_SteamPress1_Bar) < 0.5;
bHotPlatesOK := (ABS(rHotPlateTempSP_C - AI_HotPlateTempZone1_C) < 5.0) AND
                (ABS(stHotPlatePID_Z2.SP - AI_HotPlateTempZone2_C) < 5.0) AND
                (ABS(stHotPlatePID_Z3.SP - AI_HotPlateTempZone3_C) < 5.0);

bSystemReady := bStarchOK AND bSteamOK AND bHotPlatesOK;

// Alarms
IF rStarchTempAvg > 120.0 THEN
    bAlarmActive := TRUE;
    iAlarmCode := 101; // Starch over-temp
ELSIF AI_SteamPress1_Bar > 12.0 THEN
    bAlarmActive := TRUE;
    iAlarmCode := 102; // Steam over-pressure
ELSE
    bAlarmActive := FALSE;
    iAlarmCode := 0;
END_IF;

END_FUNCTION_BLOCK"""

assistant_content = f"```iec-st\n{iec_code}\n```"

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": assistant_content}
    ]
}

file_path = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(file_path, "w", encoding="utf-8") as f:
    json.dump(record, f, indent=2)
print(f"Success: {file_path}")
