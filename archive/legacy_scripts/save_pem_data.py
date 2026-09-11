import json, uuid, os

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Industrial Scale Green Hydrogen Proton Exchange Membrane (PEM) Electrolyzer**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., 20MW multi-stack current ripple harmonic filtering, anodic oxygen cross-over explosive limit detection, and ultra-pure water (UPW) deionization polishing loop). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\nFUNCTION_BLOCK FB_PEM_Electrolyzer\n//...\nEND_FUNCTION_BLOCK\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Industrial Scale Green Hydrogen Proton Exchange Membrane (PEM) Electrolyzer

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_PEM_Electrolyzer_20MW
VAR_INPUT
    (* System Operation & Safety Inputs *)
    bEnable                 : BOOL;     (* System enable signal from master DCS *)
    bEmergencyStop          : BOOL;     (* Safety relay OK signal (Normally Closed fail-safe) *)
    rStackCurrent_A         : REAL;     (* Measured stack DC current [Amperes] from high-speed shunt *)
    
    (* Critical Process Constraints *)
    rAnodeO2Concentration   : REAL;     (* Oxygen concentration in H2 stream [% LEL] *)
    rUPWConductivity        : REAL;     (* Ultra-pure water conductivity [uS/cm] polishing loop return *)
    rStackTemp_C            : REAL;     (* Stack temperature [Degrees Celsius] *)
    rH2Pressure_Bar         : REAL;     (* Hydrogen product backpressure [Bar] *)
END_VAR
VAR_OUTPUT
    (* System Status & Control Signals *)
    bSystemReady            : BOOL;     (* System ready status for sequence operation *)
    rRectifierDemand        : REAL;     (* Demand setpoint output to DC Rectifier [Amperes] *)
    
    (* Alarm & Safety Interventions *)
    bAlarm                  : BOOL;     (* General fault alarm output (Non-critical) *)
    bSafetyTrip             : BOOL;     (* Critical safety shutdown trip flag *)
    bPurgeValveOpen         : BOOL;     (* Nitrogen Purge valve command for safe-state venting *)
END_VAR
VAR
    (* Internal State & Timers *)
    iState                  : INT := 0; (* Internal state machine tracker *)
    tGeneralTimer           : TON;      (* General purpose state transition timer *)
    tPurgeTimer             : TON;      (* Dedicated timer for N2 purge sequences *)
    
    (* Harmonic Ripple Filtering (Exponential Moving Average) *)
    rFilteredCurrent        : REAL;     (* Exponential moving average of stack current *)
    rAlpha                  : REAL := 0.05; (* Filter smoothing factor *)
    
    (* Hardcoded Safety Limits *)
    rMAX_O2_LEL             : REAL := 2.0;  (* Maximum allowable O2 in H2 [% LEL] *)
    rMAX_UPW_COND           : REAL := 1.0;  (* Maximum UPW conductivity [uS/cm] *)
    rMAX_TEMP_C             : REAL := 80.0; (* Maximum stack operational temperature [C] *)
END_VAR

(* === SAFETY INTERLOCKS AND FAULT DETECTION === *)
(* Fail-safe E-Stop evaluation. FALSE indicates loop is broken/E-Stop pressed *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bSafetyTrip := TRUE;
    bAlarm := TRUE;
    rRectifierDemand := 0.0;
    bPurgeValveOpen := TRUE; (* Command N2 purge to instantly vent hazardous gases *)
    iState := 99; (* Force state machine to FAULT state *)
    RETURN;
END_IF;

(* Continuous monitoring of critical process variables to prevent catastrophic failure *)
IF rAnodeO2Concentration > rMAX_O2_LEL OR 
   rUPWConductivity > rMAX_UPW_COND OR 
   rStackTemp_C > rMAX_TEMP_C THEN
    
    bSafetyTrip := TRUE;
    bAlarm := TRUE;
    rRectifierDemand := 0.0;
    bPurgeValveOpen := TRUE;
    iState := 99;
    RETURN;
END_IF;

(* Current Ripple Harmonic Filtering *)
(* Executes continuous Exponential Moving Average (EMA) to smooth high-frequency rectifier noise *)
(* Formula: y[i] = alpha * x[i] + (1 - alpha) * y[i-1] *)
rFilteredCurrent := (rAlpha * rStackCurrent_A) + ((1.0 - rAlpha) * rFilteredCurrent);

(* === ELECTROLYZER MAIN CONTROL STATE MACHINE === *)
CASE iState OF
    0: (* STATE 0: IDLE / READY TO START *)
        bSystemReady := TRUE;
        bSafetyTrip := FALSE;
        bAlarm := FALSE;
        rRectifierDemand := 0.0;
        bPurgeValveOpen := FALSE;
        
        IF bEnable THEN
            bSystemReady := FALSE;
            iState := 10; (* Transition to Pre-Purge Sequence *)
        END_IF;

    10: (* STATE 10: PRE-START N2 PURGE SEQUENCE *)
        bPurgeValveOpen := TRUE;
        tPurgeTimer(IN := TRUE, PT := T#30S);
        
        IF tPurgeTimer.Q THEN
            tPurgeTimer(IN := FALSE);
            bPurgeValveOpen := FALSE;
            iState := 20; (* Transition to Rectifier Ramp-Up *)
        END_IF;

    20: (* STATE 20: RECTIFIER CURRENT RAMP-UP *)
        (* Gradually increase current demand to mitigate stack thermal shock and voltage transients *)
        IF rRectifierDemand < 5000.0 THEN
            rRectifierDemand := rRectifierDemand + 15.0; (* Ramp 15A per PLC cycle *)
        ELSE
            iState := 30; (* Nominal setpoint reached, transition to Production *)
        END_IF;

    30: (* STATE 30: NOMINAL H2 PRODUCTION *)
        (* Implement dynamic load derating based on output H2 backpressure *)
        IF rH2Pressure_Bar > 30.0 THEN
            rRectifierDemand := 2500.0; (* Derate production 50% due to high pressure *)
        ELSE
            rRectifierDemand := 5000.0; (* Full nominal 20MW load ~5kA *)
        END_IF;

        IF NOT bEnable THEN
            iState := 40; (* Stop command received, transition to Shutdown *)
        END_IF;

    40: (* STATE 40: CONTROLLED SHUTDOWN *)
        rRectifierDemand := 0.0; (* Drop current demand instantly *)
        tGeneralTimer(IN := TRUE, PT := T#15S); (* Wait for stack depolarization *)
        IF tGeneralTimer.Q THEN
            tGeneralTimer(IN := FALSE);
            iState := 0; (* Return to IDLE state *)
        END_IF;

    99: (* STATE 99: FAULT LATCH & RECOVERY *)
        (* Faults remain latched until the enable signal is dropped and conditions normalize *)
        IF NOT bEnable AND rAnodeO2Concentration < (rMAX_O2_LEL * 0.8) THEN
            bSafetyTrip := FALSE;
            bAlarm := FALSE;
            bPurgeValveOpen := FALSE;
            iState := 0;
        END_IF;

END_CASE;

END_FUNCTION_BLOCK
```"""

record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
print("Saved")
