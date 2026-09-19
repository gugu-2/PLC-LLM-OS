import json
import uuid
import os

prompt = """<USER_REQUEST>
You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Automated Inland Waterway Navigation Lock Chamber Flooding Valve Sequence and Ship Arrestor**

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_NavigationLock_Control\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Automated Inland Waterway Navigation Lock Chamber Flooding Valve Sequence and Ship Arrestor

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT.
</USER_REQUEST>"""

code = """```iec-st
FUNCTION_BLOCK FB_NavigationLock_Chamber_Valve_Arrestor_Control
VAR_INPUT
    (* Physical Inputs *)
    bSystemEnable           : BOOL;     (* Overall system operational enable signal *)
    bEStopActive            : BOOL;     (* Emergency stop circuit OK signal (Safety Relay) *)
    rUpstreamLevel          : REAL;     (* Upstream water level in meters, filtered *)
    rDownstreamLevel        : REAL;     (* Downstream water level in meters, filtered *)
    rChamberLevel           : REAL;     (* Current chamber water level in meters *)
    bShipDetected           : BOOL;     (* Radar/LiDAR detection of ship in arrestor zone *)
    rArrestorTension        : REAL;     (* Tension on ship arrestor cable in kN *)
    rValvePositionFeed      : REAL;     (* Feedback of current filling valve position (0.0 to 100.0%) *)
    bVesselInLock           : BOOL;     (* Indicates a vessel is confirmed inside the lock chamber *)
END_VAR
VAR_OUTPUT
    (* Physical Outputs *)
    bSystemReady            : BOOL;     (* Indicates system is ready for automated cycle *)
    rValveCommandOut        : REAL;     (* Command signal to flooding valve (0.0 to 100.0%) *)
    bArrestorEngage         : BOOL;     (* Command to deploy/engage ship arrestor mechanism *)
    bArrestorRelease        : BOOL;     (* Command to retract/release ship arrestor mechanism *)
    bCriticalAlarm          : BOOL;     (* General fault/critical alarm indicator *)
    iSequenceState          : INT;      (* Current active state of the operation sequence *)
    rHeadDifference         : REAL;     (* Calculated head difference between chamber and target *)
END_VAR
VAR
    (* Internal State and Timers *)
    iState                  : INT := 0; (* Internal state machine tracker *)
    tFillTimer              : TON;      (* Maximum allowed time for chamber filling operation *)
    tArrestorDeployTime     : TON;      (* Delay timer for arrestor deployment confirmation *)
    
    (* Filter Variables *)
    rFilteredChamberLevel   : REAL := 0.0;
    rAlpha                  : REAL := 0.1; (* Low pass filter coefficient *)
    
    (* PID & Control Variables *)
    rError                  : REAL := 0.0;
    rIntegral               : REAL := 0.0;
    rDerivative             : REAL := 0.0;
    rLastError              : REAL := 0.0;
    rKp                     : REAL := 2.5;
    rKi                     : REAL := 0.15;
    rKd                     : REAL := 0.05;
    rPIDOutput              : REAL := 0.0;
    
    (* Constants *)
    rMaxFillRate            : REAL := 1.5; (* Max allowed level change rate m/min *)
    rArrestorMaxTension     : REAL := 1500.0; (* Max allowed cable tension in kN before emergency release *)
    rLevelTolerance         : REAL := 0.05; (* Tolerance in meters for water level equality *)
END_VAR

(* === MAIN SAFETY INTERLOCKS === *)
IF NOT bEStopActive THEN
    (* Immediate safe state upon Emergency Stop *)
    rValveCommandOut := 0.0;
    bArrestorEngage := FALSE;
    bArrestorRelease := FALSE;
    bCriticalAlarm := TRUE;
    bSystemReady := FALSE;
    iState := 999; (* Fault state *)
    RETURN;
END_IF;

(* === SENSOR NOISE FILTERING === *)
(* Exponential Moving Average Low-Pass Filter for Chamber Level *)
rFilteredChamberLevel := (rAlpha * rChamberLevel) + ((1.0 - rAlpha) * rFilteredChamberLevel);

(* Calculate active Head Difference *)
rHeadDifference := ABS(rUpstreamLevel - rFilteredChamberLevel);

(* === SHIP ARRESTOR SAFETY OVERRIDE === *)
(* If ship strikes arrestor too hard, trigger emergency sequence to prevent structural failure *)
IF bShipDetected AND (rArrestorTension > rArrestorMaxTension) THEN
    bArrestorRelease := TRUE;
    bArrestorEngage := FALSE;
    bCriticalAlarm := TRUE;
    iState := 999;
END_IF;

(* === MAIN STATE MACHINE === *)
CASE iState OF
    0: (* IDLE & INITIALIZATION *)
        rValveCommandOut := 0.0;
        bArrestorEngage := FALSE;
        bArrestorRelease := TRUE;
        bCriticalAlarm := FALSE;
        bSystemReady := bSystemEnable AND NOT bCriticalAlarm;
        
        IF bSystemReady AND bVesselInLock THEN
            iState := 10;
        END_IF;
        
    10: (* DEPLOY ARRESTOR BEFORE FLOODING *)
        bArrestorEngage := TRUE;
        bArrestorRelease := FALSE;
        
        tArrestorDeployTime(IN := TRUE, PT := T#10S);
        IF tArrestorDeployTime.Q THEN
            tArrestorDeployTime(IN := FALSE);
            iState := 20;
        END_IF;

    20: (* CALCULATE & CONTROL VALVE FLOODING (PID CONTROL) *)
        rError := rUpstreamLevel - rFilteredChamberLevel;
        
        (* PID Calculations *)
        rIntegral := rIntegral + rError;
        (* Anti-windup *)
        IF rIntegral > 100.0 THEN rIntegral := 100.0; END_IF;
        IF rIntegral < -100.0 THEN rIntegral := -100.0; END_IF;
        
        rDerivative := rError - rLastError;
        rPIDOutput := (rKp * rError) + (rKi * rIntegral) + (rKd * rDerivative);
        rLastError := rError;
        
        (* Bound Valve Command 0-100% *)
        IF rPIDOutput > 100.0 THEN rValveCommandOut := 100.0; 
        ELSIF rPIDOutput < 0.0 THEN rValveCommandOut := 0.0; 
        ELSE rValveCommandOut := rPIDOutput; 
        END_IF;
        
        (* Watchdog timer for flooding process *)
        tFillTimer(IN := TRUE, PT := T#45M);
        IF tFillTimer.Q THEN
            bCriticalAlarm := TRUE;
            iState := 999; (* Timeout fault *)
        END_IF;
        
        (* Check if level reached *)
        IF ABS(rError) <= rLevelTolerance THEN
            tFillTimer(IN := FALSE);
            iState := 30;
        END_IF;
        
    30: (* EQUALIZATION COMPLETE, CLOSE VALVES *)
        rValveCommandOut := 0.0;
        (* Ensure valve feedback is fully closed before releasing ship *)
        IF rValvePositionFeed <= 1.0 THEN
            iState := 40;
        END_IF;
        
    40: (* RELEASE ARRESTOR AND END CYCLE *)
        bArrestorEngage := FALSE;
        bArrestorRelease := TRUE;
        
        IF NOT bVesselInLock THEN
            iState := 0; (* Vessel has exited, return to idle *)
        END_IF;
        
    999: (* FAULT HANDLING *)
        rValveCommandOut := 0.0;
        bSystemReady := FALSE;
        IF NOT bCriticalAlarm AND bSystemEnable THEN
            (* Fault acknowledged/reset *)
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
