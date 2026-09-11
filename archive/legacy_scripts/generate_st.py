import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Advanced Bio-Synthetic Artificial Retina Photoreceptor Micro-Electrode Array**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., 10,000-channel asynchronous multiplexing, neural-tissue impedance spectroscopy mapping, and localized biphasic charge-balanced stimulation pulses). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_ArtificialRetinaMEA\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Advanced Bio-Synthetic Artificial Retina Photoreceptor Micro-Electrode Array

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_ArtificialRetinaMEA
(* =================================================================================
   Lumina AI Cloud Swarm - Elite Synthetic Data Architect (40+ Years Experience)
   Domain: Advanced Bio-Synthetic Artificial Retina Photoreceptor Micro-Electrode Array
   Module: MEA_MainController
   Description: Manages 10,000-channel asynchronous multiplexing, neural-tissue 
   impedance spectroscopy mapping, and localized biphasic charge-balanced 
   stimulation pulses.
   ================================================================================= *)

VAR_INPUT
    bSystemEnable           : BOOL;     (* Main safety interlock / enable signal for the artificial retina array *)
    bEmergencyStop          : BOOL;     (* Hardware E-stop or safety relay OK signal. FALSE = immediate halt *)
    rAmbientLightLux        : REAL;     (* Measured ambient light intensity (Lux) to adjust baseline stimulation *)
    rRetinalTempC           : REAL;     (* Retinal interface temperature (Deg C) to prevent tissue damage *)
    aElectrodeImpedances    : ARRAY[0..9999] OF REAL; (* Real-time impedance measurements (Ohms) per channel *)
    iActiveChannelSelect    : INT;      (* Index for manual channel interrogation / testing (-1 for auto multiplexing) *)
    rTargetChargeDensity    : REAL;     (* Desired charge density per pulse (uC/cm^2) *)
    bInitiateScan           : BOOL;     (* Trigger mapping scan for impedance spectroscopy *)
END_VAR

VAR_OUTPUT
    bSystemReady            : BOOL;     (* TRUE when system initialized, safe, and ready for continuous pulsing *)
    bTissueFault            : BOOL;     (* TRUE if impedance exceeds safe limits or temp > threshold *)
    rGlobalStimFrequency    : REAL;     (* Calculated global base stimulation frequency (Hz) *)
    aPulseActiveMap         : ARRAY[0..9999] OF BOOL; (* High-speed boolean map indicating active stimulation channels *)
    rAvgImpedance           : REAL;     (* Moving average of array impedance for diagnostic tracking *)
    iActiveFaultCode        : INT;      (* Internal fault code for SCADA/diagnostic interface (0=No fault) *)
    rPowerOutputmW          : REAL;     (* Current calculated power output to the micro-electrode array in milliwatts *)
END_VAR

VAR
    (* Internal State and Timing *)
    iState                  : INT := 0;  (* Main State Machine: 0=Init, 10=SelfTest, 20=Mapping, 30=Active, 99=Fault *)
    tSafetyTimer            : TON;       (* Failsafe watchdog timer *)
    tScanTimer              : TON;       (* Timing for impedance scan dwell times *)
    i                       : INT;       (* Loop index *)
    
    (* Signal Processing and Filtering *)
    rImpedanceSum           : LREAL := 0.0;
    rFilteredLux            : REAL := 0.0;
    rLuxFilterAlpha         : REAL := 0.1; (* Low-pass filter coefficient for ambient light *)
    
    (* Control Logic Parameters *)
    MAX_SAFE_TEMP           : REAL := 39.5; (* Maximum allowable tissue temperature in Deg C *)
    MAX_IMPEDANCE_OHM       : REAL := 150000.0; (* 150 kOhm max safe impedance limit *)
    MIN_IMPEDANCE_OHM       : REAL := 500.0; (* 500 Ohm min limit (indicates short circuit) *)
    
    (* Charge Balancing Registers *)
    aAnodicAccumulator      : ARRAY[0..9999] OF REAL;
    aCathodicAccumulator    : ARRAY[0..9999] OF REAL;
END_VAR

