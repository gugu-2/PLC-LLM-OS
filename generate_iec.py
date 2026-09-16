import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Deep-Sea Manganese Nodule Mining Crawler Tracks Synchronisation**

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_DeepSea_Crawler\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Deep-Sea Manganese Nodule Mining Crawler Tracks Synchronisation

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_DeepSeaTrackSync
VAR_INPUT
    bEnable                 : BOOL;       (* Master enable signal from ROV topside control *)
    bEmergencyStop          : BOOL;       (* Safety relay OK signal; TRUE = OK, FALSE = STOP *)
    rTrackLeftSpeedSet      : REAL;       (* Desired speed for port-side track (m/s) *)
    rTrackRightSpeedSet     : REAL;       (* Desired speed for starboard-side track (m/s) *)
    rTrackLeftActualSpeed   : REAL;       (* Encoder feedback port track (m/s) *)
    rTrackRightActualSpeed  : REAL;       (* Encoder feedback starboard track (m/s) *)
    rInclinometerPitch      : REAL;       (* Vehicle pitch angle (degrees) for slope compensation *)
    rInclinometerRoll       : REAL;       (* Vehicle roll angle (degrees) for slip compensation *)
    bSlipDetectLeft         : BOOL;       (* Mud slip detection logic on left track *)
    bSlipDetectRight        : BOOL;       (* Mud slip detection logic on right track *)
END_VAR

VAR_OUTPUT
    bSystemReady            : BOOL;       (* Sub-sea synchronisation system ready status *)
    bAlarm                  : BOOL;       (* High severity fault alarm output *)
    bWarningSlip            : BOOL;       (* Warning indicator for traction slip on seabed *)
    rControlOutputLeft      : REAL;       (* Actuator signal to port hydraulic drive (-100 to 100%) *)
    rControlOutputRight     : REAL;       (* Actuator signal to starboard hydraulic drive (-100 to 100%) *)
    iCurrentStateCode       : INT;        (* Current internal state machine code for telemetry *)
END_VAR

VAR
    iState                  : INT := 0;   (* Internal execution state *)
    tStartupDelay           : TON;        (* Delay timer for hydraulic pressure stabilization *)
    tStallTimerLeft         : TON;        (* Timer to detect sustained stalling on port track *)
    tStallTimerRight        : TON;        (* Timer to detect sustained stalling on starboard track *)
    rPidErrorLeft           : REAL := 0.0;
    rPidIntegralLeft        : REAL := 0.0;
    rPidDerivativeLeft      : REAL := 0.0;
    rPidPrevErrorLeft       : REAL := 0.0;
    rPidErrorRight          : REAL := 0.0;
    rPidIntegralRight       : REAL := 0.0;
    rPidDerivativeRight     : REAL := 0.0;
    rPidPrevErrorRight      : REAL := 0.0;
    
    (* PI tuning parameters for deep sea viscous mud dynamics *)
    Kp                      : REAL := 12.5; 
    Ki                      : REAL := 2.1; 
    Kd                      : REAL := 0.05;
    rDt                     : REAL := 0.01; (* 10ms execution cycle time *)
END_VAR

(* === MAIN LOGIC === *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bAlarm := TRUE;
    rControlOutputLeft := 0.0;
    rControlOutputRight := 0.0;
    iState := 99; (* FAULT STATE *)
    iCurrentStateCode := iState;
    RETURN;
END_IF;

CASE iState OF
    0: (* IDLE - Awaiting Enable and Hydraulic checks *)
        bSystemReady := FALSE;
        bAlarm := FALSE;
        bWarningSlip := FALSE;
        rControlOutputLeft := 0.0;
        rControlOutputRight := 0.0;
        
        IF bEnable THEN
            iState := 10;
        END_IF;

    10: (* HYDRAULIC SPIN-UP DELAY *)
        tStartupDelay(IN := TRUE, PT := T#3S);
        IF tStartupDelay.Q THEN
            tStartupDelay(IN := FALSE);
            bSystemReady := TRUE;
            iState := 20;
        END_IF;

    20: (* RUNNING - SYNCHRONISED CLOSED LOOP CONTROL *)
        bSystemReady := TRUE;
        bWarningSlip := bSlipDetectLeft OR bSlipDetectRight;
        
        (* Slip Compensation via Speed Setpoint Derating on Roll/Pitch *)
        IF bSlipDetectLeft THEN
            rTrackLeftSpeedSet := rTrackLeftSpeedSet * 0.5; (* Cut speed demand to regain traction *)
        END_IF;
        IF bSlipDetectRight THEN
            rTrackRightSpeedSet := rTrackRightSpeedSet * 0.5;
        END_IF;

        (* Left Track PID Calculation *)
        rPidErrorLeft := rTrackLeftSpeedSet - rTrackLeftActualSpeed;
        rPidIntegralLeft := rPidIntegralLeft + (rPidErrorLeft * rDt);
        rPidDerivativeLeft := (rPidErrorLeft - rPidPrevErrorLeft) / rDt;
        rControlOutputLeft := (Kp * rPidErrorLeft) + (Ki * rPidIntegralLeft) + (Kd * rPidDerivativeLeft);
        rPidPrevErrorLeft := rPidErrorLeft;

        (* Right Track PID Calculation *)
        rPidErrorRight := rTrackRightSpeedSet - rTrackRightActualSpeed;
        rPidIntegralRight := rPidIntegralRight + (rPidErrorRight * rDt);
        rPidDerivativeRight := (rPidErrorRight - rPidPrevErrorRight) / rDt;
        rControlOutputRight := (Kp * rPidErrorRight) + (Ki * rPidIntegralRight) + (Kd * rPidDerivativeRight);
        rPidPrevErrorRight := rPidErrorRight;

        (* Output saturation limiting *)
        IF rControlOutputLeft > 100.0 THEN
            rControlOutputLeft := 100.0;
            rPidIntegralLeft := rPidIntegralLeft - (rPidErrorLeft * rDt); (* Anti-windup *)
        ELSIF rControlOutputLeft < -100.0 THEN
            rControlOutputLeft := -100.0;
            rPidIntegralLeft := rPidIntegralLeft - (rPidErrorLeft * rDt); (* Anti-windup *)
        END_IF;

        IF rControlOutputRight > 100.0 THEN
            rControlOutputRight := 100.0;
            rPidIntegralRight := rPidIntegralRight - (rPidErrorRight * rDt); (* Anti-windup *)
        ELSIF rControlOutputRight < -100.0 THEN
            rControlOutputRight := -100.0;
            rPidIntegralRight := rPidIntegralRight - (rPidErrorRight * rDt); (* Anti-windup *)
        END_IF;

        IF NOT bEnable THEN
            iState := 0;
            rPidIntegralLeft := 0.0;
            rPidIntegralRight := 0.0;
        END_IF;

    99: (* FAULT LOCKOUT *)
        rControlOutputLeft := 0.0;
        rControlOutputRight := 0.0;
        (* Requires bEmergencyStop cycle to reset *)
        IF bEmergencyStop AND NOT bEnable THEN
            iState := 0;
            bAlarm := FALSE;
        END_IF;

END_CASE;

iCurrentStateCode := iState;

END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
print(f"Saved to {filename}")
