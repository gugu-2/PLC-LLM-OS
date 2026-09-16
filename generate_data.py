import os
import json, uuid

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Commercial Data Center Hot Aisle Containment CRAC Airflow Balancing**

Task: Invent a highly complex, ultra-realistic control scenario for this domain. Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_DataCenter_CRAC_Balancing\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Commercial Data Center Hot Aisle Containment CRAC Airflow Balancing

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_DataCenter_CRAC_Balancing
VAR_INPUT
    bSystemEnable       : BOOL;     (* System master enable signal *)
    bEmergencyStop      : BOOL;     (* Safety loop OK - 0 = E-Stop active *)
    rHotAisleTemp       : REAL;     (* Current hot aisle temperature [degC] *)
    rColdAisleTemp      : REAL;     (* Current cold aisle temperature [degC] *)
    rDifferentialPress  : REAL;     (* Pressure diff between aisles [Pa] *)
    rSupplyAirTemp      : REAL;     (* CRAC supply air temp [degC] *)
    rReturnAirTemp      : REAL;     (* CRAC return air temp [degC] *)
    rExternalAmbientTemp: REAL;     (* External ambient temp for free cooling check [degC] *)
END_VAR
VAR_OUTPUT
    bSystemReady        : BOOL;     (* Control system is ready for operation *)
    rFanSpeedSetpoint   : REAL;     (* CRAC EC Fan speed command [0-100%] *)
    rChilledWaterValve  : REAL;     (* CW Valve position command [0-100%] *)
    bWarningAlarm       : BOOL;     (* Warning: approaching limits *)
    bCriticalAlarm      : BOOL;     (* Critical: limits exceeded, possible thermal runaway *)
    bFreeCoolingActive  : BOOL;     (* Indication that economizer/free cooling is active *)
END_VAR
VAR
    iState              : INT := 0; (* State machine step *)
    tStartupDelay       : TON;      (* Prevent rapid cycling *)
    tEStopDelay         : TOF;      (* Debounce E-Stop recovery *)
    
    (* Filter variables *)
    rFilteredDP         : REAL;
    rFilteredHAT        : REAL;
    
    (* PID Variables for Pressure *)
    rDP_SetPoint        : REAL := 12.5; (* Target DP in Pa *)
    rDP_Error           : REAL;
    rDP_Integral        : REAL;
    rDP_Derivative      : REAL;
    rDP_LastError       : REAL;
    rKp_DP              : REAL := 2.5;
    rKi_DP              : REAL := 0.15;
    rKd_DP              : REAL := 0.5;
    
    (* PID Variables for Temperature *)
    rTemp_SetPoint      : REAL := 24.0; (* Target cold aisle temp in degC *)
    rTemp_Error         : REAL;
    rTemp_Integral      : REAL;
    rTemp_Derivative    : REAL;
    rTemp_LastError     : REAL;
    rKp_T               : REAL := 5.0;
    rKi_T               : REAL := 0.25;
    rKd_T               : REAL := 1.0;
    
    (* Internal Status *)
    bInitDone           : BOOL := FALSE;
    bThermalsSafe       : BOOL := FALSE;
END_VAR

(* === MAIN LOGIC === *)
(* 1. Safety and Interlocks *)
IF NOT bEmergencyStop THEN
    iState := 999; (* Fault state *)
    bSystemReady := FALSE;
    rFanSpeedSetpoint := 100.0; (* Fail safe: max airflow to prevent hot spots *)
    rChilledWaterValve := 100.0; (* Fail safe: max cooling *)
    bCriticalAlarm := TRUE;
    bWarningAlarm := TRUE;
    rDP_Integral := 0.0;
    rTemp_Integral := 0.0;
    RETURN;
END_IF;

(* 2. Initialization *)
IF NOT bInitDone THEN
    rFilteredDP := rDifferentialPress;
    rFilteredHAT := rHotAisleTemp;
    rDP_LastError := 0.0;
    rTemp_LastError := 0.0;
    bInitDone := TRUE;
    iState := 0;
END_IF;

(* 3. Signal Filtering (Exponential Moving Average) *)
rFilteredDP := (rFilteredDP * 0.9) + (rDifferentialPress * 0.1);
rFilteredHAT := (rFilteredHAT * 0.85) + (rHotAisleTemp * 0.15);

