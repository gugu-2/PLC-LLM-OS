import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Hydrogen Fuel Cell Stack Automated Manufacturing & Assembly Line**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., precise bipolar plate robotic stacking, nanometer-level Membrane Electrode Assembly (MEA) alignment, active clamping force feedback loops, and leak test pressurization). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_FuelCellAssembly\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Hydrogen Fuel Cell Stack Automated Manufacturing & Assembly Line

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_H2CellStackAssembly
(* 
    Advanced Control Block for Hydrogen Fuel Cell Stack Assembly
    Handles MEA nanometer alignment, bipolar plate stacking,
    active clamping force control, and pressurization leak testing.
*)
VAR_INPUT
    bEnable                 : BOOL;     (* System enable signal *)
    bEmergencyStop          : BOOL;     (* Safety relay OK signal (Active High) *)
    bStartAssembly          : BOOL;     (* Trigger to start a new stack *)
    rMEAAlignmentX_nm       : REAL;     (* Vision system MEA X alignment error in nanometers *)
    rMEAAlignmentY_nm       : REAL;     (* Vision system MEA Y alignment error in nanometers *)
    rActualClampForce_kN    : REAL;     (* Load cell feedback for clamping force *)
    rLeakTestPressure_bar   : REAL;     (* Pressure sensor feedback for leak testing *)
    iTargetCellCount        : INT;      (* Total number of cells to stack *)
END_VAR

VAR_OUTPUT
    bSystemReady            : BOOL;     (* System ready for operation *)
    bAssemblyComplete       : BOOL;     (* Stack assembly finished successfully *)
    bAlarm                  : BOOL;     (* Fault alarm output *)
    iAlarmCode              : INT;      (* Detailed fault code *)
    rAlignActuatorX_cmd     : REAL;     (* Command to X nano-positioner *)
    rAlignActuatorY_cmd     : REAL;     (* Command to Y nano-positioner *)
    rClampActuator_cmd      : REAL;     (* Command to servo press for clamping *)
    bPressurizeValve        : BOOL;     (* Control valve for leak test air *)
END_VAR

VAR
    iState                  : INT := 0;
    iCurrentCell            : INT := 0;
    
    (* Timers *)
    tAlignmentTimeout       : TON;
    tClampStabilization     : TON;
    tLeakTestTimer          : TON;
    
    (* PI Controller for Clamping Force *)
    rClampError             : REAL;
    rClampIntegral          : REAL;
    rKp_Clamp               : REAL := 0.25;
    rKi_Clamp               : REAL := 0.05;
    
    (* Constants *)
    rTolerance_nm           : REAL := 50.0; (* 50 nanometers alignment tolerance *)
    rTargetForce_kN         : REAL := 15.0; (* 15 kN target clamp force *)
    rForceTolerance_kN      : REAL := 0.1;  
    rTargetPressure_bar     : REAL := 2.5;
    rPressureDropLimit_bar  : REAL := 0.05;
    rStartPressure_bar      : REAL;
END_VAR

(* === MAIN LOGIC === *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bAssemblyComplete := FALSE;
    bAlarm := TRUE;
    iAlarmCode := 999; (* Emergency Stop Active *)
    rAlignActuatorX_cmd := 0.0;
    rAlignActuatorY_cmd := 0.0;
    rClampActuator_cmd := 0.0;
    bPressurizeValve := FALSE;
    iState := 0;
    RETURN;
END_IF;

CASE iState OF
    0: (* INIT / IDLE *)
        bSystemReady := TRUE;
        bAssemblyComplete := FALSE;
        bAlarm := FALSE;
        iAlarmCode := 0;
        iCurrentCell := 0;
        rClampIntegral := 0.0;
        bPressurizeValve := FALSE;
        
        IF bEnable AND bStartAssembly THEN
            bSystemReady := FALSE;
            iState := 10;
        END_IF;

    10: (* PICK AND PLACE NEXT COMPONENT *)
        (* Logic to control robot to place MEA and Bipolar Plate *)
        (* Assuming synchronous handshake with robot is abstracted here *)
        iCurrentCell := iCurrentCell + 1;
        tAlignmentTimeout(IN := FALSE);
        iState := 20;

    20: (* NANOMETER ALIGNMENT *)
        tAlignmentTimeout(IN := TRUE, PT := T#10S);
        
        (* Simple Proportional control for alignment *)
        rAlignActuatorX_cmd := rMEAAlignmentX_nm * -0.1;
        rAlignActuatorY_cmd := rMEAAlignmentY_nm * -0.1;
        
        IF (ABS(rMEAAlignmentX_nm) < rTolerance_nm) AND (ABS(rMEAAlignmentY_nm) < rTolerance_nm) THEN
            (* Alignment successful *)
            rAlignActuatorX_cmd := 0.0;
            rAlignActuatorY_cmd := 0.0;
            IF iCurrentCell >= iTargetCellCount THEN
                iState := 30; (* Move to clamping *)
            ELSE
                iState := 10; (* Loop back for next cell *)
            END_IF;
        ELSIF tAlignmentTimeout.Q THEN
            bAlarm := TRUE;
            iAlarmCode := 101; (* Alignment Timeout Error *)
            iState := 99; (* Fault state *)
        END_IF;

    30: (* ACTIVE CLAMPING WITH PI CONTROL *)
        rClampError := rTargetForce_kN - rActualClampForce_kN;
        rClampIntegral := rClampIntegral + (rClampError * 0.01); (* Assuming 10ms task cycle *)
        
        (* Anti-windup *)
        IF rClampIntegral > 100.0 THEN rClampIntegral := 100.0; END_IF;
        IF rClampIntegral < -100.0 THEN rClampIntegral := -100.0; END_IF;
        
        rClampActuator_cmd := (rKp_Clamp * rClampError) + (rKi_Clamp * rClampIntegral);
        
        tClampStabilization(IN := (ABS(rClampError) < rForceTolerance_kN), PT := T#5S);
        
        IF tClampStabilization.Q THEN
            tClampStabilization(IN := FALSE);
            iState := 40;
        END_IF;

    40: (* LEAK TEST PREPARATION *)
        bPressurizeValve := TRUE;
        IF rLeakTestPressure_bar >= rTargetPressure_bar THEN
            bPressurizeValve := FALSE;
            rStartPressure_bar := rLeakTestPressure_bar;
            tLeakTestTimer(IN := FALSE);
            iState := 50;
        END_IF;

    50: (* LEAK TEST MONITORING *)
        tLeakTestTimer(IN := TRUE, PT := T#60S);
        
        IF (rStartPressure_bar - rLeakTestPressure_bar) > rPressureDropLimit_bar THEN
            (* Leak detected *)
            bAlarm := TRUE;
            iAlarmCode := 201; (* Failed Leak Test *)
            bPressurizeValve := FALSE;
            iState := 99;
        ELSIF tLeakTestTimer.Q THEN
            (* Leak test passed *)
            tLeakTestTimer(IN := FALSE);
            iState := 60;
        END_IF;

    60: (* ASSEMBLY COMPLETE *)
        bAssemblyComplete := TRUE;
        IF NOT bStartAssembly THEN
            iState := 0;
        END_IF;
        
    99: (* FAULT HANDLING *)
        (* Wait for reset / manual intervention *)
        bPressurizeValve := FALSE;
        rClampActuator_cmd := 0.0;
        IF NOT bEnable THEN
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
