import os, json, uuid

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Industrial Scale Wind Turbine Nacelle Yaw Drive and Cable Untwist Synchronization**

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_WindTurbine_Yaw\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Industrial Scale Wind Turbine Nacelle Yaw Drive and Cable Untwist Synchronization

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_WTG_YawDrive_Untwist_Sync
(* 
    Industrial Scale Wind Turbine Nacelle Yaw Drive and Cable Untwist Synchronization
    Advanced Control Algorithm with Fault Tolerance, PID Filtering, and Safety Interlocks
*)
VAR_INPUT
    bEnable                 : BOOL;     (* Master system enable signal from top-level controller *)
    bEmergencyStop          : BOOL;     (* Safety loop OK signal, MUST be TRUE to operate *)
    rWindDirection          : REAL;     (* Filtered external wind direction measurement [0..359.9 deg] *)
    rNacellePosition        : REAL;     (* Current Nacelle absolute position [-720.0 .. 720.0 deg] *)
    rWindSpeed              : REAL;     (* Free-stream wind speed [m/s] *)
    bYawMotorThermalFault   : BOOL;     (* Aggregate thermal trip switch from all yaw motors *)
    rGridVoltage            : REAL;     (* Main grid voltage for active power alignment checks [V] *)
    iCableTwistCount        : INT;      (* Number of physical cable twists [-3..3], max limit = +/- 3 *)
END_VAR
VAR_OUTPUT
    bSystemReady            : BOOL;     (* Yaw system ready for autonomous tracking *)
    bYawCW_Cmd              : BOOL;     (* Digital command to yaw Clockwise *)
    bYawCCW_Cmd             : BOOL;     (* Digital command to yaw Counter-Clockwise *)
    rYawSpeedRef            : REAL;     (* Speed reference for VFD driven yaw motors [rpm] *)
    bUntwistActive          : BOOL;     (* Indicates automated cable untwist sequence is executing *)
    bCriticalAlarm          : BOOL;     (* Critical fault requiring immediate shutdown and manual reset *)
    iErrorCode              : INT;      (* Detailed diagnostic error code *)
END_VAR
VAR
    iState                  : INT := 0; (* Internal state machine variable *)
    rFilteredWindDir        : REAL;     (* Low-pass filtered wind direction *)
    rPositionError          : REAL;     (* Calculated error between target wind dir and actual nacelle pos *)
    tUntwistTimer           : TON;      (* Timer for untwist duration monitoring to detect mechanical jams *)
    tDeadbandTimer          : TON;      (* Timer to prevent rapid oscillation in yaw tracking *)
    bTwistLimitExceeded     : BOOL;     (* Internal flag for cable twist limits *)
    
    (* Filter Constants *)
    rAlpha                  : REAL := 0.05; 
    
    (* Thresholds *)
    rYawDeadband            : REAL := 5.0;  (* Deg error required to initiate yaw *)
    rMaxTwistLimit          : INT := 3;     (* Maximum twists before forced untwist *)
    rCriticalTwistLimit     : INT := 4;     (* Twist limit requiring e-stop *)
END_VAR