(* 4. Thermal Safety Checks *)
IF (rFilteredHAT > 35.0) OR (rColdAisleTemp > 28.0) THEN
    bCriticalAlarm := TRUE;
    bThermalsSafe := FALSE;
ELSE
    bCriticalAlarm := FALSE;
    bThermalsSafe := TRUE;
END_IF;

IF (rFilteredHAT > 32.0) OR (rColdAisleTemp > 26.0) THEN
    bWarningAlarm := TRUE;
ELSE
    bWarningAlarm := FALSE;
END_IF;

(* 5. State Machine Control *)
CASE iState OF
    0: (* IDLE *)
        bSystemReady := FALSE;
        rFanSpeedSetpoint := 0.0;
        rChilledWaterValve := 0.0;
        bFreeCoolingActive := FALSE;
        
        IF bSystemEnable AND bThermalsSafe THEN
            iState := 10;
        END_IF;
        
    10: (* STARTING *)
        tStartupDelay(IN := TRUE, PT := T#15S);
        IF tStartupDelay.Q THEN
            bSystemReady := TRUE;
            iState := 20;
            tStartupDelay(IN := FALSE);
        END_IF;
        
    20: (* RUNNING - ACTIVE BALANCING *)
        IF NOT bSystemEnable THEN
            iState := 0;
        END_IF;
        
        (* Cascade / Dual PID Logic for Balancing *)
        (* Calculate Pressure Error for Fan Speed *)
        rDP_Error := rDP_SetPoint - rFilteredDP;
        rDP_Integral := rDP_Integral + (rDP_Error * 0.1); (* Assuming 100ms cycle *)
        
        (* Anti-windup for Fan PID *)
        IF rDP_Integral > 100.0 THEN rDP_Integral := 100.0; END_IF;
        IF rDP_Integral < -50.0 THEN rDP_Integral := -50.0; END_IF;
        
        rDP_Derivative := (rDP_Error - rDP_LastError) / 0.1;
        rDP_LastError := rDP_Error;
        
        rFanSpeedSetpoint := (rKp_DP * rDP_Error) + (rKi_DP * rDP_Integral) + (rKd_DP * rDP_Derivative);
        
        (* Clamp Fan Speed *)
        IF rFanSpeedSetpoint > 100.0 THEN rFanSpeedSetpoint := 100.0; END_IF;
        IF rFanSpeedSetpoint < 20.0 THEN rFanSpeedSetpoint := 20.0; END_IF; (* Minimum fan speed to maintain static pressure *)
        
        (* Calculate Temperature Error for Chilled Water Valve *)
        rTemp_Error := rFilteredHAT - rTemp_SetPoint;
        rTemp_Integral := rTemp_Integral + (rTemp_Error * 0.1);
        
        (* Anti-windup for Valve PID *)
        IF rTemp_Integral > 100.0 THEN rTemp_Integral := 100.0; END_IF;
        IF rTemp_Integral < 0.0 THEN rTemp_Integral := 0.0; END_IF;
        
        rTemp_Derivative := (rTemp_Error - rTemp_LastError) / 0.1;
        rTemp_LastError := rTemp_Error;
        
        rChilledWaterValve := (rKp_T * rTemp_Error) + (rKi_T * rTemp_Integral) + (rKd_T * rTemp_Derivative);
        
        (* Clamp Valve Position *)
        IF rChilledWaterValve > 100.0 THEN rChilledWaterValve := 100.0; END_IF;
        IF rChilledWaterValve < 0.0 THEN rChilledWaterValve := 0.0; END_IF;
        
        (* Economizer / Free Cooling Evaluation *)
        IF (rExternalAmbientTemp < 15.0) AND (rChilledWaterValve > 50.0) THEN
            bFreeCoolingActive := TRUE;
            (* Adjust PID tuning for free cooling dynamics if needed *)
        ELSE
            bFreeCoolingActive := FALSE;
        END_IF;

    999: (* FAULT STATE *)
        IF bEmergencyStop AND bThermalsSafe AND NOT bSystemEnable THEN
            (* Wait for operator to clear enable signal and safe condition before reset *)
            iState := 0;
        END_IF;

END_CASE;

END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
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
