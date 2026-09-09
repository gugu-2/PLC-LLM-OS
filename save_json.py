import json, uuid, os

os.makedirs('data/swarm_raw', exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Industrial Scale Liquid Metal Battery Grid Energy Storage**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Antimony-lead / lithium interface joule heating self-regulation, high-current (10kA) bi-directional DC-DC isolation, and thermal stratification layer mapping). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_LiquidMetalBattery\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Industrial Scale Liquid Metal Battery Grid Energy Storage

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_LiquidMetalBatteryMgmt
VAR_INPUT
    (* Required: at least 4-8 physical inputs with types and comments *)
    bEnable                 : BOOL;     (* System master enable signal *)
    bEmergencyStop          : BOOL;     (* Safety loop OK signal (Active High) *)
    rPackVoltage            : REAL;     (* Measured total pack voltage (V) *)
    rStackCurrent           : REAL;     (* Current flowing through stack (A) - positive is charge *)
    rCoreTemperature        : REAL;     (* Measured core temperature in the molten zone (deg C) *)
    rTopLayerTemp           : REAL;     (* Lithium layer temperature (deg C) *)
    rBottomLayerTemp        : REAL;     (* Antimony-Lead layer temperature (deg C) *)
    rTargetChargeCurrent    : REAL;     (* Target bi-directional DC-DC current (A) *)
END_VAR
VAR_OUTPUT
    (* Required: at least 3-6 outputs with types and comments *)
    bSystemReady            : BOOL;     (* System is nominal and ready for charge/discharge *)
    rCmdDcDcCurrent         : REAL;     (* Commanded current to the 10kA bi-directional DC-DC (A) *)
    bHeaterEnable           : BOOL;     (* Auxiliary heater enable for cold start or low load *)
    rJouleHeatingPwr        : REAL;     (* Estimated internal joule heating power (kW) *)
    bThermalStratWarn       : BOOL;     (* Warning: Thermal stratification boundaries exceeded *)
    bCriticalAlarm          : BOOL;     (* Critical fault active - immediate shutdown *)
END_VAR
VAR
    (* Internal state variables *)
    iOpState                : INT := 0; 
    tPrechargeTimer         : TON;
    tCoolDownTimer          : TON;
    rInternalResistance     : REAL := 0.00015; (* Nominal internal resistance in ohms *)
    rTempDeltaMax           : REAL := 45.0;    (* Max allowed delta T between layers (deg C) *)
    rNominalTemp            : REAL := 480.0;   (* Target operating temp for liquid metal (deg C) *)
END_VAR

(* === MAIN LOGIC === *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bHeaterEnable := FALSE;
    rCmdDcDcCurrent := 0.0;
    bCriticalAlarm := TRUE;
    iOpState := 99; (* Fault state *)
    RETURN;
END_IF;

(* Estimate Joule Heating Power in kW (P = I^2 * R / 1000) *)
rJouleHeatingPwr := (rStackCurrent * rStackCurrent * rInternalResistance) / 1000.0;

(* Check Thermal Stratification limits *)
IF ABS(rTopLayerTemp - rBottomLayerTemp) > rTempDeltaMax THEN
    bThermalStratWarn := TRUE;
ELSE
    bThermalStratWarn := FALSE;
END_IF;

CASE iOpState OF
    0: (* IDLE / OFF *)
        bSystemReady := FALSE;
        rCmdDcDcCurrent := 0.0;
        bCriticalAlarm := FALSE;
        
        IF bEnable AND rCoreTemperature >= (rNominalTemp - 20.0) THEN
            iOpState := 10;
        ELSIF bEnable AND rCoreTemperature < (rNominalTemp - 20.0) THEN
            iOpState := 5; (* Go to auxiliary heating *)
        END_IF;

    5: (* AUXILIARY HEATING *)
        bHeaterEnable := TRUE;
        rCmdDcDcCurrent := 0.0;
        
        IF rCoreTemperature >= (rNominalTemp - 5.0) THEN
            bHeaterEnable := FALSE;
            iOpState := 10;
        END_IF;
        IF NOT bEnable THEN
            bHeaterEnable := FALSE;
            iOpState := 0;
        END_IF;

    10: (* PRECHARGE & STABILIZATION *)
        tPrechargeTimer(IN := TRUE, PT := T#10S);
        IF tPrechargeTimer.Q THEN
            tPrechargeTimer(IN := FALSE);
            iOpState := 20;
        END_IF;

    20: (* RUNNING / ACTIVE CYCLING *)
        bSystemReady := TRUE;
        
        (* Self-regulating heating logic: if joule heating is insufficient, supplement *)
        IF rCoreTemperature < rNominalTemp AND rJouleHeatingPwr < 50.0 THEN
            bHeaterEnable := TRUE;
        ELSE
            bHeaterEnable := FALSE;
        END_IF;
        
        (* Command DC-DC current based on target, but foldback if temp gets too high *)
        IF rCoreTemperature > (rNominalTemp + 30.0) THEN
            rCmdDcDcCurrent := rTargetChargeCurrent * 0.5; (* 50% derate *)
        ELSE
            rCmdDcDcCurrent := rTargetChargeCurrent;
        END_IF;
        
        IF NOT bEnable THEN
            iOpState := 30;
        END_IF;

    30: (* COOLDOWN / RAMP DOWN *)
        bSystemReady := FALSE;
        rCmdDcDcCurrent := 0.0;
        bHeaterEnable := FALSE;
        
        tCoolDownTimer(IN := TRUE, PT := T#30S);
        IF tCoolDownTimer.Q THEN
            tCoolDownTimer(IN := FALSE);
            iOpState := 0;
        END_IF;
        
    99: (* FAULT HANDLING *)
        bSystemReady := FALSE;
        rCmdDcDcCurrent := 0.0;
        bHeaterEnable := FALSE;
        
        IF bEmergencyStop AND NOT bEnable THEN
            (* Wait for user reset via enable toggle *)
            bCriticalAlarm := FALSE;
            iOpState := 0;
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

filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print(f"Saved to {filename}")
