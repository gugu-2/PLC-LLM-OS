import json, uuid, os

prompt = '''<USER_REQUEST>
You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Offshore Floating Wind Turbine Active Ballast Compensation**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., 6-DOF wave motion predictive damping, rapid ballast water transfer, and emergency storm gyroscopic stabilization). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   prompt = """<copy this exact user prompt here>"""
   code = """```iec-st\nFUNCTION_BLOCK FB_FloatingWind_Ballast\n//...\nEND_FUNCTION_BLOCK\n```"""
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
6. REPLY with: EVOLUTION COMPLETE: Offshore Floating Wind Turbine Active Ballast Compensation

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT.
</USER_REQUEST>'''

code = '''```iec-st
FUNCTION_BLOCK FB_FloatingWind_Ballast
VAR_INPUT
    (* Required: at least 4-8 physical inputs with types and comments *)
    bEnable               : BOOL;     (* System master enable signal *)
    bEmergencyStop        : BOOL;     (* Safety relay OK signal (Active HIGH) *)
    rPitchAngle           : REAL;     (* Physical measurement: Pitch angle from 6-DOF IMU [deg] *)
    rRollAngle            : REAL;     (* Physical measurement: Roll angle from 6-DOF IMU [deg] *)
    rWaveHeaveSpeed       : REAL;     (* Vertical heave velocity from wave radar [m/s] *)
    rWindSpeed            : REAL;     (* Anemometer wind speed [m/s] *)
    rBallastLevelPort     : REAL;     (* Port side ballast tank level [%] *)
    rBallastLevelStbd     : REAL;     (* Starboard side ballast tank level [%] *)
END_VAR
VAR_OUTPUT
    (* Required: at least 3-6 outputs with types and comments *)
    bSystemReady          : BOOL;     (* System initialized and ready for control *)
    rPumpCmdPort          : REAL;     (* Control signal to Port actuator pump [-100..100%] *)
    rPumpCmdStbd          : REAL;     (* Control signal to Starboard actuator pump [-100..100%] *)
    bStormModeActive      : BOOL;     (* Emergency storm gyroscopic stabilization mode active indicator *)
    bAlarm                : BOOL;     (* Fault alarm output (Critical faults) *)
    bMaintenanceWarning   : BOOL;     (* Non-critical maintenance warning *)
END_VAR
VAR
    (* Internal state variables *)
    iState                : INT := 0;
    tTimer                : TON;
    tEStopDebounce        : TON;
    
    (* Filter and Derivative State *)
    rFilteredPitch        : REAL := 0.0;
    rFilteredRoll         : REAL := 0.0;
    rLastPitch            : REAL := 0.0;
    rLastRoll             : REAL := 0.0;
    rPitchDerivative      : REAL := 0.0;
    rRollDerivative       : REAL := 0.0;
    
    (* Controller Parameters *)
    rAlpha                : REAL := 0.15;   (* Low-pass filter coefficient for IMU noise *)
    rDt                   : REAL := 0.05;   (* Control loop cycle time [s] *)
    rKp                   : REAL := 12.5;   (* Proportional gain for attitude correction *)
    rKd                   : REAL := 4.2;    (* Derivative gain for predictive wave damping *)
    
    (* Storm Thresholds *)
    rWindStormThreshold   : REAL := 28.0;   (* Wind speed triggering storm mode [m/s] *)
    rHeaveStormThreshold  : REAL := 4.5;    (* Heave velocity triggering storm mode [m/s] *)
END_VAR

(* === MAIN LOGIC === *)

(* Multi-layered Safety Interlocks *)
tEStopDebounce(IN := NOT bEmergencyStop, PT := T#250MS);
IF tEStopDebounce.Q THEN
    bSystemReady := FALSE;
    bAlarm := TRUE;
    rPumpCmdPort := 0.0;
    rPumpCmdStbd := 0.0;
    bStormModeActive := FALSE;
    iState := 999; (* Enter Critical Error State Latch *)
    RETURN;
END_IF;

(* Sensor Noise Filtering using Exponential Weighted Moving Average (EWMA) *)
rFilteredPitch := rFilteredPitch + rAlpha * (rPitchAngle - rFilteredPitch);
rFilteredRoll  := rFilteredRoll  + rAlpha * (rRollAngle - rFilteredRoll);

(* Derivative calculation for 6-DOF wave motion predictive damping *)
rPitchDerivative := (rFilteredPitch - rLastPitch) / rDt;
rRollDerivative  := (rFilteredRoll - rLastRoll) / rDt;
rLastPitch := rFilteredPitch;
rLastRoll := rFilteredRoll;

CASE iState OF
    0: (* IDLE & SYSTEM WARMUP *)
        bSystemReady := FALSE;
        rPumpCmdPort := 0.0;
        rPumpCmdStbd := 0.0;
        bStormModeActive := FALSE;
        
        IF bEnable AND NOT bAlarm THEN
            (* Initiate warmup timer for hydraulic accumulators *)
            tTimer(IN := TRUE, PT := T#10S);
            IF tTimer.Q THEN
                tTimer(IN := FALSE);
                iState := 10;
            END_IF;
        ELSE
            tTimer(IN := FALSE);
        END_IF;

    10: (* RUNNING: ACTIVE BALLAST COMPENSATION *)
        bSystemReady := TRUE;
        
        (* Evaluate Emergency Storm Gyroscopic Stabilization criteria *)
        IF rWindSpeed >= rWindStormThreshold OR ABS(rWaveHeaveSpeed) >= rHeaveStormThreshold THEN
            bStormModeActive := TRUE;
            iState := 20; (* Transition to Storm Mode *)
        ELSE
            bStormModeActive := FALSE;
            
            (* Advanced PD Control for Roll/Pitch compensation via rapid ballast water transfer *)
            (* Port pump corrects negative roll, Starboard corrects positive roll *)
            rPumpCmdPort := (rFilteredRoll * rKp) + (rRollDerivative * rKd);
            rPumpCmdStbd := -(rFilteredRoll * rKp) - (rRollDerivative * rKd);
            
            (* Command Saturation Limits *)
            IF rPumpCmdPort > 100.0 THEN rPumpCmdPort := 100.0; END_IF;
            IF rPumpCmdPort < -100.0 THEN rPumpCmdPort := -100.0; END_IF;
            IF rPumpCmdStbd > 100.0 THEN rPumpCmdStbd := 100.0; END_IF;
            IF rPumpCmdStbd < -100.0 THEN rPumpCmdStbd := -100.0; END_IF;
            
            (* Anti-Cavitation and Overflow Protection Interlocks *)
            IF (rBallastLevelPort > 98.0 AND rPumpCmdPort > 0.0) OR (rBallastLevelPort < 2.0 AND rPumpCmdPort < 0.0) THEN
                rPumpCmdPort := 0.0;
                bMaintenanceWarning := TRUE;
            END_IF;
            IF (rBallastLevelStbd > 98.0 AND rPumpCmdStbd > 0.0) OR (rBallastLevelStbd < 2.0 AND rPumpCmdStbd < 0.0) THEN
                rPumpCmdStbd := 0.0;
                bMaintenanceWarning := TRUE;
            END_IF;
        END_IF;
        
        (* Monitor master enable *)
        IF NOT bEnable THEN
            iState := 0;
        END_IF;

    20: (* EMERGENCY STORM MODE *)
        (* Maximize ballast water at the lowest structural level to lower center of gravity *)
        rPumpCmdPort := 100.0; 
        rPumpCmdStbd := 100.0;
        
        IF rBallastLevelPort >= 100.0 THEN rPumpCmdPort := 0.0; END_IF;
        IF rBallastLevelStbd >= 100.0 THEN rPumpCmdStbd := 0.0; END_IF;
        
        (* Hysteresis for exiting storm mode *)
        IF rWindSpeed < (rWindStormThreshold - 5.0) AND ABS(rWaveHeaveSpeed) < (rHeaveStormThreshold - 1.5) THEN
            bStormModeActive := FALSE;
            iState := 10; (* Return to standard active compensation *)
        END_IF;
        
        IF NOT bEnable THEN
            iState := 0;
        END_IF;

    999: (* CRITICAL FAULT LATCH *)
        (* Requires physical inspection, valid safety relay, and system reset via master enable cycle *)
        IF bEmergencyStop AND NOT bEnable THEN
            bAlarm := FALSE;
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
