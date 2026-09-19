import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Industrial Non-Woven Fabric Meltblown Extrusion Spinneret Hot Air Velocity and Web Tension**

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_Meltblown_Extrusion\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Industrial Non-Woven Fabric Meltblown Extrusion Spinneret Hot Air Velocity and Web Tension

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_Meltblown_Extrusion_Control
VAR_INPUT
    bSystemEnable       : BOOL;     (* Main system enable signal *)
    bEmergencyStop      : BOOL;     (* Safety relay OK signal, normally closed (TRUE=OK) *)
    rSpinneretTemp      : REAL;     (* Measured spinneret temperature [deg C] *)
    rAirVelocityAct     : REAL;     (* Measured hot air velocity [m/s] *)
    rWebTensionAct      : REAL;     (* Measured web tension [N] *)
    rTargetVelocity     : REAL;     (* Setpoint for hot air velocity [m/s] *)
    rTargetTension      : REAL;     (* Setpoint for web tension [N] *)
    rExtruderPressure   : REAL;     (* Melt pressure at die [bar] *)
END_VAR
VAR_OUTPUT
    bSystemReady        : BOOL;     (* System ready status flag *)
    rAirBlowerSpeedRef  : REAL;     (* Reference signal for hot air blower speed [%] *)
    rWinderTorqueRef    : REAL;     (* Reference signal for winder torque/speed [%] *)
    bWarningAlarm       : BOOL;     (* Process warning - limits exceeded slightly *)
    bCriticalAlarm      : BOOL;     (* Process fault - critical limits exceeded, stopping *)
    iCurrentState       : INT;      (* Current state machine state *)
END_VAR
VAR
    iState              : INT := 0; (* Internal state tracking *)
    tStartupDelay       : TON;      (* Timer for pre-heating and stabilization *)
    tStabilizationTimer : TON;      (* Timer for process stabilization *)
    rAirVelocityError   : REAL;
    rAirVelocityInt     : REAL := 0.0;
    rTensionError       : REAL;
    rTensionInt         : REAL := 0.0;
    
    (* Filter variables *)
    rFilteredVelocity   : REAL := 0.0;
    rFilteredTension    : REAL := 0.0;
    
    (* Constants *)
    rAlpha              : REAL := 0.1; (* Low pass filter coefficient *)
    rKp_Air             : REAL := 2.5;
    rKi_Air             : REAL := 0.05;
    rKp_Ten             : REAL := 1.8;
    rKi_Ten             : REAL := 0.02;
    
    rMaxSpeed           : REAL := 100.0;
    rMinSpeed           : REAL := 0.0;
END_VAR

(* === MAIN LOGIC === *)

(* Safety and Interlocks *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bCriticalAlarm := TRUE;
    rAirBlowerSpeedRef := 0.0;
    rWinderTorqueRef := 0.0;
    iState := 99; (* Fault state *)
    RETURN;
END_IF;

(* Input Filtering - EWMA (Exponentially Weighted Moving Average) *)
rFilteredVelocity := rAlpha * rAirVelocityAct + (1.0 - rAlpha) * rFilteredVelocity;
rFilteredTension := rAlpha * rWebTensionAct + (1.0 - rAlpha) * rFilteredTension;

(* Alarms *)
bWarningAlarm := (ABS(rFilteredVelocity - rTargetVelocity) > 5.0) OR (ABS(rFilteredTension - rTargetTension) > 10.0);
bCriticalAlarm := (rExtruderPressure > 250.0) OR (rSpinneretTemp > 350.0);

IF bCriticalAlarm THEN
    iState := 99;
END_IF;

iCurrentState := iState;

(* State Machine *)
CASE iState OF
    0: (* IDLE *)
        bSystemReady := FALSE;
        rAirBlowerSpeedRef := 0.0;
        rWinderTorqueRef := 0.0;
        IF bSystemEnable AND NOT bCriticalAlarm THEN
            iState := 10;
        END_IF;

    10: (* PRE-HEATING & CHECK *)
        tStartupDelay(IN := TRUE, PT := T#10S);
        IF tStartupDelay.Q THEN
            tStartupDelay(IN := FALSE);
            IF rSpinneretTemp > 200.0 THEN (* Minimum operational temp *)
                iState := 20;
            ELSE
                bWarningAlarm := TRUE;
            END_IF;
        END_IF;

    20: (* RUNNING & PID CONTROL *)
        bSystemReady := TRUE;
        
        (* Air Velocity PI Controller *)
        rAirVelocityError := rTargetVelocity - rFilteredVelocity;
        rAirVelocityInt := rAirVelocityInt + (rAirVelocityError * rKi_Air);
        
        (* Anti-windup for Air Velocity *)
        IF rAirVelocityInt > rMaxSpeed THEN rAirVelocityInt := rMaxSpeed; END_IF;
        IF rAirVelocityInt < rMinSpeed THEN rAirVelocityInt := rMinSpeed; END_IF;
        
        rAirBlowerSpeedRef := (rAirVelocityError * rKp_Air) + rAirVelocityInt;
        
        (* Saturation for Output *)
        IF rAirBlowerSpeedRef > rMaxSpeed THEN rAirBlowerSpeedRef := rMaxSpeed; END_IF;
        IF rAirBlowerSpeedRef < rMinSpeed THEN rAirBlowerSpeedRef := rMinSpeed; END_IF;
        
        (* Web Tension PI Controller *)
        rTensionError := rTargetTension - rFilteredTension;
        rTensionInt := rTensionInt + (rTensionError * rKi_Ten);
        
        (* Anti-windup for Web Tension *)
        IF rTensionInt > rMaxSpeed THEN rTensionInt := rMaxSpeed; END_IF;
        IF rTensionInt < rMinSpeed THEN rTensionInt := rMinSpeed; END_IF;
        
        rWinderTorqueRef := (rTensionError * rKp_Ten) + rTensionInt;
        
        (* Saturation for Output *)
        IF rWinderTorqueRef > rMaxSpeed THEN rWinderTorqueRef := rMaxSpeed; END_IF;
        IF rWinderTorqueRef < rMinSpeed THEN rWinderTorqueRef := rMinSpeed; END_IF;
        
        IF NOT bSystemEnable THEN
            iState := 30; (* Ramp down *)
        END_IF;
        
    30: (* RAMP DOWN *)
        rAirBlowerSpeedRef := rAirBlowerSpeedRef * 0.9;
        rWinderTorqueRef := rWinderTorqueRef * 0.9;
        IF rAirBlowerSpeedRef < 1.0 AND rWinderTorqueRef < 1.0 THEN
            rAirBlowerSpeedRef := 0.0;
            rWinderTorqueRef := 0.0;
            iState := 0;
        END_IF;

    99: (* FAULT HANDLING *)
        bSystemReady := FALSE;
        rAirBlowerSpeedRef := 0.0;
        rWinderTorqueRef := 0.0;
        tStartupDelay(IN := FALSE);
        IF bSystemEnable = FALSE AND bCriticalAlarm = FALSE THEN
            iState := 0;
        END_IF;

END_CASE;

END_FUNCTION_BLOCK
```"""

record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
print(f"Saved to {filename}")
