import os
import json
import uuid

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Automated Commercial Ski Lift Chair Gripper Force and Variable Rope Speed Synchronization**

Task: Invent a highly complex, ultra-realistic control scenario for this domain. Make this code EVEN BETTER, MORE ADVANCED, and MORE RIGOROUS than previous iterations. Include extreme edge-case handling, advanced math, and robust fault-tolerance.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_SkiLift_GripperSync\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
FUNCTION_BLOCK FB_SkiLift_GripperSync
VAR_INPUT
    bEnable                 : BOOL;       (* Master enable signal for gripper and speed sync *)
    bEmergencyStop          : BOOL;       (* Safety circuit OK (Active HIGH) *)
    rRopeSpeed_mps          : REAL;       (* Current bullwheel/rope speed in meters per second *)
    rTargetRopeSpeed_mps    : REAL;       (* Desired rope speed from main controller *)
    rGripperForceAct_kN     : REAL;       (* Actual measured clamping force of the chair gripper in kN *)
    rWindSpeed_mps          : REAL;       (* Measured cross-wind speed in meters per second *)
    bChairInTerminal        : BOOL;       (* Proximity sensor indicating a chair is approaching terminal *)
    bIceDetected            : BOOL;       (* Optical/capacitive sensor detecting ice on the rope *)
END_VAR
VAR_OUTPUT
    bSystemReady            : BOOL;       (* Sync system is ready and nominal *)
    rCmdRopeSpeed_mps       : REAL;       (* Commanded speed to drive VFD *)
    rCmdGripperForce_kN     : REAL;       (* Target clamping force commanded to hydraulic/spring tensioner *)
    bForceAlarm             : BOOL;       (* True if gripper force cannot be maintained *)
    bSyncFault              : BOOL;       (* True if speed or force tracking errors exceed limits *)
END_VAR
VAR
    iState                  : INT := 0;   (* Internal state machine step *)
    rFilteredForce          : REAL := 0.0;
    rFilteredWind           : REAL := 0.0;
    rForceError             : REAL := 0.0;
    rForceIntegral          : REAL := 0.0;
    tFaultTimer             : TON;
    tIceCompTimer           : TON;
    rNominalForce           : REAL := 12.5; (* Nominal force in kN *)
    rMaxForceLimit          : REAL := 18.0; (* Max allowable force *)
    rMinForceLimit          : REAL := 10.0; (* Min allowable force *)
    rKp                     : REAL := 0.85; (* Proportional gain for force control *)
    rKi                     : REAL := 0.25; (* Integral gain for force control *)
    rSpeedRampRate          : REAL := 0.5;  (* Max acceleration/deceleration m/s^2 *)
    bIceCompActive          : BOOL := FALSE;
END_VAR

