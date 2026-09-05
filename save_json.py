import json, uuid, os
prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Semiconductor Chemical Vapor Deposition (CVD) Graphene Furnace**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Precursor mass flow synchronization, 1000°C isothermal zone mapping, and inert argon purging cross-contamination lock). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_CVD_GrapheneFurnace\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Semiconductor Chemical Vapor Deposition (CVD) Graphene Furnace

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_CVD_GrapheneFurnace
VAR_INPUT
    (* Physical inputs for the CVD Furnace System *)
    bEnable                 : BOOL;     (* System enable signal from master recipe controller *)
    bEmergencyStop          : BOOL;     (* Safety relay OK signal (E-Stop Loop) *)
    rTempZone1              : REAL;     (* Temperature of Zone 1 in deg C *)
    rTempZone2              : REAL;     (* Temperature of Zone 2 in deg C *)
    rTempZone3              : REAL;     (* Temperature of Zone 3 in deg C *)
    rMassFlowArgon          : REAL;     (* Actual mass flow of Argon in sccm *)
    rMassFlowMethane        : REAL;     (* Actual mass flow of Methane (Precursor) in sccm *)
    rChamberPressure        : REAL;     (* Vacuum chamber pressure in Torr *)
END_VAR
VAR_OUTPUT
    (* Outputs to Physical Actuators and Status Flags *)
    bSystemReady            : BOOL;     (* System ready status for recipe execution *)
    rHeaterControlZone1     : REAL;     (* Control signal to Zone 1 thyristor (0-100%) *)
    rHeaterControlZone2     : REAL;     (* Control signal to Zone 2 thyristor (0-100%) *)
    rHeaterControlZone3     : REAL;     (* Control signal to Zone 3 thyristor (0-100%) *)
    rMFCSetPointArgon       : REAL;     (* Mass flow controller setpoint for Argon (sccm) *)
    rMFCSetPointMethane     : REAL;     (* Mass flow controller setpoint for Methane (sccm) *)
    bVacuumPumpEnable       : BOOL;     (* Vacuum pump operation command *)
    bAlarm                  : BOOL;     (* Critical fault alarm output *)
    iCurrentState           : INT;      (* Current state of the CVD process *)
END_VAR
VAR
    (* Internal state variables and timers *)
    iState                  : INT := 0;
    tPurgeTimer             : TON;
    tGrowthTimer            : TON;
    tCoolDownTimer          : TON;
    rTargetTemp             : REAL := 1000.0; (* 1000°C isothermal target *)
    rTolerance              : REAL := 2.5;    (* Temperature tolerance in deg C *)
    bTempStable             : BOOL;
    
    (* PI Controller States (Simplified for example) *)
    rErrorZ1                : REAL;
    rErrorZ2                : REAL;
    rErrorZ3                : REAL;
END_VAR

(* === MAIN LOGIC === *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bAlarm := TRUE;
    rHeaterControlZone1 := 0.0;
    rHeaterControlZone2 := 0.0;
    rHeaterControlZone3 := 0.0;
    rMFCSetPointArgon := 0.0;
    rMFCSetPointMethane := 0.0;
    bVacuumPumpEnable := FALSE;
    iState := 999; (* Fault State *)
    iCurrentState := iState;
    RETURN;
END_IF;

bAlarm := FALSE;
bTempStable := (ABS(rTempZone1 - rTargetTemp) < rTolerance) AND 
               (ABS(rTempZone2 - rTargetTemp) < rTolerance) AND 
               (ABS(rTempZone3 - rTargetTemp) < rTolerance);

CASE iState OF
    0: (* IDLE & STANDBY *)
        bSystemReady := TRUE;
        bVacuumPumpEnable := FALSE;
        rHeaterControlZone1 := 0.0;
        rHeaterControlZone2 := 0.0;
        rHeaterControlZone3 := 0.0;
        rMFCSetPointArgon := 0.0;
        rMFCSetPointMethane := 0.0;
        IF bEnable THEN
            bSystemReady := FALSE;
            iState := 10;
        END_IF;

    10: (* PUMPDOWN TO BASE PRESSURE *)
        bVacuumPumpEnable := TRUE;
        IF rChamberPressure < 0.01 THEN (* 10 mTorr base *)
            iState := 20;
        END_IF;

    20: (* INERT ARGON PURGE (CROSS-CONTAMINATION LOCK) *)
        rMFCSetPointArgon := 1000.0; (* 1000 sccm purge *)
        rMFCSetPointMethane := 0.0;
        tPurgeTimer(IN := TRUE, PT := T#5M);
        IF tPurgeTimer.Q THEN
            tPurgeTimer(IN := FALSE);
            iState := 30;
        END_IF;

    30: (* HEATING TO ISOTHERMAL 1000C *)
        (* Basic Proportional Control for demonstration *)
        rErrorZ1 := rTargetTemp - rTempZone1;
        rErrorZ2 := rTargetTemp - rTempZone2;
        rErrorZ3 := rTargetTemp - rTempZone3;
        
        rHeaterControlZone1 := LIMIT(0.0, rErrorZ1 * 2.5, 100.0);
        rHeaterControlZone2 := LIMIT(0.0, rErrorZ2 * 2.5, 100.0);
        rHeaterControlZone3 := LIMIT(0.0, rErrorZ3 * 2.5, 100.0);
        
        IF bTempStable THEN
            iState := 40;
        END_IF;

    40: (* GRAPHENE PRECURSOR INTRODUCTION & GROWTH *)
        rMFCSetPointArgon := 500.0;
        rMFCSetPointMethane := 15.0; (* Introduce Methane for Growth *)
        
        (* Maintain Heat *)
        rHeaterControlZone1 := LIMIT(0.0, (rTargetTemp - rTempZone1) * 2.5, 100.0);
        rHeaterControlZone2 := LIMIT(0.0, (rTargetTemp - rTempZone2) * 2.5, 100.0);
        rHeaterControlZone3 := LIMIT(0.0, (rTargetTemp - rTempZone3) * 2.5, 100.0);
        
        tGrowthTimer(IN := TRUE, PT := T#30M); (* 30 Min Growth *)
        IF tGrowthTimer.Q THEN
            tGrowthTimer(IN := FALSE);
            iState := 50;
        END_IF;

    50: (* POST-GROWTH COOL DOWN & PURGE *)
        rHeaterControlZone1 := 0.0;
        rHeaterControlZone2 := 0.0;
        rHeaterControlZone3 := 0.0;
        rMFCSetPointMethane := 0.0;
        rMFCSetPointArgon := 1000.0; (* Maintain Argon for protective cooling *)
        
        IF (rTempZone1 < 100.0) AND (rTempZone2 < 100.0) AND (rTempZone3 < 100.0) THEN
            iState := 60;
        END_IF;

    60: (* COMPLETE *)
        bVacuumPumpEnable := FALSE;
        rMFCSetPointArgon := 0.0;
        bSystemReady := TRUE;
        IF NOT bEnable THEN
            iState := 0;
        END_IF;
        
    999: (* FAULT HANDLING *)
        bSystemReady := FALSE;
        IF bEmergencyStop THEN
            iState := 0;
        END_IF;

END_CASE;

iCurrentState := iState;

END_FUNCTION_BLOCK
```"""
os.makedirs("data/swarm_raw", exist_ok=True)
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
