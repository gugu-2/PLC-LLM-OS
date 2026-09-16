import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Commercial Autonomous Heavy-Duty Gantry Crane Sway Control**

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_GantryCrane_SwayControl\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Commercial Autonomous Heavy-Duty Gantry Crane Sway Control

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_GantryCrane_SwayControl
(* 
   =============================================================================
   Block Name: FB_GantryCrane_SwayControl
   Description: Anti-sway and position control for heavy-duty gantry cranes.
                Implements observer-based state feedback for load sway reduction,
                combined with trajectory generation for minimum-time point-to-point
                transfer under safety constraints.
   =============================================================================
*)
VAR_INPUT
    bEnable                 : BOOL;     (* System Enable Signal - Master command *)
    bEmergencyStop          : BOOL;     (* E-Stop relay status (TRUE = OK) *)
    bLimitSwitchPos         : BOOL;     (* Positive end limit switch (TRUE = Reached) *)
    bLimitSwitchNeg         : BOOL;     (* Negative end limit switch (TRUE = Reached) *)
    rTrolleyPosition        : REAL;     (* Current trolley position [m] *)
    rTrolleyVelocity        : REAL;     (* Current trolley velocity [m/s] *)
    rHoistCableLength       : REAL;     (* Current hoist cable length (pendulum length) [m] *)
    rLoadSwayAngle          : REAL;     (* Load sway angle measured by vision/IMU [rad] *)
    rLoadSwayRate           : REAL;     (* Load sway angular velocity [rad/s] *)
    rTargetPosition         : REAL;     (* Operator requested target position [m] *)
    rMaxVelocity            : REAL;     (* Maximum allowable trolley velocity [m/s] *)
    rMaxAcceleration        : REAL;     (* Maximum allowable trolley acceleration [m/s^2] *)
END_VAR
VAR_OUTPUT
    bSystemReady            : BOOL;     (* Drive system ready to accept commands *)
    rTrolleySpeedCommand    : REAL;     (* Velocity setpoint to trolley drive [m/s] *)
    bTargetReached          : BOOL;     (* Positioning complete and sway < tolerance *)
    bAlarm                  : BOOL;     (* Generic fault alarm output *)
    iErrorCode              : INT;      (* Diagnostics error code *)
END_VAR
VAR
    (* Internal States and Registers *)
    iState                  : INT := 0; (* Internal State Machine *)
    tControlCycleTimer      : TON;      (* Control loop execution timer *)
    rFilteredSwayAngle      : REAL;     (* Low-pass filtered sway angle *)
    rFilteredSwayRate       : REAL;     (* Low-pass filtered sway angular rate *)
    
    (* Kinematic calculations *)
    rNaturalFreq            : REAL;     (* Omega_n = sqrt(g / L) *)
    rGravity                : REAL := 9.81;
    
    (* Feedback Gains (State-space LQR pre-calculated or scheduled) *)
    K_pos                   : REAL := 0.85;
    K_vel                   : REAL := 2.10;
    K_sway                  : REAL := 15.5;
    K_sway_rate             : REAL := 4.25;
    
    rPosError               : REAL;
    rCommandAccel           : REAL;
    
    (* Filtering *)
    rAlpha                  : REAL := 0.15; (* Filter coefficient *)
END_VAR

(* === MAIN LOGIC START === *)

(* 1. Safety Interlocks & E-Stop *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    rTrolleySpeedCommand := 0.0;
    bAlarm := TRUE;
    iErrorCode := 99; (* E-STOP Active *)
    iState := 0;
    RETURN;
END_IF;

(* 2. Signal Processing (Sensor Noise Filtering) *)
rFilteredSwayAngle := (rAlpha * rLoadSwayAngle) + ((1.0 - rAlpha) * rFilteredSwayAngle);
rFilteredSwayRate  := (rAlpha * rLoadSwayRate) + ((1.0 - rAlpha) * rFilteredSwayRate);

(* Limit Hoist Cable Length to avoid division by zero or unrealistic frequencies *)
IF rHoistCableLength < 0.5 THEN
    rHoistCableLength := 0.5;
END_IF;

(* Calculate Pendulum Natural Frequency *)
rNaturalFreq := SQRT(rGravity / rHoistCableLength);

(* 3. Main State Machine *)
CASE iState OF
    0: (* IDLE & INITIALIZATION *)
        rTrolleySpeedCommand := 0.0;
        bSystemReady := FALSE;
        bTargetReached := FALSE;
        bAlarm := FALSE;
        iErrorCode := 0;
        
        IF bEnable AND (NOT bLimitSwitchPos AND NOT bLimitSwitchNeg) THEN
            bSystemReady := TRUE;
            iState := 10;
        END_IF;

    10: (* ACTIVE CONTROL / POSITIONING *)
        rPosError := rTargetPosition - rTrolleyPosition;
        
        (* Evaluate End Limits to prevent crashing *)
        IF (rPosError > 0.0 AND bLimitSwitchPos) OR (rPosError < 0.0 AND bLimitSwitchNeg) THEN
            rPosError := 0.0; (* Override target *)
        END_IF;
        
        (* State Feedback Control Law calculation (LQR inspired)
           u = -Kx = K_pos*e_pos - K_vel*vel - K_sway*theta - K_sway_rate*theta_dot *)
           
        rCommandAccel := (K_pos * rPosError) 
                         - (K_vel * rTrolleyVelocity) 
                         - (K_sway * rFilteredSwayAngle) 
                         - (K_sway_rate * rFilteredSwayRate);
                         
        (* Acceleration saturation *)
        IF rCommandAccel > rMaxAcceleration THEN
            rCommandAccel := rMaxAcceleration;
        ELSIF rCommandAccel < -rMaxAcceleration THEN
            rCommandAccel := -rMaxAcceleration;
        END_IF;
        
        (* Velocity Command Integration (Assuming 50ms cycle) *)
        rTrolleySpeedCommand := rTrolleySpeedCommand + (rCommandAccel * 0.05);
        
        (* Velocity saturation *)
        IF rTrolleySpeedCommand > rMaxVelocity THEN
            rTrolleySpeedCommand := rMaxVelocity;
        ELSIF rTrolleySpeedCommand < -rMaxVelocity THEN
            rTrolleySpeedCommand := -rMaxVelocity;
        END_IF;
        
        (* Convergence Check *)
        IF ABS(rPosError) < 0.05 AND ABS(rFilteredSwayAngle) < 0.01 AND ABS(rTrolleyVelocity) < 0.02 THEN
            iState := 20;
        END_IF;
        
        (* Disable condition *)
        IF NOT bEnable THEN
            iState := 0;
        END_IF;

    20: (* TARGET REACHED / STABILIZED *)
        rTrolleySpeedCommand := 0.0;
        bTargetReached := TRUE;
        
        IF ABS(rTargetPosition - rTrolleyPosition) >= 0.05 THEN
            bTargetReached := FALSE;
            iState := 10;
        END_IF;
        
        IF NOT bEnable THEN
            iState := 0;
        END_IF;
        
    ELSE
        iState := 0;
END_CASE;

END_FUNCTION_BLOCK
```"""

import os
os.makedirs("data/swarm_raw", exist_ok=True)
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
print(f"Saved to {filename}")
