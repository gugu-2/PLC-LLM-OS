import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Advanced Semiconductor Chemical Mechanical Polishing (CMP) Slurry Flow and Platen Downforce**

Task: Invent a highly complex, ultra-realistic control scenario for this domain. Make this code EVEN BETTER, MORE ADVANCED, and MORE RIGOROUS than previous iterations. Include extreme edge-case handling, advanced math, and robust fault-tolerance.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_Semi_CMP_Polishing\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Advanced Semiconductor Chemical Mechanical Polishing (CMP) Slurry Flow and Platen Downforce

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_AdvancedCMP_Controller
VAR_INPUT
    bEnable               : BOOL;   (* System enable command *)
    bEmergencyStop        : BOOL;   (* Safety E-Stop signal (Active LOW) *)
    rWaferThickness       : REAL;   (* In-situ metrology: Remaining thickness (nm) *)
    rSlurryFlowTarget     : REAL;   (* Desired slurry flow rate (ml/min) *)
    rPlatenDownforceTarget: REAL;   (* Desired downforce pressure (kPa) *)
    rActualSlurryFlow     : REAL;   (* Sensor feedback: Slurry flow (ml/min) *)
    rActualPlatenDownforce: REAL;   (* Sensor feedback: Platen pressure (kPa) *)
    rPlatenSpeed          : REAL;   (* Platen rotation speed (RPM) *)
    bPadConditionerOK     : BOOL;   (* Pad conditioner status OK *)
END_VAR
VAR_OUTPUT
    bSystemReady          : BOOL;   (* CMP system ready for polishing *)
    rCmdSlurryValve       : REAL;   (* Control signal to slurry proportional valve (0-100%) *)
    rCmdDownforceValve    : REAL;   (* Control signal to downforce servo pneumatic valve (0-100%) *)
    bProcessComplete      : BOOL;   (* End-point detection flag *)
    bAlarm                : BOOL;   (* General fault/alarm output *)
    iErrorCode            : INT;    (* Diagnostic error code *)
END_VAR
VAR
    iState                : INT := 0; (* Internal state machine *)
    rSlurryError          : REAL;
    rSlurryIntegral       : REAL := 0.0;
    rDownforceError       : REAL;
    rDownforceIntegral    : REAL := 0.0;
    tProcessTimer         : TON;
    tStabilizationTimer   : TON;
    rTargetThickness      : REAL := 15.0; (* Target endpoint thickness nm *)
    
    Kp_Slurry             : REAL := 1.25;
    Ki_Slurry             : REAL := 0.15;
    Kp_Force              : REAL := 2.50;
    Ki_Force              : REAL := 0.45;
END_VAR

