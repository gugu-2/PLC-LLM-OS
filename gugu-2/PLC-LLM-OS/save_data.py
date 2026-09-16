import os, json, uuid

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Ultra-High Vacuum (UHV) Molecular Beam Epitaxy (MBE) Chamber**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Effusion cell thermal profile management, cryopump regeneration sequence, and atomic flux reflection high-energy electron diffraction (RHEED) timing). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_MBE_VacuumChamber\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Ultra-High Vacuum (UHV) Molecular Beam Epitaxy (MBE) Chamber

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_MBE_UHV_Control
VAR_INPUT
    (* Essential Safety and System Status *)
    bSystemEnable       : BOOL;     (* Global enable for the MBE process *)
    bEmergencyStop      : BOOL;     (* Main safety loop OK - Active High *)
    bCoolingWaterOK     : BOOL;     (* Cryopump and cell water jacket flow OK *)
    
    (* Process Variables *)
    rChamberPressure    : REAL;     (* Current main chamber pressure in Torr (e.g. 1.0E-10) *)
    rCryoTemp           : REAL;     (* Cryopump temperature in Kelvin *)
    rEffusionCellTemp   : REAL;     (* Effusion cell actual temperature in deg C *)
    rRHEED_Intensity    : REAL;     (* RHEED specular spot intensity (normalized 0-1) *)
    
    (* Setpoints *)
    rCellTempSetpoint   : REAL;     (* Target effusion cell temperature in deg C *)
    rBasePressureSp     : REAL;     (* Target base pressure before deposition *)
END_VAR
VAR_OUTPUT
    (* Actuators and Status *)
    bSystemReady        : BOOL;     (* UHV condition met, ready for epitaxy *)
    bGateValveOpen      : BOOL;     (* Main isolation gate valve control *)
    bCryopumpRegen      : BOOL;     (* Initiate cryopump regeneration cycle *)
    rCellHeaterPWM      : REAL;     (* Effusion cell heater power output (0-100%) *)
    bShutterOpen        : BOOL;     (* Effusion cell pneumatic shutter control *)
    
    (* Diagnostics *)
    bAlarm              : BOOL;     (* General fault alarm *)
    iFaultCode          : INT;      (* Detailed fault code for HMI *)
END_VAR
VAR
    (* Internal State *)
    iState              : INT := 0; (* Main state machine step *)
    iCellState          : INT := 0; (* Effusion cell thermal state *)
    
    (* Timers and Filters *)
    tSoakTimer          : TON;
    tRegenTimer         : TON;
    rPressureFiltered   : REAL := 1.0;
    
    (* PID Control for Effusion Cell *)
    rErrorSum           : REAL := 0.0;
    rLastError          : REAL := 0.0;
    rKp                 : REAL := 2.5;
    rKi                 : REAL := 0.05;
    rKd                 : REAL := 0.1;
    rError              : REAL;
    rDerivative         : REAL;
END_VAR

(* === MAIN LOGIC === *)
(* 1. Safety Interlocks and Hardware Protection *)
IF NOT bEmergencyStop OR NOT bCoolingWaterOK THEN
    bSystemReady   := FALSE;
    bGateValveOpen := FALSE;
    bShutterOpen   := FALSE;
    rCellHeaterPWM := 0.0;
    bAlarm         := TRUE;
    iFaultCode     := 99; (* 99 = Critical Hardware Safety Fault *)
    iState         := 0;
    RETURN;
END_IF;

(* 2. Sensor Noise Filtering (Exponential Moving Average) *)
rPressureFiltered := rPressureFiltered + 0.1 * (rChamberPressure - rPressureFiltered);

(* 3. Main Chamber State Machine *)
CASE iState OF
    0: (* IDLE *)
        bSystemReady := FALSE;
        bAlarm       := FALSE;
        iFaultCode   := 0;
        IF bSystemEnable THEN
            iState := 10;
        END_IF;
        
    10: (* PUMPDOWN & CRYO CHECK *)
        IF rCryoTemp > 15.0 THEN
            bCryopumpRegen := TRUE;
            tRegenTimer(IN := TRUE, PT := T#12H);
            IF tRegenTimer.Q THEN
                bCryopumpRegen := FALSE;
                tRegenTimer(IN := FALSE);
            END_IF;
        ELSE
            bCryopumpRegen := FALSE;
            IF rPressureFiltered <= rBasePressureSp THEN
                bGateValveOpen := TRUE;
                iState := 20;
            END_IF;
        END_IF;
        
    20: (* THERMAL PREP *)
        IF rEffusionCellTemp >= (rCellTempSetpoint - 2.0) THEN
            tSoakTimer(IN := TRUE, PT := T#30M);
            IF tSoakTimer.Q THEN
                iState := 30;
                bSystemReady := TRUE;
            END_IF;
        ELSE
            tSoakTimer(IN := FALSE);
        END_IF;
        
    30: (* DEPOSITION *)
        IF rRHEED_Intensity > 0.8 THEN
            bShutterOpen := TRUE;
        END_IF;
        
        IF NOT bSystemEnable THEN
            bShutterOpen := FALSE;
            bSystemReady := FALSE;
            iState := 0;
        END_IF;
        
    ELSE
        iState := 0;
END_CASE;

(* 4. PID Controller *)
IF iState >= 20 THEN
    rError := rCellTempSetpoint - rEffusionCellTemp;
    rErrorSum := rErrorSum + rError;
    
    IF rErrorSum > 1000.0 THEN rErrorSum := 1000.0; END_IF;
    IF rErrorSum < -1000.0 THEN rErrorSum := -1000.0; END_IF;
    
    rDerivative := rError - rLastError;
    rLastError := rError;
    
    rCellHeaterPWM := (rKp * rError) + (rKi * rErrorSum) + (rKd * rDerivative);
    
    IF rCellHeaterPWM > 100.0 THEN rCellHeaterPWM := 100.0; END_IF;
    IF rCellHeaterPWM < 0.0 THEN rCellHeaterPWM := 0.0; END_IF;
ELSE
    rCellHeaterPWM := 0.0;
    rErrorSum := 0.0;
    rLastError := 0.0;
END_IF;

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
