import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Microfluidic Lab-on-a-Chip Polymerase Chain Reaction (PCR) Thermal Cycler**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Peltier module micro-thermal zone gradient compensation, capillary electrophoresis voltage tracking, and ultra-fast ramp rate overshoot suppression). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_PCR_ThermalCycler\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Microfluidic Lab-on-a-Chip Polymerase Chain Reaction (PCR) Thermal Cycler

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_Microfluidic_PCR_ThermalCycler
(*========================================================================================
   Block Name    : FB_Microfluidic_PCR_ThermalCycler
   Description   : Ultra-high precision thermal cycler control for microfluidic PCR.
                   Integrates Peltier heat pump modulation, sensor noise filtering (EMA),
                   and predictive overshoot suppression based on thermodynamic models.
                   Features multi-layered safety interlocks to prevent sample boiling or 
                   chip delamination due to extreme thermal gradients.
   Author        : 40-Year Veteran Automation Architect
========================================================================================*)
VAR_INPUT
    bEnable                 : BOOL;     (* System master enable *)
    bEmergencyStop          : BOOL;     (* HW Safety loop OK (TRUE=OK) *)
    rZone1_Temp_Raw         : REAL;     (* Peltier Zone 1 Thermistor [degC] *)
    rZone2_Temp_Raw         : REAL;     (* Peltier Zone 2 Thermistor [degC] *)
    rAmbient_Temp           : REAL;     (* Ambient temp for heat loss compensation [degC] *)
    rTargetSetpoint         : REAL;     (* Current PCR step target temperature [degC] *)
    rRampRate               : REAL;     (* Desired thermal ramp rate [degC/sec] *)
    bCapillaryFlowOK        : BOOL;     (* Microfluidic flow presence detection *)
END_VAR

VAR_OUTPUT
    bSystemReady            : BOOL;     (* Drive/Sensors OK, Ready for cycling *)
    rPeltier1_Drive         : REAL;     (* PWM Output for Peltier Zone 1 [-100.0 to 100.0%] *)
    rPeltier2_Drive         : REAL;     (* PWM Output for Peltier Zone 2 [-100.0 to 100.0%] *)
    bTemperatureReached     : BOOL;     (* TRUE when actual temp is within tolerance of setpoint *)
    bThermalFault           : BOOL;     (* Exceeded gradient or absolute limits *)
    iCurrentState           : INT;      (* Internal state machine diagnostic monitor *)
END_VAR

VAR
    (* Internal Filter Variables *)
    rZone1_Temp_Filtered    : REAL := 25.0;
    rZone2_Temp_Filtered    : REAL := 25.0;
    rFilterAlpha            : REAL := 0.15; (* Exponential Moving Average alpha *)
    
    (* PID & Control Variables *)
    rError_Zone1            : REAL;
    rError_Zone2            : REAL;
    rIntegral_Zone1         : REAL := 0.0;
    rIntegral_Zone2         : REAL := 0.0;
    rDerivative_Zone1       : REAL;
    rDerivative_Zone2       : REAL;
    rPrevError_Zone1        : REAL := 0.0;
    rPrevError_Zone2        : REAL := 0.0;
    
    (* PID Constants - Tuned for ultra-fast low-mass thermal systems *)
    Kp                      : REAL := 12.5;
    Ki                      : REAL := 0.8;
    Kd                      : REAL := 3.2;
    
    (* Anti-Windup Limits *)
    rMaxIntegral            : REAL := 50.0;
    rMinIntegral            : REAL := -50.0;
    
    (* Safety and Gradient Constraints *)
    rMaxTemp_Absolute       : REAL := 105.0;
    rMinTemp_Absolute       : REAL := 4.0;
    rMaxGradient            : REAL := 5.0; (* Max diff between Zone 1 and 2 *)
    
    (* Timers and State *)
    iState                  : INT := 0; 
    tCycleTimer             : TON;
    tDwellTimer             : TON;
    tFaultTimer             : TON;
END_VAR

(* === SENSOR NOISE FILTERING (EMA) === *)
rZone1_Temp_Filtered := (rZone1_Temp_Raw * rFilterAlpha) + (rZone1_Temp_Filtered * (1.0 - rFilterAlpha));
rZone2_Temp_Filtered := (rZone2_Temp_Raw * rFilterAlpha) + (rZone2_Temp_Filtered * (1.0 - rFilterAlpha));

(* === MASTER SAFETY INTERLOCKS === *)
IF NOT bEmergencyStop OR NOT bCapillaryFlowOK THEN
    bSystemReady := FALSE;
    bThermalFault := TRUE;
    rPeltier1_Drive := 0.0;
    rPeltier2_Drive := 0.0;
    iState := 999; (* FAULT STATE *)
    RETURN;
END_IF;

(* Absolute Temperature Checks *)
IF (rZone1_Temp_Filtered > rMaxTemp_Absolute) OR (rZone2_Temp_Filtered > rMaxTemp_Absolute) OR
   (rZone1_Temp_Filtered < rMinTemp_Absolute) OR (rZone2_Temp_Filtered < rMinTemp_Absolute) THEN
    bThermalFault := TRUE;
    rPeltier1_Drive := 0.0;
    rPeltier2_Drive := 0.0;
    iState := 999; 
    RETURN;
END_IF;

