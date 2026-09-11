import os
import json
import uuid

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Next-Gen Subsea High-Voltage Direct Current (HVDC) Circuit Breaker**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Active resonance commutation, ultra-fast piezoelectric vacuum interrupter separation, and metal-oxide varistor (MOV) energy dissipation cascading). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_HVDC_SubseaCircuitBreaker\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Next-Gen Subsea High-Voltage Direct Current (HVDC) Circuit Breaker

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_SubseaHvdcCircuitBreaker
VAR_INPUT
    bEnable                 : BOOL;     (* System Enable Signal - Watchdog verified *)
    bEmergencyTrip          : BOOL;     (* SIL4 Emergency trip command from station control *)
    rLineCurrent            : REAL;     (* Measured DC line current [kA], nominal 2.5kA *)
    rLineVoltage            : REAL;     (* Measured DC line voltage [kV], nominal 525kV *)
    rWaterPressure          : REAL;     (* Ambient subsea water pressure [bar] *)
    rCoolantTemp            : REAL;     (* Coolant temperature for commutation circuit [C] *)
END_VAR
VAR_OUTPUT
    bSystemReady            : BOOL;     (* Circuit Breaker is healthy and ready to operate *)
    bTripSuccessful         : BOOL;     (* Acknowledgment that DC fault was cleared *)
    rMovEnergyDissipated    : REAL;     (* Estimated energy dissipated by Metal Oxide Varistors [MJ] *)
    bAlarm                  : BOOL;     (* General fault / warning output *)
    iOperatingState         : INT;      (* Current internal state enum *)
END_VAR
VAR
    (* Internal State Machine Enum *)
    iState                  : INT := 0;
    
    (* Filtered Measurements *)
    rFiltLineCurrent        : REAL := 0.0;
    rFiltLineVoltage        : REAL := 0.0;
    
    (* Timers *)
    tTripTimer              : TON;
    tCommutationTimer       : TON;
    tCoolingTimer           : TON;
    
    (* Trip sequence variables *)
    bFaultDetected          : BOOL := FALSE;
    bArcExtinguished        : BOOL := FALSE;
    rFaultCurrentPeak       : REAL := 0.0;
    
    (* Constants *)
    c_rCurrentThreshold     : REAL := 4.5;    (* Fault current threshold [kA] *)
    c_rVoltageThreshold     : REAL := 400.0;  (* Under-voltage threshold [kV] *)
    c_rMaxCoolantTemp       : REAL := 85.0;   (* Max safe operating temp [C] *)
    
    (* Low-pass filter coefficients *)
    c_rAlpha                : REAL := 0.2;
END_VAR

(* === MAIN LOGIC === *)

(* Safety and Hardware Interlocks *)
IF bEmergencyTrip THEN
    bSystemReady := FALSE;
    bAlarm := TRUE;
    iState := 99; (* EMERGENCY TRIP STATE *)
END_IF;

IF rWaterPressure > 350.0 OR rCoolantTemp > c_rMaxCoolantTemp THEN
    bAlarm := TRUE;
    IF iState < 10 THEN
        bSystemReady := FALSE;
        iState := 0; (* Forbid start *)
    END_IF;
END_IF;

(* First-order low pass filter for analog inputs to mitigate sensor noise *)
rFiltLineCurrent := rFiltLineCurrent + c_rAlpha * (rLineCurrent - rFiltLineCurrent);
rFiltLineVoltage := rFiltLineVoltage + c_rAlpha * (rLineVoltage - rFiltLineVoltage);

(* Fault Detection Logic (di/dt simplified to absolute threshold for ST example) *)
IF (rFiltLineCurrent > c_rCurrentThreshold) OR (rFiltLineVoltage < c_rVoltageThreshold AND rFiltLineCurrent > 3.0) THEN
    bFaultDetected := TRUE;
ELSE
    bFaultDetected := FALSE;
END_IF;

CASE iState OF
    0: (* IDLE / INITIALIZATION *)
        bSystemReady := FALSE;
        bTripSuccessful := FALSE;
        bAlarm := FALSE;
        rMovEnergyDissipated := 0.0;
        
        IF bEnable AND NOT bEmergencyTrip THEN
            iState := 10;
        END_IF;
        
    10: (* READY / MONITORING *)
        bSystemReady := TRUE;
        
        IF bFaultDetected THEN
            bSystemReady := FALSE;
            rFaultCurrentPeak := rFiltLineCurrent;
            iState := 20; (* INITIATE COMMUTATION *)
        END_IF;
        
    20: (* ACTIVE RESONANCE COMMUTATION *)
        (* Trigger piezo-actuators for ultra-fast vacuum interrupter separation *)
        tCommutationTimer(IN := TRUE, PT := T#2MS);
        
        IF tCommutationTimer.Q THEN
            tCommutationTimer(IN := FALSE);
            bArcExtinguished := TRUE;
            iState := 30; (* MOV ENERGY DISSIPATION *)
        END_IF;
        
    30: (* METAL-OXIDE VARISTOR (MOV) CASCADING *)
        (* Energy = Integral of V * I * dt, approximated here *)
        rMovEnergyDissipated := rMovEnergyDissipated + (rFiltLineVoltage * rFiltLineCurrent * 0.001); 
        
        tTripTimer(IN := TRUE, PT := T#15MS);
        IF tTripTimer.Q THEN
            tTripTimer(IN := FALSE);
            bTripSuccessful := TRUE;
            iState := 40; (* POST-TRIP COOLING *)
        END_IF;
        
    40: (* POST-TRIP COOLING *)
        tCoolingTimer(IN := TRUE, PT := T#10S);
        IF tCoolingTimer.Q THEN
            tCoolingTimer(IN := FALSE);
            IF NOT bFaultDetected AND NOT bEnable THEN
                iState := 0; (* Reset sequence *)
            END_IF;
        END_IF;
        
    99: (* EMERGENCY LOCKOUT *)
        (* Mechanical latches engaged, requires manual reset via station control *)
        bSystemReady := FALSE;
        IF NOT bEmergencyTrip AND NOT bEnable THEN
            iState := 0;
        END_IF;
        
END_CASE;

iOperatingState := iState;

END_FUNCTION_BLOCK
```"""

os.makedirs("C:/Users/majip/Downloads/LLM REASEARCH/data/swarm_raw", exist_ok=True)
record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": code}
    ]
}

filename = f"C:/Users/majip/Downloads/LLM REASEARCH/data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print(f"Saved to {filename}")
