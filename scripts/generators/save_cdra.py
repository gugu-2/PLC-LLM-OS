import json, uuid
import os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Advanced Spacecraft Carbon Dioxide (CO2) Removal Assembly (CDRA)**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Zeolite molecular sieve dual-bed thermal swing adsorption, deep space vacuum desorb cascading, and multi-valve synchronization for zero-air-loss cycling). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_SpacecraftCDRA\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Advanced Spacecraft Carbon Dioxide (CO2) Removal Assembly (CDRA)

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_SpacecraftCDRA
(* 
   Advanced Spacecraft Carbon Dioxide Removal Assembly (CDRA)
   Implements a Zeolite molecular sieve dual-bed thermal swing adsorption cycle.
   Features include deep space vacuum desorb cascading and multi-valve synchronization 
   for zero-air-loss cycling.
*)
VAR_INPUT
    (* Required: at least 4-8 physical inputs with types and comments *)
    bEnable                 : BOOL;     (* System overall enable signal *)
    bEmergencyStop          : BOOL;     (* Safety relay OK / emergency stop interlock *)
    rCabinCO2Level          : REAL;     (* Measured cabin CO2 partial pressure (mmHg) *)
    rBed1Temp               : REAL;     (* Bed 1 internal temperature (Deg C) *)
    rBed2Temp               : REAL;     (* Bed 2 internal temperature (Deg C) *)
    bVacuumVentValveClosed  : BOOL;     (* Deep space vacuum vent valve limit switch closed *)
    bAirSavePumpStatus      : BOOL;     (* Air save pump operational status *)
END_VAR
VAR_OUTPUT
    (* Required: at least 3-6 outputs with types and comments *)
    bSystemReady            : BOOL;     (* System ready for active cycle operation *)
    rHeaterControlBed1      : REAL;     (* PID control signal for Bed 1 heater (0.0-100.0%) *)
    rHeaterControlBed2      : REAL;     (* PID control signal for Bed 2 heater (0.0-100.0%) *)
    bDesorbVacuumValveCmd   : BOOL;     (* Command to open deep space vacuum desorb valve *)
    bAirSaveValveCmd        : BOOL;     (* Command to route initial desorb volume to air save pump *)
    iCurrentCycleState      : INT;      (* Current operating mode/state of the CDRA *)
    bCriticalAlarm          : BOOL;     (* Latched fault/alarm status *)
END_VAR
VAR
    (* Internal state tracking and timers *)
    iState                  : INT := 0;
    tCycleTimer             : TON;
    tValveSyncTimer         : TON;
    rTargetDesorbTemp       : REAL := 204.4; (* Nominal 400F for Zeolite regeneration *)
    rCO2ThresholdHigh       : REAL := 3.0;   (* Partial pressure to trigger active scrubbing *)
    rCO2ThresholdLow        : REAL := 1.5;   (* Partial pressure to enter standby mode *)
    
    (* Valve interlock flags to ensure zero-air-loss transitions *)
    bBed1Adsorbing          : BOOL := FALSE;
    bBed2Adsorbing          : BOOL := FALSE;
END_VAR

