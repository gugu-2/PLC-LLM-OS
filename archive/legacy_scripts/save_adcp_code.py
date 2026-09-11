import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Deep-Sea Acoustic Doppler Current Profiler (ADCP) Calibration Tank**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Micro-turbulence anechoic reflection suppression, high-precision phased array beam forming, and temperature-salinity-depth (TSD) acoustic velocity profile simulation). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_ADCP_CalibrationTank\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Deep-Sea Acoustic Doppler Current Profiler (ADCP) Calibration Tank

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_ADCP_Calibration_Tank
VAR_INPUT
    (* System Master Controls *)
    bEnable                 : BOOL;     (* System master enable signal *)
    bEmergencyStop          : BOOL;     (* Safety relay OK signal (Normally Closed) *)
    
    (* Environmental Sensors *)
    rWaterTemp              : REAL;     (* Measured tank water temperature [deg C] *)
    rSalinity               : REAL;     (* Measured tank water salinity [PSU] *)
    rHydrostaticPressure    : REAL;     (* Measured tank pressure simulating depth [bar] *)
    
    (* Acoustic Telemetry Inputs *)
    rBeamFrequency          : REAL;     (* ADCP transducer transmission frequency [kHz] *)
    rAnechoicReflection     : REAL;     (* Measured acoustic reflection amplitude from walls [dB] *)
    bStartCalibration       : BOOL;     (* Trigger for active acoustic calibration cycle *)
END_VAR
VAR_OUTPUT
    (* System Status Flags *)
    bSystemReady            : BOOL;     (* Environmental conditions stabilized and system ready *)
    bAlarm                  : BOOL;     (* System fault or safety tolerance breached *)
    iErrorCode              : INT;      (* Detailed error code for HMI diagnostics *)
    
    (* Environmental Actuator Commands *)
    rTempControlOut         : REAL;     (* Chiller/Heater analog command [0-100%] *)
    rSalinityControlOut     : REAL;     (* Brine injection pump analog command [0-100%] *)
    rPressureControlOut     : REAL;     (* High-pressure vessel pump command [0-100%] *)
    
    (* Acoustic Control Commands *)
    rBeamPowerTarget        : REAL;     (* Computed optimal Tx power to avoid saturation [Watts] *)
    rCalculatedSoundSpeed   : REAL;     (* Real-time theoretical sound speed profile [m/s] *)
END_VAR
VAR
    (* Internal State Tracking *)
    iState                  : INT := 0; (* Internal state machine sequence step *)
    tStabilizationTimer     : TON;      (* Timer to ensure environmental conditions hold steady *)
    tAcousticPulseTimer     : TON;      (* Pulse interval timing for reflection tests *)
    
    (* Environmental Targets *)
    rTargetTemp             : REAL := 2.5;   (* Deep ocean typical target [deg C] *)
    rTargetSalinity         : REAL := 35.0;  (* Deep ocean typical salinity [PSU] *)
    rTargetPressure         : REAL := 400.0; (* Deep ocean target pressure (approx 4000m) [bar] *)
    
    (* PID Proportional Gains *)
    Kp_Temp                 : REAL := 2.5;
    Kp_Sal                  : REAL := 1.8;
    Kp_Pres                 : REAL := 5.0;
    
    (* Internal Calculation Variables *)
    rTempError              : REAL;
    rSalinityError          : REAL;
    rPressureError          : REAL;
    bEnvStable              : BOOL;
END_VAR

