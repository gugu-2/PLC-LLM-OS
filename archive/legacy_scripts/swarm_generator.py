import os
import json
import uuid

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Industrial Scale High-Altitude Pseudo-Satellite (HAPS) Solar Telecom Relay**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Stratospheric diurnal thermal cycling battery thermal management, phased array RF beamforming multi-axis tracking gimbal, and aeroelastic flutter active aerodynamic damping). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\nFUNCTION_BLOCK FB_HAPS_TelecomRelay\n//...\nEND_FUNCTION_BLOCK\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Industrial Scale High-Altitude Pseudo-Satellite (HAPS) Solar Telecom Relay

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_HAPS_Core_Control
VAR_INPUT
    (* Required physical inputs *)
    bSystemEnable       : BOOL;     (* Main HAPS system enable *)
    bEmergencySafeMode  : BOOL;     (* Failsafe active low signal, triggers safe state *)
    rBatteryTemp        : REAL;     (* Stratospheric battery pack temp in deg C *)
    rAltitude           : REAL;     (* Current altitude in meters *)
    rWindShearStress    : REAL;     (* Measured aeroelastic stress from wing sensors [N/m2] *)
    rRFBeamAngleTarget  : REAL;     (* Target phased array gimbal angle [deg] *)
    rRFBeamAngleActual  : REAL;     (* Actual phased array gimbal angle [deg] *)
    bSolarPowerOK       : BOOL;     (* Solar irradiance sufficient for operations *)
END_VAR
VAR_OUTPUT
    (* Required outputs *)
    bSystemReady        : BOOL;     (* HAPS systems initialized and operational *)
    rHeaterControlCmd   : REAL;     (* PWM control signal to battery heater [0-100%] *)
    rAeroDampingCmd     : REAL;     (* Deflection command for active aeroelastic flutter damping *)
    rGimbalTorqueCmd    : REAL;     (* Torque command to RF tracking gimbal [Nm] *)
    bCriticalAlarm      : BOOL;     (* System fault, requires ground station intervention *)
    bTelecomRelayActive : BOOL;     (* RF systems actively relaying telemetry/data *)
END_VAR
VAR
    (* Internal State Variables *)
    iMainState          : INT := 0;
    tThermalTimer       : TON;
    tDampingTimer       : TON;
    
    (* Filter and PID states *)
    rFilteredWindStress : REAL := 0.0;
    rGimbalError        : REAL := 0.0;
    rGimbalIntegral     : REAL := 0.0;
    rGimbalDerivative   : REAL := 0.0;
    rGimbalPrevError    : REAL := 0.0;
    
    (* Constants *)
    rKpGimbal           : REAL := 2.5;
    rKiGimbal           : REAL := 0.1;
    rKdGimbal           : REAL := 0.5;
    rMaxGimbalTorque    : REAL := 50.0;
END_VAR

(* === MAIN LOGIC === *)
(* Emergency Handling *)
IF NOT bEmergencySafeMode THEN
    bSystemReady := FALSE;
    bCriticalAlarm := TRUE;
    bTelecomRelayActive := FALSE;
    rHeaterControlCmd := 100.0; (* Ensure batteries do not freeze in safe mode *)
    rAeroDampingCmd := 0.0;     (* Neutral position *)
    rGimbalTorqueCmd := 0.0;
    iMainState := 999;
    RETURN;
END_IF;

(* First order low-pass filter for noisy aeroelastic stress sensors *)
rFilteredWindStress := (rFilteredWindStress * 0.8) + (rWindShearStress * 0.2);

CASE iMainState OF
    0: (* IDLE / WARMUP *)
        bSystemReady := FALSE;
        bTelecomRelayActive := FALSE;
        rGimbalTorqueCmd := 0.0;
        
        (* Battery Thermal Management - Stratospheric extreme cold *)
        IF rBatteryTemp < -20.0 THEN
            rHeaterControlCmd := 100.0;
        ELSIF rBatteryTemp < -5.0 THEN
            rHeaterControlCmd := 50.0;
        ELSE
            rHeaterControlCmd := 0.0;
            IF bSystemEnable AND bSolarPowerOK THEN
                iMainState := 10;
            END_IF;
        END_IF;

    10: (* ACTIVE FLIGHT & AERO DAMPING *)
        bSystemReady := TRUE;
        
        (* Thermal control loop (simplified hysteresis) *)
        IF rBatteryTemp < -10.0 THEN
            rHeaterControlCmd := 80.0;
        ELSIF rBatteryTemp > 5.0 THEN
            rHeaterControlCmd := 0.0;
        END_IF;
        
        (* Aeroelastic flutter active damping *)
        IF rFilteredWindStress > 500.0 THEN
            (* Proportional opposing deflection *)
            rAeroDampingCmd := rFilteredWindStress * 0.05;
            IF rAeroDampingCmd > 45.0 THEN rAeroDampingCmd := 45.0; END_IF; (* saturation limits *)
        ELSE
            rAeroDampingCmd := 0.0;
        END_IF;
        
        (* Transition to telecom operation if altitude is stratospheric *)
        IF rAltitude > 18000.0 THEN
            iMainState := 20;
        END_IF;

    20: (* TELECOM RELAY & GIMBAL TRACKING *)
        bSystemReady := TRUE;
        bTelecomRelayActive := TRUE;
        
        (* Gimbal PID Control Loop *)
        rGimbalError := rRFBeamAngleTarget - rRFBeamAngleActual;
        rGimbalIntegral := rGimbalIntegral + rGimbalError;
        (* Anti-windup limit *)
        IF rGimbalIntegral > 100.0 THEN rGimbalIntegral := 100.0; END_IF;
        IF rGimbalIntegral < -100.0 THEN rGimbalIntegral := -100.0; END_IF;
        
        rGimbalDerivative := rGimbalError - rGimbalPrevError;
        
        rGimbalTorqueCmd := (rKpGimbal * rGimbalError) + (rKiGimbal * rGimbalIntegral) + (rKdGimbal * rGimbalDerivative);
        
        (* Output saturation *)
        IF rGimbalTorqueCmd > rMaxGimbalTorque THEN
            rGimbalTorqueCmd := rMaxGimbalTorque;
        ELSIF rGimbalTorqueCmd < -rMaxGimbalTorque THEN
            rGimbalTorqueCmd := -rMaxGimbalTorque;
        END_IF;
        
        rGimbalPrevError := rGimbalError;
        
        (* Dropping altitude below operational ceiling returns to active flight mode *)
        IF rAltitude < 17500.0 THEN
            iMainState := 10;
        END_IF;
        
        IF NOT bSystemEnable THEN
            iMainState := 0;
        END_IF;
        
    999: (* FAULT / SAFE MODE RECOVERY *)
        IF bEmergencySafeMode AND bSystemEnable THEN
            bCriticalAlarm := FALSE;
            iMainState := 0;
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
