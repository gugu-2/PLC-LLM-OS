import json, uuid, os

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Deep-Sea Cable Laying Remotely Operated Trenching Plow**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Subsea hydraulic traction winching, seabed soil density feed-forward blade depth compensation, and dynamic pitch/roll stabilization under 300-bar ambient pressure). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_Subsea_TrenchingPlow\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Deep-Sea Cable Laying Remotely Operated Trenching Plow

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_TrenchingPlowControl
VAR_INPUT
    (* Required: at least 4-8 physical inputs with types and comments *)
    bEnable            : BOOL;     (* System enable signal from topside vessel *)
    bEmergencyStop     : BOOL;     (* Safety relay OK signal - TRUE means safe *)
    rAmbientPressure   : REAL;     (* Ambient pressure in Bar, approx 300 Bar at 3000m *)
    rSoilDensity       : REAL;     (* Forward acoustic sensor soil density reading (kg/m^3) *)
    rPitchAngle        : REAL;     (* Inclinometer Pitch angle in degrees *)
    rRollAngle         : REAL;     (* Inclinometer Roll angle in degrees *)
    rTargetTrenchDepth : REAL;     (* Target burial depth for the cable (meters) *)
    rCurrentBladeDepth : REAL;     (* Actual measured blade depth from LVDT (meters) *)
END_VAR
VAR_OUTPUT
    (* Required: at least 3-6 outputs with types and comments *)
    bSystemReady       : BOOL;     (* System ready status *)
    bAlarm             : BOOL;     (* Fault alarm output (Critical Failure) *)
    rBladeHydraulicOut : REAL;     (* Control signal to blade hydraulic actuator (-100 to 100%) *)
    rLeftTrackSpeed    : REAL;     (* Hydraulic speed command to left track (%) *)
    rRightTrackSpeed   : REAL;     (* Hydraulic speed command to right track (%) *)
    iCurrentState      : INT;      (* Diagnostics: Current active state of the FB *)
END_VAR
VAR
    (* Internal state variables *)
    iState             : INT := 0; (* Internal State Machine variable *)
    tTimer             : TON;
    rFilteredDensity   : REAL := 1500.0; (* Low-pass filtered soil density *)
    rDepthError        : REAL;
    rDepthIntegral     : REAL := 0.0;
    rDepthDerivative   : REAL := 0.0;
    rPrevDepthError    : REAL := 0.0;
    rFeedForwardTerm   : REAL;
    rPIDOutput         : REAL;
    
    (* Constants for PID & Filters *)
    Kp                 : REAL := 45.5;
    Ki                 : REAL := 2.1;
    Kd                 : REAL := 15.0;
    Alpha_Density      : REAL := 0.1; (* Filter coefficient *)
    Max_Pitch          : REAL := 15.0; (* Degrees before stability limits exceeded *)
    Max_Roll           : REAL := 10.0; (* Degrees before stability limits exceeded *)
END_VAR

(* === MAIN LOGIC === *)
(* 1. Safety & Interlock Checking *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bAlarm := TRUE;
    rBladeHydraulicOut := 0.0;
    rLeftTrackSpeed := 0.0;
    rRightTrackSpeed := 0.0;
    iState := 99; (* Force to Fault State *)
    iCurrentState := iState;
    RETURN;
END_IF;

(* 2. Signal Processing (Sensor Filtering) *)
rFilteredDensity := (Alpha_Density * rSoilDensity) + ((1.0 - Alpha_Density) * rFilteredDensity);

(* 3. Active State Machine *)
CASE iState OF
    0: (* IDLE - Waiting for Topsides Enable *)
        bSystemReady := TRUE;
        bAlarm := FALSE;
        rBladeHydraulicOut := 0.0;
        rLeftTrackSpeed := 0.0;
        rRightTrackSpeed := 0.0;
        IF bEnable THEN
            iState := 10; (* Move to Prep/Calibration *)
        END_IF;

    10: (* PREP & CALIBRATION *)
        bSystemReady := TRUE;
        (* Verify environmental constraints before deploying blade *)
        IF ABS(rPitchAngle) > Max_Pitch OR ABS(rRollAngle) > Max_Roll THEN
            bAlarm := TRUE;
            iState := 99; (* Terrain too steep/unstable *)
        ELSIF rAmbientPressure < 10.0 THEN
            (* Safety Check: Must be subsea to operate hydraulics fully *)
            bAlarm := TRUE;
            iState := 99;
        ELSE
            tTimer(IN := TRUE, PT := T#5S);
            IF tTimer.Q THEN
                tTimer(IN := FALSE);
                iState := 20; (* Proceed to Trenching *)
            END_IF;
        END_IF;

    20: (* ACTIVE TRENCHING / PID & FEED-FORWARD CONTROL *)
        bSystemReady := TRUE;
        bAlarm := FALSE;

        (* PID calculation for Blade Depth Control *)
        rDepthError := rTargetTrenchDepth - rCurrentBladeDepth;
        rDepthIntegral := rDepthIntegral + (rDepthError * 0.1); (* Assuming 100ms cycle *)
        
        (* Anti-windup for integral term *)
        IF rDepthIntegral > 50.0 THEN rDepthIntegral := 50.0; END_IF;
        IF rDepthIntegral < -50.0 THEN rDepthIntegral := -50.0; END_IF;

        rDepthDerivative := (rDepthError - rPrevDepthError) / 0.1;
        rPrevDepthError := rDepthError;

        (* Feed-Forward based on soil density: Harder soil requires more downward pressure *)
        rFeedForwardTerm := (rFilteredDensity - 1000.0) * 0.05;

        (* Calculate Final Hydraulic Output *)
        rPIDOutput := (Kp * rDepthError) + (Ki * rDepthIntegral) + (Kd * rDepthDerivative) + rFeedForwardTerm;

        (* Clamp output to realistic hydraulic actuator limits [-100%, 100%] *)
        IF rPIDOutput > 100.0 THEN
            rBladeHydraulicOut := 100.0;
        ELSIF rPIDOutput < -100.0 THEN
            rBladeHydraulicOut := -100.0;
        ELSE
            rBladeHydraulicOut := rPIDOutput;
        END_IF;

        (* Traction Control with Roll Stabilization Compensation *)
        (* If rolled right, increase right track speed slightly to compensate drag *)
        rLeftTrackSpeed := 50.0 - (rRollAngle * 1.5); 
        rRightTrackSpeed := 50.0 + (rRollAngle * 1.5);

        IF NOT bEnable THEN
            iState := 0; (* Return to Idle if enable dropped *)
        END_IF;

    99: (* FAULT STATE *)
        bSystemReady := FALSE;
        rBladeHydraulicOut := 0.0;
        rLeftTrackSpeed := 0.0;
        rRightTrackSpeed := 0.0;
        (* Requires E-Stop toggle to reset *)
        IF NOT bEnable THEN
            bAlarm := FALSE;
            iState := 0;
        END_IF;

END_CASE;

iCurrentState := iState;

END_FUNCTION_BLOCK
```"""

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
