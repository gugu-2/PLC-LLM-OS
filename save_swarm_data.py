import json, uuid, os

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Advanced Synchrotron Light Source Electron Storage Ring**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., 3-GeV bending magnet power supply ramping, ultra-high vacuum (UHV) non-evaporable getter (NEG) activation, and beam position monitor (BPM) fast orbit feedback). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_SynchrotronStorageRing\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Advanced Synchrotron Light Source Electron Storage Ring

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_StorageRingOrbitFeedback
VAR_INPUT
    bEnable                 : BOOL;     (* Fast orbit feedback system enable *)
    bBeamDumpInterlock      : BOOL;     (* MPS beam dump interlock status (TRUE = OK) *)
    rBeamCurrent_mA         : REAL;     (* Stored electron beam current in mA *)
    arBPM_X_um              : ARRAY[1..120] OF REAL; (* Horizontal Beam Position Monitor readings (um) *)
    arBPM_Y_um              : ARRAY[1..120] OF REAL; (* Vertical Beam Position Monitor readings (um) *)
    rRfCavityVoltage_kV     : REAL;     (* RF cavity gap voltage (kV) *)
    bUHV_ValveStatus        : BOOL;     (* Ultra-High Vacuum sector valves status (TRUE = OPEN) *)
END_VAR
VAR_OUTPUT
    bSystemReady            : BOOL;     (* FOFB system ready and healthy *)
    arCorrector_X_urad      : ARRAY[1..80] OF REAL; (* Horizontal fast corrector magnet setpoints (urad) *)
    arCorrector_Y_urad      : ARRAY[1..80] OF REAL; (* Vertical fast corrector magnet setpoints (urad) *)
    bOrbitStable            : BOOL;     (* True if orbit RMS is within tolerance *)
    bAlarm                  : BOOL;     (* FOFB general fault alarm *)
    iErrorCode              : INT;      (* Error code for diagnostics *)
END_VAR
VAR
    iState                  : INT := 0;
    i                       : INT;
    rRmsX                   : REAL;
    rRmsY                   : REAL;
    rSumSquareX             : REAL := 0.0;
    rSumSquareY             : REAL := 0.0;
    tSettleTimer            : TON;
    rMaxPosTol_um           : REAL := 5.0; (* 5 micrometer RMS tolerance *)
    
    (* PI Controller internal states for each plane *)
    arIntSum_X              : ARRAY[1..80] OF REAL;
    arIntSum_Y              : ARRAY[1..80] OF REAL;
    rKp                     : REAL := 0.5;
    rKi                     : REAL := 0.01;
END_VAR

(* === MAIN LOGIC === *)
(* Global Safety and Interlock Check *)
IF NOT bBeamDumpInterlock OR NOT bUHV_ValveStatus THEN
    bSystemReady := FALSE;
    bOrbitStable := FALSE;
    bAlarm := TRUE;
    iErrorCode := 1001; (* Critical interlock tripped *)
    
    (* Zero all corrector strengths for safety *)
    FOR i := 1 TO 80 DO
        arCorrector_X_urad[i] := 0.0;
        arCorrector_Y_urad[i] := 0.0;
        arIntSum_X[i] := 0.0;
        arIntSum_Y[i] := 0.0;
    END_FOR;
    
    iState := 0;
    RETURN;
END_IF;

(* Main State Machine *)
CASE iState OF
    0: (* IDLE / INITIALIZATION *)
        bSystemReady := FALSE;
        bOrbitStable := FALSE;
        bAlarm := FALSE;
        iErrorCode := 0;
        
        IF bEnable AND (rBeamCurrent_mA > 5.0) AND (rRfCavityVoltage_kV > 2500.0) THEN
            iState := 10;
        END_IF;

    10: (* CALCULATION & CORRECTION *)
        bSystemReady := TRUE;
        rSumSquareX := 0.0;
        rSumSquareY := 0.0;
        
        (* Calculate RMS Orbit Distortion *)
        FOR i := 1 TO 120 DO
            rSumSquareX := rSumSquareX + (arBPM_X_um[i] * arBPM_X_um[i]);
            rSumSquareY := rSumSquareY + (arBPM_Y_um[i] * arBPM_Y_um[i]);
        END_FOR;
        
        rRmsX := SQRT(rSumSquareX / 120.0);
        rRmsY := SQRT(rSumSquareY / 120.0);
        
        (* Apply SVD-based inverted response matrix logic (simplified for ST abstraction) 
           Here we simulate the PI loop update for fast corrector magnets *)
        FOR i := 1 TO 80 DO
            (* Pseudo-feedback integrating local BPMs to correctors *)
            arIntSum_X[i] := arIntSum_X[i] + (arBPM_X_um[i] * rKi);
            arIntSum_Y[i] := arIntSum_Y[i] + (arBPM_Y_um[i] * rKi);
            
            arCorrector_X_urad[i] := -(rKp * arBPM_X_um[i]) - arIntSum_X[i];
            arCorrector_Y_urad[i] := -(rKp * arBPM_Y_um[i]) - arIntSum_Y[i];
            
            (* Anti-windup clamping *)
            IF arCorrector_X_urad[i] > 100.0 THEN arCorrector_X_urad[i] := 100.0; arIntSum_X[i] := arIntSum_X[i] - (arBPM_X_um[i] * rKi); END_IF;
            IF arCorrector_X_urad[i] < -100.0 THEN arCorrector_X_urad[i] := -100.0; arIntSum_X[i] := arIntSum_X[i] - (arBPM_X_um[i] * rKi); END_IF;
            
            IF arCorrector_Y_urad[i] > 100.0 THEN arCorrector_Y_urad[i] := 100.0; arIntSum_Y[i] := arIntSum_Y[i] - (arBPM_Y_um[i] * rKi); END_IF;
            IF arCorrector_Y_urad[i] < -100.0 THEN arCorrector_Y_urad[i] := -100.0; arIntSum_Y[i] := arIntSum_Y[i] - (arBPM_Y_um[i] * rKi); END_IF;
        END_FOR;
        
        IF (rRmsX <= rMaxPosTol_um) AND (rRmsY <= rMaxPosTol_um) THEN
            tSettleTimer(IN := TRUE, PT := T#2S);
            IF tSettleTimer.Q THEN
                tSettleTimer(IN := FALSE);
                bOrbitStable := TRUE;
                iState := 20;
            END_IF;
        ELSE
            tSettleTimer(IN := FALSE);
            bOrbitStable := FALSE;
        END_IF;
        
        IF NOT bEnable THEN
            tSettleTimer(IN := FALSE);
            iState := 0;
        END_IF;

    20: (* STABLE OPERATION *)
        bSystemReady := TRUE;
        bOrbitStable := TRUE;
        
        (* Continuous monitoring without heavy correction *)
        IF (arBPM_X_um[1] > 20.0) OR (arBPM_Y_um[1] > 20.0) THEN (* Trigger if glitch detected *)
            bOrbitStable := FALSE;
            tSettleTimer(IN := FALSE);
            iState := 10;
        END_IF;
        
        IF NOT bEnable THEN
            iState := 0;
        END_IF;

    ELSE
        iState := 0;
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
