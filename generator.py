import os, json, uuid

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Autonomous Large-Scale Plastic Injection Molding Clamping Force and Hold Pressure Profiling**

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_InjectionMolding_PressureProfile\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Autonomous Large-Scale Plastic Injection Molding Clamping Force and Hold Pressure Profiling

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_InjectionMolding_PressureProfile
(*========================================================================================
   Block Name    : FB_InjectionMolding_PressureProfile
   Description   : Autonomous Large-Scale Plastic Injection Molding Clamping Force 
                   and Hold Pressure Profiling Control Algorithm
   Author        : 40-Year PLC Automation Architect
   Date          : 2026-09-17
   Description   : Implements multi-layered state machine for clamping force buildup,
                   advanced PID with noise filtering for hold pressure profiling, and 
                   safety interlocks required for autonomous large-scale injection molding.
========================================================================================*)
VAR_INPUT
    bEnable                 : BOOL;     (* System enable signal from master controller *)
    bEmergencyStop_OK       : BOOL;     (* Safety relay OK signal (TRUE = safe to run) *)
    rMoldPosition_mm        : REAL;     (* Feedback from linear transducer on mold platen *)
    rClampPressure_bar      : REAL;     (* Hydraulic clamp pressure transmitter feedback *)
    rInjectionPressure_bar  : REAL;     (* Melt hold pressure feedback *)
    rSetClampForce_kN       : REAL;     (* Target clamping force in kiloNewtons *)
    rTargetHoldPress_bar    : REAL;     (* Target hold pressure setpoint *)
END_VAR

VAR_OUTPUT
    bSystemReady            : BOOL;     (* TRUE when interlocks met and system is in IDLE *)
    rClampValveCmd_Pct      : REAL;     (* 0-100% command to proportional clamp valve *)
    rInjectValveCmd_Pct     : REAL;     (* 0-100% command to proportional injection valve *)
    bCycleComplete          : BOOL;     (* TRUE when the molding cycle has finished normally *)
    bAlarm                  : BOOL;     (* Fault alarm output (interlock trip, timeout, etc.) *)
    iAlarmCode              : INT;      (* Diagnostics code for HMI troubleshooting *)
END_VAR

VAR
    (* Internal state variables *)
    iState                  : INT := 0; 
    tCycleTimer             : TON;
    tHoldTimer              : TON;
    tFilterTimer            : TON;
    
    (* Filtered signals *)
    rFilteredClampPress     : REAL := 0.0;
    rFilteredInjectPress    : REAL := 0.0;
    rAlpha                  : REAL := 0.15; (* First-order low pass filter coefficient *)
    
    (* PID variables for Hold Pressure *)
    rError                  : REAL;
    rIntegral               : REAL := 0.0;
    rDerivative             : REAL := 0.0;
    rLastError              : REAL := 0.0;
    rKp                     : REAL := 2.5;
    rKi                     : REAL := 0.8;
    rKd                     : REAL := 0.05;
    rDt                     : REAL := 0.01; (* Assume 10ms task cycle time *)
END_VAR

(* === MAIN LOGIC === *)
IF NOT bEmergencyStop_OK THEN
    bSystemReady := FALSE;
    bCycleComplete := FALSE;
    rClampValveCmd_Pct := 0.0;
    rInjectValveCmd_Pct := 0.0;
    bAlarm := TRUE;
    iAlarmCode := 9999; (* E-STOP Activated *)
    iState := 99;       (* Fault State *)
    RETURN;
END_IF;

(* === SIGNAL CONDITIONING / NOISE FILTERING === *)
(* Exponential Moving Average Filter for raw analog pressures *)
rFilteredClampPress := (rAlpha * rClampPressure_bar) + ((1.0 - rAlpha) * rFilteredClampPress);
rFilteredInjectPress := (rAlpha * rInjectionPressure_bar) + ((1.0 - rAlpha) * rFilteredInjectPress);

