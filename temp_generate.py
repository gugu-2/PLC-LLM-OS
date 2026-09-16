import json, uuid
import os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Multi-Zone Industrial Continuous Tunnel Glass Tempering Furnace**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Roller hearth oscillating drive sync, top/bottom radiant heating delta-T minimization to prevent glass bowing, and high-pressure air quench blast sequencing). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_Glass_TemperingFurnace\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Multi-Zone Industrial Continuous Tunnel Glass Tempering Furnace

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_Glass_TemperingFurnace
VAR_INPUT
    bSystemEnable       : BOOL;     (* Main system enable signal *)
    bEmergencyStop      : BOOL;     (* Emergency stop circuit OK (True = OK) *)
    rTempTopZone1       : REAL;     (* Measured temperature top zone 1 [deg C] *)
    rTempBotZone1       : REAL;     (* Measured temperature bottom zone 1 [deg C] *)
    rGlassThickness     : REAL;     (* Glass thickness [mm] *)
    rGlassWidth         : REAL;     (* Glass width [mm] *)
    rLineSpeedCmd       : REAL;     (* Master line speed command [mm/s] *)
    bQuenchAirPressureOK: BOOL;     (* High pressure air quench ready *)
END_VAR
VAR_OUTPUT
    bFurnaceReady       : BOOL;     (* Furnace is at temperature and ready for glass *)
    rHeaterPowerTop1    : REAL;     (* Output power to top heater zone 1 [%] *)
    rHeaterPowerBot1    : REAL;     (* Output power to bottom heater zone 1 [%] *)
    rRollerSpeedOut     : REAL;     (* Sync speed for oscillating roller drive [mm/s] *)
    bQuenchBlastEnable  : BOOL;     (* Trigger for quench air blast *)
    bSystemAlarm        : BOOL;     (* Critical fault alarm *)
    iAlarmCode          : INT;      (* Detailed alarm code *)
END_VAR
VAR
    (* Internal State and Processing *)
    iSequenceState      : INT := 0;
    
    (* Filtered values *)
    rTempTopFiltered    : REAL;
    rTempBotFiltered    : REAL;
    
    (* Control parameters *)
    rTempSetpointTop    : REAL := 680.0;
    rTempSetpointBot    : REAL := 675.0; 
    
    (* PID logic states *)
    rErrorTop           : REAL;
    rErrorBot           : REAL;
    rIntegralTop        : REAL := 0.0;
    rIntegralBot        : REAL := 0.0;
    
    (* Constants *)
    Kp : REAL := 2.5;
    Ki : REAL := 0.15;
    MaxPower : REAL := 100.0;
    
    (* Delta-T protection *)
    rDeltaT             : REAL;
    MaxDeltaT           : REAL := 15.0;
    
    (* Timers *)
    tOscillationTimer   : TON;
    bOscDir             : BOOL := FALSE;
    tQuenchDelay        : TON;
END_VAR

(* === MAIN LOGIC === *)
(* 1. Safety & Interlocks *)
IF NOT bEmergencyStop THEN
    bFurnaceReady := FALSE;
    rHeaterPowerTop1 := 0.0;
    rHeaterPowerBot1 := 0.0;
    rRollerSpeedOut := 0.0;
    bQuenchBlastEnable := FALSE;
    bSystemAlarm := TRUE;
    iAlarmCode := 999; (* E-STOP Active *)
    iSequenceState := 0;
    RETURN;
END_IF;

(* 2. Sensor Noise Filtering (EMA filter) *)
rTempTopFiltered := (rTempTopFiltered * 0.9) + (rTempTopZone1 * 0.1);
rTempBotFiltered := (rTempBotFiltered * 0.9) + (rTempBotZone1 * 0.1);

(* 3. Delta-T Minimization (Bowing Prevention) *)
rDeltaT := ABS(rTempTopFiltered - rTempBotFiltered);
IF rDeltaT > MaxDeltaT THEN
    bSystemAlarm := TRUE;
    iAlarmCode := 101; (* Delta-T limit exceeded *)
    (* Power reduction to prevent severe bowing *)
    MaxPower := 50.0;
ELSE
    bSystemAlarm := FALSE;
    iAlarmCode := 0;
    MaxPower := 100.0;
END_IF;

(* 4. State Machine *)
CASE iSequenceState OF
    0: (* IDLE *)
        bFurnaceReady := FALSE;
        rHeaterPowerTop1 := 0.0;
        rHeaterPowerBot1 := 0.0;
        rRollerSpeedOut := 0.0;
        bQuenchBlastEnable := FALSE;
        IF bSystemEnable THEN
            iSequenceState := 10;
        END_IF;

    10: (* HEATING UP *)
        (* Simple PID implementation for top zone *)
        rErrorTop := rTempSetpointTop - rTempTopFiltered;
        rIntegralTop := rIntegralTop + rErrorTop;
        rHeaterPowerTop1 := (Kp * rErrorTop) + (Ki * rIntegralTop);
        
        (* Simple PID implementation for bottom zone *)
        rErrorBot := rTempSetpointBot - rTempBotFiltered;
        rIntegralBot := rIntegralBot + rErrorBot;
        rHeaterPowerBot1 := (Kp * rErrorBot) + (Ki * rIntegralBot);
        
        (* Clamp outputs *)
        IF rHeaterPowerTop1 > MaxPower THEN rHeaterPowerTop1 := MaxPower; END_IF;
        IF rHeaterPowerTop1 < 0.0 THEN rHeaterPowerTop1 := 0.0; END_IF;
        IF rHeaterPowerBot1 > MaxPower THEN rHeaterPowerBot1 := MaxPower; END_IF;
        IF rHeaterPowerBot1 < 0.0 THEN rHeaterPowerBot1 := 0.0; END_IF;
        
        IF (ABS(rTempSetpointTop - rTempTopFiltered) < 5.0) AND 
           (ABS(rTempSetpointBot - rTempBotFiltered) < 5.0) THEN
            iSequenceState := 20;
        END_IF;

    20: (* READY / RUNNING *)
        bFurnaceReady := TRUE;
        
        (* Roller hearth oscillation logic for heat uniformity *)
        tOscillationTimer(IN := NOT tOscillationTimer.Q, PT := T#2S);
        IF tOscillationTimer.Q THEN
            bOscDir := NOT bOscDir;
        END_IF;
        
        IF bOscDir THEN
            rRollerSpeedOut := rLineSpeedCmd * 1.1;
        ELSE
            rRollerSpeedOut := rLineSpeedCmd * 0.9;
        END_IF;
        
        (* Quench sequence trigger based on thickness threshold simulation *)
        IF rGlassThickness > 6.0 AND bQuenchAirPressureOK THEN
            tQuenchDelay(IN := TRUE, PT := T#3S);
            IF tQuenchDelay.Q THEN
                bQuenchBlastEnable := TRUE;
            END_IF;
        ELSE
            bQuenchBlastEnable := FALSE;
            tQuenchDelay(IN := FALSE);
        END_IF;

        IF NOT bSystemEnable THEN
            iSequenceState := 0;
        END_IF;
        
    ELSE
        iSequenceState := 0;
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
