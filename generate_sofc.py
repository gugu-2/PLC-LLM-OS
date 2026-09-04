import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Utility-Scale Solid Oxide Fuel Cell (SOFC) Co-Generation Plant**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., natural gas reforming fuel-to-steam ratio cascading, high-temperature (800°C) stack voltage degradation active trimming, and thermal runaway prevention). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_SOFC_Plant\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
   record = {\"messages\": [{\"role\": \"user\", \"content\": prompt}, {\"role\": \"assistant\", \"content\": code}]}
   with open(f\"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json\", \"w\", encoding=\"utf-8\") as f:
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
6. REPLY with: EVOLUTION COMPLETE: Utility-Scale Solid Oxide Fuel Cell (SOFC) Co-Generation Plant

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_SOFC_PlantControl
VAR_INPUT
    (* System Operation & Safety Signals *)
    bEnableSystem          : BOOL;     (* Main plant enable signal *)
    bEmergencyStop         : BOOL;     (* Safety relay OK (TRUE = OK, FALSE = TRIP) *)
    rPowerDemandKW         : REAL;     (* Grid power demand [kW] *)
    
    (* Physical Process Variables *)
    rStackTempAvg          : REAL;     (* Average stack temperature [deg C] (Target ~ 800) *)
    rFuelCellVoltage       : REAL;     (* Aggregate stack voltage [VDC] *)
    rNaturalGasFlow        : REAL;     (* Natural gas inlet mass flow [kg/s] *)
    rSteamInletFlow        : REAL;     (* Reformer steam inlet mass flow [kg/s] *)
END_VAR
VAR_OUTPUT
    (* System Status *)
    bSystemReady           : BOOL;     (* Plant is ready for grid synchronization *)
    bCriticalAlarm         : BOOL;     (* High-priority shutdown alarm *)
    
    (* Actuator & Converter Commands *)
    rGasValveCmd           : REAL;     (* Natural gas valve position 0-100% *)
    rSteamValveCmd         : REAL;     (* Steam valve position 0-100% for S/C ratio *)
    rStackCurrentRef       : REAL;     (* Reference DC current to inverter [A] *)
    bThermalBypass         : BOOL;     (* Active thermal runaway mitigation bypass *)
END_VAR
VAR
    (* Internal State & Memory *)
    iPlantState            : INT := 0; (* Main State Machine Step *)
    rTargetGasFlow         : REAL;     (* Derived from Power Demand and efficiency curve *)
    rDegradationFactor     : REAL := 1.0; (* Voltage degradation trim / aging compensation *)
    
    (* Timers *)
    tWarmupTimer           : TON;
END_VAR

(* === MAIN SAFETY INTERLOCKS === *)
IF NOT bEmergencyStop THEN
    iPlantState := 999; (* FAULT STATE *)
    bSystemReady := FALSE;
    rGasValveCmd := 0.0;
    rSteamValveCmd := 100.0; (* Maximum steam flow for aggressive purge and cooling *)
    rStackCurrentRef := 0.0;
    bThermalBypass := TRUE;
    bCriticalAlarm := TRUE;
    RETURN;
END_IF;

(* High-Temperature / Thermal Runaway Prevention *)
(* SOFCs typically operate around 800C. Exceeding 850C risks irreversible cell damage. *)
IF rStackTempAvg > 850.0 THEN
    bThermalBypass := TRUE;
    bCriticalAlarm := TRUE;
    (* Immediately shed load to reduce exothermic I2R heating effects *)
    rStackCurrentRef := 0.0;
    iPlantState := 900; (* Enter controlled cooldown sequence *)
ELSE
    bThermalBypass := FALSE;
    bCriticalAlarm := FALSE;
END_IF;

(* Voltage degradation tracking & active trimming *)
(* As stack ages, nominal voltage drops; this compensates the fuel demand dynamically. *)
IF iPlantState = 40 THEN
    IF rFuelCellVoltage < 950.0 AND rFuelCellVoltage > 500.0 THEN
        rDegradationFactor := 950.0 / rFuelCellVoltage;
    ELSE
        rDegradationFactor := 1.0;
    END_IF;
END_IF;

(* === MAIN PLANT CONTROL STATE MACHINE === *)
CASE iPlantState OF
    0: (* OFF / STANDBY STATE *)
        bSystemReady := FALSE;
        rGasValveCmd := 0.0;
        rSteamValveCmd := 0.0;
        rStackCurrentRef := 0.0;
        IF bEnableSystem AND bEmergencyStop THEN
            iPlantState := 10;
        END_IF;

    10: (* COLD PURGE AND INITIAL WARMUP *)
        (* Prevent anode oxidation by displacing air with steam *)
        rSteamValveCmd := 30.0; 
        rGasValveCmd := 0.0;
        tWarmupTimer(IN := TRUE, PT := T#10M);
        IF tWarmupTimer.Q AND rStackTempAvg > 300.0 THEN
            tWarmupTimer(IN := FALSE);
            iPlantState := 20;
        END_IF;

    20: (* REFORMER LIGHT-OFF & THERMAL RAMP *)
        (* Gradually increase gas and steam maintaining minimum Steam-to-Carbon ratio > 2.5 *)
        rGasValveCmd := 10.0;
        rSteamValveCmd := 40.0;
        (* Wait until minimum operating temperature is reached before drawing current *)
        IF rStackTempAvg >= 750.0 THEN
            iPlantState := 30;
        END_IF;
        
    30: (* OPEN CIRCUIT VOLTAGE (OCV) VERIFICATION *)
        (* Confirm stack health via expected Nernst potential *)
        IF rFuelCellVoltage > 980.0 THEN
            bSystemReady := TRUE;
            iPlantState := 40;
        END_IF;

    40: (* STEADY-STATE POWER GENERATION *)
        (* 1. Fuel demand cascading control based on load and degradation *)
        rTargetGasFlow := rPowerDemandKW * 0.015 * rDegradationFactor;
        
        IF (rTargetGasFlow / 100.0) * 100.0 > 100.0 THEN
            rGasValveCmd := 100.0;
        ELSE
            IF (rTargetGasFlow / 100.0) * 100.0 < 0.0 THEN
                rGasValveCmd := 0.0;
            ELSE
                rGasValveCmd := (rTargetGasFlow / 100.0) * 100.0;
            END_IF;
        END_IF;
        
        (* 2. Steam mass flow regulation to prevent carbon coking *)
        (* Maintain nominal S/C ratio of 2.8 *)
        IF rGasValveCmd * 2.8 > 100.0 THEN
            rSteamValveCmd := 100.0;
        ELSE
            rSteamValveCmd := rGasValveCmd * 2.8;
        END_IF;
        
        (* 3. Inverter current reference derived from power equation (P = V*I) *)
        IF rFuelCellVoltage > 0.0 THEN
            rStackCurrentRef := (rPowerDemandKW * 1000.0) / rFuelCellVoltage; 
        END_IF;

        IF NOT bEnableSystem THEN
            iPlantState := 900; (* Operator requested shutdown *)
        END_IF;

    900: (* CONTROLLED COOLDOWN SEQUENCE *)
        rStackCurrentRef := 0.0;
        rGasValveCmd := 0.0;
        (* Maintain base steam flow to prevent oxidation during temp decay *)
        rSteamValveCmd := 20.0; 
        IF rStackTempAvg < 150.0 THEN
            iPlantState := 0;
        END_IF;

    999: (* FAULT LOCKOUT *)
        (* Waiting for manual reset via bEmergencyStop rising edge combined with toggle *)
        IF bEmergencyStop AND NOT bEnableSystem THEN
            iPlantState := 0;
            bCriticalAlarm := FALSE;
        END_IF;
        
END_CASE;

END_FUNCTION_BLOCK
```"""

record = {
    'messages': [
        {'role': 'user', 'content': prompt},
        {'role': 'assistant', 'content': code}
    ]
}

os.makedirs('data/swarm_raw', exist_ok=True)
filename = f'data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json'
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(record, f, ensure_ascii=False, indent=2)

print(f'Saved to {filename}')
