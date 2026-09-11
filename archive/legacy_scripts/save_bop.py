import os
import json
import uuid

os.makedirs('data/swarm_raw', exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Industrial Scale Deep-Sea Sub-Salt Oil Well Blowout Preventer (BOP)**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., 15,000 psi triple-ram hydraulic accumulator rapid discharge, acoustic telemetry dead-man switch auto-shear sequencing, and annular seal dynamic elastomer extrusion compensation). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_SubseaBOP\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Industrial Scale Deep-Sea Sub-Salt Oil Well Blowout Preventer (BOP)

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_SubseaBOP
(* 
   Ultra-High Reliability Deep-Sea Sub-Salt Oil Well Blowout Preventer (BOP) Control Logic
   Design: 15,000 psi triple-ram hydraulic accumulator rapid discharge, 
           acoustic telemetry dead-man switch auto-shear sequencing,
           annular seal dynamic elastomer extrusion compensation.
*)
VAR_INPUT
    (* Mandatory Physical Inputs *)
    bSystemEnable           : BOOL;     (* Overall system enable signal *)
    bAcousticDeadManActive  : BOOL;     (* Acoustic telemetry dead-man switch signal *)
    bManualShearCommand     : BOOL;     (* Surface operator manual shear override *)
    rWellborePressure_psi   : REAL;     (* Downhole wellbore pressure in psi *)
    rAccumulatorVolume_L    : REAL;     (* Hydraulic accumulator volume in Liters *)
    rAnnularSealTemp_C      : REAL;     (* Annular elastomer seal temperature in Celsius *)
    rAmbientSeawaterTemp_C  : REAL;     (* Ambient seawater temperature at depth *)
    bPowerBusOK             : BOOL;     (* Dual-redundant subsea power bus status *)
END_VAR
VAR_OUTPUT
    (* Mandatory Physical Outputs *)
    bBOP_SystemReady        : BOOL;     (* BOP operational readiness state *)
    bShearRamTrigger        : BOOL;     (* Fast-acting blind shear ram trigger *)
    bAnnularSealEngage      : BOOL;     (* Variable bore annular seal activation *)
    rHydraulicDischargeCmd  : REAL;     (* Modulated hydraulic flow command 0.0 to 1.0 *)
    bCriticalAlarm          : BOOL;     (* High-priority surface alarm *)
    iSequenceStep           : INT;      (* Current execution sequence step *)
END_VAR
VAR
    (* Internal State Variables *)
    iState                  : INT := 0; (* Primary State Machine Variable *)
    tShearTimer             : TON;      (* Dead-man switch debounce / delay timer *)
    tSealTimer              : TON;      (* Annular seal extrusion delay timer *)
    rFilteredPressure       : REAL;     (* Exponential moving average of wellbore pressure *)
    rAlpha                  : REAL := 0.05; (* Filter coefficient for sensor noise *)
    bKicksDetected          : BOOL := FALSE;
    bEmergencySeqLatched    : BOOL := FALSE;
END_VAR

(* === MAIN LOGIC === *)
(* 1. Sensor Noise Filtering - EMA on Wellbore Pressure *)
rFilteredPressure := (rAlpha * rWellborePressure_psi) + ((1.0 - rAlpha) * rFilteredPressure);

(* 2. Core Safety Interlocks & Power Monitoring *)
IF NOT bPowerBusOK THEN
    bBOP_SystemReady := FALSE;
    bCriticalAlarm := TRUE;
    (* Subsea systems typically fail-safe, but latching is required *)
    IF NOT bAcousticDeadManActive THEN
        bEmergencySeqLatched := TRUE;
    END_IF;
ELSE
    bCriticalAlarm := FALSE;
END_IF;

(* 3. Blowout Kick Detection Algorithm (15k psi limit) *)
IF rFilteredPressure > 14500.0 THEN
    bKicksDetected := TRUE;
    bCriticalAlarm := TRUE;
END_IF;

(* 4. State Machine for BOP Auto-Shear and Annular Seal Sequencing *)
CASE iState OF
    0: (* IDLE & SYSTEM CHECKS *)
        IF bSystemEnable AND bPowerBusOK AND (rAccumulatorVolume_L > 200.0) THEN
            iState := 10;
            bBOP_SystemReady := TRUE;
            bAnnularSealEngage := FALSE;
            bShearRamTrigger := FALSE;
            rHydraulicDischargeCmd := 0.0;
        ELSE
            bBOP_SystemReady := FALSE;
        END_IF;

        (* Immediate transition to emergency if manual or dead-man override *)
        IF bManualShearCommand OR bEmergencySeqLatched OR (bKicksDetected AND NOT bAcousticDeadManActive) THEN
            iState := 99; (* JUMP TO EMERGENCY *)
        END_IF;

    10: (* ACTIVE MONITORING *)
        iSequenceStep := 1;
        
        (* Monitor for pressure kicks or deadman loss *)
        IF bManualShearCommand OR bEmergencySeqLatched THEN
            iState := 99;
        ELSIF bKicksDetected THEN
            iState := 20; (* Initial annular seal engagement to control kick *)
        END_IF;

    20: (* ANNULAR SEAL DEPLOYMENT *)
        iSequenceStep := 2;
        bAnnularSealEngage := TRUE;
        (* Compensate hydraulic pressure based on elastomer temperature differential *)
        IF rAnnularSealTemp_C > 80.0 THEN
            rHydraulicDischargeCmd := 0.75; (* Higher viscosity/expansion, lower cmd *)
        ELSE
            rHydraulicDischargeCmd := 1.0;  (* Max pressure for cold extrusion *)
        END_IF;

        tSealTimer(IN := TRUE, PT := T#15S);
        IF tSealTimer.Q THEN
            tSealTimer(IN := FALSE);
            (* Evaluate if seal held the pressure *)
            IF rFilteredPressure > 14800.0 THEN
                iState := 99; (* Seal failed, initiate blind shear *)
            ELSE
                iState := 30; (* Kick contained *)
            END_IF;
        END_IF;

    30: (* KICK CONTAINED - HOLD POSITION *)
        iSequenceStep := 3;
        rHydraulicDischargeCmd := 0.2; (* Maintenance pressure *)
        IF NOT bKicksDetected THEN
            iState := 10; (* Return to monitoring *)
        END_IF;

    99: (* CRITICAL EMERGENCY - BLIND SHEAR RAM DEPLOYMENT *)
        iSequenceStep := 9;
        bCriticalAlarm := TRUE;
        bBOP_SystemReady := FALSE;
        
        (* Rapid discharge sequence from triple-ram accumulator *)
        rHydraulicDischargeCmd := 1.0; 
        
        (* Sequence timing for shear rams to clear pipe *)
        tShearTimer(IN := TRUE, PT := T#3S);
        IF tShearTimer.Q THEN
            bShearRamTrigger := TRUE;
            bAnnularSealEngage := TRUE; (* Backup sealing *)
            tShearTimer(IN := FALSE);
            iState := 100;
        END_IF;

    100: (* SECURED & LOCKED *)
        iSequenceStep := 10;
        rHydraulicDischargeCmd := 0.0;
        (* End of sequence. Requires surface intervention to reset. *)
        IF NOT bSystemEnable THEN
            bEmergencySeqLatched := FALSE;
            bKicksDetected := FALSE;
            bShearRamTrigger := FALSE;
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
