import json, uuid, os
prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Automated High-Speed Beverage Bottling Line Filler Valve and Capper Synchronization**

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_BeverageBottling_Sync\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Automated High-Speed Beverage Bottling Line Filler Valve and Capper Synchronization

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_BeverageBottling_Sync
VAR_INPUT
    bSystemEnable       : BOOL;     (* Main line enable from supervisory control *)
    bEStop_OK           : BOOL;     (* Emergency stop circuit healthy and reset *)
    rLineSpeedCmd       : REAL;     (* Requested line speed in bottles per minute (BPM) *)
    bBottlePresent      : BOOL;     (* Optical sensor indicating bottle under filler valve *)
    rFillLevelCmd       : REAL;     (* Target fill volume in ml *)
    rFlowMeter          : REAL;     (* Instantaneous flow rate from Coriolis meter in ml/s *)
    bCapperReady        : BOOL;     (* Capper station ready flag for synchronization *)
    rCapperTorque_FB    : REAL;     (* Feedback torque from capper servo in Nm *)
END_VAR
VAR_OUTPUT
    bSystemReady        : BOOL;     (* Overall subsystem ready flag to master *)
    rValvePosCmd        : REAL;     (* Filler valve position command 0-100% *)
    rCapperSpeedRef     : REAL;     (* Capper synchronization speed reference in RPM *)
    bFaultActive        : BOOL;     (* Critical fault active indicator *)
    iFaultCode          : INT;      (* Diagnostics fault code (0 = no fault) *)
    bBottleFilled       : BOOL;     (* Handshake signal to indexing conveyor to move *)
END_VAR
VAR
    iState              : INT := 0;
    rCurrentVolume      : REAL := 0.0;
    tFillTimer          : TON;
    tDripTimer          : TON;
    tFaultTimer         : TON;
    rFlowFilt           : REAL;
    tFilter             : REAL := 0.1; (* 100ms first order low pass coefficient *)
    rPrevFlow           : REAL;
END_VAR

(* === SAFETY & INTERLOCKS === *)
IF NOT bEStop_OK THEN
    bSystemReady := FALSE;
    rValvePosCmd := 0.0;
    rCapperSpeedRef := 0.0;
    bFaultActive := TRUE;
    iFaultCode := 99; (* E-Stop Pressed *)
    iState := 0;
    RETURN;
END_IF;

(* First-order low-pass filter for flow meter to mitigate sensor noise *)
rFlowFilt := (tFilter * rFlowFilt) + ((1.0 - tFilter) * rFlowMeter);

CASE iState OF
    0: (* INIT *)
        bSystemReady := FALSE;
        rValvePosCmd := 0.0;
        bBottleFilled := FALSE;
        IF bSystemEnable AND bCapperReady THEN
            bSystemReady := TRUE;
            bFaultActive := FALSE;
            iFaultCode := 0;
            iState := 10;
        END_IF;

    10: (* WAIT_FOR_BOTTLE *)
        rCurrentVolume := 0.0;
        bBottleFilled := FALSE;
        IF bBottlePresent AND bCapperReady THEN
            iState := 20;
        END_IF;

    20: (* FAST_FILL *)
        rValvePosCmd := 100.0; (* Open valve fully to maximize throughput *)
        rCurrentVolume := rCurrentVolume + (rFlowFilt * 0.01); (* Assume 10ms task cycle for integration *)
        
        IF rCurrentVolume >= (rFillLevelCmd * 0.85) THEN
            iState := 30; (* Switch to fine fill to avoid splashing and foaming *)
        END_IF;

    30: (* FINE_FILL *)
        rValvePosCmd := 20.0; (* Throttle valve to 20% for precision volume control *)
        rCurrentVolume := rCurrentVolume + (rFlowFilt * 0.01);
        
        IF rCurrentVolume >= rFillLevelCmd THEN
            rValvePosCmd := 0.0;
            tDripTimer(IN := TRUE, PT := T#200MS);
            IF tDripTimer.Q THEN
                tDripTimer(IN := FALSE);
                iState := 40;
            END_IF;
        END_IF;

    40: (* SYNC_TO_CAPPER *)
        bBottleFilled := TRUE;
        (* Dynamically compute capper speed ref based on line speed and torque margin *)
        IF rCapperTorque_FB < 5.0 THEN
            rCapperSpeedRef := rLineSpeedCmd * 1.05; (* Slight overspeed to catch up and engage cap *)
        ELSE
            rCapperSpeedRef := rLineSpeedCmd; (* Run at synchronized line speed *)
        END_IF;

        IF NOT bBottlePresent THEN
            iState := 10; (* Bottle moved to capper, wait for next index *)
        END_IF;

    ELSE
        (* Fault Catch-all *)
        bFaultActive := TRUE;
        iFaultCode := 500;
        iState := 0;
END_CASE;

END_FUNCTION_BLOCK
```"""
os.makedirs('data/swarm_raw', exist_ok=True)
record = {'messages': [{'role': 'user', 'content': prompt}, {'role': 'assistant', 'content': code}]}
with open(f'data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json', 'w', encoding='utf-8') as f:
    json.dump(record, f, ensure_ascii=False)