(* === MAIN SAFETY AND INTERLOCKS === *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    rCmdSlurryValve := 0.0;
    rCmdDownforceValve := 0.0;
    bAlarm := TRUE;
    iErrorCode := 999; (* Critical E-Stop *)
    iState := 0;
    RETURN;
END_IF;

IF NOT bPadConditionerOK AND iState > 10 THEN
    bAlarm := TRUE;
    iErrorCode := 101; (* Pad conditioning failure during process *)
    iState := 900; (* Abort state *)
END_IF;

(* === STATE MACHINE === *)
CASE iState OF
    0: (* IDLE *)
        bSystemReady := TRUE;
        bProcessComplete := FALSE;
        rCmdSlurryValve := 0.0;
        rCmdDownforceValve := 0.0;
        rSlurryIntegral := 0.0;
        rDownforceIntegral := 0.0;
        bAlarm := FALSE;
        iErrorCode := 0;
        
        IF bEnable AND rWaferThickness > rTargetThickness THEN
            iState := 10;
        END_IF;

    10: (* SLURRY PRE-WETTING & STABILIZATION *)
        bSystemReady := FALSE;
        
        (* PI Control for Slurry Flow *)
        rSlurryError := rSlurryFlowTarget - rActualSlurryFlow;
        rSlurryIntegral := rSlurryIntegral + (rSlurryError * 0.1); (* Assuming 100ms cycle *)
        
        (* Anti-windup *)
        IF rSlurryIntegral > 50.0 THEN rSlurryIntegral := 50.0; END_IF;
        IF rSlurryIntegral < -50.0 THEN rSlurryIntegral := -50.0; END_IF;
        
        rCmdSlurryValve := (Kp_Slurry * rSlurryError) + (Ki_Slurry * rSlurryIntegral);
        
        (* Saturate output 0-100% *)
        IF rCmdSlurryValve > 100.0 THEN rCmdSlurryValve := 100.0; END_IF;
        IF rCmdSlurryValve < 0.0 THEN rCmdSlurryValve := 0.0; END_IF;
        
        tStabilizationTimer(IN := TRUE, PT := T#3S);
        IF tStabilizationTimer.Q THEN
            tStabilizationTimer(IN := FALSE);
            IF ABS(rSlurryError) < (rSlurryFlowTarget * 0.05) THEN
                iState := 20; (* Slurry stabilized, proceed to downforce application *)
            ELSE
                bAlarm := TRUE;
                iErrorCode := 201; (* Slurry flow unstable *)
                iState := 900;
            END_IF;
        END_IF;

    20: (* PLATEN DOWNFORCE APPLICATION & ACTIVE POLISHING *)
        (* Maintain Slurry Flow Control *)
        rSlurryError := rSlurryFlowTarget - rActualSlurryFlow;
        rSlurryIntegral := rSlurryIntegral + (rSlurryError * 0.1);
        rCmdSlurryValve := (Kp_Slurry * rSlurryError) + (Ki_Slurry * rSlurryIntegral);
        IF rCmdSlurryValve > 100.0 THEN rCmdSlurryValve := 100.0; END_IF;
        IF rCmdSlurryValve < 0.0 THEN rCmdSlurryValve := 0.0; END_IF;

        (* PI Control for Downforce *)
        rDownforceError := rPlatenDownforceTarget - rActualPlatenDownforce;
        rDownforceIntegral := rDownforceIntegral + (rDownforceError * 0.1);
        
        (* Anti-windup *)
        IF rDownforceIntegral > 80.0 THEN rDownforceIntegral := 80.0; END_IF;
        IF rDownforceIntegral < -80.0 THEN rDownforceIntegral := -80.0; END_IF;
        
        rCmdDownforceValve := (Kp_Force * rDownforceError) + (Ki_Force * rDownforceIntegral);
        
        IF rCmdDownforceValve > 100.0 THEN rCmdDownforceValve := 100.0; END_IF;
        IF rCmdDownforceValve < 0.0 THEN rCmdDownforceValve := 0.0; END_IF;

        (* Process Endpoint Detection *)
        IF rWaferThickness <= rTargetThickness THEN
            iState := 30; (* Polish complete *)
        END_IF;
        
        (* Safety check during polish *)
        IF rActualPlatenDownforce > (rPlatenDownforceTarget * 1.2) THEN
            bAlarm := TRUE;
            iErrorCode := 301; (* Downforce over-pressure critical *)
            iState := 900;
        END_IF;

    30: (* PROCESS COMPLETE DE-ESCALATION *)
        bProcessComplete := TRUE;
        rCmdDownforceValve := 0.0; (* Lift platen *)
        
        (* Keep slurry flowing slightly for cleaning briefly *)
        rCmdSlurryValve := 10.0; 
        
        tProcessTimer(IN := TRUE, PT := T#2S);
        IF tProcessTimer.Q THEN
            tProcessTimer(IN := FALSE);
            rCmdSlurryValve := 0.0;
            IF NOT bEnable THEN
                iState := 0;
            END_IF;
        END_IF;

    900: (* FAULT RECOVERY / ABORT *)
        rCmdSlurryValve := 0.0;
        rCmdDownforceValve := 0.0;
        tStabilizationTimer(IN := FALSE);
        tProcessTimer(IN := FALSE);
        
        IF NOT bEnable THEN
            bAlarm := FALSE;
            iErrorCode := 0;
            iState := 0;
        END_IF;

END_CASE;

END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
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
