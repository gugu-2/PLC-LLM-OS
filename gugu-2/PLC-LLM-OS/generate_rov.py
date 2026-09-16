import os, json, uuid

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Autonomous Deep-Sea ROV 7-Function Hydraulic Manipulator Force Feedback**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Subsea 400-bar depth pressure-compensated servo valve dithering, master-slave haptic compliance impedance control, and joint overload anti-jam bypass). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\nFUNCTION_BLOCK FB_ROV_ManipulatorControl\n//...\nEND_FUNCTION_BLOCK\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Autonomous Deep-Sea ROV 7-Function Hydraulic Manipulator Force Feedback

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_ROV_ManipulatorControl
VAR_INPUT
    (* Required: at least 4-8 physical inputs with types and comments *)
    bEnable                 : BOOL;     (* System master enable *)
    bEmergencyStop          : BOOL;     (* True = OK to operate, False = E-Stop active *)
    rDepthPressure_bar      : REAL;     (* Ambient subsea pressure for compensation *)
    rMasterPosCommand       : REAL;     (* Haptic master arm position command 0-100% *)
    rSlaveForceFeedback     : REAL;     (* Current force feedback from the slave arm *)
    rHydraulicSupply_bar    : REAL;     (* Main hydraulic ring supply pressure *)
    bJointOverload          : BOOL;     (* Digital flag for joint overload condition *)
    rOilTemp_C              : REAL;     (* Hydraulic fluid temperature *)
END_VAR
VAR_OUTPUT
    (* Required: at least 3-6 outputs with types and comments *)
    bSystemReady            : BOOL;     (* System ready for operation *)
    rServoValveDither       : REAL;     (* High-frequency dither signal for servo *)
    rMainControlOutput      : REAL;     (* Impedance controlled valve command *)
    bAlarm                  : BOOL;     (* General fault alarm *)
    bOverloadBypassActive   : BOOL;     (* Jam bypass mode active indicator *)
END_VAR
VAR
    (* Internal state variables *)
    iState                  : INT := 0;
    tDitherTimer            : TON;
    rPosError               : REAL := 0.0;
    rForceError             : REAL := 0.0;
    rImpedanceCompliance    : REAL := 0.05;
    rIntegral               : REAL := 0.0;
    rDerivative             : REAL := 0.0;
    rLastError              : REAL := 0.0;
    Kp                      : REAL := 2.5;
    Ki                      : REAL := 0.1;
    Kd                      : REAL := 0.5;
    tSafetyTimer            : TON;
    bInitialize             : BOOL := TRUE;
    rCompensatedPressure    : REAL := 0.0;
END_VAR

(* === MAIN LOGIC === *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bAlarm := TRUE;
    rMainControlOutput := 0.0;
    rServoValveDither := 0.0;
    iState := 0;
    RETURN;
END_IF;

(* Ambient pressure compensation calculation based on 400-bar depth *)
rCompensatedPressure := rHydraulicSupply_bar - (rDepthPressure_bar * 0.98);
IF rCompensatedPressure < 50.0 OR rOilTemp_C > 85.0 THEN
    bAlarm := TRUE;
    iState := 99; (* FAULT STATE *)
ELSE
    bAlarm := FALSE;
END_IF;

CASE iState OF
    0: (* IDLE & INITIALIZATION *)
        bSystemReady := FALSE;
        bOverloadBypassActive := FALSE;
        rMainControlOutput := 0.0;
        IF bEnable AND bInitialize THEN
            tSafetyTimer(IN := FALSE);
            iState := 10;
        END_IF;

    10: (* HYDRAULIC PRIME & DITHER START *)
        bSystemReady := TRUE;
        (* 400Hz dither generation using timer approximation for servo valve stiction removal *)
        tDitherTimer(IN := TRUE, PT := T#2MS);
        IF tDitherTimer.Q THEN
            IF rServoValveDither > 0.0 THEN
                rServoValveDither := -0.05;
            ELSE
                rServoValveDither := 0.05;
            END_IF;
            tDitherTimer(IN := FALSE);
        END_IF;
        
        IF NOT bJointOverload THEN
            iState := 20;
        ELSE
            iState := 30;
        END_IF;

    20: (* IMPEDANCE & COMPLIANCE CONTROL (ACTIVE OPERATION) *)
        rPosError := rMasterPosCommand - rSlaveForceFeedback * rImpedanceCompliance;
        
        (* PID Computation *)
        rIntegral := rIntegral + (rPosError * 0.01);
        rDerivative := (rPosError - rLastError) / 0.01;
        rLastError := rPosError;
        
        rMainControlOutput := (Kp * rPosError) + (Ki * rIntegral) + (Kd * rDerivative);
        
        (* Apply bounds *)
        IF rMainControlOutput > 100.0 THEN
            rMainControlOutput := 100.0;
        ELSIF rMainControlOutput < -100.0 THEN
            rMainControlOutput := -100.0;
        END_IF;
        
        IF bJointOverload THEN
            iState := 30;
        END_IF;
        
    30: (* ANTI-JAM OVERLOAD BYPASS *)
        bOverloadBypassActive := TRUE;
        rMainControlOutput := -15.0; (* Slight reversal to relieve pressure *)
        tSafetyTimer(IN := TRUE, PT := T#3S);
        IF tSafetyTimer.Q THEN
            IF NOT bJointOverload THEN
                bOverloadBypassActive := FALSE;
                tSafetyTimer(IN := FALSE);
                iState := 20;
            ELSE
                iState := 99; (* FAIL-SAFE TRIGGERED *)
            END_IF;
        END_IF;
        
    99: (* FAULT HANDLING *)
        bSystemReady := FALSE;
        rMainControlOutput := 0.0;
        bOverloadBypassActive := FALSE;
        rServoValveDither := 0.0;
        IF NOT bEnable AND rCompensatedPressure > 50.0 AND rOilTemp_C <= 85.0 THEN
            bAlarm := FALSE;
            iState := 0;
        END_IF;

END_CASE;

END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
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
