import os, json, uuid

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Industrial Scale Biomass Gasification Fluidized Bed Reactor**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., High-temperature steam-oxygen blow continuous fluidization velocity mapping, bed agglomeration acoustic emission prevention, and synthetic gas (syngas) calorific value forward-feed trimming). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_Biomass_FluidizedBedReactor\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Industrial Scale Biomass Gasification Fluidized Bed Reactor

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_Biomass_FluidizedBedReactor
VAR_INPUT
    (* Required physical inputs *)
    bEnable                 : BOOL;     (* System master enable signal *)
    bEmergencyStop          : BOOL;     (* Safety relay OK signal (active high) *)
    rBedTemperature         : REAL;     (* Reactor bed temperature [deg C] *)
    rAcousticEmissionLevel  : REAL;     (* Bed agglomeration acoustic signature [mV] *)
    rSyngasCalorificValue   : REAL;     (* Online gas analyzer CV reading [MJ/Nm3] *)
    rFeedRate               : REAL;     (* Biomass screw conveyor feed rate [kg/hr] *)
    rFluidizationAirFlow    : REAL;     (* Measured fluidization air flow [Nm3/hr] *)
    rSteamInjectionRate     : REAL;     (* High-temp steam injection flow [kg/hr] *)
END_VAR
VAR_OUTPUT
    (* Required outputs *)
    bSystemReady            : BOOL;     (* System ready for operation *)
    rTargetAirFlow          : REAL;     (* Modulated setpoint for fluidization blower [Nm3/hr] *)
    rTargetSteamFlow        : REAL;     (* Modulated setpoint for steam control valve [kg/hr] *)
    bAgglomerationAlarm     : BOOL;     (* Alarm triggered by high acoustic emission *)
    bShutdownInterlock      : BOOL;     (* Hardware interlock trip command *)
    rPredictedCV            : REAL;     (* Feed-forward predicted calorific value [MJ/Nm3] *)
END_VAR
VAR
    (* Internal State and Timers *)
    iState                  : INT := 0; (* State machine step *)
    tStartupTimer           : TON;
    tSafetyDelay            : TON;
    
    (* Filtered Variables *)
    rFilteredAcoustic       : REAL := 0.0;
    rFilteredTemp           : REAL := 0.0;
    
    (* Constants *)
    c_rAcousticLimit        : REAL := 75.0; (* Limit for agglomeration risk *)
    c_rBedTempOptimal       : REAL := 850.0;
    
    (* PID internal approximations *)
    rErrorTemp              : REAL := 0.0;
    rIntegralTemp           : REAL := 0.0;
END_VAR

(* === MAIN LOGIC === *)

(* Multi-layered safety interlocks *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bShutdownInterlock := TRUE;
    rTargetAirFlow := 0.0;
    rTargetSteamFlow := 0.0;
    bAgglomerationAlarm := FALSE;
    iState := 999; (* FAULT STATE *)
    RETURN;
END_IF;

(* Sensor noise filtering (First-order low-pass) *)
rFilteredAcoustic := rFilteredAcoustic + 0.1 * (rAcousticEmissionLevel - rFilteredAcoustic);
rFilteredTemp := rFilteredTemp + 0.05 * (rBedTemperature - rFilteredTemp);

(* Acoustic emission check for bed agglomeration prevention *)
IF rFilteredAcoustic > c_rAcousticLimit THEN
    bAgglomerationAlarm := TRUE;
ELSE
    bAgglomerationAlarm := FALSE;
END_IF;

(* Main State Machine *)
CASE iState OF
    0: (* IDLE *)
        bSystemReady := FALSE;
        rTargetAirFlow := 0.0;
        rTargetSteamFlow := 0.0;
        IF bEnable AND NOT bShutdownInterlock THEN
            iState := 10;
        END_IF;

    10: (* PURGE AND PRE-HEAT *)
        rTargetAirFlow := 500.0; (* Purge flow rate *)
        tStartupTimer(IN := TRUE, PT := T#30S);
        IF tStartupTimer.Q THEN
            tStartupTimer(IN := FALSE);
            iState := 20;
        END_IF;
        
    20: (* RAMP TO OPTIMAL TEMPERATURE *)
        rTargetAirFlow := 1000.0 + rFeedRate * 1.2;
        IF rFilteredTemp >= c_rBedTempOptimal * 0.9 THEN
            iState := 30;
            bSystemReady := TRUE;
        END_IF;
        (* Safety fallback *)
        IF bAgglomerationAlarm THEN
            iState := 999;
        END_IF;
        
    30: (* CONTINUOUS GASIFICATION CONTROL LOOP *)
        (* Forward-feed trimming for syngas CV *)
        rPredictedCV := rSyngasCalorificValue * 0.8 + (rFeedRate / (rFluidizationAirFlow + 1.0)) * 2.0;
        
        (* Bed Temp PI Control Approximation *)
        rErrorTemp := c_rBedTempOptimal - rFilteredTemp;
        rIntegralTemp := rIntegralTemp + rErrorTemp * 0.01;
        
        rTargetSteamFlow := 200.0 + (rErrorTemp * 1.5) + rIntegralTemp;
        
        (* Bounds checking *)
        IF rTargetSteamFlow < 0.0 THEN
            rTargetSteamFlow := 0.0;
        END_IF;
        
        IF NOT bEnable OR bAgglomerationAlarm THEN
            iState := 0; 
            IF bAgglomerationAlarm THEN
                iState := 999;
            END_IF;
        END_IF;
        
    999: (* FAULT HANDLING *)
        bSystemReady := FALSE;
        rTargetAirFlow := 200.0; (* Minimal safe cooling flow *)
        rTargetSteamFlow := 0.0;
        tSafetyDelay(IN := TRUE, PT := T#60S);
        IF NOT bAgglomerationAlarm AND NOT bShutdownInterlock AND tSafetyDelay.Q THEN
            tSafetyDelay(IN := FALSE);
            IF NOT bEnable THEN
                iState := 0;
            END_IF;
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
