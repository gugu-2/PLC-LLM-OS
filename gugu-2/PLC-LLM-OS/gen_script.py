import os, json, uuid

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Hydrogen Electrolyzer PEM Stack Anode/Cathode Pressure Balancing**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., cross-membrane pressure differential control at mbar resolution, cascading water feed flow loops, and explosive gas mixture detection interlocks). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_PEMElectrolyzer\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Hydrogen Electrolyzer PEM Stack Anode/Cathode Pressure Balancing

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_PEM_PressureBalanceControl
VAR_INPUT
    bEnable                 : BOOL;     (* System enable signal *)
    bEmergencyStop          : BOOL;     (* Emergency stop / Safety chain OK signal *)
    rAnodePressure          : REAL;     (* Measured O2 pressure at Anode (mbar) *)
    rCathodePressure        : REAL;     (* Measured H2 pressure at Cathode (mbar) *)
    rAnodeTemp              : REAL;     (* Anode temperature (Deg C) *)
    rCathodeTemp            : REAL;     (* Cathode temperature (Deg C) *)
    rWaterFeedFlow          : REAL;     (* Current water feed flow to stack (L/min) *)
    rMaxDiffPressure        : REAL;     (* Maximum allowable cross-membrane pressure diff (mbar) *)
END_VAR
VAR_OUTPUT
    bSystemReady            : BOOL;     (* System ready for operation *)
    rAnodeValveCmd          : REAL;     (* Anode pressure control valve command 0-100% *)
    rCathodeValveCmd        : REAL;     (* Cathode pressure control valve command 0-100% *)
    rWaterPumpCmd           : REAL;     (* Water feed pump speed command 0-100% *)
    bAlarmDifferential      : BOOL;     (* Cross-membrane differential pressure alarm *)
    bAlarmGasMixture        : BOOL;     (* Explosive gas mixture risk detected alarm *)
    bSafetyTrip             : BOOL;     (* Critical safety trip signal (hardware interlock) *)
END_VAR
VAR
    iState                  : INT := 0;
    rPressureDiff           : REAL;
    rPressureDiffFiltered   : REAL;
    rAlphaFilter            : REAL := 0.1;
    tFaultTimer             : TON;
    tStartupDelay           : TON;
    
    (* PI Controller States for Anode *)
    rAnodeKp                : REAL := 2.5;
    rAnodeKi                : REAL := 0.8;
    rAnodeError             : REAL;
    rAnodeIntegral          : REAL := 0.0;
    rAnodeSetpoint          : REAL := 15000.0; (* 15 bar in mbar *)
    
    (* PI Controller States for Cathode *)
    rCathodeKp              : REAL := 3.0;
    rCathodeKi              : REAL := 1.2;
    rCathodeError           : REAL;
    rCathodeIntegral        : REAL := 0.0;
    rCathodeSetpoint        : REAL := 15050.0; (* 15.05 bar in mbar *)
END_VAR

(* === MAIN LOGIC === *)
(* 1. Safety Interlocks and Diagnostics *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bSafetyTrip := TRUE;
    rAnodeValveCmd := 0.0;
    rCathodeValveCmd := 0.0;
    rWaterPumpCmd := 0.0;
    iState := 99; (* Fault State *)
    RETURN;
END_IF;

(* 2. Process Variable Filtering and Calculations *)
rPressureDiff := ABS(rCathodePressure - rAnodePressure);
rPressureDiffFiltered := (rPressureDiff * rAlphaFilter) + (rPressureDiffFiltered * (1.0 - rAlphaFilter));

(* 3. Alarm Generation *)
IF rPressureDiffFiltered > rMaxDiffPressure THEN
    tFaultTimer(IN := TRUE, PT := T#500MS);
    IF tFaultTimer.Q THEN
        bAlarmDifferential := TRUE;
        bSafetyTrip := TRUE;
    END_IF;
ELSE
    tFaultTimer(IN := FALSE);
    bAlarmDifferential := FALSE;
END_IF;

(* Check for dangerous temperature deviations which could imply gas crossover *)
IF (rAnodeTemp > 90.0) OR (rCathodeTemp > 90.0) THEN
    bAlarmGasMixture := TRUE;
    bSafetyTrip := TRUE;
END_IF;

IF bSafetyTrip THEN
    rAnodeValveCmd := 100.0;   (* Fail safe open to vent *)
    rCathodeValveCmd := 100.0; (* Fail safe open to vent *)
    rWaterPumpCmd := 0.0;
    bSystemReady := FALSE;
    iState := 99;
    RETURN;
END_IF;

(* 4. State Machine Control *)
CASE iState OF
    0: (* IDLE - Wait for System Enable *)
        rAnodeValveCmd := 0.0;
        rCathodeValveCmd := 0.0;
        rWaterPumpCmd := 0.0;
        bSystemReady := FALSE;
        IF bEnable AND NOT bSafetyTrip THEN
            iState := 10;
        END_IF;

    10: (* PURGE & PRESSURIZE PREP *)
        rWaterPumpCmd := 20.0; (* Low flow for membrane wetting *)
        tStartupDelay(IN := TRUE, PT := T#10S);
        IF tStartupDelay.Q THEN
            tStartupDelay(IN := FALSE);
            iState := 20;
        END_IF;

    20: (* RAMP TO PRESSURE *)
        (* Simple ramp logic or pass through to closed loop control *)
        bSystemReady := TRUE;
        iState := 30;

    30: (* CLOSED LOOP CONTROL - NORMAL OPERATION *)
        IF NOT bEnable THEN
            iState := 0;
        END_IF;
        
        (* Anode PI Control *)
        rAnodeError := rAnodeSetpoint - rAnodePressure;
        rAnodeIntegral := rAnodeIntegral + (rAnodeError * 0.01); (* Assume 10ms cycle *)
        rAnodeValveCmd := (rAnodeError * rAnodeKp) + rAnodeIntegral;
        
        (* Cathode PI Control - cascaded to maintain slight diff pressure *)
        rCathodeError := rCathodeSetpoint - rCathodePressure;
        rCathodeIntegral := rCathodeIntegral + (rCathodeError * 0.01);
        rCathodeValveCmd := (rCathodeError * rCathodeKp) + rCathodeIntegral;
        
        (* Anti-windup limits *)
        IF rAnodeValveCmd > 100.0 THEN rAnodeValveCmd := 100.0; END_IF;
        IF rAnodeValveCmd < 0.0 THEN rAnodeValveCmd := 0.0; END_IF;
        IF rCathodeValveCmd > 100.0 THEN rCathodeValveCmd := 100.0; END_IF;
        IF rCathodeValveCmd < 0.0 THEN rCathodeValveCmd := 0.0; END_IF;

        (* Cascading Water Feed Loop *)
        rWaterPumpCmd := 50.0 + (rPressureDiffFiltered * 0.5);
        IF rWaterPumpCmd > 100.0 THEN rWaterPumpCmd := 100.0; END_IF;

    99: (* FAULT STATE *)
        bSystemReady := FALSE;
        IF NOT bSafetyTrip AND NOT bEnable THEN
            iState := 0; (* Reset required by disabling *)
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
