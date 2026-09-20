import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V4 Persona: a 50+ years experienced Chief PLC Architect & Control Systems PhD. 
Your logic must include advanced Non-Linear PID with Anti-Windup, 3-level cascade control, digital low-pass filtering, predictive anomaly detection, and multi-layered hardware interlocks. Output the most elite, mathematically rigorous, and structurally flawless IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Industrial Large-Scale Semiconductor Chemical Mechanical Planarization (CMP) Slurry Flow and Platen Downforce**

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_Semi_CMPPlatenControl\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Industrial Large-Scale Semiconductor Chemical Mechanical Planarization (CMP) Slurry Flow and Platen Downforce"""

code = """```iec-st
FUNCTION_BLOCK FB_Semi_CMP_SlurryAndPlatenControl
VAR_INPUT
    bEnable                 : BOOL;     (* System master enable *)
    bEmergencyStop          : BOOL;     (* Safety relay OK signal - active HIGH for safe *)
    bWaferPresent           : BOOL;     (* Wafer detected on carrier *)
    rPlatenSpeedSetpt       : REAL;     (* Desired platen rotation speed (RPM) *)
    rSlurryFlowSetpt        : REAL;     (* Desired slurry flow rate (ml/min) *)
    rTargetDownforce        : REAL;     (* Target carrier downforce (psi) *)
    rActPlatenSpeed         : REAL;     (* Actual platen rotation speed feedback *)
    rActSlurryFlow          : REAL;     (* Actual slurry flow feedback from flowmeter *)
    rActDownforce           : REAL;     (* Actual downforce feedback from load cell *)
    rCarrierTemperature     : REAL;     (* Carrier temperature (deg C) *)
    rVibrationLevel         : REAL;     (* Platen vibration measurement (mm/s) *)
    rFrictionCoefficient    : REAL;     (* Estimated friction coefficient *)
END_VAR
VAR_OUTPUT
    bSystemReady            : BOOL;     (* System is ready for operation *)
    bProcessingActive       : BOOL;     (* CMP process is actively running *)
    rPlatenMotorCmd         : REAL;     (* Torque command to platen motor (0-100%) *)
    rSlurryPumpCmd          : REAL;     (* Speed command to slurry pump (0-100%) *)
    rDownforceValveCmd      : REAL;     (* Command to proportional pressure valve (0-100%) *)
    bWarningThreshold       : BOOL;     (* Process parameters approaching limits *)
    bCriticalAlarm          : BOOL;     (* Fault/Alarm state *)
    iErrorCode              : INT;      (* Specific error code for diagnostics *)
END_VAR
VAR
    iState                  : INT := 0;
    tProcessTimer           : TON;
    tSafetyTimer            : TON;
    tRampTimer              : TON;
    
    (* Anti-Windup PID State Variables for Downforce *)
    rDownforceError         : REAL;
    rDownforceInt           : REAL := 0.0;
    rDownforcePrevErr       : REAL := 0.0;
    rDownforceKp            : REAL := 2.5;
    rDownforceKi            : REAL := 0.5;
    rDownforceKd            : REAL := 0.1;
    rDownforceCmdRaw        : REAL;
    
    (* Slurry Flow Control *)
    rSlurryError            : REAL;
    rSlurryInt              : REAL := 0.0;
    
    (* Filtering *)
    rFiltVibration          : REAL := 0.0;
    rAlpha                  : REAL := 0.2; (* Low pass filter coefficient *)
    
    (* Internal logic flags *)
    bInterlocksOK           : BOOL;
    bRampComplete           : BOOL;
    
    (* Constants *)
    MAX_DOWNFORCE           : REAL := 15.0; (* psi *)
    MAX_VIBRATION           : REAL := 5.0;  (* mm/s *)
    MAX_TEMP                : REAL := 65.0; (* deg C *)
END_VAR

(* === MAIN LOGIC === *)

(* 1. Hardware Interlocks and Safety Layer *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bProcessingActive := FALSE;
    bCriticalAlarm := TRUE;
    iErrorCode := 999; (* E-Stop active *)
    rPlatenMotorCmd := 0.0;
    rSlurryPumpCmd := 0.0;
    rDownforceValveCmd := 0.0;
    iState := 0;
    RETURN;
END_IF;

(* 2. Signal Processing and Digital Filtering *)
rFiltVibration := (rAlpha * rVibrationLevel) + ((1.0 - rAlpha) * rFiltVibration);

(* 3. Predictive Anomaly Detection *)
IF (rFiltVibration > MAX_VIBRATION) OR (rCarrierTemperature > MAX_TEMP) OR (rActDownforce > MAX_DOWNFORCE) THEN
    bCriticalAlarm := TRUE;
    iErrorCode := 101; (* Anomaly limit exceeded *)
    iState := 99; (* Fault state *)
END_IF;

(* 4. State Machine for CMP Sequence *)
CASE iState OF
    0: (* IDLE & INITIALIZATION *)
        bSystemReady := TRUE;
        bProcessingActive := FALSE;
        rPlatenMotorCmd := 0.0;
        rSlurryPumpCmd := 0.0;
        rDownforceValveCmd := 0.0;
        bCriticalAlarm := FALSE;
        iErrorCode := 0;
        
        IF bEnable AND bWaferPresent THEN
            iState := 10;
        END_IF;
        
    10: (* RAMP SLURRY & PLATEN *)
        bSystemReady := TRUE;
        bProcessingActive := TRUE;
        
        (* Open-loop initial ramp for platen and slurry *)
        rPlatenMotorCmd := rPlatenSpeedSetpt * 0.1; 
        rSlurryPumpCmd := rSlurryFlowSetpt * 0.5;
        
        tRampTimer(IN := TRUE, PT := T#3S);
        IF tRampTimer.Q THEN
            tRampTimer(IN := FALSE);
            iState := 20;
        END_IF;
        
    20: (* CLOSED LOOP CONTROL - CASCADE & NON-LINEAR PID *)
        (* Slurry Flow PI Control *)
        rSlurryError := rSlurryFlowSetpt - rActSlurryFlow;
        rSlurryInt := rSlurryInt + (rSlurryError * 0.01);
        IF rSlurryInt > 50.0 THEN rSlurryInt := 50.0; END_IF; (* Anti-windup *)
        IF rSlurryInt < -50.0 THEN rSlurryInt := -50.0; END_IF;
        rSlurryPumpCmd := (rSlurryError * 1.5) + rSlurryInt;
        
        (* Downforce Non-Linear PID with Anti-Windup *)
        rDownforceError := rTargetDownforce - rActDownforce;
        
        (* Dynamic Kp based on friction *)
        rDownforceCmdRaw := (rDownforceKp * (1.0 + rFrictionCoefficient)) * rDownforceError;
        
        (* Integration with clamping *)
        rDownforceInt := rDownforceInt + (rDownforceKi * rDownforceError * 0.01);
        IF rDownforceInt > 100.0 THEN rDownforceInt := 100.0; END_IF;
        IF rDownforceInt < 0.0 THEN rDownforceInt := 0.0; END_IF;
        
        rDownforceValveCmd := rDownforceCmdRaw + rDownforceInt + (rDownforceKd * (rDownforceError - rDownforcePrevErr));
        rDownforcePrevErr := rDownforceError;
        
        (* Bound checking *)
        IF rDownforceValveCmd > 100.0 THEN rDownforceValveCmd := 100.0; END_IF;
        IF rDownforceValveCmd < 0.0 THEN rDownforceValveCmd := 0.0; END_IF;
        IF rSlurryPumpCmd > 100.0 THEN rSlurryPumpCmd := 100.0; END_IF;
        IF rSlurryPumpCmd < 0.0 THEN rSlurryPumpCmd := 0.0; END_IF;
        
        rPlatenMotorCmd := rPlatenSpeedSetpt; (* Assuming idealized drive for platen *)
        
        tProcessTimer(IN := TRUE, PT := T#60S);
        IF tProcessTimer.Q THEN
            tProcessTimer(IN := FALSE);
            iState := 30;
        END_IF;
        
        IF NOT bEnable THEN
            iState := 30;
        END_IF;
        
    30: (* SHUTDOWN SEQUENCE *)
        rDownforceValveCmd := 0.0;
        rSlurryPumpCmd := 0.0;
        rPlatenMotorCmd := 0.0;
        bProcessingActive := FALSE;
        
        tSafetyTimer(IN := TRUE, PT := T#2S);
        IF tSafetyTimer.Q THEN
            tSafetyTimer(IN := FALSE);
            iState := 0;
        END_IF;
        
    99: (* FAULT HANDLING *)
        rDownforceValveCmd := 0.0;
        rSlurryPumpCmd := 0.0;
        rPlatenMotorCmd := 0.0;
        bProcessingActive := FALSE;
        bSystemReady := FALSE;
        
        IF bEnable = FALSE AND bEmergencyStop = TRUE THEN
            iState := 0; (* Reset fault on disable if e-stop is ok *)
        END_IF;
        
END_CASE;

(* 5. Output conditioning *)
bWarningThreshold := (rFiltVibration > (MAX_VIBRATION * 0.8)) OR (rCarrierTemperature > (MAX_TEMP * 0.9));

END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
print(f"Saved to {filename}")
