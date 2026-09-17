import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Automated Commercial Ship Ballast Water Treatment System (BWTS) UV Sterilization and Filtration**

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_BWTS_Control\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Automated Commercial Ship Ballast Water Treatment System (BWTS) UV Sterilization and Filtration

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_BWTS_Control
VAR_INPUT
    (* Required: at least 4-8 physical inputs with types and comments *)
    bEnable         : BOOL;     (* System enable signal *)
    bEmergencyStop  : BOOL;     (* Safety relay OK signal (Normally Closed) *)
    rFlowRate       : REAL;     (* Ballast water flow rate (m3/h) *)
    rUVDoseSetpoint : REAL;     (* Target UV dose (mJ/cm2) *)
    rUVIntensity    : REAL;     (* Measured UV intensity (W/m2) *)
    rTurbidity      : REAL;     (* Water turbidity (NTU) *)
    bFilterPressureOk : BOOL;   (* Filter differential pressure switch (True = OK) *)
    bValvesAligned  : BOOL;     (* All system valves in correct position for operation *)
END_VAR
VAR_OUTPUT
    (* Required: at least 3-6 outputs with types and comments *)
    bSystemReady    : BOOL;     (* System ready status for ship control system *)
    rUVPowerControl : REAL;     (* Control signal to UV lamp electronic ballasts (0-100%) *)
    bValveOpenCmd   : BOOL;     (* Command to open main inlet and outlet valves *)
    bBackwashCmd    : BOOL;     (* Command to initiate automatic filter backwash cycle *)
    bAlarm          : BOOL;     (* Fault alarm output to ship alarm system *)
    iErrorCode      : INT;      (* Specific error code for detailed diagnostics *)
END_VAR
VAR
    (* Internal state variables *)
    iState          : INT := 0;
    tStartTimer     : TON;
    tBackwashTimer  : TON;
    tUVWarmupTimer  : TON;
    rCalculatedDose : REAL;
    rFilteredFlow   : REAL;
    rFlowFilterAlpha: REAL := 0.05; (* Low pass filter alpha for smoothing flow sensor noise *)
    bUVReady        : BOOL := FALSE;
    bBackwashReq    : BOOL := FALSE;
END_VAR

(* === MAIN LOGIC === *)
(* Emergency Stop Interlock - Highest Priority *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bValveOpenCmd := FALSE;
    rUVPowerControl := 0.0;
    bBackwashCmd := FALSE;
    bAlarm := TRUE;
    iErrorCode := 99; (* Emergency stop active *)
    iState := 0;
    RETURN;
END_IF;

(* Input Filtering - First order Low Pass Filter on Flow Rate to remove sensor noise and fluid dynamics spikes *)
rFilteredFlow := (rFlowFilterAlpha * rFlowRate) + ((1.0 - rFlowFilterAlpha) * rFilteredFlow);

(* Calculate Actual Applied UV Dose dynamically *)
(* Formula approximation: Dose = (Intensity * Time) / Flow Area equivalent *)
IF rFilteredFlow > 5.0 THEN
    (* Avoid division by zero, scale factor applies to specific reactor chamber geometry *)
    rCalculatedDose := (rUVIntensity * 3600.0 * 0.85) / rFilteredFlow;
ELSE
    rCalculatedDose := 0.0;
END_IF;

(* Main State Machine *)
CASE iState OF
    0: (* STATE 0: IDLE AND STANDBY *)
        bSystemReady := FALSE;
        rUVPowerControl := 0.0;
        bValveOpenCmd := FALSE;
        bBackwashCmd := FALSE;
        bUVReady := FALSE;
        
        IF bEnable AND bValvesAligned THEN
            iErrorCode := 0;
            bAlarm := FALSE;
            iState := 10;
        ELSIF bEnable AND NOT bValvesAligned THEN
            bAlarm := TRUE;
            iErrorCode := 1; (* Valves not aligned properly for startup *)
        END_IF;

    10: (* STATE 10: WARMUP UV REACTORS *)
        rUVPowerControl := 100.0; (* Full power to strike and warmup lamps quickly *)
        tUVWarmupTimer(IN := TRUE, PT := T#45S);
        
        IF tUVWarmupTimer.Q AND (rUVIntensity > 55.0) THEN
            tUVWarmupTimer(IN := FALSE);
            bUVReady := TRUE;
            iState := 20;
        ELSIF tUVWarmupTimer.Q THEN
            (* Failed to reach minimum operational intensity within time window *)
            tUVWarmupTimer(IN := FALSE);
            bAlarm := TRUE;
            iErrorCode := 2; (* UV Warmup failed, check lamp health or sleeve fouling *)
            iState := 0;
        END_IF;

    20: (* STATE 20: RUNNING / DOSING CONTROL *)
        bSystemReady := TRUE;
        bValveOpenCmd := TRUE;
        
        (* Proportional Control Loop for UV Power based on Dose Setpoint Tracking *)
        IF rCalculatedDose < rUVDoseSetpoint THEN
            (* Increase power gently to avoid electrical stress *)
            rUVPowerControl := MIN(rUVPowerControl + 0.5, 100.0);
        ELSIF rCalculatedDose > (rUVDoseSetpoint + 15.0) THEN
            (* Reduce power to save energy if over-dosing, but maintain minimum striking voltage *)
            rUVPowerControl := MAX(rUVPowerControl - 0.5, 30.0);
        END_IF;
        
        (* Continuous Filter Monitoring and Backwash Triggering *)
        IF NOT bFilterPressureOk OR rTurbidity > 35.0 THEN
            bBackwashReq := TRUE;
        END_IF;
        
        IF bBackwashReq THEN
            iState := 30; (* Transition to Initiate Backwash *)
        END_IF;
        
        IF NOT bEnable THEN
            bValveOpenCmd := FALSE;
            iState := 40; (* Transition to Shutdown and Cool down *)
        END_IF;

    30: (* STATE 30: FILTER BACKWASH SEQUENCE *)
        bBackwashCmd := TRUE;
        bValveOpenCmd := FALSE; (* Isolate main flow during backwash cycle to maximize back-pressure *)
        rUVPowerControl := 30.0; (* Drop to minimum power during zero flow to prevent overheating *)
        
        tBackwashTimer(IN := TRUE, PT := T#25S);
        
        IF tBackwashTimer.Q THEN
            tBackwashTimer(IN := FALSE);
            bBackwashCmd := FALSE;
            bBackwashReq := FALSE;
            IF bFilterPressureOk THEN
                iState := 20; (* Return to main run state *)
            ELSE
                bAlarm := TRUE;
                iErrorCode := 3; (* Backwash failed to clear filter obstruction *)
                iState := 40; (* Go to safe shutdown *)
            END_IF;
        END_IF;

    40: (* STATE 40: SHUTDOWN COOLING CYCLE *)
        bSystemReady := FALSE;
        rUVPowerControl := 30.0; (* Low power for controlled lamp cooling down *)
        bValveOpenCmd := TRUE; (* Keep water flowing briefly to remove residual heat *)
        tStartTimer(IN := TRUE, PT := T#30S);
        
        IF tStartTimer.Q THEN
            tStartTimer(IN := FALSE);
            rUVPowerControl := 0.0;
            bValveOpenCmd := FALSE;
            iState := 0;
        END_IF;

END_CASE;

END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
print(f"Saved to {filename}")
