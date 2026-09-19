import json, uuid, os
prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Automated Civil Tunnel Boring Machine (TBM) Cutterhead Torque and Thrust Cylinder Sync**

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_TBM_CutterheadControl\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Automated Civil Tunnel Boring Machine (TBM) Cutterhead Torque and Thrust Cylinder Sync

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_TBM_CutterheadControl
(* 
   Automated Civil Tunnel Boring Machine (TBM) Cutterhead Torque and Thrust Cylinder Sync
   Advanced PLC automation architect implementation.
   Provides real-time synchronization between cutterhead rotational torque and forward thrust.
*)

VAR_INPUT
    bEnable                 : BOOL;     (* System enable signal *)
    bEmergencyStop          : BOOL;     (* Safety relay OK signal (TRUE = safe, FALSE = E-STOP) *)
    rActualTorque           : REAL;     (* Current cutterhead torque feedback (kNm) *)
    rActualThrustPressure   : REAL;     (* Current thrust cylinder pressure feedback (bar) *)
    rTargetAdvanceRate      : REAL;     (* Target TBM advance rate (mm/min) *)
    rRockDensityFactor      : REAL;     (* Geology factor based on seismic/probing (0.0 to 1.0) *)
    bOverloadProtection     : BOOL;     (* Hardware overload relay status *)
    rMaxAllowableTorque     : REAL;     (* Maximum safe operating torque (kNm) *)
END_VAR

VAR_OUTPUT
    bSystemReady            : BOOL;     (* System ready status for main control room *)
    rThrustCommand          : REAL;     (* Command signal to proportional thrust valves (0-100%) *)
    rTorqueLimitCommand     : REAL;     (* Command signal to VFD torque limiters (0-100%) *)
    bAlarm                  : BOOL;     (* Critical fault alarm output *)
    bWarningOverTorque      : BOOL;     (* Early warning for approaching torque limit *)
    iOperatingState         : INT;      (* Current internal state machine value *)
END_VAR

VAR
    iState                  : INT := 0; (* Internal State: 0=IDLE, 10=INIT, 20=RUNNING, 99=FAULT *)
    tStartupDelay           : TON;
    tFilteringTimer         : TON;
    
    (* Internal process variables *)
    rFilteredTorque         : REAL := 0.0;
    rTorqueError            : REAL := 0.0;
    rThrustCalculated       : REAL := 0.0;
    
    (* PI Controller for Thrust Sync *)
    rKpThrust               : REAL := 2.5;
    rKiThrust               : REAL := 0.15;
    rIntegralSum            : REAL := 0.0;
    rLastError              : REAL := 0.0;
    
    (* Filter Constants *)
    rAlpha                  : REAL := 0.1; (* Low pass filter coefficient *)
END_VAR

(* === MAIN LOGIC === *)
(* 1. Safety and Critical Interlocks *)
IF NOT bEmergencyStop OR NOT bOverloadProtection THEN
    bSystemReady := FALSE;
    bAlarm := TRUE;
    rThrustCommand := 0.0;
    rTorqueLimitCommand := 0.0;
    iState := 99; (* FAULT STATE *)
    iOperatingState := iState;
    RETURN;
END_IF;

(* 2. Signal Filtering - Exponential moving average for sensor noise reduction *)
rFilteredTorque := rAlpha * rActualTorque + (1.0 - rAlpha) * rFilteredTorque;

(* 3. Alarm Generation - Pre-warning for torque *)
IF rFilteredTorque > (rMaxAllowableTorque * 0.9) THEN
    bWarningOverTorque := TRUE;
ELSE
    bWarningOverTorque := FALSE;
END_IF;

(* 4. State Machine Execution *)
CASE iState OF
    0: (* IDLE *)
        bSystemReady := TRUE;
        bAlarm := FALSE;
        rThrustCommand := 0.0;
        rTorqueLimitCommand := 0.0;
        
        IF bEnable THEN
            iState := 10;
            tStartupDelay(IN := FALSE); (* Reset timer *)
        END_IF;

    10: (* INIT - Pre-charging hydraulic systems and preparing VFDs *)
        tStartupDelay(IN := TRUE, PT := T#5S);
        
        (* Gradually set torque limit to safe start value *)
        rTorqueLimitCommand := 20.0; 
        
        IF tStartupDelay.Q THEN
            tStartupDelay(IN := FALSE);
            rIntegralSum := 0.0; (* Reset PID integral *)
            iState := 20;
        END_IF;
        
        IF NOT bEnable THEN
            iState := 0;
        END_IF;

    20: (* RUNNING - Synchronizing Torque and Thrust *)
        
        (* Calculate dynamic torque error *)
        rTorqueError := rMaxAllowableTorque - rFilteredTorque;
        
        (* If we are too close to torque limit, we must reduce thrust to prevent cutterhead jamming *)
        IF rTorqueError < (rMaxAllowableTorque * 0.15) THEN
            (* PI Control for Thrust Reduction *)
            rIntegralSum := rIntegralSum + (rTorqueError * rKiThrust);
            
            (* Anti-windup protection *)
            IF rIntegralSum > 50.0 THEN rIntegralSum := 50.0; END_IF;
            IF rIntegralSum < -50.0 THEN rIntegralSum := -50.0; END_IF;
            
            rThrustCalculated := (rTorqueError * rKpThrust) + rIntegralSum;
        ELSE
            (* Safe operating zone, base thrust on target advance rate and rock density *)
            rThrustCalculated := rTargetAdvanceRate * (1.5 - rRockDensityFactor);
            (* Decay integral action when safe *)
            rIntegralSum := rIntegralSum * 0.99;
        END_IF;
        
        (* Clamp thrust command *)
        IF rThrustCalculated > 100.0 THEN
            rThrustCommand := 100.0;
        ELSIF rThrustCalculated < 0.0 THEN
            rThrustCommand := 0.0;
        ELSE
            rThrustCommand := rThrustCalculated;
        END_IF;
        
        (* Set dynamic torque limit based on geology *)
        rTorqueLimitCommand := 100.0 - (rRockDensityFactor * 20.0);
        
        IF NOT bEnable THEN
            iState := 0;
        END_IF;

    99: (* FAULT HANDLING *)
        (* Wait for operator reset which requires disabling enable signal first *)
        IF NOT bEnable AND bEmergencyStop AND bOverloadProtection THEN
            iState := 0;
            bAlarm := FALSE;
        END_IF;

END_CASE;

(* Update external state output *)
iOperatingState := iState;

END_FUNCTION_BLOCK
```"""
os.makedirs("c:/Users/majip/Downloads/LLM REASEARCH/data/swarm_raw", exist_ok=True)
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
filename = f"c:/Users/majip/Downloads/LLM REASEARCH/data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
print(f"Saved to {filename}")
