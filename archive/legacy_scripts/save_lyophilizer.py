import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Next-Gen Pharmaceutical Lyophilizer (Freeze Dryer) Shelf Cooling**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Silicone oil multi-zone cascaded refrigeration, sublimation primary drying vacuum setpoint drifting, and endpoint Pirani/Capacitance manometer convergence tracking). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_PharmaLyophilizer\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Next-Gen Pharmaceutical Lyophilizer (Freeze Dryer) Shelf Cooling

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_LyophilizerShelfCooling
VAR_INPUT
    (* Required: at least 4-8 physical inputs with types and comments *)
    bEnable                 : BOOL;     (* System enable signal, master interlock *)
    bEmergencyStop          : BOOL;     (* Safety relay OK signal (Normally Closed = TRUE) *)
    rChamberVacuum_mTorr    : REAL;     (* Capacitance manometer reading, 0-100000 mTorr *)
    rPiraniVacuum_mTorr     : REAL;     (* Pirani gauge reading for endpoint determination *)
    rShelfTempSetPoint_C    : REAL;     (* Desired shelf temperature in Celsius *)
    rShelfTempActual_C      : REAL;     (* RTD array averaged actual shelf temperature *)
    rSiliconeOilFlow_Lmin   : REAL;     (* Heat transfer fluid flow rate in L/min *)
    bDefrostActive          : BOOL;     (* True if SIP/CIP or defrost cycle is active *)
END_VAR

VAR_OUTPUT
    (* Required: at least 3-6 outputs with types and comments *)
    bSystemReady            : BOOL;     (* System ready status for primary drying phase *)
    rCoolingValveCmd_Pct    : REAL;     (* Cascaded refrigeration cooling valve command 0-100% *)
    rHeatingValveCmd_Pct    : REAL;     (* Heat transfer fluid heater SCR command 0-100% *)
    bSublimationEndpoint    : BOOL;     (* True when Pirani and Capacitance gauges converge *)
    bAlarm                  : BOOL;     (* General fault alarm output *)
    iFaultCode              : INT;      (* Diagnostics: 0=None, 1=E-Stop, 2=Flow, 3=Temp Dev *)
END_VAR

VAR
    (* Internal state variables *)
    iState                  : INT := 0; 
    tStabilizationTimer     : TON;
    tEndpointTimer          : TON;
    rTempError              : REAL;
    rIntegralTerm           : REAL := 0.0;
    rDerivativeTerm         : REAL := 0.0;
    rLastError              : REAL := 0.0;
    
    (* PID Constants *)
    Kp                      : REAL := 2.5;
    Ki                      : REAL := 0.15;
    Kd                      : REAL := 0.05;
    
    (* Safety limits *)
    MAX_TEMP_ERROR          : REAL := 5.0;
    MIN_OIL_FLOW            : REAL := 15.0;
    MAX_OUTPUT              : REAL := 100.0;
    MIN_OUTPUT              : REAL := -100.0;
    
    bFilterInit             : BOOL := FALSE;
    rFilteredTemp           : REAL := 0.0;
    rPIDOutput              : REAL := 0.0;
END_VAR

(* === MAIN LOGIC === *)

