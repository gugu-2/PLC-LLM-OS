import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Industrial High-Tonnage Hydraulic Stamping Press Vibration Damper**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., 2000-ton hydraulic blanking breakout shock absorption, servo-hydraulic proportional counter-cylinder pre-pressurization, and structural foundation accelerometer active damping). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_StampingPress_VibrationDamper\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Industrial High-Tonnage Hydraulic Stamping Press Vibration Damper

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_StampingPress_VibrationDamper
VAR_INPUT
    bEnable               : BOOL;   (* System enable signal *)
    bEmergencyStop        : BOOL;   (* Safety relay OK signal - active HIGH for safe *)
    bPressCycleStart      : BOOL;   (* Trigger signal from master press controller *)
    rAccelX               : REAL;   (* Foundation accelerometer X-axis [g] *)
    rAccelY               : REAL;   (* Foundation accelerometer Y-axis [g] *)
    rAccelZ               : REAL;   (* Foundation accelerometer Z-axis [g] *)
    rMainRamPos           : REAL;   (* Main press ram position feedback [mm] *)
    rMainRamVel           : REAL;   (* Main press ram velocity feedback [mm/s] *)
    rCylinderPressA       : REAL;   (* Counter-cylinder A pressure [bar] *)
    rCylinderPressB       : REAL;   (* Counter-cylinder B pressure [bar] *)
END_VAR
VAR_OUTPUT
    bSystemReady          : BOOL;   (* Damper system ready for next cycle *)
    rValveCtrlA           : REAL;   (* Servo valve A control output [-100.0..100.0%] *)
    rValveCtrlB           : REAL;   (* Servo valve B control output [-100.0..100.0%] *)
    bActiveDampingOn      : BOOL;   (* Active damping phase in progress *)
    bAlarm                : BOOL;   (* Fault alarm output *)
    iErrorCode            : INT;    (* Specific error code if bAlarm is TRUE *)
END_VAR
VAR
    iState                : INT := 0;
    tWatchdog             : TON;
    tDampingDuration      : TON;
    rFilteredAccelZ       : REAL := 0.0;
    rTargetPressureA      : REAL := 0.0;
    rTargetPressureB      : REAL := 0.0;
    rErrorA               : REAL := 0.0;
    rErrorB               : REAL := 0.0;
    
    (* Filter constants *)
    rAlphaAccel           : REAL := 0.15; (* Low pass filter coefficient for accelerometer *)
    
    (* PID Constants for counter-cylinder pressure control *)
    rKp                   : REAL := 2.5;
    rKi                   : REAL := 0.8;
    rKd                   : REAL := 0.05;
    rIntegralA            : REAL := 0.0;
    rIntegralB            : REAL := 0.0;
    rPrevErrorA           : REAL := 0.0;
    rPrevErrorB           : REAL := 0.0;
    
    (* Shock parameters *)
    rBreakoutThreshold    : REAL := 2.5; (* Z-acceleration threshold indicating material breakout [g] *)
    rPrePressurizePos     : REAL := 50.0; (* Ram position [mm] to start pre-pressurization *)
END_VAR

