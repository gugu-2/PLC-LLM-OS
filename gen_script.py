import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: High-Energy Free Electron Laser (FEL) Beamline Stabilizer**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Undulator magnetic gap micrometer positioning, electron bunch arrival time jitter compensation, and mirror thermal distortion active cooling). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_FEL_BeamlineStabilizer\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
   record = {\"messages\": [{\"role\": \"user\", \"content\": prompt}, {\"role\": \"assistant\", \"content\": code}]}
   with open(f\"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json\", \"w\", encoding=\"utf-8\") as f:
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
6. REPLY with: EVOLUTION COMPLETE: High-Energy Free Electron Laser (FEL) Beamline Stabilizer

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_FEL_BeamlineStabilizer
VAR_INPUT
    (* Required: at least 4-8 physical inputs with types and comments *)
    bSystemEnable           : BOOL;     (* System master enable signal *)
    bEmergencyStopOk        : BOOL;     (* Safety relay OK signal, normally high *)
    rUndulatorGapCmd        : REAL;     (* Desired undulator magnetic gap in mm *)
    rUndulatorGapAct        : REAL;     (* Actual undulator magnetic gap feedback in mm *)
    rArrivalJitterPs        : REAL;     (* Electron bunch arrival time jitter in picoseconds *)
    rMirrorTempAct          : REAL;     (* Mirror surface actual temperature in deg C *)
    rCoolantTempAct         : REAL;     (* Coolant inlet temperature in deg C *)
    bBeamDumpEngaged        : BOOL;     (* Beam dump safety status *)
END_VAR
VAR_OUTPUT
    (* Required: at least 3-6 outputs with types and comments *)
    bSystemReady            : BOOL;     (* System fully operational and ready for beam *)
    rUndulatorMotorDrive    : REAL;     (* Control signal to gap micrometer drive [-10V..10V] *)
    rCoolerValveCmd         : REAL;     (* Chiller valve position command 0..100% *)
    rJitterCompRfPhase      : REAL;     (* RF phase compensation signal for timing jitter in degrees *)
    bWarningAlarm           : BOOL;     (* Non-critical warning alarm *)
    bCriticalFault          : BOOL;     (* Critical fault requiring immediate beam dump *)
END_VAR
VAR
    (* Internal state variables *)
    iState                  : INT := 0; (* Main state machine state *)
    tStartupDelay           : TON;      (* Timer for system initialization *)
    
    (* Filter and control variables *)
    rGapError               : REAL;     (* Error between commanded and actual gap *)
    rGapIntegral            : REAL;     (* Integral accumulator for gap PID *)
    rGapDerivative          : REAL;     (* Derivative term for gap PID *)
    rLastGapError           : REAL;     (* Previous cycle gap error *)
    
    (* Filtered inputs *)
    rFiltMirrorTemp         : REAL;     (* Low-pass filtered mirror temperature *)
    rFiltJitter             : REAL;     (* Filtered jitter reading *)
    
    (* Constants *)
    Kp_Gap                  : REAL := 12.5;
    Ki_Gap                  : REAL := 2.1;
    Kd_Gap                  : REAL := 0.5;
    Max_Motor_Drive         : REAL := 10.0;
    Min_Motor_Drive         : REAL := -10.0;
    Temp_Setpoint           : REAL := 24.5; (* Desired mirror temp in deg C *)
    Filter_Alpha            : REAL := 0.15; (* IIR filter coefficient *)
END_VAR

(* === MAIN LOGIC === *)

(* Emergency and Safety Interlocks *)
IF NOT bEmergencyStopOk OR bBeamDumpEngaged THEN
    bSystemReady := FALSE;
    bCriticalFault := TRUE;
    rUndulatorMotorDrive := 0.0;
    rCoolerValveCmd := 100.0; (* Full cooling on fault *)
    rJitterCompRfPhase := 0.0;
    iState := 999; (* FAULT STATE *)
    RETURN;
END_IF;

(* Input Filtering (Sensor Noise Reduction) *)
rFiltMirrorTemp := (Filter_Alpha * rMirrorTempAct) + ((1.0 - Filter_Alpha) * rFiltMirrorTemp);
rFiltJitter := (Filter_Alpha * rArrivalJitterPs) + ((1.0 - Filter_Alpha) * rFiltJitter);

CASE iState OF
    0: (* IDLE *)
        bSystemReady := FALSE;
        bWarningAlarm := FALSE;
        bCriticalFault := FALSE;
        rUndulatorMotorDrive := 0.0;
        rCoolerValveCmd := 0.0;
        
        IF bSystemEnable THEN
            iState := 10;
        END_IF;

    10: (* INITIALIZING *)
        tStartupDelay(IN := TRUE, PT := T#5S);
        (* Pre-cool the mirror before enabling beam *)
        IF rFiltMirrorTemp > Temp_Setpoint + 1.0 THEN
            rCoolerValveCmd := 75.0;
        ELSE
            rCoolerValveCmd := 25.0;
        END_IF;
        
        IF tStartupDelay.Q THEN
            tStartupDelay(IN := FALSE);
            iState := 20;
        END_IF;

    20: (* RUNNING & STABILIZATION *)
        (* 1. Undulator Gap Micrometer PID Control *)
        rGapError := rUndulatorGapCmd - rUndulatorGapAct;
        rGapIntegral := rGapIntegral + (rGapError * 0.01); (* Assuming 10ms cycle time *)
        
        (* Anti-windup protection *)
        IF rGapIntegral > 10.0 THEN rGapIntegral := 10.0; END_IF;
        IF rGapIntegral < -10.0 THEN rGapIntegral := -10.0; END_IF;
        
        rGapDerivative := (rGapError - rLastGapError) / 0.01;
        rLastGapError := rGapError;
        
        rUndulatorMotorDrive := (Kp_Gap * rGapError) + (Ki_Gap * rGapIntegral) + (Kd_Gap * rGapDerivative);
        
        (* Drive Saturation Output Limitation *)
        IF rUndulatorMotorDrive > Max_Motor_Drive THEN
            rUndulatorMotorDrive := Max_Motor_Drive;
        ELSIF rUndulatorMotorDrive < Min_Motor_Drive THEN
            rUndulatorMotorDrive := Min_Motor_Drive;
        END_IF;
        
        (* 2. Mirror Thermal Distortion Active Cooling *)
        (* Simple proportional control for cooling valve *)
        rCoolerValveCmd := 50.0 + (rFiltMirrorTemp - Temp_Setpoint) * 10.0;
        IF rCoolerValveCmd > 100.0 THEN rCoolerValveCmd := 100.0; END_IF;
        IF rCoolerValveCmd < 0.0 THEN rCoolerValveCmd := 0.0; END_IF;
        
        (* 3. Electron Bunch Arrival Time Jitter Compensation *)
        (* Map picosecond jitter to RF phase degrees. (Example constant: 0.1 deg/ps) *)
        rJitterCompRfPhase := rFiltJitter * 0.1;
        
        (* Set system ready when all loops are within tolerance *)
        IF ABS(rGapError) < 0.05 AND ABS(rFiltMirrorTemp - Temp_Setpoint) < 0.5 THEN
            bSystemReady := TRUE;
        ELSE
            bSystemReady := FALSE;
        END_IF;
        
        (* Warnings *)
        IF ABS(rGapError) > 2.0 OR rFiltMirrorTemp > Temp_Setpoint + 5.0 THEN
            bWarningAlarm := TRUE;
        ELSE
            bWarningAlarm := FALSE;
        END_IF;
        
        IF NOT bSystemEnable THEN
            iState := 0;
        END_IF;

    999: (* FAULT HANDLING *)
        bSystemReady := FALSE;
        bWarningAlarm := TRUE;
        bCriticalFault := TRUE;
        (* Require manual reset of Enable after fault is cleared *)
        IF NOT bEmergencyStopOk OR bBeamDumpEngaged THEN
            (* Stay in fault *)
        ELSIF NOT bSystemEnable THEN
            iState := 0; (* Reset sequence *)
        END_IF;

END_CASE;

END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump({"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}, f, ensure_ascii=False)
print(f"Saved to {filename}")
