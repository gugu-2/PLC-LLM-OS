import json, uuid
import os

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Industrial Scale Liquid Hydrogen (LH2) Zero-Boil-Off (ZBO) Storage**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Cryocooler reversed Brayton cycle mass flow modulation, ortho-to-para hydrogen conversion catalyst thermal integration, and vacuum-jacketed structural strain relief). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_LH2_ZBO_Storage\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Industrial Scale Liquid Hydrogen (LH2) Zero-Boil-Off (ZBO) Storage

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_LH2_ZBO_AdvancedControl
VAR_INPUT
    bEnableSys            : BOOL;   (* Master enable for ZBO LH2 storage system *)
    bEmergencyEStop       : BOOL;   (* Hardware E-stop, safety relay monitored *)
    rTankPressure_kPa     : REAL;   (* Main LH2 vessel absolute pressure, kPa *)
    rTankTemp_K           : REAL;   (* LH2 bulk liquid temperature, Kelvin *)
    rCryocoolerSpeed_RPM  : REAL;   (* Feedback speed of reverse Brayton compressor, RPM *)
    rVacuumPressure_Torr  : REAL;   (* Annular vacuum space pressure, Torr *)
    rCatalystBedTemp_K    : REAL;   (* Ortho-to-para conversion catalyst bed temp, K *)
    rStrainGauge_uE       : REAL;   (* Micro-strain from inner vessel support struts *)
END_VAR
VAR_OUTPUT
    bSystemReady          : BOOL;   (* ZBO System fully operational and nominal *)
    rCryocoolerCmd_Pct    : REAL;   (* Compressor VFD command for cooling power, 0-100% *)
    bVentValveCmd         : BOOL;   (* Emergency boil-off vent valve command *)
    bHeaterCmd            : BOOL;   (* Catalyst bed heater command for regen *)
    iAlarmCode            : INT;    (* System alarm code (0=OK) *)
    bCriticalFault        : BOOL;   (* Critical safety trip *)
END_VAR
VAR
    (* Internal State and Timers *)
    iState                : INT := 0; (* Main state machine state *)
    tVentTimer            : TON;
    tStrainReliefTimer    : TON;
    rFilteredPressure     : REAL := 0.0;
    rFilteredTemp         : REAL := 0.0;
    
    (* PID & Control Variables *)
    rPressureError        : REAL;
    rPressureIntegral     : REAL := 0.0;
    rPressureDerivative   : REAL;
    rLastPressureError    : REAL := 0.0;
    rKp                   : REAL := 2.5;
    rKi                   : REAL := 0.05;
    rKd                   : REAL := 1.2;
    rMaxCryoCmd           : REAL := 100.0;
    
    (* Constants *)
    c_rMaxSafePressure    : REAL := 350.0; (* kPa *)
    c_rTargetPressure     : REAL := 120.0; (* kPa *)
    c_rMaxStrain          : REAL := 1500.0;(* uE *)
    c_rLossOfVacuum       : REAL := 1.0E-2;(* Torr *)
    
    bInitDone             : BOOL := FALSE;
END_VAR

(* === INITIALIZATION & FILTERING === *)
IF NOT bInitDone THEN
    rFilteredPressure := rTankPressure_kPa;
    rFilteredTemp := rTankTemp_K;
    bInitDone := TRUE;
END_IF;

(* First-order low-pass filter for sensor noise (Alpha = 0.1) *)
rFilteredPressure := (0.1 * rTankPressure_kPa) + (0.9 * rFilteredPressure);
rFilteredTemp := (0.1 * rTankTemp_K) + (0.9 * rFilteredTemp);

(* === SAFETY INTERLOCKS === *)
IF NOT bEmergencyEStop THEN
    bSystemReady       := FALSE;
    rCryocoolerCmd_Pct := 0.0;
    bVentValveCmd      := FALSE;
    bHeaterCmd         := FALSE;
    iAlarmCode         := 999; (* E-STOP *)
    bCriticalFault     := TRUE;
    iState             := 0;
    RETURN;
