import os
import json
import uuid

os.makedirs('data/swarm_raw', exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Next-Generation Perovskite Solar Cell Slot-Die Coating**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Nanoscale wet film thickness interferometry feedback, anti-solvent quenching rapid timing, and multi-zone meniscus stability control). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_Perovskite_SlotDieCoating\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Next-Generation Perovskite Solar Cell Slot-Die Coating

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_Perovskite_SlotDieCoating
(* ==============================================================================
   Block: FB_Perovskite_SlotDieCoating
   Description: Advanced slot-die coating control for next-gen perovskite solar cells.
   Author: Lumina AI Elite Architect
   Date: 2026-09-12
   Revision: 3.1.4 (Final Production)
   
   Features:
   - Nanoscale wet film thickness interferometry feedback loop.
   - Anti-solvent quenching rapid timing integration.
   - Multi-zone meniscus stability via dual PID and cross-coupled control.
   - Moving average filtering for high-frequency sensor noise.
   ============================================================================== *)

VAR_INPUT
    bEnable                 : BOOL;     (* Main sequence enable command *)
    bEmergencyStop          : BOOL;     (* True if E-Stop is NOT pressed (OK condition) *)
    rInterferometryThickness: REAL;     (* Measured wet film thickness [nm] *)
    rTargetThickness        : REAL;     (* Setpoint for wet film thickness [nm] *)
    rSubstrateSpeed         : REAL;     (* Web speed of the flexible substrate [m/min] *)
    rMeniscusPressure       : REAL;     (* Vacuum box pressure for meniscus stability [mbar] *)
    rCoatingTemperature     : REAL;     (* Die body temperature for rheology control [deg C] *)
    bQuenchTrigger          : BOOL;     (* Synchronized trigger for anti-solvent drop *)
END_VAR

VAR_OUTPUT
    bSystemReady            : BOOL;     (* TRUE when all zones are at temp and stable *)
    rPumpFlowRateCmd        : REAL;     (* Syringe/gear pump flow setpoint [uL/min] *)
    rVacuumBoxCmd           : REAL;     (* Commanded vacuum level for meniscus [mbar] *)
    bQuenchValveOpen        : BOOL;     (* High-speed pneumatic valve for anti-solvent *)
    bAlarmThicknessDev      : BOOL;     (* Out of tolerance alarm for thickness *)
    bFault                  : BOOL;     (* General system fault (latching) *)
    iSequenceState          : INT;      (* Current state of the coating state machine *)
END_VAR

VAR
    (* Internal State Variables *)
    iState                  : INT := 0;
    
    (* Filter Arrays *)
    arThicknessBuffer       : ARRAY[0..9] OF REAL;
    iFilterIdx              : INT := 0;
    rFilteredThickness      : REAL;
    rThicknessSum           : REAL;
    i                       : INT;
    
    (* PID Control Variables (Simplified representations) *)
    rProportionalError      : REAL;
    rIntegralError          : REAL;
    rDerivativeError        : REAL;
    rLastError              : REAL;
    rKp                     : REAL := 1.25;
    rKi                     : REAL := 0.45;
    rKd                     : REAL := 0.08;
    
    (* Timers *)
    tQuenchDelay            : TON;
    tStabilization          : TON;
    
    (* Safety limits *)
    MAX_FLOW_RATE           : REAL := 5000.0; (* uL/min *)
    MAX_THICKNESS_ERR       : REAL := 15.0;   (* nm *)
END_VAR

