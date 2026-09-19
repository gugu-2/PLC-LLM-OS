import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Large-Scale Space Observatory Dome Rotation and Telescope Shutter Tracking**

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_Observatory_DomeTracking\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Large-Scale Space Observatory Dome Rotation and Telescope Shutter Tracking

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_ObservatoryDomeControl
VAR_INPUT
    bSystemEnable       : BOOL;     (* Master enable signal for the dome tracking system *)
    bEmergencyStop      : BOOL;     (* Safety relay OK signal (active high) *)
    rTelescopeAzimuth   : REAL;     (* Current telescope azimuth in degrees (0.0 - 360.0) *)
    rWindSpeed          : REAL;     (* Current external wind speed in m/s *)
    bRainSensor         : BOOL;     (* Rain detection sensor (TRUE = rain detected) *)
    rDomeCurrentAzimuth : REAL;     (* Current dome azimuth feedback from absolute encoder *)
    rDomeSpeedRef       : REAL;     (* Requested dome rotation speed reference *)
    bShutterOpenReq     : BOOL;     (* Request to open the observation shutter *)
END_VAR
VAR_OUTPUT
    bSystemReady        : BOOL;     (* Tracking system ready for operation *)
    rDomeMotorCmd       : REAL;     (* Velocity command to dome rotation VFD (-100.0 to 100.0%) *)
    bShutterCmd         : BOOL;     (* Command to open/close shutter (TRUE = open) *)
    bAlarmState         : BOOL;     (* Active alarm or fault condition *)
    iTrackingState      : INT;      (* Current tracking state machine value *)
END_VAR
VAR
    iState              : INT := 0; (* Internal state machine *)
    rAzimuthError       : REAL;     (* Difference between telescope and dome azimuth *)
    rFilteredWindSpeed  : REAL;     (* Low-pass filtered wind speed *)
    tShutterTimer       : TON;      (* Timer for shutter movement sequencing *)
    tFaultTimer         : TON;      (* Delay timer for transient fault filtering *)
    rKp                 : REAL := 2.5; (* Proportional gain for position control *)
    bWeatherSafe        : BOOL;     (* Weather condition evaluation flag *)
END_VAR

(* === MAIN LOGIC === *)
(* Emergency and Safety Interlocks *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bAlarmState := TRUE;
    rDomeMotorCmd := 0.0;
    bShutterCmd := FALSE;
    iState := 99; (* Fault state *)
    RETURN;
END_IF;

(* Weather Filtering and Assessment *)
rFilteredWindSpeed := (rFilteredWindSpeed * 0.9) + (rWindSpeed * 0.1);
IF (rFilteredWindSpeed > 15.0) OR bRainSensor THEN
    bWeatherSafe := FALSE;
ELSE
    bWeatherSafe := TRUE;
END_IF;

(* Azimuth Error Calculation (Shortest Path) *)
rAzimuthError := rTelescopeAzimuth - rDomeCurrentAzimuth;
IF rAzimuthError > 180.0 THEN
    rAzimuthError := rAzimuthError - 360.0;
ELSIF rAzimuthError < -180.0 THEN
    rAzimuthError := rAzimuthError + 360.0;
END_IF;

CASE iState OF
    0: (* IDLE & INITIALIZATION *)
        rDomeMotorCmd := 0.0;
        bShutterCmd := FALSE;
        IF bSystemEnable AND bWeatherSafe THEN
            bSystemReady := TRUE;
            bAlarmState := FALSE;
            iState := 10;
        END_IF;

    10: (* TRACKING ACTIVE *)
        bSystemReady := TRUE;
        bAlarmState := FALSE;
        
        (* Proportional tracking control with deadband *)
        IF ABS(rAzimuthError) > 2.0 THEN
            rDomeMotorCmd := rAzimuthError * rKp;
            (* Clamp command *)
            IF rDomeMotorCmd > 100.0 THEN rDomeMotorCmd := 100.0; END_IF;
            IF rDomeMotorCmd < -100.0 THEN rDomeMotorCmd := -100.0; END_IF;
        ELSE
            rDomeMotorCmd := 0.0;
        END_IF;

        (* Shutter Control Logic *)
        IF bShutterOpenReq AND bWeatherSafe AND ABS(rAzimuthError) < 5.0 THEN
            bShutterCmd := TRUE;
        ELSE
            bShutterCmd := FALSE;
        END_IF;

        (* Weather Fault transition *)
        IF NOT bWeatherSafe THEN
            iState := 20;
        END_IF;
        
        IF NOT bSystemEnable THEN
            iState := 0;
        END_IF;

    20: (* WEATHER SECURING SEQUENCE *)
        bSystemReady := FALSE;
        rDomeMotorCmd := 0.0;
        bShutterCmd := FALSE; (* Force shutter close *)
        
        tShutterTimer(IN := TRUE, PT := T#30S);
        IF tShutterTimer.Q THEN
            tShutterTimer(IN := FALSE);
            bAlarmState := TRUE;
            iState := 99;
        END_IF;

    99: (* FAULT STATE *)
        bSystemReady := FALSE;
        rDomeMotorCmd := 0.0;
        bShutterCmd := FALSE;
        IF NOT bAlarmState AND bSystemEnable THEN
            iState := 0;
        END_IF;
END_CASE;

iTrackingState := iState;

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
