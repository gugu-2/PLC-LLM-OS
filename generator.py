import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Advanced Biomedical Proton Therapy Synchrotron Beamline**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., 250 MeV proton extraction septum magnet ramping, scanning dipole raster precise dose delivery, and real-time Bragg peak tissue depth modulation). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_ProtonTherapySynchrotron\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Advanced Biomedical Proton Therapy Synchrotron Beamline

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_ProtonTherapySynchrotron
VAR_INPUT
    bEnable                 : BOOL;     (* System master enable *)
    bEmergencyStopOk        : BOOL;     (* Safety relay loop closed and OK *)
    rBeamEnergySetpt        : REAL;     (* Target proton beam energy in MeV (e.g., 70 - 250 MeV) *)
    rDoseRateSetpt          : REAL;     (* Desired dose rate in Gy/min *)
    rExtractionSeptumCur    : REAL;     (* Septum magnet current feedback in Amps *)
    rScanningDipoleXFB      : REAL;     (* Raster scanning dipole X-axis position feedback (mm) *)
    rScanningDipoleYFB      : REAL;     (* Raster scanning dipole Y-axis position feedback (mm) *)
    bPatientAlignmentOk     : BOOL;     (* Patient 6D couch positioning verification *)
END_VAR
VAR_OUTPUT
    bSystemReady            : BOOL;     (* Beamline ready for extraction and delivery *)
    bBeamActive             : BOOL;     (* Proton beam is currently active and extracting *)
    rSeptumCurrentCmd       : REAL;     (* Command signal to extraction septum magnet power supply *)
    rDipoleXCurrentCmd      : REAL;     (* X-axis dipole scanning magnet command *)
    rDipoleYCurrentCmd      : REAL;     (* Y-axis dipole scanning magnet command *)
    bDoseDelivered          : BOOL;     (* Target accumulated dose achieved *)
    bSafetyInterlockTrip    : BOOL;     (* Critical safety violation detected, beam aborted *)
    iErrorCode              : INT;      (* Diagnostics error code for HMI/SCADA *)
END_VAR
VAR
    iState                  : INT := 0; (* Main state machine step *)
    tStartupDelay           : TON;
    tDoseTimer              : TON;
    rAccumulatedDose        : REAL := 0.0;
    rSeptumError            : REAL := 0.0;
    rSeptumIntegral         : REAL := 0.0;
    rSeptumKp               : REAL := 0.85;
    rSeptumKi               : REAL := 0.12;
    rMaxSeptumCurrent       : REAL := 5000.0; (* Max 5kA *)
    bFaultActive            : BOOL := FALSE;
END_VAR

(* === MAIN LOGIC === *)
(* Real-time safety interlock evaluation - 1ms deterministic execution *)
IF NOT bEmergencyStopOk OR NOT bPatientAlignmentOk THEN
    bFaultActive := TRUE;
    bSystemReady := FALSE;
    bBeamActive := FALSE;
    bSafetyInterlockTrip := TRUE;
    rSeptumCurrentCmd := 0.0;
    rDipoleXCurrentCmd := 0.0;
    rDipoleYCurrentCmd := 0.0;
    iState := 999; (* Transition to FAULT state *)
    IF NOT bEmergencyStopOk THEN
        iErrorCode := 1001; (* E-Stop Pressed or Loop Open *)
    ELSE
        iErrorCode := 1002; (* Patient Alignment Lost During Treatment *)
    END_IF;
    RETURN;
END_IF;

CASE iState OF
    0: (* IDLE & INITIALIZATION *)
        bSystemReady := FALSE;
        bBeamActive := FALSE;
        bSafetyInterlockTrip := FALSE;
        bDoseDelivered := FALSE;
        rAccumulatedDose := 0.0;
        
        IF bEnable AND NOT bFaultActive THEN
            iState := 10;
        END_IF;

    10: (* WARMUP & BEAM ENERGY CONFIGURATION *)
        (* Simulate setting up the synchrotron ring for desired energy *)
        tStartupDelay(IN := TRUE, PT := T#2S);
        IF tStartupDelay.Q THEN
            tStartupDelay(IN := FALSE);
            iState := 20;
        END_IF;

    20: (* SEPTUM MAGNET RAMPING PID CONTROL *)
        (* Closed-loop control of the extraction septum magnet *)
        rSeptumError := (rBeamEnergySetpt * 15.4) - rExtractionSeptumCur; (* 15.4 A/MeV heuristic *)
        rSeptumIntegral := rSeptumIntegral + rSeptumError;
        
        (* Anti-windup *)
        IF rSeptumIntegral > 1000.0 THEN rSeptumIntegral := 1000.0; END_IF;
        IF rSeptumIntegral < -1000.0 THEN rSeptumIntegral := -1000.0; END_IF;
        
        rSeptumCurrentCmd := (rSeptumKp * rSeptumError) + (rSeptumKi * rSeptumIntegral);
        
        (* Saturation limits *)
        IF rSeptumCurrentCmd > rMaxSeptumCurrent THEN
            rSeptumCurrentCmd := rMaxSeptumCurrent;
        ELSIF rSeptumCurrentCmd < 0.0 THEN
            rSeptumCurrentCmd := 0.0;
        END_IF;
        
        (* Check if septum current is within 0.1% tolerance *)
        IF ABS(rSeptumError) < 5.0 THEN
            bSystemReady := TRUE;
            iState := 30;
        END_IF;

    30: (* BEAM EXTRACTION & DOSE DELIVERY *)
        bBeamActive := TRUE;
        
        (* Raster scanning logic - simplified spiral or raster pattern simulated by dose time *)
        rDipoleXCurrentCmd := rScanningDipoleXFB + 0.1; (* Increment scan X *)
        IF rDipoleXCurrentCmd > 100.0 THEN rDipoleXCurrentCmd := -100.0; END_IF;
        
        rDipoleYCurrentCmd := rScanningDipoleYFB + 0.05; (* Increment scan Y *)
        IF rDipoleYCurrentCmd > 100.0 THEN rDipoleYCurrentCmd := -100.0; END_IF;
        
        (* Dose accumulation model *)
        rAccumulatedDose := rAccumulatedDose + (rDoseRateSetpt / 60000.0); (* Per ms integration *)
        
        IF rAccumulatedDose >= 2.0 THEN (* Target 2.0 Gy per fraction *)
            bDoseDelivered := TRUE;
            bBeamActive := FALSE;
            rSeptumCurrentCmd := 0.0;
            iState := 40;
        END_IF;

    40: (* COMPLETE / POST-IRRADIATION VERIFICATION *)
        bSystemReady := FALSE;
        IF NOT bEnable THEN
            iState := 0; (* Reset for next fraction *)
        END_IF;
        
    999: (* FAULT RECOVERY *)
        bSystemReady := FALSE;
        bBeamActive := FALSE;
        IF NOT bEnable AND NOT bSafetyInterlockTrip THEN
            bFaultActive := FALSE;
            iErrorCode := 0;
            iState := 0;
        END_IF;

END_CASE;

END_FUNCTION_BLOCK
```"""

import os
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
