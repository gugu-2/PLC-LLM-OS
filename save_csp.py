import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Utility-Scale Concentrated Solar Power (CSP) Parabolic Trough Tracking**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., high-precision inclinometer astronomical algorithm tracking, heat transfer fluid (HTF) mass flow rate thermal stabilization at 400°C, and wind stow-mode safety overrides). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_CSP_Tracking\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Utility-Scale Concentrated Solar Power (CSP) Parabolic Trough Tracking

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_CSP_Parabolic_Tracker
VAR_INPUT
    bSystemEnable       : BOOL;     (* Main enable signal for the tracking system *)
    bEmergencyStow      : BOOL;     (* Emergency stow signal from main safety PLC *)
    rInclinometerAngle  : REAL;     (* Current trough angle from high-precision inclinometer [deg] *)
    rWindSpeed          : REAL;     (* Anemometer wind speed reading [m/s] *)
    rTargetElevation    : REAL;     (* Calculated solar elevation angle from astronomical algorithm [deg] *)
    rHtfTemperatureOut  : REAL;     (* Heat Transfer Fluid outlet temperature [deg C] *)
    rDni                : REAL;     (* Direct Normal Irradiance [W/m^2] *)
END_VAR
VAR_OUTPUT
    bMotorDriveRun      : BOOL;     (* Command to variable frequency drive (VFD) for slew drive *)
    bMotorDriveDir      : BOOL;     (* Direction command (0 = East, 1 = West) *)
    rTargetVelocity     : REAL;     (* Velocity setpoint to VFD [deg/min] *)
    bStowPositionReached: BOOL;     (* True if trough is securely in the stow position *)
    bAlarmActive        : BOOL;     (* True if any interlock or fault condition is active *)
    iTrackingState      : INT;      (* Current state of the tracking state machine *)
END_VAR
VAR
    (* Internal State variables *)
    tStowTimer          : TON;
    tHtfOverTempTimer   : TON;
    rAngleError         : REAL;
    rIntegralError      : REAL := 0.0;
    rPreviousError      : REAL := 0.0;
    rDerivativeError    : REAL;
    rPidOutput          : REAL;
    
    (* Constants for PID & Limits *)
    Kp                  : REAL := 2.5;
    Ki                  : REAL := 0.05;
    Kd                  : REAL := 1.2;
    rMaxVelocity        : REAL := 30.0;
    rDeadband           : REAL := 0.05; (* [deg] deadband to avoid hunting *)
    
    (* Safety limits *)
    rMaxWindSpeed       : REAL := 15.0; (* Wind stow threshold 15 m/s *)
    rStowAngle          : REAL := -90.0; (* Face down for stow *)
    rMaxHtfTemp         : REAL := 400.0; (* Max HTF operating temp 400C *)
    bWindAlarm          : BOOL;
    bHtfAlarm           : BOOL;
END_VAR

(* === MAIN LOGIC === *)
(* 1. Safety & Interlock Evaluation *)
bWindAlarm := (rWindSpeed > rMaxWindSpeed);

tHtfOverTempTimer(IN := (rHtfTemperatureOut > rMaxHtfTemp), PT := T#10S);
bHtfAlarm := tHtfOverTempTimer.Q;

IF bEmergencyStow OR bWindAlarm OR bHtfAlarm THEN
    bAlarmActive := TRUE;
    iTrackingState := 99; (* STOW OVERRIDE STATE *)
ELSE
    bAlarmActive := FALSE;
END_IF;

(* 2. Tracking State Machine *)
CASE iTrackingState OF
    0: (* IDLE / INITIALIZATION *)
        bMotorDriveRun := FALSE;
        rTargetVelocity := 0.0;
        bStowPositionReached := FALSE;
        IF bSystemEnable AND NOT bAlarmActive THEN
            IF rDni > 200.0 THEN 
                iTrackingState := 10; (* Start Tracking *)
            ELSE
                iTrackingState := 20; (* Low DNI, standby *)
            END_IF;
        END_IF;

    10: (* ACTIVE ASTRONOMICAL TRACKING *)
        (* PID Control for high-precision positioning *)
        rAngleError := rTargetElevation - rInclinometerAngle;
        
        IF ABS(rAngleError) > rDeadband THEN
            rIntegralError := rIntegralError + rAngleError;
            rDerivativeError := rAngleError - rPreviousError;
            
            rPidOutput := (Kp * rAngleError) + (Ki * rIntegralError) + (Kd * rDerivativeError);
            
            (* Slew limit and velocity assignment *)
            IF rPidOutput > rMaxVelocity THEN
                rPidOutput := rMaxVelocity;
            ELSIF rPidOutput < -rMaxVelocity THEN
                rPidOutput := -rMaxVelocity;
            END_IF;
            
            bMotorDriveRun := TRUE;
            IF rPidOutput >= 0.0 THEN
                bMotorDriveDir := 1; (* West *)
                rTargetVelocity := rPidOutput;
            ELSE
                bMotorDriveDir := 0; (* East *)
                rTargetVelocity := -rPidOutput;
            END_IF;
        ELSE
            bMotorDriveRun := FALSE;
            rTargetVelocity := 0.0;
        END_IF;
        
        rPreviousError := rAngleError;
        
        IF NOT bSystemEnable THEN
            iTrackingState := 0;
        END_IF;
        
    20: (* STANDBY (LOW DNI) *)
        bMotorDriveRun := FALSE;
        rTargetVelocity := 0.0;
        IF rDni > 250.0 AND NOT bAlarmActive THEN
            iTrackingState := 10;
        END_IF;
        IF NOT bSystemEnable THEN
            iTrackingState := 0;
        END_IF;
        
    99: (* EMERGENCY STOW *)
        rAngleError := rStowAngle - rInclinometerAngle;
        IF ABS(rAngleError) > rDeadband THEN
            bMotorDriveRun := TRUE;
            bStowPositionReached := FALSE;
            IF rAngleError > 0.0 THEN
                bMotorDriveDir := 1;
            ELSE
                bMotorDriveDir := 0;
            END_IF;
            rTargetVelocity := rMaxVelocity; (* Move to stow at max speed *)
        ELSE
            bMotorDriveRun := FALSE;
            rTargetVelocity := 0.0;
            bStowPositionReached := TRUE;
        END_IF;
        
        (* Recovery from stow requires explicit enable cycle and cleared alarms *)
        IF NOT bAlarmActive AND NOT bSystemEnable THEN
            iTrackingState := 0;
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

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print(f"Saved to {filename}")
