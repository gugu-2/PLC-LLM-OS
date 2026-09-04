import os, json, uuid

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Heavy-Duty Mining Dragline Excavator Walking Mechanism**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., quad-shoe synchronized lifting, multi-axis hydraulic cylinder phase interlocking, and center-of-gravity dynamic balancing on uneven terrain). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_DraglineWalking\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Heavy-Duty Mining Dragline Excavator Walking Mechanism

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_DraglineWalkCoordinator
VAR_INPUT
    bWalkEnable           : BOOL;  (* Master walk mode enable command *)
    bEmergencyStop        : BOOL;  (* Global E-Stop, failsafe low *)
    rInclinometerPitch    : REAL;  (* Base pitch inclination (degrees), limits: -5.0 to +5.0 *)
    rInclinometerRoll     : REAL;  (* Base roll inclination (degrees), limits: -5.0 to +5.0 *)
    rLiftCyl1_Position    : REAL;  (* Shoe 1 lift cylinder extension (mm) *)
    rLiftCyl2_Position    : REAL;  (* Shoe 2 lift cylinder extension (mm) *)
    rLiftCyl3_Position    : REAL;  (* Shoe 3 lift cylinder extension (mm) *)
    rLiftCyl4_Position    : REAL;  (* Shoe 4 lift cylinder extension (mm) *)
    rDragCyl_Position     : REAL;  (* Main drag cylinder position (mm) *)
    bTerrainOk            : BOOL;  (* Ground radar terrain check valid *)
END_VAR
VAR_OUTPUT
    bSystemReady          : BOOL;  (* Walking system ready to engage *)
    bWalkInProgress       : BOOL;  (* Walk cycle currently active *)
    bAlarm                : BOOL;  (* Fault detected (tilt, sync, limit) *)
    rLiftCyl1_Cmd         : REAL;  (* Command signal to Lift Valve 1 (0-100%) *)
    rLiftCyl2_Cmd         : REAL;  (* Command signal to Lift Valve 2 (0-100%) *)
    rLiftCyl3_Cmd         : REAL;  (* Command signal to Lift Valve 3 (0-100%) *)
    rLiftCyl4_Cmd         : REAL;  (* Command signal to Lift Valve 4 (0-100%) *)
    rDragCyl_Cmd          : REAL;  (* Command signal to Drag Valve (0-100%) *)
    iFaultCode            : INT;   (* Specific fault identifier *)
END_VAR
VAR
    iState                : INT := 0; 
    tSyncWatchdog         : TON;
    tSettleDelay          : TON;
    rMaxPosDev            : REAL := 15.0; (* Max allowable sync deviation in mm *)
    rTargetLift           : REAL := 1200.0; (* Target lift stroke in mm *)
    rAvgLiftPos           : REAL;
    bDeviationFault       : BOOL;
    bTiltFault            : BOOL;
END_VAR

