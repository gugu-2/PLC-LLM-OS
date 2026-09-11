import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Utility-Scale Commercial Ocean Thermal Energy Conversion (OTEC) Ammonia Turbine**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Deep seawater cold water pipe (CWP) upwelling flow balancing, closed-cycle ammonia evaporation/condensation pressure mapping, and multi-megawatt axial turbine over-speed protection). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_OTEC_AmmoniaTurbine\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Utility-Scale Commercial Ocean Thermal Energy Conversion (OTEC) Ammonia Turbine

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_OTEC_AmmoniaTurbine
VAR_INPUT
    bEnable                 : BOOL;     (* System master enable signal *)
    bEmergencyStop          : BOOL;     (* Safety circuit OK, TRUE = healthy *)
    rWarmSeawaterTemp       : REAL;     (* Warm seawater intake temperature [deg C] *)
    rColdSeawaterTemp       : REAL;     (* Cold seawater intake temperature [deg C] *)
    rAmmoniaPressureEvap    : REAL;     (* Evaporator ammonia pressure [bar] *)
    rAmmoniaPressureCond    : REAL;     (* Condenser ammonia pressure [bar] *)
    rTurbineSpeedRPM        : REAL;     (* Main axial turbine speed [RPM] *)
    rGridFrequency          : REAL;     (* Power grid frequency [Hz] *)
END_VAR
VAR_OUTPUT
    bSystemReady            : BOOL;     (* System ready for grid synchronization *)
    rAmmoniaFlowDemand      : REAL;     (* Demand signal to ammonia feed pump [%] *)
    rColdWaterPumpDemand    : REAL;     (* Demand signal to deep CWP variable speed drive [%] *)
    rWarmWaterPumpDemand    : REAL;     (* Demand signal to surface seawater pump [%] *)
    rTurbineValvePos        : REAL;     (* Turbine inlet guide vane/valve position [%] *)
    bOverspeedTrip          : BOOL;     (* Turbine over-speed mechanical trip signal *)
    bAlarm                  : BOOL;     (* General system fault alarm *)
    iOperatingState         : INT;      (* Current operating state machine step *)
END_VAR
VAR
    iState                  : INT := 0; (* Internal state machine step *)
    tStartupTimer           : TON;      (* Startup sequence timer *)
    tShutdownTimer          : TON;      (* Shutdown sequence timer *)
    rDeltaTemp              : REAL;     (* Computed temperature differential *)
    rTargetAmmoniaFlow      : REAL;     (* Internal calculated ammonia flow target *)
    rPidError               : REAL;     (* Error term for pressure control *)
    rPidIntegral            : REAL;     (* Integral term for pressure control *)
    bIsTripped              : BOOL;     (* Internal trip state latch *)
END_VAR

(* === OTEC THERMAL ENERGY CONVERSION MAIN LOGIC === *)

