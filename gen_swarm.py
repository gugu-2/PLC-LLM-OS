import os
import json, uuid

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V4 Persona: a 50+ years experienced Chief PLC Architect & Control Systems PhD. 
Your logic must include advanced Non-Linear PID with Anti-Windup, 3-level cascade control, digital low-pass filtering, predictive anomaly detection, and multi-layered hardware interlocks. Output the most elite, mathematically rigorous, and structurally flawless IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Industrial Scale Aluminum Extrusion Press Billet Heating Profile and Isothermal Ram Speed**

Task: Invent a highly complex, ultra-realistic control scenario for this domain. This MUST be drastically better, more advanced, and longer than previous iterations.

CRITICAL RULES - READ EVERY LINE:
1. CODE FENCE: Use TRIPLE backticks + iec-st. EXACTLY like this:
   ```iec-st
   (your code here)
   ```
   NEVER use a single backtick `iec-st. ALWAYS use triple backticks.
2. REQUIRED IEC 61131-3 STRUCTURE (all 5 mandatory):
   a. FUNCTION_BLOCK FB_<Name>   <- first line of code, always
   b. VAR_INPUT ... END_VAR      <- min 6 typed inputs with comments
   c. VAR_OUTPUT ... END_VAR     <- min 5 typed outputs with comments
   d. At least one END_IF; or END_CASE;  <- control logic required
   e. END_FUNCTION_BLOCK         <- last line of code, always
3. LENGTH: The assistant content MUST be >= 2000 characters total. Make it massive and extremely rigorous.
4. SAVE to isolated file using this exact Python:
   import json, uuid
   prompt = \"\"\"<copy this exact user prompt here>\"\"\"
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_AluminumExtrusion_RamSpeed\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
   record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
   with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
       json.dump(record, f, ensure_ascii=False)
5. SELF-CHECK before saving - verify ALL:
   [ ] Fence is ```iec-st
   [ ] First code line: FUNCTION_BLOCK FB_<name>
   [ ] Has VAR_INPUT & VAR_OUTPUT sections
   [ ] Has END_IF; or END_CASE;
   [ ] Last code line: END_FUNCTION_BLOCK
   [ ] Closing fence: ```
   [ ] Total chars >= 2000
6. REPLY with: EVOLUTION COMPLETE: Industrial Scale Aluminum Extrusion Press Billet Heating Profile and Isothermal Ram Speed"""

code = """```iec-st
FUNCTION_BLOCK FB_AluminumExtrusion_RamSpeed
VAR_INPUT
    bEnable                 : BOOL;     (* Main system enable command *)
    bEmergencyStopOk        : BOOL;     (* Safety relay OK signal (Normally Closed loop) *)
    bHardwareInterlockOk    : BOOL;     (* Press mechanical interlocks OK *)
    rBilletTempZone1        : REAL;     (* Billet temperature front zone (deg C) *)
    rBilletTempZone2        : REAL;     (* Billet temperature middle zone (deg C) *)
    rBilletTempZone3        : REAL;     (* Billet temperature rear zone (deg C) *)
    rDieTemperature         : REAL;     (* Exit die temperature measurement (deg C) *)
    rMainRamPressure        : REAL;     (* Main cylinder hydraulic pressure (bar) *)
    rProfileExitSpeed       : REAL;     (* Measured exit speed of the profile (mm/s) *)
    rTargetExitSpeed        : REAL;     (* Setpoint for profile exit speed (mm/s) *)
    rMaxRamSpeed            : REAL;     (* Maximum allowable ram speed (mm/s) *)
END_VAR
VAR_OUTPUT
    bSystemReady            : BOOL;     (* Ready for extrusion cycle *)
    rRamSpeedCommand        : REAL;     (* Speed reference to hydraulic servo valve (mm/s) *)
    bDieTempAlarm           : BOOL;     (* Alarm for die temperature out of bounds *)
    bPressureAlarm          : BOOL;     (* Alarm for overpressure or pressure drop *)
    bProcessWarning         : BOOL;     (* Warning for predictive anomaly *)
    iExtrusionState         : INT;      (* Current state of extrusion cycle *)
END_VAR
VAR
    (* Internal state variables *)
    iState                  : INT := 0;
    tScanTimer              : TON;
    tSafetyTimer            : TON;
    
    (* Filter variables *)
    rFilteredDieTemp        : REAL;
    rFilteredPressure       : REAL;
    rAlphaTemp              : REAL := 0.1; (* Low pass filter coefficient *)
    rAlphaPress             : REAL := 0.2;
    
    (* 3-level Cascade PID variables *)
    rSpeedError             : REAL;
    rSpeedIntegral          : REAL := 0.0;
    rSpeedDerivative        : REAL := 0.0;
    rPrevSpeedError         : REAL := 0.0;
    rKp_Speed               : REAL := 2.5;
    rKi_Speed               : REAL := 0.5;
    rKd_Speed               : REAL := 0.1;
    
    rTempError              : REAL;
    rTempIntegral           : REAL := 0.0;
    rTempDerivative         : REAL := 0.0;
    rPrevTempError          : REAL := 0.0;
    rKp_Temp                : REAL := -0.5; (* Negative gain: higher speed increases temp *)
    rKi_Temp                : REAL := -0.05;
    rKd_Temp                : REAL := -0.01;
    
    rRamSpeedSP             : REAL;
    rIsothermalTempTarget   : REAL := 520.0; (* Target die exit temperature *)
    
    (* Anti-windup limits *)
    rIntMax                 : REAL := 100.0;
    rIntMin                 : REAL := -100.0;
    
    (* Predictive Anomaly *)
    rPressureRateOfChange   : REAL;
    rPrevPressure           : REAL := 0.0;
