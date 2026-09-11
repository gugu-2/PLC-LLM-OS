import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Advanced Semiconductor Chemical Mechanical Polishing (CMP) Planarization**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., retaining ring / platen multi-zone pneumatic pressure profiling, abrasive slurry viscosity mass flow metering, and optical endpoint laser reflectometry detection). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_CMP_Planarization\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Advanced Semiconductor Chemical Mechanical Polishing (CMP) Planarization

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_CMP_PlanarizationControl
VAR_INPUT
    bEnableSys                  : BOOL;     (* System master enable *)
    bEmergencyStop              : BOOL;     (* Safety circuit OK (Active HIGH) *)
    rWaferPressureZone1         : REAL;     (* Retaining ring pressure feedback [kPa] *)
    rWaferPressureZone2         : REAL;     (* Inner zone pressure feedback [kPa] *)
    rPlatenSpeedFb              : REAL;     (* Platen rotational speed feedback [RPM] *)
    rSlurryMassFlow             : REAL;     (* Abrasive slurry mass flow rate [g/s] *)
    rOpticalReflectance         : REAL;     (* Laser reflectometry intensity [%] *)
    rPolishingTimeTarget        : REAL;     (* Target polishing duration [s] *)
END_VAR
VAR_OUTPUT
    bSystemReady                : BOOL;     (* System ready for polishing cycle *)
    rCmdPressureZone1           : REAL;     (* Command retaining ring pressure [kPa] *)
    rCmdPressureZone2           : REAL;     (* Command inner zone pressure [kPa] *)
    rCmdPlatenSpeed             : REAL;     (* Command platen speed [RPM] *)
    rCmdSlurryFlow              : REAL;     (* Command slurry flow valve [0-100%] *)
    bEndpointReached            : BOOL;     (* Polishing optical endpoint detected *)
    bAlarmFault                 : BOOL;     (* System fault active *)
    iFaultCode                  : INT;      (* Specific fault code for diagnostics *)
END_VAR
VAR
    iState                      : INT := 0; (* Internal state machine *)
    rElapsedTime                : REAL := 0.0;
    tCycleTimer                 : TON;
    rIntegralErrorP1            : REAL := 0.0;
    rIntegralErrorP2            : REAL := 0.0;
    
    (* PID Constants - Tuned for aggressive response on CMP *)
    KP_PRESS : REAL := 1.25;
    KI_PRESS : REAL := 0.45;
    
    rTargetP1 : REAL := 35.0; (* kPa *)
    rTargetP2 : REAL := 28.0; (* kPa *)
    
    rReflectanceDerivative      : REAL := 0.0;
    rPrevReflectance            : REAL := 0.0;
END_VAR

(* === MAIN SAFETY & INTERLOCK LOGIC === *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    rCmdPressureZone1 := 0.0;
    rCmdPressureZone2 := 0.0;
    rCmdPlatenSpeed := 0.0;
    rCmdSlurryFlow := 0.0;
    bAlarmFault := TRUE;
    iFaultCode := 99; (* E-STOP Active *)
    iState := 0;
    RETURN;
END_IF;

(* Clear faults if system enabled normally *)
IF bEnableSys AND iFaultCode = 99 THEN
    bAlarmFault := FALSE;
    iFaultCode := 0;
END_IF;

(* === CMP PROCESS STATE MACHINE === *)
CASE iState OF
    0: (* IDLE & PREPARATION *)
        bSystemReady := TRUE;
        bEndpointReached := FALSE;
        rCmdPlatenSpeed := 0.0;
        rCmdSlurryFlow := 0.0;
        
        IF bEnableSys AND NOT bAlarmFault THEN
            bSystemReady := FALSE;
            iState := 10;
        END_IF;

    10: (* SLURRY PRE-WET & PLATEN SPIN-UP *)
        rCmdSlurryFlow := 75.0; (* 75% valve open for pre-wetting *)
        rCmdPlatenSpeed := 60.0; (* Spin up to 60 RPM *)
        
        IF rPlatenSpeedFb > 58.0 AND rSlurryMassFlow > 10.0 THEN
            iState := 20;
        END_IF;

    20: (* DYNAMIC PRESSURE PROFILING (POLISHING) *)
        (* Closed loop PI control for pneumatic multi-zone pressure *)
        rIntegralErrorP1 := rIntegralErrorP1 + (rTargetP1 - rWaferPressureZone1) * 0.1; 
        rIntegralErrorP2 := rIntegralErrorP2 + (rTargetP2 - rWaferPressureZone2) * 0.1;
        
        (* Anti-windup limit *)
        IF rIntegralErrorP1 > 20.0 THEN rIntegralErrorP1 := 20.0; END_IF;
        IF rIntegralErrorP1 < -20.0 THEN rIntegralErrorP1 := -20.0; END_IF;
        IF rIntegralErrorP2 > 20.0 THEN rIntegralErrorP2 := 20.0; END_IF;
        IF rIntegralErrorP2 < -20.0 THEN rIntegralErrorP2 := -20.0; END_IF;
        
        rCmdPressureZone1 := (rTargetP1 - rWaferPressureZone1) * KP_PRESS + rIntegralErrorP1;
        rCmdPressureZone2 := (rTargetP2 - rWaferPressureZone2) * KP_PRESS + rIntegralErrorP2;
        
        (* Maintain optimal polishing speed and flow *)
        rCmdPlatenSpeed := 90.0; 
        rCmdSlurryFlow := 50.0;
        
        (* Optical Endpoint Detection via Reflectometry Derivative *)
        rReflectanceDerivative := rOpticalReflectance - rPrevReflectance;
        rPrevReflectance := rOpticalReflectance;
        
        (* If reflectance drops sharply, endpoint is reached (oxide cleared to underlying metal/stop layer) *)
        IF rReflectanceDerivative < -5.0 OR rElapsedTime >= rPolishingTimeTarget THEN
            bEndpointReached := TRUE;
            iState := 30;
        END_IF;

        (* Simulated time integration (normally derived from system clock delta) *)
        rElapsedTime := rElapsedTime + 0.1;

    30: (* DE-CHUCK AND RINSE SEQUENCE *)
        rCmdPressureZone1 := 0.0;
        rCmdPressureZone2 := 0.0;
        rCmdSlurryFlow := 0.0; (* Stop slurry, DI water rinse handled externally *)
        rCmdPlatenSpeed := 10.0; (* Slow spin down *)
        
        IF rPlatenSpeedFb < 15.0 THEN
            rCmdPlatenSpeed := 0.0;
            iState := 40;
        END_IF;
        
    40: (* COMPLETE *)
        bSystemReady := TRUE;
        rElapsedTime := 0.0;
        rIntegralErrorP1 := 0.0;
        rIntegralErrorP2 := 0.0;
        IF NOT bEnableSys THEN
            iState := 0;
            bEndpointReached := FALSE;
        END_IF;

    ELSE
        (* INVALID STATE RECOVERY *)
        iFaultCode := 100;
        bAlarmFault := TRUE;
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
