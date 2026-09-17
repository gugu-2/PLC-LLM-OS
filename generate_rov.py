import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Automated Subsea Remotely Operated Vehicle (ROV) Thruster Vectoring and Depth Hold**

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_SubseaROV_Vectoring\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Automated Subsea Remotely Operated Vehicle (ROV) Thruster Vectoring and Depth Hold

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_SubseaROV_Vectoring
VAR_INPUT
    (* Required inputs for ROV thruster and depth control *)
    bSystemEnable       : BOOL;     (* Main system enable signal *)
    bEstopStatusOk      : BOOL;     (* Emergency stop circuit healthy *)
    rTargetDepth        : REAL;     (* Desired depth in meters *)
    rCurrentDepth       : REAL;     (* Actual measured depth in meters from pressure transducer *)
    rPitchAngle         : REAL;     (* Current pitch angle in degrees from IMU *)
    rRollAngle          : REAL;     (* Current roll angle in degrees from IMU *)
    rYawRate            : REAL;     (* Current yaw rate in degrees/sec from IMU *)
    bLeakDetected       : BOOL;     (* Water ingress detection in hull *)
END_VAR
VAR_OUTPUT
    (* Required outputs *)
    bSystemReady        : BOOL;     (* Subsea ROV system is ready and initialized *)
    bCriticalAlarm      : BOOL;     (* Critical fault alarm (leak, over-depth, E-stop) *)
    rThrusterCmd_Port   : REAL;     (* Commanded thrust port side (-100.0 to 100.0 %) *)
    rThrusterCmd_Stbd   : REAL;     (* Commanded thrust starboard side (-100.0 to 100.0 %) *)
    rThrusterCmd_Vert1  : REAL;     (* Commanded vertical thrust forward (-100.0 to 100.0 %) *)
    rThrusterCmd_Vert2  : REAL;     (* Commanded vertical thrust aft (-100.0 to 100.0 %) *)
    iOperatingState     : INT;      (* Current state machine step *)
END_VAR
VAR
    (* Internal state and filtering variables *)
    iState              : INT := 0;
    rFilteredDepth      : REAL := 0.0;
    rDepthError         : REAL := 0.0;
    rDepthErrorPrev     : REAL := 0.0;
    rDepthIntegral      : REAL := 0.0;
    rDepthDerivative    : REAL := 0.0;
    
    (* PID Constants for Depth Hold *)
    Kp_Depth            : REAL := 2.5;
    Ki_Depth            : REAL := 0.1;
    Kd_Depth            : REAL := 1.2;
    rDt                 : REAL := 0.05; (* 50ms cycle time assumption *)
    
    (* Max limits *)
    rMaxThrust          : REAL := 100.0;
    rMaxDepth           : REAL := 3000.0; (* 3000m max rated depth *)
    
    (* Timers *)
    tStartupDelay       : TON;
    tFaultTimer         : TON;
    
    (* Filter alpha *)
    rAlpha              : REAL := 0.15; 
END_VAR

(* === MAIN LOGIC === *)
(* 1. Safety Interlocks and Hardware Checks *)
IF NOT bEstopStatusOk OR bLeakDetected OR (rCurrentDepth > rMaxDepth) THEN
    (* Immediate shutdown on critical fault *)
    bSystemReady := FALSE;
    bCriticalAlarm := TRUE;
    iState := 99; (* FAULT STATE *)
    rThrusterCmd_Port := 0.0;
    rThrusterCmd_Stbd := 0.0;
    rThrusterCmd_Vert1 := 0.0;
    rThrusterCmd_Vert2 := 0.0;
    iOperatingState := iState;
    RETURN;
END_IF;

bCriticalAlarm := FALSE;

(* 2. Sensor Noise Filtering (Low-pass filter on depth) *)
rFilteredDepth := (rAlpha * rCurrentDepth) + ((1.0 - rAlpha) * rFilteredDepth);

(* 3. Main State Machine *)
CASE iState OF
    0: (* INIT *)
        bSystemReady := FALSE;
        rThrusterCmd_Port := 0.0;
        rThrusterCmd_Stbd := 0.0;
        rThrusterCmd_Vert1 := 0.0;
        rThrusterCmd_Vert2 := 0.0;
        
        IF bSystemEnable THEN
            tStartupDelay(IN := TRUE, PT := T#2S);
            IF tStartupDelay.Q THEN
                tStartupDelay(IN := FALSE);
                iState := 10;
            END_IF;
        ELSE
            tStartupDelay(IN := FALSE);
        END_IF;

    10: (* READY / IDLE *)
        bSystemReady := TRUE;
        rDepthIntegral := 0.0; (* Reset integral on entry to active control *)
        rDepthErrorPrev := 0.0;
        
        IF bSystemEnable THEN
            iState := 20; (* Moving to active depth hold *)
        ELSE
            iState := 0;
        END_IF;

    20: (* ACTIVE DEPTH HOLD & THRUSTER VECTORING *)
        bSystemReady := TRUE;
        
        (* Calculate Depth PID *)
        rDepthError := rTargetDepth - rFilteredDepth;
        
        (* Anti-windup for integral term *)
        rDepthIntegral := rDepthIntegral + (rDepthError * rDt);
        IF rDepthIntegral > 50.0 THEN
            rDepthIntegral := 50.0;
        ELSIF rDepthIntegral < -50.0 THEN
            rDepthIntegral := -50.0;
        END_IF;
        
        rDepthDerivative := (rDepthError - rDepthErrorPrev) / rDt;
        
        (* Calculate baseline vertical thrust required *)
        rThrusterCmd_Vert1 := (Kp_Depth * rDepthError) + (Ki_Depth * rDepthIntegral) + (Kd_Depth * rDepthDerivative);
        rThrusterCmd_Vert2 := rThrusterCmd_Vert1; (* Simplified distribution *)
        
        (* Active Pitch/Roll Compensation (Vectoring mix) *)
        (* Compensate for pitch to keep ROV level by differential vertical thrust *)
        rThrusterCmd_Vert1 := rThrusterCmd_Vert1 - (rPitchAngle * 1.5);
        rThrusterCmd_Vert2 := rThrusterCmd_Vert2 + (rPitchAngle * 1.5);
        
        (* Saturate vertical thrust outputs *)
        IF rThrusterCmd_Vert1 > rMaxThrust THEN rThrusterCmd_Vert1 := rMaxThrust; END_IF;
        IF rThrusterCmd_Vert1 < -rMaxThrust THEN rThrusterCmd_Vert1 := -rMaxThrust; END_IF;
        IF rThrusterCmd_Vert2 > rMaxThrust THEN rThrusterCmd_Vert2 := rMaxThrust; END_IF;
        IF rThrusterCmd_Vert2 < -rMaxThrust THEN rThrusterCmd_Vert2 := -rMaxThrust; END_IF;
        
        (* Maintain previous error for derivative calculation *)
        rDepthErrorPrev := rDepthError;
        
        (* Example of horizontal vectoring mixing with yaw rate *)
        rThrusterCmd_Port := rYawRate * 2.0;
        rThrusterCmd_Stbd := -rYawRate * 2.0;
        
        IF NOT bSystemEnable THEN
            iState := 10;
        END_IF;

    99: (* FAULT HANDLING *)
        (* Wait for manual reset sequence (simulated by dropping enable) *)
        IF NOT bSystemEnable THEN
            iState := 0;
        END_IF;

END_CASE;

iOperatingState := iState;

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
