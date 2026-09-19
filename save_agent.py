import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Large-Scale Agricultural GPS-Guided Autonomous Harvester Header Height and Threshing Drum Sync**

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_Harvester_HeaderThreshing\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Large-Scale Agricultural GPS-Guided Autonomous Harvester Header Height and Threshing Drum Sync

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_AutonomousHarvesterHeaderThreshingSync
VAR_INPUT
    bEnableSys                  : BOOL;   (* Main System Enable from Cab / Autonomous Controller *)
    bEmergencyStop              : BOOL;   (* Safety loop feedback - TRUE = OK *)
    rGPSHeadingErr              : REAL;   (* GPS Tracking error relative to swath (m) *)
    rCropDensitySensor          : REAL;   (* Lidar/Radar crop density reading ahead of header (kg/m^3) *)
    rActualHeaderHeight         : REAL;   (* Current header height measured by ground radar (mm) *)
    rTargetHeaderHeight         : REAL;   (* Desired header height (mm) *)
    rActualThreshingRPM         : REAL;   (* Measured RPM of threshing drum *)
    rGroundSpeed                : REAL;   (* Autonomous ground speed (m/s) *)
    bHeaderOverloadLimit        : BOOL;   (* Header auger/conveyor overload detection switch *)
END_VAR

VAR_OUTPUT
    bSystemReady                : BOOL;   (* System initialized and ready for auto-harvesting *)
    rCmdHeaderLiftValve         : REAL;   (* Proportional command to header lift hydraulics (-100.0 to 100.0 %) *)
    rCmdThreshingDrivePWM       : REAL;   (* PWM command for threshing drum hydrostat drive (0.0 to 100.0 %) *)
    bActiveAlarm                : BOOL;   (* General alarm / fault flag *)
    iFaultCode                  : INT;    (* Diagnostic fault code: 0 = OK, >0 = Error *)
    rCalculatedCropLoad         : REAL;   (* Estimated crop mass flow rate (kg/s) *)
END_VAR

VAR
    iMainState                  : INT := 0; (* Internal state machine *)
    rHeaderHeightError          : REAL;
    rHeaderIntegral             : REAL := 0.0;
    rLastHeaderHeight           : REAL := 0.0;
    rHeaderDerivative           : REAL;
    
    rTargetThreshingRPM         : REAL;
    rRPMError                   : REAL;
    rRPMIntegral                : REAL := 0.0;
    
    (* Filter variables *)
    rFilteredDensity            : REAL := 0.0;
    rFilteredSpeed              : REAL := 0.0;
    
    (* Timers *)
    tOverloadTimer              : TON;
    tStartupDelay               : TON;
    
    (* PID Tuning Constants *)
    Kp_H                        : REAL := 1.2;
    Ki_H                        : REAL := 0.15;
    Kd_H                        : REAL := 0.05;
    Kp_R                        : REAL := 0.8;
    Ki_R                        : REAL := 0.08;
    
    (* Constraints *)
    MAX_LIFT_CMD                : REAL := 100.0;
    MIN_LIFT_CMD                : REAL := -100.0;
    MAX_DRIVE_CMD               : REAL := 100.0;
END_VAR

(* === MAIN LOGIC EXECUTION === *)

(* 1. Safety Interlocks & Emergency Stop *)
IF NOT bEmergencyStop THEN
    bSystemReady          := FALSE;
    rCmdHeaderLiftValve   := 0.0;
    rCmdThreshingDrivePWM := 0.0;
    bActiveAlarm          := TRUE;
    iFaultCode            := 999; (* 999: E-Stop Activated *)
    iMainState            := 0;
    rHeaderIntegral       := 0.0;
    rRPMIntegral          := 0.0;
    RETURN;
END_IF;