(* === MAIN SAFETY INTERLOCK ROUTINE === *)
(* Extremely strict safety isolation due to high pressure vessel risks *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    rTempControlOut := 0.0;
    rSalinityControlOut := 0.0;
    rPressureControlOut := 0.0;
    rBeamPowerTarget := 0.0;
    bAlarm := TRUE;
    iErrorCode := 999; (* 999 = Critical Safety Emergency Stop Triggered *)
    iState := 0;
    RETURN;
END_IF;

(* === REAL-TIME SPEED OF SOUND SIMULATION (Simplified Mackenzie Equation) === *)
(* Empirical equation mapping Temp, Salinity, and Depth to Acoustic Velocity *)
(* Original: c = 1448.96 + 4.591*T - 0.05304*T^2 + 2.374e-4*T^3 + 1.34*(S - 35) + 0.0163*z + 1.675e-7*z^2 - 0.01025*T*(S - 35) - 7.139e-13*T*z^3 *)
(* Depth [z] is derived approximately from pressure (1 bar approx 10 meters) *)
rCalculatedSoundSpeed := 1449.2 + (4.6 * rWaterTemp) - (0.055 * rWaterTemp * rWaterTemp) 
                         + (1.39 * (rSalinity - 35.0)) + (0.016 * (rHydrostaticPressure * 10.0));

(* === ENVIRONMENTAL ERROR CALCULATION === *)
rTempError := rTargetTemp - rWaterTemp;
rSalinityError := rTargetSalinity - rSalinity;
rPressureError := rTargetPressure - rHydrostaticPressure;

(* === MAIN SEQUENTIAL CONTROL MACHINE === *)
CASE iState OF
    0: (* 0 = IDLE & INITIALIZATION STATE *)
        bSystemReady := FALSE;
        bAlarm := FALSE;
        iErrorCode := 0;
        IF bEnable THEN
            iState := 10;
        END_IF;

    10: (* 10 = ENVIRONMENTAL STABILIZATION (TSD LOOP) *)
        (* Proportional control applying limits for hardware protection *)
        rTempControlOut := LIMIT(0.0, (rTempError * Kp_Temp) + 50.0, 100.0);
        rSalinityControlOut := LIMIT(0.0, rSalinityError * Kp_Sal, 100.0);
        rPressureControlOut := LIMIT(0.0, rPressureError * Kp_Pres, 100.0);

        (* Check against strict tolerance bands for deep-sea simulation *)
        bEnvStable := (ABS(rTempError) < 0.2) AND (ABS(rSalinityError) < 0.5) AND (ABS(rPressureError) < 2.0);

        (* Demand that stable conditions hold for a full 30 seconds *)
        tStabilizationTimer(IN := bEnvStable, PT := T#30S);
        IF tStabilizationTimer.Q THEN
            bSystemReady := TRUE;
            IF bStartCalibration THEN
                tStabilizationTimer(IN := FALSE);
                iState := 20;
            END_IF;
        END_IF;
        
        (* Graceful fallback if disabled *)
        IF NOT bEnable THEN
            iState := 0;
        END_IF;

    20: (* 20 = ANECHOIC REFLECTION AND POWER TUNING *)
        (* Incrementally seek optimal beam power to prevent transducer saturation *)
        tAcousticPulseTimer(IN := TRUE, PT := T#2S);
        
        IF tAcousticPulseTimer.Q THEN
            IF rAnechoicReflection > -40.0 THEN
                (* Wall reflections are too prominent, throttle down beam power *)
                rBeamPowerTarget := rBeamPowerTarget - 0.5;
            ELSIF rAnechoicReflection < -60.0 THEN
                (* Signal-to-noise ratio is weak, cautiously raise beam power *)
                rBeamPowerTarget := rBeamPowerTarget + 0.5;
            END_IF;
            
            (* Safety limits curve: lower max power at higher frequencies to avoid cavitation *)
            rBeamPowerTarget := LIMIT(0.5, rBeamPowerTarget, 1000.0 / rBeamFrequency);
            
            tAcousticPulseTimer(IN := FALSE);
            
            (* If target anechoic decay is achieved, lock parameters and start profiling *)
            IF (rAnechoicReflection <= -40.0) AND (rAnechoicReflection >= -60.0) THEN
                iState := 30; 
            END_IF;
        END_IF;

    30: (* 30 = ACTIVE ACOUSTIC PROFILING & HOLD *)
        (* Lock power parameters, but maintain the TSD environment closed-loop *)
        rTempControlOut := LIMIT(0.0, (rTempError * Kp_Temp) + 50.0, 100.0);
        rSalinityControlOut := LIMIT(0.0, rSalinityError * Kp_Sal, 100.0);
        rPressureControlOut := LIMIT(0.0, rPressureError * Kp_Pres, 100.0);

        IF NOT bStartCalibration THEN
            iState := 10; (* Safe return to stabilization standby *)
        END_IF;
        
        (* Continuous monitoring for sudden breaches or turbulence artifacts *)
        IF ABS(rTempError) > 2.0 OR ABS(rSalinityError) > 2.0 OR ABS(rPressureError) > 5.0 THEN
            bAlarm := TRUE;
            iErrorCode := 101; (* Error 101 = Environmental stability envelope breached during run *)
            iState := 10;
        END_IF;

    ELSE
        (* CATCH-ALL FAULT RECOVERY *)
        iState := 0;
        iErrorCode := 888; (* Error 888 = Invalid State Exception *)
        
END_CASE;

END_FUNCTION_BLOCK
```"""

record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
os.makedirs("data/swarm_raw", exist_ok=True)
filepath = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filepath, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
print(f"Saved to {filepath}")
