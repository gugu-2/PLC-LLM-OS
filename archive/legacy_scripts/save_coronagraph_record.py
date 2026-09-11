import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Deep-Space Exoplanet Coronagraph Deformable Mirror**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., 4000-actuator electro-strictive wavefront phase correction, sub-nanometer speckle nulling algorithm, and low-order stray light rejection). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_CoronagraphDeformableMirror\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Deep-Space Exoplanet Coronagraph Deformable Mirror

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_CoronagraphDeformableMirror
VAR_INPUT
    (* System & Safety Inputs *)
    bEnable                 : BOOL;     (* Main activation command for the wavefront correction loop *)
    bEmergencyStop          : BOOL;     (* Hardware interlock / Safe mode trigger (Active LOW) *)
    rHighVoltageRail_V      : REAL;     (* Feedback from the 150V electro-strictive actuator power supply *)
    
    (* Metrology / Wavefront Sensor Inputs *)
    rZernikeTip             : REAL;     (* Low-order Tip aberration measurement (nanometers RMS) *)
    rZernikeTilt            : REAL;     (* Low-order Tilt aberration measurement (nanometers RMS) *)
    rSpeckleIntensity       : REAL;     (* Focal plane array localized speckle intensity (normalized 0.0-1.0) *)
    rThermalDrift_K         : REAL;     (* Optical bench thermal gradient drift in Kelvin *)
    
    (* Mode Control *)
    bEnableSpeckleNulling   : BOOL;     (* Engage ultra-high contrast sub-nanometer speckle nulling algorithm *)
END_VAR

VAR_OUTPUT
    (* System Status *)
    bSystemReady            : BOOL;     (* High-voltage initialized and deformable mirror thermalized *)
    bClosedLoopActive       : BOOL;     (* Adaptive optics loop is running and stabilized *)
    bAlarm                  : BOOL;     (* System fault (thermal, over-voltage, or uncorrectable wavefront) *)
    
    (* Actuator Commands & Telemetry *)
    rGlobalStrokeCmd_nm     : REAL;     (* Mean stroke command telemetry (nanometers) *)
    rPhaseErrorRMS_nm       : REAL;     (* Computed residual wavefront error *)
    iActiveSpeckleMode      : INT;      (* Currently active speckle nulling iteration mode (0-10) *)
END_VAR

VAR
    (* Internal State Variables *)
    iState                  : INT := 0; 
    
    (* Timers & Filters *)
    tInitializationTimer    : TON;
    rFilteredSpeckle        : REAL := 0.0;
    
    (* PI Controller Variables for Tip/Tilt *)
    rTipIntegral            : REAL := 0.0;
    rTiltIntegral           : REAL := 0.0;
    rKp                     : REAL := 0.45;
    rKi                     : REAL := 0.02;
    
    (* Safety Limits *)
    MAX_VOLTAGE_V           : REAL := 150.0;
    MAX_THERMAL_DRIFT       : REAL := 0.05;
    
    (* Math Constants *)
    rAlpha                  : REAL := 0.1; (* Low pass filter coefficient *)
END_VAR

(* === MAIN SAFETY & INTERLOCK LOGIC === *)
IF NOT bEmergencyStop THEN
    (* Immediate hardware safing *)
    bSystemReady        := FALSE;
    bClosedLoopActive   := FALSE;
    bAlarm              := TRUE;
    rGlobalStrokeCmd_nm := 0.0;
    rTipIntegral        := 0.0;
    rTiltIntegral       := 0.0;
    iState              := 99; (* Fault state *)
    RETURN;
END_IF;

(* Continuous Monitoring *)
IF rHighVoltageRail_V > MAX_VOLTAGE_V OR rThermalDrift_K > MAX_THERMAL_DRIFT THEN
    bAlarm := TRUE;
    bClosedLoopActive := FALSE;
    iState := 99; 
ELSE
    bAlarm := FALSE;
END_IF;

(* === MAIN STATE MACHINE === *)
CASE iState OF
    
    0: (* IDLE & STANDBY *)
        bSystemReady := FALSE;
        bClosedLoopActive := FALSE;
        
        IF bEnable AND NOT bAlarm THEN
            iState := 10;
        END_IF;
        
    10: (* INITIALIZE HIGH VOLTAGE & THERMAL SETTLE *)
        tInitializationTimer(IN := TRUE, PT := T#2S);
        
        IF tInitializationTimer.Q THEN
            tInitializationTimer(IN := FALSE);
            bSystemReady := TRUE;
            iState := 20;
        END_IF;
        
    20: (* LOW-ORDER WAVEFRONT CORRECTION (CLOSED LOOP) *)
        bClosedLoopActive := TRUE;
        
        (* PI Control for Tip/Tilt Rejection (Stray light mitigation) *)
        rTipIntegral := rTipIntegral + (rZernikeTip * rKi);
        rTiltIntegral := rTiltIntegral + (rZernikeTilt * rKi);
        
        (* Anti-windup *)
        IF rTipIntegral > 50.0 THEN rTipIntegral := 50.0; END_IF;
        IF rTipIntegral < -50.0 THEN rTipIntegral := -50.0; END_IF;
        IF rTiltIntegral > 50.0 THEN rTiltIntegral := 50.0; END_IF;
        IF rTiltIntegral < -50.0 THEN rTiltIntegral := -50.0; END_IF;
        
        rGlobalStrokeCmd_nm := (rZernikeTip * rKp) + rTipIntegral + (rZernikeTilt * rKp) + rTiltIntegral;
        rPhaseErrorRMS_nm := SQRT((rZernikeTip * rZernikeTip) + (rZernikeTilt * rZernikeTilt));
        
        IF bEnableSpeckleNulling THEN
            iState := 30;
        END_IF;
        
        IF NOT bEnable THEN
            iState := 0;
        END_IF;
        
    30: (* DEEP-SPACE SPECKLE NULLING (HIGH-ORDER CORRECTION) *)
        (* Filter speckle intensity (noisy focal plane telemetry) *)
        rFilteredSpeckle := (rAlpha * rSpeckleIntensity) + ((1.0 - rAlpha) * rFilteredSpeckle);
        
        IF rFilteredSpeckle > 0.8 THEN
            iActiveSpeckleMode := 1; (* Probe phase *)
        ELSIF rFilteredSpeckle > 0.3 THEN
            iActiveSpeckleMode := 2; (* Nulling iteration *)
        ELSE
            iActiveSpeckleMode := 3; (* Dark hole achieved *)
        END_IF;
        
        (* Exit condition for speckle nulling mode *)
        IF NOT bEnableSpeckleNulling THEN
            iActiveSpeckleMode := 0;
            iState := 20;
        END_IF;
        
    99: (* FAULT HANDLING *)
        bSystemReady := FALSE;
        bClosedLoopActive := FALSE;
        iActiveSpeckleMode := 0;
        
        (* Wait for operator reset via dropping enable signal *)
        IF NOT bEnable AND NOT bAlarm THEN
            iState := 0;
        END_IF;

END_CASE;

END_FUNCTION_BLOCK
```"""

os.makedirs('data/swarm_raw', exist_ok=True)
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
