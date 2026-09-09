import json, uuid, os
prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Advanced Semiconductor Deep Ultraviolet (DUV) Immersion Scanner**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., 193nm ArF excimer laser dose pulse energy matching, nanometer-level wafer stage interferometry, and dynamic lens heating (DLH) aberration correction). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_DUV_ImmersionScanner\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Advanced Semiconductor Deep Ultraviolet (DUV) Immersion Scanner

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_DUV_ImmersionScanner
VAR_INPUT
    (* Required: at least 4-8 physical inputs with types and comments *)
    bEnable                 : BOOL;     (* System enable signal for the scanner *)
    bEmergencyStop          : BOOL;     (* Safety relay OK signal; TRUE means OK, FALSE means E-STOP *)
    rLaserPulseEnergy_mJ    : REAL;     (* Measured 193nm ArF excimer laser pulse energy in millijoules *)
    lrWaferInterferometerX  : LREAL;    (* Wafer stage X-axis position from interferometry in nanometers *)
    lrWaferInterferometerY  : LREAL;    (* Wafer stage Y-axis position from interferometry in nanometers *)
    rLensTemperature_C      : REAL;     (* Projection lens internal temperature for DLH tracking in deg C *)
    rCoolantFlowRate_Lpm    : REAL;     (* Immersion hood ultrapure water (UPW) coolant flow rate in L/min *)
END_VAR
VAR_OUTPUT
    (* Required: at least 3-6 outputs with types and comments *)
    bSystemReady            : BOOL;     (* System ready status for exposure operations *)
    rDoseControlSignal      : REAL;     (* Control signal for next pulse energy adjustment (dose matching) *)
    rLensAberrationComp     : REAL;     (* Calculated Dynamic Lens Heating (DLH) aberration compensation *)
    bAlarm                  : BOOL;     (* Fault alarm output for process excursions *)
    bLaserTriggerEnable     : BOOL;     (* Hardware interlocked laser trigger enable signal *)
END_VAR
VAR
    (* Internal state variables *)
    iState                  : INT := 0;
    tWarmupTimer            : TON;
    tSettleTimer            : TON;
    
    (* Internal thresholds and calibration constants *)
    rTargetDose_mJ          : REAL := 15.5;      (* Nominal exposure dose per pulse *)
    rDoseKp                 : REAL := 0.85;      (* Proportional gain for dose matching loop *)
    rNominalTemp_C          : REAL := 22.0;      (* Reference thermal setpoint for optics *)
    rMaxTempDeviation       : REAL := 0.25;      (* Max allowed thermal deviation before fault *)
    rMinCoolantFlow         : REAL := 1.2;       (* Minimum UPW flow required to avoid bubble defects *)
    
    (* Filtered state *)
    rFilteredPulseEnergy    : REAL := 0.0;
    rAlphaFilter            : REAL := 0.2;
END_VAR

(* === MAIN LOGIC === *)
IF NOT bEmergencyStop THEN
    (* Immediate safe state on E-STOP drop *)
    bSystemReady        := FALSE;
    bAlarm              := TRUE;
    bLaserTriggerEnable := FALSE;
    rDoseControlSignal  := 0.0;
    rLensAberrationComp := 0.0;
    iState              := 0;
    RETURN;
END_IF;

CASE iState OF
    0: (* IDLE - Await System Enable *)
        bSystemReady        := FALSE;
        bAlarm              := FALSE;
        bLaserTriggerEnable := FALSE;
        rDoseControlSignal  := 0.0;
        
        IF bEnable THEN
            iState := 10;
        END_IF;

    10: (* WARMUP & IMMERSION FLUID STABILIZATION *)
        (* Check coolant flow for index of refraction stability *)
        IF rCoolantFlowRate_Lpm < rMinCoolantFlow THEN
            iState := 99; (* Coolant flow failure fault *)
        ELSE
            tWarmupTimer(IN := TRUE, PT := T#5S);
            IF tWarmupTimer.Q THEN
                tWarmupTimer(IN := FALSE);
                iState := 20;
            END_IF;
        END_IF;

    20: (* EXPOSURE RUNNING & CONTINUOUS CONTROL *)
        (* 1. Dynamic Lens Heating (DLH) Compensation *)
        rLensAberrationComp := (rLensTemperature_C - rNominalTemp_C) * 0.0245; 
        
        (* 2. Excimer Laser Dose Matching *)
        (* First-order IIR filter on pulse energy for stability *)
        IF rLaserPulseEnergy_mJ > 0.0 THEN
            rFilteredPulseEnergy := (rAlphaFilter * rLaserPulseEnergy_mJ) + ((1.0 - rAlphaFilter) * rFilteredPulseEnergy);
            rDoseControlSignal   := (rTargetDose_mJ - rFilteredPulseEnergy) * rDoseKp;
        ELSE
            rDoseControlSignal   := 0.0;
        END_IF;
        
        (* 3. Operational Interlocks *)
        bSystemReady        := TRUE;
        bLaserTriggerEnable := TRUE;
        
        (* 4. Fault Detection *)
        IF ABS(rLensTemperature_C - rNominalTemp_C) > rMaxTempDeviation THEN
            iState := 99; (* Thermal excursion fault *)
        END_IF;
        
        IF rCoolantFlowRate_Lpm < (rMinCoolantFlow * 0.9) THEN
            iState := 99; (* Coolant flow drop during exposure *)
        END_IF;
        
        IF NOT bEnable THEN
            bLaserTriggerEnable := FALSE;
            tSettleTimer(IN := TRUE, PT := T#2S);
            IF tSettleTimer.Q THEN
                tSettleTimer(IN := FALSE);
                iState := 0;
            END_IF;
        END_IF;

    99: (* FAULT STATE *)
        bSystemReady        := FALSE;
        bAlarm              := TRUE;
        bLaserTriggerEnable := FALSE;
        rDoseControlSignal  := 0.0;
        
        (* Require operator to disable system to clear fault *)
        IF NOT bEnable THEN
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
