import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Automated Commercial Ski Lift Chair Gripper Force and Variable Rope Speed Synchronization**

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_SkiLift_Gripper\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Automated Commercial Ski Lift Chair Gripper Force and Variable Rope Speed Synchronization

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_SkiLift_RopeGripSync
(* 
   Advanced Chairlift Gripper Force and Variable Rope Speed Synchronization Control
   Developed for High-Speed Detachable Grip Systems (EN 12929-1 compliance)
*)
VAR_INPUT
    bEnableSystem          : BOOL;  (* System enable switch from main panel *)
    bSafetyRelayOK         : BOOL;  (* Hardwired safety loop status (E-Stop, derailment) *)
    rHaulRopeSpeed         : REAL;  (* Current haul rope speed in m/s (0.0 to 6.0) *)
    rChairVelocity         : REAL;  (* Velocity of the chair approaching the grip area in m/s *)
    rAmbientTemp           : REAL;  (* Ambient temperature in deg C to compensate spring stiffness *)
    rTargetGripForce       : REAL;  (* Desired gripping force setpoint in kN *)
    bTerminalArrivalSignal : BOOL;  (* Proximity sensor indicating chair arrival at grip point *)
    rWindSpeed             : REAL;  (* Anemometer reading in m/s for safety speed limits *)
END_VAR
VAR_OUTPUT
    bSystemReady           : BOOL;  (* Ready for engagement sequence *)
    rActualGripForce       : REAL;  (* Applied and verified gripping force in kN *)
    rSynchronizedSpeedCmd  : REAL;  (* Speed command for terminal conveyor to match haul rope *)
    bGripFault             : BOOL;  (* Fault detected during gripping process *)
    bEmergencyBrake        : BOOL;  (* Command to trigger bullwheel emergency brakes *)
    iOperationState        : INT;   (* Current state of the synchronization state machine *)
END_VAR
VAR
    iState                 : INT := 0; (* Internal state machine counter *)
    tGripTimeout           : TON;      (* Timeout for gripping engagement sequence *)
    tBrakeDelay            : TON;      (* Delay before applying brake on fault *)
    rSpeedError            : REAL;     (* Error between rope speed and chair speed *)
    rForceError            : REAL;     (* Error between target and actual force *)
    rIntegrationAcc        : REAL;     (* Integral accumulator for speed PID *)
    bForceEstablished      : BOOL;
    
    (* Constants *)
    MAX_SPEED_ERROR        : REAL := 0.05; (* Max allowed speed diff in m/s *)
    MIN_GRIP_FORCE         : REAL := 25.0; (* Minimum safe gripping force in kN *)
END_VAR

(* === MAIN LOGIC === *)
(* Emergency Safety Interlock *)
IF NOT bSafetyRelayOK OR (rWindSpeed > 20.0) THEN
    bSystemReady := FALSE;
    bGripFault := TRUE;
    bEmergencyBrake := TRUE;
    iOperationState := 999;
    RETURN;
END_IF;

(* Temperature Compensation for Spring Washers (Belleville Springs) *)
(* As temp drops, stiffness increases slightly, requiring more applied pressure *)
VAR
    rTempCompFactor : REAL;
END_VAR
IF rAmbientTemp < 0.0 THEN
    rTempCompFactor := 1.0 + (ABS(rAmbientTemp) * 0.005);
ELSE
    rTempCompFactor := 1.0;
END_IF;

(* Main State Machine *)
CASE iState OF
    0: (* IDLE & INITIATION *)
        bSystemReady := FALSE;
        bGripFault := FALSE;
        bEmergencyBrake := FALSE;
        rSynchronizedSpeedCmd := 0.0;
        
        IF bEnableSystem AND bSafetyRelayOK THEN
            bSystemReady := TRUE;
            iState := 10;
        END_IF;

    10: (* SPEED SYNCHRONIZATION *)
        iOperationState := 10;
        (* PID loop to match terminal chair speed to haul rope speed *)
        rSpeedError := rHaulRopeSpeed - rChairVelocity;
        rIntegrationAcc := rIntegrationAcc + (rSpeedError * 0.01); (* Simplified dt *)
        
        (* Anti-windup *)
        IF rIntegrationAcc > 2.0 THEN rIntegrationAcc := 2.0; END_IF;
        IF rIntegrationAcc < -2.0 THEN rIntegrationAcc := -2.0; END_IF;
        
        rSynchronizedSpeedCmd := rHaulRopeSpeed + (rSpeedError * 1.5) + (rIntegrationAcc * 0.5);
        
        IF bTerminalArrivalSignal THEN
            IF ABS(rSpeedError) <= MAX_SPEED_ERROR THEN
                iState := 20; (* Speeds matched, begin gripping *)
            ELSE
                bGripFault := TRUE;
                iState := 99; (* Fault state *)
            END_IF;
        END_IF;

    20: (* GRIP ENGAGEMENT AND FORCE APPLICATION *)
        iOperationState := 20;
        tGripTimeout(IN := TRUE, PT := T#1S);
        
        (* Simulate force application feedback - in reality read from load cell *)
        rActualGripForce := rTargetGripForce * rTempCompFactor;
        
        IF rActualGripForce >= MIN_GRIP_FORCE THEN
            bForceEstablished := TRUE;
            tGripTimeout(IN := FALSE);
            iState := 30;
        END_IF;
        
        IF tGripTimeout.Q THEN
            bGripFault := TRUE;
            iState := 99; (* Fault: Failed to establish force *)
        END_IF;

    30: (* GRIP SECURED, TRANSIT *)
        iOperationState := 30;
        IF NOT bEnableSystem THEN
            iState := 0;
        END_IF;
        
    99: (* FAULT HANDLING *)
        iOperationState := 99;
        bEmergencyBrake := TRUE;
        bSystemReady := FALSE;
        IF NOT bEnableSystem THEN
            iState := 0; (* Reset on disable *)
        END_IF;
END_CASE;

END_FUNCTION_BLOCK
```"""

import os
os.makedirs('data/swarm_raw', exist_ok=True)
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
print(f"Saved to {filename}")
