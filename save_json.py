import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Automated Commercial Textile Weaving Loom Warp Tension and Weft Insertion Synchronization**

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_TextileLoom_Sync\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Automated Commercial Textile Weaving Loom Warp Tension and Weft Insertion Synchronization

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_LoomTensionWeftSync
VAR_INPUT
    (* Required: at least 4-8 physical inputs with types and comments *)
    bEnable                 : BOOL;     (* System enable signal *)
    bEmergencyStop          : BOOL;     (* Safety relay OK signal (TRUE = safe) *)
    rWarpTensionRaw         : REAL;     (* Raw warp tension sensor input (N) *)
    rWeftInsertionSpeed     : REAL;     (* Weft insertion target speed (m/s) *)
    rMachineAngle           : REAL;     (* Main drive shaft angle (degrees 0-360) *)
    bWeftBreakDetector      : BOOL;     (* TRUE if weft yarn is broken *)
END_VAR
VAR_OUTPUT
    (* Required: at least 3-6 outputs with types and comments *)
    bSystemReady            : BOOL;     (* System ready status for main control *)
    rTensionMotorTorque     : REAL;     (* Control signal to warp let-off motor (Nm) *)
    bWeftFireSignal         : BOOL;     (* Command to fire weft insertion nozzle/rapier *)
    bAlarm                  : BOOL;     (* Fault alarm output *)
    iFaultCode              : INT;      (* Detailed fault code *)
END_VAR
VAR
    (* Internal State *)
    iState                  : INT := 0;
    
    (* Filtering and PID variables *)
    rTensionFiltered        : REAL := 0.0;
    rTensionSetpoint        : REAL := 250.0; (* N *)
    rTensionError           : REAL := 0.0;
    rIntegral               : REAL := 0.0;
    rDerivative             : REAL := 0.0;
    rPrevError              : REAL := 0.0;
    
    (* Tuning params *)
    Kp                      : REAL := 1.25;
    Ki                      : REAL := 0.05;
    Kd                      : REAL := 0.10;
    
    (* Timers and tracking *)
    tStartupDelay           : TON;
    tCycleTimer             : TON;
    bWeftFired              : BOOL := FALSE;
    rInsertionAngleWindow   : REAL := 85.0; (* Degrees *)
END_VAR

(* === MAIN LOGIC === *)
(* 1. Safety and Interlocks *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bAlarm := TRUE;
    iFaultCode := 99; (* E-Stop active *)
    rTensionMotorTorque := 0.0;
    bWeftFireSignal := FALSE;
    iState := 0;
    RETURN;
END_IF;

IF bWeftBreakDetector THEN
    bSystemReady := FALSE;
    bAlarm := TRUE;
    iFaultCode := 42; (* Weft Break *)
    rTensionMotorTorque := 0.0;
    bWeftFireSignal := FALSE;
    iState := 0;
    RETURN;
END_IF;

(* 2. Input Filtering (Exponential Moving Average for sensor noise) *)
rTensionFiltered := (0.1 * rWarpTensionRaw) + (0.9 * rTensionFiltered);

(* 3. State Machine *)
CASE iState OF
    0: (* IDLE - Await Enable *)
        bSystemReady := FALSE;
        rTensionMotorTorque := 0.0;
        bWeftFireSignal := FALSE;
        bAlarm := FALSE;
        iFaultCode := 0;
        
        IF bEnable THEN
            tStartupDelay(IN := FALSE);
            iState := 10;
        END_IF;

    10: (* STARTUP - Establish Base Tension *)
        tStartupDelay(IN := TRUE, PT := T#3S);
        
        (* Apply open-loop soft start torque to establish tension *)
        rTensionMotorTorque := 50.0; 
        
        IF tStartupDelay.Q THEN
            IF rTensionFiltered > 150.0 THEN
                tStartupDelay(IN := FALSE);
                iState := 20;
            ELSE
                bAlarm := TRUE;
                iFaultCode := 10; (* Failed to establish tension *)
                iState := 0;
            END_IF;
        END_IF;
        
        IF NOT bEnable THEN
            iState := 0;
        END_IF;

    20: (* RUNNING - Synchronized PID Control and Insertion *)
        bSystemReady := TRUE;
        
        (* Active Tension PID Control *)
        rTensionError := rTensionSetpoint - rTensionFiltered;
        rIntegral := rIntegral + rTensionError;
        
        (* Anti-windup *)
        IF rIntegral > 1000.0 THEN rIntegral := 1000.0; END_IF;
        IF rIntegral < -1000.0 THEN rIntegral := -1000.0; END_IF;
        
        rDerivative := rTensionError - rPrevError;
        rPrevError := rTensionError;
        
        rTensionMotorTorque := (Kp * rTensionError) + (Ki * rIntegral) + (Kd * rDerivative) + 100.0; (* Feed-forward base *)
        
        (* Clamp Output Torque *)
        IF rTensionMotorTorque > 400.0 THEN rTensionMotorTorque := 400.0; END_IF;
        IF rTensionMotorTorque < 0.0 THEN rTensionMotorTorque := 0.0; END_IF;
        
        (* Weft Insertion Synchronization based on Main Drive Angle *)
        (* Fire insertion nozzle/rapier only in the specific angle window *)
        IF (rMachineAngle >= rInsertionAngleWindow) AND (rMachineAngle <= (rInsertionAngleWindow + 20.0)) THEN
            IF NOT bWeftFired THEN
                bWeftFireSignal := TRUE;
                bWeftFired := TRUE;
            ELSE
                bWeftFireSignal := FALSE;
            END_IF;
        ELSE
            bWeftFireSignal := FALSE;
        END_IF;
        
        (* Reset weft fired flag for next cycle *)
        IF rMachineAngle > 350.0 THEN
            bWeftFired := FALSE;
        END_IF;

        IF NOT bEnable THEN
            iState := 0;
        END_IF;
        
    ELSE
        iState := 0;
END_CASE;

END_FUNCTION_BLOCK
```"""

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": code}
    ]
}

os.makedirs(r"C:\Users\majip\Downloads\LLM REASEARCH\data\swarm_raw", exist_ok=True)
filename = f"C:\\Users\\majip\\Downloads\\LLM REASEARCH\\data\\swarm_raw\\agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print(f"Saved to {filename}")
