import json, uuid, os

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Automated Subsea Pipeline Pipelay Vessel Dynamic Positioning System**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., 6-DOF dynamic thruster allocation, subsea pipeline tensioner cascade loops, environmental wave/wind feed-forward compensation, and heading hold). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\nFUNCTION_BLOCK FB_DynamicPositioning\n//...\nEND_FUNCTION_BLOCK\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Automated Subsea Pipeline Pipelay Vessel Dynamic Positioning System

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_Subsea_Pipelay_DP
VAR_INPUT
    (* Required: at least 4-8 physical inputs with types and comments *)
    bEnable                 : BOOL;     (* System enable signal *)
    bEmergencyStop          : BOOL;     (* Safety relay OK signal *)
    rWindSpeed              : REAL;     (* Environmental Wind Speed m/s *)
    rWindDir                : REAL;     (* Environmental Wind Direction degrees *)
    rWaveHeight             : REAL;     (* Environmental Wave Height m *)
    rWaveDir                : REAL;     (* Environmental Wave Direction degrees *)
    rCurrentSpeed           : REAL;     (* Sea Current Speed m/s *)
    rCurrentDir             : REAL;     (* Sea Current Direction degrees *)
    rVesselHeading          : REAL;     (* Measured Vessel Heading degrees *)
    rTargetHeading          : REAL;     (* Target Vessel Heading degrees *)
    rTargetPosX             : REAL;     (* Target X position in world coordinates *)
    rTargetPosY             : REAL;     (* Target Y position in world coordinates *)
    rMeasuredPosX           : REAL;     (* Measured X position in world coordinates *)
    rMeasuredPosY           : REAL;     (* Measured Y position in world coordinates *)
    rTensionerForce         : REAL;     (* Subsea pipeline tensioner force feedback kN *)
END_VAR
VAR_OUTPUT
    (* Required: at least 3-6 outputs with types and comments *)
    bSystemReady            : BOOL;     (* DP System ready status *)
    bAlarm                  : BOOL;     (* Fault alarm output *)
    rThruster1_Cmd          : REAL;     (* Azimuth thruster 1 thrust command % *)
    rThruster1_Azimuth      : REAL;     (* Azimuth thruster 1 angle command degrees *)
    rThruster2_Cmd          : REAL;     (* Azimuth thruster 2 thrust command % *)
    rThruster2_Azimuth      : REAL;     (* Azimuth thruster 2 angle command degrees *)
    rBowThruster_Cmd        : REAL;     (* Tunnel bow thruster command % *)
    rSurgeError             : REAL;     (* Calculated surge error *)
    rSwayError              : REAL;     (* Calculated sway error *)
    rHeadingError           : REAL;     (* Calculated heading error *)
END_VAR
VAR
    (* Internal state variables *)
    iState                  : INT := 0;
    tWatchdog               : TON;
    rErrorX                 : REAL;
    rErrorY                 : REAL;
    rCosHeading             : REAL;
    rSinHeading             : REAL;
    rFeedForwardSurge       : REAL;
    rFeedForwardSway        : REAL;
    rFeedForwardYaw         : REAL;
    rKp_Surge               : REAL := 1.5;
    rKi_Surge               : REAL := 0.05;
    rKd_Surge               : REAL := 2.0;
    rKp_Sway                : REAL := 1.5;
    rKi_Sway                : REAL := 0.05;
    rKd_Sway                : REAL := 2.0;
    rKp_Yaw                 : REAL := 2.5;
    rKi_Yaw                 : REAL := 0.1;
    rKd_Yaw                 : REAL := 5.0;
    rIntSurge               : REAL;
    rIntSway                : REAL;
    rIntYaw                 : REAL;
    rPrevSurgeError         : REAL;
    rPrevSwayError          : REAL;
    rPrevHeadingError       : REAL;
    rSurgeCmd               : REAL;
    rSwayCmd                : REAL;
    rYawCmd                 : REAL;
    PI                      : REAL := 3.14159265359;
END_VAR

