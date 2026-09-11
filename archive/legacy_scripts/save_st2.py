import os
import json, uuid

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Continuous Biomanufacturing Perfusion Cell Culture System**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., ultrafiltration/diafiltration (UF/DF) crossflow cascading, hollow fiber membrane transmembrane pressure (TMP) regulation, and continuous media bleed rate dynamic dosing). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_PerfusionBioreactor\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Continuous Biomanufacturing Perfusion Cell Culture System

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_PerfusionControl_UFDF
VAR_INPUT
    bEnable                 : BOOL;     (* System enable signal for the perfusion process *)
    bEmergencyStop          : BOOL;     (* Safety relay OK signal (TRUE = Safe) *)
    rInletPressure          : REAL;     (* Feed pressure to the hollow fiber filter (bar) *)
    rRetentatePressure      : REAL;     (* Retentate pressure returning to bioreactor (bar) *)
    rPermeatePressure       : REAL;     (* Permeate pressure on the extract side (bar) *)
    rVesselWeight           : REAL;     (* Bioreactor vessel weight for bleed rate control (kg) *)
    rTargetTMP              : REAL;     (* Setpoint for Transmembrane Pressure (bar) *)
    rBleedRateSP            : REAL;     (* Target continuous media bleed rate (L/hr) *)
END_VAR
VAR_OUTPUT
    bSystemReady            : BOOL;     (* System ready status for upstream integration *)
    rPermeatePumpCmd        : REAL;     (* Speed command for permeate extraction pump (%) *)
    rBleedPumpCmd           : REAL;     (* Speed command for cell bleed pump (%) *)
    rCalculatedTMP          : REAL;     (* Live calculation of Transmembrane Pressure (bar) *)
    bTMPAlarm               : BOOL;     (* High TMP alarm indicating potential membrane fouling *)
    bWeightAlarm            : BOOL;     (* Vessel weight deviation alarm *)
END_VAR
VAR
    iState                  : INT := 0; (* Internal state machine step *)
    tStartupDelay           : TON;      (* Delay timer for pump staging *)
    tTMPFilter              : TON;      (* Smoothing timer for TMP alarms *)
    rErrorTMP               : REAL;     (* PID error for TMP control *)
    rIntegralTMP            : REAL;     (* PID integral term for TMP *)
    rKp                     : REAL := 2.5; (* Proportional gain for TMP PID *)
    rKi                     : REAL := 0.15;(* Integral gain for TMP PID *)
    rMaxPumpCmd             : REAL := 100.0;
    rMinPumpCmd             : REAL := 0.0;
END_VAR

(* === MAIN LOGIC === *)
(* Safety Interlock *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    rPermeatePumpCmd := 0.0;
    rBleedPumpCmd := 0.0;
    bTMPAlarm := TRUE;
    bWeightAlarm := TRUE;
    iState := 0;
    RETURN;
END_IF;

(* Continuous TMP Calculation: TMP = (P_inlet + P_retentate)/2 - P_permeate *)
rCalculatedTMP := ((rInletPressure + rRetentatePressure) / 2.0) - rPermeatePressure;

(* High TMP Alarm Logic *)
IF rCalculatedTMP > (rTargetTMP * 1.25) THEN
    tTMPFilter(IN := TRUE, PT := T#3S);
    IF tTMPFilter.Q THEN
        bTMPAlarm := TRUE;
    END_IF;
ELSE
    tTMPFilter(IN := FALSE);
    bTMPAlarm := FALSE;
END_IF;

(* State Machine for Perfusion Control *)
CASE iState OF
    0: (* IDLE State *)
        bSystemReady := FALSE;
        rPermeatePumpCmd := 0.0;
        rBleedPumpCmd := 0.0;
        IF bEnable THEN
            iState := 10;
        END_IF;

    10: (* STARTUP Staging *)
        (* Staging pumps to prevent pressure spikes *)
        tStartupDelay(IN := TRUE, PT := T#10S);
        IF tStartupDelay.Q THEN
            tStartupDelay(IN := FALSE);
            bSystemReady := TRUE;
            iState := 20;
        END_IF;

    20: (* RUNNING State - Active Control *)
        IF NOT bEnable THEN
            iState := 0;
        ELSE
            (* PID Control for Permeate Pump based on TMP *)
            rErrorTMP := rTargetTMP - rCalculatedTMP;
            rIntegralTMP := rIntegralTMP + (rErrorTMP * rKi);
            
            (* Anti-windup for integral term *)
            IF rIntegralTMP > rMaxPumpCmd THEN rIntegralTMP := rMaxPumpCmd; END_IF;
            IF rIntegralTMP < rMinPumpCmd THEN rIntegralTMP := rMinPumpCmd; END_IF;
            
            rPermeatePumpCmd := (rErrorTMP * rKp) + rIntegralTMP;
            
            (* Clamp Permeate Pump Command *)
            IF rPermeatePumpCmd > rMaxPumpCmd THEN rPermeatePumpCmd := rMaxPumpCmd; END_IF;
            IF rPermeatePumpCmd < rMinPumpCmd THEN rPermeatePumpCmd := rMinPumpCmd; END_IF;

            (* Basic bleed pump control linked to setpoint *)
            rBleedPumpCmd := rBleedRateSP * 0.8; (* Simplified linear scaling for demonstration *)
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
