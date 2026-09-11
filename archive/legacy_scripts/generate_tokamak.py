import json
import uuid
import os

os.makedirs('data/swarm_raw', exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: Fusion Tokamak Diagnostic & Control Subsystem.
Task: Invent a highly complex control scenario for this domain (e.g., superconducting toroidal field coil quench detection, neutral beam injection (NBI) interlocks, and cryopump regeneration).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."""

st_code = """FUNCTION_BLOCK FB_Tokamak_Diagnostic_Control
VAR_INPUT
    bSystemEnable : BOOL; // Main system enable
    rTF_CoilTemp : ARRAY[1..16] OF REAL; // Toroidal Field coil temperatures (K)
    rTF_VoltageDrop : ARRAY[1..16] OF REAL; // Voltage drop across coils (V)
    rTF_Current : REAL; // Total TF coil current (kA)
    bNBI_Ready : BOOL; // Neutral Beam Injector readiness
    rPlasmaDensity : REAL; // Plasma density (10^19 m^-3)
    bCryoPumpHighLevel : BOOL; // Cryopump saturation level
    rCryoPumpTemp : REAL; // Cryopump operating temperature (K)
    bEmergencyStop : BOOL; // Hard emergency stop
END_VAR

VAR_OUTPUT
    bQuenchDetected : BOOL; // TF Coil Quench detected!
    bFastDischarge : BOOL; // Trigger fast energy discharge
    bNBI_InterlockEnable : BOOL; // Enable NBI injection
    bCryoRegenStart : BOOL; // Start cryopump regeneration cycle
    bSystemFault : BOOL; // General system fault
    wFaultCode : WORD; // Detailed fault code
END_VAR

VAR
    i : INT;
    rTempThreshold : REAL := 5.2; // Critical temperature threshold (K)
    rVoltageThreshold : REAL := 0.050; // Critical resistive voltage drop (V)
    timerQuenchDelay : TON;
    timerRegenDuration : TON;
    bRegenActive : BOOL := FALSE;
    bNBI_Permit : BOOL := FALSE;
    stateMachine : INT := 0; // 0=IDLE, 1=RUN, 2=REGEN, 99=FAULT
END_VAR

// ==============================================================================
// 1. Quench Detection Logic (Superconducting TF Coils)
// ==============================================================================
bQuenchDetected := FALSE;
FOR i := 1 TO 16 DO
    // Check for both high temperature and resistive voltage drop anomalies
    IF (rTF_CoilTemp[i] > rTempThreshold) AND (rTF_VoltageDrop[i] > rVoltageThreshold) THEN
        bQuenchDetected := TRUE;
    END_IF;
END_FOR;

// Delay timer to prevent false positives on voltage spikes
timerQuenchDelay(IN := bQuenchDetected, PT := T#50MS);

IF timerQuenchDelay.Q OR bEmergencyStop THEN
    bFastDischarge := TRUE;
    bSystemFault := TRUE;
    wFaultCode := 16#F001; // Quench or E-Stop Fault
    stateMachine := 99;
END_IF;

// ==============================================================================
// 2. NBI Interlocks (Neutral Beam Injection)
// ==============================================================================
// Injection is only permitted if the plasma density is sufficient to absorb the beam,
// avoiding damage to the opposite wall of the tokamak vacuum vessel.
IF (rPlasmaDensity > 2.5) AND bNBI_Ready AND NOT bSystemFault AND (stateMachine = 1) THEN
    bNBI_Permit := TRUE;
ELSE
    bNBI_Permit := FALSE;
END_IF;

bNBI_InterlockEnable := bNBI_Permit;

// ==============================================================================
// 3. Cryopump Regeneration Logic
// ==============================================================================
IF bCryoPumpHighLevel AND NOT bRegenActive AND (stateMachine <> 99) THEN
    bRegenActive := TRUE;
    bCryoRegenStart := TRUE;
END_IF;

timerRegenDuration(IN := bRegenActive, PT := T#120M); // 2 hour regeneration

IF timerRegenDuration.Q OR (rCryoPumpTemp > 80.0) THEN // 80K means fully defrosted
    bRegenActive := FALSE;
    bCryoRegenStart := FALSE;
END_IF;

// ==============================================================================
// 4. Main State Machine
// ==============================================================================
CASE stateMachine OF
    0: // IDLE
        IF bSystemEnable AND NOT bSystemFault THEN
            stateMachine := 1;
        END_IF;
    
    1: // RUN
        IF NOT bSystemEnable THEN
            stateMachine := 0;
        END_IF;
        IF bRegenActive THEN
            stateMachine := 2;
        END_IF;
        
    2: // REGEN
        IF NOT bRegenActive THEN
            stateMachine := 1;
        END_IF;
        
    99: // FAULT
        bFastDischarge := TRUE;
        bNBI_InterlockEnable := FALSE;
END_CASE;

END_FUNCTION_BLOCK"""

content = "```iec-st\n" + st_code + "\n```"

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": content}
    ]
}

# Save to swarm_raw per user instructions
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, indent=2)
print(f"Saved to {filename}")

# Append to synthetic_generation_v3_enterprise.jsonl per system instructions
os.makedirs('data', exist_ok=True)
with open("data/synthetic_generation_v3_enterprise.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(record) + "\\n")
print("Appended to data/synthetic_generation_v3_enterprise.jsonl")
