import json, uuid, os

prompt = """<USER_REQUEST>
You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Deep-Space Optical Communications (DSOC) Ground Station Telescope Gimbal**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Sub-microradian pointing accuracy using active star-tracking feed-forward, wind-buffeting disturbance rejection, and cryogenic detector thermal control). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_DSOC_TelescopeGimbal\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Deep-Space Optical Communications (DSOC) Ground Station Telescope Gimbal

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT.
</USER_REQUEST>"""

code = """```iec-st
FUNCTION_BLOCK FB_DSOC_TelescopeGimbal
VAR_INPUT
    (* Deep-Space Optical Communications (DSOC) Ground Station Telescope Gimbal - Inputs *)
    bSystemEnable       : BOOL;     (* System master enable interlock *)
    bEmergencyStop      : BOOL;     (* Hardware E-Stop safety relay (Fail-Safe active LOW) *)
    rAzimuthCmd         : LREAL;    (* Commanded Azimuth in microradians *)
    rElevationCmd       : LREAL;    (* Commanded Elevation in microradians *)
    rAzimuthFeedback    : LREAL;    (* High-resolution absolute encoder Azimuth feedback (urad) *)
    rElevationFeedback  : LREAL;    (* High-resolution absolute encoder Elevation feedback (urad) *)
    rWindSpeed          : REAL;     (* Anemometer wind speed feedback (m/s) for disturbance rejection *)
    rCryoTemp           : REAL;     (* Superconducting nanowire single-photon detector (SNSPD) temp (K) *)
    bStarTrackerValid   : BOOL;     (* Active star-tracking feed-forward validity flag *)
    rStarTrackerAzOffset: LREAL;    (* Fast-steering mirror azimuth feed-forward offset (urad) *)
    rStarTrackerElOffset: LREAL;    (* Fast-steering mirror elevation feed-forward offset (urad) *)
END_VAR

VAR_OUTPUT
    (* DSOC Gimbal - Outputs *)
    bSystemReady        : BOOL;     (* Gimbal initialized, calibrated, and ready for pointing *)
    bTrackingActive     : BOOL;     (* True when pointing error is within sub-microradian threshold *)
    rAzimuthDriveOut    : LREAL;    (* Torque command for Azimuth direct-drive motor (Nm) *)
    rElevationDriveOut  : LREAL;    (* Torque command for Elevation direct-drive motor (Nm) *)
    rCryoCoolerCmd      : REAL;     (* Command signal for the closed-cycle cryocooler (0-100%) *)
    bFaultActive        : BOOL;     (* Aggregated fault indicator *)
    iFaultCode          : INT;      (* Diagnostic fault code for telemetry *)
END_VAR

VAR
    (* Internal State and Controller Variables *)
    iState              : INT := 0; (* Main State Machine Step *)
    
    (* Azimuth PID Controller State *)
    rAzError            : LREAL;
    rAzErrorPrev        : LREAL;
    rAzIntegral         : LREAL;
    rAzDerivative       : LREAL;
    
    (* Elevation PID Controller State *)
    rElError            : LREAL;
    rElErrorPrev        : LREAL;
    rElIntegral         : LREAL;
    rElDerivative       : LREAL;
    
    (* Controller Tuning Constants (Sub-microradian precision) *)
    rKp                 : LREAL := 15.75;
    rKi                 : LREAL := 2.45;
    rKd                 : LREAL := 0.85;
    
    (* Filters and Timers *)
    rWindBuffetFilter   : REAL;     (* Low-pass filtered wind disturbance estimator *)
    rCryoTempFiltered   : REAL;     (* Moving average of cryostat temperature *)
    tStartupDelay       : TON;      (* Initialization stabilization timer *)
    tCryoWarmAlarm      : TON;      (* Timeout for cryocooler failing to maintain superconducting temp *)
    
    (* Internal safety/limits *)
    MAX_DRIVE_TORQUE    : LREAL := 5000.0; (* Nm limit for motors *)
    MAX_TRACKING_ERROR  : LREAL := 0.5;    (* urad limit to consider "Tracking Active" *)
    CRYO_OPERATING_TEMP : REAL := 4.2;     (* Kelvin (Liquid Helium temp) *)
END_VAR

(* === MAIN LOGIC === *)

(* 1. Multi-layered Safety Interlocks & E-Stop *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bTrackingActive := FALSE;
    rAzimuthDriveOut := 0.0;
    rElevationDriveOut := 0.0;
    bFaultActive := TRUE;
    iFaultCode := 999; (* EMERGENCY STOP *)
    iState := 0;
    RETURN;
END_IF;

(* 2. Sensor Noise Filtering (Cryostat & Wind) *)
(* Simple EMA (Exponential Moving Average) filter for thermal noise rejection *)
rCryoTempFiltered := rCryoTempFiltered * 0.95 + rCryoTemp * 0.05;
(* Wind buffeting estimation filter for feed-forward disturbance rejection *)
rWindBuffetFilter := rWindBuffetFilter * 0.90 + rWindSpeed * 0.10;

(* 3. Cryogenic Thermal Control (Deadband Bang-Bang with Proportional assist) *)
IF rCryoTempFiltered > CRYO_OPERATING_TEMP + 0.1 THEN
    rCryoCoolerCmd := 100.0; (* Max cooling if warming *)
ELSIF rCryoTempFiltered < CRYO_OPERATING_TEMP - 0.1 THEN
    rCryoCoolerCmd := 20.0;  (* Minimum idle cooling to prevent thermal shock *)
ELSE
    (* Proportional maintenance cooling *)
    rCryoCoolerCmd := 50.0 + (rCryoTempFiltered - CRYO_OPERATING_TEMP) * 100.0;
END_IF;

(* Thermal Fault Detection *)
tCryoWarmAlarm(IN := (rCryoTempFiltered > 5.0), PT := T#10S);
IF tCryoWarmAlarm.Q THEN
    bFaultActive := TRUE;
    iFaultCode := 101; (* CRYOSTAT OVERTEMP FAULT *)
    iState := 99; (* Transition to safe shutdown *)
END_IF;

(* 4. Main Gimbal State Machine *)
CASE iState OF
    0: (* IDLE & SYSTEM CHECKS *)
        bSystemReady := FALSE;
        bTrackingActive := FALSE;
        rAzimuthDriveOut := 0.0;
        rElevationDriveOut := 0.0;
        
        IF bSystemEnable AND NOT bFaultActive THEN
            iState := 10;
        END_IF;
        
    10: (* INITIALIZING & CALIBRATING *)
        tStartupDelay(IN := TRUE, PT := T#5S);
        IF tStartupDelay.Q THEN
            tStartupDelay(IN := FALSE);
            bSystemReady := TRUE;
            iState := 20;
        END_IF;
        
    20: (* CLOSED-LOOP OPTICAL TRACKING *)
        IF NOT bSystemEnable THEN
            iState := 0;
        END_IF;
        
        (* Calculate pointing errors *)
        rAzError := rAzimuthCmd - rAzimuthFeedback;
        rElError := rElevationCmd - rElevationFeedback;
        
        (* Active Star-Tracker Feed-Forward (if valid) *)
        IF bStarTrackerValid THEN
            rAzError := rAzError + rStarTrackerAzOffset;
            rElError := rElError + rStarTrackerElOffset;
        END_IF;
        
        (* Wind Disturbance Rejection (Feed-forward torque compensation based on wind model) *)
        (* Simplified aerodynamic drag coefficient model *)
        VAR
            rWindCompTorque : LREAL;
        END_VAR
        rWindCompTorque := rWindBuffetFilter * rWindBuffetFilter * 0.025; 
        
        (* Azimuth PID Computation *)
        rAzIntegral := rAzIntegral + (rAzError * 0.01); (* Assuming 10ms task cycle *)
        rAzDerivative := (rAzError - rAzErrorPrev) / 0.01;
        rAzimuthDriveOut := (rKp * rAzError) + (rKi * rAzIntegral) + (rKd * rAzDerivative) + rWindCompTorque;
        rAzErrorPrev := rAzError;
        
        (* Elevation PID Computation *)
        rElIntegral := rElIntegral + (rElError * 0.01);
        rElDerivative := (rElError - rElErrorPrev) / 0.01;
        rElevationDriveOut := (rKp * rElError) + (rKi * rElIntegral) + (rKd * rElDerivative);
        rElErrorPrev := rElError;
        
        (* Torque Limiting (Anti-windup & Actuator protection) *)
        IF rAzimuthDriveOut > MAX_DRIVE_TORQUE THEN rAzimuthDriveOut := MAX_DRIVE_TORQUE; rAzIntegral := rAzIntegral - (rAzError * 0.01); END_IF;
        IF rAzimuthDriveOut < -MAX_DRIVE_TORQUE THEN rAzimuthDriveOut := -MAX_DRIVE_TORQUE; rAzIntegral := rAzIntegral - (rAzError * 0.01); END_IF;
        IF rElevationDriveOut > MAX_DRIVE_TORQUE THEN rElevationDriveOut := MAX_DRIVE_TORQUE; rElIntegral := rElIntegral - (rElError * 0.01); END_IF;
        IF rElevationDriveOut < -MAX_DRIVE_TORQUE THEN rElevationDriveOut := -MAX_DRIVE_TORQUE; rElIntegral := rElIntegral - (rElError * 0.01); END_IF;
        
        (* Tracking Status Evaluation *)
        IF (ABS(rAzError) < MAX_TRACKING_ERROR) AND (ABS(rElError) < MAX_TRACKING_ERROR) THEN
            bTrackingActive := TRUE;
        ELSE
            bTrackingActive := FALSE;
        END_IF;

    99: (* FAULT SHUTDOWN SEQUENCE *)
        bSystemReady := FALSE;
        bTrackingActive := FALSE;
        rAzimuthDriveOut := 0.0;
        rElevationDriveOut := 0.0;
        (* Require manual reset of fault logic to recover *)
        IF NOT bFaultActive THEN
            iState := 0;
        END_IF;
        
END_CASE;

END_FUNCTION_BLOCK
```"""

os.makedirs('data/swarm_raw', exist_ok=True)
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print(f"Saved to {filename}")
