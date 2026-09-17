import json, uuid, os

prompt = """<USER_REQUEST>
You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Large-Scale Stadium Retractable Roof Hydraulic Actuation and Wind Load Safety Override**

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_StadiumRoof_Actuation\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Large-Scale Stadium Retractable Roof Hydraulic Actuation and Wind Load Safety Override

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT.
</USER_REQUEST>"""

code = """```iec-st
FUNCTION_BLOCK FB_StadiumRoof_Actuation
(* 
   =============================================================================
   Large-Scale Stadium Retractable Roof Hydraulic Actuation and Wind Load Safety
   Architecture: Triple-redundant PLC layout
   Designer: Chief Automation Architect (40+ years experience)
   =============================================================================
*)
VAR_INPUT
    bSystemEnable       : BOOL;     (* Master enable for the roof hydraulic system *)
    bEmergencyStop      : BOOL;     (* E-Stop safety relay OK signal, normally closed (TRUE = OK) *)
    rWindSpeedAvg_ms    : REAL;     (* 10-minute average wind speed from primary anemometer (m/s) *)
    rWindSpeedGust_ms   : REAL;     (* Instantaneous wind gust reading (m/s) *)
    rHydraulicPressure1 : REAL;     (* Primary hydraulic loop pressure (Bar) *)
    rHydraulicPressure2 : REAL;     (* Secondary hydraulic loop pressure (Bar) *)
    rPositionFeedback   : REAL;     (* Absolute encoder feedback for roof position (0.0 to 100.0%) *)
    bOpenCommand        : BOOL;     (* Operator command to OPEN roof *)
    bCloseCommand       : BOOL;     (* Operator command to CLOSE roof *)
END_VAR
VAR_OUTPUT
    bSystemReady        : BOOL;     (* System is primed, pressurized, and ready for actuation *)
    rValveControlSignal : REAL;     (* 4-20mA equivalent (0.0 to 100.0) control signal to proportional valves *)
    bSafetyOverride     : BOOL;     (* TRUE if wind load or pressure anomalies trigger a safety lock *)
    bMovementActive     : BOOL;     (* TRUE when the roof is currently in motion *)
    bAlarmFault         : BOOL;     (* Major fault requiring manual reset *)
    iErrorCode          : INT;      (* Diagnostic error code for HMI display *)
END_VAR
VAR
    iState              : INT := 0; 
    tMotionTimeout      : TON;
    tSafetyDelay        : TON;
    rFilteredWindSpeed  : REAL := 0.0;
    rTargetPosition     : REAL := 0.0;
    rErrorLimit         : REAL := 2.5; 
    bPressureOK         : BOOL := FALSE;
    bWindSafe           : BOOL := TRUE;
    rAlpha              : REAL := 0.1; (* Low-pass filter coefficient for wind speed *)
END_VAR

(* === MAIN LOGIC === *)
(* 1. Safety Interlocks & Emergency Handling *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bSafetyOverride := TRUE;
    bMovementActive := FALSE;
    rValveControlSignal := 0.0;
    bAlarmFault := TRUE;
    iErrorCode := 999; (* 999: E-Stop Activated *)
    iState := 0;
    RETURN;
END_IF;

(* 2. Sensor Noise Filtering - Low-pass filter on wind gust *)
rFilteredWindSpeed := (rAlpha * rWindSpeedGust_ms) + ((1.0 - rAlpha) * rFilteredWindSpeed);

(* 3. Wind Load Safety Evaluation *)
IF (rWindSpeedAvg_ms > 15.0) OR (rFilteredWindSpeed > 22.0) THEN
    bWindSafe := FALSE;
    tSafetyDelay(IN := TRUE, PT := T#3S);
    IF tSafetyDelay.Q THEN
        bSafetyOverride := TRUE;
        iErrorCode := 101; (* 101: Wind limit exceeded *)
    END_IF;
ELSE
    bWindSafe := TRUE;
    tSafetyDelay(IN := FALSE);
    bSafetyOverride := FALSE;
END_IF;

(* 4. Hydraulic Pressure Redundancy Check *)
IF (rHydraulicPressure1 > 180.0 AND rHydraulicPressure1 < 220.0) AND 
   (rHydraulicPressure2 > 180.0 AND rHydraulicPressure2 < 220.0) THEN
    bPressureOK := TRUE;
ELSE
    bPressureOK := FALSE;
END_IF;

(* 5. State Machine for Roof Actuation *)
CASE iState OF
    0: (* IDLE & SYSTEM CHECK *)
        bMovementActive := FALSE;
        rValveControlSignal := 0.0;
        IF bSystemEnable AND bWindSafe AND bPressureOK THEN
            bSystemReady := TRUE;
            iErrorCode := 0;
            IF bOpenCommand AND NOT bCloseCommand AND rPositionFeedback < 99.0 THEN
                rTargetPosition := 100.0;
                iState := 10;
            ELSIF bCloseCommand AND NOT bOpenCommand AND rPositionFeedback > 1.0 THEN
                rTargetPosition := 0.0;
                iState := 20;
            END_IF;
        ELSE
            bSystemReady := FALSE;
            IF NOT bPressureOK THEN
                iErrorCode := 202; (* 202: Pressure fault *)
            END_IF;
        END_IF;

    10: (* OPENING ROOF *)
        IF NOT bWindSafe THEN
            iState := 50; (* Transition to Safety Hold *)
        ELSIF rPositionFeedback >= 99.5 THEN
            rValveControlSignal := 0.0;
            iState := 0;
        ELSE
            bMovementActive := TRUE;
            rValveControlSignal := 75.0; (* 75% flow rate *)
            tMotionTimeout(IN := TRUE, PT := T#300S); (* 5 mins max per move *)
            IF tMotionTimeout.Q THEN
                iState := 99; (* Timeout Fault *)
            END_IF;
        END_IF;

    20: (* CLOSING ROOF *)
        IF NOT bPressureOK THEN
            iState := 50; (* Holding state *)
        ELSIF rPositionFeedback <= 0.5 THEN
            rValveControlSignal := 0.0;
            iState := 0;
        ELSE
            bMovementActive := TRUE;
            rValveControlSignal := -75.0; (* Negative flow or directional logic *)
            tMotionTimeout(IN := TRUE, PT := T#300S);
            IF tMotionTimeout.Q THEN
                iState := 99; (* Timeout Fault *)
            END_IF;
        END_IF;

    50: (* SAFETY HOLD MID-MOTION *)
        bMovementActive := FALSE;
        rValveControlSignal := 0.0;
        tMotionTimeout(IN := FALSE);
        IF bWindSafe AND bPressureOK AND bSystemEnable THEN
            (* Operator must re-issue command to resume *)
            iState := 0; 
        END_IF;

    99: (* FATAL MOTION FAULT *)
        bMovementActive := FALSE;
        rValveControlSignal := 0.0;
        bAlarmFault := TRUE;
        iErrorCode := 500; (* Motion Timeout / Actuator jam *)
        (* Requires E-Stop cycle or maintenance reset to clear *)

END_CASE;

END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
print(f"Saved to {filename}")