END_IF;

(* Hard Safety Limits *)
IF (rFilteredPressure > c_rMaxSafePressure) OR (rVacuumPressure_Torr > c_rLossOfVacuum) OR (rStrainGauge_uE > c_rMaxStrain) THEN
    bCriticalFault     := TRUE;
    bVentValveCmd      := (rFilteredPressure > c_rMaxSafePressure);
    rCryocoolerCmd_Pct := 0.0;
    iAlarmCode         := 100; (* CRITICAL OVERPRESSURE OR VACUUM LOSS OR STRAIN OVERLOAD *)
    iState             := 99;  (* FAULT STATE *)
    RETURN;
END_IF;

bCriticalFault := FALSE;

(* === MAIN STATE MACHINE === *)
CASE iState OF
    0: (* IDLE & SELF-CHECK *)
        bSystemReady := FALSE;
        rCryocoolerCmd_Pct := 0.0;
        bVentValveCmd := FALSE;
        
        IF bEnableSys AND (iAlarmCode = 0) THEN
            iState := 10; (* TRANSITION TO PRE-COOLING *)
        END_IF;

    10: (* PRE-COOLING CRYOCOOLER *)
        rCryocoolerCmd_Pct := 20.0; (* Startup mass flow modulation *)
        IF rCryocoolerSpeed_RPM > 1500.0 THEN
            iState := 20; (* TRANSITION TO ACTIVE ZBO CONTROL *)
        END_IF;
        
        IF NOT bEnableSys THEN
            iState := 0;
        END_IF;

    20: (* ACTIVE ZBO CONTROL (PID PRESSURE REGULATION) *)
        bSystemReady := TRUE;
        
        (* PID Computation for Pressure Control *)
        rPressureError := rFilteredPressure - c_rTargetPressure;
        rPressureIntegral := rPressureIntegral + (rPressureError * 0.1); (* 100ms task assumed *)
        rPressureDerivative := (rPressureError - rLastPressureError) / 0.1;
        
        rCryocoolerCmd_Pct := (rKp * rPressureError) + (rKi * rPressureIntegral) + (rKd * rPressureDerivative);
        
        (* Anti-windup and Saturation limits *)
        IF rCryocoolerCmd_Pct > rMaxCryoCmd THEN
            rCryocoolerCmd_Pct := rMaxCryoCmd;
            rPressureIntegral := rPressureIntegral - (rPressureError * 0.1); (* Anti-windup *)
        ELSIF rCryocoolerCmd_Pct < 0.0 THEN
            rCryocoolerCmd_Pct := 0.0;
        END_IF;
        
        rLastPressureError := rPressureError;
        
        (* Ortho-Para Catalyst Thermal Management *)
        IF rCatalystBedTemp_K < 45.0 THEN
            bHeaterCmd := TRUE;
        ELSE
            bHeaterCmd := FALSE;
        END_IF;
        
        IF NOT bEnableSys THEN
            iState := 30; (* SHUTDOWN SEQUENCE *)
        END_IF;

    30: (* SHUTDOWN SEQUENCE *)
        bSystemReady := FALSE;
        rCryocoolerCmd_Pct := rCryocoolerCmd_Pct * 0.95; (* Ramp down *)
        IF rCryocoolerCmd_Pct < 1.0 THEN
            rCryocoolerCmd_Pct := 0.0;
            iState := 0;
        END_IF;
        
    99: (* FAULT HANDLING *)
        bSystemReady := FALSE;
        rCryocoolerCmd_Pct := 0.0;
        IF (rFilteredPressure < c_rTargetPressure) AND bEnableSys THEN
            iAlarmCode := 0;
            iState := 0;
        END_IF;

END_CASE;

END_FUNCTION_BLOCK
```"""

filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": code}
    ]
}
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print(f"Saved to {filename}")