(* === MAIN LOGIC === *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bAlarm := TRUE;
    rThruster1_Cmd := 0.0;
    rThruster2_Cmd := 0.0;
    rBowThruster_Cmd := 0.0;
    iState := 0;
    RETURN;
END_IF;

CASE iState OF
    0: (* IDLE *)
        bSystemReady := FALSE;
        bAlarm := FALSE;
        rThruster1_Cmd := 0.0;
        rThruster2_Cmd := 0.0;
        rBowThruster_Cmd := 0.0;
        IF bEnable THEN
            iState := 10;
            (* Reset Integrators *)
            rIntSurge := 0.0;
            rIntSway := 0.0;
            rIntYaw := 0.0;
        END_IF;

    10: (* RUNNING *)
        bSystemReady := TRUE;
        
        (* Coordinate Transformation (World to Vessel Body Frame) *)
        rErrorX := rTargetPosX - rMeasuredPosX;
        rErrorY := rTargetPosY - rMeasuredPosY;
        
        rCosHeading := COS(rVesselHeading * PI / 180.0);
        rSinHeading := SIN(rVesselHeading * PI / 180.0);
        
        rSurgeError := rErrorX * rCosHeading + rErrorY * rSinHeading;
        rSwayError  := -rErrorX * rSinHeading + rErrorY * rCosHeading;
        rHeadingError := rTargetHeading - rVesselHeading;
        
        (* Handle heading wrap-around *)
        IF rHeadingError > 180.0 THEN
            rHeadingError := rHeadingError - 360.0;
        ELSIF rHeadingError < -180.0 THEN
            rHeadingError := rHeadingError + 360.0;
        END_IF;
        
        (* Environmental Feedforward Compensation (Simplified model) *)
        rFeedForwardSurge := 0.05 * rWindSpeed * COS((rWindDir - rVesselHeading) * PI / 180.0) +
                             0.10 * rCurrentSpeed * COS((rCurrentDir - rVesselHeading) * PI / 180.0);
                             
        rFeedForwardSway  := 0.05 * rWindSpeed * SIN((rWindDir - rVesselHeading) * PI / 180.0) +
                             0.10 * rCurrentSpeed * SIN((rCurrentDir - rVesselHeading) * PI / 180.0);
                             
        (* Pipelay Tensioner Compensation - Pipelay operations induce significant surge force *)
        rFeedForwardSurge := rFeedForwardSurge + (rTensionerForce * 0.002);
        
        (* PID Control Algorithms *)
        rIntSurge := rIntSurge + (rSurgeError * 0.1); (* Assuming 100ms scan time *)
        rIntSway  := rIntSway + (rSwayError * 0.1);
        rIntYaw   := rIntYaw + (rHeadingError * 0.1);
        
        rSurgeCmd := (rKp_Surge * rSurgeError) + (rKi_Surge * rIntSurge) + (rKd_Surge * (rSurgeError - rPrevSurgeError)/0.1) + rFeedForwardSurge;
        rSwayCmd  := (rKp_Sway * rSwayError) + (rKi_Sway * rIntSway) + (rKd_Sway * (rSwayError - rPrevSwayError)/0.1) + rFeedForwardSway;
        rYawCmd   := (rKp_Yaw * rHeadingError) + (rKi_Yaw * rIntYaw) + (rKd_Yaw * (rHeadingError - rPrevHeadingError)/0.1);
        
        rPrevSurgeError := rSurgeError;
        rPrevSwayError := rSwayError;
        rPrevHeadingError := rHeadingError;
        
        (* Pseudo 6-DOF Thruster Allocation Logic *)
        (* Bow Thruster mainly handles sway and yaw *)
        rBowThruster_Cmd := LIMIT(-100.0, rSwayCmd * 0.4 + rYawCmd * 0.3, 100.0);
        
        (* Azimuth 1 (Port Aft) *)
        rThruster1_Cmd := LIMIT(0.0, SQRT(rSurgeCmd * rSurgeCmd + rSwayCmd * rSwayCmd) * 0.5, 100.0);
        IF rSurgeCmd <> 0.0 THEN
            rThruster1_Azimuth := ATAN(rSwayCmd / rSurgeCmd) * 180.0 / PI;
        END_IF;
        
        (* Azimuth 2 (Starboard Aft) *)
        rThruster2_Cmd := LIMIT(0.0, SQRT(rSurgeCmd * rSurgeCmd + rSwayCmd * rSwayCmd) * 0.5, 100.0);
        IF rSurgeCmd <> 0.0 THEN
            rThruster2_Azimuth := ATAN(rSwayCmd / rSurgeCmd) * 180.0 / PI;
        END_IF;
        
        IF NOT bEnable THEN
            iState := 0;
        END_IF;
        
    20: (* FAULT *)
        bSystemReady := FALSE;
        bAlarm := TRUE;
        rThruster1_Cmd := 0.0;
        rThruster2_Cmd := 0.0;
        rBowThruster_Cmd := 0.0;
        IF NOT bEnable AND NOT bEmergencyStop THEN
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
