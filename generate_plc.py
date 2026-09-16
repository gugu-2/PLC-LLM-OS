import json, uuid, os

prompt = """<USER_REQUEST>
You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Automated Commercial-Scale Mycelium Mycoprotein Bioreactor**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Substrate glucose feed-forward titration, dissolved oxygen cascaded sparge control, and filamentous biomass density acoustic sensing). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_Mycelium_Bioreactor\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Automated Commercial-Scale Mycelium Mycoprotein Bioreactor

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT.
</USER_REQUEST>"""

code = """```iec-st
FUNCTION_BLOCK FB_Mycelium_Bioreactor
VAR_INPUT
    bEnable                 : BOOL;     (* System master enable for bioreactor process *)
    bEmergencyStop          : BOOL;     (* E-Stop safety circuit status (TRUE = OK, FALSE = Tripped) *)
    rDissolvedOxygen        : REAL;     (* Measured Dissolved Oxygen (DO) in % saturation *)
    rVesselTemp             : REAL;     (* Process temperature in deg Celsius *)
    rGlucoseConcentration   : REAL;     (* Substrate glucose concentration in g/L *)
    rBiomassDensity         : REAL;     (* Acoustic sensor measurement of filamentous density in g/L *)
    rpHLevel                : REAL;     (* pH measurement of the culture media *)
END_VAR
VAR_OUTPUT
    bSystemReady            : BOOL;     (* Bioreactor system readiness status *)
    bProcessActive          : BOOL;     (* Main fermentation sequence is active *)
    rSpargeAirFlow          : REAL;     (* Control output for DO sparge valve (0-100%) *)
    rAgitatorSpeed          : REAL;     (* Control output for agitator VFD (0-100%) *)
    rGlucoseFeedRate        : REAL;     (* Control output for substrate dosing pump (L/hr) *)
    bAlarmHighTemp          : BOOL;     (* Critical alarm for high temperature *)
    bAlarmLowDO             : BOOL;     (* Warning alarm for low dissolved oxygen *)
    bSafeStateInterlock     : BOOL;     (* Indicates system is in forced safe state *)
END_VAR
VAR
    iState                  : INT := 0; (* Internal state machine tracker *)
    tProcessTimer           : TON;      (* Process phase timer *)
    tSafetyTimer            : TON;      (* Delay timer for safety monitoring *)
    
    (* Internal PID / Control structures (simulated representation) *)
    rErrorDO                : REAL;
    rIntegralDO             : REAL;
    rDerivativeDO           : REAL;
    rPrevErrorDO            : REAL;
    
    (* Filtered signals *)
    rFilteredDO             : REAL;
    rFilteredTemp           : REAL;
    
    (* Constants *)
    c_rSetpointDO           : REAL := 45.0;     (* Target DO % *)
    c_rSetpointTemp         : REAL := 28.5;     (* Target Temp C *)
    c_rTargetBiomass        : REAL := 40.0;     (* Target final density g/L *)
    
    c_KpDO                  : REAL := 2.5;
    c_KiDO                  : REAL := 0.15;
    c_KdDO                  : REAL := 0.05;
END_VAR

(* === MAIN LOGIC === *)
(* Input Filtering (EMA filter for noise reduction) *)
rFilteredDO := (rFilteredDO * 0.9) + (rDissolvedOxygen * 0.1);
rFilteredTemp := (rFilteredTemp * 0.9) + (rVesselTemp * 0.1);

(* Safety Interlock Handling *)
IF NOT bEmergencyStop THEN
    iState := 999; (* Transition to fault state *)
    bSafeStateInterlock := TRUE;
    bSystemReady := FALSE;
    bProcessActive := FALSE;
    rSpargeAirFlow := 0.0;
    rAgitatorSpeed := 0.0;
    rGlucoseFeedRate := 0.0;
    RETURN;
END_IF;

bSafeStateInterlock := FALSE;

(* Main Process State Machine *)
CASE iState OF
    0: (* IDLE & PRE-CHECK *)
        bSystemReady := TRUE;
        bProcessActive := FALSE;
        rSpargeAirFlow := 5.0; (* Idle sweep *)
        rAgitatorSpeed := 10.0;
        rGlucoseFeedRate := 0.0;
        
        IF bEnable THEN
            iState := 10;
        END_IF;

    10: (* INOCULATION & GROWTH PHASE *)
        bSystemReady := TRUE;
        bProcessActive := TRUE;
        
        (* Cascaded DO Control with Sparge and Agitation *)
        rErrorDO := c_rSetpointDO - rFilteredDO;
        rIntegralDO := rIntegralDO + rErrorDO;
        rDerivativeDO := rErrorDO - rPrevErrorDO;
        
        (* PID calculation for sparge air flow *)
        rSpargeAirFlow := (c_KpDO * rErrorDO) + (c_KiDO * rIntegralDO) + (c_KdDO * rDerivativeDO);
        
        (* Clamp outputs *)
        IF rSpargeAirFlow > 100.0 THEN
            rSpargeAirFlow := 100.0;
        ELSIF rSpargeAirFlow < 5.0 THEN
            rSpargeAirFlow := 5.0;
        END_IF;
        
        rPrevErrorDO := rErrorDO;
        
        (* Base Agitator profile linked to Biomass density *)
        rAgitatorSpeed := 20.0 + (rBiomassDensity * 1.5);
        IF rAgitatorSpeed > 80.0 THEN
            rAgitatorSpeed := 80.0;
        END_IF;
        
        (* Feed-forward substrate dosing based on density *)
        rGlucoseFeedRate := rBiomassDensity * 0.25;
        
        (* Phase Transition condition *)
        IF rBiomassDensity >= c_rTargetBiomass THEN
            iState := 20;
        END_IF;
        
        (* Fault Checks *)
        IF rFilteredTemp > 35.0 THEN
            bAlarmHighTemp := TRUE;
            iState := 999;
        END_IF;
        
        IF rFilteredDO < 15.0 THEN
            bAlarmLowDO := TRUE;
        ELSE
            bAlarmLowDO := FALSE;
        END_IF;

    20: (* HARVEST PREPARATION *)
        bProcessActive := FALSE;
        rSpargeAirFlow := 2.0;
        rAgitatorSpeed := 5.0;
        rGlucoseFeedRate := 0.0;
        
        IF NOT bEnable THEN
            iState := 0;
        END_IF;

    999: (* FAULT STATE *)
        rSpargeAirFlow := 100.0; (* Max sparge to prevent anaerobiosis during fault *)
        rAgitatorSpeed := 0.0;
        rGlucoseFeedRate := 0.0;
        
        IF bEmergencyStop AND bEnable = FALSE AND rFilteredTemp < 30.0 THEN
            bAlarmHighTemp := FALSE;
            iState := 0;
        END_IF;

END_CASE;

END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": code}
    ]
}
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
print(f"Saved to {filename}")