(* Safety and Interlock Check *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    rCoolingValveCmd_Pct := 0.0;
    rHeatingValveCmd_Pct := 0.0;
    bAlarm := TRUE;
    iFaultCode := 1;
    iState := 0;
    RETURN;
END_IF;

IF rSiliconeOilFlow_Lmin < MIN_OIL_FLOW AND bEnable AND NOT bDefrostActive THEN
    bSystemReady := FALSE;
    rCoolingValveCmd_Pct := 0.0;
    rHeatingValveCmd_Pct := 0.0;
    bAlarm := TRUE;
    iFaultCode := 2;
    iState := 0;
    RETURN;
END_IF;

(* First-order low pass filter for actual temperature to reduce sensor noise *)
IF NOT bFilterInit THEN
    rFilteredTemp := rShelfTempActual_C;
    bFilterInit := TRUE;
ELSE
    rFilteredTemp := rFilteredTemp * 0.9 + rShelfTempActual_C * 0.1;
END_IF;

(* Sublimation Endpoint Determination via Gauge Convergence *)
IF iState = 20 THEN
    (* Pirani reads higher when water vapor is present. When it converges to CapMan, primary drying is complete *)
    IF ABS(rPiraniVacuum_mTorr - rChamberVacuum_mTorr) < 5.0 THEN
        tEndpointTimer(IN := TRUE, PT := T#30M);
        IF tEndpointTimer.Q THEN
            bSublimationEndpoint := TRUE;
        END_IF;
    ELSE
        tEndpointTimer(IN := FALSE);
        bSublimationEndpoint := FALSE;
    END_IF;
ELSE
    tEndpointTimer(IN := FALSE);
    bSublimationEndpoint := FALSE;
END_IF;

CASE iState OF
    0: (* IDLE & RESET *)
        bSystemReady := FALSE;
        rCoolingValveCmd_Pct := 0.0;
        rHeatingValveCmd_Pct := 0.0;
        bAlarm := FALSE;
        iFaultCode := 0;
        rIntegralTerm := 0.0;
        
        IF bEnable AND NOT bDefrostActive THEN
            iState := 10;
        END_IF;

    10: (* CHILLING & TEMPERATURE STABILIZATION *)
        bSystemReady := FALSE;
        
        (* Calculate Error *)
        rTempError := rShelfTempSetPoint_C - rFilteredTemp;
        
        (* Advanced PID Calculation *)
        rIntegralTerm := rIntegralTerm + (rTempError * Ki);
        
        (* Anti-windup *)
        IF rIntegralTerm > MAX_OUTPUT THEN
            rIntegralTerm := MAX_OUTPUT;
        ELSIF rIntegralTerm < MIN_OUTPUT THEN
            rIntegralTerm := MIN_OUTPUT;
        END_IF;
        
        rDerivativeTerm := (rTempError - rLastError) * Kd;
        rLastError := rTempError;
        
        (* Control Output Mapping *)
        rPIDOutput := (rTempError * Kp) + rIntegralTerm + rDerivativeTerm;
        
        IF rPIDOutput > 0.0 THEN
            rHeatingValveCmd_Pct := LIMIT(0.0, rPIDOutput, MAX_OUTPUT);
            rCoolingValveCmd_Pct := 0.0;
        ELSE
            rCoolingValveCmd_Pct := LIMIT(0.0, ABS(rPIDOutput), MAX_OUTPUT);
            rHeatingValveCmd_Pct := 0.0;
        END_IF;
        
        (* Check if temperature is stable to move to primary drying *)
        IF ABS(rTempError) < 0.5 THEN
            tStabilizationTimer(IN := TRUE, PT := T#15M);
            IF tStabilizationTimer.Q THEN
                tStabilizationTimer(IN := FALSE);
                iState := 20;
            END_IF;
        ELSE
            tStabilizationTimer(IN := FALSE);
        END_IF;

    20: (* PRIMARY DRYING (SUBLIMATION) *)
        bSystemReady := TRUE;
        
        (* Continue PID Control to maintain tight shelf temp *)
        rTempError := rShelfTempSetPoint_C - rFilteredTemp;
        
        IF ABS(rTempError) > MAX_TEMP_ERROR THEN
            bAlarm := TRUE;
            iFaultCode := 3;
            iState := 0;
        END_IF;
        
        rIntegralTerm := rIntegralTerm + (rTempError * Ki);
        rDerivativeTerm := (rTempError - rLastError) * Kd;
        rLastError := rTempError;
        
        rPIDOutput := (rTempError * Kp) + rIntegralTerm + rDerivativeTerm;
        
        IF rPIDOutput > 0.0 THEN
            rHeatingValveCmd_Pct := LIMIT(0.0, rPIDOutput, MAX_OUTPUT);
            rCoolingValveCmd_Pct := 0.0;
        ELSE
            rCoolingValveCmd_Pct := LIMIT(0.0, ABS(rPIDOutput), MAX_OUTPUT);
            rHeatingValveCmd_Pct := 0.0;
        END_IF;
        
        IF NOT bEnable THEN
            iState := 0;
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