(* === MAIN LOGIC === *)
(* 1. Safety and E-Stop Interlock *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bWalkInProgress := FALSE;
    bAlarm := TRUE;
    iFaultCode := 101; (* E-Stop active *)
    rLiftCyl1_Cmd := 0.0;
    rLiftCyl2_Cmd := 0.0;
    rLiftCyl3_Cmd := 0.0;
    rLiftCyl4_Cmd := 0.0;
    rDragCyl_Cmd := 0.0;
    iState := 999; (* FAULT STATE *)
    RETURN;
END_IF;

(* 2. Inclinometer Monitoring *)
IF (ABS(rInclinometerPitch) > 4.5) OR (ABS(rInclinometerRoll) > 4.5) THEN
    bTiltFault := TRUE;
ELSE
    bTiltFault := FALSE;
END_IF;

IF bTiltFault AND iState < 900 THEN
    bAlarm := TRUE;
    iFaultCode := 102; (* Base tilt exceeded safe limits *)
    iState := 900; (* RAMP DOWN TO SAFE STOP *)
END_IF;

(* 3. Cylinder Sync Calculation *)
rAvgLiftPos := (rLiftCyl1_Position + rLiftCyl2_Position + rLiftCyl3_Position + rLiftCyl4_Position) / 4.0;
bDeviationFault := (ABS(rLiftCyl1_Position - rAvgLiftPos) > rMaxPosDev) OR
                   (ABS(rLiftCyl2_Position - rAvgLiftPos) > rMaxPosDev) OR
                   (ABS(rLiftCyl3_Position - rAvgLiftPos) > rMaxPosDev) OR
                   (ABS(rLiftCyl4_Position - rAvgLiftPos) > rMaxPosDev);

IF bDeviationFault AND iState >= 20 AND iState < 900 THEN
    bAlarm := TRUE;
    iFaultCode := 201; (* Shoe sync error *)
    iState := 900; 
END_IF;

(* 4. State Machine for Walking Mechanism *)
CASE iState OF
    0: (* IDLE & CHECK PARAMETERS *)
        bSystemReady := TRUE;
        bWalkInProgress := FALSE;
        bAlarm := FALSE;
        iFaultCode := 0;
        IF bWalkEnable AND bTerrainOk AND NOT bTiltFault AND NOT bDeviationFault THEN
            bSystemReady := FALSE;
            bWalkInProgress := TRUE;
            iState := 10;
        END_IF;

    10: (* PRE-LIFT PRESSURIZATION *)
        (* Issue initial low-level pressure commands to overcome static friction *)
        rLiftCyl1_Cmd := 10.0;
        rLiftCyl2_Cmd := 10.0;
        rLiftCyl3_Cmd := 10.0;
        rLiftCyl4_Cmd := 10.0;
        
        tSettleDelay(IN := TRUE, PT := T#2S);
        IF tSettleDelay.Q THEN
            tSettleDelay(IN := FALSE);
            iState := 20;
        END_IF;

    20: (* SYNCHRONIZED LIFTING *)
        (* Implement proportional control to hit target lift while keeping sync *)
        rLiftCyl1_Cmd := (rTargetLift - rLiftCyl1_Position) * 0.5 + 20.0;
        rLiftCyl2_Cmd := (rTargetLift - rLiftCyl2_Position) * 0.5 + 20.0;
        rLiftCyl3_Cmd := (rTargetLift - rLiftCyl3_Position) * 0.5 + 20.0;
        rLiftCyl4_Cmd := (rTargetLift - rLiftCyl4_Position) * 0.5 + 20.0;
        
        IF (rAvgLiftPos > (rTargetLift - 10.0)) THEN
            iState := 30;
        END_IF;
        
        (* Watchdog timer for lifting *)
        tSyncWatchdog(IN := TRUE, PT := T#30S);
        IF tSyncWatchdog.Q THEN
            tSyncWatchdog(IN := FALSE);
            bAlarm := TRUE;
            iFaultCode := 301; (* Lift timeout *)
            iState := 900;
        END_IF;

    30: (* DRAG FORWARD *)
        tSyncWatchdog(IN := FALSE);
        (* Hold lift position *)
        rLiftCyl1_Cmd := 15.0;
        rLiftCyl2_Cmd := 15.0;
        rLiftCyl3_Cmd := 15.0;
        rLiftCyl4_Cmd := 15.0;
        
        (* Extend drag cylinder to move machine *)
        rDragCyl_Cmd := 50.0;
        
        IF rDragCyl_Position > 3500.0 THEN (* Assume 3.5m step *)
            iState := 40;
        END_IF;
        
    40: (* SYNCHRONIZED LOWERING *)
        rDragCyl_Cmd := 0.0;
        rLiftCyl1_Cmd := -20.0;
        rLiftCyl2_Cmd := -20.0;
        rLiftCyl3_Cmd := -20.0;
        rLiftCyl4_Cmd := -20.0;
        
        IF rAvgLiftPos < 50.0 THEN
            iState := 50;
        END_IF;

    50: (* DRAG RETRACT *)
        rLiftCyl1_Cmd := 0.0;
        rLiftCyl2_Cmd := 0.0;
        rLiftCyl3_Cmd := 0.0;
        rLiftCyl4_Cmd := 0.0;
        
        rDragCyl_Cmd := -50.0; (* Retract drag *)
        
        IF rDragCyl_Position < 50.0 THEN
            bWalkInProgress := FALSE;
            IF NOT bWalkEnable THEN
                iState := 0;
            ELSE
                (* Auto repeat if enable held *)
                iState := 10;
            END_IF;
        END_IF;

    900: (* CONTROLLED FAULT RAMP DOWN *)
        rLiftCyl1_Cmd := 0.0;
        rLiftCyl2_Cmd := 0.0;
        rLiftCyl3_Cmd := 0.0;
        rLiftCyl4_Cmd := 0.0;
        rDragCyl_Cmd := 0.0;
        tSyncWatchdog(IN := FALSE);
        tSettleDelay(IN := FALSE);
        iState := 999;

    999: (* FAULT LOCKOUT *)
        (* Must toggle E-Stop or wait for reset from HMI, here simplified *)
        IF NOT bWalkEnable AND NOT bAlarm THEN
            iState := 0;
        END_IF;
        
END_CASE;

END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print(f"Saved to {filename}")
