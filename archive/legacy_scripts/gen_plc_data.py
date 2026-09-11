import os, json, uuid

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Next-Gen Bio-Pharmaceutical Monoclonal Antibody (mAb) Continuous Chromatography**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Simulated moving bed (SMB) column switching synchronization, UV absorbance breakthrough peak detection, and gradient elution buffer blending). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_mAb_Chromatography\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Next-Gen Bio-Pharmaceutical Monoclonal Antibody (mAb) Continuous Chromatography

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_ContinuousChromatographySMB
VAR_INPUT
    (* Required: at least 4-8 physical inputs with types and comments *)
    bEnable               : BOOL;   (* System enable signal for the SMB process *)
    bEmergencyStop        : BOOL;   (* Safety relay OK signal - active high means safe *)
    rUV_Absorbance        : REAL;   (* UV absorbance at column outlet (AU) *)
    rFeedFlowRate         : REAL;   (* mAb feed flow rate measurement (L/min) *)
    rBufferConductivity   : REAL;   (* Elution buffer conductivity (mS/cm) *)
    rColumnPressure       : REAL;   (* Differential pressure across SMB column (bar) *)
END_VAR
VAR_OUTPUT
    (* Required: at least 3-6 physical outputs with types and comments *)
    bSystemReady          : BOOL;   (* System ready status indicating safe operation *)
    rPumpSpeedTarget      : REAL;   (* Target speed for feed and eluent pumps (0-100%) *)
    bAlarm                : BOOL;   (* Fault alarm output - high when system faults *)
    iActiveColumn         : INT;    (* Currently active SMB column (1-4) *)
    bPeakDetected         : BOOL;   (* Breakthrough product peak detection flag *)
END_VAR
VAR
    (* Internal state variables *)
    iState                : INT := 0; 
    tCycleTimer           : TON;
    rFilteredUV           : REAL := 0.0;
    rPrevUV               : REAL := 0.0;
    rUV_Derivative        : REAL := 0.0;
    tSampleTimer          : TON;
    rMaxPressureLimit     : REAL := 5.5; (* Max allowed DP in bar *)
    iCycleCount           : INT := 0;
END_VAR

(* === MULTI-LAYERED SAFETY INTERLOCKS === *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    rPumpSpeedTarget := 0.0;
    bAlarm := TRUE;
    iState := 999; (* Transition to FAULT state *)
    RETURN;
END_IF;

IF rColumnPressure > rMaxPressureLimit THEN
    bSystemReady := FALSE;
    rPumpSpeedTarget := 0.0;
    bAlarm := TRUE;
    iState := 999; (* Overpressure FAULT *)
    RETURN;
END_IF;

(* === SENSOR NOISE FILTERING === *)
(* Implement a simple exponential moving average filter for UV absorbance *)
rFilteredUV := (0.1 * rUV_Absorbance) + (0.9 * rFilteredUV);

(* === BREAKTHROUGH PEAK DETECTION === *)
tSampleTimer(IN := TRUE, PT := T#100MS);
IF tSampleTimer.Q THEN
    rUV_Derivative := (rFilteredUV - rPrevUV) / 0.1;
    rPrevUV := rFilteredUV;
    tSampleTimer(IN := FALSE);
END_IF;

IF (rFilteredUV > 1.2) AND (rUV_Derivative < -0.05) THEN
    bPeakDetected := TRUE;
ELSE
    bPeakDetected := FALSE;
END_IF;

(* === MAIN CONTINUOUS CHROMATOGRAPHY STATE MACHINE === *)
CASE iState OF
    0: (* IDLE *)
        bSystemReady := TRUE;
        rPumpSpeedTarget := 0.0;
        bAlarm := FALSE;
        iActiveColumn := 1;
        IF bEnable THEN
            iState := 10;
        END_IF;

    10: (* EQUILIBRATION *)
        bSystemReady := FALSE;
        rPumpSpeedTarget := 30.0; (* 30% nominal flow for equilibration *)
        tCycleTimer(IN := TRUE, PT := T#5M);
        IF tCycleTimer.Q AND (rBufferConductivity > 15.0) AND (rBufferConductivity < 20.0) THEN
            tCycleTimer(IN := FALSE);
            iState := 20;
        END_IF;

    20: (* LOAD *)
        rPumpSpeedTarget := 75.0; (* Load mAb feed *)
        IF bPeakDetected THEN
            (* Breakthrough reached, advance column *)
            iState := 30;
        END_IF;

    30: (* ELUTE & COLUMN SWITCHING SYNCHRONIZATION *)
        rPumpSpeedTarget := 50.0;
        tCycleTimer(IN := TRUE, PT := T#2M);
        IF tCycleTimer.Q THEN
            tCycleTimer(IN := FALSE);
            iCycleCount := iCycleCount + 1;
            
            (* Rotate active column in simulated moving bed (1 to 4) *)
            iActiveColumn := iActiveColumn + 1;
            IF iActiveColumn > 4 THEN
                iActiveColumn := 1;
            END_IF;
            
            iState := 40;
        END_IF;

    40: (* REGENERATE *)
        rPumpSpeedTarget := 100.0; (* Max flow for CIP / Regeneration *)
        tCycleTimer(IN := TRUE, PT := T#10M);
        IF tCycleTimer.Q THEN
            tCycleTimer(IN := FALSE);
            IF NOT bEnable THEN
                iState := 0;
            ELSE
                iState := 10; (* Start next cycle *)
            END_IF;
        END_IF;

    999: (* FAULT HANDLING *)
        rPumpSpeedTarget := 0.0;
        IF bEnable = FALSE AND bEmergencyStop = TRUE AND rColumnPressure < (rMaxPressureLimit - 1.0) THEN
            bAlarm := FALSE;
            iState := 0; (* Reset fault when enable is dropped and conditions safe *)
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

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print(f"Saved to {filename}")