(* === MAIN LOGIC === *)
(* Immediate safety override *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    rHeaterControlBed1 := 0.0;
    rHeaterControlBed2 := 0.0;
    bDesorbVacuumValveCmd := FALSE;
    bAirSaveValveCmd := FALSE;
    bCriticalAlarm := TRUE;
    iState := 999; (* Fault state *)
    iCurrentCycleState := iState;
    RETURN;
END_IF;

(* Main State Machine for Dual-Bed Cycle *)
CASE iState OF
    0: (* IDLE / INITIALIZATION *)
        bSystemReady := TRUE;
        bCriticalAlarm := FALSE;
        rHeaterControlBed1 := 0.0;
        rHeaterControlBed2 := 0.0;
        IF bEnable AND (rCabinCO2Level > rCO2ThresholdHigh) THEN
            iState := 10;
        END_IF;

    10: (* AIR SAVE PHASE - BED 1 TO DESORB *)
        (* Route initial interstitial air from Bed 1 back to cabin via pump before exposing to vacuum *)
        bBed1Adsorbing := FALSE;
        bBed2Adsorbing := TRUE;
        bAirSaveValveCmd := TRUE;
        tValveSyncTimer(IN := TRUE, PT := T#30S);
        
        IF tValveSyncTimer.Q AND bAirSavePumpStatus THEN
            tValveSyncTimer(IN := FALSE);
            bAirSaveValveCmd := FALSE;
            iState := 20;
        ELSIF tValveSyncTimer.Q AND NOT bAirSavePumpStatus THEN
            (* Pump failure during air save *)
            bCriticalAlarm := TRUE;
            iState := 999;
        END_IF;

    20: (* THERMAL SWING DESORB PHASE - BED 1 *)
        (* Open deep space vent and begin heating Bed 1 for regeneration *)
        bDesorbVacuumValveCmd := TRUE;
        
        (* Proportional heating logic - simplified for PLC simulation *)
        IF rBed1Temp < rTargetDesorbTemp THEN
            rHeaterControlBed1 := 100.0;
        ELSE
            rHeaterControlBed1 := 10.0; (* Maintenance heat *)
        END_IF;
        
        tCycleTimer(IN := TRUE, PT := T#14400S); (* 4 Hour Half-Cycle *)
        
        IF tCycleTimer.Q THEN
            tCycleTimer(IN := FALSE);
            rHeaterControlBed1 := 0.0;
            bDesorbVacuumValveCmd := FALSE;
            iState := 30;
        END_IF;

    30: (* BED CHANGEOVER - COOL DOWN & REPRESSURIZE *)
        (* Close vacuum and allow Bed 1 to cool before returning to adsorption *)
        IF bVacuumVentValveClosed THEN
            IF rBed1Temp < 50.0 THEN
                iState := 40;
            END_IF;
        END_IF;

    40: (* SYMMETRIC AIR SAVE PHASE - BED 2 TO DESORB *)
        bBed1Adsorbing := TRUE;
        bBed2Adsorbing := FALSE;
        bAirSaveValveCmd := TRUE;
        tValveSyncTimer(IN := TRUE, PT := T#30S);
        
        IF tValveSyncTimer.Q AND bAirSavePumpStatus THEN
            tValveSyncTimer(IN := FALSE);
            bAirSaveValveCmd := FALSE;
            iState := 50;
        END_IF;

    50: (* THERMAL SWING DESORB PHASE - BED 2 *)
        bDesorbVacuumValveCmd := TRUE;
        
        IF rBed2Temp < rTargetDesorbTemp THEN
            rHeaterControlBed2 := 100.0;
        ELSE
            rHeaterControlBed2 := 10.0;
        END_IF;
        
        tCycleTimer(IN := TRUE, PT := T#14400S); 
        
        IF tCycleTimer.Q THEN
            tCycleTimer(IN := FALSE);
            rHeaterControlBed2 := 0.0;
            bDesorbVacuumValveCmd := FALSE;
            iState := 60;
        END_IF;

    60: (* CYCLE COMPLETE - STANDBY OR RESTART *)
        IF bVacuumVentValveClosed AND (rBed2Temp < 50.0) THEN
            IF rCabinCO2Level <= rCO2ThresholdLow THEN
                iState := 0; (* Return to standby *)
            ELSE
                iState := 10; (* Continue cycle *)
            END_IF;
        END_IF;
        
    999: (* FAULT HANDLING *)
        bDesorbVacuumValveCmd := FALSE;
        bAirSaveValveCmd := FALSE;
        rHeaterControlBed1 := 0.0;
        rHeaterControlBed2 := 0.0;
        IF NOT bEmergencyStop THEN
            (* Wait for safety relay reset *)
        ELSE
            IF bEnable THEN 
                bCriticalAlarm := FALSE;
                iState := 0; 
            END_IF;
        END_IF;

END_CASE;

iCurrentCycleState := iState;

END_FUNCTION_BLOCK
```"""

import os
target_dir = os.path.join(os.getcwd(), "data", "swarm_raw")
os.makedirs(target_dir, exist_ok=True)
filename = os.path.join(target_dir, f"agent_{uuid.uuid4().hex[:8]}.json")
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print(f"Saved to {filename}")