(* === MAIN STATE MACHINE === *)
CASE iState OF
    0: (* IDLE & READY *)
        bSystemReady := TRUE;
        bCycleComplete := FALSE;
        rClampValveCmd_Pct := 0.0;
        rInjectValveCmd_Pct := 0.0;
        bAlarm := FALSE;
        iAlarmCode := 0;
        rIntegral := 0.0;
        
        IF bEnable THEN
            bSystemReady := FALSE;
            iState := 10; (* Start cycle: Mold Closing *)
        END_IF;

    10: (* MOLD CLOSING & CLAMPING FORCE BUILDUP *)
        (* Simplified logic for mold position approaching zero *)
        IF rMoldPosition_mm > 5.0 THEN
            rClampValveCmd_Pct := 80.0; (* Fast close *)
        ELSE
            rClampValveCmd_Pct := 20.0; (* Slow mold protection *)
        END_IF;
        
        (* If clamped, build tonnage *)
        IF rMoldPosition_mm <= 0.1 THEN
            rClampValveCmd_Pct := 100.0; (* Build full pressure *)
            IF rFilteredClampPress >= (rSetClampForce_kN * 0.95) THEN
                iState := 20; (* Clamp built, proceed to injection/hold *)
            END_IF;
        END_IF;
        
        (* Watchdog timer for clamp buildup *)
        tCycleTimer(IN := TRUE, PT := T#15S);
        IF tCycleTimer.Q THEN
            iState := 99; (* Timeout fault *)
            iAlarmCode := 1010;
        END_IF;

    20: (* HOLD PRESSURE PROFILING (PID CONTROL) *)
        tCycleTimer(IN := FALSE); (* Reset clamp watchdog *)
        
        (* Execute PID for injection valve *)
        rError := rTargetHoldPress_bar - rFilteredInjectPress;
        rIntegral := rIntegral + (rError * rDt);
        
        (* Anti-windup *)
        IF rIntegral > 100.0 THEN rIntegral := 100.0; END_IF;
        IF rIntegral < -100.0 THEN rIntegral := -100.0; END_IF;
        
        rDerivative := (rError - rLastError) / rDt;
        rLastError := rError;
        
        rInjectValveCmd_Pct := (rKp * rError) + (rKi * rIntegral) + (rKd * rDerivative);
        
        (* Clamp Output 0-100% *)
        IF rInjectValveCmd_Pct > 100.0 THEN rInjectValveCmd_Pct := 100.0; END_IF;
        IF rInjectValveCmd_Pct < 0.0 THEN rInjectValveCmd_Pct := 0.0; END_IF;
        
        (* Maintain Clamp force passively or active control as needed *)
        rClampValveCmd_Pct := 50.0; 
        
        (* Timer for hold phase duration *)
        tHoldTimer(IN := TRUE, PT := T#20S);
        IF tHoldTimer.Q THEN
            tHoldTimer(IN := FALSE);
            iState := 30;
        END_IF;

    30: (* DECOMPRESSION & COOLING *)
        rInjectValveCmd_Pct := 0.0;
        rClampValveCmd_Pct := 10.0; (* Maintain slight clamp during cooling *)
        
        tHoldTimer(IN := TRUE, PT := T#10S); (* Cooling timer *)
        IF tHoldTimer.Q THEN
             tHoldTimer(IN := FALSE);
             iState := 40;
        END_IF;

    40: (* CYCLE COMPLETE *)
        bCycleComplete := TRUE;
        rClampValveCmd_Pct := 0.0;
        rInjectValveCmd_Pct := 0.0;
        
        IF NOT bEnable THEN
            iState := 0; (* Wait for next trigger *)
        END_IF;

    99: (* FAULT STATE *)
        bSystemReady := FALSE;
        rClampValveCmd_Pct := 0.0;
        rInjectValveCmd_Pct := 0.0;
        bAlarm := TRUE;
        
        (* Require enable cycle to reset *)
        IF NOT bEnable AND bEmergencyStop_OK THEN
            bAlarm := FALSE;
            iState := 0;
        END_IF;

END_CASE;

END_FUNCTION_BLOCK
```"""

record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
