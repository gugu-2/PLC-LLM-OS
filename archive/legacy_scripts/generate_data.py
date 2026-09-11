import json, uuid, os

prompt = """<USER_REQUEST>
You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Industrial Scale Polymer Electrolyte Membrane (PEM) Electrolyzer Hydrogen Production**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., 20MW multi-stack current density active balancing, dynamic gas-liquid separator back-pressure cross-regulation, and rapid cold-start thermal transient mitigation). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\nFUNCTION_BLOCK FB_PEM_Electrolyzer\n//...\nEND_FUNCTION_BLOCK\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Industrial Scale Polymer Electrolyte Membrane (PEM) Electrolyzer Hydrogen Production

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT.
</USER_REQUEST>"""

code = """```iec-st
FUNCTION_BLOCK FB_PEM_Electrolyzer_Control
VAR_INPUT
    bSystemEnable           : BOOL;     (* Main system enable command *)
    bEmergencyStop          : BOOL;     (* E-Stop chain healthy (1 = OK) *)
    bGridInterlock          : BOOL;     (* Grid power quality interlock *)
    rTotalCurrentSetpoint   : REAL;     (* Requested total stack current (A) *)
    rStack1Current          : REAL;     (* Measured Stack 1 Current (A) *)
    rStack2Current          : REAL;     (* Measured Stack 2 Current (A) *)
    rStack1Voltage          : REAL;     (* Measured Stack 1 Voltage (V) *)
    rStack2Voltage          : REAL;     (* Measured Stack 2 Voltage (V) *)
    rCathodePressure        : REAL;     (* H2 Gas-Liquid separator pressure (bar) *)
    rAnodePressure          : REAL;     (* O2 Gas-Liquid separator pressure (bar) *)
    rStackTemperatureIn     : REAL;     (* Stack coolant inlet temperature (deg C) *)
    rStackTemperatureOut    : REAL;     (* Stack coolant outlet temperature (deg C) *)
    bPurgeComplete          : BOOL;     (* Nitrogen purge complete signal *)
END_VAR

VAR_OUTPUT
    bSystemReady            : BOOL;     (* System is ready for operation *)
    bHydrogenProducing      : BOOL;     (* System is in active production state *)
    bCriticalAlarm          : BOOL;     (* Critical fault detected, immediate shutdown *)
    iOperationState         : INT;      (* Current operating state machine step *)
    rStack1CurrentCmd       : REAL;     (* Commanded current for Stack 1 Rectifier (A) *)
    rStack2CurrentCmd       : REAL;     (* Commanded current for Stack 2 Rectifier (A) *)
    rCathodePressureValveCmd: REAL;     (* Back-pressure control valve command H2 side (0-100%) *)
    rCoolantPumpSpeedCmd    : REAL;     (* Coolant pump variable speed drive command (0-100%) *)
    rTotalH2Production      : REAL;     (* Estimated H2 production rate (kg/h) *)
END_VAR

VAR
    (* Internal State Variables *)
    iState                  : INT := 0; (* 0: IDLE, 10: PURGE, 20: STANDBY, 30: STARTUP, 40: RUN, 99: FAULT *)
    tStartupTimer           : TON;
    tPurgeTimer             : TON;
    tFaultDelay             : TON;
    
    (* Filtering and Processing *)
    rFiltCathodePress       : REAL := 0.0;
    rFiltAnodePress         : REAL := 0.0;
    rFiltTempOut            : REAL := 0.0;
    rAlphaPress             : REAL := 0.1; (* Low pass filter coefficient for pressure *)
    rAlphaTemp              : REAL := 0.05;(* Low pass filter coefficient for temperature *)
    
    (* Control Variables *)
    rPressureDiff           : REAL;
    rTargetTemperature      : REAL := 65.0; (* Optimal PEM operating temp *)
    rTempError              : REAL;
    
    (* Constants *)
    rFARADAY_CONST          : REAL := 96485.33; 
    rMOLAR_MASS_H2          : REAL := 2.016;
END_VAR

(* === MAIN LOGIC === *)

(* Safety and Interlock Processing *)
IF NOT bEmergencyStop OR NOT bGridInterlock THEN
    iState := 99; (* Force immediate fault state *)
END_IF;

(* Sensor Noise Filtering (First-order IIR low-pass filter) *)
rFiltCathodePress := rFiltCathodePress + rAlphaPress * (rCathodePressure - rFiltCathodePress);
rFiltAnodePress   := rFiltAnodePress + rAlphaPress * (rAnodePressure - rFiltAnodePress);
rFiltTempOut      := rFiltTempOut + rAlphaTemp * (rStackTemperatureOut - rFiltTempOut);

(* Pressure Differential Monitoring *)
rPressureDiff := ABS(rFiltCathodePress - rFiltAnodePress);

CASE iState OF
    0: (* IDLE STATE *)
        bSystemReady := FALSE;
        bHydrogenProducing := FALSE;
        bCriticalAlarm := FALSE;
        rStack1CurrentCmd := 0.0;
        rStack2CurrentCmd := 0.0;
        rCathodePressureValveCmd := 0.0;
        rCoolantPumpSpeedCmd := 0.0;
        
        IF bSystemEnable AND bEmergencyStop AND bGridInterlock THEN
            iState := 10; (* Transition to PURGE *)
        END_IF;

    10: (* PURGE STATE - N2 sweeping lines *)
        tPurgeTimer(IN := TRUE, PT := T#30S);
        IF bPurgeComplete AND tPurgeTimer.Q THEN
            tPurgeTimer(IN := FALSE);
            iState := 20; (* Transition to STANDBY *)
        ELSIF NOT bSystemEnable THEN
            tPurgeTimer(IN := FALSE);
            iState := 0;
        END_IF;

    20: (* STANDBY STATE - System Ready *)
        bSystemReady := TRUE;
        
        IF bSystemEnable AND (rTotalCurrentSetpoint > 0.0) THEN
            iState := 30; (* Transition to STARTUP *)
        ELSIF NOT bSystemEnable THEN
            iState := 0;
        END_IF;

    30: (* STARTUP STATE - Thermal Transient Mitigation *)
        (* Bring up coolant circulation slowly *)
        rCoolantPumpSpeedCmd := 25.0; 
        
        tStartupTimer(IN := TRUE, PT := T#15S);
        IF tStartupTimer.Q THEN
            tStartupTimer(IN := FALSE);
            iState := 40; (* Transition to RUN *)
        END_IF;

    40: (* RUN STATE - Active Production *)
        bSystemReady := TRUE;
        bHydrogenProducing := TRUE;
        
        (* 1. Active Current Density Balancing (20MW Multi-Stack) *)
        (* Distribute total current equally, but adjust based on stack voltage health *)
        IF rStack1Voltage > 0.0 AND rStack2Voltage > 0.0 THEN
            rStack1CurrentCmd := (rTotalCurrentSetpoint / 2.0) * (rStack2Voltage / rStack1Voltage);
            rStack2CurrentCmd := (rTotalCurrentSetpoint / 2.0) * (rStack1Voltage / rStack2Voltage);
        ELSE
            rStack1CurrentCmd := rTotalCurrentSetpoint / 2.0;
            rStack2CurrentCmd := rTotalCurrentSetpoint / 2.0;
        END_IF;
        
        (* Limit checking to prevent individual stack overload (Assuming 10kA max per stack) *)
        IF rStack1CurrentCmd > 10000.0 THEN rStack1CurrentCmd := 10000.0; END_IF;
        IF rStack2CurrentCmd > 10000.0 THEN rStack2CurrentCmd := 10000.0; END_IF;

        (* 2. Dynamic Gas-Liquid Separator Back-Pressure Cross-Regulation *)
        (* Target is to keep cathode (H2) pressure slightly above anode (O2) pressure (e.g., 0.2 bar diff) *)
        IF (rFiltCathodePress - rFiltAnodePress) < 0.2 THEN
            rCathodePressureValveCmd := rCathodePressureValveCmd - 1.0; (* Close valve slightly to build pressure *)
        ELSIF (rFiltCathodePress - rFiltAnodePress) > 0.4 THEN
            rCathodePressureValveCmd := rCathodePressureValveCmd + 1.0; (* Open valve slightly to relieve pressure *)
        END_IF;
        
        (* Valve command clamping *)
        IF rCathodePressureValveCmd > 100.0 THEN rCathodePressureValveCmd := 100.0; END_IF;
        IF rCathodePressureValveCmd < 0.0 THEN rCathodePressureValveCmd := 0.0; END_IF;

        (* 3. Thermal Management (PI-like action for pump speed) *)
        rTempError := rFiltTempOut - rTargetTemperature;
        rCoolantPumpSpeedCmd := 50.0 + (rTempError * 5.0);
        IF rCoolantPumpSpeedCmd > 100.0 THEN rCoolantPumpSpeedCmd := 100.0; END_IF;
        IF rCoolantPumpSpeedCmd < 20.0 THEN rCoolantPumpSpeedCmd := 20.0; END_IF;

        (* Fault Detection during RUN *)
        IF rPressureDiff > 2.0 OR rFiltTempOut > 85.0 THEN
            tFaultDelay(IN := TRUE, PT := T#2S);
            IF tFaultDelay.Q THEN
                iState := 99;
            END_IF;
        ELSE
            tFaultDelay(IN := FALSE);
        END_IF;
        
        IF NOT bSystemEnable OR (rTotalCurrentSetpoint <= 0.0) THEN
            iState := 20; (* Return to STANDBY *)
            bHydrogenProducing := FALSE;
        END_IF;

    99: (* FAULT STATE - Critical shutdown *)
        bSystemReady := FALSE;
        bHydrogenProducing := FALSE;
        bCriticalAlarm := TRUE;
        rStack1CurrentCmd := 0.0;
        rStack2CurrentCmd := 0.0;
        rCathodePressureValveCmd := 100.0; (* Fail-safe open *)
        rCoolantPumpSpeedCmd := 100.0; (* Max cooling during fault *)
        tPurgeTimer(IN := FALSE);
        tStartupTimer(IN := FALSE);
        tFaultDelay(IN := FALSE);
        
        IF NOT bEmergencyStop AND NOT bGridInterlock AND NOT bSystemEnable THEN
            (* Acknowledge fault only when enable is dropped and safeties are clear *)
            iState := 0;
        END_IF;

END_CASE;

(* Faradaic Hydrogen Production Calculation *)
IF bHydrogenProducing THEN
    (* Rate (kg/h) = (Total Current (A) * Cells * Molar Mass (kg/kmol)) / (z * Faraday Constant (C/mol)) * 3600 *)
    (* Assuming 200 cells per stack, z=2 for H2 *)
    rTotalH2Production := ((rStack1Current + rStack2Current) * 200.0 * (rMOLAR_MASS_H2 / 1000.0) * 3600.0) / (2.0 * rFARADAY_CONST);
ELSE
    rTotalH2Production := 0.0;
END_IF;

iOperationState := iState;

END_FUNCTION_BLOCK
```"""

os.makedirs('data/swarm_raw', exist_ok=True)
filename = f'data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json'
record = {'messages': [{'role': 'user', 'content': prompt}, {'role': 'assistant', 'content': code}]}
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(record, f, ensure_ascii=False)
print(f'Saved to {filename}')
