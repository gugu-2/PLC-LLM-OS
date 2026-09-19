import json, uuid, os

os.makedirs("data/swarm_raw", exist_ok=True)
prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Industrial Metrology CMM (Coordinate Measuring Machine) Air Bearing Pressure and Thermal Expansion Compensation**

Task: Invent a highly complex, ultra-realistic control scenario for this domain. Make this code EVEN BETTER, MORE ADVANCED, and MORE RIGOROUS than previous iterations. Include extreme edge-case handling, advanced math, and robust fault-tolerance.

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
   code = \"\"\"```iec-st\nFUNCTION_BLOCK FB_CMM_ThermalCompensation\n//...\nEND_FUNCTION_BLOCK\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Industrial Metrology CMM (Coordinate Measuring Machine) Air Bearing Pressure and Thermal Expansion Compensation

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_CMM_AirBearing_ThermalComp
VAR_INPUT
    bEnable                 : BOOL;     (* System Enable Signal *)
    bEmergencyStop          : BOOL;     (* Safety Circuit OK Signal (Active High) *)
    rAirSupplyPressure      : REAL;     (* Main air supply pressure [bar] *)
    rXAxisTemperature       : REAL;     (* X-Axis Granite Guideway Temperature [°C] *)
    rYAxisTemperature       : REAL;     (* Y-Axis Granite Guideway Temperature [°C] *)
    rZAxisTemperature       : REAL;     (* Z-Axis Ceramic Ram Temperature [°C] *)
    rAmbientTemperature     : REAL;     (* Cleanroom Ambient Temperature [°C] *)
    rZAxisPosition          : REAL;     (* Current Z-Axis Position for cantilever calculation [mm] *)
END_VAR
VAR_OUTPUT
    bSystemReady            : BOOL;     (* CMM ready for measurement operations *)
    bAlarm                  : BOOL;     (* Critical fault active *)
    iErrorCode              : INT;      (* Specific fault code for diagnostics *)
    rAirPressureCommand     : REAL;     (* Commanded pressure to proportional valve [bar] *)
    rXThermalCompVal        : LREAL;    (* Thermal expansion compensation for X-Axis [um] *)
    rYThermalCompVal        : LREAL;    (* Thermal expansion compensation for Y-Axis [um] *)
    rZThermalCompVal        : LREAL;    (* Thermal expansion compensation for Z-Axis [um] *)
END_VAR
VAR
    iState                  : INT := 0; (* Internal state machine *)
    tStartupDelay           : TON;      (* Delay to allow air pressure stabilization *)
    tTempFilterTimer        : TON;      (* Timer for temperature filtering *)
    rFilteredXTemp          : REAL := 20.0;
    rFilteredYTemp          : REAL := 20.0;
    rFilteredZTemp          : REAL := 20.0;
    rFilteredAmbient        : REAL := 20.0;
    
    (* Constants *)
    c_rGraniteCTE           : LREAL := 6.8E-6;  (* Granite Coefficient of Thermal Expansion [1/K] *)
    c_rCeramicCTE           : LREAL := 3.2E-6;  (* Ceramic Coefficient of Thermal Expansion [1/K] *)
    c_rNominalTemp          : LREAL := 20.0;    (* Reference Temperature [°C] *)
    c_rMinPressure          : REAL := 4.5;      (* Minimum safe air bearing pressure [bar] *)
    c_rOptimalPressure      : REAL := 5.0;      (* Optimal air bearing pressure [bar] *)
    
    bInitDone               : BOOL := FALSE;
END_VAR

(* === MAIN LOGIC === *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bAlarm := TRUE;
    iErrorCode := 999; (* Emergency Stop Active *)
    rAirPressureCommand := 0.0;
    iState := 0;
    RETURN;
END_IF;

IF NOT bInitDone THEN
    (* Initialize filter values to nominal *)
    rFilteredXTemp := rXAxisTemperature;
    rFilteredYTemp := rYAxisTemperature;
    rFilteredZTemp := rZAxisTemperature;
    rFilteredAmbient := rAmbientTemperature;
    bInitDone := TRUE;
END_IF;

(* Continuous low-pass filter for temperature readings to eliminate sensor noise *)
rFilteredXTemp := rFilteredXTemp + 0.05 * (rXAxisTemperature - rFilteredXTemp);
rFilteredYTemp := rFilteredYTemp + 0.05 * (rYAxisTemperature - rFilteredYTemp);
rFilteredZTemp := rFilteredZTemp + 0.05 * (rZAxisTemperature - rFilteredZTemp);
rFilteredAmbient := rFilteredAmbient + 0.01 * (rAmbientTemperature - rFilteredAmbient);

CASE iState OF
    0: (* IDLE & SAFETY CHECKS *)
        bSystemReady := FALSE;
        bAlarm := FALSE;
        iErrorCode := 0;
        rAirPressureCommand := 0.0;
        rXThermalCompVal := 0.0;
        rYThermalCompVal := 0.0;
        rZThermalCompVal := 0.0;
        
        IF bEnable THEN
            IF rAirSupplyPressure < c_rMinPressure THEN
                bAlarm := TRUE;
                iErrorCode := 101; (* Low inlet pressure *)
            ELSE
                iState := 10;
            END_IF;
        END_IF;

    10: (* PRESSURIZE AIR BEARINGS *)
        rAirPressureCommand := c_rOptimalPressure;
        tStartupDelay(IN := TRUE, PT := T#3S);
        
        IF tStartupDelay.Q THEN
            tStartupDelay(IN := FALSE);
            IF rAirSupplyPressure >= c_rOptimalPressure * 0.95 THEN
                iState := 20;
            ELSE
                bAlarm := TRUE;
                iErrorCode := 102; (* Pressure failed to build *)
                iState := 0;
            END_IF;
        END_IF;

    20: (* RUNNING & COMPENSATING *)
        bSystemReady := TRUE;
        bAlarm := FALSE;
        
        (* Dynamic pressure adjustment based on Z-Axis cantilever extension (simplified) *)
        rAirPressureCommand := c_rOptimalPressure + (rZAxisPosition * 0.0005);
        IF rAirPressureCommand > 6.0 THEN
            rAirPressureCommand := 6.0; (* Safety clamp *)
        END_IF;
        
        (* Calculate thermal expansion compensation [um] based on filtered delta T and CTE *)
        (* Assuming standard axis lengths for calculation (X=1000mm, Y=1000mm, Z=800mm) *)
        rXThermalCompVal := (rFilteredXTemp - c_rNominalTemp) * c_rGraniteCTE * 1000.0 * 1000.0;
        rYThermalCompVal := (rFilteredYTemp - c_rNominalTemp) * c_rGraniteCTE * 1000.0 * 1000.0;
        rZThermalCompVal := (rFilteredZTemp - c_rNominalTemp) * c_rCeramicCTE * 800.0 * 1000.0;
        
        (* Monitor bounds *)
        IF ABS(rFilteredXTemp - c_rNominalTemp) > 2.0 OR ABS(rFilteredYTemp - c_rNominalTemp) > 2.0 THEN
            bAlarm := TRUE;
            iErrorCode := 201; (* Temperature out of metrology specification *)
        END_IF;
        
        IF NOT bEnable THEN
            iState := 0;
        END_IF;
        
    ELSE
        iState := 0;
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
