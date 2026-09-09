import os
os.makedirs("data/swarm_raw", exist_ok=True)
import json, uuid
prompt = """<USER_REQUEST>
You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Utility-Scale Coal Gasification (IGCC) Syngas Shift Converter**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Carbon monoxide to carbon dioxide water-gas shift catalytic thermal profiling, high-pressure syngas mass balancing, and steam injection stoichiometric cascading). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_SyngasShiftConverter\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Utility-Scale Coal Gasification (IGCC) Syngas Shift Converter

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT.
</USER_REQUEST>
<ADDITIONAL_METADATA>
The current local time is: 2026-09-06T12:54:43+05:30.
</ADDITIONAL_METADATA>"""
code = """```iec-st
FUNCTION_BLOCK FB_SyngasShiftConverter
(* 
   =============================================================================
   Block Name: FB_SyngasShiftConverter
   Description: Advanced Utility-Scale Coal Gasification (IGCC) Water-Gas Shift 
                Converter Controller. Integrates highly complex carbon monoxide to 
                carbon dioxide water-gas shift catalytic thermal profiling, high-pressure 
                syngas mass balancing, and steam injection stoichiometric cascading.
   =============================================================================
*)
VAR_INPUT
    bEnable               : BOOL;     (* System overall enable signal *)
    bEmergencyStop        : BOOL;     (* Safety instrumented system (SIS) OK signal, FALSE = Trip *)
    rSyngasFlowIn         : REAL;     (* Inlet syngas mass flow rate (kg/s) *)
    rSyngasCOFraction     : REAL;     (* Inlet syngas carbon monoxide mole fraction (0.0 - 1.0) *)
    rCatalystBedTemp      : REAL;     (* Average catalytic bed temperature (deg C) *)
    rReactorPress         : REAL;     (* Reactor vessel internal pressure (bar) *)
    rSteamHeaderPress     : REAL;     (* Available steam header pressure (bar) *)
    rTargetCOSlip         : REAL;     (* Target CO slip / unreacted CO fraction at outlet (0.0 - 1.0) *)
END_VAR

VAR_OUTPUT
    bSystemReady          : BOOL;     (* Shift converter ready for normal operation *)
    rSteamInjectionValve  : REAL;     (* Steam injection control valve position (0.0 - 100.0 %) *)
    rQuenchWaterValve     : REAL;     (* Quench water control valve for exotherm management (0.0 - 100.0 %) *)
    bHighTempAlarm        : BOOL;     (* Catalyst bed high-temperature excursion alarm *)
    bLowSteamRatioAlarm   : BOOL;     (* Steam-to-carbon ratio below minimum stoichiometric requirement *)
    bTripActivated        : BOOL;     (* Reactor tripped and isolated *)
END_VAR

VAR
    iState                : INT := 0; (* Internal state machine (0: OFF, 10: PURGE, 20: WARMUP, 30: RUN, 99: TRIP) *)
    tRunTimer             : TON;
    tPurgeTimer           : TON;
    rCalculatedSteamReq   : REAL;     (* Calculated steam requirement in kg/s *)
    rSteamToCarbonRatio   : REAL;     (* Real-time H2O/CO ratio *)
    rTempError            : REAL;     (* Thermal profiling error *)
    rProportionalBand     : REAL := 2.5; 
    rIntegralTime         : REAL := 120.0;
    rIntegralAccumulator  : REAL := 0.0;
    
    (* Constants for Water-Gas Shift (WGS) kinetics *)
    c_rMinSteamRatio      : REAL := 2.8;  (* Minimum H2O/CO ratio to prevent coking *)
    c_rMaxBedTemp         : REAL := 450.0;(* Maximum allowable catalyst temperature deg C *)
    c_rOptimalBedTemp     : REAL := 380.0;(* Optimal kinetic temperature for shift reaction *)
END_VAR

(* === MAIN LOGIC === *)
(* 1. Safety Interlocks and Critical Fault Handling *)
IF NOT bEmergencyStop OR rReactorPress > 85.0 THEN
    iState := 99; (* Force trip state *)
END_IF;

IF rCatalystBedTemp > c_rMaxBedTemp THEN
    bHighTempAlarm := TRUE;
ELSE
    bHighTempAlarm := FALSE;
END_IF;

(* 2. Mass Balance and Stoichiometric Calculation *)
(* Calculate moles of CO entering and required steam to maintain optimal ratio *)
IF rSyngasFlowIn > 0.0 THEN
    rSteamToCarbonRatio := rCalculatedSteamReq / (rSyngasFlowIn * rSyngasCOFraction + 0.001);
ELSE
    rSteamToCarbonRatio := 0.0;
END_IF;

bLowSteamRatioAlarm := (rSteamToCarbonRatio < c_rMinSteamRatio) AND (iState = 30);

(* 3. Core State Machine *)
CASE iState OF
    0: (* IDLE / OFF *)
        bSystemReady := FALSE;
        rSteamInjectionValve := 0.0;
        rQuenchWaterValve := 0.0;
        bTripActivated := FALSE;
        
        IF bEnable AND bEmergencyStop THEN
            iState := 10;
        END_IF;

    10: (* N2 PURGE SEQUENCE *)
        bSystemReady := FALSE;
        tPurgeTimer(IN := TRUE, PT := T#300S);
        IF tPurgeTimer.Q THEN
            tPurgeTimer(IN := FALSE);
            iState := 20;
        END_IF;
        
    20: (* CATALYST WARMUP AND STEAM INTRO *)
        (* Slowly introduce steam to heat catalyst bed *)
        rSteamInjectionValve := rSteamInjectionValve + 0.1;
        IF rSteamInjectionValve > 25.0 THEN
            rSteamInjectionValve := 25.0;
        END_IF;
        
        IF rCatalystBedTemp >= 250.0 THEN
            iState := 30;
        END_IF;
        
    30: (* NORMAL OPERATION: STOICHIOMETRIC CASCADING & THERMAL PROFILING *)
        bSystemReady := TRUE;
        
        (* Cascade 1: Steam-to-Carbon Ratio Controller *)
        rCalculatedSteamReq := rSyngasFlowIn * rSyngasCOFraction * 3.1; (* Target ratio of 3.1 *)
        rSteamInjectionValve := (rCalculatedSteamReq / rSteamHeaderPress) * 100.0;
        
        (* Clamp Steam Valve *)
        IF rSteamInjectionValve > 100.0 THEN
            rSteamInjectionValve := 100.0;
        END_IF;

        (* Cascade 2: Exotherm Thermal Management (Quench Controller) *)
        rTempError := rCatalystBedTemp - c_rOptimalBedTemp;
        IF rTempError > 0.0 THEN
            rIntegralAccumulator := rIntegralAccumulator + (rTempError / rIntegralTime);
            rQuenchWaterValve := (rTempError * rProportionalBand) + rIntegralAccumulator;
        ELSE
            rQuenchWaterValve := 0.0;
            rIntegralAccumulator := 0.0;
        END_IF;
        
        (* Clamp Quench Valve *)
        IF rQuenchWaterValve > 100.0 THEN
            rQuenchWaterValve := 100.0;
        END_IF;
        
        IF NOT bEnable THEN
            iState := 0;
        END_IF;
        
    99: (* TRIP STATE *)
        bSystemReady := FALSE;
        bTripActivated := TRUE;
        rSteamInjectionValve := 0.0;
        rQuenchWaterValve := 100.0; (* Full quench on trip to save catalyst *)
        tPurgeTimer(IN := FALSE);
        
        IF bEmergencyStop AND NOT bEnable THEN
            iState := 0; (* Reset only if interlocks clear and enable is dropped *)
        END_IF;

END_CASE;

END_FUNCTION_BLOCK
```"""
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
print("Saved")
