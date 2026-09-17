import json, uuid
import os

os.makedirs('data/swarm_raw', exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Industrial Scale Aluminum Smelting Reduction Cell Anode Baking Temperature Profiling**

Task: Invent a highly complex, ultra-realistic control scenario for this domain. Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_Smelting_AnodeBaking\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Industrial Scale Aluminum Smelting Reduction Cell Anode Baking Temperature Profiling

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_AnodeBaking_TempProfile
VAR_INPUT
    (* Required: at least 4-8 physical inputs with types and comments *)
    bEnable               : BOOL;     (* System master enable signal *)
    bEmergencyStop        : BOOL;     (* Safety relay OK signal (active high) *)
    bGasValveInterlock    : BOOL;     (* Natural gas valve safety interlock *)
    rThermocouple1_Temp   : REAL;     (* Primary baking pit temperature (deg C) *)
    rThermocouple2_Temp   : REAL;     (* Secondary baking pit temperature (deg C) *)
    rAmbientTemp          : REAL;     (* Ambient factory temperature (deg C) *)
    rTargetSoakTemp       : REAL;     (* Desired soak phase temperature (deg C) *)
    rRampRate             : REAL;     (* Desired ramp rate (deg C / hour) *)
END_VAR
VAR_OUTPUT
    (* Required: at least 3-6 outputs with types and comments *)
    bSystemReady          : BOOL;     (* Baking control system is ready *)
    rGasValveCmd          : REAL;     (* 0-100% command to main natural gas burner valve *)
    rDraftFanCmd          : REAL;     (* 0-100% command to exhaust draft fan *)
    bBurnerIgnite         : BOOL;     (* Command to ignite burner *)
    bAlarm                : BOOL;     (* General fault alarm output *)
    iCurrentPhase         : INT;      (* Current baking phase (0=Off, 1=Purge, 2=Ramp, 3=Soak, 4=Cool) *)
END_VAR
VAR
    (* Internal state variables *)
    iState                : INT := 0;
    tPhaseTimer           : TON;
    tPurgeTimer           : TON;
    rFilteredTemp         : REAL;
    rTempError            : REAL;
    rIntegral             : REAL;
    rDerivative           : REAL;
    rLastError            : REAL;
    rPIDOutput            : REAL;
    rKp                   : REAL := 2.5;
    rKi                   : REAL := 0.05;
    rKd                   : REAL := 0.1;
    rSetpoint             : REAL;
    tCycleTimer           : TON;
    bInitialize           : BOOL := TRUE;
END_VAR

(* === MAIN LOGIC === *)
IF NOT bEmergencyStop OR NOT bGasValveInterlock THEN
    bSystemReady := FALSE;
    bAlarm := TRUE;
    rGasValveCmd := 0.0;
    rDraftFanCmd := 100.0; (* Full exhaust in emergency *)
    bBurnerIgnite := FALSE;
    iState := 0;
    iCurrentPhase := 0;
    RETURN;
END_IF;

bSystemReady := TRUE;
bAlarm := FALSE;

(* Temperature sensor redundancy and filtering (moving average / averaging) *)
IF (ABS(rThermocouple1_Temp - rThermocouple2_Temp) > 15.0) THEN
    bAlarm := TRUE; (* Sensor discrepancy alarm *)
END_IF;
rFilteredTemp := (rThermocouple1_Temp * 0.6) + (rThermocouple2_Temp * 0.4);

(* Simple state machine for Anode Baking Process *)
CASE iState OF
    0: (* IDLE *)
        iCurrentPhase := 0;
        rGasValveCmd := 0.0;
        rDraftFanCmd := 0.0;
        bBurnerIgnite := FALSE;
        rSetpoint := rAmbientTemp;
        IF bEnable THEN
            iState := 10; (* Transition to Purge Phase *)
        END_IF;

    10: (* PURGE PHASE - Clear combustible gases *)
        iCurrentPhase := 1;
        rDraftFanCmd := 100.0; (* Maximum draft for purging *)
        rGasValveCmd := 0.0;
        tPurgeTimer(IN := TRUE, PT := T#5M);
        IF tPurgeTimer.Q THEN
            tPurgeTimer(IN := FALSE);
            iState := 20; (* Transition to Ramp Phase *)
            bBurnerIgnite := TRUE;
        END_IF;

    20: (* RAMP PHASE - Controlled heating *)
        iCurrentPhase := 2;
        rDraftFanCmd := 50.0; (* Nominal draft *)
        
        (* Simulate ramp setpoint calculation based on ramp rate (per cycle/sec approx) *)
        IF rSetpoint < rTargetSoakTemp THEN
            rSetpoint := rSetpoint + (rRampRate / 3600.0); (* simplistic seconds-based increment *)
        ELSE
            iState := 30; (* Transition to Soak Phase *)
        END_IF;
        
        (* PID Control for Burner *)
        rTempError := rSetpoint - rFilteredTemp;
        rIntegral := rIntegral + rTempError;
        rDerivative := rTempError - rLastError;
        rPIDOutput := (rKp * rTempError) + (rKi * rIntegral) + (rKd * rDerivative);
        rLastError := rTempError;
        
        (* Limit output to valve 0-100% *)
        IF rPIDOutput > 100.0 THEN
            rGasValveCmd := 100.0;
        ELSIF rPIDOutput < 0.0 THEN
            rGasValveCmd := 0.0;
        ELSE
            rGasValveCmd := rPIDOutput;
        END_IF;
        
        IF NOT bEnable THEN
            iState := 40;
        END_IF;

    30: (* SOAK PHASE - Hold temperature *)
        iCurrentPhase := 3;
        rSetpoint := rTargetSoakTemp;
        tPhaseTimer(IN := TRUE, PT := T#48H); (* Typical 48 hr soak for anodes *)
        
        (* PID Control for Burner *)
        rTempError := rSetpoint - rFilteredTemp;
        rIntegral := rIntegral + rTempError;
        rDerivative := rTempError - rLastError;
        rPIDOutput := (rKp * rTempError) + (rKi * rIntegral) + (rKd * rDerivative);
        rLastError := rTempError;
        
        (* Limit output to valve 0-100% *)
        IF rPIDOutput > 100.0 THEN
            rGasValveCmd := 100.0;
        ELSIF rPIDOutput < 0.0 THEN
            rGasValveCmd := 0.0;
        ELSE
            rGasValveCmd := rPIDOutput;
        END_IF;
        
        IF tPhaseTimer.Q OR NOT bEnable THEN
            tPhaseTimer(IN := FALSE);
            iState := 40; (* Transition to Cool Phase *)
        END_IF;

    40: (* COOL PHASE - Controlled cooling before removal *)
        iCurrentPhase := 4;
        bBurnerIgnite := FALSE;
        rGasValveCmd := 0.0;
        rDraftFanCmd := 75.0; (* Increased draft for cooling *)
        
        IF rFilteredTemp < 150.0 THEN
            iState := 0; (* Return to Idle when safe *)
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
