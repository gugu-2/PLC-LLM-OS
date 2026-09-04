import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Advanced Pharmaceutical Lyophilizer (Freeze Dryer)**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., shelf temperature sublimation profiling, vacuum pump condenser coil frost management, and Pirani/capacitance manometer gauge crossover logic). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_Lyophilizer\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Advanced Pharmaceutical Lyophilizer (Freeze Dryer)

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_AdvPharmaLyophilizer
VAR_INPUT
    (* Required: at least 4-8 physical inputs with types and comments *)
    bEnable                 : BOOL;     (* System master enable signal *)
    bEmergencyStop          : BOOL;     (* Safety relay OK signal (E-STOP loop) *)
    rShelfTemp1             : REAL;     (* Primary shelf temperature measurement (deg C) *)
    rShelfTemp2             : REAL;     (* Secondary shelf temperature measurement (deg C) *)
    rCondenserTemp          : REAL;     (* Condenser coil temperature (deg C) *)
    rChamberPressurePirani  : REAL;     (* Chamber pressure via Pirani gauge (mBar) *)
    rChamberPressureCapMan  : REAL;     (* Chamber pressure via Capacitance Manometer (mBar) *)
    rSublimationTargetTemp  : REAL;     (* Recipe sublimation target temperature (deg C) *)
END_VAR
VAR_OUTPUT
    (* Required: at least 3-6 outputs with types and comments *)
    bSystemReady            : BOOL;     (* System ready for primary drying status *)
    rHeaterControlOutput    : REAL;     (* PID 0-100% control output for shelf heaters *)
    rVacuumValvePosition    : REAL;     (* Butterfly vacuum valve position 0-100% *)
    bVacuumPumpStart        : BOOL;     (* Command to start main vacuum pump *)
    bCondenserRefrigStart   : BOOL;     (* Command to start condenser refrigeration loop *)
    bAlarm                  : BOOL;     (* System global fault alarm output *)
END_VAR
VAR
    (* Internal state variables and timers *)
    iState                  : INT := 0; (* Internal state machine step *)
    tProcessTimer           : TON;      (* Phase duration timer *)
    tCondenserPreChill      : TON;      (* Condenser pre-chill timer *)
    rActivePressure         : REAL;     (* Blended pressure measurement for control loop *)
    rAvgShelfTemp           : REAL;     (* Average of shelf sensors *)
    rErrorTemp              : REAL;     (* PID error term for heating *)
    rIntegralTerm           : REAL := 0.0; (* PID integral term accumulation *)
    rDerivativeTerm         : REAL := 0.0; (* PID derivative term *)
    rPrevErrorTemp          : REAL := 0.0;
    rKp                     : REAL := 2.5; (* Heater PID Proportional Gain *)
    rKi                     : REAL := 0.05;(* Heater PID Integral Gain *)
    rKd                     : REAL := 1.2; (* Heater PID Derivative Gain *)
END_VAR

