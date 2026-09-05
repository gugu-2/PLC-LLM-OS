import json
import uuid
import os

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: High-Speed Passenger Rail Active Tilt Bogie Suspension**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Centrifugal acceleration gyroscopic feed-forward logic, pneumatic air-spring dynamic pressure profiling, and derailment limit cross-check redundancy). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_HighSpeedRailTilt\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: High-Speed Passenger Rail Active Tilt Bogie Suspension

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_ActiveTiltBogieControl
VAR_INPUT
    (* Required: at least 4-8 physical inputs with types and comments *)
    bEnable             : BOOL;     (* System master enable signal *)
    bEmergencyStop      : BOOL;     (* Safety relay OK / E-Stop signal *)
    rTrainSpeed         : REAL;     (* Current train velocity in m/s *)
    rLateralAccel       : REAL;     (* Lateral acceleration measured at bogie in m/s^2 *)
    rYawRate            : REAL;     (* Gyroscopic yaw rate in rad/s from inertial measurement unit *)
    rAirSpringPressL    : REAL;     (* Left pneumatic air-spring dynamic pressure (bar) feedback *)
    rAirSpringPressR    : REAL;     (* Right pneumatic air-spring dynamic pressure (bar) feedback *)
END_VAR
VAR_OUTPUT
    (* Required: at least 3-6 outputs with types and comments *)
    bSystemReady        : BOOL;     (* Active tilt system ready/healthy status *)
    rTiltActuatorCmd    : REAL;     (* Tilt actuator control signal (-100.0 to +100.0 %) *)
    rAirSpringSetptL    : REAL;     (* Target left air spring pressure (bar) command *)
    rAirSpringSetptR    : REAL;     (* Target right air spring pressure (bar) command *)
    bDerailmentAlarm    : BOOL;     (* Critical fault / derailment risk alarm output *)
END_VAR
VAR
    (* Internal state variables *)
    iState              : INT := 0; (* Main state machine index *)
    tFaultTimer         : TON;      (* Fault debounce timer to prevent spurious trips *)
    rCurveRadius        : REAL;     (* Calculated track curve radius in meters *)
    rTargetTiltAngle    : REAL;     (* Desired compensation tilt angle in radians *)
    rCentrifugalAccel   : REAL;     (* Calculated uncompensated centrifugal acceleration *)
    rGyroFeedForward    : REAL;     (* Feed-forward predictive component based on yaw rate *)
    bDerailRisk         : BOOL;     (* Internal flag indicating excessive lateral forces *)
END_VAR
VAR CONSTANT
    (* Physical and system limits *)
    MAX_TILT_ANGLE      : REAL := 0.14;   (* Maximum allowed tilt angle ~ 8 degrees *)
    MAX_LAT_ACCEL       : REAL := 1.5;    (* Maximum allowed uncompensated lateral accel m/s^2 *)
    NOMINAL_PRESSURE    : REAL := 5.0;    (* Nominal air spring pressure in bar at rest *)
    GRAVITY             : REAL := 9.81;   (* Gravitational constant in m/s^2 *)
END_VAR

(* === MAIN SAFETY INTERLOCK LOGIC === *)
(* Ensure safety circuits are intact before engaging dynamic suspension *)
IF NOT bEmergencyStop OR NOT bEnable THEN
    bSystemReady := FALSE;
    bDerailmentAlarm := FALSE;
    rTiltActuatorCmd := 0.0;
    rAirSpringSetptL := NOMINAL_PRESSURE;
    rAirSpringSetptR := NOMINAL_PRESSURE;
    iState := 0;
    RETURN;
END_IF;

(* === SENSOR CROSS-CHECKS & DERAILMENT PREVENTION === *)
(* Continuously monitor lateral acceleration against safe passenger comfort and derailment limits *)
bDerailRisk := (ABS(rLateralAccel) > MAX_LAT_ACCEL) OR (rTrainSpeed > 100.0); (* 100 m/s = 360 km/h limit *)
tFaultTimer(IN := bDerailRisk, PT := T#200MS);

IF tFaultTimer.Q THEN
    bDerailmentAlarm := TRUE;
    iState := 99; (* FORCE INTO EMERGENCY FAULT STATE *)
END_IF;

(* === ACTIVE TILT STATE MACHINE === *)
CASE iState OF
    0: (* IDLE / INITIALIZATION *)
        bSystemReady := TRUE;
        rTiltActuatorCmd := 0.0;
        rAirSpringSetptL := NOMINAL_PRESSURE;
        rAirSpringSetptR := NOMINAL_PRESSURE;
        
        (* Transition to active running state when speed exceeds threshold *)
        IF rTrainSpeed > 5.0 THEN
            iState := 10;
        END_IF;

    10: (* NORMAL RUNNING & GYROSCOPIC FEED-FORWARD CALCULATION *)
        (* Calculate kinematic curve parameters based on yaw rate and velocity *)
        IF ABS(rYawRate) > 0.001 AND rTrainSpeed > 5.0 THEN
            rCurveRadius := rTrainSpeed / rYawRate;
            rCentrifugalAccel := (rTrainSpeed * rTrainSpeed) / rCurveRadius;
        ELSE
            rCurveRadius := 99999.0; (* Effectively straight track *)
            rCentrifugalAccel := 0.0;
        END_IF;
        
        (* Compute Gyro Feed-Forward to anticipate curve entry before lateral G's build up *)
        rGyroFeedForward := rYawRate * 2.5; (* 2.5 represents the dynamic system look-ahead gain *)
        
        (* Calculate desired tilt angle to compensate for centrifugal force, maintaining passenger comfort *)
        rTargetTiltAngle := ATAN((rCentrifugalAccel + rGyroFeedForward) / GRAVITY);
        
        (* Saturate target angle against physical constraints of the bogie mechanics *)
        IF rTargetTiltAngle > MAX_TILT_ANGLE THEN
            rTargetTiltAngle := MAX_TILT_ANGLE;
        ELSIF rTargetTiltAngle < -MAX_TILT_ANGLE THEN
            rTargetTiltAngle := -MAX_TILT_ANGLE;
        END_IF;
        
        (* Translate computed tilt angle to proportional actuator command percentage *)
        rTiltActuatorCmd := (rTargetTiltAngle / MAX_TILT_ANGLE) * 100.0;
        
        (* Adjust air-spring dynamic pressure profiling to counteract rolling moment *)
        (* Left/Right pressure differential provides secondary roll stiffness *)
        rAirSpringSetptL := NOMINAL_PRESSURE + (rTargetTiltAngle * 10.0);
        rAirSpringSetptR := NOMINAL_PRESSURE - (rTargetTiltAngle * 10.0);

    99: (* EMERGENCY SAFE STATE *)
        bSystemReady := FALSE;
        rTiltActuatorCmd := 0.0; (* Center the tilt mechanisms *)
        
        (* Stiffen outer springs globally to prevent excessive body roll and roll-over risks *)
        rAirSpringSetptL := NOMINAL_PRESSURE * 1.5;
        rAirSpringSetptR := NOMINAL_PRESSURE * 1.5;
        
        (* Auto-recovery from minor transient faults (typically requires manual reset in real systems) *)
        IF NOT bDerailRisk THEN
            bDerailmentAlarm := FALSE;
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
