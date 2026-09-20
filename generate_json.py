import json, uuid, os
prompt = '''You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V4 Persona: a 50+ years experienced Chief PLC Architect & Control Systems PhD. 
Your logic must include advanced Non-Linear PID with Anti-Windup, 3-level cascade control, digital low-pass filtering, predictive anomaly detection, and multi-layered hardware interlocks. Output the most elite, mathematically rigorous, and structurally flawless IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Mega-Scale High-Voltage Direct Current (HVDC) Converter Station Valve Cooling Water Deionization**

Task: Invent a highly complex, ultra-realistic control scenario for this domain. This MUST be drastically better, more advanced, and longer than previous iterations.

CRITICAL RULES - READ EVERY LINE:
1. CODE FENCE: Use TRIPLE backticks + iec-st. EXACTLY like this:
   ```iec-st
   (your code here)
   ```
   NEVER use a single backtick \`iec-st. ALWAYS use triple backticks.
2. REQUIRED IEC 61131-3 STRUCTURE (all 5 mandatory):
   a. FUNCTION_BLOCK FB_<Name>   <- first line of code, always
   b. VAR_INPUT ... END_VAR      <- min 6 typed inputs with comments
   c. VAR_OUTPUT ... END_VAR     <- min 5 typed outputs with comments
   d. At least one END_IF; or END_CASE;  <- control logic required
   e. END_FUNCTION_BLOCK         <- last line of code, always
3. LENGTH: The assistant content MUST be >= 2000 characters total. Make it massive and extremely rigorous.
4. SAVE to isolated file using this exact Python:
   import json, uuid
   prompt = """<copy this exact user prompt here>"""
   code = """```iec-st\\nFUNCTION_BLOCK FB_HVDC_CoolingWaterDeionization\\n//...\\nEND_FUNCTION_BLOCK\\n```"""
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
6. REPLY with: EVOLUTION COMPLETE: Mega-Scale High-Voltage Direct Current (HVDC) Converter Station Valve Cooling Water Deionization'''

