import json, uuid
import os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: High-Speed Aluminum Can Seaming and Rotary Filler Synchronization**

Task: Invent a highly complex, ultra-realistic control scenario for this domain. Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_CanSeaming_RotaryFiller\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
   record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
   with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
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
6. REPLY with: EVOLUTION COMPLETE: High-Speed Aluminum Can Seaming and Rotary Filler Synchronization

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_HighSpeedCanSeamingFillerSync
(* 
   =============================================================================
   AUTHOR: Lumina AI Cloud Swarm
   DOMAIN: High-Speed Aluminum Can Seaming and Rotary Filler Synchronization
   DESCRIPTION:
   Advanced, mathematically rigorous synchronization logic for a high-speed
   rotary volumetric filler and double-seam can seamer. Incorporates
   moving-average noise filtering, phase-locked loop (PLL) style virtual axis
   synchronization, multi-layered safety and jam detection, and a high-fidelity
   PID trim loop for precise angular offset control.
   =============================================================================
*)

VAR_INPUT
    bSystemEnable           : BOOL;     (* Global permissive for system operation *)
    bEStopOK                : BOOL;     (* Main safety relay loop healthy (TRUE = OK) *)
    rFillerSpeedMaster      : REAL;     (* Master velocity setpoint from line controller (Cans Per Minute) *)
    rFillerActualPos        : REAL;     (* Encoder feedback: Filler absolute position [0.0 - 360.0 deg] *)
    rSeamerActualPos        : REAL;     (* Encoder feedback: Seamer absolute position [0.0 - 360.0 deg] *)
    rPhaseOffsetSp          : REAL;     (* Target phase offset between Filler and Seamer [deg] *)
    bSeamerTorqueLimitOK    : BOOL;     (* True if seamer servo torque is within normal limits *)
    bCanPresenceSensor      : BOOL;     (* Optical sensor detecting can transfer handoff *)
END_VAR

VAR_OUTPUT
    bSystemReady            : BOOL;     (* Indicates drive servos are engaged and synchronized *)
    rSeamerSpeedCmd         : REAL;     (* Base velocity command to seamer servo drive *)
    rSeamerTrimTorque       : REAL;     (* Additional trim torque/velocity for precise phase alignment *)
    bCriticalJamAlarm       : BOOL;     (* Triggered on catastrophic desync or high torque *)
    iOperationState         : INT;      (* Current state of the synchronization state machine *)
END_VAR

VAR
    (* Internal State and Filtering *)
    iState                  : INT := 0; (* Internal state tracking *)
    rPosError               : REAL := 0.0;
    rPosErrorFiltered       : REAL := 0.0;
    rLastError              : REAL := 0.0;
    rIntegral               : REAL := 0.0;
    rDerivative             : REAL := 0.0;
    
    (* PID Parameters for Trim *)
    rKp                     : REAL := 1.25;
    rKi                     : REAL := 0.15;
    rKd                     : REAL := 0.05;
    
    (* Timers *)
    tEStopDebounce          : TON;
    tSyncTimeout            : TON;
    tJamFilter              : TON;
    
    (* Noise Filter Constants *)
    rAlpha                  : REAL := 0.2; (* Low-pass filter coefficient for position error *)
    
    (* Constants *)
    C_MAX_PHASE_ERROR       : REAL := 5.0;  (* Maximum allowed phase error in degrees before fault *)
    C_NOMINAL_ACCEL         : REAL := 50.0; (* Base acceleration limit *)
END_VAR

(* === MAIN LOGIC === *)

