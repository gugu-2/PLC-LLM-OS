import os, json, uuid
os.makedirs('data/swarm_raw', exist_ok=True)
prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Advanced Pharmaceutical Inhalation Dry Powder Blending**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., resonant acoustic mixing (RAM) high-g vibration profiling, near-infrared (NIR) real-time blend uniformity analysis, and micronized API electrostatic discharge (ESD) suppression). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

CRITICAL RULES - READ EVERY LINE:
1. CODE FENCE: Use TRIPLE backticks + iec-st. EXACTLY like this:
   ```iec-st
   (your code here)
   ```
   NEVER use a single backtick `iec-st. ALWAYS use triple backticks.
2. REQUIRED IEC 61131-3 STRUCTURE (all 5 mandatory):
   a. FUNCTION_BLOCK FB_<Name>   <- first line of code, always
   b. VAR_INPUT ... END_VAR      <- min 4 typed inputs with comments
   c. VAR_OUTPUT ... END_VAR     <- min 3 typed outputs with comments
   d. At least one END_IF; or END_CASE;  <- control logic required
   e. END_FUNCTION_BLOCK         <- last line of code, always
3. LENGTH: The assistant content MUST be >= 1500 characters total.
4. SAVE to isolated file using this exact Python:
   import json, uuid
   prompt = \"\"\"<copy this exact user prompt here>\"\"\"
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_DryPowderBlending\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
   record = {\"messages\": [{\"role\": \"user\", \"content\": prompt}, {\"role\": \"assistant\", \"content\": code}]}
   with open(f\"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json\", \"w\", encoding=\"utf-8\") as f:
       json.dump(record, f, ensure_ascii=False)
5. SELF-CHECK before saving - verify ALL:
   [ ] Fence is ```iec-st
   [ ] First code line: FUNCTION_BLOCK FB_<name>
   [ ] Has VAR_INPUT section
   [ ] Has VAR_OUTPUT section
   [ ] Has END_IF; or END_CASE;
   [ ] Last code line: END_FUNCTION_BLOCK
   [ ] Closing fence: ```
   [ ] Total chars >= 1500
6. REPLY with: EVOLUTION COMPLETE: Advanced Pharmaceutical Inhalation Dry Powder Blending

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_AdvPharmaRAM_Blender
TITLE = 'Advanced Pharmaceutical Inhalation Dry Powder Blending Control'
(*
  Author: Lumina AI Swarm
  Description: Highly complex state machine for Resonant Acoustic Mixing (RAM)
  incorporating real-time Near-Infrared (NIR) blend uniformity feedback,
  high-g vibration profiling, and active Electrostatic Discharge (ESD) suppression
  for micronized Active Pharmaceutical Ingredients (APIs).
*)
VAR_INPUT
    bEnable             : BOOL;  (* System enable / start sequence command *)
    bEmergencyStop      : BOOL;  (* Safety relay status: TRUE = Healthy, FALSE = E-STOP *)
    rTargetG_Force      : REAL;  (* Desired resonance acceleration in [g] (e.g., 20.0 - 100.0) *)
    rNIR_RSD_Current    : REAL;  (* Current Relative Standard Deviation from NIR probe [%] *)
    rNIR_RSD_Target     : REAL;  (* Target RSD for acceptable blend uniformity [%] *)
    rESD_Voltage_kV     : REAL;  (* Vessel electrostatic voltage measurement [kV] *)
    rVesselTemp_C       : REAL;  (* Mixing vessel temperature [deg C] *)
    bN2_PurgeOK         : BOOL;  (* Nitrogen inerting system status *)
END_VAR
VAR_OUTPUT
    bSystemReady        : BOOL;  (* TRUE when IDLE and ready for a new batch *)
    rDriveCommand       : REAL;  (* Speed/Force command to the acoustic drive [0.0 - 100.0%] *)
    bESD_IonizerCmd     : BOOL;  (* Command to activate high-voltage ionizing ESD suppression *)
    bUniformityReached  : BOOL;  (* TRUE when NIR target RSD is met and sustained *)
    bCriticalAlarm      : BOOL;  (* TRUE on temp high, ESD critically high, or e-stop *)
    iState_Current      : INT;   (* Current active step in the processing sequence *)
END_VAR
VAR
    iState              : INT := 0;
    tStateTimer         : TON;
    tNIR_Stabilize      : TON;
    rCurrentCommand     : REAL := 0.0;
    rMaxTempLimit       : REAL := 45.0; (* Inhalation APIs degrade > 45C *)
    rESD_MaxLimit       : REAL := 5.0;  (* > 5kV requires active suppression *)
    rESD_TripLimit      : REAL := 15.0; (* > 15kV requires emergency shutdown *)
    rRampRate           : REAL := 2.5;  (* Command increase per cycle *)
END_VAR

(* === CRITICAL SAFETY & INTERLOCK LOGIC === *)
IF NOT bEmergencyStop OR (rVesselTemp_C > rMaxTempLimit) OR (rESD_Voltage_kV > rESD_TripLimit) OR NOT bN2_PurgeOK THEN
    (* Immediate fail-safe state *)
    rCurrentCommand := 0.0;
    rDriveCommand := 0.0;
    bESD_IonizerCmd := TRUE; (* Maximize suppression during fault dump *)
    bSystemReady := FALSE;
    bUniformityReached := FALSE;
    bCriticalAlarm := TRUE;
    iState := 99; (* Fault state *)
    RETURN;
END_IF;

(* Active ESD Suppression Loop *)
IF rESD_Voltage_kV > rESD_MaxLimit THEN
    bESD_IonizerCmd := TRUE;
ELSE
    bESD_IonizerCmd := FALSE;
END_IF;

(* === MAIN PROCESS STATE MACHINE === *)
CASE iState OF
    0: (* IDLE & READY *)
        bSystemReady := TRUE;
        bCriticalAlarm := FALSE;
        rCurrentCommand := 0.0;
        rDriveCommand := 0.0;
        bUniformityReached := FALSE;

        IF bEnable THEN
            bSystemReady := FALSE;
            iState := 10;
        END_IF;

    10: (* PRE-BLENDING INERTING & CHECK *)
        (* Wait for N2 purge to stabilize *)
        tStateTimer(IN := TRUE, PT := T#10S);
        IF tStateTimer.Q THEN
            tStateTimer(IN := FALSE);
            iState := 20;
        END_IF;

    20: (* RAMP UP RAM VIBRATION *)
        IF rCurrentCommand < rTargetG_Force THEN
            rCurrentCommand := rCurrentCommand + rRampRate;
        ELSE
            rCurrentCommand := rTargetG_Force;
            iState := 30;
        END_IF;
        rDriveCommand := rCurrentCommand;

    30: (* STEADY STATE BLENDING & NIR ANALYSIS *)
        rDriveCommand := rTargetG_Force;
        
        (* Check Blend Uniformity via NIR Relative Standard Deviation *)
        IF rNIR_RSD_Current <= rNIR_RSD_Target THEN
            tNIR_Stabilize(IN := TRUE, PT := T#30S); (* Must hold tolerance for 30s *)
        ELSE
            tNIR_Stabilize(IN := FALSE);
        END_IF;

        IF tNIR_Stabilize.Q THEN
            bUniformityReached := TRUE;
            tNIR_Stabilize(IN := FALSE);
            iState := 40;
        END_IF;

    40: (* RAMP DOWN *)
        IF rCurrentCommand > 0.0 THEN
            rCurrentCommand := rCurrentCommand - rRampRate;
        ELSE
            rCurrentCommand := 0.0;
            iState := 50;
        END_IF;
        rDriveCommand := rCurrentCommand;

    50: (* POST-BLEND ESD DISSIPATION *)
        (* Allow any residual static to dissipate before operator access *)
        bESD_IonizerCmd := TRUE; 
        tStateTimer(IN := TRUE, PT := T#15S);
        IF tStateTimer.Q THEN
            bESD_IonizerCmd := FALSE;
            tStateTimer(IN := FALSE);
            iState := 60;
        END_IF;

    60: (* BATCH COMPLETE *)
        IF NOT bEnable THEN
            iState := 0;
        END_IF;

    99: (* FAULT HANDLING *)
        (* Waiting for operator reset / e-stop clear *)
        IF NOT bEnable AND bEmergencyStop AND (rVesselTemp_C < rMaxTempLimit) AND (rESD_Voltage_kV < rESD_TripLimit) THEN
            iState := 0;
        END_IF;

END_CASE;

iState_Current := iState;

END_FUNCTION_BLOCK
```"""

record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
print(f"Saved to {filename}")
