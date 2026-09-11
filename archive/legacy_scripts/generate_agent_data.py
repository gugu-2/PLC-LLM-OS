import os
os.makedirs("data/swarm_raw", exist_ok=True)
import json, uuid

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Next-Gen Subsea Multiphase Hydrocyclone Desander**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Crude oil / water / sand vortex flow separation mapping, differential pressure core extraction throttling, and abrasive wear acoustic signature detection). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\nFUNCTION_BLOCK FB_SubseaHydrocyclone_Desander\n//...\nEND_FUNCTION_BLOCK\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Next-Gen Subsea Multiphase Hydrocyclone Desander

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_Subsea_Multiphase_Hydrocyclone_Desander
VAR_INPUT
    (* Required: at least 4-8 physical inputs with types and comments *)
    bEnable                 : BOOL;     (* System enable signal *)
    bEmergencyStop          : BOOL;     (* Safety relay OK signal - active low for failsafe operation *)
    rInletPressure          : REAL;     (* Inlet multiphase fluid pressure (bar) *)
    rOverflowPressure       : REAL;     (* Clean fluid overflow pressure (bar) *)
    rUnderflowPressure      : REAL;     (* Sand slurry underflow pressure (bar) *)
    rAcousticWearSignal     : REAL;     (* Acoustic sensor reading for apex wear monitoring (mV) *)
    rVortexCoreTemp         : REAL;     (* Temperature at vortex core to ensure no hydrate formation (deg C) *)
    bFlushRequest           : BOOL;     (* Operator manual flush request *)
END_VAR
VAR_OUTPUT
    (* Required: at least 3-6 outputs with types and comments *)
    bSystemReady            : BOOL;     (* System ready status indicator *)
    bAlarm                  : BOOL;     (* Fault alarm output to SCADA *)
    rThrottleValveCmd       : REAL;     (* Overflow throttle valve command 0-100% *)
    rUnderflowValveCmd      : REAL;     (* Underflow extraction valve command 0-100% *)
    iStateOut               : INT;      (* Current state representation for HMI display *)
END_VAR
VAR
    (* Internal state variables *)
    iState                  : INT := 0;
    tTimer                  : TON;
    rDeltaP                 : REAL;     (* Differential pressure calculation *)
    rFilteredAcoustic       : REAL := 0.0; (* Filtered acoustic wear signal *)
    rWearThreshold          : REAL := 850.0; (* Acoustic wear warning threshold *)
END_VAR

(* === MAIN LOGIC === *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bAlarm := TRUE;
    rThrottleValveCmd := 0.0;
    rUnderflowValveCmd := 0.0;
    iState := 99; (* EMERGENCY STOP STATE *)
    RETURN;
END_IF;

(* Exponential moving average filter for acoustic wear sensor to filter out multiphase flow noise *)
rFilteredAcoustic := (rFilteredAcoustic * 0.95) + (rAcousticWearSignal * 0.05);

(* Differential Pressure Calculation across hydrocyclone *)
rDeltaP := rInletPressure - rOverflowPressure;

CASE iState OF
    0: (* IDLE *)
        bSystemReady := TRUE;
        bAlarm := FALSE;
        rThrottleValveCmd := 0.0;
        rUnderflowValveCmd := 0.0;
        IF bEnable THEN
            iState := 10;
        END_IF;

    10: (* RAMP UP / INITIALIZATION *)
        bSystemReady := FALSE;
        (* Slowly open overflow valve to establish vortex core *)
        rThrottleValveCmd := rThrottleValveCmd + 0.5; 
        IF rThrottleValveCmd >= 40.0 THEN
            iState := 20;
        END_IF;

    20: (* STEADY STATE SEPARATION *)
        (* Maintain optimal differential pressure for maximum centrifugal separation *)
        IF rDeltaP > 50.0 THEN
            rThrottleValveCmd := rThrottleValveCmd + 0.1;
        ELSIF rDeltaP < 45.0 THEN
            rThrottleValveCmd := rThrottleValveCmd - 0.1;
        END_IF;

        (* Clamp throttle command strictly between 0 and 100 percent limits *)
        IF rThrottleValveCmd > 100.0 THEN rThrottleValveCmd := 100.0; END_IF;
        IF rThrottleValveCmd < 0.0 THEN rThrottleValveCmd := 0.0; END_IF;

        (* Regulate underflow to extract sand based on pressure ratio constraints *)
        IF (rInletPressure - rUnderflowPressure) > 70.0 THEN
            rUnderflowValveCmd := 30.0;
        ELSE
            rUnderflowValveCmd := 10.0;
        END_IF;

        (* Check for severe wear via acoustic signature over limit *)
        IF rFilteredAcoustic > rWearThreshold THEN
            bAlarm := TRUE;
            iState := 30; (* INITIATE SAFE SHUTDOWN *)
        END_IF;

        IF bFlushRequest THEN
            iState := 40; (* ENTER FLUSH ROUTINE *)
        END_IF;

        IF NOT bEnable THEN
            iState := 30; (* NORMAL SHUTDOWN PROGRESSION *)
        END_IF;

    30: (* SHUTDOWN SEQUENCE *)
        rThrottleValveCmd := rThrottleValveCmd - 1.0;
        rUnderflowValveCmd := rUnderflowValveCmd - 1.0;
        IF rThrottleValveCmd <= 0.0 AND rUnderflowValveCmd <= 0.0 THEN
            rThrottleValveCmd := 0.0;
            rUnderflowValveCmd := 0.0;
            iState := 0;
        END_IF;

    40: (* AUTOMATED FLUSH CYCLE *)
        rUnderflowValveCmd := 100.0; (* Full open to flush accumulated sand out *)
        tTimer(IN := TRUE, PT := T#15S);
        IF tTimer.Q THEN
            tTimer(IN := FALSE);
            iState := 20; (* Return to steady state *)
        END_IF;
        
    99: (* EMERGENCY STOP RECOVERY *)
        (* Wait for E-Stop reset mechanism *)
        IF bEmergencyStop THEN
            iState := 0;
        END_IF;

END_CASE;

iStateOut := iState;

END_FUNCTION_BLOCK
```"""

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": code}
    ]
}

filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print(f"Saved to {filename}")
