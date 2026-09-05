import json
import uuid
import os

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Utility-Scale Concentrating Photovoltaic (CPV) Dual-Axis Tracker**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., direct normal irradiance (DNI) micro-step algorithm optimization, multi-junction cell active thermal cooling loops, and severe weather flat-stow dynamic braking). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_CPV_DualAxisTracker\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Utility-Scale Concentrating Photovoltaic (CPV) Dual-Axis Tracker

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_CPV_DualAxisTracker
VAR_INPUT
    bEnable                 : BOOL;     (* System global enable command *)
    bEmergencyStop          : BOOL;     (* Safety relay OK / E-Stop loop *)
    rWindSpeed              : REAL;     (* Measured wind speed in m/s for stow calculation *)
    rDNI                    : REAL;     (* Direct Normal Irradiance in W/m^2 from pyrheliometer *)
    rAzimuthTarget          : REAL;     (* Solar ephemeris calculated target azimuth angle (deg) *)
    rElevationTarget        : REAL;     (* Solar ephemeris calculated target elevation angle (deg) *)
    rCurrentAzimuth         : REAL;     (* Measured azimuth angle from high-res encoder (deg) *)
    rCurrentElevation       : REAL;     (* Measured elevation angle from high-res encoder (deg) *)
    rCellTemp               : REAL;     (* Maximum measured multi-junction cell temperature (deg C) *)
END_VAR
VAR_OUTPUT
    bSystemReady            : BOOL;     (* True when ready to track *)
    bTrackingActive         : BOOL;     (* True when actively pursuing DNI target *)
    bStowMode               : BOOL;     (* True when system is in flat stow due to wind or night *)
    rAzimuthVelocityCmd     : REAL;     (* Commanded azimuth rotational velocity (deg/s) *)
    rElevationVelocityCmd   : REAL;     (* Commanded elevation rotational velocity (deg/s) *)
    rCoolingPumpPwm         : REAL;     (* PWM duty cycle 0.0-100.0 for active thermal loop cooling pump *)
    bAlarm                  : BOOL;     (* General fault alarm output *)
END_VAR
VAR
    iState                  : INT := 0; (* Internal state machine sequence *)
    rAzimuthError           : REAL;     (* Calculated azimuth error *)
    rElevationError         : REAL;     (* Calculated elevation error *)
    bHighWind               : BOOL;     (* Wind speed > threshold latch *)
    bThermalOverload        : BOOL;     (* Temp > threshold latch *)
    tStowTimer              : TON;      (* Timer for wind stow hysteresis *)
    tCoolingTimer           : TON;      (* Timer for active cooling run-on *)
    
    (* PI Controller States *)
    rAzimuthIntegral        : REAL := 0.0;
    rElevationIntegral      : REAL := 0.0;
    
    (* Constants *)
    c_rWindStowLimit        : REAL := 15.0; (* m/s threshold for stow mode *)
    c_rTempLimit            : REAL := 85.0; (* deg C threshold for CPV cooling override *)
    c_rKp                   : REAL := 2.5;  (* Proportional gain *)
    c_rKi                   : REAL := 0.1;  (* Integral gain *)
    c_rDeadband             : REAL := 0.05; (* Micro-step deadband in degrees *)
END_VAR

