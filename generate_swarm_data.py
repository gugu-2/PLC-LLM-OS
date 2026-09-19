import json
import uuid
import os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: High-Volume Automotive Manufacturing Paint Shop Electrodeposition (e-Coat) Rectifier Current Profiling**

Task: Invent a highly complex, ultra-realistic control scenario for this domain. Make this code EVEN BETTER, MORE ADVANCED, and MORE RIGOROUS than previous iterations. Include extreme edge-case handling, advanced math, and robust fault-tolerance.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_PaintShop_ECoatRectifier\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: High-Volume Automotive Manufacturing Paint Shop Electrodeposition (e-Coat) Rectifier Current Profiling

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_PaintShop_ECoatRectifier
VAR_INPUT
    (* Required: at least 4-8 physical inputs with types and comments *)
    bEnable              : BOOL;     (* System enable signal from main supervisory PLC *)
    bEmergencyStop       : BOOL;     (* Safety relay OK signal (Active High = Safe) *)
    rProcessVar          : REAL;     (* Physical measurement e.g. temperature in deg C of e-coat bath *)
    rConveyorSpeed       : REAL;     (* Speed of the car body conveyor in m/min *)
    rAnodeCurrentFB      : REAL;     (* Rectifier current feedback in Amps *)
    rTargetFilmThickness : REAL;     (* Desired dry film thickness in micrometers (um) *)
    bBodyInZone          : BOOL;     (* Photoeye proximity indicating car body is in deposition zone *)
END_VAR
VAR_OUTPUT
    (* Required: at least 3-6 outputs with types and comments *)
    bSystemReady         : BOOL;     (* System ready status / Handshake to SCADA *)
    rControlOutput       : REAL;     (* Control signal to actuator: Target Rectifier Current in Amps *)
    bAlarm               : BOOL;     (* Fault alarm output for Horn/Beacon *)
    iFaultCode           : INT;      (* Advanced diagnostics code (0=OK, 1=E-Stop, 2=Temp, 3=Overcurrent) *)
END_VAR
VAR
    (* Internal state variables *)
    iState               : INT := 0;
    tTimer               : TON;
    rFilteredCurrent     : REAL := 0.0; (* EWMA Filtered current feedback *)
    rFilterAlpha         : REAL := 0.15; (* Low-pass filter coefficient for noise immunity *)
    rCalculatedDemand    : REAL := 0.0; (* Dynamically profiled target current demand *)
    rAmpMinIntegration   : REAL := 0.0; (* Coulombs / Amp-minutes integrated over immersion *)
    rTargetAmpMin        : REAL := 0.0; (* Calculated Coulombs required for thickness *)
    
    (* PID Variables for holding phase *)
    rError               : REAL := 0.0;
    rKp                  : REAL := 1.25;
    rKi                  : REAL := 0.45;
    rIntegral            : REAL := 0.0;
END_VAR

(* === MAIN LOGIC === *)
(* Signal Processing: Exponentially Weighted Moving Average (EWMA) for Rectifier Feedback *)
rFilteredCurrent := (rFilterAlpha * rAnodeCurrentFB) + ((1.0 - rFilterAlpha) * rFilteredCurrent);

(* Safety Interlocks & Emergency Halt Priority Level 0 *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    rControlOutput := 0.0;
    bAlarm := TRUE;
    iFaultCode := 1; (* E-Stop Active *)
    iState := 0;
    RETURN;
END_IF;

(* Process Tolerance Interlocks (Temperature bounds for Paint Adhesion) *)
IF (rProcessVar < 26.5) OR (rProcessVar > 35.0) THEN
    bSystemReady := FALSE;
    rControlOutput := 0.0;
    bAlarm := TRUE;
    iFaultCode := 2; (* Bath Temperature out of Spec *)
    iState := 0;
    RETURN;
END_IF;

(* Catastrophic Overcurrent Protection *)
IF rFilteredCurrent > 2500.0 THEN
    bSystemReady := FALSE;
    rControlOutput := 0.0;
    bAlarm := TRUE;
    iFaultCode := 3; (* Arc/Overcurrent Detected *)
    iState := 0;
    RETURN;
END_IF;

(* Electrodeposition Profiling State Machine *)
CASE iState OF
    0: (* IDLE - Waiting for Car Body *)
        bSystemReady := TRUE;
        bAlarm := FALSE;
        iFaultCode := 0;
        rControlOutput := 0.0;
        rCalculatedDemand := 0.0;
        rAmpMinIntegration := 0.0;
        rIntegral := 0.0;
        
        (* Faraday's law approximation: Amp-minutes required per micron thickness per body area *)
        rTargetAmpMin := rTargetFilmThickness * 45.5; 
        
        (* Transition Trigger: System enabled, Conveyor moving, Body arrived *)
        IF bEnable AND bBodyInZone AND (rConveyorSpeed > 0.5) THEN
            iState := 10;
        END_IF;

    10: (* PRE-WETTING DELAY *)
        bSystemReady := FALSE; (* Process Active *)
        tTimer(IN := TRUE, PT := T#3S);
        IF tTimer.Q THEN
            tTimer(IN := FALSE);
            iState := 20;
        END_IF;

    20: (* CONTROLLED RAMP-UP (Soft Start to prevent Rupture) *)
        rCalculatedDemand := rCalculatedDemand + 75.0; (* 75 Amps per PLC cycle ramp *)
        IF rCalculatedDemand >= 1200.0 THEN
            rCalculatedDemand := 1200.0;
            iState := 30;
        END_IF;
        rControlOutput := rCalculatedDemand;

    30: (* ACTIVE DEPOSITION (PID Control Loop) *)
        (* Integrate Amp-Minutes using simple Euler summation *)
        (* Assuming PLC scan time ~100ms, dt = 0.1s -> 1/600 minutes *)
        rAmpMinIntegration := rAmpMinIntegration + (rFilteredCurrent * 0.0001667);
        
        (* PID Control against theoretical max thickness demand *)
        rError := 1200.0 - rFilteredCurrent;
        rIntegral := rIntegral + (rError * rKi);
        
        (* Anti-windup limit *)
        IF rIntegral > 500.0 THEN rIntegral := 500.0; END_IF;
        IF rIntegral < -500.0 THEN rIntegral := -500.0; END_IF;
        
        rControlOutput := (rError * rKp) + rIntegral;
        
        (* Exit Phase Criteria: Target Coulomb limit reached OR Body left zone *)
        IF (rAmpMinIntegration >= rTargetAmpMin) OR NOT bBodyInZone THEN
            iState := 40;
        END_IF;

    40: (* RAMP-DOWN & DRAIN *)
        rCalculatedDemand := rControlOutput - 150.0; (* Fast step down *)
        IF rCalculatedDemand <= 0.0 THEN
            rCalculatedDemand := 0.0;
            iState := 50;
        END_IF;
        rControlOutput := rCalculatedDemand;

    50: (* COMPLETE / RESET *)
        bSystemReady := TRUE;
        IF NOT bEnable THEN
            iState := 0;
        END_IF;

END_CASE;

(* Hardware Safe Output Clamping *)
IF rControlOutput < 0.0 THEN
    rControlOutput := 0.0;
ELSIF rControlOutput > 2000.0 THEN
    rControlOutput := 2000.0;
END_IF;

END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump({"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}, f, ensure_ascii=False)
print(f"Saved to {filename}")
