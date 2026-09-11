import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Advanced Biomedical Multi-Leaf Collimator (MLC) Radiation Beam Shaper**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., 120-leaf sub-millimeter tungsten leaf positioning, dynamic intensity-modulated radiation therapy (IMRT) sliding window synchronization, and real-time EPID (Electronic Portal Imaging Device) verification). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_Biomedical_MLC_Controller\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Advanced Biomedical Multi-Leaf Collimator (MLC) Radiation Beam Shaper

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_Biomedical_MLC_Controller
(* 
   =============================================================================
   Title       : Advanced Biomedical Multi-Leaf Collimator (MLC) Controller
   Author      : Lumina Elite Automation Architect
   Description : Controls 120 tungsten leaves for sub-millimeter precision
                 dynamic intensity-modulated radiation therapy (IMRT). Includes
                 sliding window synchronization, real-time EPID verification,
                 and multi-layered safety interlocks.
   =============================================================================
*)
VAR_INPUT
    bSystemEnable           : BOOL;     (* System master enable *)
    bEmergencyStop          : BOOL;     (* Safety relay OK signal (Dual Channel) *)
    bBeamOn                 : BOOL;     (* Radiation beam active signal *)
    rTargetLeafPositions    : ARRAY[1..120] OF REAL; (* Target positions (mm) for 120 leaves *)
    rCurrentLeafPositions   : ARRAY[1..120] OF REAL; (* Encoders feedback (mm) for 120 leaves *)
    rDoseRate               : REAL;     (* Current LINAC dose rate (MU/min) *)
    rEPID_Fluence           : REAL;     (* Electronic Portal Imaging Device fluence feedback *)
    bGantryInterlock        : BOOL;     (* Gantry position safety interlock OK *)
END_VAR

VAR_OUTPUT
    bSystemReady            : BOOL;     (* MLC system ready for beam delivery *)
    rLeafVelocities         : ARRAY[1..120] OF REAL; (* Commanded velocities (mm/s) to leaf drives *)
    bBeamHold               : BOOL;     (* Signal to LINAC to hold beam delivery *)
    bAlarm                  : BOOL;     (* Critical fault alarm output *)
    iErrorCode              : INT;      (* Diagnostics error code *)
END_VAR

VAR
    iState                  : INT := 0; (* Internal state machine *)
    tMotionWatchdog         : TON;      (* Motion timeout watchdog *)
    i                       : INT;      (* Loop index *)
    rPosError               : REAL;     (* Position error per leaf *)
    rMaxPosError            : REAL;     (* Maximum position error across all leaves *)
    bInTolerance            : BOOL;     (* All leaves in tolerance flag *)
    
    (* PID Control Parameters per leaf *)
    Kp                      : REAL := 15.5; 
    Ki                      : REAL := 2.1;
    Kd                      : REAL := 0.5;
    rIntegral               : ARRAY[1..120] OF REAL;
    rLastError              : ARRAY[1..120] OF REAL;
    
    (* Safety limits *)
    MAX_VELOCITY            : REAL := 25.0; (* Max leaf speed mm/s *)
    MAX_TOLERANCE           : REAL := 0.25; (* Sub-millimeter tolerance mm *)
END_VAR

(* === MAIN LOGIC === *)

(* 1. Safety Interlocks & Emergency Stop *)
IF NOT bEmergencyStop OR NOT bGantryInterlock THEN
    bSystemReady := FALSE;
    bBeamHold := TRUE;
    bAlarm := TRUE;
    iErrorCode := 999; (* Critical Safety Interlock Tripped *)
    FOR i := 1 TO 120 DO
        rLeafVelocities[i] := 0.0;
    END_FOR;
    iState := 0;
    RETURN;
END_IF;

(* 2. State Machine *)
CASE iState OF
    0: (* IDLE & INITIALIZATION *)
        bSystemReady := FALSE;
        bBeamHold := TRUE;
        bAlarm := FALSE;
        iErrorCode := 0;
        
        FOR i := 1 TO 120 DO
            rLeafVelocities[i] := 0.0;
            rIntegral[i] := 0.0;
            rLastError[i] := 0.0;
        END_FOR;
        
        IF bSystemEnable THEN
            iState := 10;
        END_IF;

    10: (* POSITIONING / SLIDING WINDOW *)
        bInTolerance := TRUE;
        rMaxPosError := 0.0;
        
        (* Calculate PID and max error for all 120 leaves *)
        FOR i := 1 TO 120 DO
            rPosError := rTargetLeafPositions[i] - rCurrentLeafPositions[i];
            
            IF ABS(rPosError) > MAX_TOLERANCE THEN
                bInTolerance := FALSE;
            END_IF;
            
            IF ABS(rPosError) > rMaxPosError THEN
                rMaxPosError := ABS(rPosError);
            END_IF;
            
            (* PID Calculation *)
            rIntegral[i] := rIntegral[i] + (rPosError * 0.01); (* Assuming 10ms task cycle *)
            
            (* Anti-windup *)
            IF rIntegral[i] > 10.0 THEN rIntegral[i] := 10.0; END_IF;
            IF rIntegral[i] < -10.0 THEN rIntegral[i] := -10.0; END_IF;
            
            rLeafVelocities[i] := (Kp * rPosError) + (Ki * rIntegral[i]) + (Kd * (rPosError - rLastError[i]) / 0.01);
            rLastError[i] := rPosError;
            
            (* Velocity Saturation *)
            IF rLeafVelocities[i] > MAX_VELOCITY THEN
                rLeafVelocities[i] := MAX_VELOCITY;
            ELSIF rLeafVelocities[i] < -MAX_VELOCITY THEN
                rLeafVelocities[i] := -MAX_VELOCITY;
            END_IF;
        END_FOR;

        (* Beam Hold Logic: If leaves are moving too slowly to catch up with dose rate, hold beam *)
        IF NOT bInTolerance AND bBeamOn THEN
            bBeamHold := TRUE;
        ELSE
            bBeamHold := FALSE;
            bSystemReady := TRUE;
        END_IF;
        
        (* EPID Fluence Verification (Simulated check) *)
        IF bBeamOn AND rEPID_Fluence < (rDoseRate * 0.8) THEN
            (* Unexpected fluence drop could mean leaf collision or obstruction *)
            iState := 90; (* Fault *)
            iErrorCode := 101; 
        END_IF;

        IF NOT bSystemEnable THEN
            iState := 0;
        END_IF;

    90: (* FAULT STATE *)
        bSystemReady := FALSE;
        bBeamHold := TRUE;
        bAlarm := TRUE;
        FOR i := 1 TO 120 DO
            rLeafVelocities[i] := 0.0;
        END_FOR;
        
        IF NOT bSystemEnable THEN
            (* Require enable toggle to clear fault *)
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