(* 2. Overload Detection *)
tOverloadTimer(IN := bHeaderOverloadLimit, PT := T#2S);
IF tOverloadTimer.Q THEN
    bActiveAlarm          := TRUE;
    iFaultCode            := 101; (* 101: Header Overload *)
    iMainState            := 50;  (* Go to fault state *)
END_IF;

(* 3. Signal Filtering (Exponential Moving Average) *)
rFilteredDensity := (0.2 * rCropDensitySensor) + (0.8 * rFilteredDensity);
rFilteredSpeed   := (0.1 * rGroundSpeed) + (0.9 * rFilteredSpeed);

(* Calculate Crop Load Estimation (kg/s) = Density (kg/m^3) * Area/Volume mapping *)
rCalculatedCropLoad := rFilteredDensity * rFilteredSpeed * 9.144; (* Assuming 30ft / 9.144m header width *)

(* 4. State Machine Operations *)
CASE iMainState OF
    0: (* STATE_IDLE *)
        bSystemReady := FALSE;
        rCmdHeaderLiftValve := 0.0;
        rCmdThreshingDrivePWM := 0.0;
        
        IF bEnableSys AND (iFaultCode = 0) THEN
            iMainState := 10;
        END_IF;

    10: (* STATE_INITIALIZING *)
        tStartupDelay(IN := TRUE, PT := T#3S);
        IF tStartupDelay.Q THEN
            tStartupDelay(IN := FALSE);
            bSystemReady := TRUE;
            iMainState := 20;
        END_IF;

    20: (* STATE_AUTO_HARVESTING *)
        IF NOT bEnableSys THEN
            iMainState := 0;
        ELSE
            (* -------------------------------------------------------------
               A. HEADER HEIGHT CONTROL (PID + Feedforward for terrain)
               ------------------------------------------------------------- *)
            rHeaderHeightError := rTargetHeaderHeight - rActualHeaderHeight;
            
            (* Prevent integral windup *)
            IF (rCmdHeaderLiftValve < MAX_LIFT_CMD) AND (rCmdHeaderLiftValve > MIN_LIFT_CMD) THEN
                rHeaderIntegral := rHeaderIntegral + rHeaderHeightError * 0.01; (* Assume 10ms cycle *)
            END_IF;
            
            rHeaderDerivative := (rActualHeaderHeight - rLastHeaderHeight) / 0.01;
            rLastHeaderHeight := rActualHeaderHeight;
            
            rCmdHeaderLiftValve := (Kp_H * rHeaderHeightError) + (Ki_H * rHeaderIntegral) - (Kd_H * rHeaderDerivative);
            
            (* Command Saturation *)
            IF rCmdHeaderLiftValve > MAX_LIFT_CMD THEN rCmdHeaderLiftValve := MAX_LIFT_CMD; END_IF;
            IF rCmdHeaderLiftValve < MIN_LIFT_CMD THEN rCmdHeaderLiftValve := MIN_LIFT_CMD; END_IF;

            (* -------------------------------------------------------------
               B. THRESHING DRUM RPM SYNCHRONIZATION (Load-adaptive)
               ------------------------------------------------------------- *)
            (* Base RPM of 500, scale up dynamically based on predicted crop load.
               Higher density / speed requires higher drum speed to prevent plugging. *)
            rTargetThreshingRPM := 500.0 + (rCalculatedCropLoad * 12.5);
            
            (* Cap max target RPM *)
            IF rTargetThreshingRPM > 1050.0 THEN rTargetThreshingRPM := 1050.0; END_IF;
            
            rRPMError := rTargetThreshingRPM - rActualThreshingRPM;
            
            (* PI Control for Hydrostatic Drive *)
            rRPMIntegral := rRPMIntegral + (rRPMError * 0.01);
            IF rRPMIntegral > 100.0 THEN rRPMIntegral := 100.0; END_IF;
            IF rRPMIntegral < 0.0 THEN rRPMIntegral := 0.0; END_IF;
            
            rCmdThreshingDrivePWM := (Kp_R * rRPMError) + (Ki_R * rRPMIntegral);
            
            (* Output limiting *)
            IF rCmdThreshingDrivePWM > MAX_DRIVE_CMD THEN rCmdThreshingDrivePWM := MAX_DRIVE_CMD; END_IF;
            IF rCmdThreshingDrivePWM < 0.0 THEN rCmdThreshingDrivePWM := 0.0; END_IF;
        END_IF;

    50: (* STATE_FAULT / SAFE_SHUTDOWN *)
        bSystemReady := FALSE;
        rCmdHeaderLiftValve := 100.0; (* Raise header fully in fault *)
        rCmdThreshingDrivePWM := 0.0; (* Shut off threshing drum *)
        
        IF NOT bActiveAlarm AND NOT bEnableSys THEN
            iFaultCode := 0;
            iMainState := 0;
        END_IF;

ELSE
    iMainState := 0;
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
