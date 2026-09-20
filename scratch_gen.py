import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V4 Persona: a 50+ years experienced Chief PLC Architect & Control Systems PhD. 
Your logic must include advanced Non-Linear PID with Anti-Windup, 3-level cascade control, digital low-pass filtering, predictive anomaly detection, and multi-layered hardware interlocks. Output the most elite, mathematically rigorous, and structurally flawless IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Automated High-Speed Rail (Shinkansen) Pantograph Active Suspension and Catenary Tension**

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_HSRail_Pantograph\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
   record = {\"messages\": [{\"role\": \"user\", \"content\": prompt}, {\"role\": \"assistant\", \"content\": code}]}
   with open(f\"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json\", \"w\", encoding=\"utf-8\") as f:
       json.dump(record, f, ensure_ascii=False)
5. SELF-CHECK before saving - verify ALL:
   [ ] Fence is ```iec-st
   [ ] First code line: FUNCTION_BLOCK FB_<name>
   [ ] Has VAR_INPUT & VAR_OUTPUT sections
   [ ] Has END_IF; or END_CASE;
   [ ] Last code line: END_FUNCTION_BLOCK
   [ ] Closing fence: ```
   [ ] Total chars >= 2000
6. REPLY with: EVOLUTION COMPLETE: Automated High-Speed Rail (Shinkansen) Pantograph Active Suspension and Catenary Tension"""

code = """```iec-st
FUNCTION_BLOCK FB_HSRail_Pantograph
VAR_INPUT
    bEnable                 : BOOL;     (* System master enable *)
    bEmergencyStop          : BOOL;     (* Safety relay OK signal *)
    rTrainSpeed             : REAL;     (* Current train speed in km/h *)
    rCatenaryTension        : REAL;     (* Measured catenary wire tension in kN *)
    rPantographHeight       : REAL;     (* Current pantograph height in mm *)
    rContactForce           : REAL;     (* Measured contact force in N *)
    rWindSpeed              : REAL;     (* Measured crosswind speed in m/s *)
    rAmbientTemp            : REAL;     (* Ambient temperature in deg C *)
END_VAR
VAR_OUTPUT
    bSystemReady            : BOOL;     (* System ready status *)
    rSuspensionActuation    : REAL;     (* Command to active suspension actuator (N) *)
    rTargetForceSetpoint    : REAL;     (* Dynamic contact force setpoint (N) *)
    bWarningCatenaryTension : BOOL;     (* Warning: Catenary tension out of bounds *)
    bAlarmLossOfContact     : BOOL;     (* Fault: Contact loss detected *)
    bAlarmHighForce         : BOOL;     (* Fault: Excessive contact force *)
END_VAR
VAR
    (* Internal State *)
    iState                  : INT := 0;
    
    (* Filtering *)
    rContactForceFilt       : REAL := 0.0;
    rAlpha                  : REAL := 0.15; (* Low-pass filter coefficient *)
    
    (* Advanced Control Variables *)
    rError                  : REAL := 0.0;
    rErrorPrev              : REAL := 0.0;
    rIntegral               : REAL := 0.0;
    rDerivative             : REAL := 0.0;
    
    (* Anti-Windup and Limits *)
    rIntegralMax            : REAL := 500.0;
    rIntegralMin            : REAL := -500.0;
    rActuationMax           : REAL := 1500.0;
    rActuationMin           : REAL := -1500.0;
    
    (* Non-linear PID Gains (Speed dependent) *)
    rKp                     : REAL := 0.0;
    rKi                     : REAL := 0.0;
    rKd                     : REAL := 0.0;
    
    (* Aerodynamic compensation *)
    rAeroLiftComp           : REAL := 0.0;
    
    (* Timers *)
    tLossContactTimer       : TON;
    tHighForceTimer         : TON;
    tStartupDelay           : TON;
END_VAR

(* === MAIN LOGIC === *)
(* 1. Safety Interlocks & Emergency Stop *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    rSuspensionActuation := 0.0;
    iState := 99; (* Fault state *)
    bAlarmLossOfContact := FALSE;
    bAlarmHighForce := FALSE;
    RETURN;
END_IF;

(* 2. Signal Processing - Low Pass Filter for Contact Force *)
rContactForceFilt := rAlpha * rContactForce + (1.0 - rAlpha) * rContactForceFilt;

(* 3. Aerodynamic Lift Compensation based on Train Speed and Wind Speed *)
(* Lift force increases with the square of the speed *)
rAeroLiftComp := 0.005 * (rTrainSpeed * rTrainSpeed) + 0.5 * rWindSpeed;

(* 4. State Machine for Active Suspension Control *)
CASE iState OF
    0: (* IDLE & INITIALIZATION *)
        bSystemReady := FALSE;
        rSuspensionActuation := 0.0;
        rIntegral := 0.0;
        rTargetForceSetpoint := 0.0;
        IF bEnable THEN
            iState := 10;
        END_IF;
        
    10: (* STARTUP DELAY *)
        tStartupDelay(IN := TRUE, PT := T#2S);
        IF tStartupDelay.Q THEN
            tStartupDelay(IN := FALSE);
            iState := 20;
        END_IF;
        
    20: (* RUNNING & ACTIVE CONTROL *)
        bSystemReady := TRUE;
        
        (* Calculate dynamic force setpoint: nominal base force + speed dependent term + temperature compensation *)
        (* EN 50367 standard compliance approximation for high speed *)
        IF rTrainSpeed < 200.0 THEN
            rTargetForceSetpoint := 70.0; (* Base force in N *)
        ELSE
            rTargetForceSetpoint := 70.0 + 0.00097 * (rTrainSpeed * rTrainSpeed);
        END_IF;
        
        (* Temperature compensation for catenary tension *)
        IF rAmbientTemp < 0.0 THEN
            rTargetForceSetpoint := rTargetForceSetpoint + 5.0;
        ELSIF rAmbientTemp > 35.0 THEN
            rTargetForceSetpoint := rTargetForceSetpoint - 5.0;
        END_IF;
        
        (* Catenary Tension Monitoring *)
        IF rCatenaryTension < 15.0 OR rCatenaryTension > 30.0 THEN
            bWarningCatenaryTension := TRUE;
        ELSE
            bWarningCatenaryTension := FALSE;
        END_IF;
        
        (* Non-linear PID Parameter Scheduling *)
        IF rTrainSpeed > 300.0 THEN
            rKp := 2.5; rKi := 0.5; rKd := 0.1;
        ELSIF rTrainSpeed > 200.0 THEN
            rKp := 1.8; rKi := 0.3; rKd := 0.05;
        ELSE
            rKp := 1.2; rKi := 0.2; rKd := 0.02;
        END_IF;
        
        (* Error Calculation *)
        rError := rTargetForceSetpoint - rContactForceFilt;
        
        (* Anti-Windup Integral Calculation *)
        rIntegral := rIntegral + rError * 0.01; (* Assuming 10ms cycle time *)
        IF rIntegral > rIntegralMax THEN
            rIntegral := rIntegralMax;
        ELSIF rIntegral < rIntegralMin THEN
            rIntegral := rIntegralMin;
        END_IF;
        
        (* Derivative Calculation *)
        rDerivative := (rError - rErrorPrev) / 0.01;
        rErrorPrev := rError;
        
        (* Final Actuation Output with Aerodynamic Compensation *)
        rSuspensionActuation := (rKp * rError) + (rKi * rIntegral) + (rKd * rDerivative) - rAeroLiftComp;
        
        (* Actuator Saturation Limit *)
        IF rSuspensionActuation > rActuationMax THEN
            rSuspensionActuation := rActuationMax;
        ELSIF rSuspensionActuation < rActuationMin THEN
            rSuspensionActuation := rActuationMin;
        END_IF;
        
        (* Fault Detection: Loss of Contact *)
        tLossContactTimer(IN := (rContactForceFilt < 5.0), PT := T#50MS);
        IF tLossContactTimer.Q THEN
            bAlarmLossOfContact := TRUE;
        ELSE
            bAlarmLossOfContact := FALSE;
        END_IF;
        
        (* Fault Detection: High Force *)
        tHighForceTimer(IN := (rContactForceFilt > 350.0), PT := T#100MS);
        IF tHighForceTimer.Q THEN
            bAlarmHighForce := TRUE;
        ELSE
            bAlarmHighForce := FALSE;
        END_IF;
        
        (* State transition on disable *)
        IF NOT bEnable THEN
            iState := 0;
        END_IF;
        
    99: (* FAULT STATE *)
        bSystemReady := FALSE;
        rSuspensionActuation := 0.0;
        IF bEmergencyStop AND NOT bEnable THEN
            iState := 0; (* Reset only when safe and disabled *)
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
