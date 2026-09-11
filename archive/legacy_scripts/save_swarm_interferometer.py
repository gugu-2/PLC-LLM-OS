import os
import json
import uuid

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Deep-Space Optical Interferometer Delay Line**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Vacuum delay cart nanometer-precision piezo stepping, laser metrology active fringe tracking, and seismically isolated magnetic bearing suspension). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_InterferometerDelayLine\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Deep-Space Optical Interferometer Delay Line

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_OpticalInterferometerDelayLine
VAR_INPUT
    (* Required: physical inputs for the delay line system *)
    bEnable                 : BOOL;     (* System enable signal for the control loop *)
    bEmergencyStop          : BOOL;     (* Safety relay OK signal (active HIGH) *)
    rLaserMetrologyPos      : LREAL;    (* Laser metrology actual position in nanometers *)
    rTargetPosition         : LREAL;    (* Target position in nanometers for the active tracking *)
    rSeismicVibrationX      : REAL;     (* X-axis seismic vibration input for feed-forward compensation *)
    rSeismicVibrationY      : REAL;     (* Y-axis seismic vibration input for feed-forward compensation *)
    rSeismicVibrationZ      : REAL;     (* Z-axis seismic vibration input for feed-forward compensation *)
    bMagneticSuspensionOK   : BOOL;     (* Magnetic bearing suspension active and stable flag *)
END_VAR
VAR_OUTPUT
    (* Required: physical outputs to system actuators *)
    bSystemReady            : BOOL;     (* System ready status indicator *)
    rPiezoDriveControl      : LREAL;    (* Nanometer-precision piezo actuator drive signal (0-10V range) *)
    rLinearMotorForceCmd    : REAL;     (* Macroscopic delay line carriage force command for bulk movement *)
    bFringeTrackingActive   : BOOL;     (* Active fringe tracking engaged and locked indicator *)
    bAlarm                  : BOOL;     (* Fault alarm output triggered upon subsystem failure *)
END_VAR
VAR
    (* Internal state and controller variables *)
    iState                  : INT := 0;
    tStabilizationTimer     : TON;
    rPositionError          : LREAL := 0.0;
    rPositionErrorPrev      : LREAL := 0.0;
    rIntegralTerm           : LREAL := 0.0;
    rDerivativeTerm         : LREAL := 0.0;
    rKp                     : LREAL := 0.055;
    rKi                     : LREAL := 0.0012;
    rKd                     : LREAL := 0.015;
    rPiezoMax               : LREAL := 10.0;
    rPiezoMin               : LREAL := 0.0;
    rSeismicCompensation    : LREAL := 0.0;
END_VAR

(* === MAIN LOGIC === *)
(* Immediate safety interlock evaluation *)
IF NOT bEmergencyStop OR NOT bMagneticSuspensionOK THEN
    bSystemReady := FALSE;
    bFringeTrackingActive := FALSE;
    rLinearMotorForceCmd := 0.0;
    rPiezoDriveControl := 0.0;
    bAlarm := TRUE;
    iState := 0;
    RETURN;
END_IF;

bAlarm := FALSE;

(* High-precision finite state machine for delay line control *)
CASE iState OF
    0: (* IDLE *)
        bSystemReady := TRUE;
        bFringeTrackingActive := FALSE;
        IF bEnable THEN
            iState := 10;
        END_IF;

    10: (* MACRO POSITIONING - Slew carriage to within capture range of piezo *)
        rPositionError := rTargetPosition - rLaserMetrologyPos;
        IF ABS(rPositionError) > 5000.0 THEN
            (* Proportional control for macro linear motor positioning *)
            rLinearMotorForceCmd := LREAL_TO_REAL(rPositionError * 0.001);
        ELSE
            rLinearMotorForceCmd := 0.0;
            iState := 20;
        END_IF;

    20: (* STABILIZATION - Wait for carriage mechanical vibrations to dampen *)
        tStabilizationTimer(IN := TRUE, PT := T#2S);
        IF tStabilizationTimer.Q THEN
            tStabilizationTimer(IN := FALSE);
            iState := 30;
            rIntegralTerm := 0.0;
            rPositionErrorPrev := rTargetPosition - rLaserMetrologyPos;
        END_IF;

    30: (* NANO POSITIONING - Piezo active fringe tracking (Nanometer-precision) *)
        bFringeTrackingActive := TRUE;
        rPositionError := rTargetPosition - rLaserMetrologyPos;
        
        (* PID Control for Piezo Actuator *)
        rIntegralTerm := rIntegralTerm + (rPositionError * rKi);
        
        (* Anti-windup saturation logic for integral accumulation *)
        IF rIntegralTerm > rPiezoMax THEN rIntegralTerm := rPiezoMax; END_IF;
        IF rIntegralTerm < rPiezoMin THEN rIntegralTerm := rPiezoMin; END_IF;
        
        rDerivativeTerm := (rPositionError - rPositionErrorPrev) * rKd;
        rPositionErrorPrev := rPositionError;
        
        (* Seismic Feed-forward compensation utilizing external vibration sensors *)
        rSeismicCompensation := REAL_TO_LREAL(rSeismicVibrationZ) * 0.0005;
        
        (* Final control effort calculation *)
        rPiezoDriveControl := (rPositionError * rKp) + rIntegralTerm + rDerivativeTerm + rSeismicCompensation;
        
        (* Output saturation limiting to protect physical piezo constraints *)
        IF rPiezoDriveControl > rPiezoMax THEN
            rPiezoDriveControl := rPiezoMax;
        ELSIF rPiezoDriveControl < rPiezoMin THEN
            rPiezoDriveControl := rPiezoMin;
        END_IF;
        
        (* Exit condition *)
        IF NOT bEnable THEN
            bFringeTrackingActive := FALSE;
            rPiezoDriveControl := 0.0;
            iState := 0;
        END_IF;
        
    ELSE
        (* Failsafe default state *)
        iState := 0;
END_CASE;

END_FUNCTION_BLOCK
```"""

import os
os.makedirs('data/swarm_raw', exist_ok=True)
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
print(f"Saved to {filename}")
