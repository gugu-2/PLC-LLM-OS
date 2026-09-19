import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Automated Commercial Ship Hull Cleaning ROV Thruster Vectoring and Biofouling Brush Control**

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_HullCleaning_ROV\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Automated Commercial Ship Hull Cleaning ROV Thruster Vectoring and Biofouling Brush Control

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_ROV_HullCleanerControl
(* 
   =============================================================================
   Title:           ROV Thruster Vectoring and Biofouling Brush Control
   Description:     Provides deterministic 6-DOF thruster vectoring, depth tracking,
                    and active biofouling brush torque/speed regulation for an 
                    automated commercial ship hull cleaning ROV.
   Author:          Lumina Elite Architect (40 yr veteran)
   Version:         3.1.4
   =============================================================================
*)
VAR_INPUT
    (* Subsea Environment & Sensors *)
    bEnable                 : BOOL;     (* System global enable *)
    bEmergencyStop          : BOOL;     (* Hardware E-Stop OK relay signal *)
    rDepthSensorMeters      : REAL;     (* Hydrostatic pressure converted to depth (m) *)
    rPitchAngleDeg          : REAL;     (* IMU pitch angle (degrees) *)
    rRollAngleDeg           : REAL;     (* IMU roll angle (degrees) *)
    rHullDistanceMm         : REAL;     (* Ultrasonic acoustic altimeter distance to hull *)
    rBrushMotorCurrentA     : REAL;     (* Brush motor current feedback (Amps) *)
    bWaterLeakDetected      : BOOL;     (* Hull/canister leak detection switch *)
    
    (* Setpoints *)
    rTargetDepthMeters      : REAL;
    rTargetHullDistMm       : REAL;
    rTargetBrushSpeedRPM    : REAL;
END_VAR

VAR_OUTPUT
    (* Actuators & Control Vectors *)
    bSystemReady            : BOOL;     (* System ready for autonomous operation *)
    rThrusterVertCmd        : REAL;     (* Vertical thruster command (-100.0 to 100.0 %) *)
    rThrusterLatCmd         : REAL;     (* Lateral thruster command (-100.0 to 100.0 %) *)
    rBrushMotorCmd          : REAL;     (* Brush motor speed command (0.0 to 100.0 %) *)
    
    (* Status & Diagnostics *)
    bAlarmActive            : BOOL;     (* General fault alarm *)
    iFaultCode              : INT;      (* Diagnostics fault code *)
    bCleaningActive         : BOOL;     (* Indicates active biofouling removal phase *)
END_VAR

VAR
    (* Internal States & PIDs *)
    iState                  : INT := 0; (* 0=IDLE, 10=INIT, 20=APPROACH, 30=CLEANING, 99=FAULT *)
    tStateTimer             : TON;
    rFilteredDepth          : REAL;
    rDepthError             : REAL;
    rDepthIntegral          : REAL;
    
    (* Filter Constants *)
    rAlpha                  : REAL := 0.15; (* Low-pass filter coefficient *)
    
    (* Control Gains *)
    rKpDepth                : REAL := 25.0;
    rKiDepth                : REAL := 1.2;
    rKpBrush                : REAL := 0.5;
END_VAR

(* === MAIN SAFETY INTERLOCKS === *)
IF NOT bEmergencyStop OR bWaterLeakDetected THEN
    iState := 99;
    iFaultCode := 1001; (* Critical hardware fault or leak *)
END_IF;

(* Sensor Noise Filtering *)
rFilteredDepth := (rAlpha * rDepthSensorMeters) + ((1.0 - rAlpha) * rFilteredDepth);

(* State Machine *)
CASE iState OF
    0: (* IDLE *)
        bSystemReady := FALSE;
        bAlarmActive := FALSE;
        rThrusterVertCmd := 0.0;
        rThrusterLatCmd := 0.0;
        rBrushMotorCmd := 0.0;
        bCleaningActive := FALSE;
        
        IF bEnable AND bEmergencyStop THEN
            iState := 10;
        END_IF;
        
    10: (* INIT *)
        bSystemReady := TRUE;
        rDepthIntegral := 0.0;
        tStateTimer(IN := TRUE, PT := T#3S);
        IF tStateTimer.Q THEN
            tStateTimer(IN := FALSE);
            iState := 20;
        END_IF;
        
    20: (* APPROACH HULL *)
        (* Depth PID Control *)
        rDepthError := rTargetDepthMeters - rFilteredDepth;
        rDepthIntegral := rDepthIntegral + (rDepthError * 0.1); (* Assuming 100ms cycle *)
        
        (* Anti-windup *)
        IF rDepthIntegral > 50.0 THEN rDepthIntegral := 50.0; END_IF;
        IF rDepthIntegral < -50.0 THEN rDepthIntegral := -50.0; END_IF;
        
        rThrusterVertCmd := (rKpDepth * rDepthError) + (rKiDepth * rDepthIntegral);
        
        (* Limit Outputs *)
        IF rThrusterVertCmd > 100.0 THEN rThrusterVertCmd := 100.0; END_IF;
        IF rThrusterVertCmd < -100.0 THEN rThrusterVertCmd := -100.0; END_IF;
        
        (* Check approach criteria *)
        IF ABS(rTargetHullDistMm - rHullDistanceMm) < 50.0 THEN
            iState := 30;
        END_IF;
        
        IF NOT bEnable THEN
            iState := 0;
        END_IF;

    30: (* CLEANING *)
        bCleaningActive := TRUE;
        
        (* Lateral force to push against hull *)
        rThrusterLatCmd := 45.0; 
        
        (* Brush speed control with basic overload protection *)
        IF rBrushMotorCurrentA > 25.0 THEN
            rBrushMotorCmd := rBrushMotorCmd * 0.8; (* Back off torque *)
        ELSE
            rBrushMotorCmd := rTargetBrushSpeedRPM * rKpBrush;
        END_IF;
        
        IF rBrushMotorCmd > 100.0 THEN rBrushMotorCmd := 100.0; END_IF;
        
        IF rHullDistanceMm > (rTargetHullDistMm + 200.0) THEN
            (* Lost hull contact *)
            bCleaningActive := FALSE;
            rBrushMotorCmd := 0.0;
            iState := 20;
        END_IF;
        
        IF NOT bEnable THEN
            iState := 0;
        END_IF;
        
    99: (* FAULT *)
        bSystemReady := FALSE;
        bAlarmActive := TRUE;
        bCleaningActive := FALSE;
        rThrusterVertCmd := 0.0;
        rThrusterLatCmd := 0.0;
        rBrushMotorCmd := 0.0;
        
        IF NOT bWaterLeakDetected AND bEmergencyStop AND NOT bEnable THEN
            (* Reset condition *)
            iState := 0;
            iFaultCode := 0;
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

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print(f"Saved to {filename}")