(* 1. Safety and Interlock Layer *)
tEStopDebounce(IN := NOT bEStopOK, PT := T#50MS);
IF tEStopDebounce.Q THEN
    (* Immediate catastrophic fault response *)
    bSystemReady := FALSE;
    bCriticalJamAlarm := TRUE;
    rSeamerSpeedCmd := 0.0;
    rSeamerTrimTorque := 0.0;
    iState := 999; (* Fault State *)
    iOperationState := iState;
    RETURN;
END_IF;

(* 2. Moving Average / Low-Pass Noise Filter on Phase Error *)
(* Calculate raw shortest-path angular error [-180, 180] *)
rPosError := (rFillerActualPos - rSeamerActualPos) - rPhaseOffsetSp;
IF rPosError > 180.0 THEN
    rPosError := rPosError - 360.0;
ELSIF rPosError < -180.0 THEN
    rPosError := rPosError + 360.0;
END_IF;

(* Apply Exponential Smoothing Low-Pass Filter *)
rPosErrorFiltered := rAlpha * rPosError + (1.0 - rAlpha) * rPosErrorFiltered;

(* 3. Seamer Jam Detection via Torque Limit and Phase Error *)
tJamFilter(IN := (NOT bSeamerTorqueLimitOK) OR (ABS(rPosErrorFiltered) > C_MAX_PHASE_ERROR), PT := T#20MS);
IF tJamFilter.Q THEN
    bCriticalJamAlarm := TRUE;
    bSystemReady := FALSE;
    iState := 999;
END_IF;

(* 4. Main Synchronization State Machine *)
CASE iState OF
    0: (* INIT / STANDBY *)
        bSystemReady := FALSE;
        rSeamerSpeedCmd := 0.0;
        rSeamerTrimTorque := 0.0;
        bCriticalJamAlarm := FALSE;
        
        IF bSystemEnable AND bEStopOK THEN
            iState := 10;
        END_IF;

    10: (* RAMP-UP TO MASTER VELOCITY (Open Loop) *)
        rSeamerSpeedCmd := rFillerSpeedMaster; (* Feed-forward base speed *)
        rSeamerTrimTorque := 0.0;
        
        IF rFillerSpeedMaster > 100.0 THEN (* Cans per minute minimum threshold *)
            iState := 20;
            tSyncTimeout(IN := FALSE);
        END_IF;
        
        IF NOT bSystemEnable THEN
            iState := 0;
        END_IF;

    20: (* PHASE-LOCKED LOOP SYNC (Closed Loop Trim) *)
        (* Run precise PID for phase alignment *)
        rIntegral := rIntegral + rPosErrorFiltered;
        (* Anti-windup protection *)
        IF rIntegral > 100.0 THEN rIntegral := 100.0; END_IF;
        IF rIntegral < -100.0 THEN rIntegral := -100.0; END_IF;
        
        rDerivative := rPosErrorFiltered - rLastError;
        
        (* Calculate Trim Output *)
        rSeamerTrimTorque := (rKp * rPosErrorFiltered) + (rKi * rIntegral) + (rKd * rDerivative);
        
        rLastError := rPosErrorFiltered;
        
        (* Evaluate Sync Condition *)
        IF ABS(rPosErrorFiltered) < 1.0 THEN
            tSyncTimeout(IN := TRUE, PT := T#500MS);
            IF tSyncTimeout.Q THEN
                iState := 30;
                bSystemReady := TRUE;
            END_IF;
        ELSE
            tSyncTimeout(IN := FALSE);
        END_IF;
        
        IF NOT bSystemEnable THEN
            iState := 0;
        END_IF;

    30: (* SYNCHRONIZED RUNNING *)
        bSystemReady := TRUE;
        (* Continuous closed-loop trim calculation *)
        rIntegral := rIntegral + rPosErrorFiltered;
        (* Strict Anti-windup in running mode *)
        IF rIntegral > 50.0 THEN rIntegral := 50.0; END_IF;
        IF rIntegral < -50.0 THEN rIntegral := -50.0; END_IF;
        
        rDerivative := rPosErrorFiltered - rLastError;
        rSeamerTrimTorque := (rKp * rPosErrorFiltered) + (rKi * rIntegral) + (rKd * rDerivative);
        rLastError := rPosErrorFiltered;
        
        (* Fallback to re-sync if drifted too far but not jammed *)
        IF ABS(rPosErrorFiltered) >= 1.0 THEN
            bSystemReady := FALSE;
            iState := 20;
        END_IF;
        
        IF NOT bSystemEnable THEN
            iState := 0;
        END_IF;
        
    999: (* FAULT / JAMMED *)
        bSystemReady := FALSE;
        rSeamerSpeedCmd := 0.0;
        rSeamerTrimTorque := 0.0;
        
        (* Wait for manual reset sequence (simulated by toggle of Enable) *)
        IF NOT bSystemEnable AND bEStopOK AND NOT tJamFilter.Q THEN
            bCriticalJamAlarm := FALSE;
            iState := 0;
        END_IF;

END_CASE;

iOperationState := iState;

END_FUNCTION_BLOCK
```"""

import os

os.makedirs("c:/Users/majip/Downloads/LLM REASEARCH/data/swarm_raw", exist_ok=True)

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": code}
    ]
}

filename = f"c:/Users/majip/Downloads/LLM REASEARCH/data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print(f"Saved to {filename}")