(* === MAIN LOGIC === *)
(* 1. Safety Interlocks and Critical Fast-Stop *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bVacuumPumpStart := FALSE;
    bCondenserRefrigStart := FALSE;
    rHeaterControlOutput := 0.0;
    rVacuumValvePosition := 0.0;
    bAlarm := TRUE;
    iState := 999; (* Fault state *)
    RETURN;
END_IF;

(* 2. Signal Processing and Sensor Fusion *)
rAvgShelfTemp := (rShelfTemp1 + rShelfTemp2) / 2.0;

(* Sensor Crossover Logic: Pirani is gas dependent, Capacitance Manometer is absolute. 
   Blend them based on pressure regime. *)
IF rChamberPressureCapMan > 1.0 THEN
    rActivePressure := rChamberPressureCapMan; (* High vacuum range *)
ELSIF rChamberPressureCapMan < 0.1 THEN
    rActivePressure := rChamberPressurePirani; (* Deep vacuum range *)
ELSE
    (* Linear interpolation crossover band *)
    rActivePressure := ((rChamberPressureCapMan - 0.1) / 0.9) * rChamberPressureCapMan + 
                       ((1.0 - rChamberPressureCapMan) / 0.9) * rChamberPressurePirani;
END_IF;

(* 3. Process State Machine *)
CASE iState OF
    0: (* IDLE & PRE-CHECKS *)
        bSystemReady := TRUE;
        bCondenserRefrigStart := FALSE;
        bVacuumPumpStart := FALSE;
        rHeaterControlOutput := 0.0;
        
        IF bEnable THEN
            bSystemReady := FALSE;
            bAlarm := FALSE;
            iState := 10;
        END_IF;

    10: (* CONDENSER PRE-CHILL *)
        bCondenserRefrigStart := TRUE;
        (* Wait for condenser to reach target frost temperature - typically -50C or lower *)
        IF rCondenserTemp <= -50.0 THEN
            tCondenserPreChill(IN := TRUE, PT := T#30M); (* Hold for 30 min soak *)
            IF tCondenserPreChill.Q THEN
                tCondenserPreChill(IN := FALSE);
                iState := 20;
            END_IF;
        ELSE
            tCondenserPreChill(IN := FALSE);
        END_IF;

    20: (* EVACUATION PHASE *)
        bVacuumPumpStart := TRUE;
        rVacuumValvePosition := 100.0; (* Valve fully open *)
        
        IF rActivePressure < 0.2 THEN (* Primary drying start threshold *)
            iState := 30;
        END_IF;

    30: (* PRIMARY DRYING (SUBLIMATION) *)
        (* Execute PID control for shelf heating *)
        rErrorTemp := rSublimationTargetTemp - rAvgShelfTemp;
        rIntegralTerm := rIntegralTerm + (rErrorTemp * rKi);
        
        (* Anti-windup limit for integral term *)
        IF rIntegralTerm > 100.0 THEN rIntegralTerm := 100.0; END_IF;
        IF rIntegralTerm < 0.0 THEN rIntegralTerm := 0.0; END_IF;
        
        rDerivativeTerm := (rErrorTemp - rPrevErrorTemp) * rKd;
        
        rHeaterControlOutput := (rErrorTemp * rKp) + rIntegralTerm + rDerivativeTerm;
        rPrevErrorTemp := rErrorTemp;
        
        (* Saturation limits *)
        IF rHeaterControlOutput > 100.0 THEN rHeaterControlOutput := 100.0; END_IF;
        IF rHeaterControlOutput < 0.0 THEN rHeaterControlOutput := 0.0; END_IF;
        
        (* Vacuum pressure control via butterfly valve (choked flow modulation) *)
        IF rActivePressure > 0.3 THEN
            rVacuumValvePosition := rVacuumValvePosition + 1.0;
        ELSIF rActivePressure < 0.15 THEN
            rVacuumValvePosition := rVacuumValvePosition - 1.0;
        END_IF;
        
        IF rVacuumValvePosition > 100.0 THEN rVacuumValvePosition := 100.0; END_IF;
        IF rVacuumValvePosition < 10.0 THEN rVacuumValvePosition := 10.0; END_IF;
        
        (* Example end condition for primary drying: hold for specific time, or process logic *)
        tProcessTimer(IN := TRUE, PT := T#24H);
        IF tProcessTimer.Q THEN
            tProcessTimer(IN := FALSE);
            iState := 40;
        END_IF;
        
    40: (* SECONDARY DRYING AND FINISH *)
        rHeaterControlOutput := 0.0;
        rVacuumValvePosition := 100.0;
        (* Secondary drying logic would go here. For now, transition to complete. *)
        IF rAvgShelfTemp >= 20.0 THEN (* Return to ambient *)
            iState := 50;
        END_IF;
        
    50: (* COMPLETE / SHUTDOWN *)
        bVacuumPumpStart := FALSE;
        bCondenserRefrigStart := FALSE;
        rVacuumValvePosition := 0.0;
        bSystemReady := TRUE;
        
        IF NOT bEnable THEN
            iState := 0;
        END_IF;
        
    999: (* FAULT RECOVERY *)
        bSystemReady := FALSE;
        (* Require E-Stop reset and master disable to clear fault *)
        IF bEmergencyStop AND NOT bEnable THEN
            bAlarm := FALSE;
            iState := 0;
        END_IF;

END_CASE;

END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump({"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}, f, ensure_ascii=False)

print(f"Saved to {filename}")