(* === MAIN SAFETY INTERLOCKS === *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bTissueFault := TRUE;
    iActiveFaultCode := 999; (* 999 = Emergency Stop Engaged *)
    rGlobalStimFrequency := 0.0;
    rPowerOutputmW := 0.0;
    FOR i := 0 TO 9999 DO
        aPulseActiveMap[i] := FALSE;
    END_FOR;
    iState := 0;
    RETURN;
END_IF;

IF rRetinalTempC > MAX_SAFE_TEMP THEN
    bTissueFault := TRUE;
    iActiveFaultCode := 101; (* Thermal overload *)
    iState := 99; (* Force fault state *)
END_IF;

(* Continuous Signal Filtering (First-Order Low-Pass) *)
rFilteredLux := (rLuxFilterAlpha * rAmbientLightLux) + ((1.0 - rLuxFilterAlpha) * rFilteredLux);

(* === MAIN STATE MACHINE === *)
CASE iState OF
    0: (* SYSTEM INITIALIZATION & IDLE *)
        bSystemReady := FALSE;
        bTissueFault := FALSE;
        iActiveFaultCode := 0;
        
        IF bSystemEnable THEN
            iState := 10;
        END_IF;

    10: (* HARDWARE SELF-TEST & CAPACITIVE CALIBRATION *)
        tSafetyTimer(IN := TRUE, PT := T#2S);
        
        (* Verify reasonable inputs *)
        IF rTargetChargeDensity <= 0.0 THEN
            iActiveFaultCode := 201; (* Invalid parameter *)
            iState := 99;
        END_IF;

        IF tSafetyTimer.Q AND iActiveFaultCode = 0 THEN
            tSafetyTimer(IN := FALSE);
            iState := 20;
        END_IF;

    20: (* IMPEDANCE SPECTROSCOPY MAPPING *)
        IF bInitiateScan THEN
            rImpedanceSum := 0.0;
            bTissueFault := FALSE;
            
            FOR i := 0 TO 9999 DO
                (* Check per-channel impedance limits *)
                IF aElectrodeImpedances[i] > MAX_IMPEDANCE_OHM OR aElectrodeImpedances[i] < MIN_IMPEDANCE_OHM THEN
                    aPulseActiveMap[i] := FALSE; (* Isolate failed channel *)
                    bTissueFault := TRUE;
                ELSE
                    rImpedanceSum := rImpedanceSum + aElectrodeImpedances[i];
                END_IF;
            END_FOR;
            
            rAvgImpedance := LREAL_TO_REAL(rImpedanceSum / 10000.0);
            
            IF bTissueFault THEN
                iActiveFaultCode := 102; (* Partial or total array impedance failure *)
                iState := 99;
            ELSE
                bSystemReady := TRUE;
                iState := 30;
            END_IF;
        END_IF;

    30: (* ACTIVE ASYNCHRONOUS MULTIPLEXING & STIMULATION *)
        (* Dynamic adaptation of frequency based on filtered ambient light *)
        rGlobalStimFrequency := 10.0 + (rFilteredLux * 0.05);
        IF rGlobalStimFrequency > 250.0 THEN
            rGlobalStimFrequency := 250.0; (* Cap at physiological limit *)
        END_IF;
        
        (* Power calculation (simplified deterministic estimation) *)
        rPowerOutputmW := rAvgImpedance * rGlobalStimFrequency * rTargetChargeDensity * 0.001;

        (* Pulse Generation Logic with basic charge balance check *)
        FOR i := 0 TO 9999 DO
            IF NOT bTissueFault AND (iActiveChannelSelect = -1 OR iActiveChannelSelect = i) THEN
                (* Simulate biphasic charge accumulation tracking *)
                aAnodicAccumulator[i] := aAnodicAccumulator[i] + rTargetChargeDensity;
                aCathodicAccumulator[i] := aCathodicAccumulator[i] + rTargetChargeDensity;
                
                (* Ensure strict charge balance (<1% error tolerance) *)
                IF ABS(aAnodicAccumulator[i] - aCathodicAccumulator[i]) < (rTargetChargeDensity * 0.01) THEN
                    aPulseActiveMap[i] := TRUE;
                ELSE
                    aPulseActiveMap[i] := FALSE; (* Disable channel to prevent DC drift toxicity *)
                END_IF;
            ELSE
                aPulseActiveMap[i] := FALSE;
            END_IF;
        END_FOR;
        
        IF NOT bSystemEnable THEN
            bSystemReady := FALSE;
            iState := 0;
        END_IF;

    99: (* FAULT HANDLING *)
        bSystemReady := FALSE;
        rGlobalStimFrequency := 0.0;
        FOR i := 0 TO 9999 DO
            aPulseActiveMap[i] := FALSE;
        END_FOR;
        
        (* Require manual reset via bSystemEnable cycle *)
        IF NOT bSystemEnable THEN
            iActiveFaultCode := 0;
            bTissueFault := FALSE;
            iState := 0;
        END_IF;

END_CASE;

END_FUNCTION_BLOCK
```"""

import os
os.makedirs("data/swarm_raw", exist_ok=True)
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
print(f"Saved to {filename}")