(* === MAIN LOGIC === *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bTrackingActive := FALSE;
    bStowMode := FALSE;
    rAzimuthVelocityCmd := 0.0;
    rElevationVelocityCmd := 0.0;
    rCoolingPumpPwm := 100.0; (* Fail-safe cooling ON *)
    bAlarm := TRUE;
    iState := 0;
    RETURN;
END_IF;

(* Wind monitoring with hysteresis timer *)
IF rWindSpeed >= c_rWindStowLimit THEN
    bHighWind := TRUE;
ELSE
    bHighWind := FALSE;
END_IF;

tStowTimer(IN := bHighWind, PT := T#3S);

(* Active Cooling Thermal Loop Management *)
IF rCellTemp > c_rTempLimit THEN
    bThermalOverload := TRUE;
    rCoolingPumpPwm := 100.0; (* Max cooling capacity *)
ELSIF rCellTemp > (c_rTempLimit - 20.0) THEN
    bThermalOverload := FALSE;
    (* Proportional cooling based on temp delta *)
    rCoolingPumpPwm := 50.0 + ((rCellTemp - (c_rTempLimit - 20.0)) * 2.5);
ELSE
    bThermalOverload := FALSE;
    rCoolingPumpPwm := 20.0; (* Minimum idle circulation *)
END_IF;

(* Main State Machine *)
CASE iState OF
    0: (* IDLE & INIT *)
        bSystemReady := FALSE;
        bTrackingActive := FALSE;
        rAzimuthVelocityCmd := 0.0;
        rElevationVelocityCmd := 0.0;
        rAzimuthIntegral := 0.0;
        rElevationIntegral := 0.0;
        
        IF bEnable AND NOT bAlarm THEN
            iState := 10;
        END_IF;

    10: (* READY TO TRACK OR STOW *)
        bSystemReady := TRUE;
        
        IF tStowTimer.Q THEN
            iState := 99; (* Enter wind stow sequence *)
        ELSIF rDNI > 150.0 AND NOT bThermalOverload THEN
            iState := 20; (* Sufficient irradiance, begin precise tracking *)
        END_IF;

        IF NOT bEnable THEN
            iState := 0;
        END_IF;

    20: (* ACTIVE MICRO-STEP TRACKING *)
        bTrackingActive := TRUE;
        bStowMode := FALSE;
        
        IF tStowTimer.Q THEN
            iState := 99;
        END_IF;
        
        IF rDNI <= 150.0 OR bThermalOverload THEN
            iState := 10; (* Return to ready, pause tracking *)
        END_IF;
        
        (* Calculate angular errors *)
        rAzimuthError := rAzimuthTarget - rCurrentAzimuth;
        rElevationError := rElevationTarget - rCurrentElevation;
        
        (* Micro-step deadband logic for Azimuth *)
        IF ABS(rAzimuthError) > c_rDeadband THEN
            rAzimuthIntegral := rAzimuthIntegral + (rAzimuthError * 0.1); (* Assuming 100ms cycle *)
            rAzimuthVelocityCmd := (rAzimuthError * c_rKp) + (rAzimuthIntegral * c_rKi);
        ELSE
            rAzimuthVelocityCmd := 0.0;
            rAzimuthIntegral := rAzimuthIntegral * 0.9; (* Bleed off integral when on target *)
        END_IF;
        
        (* Micro-step deadband logic for Elevation *)
        IF ABS(rElevationError) > c_rDeadband THEN
            rElevationIntegral := rElevationIntegral + (rElevationError * 0.1);
            rElevationVelocityCmd := (rElevationError * c_rKp) + (rElevationIntegral * c_rKi);
        ELSE
            rElevationVelocityCmd := 0.0;
            rElevationIntegral := rElevationIntegral * 0.9;
        END_IF;
        
        (* Velocity Limiters *)
        IF rAzimuthVelocityCmd > 5.0 THEN rAzimuthVelocityCmd := 5.0; END_IF;
        IF rAzimuthVelocityCmd < -5.0 THEN rAzimuthVelocityCmd := -5.0; END_IF;
        IF rElevationVelocityCmd > 5.0 THEN rElevationVelocityCmd := 5.0; END_IF;
        IF rElevationVelocityCmd < -5.0 THEN rElevationVelocityCmd := -5.0; END_IF;
        
    99: (* WIND STOW & DYNAMIC BRAKING *)
        bTrackingActive := FALSE;
        bStowMode := TRUE;
        
        (* Override target to safe stow position (0 elevation, 0 azimuth relative) *)
        rAzimuthError := 0.0 - rCurrentAzimuth;
        rElevationError := 0.0 - rCurrentElevation;
        
        (* Aggressive return to stow *)
        rAzimuthVelocityCmd := rAzimuthError * (c_rKp * 1.5);
        rElevationVelocityCmd := rElevationError * (c_rKp * 1.5);
        
        IF (ABS(rAzimuthError) < 0.5) AND (ABS(rElevationError) < 0.5) THEN
            (* Locked in stow, apply dynamic braking by holding 0 velocity cmd tightly *)
            rAzimuthVelocityCmd := 0.0;
            rElevationVelocityCmd := 0.0;
        END_IF;
        
        (* Exit stow if wind subsides for prolonged period (using inverted logic and timer in external real-world code) *)
        IF NOT bHighWind THEN
            (* For safety, stow is manual reset or long timer reset, assuming manual/remote reset here *)
            IF NOT bEnable THEN
                iState := 0;
            END_IF;
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
