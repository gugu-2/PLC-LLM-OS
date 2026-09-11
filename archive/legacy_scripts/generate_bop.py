import json, uuid, os

st_code = """```iec-st
FUNCTION_BLOCK FB_Subsea_Acoustic_BOP_Control
TITLE = 'Subsea Acoustic BOP Control System'
VERSION : '2.5'
AUTHOR : 'Lumina Elite Data Architect'

VAR_INPUT
    bAcousticSignalValid : BOOL; // Indicates valid acoustic telemetry packet received
    dwAcousticCommandID : DWORD; // Decoded acoustic command ID
    rAccumulatorPressure : REAL; // Current accumulator pressure (psi)
    rWellborePressure : REAL; // Current wellbore pressure (psi)
    bDeadmanSwitchActive : BOOL; // Loss of communication and power indication
    bAutoShearArmed : BOOL; // Auto-shear sequence armed status
    bManualOverride : BOOL; // Surface manual override flag
END_VAR

VAR_OUTPUT
    bShearRamCloseCmd : BOOL; // Command to close blind shear rams
    bPipeRamCloseCmd : BOOL; // Command to close pipe rams
    bAccumulatorChargeCmd : BOOL; // Command to charge accumulator banks
    bAcousticAckTx : BOOL; // Transmit acoustic acknowledgment
    dwSystemState : DWORD; // Current state machine status word
    rEstimatedClosureTime : REAL; // Estimated time to closure (s)
END_VAR

VAR
    Tmr_TelemetryTimeout : TON; // Timeout for acoustic telemetry loss
    Tmr_ShearDelay : TON; // Delay before initiating shear sequence
    Tmr_AccumulatorRecharge : TON; // Minimum recharge duration
    
    // Internal States
    eState : INT; // Main state machine state
    bEmergencySequenceTriggered : BOOL;
    bLowPressureAlarm : BOOL;
    
    // Constants
    c_dwCMD_SHEAR_CLOSE : DWORD := 16#A1B2C3D4;
    c_dwCMD_PIPE_CLOSE : DWORD := 16#E5F60718;
    c_dwCMD_SYSTEM_RESET : DWORD := 16#99887766;
    
    c_rMinAccumulatorPres : REAL := 3000.0; // Minimum required pressure (psi)
    c_rMaxAccumulatorPres : REAL := 5000.0; // Maximum allowed pressure (psi)
    c_rCriticalWellPres : REAL := 12000.0; // Critical wellbore pressure (psi)
END_VAR

(* 
    ========================================================================
    STATE MACHINE DEFINITIONS
    ========================================================================
    0: IDLE / STANDBY
    10: PROCESSING ACOUSTIC COMMAND
    20: DEAD-MAN / AUTO-SHEAR EVALUATION
    30: SHEAR RAM CLOSURE SEQUENCE
    40: ACCUMULATOR MANAGEMENT
    99: SYSTEM FAULT
*)

// 1. Acoustic Telemetry Decoding
IF bAcousticSignalValid AND NOT bEmergencySequenceTriggered THEN
    IF dwAcousticCommandID = c_dwCMD_SHEAR_CLOSE THEN
        eState := 30; // Initiate direct shear
    ELSIF dwAcousticCommandID = c_dwCMD_PIPE_CLOSE THEN
        bPipeRamCloseCmd := TRUE;
        bAcousticAckTx := TRUE;
    ELSIF dwAcousticCommandID = c_dwCMD_SYSTEM_RESET THEN
        eState := 0;
        bEmergencySequenceTriggered := FALSE;
        bShearRamCloseCmd := FALSE;
        bPipeRamCloseCmd := FALSE;
    END_IF;
END_IF;

// 2. Dead-Man & Auto-Shear Evaluation
Tmr_TelemetryTimeout(IN := NOT bAcousticSignalValid AND NOT bManualOverride, PT := T#300S);

IF (Tmr_TelemetryTimeout.Q AND bDeadmanSwitchActive) OR 
   (bAutoShearArmed AND rWellborePressure > c_rCriticalWellPres) THEN
    bEmergencySequenceTriggered := TRUE;
    eState := 20;
END_IF;

IF eState = 20 THEN
    // Dead-Man arming delay to allow transient faults to clear
    Tmr_ShearDelay(IN := TRUE, PT := T#15S);
    IF Tmr_ShearDelay.Q THEN
        eState := 30; // Proceed to shear
        Tmr_ShearDelay(IN := FALSE); // Reset timer
    END_IF;
ELSE
    Tmr_ShearDelay(IN := FALSE);
END_IF;

// 3. Shear Ram Closure Sequence
IF eState = 30 THEN
    // Ensure sufficient accumulator pressure before shearing
    IF rAccumulatorPressure >= c_rMinAccumulatorPres THEN
        bShearRamCloseCmd := TRUE;
        bAcousticAckTx := TRUE;
        rEstimatedClosureTime := 4.5; // Fixed theoretical closure time
        dwSystemState := 16#FFFF; // Indicate locked/closed state
        eState := 40; // Transition to post-shear pressure management
    ELSE
        bLowPressureAlarm := TRUE;
        eState := 99; // Transition to fault state
    END_IF;
END_IF;

// 4. Accumulator Pressure Management
IF eState = 40 OR eState = 0 THEN
    IF rAccumulatorPressure < c_rMinAccumulatorPres THEN
        bAccumulatorChargeCmd := TRUE;
    ELSIF rAccumulatorPressure > c_rMaxAccumulatorPres THEN
        bAccumulatorChargeCmd := FALSE;
    END_IF;
    
    // Recharge timer logic
    Tmr_AccumulatorRecharge(IN := bAccumulatorChargeCmd, PT := T#60S);
    IF Tmr_AccumulatorRecharge.Q THEN
        bAccumulatorChargeCmd := FALSE; // Prevent pump overheating
    END_IF;
END_IF;

// 5. Fault Handling
IF eState = 99 THEN
    dwSystemState := 16#DEADDEAD;
    // Latch commands off unless overridden
    IF NOT bManualOverride THEN
        bAccumulatorChargeCmd := FALSE;
    END_IF;
END_IF;

// Update status outputs
dwSystemState := dwSystemState OR INT_TO_DWORD(eState);

END_FUNCTION_BLOCK
```"""

user_prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: Subsea Acoustic Blowout Preventer (BOP).
Task: Invent a highly complex control scenario for this domain (e.g., deepwater acoustic telemetry decoding, accumulator pressure management, and dead-man blind shear ram sequencing).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O.

CRITICAL RULES:
1. You MUST output the code enclosed in a ```iec-st markdown code fence. DO NOT APOLOGIZE. DO NOT EXPLAIN.
2. The code must be >= 1500 chars, with FUNCTION_BLOCK and VAR_INPUT/VAR_OUTPUT."""

record = {
    "messages": [
        {"role": "user", "content": user_prompt},
        {"role": "assistant", "content": st_code}
    ]
}

os.makedirs("data/swarm_raw", exist_ok=True)
os.makedirs("data", exist_ok=True)

file_id = uuid.uuid4().hex[:8]
json_filename = f"data/swarm_raw/agent_{file_id}.json"

with open(json_filename, "w", encoding="utf-8") as f:
    json.dump(record, f, indent=2)

with open("data/synthetic_generation_v3_enterprise.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(record) + "\n")
