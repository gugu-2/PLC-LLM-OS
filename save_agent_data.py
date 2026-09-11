import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Deep-Sea Oil Platform Active Heave Compensation (AHC) Drawworks**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Mooring line dynamic tension filtering, hydraulic motor torque override, and variable sea-state spectral period estimation). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_AHC_Drawworks\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Deep-Sea Oil Platform Active Heave Compensation (AHC) Drawworks

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_AHC_Drawworks
VAR_INPUT
    bSystemEnable       : BOOL;     (* Main AHC System Enable *)
    bEmergencyStop      : BOOL;     (* Safety loop status (TRUE = OK) *)
    rMRUSensorHeave     : REAL;     (* Motion Reference Unit - Heave (meters) *)
    rMRUSensorVel       : REAL;     (* Motion Reference Unit - Heave Velocity (m/s) *)
    rDrawworksTension   : REAL;     (* Dynamic tension from load cell (kN) *)
    rHydraulicPress     : REAL;     (* Main hydraulic ring pressure (bar) *)
END_VAR
VAR_OUTPUT
    bSystemReady        : BOOL;     (* System ready for operation *)
    bActiveComp         : BOOL;     (* Active Heave Compensation running *)
    rWinchSpeedCmd      : REAL;     (* Speed command to drawworks winch (m/s) *)
    rWinchTorqueCmd     : REAL;     (* Torque limit command (Nm) *)
    bAlarmFault         : BOOL;     (* General system fault / alarm *)
    iFaultCode          : INT;      (* Specific fault code for SCADA *)
END_VAR
VAR
    iState              : INT := 0; (* Internal state machine *)
    rFilteredHeave      : REAL := 0.0;
    rFilteredTension    : REAL := 0.0;
    rAlphaHeave         : REAL := 0.15; (* Low-pass filter constant for Heave *)
    rAlphaTension       : REAL := 0.05; (* Low-pass filter constant for Tension *)
    
    tStartDelay         : TON;      (* Startup sequence timer *)
    tFaultReset         : TON;      (* Fault reset timer limit *)
    
    (* Internal Limits *)
    rMaxHeave           : REAL := 8.5;  (* Max allowable heave compensation range *)
    rMinTension         : REAL := 15.0; (* Minimum snap-load tension limit *)
    rMaxTension         : REAL := 450.0;(* Maximum overload tension limit *)
    
    (* Sea-State Estimation *)
    rPeakHeaveLast      : REAL;
    tSeaStateTimer      : TON;
END_VAR

(* === MAIN LOGIC === *)
(* 1. Multi-Layered Safety Interlocks & E-Stop *)
IF NOT bEmergencyStop OR rHydraulicPress < 150.0 THEN
    bSystemReady := FALSE;
    bActiveComp  := FALSE;
    rWinchSpeedCmd := 0.0;
    rWinchTorqueCmd := 0.0;
    bAlarmFault := TRUE;
    iState := 999; (* FAULT STATE *)
    IF NOT bEmergencyStop THEN
        iFaultCode := 101; (* E-STOP Active *)
    ELSE
        iFaultCode := 102; (* Low Hydraulic Pressure *)
    END_IF;
    RETURN;
END_IF;

(* 2. Sensor Noise Filtering (Low-Pass IIR) *)
rFilteredHeave := rFilteredHeave + rAlphaHeave * (rMRUSensorHeave - rFilteredHeave);
rFilteredTension := rFilteredTension + rAlphaTension * (rDrawworksTension - rFilteredTension);

(* 3. Tension Out-of-Bounds Detection *)
IF (rFilteredTension < rMinTension) OR (rFilteredTension > rMaxTension) THEN
    bAlarmFault := TRUE;
    iFaultCode := 201; (* Tension out of limits *)
    iState := 999;
    RETURN;
END_IF;

(* 4. Main State Machine for AHC Drawworks *)
CASE iState OF
    0: (* IDLE & SYSTEM CHECKS *)
        bSystemReady := FALSE;
        bActiveComp  := FALSE;
        rWinchSpeedCmd := 0.0;
        bAlarmFault := FALSE;
        iFaultCode := 0;
        
        IF bSystemEnable AND bEmergencyStop THEN
            iState := 10;
        END_IF;

    10: (* STARTUP SEQUENCE *)
        tStartDelay(IN := TRUE, PT := T#3S);
        IF tStartDelay.Q THEN
            tStartDelay(IN := FALSE);
            bSystemReady := TRUE;
            iState := 20;
        END_IF;

    20: (* READY / PASSIVE HEAVE COMP *)
        bSystemReady := TRUE;
        bActiveComp := FALSE;
        rWinchSpeedCmd := 0.0;
        
        IF ABS(rFilteredHeave) > 0.5 THEN
            iState := 30; (* Engage Active Compensation *)
        END_IF;
        
        IF NOT bSystemEnable THEN
            iState := 0;
        END_IF;

    30: (* ACTIVE HEAVE COMPENSATION RUNNING *)
        bActiveComp := TRUE;
        
        (* Core AHC Kinematic Speed Command Calculation: Target inverse velocity *)
        rWinchSpeedCmd := -1.0 * rMRUSensorVel * 0.98; (* 98% efficiency tracking factor *)
        
        (* Dynamic Torque Override based on Tension *)
        IF rFilteredTension > (rMaxTension * 0.8) THEN
            (* Throttle torque if nearing max safe working load *)
            rWinchTorqueCmd := 15000.0 * ((rMaxTension - rFilteredTension) / (rMaxTension * 0.2));
        ELSE
            rWinchTorqueCmd := 15000.0; (* Nominal AHC working torque *)
        END_IF;
        
        (* Soft Limit Handling *)
        IF ABS(rFilteredHeave) > rMaxHeave THEN
            rWinchSpeedCmd := 0.0;
            bAlarmFault := TRUE;
            iFaultCode := 301; (* Soft stroke limit reached *)
            iState := 999;
        END_IF;

        IF NOT bSystemEnable THEN
            iState := 0;
        END_IF;

    999: (* FAULT HANDLING *)
        bSystemReady := FALSE;
        bActiveComp := FALSE;
        rWinchSpeedCmd := 0.0;
        
        tFaultReset(IN := bSystemEnable, PT := T#5S);
        IF tFaultReset.Q THEN
            IF bEmergencyStop AND rHydraulicPress >= 150.0 AND rFilteredTension > rMinTension THEN
                bAlarmFault := FALSE;
                iFaultCode := 0;
                iState := 0;
                tFaultReset(IN := FALSE);
            END_IF;
        END_IF;

END_CASE;

END_FUNCTION_BLOCK
```"""

os.makedirs("C:/Users/majip/Downloads/LLM REASEARCH/data/swarm_raw", exist_ok=True)
filename = f"C:/Users/majip/Downloads/LLM REASEARCH/data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump({"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}, f, ensure_ascii=False)
print(f"Saved to {filename}")
