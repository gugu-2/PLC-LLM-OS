import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Utility-Scale Cryogenic Carbon Capture and Storage (CCS) Liquefaction**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., -120°C auto-refrigerated cascade expansion, solid CO2 desublimation physical scraping, and dense phase supercritical pipeline injection). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_CCS_CryogenicLiquefaction\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Utility-Scale Cryogenic Carbon Capture and Storage (CCS) Liquefaction

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_CCS_CryogenicLiquefaction
VAR_INPUT
    bEnable                 : BOOL;     (* System enable signal *)
    bEmergencyStop          : BOOL;     (* Safety relay OK signal (Normally Closed) *)
    rInletGasTemp           : REAL;     (* Inlet CO2 gas temperature in deg C *)
    rInletGasPressure       : REAL;     (* Inlet CO2 gas pressure in bar *)
    rCascadeRefrigerantTemp : REAL;     (* Cascade auto-refrigerant temperature in deg C *)
    bScraperMotorOK         : BOOL;     (* Desublimation solid CO2 scraper motor status *)
    rSupercriticalDischargeP: REAL;     (* Pipeline injection discharge pressure in bar *)
    bVibrationHigh          : BOOL;     (* Compressor high vibration interlock *)
END_VAR
VAR_OUTPUT
    bSystemReady            : BOOL;     (* System ready status for sequence start *)
    rCompressorSpeedCmd     : REAL;     (* Main compressor speed command 0-100% *)
    bScraperRunCmd          : BOOL;     (* Scraper motor run command *)
    bExpansionValveOpen     : BOOL;     (* Cascade expansion valve open command *)
    rInjectionValvePos      : REAL;     (* Supercritical pipeline injection valve position 0-100% *)
    bCriticalAlarm          : BOOL;     (* Critical fault alarm requiring manual reset *)
    iSequenceStep           : INT;      (* Current step of liquefaction sequence *)
END_VAR
VAR
    iState                  : INT := 0;
    tStartDelay             : TON;
    tScraperTimer           : TON;
    tSurgeProtection        : TON;
    rIntegralError          : REAL := 0.0;
    rKp                     : REAL := 2.5;
    rKi                     : REAL := 0.1;
    bSurgeCondition         : BOOL := FALSE;
END_VAR

(* === MAIN SAFETY INTERLOCKS === *)
IF NOT bEmergencyStop OR bVibrationHigh THEN
    bSystemReady := FALSE;
    bCriticalAlarm := TRUE;
    rCompressorSpeedCmd := 0.0;
    bScraperRunCmd := FALSE;
    bExpansionValveOpen := FALSE;
    rInjectionValvePos := 0.0;
    iState := 999; (* FAULT STATE *)
    iSequenceStep := 999;
    RETURN;
END_IF;

(* === MAIN STATE MACHINE === *)
CASE iState OF
    0: (* IDLE & PRE-CHECKS *)
        iSequenceStep := 0;
        bSystemReady := (rInletGasPressure > 1.0) AND (rCascadeRefrigerantTemp < -40.0) AND bScraperMotorOK;
        rCompressorSpeedCmd := 0.0;
        bScraperRunCmd := FALSE;
        rInjectionValvePos := 0.0;
        
        IF bEnable AND bSystemReady THEN
            iState := 10;
        END_IF;

    10: (* CASCADE REFRIGERATION STARTUP *)
        iSequenceStep := 10;
        bExpansionValveOpen := TRUE;
        tStartDelay(IN := TRUE, PT := T#15S);
        
        IF tStartDelay.Q THEN
            tStartDelay(IN := FALSE);
            iState := 20;
        END_IF;

    20: (* MAIN COMPRESSOR RAMP UP & SURGE CONTROL *)
        iSequenceStep := 20;
        (* Basic PI control for compressor speed based on inlet pressure to maintain suction *)
        rIntegralError := rIntegralError + ((2.5 - rInletGasPressure) * rKi);
        
        (* Anti-windup *)
        IF rIntegralError > 50.0 THEN rIntegralError := 50.0; END_IF;
        IF rIntegralError < -50.0 THEN rIntegralError := -50.0; END_IF;
        
        rCompressorSpeedCmd := ((2.5 - rInletGasPressure) * rKp) + rIntegralError;
        
        (* Clamp output *)
        IF rCompressorSpeedCmd > 100.0 THEN rCompressorSpeedCmd := 100.0; END_IF;
        IF rCompressorSpeedCmd < 20.0 THEN rCompressorSpeedCmd := 20.0; END_IF;
        
        (* Check for desublimation conditions (-78.5 C at 1 atm, but lower here) *)
        IF rCascadeRefrigerantTemp <= -110.0 THEN
            iState := 30;
        END_IF;

    30: (* SOLID CO2 DESUBLIMATION SCRAPING *)
        iSequenceStep := 30;
        bScraperRunCmd := TRUE;
        tScraperTimer(IN := TRUE, PT := T#5M);
        
        IF tScraperTimer.Q THEN
            (* Duty cycle scraping complete, move to dense phase transition *)
            tScraperTimer(IN := FALSE);
            bScraperRunCmd := FALSE;
            iState := 40;
        END_IF;

    40: (* SUPERCRITICAL PIPELINE INJECTION *)
        iSequenceStep := 40;
        (* To reach supercritical phase, P > 73.8 bar, T > 31.1 C, but here we are dense phase liquid injection *)
        IF rSupercriticalDischargeP < 150.0 THEN
            rInjectionValvePos := rInjectionValvePos + 0.5;
        ELSE
            rInjectionValvePos := rInjectionValvePos - 0.5;
        END_IF;
        
        IF NOT bEnable THEN
            iState := 50;
        END_IF;

    50: (* CONTROLLED SHUTDOWN *)
        iSequenceStep := 50;
        rInjectionValvePos := 0.0;
        bScraperRunCmd := FALSE;
        rCompressorSpeedCmd := rCompressorSpeedCmd - 1.0;
        
        IF rCompressorSpeedCmd <= 0.0 THEN
            rCompressorSpeedCmd := 0.0;
            bExpansionValveOpen := FALSE;
            iState := 0;
        END_IF;

    999: (* FAULT HANDLING *)
        (* Wait for manual reset sequence *)
        IF NOT bEnable AND NOT bCriticalAlarm THEN
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
