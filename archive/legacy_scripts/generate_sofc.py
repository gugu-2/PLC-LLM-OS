import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Utility-Scale Solid Oxide Fuel Cell (SOFC) Co-Generation Plant**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., 800°C ceramic stack anode/cathode differential pressure tracking, exhaust heat recovery cascade (CHP), and natural gas desulfurization breakthrough detection). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_SOFC_CoGenPlant\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Utility-Scale Solid Oxide Fuel Cell (SOFC) Co-Generation Plant

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_SOFC_CoGenPlant
VAR_INPUT
    bSystemEnable           : BOOL;     (* Main system enable command from master DCS *)
    bEmergencyStop          : BOOL;     (* Emergency stop safety loop OK (1 = Safe) *)
    rStackTempActual        : REAL;     (* Ceramic stack temperature [degC], target 800-850 *)
    rAnodePressure          : REAL;     (* Anode fuel gas pressure [kPa] *)
    rCathodePressure        : REAL;     (* Cathode air pressure [kPa] *)
    rFuelFlowActual         : REAL;     (* Natural gas flow rate [kg/h] *)
    bDesulfurizationOK      : BOOL;     (* Desulfurization breakthrough detection signal (1 = OK) *)
    rHeatRecoveryTemp       : REAL;     (* CHP exhaust heat recovery inlet temp [degC] *)
END_VAR
VAR_OUTPUT
    bSystemReady            : BOOL;     (* System is ready for load / producing power *)
    rAnodeValveCmd          : REAL;     (* Control signal for Anode fuel valve 0-100% *)
    rCathodeBlowerCmd       : REAL;     (* Control signal for Cathode blower VFD 0-100% *)
    bSafetyTrip             : BOOL;     (* Main safety trip output (trip all fuel) *)
    bWarningAlarm           : BOOL;     (* Non-critical warning (e.g. slight delta P deviation) *)
    rCHP_BypassValveCmd     : REAL;     (* Exhaust heat recovery bypass valve 0-100% *)
END_VAR
VAR
    iStateMachine           : INT := 0; (* Internal state logic step for sequence control *)
    tStartupTimer           : TON;      (* Heat up timer for purging and preheating phases *)
    tTripTimer              : TON;      (* Trip delay timer for delta pressure anomaly *)
    rDeltaPressure          : REAL;     (* Computed Anode/Cathode diff pressure *)
    rTempError              : REAL;     (* Temperature tracking error versus target *)
    
    (* Internal tuning constants *)
    rMAX_DELTA_P            : REAL := 5.0;  (* Maximum allowed diff pressure [kPa] before trip *)
    rTARGET_TEMP            : REAL := 825.0;(* Target operating temp [degC] for ceramic stack *)
END_VAR

(* === MAIN SAFETY INTERLOCKS === *)
(* Immediate hardware protection loop overrides all other states *)
IF NOT bEmergencyStop OR NOT bDesulfurizationOK THEN
    bSafetyTrip := TRUE;
    bSystemReady := FALSE;
    rAnodeValveCmd := 0.0;
    rCathodeBlowerCmd := 10.0; (* Maintain slight purge flow on shutdown to prevent explosive mixtures *)
    iStateMachine := 999; (* Transition to TRIPPED FAULT STATE *)
    RETURN;
END_IF;

(* === CONTINUOUS DIAGNOSTICS & CALCULATIONS === *)
(* Compute the differential pressure across the solid oxide membrane *)
rDeltaPressure := ABS(rAnodePressure - rCathodePressure);

(* If delta pressure exceeds critical threshold, start the trip timer to filter noise *)
IF rDeltaPressure > rMAX_DELTA_P THEN
    tTripTimer(IN := TRUE, PT := T#2S);
ELSE
    tTripTimer(IN := FALSE);
END_IF;

IF tTripTimer.Q THEN
    bSafetyTrip := TRUE;
    iStateMachine := 999; (* Critical failure: Overpressure on ceramic plates *)
END_IF;

(* Early warning for operators if delta P is drifting high *)
IF rDeltaPressure > (rMAX_DELTA_P * 0.75) THEN
    bWarningAlarm := TRUE;
ELSE
    bWarningAlarm := FALSE;
END_IF;

(* === MAIN OPERATIONAL STATE MACHINE === *)
CASE iStateMachine OF
    0: (* IDLE / OFF / DE-ENERGIZED *)
        bSystemReady := FALSE;
        rAnodeValveCmd := 0.0;
        rCathodeBlowerCmd := 0.0;
        rCHP_BypassValveCmd := 100.0; (* Full bypass to exhaust stack when idle *)
        
        IF bSystemEnable AND NOT bSafetyTrip THEN
            iStateMachine := 10;
        END_IF;
        
    10: (* PURGE AND PRE-HEAT CYCLE *)
        rCathodeBlowerCmd := 30.0; (* Establish base air flow for initial thermal equilibrium *)
        rAnodeValveCmd := 0.0;
        tStartupTimer(IN := TRUE, PT := T#60S); (* Simulated long preheat cycle for ceramics *)
        
        IF tStartupTimer.Q THEN
            tStartupTimer(IN := FALSE);
            iStateMachine := 20;
        END_IF;
        
    20: (* RAMP TO THERMAL OPERATING TEMPERATURE *)
        (* Cathode air serves as primary heat transfer medium initially during ramp up *)
        rCathodeBlowerCmd := 50.0;
        (* Introduce fuel cautiously to prevent thermal shock *)
        rAnodeValveCmd := 15.0;
        
        IF rStackTempActual >= 750.0 THEN
            iStateMachine := 30;
        END_IF;
        
    30: (* NOMINAL POWER GENERATION AND CHP CONTROL (STEADY STATE) *)
        bSystemReady := TRUE;
        
        (* Proportional temperature control cascade mockup *)
        rTempError := rTARGET_TEMP - rStackTempActual;
        rAnodeValveCmd := 50.0 + (rTempError * 0.25);
        
        (* Actuator limits *)
        IF rAnodeValveCmd > 100.0 THEN rAnodeValveCmd := 100.0; END_IF;
        IF rAnodeValveCmd < 20.0 THEN rAnodeValveCmd := 20.0; END_IF;
        
        (* Differential pressure control - dynamically slave cathode to anode *)
        rCathodeBlowerCmd := rAnodeValveCmd * 1.05; 
        IF rCathodeBlowerCmd > 100.0 THEN rCathodeBlowerCmd := 100.0; END_IF;
        
        (* Heat Recovery / Co-Generation Cascade Loop *)
        IF rHeatRecoveryTemp < 150.0 THEN
            rCHP_BypassValveCmd := 0.0; (* All waste heat routed to recovery exchanger *)
        ELSIF rHeatRecoveryTemp > 250.0 THEN
            rCHP_BypassValveCmd := 100.0; (* Dump heat to exhaust to protect thermal loop *)
        ELSE
            (* Proportional modulation of the bypass valve for CHP regulation *)
            rCHP_BypassValveCmd := (rHeatRecoveryTemp - 150.0) * 1.0; 
        END_IF;
        
        IF NOT bSystemEnable THEN
            iStateMachine := 0; (* Graceful shutdown requested *)
        END_IF;
        
    999: (* FAULT HANDLING AND LATCHING *)
        bSystemReady := FALSE;
        IF NOT bEmergencyStop THEN
            (* Wait for manual hardware reset of the physical estop circuit *)
            bSafetyTrip := FALSE;
        END_IF;
        
        (* Require toggle of system enable to clear state machine fault *)
        IF bSystemEnable = FALSE AND bSafetyTrip = FALSE THEN
            iStateMachine := 0;
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
