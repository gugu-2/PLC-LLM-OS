import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Deep-Space Asteroid Mining Optical Sorting Centrifuge**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Zero-gravity triboelectric regolith charging, multi-spectral laser induced breakdown spectroscopy (LIBS) target gating, and high-RPM spin stabilization bearing levitation). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   prompt = "<copy this exact user prompt here>"
   code = "```iec-st\\nFUNCTION_BLOCK FB_AsteroidSortingCentrifuge\\n//...\\nEND_FUNCTION_BLOCK\\n```"
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
6. REPLY with: EVOLUTION COMPLETE: Deep-Space Asteroid Mining Optical Sorting Centrifuge

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_AsteroidSortingCentrifuge
VAR_INPUT
    bSystemEnable     : BOOL;  (* System enable signal for zero-G centrifuge *)
    bEmergencyStop    : BOOL;  (* Safety relay OK signal; TRUE = Safe, FALSE = E-STOP *)
    rCentrifugeRPM    : REAL;  (* Current feedback from magnetic levitation bearings (RPM) *)
    rRegolithMassFlow : REAL;  (* Incoming asteroid regolith mass flow rate (kg/s) *)
    rSpectralScore    : REAL;  (* Multi-spectral LIBS target signature (0.0 - 1.0) *)
    bTriboChargeReady : BOOL;  (* Triboelectric charging field operational and stable *)
END_VAR
VAR_OUTPUT
    bSystemReady         : BOOL;  (* Centrifuge operational, spin-stabilized, and ready for feed *)
    rMagneticGateControl : REAL;  (* Deflection field intensity (T) for optical sorting *)
    rTargetRPM           : REAL;  (* Target RPM speed setpoint to mag-lev drive controller *)
    bParticleReject      : BOOL;  (* Trigger pneumatic/plasma reject gate for slag material *)
    bAlarm               : BOOL;  (* Critical fault active (e.g., imbalance, sensor loss) *)
END_VAR
VAR
    iState               : INT := 0; 
    tStabilizationTimer  : TON;
    tGatingTimer         : TON;
    rLastError           : REAL := 0.0;
    rIntegral            : REAL := 0.0;
    rDerivative          : REAL := 0.0;
    rKp                  : REAL := 2.5;
    rKi                  : REAL := 0.1;
    rKd                  : REAL := 0.05;
    rError               : REAL := 0.0;
    rNominalSpeed        : REAL := 15000.0; (* 15k RPM for micro-g separation *)
    rThresholdScore      : REAL := 0.85;    (* LIBS threshold for precious metals *)
END_VAR

(* === MAIN LOGIC === *)
(* Emergency Stop Interlock *)
IF NOT bEmergencyStop THEN
    bSystemReady         := FALSE;
    bParticleReject      := FALSE;
    rTargetRPM           := 0.0;
    rMagneticGateControl := 0.0;
    bAlarm               := TRUE;
    iState               := 99; (* Fault state *)
    RETURN;
END_IF;

(* State Machine for Centrifuge Sequence *)
CASE iState OF
    0: (* IDLE & INITIALIZATION *)
        bSystemReady := FALSE;
        bAlarm := FALSE;
        rTargetRPM := 0.0;
        IF bSystemEnable AND bTriboChargeReady THEN
            iState := 10;
        END_IF;

    10: (* SPIN-UP SEQUENCE *)
        rTargetRPM := rNominalSpeed;
        rError := rTargetRPM - rCentrifugeRPM;
        
        (* Simple PID execution for spin stability *)
        rIntegral := rIntegral + rError;
        rDerivative := rError - rLastError;
        rLastError := rError;
        
        IF (ABS(rError) < 50.0) THEN
            tStabilizationTimer(IN := TRUE, PT := T#15S);
            IF tStabilizationTimer.Q THEN
                tStabilizationTimer(IN := FALSE);
                iState := 20;
            END_IF;
        ELSE
            tStabilizationTimer(IN := FALSE);
        END_IF;

    20: (* STEADY-STATE SORTING *)
        bSystemReady := TRUE;
        
        (* Maintain speed based on incoming mass flow disturbance *)
        rTargetRPM := rNominalSpeed + (rRegolithMassFlow * 12.5);
        
        (* Multi-Spectral LIBS Gating Logic *)
        IF rSpectralScore >= rThresholdScore THEN
            (* Target identified - activate magnetic deflection field *)
            rMagneticGateControl := 5.5; (* 5.5 Tesla deflection *)
            bParticleReject := FALSE;
        ELSE
            (* Slag/gangue material - trigger reject *)
            rMagneticGateControl := 0.0;
            bParticleReject := TRUE;
        END_IF;
        
        (* Loss of enable or field decay *)
        IF NOT bSystemEnable OR NOT bTriboChargeReady THEN
            iState := 30;
        END_IF;

    30: (* SPIN-DOWN SEQUENCE *)
        bSystemReady := FALSE;
        rMagneticGateControl := 0.0;
        bParticleReject := FALSE;
        rTargetRPM := 0.0;
        IF (rCentrifugeRPM < 10.0) THEN
            iState := 0;
        END_IF;
        
    99: (* FAULT HANDLING *)
        IF bEmergencyStop AND NOT bSystemEnable THEN
            bAlarm := FALSE;
            iState := 0;
        END_IF;

END_CASE;

END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
print(f"Saved to {filename}")
