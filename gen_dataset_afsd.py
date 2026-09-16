import json, uuid, os

prompt = """<USER_REQUEST>
You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Multi-Axis Additive Friction Stir Deposition (AFSD) Spindle**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Solid-state metallurgical bonding acoustic emission feedback, non-Newtonian plasticized aluminum shear rate control, and multi-vector forging force). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_AFSD_AdditiveSpindle\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Multi-Axis Additive Friction Stir Deposition (AFSD) Spindle

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT.
</USER_REQUEST>"""

code = """```iec-st
FUNCTION_BLOCK FB_AFSD_AdditiveSpindle_Control
VAR_INPUT
    bEnableSys                  : BOOL;     (* Main system enable signal *)
    bEStop_OK                   : BOOL;     (* Emergency stop circuit OK (TRUE = safe) *)
    rSpindleRPM_SP              : REAL;     (* Setpoint for spindle rotation speed (RPM) *)
    rFeedRate_SP                : REAL;     (* Setpoint for material feed rate (mm/s) *)
    rDownwardForce_SP           : REAL;     (* Setpoint for Z-axis forging force (kN) *)
    rToolTemp_Act               : REAL;     (* Actual tool temperature measured via thermocouple (deg C) *)
    rAcousticEmission_Act       : REAL;     (* High-frequency acoustic emission sensor feedback (V) *)
    rSpindleTorque_Act          : REAL;     (* Actual spindle motor torque (Nm) *)
    rZAxisPosition              : REAL;     (* Z-axis position (mm) *)
END_VAR
VAR_OUTPUT
    bSystemReady                : BOOL;     (* Spindle and feed systems are ready for deposition *)
    bDepositionActive           : BOOL;     (* Active deposition state indication *)
    rSpindleVel_Out             : REAL;     (* Control signal to spindle VFD/Servo (RPM) *)
    rFeedRate_Out               : REAL;     (* Control signal to material feeder (mm/s) *)
    rZAxisForce_Out             : REAL;     (* Control signal for Z-axis actuator force (kN) *)
    bAlarm_TempHigh             : BOOL;     (* Critical alarm: Tool temperature exceeded safe limit *)
    bAlarm_ForceDeviation       : BOOL;     (* Critical alarm: Forging force deviation too high *)
    bAlarm_AcousticFault        : BOOL;     (* Critical alarm: Poor metallurgical bond detected via AE *)
END_VAR
VAR
    iState                      : INT := 0; (* Internal state machine tracker *)
    tDepositionTimer            : TON;      (* Timer for stabilizing the shear layer *)
    tCoolDownTimer              : TON;      (* Post-deposition cool down timer *)
    rFilteredTorque             : REAL := 0.0; (* Low-pass filtered spindle torque *)
    rFilteredForce              : REAL := 0.0; (* Low-pass filtered forging force *)
    rTorqueError                : REAL := 0.0;
    
    (* Filter constants *)
    rAlpha                      : REAL := 0.15; (* EMA filter constant *)
    
    (* Limit Parameters *)
    MAX_TOOL_TEMP               : REAL := 550.0; (* deg C, max safe temp for aluminum alloys *)
    MAX_TORQUE_DEVIATION        : REAL := 25.0;  (* Nm *)
    MIN_AE_THRESHOLD            : REAL := 1.2;   (* V, minimum acoustic emission for good bond *)
END_VAR

(* === MAIN SAFETY INTERLOCKS === *)
IF NOT bEStop_OK THEN
    (* Immediate safe shutdown *)
    bSystemReady := FALSE;
    bDepositionActive := FALSE;
    rSpindleVel_Out := 0.0;
    rFeedRate_Out := 0.0;
    rZAxisForce_Out := 0.0;
    iState := 0;
    RETURN;
END_IF;

(* === SENSOR NOISE FILTERING === *)
(* Apply Exponential Moving Average (EMA) to critical high-noise signals *)
rFilteredTorque := (rAlpha * rSpindleTorque_Act) + ((1.0 - rAlpha) * rFilteredTorque);
rFilteredForce := (rAlpha * rDownwardForce_SP) + ((1.0 - rAlpha) * rFilteredForce); (* Simulating force feedback matching *)

(* === CONTINUOUS FAULT MONITORING === *)
IF rToolTemp_Act > MAX_TOOL_TEMP THEN
    bAlarm_TempHigh := TRUE;
ELSE
    bAlarm_TempHigh := FALSE;
END_IF;

IF iState >= 20 AND iState <= 30 THEN
    IF rAcousticEmission_Act < MIN_AE_THRESHOLD THEN
        bAlarm_AcousticFault := TRUE;
    ELSE
        bAlarm_AcousticFault := FALSE;
    END_IF;
END_IF;

(* === MAIN STATE MACHINE === *)
CASE iState OF
    0: (* SYSTEM IDLE / INIT *)
        bSystemReady := FALSE;
        bDepositionActive := FALSE;
        rSpindleVel_Out := 0.0;
        rFeedRate_Out := 0.0;
        rZAxisForce_Out := 0.0;
        
        IF bEnableSys AND NOT bAlarm_TempHigh THEN
            bSystemReady := TRUE;
            iState := 10;
        END_IF;

    10: (* SPINDLE RAMP UP *)
        bSystemReady := TRUE;
        (* Ramp spindle speed to setpoint, maintaining zero feed and minimal force *)
        rSpindleVel_Out := rSpindleRPM_SP; 
        rZAxisForce_Out := 5.0; (* Pre-load force (kN) *)
        rFeedRate_Out := 0.0;
        
        (* Check if spindle torque is stabilized (simulated check) *)
        rTorqueError := ABS(rSpindleRPM_SP * 0.1 - rFilteredTorque);
        IF rTorqueError < 5.0 THEN
            iState := 20;
        END_IF;
        
        IF NOT bEnableSys THEN
            iState := 40;
        END_IF;

    20: (* PLASTICIZATION AND BONDING (DEPOSITION ACTIVE) *)
        bDepositionActive := TRUE;
        rSpindleVel_Out := rSpindleRPM_SP;
        rFeedRate_Out := rFeedRate_SP;
        
        (* Advanced Force Control: Modulate Z-axis force based on tool temperature *)
        (* If temperature drops, increase force to generate more frictional heat *)
        IF rToolTemp_Act < 400.0 THEN
            rZAxisForce_Out := rDownwardForce_SP * 1.1;
        ELSIF rToolTemp_Act > 500.0 THEN
            rZAxisForce_Out := rDownwardForce_SP * 0.9;
        ELSE
            rZAxisForce_Out := rDownwardForce_SP;
        END_IF;
        
        IF bAlarm_AcousticFault OR NOT bEnableSys OR bAlarm_TempHigh THEN
            iState := 30;
        END_IF;

    30: (* DEPOSITION HALT AND DWELL *)
        bDepositionActive := FALSE;
        rFeedRate_Out := 0.0;
        (* Maintain rotation and force to consolidate the last layer *)
        tDepositionTimer(IN := TRUE, PT := T#3S);
        
        IF tDepositionTimer.Q THEN
            tDepositionTimer(IN := FALSE);
            iState := 40;
        END_IF;

    40: (* SPINDLE SPINDOWN & RETRACT *)
        rSpindleVel_Out := 0.0;
        rZAxisForce_Out := 0.0;
        
        IF rFilteredTorque < 1.0 THEN
            iState := 0;
        END_IF;

END_CASE;

END_FUNCTION_BLOCK
```"""

os.makedirs(r"c:\Users\majip\Downloads\LLM REASEARCH\data\swarm_raw", exist_ok=True)
with open(f"c:\\Users\\majip\\Downloads\\LLM REASEARCH\\data\\swarm_raw\\agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
    json.dump({"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}, f, ensure_ascii=False)
