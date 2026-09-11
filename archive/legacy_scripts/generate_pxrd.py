import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Advanced Pharmaceutical Powder X-Ray Diffraction (PXRD) Analyzer**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Goniometer theta/2-theta stepping (micro-degree precision), copper K-alpha X-ray tube high-voltage tracking, and scintillation detector dead-time active correction). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_PXRD_Analyzer\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Advanced Pharmaceutical Powder X-Ray Diffraction (PXRD) Analyzer

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_PXRD_Analyzer
VAR_INPUT
    bEnable             : BOOL;     (* System enable signal for the PXRD analysis sequence *)
    bEmergencyStop      : BOOL;     (* Safety relay OK signal (TRUE = Safe, FALSE = E-STOP) *)
    rThetaPosition      : LREAL;    (* Goniometer actual theta angle feedback in degrees *)
    rXRayTubeVoltage    : REAL;     (* X-Ray Tube actual high voltage feedback in kV *)
    rXRayTubeCurrent    : REAL;     (* X-Ray Tube actual emission current feedback in mA *)
    udiRawDetectorCounts: UDINT;    (* Raw counts accumulated from the scintillation detector *)
    tDwellTime          : TIME;     (* Target dwell time per step for data collection *)
END_VAR
VAR_OUTPUT
    bSystemReady        : BOOL;     (* System ready status, TRUE when initialized and idle *)
    rThetaTarget        : LREAL;    (* Goniometer target theta position command in degrees *)
    rCorrectedIntensity : REAL;     (* Dead-time corrected X-ray intensity in Counts Per Second (CPS) *)
    bHV_Enable          : BOOL;     (* Command to enable High Voltage generator for the X-Ray tube *)
    rHV_TargetVoltage   : REAL;     (* Target High Voltage setpoint (kV) for the generator *)
    rHV_TargetCurrent   : REAL;     (* Target emission current setpoint (mA) for the generator *)
    bAlarm              : BOOL;     (* Fault alarm output indicating a system error or interlock trip *)
END_VAR
VAR
    iState              : INT := 0; (* Internal state machine variable *)
    tDwellTimer         : TON;      (* Timer for step dwell time during scan *)
    rDeadTimeTau        : REAL := 2.0E-6; (* Scintillation detector dead time constant in seconds (2 microseconds) *)
    rRawCountRate       : REAL;     (* Intermediate calculated raw count rate (CPS) *)
    rThetaStart         : LREAL := 2.0;   (* Default starting angle (2-Theta) *)
    rThetaStop          : LREAL := 60.0;  (* Default stopping angle (2-Theta) *)
    rThetaStep          : LREAL := 0.01;  (* Default step size (2-Theta) *)
    rTolerance          : LREAL := 0.001; (* Positioning tolerance for the goniometer *)
    bScanComplete       : BOOL;     (* Flag indicating the current scan is finished *)
END_VAR

(* === MAIN SAFETY AND INTERLOCK LOGIC === *)
(* Ensure safety interlocks are met before proceeding *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bHV_Enable := FALSE;
    rHV_TargetVoltage := 0.0;
    rHV_TargetCurrent := 0.0;
    bAlarm := TRUE;
    iState := 99; (* Transition immediately to FAULT state *)
    RETURN;
END_IF;

(* === PXRD AUTOMATION STATE MACHINE === *)
CASE iState OF
    0: (* IDLE - Await Enable Signal *)
        bSystemReady := TRUE;
        bScanComplete := FALSE;
        bAlarm := FALSE;
        bHV_Enable := FALSE;
        IF bEnable THEN
            bSystemReady := FALSE;
            iState := 10;
        END_IF;

    10: (* INIT_HV - Initialize High Voltage for Copper K-alpha Source *)
        bHV_Enable := TRUE;
        rHV_TargetVoltage := 40.0; (* 40 kV standard operation *)
        rHV_TargetCurrent := 40.0; (* 40 mA standard operation *)
        
        (* Check if HV has reached setpoint within 1% tolerance *)
        IF (ABS(rXRayTubeVoltage - rHV_TargetVoltage) < 0.4) AND (ABS(rXRayTubeCurrent - rHV_TargetCurrent) < 0.4) THEN
            iState := 20;
        END_IF;
        
        (* If disabled during HV ramp, shutdown gracefully *)
        IF NOT bEnable THEN
            iState := 60;
        END_IF;

    20: (* GOTO_START - Move Goniometer to Starting Angle *)
        rThetaTarget := rThetaStart;
        IF ABS(rThetaPosition - rThetaStart) <= rTolerance THEN
            iState := 30;
        END_IF;

    30: (* SCAN_STEP - Dwell and Count *)
        tDwellTimer(IN := TRUE, PT := tDwellTime);
        
        IF tDwellTimer.Q THEN
            (* Calculate raw count rate *)
            rRawCountRate := UDINT_TO_REAL(udiRawDetectorCounts) / (TIME_TO_REAL(tDwellTime) / 1000.0);
            
            (* Perform Dead-Time Active Correction using the non-paralyzable model: N = n / (1 - n * tau) *)
            IF (1.0 - (rRawCountRate * rDeadTimeTau)) > 0.0 THEN
                rCorrectedIntensity := rRawCountRate / (1.0 - (rRawCountRate * rDeadTimeTau));
            ELSE
                rCorrectedIntensity := 0.0; (* Saturation fault condition *)
                iState := 99; 
            END_IF;

            tDwellTimer(IN := FALSE);
            iState := 40;
        END_IF;

    40: (* NEXT_STEP - Increment Goniometer Angle *)
        rThetaTarget := rThetaTarget + rThetaStep;
        
        IF rThetaTarget > rThetaStop THEN
            bScanComplete := TRUE;
            iState := 60; (* Scan finished, transition to shutdown *)
        ELSE
            (* Wait until goniometer reaches the new step position before acquiring next point *)
            IF ABS(rThetaPosition - rThetaTarget) <= rTolerance THEN
                iState := 30;
            END_IF;
        END_IF;

    60: (* SHUTDOWN - Ramp down HV and reset *)
        bHV_Enable := FALSE;
        rHV_TargetVoltage := 0.0;
        rHV_TargetCurrent := 0.0;
        
        IF (rXRayTubeVoltage < 1.0) AND (rXRayTubeCurrent < 1.0) THEN
            IF NOT bEnable THEN
                iState := 0;
            END_IF;
        END_IF;

    99: (* FAULT - System Error Handling *)
        bSystemReady := FALSE;
        bHV_Enable := FALSE;
        rHV_TargetVoltage := 0.0;
        rHV_TargetCurrent := 0.0;
        bAlarm := TRUE;
        
        IF NOT bEnable AND bEmergencyStop THEN
            bAlarm := FALSE;
            iState := 0;
        END_IF;

END_CASE;

END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump({"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}, f, ensure_ascii=False)

print(f"Saved to {filename}")