(* === MAIN LOGIC === *)
(* Multi-layered safety interlock check *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bForceAlarm := TRUE;
    bSyncFault := TRUE;
    rCmdRopeSpeed_mps := 0.0; (* Immediate stop command *)
    rCmdGripperForce_kN := rMaxForceLimit; (* Clamp tight on emergency *)
    iState := 999; (* Fault state *)
    RETURN;
END_IF;

(* Sensor Noise Filtering (EMA - Exponential Moving Average) *)
rFilteredForce := (0.2 * rGripperForceAct_kN) + (0.8 * rFilteredForce);
rFilteredWind := (0.1 * rWindSpeed_mps) + (0.9 * rFilteredWind);

(* Edge case handling: High wind dictates lower max speed *)
IF rFilteredWind > 20.0 THEN
    rTargetRopeSpeed_mps := LIMIT(0.0, rTargetRopeSpeed_mps, 3.0);
ELSIF rFilteredWind > 15.0 THEN
    rTargetRopeSpeed_mps := LIMIT(0.0, rTargetRopeSpeed_mps, 4.0);
END_IF;

CASE iState OF
    0: (* IDLE & INITIALIZATION *)
        bSystemReady := FALSE;
        bForceAlarm := FALSE;
        bSyncFault := FALSE;
        rCmdRopeSpeed_mps := 0.0;
        rCmdGripperForce_kN := rNominalForce;
        IF bEnable AND (rFilteredForce > rMinForceLimit) THEN
            iState := 10;
        END_IF;

    10: (* RAMP UP ROPE SPEED & SYNCHRONIZE GRIPPER *)
        bSystemReady := TRUE;
        
        (* Ramp speed *)
        IF rCmdRopeSpeed_mps < rTargetRopeSpeed_mps THEN
            rCmdRopeSpeed_mps := rCmdRopeSpeed_mps + (rSpeedRampRate * 0.01); (* Assume 10ms cycle time *)
        ELSIF rCmdRopeSpeed_mps > rTargetRopeSpeed_mps THEN
            rCmdRopeSpeed_mps := rCmdRopeSpeed_mps - (rSpeedRampRate * 0.01);
        END_IF;
        
        (* Dynamic Gripper Force Calculation based on speed and conditions *)
        rForceError := (rNominalForce + (rCmdRopeSpeed_mps * 0.15)) - rFilteredForce;
        
        (* Ice compensation logic *)
        IF bIceDetected AND NOT bIceCompActive THEN
            bIceCompActive := TRUE;
        ELSIF NOT bIceDetected THEN
            bIceCompActive := FALSE;
        END_IF;
        
        IF bIceCompActive THEN
            rForceError := rForceError + 2.5; (* Increase force setpoint if ice is detected to prevent slipping *)
        END_IF;

        rForceIntegral := rForceIntegral + (rForceError * 0.01);
        rForceIntegral := LIMIT(-5.0, rForceIntegral, 5.0); (* Anti-windup *)
        
        rCmdGripperForce_kN := rNominalForce + (rKp * rForceError) + (rKi * rForceIntegral);
        rCmdGripperForce_kN := LIMIT(rMinForceLimit, rCmdGripperForce_kN, rMaxForceLimit);

        (* Fault Monitoring *)
        IF ABS(rCmdGripperForce_kN - rFilteredForce) > 3.0 THEN
            tFaultTimer(IN := TRUE, PT := T#2S);
        ELSE
            tFaultTimer(IN := FALSE, PT := T#2S);
        END_IF;
        
        IF tFaultTimer.Q THEN
            bForceAlarm := TRUE;
            iState := 20;
        END_IF;

        IF NOT bEnable THEN
            iState := 30;
        END_IF;

    20: (* CONTROLLED FAULT RAMP DOWN *)
        bSystemReady := FALSE;
        bSyncFault := TRUE;
        rCmdRopeSpeed_mps := rCmdRopeSpeed_mps - (rSpeedRampRate * 0.02); (* Fast decel *)
        rCmdRopeSpeed_mps := MAX(rCmdRopeSpeed_mps, 0.0);
        IF rCmdRopeSpeed_mps <= 0.0 THEN
            iState := 999;
        END_IF;

    30: (* NORMAL STOP *)
        bSystemReady := FALSE;
        rCmdRopeSpeed_mps := rCmdRopeSpeed_mps - (rSpeedRampRate * 0.01);
        rCmdRopeSpeed_mps := MAX(rCmdRopeSpeed_mps, 0.0);
        rCmdGripperForce_kN := rNominalForce;
        IF rCmdRopeSpeed_mps <= 0.0 THEN
            iState := 0;
        END_IF;
        
    999: (* FAULT LOCKOUT *)
        rCmdRopeSpeed_mps := 0.0;
        rCmdGripperForce_kN := rMaxForceLimit; (* Hold chairs tight *)
        IF NOT bEnable AND NOT bEmergencyStop THEN
            bSyncFault := FALSE;
            bForceAlarm := FALSE;
            iState := 0; (* Reset if enable and e-stop are cleared *)
        END_IF;

END_CASE;

END_FUNCTION_BLOCK
```"""

record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
