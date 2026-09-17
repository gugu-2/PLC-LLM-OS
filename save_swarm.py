import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Commercial Printing Press High-Speed Web Tension and Color Registration**

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_PrintingPress_WebTension\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Commercial Printing Press High-Speed Web Tension and Color Registration

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_PrintingPress_WebTension
VAR_INPUT
    (* Required: at least 4-8 physical inputs with types and comments *)
    bEnable                 : BOOL;     (* System enable signal *)
    bEmergencyStop          : BOOL;     (* Safety relay OK signal (TRUE = OK) *)
    rWebSpeedActual         : REAL;     (* Current web speed in m/min *)
    rWebSpeedSetpoint       : REAL;     (* Target web speed in m/min *)
    rTensionSensorFront     : REAL;     (* Front tension sensor reading in N *)
    rTensionSensorRear      : REAL;     (* Rear tension sensor reading in N *)
    rColorRegMarkError      : REAL;     (* Vision system color registration error in mm *)
    bSpliceApproaching      : BOOL;     (* True if a paper splice is approaching the nip *)
END_VAR
VAR_OUTPUT
    (* Required: at least 3-6 outputs with types and comments *)
    bSystemReady            : BOOL;     (* System ready status *)
    rTensionControlOut      : REAL;     (* Tension servo torque/speed trim command (-100 to 100%) *)
    rColorRegCorrectionOut  : REAL;     (* Color registration compensator stepper command *)
    bAlarm                  : BOOL;     (* Fault alarm output *)
    bWebBreakDetected       : BOOL;     (* Web break fault triggered *)
    bWarning                : BOOL;     (* Non-critical warning (e.g., tension tracking error) *)
END_VAR
VAR
    (* Internal state variables *)
    iState                  : INT := 0;
    tTimer                  : TON;
    tSpliceTimer            : TON;
    rFilteredTension        : REAL := 0.0;
    rTensionError           : REAL := 0.0;
    rTensionIntegral        : REAL := 0.0;
    rTensionDerivative      : REAL := 0.0;
    rTensionPrevError       : REAL := 0.0;
    rTensionKp              : REAL := 2.5;
    rTensionKi              : REAL := 0.15;
    rTensionKd              : REAL := 0.05;
    
    rColorRegIntegral       : REAL := 0.0;
    
    (* Filter Constants *)
    rAlpha                  : REAL := 0.2; (* Low pass filter coefficient for tension noise *)
    
    (* Safety limits *)
    rMaxTension             : REAL := 500.0; (* N *)
    rMinTension             : REAL := 50.0;  (* N *)
    rWebBreakThreshold      : REAL := 20.0;  (* N *)
END_VAR

(* === MAIN LOGIC === *)

(* Emergency Stop Interlock *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bAlarm := TRUE;
    rTensionControlOut := 0.0;
    rColorRegCorrectionOut := 0.0;
    iState := 999; (* Fault state *)
    RETURN;
END_IF;

(* Sensor Noise Filtering (First-Order Low Pass) *)
rFilteredTension := (rAlpha * ((rTensionSensorFront + rTensionSensorRear) / 2.0)) + ((1.0 - rAlpha) * rFilteredTension);

(* Web Break Detection *)
IF (iState = 20) AND (rFilteredTension < rWebBreakThreshold) AND (rWebSpeedActual > 10.0) THEN
    bWebBreakDetected := TRUE;
    bAlarm := TRUE;
    iState := 999; (* Drop to fault on web break *)
END_IF;

CASE iState OF
    0: (* IDLE *)
        bSystemReady := FALSE;
        rTensionControlOut := 0.0;
        rColorRegCorrectionOut := 0.0;
        rTensionIntegral := 0.0;
        rColorRegIntegral := 0.0;
        IF bEnable AND bEmergencyStop THEN
            iState := 10;
        END_IF;

    10: (* RAMP UP / INITIALIZATION *)
        bSystemReady := TRUE;
        (* Apply initial pre-tension before high-speed run *)
        rTensionControlOut := 15.0; 
        tTimer(IN := TRUE, PT := T#3S);
        IF tTimer.Q THEN
            tTimer(IN := FALSE);
            iState := 20;
        END_IF;

    20: (* RUNNING (PID TENSION CONTROL & REGISTRATION) *)
        bSystemReady := TRUE;
        
        (* Tension PID Control *)
        rTensionError := (rMaxTension / 2.0) - rFilteredTension; (* Target is mid-range tension *)
        rTensionIntegral := rTensionIntegral + rTensionError;
        
        (* Anti-windup for tension integral *)
        IF rTensionIntegral > 1000.0 THEN rTensionIntegral := 1000.0; END_IF;
        IF rTensionIntegral < -1000.0 THEN rTensionIntegral := -1000.0; END_IF;
        
        rTensionDerivative := rTensionError - rTensionPrevError;
        rTensionControlOut := (rTensionKp * rTensionError) + (rTensionKi * rTensionIntegral) + (rTensionKd * rTensionDerivative);
        rTensionPrevError := rTensionError;
        
        (* Clamp Output (-100% to 100%) *)
        IF rTensionControlOut > 100.0 THEN rTensionControlOut := 100.0; END_IF;
        IF rTensionControlOut < -100.0 THEN rTensionControlOut := -100.0; END_IF;

        (* Color Registration PI Control (only active when speed is stable) *)
        IF ABS(rWebSpeedActual - rWebSpeedSetpoint) < 5.0 THEN
            rColorRegIntegral := rColorRegIntegral + rColorRegMarkError;
            rColorRegCorrectionOut := (rColorRegMarkError * 1.2) + (rColorRegIntegral * 0.05);
        ELSE
            rColorRegCorrectionOut := 0.0; (* Suspend color reg correction during speed transients *)
        END_IF;

        (* Splice handling (temporary tension drop to prevent breaks at splice tape) *)
        IF bSpliceApproaching THEN
            rTensionControlOut := rTensionControlOut * 0.8; (* Reduce tension by 20% *)
            bWarning := TRUE;
        ELSE
            bWarning := FALSE;
        END_IF;
        
        IF NOT bEnable THEN
            iState := 0;
        END_IF;

    999: (* FAULT STATE *)
        bSystemReady := FALSE;
        rTensionControlOut := 0.0;
        rColorRegCorrectionOut := 0.0;
        (* Requires bEnable to be toggled off to reset, assuming E-Stop is clear *)
        IF NOT bEnable AND bEmergencyStop AND NOT bWebBreakDetected THEN
            bAlarm := FALSE;
            iState := 0;
        END_IF;
        
END_CASE;

END_FUNCTION_BLOCK
```"""

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": code}
    ]
}

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print(f"Saved to {filename}")
