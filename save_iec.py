import json, uuid
import os

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Hypersonic Wind Tunnel Active Airflow Control System**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Mach 8+ flow stabilization, multi-stage compressor anti-surge control, extreme rapid-response temperature/pressure regulation, and cryogenic cooling loops). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_HypersonicTunnel\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Hypersonic Wind Tunnel Active Airflow Control System

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_HypersonicTunnelControl
VAR_INPUT
    bEnableFlow             : BOOL;     (* System master enable signal for airflow start sequence *)
    bEmergencyStop          : BOOL;     (* Safety loop OK signal - drops FALSE on any hardware trip *)
    rMachNumberTarget       : REAL;     (* Desired Mach number for the current test envelope (e.g. Mach 8.5) *)
    rStagnationPressure     : REAL;     (* Feedback from stagnation chamber pressure sensor (Bar) *)
    rStagnationTemp         : REAL;     (* Feedback from stagnation chamber temperature sensor (K) *)
    rCompressorRPM          : REAL;     (* Current rotational speed of the multi-stage compressor (RPM) *)
    rCryoCoolantFlow        : REAL;     (* Liquid Nitrogen coolant flow rate feedback (kg/s) *)
    bSurgeDetectorOK        : BOOL;     (* Active TRUE if multi-stage compressor is away from surge line *)
END_VAR
VAR_OUTPUT
    bSystemReady            : BOOL;     (* TRUE when flow parameters are stabilized at target conditions *)
    rMainThrottleValve      : REAL;     (* Control signal 0-100% for the primary hypersonic nozzle throttle *)
    rCryoValveControl       : REAL;     (* Control signal 0-100% for the heat exchanger cryogenic cooling valve *)
    rCompressorDriveSet     : REAL;     (* RPM setpoint for the Variable Frequency Drive (VFD) of compressor *)
    bAntiSurgeValveOpen     : BOOL;     (* Fast-acting anti-surge bypass valve state *)
    bCriticalAlarm          : BOOL;     (* Major fault alarm output requiring immediate shutdown *)
END_VAR
VAR
    iState                  : INT := 0; (* Internal state machine step index *)
    tSurgeTimer             : TON;      (* Timer to filter spurious anti-surge detector trips *)
    tStabilizationTimer     : TON;      (* Timer to confirm steady state at Mach target *)
    rErrorPressure          : REAL;     (* Internal PI error for pressure *)
    rIntegralPressure       : REAL;     (* Internal PI integral for pressure *)
    rErrorTemp              : REAL;     (* Internal PI error for temperature *)
    rIntegralTemp           : REAL;     (* Internal PI integral for temperature *)
    rKp_P                   : REAL := 2.5; (* Proportional gain for pressure control loop *)
    rKi_P                   : REAL := 0.15;(* Integral gain for pressure control loop *)
    rKp_T                   : REAL := 5.0; (* Proportional gain for temperature control loop *)
    rKi_T                   : REAL := 0.2; (* Integral gain for temperature control loop *)
END_VAR

(* === MAIN LOGIC === *)
(* Emergency Stop Interlock - Immediate Fail-safe Actions *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bCriticalAlarm := TRUE;
    rMainThrottleValve := 0.0;
    rCryoValveControl := 100.0; (* Maximum cooling on trip *)
    rCompressorDriveSet := 0.0;
    bAntiSurgeValveOpen := TRUE; (* Open bypass *)
    iState := 999; (* Fault state *)
    RETURN;
END_IF;

(* Continuous Anti-Surge Protection *)
IF NOT bSurgeDetectorOK THEN
    tSurgeTimer(IN := TRUE, PT := T#50MS);
    IF tSurgeTimer.Q THEN
        bAntiSurgeValveOpen := TRUE;
        bCriticalAlarm := TRUE;
        rCompressorDriveSet := rCompressorDriveSet * 0.8; (* Drop speed by 20% fast *)
    END_IF;
ELSE
    tSurgeTimer(IN := FALSE);
    bAntiSurgeValveOpen := FALSE;
END_IF;

(* Sequence State Machine *)
CASE iState OF
    0: (* IDLE *)
        bSystemReady := FALSE;
        rMainThrottleValve := 0.0;
        IF bEnableFlow AND bEmergencyStop THEN
            iState := 10;
        END_IF;

    10: (* COMPRESSOR RAMP-UP *)
        (* Bring compressor to base speed for initialization *)
        rCompressorDriveSet := 12000.0; (* Base RPM *)
        IF rCompressorRPM > 11500.0 THEN
            iState := 20;
        END_IF;

    20: (* PRESSURE & TEMP STABILIZATION (PI LOOPS) *)
        (* Target calculations based on requested Mach number approximation *)
        rErrorPressure := (rMachNumberTarget * 10.0) - rStagnationPressure;
        rIntegralPressure := rIntegralPressure + (rErrorPressure * 0.01); 
        rMainThrottleValve := (rKp_P * rErrorPressure) + (rIntegralPressure * rKi_P);
        
        (* Clamp throttle *)
        IF rMainThrottleValve > 100.0 THEN rMainThrottleValve := 100.0; END_IF;
        IF rMainThrottleValve < 0.0 THEN rMainThrottleValve := 0.0; END_IF;

        (* Temperature Control via Cryo Valve *)
        rErrorTemp := rStagnationTemp - (rMachNumberTarget * 150.0); (* Rough cooling demand model *)
        rIntegralTemp := rIntegralTemp + (rErrorTemp * 0.01);
        rCryoValveControl := (rKp_T * rErrorTemp) + (rIntegralTemp * rKi_T);
        
        (* Clamp cryo valve *)
        IF rCryoValveControl > 100.0 THEN rCryoValveControl := 100.0; END_IF;
        IF rCryoValveControl < 0.0 THEN rCryoValveControl := 0.0; END_IF;

        (* Check stability envelope *)
        IF ABS(rErrorPressure) < 2.0 AND ABS(rErrorTemp) < 10.0 THEN
            tStabilizationTimer(IN := TRUE, PT := T#10S);
            IF tStabilizationTimer.Q THEN
                iState := 30;
                tStabilizationTimer(IN := FALSE);
            END_IF;
        ELSE
            tStabilizationTimer(IN := FALSE);
        END_IF;

    30: (* HYPERSONIC FLOW MAINTAINED - SYSTEM READY *)
        bSystemReady := TRUE;
        (* Continue running PI loops as above *)
        rErrorPressure := (rMachNumberTarget * 10.0) - rStagnationPressure;
        rIntegralPressure := rIntegralPressure + (rErrorPressure * 0.01); 
        rMainThrottleValve := (rKp_P * rErrorPressure) + (rIntegralPressure * rKi_P);
        IF rMainThrottleValve > 100.0 THEN rMainThrottleValve := 100.0; END_IF;
        IF rMainThrottleValve < 0.0 THEN rMainThrottleValve := 0.0; END_IF;

        IF NOT bEnableFlow THEN
            iState := 40;
        END_IF;

    40: (* SHUTDOWN SEQUENCE *)
        bSystemReady := FALSE;
        rMainThrottleValve := rMainThrottleValve - 1.0; (* Ramp down *)
        IF rMainThrottleValve <= 0.0 THEN
            rMainThrottleValve := 0.0;
            iState := 0;
        END_IF;

    999: (* FAULT LOCKOUT *)
        (* Wait for manual reset or bEmergencyStop recovery to transition back to 0 *)
        IF bEmergencyStop THEN
            bCriticalAlarm := FALSE;
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
