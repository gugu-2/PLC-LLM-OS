import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Semiconductor Photolithography Immersion Fluid Handling**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Ultra-pure water (UPW) refractive index thermal stabilization, micro-bubble acoustic cavitation filtering, and meniscus tracking at 800mm/s scan speeds). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_ImmersionLithography\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Semiconductor Photolithography Immersion Fluid Handling

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_ImmersionFluidHandling
VAR_INPUT
    bSystemEnable           : BOOL;     (* System master enable for fluid handling *)
    bEmergencyStop          : BOOL;     (* Safety interlock from master tool control *)
    rUpwTemperature         : REAL;     (* UPW Temp (Deg C) - critical for refractive index *)
    rScanSpeed              : REAL;     (* Current reticle stage scan speed (mm/s), max 800.0 *)
    rDissolvedOxygen        : REAL;     (* Dissolved O2 measurement (ppb) for micro-bubble prevention *)
    bAcousticFilterOk       : BOOL;     (* Status of the acoustic cavitation filtering subsystem *)
    rMeniscusPressure       : REAL;     (* Pressure at the dynamic meniscus confinement zone (kPa) *)
END_VAR
VAR_OUTPUT
    bFluidSystemReady       : BOOL;     (* Fluid system is stable, index of refraction is calibrated *)
    rHeaterControlSignal    : REAL;     (* Precision control signal to UPW pre-heater (%) *)
    rPumpSpeedSetpoint      : REAL;     (* Dispense and recovery pump speed command (RPM) *)
    bMeniscusLossAlarm      : BOOL;     (* Critical alarm: Dynamic meniscus containment failure *)
    iOperatingState         : INT;      (* Current state machine step for tool diagnostics *)
END_VAR
VAR
    iState                  : INT := 0; (* Internal state tracking *)
    rTargetTemperature      : REAL := 22.0000; (* Baseline target temperature for 193nm immersion *)
    rTempError              : REAL := 0.0;
    rIntegral               : REAL := 0.0;
    rDerivative             : REAL := 0.0;
    rLastError              : REAL := 0.0;
    rKp                     : REAL := 15.5;
    rKi                     : REAL := 2.1;
    rKd                     : REAL := 0.8;
    tStabilizationTimer     : TON;
    tAcousticRecoveryTimer  : TON;
    bMeniscusStable         : BOOL := FALSE;
    rMaxPumpSpeed           : REAL := 3000.0;
END_VAR

(* === MAIN SAFETY INTERLOCKS === *)
IF NOT bEmergencyStop THEN
    bFluidSystemReady := FALSE;
    bMeniscusLossAlarm := TRUE;
    rHeaterControlSignal := 0.0;
    rPumpSpeedSetpoint := 0.0;
    iState := 999; (* Fault state *)
    iOperatingState := iState;
    RETURN;
END_IF;

(* === MAIN STATE MACHINE === *)
CASE iState OF
    0: (* IDLE & INITIALIZATION *)
        bFluidSystemReady := FALSE;
        bMeniscusLossAlarm := FALSE;
        rHeaterControlSignal := 0.0;
        rPumpSpeedSetpoint := 0.0;
        
        IF bSystemEnable THEN
            iState := 10;
        END_IF;
        
    10: (* UPW THERMAL CONDITIONING - PID LOOP *)
        (* Target accuracy required: +/- 0.001 deg C to maintain constant index of refraction *)
        rTempError := rTargetTemperature - rUpwTemperature;
        rIntegral := rIntegral + rTempError;
        
        (* Anti-windup limit for integral *)
        IF rIntegral > 100.0 THEN rIntegral := 100.0; END_IF;
        IF rIntegral < -100.0 THEN rIntegral := -100.0; END_IF;
        
        rDerivative := rTempError - rLastError;
        rHeaterControlSignal := (rKp * rTempError) + (rKi * rIntegral) + (rKd * rDerivative);
        rLastError := rTempError;
        
        (* Saturation limits for heater control *)
        IF rHeaterControlSignal > 100.0 THEN
            rHeaterControlSignal := 100.0;
        ELSIF rHeaterControlSignal < 0.0 THEN
            rHeaterControlSignal := 0.0;
        END_IF;
        
        (* Check if temperature is stable *)
        tStabilizationTimer(IN := (ABS(rTempError) < 0.005), PT := T#10S);
        
        IF tStabilizationTimer.Q THEN
            tStabilizationTimer(IN := FALSE);
            iState := 20;
        END_IF;

    20: (* DEGASSING & ACOUSTIC FILTERING *)
        (* Ensure dissolved oxygen is ultra-low to prevent micro-bubble formation during high-speed scanning *)
        IF NOT bAcousticFilterOk OR rDissolvedOxygen > 1.5 THEN
            tAcousticRecoveryTimer(IN := TRUE, PT := T#5S);
            IF tAcousticRecoveryTimer.Q THEN
                iState := 999; (* Abort to fault if recovery fails *)
            END_IF;
        ELSE
            tAcousticRecoveryTimer(IN := FALSE);
            iState := 30;
        END_IF;
        
    30: (* DYNAMIC MENISCUS CONTAINMENT *)
        (* Calculate predictive pump speed based on current scanning velocity (up to 800mm/s) *)
        rPumpSpeedSetpoint := (rScanSpeed / 800.0) * (rMaxPumpSpeed * 0.8) + 500.0; 
        
        (* Verify containment pressure *)
        IF rMeniscusPressure < 15.0 OR rMeniscusPressure > 45.0 THEN
            bMeniscusStable := FALSE;
        ELSE
            bMeniscusStable := TRUE;
        END_IF;
        
        IF bMeniscusStable THEN
            iState := 40;
        ELSE
            bMeniscusLossAlarm := TRUE;
            iState := 999;
        END_IF;

    40: (* SYSTEM READY FOR EXPOSURE *)
        bFluidSystemReady := TRUE;
        bMeniscusLossAlarm := FALSE;
        
        (* Continual PID monitoring and tracking *)
        rTempError := rTargetTemperature - rUpwTemperature;
        rIntegral := rIntegral + rTempError;
        IF rIntegral > 100.0 THEN rIntegral := 100.0; END_IF;
        IF rIntegral < -100.0 THEN rIntegral := -100.0; END_IF;
        rDerivative := rTempError - rLastError;
        rHeaterControlSignal := (rKp * rTempError) + (rKi * rIntegral) + (rKd * rDerivative);
        rLastError := rTempError;
        
        IF rHeaterControlSignal > 100.0 THEN rHeaterControlSignal := 100.0; END_IF;
        IF rHeaterControlSignal < 0.0 THEN rHeaterControlSignal := 0.0; END_IF;
        
        (* Maintain dynamic pump speed *)
        rPumpSpeedSetpoint := (rScanSpeed / 800.0) * (rMaxPumpSpeed * 0.8) + 500.0;
        
        (* Fallback conditions *)
        IF NOT bSystemEnable THEN
            iState := 0;
        ELSIF ABS(rTempError) > 0.01 OR rMeniscusPressure < 15.0 THEN
            iState := 10;
        END_IF;

    999: (* FAULT HANDLING *)
        bFluidSystemReady := FALSE;
        rHeaterControlSignal := 0.0;
        rPumpSpeedSetpoint := 0.0;
        IF bEmergencyStop AND NOT bMeniscusLossAlarm AND bSystemEnable THEN
            (* Reset condition *)
            iState := 0;
        END_IF;
        
END_CASE;

iOperatingState := iState;

END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
print(f"Saved to {filename}")
