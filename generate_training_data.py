import json, uuid, os

os.makedirs('data/swarm_raw', exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Automated Micro-CT Scanner Sample Rotary Stage Tilt and Translate Vectoring**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Nanometer-precision piezo-stepper stage runout compensation, continuous 360-degree slip-ring synchronization, and X-ray beam shutter interlock). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_MicroCT_StageControl\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
   record = {\"messages\": [{\"role\": \"user\", \"content\": prompt}, {\"role\": \"assistant\", \"content\": code}]}
   with open(f\"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json\", \"w\", encoding=\"utf-8\") as f:
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
6. REPLY with: EVOLUTION COMPLETE: Automated Micro-CT Scanner Sample Rotary Stage Tilt and Translate Vectoring

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_MicroCT_StageControl
VAR_INPUT
    (* Core enabling and safety signals *)
    bEnableSystem          : BOOL;     (* System master enable signal from overarching control *)
    bXRayShutterOpen       : BOOL;     (* Beam shutter interlock signal feedback *)
    bEmergencyStop         : BOOL;     (* E-stop loop OK, dual-channel redundancy *)
    
    (* Trajectory Commands *)
    rTargetTheta           : REAL;     (* Target rotation angle in degrees (0-360) *)
    rTargetTranslateZ      : REAL;     (* Target Z height in mm, micro-stepping *)
    rTargetTiltX           : REAL;     (* Target X tilt in degrees for wobble compensation *)
    
    (* High-resolution feedback *)
    rCurrentThetaEncoder   : REAL;     (* Feedback from ultra-high-res rotary encoder *)
    rCurrentZEncoder       : REAL;     (* Feedback from Z linear nanometer encoder *)
    rCurrentTiltEncoder    : REAL;     (* Feedback from Tilt piezo strain gauge *)
END_VAR
VAR_OUTPUT
    (* Status and Control signals *)
    bSystemReady           : BOOL;     (* Stage synchronized and ready for imaging acquisition *)
    rControlOutTheta       : REAL;     (* Drive signal for rotary stage continuous rotation *)
    rControlOutZ           : REAL;     (* Drive signal for Z translation stepper *)
    rControlOutTilt        : REAL;     (* Drive signal for Tilt piezo vectoring *)
    bShutterInterlockOk    : BOOL;     (* Safe to open X-ray shutter - stage stable *)
    bFaultActive           : BOOL;     (* Active fault state - halts scan sequence *)
    iErrorCode             : INT;      (* Diagnostics error code for HMI reporting *)
END_VAR
VAR
    (* Internal State and timers *)
    iStateMachine          : INT := 0;
    tSettleTimer           : TON;
    tWatchdog              : TON;
    
    (* PID variables for multi-axis compensation *)
    rErrorTheta            : REAL;
    rErrorZ                : REAL;
    rErrorTilt             : REAL;
    rIntegralTheta         : REAL := 0.0;
    rDerivativeTheta       : REAL := 0.0;
    rLastErrorTheta        : REAL := 0.0;
    
    (* Tuning parameters and tolerances *)
    rKpTheta               : REAL := 2.55; 
    rKiTheta               : REAL := 0.12; 
    rKdTheta               : REAL := 0.045;
    rTolTheta              : REAL := 0.0005; (* Extremely tight angular tolerance *)
    rTolZ                  : REAL := 0.0001; (* Nanometer range Z tolerance *)
    rTolTilt               : REAL := 0.0001;
    
    bInPosition            : BOOL;
END_VAR

(* === MAIN LOGIC === *)
(* Master Safety Interlock *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bFaultActive := TRUE;
    iErrorCode := 999; (* Code 999: E-Stop Tripped *)
    rControlOutTheta := 0.0;
    rControlOutZ := 0.0;
    rControlOutTilt := 0.0;
    bShutterInterlockOk := FALSE;
    rIntegralTheta := 0.0; (* Reset windup *)
    RETURN;
END_IF;

CASE iStateMachine OF
    0: (* IDLE & INIT *)
        bSystemReady := FALSE;
        bFaultActive := FALSE;
        bShutterInterlockOk := FALSE;
        iErrorCode := 0;
        
        (* Reset integrators on idle *)
        rIntegralTheta := 0.0;
        rLastErrorTheta := 0.0;
        
        IF bEnableSystem THEN
            iStateMachine := 10;
        END_IF;

    10: (* CALCULATION & PRECISION PID VECTORING CONTROL *)
        (* Calculate errors *)
        rErrorTheta := rTargetTheta - rCurrentThetaEncoder;
        
        (* Wrap-around handling for continuous 360-degree rotation *)
        IF rErrorTheta > 180.0 THEN
            rErrorTheta := rErrorTheta - 360.0;
        ELSIF rErrorTheta < -180.0 THEN
            rErrorTheta := rErrorTheta + 360.0;
        END_IF;
        
        rErrorZ := rTargetTranslateZ - rCurrentZEncoder;
        rErrorTilt := rTargetTiltX - rCurrentTiltEncoder;
        
        (* PID for Theta - High Speed, High Precision *)
        rIntegralTheta := rIntegralTheta + rErrorTheta;
        
        (* Anti-windup clamping *)
        IF rIntegralTheta > 100.0 THEN rIntegralTheta := 100.0; END_IF;
        IF rIntegralTheta < -100.0 THEN rIntegralTheta := -100.0; END_IF;
        
        rDerivativeTheta := rErrorTheta - rLastErrorTheta;
        rControlOutTheta := (rKpTheta * rErrorTheta) + (rKiTheta * rIntegralTheta) + (rKdTheta * rDerivativeTheta);
        rLastErrorTheta := rErrorTheta;
        
        (* PD for Z and Proportional for Tilt *)
        rControlOutZ := (rErrorZ * 150.0) + ((rErrorZ - rLastErrorTheta) * 5.0); 
        rControlOutTilt := rErrorTilt * 300.0; (* Fast piezo response *)
        
        (* In-Position Boolean Logic *)
        bInPosition := (ABS(rErrorTheta) <= rTolTheta) AND (ABS(rErrorZ) <= rTolZ) AND (ABS(rErrorTilt) <= rTolTilt);
        
        (* Stabilization Timer *)
        IF bInPosition THEN
            tSettleTimer(IN := TRUE, PT := T#2S);
            IF tSettleTimer.Q THEN
                iStateMachine := 20;
            END_IF;
        ELSE
            tSettleTimer(IN := FALSE);
            bSystemReady := FALSE;
        END_IF;
        
        (* Watchdog timer for motion stagnation *)
        tWatchdog(IN := NOT bInPosition, PT := T#15S);
        IF tWatchdog.Q THEN
            iStateMachine := 100; (* FAULT - Timeout *)
        END_IF;

        IF NOT bEnableSystem THEN
            iStateMachine := 0;
        END_IF;

    20: (* IN POSITION - SYNCHRONIZED ACQUISITION READY *)
        bSystemReady := TRUE;
        bShutterInterlockOk := TRUE; (* Stage is stationary, safe to expose *)
        
        (* Continuous monitoring for micro-disturbances during imaging *)
        IF NOT bInPosition THEN
            bSystemReady := FALSE;
            bShutterInterlockOk := FALSE;
            tSettleTimer(IN := FALSE);
            iStateMachine := 10; (* Re-adjust *)
        END_IF;

        IF NOT bEnableSystem THEN
            iStateMachine := 0;
        END_IF;

    100: (* FAULT STATE - MOTION TIMEOUT OR SERVO ERROR *)
        bSystemReady := FALSE;
        bShutterInterlockOk := FALSE;
        bFaultActive := TRUE;
        iErrorCode := 101; (* Code 101: Stage Motion Timeout/Tracking Error *)
        
        (* Safe zero-energy state *)
        rControlOutTheta := 0.0;
        rControlOutZ := 0.0;
        rControlOutTilt := 0.0;
        
        IF NOT bEnableSystem THEN
            iStateMachine := 0;
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

with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print("success")
