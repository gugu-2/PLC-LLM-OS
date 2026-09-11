import os, json, uuid

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Next-Gen Aerospace Reusable Launch Vehicle (RLV) Supersonic Retro-Propulsion**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Plume-induced flow separation hypersonic drag modulation, grid fin differential aerodynamic torque vectoring, and cryogenic engine continuous deep throttling). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\nFUNCTION_BLOCK FB_RLV_RetroPropulsion\n//...\nEND_FUNCTION_BLOCK\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Next-Gen Aerospace Reusable Launch Vehicle (RLV) Supersonic Retro-Propulsion

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_RLV_RetroPropulsion_Control
VAR_INPUT
    (* Required: at least 4-8 physical inputs with types and comments *)
    bEnable                 : BOOL;     (* System enable signal for Retro-propulsion sequence *)
    bEmergencyStop          : BOOL;     (* Safety interlock / Flight Termination System (FTS) OK signal *)
    rAltitude               : REAL;     (* Current radar altitude in meters *)
    rVelocity               : REAL;     (* Current vertical velocity in m/s (negative for descent) *)
    rMachNumber             : REAL;     (* Current Mach number for aerodynamic torque scheduling *)
    rTargetThrust           : REAL;     (* Commanded target thrust level (0.0 to 100.0%) *)
    aIMU_PitchYawRoll       : ARRAY[0..2] OF REAL; (* Inertial Measurement Unit pitch, yaw, roll rates *)
END_VAR
VAR_OUTPUT
    (* Required: at least 3-6 outputs with types and comments *)
    bSystemReady            : BOOL;     (* True when engines are chilled, purged, and ready for ignition *)
    rEngineThrottleOut      : REAL;     (* Commanded deep throttling value to Main Engine Controllers (MEC) *)
    aGridFinActuatorCmd     : ARRAY[0..3] OF REAL; (* Differential aerodynamic torque vectoring commands *)
    bAlarm                  : BOOL;     (* Major fault or anomaly detection flag *)
    bIgnitionCmd            : BOOL;     (* Engine ignition sequence start command *)
END_VAR
VAR
    (* Internal state variables *)
    iState                  : INT := 0; (* Internal state machine sequence ID *)
    tTimer                  : TON;      (* General purpose step timer *)
    rFilteredAltitude       : REAL;     (* Exponential moving average of altitude *)
    rAltitudeAlpha          : REAL := 0.2; (* Filter coefficient *)
    rKp_Throttling          : REAL := 1.25;(* Proportional gain for throttle control *)
    rKd_Throttling          : REAL := 0.45;(* Derivative gain for throttle control *)
    rErrorVal               : REAL;
    rLastErrorVal           : REAL;
    rMachDragLimit          : REAL;
END_VAR

(* === MAIN LOGIC === *)
(* First layer of defense: Hard-wired Flight Termination or manual E-Stop *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bIgnitionCmd := FALSE;
    rEngineThrottleOut := 0.0;
    aGridFinActuatorCmd[0] := 0.0;
    aGridFinActuatorCmd[1] := 0.0;
    aGridFinActuatorCmd[2] := 0.0;
    aGridFinActuatorCmd[3] := 0.0;
    bAlarm := TRUE;
    iState := 999; (* FAULT STATE *)
    RETURN;
END_IF;

(* Sensor Noise Filtering - EMA for radar altitude smoothing during supersonic plume interference *)
rFilteredAltitude := (rAltitudeAlpha * rAltitude) + ((1.0 - rAltitudeAlpha) * rFilteredAltitude);

CASE iState OF
    0: (* IDLE & PRE-CHILL *)
        bSystemReady := TRUE;
        bAlarm := FALSE;
        rEngineThrottleOut := 0.0;
        bIgnitionCmd := FALSE;
        IF bEnable AND rAltitude < 40000.0 AND rVelocity < 0.0 THEN
            iState := 10;
        END_IF;

    10: (* ENGINE IGNITION SEQUENCE *)
        bSystemReady := FALSE;
        bIgnitionCmd := TRUE;
        rEngineThrottleOut := 40.0; (* Minimum ignition thrust *)
        tTimer(IN := TRUE, PT := T#2S);
        IF tTimer.Q THEN
            tTimer(IN := FALSE);
            iState := 20;
        END_IF;

    20: (* SUPERSONIC RETRO-PROPULSION THROTTLE MODULATION *)
        (* Calculate dynamic pressure proxy and aerodynamic drag limits for grid fin deploy *)
        rMachDragLimit := rMachNumber * 1.5; 
        IF rMachNumber > 1.2 THEN
            aGridFinActuatorCmd[0] := aIMU_PitchYawRoll[0] * 5.0 + rMachDragLimit;
            aGridFinActuatorCmd[1] := aIMU_PitchYawRoll[0] * -5.0 + rMachDragLimit;
            aGridFinActuatorCmd[2] := aIMU_PitchYawRoll[1] * 5.0 + rMachDragLimit;
            aGridFinActuatorCmd[3] := aIMU_PitchYawRoll[1] * -5.0 + rMachDragLimit;
        END_IF;
        
        (* Deep Throttling PD Controller to manage velocity profile *)
        rErrorVal := rTargetThrust - rVelocity; 
        rEngineThrottleOut := rEngineThrottleOut + (rKp_Throttling * rErrorVal) + (rKd_Throttling * (rErrorVal - rLastErrorVal));
        rLastErrorVal := rErrorVal;
        
        (* Clamp throttle between 30% and 100% (Deep throttle limits) *)
        IF rEngineThrottleOut > 100.0 THEN
            rEngineThrottleOut := 100.0;
        ELSIF rEngineThrottleOut < 30.0 THEN
            rEngineThrottleOut := 30.0;
        END_IF;

        IF rFilteredAltitude < 50.0 THEN
            iState := 30;
        END_IF;

    30: (* TERMINAL HOVER & TOUCHDOWN *)
        rEngineThrottleOut := 35.0; (* Hover thrust *)
        aGridFinActuatorCmd[0] := 0.0;
        aGridFinActuatorCmd[1] := 0.0;
        aGridFinActuatorCmd[2] := 0.0;
        aGridFinActuatorCmd[3] := 0.0;
        IF rVelocity > -1.0 AND rFilteredAltitude < 2.0 THEN
            iState := 40;
        END_IF;

    40: (* TOUCHDOWN COMPLETE - ENGINE SHUTDOWN *)
        bIgnitionCmd := FALSE;
        rEngineThrottleOut := 0.0;
        bSystemReady := TRUE;
        IF NOT bEnable THEN
            iState := 0;
        END_IF;

    999: (* FAULT HANDLING *)
        bAlarm := TRUE;
        bIgnitionCmd := FALSE;
        rEngineThrottleOut := 0.0;
        IF bEmergencyStop AND NOT bEnable THEN
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
