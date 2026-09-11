import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Utility-Scale Liquid Metal Battery (LMB) Grid Storage**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., 400°C isothermal multi-cell voltage balancing, rapid charge/discharge thermal mass dissipation, and liquid metal interfacial wave suppression). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_LMB_GridStorage\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Utility-Scale Liquid Metal Battery (LMB) Grid Storage

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_LMB_GridStorage
(* 
   Utility-Scale Liquid Metal Battery (LMB) Grid Storage Controller
   Advanced control for 400°C isothermal multi-cell voltage balancing, rapid charge/discharge
   thermal mass dissipation, and liquid metal interfacial wave suppression.
*)
VAR_INPUT
    bSystemEnable       : BOOL;     (* Main grid-scale system enable command *)
    bEmergencyStop      : BOOL;     (* Multi-layer hardware safety relay OK signal *)
    rCellVoltage        : REAL;     (* Aggregate or min/max cell voltage measurement [V] *)
    rOperatingTemp      : REAL;     (* LMB operating temperature measurement [°C] *)
    rGridDemandKW       : REAL;     (* Current grid charge/discharge demand [kW] *)
    rVibrationSensor    : REAL;     (* Accelerometer data for interfacial wave detection [m/s2] *)
END_VAR

VAR_OUTPUT
    bSystemReady        : BOOL;     (* System is operational and at nominal temperature *)
    rInverterSetPoint   : REAL;     (* Output charge/discharge command to bi-directional inverter [kW] *)
    rHeaterControl      : REAL;     (* PID command for internal cell heaters (0-100%) *)
    bAlarm              : BOOL;     (* Critical fault alarm output (e.g. overtemp, voltage drop) *)
    iOperatingState     : INT;      (* Current internal state machine status code *)
END_VAR

VAR
    iState              : INT := 0;
    tInitDelay          : TON;
    tSafetyTimer        : TON;
    rFilteredTemp       : REAL := 0.0;
    rFilteredVolt       : REAL := 0.0;
    rIntegralErrorTemp  : REAL := 0.0;
    rErrorTemp          : REAL := 0.0;
    
    (* Filter Constants *)
    ALPHA_TEMP          : REAL := 0.05;
    ALPHA_VOLT          : REAL := 0.10;
    
    (* PID Constants for Temperature Control *)
    KP_TEMP             : REAL := 2.5;
    KI_TEMP             : REAL := 0.02;
    TEMP_SETPOINT       : REAL := 400.0;
    
    (* Operational Limits *)
    TEMP_MAX            : REAL := 450.0;
    TEMP_MIN            : REAL := 380.0;
    VOLTAGE_MIN         : REAL := 0.8;
    VOLTAGE_MAX         : REAL := 1.25;
    WAVE_THRESHOLD      : REAL := 1.5; (* max allowable vibration [m/s2] *)
END_VAR

(* === MAIN LOGIC === *)
(* Multilayer Safety Interlock Check *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bAlarm := TRUE;
    rInverterSetPoint := 0.0;
    rHeaterControl := 0.0;
    iState := 99; (* FAULT STATE *)
    iOperatingState := iState;
    RETURN;
END_IF;

(* Sensor Noise Filtering (Exponential Moving Average) *)
rFilteredTemp := (ALPHA_TEMP * rOperatingTemp) + ((1.0 - ALPHA_TEMP) * rFilteredTemp);
rFilteredVolt := (ALPHA_VOLT * rCellVoltage) + ((1.0 - ALPHA_VOLT) * rFilteredVolt);

(* Continuous Hardware Protections *)
IF (rFilteredTemp > TEMP_MAX) OR (rFilteredVolt < VOLTAGE_MIN) OR (rFilteredVolt > VOLTAGE_MAX) THEN
    bSystemReady := FALSE;
    bAlarm := TRUE;
    rInverterSetPoint := 0.0;
    rHeaterControl := 0.0;
    iState := 99;
    iOperatingState := iState;
    RETURN;
END_IF;

(* Interfacial Wave Suppression Logic - Reduces power if sloshing/waves detected *)
IF rVibrationSensor > WAVE_THRESHOLD THEN
    (* Derate grid demand temporarily to allow waves to settle *)
    rGridDemandKW := rGridDemandKW * 0.5;
END_IF;

(* Primary State Machine *)
CASE iState OF
    0: (* IDLE & PRE-HEAT *)
        bSystemReady := FALSE;
        bAlarm := FALSE;
        rInverterSetPoint := 0.0;
        
        (* Thermal PID Loop - Pre-heating phase *)
        rErrorTemp := TEMP_SETPOINT - rFilteredTemp;
        rIntegralErrorTemp := rIntegralErrorTemp + (rErrorTemp * 0.1); (* Assuming 100ms cycle *)
        rHeaterControl := (KP_TEMP * rErrorTemp) + (KI_TEMP * rIntegralErrorTemp);
        
        IF rHeaterControl > 100.0 THEN
            rHeaterControl := 100.0;
        ELSIF rHeaterControl < 0.0 THEN
            rHeaterControl := 0.0;
        END_IF;
        
        IF bSystemEnable AND (rFilteredTemp >= TEMP_MIN) THEN
            tInitDelay(IN := TRUE, PT := T#10S);
            IF tInitDelay.Q THEN
                tInitDelay(IN := FALSE);
                iState := 10;
            END_IF;
        ELSE
            tInitDelay(IN := FALSE);
        END_IF;

    10: (* ACTIVE / RUNNING *)
        bSystemReady := TRUE;
        bAlarm := FALSE;
        
        (* Active Thermal Management - Heating during idle, but cooling / passive during heavy discharge *)
        rErrorTemp := TEMP_SETPOINT - rFilteredTemp;
        rIntegralErrorTemp := rIntegralErrorTemp + (rErrorTemp * 0.1);
        rHeaterControl := (KP_TEMP * rErrorTemp) + (KI_TEMP * rIntegralErrorTemp);
        
        IF rHeaterControl > 100.0 THEN rHeaterControl := 100.0; END_IF;
        IF rHeaterControl < 0.0 THEN rHeaterControl := 0.0; END_IF;
        
        (* Load following mode with self-heating factor estimation *)
        rInverterSetPoint := rGridDemandKW;
        
        IF NOT bSystemEnable THEN
            iState := 0;
        END_IF;

    99: (* FAULT HANDLING *)
        bSystemReady := FALSE;
        bAlarm := TRUE;
        rInverterSetPoint := 0.0;
        rHeaterControl := 0.0;
        tSafetyTimer(IN := TRUE, PT := T#5S);
        IF tSafetyTimer.Q AND bEmergencyStop AND (rFilteredTemp <= TEMP_MAX) THEN
            (* Manual reset could be required, but auto-recover if conditions clear *)
            tSafetyTimer(IN := FALSE);
            iState := 0;
        END_IF;
        
END_CASE;

iOperatingState := iState;

END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
print(f"Saved to {filename}")