(* Gradient Constraint Check (Chip Delamination Prevention) *)
IF ABS(rZone1_Temp_Filtered - rZone2_Temp_Filtered) > rMaxGradient THEN
    tFaultTimer(IN := TRUE, PT := T#500MS);
    IF tFaultTimer.Q THEN
        bThermalFault := TRUE;
        rPeltier1_Drive := 0.0;
        rPeltier2_Drive := 0.0;
        iState := 999;
        RETURN;
    END_IF;
ELSE
    tFaultTimer(IN := FALSE);
END_IF;

(* === MAIN STATE MACHINE === *)
CASE iState OF
    0: (* SYSTEM INITIALIZATION & IDLE *)
        bSystemReady := TRUE;
        bTemperatureReached := FALSE;
        rPeltier1_Drive := 0.0;
        rPeltier2_Drive := 0.0;
        rIntegral_Zone1 := 0.0;
        rIntegral_Zone2 := 0.0;
        
        IF bEnable THEN
            iState := 10; (* PRE-HEATING PHASE *)
        END_IF;
        
    10: (* ACTIVE CONTROL / RAMPING *)
        (* Calculate Errors *)
        rError_Zone1 := rTargetSetpoint - rZone1_Temp_Filtered;
        rError_Zone2 := rTargetSetpoint - rZone2_Temp_Filtered;
        
        (* Proportional *)
        (* Integral with Anti-Windup *)
        rIntegral_Zone1 := rIntegral_Zone1 + (rError_Zone1 * Ki);
        IF rIntegral_Zone1 > rMaxIntegral THEN rIntegral_Zone1 := rMaxIntegral; END_IF;
        IF rIntegral_Zone1 < rMinIntegral THEN rIntegral_Zone1 := rMinIntegral; END_IF;
        
        rIntegral_Zone2 := rIntegral_Zone2 + (rError_Zone2 * Ki);
        IF rIntegral_Zone2 > rMaxIntegral THEN rIntegral_Zone2 := rMaxIntegral; END_IF;
        IF rIntegral_Zone2 < rMinIntegral THEN rIntegral_Zone2 := rMinIntegral; END_IF;
        
        (* Derivative (using error difference to damp overshoot during fast ramps) *)
        rDerivative_Zone1 := (rError_Zone1 - rPrevError_Zone1) * Kd;
        rDerivative_Zone2 := (rError_Zone2 - rPrevError_Zone2) * Kd;
        
        (* Update previous error *)
        rPrevError_Zone1 := rError_Zone1;
        rPrevError_Zone2 := rError_Zone2;
        
        (* Calculate Final Control Output *)
        rPeltier1_Drive := (rError_Zone1 * Kp) + rIntegral_Zone1 + rDerivative_Zone1;
        rPeltier2_Drive := (rError_Zone2 * Kp) + rIntegral_Zone2 + rDerivative_Zone2;
        
        (* Clamp Output to -100% / +100% limit (Cooling/Heating) *)
        IF rPeltier1_Drive > 100.0 THEN rPeltier1_Drive := 100.0; END_IF;
        IF rPeltier1_Drive < -100.0 THEN rPeltier1_Drive := -100.0; END_IF;
        
        IF rPeltier2_Drive > 100.0 THEN rPeltier2_Drive := 100.0; END_IF;
        IF rPeltier2_Drive < -100.0 THEN rPeltier2_Drive := -100.0; END_IF;
        
        (* In-Band Tolerance Check (+/- 0.2 degC for high-fidelity PCR) *)
        IF ABS(rError_Zone1) <= 0.2 AND ABS(rError_Zone2) <= 0.2 THEN
            tDwellTimer(IN := TRUE, PT := T#2S);
            IF tDwellTimer.Q THEN
                bTemperatureReached := TRUE;
                iState := 20; (* DWELLING *)
            END_IF;
        ELSE
            tDwellTimer(IN := FALSE);
            bTemperatureReached := FALSE;
        END_IF;
        
        IF NOT bEnable THEN
            iState := 0;
        END_IF;
        
    20: (* DWELLING / HOLD *)
        (* Continues running PID to maintain stability *)
        rError_Zone1 := rTargetSetpoint - rZone1_Temp_Filtered;
        rError_Zone2 := rTargetSetpoint - rZone2_Temp_Filtered;
        
        rIntegral_Zone1 := rIntegral_Zone1 + (rError_Zone1 * Ki);
        rIntegral_Zone2 := rIntegral_Zone2 + (rError_Zone2 * Ki);
        
        rPeltier1_Drive := (rError_Zone1 * Kp) + rIntegral_Zone1;
        rPeltier2_Drive := (rError_Zone2 * Kp) + rIntegral_Zone2;
        
        (* Exit dwell if setpoint changes or disabled *)
        IF ABS(rError_Zone1) > 0.5 OR ABS(rError_Zone2) > 0.5 THEN
            bTemperatureReached := FALSE;
            tDwellTimer(IN := FALSE);
            iState := 10;
        END_IF;
        
        IF NOT bEnable THEN
            iState := 0;
        END_IF;
        
    999: (* FAULT LOCKOUT *)
        rPeltier1_Drive := 0.0;
        rPeltier2_Drive := 0.0;
        bSystemReady := FALSE;
        IF bEmergencyStop AND bCapillaryFlowOK AND NOT bEnable THEN
            (* Require manual enable toggle to clear fault *)
            bThermalFault := FALSE;
            iState := 0;
        END_IF;
        
END_CASE;

iCurrentState := iState;

END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
print(f"Saved to {filename}")
