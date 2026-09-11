import json, uuid, os

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Next-Gen Space Telescope Beryllium Primary Mirror Segment Actuator**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., 10-nanometer resolution piezoelectric strut extension, thermal distortion wavefront pre-compensation, and highly redundant fault-tolerant absolute encoding). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_SpaceTelescope_MirrorActuator\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Next-Gen Space Telescope Beryllium Primary Mirror Segment Actuator

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_SpaceTelescope_MirrorActuator
VAR_INPUT
    (* High-precision physical inputs *)
    bEnableSys               : BOOL;     (* System master enable interlock *)
    bSafetyOK                : BOOL;     (* Hardware safety loop closed *)
    rCmdPosition_nm          : REAL;     (* Commanded extension in nanometers (10nm res) *)
    rActualPosA_nm           : REAL;     (* Main absolute encoder position *)
    rActualPosB_nm           : REAL;     (* Redundant absolute encoder position *)
    rTemperature_K           : REAL;     (* Beryllium segment temperature in Kelvin *)
    rThermalWavefrontComp    : REAL;     (* Thermal distortion pre-compensation offset *)
    bForceCalibrate          : BOOL;     (* Force recalibration sequence *)
END_VAR
VAR_OUTPUT
    (* Actuator drive outputs and status *)
    bActuatorReady           : BOOL;     (* Ready for precision tracking *)
    rPiezoDriveVolts         : REAL;     (* Commanded drive voltage to piezoelectric strut (0-150V) *)
    bPositionAchieved        : BOOL;     (* Position within tight tolerance band *)
    bThermalWarning          : BOOL;     (* Temperature gradient exceeds safe limits *)
    bEncoderFault            : BOOL;     (* Divergence between primary and redundant encoders *)
    iSystemStateOut          : INT;      (* Current state machine state *)
END_VAR
VAR
    (* Internal State and Filtering *)
    iState                   : INT := 0;
    rFilteredPos_nm          : REAL := 0.0;
    rPosError_nm             : REAL := 0.0;
    rIntegralTerm            : REAL := 0.0;
    rDerivativeTerm          : REAL := 0.0;
    rLastError_nm            : REAL := 0.0;
    
    (* Filter Constants and PID Gains *)
    rKp                      : REAL := 0.005;
    rKi                      : REAL := 0.0001;
    rKd                      : REAL := 0.015;
    rAlphaFilter             : REAL := 0.1;
    
    (* Timers and Safety bounds *)
    tSettleTimer             : TON;
    tSafetyTimer             : TON;
    rMaxVoltage_V            : REAL := 150.0;
    rMaxTempGradient         : REAL := 0.5;
    rEncoderTol_nm           : REAL := 5.0; (* Maximum allowed deviation between encoders *)
    
    bInitDone                : BOOL := FALSE;
END_VAR

(* === MAIN LOGIC === *)
(* 1. Safety Interlocks and Hardware Fault Detection *)
IF NOT bEnableSys OR NOT bSafetyOK THEN
    iState := 99; (* Fault state *)
END_IF;

(* Encoder validation - detect divergence *)
IF ABS(rActualPosA_nm - rActualPosB_nm) > rEncoderTol_nm THEN
    bEncoderFault := TRUE;
    iState := 99;
ELSE
    bEncoderFault := FALSE;
END_IF;

(* Initialise filter *)
IF NOT bInitDone THEN
    rFilteredPos_nm := rActualPosA_nm;
    bInitDone := TRUE;
END_IF;

(* Exponential moving average filter on primary encoder *)
rFilteredPos_nm := (rAlphaFilter * rActualPosA_nm) + ((1.0 - rAlphaFilter) * rFilteredPos_nm);

(* Thermal bounds checking *)
IF (rTemperature_K < 20.0) OR (rTemperature_K > 50.0) THEN
    bThermalWarning := TRUE;
ELSE
    bThermalWarning := FALSE;
END_IF;

CASE iState OF
    0: (* IDLE *)
        bActuatorReady := FALSE;
        rPiezoDriveVolts := 0.0;
        bPositionAchieved := FALSE;
        rIntegralTerm := 0.0;
        IF bEnableSys AND bSafetyOK AND NOT bEncoderFault AND NOT bForceCalibrate THEN
            iState := 10;
        ELSIF bForceCalibrate THEN
            iState := 5;
        END_IF;

    5: (* CALIBRATE *)
        (* Simulated zeroing procedure for absolute referencing *)
        rPiezoDriveVolts := 0.0;
        tSettleTimer(IN := TRUE, PT := T#2S);
        IF tSettleTimer.Q THEN
            tSettleTimer(IN := FALSE);
            iState := 10;
        END_IF;
        
    10: (* ACTIVE TRACKING *)
        bActuatorReady := TRUE;
        
        (* Calculate target with thermal pre-compensation applied *)
        rPosError_nm := (rCmdPosition_nm + rThermalWavefrontComp) - rFilteredPos_nm;
        
        (* PID Control Law for Piezoelectric Extension *)
        rIntegralTerm := rIntegralTerm + (rPosError_nm * rKi);
        
        (* Anti-windup clamping *)
        IF rIntegralTerm > 50.0 THEN
            rIntegralTerm := 50.0;
        ELSIF rIntegralTerm < -50.0 THEN
            rIntegralTerm := -50.0;
        END_IF;
        
        rDerivativeTerm := (rPosError_nm - rLastError_nm) * rKd;
        
        (* Compute Output Voltage *)
        rPiezoDriveVolts := (rPosError_nm * rKp) + rIntegralTerm + rDerivativeTerm;
        
        (* Clamp Output voltage to hardware limits (0 - 150V) *)
        IF rPiezoDriveVolts > rMaxVoltage_V THEN
            rPiezoDriveVolts := rMaxVoltage_V;
        ELSIF rPiezoDriveVolts < 0.0 THEN
            rPiezoDriveVolts := 0.0;
        END_IF;
        
        (* Update state variables *)
        rLastError_nm := rPosError_nm;
        
        (* Determine if settled within 10nm band *)
        IF ABS(rPosError_nm) <= 10.0 THEN
            tSettleTimer(IN := TRUE, PT := T#500MS);
            IF tSettleTimer.Q THEN
                bPositionAchieved := TRUE;
            END_IF;
        ELSE
            tSettleTimer(IN := FALSE);
            bPositionAchieved := FALSE;
        END_IF;
        
        IF bForceCalibrate THEN
            iState := 5;
        END_IF;

    99: (* FAULT SHUTDOWN *)
        bActuatorReady := FALSE;
        bPositionAchieved := FALSE;
        (* Gentle ramp down to zero voltage would be implemented here. For immediate safety: *)
        rPiezoDriveVolts := 0.0;
        
        (* Recovery condition *)
        IF bEnableSys AND bSafetyOK AND NOT bEncoderFault THEN
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

filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print(f"Saved to {filename}")