(* === SAFETY & INTERLOCK LOGIC === *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bFault := TRUE;
    rPumpFlowRateCmd := 0.0;
    rVacuumBoxCmd := 0.0;
    bQuenchValveOpen := FALSE;
    iState := 999; (* Fault state *)
    RETURN;
END_IF;

(* === HIGH-FREQUENCY SENSOR FILTERING === *)
(* 10-point moving average filter for interferometry thickness *)
arThicknessBuffer[iFilterIdx] := rInterferometryThickness;
iFilterIdx := (iFilterIdx + 1) MOD 10;

rThicknessSum := 0.0;
FOR i := 0 TO 9 DO
    rThicknessSum := rThicknessSum + arThicknessBuffer[i];
END_FOR;
rFilteredThickness := rThicknessSum / 10.0;

(* Check for critical thickness deviation *)
IF ABS(rFilteredThickness - rTargetThickness) > MAX_THICKNESS_ERR THEN
    bAlarmThicknessDev := TRUE;
ELSE
    bAlarmThicknessDev := FALSE;
END_IF;

(* === MAIN COATING STATE MACHINE === *)
CASE iState OF
    0: (* IDLE - Awaiting Enable and verifying temperature *)
        rPumpFlowRateCmd := 0.0;
        bQuenchValveOpen := FALSE;
        
        IF (rCoatingTemperature > 22.5 AND rCoatingTemperature < 23.5) THEN
            bSystemReady := TRUE;
        ELSE
            bSystemReady := FALSE;
        END_IF;
        
        IF bEnable AND bSystemReady THEN
            iState := 10;
        END_IF;

    10: (* PRIMING - Initial flow establishment *)
        rPumpFlowRateCmd := (rTargetThickness * rSubstrateSpeed * 0.001) * 1.05; (* Open loop estimation *)
        rVacuumBoxCmd := -5.0; (* Slight vacuum to hold meniscus *)
        
        tStabilization(IN := TRUE, PT := T#3S);
        IF tStabilization.Q THEN
            tStabilization(IN := FALSE);
            iState := 20;
        END_IF;

    20: (* CLOSED LOOP COATING - Active thickness control *)
        (* PID calculation for flow rate fine-tuning *)
        rProportionalError := rTargetThickness - rFilteredThickness;
        rIntegralError := rIntegralError + (rProportionalError * 0.01); (* Assume 10ms task cycle *)
        
        (* Anti-windup clamping *)
        IF rIntegralError > 100.0 THEN rIntegralError := 100.0; END_IF;
        IF rIntegralError < -100.0 THEN rIntegralError := -100.0; END_IF;
        
        rDerivativeError := (rProportionalError - rLastError) / 0.01;
        rLastError := rProportionalError;
        
        rPumpFlowRateCmd := (rTargetThickness * rSubstrateSpeed * 0.001) + 
                            (rKp * rProportionalError) + 
                            (rKi * rIntegralError) + 
                            (rKd * rDerivativeError);
                            
        (* Limit flow rate to safe bounds *)
        IF rPumpFlowRateCmd > MAX_FLOW_RATE THEN
            rPumpFlowRateCmd := MAX_FLOW_RATE;
        ELSIF rPumpFlowRateCmd < 0.0 THEN
            rPumpFlowRateCmd := 0.0;
        END_IF;
        
        (* Active Meniscus Control (Cross-coupling logic) *)
        rVacuumBoxCmd := -5.0 - (rSubstrateSpeed * 0.2); 
        
        (* Anti-solvent quenching sequence execution *)
        IF bQuenchTrigger THEN
            tQuenchDelay(IN := TRUE, PT := T#150MS); (* Critical delay for crystalization window *)
        END_IF;
        
        IF tQuenchDelay.Q THEN
            bQuenchValveOpen := TRUE;
            tQuenchDelay(IN := FALSE);
        END_IF;
        
        (* Stop condition *)
        IF NOT bEnable THEN
            rIntegralError := 0.0;
            iState := 30;
        END_IF;
        
    30: (* SHUTDOWN - Clean break of meniscus *)
        rPumpFlowRateCmd := 0.0;
        rVacuumBoxCmd := 0.0; (* Drop vacuum to break meniscus *)
        bQuenchValveOpen := FALSE;
        
        tStabilization(IN := TRUE, PT := T#1S);
        IF tStabilization.Q THEN
            tStabilization(IN := FALSE);
            iState := 0;
        END_IF;

    999: (* FAULT HANDLING *)
        IF bEmergencyStop AND NOT bEnable THEN
            bFault := FALSE;
            iState := 0;
        END_IF;
        
END_CASE;

END_FUNCTION_BLOCK
```"""

record = {'messages': [{'role': 'user', 'content': prompt}, {'role': 'assistant', 'content': code}]}
filename = f'data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json'
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(record, f, ensure_ascii=False)
print(f'Saved to {filename}')
