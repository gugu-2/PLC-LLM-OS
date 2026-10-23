import json
import uuid
import os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Industrial Wire Drawing Multi-Draft Tension and Spooling Synchronization**

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_WireDrawing_Tension\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Industrial Wire Drawing Multi-Draft Tension and Spooling Synchronization

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_WireDrawing_MultiDraftSync
VAR_INPUT
    bEnable                 : BOOL;     (* System master enable signal *)
    bEmergencyStopOk        : BOOL;     (* Safety relay OK signal, active high *)
    bLineRampUp             : BOOL;     (* Command to start acceleration ramp *)
    rMasterSpeedSet         : REAL;     (* Master line speed setpoint (m/min) *)
    rActTensionDancer1      : REAL;     (* Feedback from draft 1 dancer (0-100%) *)
    rActTensionDancer2      : REAL;     (* Feedback from draft 2 dancer (0-100%) *)
    rActSpoolDiameter       : REAL;     (* Calculated or measured spool diameter (mm) *)
    rMotorTempCapstan1      : REAL;     (* Capstan 1 motor temperature (deg C) *)
END_VAR
VAR_OUTPUT
    bSystemReady            : BOOL;     (* System ready for operation *)
    rSpeedRefCapstan1       : REAL;     (* Speed reference for Capstan 1 (rpm) *)
    rSpeedRefCapstan2       : REAL;     (* Speed reference for Capstan 2 (rpm) *)
    rSpeedRefSpooler        : REAL;     (* Speed reference for Spooler (rpm) *)
    bTensionAlarm           : BOOL;     (* High tension deviation or break detected *)
    bThermalWarning         : BOOL;     (* Drive thermal warning threshold exceeded *)
END_VAR
VAR
    iState                  : INT := 0; (* Main state machine index *)
    tStartupDelay           : TON;      (* Delay before engaging drives *)
    tDriveFaultDbnc         : TON;      (* Debounce for thermal warnings *)
    
    (* Internal PID variables for Dancer 1 *)
    rTensionErr1            : REAL;
    rTensionInt1            : REAL := 0.0;
    rTensionDeriv1          : REAL;
    rLastErr1               : REAL := 0.0;
    rKp1                    : REAL := 1.25;
    rKi1                    : REAL := 0.05;
    rKd1                    : REAL := 0.1;
    
    (* Internal PID variables for Dancer 2 *)
    rTensionErr2            : REAL;
    rTensionInt2            : REAL := 0.0;
    
    rCurrentMasterSpeed     : REAL := 0.0;
    rRampRate               : REAL := 5.0; (* m/min per cycle *)
    
    bInitDone               : BOOL := FALSE;
END_VAR

(* === MAIN LOGIC === *)
(* Emergency Stop and Safety Interlocks *)
IF NOT bEmergencyStopOk THEN
    bSystemReady := FALSE;
    bTensionAlarm := TRUE;
    rSpeedRefCapstan1 := 0.0;
    rSpeedRefCapstan2 := 0.0;
    rSpeedRefSpooler := 0.0;
    iState := 0;
    RETURN;
END_IF;

(* Filter thermal sensor and trigger warning *)
tDriveFaultDbnc(IN := rMotorTempCapstan1 > 85.0, PT := T#2S);
bThermalWarning := tDriveFaultDbnc.Q;

CASE iState OF
    0: (* IDLE *)
        bSystemReady := FALSE;
        rCurrentMasterSpeed := 0.0;
        rSpeedRefCapstan1 := 0.0;
        rSpeedRefCapstan2 := 0.0;
        rSpeedRefSpooler := 0.0;
        
        IF bEnable THEN
            tStartupDelay(IN := TRUE, PT := T#1S);
            IF tStartupDelay.Q THEN
                bSystemReady := TRUE;
                tStartupDelay(IN := FALSE);
                iState := 10;
            END_IF;
        ELSE
            tStartupDelay(IN := FALSE);
        END_IF;

    10: (* READY / HOLD *)
        IF bLineRampUp AND bEnable THEN
            iState := 20;
        END_IF;
        IF NOT bEnable THEN
            iState := 0;
        END_IF;

    20: (* RAMP UP & RUNNING *)
        (* Master speed ramp generator *)
        IF rCurrentMasterSpeed < rMasterSpeedSet THEN
            rCurrentMasterSpeed := rCurrentMasterSpeed + rRampRate;
            IF rCurrentMasterSpeed > rMasterSpeedSet THEN
                rCurrentMasterSpeed := rMasterSpeedSet;
            END_IF;
        ELSIF rCurrentMasterSpeed > rMasterSpeedSet THEN
            rCurrentMasterSpeed := rCurrentMasterSpeed - rRampRate;
            IF rCurrentMasterSpeed < rMasterSpeedSet THEN
                rCurrentMasterSpeed := rMasterSpeedSet;
            END_IF;
        END_IF;
        
        (* Dancer 1 PID Calculation - Position setpoint typically 50% *)
        rTensionErr1 := 50.0 - rActTensionDancer1;
        rTensionInt1 := rTensionInt1 + rTensionErr1;
        (* Anti-windup *)
        IF rTensionInt1 > 100.0 THEN rTensionInt1 := 100.0; END_IF;
        IF rTensionInt1 < -100.0 THEN rTensionInt1 := -100.0; END_IF;
        
        rTensionDeriv1 := rTensionErr1 - rLastErr1;
        rLastErr1 := rTensionErr1;
        
        (* Capstan 1 speed trim *)
        rSpeedRefCapstan1 := rCurrentMasterSpeed * 10.0 + (rTensionErr1 * rKp1 + rTensionInt1 * rKi1 + rTensionDeriv1 * rKd1);
        
        (* Capstan 2 and Spooler logic *)
        rTensionErr2 := 50.0 - rActTensionDancer2;
        rSpeedRefCapstan2 := rCurrentMasterSpeed * 11.5 + (rTensionErr2 * rKp1); (* Simplified P control for Draft 2 *)
        
        (* Spooler diameter compensation *)
        IF rActSpoolDiameter > 10.0 THEN
            rSpeedRefSpooler := (rCurrentMasterSpeed * 1000.0) / (3.14159 * rActSpoolDiameter);
        ELSE
            rSpeedRefSpooler := 0.0;
        END_IF;
        
        (* Break detection *)
        IF rActTensionDancer1 < 5.0 OR rActTensionDancer2 < 5.0 THEN
            bTensionAlarm := TRUE;
            iState := 30; (* FAULT / FAST STOP *)
        END_IF;

        IF NOT bLineRampUp THEN
            iState := 10;
            rCurrentMasterSpeed := 0.0;
        END_IF;
        
    30: (* FAULT / FAST STOP *)
        rSpeedRefCapstan1 := 0.0;
        rSpeedRefCapstan2 := 0.0;
        rSpeedRefSpooler := 0.0;
        bSystemReady := FALSE;
        IF NOT bEnable THEN
            bTensionAlarm := FALSE;
            iState := 0;
        END_IF;

END_CASE;

END_FUNCTION_BLOCK
```"""

os.makedirs(os.path.join(os.getcwd(), "data", "swarm_raw"), exist_ok=True)
filename = os.path.join(os.getcwd(), "data", "swarm_raw", f"agent_{uuid.uuid4().hex[:8]}.json")
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
print(f"Saved to {filename}")