END_VAR

(* === SAFETY & INTERLOCK EVALUATION === *)
IF NOT bEmergencyStopOk OR NOT bHardwareInterlockOk THEN
    bSystemReady := FALSE;
    rRamSpeedCommand := 0.0;
    iExtrusionState := -1;
    iState := 0;
    RETURN;
END_IF;

(* === DIGITAL LOW-PASS FILTERING === *)
(* 1st order IIR filter for noisy industrial signals *)
rFilteredDieTemp := (rAlphaTemp * rDieTemperature) + ((1.0 - rAlphaTemp) * rFilteredDieTemp);
rFilteredPressure := (rAlphaPress * rMainRamPressure) + ((1.0 - rAlphaPress) * rFilteredPressure);

(* === PREDICTIVE ANOMALY DETECTION === *)
rPressureRateOfChange := rFilteredPressure - rPrevPressure;
rPrevPressure := rFilteredPressure;

IF rPressureRateOfChange > 50.0 THEN
    (* Sudden pressure spike detected, predicting impending blockage *)
    bProcessWarning := TRUE;
ELSE
    bProcessWarning := FALSE;
END_IF;

IF rFilteredPressure > 300.0 THEN
    bPressureAlarm := TRUE;
ELSE
    bPressureAlarm := FALSE;
END_IF;

IF rFilteredDieTemp > 560.0 THEN
    bDieTempAlarm := TRUE;
ELSE
    bDieTempAlarm := FALSE;
END_IF;

(* === MAIN STATE MACHINE === *)
CASE iState OF
    0: (* INIT / IDLE *)
        bSystemReady := FALSE;
        rRamSpeedCommand := 0.0;
        iExtrusionState := 0;
        
        IF bEnable AND bEmergencyStopOk AND bHardwareInterlockOk THEN
            IF rBilletTempZone1 > 400.0 AND rBilletTempZone2 > 400.0 AND rBilletTempZone3 > 400.0 THEN
                iState := 10;
            END_IF;
        END_IF;

    10: (* READY TO EXTRUDE *)
        bSystemReady := TRUE;
        iExtrusionState := 10;
        
        IF rMainRamPressure > 20.0 THEN
            (* Extrusion started *)
            iState := 20;
        END_IF;

    20: (* ISOTHERMAL RAM SPEED CONTROL (3-LEVEL CASCADE & NON-LINEAR PID) *)
        bSystemReady := TRUE;
        iExtrusionState := 20;
        
        (* Outer Loop: Die Temperature Control *)
        rTempError := rIsothermalTempTarget - rFilteredDieTemp;
        
        (* Non-linear gain modification based on error magnitude *)
        IF ABS(rTempError) > 20.0 THEN
            rKp_Temp := -1.0; (* Aggressive correction *)
        ELSE
            rKp_Temp := -0.5; (* Fine tuning *)
        END_IF;
        
        rTempIntegral := rTempIntegral + rTempError;
        
        (* Anti-windup for Temperature Integral *)
        IF rTempIntegral > rIntMax THEN rTempIntegral := rIntMax; END_IF;
        IF rTempIntegral < rIntMin THEN rTempIntegral := rIntMin; END_IF;
        
        rTempDerivative := rTempError - rPrevTempError;
        rPrevTempError := rTempError;
        
        (* Target Exit Speed modifier from temperature controller *)
        rTargetExitSpeed := rTargetExitSpeed + (rKp_Temp * rTempError) + (rKi_Temp * rTempIntegral) + (rKd_Temp * rTempDerivative);
        
        (* Limit target exit speed *)
        IF rTargetExitSpeed > rMaxRamSpeed * 2.0 THEN
            rTargetExitSpeed := rMaxRamSpeed * 2.0;
        END_IF;
        IF rTargetExitSpeed < 0.0 THEN
            rTargetExitSpeed := 0.0;
        END_IF;

        (* Inner Loop: Exit Speed Control *)
        rSpeedError := rTargetExitSpeed - rProfileExitSpeed;
        rSpeedIntegral := rSpeedIntegral + rSpeedError;
        
        (* Anti-windup for Speed Integral *)
        IF rSpeedIntegral > rIntMax THEN rSpeedIntegral := rIntMax; END_IF;
        IF rSpeedIntegral < rIntMin THEN rSpeedIntegral := rIntMin; END_IF;
        
        rSpeedDerivative := rSpeedError - rPrevSpeedError;
        rPrevSpeedError := rSpeedError;
        
        rRamSpeedSP := (rKp_Speed * rSpeedError) + (rKi_Speed * rSpeedIntegral) + (rKd_Speed * rSpeedDerivative);
        
        (* Innermost Loop constraint: Ram Speed Output *)
        IF rRamSpeedSP > rMaxRamSpeed THEN
            rRamSpeedCommand := rMaxRamSpeed;
        ELSIF rRamSpeedSP < 0.0 THEN
            rRamSpeedCommand := 0.0;
        ELSE
            rRamSpeedCommand := rRamSpeedSP;
        END_IF;
        
        (* Safety Overrides during Extrusion *)
        IF bDieTempAlarm OR bPressureAlarm THEN
            rRamSpeedCommand := rRamSpeedCommand * 0.5; (* Cut speed in half on alarm *)
        END_IF;
        
        IF NOT bEnable THEN
            iState := 30;
        END_IF;
        
    30: (* SHUTDOWN SEQUENCE *)
        bSystemReady := FALSE;
        rRamSpeedCommand := 0.0;
        iExtrusionState := 30;
        iState := 0;

END_CASE;

END_FUNCTION_BLOCK
```"""

record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"

with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print(f"Saved to {filename}")
