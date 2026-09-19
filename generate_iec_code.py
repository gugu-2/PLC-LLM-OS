import os
import json
import uuid

os.chdir('C:/Users/majip/Downloads/LLM REASEARCH')
if not os.path.exists('data/swarm_raw'):
    os.makedirs('data/swarm_raw', exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: High-Speed Commercial Newspaper Printing Press Web Tension and Ink Registration**

Task: Invent a highly complex, ultra-realistic control scenario for this domain. Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_PrintingPress_WebTension\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: High-Speed Commercial Newspaper Printing Press Web Tension and Ink Registration

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_PrintingPress_WebTension_InkRegistration
VAR_INPUT
    bEnable                 : BOOL;     (* System Enable Signal - Master Run *)
    bEmergencyStop          : BOOL;     (* Safety Relay OK Signal - E-Stop Circuit *)
    rWebTensionActual       : REAL;     (* Feedback from load cells in N/m *)
    rWebTensionSetpoint     : REAL;     (* Target tension setpoint in N/m *)
    rPressSpeed             : REAL;     (* Master press line speed in m/min *)
    rInkViscosity           : REAL;     (* Measured ink viscosity in mPa.s *)
    rRegistrationMarkErrorX : REAL;     (* Transverse registration error in mm *)
    rRegistrationMarkErrorY : REAL;     (* Longitudinal registration error in mm *)
END_VAR
VAR_OUTPUT
    bSystemReady            : BOOL;     (* Registration and Tension systems ready *)
    rTensionMotorCommand    : REAL;     (* Speed command to tension control nip roller in % *)
    rCompensatorRollerPos   : REAL;     (* Commanded position for longitudinal compensator roller in mm *)
    rLateralGuidePos        : REAL;     (* Commanded position for web edge guide in mm *)
    rInkDuctMotorSpeed      : REAL;     (* Speed command to ink duct motor in % *)
    bWebBreakAlarm          : BOOL;     (* Fault: Web break detected *)
    bRegistrationAlarm      : BOOL;     (* Fault: Registration out of bounds *)
END_VAR
VAR
    iState                  : INT := 0; (* State Machine Index *)
    tStartupDelay           : TON;      (* Start delay timer *)
    tWebBreakFilter         : TON;      (* Filter timer for web break detection *)
    
    (* Tension Control PID Variables *)
    rTensionError           : REAL;
    rTensionIntegral        : REAL;
    rTensionDerivative      : REAL;
    rTensionLastError       : REAL;
    rTensionKp              : REAL := 1.25;
    rTensionKi              : REAL := 0.45;
    rTensionKd              : REAL := 0.15;
    
    (* Registration Control PID Variables *)
    rRegErrorX              : REAL;
    rRegIntegralX           : REAL;
    rRegErrorY              : REAL;
    rRegIntegralY           : REAL;
    
    (* Filters *)
    rTensionFiltered        : REAL;
    rAlpha                  : REAL := 0.1; (* Low pass filter coefficient *)
    
    (* Limits *)
    rMaxTensionErr          : REAL := 250.0;
    rMaxRegErr              : REAL := 5.0;
    rMinTension             : REAL := 50.0;
    
END_VAR

(* === MAIN LOGIC === *)
(* 1. Safety and Fundamental Checks *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    rTensionMotorCommand := 0.0;
    rCompensatorRollerPos := 0.0;
    rLateralGuidePos := 0.0;
    rInkDuctMotorSpeed := 0.0;
    bWebBreakAlarm := FALSE;
    bRegistrationAlarm := FALSE;
    iState := 0;
    RETURN;
END_IF;

(* 2. Input Filtering (First Order Low-Pass) *)
rTensionFiltered := (rAlpha * rWebTensionActual) + ((1.0 - rAlpha) * rTensionFiltered);

(* 3. Web Break Detection *)
IF (rPressSpeed > 50.0) AND (rTensionFiltered < rMinTension) THEN
    tWebBreakFilter(IN := TRUE, PT := T#500MS);
ELSE
    tWebBreakFilter(IN := FALSE, PT := T#500MS);
END_IF;

IF tWebBreakFilter.Q THEN
    bWebBreakAlarm := TRUE;
    iState := 99; (* Fault State *)
END_IF;

(* 4. State Machine for Control *)
CASE iState OF
    0: (* IDLE *)
        bSystemReady := FALSE;
        rTensionMotorCommand := 0.0;
        rCompensatorRollerPos := 0.0;
        rLateralGuidePos := 0.0;
        rTensionIntegral := 0.0;
        IF bEnable AND NOT bWebBreakAlarm THEN
            iState := 10;
        END_IF;

    10: (* PRE-TENSIONING *)
        (* Slowly ramp up tension motor command *)
        rTensionMotorCommand := rTensionMotorCommand + 0.1;
        IF rTensionFiltered >= (rWebTensionSetpoint * 0.8) THEN
            tStartupDelay(IN := TRUE, PT := T#3S);
            IF tStartupDelay.Q THEN
                tStartupDelay(IN := FALSE);
                bSystemReady := TRUE;
                iState := 20;
            END_IF;
        END_IF;
        IF NOT bEnable THEN
            iState := 0;
        END_IF;

    20: (* RUNNING - CLOSED LOOP PID *)
        (* Tension PID Loop *)
        rTensionError := rWebTensionSetpoint - rTensionFiltered;
        rTensionIntegral := rTensionIntegral + (rTensionError * 0.01); (* Assuming 10ms cycle *)
        
        (* Anti-windup for Tension *)
        IF rTensionIntegral > 100.0 THEN rTensionIntegral := 100.0; END_IF;
        IF rTensionIntegral < -100.0 THEN rTensionIntegral := -100.0; END_IF;
        
        rTensionDerivative := (rTensionError - rTensionLastError) / 0.01;
        rTensionLastError := rTensionError;
        
        (* Feedforward from press speed *)
        rTensionMotorCommand := (rPressSpeed * 0.5) + (rTensionKp * rTensionError) + (rTensionKi * rTensionIntegral) + (rTensionKd * rTensionDerivative);
        
        (* Registration Loop (Lateral and Longitudinal) *)
        rRegErrorX := rRegistrationMarkErrorX;
        rRegErrorY := rRegistrationMarkErrorY;
        
        IF ABS(rRegErrorX) > rMaxRegErr OR ABS(rRegErrorY) > rMaxRegErr THEN
            bRegistrationAlarm := TRUE;
        ELSE
            bRegistrationAlarm := FALSE;
        END_IF;
        
        (* Simple P-control for Web Guide and Compensator Roller *)
        rLateralGuidePos := rLateralGuidePos + (rRegErrorX * 0.2);
        rCompensatorRollerPos := rCompensatorRollerPos + (rRegErrorY * 0.25);
        
        (* Ink Duct Control based on speed and viscosity compensation *)
        rInkDuctMotorSpeed := (rPressSpeed * 0.8) * (1.0 + ((rInkViscosity - 100.0) * 0.001));

        IF NOT bEnable THEN
            iState := 0;
        END_IF;
        
    99: (* FAULT STATE *)
        bSystemReady := FALSE;
        rTensionMotorCommand := 0.0;
        IF NOT bWebBreakAlarm AND NOT bRegistrationAlarm AND NOT bEnable THEN
            iState := 0; (* Reset conditions met *)
        END_IF;

END_CASE;

END_FUNCTION_BLOCK
```"""

record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"

with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print(f"Saved to {filename}")
