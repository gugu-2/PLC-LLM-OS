import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Commercial Aviation Composite Fuselage Automated Tape Laying (ATL)**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., 12-axis gantry synchronous kinematics, ultra-sonic tape cutter dynamic tensioning, and laser line-scan gap/overlap dimensional tracking). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_AviationATL\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Commercial Aviation Composite Fuselage Automated Tape Laying (ATL)

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_AviationFuselageATL_Control
VAR_INPUT
    bEnableRun          : BOOL;         (* Master enable for the ATL sequence *)
    bSafetyOk           : BOOL;         (* Safety curtain and interlocks OK *)
    rTapeTensionSet     : REAL;         (* Desired tape tension in Newtons *)
    rLayupSpeedSet      : REAL;         (* Setpoint for layup speed in mm/s *)
    rLaserGapTolerance  : REAL;         (* Maximum allowable gap/overlap in mm *)
    rHeatShoeTempSet    : REAL;         (* Target temperature for heat shoe in degC *)
    bUltrasonicCutterOk : BOOL;         (* Ultrasonic cutter subsystem status ready *)
    aAxesPositions      : ARRAY[1..12] OF REAL; (* Real-time feedback from 12-axis gantry *)
END_VAR
VAR_OUTPUT
    bSystemReady        : BOOL;         (* System ready to commence layup *)
    bActiveLaying       : BOOL;         (* Tape is actively being laid down *)
    rTapeTensionCmd     : REAL;         (* Tension command to dynamic tensioner *)
    aAxesCommands       : ARRAY[1..12] OF REAL; (* Motion commands to 12-axis gantry *)
    bAlarmState         : BOOL;         (* Fault condition exists *)
    iErrorCode          : INT;          (* Detailed error code for diagnostics *)
END_VAR
VAR
    iMainState          : INT := 0;     (* State machine internal state *)
    rCurrentTension     : REAL := 0.0;  (* Filtered actual tension *)
    rCurrentGap         : REAL := 0.0;  (* Laser scanned gap measurement *)
    rPID_Integral       : REAL := 0.0;  (* PID integral term for tension *)
    rPID_ErrorPrev      : REAL := 0.0;  (* PID previous error for derivative *)
    tProcessDelay       : TON;          (* Process stabilization timer *)
    tHeatShoeWarmup     : TON;          (* Heat shoe stabilization timer *)
    rKp                 : REAL := 2.5;  (* Proportional gain *)
    rKi                 : REAL := 0.5;  (* Integral gain *)
    rKd                 : REAL := 0.1;  (* Derivative gain *)
END_VAR

(* === MAIN LOGIC === *)
IF NOT bSafetyOk THEN
    bSystemReady := FALSE;
    bActiveLaying := FALSE;
    bAlarmState := TRUE;
    iErrorCode := 100; (* 100: Safety Interlock Broken *)
    rTapeTensionCmd := 0.0;
    iMainState := 0;
    RETURN;
END_IF;

CASE iMainState OF
    0: (* INIT AND IDLE *)
        bSystemReady := TRUE;
        bActiveLaying := FALSE;
        bAlarmState := FALSE;
        iErrorCode := 0;
        
        IF bEnableRun AND bUltrasonicCutterOk THEN
            iMainState := 10;
        ELSIF bEnableRun AND NOT bUltrasonicCutterOk THEN
            bAlarmState := TRUE;
            iErrorCode := 201; (* 201: Cutter Not Ready *)
        END_IF;

    10: (* HEATER WARMUP AND TENSION PRELOAD *)
        bSystemReady := FALSE;
        rTapeTensionCmd := rTapeTensionSet * 0.1; (* Pre-tension *)
        
        tHeatShoeWarmup(IN := TRUE, PT := T#10S);
        IF tHeatShoeWarmup.Q THEN
            tHeatShoeWarmup(IN := FALSE);
            iMainState := 20;
        END_IF;

    20: (* ACTIVE LAYUP AND SYNCHRONOUS KINEMATICS *)
        bActiveLaying := TRUE;
        
        (* Dynamic Tension Control PID *)
        rPID_Integral := rPID_Integral + (rTapeTensionSet - rCurrentTension);
        rTapeTensionCmd := (rKp * (rTapeTensionSet - rCurrentTension)) + (rKi * rPID_Integral) + (rKd * ((rTapeTensionSet - rCurrentTension) - rPID_ErrorPrev));
        rPID_ErrorPrev := rTapeTensionSet - rCurrentTension;
        
        (* Laser Line-Scan Gap/Overlap Validation *)
        IF rCurrentGap > rLaserGapTolerance THEN
            bAlarmState := TRUE;
            iErrorCode := 305; (* 305: Gap Tolerance Exceeded *)
            iMainState := 99; (* Go to error recovery *)
        END_IF;
        
        (* 12-Axis Synchronized Path Interpolation (Simulated output mapped to speed) *)
        aAxesCommands[1] := aAxesPositions[1] + rLayupSpeedSet * 0.01;
        aAxesCommands[2] := aAxesPositions[2] + rLayupSpeedSet * 0.01;
        
        tProcessDelay(IN := TRUE, PT := T#60S); (* Simulate layup cycle time *)
        IF tProcessDelay.Q THEN
            tProcessDelay(IN := FALSE);
            iMainState := 30;
        END_IF;
        
        IF NOT bEnableRun THEN
            iMainState := 30; (* Graceful stop *)
        END_IF;

    30: (* RAMP DOWN AND CUT *)
        bActiveLaying := FALSE;
        rTapeTensionCmd := 0.0;
        iMainState := 0;

    99: (* FAULT HANDLING *)
        bActiveLaying := FALSE;
        rTapeTensionCmd := 0.0;
        IF NOT bEnableRun THEN
            iMainState := 0; (* Reset fault on disable *)
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
