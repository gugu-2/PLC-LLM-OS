import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Advanced Deep-Space Optical Interferometer Delay Line**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Picometer-precision piezoelectric carriage tracking, laser metrology active fringe stabilization, and micro-gravity jitter active damping). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\nFUNCTION_BLOCK FB_InterferometerDelayLine\n//...\nEND_FUNCTION_BLOCK\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Advanced Deep-Space Optical Interferometer Delay Line

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_DeepSpaceInterferometerDelayLine
VAR_INPUT
    bEnable                 : BOOL;     (* System master enable *)
    bEmergencyStop          : BOOL;     (* Safety relay / interlock OK signal *)
    rMetrologyPosition      : REAL;     (* Laser metrology readback in nanometers *)
    rTargetPosition         : REAL;     (* Commanded delay line position in nanometers *)
    rJitterSensorX          : REAL;     (* Micro-gravity jitter accelerometer X axis *)
    rJitterSensorY          : REAL;     (* Micro-gravity jitter accelerometer Y axis *)
END_VAR
VAR_OUTPUT
    bSystemReady            : BOOL;     (* System initialization and tracking ready *)
    rPiezoDriveV            : REAL;     (* Fast piezoelectric actuator drive voltage (-10 to 10V) *)
    rVoiceCoilDriveA        : REAL;     (* Coarse voice coil carriage drive current (-5 to 5A) *)
    bTrackingLocked         : BOOL;     (* Active fringe stabilization lock achieved *)
    bAlarm                  : BOOL;     (* System fault or tolerance violation alarm *)
END_VAR
VAR
    (* Internal state variables *)
    iState                  : INT := 0;
    tStartupTimer           : TON;
    tLockTimeout            : TON;
    
    (* Filter variables *)
    rFilteredPosition       : REAL := 0.0;
    rPosError               : REAL := 0.0;
    rPosErrorIntegral       : REAL := 0.0;
    rPosErrorDerivative     : REAL := 0.0;
    rLastPosError           : REAL := 0.0;
    
    (* PID Constants *)
    Kp_Fine                 : REAL := 0.05;
    Ki_Fine                 : REAL := 0.001;
    Kd_Fine                 : REAL := 0.02;
    Kp_Coarse               : REAL := 1.2;
    
    (* Anti-windup and limits *)
    rMaxIntegral            : REAL := 500.0;
    rMaxPiezoV              : REAL := 10.0;
    rMaxCoilA               : REAL := 5.0;
    
    (* Kalman-esque simplistic filter state for jitter *)
    rJitterMagnitude        : REAL := 0.0;
    rActiveDampingFeedback  : REAL := 0.0;
END_VAR

(* === MAIN LOGIC === *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bTrackingLocked := FALSE;
    bAlarm := TRUE;
    rPiezoDriveV := 0.0;
    rVoiceCoilDriveA := 0.0;
    iState := 0;
    RETURN;
END_IF;

(* Calculate magnitude of external mechanical jitter *)
rJitterMagnitude := SQRT(rJitterSensorX * rJitterSensorX + rJitterSensorY * rJitterSensorY);

(* Implement simple low-pass filter for metrology reading to avoid high-frequency quantization noise *)
rFilteredPosition := rFilteredPosition + 0.8 * (rMetrologyPosition - rFilteredPosition);
rPosError := rTargetPosition - rFilteredPosition;

CASE iState OF
    0: (* IDLE & INITIALIZATION *)
        bSystemReady := FALSE;
        bTrackingLocked := FALSE;
        bAlarm := FALSE;
        rPiezoDriveV := 0.0;
        rVoiceCoilDriveA := 0.0;
        
        IF bEnable THEN
            iState := 10;
        END_IF;

    10: (* CALIBRATION & WARMUP *)
        (* Simulate hardware warmup and self-check phase *)
        tStartupTimer(IN := TRUE, PT := T#2S);
        IF tStartupTimer.Q THEN
            tStartupTimer(IN := FALSE);
            bSystemReady := TRUE;
            iState := 20;
        END_IF;

    20: (* COARSE TRACKING (Voice Coil) *)
        (* In coarse tracking, error is handled primarily by voice coil *)
        rVoiceCoilDriveA := rPosError * Kp_Coarse;
        
        (* Saturate voice coil drive *)
        IF rVoiceCoilDriveA > rMaxCoilA THEN
            rVoiceCoilDriveA := rMaxCoilA;
        ELSIF rVoiceCoilDriveA < -rMaxCoilA THEN
            rVoiceCoilDriveA := -rMaxCoilA;
        END_IF;
        
        (* Zero the piezo drive during coarse movement *)
        rPiezoDriveV := 0.0;
        rPosErrorIntegral := 0.0;
        rLastPosError := rPosError;
        
        (* Check if we are within the handover threshold (e.g., 50 nm) *)
        IF ABS(rPosError) < 50.0 THEN
            iState := 30;
        END_IF;
        
        IF NOT bEnable THEN
            iState := 0;
        END_IF;

    30: (* FINE TRACKING & ACTIVE FRINGE LOCK (Piezoelectric) *)
        (* Integral action with anti-windup *)
        rPosErrorIntegral := rPosErrorIntegral + rPosError;
        IF rPosErrorIntegral > rMaxIntegral THEN
            rPosErrorIntegral := rMaxIntegral;
        ELSIF rPosErrorIntegral < -rMaxIntegral THEN
            rPosErrorIntegral := -rMaxIntegral;
        END_IF;
        
        (* Derivative action *)
        rPosErrorDerivative := rPosError - rLastPosError;
        rLastPosError := rPosError;
        
        (* Compute active damping feedback derived from jitter sensors *)
        rActiveDampingFeedback := rJitterMagnitude * 0.005; 
        
        (* Fine PID control calculation for Piezo actuator *)
        rPiezoDriveV := (rPosError * Kp_Fine) + (rPosErrorIntegral * Ki_Fine) + (rPosErrorDerivative * Kd_Fine) - rActiveDampingFeedback;
        
        (* Saturate piezo drive *)
        IF rPiezoDriveV > rMaxPiezoV THEN
            rPiezoDriveV := rMaxPiezoV;
        ELSIF rPiezoDriveV < -rMaxPiezoV THEN
            rPiezoDriveV := -rMaxPiezoV;
        END_IF;
        
        (* Determine fringe lock condition (< 5 nm error) *)
        IF ABS(rPosError) < 5.0 THEN
            bTrackingLocked := TRUE;
            tLockTimeout(IN := FALSE);
        ELSE
            bTrackingLocked := FALSE;
            (* If we lose lock for too long, drop back to coarse tracking *)
            tLockTimeout(IN := TRUE, PT := T#500MS);
            IF tLockTimeout.Q THEN
                iState := 20;
                tLockTimeout(IN := FALSE);
            END_IF;
        END_IF;
        
        IF NOT bEnable THEN
            iState := 0;
        END_IF;
        
    ELSE
        iState := 0;
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
