import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Utility-Scale Compressed Air Energy Storage (CAES) Turbine**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., multi-stage adiabatic expansion, thermal energy storage (TES) oil/salt recuperation loops, and synchronous condenser grid-tie synchronization). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_CAESTurbine\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Utility-Scale Compressed Air Energy Storage (CAES) Turbine

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_CAES_TurbineControl
VAR_INPUT
    bEnableCmd          : BOOL;  (* Master enable command from DCS *)
    bEmergencyStop      : BOOL;  (* Hardwired safety loop OK (active high) *)
    rAirMassFlowCmd     : REAL;  (* Setpoint for air mass flow (kg/s) *)
    rCavernPressure     : REAL;  (* Pressure in the underground salt cavern (bar) *)
    rGridFreq           : REAL;  (* Grid frequency (Hz) for synch condenser mode *)
    rTES_HotTemp        : REAL;  (* Thermal Energy Storage hot fluid temperature (C) *)
    rTurbineSpeed       : REAL;  (* Current turbine speed (RPM) *)
    rVibrationLevel     : REAL;  (* Peak vibration measurement (mm/s) *)
END_VAR
VAR_OUTPUT
    bSystemReady        : BOOL;  (* Subsystem ready to start expansion *)
    bGridSynchronized   : BOOL;  (* Synchronous condenser grid-tied status *)
    rInletValvePos      : REAL;  (* Main air inlet control valve position (0-100%) *)
    rRecuperatorValve   : REAL;  (* TES fluid recuperator valve position (0-100%) *)
    bWarning            : BOOL;  (* Non-critical warning alarm *)
    bCriticalTrip       : BOOL;  (* Critical safety trip activated *)
END_VAR
VAR
    iMainState          : INT := 0; (* Main state machine sequencer *)
    rSpeedError         : REAL;
    rFlowError          : REAL;
    tStartupTimer       : TON;
    tSyncTimer          : TON;
    bSynchCondMode      : BOOL;
    
    (* PI Controller for Speed/Flow *)
    rKp                 : REAL := 2.5;
    rKi                 : REAL := 0.8;
    rIntegralSum        : REAL := 0.0;
    rLastFlowError      : REAL := 0.0;
END_VAR

(* === MAIN LOGIC === *)
(* 1. Safety Interlocks & Limits *)
IF NOT bEmergencyStop OR (rVibrationLevel > 12.5) THEN
    bCriticalTrip := TRUE;
    bSystemReady := FALSE;
    bGridSynchronized := FALSE;
    rInletValvePos := 0.0;
    rRecuperatorValve := 0.0;
    iMainState := 999; (* Fault State *)
    RETURN;
END_IF;

bCriticalTrip := FALSE;

(* 2. Thermal Limits Warning *)
IF rTES_HotTemp < 350.0 THEN
    bWarning := TRUE;
ELSE
    bWarning := FALSE;
END_IF;

(* 3. Main Sequencer *)
CASE iMainState OF
    0: (* IDLE & PRE-CHECKS *)
        rInletValvePos := 0.0;
        rRecuperatorValve := 0.0;
        bSystemReady := (rCavernPressure > 45.0) AND (rTES_HotTemp > 300.0);
        
        IF bSystemReady AND bEnableCmd THEN
            iMainState := 10;
        END_IF;

    10: (* PRE-HEATING RECUPERATOR LOOP *)
        rRecuperatorValve := 35.0; (* Open TES valve slightly to pre-warm *)
        tStartupTimer(IN := TRUE, PT := T#30S);
        
        IF tStartupTimer.Q THEN
            tStartupTimer(IN := FALSE);
            iMainState := 20;
        END_IF;

    20: (* RAMP TO SYNCHRONOUS SPEED (3600 RPM for 60Hz) *)
        rSpeedError := 3600.0 - rTurbineSpeed;
        
        IF rSpeedError > 100.0 THEN
            rInletValvePos := rInletValvePos + 0.1; (* Ramp up *)
        ELSIF rSpeedError < -50.0 THEN
            rInletValvePos := rInletValvePos - 0.1; (* Ramp down *)
        END_IF;
        
        (* Limit valve *)
        IF rInletValvePos > 100.0 THEN rInletValvePos := 100.0; END_IF;
        IF rInletValvePos < 0.0 THEN rInletValvePos := 0.0; END_IF;
        
        IF ABS(rSpeedError) < 15.0 AND (ABS(rGridFreq - 60.0) < 0.05) THEN
            tSyncTimer(IN := TRUE, PT := T#5S);
            IF tSyncTimer.Q THEN
                bGridSynchronized := TRUE;
                tSyncTimer(IN := FALSE);
                iMainState := 30;
            END_IF;
        ELSE
            tSyncTimer(IN := FALSE);
        END_IF;

    30: (* GRID-TIED & LOAD CONTROL *)
        (* Switch to flow/load control since speed is locked to grid *)
        rFlowError := rAirMassFlowCmd - (rInletValvePos * rCavernPressure * 0.01);
        rIntegralSum := rIntegralSum + (rFlowError * 0.1);
        
        IF rIntegralSum > 50.0 THEN rIntegralSum := 50.0; END_IF;
        IF rIntegralSum < -50.0 THEN rIntegralSum := -50.0; END_IF;
        
        rInletValvePos := (rKp * rFlowError) + (rKi * rIntegralSum);
        
        IF rInletValvePos > 100.0 THEN rInletValvePos := 100.0; END_IF;
        IF rInletValvePos < 10.0 THEN rInletValvePos := 10.0; END_IF;
        
        (* Optimize TES Recuperator based on expansion cooling *)
        rRecuperatorValve := 50.0 + (rInletValvePos * 0.5);
        
        IF NOT bEnableCmd THEN
            bGridSynchronized := FALSE;
            iMainState := 40;
        END_IF;
        
    40: (* SHUTDOWN SEQUENCE *)
        rInletValvePos := rInletValvePos - 0.5;
        rRecuperatorValve := rRecuperatorValve - 0.2;
        
        IF (rInletValvePos <= 0.0) AND (rRecuperatorValve <= 0.0) THEN
            iMainState := 0;
        END_IF;
        
    999: (* FAULT HANDLING *)
        (* Wait for operator reset which requires dropping enable cmd and clearing faults *)
        IF NOT bEnableCmd AND NOT bCriticalTrip THEN
            iMainState := 0;
        END_IF;

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