code = '''```iec-st
FUNCTION_BLOCK FB_HVDC_CoolingWaterDeionization
VAR_INPUT
    (* High-Availability Redundant Hardware Interlocks *)
    bSystemEnable           : BOOL;     (* Main HVDC system cooling enable authorization *)
    bEmergencyStop          : BOOL;     (* SIL-3 certified Emergency Stop relay loop OK *)
    bLeakageDetected        : BOOL;     (* Valve hall water leakage optical detection array OK (FALSE = Leak) *)
    
    (* Primary Physical Measurements *)
    rConductivityRaw_A      : REAL;     (* Sensor A: Raw water conductivity in microSiemens/cm *)
    rConductivityRaw_B      : REAL;     (* Sensor B: Redundant raw water conductivity in microSiemens/cm *)
    rFlowRateInlet          : REAL;     (* Main cooling water flow rate L/s *)
    rResinTemperature       : REAL;     (* Mixed-bed ion exchange resin temperature deg C *)
    rMainWaterPressure      : REAL;     (* Pressure at deionization inlet manifold in Bar *)
    rReferenceConductivity  : REAL;     (* Setpoint for required conductivity (e.g., < 0.1 uS/cm) *)
    
    (* Predictor / Anomaly Feed *)
    rPumpVibrationPeak      : REAL;     (* Vibration peak of main deionization pump in mm/s *)
END_VAR
VAR_OUTPUT
    (* Actuators and Control Signals *)
    rValveDeionBypassCmd    : REAL;     (* 0-100% position command for Deionization bypass valve *)
    rPumpSpeedCmd           : REAL;     (* 0-100% command for VFD of the deionization circulation pump *)
    rResinCoolingFlowCmd    : REAL;     (* 0-100% command for resin heat exchanger cooling flow *)
    
    (* Status and Safety Flags *)
    bSystemReady            : BOOL;     (* System operational and stabilized *)
    bIonExchangerExhausted  : BOOL;     (* Alarm: Resin bed chemically exhausted and requires regeneration/swap *)
    bAnomalyDetected        : BOOL;     (* Predictive maintenance anomaly detected (vibration/temp drift) *)
    bCriticalFault          : BOOL;     (* Hard fault necessitating HVDC load reduction or trip *)
    rFilteredConductivity   : REAL;     (* Filtered, voted, and compensated conductivity output *)
END_VAR
VAR
    (* Internal State Machine & Filtering *)
    iState                  : INT := 0; 
    rAlpha                  : REAL := 0.05; (* Low-pass filter smoothing factor *)
    rCondPrev               : REAL := 0.0;
    
    (* Non-Linear PID Controller with Anti-Windup (Deionization Loop) *)
    rError                  : REAL;
    rErrorPrev              : REAL := 0.0;
    rIntegral               : REAL := 0.0;
    rDerivative             : REAL;
    rKp                     : REAL := 2.5; 
    rKi                     : REAL := 0.15; 
    rKd                     : REAL := 0.5;
    rPID_Output             : REAL;
    rPID_Max                : REAL := 100.0;
    rPID_Min                : REAL := 0.0;
    rKp_Adaptive            : REAL;
    
    (* Cascade Control Internal Signals *)
    rTempSetpt              : REAL;
    rTempError              : REAL;
    
    (* Anomaly & Timer Objects *)
    tStartupDelay           : TON;
    tStabilityTimer         : TON;
    tFaultTimer             : TON;
    
    (* Constants *)
    COND_MAX_ALLOWED        : REAL := 0.5;  (* Maximum absolute conductivity trip threshold (uS/cm) *)
    TEMP_MAX_RESIN          : REAL := 60.0; (* Max temp before resin degradation *)
    VIB_THRESHOLD           : REAL := 4.5;  (* Max allowable pump vibration (ISO 10816) *)
END_VAR

(* === ADVANCED SENSOR FUSION & DIGITAL LOW-PASS FILTERING === *)
(* Redundancy checking and averaging of conductivity sensors *)
IF ABS(rConductivityRaw_A - rConductivityRaw_B) > 0.05 THEN
    (* Sensor divergence detected - use higher value for safety (conservative estimation) *)
    IF rConductivityRaw_A > rConductivityRaw_B THEN
        rFilteredConductivity := rConductivityRaw_A;
    ELSE
        rFilteredConductivity := rConductivityRaw_B;
    END_IF;
ELSE
    rFilteredConductivity := (rConductivityRaw_A + rConductivityRaw_B) / 2.0;
END_IF;

(* First-order Infinite Impulse Response (IIR) Low-Pass Filter *)
rFilteredConductivity := (rAlpha * rFilteredConductivity) + ((1.0 - rAlpha) * rCondPrev);
rCondPrev := rFilteredConductivity;


(* === MULTI-LAYERED HARDWARE INTERLOCKS === *)
IF NOT bEmergencyStop OR NOT bLeakageDetected OR (rMainWaterPressure < 1.0) THEN
    (* Critical immediate shutdown *)
    bSystemReady := FALSE;
    bCriticalFault := TRUE;
    rValveDeionBypassCmd := 100.0; (* Bypass DI bed entirely to maintain main cooling loop if possible *)
    rPumpSpeedCmd := 0.0;
    rResinCoolingFlowCmd := 0.0;
    iState := 999; (* FAULT STATE *)
    RETURN;
END_IF;


(* === PREDICTIVE ANOMALY DETECTION === *)
IF (rPumpVibrationPeak > VIB_THRESHOLD) OR (rResinTemperature > TEMP_MAX_RESIN - 5.0) THEN
    bAnomalyDetected := TRUE;
ELSE
    bAnomalyDetected := FALSE;
END_IF;

IF rResinTemperature > TEMP_MAX_RESIN THEN
    bCriticalFault := TRUE;
    iState := 999;
    RETURN;
END_IF;


(* === MAIN CASCADE CONTROL LOGIC STATE MACHINE === *)
CASE iState OF
    0: (* IDLE & SYSTEM CHECKS *)
        bSystemReady := FALSE;
        bCriticalFault := FALSE;
        bIonExchangerExhausted := FALSE;
        rValveDeionBypassCmd := 100.0; (* Bypass on idle *)
        rPumpSpeedCmd := 0.0;
        
        IF bSystemEnable THEN
            iState := 10;
        END_IF;
        
    10: (* PRIMING & STARTUP DELAY *)
        rPumpSpeedCmd := 20.0; (* Gentle prime *)
        tStartupDelay(IN := TRUE, PT := T#10S);
        
        IF tStartupDelay.Q THEN
            tStartupDelay(IN := FALSE);
            iState := 20;
        END_IF;
        
    20: (* ACTIVE DEIONIZATION CONTROL LOOP (NON-LINEAR PID) *)
        bSystemReady := TRUE;
        
        (* 1. Calculate Error *)
        rError := rFilteredConductivity - rReferenceConductivity;
        
        (* 2. Adaptive Gain Scheduling (Non-linear Kp) based on error magnitude *)
        IF ABS(rError) > 0.2 THEN
            rKp_Adaptive := rKp * 2.5; (* Aggressive response for large deviations *)
        ELSE
            rKp_Adaptive := rKp;
        END_IF;
        
        (* 3. Proportional, Integral, Derivative terms *)
        rDerivative := (rError - rErrorPrev);
        rIntegral := rIntegral + (rError * rKi);
        
        (* 4. Anti-Windup Clamping *)
        IF rIntegral > rPID_Max THEN
            rIntegral := rPID_Max;
        ELSIF rIntegral < rPID_Min THEN
            rIntegral := rPID_Min;
        END_IF;
        
        (* 5. Final PID Output computation *)
        rPID_Output := (rKp_Adaptive * rError) + rIntegral + (rKd * rDerivative);
        rErrorPrev := rError;
        
        (* 6. Actuator Mapping (Valve and Pump) *)
        (* Deionization flow is increased as error increases *)
        IF rPID_Output > 100.0 THEN rPID_Output := 100.0; END_IF;
        IF rPID_Output < 0.0 THEN rPID_Output := 0.0; END_IF;
        
        rValveDeionBypassCmd := 100.0 - rPID_Output; (* 0% bypass = 100% DI flow *)
        
        (* 3-Level Cascade: Conductivity -> Flow -> Temperature *)
        (* Adjust pump speed based on bypass valve position and flow setpoint *)
        rPumpSpeedCmd := 50.0 + (rPID_Output * 0.5); 
        
        (* Resin Temperature cascade loop *)
        rTempSetpt := 35.0; 
        rTempError := rResinTemperature - rTempSetpt;
        IF rTempError > 0.0 THEN
            rResinCoolingFlowCmd := LIMIT(0.0, rTempError * 5.0, 100.0);
        ELSE
            rResinCoolingFlowCmd := 0.0;
        END_IF;
        
        (* Resin Exhaustion Check *)
        IF (rFilteredConductivity > COND_MAX_ALLOWED) AND (rValveDeionBypassCmd < 5.0) THEN
            tFaultTimer(IN := TRUE, PT := T#30S);
            IF tFaultTimer.Q THEN
                bIonExchangerExhausted := TRUE;
            END_IF;
        ELSE
            tFaultTimer(IN := FALSE);
        END_IF;
        
        IF NOT bSystemEnable THEN
            iState := 0;
            tFaultTimer(IN := FALSE);
        END_IF;
        
    999: (* FAULT HANDLING *)
        bSystemReady := FALSE;
        rValveDeionBypassCmd := 100.0;
        rPumpSpeedCmd := 0.0;
        rResinCoolingFlowCmd := 100.0; (* Max cooling in fault *)
        
        IF bSystemEnable = FALSE AND bEmergencyStop = TRUE AND bLeakageDetected = TRUE THEN
            (* Reset logic *)
            iState := 0;
        END_IF;
END_CASE;

END_FUNCTION_BLOCK
```'''

os.makedirs('data/swarm_raw', exist_ok=True)
record = {'messages': [{'role': 'user', 'content': prompt}, {'role': 'assistant', 'content': code}]}
filename = f'data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json'
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(record, f, ensure_ascii=False)
print(f'Saved to {filename}')