(* Safety and Interlock Processing *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bAlarm := TRUE;
    bOverspeedTrip := FALSE;
    rAmmoniaFlowDemand := 0.0;
    rColdWaterPumpDemand := 0.0;
    rWarmWaterPumpDemand := 0.0;
    rTurbineValvePos := 0.0;
    iState := 999; (* Transition to fault state *)
    bIsTripped := TRUE;
    RETURN;
END_IF;

(* Critical Turbine Overspeed Protection *)
IF rTurbineSpeedRPM > 3600.0 THEN
    bOverspeedTrip := TRUE;
    bAlarm := TRUE;
    bIsTripped := TRUE;
    rTurbineValvePos := 0.0; (* Slam shut *)
    iState := 999;
END_IF;

(* Temperature Differential Calculation *)
rDeltaTemp := rWarmSeawaterTemp - rColdSeawaterTemp;

(* Main Operating State Machine *)
CASE iState OF
    0: (* IDLE STATE *)
        bSystemReady := FALSE;
        rAmmoniaFlowDemand := 0.0;
        rColdWaterPumpDemand := 0.0;
        rWarmWaterPumpDemand := 0.0;
        rTurbineValvePos := 0.0;
        
        IF bEnable AND NOT bIsTripped THEN
            IF rDeltaTemp >= 18.0 THEN (* Minimum viable delta T for OTEC *)
                iState := 10;
            ELSE
                bAlarm := TRUE; (* Insufficient thermal gradient *)
            END_IF;
        END_IF;
        
    10: (* SEAWATER PUMP STARTUP sequence *)
        (* Ramp up cold water pipe flow to establish condenser delta T *)
        rColdWaterPumpDemand := rColdWaterPumpDemand + 0.1;
        rWarmWaterPumpDemand := rWarmWaterPumpDemand + 0.15;
        
        IF (rColdWaterPumpDemand > 60.0) AND (rWarmWaterPumpDemand > 75.0) THEN
            tStartupTimer(IN := TRUE, PT := T#30S);
            IF tStartupTimer.Q THEN
                tStartupTimer(IN := FALSE);
                iState := 20;
            END_IF;
        END_IF;
        
    20: (* AMMONIA PRESSURIZATION *)
        (* Start closed-loop ammonia cycle feed pump *)
        rPidError := 15.0 - rAmmoniaPressureEvap; (* Target 15 bar for working fluid *)
        rPidIntegral := rPidIntegral + (rPidError * 0.01);
        rTargetAmmoniaFlow := (rPidError * 2.5) + (rPidIntegral * 0.5);
        
        IF rTargetAmmoniaFlow > 100.0 THEN
            rTargetAmmoniaFlow := 100.0;
        ELSIF rTargetAmmoniaFlow < 0.0 THEN
            rTargetAmmoniaFlow := 0.0;
        END_IF;
        
        rAmmoniaFlowDemand := rTargetAmmoniaFlow;
        
        IF rAmmoniaPressureEvap > 14.5 AND rAmmoniaPressureCond < 5.0 THEN
            iState := 30;
        END_IF;
        
    30: (* TURBINE ROLL AND SYNCHRONIZATION *)
        (* Crack open the inlet guide vanes *)
        IF rTurbineSpeedRPM < 3000.0 THEN
            rTurbineValvePos := rTurbineValvePos + 0.05;
        ELSE
            (* Speed control mode approaching synchronous speed *)
            rTurbineValvePos := 45.0 + ((3000.0 - rTurbineSpeedRPM) * 0.1);
        END_IF;
        
        IF (rTurbineSpeedRPM >= 2990.0) AND (rTurbineSpeedRPM <= 3010.0) THEN
            bSystemReady := TRUE;
            iState := 40;
        END_IF;
        
    40: (* STEADY STATE GENERATION *)
        (* Grid synchronized, maintain optimal thermal efficiency *)
        rColdWaterPumpDemand := 85.0 - (rAmmoniaPressureCond * 2.0);
        rWarmWaterPumpDemand := 90.0 + (15.0 - rAmmoniaPressureEvap);
        
        IF NOT bEnable THEN
            iState := 50; (* Normal shutdown sequence *)
        END_IF;
        
    50: (* NORMAL SHUTDOWN *)
        bSystemReady := FALSE;
        rTurbineValvePos := rTurbineValvePos - 0.5;
        IF rTurbineValvePos <= 0.0 THEN
            rTurbineValvePos := 0.0;
            tShutdownTimer(IN := TRUE, PT := T#60S);
            IF tShutdownTimer.Q THEN
                tShutdownTimer(IN := FALSE);
                iState := 0;
            END_IF;
        END_IF;
        
    999: (* FAULT / TRIP STATE *)
        bSystemReady := FALSE;
        rTurbineValvePos := 0.0;
        rAmmoniaFlowDemand := 0.0;
        
        (* Maintain some cooling flow during fault trip to prevent pressure spike *)
        rColdWaterPumpDemand := 30.0;
        rWarmWaterPumpDemand := 30.0;
        
        IF bEmergencyStop AND NOT bOverspeedTrip AND NOT bEnable THEN
            bIsTripped := FALSE;
            bAlarm := FALSE;
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
