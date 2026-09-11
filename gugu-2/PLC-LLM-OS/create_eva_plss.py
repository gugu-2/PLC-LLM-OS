import os, json, uuid

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Deep-Space Extra-Vehicular Activity (EVA) Spacesuit PLSS Life Support**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Cryogenic liquid oxygen (LOX) sublimator heat rejection, rapid depressurization metabolic oxygen cascade, and dual-loop primary/secondary ventilation switching). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_EVA_PLSS_LifeSupport\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Deep-Space Extra-Vehicular Activity (EVA) Spacesuit PLSS Life Support

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_EVA_PLSS_LifeSupport
VAR_INPUT
    bEnable                 : BOOL;     (* Master Enable signal for PLSS *)
    bEmergencyDepress       : BOOL;     (* True if suit pressure is dropping rapidly *)
    rMetabolicO2Flow        : REAL;     (* Current metabolic O2 consumption (kg/h) *)
    rSuitPressure           : REAL;     (* Current spacesuit internal pressure (kPa) *)
    rCoolantTemp            : REAL;     (* Cryogenic LOX sublimator coolant temp (deg C) *)
    bPrimaryVentLoopFail    : BOOL;     (* True if primary ventilation loop failure detected *)
    bManualOverride         : BOOL;     (* Astronaut manual override for secondary loop *)
END_VAR
VAR_OUTPUT
    bSystemReady            : BOOL;     (* PLSS ready and stable *)
    rO2SupplyValveCmd       : REAL;     (* Command to primary O2 supply valve (0.0 to 1.0) *)
    rSublimatorBypass       : REAL;     (* Command to cooling bypass valve (0.0 to 1.0) *)
    bSecondaryVentActive    : BOOL;     (* True when secondary vent loop is running *)
    bSuitLeakAlarm          : BOOL;     (* Critical alarm for uncontrolled suit depressurization *)
    bHypoxiaWarning         : BOOL;     (* Warning for low metabolic O2 flow vs pressure *)
END_VAR
VAR
    iOpMode                 : INT := 0; (* 0: INIT, 10: NOMINAL, 20: HIGH_METABOLIC, 30: EMERGENCY *)
    tDepressTimer           : TON;
    tLoopSwitchTimer        : TON;
    rNominalPressure        : REAL := 29.6; (* kPa, standard EVA pressure *)
    rMinSafePressure        : REAL := 24.1; (* kPa, absolute minimum safe pressure *)
    rTargetCoolantTemp      : REAL := 15.0; (* deg C, target setpoint *)
    rCoolingError           : REAL;
END_VAR

(* === MAIN LOGIC === *)
(* Emergency Depressurization Detection *)
IF rSuitPressure < rMinSafePressure OR bEmergencyDepress THEN
    bSuitLeakAlarm := TRUE;
    iOpMode := 30; (* Force EMERGENCY mode *)
ELSE
    bSuitLeakAlarm := FALSE;
END_IF;

(* Ventilation Loop Redundancy Management *)
IF bPrimaryVentLoopFail OR bManualOverride THEN
    tLoopSwitchTimer(IN := TRUE, PT := T#2S);
    IF tLoopSwitchTimer.Q THEN
        bSecondaryVentActive := TRUE;
    END_IF;
ELSE
    tLoopSwitchTimer(IN := FALSE);
    bSecondaryVentActive := FALSE;
END_IF;

(* Main State Machine *)
CASE iOpMode OF
    0: (* INIT Phase *)
        bSystemReady := FALSE;
        rO2SupplyValveCmd := 0.0;
        rSublimatorBypass := 1.0; (* Full bypass until temp stabilizes *)
        IF bEnable AND rSuitPressure >= rMinSafePressure THEN
            iOpMode := 10;
        END_IF;

    10: (* NOMINAL Operations *)
        bSystemReady := TRUE;
        
        (* Cascade O2 Control based on pressure *)
        IF rSuitPressure < rNominalPressure THEN
            rO2SupplyValveCmd := (rNominalPressure - rSuitPressure) * 0.5 + rMetabolicO2Flow * 0.1;
        ELSE
            rO2SupplyValveCmd := rMetabolicO2Flow * 0.1;
        END_IF;
        
        (* LOX Sublimator Heat Rejection Control *)
        rCoolingError := rCoolantTemp - rTargetCoolantTemp;
        IF rCoolingError > 0.0 THEN
            rSublimatorBypass := rSublimatorBypass - (rCoolingError * 0.05); (* Decrease bypass to cool more *)
        ELSE
            rSublimatorBypass := rSublimatorBypass + (ABS(rCoolingError) * 0.05); (* Increase bypass to warm *)
        END_IF;

        (* Clamp values *)
        IF rO2SupplyValveCmd > 1.0 THEN rO2SupplyValveCmd := 1.0; END_IF;
        IF rO2SupplyValveCmd < 0.0 THEN rO2SupplyValveCmd := 0.0; END_IF;
        IF rSublimatorBypass > 1.0 THEN rSublimatorBypass := 1.0; END_IF;
        IF rSublimatorBypass < 0.0 THEN rSublimatorBypass := 0.0; END_IF;

        (* Check for high metabolic load *)
        IF rMetabolicO2Flow > 2.5 THEN
            iOpMode := 20;
        END_IF;

    20: (* HIGH METABOLIC LOAD Operations *)
        bSystemReady := TRUE;
        (* Aggressive cooling and O2 supply *)
        rO2SupplyValveCmd := 0.8 + (rMetabolicO2Flow * 0.05);
        rSublimatorBypass := 0.0; (* Full cooling active *)
        
        IF rO2SupplyValveCmd > 1.0 THEN rO2SupplyValveCmd := 1.0; END_IF;
        
        IF rMetabolicO2Flow <= 2.0 THEN
            iOpMode := 10;
        END_IF;

    30: (* EMERGENCY Phase *)
        bSystemReady := FALSE;
        (* Flood suit with O2 to combat depressurization leak *)
        rO2SupplyValveCmd := 1.0; 
        rSublimatorBypass := 1.0; (* Conserve sublimator resources / freeze prevention *)
        bHypoxiaWarning := TRUE;
        
        (* Latch emergency state - requires manual reset/re-enable after clearing *)
        IF NOT bEnable AND NOT bSuitLeakAlarm THEN
            iOpMode := 0;
            bHypoxiaWarning := FALSE;
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
