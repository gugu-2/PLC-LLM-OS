import os, json, uuid

prompt = """<USER_REQUEST>
You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Utility-Scale Pumped Hydro Storage Reversible Pump-Turbine**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., active runner wicket gate synchronized positioning, penstock water hammer pressure transient active damping, and critical transition state logic between pumping/generating). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_PumpedHydroTurbine\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Utility-Scale Pumped Hydro Storage Reversible Pump-Turbine

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT.
</USER_REQUEST>"""

code = """```iec-st
FUNCTION_BLOCK FB_PumpedHydroStorageControl
VAR_INPUT
    bEnableMaster       : BOOL;     (* System master enable for transition and regulation *)
    bEmergencyStop      : BOOL;     (* Main safety trip from hardwired relays *)
    bRequestGenerate    : BOOL;     (* Request to transition to generation mode *)
    bRequestPump        : BOOL;     (* Request to transition to pumping mode *)
    rPenstockPressure   : REAL;     (* Measured penstock water pressure [bar] *)
    rRunnerSpeed        : REAL;     (* Runner rotational speed [rpm] *)
    rGridFreq           : REAL;     (* Grid frequency for synchronization [Hz] *)
    rWicketGateFb       : REAL;     (* Actual wicket gate position feedback [%] *)
END_VAR
VAR_OUTPUT
    bSystemReady        : BOOL;     (* Indication that system is ready for grid sync *)
    rWicketGateSetpt    : REAL;     (* Commanded wicket gate position [%] *)
    bBypassValveCmd     : BOOL;     (* Command to open bypass valve for surge relief *)
    bMainBreakerClose   : BOOL;     (* Command to close generator/motor breaker *)
    bAlarmWaterHammer   : BOOL;     (* Alarm for critical penstock pressure surge *)
    bCriticalFault      : BOOL;     (* Trip command for fatal control failure *)
END_VAR
VAR
    iOpMode             : INT := 0; (* 0=Stop, 1=PrepGen, 2=Gen, 3=PrepPump, 4=Pump *)
    iState              : INT := 0; (* Internal state machine *)
    tSyncTimer          : TON;
    tSurgeReliefTmr     : TON;
    rErrorSpeed         : REAL;
    rKp                 : REAL := 1.25;
    rKi                 : REAL := 0.45;
    rIntegralTerm       : REAL := 0.0;
    rMaxPressureLimit   : REAL := 85.0; (* bar *)
    bWaterHammerDetect  : BOOL := FALSE;
    bModeTransition     : BOOL := FALSE;
END_VAR

(* === MAIN LOGIC === *)

(* 1. Safety and Interlocks *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bCriticalFault := TRUE;
    rWicketGateSetpt := 0.0;
    bMainBreakerClose := FALSE;
    bBypassValveCmd := TRUE; (* Open bypass to relieve pressure safely *)
    iOpMode := 0;
    iState := 0;
    RETURN;
ELSE
    bCriticalFault := FALSE;
END_IF;

(* 2. Water Hammer Active Damping & Surge Protection *)
IF rPenstockPressure > rMaxPressureLimit THEN
    bWaterHammerDetect := TRUE;
    bAlarmWaterHammer := TRUE;
    tSurgeReliefTmr(IN := TRUE, PT := T#3S);
    bBypassValveCmd := TRUE; 
    (* Actively reduce wicket gate opening to dampen transient *)
    rWicketGateSetpt := rWicketGateSetpt * 0.98;
ELSE
    tSurgeReliefTmr(IN := FALSE);
    IF bWaterHammerDetect AND NOT tSurgeReliefTmr.Q THEN
        bWaterHammerDetect := FALSE;
        bAlarmWaterHammer := FALSE;
        bBypassValveCmd := FALSE;
    END_IF;
END_IF;

(* 3. Mode Selection & Master Control State Machine *)
CASE iState OF
    0: (* STANDBY / IDLE *)
        rWicketGateSetpt := 0.0;
        bSystemReady := FALSE;
        bMainBreakerClose := FALSE;
        IF bEnableMaster THEN
            IF bRequestGenerate AND NOT bRequestPump THEN
                iOpMode := 1;
                iState := 10;
            ELSIF bRequestPump AND NOT bRequestGenerate THEN
                iOpMode := 3;
                iState := 20;
            END_IF;
        END_IF;

    10: (* PREPARE GENERATION - RUNNER ACCELERATION *)
        (* Open wicket gates gradually to accelerate runner *)
        IF rWicketGateSetpt < 15.0 THEN
            rWicketGateSetpt := rWicketGateSetpt + 0.1;
        END_IF;
        
        (* Sync speed control approx 300 RPM for 50Hz typically *)
        rErrorSpeed := 300.0 - rRunnerSpeed;
        
        IF ABS(rErrorSpeed) < 2.0 THEN
            tSyncTimer(IN := TRUE, PT := T#5S);
            IF tSyncTimer.Q THEN
                iState := 15; (* Ready to sync *)
            END_IF;
        ELSE
            tSyncTimer(IN := FALSE);
        END_IF;

    15: (* SYNCHRONIZATION AND GRID CONNECT *)
        bSystemReady := TRUE;
        (* Assume external synchro-check relay closes breaker or we command it *)
        IF ABS(rGridFreq - 50.0) < 0.2 THEN
            bMainBreakerClose := TRUE;
            iOpMode := 2;
            iState := 100; (* Generating *)
        END_IF;

    20: (* PREPARE PUMPING - BLOWDOWN AND MOTOR START *)
        (* Pumping requires driving the runner as a motor in water or air *)
        (* Simplified logic for starter motor / VFD sequence *)
        bSystemReady := TRUE;
        tSyncTimer(IN := TRUE, PT := T#10S);
        IF tSyncTimer.Q THEN
            bMainBreakerClose := TRUE;
            iOpMode := 4;
            iState := 200; (* Pumping *)
        END_IF;

    100: (* GENERATING - ACTIVE POWER CONTROL *)
        (* PI Control for speed/power regulation *)
        IF NOT bWaterHammerDetect THEN
            rErrorSpeed := 300.0 - rRunnerSpeed;
            rIntegralTerm := rIntegralTerm + (rErrorSpeed * rKi * 0.1); 
            (* Anti-windup *)
            IF rIntegralTerm > 100.0 THEN rIntegralTerm := 100.0; END_IF;
            IF rIntegralTerm < 0.0 THEN rIntegralTerm := 0.0; END_IF;
            
            rWicketGateSetpt := (rErrorSpeed * rKp) + rIntegralTerm;
            
            (* Limit wicket gate max opening *)
            IF rWicketGateSetpt > 95.0 THEN
                rWicketGateSetpt := 95.0;
            END_IF;
        END_IF;
        
        IF NOT bEnableMaster OR NOT bRequestGenerate THEN
            iState := 900; (* Shutdown sequence *)
        END_IF;

    200: (* PUMPING - DISCHARGE CONTROL *)
        (* Open wicket gates to optimal pumping efficiency point *)
        IF rWicketGateSetpt < 75.0 THEN
             rWicketGateSetpt := rWicketGateSetpt + 0.5;
        END_IF;
        
        IF NOT bEnableMaster OR NOT bRequestPump THEN
            iState := 900; (* Shutdown sequence *)
        END_IF;

    900: (* SHUTDOWN SEQUENCE *)
        bMainBreakerClose := FALSE;
        rIntegralTerm := 0.0;
        IF rWicketGateSetpt > 0.0 THEN
            rWicketGateSetpt := rWicketGateSetpt - 0.5;
        ELSE
            iState := 0;
            iOpMode := 0;
        END_IF;

END_CASE;

END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
print(f"Saved to {filename}")