(* === MAIN SAFETY AND PRE-CONDITION LOGIC === *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bYawCW_Cmd := FALSE;
    bYawCCW_Cmd := FALSE;
    rYawSpeedRef := 0.0;
    bCriticalAlarm := TRUE;
    iErrorCode := 999; (* E-STOP TRIGGERED *)
    RETURN;
END_IF;

IF bYawMotorThermalFault THEN
    bSystemReady := FALSE;
    bYawCW_Cmd := FALSE;
    bYawCCW_Cmd := FALSE;
    rYawSpeedRef := 0.0;
    bCriticalAlarm := TRUE;
    iErrorCode := 101; (* MOTOR OVERHEAT *)
    RETURN;
END_IF;

IF ABS(iCableTwistCount) >= rCriticalTwistLimit THEN
    bSystemReady := FALSE;
    bYawCW_Cmd := FALSE;
    bYawCCW_Cmd := FALSE;
    rYawSpeedRef := 0.0;
    bCriticalAlarm := TRUE;
    iErrorCode := 202; (* CRITICAL CABLE TWIST *)
    RETURN;
END_IF;

(* Low-pass filter on Wind Direction to reject sensor noise and turbulence *)
rFilteredWindDir := (rAlpha * rWindDirection) + ((1.0 - rAlpha) * rFilteredWindDir);

(* Calculate shortest path error accounting for 360 deg wrap-around *)
rPositionError := rFilteredWindDir - rNacellePosition;
WHILE rPositionError > 180.0 DO
    rPositionError := rPositionError - 360.0;
END_WHILE;
WHILE rPositionError < -180.0 DO
    rPositionError := rPositionError + 360.0;
END_WHILE;

(* === MAIN STATE MACHINE === *)
CASE iState OF
    0: (* IDLE & INIT *)
        bSystemReady := FALSE;
        bUntwistActive := FALSE;
        bYawCW_Cmd := FALSE;
        bYawCCW_Cmd := FALSE;
        rYawSpeedRef := 0.0;
        bCriticalAlarm := FALSE;
        iErrorCode := 0;
        
        IF bEnable AND rWindSpeed > 3.0 THEN
            iState := 10;
        END_IF;

    10: (* MONITORING AND DEAD-BAND CHECK *)
        bSystemReady := TRUE;
        bUntwistActive := FALSE;
        bYawCW_Cmd := FALSE;
        bYawCCW_Cmd := FALSE;
        rYawSpeedRef := 0.0;
        
        (* Check if untwist is required *)
        IF ABS(iCableTwistCount) >= rMaxTwistLimit THEN
            iState := 50; (* Transition to untwist *)
        ELSIF ABS(rPositionError) > rYawDeadband THEN
            tDeadbandTimer(IN := TRUE, PT := T#10S);
            IF tDeadbandTimer.Q THEN
                tDeadbandTimer(IN := FALSE);
                iState := 20; (* Transition to tracking *)
            END_IF;
        ELSE
            tDeadbandTimer(IN := FALSE);
        END_IF;
        
        IF NOT bEnable THEN
            iState := 0;
        END_IF;

    20: (* YAW TRACKING (CW or CCW) *)
        IF rPositionError > 0.0 THEN
            bYawCW_Cmd := TRUE;
            bYawCCW_Cmd := FALSE;
        ELSE
            bYawCW_Cmd := FALSE;
            bYawCCW_Cmd := TRUE;
        END_IF;
        
        (* Proportional speed control up to max speed *)
        rYawSpeedRef := ABS(rPositionError) * 1.2;
        IF rYawSpeedRef > 15.0 THEN
            rYawSpeedRef := 15.0; (* Max motor RPM limit *)
        END_IF;
        
        IF ABS(rPositionError) < (rYawDeadband * 0.5) THEN
            (* Error reduced below half deadband, stop yawing *)
            iState := 10;
        END_IF;
        
        IF ABS(iCableTwistCount) >= rMaxTwistLimit THEN
            iState := 50; (* Priority transition to untwist *)
        END_IF;
        
        IF NOT bEnable THEN
            iState := 0;
        END_IF;

    50: (* CABLE UNTWIST SEQUENCE INIT *)
        bSystemReady := FALSE;
        bUntwistActive := TRUE;
        tUntwistTimer(IN := FALSE);
        
        IF iCableTwistCount > 0 THEN
            iState := 51; (* Untwist CCW *)
        ELSE
            iState := 52; (* Untwist CW *)
        END_IF;

    51: (* UNTWIST CCW (Negative correction) *)
        bYawCW_Cmd := FALSE;
        bYawCCW_Cmd := TRUE;
        rYawSpeedRef := 10.0; (* Fixed untwist speed *)
        
        tUntwistTimer(IN := TRUE, PT := T#300S); (* Max time to untwist *)
        IF tUntwistTimer.Q THEN
            bCriticalAlarm := TRUE;
            iErrorCode := 303; (* UNTWIST TIMEOUT *)
            iState := 99; (* FAULT STATE *)
        END_IF;
        
        IF iCableTwistCount <= 0 THEN
            tUntwistTimer(IN := FALSE);
            iState := 10; (* Return to monitoring *)
        END_IF;

    52: (* UNTWIST CW (Positive correction) *)
        bYawCW_Cmd := TRUE;
        bYawCCW_Cmd := FALSE;
        rYawSpeedRef := 10.0; (* Fixed untwist speed *)
        
        tUntwistTimer(IN := TRUE, PT := T#300S); (* Max time to untwist *)
        IF tUntwistTimer.Q THEN
            bCriticalAlarm := TRUE;
            iErrorCode := 304; (* UNTWIST TIMEOUT *)
            iState := 99; (* FAULT STATE *)
        END_IF;
        
        IF iCableTwistCount >= 0 THEN
            tUntwistTimer(IN := FALSE);
            iState := 10; (* Return to monitoring *)
        END_IF;
        
    99: (* FAULT LATCH STATE *)
        bSystemReady := FALSE;
        bYawCW_Cmd := FALSE;
        bYawCCW_Cmd := FALSE;
        rYawSpeedRef := 0.0;
        bUntwistActive := FALSE;
        (* Requires manual reset which would transition iState back to 0 externally or via another reset input *)

END_CASE;

END_FUNCTION_BLOCK
```"""

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": code}
    ]
}

with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
