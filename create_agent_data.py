import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Advanced Quantum Computer Cryogenic Dilution Refrigerator**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Helium-3/Helium-4 phase boundary isotope mixing, 10-milliKelvin continuous circulation turbo-pumping, and multi-stage radiation shield gradient tracking). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_QuantumDilutionFridge\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Advanced Quantum Computer Cryogenic Dilution Refrigerator

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_QuantumCryoDilutionFr
VAR_INPUT
    bEnableOperation      : BOOL;     (* System master enable *)
    bEstopStatusOk        : BOOL;     (* Hardwired emergency stop safety OK loop *)
    rTempMixingChamber    : REAL;     (* Temperature at the mixing chamber (Kelvin) *)
    rTempStill            : REAL;     (* Temperature at the still (Kelvin) *)
    rHe3FlowRate          : REAL;     (* Helium-3 circulation flow rate (mol/s) *)
    rPressureCondense     : REAL;     (* Condensing line pressure (mbar) *)
    bTurboPumpRunning     : BOOL;     (* Main circulation turbo pump status *)
    rHe4BathLevel         : REAL;     (* Liquid Helium-4 bath level (%) *)
END_VAR
VAR_OUTPUT
    bSystemStable         : BOOL;     (* Millikelvin target achieved and stable *)
    rTurboPumpSpeedRef    : REAL;     (* Speed reference output to turbo pump (Hz) *)
    rHe3He4MixRatioOut    : REAL;     (* Desired mixing ratio valve command (%) *)
    rHeaterStillCmd       : REAL;     (* Still heater power command (W) *)
    rHeaterMixChamberCmd  : REAL;     (* Mixing chamber heater power command (W) for PID *)
    bCriticalAlarm        : BOOL;     (* Quench or catastrophic warming alarm *)
END_VAR
VAR
    iState                : INT := 0; (* Cryo state machine sequence index *)
    rTargetBaseTemp       : REAL := 0.010; (* 10 mK base target *)
    rTargetStillTemp      : REAL := 0.8;   (* 800 mK still target *)
    rTempErrorMix         : REAL;
    rTempErrorStill       : REAL;
    rMixP                 : REAL := 15.0;
    rMixI                 : REAL := 0.5;
    rMixIntegral          : REAL := 0.0;
    rStillP               : REAL := 5.0;
    rStillI               : REAL := 0.1;
    rStillIntegral        : REAL := 0.0;
    tStabilizationTimer   : TON;
    tAlarmDelayTimer      : TON;
    bFirstScan            : BOOL := TRUE;
END_VAR

(* === MAIN LOGIC === *)
IF NOT bEstopStatusOk THEN
    bSystemStable := FALSE;
    bCriticalAlarm := TRUE;
    rTurboPumpSpeedRef := 0.0;
    rHeaterStillCmd := 0.0;
    rHeaterMixChamberCmd := 0.0;
    rHe3He4MixRatioOut := 0.0;
    iState := 999; (* FAULT STATE *)
    RETURN;
END_IF;

IF bFirstScan THEN
    bFirstScan := FALSE;
    iState := 0;
    bCriticalAlarm := FALSE;
END_IF;

CASE iState OF
    0: (* IDLE AND PRE-COOLING CHECK *)
        bSystemStable := FALSE;
        rTurboPumpSpeedRef := 0.0;
        rHeaterStillCmd := 0.0;
        rHeaterMixChamberCmd := 0.0;
        
        IF bEnableOperation AND (rTempMixingChamber < 4.2) THEN
            iState := 10; (* Start turbo pumps for circulation *)
        END_IF;

    10: (* TURBO PUMP RAMP UP AND CONDENSATION *)
        IF rPressureCondense > 50.0 THEN
            rTurboPumpSpeedRef := 800.0; (* Nominal 800 Hz *)
        ELSE
            rTurboPumpSpeedRef := 400.0; (* Condensing rate limit *)
        END_IF;
        
        IF bTurboPumpRunning AND (rHe3FlowRate > 0.005) THEN
            iState := 20; (* Circulation established *)
        END_IF;
        
        tAlarmDelayTimer(IN := TRUE, PT := T#60M);
        IF tAlarmDelayTimer.Q THEN
            bCriticalAlarm := TRUE; (* Failed to establish circulation *)
            iState := 999;
        END_IF;

    20: (* DILUTION COOLING AND PID CONTROL ACTIVE *)
        tAlarmDelayTimer(IN := FALSE);
        
        (* Still Heater Control - PI Loop *)
        rTempErrorStill := rTargetStillTemp - rTempStill;
        rStillIntegral := rStillIntegral + (rTempErrorStill * 0.1); (* Assuming 100ms cycle *)
        
        IF rStillIntegral > 10.0 THEN rStillIntegral := 10.0; END_IF;
        IF rStillIntegral < 0.0 THEN rStillIntegral := 0.0; END_IF;
        
        rHeaterStillCmd := (rTempErrorStill * rStillP) + (rStillIntegral * rStillI);
        IF rHeaterStillCmd > 20.0 THEN rHeaterStillCmd := 20.0; END_IF;
        IF rHeaterStillCmd < 0.0 THEN rHeaterStillCmd := 0.0; END_IF;

        (* Mixing Chamber Control - Fine PI Loop for 10 mK stabilization *)
        rTempErrorMix := rTargetBaseTemp - rTempMixingChamber;
        rMixIntegral := rMixIntegral + (rTempErrorMix * 0.1);
        
        IF rMixIntegral > 5.0 THEN rMixIntegral := 5.0; END_IF;
        IF rMixIntegral < -5.0 THEN rMixIntegral := -5.0; END_IF;
        
        rHeaterMixChamberCmd := (rTempErrorMix * rMixP) + (rMixIntegral * rMixI);
        IF rHeaterMixChamberCmd > 1.0 THEN rHeaterMixChamberCmd := 1.0; END_IF;
        IF rHeaterMixChamberCmd < 0.0 THEN rHeaterMixChamberCmd := 0.0; END_IF;

        (* Check for stable operation *)
        tStabilizationTimer(IN := (ABS(rTempErrorMix) < 0.002), PT := T#10M);
        
        IF tStabilizationTimer.Q THEN
            bSystemStable := TRUE;
        ELSE
            bSystemStable := FALSE;
        END_IF;
        
        (* Critical temperature loss check *)
        IF rTempMixingChamber > 0.1 THEN
            bCriticalAlarm := TRUE;
            iState := 999; (* Quench / thermal runaway *)
        END_IF;

        IF NOT bEnableOperation THEN
            iState := 0;
        END_IF;
        
    999: (* FAULT HANDLING *)
        bSystemStable := FALSE;
        rTurboPumpSpeedRef := 0.0;
        rHeaterStillCmd := 0.0;
        rHeaterMixChamberCmd := 0.0;
        IF bEnableOperation = FALSE THEN
            iState := 0;
            bCriticalAlarm := FALSE;
        END_IF;

END_CASE;

END_FUNCTION_BLOCK
```"""

os.makedirs("C:/Users/majip/Downloads/LLM REASEARCH/data/swarm_raw", exist_ok=True)
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
filename = f"C:/Users/majip/Downloads/LLM REASEARCH/data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print(f"Saved to {filename}")