(* === MAIN LOGIC === *)
(* Emergency Stop Interlock *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bActiveDampingOn := FALSE;
    rValveCtrlA := 0.0;
    rValveCtrlB := 0.0;
    bAlarm := TRUE;
    iErrorCode := 9999; (* E-Stop active *)
    iState := 0;
    RETURN;
END_IF;

(* Continuous Sensor Filtering *)
rFilteredAccelZ := (rAlphaAccel * rAccelZ) + ((1.0 - rAlphaAccel) * rFilteredAccelZ);

(* Main State Machine *)
CASE iState OF
    0: (* IDLE & FAULT RESET *)
        bSystemReady := FALSE;
        bActiveDampingOn := FALSE;
        rValveCtrlA := 0.0;
        rValveCtrlB := 0.0;
        rIntegralA := 0.0;
        rIntegralB := 0.0;
        
        IF bEnable AND bEmergencyStop THEN
            bAlarm := FALSE;
            iErrorCode := 0;
            iState := 10;
        END_IF;

    10: (* READY TO CYCLE *)
        bSystemReady := TRUE;
        bActiveDampingOn := FALSE;
        
        IF bPressCycleStart THEN
            bSystemReady := FALSE;
            iState := 20;
        ELSIF NOT bEnable THEN
            iState := 0;
        END_IF;

    20: (* MONITORING RAM POSITION FOR PRE-PRESSURIZATION *)
        IF rMainRamPos <= rPrePressurizePos AND rMainRamVel < -10.0 THEN
            (* Ram is approaching bottom dead center fast, start pre-pressurizing *)
            iState := 30;
        END_IF;
        
        (* Safety timeout or cycle abort could be handled here *)
        IF NOT bPressCycleStart THEN
            iState := 10;
        END_IF;

    30: (* PRE-PRESSURIZATION & ACTIVE DAMPING (BREAKOUT PHASE) *)
        bActiveDampingOn := TRUE;
        
        (* Calculate dynamic target pressure based on RAM velocity to anticipate shock *)
        rTargetPressureA := ABS(rMainRamVel) * 1.5; 
        rTargetPressureB := ABS(rMainRamVel) * 1.5;
        
        (* Detect shock via filtered Z acceleration *)
        IF rFilteredAccelZ > rBreakoutThreshold THEN
            (* Intense breakout shock detected, boost target pressure massively *)
            rTargetPressureA := rTargetPressureA + (rFilteredAccelZ * 50.0);
            rTargetPressureB := rTargetPressureB + (rFilteredAccelZ * 50.0);
        END_IF;
        
        (* Clamp target pressures to safe structural limits (e.g. max 300 bar) *)
        IF rTargetPressureA > 300.0 THEN rTargetPressureA := 300.0; END_IF;
        IF rTargetPressureB > 300.0 THEN rTargetPressureB := 300.0; END_IF;

        (* PID Controller for Cylinder A *)
        rErrorA := rTargetPressureA - rCylinderPressA;
        rIntegralA := rIntegralA + rErrorA;
        rValveCtrlA := (rKp * rErrorA) + (rKi * rIntegralA) + (rKd * (rErrorA - rPrevErrorA));
        rPrevErrorA := rErrorA;
        
        (* PID Controller for Cylinder B *)
        rErrorB := rTargetPressureB - rCylinderPressB;
        rIntegralB := rIntegralB + rErrorB;
        rValveCtrlB := (rKp * rErrorB) + (rKi * rIntegralB) + (rKd * (rErrorB - rPrevErrorB));
        rPrevErrorB := rErrorB;
        
        (* Output Clamping *)
        IF rValveCtrlA > 100.0 THEN rValveCtrlA := 100.0; ELSIF rValveCtrlA < -100.0 THEN rValveCtrlA := -100.0; END_IF;
        IF rValveCtrlB > 100.0 THEN rValveCtrlB := 100.0; ELSIF rValveCtrlB < -100.0 THEN rValveCtrlB := -100.0; END_IF;

        (* Damping phase duration timer *)
        tDampingDuration(IN := TRUE, PT := T#500MS);
        IF tDampingDuration.Q THEN
            tDampingDuration(IN := FALSE);
            iState := 40;
        END_IF;

    40: (* DECOMPRESSION & RECOVERY *)
        bActiveDampingOn := FALSE;
        rValveCtrlA := -50.0; (* Open return lines to bleed pressure *)
        rValveCtrlB := -50.0;
        
        IF rCylinderPressA < 10.0 AND rCylinderPressB < 10.0 THEN
            rValveCtrlA := 0.0;
            rValveCtrlB := 0.0;
            iState := 50;
        END_IF;

    50: (* CYCLE COMPLETE WAITING *)
        bSystemReady := TRUE;
        IF NOT bPressCycleStart THEN
            iState := 10;
        END_IF;
        
    ELSE
        (* Invalid State recovery *)
        bAlarm := TRUE;
        iErrorCode := iState;
        iState := 0;
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
