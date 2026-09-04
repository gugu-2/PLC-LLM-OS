import os, json, uuid
os.makedirs('data/swarm_raw', exist_ok=True)
prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Semiconductor Chemical Mechanical Planarization (CMP) Polisher**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., nano-level dynamic downward force feedback, precise slurry pH/flow cascading loops, wafer slip/friction detection, and active platen cooling). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_CMP_Polisher\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
   record = {\"messages\": [{\"role\": \"user\", \"content\": prompt}, {\"role\": \"assistant\", \"content\": code}]}
   with open(f\"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json\", \"w\", encoding=\"utf-8\") as f:
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
6. REPLY with: EVOLUTION COMPLETE: Semiconductor Chemical Mechanical Planarization (CMP) Polisher

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_CMP_Polisher_Control
VAR_INPUT
    bEnable                 : BOOL;     (* System master enable *)
    bEmergencyStop          : BOOL;     (* Safety relay OK signal *)
    rWaferDownwardForceCmd  : REAL;     (* Target nano-level downward force (N) *)
    rWaferDownwardForceAct  : REAL;     (* Actual downward force from piezo sensor (N) *)
    rPlatenSpeedCmd         : REAL;     (* Target platen rotation speed (RPM) *)
    rPlatenSpeedAct         : REAL;     (* Actual platen speed from encoder (RPM) *)
    rSlurryFlowRateCmd      : REAL;     (* Target slurry flow rate (ml/min) *)
    rSlurryFlowRateAct      : REAL;     (* Actual slurry flow rate (ml/min) *)
    rSlurryPHAct            : REAL;     (* Actual slurry pH reading *)
    rPlatenTempAct          : REAL;     (* Actual platen temperature (deg C) *)
    rCarrierFriction        : REAL;     (* Friction torque estimation (Nm) *)
END_VAR
VAR_OUTPUT
    bSystemReady            : BOOL;     (* System ready for planarization *)
    rDownwardForceOut       : REAL;     (* Control signal to pneumatic/piezo actuator (0-10V) *)
    rPlatenSpeedOut         : REAL;     (* Control signal to platen servo drive (0-10V) *)
    rSlurryPumpOut          : REAL;     (* Control signal to slurry peristaltic pump (0-100%) *)
    rCoolingValveOut        : REAL;     (* Control signal to active platen cooling valve (0-100%) *)
    bWaferSlipAlarm         : BOOL;     (* Alarm: Wafer slipping or friction out of bounds *)
    bProcessAlarm           : BOOL;     (* Alarm: General process fault *)
END_VAR
VAR
    iState                  : INT := 0;
    tTimer                  : TON;
    rForceError             : REAL;
    rForceIntegral          : REAL := 0.0;
    rForceKp                : REAL := 2.5;
    rForceKi                : REAL := 0.15;
    
    rSpeedError             : REAL;
    rSpeedKp                : REAL := 1.2;
    rSpeedIntegral          : REAL := 0.0;
    
    rFrictionLimitHigh      : REAL := 15.0; (* Nm *)
    rFrictionLimitLow       : REAL := 2.0;  (* Nm *)
    rMaxTemp                : REAL := 45.0; (* Max platen temp deg C *)
END_VAR

(* === MAIN SAFETY AND INTERLOCK LOGIC === *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bProcessAlarm := TRUE;
    rDownwardForceOut := 0.0;
    rPlatenSpeedOut := 0.0;
    rSlurryPumpOut := 0.0;
    rCoolingValveOut := 0.0;
    iState := 0;
    RETURN;
END_IF;

(* === ACTIVE PLATEN COOLING LOOP === *)
IF rPlatenTempAct > 35.0 THEN
    rCoolingValveOut := LIMIT(0.0, (rPlatenTempAct - 35.0) * 10.0, 100.0);
ELSE
    rCoolingValveOut := 0.0;
END_IF;

IF rPlatenTempAct >= rMaxTemp THEN
    bProcessAlarm := TRUE;
    iState := 99; (* Fault state *)
END_IF;

(* === SLURRY PH & FLOW CASCADING LOOP === *)
(* Assuming a nominal pump curve and adjusting for pH anomalies if needed *)
rSlurryPumpOut := LIMIT(0.0, rSlurryFlowRateCmd * 0.8 + (rSlurryFlowRateCmd - rSlurryFlowRateAct) * 0.5, 100.0);
IF rSlurryPHAct < 2.0 OR rSlurryPHAct > 12.0 THEN
    bProcessAlarm := TRUE;
END_IF;

(* === MAIN STATE MACHINE === *)
CASE iState OF
    0: (* IDLE & INITIALIZATION *)
        bSystemReady := TRUE;
        rForceIntegral := 0.0;
        rSpeedIntegral := 0.0;
        bWaferSlipAlarm := FALSE;
        IF bEnable AND NOT bProcessAlarm THEN
            iState := 10;
        END_IF;

    10: (* RAMP UP PLATEN SPEED *)
        rSpeedError := rPlatenSpeedCmd - rPlatenSpeedAct;
        rSpeedIntegral := rSpeedIntegral + (rSpeedError * 0.01);
        rPlatenSpeedOut := LIMIT(0.0, (rSpeedError * rSpeedKp) + rSpeedIntegral, 10.0);
        
        IF ABS(rSpeedError) < 2.0 THEN
            tTimer(IN := TRUE, PT := T#2S);
            IF tTimer.Q THEN
                tTimer(IN := FALSE);
                iState := 20;
            END_IF;
        ELSE
            tTimer(IN := FALSE);
        END_IF;

    20: (* DYNAMIC DOWNWARD FORCE CONTROL & PLANARIZATION *)
        rForceError := rWaferDownwardForceCmd - rWaferDownwardForceAct;
        rForceIntegral := rForceIntegral + (rForceError * 0.005);
        rDownwardForceOut := LIMIT(0.0, (rForceError * rForceKp) + rForceIntegral, 10.0);
        
        (* Platen speed continues *)
        rSpeedError := rPlatenSpeedCmd - rPlatenSpeedAct;
        rSpeedIntegral := rSpeedIntegral + (rSpeedError * 0.01);
        rPlatenSpeedOut := LIMIT(0.0, (rSpeedError * rSpeedKp) + rSpeedIntegral, 10.0);
        
        (* Wafer Slip & Friction Detection *)
        IF rCarrierFriction > rFrictionLimitHigh OR rCarrierFriction < rFrictionLimitLow THEN
            bWaferSlipAlarm := TRUE;
            iState := 99;
        END_IF;
        
        IF NOT bEnable THEN
            iState := 30;
        END_IF;

    30: (* RAMP DOWN & RETRACT *)
        rDownwardForceOut := 0.0;
        rPlatenSpeedOut := 0.0;
        IF rPlatenSpeedAct < 1.0 THEN
            iState := 0;
        END_IF;

    99: (* FAULT HANDLING *)
        rDownwardForceOut := 0.0;
        rPlatenSpeedOut := 0.0;
        rSlurryPumpOut := 0.0;
        bSystemReady := FALSE;
        IF NOT bEnable THEN
            bProcessAlarm := FALSE;
            bWaferSlipAlarm := FALSE;
            iState := 0;
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
