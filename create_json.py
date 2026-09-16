import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Offshore Floating Wind Turbine (FOWT) Active Ballast Control**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., 6-DOF IMU wave motion compensation, rapid seawater transfer pump coordination, and mooring line tension limiting). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_FOWT_ActiveBallast\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Offshore Floating Wind Turbine (FOWT) Active Ballast Control

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT.
"""

code = """```iec-st
FUNCTION_BLOCK FB_FOWT_ActiveBallast
VAR_INPUT
    (* Essential Safety and System Enable *)
    bSystemEnable       : BOOL;     (* Main system enable from SCADA *)
    bEmergencyStop      : BOOL;     (* Hardware E-Stop OK signal (TRUE = OK) *)
    
    (* 6-DOF IMU Sensor Data for Motion Compensation *)
    rPitchAngle         : REAL;     (* Platform pitch angle in degrees *)
    rRollAngle          : REAL;     (* Platform roll angle in degrees *)
    rHeaveAccel         : REAL;     (* Heave acceleration in m/s^2 *)
    
    (* Mooring Line Tension Monitoring *)
    rTensionLine1       : REAL;     (* Mooring line 1 tension in kN *)
    rTensionLine2       : REAL;     (* Mooring line 2 tension in kN *)
    rTensionLine3       : REAL;     (* Mooring line 3 tension in kN *)
    
    (* Ballast Tank Levels *)
    rTankLevelFwd       : REAL;     (* Forward ballast tank level % *)
    rTankLevelAft       : REAL;     (* Aft ballast tank level % *)
    rTankLevelPort      : REAL;     (* Port ballast tank level % *)
    rTankLevelStbd      : REAL;     (* Starboard ballast tank level % *)
END_VAR
VAR_OUTPUT
    (* System Status *)
    bSystemReady        : BOOL;     (* System is initialized and ready *)
    bAlarmActive        : BOOL;     (* Global alarm flag *)
    
    (* Pump and Valve Control Commands *)
    rPumpCmdFwdAft      : REAL;     (* Command to Fwd-Aft transfer pump (-100% to 100%) *)
    rPumpCmdPortStbd    : REAL;     (* Command to Port-Stbd transfer pump (-100% to 100%) *)
    bValveSeaWaterIn    : BOOL;     (* Seawater intake valve open command *)
    bValveSeaWaterOut   : BOOL;     (* Seawater discharge valve open command *)
    
    (* Filtered States for SCADA *)
    rFilteredPitch      : REAL;     (* Kalman-filtered pitch estimate *)
    rFilteredRoll       : REAL;     (* Kalman-filtered roll estimate *)
END_VAR
VAR
    (* Internal State Machine *)
    iState              : INT := 0; 
    
    (* Filters and Timers *)
    rPrevPitch          : REAL := 0.0;
    rPrevRoll           : REAL := 0.0;
    tInitDelay          : TON;
    tSafetyDelay        : TON;
    
    (* Control Gains *)
    rKpPitch            : REAL := 2.5;
    rKpRoll             : REAL := 2.5;
    rMaxTensionLimit    : REAL := 5000.0; (* Max allowable tension in kN *)
    
    (* Intermediate computations *)
    rPitchError         : REAL;
    rRollError          : REAL;
    rMaxTension         : REAL;
    bTensionCrit        : BOOL;
END_VAR

(* === MAIN LOGIC === *)
(* 1. Safety Interlocks *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bAlarmActive := TRUE;
    rPumpCmdFwdAft := 0.0;
    rPumpCmdPortStbd := 0.0;
    bValveSeaWaterIn := FALSE;
    bValveSeaWaterOut := FALSE;
    iState := 0;
    RETURN;
END_IF;

(* 2. Maximum Mooring Tension Check *)
rMaxTension := MAX(rTensionLine1, MAX(rTensionLine2, rTensionLine3));
IF rMaxTension > rMaxTensionLimit THEN
    bTensionCrit := TRUE;
    bAlarmActive := TRUE;
ELSE
    bTensionCrit := FALSE;
END_IF;

(* 3. Simple Low-Pass Filtering for IMU Noise Reduction (Alpha = 0.1) *)
rFilteredPitch := (0.1 * rPitchAngle) + (0.9 * rPrevPitch);
rPrevPitch := rFilteredPitch;
rFilteredRoll := (0.1 * rRollAngle) + (0.9 * rPrevRoll);
rPrevRoll := rFilteredRoll;

(* 4. State Machine for Active Ballast Control *)
CASE iState OF
    0: (* IDLE / OFF *)
        bSystemReady := FALSE;
        rPumpCmdFwdAft := 0.0;
        rPumpCmdPortStbd := 0.0;
        bValveSeaWaterIn := FALSE;
        bValveSeaWaterOut := FALSE;
        
        IF bSystemEnable AND NOT bTensionCrit THEN
            tInitDelay(IN := TRUE, PT := T#3S);
            IF tInitDelay.Q THEN
                tInitDelay(IN := FALSE);
                iState := 10;
            END_IF;
        ELSE
            tInitDelay(IN := FALSE);
        END_IF;
        
    10: (* ACTIVE STABILIZATION *)
        bSystemReady := TRUE;
        
        (* Calculate Pitch/Roll Errors - target is 0.0 degrees *)
        rPitchError := 0.0 - rFilteredPitch;
        rRollError  := 0.0 - rFilteredRoll;
        
        (* Proportional control for transfer pumps (simplified PID) *)
        rPumpCmdFwdAft := LIMIT(-100.0, rPitchError * rKpPitch, 100.0);
        rPumpCmdPortStbd := LIMIT(-100.0, rRollError * rKpRoll, 100.0);
        
        (* Heave compensation (Basic buoyancy adjustment) *)
        IF rHeaveAccel > 2.0 THEN
            bValveSeaWaterIn := FALSE;
            bValveSeaWaterOut := TRUE;
        ELSIF rHeaveAccel < -2.0 THEN
            bValveSeaWaterIn := TRUE;
            bValveSeaWaterOut := FALSE;
        ELSE
            bValveSeaWaterIn := FALSE;
            bValveSeaWaterOut := FALSE;
        END_IF;
        
        (* Emergency state transition if tension becomes critical or disable requested *)
        IF NOT bSystemEnable OR bTensionCrit THEN
            iState := 20;
        END_IF;
        
    20: (* SECURING *)
        (* Gradually ramp down pumps *)
        rPumpCmdFwdAft := rPumpCmdFwdAft * 0.9;
        rPumpCmdPortStbd := rPumpCmdPortStbd * 0.9;
        bValveSeaWaterIn := FALSE;
        bValveSeaWaterOut := FALSE;
        
        IF ABS(rPumpCmdFwdAft) < 1.0 AND ABS(rPumpCmdPortStbd) < 1.0 THEN
            rPumpCmdFwdAft := 0.0;
            rPumpCmdPortStbd := 0.0;
            iState := 0;
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

os.makedirs("c:/Users/majip/Downloads/LLM REASEARCH/data/swarm_raw", exist_ok=True)
filename = f"c:/Users/majip/Downloads/LLM REASEARCH/data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print(f"Saved to {filename}")
